from gi.repository import Gtk, Pango, GLib
from ptxprint.gtkutils import getWidgetVal, setWidgetVal
from ptxprint.styleditor import StyleEditor, aliases
from ptxprint.usxutils import mrktype
from ptxprint.utils import _, coltotex, textocol, asfloat
from ptxprint.imagestyle import imageStyleFromStyle, ImageStyle
from ptxprint.borderstyle import borderStyleFromStyle, BorderStyle
from usfmtc.usfmparser import Grammar
import re, logging

logger = logging.getLogger(__name__)

# .sty marker:  control id, label id, default, fn -> sty marker, None
stylemap = {
    'Marker':       ('l_styleTag',          None,               None, None, None),
    'Description':  ('l_styDescription',    None,               None, None, None),
    'mrktype':      ('fcb_styType',         'l_styType',        'Paragraph', None, None),
    'font':         ('bl_font_styFontName', 'l_styFontName',    None, None, None),
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
    'NonJustifiedFill':  ("s_styNonJustifiedFill", "l_styNonJustifiedFill", 0.25, None, None),
    'CallerStyle':  ('t_styCallerStyle',    'l_styCallerStyle', '', None, None),
    'NoteCallerStyle': ('t_styNoteCallerStyle', 'l_styNoteCallerStyle', '', None, None),
    'NoteBlendInto': ('t_NoteBlendInto',    'l_NoteBlendInto',  '', None, None),
    'CallerRaise':  ('s_styCallerRaise',    'l_styCallerRaise', 0, None, None),
    'NoteCallerRaise': ('s_styNoteCallerRaise', 'l_styNoteCallerRaise', 0, None, None),
    'Position':     ('t_sbPgPos',           None, 't', None, None),
    'Scale':        ('s_sbWidth',           'l_sbWidth',        1, None, None),
    'Alpha':        ('s_sbAlpha',           'l_sbAlpha',        0.5, None, None),
    'BgColor':      ('col_sb_backColor',    'l_sb_backColor', '0.8 0.8 0.8', None, None),
    'VerticalAlign': ('fcb_stytcVpos',      None,               None, None, None),

    '_fontsize':    ('c_styFontScale',           'c_styFontScale',   False, lambda v: "FontScale" if v else "FontSize", None),
    '_linespacing': ('c_styAbsoluteLineSpacing', 'c_styAbsoluteLineSpacing', False, lambda v: "BaseLine" if v else 'LineSpacing', None),
    '_publishable': ('c_styTextProperties',      'c_styTextProperties', False, None, None)
}

topLevelOrder = (
    _('Identification'), 
    _('Introduction'), 
    _('Chapters & Verses'), 
    _('Paragraphs'), 
    _('Poetry'), 
    _('Titles & Headings'), 
    _('Tables'), 
    _('Lists'), 
    _('Footnotes'), 
    _('Cross References'), 
    _('Special Text'), 
    _('Character Styling'), 
    _('Cover'), 
    _('Diglot'), 
    _('Module'), 
    _('Peripheral Materials'), 
    _('Peripheral References'), 
    _('Extended Study Content'), 
    _("Strong's Index"), 
    _('Milestones'), 
    _('Conditional text'), 
    _('Breaks'), 
    _('Other'), 
    _('Obsolete & Deprecated'))
catorder = {k: i for i, k in enumerate(topLevelOrder)}

noEndmarker = ('fr', 'fq', 'fqa', 'fk', 'fl', 'fw', 'fp', 'ft', 'xo', 'xk', 'xq', 'xt', 'xta')
fxceptions  = ('fig', 'fs', 'xtSee', 'xtSeeAlso')
dualmarkers = {'BaseLine': 'LineSpacing', 'FontScale': 'FontSize'}

name_reg = re.compile(r"^(OBSOLETE|DEPRECATED)?\s*(.*?)\s+-\s+([^-]*?)\s*(?:-\s*(.*?)\s*)?$")

    # '*Publication':                '*DROP from list*'
