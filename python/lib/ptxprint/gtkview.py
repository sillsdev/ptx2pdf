#!/usr/bin/python3

import sys, os, re, regex, subprocess, traceback, ssl
try:
    import gi
except ModuleNotFoundError:
    print("PTXprint is in an environment where it can only run headless. Make sure -P is in the command line options")
    sys.exit(1)
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Poppler', '0.18')
from shutil import rmtree, copy2
import datetime, time, locale, urllib.request, json, hashlib
from ptxprint.utils import universalopen, refKey, refSort, chgsHeader, saferelpath, startfile
from gi.repository import Gdk, Gtk, Pango, GObject, GLib, GdkPixbuf

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    # sys.stdout = open(os.devnull, "w")
    # sys.stdout = open("D:\Temp\ptxprint-sysout.tmp", "w")
    # sys.stderr = sys.stdout
    pass
else:
    gi.require_version('GtkSource', '3.0')
from gi.repository import GtkSource, Poppler, Gio
import cairo

import xml.etree.ElementTree as et
from ptxprint.font import TTFont, initFontCache, fccache, FontRef, parseFeatString
from ptxprint.view import ViewModel, Path, VersionStr, GitVersionStr
from ptxprint.gtkutils import getWidgetVal, setWidgetVal, setFontButton, makeSpinButton, doError
from ptxprint.utils import APP, setup_i18n, brent, xdvigetpages, allbooks, books, \
            bookcodes, chaps, print_traceback, pt_bindir, pycodedir, getcaller, runChanges, \
            _, f_, textocol, _allbkmap, coltotex, UnzipDir, convert2mm, extraDataDir, getPDFconfig, \
            _categoryColors, _bookToCategory, getResourcesDir
from ptxprint.ptsettings import ParatextSettings
from ptxprint.gtkpiclist import PicList, dispLocPreview, getLocnKey
from ptxprint.piclist import Piclist
from ptxprint.gtkstyleditor import StyleEditorView
from ptxprint.styleditor import aliases
from ptxprint.runjob import isLocked, unlockme
from ptxprint.texmodel import TexModel
from ptxprint.modelmap import ModelMap
from ptxprint.minidialog import MiniDialog
from ptxprint.dbl import UnpackBundle, GetDBLName
from ptxprint.texpert import TeXpert
from ptxprint.picselect import ThumbnailDialog, unpackImageset, getImageSets
from ptxprint.hyphen import Hyphenation
from ptxprint.accelerate import onTextEditKeypress
from ptxprint.gtkadjlist import AdjListView
from ptxprint.pdf_viewer import PDFViewer, Paragraphs
from ptxprint.tatweel import TatweelDialog
from ptxprint.gtkpolyglot import PolyglotSetup
from ptxprint.report import Report
import ptxprint.scriptsnippets as scriptsnippets
import configparser, logging
import webbrowser
import unicodedata
from threading import Thread
from base64 import b64encode, b64decode
from io import BytesIO
from dataclasses import asdict
# import zipfile
from zipfile import ZipFile, BadZipFile, ZIP_DEFLATED
from usfmtc.reference import Ref, Environment
from collections import defaultdict


logger = logging.getLogger(__name__)

ssl._create_default_https_context = ssl._create_unverified_context
pdfre = re.compile(r".+[\\/](.+\.pdf)")


# xmlstarlet sel -t -m '//iso_15924_entry' -o '"' -v '@alpha_4_code' -o '" : "' -v '@name' -o '",' -n /usr/share/xml/iso-codes/iso_15924.xml
# but remove everything not in the range 100-499
_allscripts = { "Zyyy" : "Default", "Adlm" : "Adlam", "Aghb" : "Caucasian Albanian", "Ahom" : "Ahom, Tai Ahom", 
    "Arab" : "Arabic", "Armi" : "Imperial Aramaic", "Armn" : "Armenian", "Avst" : "Avestan",
    "Bali" : "Balinese",
    "Bamu" : "Bamum", "Bass" : "Bassa Vah", "Batk" : "Batak", "Beng" : "Bengali", "Bhks" : "Bhaiksuki", "Bopo" : "Bopomofo",
    "Brah" : "Brahmi", "Brai" : "Braille", "Bugi" : "Buginese", "Buhd" : "Buhid",
    "Cakm" : "Chakma", "Cans" : "Canadian Aboriginal Syllabics",
    "Cari" : "Carian", "Cham" : "Cham", "Cher" : "Cherokee", "Chrs" : "Chorasmian", "Copt" : "Coptic", 
    "Cpmn" : "Cypro-Minoan", "Cprt" : "Cypriot", "Cyrl" : "Cyrillic",
    "Deva" : "Devanagari", "Diak" : "Dives Akuru",  "Dogr" : "Dogra", "Dsrt" : "Deseret (Mormon)",
    "Elba" : "Elbasan", "Elym" : "Elymiac", "Ethi" : "Ethiopic (Geʻez)",
    "Geor" : "Georgian (Mkhedruli)", "Glag" : "Glagolitic", "Gong" : "Gunjala-Gondi", "Gonm" : "Masaram-Gondi",
    "Goth" : "Gothic", "Gran" : "Grantha", "Grek" : "Greek", "Gujr" : "Gujarati", "Guru" : "Gurmukhi",
    "Hang" : "Hangul (Hangŭl, Hangeul)", "Hano" : "Hanunoo (Hanunóo)", 
    "Hans" : "Han (Simplified)", "Hant" : "Han (Traditional)", "Hatr" : "Hatran", "Hebr" : "Hebrew",
    "Hira" : "Hiragana", "Hmng" : "Pahawh-Hmong",
    "Hung" : "Old Hungarian (Runic)",
    "Ital" : "Old Italic (Etruscan, Oscan)",
    "Java" : "Javanese",
    "Kali" : "Kayah-Li", "Kana" : "Katakana", "Kawi" : "Kawi", "Khar" : "Kharoshthi",
    "Khmr" : "Khmer", "Khoj" : "Khojki", "Kits" : "Khitan (small)", "Knda" : "Kannada",
    "Kthi" : "Kaithi",
    "Lana" : "Tai Tham (Lanna)", "Laoo" : "Lao",
    "Latn" : "Latin", "Leke" : "Leke", "Lepc" : "Lepcha (Róng)", "Limb" : "Limbu", "Lina" : "Linear A",
    "Linb" : "Linear B", "Lisu" : "Lisu (Fraser)", "Lyci" : "Lycian", "Lydi" : "Lydian",
    "Mahj" : "Mahajani", "Maka" : "Makasar", 
    "Mand" : "Mandaic, Mandaean", "Mani" : "Manichaean", "Marc" : "Marchen", "Medf" : "Medefaidrin",
    "Mend" : "Mende Kikakui", "Merc" : "Meroitic Cursive", "Mero" : "Meroitic Hieroglyphs", 
    "Mlym" : "Malayalam", "Mong" : "Mongolian", "Mroo" : "Mro, Mru", "Mtei" : "Meitei-Mayek", "Mult" : "Multani", 
    "Mymr" : "Myanmar (Burmese)",
    "Nagm" : "Nag Mundari", "Nand" : "Nandinagari", "Narb" : "North Arabian (Ancient)", "Nbat" : "Nabataean", "Newa" : "New (Newar, Newari)",
    "Nkoo" : "N’Ko", "Nshu" : "Nüshu",
    "Ogam" : "Ogham", "Olck" : "Ol Chiki (Ol Cemet’, Santali)", 
    "Orkh" : "Old Turkic, Orkhon Runic", "Orya" : "Oriya", "Osge" : "Osage", "Osma" : "Osmanya", "Ougr" : "Old Uyghur", 
    "Palm" : "Palmyrene",
    "Pauc" : "Pau Cin Hau", "Perm" : "Old Permic", "Phag" : "Phags-pa", "Phli" : "Inscriptional Pahlavi", "Phlp" : "Psalter Pahlavi",
    "Phnx" : "Phoenician", "Plrd" : "Miao (Pollard)", "Prti" : "Inscriptional Parthian",
    "Rjng" : "Rejang (Redjang, Kaganga)", "Rohg" : "Hanifi Rohingya",
    "Runr" : "Runic",
    "Samr" : "Samaritan", "Sarb" : "Old South Arabian", "Saur" : "Saurashtra", "Shaw" : "Shavian (Shaw)", 
    "Shrd" : "Sharada", "Sidd" : "Siddham, Siddhamātṛkā", "Sind" : "Sindhi, Khudawadi", "Sinh" : "Sinhala",
    "Sogd" : "Sogdian", "Sogo" : "Old Sogdian", "Sora" : "Sora-Sompeng",
    "Sund" : "Sundanese", "Sylo" : "Syloti Nagri", "Syrc" : "Syriac",
    "Tagb" : "Tagbanwa", "Takr" : "Takri, Ṭāṅkrī", "Tale" : "Tai Le", "Talu" : "New-Tai-Lue", 
    "Taml" : "Tamil", "Tavt" : "Tai Viet", "Telu" : "Telugu", "Tfng" : "Tifinagh (Berber)",
    "Tglg" : "Tagalog (Baybayin, Alibata)", "Thaa" : "Thaana", "Thai" : "Thai", "Tibt" : "Tibetan", "Tirh" : "Tirhuta", "Tnsa" : "Tangsa",
    "Vaii" : "Vai", "Vith" : "Vithkuqi",
    "Wara" : "Warang-Citi", "Wcho" : "Wancho", "Xpeo" : "Old Persian",
    "Yezi" : "Yezidi", "Yiii" : "Yi",
    "Zanb" : "Zanabazar Square", "Zzzz" : "Uncoded script"
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
    "Kore" : "ko"   # "Korean (Hangul+Han)",

  # "Hanb" : "zh",  # "Han with Bopomofo",
  # "Khmr" : "km",  # "Khmer",
  # "Mymr" : "my",  # "Myanmar (Burmese)",    
  # "Thai" : "th"   # "Thai"
}
# Note that ls_digits (in the glade file) is used to map these "friendly names" to the "mapping table names" (especially the non-standard ones)
_alldigits = [ "Default", "Adlam", "Ahom", "Arabic-Indic", "Balinese", "Bengali", "Bhaiksuki", "Brahmi", "Chakma", "Cham", "Devanagari", 
    "Ethiopic", "Extended-Arabic", "Fullwidth", "FixHyphens-Non", "Gujarati", "Gunjala-Gondi", "Gurmukhi", "Hanifi-Rohingya", "Hebrew", "Javanese", "Kannada", 
    "Kayah-Li", "Khmer", "Khudawadi", "Lao", "Lepcha", "Limbu", "Malayalam", "Masaram-Gondi", "Meetei-Mayek", "Modi", "Mongolian", 
    "Mro", "Myanmar", "Myanmar-Shan", "Myanmar-Tai-Laing", "New-Tai-Lue", "Newa", "Nko", "Nyiakeng-Puachue-Hmong", "Ol-Chiki", "Oriya", 
    "Osmanya", "Pahawh-Hmong", "Rumi", "Saurashtra", "Sharada", "Sinhala-Lith", "Sora-Sompeng", "Sundanese", "Tai-Tham-Hora", 
    "Tai-Tham-Tham", "Takri", "Tamil", "Telugu", "Thai", "Tibetan", "Tirhuta", "Vai", "Wancho", "Warang-Citi", "Western-Cham"]

_progress = {
    'gp' : _("Gathering pics..."),
    'pr' : _("Processing..."),
    'lo' : _("Laying out..."),
    'xp' : _("Making PDF..."),
    'fn' : _("Finishing..."),
    'al' : _("Analyzing Layout...")
}

_ui_minimal = """
btn_menu bx_statusBar t_find
btn_menu_showPDF l_menu_showPDF
btn_menu_level btn_menu_lang btn_menu_feedback  btn_menu_donate l_menu_level l_menu_uilang
fcb_filterXrefs c_quickRun
tb_Basic lb_Basic
fr_projScope l_project fcb_project l_projectFullName r_book_single ecb_book 
l_chapfrom l_chapto t_chapfrom t_chapto 
r_book_multiple btn_chooseBooks ecb_booklist 
fr_SavedConfigSettings l_cfgName ecb_savedConfig t_savedConfig btn_saveConfig btn_lockunlock t_password
tb_Layout lb_Layout
fr_pageSetup l_pageSize ecb_pagesize l_fontsize s_fontsize
fr_2colLayout c_doublecolumn gr_doubleColumn c_verticalrule 
tb_Font lb_Font
fr_FontConfig l_fontR bl_fontR tv_fontFamily fcb_fontFaces t_fontSearch 
tb_Help lb_Help
fr_Help
r_generate_selected l_generate_booklist r_generate_all c_randomPicPosn
l_statusLine btn_dismissStatusLine
l_artStatusLine
s_pdfZoomLevel btn_page_first btn_page_previous t_pgNum btn_page_next btn_page_last
b_reprint btn_closePreview l_pdfContents l_pdfPgCount l_pdfPgsSprds tv_pdfContents
c_pdfadjoverlay c_pdfparabounds c_bkView scr_previewPDF scr_previewPDF bx_previewPDF
btn_prvOpenFolder btn_prvSaveAs btn_prvOpen btn_prvPrint
btn_showSettings
""".split() # btn_reloadConfig   btn_imgClearSelection

_ui_enable4diglot2ndary = """
l_fontB bl_fontB l_fontI bl_fontI l_fontBI bl_fontBI 
tb_NotesRefs lb_NotesRefs tb_general
tb_footnotes c_includeFootnotes l_fnPos  c_fneachnewline
tb_xrefs     c_includeXrefs     l_xrPos  c_xreachnewline
c_fontFake fr_fontFake l_fontBold s_fontBold l_fontItalic s_fontItalic
fr_writingSystem l_textDirection fcb_textDirection fcb_script l_script
tb_Body lb_Body
fr_BeginEnding c_bookIntro c_introOutline c_filterGlossary c_ch1pagebreak
fr_IncludeScripture c_mainBodyText gr_mainBodyText c_chapterNumber c_justify c_sectionHeads
c_verseNumbers c_preventorphans c_hideEmptyVerses c_elipsizeMissingVerses
""".split()

# bx_fnOptions bx_xrOptions 
_ui_basic = """
t_configName l_configNameMsg l_projectNameMsg btn_cfg_ok btn_cfg_cancel
r_book_module btn_chooseBibleModule lb_bibleModule
btn_DBLbundleDiglot1 btn_DBLbundleDiglot2 btn_locateDBLbundle t_DBLprojName 
lb_DBLbundleFilename lb_DBLbundleNameDesc lb_DBLdownloads lb_openBible
btn_deleteConfig l_notes t_configNotes t_invisiblePassword
c_mirrorpages c_pagegutter s_pagegutter
l_linespacing s_linespacing
bx_onOffGridSettings l_gridAligned l_gridVariable
l_colgutterfactor s_colgutterfactor
c_noGrid c_variableLineSpacing c_allowUnbalanced
fr_margins l_margins s_margins l_topmargin s_topmargin l_bottommargin s_bottommargin
c_rhrule l_rhruleposition s_rhruleposition
l_fontB bl_fontB l_fontI bl_fontI l_fontBI bl_fontBI 
c_fontFake fr_fontFake l_fontBold s_fontBold l_fontItalic s_fontItalic
fr_writingSystem l_textDirection fcb_textDirection fcb_script l_script
tb_Body lb_Body
fr_BeginEnding c_bookIntro c_introOutline c_filterGlossary c_ch1pagebreak c_pagebreakAllChs
fr_IncludeScripture c_mainBodyText gr_mainBodyText c_chapterNumber c_justify c_sectionHeads
c_verseNumbers c_preventorphans c_hideEmptyVerses c_elipsizeMissingVerses
tb_NotesRefs lb_NotesRefs tb_general
tb_footnotes c_includeFootnotes l_fnPos  c_fneachnewline
tb_xrefs     c_includeXrefs     l_xrPos  c_xreachnewline
tb_HeadFoot lb_HeadFoot
fr_Header l_hdrleft ecb_hdrleft l_hdrcenter ecb_hdrcenter l_hdrright ecb_hdrright
fr_Footer l_ftrcenter ecb_ftrcenter
tb_Pictures lb_Pictures
c_includeillustrations tb_settings lb_settings fr_inclPictures gr_IllustrationOptions c_cropborders
c_useCustomFolder btn_selectFigureFolder lb_selectFigureFolder
l_homePage lb_homePage btn_createZipArchiveXtra btn_deleteTempFiles btn_about
l_complexScript btn_scrsettings 
rule_marginalVerses c_marginalverses l_marginVrsPosn fcb_marginVrsPosn l_columnShift s_columnShift
fr_layoutSpecialBooks l_showChaptersIn c_show1chBookNum c_showNonScriptureChapters l_glossaryMarkupStyle fcb_glossaryMarkupStyle
tb_studynotes fr_txlQuestions c_txlQuestionsInclude gr_txlQuestions l_txlQuestionsLang t_txlQuestionsLang
c_txlQuestionsOverview c_txlQuestionsNumbered c_txlQuestionsRefs rule_txl l_txlExampleHead l_txlExample
tb_Peripherals bx_ToC c_autoToC t_tocTitle c_frontmatter
fr_variables gr_frontmatter scr_zvarlist tv_zvarEdit col_zvar_name cr_zvar_name col_zvar_value cr_zvar_value
tb_Finishing fr_pagination l_pagesPerSpread fcb_pagesPerSpread l_sheetSize ecb_sheetSize
fr_compare l_selectDiffPDF btn_selectDiffPDF c_onlyDiffs lb_diffPDF c_createDiff
btn_importSettings btn_importSettingsOK btn_importCancel r_impSource_pdf btn_impSource_pdf lb_impSource_pdf
r_impTarget_folder btn_tgtFolder
r_impTarget_prjcfg l_tgtProject ecb_targetProject l_tgtConfig ecb_targetConfig t_targetConfig
nbk_Import r_impSource_config l_impProject fcb_impProject l_impConfig ecb_impConfig
btn_resetConfig tb_impPictures tb_impLayout tb_impFontsScript tb_impStyles tb_impOther
bx_impPics_basic c_impPicsAddNew c_impPicsDelOld c_sty_OverrideAllStyles 
gr_impOther c_oth_Body c_oth_NotesRefs c_oth_HeaderFooter c_oth_ThumbTabs 
c_oth_Advanced c_oth_FrontMatter c_oth_OverwriteFrtMatter c_oth_Cover 
c_impPictures c_impLayout c_impFontsScript c_impStyles c_impOther c_oth_customScript
btn_adjust_diglot btn_seekPage2fill_previous btn_seekPage2fill_next
""".split()
# tb_Diglot fr_diglot gr_diglot c_diglot l_diglotSecProject fcb_diglotSecProject l_diglotSecConfig ecb_diglotSecConfig 
# lpolyfraction_ spolyfraction_ tb_diglotSwitch btn_diglotSwitch

_ui_experimental = """
""".split()

# every control that doesn't cause a config change
_ui_unchanged = """r_book t_chapto t_chapfrom ecb_booklist ecb_savedConfig l_statusLine
c_bkView s_pdfZoomLevel t_pgNum b_reprint fcb_project ecb_savedConfig
l_menu_level btn_prvOpenFolder btn_prvSaveAs btn_prvOpen btn_prvPrint 
""".split()

# removed from list above: 
# r_pictureRes_High r_pictureRes_Low
# gr_importFrontPDF gr_importBackPDF 
# c_inclFrontMatter btn_selectFrontPDFs lb_inclFrontMatter
# c_inclBackMatter btn_selectBackPDFs lb_inclBackMatter
# btn_editFrontMatter

_fullpage = {"F": "full", "P": "page"}

_clr = {"margins" : "toporange",        "topmargin" : "topred", "headerposition" : "toppurple", "rhruleposition" : "topgreen",
        "margin2header" : "topblue", "bottommargin" : "botred", "footerposition" : "botpurple", "footer2edge" : "botblue"}

_ui_noToggleVisible = ("btn_resetDefaults", "btn_deleteConfig", "lb_details", "tb_details", "lb_checklist", "tb_checklist", 
                       "ex_styNote", "l_diglotSerialBooks", "t_diglotSerialBooks") # toggling these causes a crash
                       # "lb_footnotes", "tb_footnotes", "lb_xrefs", "tb_xrefs")  # for some strange reason, these are fine!

_ui_keepHidden = ["btn_download_update", "l_extXrefsComingSoon", "tb_Logging", "lb_Logging", "tb_PoD", "lb_Expert",
                  "bx_statusMsgBar", "fr_plChecklistFilter", "l_picListWarn1", "l_picListWarn2", "col_noteLines", 
                  "l_thumbVerticalL", "l_thumbVerticalR", "l_thumbHorizontalL", "l_thumbHorizontalR"]
                  # "col_dibackcol", "fcb_diglotSecProject", "ecb_diglotSecConfig", "c_diglot2captions", 
                  # "spolyfraction_", "btn_diglotSwitch", "btn_adjust_diglot", "l_diglotSecProject",
                  # "l_dibackcol", "l_diglotSecConfig", "lpolyfraction_", "tb_diglotSwitch"]  # "c_pdfGridlines" "bx_imageMsgBar", 

_uiLevels = {
    2 : _ui_minimal,
    4 : _ui_basic,
}

_showActiveTabs = {
    "c_includeillustrations" : ["tb_Pictures"],
    "c_diglot" :               ["tb_Diglot", "fr_diglot"], #, "btn_diglotSwitch"],
    "c_thumbtabs" :            ["tb_TabsBorders", "fr_tabs"],
    "c_useOrnaments" :         ["tb_TabsBorders", "fr_borders"],
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
    "r_border": {
        "r_border_text":       ["lb_style_textborder"],
        "r_border_page":       ["lb_style_pageborder"],
        "r_border_pdf":        ["btn_selectPageBorderPDF", "lb_inclPageBorder", "c_borderPageWide"]},
    "r_xrpos": {
        "r_xrpos_centre" :     ["l_internote", "s_internote", "fr_colXrefs", "l_xrColWid", "s_centreColWidth"]}, 
    "r_pictureRes": {
        "r_pictureRes_High" :  ["btn_requestIllustrations"]}, 
        
    "noGrid" :                 ["c_variableLineSpacing"],
    "c_mainBodyText" :         ["gr_mainBodyText"],
    "c_doublecolumn" :         ["gr_doubleColumn", "r_fnpos_column"],
    "c_useFallbackFont" :      ["btn_findMissingChars", "t_missingChars", "l_fallbackFont", "bl_fontExtraR"],
    "c_includeFootnotes" :     ["c_fneachnewline", "c_fnOverride", "c_fnautocallers", "t_fncallers", 
                                "btn_resetFNcallers", "c_fnomitcaller", "c_fnpageresetcallers",
                                "lb_style_f", "l_fnPos", "r_fnpos_normal", "r_fnpos_column", "r_fnpos_endnote"],
    "c_useXrefList" :          ["gr_extXrefs"],
    "c_strongsShowInText" :    ["c_strongsShowAll"],
    
    "c_includeillustrations" : ["gr_IllustrationOptions", "lb_details", "tb_details", "tb_checklist"],
    "c_diglot" :               ["gr_diglot", "r_hdrLeft_Pri", "r_hdrCenter_Pri", "r_hdrRight_Pri",
                                "r_ftrCenter_Pri", "r_hdrLeft_Sec", "r_hdrCenter_Sec", "r_hdrRight_Sec", "r_ftrCenter_Sec"], # "fcb_diglotPicListSources", 
    "c_diglotSeparateNotes" :  ["c_diglotNotesRule", "c_diglotJoinVrule"],
    "c_diglotNotesRule" :      ["c_diglotJoinVrule"],
    "c_useOrnaments" :         ["gr_borders"],

    "c_pagegutter" :           ["s_pagegutter", "c_outerGutter"],
    "c_verticalrule" :         ["l_colgutteroffset", "s_colgutteroffset"],
    "c_rhrule" :               ["s_rhruleposition"],
    "c_introOutline" :         ["c_prettyIntroOutline"],
    # "c_ch1pagebreak" :         ["c_pagebreakAllChs"],
    "c_sectionHeads" :         ["c_parallelRefs", "lb_style_s", "lb_style_r"],
    "c_parallelRefs" :         ["lb_style_r"],
    "c_useChapterLabel" :      ["t_clBookList", "l_clHeading", "t_clHeading", "c_optimizePoetryLayout"],
    "c_differentColLayout" :   ["t_differentColBookList"],
    "c_autoToC" :              ["t_tocTitle", "gr_toc", "l_toc", "l_leaderStyle", "fcb_leaderStyle"],
    "c_hideEmptyVerses" :      ["c_elipsizeMissingVerses"],
    "c_marginalverses" :       ["l_marginVrsPosn", "fcb_marginVrsPosn", "l_columnShift", "s_columnShift"],
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
    "c_inclPageBorder" :       ["gr_pageBorder"],
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
    "c_txlQuestionsInclude":   ["gr_txlQuestions"],
    # "c_txlQuestionsOverview":  ["c_txlBoldOverview"],
    "c_filterCats":            ["gr_filterCats"],
    "c_makeCoverPage":         ["bx_cover", "c_coverSeparatePDF"],
    "c_inclSpine":             ["gr_spine"],
    "c_overridePageCount":     ["s_totalPages"],
    "r_impSource": {
        "r_impSource_pdf":     ["btn_impSource_pdf", "lb_impSource_pdf"],
        "r_impSource_config":  ["fcb_impProject", "ecb_impConfig", "l_impProject", "l_impConfig", ]},
    "r_impTarget": {
        "r_impTarget_folder":  ["btn_tgtFolder", "lb_tgtFolder"],
        "r_impTarget_prjcfg":  ["ecb_targetProject", "ecb_targetConfig", "l_tgtProject", "l_tgtConfig", ]},
    "c_impPictures":           ["tb_impPictures"],
    "r_impPics": {
        "r_impPics_elements":  ["gr_picElements"]},
    "c_impOther":              ["gr_impOther"],
    "c_oth_FrontMatter":       ["c_oth_OverwriteFrtMatter"],
    "c_oth_Cover":             ["c_oth_OverwriteFrtMatter"],
    "c_impEverything":         ["c_impPictures", "c_impLayout", "c_impFontsScript", "c_impStyles", "c_impOther"],
    "r_sbiPosn": {
        "r_sbiPosn_above":     ["fcb_sbi_posn_above"],
        "r_sbiPosn_beside":    ["fcb_sbi_posn_beside"],
        "r_sbiPosn_cutout":    ["fcb_sbi_posn_cutout", "s_sbiCutoutLines", "l_sbiCutoutLines"]},
    "c_coverBorder":           ["fcb_coverBorder", "col_coverBorder", "l_coverBorder"],
    "c_coverShading":          ["col_coverShading", "s_coverShadingAlpha", "l_coverShading"],
    "c_coverSelectImage":      ["fcb_coverImageSize", "c_coverImageFront", "s_coverImageAlpha", "btn_coverSelectImage", "lb_coverImageFilename"],
    "c_layoutAnalysis":        ["btn_findButton"],
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
    "c_inclSpine":             ["c_coverCropMarks"],
    "c_lockUI4Layout":         ["ecb_pagesize", "c_mirrorpages", "s_indentUnit", "s_fontsize", "btn_adjust_spacing",
                                "c_lockFontSize2Baseline", "c_pagegutter", "s_pagegutter", "s_linespacing", 
                                "btn_adjust_spacing", "c_outerGutter", "c_doublecolumn", "s_colgutterfactor", 
                                "fr_margins", "tb_Font", "tb_StyleEditor"],
    "r_xrpos": {
        "r_xrpos_below" :     [],
        "r_xrpos_blend" :     ["l_internote", "s_internote"],
        "r_xrpos_centre" :    []},
    "c_boxPadSymmetrical":     ["s_sbBoxPadL", "s_sbBoxPadR", "s_sbBoxPadB"],
    "c_bdrPadSymmetrical":     ["s_sbBdrPadL", "s_sbBdrPadR", "s_sbBdrPadB"],
}
_object_classes = {
    "printbutton": ("b_print", "btn_refreshFonts", "btn_createZipArchiveXtra", "btn_Generate",
                    "b_reprint", "btn_refreshCaptions", "btn_adjust_diglot"), 
    "sbimgbutton": ("btn_sbFGIDia", "btn_sbBGIDia"),
    "smallbutton": ("btn_dismissStatusLine", "btn_imgClearSelection", "btn_requestPermission", "btn_downloadPics",
                    "btn_requestIllustrations", "btn_requestIllustrations2", "c_createDiff", "c_quickRun", "btn_addMaps2",
                    "btn_DBLbundleDiglot1", "btn_DBLbundleDiglot2"),
    "tinybutton":  ("col_noteLines",),
    "fontbutton":  ("bl_fontR", "bl_fontB", "bl_fontI", "bl_fontBI"),
    "mainnb":      ("nbk_Main", ),
    "viewernb":    ("nbk_Viewer", "nbk_PicList"),
    "scale-slider":("s_viewEditFontSize", "s_coverShadingAlpha", "s_coverImageAlpha"), # "spolyfraction_", 
    "thumbtabs":   ("l_thumbVerticalL", "l_thumbVerticalR", "l_thumbHorizontalL", "l_thumbHorizontalR"),
    "stylinks":    ("lb_style_c", "lb_style__v", "lb_style_s", "lb_style_r", "lb_style_v", "lb_style_f", "lb_style_x", "lb_style_fig",
                    "lb_style_rb", "lb_style_gloss|rb", "lb_style_toc3", "lb_style_x-credit", "lb_omitPics",
                    "lb_style_cat:coverfront|esb", "lb_style_cat:coverback|esb",
                    "lb_style_cat:coverspine|esb", "lb_style_cat:coverwhole|esb", ), 
    "stybutton":   ("btn_resetCopyright", "btn_rescanFRTvars", "btn_resetColophon", 
                    "btn_resetFNcallers", "btn_resetXRcallers", "btn_styAdd", "btn_styEdit", "btn_styDel", 
                    "btn_styReset", "btn_refreshFonts", "btn_plAdd", "btn_plDel", 
                    "btn_plGenerate", "btn_downloadPics", "btn_resetTabGroups", "btn_adjust_spacing", 
                    "btn_adjust_top", "btn_adjust_bottom",  
                    "btn_resetGrid", "btn_refreshCaptions", "btn_sb_rescanCats") # "btn_reloadConfig", 
}

_pgpos = {
    "Top": "t", 
    "Bottom": "b", 
    "Below Notes": "B", 
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
_allpgids = ["tb_FrontMatter", "tb_AdjList", "tb_FinalSFM", 
             "tb_TeXfile", "tb_XeTeXlog", "tb_Settings1", "tb_Settings2", "tb_Settings3"]

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

_notebooks = ("Main", "Viewer", "PicList", "fnxr", "Import", "Advanced")

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
    # 'state-set': ("Switch",),
    'row-activated': ("TreeView",),
}

