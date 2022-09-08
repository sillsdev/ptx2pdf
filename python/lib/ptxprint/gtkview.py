#!/usr/bin/python3

import sys, os, re, regex, gi, subprocess, traceback, ssl
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Poppler', '0.18')
from shutil import rmtree
import time, locale, urllib.request, json
from ptxprint.utils import universalopen, refKey, chgsHeader
from gi.repository import Gdk, Gtk, Pango, GObject, GLib, GdkPixbuf

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    # sys.stdout = open(os.devnull, "w")
    # sys.stdout = open("D:\Temp\ptxprint-sysout.tmp", "w")
    # sys.stderr = sys.stdout
    pass
else:
    gi.require_version('GtkSource', '3.0')
from gi.repository import GtkSource, Poppler
import cairo

import xml.etree.ElementTree as et
from ptxprint.font import TTFont, initFontCache, fccache, FontRef, parseFeatString
from ptxprint.view import ViewModel, Path, VersionStr, GitVersionStr
from ptxprint.gtkutils import getWidgetVal, setWidgetVal, setFontButton, makeSpinButton
from ptxprint.utils import APP, setup_i18n, brent, xdvigetpages, allbooks, books, bookcodes, chaps, print_traceback, pycodedir, getcaller, runChanges
from ptxprint.ptsettings import ParatextSettings
from ptxprint.gtkpiclist import PicList
from ptxprint.piclist import PicChecks, PicInfo, PicInfoUpdateProject
from ptxprint.gtkstyleditor import StyleEditorView
from ptxprint.styleditor import aliases
from ptxprint.runjob import isLocked, unlockme
from ptxprint.texmodel import TexModel, ModelMap
from ptxprint.minidialog import MiniDialog
from ptxprint.dbl import UnpackDBL
import ptxprint.scriptsnippets as scriptsnippets
from ptxprint.utils import _, f_, textocol, _allbkmap
import configparser, logging
from threading import Thread

logger = logging.getLogger(__name__)

ssl._create_default_https_context = ssl._create_unverified_context
pdfre = re.compile(r".+[\\/](.+\.pdf)")

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
_alldigits = [ "Default", "Adlam", "Ahom", "Arabic-Indic", "Balinese", "Bengali", "Bhaiksuki", "Brahmi", "Chakma", "Cham", "Devanagari", 
    "Ethiopic", "Extended-Arabic", "Fullwidth", "Gujarati", "Gunjala-Gondi", "Gurmukhi", "Hanifi-Rohingya", "Javanese", "Kannada", 
    "Kayah-Li", "Khmer", "Khudawadi", "Lao", "Lepcha", "Limbu", "Malayalam", "Masaram-Gondi", "Meetei-Mayek", "Modi", "Mongolian", 
    "Mro", "Myanmar", "Myanmar-Shan", "Myanmar-Tai-Laing", "New-Tai-Lue", "Newa", "Nko", "Nyiakeng-Puachue-Hmong", "Ol-Chiki", "Oriya", 
    "Osmanya", "Pahawh-Hmong", "Rumi", "Saurashtra", "Sharada", "Sinhala-Lith", "Sora-Sompeng", "Sundanese", "Tai-Tham-Hora", 
    "Tai-Tham-Tham", "Takri", "Tamil", "Telugu", "Thai", "Tibetan", "Tirhuta", "Vai", "Wancho", "Warang-Citi", "Western-Cham"]

_ui_minimal = """
bx_statusBar fcb_uiLevel t_find
fcb_filterXrefs fcb_interfaceLang c_quickRun
tb_Basic lb_Basic
fr_projScope l_project fcb_project l_projectFullName r_book_single ecb_book 
l_chapfrom l_chapto t_chapfrom t_chapto 
r_book_multiple btn_chooseBooks ecb_booklist 
fr_SavedConfigSettings l_cfgName ecb_savedConfig t_savedConfig btn_saveConfig btn_lockunlock t_password
tb_Layout lb_Layout
fr_pageSetup l_pageSize ecb_pagesize l_fontsize s_fontsize l_linespacing s_linespacing 
fr_2colLayout c_doublecolumn gr_doubleColumn c_verticalrule 
tb_Font lb_Font
fr_FontConfig l_fontR bl_fontR tv_fontFamily fcb_fontFaces t_fontSearch 
tb_Help lb_Help
fr_Help
r_generate_selected l_generate_booklist r_generate_all c_randomPicPosn
l_statusLine btn_dismissStatusLine
""".split() # btn_reloadConfig 

_ui_enable4diglot2ndary = """
l_fontB bl_fontB l_fontI bl_fontI l_fontBI bl_fontBI 
tb_NotesRefs lb_NotesRefs tb_general
tb_footnotes c_includeFootnotes l_fnPos  c_fneachnewline
tb_xrefs     c_includeXrefs     l_xrPos  c_xreachnewline
c_fontFake l_fontBold s_fontBold l_fontItalic s_fontItalic
fr_writingSystem l_textDirection fcb_textDirection fcb_script l_script
tb_Body lb_Body
fr_BeginEnding c_bookIntro c_introOutline c_filterGlossary c_ch1pagebreak
fr_IncludeScripture c_mainBodyText gr_mainBodyText c_chapterNumber c_justify c_sectionHeads
c_verseNumbers c_preventorphans c_hideEmptyVerses c_elipsizeMissingVerses
""".split()

# bx_fnOptions bx_xrOptions 
_ui_basic = """
r_book_module btn_chooseBibleModule lb_bibleModule
btn_deleteConfig l_notes t_configNotes t_invisiblePassword
c_mirrorpages l_gutterWidth btn_adjust_spacing
s_colgutterfactor l_bottomRag s_bottomRag
fr_margins l_margins s_margins l_topmargin s_topmargin l_btmMrgn s_bottommargin
l_margin2header1 l_margin2header2 l_margin2header3
c_rhrule l_rhruleoffset s_rhruleposition
l_fontB bl_fontB l_fontI bl_fontI l_fontBI bl_fontBI 
c_fontFake l_fontBold s_fontBold l_fontItalic s_fontItalic
fr_writingSystem l_textDirection fcb_textDirection fcb_script l_script
tb_Body lb_Body
fr_BeginEnding c_bookIntro c_introOutline c_filterGlossary c_ch1pagebreak
fr_IncludeScripture c_mainBodyText gr_mainBodyText c_chapterNumber c_justify c_sectionHeads
c_verseNumbers c_preventorphans c_hideEmptyVerses c_elipsizeMissingVerses
tb_NotesRefs lb_NotesRefs tb_general
tb_footnotes c_includeFootnotes l_fnPos  c_fneachnewline
tb_xrefs     c_includeXrefs     l_xrPos  c_xreachnewline
tb_HeadFoot lb_HeadFoot
fr_Header l_hdrleft ecb_hdrleft l_hdrcenter ecb_hdrcenter l_hdrright ecb_hdrright
fr_Footer l_ftrcenter ecb_ftrcenter
tb_Pictures lb_Pictures
c_includeillustrations tb_settings lb_settings fr_inclPictures gr_IllustrationOptions c_cropborders r_pictureRes_High r_pictureRes_Low
l_homePage lb_homePage l_createZipArchiveXtra btn_createZipArchiveXtra btn_deleteTempFiles btn_about
""".split()

_ui_noToggleVisible = ("lb_details", "tb_details", "lb_checklist", "tb_checklist", "ex_styNote") # toggling these causes a crash
                       # "lb_footnotes", "tb_footnotes", "lb_xrefs", "tb_xrefs")  # for some strange reason, these are fine!

_ui_keepHidden = ("btn_download_update ", "l_extXrefsComingSoon", "tb_Logging", "lb_Logging",
                  "c_customOrder", "t_mbsBookList", "bx_statusMsgBar", "fr_plChecklistFilter",
                  "l_thumbVerticalL", "l_thumbVerticalR", "l_thumbHorizontalL", "l_thumbHorizontalR")

_uiLevels = {
    2 : _ui_minimal,
    4 : _ui_basic,
}

_showActiveTabs = {
    "c_includeillustrations" : ["tb_Pictures"],
    "c_diglot" :               ["tb_Diglot", "fr_diglot", "btn_diglotSwitch"],
    "c_thumbtabs" :            ["tb_TabsBorders", "fr_tabs"],
    "c_borders" :              ["tb_TabsBorders", "fr_borders"],
    "c_inclFrontMatter" :      ["tb_Peripherals", "gr_importFrontPDF"],
    "c_inclBackMatter" :       ["tb_Peripherals", "gr_importBackPDF"],
    "c_autoToC" :              ["tb_Peripherals", "bx_ToC"],
    "c_frontmatter" :          ["tb_Peripherals", "gr_frontmatter"],
    "c_colophon" :             ["tb_Peripherals", "bx_colophon"],
}

# The 3 dicts below are used by method: sensiVisible() to toggle object states

# Checkboxes and the different objects they make (in)sensitive when toggled
# Order is important, as the 1st object can be told to "grab_focus"
_sensitivities = {
    "r_decorator": {
        "r_decorator_file":    ["btn_selectVerseDecorator", "lb_inclVerseDecorator", "lb_style_v",
                                "l_verseDecoratorShift", "l_verseDecoratorScale",
                                "s_verseDecoratorShift", "s_verseDecoratorScale"],
        "r_decorator_ayah":    ["lb_style_v"]},
    "r_xrpos": {
        # "r_xrpos_normal" :    ["l_internote", "s_internote", "l_xrColWid", "s_centreColWidth", "r_fnpos_column"],
        # "r_xrpos_column" :    ["l_internote", "s_internote", "l_xrColWid", "s_centreColWidth", "r_fnpos_column"],
        # "r_xrpos_endnote" :   ["l_internote", "s_internote", "l_xrColWid", "s_centreColWidth", "r_fnpos_column"],
        # "r_xrpos_below" :     ["l_internote", "s_internote", "l_xrColWid", "s_centreColWidth"], # , "r_fnpos_column"],
        # "r_xrpos_blend" :     [],
        "r_xrpos_centre" :    ["l_internote", "s_internote", "fr_colXrefs", "l_xrColWid", "s_centreColWidth"]}, 
        
    "r_xrSource": {
        "r_xrSource_standard": ["s_xrSourceSize", "l_xrSourceSize", "l_xrSourceLess", "l_xrSourceMore"],
        "r_xrSource_custom" :  ["btn_selectXrFile"]},
    "c_mainBodyText" :         ["gr_mainBodyText"],
    "c_doublecolumn" :         ["gr_doubleColumn", "r_fnpos_column"],
    "c_useFallbackFont" :      ["btn_findMissingChars", "t_missingChars", "l_fallbackFont", "bl_fontExtraR"],
    "c_includeFootnotes" :     ["c_fneachnewline", "c_fnOverride", "c_fnautocallers", "t_fncallers", 
                                "btn_resetFNcallers", "c_fnomitcaller", "c_fnpageresetcallers",
                                "lb_style_f", "l_fnPos", "r_fnpos_normal", "r_fnpos_column", "r_fnpos_endnote"],
    "c_useXrefList" :          ["gr_extXrefs"],
    
    "c_includeillustrations" : ["gr_IllustrationOptions", "lb_details", "tb_details", "tb_checklist"],
    "c_diglot" :               ["gr_diglot", "fcb_diglotPicListSources", "r_hdrLeft_Pri", "r_hdrCenter_Pri", "r_hdrRight_Pri",
                                "r_ftrCenter_Pri", "r_hdrLeft_Sec", "r_hdrCenter_Sec", "r_hdrRight_Sec", "r_ftrCenter_Sec"],
    "c_diglotSeparateNotes" :  ["c_diglotNotesRule", "c_diglotJoinVrule"],
    "c_diglotNotesRule" :      ["c_diglotJoinVrule"],
    "c_borders" :              ["gr_borders"],

    "c_pagegutter" :           ["s_pagegutter", "c_outerGutter"],
    "c_verticalrule" :         ["l_colgutteroffset", "s_colgutteroffset"],
    "c_rhrule" :               ["s_rhruleposition"],
    "c_grid" :                 ["btn_adjustGrid"],
    "c_gridGraph" :            ["gr_graphPaper"],
    "c_introOutline" :         ["c_prettyIntroOutline"],
    "c_sectionHeads" :         ["c_parallelRefs", "lb_style_s", "lb_style_r"],
    "c_parallelRefs" :         ["lb_style_r"],
    "c_useChapterLabel" :      ["t_clBookList", "l_clHeading", "t_clHeading", "c_optimizePoetryLayout"],
    "c_differentColLayout" :   ["t_differentColBookList"],
    "c_autoToC" :              ["t_tocTitle", "gr_toc", "l_toc", "l_leaderStyle", "fcb_leaderStyle"],
    "c_hideEmptyVerses" :      ["c_elipsizeMissingVerses"],
    "c_marginalverses" :       ["s_columnShift"],
    "c_rangeShowVerse" :       ["l_chvsSep", "r_CVsep_period", "r_CVsep_colon"],
    "c_fnautocallers" :        ["t_fncallers", "btn_resetFNcallers", "c_fnomitcaller", "c_fnpageresetcallers"],
    "c_xrautocallers" :        ["t_xrcallers", "btn_resetXRcallers", "c_xromitcaller", "c_xrpageresetcallers"],
    "c_footnoterule" :         ["rule_footnote", "l_fnAboveSpace", "l_fnBelowSpace", "s_fnBelowSpace", "gr_fnRulePosParms"],
    "c_xrefrule" :             ["rule_xref",     "l_xrAboveSpace", "l_xrBelowSpace", "s_xrBelowSpace", "gr_xrRulePosParms"],
    "c_useCustomFolder" :      ["btn_selectFigureFolder", "c_exclusiveFiguresFolder", "lb_selectFigureFolder"],
    "c_processScript" :        ["r_when2processScript_before", "r_when2processScript_after", "btn_selectScript", "btn_editScript"],
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
    "c_inclVerseDecorator" :   ["gr_verseDecorator", "r_decorator_ayah", "r_decorator_file"],
    "c_fontFake":              ["s_fontBold", "s_fontItalic", "l_fontBold", "l_fontItalic"],
    "c_thumbtabs":             ["gr_thumbs"],
    "c_thumbrotate":           ["fcb_rotateTabs"],
    "c_frontmatter":           ["c_periphPageBreak", "btn_editFrontMatter"],
    "c_colophon":              ["gr_colophon"],
    "c_plCreditApply2all":     ["c_plCreditOverwrite"],
    "c_rangeShowChapter":      ["c_rangeShowVerse", "l_chvsSep", "r_CVsep_period", "r_CVsep_colon"],
    "c_strongs2cols":          ["l_strongRag", "s_strongRag"],
    "c_extendedFnotes":        ["gr_ef_layout"],
    "c_ef_verticalrule" :      ["l_ef_colgutteroffset", "s_ef_colgutteroffset", "line_efGutter"],
    "c_filterCats":            ["gr_filterCats"],
    "r_sbiPosn": {
        "r_sbiPosn_above":     ["fcb_sbi_posn_above"],
        "r_sbiPosn_beside":    ["fcb_sbi_posn_beside"],
        "r_sbiPosn_cutout":    ["fcb_sbi_posn_cutout", "s_sbiCutoutLines", "l_sbiCutoutLines"]},
}
# Checkboxes and the different objects they make (in)sensitive when toggled
# These function OPPOSITE to the ones above (they turn OFF/insensitive when the c_box is active)
_nonsensitivities = {
    "c_marginalverses" :       ["c_hangpoetry"],
    "c_noInternet" :           ["c_useEngLinks"],
    "c_styFaceSuperscript" :   ["l_styRaise", "s_styRaise"],
    "c_interlinear" :          ["c_letterSpacing", "s_letterShrink", "s_letterStretch"],
    "c_fighidecaptions" :      ["c_fighiderefs"],
    "c_doublecolumn" :         ["l_colXRside", "fcb_colXRside"],
    # "c_lockFontSize2Baseline": ["l_linespacing", "s_linespacing", "btn_adjust_spacing"],
    "c_sbi_lockRatio" :        ["s_sbi_scaleHeight"],
    "c_styTextProperties":     ["scr_styleSettings"],
    "r_xrpos": {
        "r_xrpos_below" :     [],
        "r_xrpos_blend" :     ["l_internote", "s_internote"],
        "r_xrpos_centre" :    []},
}

_object_classes = {
    "printbutton": ("b_print", "btn_refreshFonts", "btn_adjust_diglot", "btn_createZipArchiveXtra", "btn_Generate"),
    "sbimgbutton": ("btn_sbFGIDia", "btn_sbBGIDia"),
    "smallbutton": ("btn_dismissStatusLine", ),
    "fontbutton":  ("bl_fontR", "bl_fontB", "bl_fontI", "bl_fontBI"),
    "mainnb":      ("nbk_Main", ),
    "viewernb":    ("nbk_Viewer", "nbk_PicList"),
    "thumbtabs":   ("l_thumbVerticalL", "l_thumbVerticalR", "l_thumbHorizontalL", "l_thumbHorizontalR"),
    "stylinks":    ("lb_style_s", "lb_style_r", "lb_style_v", "lb_style_f", "lb_style_x", "lb_style_fig",
                    "lb_style_rb", "lb_style_gloss|rb", "lb_style_toc3", "lb_style_x-credit|fig", "lb_omitPics"), 
    "stybutton":   ("btn_resetCopyright", "btn_rescanFRTvars", "btn_resetColophon", 
                    "btn_resetFNcallers", "btn_resetXRcallers", "btn_styAdd", "btn_styEdit", "btn_styDel", 
                    "btn_styReset", "btn_refreshFonts", "btn_plAdd", "btn_plDel", 
                    "btn_plGenerate", "btn_plSaveEdits", "btn_resetTabGroups", "btn_adjust_spacing", 
                    "btn_adjust_top", "btn_adjust_bottom", "btn_DBLbundleDiglot1", "btn_DBLbundleDiglot2", 
                    "btn_resetGrid", "btn_refreshCaptions", "btn_sb_rescanCats") # "btn_reloadConfig", 
}

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
_allpgids = ["scroll_FrontMatter", "scroll_AdjList", "scroll_FinalSFM", 
             "scroll_TeXfile", "scroll_XeTeXlog", "scroll_Settings", "scroll_SettingsOld"]

