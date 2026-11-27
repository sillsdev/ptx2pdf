r"""Pretore (Netherlands) — live quotations and ordering via their API."""

import os, json, threading, socket, urllib.request, urllib.error, logging

logger = logging.getLogger(__name__)
from shutil import copy
from gi.repository import Gtk, GLib, Gdk
from ptxprint.utils import _, appdirs
from ptxprint.printers.base import PrinterBase, Choice, Spin, BINDING_HARD, BINDING_SADDLE, BINDING_SOFT
from zipfile import ZipFile, ZIP_DEFLATED

querymap = {
    "settings/quantity":    (lambda s: [s.jobCopies()], None, False),
    "settings/description": ("t_prnl_description", str, False),
    "settings/height":      (lambda s: s.height(), int, False),
    "settings/width":       (lambda s: s.width(), int, False),
    "data/11-211-widget-1": ("t_prnl_bookID", str, False),
    "data/8-203-widget-0":  ("t_prnl_description", str, False),
    "data/1-189-widget-4":  ("s_prn_pages", int, False),
    "data/1-189-widget-5":  ("fcb_prnl_paperType", int, False),
    "data/6-200-widget-3":  ("fcb_prnl_coverLamination", int, False),
    "data/31-194-widget-4": ("s_prnl_ribbons", int, True),
    "data/23-135-widget-5": ("fcb_prnl_wrap", int, False),
    "data/22-149-widget-1": ("fcb_prnl_endPapers", int, True)
}

querytypes = {
    "b3a6zov4hypx4eyfrex3cdji": [k for k, v in querymap.items() if not v[2]],
    "bgw3emd69pisfn57743qqcmd": [k for k, v in querymap.items() if v[2]],
    "ql43iqz2c3bx0skgytkbbwe9": list(querymap.keys()),
    "ys08ztakhzsbp8iqfc277v7y": list(querymap.keys()),
}

softqueryremap = {
    "data/1-189-widget-5": {728: 727, 364: 786}
}

def labelWidget(txt, widget, grid, x, y):
    label = Gtk.Label(label=txt)
    label.set_halign(Gtk.Align.END)
    grid.attach(label, x, y, 1, 1)
    grid.attach(widget, x+1, y, 1, 1)


def message(text, error=False, secondary=None):
    dialog = Gtk.MessageDialog(parent=None,
            message_type=Gtk.MessageType.ERROR if error else Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK, text=text)
    if secondary:
        dialog.format_secondary_text(secondary)
    dialog.run()
    dialog.destroy()


def _errorText(result):
    """The reason a server call failed, or None if it didn't."""
    if result is None:
        return _("No response was received from Pretore.")
    if isinstance(result, dict) and "_error" in result:
        return result["_error"]
    return None


