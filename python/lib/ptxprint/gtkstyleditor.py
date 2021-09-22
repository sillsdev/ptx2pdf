from gi.repository import Gtk, Pango
from ptxprint.gtkutils import getWidgetVal, setWidgetVal
from ptxprint.sfm.style import Marker, CaselessStr
from ptxprint.styleditor import StyleEditor, aliases
from ptxprint.utils import _, coltotex, textocol, asfloat
import re

stylemap = {
    'Marker':       ('l_styleTag',          None,               None, None, None),
    'Description':  ('l_styDescription',    None,               None, None, None),
    'TextType':     ('fcb_styTextType',     'l_styTextType',    'Paragraph', None, None),
    'StyleType':    ('fcb_styStyleType',    'l_styStyleType',   'Paragraph', None, None),
    'FontName':     ('bl_font_styFontName', 'l_styFontName',    None, None, None),
    'Color':        ('col_styColor',        'l_styColor',       'x000000', None, None),
    'FontSize':     ('s_styFontSize',       'l_styFontSize',    1, None, None),
    'Bold':         ('c_styFaceBold',       'c_styFaceBold',    False, None, None),
    'Italic':       ('c_styFaceItalic',     'c_styFaceItalic',  False, None, None),
    'Smallcaps':    ('c_stySmallCap',       'c_stySmallCap',    False, None, None),
    'Superscript':  ('c_styFaceSuperscript', 'c_styFaceSuperscript', False, None, None),
    'Raise':        ('s_styRaise',          'l_styRaise',       0, None, None, None),
    'Justification': ('fcb_styJustification', 'l_styJustification', 'Justified', lambda v: "" if v == "Justified" else v, None),
    'FirstLineIndent': ('s_styFirstLineIndent', 'l_styFirstLineIndent', '0', None, None),
    'LeftMargin':   ('s_styLeftMargin',     'l_styLeftMargin',  0, None, None),
    'RightMargin':  ('s_styRightMargin',    'l_styRightMargin', 0, None, None),
    'LineSpacing':  ('s_styLineSpacing',    'l_styLineSpacing', 1, None, None),
    'SpaceBefore':  ('s_stySpaceBefore',    'l_stySpaceBefore', 0, None, None),
    'SpaceAfter':   ('s_stySpaceAfter',     'l_stySpaceAfter',  0, None, None),
    'CallerStyle':  ('t_styCallerStyle',  'l_styCallerStyle', '', None, None),
    'NoteCallerStyle': ('t_styNoteCallerStyle', 'l_styNoteCallerStyle', '', None, None),
    'NoteBlendInto': ('t_NoteBlendInto',  'l_NoteBlendInto',  '', None, None),
    'CallerRaise':  ('s_styCallerRaise',    'l_styCallerRaise', 0, None, None),
    'NoteCallerRaise': ('s_styNoteCallerRaise', 'l_styNoteCallerRaise', 0, None, None),
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
dualmarkers = {'BaseLine': 'LineSpacing', 'FontScale': 'FontSize'}

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
    'Milestone':                   ('Milestones', 'milestones'),
    'Other':                       ('Other', None),
    'OBSOLETE':                    ('Obsolete & Deprecated', None),
    'DEPRECATED':                  ('Obsolete & Deprecated', None),
    'Module Import':               ('Module', 'modules'),
    'Module Include Options':      ('Module', 'modules'),
    'Module Text Replacement':     ('Module', 'modules'),
    'Module Verse Reference':      ('Module', 'modules'),
    'Module Verse Reference No Paragraphs':     ('Module', 'modules'),
    'Module Versification':        ('Module', 'modules') 
}

