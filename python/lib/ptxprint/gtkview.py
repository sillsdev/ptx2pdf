#!/usr/bin/python3

import sys, os, re, regex, gi, subprocess, traceback
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from shutil import rmtree
import time, locale

from gi.repository import Gdk, Gtk, Pango, GObject, GLib, GdkPixbuf

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    # sys.stdout = open(os.devnull, "w")
    # sys.stdout = open("D:\Temp\ptxprint-sysout.tmp", "w")
    # sys.stderr = sys.stdout
    pass
else:
    gi.require_version('GtkSource', '3.0')
from gi.repository import GtkSource

import xml.etree.ElementTree as et
from ptxprint.font import TTFont, initFontCache, fccache, FontRef, parseFeatString
from ptxprint.view import ViewModel, Path, VersionStr
from ptxprint.gtkutils import getWidgetVal, setWidgetVal, setFontButton, makeSpinButton
from ptxprint.utils import APP, setup_i18n, brent, xdvigetpages
from ptxprint.ptsettings import ParatextSettings, allbooks, books, bookcodes, chaps
from ptxprint.gtkpiclist import PicList
from ptxprint.piclist import PicChecks, PicInfoUpdateProject
from ptxprint.gtkstyleditor import StyleEditorView
from ptxprint.runjob import isLocked, unlockme
from ptxprint.texmodel import TexModel, ModelMap
from ptxprint.minidialog import MiniDialog
from ptxprint.dbl import UnpackDBL
import ptxprint.scriptsnippets as scriptsnippets
from ptxprint.utils import _, f_, textocol
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
_cjkLangs = {
    "Hang" : "zh",  # "Hangul (Hangŭl, Hangeul)",
    "Hani" : "zh",  # "Han (Hanzi, Kanji, Hanja)",
    "Hano" : "zh",  # "Hanunoo (Hanunóo)",
    "Hans" : "zh",  # "Han (Simplified)",
    "Hant" : "zh",  # "Han (Traditional)"
    "Hrkt" : "ja",  # "Japanese (Hiragana+Katakana)",
    "Jamo" : "ja",  # "Jamo (subset of Hangul)",
    "Jpan" : "ja",  # "Japanese (Han+Hiragana+Katakana)"
    "Kore" : "ko"   # "Korean (Hangul+Han)"

  # "Hanb" : "zh",  # "Han with Bopomofo",
  # "Khmr" : "km",  # "Khmer",
  # "Mymr" : "my",  # "Myanmar (Burmese)"    
  # "Thai" : "th"   # "Thai"
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
        "r_book_single":       ["ecb_book", "l_chapfrom", "s_chapfrom", "l_chapto", "s_chapto"],
        "r_book_multiple":     ["btn_chooseBooks", "t_booklist", "c_combine", "c_autoToC"],
        "r_book_module":       ["btn_chooseBibleModule", "lb_bibleModule"]},
        # "r_book_dbl":          ["btn_chooseDBLbundle", "l_dblBundle"]},
    "c_mainBodyText" :         ["gr_mainBodyText"],
    "c_doublecolumn" :         ["gr_doubleColumn", "c_singleColLayout", "t_singleColBookList"],
    "c_useFallbackFont" :      ["btn_findMissingChars", "t_missingChars", "l_fallbackFont", "bl_fontExtraR"],
    "c_includeFootnotes" :     ["bx_fnOptions"],
    "c_includeXrefs" :         ["bx_xrOptions"],
    "c_includeillustrations" : ["gr_IllustrationOptions"],
    "c_diglot" :               ["gr_diglot", "fcb_diglotPicListSources", "r_hdrLeft_Pri", "r_hdrCenter_Pri", "r_hdrRight_Pri",
                                "r_ftrCenter_Pri", "r_hdrLeft_Sec", "r_hdrCenter_Sec", "r_hdrRight_Sec", "r_ftrCenter_Sec"],
    "c_borders" :              ["gr_borders"],

    "c_pagegutter" :           ["s_pagegutter"],
    "c_verticalrule" :         ["l_colgutteroffset", "s_colgutteroffset"],
    "c_rhrule" :               ["s_rhruleposition"],
    "c_introOutline" :         ["c_prettyIntroOutline"],
    "c_sectionHeads" :         ["c_parallelRefs", "lb_style_s", "lb_style_r"],
    "c_parallelRefs" :         ["lb_style_r"],
    "c_useChapterLabel" :      ["t_clBookList", "l_clHeading", "t_clHeading", "c_optimizePoetryLayout"],
    "c_singleColLayout" :      ["t_singleColBookList"],
    "c_autoToC" :              ["t_tocTitle", "gr_toc", "l_toc"],
    "c_marginalverses" :       ["s_columnShift"],
    "c_hdrverses" :            ["c_sepPeriod", "c_sepColon"],
    "c_fnautocallers" :        ["t_fncallers", "btn_resetFNcallers", "c_fnomitcaller", "c_fnpageresetcallers"],
    "c_xrautocallers" :        ["t_xrcallers", "btn_resetXRcallers", "c_xromitcaller", "c_xrpageresetcallers"],
    "c_glossaryFootnotes" :    ["c_firstOccurenceOnly"],
    "c_useCustomFolder" :      ["btn_selectFigureFolder", "c_exclusiveFiguresFolder", "lb_selectFigureFolder"],
    "c_processScript" :        ["c_processScriptBefore", "c_processScriptAfter", "btn_selectScript", "btn_editScript"],
    "c_usePrintDraftChanges" : ["btn_editChangesFile"],
    "c_useModsTex" :           ["btn_editModsTeX"],
    "c_usePreModsTex" :        ["btn_editModsPreTex"],
    "c_useCustomSty" :         ["btn_editCustomSty"],
    "c_useModsSty" :           ["btn_editModsSty"],
    "c_inclFrontMatter" :      ["btn_selectFrontPDFs"],
    "c_inclBackMatter" :       ["btn_selectBackPDFs"],
    "c_applyWatermark" :       ["btn_selectWatermarkPDF"],
    "c_linebreakon" :          ["t_linebreaklocale"],
    "c_letterSpacing" :        ["s_letterShrink", "s_letterStretch"],
    "c_spacing" :              ["s_minSpace", "s_maxSpace"],
    "c_inclPageBorder" :       ["btn_selectPageBorderPDF", "lb_inclPageBorder", "c_borderPageWide"],
    "c_inclSectionHeader" :    ["btn_selectSectionHeaderPDF", "lb_inclSectionHeader", 
                                "l_inclSectionShift", "l_inclSectionScale", 
                                "s_inclSectionShift", "s_inclSectionScale"],
    "c_inclEndOfBook" :        ["btn_selectEndOfBookPDF", "lb_inclEndOfBook"],
    "c_inclVerseDecorator" :   ["btn_selectVerseDecorator", "lb_inclVerseDecorator", "lb_style_v",
                                "l_verseDecoratorShift", "l_verseDecoratorScale",
                                "s_verseDecoratorShift", "s_verseDecoratorScale"],
    "c_fontFake":              ["s_fontBold", "s_fontItalic", "l_fontBold", "l_fontItalic"],
    "c_thumbtabs":             ["gr_thumbs"],
    "c_thumbrotate":           ["fcb_rotateTabs"],
    "c_colophon":              ["gr_colophon"],
}
# Checkboxes and the different objects they make (in)sensitive when toggled
# These function OPPOSITE to the ones above (they turn OFF/insensitive when the c_box is active)
_nonsensitivities = {
    "c_omitrhchapnum" :        ["c_hdrverses"],
    "c_blendfnxr" :            ["l_internote", "s_internote"],
    "c_useprintdraftfolder" :  ["btn_selectOutputFolder"],
    "c_styFaceSuperscript" :   ["l_styRaise", "s_styRaise"],
}
_object_classes = {
    "printbutton": ("b_print", "btn_refreshFonts"),
    "fontbutton":  ("bl_fontR", "bl_fontB", "bl_fontI", "bl_fontBI"),
    "mainnb":      ("nbk_Main", ),
    "viewernb":    ("nbk_Viewer", "nbk_PicList"),
    "thumbtabs":   ("l_thumbVerticalL", "l_thumbVerticalR", "l_thumbHorizontalL", "l_thumbHorizontalR"),
    "stylinks":    ("lb_style_s", "lb_style_r", "lb_style_v", "lb_style_f", "lb_style_x", 
                    "lb_style_rb", "lb_style_gloss|rb", "lb_style_toc3", "lb_style_x-credit|fig"), 
    "stybutton":   ("btn_reloadConfig", "btn_resetCopyright", "btn_resetColophon", "btn_resetFNcallers", "btn_resetXRcallers", 
                    "btn_styAdd", "btn_styEdit", "btn_styDel", "btn_styReset", "btn_refreshFonts", "btn_resetStyFilter",
                    "btn_plAdd", "btn_plDel", "btn_plGenerate", "btn_plSaveEdits",
                    "btn_adjust_spacing", "btn_adjust_top", "btn_adjust_bottom", )
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

_allcols = ["anchor", "caption", "file", "frame", "scale", "posn", "ref", "mirror", "desc", "copy", "media", "credit", "crrot", "crbox", "crposn"]

_selcols = {
    "settings":  ["anchor", "caption",         "desc"],
    "details":   ["anchor", "caption", "file", "frame", "scale", "posn", "ref", "mirror", "desc", "copy", "media"],
    "checklist": ["anchor", "caption", "file", "desc"]
  # "credits":   [          "caption", "file", "credit", "crrot", "crbox", "crposn"]
}

_defaultColophon = r"""\pc \zcopyright
\pc \zlicense
\b 
\pc \zimagecopyrights
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

_olst = ["fr_SavedConfigSettings", "tb_Layout", "tb_Font", "tb_Body", "tb_NotesRefs", "tb_HeadFoot", "tb_Pictures",
         "tb_Advanced", "tb_Logging", "tb_Tabs", "tb_DiglotBorder", "tb_StyleEditor", "tb_ViewerEditor", "tb_Help"]

def _doError(text, secondary, title, copy2clip=False):
    dialog = Gtk.MessageDialog(parent=None, message_type=Gtk.MessageType.ERROR,
             buttons=Gtk.ButtonsType.OK, text=text)
    if title is None:
        title = "PTXprint Version " + VersionStr
    dialog.set_title(title)
    if copy2clip:
        lines = [title]
        if text is not None and len(text):
            lines.append(text)
        if secondary is not None and len(secondary):
            lines.append(secondary)
        s = "Please send this error message to ptxprint_support@sil.org\n\n{}".format("\n\n".join(lines))
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(s, -1)
        clipboard.store() # keep after app crashed
        if secondary is not None:
            secondary.append("\n\nThe text of this error message has been copied to the clipboard.")
        else:
            secondary = "The text of this error message has been copied to the clipboard."
    if secondary is not None:
        dialog.format_secondary_text(secondary)
    if sys.platform == "win32":
        dialog.set_keep_above(True)
    dialog.run()
    if sys.platform == "win32":
        dialog.set_keep_above(False)
    dialog.destroy()

def getPTDir():
    txt = _('''Paratext is not installed on this system.
Please locate the directory containing your (paratext) project directories. Or cancel to exit''')
    dialog = Gtk.MessageDialog(parent=None, message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK_CANCEL, text=txt)
    response = dialog.run()
    dialog.destroy()
    if response == Gtk.ResponseType.OK:
        action = Gtk.FileChooserAction.SELECT_FOLDER
        btnlabel = "Select"
        fdialog = Gtk.FileChooserDialog("Paratext Projects directory", None,
            (action),
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            (btnlabel), Gtk.ResponseType.OK))
        fdialog.set_default_size(400, 300)
        fdialog.set_select_multiple(False)
        fresponse = fdialog.run()
        fcFilepath = None
        if fresponse == Gtk.ResponseType.OK:
            fcFilepath = Path(fdialog.get_filename()+"/")
        fdialog.destroy()
        return fcFilepath
    else:
        return None

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
            self.builder.add_from_file(gladefile)
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
        self.rtl = False
        self.isDiglotMeasuring = False
        self.printReason = 0
        self.lang = args.lang if args.lang is not None else 'en'
        ilang = self.builder.get_object("fcb_interfaceLang")
        llang = self.builder.get_object("ls_interfaceLang")
        for i, r in enumerate(llang):
            if self.lang.startswith(r[1]):
                ilang.set_active(i)
                break
        for n in _notebooks:
            nbk = self.builder.get_object("nbk_"+n)
            self.notebooks[n] = [Gtk.Buildable.get_name(nbk.get_nth_page(i)) for i in range(nbk.get_n_pages())]
        for fcb in ("interfaceLang", "digits", "script", "diglotPicListSources",
                    "textDirection", "glossaryMarkupStyle", "fontFaces", "featsLangs",
                    "picaccept", "pubusage", "pubaccept", "chklstFilter|0.75"):
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

        for d in ("dlg_multiBookSelector", "dlg_fontChooser", "dlg_password", "dlg_overlayCredit",
                  "dlg_generate", "dlg_styModsdialog", "dlg_DBLbundle", "dlg_features"):
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
            view.set_show_line_numbers(True if i > 1 else False)
            view.pageid = "scroll_"+k
            view.connect("focus-out-event", self.onViewerLostFocus)
            view.connect("focus-in-event", self.onViewerFocus)

        if self.get("c_colophon") and self.get("tb_colophon") == "":
            self.set("tb_colophon", _defaultColophon)

        self.picListView = PicList(self.builder.get_object('tv_picListEdit'), self.builder, self)
        self.styleEditor = StyleEditorView(self)

        self.mw = self.builder.get_object("ptxprint")

        projects = self.builder.get_object("ls_projects")
        digprojects = self.builder.get_object("ls_digprojects")
        projects.clear()
        digprojects.clear()
        allprojects = []
        for d in os.listdir(self.settings_dir):
            p = os.path.join(self.settings_dir, d)
            if not os.path.isdir(p):
                continue
            try:
                if os.path.exists(os.path.join(p, 'Settings.xml')) \
                        or any(x.lower().endswith("sfm") for x in os.listdir(p)):
                    allprojects.append(d)
            except OSError:
                pass
        for p in sorted(allprojects, key = lambda s: s.casefold()):
            projects.append([p])
            digprojects.append([p])
        wide = int(len(allprojects)/16)+1
        self.builder.get_object("fcb_project").set_wrap_width(wide)
        self.builder.get_object("fcb_diglotSecProject").set_wrap_width(wide)
        self.getInitValues()

    def _setup_css(self):
        css = """
            .printbutton:active { background-color: chartreuse; background-image: None }
            .fontbutton {font-size: smaller}
            .stylinks {font-weight: bold; text-decoration: None; padding: 1px 1px}
            .stybutton {font-size: 12px; padding: 4px 6px}
            progress, trough {min-height: 24px}
            .mainnb {background-color: #F0F0F0}
            .mainnb tab {min-height: 0pt; margin: 0pt; padding-bottom: 8pt}
            .viewernb {background-color: #F0F0F0}
            .viewernb tab {min-height: 0pt; margin: 0pt; padding-bottom: 3pt}
            .smradio {font-size: 11px; padding: 1px 1px}
            .changed {font-weight: bold} """
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode("utf-8"))
        Gtk.StyleContext().add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def run(self, callback):
        self.callback = callback
        fc = initFontCache()
        self.initialised = True
        for o in _olst:
            self.builder.get_object(o).set_sensitive(False)
        self.setPrintBtnStatus(1, _("No project set"))
        self.updateDialogTitle()
        if self.pendingPid is not None:
            self.set("fcb_project", self.pendingPid)
            self.pendingPid = None
        if self.pendingConfig is not None:
            self.set("ecb_savedConfig", self.pendingConfig)
            self.pendingConfig = None
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
        sys.excepthook = self.doSysError
        lsfonts = self.builder.get_object("ls_font")
        lsfonts.clear()
        try:
            Gtk.main()
        except Exception as e:
            s = traceback.format_exc()
            s += "\n{}: {}".format(type(e), str(e))
            self.doError(s, copy2clip=True)

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
            _doError(*self.pendingerror)
            self.pendingerror = None
        return True

    def onMainConfigure(self, w, ev, *a):
        if self.picListView is not None:
            self.picListView.onResized()

    def getInitValues(self):
        self.initValues = {v[0]: self.get(v[0], skipmissing=True) for k, v in ModelMap.items() if v[0] is not None}

    def resetToInitValues(self):
        super().resetToInitValues()
        self.rtl = False
        self.picinfos.clear(self)
        for k, v in self.initValues.items():
            if k.startswith("bl_") or v is not None:
                self.set(k, v)
        self._setChapRange("from", 1, 999, 1)
        self._setChapRange("to", 1, 999, 1)
        self.colourTabs()

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
                      
        for c in ("tb_Advanced", "tb_ViewerEditor", "tb_StyleEditor", "tb_Pictures", "tb_Tabs", "tb_DiglotBorder",
                  "fr_copyrightLicense", "r_book_module", "btn_chooseBibleModule", "lb_bibleModule", "c_combine",
                  "c_fighiderefs", "lb_selectFigureFolder", "l_indentUnit", "s_indentUnit", "lb_style_s", "lb_style_r", 
                  "l_btmMrgn", "s_bottommargin", "l_ftrPosn", "s_footerposition", "r_ftrCenter_Pri", "r_ftrCenter_Sec", 
                  "l_missingPictureString", "l_imageTypeOrder", "t_imageTypeOrder", "fr_layoutSpecialBooks", "fr_layoutOther",
                  "s_colgutteroffset", "bx_TopMarginSettings", "gr_HeaderAdvOptions", "l_colgutteroffset",
                  "c_fighiderefs", "c_skipmissingimages", "c_useCustomFolder", "btn_selectFigureFolder", "c_exclusiveFiguresFolder",
                  "c_startOnHalfPage", "c_prettyIntroOutline", "c_marginalverses", "s_columnShift", "c_figplaceholders",
                  "fr_fallbackFont", "l_colgutteroffset", "fr_hyphenation",
                  "bx_fnCallers", "bx_fnCalleeCaller", "bx_xrCallers", "bx_xrCalleeCaller", "c_fnOverride", "c_xrOverride",
                  "row_ToC", "c_hyphenate", "l_missingPictureCount", "bx_colophon", "btn_deleteConfig", "btn_lockunlock",
                  "r_hdrLeft_Pri", "r_hdrLeft_Sec", "r_hdrCenter_Pri", "r_hdrCenter_Sec", "r_hdrRight_Pri", "r_hdrRight_Sec", 
                  "c_omitverseone", "c_glueredupwords", "c_firstParaIndent", "c_hangpoetry", "c_preventwidows", 
                  "btn_unpackDBLbundle", "c_cropmarks", "fr_margins", "c_linebreakon", "t_linebreaklocale", 
                  "c_pagegutter", "s_pagegutter", "l_digits", "fcb_digits", "c_quickRun", "c_mirrorpages",
                  "t_invisiblePassword", "t_configNotes", "l_notes", "c_elipsizeMissingVerses", "fcb_glossaryMarkupStyle",
                  "gr_fnAdvOptions", "c_figexclwebapp", "l_glossaryMarkupStyle", "btn_refreshFonts",
                  "fr_spacingAdj", "fr_fallbackFont", "l_complexScript", "b_scrsettings", "c_colorfonts",
                  "scr_picListEdit", "gr_picButtons", "tb_picPreview", "l_linesOnPageLabel", "l_linesOnPage", 
                  "btn_adjust_spacing", "btn_adjust_top", "btn_adjust_bottom", "fr_diglot", "btn_diglotSwitch", "fr_borders"):
            # print(c)
            self.builder.get_object(c).set_visible(val)

        # Selectively turn things back on if their settings are enabled
        if not val:
            if self.get("c_includeillustrations"):
                self.builder.get_object("tb_Pictures").set_visible(True)
            if self.get("c_thumbtabs"):
                self.builder.get_object("tb_Tabs").set_visible(True)
            if self.get("c_diglot") or self.get("c_borders"):
                self.builder.get_object("tb_DiglotBorder").set_visible(True)
                if self.get("c_diglot"):
                    self.builder.get_object("fr_diglot").set_visible(True)
                    self.builder.get_object("btn_diglotSwitch").set_visible(True)
                if self.get("c_borders"):
                    self.builder.get_object("fr_borders").set_visible(True)

        # Disable/Enable the Details and Checklist tabs on the Pictures tab
        for w in ["tb_details", "tb_checklist"]:
            self.builder.get_object(w).set_sensitive(val)        
        for w in ["tb_plTopPane", "tb_picPreview", "scr_detailsBottom", "scr_checklistBottom", "l_globalPicSettings"]: 
            self.builder.get_object(w).set_visible(val)        
            
        # Show Hide specific Help items
        for pre in ("l_", "lb_"):
            for h in ("ptxprintdir", "prjdir", "settings_dir", "pdfViewer", "techFAQ", "reportBugs"): 
                self.builder.get_object("{}{}".format(pre, h)).set_visible(val)
                
        self.colourTabs()
        # Resize Main UI Window appropriately
        if not val:
            self.mw.resize(828, 292)
        else:
            self.mw.resize(830, 594)

    def addCR(self, name, index):
        if "|" in name:
            name, size = name.split("|")
        else:
            size = None
        v = self.builder.get_object(name)
        setattr(self, name, v)
        c = Gtk.CellRendererText()
        if size is not None:
            width, height = c.get_fixed_size()
            width = float(size) * width
            c.set_fixed_size(width, height)
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

    def doSysError(self, tp, value, tb):
        s = "".join(traceback.format_exception(tp, value, tb))
        self.doError(s, copy2clip=True)

    def doError(self, txt, secondary=None, title=None, threaded=False, copy2clip=False):
        if threaded:
            self.pendingerror=(txt, secondary, title)
        else:
            _doError(txt, secondary, title, copy2clip)

    def doStatus(self, txt=""):
        self.set("l_statusLine", txt)
        
    def setPrintBtnStatus(self, idnty, txt=""):
        if not txt:
            self.printReason &= ~idnty
        else:
            self.printReason |= idnty
        if txt or not self.printReason:
            self.doStatus(txt)
        for w in ["b_print", "btn_adjust_diglot", "s_diglotPriFraction"]:
            self.builder.get_object(w).set_sensitive(not self.printReason)
        
    def onOK(self, btn):
        if isLocked():
            return
        jobs = self.getBooks(files=True)
        if not len(jobs) or jobs[0] == '':
            return
        # If the viewer/editor is open on an Editable tab, then "autosave" contents
        if Gtk.Buildable.get_name(self.builder.get_object("nbk_Main").get_nth_page(self.get("nbk_Main"))) == "tb_ViewerEditor":
            pgnum = self.get("nbk_Viewer")
            if self.notebooks["Viewer"][pgnum] in ("scroll_AdjList", "scroll_Settings"):
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
            s += "\n{}: {}".format(type(e), str(e))
            self.doError(s, copy2clip=True)
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
            # self.doError(_("Can't delete 'Default' configuration!"), secondary=_("Folder: ") + delCfgPath)
            self.resetToInitValues()
            # Note that we may give them an option (later) to delete the entire "Default" including piclists etc.
            # Right now it (only) re-initializes the UI settings.
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
            self.readConfig("Default")
            self.updateDialogTitle()
            self.triggervcs = True
        self.colourTabs()

    def updateBookList(self):
        self.bookNoUpdate = True
        cbbook = self.builder.get_object("ecb_book")
        cbbook.set_model(None)
        lsbooks = self.builder.get_object("ls_books")
        lsbooks.clear()
        # if self.ptsettings is not None:
        bks = self.getAllBooks()
        for b in bks:
            # ind = books.get(b, 0)-1
            # if 0 <= ind <= len(bp) and bp[ind - 1 if ind > 39 else ind] == "1":
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
            for w in v:
                self.builder.get_object(w).set_sensitive(state)
        for k, v in _nonsensitivities.items():
            state = not self.get(k)
            for w in v:
                self.builder.get_object(w).set_sensitive(state)
        self.colourTabs()
        self.updateMarginGraphics()

    def colourTabs(self):
        col = "#688ACC"

        ic = " color='"+col+"'" if self.get("c_includeillustrations") else ""
        self.builder.get_object("lb_Pictures").set_markup("<span{}>".format(ic)+_("Pictures")+"</span>")

        tc = " color='"+col+"'" if self.get("c_thumbtabs") else ""
        self.builder.get_object("lb_Tabs").set_markup("<span{}>".format(tc)+_("Tabs")+"</span>")

        dglt = self.get("c_diglot")
        brdr = self.get("c_borders")
        dc = "<span color='{}'>".format(col)+_("Diglot")+"</span>" if dglt \
            else "Diglot" if self.builder.get_object("fr_diglot").get_visible() else ""
        bc = "<span color='{}'>".format(col)+_("Border")+"</span>" if brdr \
            else "Border" if self.builder.get_object("fr_borders").get_visible() else ""
        jn = "+" if ((dglt and brdr) or self.get("c_hideAdvancedSettings")) else ""
        self.builder.get_object("lb_DiglotBorder").set_markup(dc+jn+bc)

        self.builder.get_object("c_hideAdvancedSettings").set_sensitive(not (dglt and brdr))

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

    def onVertRuleClicked(self, btn):
        self.onSimpleClicked(btn)
        self.updateMarginGraphics()
        
    def on2colClicked(self, btn):
        self.onSimpleClicked(btn)
        self.updateMarginGraphics()
        if self.loadingConfig:
            return
        self.picListView.onRadioChanged()
        val = self.get("s_indentUnit")
        if btn.get_active():
            val = float(val) / 2
        else:
            val = float(val) * 2
        self.set("s_indentUnit", val)

    def onSimpleFocusClicked(self, btn):
        self.sensiVisible(Gtk.Buildable.get_name(btn), focus=True)

    def onCallersClicked(self, btn):
        w1 = Gtk.Buildable.get_name(btn)
        status = self.sensiVisible(w1, focus=True)
        for s in ['omitcaller', 'pageresetcallers']:
            w2 = w1[:4]+s
            self.builder.get_object(w2).set_active(status)

    def onReloadConfigClicked(self, btn_reloadConfig):
        self.updateProjectSettings(self.prjid, configName = self.configName(), readConfig=True)

    def onLockUnlockSavedConfig(self, btn):
        if self.configName() == "Default":
            self.builder.get_object("btn_lockunlock").set_sensitive(False)
            return
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
            lockBtn.set_label(_("Lock"))
        else:
            status = False
            lockBtn.set_label(_("Unlock"))
        for c in ["btn_saveConfig", "btn_deleteConfig", "t_configNotes", "c_hideAdvancedSettings", 
                  "btn_Generate", "btn_plAdd", "btn_plDel"]:
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
        bks2gen = self.getBooks()
        if not len(bks2gen):
            return
        ab = self.getAllBooks()
        bks = bks2gen
        dialog = self.builder.get_object("dlg_generate")
        self.set("l_generate_booklist", " ".join(bks))
        if sys.platform == "win32":
            dialog.set_keep_above(True)
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
                if mode in ("bth", "pri"):
                    PicInfoUpdateProject(self, procbks, ab, self.picinfos,
                                         suffix="L", random=rnd, cols=cols, clearsuffix=(mode != "bth"))
                if mode in ("bth", "sec"):
                    diallbooks = self.diglotView.getAllBooks()
                    PicInfoUpdateProject(self.diglotView, procbks, diallbooks,
                                         self.picinfos, suffix="R", random=rnd, cols=cols, doclear=doclear & (mode != "both"), clearsuffix=(mode != "bth"))
            self.updatePicList(procbks)
            self.savePics()
            self.set("c_filterPicList", False)
        if sys.platform == "win32":
            dialog.set_keep_above(False)
        dialog.hide()

    def onFilterPicListClicked(self, btn):
        self.updatePicList()

    def onGenerateClicked(self, btn):
        priority=self.get("fcb_diglotPicListSources")
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
        elif pgid == "tb_Tabs":
            self.onThumbColourChange()
        # elif pgid == "tb_Pictures":
            # need to get it to hide detail columns

    def onRefreshViewerTextClicked(self, btn):
        pg = self.get("nbk_Viewer")
        self.onViewerChangePage(None, None, pg)

    def onViewerChangePage(self, nbk_Viewer, scrollObject, pgnum):
        allpgids = ("tb_settings", "scroll_AdjList", "scroll_FinalSFM", "scroll_TeXfile",
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
            self.fileViews[pgnum][0].set_text("\n"  +_(" PicLists have been renamed and moved!") + \
                                              "\n"  +_(" Look on the <Pictures> tab for Details & Checklist along the top row.") + \
                                              "\n"*2+_(" A tool to help create Front Matter (the FRT book) may show up here in future."))
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
                fpath = fpath[:doti] + "-" + (self.configName() or "") + fpath[doti:] + fndict[pgid][1]
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
            self.fileViews[pgnum][0].set_text(_("\nThis file doesn't exist yet.\n\nTry clicking... \
                                               \n   * the 'Generate' button \
                                               \n   * the 'Print' button to create the PDF first"))
        self.bookNoUpdate = False

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
        if pg == 1:
            bk = self.get("ecb_examineBook")
            fname = self.getDraftFilename(bk, ext=".adj")
            fdir= os.path.join(self.configPath(self.configName()), "AdjLists")
            os.makedirs(fdir, exist_ok=True)
            fpath = os.path.join(fdir, fname)
        else:
            fpath = self.builder.get_object("l_{1}".format(*pgid.split("_"))).get_tooltip_text()
        if fpath is None: return
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
        if self.loadingConfig:
            return
        self.fcb_digits.set_active_id(self.get('fcb_script'))
        script = self.get("fcb_script")
        if script is not None:
            gclass = getattr(scriptsnippets, script.lower(), None)
        else:
            gclass = None
        if gclass is None or gclass.dialogstruct is None:
            state = False
        else:
            state = True
        for w in ["l_complexScript", "b_scrsettings"]:
            wid = self.builder.get_object(w)
            if wid is not None:
                wid.set_sensitive(state)

        if script not in _cjkLangs.keys():
            self.set("t_linebreaklocale", "")
            self.set("c_linebreakon", False)
        else:
            self.set("t_linebreaklocale", _cjkLangs[script])
            self.set("c_linebreakon", True)

    def onFontChanged(self, fbtn):
        # traceback.print_stack(limit=3)
        super(GtkViewModel, self).onFontChanged(fbtn)
        self.setEntryBoxFont()

    def setEntryBoxFont(self):
        # Set the font of any GtkEntry boxes to the primary body text font for this project
        fsize = self.get("s_fontsize")
        fontr = self.get("bl_fontR", skipmissing=True)
        if fontr is None:
            return
        fallbacks = ['Empties', 'Sans']
        if self.diglotView is not None:
            digfontr = self.diglotView.get("bl_fontR")
            fallbacks.append(digfontr.name)
        pangostr = fontr.asPango(fallbacks, fsize)
        p = Pango.FontDescription(pangostr)
        for w in ("t_clHeading", "t_tocTitle", "t_configNotes", "scroll_FinalSFM", \
                  "ecb_ftrcenter", "ecb_hdrleft", "ecb_hdrcenter", "ecb_hdrright", "t_fncallers", "t_xrcallers", \
                  "l_projectFullName", "t_plCaption", "t_plRef", "t_plAltText", "t_plCopyright", "textv_colophon"):
            self.builder.get_object(w).modify_font(p)
        self.picListView.modify_font(p)

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
    
    def onReverseRadioChanged(self, btn):
        self.onPicRadioChanged(btn)
        self.picChecksView.onReverseRadioChanged()
    
    def onSectionHeadsClicked(self, btn):
        self.onSimpleClicked(btn)
        status = self.sensiVisible("c_sectionHeads")
        self.builder.get_object("c_parallelRefs").set_active(status)

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
        self.onPicRescan(btn)
        
    def onPicRescan(self, btn):
        self.picListView.clearSrcPaths()
        
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

    def onFnBlendClicked(self, btn):
        self.onSimpleClicked(btn)
        try:
            self.styleEditor.setval("x", "NoteBlendInto", "f" if btn.get_active() else None)
        except KeyError:
            return

    def onverseNumbersClicked(self, btn):
        self.onSimpleClicked(btn)
        x = "" if btn.get_active() else "non"
        try:
            self.styleEditor.setval("v", "TextProperties", "{}publishable verse".format(x))
        except KeyError:
            return

    def onDirectionChanged(self, btn, *a):
        rtl = self.get("fcb_textDirection") == "rtl"
        if self.loadingConfig:
            self.rtl = rtl
        if rtl == self.rtl:
            return
        else:
            self.rtl = rtl
        for k in self.styleEditor.allStyles():
            try:
                j = self.styleEditor.getval(k, "Justification")
            except KeyError:
                return
            if j is not None and j.lower() == "right":
                self.styleEditor.setval(k, "Justification", "Left")
            elif j is not None and j.lower() == "left":
                self.styleEditor.setval(k, "Justification", "Right")

    def onEditStyleClicked(self, btn):
        mkr = Gtk.Buildable.get_name(btn)[9:]
        if mkr == "toc3" and self.get("c_thumbIsZthumb"):
            self.set("c_styTextProperties", False)
            mkr = "zthumbtab"
        elif mkr == "x-credit|fig":
            # close the dialog for them
            # MH: This doesn't work yet  FIXME
            dialog = self.builder.get_object("dlg_overlayCredit")
            dialog.set_keep_above(False)
            dialog.hide()
        self.styleEditor.selectMarker(mkr)
        mpgnum = self.notebooks['Main'].index("tb_StyleEditor")
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
            self.picinfos.clearDests()

    def onRefreshFontsclicked(self, btn):
        fc = fccache()
        lsfonts = self.builder.get_object("ls_font")
        fc.fill_liststore(lsfonts)

    def onFontRclicked(self, btn):
        if self.getFontNameFace("bl_fontR"):
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
        if row is not None:
            name = ls.get_value(row, 0)
            initFontCache().fill_cbstore(name, lsstyles)
            self.builder.get_object("fcb_fontFaces").set_active(0)
            self.set("t_fontFeatures", "")

    def responseToDialog(entry, dialog, response):
        dialog.response(response)

    def _getSelectedFont(self):
        lb = self.builder.get_object("tv_fontFamily")
        sel = lb.get_selection()
        ls, row = sel.get_selected()
        name = ls.get_value(row, 0)
        style = self.get("fcb_fontFaces")
        if style.lower() == "regular":
            style = None
        return (name, style)

    def getFontNameFace(self, btnid, noStyles=False, noFeats=False):
        btn = self.builder.get_object(btnid)
        f = self.get(btnid)
        lb = self.builder.get_object("tv_fontFamily")
        ls = lb.get_model()
        fc = initFontCache()
        fc.wait()
        fc.fill_liststore(ls)
        dialog = self.builder.get_object("dlg_fontChooser")
        if f is None:
            i = 0
            isGraphite = False
            feats = ""
            hasfake = False
            embolden = None
            italic = None
            isCtxtSpace = False
        else:
            for i, row in enumerate(ls):
                if row[0] == f.name:
                    break
            else:
                i = 0
            # print(btnid, f, i)
            isGraphite = f.isGraphite
            isCtxtSpace = f.isCtxtSpace
            feats = f.asFeatStr()
            embolden = f.getFake("embolden")
            italic = f.getFake("slant")
            hasfake = embolden is not None or italic is not None
        lb.set_cursor(i)
        lb.scroll_to_cell(i)
        self.builder.get_object("t_fontSearch").set_text("")
        self.builder.get_object("t_fontSearch").has_focus()
        self.builder.get_object("fcb_fontFaces").set_sensitive(not noStyles)
        self.builder.get_object("t_fontFeatures").set_text(feats)
        self.builder.get_object("t_fontFeatures").set_sensitive(not noFeats)
        self.builder.get_object("c_fontGraphite").set_active(isGraphite)
        self.builder.get_object("c_fontCtxtSpaces").set_active(isCtxtSpace)
        self.builder.get_object("s_fontBold").set_value(float(embolden or 0.))
        self.builder.get_object("s_fontItalic").set_value(float(italic or 0.))
        self.builder.get_object("c_fontFake").set_active(hasfake)
        for a in ("Bold", "Italic"):
            self.builder.get_object("s_font"+a).set_sensitive(hasfake)
        # dialog.set_default_response(Gtk.ResponseType.OK)
        dialog.set_keep_above(True)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            (name, style) = self._getSelectedFont()
            if self.get("c_fontFake"):
                bi = (self.get("s_fontBold"), self.get("s_fontItalic"))
            else:
                bi = None
            f = FontRef.fromDialog(name, style, self.get("c_fontGraphite"), 
                                   self.get("c_fontCtxtSpaces"), self.get("t_fontFeatures"), bi)
            self.set(btnid, f)
            res = True
        elif response == Gtk.ResponseType.CANCEL:
            res = False
        dialog.set_keep_above(False)
        dialog.hide()
        return res

    def onFontFeaturesClicked(self, btn):
        (name, style) = self._getSelectedFont()
        f = TTFont(name, style)
        if f is None:
            return
        isGraphite = self.get("c_fontGraphite")
        dialog = self.builder.get_object("dlg_features")
        featbox = self.builder.get_object("box_featsFeatures")
        lslangs = self.builder.get_object("ls_featsLangs")
        if isGraphite:
            feats = f.feats
            vals = f.featvals
            langs = f.grLangs
            self.currdefaults = f.featdefaults
            langfeats = f.langfeats
        else:
            feats = f.otFeats
            vals = f.otVals
            langs = f.otLangs
            self.currdefaults = {}
            langfeats = {}
        numrows = len(feats)
        (lang, setfeats) = parseFeatString(self.get("t_fontFeatures"), defaults=self.currdefaults, langfeats=langfeats)
        for i, (k, v) in enumerate(sorted(feats.items())):
            featbox.insert_row(i)
            l = Gtk.Label(label=v+":")
            l.set_halign(Gtk.Align.END)
            featbox.attach(l, 0, i, 1, 1)
            l.show()
            inival = int(setfeats.get(k, "0"))
            if k in vals:
                if len(vals[k]) < 3:
                    obj = Gtk.CheckButton()
                    obj.set_tooltip_text(vals[k][1])
                    obj.set_active(inival)
                else:
                    obj = Gtk.ComboBoxText()
                    for j, n in sorted(vals[k].items()):
                        obj.append(str(j), n)
                    obj.set_active(inival)
                    obj.set_entry_text_column(1)
            elif k == "aalt":
                obj = makeSpinButton(0, 100, 0)
                obj.set_value(inival)
            else:
                obj = Gtk.CheckButton()
                obj.set_active(inival)
            obj.set_halign(Gtk.Align.START)
            featbox.attach(obj, 1, i, 1, 1)
            obj.show()
        lslangs.clear()
        for k, v in sorted(langs.items()):
            lslangs.append([v, k])
        if lang is not None:
            self.set("fcb_featsLangs", lang)
        def onLangChanged(fcb):
            newlang = self.get("fcb_featsLangs")
            newdefaults = langfeats.get(newlang, self.currdefaults)
            print("New defaults for lang {}: {}".format(newlang, newdefaults))
            for i, (k, v) in enumerate(sorted(feats.items())):
                if newdefaults.get(k, 0) == self.currdefaults.get(k, 0):
                    continue
                obj = featbox.get_child_at(1, i)
                print("Changing feature {} in lang {}".format(k, newlang))
                if isinstance(obj, Gtk.CheckButton):
                    if (1 if obj.get_active() else 0) == self.currdefaults.get(k, 0):
                        obj.set_active(newdefaults.get(k, 0) == 1)
                elif isinstnace(obj, GtkSpinButton):
                    if obj.get_value() == self.currdefaults.get(k, 0):
                        obj.set_value(newdefaults.get(k, 0))
                elif isinstance(obj, Gtk.ComboBoxText):
                    if obj.get_active_id() == self.currdefaults.get(k, 0):
                        ob.set_active_id(newdefaults.get(k, 0))
            self.currdefaults = newdefaults
        langChangedId = self.builder.get_object("fcb_featsLangs").connect("changed", onLangChanged)
        dialog.set_keep_above(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            results = []
            lang = self.get("fcb_featsLangs")
            if lang is not None:
                results.append("language="+lang)
                self.currdefaults = langfeats.get(lang, self.currdefaults)
            for i, (k, v) in enumerate(sorted(feats.items())):
                obj = featbox.get_child_at(1, i)
                if isinstance(obj, Gtk.CheckButton):
                    val = 1 if obj.get_active() else 0
                elif isinstance(obj, Gtk.SpinButton):
                    val = int(obj.get_value())
                elif isinstance(obj, Gtk.ComboBoxText):
                    val = obj.get_active_id()
                if val is not None and ((self.currdefaults is not None and str(self.currdefaults.get(k, 0)) != str(val))\
                                        or (self.currdefaults is None and str(val) != "0")):
                    results.append("{}={}".format(k, val))
            self.set("t_fontFeatures", ", ".join(results))
        for i in range(numrows-1, -1, -1):
            featbox.remove_row(i)
        self.builder.get_object("fcb_featsLangs").disconnect(langChangedId)
        dialog.set_keep_above(False)
        dialog.hide()

    def onFontIsGraphiteClicked(self, btn):
        self.onSimpleClicked(btn)
        self.set("t_fontFeatures", "")

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
            self.set("c_usetoc1", True)
        if self.get("c_autoToC"):
            if self.get("c_thumbtabs"):
                if not self.get("c_usetoc3"):
                    self.set("c_thumbIsZthumb", True)
                self.builder.get_object("c_thumbIsZthumb").set_sensitive(self.get("c_usetoc3"))
        else:
            self.builder.get_object("c_thumbIsZthumb").set_sensitive(True)
        
        
    def _setChapRange(self, fromTo, minimum, maximum, value):
        initChap = int(float(self.get('s_chap'+fromTo)))
        chap = self.builder.get_object('s_chap'+fromTo)
        chap.set_range(minimum, maximum)
        if value:
            chap.set_value(value if value in range(minimum, maximum) else (minimum if fromTo == "from" else maximum))
        else:
            chap.set_value(initChap if initChap in range(minimum, maximum) else (minimum if fromTo == "from" else maximum))

    def onBookChange(self, cb_book):
        bk = self.get("ecb_book")
        if bk == "NON":
            self.set("ecb_book", "")
            return
        if bk is not None and bk != "":
            chs = int(chaps.get(str(bk), 999))
            if self.loadingConfig:
                self.set("r_book", "single")
                self._setChapRange("from", 1, chs, int(float(self.get("s_chapfrom"))))
                self._setChapRange("to", 1, chs, int(float(self.get("s_chapto"))))
            else:
                self._setChapRange("from", 1, chs, 1)
                self._setChapRange("to", 1, chs, chs)
            self.updateExamineBook()
        self.updateDialogTitle()
        self.updatePicList()

    def onChapChg(self, btn):
        if self.loadingConfig:
            return
        bk = self.get("ecb_book")
        if bk != "":
            self.set("r_book", "single")
            chs = int(chaps.get(str(bk), 999))
            strt = int(float(self.get("s_chapfrom")))
            self._setChapRange("to", strt, chs, 0)

    def _setNoteSpacingRange(self, fromTo, minimum, maximum, value):
        initSpace = int(float(self.get('s_notespacing'+fromTo)))
        spacing = self.builder.get_object('s_notespacing'+fromTo)
        spacing.set_range(minimum, maximum)
        if value:
            spacing.set_value(value if value in range(minimum, maximum) else (minimum if fromTo == "min" else maximum))
        else:
            spacing.set_value(initSpace if initSpace in range(minimum, maximum) else (minimum if fromTo == "min" else initSpace + 4))

    def onNoteSpacingChanged(self, btn):
        if self.loadingConfig:
            return
        strt = int(float(self.get("s_notespacingmin"))) + 4
        self._setNoteSpacingRange("max", strt, 40, 0)

    def onstyColorSet(self, btn):
        def coltohex(s):
            vals = s[s.find("(")+1:-1].split(",")
            h = "#"+"".join("{:02x}".format(int(x)) for x in vals)
            return h
        col = coltohex(self.get("col_styColor"))
        self.set("l_styColorValue", col)
        if col != "x000000" and not self.get("c_colorfonts"):
            self.set("c_colorfonts", True)
            self.doError(_("'Enable Colored Text' has now been turned on.\nSee Fonts+Script tab for details."))

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
        if not self.initialised:
            return
        self.updatePrjLinks()
        self.builder.get_object("btn_saveConfig").set_sensitive(True)
        # self.builder.get_object("btn_deleteConfig").set_sensitive(False)
        lockBtn = self.builder.get_object("btn_lockunlock")
        lockBtn.set_label("Lock")
        lockBtn.set_sensitive(False)
        self.updateProjectSettings(None, saveCurrConfig=True, configName="Default")
        self.updateSavedConfigList()
        for o in _olst:
            self.builder.get_object(o).set_sensitive(True)
        self.setPrintBtnStatus(1)
        self.updateFonts()
        # self.updateHdrFtrOptions(self.get("c_diglot"))
        if self.ptsettings is not None:
            self.builder.get_object("l_projectFullName").set_label(self.ptsettings.get('FullName', ""))
            self.builder.get_object("l_projectFullName").set_tooltip_text(self.ptsettings.get('Copyright', ""))
        else:
            self.builder.get_object("l_projectFullName").set_label("")
            self.builder.get_object("l_projectFullName").set_tooltip_text("")
        pts = self._getPtSettings()
        if pts is not None and self.get("t_copyrightStatement") == "":
            self.builder.get_object("t_copyrightStatement").set_text(pts.get('Copyright', ""))

    def updatePrjLinks(self):
        if self.settings_dir != None and self.prjid != None:
            self.builder.get_object("lb_ptxprintdir").set_label(os.path.dirname(__file__))
            self.builder.get_object("lb_prjdir").set_label(os.path.join(self.settings_dir, self.prjid))
            self.builder.get_object("lb_settings_dir").set_label(self.configPath(cfgname=self.configName()) or "")
            self.builder.get_object("lb_working_dir").set_label(self.working_dir or "")
            
    def updateProjectSettings(self, prjid, saveCurrConfig=False, configName=None, readConfig=False):
        self.picListView.clear()
        if self.picinfos is not None:
            self.picinfos.clear()
        if not super(GtkViewModel, self).updateProjectSettings(prjid, saveCurrConfig=saveCurrConfig, configName=configName, readConfig=readConfig):
            for fb in ['bl_fontR', 'bl_fontB', 'bl_fontI', 'bl_fontBI', 'bl_fontExtraR']:
                fblabel = self.builder.get_object(fb).set_label("Select font...")
        if self.prjid:
            self.updatePrjLinks()
            self.userconfig.set("init", "project", self.prjid)
            if getattr(self, 'configId', None) is not None:
                self.userconfig.set("init", "config", self.configId)
        # self.updateBookList()
        books = self.getBooks()
        if books is None or not len(books):
            books = self.getAllBooks()
            for b in allbooks:
                if b in books:
                    self.set("ecb_book", b)
                    self.set("r_book", "single")
                    break
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
        self.styleEditor.editMarker()
        self.updateMarginGraphics()
        self.onBodyHeightChanged(None)

    def onConfigNameChanged(self, cb_savedConfig):
        lockBtn = self.builder.get_object("btn_lockunlock")
        if self.configName() == "Default":
            lockBtn.set_sensitive(False)
        if self.configNoUpdate or self.get("ecb_savedConfig") == "":
            return
        self.builder.get_object("c_hideAdvancedSettings").set_sensitive(True)
        lockBtn.set_label("Lock")
        self.builder.get_object("t_invisiblePassword").set_text("")
        self.builder.get_object("btn_saveConfig").set_sensitive(True)
        self.builder.get_object("btn_deleteConfig").set_sensitive(True)
        if len(self.get("ecb_savedConfig")):
            if self.configName() != "Default":
                lockBtn.set_sensitive(True)
        else:
            self.builder.get_object("t_configNotes").set_text("")
            lockBtn.set_sensitive(False)
        cpath = self.configPath(cfgname=self.configName(), makePath=False)
        if cpath is not None and os.path.exists(cpath):
            self.updateProjectSettings(self.prjid, saveCurrConfig=False, configName=self.configName()) # False means DON'T Save!
        self.updateDialogTitle()

    def updateFonts(self):
        if self.ptsettings is None:
            return
        ptfont = self.get("bl_fontR", skipmissing=True)
        if ptfont is None:
            ptfont = FontRef(self.ptsettings.get("DefaultFont", "Arial"), "")
            self.set('bl_fontR', ptfont)
            self.onFontChanged(None)

    def updateDialogTitle(self):
        titleStr = super(GtkViewModel, self).getDialogTitle()
        self.builder.get_object("ptxprint").set_title(titleStr)

    def _locFile(self, file2edit, loc, fallback=False):
        fpath = None
        self.prjdir = os.path.join(self.settings_dir, self.prjid)
        if loc == "wrk":
            fpath = os.path.join(self.working_dir, file2edit)
        elif loc == "prj":
            fpath = os.path.join(self.settings_dir, self.prjid, file2edit)
        elif loc == "cfg":
            cfgname = self.configName()
            fpath = os.path.join(self.configPath(cfgname), file2edit)
            if fallback and not os.path.exists(fpath):
                fpath = os.path.join(self.configPath(""), file2edit)
        elif "\\" in loc or "/" in loc:
            fpath = os.path.join(loc, file2edit)
        return fpath

    def editFile(self, file2edit, loc="wrk", pgid="scroll_Settings", switch=None): # keep param order
        if switch is None:
            switch = pgid == "scroll_Settings"
        pgnum = self.notebooks["Viewer"].index(pgid)
        mpgnum = self.notebooks["Main"].index("tb_ViewerEditor")
        if switch:
            self.builder.get_object("nbk_Main").set_current_page(mpgnum)
            self.builder.get_object("nbk_Viewer").set_current_page(pgnum)
        # self.prjid = self.get("fcb_project")
        fpath = self._locFile(file2edit, loc)
        if fpath is None:
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

    def _editProcFile(self, fname, loc, intro=""):
        fpath = self._locFile(fname, loc)
        if intro != "" and not os.path.exists(fpath):
            openfile = open(fpath,"w", encoding="utf-8")
            openfile.write(intro)
            openfile.close()
        self.editFile(fname, loc)

    def onEditScriptFile(self, btn):
        customScriptFPath = self.get("btn_selectScript")
        scriptName = os.path.basename(customScriptFPath)
        scriptPath = customScriptFPath[:-len(scriptName)]
        if len(customScriptFPath):
            self._editProcFile(scriptName, scriptPath)

    def onEditChangesFile(self, btn):
        self._editProcFile("PrintDraftChanges.txt", "prj")

    def onEditModsTeX(self, btn):
        cfgname = self.configName()
        self._editProcFile("ptxprint-mods.tex", "cfg",
            intro=_(_("""% This is the .tex file specific for the {} project used by PTXprint.
% Saved Configuration name: {}
""").format(self.prjid, cfgname)))

    def onEditPreModsTeX(self, btn):
        cfgname = self.configName()
        self._editProcFile("ptxprint-premods.tex", "cfg",
            intro=_(_("""% This is the preprocessing .tex file specific for the {} project used by PTXprint.
% Saved Configuration name: {}
""").format(self.prjid, cfgname)))

    def onEditCustomSty(self, btn):
        self.editFile("custom.sty", "prj")

    def onEditModsSty(self, btn):
        self.editFile("ptxprint-mods.sty", "cfg")

    def onExtraFileClicked(self, btn):
        self.onSimpleClicked(btn)
        if btn.get_active():
            self.triggervcs = True

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
            try:
                self.createArchive(str(archiveZipFile[0]))
            except Exception as e:
                s = traceback.format_exc()
                s += "\n{}: {}".format(type(e), str(e))
                self.doError(s, copy2clip=True)
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
            moduleFile = [Path(os.path.relpath(x, prjdir)) for x in moduleFile]
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
        # self.updateHdrFtrOptions(btn.get_active())
        self.colourTabs()
        if self.loadingConfig:
            return
        if self.get("c_diglot"):
            self.diglotView = self.createDiglotView()
        else:
            self.setPrintBtnStatus(2)
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
            # self.set("c_diglot", True)
            # self.builder.get_object("c_diglot").set_sensitive(True)
        elif self.get("c_diglot"):
            oprjid = self.get("fcb_diglotSecProject")
            oconfig = self.get("ecb_diglotSecConfig")
            if oprjid is not None and oconfig is not None:
                self.otherDiglot = (self.prjid, self.configName())
                # self.set("c_diglot", False)
                # self.builder.get_object("c_diglot").set_sensitive(False)
                btn.set_label(_("Save & Return to\nDiglot Project"))
        self.onSaveConfig(None)
        if oprjid is not None and oconfig is not None:
            self.set("fcb_project", oprjid)
            self.set("ecb_savedConfig", oconfig)
        mpgnum = self.notebooks['Main'].index("tb_DiglotBorder")
        self.builder.get_object("nbk_Main").set_current_page(mpgnum)
        
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
        if self.loadingConfig:
            return
        if self.get("c_diglot"):
            self.diglotView = self.createDiglotView()
        else:
            self.setPrintBtnStatus(2)
            self.diglotView = None
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
        GLib.idle_add(lambda: self._incrementProgress(val=0.))

    def _incrementProgress(self, val=None):
        wid = self.builder.get_object("pr_runs")
        if val is None:
            val = wid.get_fraction()
            val = 0.25 if val < 0.1 else 1. - (1. - val) * 0.5
        wid.set_fraction(val)

    def incrementProgress(self):
        GLib.idle_add(self._incrementProgress)

    def onIdle(self, fn, *args):
        GLib.idle_add(fn, *args)

    def showLogFile(self):
        mpgnum = self.notebooks['Main'].index("tb_ViewerEditor")
        self.builder.get_object("nbk_Main").set_current_page(mpgnum)
        vpgnum = self.notebooks['Viewer'].index("scroll_XeTeXlog")
        self.builder.get_object("nbk_Viewer").set_current_page(vpgnum)
        # self.onViewerFocus(self, w) # @@@@ MH please FIXME
        # self.builder.get_object("scroll_XeTeXlog").scroll_to_mark(self.buf[4].get_insert(), 0.0, True, 0.5, 0.5)

    def onTabsClicked(self, btn):
        self.onSimpleClicked(btn)
        self.colourTabs()
        self.onNumTabsChanged()
        if self.get("c_thumbtabs"):
            if not self.get("c_usetoc3"):
                self.set("c_thumbIsZthumb", True)
            self.builder.get_object("c_thumbIsZthumb").set_sensitive(self.get("c_usetoc3"))

    def onNumTabsChanged(self, *a):
        if not super().onNumTabsChanged(*a):
            return
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
        self.set("l_thumbbackValue", bcol)
        tabstyle = "zthumbtab" if self.get("c_thumbIsZthumb") else "toc3"
        fcol = coltohex(textocol(self.styleEditor.getval(tabstyle, "color")))
        bold = "bold" if self.styleEditor.getval(tabstyle, "bold") == "" else "normal"
        ital = "italic" if self.styleEditor.getval(tabstyle, "italic") == "" else "normal"
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
        
    def onColophonClicked(self, btn):
        self.onSimpleClicked(btn)
        if self.get("c_colophon") and self.get("tb_colophon") == "":
            self.set("tb_colophon", _defaultColophon)

    def onColophonResetClicked(self, btn):
        self.set("tb_colophon", _defaultColophon)

    def onResetCopyrightClicked(self, btn):
        self.builder.get_object("t_copyrightStatement").set_text(self._getPtSettings().get('Copyright', ""))

    def onCopyrightStatementChanged(self, btn):
        btname = Gtk.Buildable.get_name(btn)
        w = self.builder.get_object(btname)
        t = w.get_text()
        t = re.sub("</?p>", "", t)
        t = re.sub("\([cC]\)", "\u00a9 ", t)
        if btname == 't_plCreditText':
            if self.get('c_sensitive'):
                t = re.sub(r"(?i)dcc", "\u00a9 DCC", t)
            else:
                t = re.sub(r"(?i)dcc", "\u00a9 David C Cook", t)
        w.set_text(t)
        
    def onStyleAdd(self, btn):
        self.styleEditor.mkrDialog(newkey=True)

    def onStyleEdit(self, btn):
        self.styleEditor.mkrDialog()

    def onStyleDel(self, btn):
        self.styleEditor.delKey()

    def onStyleRefresh(self, btn):
        self.styleEditor.refreshKey()

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
        # Ensure that the anchor ref only uses . (and not :) as the ch.vs separator and is upperCASE
        self.set("t_plAnchor", re.sub(r':', r'.', self.get('t_plAnchor').upper()))

    def resetParam(self, btn, foo):
        label = Gtk.Buildable.get_name(btn.get_child())
        self.styleEditor.resetParam(label)

    def onPLpageChanged(self, nbk_PicList, scrollObject, pgnum):
        page = nbk_PicList.get_nth_page(pgnum)
        if page == None:
            return
        pgid = Gtk.Buildable.get_name(page).split('_')[-1]
        filterSensitive = True if pgid == "checklist" else False
        self.builder.get_object("fr_plChecklistFilter").set_sensitive(filterSensitive)
        for w in _allcols:
            if w in _selcols[pgid]:
                self.builder.get_object("col_{}".format(w)).set_visible(True)
            else:
                self.builder.get_object("col_{}".format(w)).set_visible(False)

        # Ask MH: @@@@
        # if pgid in ["settings", "checklist", "credits"]:
            # self.builder.get_object("scr_picListEdit").set_policy(None, GTK_POLICY_NEVER, GTK_POLICY_ALWAYS)

        # See: https://stackoverflow.com/questions/50414957/gtk3-0-scrollbar-on-treeview-scrolledwindow-css-properties-to-control-scrol
        # set_policy(GTK_SCROLLED_WINDOW(scwin), GTK_POLICY_AUTOMATIC,GTK_POLICY_ALWAYS)
        
        # sw = gtk_scrolled_window_new(NULL, NULL);
        # gtk_container_set_border_width( GTK_CONTAINER(sw), 0 );
        # gtk_scrolled_window_set_policy( GTK_SCROLLED_WINDOW(sw), GTK_POLICY_NEVER, GTK_POLICY_ALWAYS ); //scroll bars
        # //Set scrollbar to ALWAYS be displayed and not as temporary overlay
        # g_object_set( sw , "overlay-scrolling", FALSE , NULL);

    def onUnpackDBLbundleClicked(self, btn):
        dialog = self.builder.get_object("dlg_DBLbundle")
        response = dialog.run()
        if response == Gtk.ResponseType.OK and self.builder.get_object("btn_chooseDBLbundle").get_sensitive:
            prj = self.get("t_DBLprojName")
            if prj != "":
                UnpackDBL(self.DBLfile, prj, self.settings_dir)
                # add prj to ls_project before selecting it.
                lsp = self.builder.get_object("ls_projects")
                allprojects = [x[0] for x in lsp]
                for i, p in enumerate(allprojects):
                    if prj.casefold() > p.casefold():
                        lsp.insert(i, [prj])
                        break
                self.set("fcb_project", prj)
        dialog.hide()

    def onChooseDBLbundleClicked(self, btn):
        prjdir = os.path.join(self.settings_dir, self.prjid)
        DBLfile = self.fileChooser("Select a DBL Bundle file", 
                filters = {"DBL Bundles": {"patterns": ["*.zip"] , "mime": "text/plain", "default": True},
                           "All Files": {"pattern": "*"}},
                multiple = False, basedir=os.path.join(prjdir, "Bundles"))
        if DBLfile is not None:
            # DBLfile = [x.relative_to(prjdir) for x in DBLfile]
            self.DBLfile = DBLfile[0]
            self.builder.get_object("lb_DBLbundleFilename").set_label(os.path.basename(DBLfile[0]))
            self.builder.get_object("btn_chooseDBLbundle").set_tooltip_text(str(DBLfile[0]))
        else:
            self.builder.get_object("lb_DBLbundleFilename").set_label("")
            self.DBLfile = None
            self.builder.get_object("btn_chooseDBLbundle").set_tooltip_text("")
    
    def onDBLprojNameChanged(self, widget):
        text = self.get("t_DBLprojName")
        btn = self.builder.get_object("btn_chooseDBLbundle")
        lsp = self.builder.get_object("ls_projects")
        allprojects = [x[0] for x in lsp]
        btn.set_sensitive(not text in allprojects)

    def onParagraphednotesClicked(self, btn):
        status = not (self.get("c_fneachnewline") and self.get("c_xreachnewline"))
        for w in ["l_paragraphedNotes", "s_notespacingmin", "s_notespacingmax", "l_min", "l_max"]:
            wid = self.builder.get_object(w)
            if wid is not None:
                wid.set_sensitive(status)

    def oninterfaceLangChanged(self, btn):
        if self.initialised:
            lang = self.get("fcb_interfaceLang")
            try:
                setup_i18n(lang)
            except locale.Error:
                self.doError(_("Unsupported Locale"),
                             secondary=_("This locale is not supported on your system, you may need to install it"))
                return
            self.lang = lang
            self.builder.get_object("ptxprint").destroy()
            self.onDestroy(None)
            
    def onRHruleClicked(self, btn):
        status = self.get("c_rhrule")
        self.updateMarginGraphics()
        for w in ["l_rhruleoffset", "s_rhruleposition"]:
            self.builder.get_object(w).set_visible(status)        
            self.builder.get_object(w).set_sensitive(status)        

    def _calcBodyHeight(self):
        linespacing = float(self.get("s_linespacing")) * 25.4 / 72.27
        unitConv = {'mm':1, 'cm':10, 'in':25.4, '"':25.4}
        m = re.match(r"^.*?,\s*([\d.]+)(\S+)\s*(?:.*|$)", self.get("ecb_pagesize"))
        if m:
            pageheight = float(m.group(1)) * unitConv.get(m.group(2), 1)
        else:
            pageheight = 210
        bottommargin = float(self.get("s_bottommargin"))
        topmargin = float(self.get("s_topmargin"))
        font = self.get("bl_fontR")
        if font is not None:
            tt = font.getTtfont()
            if tt is not None:
                ttadj = tt.descent / tt.upem * float(self.get("s_fontsize")) * 25.4 / 72.27
                bottommargin -= ttadj
        return (pageheight - bottommargin - topmargin, linespacing)

    def onBodyHeightChanged(self, btn):
        textheight, linespacing = self._calcBodyHeight()
        lines = textheight / linespacing
        self.set("l_linesOnPage", "{:.1f}".format(lines))
        self.setMagicAdjustSensitive(int(lines) != lines)
        
    def onMagicAdjustClicked(self, btn):
        param = Gtk.Buildable.get_name(btn).split("_")[-1]
        textheight, linespacing = self._calcBodyHeight()
        lines = textheight / linespacing
        extra = int(lines) - lines
        if extra < -0.5:
            extra += 1.
            lines += 1
        extra *= linespacing
        
        if param == "spacing":
            l = float(self.get("s_linespacing"))
            l -= (extra * 72.27 / 25.4) / (int(lines))
            self.set("s_linespacing", l)
        elif param == "top":
            self.set("s_topmargin", float(self.get("s_topmargin")) - extra)
            
        elif param == "bottom":
            self.set("s_bottommargin", float(self.get("s_bottommargin")) - extra)
        else:
            print("Oops! No more Magic Adjust options...")
        self.set("l_linesOnPage", "{:.1f}".format(int(lines)))
        self.setMagicAdjustSensitive(False)
            
    def setMagicAdjustSensitive(self, clickable=False):
        btns = ["spacing", "top", "bottom"]
        for w in btns:
            self.builder.get_object("btn_adjust_{}".format(w)).set_sensitive(clickable)
    
    def updateMarginGraphics(self):
        cols = 2 if self.get("c_doublecolumn") else 1
        vert = self.get("c_verticalrule")
        horiz = self.get("c_rhrule")
        top = re.sub("1True", "1False", "{}{}{}".format(cols,vert,horiz))
        bottom = re.sub("1True", "1False", "{}{}".format(cols,vert))
        for t in ["1FalseFalse", "1FalseTrue", "2FalseFalse", "2FalseTrue", "2TrueFalse", "2TrueTrue"]:
            self.builder.get_object("img_Top{}".format(t)).set_visible(t == top)        
        for b in ["1False", "2False", "2True"]:
            self.builder.get_object("img_Bottom{}".format(b)).set_visible(b == bottom)        

    def onOverlayCreditClicked(self, btn):
        dialog = self.builder.get_object("dlg_overlayCredit")
        dialog.set_keep_above(True)
        crParams = self.get("t_piccreditbox")
        m = re.match(r"^([tcb]?)([lrcio]?),(-?9?0?|None),(\w*)", crParams)
        if m:
            self.set("fcb_plCreditVpos", m[0])
            self.set("fcb_plCreditHpos", m[1])
            self.set("fcb_plCreditRotate", m[2])
            self.set("ecb_plCreditBoxStyle", m[3])
        self.set("t_piccredit", self.get("l_piccredit"))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            vpos = self.get("fcb_plCreditVpos")
            hpos = self.get("fcb_plCreditHpos")
            rota = self.get("fcb_plCreditRotate")
            bbox = self.get("ecb_plCreditBoxStyle")
            text = self.get("t_plCreditText")
            crParams = "{}{},{},{}".format(vpos, hpos, (rota if rota is not None else "0"), bbox)
            self.set("t_piccreditbox", crParams)
            self.set("l_piccredit", text)
        elif response == Gtk.ResponseType.CANCEL:
            pass
        else:
            return
        dialog.set_keep_above(False)
        dialog.hide()

    def onDiglotAutoAdjust(self, btn):
        if self.isDiglotMeasuring:
            btn.set_active(True)
            return
        elif not self.get("c_diglot"):
            btn.set_active(False)
            return
        elif not btn.get_active():
            return
        self.isDiglotMeasuring = True
        btn.set_active(True)
        xdvname = os.path.join(self.working_dir, self.baseTeXPDFnames()[0] + ".xdv")
        def score(x):
            self.set("s_diglotPriFraction", x*100)
            runjob = self.callback(self, maxruns=1, noview=True)
            while runjob.thread.is_alive():
                Gtk.main_iteration_do(False)
            runres = runjob.res
            return None if runres else xdvigetpages(xdvname)
        mid = float(self.get("s_diglotPriFraction")) / 100.
        res = brent(0., 1., mid, score, 0.001)
        self.set("s_diglotPriFraction", res*100)
        self.isDiglotMeasuring = False
        btn.set_active(False)

    def onDiglotSwapSideClicked(self, btn):
        if self.get("r_hdrLeft") != self.get("r_hdrRight"):
            for a in ("r_hdrLeft", "r_hdrRight"):
                v = self.get(a)
                v = "Sec" if v == "Pri" else ("Pri" if v == "Sec" else v)
                self.set(a, v)    