_allcols = ["anchor", "caption", "file", "frame", "scale", "posn", "ref", "mirror", "caption2", "desc", "copy", "media", ]

_selcols = {
    "settings":  ["anchor", "caption",         "desc"],
    "details":   ["anchor", "caption", "file", "frame", "scale", "posn", "ref", "mirror", "caption2", "desc", "copy", "media"],
    "checklist": ["anchor", "caption", "file", "desc"]
} 

_availableColophons = ("fr", "es") # update when .json file gets expanded
_defaultColophon = r"""\pc \zcopyright
\pc \zlicense
\b 
\pc \zimagecopyrights
"""
_defaultDigColophon = r"""\usediglot\empty\pc \zcopyright
\pc \zlicense
\usediglot R \pc \zcopyrightR\usediglot\empty
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
    'value-changed': ("SpinButton",),
    'state-set': ("Switch",),
    'row-activated': ("TreeView",),
}

_olst = ["fr_SavedConfigSettings", "tb_Layout", "tb_Font", "tb_Body", "tb_NotesRefs", "tb_HeadFoot", "tb_Pictures",
         "tb_Advanced", "tb_Logging", "tb_TabsBorders", "tb_Diglot", "tb_StyleEditor", "tb_ViewerEditor", "tb_Help"]

_dlgtriggers = {
    "dlg_multiBookSelect":  "onChooseBooksClicked",
    "dlg_about":            "onAboutClicked",
    "dlg_password":         "onLockUnlockSavedConfig",
    "dlg_generatePL":       "onGeneratePicListClicked",
    "dlg_generateFRT":      "onGenerateClicked",
    "dlg_fontChooser":      "getFontNameFace",
    "dlg_features":         "onFontFeaturesClicked",
    "dlg_multProjSelector": "onChooseTargetProjectsClicked",
    "dlg_gridsGuides":      "adjustGuideGrid",
    "dlg_DBLbundle":        "onDBLbundleClicked",
    "dlg_overlayCredit":    "onOverlayCreditClicked",
    "dlg_strongsGenerate":  "onGenerateStrongsClicked",
    "dlg_borders":          "onSBborderClicked"
}

def _doError(text, secondary="", title=None, copy2clip=False, show=True, **kw):
    logger.error(text)
    if secondary:
        logger.error(secondary)
    if copy2clip:
        if secondary is not None:
            secondary += _("\nPTXprint Version {}").format(GitVersionStr)
        lines = [title or ""]
        if text is not None and len(text):
            lines.append(text)
        if secondary is not None and len(secondary):
            lines.append(secondary)
        s = _("Please send to: ptxprint_support@sil.org") + "\n\n{}".format("\n\n".join(lines))
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(s, -1)
        clipboard.store() # keep after app crashed
        if secondary is not None:
            secondary += "\n\n" + " "*18 + "[" + _("This message has been copied to the clipboard.")+ "]"
        else:
            secondary = " "*18 + "[" + _("This message has been copied to the clipboard.")+ "]"
    if show:
        dialog = Gtk.MessageDialog(parent=None, message_type=Gtk.MessageType.ERROR,
                 buttons=Gtk.ButtonsType.OK, text=text)
        if title is None:
            title = "PTXprint Version " + VersionStr
        dialog.set_title(title)
        if secondary is not None:
            dialog.format_secondary_text(secondary)
        if sys.platform == "win32":
            dialog.set_keep_above(True)
        dialog.run()
        if sys.platform == "win32":
            dialog.set_keep_above(False)
        dialog.destroy()
    else:
        print(text)
        if secondary is not None:
            print(secondary)

def getPTDir():
    txt = _("Paratext is not installed on this system.\n" + \
            "Please locate the directory where your USFM projects\n" +\
            "are (or will be) stored. Or click cancel to exit.")
    dialog = Gtk.MessageDialog(parent=None, message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK_CANCEL, text=txt)
    response = dialog.run()
    dialog.destroy()
    if response == Gtk.ResponseType.OK:
        action = Gtk.FileChooserAction.SELECT_FOLDER
        btnlabel = "Select"
        fdialog = Gtk.FileChooserDialog("Paratext Projects Directory", None,
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

def reset_gtk_direction():
    direction = Gtk.get_locale_direction()
    Gtk.Widget.set_default_direction(direction)

def getsign(b, v, a):
    r = ""
    if b > 0 and b < v:
        r = "-"
    if v < a:
        r = "+" + r
    return r

class GtkViewModel(ViewModel):

    def __init__(self, settings_dir, workingdir, userconfig, scriptsdir, args=None):
        logger.debug("Starting init in gtkview")
        super(GtkViewModel, self).__init__(settings_dir, workingdir, userconfig, scriptsdir, args)
        self.lang = args.lang if args.lang is not None else 'en'
        self.args = args
        self.initialised = False

    def setup_ini(self):
        self._setup_css()
        self.radios = {}
        GLib.set_prgname("ptxprint")
        self.builder = Gtk.Builder()
        gladefile = os.path.join(pycodedir(), "ptxprint.glade")
        GObject.type_register(GtkSource.View)
        GObject.type_register(GtkSource.Buffer)
        tree = et.parse(gladefile)
        self.allControls = []
        modelbtns = set([v[0] for v in ModelMap.values() if v[0] is not None and v[0].startswith("btn_")])
        self.btnControls = set()
        self.finddata = {}
        self.widgetnames = {}
        nid = None
        for node in tree.iter():
            if 'translatable' in node.attrib:
                node.text = _(node.text)
                del node.attrib['translatable']
            elif node.get('name', '') == 'name':
                node.text = _(node.text)
            if node.tag == "property" and nid is not None and not nid.startswith("lb_") and not nid.startswith("l_"):
                n = node.get('name')
                if n in ("name", "tooltip-text", "label"):
                    self.finddata[node.text.lower()] = (nid, 1 if  n == "tooltip-text" else 4)
                if n == 'name':
                    self.widgetnames[nid] = node.text
            if node.get('name') in ('pixbuf', 'icon', 'logo'):
                node.text = os.path.join(pycodedir(), node.text)
            if node.tag == "object":
                nid = node.get('id')
                if nid is None:
                    pass
                elif nid == 'txbf_colophon':
                    node.set('class', 'GtkSourceBuffer')
                elif nid == 'textv_colophon':
                    node.set('class', 'GtkSourceView')
                elif nid.startswith("r_"):
                    m = re.match(r"^r_(.+)?_(.+)$", nid)
                    if m:
                        self.radios.setdefault(m.group(1), set()).add(m.group(2))
                if nid is not None:
                    pre, name = nid.split("_", 1) if "_" in nid else ("", nid)
                    if pre in ("bl", "btn", "bx", "c", "col", "ecb", "ex", "fcb", "fr", "gr", 
                               "l", "lb", "r", "s", "scr", "t", "tb", "textv", "tv", "rule", "img"):
                        self.allControls.append(nid)
                        if pre == "btn" and nid not in modelbtns:
                            self.btnControls.add(nid)
        xml_text = et.tostring(tree.getroot(), encoding='unicode', method='xml')
        self.builder = Gtk.Builder.new_from_string(xml_text, -1)
        #    self.builder.set_translation_domain(APP)
        #    self.builder.add_from_file(gladefile)
        self.builder.connect_signals(self)
        logger.debug("Glade loaded in gtkview")
        self.isDisplay = True
        self.searchWidget = []
        self.config_dir = None
        self.booklistKeypressed = False
        self.configKeypressed = False
        self.configNoUpdate = False
        self.noUpdate = False
        self.pendingPid = None
        self.pendingConfig = None
        self.otherDiglot = None
        self.notebooks = {}
        self.pendingerror = None
        self.logfile = None
        self.highlight = False
        self.rtl = False
        self.isDiglotMeasuring = False
        self.warnedSIL = False
        self.printReason = 0
        self.mruBookList = self.userconfig.get('init', 'mruBooks', fallback='').split('\n')
        ilang = self.builder.get_object("fcb_interfaceLang")
        llang = self.builder.get_object("ls_interfaceLang")
        for i, r in enumerate(llang):
            if self.lang.startswith(r[1]):
                ilang.set_active(i)
                break
        for n in _notebooks:
            nbk = self.builder.get_object("nbk_"+n)
            self.notebooks[n] = [Gtk.Buildable.get_name(nbk.get_nth_page(i)) for i in range(nbk.get_n_pages())]
        self.noInt = self.userconfig.getboolean('init', 'nointernet', fallback=None)
        if self.noInt is not None:
            self.set("c_noInternet", self.noInt)
        for fcb in ("project", "uiLevel", "interfaceLang", "fontdigits", "script", "diglotPicListSources",
                    "textDirection", "glossaryMarkupStyle", "fontFaces", "featsLangs", "leaderStyle",
                    "picaccept", "pubusage", "pubaccept", "chklstFilter|0.75", "gridUnits", "gridOffset",
                    "fnHorizPosn", "xrHorizPosn", "snHorizPosn", "filterXrefs", "colXRside", "outputFormat", 
                    "stytcVpos", "strongsMajorLg", "strongswildcards", "strongsNdxBookId"):
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

        self._setup_digits()
        self.fcb_fontdigits.set_active_id(_alldigits[0])

        mrubl = self.builder.get_object("ecb_booklist")
        mrubl.remove_all()
        for m in self.mruBookList:
            mrubl.append(None, m)

        # for d in ("multiBookSelector", "multiProjSelector", "fontChooser", "password", "overlayCredit",
                  # "generateFRT", "generatePL", "styModsdialog", "DBLbundle", "features", "gridsGuides"):
            # dialog = self.builder.get_object("dlg_" + d)
            # dialog.add_buttons(
                # Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                # Gtk.STOCK_OK, Gtk.ResponseType.OK)
                
        self.fileViews = []
        self.buf = []
        self.uneditedText = {}
        self.cursors = []
        for i,k in enumerate(["FrontMatter", "AdjList", "FinalSFM", "TeXfile", "XeTeXlog", "Settings", "SettingsOld"]):
            self.buf.append(GtkSource.Buffer())
            self.cursors.append((0,0))
            view = GtkSource.View.new_with_buffer(self.buf[i])
            scroll = self.builder.get_object("scroll_" + k)
            scroll.add(view)
            self.fileViews.append((self.buf[i], view))
            view.set_left_margin(8)
            view.set_top_margin(6)
            view.set_bottom_margin(24)  
            view.set_show_line_numbers(True if i > 1 else False)
            view.set_editable(False if i in [2,3,4] else True)
            view.pageid = "scroll_"+k
            view.connect("focus-out-event", self.onViewerLostFocus)
            view.connect("focus-in-event", self.onViewerFocus)
            if not i in [2,3,4]: # Ignore the uneditable views
                # Set up signals to pick up any edits in the TextView window
                for evnt in ["key-press-event", "key-release-event", "delete-from-cursor", 
                             "backspace", "cut-clipboard", "paste-clipboard"]:
                    view.connect(evnt, self.onViewEdited) 
            
        if self.get("c_colophon") and self.get("txbf_colophon") == "":
            self.set("txbf_colophon", _defaultColophon)

        # Keep this tooltip safe for later
        self.frtMatterTooltip = self.builder.get_object("btn_infoViewEdit").get_tooltip_text()

        self.picListView = PicList(self.builder.get_object('tv_picListEdit'), self.builder, self)
        self.styleEditor = StyleEditorView(self)
        self.pubvarlist = self.builder.get_object("ls_zvarList")
        self.sbcatlist = self.builder.get_object("ls_sbCatList")
        self.strongsvarlist = self.builder.get_object("ls_strvarList")

        self.mw = self.builder.get_object("ptxprint")

        for w in self.allControls:
            if w.startswith(("c_", "s_", "t_", "r_")):  # These don't work. But why not? "bl_", "btn_", "ecb_", "fcb_")):
                # try:
                self.builder.get_object(w).connect("button-release-event", self.button_release_callback)
                # except (AttributeError, TypeError):
                    # print("Can't do that for:", w)
                    # pass

        logger.debug("Static controls initialized")
        projects = self.builder.get_object("ls_projects")
        digprojects = self.builder.get_object("ls_digprojects")
        strngsfbprojects = self.builder.get_object("ls_strongsfallbackprojects")
        projects.clear()
        digprojects.clear()
        strngsfbprojects.clear()
        allprojects = []
        for d in os.listdir(self.settings_dir):
            p = os.path.join(self.settings_dir, d)
            if not os.path.isdir(p):
                continue
            try:
                if os.path.exists(os.path.join(p, 'Settings.xml')):
                    with open(os.path.join(p, 'Settings.xml'), encoding="utf-8") as inf:
                        for l in inf.readlines():
                            if '<TranslationInfo>' in l:
                                if 'ConsultantNotes:' not in l and 'StudyBibleAdditions:' not in l:
                                    allprojects.append(d)
                                break
                        else:
                            allprojects.append(d)
                elif os.path.exists(os.path.join(p, 'ptxSettings.xml')) \
                        or any(x.lower().endswith("sfm") for x in os.listdir(p)):
                    allprojects.append(d)
            except OSError:
                pass
        strngsfbprojects.append(["None"])
        for p in sorted(allprojects, key = lambda s: s.casefold()):
            projects.append([p])
            digprojects.append([p])
            if os.path.exists(os.path.join(self.settings_dir, p, 'TermRenderings.xml')):
                strngsfbprojects.append([p])
        wide = int(len(allprojects)/16)+1 if len(allprojects) > 14 else 1
        # self.builder.get_object("fcb_project").set_wrap_width(1)
        self.builder.get_object("fcb_project").set_wrap_width(wide)
        self.builder.get_object("fcb_diglotSecProject").set_wrap_width(wide)
        self.builder.get_object("fcb_strongsFallbackProj").set_wrap_width(wide)
        self.getInitValues(addtooltips=self.args.identify)
        self.updateFont2BaselineRatio()
        self.tabsHorizVert()
        logger.debug("Project list loaded")

            # .mainnb {background-color: #d3d3d3;}
            # .mainnb panel {background-color: #d3d3d3;}
            # .mainnb panel:active {border: 1px solid green;}
            # .mainnb label:active{background-color: darker(powderblue);}

    def _setup_digits(self):
        digits = self.builder.get_object("ls_digits")
        currdigits = {r[0]: r[1] for r in digits}
        digits.clear()
        for d in _alldigits: # .items():
            v = currdigits.get(d, d.lower())
            digits.append([d, v])
        if self.prjid is None:
            return
        cfgpath = os.path.join(self.settings_dir, self.prjid, 'shared', 'fonts', 'mappings')
        if os.path.exists(cfgpath):
            added = set()
            for f in os.listdir(cfgpath):
                fname = f[:f.rindex(".")]
                if fname not in added:
                    digits.append([fname, fname])
                    added.add(fname)

    def _setup_css(self):
        css = """
            .printbutton:active { background-color: chartreuse; background-image: None }
            .sbimgbutton:active { background-color: lightskyblue; font-weight: bold}
            .smallbutton {font-size: 10px; min-height: 0pt; min-width:0px;  padding:1px;}
            .fontbutton {font-size: 12px}
            tooltip {color: rgb(255,255,255); background-color: rgb(64,64,64)} 
            .stylinks {font-weight: bold; text-decoration: None; padding: 1px 1px}
            .stybutton {font-size: 12px; padding: 4px 6px}
            progress, trough {min-height: 24px}
            .mainnb tab {min-height: 0pt; margin: 0pt; padding-bottom: 6pt}
            .mainnb tab:checked {background-color: lightsteelblue}
            .mainnb tab:checked label {font-weight: bold}
            .viewernb {background-color: #d3d3d3}
            .viewernb tab {min-height: 0pt; margin: 0pt; padding-bottom: 3pt}
            .smradio {font-size: 11px; padding: 1px 1px}
            .changed {font-weight: bold}
            .highlighted {background-color: peachpuff; background: peachpuff}
            combobox.highlighted > box.linked > entry.combo { background-color: peachpuff; background: peachpuff}
            entry.progress, entry.trough {min-height: 24px} """
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode("utf-8"))
        Gtk.StyleContext().add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def run(self, callback):
        super().setup_ini()
        logger.debug("Starting to run gtkview")
        self.callback = callback
        fc = initFontCache()
        logger.debug("Fonts initialised, well perhaps started")
        self.initialised = True
        for o in _olst:
            self.builder.get_object(o).set_sensitive(False)
        self.setPrintBtnStatus(1, _("No project set"))
        self.updateDialogTitle()
        logger.debug("Setting project")
        if self.pendingPid is not None:
            self.set("fcb_project", self.pendingPid)
            self.pendingPid = None
        logger.debug("Setting config")
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
        el = self.userconfig.getboolean('init', 'englinks', fallback=False)
        self.set("c_useEngLinks", el)
        # expert = self.userconfig.getboolean('init', 'expert', fallback=False)
        # self.set("c_showAdvancedOptions", not expert)
        # self.onShowAdvancedOptionsClicked(None)
        sys.excepthook = self.doSysError
        lsfonts = self.builder.get_object("ls_font")
        tvfonts = self.builder.get_object("tv_fontFamily")
        tvfonts.set_model(None)
        lsfonts.clear()
        tvfonts.set_model(lsfonts)
        self.onUILevelChanged(None)
        logger.debug("Starting UI")
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
            _doError(*self.pendingerror[:-1], **self.pendingerror[-1])
            self.pendingerror = None
        return True

    def onFindActivate(self, entry):
        self.onFindClicked(entry, Gtk.EntryIconPosition.PRIMARY, None)

    def onFindKey(self, entry, ev):
        if ev.keyval == Gdk.KEY_Escape:
            self.onFindClicked(entry, Gtk.EntryIconPosition.SECONDARY, ev)
        else:
            return False

    def onFindClicked(self, entry, which, event):
        txt = self.get("t_find").lower()
        if which == Gtk.EntryIconPosition.PRIMARY:
            self.doFind(txt)
        else:
            self.doFind(None)

    def doFind(self, txt):
        # if txt is None:   # keep track of recent finds
        for wid in self.searchWidget:
            self.highlightwidget(wid, highlight=False)
        self.searchWidget = []
        self.set("t_find", txt or "")
        if txt is None:
            return
        if self.builder.get_object(txt) is not None:
            self.highlightwidget(txt)
            return
        scores = {}
        for k, v in self.finddata.items():
            p = -1
            count = 0
            while True:
                p = k.find(txt, p+1)
                if p > -1:
                    count += 1
                else:
                    break
            if count > 0:
                s = scores.setdefault(v[0], 0)
                scores[v[0]] = s + count * v[1]
        choices = []
        entry = self.builder.get_object("t_find")
        for k in sorted(scores.keys(), key=lambda x:-scores[x]):
            n = self.widgetnames.get(k, None)
            if n is not None:
                choices.append((k, n))
        self._makeFindPopup(entry, choices)

    def _makeFindPopup(self, entry, choices):
        self.popover = Gtk.Popover()
        self.popover.set_position(Gtk.PositionType.TOP)
        self.popover.set_relative_to(entry)
        # Set the size of the pop-up help list
        popupHeight = min(300, min(7,len(choices))*30)
        self.popover.set_size_request(400, popupHeight)
        scr = Gtk.ScrolledWindow()
        ls = Gtk.ListStore(str, str)
        if len(choices):
            for w, v in choices:
                ls.append([w, v])
        else:
            ls.append(["t_find", _("No matches found - try another search term")])
        tv = Gtk.TreeView(model=ls)
        tv.set_headers_visible(False)
        tv.set_activate_on_single_click(True)
        tv.connect('row-activated', self._onFindRowActivated)
        cr = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(cell_renderer=cr, text=1)
        tv.append_column(col)
        scr.add(tv)
        self.popover.add(scr)
        self.popover.show_all()

    def _onFindRowActivated(self, tv, tp, tc):
        selection = tv.get_selection()
        model, i = selection.get_selected()
        self.highlightwidget(model[i][0], highlight=True)
        self.popover.destroy()

    def highlightwidget(self, wid, highlight=True):
        w = self.builder.get_object(wid)
        if w is None:
            return
        if highlight:
            self.searchWidget.append(wid)
        parent = w.get_parent()
        while parent is not None:
            name = Gtk.Buildable.get_name(parent)
            if name.startswith("tb_"):
                if highlight:
                    w.get_style_context().add_class("highlighted")
                    keepgoing = True
                    for k, v in self.notebooks.items():
                        if name in v:
                            pgnum = v.index(name)
                            t = self.builder.get_object('nbk_{}'.format(k)).set_current_page(pgnum)
                            keepgoing = k != 'Main'
                            break
                    if not keepgoing:
                        break
                else:
                    w.get_style_context().remove_class("highlighted")
                    break
            elif name.startswith("ex_"):
                parent.set_expanded(True)
            elif name in _dlgtriggers:
                if highlight:
                    w.get_style_context().add_class("highlighted")
                    getattr(self, _dlgtriggers[name])(None)
                else:
                    w.get_style_context().remove_class("highlighted")
                break
            parent = parent.get_parent()

    def onMainConfigure(self, w, ev, *a):
        if self.picListView is not None:
            self.picListView.onResized()

    def getInitValues(self, addtooltips=False):
        self.initValues = {}
        allentries = list(ModelMap.items()) + [("", [v]) for v in self.btnControls]
        for k, v in allentries:
            if v[0] is None:
                continue
            if addtooltips and not k.endswith("_"):
                w = self.builder.get_object(v[0])
                if w is not None:
                    try:
                        t = w.get_tooltip_text()
                    except AttributeError:
                        continue
                    if t is not None:
                        t += "\n" + v[0]
                    else:
                        t = v[0]
                    w.set_tooltip_text(t)
            if k and not v[0].startswith("r_"):
                self.initValues[v[0]] = self.get(v[0], skipmissing=True)
        for r, a in self.radios.items():
            for v in a:
                w = self.builder.get_object("r_{}_{}".format(r, v))
                if w.get_active():
                    self.initValues["r_{}".format(r)] = v
        self.resetToInitValues()

    def resetToInitValues(self):
        self.rtl = False
        super().resetToInitValues()
        if self.picinfos is not None:
            self.picinfos.clear(self)
        for k, v in self.initValues.items():
            if k.startswith("bl_") or v is not None:
                self.set(k, v)
        self.colorTabs()

    def onUILevelChanged(self, btn):
        pgId = self.builder.get_object("nbk_Main").get_current_page()
        ui = int(self.get("fcb_uiLevel"))
        self.userconfig.set('init', 'userinterface', str(ui))
                
        if ui < 6:
            for w in reversed(sorted(self.allControls)):
                self.toggleUIdetails(w, False)
                
            widgets = sum((v for k, v in _uiLevels.items() if ui >= k), [])
        else:
            # Selectively turn things back on if their settings are enabled
            for k, v in _showActiveTabs.items():
                if self.get(k):
                    for w in v:
                        self.toggleUIdetails(w, True)
                
            widgets = self.allControls

        for w in sorted(widgets):
            if w not in _ui_keepHidden:
                self.toggleUIdetails(w, True)
                
        for nbp in ["nbk_fnxr", "nbk_PicList"]:
            self.builder.get_object(nbp).set_current_page(0)

        for b in "dbl gnr8frt gnr8pl mbs mps pw feats font guides ovrly strong sty".split():
            self.toggleUIdetails("btn_"+b+"_cancel", True)
            self.toggleUIdetails("btn_"+b+"_ok", True)
            
        self.noInternetClicked(None)
        self.updateMarginGraphics()
        self.colorTabs()
        self.onRotateTabsChanged()
        self.checkUpdates()
        self.mw.resize(200, 200)
        self.builder.get_object("nbk_Main").set_current_page(pgId)

    def toggleUIdetails(self, w, state):
        # print(w)
        if w in _ui_noToggleVisible:
            self.builder.get_object(w).set_sensitive(state)
        else:
            self.builder.get_object(w).set_visible(state)

    def noInternetClicked(self, btn):
        ui = int(self.get("fcb_uiLevel"))
        if btn is not None:
            val = self.get("c_noInternet") or (ui < 6)
        else:
            val = self.noInt if self.noInt is not None else True
        adv = (ui >= 6)
        for w in ["l_url_usfm", "lb_DBLdownloads", "lb_openBible", 
                   "l_homePage",  "l_community",  "l_faq",  "l_pdfViewer",  "l_reportBugs",
                  "lb_homePage", "lb_community", "lb_faq", "lb_pdfViewer", "lb_reportBugs", 
                  "btn_about"]:
            self.builder.get_object(w).set_visible(not val)
        newval = self.get("c_noInternet")
        self.noInt = newval
        self.userconfig.set("init", "nointernet", "true" if newval else "false")
        # self.styleEditor.editMarker()  # Not sure WHY this was here. MH: Any ideas?
        # Show Hide specific Help items
        for pre in ("l_", "lb_"):
            for h in ("ptxprintdir", "prjdir", "settings_dir"): 
                self.builder.get_object("{}{}".format(pre, h)).set_visible(adv)
        for w in ["btn_DBLbundleDiglot1", "btn_DBLbundleDiglot2", "lb_omitPics", "l_techFAQ",  "lb_techFAQ"]:
            self.builder.get_object(w).set_visible(not newval and adv)

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
            res = super().get(wid, default=default)
            if not skipmissing and not (wid.startswith("_") or wid.startswith("r_")):
                print("Can't get {} in the model. Returning {}".format(wid, res))
            return res
        if wid.startswith("r_"):
            bits = wid.split("_")[1:]
            if len(bits) > 1:
                return w.get_active()
            return super().get(wid, default=default)
        return getWidgetVal(wid, w, default=default, asstr=asstr, sub=sub)

    def set(self, wid, value, skipmissing=False):
        if wid == "l_statusLine":
            self.builder.get_object("bx_statusMsgBar").set_visible(len(value))
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

    def getvar(self, k, dest=None):
        if dest is None:
            varlist = self.pubvarlist
        elif dest == "strongs":
            varlist = self.strongsvarlist
        else:
            varlist = []
        # elif dest == "sbcats":
            # varlist = self.sbcatlist
        for r in varlist:
            if r[0] == k:
                return r[1]
        return None

    def setvar(self, k, v, dest=None):
        if dest is None:
            varlist = self.pubvarlist
        elif dest == "strongs":
            varlist = self.strongsvarlist
        # elif dest == "sbcats":
            # varlist = self.sbcatlist
        for r in varlist:
            if r[0] == k:
                r[1] = v
                break
        else:
            varlist.append([k, v])

    def allvars(self, dest=None):
        if dest is None:
            varlist = self.pubvarlist
        elif dest == "strongs":
            varlist = self.strongsvarlist
        # elif dest == "sbcats":
            # varlist = self.sbcatlist
        return [r[0] for r in varlist]

    def clearvars(self, dest=None):
        if dest is None:
            self.pubvarlist.clear()
        elif dest == "strongs":
            self.strongsvarlist.clear()
        # elif dest == "sbcats":
            # self.sbcatlist.clear()

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

    def doError(self, txt, threaded=False, **kw):
        if threaded:
            self.pendingerror=(txt, kw)
        else:
            _doError(txt, **kw)

    def doStatus(self, txt=""):
        sl = self.builder.get_object("l_statusLine")
        self.set("l_statusLine", txt)
        status = len(self.get("l_statusLine"))
        sl = self.builder.get_object("bx_statusMsgBar").set_visible(status)
        
    def onHideStatusMsgClicked(self, btn):
        sl = self.builder.get_object("bx_statusMsgBar").set_visible(False)

    def waitThread(self, thread):
        while thread.is_alive():
            Gtk.main_iteration_do(False)
        
    def setPrintBtnStatus(self, idnty, txt=""):
        if not txt:
            self.printReason &= ~idnty
        else:
            self.printReason |= idnty
        if txt or not self.printReason:
            self.doStatus(txt)
        for w in ["b_print", "b_print2ndDiglotText", "btn_adjust_diglot", "s_diglotPriFraction"]:
            self.builder.get_object(w).set_sensitive(not self.printReason)

    def checkFontsMissing(self):
        self.setPrintBtnStatus(4, "")
        for f in ['R','B','I','BI']:
            if self.get("bl_font" + f) is None:
                self.setPrintBtnStatus(4, _("Font(s) not set"))
                return True
        return False
                
    def print2ndDiglotTextClicked(self, btn):
        self.onOK(btn)
        
    def onOK(self, btn):
        if btn == self.builder.get_object("b_print2ndDiglotText"):
            pass
        elif self.otherDiglot is not None:
            self.onDiglotSwitchClicked(self.builder.get_object("btn_diglotSwitch"))
            return
        if isLocked():
            self.doStatus(_("Printing busy"))
            return
        jobs = self.getBooks(files=True)
        if not len(jobs) or jobs[0] == '':
            self.doStatus(_("No books to print"))
            return
        if self.checkFontsMissing():
            self.doStatus(_("One of more fonts have not been set yet"))
            return
        # If the viewer/editor is open on an Editable tab, then "autosave" contents
        if Gtk.Buildable.get_name(self.builder.get_object("nbk_Main").get_nth_page(self.get("nbk_Main"))) == "tb_ViewerEditor":
            pgnum = self.get("nbk_Viewer")
            if self.notebooks["Viewer"][pgnum] in ("scroll_FrontMatter", "scroll_AdjList", "scroll_Settings", "scroll_SettingsOld"):
                self.onSaveEdits(None)
        cfgname = self.configName()
        if cfgname is None:
            cfgname = ""
        else:
            cfgname = "-" + cfgname
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)
        pdfnames = self.baseTeXPDFnames(diff=self.docreatediff)
        for basename in pdfnames:
            pdfname = os.path.join(self.working_dir, "..", basename) + ".pdf"
            exists = os.path.exists(pdfname)
            fileLocked = True
            while fileLocked:
                try:
                    with open(pdfname, "ab+") as outf:
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
                        self.doStatus(_("Close the old PDF file before you try again."))
                        self.finished()
                        return
                fileLocked = False
            if not exists:
                os.remove(pdfname)
        self.onSaveConfig(None)

        self._incrementProgress(val=0.)
        self.builder.get_object("t_find").set_placeholder_text(_("Processing..."))
        try:
            self.callback(self)
        except Exception as e:
            s = traceback.format_exc()
            s += "\n{}: {}".format(type(e), str(e))
            self.doError(s, copy2clip=True)
            unlockme()
            self.builder.get_object("t_find").set_placeholder_text("Search for settings")

    def onCancel(self, btn):
        self.onDestroy(btn)

    def warnSlowRun(self, btn):
        ofmt = self.get("fcb_outputFormat")
        if self.get("c_includeillustrations") and ofmt != "Screen":
            self.doStatus(_("Note: It may take a while for pictures to convert for selected PDF Output Format ({}).".format(ofmt)))
        else:
            self.doStatus("")
        spotColorStatus = ofmt == "Spot"
        for w in ["l_spotColor", "col_spotColor", "l_spotColorTolerance", "s_spotColorTolerance"]:
            self.builder.get_object(w).set_sensitive(spotColorStatus)
            
    def enableDisableSpotColor(self, btn):
        ofmt = self.get("fcb_outputFormat")
        print(f"{ofmt=}")

    def onAboutClicked(self, btn_about):
        dialog = self.builder.get_object("dlg_about")
        dialog.set_keep_above(True)
        response = dialog.run()
        dialog.set_keep_above(False)
        dialog.hide()

    def onBookScopeClicked(self, btn):
        self.bookrefs = None

    def onBookListChanged(self, ecb_booklist): # called on "focus-out-event"
        if not self.initialised:
            return
        if self.booklistKeypressed:
            self.booklistKeypressed = False
            return
        self.doBookListChange()
        
    def onBkLstKeyPressed(self, btn, *a):
        self.booklistKeypressed = True
        # print("onBkLstKeyPressed-m")
        # (this needs constraining somehow 
        self.set("r_book", "multiple")

    def onBkLstFocusOutEvent(self, btn, *a):
        self.booklistKeypressed = False
        self.doBookListChange()

    def doBookListChange(self):
        #bls = " ".join(self.getBooks())
        #self.set('ecb_booklist', bls)
        bls = self.get('ecb_booklist', '')
        self.bookrefs = None
        bl = self.getAllBooks()
        if not self.booklistKeypressed and not len(bl):
            # print("doBookListChange-A-s")
            # self.set("r_book", "single")
            self.set("ecb_book", list(bl.keys())[0])
        else:
            # print("doBookListChange-B-m") 
            # (this needs constraining somehow 
            # as it is called on onBkLstFocusOutEvent)
            self.set("r_book", "multiple")
        self.updateExamineBook()
        self.updateDialogTitle()
        # Save to user's MRU
        if bls in self.mruBookList or bls == "":
            return
        self.mruBookList.insert(0, bls)
        w = self.builder.get_object("ecb_booklist")
        w.prepend_text(bls)
        while len(self.mruBookList) > 10:
            self.mruBookList.pop(10)
            w.remove(10)
        self.userconfig.set('init', 'mruBooks', "\n".join(self.mruBookList))
        
    def onSaveConfig(self, btn, force=False):
        if self.prjid is None or (not force and self.configLocked()):
            return
        newconfigId = self.configName()
        if newconfigId != self.configId:
            self.applyConfig(self.configId, newconfigId, nobase=True)
            self.updateProjectSettings(self.prjid, configName=newconfigId, readConfig=True)
            self.configId = newconfigId
            self.updateSavedConfigList()
            stngdir = self.configPath(cfgname=self.configName())
            self.set("lb_settings_dir", '<a href="{}">{}</a>'.format(stngdir, stngdir))
            self.updateDialogTitle()
        self.userconfig.set("init", "project", self.prjid)
        self.userconfig.set("init", "nointernet", "true" if self.get("c_noInternet") else "false")
        self.noInt = self.get("c_noInternet")
        self.userconfig.set("init", "englinks", "true" if self.get("c_useEngLinks") else "false")
        if getattr(self, 'configId', None) is not None:
            self.userconfig.set("init", "config", self.configId)
        self.writeConfig(force=force)
        self.savePics(force=force)
        self.saveStyles(force=force)
        self.onSaveEdits(None)

    def writeConfig(self, cfgname=None, force=False):
        if self.prjid is not None:
            self.picChecksView.writeCfg(os.path.join(self.settings_dir, self.prjid), self.configId)
        super().writeConfig(cfgname=cfgname, force=force)

    def onDeleteConfig(self, btn):
        cfg = self.get("t_savedConfig")
        delCfgPath = self.configPath(cfgname=cfg)
        if cfg == 'Default':
            self.resetToInitValues()
            self.onFontChanged(None)
            # Right now this 'reset' (only) re-initializes the UI settings, and removes the ptxprint.sty file
            # We could provide a dialog with options about what else to delete (piclists, adjlists, etc.)
            sec = _("And the ptxprint.sty stylesheet has been deleted.")
            try:
                print("Reset Default config; Deleting: ", os.path.join(delCfgPath, "ptxprint.sty"))
                os.remove(os.path.join(delCfgPath, "ptxprint.sty"))
            except OSError:
                sec = _("But the ptxprint.sty stylesheet could not be deleted.")
            self.triggervcs = True
            self.updateFonts()
            self.doError(_("The 'Default' config settings have been reset."), secondary=sec)
            return
        else:
            if not os.path.exists(os.path.join(delCfgPath, "ptxprint.cfg")):
                self.doError(_("Internal error occurred, trying to delete a directory tree"), secondary=_("Folder: ")+delCfgPath)
                return
            try: # Delete the entire settings folder
                rmtree(delCfgPath)
            except OSError:
                self.doError(_("Cannot delete folder from disk!"), secondary=_("Folder: ") + delCfgPath)

            if not self.working_dir.startswith(os.path.join(self.settings_dir, self.prjid, "local", "ptxprint")):
                self.doError(_("Non-standard output folder needs to be deleted manually"), secondary=_("Folder: ")+self.working_dir)
            try: # Delete the entire output folder
                rmtree(self.working_dir)
            except FileNotFoundError:
                pass
            except OSError:
                self.doError(_("Cannot delete folder from disk!"), secondary=_("Folder: ") + self.working_dir)

            self.updateSavedConfigList()
            self.set("t_savedConfig", "Default")
            self.readConfig("Default")
            self.updateDialogTitle()
            self.triggervcs = True
        self.colorTabs()

    def updateBookList(self):
        self.noUpdate = True
        cbbook = self.builder.get_object("ecb_book")
        cbbook.set_model(None)
        lsbooks = self.builder.get_object("ls_books")
        lsbooks.clear()
        # if self.ptsettings is not None:
        bks = self.getAllBooks()
        for b in bks:
            if b != "FRT": # We no longer list the FRT book in the book chooser(s)
                # ind = books.get(b, 0)-1
                # if 0 <= ind <= len(bp) and bp[ind - 1 if ind > 39 else ind] == "1":
                lsbooks.append([b])
        cbbook.set_model(lsbooks)
        self.noUpdate = False

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
            if k.startswith("r_"):
                continue
            state = self.get(k)
            for w in v:
                # print(w)
                self.builder.get_object(w).set_sensitive(state)
        for k, v in _nonsensitivities.items():
            if k.startswith("r_"):
                continue
            state = not self.get(k)
            for w in v:
                self.builder.get_object(w).set_sensitive(state)
        self.colorTabs()
        self.updateMarginGraphics()

    def colorTabs(self):
        # col = "crimson"
        col = "#0000CD"
        fs = " color='"+col+"'" if self.get("c_colorfonts") else ""
        self.builder.get_object("lb_Font").set_markup("<span{}>".format(fs)+_("Fonts")+"</span>"+"+"+_("Scripts"))

        pi = " color='"+col+"'" if (self.get("c_inclFrontMatter") or self.get("c_autoToC") or \
           self.get("c_frontmatter") or self.get("c_colophon") or self.get("c_inclBackMatter")) else ""
        self.builder.get_object("lb_Peripherals").set_markup("<span{}>".format(pi)+_("Peripherals")+"</span>")

        ic = " color='"+col+"'" if self.get("c_includeillustrations") else ""
        self.builder.get_object("lb_Pictures").set_markup("<span{}>".format(ic)+_("Pictures")+"</span>")

        dg = " color='"+col+"'" if self.get("c_diglot") else ""
        self.builder.get_object("lb_Diglot").set_markup("<span{}>".format(dg)+_("Diglot")+"</span>")

        xl = " color='"+col+"'" if self.get("c_useXrefList") else ""
        self.builder.get_object("lb_NotesRefs").set_markup(_("Notes+")+"<span{}>".format(xl)+_("Refs")+"</span>")
        self.builder.get_object("lb_xrefs").set_markup("<span{}>".format(xl)+_("Cross-References")+"</span>")

        tb = self.get("c_thumbtabs")
        bd = self.get("c_borders")
        tc = "<span color='{}'>".format(col)+_("Tabs")+"</span>" if tb \
            else _("Tabs") if self.builder.get_object("fr_tabs").get_visible() else ""
        bc = "<span color='{}'>".format(col)+_("Borders")+"</span>" if bd \
            else _("Borders") if self.builder.get_object("fr_borders").get_visible() else ""
        jn = "+" if ((tb and bd) or int(self.get("fcb_uiLevel")) >= 6) else ""
        self.builder.get_object("lb_TabsBorders").set_markup(tc+jn+bc)

        ad = False
        for w in ["processScript", "usePrintDraftChanges", "usePreModsTex", \
                  "useModsTex", "useCustomSty", "useModsSty", "interlinear"]:
            if self.get("c_" + w):
                ad = True
                break
        ac = " color='"+col+"'" if ad else ""
        self.builder.get_object("lb_Advanced").set_markup("<span{}>".format(ac)+_("Advanced")+"</span>")

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
                    v = list(d[k].values())[0]
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
        self.colorTabs()

    def onFnPosChanged(self, btn):
        if self.get("r_fnpos") == "column" and self.get("r_xrpos") == "normal":
            self.set("r_xrpos", "column")

        if self.get("r_fnpos") == "normal" and self.get("r_xrpos") == "column":
            self.set("r_xrpos", "normal")
    
    def onXrefLocnClicked(self, btn):
        # if self.get("r_xrpos") == "blend" and self.get("r_fnpos") == "column":
            # self.set("r_fnpos", "normal")

        if self.get("r_xrpos") == "column" and self.get("r_fnpos") == "normal":
            self.set("r_fnpos", "column")

        if self.get("r_xrpos") == "normal" and self.get("r_fnpos") == "column":
            self.set("r_fnpos", "normal")

        if self.get("r_xrpos") in ("centre", "column"):
            self.set("r_fnpos", "column")

        if self.get("r_xrpos") == "centre":
            self.builder.get_object("ex_xrListSettings").set_expanded(True)
        
        self.onSimpleClicked(btn)
        try:
            self.styleEditor.setval("x", "NoteBlendInto", "f" if self.get("r_xrpos") == "blend" else None)
        except KeyError:
            return
    
    def onVertRuleClicked(self, btn):
        self.onSimpleClicked(btn)
        self.updateMarginGraphics()
        
    def on2colClicked(self, btn):
        self.onSimpleClicked(btn)
        self.updateMarginGraphics()
        self.updateDialogTitle()
        if self.loadingConfig:
            return
        self.picListView.onRadioChanged()
        val = self.get("s_indentUnit")
        if btn.get_active():
            val = float(val) / 2
        else:
            val = float(val) * 2
        self.set("s_indentUnit", val)
        # for fx in ("fn", "xr"): 
            # if not btn.get_active() and self.get("r_{}pos".format(fx)) == "column":
               # self.set("r_{}pos".format(fx), "normal")
        # for w in ("l_colXRside", "fcb_colXRside"):
            # self.builder.get_object(w).set_visible(not btn.get_active())            

    def onSimpleFocusClicked(self, btn):
        self.sensiVisible(Gtk.Buildable.get_name(btn), focus=True)

    def onCallersClicked(self, btn):
        w1 = Gtk.Buildable.get_name(btn)
        status = self.sensiVisible(w1, focus=True)
        for s in ['omitcaller', 'pageresetcallers']:
            w2 = w1[:4]+s
            self.builder.get_object(w2).set_active(status)

    # def onReloadConfigClicked(self, btn_reloadConfig):
        # self.updateProjectSettings(self.prjid, configName = self.configName(), readConfig=True)

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
            # self.builder.get_object("btn_showMoreOrLess").set_sensitive(False)
            self.onSaveConfig(None, force=True)     # Always save the config when locking
        else: # try to unlock the settings by removing the settings
            if pw == invPW:
                self.builder.get_object("t_invisiblePassword").set_text("")
                # self.builder.get_object("btn_showMoreOrLess").set_sensitive(True)
            else: # Mismatching password - Don't do anything
                pass
        self.builder.get_object("t_password").set_text("")
        dialog.set_keep_above(False)
        dialog.hide()

    def onPasswordChanged(self, t_invisiblePassword):
        lockBtn = self.builder.get_object("btn_lockunlock")
    
        if self.get("t_invisiblePassword") == "":
            status = True
            img = Gtk.Image.new_from_icon_name("changes-allow-symbolic", Gtk.IconSize.LARGE_TOOLBAR)
            lockBtn.set_image(img)
            # o = self.builder.get_object("icon_unlocked")
            # print(f"{o=}")
            # lockBtn.set_image(o)
        else:
            status = False
            # o = self.builder.get_object("icon_locked")
            # print(f"{o=}")
            # lockBtn.set_image(o)
            img = Gtk.Image.new_from_icon_name("changes-prevent-symbolic", Gtk.IconSize.LARGE_TOOLBAR)
            lockBtn.set_image(img)
            # lockBtn.set_image(self.builder.get_object("icon_locked"))
        for c in ["btn_saveConfig", "btn_deleteConfig", "t_configNotes", "fcb_uiLevel", 
                  "btn_Generate", "btn_plAdd", "btn_plDel"]:
            self.builder.get_object(c).set_sensitive(status)
        
    def onExamineBookChanged(self, cb_examineBook):
        if self.noUpdate == True:
            return
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        self.onViewerChangePage(None, None, pg, forced=True)

    def onBookSelectorChange(self, btn):
        # status = self.sensiVisible("r_book_multiple")
        # if status and self.get("ecb_booklist") == "" and self.prjid is not None:
        if self.get("ecb_booklist") == "" and self.prjid is not None:
            self.updateDialogTitle()
        else:
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

    def onUpdatePicCaptionsClicked(self, btn):
        # import pdb; pdb.set_trace()
        if self.diglotView is not None:
            pref = "L"
            digpics = PicInfo(self.diglotView)
            digpics.threadUsfms(self.diglotView, "R", nosave=True)
            self.picinfos.merge("L", "R", indat=digpics, mergeCaptions=True, bkanchors=True)
        else:
            pref = ""
        newpics = PicInfo(self)
        newpics.threadUsfms(self, pref, nosave=True)
        self.picinfos.merge(pref, pref, indat=newpics, mergeCaptions=True, bkanchors=True, captionpre="")
        self.updatePicList()

    def onGeneratePicListClicked(self, btn):
        bks2gen = self.getBooks()
        if not len(bks2gen):
            return
        ab = self.getAllBooks()
        bks = bks2gen
        dialog = self.builder.get_object("dlg_generatePL")
        self.set("l_generate_booklist", " ".join(bks))
        if sys.platform == "win32":
            dialog.set_keep_above(True)
        # If there is no PicList file for this config, then don't even ask - just generate it
        plpath = os.path.join(self.configPath(self.configName()),"{}-{}.piclist".format(self.prjid, self.configName()))
        if not os.path.exists(plpath):
            response = Gtk.ResponseType.OK
            self.set("r_generate", "all")
        else:
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
            mrgCptn = self.get("c_diglot2captions")
            if self.diglotView is None:
                PicInfoUpdateProject(self, procbks, ab, self.picinfos, random=rnd, cols=cols, doclear=doclear, clearsuffix=True)
            else:
                mode = self.get("fcb_diglotPicListSources")
                PicInfoUpdateProject(self, procbks, ab, self.picinfos,
                                     suffix="L", random=rnd, cols=cols, doclear=doclear, clearsuffix=True)
                diallbooks = self.diglotView.getAllBooks()
                PicInfoUpdateProject(self.diglotView, procbks, diallbooks,
                                     self.picinfos, suffix="R", random=rnd, cols=cols, doclear=False)
                if mode == "pri":
                    self.picinfos.merge("L", "R", mergeCaptions=mrgCptn)
                elif mode == "sec":
                    self.picinfos.merge("R", "L", mergeCaptions=mrgCptn)
            self.updatePicList(procbks)
            self.savePics()
            if self.get('r_generate') == 'all':
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
        if pgid == "scroll_FrontMatter":
            ptFRT = os.path.exists(os.path.join(self.settings_dir, self.prjid, self.getBookFilename("FRT", self.prjid)))
            self.builder.get_object("r_generateFRT_paratext").set_sensitive(ptFRT)
            dialog = self.builder.get_object("dlg_generateFRT")
            if sys.platform == "win32":
                dialog.set_keep_above(True)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                self.generateFrontMatter(self.get("r_generateFRT"), self.get("c_includeCoverSections"))
                self.rescanFRTvarsClicked(None, autosave=False)
            if sys.platform == "win32":
                dialog.set_keep_above(False)
            dialog.hide()

        if pgid == "scroll_AdjList":
            if bk not in bks2gen:
                self.doError(_("The Book in focus is not within scope"), 
                    secondary=_("To generate an AdjList, the book must be\n"+
                                "in the list of books to be printed."))
                return
            self.generateAdjList()

        elif pgid == "scroll_FinalSFM" and bk is not None:
            bk = bk if bk in bks2gen else None
            tmodel = TexModel(self, self.settings_dir, self._getPtSettings(self.prjid), self.prjid)
            out = tmodel.convertBook(bk, None, self.working_dir, os.path.join(self.settings_dir, self.prjid))
            self.editFile(out, loc="wrk", pgid=pgid)
        self.onViewerChangePage(None, None, pg, forced=True)

    def generateAdjList(self, books=None, dynamic=True):
        existingFilelist = []
        booklist = self.getBooks() if books is None else books
        diglot  = self.get("c_diglot")
        prjid = self.get("fcb_project")
        secprjid = ""
        if diglot:
            secprjid = self.get("fcb_diglotSecProject")
            if secprjid is not None:
                secprjdir = os.path.join(self.settings_dir, secprjid)
            else:
                self.doError(_("No Secondary Project Set"), secondary=_("In order to generate an AdjList for a diglot, the \n"+
                                                                        "Secondary project must be set on the Diglot tab."))
                return
        prjdir = os.path.join(self.settings_dir, self.prjid)
        usfms = self.get_usfms()
        if diglot:
            dusfms = self.diglotView.get_usfms()
        skipbooks = []
        for bk in booklist:
            fname = self.getAdjListFilename(bk, ext=".adj")
            outfname = os.path.join(self.configPath(self.configName()), "AdjLists", fname)
            if os.path.exists(outfname):
                if os.path.getsize(outfname) > 0:
                    skipbooks.append(bk)
                    existingFilelist.append(re.split(r"\\|/",outfname)[-1])
        if len(existingFilelist):
            if len(existingFilelist) > 13:
                existingFilelist = existingFilelist[:6] + ["..."] + existingFilelist[-6:]
            q1 = _("One or more Paragraph Adjust file(s) already exist!")
            q2 = "\n".join(existingFilelist)+_("\n\nDo you want to OVERWRITE the above-listed file(s)?")
            if self.msgQuestion(q1, q2, default=False):
                skipbooks = []
        booklist = [x for x in booklist if x not in skipbooks]
        if not len(booklist):
            return
        parlocs = os.path.join(self.working_dir, self.baseTeXPDFnames()[0] + ".parlocs")
        adjs = {}
        for i, loose in enumerate(("-1", "0", "+1")):
            runjob = self.callback(self, maxruns=1, forcedlooseness=loose, noview=True)
            while runjob.thread.is_alive():
                Gtk.main_iteration_do(False)
            runres = runjob.res
            if runres:
                continue
            with universalopen(parlocs) as inf:
                for l in inf.readlines():
                    if not l.startswith(r"\@parlen"):
                        continue
                    m = re.findall(r"\{(.*?)\}", l)
                    if not m:
                        continue
                    adjs.setdefault(m[0], {}).setdefault(int(m[1]), [0]*3)[i] = int(m[2])
        adjpath = os.path.join(self.configPath(self.configName()), "AdjLists")
        os.makedirs(adjpath, exist_ok=True)
        for bk in booklist:
            fname = self.getAdjListFilename(bk, ext=".adj")
            outfname = os.path.join(self.configPath(self.configName()), "AdjLists", fname)
            with open(outfname, "w", encoding="utf-8") as outf:
                outf.write("% syntax bk c.v +num[paragraph]. E.g. JHN 3.18 +1[2] for para after 3.18\n")
                outf.write("% autogenerated hints for paragraph possible changes: +0 for increases, -0 for decreases\n")
                for k, v in sorted(adjs.items(), key=lambda x:refKey(x[0])):
                    r = refKey(k)
                    if k[:3] != bk or r[0] >= 100: # May need to take these lines out!
                        continue                   # May need to take these lines out!
                    vals = []
                    first = True
                    s = ""
                    for sk, sv in sorted(v.items()):
                        if first:
                            s = getsign(*sv) + "0"
                            p = sk if sk != 1 else 0
                            first = False
                        else:
                            t = getsign(*sv)
                            if t != "":
                                vals.append("{}[{}]".format(t, sk))
                    if s == "0" and not len(vals):
                        continue
                    # if r[1] != 0: # This was preventing Intro matter vals from appearing
                    outs = "{} {}.{} {}".format(bk+r[3], r[1], str(r[2]) + r[5], s)
                    if p > 0:
                        outs += "[{}]".format(p)
                    if len(vals):
                        outs += "% " + " ".join(vals)
                    outf.write(outs+"\n")

    def onChangedMainTab(self, nbk_Main, scrollObject, pgnum=-1):
        pgid = Gtk.Buildable.get_name(nbk_Main.get_nth_page(pgnum))
        if pgid == "tb_ViewerEditor": # Viewer tab
            self.onRefreshViewerTextClicked(None)
        elif pgid == "tb_TabsBorders":
            self.onThumbColorChange()
        elif pgid == "tb_Pictures":
            self.onPLpageChanged(None, None, pgnum=-1)

    def onRefreshViewerTextClicked(self, btn):
        pg = self.get("nbk_Viewer")
        self.onViewerChangePage(None, None, pg, forced=True)

    def onViewerChangePage(self, nbk_Viewer, scrollObject, pgnum, forced=False):
        if nbk_Viewer is None:
            nbk_Viewer = self.builder.get_object("nbk_Viewer")
        page = nbk_Viewer.get_nth_page(pgnum)
        if page == None:
            return
        for w in ["gr_editableButtons", "l_examineBook", "ecb_examineBook", "c_autoSave",
                  "btn_refreshViewerText", "btn_viewEdit"]:
            self.builder.get_object(w).set_sensitive(True)
        self.builder.get_object("btn_viewEdit").set_label("View/Edit...")
        ibtn = self.builder.get_object("btn_infoViewEdit")
        ibtn.set_sensitive(False)
        ibtn.set_tooltip_text("")
        genBtn = self.builder.get_object("btn_Generate")
        genBtn.set_sensitive(False)
        self.builder.get_object("btn_editZvars").set_visible(False)
        self.builder.get_object("btn_removeZeros").set_visible(False)
        self.noUpdate = True
        prjid = self.get("fcb_project")
        prjdir = os.path.join(self.settings_dir, prjid)
        bks = self.getBooks()
        bk = self.get("ecb_examineBook")
        if bk == None or bk == "" and len(bks):
            bk = bks[0]
            self.builder.get_object("ecb_examineBook").set_active_id(bk)
        pgid = Gtk.Buildable.get_name(page)
        for o in ("l_examineBook", "ecb_examineBook"):
            if self.get("r_book") == "module":
                self.builder.get_object(o).set_sensitive(False)
            else:
                self.builder.get_object(o).set_sensitive(pgid in _allpgids[1:3])

        fndict = {"scroll_FrontMatter" : ("", ""), "scroll_AdjList" : ("AdjLists", ".adj"),
                  "scroll_FinalSFM" : ("", ""), "scroll_TeXfile" : ("", ".tex"),
                  "scroll_XeTeXlog" : ("", ".log"), "scroll_Settings": ("", ""),
                  "scroll_SettingsOld": ("", "")}

        if pgid == "scroll_FrontMatter":
            ibtn = self.builder.get_object("btn_infoViewEdit")
            ibtn.set_sensitive(True)
            ibtn.set_tooltip_text(self.frtMatterTooltip)
            fpath = self.configFRT()
            if not os.path.exists(fpath):
                self.uneditedText[pgnum] = _("Click the Generate button (above) to start the process of creating Front Matter...")
                self.fileViews[pgnum][0].set_text(self.uneditedText[pgnum])
                fpath = None
            if self.get("t_invisiblePassword") == "":
                genBtn.set_sensitive(True)
                self.builder.get_object("btn_editZvars").set_visible(True)
            else:
                self.builder.get_object("c_autoSave").set_sensitive(False)
                self.set("c_autoSave", False)

        elif pgid in ("scroll_AdjList", "scroll_FinalSFM"):
            fname = self.getBookFilename(bk, prjid)
            if pgid == "scroll_FinalSFM":
                fpath = os.path.join(self.working_dir, fndict[pgid][0], fname)
                genBtn.set_sensitive(True)
            else:
                fpath = os.path.join(self.configPath(cfgname=self.configId, makePath=False), fndict[pgid][0], fname)
            doti = fpath.rfind(".")
            if doti > 0:
                if self.get("c_diglot"):
                    fpath = fpath[:doti] + "-" + (self.configName() or "Default") + "-diglot" + fpath[doti:] + fndict[pgid][1]
                else:
                    if self.get("r_book") == "module":
                        modname = os.path.basename(self.moduleFile)
                        doti = modname.rfind(".")
                        fpath = os.path.join(self.working_dir, modname[:doti] + "-flat" + modname[doti:])
                    else:
                        fpath = fpath[:doti] + "-" + (self.configName() or "Default") + fpath[doti:] + fndict[pgid][1]
            if pgid == "scroll_AdjList":
                if self.get("t_invisiblePassword") == "":
                    genBtn.set_sensitive(True)
                    self.builder.get_object("btn_removeZeros").set_visible(True)
                else:
                    self.builder.get_object("c_autoSave").set_sensitive(False)
                    self.set("c_autoSave", False)
            elif pgid == "scroll_FinalSFM":
                self.builder.get_object("c_autoSave").set_sensitive(False)
                self.builder.get_object("btn_refreshViewerText").set_sensitive(False)
                self.builder.get_object("btn_viewEdit").set_label(_("View Only..."))

        elif pgid in ("scroll_TeXfile", "scroll_XeTeXlog"): # (TeX,Log)
            fpath = os.path.join(self.working_dir, self.baseTeXPDFnames()[0])+fndict[pgid][1]
            self.builder.get_object("c_autoSave").set_sensitive(False)
            self.builder.get_object("btn_refreshViewerText").set_sensitive(False)
            self.builder.get_object("btn_viewEdit").set_label(_("View Only..."))

        elif pgid in ("scroll_Settings", "scroll_SettingsOld"): # View/Edit one of the 4 Settings files or scripts
            lname = "l_{1}".format(*pgid.split('_'))
            fpath = self.builder.get_object(lname).get_tooltip_text()
            if fpath == None:
                self.uneditedText[pgnum] = _("Use the 'Advanced' tab to select which settings you want to view or edit.")
                self.fileViews[pgnum][0].set_text(self.uneditedText[pgnum])
                self.builder.get_object(lname).set_text("Settings")
                self.noUpdate = False
                return
        else:
            self.noUpdate = False
            return

        if fpath is None:
            self.noUpdate = False
            return
        set_tooltip = self.builder.get_object("l_{1}".format(*pgid.split("_"))).set_tooltip_text
        buf = self.fileViews[pgnum][0]
        logger.debug(f"Viewing({pgid[7:]} {bk} -> {fpath}")

        if os.path.exists(fpath):
            set_tooltip(fpath)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as inf:
                txt = inf.read()
                if len(txt) > 60000:
                    txt = txt[:60000]+_("\n\n------------------------------------- \
                                           \n[File has been truncated for display] \
                                           \nClick on View/Edit... button to see more.")
            self.fileViews[pgnum][0].set_text(txt)
            self.uneditedText[pgnum] = txt
            self.onViewerFocus(self.fileViews[pgnum][1], None)
        else:
            set_tooltip(None)
            txt = _("This file doesn't exist yet.\n\nTry clicking... \
                     \n   * the 'Generate' button \
                     \n   * the 'Print' button to create the PDF first")
            self.fileViews[pgnum][0].set_text(txt)
            self.uneditedText[pgnum] = txt
        self.noUpdate = False
        self.onViewEdited()

    def savePics(self, fromdata=False, force=False):
        if not force and self.configLocked():
            return
        if not fromdata and self.picinfos is not None and self.picinfos.loaded:
            self.picListView.updateinfo(self.picinfos)
        super().savePics(fromdata=fromdata, force=force)

    def loadPics(self, mustLoad=True, fromdata=True):
        super().loadPics(mustLoad=mustLoad, fromdata=fromdata)
        self.updatePicList()

    def onSavePicListEdits(self, btn):
        self.savePics()

    def onSaveEdits(self, btn, pgid=None):
        if pgid is not None:
            try:
                pg = self.notebooks["Viewer"].index(pgid)
            except ValueError:
                print("ValueError, pg=", pg)
                pg = 0
        else:
            pg = self.builder.get_object("nbk_Viewer").get_current_page()
            pgid = self.notebooks["Viewer"][pg]
        buf = self.fileViews[pg][0]
        if pgid == "scroll_AdjList":
            bk = self.get("ecb_examineBook")
            fname = self.getAdjListFilename(bk, ext=".adj")
            fdir= os.path.join(self.configPath(self.configName()), "AdjLists")
            os.makedirs(fdir, exist_ok=True)
            fpath = os.path.join(fdir, fname)
        elif pgid == "scroll_FrontMatter":
            fpath = self.configFRT()
        else:
            fpath = self.builder.get_object("l_{1}".format(*pgid.split("_"))).get_tooltip_text()
        if fpath is None: return
        titer = buf.get_iter_at_mark(buf.get_insert())
        self.cursors[pg] = (titer.get_line(), titer.get_line_offset())
        text2save = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        openfile = open(fpath,"w", encoding="utf-8")
        openfile.write(text2save)
        openfile.close()
        self.uneditedText[pg] = text2save
        self.onViewEdited()

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
        # if self.loadingConfig:
            # return
        self.fcb_fontdigits.set_active_id(self.get('fcb_script'))
        script = self.get("fcb_script")
        if script is not None:
            gclass = getattr(scriptsnippets, script.lower(), None)
        else:
            gclass = None
        if gclass is None or gclass.dialogstruct is None:
            state = False
        else:
            state = True
        for w in ["l_complexScript", "btn_scrsettings"]:
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
        for w in ("t_clHeading", "t_tocTitle", "t_configNotes", "scroll_FinalSFM", "scroll_FrontMatter", \
                  "ecb_ftrcenter", "ecb_hdrleft", "ecb_hdrcenter", "ecb_hdrright", "t_fncallers", "t_xrcallers", \
                  "l_projectFullName", "t_plCaption", "t_plRef", "t_plAltText", "t_plCopyright", "textv_colophon"):
            self.builder.get_object(w).modify_font(p)
        self.picListView.modify_font(p)

        w = self.builder.get_object("cr_zvar_value")
        w = self.builder.get_object("cr_strvar_value")
        w.set_property("font-desc", p)

    def onRadioChanged(self, btn):
        n = Gtk.Buildable.get_name(btn)
        bits = n.split("_")[1:]
        if btn.get_active():
            self.set("r_"+bits[0], bits[1])
        self.sensiVisible("r_"+bits[0])
        if n.startswith("r_book_") and self.get("r_book") != "module":
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
        pics = self.get("c_includeillustrations")
        self.colorTabs()
        if pics:
            self.loadPics()
        else:
            self.picinfos.clear(self)
            self.picListView.clear()
        self.onPicRescan(None)
        self.picPreviewShowHide(pics)
        
    def picPreviewShowHide(self, show=True):
        for w in ["bx_showImage", "tb_picPreview"]: #, "fr_picPreview", "img_picPreview"]:
            self.builder.get_object(w).set_visible(show)
        # if show and self.picListView is not None:
            # self.mw.resize(830, 594)
            # self.picListView.onResized()
            
    def onUseCustomFolderclicked(self, btn):
        status = self.sensiVisible("c_useCustomFolder")
        if not status:
            self.builder.get_object("c_exclusiveFiguresFolder").set_active(status)
        else:
            if self.get("lb_selectFigureFolder") == "":
                self.onSelectFigureFolderClicked(None)
        self.onPicRescan(btn)
        
    def onPrefImageTypeFocusOut(self, btn, foo):
        self.onPicRescan(btn)
        
    def onPicRescan(self, btn):
        self.picListView.clearSrcPaths()
        self.picListView.onRadioChanged()
        
    def onPageNumTitlePageChanged(self, btn):
        if self.get("c_pageNumTitlePage"):
            self.builder.get_object("c_printConfigName").set_active(False)

    def onPrintConfigNameChanged(self, btn):
        if self.get("c_printConfigName"):
            self.builder.get_object("c_pageNumTitlePage").set_active(False)

    def onResetFNcallersClicked(self, btn_resetFNcallers):
        w = self.builder.get_object("t_fncallers")
        ptset = re.sub(" ", ",", self.ptsettings.get('footnotes', ""))
        if ptset == "" or w.get_text() == ptset:
            w.set_text("a,b,c,d,e,f,✶,☆,✦,✪,†,‡,§")
        else:
            w.set_text(ptset)

    def onResetXRcallersClicked(self, btn_resetXRcallers):
        w = self.builder.get_object("t_xrcallers")
        ptset = re.sub(" ", ",", self.ptsettings.get('crossrefs', ""))
        if ptset == "" or w.get_text() == ptset:
            w.set_text("†,‡,§,∥,#")
        else:
            w.set_text(ptset)

    def onResetTabGroupsClicked(self, btn_resetTabGroups):
        grps = "RUT 1SA; EZR NEH EST; ECC SNG; HOS JOL AMO OBA JON MIC; NAM HAB ZEP HAG ZEC MAL; " + \
               "GAL EPH PHP COL; 1TH 2TH 1TI 2TI TIT PHM; JAS 1PE 2PE 1JN 2JN 3JN JUD"
        self.set("t_thumbgroups", grps)

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

    def onEditStyleClicked(self, btn):
        mkr = Gtk.Buildable.get_name(btn)[9:]
        if mkr == "toc3" and self.get("r_thumbText") == "zthumbtab":  # "c_thumbIsZthumb"):
            self.set("c_styTextProperties", False)  # MH: why is this being done?
            mkr = "zthumbtab"
        elif mkr == "x-credit|fig":
            dialog = self.builder.get_object("dlg_overlayCredit")
            dialog.set_keep_above(False)
            dialog.hide()
        elif mkr.endswith("strong-s"):
            simple = mkr.split("+",1)[0]
            for a in ("+strong-s", ""):
                if simple+a in self.styleEditor.allStyles():
                    mkr = simple+a
                    break # skip the next else
            else:
                mkr = None
        if mkr is not None:
            self.styleEditor.selectMarker(mkr)
            mpgnum = self.notebooks['Main'].index("tb_StyleEditor")
            self.builder.get_object("nbk_Main").set_current_page(mpgnum)
            self.wiggleCurrentTabLabel()

    # def hoverOverStyleLink(self, *argv):  # signal: query_tooltip
        # self.wiggleCurrentTabLabel()

    def wiggleCurrentTabLabel(self):
        lb = self.builder.get_object("lb_StyleEditor")
        t = lb.get_label()
        for b in range(8,-1,-1):
            lb.set_label(" "*b+t)
            Gtk.main_iteration_do(False)
            time.sleep(0.08)
            Gtk.main_iteration_do(False)
        
    def onProcessScriptClicked(self, btn):
        self.colorTabs()
        if not self.sensiVisible("c_processScript"):
            self.builder.get_object("btn_editScript").set_sensitive(False)
        else:
            if self.customScript != None:
                self.builder.get_object("btn_editScript").set_sensitive(True)

    def onIntroOutlineClicked(self, btn):
        if not self.sensiVisible("c_introOutline"):
            self.builder.get_object("c_prettyIntroOutline").set_active(False)

    def onRefreshFontsclicked(self, btn):
        fc = fccache()
        lsfonts = self.builder.get_object("ls_font")
        fc.fill_liststore(lsfonts)

    def onFontRclicked(self, btn):
        if self.getFontNameFace("bl_fontR"):
            self.onFontChanged(btn)
        self.checkFontsMissing()
        
    def onFontBclicked(self, btn):
        self.getFontNameFace("bl_fontB")
        self.checkFontsMissing()
        
    def onFontIclicked(self, btn):
        self.getFontNameFace("bl_fontI")
        self.checkFontsMissing()
        
    def onFontBIclicked(self, btn):
        self.getFontNameFace("bl_fontBI")
        self.checkFontsMissing()
        
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

    def _getSelectedFont(self, fallback=""):
        lb = self.builder.get_object("tv_fontFamily")
        sel = lb.get_selection()
        ls, row = sel.get_selected()
        if row is None:
            return (fallback, None)
        name = ls.get_value(row, 0) or fallback
        style = self.get("fcb_fontFaces")
        if style.lower() == "regular":
            style = ""
        return (name, style)

    def getFontNameFace(self, btnid, noStyles=False, noFeats=False):
        btn = self.builder.get_object(btnid) if btnid is not None else None
        f = self.get(btnid) if btnid is not None else None
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
            extend = None
            isCtxtSpace = False
            mapping = "Default"
            name = None
        else:
            for i, row in enumerate(ls):
                if row[0] == f.name:
                    break
            else:
                i = 0
            isGraphite = f.isGraphite
            isCtxtSpace = f.isCtxtSpace
            feats = f.asFeatStr()
            embolden = f.getFake("embolden")
            italic = f.getFake("slant")
            extend = f.getFake("extend") or "1.0"
            hasfake = embolden is not None or italic is not None
            mapping = f.getMapping()
            name = f.name
        lb.set_cursor(i)
        lb.scroll_to_cell(i)
        if name is not None:
            tv = self.builder.get_object("tv_fontFamily")
            tm = self.builder.get_object("ls_font")
            try:
                tp = [x[0] for x in tm].index(name)
            except ValueError:
                tp = None
            if tp is not None:
                ti = tm.get_iter(Gtk.TreePath.new_from_indices([tp]))
                tv.get_selection().select_iter(ti)
                logger.debug("Found {} in font dialog at {}".format(name, tp))
        self.builder.get_object("t_fontSearch").set_text("")
        self.builder.get_object("t_fontSearch").has_focus()
        self.builder.get_object("fcb_fontFaces").set_sensitive(not noStyles)
        self.builder.get_object("t_fontFeatures").set_text(feats)
        self.builder.get_object("t_fontFeatures").set_sensitive(not noFeats)
        self.builder.get_object("c_fontGraphite").set_active(isGraphite)
        self.builder.get_object("c_fontCtxtSpaces").set_active(isCtxtSpace)
        self.builder.get_object("s_fontBold").set_value(float(embolden or 0.))
        self.builder.get_object("s_fontItalic").set_value(float(italic or 0.))
        self.builder.get_object("s_fontExtend").set_value(float(extend or 1.0))
        self.builder.get_object("c_fontFake").set_active(hasfake)
        self.builder.get_object("fcb_fontdigits").set_active_id(mapping)
        for a in ("Bold", "Italic"):
            self.builder.get_object("s_font"+a).set_sensitive(hasfake)
        # dialog.set_default_response(Gtk.ResponseType.OK)
        dialog.set_keep_above(True)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            (name, style) = self._getSelectedFont(name)
            if self.get("c_fontFake"):
                bi = (self.get("s_fontBold"), self.get("s_fontItalic"))
            else:
                bi = None
            f = FontRef.fromDialog(name, style, self.get("c_fontGraphite"), 
                                   self.get("c_fontCtxtSpaces"), self.get("t_fontFeatures"),
                                   bi, self.get("s_fontExtend"), self.get("fcb_fontdigits"))
            if btnid is not None:
                self.set(btnid, f)
            res = True
        else:
            res = False
        dialog.set_keep_above(False)
        dialog.hide()
        return res

    def onFontFeaturesClicked(self, btn):
        (name, style) = self._getSelectedFont()
        if name is None:
            return
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
            tips = {}
        else:
            feats = f.otFeats
            vals = f.otVals
            langs = f.otLangs
            self.currdefaults = {}
            langfeats = {}
            tips = f.tipFeats

        numrows = len(feats)
        (lang, setfeats) = parseFeatString(self.get("t_fontFeatures"), defaults=self.currdefaults, langfeats=langfeats)
        for i, (k, v) in enumerate(sorted(feats.items())):
            featbox.insert_row(i)
            l = Gtk.Label(label=v+":")
            l.set_halign(Gtk.Align.END)
            if k in tips:
                l.set_tooltip_markup(tips[k])
            featbox.attach(l, 0, i, 1, 1)
            l.show()
            inival = int(setfeats.get(k, "0"))
            if k in vals:
                if len(vals[k]) < 3:
                    obj = Gtk.CheckButton()
                    if k in vals and len(vals[k]) > 1:
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
            logger.debug("New defaults for lang {}: {}".format(newlang, newdefaults))
            for i, (k, v) in enumerate(sorted(feats.items())):
                if newdefaults.get(k, 0) == self.currdefaults.get(k, 0):
                    continue
                obj = featbox.get_child_at(1, i)
                logger.debug("Changing feature {} in lang {}".format(k, newlang))
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
        bl = self.getBooks(scope="multiple", local=True)
        self.alltoggles = []
        for i, b in enumerate(lsbooks):
            tbox = Gtk.ToggleButton(b[0])
            tbox.show()
            if tbox.get_label() in bl:
                tbox.set_active(True)
            self.alltoggles.append(tbox)
            mbs_grid.attach(tbox, i // 13, i % 13, 1, 1)
        response = dialog.run()
        booklist = []
        if response == Gtk.ResponseType.OK:
            booklist = sorted((b.get_label() for b in self.alltoggles if b.get_active()), \
                                    key=lambda x:_allbkmap.get(x, len(_allbkmap)))
            self.set("ecb_booklist", " ".join(b for b in booklist))
        if self.get("r_book") in ("single", "multiple"):
            print("onChooseBooksClicked-m/s")
            self.set("r_book", "multiple" if len(booklist) else "single")
        self.updateDialogTitle()
        self.updateExamineBook()
        self.updatePicList()
        dialog.set_keep_above(False)
        dialog.hide()
        
    def onChooseTargetProjectsClicked(self, btn):
        dialog = self.builder.get_object("dlg_multiProjSelector")
        dialog.set_keep_above(True)
        mps_grid = self.builder.get_object("mps_grid")
        mps_grid.forall(mps_grid.remove)
        self.alltoggles = []
        prjs = self.builder.get_object("ls_projects")
        prjCtr = len(prjs)
        cols = int(prjCtr**0.6) if prjCtr <= 70 else 5
        for i, b in enumerate(prjs):
            if self.prjid == b[0]:
                tbox = Gtk.Label()
                tbox.set_text('<span background="black" foreground="white" font-weight="bold">  {} </span>'.format(b[0]))
                tbox.set_use_markup(True)
            else:
                tbox = Gtk.ToggleButton(b[0])
            tbox.show()
            self.alltoggles.append(tbox)
            mps_grid.attach(tbox, i % cols, i // cols, 1, 1)
        response = dialog.run()
        projlist = []
        if response == Gtk.ResponseType.OK:
            cfg = self.configName()
            for b in self.alltoggles:
                try:
                    if b.get_active():
                        projlist.append(b.get_label())
                except AttributeError:
                    pass
            for p in projlist:
                try:
                    if self.get("r_copyConfig") == "noReplace":
                        self.applyConfig(cfg, cfg, newprj=p)
                    elif self.get("r_copyConfig") == "merge":
                        self.applyConfig(cfg, cfg, action=1, newprj=p)
                    elif self.get("r_copyConfig") == "overwrite":
                        self.applyConfig(cfg, cfg, action=0, newprj=p)
                except FileNotFoundError as e:
                    self.doError(_("File not found"), str(e))
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
                    self.set("r_thumbText", "zthumbtab") # c_thumbIsZthumb", True)
                self.builder.get_object("r_thumbText_toc3").set_sensitive(self.get("c_usetoc3"))
                self.builder.get_object("r_thumbText_zthumbtab").set_sensitive(self.get("c_usetoc3"))
        else:
            self.builder.get_object("r_thumbText_toc3").set_sensitive(True)
            self.builder.get_object("r_thumbText_zthumbtab").set_sensitive(True)
        
    def filter_numbers(self, wid):
        w = Gtk.Buildable.get_name(wid)
        tbx = self.builder.get_object(w)
        text = tbx.get_text().strip().split('.')[0]
        tbx.set_text(''.join([i for i in text if i in '0123456789']))
        # print("filter_numbers-s")
        self.set("r_book", "single")
            
    def fromChapChange(self, x, y):
        fr = self.get("t_chapfrom")
        frCh = round(float(fr)) if fr != '' else 0 
        self.set("t_chapfrom", str(frCh))
        to = self.get("t_chapto")
        toCh = round(float(to)) if to != '' else 999
        if frCh < 1:
            self.set("t_chapfrom", "1")
        bk = self.get("ecb_book")
        if bk is not None and bk != "" and self.get("r_book") != "module":
            maxCh = int(chaps.get(str(bk), 999))
        else:
            self.set("t_chapfrom", "1")
            maxCh = 999
        if frCh > maxCh:
            self.set("t_chapfrom", str(maxCh))
            frCh = maxCh
        if frCh > toCh:
            self.set("t_chapto", str(frCh))
        # print("fromChapChange-s")
        self.set("r_book", "single")

    def toChapChange(self, x, y):
        fr = self.get("t_chapfrom")
        frCh = round(float(fr)) if fr != '' else 0 
        to = self.get("t_chapto")
        toCh = round(float(to)) if to != '' else 999
        self.set("t_chapto", str(toCh))
        bk = self.get("ecb_book")
        if bk is not None and bk != "" and self.get("r_book") != "module":
            maxCh = int(chaps.get(str(bk), 999))
            if toCh > maxCh:
                self.set("t_chapto", str(maxCh))
            elif toCh < frCh:
                self.set("t_chapfrom", str(toCh))
        # print("toChapChange-s")
        self.set("r_book", "single")

    def onBookChange(self, cb_book):
        bk = self.get("ecb_book")
        if bk == "NON":
            self.set("ecb_book", "")
            return
        if bk is not None and bk != "" and self.get("r_book") != "module":
            if not self.loadingConfig:
                # self.set("r_book", "single")
            # else:
                self.set("t_chapfrom", "1")
                self.set("t_chapto", str(chaps.get(str(bk), 999)))
            self.updateExamineBook()
        self.updateDialogTitle()
        self.updatePicList()
        # print("onBookChange-s")
        self.set("r_book", "single")

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
        c = self.get("col_styColor")
        col = coltohex(c)
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

    def setPrjConfig(self, prjid, configid):
        self.setPrjid(prjid)
        self.setConfigId(configid)

    def onProjectChange(self, cb_prj):
        if not self.initialised:
            return
        self.builder.get_object("btn_saveConfig").set_sensitive(True)
        # self.builder.get_object("btn_deleteConfig").set_sensitive(False)
        lockBtn = self.builder.get_object("btn_lockunlock")
        # lockBtn.set_label("Lock")
        lockBtn.set_sensitive(False)
        self.updateProjectSettings(None, saveCurrConfig=True, configName="Default")
        self.updateSavedConfigList()
        for o in _olst:
            self.builder.get_object(o).set_sensitive(True)
        self.setPrintBtnStatus(1)
        self.updateFonts()
        if self.ptsettings is not None:
            self.builder.get_object("l_projectFullName").set_label(self.ptsettings.get('FullName', ""))
            self.builder.get_object("l_projectFullName").set_tooltip_text(self.ptsettings.get('Copyright', ""))
        else:
            self.builder.get_object("l_projectFullName").set_label("")
            self.builder.get_object("l_projectFullName").set_tooltip_text("")
        pts = self._getPtSettings()
        if pts is not None:
            if self.get("t_copyrightStatement") == "":
                self.builder.get_object("t_copyrightStatement").set_text(pts.get('Copyright', ""))
        self.onUseIllustrationsClicked(None)
        self.updatePrjLinks()
        self.checkFontsMissing()

    def updatePrjLinks(self):
        if self.settings_dir != None and self.prjid != None:
            self.set("lb_ptxprintdir", '<a href="{}">{}</a>'.format(pycodedir(), pycodedir()))

            projdir = os.path.join(self.settings_dir, self.prjid)
            self.set("lb_prjdir", '<a href="{}">{}</a>'.format(projdir, projdir))

            stngdir = self.configPath(cfgname=self.configName()) or ""
            self.set("lb_settings_dir", '<a href="{}">{}</a>'.format(stngdir, stngdir))

            outdir =  self.working_dir.rstrip(self.configName()) or "" if self.working_dir is not None else ""
            self.set("lb_working_dir", '<a href="{}">{}</a>'.format(outdir, outdir))
            
    def updateProjectSettings(self, prjid, saveCurrConfig=False, configName=None, readConfig=None):
        if prjid == self.prjid and configName == self.configId:
            return True
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
        books = self.getBooks()
        if self.get("r_book") in ("single", "multiple") and (books is None or not len(books)):
            books = self.getAllBooks()
            for b in allbooks:
                if b in books.keys():
                    self.set("ecb_book", b)
                    # print("updateProjectSettings-s")
                    self.set("r_book", "single")
                    break
        # status = self.get("r_book") == "multiple"
        # self.builder.get_object("ecb_booklist").set_sensitive(status)
        for i in self.notebooks['Viewer']:
            obj = self.builder.get_object("l_{1}".format(*i.split("_")))
            if obj is not None:
                obj.set_tooltip_text(None)
        self.updatePrjLinks()
        self.setEntryBoxFont()
        self._setup_digits()
        self.updatePicList()
        self.updateDialogTitle()
        self.styleEditor.editMarker()
        self.updateMarginGraphics()
        self.onBodyHeightChanged(None)
        logger.debug(f"Changed project to {prjid} {configName=}")

    def onConfigNameChanged(self, cb_savedConfig):
        if self.configKeypressed:
            self.configKeypressed = False
            return
        self.doConfigNameChange()

    def doConfigNameChange(self):
        lockBtn = self.builder.get_object("btn_lockunlock")
        if self.configName() == "Default":
            lockBtn.set_sensitive(False)
        if self.configNoUpdate or self.get("ecb_savedConfig") == "":
            return
        self.builder.get_object("fcb_uiLevel").set_sensitive(True)
        # lockBtn.set_label("Lock")
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

    def onConfigKeyPressed(self, btn, *a):
        self.configKeypressed = True

    def onCfgFocusOutEvent(self, btn, *a):
        self.configKeypressed = False
        self.doConfigNameChange()

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
        fpath = self._locFile(file2edit, loc)
        if fpath is None:
            return
        label = self.builder.get_object("l_{1}".format(*pgid.split("_")))
        if pgid == "scroll_Settings":
            currpath = label.get_tooltip_text()
            oldlabel = self.builder.get_object("l_SettingsOld")
            oldpath = oldlabel.get_tooltip_text()
            if fpath == oldpath:
                label = oldlabel
                pgnum += 1
            elif fpath != currpath:
                self.onSaveEdits(None, pgid="scroll_SettingsOld")
                oldlabel.set_tooltip_text(label.get_tooltip_text())
                oldlabel.set_text(label.get_text())
                self.builder.get_object("gr_editableButtons").set_sensitive(True)
                label.set_text(file2edit)
                buf = self.fileViews[pgnum][0]
                text2save = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
                self.fileViews[pgnum+1][0].set_text(text2save)
        label.set_tooltip_text(fpath)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as inf:
                txt = inf.read()
            self.fileViews[pgnum][0].set_text(txt)
            self.onViewerFocus(self.fileViews[pgnum][1], None)
        else:
            self.fileViews[pgnum][0].set_text(_("\nThis file doesn't exist yet!\n\nEdit here and Click 'Save' to create it."))

    def editFile_delayed(self, *a):
        GLib.idle_add(self.editFile, *a)

    def onViewerLostFocus(self, widget, event):
        pgnum = self.notebooks['Viewer'].index(widget.pageid)
        buf = self.fileViews[pgnum][0]
        t = buf.get_iter_at_mark(self.fileViews[pgnum][0].get_insert())
        self.cursors[pgnum] = (t.get_line(), t.get_line_offset())
        currentText = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        label = self.builder.get_object(_allpgids[pgnum][5:])
        tt = label.get_tooltip_text()
        if tt is not None and not currentText == self.uneditedText[pgnum]:
            if self.get("c_autoSave"):
                self.onSaveEdits(None)
            elif self.msgQuestion(_("Save changes?"), _("Do you wish to save the changes you made?") + \
                                                        "\n\n" + _("File: ") + tt):
                self.onSaveEdits(None)
            else:
                self.onRefreshViewerTextClicked(None)
        self.onViewEdited()
                
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

    def onViewEdited(self, *argv):
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        buf = self.fileViews[pg][0]
        currentText = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        label = self.builder.get_object(_allpgids[pg][5:])
        txtcol = " color='crimson'" if not currentText == self.uneditedText[pg] else ""
        label.set_markup("<span{}>".format(txtcol)+label.get_text()+"</span>")

    def _editProcFile(self, fname, loc, intro=""):
        fpath = self._locFile(fname, loc)
        if intro != "" and not os.path.exists(fpath):
            openfile = open(fpath,"w", encoding="utf-8")
            openfile.write(intro)
            openfile.close()
        self.editFile(fname, loc)

    def onEditScriptFile(self, btn):
        scriptName = os.path.basename(self.customScript)
        scriptPath = os.path.dirname(self.customScript)
        if self.customScript:
            self._editProcFile(scriptName, scriptPath)

    def onEditChangesFile(self, btn):
        self._editProcFile("PrintDraftChanges.txt", "prj")
        self._editProcFile("changes.txt", "cfg")

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
        self.colorTabs()
        if btn.get_active():
            self.triggervcs = True

    def onChangesFileClicked(self, btn):
        self.onExtraFileClicked(btn)
        cfile = os.path.join(self.configPath(self.configName()), "changes.txt")
        if not os.path.exists(cfile):
            with open(cfile, "w", encoding="utf-8") as outf:
                outf.write(chgsHeader)

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
            for c in ("r_when2processScript_before", "r_when2processScript_after", "btn_editScript"):
                self.builder.get_object(c).set_sensitive(True)
        else:
            self.customScript = None
            btn_selectScript.set_tooltip_text("")
            self.builder.get_object("c_processScript").set_active(False)
            for c in ("r_when2processScript_before", "r_when2processScript_after", "btn_editScript"):
                self.builder.get_object(c).set_sensitive(False)

    def onSelectXrFileClicked(self, btn_selectXrFile):
        prjdir = os.path.join(self.settings_dir, self.prjid)
        customXRfile = self.fileChooser("Select a Custom Cross-Reference file", 
                filters = {"Paratext XRF Files": {"patterns": "*.xrf", "mime": "text/plain", "default": True},
                           "All Files": {"pattern": "*"}},
                multiple = False, basedir=os.path.join(prjdir, "..", "_Cross References"))
        if customXRfile is not None:
            self.customXRfile = customXRfile[0]
            self.builder.get_object("r_xrSource_custom").set_active(True)
            btn_selectXrFile.set_tooltip_text(str(customXRfile[0]))
        else:
            self.customXRfile = None
            btn_selectXrFile.set_tooltip_text("")
            self.builder.get_object("r_xrSource_custom").set_active(False)

    def onCreateZipArchiveClicked(self, btn_createZipArchive):
        cfname = self.configName()
        zfname = self.prjid+("-"+cfname if cfname else "")+"PTXprintArchive.zip"
        archiveZipFile = self.fileChooser(_("Select the location and name for the Archive file"),
                filters={"ZIP files": {"pattern": "*.zip", "mime": "application/zip"}},
                multiple=False, folder=False, save=True, basedir=self.working_dir, defaultSaveName=zfname)
        if archiveZipFile is not None:
            btn_createZipArchive.set_tooltip_text(str(archiveZipFile[0]))
            try:
                self.createArchive(str(archiveZipFile[0]))
                self.openFolder(os.path.dirname(archiveZipFile[0]))
            except Exception as e:
                s = traceback.format_exc()
                s += "\n{}: {}".format(type(e), str(e))
                self.doError(s, copy2clip=True)
        else:
            btn_createZipArchive.set_tooltip_text("No Archive File Created")

    def onSelectModuleClicked(self, btn):
        prjdir = os.path.join(self.settings_dir, self.prjid)
        tgtfldr = os.path.join(prjdir, "Modules")
        if not os.path.exists(tgtfldr):
            tgtfldr = os.path.join(self.settings_dir, "_Modules")
        moduleFile = self.fileChooser("Select a Paratext Module", 
                filters = {"Modules": {"patterns": ["*.sfm"] , "mime": "text/plain", "default": True},
                           "All Files": {"pattern": "*"}},
                multiple = False, basedir=tgtfldr)
        if moduleFile is not None:
            moduleFile = [Path(os.path.relpath(x, prjdir)) for x in moduleFile]
            self.moduleFile = moduleFile[0]
            self.builder.get_object("lb_bibleModule").set_label(os.path.basename(moduleFile[0]))
            self.builder.get_object("btn_chooseBibleModule").set_tooltip_text(str(moduleFile[0]))
            # print("onSelectModuleClicked-A-mod")
            self.set("r_book", "module")

        else:
            self.builder.get_object("r_book_single").set_active(True)
            self.builder.get_object("lb_bibleModule").set_label("")
            self.moduleFile = None
            self.builder.get_object("btn_chooseBibleModule").set_tooltip_text("")
            # print("onSelectModuleClicked-B-s")
            self.set("r_book", "single")
        self.updateDialogTitle()

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
            if self.picListView is not None and self.picListView.picinfo is not None:
                self.picListView.picinfo.build_searchlist()
                self.picListView.onRadioChanged()

    def _onPDFClicked(self, title, isSingle, basedir, ident, attr, btn, chkbx=True):
        folderattr = getattr(self, attr, None)
        if folderattr is None:
            folderattr = basedir if isSingle else [basedir]
        if isSingle:
            fldr = os.path.dirname(folderattr)
        else:
            fldr = os.path.dirname(folderattr[0])
        if not os.path.exists(fldr):
            fldr = basedir
        vals = self.fileChooser(title,
                filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                multiple = not isSingle, basedir=fldr)
        if vals != None and len(vals) and str(vals[0]) != "None":
            if chkbx:
                self.builder.get_object("c_"+ident).set_active(True)
            if isSingle:
                setattr(self, attr, vals[0])
                btn.set_tooltip_text(str(vals[0]))
                self.set("lb_"+ident, pdfre.sub(r"\1", str(vals[0])))
            else:
                setattr(self, attr, vals)
                btn.set_tooltip_text("\n".join(str(s) for s in vals))
                self.set("lb_"+ident, ", ".join(pdfre.sub(r"\1", str(s)) for s in vals))
        else:
            setattr(self, attr, None)
            btn.set_tooltip_text("")
            self.set("lb_"+ident, "")
            if chkbx:
                btn.set_sensitive(False)
                self.set("c_"+ident, False)

    def onImportPDFsettingsClicked(self, btn_importPDF):
        vals = self.fileChooser(_("Select a PDF to import the settings from"),
                filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                multiple = False, basedir=os.path.join(self.working_dir, ".."))
        if vals is None or not len(vals) or str(vals[0]) == "None":
            return
        zipdata = self.getPDFconfig(vals[0])
        if zipdata is not None:
            if self.msgQuestion(_("Overwite current Configuration?"), 
                    _("WARNING: Importing the settings from the selected PDF will overwrite the current configuration.\n\nDo you wish to continue?")):
                self.unpackSettingsZip(zipdata, self.prjid, self.configName(), self.configPath(self.configName()))
        else:
            self.doError(_("PDF Config Import Error"), 
                    secondary=_("Sorry - Can't find any settings to import from the selected PDF.\n\n") + \
                            _("Only PDFs created with PTXprint version 2.3 or later contain settings\n") + \
                            _("if created with 'Include Config Settings Within PDF' option enabled."))
        
    def onFrontPDFsClicked(self, btn_selectFrontPDFs):
        self._onPDFClicked(_("Select one or more PDF(s) for FRONT matter"), False, 
                os.path.join(self.settings_dir, self.prjid), 
                "inclFrontMatter", "FrontPDFs", btn_selectFrontPDFs)

    def onBackPDFsClicked(self, btn_selectBackPDFs):
        self._onPDFClicked(_("Select one or more PDF(s) for BACK matter"), False, 
                os.path.join(self.settings_dir, self.prjid), 
                "inclBackMatter", "BackPDFs", btn_selectBackPDFs)

    def onWatermarkPDFclicked(self, btn_selectWatermarkPDF):
        self._onPDFClicked(_("Select Watermark PDF file"), True,
                os.path.join(pycodedir(), "PDFassets", "watermarks"),
                "applyWatermark", "watermarks", btn_selectWatermarkPDF)

    def onPageBorderPDFclicked(self, btn_selectPageBorderPDF):
        self._onPDFClicked(_("Select Page Border PDF file"), True,
                os.path.join(pycodedir(), "PDFassets", "border-art"),
                "inclPageBorder", "pageborder", btn_selectPageBorderPDF)

    def onSectionHeaderPDFclicked(self, btn_selectSectionHeaderPDF):
        self._onPDFClicked(_("Select Section Header PDF file"), True,
                os.path.join(pycodedir(), "PDFassets", "border-art"),
                "inclSectionHeader", "sectionheader", btn_selectSectionHeaderPDF)

    def onEndOfBookPDFclicked(self, btn_selectEndOfBookPDF):
        self._onPDFClicked(_("Select End of Book PDF file"), True,
                os.path.join(pycodedir(), "PDFassets", "border-art"),
                "inclEndOfBook", "endofbook", btn_selectEndOfBookPDF)

    def onVerseDecoratorPDFclicked(self, btn_selectVerseDecoratorPDF):
        self._onPDFClicked(_("Select Verse Decorator PDF file"), True,
                os.path.join(pycodedir(), "PDFassets", "border-art"),
                "inclVerseDecorator", "versedecorator", btn_selectVerseDecoratorPDF)

    def onSelectDiffPDFclicked(self, btn_selectDiffPDF):
        self._onPDFClicked(_("Select a PDF file to compare with"), True,
                os.path.join(self.working_dir),
                "diffPDF", "diffPDF", btn_selectDiffPDF, False)
        if self.get("lb_diffPDF") == "":
            self.set("lb_diffPDF", _("Previous PDF (_1)"))

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
        if basedir is not None or not basedir:
            dialog.set_current_folder(str(basedir))
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
        if filters != None:
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
        self.colorTabs()
        if self.loadingConfig:
            return
        if self.get("c_diglot"):
            self.diglotView = self.createDiglotView()
            self.set("c_doublecolumn", True)
            self.builder.get_object("c_doublecolumn").set_sensitive(False)
        else:
            self.builder.get_object("c_doublecolumn").set_sensitive(True)
            self.setPrintBtnStatus(2)
            self.diglotView = None
        self.updateDialogTitle()
        self.loadPics(mustLoad=False)

    def onDiglotSwitchClicked(self, btn):
        oprjid = None
        oconfig = None
        if self.otherDiglot is not None:
            oprjid, oconfig = self.otherDiglot
            self.otherDiglot = None
            btn.set_label(_("Switch to Other\nDiglot Project"))
            self.builder.get_object("b_print2ndDiglotText").set_visible(False)
            self.changeLabel("b_print", _("Print (Make PDF)"))
        elif self.get("c_diglot"):
            oprjid = self.get("fcb_diglotSecProject")
            oconfig = self.get("ecb_diglotSecConfig")
            if oprjid is not None and oconfig is not None:
                self.otherDiglot = (self.prjid, self.configName())
                btn.set_label(_("Save & Return to\nDiglot Project"))
            self.builder.get_object("b_print2ndDiglotText").set_visible(True)
            self.changeLabel("b_print", _("Return to Primary"))
        self.onSaveConfig(None)
        if oprjid is not None and oconfig is not None:
            self.set("fcb_project", oprjid)
            self.set("ecb_savedConfig", oconfig)
        mpgnum = self.notebooks['Main'].index("tb_Diglot")
        self.builder.get_object("nbk_Main").set_current_page(mpgnum)

    def changeLabel(self, w, lbl):
        b = self.builder.get_object(w)
        b.set_visible(False)
        b.set_label(lbl)
        b.set_visible(True)
        
    def ondiglotSecProjectChanged(self, btn):
        self.updateDiglotConfigList()
        self.updateDialogTitle()

    def ondiglotSecConfigChanged(self, btn):
        if self.loadingConfig:
            return
        if self.get("c_diglot"):
            self.diglotView = self.createDiglotView()
        else:
            self.setPrintBtnStatus(2)
            self.diglotView = None
        self.loadPics()
        
    def onGenerateHyphenationListClicked(self, btn):
        scrsnpt = self.getScriptSnippet()
        # Show dialog with various options
        dialog = self.builder.get_object("dlg_createHyphenList")
        self.set("l_createHyphenList_booklist", " ".join(self.getBooks()))
        sylbrk = scrsnpt.isSyllableBreaking(self)
        if not sylbrk:
            self.set("c_addSyllableBasedHyphens", False)
        self.builder.get_object("c_addSyllableBasedHyphens").set_sensitive(sylbrk)
        if sys.platform == "win32":
            dialog.set_keep_above(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.generateHyphenationFile(inbooks=self.get("c_hyphenLimitBooks"), addsyls=self.get("c_addSyllableBasedHyphens"))
        if sys.platform == "win32":
            dialog.set_keep_above(False)
        dialog.hide()

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
        
    def msgQuestion(self, title, question, default=False):
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

    def onOpenFolderButtonClicked(self, btn):
        self.onOpenFolderClicked(self.builder.get_object("lb_working_dir"))
        
    def onOpenFolderClicked(self, btn, *argv):
        p = re.search(r'(?<=href=\")[^<>]+(?=\")',btn.get_label())
        outputfolder =  p[0]
        self.openFolder(outputfolder)

    def openFolder(self, fldrpath):
        path = os.path.realpath(fldrpath)
        if sys.platform.startswith("win") and os.path.exists(fldrpath):
            os.startfile(fldrpath)

    def finished(self):
        # print("Reset progress bar")
        GLib.idle_add(lambda: self._incrementProgress(val=0.))

    def _incrementProgress(self, val=None):
        wid = self.builder.get_object("t_find")
        if val is None:
            val = wid.get_progress_fraction()
            val = 0.20 if val < 0.1 else (1. + val) * 0.5
        wid.set_progress_fraction(val)

    def incrementProgress(self):
        GLib.idle_add(self._incrementProgress)

    def onIdle(self, fn, *args):
        GLib.idle_add(fn, *args)

    def showLogFile(self):
        mpgnum = self.notebooks['Main'].index("tb_ViewerEditor")
        self.builder.get_object("nbk_Main").set_current_page(mpgnum)
        vpgnum = self.notebooks['Viewer'].index("scroll_XeTeXlog")
        self.builder.get_object("nbk_Viewer").set_current_page(vpgnum)

    def onBorderClicked(self, btn):
        self.onSimpleClicked(btn)
        self.sensiVisible("c_borders")
        self.colorTabs()

    def onTabsClicked(self, btn):
        self.onSimpleClicked(btn)
        self.sensiVisible("c_thumbtabs")
        self.colorTabs()
        self.onNumTabsChanged()
        status = self.get("c_thumbtabs")
        if status:
            if not self.get("c_usetoc3"):
                self.set("r_thumbText", "zthumbtab")
            self.builder.get_object("r_thumbText_toc3").set_sensitive(self.get("c_usetoc3"))
            self.builder.get_object("r_thumbText_zthumbtab").set_sensitive(self.get("c_usetoc3"))

    def onNumTabsChanged(self, *a):
        if not super().onNumTabsChanged(*a):
            return
        if self.get("c_thumbtabs"):
            self.updateThumbLines()
            self.onThumbColorChange()
        self.tabsHorizVert()
            
    def tabsHorizVert(self):
        if self.get("c_thumbtabs"):
            self.builder.get_object("l_thumbVerticalL").set_visible(self.get("c_thumbrotate"))
            self.builder.get_object("l_thumbVerticalR").set_visible(self.get("c_thumbrotate"))
            self.builder.get_object("l_thumbHorizontalL").set_visible(not self.get("c_thumbrotate"))
            self.builder.get_object("l_thumbHorizontalR").set_visible(not self.get("c_thumbrotate"))
        else:
            for w in ["l_thumbHorizontalL", "l_thumbVerticalL", "l_thumbHorizontalR", "l_thumbVerticalR"]:
                self.builder.get_object(w).set_visible(False)
                
    def onThumbColorChange(self, *a):
        def coltohex(s):
            vals = s[s.find("(")+1:-1].split(",")
            h = "#"+"".join("{:02x}".format(int(x)) for x in vals)
            return h
        bcol = coltohex(self.get("col_thumbback"))
        self.set("l_thumbbackValue", bcol)
        tabstyle = "zthumbtab" if self.get("r_thumbText") == "zthumbtab" else "toc3"
        colval = self.styleEditor.getval(tabstyle, "color")
        fcol = coltohex(textocol(colval))
        bold = "bold" if self.styleEditor.getval(tabstyle, "bold") == "" else "normal"
        ital = "italic" if self.styleEditor.getval(tabstyle, "italic") == "" else "normal"
        markup = '<span background="{}" foreground="{}" font-weight="{}" font-style="{}">  {{}}  </span>'.format(bcol, fcol, bold, ital)
        # print(f"{colval=}  {markup=}")
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
        self.getFontNameFace("bl_font_styFontName") #, noStyles=True)
        self.styleEditor.item_changed(btn, "FontName")
        
    def onColophonClicked(self, btn):
        self.onSimpleClicked(btn)
        if self.get("c_colophon") and self.get("txbf_colophon") == "":
            self.localizeDefColophon()

    def onColophonResetClicked(self, btn):
        self.localizeDefColophon()
        
    def localizeDefColophon(self):
        ct = _defaultDigColophon if self.get("c_diglot") else _defaultColophon
        if self.lang in _availableColophons:
            ct = re.sub(r'\\zimagecopyrights', r'\\zimagecopyrights' + self.lang, ct)
        self.set("txbf_colophon", ct)

    def onResetCopyrightClicked(self, btn):
        self.builder.get_object("t_copyrightStatement").set_text(self._getPtSettings().get('Copyright', ""))

    def onCopyrightStatementChanged(self, btn):
        btname = Gtk.Buildable.get_name(btn)
        w = self.builder.get_object(btname)
        t = w.get_text()
        if not self.warnedSIL:
            chkSIL = re.findall(r"(?i)\bs\.?i\.?l\.?\b", t)
            if len(chkSIL):
                self.doError(_("Warning! SIL's Executive Limitations do not permit SIL to publish scripture."), 
                   secondary=_("The reference to SIL in the project's copyright line has been removed. " + \
                               "Contact your entity's Publishing Coordinator for advice regarding protocols."))
                t = re.sub(r"(?i)\bs\.?i\.?l\.?\b ?(International)* ?", "", t)
                self.warnedSIL = True
        t = re.sub("</?p>", "", t)
        t = re.sub("\([cC]\)", "\u00a9 ", t)
        t = re.sub("\([rR]\)", "\u00ae ", t)
        t = re.sub("\([tT][mM]\)", "\u2122 ", t)
        if btname == 't_plCreditText' and len(t) == 3:
            if self.get('c_sensitive'):
                t = re.sub(r"(?i)dcc", "\u00a9 DCC", t)
            else:
                t = re.sub(r"(?i)dcc", "\u00a9 David C Cook", t)
        w.set_text(t)
        
    def onStyleAdd(self, btn):
        self.styleEditor.mkrDialog(newkey=True)

    def onStyleEdit(self, btn):
        self.styleEditor.mkrDialog()

    def onStyleFilter(self, btn):
        def widen(x):
            if x in aliases:
                return [x, x+"1"]
            elif x[:-1] in aliases and x.endswith("1"):
                return [x, x[:-1]]
            else:
                return [x]
        mrkrset = self.get_usfms().get_markers(self.getBooks()) if btn.get_active() else set()
        mrkrset = set(sum((widen(x) for x in mrkrset), []))
        logger.debug(f"{self.getBooks()=}  {mrkrset=}")
        self.styleEditor.add_filter(btn.get_active(), mrkrset)

    def onEditMarkerChanged(self, mkrw):
        m = mkrw.get_text()
        t = self.get("t_styName")
        self.set("t_styName", re.sub(r"^.*?-", m+" -", t))

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
                                  filters={"Images": {"patterns": ['*.tif', '*.png', '*.jpg', '*.pdf'], "mime": "application/image"}},
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
        # Ensure that the anchor ref only uses . (and not :) as the ch.vs separator and that _bk_ is upperCASE
        a = self.get('t_plAnchor')
        a = a[:4].upper() + re.sub(r'(\d+):(\d+)', r'\1.\2', a[4:])
        # Make sure there are no spaces after the _bk_ code (easy to paste in a \k "Phrase with spaces:"\k*
        #                                                   which gets converted to k.Phrasewithspaces:
        a = a[:5] + re.sub(' ', '', a[5:])
        a = re.sub('\\\+?[a-z0-9\-]+\*? ', '', a)
        self.set("t_plAnchor", a)

    def resetParam(self, btn, foo):
        label = Gtk.Buildable.get_name(btn.get_child())
        self.styleEditor.resetParam(label)

    def adjustGuideGrid(self, btn):
        # if self.get('c_grid'):
        dialog = self.builder.get_object("dlg_gridsGuides")
        dialog.set_keep_above(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            pass
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.set_keep_above(False)
        dialog.hide()

    def onRefreshGridDefaults(self, btn):
        self.set("fcb_gridUnits", "cm")
        self.set("s_gridMinorDivisions", "5")
        self.set("fcb_gridOffset", "page")
        self.set("s_gridMajorThick", "0.2")
        self.set("col_gridMajor", "rgb(204,0,0)")
        self.set("s_gridMinorThick", "0.2")
        self.set("col_gridMinor", "rgb(115,210,22)")

    def onPLpageChanged(self, nbk_PicList, scrollObject, pgnum):
        page = 99
        if nbk_PicList is None:
            nbk_PicList = self.builder.get_object("nbk_PicList")
        if pgnum == -1:
            pgnum = nbk_PicList.get_current_page()
        page = nbk_PicList.get_nth_page(pgnum)
        pgid = Gtk.Buildable.get_name(page).split('_')[-1]
        filterSensitive = True if pgid == "checklist" else False
        self.builder.get_object("bx_activeRefresh").set_visible(False)
        self.builder.get_object("fr_plChecklistFilter").set_sensitive(filterSensitive)
        self.builder.get_object("fr_plChecklistFilter").set_visible(filterSensitive)
        self.builder.get_object("gr_picButtons").set_visible(not filterSensitive)
        self.builder.get_object("bx_activeRefresh").set_visible(True)
        for w in _allcols:
            if w in _selcols[pgid]:
                self.builder.get_object("col_{}".format(w)).set_visible(True)
            else:
                self.builder.get_object("col_{}".format(w)).set_visible(False)

    def onDBLbundleClicked(self, btn):
        dialog = self.builder.get_object("dlg_DBLbundle")
        response = dialog.run()
        dialog.hide()
        if response == Gtk.ResponseType.OK and self.builder.get_object("btn_locateDBLbundle").get_sensitive:
            prj = self.get("t_DBLprojName")
            if prj != "":
                if UnpackDBL(self.DBLfile, prj, self.settings_dir):
                    # add prj to ls_project before selecting it.
                    for a in ("ls_projects", "ls_digprojects", "ls_strongsfallbackprojects"):
                        lsp = self.builder.get_object(a)
                        allprojects = [x[0] for x in lsp]
                        for i, p in enumerate(allprojects):
                            if prj.casefold() > p.casefold():
                                lsp.insert(i, [prj])
                                break
                        else:
                            lsp.append([prj])
                    self.resetToInitValues()
                    self.set("fcb_project", prj)
                else:
                    self.doError("Faulty DBL Bundle", "Please check that you have selected a valid DBL bundle (ZIP) file. "
                                                      "Or contact the DBL bundle provider.")

    def onLocateDBLbundleClicked(self, btn):
        DBLfile = self.fileChooser("Select a DBL Bundle file", 
                filters = {"DBL Bundles": {"patterns": ["*.zip"] , "mime": "text/plain", "default": True},
                           "All Files": {"pattern": "*"}},
                multiple = False, basedir=os.path.join(self.settings_dir, "Bundles"))
        if DBLfile is not None:
            # DBLfile = [x.relative_to(prjdir) for x in DBLfile]
            self.DBLfile = DBLfile[0]
            self.builder.get_object("lb_DBLbundleFilename").set_label(os.path.basename(DBLfile[0]))
            self.set("t_DBLprojName", os.path.basename(DBLfile[0])[:8])
            self.builder.get_object("btn_locateDBLbundle").set_tooltip_text(str(DBLfile[0]))
        else:
            self.builder.get_object("lb_DBLbundleFilename").set_label("")
            self.set("t_DBLprojName", "")
            self.DBLfile = None
            self.builder.get_object("btn_locateDBLbundle").set_tooltip_text("")
    
    def onDBLprojNameChanged(self, widget):
        text = self.get("t_DBLprojName")
        btn = self.builder.get_object("btn_locateDBLbundle")
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
        m = re.match(r"^.*?[,xX]\s*([\d.]+)(\S+)\s*(?:.*|$)", self.get("ecb_pagesize"))
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
        crParams = "bl,0,None" if not len(crParams) else crParams
        m = re.match(r"^([tcb]?)([lrcio]?),(-?9?0?|None),(\w*)", crParams)
        if m:
            self.set("fcb_plCreditVpos", m[1])
            self.set("fcb_plCreditHpos", m[2])
            self.set("fcb_plCreditRotate", m[3])
            self.set("ecb_plCreditBoxStyle", m[4])
        self.set("t_plCreditText", self.get("l_piccredit") if len(self.get("l_piccredit")) else "")
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
            if self.get("c_plCreditApply2all"):
                srcs = set(v.get('src', None) for v in self.picinfos.values())
                self.picChecksView.setMultiCreditOverlays(srcs, text, crParams, self.get("t_plFilename"))
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
            return 20000 if runres else xdvigetpages(xdvname)
        mid = float(self.get("s_diglotPriFraction")) / 100.
        res = brent(0., 1., mid, score, 0.001)
        self.set("s_diglotPriFraction", res*100)
        self.isDiglotMeasuring = False
        self.callback(self)
        btn.set_active(False)

    def onDiglotSwapSideClicked(self, btn):
        if self.get("r_hdrLeft") != self.get("r_hdrRight"):
            for a in ("r_hdrLeft", "r_hdrRight"):
                v = self.get(a)
                v = "Sec" if v == "Pri" else ("Pri" if v == "Sec" else v)
                self.set(a, v)

    def onFootnotesClicked(self, btn):
        if not self.sensiVisible("c_includeFootnotes"):
            if self.get("r_xrpos") == "below" or self.get("r_xrpos") == "blend":
                self.set("r_xrpos", "centre") if self.get("c_useXrefList") else self.set("r_xrpos", "normal")

    def updateColxrefSetting(self, btn):
        xrc = self.get("r_xrpos") == "centre" # i.e. Column Cross-References
        self.builder.get_object("fr_colXrefs").set_sensitive(xrc)
        if self.get("c_useXrefList"):
            self.builder.get_object("ex_xrListSettings").set_expanded(True)
            self.builder.get_object("ex_xrefs").set_expanded(False)

    def onGenerateStrongsClicked(self, btn):
        dialog = self.builder.get_object("dlg_strongsGenerate")
        if sys.platform == "win32":
            dialog.set_keep_above(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK: # Create Index... clicked
            cols = 2 if self.get("c_strongs2cols") else 1
            bkid = self.get("fcb_strongsNdxBookId") or "XXS"
            self.generateStrongs(bkid=bkid, cols=cols)
            bl = self.getBooks()
            self.set("r_book", "multiple")
            if bkid not in bl:
                bls = " ".join(bl)+ " " + bkid
                self.set('ecb_booklist', bls)
            self.doStatus(_("Strong's Index generated in: {}").format(bkid))
            if self.get("c_strongsOpenIndex"):
                fpath = os.path.join(self.settings_dir, self.prjid, self.getBookFilename(bkid))
                if os.path.exists(fpath):
                    if sys.platform == "win32":
                        os.startfile(fpath)
                    elif sys.platform == "linux":
                        subprocess.call(('xdg-open', fpath))
        if sys.platform == "win32":
            dialog.set_keep_above(False)
        dialog.hide()
        
    def onInterlinearClicked(self, btn):
        if self.sensiVisible("c_interlinear"):
            if self.get("c_letterSpacing"):
                self.set("c_letterSpacing", False)
                self.doError(_("FYI: This Interlinear option is not compatible with the\n" +\
                               "'Spacing Adjustments Between Letters' on the Fonts+Script page.\n" +\
                               "So that option has just been disabled."))

    def checkUpdates(self, background=True):
        logger.debug(f"check for updates at {getcaller()}. OS is {sys.platform}")
        wid = self.builder.get_object("btn_download_update")
        wid.set_visible(False)
        if sys.platform != "win32":
            return
        version = None
        if self.noInt is None or self.noInt:
            logger.debug(f"Returning because {self.noInt=}.")
            return
        try:
            logger.debug(f"Trying to access URL to see in updates are available")
            with urllib.request.urlopen("https://software.sil.org/downloads/r/ptxprint/latest.win.json") as inf:
                info = json.load(inf)
                version = info['version']
        except (OSError, KeyError, ValueError) as e:
            logger.debug(f"{e=}")
            pass
        logger.debug(f"{version=}")
        if version is None:
            logger.debug(f"Returning because version is None.")
            return
        newv = [int(x) for x in version.split('.')]
        currv = [int(x) for x in VersionStr.split('.')]
        logger.debug(f"{newv=}, {currv=}")
        if newv <= currv:
            return
        def enabledownload():
            tip = _("A newer version of PTXprint ({}) is available.\nClick to visit download page on the website.".format(version))
            wid.set_tooltip_text(tip)
            wid.set_visible(True)
        if background:
            GLib.idle_add(enabledownload)
        else:
            enabledownload()

    def openURL(self, url):
        if self.noInt is None or self.noInt:
            self.deniedInternet()
            return
        if sys.platform == "win32":
            os.system("start \"\" {}".format(url))
        elif sys.platform == "linux":
            os.system("xdg-open \"\" {}".format(url))

    def onUpdateButtonClicked(self, btn):
        self.openURL("https://software.sil.org/ptxprint/download")

    def deniedInternet(self):
        self.doError(_("Internet Access Disabled"), secondary=_("All Internet URLs have been disabled \nusing the option on the Advanced Tab"))

    def editZvarsClicked(self, btn):
        self.rescanFRTvarsClicked(None, autosave=True)
        mpgnum = self.notebooks['Main'].index("tb_Peripherals")
        self.builder.get_object("nbk_Main").set_current_page(mpgnum)
        self.set("c_frontmatter", True)

    def editFrontMatterClicked(self, btn):
        mpgnum = self.notebooks['Main'].index("tb_ViewerEditor")
        self.builder.get_object("nbk_Main").set_current_page(mpgnum)
        pgnum = self.notebooks["Viewer"].index("scroll_FrontMatter")
        self.builder.get_object("nbk_Viewer").set_current_page(pgnum)

    def removeZerosClicked(self, btn):
        pgnum = self.notebooks["Viewer"].index("scroll_AdjList")
        buf = self.fileViews[pgnum][0]
        titer = buf.get_iter_at_mark(buf.get_insert())
        self.cursors[pgnum] = (titer.get_line(), titer.get_line_offset())
        oldlist = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        self.fileViews[pgnum][0].set_text(re.sub(r"[A-Z123]{3}\s\d.+?[-+]+0([%[].+\])?\r?\n", "", oldlist))

    def rescanFRTvarsClicked(self, btn, autosave=True):
        prjid = self.get("fcb_project")
        if autosave:
            self.onSaveEdits(None, pgid="scroll_FrontMatter") # make sure that FRTlocal has been saved
        fpath = self.configFRT()
        with universalopen(fpath) as inf:
            frtxt = inf.read()
        vlst = regex.findall(r"(\\zvar ?\|)([a-zA-Z0-9\-]+)\\\*", frtxt)
        for a, b in vlst:
            if b == "copiesprinted" and self.getvar(b) is None:
                self.setvar(b, "50")
            elif b == "toctitle":
                pass
            elif self.getvar(b) is None:
                self.setvar(b, _("<Type Value Here>"))
                
    def onEnglishClicked(self, btn):
        self.styleEditor.editMarker()
        self.userconfig.set("init", "englinks", "true" if self.get("c_useEngLinks") else "false")
        
    def onvarEdit(self, tv, path, text): #cr, path, text, tv):
        if len(text) > 0:
            model = tv.get_model()
            it = model.get_iter_from_string(path)
            if it:
                model.set(it, 1, text)

    def onzvarAdd(self, btn):
        def responseToDialog(entry, dialog, response):
            dialog.response(response)
        dialog = Gtk.MessageDialog(parent=None, message_type=Gtk.MessageType.QUESTION,
                 buttons=Gtk.ButtonsType.OK_CANCEL, text=_("Variable Name"))
        entry = Gtk.Entry()
        entry.connect("activate", responseToDialog, dialog, Gtk.ResponseType.OK)
        dbox = dialog.get_content_area()
        dbox.pack_end(entry, False, False, 0)
        dialog.set_keep_above(True)
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            k = entry.get_text()
            if self.getvar(k) is None:
                self.setvar(k, "")
        dialog.destroy()

    def onzvarDel(self, btn):
        tv = self.builder.get_object("tv_zvarEdit")
        selection = tv.get_selection()
        model, i = selection.get_selected_rows()
        for r in reversed(i):
            itr = model.get_iter(r)
            model.remove(itr)

    def onPageSizeChanged(self, btn):
        val = "cropmarks" in self.get("ecb_pagesize")
        for w in ["c_cropmarks", "c_grid"]:
            self.set(w, val)

    def onFootnoteRuleClicked(self, btn):
        status = self.sensiVisible("c_footnoterule")
        self.builder.get_object("rule_footnote").set_visible(status)

    def onXrefRuleClicked(self, btn):
        status = self.sensiVisible("c_xrefrule")
        self.builder.get_object("rule_xref").set_visible(status)

    def diglotPicListSourcesChanged(self, btn):
        status = not self.get("fcb_diglotPicListSources") == "bth"
        self.builder.get_object("c_diglot2captions").set_sensitive(status)
        self.set("c_diglot2captions", status)

    def button_release_callback(self, widget, event, data=None):
        # Experimenting with the View/Edit button to see what 
        # we can do to lock controls etc. (e.g. hold Ctrl to toggle state)
        if event.get_state() & Gdk.ModifierType.CONTROL_MASK:
            sc = widget.get_style_context()
            if sc.has_class("highlighted"):
                sc.remove_class("highlighted")
            else:
                sc.add_class("highlighted")
            return True
            # wname = Gtk.Buildable.get_name(widget)
            # if wname.startswith("c_"):
                # self.set(wname, not self.get(wname)) # this makes sure that Ctrl+Click doesn't ALSO toggle the value
            # widget.set_sensitive(False)
        # else:
            # print("Ctrl not held")

    def grab_notify_event(self, widget, event, data=None):
        pass
        # print("Got it!")
        # widget.get_style_context().add_class("inactivewidget")

    def onCatListAdd(self, btn): # Copied from 'onzvarAdd'
        def responseToDialog(entry, dialog, response):
            dialog.response(response)
        dialog = Gtk.MessageDialog(parent=None, message_type=Gtk.MessageType.QUESTION,
                 buttons=Gtk.ButtonsType.OK_CANCEL, text=_("Category Name"))
        entry = Gtk.Entry()
        entry.connect("activate", responseToDialog, dialog, Gtk.ResponseType.OK)
        dbox = dialog.get_content_area()
        dbox.pack_end(entry, False, False, 0)
        dialog.set_keep_above(True)
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            k = entry.get_text()
            self.sbcatlist.append([k, True, True])   
        dialog.destroy()

    def onCatListDel(self, btn):
        tv = self.builder.get_object("tv_sbCatEdit")
        selection = tv.get_selection()
        model, i = selection.get_selected_rows()
        for r in reversed(i):
            itr = model.get_iter(r)
            model.remove(itr)

    def onReScanCatList(self, btn):
        myDict = self.getAllBooks()
        allCats = set()
        for f in myDict.values():
            with open(f, encoding = "utf-8") as inf:
                dat = inf.read()
                for m in re.findall(r"\\cat\s+(.*?)\s*\\cat\*", dat):
                    allCats.add(m)
        self.sbcatlist.clear()
        for c in sorted(allCats):
            self.sbcatlist.append([c, True, True])
            
    def onFilterCatsClicked(self, btn):
        if btn.get_active() and not len(self.sbcatlist):
            self.onReScanCatList(None)
    
    def onCatEFtoggled(self, cell, path):
        self.sbcatlist[path][1] = not cell.get_active()

    def onCatSBtoggled(self, cell, path):
        self.sbcatlist[path][2] = not cell.get_active()

    def onSBborderClicked(self, btn):
        self.styleEditor.sidebarBorderDialog()

    def onBorderLineClicked(self, btn):
        btname = Gtk.Buildable.get_name(btn)
        if btname[-3:] in ["inn", "out"] and self.get(btname):
            self.set("c_sbBorder_lhs", False)
            self.set("c_sbBorder_rhs", False)
        elif btname[-3:] in ["lhs", "rhs"] and self.get(btname):
            self.set("c_sbBorder_inn", False)
            self.set("c_sbBorder_out", False)
        
    def onSBimageClicked(self, btn):
        btname = Gtk.Buildable.get_name(btn)
        isbg = btname == "btn_sbBGIDia"
        self.styleEditor.sidebarImageDialog(isbg)
        
    def onSBimageFileChooser(self, btn):
        picpath = os.path.join(self.settings_dir, self.prjid)
        def update_preview(dialog):
            picpath = dialog.get_preview_filename()
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(picpath, 200, 300)
            except Exception as e:
                pixbuf = None
            return pixbuf

        picfiles = self.fileChooser(_("Choose Image"),
                                  filters={"Images": {"patterns": ['*.png', '*.jpg', '*.pdf'], "mime": "application/image"}},
                                   multiple=False, basedir=picpath, preview=update_preview)
        self.set("lb_sbFilename", str(picfiles[0]) if picfiles is not None and len(picfiles) else "")

    def onDeleteTempFolders(self, btn):
        notDeleted = []
        for p in self.getConfigList(self.prjid):
            path2del = os.path.join(self.settings_dir, self.prjid, "local", "ptxprint", p)
            if os.path.exists(path2del):
                try:
                    rmtree(path2del)
                except OSError:
                    notDeleted += [path2del]
        if len(notDeleted):
            self.doError(_("Warning: Could not completely delete\nsome temporary folder(s):"),
                    secondary="\n".join(set(notDeleted)))

    def btn_RemoveSBimage(self, btn):
        self.set("lb_sbFilename", "")

    def onMarginalVersesClicked(self, btn):
        self.onSimpleClicked(btn)
        if self.sensiVisible("c_marginalverses"):
            self.builder.get_object("c_hangpoetry").set_active(False)

    def onBaseFontSizeChanged(self, btn):
        if self.loadingConfig or self.noUpdate:
            return
        if self.get("c_lockFontSize2Baseline"):
            lnsp = float(self.get("s_fontsize")) / self.font2baselineRatio
            self.noUpdate = True
            self.set("s_linespacing", lnsp)
            self.noUpdate = False
        else:
            self.updateFont2BaselineRatio()

    def onBaseLineSpacingChanged(self, btn):
        if self.loadingConfig or self.noUpdate:
            return
        if self.get("c_lockFontSize2Baseline"):
            fntsz = float(self.get("s_linespacing")) * self.font2baselineRatio
            self.noUpdate = True
            self.set("s_fontsize", fntsz)
            self.noUpdate = False
        else:
            self.updateFont2BaselineRatio()
            
    def onLockRatioClicked(self, btn):
        if self.loadingConfig:
            return
        if self.get("c_lockFontSize2Baseline"):
            self.updateFont2BaselineRatio()

    def onCreateDiffclicked(self, btn):
        self.docreatediff = True
        self.onOK(None)
        
    def onPaperWeightChanged(self, btn):
        if self.loadingConfig or self.noUpdate:
            return
        thck = int(float(self.get("s_paperWeight")) / 0.8)
        self.noUpdate = True
        self.set("s_paperThickness", thck)
        self.noUpdate = False
        
    def onpaperThicknessChanged(self, btn):
        if self.loadingConfig or self.noUpdate:
            return
        wght = int(float(self.get("s_paperThickness")) * 0.8)
        self.noUpdate = True
        self.set("s_paperWeight", wght)
        self.noUpdate = False
    
    # def onLetterSpacingClicked(self, btn):
        # if self.loadingConfig or self.noUpdate:
            # return
        # self.noUpdate = True
        # if self.get("c_hyphenate"):
            # self.set("c_hyphenate", False)
        # self.noUpdate = False

    # def onHyphenateClicked(self, btn):
        # if self.loadingConfig or self.noUpdate:
            # return
        # self.noUpdate = True
        # if self.get("c_letterSpacing"):
            # self.set("c_letterSpacing", False)
        # self.noUpdate = False

    def onMarginEnterNotifyEvent(self, btn, *args):
        self.highlightMargin(btn, True)

    def onMarginLeaveNotifyEvent(self, btn, *args):
        self.highlightMargin(btn, False)

    def highlightMargin(self, btn, highlightMargin=True):
        n = Gtk.Buildable.get_name(btn)
        wid = "img_" + n[2:]
        for w in ["topmargin", "bottommargin", "footerposition", "headerposition", "margins", "rhruleposition", "blanktop", "blankbottom"]:
            self.builder.get_object(f"img_{w}").set_visible(False)
        if highlightMargin:
            for b in ["1False", "2False", "2True"]:
                self.builder.get_object(f"img_Bottom{b}").set_visible(False)
            for t in ["1FalseFalse", "1FalseTrue", "2FalseFalse", "2FalseTrue", "2TrueFalse", "2TrueTrue"]:
                self.builder.get_object(f"img_Top{t}").set_visible(False)
            if wid in ["img_bottommargin", "img_footerposition"]:
                self.builder.get_object("img_blanktop").set_visible(True)
            else:
                self.builder.get_object("img_blankbottom").set_visible(True)
            self.builder.get_object(wid).set_visible(True)
        else:
            self.updateMarginGraphics()
