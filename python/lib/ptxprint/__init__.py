#!/usr/bin/python3

import sys, os, re, regex, gi, random, subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import xml.etree.ElementTree as et
from ptxprint.font import TTFont
from ptxprint.runner import StreamTextBuffer
from ptxprint.ptsettings import ParatextSettings, allbooks, books, chaps
from ptxprint.info import Info
# from PIL import Image
import configparser
import traceback

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
_alldigits = [ "Default", "Adlam", "Ahom", "Arabic-Farsi", "Arabic-Hindi", "Balinese", "Bengali", "Bhaiksuki", "Brahmi", "Burmese", 
    "Chakma", "Cham", "Devanagari", "Gujarati", "Gunjala-Gondi", "Gurmukhi", "Gurmukhi", "Hanifi-Rohingya", "Javanese", "Kannada", 
    "Kayah-Li", "Khmer", "Khudawadi", "Lao", "Lepcha", "Limbu", "Malayalam", "Masaram-Gondi", "Meetei-Mayek", "Modi", "Mongolian", 
    "Mro", "Myanmar", "Myanmar-Shan", "Myanmar-Tai-Laing", "New-Tai-Lue", "Newa", "Nko", "Nyiakeng-Puachue-Hmong", "Ol-Chiki", "Oriya", 
    "Osmanya", "Pahawh-Hmong", "Persian", "Saurashtra", "Sharada", "Sinhala-Lith", "Sora-Sompeng", "Sundanese", "Tai-Tham-Hora", 
    "Tai-Tham-Tham", "Takri", "Tamil", "Telugu", "Thai", "Tibetan", "Tirhuta", "Urdu", "Vai", "Wancho", "Warang-Citi" ]


