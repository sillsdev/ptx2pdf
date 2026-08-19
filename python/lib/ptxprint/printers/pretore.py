r"""Pretore (Netherlands) — live quotations and ordering via their API."""

import os, json, threading, urllib, logging

logger = logging.getLogger(__name__)
from shutil import copy
from gi.repository import Gtk, GLib, Gdk
from ptxprint.utils import _, appdirs
from ptxprint.printers.base import PrinterBase, Choice, Spin, BINDING_HARD, BINDING_SADDLE
from zipfile import ZipFile, ZIP_DEFLATED

querymap = {
    "settings/quantity":    (lambda s: [s.jobCopies()], None),
    "settings/description": ("t_prnl_description", str),
    "settings/height":      (lambda s: s.height(), int),
    "settings/width":       (lambda s: s.width(), int),
    "data/11-211-widget-1": ("t_prnl_bookID", str),
    "data/8-203-widget-0":  ("t_prnl_description", str),
    "data/1-189-widget-4":  ("s_prn_pages", int),
    "data/1-189-widget-5":  ("fcb_prnl_paperType", int),
    "data/6-200-widget-3":  ("fcb_prnl_coverLamination", int),
    "data/31-194-widget-4": ("s_prnl_ribbons", int),
    "data/23-135-widget-5": ("fcb_prnl_wrap", int)
}

querytypes = {
    "306": list(querymap.keys()),
    "307": [k for k in querymap.keys() if k != "data/31-194-widget-4"]
}

def labelWidget(txt, widget, grid, x, y):
    label = Gtk.Label(label=txt)
    label.set_halign(Gtk.Align.END)
    grid.attach(label, x, y, 1, 1)
    grid.attach(widget, x+1, y, 1, 1)