widgetsignals = {
    "s": "value-changed",
    "c": "toggled",
    "bl": None,
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
            if signal is not None:
                w.connect(signal, self.item_changed, k)
            # if v[0].startswith("s_"):
            #     w.connect("focus-out-event", self.item_changed, k)
        self.isLoading = False
        self.stylediverts = {
            "LineSpacing": ("_linespacing", _("Line Spacing\nFactor:"), _("Baseline:")),
            "FontSize": ("_fontsize", _("Font Size\nFactor:"), _("Font Scale:"))
        }


    def setval(self, mrk, key, val, ifunchanged=False):
        super().setval(mrk, key, val, ifunchanged=ifunchanged)
        if mrk == self.marker:
            v = stylemap.get(dualmarkers.get(key, key))
            if v is None:
                return
            self.loading = True
            self.set(v[0], val or "")
            if key == "Color":
                self.set("l_styColorValue", str(val))
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
        try:
            setWidgetVal(key, w, value)
        except (TypeError, ValueError) as e:
            raise e.__class__("{} for widget {}".format(e, key))

    def load(self, sheetfiles):
        super().load(sheetfiles)
        results = {"Tables": {"th": {"thc": {}, "thr": {}}, "tc": {"tcc": {}, "tcr": {}}},
                   "Peripheral Materials": {"zpa-": {}},
                   "Identification": {"toc": {}}}
        for k in sorted(self.allStyles(), key=lambda x:(len(x), x)):
            # v = self.sheet.get(k, self.basesheet.get(k, {}))
            v = self.asStyle(k)
            if 'zDerived' in v:
                # self.sheet[v['zDerived']][' endMilestone']=k
                self.setval(v['zDerived'], ' endMilestone', k)
                continue
            if k not in self.basesheet:
                # v[' deletable'] = True
                self.setval(k, ' deletable', True)
            if k == "p":
                foundp = True
            cat = 'Other'
            if 'Name' in v:
                if not v['Name']:
                    v['Name'] = "{} - Other".format(k)
                m = name_reg.match(str(v['Name']))
                if m:
                    if not m.group(1) and " " in m.group(2):
                        cat = m.group(2)
                    else:
                        cat = m.group(1) or m.group(3)
                else:
                    cat = str(v['Name']).strip()
                cat, url = categorymapping.get(cat, (cat, None))
                # v[' category'] = cat
                self.setval(k, ' category', cat)
                # v[' url'] = url
                self.setval(k, ' url', url)
            else:
                print(k)
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
        allStyles = self.allStyles()
        for k, v in sorted(d.items(), key=keyfn):
            ismarker = True
            if k in allStyles:
                # n = self.sheet[k].get('name', k)
                n = self.getval(k, 'name') or ""
                m = re.match(r"^([^-\s]*)\s*([^-]+)(?:-\s*|$)", n)
                if m:
                    if m.group(1) and m.group(1) not in ('OBSOLETE', 'DEPRECATED'):
                        n = k + " - " + n
                    elif m.group(2):
                        n = k + " - " + n[m.end():]
            elif k not in self.basesheet:
                ismarker = False
                n = k
            else:
                n = k
            s = [str(k), str(n), ismarker]
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
        if self.marker is None:
            return
        if self.marker in aliases:
            self.marker += "1"
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
                # val = 'nonpublishable' in data.get('TextProperties', '')
                props = data.get('TextProperties', set())
                if not isinstance(props, set):
                    props = set(props.split())
                val = 'nonpublishable' in (x.lower() for x in props)
                # oldval = 'nonpublishable' in old.get('TextProperties', '')
                oldval = 'nonpublishable' in (x.lower() for x in old.get('TextProperties', []))
            elif k.startswith("_"):
                basekey = v[3](v[2])        # default data key e.g. "FontSize"
                obasekey = v[3](not v[2])   # non-default data key e.g. "FontScale"
                oldval = self.getval(self.marker, basekey, self.getval(self.marker, obasekey, baseonly=True), baseonly=True)
                val = self.getval(self.marker, basekey)
                olddat = v[2]
                controlk = v[3](False)
                # try each switch state
                for m, f in ((v[3](x), x) for x in (not v[2], v[2])):
                    if m in old:            # key in underlying?
                        olddat = f          # set the state and get the val
                        oldval = self.getval(self.marker, m)
                    if m in data:
                        val = self.getval(self.marker, m)
                        self._setFieldVal(m, v, olddat, f)
                        break
                else:
                    f = olddat
                    val = oldval
                r = v[3](f)
                v = stylemap[dualmarkers.get(r, r)]
                newlabel = self.stylediverts[controlk][2 if f else 1]
                controlw = stylemap[controlk][1]
                self.set(controlw, newlabel)
                old[" "+k] = olddat
            else:
                oldval = self.getval(self.marker, k, v[2], baseonly=True)
                val = self.getval(self.marker, k, v[2])
                if v[0].startswith("c_"):
                    val = val or False
                    oldval = oldval or False
            if k == "_fontsize":
                fstyles = []
                fref = self.getval(self.marker, 'FontName')
                if fref is None:
                    fref = self.model.get("bl_fontR")
                f = fref.getTtfont() if fref is not None else None
                bfontsize = float(self.model.get("s_fontsize"))
                fsize = asfloat(val, 1.) * bfontsize
                if f is not None:
                    asc = f.ascent / f.upem * bfontsize
                    des = f.descent / f.upem * bfontsize
                    self.set("l_styActualFontSize", "{}\n{:.1f}pt (+{:.1f} -{:.1f})".format(fref.name, fsize, asc, -des))
                else:
                    self.set("l_styActualFontSize", "{:.1f}pt".format(fsize))
            self._setFieldVal(k, v, oldval, val)

        stype = self.getval(self.marker, 'StyleType')
        _showgrid = {'Para': (True, True, False), 'Char': (False, True, False), 'Note': (True, True, True)}
        visibles = _showgrid.get(stype[:4] if stype is not None else "",(True, True, True))
        for i, w in enumerate(('Para', 'Char', 'Note')):
            self.builder.get_object("ex_sty"+w).set_expanded(visibles[i])

        if not self.model.get("c_noInternet"):
            site = 'https://ubsicap.github.io/usfm'
            tl = self.get("fcb_interfaceLang") # target language for Google Translate
            ggltrans = "" 
            if not self.model.get("c_useEngLinks") and \
                   tl in ['ar_SA', 'my', 'zh', 'fr', 'hi', 'hu', 'id', 'ko', 'pt', 'ro', 'ru', 'es', 'th']:
                ggltrans = r"https://translate.google.com/translate?sl=en&tl={}&u=".format(tl)
            if urlcat is None:
                self.builder.get_object("l_url_usfm").set_uri('{}{}/search.html?q=%5C{}&check_keywords=yes&area=default'.format(ggltrans, site, urlmkr.split('-')[0]))
            else:
                usfmkeys = tuple(usfmpgname.keys())
                pgname = 'index'
                if urlmkr.split('-')[0] not in fxceptions and urlmkr.startswith(usfmkeys):
                    for i in range(len(urlmkr), 0, -1):
                        if urlmkr[:i] in usfmkeys:
                            pgname = usfmpgname.get(urlmkr[:i])
                            continue
                self.builder.get_object("l_url_usfm").set_uri('{}{}/{}/{}.html#{}'.format(ggltrans, site, urlcat, pgname, urlmkr))
        self.isLoading = False

    def _cmp(self, a, b):
        try:
            fa = float(a)
            fb = float(b)
            return fb == fa
        except (TypeError, ValueError):
            return a == b

    def _setFieldVal(self, k, v, oldval, val):
        w = self.builder.get_object(v[0])
        if w is None:
            print("Can't find widget {}".format(v[0]))
        else:
            if v[0].startswith("col_"):
                newval = textocol(val)
                self.set("l_styColorValue", val)
            else:
                newval = val
            if newval is None:
                dflt = self.getval('p', k)
                self.set(v[0], dflt)
            else:
                self.set(v[0], newval)
        if v[1] is not None:
            ctxt = self.builder.get_object(v[1]).get_style_context()
            if oldval is not None and not self._cmp(val, oldval):
                ctxt.add_class("changed")
            else:
                ctxt.remove_class("changed")

    def item_changed(self, w, *a):
        if self.isLoading:
            return
        key = a[-1]
        data = self.asStyle(self.marker)
        v = stylemap[key]
        val = self.get(v[0], v[2])
        if key == '_publishable':
            if val:
                add, rem = "non", ""
            else:
                add, rem = "", "non"
            props = self.sheet.setdefault(self.marker, {}).setdefault('TextProperties', set())
            if props is None:
                props = set()
                self.sheet[self.marker]['TextProperties'] = props
            try:
                props.remove(rem+'publishable')
            except KeyError:
                pass
            props.add(add+'publishable')
            return
        elif key in self.stylediverts:
            newk = self.stylediverts[key][0]
            newv = stylemap[newk]
            isset = self.get(newv[0], newv[2])
            # print(f"{key=}[{isset=}=>{newv[3](isset)}]: {val=}")
            key = newv[3](isset)
            other = newv[3](not isset)
            if other in data:
                super(self.__class__, self).setval(self.marker, key, None)
            value = val if isset or v[3] is None else v[3](val) # v[4 if isset else 3] is None else v[4 if isset else 3](val)
        elif v[0].startswith("col_"):
            value = coltotex(val)
        elif key.startswith("_"):
            newkey = v[3](val)
            otherkey = v[3](not val)
            controlk = v[3](False)
            newv = stylemap.get(newkey, stylemap.get(otherkey, [None]))
            oldval = self.getval(self.marker, otherkey)
            newval = self._convertabs(newkey, oldval)
            self.setval(self.marker, newkey, newval)
            # print(f"{newkey}: {oldval=} -> {newval=} | {self.getval(self.marker, newkey)}")
            newlabel = self.stylediverts[controlk][2 if val else 1]
            controlw = stylemap[controlk][1]
            self.set(controlw, newlabel)
            if otherkey in data:
                super(self.__class__, self).setval(self.marker, otherkey, None)
            value = val
            # value = val if newv[3] is None else newv[3](val)
        elif v[3] is not None:
            value = v[3](val)
        else:
            value = val
        if not key.startswith("_"):
            super(self.__class__, self).setval(self.marker, key, value)
            if key == "FontSize":
                self.set("l_styActualFontSize", "{:.1f}pt".format(float(value) * float(self.model.get("s_fontsize"))))
        if v[1] is not None:
            ctxt = self.builder.get_object(v[1]).get_style_context()
            if key.startswith("_"):
                oldval = self.basesheet.get(self.marker, {}).get(" "+key, False)
            else:
                oldval = self.getval(self.marker, key, v[2], baseonly=True)
            if v[0].startswith("s_"):
                diff = abs(float(oldval) - float(value)) > 0.001
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
        for k, v in dialogKeys.items():
            if k == "OccursUnder":
                self.model.set(v, " ".join(sorted(self.getval(self.marker, k, {}))))
            elif self.getval(self.marker, k) is not None:
                self.model.set(v, self.getval(self.marker, k, ''))
        self.model.set(dialogKeys['Marker'], '' if newkey else self.marker)
        wid = self.builder.get_object(dialogKeys['Marker'])
        if wid is not None:
            wid.set_sensitive(newkey)
        tryme = True
        while tryme:
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                key = self.model.get(dialogKeys['Marker']).strip().replace("\\","")
                if key == "":
                    break
                for a in ('StyleType', 'TextType', 'OccursUnder'):
                    if not self.model.get(dialogKeys[a]):
                        self.model.doError(_("Required element {} is not set. Please set it").format(a))
                        break
                else:
                    tryme = False
                if tryme:
                    continue
                (d, selecti) = self.treeview.get_selection().get_selected()
                name = self.model.get(dialogKeys['Name'], '')
                if key not in self.sheet:
                    self.sheet[key] = Marker({" deletable": True})
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
                else:
                    self.treestore.set_value(selecti, 1, name)
                for k, v in dialogKeys.items():
                    if k == 'Marker':
                        continue
                    val = self.model.get(v).replace("\\","")
                    # print(f"{k=} {v=} -> {val=}")
                    if k.lower() == 'occursunder':
                        val = set(val.split())
                    self.setval(self.marker, k, val)
                st = self.getval(self.marker, 'StyleType', '')
                if st == 'Character' or st == 'Note':
                    self.setval(self.marker, 'EndMarker', key + "*")
                    if st == 'Character':
                        ou = self.getval(self.marker, 'OccursUnder')
                        if not isinstance(ou, set):
                            ou = set(ou.split())
                        ou.add("NEST")
                        self.setval(self.marker, 'OccursUnder', ou)
                    self.resolveEndMarker(key, None)
                elif st == 'Milestone':
                    self.resolveEndMarker(key, self.getval(self.marker, 'EndMarker'))
                    self.setval(self.marker, 'EndMarker', None)
                self.marker = key
                self.treeview.get_selection().select_iter(selecti)
            else:
                tryme = False
                #self.editMarker()
        dialog.hide()

    def resolveEndMarker(self, key, newval):
        endm = self.getval(self.marker, key, ' endMilestone')
        if endm is not None and endm != ' None' and endm != newval:
            derivation = self.getval(endm, 'zDerived')
            if derivation is not None:
                if endm in self.sheet:
                    del self.sheet[endm]
                if endm in self.basesheet:
                    del self.basesheet[endm]
        st = self.getval(self.marker, 'StyleType')
        if st == 'Milestone':
            if newval is None:
                if self.getval(self.marker, ' endMarker') is not None:
                    self.setval(self.marker, ' endMarker', ' None')
            elif newval != endm:
                self.setval(self.marker, ' endMarker', newval)

    def delKey(self, key=None):
        if key is None:
            key = self.marker
        if self.sheet.get(key, {}).get(" deletable", False):
            del self.sheet[key]
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
        if k in self.stylediverts:
            newk = self.stylediverts[k][0]
            newval = old.get(" "+newk, None)
            if newval is not None:
                self._setFieldVal(k, stylemap[newk], newval, newval)
        oldval = self.getval(self.marker, k, baseonly=True)
        self._setFieldVal(k, v, oldval, oldval)
