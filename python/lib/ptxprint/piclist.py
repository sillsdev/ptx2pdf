
from ptxprint.gtkutils import getWidgetVal, setWidgetVal
from ptxprint.view import refKey
from gi.repository import Gtk

_piclistfields = ["anchor", "caption", "src", "size", "scale", "pgpos", "alt", "ref", "copyright", "mirror"]
_form_structure = {
    'anchor':   't_plAnchor',
    'caption':  't_plCaption',
    'src':      't_plFilename',
    'size':     'fcb_plSize',
    'scale':    's_plScale',
    'pgpos':    'fcb_plPgPos',
    'alt':      't_plAltText',
    'ref':      't_plRef',
    'copyright':    't_plCopyright',
    'mirror':   'fcb_plMirror',
    'hpos':     'fcb_plHoriz',
    'nlines':   's_plLines',
}
_comblist = ['pgpos', 'hpos', 'nlines']

class PicList:
    def __init__(self, view, listview,builder):
        self.view = view
        self.model = view.get_model()
        self.listview = listview
        self.builder = builder
        self.selection = view.get_selection()
        self.selection.set_mode=Gtk.SelectionMode.SINGLE
        self.selection.connect("changed", self.row_select)
        for k, v in _form_structure.items():
            w = builder.get_object(v)
            w.connect("value-changed" if v[0].startswith("s_") else "changed", self.item_changed, k)
        pass

    def isEmpty(self):
        return len(self.model) == 0

    def clear(self):
        self.model.clear()

    def load(self, picinfo):
        if picinfo is None:
            return
        self.view.set_model(None)
        self.listview.set_model(None)
        self.model.clear()
        for k, v in sorted(picinfo.items(), key=lambda x:(refKey(x[0]), x[1])):
            row = [k] + [v[e] if e in v else (1 if e == "scale" else "") for e in _piclistfields[1:]]
            try:
                row[4] = int(row[4]) * 100
            except ValueError, TypeError:
                row[4] = 100
            self.model.append(row)
        self.view.set_model(self.model)
        self.listview.set_model(self.model)

    def get(self, wid, default=None):
        wid = _form_structure.get(wid, wid)
        w = self.builder.get_object(wid)
        res = getWidgetVal(wid, w, default=default)
        if wid.startswith("s_") and res.find(".") >= 0:
            res = res[:res.find(".")]
        return res

    def getinfo(self):
        res = {}
        for row in self.model:
            e = {k: row[i+1] for i, k in enumerate(_piclistfields[1:])}
            e['scale'] = e['scale'] / 100. if e['scale'] != 100 else None
            res[row[0]] = e
        return res

    def row_select(self, selection):
        if selection.count_selected_rows() != 1:
            return
        model, i = selection.get_selected()
        row = self.model[i]
        for i, (k, v) in enumerate(_form_structure.items()): # relies on ordered dict
            if k == 'pgpos':
                val = row[i][0]
            elif k == 'hpos':
                val = row[5]
                val = val[1] if len(val) > 1 else ""
            elif k == 'nlines':
                val = row[5]
                val = int(val[2]) if len(val) > 2 else 0
            else:
                val = row[i]
            w = self.builder.get_object(v)
            setWidgetVal(v, w, val)

    def item_changed(self, w, key):
        if key in _comblist:
            val = "".join(self.get(k, default="") for k in _comblist)
            key = "pgpos"
        else:
            val = self.get(key)
        self.model[self.selection.get_selected()[1]][_piclistfields.index(key)] = val

        
