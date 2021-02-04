from gi.repository import Gtk, Pango
from ptxprint.gtkutils import getWidgetVal, setWidgetVal
from ptxprint.sfm.style import Marker, CaselessStr
from ptxprint.styleditor import StyleEditor
from ptxprint.utils import _, coltotex, textocol
import re

stylemap = {
    'Marker':       ('l_styleTag',          None,               None, None, None),
    'Description':  ('l_styDescription',    None,               None, None, None),
    'TextType':     ('fcb_styTextType',     'l_styTextType',    'Paragraph', None, None),
    'StyleType':    ('fcb_styStyleType',    'l_styStyleType',   'Paragraph', None, None),
    ' font':        ('bl_font_styFontName', 'l_styFontName',    None, None, None),
    'Color':        ('col_styColor',        'l_styColor',       'x000000', None, None),
    'FontSize':     ('s_styFontSize',       'l_styFontSize',    '12', lambda v: "{:.3f}".format(float(v) * 12), lambda v:float(v) / 12),
    'Bold':         ('c_styFaceBold',       'c_styFaceBold',    '-', lambda v: "" if v else "-", None),
    'Italic':       ('c_styFaceItalic',     'c_styFaceItalic',  '-', lambda v: "" if v else "-", None),
    'SmallCap':     ('c_stySmallCap',       'c_stySmallCap',    '-', lambda v: "" if v else "-", None),
    'Superscript':  ('c_styFaceSuperscript', 'c_styFaceSuperscript', '-', lambda v: "" if v else "-", None),
    'Raise':        ('s_styRaise',          'l_styRaise',       '0', None, lambda v: re.sub(r"(?<=\d)\D+$", "", v)),
    'Justification': ('fcb_styJustification', 'l_styJustification', 'Justified', lambda v: "" if v == "Justified" else v, None),
    'FirstLineIndent': ('s_styFirstLineIndent', 'l_styFirstLineIndent', '0', None, None),
    'LeftMargin':   ('s_styLeftMargin',     'l_styLeftMargin',  '0', None, None),
    'RightMargin':  ('s_styRightMargin',    'l_styRightMargin', '0', None, None),
    'LineSpacing':  ('s_styLineSpacing',    'l_styLineSpacing', '1', None, None),
    'SpaceBefore':  ('s_stySpaceBefore',    'l_stySpaceBefore', '0', lambda v: "{:.3f}".format(float(v) * 12), lambda v:float(v) / 12),
    'SpaceAfter':   ('s_stySpaceAfter',     'l_stySpaceAfter',  '0', lambda v: "{:.3f}".format(float(v) * 12), lambda v:float(v) / 12),
    'CallerStyle':  ('t_styCallerStyle',  'l_styCallerStyle', '', None, None),
    'NoteCallerStyle': ('t_styNoteCallerStyle', 'l_styNoteCallerStyle', '', None, None),
    'NoteBlendInto': ('t_NoteBlendInto',  'l_NoteBlendInto',  '', None, None),
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

noEndmarker = ('fr', 'fq', 'fqa', 'fk', 'fl', 'fw', 'fp', 'ft', 'xo', 'xk', 'xq', 'xt', 'xta')
fxceptions  = ('fig', 'fs', 'xtSee', 'xtSeeAlso')

name_reg = re.compile(r"^(OBSOLETE|DEPRECATED)?\s*(.*?)\s+-\s+([^-]*?)\s*(?:-\s*(.*?)\s*)?$")

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
    "Milestone":                   ("Milestones", "milestones"),
    'Other':                       ('Other', None),
    'OBSOLETE':                    ('Obsolete & Deprecated', None),
    'DEPRECATED':                  ('Obsolete & Deprecated', None)
}

stylediverts = {
    'LineSpacing': ('_linespacing', _('Line Spacing\nFactor:'), _('Baseline:')),
    'FontSize': ('_fontsize', _('Font Size\nFactor:'), _('Font Scale:'))
}

widgetsignals = {
    's': "value-changed",
    'c': "toggled",
    "bl": "clicked",
    "col": "color-set"
}

dialogKeys = {
    "Marker":       "t_styMarker",
    "EndMarker":    "t_styEndMarker",
    "Name":         "t_styName",
    "Description":  "tb_styDesc",
    "OccursUnder":  "t_styOccursUnder",
    "TextType":     "fcb_styTextType",
    "StyleType":    "fcb_styStyleType"
}