_olst = ["fr_SavedConfigSettings", "tb_Layout", "tb_Font", "tb_Body", "tb_NotesRefs", "tb_HeadFoot", "tb_Pictures",
         "tb_Advanced", "tb_Logging", "tb_TabsBorders", "tb_Diglot", "tb_StyleEditor", "tb_Viewer", 
         "tb_Peripherals", "tb_Cover", "tb_Finishing", "tb_PoD"]  # "tb_Help"

_dlgtriggers = {
    "dlg_multiBookSelect":  "onChooseBooksClicked",
    "dlg_about":            "onAboutClicked",
    "dlg_password":         "onLockUnlockSavedConfig",
    "dlg_generatePL":       "onGeneratePicListClicked",
    "dlg_generateFRT":      "onGenerateClicked",
    "dlg_fontChooser":      "getFontNameFace",
    "dlg_features":         "onFontFeaturesClicked",
    "dlg_multProjSelector": "onChooseTargetProjectsClicked",
    "dlg_gridsGuides":      "adjustGridSettings",
    "dlg_DBLbundle":        "onDBLbundleClicked",
    "dlg_overlayCredit":    "onOverlayCreditClicked",
    "dlg_sbPosition":       "onSBpositionClicked",
    "dlg_strongsGenerate":  "onGenerateStrongsClicked",
    "dlg_generateCover":    "onGenerateCoverClicked",
    "dlg_borders":          "onSBborderClicked",
    # "dlg_preview":          "????",
}

mac_menu = {
    "PTXprint": {
        "Quit": 'onDestroy',
    },
    # "Help": {
    #     "About": 'do_help',     # switch to the help tab or create a dialog
    # }
}

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

def getsign(b, v, a, m=""):
    r = ""
    if b > 0 and b < v:
        r = "-"
    if v < a:
        r = "+" + r
    return r

def dummy(*a):
    pass

