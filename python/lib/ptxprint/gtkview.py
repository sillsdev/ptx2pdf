#!/usr/bin/python3

import sys, os, re, regex, gi, subprocess
gi.require_version('Gtk', '3.0')
from shutil import copyfile, copytree, rmtree
from gi.repository import Gtk, Pango, GObject
from gi.repository import GtkSource
import xml.etree.ElementTree as et
from ptxprint.font import TTFont, initFontCache
from ptxprint.view import ViewModel, Path
from ptxprint.runner import StreamTextBuffer
from ptxprint.ptsettings import ParatextSettings, allbooks, books, bookcodes, chaps
import configparser
import traceback
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
_alldigits = [ "Default", "Adlam", "Ahom", "Arabic-Farsi", "Arabic-Hindi", "Balinese", "Bengali", "Bhaiksuki", "Brahmi", "Burmese", 
    "Chakma", "Cham", "Devanagari", "Gujarati", "Gunjala-Gondi", "Gurmukhi", "Hanifi-Rohingya", "Javanese", "Kannada", 
    "Kayah-Li", "Khmer", "Khudawadi", "Lao", "Lepcha", "Limbu", "Malayalam", "Masaram-Gondi", "Meetei-Mayek", "Modi", "Mongolian", 
    "Mro", "Myanmar", "Myanmar-Shan", "Myanmar-Tai-Laing", "New-Tai-Lue", "Newa", "Nko", "Nyiakeng-Puachue-Hmong", "Ol-Chiki", "Oriya", 
    "Osmanya", "Pahawh-Hmong", "Persian", "Saurashtra", "Sharada", "Sinhala-Lith", "Sora-Sompeng", "Sundanese", "Tai-Tham-Hora", 
    "Tai-Tham-Tham", "Takri", "Tamil", "Telugu", "Thai", "Tibetan", "Tirhuta", "Urdu", "Vai", "Wancho", "Warang-Citi" ]

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

class Splash(Thread):
    def __init__(self, window):
        super(Splash, self).__init__()
        self.window = window
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_default_size(400, 250)
        self.window.connect('destroy', Gtk.main_quit)

    def run(self):
        GObject.threads_init()
        self.window.set_auto_startup_notification(False)
        self.window.show_all()
        self.window.set_auto_startup_notification(True)
        Gtk.main()

    def destroy(self):
        self.window.destroy()

# The 3 structures below are used by method: sensiVisible() to toggle object states

# Checkboxes and the different objects they make (in)sensitive when toggled
# Order is important, as the 1st object can be told to "grab_focus"
_sensitivities = {
    "c_mainBodyText" :         ["gr_mainBodyText"],
    "c_doublecolumn" :         ["gr_doubleColumn", "c_clSingleColLayout"],
    "c_useFallbackFont" :      ["gr_fallbackFont"],
    "c_includeFootnotes" :     ["bx_fnOptions"],
    "c_includeXrefs" :         ["bx_xrOptions"],
    "c_includeillustrations" : ["gr_IllustrationOptions"],
    "c_includefigsfromtext"  : ["c_figexclwebapp"],
    "c_diglot" :               ["gr_diglot"],
    "c_borders" :              ["gr_borders"],

    "c_multiplebooks" :        ["c_combine", "t_booklist"],
    "c_pagegutter" :           ["s_pagegutter"],
    "c_variableLineSpacing" :  ["s_linespacingmin", "s_linespacingmax", "l_min", "l_max"],
    "c_verticalrule" :         ["l_colgutteroffset", "s_colgutteroffset"],
    "c_rhrule" :               ["s_rhruleposition", "gr_horizRule"],
    "c_useChapterLabel" :      ["t_clBookList", "l_clHeading", "t_clHeading", "c_clSingleColLayout"],
    "c_autoToC" :              ["t_tocTitle", "gr_toc", "l_toc"],
    "c_marginalverses" :       ["s_columnShift"],
    "c_omitrhchapnum" :        ["c_hdrverses"],
    "c_hdrverses" :            ["c_sepPeriod", "c_sepColon"],
    "c_fnautocallers" :        ["t_fncallers", "btn_resetFNcallers"],
    "c_xrautocallers" :        ["t_xrcallers", "btn_resetXRcallers"],
    "c_blendfnxr" :            ["fcb_blendedXrefCaller"],
    "c_glossaryFootnotes" :    ["c_firstOccurenceOnly"],
    "c_usePicList" :           ["btn_editPicList"],
    "c_useCustomFolder" :      ["btn_selectFigureFolder", "c_exclusiveFiguresFolder"],
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
    "c_inclVerseDecorator" :   ["l_verseFont", "bl_verseNumFont", "l_verseSize", "s_verseNumSize", "btn_selectVerseDecorator"],
    "c_fakebold" :             ["s_boldembolden", "s_boldslant"],
    "c_fakeitalic" :           ["s_italicembolden", "s_italicslant"],
    "c_fakebolditalic" :       ["s_bolditalicembolden", "s_bolditalicslant"]
}
# Checkboxes and the different objects they make (in)sensitive when toggled
# These function OPPOSITE to the ones above (they turn OFF/insensitive when the c_box is active)
_nonsensitivities = {
    "c_omitIntroOutline" :     ["c_prettyIntroOutline"],
    "c_omitSectHeads" :        ["c_omitParallelRefs"],
    "c_multiplebooks" :        ["l_singlebook", "ecb_book", "l_chapfrom", "fcb_chapfrom", "l_chapto", "fcb_chapto"],
    "c_blendfnxr" :            ["c_includeXrefs", "c_xrautocallers", "t_xrcallers", "c_xromitcaller", "c_xrpageresetcallers", "c_paragraphedxrefs"]
}
# Checkboxes and the Tabs that they make (in)visible
_visibilities = {
    "c_showLayoutTab" :        ["tb_Layout"],
    "c_showBodyTab" :          ["tb_Body"],
    "c_showHeadFootTab" :      ["tb_HeadFoot"],
    "c_showPicturesTab" :      ["tb_Pictures"],
    "c_showAdvancedTab" :      ["tb_Advanced"],
    "c_showViewerTab" :        ["tb_ViewerEditor"],
    "c_showDiglotTab" :        ["tb_Diglot"],
    "c_showBordersTab" :       ["tb_FancyBorders"],
}