usfmpgname = {
    'f':     'fnotes',
    'x':     'xrefs',
    'rq':    'xrefs',
    'ef':    'efnotes',
    'ex':    'exrefs',
    'esb':   'sidebars',
    'esbe':  'sidebars',
    'cat':   'categories'
}

def triefit(k, base, start):
    for i in range(start, len(k)):
        if k[:i] in base:
            triefit(k, base[k[:i]], i+1)
            break
    else:
        base[k] = {}



class StyleEditorView(StyleEditor):

    def __init__(self, model):
        super().__init__(model)
        self.builder = model.builder
        self.treestore = self.builder.get_object("ts_styles")
        self.treeview = self.builder.get_object("tv_Styles")
        self.treeview.set_model(self.treestore)
        cr = Gtk.CellRendererText()
        tvc = Gtk.TreeViewColumn("Marker", cr, text=1)
        self.treeview.append_column(tvc)
        tself = self.treeview.get_selection()
        tself.connect("changed", self.onSelected)
        self.treeview.set_search_equal_func(self.tree_search)
        searchentry = self.builder.get_object("t_styleSearch")
        self.treeview.set_search_entry(searchentry)
        #self.treeview.set_enable_search(True)
        for k, v in stylemap.items():
            if v[0].startswith("l_") or k in dialogKeys:
                continue
            w = self.builder.get_object(v[0])
            #key = stylediverts.get(k, k)
            (pref, name) = v[0].split("_", 1)
            signal = widgetsignals.get(pref, "changed")
            w.connect(signal, self.item_changed, k)
        self.isLoading = False

    def setval(self, mrk, key, val, ifunchanged=False):
        super().setval(mrk, key, val, ifunchanged=ifunchanged)
        if mrk == self.marker:
            v = stylemap.get(key)
            if v is None:
                return
            self.loading = True
            self.set(v[0], val)
            self.loading = False

    def get(self, key, default=None):
        w = self.builder.get_object(key)
        if w is None:
            return None
        return getWidgetVal(key, w, default)

    def set(self, key, value):
        w = self.builder.get_object(key)
        if w is None:
            return
        setWidgetVal(key, w, value)

    def load(self, sheetfiles):
        super().load(sheetfiles)
        results = {"Tables": {"th": {"thc": {}, "thr": {}}, "tc": {"tcc": {}, "tcr": {}}},
                   "Peripheral Materials": {"zpa-": {}},
                   "Identification": {"toc": {}}}
        for k, v in sorted(self.sheet.items(), key=lambda x:(len(x[0]), x[0])):
            if k == "p":
                foundp = True
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
        if foundp:
            self.selectMarker("p")

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

    def selectMarker(self, marker):
        root = self.treestore.get_iter_first()
        it = self._searchMarker(root, marker)
        path = self.treestore.get_path(it)
        self.treeview.expand_to_path(path)
        self.treeview.get_selection().select_path(path)

    def _searchMarker(self, it, marker):
        while it is not None:
            if self.treestore[it][0] == marker:
                return it
            if self.treestore.iter_has_child(it):
                childit = self.treestore.iter_children(it)
                ret = self._searchMarker(childit, marker)
                if ret is not None:
                    return ret
            it = self.treestore.iter_next(it)
        return None

    def tree_search(self, model, colmn, key, rowiter):
        root = self.treestore.get_iter_first()
        it = self._searchMarker(root, key.lower())
        if it is None:
            return False
        path = model.get_path(it)
        self.treeview.expand_to_path(path)
        self.treeview.scroll_to_cell(path)
        return True

    def editMarker(self):
        self.isLoading = True
        data = self.sheet.get(self.marker, {})
        old = self.basesheet.get(self.marker, {})
        oldval = None
        if 'LineSpacing' not in old and 'BaseLine' not in old:
            old['LineSpacing'] = "1"
            if 'LineSpacing' not in data and 'BaseLine' not in data:
                data['LineSpacing'] = "1"
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
                basekey = v[3](v[2])
                obasekey = v[3](not v[2])
                oldval = old.get(basekey, old.get(obasekey, ''))
                val = data.get(basekey, oldval)
                olddat = v[2]
                controlk = v[3](False)
                for m, f in ((v[3](x), x) for x in (v[2], not v[2])):
                    if m in old:
                        olddat = f
                        oldval = old[m]
                        if m.lower() == "baseline":
                            oldval = re.sub(r"(-?\d*\.?\d*)(\D|$)", r"\1", str(oldval))
                    if m in data:
                        val = data[m]
                        if m.lower() == "baseline":
                            val = re.sub(r"(-?\d*\.?\d*)(\D|$)", r"\1", str(val))
                        self._setFieldVal(v, olddat, f)
                        v = stylemap[v[3](False)]
                        break
                else:
                    f = v[2]
                newlabel = stylediverts[controlk][2 if f else 1]
                controlw = stylemap[controlk][1]
                self.set(controlw, newlabel)
                old[" "+k] = olddat
            else:
                oldval = old.get(k, v[2])
                val = data.get(k, oldval)
                if v[0].startswith("c_"):
                    val = val != v[2]
                    oldval = oldval != v[2]
            self._setFieldVal(v, oldval, val)

        stype = data.get('StyleType', old.get('StyleType', ''))
        _showgrid = {'Para': (True, True, False), 'Char': (False, True, False), 'Note': (True, True, True)}
        visibles = _showgrid.get(stype[:4],(True, True, True))
        for i, w in enumerate(('Para', 'Char', 'Note')):
            self.builder.get_object("ex_sty"+w).set_expanded(visibles[i])
            
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
            if v[0].startswith("col_"):
                newval = textocol(val)
            else:
                newval = val
            setWidgetVal(v[0], w, newval if v[4] is None else v[4](newval))
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
        val = self.get(v[0], v[2])
        if key == '_publishable':
            if val:
                add, rem = "non", ""
            else:
                add, rem = "", "non"
            try:
                data['TextProperties'].remove(rem+'publishable')
            except KeyError:
                pass
            data['TextProperties'].add(add+'publishable')
            return
        elif key in stylediverts:
            newk = stylediverts[key][0]
            newv = stylemap[newk]
            isset = self.get(newv[0], newv[2])
            key = newv[3](isset)
            other = newv[3](not isset)
            if other in data:
                del data[other]
            value = val
        elif v[0].startswith("col_"):
            value = coltotex(val)
        elif key.startswith("_"):
            newkey = v[3](val)
            otherkey = v[3](not val)
            controlk = v[3](False)
            self._setData(newkey, self._convertabs(newkey, data.get(otherkey, None)))
            self.set(stylemap.get(newkey, stylemap.get(otherkey, [None]))[0], data[newkey])
            newlabel = stylediverts[controlk][2 if val else 1]
            controlw = stylemap[controlk][1]
            self.set(controlw, newlabel)
            if otherkey in data:
                del data[otherkey]
            value = val
        elif v[3] is not None:
            value = v[3](val)
        else:
            value = val
        if not key.startswith("_"):
            self._setData(key, value)
        if v[1] is not None:
            ctxt = self.builder.get_object(v[1]).get_style_context()
            if key.startswith("_"):
                oldval = self.basesheet.get(" "+key, False)
            else:
                oldval = self.basesheet.get(self.marker, {}).get(key, v[2])
            if v[0].startswith("s_"):
                diff = abs(self.asFloatPts(oldval) - self.asFloatPts(value)) > 0.05
            else:
                diff = oldval != value
            if diff:
                ctxt.add_class("changed")
            else:
                ctxt.remove_class("changed")

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

    def mkrDialog(self, newkey=False):
        dialog = self.builder.get_object("dlg_styModsdialog")
        data = self.sheet.get(self.marker, {})
        for k, v in dialogKeys.items():
            if k == "OccursUnder":
                self.model.set(v, " ".join(sorted(data.get(k, {}))))
            elif data.get(k, '') is not None:
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
                if k == 'Marker':
                    continue
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
            self.marker = key
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
        if self.marker in self.sheet:
            self.sheet[self.marker] = {k: v for k,v in self.sheet[self.marker].items() if k in dialogKeys}
            self.editMarker()
        
    def resetParam(self, label):
        if label is None:
            return
        for k, v in stylemap.items():
            if v[1] == label:
                break
        else:
            return
        old = self.basesheet.get(self.marker, {})
        if k in stylediverts:
            newk = stylediverts[k][0]
            newval = old.get(" "+newk, None)
            if newval is not None:
                self._setFieldVal(stylemap[newk], newval, newval)
        oldval = old.get(k, v[2])
        self._setFieldVal(v, oldval, oldval)