class GtkViewModel(ViewModel):

    def __init__(self, prjtree, userconfig, scriptsdir, args=None):
        # logger.debug("Starting init in gtkview")
        super(GtkViewModel, self).__init__(prjtree, userconfig, scriptsdir, args)
        self.lang = args.lang if args.lang is not None else 'en'
        self.args = args
        self.initialised = False

    def _add_mac_menu(self, app, menudesc=mac_menu, parent=None):
        if parent is None:
            parent = Gio.Menu()
        for k, v in menudesc.items():
            if isinstance(v, str):
                action = Gio.SimpleAction.new(v, None)
                action.connect("activate", getattr(self, v, None))
                app.add_action(action)
                parent.append(k, f"app.{v}")
                print(f"Appending action {k} to {v}")
            else:
                submenu = Gio.Menu()
                self._add_mac_menu(app, menudesc=v, parent=submenu)
                parent.append_submenu(k, submenu)
        return parent

    def setup_ini(self):
        # logger.debug("Starting setup_ini in gtkview")
        if sys.platform.startswith("win"):
            # import ctypes
            from ctypes import windll
            # Set DPI awareness
            try:
                windll.shcore.SetProcessDpiAwareness(2)  # DPI_AWARENESS_PER_MONITOR_AWARE
            except:
                windll.user32.SetProcessDPIAware()  # Fallback for older Windows versions

        if not self.args.quiet:
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                if sys.platform == "darwin":
                    runsplash_path = os.path.join(sys._MEIPASS, '..', 'MacOS', 'runsplash')
                    runsplash_path = os.path.abspath(runsplash_path)
                else:
                    runsplash_path = os.path.join(sys._MEIPASS, 'runsplash')
                cmds = [runsplash_path, os.path.join(pycodedir(), 'splash.glade')]
            else:
                cmds = [sys.executable, os.path.join(pycodedir(), "runsplash.py"), os.path.join(pycodedir(), "splash.glade")]
            self.splash = subprocess.Popen(cmds)
        else:
            self.splash = None

        self._setup_css()
        self.radios = {}
        GLib.set_prgname("ptxprint")
        gladefile = os.path.join(pycodedir(), "ptxprint.glade")
        GObject.type_register(GtkSource.View)
        GObject.type_register(GtkSource.Buffer)
        tree = et.parse(gladefile)
        self.allControls = []
        modelbtns = set([v.widget for v in ModelMap.values() if v.widget is not None and v.widget.startswith("btn_")])
        self.btnControls = set()
        self.finddata = {}
        self.widgetnames = {}
        self.setup_book_button_styles()
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
        logger.debug("Loading glade")
        xml_text = et.tostring(tree.getroot(), encoding='unicode', method='xml')
        self.builder = Gtk.Builder()
        self.builder.add_from_string(xml_text)
        self.builder.connect_signals(self)
        self.mw = self.builder.get_object("ptxprint")
        logger.debug("Glade loaded in gtkview")

        class MacApp(Gtk.Application):
            def __init__(self, view, *a, **kw):
                super().__init__(*a, flags=Gio.ApplicationFlags.NON_UNIQUE, **kw)
                GLib.set_application_name("PTXprint")
                self.view = view
                self.win = None
                self.hold()

            def do_startup(self):
                Gtk.Application.do_startup(self)
                self.win = self.view.builder.get_object("mainapp_win")
                if not sys.platform.startswith("win"):
                    mb = self.view._add_mac_menu(self)
                    self.set_app_menu(mb)
                self.win.show_all()
                self.view.first_method()

            def do_activate(self):
                #Gtk.Application.do_activate(self)
                pass

            def on_window_destory(self, widget):
                self.release()

        self.mainapp = MacApp(self)

        self.startedtime = time.time()
        self.lastUpdatetime = time.time() - 3600
        self.isDisplay = True
        self.searchWidget = []
        self.uilevel = int(self.userconfig.get('init', 'userinterface', fallback='4'))
        self.set("c_quickRun", self.userconfig.getboolean('init', 'quickrun', fallback=False))
        self.set("c_updatePDF", self.userconfig.getboolean('init', 'updatepdf', fallback=True))
        self.set("c_bkView", self.userconfig.getboolean('init', 'bkview', fallback=True))
        logger.debug(f"Loaded UI level from user config: {self.uilevel}")
        self.painted = set()
        self.locked = set()
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
        # self.warnedSIL = False
        self.thickActive = False
        self.printReason = 0
        self.warnedMissingZvars = False
        self.blInitValue = None
        self.currCodeletVbox = None
        self.codeletVboxes = {}
        self.gtkpolyglot = None
        self.currentPDFpath = None
        self.ufPages = []
        self.picrect = None

        self.initialize_uiLevel_menu()
        self.updateShowPDFmenu()
        self.mruBookList = self.userconfig.get('init', 'mruBooks', fallback='').split('\n')

        llang = self.builder.get_object("ls_interfaceLang")
        btn_language = self.builder.get_object("btn_menu_lang")
        menu = Gtk.Menu()
        for row in llang:
            lang_name, lang_code = row[:2]
            label = Gtk.Label()
            if self.lang.startswith(lang_code):
                label.set_markup(f'<span foreground="medium blue"><b>{lang_name}</b></span>')
                self.set("l_menu_uilang", _("Language\n({})").format(lang_name))
            else:
                label.set_text(lang_name)
            label.set_use_markup(True)
            label.set_xalign(0)
            item = Gtk.MenuItem()
            item.add(label)
            item.connect("activate", self.changeInterfaceLang, lang_code)
            menu.append(item)
        menu.show_all()
        btn_language.set_popup(menu)
        logger.debug(f"UI Language list: {[row[:] for row in llang]}")
        for n in _notebooks:
            nbk = self.builder.get_object("nbk_"+n)
            self.notebooks[n] = [Gtk.Buildable.get_name(nbk.get_nth_page(i)) for i in range(nbk.get_n_pages())]
        self.noInt = self.userconfig.getboolean('init', 'nointernet', fallback=None)
        if self.noInt is not None:
            self.set("c_noInternet", self.noInt)
        for fcb in ("project", "fontdigits", "script",
                    "textDirection", "glossaryMarkupStyle", "fontFaces", "featsLangs", "leaderStyle",
                    "picaccept", "pubusage", "pubaccept", "chklstFilter|0.75", "gridUnits", "gridOffset",
                    "fnHorizPosn", "xrHorizPosn", "snHorizPosn", "filterXrefs", "colXRside", "outputFormat", 
                    "stytcVpos", "strongsMajorLg", "strongswildcards", "strongsNdxBookId", "xRefExtListSource",
                    "sbBorderStyle", "ptxMapBook"):
            self.addCR("fcb_"+fcb, 0)
        self.cb_savedConfig = self.builder.get_object("ecb_savedConfig")
        # self.ecb_diglotSecConfig = self.builder.get_object("ecb_diglotSecConfig")
        self.ecb_impConfig = self.builder.get_object("ecb_impConfig")
        self.ecb_targetConfig = self.builder.get_object("ecb_targetConfig")
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

        imsets = self.builder.get_object("ecb_artPictureSet")
        imsets.remove_all()
        ims = getImageSets()
        if ims is not None:
            for m in ims:
                logger.debug(f"Found imageset: {m}")
                imsets.append_text(m)
            imsets.set_active(0)

        # for d in ("multiBookSelector", "multiProjSelector", "fontChooser", "password", "overlayCredit",
                  # "generateFRT", "generatePL", "styModsdialog", "DBLbundle", "features", "gridsGuides"):
            # dialog = self.builder.get_object("dlg_" + d)
            # dialog.add_buttons(
                # Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                # Gtk.STOCK_OK, Gtk.ResponseType.OK)
                
        self.fileViews = []
        self.buf = []
        self.uneditedText = [""] * 8
        self.cursors = []
            
        if self.get("c_colophon") and self.get("txbf_colophon") == "":
            self.set("txbf_colophon", _defaultColophon)

        # Keep this tooltip safe for later
        self.frtMatterTooltip = self.builder.get_object("btn_infoViewEdit").get_tooltip_text()
        self.adjListTooltip = self.builder.get_object("l_AdjList").get_tooltip_text()

        logger.debug("Create PicList")
        self.picListView = PicList(self.builder.get_object('tv_picListEdit'), self.builder, self)
        self.styleEditor = StyleEditorView(self)
        self.pdf_viewer = PDFViewer(self, self.builder.get_object("bx_previewPDF"), self.builder.get_object("tv_pdfContents"))
        self.pubvarlist = self.builder.get_object("ls_zvarList")
        self.sbcatlist = self.builder.get_object("ls_sbCatList")
        self.strongsvarlist = self.builder.get_object("ls_strvarList")
        self.tv_polyglot = Gtk.TreeView()

        for w in self.allControls:
            if w.startswith(("c_", "s_", "t_", "r_")):  # These ("bl_", "btn_", "ecb_", "fcb_") don't work. But why not?
                self.builder.get_object(w).connect("button-release-event", self.button_release_callback)

        logger.debug("Static controls initialized")

        # 1. Get all projects and their last-modified times
        all_projects = self.prjTree.projectList()
        resource_projects = []
        projects_with_time = []
        for p in all_projects:
            if "_PTXprint" in p.path:
                resource_projects.append(p.guid) 
            config_file_path = os.path.join(p.path, "unique.id")
            try:
                mtime = os.path.getmtime(config_file_path)
            except FileNotFoundError:
                mtime = 0 # Projects without a unique.id file will be considered "oldest"
            projects_with_time.append({'p': p, 'mtime': mtime})

        # 2. If more than 10 projects, identify the most recent 10% (max of 10) of project IDs to be highlighted
        recent_project_ids = {}
        if len(all_projects) > 10:
            topTenPcnt = min(int(len(all_projects)/10), 10)
            # print(f"{topTenPcnt=}")
            projects_with_time.sort(key=lambda x: x['mtime'], reverse=True)
            recent_project_ids = {d['p'].prjid for d in projects_with_time[:topTenPcnt] if d['mtime'] > 0}

        # 3. Get models and clear them
        projects = self.builder.get_object("ls_projects")
        digprojects = self.builder.get_object("ls_digprojects")
        strngsfbprojects = self.builder.get_object("ls_strongsfallbackprojects")
        projects.clear()
        digprojects.clear()
        strngsfbprojects.clear()

        # 4. Populate models with styling information
        # Sort projects alphabetically (case-insensitive) for the final display order
        all_projects.sort(key=lambda p: p.prjid.lower()) 
        for p in all_projects:
            prjid = p.prjid
            guid = p.guid
            
            # Determine style based on whether the project is in our "recent" set
            is_recent = prjid in recent_project_ids
            weight = Pango.Weight.BOLD if is_recent else Pango.Weight.NORMAL
            if guid in resource_projects:
                color = "#800080" # purple if resource text
            elif is_recent:
                color = "#00008B" # blue if recent project
            else: 
                color = "#000000" # otherwise black

            # Append to all relevant models, adding style info to the main one
            projects.append([prjid, guid, weight, color]) 
            digprojects.append([prjid, guid]) # Other models don't need styling
            if os.path.exists(os.path.join(p.path, 'TermRenderings.xml')):
                strngsfbprojects.append([prjid, guid])

        # 5. Connect the styling function to the ComboBox renderer
        combo = self.builder.get_object("fcb_project")
        renderer = combo.get_cells()[0] 
        combo.set_cell_data_func(renderer, self.set_project_style)

        wide = int(len(projects)/16)+1 if len(projects) > 14 else 1
        combo.set_wrap_width(wide)
        # self.builder.get_object("fcb_diglotSecProject").set_wrap_width(wide)
        self.builder.get_object("fcb_impProject").set_wrap_width(wide)
        self.builder.get_object("fcb_strongsFallbackProj").set_wrap_width(wide)
        self.builder.get_object("s_coverShadingAlpha").set_size_request(50, -1)
        self.builder.get_object("s_coverImageAlpha").set_size_request(50, -1)
        self.builder.get_object("scr_previewPDF").set_visible(False)
        self.getInitValues(addtooltips=self.args.identify)
        self.builder.get_object("l_updateDelay").set_label(_("({}s delay)").format(self.get("s_autoupdatedelay", 3.0)))
        self.updateFont2BaselineRatio()
        self.tabsHorizVert()
        logger.debug("Project list loaded")

        return True

    def set_project_style(self, cell_layout, cell, model, tree_iter, data=None):
        """
        Applies font weight and color to the ComboBox renderer based on the model.
        This is a cell data function.
        """
        # Column index 2 holds the font weight (an integer)
        # Column index 3 holds the foreground color (a string)
        font_weight = model.get_value(tree_iter, 2)
        fg_color = model.get_value(tree_iter, 3)
        
        # Apply the properties to the cell renderer
        cell.set_property('weight', font_weight)
        cell.set_property('foreground', fg_color)
        
    def initialize_uiLevel_menu(self):
        levels = self.builder.get_object("ls_uiLevel")
        btn = self.builder.get_object("btn_menu_level")
        menu = Gtk.Menu()
        for row in levels:
            label_text = row[0]  # e.g., "Beginner (1)"
            level_value = int(row[1])  # e.g., 1

            label = Gtk.Label()
            if level_value == self.uilevel:
                label.set_markup(f'<span foreground="#0000CD"><b>{label_text}</b></span>')
            else:
                label.set_text(label_text)
            label.set_use_markup(True)
            label.set_xalign(0)

            item = Gtk.MenuItem()
            item.add(label)
            item.connect("activate", self.setUIlevel, level_value)
            menu.append(item)

        menu.show_all()
        btn.set_popup(menu)

    def updateShowPDFmenu(self):
        self.showPDFmode = self.userconfig.get('init', 'showPDFmode', fallback='preview')
        lst = self.builder.get_object("ls_showPDF")
        btn = self.builder.get_object("btn_menu_showPDF")
        menu = Gtk.Menu()
        for row in lst:
            label_text = row[0]
            option_value = row[1]
            label = Gtk.Label()
            if option_value == self.showPDFmode:
                label.set_markup(f'<span foreground="medium blue"><b>{label_text}</b></span>')
            else:
                label.set_text(label_text)
            label.set_use_markup(True)
            label.set_xalign(0)
            item = Gtk.MenuItem()
            item.add(label)
            item.connect("activate", self.set_showPDFmode, option_value)
            menu.append(item)
        menu.show_all()
        btn.set_popup(menu)


    def _setup_digits(self):
        digits = self.builder.get_object("ls_digits")
        currdigits = {r[0]: r[1] for r in digits}
        digits.clear()
        for d in _alldigits: # .items():
            v = currdigits.get(d, d.lower())
            digits.append([d, v])
        if self.project is None or self.project.prjid is None:
            return
        cfgpath = os.path.join(self.project.path, 'shared', 'fonts', 'mappings')
        if os.path.exists(cfgpath):
            added = set()
            for f in os.listdir(cfgpath):
                fname = f[:f.rindex(".")]
                if fname not in added:
                    digits.append([fname, fname])
                    added.add(fname)

    def _setup_css(self):
            # .dblbutton {font-size: 10px; min-height: 0; min-width:0;  padding:2px;}
        css = """
            .printbutton:active { background-color: chartreuse; background-image: None }
            .sbimgbutton:active { background-color: lightskyblue; font-weight: bold}
            .smallbutton {font-size: 10px; min-height: 0pt; min-width:10px;  padding:1px;}
            .tinybutton {font-size: 3pt; border:none; min-height: 0pt; min-width:10px;  padding:0pt;}
            .fontbutton {font-size: 12px}
            .scale-slider trough {min-height: 5px}
            tooltip {color: rgb(255,255,255); background-color: rgb(64,64,64)} 
            .stylinks {font-weight: bold; text-decoration: None; padding: 1px 1px}
            .stybutton {font-size: 12px; padding: 4px 6px}
            progress, trough {min-height: 24px}
            .mainnb tab {min-height: 0pt; margin: 0pt; padding-bottom: 6pt}
            .mainnb tab:checked {background-color: lightsteelblue}
            .mainnb tab:checked label {font-weight: bold}
            .viewernb {background-color: #d3d3d3}
            .graybox {background-color: #ecebea}
            .viewernb tab {min-height: 0pt; margin: 0pt; padding-bottom: 3pt}
            .smradio {font-size: 11px; padding: 1px 1px}
            .changed {font-weight: bold}
            .blue-label {color: blue; font-weight: bold}
            .red-label {color: red}
            .backsettingsfrt text {background-color: #fffff0;}
            .backsettingsadj text {background-color: #fff0ff;}
            .backsettings1 text {background-color: #f0f0ff;}
            .backsettings2 text {background-color: #fff0f0;}
            .backsettings3 text {background-color: #f0fff0;}
            
            .update-blue   {color: #3498db; /* A nice, friendly blue = update available*/}
            .update-orange {color: #f39c12; /* A noticeable orange = warning! out of date*/}
            .update-red    {color: #e74c3c; /* A strong, urgent red =majorly out of date */}
            button {transition: color 0.3s ease-in-out; /* Transition for a smooth color change */}
            
            .highlighted {background-color: peachpuff; background: peachpuff}
            .yellowlighted {background-color: rgb(255,255,102); background: rgb(255,255,102)}
            .attention {background-color: lightblue; background: lightblue}
            .warning {background: lightpink;font-weight: bold; color: darkred}
            combobox.highlighted > box.linked > entry.combo { background-color: peachpuff; background: peachpuff}
            combobox.yellowlighted > box.linked > entry.combo { background-color: rgb(255,255,102); background: rgb(255,255,102)}
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

        logger.debug("Creating source views")
        lm = GtkSource.LanguageManager()
        langpath = os.path.join(os.path.dirname(__file__), "syntax")
        sm = GtkSource.StyleSchemeManager()
        logger.debug(f"Setting syntax files path to {langpath}")
        lm.set_search_path([langpath])
        sm.set_search_path([langpath])
        for i,k in enumerate(["FrontMatter", "AdjList", "FinalSFM", "TeXfile", "XeTeXlog", \
                              "Settings1", "Settings2", "Settings3"]):
            self.cursors.append((0,0))
            if k == "AdjList":
                self.buf.append(None)
                self.fileViews.append((None, None))
                continue
            self.buf.append(GtkSource.Buffer())
            view = GtkSource.View.new_with_buffer(self.buf[i])
            scroll = self.builder.get_object("tb_" + k)
            scroll.add(view)
            self.fileViews.append((self.buf[i], view))
            view.set_left_margin(8)
            view.set_top_margin(6)
            view.set_bottom_margin(24)  
            view.set_show_line_numbers(True if i > 1 else False)
            view.set_editable(False if i in [2,3,4] else True)
            view.set_wrap_mode(Gtk.WrapMode.CHAR)
            view.pageid = "tb_"+k

            view.connect("focus-out-event", self.onViewerLostFocus)
            view.connect("focus-in-event", self.onViewerFocus)
            if not i in [2,3,4]: # Ignore the uneditable views
                # Set up signals to pick up any edits in the TextView window
                for evnt in ["key-release-event", "delete-from-cursor", 
                             "backspace", "cut-clipboard", "paste-clipboard"]:
                    view.connect(evnt, self.onViewEdited)
            view.connect("key-press-event", onTextEditKeypress, tuple([i]+list(self.fileViews[i])+[self]))
            if k == "FrontMatter":
                view.get_style_context().add_class(f"backsettingsfrt")
            if k.startswith("Settings"):
                view.get_style_context().add_class(f"backsettings{k[-1]}")

        self.adjView = AdjListView(self)
        scroll = self.builder.get_object("tb_AdjList")
        scroll.add(self.adjView.view)
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

        self.mw.show_all()
        self.set_uiChangeLevel(self.uilevel)
        GObject.timeout_add(1000, self.monitor)
        if self.args is not None and self.args.capture is not None:
            self.logfile = open(self.args.capture, "w")
            self.logfile.write("<?xml version='1.0'?>\n<actions>\n")
            self.starttime = time.time()
            for k, v in _signals.items():
                for w in v:
                    # print(f"{k=} {w=}")
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
        self.setupTeXOptions()
        self.builder.get_object('c_variableLineSpacing').set_sensitive(self.get("c_noGrid"))

        w = self.builder.get_object("col_noteLines")
        (rect, bline) = w.get_allocated_size()
        rect.width *= 0.75
        w.size_allocate_with_baseline(rect, bline)

        if self.splash is not None:
            self.splash.terminate()
            self.splash = None

        self.changed(False)
        logger.debug("Starting UI")
        try:
            if self.mainapp is not None:
                self.mainapp.run()
            else:
                Gtk.main()
        except Exception as e:
            s = traceback.format_exc()
            s += "\n{}: {}".format(type(e), str(e))
            self.doError(s, copy2clip=True)

    def first_method(self):
        """ This is called first thing after the UI is set up and all is active """
        width = self.userconfig.getint("geometry", f"ptxprint_width", fallback=1005)
        height = self.userconfig.getint("geometry", f"ptxprint_height", fallback=665)
        self.mainapp.win.resize(width, height)
        self.doConfigNameChange(None)
        if sys.platform.startswith("win"):
            self.restore_window_geometry()


    def emission_hook(self, w, *a):
        if not self.logactive:
            return True
        name = Gtk.Buildable.get_name(w)
        self.logfile.write('    <event w="{}" s="{}" t="{}"/>\n'.format(name, a[0],
                            time.time()-self.starttime))
        logger.debug(f'event: {name=} {a[0]=}')
        return True

    def pause_logging(self):
        self.logactive = False

    def unpause_logging(self):
        self.logactive = True

    def monitor(self):
        if self.pendingerror is not None:
            doError(*self.pendingerror[:-1], **self.pendingerror[-1])
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
        scr.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)        
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
            ui = self.uilevel
            setLevel = 0
            for i in range(2, 5):
                if i in _uiLevels and wid in _uiLevels[i]:
                    if i > ui:
                        setLevel = i
                    break
            else:
                setLevel = 6
            if setLevel > 0:
                self.set_uiChangeLevel(setLevel)
        parent = w.get_parent()
        atfinish = None
        curry = 0 # w.get_allocation().y
        while parent is not None:
            curry += parent.get_allocation().y
            name = Gtk.Buildable.get_name(parent)
            # print(f"{name=}")
            if name.startswith("tb_"):
                if highlight:
                    w.get_style_context().add_class("highlighted")
                    keepgoing = True
                    for k, v in self.notebooks.items():
                        if name in v:
                            pgnum = v.index(name)
                            t = self.builder.get_object('nbk_{}'.format(k)).set_current_page(pgnum)
                            keepgoing = k != 'Main'
                            pw = w.get_parent()
                            if isinstance(parent, Gtk.ScrolledWindow):
                                def make_sw():
                                    sw = parent
                                    cv = curry
                                    tw = w
                                    def swidg():
                                        wy = tw.get_allocation().y
                                        vadj = sw.get_vadjustment()
                                        vadj.set_value(cv + wy)
                                        vadj.value_changed()
                                    return swidg
                                Gdk.threads_add_idle(0, make_sw())
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
        if atfinish is not None:
            Gdk.threads_add_idle(0, atfinish)

    def onMainConfigure(self, w, ev, *a):
        if self.picListView is not None:
            self.picListView.onResized()

    def getInitValues(self, addtooltips=False):
        self.initValues = {}
        allentries = [(x.texname, x.widget) for x in ModelMap.values()] + [("", b) for b in self.btnControls]
        for k, v in allentries:
            if v is None:
                continue
            if addtooltips and not k.endswith("_"):
                w = self.builder.get_object(v)
                if w is not None:
                    try:
                        t = w.get_tooltip_text()
                    except AttributeError:
                        continue
                    if t is not None:
                        t += "\n{}({})".format(k, v)
                    else:
                        t = "{}({})".format(k, v)
                    w.set_tooltip_text(t)
            if k and not v.startswith("r_"):
                self.initValues[v] = self.get(v, skipmissing=True)
        for r, a in self.radios.items():
            for v in a:
                w = self.builder.get_object("r_{}_{}".format(r, v))
                if w.get_active():
                    self.initValues["r_{}".format(r)] = v
        self.resetToInitValues()

    def resetToInitValues(self, updatebklist=True):
        self.loadingConfig = True
        self.rtl = False
        super().resetToInitValues(updatebklist=updatebklist)
        if self.picinfos is not None:
            self.picinfos.clear(self)
        self.diglotviews = {}
        self.polyglots = {}
        if self.gtkpolyglot is not None:
            self.gtkpolyglot.clear_polyglot_treeview()
        self.gtkpolyglot = None
        # Also reset the Peripheral tab Variables
        tv = self.builder.get_object("ls_zvarList")
        tv.clear()
        for k, v in self.initValues.items():
            if not updatebklist and k in self._nonresetcontrols:
                continue
            if k.startswith("bl_") or v is not None:
                self.set(k, v)
        self.colorTabs()
        self.loadingConfig = False

    def onResetPage(self, widget):
        pass

    def setUIlevel(self, menuitem, ui):
        self.set_uiChangeLevel(ui)
        
    def popdownMainMenu(self):
        menu_main = self.builder.get_object("menu_main")
        if isinstance(menu_main, Gtk.Popover):
            menu_main.popdown()        

    def set_uiChangeLevel(self, ui):
        if self.loadingConfig:
            return
        self.popdownMainMenu()
        if isinstance(ui, str):
            try:
                ui = int(ui)
            except ValueError:
                logger.warning(f"Unexpected ui value of {ui}")
                ui = 4

        if ui <= 0 or ui > 6:
            ui = 4

        pgId = self.builder.get_object("nbk_Main").get_current_page()
        self.uilevel = ui
        if not self.userconfig.has_section("init"):
            self.userconfig.add_section("init")
        self.userconfig.set('init', 'userinterface', str(ui))
        levels = self.builder.get_object("ls_uiLevel")
        levelname = None
        for r in levels:
            if int(r[1]) == ui:
                levelname = " ".join(r[0].split(" ")[:-1])  # remove (n)
                break
        self.set("l_menu_level", _("View Level\n({})").format(levelname) if levelname else _("View Level"))
        self.initialize_uiLevel_menu()

        # Apply UI filtering logic
        if ui < 6:
            for w in reversed(sorted(self.allControls)):
                self.toggleUIdetails(w, False)
            widgets = sum((v for k, v in _uiLevels.items() if ui >= k), [])
            if self.args.experimental & 1 != 0:
                widgets += _ui_experimental
        else:
            # Selectively turn things back on if their settings are enabled
            for k, v in _showActiveTabs.items():
                if self.get(k):
                    for w in v:
                        self.toggleUIdetails(w, True)
                
            widgets = set(self.allControls)
            if self.args.experimental & 1 == 0:
                for k in _ui_experimental:
                    widgets.discard(k)

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
        # self.mw.resize(200, 200)
        self.builder.get_object("nbk_Main").set_current_page(pgId)
        return True

    def toggleUIdetails(self, w, state):
        if w in _ui_noToggleVisible:
            self.builder.get_object(w).set_sensitive(state)
        else:
            self.builder.get_object(w).set_visible(state)

    def noInternetClicked(self, btn):
        ui = self.uilevel
        if btn is not None:
            val = self.get("c_noInternet") or (ui < 6)
        else:
            val = self.noInt if self.noInt is not None else True
        adv = (ui >= 6)
        for w in "l_url_usfm lb_DBLdownloads lb_openBible l_homePage l_community l_trainingVideos l_reportBugs lb_trainingOnVimeo lb_chatBot lb_homePage lb_community lb_trainingOnPTsite lb_reportBugs lb_techFAQ lb_learnHowTo l_giveFeedback lb_giveFeeback btn_about".split():
            self.builder.get_object(w).set_visible(not val)
        newval = self.get("c_noInternet")
        self.noInt = newval
        self.userconfig.set("init", "nointernet", "true" if newval else "false")
        # Show Hide specific Help items
        for pre in ("l_", "lb_"):
            for h in ("ptxprintdir", "prjdir", "settings_dir"): 
                self.builder.get_object("{}{}".format(pre, h)).set_visible(adv)
        for w in ["lb_omitPics", "lb_techFAQ", "l_reportBugs", "lb_reportBugs"]:
            self.builder.get_object(w).set_visible(not newval and adv)
        for w in ["l_techFAQ", "lb_ornaments_cat", "lb_tech_ref"]:
            self.builder.get_object(w).set_visible(adv)
        for w in ["btn_DBLbundleDiglot1", "btn_DBLbundleDiglot2"]:
            self.builder.get_object(w).set_visible(not newval)
        self.i18nizeURIs()

    def i18nizeURIs(self):
        self.builder.get_object("l_url_usfm").set_label(_('More Info...'))
        tl = self.lang if not self.get("c_useEngLinks") and \
           self.lang in ['ar_SA', 'my', 'zh', 'fr', 'hi', 'hu', 'id', 'ko', 'pt', 'ro', 'ru', 'es', 'th'] else ""
        for u in "homePage community techFAQ reportBugs".split(): # lb_DBLdownloads lb_openBible ?as well?
            w = self.builder.get_object("lb_" + u)
            if "translate.goog" in w.get_uri():
                continue
            site = w.get_uri()
            partA, partB = self.splitURL(site)
            partA = re.sub(r"\.", r"-", partA)
            
            if len(tl) and "/tree/" not in site:
                site = "{}.translate.goog/{}?_x_tr_sl=en&_x_tr_tl={}&_x_tr_hl=en&_x_tr_pto=wapp&_x_tr_hist=true".format(partA, partB, tl)
            w.set_uri(f'{site}')
            
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
        return [m.group(1), int(m.group(2))] if m else [font, 0]

    def get(self, wid, default=None, sub=-1, asstr=False, skipmissing=False):
        if "[" in wid:
            subi = wid.index("[")
            sub = int(wid[subi+1:-1])
            wid = wid[:subi]
        w = self.builder.get_object(wid)
        if w is None:
            if wid.startswith("+"):
                if hasattr(self, "get_"+wid[1:]):
                    res = getattr(self, "get_"+wid[1:])()
                    return res
            res = super().get(wid, default=default)
            if not skipmissing and not any(wid.startswith(x) for x in ("_", "r_")):
                logger.debug("Can't get {} in the model. Returning {}".format(wid, res))
            return res
        if wid.startswith("r_"):
            bits = wid.split("_")[1:]
            if len(bits) > 1:
                return w.get_active()
            return super().get(wid, default=default)
        return getWidgetVal(wid, w, default=default, asstr=asstr, sub=sub)

    def set(self, wid, value, skipmissing=False, useMarkup=False, sub=-1, mod=True):
        if "[" in wid:
            subi = wid.index("[")
            sub = int(wid[subi+1:-1])
            wid = wid[:subi]
        if wid == "l_statusLine":
            self.builder.get_object("bx_statusMsgBar").set_visible(len(value))
        w = self.builder.get_object(wid)
        if w is None:
            if wid.startswith("+"):
                m = getattr(self, "set_"+wid[1:], None)
                if m is not None and not isinstance(m, str):
                    if not getattr(self, "set_"+wid[1:])(value):
                        return
                wid = wid[1:]
            elif wid.startswith("r_"):
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
            elif wid.startswith("c_") or wid.startswith("s_") and TeXpert.hasopt(wid[2:]):
                pass
            elif not skipmissing:
                if not wid.startswith('_'):
                    print(_("Can't set {} in the model").format(wid))
            super(GtkViewModel, self).set(wid, value)
            return
        setWidgetVal(wid, w, value, useMarkup=useMarkup, sub=sub)
        if mod and wid not in _ui_unchanged and not any(wid.startswith(x) for x in ("lb_", "nbk_")):
            self.changed()

    def getvar(self, k, default="", dest=None):
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
        return default

    def setvar(self, k, v, dest=None, editable=True, colour=None):
        if dest is None:
            varlist = self.pubvarlist
        elif dest == "strongs":
            varlist = self.strongsvarlist
        # elif dest == "sbcats":
            # varlist = self.sbcatlist
        for r in varlist:
            if r[0] == k:
                r[1] = v
                r[2] = editable
                if colour is not None:
                    r[3] = colour
                break
        else:
            varlist.append([k, v, editable, colour])

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

    def onDestroy(self, btn, *a):
        if self.logfile != None:
            self.logfile.write("</actions>\n")
            self.logfile.close()
        self.mainapp.quit()

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
            doError(txt, **kw)

    def doStatus(self, txt=""): 
        btn = self.builder.get_object("btn_dismissStatusLine")
        if txt.startswith(r"\u"): # i.e. the results of an Alt-X (show unicode chars)
            btn.set_label(_(" Copy to Clipboard "))
        else:
            btn.set_label(_("Dismiss"))
        sl = self.builder.get_object("l_statusLine")
        self.set("l_statusLine", txt)
        status = len(self.get("l_statusLine"))
        sl = self.builder.get_object("bx_statusMsgBar").set_visible(status)
        
    def onHideStatusMsgClicked(self, btn):
        t = self.builder.get_object("l_statusLine").get_label() 
        if t.startswith(r"\u"): # If the status message contains the results of an Alt-X (show unicode chars)
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            clipboard.set_text(t, -1)
            clipboard.store()
        sl = self.builder.get_object("bx_statusMsgBar").set_visible(False)

    def waitThread(self, thread):
        while thread.is_alive():
            Gtk.main_iteration_do(False)
        
    def setPrintBtnStatus(self, idnty, txt=""):
        logger.debug(f"{idnty=} {len(txt) if txt is not None else 'None'} {getcaller(1)}")
        if txt is None or not len(txt):
            self.printReason &= ~idnty
        else:
            self.printReason |= idnty
        if txt or not self.printReason:
            self.doStatus(txt)
        for w in ["b_print", "b_print4cover"]: # "b_print2ndDiglotText", "spolyfraction_"
            self.builder.get_object(w).set_sensitive(not self.printReason)
        if self.gtkpolyglot is not None:    
            self.builder.get_object("btn_adjust_diglot").set_sensitive(not self.printReason and len(self.gtkpolyglot.ls_treeview) == 2)

    def checkFontsMissing(self):
        self.setPrintBtnStatus(4, "")
        for f in ['R','B','I','BI']:
            if self.get("bl_font" + f) is None:
                logger.debug(f"bl_font: {f} is None. {getcaller()}")
                self.setPrintBtnStatus(4, _("Font(s) not set"))
                return True
        return False
                
    def print2ndDiglotTextClicked(self, btn):
        self.onOK(btn)
        
    def onOK(self, btn):
        if btn == self.builder.get_object("b_print2ndDiglotText"):
            pass
        elif self.otherDiglot is not None:
            # self.updateProjectSettings(self.otherDiglot[0].prjid, self.otherDiglot[0].guid, configName=self.otherDiglot[1], saveCurrConfig=True)
            self.changeBtnLabel("b_print", _("Print (Make PDF)"))
            self.builder.get_object("b_print2ndDiglotText").set_visible(False)
            self.builder.get_object("b_reprint").set_sensitive(True)
            self.set("fcb_project", self.otherDiglot[0].prjid)
            self.set("ecb_savedConfig", self.otherDiglot[1])
            self.otherDiglot = None
            return
        if isLocked():
            self.doStatus(_("Printing busy"))
            return

        self.builder.get_object("spin_preview").start()
        self.builder.get_object("l_updateDelay").set_label(_("({}s delay)").format(self.get("s_autoupdatedelay", 3.0)))
        print_count_str = self.get("_printcount", "")
        if print_count_str:
            print_count = int(print_count_str)
        else:
            print_count = 0
        print_count += 1
        self.set("_printcount", print_count, skipmissing=True)

        jobs = self.getBooks(files=True)
        if not len(jobs) or jobs[0] == '':
            self.doStatus(_("No books to print"))
            return
        if self.checkFontsMissing():
            self.doStatus(_("One of more fonts have not been set yet"))
            return
        # If the viewer/editor is open on an Editable tab, then "autosave" contents
        if Gtk.Buildable.get_name(self.builder.get_object("nbk_Main").get_nth_page(self.get("nbk_Main"))) == "tb_Viewer":
            pgnum = self.get("nbk_Viewer")
            if self.notebooks["Viewer"][pgnum] in ("tb_FrontMatter", "tb_AdjList", "tb_Settings1", "tb_Settings2", "tb_Settings3"):
                self.onSaveEdits(None)
        cfgname = self.cfgid
        if cfgname is None:
            cfgname = ""
        else:
            cfgname = "-" + cfgname
        if not os.path.exists(self.project.printPath(self.cfgid)):
            os.makedirs(self.project.printPath(self.cfgid))
        self.docreatediff = self.get("c_createDiff")
        pdfnames = self.baseTeXPDFnames(diff=self.docreatediff)
        for basename in pdfnames:
            pdfname = os.path.join(self.project.printPath(self.cfgid), "..", basename) + ".pdf"
            exists = os.path.exists(pdfname)
            if exists:
                fileLocked = True
                while fileLocked:
                    try:
                        with open(pdfname, "ab+") as outf:
                            outf.close()
                    except PermissionError:
                        question = _("Please close the file in your PDF viewer.\
                         \n\n{}\n\n Note: It is better to use the Preview Pane.\
                                 \n See 'Show PDF' options on the PTXprint menu. \
                               \n\n       Do you want to try again?").format(basename + ".pdf")
                        if self.msgQuestion(_("Cannot update PDF file while it is locked!"), question):
                            continue
                        else:
                            self.doStatus(_("Close the old PDF file before you try again."))
                            self.finished()
                            return
                    fileLocked = False
        self.onSaveConfig(None)
        self.checkUpdates()

        self._incrementProgress(val=0.)
        self.builder.get_object("t_find").set_placeholder_text(_("Processing..."))
        self.builder.get_object("t_find").set_text("")
        try:
            self.callback(self)
        except Exception as e:
            if "SyntaxError" in str(type(e)):
            # if "SyntaxError" in type(e):
                s = _("Failed due to an error in the USFM file.") + "\n" + \
                    _("Run the Basic Checks in Paratext and try again.") + "\n"
            else:
                s = traceback.format_exc()
            s += "\n{}: {}".format(type(e), str(e))
            self.doError(s, copy2clip=True)
            unlockme()
            self.builder.get_object("t_find").set_placeholder_text("Search for settings")
            self.builder.get_object("t_find").set_text("")

    def onCancel(self, btn):
        self.onDestroy(btn)

    def warnStrongsInText(self, btn):
        if self.get("c_useXrefList") and self.get("c_strongsShowInText"):
            self.doStatus(_("Note: It may take a while for the PDF to be produced due to including Strong's numbers in the text."))
        else:
            self.doStatus("")

    def warnSlowRun(self, btn):
        ofmt = self.get("fcb_outputFormat")
        if self.get("c_includeillustrations") and ofmt != "Screen":
            self.doStatus(_("Note: It may take a while for pictures to convert for selected PDF Output Format ({}).".format(ofmt)))
        else:
            self.doStatus("")

    def outputFormatChanged(self, btn):
        if self.loadingConfig:
            return
        ofmt = self.get("fcb_outputFormat")
        self.enableDisableSpotColor(ofmt)
        if self.get("c_thumbtabs") and not self.get("c_tabsOddOnly"):
            if ofmt in ["CMYK", "Gray", "Spot"]:
                self.set("c_tabsOddOnly", True)
                self.doStatus(_("Thumb tabs set to 'Only Show on Odd Pages' for PDF Output Format ({}).".format(ofmt)))
        else:
            self.warnSlowRun(None)

    def enableDisableSpotColor(self, ofmt):
        for w in ["l_spotColor", "col_spotColor", "l_spotColorTolerance", "s_spotColorTolerance"]:
            self.builder.get_object(w).set_sensitive(ofmt == "Spot")

    def onAboutClicked(self, btn_about):
        dialog = self.builder.get_object("dlg_about")
        response = dialog.run()
        dialog.hide()

    def onBookScopeClicked(self, btn):
        self.bookrefs = None

    def onBookListChanged(self, ecb_booklist): # called on "focus-out-event"
        if not self.initialised:
            return
        # if self.loadingConfig:
            # return
        if self.booklistKeypressed:
            self.booklistKeypressed = False
            return
        self.doBookListChange()
        
    def onBkLstKeyPressed(self, btn, *a):
        # if self.loadingConfig:
            # return
        self.booklistKeypressed = True
        if self.blInitValue != self.get('ecb_booklist'):
            self.set("r_book", "multiple")

    def onBkLstFocusOutEvent(self, btn, *a):
        self.booklistKeypressed = False
        self.doBookListChange()

    def doBookListChange(self):
        raw_bls = self.get('ecb_booklist', '').strip()
        normalized = unicodedata.normalize('NFD', raw_bls)
        no_accents = ''.join(ch for ch in normalized if unicodedata.category(ch) != 'Mn')
        cleaned = re.sub(r'[^A-Za-z0-9\-:;, ]+', '', no_accents)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        bls = re.sub(r'-END', '-end', cleaned.upper())
        self.set('ecb_booklist', bls)
        self.bookrefs = None
        bl = self.getAllBooks()
        if not self.booklistKeypressed and not len(bl):
            self.set("ecb_book", list(bl.keys())[0])
        self.updateExamineBook()
        self.updateDialogTitle()
        self.disableLayoutAnalysis()
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
        self.showmybook()

    def onSaveConfig(self, btn, force=False):
        """ Save the view """
        if self.project.prjid is None or (not force and self.configLocked()):
            return
        newconfigId = self.getConfigName()
        if newconfigId != self.cfgid: # only for new configs
            # self.applyConfig(self.cfgid, newconfigId, nobase=True)
            self.updateProjectSettings(self.project.prjid, self.project.guid, configName=newconfigId, readConfig=True)
            self.updateSavedConfigList()
            stngdir = self.project.srcPath(self.cfgid)
            self.set("lb_settings_dir", '<a href="{}">{}</a>'.format(stngdir, stngdir))
            self.updateDialogTitle()
            self.disableLayoutAnalysis()
        self.userconfig.set("init", "project", self.project.prjid)
        self.userconfig.set("init", "nointernet", "true" if self.get("c_noInternet") else "false")
        self.userconfig.set("init", "quickrun",   "true" if self.get("c_quickRun")   else "false")
        self.userconfig.set("init", "updatepdf",  "true" if self.get("c_updatePDF")  else "false")
        self.userconfig.set("init", "bkview",     "true" if self.get("c_bkView")     else "false")
        self.noInt = self.get("c_noInternet")
        self.userconfig.set("init", "englinks",  "true" if self.get("c_useEngLinks") else "false")
        if sys.platform.startswith("win"):
            self.save_window_geometry()
        if self.cfgid is not None:
            self.userconfig.set("init", "config", self.cfgid)
        self.saveConfig(force=force)
        self.onSaveEdits(None)

    def writeConfig(self, cfgname=None, force=False):
        super().writeConfig(cfgname=cfgname, force=force)
        if self.project.prjid is not None:
            self.picChecksView.writeCfg(self.project.srcPath(), self.cfgid)

    def fillCopyrightDetails(self):
        pts = self._getPtSettings()
        if pts is not None:
            t = pts.get('Copyright', "")
            t = re.sub(r"\([cC]\)", "\u00a9 ", t)
            t = re.sub(r"\([rR]\)", "\u00ae ", t)
            t = re.sub(r"\([tT][mM]\)", "\u2122 ", t)
            if len(t) < 100:
                t = re.sub(r"</?p>", "", t)
                self.builder.get_object("t_copyrightStatement").set_text(t)
            else:
                if len(self.get("txbf_colophon")) > 100:
                    return # Don't overwrite what has already been placed in the colophon
                           # from an earlier run, which could also have been edited manually.
                t = re.sub(r"<p>", r"\n\\pc ", t)
                t = re.sub(r"</p>", "", t)
                t = re.sub(r"\\pc ?\n?\\pc ", r"\\pc ", r"\pc " + t)
                self.set("txbf_colophon", t)
                self.builder.get_object("t_copyrightStatement").set_text(' ')
                self.set("c_colophon", True)
                self.doStatus(_("Note: Copyright statement is too long. It has been placed in the Colophon (see Peripherals tab)."))

    def onDeleteConfig(self, btn):
        cfg = self.get("t_savedConfig")
        delCfgPath = self.project.srcPath(cfg)
        sec = ""
        if cfg == 'Default':
            ui = self.uilevel
            self.resetToInitValues()
            self.set_uiChangeLevel(ui)
            try:
                rmtree(delCfgPath)
            except OSError:
                sec = _("But the 'Default' folder could not be erased completely:") + "\n" + delCfgPath

            self.writeConfig(cfgname="Default", force=True)
            self.triggervcs = True
            self.updateFonts()
            self.readConfig("Default")
            self.fillCopyrightDetails()
            self.doStatus(_("The 'Default' config settings have been reset.") + sec)
            return
        else:
            dialog = self.builder.get_object("dlg_confirmDelete")
            response = dialog.run()
            dialog.hide()
            if response != Gtk.ResponseType.YES:
                return # Don't delete anything!
            msg = _("Deleted config: {}".format(cfg))
            
            if not os.path.exists(os.path.join(delCfgPath, "ptxprint.cfg")):
                self.doStatus(_("Internal error occurred, trying to delete a directory tree") + _("Folder: ") + delCfgPath)
                return
            try: # Delete the entire settings folder
                rmtree(delCfgPath)
            except OSError:
                msg = _("Cannot delete folder from disk!") + _("Folder: ") + delCfgPath

            try: # Delete the entire output folder
                rmtree(self.project.printPath(None))
            except FileNotFoundError:
                pass
            except OSError:
                msg = _("Cannot delete folder from disk!") + _("Folder: ") + self.project.printPath(self.cfgid)

            self.updateSavedConfigList()
            self.set("t_savedConfig", "Default")
            self.readConfig("Default")
            self.updateDialogTitle()
            self.triggervcs = True
            self.doStatus(msg)
        self.colorTabs()
        self.disableLayoutAnalysis()

    def updateBookList(self):
        self.noUpdate = True
        cbbook = self.builder.get_object("ecb_book")
        cbbook.set_model(None)
        lsbooks = self.builder.get_object("ls_books")
        lsbooks.clear()
        # if self.ptsettings is not None:
        bks = self.getAllBooks()
        for b in bks:
            # if b not in ("FRT", "INT"):
            if b != "FRT": # We no longer list the FRT book in the book chooser(s)
                # ind = books.get(b, 0)-1
                # if 0 <= ind <= len(bp) and bp[ind - 1 if ind > 39 else ind] == "1":
                lsbooks.append([b])
        cbbook.set_model(lsbooks)
        # cbbook.set_wrap_width(13)
        self.noUpdate = False

    def updateSavedConfigList(self):
        self.configNoUpdate = True
        currConf = self.userconfig.get("projects", self.project.prjid, fallback=self.get("ecb_savedConfig"))
        self.cb_savedConfig.remove_all()
        savedConfigs = sorted(self.project.configs.keys())
        if len(savedConfigs):
            for cfgName in savedConfigs:
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

    def _fillConfigList(self, prjwname, configlist):
        impprj = self._getProject(prjwname)
        if impprj is None:
            return 0
        impConfigs = sorted(impprj.configs.keys())
        configlist.remove_all()
        if len(impConfigs):
            for cfgName in impConfigs:
                configlist.append_text(cfgName)
        return len(impConfigs)

    def updateimpProjectConfigList(self):
        if self._fillConfigList("fcb_impProject", self.ecb_impConfig) > 0:
            self.set("ecb_impConfig", "Default")

    def updatetgtProjectConfigList(self):
        if self._fillConfigList("ecb_targetProject", self.ecb_targetConfig) > 0:
            self.set("ecb_targetConfig", "Default")
            
    def updateAllConfigLists(self):
        self.updateSavedConfigList()
        self.updateimpProjectConfigList()
        self.updatetgtProjectConfigList()
        # self.updateDiglotConfigList()
    
    def loadConfig(self, config, clearvars=True, **kw):
        self.updateBookList()
        if clearvars:
            self.unpaintUnlock()
        super(GtkViewModel, self).loadConfig(config, clearvars=clearvars, **kw)
        if clearvars:
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
        self.sensiVisible('c_lockUI4Layout') # Why does this do nothing? Is it in the wrong place?
        self.onExtListSourceChanges(None)
        # self.onExpertModeClicked(None)
        x = self.get("btn_selectDiffPDF")
        if x is not None and len(x) < 200:
            self.makeLabelBold("l_selectDiffPDF", True)
            self.set("lb_diffPDF", pdfre.sub(r"\1", x))
        else:
            self.set("lb_diffPDF", _("Previous PDF (_1)"))
        
    def colorTabs(self):
        # col = "crimson"
        col = "#0000CD"
        fs = " color='"+col+"'" if self.get("c_colorfonts") else ""
        self.builder.get_object("lb_Font").set_markup("<span{}>".format(fs)+_("Fonts")+"</span>"+"+"+_("Scripts"))

        pi = " color='"+col+"'" if (self.get("c_inclFrontMatter") or self.get("c_autoToC") or \
           self.get("c_frontmatter") or self.get("c_inclBackMatter")) else ""  # or self.get("c_colophon") 
        self.builder.get_object("lb_Peripherals").set_markup("<span{}>".format(pi)+_("Peripherals")+"</span>")

        ic = " color='"+col+"'" if self.get("c_includeillustrations") else ""
        self.builder.get_object("lb_Pictures").set_markup("<span{}>".format(ic)+_("Pictures")+"</span>")

        dg = " color='"+col+"'" if self.get("c_diglot") else ""
        self.builder.get_object("lb_Diglot").set_markup("<span{}>".format(dg)+_("Diglot")+"</span>")

        fh = " color='"+col+"'" if self.get("fcb_pagesPerSpread") != "1" else ""
        self.builder.get_object("lb_Finishing").set_markup("<span{}>".format(fh)+_("Finishing")+"</span>")

        xl = " color='"+col+"'" if self.get("c_useXrefList") else ""
        self.builder.get_object("lb_NotesRefs").set_markup(_("Notes+")+"<span{}>".format(xl)+_("Refs")+"</span>")
        self.builder.get_object("lb_xrefs").set_markup("<span{}>".format(xl)+_("Cross-References")+"</span>")

        cv = " color='"+col+"'" if self.get("c_makeCoverPage") else ""
        self.builder.get_object("lb_Cover").set_markup("<span{}>".format(cv)+_("Cover")+"</span>")

        tb = self.get("c_thumbtabs")
        bd = self.get("c_useOrnaments")
        tc = "<span color='{}'>".format(col)+_("Tabs")+"</span>" if tb \
            else _("Tabs") if self.builder.get_object("fr_tabs").get_visible() else ""
        bc = "<span color='{}'>".format(col)+_("Borders")+"</span>" if bd \
            else _("Borders") if self.builder.get_object("fr_borders").get_visible() else ""
        jn = "+" if ((tb and bd) or self.uilevel >= 6) else ""
        self.builder.get_object("lb_TabsBorders").set_markup(tc+jn+bc)

        ad = False
        for w in ["processScript", "usePrintDraftChanges", "usePreModsTex", \
                  "useModsTex", "useCustomSty", "useModsSty", "interlinear"]:
            if self.get("c_" + w):
                ad = True
                break
        ac = " color='"+col+"'" if ad else ""
        self.builder.get_object("lb_Advanced").set_markup("<span{}>".format(ac)+_("Advanced")+"</span>")

    def paintLock(self, wid, lock, editableOverride):
        wids = []
        if wid.startswith("r_"):
            wids = ["{}_{}".format(wid, v) for v in self.radios.get(wid[2:], [])]
        if not len(wids):
            wids = [wid]
        for wid in wids:
            w = self.builder.get_object(wid)
            if w is None:
                continue
            if lock and not editableOverride:
                if w.get_sensitive():
                    self.locked.add(wid)
                    w.set_sensitive(False)
            elif editableOverride:
                self.painted.add(wid)
                w.get_style_context().add_class("highlighted")

    def unpaintUnlock(self):
        for wid in self.painted:
            if wid.startswith("txbf_"):
                pass
            else:
                w = self.builder.get_object(wid)
                w.get_style_context().remove_class("highlighted")
        self.painted.clear()
        for wid in self.locked:
            w = self.builder.get_object(wid)
            w.set_sensitive(True)
        self.locked.clear()

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
                        if wid is not None and wid not in self.locked:
                            wid.set_sensitive(l(s))
                if not anyset:
                    v = list(d[k].values())[0]
                    for w in v:
                        wid = self.builder.get_object(w)
                        if wid is not None and wid not in self.locked:
                            wid.set_sensitive(l(s))
            else:
                for w in d[k]:
                    wid = self.builder.get_object(w)
                    if wid is not None and wid not in self.locked:
                        wid.set_sensitive(l(state))
        if focus and k in _sensitivities:
            self.builder.get_object(_sensitivities[k][0]).grab_focus()
        return state

    def onSimpleClicked(self, btn):
        wid = Gtk.Buildable.get_name(btn)
        self.sensiVisible(wid)
        self.colorTabs()
        if wid not in _ui_unchanged:
            self.changed()

    def onLocalFRTclicked(self, w):
        if self.loadingConfig:
            return
        if self.get('c_frontmatter'):
            self.set('c_colophon', False)
            frtpath = self.configFRT()
            # when FRT doesn't even exist yet, or is empty:
            if not os.path.exists(frtpath) or \
                  (os.path.exists(frtpath) and os.path.getsize(frtpath) == 0):
                self.generateFrontMatter()
                self.rescanFRTvarsClicked(None, autosave=False)
                self.onViewerChangePage(None, None, 0, forced=True)
        else:
            self.set('c_colophon', True)
    
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
        self.disableLayoutAnalysis()
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

    def setOneTwoColumnLabel(self):
        if self.get("c_doublecolumn"):
            self.builder.get_object("c_differentColLayout").set_label(_("Use One Column\nLayout for These Books:"))
        else:
            self.builder.get_object("c_differentColLayout").set_label(_("Use Two Column\nLayout for These Books:"))

    def onSimpleFocusClicked(self, btn):
        self.sensiVisible(Gtk.Buildable.get_name(btn), focus=True)

    def onCallersClicked(self, btn):
        w1 = Gtk.Buildable.get_name(btn)
        status = self.sensiVisible(w1, focus=True)
        for s in ['omitcaller', 'pageresetcallers']:
            w2 = w1[:4]+s
            self.builder.get_object(w2).set_active(status)
        self.changed()

    def onLockUnlockSavedConfig(self, btn):
        if self.cfgid == "Default":
            self.builder.get_object("btn_lockunlock").set_sensitive(False)
            return
        lockBtn = self.builder.get_object("btn_lockunlock")
        dialog = self.builder.get_object("dlg_password")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            pw = self.get("t_password")
        elif response == Gtk.ResponseType.CANCEL:
            pw = ""
        else:
            return
        m = hashlib.md5()
        m.update(pw.encode("utf-8"))
        pw = m.digest()
        invPW = b64decode(self.get("t_invisiblePassword") or "")
        logger.debug(f"{pw=} {invPW=}")
        if invPW == None or not len(invPW): # No existing PW, so set a new one
            self.builder.get_object("t_invisiblePassword").set_text(b64encode(pw).decode("UTF-8"))
            self.onSaveConfig(None, force=True)     # Always save the config when locking
        else: # try to unlock the settings by removing the settings
            if pw == invPW:
                self.builder.get_object("t_invisiblePassword").set_text("")
            else: # Mismatching password - Don't do anything
                pass
        self.builder.get_object("t_password").set_text("")
        dialog.hide()

    def onPasswordChanged(self, t_invisiblePassword):
        lockBtn = self.builder.get_object("btn_lockunlock")
    
        if self.get("t_invisiblePassword") == "":
            status = True
            img = Gtk.Image.new_from_icon_name("changes-allow-symbolic", Gtk.IconSize.LARGE_TOOLBAR)
            lockBtn.set_image(img)
        else:
            status = False
            img = Gtk.Image.new_from_icon_name("changes-prevent-symbolic", Gtk.IconSize.LARGE_TOOLBAR)
            lockBtn.set_image(img)
        for c in ["btn_saveConfig", "btn_deleteConfig", "t_configNotes",
                  "btn_Generate", "btn_plAdd", "btn_plDel"]:
            self.builder.get_object(c).set_sensitive(status)

    def get_adjlist(self, bk, save=True, gtk=None):
        return super().get_adjlist(bk, save=save, gtk=Gtk)

    def onExamineBookChanged(self, cb_examineBook):
        if self.noUpdate == True:
            return
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        self.onViewerChangePage(None, None, pg, forced=True)
        adjl = self.get_adjlist(self.get("ecb_examineBook"), gtk=Gtk)
        if adjl is not None:
            self.adjView.set_model(adjl, save=True)

    def onBookSelectorChange(self, btn):
        if self.get("ecb_booklist") == "" and self.project.prjid is not None:
            self.updateDialogTitle()
        else:
            self.updateDialogTitle()
            bks = self.getBooks()
            if len(bks) > 1:
                self.builder.get_object("ecb_examineBook").set_active_id(bks[0])
        self.updatePicList()

    def updatePicList(self, bks=None, priority="Both", output=False):
        super().updatePicList(bks=bks, priority=priority, output=output)
        if self.picinfos is None:
            return
        filtered = self.get("c_filterPicList")
        if bks is None and filtered:
            bks = self.getBooks()
        if bks is None:
            bks = []
        if self.get('c_frontmatter'):
            bks.append("FRT")
        if self.get('c_useSectIntros'):
            bks.append("INT")
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
        self.picListView.pause()
        if len(self.diglotViews):
            pref = "L"
            self.picinfos = Piclist(self, diglot=True)
        else:
            pref = ""
        newpics = Piclist(self)
        newpics.threadUsfms(self, nosave=True)
        self.picinfos.merge(newpics, pref, mergeCaptions=True, bkanchors=True)
        if len(self.diglotViews):
            for k, v in self.diglotViews.items():
                if v is None:
                    continue
                digpics = Piclist(v)
                digpics.threadUsfms(v, nosave=True)     # is this safe?
                self.picinfos.merge(digpics, k, mergeCaptions=True, bkanchors=True)
        self.updatePicList()
        self.picListView.unpause()
        self.doStatus(_("Done! Picture Captions have been updated."))
        self.changed()

    def onGeneratePicListClicked(self, btn):
        bks2gen = self.getBooks()
        if not len(bks2gen):
            return
        ab = self.getAllBooks()
        bks = bks2gen
        dialog = self.builder.get_object("dlg_generatePL")
        self.set("l_generate_booklist", " ".join(bks))
        # If there is no PicList file for this config, then don't even ask - just generate it
        plpath = os.path.join(self.project.srcPath(self.cfgid),"{}-{}{}.piclist".format(
                        self.project.prjid, self.cfgid, "-diglot" if len(self.diglotViews) else ""))
        if not os.path.exists(plpath):
            response = Gtk.ResponseType.OK
            self.set("r_generate", "all")
        else:
            response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.savePics()
            if self.get("r_generate") == "all":
                procbks = ab.keys()
                doclear = True and not self.get("c_protectPicList", True)
            else:
                procbks = bks
                doclear = False
            self.generatePicList(procbks=procbks, doclear=doclear)
            self.savePics()
            if self.get('r_generate') == 'all':
                self.set("c_filterPicList", False)
            self.changed()
        dialog.hide()

    def onFilterPicListClicked(self, btn):
        self.updatePicList()

    def onGenerateClicked(self, btn):
        # priority=self.get("fcb_diglotPicListSources")
        pg = self.get("nbk_Viewer")
        pgid = self.notebooks['Viewer'][pg]
        bks2gen = self.getBooks()
        if not len(bks2gen):
            return
        bk = self.get("ecb_examineBook")
        if pgid == "tb_FrontMatter":
            ptFRT = os.path.exists(os.path.join(self.project.path, self.getBookFilename("FRT", self.project.prjid)))
            self.builder.get_object("r_generateFRT_paratext").set_sensitive(ptFRT)
            dialog = self.builder.get_object("dlg_generateFRT")
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                self.generateFrontMatter(self.get("r_generateFRT"), self.get("c_includeCoverSections"))
                self.rescanFRTvarsClicked(None, autosave=False)
                self.changed()
            dialog.hide()

        if pgid == "tb_AdjList":
            if bk not in bks2gen:
                self.doError(_("The Book in focus is not within scope"), 
                    secondary=_("To generate an AdjList, the book must be\n"+
                                "in the list of books to be printed."))
                return
            self.generateAdjList()
            self.changed()

        elif pgid == "tb_FinalSFM" and bk is not None:
            bk = bk if bk in bks2gen else None
            self.wipe_usfms([bk])
            tmodel = TexModel(self, self._getPtSettings(self.project.prjid), self.project.prjid)
            out = tmodel.convertBook(bk, None, self.project.printPath(self.cfgid), self.project.path)
            self.editFile(out, loc="wrk", pgid=pgid)
            self.changed()
        self.onViewerChangePage(None, None, pg, forced=True)

    def generateAdjList(self, books=None, dynamic=True):
        existingFilelist = []
        booklist = self.getBooks() if books is None else books
        diglot = self.get("c_diglot")
        prjid = self.project.prjid
        prjdir = self.project.path
        usfms = self.get_usfms()
        if diglot:
            for v in self.diglotViews.values():
                dusfms = v.get_usfms()
        skipbooks = []
        for bk in booklist:
            fname = self.getAdjListFilename(bk, ext=".adj")
            outfname = os.path.join(self.project.srcPath(self.cfgid), "AdjLists", fname)
            if os.path.exists(outfname):
                if os.path.getsize(outfname) > 0:
                    existingFilelist.append(re.split(r"\\|/",outfname)[-1])
        forceAdjs = False
        if len(existingFilelist):
            if len(existingFilelist) > 13:
                existingFilelist = existingFilelist[:6] + ["..."] + existingFilelist[-6:]
            q1 = _("One or more Adjust List(s) already exist!")
            q2a = _("Do you want to OVERWRITE the existing list(s)?")
            q2b = _("Yes - Wipe out existing list(s) and start again")
            q2c = _("No - Keep existing list(s) and merge new [safe option]")
            q2d = _("Cancel - leave Adjust List(s) as they are [do nothing]")
            q2 = "\n".join(existingFilelist) + f"\n\n{q2a}\n   {q2b}\n   {q2c}\n   {q2d}"
            par = self.builder.get_object('ptxprint')
            dialog = Gtk.MessageDialog(parent=par, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.NONE, message_format=q1)
            dialog.add_buttons("Yes", Gtk.ResponseType.YES, "No", Gtk.ResponseType.NO, "Cancel", Gtk.ResponseType.CANCEL)
            dialog.format_secondary_text(q2)
            response = dialog.run()
            dialog.destroy()            
            if response == Gtk.ResponseType.YES:
                forceAdjs = True
            elif response == Gtk.ResponseType.NO:
                forceAdjs = False
            elif response == Gtk.ResponseType.CANCEL:
                return
        if not len(booklist):
            return
        parlocs = os.path.join(self.project.printPath(self.cfgid), self.baseTeXPDFnames()[0] + ".parlocs")
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
                    k = (m[0], int(m[1]))
                    adjs.setdefault(k, [0]*3+[""])[i] = int(m[2])
                    adjs[k][3] = m[3]
        adjpath = os.path.join(self.project.srcPath(self.cfgid), "AdjLists")
        os.makedirs(adjpath, exist_ok=True)
        for bk in booklist:
            adj = self.get_adjlist(bk, save=False, gtk=Gtk)
            if forceAdjs:
                adj.clear()
            for k, v in sorted(adjs.items(), key=lambda x:refSort(x[0][0])):
                r = refKey(k[0])
                logger.debug(f"{k=} {r=}, {v=}")
                s = getsign(*v) + "0"
                if k[0][:3] != bk:
                    continue
                elif r[0] >= 100 or (r[1] == 0 and r[2] == 0): # May need to take these lines out!
                    adj.setval(bk + r[3], ("{}.".format(r[4]) if len(r[4]) else "") + r[5], int(k[1]), s, v[3], force=forceAdjs)
                    continue                   # May need to take these lines out!
                adj.setval(bk + r[3], "{}.{}{}".format(r[1], r[2], r[4]) + r[5], int(k[1]), s, v[3], force=forceAdjs)
            if not adj.adjfile:
                adj.adjfile = os.path.join(self.project.srcPath(self.cfgid), "AdjLists", self.getAdjListFilename(bk))
            adj.sort()
            adj.changed = True

    def onChangedMainTab(self, nbk_Main, scrollObject, pgnum=-1):
        pgid = Gtk.Buildable.get_name(nbk_Main.get_nth_page(pgnum))
        if pgid == "tb_Viewer": # Viewer tab
            self.onRefreshViewerTextClicked(None)
        elif pgid == "tb_TabsBorders":
            self.onThumbColorChange()
        elif pgid == "tb_Pictures":
            self.onPLpageChanged(None, None, pgnum=-1)

    def onRefreshViewerTextClicked(self, btn):
        pg = self.get("nbk_Viewer")
        self.onViewerChangePage(None, None, pg, forced=True)
        
    def clearEditableBuffers(self):
        self.fileViews[0][0].set_text("")

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
        # self.builder.get_object("btn_removeZeros").set_visible(False)
        prjid = self.get("fcb_project")
        if prjid is None:
            return          # at least we don't crash if there is no project
        self.noUpdate = True
        prjdir = self.project.path
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

        fndict = {"tb_FrontMatter" : ("", ""), "tb_AdjList" : ("AdjLists", ".adj"),
                  "tb_FinalSFM" : ("", ""), "tb_TeXfile" : ("", ".tex"),
                  "tb_XeTeXlog" : ("", ".log"), "tb_Settings1": ("", ""),
                  "tb_Settings2": ("", ""), "tb_Settings3": ("", "")}

        if pgid == "tb_FrontMatter":
            ibtn.set_sensitive(True)
            ibtn.set_tooltip_text(self.frtMatterTooltip)
            fpath = self.configFRT()
            if fpath is None:
                return
            buf = self.fileViews[pgnum][0]
            if forced or buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True) == "":
                if not os.path.exists(fpath):
                    logger.debug(f"Front matter from {fpath} does not exist")
                    self.uneditedText[pgnum] = _("\\rem Click the Generate button (above) to start the process of creating Front Matter...")
                    buf.set_text(self.uneditedText[pgnum])
                else:
                    with open(fpath, "r", encoding="utf-8") as inf:
                        txt = inf.read()
                        buf.set_text(txt)
            self.enableCodelets(pgnum, fpath)
            self.noUpdate = False
            self.builder.get_object("l_{1}".format(*pgid.split("_"))).set_tooltip_text(fpath)
            fpath = None
            if self.get("t_invisiblePassword") == "":
                genBtn.set_sensitive(True)
                self.builder.get_object("btn_editZvars").set_visible(True)
            else:
                logger.debug(f"Front matter from {fpath} exists")
                self.builder.get_object("c_autoSave").set_sensitive(False)
                self.set("c_autoSave", False)
            return
        elif pgid == "tb_FinalSFM":
            fname = self.getBookFilename(bk, prjid)
            fpath = os.path.join(self.project.printPath(self.cfgid), fndict[pgid][0], fname)
            genBtn.set_sensitive(True)
            doti = fpath.rfind(".")
            if doti > 0:
                if self.get("c_diglot"):
                    fpath = fpath[:doti] + "-" + (self.cfgid or "Default") + "-diglot" + fpath[doti:] + fndict[pgid][1]
                else:
                    if self.get("r_book") == "module":
                        modname = os.path.basename(self.moduleFile)
                        doti = modname.rfind(".")
                        fpath = os.path.join(self.project.printPath(self.cfgid), modname[:doti] + "-flat" + modname[doti:])
                    else:
                        fpath = fpath[:doti] + "-" + (self.cfgid or "Default") + fpath[doti:] + fndict[pgid][1]
            self.builder.get_object("c_autoSave").set_sensitive(False)
            self.builder.get_object("btn_refreshViewerText").set_sensitive(False)
            self.builder.get_object("btn_viewEdit").set_label(_("View Only..."))

        elif pgid == "tb_AdjList":
            genBtn.set_sensitive(True)
            fpath = None
            for w in ["l_codeSnippets", "box_codelets", "lb_snippets"]:
                self.builder.get_object(w).set_visible(False)

        elif pgid in ("tb_TeXfile", "tb_XeTeXlog"): # (TeX,Log)
            fpath = os.path.join(self.project.printPath(self.cfgid), self.baseTeXPDFnames()[0])+fndict[pgid][1]
            self.builder.get_object("c_autoSave").set_sensitive(False)
            self.builder.get_object("btn_refreshViewerText").set_sensitive(False)
            self.builder.get_object("btn_viewEdit").set_label(_("View Only..."))

        elif pgid in ("tb_Settings1", "tb_Settings2", "tb_Settings3"): # mulit-purpose View/Edit tabs
            lname = "l_{1}".format(*pgid.split('_'))
            fpath = self.builder.get_object(lname).get_tooltip_text()
            if fpath == None:
                self.uneditedText[pgnum] = _("Use the 'Advanced' tab to select which settings you want to view or edit.")
                self.fileViews[pgnum][0].set_text(self.uneditedText[pgnum])
                self.builder.get_object(lname).set_text("Settings")
                self.noUpdate = False
                return
            else:
                self.enableCodelets(pgnum, fpath)
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
                if len(txt) > 60000 and pgid not in ("tb_AdjList",):
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
        self.enableCodelets(pgnum, fpath)
        self.noUpdate = False
        self.onViewEdited()

    def enableCodelets(self, pgnum, fpath):
        if self.loadingConfig:
            return
        pgcats = ['Front', None, None, None, None, 'File', 'File', 'File']
        cat = pgcats[pgnum]
        if self.currCodeletVbox is not None:
            self.currCodeletVbox.hide()
            self.currCodeletVbox.set_no_show_all(True)
            self.currCodeletVbox.set_visible(False)
            self.currCodeletVbox = None
        if cat is None:
            return
        else:
            for w in ["l_codeSnippets", "box_codelets", "lb_snippets"]:
                self.builder.get_object(w).set_visible(True)
        if cat == 'File':
            cat = os.path.splitext(fpath)[1].lower()  # could be .txt, .tex, or .sty
        if not len(self.codeletVboxes):
            self.loadCodelets()
        self.currCodeletVbox = self.codeletVboxes.get(cat, None)
        if self.currCodeletVbox is not None:
            self.currCodeletVbox.set_no_show_all(False)
            self.currCodeletVbox.set_visible(True)
            self.currCodeletVbox.show_all()
        
    def loadCodelets(self):
        # Read codelets from JSON file
        with universalopen(os.path.join(pycodedir(), 'codelets.json')) as file:
            codelets = json.load(file)

        daddybox = self.builder.get_object("box_codelets")
        for cat, info in codelets.items():
            vb = Gtk.VBox(daddybox)
            self.codeletVboxes[cat] = vb
            self.builder.expose_object(f"vb_{cat}", vb)
            daddybox.pack_start(vb, True, False, 6)
            
            # Add categories and buttons
            for category, codeitems in info.items():
                # if category == "Arabic" and self.get('fcb_script') != 'Arab': # FixMe!MP (this needs to updated when we
                    # print(f"Skipping Arabic")                                 # change projects/configs but it doesn't
                    # continue                                                  # because the menu is already populated.
                    #                              Need to run loadCodelets whenever project, or config, or script are changed.
                bname = f"btn_{cat}_{category}"
                button = Gtk.Button.new_with_label(category)
                self.widgetnames[bname] = f"Insert Codelet {cat} {category}"
                self.builder.expose_object(bname, button)
                self.allControls.append(bname)
                button.set_focus_on_click(False)
                button.set_halign(Gtk.Align.START)
                button.set_size_request(100, -1)
                vb.pack_start(button, True, False, 6)

                submenu = Gtk.Menu()
                for i, codelet in enumerate(codeitems):
                    mname = f"codelets_{cat}_{category}_{i}"
                    menu_item = Gtk.MenuItem(label=codelet["Label"])
                    menu_item.set_tooltip_text(codelet["Description"])
                    menu_item.connect("activate", self.insert_codelet, codelet)
                    submenu.append(menu_item)
                    self.finddata[codelet["Label"].lower()] = (bname, 1)
            
                button.connect("clicked", self.showCodeletMenu, submenu)

            vb.set_no_show_all(True)

    def showMakeTatweelRuleDialog(self):
        # Instantiate TatweelDialog and display it
        if not hasattr(self, 'tatweel_dialog'):
            font = str(self.get('bl_fontR', None)).split("|")[0]
            self.dialog = TatweelDialog(self.builder, font)
        else:
            self.tatweel_dialog.show_all()

    def showCodeletMenu(self, button, menu):
        menu.show_all()
        menu.popup(None, None, None, None, 0, Gdk.CURRENT_TIME)

    def insert_codelet(self, menu_item, codelet):
        code_codelet = codelet.get("CodeSnippet", codelet["Label"])
        nbk_Viewer = self.builder.get_object("nbk_Viewer")
        pgnum = nbk_Viewer.get_current_page()
        buf = self.fileViews[pgnum][0]

        # Get the iterator at the current cursor position
        cursor_iter = buf.get_iter_at_mark(buf.get_insert())
        ty = codelet['Type']

        if not self.get("t_invisiblePassword") == "":
            # Don't let any changes be made to a locked config!
            # Ideally we should disable all the codelet buttons if it is locked.
            return
        
        if ty.startswith('global') or ty.startswith('line'):
            find = code_codelet.split(' > ')[0]
            repl = code_codelet.split(' > ')[1]
            if ty.startswith('global'):
                oldtext = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
                self.fileViews[pgnum][0].set_text(re.sub(find, repl, oldtext))
            elif ty.startswith('line'):
                start_iter = buf.get_iter_at_line(cursor_iter.get_line())
                end_iter = buf.get_iter_at_line(cursor_iter.get_line() + 1)
                newtext = buf.get_text(start_iter, end_iter, include_hidden_chars=False)
                oldtext = ''
                while oldtext != newtext:
                    oldtext = newtext
                    newtext = re.sub(find, repl, oldtext)
                    if ty == 'line':
                        break
                buf.begin_user_action()
                buf.delete(start_iter, end_iter)
                buf.insert(start_iter, newtext)
                buf.end_user_action()
            self.changed()
            return

        if ty.startswith('comment'):
            txt = f"{ty[7:]} {codelet['Label']}\n{code_codelet}\n"
            buf.insert(cursor_iter, txt)
        elif ty.startswith('method'):
            m = getattr(self, code_codelet, None)
            if m is not None:
                m()
        else:
            txt = f"{code_codelet}\n"
            buf.insert(cursor_iter, txt)
            self.changed()

    def on_insert_tatweel_rule(self, button):
        w = self.builder.get_object("t_tatweelPreview")
        rule_text = w.get_text()
        nbk_Viewer = self.builder.get_object("nbk_Viewer")
        pgnum = nbk_Viewer.get_current_page()
        buf = self.fileViews[pgnum][0]
        cursor_iter = buf.get_iter_at_mark(buf.get_insert())
        buf.insert(cursor_iter, rule_text+'\n')
        self.changed()        
        
    def savePics(self, fromdata=False, force=False):
        if not force and self.configLocked():
            return
        if not fromdata and self.picinfos is not None and self.picinfos.loaded:
            self.picListView.updateinfo(self.picinfos)
        super().savePics(fromdata=fromdata, force=force)

    def loadPics(self, mustLoad=True, fromdata=True, force=False):
        super().loadPics(mustLoad=mustLoad, fromdata=fromdata, force=force)
        self.updatePicList()

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
        if pgid == "tb_AdjList":
            self.adjView.adjlist.save()
            fpath = None
        elif pgid == "tb_FrontMatter":
            fpath = self.configFRT()
        else:
            fpath = self.builder.get_object("l_{1}".format(*pgid.split("_"))).get_tooltip_text()
        if fpath is None: return
        titer = buf.get_iter_at_mark(buf.get_insert())
        self.cursors[pg] = (titer.get_line(), titer.get_line_offset())
        text2save = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        if text2save is None or text2save == "":
            return
        openfile = open(fpath,"w", encoding="utf-8")
        openfile.write(text2save)
        openfile.close()
        self.uneditedText[pg] = text2save
        self.onViewEdited()

    def onOpenInSystemEditor(self, btn):
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        pgid = self.notebooks["Viewer"][pg]
        fpath = self.builder.get_object("l_{1}".format(*pgid.split("_"))).get_tooltip_text() or ""
        startfile(fpath)

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

        if not self.loadingConfig:
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
        self.changed()

    def onChangeViewEditFontSize(self, btn, foo):
        self.setEntryBoxFont()

    def setEntryBoxFont(self):
        # Set the font of any GtkEntry boxes to the primary body text font for this project
        fsize = self.get("s_viewEditFontSize")
        if fsize is None:
            fsize = "12"
        fontr = self.get("bl_fontR", skipmissing=True)
        if fontr is None:
            return
        fallbacks = ['Source Code Pro']
        if len(self.diglotViews):
            for v in self.diglotViews.values():
                if v is None:
                    continue
                digfontr = v.get("bl_fontR")
                fallbacks.append(digfontr.name)
        pangostr = fontr.asPango(fallbacks, fsize)
        p = Pango.FontDescription(pangostr)
        logger.debug(f"{pangostr=}, {p}")
        for w in ("t_clHeading", "t_tocTitle", "t_configNotes", \
                  "tb_FinalSFM", "tb_AdjList", "tb_FrontMatter", \
                  "tb_Settings1", "tb_Settings2", "tb_Settings3", \
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
        if n not in _ui_unchanged:
            self.changed()

    def onPicRadioChanged(self, btn):
        self.onRadioChanged(btn)
        self.picListView.onRadioChanged()
        self.changed()
    
    def onReverseRadioChanged(self, btn):
        self.onPicRadioChanged(btn)
        self.picChecksView.onReverseRadioChanged()
        self.changed()
    
    def onSectionHeadsClicked(self, btn):
        self.onSimpleClicked(btn)
        status = self.sensiVisible("c_sectionHeads")
        self.builder.get_object("c_parallelRefs").set_active(status)

    def onUseIllustrationsClicked(self, btn):
        changed = not self.loadingConfig
        pics = self.get("c_includeillustrations")
        self.colorTabs()
        if pics:
            self.loadPics(force=False)
        else:
            self.picinfos.clear(self)
            self.picListView.clear()
        self.onPicRescan(None)
        self.picPreviewShowHide(pics)
        self.changed(changed)
        
    def reloadDiglotPics(self, digView, old, new):
        super().reloadDiglotPics(digView, old, new)
        pics = self.get("c_includeillustrations")
        if pics and self.picListView:
            self.picListView.load(self.picinfos)
        
    def picPreviewShowHide(self, show=True):
        for w in ["bx_showImage", "tb_picPreview"]:
            self.builder.get_object(w).set_visible(show)
            
    def onUseCustomFolderclicked(self, btn):
        status = self.sensiVisible("c_useCustomFolder")
        if not status:
            self.builder.get_object("c_exclusiveFiguresFolder").set_active(status)
        else:
            if not self.get("lb_selectFigureFolder"):
                self.onSelectFigureFolderClicked(None)
        self.onPicRescan(btn)
        
    def onPrefImageTypeFocusOut(self, btn, foo):
        self.onPicRescan(btn)
        
    def onPicRescan(self, btn, changed=True):
        self.picListView.clearSrcPaths()
        self.picListView.onRadioChanged()
        self.changed(changed)
        
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
        self.changed()

    def onResetXRcallersClicked(self, btn_resetXRcallers):
        w = self.builder.get_object("t_xrcallers")
        ptset = re.sub(" ", ",", self.ptsettings.get('crossrefs', ""))
        if ptset == "" or w.get_text() == ptset:
            w.set_text("†,‡,§,∥,#")
        else:
            w.set_text(ptset)
        self.changed()

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
            self.set("c_RTLbookBinding", rtl)

    def onEditStyleClicked(self, btn):
        mkr = Gtk.Buildable.get_name(btn)[9:].strip("_")
        if mkr == "toc3" and self.get("r_thumbText") == "zthumbtab":  # "c_thumbIsZthumb"):
            self.set("c_styTextProperties", False, mod=False)  # MH: why is this being done?
            mkr = "zthumbtab"
        elif mkr == "x-credit|fig":
            dialog = self.builder.get_object("dlg_overlayCredit")
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
            self.builder.get_object("ptxprint").present()
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
        self.changed()

    def onIntroOutlineClicked(self, btn):
        if not self.sensiVisible("c_introOutline"):
            self.builder.get_object("c_prettyIntroOutline").set_active(False)
        self.changed()

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
            tfont = self.get("bl_fontR")
            name = tfont.name if tfont is not None else None
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
            self.set("fcb_featsLangs", lang, mod=False)
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
            self.set("t_fontFeatures", ", ".join(results), mod=False)
        for i in range(numrows-1, -1, -1):
            featbox.remove_row(i)
        self.builder.get_object("fcb_featsLangs").disconnect(langChangedId)
        dialog.hide()

    def onFontIsGraphiteClicked(self, btn):
        self.onSimpleClicked(btn)
        self.set("t_fontFeatures", "", mod=False)

    # this is copied from 'onFontFeaturesClicked' in order to do something similar with TeXpert options

    # Dict looks like this:
#          "notesEachBook": ["Endnotes at Each Book", "Output endnotes at the end of each book", True],
    # Results need to look like this:
#          \ifnotesEachBookfalse   (and should only be set if option is set different to the default value)

    def setupTeXOptions(self):
        groupCats = {
            'LAY': 'Page Layout and Spacing',
            'CVS': 'Chapter and Verse',
            'BDY': 'Body Text',
            'FNT': 'Fonts and Underline',
            'NTS': 'Footnotes, Cross-references, Study Notes',
            'DIG': 'Diglot',
            'PIC': 'Pictures, Figures, Images, Sidebars', 
            'PDF': 'PDF Options, Show/Hide',
            'PRV': 'Preview Pane: Adjustment and Analysis Settings',
            'OTH': 'Other Miscellaneous Settings' }

        texopts = self.builder.get_object("gr_texoptions")
        expanders = {} # Dictionary to hold expanders for each group
        row_index = 0  # Track the overall row index for the main grid
        for k, opt, wname in TeXpert.opts():
            # Check if the group already has an expander, if not create one
            if opt.group not in expanders:
                expander_label = Gtk.Label()
                expander_label.set_markup(f"<span weight='bold' foreground='cornflowerblue'>{groupCats[opt.group]}</span>")
                expander_label.set_halign(Gtk.Align.START)
                expander_label.set_margin_top(9)  # Add some top margin for padding
                expander_label.set_margin_bottom(9)  # Add bottom margin for padding

                expander = Gtk.Expander()
                expander.set_label_widget(expander_label)  # Use the custom label widget for the expander
                expander.set_halign(Gtk.Align.FILL)
                expander.set_hexpand(True)
                expander.set_vexpand(False)
                texopts.insert_row(row_index)
                texopts.attach(expander, 0, row_index, 3, 1)
                row_index += 1
                expanders[opt.group] = expander
                self.builder.expose_object("ex_texpert"+opt.group, expander)

                # Create a new grid for each expander
                grid = Gtk.Grid()
                grid.set_column_spacing(6)
                grid.set_row_spacing(6)
                
                # Set the width of the first column to a fixed value (e.g., 200)
                grid.get_column_homogeneous()
                grid.get_style_context().add_class("grid")
                grid.set_column_homogeneous(True)  # Ensures uniform column width distribution               
                self.builder.expose_object("gr_texpert"+opt.group, grid)

                expander.add(grid)
            else:
                grid = expanders[opt.group].get_child()

            # Add the widgets to the grid within the appropriate expander
            row = len(grid.get_children()) // 2  # Calculate current row based on number of children
            label = Gtk.Label(label=opt.name + ":")
            label.set_halign(Gtk.Align.END)
            lname = "l_"+wname[wname.index("_")+1:]
            self.builder.expose_object(lname, label)

            findname = wname
            changeMethod = None
            if opt.group == "PRV":
                changeMethod = "viewerValChanged"
            if wname.startswith("c_"):
                obj = Gtk.CheckButton()
                self.btnControls.add(wname)
                v = opt.val
                tiptext = "{k}:\t[{val}]\n\n{descr}".format(k=k, **asdict(opt))
                findname = lname
                self.initValues[wname] = v
                changeMethod = changeMethod or getattr(opt, "method", None) or "buttonChanged"
                obj.connect("clicked", getattr(self, changeMethod))
            elif wname.startswith("s_"):
                x = opt.val
                adj = Gtk.Adjustment(value=x[0], lower=x[1], upper=x[2], step_increment=x[3], page_increment=x[4])
                obj = Gtk.SpinButton()
                obj.set_adjustment(adj)
                obj.set_digits(x[5])  # Set the number of decimal places
                changeMethod = changeMethod or getattr(opt, "method", None) or "labelledChanged"
                # put the label in an EventBox and then add button-release-event on the eventbox
                obj.connect("value-changed", getattr(self, changeMethod))
                eb = Gtk.EventBox()
                eb.add(label)
                eb.connect("button-release-event", getattr(self, "resetLabel"))
                label = eb
                v = str(x[0])
                self.initValues[wname] = v
                tiptext = "{k}:\t[{val}]\n\n{descr}".format(k=k, **asdict(opt))
            elif wname.startswith("fcb_"):
                obj = Gtk.ComboBoxText()
                for i, (a, b) in enumerate(opt.val.items()):
                    obj.append(a, b)
                    if i == 0:
                        v = a
                obj.set_entry_text_column(0)
                obj.set_id_column(1)
                obj.set_active_id(v)
                tiptext = "{k}:\t[{v}]\n\n{descr}".format(k=k, v=v, **asdict(opt))

            grid.attach(label, 0, row, 1, 1)
            label.show()
            label.set_tooltip_text(tiptext)
            self.finddata[tiptext.lower()] = (findname, 1)
            self.finddata[opt.name.lower()] = (findname, 4)
            self.widgetnames[findname] = opt.name
            obj.set_tooltip_text(tiptext)
            obj.set_halign(Gtk.Align.START)
            grid.attach(obj, 1, row, 1, 1)
            self.builder.expose_object(wname, obj)
            if wname in self.dict:
                v = self.dict[wname]
            self.set(wname, v, mod=False)
            if wname.startswith("c_"): # Making sure that even the unchecked labels get bold applied if not default
                lbl = obj.get_child()
                self.changeLabel(wname, lbl)
            self.allControls.append(wname)
            obj.show()
            expanders[opt.group].show_all()  # Ensure that the expander and its content are shown

    def btnUnpackClicked(self, btn):
        file2unpack = self.builder.get_object("btn_pdfZip2unpack")
        unpack2fldr = self.builder.get_object("btn_unpack2folder")
        try:
            confstream = getPDFconfig(file2unpack.get_filename())
            zipinf = BytesIO(confstream)
            zipdata = ZipFile(zipinf, compression=ZIP_DEFLATED)
            zipdata.extractall(unpack2fldr.get_filename())
            self.doStatus(_("PDF settings unpacked. That was easy, wasn't it!"))
            startfile(unpack2fldr.get_filename())
        except BadZipFile as e:
            self.doStatus(_("Sorry, that PDF doesn't seem to be a valid PTXprint file with config settings included in it."))

    def setup_book_button_styles(self):
        """Generates and applies CSS for book button coloring. Call once at init."""
        css_style = ""
        for category_key, colors in _categoryColors.items():
            normal_bg = colors["normal"]
            checked_bg = colors["checked"]
            text_color = colors["text"]
            try:
                gdk_rgba_normal = Gdk.RGBA()
                gdk_rgba_normal.parse(normal_bg)
                gdk_rgba_normal_darker = Gdk.RGBA(
                    red=max(0, gdk_rgba_normal.red - 0.05),
                    green=max(0, gdk_rgba_normal.green - 0.05),
                    blue=max(0, gdk_rgba_normal.blue - 0.05),
                    alpha=gdk_rgba_normal.alpha
                )
                hover_bg = gdk_rgba_normal_darker.to_string()
            except:
                hover_bg = normal_bg
            css_class_name = f"category-{category_key.lower().replace('_', '-')}-button"
            css_style += f"""
            .book-toggle-button.{css_class_name} {{
                background-image: none;
                background-color: {normal_bg};
                color: {text_color};
                border: 1px solid #D0D0D0; /* Lighter border for subtler look */
                border-radius: 3px;
            }}
            .book-toggle-button.{css_class_name}:checked {{
                background-color: {checked_bg};
                color: {text_color};
                border: 1px solid #909090;
                font-weight: bold; /* This line is new! */
            }}
            .book-toggle-button.{css_class_name}:hover {{
                background-color: {hover_bg};
            }}
            """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css_style.encode('utf-8'))
        screen = Gdk.Screen.get_default()
        if screen:
            Gtk.StyleContext.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def onChooseBooksClicked(self, btn):
        dialog = self.builder.get_object("dlg_multiBookSelector")
        mbs_grid = self.builder.get_object("mbs_grid")
        mbs_grid.forall(mbs_grid.remove)
        lsbooks = self.builder.get_object("ls_books")
        bl = self.getBooks(scope="multiple", local=True)
        self.alltoggles = []
        for i, b_row in enumerate(lsbooks):
            book_id = b_row[0]
            tbox = Gtk.ToggleButton(label=book_id)
            tbox.get_style_context().add_class("book-toggle-button")
            category = _bookToCategory.get(book_id, "Default")
            css_class_name = f"category-{category.lower().replace('_', '-')}-button"
            tbox.get_style_context().add_class(css_class_name)
            tbox.show()
            if book_id in bl:
                tbox.set_active(True)
            self.alltoggles.append(tbox)
            mbs_grid.attach(tbox, i // 13, i % 13, 1, 1)
        response = dialog.run()
        booklist = []
        if response == Gtk.ResponseType.OK:
            booklist = sorted((b.get_label() for b in self.alltoggles if b.get_active()), \
                                    key=lambda x:_allbkmap.get(x, len(_allbkmap)))
            self.set("ecb_booklist", " ".join(b for b in booklist), mod=False)
        if not self.loadingConfig and self.get("r_book") in ("single", "multiple"):
            self.set("r_book", "multiple" if len(booklist) else "single", mod=False)
        self.doBookListChange()
        self.updateDialogTitle()
        self.disableLayoutAnalysis()
        self.updateExamineBook()
        self.updatePicList()
        dialog.hide()
        
    def onChooseTargetProjectsClicked(self, btn):
        dialog = self.builder.get_object("dlg_multiProjSelector")
        mps_grid = self.builder.get_object("mps_grid")
        mps_grid.forall(mps_grid.remove)
        self.alltoggles = []
        prjs = self.builder.get_object("ls_projects")
        prjCtr = len(prjs)
        cols = int(prjCtr**0.6) if prjCtr <= 70 else 5
        for i, b in enumerate(prjs):
            if self.project.guid == b[1]:
                tbox = Gtk.Label()
                tbox.set_text('<span background="black" foreground="white" font-weight="bold">  {} </span>'.format(b[0]))
                tbox.set_use_markup(True)
            else:
                tbox = Gtk.ToggleButton(b[0])
            tbox.show()
            self.alltoggles.append((tbox, b[1]))
            mps_grid.attach(tbox, i % cols, i // cols, 1, 1)
        response = dialog.run()
        projlist = []
        if response == Gtk.ResponseType.OK:
            cfg = self.cfgid
            for b, g in self.alltoggles:
                try:
                    if b.get_active():
                        projlist.append(self.prjTree.getProject(g))
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
                    with open(os.path.join(p.path, "unique.id"), "w") as outf:
                        outf.write("ptxprint-{}".format(datetime.datetime.now().isoformat(" ")))
                except FileNotFoundError as e:
                    self.doError(_("File not found"), str(e))
        dialog.hide()
        
    def updateExamineBook(self):
        try:
            bks = self.getBooks()
        except (SyntaxError, ValueError):     # mid typing the reflist may be bad
            return
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
        self.set("r_book", "single", mod=False)
            
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
        self.blInitValue = self.get("ecb_booklist")

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
        self.disableLayoutAnalysis()
        self.updatePicList()
        # print("onBookChange-s")
        self.set("r_book", "single")
        if not self.loadingConfig:
            self.showmybook()

    def _setNoteSpacingRange(self, fromTo, minimum, maximum, value):
        initSpace = int(float(self.get('s_notespacing'+fromTo)))
        spacing = self.builder.get_object('s_notespacing'+fromTo)
        spacing.set_range(minimum, maximum)
        if value:
            spacing.set_value(value if value in range(minimum, maximum) else (minimum if fromTo == "min" else maximum))
        else:
            spacing.set_value(initSpace if initSpace in range(minimum, maximum) else (minimum if fromTo == "min" else initSpace + 4))
        self.changed()

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
        self.set("l_styColor", _("Color:")+"\n"+col)
        if col != "x000000" and not self.get("c_colorfonts"):
            self.set("c_colorfonts", True)
            self.doStatus(_("'Enable Colored Text' has now been turned on. (See Fonts+Script tab for details.)"))

    def getConfigName(self):
        cfg = self.pendingConfig or self.get("ecb_savedConfig") or ""
        cfgName = re.sub('[^-a-zA-Z0-9_()]+', '', cfg)
        if self.pendingConfig is None:
            self.set("ecb_savedConfig", cfgName)
        else:
            self.pendingConfig = cfgName
        return cfgName or self.cfgid

    def onSaveAsNewConfig(self, w):
        self.set("t_configName", "")
        dialog = self.builder.get_object("dlg_configName")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            cfg = self.get("t_configName")
            self.set("ecb_savedConfig", cfg)
            self.doConfigNameChange(cfg)
            self.changed()
            self.onSaveConfig(None)
            self.updateConfigIdentity(cfg)
        dialog.hide()

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
        # breakpoint()
        if not self.initialised:
            return
        self.builder.get_object("btn_saveConfig").set_sensitive(True)
        # self.builder.get_object("btn_deleteConfig").set_sensitive(False)
        lockBtn = self.builder.get_object("btn_lockunlock")
        # lockBtn.set_label("Lock")
        lockBtn.set_sensitive(False)
        w = self.builder.get_object("fcb_project")
        m = w.get_model()
        aid = w.get_active_iter()
        prjid = m.get_value(aid, 0)
        guid = m.get_value(aid, 1)
        cfgname = self.pendingConfig or self.userconfig.get('projects', prjid, fallback="Default")
        # Q: Why is saveme never used below?
        saveme = self.pendingPid is None and self.pendingConfig is None
        self.updateProjectSettings(prjid, guid, saveCurrConfig=True, configName=cfgname)
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
        if self.get("t_copyrightStatement") == "":
            self.fillCopyrightDetails()
        # print(f"In onProjectChanged. About to call onUseIllustrationsClicked {self.initialised=}  {self.loadingConfig=}")
        # self.onUseIllustrationsClicked(None) # Not sure why this was there. Removed 16-1-2025
        self.updatePrjLinks()
        self.checkFontsMissing()
        self.changed(False)

    def updatePrjLinks(self):
        if self.project is not None:
            self.set("lb_ptxprintdir", '<a href="{}">{}</a>'.format(pt_bindir(), pt_bindir()))

            projdir = self.project.path
            self.set("lb_prjdir", '<a href="{}">{}</a>'.format(projdir, projdir))

            stngdir = self.project.srcPath(self.cfgid) or ""
            self.set("lb_settings_dir", '<a href="{}">{}</a>'.format(stngdir, stngdir))

            tmp = self.project.printPath(self.cfgid)
            outdir = tmp.rstrip(self.cfgid) or "" if tmp is not None else ""
            self.set("lb_working_dir", '<a href="{}">{}</a>'.format(outdir, outdir))
            
    def updateProjectSettings(self, prjid, guid, saveCurrConfig=False, configName=None, readConfig=None):
        if prjid == getattr(self.project, 'prjid', None) and configName == self.cfgid:
            return True
        self.picListView.clear()
        if self.picinfos is not None:
            self.picinfos.clear()
        if not super(GtkViewModel, self).updateProjectSettings(prjid, guid, saveCurrConfig=saveCurrConfig, configName=configName, readConfig=readConfig):
            for fb in ['bl_fontR', 'bl_fontB', 'bl_fontI', 'bl_fontBI', 'bl_fontExtraR']:
                fblabel = self.builder.get_object(fb).set_label("Select font...")
        if self.project.prjid:
            self.updatePrjLinks()
            self.userconfig.set("init", "project", self.project.prjid)
            if self.cfgid is not None:
                self.userconfig.set("init", "config", self.cfgid)
                if not self.userconfig.has_section("projects"):
                    self.userconfig.add_section("projects")
                self.userconfig.set('projects', self.project.prjid, self.cfgid)
        books = self.getBooks()
        if self.get("r_book") in ("single", "multiple") and (books is None or not len(books)):
            books = self.getAllBooks()
            for b in allbooks:
                if b in books.keys():
                    self.set("ecb_book", b)
                    self.set("r_book", "single")
                    break
        for i in self.notebooks['Viewer']:
            obj = self.builder.get_object("l_{1}".format(*i.split("_")))
            if obj is not None:
                obj.set_tooltip_text(None)
        books = self.getBooks()
        if len(books):
            self.adjView.set_model(self.get_adjlist(books[0], gtk=Gtk))
        self.updatePrjLinks()
        self.setEntryBoxFont()
        self._setup_digits()
        self.updatePicList()
        self.updateDialogTitle()
        self.disableLayoutAnalysis()  # Do we need this here?
        self.styleEditor.editMarker()
        self.updateMarginGraphics()
        self.loadPolyglotSettings()
        self.enableTXLoption()
        self.onBodyHeightChanged(None)
        self.checkFontsMissing()
        self.clearEditableBuffers()
        logger.debug(f"Changed project to {prjid} {configName=}")
        self.builder.get_object("nbk_Main").set_current_page(0)
        self.changed(False)
        self.showmybook(True)

    def updateConfigIdentity(self, cfg):
        self.cfgid = cfg
        self.loadPolyglotSettings(cfg)

    def loadPolyglotSettings(self, config=None):
        if self.gtkpolyglot is not None:
            self.gtkpolyglot.clear_polyglot_treeview()
        if self.get("c_diglot"):
            if self.gtkpolyglot is None:
                self.gtkpolyglot = PolyglotSetup(self.builder, self, self.tv_polyglot)
                polyset = self.builder.get_object('bx_polyglot')
                polyset.pack_start(self.gtkpolyglot, True, True, 0)
                polyset.show_all()
            if config is not None:
                self.polyglots["L"].cfg = config
            self.gtkpolyglot.load_polyglots_into_treeview()
                

    def showmybook(self, isfirst=False):
        if self.otherDiglot is None and self.initialised and self.showPDFmode == "preview": # preview is on
            prvw = self.builder.get_object("dlg_preview")
            pdffile = os.path.join(self.project.printPath(None), self.getPDFname())
            logger.debug(f"Trying to show {pdffile} exists={os.path.exists(pdffile)}")
            if os.path.exists(pdffile):
                pdft = os.stat(pdffile).st_mtime
                cfgfile = os.path.join(self.project.srcPath(self.cfgid), "ptxprint.cfg")
                if not os.path.exists(cfgfile):
                    return
                cfgt = os.stat(cfgfile).st_mtime
                for bk in self.getBooks():
                    adj = self.get_adjlist(bk, gtk=Gtk)
                logger.debug(f"time({pdffile})={pdft}, time({cfgfile})={cfgt}")
                if pdft > cfgt:
                    if isfirst:
                        prvw.set_gravity(Gdk.Gravity.NORTH_EAST)
                    pdfname = self.baseTeXPDFnames()[0]
                    if len(pdfname):
                        plocname = os.path.join(self.project.printPath(self.cfgid), pdfname+".parlocs")
                        self.pdf_viewer.loadnshow(pdffile, rtl=self.rtl, parlocs=plocname, widget=prvw, page=1,
                                                    isdiglot=self.get("c_diglot"))
                        return
            self.pdf_viewer.clear(widget=prvw)

    def enableTXLoption(self):
        txlpath = os.path.join(self.project.path, "pluginData", "Transcelerator", "Transcelerator")
        w = "c_txlQuestionsInclude"
        if os.path.exists(txlpath):
            self.builder.get_object(w).set_sensitive(True)
        else:
            self.builder.get_object(w).set_sensitive(False)
            self.set(w, False, mod=False)

    def doConfigNameChange(self, w):
        lockBtn = self.builder.get_object("btn_lockunlock")
        isDefault = self.cfgid == "Default"
        lockBtn.set_sensitive(not isDefault)
        self.builder.get_object("btn_deleteConfig").set_visible(not isDefault)
        self.builder.get_object("btn_resetDefaults").set_visible(isDefault)
        if self.configNoUpdate or self.get("ecb_savedConfig") == "":
            return
        self.builder.get_object("t_invisiblePassword").set_text("")
        self.builder.get_object("btn_saveConfig").set_sensitive(True)
        self.builder.get_object("btn_deleteConfig").set_sensitive(True)
        configName = self.getConfigName()
        if self.gtkpolyglot is not None:
            self.gtkpolyglot.changeConfigName(configName)
        if len(self.get("ecb_savedConfig")):
            if configName != "Default":
                lockBtn.set_sensitive(True)
        else:
            # self.builder.get_object("t_configNotes").set_text("") # Why are we doing this? (it often wipes it out!)
            lockBtn.set_sensitive(False)
        cpath = self.project.srcPath(configName) if self.project is not None else None
        if cpath is not None and os.path.exists(cpath):
            self.updateProjectSettings(self.project.prjid, self.project.guid, saveCurrConfig=False, configName=configName, readConfig=True) # False means DON'T Save!
            self.updateDialogTitle()
        self.disableLayoutAnalysis()

    def onConfigNameChanged(self, btn, *a):
        if self.configKeypressed:
            self.configKeypressed = False
            return
        # self.doConfigNameChange(None)

    def onConfigKeyPressed(self, btn, *a):
        self.configKeypressed = True
        self.builder.get_object("btn_cfg_ok").set_sensitive(False) 
        msg = ""
        cfg = self.get("t_configName")
        cleanCfg = re.sub('[^-a-zA-Z0-9_()]+', '', cfg)
        cpath = self.project.srcPath(cleanCfg)
        if cfg != cleanCfg:
            msg = _("Do not use spaces or special characters")
        elif not len(cfg):
            pass
        elif cpath is not None and os.path.exists(cpath):
            msg = _("That Configuration already exists.\nUse another name.")
        else:
            self.builder.get_object("btn_cfg_ok").set_sensitive(True) 
        self.builder.get_object("l_configNameMsg").set_text(msg) 

    def onCfgFocusOutEvent(self, btn, *a):
        self.configKeypressed = False

    def onProjectNameChanged(self, btn, *a):
        if self.projectKeypressed:
            self.projectKeypressed = False
            return

    def onProjectKeyPressed(self, btn, *a):
        self.projectKeypressed = True
        self.builder.get_object("btn_dbl_ok").set_sensitive(False) 
        msg = ""
        prj = self.get("t_DBLprojName")
        cleanPrj = re.sub('[^-a-zA-Z0-9_()]+', '', prj)
        prjpath = os.path.join(self.prjTree.treedirs[0], cleanPrj)
        if prj != cleanPrj:
            msg = _("Do not use spaces or special characters")
        elif not len(prj):
            pass
        elif prjpath is not None and os.path.exists(prjpath):
            msg = _("That Project already exists.\nUse another name.")
        else:
            self.builder.get_object("btn_dbl_ok").set_sensitive(True) 
        self.builder.get_object("l_projectNameMsg").set_text(msg) 

    def onPrjFocusOutEvent(self, btn, *a):
        self.projectKeypressed = False

    # def onDBLprojNameChanged(self, widget):
        # text = self.get("t_DBLprojName")
        # btn = self.builder.get_object("btn_locateDBLbundle") #should have been btn_dbl_ok
        # lsp = self.builder.get_object("ls_projects")
        # allprojects = [x[0] for x in lsp]
        # btn.set_sensitive(not text in allprojects)

    def updateFonts(self):
        if self.ptsettings is None:
            return
        ptfont = self.get("bl_fontR", skipmissing=True)
        if ptfont is None:
            ptfont = FontRef(self.ptsettings.get("DefaultFont", "Arial"), "")
            self.set('bl_fontR', ptfont)
            self.onFontChanged(None)

    def disableLayoutAnalysis(self):
        self.set('c_layoutAnalysis', False)
        
    def updateDialogTitle(self):
        titleStr = super(GtkViewModel, self).getDialogTitle()
        #self.builder.get_object("ptxprint").set_title(titleStr)
        if self.mainapp.win:
            self.mainapp.win.set_title(titleStr)

    def _locFile(self, file2edit, loc, fallback=False):
        fpath = None
        if loc == "wrk":
            fpath = os.path.join(self.project.printPath(self.cfgid), file2edit)
        elif loc == "prj":
            fpath = os.path.join(self.project.path, file2edit)
        elif loc == "cfg":
            cfgname = self.cfgid
            fpath = os.path.join(self.project.srcPath(cfgname), file2edit)
        elif "\\" in loc or "/" in loc:
            fpath = os.path.join(loc, file2edit)
        return fpath

    def editFile(self, file2edit, loc="wrk", pgid="tb_Settings1", switch=None): # keep param order
        if switch is None:
            switch = pgid == "tb_Settings1"
        pgnum = self.notebooks["Viewer"].index(pgid)
        mpgnum = self.notebooks["Main"].index("tb_Viewer")
        fpath = self._locFile(file2edit, loc)
        if fpath is None:
            return
        label = self.builder.get_object("l_{1}".format(*pgid.split("_")))
        
        if switch:
            labels = [self.builder.get_object("l_Settings{}".format(i)) for i in range(1,4)]
            paths = [l.get_tooltip_text() for l in labels]
            for i, p in enumerate(paths):
                if fpath == p:
                    start = i
                    break
            else:
                # only shift if we are inserting a file not replacing
                for i in range(2, 0, -1):     # shift from right hand end
                    buf = self.fileViews[pgnum+i-1][0]
                    txt = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
                    self.fileViews[pgnum+i][0].set_text(txt)
                    labels[i].set_text(labels[i-1].get_text())
                    labels[i].set_tooltip_text(paths[i-1])
                start = 0
            pgnum += start
            label = labels[start]
            label.set_text(file2edit)

        label.set_tooltip_text(fpath)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as inf:
                txt = inf.read()
            self.fileViews[pgnum][0].set_text(txt)
            self.onViewerFocus(self.fileViews[pgnum][1], None)
        else:
            self.fileViews[pgnum][0].set_text(_("# This file doesn't exist yet!\n# Edit here and Click 'Save' to create it."))
        if switch:
            self.builder.get_object("nbk_Main").set_current_page(mpgnum)
            self.builder.get_object("nbk_Viewer").set_current_page(pgnum)

    def editFile_delayed(self, *a):
        GLib.idle_add(self.editFile, *a)

    def onViewerLostFocus(self, widget, event):
        pgnum = self.notebooks['Viewer'].index(widget.pageid)
        buf = self.fileViews[pgnum][0]
        t = buf.get_iter_at_mark(self.fileViews[pgnum][0].get_insert())
        self.cursors[pgnum] = (t.get_line(), t.get_line_offset())
        currentText = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        label = self.builder.get_object("l"+_allpgids[pgnum][2:])
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
        if pg in (1,):
            return
        buf = self.fileViews[pg][0]
        currentText = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        label = self.builder.get_object("l"+_allpgids[pg][2:])
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
        self.onRefreshViewerTextClicked(None)
        
    def onEditModule(self, btn):
        if self.moduleFile is not None:
            self._editProcFile(str(self.moduleFile), "prj")
            self.onRefreshViewerTextClicked(None)
            self.builder.get_object('l_Settings1').set_label(os.path.basename(self.moduleFile))
        
    def onEditModsTeX(self, btn):
        cfgname = self.cfgid
        self._editProcFile("ptxprint-mods.tex", "cfg",
            intro=_(_("""% This is the .tex file specific for the {} project used by PTXprint.
