
import os, json, threading, urllib, time, logging

logger = logging.getLogger(__name__)
from shutil import copy
from gi.repository import Gtk, GLib, Gdk
from ptxprint.utils import _, appdirs
from ptxprint.printers.currency import allcurrencies, getExchangeRates
from zipfile import ZipFile, ZIP_DEFLATED

querymap = {
    "settings/quantity":    (lambda s:[int(s.get("s_prnl_copies"))], None),
    "settings/description": ("t_prnl_description", str),
    "settings/height":      (lambda s:s.height(), int),
    "settings/width":       (lambda s:s.width(), int),
    "data/11-211-widget-1": ("t_prnl_bookID", str),
    "data/8-203-widget-0":  ("t_prnl_description", str),
    "data/1-189-widget-4":  ("s_prnl_pages", int),
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


class Pretore:
    displayName = "Pretore"
    homeCurrency = "EUR"

    def __init__(self, view):
        self.view = view
        self.user = None
        self.exchangeRates = getExchangeRates()
        self.currency = "EUR"
        self.thread = None
        self._autoDescription = None
        self._widgetsDone = False

    def get(self, wname, **kw):
        return self.view.get(wname, **kw)

    def set(self, wname, val, **kw):
        return self.view.set(wname, val, **kw)

    def _ratesArrived(self, rates):
        GLib.idle_add(self._populateCurrencyCombo)

    def _populateCurrencyCombo(self):
        combo = self.view.builder.get_object("fcb_prnl_currency")
        if combo is None:
            return
        current = self.currency
        combo.remove_all()
        for code in sorted(self.exchangeRates.rates.keys()):
            combo.append(code, code)
        combo.set_active_id(current)

    # Paper type ID → mm per page (single page, not leaf)
    _paperThickness = {
        "755": 0.050,   # 40 gsm ThinLeaf
        "355": 0.060,   # 50 gsm Thinopaque
        "364": 0.095,   # 80 gsm woodfree
        "366": 0.105,   # 90 gsm woodfree
        "575": 0.115,   # 100 gsm woodfree
    }
    # Binding type ID → cover thickness in mm (both covers combined)
    _coverThickness = {
        "307": 1.5,     # Paperback (light card)
        "306": 8.0,     # Hardback (boards + liner)
    }

    def _updateThickness(self, *a):
        numpages = self.numpages() or 0
        paperID  = self.get("fcb_prnl_paperType") or "755"
        bindID   = self.get("fcb_prnl_binding")   or "307"
        mmPerPage = self._paperThickness.get(paperID, 0.050)
        coverMm   = self._coverThickness.get(bindID, 1.5)
        thickness = numpages * mmPerPage + coverMm
        self.set("l_prnl_thickness", "{:.1f} mm".format(thickness))

    def _updateButtonSensitivity(self, *a):
        ok = bool(self.get("t_prnl_bookID")) and bool(self.get("t_prnl_description"))
        for wid in ("btn_prnl_getQuote", "btn_prnl_createOrder", "btn_prnl_multiQuote"):
            w = self.view.builder.get_object(wid)
            if w:
                w.set_sensitive(ok)

    def _applyPageCountStyle(self, numpages):
        w = self.view.builder.get_object("s_prnl_pages")
        if w is None:
            return
        ctx = w.get_style_context()
        if numpages < 120 or numpages > 2000:
            ctx.add_class("red-label")
        else:
            ctx.remove_class("red-label")

    def setup(self):
        actualcount = self.view.getPageCount()
        if actualcount is not None:
            self.set("s_prnl_pages", actualcount)
            self._applyPageCountStyle(actualcount)
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
        self._updateThickness()
        self._updateButtonSensitivity()
        if not self._widgetsDone:
            self._widgetsDone = True
            for wid in ("t_prnl_bookID", "t_prnl_description"):
                w = self.view.builder.get_object(wid)
                if w:
                    w.connect("changed", self._updateButtonSensitivity)
            for wid in ("fcb_prnl_paperType", "fcb_prnl_binding"):
                w = self.view.builder.get_object(wid)
                if w:
                    w.connect("changed", self._updateThickness)
            w = self.view.builder.get_object("s_prnl_pages")
            if w:
                w.connect("value-changed", self._updateThickness)
        if self.user is not None:
            return
        self.exchangeRates.startFetch(onDone=self._ratesArrived)
        self.configdir = os.path.join(appdirs.user_config_dir("ptxprint", "SIL"), "printers", "pretore")
        os.makedirs(self.configdir, exist_ok=True)

        self.accounts = {}
        for f in os.listdir(self.configdir):
            if f.endswith(".json"):
                self.read_account(os.path.join(self.configdir, f))
        if len(self.accounts):
            self.user = list(self.accounts.keys())[0]
            self.set("l_prnl_userid", self.user)

    def prepare(self):
        self.setup()

    def refreshPageCount(self):
        actualcount = self.view.getPageCount()
        if actualcount is not None:
            self.set("s_prnl_pages", actualcount)
            self._applyPageCountStyle(actualcount)
            self._updateThickness()

    def read_account(self, fname):
        with open(fname, encoding="utf-8") as inf:
            data = json.load(inf)
        if not isinstance(data, dict) or 'email' not in data:
            return None
        k = data['email']
        self.accounts[k] = data
        return k

    def height(self):
        (width, height) = self.view.calcPageSize()
        return height

    def width(self):
        (width, height) = self.view.calcPageSize()
        return width

    def numpages(self):
        v = self.get("s_prnl_pages")
        return int(float(v)) if v else None

    def select_account(self, btn, *a):
        olduser = self.user
        self.user = None
        self.setup()        # force a setup again
        self.user = olduser
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

    def prepare_quote(self, quantities=None):
        booktype = self.get("fcb_prnl_binding", default="307")
        qinfo = {}
        for k in querytypes[booktype]:
            v, t = querymap[k]
            if isinstance(v, str):
                val = self.get(v)
            else:
                val = v(self)
            if val is None:
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

    def _refreshCurrencyDisplay(self):
        if not hasattr(self, 'amount') or self.amount is None:
            return
        copies = int(self.get("s_prnl_copies"))
        amount = (self.exchangeRates.rate(self.currency) or 1.0) * self.amount
        cs = allcurrencies.get(self.currency, "\u20AC")
        self.set('l_prnl_total', "{}{:.2f}".format(cs, amount))
        self.set('l_prnl_percopy', "{}{:.2f}".format(cs, amount / copies))

    def updatequote(self, result, curr):
        if result is None:
            print("Failed quote")
            return
        if curr is not None:
            self.currency = curr
        copies = int(self.get("s_prnl_copies"))
        self.amount = result['cost'][str(copies)]
        self._refreshCurrencyDisplay()

    def getEstimateAsync(self, quantities, callback):
        """Fetch per-copy prices from the API for each quantity.

        callback({qty: perCopyEUR}) runs on the GTK main loop; called with
        None when no account is configured, the job fields are incomplete,
        or the quote fails.
        """
        self.setup()
        if self.user is None or not self.get("t_prnl_bookID") or not self.get("t_prnl_description"):
            callback(None)
            return
        def _cb(result, curr):
            if result is None or 'cost' not in result:
                print("Failed quote")
                callback(None)
                return
            callback({int(k): v / int(k) for k, v in result['cost'].items()})
        self.do_quote("calculate", cb=_cb, quantities=quantities)

    def showCreateResults(self, result, curr):
        if result is None:
            logger.debug("showCreateResults: no result returned")
            return
        quoteid = result.get("number", _("Unknown"))
        self.set("l_prnl_orderRef", quoteid)
        self.set("l_prnl_zipFilename", os.path.basename(self.zipname))

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
        # if rates are still unavailable after a grace period, fall back to EUR
        curr = None if self.exchangeRates.wait(10) else "EUR"
        GLib.idle_add(callback, result, curr)

    def do_quote(self, command, cb=None, quantities=None):
        if cb is None:
            cb = self.updatequote
        booktype, qinfo = self.prepare_quote(quantities=quantities)
        uuid = self.accounts[self.user]['UUID']
        endpoint = f"https://ptxprint.pretore.com/wp-json/emily/v1/calculation/{uuid}/{booktype}/{command}"
        self.submit_quote(qinfo, endpoint, cb=cb)

    def quote(self, btn, *a):
        btn.set_sensitive(False)
        self.setup()
        self.do_quote("calculate")
        btn.set_sensitive(True)

    def createOrder(self, btn, *a):
        if getattr(self.view, 'pdfFiles', None) is None or not len(self.view.pdfFiles):
            message("Print the job to create the files to upload")
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

    def change_currency(self, w, *a):
        curr = self.get("fcb_prnl_currency")
        if self.exchangeRates.rate(curr) is not None:
            self.currency = curr
            self._refreshCurrencyDisplay()

    def show_multi_quote_comparison(self, btn, *a):
        from ptxprint.printers import comparePrinterPrices
        btn.set_sensitive(False)
        comparePrinterPrices(self.view)
        btn.set_sensitive(True)
