#!/usr/bin/python3

import sys, os, re, regex, gi, subprocess, traceback
gi.require_version('Gtk', '3.0')
from shutil import copyfile, copytree, rmtree
import time
from gi.repository import Gdk, Gtk, Pango, GObject, GLib, GdkPixbuf

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    sys.stdout = open(os.devnull, "w")
    # sys.stdout = open("D:\Temp\ptxprint-sysout.tmp", "w")
    sys.stderr = sys.stdout
else:
    gi.require_version('GtkSource', '3.0')
from gi.repository import GtkSource

import xml.etree.ElementTree as et
from ptxprint.font import TTFont, initFontCache, fccache
from ptxprint.view import ViewModel, Path
from ptxprint.gtkutils import getWidgetVal, setWidgetVal, setFontButton
from ptxprint.utils import APP
from ptxprint.runner import StreamTextBuffer
from ptxprint.ptsettings import ParatextSettings, allbooks, books, bookcodes, chaps
from ptxprint.piclist import PicList, PicChecks, PicInfoUpdateProject
from ptxprint.styleditor import StyleEditor
from ptxprint.runjob import isLocked, unlockme
from ptxprint.texmodel import TexModel
from ptxprint.minidialog import MiniDialog
import ptxprint.scriptsnippets as scriptsnippets
from ptxprint.utils import _, f_
import configparser
from threading import Thread

pdfre = re.compile(r".+[\\/](.+)\.pdf")

# xmlstarlet sel -t -m '//iso_15924_entry' -o '"' -v '@alpha_4_code' -o '" : "' -v '@name' -o '",' -n /usr/share/xml/iso-codes/iso_15924.xml
_allscripts = { "Zyyy" : "Default", "Adlm" : "Adlam", "Afak" : "Afaka", "Aghb" : "Caucasian Albanian", "Ahom" : "Ahom, Tai Ahom", 
    "Arab" : "Arabic", "Aran" : "Arabic (Nastaliq)", "Armi" : "Imperial Aramaic", "Armn" : "Armenian", "Avst" : "Avestan", "Bali" : "Balinese",
    "Bamu" : "Bamum", "Bass" : "Bassa Vah", "Batk" : "Batak", "Beng" : "Bengali", "Bhks" : "Bhaiksuki", "Blis" : "Blissymbols", "Bopo" : "Bopomofo",
    "Brah" : "Brahmi", "Brai" : "Braille", "Bugi" : "Buginese", "Buhd" : "Buhid", "Cakm" : "Chakma", "Cans" : "Canadian Aboriginal Syllabics",
    "Cari" : "Carian", "Cham" : "Cham", "Cher" : "Cherokee", "Cirt" : "Cirth", "Copt" : "Coptic", "Cprt" : "Cypriot", "Cyrl" : "Cyrillic",
    "Cyrs" : "Cyrillic (Old Church Slavonic)", "Deva" : "Devanagari", "Dsrt" : "Deseret (Mormon)", "Egyd" : "Egyptian demotic", 
    "Egyh" : "Egyptian hieratic", "Elba" : "Elbasan", "Ethi" : "Ethiopic (Geʻez)", "Geok" : "Khutsuri (Asomtavruli & Nuskhuri)", 
    "Geor" : "Georgian (Mkhedruli)", "Glag" : "Glagolitic", "Gong" : "Gunjala-Gondi", "Gonm" : "Masaram-Gondi",
    "Goth" : "Gothic", "Gran" : "Grantha", "Grek" : "Greek", "Gujr" : "Gujarati", "Guru" : "Gurmukhi",
    "Hanb" : "Han with Bopomofo", "Hang" : "Hangul (Hangŭl, Hangeul)", "Hani" : "Han (Hanzi, Kanji, Hanja)",
    "Hano" : "Hanunoo (Hanunóo)", "Hans" : "Han (Simplified)", "Hant" : "Han (Traditional)", "Hatr" : "Hatran", "Hebr" : "Hebrew",
    "Hira" : "Hiragana", "Hmng" : "Pahawh-Hmong", "Hrkt" : "Japanese (Hiragana+Katakana)", "Hung" : "Old Hungarian (Runic)",
    "Ital" : "Old Italic (Etruscan, Oscan)", "Jamo" : "Jamo (subset of Hangul)", "Java" : "Javanese",
    "Jpan" : "Japanese (Han+Hiragana+Katakana)", "Jurc" : "Jurchen", "Kali" : "Kayah-Li", "Kana" : "Katakana", "Khar" : "Kharoshthi",
    "Khmr" : "Khmer", "Khoj" : "Khojki", "Kitl" : "Khitan (large)", "Kits" : "Khitan (small)", "Knda" : "Kannada", "Kore" : "Korean (Hangul+Han)",
    "Kpel" : "Kpelle", "Kthi" : "Kaithi", "Lana" : "Tai Tham (Lanna)", "Laoo" : "Lao", "Latf" : "Latin (Fraktur)",
    "Latg" : "Latin (Gaelic)", "Latn" : "Latin", "Leke" : "Leke", "Lepc" : "Lepcha (Róng)", "Limb" : "Limbu", "Lina" : "Linear A",
    "Linb" : "Linear B", "Lisu" : "Lisu (Fraser)", "Loma" : "Loma", "Lyci" : "Lycian", "Lydi" : "Lydian", "Mahj" : "Mahajani", 
    "Mand" : "Mandaic, Mandaean", "Mani" : "Manichaean", "Marc" : "Marchen", "Mend" : "Mende Kikakui", "Merc" : "Meroitic Cursive",
    "Mlym" : "Malayalam", "Modi" : "Modi", "Mong" : "Mongolian", "Mroo" : "Mro, Mru", "Mtei" : "Meitei-Mayek", "Mult" : "Multani", 
    "Mymr" : "Myanmar (Burmese)", "Narb" : "North Arabian (Ancient)", "Nbat" : "Nabataean", "Newa" : "New (Newar, Newari)",
    "Nkgb" : "Nakhi Geba (Naxi Geba)", "Nkoo" : "N’Ko", "Nshu" : "Nüshu", "Ogam" : "Ogham", "Olck" : "Ol Chiki (Ol Cemet’, Santali)", 
    "Orkh" : "Old Turkic, Orkhon Runic", "Orya" : "Oriya", "Osge" : "Osage", "Osma" : "Osmanya", "Palm" : "Palmyrene",
    "Pauc" : "Pau Cin Hau", "Perm" : "Old Permic", "Phag" : "Phags-pa", "Phli" : "Inscriptional Pahlavi", "Phlp" : "Psalter Pahlavi",
    "Phlv" : "Book Pahlavi", "Phnx" : "Phoenician", "Plrd" : "Miao (Pollard)", "Prti" : "Inscriptional Parthian",
    "Rjng" : "Rejang (Redjang, Kaganga)", "Roro" : "Rongorongo",
    "Runr" : "Runic", "Samr" : "Samaritan", "Sara" : "Sarati", "Sarb" : "Old South Arabian", "Saur" : "Saurashtra", "Shaw" : "Shavian (Shaw)", 
    "Shrd" : "Sharada", "Sidd" : "Siddham, Siddhamātṛkā", "Sind" : "Sindhi, Khudawadi", "Sinh" : "Sinhala", "Sora" : "Sora-Sompeng",
    "Sund" : "Sundanese", "Sylo" : "Syloti Nagri", "Syrc" : "Syriac", "Syre" : "Syriac (Estrangelo)", "Syrj" : "Syriac (Western)",
    "Syrn" : "Syriac (Eastern)", "Tagb" : "Tagbanwa", "Takr" : "Takri, Ṭāṅkrī", "Tale" : "Tai Le", "Talu" : "New-Tai-Lue", 
    "Taml" : "Tamil", "Tang" : "Tangut", "Tavt" : "Tai Viet", "Telu" : "Telugu", "Teng" : "Tengwar", "Tfng" : "Tifinagh (Berber)",
    "Tglg" : "Tagalog (Baybayin, Alibata)", "Thaa" : "Thaana", "Thai" : "Thai", "Tibt" : "Tibetan", "Tirh" : "Tirhuta", "Ugar" : "Ugaritic",
    "Vaii" : "Vai", "Wara" : "Warang-Citi", "Wole" : "Woleai", "Xpeo" : "Old Persian", "Yiii" : "Yi", "Zzzz" : "Uncoded script"
}
# Note that ls_digits (in the glade file) is used to map these "friendly names" to the "mapping table names" (especially the non-standard ones)
_alldigits = [ "Default", "Adlam", "Ahom", "Arabic-Indic", "Balinese", "Bengali", "Bhaiksuki", "Brahmi",
    "Chakma", "Cham", "Devanagari", "Ethiopic", "Extended-Arabic", "Gujarati", "Gunjala-Gondi", "Gurmukhi", "Hanifi-Rohingya", "Javanese", "Kannada", 
    "Kayah-Li", "Khmer", "Khudawadi", "Lao", "Lepcha", "Limbu", "Malayalam", "Masaram-Gondi", "Meetei-Mayek", "Modi", "Mongolian", 
    "Mro", "Myanmar", "Myanmar-Shan", "Myanmar-Tai-Laing", "New-Tai-Lue", "Newa", "Nko", "Nyiakeng-Puachue-Hmong", "Ol-Chiki", "Oriya", 
    "Osmanya", "Pahawh-Hmong", "Persian", "Rumi", "Saurashtra", "Sharada", "Sinhala-Lith", "Sora-Sompeng", "Sundanese", "Tai-Tham-Hora", 
    "Tai-Tham-Tham", "Takri", "Tamil", "Telugu", "Thai", "Tibetan", "Tirhuta", "Vai", "Wancho", "Warang-Citi" ]

_allbooks = ["FRT", "INT", 
            "GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT", "1SA", "2SA", "1KI", "2KI", "1CH", "2CH", "EZR", "NEH", "EST",
            "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER", "LAM", "EZK", "DAN", "HOS", "JOL", "AMO", "OBA", "JON", "MIC", "NAM",
            "HAB", "ZEP", "HAG", "ZEC", "MAL", 
            "TOB", "JDT", "ESG", "WIS", "SIR", "BAR", "LJE", "S3Y", "SUS", "BEL", 
            "1MA", "2MA", "3MA", "4MA", "1ES", "2ES", "MAN", "PS2", "DAG", "LAO",
            "MAT", "MRK", "LUK", "JHN", "ACT", "ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI", "TIT",
            "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV", 
            "XXA", "XXB", "XXC", "XXD", "XXE", "XXF", "XXG",
            "GLO", "TDX", "NDX", "CNC", "OTH", "BAK"]
_allbkmap = {k: i for i, k in enumerate(_allbooks)} 

# The 3 dicts below are used by method: sensiVisible() to toggle object states