% Saved Configuration name: {}
""").format(self.project.prjid, cfgname)))
        self.onRefreshViewerTextClicked(None)

    def onEditPreModsTeX(self, btn):
        cfgname = self.cfgid
        self._editProcFile("ptxprint-premods.tex", "cfg",
            intro=_(_("""% This is the preprocessing .tex file specific for the {} project used by PTXprint.
% Saved Configuration name: {}
""").format(self.project.prjid, cfgname)))
        self.onRefreshViewerTextClicked(None)

    def onEditCustomSty(self, btn):
        self._editProcFile("custom.sty", "prj", intro="# This file is currently empty\n")
        self.onRefreshViewerTextClicked(None)

    def onEditModsSty(self, btn):
        self._editProcFile("ptxprint-mods.sty", "cfg", intro="# This file is currently empty\n")
        self.onRefreshViewerTextClicked(None)

    def onExtraFileClicked(self, btn):
        self.onSimpleClicked(btn)
        self.colorTabs()
        if btn.get_active():
            self.triggervcs = True
        self.onRefreshViewerTextClicked(None)

    def onChangesFileClicked(self, btn):
        self.onExtraFileClicked(btn)
        cfile = os.path.join(self.project.srcPath(self.cfgid), "changes.txt")
        logger.debug(f"in onChangesFileClicked: {self.loadingConfig=} {cfile=}")
        if not os.path.exists(cfile):
            try:
                with open(cfile, "w", encoding="utf-8") as outf:
                    outf.write(chgsHeader)
            except PermissionError:
                logger.debug(f"Cannot write file (Permission Error): {cfile}")
        self.onRefreshViewerTextClicked(None)

    def onMainBodyTextChanged(self, btn):
        self.sensiVisible("c_mainBodyText")

    def onSelectScriptClicked(self, btn_selectScript):
        customScript = self.fileChooser("Select a Custom Script file", 
                filters = {"Executable Scripts": {"patterns": ["*.bat", "*.exe", "*.py", "*.sh"] , "mime": "application/bat", "default": True},
                           "All Files": {"pattern": "*"}},
                           # "TECkit Mappings": {"pattern": ["*.map", "*.tec"]},
                           # "CC Tables": {"pattern": "*.cct"},
                multiple = False, basedir=self.project.printPath(self.cfgid))
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
        prjdir = self.project.path
        customXRfile = self.fileChooser("Select a Custom Cross-Reference file", 
                filters = {"Paratext XRF Files": {"patterns": "*.xrf" , "mime": "text/plain", "default": True},
                           "Extended XRF files": {"pattern": "*.xre"},
                           "XML Cross-Ref Files": {"pattern": "*.xml"},
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
        cfname = self.cfgid
        zfname = self.project.prjid+("-"+cfname if cfname else "")+"PTXprintArchive.zip"
        archiveZipFile = self.fileChooser(_("Select the location and name for the Archive file"),
                filters={"ZIP files": {"pattern": "*.zip", "mime": "application/zip"}},
                multiple=False, folder=False, save=True,
                basedir=os.path.join(self.project.printPath(self.cfgid), '..'), defaultSaveName=zfname)
        if archiveZipFile is not None:
            btn_createZipArchive.set_tooltip_text(str(archiveZipFile[0]))
            try:
                self.createArchive(str(archiveZipFile[0]))
                startfile(os.path.dirname(archiveZipFile[0]))
            except Exception as e:
                s = traceback.format_exc()
                s += "\n{}: {}".format(type(e), str(e))
                self.doError(s, copy2clip=True)
        else:
            self.doStatus(_("No Archive File Created"))

    def onSelectModuleClicked(self, btn):
        prjdir = self.project.path
        tgtfldr = os.path.join(prjdir, "Modules")
        if not os.path.exists(tgtfldr):
            tgtfldr = os.path.join(prjdir, "_Modules")
        moduleFile = self.fileChooser("Select a Paratext Module", 
                filters = {"Modules": {"patterns": ["*.sfm"] , "mime": "text/plain", "default": True},
                           "All Files": {"pattern": "*"}},
                multiple = False, basedir=tgtfldr)
        if moduleFile is not None:
            print(moduleFile)
            moduleFile = [Path(saferelpath(x, prjdir)) for x in moduleFile]
            self.moduleFile = moduleFile[0]
            print(self.moduleFile)
            self.builder.get_object("lb_bibleModule").set_label(os.path.basename(moduleFile[0]))
            self.builder.get_object("btn_chooseBibleModule").set_tooltip_text(str(moduleFile[0]))
            self.set("r_book", "module")

        else:
            self.builder.get_object("r_book_single").set_active(True)
            self.builder.get_object("lb_bibleModule").set_label("")
            self.moduleFile = None
            self.builder.get_object("btn_chooseBibleModule").set_tooltip_text("")
            self.set("r_book", "single")
        self.updateDialogTitle()
        self.disableLayoutAnalysis()

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
                self.picListView.onRadioChanged()
                
    def onSelectTargetFolderClicked(self, btn_tgtFolder):
        impTargetFolder = self.fileChooser(_("Select a folder to extract the settings into"),
                filters = None, multiple = False, folder = True)
        if impTargetFolder is not None:
            if len(impTargetFolder):
                self.impTargetFolder = impTargetFolder[0]
                self.set("lb_tgtFolder", str(impTargetFolder[0]))
            else:
                self.impTargetFolder = None
                self.set("lb_tgtFolder", "")
                self.builder.get_object("btn_tgtFolder").set_sensitive(False)
        self.setImportButtonOKsensitivity(None)

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
        # else: # Commented out as a result of #887
            # setattr(self, attr, None)
            # btn.set_tooltip_text("")
            # self.set("lb_"+ident, "")
            # if chkbx:
                # btn.set_sensitive(False)
                # self.set("c_"+ident, False)
                
    def onImportSegmentClicked(self, w):
        name = Gtk.Buildable.get_name(w)[2:]
        mpgnum = self.notebooks['Import'].index("tb_"+name)
        self.builder.get_object("nbk_Import").set_current_page(mpgnum)
        self.setImportButtonOKsensitivity(None)

    def setImportButtonOKsensitivity(self, w):
        status = (self.get('r_impSource') == 'pdf' and self.get('lb_impSource_pdf') == "") or \
                 (self.get('r_impTarget') == 'folder' and self.get('lb_tgtFolder') == "") or \
                 (self.get('r_impSource') == 'config' and ((self.get('fcb_impProject') is None or self.get('ecb_impConfig') is None) or \
                 (str(self.get('fcb_impProject')) == str(self.get("ecb_targetProject")) and \
                  str(self.get('ecb_impConfig'))  == str(self.get('ecb_targetConfig'))))) or \
                 (self.get('r_impTarget') == 'prjcfg' and (not len(self.get('ecb_targetProject')) or not len(self.get('ecb_targetConfig'))))
                 # (str(self.get('fcb_impProject')) == str(self.get("fcb_project")) and \
                 #  str(self.get('ecb_impConfig'))  == str(self.get('ecb_savedConfig'))) or \
        
        # Also turn on Everything setting under certain conditions:
        somethingON = False
        turnONall = (self.get('r_impTarget') == 'folder' and self.get('lb_tgtFolder') != "")
        if turnONall: # Or IF a new project/config combo is selected. MH please help FIX ME!
            self.set("c_impEverything", turnONall)
        for c in ['Pictures', 'Layout', 'FontsScript', 'Styles', 'Other', 'Everything']:
            somethingON = somethingON or self.get("c_imp"+c, False)
            self.builder.get_object("c_imp"+c).set_sensitive(not turnONall)
        
        # The Custom Script file is NOT stored in a PDF file, so don't offer importing it as an option
        fname = str(getattr(self, "impSourcePDF", None))
        cstmScr = self.builder.get_object("c_oth_customScript")
        csStat = self.get("r_impSource") == "pdf" and fname.endswith(".pdf")
        cstmScr.set_sensitive(not csStat)
        if csStat:
            cstmScr.set_active(False)

        self.builder.get_object("btn_importSettingsOK").set_sensitive(not status and somethingON)

    def _findProjectInArchive(self, zf):
        trials = [f for f in zf.namelist() if 'ptxprint.cfg' in f and 'shared' in f]
        respath = None
        if len(trials) > 1:
            for t in trials:
                with zf.open(t) as inf:
                    for l in inf.readlines():
                        s = l.decode("utf-8")
                        if s.lstrip().startswith("ifdiglot"):
                            if s.rstrip().endswith("True"):
                                # this is our answer
                                respath = t
                                break
        if respath is None:
            if len(trials) == 1:
                respath = trials[0]
            else:
                respath = None
        if respath is not None:
            res = os.path.dirname(respath)
        else:
            res = None
        return res

    def onImportClicked(self, btn_importPDF):
        dialog = self.builder.get_object("dlg_importSettings")
        self.setImportButtonOKsensitivity(None)
        self.set("ecb_targetProject", self.project.prjid)
        self.set("ecb_targetConfig", self.cfgid)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            zipinf = None
            prefix = None
            if self.get("r_impSource") == "pdf":
                fname = str(getattr(self, "impSourcePDF", None))
                if fname.endswith(".pdf") and os.path.exists(fname):
                    confstream = getPDFconfig(fname)
                    zipinf = BytesIO(confstream)
                    zipdata = ZipFile(zipinf, compression=ZIP_DEFLATED)
                elif os.path.exists(fname):
                    zipdata = ZipFile(fname)
                    # import pdb; pdb.set_trace()
                    prefix = self._findProjectInArchive(zipdata)
                else:
                    zipdata = None
            elif self.get("fcb_impProject"):
                impprj = self._getProject("fcb_impProject")
                dpath = os.path.join(impprj.srcPath(self.get("ecb_impConfig", "Default")))
                zipdata = UnzipDir(dpath)
            else:
                zipdata = None
            statMsg = None
            if zipdata is not None:
                if self.get("r_impTarget") == "folder":
                    outdir = str(getattr(self, "impTargetFolder", None))
                    if outdir is not None:
                        os.makedirs(outdir, exist_ok=True)
                        zipdata.extractall(outdir)
                        statMsg = _("Exported Settings to: {}").format(outdir)
                    else:
                        statMsg = _("Undefined target folder. Could not export settings!")
                else:
                    tp = self._getProject('ecb_targetProject')
                    tc = self.get('ecb_targetConfig',  None)
                    self.importConfig(zipdata, prefix=prefix, tgtPrj=tp, tgtCfg=tc)
                    if tp.prjid == self.project.prjid:
                        self.updateAllConfigLists()
                    statMsg = _("Imported Settings into: {}::{}").format(tp.prjid, tc)
                zipdata.close()
            if zipinf is not None:
                zipinf.close()
            if self.get("c_impPictures") or self.get("c_impEverything"):  # MH - FIX ME!
                self.updatePicList()
            self.onRefreshViewerTextClicked(None)
            if statMsg is not None:
                self.doStatus(statMsg)
        dialog.hide()

    def onResetCurrentConfigClicked(self, btn):
        self.resetToInitValues(updatebklist=False)

    def onSelectPDForZIPfileToImport(self, btn_importPDF):
        pdfORzipFile = self.fileChooser(_("Select a PDF (or ZIP archive) to import the settings from"),
                filters = {"PDF/ZIP files": {"patterns": ["*.pdf", "*.zip"], "mime": "application/pdf", "default": True}},
                multiple = False, basedir=os.path.join(self.project.printPath(self.cfgid), ".."))

        if pdfORzipFile == None or not len(pdfORzipFile) or str(pdfORzipFile[0]) == "None":
            self.set("r_impSource", "config")
            setattr(self, "impSourcePDF", None)
            btn_importPDF.set_tooltip_text("")
            self.set("lb_impSource_pdf", "")
            return

        zipdata = getPDFconfig(pdfORzipFile[0])
        if zipdata is None:
            self.doError(_("PDF/ZIP Import Config Error"), 
                    secondary=_("Cannot find any settings to import from the selected file.\n\n") + \
                            _("If importing from a PDF (created with PTXprint version 2.3 or later) check ") + \
                            _("if it was created with 'Include Config Settings Within PDF' option enabled."))
            return

        self.set("r_impSource", "pdf")
        setattr(self, "impSourcePDF", pdfORzipFile[0])
        btn_importPDF.set_tooltip_text(str(pdfORzipFile[0]))
        self.set("lb_impSource_pdf", pdfre.sub(r"\1", str(pdfORzipFile[0])))

        self.setImportButtonOKsensitivity(None)

    def onFrontPDFsClicked(self, btn_selectFrontPDFs):
        self._onPDFClicked(_("Select one or more PDF(s) for FRONT matter"), False, 
                self.project.path, "inclFrontMatter", "FrontPDFs", btn_selectFrontPDFs)

    def onBackPDFsClicked(self, btn_selectBackPDFs):
        self._onPDFClicked(_("Select one or more PDF(s) for BACK matter"), False, 
                self.project.path, "inclBackMatter", "BackPDFs", btn_selectBackPDFs)

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
                os.path.join(self.project.printPath(None)), "diffPDF", "diffPDF", btn_selectDiffPDF, False)
        if self.get("lb_diffPDF") == "":
            self.set("lb_diffPDF", _("Previous PDF (_1)"))
            self.makeLabelBold("l_selectDiffPDF", False)
        else:
            self.makeLabelBold("l_selectDiffPDF", True)

    def makeLabelBold(self, lbl, bold=True):
        lb = self.builder.get_object(lbl)
        ctxt = lb.get_style_context()
        if not bold:
            ctxt.remove_class("changed")
        else:
            ctxt.add_class("changed")

    def resetComparePDFfileToPrevious(self, btn, foo):
        self.makeLabelBold("l_selectDiffPDF", False)
        self.set("btn_selectDiffPDF", None)
        self.set("lb_diffPDF", _("Previous PDF (_1)"))

    def onEditAdjListClicked(self, btn_editParaAdjList):
        pgnum = 1
        mpgnum = self.notebooks["Main"].index("tb_Viewer")
        self.set("nbk_Main", mpgnum, mod=False)
        self.set("nbk_Viewer", pgnum, mod=False)
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
            self.loadPolyglotSettings()
            self.diglotViews['R'] = self.createDiglotView()
            self.set("c_doublecolumn", True)
            self.builder.get_object("c_doublecolumn").set_sensitive(False)
        else:
            self.builder.get_object("c_doublecolumn").set_sensitive(True)
            self.setPrintBtnStatus(2)
            self.diglotViews = {}
        self.updateDialogTitle()
        self.disableLayoutAnalysis()
        self.loadPics(mustLoad=False, force=True)
        if self.get("c_includeillustrations"):
            self.onUpdatePicCaptionsClicked(None)

    def switchToDiglot(self, pref):
        dv = self.diglotViews.get(pref, None)
        if dv is None:
            return False
        dv.saveConfig()
        dvprj = dv.project
        self.otherDiglot = (self.project, self.cfgid)
        # self.builder.get_object("b_print2ndDiglotText").set_visible(True)
        self.changeBtnLabel("b_print", _("Return to Primary"))
        self.builder.get_object("b_reprint").set_sensitive(False)
        self.set("fcb_project", dvprj.prjid)
        self.set("ecb_savedConfig", dv.cfgid)
        self.disableLayoutAnalysis()
        # self.updateProjectSettings(dvprj.prjid, dvprj.guid, configName=dv.cfgid)
        # self.updateDialogTitle()
        return True

    def changeBtnLabel(self, w, lbl):
        b = self.builder.get_object(w)
        b.set_visible(False)
        b.set_label(lbl)
        b.set_visible(True)
        
    def onimpProjectChanged(self, btn):
        self.set("r_impSource", "config")
        self.updateimpProjectConfigList()
        self.setImportButtonOKsensitivity(None)
        
    def onimpConfigChanged(self, btn):
        self.set("r_impSource", "config")
        self.setImportButtonOKsensitivity(None)
        
    def ontgtProjectChanged(self, btn):
        self.set("r_impTarget", "prjcfg")
        self.updatetgtProjectConfigList()
        self.setImportButtonOKsensitivity(None)
        
    def ontgtConfigChanged(self, btn):
        self.set("r_impTarget", "prjcfg")
        self.setImportButtonOKsensitivity(None)
        
    def onCoverFrontBackClicked(self, w):
        status = self.get("c_oth_FrontMatter") or self.get("c_oth_Cover")
        self.builder.get_object("c_oth_OverwriteFrtMatter").set_sensitive(status)
        if not status:
            self.set("c_oth_OverwriteFrtMatter", False)
        
    def onGenerateHyphenationListClicked(self, btn):
        scrsnpt = self.getScriptSnippet()
        # Show dialog with various options
        dialog = self.builder.get_object("dlg_createHyphenList")
        self.set("l_createHyphenList_booklist", " ".join(self.getBooks()))
        sylbrk = scrsnpt.isSyllableBreaking(self)
        if not sylbrk:
            self.set("c_addSyllableBasedHyphens", False)
        self.builder.get_object("c_addSyllableBasedHyphens").set_sensitive(sylbrk)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            prjdir = self.project.path
            self.hyphenation = Hyphenation.fromPTXFile(self, self.project.prjid, prjdir,
                                            inbooks=self.get("c_hyphenLimitBooks"),
                                            addsyls=self.get("c_addSyllableBasedHyphens"),
                                            strict=self.get("c_hyphenApprovedWords"),
                                            hyphen="\u2011" if self.get('c_nonBreakingHyphens') else "\u2010")
            self.doError(self.hyphenation.m1, secondary=self.hyphenation.m2)
        dialog.hide()

    def onHyphenateClicked(self, w1):
        w2 = "c_letterSpacing"
        if self.get(w2):
            self.set(w2, False)
            self.highlightwidget(w2)
            self.doStatus(_("The Between Letters Spacing Adjustments have been disabled due to Hyphenate being enabled."))

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
        response = dialog.run()
        dialog.destroy()
        return True if response == Gtk.ResponseType.YES else False

    def onOpenOutputFolderclicked(self, w):
        startfile(self.project.printPath(None))

    def onOpenFolderClicked(self, btn, *argv):
        p = re.search(r'(?<=href=\")[^<>]+(?=\")',btn.get_label())
        startfile(p[0])

    def finished(self, passed=True):
        GLib.idle_add(lambda: self._incrementProgress(val=0.))
        if not passed and self.showPDFmode == "preview":
            self.pdf_viewer.loadnshow(None)
        # TO DO: enable/disable the Permission Letter button

    def _incrementProgress(self, val=None):
        wid = self.builder.get_object("t_find")
        if val is None:
            val = wid.get_progress_fraction()
            val = 0.10 if val < 0.1 else (1. + 19 * val) / 20
        wid.set_progress_fraction(val)

    def incrementProgress(self, inproc=False, stage="pr", run=0):
        GLib.idle_add(self._incrementProgress)
        currMsg = self.builder.get_object("t_find").get_placeholder_text()
        if stage == 'lo' and run > 0:
            msg = _(f"Redoing layout {run}...")
        elif stage is None:
            msg = ""
        else:
            msg = _progress[stage]
        GLib.idle_add(lambda: self.builder.get_object("t_find").set_placeholder_text(msg))
        if inproc:
            self._incrementProgress()
            while (Gtk.events_pending()):
                Gtk.main_iteration_do(False)

    def onIdle(self, fn, *args):
        GLib.idle_add(fn, *args)

    def showLogFile(self):
        mpgnum = self.notebooks['Main'].index("tb_Viewer")
        self.builder.get_object("nbk_Main").set_current_page(mpgnum)
        vpgnum = self.notebooks['Viewer'].index("tb_XeTeXlog")
        self.builder.get_object("nbk_Viewer").set_current_page(vpgnum)

    def onBorderClicked(self, btn):
        if self.loadingConfig:
            return
        self.onSimpleClicked(btn)
        self.sensiVisible("c_useOrnaments")
        self.colorTabs()
        self.setPublishableTextBorder()

    def onOpenTextBorderDialog(self, btn):
        self.setPublishableTextBorder()
        self.styleEditor.sidebarBorderDialog()
        # mpgnum = self.notebooks['Main'].index("tb_TabsBorders")
        # self.builder.get_object("nbk_Main").set_current_page(mpgnum)

    def setPublishableTextBorder(self):
        x = "" if self.get("c_useOrnaments") and self.get("c_inclPageBorder") \
              and self.get("r_border_text") else "non"
        try:
            self.styleEditor.selectMarker("textborder")
            self.styleEditor.setval("textborder", "TextProperties", "{}publishable verse".format(x))
            self.set("c_styTextProperties", True if x == "non" else False)
        except KeyError:
            return
            
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
            self.builder.get_object("l_thumbVerticalL").set_visible(self.get("c_thumbrotate") and not self.get("c_tabsOddOnly"))
            self.builder.get_object("l_thumbVerticalR").set_visible(self.get("c_thumbrotate"))
            self.builder.get_object("l_thumbHorizontalL").set_visible(not self.get("c_thumbrotate") and not self.get("c_tabsOddOnly"))
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
        self.changed()

    def onRotateTabsChanged(self, *a):
        orientation = self.get("fcb_rotateTabs")
        self.builder.get_object("l_thumbVerticalL").set_angle(_vertical_thumb[orientation][0])
        self.builder.get_object("l_thumbVerticalR").set_angle(_vertical_thumb[orientation][1])

    def onPLsizeChanged(self, *a):
        self.onSizeChanged("pl")
        
    def onSBsizeChanged(self, *a):
        self.onSizeChanged("sb")
        
    def onSizeChanged(self, plsb):
        size = self.get("fcb_{}Size".format(plsb))
        wids = ["l_{}Horiz".format(plsb), "fcb_{}Horiz".format(plsb)]
        # if size in ["col", "span"]:
        self._updatePgPosOptions(size, plsb)
        if size == "span":
            for w in wids:
                self.builder.get_object("fcb_{}Horiz".format(plsb)).set_active_id("-")
                self.builder.get_object(w).set_sensitive(False)
        else:
            for w in wids:
                if size == "col":
                    self.builder.get_object("fcb_{}Horiz".format(plsb)).set_active_id("l")
                self.builder.get_object(w).set_sensitive(True)

    def onPLpgPosChanged(self, *a):
        self.onPgPosChanged("pl")
        
    def onSBpgPosChanged(self, *a):
        self.onPgPosChanged("sb")
        
    def onPgPosChanged(self, plsb):
        pgpos = self.get("fcb_{}PgPos".format(plsb))
        wids = ["l_{}OffsetNum".format(plsb), "s_{}Lines".format(plsb)]
        if pgpos in ["p", "c"]:
            for w in wids:
                self.builder.get_object(w).set_sensitive(True)
            if pgpos == "p":
                self.builder.get_object("l_{}OffsetNum".format(plsb)).set_label("Number of\nparagraphs:")
                self.set("s_{}Lines".format(plsb), int(float(self.get("s_{}Lines".format(plsb)))))
                self.builder.get_object("s_{}Lines".format(plsb)).set_digits(0)
                self.builder.get_object("s_{}Lines".format(plsb)).set_increments(1.00, 2)  # Climb rate 1.00, step increment 2
            else:
                self.builder.get_object("l_{}OffsetNum".format(plsb)).set_label("Number of\nlines:")
                self.builder.get_object("s_{}Lines".format(plsb)).set_digits(2)
                self.builder.get_object("s_{}Lines".format(plsb)).set_increments(0.10, 1)  # Climb rate 0.10, step increment 1
        else:
            for w in wids:
                self.builder.get_object(w).set_sensitive(False)
        self._updateHorizOptions(self.get("fcb_{}Size".format(plsb)), self.get("fcb_{}PgPos".format(plsb)), plsb)

    def _updatePgPosOptions(self, size, plsb):
        lsp = self.builder.get_object("ls_{}PgPos".format(plsb))
        fcb = self.builder.get_object("fcb_{}PgPos".format(plsb))
        lsp.clear()
        if size in ["page", "full"]:
            # Note: "Fill" is only applicable if in a Sidebar (but not in a normal picture)
            options = ["Top", "Center", "Bottom"] if plsb == 'pl' else ["Top", "Center", "Fill", "Bottom"]
            for posn in options:
                lsp.append([posn, "{}{}".format(size[:1].upper(), posn[:1].lower())])
            fcb.set_active(1)
        elif size == "span":
            for posn in ["Top", "Bottom", "Below Notes"]:
                lsp.append([posn, _pgpos[posn]])
            fcb.set_active(0)
        else: # size == "col"
            for posn in _pgpos.keys():
                if posn != "Below Notes":
                    lsp.append([posn, _pgpos[posn]])
            fcb.set_active(0)
        self._updateHorizOptions(size, self.get("fcb_{}PgPos".format(plsb)), plsb)
 
    def _updateHorizOptions(self, size, pgpos, plsb):
        lsp = self.builder.get_object("ls_{}Horiz".format(plsb))
        fcb = self.builder.get_object("fcb_{}Horiz".format(plsb))
        initVal = self.get("fcb_{}Horiz".format(plsb))
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
                self.set("fcb_{}Horiz".format(plsb), initVal)
            else:
                fcb.set_active(0)
 
    def onPLrowActivated(self, *a):
        self.set("nbk_PicList", 1)

    def onScrSettingsClicked(self, btn):
        script = self.get("fcb_script")
        gclass = getattr(scriptsnippets, script.lower(), None)
        if gclass is None or gclass.dialogstruct is None:
            return
        d = MiniDialog(self, gclass.dialogstruct, _(f"{script} Script Settings"))
        response = d.run()
        d.destroy()
        
    def onstyTextPropertiesClicked(self, btn):
        self.onSimpleClicked(btn)
        if self.styleEditor.marker == 'textborder':
            if 'publishable' in self.styleEditor.getval('textborder', 'TextProperties'):
                for w in ["c_useOrnaments", "c_inclPageBorder"]:
                    self.set(w, True)
                self.set("r_border", "text")
            else:
                self.set("c_inclPageBorder", False)

    def onFontStyclicked(self, btn):
        if self.getFontNameFace("bl_font_styFontName"): #, noStyles=True)
            self.styleEditor.item_changed(btn, "font")
        
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
        self.fillCopyrightDetails()

    def onCopyrightStatementChanged(self, btn):
        btname = Gtk.Buildable.get_name(btn)
        w = self.builder.get_object(btname)
        t = w.get_text()
        t = re.sub("</?p>", "", t)
        t = re.sub(r"\([cC]\)", "\u00a9 ", t)
        t = re.sub(r"\([rR]\)", "\u00ae ", t)
        t = re.sub(r"\([tT][mM]\)", "\u2122 ", t)
        if btname == 't_plCreditText' and len(t) == 3:
            if self.get('c_sensitive'):
                t = re.sub(r"(?i)dcc", "\u00a9 DCC", t)
            else:
                t = re.sub(r"(?i)dcc", "\u00a9 David C Cook", t)
        w.set_text(t)
        self.changed()
        
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
        try:
            mrkrset = self.get_usfms().get_markers(self.getBooks()) if btn.get_active() else set()
        except SyntaxError as e:
            self.doError(_("USFM syntax error"), secondary=_("Syntax error: {}").format(e))
            return
        mrkrset = set(sum((widen(x) for x in mrkrset), []))
        logger.debug(f"{self.getBooks()=}  {mrkrset=}")
        self.styleEditor.add_filter(btn.get_active(), mrkrset)

    def onEditMarkerChanged(self, mkrw):
        m = mkrw.get_text()
        t = self.get("t_styName")
        self.set("t_styName", re.sub(r"^.*?-", m+" -", t), mod=False)

    def onStyleDel(self, btn):
        self.styleEditor.delKey()

    def onStyleRefresh(self, btn):
        self.styleEditor.refreshKey()

    def onPlAddClicked(self, btn):
        picroot = self.project.path
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
                self.set(w, "", mod=False)
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
        a = re.sub(r'\\\+?[a-z0-9\-]+\*? ', '', a)
        self.set("t_plAnchor", a)

    def resetParam(self, btn, foo):
        label = Gtk.Buildable.get_name(btn.get_child())
        self.styleEditor.resetParam(label)
        self.changed()

    def resetLabel(self, btn, foo):
        lb = btn.get_child()
        ctxt = lb.get_style_context()
        if not ctxt.has_class("changed"):
            return
        label = Gtk.Buildable.get_name(lb)
        (pref, name) = label.split("_")
        ctrl = "s_"+name
        w = self.builder.get_object(ctrl)
        if not w.get_sensitive():
            return
        if ctrl in self.initValues:
            self.set(ctrl, self.initValues[ctrl])

    def changeLabel(self, ctrl, lb):
        if lb is None:
            (pref, name) = ctrl.split("_")
            lb = self.builder.get_object("l_"+name)
        if lb is None or ctrl not in self.initValues:
            return
        v = self.get(ctrl)
        logger.debug(f"{ctrl} changed to {v}, default is {self.initValues[ctrl]}")
        ctxt = lb.get_style_context()
        if v == self.initValues[ctrl]:
            ctxt.remove_class("changed")
        else:
            ctxt.add_class("changed")
        self.changed()

    def labelledChanged(self, widg, *a):
        ctrl = Gtk.Buildable.get_name(widg)
        logger.debug(f"{ctrl} changed")
        self.changeLabel(ctrl, None)

    def buttonChanged(self, widg, *a):
        ctrl = Gtk.Buildable.get_name(widg)
        lbl = widg.get_child()
        self.changeLabel(ctrl, lbl)

    def viewerValChanged(self, widg, *a):
        self.labelledChanged(widg, *a)
        if self.pdf_viewer is not None:
            self.pdf_viewer.settingsChanged()
            self.pdf_viewer.show_pdf()

    def adjustGridSettings(self, btn, foo):
        dialog = self.builder.get_object("dlg_gridSettings")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.showGridClicked(None)
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.hide()

    def onRefreshGridDefaults(self, btn):
        self.set("fcb_gridUnits", "cm")
        self.set("s_gridMinorDivisions", "5")
        self.set("fcb_gridOffset", "page")
        self.set("s_gridMajorThick", "0.2")
        self.set("col_gridMajor", "rgb(204,0,0)")
        self.set("s_gridMinorThick", "0.2")
        self.set("col_gridMinor", "rgb(98,160,234)")

    def onPLpageChanged(self, nbk_PicList, scrollObject, pgnum):
        page = 99
        if nbk_PicList is None:
            nbk_PicList = self.builder.get_object("nbk_PicList")
        if pgnum == -1:
            pgnum = nbk_PicList.get_current_page()
        page = nbk_PicList.get_nth_page(pgnum)
        pgid = Gtk.Buildable.get_name(page).split('_')[-1]
        filterSensitive = True if pgid == "checklist" else False
        # self.builder.get_object("bx_activeRefresh").set_visible(False)
        self.builder.get_object("fr_plChecklistFilter").set_sensitive(filterSensitive)
        self.builder.get_object("fr_plChecklistFilter").set_visible(filterSensitive)
        self.builder.get_object("gr_picButtons").set_visible(not filterSensitive)
        # self.builder.get_object("bx_activeRefresh").set_visible(True)
        for w in _allcols:
            if w in _selcols[pgid]:
                self.builder.get_object("col_{}".format(w)).set_visible(True)
            else:
                self.builder.get_object("col_{}".format(w)).set_visible(False)

    def _expandDBLBundle(self, prj, dblfile):
        tdir = self.prjTree.findWriteable()
        if UnpackBundle(dblfile, prj, tdir):
            self._selectProject(prj, tdir)
        else:
            self.doError("Faulty Scripture Text Bundle", "Check if you have selected a valid scripture text bundle (ZIP) file.")

    def _selectProject(self, prj, tdir):
        pjct = self.prjTree.addProject(prj, os.path.join(tdir, prj), None)
        v = [getattr(pjct, a) for a in ['prjid', 'guid']]
        extras = [Pango.Weight.NORMAL, "#000000"]
        # add prj to ls_project before selecting it.
        for a in ("ls_projects", "ls_digprojects", "ls_strongsfallbackprojects"):
            lsp = self.builder.get_object(a)
            allprojects = [x[0] for x in lsp]
            for i, p in enumerate(allprojects):
                if prj.casefold() > p.casefold():
                    lsp.insert(i, v + (extras if a == "ls_projects" else []))
                    break
            else:
                lsp.append(v + (extras if a == "ls_projects" else []))
        ui = self.uilevel
        self.resetToInitValues()
        self.set("fcb_project", prj)
        self.set_uiChangeLevel(ui)

    def onDBLbundleClicked(self, btn):
        dialog = self.builder.get_object("dlg_DBLbundle")
        response = dialog.run()
        dialog.hide()
        if response == Gtk.ResponseType.OK and self.builder.get_object("btn_locateDBLbundle").get_sensitive:
            prj = self.get("t_DBLprojName")
            if prj != "":
                self._expandDBLBundle(prj, self.DBLfile)

    def onImageSetClicked(self, btn):
        dialog = self.builder.get_object("dlg_getImageSet")
        response = dialog.run()
        dialog.hide()
        if response == Gtk.ResponseType.OK:
            if self.get("c_downloadImages"):
                imgset = "ccsampleimages.zip" # this will eventually be a variable, or even a list of img sets to download.
                self.doStatus(_("Downloading Image Set: '{}'   Please wait...".format(imgset)))
                while Gtk.events_pending():
                    Gtk.main_iteration()
                try:
                    urlfile = urllib.request.urlopen(r"https://software.sil.org/downloads/r/ptxprint/{}".format(imgset))
                    tzdir = extraDataDir("imagesets", "../zips", create=True)
                    zfile = os.path.join(tzdir, imgset)
                    with open(zfile, 'wb') as f:
                        f.write(urlfile.read())
                except urllib.error.URLError:
                    self.doStatus(_("ERROR: Downloading Image Set failed. Check internet connection and try again."))
                    while Gtk.events_pending():
                        Gtk.main_iteration()
                    return
                self.onHideStatusMsgClicked(None)
            else:
                zfile = self.get("btn_locateImageSet")
            imgsetname = unpackImageset(zfile, self.project.path)
            if imgsetname is not None and imgsetname != "":
                uddir = extraDataDir("imagesets", imgsetname, create=False)
                if not self.displayReadmeFile(imgsetname, uddir):
                    # remove the unpacked imageset!
                    try:
                        if len(uddir):
                            rmtree(uddir)
                            self.doStatus(_("Image Set '{}' removed due to not agreeing to terms and conditions of use.".format(imgsetname)))
                        return
                    except OSError:
                        self.doStatus(_("Cannot delete folder from disk! Image Set: {}".format(imgsetname)))
                else:
                    # add imgsetname to ecb_artPictureSet before selecting it.
                    lsp = self.builder.get_object("ecb_artPictureSet")
                    allimgsets = [x[0] for x in lsp.get_model()]
                    # Check if imgsetname is already in the list (case insensitive)
                    if imgsetname.casefold() not in [p.casefold() for p in allimgsets]:
                        for i, p in enumerate(allimgsets):
                            if imgsetname.casefold() > p.casefold():
                                lsp.insert_text(i, imgsetname)
                                break
                            else:
                                lsp.append_text(imgsetname)
                    self.set("ecb_artPictureSet", imgsetname, mod=False)
                    self.doStatus(_("Installed the downloaded Image Set: {}".format(imgsetname)))
                    self.onGetPicturesClicked(None)
            elif imgsetname == "":
                f = os.path.join(self.project.path, "local","figures")
                self.doStatus(_("Unzipped images to {}".format(f)))
                pass
            else:
                if self.get("c_downloadImages"):
                    self.doError("Failed Image Set", secondary="The Image Set failed to download and/or install.")
                else:
                    self.doError("Faulty Image Set", secondary="Please check that you have selected a valid Image Set (ZIP) file.")

    def displayReadmeFile(self, imgsetname, uddir):
        readme_path = os.path.join(uddir ,"readme.txt")
        try:
            with open(readme_path, 'r') as f:
                readme_content = f.read()
        except FileNotFoundError: # ?Why don't we assume that if there is no readme.txt file, that the images are free to use?
            self.doError("Error: readme.txt not found.", secondary=f"The file containing the terms and conditions of use for these images could not be located. Therefore the '{imgsetname}' image set will be deleted.")
            return False # ?Should we invert this behaviour?

        dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL,
            Gtk.MessageType.INFO, Gtk.ButtonsType.YES_NO, "readme")
        dialog.set_default_size(400, 300)
        dialog.set_title("Do you agree to the terms and conditions of use?")
        dialog.set_property("text", f"\nImage Set: {imgsetname}\n\n" + readme_content)
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            return True
        else:
            return False

    def onLocateDBLbundleClicked(self, btn):
        DBLfile = self.fileChooser("Select a DBL Bundle file", 
                filters = {"DBL Bundles": {"patterns": ["*.zip"] , "mime": "text/plain", "default": True},
                           "All Files": {"pattern": "*"}},
                multiple = False, basedir=os.path.join(self.prjTree.treedirs[0], "Bundles"))
        if DBLfile is not None:
            # DBLfile = [x.relative_to(prjdir) for x in DBLfile]
            self.DBLfile = DBLfile[0]
            self.builder.get_object("lb_DBLbundleFilename").set_label(os.path.basename(DBLfile[0]))
            dblname = GetDBLName(self.DBLfile)
            while True:
                pdir = self.prjTree.findProject(dblname)
                if pdir is None:
                    break
                if dblname[-1].isdigit():
                    dblname = dblname[:-1] + str(int(dblname[-1]) + 1)
                else:
                    dblname += "1"
            self.set("t_DBLprojName", dblname, mod=False)
            self.builder.get_object("btn_locateDBLbundle").set_tooltip_text(str(DBLfile[0]))
        else:
            self.builder.get_object("lb_DBLbundleFilename").set_label("")
            self.set("t_DBLprojName", "", mod=False)
            self.DBLfile = None
            self.builder.get_object("btn_locateDBLbundle").set_tooltip_text("")
    
    def onLocateImageSetClicked(self, btn):
        imgsetfile = self.fileChooser("Select an Image Set file", 
                filters = {"Image Sets": {"patterns": ["*.zip"] , "mime": "text/plain", "default": True},
                           "All Files": {"pattern": "*"}},
                multiple = False, basedir=os.path.join(self.project.path, "Bundles"))
        if imgsetfile is not None:
            # imgsetfile = [x.relative_to(prjdir) for x in imgsetfile]
            self.imgsetfile = imgsetfile[0]
            self.builder.get_object("lb_imageSetFilename").set_label(os.path.basename(imgsetfile[0]))
            self.builder.get_object("btn_locateImageSet").set_tooltip_text(str(imgsetfile[0]))
        else:
            self.builder.get_object("lb_imageSetFilename").set_label("")
            self.imgsetfile = None
            self.builder.get_object("btn_locateImageSet").set_tooltip_text("")
    
    def onParagraphednotesClicked(self, btn):
        status = not (self.get("c_fneachnewline") and self.get("c_xreachnewline"))
        for w in ["l_paragraphedNotes", "s_notespacingmin", "s_notespacingmax", "l_min", "l_max"]:
            wid = self.builder.get_object(w)
            if wid is not None:
                wid.set_sensitive(status)

    def changeInterfaceLang(self, mnu, lang):
        if lang == self.lang:
            return
        try:
            setup_i18n(lang)
        except locale.Error:
            self.doError(_("Unsupported Locale"),
                         secondary=_("This locale is not supported on your system, you may need to install it"))
            return
        self.lang = lang
        self.builder.get_object("ptxprint").destroy()
        self.builder.get_object("dlg_preview").destroy()
        self.onDestroy(None)
        print("Calling i18nize from changeInterfaceLang")
        self.i18nizeURIs()
            
    def onRHruleClicked(self, btn):
        status = self.get("c_rhrule")
        self.updateMarginGraphics()
        for w in ["l_rhruleposition", "s_rhruleposition"]:
            self.builder.get_object(w).set_sensitive(status)

    def onBodyHeightChanged(self, btn):
        textheight, linespacing = self.calcBodyHeight()
        lines = textheight / linespacing
        self.set("l_linesOnPage", "{:.1f}".format(lines))
        self.colorLinesOnPage()
        
    def colorLinesOnPage(self):
        lines = float(self.get("l_linesOnPage"))
        lb = self.builder.get_object("l_linesOnPage")
        ctxt = lb.get_style_context()
        if int(lines * 20) == int(lines) * 20:
            self.setMagicAdjustSensitive(False)
            ctxt.add_class("blue-label")
            ctxt.remove_class("red-label")
        else:
            self.setMagicAdjustSensitive(True)
            ctxt.add_class("red-label")
            ctxt.remove_class("blue-label")

    def onMagicAdjustClicked(self, btn):
        param = Gtk.Buildable.get_name(btn).split("_")[-1]
        textheight, linespacing = self.calcBodyHeight()
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
            
    def setMagicAdjustSensitive(self, clickable=False):
        btns = ["spacing", "top", "bottom"]
        for w in btns:
            self.builder.get_object("btn_adjust_{}".format(w)).set_sensitive(clickable)
    
    def updateMarginGraphics(self):
        self.setOneTwoColumnLabel()
        for tb in ["top", "bot", "nibot"]:
            self.builder.get_object("img_{}grid".format(tb)).set_visible(False)
            self.builder.get_object("img_{}vrule".format(tb)).set_visible(False)
            for c in ["1", "2"]:
                self.builder.get_object("img_{}{}col".format(tb,c)).set_visible(False)
        self.showColouredArrows(True)

        cols = 2 if self.get("c_doublecolumn") else 1
        vert = self.get("c_verticalrule") and self.get("c_doublecolumn")
        horiz = self.get("c_rhrule")
        ni = "ni" if self.get("c_noinkinmargin") else ""
        
        for tb in ["top", ni+"bot"]:
            self.builder.get_object("img_{}grid".format(tb)).set_visible(True)
            self.builder.get_object("img_{}{}col".format(tb,cols)).set_visible(True)
            self.builder.get_object("img_{}vrule".format(tb)).set_visible(vert)
        self.builder.get_object("img_tophrule".format(tb)).set_visible(horiz)

    def onOverlayCreditClicked(self, btn):
        dialog = self.builder.get_object("dlg_overlayCredit")
        crParams = self.get("t_piccreditbox")
        crParams = "bl,0,None" if not len(crParams) else crParams
        m = re.match(r"^([tcb]?)([lrc]?),(-?9?0?|None),(\w*)", crParams)
        if m:
            self.set("fcb_plCreditVpos", m[1], mod=False)
            self.set("fcb_plCreditHpos", m[2], mod=False)
            self.set("fcb_plCreditRotate", m[3], mod=False)
            self.set("ecb_plCreditBoxStyle", m[4], mod=False)
        self.set("t_plCreditText", self.get("l_piccredit") if len(self.get("l_piccredit")) else "", mod=False)
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
                srcs = set(v.get('src', None) for v in self.picinfos.get_pics())
                self.picChecksView.setMultiCreditOverlays(srcs, text, crParams, self.get("t_plFilename"))
        elif response == Gtk.ResponseType.CANCEL:
            pass
        else:
            return
        dialog.hide()

    def onSBpositionClicked(self, btn):
        reswid = "t_mapPgPos" if btn == self.builder.get_object("btn_mapSizePosition") else "t_sbPgPos"
        dialog = self.builder.get_object("dlg_sbPosition")
        sbParams = self.get(reswid)
        sbParams = "t" if not len(sbParams) else sbParams
        sbParams = re.sub(r'^([PF])([lcrio])([tcbf])', r'\1\3\2', sbParams)
        m = re.match(r"^([PF]?)([tcbf])([lrcio]?)([\d\.\-]*)", sbParams)
        if m:
            try:
                self.set("fcb_sbSize", _fullpage[m[1]])
            except KeyError:
                self.set("fcb_sbSize", m[1], mod=False)
            frSize = self.get("fcb_sbSize")
            self.set("fcb_sbPgPos", m[2], mod=False)
            self.set("fcb_sbHoriz", m[3], mod=False)
            self.set("s_sbLines", m[4], mod=False)
        self.updatePosnPreview()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.set(reswid, self.get("l_sbPosition"))
        elif response == Gtk.ResponseType.CANCEL:
            pass
        else:
            return
        dialog.hide()

    def _getLines(self):
        w = "s_sbLines"
        lines = ""
        v = self.get(w, "0.0") 
        if self.builder.get_object(w).get_sensitive():
            lines = v if float(v) != 0.0 else ""
        return lines
                
    def updatePosnPreview(self, *a):
        cols = 2 if self.get("c_doublecolumn") else 1
        frSize = self.get("fcb_sbSize")
        hpos = self.get("fcb_sbHoriz")
        if hpos is None:
            return
        hpos = "" if hpos == "-" else hpos
        pgposLocn = self.get("fcb_sbPgPos", "c") + hpos + self._getLines()
        pgposLocn = re.sub(r'([PF])([tcbf])([lcrio])', r'\1\3\2', pgposLocn)
        self.set("l_sbPosition", pgposLocn)
        locKey = getLocnKey(cols, frSize, pgposLocn)
        pixbuf = dispLocPreview(locKey)
        pic = self.builder.get_object("img_sbPreview")
        if pixbuf is None:
            pic.clear()
        else:
            pic.set_from_pixbuf(pixbuf)

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
        xdvname = os.path.join(self.project.printPath(self.cfgid), self.baseTeXPDFnames()[0] + ".xdv")
        def score(x):
            self.gtkpolyglot.set_fraction(x)
            runjob = self.callback(self, maxruns=1, noview=True)
            while runjob.thread.is_alive():
                Gtk.main_iteration_do(False)
            runres = runjob.res
            return 20000 if runres else xdvigetpages(xdvname)
        mid = self.gtkpolyglot.get_fraction()
        res = brent(0., 1., mid, score, 0.001)
        self.gtkpolyglot.set_fraction(res)
        self.isDiglotMeasuring = False
        self.callback(self)
        btn.set_active(False)

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
                fpath = os.path.join(self.project.path, self.getBookFilename(bkid))
                startfile(fpath)
        dialog.hide()
        
    def onGenerateCoverClicked(self, btn):
        metadata = {"langiso":       "<Ethnologue code>", 
                    "languagename":  "<Language>", 
                    "maintitle":     "<Title>", 
                    "subtitle" :     "<Subtitle>", 
                    "isbn":          ""}
    
        dialog = self.builder.get_object("dlg_generateCover")
        for a in (('front', True), ('whole', False)):
            img = self.styleEditor.getval(f'cat:cover{a[0]}|esb', 'BgImage', '')
            scl = self.styleEditor.getval(f'cat:cover{a[0]}|esb', 'BgImageScaleTo', '')
            if img:
                self.set("btn_coverSelectImage", img, mod=False)
                self.set("lb_coverImageFilename", img, mod=False)
                self.set("c_coverImageFront", a[1], mod=False)
                self.set("fcb_coverImageSize", self.styleEditor.getval(f'cat:cover{a[0]}|esb', 'BgImageScaleTo ', scl), mod=False)
                break
        if self.styleEditor.getval('cat:coverfront|esb', 'Border', '') == 'All':
            ornaments = self.styleEditor.getval('cat:coverfront|esb', 'BorderRef', '')
            self.set('fcb_coverBorder', ornaments, mod=False)
            bc = textocol(self.styleEditor.getval('cat:coverfront|esb', 'BorderColor', 'xFFFFFF'))
            self.set('col_coverBorder', bc, mod=False)
            self.set('c_coverBorder', True, mod=False)
        else:
            self.set('c_coverBorder', False, mod=False)
        fgc = textocol(self.styleEditor.getval('cat:coverwhole|esb', 'BgColor', 'xFFFFFF'))
        self.set('col_coverShading', fgc, mod=False)
        self.set('c_coverShading', fgc != "rgb(255,255,255)", mod=False)
        mtsize = float(self.styleEditor.getval('mt1', 'FontSize', 1))
        # breakpoint()
        fsize = float(self.styleEditor.getval('cat:coverfront|mt1', 'FontSize', 1))
        logger.debug(f"{mtsize=} {fsize=}")
        self.set('s_coverTextScale', fsize / mtsize, mod=False)
        self.set('col_coverText', textocol(self.styleEditor.getval('cat:coverfront|mt1', 'Color', 'x000000')), mod=False)
        
        # if Front Matter contains one or more cover periphs, then turn OFF the auto-overwrite,
        # but if there are no \periphs relating to the cover, then turn it ON and disable control.
        coverPeriphs = ['coverfront', 'coverspine', 'coverback', 'coverwhole']
        lt = _(" \\periphs in Front Matter")
        hasCoverPeriphs = self.isPeriphInFrontMatter(periphnames=coverPeriphs)
        w = self.builder.get_object("c_coverOverwritePeriphs")
        w.set_sensitive(True if hasCoverPeriphs else False)
        w.set_label(_("Overwrite")+lt if hasCoverPeriphs else _("Create")+lt)
        self.set('c_coverOverwritePeriphs', False if hasCoverPeriphs else True, mod=False)
        response = dialog.run()

        if response == Gtk.ResponseType.CANCEL:
            dialog.hide()
            return
        elif response == Gtk.ResponseType.OK: # Create Cover Settings clicked
            # Enable ESBs
            self.set("c_sidebars", True)
            # Scale the font size of mt1 and mt2 for front and spine
            scaleText = float(self.get('s_coverTextScale'))
            # Set foreground (text) color
            fg = coltotex(self.get('col_coverText'))
            for m in ['mt1', 'mt2']:
                sz = float(self.styleEditor.getval(m, 'FontSize', 1.0))
                for cvr in ['front', 'spine']:
                    sf = 1 if cvr == 'front' else 0.65
                    self.styleEditor.setval(f'cat:cover{cvr}|{m}', 'FontSize', sz*scaleText*sf, mapin=False)
                    self.styleEditor.setval(f'cat:cover{cvr}|{m}', 'Color', fg)

            if self.get('c_coverBorder'):
                # Set border colour
                bc = coltotex(self.get('col_coverBorder'))
                self.set("c_useOrnaments", True)
                ornaments = self.get('fcb_coverBorder')
                self.styleEditor.setval('cat:coverfront|esb', 'BorderStyle', 'ornaments')
                self.styleEditor.setval('cat:coverfront|esb', 'BorderRef', ornaments)
                self.styleEditor.setval('cat:coverfront|esb', 'BorderColor', bc)
                self.styleEditor.setval('cat:coverfront|esb', 'Border', 'All')
            else:
                self.styleEditor.setval('cat:coverfront|esb', 'BorderStyle', '')
                self.styleEditor.setval('cat:coverfront|esb', 'BorderRef', '')
                self.styleEditor.setval('cat:coverfront|esb', 'BorderColor', '')
                self.styleEditor.setval('cat:coverfront|esb', 'Border', 'None')

            # Set background color
            if self.get('c_coverShading'):
                s = self.get('s_coverShadingAlpha')
                self.styleEditor.setval('cat:coverwhole|esb', 'BgColor', coltotex(self.get('col_coverShading')))
                self.styleEditor.setval('cat:coverwhole|esb', 'Alpha', s)
            else:
                self.styleEditor.setval('cat:coverwhole|esb', 'BgColor', '1 1 1')
                self.styleEditor.setval('cat:coverwhole|esb', 'Alpha', '0.001')
                
            for c in ['front', 'whole']:
                for p in ['BgImage', 'BgImageScale', 'BgImageScaleTo', 'BgImageAlpha']:
                    self.styleEditor.setval(f'cat:cover{c}|esb', p, None)
            if self.get('c_coverSelectImage'):
                img = self.get('lb_coverImageFilename')
                scaleto = self.get('fcb_coverImageSize')
                self.styleEditor.setval('cat:coverfront|esb' if self.get('c_coverImageFront') else 'cat:coverwhole|esb', 'BgImage', img.strip('"'))
                self.styleEditor.setval('cat:coverfront|esb' if self.get('c_coverImageFront') else 'cat:coverwhole|esb', 'BgImageScale', '1x1')
                self.styleEditor.setval('cat:coverfront|esb' if self.get('c_coverImageFront') else 'cat:coverwhole|esb', 'BgImageScaleTo', scaleto)

            if self.get('c_coverSelectImage'):
                i = self.get('s_coverImageAlpha')
                invi = 1.001 - float(i)
                frnt = self.get('c_coverImageFront')
                self.styleEditor.setval('cat:coverfront|esb' if frnt else 'cat:coverwhole|esb', 'BgImageAlpha', i)
                self.styleEditor.setval('cat:coverwhole|esb' if frnt else 'cat:coverfront|esb', 'BgImageAlpha', invi)
                # if not frnt:
                    # self.styleEditor.setval('cat:coverback|esb', 'Alpha', 0.001)
                    # self.styleEditor.setval('cat:coverspine|esb', 'Alpha', 0.001)
                # else:
                    # self.styleEditor.setval('cat:coverback|esb', 'Alpha', 1)
                    # self.styleEditor.setval('cat:coverspine|esb', 'Alpha', 1)

            if self.get('c_coverOverwritePeriphs'):
                self.createCoverPeriphs(noDiglot = r'\zglot|\*' if len(self.diglotViews) else "")
            self.set("c_frontmatter", True)

            dialog.hide()

            if not self.get('c_coverOverwritePeriphs'):
                return
            # See if any of the meta-data fields are missing in the zvars, and if so
            # add them and ask the user to fill them in.
            if not self.warnedMissingZvars:
                missing = False
                for k, v in metadata.items():
                    if self.getvar(k, default=None) is None:
                        missing = True
                        self.setvar(k, v)
                if missing:
                    mpgnum = self.notebooks['Main'].index("tb_Peripherals")
                    self.builder.get_object("nbk_Main").set_current_page(mpgnum)
                    _errText = _("Please fill in any missing <Values> on") + "\n" + \
                               _("the Peripherals tab before proceeding.") + "\n" + \
                               _("Update the ISBN number or delete the entry.")
                    self.doError("Missing details for cover page", secondary=_errText, \
                              title="PTXprint", copy2clip=False, show=True)
                    self.warnedMissingZvars = True
                    return
            # Switch briefly to the Front Matter tab so that the updated content is activated and
            # gets saved/updated. But then switch back to the Cover tab immediately after so the 
            # view is back to where they clicked on the Generate Cover button to begin with.
            mpgnum = self.notebooks['Main'].index("tb_Viewer")
            self.builder.get_object("nbk_Main").set_current_page(mpgnum)
            self.builder.get_object("nbk_Viewer").set_current_page(0)
            mpgnum = self.notebooks['Main'].index("tb_Cover")
            self.builder.get_object("nbk_Main").set_current_page(mpgnum)

    def createCoverPeriphs(self, **kw):
        self.periphs['coverfront'] = r'''
{noDiglot}
\periph front|id="coverfront"
\zgap|30pt\*
\mt1 \zvar|maintitle\*
\mt2 \zvar|subtitle\*
\vfill
\endgraf'''.format(**kw)
        self.periphs['coverspine'] = r'''
{noDiglot}
\periph spine|id="coverspine"
\mt2 \zvar|maintitle\* ~~-~~ \zvar|subtitle\*
\p'''.format(**kw)
        self.periphs['coverback'] = r'''
{noDiglot}
\periph back|id="coverback"
\zgap|1in\*
\pc ~
\vfill
\zifvarset|var="isbn" emptyok="F"\*
\ztruetext
\esb \cat ISBNbox\cat* \pc \zISBNbarcode|var="isbn" height="medium"\* \esbe
\zgap|10pt\*
\ztruetext*'''.format(**kw)
        self.periphs['coverwhole'] = r'''
{noDiglot}
\periph spannedCover|id="coverwhole"
\zgap|1pt\*
\vfill
\pc ~
\vfill
\endgraf'''.format(**kw)
        self.updateFrontMatter()
        self.onLocalFRTclicked(None)

    def onInterlinearClicked(self, btn):
        if self.sensiVisible("c_interlinear"):
            if self.get("c_letterSpacing"):
                self.set("c_letterSpacing", False)
                self.doError(_("FYI: This Interlinear option is not compatible with the\n" +\
                               "'Spacing Adjustments Between Letters' on the Fonts+Script page.\n" +\
                               "So that option has just been disabled."))
        self.changed()

    def _checkUpdate(self, wid, file_age_seconds, background):
        version = None
        try:
            logger.debug(f"Trying to access URL to see if updates are available")
            with urllib.request.urlopen("https://software.sil.org/downloads/r/ptxprint/latest.win.json") as inf:
                info = json.load(inf)
                version = info.get('version')
        except (OSError, KeyError, ValueError) as e:
            logger.debug(f"Update check failed: {e}")
            return # Exit silently on any error

        # version = "3.0.0" # useful for testing - set a hypothetical (new) version number
        if version is None:
            logger.debug(f"Returning because version is None.")
            return

        newv_str = version.split('.')
        currv_str = VersionStr.split('.')
        
        # Ensure version lists are of equal length for safe comparison by padding with 0
        max_len = max(len(newv_str), len(currv_str))
        newv = [int(x) for x in newv_str] + [0] * (max_len - len(newv_str))
        currv = [int(x) for x in currv_str] + [0] * (max_len - len(currv_str))

        logger.debug(f"Available version: {newv}, Current version: {currv}")

        # Determine update severity if a new version is available
        severity_color = None
        # file_age_seconds = 190 * 24 * 3600 # 36000 # useful for testing - set a hypothetical age of the executable
        if newv > currv:
            already2monthsOld = file_age_seconds > 60 * 24 * 3600 
            already6monthsOld = file_age_seconds > 180 * 24 * 3600 

            # Default to blue for any update
            severity_color = "blue" # Patch version change (e.g., 2.8.15 -> 2.8.17)
            if newv[0] == currv[0] and newv[1] == currv[1]:
                extraMsg = _("FYI: Minor patch version change.")
            else:
                extraMsg = _("Recent major version change.")

            # Promote to orange for a minor version change
            if newv[0] == currv[0] and newv[1] > currv[1] or (already2monthsOld and not already6monthsOld):
                severity_color = "orange" # Minor version change (e.g., 2.7.x -> 2.8.x)
                extraMsg = _("You are using an outdated version!")
                if already2monthsOld:
                    logger.debug(f"Update is ORANGE because installation is 2+ months old.")
                    
            # Promote to red for a major version change > 2 months ago OR if the app is > 6 months old
            elif (newv[0] > currv[0] and already2monthsOld) or already6monthsOld:
                severity_color = "red" # Major version change (e.g., 1.x -> 2.x) or very old
                extraMsg = _("WARNING: This is a very old version!")
                if already6monthsOld:
                    logger.debug(f"Update is RED because installation is very old.")

        def enabledownload(extraMsg):
            tip = _("A newer version of PTXprint ({}) is available.\nClick to visit download page on the website.").format(version)
            wid.set_tooltip_text(f"{extraMsg}\n{tip}")

            # Apply color via CSS classes
            style_context = wid.get_style_context()
            # First, remove any existing color classes to reset the state
            style_context.remove_class("update-blue")
            style_context.remove_class("update-orange")
            style_context.remove_class("update-red")
            
            # Add the class for the current severity
            if severity_color:
                style_context.add_class(f"update-{severity_color}")
                logger.debug(f"Setting update icon color to {severity_color}")

            wid.set_visible(True)
            self.thread = None

        def disabledownload():
            wid.set_visible(False)
            self.thread = None

        # Schedule the UI update on the main GTK thread
        if severity_color:
            GLib.idle_add(enabledownload, extraMsg)
        else:
            GLib.idle_add(disabledownload)

    def checkUpdates(self):
        wid = self.builder.get_object("btn_download_update")
        lastchecked = self.userconfig.getfloat("init", "checkedupdate", fallback=0)
        if time.time() - self.startedtime < 300: # i.e. started less than 5 mins ago
            logger.debug("Check for updates didn't run as it hasn't been 5 mins since startup")
            # pass - enable for testing
            return
        elif lastchecked != 0 and time.time() - lastchecked < 24*3600: # i.e. checked less than 24 hours ago
            logger.debug("Check for updates didn't run as it hasn't been 24 hours since the last check")
            # pass - enable for testing
            return
        else:
            logger.debug(f"Check for updates. OS is {sys.platform}")
            self.lastUpdatetime = time.time()
            self.userconfig.set("init", "checkedupdate", str(self.lastUpdatetime))

        if not sys.platform.startswith("win"):
            return

        # Calculate the age of the running executable
        file_age_seconds = 0
        try:
            # sys.executable points to ptxprint.exe in a frozen build
            exe_mtime = os.path.getmtime(sys.executable)
            file_age_seconds = time.time() - exe_mtime
            logger.debug(f"Current PTXprint installation is {file_age_seconds / (24*3600):.1f} days old.")
        except OSError as e:
            logger.warning(f"Could not determine executable modification time: {e}")

        version = None
        if self.noInt is None or self.noInt:
            logger.debug(f"Returning because no Internet connection is available.")
            return
            
        self.thread = Thread(target=self._checkUpdate, args=(wid, file_age_seconds, True))
        self.thread.start()

    def openURL(self, url):
        if self.noInt is None or self.noInt:
            self.deniedInternet()
            return
        webbrowser.open(url)

    def onUpdateButtonClicked(self, btn):
        self.openURL("https://software.sil.org/ptxprint/download")

    def onGiveFeedbackClicked(self, btn):
        self.popdownMainMenu()
        self.openURL(r"http://tiny.cc/ptxprintfeedback")
                    
    def onDonateClicked(self, btn):
        self.popdownMainMenu()
        self.openURL(r"https://give.sil.org/campaign/597654/donate")
                    
    def deniedInternet(self):
        self.doError(_("Internet Access Disabled"), secondary=_("All Internet URLs have been disabled \nusing the option on the Advanced Tab"))

    def editZvarsClicked(self, btn):
        self.rescanFRTvarsClicked(None, autosave=True)
        mpgnum = self.notebooks['Main'].index("tb_Peripherals")
        self.builder.get_object("nbk_Main").set_current_page(mpgnum)
        self.set("c_frontmatter", True)

    def editFrontMatterClicked(self, btn):
        mpgnum = self.notebooks['Main'].index("tb_Viewer")
        self.builder.get_object("nbk_Main").set_current_page(mpgnum)
        pgnum = self.notebooks["Viewer"].index("tb_FrontMatter")
        self.builder.get_object("nbk_Viewer").set_current_page(pgnum)

    def rescanFRTvarsClicked(self, btn, autosave=True):
        prjid = self.get("fcb_project")
        if autosave:
            self.onSaveEdits(None, pgid="tb_FrontMatter") # make sure that FRTlocal has been saved
        fpath = self.configFRT()
        with universalopen(fpath) as inf:
            frtxt = inf.read()
        vlst = regex.findall(r"(\\zvar ?\|)([a-zA-Z0-9\-]+)\\\*", frtxt)
        for a, b in vlst:
            if b == "copiesprinted" and self.getvar(b) is None:
                self.setvar(b, "50")
            elif b == "toctitle":
                pass
            elif self.getvar(b, default=None) is None:
                self.setvar(b, _("<Type Value Here>"))
                
    def onEnglishClicked(self, btn):
        self.styleEditor.editMarker()
        self.userconfig.set("init", "englinks", "true" if self.get("c_useEngLinks") else "false")
        self.i18nizeURIs()
        
    def onvarEdit(self, tv, path, text): #cr, path, text, tv):
        model = tv.get_model()
        it = model.get_iter_from_string(path)
        if it:
            model.set(it, 1, text.strip())
            self.setvar(model.get(it, 0)[0], text.strip())
            self.changed()

    def onzvarAdd(self, btn):
        def responseToDialog(entry, dialog, response):
            dialog.response(response)
        dialog = Gtk.MessageDialog(parent=None, message_type=Gtk.MessageType.QUESTION,
                 buttons=Gtk.ButtonsType.OK_CANCEL, text=_("Variable Name"))
        entry = Gtk.Entry()
        entry.connect("activate", responseToDialog, dialog, Gtk.ResponseType.OK)
        dbox = dialog.get_content_area()
        dbox.pack_end(entry, False, False, 0)
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            k = entry.get_text()
            if self.getvar(k, default=None) is None:
                self.setvar(k, "")
        dialog.destroy()

    def onzvarDel(self, btn):
        tv = self.builder.get_object("tv_zvarEdit")
        selection = tv.get_selection()
        model, i = selection.get_selected_rows()
        for r in reversed(i):
            itr = model.get_iter(r)
            model.remove(itr)
            self.changed()

    # def onPageSizeChanged(self, btn): # was a signal on ecb_pagesize
        # val = "cropmarks" in self.get("ecb_pagesize")
        # for w in ["c_cropmarks", "c_grid"]:
            # self.set(w, val)

    def onFootnoteRuleClicked(self, btn):
        status = self.sensiVisible("c_footnoterule")
        self.builder.get_object("rule_footnote").set_visible(status)

    def onXrefRuleClicked(self, btn):
        status = self.sensiVisible("c_xrefrule")
        self.builder.get_object("rule_xref").set_visible(status)

    def button_release_callback(self, widget, event, data=None):
        # If a user wants to highlight a control (for training or documentation
        # purposes) using Ctrl to toggle state then we want it to be a 
        # different color from the peachpuff which carries another meaning.
        if event.get_state() & Gdk.ModifierType.CONTROL_MASK:
            sc = widget.get_style_context()
            if sc.has_class("yellowlighted"):
                sc.remove_class("yellowlighted")
            else:
                sc.add_class("yellowlighted")
            return True

    def grab_notify_event(self, widget, event, data=None):
        pass

    def onCatListAdd(self, btn):
        def responseToDialog(entry, dialog, response):
            dialog.response(response)
        dialog = Gtk.MessageDialog(parent=None, message_type=Gtk.MessageType.QUESTION,
                 buttons=Gtk.ButtonsType.OK_CANCEL, text=_("Category Name"))
        entry = Gtk.Entry()
        entry.connect("activate", responseToDialog, dialog, Gtk.ResponseType.OK)
        dbox = dialog.get_content_area()
        dbox.pack_end(entry, False, False, 0)
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
        self.set("lb_sbFilename", "")
        isbg = btname == "btn_sbBGIDia"
        self.styleEditor.sidebarImageDialog(isbg)
        
    def onSBimageFileChooser(self, btn):
        picpath = self.project.path
        def update_preview(dialog):
            picpath = dialog.get_preview_filename()
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(picpath, 200, 300)
            except Exception as e:
                pixbuf = None
            return pixbuf

        picfiles = self.fileChooser(_("Choose Image"),
                                  filters={"Images": {"patterns": ['*.jpg', '*.png', '*.pdf'], "mime": "application/image"}},
                                   multiple=False, basedir=picpath, preview=update_preview)
        self.set("lb_sbFilename", str(picfiles[0]) if picfiles is not None and len(picfiles) else "")
        self.changed()

    def onCoverSelectImageClicked(self, btn):
        picpath = self.project.path
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
        self.set("lb_coverImageFilename", str(picfiles[0]) if picfiles is not None and len(picfiles) else "")
        self.changed()

    def onDeleteTempFolders(self, btn):
        notDeleted = []
        for p in self.project.configs.keys():
            path2del = os.path.join(self.project.printPath(p))
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
        self.changed()

    def onMarginalVersesClicked(self, btn):
        self.onSimpleClicked(btn)
        if self.sensiVisible("c_marginalverses"):
            self.builder.get_object("c_hangpoetry").set_active(False)

    def onBaseFontSizeChanged(self, btn):
        if self.loadingConfig or self.noUpdate:
            return
        self.noUpdate = True
        lnsp = -1
        if self.get("c_lockFontSize2Baseline"):
            lnsp = float(self.get("s_fontsize")) / self.font2baselineRatio
            self.set("s_linespacing", lnsp)
        else:
            self.updateFont2BaselineRatio()
        if self.gtkpolyglot:
            if lnsp >= 0:
                self.gtkpolyglot.setbaseline(lnsp)
            self.gtkpolyglot.setfontsize(self.get("s_fontsize"))
        self.noUpdate = False

    def onBaseLineSpacingChanged(self, btn):
        if self.loadingConfig or self.noUpdate:
            return
        self.noUpdate = True
        fntsz = -1
        if self.get("c_lockFontSize2Baseline"):
            fntsz = float(self.get("s_linespacing")) * self.font2baselineRatio
            self.noUpdate = True
            self.set("s_fontsize", fntsz)
        else:
            self.updateFont2BaselineRatio()
        if self.gtkpolyglot:
            if fntsz >= 0:
                self.gtkpolyglot.setfontsize(fntsz)
            self.gtkpolyglot.setbaseline(self.get("s_linespacing"))
        self.noUpdate = False
            
    def onLockRatioClicked(self, btn):
        if self.loadingConfig:
            return
        if self.get("c_lockFontSize2Baseline"):
            self.updateFont2BaselineRatio()

    def onMarginEnterNotifyEvent(self, btn, *args):
        self.highlightMargin(btn, True)

    def onMarginLeaveNotifyEvent(self, btn, *args):
        self.highlightMargin(btn, False)

    def showColouredArrows(self, status=True):
        for i in _clr:
            self.builder.get_object("img_{}".format(_clr[i])).set_visible(status)
            if _clr[i].startswith("bot"):
                if self.get("c_noinkinmargin"):
                    self.builder.get_object("img_ni{}".format(_clr[i])).set_visible(status)
                    self.builder.get_object("img_{}".format(_clr[i])).set_visible(False)
                else:
                    self.builder.get_object("img_ni{}".format(_clr[i])).set_visible(False)
                    self.builder.get_object("img_{}".format(_clr[i])).set_visible(status)
                
    def highlightMargin(self, btn, highlightMargin=True):
        self.showColouredArrows(False)
        n = Gtk.Buildable.get_name(btn)
        iname = _clr[n[2:]]
        ni = "ni" if self.get("c_noinkinmargin") and iname.startswith("bot") else ""
        wid = "img_" + ni + iname

        if highlightMargin:
            self.builder.get_object(wid).set_visible(True)
        else:
            self.updateMarginGraphics()

    def onOnlyShowVerseumsToggled(self, btn):
        self.strongs = None
        
    def onExtListSourceChanges(self, fcb):
        self.Strongs = None
        s = self.get("fcb_xRefExtListSource")
        ttt = self.builder.get_object("r_xrSource_{}".format(s.split("_")[0])).get_tooltip_text()
        self.builder.get_object("btn_infoXrefSource").set_tooltip_text(ttt)
        self.builder.get_object("fr_strongs").set_sensitive(s.startswith("strongs"))
        self.builder.get_object("btn_selectXrFile").set_sensitive(s == "custom")

    def onNoInkInMarginClicked(self, btn):
        self.updateMarginGraphics()

    def onPagesPerSpreadChanged(self, btn):
        self.colorTabs()
        status = self.get("fcb_pagesPerSpread") != "1"
        if status and self.showPDFmode == "preview":
            self.set("c_bkView", False)
            self.set("c_pdfadjoverlay", False)
            self.set("c_pdfparabounds", False)
            self.builder.get_object("c_pdfadjoverlay").set_sensitive(False)
            self.builder.get_object("c_pdfparabounds").set_sensitive(False)
            self.onBookViewClicked(None)
        else:
            self.builder.get_object("c_bkView").set_sensitive(True)
            self.builder.get_object("c_pdfadjoverlay").set_sensitive(True)
            self.builder.get_object("c_pdfparabounds").set_sensitive(True)
        for w in ["s_sheetsPerSignature", "ecb_sheetSize", "s_foldCutMargin", "c_foldFirst", 
                  "l_sheetsPerSignature", "l_sheetSize",   "l_foldCutMargin"]:
            self.builder.get_object(w).set_sensitive(status)

    def onTxlOptionsChanged(self, btn):
        o = _("What did Mary say that God had done?")
        # ov = "<b>"+o+"</b>" if self.get("c_txlBoldOverview") else o
        ov = o
        t1 = _("What does it means to bless someone?")
        t2 = _("What do you know about the high priest?")
        overview = self.get("c_txlQuestionsOverview")
        numberedQs = self.get("c_txlQuestionsNumbered")
        showRefs = self.get("c_txlQuestionsRefs")
        if numberedQs and showRefs:
            ex = f"13. (3:25) {t1}\n14. (4:6) {t2}"
            l = f"12. (1:46-56) {ov}\n{ex}" if overview else ex
        elif numberedQs:
            ex = f"13. {t1}\n14. {t2}"
            l = f"12. {ov}\n{ex}" if overview else ex
        elif showRefs:
            ex = f"3:25 {t1}\n4:6 {t2}"
            l = f"1:46-56 {ov}\n{ex}" if overview else ex
        else:
            ex = f"{t1}\n{t2}"
            l = f"{ov}\n{ex}" if overview else ex
        self.builder.get_object("l_txlExample").set_label(l)

    def onCoverSettingsChanged(self, btn):
        self.sensiVisible("c_makeCoverPage")
        self.colorTabs()
        hbx = self.builder.get_object("bx_coverPreview")
        b = self.builder.get_object("vp_coverBack")
        s = self.builder.get_object("vp_spine")
        f = self.builder.get_object("vp_coverFront")
        for v in [b,s,f]:
            hbx.remove(v)
        if self.get("c_RTLbookBinding"):
            for v in [b,s,f]:
                hbx.pack_end(v, False, False, 0)
        else:
            for v in [f,s,b]:
                hbx.pack_end(v, False, False, 0)
        
        rotateDegrees = float(self.get("fcb_rotateSpineText"))
        self.builder.get_object("lb_spineTitle").set_angle(rotateDegrees)
        if rotateDegrees != 0:
            self.builder.get_object("lb_spineTitle").set_label(_("Main Title   -   Subtitle"))
        else:
            self.builder.get_object("lb_spineTitle").set_label(_("Main\nTitle\n\nSubtitle"))
        if rotateDegrees == 90:
            self.styleEditor.setval('cat:coverspine|esb', 'Rotation', 'l')
        elif rotateDegrees == 270:
            self.styleEditor.setval('cat:coverspine|esb', 'Rotation', 'r')
        else:
            self.styleEditor.setval('cat:coverspine|esb', 'Rotation', 'F')
        
        pgs = float(self.get("s_totalPages"))
        adj = float(self.get("s_coverAdjust"))
        thck = float(self.get("s_paperWidthOrThick"))
        if self.get("r_paperCalc") == "weight":
            # Value below is from Pretore's paper thickness calculations 
            #                     (GSM/um, 36/43, 40/47, 50/60, 60/70)
            thck = thck / .845 
        self.spine = (thck * pgs / 2000) + adj

        showSpine = self.sensiVisible("c_inclSpine")
        self.set('c_coverCropMarks', showSpine)
        for w in ["vp_spine", "lb_style_cat:coverspine|esb"]:
            self.builder.get_object(w).set_visible(showSpine)
            
        self.builder.get_object("lb_style_cat:coverspine|esb").set_visible(self.get("c_inclSpine"))
        # Calculate the actual page width (in mm) based on page size
        pw = convert2mm(re.sub(r"^(.*?)\s*[,xX].*$", r"\1", self.get("ecb_pagesize") or "148mm"))
        # 180 is the width (pixels) of the front/back page in the UI
        thick = self.spine * 180 / pw
        self.builder.get_object("vp_spine").set_size_request(thick, -1)
        self.builder.get_object("l_spineWidth").set_label(f"{self.spine:.3f}mm")

    def editCoverSidebarStyle(self, btn, foo):
        posn = Gtk.Buildable.get_name(btn)[3:]
        self.styleEditor.selectMarker(f"cat:cover{posn}|esb")
        mpgnum = self.notebooks['Main'].index("tb_StyleEditor")
        self.builder.get_object("nbk_Main").set_current_page(mpgnum)
        self.wiggleCurrentTabLabel()

    def onFillRequestIllustrationsForm(self, btn):
        # These 3 are intentionally NOT filled in. They will need 
        # to be filled in manually on the form before submission
        # &entry.404873931=email@address.org
        # &entry.1412507746=Supervisor+name
        # &entry.1562752049=Supervisor+email
        _formURL = 'https://docs.google.com/forms/d/e/1FAIpQLScCAOsNhonkU8H9msz7eUncVVme4MvtJ7Tnzjgl9s-KAtL3oA/viewform?usp=pp_url'
        entries = []

        booklist = set(self.getBooks())
        pics = self.getPicsInConfig(booklist)
        if not len(pics):
            return

        prjName = self.ptsettings.get('FullName', "") if self.ptsettings is not None else ""
        entries.append(f"&entry.344966571={prjName}")                       # Paratext Project Name
        entries.append(f"&entry.732448545={self.getUserName()}")            # Paratext Registration Name
        entries.append(f"&entry.751047469={self.getvar('pubentity', '')}")  # Organization
        entries.append(f"&entry.920891476={',+'.join(pics)}")               # List of Illustrations
        
        ans1 = "1. I am requesting access to a specific set of illustrations to be used in one translation project."
        entries.append(f"&entry.1554405631={ans1}")
        entries.append(f"&entry.634072881={ans1}")
        ans2 = "2. Typesetting for print publications using PTXprint."
        entries.append(f"&entry.75078676={ans2}")
        ans3 = "Yes, I agree."
        entries.append(f"&entry.1763079060={ans3}")
        entries.append(f"&entry.646337528={ans3}")
        ans4 = "Yes"
        entries.append(f"&entry.580369903={ans4}")

        url = f"{_formURL}{''.join(entries)}".replace(" ", "+")
        logger.debug(f"Opening Pre-populated Request for Illustrations Form: {url}")
        self.openURL(url)
        
    def getUserName(self):
        unfpath = self.prjTree.findFile("localUsers.txt")
        ptregname = ""
        if unfpath is not None and os.path.exists(unfpath):
            with open(unfpath, 'r') as file:
                ptregname = file.readline().strip()  # Read the first line and strip any extra whitespace
        return ptregname

    def getPicsInConfig(self, booklist):
        pics = [x["src"][:-5].lower() for x in self.picinfos.get_pics() if x["anchor"][:3] in booklist]
        if len(pics) == 0:
            _errText = _("No illustrations were detected for this configuration.")
            self.doError("Request Error", secondary=_errText, \
                      title="PTXprint", copy2clip=False, show=True)
        return pics

    def onFillPicturePermissionForm(self, btn):
        _formURL = 'https://docs.google.com/forms/d/e/1FAIpQLScGc_jhYmu2KrVzlX8oL0-Iw32-0UY6kzD6j_wm5j-VD6RsAw/viewform?usp=pp_url'
        entries = []
        pics = []
        metadata = {"country":       "<Country>", 
                    "langiso":       "<Ethnologue code>", 
                    "languagename":  "<Language>", 
                    "maintitle":     "<Title>", 
                    "englishtitle" : "<Title in English>",
                    "pubtype":       "<[Portion|NT|Bible]>",
                    "copiesprinted": "<99>",
                    "pubentity":     "<Publishing Entity>"}
        entryIDs = {"1044245222": "pubentity",       #Organization
                    "1280052018": "country",         #Country Name
                    "1836240032": "languagename",    #Language Name
                    "117154869" : "langiso",         #Language Identifier
                    "1711096593": "maintitle",       #Vernacular Publication Title
                    "670351452" : "englishtitle",    #English Publication Title
                    "1279725472": "copiesprinted"}   #Number of Copies

        booklist = set(self.getBooks())
        pics = self.getPicsInConfig(booklist)
        if not len(pics):
            return
        # If meta-data fields are missing, ask the user to fill them in.
        missing = False
        for k, v in metadata.items():
            if self.getvar(k, default=None) is None:
                missing = True
                self.setvar(k, v)
        if missing:
            mpgnum = self.notebooks['Main'].index("tb_Peripherals")
            self.builder.get_object("nbk_Main").set_current_page(mpgnum)
            _errText = _("Please fill in any missing <Values> on") + "\n" + \
                       _("the Peripherals tab before proceeding.")
            self.doError("Missing details for permission request form", secondary=_errText, \
                      title="PTXprint", copy2clip=False, show=True)
            return
        entries.append(f"&entry.1518194895={self.getUserName()}")
        validRegKey = False
        if self.ptsettings is not None:
            regKey = self.ptsettings.get('ParatextRegistryId', "")
            if len(regKey):
                validRegKey = True
        if validRegKey:
            entries.append(f"&entry.1337767606=Yes")
            entries.append(f"&entry.1765920399=https://registry.paratext.org/projects/{regKey}")
        else:
            entries.append(f"&entry.1337767606=No")

        for k, v in entryIDs.items():
            entries.append(f"&entry.{k}={self.getvar(v, '')}")

        sensitive = "Yes" if self.get('c_sensitive') else "No"
        entries.append(f"&entry.912917069={sensitive}")
        entries.append(f"&entry.1060720564=Scripture,+including+Study+Bible")                     #Publication Type()
        entries.append(f"&entry.1928747119={self.getvar('pubtype', '')} ({' '.join(booklist)})")  #Scope of Publication
        entries.append(f"&entry.667305653={',+'.join(pics)}")
        entries.append(f"&entry.933375377=print")
        entries.append(f"&entry.882233224=No")                                  #Reprint(Yes/No)
        # entries.append(f"&entry.437213008" : "",           #Questions or Comments
        # entries.append(f"&entry.1059397738": "",           #Sign(get them to fill it in manually!)
        
        if self.noInt is None or self.noInt:
            # If the user has internet access disabled, draft an e-mail and put it on the clipboard.
            if self.get('c_sensitive'):
                sensitive = "\nDue to regional sensitivities, we plan to use the abbreviated form " + \
                "(© DCC, or © BFBS) in the copyright statement for these illustration.\n"
            else:
                sensitive = ""
            _permissionRequest = """
