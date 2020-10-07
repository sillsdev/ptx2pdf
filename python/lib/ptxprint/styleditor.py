
from gi.repository import Gtk
from ptxprint.gtkutils import getWidgetVal, setWidgetVal

stylemap = {
    'Description':  ('l_description', None, None),
    'TextType':     ('fcb_styTextType', 'Paragraph', None),
    'StyleType':    ('fcb_styStyleType', 'Paragraph', None),
    'FontName':     ('bl_font_styFontName', None, None),
    'Color':        ('col_styColor', 'x000000', None),
    'FontSize':     ('s_styLineSpacing1', '12', None),
    'Bold':         ('c_styFaceBold', '-', lambda v: "" if v else "-"),
    'Italic':       ('c_styFaceItalic', '-', lambda v: "" if v else "-"),
    'SmallCap':     ('c_stySmallCap', '-', lambda v: "" if v else "-"),
    'Superscript':  ('c_styFaceSuperscript', '-', lambda v: "" if v else "-"),
    'Raise':        ('s_styRaise', '0', None),
    'Justification': ('fcb_styJustification', 'full', None),
    'FirstLineIndent': ('s_styFirstLineIndent', '0', None),
    'LeftMargin':   ('s_styLeftMargin', '0', None),
    'RightMargin':  ('s_styRightMargin', '0', None),
    'LineSpacing':  ('s_styLineSpacing', '0', None),
    'SpaceBefore':  ('s_stySpaceBefore', '0', None),
    'SpaceAfter':   ('s_stySpaceAfter', '0', None),
    'CallerStyle':  ('fcb_styCallerStyle', '', None),
    'NoteCallerStyle': ('fcb_styNoteCallerStyle', '', None),
    'NoteBlendInto': ('fcb_NoteBlendInto', '', None),
    'CallerRaise':  ('s_styCallerRaise', '0', None),
    'NoteCallerRaise': ('s_styNoteCallerRaise', '0', None),
    '_fontsize':    ('c_styFontScale', False, lambda v: "FontScale" if v else "FontSize"),
    '_linespacing': ('c_styAbsoluteLineSpacing', False, lambda v: "BaseLine" if v else 'LineSpacing')
}

topLevelList = (
    'Introduction',
    'Chapters & Verses',
    'Paragraphs',
    'Poetry',
    'Titles & Headings',
    'Tables',
    'Lists',
    'Footnotes',
    'Cross References',
    'Special Text',
    'Character Styling',
    'Breaks',
    'Peripheral Materials',
    'Peripheral References',
    'Other'
)

categorymapping = {
    'Chapter': 'Chapters & Verses',
    'Chapter Number': 'Chapters & Verses',
    'Verse Number': 'Chapters & Verses',
    'Paragraph': 'Paragraphs',
    'Poetry Text': 'Poetry',
    'Title': 'Titles & Headings',
    'Heading': 'Titles & Headings',
    'Table': 'Tables',
    'List Entry': 'Lists',
    'Footnote': 'Footnotes',
    'Cross Reference': 'Cross References',
    'Character': 'Character Styling',
    'Break': 'Breaks',
    'Concordance and Names Index': 'Peripheral Materials',
    'Peripheral Ref': 'Peripheral References',
    'Periph': 'Peripheral Materials',
    'Peripherals': 'Peripheral Materials',
    'Auxiliary': 'Peripheral Materials'
}
    # '*Introduction': 'Introduction',
    # '*Poetry': 'Poetry',
    # '*Special Text': 'Special Text',
    # '*Other': 'Other',

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
        tvc = Gtk.TreeViewColumn("Marker", cr, text=1)
        self.treeview.append_column(tvc)
        tself = self.treeview.get_selection()
        tself.connect("changed", self.onSelected)
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
                n = self.sheet[k].get('name', k)
            else:
                n = k
            s = [k, n, n != k]
            this = self.treestore.append(parent, s)
            if len(v):
                self._fill_store(v, this)

    def onSelected(self, selection):
        if selection.count_selected_rows() != 1:
            return
        model, i = selection.get_selected()
        if not model[i][2]:
            return
        self.marker = model[i][0]
        self.editMarker()

    def editMarker(self):
        data = self.sheet.get(self.marker, {})
        for k, v in stylemap.items():
            if v[0].startswith("bl_"):
                continue
            if k.startswith("_"):
                val = v[1]
                for m, f in ((v[2](x), x) for x in (False, True)):
                    if m in data:
                        val = f
                        break
            else:
                val = data.get(k, v[1])
            w = self.builder.get_object(v[0])
            if w is None:
                print("Can't find widget {}".format(v[0]))
            else:
                setWidgetVal(v[0], w, val)

    def item_changed(self, w, key):
        v = stylemap[key]
        val = v[2](getWidgetVal(v[0], w))
        if key.startswith("_"):
            k = v[2](False)

            


