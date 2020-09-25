
from ptxprint.gtkutils import getWidgetVal, setWidgetVal
from ptxprint.view import refKey, newBase
from gi.repository import Gtk, GdkPixbuf
import configparser
import os, regex


_piclistfields = ["anchor", "caption", "src", "size", "scale", "pgpos", "ref", "alt", "copyright", "mirror"]
_form_structure = {
    'anchor':   't_plAnchor',
    'caption':  't_plCaption',
    'src':      't_plFilename',
    'size':     'fcb_plSize',
    'scale':    's_plScale',
    'pgpos':    'fcb_plPgPos',
    'ref':      't_plRef',
    'alt':      't_plAltText',
    'copyright':    't_plCopyright',
    'mirror':   'fcb_plMirror',
    'hpos':     'fcb_plHoriz',
    'nlines':   's_plLines',
}
_comblist = ['pgpos', 'hpos', 'nlines']

class PicList:
    def __init__(self, view, listview, builder, parent):
        self.view = view
        self.model = view.get_model()
        self.listview = listview
        self.builder = builder
        self.parent = parent
        self.selection = view.get_selection()
        for w in ("tv_picList", "tv_picListEdit", "tv_picListEdit1"):
            wid = self.builder.get_object(w)
            sel = wid.get_selection()
            sel.set_mode=Gtk.SelectionMode.SINGLE
            sel.connect("changed", self.row_select)
        for k, v in _form_structure.items():
            w = builder.get_object(v)
            w.connect("value-changed" if v[0].startswith("s_") else "changed", self.item_changed, k)
        pass

    def isEmpty(self):
        return len(self.model) == 0

    def clear(self):
        self.model.clear()

    def load(self, picinfo):
        self.view.set_model(None)
        self.listview.set_model(None)
        self.model.clear()
        if picinfo is not None:
            for k, v in sorted(picinfo.items(), key=lambda x:(refKey(x[0]), x[1])):
                row = [k] + [v[e] if e in v else (1 if e == "scale" else "") for e in _piclistfields[1:]]
                try:
                    row[4] = int(row[4]) * 100
                except (ValueError, TypeError):
                    row[4] = 100
                self.model.append(row)
        self.view.set_model(self.model)
        self.listview.set_model(self.model)

    def get(self, wid, default=None):
        wid = _form_structure.get(wid, wid)
        w = self.builder.get_object(wid)
        res = getWidgetVal(wid, w, default=default)
        if wid.startswith("s_"):
            res = int(res[:res.find(".")]) if res.find(".") >= 0 else int(res)
        return res

    def getrowinfo(self, row):
        e = {k: row[i+1] for i, k in enumerate(_piclistfields[1:])}
        e['scale'] = e['scale'] / 100. if e['scale'] != 100 else None
        return e

    def getinfo(self):
        res = {}
        for row in self.model:
            res[row[0]] = self.getrowinfo(row)
        return res

    def row_select(self, selection):
        if selection.count_selected_rows() != 1:
            return
        model, i = selection.get_selected()
        for w in (self.builder.get_object(x) for x in ("tv_picList", "tv_picListEdit", "tv_picListEdit1")):
            s = w.get_selection()
            if s != selection:
                s.select_iter(i)
                p = w.get_model().get_path(i)
                w.scroll_to_cell(p)
        if selection != self.selection:
            return
        if self.model.get_path(i).get_indices()[0] >= len(self.model):
            return
        row = self.model[i]
        for j, (k, v) in enumerate(_form_structure.items()): # relies on ordered dict
            if k == 'pgpos':
                val = row[j][0]
            elif k == 'hpos':
                val = row[5]
                val = val[1] if len(val) > 1 else ""
            elif k == 'nlines':
                val = row[5]
                val = int(val[2]) if len(val) > 2 else 0
            else:
                val = row[j]
            w = self.builder.get_object(v)
            setWidgetVal(v, w, val)

    def select_row(self, i):
        if i >= len(self.model):
            i = len(self.model) - 1
        treeiter = self.model.get_iter_from_string(str(i))
        self.selection.select_iter(treeiter)

    def get_pgpos(self):
        res = "".join(self.get(k, default="") for k in _comblist[:-1])
        if res.startswith("c"):
            res += str(self.get(_comblist[-1]))
        res = regex.sub(r'([PF])([tcb])([lcr])', r'\1\3\2', res).strip("c") 
        return res

    def item_changed(self, w, key):
        if key in _comblist:
            val = self.get_pgpos()
            key = "pgpos"
        else:
            val = self.get(key)
        if self.model is not None and len(self.model):
            row = self.model[self.selection.get_selected()[1]]
            row[_piclistfields.index(key)] = val
            if key == "src":
                tempinfo = {}
                e = self.getrowinfo(row)
                tempinfo[row[0]] = e
                self.parent.getFigureSources(tempinfo)
                pic = self.builder.get_object("img_picPreview")
                picc = self.builder.get_object("img_piccheckPreview")
                if 'src path' in e:
                    self.parent.updatePicChecks(val)       # only update checks if src exists
                    picframe = self.builder.get_object("fr_picPreview")
                    rect = picframe.get_allocation()
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(e['src path'], rect.width - 12, rect.height)
                    pic.set_from_pixbuf(pixbuf)
                    picc.set_from_pixbuf(pixbuf)
                else:
                    pic.clear()
                    picc.clear()

    def get_row_from_items(self):
        row = [self.get(k, default="") for k in _piclistfields]
        row[_piclistfields.index('pgpos')] = self.get_pgpos()
        return row

    def add_row(self):
        if len(self.model) > 0:
            row = self.model[self.selection.get_selected()[1]][:]
            row[0] = ""
        else:
            row = self.get_row_from_items()
        self.model.append(row)
        self.select_row(len(self.model)-1)

    def del_row(self):
        model, i = self.selection.get_selected()
        del self.model[i]
        self.select_row(model.get_path(i).get_indices()[0])