class PtxPrinterDialog:
    def __init__(self, allprojects, settings_dir):
        # print(" init: __init__",self, allprojects, settings_dir)
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(os.path.dirname(__file__), "ptxprint.glade"))
        self.builder.connect_signals(self)
        self.addCR("cb_digits", 0)
        self.addCR("cb_script", 0)
        self.addCR("cb_chapfrom", 0)
        self.addCR("cb_chapto", 0)
        self.addCR("cb_blendedXrefCaller", 0)
        self.addCR("cb_glossaryMarkupStyle", 0)
        # self.addCR("cb_diglotPriProject", 0)
        # self.addCR("cb_diglotSecProject", 0)

        scripts = self.builder.get_object("ls_scripts")
        scripts.clear()
        for k, v in _allscripts.items():
            scripts.append([v, k])
        self.cb_script.set_active_id('Zyyy')

        digits = self.builder.get_object("ls_digits")
        digits.clear()
        for d in _alldigits: # .items():
            digits.append([d])
        self.cb_digits.set_active_id(_alldigits[0])

        # glostyle = self.builder.get_object("ls_glossaryMarkupStyle")
        # glostyle.clear()
        # for g in Info._glossarymarkup.keys():
            # try:
                # print(g)
            # except UnicodeEncodeError:
                # pass
            # glostyle.append([g])

        dia = self.builder.get_object("dlg_multiBookSelector")
        dia.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        self.logbuffer = StreamTextBuffer()
        self.builder.get_object("tv_logging").set_buffer(self.logbuffer)
        self.mw = self.builder.get_object("ptxprint")
        self.projects = self.builder.get_object("ls_projects")
        self.info = None
        self.settings_dir = settings_dir
        self.ptsettings = None
        self.booklist = []
        self.CustomScript = None
        self.FrontPDFs = None
        self.BackPDFs = None
        self.watermarks = None
        self.customFigFolder = None
        self.prjid = None
        for p in sorted(allprojects, key = lambda s: s.casefold()):
            self.projects.append([p])

    def run(self, callback):
        # print(" init: run",callback)
        self.callback = callback
        self.mw.show_all()
        self.onHideAdvancedSettingsClicked(None)
        Gtk.main()

    def enableExperimental(self):
        pass
        
    def addCR(self, name, index):
        # print(" init: addCR",self, name, index)
        v = self.builder.get_object(name)
        setattr(self, name, v)
        c = Gtk.CellRendererText()
        v.pack_start(c, True)
        v.add_attribute(c, "text", index)

    def parse_fontname(self, font):
        # print(" init: parse_fontname",self, font)
        m = re.match(r"^(.*?)(\d+(?:\.\d+)?)$", font)
        if m:
            return [m.group(1), int(m.group(2))]
        else:
            return [font, 0]

    def get(self, wid, sub=0, asstr=False):
        # print(" init: get",self, wid, "sub=0, asstr=False")
        w = self.builder.get_object(wid)
        v = ""
        if wid.startswith("cb_"):
            model = w.get_model()
            i = w.get_active()
            if i < 0:
                e = w.get_child()
                if e is not None:
                    v = e.get_text()
            elif model is not None:
                v = model[i][sub]
        elif wid.startswith("t_"):
            v = w.get_text()
        elif wid.startswith("f_"):
            v = w.get_font_name()
        elif wid.startswith("c_"):
            v = w.get_active()
        elif wid.startswith("s_"):
            v = w.get_value()
        elif wid.startswith("btn_"):
            v = w.get_tooltip_text()
        return v

    def set(self, wid, value):
        # print(" init: set",self, wid, value)
        w = self.builder.get_object(wid)
        if wid.startswith("cb_"):
            model = w.get_model()
            e = w.get_child()
            if e is not None and isinstance(e, Gtk.Entry):
                e.set_text(value)
                # e.emit("changed")
            else:
                for i, v in enumerate(model):
                    if v[w.get_id_column()] == value:
                        w.set_active_id(value)
                        # w.emit("changed")
                        break
        elif wid.startswith("t_"):
            w.set_text(value)
        elif wid.startswith("f_"):
            w.set_font_name(value)
            w.emit("font-set")
        elif wid.startswith("c_"):
            w.set_active(value)
        elif wid.startswith("s_"):
            w.set_value(value)
        elif wid.startswith("btn_"):
            w.set_tooltip_text(value)

    def getBooks(self):
        # print(" init: getBooks",self)
        if not self.get('c_multiplebooks'):
            return [self.get('cb_book')]
        elif len(self.booklist):
            return self.booklist
        else:
            return self.get('t_booklist').split()

    def getBookFilename(self, bk, prjdir):
        # print(" init: getBookFilename",self, bk, prjdir)
        if self.ptsettings is None:
            self.ptsettings = ParatextSettings(prjdir)
        fbkfm = self.ptsettings['FileNameBookNameForm']
        bknamefmt = fbkfm.replace("MAT","{bkid}").replace("41","{bknum:02d}") + \
                    self.ptsettings['FileNamePostPart']
        fname = bknamefmt.format(bkid=bk, bknum=books.get(bk, 0))
        return fname
        
    def onDestroy(self, btn):
        Gtk.main_quit()

    def onOK(self, btn):
        # print("\n init: onOK",self, btn,"\n")
        if self.prjid is not None:
            self.callback(self)
        else:
            dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
                "Cannot create a PDF without a Project selected")
            dialog.format_secondary_text("Please select a Paratext Project and try again.")
            dialog.run()
            dialog.destroy()
            self.cb_project.grab_focus() # this doesn't appear to do anything yet!

    def onCancel(self, btn):
        self.onDestroy(btn)

    def onScriptChanged(self, cb_script):
        # print(" init: onScriptChanged",self, cb_script)
        # If there is a matching digit style for the script that has just been set, 
        # then turn that on (but it can be overridden later).
        try:
            self.cb_digits.set_active_id(self.get('cb_script'))
        except:
            self.cb_digits.grab_focus()  # this doesn't appear to do anything yet!

    def onFontChange(self, fbtn):
        # print(" init: onFontChange",self, fbtn)
        # traceback.print_stack(limit=3)
        font = fbtn.get_font_name()
        (name, size) = self.parse_fontname(font)
        label = self.builder.get_object("l_font")
        for s in ('bold', 'italic', 'bold italic'):
            sid = s.replace(" ", "")
            w = self.builder.get_object("f_"+sid)
            f = TTFont(name, style = " ".join(s.split()))
            fname = f.family + ", " + f.style + " " + str(size)
            w.set_font_name(fname)
            # print(fname, f.family, f.style, f.filename)
            # print(s, fname, f.extrastyles)
            if 'bold' in f.style.lower():
                self.set("s_{}embolden".format(sid), 2)
            if 'italic' in f.style.lower():
                self.set("s_{}slant".format(sid), 0.15)

    def updateFakeLabels(self):
        status = self.get("c_fakebold") or self.get("c_fakeitalic") or self.get("c_fakebolditalic")
        for c in ("l_embolden", "l_slant"):
            self.builder.get_object(c).set_sensitive(status)

    def onFakeboldClicked(self, c_fakebold):
        status = self.get("c_fakebold")
        for c in ("s_boldembolden", "s_boldslant"):
            self.builder.get_object(c).set_sensitive(status)
        self.updateFakeLabels()
        
    def onFakeitalicClicked(self, c_fakeitalic):
        status = self.get("c_fakeitalic")
        for c in ("s_italicembolden", "s_italicslant"):
            self.builder.get_object(c).set_sensitive(status)
        self.updateFakeLabels()

    def onFakebolditalicClicked(self, c_fakebolditalic):
        status = self.get("c_fakebolditalic")
        for c in ("s_bolditalicembolden", "s_bolditalicslant"):
            self.builder.get_object(c).set_sensitive(status)
        self.updateFakeLabels()

    def onVariableLineSpacingClicked(self, c_variableLineSpacing):
        status = self.get("c_variableLineSpacing")
        for c in ("s_linespacingmin", "s_linespacingmax", "l_min", "l_max"):
            self.builder.get_object(c).set_sensitive(status)
        lnsp = self.builder.get_object("s_linespacing")
        min = self.builder.get_object("s_linespacingmin")
        max = self.builder.get_object("s_linespacingmax")
        lnspVal = round(lnsp.get_value(),1)
        minVal = round(min.get_value(),1)
        maxVal = round(max.get_value(),1)
        if status and lnspVal == minVal and lnspVal == maxVal:
            min.set_value(lnspVal-1) 
            max.set_value(lnspVal+2) 

    def onUseIllustrationsClicked(self, c_includeillustrations):
        status = self.get("c_includeillustrations")
        for c in ("c_includefigsfromtext", "c_usePicList", "l_useFolder", "c_useFiguresFolder", "c_useLocalFiguresFolder", "c_useCustomFolder",
                  "btn_selectFigureFolder", "l_useFiguresFolder", "l_useLocalFiguresFolder",
                  "c_figexclwebapp", "c_figplaceholders", "c_fighiderefs", "c_skipmissingimages"):  # add this later: "c_convertTIFtoPNG", 
            self.builder.get_object(c).set_sensitive(status)
        if status:
            status = self.get("c_includefigsfromtext")
            for c in ("c_figexclwebapp", "c_figplaceholders", "c_fighiderefs"):
                self.builder.get_object(c).set_sensitive(status)

    def onUseCustomFolderclicked(self, c_useCustomFolder):
        self.builder.get_object("btn_selectFigureFolder").set_sensitive(self.get("c_useCustomFolder"))

    def onBlendedXrsClicked(self, c_blendfnxr):
        status = self.get("c_blendfnxr")
        for c in ("c_includeXrefs", "c_xrautocallers", "t_xrcallers", "c_xromitcaller", "c_xrpageresetcallers", "c_paragraphedxrefs"):
            self.builder.get_object(c).set_sensitive(not status)
        self.builder.get_object("cb_blendedXrefCaller").set_sensitive(status)
    
    def onClickedIncludeFootnotes(self, c_includeFootnotes):
        status = self.get("c_includeFootnotes")
        for c in ("c_fnautocallers", "t_fncallers", "c_fnomitcaller", "c_fnpageresetcallers", "c_fnparagraphednotes"):
            self.builder.get_object(c).set_sensitive(status)
        # self.GenerateNestedStyles(None)
        
    def onClickedIncludeXrefs(self, c_includeXrefs):
        status = self.get("c_includeXrefs")
        for c in ("c_xrautocallers", "t_xrcallers", "c_xromitcaller", "c_xrpageresetcallers", "c_paragraphedxrefs"):
            self.builder.get_object(c).set_sensitive(status)
        # self.GenerateNestedStyles(None)

    def onPageGutterChanged(self, c_pagegutter):
        status = self.get("c_pagegutter")
        gtr = self.builder.get_object("s_pagegutter")
        gtr.set_sensitive(status)
        if status:
            gtr.grab_focus() 

    def onDoubleColumnChanged(self, c_doublecolumn):
        status = self.get("c_doublecolumn")
        for c in ("c_verticalrule", "l_gutterWidth", "s_colgutterfactor"):
            self.builder.get_object(c).set_sensitive(status)

    def onBookSelectorChange(self, c_multiplebooks):
        status = self.get("c_multiplebooks")
        for c in ("c_combine", "t_booklist"):
            self.builder.get_object(c).set_sensitive(status)
        toc = self.builder.get_object("c_autoToC") # Ensure that we're not trying to build a ToC for a single book!
        toc.set_sensitive(status)
        if not status:
            toc.set_active(False)
        for c in ("l_singlebook", "cb_book", "l_chapfrom", "cb_chapfrom", "l_chapto", "cb_chapto"):
            self.builder.get_object(c).set_sensitive(not status)
            
    def onFigsChanged(self, c_includefigsfromtext):
        status = self.get("c_includefigsfromtext")
        for c in ("c_figexclwebapp", "c_figplaceholders", "c_fighiderefs"):
            self.builder.get_object(c).set_sensitive(status)

    def onInclFrontMatterChanged(self, c_inclFrontMatter):
        self.builder.get_object("btn_selectFrontPDFs").set_sensitive(self.get("c_inclFrontMatter"))

    def onInclBackMatterChanged(self, c_inclBackMatter):
        self.builder.get_object("btn_selectBackPDFs").set_sensitive(self.get("c_inclBackMatter"))
            
    def onApplyWatermarkChanged(self, c_applyWatermark):
        self.builder.get_object("btn_selectWatermarkPDF").set_sensitive(self.get("c_applyWatermark"))
    
    def onAutoTocChanged(self, c_autoToC):
        atoc = self.builder.get_object("t_tocTitle")
        if self.get("c_autoToC"):
            atoc.set_sensitive(True)
            atoc.grab_focus() 
        else:   
            atoc.set_sensitive(False)

    def onLineBreakChanged(self, c_linebreakon):
        lbrk = self.builder.get_object("t_linebreaklocale")
        if self.get("c_linebreakon"):
            lbrk.set_sensitive(True)
            lbrk.grab_focus() 
        else:   
            lbrk.set_sensitive(False)
            
    def onFnCallersChanged(self, c_fnautocallers):
        fnc = self.builder.get_object("t_fncallers")
        if self.get("c_fnautocallers"):
            fnc.set_sensitive(True)
            fnc.grab_focus() 
        else:   
            fnc.set_sensitive(False)
            
    def onXrCallersChanged(self, c_xrautocallers):
        xrc = self.builder.get_object("t_xrcallers")
        if self.get("c_xrautocallers"):
            xrc.set_sensitive(True)
            xrc.grab_focus() 
        else:   
            xrc.set_sensitive(False)
            
    def onrunningFooterChanged(self, c_runningFooter):
        rnf = self.builder.get_object("t_runningFooter")
        if self.get("c_runningFooter"):
            rnf.set_sensitive(True)
            rnf.grab_focus() 
        else:   
            rnf.set_sensitive(False)
            
    def onRHruleChanged(self, c_rhrule):
        rhr = self.builder.get_object("s_rhruleposition")
        if self.get("c_rhrule"):
            rhr.set_sensitive(True)
            rhr.grab_focus() 
        else:   
            rhr.set_sensitive(False)

    def onProcessScriptClicked(self, c_processScript):
        status = self.get("c_processScript")
        for c in ("c_processScriptBefore", "c_processScriptAfter", "btn_selectScript"):
            self.builder.get_object(c).set_sensitive(status)
            
    def onUsePrintDraftChangesClicked(self, c_usePrintDraftChanges):
        status = self.get("c_usePrintDraftChanges")
        for c in ("btn_editChangesFile", "c_processScriptBefore", "c_processScriptAfter", "l_processScript"):
            self.builder.get_object(c).set_sensitive(status)
        if self.info is not None:           # trigger a rereading of the changes
            # this is a kludge. Better to keep the last modified date and test in Info.convertBook
            self.info.changes = None
        
    def onUseModsTexClicked(self, c_useModsTex):
        self.builder.get_object("btn_editModsTeX").set_sensitive(self.get("c_useModsTex"))
        
    def onUseModsStyClicked(self, c_useModsSty):
        self.builder.get_object("btn_editModsSty").set_sensitive(self.get("c_useModsSty"))
        
    def onSuppressOutlineClicked(self, c_omitIntroOutline):
        self.builder.get_object("c_prettyIntroOutline").set_sensitive(not self.get("c_omitIntroOutline"))
        self.builder.get_object("c_prettyIntroOutline").set_active(False)
        # self.GenerateNestedStyles(None)

    def onUsePTmacrosClicked(self, c_usePTmacros):
        status = self.get("c_usePTmacros")
        for c in ("c_variableLineSpacing", "s_linespacingmin", "s_linespacingmax", "l_min", "l_max"):
            self.builder.get_object(c).set_sensitive(not status)
        # These are (temporarily) disabled until we get them working properly and predictably
        for c in ("c_startOnHalfPage", "c_marginalverses"):
            self.builder.get_object(c).set_sensitive(False)

    def onHideAdvancedSettingsClicked(self, c_hideAdvancedSettings):
        # Turn Dangerous Settings OFF
        for c in ("c_startOnHalfPage", "c_marginalverses", "c_prettyIntroOutline", "c_blendfnxr", "c_autoToC", "c_figplaceholders",
                  "c_omitallverses", "c_glueredupwords", "c_omit1paraIndent", "c_hangpoetry", "c_preventwidows"):
            self.builder.get_object(c).set_active(False)
            
        # Turn Essential Settings ON
        for c in ("c_mainBodyText", "c_footnoterule",
                  "c_includefigsfromtext", "c_skipmissingimages", "c_convertTIFtoPNG", "c_useFiguresFolder"):
            self.builder.get_object(c).set_active(True)
            
        # Hide a whole bunch of stuff that they don't need to see
        for c in ("tb_Markers", "tb_Diglot", "tb_Advanced","tb_Logging", "fr_FontConfig", "row_ToC", "c_figplaceholders",
                  "bx_BottomMarginSettings", "bx_TopMarginSettings", "gr_HeaderAdvOptions", "box_AdvFootnoteConfig", 
                  "c_usePicList", "c_skipmissingimages", "c_convertTIFtoPNG", "c_useCustomFolder", "btn_selectFigureFolder", 
                  "c_startOnHalfPage", "c_prettyIntroOutline", "c_marginalverses",
                  "bx_fnCallers", "bx_fnCalleeCaller", "bx_xrCallers", "bx_xrCalleeCaller",
                  "c_omitallverses", "c_glueredupwords", "c_omit1paraIndent", "c_hangpoetry", "c_preventwidows"):
            self.builder.get_object(c).set_visible(not self.get("c_hideAdvancedSettings"))
        
    def onKeepTemporaryFilesClicked(self, c_keepTemporaryFiles):
        self.builder.get_object("gr_debugTools").set_sensitive(self.get("c_keepTemporaryFiles"))
        
    def onViewSFMfileClicked(self, btn_viewSFMfile):
        bk = self.get("cb_examineBook")
        prjid = self.get("cb_project")
        prjdir = os.path.join(self.settings_dir, self.prjid)
        fname = self.getBookFilename(bk, prjdir)
        viewfile = os.path.join(prjdir, "PrintDraft", fname)
        doti = viewfile.rfind(".")
        if doti > 0:
            viewfile = viewfile[:doti] + "-draft" + viewfile[doti:]
        if os.path.exists(viewfile):
            if sys.platform == "win32":
                os.startfile(viewfile)
            elif sys.platform == "linux":
                subprocess.call(('xdg-open', viewfile))
            
    def ViewOutputFile(self, extn):
        prjid = self.get("cb_project")
        bks = self.getBooks()
        prjdir = os.path.join(self.settings_dir, self.prjid)
        if len(bks) > 1:
            fname = "ptxprint-{}_{}{}.{}".format(bks[0], bks[-1], prjid, extn)
        else:
            fname = "ptxprint-{}{}.{}".format(bks[0], prjid, extn)
        viewfile = os.path.join(prjdir, "PrintDraft", fname)
        if os.path.exists(viewfile):
            if sys.platform == "win32":
                os.startfile(viewfile)
            elif sys.platform == "linux":
                subprocess.call(('xdg-open', viewfile))
        
    def onViewTeXfileClicked(self, btn_viewTeXfile):
        self.ViewOutputFile("tex")
        
    def onViewLogFileClicked(self, btn_viewLogFile):
        self.ViewOutputFile("log")
        
    def onChooseBooksClicked(self, btn):
        dia = self.builder.get_object("dlg_multiBookSelector")
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
        response = dia.run()
        if response == Gtk.ResponseType.OK:
            self.booklist = [b.get_label() for b in self.alltoggles if b.get_active()]
            bl.set_text(" ".join(b for b in self.booklist))
            self.builder.get_object("c_multiplebooks").set_active(not self.booklist == [])

        dia.hide()

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

    def onTocClicked(self, c_toc):
        if not self.get("c_usetoc1") and not self.get("c_usetoc2") and not self.get("c_usetoc3"):
            toc = self.builder.get_object("c_usetoc1")
            toc.set_active(True)
            
    def _setchap(self, ls, start, end):
        ls.clear()
        for c in range(start, end+1):
            ls.append([str(c)])

    def onBookChange(self, cb_book):
        # print(" init: onBookChange",self, cb_book)
        self.bk = self.get("cb_book")
        if self.bk != "":
            self.chs = int(chaps.get(str(self.bk)))
            self.chapfrom = self.builder.get_object("ls_chapfrom")
            self._setchap(self.chapfrom, 1, self.chs)
            self.cb_chapfrom.set_active_id('1')
        
            self.chapto = self.builder.get_object("ls_chapto")
            self._setchap(self.chapto, 1, self.chs)
            self.cb_chapto.set_active_id(str(self.chs))

    def onChapFrmChg(self, cb_chapfrom):
        self.bk = self.get("cb_book")
        if self.bk != "":
            self.chs = int(chaps.get(str(self.bk)))
            self.strt = self.builder.get_object("cb_chapfrom").get_active_id()
            self.chapto = self.builder.get_object("ls_chapto")
            self._setchap(self.chapto, (int(self.strt) if self.strt is not None else 0), self.chs)
            self.cb_chapto.set_active_id(str(self.chs))
        
    def onProjectChange(self, cb_prj):
        currprj = self.prjid
        if currprj is not None:
            if self.info is None:
                self.info = Info(self, self.settings_dir, prjid = currprj)
            config = self.info.createConfig(self)
            with open(os.path.join(self.settings_dir, currprj, "ptxprint.cfg"), "w", encoding="utf-8") as outf:
                config.write(outf)
        self.prjid = self.get("cb_project")
        self.ptsettings = None
        lsbooks = self.builder.get_object("ls_books")
        if currprj is not None:
            cbbook = self.builder.get_object("cb_book")
            cbbook.set_model(None)
            lsbooks.clear()
            cbbook.set_model(lsbooks)
        if not self.prjid:
            return
        self.ptsettings = ParatextSettings(self.settings_dir, self.prjid)
        bp = self.ptsettings['BooksPresent']
        for b in allbooks:
            ind = books.get(b, 0)-1
            if 0 <= ind < len(bp) and bp[ind - 1 if ind > 40 else ind] == "1":
                lsbooks.append([b])
        cb_bk = self.builder.get_object("cb_book")
        cb_bk.set_active(0)
        font_name = self.ptsettings.get('DefaultFont', 'Arial') + ", " + self.ptsettings.get('DefaultFontSize', '12')
        self.set('f_body', font_name)
        configfile = os.path.join(self.settings_dir, self.prjid, "ptxprint.cfg")
        if os.path.exists(configfile):
            print("Reading configfile {}".format(configfile))
            self.info = Info(self, self.settings_dir, self.prjid)
            config = configparser.ConfigParser()
            config.read(configfile, encoding="utf-8")
            self.info.loadConfig(self, config)
        else:
            self.info.update()
        status = self.get("c_multiplebooks")
        for c in ("c_combine", "t_booklist"):
            self.builder.get_object(c).set_sensitive(status)
        toc = self.builder.get_object("c_autoToC") # Ensure that we're not trying to build a ToC for a single book!
        toc.set_sensitive(status)
        if not status:
            toc.set_active(False)
        for c in ("l_singlebook", "cb_book", "l_chapfrom", "cb_chapfrom", "l_chapto", "cb_chapto"):
            self.builder.get_object(c).set_sensitive(not status)

    def onEditChangesFile(self, cb_prj):
        self.prjid = self.get("cb_project")
        changesfile = os.path.join(self.settings_dir, self.prjid, "PrintDraftChanges.txt")
        if os.path.exists(changesfile):
            if sys.platform == "win32":
                os.startfile(changesfile)
            elif sys.platform == "linux":
                subprocess.call(('xdg-open', changesfile))

    def onEditModsTeX(self, cb_prj):
        self.prjid = self.get("cb_project")
        modstexfile = os.path.join(self.settings_dir, self.prjid, "PrintDraft", "PrintDraft-mods.tex")
        if os.path.exists(modstexfile):
            if sys.platform == "win32":
                os.startfile(modstexfile)
            elif sys.platform == "linux":
                subprocess.call(('xdg-open', modstexfile))

    def onEditModsSty(self, cb_prj):
        self.prjid = self.get("cb_project")
        modsstyfile = os.path.join(self.settings_dir, self.prjid, "PrintDraft", "PrintDraft-mods.sty")
        if os.path.exists(modsstyfile):
            if sys.platform == "win32":
                os.startfile(modsstyfile)
            elif sys.platform == "linux":
                subprocess.call(('xdg-open', modsstyfile))

    def onMainBodyTextChanged(self, c_mainBodyText):
        self.builder.get_object("gr_mainBodyText").set_sensitive(self.get("c_mainBodyText"))

    def onSelectScriptClicked(self, btn_selectScript):
        CustomScript = self.fileChooser("Select a Custom Script file", 
                filters = {"Executable Scripts": {"patterns": "*.bat", "mime": "application/bat"}},
                # ),("*.sh", "mime": "application/x-sh")
                multiple = False)
        if CustomScript is not None:
            self.CustomScript = CustomScript
            btn_selectScript.set_tooltip_text("\n".join('{}'.format(s) for s in CustomScript))
        else:
            self.CustomScript = None
            btn_selectScript.set_tooltip_text("")
            self.builder.get_object("btn_selectScript").set_sensitive(False)
            self.builder.get_object("c_processScript").set_active(False)
            for c in ("btn_selectScript", "c_processScriptBefore", "c_processScriptAfter", "l_script2process"):
                self.builder.get_object(c).set_sensitive(False)

    def onFrontPDFsClicked(self, btn_selectFrontPDFs):
        FrontPDFs = self.fileChooser("Select one or more PDF(s) for FRONT matter", 
                filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                multiple = True)
        if FrontPDFs is not None and FrontPDFs != 'None':
            self.FrontPDFs = FrontPDFs
            btn_selectFrontPDFs.set_tooltip_text("\n".join('{}'.format(s) for s in FrontPDFs))
        else:
            self.FrontPDFs = None
            btn_selectFrontPDFs.set_tooltip_text("")
            self.builder.get_object("btn_selectFrontPDFs").set_sensitive(False)
            self.builder.get_object("c_inclFrontMatter").set_active(False)

    def onBackPDFsClicked(self, btn_selectBackPDFs):
        BackPDFs = self.fileChooser("Select one or more PDF(s) for BACK matter", 
                filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                multiple = True)
        if BackPDFs is not None and BackPDFs != 'None':
            self.BackPDFs = BackPDFs
            btn_selectBackPDFs.set_tooltip_text("\n".join('{}'.format(s) for s in BackPDFs))
        else:
            self.BackPDFs = None
            btn_selectBackPDFs.set_tooltip_text("")
            self.builder.get_object("btn_selectBackPDFs").set_sensitive(False)
            self.builder.get_object("c_inclBackMatter").set_active(False)

    def onWatermarkPDFclicked(self, btn_selectWatermarkPDF):
        watermarks = self.fileChooser("Select Watermark PDF file", 
                filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                multiple = False)
        if watermarks is not None and watermarks != 'None':
            self.watermarks = watermarks[0]
            btn_selectWatermarkPDF.set_tooltip_text(watermarks[0])
        else:
            self.watermarks = None
            btn_selectWatermarkPDF.set_tooltip_text("")
            self.builder.get_object("btn_selectWatermarkPDF").set_sensitive(False)
            self.builder.get_object("c_applyWatermark").set_active(False)

    def onSelectFigureFolderClicked(self, btn_selectFigureFolder):
        customFigFolder = self.fileChooser("Select the folder containing image files", 
                filters = None, multiple = False, folder = True)
        if customFigFolder is not None:
            self.customFigFolder = customFigFolder[0]
            btn_selectFigureFolder.set_tooltip_text(customFigFolder[0])
            self.builder.get_object("c_useCustomFolder").set_active(True)
        else:
            self.watermarks = None
            btn_selectFigureFolder.set_tooltip_text("")
            self.builder.get_object("btn_selectFigureFolder").set_sensitive(False)
            self.builder.get_object("c_useFiguresFolder").set_active(True)

    def onGeneratePicList(self, btn_generateParaAdjList):
        # Format of lines in pic-list file: BBB C.V desc|file|size|loc|copyright|caption|ref
        # MRK 1.16 fishermen...catching fish with a net.|hk00207b.png|span|b||Jesus calling the disciples to follow him.|1.16
        _picposn = {
            "col":      ("tl", "tr", "bl", "br"),
            "span":     ("t", "b")
        }
        existingFilelist = []
        for bk in self.getBooks():
            prjid = self.get("cb_project")
            prjdir = os.path.join(self.settings_dir, self.prjid)
            tmpdir = os.path.join(prjdir, 'PrintDraft') if self.get("c_useprintdraftfolder") else r"C:\temp"  # args.directory ???
            fname = self.getBookFilename(bk, prjdir)
            infname = os.path.join(prjdir, fname)
            outfname = os.path.join(prjdir, "PrintDraft\PicLists", fname)
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:] + ".piclist"
            piclist = []
            with open(infname, "r", encoding="utf-8") as inf:
                dat = inf.read()
                # Finds USFM2-styled markup in text:
                #                0         1       2     3     4              5       
                # \\fig .*\|(.+?\....)\|(....?)\|(.*)\|(.*)\|(.+?)\|(\d+[:.]\d+([-,]\d+)?)\\fig\*
                # \fig |CN01684C.jpg|col|||key-kālk arsi manvan yēsunaga tarval|9:2\fig*
                #           0         1  2 3          4                          5  
                # BKN \5 \|\0\|\1\|tr\|\|\4\|\5
                # MAT 9.2 bringing the paralyzed man to Jesus|CN01684C.jpg|col|tr||key-kālk arsi manvan yēsunaga tarval|9:2
                m = re.findall(r"\\fig .*\|(.+?\....)\|(....?)\|(.+)?\|(.+)?\|(.+)?\|(\d+[\:\.]\d+([\-,]\d+)?)\\fig\*", dat)
                if m is not None:
                    for f in m:
                        picfname = re.sub(r"\.[Tt][Ii][Ff]",".jpg",f[0])           # Change all TIFs to JPGs
                        if self.get("c_randomPicPosn"):
                            pageposn = random.choice(_picposn.get(f[1], f[1]))    # Randomize location of illustrations on the page (tl,tr,bl,br)
                        else:
                            pageposn = (_picposn.get(f[1], f[1]))[0]              # use the t or tl (first in list)
                        piclist.append(bk+" "+re.sub(r":",".", f[5])+" |"+picfname+"|"+f[1]+"|"+pageposn+"||"+f[4]+"|"+f[5]+"\n")
                else:
                    # If none of the USFM2-styled illustrations were found then look for USFM3-styled markup in text 
                    # (Q: How to handle any additional/non-standard xyz="data" ? Will the .* before \\fig\* take care of it adequately?)
                    #         0              1               2                  3      [4]
                    # \\fig (.+?)\|src="(.+?\....)" size="(....?)" ref="(\d+[:.]\d+([-,]\d+)?)".*\\fig\*
                    # \fig hāgartun saṅga dūtal vaḍkval|src="CO00659B.TIF" size="span" ref="21:16"\fig*
                    #                   0                         1                2          3  [4]
                    # BKN \3 \|\1\|\2\|tr\|\|\0\|\3
                    # GEN 21.16 an angel speaking to Hagar|CO00659B.TIF|span|t||hāgartun saṅga dūtal vaḍkval|21:16
                    m = re.findall(r'\\fig (.+?)\|src="(.+?\....)" size="(....?)" ref="(\d+[:.]\d+([-,]\d+)?)".*\\fig\*', dat)
                    if m is not None:
                        for f in m:
                            picfname = re.sub(r"\.[Tt][Ii][Ff]",".jpg",f[1])           # Change all TIFs to JPGs
                            if self.get("c_randomPicPosn"):
                                pageposn = random.choice(_picposn.get(f[2], f[2]))     # Randomize location of illustrations on the page (tl,tr,bl,br)
                            else:
                                pageposn = (_picposn.get(f[2], f[2]))[0]               # use the t or tl (first in list)
                            piclist.append(bk+" "+re.sub(r":",".", f[3])+" |"+picfname+"|"+f[2]+"|"+pageposn+"||"+f[0]+"|"+f[3]+"\n")
                if len(m):
                    plpath = os.path.join(prjdir, "PrintDraft\PicLists")
                    if not os.path.exists(plpath):
                        os.mkdir(plpath)
                    if not os.path.exists(outfname):
                        with open(outfname, "w", encoding="utf-8") as outf:
                            outf.write("".join(piclist))
                    else:
                        existingFilelist.append(outfname.split("/")[-1])
                else:
                    print(r"No illustrations \fig ...\fig* found in {}".format(bk)) # This needs to go to the log/console: 
        if len(existingFilelist):
            if len(existingFilelist) > 1:
                m1 = "Several PicList files already exist:"
                m2 = "\n".join(existingFilelist)+"\n\nThese have not been overwritten. Click Edit PicList...\nto select a PicList file to be edited."
            else: # if only 1 file found
                m1 = "This PicList file already exists:"
                m2 = "\n".join(existingFilelist)+"\n\nIt has not been overwritten. Now just click Edit PicList..."
            dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, m1)
            dialog.format_secondary_text(m2)
            dialog.format_secondary_text(m2)
            dialog.run()
            dialog.destroy()

    def onGenerateParaAdjList(self, btn_generateParaAdjList):
        existingFilelist = []
        for bk in self.getBooks():
            prjid = self.get("cb_project")
            prjdir = os.path.join(self.settings_dir, self.prjid)
            tmpdir = os.path.join(prjdir, 'PrintDraft') if self.get("c_useprintdraftfolder") else r"C:\temp"
            fname = self.getBookFilename(bk, prjdir)
            infname = os.path.join(prjdir, fname)
            outfname = os.path.join(prjdir, "PrintDraft/AdjLists", fname)
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:] + ".adj"
            adjlist = []
            with open(infname, "r", encoding="utf-8") as inf:
                dat = inf.read()
                m = re.findall(r"\\p ?\r?\n\\v (\d+)",dat)
                if m is not None:
                    prv = 0
                    ch = 1
                    for v in m:
                        if int(v) < int(prv):
                            ch = ch + 1
                        adjlist.append(bk+" "+str(ch)+"."+v+" +0\n")
                        prv = v
                    adjpath = os.path.join(prjdir, "PrintDraft\AdjLists")
                    if not os.path.exists(adjpath):
                        os.mkdir(adjpath)
                    if not os.path.exists(outfname):
                        with open(outfname, "w", encoding="utf-8") as outf:
                            outf.write("".join(adjlist))
                    else:
                        existingFilelist.append(outfname.split("/")[-1])
        if len(existingFilelist):
            if len(existingFilelist) > 1:
                m1 = "Several Paragraph Adjust files already exist:"
                m2 = "\n".join(existingFilelist)+"\n\nThese have not been overwritten. Click on Edit Adjust List...\nto select a Paragraph Adjust List file to be edited."
            else: # if only 1 file found
                m1 = "This Paragraph Adjust List already exists:"
                m2 = "\n".join(existingFilelist)+"\n\nIt has not been overwritten. Click on Edit Adjust List..."
            dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, m1)
            dialog.format_secondary_text(m2)
            dialog.format_secondary_text(m2)
            dialog.run()
            dialog.destroy()

    def onEditAdjListClicked(self, btn_editParaAdjList):
        if not self.get("c_multiplebooks"):
            bk = self.get("cb_book")
            prjid = self.get("cb_project")
            prjdir = os.path.join(self.settings_dir, self.prjid)
            fname = self.getBookFilename(bk, prjdir)
            adjfname = os.path.join(prjdir, "PrintDraft\AdjLists", fname)
            doti = adjfname.rfind(".")
            if doti > 0:
                adjfname = adjfname[:doti] + "-draft" + adjfname[doti:] + ".adj"
            if os.path.exists(adjfname):
                if sys.platform == "win32":
                    os.startfile(adjfname)
                elif sys.platform == "linux":
                    subprocess.call(('xdg-open', adjfname))
            else:
                dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
                    "Unable to edit Adj List file!")
                dialog.format_secondary_text("Please click the Generate button first\nto create the file(s). Then try again.")
                dialog.run()
                dialog.destroy()
        else:
            adjfname = self.fileChooser("Select an Adjust file to edit", 
                    filters = {"Adjust files": {"pattern": "*.adj", "mime": "none"}},
                    multiple = True)
            if adjfname is not None:
                if os.path.exists(adjfname):
                    if sys.platform == "win32":
                        os.startfile(adjfname)
                    elif sys.platform == "linux":
                        subprocess.call(('xdg-open', adjfname))

    def onEditPicListClicked(self, btn_editPicList):
        if not self.get("c_multiplebooks"):
            bk = self.get("cb_book")
            prjid = self.get("cb_project")
            prjdir = os.path.join(self.settings_dir, self.prjid)
            fname = self.getBookFilename(bk, prjdir)
            picfname = os.path.join(prjdir, "PrintDraft\PicLists", fname)
            doti = picfname.rfind(".")
            if doti > 0:
                picfname = picfname[:doti] + "-draft" + picfname[doti:] + ".piclist"
            if os.path.exists(picfname):
                if sys.platform == "win32":
                    os.startfile(picfname)
                elif sys.platform == "linux":
                    subprocess.call(('xdg-open', picfname))
            else:
                dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
                    "Unable to edit Pic List file!")
                dialog.format_secondary_text("Please click the Generate button first\nto create the file(s). Then try again.")
                dialog.run()
                dialog.destroy()
        else:
            # Is there a way to force the file chooser to look in the PicList folder?
            picfname = self.fileChooser("Select a PicList file to edit", 
                    filters = {"PicList files": {"pattern": "*.piclist", "mime": "none"}},
                    multiple = True)
            if picfname is not None:
                if os.path.exists(picfname):
                    if sys.platform == "win32":
                        os.startfile(picfname)
                    elif sys.platform == "linux":
                        subprocess.call(('xdg-open', picfname))
    
    def ontv_sizeallocate(self, atv, dummy):
        b = atv.get_buffer()
        it = b.get_iter_at_offset(-1)
        atv.scroll_to_iter(it, 0, False, 0, 0)

    def fileChooser(self, title, filters = None, multiple = True, folder = False):
        dialog = Gtk.FileChooserDialog(title, None,
            (Gtk.FileChooserAction.SELECT_FOLDER if folder else Gtk.FileChooserAction.OPEN),
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            ("Select" if folder else Gtk.STOCK_OPEN), Gtk.ResponseType.OK))
        dialog.set_default_size(800, 600)
        dialog.set_select_multiple(multiple)
        if filters != None: # was len(filters):
            # filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}}
            filter_in = Gtk.FileFilter()
            for k, f in filters.items():
                filter_in.set_name(k)
                for t, v in f.items():
                    if t == "pattern":
                        filter_in.add_pattern(v)
                    elif t == "patterns":
                        for p in v:
                            filter_in.add_pattern(p)
                    if t == "mime":
                        filter_in.add_mime_type(v)
            dialog.add_filter(filter_in)

        response = dialog.run()
        fcFilepath = None
        if response == Gtk.ResponseType.OK:
            if folder:
                fcFilepath = [dialog.get_filename()+"/"]
            else:
                fcFilepath = dialog.get_filenames()
        dialog.destroy()
        return fcFilepath

    # Awaiting installation of the PIL/Pillow library to do TIF to PNG conversions
    # def convertTIFtoPNG(self, picfname):
        # if os.path.splitext(os.path.join(root, picfname))[1].lower() == ".tif":
            # if os.path.isfile(os.path.splitext(os.path.join(root, picfname))[0] + ".png"):
                # print("A PNG file already exists for {}".format(picfname))
            # else:
                # outputfile = os.path.splitext(os.path.join(root, picfname))[0] + ".png"
                # try:
                    # im = Image.open(os.path.join(root, picfname))
                    # print("Converting TIF for {}".format(picfname))
                    # if im.mode == "CMYK":
                        # im = im.convert("Gray")
                    # im.save(outputfile, "PNG")
                # except Exception, e:
                    # print(e)
    def onDiglotClicked(self, c_diglot):
        self.builder.get_object("gr_diglot").set_sensitive(self.get("c_diglot"))
        self.onDiglotDimensionsChanged(None)

    def onDiglotDimensionsChanged(self, btn):
        PageWidth = 210  # need to make this dynamic
        Margins = self.get("s_margins")
        MiddleGutter = self.get("s_diglotMiddleGutter")
        BindingGutter = self.get("s_pagegutter")
        PriColWid = self.get("s_PriColWidth")
        SecColWid = PageWidth - PriColWid - MiddleGutter - BindingGutter - (2*Margins)
        self.builder.get_object("s_SecColWidth").set_value(SecColWid)
        
        # Calc Pri Settings (righ   t side of page; or outer if mirrored)
        PriColWid = self.get("s_PriColWidth") # this is the only parameter we want them to tweak with a slider (<--40%--|---60%--->)
        PriSideMarginFactor = 1
        PriBindingGutter = PageWidth - PriColWid - (2*Margins)
        
        # Calc Sec Settings (left side of page; or inner if mirrored)
        SecColWid = PageWidth - PriColWid - MiddleGutter - BindingGutter - (2*Margins)
        SecSideMarginFactor = (PriColWid + Margins + MiddleGutter) / Margins
        SecBindingGutter = PageWidth - SecColWid - (2*Margins*SecSideMarginFactor)
        
        PriPercent = round((PriColWid / (PriColWid + SecColWid) * 100),1)
        SecPercent = 100 - PriPercent
        self.builder.get_object("t_PriPercent").set_text(str(PriPercent)+"%")
        self.builder.get_object("t_SecPercent").set_text(str(SecPercent)+"%")
        
        if self.get("c_outputSecText"):
            DiglotString = "\BindingGuttertrue"+ \
                           "\n\BindingGutter={}mm".format(SecBindingGutter)+ \
                           "\n\def\SideMarginFactor{{{:.2f}}}".format(SecSideMarginFactor)+ \
                           "\n\BodyColumns=1"

        else:
            priprjid = self.get("cb_diglotPriProject")
            pritmpdir = os.path.join(self.settings_dir, priprjid, 'PrintDraft') # if self.get("c_useprintdraftfolder") else args.directory
            bkid = self.get("cb_book")
            prifname = os.path.join(pritmpdir, "ptxprint-{}{}.pdf".format(bkid, priprjid))

            DiglotString = "\BindingGuttertrue"+ \
                           "\n\BindingGutter={}mm".format(PriBindingGutter)+ \
                           "\n\def\SideMarginFactor{{{:.2f}}}".format(PriSideMarginFactor)+ \
                           "\n\BodyColumns=1" + \
                           "\def\MergePDF{{" + prifname + "}}"
        self.builder.get_object("l_diglotString").set_text(DiglotString)

    def onBlendPDFsClicked(self, btn):
        if sys.platform == "win32":
            priprjid = self.get("cb_diglotPriProject")
            secprjid = self.get("cb_diglotSecProject")
            pritmpdir = os.path.join(self.settings_dir, priprjid, 'PrintDraft') # if self.get("c_useprintdraftfolder") else args.directory
            sectmpdir = os.path.join(self.settings_dir, secprjid, 'PrintDraft') # if self.get("c_useprintdraftfolder") else args.directory
            bkid = self.get("cb_book")
            prifname = os.path.join(pritmpdir, "ptxprint-{}{}.pdf".format(bkid, priprjid))
            secfname = os.path.join(sectmpdir, "ptxprint-{}{}.pdf".format(bkid, secprjid))
            pdffname = os.path.join(pritmpdir, "ptxprint-diglot-{}-{}-{}.pdf".format(bkid, secprjid, priprjid))
            PDFtkEXE = r"C:\Program Files (x86)\PDFtk Server\bin\pdftk.exe"
            params = '"'+PDFtkEXE+'" "'+prifname+'" '+"multibackground"+' "'+secfname+'" '+"output"+' "'+pdffname+'"'
            params = re.sub(r"/",r"\\", params)
            # pdftk A.pdf multibackground B.pdf output A_B_Diglot.pdf
            print(params)
            # subprocess.run([PDFtkEXE, params])
            subprocess.run([params])
        if os.path.exists(pdffname):
            if sys.platform == "win32":
                os.startfile(pdffname)
