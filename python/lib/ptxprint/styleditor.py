
from gi.repository import Gtk

stylemap = {
    'TextType':     ('fcb_styTextType', None),
    'StyleType':    ('fcb_styStyleType', None),
    'FontName':     ('bl_font_styFontName', None),
    'Color':        ('col_styColor', None),
    'FontSize':     ('s_styLineSpacing1', None),
    'Bold':         ('c_styFaceBold', lambda v: "" if v else "-"),
    'Italic':       ('c_styFaceItalic', lambda v: "" if v else "-"),
    'SmallCap':     ('c_stySmallCap', lambda v: "" if v else "-"),
    'Superscript':  ('c_styFaceSuperscript', lambda v: "" if v else "-"),
    'Raise':        ('s_styRaise', None),
    'Justification': ('fcb_styJustification', None),
    'FirstLineIndent': ('s_styFirstLineIndent', None),
    'LeftMargin':   ('s_styLeftMargin', None),
    'RightMargin':  ('s_styRightMargin', None),
    'LineSpacing':  ('s_styLineSpacing', None),
    'SpaceBefore':  ('s_stySpaceBefore', None),
    'SpaceAfter':   ('s_stySpaceAfter', None),
    'CallerStyle':  ('fcb_styCallerStyle', None),
    'NoteCallerStyle': ('fcb_styCallerStyle1', None),
    'NoteBlendInto': ('fcb_styCallerStyle2', None),
    'CallerRaise':  ('s_styCallerRaise', None),
    'NoteCallerRaise': ('s_styCallerRaise1', None),
    '_fontsize':    ('c_styAbsoluteFontSize', lambda v: "FontScale" if v else "FontSize"),
    '_linespacing': ('c_styAbsoluteLineSpacing', lambda v: "BaseLine" if v else 'LineSpacing')
}

def triefit(k, base, start):
    for i in range(start, len(k)):
        if k[:i] in base:
            triefit(k, base[k[:i]], i+1)
            break
    else:
        base[k] = {}

class StyleEditor:
    def __init__(self, builder):
        self.builder = builder
        self.treestore = builder.get_object("ts_styles")
        self.treeview = self.builder.get_object("tv_Styles")
        self.treeview.set_model(self.treestore)
        cr = Gtk.CellRendererText()
        tvc = Gtk.TreeViewColumn("Marker", cr, text=0)
        self.treeview.append_column(tvc)
        self.sheet = None

    def load(self, sheet):
        self.sheet = sheet
        hierarchy = {"th": {"thc": {}, "thr": {}}, "tc": {"tcc": {}, "tcr": {}}, "zpa-": {}}
        results = {}
        for k in sorted(sheet.keys(), key=lambda x:(len(x), x)):
            triefit(k, hierarchy, 1)
        for k, v in sorted(hierarchy.items(), key=lambda x:(len(x[0]), x[0])):
            if k not in sheet:
                tt = sheet[list(v.keys())[-1]]['TextType']
            else:
                tt = sheet[k]['TextType']
            results.setdefault(tt, {})[k] = v
        self.treestore.clear()
        self._fill_store(results, None)

    def _fill_store(self, d, parent):
        for k, v in sorted(d.items(), key=lambda x:(len(x), x)):
            if k in self.sheet:
                n = self.sheet[k].get('name', None)
            else:
                n = None
            s = ["{} - {}".format(k, n), True] if n is not None else [k, False]
            this = self.treestore.append(parent, s)
            if len(v):
                self._fill_store(v, this)

