#!/usr/bin/python3

import sys, os, re, regex
from gi.repository import Gtk
import xml.etree.ElementTree as et
from ptxprint.font import TTFont

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

    def parse_fontname(self, font):
        m = re.match(r"^(.*?),?\s*((?:[^,\s]+\s+)*)(\d+(?:\.\d+)?)$", font)
        if m:
            styles = m.group(2).strip().split()
            if not m.group(1):
                return [styles[0], styles[1:], m.group(3)]
            else:
                return [m.group(1), styles, m.group(3)]
        else:
            return [font, [], 0]

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
            v = self.parse_fontname(w.get_font_name())
        elif wid.startswith("c_"):
            v = w.get_active()
        return v

    def set(self, wid, value):
        w = self.builder.get_object(wid)
        if wid.startswith("cb_"):
            model = w.get_model()
            e = w.get_child()
            if e is not None and isinstance(e, Gtk.Entry):
                e.set_text(value)
            else:
                w.set_active_id(value)
        elif wid.startswith("t_"):
            w.set_text(value)
        elif wid.startswith("f_"):
            w.set_font_name(value)
        elif wid.startswith("c_"):
            w.set_active(value)

    def getBooks(self):
        if self.get('c_onebook'):
            return [self.get('cb_onebook')]
        else:
            return self.get('t_booklist').split()

    def onDestroy(self, btn):
        Gtk.main_quit()

    def onOK(self, btn):
        print("Do something")
        self.callback(self)

    def onCancel(self, btn):
        print("Do nothing")
        self.onDestroy(btn)

    def onFontChange(self, fbtn):
        font = fbtn.get_font_name()
        (family, style, size) = self.parse_fontname(font)
        style = [s.lower() for s in style if s not in ("Regular", "Medium")]
        label = self.builder.get_object("l_font")
        label.set_text(font)
        for s in ('bold', 'italic', 'bold italic'):
            w = self.builder.get_object("f_"+s.replace(" ", ""))
            fname = family + ", " + " ".join(style + s.split()) + " "+ str(size)
            print("|".join([s, font, fname]))
            w.set_font_name(fname)


_bookslist = """GEN EXO LEV NUM DEU JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR NEH
        EST JOB PSA PRO ECC SNG ISA JER LAM EZK DAN HOS JOL AMO OBA JON MIC NAM
        HAB ZEP HAG ZEC MAL ZZZ
        MAT MRK LUK JHN ACT ROM 1CO 2CO GAL EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM
        HEB JAS 1PE 2PE 1JN 2JN 3JN JUD REV
        TOB JDT ESG WIS DIR BAR LJE S3Y SUS BEL 1MA 2MA 3MA 4MA 1ES 2ES MAN PS2
        ODA PSS"""
books = dict((b, i+1) for i, b in enumerate(_bookslist.split()))

class ParatextSettings:
    def __init__(self, prjdir):
        self.dict = {}
        doc = et.parse(os.path.join(prjdir, "Settings.xml"))
        for c in doc.getroot():
            self.dict[c.tag] = c.text

    def __getitem__(self, key):
        return self.dict[key]


class Info:
    _mappings = {
        "project/id": lambda w:w.get("cb_project"),
        "paper/height": lambda w:re.sub(r"^.*?, \s*(.+?)\s*(?:\(.*|$)", r"\1", w.get("cb_pagesize")) or "210mm",
        "paper/width": lambda w:re.sub(r"^(.*?)\s*,.*$", r"\1", w.get("cb_pagesize")) or "148mm",
        "paper/margins": lambda w:w.get("t_margins") or "14mm",
        "paper/columns": lambda w:w.get("cb_columns"),
        "paper/fontfactor": lambda w:float(w.get("f_body")[2]) / 12,
        "paragraph/linespacing": lambda w:w.get("t_linespacing")
    }
    _fonts = {
        "font/regular": "f_body",
        "font/bold": "f_bold",
        "font/italic": "f_italic",
        "font/bolditalic": "f_bolditalic"
    }

    def __init__(self, printer, path):
        self.dict = {"/ptxpath": path}
        for k, v in self._mappings.items():
            self.dict[k] = v(printer)
        self.processFonts(printer)
        self.ptsettings = None
        self.changes = None

    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def processFonts(self, printer):
        for p, wid in self._fonts.items():
            (family, style, size) = printer.get(wid)
            f = TTFont(family, " ".join(style))
            if 'Silf' in f:
                engine = "/GR"
            else:
                engine = ""
            s = ""
            if len(style):
                s = "/" + "".join(x[0].upper() for x in style)
            self.dict[p] = family + engine + s            

    def asTex(self, template="template.tex"):
        res = []
        with open(os.path.join(os.path.dirname(__file__), template)) as inf:
            for l in inf.readlines():
                if l.startswith(r"\ptxfile"):
                    for f in self.dict['project/books']:
                        res.append("\\ptxfile{{{}}}\n".format(os.path.abspath(f)))
                else:
                    res.append(l.format(**self.dict))
        return "".join(res)

    def convertBook(self, bk, outdir, prjdir):
        if self.ptsettings is None:
            self.ptsettings = ParatextSettings(prjdir)
        if self.changes is None:
            self.changes = self.readChanges(os.path.join(prjdir, 'PrintDraftChanges.txt'))
        fbkfm = self.ptsettings['FileNameBookNameForm']
        bknamefmt = fbkfm.replace("MAT","{bkid}").replace("41","{bknum:02d}") + \
                    self.ptsettings['FileNamePostPart']
        fname = bknamefmt.format(bkid=bk, bknum=books.get(bk, 0))
        infname = os.path.join(prjdir, fname)
        if self.changes is not None:
            outfname = os.path.join(outdir, fname)
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:]
            with open(infname, "r") as inf:
                dat = inf.read()
                for c in self.changes:
                    dat = c[0].sub(c[1], dat)
            with open(outfname, "w") as outf:
                outf.write(dat)
            return outfname
        else:
            return infname

    def readChanges(self, fname):
        changes = []
        with open(fname, "r") as inf:
            for l in inf.readlines():
                l = l.strip().replace(u"\uFEFF", "")
                l = re.sub(r"\s*#.*$", "", l)
                if not len(l):
                    continue
                m = re.match(r"^(['\"])(.*?)(?<!\\)\1\s*>\s*(['\"])(.*?)(?<!\\)\3", l)
                if m:
                    changes.append((regex.compile(m.group(2), flags=regex.M), m.group(4)))
        if not len(changes):
            return None
        return changes