TO: International Publishing Services Coordinator
7500 West Camp Wisdom Road
Dallas, TX 75236 USA\n
I am writing to request permission to use the following illustrations in a publication.\n
1. The name of the country, language, Ethnologue code:
\t{}, {}, {}\n
2. The title of the book in the vernacular:
\t{}\n
3. The title of the book in English:
\t{}\n
4. The kind of book:
\t{}\n
5. The number of books to be printed:
\t{} copies\n
6. The number of illustrations and specific catalog number(s) of the illustrations/pictures:
\t{} illustrations:\n{}\n{}
Thank you,
{}
{}
""".format(self.getvar("country", ""), self.getvar("languagename",  ""), \
           self.getvar("langiso", ""), self.getvar("maintitle",     ""), \
           self.getvar("englishtitle", ""), self.getvar("pubtype", "") + " (" + ' '.join(booklist) + ")", \
           self.getvar("copiesprinted", ""), len(pics), ', '.join(pics), sensitive, \
           self.getUserName(), self.getvar("pubentity", ""))
            self.doError("Illustration Usage Permission Request", secondary=_permissionRequest, \
                          title="PTXprint", copy2clip=True, show=True, \
                          who2email="scripturepicturepermissions_intl@sil.org")
        else:
            url = f"{_formURL}{''.join(entries)}".replace(" ", "+")
            logger.debug(f"Opening Pre-populated Permission Request Form: {url}")
            self.openURL(url)
            
    def onOverridePageCountClicked(self, btn):
        override = self.sensiVisible('c_overridePageCount')
        if not override:
            self.set('s_totalPages', self.getPageCount(), mod=False)

    def getPageCount(self):
        if self.getBooks() == []:
            return
        xdvname = os.path.join(self.project.printPath(self.cfgid), self.baseTeXPDFnames()[0] + ".xdv")
        if os.path.exists(xdvname):
            return xdvigetpages(xdvname)
        else:
            return 99

    def onCatalogClicked(self, btn):
        catpdf = os.path.join(pycodedir(), "PDFassets", "reference", "OrnamentsCatalogue.pdf")
        logger.debug(f"{catpdf=}")
        if not os.path.exists(catpdf):
            catpdf = os.path.join(pycodedir(), "..", "..", "..", "docs", "documentation", "OrnamentsCatalogue.pdf")
        if not os.path.exists(catpdf):
            logger.warn(f"Ornaments Catalogue not found: {catpdf}")
        else:
            showref = self.builder.get_object("dlg_preview")
            self.pdf_viewer.loadnshow(catpdf, widget=showref)
            self.set("c_bkView", False, mod=False)
            self.pdf_viewer.set_zoom_fit_to_screen(None)
        logger.debug(f"{catpdf=}")

    def onTechRefClicked(self, btn):
        techref = os.path.join(pycodedir(), "PDFassets", "reference", "PTXprintTechRef.pdf")
        logger.debug(f"{techref=}")
        if not os.path.exists(techref):
            techref = os.path.join(pycodedir(), "..", "..", "..", "docs", "documentation", "PTXprintTechRef.pdf")
        if not os.path.exists(techref):
            logger.warn(f"Technical Reference not found: {techref}")
        else:
            showref = self.builder.get_object("dlg_preview")
            self.pdf_viewer.loadnshow(techref, widget=showref)
            self.set("c_bkView", True, mod=False)
            self.pdf_viewer.set_zoom_fit_to_screen(None)
        logger.debug(f"{techref=}")

    def onCropMarksClicked(self, btn):
        if not self.get("c_coverCropMarks"):
            self.set("s_coverBleed", 0, mod=False)
            self.set("s_coverArtBleed", 0, mod=False)

    def onGotCoverFocus(self, widget, event):
        if not self.get('c_overridePageCount'):
            self.set('s_totalPages', self.getPageCount(), mod=False)
            
    def isCoverTabOpen(self):
        if not self.get("c_makeCoverPage"):
            return False
        if self.builder.get_object("nbk_Main").get_current_page() == self.notebooks["Main"].index("tb_Cover"):
            return True
        else:
            return False

    def onGetPicturesClicked(self, btn): # Catalogue...
        dialog = self.builder.get_object("dlg_imagePicker")
        gridbox = self.builder.get_object("box_images")
        self.thumbnails = ThumbnailDialog(dialog, self, gridbox, 5)
        res = self.thumbnails.run()
        if res:
            for p in res:
                ref = p[1]
                if ref is None:
                    ref = Ref("UNK 0:0")
                if ref.verse == 0:
                    ref.verse = ref.numverses() // 2 + 1
                self.picinfos.addpic(suffix=self.digSuffix, anchor=p[1].str(env=Environment(cvsep='.')), src=p[0]+'.jpg',
                        ref=p[1].str(env=self.getRefEnv(nobook=True)), alt=p[2], size='col', pgpos='tl')
            self.picListView.load(self.picinfos)

    def onArtistToggled(self, btn, path):
        model = self.builder.get_object("ls_artists")
        model[path][0] = not model[path][0]
        
        if model[path][0]:
            self.thumbnails.add_artist(model[path][1].lower())
        else:
            self.thumbnails.remove_artist(model[path][1].lower())
        logger.debug(f"Toggled {path}")

    def btnImageRefreshClicked(self, btn):
        self.thumbnails.refresh()
        
    def onImgClearSelected(self, btn):
        self.thumbnails.clear()
        
    def onImageSearchChanged(self, btn):
        t = self.get('t_artSearch')
        self.thumbnails.set_filter(t)
        
    def onImageRefRangeChanged(self, btn):
        t = self.get('t_artRefRange')
        self.thumbnails.set_reflist(t)

    def onImageSetChosen(self, ecb, *a):
        imgset = self.get('ecb_artPictureSet')
        try:
            self.thumbnails.set_imageset(imgset)
        except AttributeError:
            pass

    def onSBborderSettingsChanged(self, btn):
        self.styleEditor.onSBborderSettingsChanged()
        
    def boxPaddingUniformClicked(self, btn):
        self.styleEditor.boxPaddingUniformClicked()
        
    def bdrPaddingUniformClicked(self, btn):
        self.styleEditor.bdrPaddingUniformClicked()

    def onlockXeTeXLayoutClicked(self, wid):
        if self.get("c_lockXeTeXLayout"):
            self.set("s_ptxversion", str(TexModel._ptxversion))
        else:
            self.set("s_ptxversion", "0")

    def onlockUI4LayoutClicked(self, wid):
        self.sensiVisible('c_lockUI4Layout')

    def onProtectPicListClicked(self, wid):
        status = self.get("c_protectPicList")
        self.builder.get_object('l_picListWarn1').set_visible(not status)
        self.builder.get_object('l_picListWarn2').set_visible(not status)

    def onMoveEndOfAyahClicked(self, wid):
        self.set('c_verseNumbers', not self.get("c_decorator_endayah"))
        
    def onGridSettingChanged(self, wid, x):
        if self.loadingConfig:
            return
        status = self.get("c_noGrid")
        self.builder.get_object('c_variableLineSpacing').set_sensitive(status)
        self.set("c_variableLineSpacing", status)
        self.set("c_allowUnbalanced", status)
        if status and self.get("c_doublecolumn") and float(self.get("s_bottomrag")) == 0:
            self.highlightwidget("c_allowUnbalanced")

    def onAllowUnbalancedClicked(self, wid):
        if self.loadingConfig:
            return
        if self.get("c_doublecolumn") \
           and self.get("c_allowUnbalanced") and float(self.get("s_bottomrag")) == 0:
            self.highlightwidget("c_allowUnbalanced")
            self.set("s_bottomrag", 3.0)
        else: # float(self.get("s_bottomrag")) > 0:
            self.highlightwidget("c_allowUnbalanced", highlight=False)

    def onNoteLinesClicked(self, wid):
        if self.loadingConfig:
            return
        status = self.sensiVisible("c_noteLines")
        self.set("c_pagegutter", status)
        self.set("c_outerGutter", status)
        self.builder.get_object('col_noteLines').set_visible(status)
        if status:
            if float(self.get("s_pagegutter",0)) < 30:
                self.set("s_pagegutter", 40)

    def set_showPDFmode(self, menuitem, option_value):
        self.showPDFmode = option_value
        self.userconfig.set('init', 'showPDFmode', option_value)
        self.updateShowPDFmenu()
        self.popdownMainMenu()
        self.onShowPDF(None)

    def onShowPDF(self, path=None):
        pdffile = os.path.join(self.project.printPath(None), self.getPDFname()) if path is None else str(path)
        if self.showPDFmode == "preview":
            prvw = self.builder.get_object("dlg_preview")
            if os.path.exists(pdffile):
                if pdffile.endswith(("_cover.pdf", "_diff.pdf")):
                    plocname = None
                else:
                    plocname = os.path.join(self.project.printPath(self.cfgid), self.baseTeXPDFnames()[0]+".parlocs")
                self.pdf_viewer.loadnshow(pdffile, rtl=self.get("c_RTLbookBinding", False), parlocs=plocname, \
                                          widget=prvw, page=None, isdiglot=self.get("c_diglot"))
            else:
                self.pdf_viewer.clear(widget=prvw)

        elif os.path.exists(pdffile):
            if self.showPDFmode == "sysviewer":
                startfile(pdffile)
            elif self.showPDFmode == "openfolder":
                startfile(self.project.printPath(None))
    
    def onClosePreview(self, widget):
        self.builder.get_object("dlg_preview").hide()

    def set_preview_pages(self, npages, units=None):
        if units:
            self.builder.get_object("l_pdfPgsSprds").set_label(units)
        lpcount = self.builder.get_object("l_pdfPgCount")
        if npages is None:
            lpcount.set_label("")
        else:
            if not self.pdf_viewer.parlocs or not self.pdf_viewer.parlocs.pnums:
                lpcount.set_label(f"{str(npages)}")  # Default to total pages
            else:
                if npages < len(self.pdf_viewer.parlocs.pnums):
                    lpcount.set_label(f"{str(npages)}")
                else:
                    minPg = min(self.pdf_viewer.parlocs.pnums)
                    last_key = list(self.pdf_viewer.parlocs.pnums.keys())[-1]
                    if minPg < 1:
                        lpcount.set_label(f"({str(abs(minPg))})+{str(last_key)}")
                    else:
                        lpcount.set_label(f"{str(last_key)}")            

    def onBookViewClicked(self, widget):
        window = self.builder.get_object("dlg_preview")
        bkview = self.get("c_bkView", True)
        pgsprd = self.get("fcb_pagesPerSpread", "1")
        allocation = window.get_allocation()
        x = allocation.width
        y = allocation.height
        if pgsprd == "1" and y > x and bkview \
           or pgsprd in ["2", "8"]:
            sz = ((x * 2) - 167, y) # (1040, 715)
        elif x > y and not bkview or pgsprd == "4":
            sz = (((x - 167) / 2) + 167, y)
        else:
            sz = (x, y)
        window.resize(*sz)
        step_increment = 2 if bkview else 1
        if hasattr(self, 'pdf_viewer'):
            self.pdf_viewer.set_zoom_fit_to_screen(None)
            self.onPgNumChanged(None, None)

    def getPgNum(self):
        if self.pdf_viewer.parlocs is not None:
            pg = self.pdf_viewer.parlocs.pnums.get(self.pdf_viewer.current_page, 1)
        else:
            pg = 1
        return pg

    def onPgNumChanged(self, widget, x):
        value = self.get("t_pgNum", "1").strip()
        pg = int(value) if value.isdigit() else 1
        if self.pdf_viewer.parlocs is not None:
            available_pnums = self.pdf_viewer.parlocs.pnums.keys()
            if len(available_pnums) and pg not in available_pnums:
                pg = min(available_pnums, key=lambda p: abs(p - pg))
        self.set("t_pgNum", str(pg), mod=False) # We need to do this here to stop it looping endlessly
        pnum = self.pdf_viewer.parlocs.pnums.get(pg, pg) if self.pdf_viewer.parlocs is not None else pg
        self.pdf_viewer.show_pdf(pnum, self.rtl, setpnum=False)

    def onPdfAdjOverlayChanged(self, widget):
        self.pdf_viewer.setShowAdjOverlay(self.get("c_pdfadjoverlay"))
        
    def onPdfParaBoxesChanged(self, widget):
        self.pdf_viewer.setShowParaBoxes(self.get("c_pdfparabounds"))

    def onPdfAnalysisChanged(self, widget):
        self.pdf_viewer.setShowAnalysis(self.get("c_layoutAnalysis"), float(self.get("s_spaceEms", 3.0)))
        
    def onPrintItClicked(self, widget):
        pages = self.pdf_viewer.numpages
        if not pages:
            return
        self.pdf_viewer.print_document()

    def onZoomLevelChanged(self, widget):
        adj_zl = max(30, min(int(float(self.get("s_pdfZoomLevel", 100))), 800))
        if self.pdf_viewer is not None:
            self.pdf_viewer.set_zoom(adj_zl / 100, scrolled=True, setz=False)
            
    def onZoomFitClicked(self, btn):
        self.pdf_viewer.set_zoom_fit_to_screen(None)

    def onZoom100Clicked(self, btn):
        self.pdf_viewer.set_zoom(1.0)

    def onSeekPage2fill(self, btn):
        direction = Gtk.Buildable.get_name(btn).split("_")[-1]
        self.pdf_viewer.seekUFpage(direction)

    def onNavigatePageClicked(self, btn):
        if self.loadingConfig:
            return
        n = Gtk.Buildable.get_name(btn)
        x = n.split("_")[-1]
        self.pdf_viewer.set_page(x)
        # print(f"No longer calling updatePageNavigation after set_page in onNavigatePageClicked")
        # self.pdf_viewer.updatePageNavigation()

    def onEditingPgNum(self, w, x):  # From 'key-release' event on t_pgNum
        if self.loadingConfig:
            return
        if hasattr(self, "pgnum_timer") and self.pgnum_timer:
            GLib.source_remove(self.pgnum_timer)
        self.pgnum_timer = GLib.timeout_add(500, self.onPgNumChanged, None, None)
        
    def onSavePDFasClicked(self, btn): # Move me to pdf_viewer!
        dialog = Gtk.FileChooserDialog(
            title="Save PDF As...",
            parent=self.mw,
            action=Gtk.FileChooserAction.SAVE,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                     Gtk.STOCK_SAVE,Gtk.ResponseType.OK))
        dialog.set_current_folder(self.userconfig.get('init', 'saveasfolder', fallback=os.path.expanduser("~")))
        dialog.set_current_name(self.getPDFname())
        pdf_filter = Gtk.FileFilter()
        pdf_filter.set_name("PDF files")
        pdf_filter.add_mime_type("application/pdf")
        dialog.add_filter(pdf_filter)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            new_file_path = dialog.get_filename()
            if not new_file_path.lower().endswith('.pdf'):
                new_file_path += '.pdf'
            try:
                pdffilepath = os.path.join(self.project.printPath(None), self.getPDFname())
                copy2(pdffilepath, new_file_path)
                self.doStatus(_("PDF saved as: ") + new_file_path)
                self.userconfig.set('init', 'saveasfolder', os.path.dirname(new_file_path).replace("\\", "/"))
            except Exception as e:
                self.doError(_("Error saving PDF: ") + str(e), 
                    secondary=_("Unable to save the PDF in the new location:") + "\n" + new_file_path)
                self.doStatus(_("Error saving PDF: ") + new_file_path)
        dialog.destroy()
      
    def onAnchorKeyRelease(self, btn, *a):
        self.builder.get_object("btn_anc_ok").set_sensitive(False) 
        curpos = self.builder.get_object("t_newAnchor").get_position() 
        msg = ""
        anc = re.sub(':', '.', self.get("t_newAnchor"))
        pattern = r"(^[123A-Z]{3})([LRA-G]?)*\s((\d+)\.(\d+)(-\d+)*|k\.\S+)$"  # includes possibility if GLO k.keywordinglossary
        match = re.match(pattern, anc)
        if not match:
            msg = _("Invalid Anchor; use format: JHN 3.16")
        else:
            self.set("t_newAnchor", anc, mod=False)
            self.builder.get_object("t_newAnchor").set_position(curpos) 
            piciter = self.picListView.find_row(anc)
            if piciter is not None:
                msg = _("There is a picture at that verse.{}Choose a different verse as anchor.").format("\n")
            else:
                self.builder.get_object("btn_anc_ok").set_sensitive(True)
            self.anchorKeypressed = True
        self.builder.get_object("l_newAnchorMsg").set_text(msg)

    def onAnchorFocusOut(self, btn, *a):
        self.anchorKeypressed = False      

    def onOpenItClicked(self, btn):
        if self.currentPDFpath is not None:
            startfile(self.currentPDFpath)

    def onLocateDigitMappingClicked(self, btn):
        self.highlightwidget('fcb_fontdigits')

    def showRulesClicked(self, btn):
        v = self.get("c_gridLines")
        if self.pdf_viewer is not None:
            self.pdf_viewer.showguides = v
            self.pdf_viewer.show_pdf()

    def showGridClicked(self, btn):
        v = self.get("c_gridGraph")
        if self.pdf_viewer is not None:
            self.pdf_viewer.showgrid = v
            self.pdf_viewer.show_pdf()

    def showRulesOrGridClicked(self, btn):
        if self.loadingConfig:
            return
        if self.get('c_updatePDF', False):
            self.onOK(None)
            
    def onShowMainDialogClicked(self, btn):
        self.mainapp.win.present()

    def get_dialog_geometry(self, dialog):
        """Retrieve the position, size, and monitor details of a given GTK dialog."""
        if dialog is None:
            return None

        # Ensure the dialog has a valid window before proceeding
        if not dialog.get_realized():
            return None

        x, y = dialog.get_position()
        width, height = dialog.get_size()

        screen = dialog.get_screen()
        window = dialog.get_window()
        if window is None:
            return None

        monitor_num = screen.get_monitor_at_window(window)

        return {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "monitor": monitor_num
        }

    def save_window_geometry(self):
        """Save positions and sizes of multiple dialogs to userconfig."""
        if not self.userconfig.has_section("geometry"):
            self.userconfig.add_section("geometry")
        prvw = self.builder.get_object("dlg_preview")
        _dialogs = {"ptxprint":    self.mainapp.win,
                    "dlg_preview": prvw }

        for name, dialog in _dialogs.items():
            geom = self.get_dialog_geometry(dialog)
            if geom:
                for key in ["x", "y", "width", "height", "monitor"]:
                    self.userconfig.set("geometry", f"{name}_{key}", str(geom[key]))

        self.saveConfig(force=True)  # Ensure settings are written (not sure we want to do this every time)

    def restore_window_geometry(self):
        """Restore dialog positions and sizes from userconfig, if the monitor is available."""
        screen = self.mw.get_screen()  # Get screen info
        current_monitor_count = screen.get_n_monitors()
        prvw = self.builder.get_object("dlg_preview")
        _dialogs = {"ptxprint":    self.mainapp.win,
                    "dlg_preview": prvw }

        for name, dialog in _dialogs.items():
            x = self.userconfig.getint("geometry", f"{name}_x", fallback=-1)
            y = self.userconfig.getint("geometry", f"{name}_y", fallback=-1)
            width = self.userconfig.getint("geometry", f"{name}_width", fallback=800)
            height = self.userconfig.getint("geometry", f"{name}_height", fallback=600)
            saved_monitor = self.userconfig.getint("geometry", f"{name}_monitor", fallback=0)

            if saved_monitor < current_monitor_count:
                dialog.move(x, y)
                dialog.resize(width, height)
        
    def onPolyglotLayoutFocusOut(self, a, b):
        self.gtkpolyglot.update_layout_preview()

    def onSpinnerClicked(self, btn, foo):
        self.highlightwidget('s_autoupdatedelay')
        self.builder.get_object("ptxprint").present()
        
    def onAnalysisSettingsClicked(self, btn, foo):
        self.highlightwidget('s_spaceEms')
        self.builder.get_object("ptxprint").present()

    def onPreviewDeleteEvent(self, widget, event): # PDF Preview dialog (X button)
        widget.hide()  # Hide the dialog instead of destroying it
        return True    # Returning True prevents the default destroy behavior

    def update_diglot_polyglot_UI(self):
        dglt = True if len(self.gtkpolyglot.ls_treeview) < 3 else False
        self.builder.get_object("btn_adjust_diglot").set_sensitive(dglt)
        merge_types = {
            _("Document based"):   "doc",
            _("Chapter Verse"):    "simple",
            _("Scored"):           "scores",
            _("Scored (Chapter)"): "scores-chapter",
            _("Scored (Verse)"):   "scores-verse"
            }
        mrgtyplist = self.builder.get_object("ls_diglotMerge")
        mrgtyplist.clear()
        orig = self.get("fcb_diglotMerge", "scores")
        for desc, code in merge_types.items():
            if dglt or code.startswith("scores"):
                mrgtyplist.append([desc, code])
        found = any(row[1] == orig for row in mrgtyplist)
        self.set("fcb_diglotMerge", orig if found else "scores") 
           
    def onGenerateReportClicked(self, btn):
        fpath = self.runReport()
        if fpath is not None:
            startfile(fpath)

    def addMapsClicked(self, btn):
        self.mapcntr = 0
        self.mapusfm = []
        dialog = self.builder.get_object("dlg_addMap")
        response = dialog.run()
        dialog.hide()
        if response == Gtk.ResponseType.OK and not self.builder.get_object("lb_mapFilename").get_label().startswith("<"):
            self.addAnotherMapClicked(None)
            mapbkid = self.get("fcb_ptxMapBook") 
            outfile = os.path.join(self.project.path, self.getBookFilename(mapbkid))
            new_map_usfm = "\n".join(self.mapusfm)
            # 1. If the file already exists, open in append mode ("a") and just add the new content
            if os.path.exists(outfile):
                with open(outfile, "a", encoding="utf-8") as outf:
                    outf.write("\n" + new_map_usfm)
            else:
                # 2. If it does not exist, create it
                title = "Maps"
                with open(outfile, "w", encoding="utf-8") as outf:
                    outf.write("\\id {0} Maps index\n\\h {1}\n\\mt1 {1}\n".format(mapbkid, title))
                    outf.write(new_map_usfm)

    def onSelectMapClicked(self, btn_selectMap):
        picroot = self.project.path
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
        mapfile = self.fileChooser(_("Choose Map Image"),
                                  filters={"Images": {"patterns": ['*.tif', '*.png', '*.jpg', '*.pdf'], "mime": "application/image"}},
                                   multiple=False, basedir=picdir, preview=update_preview)
        if mapfile is not None:

            fpath = str(mapfile[0])
            self.builder.get_object("lb_mapFilename").set_label(fpath)
            if fpath is not None and os.path.exists(fpath):
                if self.picrect is None:
                    picframe = self.builder.get_object("fr_mapPreview")
                    self.picrect = picframe.get_allocation()
                if self.picrect.width > 10 and self.picrect.height > 10:
                    try:
                        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(fpath, self.picrect.width - 6, self.picrect.height - 6)
                    except GLib.GError:
                        pixbuf = None
                    self.setPreview(pixbuf, tooltip=fpath)
                else:
                    self.setPreview(None)
            else:
                self.setPreview(None)

    def setPreview(self, pixbuf, tooltip=None):
        pic = self.builder.get_object("img_mapPreview")
        if pixbuf is None:
            pic.clear()
            tooltip = ""
        else:
            pic.set_from_pixbuf(pixbuf)
        if tooltip is not None:
            pic.set_tooltip_text(tooltip)
            self.builder.get_object("img_mapPreview").set_tooltip_text(tooltip)

    def addAnotherMapClicked(self, btn):
        mapfile = self.get("lb_mapFilename")
        caption = self.get("t_mapCaption")
        posn = self.get("t_mapPgPos")
        scale = self.get("s_mapScale")
        mapbk = self.get("fcb_ptxMapBook")
        mapcntr = 1
        if os.path.exists(mapfile):
            while True:
                anchor = f"{mapbk} map{mapcntr:02d}"
                if not self.picinfos.find(anchor=anchor):
                    break
                mapcntr += 1
            p = self.picinfos.addpic(anchor=anchor, caption=caption, srcfile=mapfile, 
                                     src=os.path.basename(mapfile), pgpos=posn, scale=scale, sync=True)
            self.set("nbk_PicList", 1)
            self.picListView.add_row(p)
            self.mapusfm.append(f'\\pb\n\\zfiga |id="{anchor[4:]}" rem="{caption}"\\*') # fixme for polyglot

        # Clear the form, ready for the next map to be selected
        self.builder.get_object("lb_mapFilename").set_label(_("<== Select an image file of the map to be added (.png, .jpg, .pdf, .tif)"))
        self.builder.get_object("t_mapCaption").set_text("")
        self.setPreview(None)

    def locateOptionsChanged(self, foo):
        if self.loadingConfig:
            return
        self.pdf_viewer.updatePageNavigation()

    def onInstallBSBclicked(self, btn):
        logger.debug("Installing BSB...")
        tdir = self.prjTree.findWriteable()
        prjid = "BSB"
        zipfile = os.path.join(getResourcesDir(), "bsb.zip")
        if UnpackBundle(zipfile, prjid, tdir):
            self._selectProject(prjid, tdir)
            logger.debug("Done installing the Berean Standard Bible")
        dialog = self.builder.get_object("dlg_DBLbundle")
        dialog.hide()