_checks = {
    "r_picclear":       "unknown",
    "fcb_picaccept":    "Unknown",
    "r_picreverse":     "unknown",
    "fcb_pubusage":     "Unknown",
    "r_pubclear":       "unchecked",
    "r_pubnoise":       "unchecked",
    "fcb_pubaccept":    "Unknown"
}

class PicChecks:

    fname = "picChecks.txt"

    def __init__(self, parent):
        self.cfgShared = configparser.ConfigParser()
        self.cfgProject = configparser.ConfigParser()
        self.parent = parent
        self.src = None

    def _init_default(self, cfg, prefix):
        if not cfg.has_section('DEFAULT'):
            for k, v in _checks.items():
                t, n = k.split("_")
                if n.startswith(prefix):
                    cfg['DEFAULT'][n] = v

    def init(self, basepath, configid):
        if basepath is None or configid is None:
            return
        self.cfgShared.read(os.path.join(basepath, self.fname), encoding="utf-8")
        self._init_default(self.cfgShared, "pic")
        self.cfgProject.read(os.path.join(basepath, configid, self.fname), encoding="utf-8")
        self._init_default(self.cfgProject, "pub")

    def writeCfg(self, basepath, configid):
        if not len(self.cfgShared) or configid is None:
            return
        self.savepic()
        with open(os.path.join(basepath, "shared", "ptxprint", self.fname), "w", encoding="utf-8") as outf:
            self.cfgShared.write(outf)
        with open(os.path.join(basepath, "shared", "ptxprint", configid, self.fname), "w", encoding="utf-8") as outf:
            self.cfgProject.write(outf)

    def loadpic(self, src):
        if self.src == newBase(src):
            return
        self.src = newBase(src)
        for k, v in _checks.items():
            t, n = k.split("_")
            cfg = self.cfgShared if n.startswith("pic") else self.cfgProject
            val = cfg.get(self.src, n, fallback=v)
            self.parent.set(k, val)

    def savepic(self):
        if self.src is None:
            return
        for k, v in _checks.items():
            val = self.parent.get(k)
            t, n = k.split("_")
            cfg = self.cfgShared if n.startswith("pic") else self.cfgProject
            try:
                cfg.set(self.src, n, val)
            except configparser.NoSectionError:
                cfg.add_section(self.src)
                cfg.set(self.src, n, val)