categorymapping = {
    'File':                                     (_('Identification'), 'identification'),
    'Identification':                           (_('Identification'), 'identification'),
    'Introduction':                             (_('Introduction'), 'introductions'),
    'Chapter':                                  (_('Chapters & Verses'), 'chapters_verses'),
    'Chapter Number':                           (_('Chapters & Verses'), 'chapters_verses'),
    'Reference':                                (_('Chapters & Verses'), 'chapters_verses'),
    'Verse Number':                             (_('Chapters & Verses'), 'chapters_verses'),
    'Paragraph':                                (_('Paragraphs'), 'paragraphs'),
    'Poetry':                                   (_('Poetry'), 'poetry'),
    'Poetry Text':                              (_('Poetry'), 'poetry'),
    'Label':                                    (_('Titles & Headings'), 'titles_headings'),
    'Title':                                    (_('Titles & Headings'), 'titles_headings'),
    'Heading':                                  (_('Titles & Headings'), 'titles_headings'),
    'Table':                                    (_('Tables'), 'tables'),
    'Embedded List Entry':                      (_('Lists'), 'lists'),
    'Embedded List Item':                       (_('Lists'), 'lists'),
    'List Entry':                               (_('Lists'), 'lists'),
    'List Footer':                              (_('Lists'), 'lists'),
    'List Header':                              (_('Lists'), 'lists'),
    'Structured List Entry':                    (_('Lists'), 'lists'),
    'Footnote':                                 (_('Footnotes'), 'notes_basic'),
    'Footnote Paragraph Mark':                  (_('Footnotes'), 'notes_basic'),
    'Endnote':                                  (_('Footnotes'), 'notes_basic'),
    'Cross Reference':                          (_('Footnotes'), 'notes_basic'),
    'Character':                                (_('Character Styling'), 'characters'),
    'Special Text':                             (_('Special Text'), 'characters'),
    'Link text':                                (_('Character Styling'), 'linking'),
    'Break':                                    (_('Breaks'), 'characters'),
    'Peripheral Ref':                           (_('Peripheral References'), 'characters'),
    'Auxiliary':                                (_('Peripheral Materials'), 'characters'),
    'Periph':                                   (_('Peripheral Materials'), None),
    'Peripherals':                              (_('Peripheral Materials'), 'peripherals'),
    'Concordance and Names Index':              (_('Peripheral Materials'), None),
    'Study':                                    (_('Extended Study Content'), 'notes_study'),
    "Strong's":                                 (_("Strong's Index"), None),
    'Module Import':                            (_('Module'), 'modules'),
    'Module Include Options':                   (_('Module'), 'modules'),
    'Module Text Replacement':                  (_('Module'), 'modules'),
    'Module Verse Reference':                   (_('Module'), 'modules'),
    'Module Verse Reference No Paragraphs':     (_('Module'), 'modules'),
    'Module Versification':                     (_('Module'), 'modules'), 
    'Quotation start/end milestone':            (_('Milestones'), 'milestones'),
    "Translator's section start/end milestone": (_('Milestones'), 'milestones'),
    'Milestone':                                (_('Milestones'), 'milestones'),
    'Other':                                    (_('Other'), None),
    'OBSOLETE':                                 (_('Obsolete & Deprecated'), None),
    'DEPRECATED':                               (_('Obsolete & Deprecated'), None)
}

usfmDocsPath = {
# 1st 2 lines are fallback links
'markers/char': 'add addpn allchars bd bdit bk dc em fdc fk fl fm fp fqa fq fr ft fv fw ior iqt it k lik litl liv nd no ord pn png pro qac qs qt rb sc sig sls sup tc tcr th thr tl wa w wg wh wj xdc xk xnt xo xop xot xq xta xt',
'markers/para': 'b cd cl cls d h ib id ide ie iex ili im imi imq imt imte io iot ip ipi ipq ipr iq is lf lh li lim m mi mr ms mt mte nb p pb pc ph pi pm pmc pmo pmr po pr qa q qc qd qm qr r rem s sd sp sr sts toca toc tr usfm',
'char/breaks': 'pb',
'char/features': 'add addpn bk dc k nd ord pn png pro qt rb sig sls tl wa w wg wh wj',
'char/format': 'bd bdit em it no sc sup',
'char/introductions': 'ior iqt',
'char/lists': 'lik litl liv',
'char/poetry': 'qac qs',
'char/tables': 'tc tcr th thr',
'markers/cv': 'ca c cp va v vp',
'markers/fig': 'fig',
'markers/ms': 'qt ts',
'markers/note': 'ef f fe f x',
'markers/periph': 'periph',
'markers/sbar': 'esb',
'note/crossref': 'ex x',
'note/footnote': 'ef f fe',
'para/identification': 'books h id ide rem sts toca toc usfm',
'para/introductions': 'ib ie iex ili im imi imq imt imte io iot ip ipi ipq ipr iq is',
'para/lists': 'lf lh li lim',
'para/paragraphs': 'b cls m mi nb p pc ph pi pm pmc pmo pmr po pr',
'para/poetry': 'b qa q qc qd qm qr',
'para/tables': 'tr',
'para/titles-sections': 'cd cl d mr ms mt mte r s sd sp sr',
}
mkr2path = {w:k for k,v in usfmDocsPath.items() for w in v.split()}

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
    "Description":  "txbf_styDesc",
    "mrktype":      "fcb_styType"
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
#    if start == len(k) and start > 1:
#        return
    for i in range(start, len(k)):
        if k[:i] in base:
            triefit(k, base[k[:i]], i+1)
            break
    else:
        base[k] = {}