def message(text):
    dialog = Gtk.MessageDialog(parent=None, message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK, text=text)
    dialog.run()
    dialog.destroy()


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
            ("355", "50 gsm Thinopaque white FSC"),
            ("364", "80 gsm woodfree offset FSC"),
            ("366", "90 gsm woodfree offset FSC"),
            ("575", "100 gsm woodfree offset FSC"),
        ], default="755"),
        Choice("fcb_prnl_coverLamination", "Cover Lamination:", [
            ("455", "Gloss"),
            ("453", "Scuff free matte"),
            ("452", "Linen"),
        ], default="455"),
        Choice("fcb_prnl_wrap", "Shrink Wrap:", [
            ("475", "Sealfoil (Strong BE13)"),
            ("779", "Sealfoil (Ultra Strong BE19)"),
            ("",    "None"),
        ], default="475"),
        Spin("s_prnl_ribbons", "Ribbons:", lower=0, upper=3, default=0, width=2,
             tip="Number of marker ribbons (Hardback only)"),
    ]

    outputs = []

    # Paper type ID → mm per page (single page, not leaf)
    _paperThickness = {
        "755": 0.050,   # 40 gsm ThinLeaf
        "355": 0.060,   # 50 gsm Thinopaque
        "364": 0.095,   # 80 gsm woodfree
        "366": 0.105,   # 90 gsm woodfree
        "575": 0.115,   # 100 gsm woodfree
    }
    # Binding class → cover thickness in mm (both covers combined)
    _coverThickness = {
        "307": 1.5,     # Paperback (light card)
        "306": 8.0,     # Hardback (boards + liner)
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
        return "306" if job.binding == BINDING_HARD else "307"

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
        if self.user is None or not self.get("t_prnl_bookID") or not self.get("t_prnl_description"):
            callback(None)
            return
        self._pendingKey = job.key()
        def _cb(result):
            if result is None or 'cost' not in result:
                print("Failed quote")
                callback(None)
                return
            data = {int(k): v / int(k) for k, v in result['cost'].items()}
            self._quoteKey = self._pendingKey
            self._quoteCache = dict(data)
            callback(data)
        self.do_quote("calculate", cb=_cb, quantities=quantities, job=job)

    def thicknessText(self, job):
        paperID = self.get("fcb_prnl_paperType") or "755"
        mmPerPage = self._paperThickness.get(paperID, 0.050)
        coverMm = self._coverThickness.get(self.bookType(job), 1.5)
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
        with open(fname, encoding="utf-8") as inf:
            data = json.load(inf)
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
                self.user = self.read_account(skey)
            else:
                self.user = combo.get_active_text()
            self.set("l_prnl_userid", self.user)
        dialog.destroy()

    def prepare_quote(self, quantities=None, job=None):
        booktype = self.bookType(job)
        qinfo = {}
        for k in querytypes[booktype]:
            v, t = querymap[k]
            if isinstance(v, str):
                val = self.get(v)
            else:
                val = v(self)
            if val is None or val == "":     # e.g. Shrink Wrap "None"
                continue
            if t is not None:
                val = t(val)
            b = k.split("/")
            c = qinfo
            for bk in b[:-1]:
                c = qinfo.setdefault(bk, {})
            c[b[-1]] = val
        if quantities is not None:
            qinfo["settings"]["quantity"] = quantities
        return booktype, qinfo

    def submit_quote(self, qinfo, endpoint, cb=None):
        if cb is None:
            cb = self.updatequote
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.url_query, args=(cb, endpoint, qinfo))
            self.thread.daemon = True
            self.thread.start()
        self.thread.join(30)
        if not self.thread.is_alive():
            self.thread = None

    def updatequote(self, result):
        if result is None or 'cost' not in result:
            print("Failed quote")
            return
        copies = self.jobCopies()
        amount = result['cost'].get(str(copies), None)
        if amount is None:
            return
        self._quoteKey = self._pendingKey
        self._quoteCache = {copies: amount / copies}
        tab = getattr(self.view, 'printerTab', None)
        if tab is not None:
            tab.updateAll()

    def showCreateResults(self, result):
        if result is None:
            logger.debug("showCreateResults: no result returned")
            return
        quoteid = result.get("number", _("Unknown"))
        self.set("l_prnl_orderRef", quoteid)
        self.set("l_prnl_zipFilename", os.path.basename(self.zipname))
        self.set("l_prnl_orderStatus", _("(awaiting payment)"))

    def url_query(self, callback, endpoint, *a):
        auth = self.accounts[self.user]['api_key']
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 11.0; Win64; x64)",
                   'Content-Type': 'application/json',
                   'Authorization': f'Bearer {auth}'}
        if len(a):
            data = json.dumps(a[0], ensure_ascii=False).encode("utf-8")
        else:
            data = None
        result = None
        logger.debug(f"{headers=}, {endpoint=}, {data=}")
        try:
            req = urllib.request.Request(endpoint, data=data, headers=headers)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    result = json.loads(response.read().decode("utf-8"))
                else:
                    print (f"Response code: {response.getcode()}")
        except urllib.error.HTTPError as e:
            print(f"Error: {e}\nHeaders: {e.headers}\nBody: {e.read().decode('utf-8')}")
        GLib.idle_add(callback, result)

    def do_quote(self, command, cb=None, quantities=None, job=None):
        if cb is None:
            cb = self.updatequote
        booktype, qinfo = self.prepare_quote(quantities=quantities, job=job)
        uuid = self.accounts[self.user]['UUID']
        endpoint = f"https://ptxprint.pretore.com/wp-json/emily/v1/calculation/{uuid}/{booktype}/{command}"
        self.submit_quote(qinfo, endpoint, cb=cb)

    def quote(self, btn, *a):
        btn.set_sensitive(False)
        self.prepare()
        if self.user is not None:
            tab = getattr(self.view, 'printerTab', None)
            self._pendingKey = tab.jobSpec().key() if tab is not None else None
            self.do_quote("calculate")
        else:
            message(_("Select or import a Pretore account first"))
        btn.set_sensitive(True)

    def createOrder(self, btn, *a):
        if getattr(self.view, 'pdfFiles', None) is None or not len(self.view.pdfFiles):
            message(_("Print the job to create the files to upload"))
            return
        self.zipname = self.view.getPDFname(noext=True) + "_pretore.zip"
        z = ZipFile(self.zipname, "w", compression=ZIP_DEFLATED)
        for k, v in self.view.pdfFiles.items():
            outkey = k.strip()
            if k == " Original" and ' Finished' not in self.view.pdfFiles:
                outkey = "Final"
            elif outkey == "Finished":
                outkey = "Final"
            z.write(v, outkey+".pdf")
        z.close

        # also make the zip, create a dialog to present the results
        self.do_quote("create", cb=self.showCreateResults)

    def configure(self, btn, *a):
        # setup the view to conform to pretore requirements
        return

    def copy_zipfname(self, btn, *a):
        zname = os.path.abspath(self.zipname)
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(zname, -1)
        clipboard.store()
