#!/usr/bin/python3

import sys, os, re, regex, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import xml.etree.ElementTree as et
from ptxprint.font import TTFont

_bookslist = """GEN|50 EXO|40 LEV|27 NUM|36 DEU|34 JOS|24 JDG|21 RUT|4 1SA|31 2SA|24 1KI|22 2KI|25 1CH|29 2CH|36 EZR|10 NEH|13
        EST|10 JOB|42 PSA|150 PRO|31 ECC|12 SNG|8 ISA|66 JER|52 LAM|5 EZK|48 DAN|12 HOS|14 JOL|3 AMO|9 OBA|1 JON|4 MIC|7 NAM|3
        HAB|3 ZEP|3 HAG|2 ZEC|14 MAL|4 ZZZ|0
        MAT|28 MRK|16 LUK|24 JHN|21 ACT|28 ROM|16 1CO|16 2CO|13 GAL|6 EPH|6 PHP|4 COL|4 1TH|5 2TH|3 1TI|6 2TI|4 TIT|3 PHM|1
        HEB|13 JAS|5 1PE|5 2PE|3 1JN|5 2JN|1 3JN|1 JUD|1 REV|22
        TOB|0 JDT|0 ESG|0 WIS|0 DIR|0 BAR|0 LJE|0 S3Y|0 SUS|0 BEL|0 1MA|0 2MA|0 3MA|0 4MA|0 1ES|0 2ES|0 MAN|0 PS2|0
        ODA|0 PSS|0"""
allbooks = [b.split("|")[0] for b in _bookslist.split() if b != "ZZZ|0"]
books = dict((b.split("|")[0], i+1) for i, b in enumerate(_bookslist.split()))
chaps = dict(b.split("|") for b in _bookslist.split())


class ParatextSettings:
    def __init__(self, basedir, prjid):
        self.dict = {}
        doc = et.parse(os.path.join(basedir, prjid, "Settings.xml"))
        for c in doc.getroot():
            self.dict[c.tag] = c.text

    def __getitem__(self, key):
        return self.dict[key]


class PtxPrinterDialog:
    def __init__(self, allprojects, settings_dir):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(os.path.dirname(__file__), "ptxprint.glade"))
        self.builder.connect_signals(self)
        self.addCR("cb_digits", 0)
        self.addCR("cb_columns", 0)
        self.mw = self.builder.get_object("ptxprint")
        self.projects = self.builder.get_object("ls_projects")
        self.settings_dir = settings_dir
        self.ptsettings = None
        for p in allprojects:
            self.projects.append([p])

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
            w.emit("font-set")
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
            w.set_font_name(fname)

    def onProjectChange(self, cb_prj):
        self.prjid = self.get("cb_project")
        self.ptsettings = None
        lsbooks = self.builder.get_object("ls_books")
        lsbooks.clear()
        if not self.prjid:
            return
        self.ptsettings = ParatextSettings(self.settings_dir, self.prjid)
        bp = self.ptsettings['BooksPresent']
        for i, b in enumerate(allbooks):
            if i < len(bp) and bp[i] == "1":
                lsbooks.append([b])
        cb_bk = self.builder.get_object("cb_book")
        cb_bk.set_active(0)
        font_name = self.ptsettings['DefaultFont'] + ", " + self.ptsettings['DefaultFontSize']
        self.set('f_body', font_name)

class Info:
    _mappings = {
        "project/id": lambda w:w.get("cb_project"),
        "paper/height": lambda w:re.sub(r"^.*?, \s*(.+?)\s*(?:\(.*|$)", r"\1", w.get("cb_pagesize")) or "210mm",
        "paper/width": lambda w:re.sub(r"^(.*?)\s*,.*$", r"\1", w.get("cb_pagesize")) or "148mm",
        "paper/margins": lambda w:w.get("t_margins") or "14mm",
        "paper/columns": lambda w:w.get("cb_columns"),
        "paper/fontfactor": lambda w:float(w.get("f_body")[2]) / 12,
        "paragraph/linespacing": lambda w:w.get("t_linespacing"),
        "document/iffigures": lambda w:"true" if w.get("c_figs") else "false",
        "document/ifjustify": lambda w:"true" if w.get("c_justify") else "false"
    }
    _fonts = {
        "font/regular": "f_body",
        "font/bold": "f_bold",
        "font/italic": "f_italic",
        "font/bolditalic": "f_bolditalic"
    }

    def __init__(self, printer, path, ptsettings=None):
        self.dict = {"/ptxpath": path}
        for k, v in self._mappings.items():
            self.dict[k] = v(printer)
        self.processFonts(printer)
        self.ptsettings = ptsettings
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

