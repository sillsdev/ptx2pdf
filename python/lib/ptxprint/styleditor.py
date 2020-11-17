
import re
from gi.repository import Gtk, Pango
from ptxprint.gtkutils import getWidgetVal, setWidgetVal
from ptxprint.usfmutils import Sheets
from ptxprint.sfm.style import Marker, CaselessStr
from copy import deepcopy

stylemap = {
    'Marker':       ('l_styleTag',          None,               None, None, None),
    'Description':  ('l_styDescription',    None,               None, None, None),
    'TextType':     ('fcb_styTextType',     'l_styTextType',    'Paragraph', None, None),
    'StyleType':    ('fcb_styStyleType',    'l_styStyleType',   'Paragraph', None, None),
    'FontName':     ('bl_font_styFontName', 'l_styFontName',    None, None, None),
    'Color':        ('col_styColor',        'l_styColor',       'x000000', None, None),
    'FontSize':     ('s_styFontSize',       'l_styFontSize',    '12', None, None),
    'Bold':         ('c_styFaceBold',       'c_styFaceBold',    '-', lambda v: "" if v else "-", None),
    'Italic':       ('c_styFaceItalic',     'c_styFaceItalic',  '-', lambda v: "" if v else "-", None),
    'SmallCap':     ('c_stySmallCap',       'c_stySmallCap',    '-', lambda v: "" if v else "-", None),
    'Superscript':  ('c_styFaceSuperscript', 'c_styFaceSuperscript', '-', lambda v: "" if v else "-", None),
    'Raise':        ('s_styRaise',          'l_styRaise',       '0', lambda v: str(v)+"ex", lambda v: re.sub(r"(?<=\d)\D+$", "", v)),
    'Justification': ('fcb_styJustification', 'l_styJustification', 'Justified', lambda v: "" if v == "Justified" else v, None),
    'FirstLineIndent': ('s_styFirstLineIndent', 'l_styFirstLineIndent', '0', None, None),
    'LeftMargin':   ('s_styLeftMargin',     'l_styLeftMargin',  '0', None, None),
    'RightMargin':  ('s_styRightMargin',    'l_styRightMargin', '0', None, None),
    'LineSpacing':  ('s_styLineSpacing',    'l_styLineSpacing', '0', None, None),
    'SpaceBefore':  ('s_stySpaceBefore',    'l_stySpaceBefore', '0', None, None),
    'SpaceAfter':   ('s_stySpaceAfter',     'l_stySpaceAfter',  '0', None, None),
    'CallerStyle':  ('fcb_styCallerStyle',  'l_styCallerStyle', '', None, None),
    'NoteCallerStyle': ('fcb_styNoteCallerStyle', 'l_styNoteCallerStyle', '', None, None),
    'NoteBlendInto': ('fcb_NoteBlendInto',  'l_NoteBlendInto',  '', None, None),
    'CallerRaise':  ('s_styCallerRaise',    'l_styCallerRaise', '0', None, None),
    'NoteCallerRaise': ('s_styNoteCallerRaise', 'l_styNoteCallerRaise', '0', None, None),
    '_fontsize':    ('c_styFontScale',      'c_styFontScale',   False, lambda v: "FontScale" if v else "FontSize", None),
    '_linespacing': ('c_styAbsoluteLineSpacing', 'c_styAbsoluteLineSpacing', False, lambda v: "BaseLine" if v else 'LineSpacing', None),
    '_publishable': ('c_styTextProperties', 'c_styTextProperties', False, None, None)
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
    'Special Text':                ('Special Text', 'characters'),
    'Link text':                   ('Character Styling', 'linking'),
    'Break':                       ('Breaks', 'characters'),
    'Peripheral Ref':              ('Peripheral References', 'characters'),
    'Auxiliary':                   ('Peripheral Materials', 'characters'),
    'Periph':                      ('Peripheral Materials', None),
    'Peripherals':                 ('Peripheral Materials', 'peripherals'),
    'Concordance and Names Index': ('Peripheral Materials', None),
    'Study':                                    ('Extended Study Content', 'notes_study'),
    'Quotation start/end milestone':            ('Milestones', 'milestones'),
    "Translator's section start/end milestone": ('Milestones', 'milestones'),
    'Other':                       ('Other', None),
    'OBSOLETE':                    ('Obsolete & Deprecated', None),
    'DEPRECATED':                  ('Obsolete & Deprecated', None)
}
usfmpgname = {
    'f':     'fnotes',
    'x':     'xrefs',
    'ef':    'efnotes',
    'ex':    'exrefs',
    'esb':   'sidebars',
    'esbe':  'sidebars',
    'cat':   'categories'
}