class GtkViewModel(ViewModel):

    def __init__(self, settings_dir, workingdir):
        super(GtkViewModel, self).__init__(settings_dir, workingdir)
        self.isDisplay = True
        self.config_dir = None
        self.initialised = False
        self.configNoUpdate = False
        self.chapNoUpdate = False
        self.bookNoUpdate = False
        self.pendingPid = None
        self.pendingConfig = None
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(os.path.dirname(__file__), "ptxprint.glade"))
        self.builder.connect_signals(self)
        for fcb in ("digits", "script", "chapfrom", "chapto", "textDirection", 
                    "blendedXrefCaller", "glossaryMarkupStyle", "fontFaces"):
            self.addCR("fcb_"+fcb, 0)
        # self.addCR("fcb_digits", 0)
        # self.addCR("fcb_script", 0)
        # self.addCR("fcb_chapfrom", 0)
        # self.addCR("fcb_chapto", 0)
        # self.addCR("fcb_textDirection", 0)
        # self.addCR("fcb_blendedXrefCaller", 0)
        # self.addCR("fcb_glossaryMarkupStyle", 0)
        # self.addCR("fcb_fontFaces", 0)
        self.cb_savedConfig = self.builder.get_object("ecb_savedConfig")
        self.addCR("fcb_diglotAlignment", 0)
        self.ecb_diglotSecConfig = self.builder.get_object("ecb_diglotSecConfig")
        pb = self.builder.get_object("b_print")
        pbc = pb.get_style_context()
        pbc.add_class("printbutton")
        for a in ("bl_fontR", "bl_fontB", "bl_fontI", "bl_fontBI"):
            b = self.builder.get_object(a)
            # b.get_child().set_justify(Gtk.Justification.CENTER)
            c = b.get_style_context()
            c.add_class("fontbutton")

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

        for d in ["dlg_multiBookSelector", "dlg_fontChooser", "dlg_password"]:
            dialog = self.builder.get_object(d)
            dialog.add_buttons(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.fileViews = []
        for i,k in enumerate(["FinalSFM", "PicList", "AdjList", "TeXfile", "XeTeXlog", "Settings"]):
            buf = GtkSource.Buffer()
            view = GtkSource.View.new_with_buffer(buf)
            scroll = self.builder.get_object("scroll_" + k)
            #scroll.add_with_viewport(view)
            scroll.add(view)
            self.fileViews.append((buf, view))
            if i > 2:
                view.set_show_line_numbers(True)  # Turn these ON
            else:
                view.set_show_line_numbers(False)  # Turn these OFF

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
            if os.path.exists(os.path.join(self.settings_dir, d, 'Settings.xml')):
                allprojects.append(d)
        for p in sorted(allprojects, key = lambda s: s.casefold()):
            projects.append([p])
            digprojects.append([p])
        wide = int(len(allprojects)/16)+1
        self.builder.get_object("fcb_project").set_wrap_width(wide)
        self.builder.get_object("fcb_diglotSecProject").set_wrap_width(wide)

    def run(self, callback, splash=True):
        self.callback = callback
        if splash:
            splashw = self.builder.get_object("w_splash")
            self.splash = Splash(splashw)   # threads don't like being gced?
            self.splash.start()

        # do slow stuff here
        fc = initFontCache()
        lsfonts = self.builder.get_object("ls_font")
        # sleep(1)  # Until we want people to see the splash screen

        olst = ["b_print", "bx_SavedConfigSettings", "tb_Layout", "tb_Body", "tb_HeadFoot", "tb_Pictures",
                "tb_Advanced", "tb_Logging", "tb_ViewerEditor", "tb_Diglot", "tb_FancyBorders"]
        self.initialised = True
        for o in olst:
            self.builder.get_object(o).set_sensitive(False)
        if self.pendingPid is not None:
            self.set("fcb_project", self.pendingPid)
            self.pendingPid = None
        if self.pendingConfig is not None:
            self.set("ecb_savedConfig", self.pendingConfig)
            self.pendingConfig = None
        if splash:
            self.splash.destroy()
            try:
                self.splash.join()
            except RuntimeError:
                pass        
        fc.fill_liststore(lsfonts)
        tv = self.builder.get_object("tv_fontFamily")
        cr = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn("Family", cr, text=0, weight=1)
        tv.append_column(col)
        ts = self.builder.get_object("t_fontSearch")
        tv.set_search_entry(ts)
        self.mw.resize(730, 640)
        self.mw.show_all()
        Gtk.main()

    def onHideAdvancedSettingsClicked(self, c_hideAdvancedSettings):
    # This method needs a big tidy-up!
        if self.get("c_hideAdvancedSettings"):
            # Turn Dangerous Settings OFF
            for c in ("c_startOnHalfPage", "c_marginalverses", "c_prettyIntroOutline", "c_blendfnxr", "c_autoToC",
                      "c_figplaceholders", "c_omitallverses", "c_glueredupwords", "c_omit1paraIndent", "c_hangpoetry", 
                      "c_preventwidows", "c_PDFx1aOutput", "c_diglot", "c_hyphenate", "c_variableLineSpacing",
                      "c_showAdvancedTab", "c_showViewerTab", "c_elipsizeMissingVerses"):  # "c_showBodyTab", 
                self.builder.get_object(c).set_active(False)

            # Turn Essential Settings ON
            for c in ("c_mainBodyText", "c_skipmissingimages", "c_includefigsfromtext"):
                self.builder.get_object(c).set_active(True)
            self.builder.get_object("c_hideAdvancedSettings").set_opacity(0.2)
            self.builder.get_object("c_hideAdvancedSettings").set_tooltip_text("")
            
        else:
            self.builder.get_object("c_hideAdvancedSettings").set_opacity(1.0)
            self.builder.get_object("c_hideAdvancedSettings").set_tooltip_text("Many of the settings in this tool only need to be\n" + \
                "set up once, or used on rare occasions. These can\nbe hidden away for most of the time if that helps.\n\n" + \
                "This setting can be toggled off again later, but\nis intentionally almost invisible (though located\nin the same place).")
                      
            for c in ("c_showAdvancedTab", "c_showViewerTab"):
                self.builder.get_object(c).set_active(True)

        for c in ("tb_Advanced", "tb_ViewerEditor", "tb_Diglot", "tb_FancyBorders", "l_missingPictureString",
                  "btn_editPicList", "l_imageTypeOrder", "t_imageTypeOrder", "fr_chapVerse", "s_colgutteroffset",
                  "fr_Footer", "bx_TopMarginSettings", "gr_HeaderAdvOptions", "bx_AdvFootnoteConfig", "l_colgutteroffset",
                  "c_usePicList", "c_skipmissingimages", "c_useCustomFolder", "btn_selectFigureFolder", 
                  "c_startOnHalfPage", "c_prettyIntroOutline", "c_marginalverses", "s_columnShift", "c_figplaceholders",
                  "fr_FontConfig", "fr_fallbackFont", "fr_paragraphAdjust", "l_textDirection", "l_colgutteroffset",
                  "bx_fnCallers", "bx_fnCalleeCaller", "bx_xrCallers", "bx_xrCalleeCaller", "row_ToC", "c_hyphenate",
                  "c_omitallverses", "c_glueredupwords", "c_omit1paraIndent", "c_hangpoetry", "c_preventwidows",
                  "l_sidemarginfactor", "s_sidemarginfactor", "l_min", "s_linespacingmin", "l_max", "s_linespacingmax",
                  "c_variableLineSpacing", "c_pagegutter", "s_pagegutter", "fcb_textDirection", "l_digits", "fcb_digits",
                  "t_invisiblePassword", "t_configNotes", "l_notes", "c_elipsizeMissingVerses", "bx_ShowTabs", "fcb_glossaryMarkupStyle",
                  "gr_fnAdvOptions", "gr_fnSpacingOptions", "c_figexclwebapp", "bx_horizRule", "l_glossaryMarkupStyle"):
            self.builder.get_object(c).set_visible(not self.get("c_hideAdvancedSettings"))

        # Resize Main UI Window appropriately
        if self.get("c_hideAdvancedSettings"):
            self.mw.resize(710, 316)
        else:
            self.mw.resize(730, 640)

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
            for exp in ("Pictures", "Logging"):
                self.builder.get_object("{}{}".format(w, exp)).set_visible(value)

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

    def get(self, wid, sub=0, asstr=False):
        w = self.builder.get_object(wid)
        if w is None:
            raise KeyError(wid)
        v = ""
        if wid.startswith("ecb_"):
            model = w.get_model()
            i = w.get_active()
            if i < 0:
                e = w.get_child()
                if e is not None and isinstance(e, Gtk.Entry):
                    v = e.get_text()
            elif model is not None:
                v = model[i][sub]
        elif wid.startswith("fcb_"):
            return w.get_active_id()
        elif wid.startswith("t_"):
            v = w.get_text()
        # elif wid.startswith("f_"):
            # v = w.get_font_name()
        elif wid.startswith("c_"):
            v = w.get_active()
        elif wid.startswith("s_"):
            v = w.get_value()
        elif wid.startswith("btn_"):
            v = w.get_tooltip_text()
        elif wid.startswith("bl_"):
            v = getattr(w, 'font_info', (None, None))
            if asstr:
                v = "\n".join(v)
        elif wid.startswith("lb_") or wid.startswith("l_"):
            v = w.get_text()
        return v

    def setFontButton(self, btn, name, style):
        btn.font_info = (name, style)
        btn.set_label("{}\n{}".format(name, style))

    def set(self, wid, value):
        w = self.builder.get_object(wid)
        if wid.startswith("ecb_"):
            model = w.get_model()
            e = w.get_child()
            for i, v in enumerate(model):
                if v[w.get_entry_text_column()] == value:
                    w.set_active(i)
                    break
            else:
                if e is not None and isinstance(e, Gtk.Entry):
                    e.set_text(value)
        elif wid.startswith("fcb_"):
            w.set_active_id(value)
        elif wid.startswith("t_"):
            w.set_text(value)
        elif wid.startswith("f_"):
            w.set_font_name(value)
            # w.emit("font-set")
        elif wid.startswith("c_"):
            w.set_active(value)
        elif wid.startswith("s_"):
            w.set_value(value)
        elif wid.startswith("btn_"):
            w.set_tooltip_text(value)
        elif wid.startswith("bl_"):
            self.setFontButton(w, *value)
        elif wid.startswith("lb_") or wid.startswith("l_"):
            w.set_text(value)

    def onDestroy(self, btn):
        Gtk.main_quit()

    def doError(self, txt, secondary=None, title=None):
        dialog = Gtk.MessageDialog(parent=None, modal=True, message_type=Gtk.MessageType.ERROR,
                 buttons=Gtk.ButtonsType.OK, text=txt)
        if title is not None:
            dialog.set_title(title)
        if secondary is not None:
            dialog.format_secondary_text(secondary)
        dialog.set_keep_above(True)
        dialog.run()
        dialog.set_keep_above(False)
        dialog.destroy()

    def onOK(self, btn):
        jobs = self.getBooks()
        # If the viewer/editor is open on an Editable tab, then "autosave" contents
        if self.builder.get_object("nbk_Main").get_current_page() == 7:
            pgnum = self.builder.get_object("nbk_Viewer").get_current_page()
            if 1 <= pgnum <= 2 or pgnum == 5:
                self.onSaveEdits(None)

        # Work out what the resulting PDFs are to be called
        if len(jobs) > 1:
            if self.get("c_combine"):
                pdfnames = [os.path.join(self.working_dir, "ptxprint-{}_{}{}.pdf".format(jobs[0], jobs[-1], self.prjid))]
            else:
                pdfnames = [os.path.join(self.working_dir, "ptxprint-{}{}.pdf".format(j, self.prjid)) for j in jobs]
        else:
            pdfnames = [os.path.join(self.working_dir, "ptxprint-{}{}.pdf".format(jobs[0], self.prjid))]
        for pdfname in pdfnames:
            fileLocked = True
            while fileLocked:
                try:
                    with open(pdfname, "wb+") as outf:
                        outf.close()
                except PermissionError:
                    question = "                   >>> PLEASE CLOSE the PDF <<<\
                     \n\n{}\n\n Or use a different PDF viewer which will \
                             \n allow updates even while the PDF is open. \
                           \n\n                        Do you want to try again?".format(pdfname)
                    if self.msgQuestion("The old PDF file is open!", question):
                        continue
                    else:
                        return
                fileLocked = False

        self.callback(self)

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
        self.updateDialogTitle()

    def onSaveConfig(self, btn):
        if self.prjid is None:
            return
        newconfigId = self.get("ecb_savedConfig")
        if newconfigId == self.configId:
            self.writeConfig()
            return
        # don't updateProjectSettings, since don't want to read old config
        currconfigpath = self.configPath(cfgname=self.configId)
        configpath = self.configPath(cfgname=newconfigId, makePath=True)
        for subdirname in ("PicLists", "AdjLists"):
            if os.path.exists(os.path.join(configpath, subdirname)) \
                    or not os.path.exists(os.path.join(currconfigpath, subdirname)): 
                continue
            copytree(os.path.join(currconfigpath, subdirname), os.path.join(configpath, subdirname))
        self.configId = newconfigId
        self.set("l_settings_dir", configpath)
        self.updateDialogTitle()

    def onDeleteConfig(self, btn):
        delCfgPath = self.configPath(cfgname=self.get("t_savedConfig"))
        if not os.path.exists(os.path.join(delCfgPath, "ptxprint.cfg")):
            self.doError("Internal error occurred, trying to delete a directory tree", secondary="Folder: "+delCfgPath)
            return
        try: # Delete the entire folder
            rmtree(delCfgPath)
        except OSError:
            self.doError("Can't delete that configuration from disk", secondary="Folder: " + delCfgPath)
        self.updateSavedConfigList()
        self.set("t_savedConfig", "")
        self.set("t_configNotes", "")
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
                if 0 <= ind <= len(bp) and bp[ind - 1 if ind > 40 else ind] == "1":
                    lsbooks.append([b])
        cbbook.set_model(lsbooks)
        self.bookNoUpdate = False

    def getConfigList(self, prjid):
        res = [""]
        if self.prjid is None:
            return res
        root = os.path.join(self.settings_dir, prjid, "shared", "ptxprint")
        if os.path.exists(root):
            for s in os.scandir(root):
                if s.is_dir and os.path.exists(os.path.join(root, s.name, "ptxprint.cfg")):
                    res.append(s.name)
        return res

    def updateSavedConfigList(self):
        self.configNoUpdate = True
        currConf = self.builder.get_object("t_savedConfig").get_text()
        self.cb_savedConfig.remove_all()
        savedConfigs = self.getConfigList(self.prjid)
        if len(savedConfigs):
            for cfgName in sorted(savedConfigs):
                self.cb_savedConfig.append_text(cfgName)
            try:
                self.builder.get_object("t_savedConfig").set_text(currConf)
            except:
                self.cb_savedConfig.set_active(0)
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
            self.ecb_diglotSecConfig.set_active_id("")

    def loadConfig(self, config):
        super(GtkViewModel, self).loadConfig(config)
        for k, v in _sensitivities.items():
            state = self.get(k)
            for w in v:
                self.builder.get_object(w).set_sensitive(state)
        for k, v in _nonsensitivities.items():
            state = not self.get(k)
            for w in v:
                self.builder.get_object(w).set_sensitive(state)

    def sensiVisible(self, k, focus=False):
        state = self.get(k)
        try:
            for w in _sensitivities[k]:
                self.builder.get_object(w).set_sensitive(state)
        except KeyError:
            pass
        if k in _nonsensitivities.keys():
            for w in _nonsensitivities[k]:
                self.builder.get_object(w).set_sensitive(not state)
        if k in _visibilities.keys():
            for w in _visibilities[k]:
                self.builder.get_object(w).set_visible(state)
        if focus:
            self.builder.get_object(_sensitivities[k][0]).grab_focus()
        return state

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
            self.onSaveConfig(None)
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
            lockBtn.set_label("Lock Config")
        else:
            status = False
            lockBtn.set_label("Unlock Config")
        for c in ["btn_saveConfig", "btn_deleteConfig", "t_configNotes", "c_hideAdvancedSettings"]:
            self.builder.get_object(c).set_sensitive(status)
        
    def onPrevBookClicked(self, btn_NextBook):
        bks = self.getBooks()
        ndx = 0
        try:
            ndx = bks.index(self.get("ecb_examineBook"))
        except ValueError:
            self.builder.get_object("ecb_examineBook").set_active_id(bks[0])
        if ndx > 0:
            self.builder.get_object("ecb_examineBook").set_active_id(bks[ndx-1])
            self.builder.get_object("btn_NextBook").set_sensitive(True)
            if ndx == 1:
                self.builder.get_object("btn_PrevBook").set_sensitive(False)
        else:
            self.builder.get_object("btn_PrevBook").set_sensitive(False)
    
    def onNextBookClicked(self, btn_NextBook):
        bks = self.getBooks()
        ndx = 0
        try:
            ndx = bks.index(self.get("ecb_examineBook"))
        except ValueError:
            self.builder.get_object("ecb_examineBook").set_active_id(bks[0])
        if ndx < len(bks)-1:
            self.builder.get_object("ecb_examineBook").set_active_id(bks[ndx+1])
            self.builder.get_object("btn_PrevBook").set_sensitive(True)
            if ndx == len(bks)-2:
                self.builder.get_object("btn_NextBook").set_sensitive(False)
        else:
            self.builder.get_object("btn_NextBook").set_sensitive(False)
    
    def onExamineBookChanged(self, cb_examineBook):
        if self.bookNoUpdate == True:
            return
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        self.onViewerChangePage(None,None,pg)

    def onBookSelectorChange(self, btn):
        status = self.sensiVisible("c_multiplebooks")
        self.set("c_prettyIntroOutline", False)
        if status and self.get("t_booklist") == "" and self.prjid is not None:
            self.updateDialogTitle()
            # pass
            # self.onChooseBooksClicked(None)
        else:
            toc = self.builder.get_object("c_autoToC") # Ensure that we're not trying to build a ToC for a single book!
            toc.set_sensitive(status)
            if not status:
                toc.set_active(False)
            self.updateDialogTitle()
            bks = self.getBooks()
            if len(bks) > 1:
                self.builder.get_object("ecb_examineBook").set_active_id(bks[0])

    def onGenerateClicked(self, btn):
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        if pg == 1: # PicList
            bks2gen = self.getBooks()
            if not self.get('c_multiplebooks') and self.get("ecb_examineBook") != bks2gen[0]: 
                self.generatePicList([self.get("ecb_examineBook")])
            else:
                self.generatePicList(bks2gen)
        elif pg == 2: # AdjList
            self.generateAdjList()
        self.onViewerChangePage(None,None,pg)

    def onRefreshViewerTextClicked(self, btn):
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        self.onViewerChangePage(None, None, pg)

    def onViewerChangePage(self, nbk_Viewer, scrollObject, pgnum):
        self.bookNoUpdate = True
        self.builder.get_object("gr_editableButtons").set_sensitive(False)
        prjid = self.get("fcb_project")
        prjdir = os.path.join(self.settings_dir, prjid)
        bks = self.getBooks()
        bk = self.get("ecb_examineBook")
        genBtn = self.builder.get_object("btn_Generate")
        genBtn.set_sensitive(False)
        genBtn.set_label("Generate")
        self.builder.get_object("c_randomPicPosn").set_sensitive(False)
        if bk == None or bk == "":
            bk = bks[0]
            self.builder.get_object("ecb_examineBook").set_active_id(bk)
        for o in ("l_examineBook", "btn_PrevBook", "ecb_examineBook", "btn_NextBook", "btn_Generate"):
            self.builder.get_object(o).set_sensitive( 0 <= pgnum <= 2)

        if len(bks) == 1:
            self.builder.get_object("btn_PrevBook").set_sensitive(False)
            self.builder.get_object("btn_NextBook").set_sensitive(False)
            
        fndict = {0 : ("", ""),     1 : ("PicLists", ".piclist"), 2 : ("AdjLists", ".adj"), \
                  3 : ("", ".tex"), 4 : ("", ".log")}
        if pgnum <= 2:  # (SFM,PicList,AdjList)
            fname = self.getBookFilename(bk, prjid)
            if pgnum == 0:
                fpath = os.path.join(self.working_dir, fndict[pgnum][0], fname)
                self.builder.get_object("btn_Generate").set_sensitive(False)
            else:
                fpath = os.path.join(self.configPath(), fndict[pgnum][0], fname)
            doti = fpath.rfind(".")
            if doti > 0:
                fpath = fpath[:doti] + "-draft" + fpath[doti:] + fndict[pgnum][1]
            if pgnum == 1: # PicList
                self.builder.get_object("c_randomPicPosn").set_sensitive(True)
                genTip = "Generate the PicList in the\ncorrect format using the markup\n(\\fig ... \\fig*) within the text."
                genBtn.set_sensitive(True)
                genBtn.set_tooltip_text(genTip)
            elif pgnum == 2: # AdjList
                genTip = "Generate a list of paragraphs\nthat may be adjusted (using\nshrink or expand values)."
                genBtn.set_sensitive(True)
                genBtn.set_tooltip_text(genTip)
            if os.path.exists(fpath):
                genBtn.set_label("Regenerate")

        elif 3 <= pgnum <= 4:  # (TeX,Log)
            if len(bks) > 1:
                fname = "ptxprint-{}_{}{}{}".format(bks[0], bks[-1], prjid, fndict[pgnum][1])
            else:
                fname = "ptxprint-{}{}{}".format(bks[0], prjid, fndict[pgnum][1])
            fpath = os.path.join(self.working_dir, fname)

        elif pgnum == 5: # View/Edit one of the 4 Settings files
            fpath = self.builder.get_object("l_{}".format(pgnum)).get_tooltip_text()
            if fpath == None:
                self.fileViews[pgnum][0].set_text("\n Use the 'Advanced' tab to select which settings you want to view or edit.")
                self.builder.get_object("l_{}".format(pgnum)).set_text("Settings")
                return

        elif pgnum == 6: # Just show the Folders & Links page
            self.builder.get_object("l_{}".format(pgnum)).set_text("Folders & Links")
            return
        else:
            return
        if os.path.exists(fpath):
            if 1 <= pgnum <= 2 or pgnum == 5:
                self.builder.get_object("gr_editableButtons").set_sensitive(True)
            self.builder.get_object("l_{}".format(pgnum)).set_tooltip_text(fpath)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as inf:
                txt = inf.read()
                if len(txt) > 60000:
                    txt = txt[:60000]+"\n\n------------------------------------- \
                                          \n[Display of file has been truncated] \
                                          \nClick on View/Edit... button to see more."
            self.fileViews[pgnum][0].set_text(txt)
        else:
            self.builder.get_object("l_{}".format(pgnum)).set_tooltip_text(None)
            self.fileViews[pgnum][0].set_text("\nThis file doesn't exist yet.\n\nTry... \
                                               \n   * Check option (above) to 'Preserve Intermediate Files and Logs' \
                                               \n   * Generate the PiCList or AdjList \
                                               \n   * Click 'Print' to create the PDF")
        self.bookNoUpdate = False

    def onSaveEdits(self, btn):
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        buf = self.fileViews[pg][0]
        fpath = self.builder.get_object("l_{}".format(pg)).get_tooltip_text()
        text2save = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        openfile = open(fpath,"w", encoding="utf-8")
        openfile.write(text2save)
        openfile.close()

    def onOpenInSystemEditor(self, btn):
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        fpath = self.builder.get_object("l_{}".format(pg)).get_tooltip_text() or ""
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
        pangostr = "{} {} {}".format(name, style, fsize)
        p = Pango.font_description_from_string(pangostr)
        for w in ("t_clHeading", "t_tocTitle", "ecb_ftrcenter", "scroll_FinalSFM", "scroll_PicList"):   # "t_runningFooter",
            self.builder.get_object(w).modify_font(p)

    def updateFakeLabels(self):
        status = self.get("c_fakebold") or self.get("c_fakeitalic") or self.get("c_fakebolditalic")
        for c in ("l_embolden", "l_slant"):
            self.builder.get_object(c).set_sensitive(status)

    def onFakeboldClicked(self, btn):
        self.sensiVisible("c_fakebold")
        self.updateFakeLabels()
        
    def onFakeitalicClicked(self, btn):
        self.sensiVisible("c_fakeitalic")
        self.updateFakeLabels()

    def onFakebolditalicClicked(self, btn):
        self.sensiVisible("c_fakebolditalic")
        self.updateFakeLabels()

    def onVariableLineSpacingClicked(self, btn):
        self.sensiVisible("c_variableLineSpacing")
        lnspVal = round(self.get("s_linespacing"), 1)
        minVal = round(self.get("s_linespacingmin"), 1)
        maxVal = round(self.get("s_linespacingmax"), 1)
        status = self.get("c_variableLineSpacing")
        if status and lnspVal == minVal and lnspVal == maxVal:
            self.set("s_linespacingmin", lnspVal - 1)
            self.set("s_linespacingmax", lnspVal + 2)

    def onVerticalRuleClicked(self, btn):
        self.sensiVisible("c_verticalrule")

    def onMarginalVersesClicked(self, btn):
        self.sensiVisible("c_marginalverses")

    def onOmitSectHeadsClicked(self, btn):
        status = self.get("c_omitSectHeads")
        self.builder.get_object("c_omitParallelRefs").set_sensitive(not status)
        self.builder.get_object("c_omitParallelRefs").set_active(status)

    def onHyphenateClicked(self, btn):
        if self.prjid is not None:
            fname = os.path.join(self.settings_dir, self.prjid, "shared", "ptxprint", 'hyphen-{}.tex'.format(self.prjid))
        
    def onUseIllustrationsClicked(self, btn):
        self.sensiVisible("c_includeillustrations")

    def onUseCustomFolderclicked(self, btn):
        status = self.sensiVisible("c_useCustomFolder")
        if not status:
            self.builder.get_object("c_exclusiveFiguresFolder").set_active(status)

    def onBlendedXrsClicked(self, btn):
        self.sensiVisible("c_blendfnxr")
    
    def onUseChapterLabelclicked(self, btn):
        self.sensiVisible("c_useChapterLabel")
        
    def onClickedIncludeFootnotes(self, btn):
        self.sensiVisible("c_includeFootnotes")
        
    def onClickedIncludeXrefs(self, btn):
        self.sensiVisible("c_includeXrefs")

    def onPageNumTitlePageChanged(self, btn):
        if self.get("c_pageNumTitlePage"):
            self.builder.get_object("c_printConfigName").set_active(False)

    def onPrintConfigNameChanged(self, btn):
        if self.get("c_printConfigName"):
            self.builder.get_object("c_pageNumTitlePage").set_active(False)

    def onPageGutterChanged(self, btn):
        self.sensiVisible("c_pagegutter", focus=True)

    def onDoubleColumnChanged(self, btn):
        self.sensiVisible("c_doublecolumn")

    def onOmitrhchapnumClicked(self, btn):
        self.sensiVisible("c_omitrhchapnum")

    def onHdrVersesClicked(self, btn):
        self.sensiVisible("c_hdrverses")

    def onUseFallbackFontchanged(self, btn):
        self.sensiVisible("c_useFallbackFont")

    def onUsePicListChanged(self, btn):
        self.sensiVisible("c_usePicList")

    def onFigsChanged(self, btn):
        self.sensiVisible("c_includefigsfromtext")

    def onInclFrontMatterChanged(self, btn):
        self.sensiVisible("c_inclFrontMatter")

    def onInclBackMatterChanged(self, btn):
        self.sensiVisible("c_inclBackMatter")

    def onApplyWatermarkChanged(self, btn):
        self.sensiVisible("c_applyWatermark")
    
    def onInclPageBorderChanged(self, btn):
        self.sensiVisible("c_inclPageBorder")

    def onInclSectionHeaderChanged(self, btn):
        self.sensiVisible("c_inclSectionHeader")

    def onInclVerseDecoratorChanged(self, btn):
        self.sensiVisible("c_inclVerseDecorator")
    
    def onAutoTocChanged(self, btn):
        self.sensiVisible("c_autoToC", focus=True)

    def onSpacingClicked(self, btn):
        self.sensiVisible("c_spacing")

    def onLineBreakChanged(self, btn):
        self.sensiVisible("c_linebreakon", focus=True)
            
    def onFnCallersChanged(self, btn):
        self.sensiVisible("c_fnautocallers", focus=True)
            
    def onResetFNcallersClicked(self, btn_resetFNcallers):
        self.builder.get_object("t_fncallers").set_text(re.sub(" ", ",", self.ptsettings['footnotes']))
        
    def onResetXRcallersClicked(self, btn_resetXRcallers):
        self.builder.get_object("t_xrcallers").set_text(re.sub(" ", ",", self.ptsettings['crossrefs']))
        
    def onXrCallersChanged(self, btn):
        self.sensiVisible("c_xrautocallers", focus=True)

    def onRHruleChanged(self, btn):
        self.sensiVisible("c_rhrule", focus=True)

    def onProcessScriptClicked(self, btn):
        status = self.sensiVisible("c_processScript")
        if not status:
            self.builder.get_object("btn_editScript").set_sensitive(False)
        else:
            if self.get("btn_selectScript") != None:
                self.builder.get_object("btn_editScript").set_sensitive(True)

    def onUsePrintDraftChangesClicked(self, btn):
        self.sensiVisible("c_usePrintDraftChanges")
        
    def onUseModsTexClicked(self, btn):
        self.sensiVisible("c_useModsTex")
        
    def onUseCustomStyClicked(self, btn):
        self.sensiVisible("c_useCustomSty")
        
    def onUseModsStyClicked(self, btn):
        self.sensiVisible("c_useModsSty")
        
    def onOmitOutlineClicked(self, btn):
        self.sensiVisible("c_omitIntroOutline")
        self.builder.get_object("c_prettyIntroOutline").set_active(False)

    def onShowLayoutTabClicked(self, btn):
        self.sensiVisible("c_showLayoutTab")

    def onShowBodyTabClicked(self, btn):
        self.sensiVisible("c_showBodyTab")

    def onShowHeadFootTabClicked(self, btn):
        self.sensiVisible("c_showHeadFootTab")

    def onShowPicturesTabClicked(self, btn):
        self.sensiVisible("c_showPicturesTab")

    def onShowAdvancedTabClicked(self, btn):
        self.sensiVisible("c_showAdvancedTab")

    def onShowViewerTabClicked(self, btn):
        self.sensiVisible("c_showViewerTab")

    def onShowDiglotTabClicked(self, btn):
        self.sensiVisible("c_showDiglotTab")

    def onShowBordersTabClicked(self, btn):
        self.sensiVisible("c_showBordersTab")

    def onKeepTemporaryFilesClicked(self, c_keepTemporaryFiles):
        dir = self.working_dir
        self.builder.get_object("gr_debugTools").set_sensitive(self.get("c_keepTemporaryFiles"))
        if self.builder.get_object("nbk_Main").get_current_page() == 7:
            if not self.get("c_keepTemporaryFiles"):
                title = "Remove Intermediate Files and Logs?"
                question = "Are you sure you want to delete\nALL the temporary PTXprint files?"
                if self.msgQuestion(title, question):
                    patterns = []
                    for extn in ('delayed','parlocs','notepages', 'log'):
                        patterns.append(r".+\.{}".format(extn))
                    patterns.append(r".+\-draft\....".format(extn))
                    patterns.append(r".+\.toc".format(extn))
                    patterns.append(r"NestedStyles\.sty".format(extn))
                    patterns.append(r"ptxprint\-.+\.tex".format(extn))
                    # print(patterns)
                    for pattern in patterns:
                        for f in os.listdir(dir):
                            if re.search(pattern, f):
                                try:
                                    os.remove(os.path.join(dir, f))
                                except OSError:
                                    self.doError("Warning: Could not delete temporary file.", secondary = "File: " + delfname)
                    for p in ["tmpPics", "tmpPicLists", "PicLists", "AdjLists"]:
                        path2del = os.path.join(dir, p)
                        # Make sure we're not deleting something closer to Root!
                        if len(path2del) > 30 and os.path.exists(path2del):
                            try:
                                rmtree(path2del)
                            except OSError:
                                print("Error Deleting temporary folder: {}".format(path2del))

    def onFontRclicked(self, btn):
        self.getFontNameFace("bl_fontR")
        self.onFontChanged(btn)
        
    def onFontBclicked(self, btn):
        self.getFontNameFace("bl_fontB")
        
    def onFontIclicked(self, btn):
        self.getFontNameFace("bl_fontI")
        
    def onFontBIclicked(self, btn):
        self.getFontNameFace("bl_fontBI")
        
    # def onFontExtraRclicked(self, btn):
        # self.getFontNameFace("bl_fontExtraR")
        
    def onVerseNumFontClicked(self, btn):
        self.getFontNameFace("bl_verseNumFont")
        
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

    def getFontNameFace(self, btnid):
        btn = self.builder.get_object(btnid)
        lb = self.builder.get_object("tv_fontFamily")
        lb.set_cursor(0)
        dialog = self.builder.get_object("dlg_fontChooser")
        self.builder.get_object("t_fontSearch").set_text("")
        self.builder.get_object("t_fontSearch").has_focus()
        # dialog.set_default_response(Gtk.ResponseType.OK)
        dialog.set_keep_above(True)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            sel = lb.get_selection()
            ls, row = sel.get_selected()
            name = ls.get_value(row, 0)
            cb = self.builder.get_object("fcb_fontFaces")
            style = cb.get_model()[cb.get_active()][0]
            if style == "Regular":
                style = ""
            self.setFontButton(btn, name, style)
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
        self.builder.get_object("c_multiplebooks").set_active(not booklist == [])
        self.set("c_prettyIntroOutline", False)
        self.updateDialogTitle()
        bks = self.getBooks()
        if len(bks) > 1:
            self.builder.get_object("ecb_examineBook").set_active_id(bks[0])
        dialog.set_keep_above(False)
        dialog.hide()

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
        if self.bookNoUpdate == True:
            return
        self.bk = self.get("ecb_book")
        self.set("c_prettyIntroOutline", False)
        if self.bk != "":
            self.chs = int(chaps.get(str(self.bk)))
            self.chapfrom = self.builder.get_object("ls_chapfrom")
            self._setchap(self.chapfrom, 1, self.chs)
            self.fcb_chapfrom.set_active_id('1')
        
            self.chapto = self.builder.get_object("ls_chapto")
            self._setchap(self.chapto, 1, self.chs)
            self.fcb_chapto.set_active_id(str(self.chs))
            self.builder.get_object("ecb_examineBook").set_active_id(self.bk)
        self.updateDialogTitle()

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

    def setPrjid(self, prjid, saveCurrConfig=False):
        if not self.initialised:
            self.pendingPid = prjid
        else:
            self.set("fcb_project", prjid)

    def setConfigId(self, configid, saveCurrConfig=False):
        if not self.initialised:
            self.pendingConfig = configid
        else:
            self.set("ecb_savedConfig", configid)

    def onProjectChange(self, cb_prj):
        self.updatePrjLinks()
        self.builder.get_object("btn_saveConfig").set_sensitive(False)
        self.builder.get_object("btn_deleteConfig").set_sensitive(False)
        lockBtn = self.builder.get_object("btn_lockunlock")
        lockBtn.set_label("Lock Config")
        lockBtn.set_sensitive(False)
        self.updateProjectSettings(None, saveCurrConfig=True)
        self.updateSavedConfigList()
        for o in ["b_print", "bx_SavedConfigSettings", "tb_Layout", "tb_Body", "tb_HeadFoot", "tb_Pictures",
                  "tb_Advanced", "tb_Logging", "tb_ViewerEditor", "tb_Diglot", "tb_FancyBorders"]:
            self.builder.get_object(o).set_sensitive(True)
        self.updateFonts()

    def updatePrjLinks(self):
        if self.settings_dir != None and self.prjid != None:
            self.builder.get_object("lb_prjdir").set_label(os.path.join(self.settings_dir, self.prjid))
            self.builder.get_object("lb_settings_dir").set_label(self.configPath() or "")
            self.builder.get_object("lb_working_dir").set_label(self.working_dir or "")
            
    def updateProjectSettings(self, prjid, saveCurrConfig=False, configName=None):
        if not super(GtkViewModel, self).updateProjectSettings(prjid, saveCurrConfig=saveCurrConfig, configName=configName):
            for fb in ['bl_fontR', 'bl_fontB', 'bl_fontI', 'bl_fontBI', 'bl_fontExtraR', 'bl_verseNumFont']:  # 
                fblabel = self.builder.get_object(fb).set_label("Select font...")
        if self.prjid:
            self.builder.get_object("ecb_book").set_active(0)
            self.updatePrjLinks()
        status = self.get("c_multiplebooks")
        for c in ("c_combine", "t_booklist"):
            self.builder.get_object(c).set_sensitive(status)
        toc = self.builder.get_object("c_autoToC") # Ensure that we're not trying to build a ToC for a single book!
        toc.set_sensitive(status)
        if not status:
            toc.set_active(False)
        for c in ("l_singlebook", "ecb_book", "l_chapfrom", "fcb_chapfrom", "l_chapto", "fcb_chapto"):
            self.builder.get_object(c).set_sensitive(not status)
        for i in range(0,6):
            self.builder.get_object("l_{}".format(i)).set_tooltip_text(None)
        self.updatePrjLinks()
        self.setEntryBoxFont()
        self.updateDialogTitle()

    def onConfigNameChanged(self, cb_savedConfig):
        if self.configNoUpdate:
            return
        self.builder.get_object("c_hideAdvancedSettings").set_sensitive(True)
        if len(self.get("ecb_savedConfig")):
            lockBtn = self.builder.get_object("btn_lockunlock")
            lockBtn.set_label("Lock Config")
            lockBtn.set_sensitive(True)
            self.builder.get_object("t_invisiblePassword").set_text("")
            self.builder.get_object("btn_saveConfig").set_sensitive(True)
            self.builder.get_object("btn_deleteConfig").set_sensitive(True)
            if os.path.exists(self.configPath(cfgname=self.get("ecb_savedConfig"))):
                self.updateProjectSettings(self.prjid, saveCurrConfig=False, configName=self.get("ecb_savedConfig")) # False means DON'T Save!
        else:
            self.config_dir = self.configPath()
            self.builder.get_object("t_configNotes").set_text("")
            lockBtn = self.builder.get_object("btn_lockunlock")
            lockBtn.set_label("Lock Config")
            lockBtn.set_sensitive(False)
            self.builder.get_object("t_invisiblePassword").set_text("")
            self.builder.get_object("l_settings_dir").set_label(self.config_dir or "")
            self.builder.get_object("btn_saveConfig").set_sensitive(False)
            self.builder.get_object("btn_deleteConfig").set_sensitive(False)
        self.updateDialogTitle()

    def updateFonts(self):
        if self.ptsettings is None:
            return
        ptfont = self.ptsettings['DefaultFont']
        for fb in ['bl_fontR', 'bl_verseNumFont']:  # 'bl_fontB', 'bl_fontI', 'bl_fontBI', 'bl_fontExtraR'
            fblabel = self.builder.get_object(fb).get_label()
            if fblabel == "Select font...":
                w = self.builder.get_object(fb)
                self.setFontButton(w, ptfont, "")
                self.onFontChanged(w)

    def updateDialogTitle(self):
        titleStr = super(GtkViewModel, self).getDialogTitle()
        self.builder.get_object("ptxprint").set_title(titleStr)

    def editFile(self, file2edit, loc="wrk"):
        pgnum = 5
        self.builder.get_object("nbk_Main").set_current_page(7)
        self.builder.get_object("nbk_Viewer").set_current_page(pgnum)
        self.prjid = self.get("fcb_project")
        self.prjdir = os.path.join(self.settings_dir, self.prjid)
        if loc == "wrk":
            fpath = os.path.join(self.working_dir, file2edit)
        elif loc == "prj":
            fpath = os.path.join(self.settings_dir, self.prjid, file2edit)
        elif loc == "cfg":
            fpath = os.path.join(self.configPath(), file2edit)
            if not os.path.exists(fpath):
                fpath = os.path.join(self.settings_dir, self.prjid, "shared", "ptxprint", file2edit)
        elif "\\" in loc or "/" in loc:
            fpath = os.path.join(loc, file2edit)
        else:
            return
        self.builder.get_object("gr_editableButtons").set_sensitive(True)
        self.builder.get_object("l_{}".format(pgnum)).set_text(file2edit)
        self.builder.get_object("l_{}".format(pgnum)).set_tooltip_text(fpath)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as inf:
                txt = inf.read()
                # if len(txt) > 32000:
                    # txt = txt[:32000]+"\n\n etc...\n\n"
            self.fileViews[pgnum][0].set_text(txt)
        else:
            self.fileViews[pgnum][0].set_text("\nThis file doesn't exist yet!\n\nEdit here and Click 'Save' to create it.")

    def onEditScriptFile(self, btn):
        # Ask MH how to do this properly (in one line!?) with Path from pathlib
        customScriptFPath = self.get("btn_selectScript")
        scriptName = os.path.basename(customScriptFPath)
        scriptPath = customScriptFPath[:-len(scriptName)]
        if len(customScriptFPath):
            self.editFile(scriptName, scriptPath)

    def onEditChangesFile(self, btn):
        self.editFile("PrintDraftChanges.txt", "prj")

    def onEditModsTeX(self, btn):
        modfname = "ptxprint-mods.tex"
        self.prjid = self.get("fcb_project")
        fpath = os.path.join(self.settings_dir, self.prjid, "shared", "ptxprint", modfname)
        if not os.path.exists(fpath):
            openfile = open(fpath,"w", encoding="utf-8")
            openfile.write("% This is the .tex file specific for the {} project used by PTXprint.\n".format(self.prjid))
            openfile.close()
        self.editFile(modfname, "cfg")

    def onEditCustomSty(self, btn):
        self.editFile("custom.sty", "prj")

    def onEditModsSty(self, btn):
        self.editFile("PrintDraft-mods.sty", "wrk")

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

    def onSelectFigureFolderClicked(self, btn_selectFigureFolder):
        customFigFolder = self.fileChooser("Select the folder containing image files", 
                filters = None, multiple = False, folder = True)
        if len(customFigFolder):
            self.customFigFolder = customFigFolder[0]
            btn_selectFigureFolder.set_tooltip_text(str(customFigFolder[0]))
            self.builder.get_object("c_useCustomFolder").set_active(True)
        else:
            self.customFigFolder = None
            btn_selectFigureFolder.set_tooltip_text("")
            self.builder.get_object("c_useCustomFolder").set_active(False)
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
        self._onPDFClicked("Select one or more PDF(s) for FRONT matter", 
                False, self.working_dir, "inclFrontMatter", "FrontPDFs", btn_selectFrontPDFs)

    def onBackPDFsClicked(self, btn_selectBackPDFs):
        self._onPDFClicked("Select one or more PDF(s) for BACK matter", 
                False, self.working_dir, "inclBackMatter", "BackPDFs", btn_selectBackPDFs)

    def onWatermarkPDFclicked(self, btn_selectWatermarkPDF):
        self._onPDFClicked("Select Watermark PDF file", True,
                os.path.join(os.path.dirname(__file__), "PDFassets", "watermarks"),
                "applyWatermark", "watermarks", btn_selectWatermarkPDF)

    def onPageBorderPDFclicked(self, btn_selectPageBorderPDF):
        self._onPDFClicked("Select Page Border PDF file", True,
                os.path.join(os.path.dirname(__file__), "PDFassets", "border-art"),
                "inclPageBorder", "pageborder", btn_selectPageBorderPDF)

    def onSectionHeaderPDFclicked(self, btn_selectSectionHeaderPDF):
        self._onPDFClicked("Select Section Header PDF file", True,
                os.path.join(os.path.dirname(__file__), "PDFassets", "border-art"),
                "inclSectionHeader", "sectionheader", btn_selectSectionHeaderPDF)

    def onVerseDecoratorPDFclicked(self, btn_selectVerseDecoratorPDF):
        self._onPDFClicked("Select Verse Decorator PDF file", True,
                os.path.join(os.path.dirname(__file__), "PDFassets", "border-art"),
                "inclVerseDecorator", "versedecorator", btn_selectVerseDecoratorPDF)

    def onEditAdjListClicked(self, btn_editParaAdjList):
        pgnum = 2
        self.builder.get_object("nbk_Main").set_current_page(7)
        self.builder.get_object("nbk_Viewer").set_current_page(pgnum)
        self.onViewerChangePage(None,None,pgnum)

    def onEditPicListClicked(self, btn_editPicList):
        pgnum = 1
        self.builder.get_object("c_usePicList").set_active(True)
        self.builder.get_object("nbk_Main").set_current_page(7)
        self.builder.get_object("nbk_Viewer").set_current_page(pgnum)
        self.onViewerChangePage(None,None,pgnum)
    
    def ontv_sizeallocate(self, atv, dummy):
        b = atv.get_buffer()
        it = b.get_iter_at_offset(-1)
        atv.scroll_to_iter(it, 0, False, 0, 0)

    def fileChooser(self, title, filters=None, multiple=True, folder=False, basedir=None):
        dialog = Gtk.FileChooserDialog(title, None,
            (Gtk.FileChooserAction.SELECT_FOLDER if folder else Gtk.FileChooserAction.OPEN),
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            ("Select" if folder else Gtk.STOCK_OPEN), Gtk.ResponseType.OK))
        dialog.set_default_size(730, 565)
        dialog.set_select_multiple(multiple)
        if basedir is not None:
            dialog.set_current_folder(basedir)
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

        dialog.set_keep_above(True)
        response = dialog.run()
        fcFilepath = None
        if response == Gtk.ResponseType.OK:
            if folder:
                fcFilepath = [Path(dialog.get_filename()+"/")]
            else:
                fcFilepath = [Path(x) for x in dialog.get_filenames()]
        dialog.set_keep_above(False)
        dialog.destroy()
        return fcFilepath

    def onDiglotClicked(self, btn):
        self.ondiglotAlignmentChanged(None)
        self.sensiVisible("c_diglot")

    def ondiglotSecProjectChanged(self, btn):
        self.updateDiglotConfigList()
        
    def onGenerateHyphenationListClicked(self, btn):
        self.generateHyphenationFile()

    def onPrettyIntroOutlineClicked(self, btn):
        if self.get("c_prettyIntroOutline"): # if turned on...
            badbks = self.checkSFMforFancyIntroMarkers()
            if len(badbks):
                self.set("c_prettyIntroOutline", False)
                m1 = "Invalid Option for Selected Books"
                m2 = "The book(s) listed below do not have the" + \
                   "\nrequired markup for this feature to be enabled." + \
                   "\n(Refer to Tooltip for further details.)" + \
                   "\n\n{}".format(", ".join(badbks))
                self.doError(m1, m2)

    def onFindMissingCharsClicked(self, btn_findMissingChars):
        missing = super(GtkViewModel, self).onFindMissingCharsClicked(btn_findMissingChars)
        missingcodes = " ".join(repr(c.encode('raw_unicode_escape'))[2:-1].replace("\\\\","\\") for c in missing)
        self.builder.get_object("t_missingChars").set_tooltip_text(missingcodes)
        if len(missing):
            self.set("c_useFallbackFont", True)
        else:
            self.set("c_useFallbackFont", False)
            self.builder.get_object("gr_fallbackFont").set_sensitive(False)
            self.doError("FYI: The Regular font already supports all the characters in the text.",
                    "A fallback font is not required so\nthe 'Use Fallback Font' option has been disabled.")

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

    def onEnableDecorativeElementsClicked(self, btn):
        self.sensiVisible("c_borders")

    def ondiglotAlignmentChanged(self, btn):
        if self.get("fcb_diglotAlignment").startswith("Align") and self.get("c_diglot"):
            self.set("c_diglotAutoAligned", True)
        else:
            self.set("c_diglotAutoAligned", False)

    def onOpenFolderPrjDirClicked(self, btn):
        print("Clicked something")
        self.openFolder(os.path.join(self.settings_dir, self.prjid))
        
    def onOpenFolderConfClicked(self, btn):
        print("Clicked something")
        self.openFolder(self.configPath())
        
    def onOpenFolderOutputClicked(self, btn):
        print("Clicked something")
        self.openFolder(self.working_dir)
        
    def openFolder(self, fldrpath):
        path = os.path.realpath(fldrpath)
        os.startfile(fldrpath)

    def onURLhomepageClicked(self, btn):
        self.openURL("https://software.sil.org/ptxprint/")
        
    def onURLsumatraClicked(self, btn):
        self.openURL("https://www.sumatrapdfreader.org/download-free-pdf-viewer.html")
        
    def onURLptx2pdfFAQClicked(self, btn):
        self.openURL("https://github.com/sillsdev/ptx2pdf/blob/master/docs/documentation/ptx2pdf-faq.md")
        
    def onURLgithubIssueClicked(self, btn):
        self.openURL("https://github.com/sillsdev/ptx2pdf/issues/new")
        
    def openURL(self, url):
        if sys.platform == "win32":
            os.system("start \"\" {}".format(url))
        elif sys.platform == "linux":
            os.system("xdg-open \"\" {}".format(url))
