#!/usr/bin/python3

import sys, os, re
from gi.repository import Gtk

class PtxPrinter:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(os.path.dirname(__file__), "ptxprint.glade"))
        self.builder.connect_signals(self)
        self.addCR("cb_digits", 0)
        self.addCR("cb_columns", 0)
        self.mw = self.builder.get_object("ptxprint")

    def run(self, callback):
        self.callback = callback
        self.mw.show_all()
        Gtk.main()

    def addCR(self, name, index):
        v = self.builder.get_object(name)
        setattr(self, name, v)
        c = Gtk.CellRendererText()
        v.pack_start(c, True)
        v.add_attribute(c, "text", index)

    def get(self, wid, sub=0):
        w = self.builder.get_object(wid)
        v = ""
        if wid.startswith("cb_"):
            model = w.get_model()
            i = w.get_active()
            if i < 0:
                e = w.get_child()
                if e is not None:
                    v = e.get_text()
            elif model is not None:
                v = model[i][sub]
        elif wid.startswith("t_"):
            v = w.get_text()
        elif wid.startswith("f_"):
            v = w.get_font_name()
            print(v)
            m = re.match(r"(^.*?),?\s*((?:\S+\s+)*)(\d+(?:\.\d+)?)$", v)
            if m:
                v = [m.group(1), m.group(2), m.group(3)]
            else:
                v = [v]
        return v

    def onDestroy(self, btn):
        Gtk.main_quit()

    def onOK(self, btn):
        print("Do something")
        self.callback(self)

    def onCancel(self, btn):
        print("Do nothing")
        self.onDestroy(btn)

class Info:
    _mappings = {
        "project/id": lambda w:w.get("cb_project"),
        "paper/width": lambda w:re.sub(r"^.*?, \s*(.+?)\s*(?:\(.*|$)", r"\1", w.get("cb_pagesize")) or "148mm",
        "paper/height": lambda w:re.sub(r"^(.*?)\s*,.*$", r"\1", w.get("cb_pagesize")) or "210mm",
        "paper/margins": lambda w:w.get("t_margins") or "14mm",
        "paper/columns": lambda w:w.get("cb_columns"),
        "paper/fontfactor": lambda w:float(w.get("f_body")[2]) / 12,
    }

    def __init__(self, printer, path):
        self.dict = {"/ptxpath": path}
        for k, v in self._mappings.items():
            self.dict[k] = v(printer)

    def asTex(self, template="template.tex"):
        res = []
        with open(os.path.join(os.path.dirname(__file__), template)) as inf:
            for l in inf.readlines():
                res.append(l.format(**self.dict))
        return "".join(res)