noEndmarker = ('fr', 'fq', 'fqa', 'fk', 'fl', 'fw', 'fp', 'ft', 'xo', 'xk', 'xq', 'xt', 'xta')
fxceptions  = ('fig', 'fs', 'xtSee', 'xtSeeAlso')
 
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

dialogKeys = {
    "Marker":       "t_styMarker",
    "Name":         "t_styName",
    "Description":  "tb_styDesc",
    "OccursUnder":  "t_styOccursUnder",
    "TextType":     "fcb_styTextType",
    "StyleType":    "fcb_styStyleType"
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
    try:
        return "x"+"".join("{:02X}".format(int(x)) for x in vals[:3])
    except (ValueError, TypeError):
        return ""

def textocol(s):
    if s.startswith("x"):
        try:
            vals = [int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16)]
        except (ValueError, TypeError):
            vals = [0, 0, 0]
    else:
        try:
            v = int(s)
        except (ValueError, TypeError):
            v = 0
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

    def __init__(self, model):
        self.model = model
        self.builder = model.builder
        self.treestore = self.builder.get_object("ts_styles")
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
        self.marker = None

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
                if n is None:
                    n = k
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
                urlcat = data.get(' url', '')
                urlmkr = self.marker
                if data.get('Endmarker', None):
                    val += " ... \\" + data['Endmarker']
                    if urlmkr not in noEndmarker:
                        urlmkr += "-" + data['Endmarker'].strip('\*')
                urlmkr = re.sub(r'\d', '', urlmkr)
            elif k == '_publishable':
                val = 'nonpublishable' in data.get('TextProperties', '')
                oldval = 'nonpublishable' in old.get('TextProperties', '')
            elif k.startswith("_"):
                val = v[2]
                olddat = False
                oldval = old.get(v[3](False), '')
                for m, f in ((v[3](x), x) for x in (True, False)):
                    if m in old:
                        olddat = f
                        oldval = old[m]
                    if m in data:
                        val = data[m]
                        self._setFieldVal(v, olddat, f)
                        v = stylemap[v[3](False)]
                        break
            else:
                val = data.get(k, v[2])
                oldval = old.get(k, v[2])
                if v[0].startswith("c_"):
                    val = val != v[2]
                    oldval = oldval != v[2]
            self._setFieldVal(v, oldval, val)

        stype = data.get('StyleType', '')
        _showgrid = {'Para': (True, True, False), 'Char': (False, True, False), 'Note': (False, True, True)}
        visibles = _showgrid.get(stype[:4],(True, True, True))
        for i, w in enumerate(('Para', 'Char', 'Note')):
            self.builder.get_object("fr_sty"+w+"Settings").set_visible(visibles[i])
            
        site = 'https://ubsicap.github.io/usfm'
        if urlcat is None:
            self.builder.get_object("l_url_usfm").set_uri('{}/search.html?q=%5C{}&check_keywords=yes&area=default'.format(site, urlmkr.split('-')[0]))
        else:
            usfmkeys = tuple(usfmpgname.keys())
            pgname = 'index'
            if urlmkr.split('-')[0] not in fxceptions and urlmkr.startswith(usfmkeys):
                for i in range(len(urlmkr), 0, -1):
                    if urlmkr[:i] in usfmkeys:
                        pgname = usfmpgname.get(urlmkr[:i])
                        continue
            self.builder.get_object("l_url_usfm").set_uri('{}/{}/{}.html#{}'.format(site, urlcat, pgname, urlmkr))
        self.isLoading = False

    def _setFieldVal(self, v, oldval, val):
        w = self.builder.get_object(v[0])
        if w is None:
            print("Can't find widget {}".format(v[0]))
        else:
            if v[0].startswith("bl_"):
                if val is None:
                    return
                val = (val, "")
            elif v[0].startswith("col_"):
                val = textocol(val)
            setWidgetVal(v[0], w, val if v[4] is None else v[4](val))
        if v[1] is not None:
            ctxt = self.builder.get_object(v[1]).get_style_context()
            if val != oldval:
                ctxt.add_class("changed")
            else:
                ctxt.remove_class("changed")

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
            newv = stylemap[v[3](False)]
            key = v[3](val)
            isset = getWidgetVal(v[0], w)
            other = v[3](not isset)
            if other in data:
                del data[other]
            wtemp = self.builder.get_object(newv[0])
            value = getWidgetVal(newv[0], wtemp)
        elif v[0].startswith("col_"):
            value = coltotex(val)
        elif key.startswith("bl_"):
            value = val[0]
        elif v[3] is not None:
            value = v[3](val)
        else:
            value = val
        data[key] = value
        if v[1] is not None:
            ctxt = self.builder.get_object(v[1]).get_style_context()
            oldval = self.basesheet.get(self.marker, {}).get(key, v[2])
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
            return b is None if a is None else (False if b is None else a == b)

    def _str_val(self, v, key=None):
        if isinstance(v, (set, list)):
            if key.lower() == "textproperties":
                return " ".join(x.lower().title() if x else "" for x in sorted(v))
            return " ".join(x or "" for x in v)
        else:
            return str(v)

    def output_diffile(self, outfh):
        def normmkr(s):
            x = s.lower().title()
            return mkrexceptions.get(x, x)
        for m in self._list_usfms():
            markerout = False
            sm = self.sheet[m]
            om = self.basesheet.get(m, {})
            for k,v in sm.items():
                if k.startswith(" "):
                    continue
                other = om.get(k, None)
                if not self._eq_val(other, v):
                    if not markerout:
                        outfh.write("\n\\Marker {}\n".format(m))
                        markerout = True
                    outfh.write("\\{} {}\n".format(normmkr(k), self._str_val(v, k)))

    def mkrDialog(self, newkey=False):
        dialog = self.builder.get_object("dlg_styModsdialog")
        data = self.sheet.get(self.marker, {})
        for k, v in dialogKeys.items():
            if k == "OccursUnder":
                self.model.set(v, " ".join(sorted(data.get(k, {}))))
            else:
                self.model.set(v, data.get(k, ''))
        self.model.set(dialogKeys['Marker'], '' if newkey else self.marker)
        wid = self.builder.get_object(dialogKeys['Marker'])
        if wid is not None:
            wid.set_sensitive(newkey)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            key = self.model.get(dialogKeys['Marker'])
            if key == "":
                return
            (_, selecti) = self.treeview.get_selection().get_selected()
            if key not in self.sheet:
                self.sheet[key] = Marker({" deletable": True})
                name = self.model.get(dialogKeys['Name'], '')
                m = name_reg.match(name)
                if m:
                    if not m.group(1) and " " in m.group(2):
                        cat = m.group(2)
                    else:
                        cat = m.group(1) or m.group(3)
                else:
                    cat = "Other"
                cat, url = categorymapping.get(cat, (cat, None))
                self.sheet[key][' category'] = cat
                selecti = self.treestore.get_iter_first()
                while selecti:
                    r = self.treestore[selecti]
                    if r[0] == cat:
                        selecti = self.treestore.append(selecti, [key, name, True])
                        break
                    selecti = self.treestore.iter_next(selecti)
                else:
                    selecti = self.treestore.append(None, [cat, cat, False])
                    selecti = self.treestore.append(selecti, [key, name, True])
            data = self.sheet[key]
            for k, v in dialogKeys.items():
                val = self.model.get(v)
                if k.lower() == 'occursunder':
                    val = set(val.split())
                    data[k] = val
                elif val:
                    data[k] = CaselessStr(val)
            if data['styletype'] == 'Character' or data['styletype'] == 'Note':
                data['EndMarker'] = key + "*"
                if data['styletype'] == 'Character':
                    data['OccursUnder'].add("NEST")
            #self.marker = key
            self.treeview.get_selection().select_iter(selecti)
            #self.editMarker()
        dialog.hide()

    def delKey(self):
        if self.sheet.get(self.marker, {}).get(" deletable", False):
            del self.sheet[self.marker]
            selection = self.treeview.get_selection()
            model, i = selection.get_selected()
            model.remove(i)
            self.onSelected(selection)

    def refreshKey(self):
        if self.marker in self.basesheet:
            self.sheet[self.marker] = deepcopy(self.basesheet[self.marker])
            self.editMarker()
        

