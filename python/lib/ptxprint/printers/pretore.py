
import os, json, threading, urllib, time
from shutil import copy
from gi.repository import Gtk, GLib, Gdk
from ptxprint.utils import _, appdirs
from ptxprint.printers import allcurrencies
from ptxprint.printers.pricing_graph import PricingGraphViewer
from zipfile import ZipFile, ZIP_DEFLATED

querymap = {
    "settings/quantity":    (lambda s:[int(s.get("s_prnl_copies"))], None),
    "settings/description": ("t_prnl_description", str),
    "settings/height":      (lambda s:s.height(), int),
    "settings/width":       (lambda s:s.width(), int),
    "data/11-211-widget-1": ("t_prnl_bookID", str),
    "data/8-203-widget-0":  ("t_prnl_description", str),
    "data/1-189-widget-4":  ("l_prnl_pages", int),
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
    def __init__(self, view):
        self.view = view
        self.user = None
        self.rates = {}
        self.currency = "EUR"
        self.thread = None
        self.exchange_thread = None

    def get(self, wname, **kw):
        return self.view.get(wname, **kw)

    def set(self, wname, val, **kw):
        return self.view.set(wname, val, **kw)

    def get_exchange_rates(self, force=False):
        if not force and len(self.rates):
            return self.rates
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 11.0; Win64; x64)"}
        url = f"https://api.frankfurter.dev/v1/latest?base=EUR&symbols="+",".join(sorted(allcurrencies.keys()))
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    rates = data.get('rates', {})
                else:
                    print (f"Response code: {response.getcode()}")
        except Exception as e:
            print(f"Error: {e}")
            return
        GLib.idle_add(self.set_exchange_rates, rates)

    def set_exchange_rates(self, rates):
        self.rates = rates

    def setup(self):
        numpages = self.numpages()
        self.set("l_prnl_pages", str(numpages))
        w = self.view.builder.get_object("l_prnl_pages").get_style_context()
        if numpages < 120 or numpages > 2000:
            w.add_class("red-label")
        else:
            w.remove_class("red-label")
        if self.user is not None:
            return
        self.exchange_thread = threading.Thread(target=self.get_exchange_rates)
        self.exchange_thread.start()
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
        return self.view.getPageCount()

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

    def updatequote(self, result, curr):
        if result is None:
            print("Failed quote")
            return
        if curr is not None:
            self.currency = curr
        copies = int(self.get("s_prnl_copies"))
        self.amount = result['cost'][str(copies)]
        amount = self.rates.get(self.currency, 1.0) * self.amount
        cs = allcurrencies.get(self.currency, "\u20AC")
        self.set('l_prnl_total', "{}{:.2f}".format(cs, amount))
        self.set('l_prnl_percopy', "{}{:.2f}".format(cs ,amount/copies))

    def updateMultiQuote(self, result, curr):
        if result is None:
            print("Failed quote")
            return
        if curr is not None:
            self.currency = curr
        currFactor = self.rates.get(self.currency, 1.0)
        sampleData = {}
        for k, v in result['cost'].items():
            sampleData[int(k)] = v / int(k) * currFactor
        currencySymbol = allcurrencies.get(self.currency, "€")
        viewer = PricingGraphViewer(
            {"Pretore" : sampleData},
            parentWindow=self.view.mainapp.win,
            currencySymbol=currencySymbol
        )
        viewer.show()

    def showCreateResults(self, result):
        self.updatequote(result)
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
        print(f"{headers=}, {endpoint=}, {data=}")
        try:
            req = urllib.request.Request(endpoint, data=data, headers=headers)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    result = json.loads(response.read().decode("utf-8"))
                else:
                    print (f"Response code: {response.getcode()}")
        except urllib.error.HTTPError as e:
            print(f"Error: {e}\nHeaders: {e.headers}\nBody: {e.read().decode('utf-8')}")
        curr = None
        if self.exchange_thread is not None and self.exchange_thread.is_alive():
            self.exchange_thread.join(10)       # wait another 10s for the exchange info
            if self.exchange_thread.is_alive():
                curr = "EUR"
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
        self.do_quote("create", cb=self.showCreateResults, amt=150)

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
        if curr in self.rates:
            self.currency = curr
            self.updatequote(None)

    def show_multi_quote_comparison(self, btn, *a):
        btn.set_sensitive(False)
        quantities = [50,100,250,500,1000]
        self.do_quote("calculate", cb=self.updateMultiQuote, quantities=quantities)
        btn.set_sensitive(True)
