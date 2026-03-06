
import os, json, threading #, requests
from shutil import copy
from gi.repository import Gtk, GLib, Gdk
from ptxprint.utils import _, appdirs
from zipfile import ZipFile, ZIP_DEFLATED

querymap = {
    "settings/quantity": lambda s:[s.get("s_prnl_copies")],
    "settings/description": "t_prnl_description",
    "settings/height": lambda s:s.height(),
    "settings/width": lambda s:s.width(),
    "data/11-211-widget-1": "t_prnl_bookID",
    "data/8-203-widget-0": "t_prnl_description",
    "data/1-189-widget-4": "l_prnl_pages",
    "data/1-189-widget-5": "fcb_prnl_paperType",
    "data/6-200-widget-3": "fcb_prnl_coverLamination",
    "data/31-194-widget-4": "s_prnl_ribbons",
    "data/23-135-widget-5": "fcb_prnl_wrap"
}

querytypes = {
    "306": list(querymap.keys()),
    "307": [k for k in querymap.keys() if k != "data/31-194-widget-4"]
}

def labelWidget(txxt, widget, grid, x, y):
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

    def get(self, wname, **kw):
        return self.view.get(wname, **kw)

    def set(self, wname, val, **kw):
        return self.view.set(wname, val, **kw)

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
        (height, width) = self.view.calcPageSize()
        return height

    def width(self):
        (height, width) = self.view.calcPageSize()
        return width

    def numpages(self):
        return self.view.getPageCount()

    def select_account(self, btn, *a):
        self.setup()
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

    def prepare_quote(self):
        booktype = self.get("fcb_prnl_binding", default="307")
        qinfo = {}
        for k in querytypes[booktype]:
            v = querymap[k]
            if isinstance(v, str):
                val = self.get(v)
            else:
                val = v(self)
            if val is None:
                continue
            b = k.split("/")
            c = qinfo
            for bk in b[:-1]:
                c = qinfo.setdefault(bk, {})
            c[b[-1]] = val
        return booktype, qinfo

    def submit_quote(self, qinfo, endpoint, cb=None, amt=100):
        if cb is None:
            cb = self.updatequote
        thread = threading.Thread(target=self.url_query, args=(cb, endpoint, amt, qinfo))
        thread.daemon = True
        thread.start()

    def updatequote(self, result):
        amount = result['data']['summary']['amount']
        copies = int(self.get("s_prnl_copies"))
        self.set('l_prnl_total', "\u20AC{:.2f}".format(amount))
        self.set('l_prnl_percopy', "\u20AC{:.2f}".format(amount/copies))

    def showCreateResults(self, result):
        self.updatequote(result)
        quoteid = result.get("number", _("Unknown"))
        self.set("l_prnl_orderRef", quoteid)
        self.set("l_prnl_zipFilename", os.path.basename(self.zipname))

    def url_query(self, callback, endpoint, amt, *a):
        message(endpoint+"\n"+"\n".join(str(x) for x in a))
        result = {"data": {"summary": {"amount": amt}}}
        GLib.idle_add(callback, result)

    def do_quote(self, command, cb=None, amt=100):
        if cb is None:
            cb = self.updatequote
        booktype, qinfo = self.prepare_quote()
        uuid = self.accounts[self.user]['UUID']
        endpoint = f"https://prxprint-pretore.com/wp-json/emily/v1/calculation/{uuid}/{booktype}/{command}"
        self.submit_quote(qinfo, endpoint, cb=cb, amt=amt)

    def quote(self, btn, *a):
        self.setup()
        self.do_quote("quote")

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
        print(zname)
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(zname, -1)
        clipboard.store()
        
