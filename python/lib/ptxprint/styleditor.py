
import re
from gi.repository import Gtk, Pango
from ptxprint.gtkutils import getWidgetVal, setWidgetVal
from ptxprint.usfmutils import Sheets

stylemap = {
    'Marker':       ('l_styleTag',          None,               None, None),
    'Description':  ('l_styDescription',    None,               None, None),
    'TextType':     ('fcb_styTextType',     'l_styTextType',    'Paragraph', None),
    'StyleType':    ('fcb_styStyleType',    'l_styStyleType',   'Paragraph', None),
    'FontName':     ('bl_font_styFontName', 'l_styFontName',    None, None),
    'Color':        ('col_styColor',        'l_styColor',       'x000000', None),
    'FontSize':     ('s_styFontSize',       'l_styFontSize',    '12', None),
    'Bold':         ('c_styFaceBold',       'c_styFaceBold',    '-', lambda v: "" if v else "-"),
    'Italic':       ('c_styFaceItalic',     'c_styFaceItalic',  '-', lambda v: "" if v else "-"),
    'SmallCap':     ('c_stySmallCap',       'c_stySmallCap',    '-', lambda v: "" if v else "-"),
    'Superscript':  ('c_styFaceSuperscript', 'c_styFaceSuperscript', '-', lambda v: "" if v else "-"),
    'Raise':        ('s_styRaise',          'l_styRaise',       '0', None),
    'Justification': ('fcb_styJustification', 'l_styJustification', 'Justified', lambda v: "" if v == "Justified" else v),
    'FirstLineIndent': ('s_styFirstLineIndent', 'l_styFirstLineIndent', '0', None),
    'LeftMargin':   ('s_styLeftMargin',     'l_styLeftMargin',  '0', None),
    'RightMargin':  ('s_styRightMargin',    'l_styRightMargin', '0', None),
    'LineSpacing':  ('s_styLineSpacing',    'l_styLineSpacing', '0', None),
    'SpaceBefore':  ('s_stySpaceBefore',    'l_stySpaceBefore', '0', None),
    'SpaceAfter':   ('s_stySpaceAfter',     'l_stySpaceAfter',  '0', None),
    'CallerStyle':  ('fcb_styCallerStyle',  'l_styCallerStyle', '', None),
    'NoteCallerStyle': ('fcb_styNoteCallerStyle', 'l_styNoteCallerStyle', '', None),
    'NoteBlendInto': ('fcb_NoteBlendInto',  'l_NoteBlendInto',  '', None),
    'CallerRaise':  ('s_styCallerRaise',    'l_styCallerRaise', '0', None),
    'NoteCallerRaise': ('s_styNoteCallerRaise', 'l_styNoteCallerRaise', '0', None),
    '_fontsize':    ('c_styFontScale',      'c_styFontScale',   False, lambda v: "FontScale" if v else "FontSize"),
    '_linespacing': ('c_styAbsoluteLineSpacing', 'c_styAbsoluteLineSpacing', False, lambda v: "BaseLine" if v else 'LineSpacing'),
    '_publishable': ('c_styTextProperties', 'c_styTextProperties', False, None)
}

topLevelOrder = ('Identification', 'Introduction', 'Chapters & Verses', 'Paragraphs', 'Poetry',
    'Titles & Headings', 'Tables', 'Lists', 'Footnotes', 'Cross References', 'Special Text', 
    'Character Styling', 'Breaks', 'Peripheral Materials', 'Peripheral References', 
    'Extended Study Content', 'Milestones', 'Other', 'Obsolete & Deprecated')
catorder = {k: i for i, k in enumerate(topLevelOrder)}

    # '*Publication':                '*DROP from list*'