class StyleEditorView(StyleEditor):

    def __init__(self, model):
        super().__init__(model)
        self.mrkrlist = []
        self.stylediverts = {
            "LineSpacing": ("_linespacing", _("Line Spacing\nFactor:"), _("Baseline:")),
            "FontSize": ("_fontsize", _("Font Size\nFactor:"), _("Font Scale:"))
        }
        self.builder = model.builder
        self.treestore = self.builder.get_object("ts_styles")
        self.treeview = self.builder.get_object("tv_Styles")
        self.filter = self.treestore.filter_new()
        self.filter_state = False
        self.filter.set_visible_func(self.apply_filter)
        self.treeview.set_model(self.filter)
        cr = Gtk.CellRendererText()
        tvc = Gtk.TreeViewColumn("Marker", cr, text=1, strikethrough=3)
        self.treeview.append_column(tvc)
        # initialize the search match set and attach painter
        self._search_matches = set()
        tvc.set_cell_data_func(cr, self._paint_tree_row)
        tself = self.treeview.get_selection()
        tself.connect("changed", self.onSelected)
        # The original interactive search caused issues. We now use a manual, delayed search.
        searchentry = self.builder.get_object("t_styleSearch")
        self.treeview.set_search_entry(None) # Explicitly disable
        self.search_timer_id = None
        searchentry.connect("search-changed", self.on_search_changed)
        for k, v in stylemap.items():
            if v[0].startswith("l_") or k in dialogKeys:
                continue
            w = self.builder.get_object(v[0])
            #key = stylediverts.get(k, k)
            (pref, name) = v[0].split("_", 1)
            signal = widgetsignals.get(pref, "changed")
            if signal is not None:
                w.connect(signal, self.item_changed, k)
        self.isLoading = False

    def _paint_tree_row(self, column, cell, model, treeiter, data=None):
        """
        - Top-level rows: blue foreground (#72729f9fcfcf) and bold.
        - Matched rows: pale peach background (#fce8d9).
        - Everyone else: inherit theme colors.
        """
        # Clear any explicit styling first so rows not matching revert to theme
        cell.set_property('foreground-set', False)
        cell.set_property('cell-background-set', False)
        cell.set_property('weight', Pango.Weight.NORMAL)

        try:
            path = model.get_path(treeiter)   # works with GtkTreeModelFilter too
        except Exception:
            return

        # Top-level (depth==1): blue label
        if len(path) == 1:
            cell.set_property('foreground', '#72729f9fcfcf') # pale blue
            cell.set_property('foreground-set', True)
            cell.set_property('weight', Pango.Weight.BOLD)

        # Search highlight: compare stringified path
        matches = getattr(self, '_search_matches', None)
        if matches and path.to_string() in matches:
            cell.set_property('cell-background', '#fce8d9') # pale peach
            cell.set_property('cell-background-set', True)

    def on_search_changed(self, entry):
        """Debounces search entry changes to avoid rapid, repeated searches."""
        # Read the current text FIRST
        key = entry.get_text()

        # If a previous timer is pending, cancel it
        if getattr(self, "search_timer_id", None) is not None:
            GLib.source_remove(self.search_timer_id)
            self.search_timer_id = None

        # If the box is empty, clear highlights immediately
        if not key.strip():
            # Make sure this exists somewhere (e.g., set() in __init__)
            self._search_matches = set()
            # collapse everything to remove search-driven expansion
            # self.treeview.collapse_all()
            self.treeview.queue_draw()
        # Start (or restart) the debounce timer
        self.search_timer_id = GLib.timeout_add(500, self.do_search, entry)

    def do_search(self, entry):
        """Performs the search after the 500ms delay."""
        # Clear the timer id since we're firing now
        self.search_timer_id = None

        key = entry.get_text().strip()
        if not key:
            # Nothing to search; keep highlights cleared by on_search_changed
            return False  # stop the timer

        self.tree_search(self.treeview.get_model(), 0, key, None)
        return False  # ensure the timer only runs once

    def setval(self, mrk, key, val, ifunchanged=False, parm=None, mapin=True):
        super().setval(mrk, key, val, ifunchanged=ifunchanged, parm=parm, mapin=mapin)
        if mrk == self.marker:
            v = stylemap.get(dualmarkers.get(key, key))
            if v is None:
                return
            # self.loading = True
            self.set(v[0], val or "")
            if key == "Color":
                # print(f"setval {val=}")
                self.set("l_styColor", _("Color:")+"\n"+str(val))
            # self.loading = False

    def get(self, key, default=None):
        w = self.builder.get_object(key)
        if w is None:
            return None
        return getWidgetVal(key, w, default)

    def set(self, key, value, useMarkup=False):
        w = self.builder.get_object(key)
        if w is None:
            return
        try:
            setWidgetVal(key, w, value, useMarkup=useMarkup)
        except (TypeError, ValueError) as e:
            raise e.__class__("{} for widget {}".format(e, key))

    def load(self, sheetfiles):
        logger.debug(f"Loading stylesheets: {sheetfiles}")
        super().load(sheetfiles)
        results = {"Tables": {"th": {"thc": {}, "thr": {}}, "tc": {"tcc": {}, "tcr": {}}},
                   "Peripheral Materials": {"zpa-": {}},
                   "Identification": {"toc": {}}}
        foundp = False
        for k in sorted(self.allStyles(), key=lambda x:(len(x), x)):
            v = self.asStyle(k)
            if v.get('styletype', '') == 'Standalone' or v.get('mrktype', '') == "barems":
                continue
            if 'zderived' in v:
                self.setval(v['zderived'], ' endMilestone', k)
                continue
            if k not in self.basesheet:
                self.setval(k, ' deletable', True)
            if k == "p":
                foundp = True
            cat = 'Other'
            if 'name' in v:
                if not v['name']:
                    v['name'] = "{} - Other".format(k)
                m = name_reg.match(str(v['name']))
                if m:
                    if not m.group(1) and " " in m.group(2):
                        cat = m.group(2)
                    else:
                        cat = m.group(1) or m.group(3)
                else:
                    cat = str(v['name']).strip()
                cat, url = categorymapping.get(cat, (cat, None))
                self.setval(k, ' category', cat)
                self.setval(k, ' url', url)
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
            isdisabled = False
            if k in allStyles:
                n = self.getval(k, 'name') or "{} - Other".format(k)
                b = re.split(r"\s*-\s*", n)
                if not len(b):
                    pass
                elif b[0] != k or any(b[0].startswith(x) for x in ('OBSOLETE', 'DEPRECATED')):
                    n = "{} - {}".format(k, " - ".join(b[1:]))
                isdisabled = 'nonpublishable' in (x.lower() for x in self.getval(k, 'TextProperties', ""))
            elif k not in self.basesheet:
                ismarker = False
                n = k
            else:
                n = k
            s = [str(k), str(n), ismarker, isdisabled]
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
        it = self._searchMarker(self.treestore, root, marker)
        path = self.treestore.get_path(it)
        self.treeview.expand_to_path(path)
        self.treeview.get_selection().select_path(path)
        self.treeview.scroll_to_cell(path, None, False, 0, 0)

    def _searchMarker(self, model, it, marker, findall=False):
        while it is not None:
            if model[it][0] == marker or (findall and marker in model[it][1].lower()):
                return it
            if model.iter_has_child(it):
                childit = model.iter_children(it)
                ret = self._searchMarker(model, childit, marker, findall=findall)
                if ret is not None:
                    return ret
            it = model.iter_next(it)
        return None

    def normalizeSearchKey(self, key):
        return key.lstrip('\\').lower()

    def tree_search(self, model, colmn, key, rowiter):
        root = model.get_iter_first()
        norm_key = self.normalizeSearchKey(key)

        # Find first match (your existing behavior)
        it = self._searchMarker(model, root, norm_key)
        if it is None:
            it = self._searchMarker(model, root, norm_key, findall=True)
            if it is None:
                # No matches → clear highlights and return
                self._search_matches = set()
                self.treeview.queue_draw()
                return False

        # --- NEW: collect ALL matches for highlighting ---
        matches = set()

        def collect_all(start_it):
            it2 = start_it
            while it2 is not None:
                try:
                    label = str(model[it2][1]).lower()
                    marker = str(model[it2][0]).lower()
                except Exception:
                    label = str(model.get_value(it2, 1)).lower()
                    marker = str(model.get_value(it2, 0)).lower()

                if marker == norm_key or (norm_key and norm_key in label):
                    matches.add(model.get_path(it2).to_string())

                if model.iter_has_child(it2):
                    collect_all(model.iter_children(it2))
                it2 = model.iter_next(it2)

        collect_all(root)
        self._search_matches = matches
        # -------------------------------------------------

        # Collapse everything, then expand only top-level categories that match
        self.treeview.collapse_all()
        top = model.get_iter_first()
        while top is not None:
            top_matches = False

            try:
                label = str(model[top][1])
            except Exception:
                label = str(model.get_value(top, 1))

            if norm_key and label and norm_key in label.lower():
                top_matches = True
            else:
                if model.iter_has_child(top):
                    child = model.iter_children(top)
                    if self._searchMarker(model, child, norm_key, findall=True) is not None:
                        top_matches = True

            if top_matches:
                self.treeview.expand_row(model.get_path(top), False)

            top = model.iter_next(top)

        # Jump to the first match, as before
        path = model.get_path(it)
        if path is None:
            self.treeview.queue_draw()
            return False

        self.treeview.expand_to_path(path)
        self.treeview.scroll_to_cell(path)
        self.treeview.get_selection().select_path(path)

        # Force repaint so highlights show immediately
        self.treeview.queue_draw()
        return True

    def old_tree_search(self, model, colmn, key, rowiter):
        root = model.get_iter_first()
        norm_key = self.normalizeSearchKey(key)

        # 1) Find the first match (keeps your existing behavior)
        it = self._searchMarker(model, root, norm_key)
        if it is None:
            it = self._searchMarker(model, root, norm_key, findall=True)
            if it is None:
                return False

        # 2) Collapse everything, then expand only top-level categories that match
        self.treeview.collapse_all()

        top = model.get_iter_first()
        while top is not None:
            top_matches = False

            # Try to read the category label (column 1) safely
            try:
                label = str(model[top][1])
            except Exception:
                label = str(model.get_value(top, 1))

            # a) top-level row's own label matches?
            if norm_key and label and norm_key in label.lower():
                top_matches = True
            else:
                # b) OR any descendant matches?
                if model.iter_has_child(top):
                    child = model.iter_children(top)
                    if self._searchMarker(model, child, norm_key, findall=True) is not None:
                        top_matches = True

            if top_matches:
                self.treeview.expand_row(model.get_path(top), False)

            top = model.iter_next(top)

        # 3) Jump to the first match as before
        path = model.get_path(it)
        if path is None:
            return False
        self.treeview.expand_to_path(path)
        self.treeview.scroll_to_cell(path)
        self.treeview.get_selection().select_path(path)
        return True

    def add_filter(self, state, mrkrset):
        self.filter_state = state
        self.mrkrlist = mrkrset
        self.filter.refilter()

        if state:
            # Expand ALL top-level categories in the (filtered) model
            model = self.treeview.get_model()      # GtkTreeModelFilter
            it = model.get_iter_first()
            while it:
                path = model.get_path(it)
                if len(path) == 1:                 # top-level only
                    self.treeview.expand_row(path, False)
                it = model.iter_next(it)
        else:
            # Filter turned OFF → collapse everything (so top level is closed)
            self.treeview.collapse_all()

    def apply_filter(self, model, it, data):
        if not self.filter_state:
            return True
        path = model.get_path(it)
        res = model[it][0] in self.mrkrlist or len(path) == 1   # in the list or top level
        #logger.debug(f"{model[it][0]} {path}({len(path)})   {res}")
        return res

    # def old_getStyleType(self, mrk):
        # ''' valid returns are: Character, Milestone, Note, Paragraph '''
        # mtype = self.getval(self.marker, 'mrktype', '')
        # if not mtype:
            # res = self.getval(self.marker, 'StyleType')
        # else:
            # res = Grammar.marker_tags.get('mtype', 'Standalone')
        # return res

    def getStyleType(self, mrk):
        """valid returns are: Character, Milestone, Note, Paragraph"""
        # what the .sty says
        mtype = self.getval(mrk, 'mrktype', '')
        # what the USFM grammar says for this marker
        cat = Grammar.marker_categories.get(mrk, '')
        # If mrktype is empty OR the default placeholder "Paragraph",
        # use the grammar category when available.
        if not mtype or mtype == 'Paragraph':
            if cat:
                return cat
        # Otherwise honor the explicit mrktype
        if mtype:
            return mtype
        # Last fallbacks: any saved StyleType, or Standalone
        st = self.getval(mrk, 'StyleType')
        return st or 'Standalone'

    def editMarker(self):
        if self.marker is None:
            return
        if self.marker in aliases:
            self.marker += "1"
        oldisLoading = getattr(self, 'isLoading', False)
        # logger.debug(f"Start editing style {self.marker}, {oldisLoading}")
        self.isLoading = True
        data = self.sheet.get(self.marker, {})
        old = self.basesheet.get(self.marker, {})
        # logger.debug(f"styles({self.marker}) = {old} + {data}")
        oldval = None
        if 'linespacing' not in old and 'baseline' not in old:
            old['linespacing'] = "1"
            if 'linespacing' not in data and 'baseline' not in data:
                data['linespacing'] = "1"
        for k, v in stylemap.items():
            if k == 'Marker':
                val = "\\" + self.marker
                urlcat = data.get(' url', '')
                urlmkr = self.marker
                if data.get('endmarker', None):
                    val += " ... \\" + data['endmarker']
                    if urlmkr not in noEndmarker:
                        urlmkr += "-" + data['endmarker'].strip(r'\*')
                urlmkr = re.sub(r'\d', '', urlmkr)
            elif k == '_publishable':
                # val = 'nonpublishable' in data.get('TextProperties', '')
                oldval = 'nonpublishable' not in (x.lower() for x in old.get('textproperties', []))  # default was "nonpublishable"
                props = data.get('textproperties', None)
                if props is None:
                    val = oldval
                else:
                    if not isinstance(props, dict):
                        props = {k:v for v,k in enumerate(props.split())}
                    val = 'nonpublishable' not in (x.lower() for x in props)
                # oldval = 'nonpublishable' in old.get('TextProperties', '')
                logger.debug(f"{self.marker} is {'' if oldval else 'non'}publishable")
            elif k.startswith("_"):
                basekey = v[3](v[2])        # default data key e.g. "FontSize"
                obasekey = v[3](not v[2])   # non-default data key e.g. "FontScale"
                oldval = self.getval(self.marker, basekey, self.getval(self.marker, obasekey, baseonly=True), baseonly=True)
                val = self.getval(self.marker, basekey)
                olddat = v[2]
                controlk = v[3](False)
                # try each switch state
                for m, f in ((v[3](x), x) for x in (not v[2], v[2])):
                    if m.lower() in old:            # key in underlying?
                        olddat = f          # set the state and get the val
                        oldval = self.getval(self.marker, m)
                    if m.lower() in data:
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
                # logger.debug(f"{k}: {oldval=}, {val=}")
            self._setFieldVal(k, v, oldval, val)

        stype = self.getStyleType(self.marker)
        _showgrid = {'Para': (True, True, False), 'Char': (False, True, False), 'Note': (True, True, True), 'Stan': (False, False, False)}
        visibles = _showgrid.get(stype[:4] if stype is not None else "",(True, True, False))
        for i, w in enumerate(('Para', 'Char', 'Note')):
            self.builder.get_object("ex_sty"+w).set_expanded(visibles[i])

        self.builder.get_object("ex_styTable").set_expanded("tc" in self.marker)
        if "tc" in self.marker:
            self.builder.get_object("ex_styPara").set_expanded(True)
        sb = (self.marker.startswith("cat:") and self.marker.endswith("esb")) or self.marker == "textborder"
        self.builder.get_object("ex_stySB").set_expanded(sb)
        if sb:
            for w in ['Para', 'Table', 'Note']:
                self.builder.get_object("ex_sty"+w).set_expanded(False)
        self.builder.get_object("ex_styOther").set_expanded(False)
        for w in (('Note', 'Table', 'SB')):
            if self.builder.get_object("ex_sty"+w).get_expanded():
                self.builder.get_object("ex_styOther").set_expanded(True)
        if not self.model.get("c_noInternet"):
            tl = self.model.lang
            w = self.builder.get_object("l_url_usfm")
            w.set_sensitive(True)
            w.set_label(_('More Info...'))
            tl = self.model.lang if not self.model.get("c_useEngLinks") and \
                 self.model.lang in ['ar_SA', 'my', 'zh', 'fr', 'hi', 'hu', 'id', 'ko', 'pt', 'ro', 'ru', 'es', 'th'] else ""
            m = self.marker.strip("123456789")
            path = mkr2path.get(m, None)
            if "+" in urlmkr or "|" in urlmkr or path is None:
                w.set_uri(_('No further information is available for\ncomplex/custom marker: {}').format(urlmkr))
                w.set_sensitive(False)
            else:
                if m.startswith("z"):
                    site = f'https://github.com/sillsdev/ptx2pdf/blob/master/docs/help/{m}.md'
                    w.set_label(_('Complex style'))
                else:
                    site = f'https://docs.usfm.bible/usfm/latest/{path}/{m}.html'

                partA, partB = self.splitURL(site)
                partA = re.sub(r"\.", r"-", partA)
                
                if len(tl) and "/blob/" not in site:
                    site = "{}.translate.goog/{}?_x_tr_sl=en&_x_tr_tl={}&_x_tr_hl=en&_x_tr_pto=wapp&_x_tr_hist=true".format(partA, partB, tl)
                w.set_uri(f'{site}')
            
        # Sensitize font size, line spacing, etc. for \paragraphs
        for w in ["s_styFontSize", "s_styLineSpacing", "c_styAbsoluteLineSpacing"]:
            widget = self.builder.get_object(w)
            widget.set_sensitive(self.marker != "p")
        self.isLoading = oldisLoading

    def splitURL(self, url):
        # Find the index of the first '/' after the initial '//'
        index = url.find('/', url.find('//') + 2)

        if index != -1:
            partA = url[:index]
            partB = url[index + 1:].rstrip('/')
        else:
            partA = url
            partB = ''

        return partA, partB

    def setFontLabel(self, fref, fsize):
        bfontsize = float(self.model.get("s_fontsize"))
        f = fref.getTtfont() if fref is not None else None
        logger.debug(f"{fsize=}, {fref=}, {bfontsize=}")
        if f is not None:
            asc = f.ascent / f.upem * bfontsize
            des = f.descent / f.upem * bfontsize
            self.set("l_styFontFeats", '<span foreground="blue">{}{}\n{}{}</span>'.format("GR " if fref.isGraphite else "",
                                            "stretch={:.0f}%".format(float(fref.feats["extend"])*100) if "extend" in fref.feats else "",
                                            "<b>bold={:.1f}</b> ".format(float(fref.feats["embolden"])) if "embolden" in fref.feats else "",
                                            "<i>ital={:.2f}</i>".format(float(fref.feats["slant"])) if "slant" in fref.feats else ""),
                                                        useMarkup=True)
            self.set("l_styActualFontSize", '<span foreground="blue">{:.1f}pt\n(\u2191{:.1f} \u2193{:.1f})</span>'.format(fsize, 
                                            asc, -des), useMarkup=True)
        else:
            self.set("l_styFontFeats", '', useMarkup=True)
            self.set("l_styActualFontSize", '<span foreground="blue">{:.1f}pt</span>'.format(fsize), useMarkup=True)

    def _cmp(self, a, b):
        try:
            fa = float(a)
            fb = float(b)
            return fb == fa
        except (TypeError, ValueError):
            return a == b

    def _setFieldVal(self, k, v, oldval, val):
        logger.log(9, f"Set style field {k} to {val} from {oldval} in context {v}")
        w = self.builder.get_object(v[0])
        if w is None:
            print("Can't find widget {}".format(v[0]))
        else:
            if v[0].startswith("col_"):
                newval = textocol(val)
                if v[0] == "col_styColor":
                    self.set("l_styColor", _("Color:")+"\n"+str(val))
            elif k == 'font':
                newval = val
                fsize = float(self.getval(self.marker, "FontSize", "1."))
                msize = float(self.model.get("s_fontsize", "1."))
                logger.debug(f"{self.marker}: FontSize={fsize}, model font size={msize}, {val=}")
                self.setFontLabel(val, fsize * msize)
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
        logger.debug(f"Style edit {key} in {self.marker} -> {val}")
        if key == '_publishable':
            if val:
                add, rem = "", "non"
            else:
                add, rem = "non", ""
            props = set((self.sheet.setdefault(self.marker, {}).setdefault('TextProperties', "") or "").split())
            if props is None:
                props = set()
                # self.sheet[self.marker]['TextProperties'] = props
            try:
                props.remove(rem+'publishable')
            except KeyError:
                pass
            props.add(add+'publishable')
            self.sheet[self.marker]['TextProperties'] = " ".join(sorted(props))
            (model, selecti) = self.treeview.get_selection().get_selected()
            model.set_value(selecti, 3, not val)
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
            if oldval is not None:
                newval = self._convertabs(newkey, oldval)
                #newval = oldval
                logger.debug(f"{newkey}: {oldval=} -> {newval=} | {self.getval(self.marker, newkey)}")
                self.setval(self.marker, newkey, newval, mapin=False)
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
            super(self.__class__, self).setval(self.marker, key, value, mapin=False)
            if key in ("font", "FontSize", "FontName", "Bold", "Italic"): # ask MH if OK to add 'font'
                fref = self.getval(self.marker, 'font')
                if fref is None:
                    fref = self.model.get("bl_fontR")
                    if fref is not None:
                        fref = fref.copy()
                if fref is not None:
                    if key in ("Bold", "Italic"):
                        setattr(fref, "is"+key, val)
                        self.setval(self.marker, 'font', fref, parm=True, mapin=False)
                    # check that defaulting this doesn't cause problems
                    fsize = float(self.getval(self.marker, "FontSize", "1."))
                    msize = float(self.model.get("s_fontsize", "1."))
                    logger.debug(f"{self.marker}: FontSize={fsize}, model font size={msize}")
                    self.setFontLabel(fref, fsize * msize)
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

    def addMarker(self, mrk, name):
        super().addMarker(mrk, name)
        m = name_reg.match(name) if name is not None else None
        if m:
            if not m.group(1) and " " in m.group(2):
                cat = m.group(2)
            else:
                cat = m.group(1) or m.group(3)
        else:
            cat = "Other"
        cat, url = categorymapping.get(cat, (cat, None))
        self.sheet[mrk][' category'] = cat
        selecti = self.treestore.get_iter_first()
        while selecti:
            r = self.treestore[selecti]
            if r[0] == cat:
                selecti = self.treestore.append(selecti, [mrk, name, True, False])
                # logger.debug(f"Inside treestore: {self.treestore.get_string_from_iter(selecti)}")
                break
            selecti = self.treestore.iter_next(selecti)
        else:
            selecti = self.treestore.append(None, [cat, cat, False, False])
            selecti = self.treestore.append(selecti, [mrk, name, True, False])
            # logger.debug(f"one step {self.treestore.get_string_from_iter(selecti)}")
        return selecti

    def mkrDialog(self, newkey=False):
        dialog = self.builder.get_object("dlg_styModsdialog")
        sheet = self.asStyle(self.marker)
        mrktype(sheet, self.marker)
        for k, v in dialogKeys.items():
            if k == "mrktype":
                val = Grammar.marker_categories.get(self.marker, '')
            else:
                val = ""
            self.model.set(v, self.getval(self.marker, k, val) or "")
            # print(f"setting {self.marker}:{k} = {self.getval(self.marker, k, '')}")
        self.model.set(dialogKeys['Marker'], '' if newkey else self.marker)
        for a in ('Marker', 'mrktype'):
            wid = self.builder.get_object(dialogKeys[a])
            if wid is not None:
                wid.set_sensitive(newkey or (False if a == "Marker" else Grammar.marker_categories.get(self.marker, None) is None))
        tryme = True    # keep trying until necessary fields filled in
        while tryme:
            response = dialog.run()
            if response != Gtk.ResponseType.OK:
                break
            key = re.sub(r"\\", "|", re.sub(r"^\\", "", self.model.get(dialogKeys['Marker']).strip()))
            if key == "":
                break
            tryme = False
            (d, selecti) = self.treeview.get_selection().get_selected()
            name = self.model.get(dialogKeys['Name'], '')
            if key.lower() not in self.sheet:
                selecti = self.addMarker(key, name)
                for k, v in stylemap.items():
                    if not k.startswith("_"):
                        self.setval(key, k, self.getval(self.marker, k), mapin=False)
            else:
                self.treestore.set_value(selecti, 1, name)
            for k, v in dialogKeys.items():
                if k == 'Marker':
                    continue
                val = self.model.get(v).replace("\\","")
                # print(f"{k=} {v=} -> {val=}")
                if k != "mrktype" or Grammar.marker_categories.get(key, '') == '':
                    self.setval(key, k, val)
            st = self.getStyleType(key)
            if st == 'Character' or st == 'Note':
                self.setval(key, 'EndMarker', key + "*")
                self.resolveEndMarker(key, None)
            elif st == 'Milestone':
                self.resolveEndMarker(key, self.getval(key, 'EndMarker'))
                self.setval(key, 'EndMarker', None)
            self.set_legacy_types(key)
            self.marker = key
            self.treeview.get_selection().select_iter(selecti)
            self.selectMarker(key)
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

    def sidebarImageDialog(self, isbg=False):
        sb = imageStyleFromStyle(self, self.marker, isbg)
        if sb is None:
            sb = ImageStyle(isbg)
        res = sb.run(self.model)
        # print(f"{res=}")
        if res and sb.filename != "":
            sb.toStyle(self, self.marker)
        elif res:
            sb.removeStyle(self, self.marker)

    def sidebarBorderDialog(self):
        self.sb = borderStyleFromStyle(self, self.marker)
        if self.sb is None:
            self.sb = BorderStyle()
        res = self.sb.run(self.model)
        if res:
            self.sb.toStyle(self, self.marker)
        self.sb = None

    def onSBborderSettingsChanged(self):
        self.sb.onSBborderSettingsChanged()
        
    def boxPaddingUniformClicked(self):
        self.sb.boxPaddingUniformClicked()
        
    def bdrPaddingUniformClicked(self):
        self.sb.bdrPaddingUniformClicked()

    def delKey(self, key=None):
        if key is None:
            key = self.marker
        if self.sheet.get(key, {}).get(" deletable", False):
            del self.sheet[key]
            selection = self.treeview.get_selection()
            model, i = selection.get_selected()
            if isinstance(model, Gtk.TreeModelFilter):
                i = model.convert_iter_to_child_iter(i)
                model = model.get_model()
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
        if k in self.stylediverts:
            newk = self.stylediverts[k][0]
            old = self.basesheet.get(self.marker, {})
            newval = old.get(" "+newk, None)
            if newval is not None:
                self._setFieldVal(k, stylemap[newk], newval, newval)
        oldval = self.getval(self.marker, k, v[2], baseonly=True)
        self._setFieldVal(k, v, oldval, oldval)