class Pretore(PrinterBase):
    pid = "pretore"
    displayName = "Pretore"
    country = "NL"
    countryName = "Netherlands"
    homeCurrency = "EUR"
    url = "https://pretore.com"
    supportsOrders = True
    liveQuotes = True           # estimates come from their API, not a local model

    options = [
        Choice("fcb_prnl_paperType", "Paper Type:", [
            ("755", "40 gsm ThinLeaf FSC"),
            ("789", "50 gsm ThinLeaf FSC"),
            ("728", "70 gsm CVF silk FSC"),             # paperback is 727
            ("364", "80 gsm woodfree offset FSC"),      # paperback is 786
            ("366", "90 gsm woodfree offset FSC")
        ], default="755"),
        Choice("fcb_prnl_endPapers", "End Papers:", [
            ("763", "150 gsm. MultiDesign Natural FSC - same color as thinleaf paper"),
            ("596", "160 gsm. Woodfree offset FSC - same color as offset or CVG paper")
        ], default="763"),
        Choice("fcb_prnl_coverLamination", "Cover Lamination:", [
            ("452", "Gloss"),
            ("453", "Scuff free matte"),
            ("454", "Soft touch"),
            ("455", "Linen"),
        ], default="452"),
        Choice("fcb_prnl_wrap", "Shrink Wrap:", [
            ("475", "Sealfoil (Strong BE13)"),
            ("779", "Sealfoil (Ultra Strong BE19)"),
            ("",    "None"),
        ], default="475"),
        Spin("s_prnl_ribbons", "Ribbons:", lower=0, upper=3, default=0, width=2,
             tip="Number of marker ribbons (Hardcover only)"),
    ]

    outputs = []

    # Paper type ID → mm per page (single page, not leaf)
    _paperThickness = {
        "755": 0.050,   # 40 gsm ThinLeaf
        "789": 0.060,   # 50 gsm Thinopaque
        "727": 0.084,   # 70 gsm
        "728": 0.084,   # 70 gsm
        "364": 0.095,   # 80 gsm woodfree
        "366": 0.105,   # 90 gsm woodfree
    }
    # Binding class → cover thickness in mm (both covers combined)
    _coverThickness = {
        "b3a6zov4hypx4eyfrex3cdji": 1.5,
        "bgw3emd69pisfn57743qqcmd": 1.5,
        "ql43iqz2c3bx0skgytkbbwe9": 8.0,
        "ys08ztakhzsbp8iqfc277v7y": 8.0
    }

    _jobTypes = {               #    soft binding, colour interior
        "b3a6zov4hypx4eyfrex3cdji": (True, False),
        "bgw3emd69pisfn57743qqcmd": (True, True),
        "ql43iqz2c3bx0skgytkbbwe9": (False, True),
        "ys08ztakhzsbp8iqfc277v7y": (False, False)
    }


    MIN_PAGES = 120
    MAX_PAGES = 2000

    def __init__(self, view):
        super().__init__(view)
        self.user = None
        self.thread = None
        self._autoDescription = None
        self._accountsDone = False
        self._quoteKey = None       # JobSpec.key() the cached quote was made for
        self._quoteCache = {}       # {qty: perCopy EUR}
        self._pendingKey = None

    def bookType(self, job=None):
        if job is None:
            job = self.view.printerTab.jobSpec()
        soft = job.binding in (BINDING_SADDLE, BINDING_SOFT)
        for k, v in self._jobTypes.items():
            if soft == v[0] and job.color == v[1]:
                return k, soft

    def jobCopies(self):
        v = self.get("s_prn_copies")
        return int(float(v)) if v else 0

    def height(self):
        (width, height) = self.view.calcPageSize()
        return height

    def width(self):
        (width, height) = self.view.calcPageSize()
        return width

    def prepare(self):
        if not self.get("t_prnl_bookID"):
            prjid = getattr(self.view.project, 'prjid', None)
            if prjid:
                self.set("t_prnl_bookID", prjid)
        bks = self.view.getBooks(files=True)
        if bks:
            if len(bks) == 1:
                autoDesc = bks[0]
            elif len(bks) <= 4:
                autoDesc = ",".join(bks)
            else:
                autoDesc = "{}...{}".format(bks[0], bks[-1])
            current = self.get("t_prnl_description")
            if not current or current == self._autoDescription:
                self.set("t_prnl_description", autoDesc)
                self._autoDescription = autoDesc
        self._updateButtonSensitivity()
        if self._accountsDone:
            return
        self._accountsDone = True
        self.configdir = os.path.join(appdirs.user_config_dir("ptxprint", "SIL"), "printers", "pretore")
        os.makedirs(self.configdir, exist_ok=True)
        self.accounts = {}
        for f in os.listdir(self.configdir):
            if f.endswith(".json"):
                self.read_account(os.path.join(self.configdir, f))
        if len(self.accounts):
            self.user = list(self.accounts.keys())[0]
            self.set("l_prnl_userid", self.user)

    def warnings(self, job):
        w = []
        if job.pages and not (self.MIN_PAGES <= job.pages <= self.MAX_PAGES):
            w.append(f"Pretore accepts {self.MIN_PAGES}–{self.MAX_PAGES} pages.")
        if job.binding == BINDING_SADDLE:
            w.append("Saddle-stitching is not offered; Paperback is quoted instead.")
        if job.color:
            w.append("Quotations do not vary by interior colour.")
        if not self._accountsDone or self.user is None:
            w.append("No account configured — use Select Account to enable live quotes.")
        return w

    def estimate(self, job, quantities):
        """The cached API quote, if it still matches the job; else None."""
        if self._quoteKey == job.key() and self._quoteCache:
            return dict(self._quoteCache)
        return None

    def estimateAsync(self, job, quantities, callback):
        """Fetch per-copy EUR prices from the API for each quantity.

        callback({qty: perCopyEUR} or None) runs on the GTK main loop.
        """
        self.prepare()
        if self._accountProblem() or not self.get("t_prnl_bookID") or not self.get("t_prnl_description"):
            callback(None)
            return
        self._pendingKey = job.key()
        def _cb(result):
            if _errorText(result) or 'cost' not in result:
                logger.warning(f"Pretore quote failed: {_errorText(result) or result}")
                callback(None)
                return
            data = {int(k): v / int(k) for k, v in result['cost'].items() if int(k) > 0}
            self._quoteKey = self._pendingKey
            self._quoteCache = dict(data)
            callback(data)
        self.do_quote("calculate", cb=_cb, quantities=quantities, job=job)

    def thicknessText(self, job):
        paperID = self.get("fcb_prnl_paperType") or "755"
        mmPerPage = self._paperThickness.get(paperID, 0.050)
        coverMm = self._coverThickness.get(self.bookType(job)[0], 1.5)
        return "{:.1f} mm".format(job.pages * mmPerPage + coverMm)

    def panelExtras(self, panel):
        panel.addEntryRow("t_prnl_bookID", _("Book Identifier:"),
                          onChanged=self._updateButtonSensitivity)
        panel.addEntryRow("t_prnl_description", _("Description:"),
                          onChanged=self._updateButtonSensitivity)
        accountBtn = panel.addButtonRow("btn_prnl_selectAccount", _("Account..."),
                                        self.select_account,
                                        labelWid="l_prnl_userid")
        quoteBtn = panel.addButtonRow("btn_prnl_getQuote", _("Get Precise Quotation"),
                                      self.quote)
        orderBtn = panel.addButtonRow("btn_prnl_createOrder", _("Create Order"),
                                      self.createOrder,
                                      labelWid="l_prnl_orderRef", labelCaption=_("Ref:"),
                                      labelDefault="-")

        fileStatusGrid = Gtk.Grid()
        fileStatusGrid.set_row_spacing(1)
        fileStatusGrid.set_column_spacing(8)

        zipLabel = Gtk.Label(label=_("File to upload:"))
        zipLabel.set_halign(Gtk.Align.END)
        fileStatusGrid.attach(zipLabel, 0, 0, 1, 1)
        zipBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        zipVal = Gtk.Label(label="-")
        zipVal.set_halign(Gtk.Align.START)
        panel.expose("l_prnl_zipFilename", zipVal)
        zipBox.pack_start(zipVal, False, False, 0)
        cpBtn = Gtk.Button.new_from_icon_name("edit-copy-symbolic", Gtk.IconSize.BUTTON)
        cpBtn.set_relief(Gtk.ReliefStyle.NONE)
        cpBtn.set_tooltip_text(_("Copy the full path of the .zip file"))
        cpBtn.connect("clicked", self.copy_zipfname)
        panel.expose("b_prn_cpzip", cpBtn)
        zipBox.pack_start(cpBtn, False, False, 0)
        fileStatusGrid.attach(zipBox, 1, 0, 1, 1)

        statusLabel = Gtk.Label(label=_("Status:"))
        statusLabel.set_halign(Gtk.Align.END)
        fileStatusGrid.attach(statusLabel, 0, 1, 1, 1)
        statusBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        statusVal = Gtk.Label(label="-")
        statusVal.set_halign(Gtk.Align.START)
        panel.expose("l_prnl_orderStatus", statusVal)
        statusBox.pack_start(statusVal, False, False, 0)
        link = Gtk.LinkButton(uri="https://ptxprint.pretore.com/login/",
                label=_("Complete Order & Payment via website"))
        link.set_halign(Gtk.Align.START)
        panel.expose("lb_prnl_completeOrder", link)
        statusBox.pack_start(link, False, False, 0)
        fileStatusGrid.attach(statusBox, 1, 1, 1, 1)

        panel.grid.attach(fileStatusGrid, 0, panel._row, 2, 1)
        panel._row += 1

    def _updateButtonSensitivity(self, *a):
        ok = bool(self.get("t_prnl_bookID")) and bool(self.get("t_prnl_description"))
        for wid in ("btn_prnl_getQuote", "btn_prnl_createOrder"):
            w = self.view.builder.get_object(wid)
            if w:
                w.set_sensitive(ok)

    def read_account(self, fname):
        try:
            with open(fname, encoding="utf-8") as inf:
                data = json.load(inf)
        except (OSError, ValueError) as e:
            logger.warning(f"Unreadable Pretore account file {fname}: {e}")
            return None
        if not isinstance(data, dict) or 'email' not in data:
            return None
        k = data['email']
        self.accounts[k] = data
        return k

    def select_account(self, btn, *a):
        self.prepare()
        dialog = Gtk.Dialog(title="Accounts", transient_for=self.view.mainapp.win)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OK, Gtk.ResponseType.OK)
        content = dialog.get_content_area()
        grid = Gtk.Grid()
        grid.set_border_width(15)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        content.add(grid)
        combo = Gtk.ComboBoxText()
        default = 0
        for i, k in enumerate(sorted(self.accounts.keys())):
            combo.append_text(k)
            if k == self.user:
                default = i
        combo.set_active(default)
        labelWidget(_("Choose Account:"), combo, grid, 0, 0)

        file_button = Gtk.FileChooserButton(title="Select Key File",
                action=Gtk.FileChooserAction.OPEN)
        labelWidget(_("Import Account File:"), file_button, grid, 0, 1)

        link = Gtk.LinkButton(uri="https://ptxprint.pretore.com/login/",
                label=_("Register / download account key at pretore.com"))
        link.set_halign(Gtk.Align.START)
        grid.attach(link, 0, 2, 2, 1)

        grid.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            fname = file_button.get_filename()
            if fname is not None:
                count = 1
                skey = os.path.join(self.configdir, f"key_{count}.json")
                while os.path.exists(skey):
                    count += 1
                    skey = os.path.join(self.configdir, f"key_{count}.json")
                copy(fname, skey)
                user = self.read_account(skey)
                if user is None:
                    os.remove(skey)
                    message(_("That file is not a Pretore account key."), error=True,
                            secondary=_("Download the account key (.json) from pretore.com and import that file."))
                else:
                    self.user = user
            else:
                self.user = combo.get_active_text()
            self.set("l_prnl_userid", self.user)
        dialog.destroy()

    def prepare_quote(self, quantities=None, job=None):
        booktype, issoft = self.bookType(job)
        qinfo = {}
        for k in querytypes[booktype]:
            v, t, hardonly = querymap[k]
            if isinstance(v, str):
                val = self.get(v)
            else:
                val = v(self)
            if val is None or val == "":     # e.g. Shrink Wrap "None"
                continue
            if t is not None:
                val = t(val)
            if issoft and k in softqueryremap:
                    val = softqueryremap[k].get(val, val)
            b = k.split("/")
            c = qinfo
            for bk in b[:-1]:
                c = qinfo.setdefault(bk, {})
            c[b[-1]] = val
        if quantities is not None:
            qinfo["settings"]["quantity"] = quantities
        logger.debug(f"{booktype=}, {qinfo}")
        return booktype, qinfo

    def submit_quote(self, qinfo, endpoint, cb=None):
        """Run the request on a worker thread; cb(result) runs on the GTK main loop.

        Never blocks the UI. If a request is already in flight, cb gets an error
        result rather than the request being silently dropped.
        """
        if cb is None:
            cb = self.updatequote
        if self.thread is not None and self.thread.is_alive():
            GLib.idle_add(cb, {"_error": _("Still waiting for Pretore to answer an earlier request. "
                                           "Please try again in a moment.")})
            return
        self.thread = threading.Thread(target=self.url_query, args=(cb, endpoint, qinfo))
        self.thread.daemon = True
        self.thread.start()

    def updatequote(self, result):
        logger.debug(f"{result=}")
        self._updateButtonSensitivity()
        err = _errorText(result)
        if err is None and 'cost' not in result:
            err = _("Pretore's reply did not include a price.")
        if err:
            message(_("Could not get a quotation from Pretore"), error=True, secondary=err)
            return
        copies = self.jobCopies()
        if copies <= 0:
            message(_("Set the number of copies to get a quotation."))
            return
        amount = result['cost'].get(str(copies), None)
        if amount is None:
            message(_("Pretore did not quote for {} copies.").format(copies), error=True,
                    secondary=_("Quantities quoted: {}").format(", ".join(result['cost'].keys()) or "-"))
            return
        self._quoteKey = self._pendingKey
        self._quoteCache = {copies: amount / copies}
        tab = getattr(self.view, 'printerTab', None)
        if tab is not None:
            tab.updateAll()
        try:
            message(_("Pretore quotation for {} copies: €{:,.2f} (€{:,.2f} per copy)").format(
                        copies, float(amount), float(amount) / copies))
        except (TypeError, ValueError):
            message(_("Pretore quotation for {} copies: {}").format(copies, amount))

    def showCreateResults(self, result):
        self._updateButtonSensitivity()
        err = _errorText(result)
        if err is None and not result.get("number"):
            err = _("Pretore's reply did not include an order number.")
        if err:
            self.set("l_prnl_orderStatus", _("(order not created)"))
            message(_("The order could not be created at Pretore"), error=True, secondary=err)
            return
        self.set("l_prnl_orderRef", result["number"])
        self.set("l_prnl_zipFilename", os.path.basename(self.zipname))
        self.set("l_prnl_orderStatus", _("(awaiting payment)"))

    def url_query(self, callback, endpoint, *a):
        """Worker-thread side of submit_quote. Always calls back exactly once."""
        result = None
        try:
            auth = self.accounts[self.user]['api_key']
            headers = {'User-Agent': "Mozilla/5.0 (Windows NT 11.0; Win64; x64)",
                       'Content-Type': 'application/json',
                       'Authorization': f'Bearer {auth}'}
            data = json.dumps(a[0], ensure_ascii=False).encode("utf-8") if len(a) else None
            logger.debug(f"{endpoint=}, {data=}")
            req = urllib.request.Request(endpoint, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as response:
                if response.getcode() == 200:
                    result = json.loads(response.read().decode("utf-8"))
                else:
                    result = {"_error": _("Pretore replied with status {}.").format(response.getcode())}
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode('utf-8', errors='replace')
                detail = json.loads(body).get("message", "")    # WordPress REST errors carry a message
            except Exception:
                detail = body[:300]
            logger.warning(f"Pretore HTTP {e.code}: {body}")
            if e.code in (401, 403):
                msg = _("Pretore did not accept your account key. Re-download it from pretore.com and import it again.")
            else:
                msg = _("Pretore reported an error ({}).").format(e.code)
            result = {"_error": msg + ("\n\n" + detail if detail else "")}
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError) as e:
            logger.warning(f"Pretore connection failed: {e}")
            result = {"_error": _("Could not connect to Pretore. Check your internet connection and try again.")
                                + f"\n\n({getattr(e, 'reason', e)})"}
        except ValueError as e:     # bad JSON in the reply
            result = {"_error": _("Pretore sent a reply that could not be read.") + f"\n\n({e})"}
        except Exception as e:
            logger.exception("Pretore request failed")
            result = {"_error": f"{type(e).__name__}: {e}"}
        GLib.idle_add(callback, result)

    def _accountProblem(self):
        """A user-facing reason the current account can't be used, or None if it's fine."""
        if self.user is None or self.user not in getattr(self, 'accounts', {}):
            return _("Select or import a Pretore account first (Account... button).")
        acct = self.accounts[self.user]
        missing = [k for k in ('UUID', 'api_key') if not acct.get(k)]
        if missing:
            return _("The account key file for {} is incomplete (missing {}). "
                     "Re-download it from pretore.com and import it again.").format(self.user, ", ".join(missing))
        return None

    def do_quote(self, command, cb=None, quantities=None, job=None):
        if cb is None:
            cb = self.updatequote
        try:
            booktype, qinfo = self.prepare_quote(quantities=quantities, job=job)
        except (ValueError, TypeError) as e:
            GLib.idle_add(cb, {"_error": _("One of the printing options has an invalid value.")
                                         + f"\n\n({e})"})
            return
        uuid = self.accounts[self.user]['UUID']
        endpoint = f"https://ptxprint.pretore.com/wp-json/emily/v1/calculation/{uuid}/{booktype}/{command}"
        self.submit_quote(qinfo, endpoint, cb=cb)

    def quote(self, btn, *a):
        self.prepare()
        problem = self._accountProblem()
        if problem:
            message(problem)
            return
        btn.set_sensitive(False)        # re-enabled by updatequote
        tab = getattr(self.view, 'printerTab', None)
        self._pendingKey = tab.jobSpec().key() if tab is not None else None
        self.do_quote("calculate")

    def _orderFiles(self):
        """[(path, nameInZip)] for the last print, or raise ValueError with a user-facing reason."""
        pdfFiles = getattr(self.view, 'pdfFiles', None)
        if not pdfFiles:
            raise ValueError(_("Print the job first to create the PDF files to upload."))
        # Everything the print produced goes: the finished PDF as Final.pdf, the prepress PDF
        # (all pages, in order, before inserts were pulled out) as Original.pdf, the cover
        # and any extracted inserts (e.g. maps) under their own names.
        # TODO: confirm with Martin which of these Pretore actually needs.
        res = []
        for k, v in pdfFiles.items():
            if k == " Original" and ' Finished' in pdfFiles and not (v and os.path.exists(v)):
                continue        # a by-product that couldn't be saved; don't block the order for it
            outkey = k.strip()
            if k == " Original" and ' Finished' not in pdfFiles:
                outkey = "Final"
            elif outkey == "Finished":
                outkey = "Final"
            res.append((v, outkey + ".pdf"))
        missing = [p for p, _n in res if not p or not os.path.exists(p)]
        if missing:
            raise ValueError(_("These PDF files from the last print can no longer be found:")
                             + "\n" + "\n".join(str(p) for p in missing)
                             + "\n\n" + _("Print the job again, then click Create Order."))
        return res

    def createOrder(self, btn, *a):
        self.prepare()
        problem = self._accountProblem()
        if problem:
            message(problem)
            return
        try:
            files = self._orderFiles()
        except ValueError as e:
            message(_("Cannot create the order yet"), error=True, secondary=str(e))
            return
        zipname = self.view.getPDFname(noext=True) + "_pretore.zip"
        tmpname = zipname + ".tmp"
        try:        # build to a temp file so a failure never leaves a half-written zip behind
            with ZipFile(tmpname, "w", compression=ZIP_DEFLATED) as z:
                for path, arcname in files:
                    z.write(path, arcname)
            os.replace(tmpname, zipname)
        except OSError as e:
            try:
                os.remove(tmpname)
            except OSError:
                pass
            message(_("Could not create the upload file"), error=True,
                    secondary=f"{zipname}\n\n{e.strerror or e}")
            return
        self.zipname = zipname
        self.set("l_prnl_zipFilename", os.path.basename(zipname))
        self.set("l_prnl_orderStatus", _("(creating order…)"))
        btn.set_sensitive(False)        # re-enabled by showCreateResults
        self.do_quote("create", cb=self.showCreateResults)

    def configure(self, btn, *a):
        # setup the view to conform to pretore requirements
        return

    def copy_zipfname(self, btn, *a):
        if not getattr(self, 'zipname', None):
            return
        zname = os.path.abspath(self.zipname)
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(zname, -1)
        clipboard.store()
