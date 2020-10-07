
import re
from gi.repository import Gtk
from ptxprint.gtkutils import getWidgetVal, setWidgetVal

stylemap = {
    'Description':  ('l_styDescription', None, None),
    'TextType':     ('fcb_styTextType', 'Paragraph', None),
    'StyleType':    ('fcb_styStyleType', 'Paragraph', None),
    'FontName':     ('bl_font_styFontName', None, None),
    'Color':        ('col_styColor', 'x000000', None),
    'FontSize':     ('s_styFontSize', '12', None),
    'Bold':         ('c_styFaceBold', '-', lambda v: "" if v else "-"),
    'Italic':       ('c_styFaceItalic', '-', lambda v: "" if v else "-"),
    'SmallCap':     ('c_stySmallCap', '-', lambda v: "" if v else "-"),
    'Superscript':  ('c_styFaceSuperscript', '-', lambda v: "" if v else "-"),
    'Raise':        ('s_styRaise', '0', None),
    'Justification': ('fcb_styJustification', 'justified', None),
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

topLevelOrder = ('File', 'Introduction', 'Chapters & Verses', 'Paragraphs', 'Poetry',
    'Titles & Headings', 'Tables', 'Lists', 'Footnotes', 'Cross References',
    'Special Text', 'Character Styling', 'Breaks', 'Peripheral Materials',
    'Peripheral References', 'Other', 'Obsolete & Deprecated')
catorder = {k: i for i, k in enumerate(topLevelOrder)}

    # '*Introduction':               'Introduction',
    # '*Poetry':                     'Poetry',
    # '*Special Text':               'Special Text',
    # '*Other':                      'Other',
    # '*File':                       '*DROP from list*'
    # '*Publication':                '*DROP from list*'
categorymapping = {
    'Chapter':                     'Chapters & Verses',
    'Chapter Number':              'Chapters & Verses',
    'Verse Number':                'Chapters & Verses',
    'Paragraph':                   'Paragraphs',
    'Poetry Text':                 'Poetry',
    'Label':                       'Titles & Headings',
    'Title':                       'Titles & Headings',
    'Heading':                     'Titles & Headings',
    'Table':                       'Tables',
    'Embedded List Entry':         'Lists',
    'Embedded List Item':          'Lists',
    'List Entry':                  'Lists',
    'List Footer':                 'Lists',
    'List Header':                 'Lists',
    'Structured List Entry':       'Lists',
    'Footnote':                    'Footnotes',
    'Footnote Paragraph Mark':     'Footnotes',
    'Endnote':                     'Footnotes',
    'Cross Reference':             'Cross References',
    'Character':                   'Character Styling',
    'Link text':                   'Character Styling',
    'Break':                       'Breaks',
    'Peripheral Ref':              'Peripheral References',
    'Periph':                      'Peripheral Materials',
    'Peripherals':                 'Peripheral Materials',
    'Auxiliary':                   'Peripheral Materials',
    'Concordance and Names Index': 'Peripheral Materials',
    'OBSOLETE':                    'Obsolete & Deprecated',
    'DEPRECATED':                  'Obsolete & Deprecated',
}

stylediverts = {
    'LineSpacing': '_linespacing',
    'FontSize': '_fontsize'
}

widgetsignals = {
    's': "value-changed",
    'c': "toggled",
    "bl": "clicked",
    "col": "color-set"
}

def triefit(k, base, start):
    for i in range(start, len(k)):
        if k[:i] in base:
            triefit(k, base[k[:i]], i+1)
            break
    else:
        base[k] = {}

def coltotex(s):
    vals = s[s.find("(")+1:-1].split(",")
    return "x"+"".join("{:02X}".format(x) for x in vals[:3])

def textocol(s):
    if s.startswith("x"):
        vals = [int(x, 16) for x in s[1::2]]
    else:
        v = int(s)
        vals = []
        while v:
            vals.append(v % 256)
            v //= 256
        vals.extend([0] * (3 - len(vals)))
    return "rgb({0},{1},{2})".format(*vals)

name_reg = re.compile(r"^(OBSOLETE|DEPRECATED)?\s*(.*?)\s+-\s+([^-]*?)\s*(?:-\s*(.*?)\s*)?$")

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
        for k, v in stylemap.items():
            if v[0].startswith("l_"):
                continue
            w = self.builder.get_object(v[0])
            key = stylediverts.get(k, k)
            (pref, name) = v[0].split("_", 1)
            signal = widgetsignals.get(pref, "changed")
            w.connect(signal, self.item_changed, key)
        self.isLoading = False

    def load(self, sheet):
        self.sheet = sheet
        results = {"Tables": {"th": {"thc": {}, "thr": {}}, "tc": {"tcc": {}, "tcr": {}}},
                   "Peripheral Materials": {"zpa-": {}},
                   "File": {"toc": {}}}
        for k, v in sorted(sheet.items(), key=lambda x:(len(x[0]), x[0])):
            cat = 'Other'
            if 'Name' in v:
                m = name_reg.match(v['Name'])
                if m:
                    cat = m.group(1) or m.group(3)
                    cat = categorymapping.get(cat, cat)
            triefit(k, results.setdefault(cat, {}), 1)
        self.treestore.clear()
        self._fill_store(results, None)

    def _fill_store(self, d, parent):
        if parent is None:
            keyfn = lambda x:(catorder.get(x[0], len(catorder)), x[0])
        else:
            keyfn = lambda x:(len(x[0]), x[0])
        for k, v in sorted(d.items(), key=keyfn):
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
        self.isLoading = True
        data = self.sheet.get(self.marker, {})
        for k, v in stylemap.items():
            if k.startswith("_"):
                val = v[1]
                for m, f in ((v[2](x), x) for x in (False, True)):
                    if m in data:
                        val = f
                        break
            else:
                val = data.get(k, v[1])
                if v[0].startswith("c_"):
                    val = val != v[1]
            w = self.builder.get_object(v[0])
            if w is None:
                print("Can't find widget {}".format(v[0]))
            else:
                if v[0].startswith("bl_"):
                    if val is None:
                        continue
                    val = (val, "")
                elif v[0].startswith("col_"):
                    val = textocol(val)
                setWidgetVal(v[0], w, val)
        self.isLoading = False

    def item_changed(self, w, key):
        if self.isLoading:
            return
        print(f"{w}, {key}")
        data = self.sheet[self.marker]
        v = stylemap[key]
        w = self.builder.get_object(v[0])  # since LineSpacing triggers the checkbutton
        val = getWidgetVal(v[0], w)
        if key.startswith("_"):
            val = v[2](val)
            isset = getWidgetVal(v[0], w)
            other = v[2](not isset)
            if other in data:
                del data[other]
            newv = stylemap[val]
            wtemp = self.builder.get_object(newv[0])
            value = getWidgetVal(newv[0], wtemp)
            key = val
        elif key.startswith("bl_"):
            value = val[0]
        elif v[2] is not None:
            value = v[2](val)
        else:
            value = val
        data[key] = value
            

            