# Checkboxes and the different objects they make (in)sensitive when toggled
# Order is important, as the 1st object can be told to "grab_focus"
_sensitivities = {
    "r_book": {
        "r_book_single":       ["ecb_book", "l_chapfrom", "fcb_chapfrom", "l_chapto", "fcb_chapto"],
        "r_book_multiple":     ["btn_chooseBooks", "t_booklist", "c_combine", "c_autoToC"],
        "r_book_module":       ["btn_chooseBibleModule", "lb_bibleModule"]},
        # "r_book_dbl":          ["btn_chooseDBLbundle", "l_dblBundle"]},
    "c_mainBodyText" :         ["gr_mainBodyText"],
    "c_doublecolumn" :         ["gr_doubleColumn", "c_singleColLayout", "t_singleColBookList"],
    "c_useFallbackFont" :      ["btn_findMissingChars", "t_missingChars", "l_fallbackFont", "bl_fontExtraR"],
    "c_includeFootnotes" :     ["bx_fnOptions"],
    "c_includeXrefs" :         ["bx_xrOptions"],
    "c_includeillustrations" : ["gr_IllustrationOptions", "c_includeImageCopyrights"],
    "c_diglot" :               ["gr_diglot", "fcb_diglotPicListSources", "c_hdrLeftPri", "c_hdrCenterPri", "c_hdrRightPri",
                                "c_ftrCenterPri", "c_hdrLeftSec", "c_hdrCenterSec", "c_hdrRightSec", "c_ftrCenterSec"],
    "c_borders" :              ["gr_borders"],

    "c_pagegutter" :           ["s_pagegutter"],
    "c_variableLineSpacing" :  ["s_linespacingmin", "s_linespacingmax", "l_min", "l_max"],
    "c_verticalrule" :         ["l_colgutteroffset", "s_colgutteroffset"],
    "c_rhrule" :               ["s_rhruleposition", "gr_horizRule"],
    "c_introOutline" :         ["c_prettyIntroOutline"],
    "c_sectionHeads" :         ["c_parallelRefs"],
    "c_useChapterLabel" :      ["t_clBookList", "l_clHeading", "t_clHeading", "c_optimizePoetryLayout"],
    "c_singleColLayout" :      ["t_singleColBookList"],
    "c_autoToC" :              ["t_tocTitle", "gr_toc", "l_toc"],
    "c_marginalverses" :       ["s_columnShift"],
    "c_hdrverses" :            ["c_sepPeriod", "c_sepColon"],
    "c_fnautocallers" :        ["t_fncallers", "btn_resetFNcallers"],
    "c_xrautocallers" :        ["t_xrcallers", "btn_resetXRcallers"],
    "c_glossaryFootnotes" :    ["c_firstOccurenceOnly"],
    # "c_usePicList" :           ["btn_editPicList"],
    "c_useCustomFolder" :      ["btn_selectFigureFolder", "c_exclusiveFiguresFolder", "lb_selectFigureFolder"],
    "c_processScript" :        ["c_processScriptBefore", "c_processScriptAfter", "btn_selectScript", "btn_editScript"],
    "c_usePrintDraftChanges" : ["btn_editChangesFile"],
    "c_useModsTex" :           ["btn_editModsTeX"],
    "c_useCustomSty" :         ["btn_editCustomSty"],
    "c_useModsSty" :           ["btn_editModsSty"],
    "c_inclFrontMatter" :      ["btn_selectFrontPDFs"],
    "c_inclBackMatter" :       ["btn_selectBackPDFs"],
    "c_applyWatermark" :       ["btn_selectWatermarkPDF"],
    "c_linebreakon" :          ["t_linebreaklocale"],
    "c_spacing" :              ["l_minSpace", "s_minSpace", "l_maxSpace", "s_maxSpace"],
    "c_inclPageBorder" :       ["btn_selectPageBorderPDF"],
    "c_inclSectionHeader" :    ["btn_selectSectionHeaderPDF"],
    "c_inclEndOfBook" :        ["btn_selectEndOfBookPDF"],
    "c_inclVerseDecorator" :   ["btn_selectVerseDecorator"],
    "c_fakebold" :             ["s_boldembolden", "s_boldslant"],
    "c_fakeitalic" :           ["s_italicembolden", "s_italicslant"],
    "c_fakebolditalic" :       ["s_bolditalicembolden", "s_bolditalicslant"],
    "c_thumbtabs":             ["gr_thumbs"],
    "c_thumbrotate":           ["fcb_rotateTabs"],
    "c_colophon":              ["gr_colophon"],
}
# Checkboxes and the different objects they make (in)sensitive when toggled
# These function OPPOSITE to the ones above (they turn OFF/insensitive when the c_box is active)
_nonsensitivities = {
    "c_omitrhchapnum" :        ["c_hdrverses"],
    "c_blendfnxr" :            ["l_internote", "s_internote"],
    # "c_usePicList" :           ["c_figexclwebapp"],
    "c_useprintdraftfolder" :  ["btn_selectOutputFolder"],
    "c_styTextProperties":     ["fr_styParaSettings", "fr_styCharSettings", "fr_styNoteSettings"],
}
# Checkboxes and the Tabs that they make (in)visible
# _visibilities = {
    # "c_showLayoutTab" :        ["tb_Layout"],
    # "c_showFontTab" :          ["tb_Font"],
    # "c_showBodyTab" :          ["tb_Body"],
    # "c_showHeadFootTab" :      ["tb_HeadFoot"],
    # "c_showPicturesTab" :      ["tb_Pictures"],
    # "c_showAdvancedTab" :      ["tb_Advanced"],
    # "c_showDiglotBorderTab" :  ["tb_DiglotBorder"],
    # "c_showViewerTab" :        ["tb_ViewerEditor"]
# }
_object_classes = {
    "printbutton": ("b_print", "b_frefresh"),
    "fontbutton":  ("bl_fontR", "bl_fontB", "bl_fontI", "bl_fontBI"),
    "mainnb":      ("nbk_Main", ),
    "viewernb":    ("nbk_Viewer", "nbk_PicList"),
    "thumbtabs":   ("l_thumbVerticalL", "l_thumbVerticalR", "l_thumbHorizontalL", "l_thumbHorizontalR"),
    "stybutton":   ("btn_resetCopyright", "btn_resetColophon", "btn_resetFNcallers", "btn_resetXRcallers", 
                    "btn_styAdd", "btn_styEdit", "btn_styDel", "btn_styReset")
}

    # "Center": "c", 
_pgpos = {
    "Top": "t", 
    "Bottom": "b", 
    "Before Verse": "h",
    "After Paragraph": "p",
    "Cutout": "c"
}

_horiz = {
    "Left":     "l", 
    "Center":   "c", 
    "Right":    "r",
    "Inner":    "i",
    "Outer":    "o",
    "-":        "-"
}

_defaultColophon = r"""\pc \zCopyright
\pc \zLicense
\pc \zImageCopyrights
"""

_notebooks = ("Main", "Viewer", "PicList")

# Vertical Thumb Tab Orientation options L+R
_vertical_thumb = {
    "1" : (270,  90),
    "2" : (90,  270),
    "3" : (90,   90),
    "4" : (270, 270),
}

_signals = {
    'clicked': ("Button",),
    'changed': ("ComboBox", "Entry"),
    'color-set': ("ColorButton",),
    'change-current-page': ("Notebook",),
    #'change-value': ("SpinButton",),
    'value-changed': ("SpinButton",),
    'state-set': ("Switch",),
    'row-activated': ("TreeView",),
}

_styleLinks = {
    "updateFnFontSize": (("f", "FontSize"),),
    "updateFnLineSpacing": (("f", "Baseline"), ("f", "LineSpacing")),
}