categorymapping = {
    'File':                        ('Identification', 'identification'),
    'Identification':              ('Identification', 'identification'),
    'Introduction':                ('Introduction', 'introductions'),
    'Chapter':                     ('Chapters & Verses', 'chapters_verses'),
    'Chapter Number':              ('Chapters & Verses', 'chapters_verses'),
    'Verse Number':                ('Chapters & Verses', 'chapters_verses'),
    'Paragraph':                   ('Paragraphs', 'paragraphs'),
    'Poetry':                      ('Poetry', 'poetry'),
    'Poetry Text':                 ('Poetry', 'poetry'),
    'Label':                       ('Titles & Headings', 'titles_headings'),
    'Title':                       ('Titles & Headings', 'titles_headings'),
    'Heading':                     ('Titles & Headings', 'titles_headings'),
    'Table':                       ('Tables', 'tables'),
    'Embedded List Entry':         ('Lists', 'lists'),
    'Embedded List Item':          ('Lists', 'lists'),
    'List Entry':                  ('Lists', 'lists'),
    'List Footer':                 ('Lists', 'lists'),
    'List Header':                 ('Lists', 'lists'),
    'Structured List Entry':       ('Lists', 'lists'),
    'Footnote':                    ('Footnotes', 'notes_basic'),
    'Footnote Paragraph Mark':     ('Footnotes', 'notes_basic'),
    'Endnote':                     ('Footnotes', 'notes_basic'),
    'Cross Reference':             ('Footnotes', 'notes_basic'),
    'Character':                   ('Character Styling', 'characters'),
    'Special Text':                ('Special Text', ''),
    'Link text':                   ('Character Styling', 'linking'),
    'Break':                       ('Breaks', 'characters'),
    'Peripheral Ref':              ('Peripheral References', None),
    'Periph':                      ('Peripheral Materials', 'peripherals'),
    'Peripherals':                 ('Peripheral Materials', 'peripherals'),
    'Auxiliary':                   ('Peripheral Materials', 'peripherals'),
    'Concordance and Names Index': ('Peripheral Materials', 'peripherals'),
    'Study':                                    ('Extended Study Content', 'notes_study'),
    'Quotation start/end milestone':            ('Milestones', 'milestones'),
    "Translator's section start/end milestone": ('Milestones', 'milestones'),
    'Other':                       ('Other', None),
    'OBSOLETE':                    ('Obsolete & Deprecated', None),
    'DEPRECATED':                  ('Obsolete & Deprecated', None)
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
mkrexceptions = {k.lower().title(): k for k in ('BaseLine', 'TextType', 'TextProperties', 'FontName',
                'FontSize', 'FirstLineIndent', 'LeftMargin', 'RightMargin',
                'SpaceBefore', 'SpaceAfter', 'CallerStyle', 'CallerRaise',
                'NoteCallerStyle', 'NoteCallerRaise', 'NoteBlendInto', 'LineSpacing',
                'StyleType', 'ColorName', 'XMLTag', 'TEStyleName')}

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

    def load(self, sheetfiles):
        if len(sheetfiles) == 0:
            return
        self.basesheet = Sheets(sheetfiles[:-1])
        self.sheet = Sheets(sheetfiles[-1:], base=self.basesheet)
        results = {"Tables": {"th": {"thc": {}, "thr": {}}, "tc": {"tcc": {}, "tcr": {}}},
                   "Peripheral Materials": {"zpa-": {}},
                   "Identification": {"toc": {}}}
        for k, v in sorted(self.sheet.items(), key=lambda x:(len(x[0]), x[0])):
            cat = 'Other'
            if 'Name' in v:
                m = name_reg.match(str(v['Name']))
                if m:
                    if not m.group(1) and " " in m.group(2):
                        cat = m.group(2)
                    else:
                        cat = m.group(1) or m.group(3)
                else:
                    cat = str(v['Name']).strip()
                cat, url = categorymapping.get(cat, (cat, None))
                v[' category'] = cat
                v[' url'] = url
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
                m = re.match(r"^([^-\s])+\s[^-]+(?:-|$)", n)
                if m and m.group(1) not in ('OBSOLETE', 'DEPRECATED'):
                    n = k + " - " + n
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
        old = self.basesheet.get(self.marker, {})
        oldval = None
        for k, v in stylemap.items():
            if k == 'Marker':
                val = "\\" + self.marker
                urlcat = data[' url']
                urlmkr = self.marker
                if data.get('Endmarker', None):
                    val += " ... \\" + data['Endmarker']
                    urlmkr += "-" + data['Endmarker'].strip('\*')
            elif k == '_publishable':
                val = 'nonpublishable' in data.get('TextProperties', '')
                oldval = 'nonpublishable' in old.get('TextProperties', '')
            elif k.startswith("_"):
                val = v[2]
                for m, f in ((v[3](x), x) for x in (False, True)):
                    if m in old:
                        oldval = f
                    if m in data:
                        val = f
                        break
            else:
                val = data.get(k, v[2])
                oldval = old.get(k, v[2])
                if v[0].startswith("c_"):
                    val = val != v[2]
                    oldval = oldval != v[2]
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
            if v[1] is not None:
                ctxt = self.builder.get_object(v[1]).get_style_context()
                if val != oldval:
                    ctxt.add_class("changed")
                else:
                    ctxt.remove_class("changed")
        self.builder.get_object("l_url_usfm").set_uri('https://ubsicap.github.io/usfm/{}/index.html#{}'.format(urlcat, urlmkr))
        self.isLoading = False

    def item_changed(self, w, key):
        if self.isLoading:
            return
        data = self.sheet[self.marker]
        v = stylemap[key]
        w = self.builder.get_object(v[0])  # since LineSpacing triggers the checkbutton
        val = getWidgetVal(v[0], w)
        if key == '_publishable':
            if val:
                add, rem = "non", ""
            else:
                add, rem = "", "non"
            data['TextProperties'].remove(rem+'publishable')
            data['TextProperties'].add(add+'publishable')
            return
        elif key.startswith("_"):
            val = v[3](val)
            isset = getWidgetVal(v[0], w)
            other = v[3](not isset)
            if other in data:
                del data[other]
            newv = stylemap[val]
            wtemp = self.builder.get_object(newv[0])
            value = getWidgetVal(newv[0], wtemp)
            key = val
        elif key.startswith("bl_"):
            value = val[0]
        elif v[3] is not None:
            value = v[3](val)
        else:
            value = val
        data[key] = value
        if v[1] is not None:
            ctxt = self.builder.get_object(v[1]).get_style_context()
            oldval = self.basesheet.get(self.marker, {}).get(key, '')
            if v[0].startswith("s_"):
                diff = float(oldval) != float(value)
            else:
                diff = oldval != value
            if diff:
                ctxt.add_class("changed")
                # print("Adding 'changed' to {} because {} != {}".format(v[1], value, oldval))
            else:
                ctxt.remove_class("changed")
                # print("Removing 'changed' to {} because {} == {}".format(v[1], value, oldval))

    def _list_usfms(self, treeiter=None):
        if treeiter is None:
            treeiter = self.treestore.get_iter_first()
        while treeiter != None:
            if self.treestore[treeiter][2]:
                yield self.treestore[treeiter][0]
            if self.treestore.iter_has_child(treeiter):
                childiter = self.treestore.iter_children(treeiter)
                for u in self._list_usfms(childiter):
                    yield u
            treeiter = self.treestore.iter_next(treeiter)

    def _eq_val(self, a, b):
        try:
            fa = float(a)
            fb = float(b)
            return fa == fb
        except (ValueError, TypeError):
            return a == b

    def _str_val(self, v):
        if isinstance(v, (set, list)):
            return " ".join(sorted(v))
        else:
            return str(v)

    def output_diffile(self, outfh):
        def normmkr(s):
            x = s.lower().title()
            return mkrexceptions.get(x, x)
        for m in self._list_usfms():
            markerout = False
            for k,v in self.sheet[m].items():
                if k.startswith(" "):
                    continue
                other = self.basesheet[m].get(k, None)
                if not self._eq_val(other, v):
                    if not markerout:
                        outfh.write("\n\\Marker {}\n".format(m))
                        markerout = True
                    outfh.write("\\{} {}\n".format(normmkr(k), self._str_val(v)))