class GtkViewModel(ViewModel):

    def __init__(self, settings_dir, workingdir, userconfig, scriptsdir, args=None):
        self._setup_css()
        GLib.set_prgname("ptxprint")
        self.builder = Gtk.Builder()
        gladefile = os.path.join(os.path.dirname(__file__), "ptxprint.glade")
        if sys.platform.startswith("win"):
            tree = et.parse(gladefile)
            for node in tree.iter():
                if 'translatable' in node.attrib:
                    node.text = _(node.text)
                    del node.attrib['translatable']
                if node.get('name') in ('pixbuf', 'icon', 'logo'):
                    node.text = os.path.join(os.path.dirname(__file__), node.text)
            xml_text = et.tostring(tree.getroot(), encoding='unicode', method='xml')
            self.builder = Gtk.Builder.new_from_string(xml_text, -1)
        else:
            self.builder.set_translation_domain(APP)
            self.builder.add_from_file(os.path.join(os.path.dirname(__file__), "ptxprint.glade"))
        self.builder.connect_signals(self)
        super(GtkViewModel, self).__init__(settings_dir, workingdir, userconfig, scriptsdir, args)
        self.isDisplay = True
        self.config_dir = None
        self.initialised = False
        self.configNoUpdate = False
        self.chapNoUpdate = False
        self.bookNoUpdate = False
        self.pendingPid = None
        self.pendingConfig = None
        self.otherDiglot = None
        self.notebooks = {}
        self.pendingerror = None
        self.logfile = None
        for n in _notebooks:
            nbk = self.builder.get_object("nbk_"+n)
            self.notebooks[n] = [Gtk.Buildable.get_name(nbk.get_nth_page(i)) for i in range(nbk.get_n_pages())]
        for fcb in ("digits", "script", "chapfrom", "chapto", "diglotPicListSources",
                    "textDirection", "glossaryMarkupStyle", "fontFaces",
                    "styTextType", "styStyleType", "styCallerStyle", "styNoteCallerStyle", "NoteBlendInto",
                    "picaccept", "pubusage", "pubaccept", "chklstFilter"): #, "rotateTabs"):
            self.addCR("fcb_"+fcb, 0)
        self.cb_savedConfig = self.builder.get_object("ecb_savedConfig")
        self.ecb_diglotSecConfig = self.builder.get_object("ecb_diglotSecConfig")
        for k, v in _object_classes.items():
            for a in v:
                w = self.builder.get_object(a)
                if w is None:
                    print("Can't find {}".format(a))
                else:
                    w.get_style_context().add_class(k)

        scripts = self.builder.get_object("ls_scripts")
        scripts.clear()
        for k, v in _allscripts.items():
            scripts.append([v, k])
        self.set('fcb_script', 'Zyyy') # i.e. Set it to "Default"

        digits = self.builder.get_object("ls_digits")
        currdigits = {r[0]: r[1] for r in digits}
        digits.clear()
        for d in _alldigits: # .items():
            v = currdigits.get(d, d.lower())
            digits.append([d, v])
        self.fcb_digits.set_active_id(_alldigits[0])

        for d in ("dlg_multiBookSelector", "dlg_fontChooser", "dlg_password",
                  "dlg_generate", "dlg_styModsdialog"):
            dialog = self.builder.get_object(d)
            dialog.add_buttons(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.fileViews = []
        self.buf = []
        self.cursors = []
        for i,k in enumerate(["FrontMatter", "AdjList", "FinalSFM", "TeXfile", "XeTeXlog", "Settings"]):
            self.buf.append(GtkSource.Buffer())
            self.cursors.append((0,0))
            view = GtkSource.View.new_with_buffer(self.buf[i])
            scroll = self.builder.get_object("scroll_" + k)
            scroll.add(view)
            self.fileViews.append((self.buf[i], view))
            if i > 2:
                view.set_show_line_numbers(True)  # Turn these ON
            else:
                view.set_show_line_numbers(False)  # Turn these OFF
            view.pageid = "scroll_"+k
            view.connect("focus-out-event", self.onViewerLostFocus)
            view.connect("focus-in-event", self.onViewerFocus)

        if self.get("c_colophon") and self.get("tb_colophon") == "":
            self.set("tb_colophon", _defaultColophon)

        self.picListView = PicList(self.builder.get_object('tv_picListEdit'),
                                   self.builder.get_object('tv_picListEdit1'), self.builder, self)
        self.picChecksView = PicChecks(self)
        self.styleEditorView = StyleEditor(self)
        for k, v in _styleLinks.items():
            for a in v:
                self.styleEditorView.registerFn(a[0], a[1], getattr(self, k))

        self.logbuffer = StreamTextBuffer()
        self.builder.get_object("tv_logging").set_buffer(self.logbuffer)
        self.mw = self.builder.get_object("ptxprint")
        self.experimental = None

        projects = self.builder.get_object("ls_projects")
        digprojects = self.builder.get_object("ls_digprojects")
        projects.clear()
        digprojects.clear()
        allprojects = []
        for d in os.listdir(self.settings_dir):
            p = os.path.join(self.settings_dir, d)
            if not os.path.isdir(p):
                continue
            if os.path.exists(os.path.join(p, 'Settings.xml')) \
                    or any(x.lower().endswith("sfm") for x in os.listdir(p)):
                allprojects.append(d)
        for p in sorted(allprojects, key = lambda s: s.casefold()):
            projects.append([p])
            digprojects.append([p])
        wide = int(len(allprojects)/16)+1
        self.builder.get_object("fcb_project").set_wrap_width(wide)
        self.builder.get_object("fcb_diglotSecProject").set_wrap_width(wide)

    def _setup_css(self):
        css = """
            .printbutton:active { background-color: chartreuse; background-image: None }
            .fontbutton {font-size: smaller}
            .stybutton {font-size: 12px; padding: 4px 6px}
            progress, trough {min-height: 24px}
            .mainnb {background-color: #F0F0F0}
            .mainnb tab {min-height: 0pt; margin: 0pt; padding-bottom: 12pt}
            .viewernb {background-color: #F0F0F0}
            .viewernb tab {min-height: 0pt; margin: 0pt; padding-bottom: 3pt}
            .smradio {font-size: 11px; padding: 1px 1px}
            .changed { font-weight: bold} """
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode("utf-8"))
        Gtk.StyleContext().add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def run(self, callback):
        self.callback = callback
        fc = initFontCache()
        lsfonts = self.builder.get_object("ls_font")

        olst = ["b_print", "fr_SavedConfigSettings", "tb_Font", "tb_Layout", "tb_Body", "tb_HeadFoot", "tb_Pictures",
                "tb_Advanced", "tb_Logging", "tb_ViewerEditor", "tb_DiglotBorder"]
        self.initialised = True
        for o in olst:
            self.builder.get_object(o).set_sensitive(False)
        if self.pendingPid is not None:
            self.set("fcb_project", self.pendingPid)
            self.pendingPid = None
        if self.pendingConfig is not None:
            self.set("ecb_savedConfig", self.pendingConfig)
            self.pendingConfig = None
        fc.fill_liststore(lsfonts)
        tv = self.builder.get_object("tv_fontFamily")
        cr = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn("Family", cr, text=0, weight=1)
        tv.append_column(col)
        ts = self.builder.get_object("t_fontSearch")
        tv.set_search_entry(ts)
        self.mw.resize(830, 594)
        self.mw.show_all()
        GObject.timeout_add(1000, self.monitor)
        if self.args is not None and self.args.capture is not None:
            self.logfile = open(self.args.capture, "w")
            self.logfile.write("<?xml version='1.0'?>\n<actions>\n")
            self.starttime = time.time()
            for k, v in _signals.items():
                for w in v:
                    GObject.add_emission_hook(getattr(Gtk, w), k, self.emission_hook, k)
            self.logactive = True
        expert = self.userconfig.getboolean('init', 'expert', fallback=False)
        self.set("c_hideAdvancedSettings", expert)
        self.onHideAdvancedSettingsClicked(None, None)
        try:
            Gtk.main()
        except Exception as e:
            s = traceback.format_exc()
            s += "\n" + str(e)
            self.doError(s)

    def emission_hook(self, w, *a):
        if not self.logactive:
            return True
        name = Gtk.Buildable.get_name(w)
        self.logfile.write('    <event w="{}" s="{}" t="{}"/>\n'.format(name, a[0],
                            time.time()-self.starttime))
        return True

    def pause_logging(self):
        self.logactive = False

    def unpause_logging(self):
        self.logactive = True

    def monitor(self):
        if self.pendingerror is not None:
            self._doError(*self.pendingerror)
            self.pendingerror = None
        return True

    def onMainConfigure(self, w, ev, *a):
        if self.picListView is not None:
            self.picListView.onResized()

    def onHideAdvancedSettingsClicked(self, c_hideAdvancedSettings, foo):
        val = self.get("c_hideAdvancedSettings")
        self.userconfig.set('init', 'expert', 'true' if val else 'false')
        if not val:
            for c in ("c_startOnHalfPage", "c_marginalverses", "c_figplaceholders"):
                self.builder.get_object(c).set_active(False)

            # Turn Essential Settings ON
            for c in ("c_mainBodyText", "c_skipmissingimages"):
                self.builder.get_object(c).set_active(True)
            self.builder.get_object("c_hideAdvancedSettings").set_opacity(0.5)
            self.builder.get_object("c_hideAdvancedSettings").set_tooltip_text( \
                _("Show Advanced Settings:\n\n" + \
                "There are many more complex options\n" + \
                "available for use within PTXprint."))
        else:
            self.builder.get_object("c_hideAdvancedSettings").set_opacity(1.0)
            self.builder.get_object("c_hideAdvancedSettings").set_tooltip_text( \
                _("Hide Advanced Settings:\n\n" + \
                "If the number of options is too overwhelming then use\n" + \
                "this switch to hide the more complex/advanced options."))
                      
        for c in ("tb_Font", "tb_Advanced", "tb_ViewerEditor", "tb_Tabs", "tb_DiglotBorder", "tb_StyleEdtor",
                  "fr_copyrightLicense", "r_book_module", "btn_chooseBibleModule", "lb_bibleModule", # "tb_Pictures",
                  "c_fighiderefs", "lb_selectFigureFolder", # "r_book_dbl", "btn_chooseDBLbundle", "l_dblBundle", 
                  "l_missingPictureString", "l_imageTypeOrder", "t_imageTypeOrder", "fr_layoutSpecialBooks", "fr_layoutOther",
                  "s_colgutteroffset", "fr_Footer", "bx_TopMarginSettings", "gr_HeaderAdvOptions", "l_colgutteroffset",
                  "c_fighiderefs", "c_skipmissingimages", "c_useCustomFolder", "btn_selectFigureFolder", "c_exclusiveFiguresFolder",
                  "c_startOnHalfPage", "c_prettyIntroOutline", "c_marginalverses", "s_columnShift", "c_figplaceholders",
                  "fr_FontConfig", "fr_fallbackFont", "fr_paragraphAdjust", "l_textDirection", "l_colgutteroffset", "fr_hyphenation",
                  "bx_fnCallers", "bx_fnCalleeCaller", "bx_xrCallers", "bx_xrCalleeCaller", "c_fnOverride", "c_xrOverride",
                  "row_ToC", "c_hyphenate", "l_missingPictureCount", "bx_colophon", "tb_StyleEdtor", 
                  "c_hdrLeftPri", "c_hdrLeftSec", "c_hdrCenterPri", "c_hdrCenterSec", "c_hdrRightPri", "c_hdrRightSec", 
                  "c_omitverseone", "c_glueredupwords", "c_firstParaIndent", "c_hangpoetry", "c_preventwidows", 
                  "l_sidemarginfactor", "s_sidemarginfactor", "l_min", "s_linespacingmin", "l_max", "s_linespacingmax",
                  "c_variableLineSpacing", "c_pagegutter", "s_pagegutter", "fcb_textDirection", "l_digits", "fcb_digits",
                  "t_invisiblePassword", "t_configNotes", "l_notes", "c_elipsizeMissingVerses", "fcb_glossaryMarkupStyle",
                  "gr_fnAdvOptions", "c_figexclwebapp", "bx_horizRule", "l_glossaryMarkupStyle"):
            self.builder.get_object(c).set_visible(val)

        # Hide the Details and Checklist tabs on the Pictures tab
        if not val:
            self.builder.get_object("scr_picListEdit").set_visible(val)
            self.builder.get_object("scr_picListEdit1").set_visible(val)
            for x in ("checklist", "details"): 
                self.builder.get_object("pn_{}".format(x)).set_visible(val)
        else: # Still haven't found a way to turn these tabs back on without a segfault! :-(
            pass
            
        # Show Hide specific Help items
        for pre in ("l_", "lb_"):
            for h in ("ptxprintdir", "prjdir", "settings_dir", "pdfViewer", "techFAQ", "reportBugs"): 
                self.builder.get_object("{}{}".format(pre, h)).set_visible(val)

        # Resize Main UI Window appropriately
        if not val:
            self.mw.resize(828, 292)
        else:
            self.mw.resize(830, 594)

    def ExperimentalFeatures(self, value):
        self.experimental = value
        if value:
                self.builder.get_object("c_experimental").set_visible(True)
                self.builder.get_object("c_experimental").set_active(True)
                self.builder.get_object("c_experimental").set_sensitive(False)
        else:
            for c in ("c_experimental", "c_experimental"):
                self.builder.get_object(c).set_active(False)
                self.builder.get_object(c).set_visible(False)
                self.builder.get_object(c).set_sensitive(False)
        for w in ("tb_", "lb_"):
            self.builder.get_object("{}Logging".format(w)).set_visible(value)

    def addCR(self, name, index):
        v = self.builder.get_object(name)
        setattr(self, name, v)
        c = Gtk.CellRendererText()
        v.pack_start(c, True)
        v.add_attribute(c, "text", index)

    def parse_fontname(self, font):
        m = re.match(r"^(.*?)(\d+(?:\.\d+)?)$", font)
        if m:
            return [m.group(1), int(m.group(2))]
        else:
            return [font, 0]

    def get(self, wid, default=None, sub=0, asstr=False, skipmissing=False):
        w = self.builder.get_object(wid)
        if w is None:
            if not skipmissing and not (wid.startswith("_") or wid.startswith("r_")):
                print(_("Can't get {} in the model").format(wid))
            return super().get(wid, default=default)
        if wid.startswith("r_"):
            bits = wid.split("_")[1:]
            if len(bits) > 1:
                return w.get_active()
            return super().get(wid, default=default)
        return getWidgetVal(wid, w, default=default, asstr=asstr, sub=sub)

    def set(self, wid, value, skipmissing=False):
        w = self.builder.get_object(wid)
        if w is None and not wid.startswith("r_"):
            if not skipmissing and not wid.startswith("_"):
                print(_("Can't set {} in the model").format(wid))
            super(GtkViewModel, self).set(wid, value)
            return
        if wid.startswith("r_"):
            bits = wid.split("_")[1:]
            if len(bits) > 1:
                if value:
                    value = bits[1]
                else:
                    return
            super().set("r_"+bits[0], value)
            wid = "r_" + "_".join([bits[0], value])
            w = self.builder.get_object(wid)
            if w is not None:
                w.set_active(True)
            return
        setWidgetVal(wid, w, value)

    def onDestroy(self, btn):
        if self.logfile != None:
            self.logfile.write("</actions>\n")
            self.logfile.close()
        Gtk.main_quit()

    def onKeyPress(self, dlg, event):
        if event.keyval == Gdk.KEY_Escape:
            # print("Esc pressed, ignoring")
            return True

    def doError(self, txt, secondary=None, title=None, threaded=True):
        if threaded:
            self.pendingerror=(txt, secondary, title)
        else:
            self._doError(txt, secondary, title)

    def _doError(self, text, secondary, title):
        dialog = Gtk.MessageDialog(parent=None, message_type=Gtk.MessageType.ERROR,
                 buttons=Gtk.ButtonsType.OK, text=text)
        if title is not None:
            dialog.set_title(title)
        else:
            dialog.set_title("PTXprint")
        if secondary is not None:
            dialog.format_secondary_text(secondary)
        if sys.platform == "win32":
            dialog.set_keep_above(True)
        dialog.run()
        if sys.platform == "win32":
            dialog.set_keep_above(False)
        dialog.destroy()

    def onOK(self, btn):
        if isLocked():
            return
        jobs = self.getBooks(files=True)
        if not len(jobs) or jobs[0] == '':
            return
        # If the viewer/editor is open on an Editable tab, then "autosave" contents
        if Gtk.Buildable.get_name(self.builder.get_object("nbk_Main").get_nth_page(self.get("nbk_Main"))) == "tb_ViewerEditor":
            pgnum = self.get("nbk_Viewer")
            if self.notebooks["Viewer"][pgnum] in ("scroll_Adjust", "scroll_FinalSFM", "scroll_Settings"):
                self.onSaveEdits(None)
        cfgname = self.configName()
        if cfgname is None:
            cfgname = ""
        else:
            cfgname = "-" + cfgname
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)
        pdfnames = self.baseTeXPDFnames()
        for basename in pdfnames:
            pdfname = os.path.join(self.working_dir, basename) + ".pdf"
            fileLocked = True
            while fileLocked:
                try:
                    with open(pdfname, "wb+") as outf:
                        outf.close()
                except PermissionError:
                    question = _("                   >>> PLEASE CLOSE the PDF <<<\
                     \n\n{}\n\n Or use a different PDF viewer which will \
                             \n allow updates even while the PDF is open. \
                             \n See 'Links' on Viewer tab for more details. \
                           \n\n                        Do you want to try again?").format(pdfname)
                    if self.msgQuestion(_("The old PDF file is open!"), question):
                        continue
                    else:
                        return
                fileLocked = False
        self.onSaveConfig(None)

        self._incrementProgress(val=0.)
        try:
            self.callback(self)
        except Exception as e:
            s = traceback.format_exc()
            s += "\n" + str(e)
            self.doError(s)
            unlockme()

    def onCancel(self, btn):
        self.onDestroy(btn)

    def onAboutClicked(self, btn_about):
        dialog = self.builder.get_object("dlg_about")
        dialog.set_keep_above(True)
        response = dialog.run()
        dialog.set_keep_above(False)
        dialog.hide()
            
    def onBookListChanged(self, t_booklist, foo): # called on "focus-out-event"
        bl = self.getBooks()
        self.set('t_booklist', " ".join(bl))
        self.updateExamineBook()
        self.updateDialogTitle()

    def onSaveConfig(self, btn, force=False):
        if self.prjid is None or (not force and self.configLocked()):
            return
        newconfigId = self.configName() # self.get("ecb_savedConfig")
        if newconfigId != self.configId:
            self._copyConfig(self.configId, newconfigId)
            self.configId = newconfigId
            self.updateSavedConfigList()
            self.set("lb_settings_dir", self.configPath(self.configName()))
            self.updateDialogTitle()
        self.writeConfig()
        self.savePics(force=force)
        self.saveStyles(force=force)

    def writeConfig(self, cfgname=None):
        if self.prjid is not None:
            self.picChecksView.writeCfg(os.path.join(self.settings_dir, self.prjid), self.configId)
        super().writeConfig(cfgname=cfgname)

    def onDeleteConfig(self, btn):
        cfg = self.get("t_savedConfig")
        delCfgPath = self.configPath(cfgname=cfg)
        if cfg == 'Default':
            self.doError(_("Can't delete 'Default' configuration!"), secondary=_("Folder: ") + delCfgPath)
            return
        else:
            if not os.path.exists(os.path.join(delCfgPath, "ptxprint.cfg")):
                self.doError(_("Internal error occurred, trying to delete a directory tree"), secondary=_("Folder: ")+delCfgPath)
                return
            try: # Delete the entire folder
                rmtree(delCfgPath)
            except OSError:
                self.doError(_("Can't delete that configuration from disk"), secondary=_("Folder: ") + delCfgPath)
            self.updateSavedConfigList()
            self.set("t_savedConfig", "Default")
            self.loadConfig("Default")
            self.updateDialogTitle()

    def updateBookList(self):
        self.bookNoUpdate = True
        cbbook = self.builder.get_object("ecb_book")
        cbbook.set_model(None)
        lsbooks = self.builder.get_object("ls_books")
        lsbooks.clear()
        if self.ptsettings is not None:
            bp = self.ptsettings['BooksPresent']
            for b in allbooks:
                ind = books.get(b, 0)-1
                if 0 <= ind <= len(bp) and bp[ind - 1 if ind > 39 else ind] == "1":
                    lsbooks.append([b])
        cbbook.set_model(lsbooks)
        self.bookNoUpdate = False

    def getConfigList(self, prjid):
        res = []
        if self.prjid is None:
            return res
        root = os.path.join(self.settings_dir, prjid, "shared", "ptxprint")
        if os.path.exists(root):
            for s in os.scandir(root):
                if s.is_dir() and os.path.exists(os.path.join(root, s.name, "ptxprint.cfg")):
                    res.append(s.name)
        if 'Default' not in res:
            res.append('Default')   # it's only going to get sorted
        return res

    def updateSavedConfigList(self):
        self.configNoUpdate = True
        currConf = self.get("ecb_savedConfig")
        self.cb_savedConfig.remove_all()
        savedConfigs = self.getConfigList(self.prjid)
        if len(savedConfigs):
            for cfgName in sorted(savedConfigs):
                self.cb_savedConfig.append_text(cfgName)
            if currConf in savedConfigs:
                self.set("ecb_savedConfig", currConf)
            else:
                self.set("ecb_savedConfig", "Default")
        else:
            self.configNoUpdate = False
            self.builder.get_object("t_savedConfig").set_text("")
            self.builder.get_object("t_configNotes").set_text("")
        self.configNoUpdate = False

    def updateDiglotConfigList(self):
        self.ecb_diglotSecConfig.remove_all()
        digprj = self.get("fcb_diglotSecProject")
        if digprj is None:
            return
        diglotConfigs = self.getConfigList(digprj)
        if len(diglotConfigs):
            for cfgName in sorted(diglotConfigs):
                self.ecb_diglotSecConfig.append_text(cfgName)
            self.set("ecb_diglotSecConfig", "Default")

    def loadConfig(self, config):
        self.updateBookList()
        super(GtkViewModel, self).loadConfig(config)
        for k, v in _sensitivities.items():
            state = self.get(k)
            # print("k,v", k,v)
            for w in v:
                # print("w", w)
                self.builder.get_object(w).set_sensitive(state)
        for k, v in _nonsensitivities.items():
            state = not self.get(k)
            for w in v:
                self.builder.get_object(w).set_sensitive(state)
        self.colourTabs()

    def colourTabs(self):
        col = "#688ACC"
        ic = " color='"+col+"'" if self.get("c_includeillustrations") else ""
        self.builder.get_object("lb_Pictures").set_markup("<span{}>Pictures</span>".format(ic))

        dc = " color='"+col+"'" if self.get("c_diglot") else ""
        bc = " color='"+col+"'" if self.get("c_borders") else ""
        self.builder.get_object("lb_DiglotBorder").set_markup("<span{}>Diglot</span>+<span{}>Border</span>".format(dc,bc))

        tc = " color='"+col+"'" if self.get("c_thumbtabs") else ""
        self.builder.get_object("lb_Tabs").set_markup("<span{}>Tabs</span>".format(tc))

    def sensiVisible(self, k, focus=False, state=None):
        if state is None:
            state = self.get(k)
        for d, l in [(_sensitivities, lambda x: x), (_nonsensitivities, lambda x: not x)]:
            if k not in d:
                continue
            if k.startswith("r_"):
                anyset = False
                for a, v in d[k].items():
                    s = self.get(a)
                    if s:
                        anyset = s
                    for w in v:
                        wid = self.builder.get_object(w)
                        if wid is not None:
                            wid.set_sensitive(l(s))
                if not anyset:
                    v = d[d[k].keys()[0]]
                    for w in v:
                        wid = self.builder.get_object(w)
                        if wid is not None:
                            wid.set_sensitive(l(s))
            else:
                for w in d[k]:
                    wid = self.builder.get_object(w)
                    if wid is not None:
                        wid.set_sensitive(l(state))
        if focus and k in _sensitivities:
            self.builder.get_object(_sensitivities[k][0]).grab_focus()
        return state

    def onSimpleClicked(self, btn):
        self.sensiVisible(Gtk.Buildable.get_name(btn))

    def on2colClicked(self, btn):
        self.onSimpleClicked(btn)
        self.picListView.onRadioChanged()
        val = self.get("s_indentUnit")
        if btn.is_active():
            val = val / 2
        else:
            val = val * 2
        self.set("s_indentUnit", val)

    def onSimpleFocusClicked(self, btn):
        self.sensiVisible(Gtk.Buildable.get_name(btn), focus=True)

    def onLockUnlockSavedConfig(self, btn):
        lockBtn = self.builder.get_object("btn_lockunlock")
        dialog = self.builder.get_object("dlg_password")
        dialog.set_keep_above(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            pw = self.get("t_password")
        elif response == Gtk.ResponseType.CANCEL:
            pw = ""
        else:
            return
        invPW = self.get("t_invisiblePassword")
        if invPW == None or invPW == "": # No existing PW, so set a new one
            self.builder.get_object("t_invisiblePassword").set_text(pw)
            self.builder.get_object("c_hideAdvancedSettings").set_sensitive(False)
            self.onSaveConfig(None, force=True)     # Always save the config when locking
        else: # try to unlock the settings by removing the settings
            if pw == invPW:
                self.builder.get_object("t_invisiblePassword").set_text("")
                self.builder.get_object("c_hideAdvancedSettings").set_sensitive(True)
            else: # Mismatching password - Don't do anything
                pass
        self.builder.get_object("t_password").set_text("")
        dialog.set_keep_above(False)
        dialog.hide()

    def onPasswordChanged(self, t_invisiblePassword):
        lockBtn = self.builder.get_object("btn_lockunlock")
        if self.get("t_invisiblePassword") == "":
            status = True
            lockBtn.set_label(_("Lock Config"))
        else:
            status = False
            lockBtn.set_label(_("Unlock Config"))
        for c in ["btn_saveConfig", "btn_deleteConfig", "t_configNotes", "c_hideAdvancedSettings", 
                  "btn_Generate", "btn_plAdd", "btn_plDel", "btn_plAdd1", "btn_plDel1", ]:
            self.builder.get_object(c).set_sensitive(status)
        
    def onExamineBookChanged(self, cb_examineBook):
        if self.bookNoUpdate == True:
            return
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        self.onViewerChangePage(None,None,pg)

    def onBookSelectorChange(self, btn):
        status = self.sensiVisible("r_book_multiple")
        if status and self.get("t_booklist") == "" and self.prjid is not None:
            self.updateDialogTitle()
        else:
            toc = self.builder.get_object("c_autoToC") # Ensure that we're not trying to build a ToC for a single book!
            toc.set_sensitive(status)
            if not status:
                toc.set_active(False)
            self.updateDialogTitle()
            bks = self.getBooks()
            if len(bks) > 1:
                self.builder.get_object("ecb_examineBook").set_active_id(bks[0])
        self.updatePicList()

    def _getFigures(self, bk, suffix="", sfmonly=False, media=None, usepiclists=False):
        if self.picListView.isEmpty():
            return super()._getFigures(bk, suffix=suffix, sfmonly=sfmonly, media=media,
                                      usepiclists=usepiclists)
        return self.picListView.getinfo()

    def updatePicList(self, bks=None, priority="Both", output=False):
        if self.picinfos is None:
            return
        filtered = self.get("c_filterPicList")
        if bks is None and filtered:
            bks = self.getBooks()
        self.picinfos.updateView(self.picListView, bks, filtered=filtered)

    def updatePicChecks(self, src):
        self.picChecksView.loadpic(src)

    def savePicChecks(self):
        self.picChecksView.savepic()

    def picChecksFilter(self, src, filt):
        return self.picChecksView.filter(src, filt)

    def onPicCheckFilterChanged(self, *a):
        w = self.builder.get_object('fcb_chklstFilter')
        f = w.get_active()
        self.picListView.setCheckFilter(self.get('c_picCheckInvFilter'), f)

    def onGeneratePicListClicked(self, btn):
        priority=self.get("fcb_diglotPicListSources")[:4]
        bks2gen = self.getBooks()
        if not len(bks2gen):
            return
        ab = self.getAllBooks()
        bks = bks2gen
        dialog = self.builder.get_object("dlg_generate")
        self.set("l_generate_booklist", " ".join(bks))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            if self.get("r_generate") == "all":
                procbks = ab.keys()
                doclear = True
            else:
                procbks = bks
                doclear = False
            rnd = self.get("c_randomPicPosn")
            cols = 2 if self.get("c_doublecolumn") else 1
            if self.diglotView is None:
                PicInfoUpdateProject(self, procbks, ab, self.picinfos, random=rnd, cols=cols, doclear=doclear)
            else:
                mode = self.get("fcb_diglotPicListSources")
                if mode in ("both", "left"):
                    PicInfoUpdateProject(self, procbks, ab, self.picinfos,
                                         suffix="L", random=rnd, cols=cols)
                if mode in ("both", "right"):
                    diallbooks = self.diglotView.getAllBooks()
                    PicInfoUpdateProject(self.diglotView, procbks, diallbooks,
                                         self.picinfos, suffix="R", random=rnd, cols=cols)
            self.updatePicList(procbks)
            self.savePics()
            self.set("c_filterPicList", False)
            dialog.hide()

    def onFilterPicListClicked(self, btn):
        self.updatePicList()

    def onGenerateClicked(self, btn):
        priority=self.get("fcb_diglotPicListSources")[:4]
        pg = self.get("nbk_Viewer")
        pgid = self.notebooks['Viewer'][pg]
        bks2gen = self.getBooks()
        if not len(bks2gen):
            return
        bk = self.get("ecb_examineBook")
        bk = bk if bk in bks2gen else None
        if pgid == "scroll_AdjList": # AdjList
            self.generateAdjList()
        elif pgid == "scroll_FinalSFM" and bk is not None: # FinalSFM
            tmodel = TexModel(self, self.settings_dir, self.ptsettings, self.prjid)
            out = tmodel.convertBook(bk, self.working_dir, os.path.join(self.settings_dir, self.prjid))
            self.editFile(out, loc="wrk", pgid=pgid)
        self.onViewerChangePage(None,None,pg)

    def onChangedMainTab(self, nbk_Main, scrollObject, pgnum):
        pgid = Gtk.Buildable.get_name(nbk_Main.get_nth_page(pgnum))
        if pgid == "tb_ViewerEditor": # Viewer tab
            self.onRefreshViewerTextClicked(None)

    def onRefreshViewerTextClicked(self, btn):
        pg = self.get("nbk_Viewer")
        self.onViewerChangePage(None, None, pg)

    def onViewerChangePage(self, nbk_Viewer, scrollObject, pgnum):
        allpgids = ("tb_PicList", "scroll_AdjList", "scroll_FinalSFM", "scroll_TeXfile",
                    "scroll_XeTeXlog", "scroll_Settings", "tb_Links")
        if nbk_Viewer is None:
            nbk_Viewer = self.builder.get_object("nbk_Viewer")
        page = nbk_Viewer.get_nth_page(pgnum)
        if page == None:
            return
        for w in ["gr_editableButtons", "l_examineBook", "ecb_examineBook", "btn_Generate", 
                  "btn_saveEdits", "btn_refreshViewerText", "btn_viewEdit"]:
            self.builder.get_object(w).set_sensitive(True)
        self.builder.get_object("btn_Generate").set_sensitive(False)
        pgid = Gtk.Buildable.get_name(page)
        self.bookNoUpdate = True
        prjid = self.get("fcb_project")
        prjdir = os.path.join(self.settings_dir, prjid)
        bks = self.getBooks()
        bk = self.get("ecb_examineBook")
        genBtn = self.builder.get_object("btn_Generate")
        if bk == None or bk == "" and len(bks):
            bk = bks[0]
            self.builder.get_object("ecb_examineBook").set_active_id(bk)
        for o in ("l_examineBook", "ecb_examineBook"):
            self.builder.get_object(o).set_sensitive(pgid in allpgids[1:3])

        fndict = {"scroll_AdjList" : ("AdjLists", ".adj"), "scroll_FinalSFM" : ("", ""),
                  "scroll_TeXfile" : ("", ".tex"), "scroll_XeTeXlog" : ("", ".log"), "scroll_Settings": ("", ""), "tb_Links": ("", "")}

        if pgid == "scroll_FrontMatter": # This hasn't been built yet, but is coming soon!
            self.fileViews[pgnum][0].set_text("\n"  +_(" PicLists have now moved! Look for Details & Checklist on the Pictures tab.") + \
                                              "\n"*2+_(" In future a tool to help build and edit Front Matter will be included here."))
            return

        elif pgid in ("scroll_AdjList", "scroll_FinalSFM"):  # (AdjList,SFM)
            fname = self.getBookFilename(bk, prjid)
            if pgid == "scroll_FinalSFM":
                fpath = os.path.join(self.working_dir, fndict[pgid][0], fname)
                genBtn.set_sensitive(True)
            else:
                fpath = os.path.join(self.configPath(cfgname=self.configId, makePath=False), fndict[pgid][0], fname)
            doti = fpath.rfind(".")
            if doti > 0:
                fpath = fpath[:doti] + "-" + self.configName() + fpath[doti:] + fndict[pgid][1]
            if pgnum == 1: # AdjList
                if self.get("t_invisiblePassword") == "":
                    genBtn.set_sensitive(True)
                else:
                    self.builder.get_object("btn_saveEdits").set_sensitive(False)
            else: # scroll_FinalSFM
                self.builder.get_object("btn_saveEdits").set_sensitive(False)
                self.builder.get_object("btn_refreshViewerText").set_sensitive(False)

        elif pgid in ("scroll_TeXfile", "scroll_XeTeXlog"): # (TeX,Log)
            fpath = os.path.join(self.working_dir, self.baseTeXPDFnames()[0])+fndict[pgid][1]
            self.builder.get_object("btn_saveEdits").set_sensitive(False)
            self.builder.get_object("btn_refreshViewerText").set_sensitive(False)

        elif pgid == "scroll_Settings": # View/Edit one of the 4 Settings files or scripts
            fpath = self.builder.get_object("l_Settings").get_tooltip_text()
            if fpath == None:
                self.fileViews[pgnum][0].set_text("\n"+_(" Use the 'Advanced' tab to select which settings you want to view or edit."))
                self.builder.get_object("l_Settings").set_text("Settings")
                return

        else:
            return

        if fpath is None:
            return
        set_tooltip = self.builder.get_object("l_{1}".format(*pgid.split("_"))).set_tooltip_text
        if os.path.exists(fpath):
            set_tooltip(fpath)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as inf:
                txt = inf.read()
                if len(txt) > 60000:
                    txt = txt[:60000]+_("\n\n------------------------------------- \
                                           \n[File has been truncated for display] \
                                           \nClick on View/Edit... button to see more.")
            self.fileViews[pgnum][0].set_text(txt)
            self.onViewerFocus(self.fileViews[pgnum][1], None)
        else:
            set_tooltip(None)
            self.fileViews[pgnum][0].set_text(_("\nThis file doesn't exist yet.\n\nTry... \
                                               \n   * Check option (above) to 'Preserve Intermediate Files and Logs' \
                                               \n   * Generate the PiCList or AdjList \
                                               \n   * Click 'Print' to create the PDF"))
        self.bookNoUpdate = False

    def saveStyles(self, force=False):
        if not force and self.configLocked():
            return
        fname = os.path.join(self.configPath(self.configName(), makePath=True), "ptxprint.sty")
        with open(fname, "w", encoding="Utf-8") as outf:
            self.styleEditorView.output_diffile(outf)

    def savePics(self, force=False):
        if not force and self.configLocked():
            return
        if self.picinfos is not None and self.picinfos.loaded:
            self.picListView.updateinfo(self.picinfos)
        super().savePics(force=force)

    def onSavePicListEdits(self, btn):
        self.savePics()

    def onSaveEdits(self, btn):
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        pgid = self.notebooks["Viewer"][pg]
        buf = self.fileViews[pg][0]
        fpath = self.builder.get_object("l_{1}".format(*pgid.split("_"))).get_tooltip_text()
        titer = buf.get_iter_at_mark(buf.get_insert())
        self.cursors[pg] = (titer.get_line(), titer.get_line_offset())
        text2save = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        openfile = open(fpath,"w", encoding="utf-8")
        openfile.write(text2save)
        openfile.close()

    def onOpenInSystemEditor(self, btn):
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        pgid = self.notebooks["Viewer"][pg]
        fpath = self.builder.get_object("l_{1}".format(*pgid.split("_"))).get_tooltip_text() or ""
        if os.path.exists(fpath):
            if sys.platform == "win32":
                os.startfile(fpath)
            elif sys.platform == "linux":
                subprocess.call(('xdg-open', fpath))

    def onScriptChanged(self, btn):
        # If there is a matching digit style for the script that has just been set, 
        # then also turn that on (but it can be overridden by the user if needed).
        self.fcb_digits.set_active_id(self.get('fcb_script'))

    def onFontChanged(self, fbtn):
        # traceback.print_stack(limit=3)
        super(GtkViewModel, self).onFontChanged(fbtn)
        self.builder.get_object('c_useGraphite').set_sensitive(self.get('c_useGraphite'))
        self.setEntryBoxFont()
        self.updateFakeLabels()

    def setEntryBoxFont(self):
        # Set the font of any GtkEntry boxes to the primary body text font for this project
        fsize = self.get("s_fontsize")
        (name, style) = self.get("bl_fontR")
        fallback = ',Sans'
        if self.diglotView is not None:
            (digname, digstyle) = self.diglotView.get("bl_fontR")
            fallback = "," + digname + fallback
        pangostr = '{}{} {} {}'.format(name, fallback, style, fsize)
        p = Pango.FontDescription(pangostr)
        for w in ("t_clHeading", "t_tocTitle", "t_configNotes", "scroll_FinalSFM", \
                  "ecb_ftrcenter", "ecb_hdrleft", "ecb_hdrcenter", "ecb_hdrright", "t_fncallers", "t_xrcallers", \
                  "l_projectFullName", "t_plCaption", "t_plRef", "t_plAltText", "t_plCopyright", "textv_colophon"):
            self.builder.get_object(w).modify_font(p)
        self.picListView.modify_font(p)
        # MH TO DO: Also need to handle TWO fallback fonts in the picList for Diglots (otherwise one script will end up as Tofu)

    def onRadioChanged(self, btn):
        n = Gtk.Buildable.get_name(btn)
        bits = n.split("_")[1:]
        if btn.get_active():
            self.set("r_"+bits[0], bits[1])
        self.sensiVisible("r_"+bits[0])
        if n.startswith("r_book_"):
            self.onBookSelectorChange(btn)
            self.updateExamineBook()
            self.updateDialogTitle()

    def onPicRadioChanged(self, btn):
        self.onRadioChanged(btn)
        self.picListView.onRadioChanged()
    
    def updateFakeLabels(self):
        status = self.get("c_fakebold") or self.get("c_fakeitalic") or self.get("c_fakebolditalic")
        for c in ("l_embolden", "l_slant"):
            self.builder.get_object(c).set_sensitive(status)

    def onFakeClicked(self, btn):
        self.onSimpleClicked(btn)
        self.updateFakeLabels()
        
    def onVariableLineSpacingClicked(self, btn):
        self.sensiVisible("c_variableLineSpacing")
        lnspVal = round(float(self.get("s_linespacing")), 1)
        minVal = round(float(self.get("s_linespacingmin")), 1)
        maxVal = round(float(self.get("s_linespacingmax")), 1)
        if self.get("c_variableLineSpacing") and lnspVal == minVal and lnspVal == maxVal:
            self.set("s_linespacingmin", lnspVal - 1)
            self.set("s_linespacingmax", lnspVal + 2)

    def onSectionHeadsClicked(self, btn):
        self.onSimpleClicked(btn)
        self.builder.get_object("c_parallelRefs").set_active(status)

    def onHyphenateClicked(self, btn):
        if self.prjid is not None:
            fname = os.path.join(self.settings_dir, self.prjid, "shared", "ptxprint", 'hyphen-{}.tex'.format(self.prjid))
        
    def onUseIllustrationsClicked(self, btn):
        self.onSimpleClicked(btn)
        self.colourTabs()
        if btn.get_active():
            if self.picinfos is None:
                self.picinfos = PicInfo(self)
            self.loadPics()
            self.updatePicList()
        else:
            self.picinfos.clear(self)
            self.picListView.clear()

    def onUseCustomFolderclicked(self, btn):
        status = self.sensiVisible("c_useCustomFolder")
        if not status:
            self.builder.get_object("c_exclusiveFiguresFolder").set_active(status)

    def onPageNumTitlePageChanged(self, btn):
        if self.get("c_pageNumTitlePage"):
            self.builder.get_object("c_printConfigName").set_active(False)

    def onPrintConfigNameChanged(self, btn):
        if self.get("c_printConfigName"):
            self.builder.get_object("c_pageNumTitlePage").set_active(False)

    def onResetFNcallersClicked(self, btn_resetFNcallers):
        w = self.builder.get_object("t_fncallers")
        w.set_text(re.sub(" ", ",", self.ptsettings.get('footnotes', "")))
        if w.get_text() == "":
            w.set_text("a,b,c,d,e,f,✶,☆,✦,✪,†,‡,§")
        
    def onResetXRcallersClicked(self, btn_resetXRcallers):
        w = self.builder.get_object("t_xrcallers")
        w.set_text(re.sub(" ", ",", self.ptsettings.get('crossrefs', "")))
        if w.get_text() == "":
            w.set_text("†,‡,§,∥,#")

    def onFnFontSizeChanged(self, btn, *a):
        val = float(self.get("s_fnfontsize"))
        val = val * float(self.get("s_fontsize")) / 12.
        self.styleEditorView.setval("f", "FontSize", val)
        self.styleEditorView.setval("x", "FontSize", val, ifunchanged=True)

    def updateFnFontSize(self, key, val):
        val = float(val) * 12. / float(self.get("s_fontsize"))
        self.set("s_fnfontsize", val)

    def onFnLineSpacingChanged(self, btn, *a):
        val = self.get("s_fnlinespacing")
        for k in ("f", "x"):
            isabs = self.styleEditorView.getval(k, "LineSpacing") == None
            if isabs:
                self.styleEditorView.setval(k, "Baseline", val)
            else:
                v = val / float(self.get("s_linespacing", default=12.))
                self.styleEditorView.setval(k, "LineSpacing", v)

    def updateFnLineSpacing(self, key, val):
        val = float(val)
        if key.lower() == "linespacing":
            val = val * self.get("s_linespacing", default=12.)
        self.set("s_fnlinespacing", val)

    def onFnBlendClicked(self, btn):
        self.onSimpleClicked(btn)
        self.styleEditorView.setval("x", "NoteBlendInto", "f" if btn.get_active() else None)

    def onDirectionChanged(self, btn, *a):
        rtl = self.get("fcb_textDirection") == "Right-to-Left"
        if self.loadingConfig:
            self.rtl = rtl
        if rtl == self.rtl:
            return
        for k in self.styleEditorView.allStyles():
            j = self.styleEditorView.getval(k, "Justification")
            if j.lower() == "right":
                self.styleEditorView.setval(k, "Justification", "Left")
            elif j.lower() == "left":
                self.styleEditorView.setval(k, "Justification", "Right")

    def onThumbStyleClicked(self, btn):
        self.styleEditorView.selectMarker("zthumbtab" if self.get("c_thumbIsZthumb") else "toc3")
        mpgnum = self.notebooks['Main'].index("Style")
        self.builder.get_object("nbk_Main").set_current_page(mpgnum)

    def onProcessScriptClicked(self, btn):
        if not self.sensiVisible("c_processScript"):
            self.builder.get_object("btn_editScript").set_sensitive(False)
        else:
            if self.get("btn_selectScript") != None:
                self.builder.get_object("btn_editScript").set_sensitive(True)

    def onIntroOutlineClicked(self, btn):
        if not self.sensiVisible("c_introOutline"):
            self.builder.get_object("c_prettyIntroOutline").set_active(False)

    def onDeleteTemporaryFilesClicked(self, btn):
        dir = self.working_dir
        warnings = []
        title = _("Remove Intermediate Files and Logs?")
        question = _("Are you sure you want to delete\nALL the temporary PTXprint files?")
        if self.msgQuestion(title, question):
            patterns = []
            for extn in ('delayed','parlocs','notepages', 'picpages', 'piclist', 'SFM', 'sfm', 'xdv', 'tex', 'log'):
                patterns.append(r".+\.{}".format(extn))
            patterns.append(r".+\-draft\....".format(extn))
            patterns.append(r".+\.toc".format(extn))
            # MH: Should we be deleting NestedStyles.sty as well? 
            # patterns.append(r"NestedStyles\.sty".format(extn)) # To be updated as locn has changed (maybe no longer need to delete it)
            patterns.append(r"ptxprint\-.+\.tex".format(extn))
            # print(patterns)
            for pattern in patterns:
                for f in os.listdir(dir):
                    if re.search(pattern, f):
                        try:
                            os.remove(os.path.join(dir, f))
                        except (OSError, PermissionError):
                            warnings += [f]
            for p in ["tmpPics", "tmpPicLists"]:
                path2del = os.path.join(dir, p)
                # Make sure we're not deleting something closer to Root!
                if len(path2del) > 30 and os.path.exists(path2del):
                    try:
                        rmtree(path2del)
                    except (OSError, PermissionError):
                        warnings += [path2del]
            if len(warnings):
                self.printer.doError(_("Warning: Could not delete some file(s) or folders(s):"),
                        secondary="\n".join(warnings))

    def onRefreshFontsclicked(self, btn):
        fc = fccache()
        lsfonts = self.builder.get_object("ls_font")
        fc.fill_liststore(lsfonts)

    def onFontRclicked(self, btn):
        self.getFontNameFace("bl_fontR")
        self.onFontChanged(btn)
        
    def onFontBclicked(self, btn):
        self.getFontNameFace("bl_fontB")
        
    def onFontIclicked(self, btn):
        self.getFontNameFace("bl_fontI")
        
    def onFontBIclicked(self, btn):
        self.getFontNameFace("bl_fontBI")
        
    def onFontRowSelected(self, dat):
        lsstyles = self.builder.get_object("ls_fontFaces")
        lb = self.builder.get_object("tv_fontFamily")
        sel = lb.get_selection()
        ls, row = sel.get_selected()
        name = ls.get_value(row, 0)
        initFontCache().fill_cbstore(name, lsstyles)
        self.builder.get_object("fcb_fontFaces").set_active(0)

    def responseToDialog(entry, dialog, response):
        dialog.response(response)

    def getFontNameFace(self, btnid, noStyles=False):
        btn = self.builder.get_object(btnid)
        lb = self.builder.get_object("tv_fontFamily")
        lb.set_cursor(0)
        dialog = self.builder.get_object("dlg_fontChooser")
        self.builder.get_object("t_fontSearch").set_text("")
        self.builder.get_object("t_fontSearch").has_focus()
        self.builder.get_object("fcb_fontFaces").set_sensitive(not noStyles)
        # dialog.set_default_response(Gtk.ResponseType.OK)
        dialog.set_keep_above(True)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            sel = lb.get_selection()
            ls, row = sel.get_selected()
            name = ls.get_value(row, 0)
            cb = self.builder.get_object("fcb_fontFaces")
            if noStyles:
                style = ""
            else:
                style = cb.get_model()[cb.get_active()][0]
                if style == "Regular":
                    style = ""
            setFontButton(btn, name, style)
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.set_keep_above(False)
        dialog.hide()

    def onChooseBooksClicked(self, btn):
        dialog = self.builder.get_object("dlg_multiBookSelector")
        dialog.set_keep_above(True)
        mbs_grid = self.builder.get_object("mbs_grid")
        mbs_grid.forall(mbs_grid.remove)
        lsbooks = self.builder.get_object("ls_books")
        bl = self.builder.get_object("t_booklist")
        self.alltoggles = []
        for i, b in enumerate(lsbooks):
            tbox = Gtk.ToggleButton(b[0])
            tbox.show()
            if tbox.get_label() in bl.get_text().split(" "):
                tbox.set_active(True)
            self.alltoggles.append(tbox)
            mbs_grid.attach(tbox, i // 13, i % 13, 1, 1)
        response = dialog.run()
        booklist = []
        if response == Gtk.ResponseType.OK:
            booklist = sorted((b.get_label() for b in self.alltoggles if b.get_active()), \
                                    key=lambda x:_allbkmap.get(x, len(_allbkmap)))
            bl.set_text(" ".join(b for b in booklist))
        if self.get("r_book") in ("single", "multiple"):
            self.set("r_book", "multiple" if len(booklist) else "single")
        # self.set("c_prettyIntroOutline", False)
        self.updateDialogTitle()
        self.updateExamineBook()
        self.updatePicList()
        dialog.set_keep_above(False)
        dialog.hide()
        
    def updateExamineBook(self):    
        bks = self.getBooks()
        if len(bks):
            self.builder.get_object("ecb_examineBook").set_active_id(bks[0])

    def toggleBooks(self,start,end):
        bp = self.ptsettings['BooksPresent']
        cPresent = sum(1 for x in bp[start:end] if x == "1")
        cActive = 0
        toggle = False
        for b in self.alltoggles:
            if b.get_active() and b.get_label() in allbooks[start:end]:
                cActive += 1
        if cActive < cPresent:
            toggle = True
        for b in self.alltoggles:
            if b.get_label() in allbooks[start:end]:
                b.set_active(toggle)
        self.updatePicList()

    def onClickmbs_all(self, btn):
        self.toggleBooks(0,124)

    def onClickmbs_OT(self, btn):
        self.toggleBooks(0,39)
        
    def onClickmbs_NT(self, btn):
        self.toggleBooks(40,67)

    def onClickmbs_DC(self, btn):
        self.toggleBooks(67,85)

    def onClickmbs_xtra(self, btn):
        self.toggleBooks(85,124)

    def onClickmbs_none(self, btn):
        for b in self.alltoggles:
            if b.get_label() in allbooks[0:124]:
                b.set_active(False)

    def onCustomOrderClicked(self, btn):
        if self.get("c_customOrder"):
            # do something
            return
        
    def onTocClicked(self, btn):
        if not self.get("c_usetoc1") and not self.get("c_usetoc2") and not self.get("c_usetoc3"):
            toc = self.builder.get_object("c_usetoc1")
            toc.set_active(True)
            
    def _setchap(self, ls, start, end):
        self.chapNoUpdate = True
        ls.clear()
        for c in range(start, end+1):
            ls.append([str(c)])
        self.chapNoUpdate = False

    def onBookChange(self, cb_book):
        self.bk = self.get("ecb_book")
        if self.bk != "":
            self.chs = int(chaps.get(str(self.bk)))
            self.chapfrom = self.builder.get_object("ls_chapfrom")
            self._setchap(self.chapfrom, 1, self.chs)
            self.fcb_chapfrom.set_active_id('1')
        
            self.chapto = self.builder.get_object("ls_chapto")
            self._setchap(self.chapto, 1, self.chs)
            self.fcb_chapto.set_active_id(str(self.chs))
            # self.builder.get_object("ecb_examineBook").set_active_id(self.bk)
            self.updateExamineBook()
        self.updateDialogTitle()
        self.updatePicList()

    def onChapFrmChg(self, cb_chapfrom):
        if self.chapNoUpdate == True:
            return
        self.bk = self.get("ecb_book")
        if self.bk != "":
            self.chs = int(chaps.get(str(self.bk)))
            self.strt = self.get("fcb_chapfrom")
            self.chapto = self.builder.get_object("ls_chapto")
            self._setchap(self.chapto, (int(self.strt) if self.strt is not None else 0), self.chs)
            self.fcb_chapto.set_active_id(str(self.chs))

    def configName(self):
        cfg = self.pendingConfig or self.get("ecb_savedConfig") or ""
        cfgName = re.sub('[^-a-zA-Z0-9_()]+', '', cfg)
        if self.pendingConfig is None:
            self.set("ecb_savedConfig", cfgName)
        else:
            self.pendingConfig = cfgName
        return cfgName or None

    def setPrjid(self, prjid, saveCurrConfig=False):
        if not self.initialised:
            self.pendingPid = prjid
        else:
            self.set("fcb_project", prjid)

    def setConfigId(self, configid, saveCurrConfig=False):
        if not configid:
            configid="Default"
        if not self.initialised:
            self.pendingConfig = configid
        else:
            self.set("ecb_savedConfig", configid)

    def onProjectChange(self, cb_prj):
        self.updatePrjLinks()
        self.builder.get_object("btn_saveConfig").set_sensitive(True)
        self.builder.get_object("btn_deleteConfig").set_sensitive(False)
        lockBtn = self.builder.get_object("btn_lockunlock")
        lockBtn.set_label("Lock Config")
        lockBtn.set_sensitive(False)
        self.updateProjectSettings(None, saveCurrConfig=True, configName="Default")
        self.updateSavedConfigList()
        for o in ["b_print", "fr_SavedConfigSettings", "tb_Font", "tb_Layout", "tb_Body", "tb_HeadFoot", "tb_Pictures",
                  "tb_Advanced", "tb_Logging", "tb_ViewerEditor", "tb_DiglotBorder"]:
            self.builder.get_object(o).set_sensitive(True)
        self.updateFonts()
        self.updateHdrFtrOptions(self.get("c_diglot"))
        if self.ptsettings is not None:
            self.builder.get_object("l_projectFullName").set_label(self.ptsettings.get('FullName', ""))
            self.builder.get_object("l_projectFullName").set_tooltip_text(self.ptsettings.get('Copyright', ""))
        else:
            self.builder.get_object("l_projectFullName").set_label("")
            self.builder.get_object("l_projectFullName").set_tooltip_text("")
        pts = self._getPtSettings()
        if pts is not None:
            self.builder.get_object("t_copyrightStatement").set_text(pts.get('Copyright', ""))

    def updatePrjLinks(self):
        if self.settings_dir != None and self.prjid != None:
            self.builder.get_object("lb_ptxprintdir").set_label(os.path.dirname(__file__))
            self.builder.get_object("lb_prjdir").set_label(os.path.join(self.settings_dir, self.prjid))
            self.builder.get_object("lb_settings_dir").set_label(self.configPath(cfgname=self.configName()) or "")
            self.builder.get_object("lb_working_dir").set_label(self.working_dir or "")
            
    def updateProjectSettings(self, prjid, saveCurrConfig=False, configName=None):
        self.picListView.clear()
        if self.picinfos is not None:
            self.picinfos.clear()
        if not super(GtkViewModel, self).updateProjectSettings(prjid, saveCurrConfig=saveCurrConfig, configName=configName):
            for fb in ['bl_fontR', 'bl_fontB', 'bl_fontI', 'bl_fontBI', 'bl_fontExtraR']:
                fblabel = self.builder.get_object(fb).set_label("Select font...")
        if self.prjid:
            self.updatePrjLinks()
            self.userconfig.set("init", "project", self.prjid)
            if getattr(self, 'configId', None) is not None:
                self.userconfig.set("init", "config", self.configId)
        status = self.get("r_book") == "multiple"
        for c in ("c_combine", "t_booklist"):
            self.builder.get_object(c).set_sensitive(status)
        toc = self.builder.get_object("c_autoToC") # Ensure that we're not trying to build a ToC for a single book!
        toc.set_sensitive(status)
        if not status:
            toc.set_active(False)
        for i in self.notebooks['Viewer']:
            obj = self.builder.get_object("l_{1}".format(*i.split("_")))
            if obj is not None:
                obj.set_tooltip_text(None)
        self.updatePrjLinks()
        self.setEntryBoxFont()
        self.updatePicList()
        self.updateDialogTitle()
        self.picChecksView.init(basepath=self.configPath(cfgname=None), configid=self.configId)
        self.styleEditorView.load(self.getStyleSheets())

    def onConfigNameChanged(self, cb_savedConfig):
        if self.configNoUpdate:
            return
        self.builder.get_object("c_hideAdvancedSettings").set_sensitive(True)
        lockBtn = self.builder.get_object("btn_lockunlock")
        lockBtn.set_label("Lock Config")
        self.builder.get_object("t_invisiblePassword").set_text("")
        self.builder.get_object("btn_saveConfig").set_sensitive(True)
        self.builder.get_object("btn_deleteConfig").set_sensitive(True)
        if len(self.get("ecb_savedConfig")):
            lockBtn.set_sensitive(True)
        else:
            self.builder.get_object("t_configNotes").set_text("")
            lockBtn.set_sensitive(False)
        cpath = self.configPath(cfgname=self.configName())
        if cpath is not None and os.path.exists(cpath):
            self.updateProjectSettings(self.prjid, saveCurrConfig=False, configName=self.configName()) # False means DON'T Save!
        self.updateDialogTitle()

    def updateFonts(self):
        if self.ptsettings is None:
            return
        ptfont = self.ptsettings.get("DefaultFont", "Arial")
        fb = 'bl_fontR'
        fblabel = self.builder.get_object(fb).get_label()
        if fblabel == _("Select font..."):
            w = self.builder.get_object(fb)
            setFontButton(w, ptfont, "")
            self.onFontChanged(w)

    def updateDialogTitle(self):
        titleStr = super(GtkViewModel, self).getDialogTitle()
        self.builder.get_object("ptxprint").set_title(titleStr)

    def editFile(self, file2edit, loc="wrk", pgid="scroll_Settings", switch=None): # keep param order
        if switch is None:
            switch = pgid == "scroll_Settings"
        pgnum = self.notebooks["Viewer"].index(pgid)
        mpgnum = self.notebooks["Main"].index("tb_ViewerEditor")
        if switch:
            self.builder.get_object("nbk_Main").set_current_page(mpgnum)
            self.builder.get_object("nbk_Viewer").set_current_page(pgnum)
        # self.prjid = self.get("fcb_project")
        self.prjdir = os.path.join(self.settings_dir, self.prjid)
        if loc == "wrk":
            fpath = os.path.join(self.working_dir, file2edit)
        elif loc == "prj":
            fpath = os.path.join(self.settings_dir, self.prjid, file2edit)
        elif loc == "cfg":
            cfgname = self.configName()
            fpath = os.path.join(self.configPath(cfgname), file2edit)
            if not os.path.exists(fpath):
                fpath = os.path.join(self.configPath(""), file2edit)
        elif "\\" in loc or "/" in loc:
            fpath = os.path.join(loc, file2edit)
        else:
            return
        label = self.builder.get_object("l_{1}".format(*pgid.split("_")))
        label.set_tooltip_text(fpath)
        if pgid == "scroll_Settings":
            self.builder.get_object("gr_editableButtons").set_sensitive(True)
            label.set_text(file2edit)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as inf:
                txt = inf.read()
                # if len(txt) > 32000:
                    # txt = txt[:32000]+"\n\n etc...\n\n"
            self.fileViews[pgnum][0].set_text(txt)
            self.onViewerFocus(self.fileViews[pgnum][1], None)
        else:
            self.fileViews[pgnum][0].set_text(_("\nThis file doesn't exist yet!\n\nEdit here and Click 'Save' to create it."))

    def editFile_delayed(self, *a):
        GLib.idle_add(self.editFile, *a)

    def onViewerLostFocus(self, widget, event):
        pgnum = self.notebooks['Viewer'].index(widget.pageid)
        t = self.fileViews[pgnum][0].get_iter_at_mark(self.fileViews[pgnum][0].get_insert())
        self.cursors[pgnum] = (t.get_line(), t.get_line_offset())

    def onViewerFocus(self, widget, event):
        pgnum = self.notebooks['Viewer'].index(widget.pageid)
        tbuf = self.fileViews[pgnum][0]
        tmark = tbuf.get_insert()
        titer = tbuf.get_iter_at_mark(tmark)
        titer.set_line(self.cursors[pgnum][0])
        titer.set_line_offset(self.cursors[pgnum][1])
        tbuf.move_mark(tmark, titer)
        tbuf.place_cursor(titer)
        GLib.idle_add(self.fileViews[pgnum][1].scroll_mark_onscreen, tmark)

    def onEditScriptFile(self, btn):
        customScriptFPath = self.get("btn_selectScript")
        scriptName = os.path.basename(customScriptFPath)
        scriptPath = customScriptFPath[:-len(scriptName)]
        if len(customScriptFPath):
            self.editFile(scriptName, scriptPath)

    def onEditChangesFile(self, btn):
        self.editFile("PrintDraftChanges.txt", "prj")

    def onEditModsTeX(self, btn):
        # self.prjid = self.get("fcb_project")
        cfgname = self.configName()
        fpath = os.path.join(self.configPath(cfgname), "ptxprint-mods.tex")
        if not os.path.exists(fpath):
            openfile = open(fpath,"w", encoding="utf-8")
            openfile.write(_("% This is the .tex file specific for the {} project used by PTXprint.\n").format(self.prjid))
            if cfgname != "":
                openfile.write(_("% Saved Configuration name: {}\n").format(cfgname))
            openfile.close()
        self.editFile("ptxprint-mods.tex", "cfg")

    def onEditCustomSty(self, btn):
        self.editFile("custom.sty", "prj")

    def onEditModsSty(self, btn):
        self.editFile("ptxprint-mods.sty", "cfg")

    def onMainBodyTextChanged(self, btn):
        self.sensiVisible("c_mainBodyText")

    def onSelectScriptClicked(self, btn_selectScript):
        customScript = self.fileChooser("Select a Custom Script file", 
                filters = {"Executable Scripts": {"patterns": ["*.bat", "*.exe", "*.py", "*.sh"] , "mime": "application/bat", "default": True},
                           "All Files": {"pattern": "*"}},
                           # "TECkit Mappings": {"pattern": ["*.map", "*.tec"]},
                           # "CC Tables": {"pattern": "*.cct"},
                multiple = False, basedir=self.working_dir)
        if customScript is not None:
            self.customScript = customScript[0]
            self.builder.get_object("c_processScript").set_active(True)
            btn_selectScript.set_tooltip_text(str(customScript[0]))
            for c in ("c_processScriptBefore", "c_processScriptAfter", "btn_editScript"):
                self.builder.get_object(c).set_sensitive(True)
        else:
            self.customScript = None
            btn_selectScript.set_tooltip_text("")
            self.builder.get_object("c_processScript").set_active(False)
            for c in ("c_processScriptBefore", "c_processScriptAfter", "btn_editScript"):
                self.builder.get_object(c).set_sensitive(False)

    def onUsePrintDraftFolderClicked(self, c_useprintdraftfolder):
        self.sensiVisible("c_useprintdraftfolder")

    def onCreateZipArchiveClicked(self, btn_createZipArchive):
        cfname = self.configName()
        zfname = self.prjid+("-"+cfname if cfname else "")+"PTXprintArchive.zip"
        archiveZipFile = self.fileChooser(_("Select the location and name for the Archive file"),
                filters={"ZIP files": {"pattern": "*.zip", "mime": "application/zip"}},
                multiple=False, folder=False, save=True, basedir=self.working_dir, defaultSaveName=zfname)
        if archiveZipFile is not None:
            # self.archiveZipFile = archiveZipFile[0]
            btn_createZipArchive.set_tooltip_text(str(archiveZipFile[0]))
            self.createArchive(str(archiveZipFile[0]))
            
        else:
            # self.archiveZipFile = None
            btn_createZipArchive.set_tooltip_text("No Archive File Created")

    def onSelectOutputFolderClicked(self, btn_selectOutputFolder):
        customOutputFolder = self.fileChooser("Select the output folder", 
                filters = None, multiple = False, folder = True)
        if customOutputFolder is not None and len(customOutputFolder):
            self.customOutputFolder = customOutputFolder[0]
            btn_selectOutputFolder.set_tooltip_text(str(customOutputFolder[0]))
            self.builder.get_object("c_useprintdraftfolder").set_active(False)
            self.working_dir = self.customOutputFolder
            self.set("btn_selectOutputFolder", self.customOutputFolder)
            self.fixed_wd = True
        else:
            self.customOutputFolder = None
            btn_selectOutputFolder.set_tooltip_text("")
            self.builder.get_object("c_useprintdraftfolder").set_active(True)
            self.builder.get_object("btn_selectOutputFolder").set_sensitive(False)

    def onSelectModuleClicked(self, btn):
        prjdir = os.path.join(self.settings_dir, self.prjid)
        moduleFile = self.fileChooser("Select a Paratext Module", 
                filters = {"Modules": {"patterns": ["*.sfm"] , "mime": "text/plain", "default": True},
                           "All Files": {"pattern": "*"}},
                multiple = False, basedir=os.path.join(prjdir, "Modules"))
        if moduleFile is not None:
            moduleFile = [x.relative_to(prjdir) for x in moduleFile]
            self.moduleFile = moduleFile[0]
            self.builder.get_object("lb_bibleModule").set_label(os.path.basename(moduleFile[0]))
            self.builder.get_object("btn_chooseBibleModule").set_tooltip_text(str(moduleFile[0]))
        else:
            self.builder.get_object("r_book_single").set_active(True)
            self.builder.get_object("lb_bibleModule").set_label("")
            self.moduleFile = None
            self.builder.get_object("btn_chooseBibleModule").set_tooltip_text("")

    def onSelectFigureFolderClicked(self, btn_selectFigureFolder):
        customFigFolder = self.fileChooser(_("Select the folder containing image files"),
                filters = None, multiple = False, folder = True)
        if customFigFolder is not None:
            if len(customFigFolder):
                self.customFigFolder = customFigFolder[0]
                self.set("lb_selectFigureFolder", str(customFigFolder[0]))
                self.set("c_useCustomFolder", True)
            else:
                self.customFigFolder = None
                self.set("lb_selectFigureFolder", "")
                self.set("c_useCustomFolder", False)
                self.builder.get_object("btn_selectFigureFolder").set_sensitive(False)

    def _onPDFClicked(self, title, isSingle, basedir, ident, attr, btn):
        vals = self.fileChooser(title,
                filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                multiple = not isSingle, basedir=basedir)
        if vals != None and len(vals) and str(vals[0]) != "None":
            self.builder.get_object("c_"+ident).set_active(True)
            if isSingle:
                setattr(self, attr, vals[0])
                btn.set_tooltip_text(str(vals[0]))
                self.set("lb_"+ident, pdfre.sub(r"\1", str(vals[0])))
            else:
                setattr(self, attr, vals)
                btn.set_tooltip_text("\n".join(str(s) for s in vals))
                self.set("lb_"+ident, ",".join(pdfre.sub(r"\1", str(s)) for s in vals))
        else:
            setattr(self, attr, None)
            btn.set_tooltip_text("")
            btn.set_sensitive(False)
            self.set("c_"+ident, False)
            self.set("lb_"+ident, "")

    def onFrontPDFsClicked(self, btn_selectFrontPDFs):
        self._onPDFClicked(_("Select one or more PDF(s) for FRONT matter"),
                False, self.working_dir, "inclFrontMatter", "FrontPDFs", btn_selectFrontPDFs)

    def onBackPDFsClicked(self, btn_selectBackPDFs):
        self._onPDFClicked(_("Select one or more PDF(s) for BACK matter"),
                False, self.working_dir, "inclBackMatter", "BackPDFs", btn_selectBackPDFs)

    def onWatermarkPDFclicked(self, btn_selectWatermarkPDF):
        self._onPDFClicked(_("Select Watermark PDF file"), True,
                os.path.join(os.path.dirname(__file__), "PDFassets", "watermarks"),
                "applyWatermark", "watermarks", btn_selectWatermarkPDF)

    def onPageBorderPDFclicked(self, btn_selectPageBorderPDF):
        self._onPDFClicked(_("Select Page Border PDF file"), True,
                os.path.join(os.path.dirname(__file__), "PDFassets", "border-art"),
                "inclPageBorder", "pageborder", btn_selectPageBorderPDF)

    def onSectionHeaderPDFclicked(self, btn_selectSectionHeaderPDF):
        self._onPDFClicked(_("Select Section Header PDF file"), True,
                os.path.join(os.path.dirname(__file__), "PDFassets", "border-art"),
                "inclSectionHeader", "sectionheader", btn_selectSectionHeaderPDF)

    def onEndOfBookPDFclicked(self, btn_selectEndOfBookPDF):
        self._onPDFClicked(_("Select End of Book PDF file"), True,
                os.path.join(os.path.dirname(__file__), "PDFassets", "border-art"),
                "inclEndOfBook", "endofbook", btn_selectEndOfBookPDF)

    def onVerseDecoratorPDFclicked(self, btn_selectVerseDecoratorPDF):
        self._onPDFClicked(_("Select Verse Decorator PDF file"), True,
                os.path.join(os.path.dirname(__file__), "PDFassets", "border-art"),
                "inclVerseDecorator", "versedecorator", btn_selectVerseDecoratorPDF)

    def onEditAdjListClicked(self, btn_editParaAdjList):
        pgnum = 1
        mpgnum = self.notebooks["Main"].index("tb_ViewerEditor")
        self.set("nbk_Main", mpgnum)
        self.set("nbk_Viewer", pgnum)
        self.onViewerChangePage(None,None,pgnum)

    def onEditPicListClicked(self, btn_editPicList):
        pgnum = 0
        mpgnum = self.notebooks["Main"].index("tb_ViewerEditor")
        self.set("nbk_Main", mpgnum)
        self.set("nbk_Viewer", pgnum)
        self.onViewerChangePage(None,None,pgnum)
        
    def ontv_sizeallocate(self, atv, dummy):
        b = atv.get_buffer()
        it = b.get_iter_at_offset(-1)
        atv.scroll_to_iter(it, 0, False, 0, 0)

    def fileChooser(self, title, filters=None, multiple=True, folder=False,
                    save=False, basedir=None, defaultSaveName=None, preview=None):
        if folder:
            action = Gtk.FileChooserAction.SELECT_FOLDER
            btnlabel = "Select"
        elif save:
            action = Gtk.FileChooserAction.SAVE
            btnlabel = "Create"
        else:
            action = Gtk.FileChooserAction.OPEN
            btnlabel = Gtk.STOCK_OPEN

        dialog = Gtk.FileChooserDialog(title, None,
            (action),
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            (btnlabel), Gtk.ResponseType.OK))
        dialog.set_default_size(400, 300)
        dialog.set_select_multiple(multiple)
        if basedir is not None:
            dialog.set_current_folder(basedir)
        if save:
            dialog.set_do_overwrite_confirmation(True)
            if defaultSaveName is None:
                dialog.set_current_name("XYZptxPrintArchive.zip")
            else:
                dialog.set_current_name(defaultSaveName)
        if preview is not None:
            preview_image = Gtk.Image()
            def dopreview(dialog):
                pixbuf = preview(dialog)
                dialog.set_preview_widget_active(pixbuf is not None)
                if pixbuf is not None:
                    preview_image.set_from_pixbuf(pixbuf)
            dialog.connect("update-preview", dopreview)
            dialog.set_preview_widget(preview_image)
        if filters != None: # was len(filters):
            # filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}}
            for k, f in filters.items():
                filter_in = Gtk.FileFilter()
                filter_in.set_name(k)
                deffilter = False
                for t, v in f.items():
                    if t == "pattern":
                        filter_in.add_pattern(v)
                    elif t == "patterns":
                        for p in v:
                            filter_in.add_pattern(p)
                    elif t == "mime":
                        filter_in.add_mime_type(v)
                    elif t == "default":
                        deffilter = True
                dialog.add_filter(filter_in)
                if deffilter:
                    dialog.set_filter(filter_in)

        response = dialog.run()
        fcFilepath = None
        if response == Gtk.ResponseType.OK:
            if folder or save:
                fcFilepath = [Path(dialog.get_filename()+"/")]
            else:
                fcFilepath = [Path(x) for x in dialog.get_filenames()]
        dialog.destroy()
        return fcFilepath

    def onDiglotClicked(self, btn):
        self.sensiVisible("c_diglot")
        self.sensiVisible("c_borders")
        self.updateHdrFtrOptions(btn.get_active())
        self.colourTabs()
        if self.get("c_diglot"):
            self.diglotView = self.createDiglotView()
        else:
            self.diglotView = None
        self.loadPics()
        self.updatePicList()

    def onDiglotSwitchClicked(self, btn):
        oprjid = None
        oconfig = None
        if self.otherDiglot is not None:
            oprjid, oconfig = self.otherDiglot
            self.otherDiglot = None
            btn.set_label(_("Switch to Other\nDiglot Project"))
        elif self.get("c_diglot"):
            oprjid = self.get("fcb_diglotSecProject")
            oconfig = self.get("ecb_diglotSecConfig")
            if oprjid is not None and oconfig is not None:
                self.otherDiglot = (self.prjid, self.configName())
                btn.set_label(_("Return to\nDiglot Project"))
        if oprjid is not None and oconfig is not None:
            self.set("fcb_project", oprjid)
            self.set("ecb_savedConfig", oconfig)
        
    def updateHdrFtrOptions(self, diglot=False):
        l = ["First Reference", "Last Reference", "Reference Range", "Page Number",
             "Time (HH:MM)", "Date (YYYY-MM-DD)", "DRAFT", "-empty-"]

        for side in ["left", "center", "right"]:
            self.builder.get_object("ecb_hdr"+side).remove_all()
            for i, v in enumerate(l):
                self.builder.get_object("ecb_hdr"+side).append_text(v)
 
        self.builder.get_object("ecb_ftrcenter").remove_all()
        for i, v in enumerate(l[2:]):
            self.builder.get_object("ecb_ftrcenter").append_text(v)

    def onBorderClicked(self, btn):
        self.sensiVisible("c_diglot")
        self.sensiVisible("c_borders")
        self.colourTabs()
        
    def ondiglotSecProjectChanged(self, btn):
        self.updateDiglotConfigList()

    def ondiglotSecConfigChanged(self, btn):
        self.diglotView = self.createDiglotView()
        self.loadPics()
        self.updatePicList()
        
    def onGenerateHyphenationListClicked(self, btn):
        self.generateHyphenationFile()

    def onFindMissingCharsClicked(self, btn_findMissingChars):
        missing = super(GtkViewModel, self).onFindMissingCharsClicked(btn_findMissingChars)
        missingcodes = " ".join(repr(c.encode('raw_unicode_escape'))[2:-1].replace("\\\\","\\") for c in missing)
        self.builder.get_object("t_missingChars").set_tooltip_text(missingcodes)
        if len(missing):
            self.set("c_useFallbackFont", True)
        else:
            self.set("c_useFallbackFont", False)
            self.doError(_("FYI: The Regular font already supports all the characters in the text."),
                    _("A fallback font is not required so\nthe 'Use Fallback Font' option will be disabled."))
        self.sensiVisible("c_useFallbackFont")
        
    def msgQuestion(self, title, question):
        par = self.builder.get_object('ptxprint')
        dialog = Gtk.MessageDialog(parent=par, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.YES_NO, message_format=title)
        dialog.format_secondary_text(question)
        dialog.set_keep_above(True)
        response = dialog.run()
        dialog.set_keep_above(False)
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            return(True)
        elif response == Gtk.ResponseType.NO:
            return(False)

    def onPTXprintDocsDirClicked(self, btn):
        self.openFolder(os.path.join(os.path.dirname(__file__),''))
        
    def onOpenFolderPrjDirClicked(self, btn):
        self.openFolder(os.path.join(self.settings_dir, self.prjid))
        
    def onOpenFolderConfClicked(self, btn):
        self.openFolder(self.configPath(cfgname=self.configName()))
        
    def onOpenFolderOutputClicked(self, btn):
        self.openFolder(self.working_dir)
        
    def openFolder(self, fldrpath):
        path = os.path.realpath(fldrpath)
        os.startfile(fldrpath)

    def finished(self):
        self._incrementProgress(val=0.)

    def _incrementProgress(self, val=None):
        wid = self.builder.get_object("pr_runs")
        if val is None:
            val = wid.get_fraction()
            val = 0.5 if val < 0.1 else 1. - (1. - val) * 0.5
        wid.set_fraction(val)

    def incrementProgress(self):
        GLib.idle_add(self._incrementProgress)

    def onIdle(self, fn, *args):
        GLib.idle_add(fn, *args)

    def showLogFile(self):
        self.builder.get_object("nbk_Main").set_current_page(12)   # Switch to the Viewer tab
        self.builder.get_object("nbk_Viewer").set_current_page(4) # Display the tab with the .log file
        # self.builder.get_object("scroll_XeTeXlog").scroll_to_mark(self.buf[4].get_insert(), 0.0, True, 0.5, 0.5)

    def onTabsClicked(self, btn):
        self.onSimpleClicked(btn)
        self.colourTabs()
        self.onNumTabsChanged()

    def onNumTabsChanged(self, *a):
        if self.get("c_thumbtabs"):
            self.updateThumbLines()
            self.onThumbColourChange()
        self.builder.get_object("l_thumbVerticalL").set_visible(self.get("c_thumbrotate"))
        self.builder.get_object("l_thumbVerticalR").set_visible(self.get("c_thumbrotate"))
        self.builder.get_object("l_thumbHorizontalL").set_visible(not self.get("c_thumbrotate"))
        self.builder.get_object("l_thumbHorizontalR").set_visible(not self.get("c_thumbrotate"))

    def onThumbColourChange(self, *a):
        def coltohex(s):
            vals = s[s.find("(")+1:-1].split(",")
            h = "#"+"".join("{:02x}".format(int(x)) for x in vals)
            return h

        bcol = coltohex(self.get("col_thumbback"))
        fcol = coltohex(self.get("col_thumbtext"))
        bold = "bold" if self.get("c_thumbbold") else "normal"
        ital = "italic" if self.get("c_thumbitalic") else "normal"
        markup = '<span background="{}" foreground="{}" font-weight="{}" font-style="{}">  {{}}  </span>'.format(bcol, fcol, bold, ital)
        for w in ("VerticalL", "VerticalR", "HorizontalL", "HorizontalR"):
            wid = self.builder.get_object("l_thumb"+w)
            wid.set_text(markup.format(w[:-1]))
            wid.set_use_markup(True)

    def onRotateTabsChanged(self, *a):
        orientation = self.get("fcb_rotateTabs")
        self.builder.get_object("l_thumbVerticalL").set_angle(_vertical_thumb[orientation][0])
        self.builder.get_object("l_thumbVerticalR").set_angle(_vertical_thumb[orientation][1])

    def onPLsizeChanged(self, *a):
        size = self.get("fcb_plSize")
        wids = ["l_plHoriz", "fcb_plHoriz"]
        # if size in ["col", "span"]:
        self._updatePgPosOptions(size)
        if size == "span":
            for w in wids:
                self.builder.get_object("fcb_plHoriz").set_active_id("-")
                self.builder.get_object(w).set_sensitive(False)
        else:
            for w in wids:
                self.builder.get_object(w).set_sensitive(True)

    def onPLpgPosChanged(self, *a):
        pgpos = self.get("fcb_plPgPos")
        wids = ["l_plOffsetNum", "s_plLines"]
        if pgpos in ["p", "c"]:
            for w in wids:
                self.builder.get_object(w).set_sensitive(True)
            if pgpos == "p":
                self.builder.get_object("l_plOffsetNum").set_label("Number of\nparagraphs:")
            else:
                self.builder.get_object("l_plOffsetNum").set_label("Number of\nlines:")
        else:
            for w in wids:
                self.builder.get_object(w).set_sensitive(False)
        self._updateHorizOptions(self.get("fcb_plSize"), self.get("fcb_plPgPos"))

    def _updatePgPosOptions(self, size):
        lsp = self.builder.get_object("ls_plPgPos")
        fcb = self.builder.get_object("fcb_plPgPos")
        lsp.clear()
        if size in ["page", "full"]:
            for posn in ["Top", "Center", "Bottom"]:
                lsp.append([posn, "{}{}".format(size[:1].upper(), posn[:1].lower())])
            fcb.set_active(1)
        elif size == "span":
            for posn in ["Top", "Bottom"]:
                lsp.append([posn, _pgpos[posn]])
            fcb.set_active(0)
        else: # size == "col"
            for posn in _pgpos.keys():
                lsp.append([posn, _pgpos[posn]])
            fcb.set_active(0)
        self._updateHorizOptions(size, self.get("fcb_plPgPos"))
 
    def _updateHorizOptions(self, size, pgpos):
        lsp = self.builder.get_object("ls_plHoriz")
        fcb = self.builder.get_object("fcb_plHoriz")
        initVal = self.get("fcb_plHoriz")
        valid = ""
        lsp.clear()
        for horiz in ["Left", "Center", "Right", "Inner", "Outer", "-"]:
            if horiz == "Center" and \
               size not in ["page", "full"] and \
               pgpos not in ["h", "p"]:
               if initVal == "Center":
                    fcb.set_active(0)
               continue
            else:
                valid += _horiz[horiz]
                lsp.append([horiz, _horiz[horiz]])
        if initVal is not None:
            if initVal in valid:
                self.set("fcb_plHoriz", initVal)
            else:
                fcb.set_active(0)
 
    def onPLrowActivated(self, *a):
        self.set("nbk_PicList", 1)

    def onScrSettingsClicked(self, btn):
        script = self.get("fcb_script")
        gclass = getattr(scriptsnippets, script.lower(), None)
        if gclass is None or gclass.dialogstruct is None:
            return
        d = MiniDialog(self, gclass.dialogstruct, f_("{script} Script Settings"))
        response = d.run()
        d.destroy()
        
    def onstyTextPropertiesClicked(self, btn):
        self.onSimpleClicked(btn)

    def onFontStyclicked(self, btn):
        self.getFontNameFace("bl_font_styFontName", noStyles=True)
        self.onFontChanged(btn)
        
    def onColophonClicked(self, btn):
        self.onSimpleClicked(btn)
        if self.get("c_colophon") and self.get("tb_colophon") == "":
            self.set("tb_colophon", _defaultColophon)

    def onColophonResetClicked(self, btn):
        self.set("tb_colophon", _defaultColophon)

    def onResetCopyrightClicked(self, btn):
        self.builder.get_object("t_copyrightStatement").set_text(self._getPtSettings().get('Copyright', ""))

    def onCopyrightStatementChanged(self, btn):
        w = self.builder.get_object("t_copyrightStatement")
        t = w.get_text()
        t = re.sub("</?p>", "", t)
        t = re.sub("\([cC]\)", "\u00a9 ", t)
        w.set_text(t)
        
    def onStyleAdd(self, btn):
        self.styleEditorView.mkrDialog(newkey=True)

    def onStyleEdit(self, btn):
        self.styleEditorView.mkrDialog()

    def onStyleDel(self, btn):
        self.styleEditorView.delKey()

    def onStyleRefresh(self, btn):
        self.styleEditorView.refreshKey()

    def onPlAddClicked(self, btn):
        picroot = os.path.join(self.settings_dir, self.prjid)
        for a in ("figures", "Figures", "FIGURES"):
            picdir = os.path.join(picroot, a)
            if os.path.exists(picdir):
                break
        else:
            picdir = picroot
        def update_preview(dialog):
            picpath = dialog.get_preview_filename()
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(picpath, 200, 300)
            except Exception as e:
                pixbuf = None

            return pixbuf
        picfile = self.fileChooser(_("Choose Image"),
                                  filters={"Images": {"patterns": ['*.tif', '*.png', '*.jpg'], "mime": "application/image"}},
                                   multiple=False, basedir=picdir, preview=update_preview)
        if picfile is not None:
            self.set("nbk_PicList", 1)
            self.picListView.add_row()
            for w in ["t_plAnchor", "t_plFilename", "t_plCaption", "t_plRef", "t_plAltText", "t_plCopyright"]: 
                self.set(w, "")
            self.picListView.set_src(os.path.basename(picfile[0]))

    def onPlDelClicked(self, btn):
        self.picListView.del_row()

    def onAnchorRefChanged(self, t_plAnchor, foo): # called on "focus-out-event"
        # Ensure that the anchor ref only uses . (and not :) as the ch.vs separator
        self.set("t_plAnchor", re.sub(r':', r'.', self.get('t_plAnchor')))

    def resetParam(self, btn, foo):
        label = Gtk.Buildable.get_name(btn.get_child())
        self.styleEditorView.resetParam(label)

    def onPLpageChanged(self, nbk_PicList, scrollObject, pgnum):
        page = nbk_PicList.get_nth_page(pgnum)
        if page == None:
            return
        pgid = Gtk.Buildable.get_name(page)
        if pgid == "pn_checklist":
            self.set("r_image", "preview")

