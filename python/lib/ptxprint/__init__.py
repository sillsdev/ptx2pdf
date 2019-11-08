#!/usr/bin/python3

import sys, os, re, regex, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import xml.etree.ElementTree as et
from ptxprint.font import TTFont
from ptxprint.runner import StreamTextBuffer
import configparser

# For future Reference on how Paratext treats this list:
# G                                    MzM                         RT                P        X      FBO    ICGTND          L  OT z NT DC  -  X Y  -  Z  --  L
# E                                    AzA                         EO                S        X      RAT    NNLDDA          A  
# N                                    LzT                         VB                2        ABCDEFGTKH    TCOXXG          O  39+1+27+18+(8)+7+3+(4)+6+(10)+1 = 124
# 111111111111111111111111111111111111111111111111111111111111111111111111111111111111000000001111111111000011111100000000001  CompleteCanon (all books possible)

_bookslist = """GEN|50 EXO|40 LEV|27 NUM|36 DEU|34 JOS|24 JDG|21 RUT|4 1SA|31 2SA|24 1KI|22 2KI|25 1CH|29 2CH|36 EZR|10 NEH|13
        EST|10 JOB|42 PSA|150 PRO|31 ECC|12 SNG|8 ISA|66 JER|52 LAM|5 EZK|48 DAN|12 HOS|14 JOL|3 AMO|9 OBA|1 JON|4 MIC|7 NAM|3
        HAB|3 ZEP|3 HAG|2 ZEC|14 MAL|4 ZZZ|0   MAT|28 MRK|16 LUK|24 JHN|21 ACT|28 ROM|16 1CO|16 2CO|13 GAL|6 EPH|6 PHP|4 COL|4 
        1TH|5 2TH|3 1TI|6 2TI|4 TIT|3 PHM|1 HEB|13 JAS|5 1PE|5 2PE|3 1JN|5 2JN|1 3JN|1 JUD|1 REV|22
        TOB|14 JDT|16 ESG|10 WIS|19 SIR|51 BAR|6 LJE|1 S3Y|1 SUS|1 BEL|1 1MA|16 2MA|15 3MA|7 4MA|18 1ES|9 2ES|16 MAN|1 PS2|1
        ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 XXA|0 XXB|0 XXC|0 XXD|0 XXE|0 XXF|0 XXG|0 FRT|0 BAK|0 OTH|0 ZZZ|0 ZZZ|0 
        ZZZ|0 ZZZ|0 INT|0 CNC|0 GLO|0 TDX|0 NDX|0 DAG|14 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 LAO|1"""

# xmlstarlet sel -t -m '//iso_15924_entry' -o '"' -v '@alpha_4_code' -o '" : "' -v '@name' -o '",' -n /usr/share/xml/iso-codes/iso_15924.xml
_allscripts = { "Zyyy" : "Default (Auto-detect script)", "Adlm" : "Adlam", "Afak" : "Afaka", "Aghb" : "Caucasian Albanian", "Ahom" : "Ahom, Tai Ahom", 
    "Arab" : "Arabic", "Aran" : "Arabic (Nastaliq)", "Armi" : "Imperial Aramaic", "Armn" : "Armenian", "Avst" : "Avestan", "Bali" : "Balinese",
    "Bamu" : "Bamum", "Bass" : "Bassa Vah", "Batk" : "Batak", "Beng" : "Bengali", "Bhks" : "Bhaiksuki", "Blis" : "Blissymbols", "Bopo" : "Bopomofo",
    "Brah" : "Brahmi", "Brai" : "Braille", "Bugi" : "Buginese", "Buhd" : "Buhid", "Cakm" : "Chakma", "Cans" : "Canadian Aboriginal Syllabics",
    "Cari" : "Carian", "Cham" : "Cham", "Cher" : "Cherokee", "Cirt" : "Cirth", "Copt" : "Coptic", "Cprt" : "Cypriot", "Cyrl" : "Cyrillic",
    "Cyrs" : "Cyrillic (Old Church Slavonic)", "Deva" : "Devanagari", "Dsrt" : "Deseret (Mormon)", "Egyd" : "Egyptian demotic", 
    "Egyh" : "Egyptian hieratic", "Elba" : "Elbasan", "Ethi" : "Ethiopic (Geʻez)", "Geok" : "Khutsuri (Asomtavruli & Nuskhuri)", 
    "Geor" : "Georgian (Mkhedruli)", "Glag" : "Glagolitic", "Gong" : "Gondi (Gunjala)", "Gonm" : "Gondi (Masaram)",
    "Goth" : "Gothic", "Gran" : "Grantha", "Grek" : "Greek", "Gujr" : "Gujarati", "Guru" : "Gurmukhi",
    "Hanb" : "Han with Bopomofo", "Hang" : "Hangul (Hangŭl, Hangeul)", "Hani" : "Han (Hanzi, Kanji, Hanja)",
    "Hano" : "Hanunoo (Hanunóo)", "Hans" : "Han (Simplified)", "Hant" : "Han (Traditional)", "Hatr" : "Hatran", "Hebr" : "Hebrew",
    "Hira" : "Hiragana", "Hmng" : "Pahawh Hmong", "Hrkt" : "Japanese (Hiragana+Katakana)", "Hung" : "Old Hungarian (Runic)",
    "Ital" : "Old Italic (Etruscan, Oscan)", "Jamo" : "Jamo (subset of Hangul)", "Java" : "Javanese",
    "Jpan" : "Japanese (Han+Hiragana+Katakana)", "Jurc" : "Jurchen", "Kali" : "Kayah Li", "Kana" : "Katakana", "Khar" : "Kharoshthi",
    "Khmr" : "Khmer", "Khoj" : "Khojki", "Kitl" : "Khitan (large)", "Kits" : "Khitan (small)", "Knda" : "Kannada", "Kore" : "Korean (Hangul+Han)",
    "Kpel" : "Kpelle", "Kthi" : "Kaithi", "Lana" : "Tai Tham (Lanna)", "Laoo" : "Lao", "Latf" : "Latin (Fraktur)",
    "Latg" : "Latin (Gaelic)", "Latn" : "Latin", "Leke" : "Leke", "Lepc" : "Lepcha (Róng)", "Limb" : "Limbu", "Lina" : "Linear A",
    "Linb" : "Linear B", "Lisu" : "Lisu (Fraser)", "Loma" : "Loma", "Lyci" : "Lycian", "Lydi" : "Lydian", "Mahj" : "Mahajani", 
    "Mand" : "Mandaic, Mandaean", "Mani" : "Manichaean", "Marc" : "Marchen", "Mend" : "Mende Kikakui", "Merc" : "Meroitic Cursive",
    "Mlym" : "Malayalam", "Modi" : "Modi", "Mong" : "Mongolian", "Mroo" : "Mro, Mru", "Mtei" : "Meitei Mayek", "Mult" : "Multani", 
    "Mymr" : "Myanmar (Burmese)", "Narb" : "North Arabian (Ancient)", "Nbat" : "Nabataean", "Newa" : "New (Newar, Newari)",
    "Nkgb" : "Nakhi Geba (Naxi Geba)", "Nkoo" : "N’Ko", "Nshu" : "Nüshu", "Ogam" : "Ogham", "Olck" : "Ol Chiki (Ol Cemet’, Santali)", 
    "Orkh" : "Old Turkic, Orkhon Runic", "Orya" : "Oriya", "Osge" : "Osage", "Osma" : "Osmanya", "Palm" : "Palmyrene",
    "Pauc" : "Pau Cin Hau", "Perm" : "Old Permic", "Phag" : "Phags-pa", "Phli" : "Inscriptional Pahlavi", "Phlp" : "Psalter Pahlavi",
    "Phlv" : "Book Pahlavi", "Phnx" : "Phoenician", "Plrd" : "Miao (Pollard)", "Prti" : "Inscriptional Parthian",
    "Rjng" : "Rejang (Redjang, Kaganga)", "Roro" : "Rongorongo",
    "Runr" : "Runic", "Samr" : "Samaritan", "Sara" : "Sarati", "Sarb" : "Old South Arabian", "Saur" : "Saurashtra", "Shaw" : "Shavian (Shaw)", 
    "Shrd" : "Sharada", "Sidd" : "Siddham, Siddhamātṛkā", "Sind" : "Sindhi, Khudawadi", "Sinh" : "Sinhala", "Sora" : "Sora Sompeng",
    "Sund" : "Sundanese", "Sylo" : "Syloti Nagri", "Syrc" : "Syriac", "Syre" : "Syriac (Estrangelo)", "Syrj" : "Syriac (Western)",
    "Syrn" : "Syriac (Eastern)", "Tagb" : "Tagbanwa", "Takr" : "Takri, Ṭāṅkrī", "Tale" : "Tai Le", "Talu" : "Tai Lue (New)", 
    "Taml" : "Tamil", "Tang" : "Tangut", "Tavt" : "Tai Viet", "Telu" : "Telugu", "Teng" : "Tengwar", "Tfng" : "Tifinagh (Berber)",
    "Tglg" : "Tagalog (Baybayin, Alibata)", "Thaa" : "Thaana", "Thai" : "Thai", "Tibt" : "Tibetan", "Tirh" : "Tirhuta", "Ugar" : "Ugaritic",
    "Vaii" : "Vai", "Wara" : "Warang Citi (Varang Kshiti)", "Wole" : "Woleai", "Xpeo" : "Old Persian", "Yiii" : "Yi", "Zzzz" : "Uncoded script"
}
_alldigits = [ "Default (0123456789)", "Arabic-Farsi", "Arabic-Hindi", "Bengali", "Burmese", "Devanagari", "Gujarati", "Gurmukhi", "Kannada", 
    "Khmer", "Lao", "Malayalam", "Oriya", "Tamil", "Telugu", "Thai", "Tibetan", "----", "Gondi-Gunjala", "Gondi-Masaram", "----", "Adlam", 
    "Ahom", "Balinese", "Bhaiksuki", "Brahmi", "Chakma", "Cham", "Gurmukhi", "Hanifi-Rohingya", "Javanese", "Kayah-Li", "Khudawadi", "Lepcha", 
    "Limbu", "Meetei-Mayek", "Modi", "Mongolian", "Mro", "Myanmar", "Myanmar-Shan", "Myanmar-Tai-Laing", "New-Tai-Lue", "Newa", "Nko", 
    "Nyiakeng-Puachue-Hmong", "Ol-Chiki", "Osmanya", "Pahawh-Hmong", "Persian", "Saurashtra", "Sharada", "Sinhala-Lith", "Sora-Sompeng", 
    "Sundanese", "Tai-Tham-Hora", "Tai-Tham-Tham", "Takri", "Tirhuta", "Urdu", "Vai", "Wancho", "Warang-Citi" ]

allbooks = [b.split("|")[0] for b in _bookslist.split() if b != "ZZZ|0"]
books = dict((b.split("|")[0], i+1) for i, b in enumerate(_bookslist.split()))
chaps = dict(b.split("|") for b in _bookslist.split())

class ParatextSettings:
    def __init__(self, basedir, prjid):
        self.dict = {}
        doc = et.parse(os.path.join(basedir, prjid, "Settings.xml"))
        for c in doc.getroot():
            self.dict[c.tag] = c.text
        langid = regex.sub('-(?=-|$)', '', self.dict['LanguageIsoCode'].replace(":", "-"))
        # print(langid)
        fname = os.path.join(basedir, prjid, langid+".ldml")
        if os.path.exists(fname):
            doc = et.parse(fname)
            for k in ['footnotes', 'crossrefs']:
                d = doc.find('.//characters/special/{{urn://www.sil.org/ldml/0.1}}exemplarCharacters[@type="{}"]'.format(k))
                if d is not None:
                    self.dict[k] = ",".join(regex.sub(r'^\[\s*(.*?)\s*\]', r'\1', d.text).split())
                    # print(k, self.dict[k].encode("unicode_escape"))

    def __getitem__(self, key):
        return self.dict[key]

    def get(self, key, default=None):
        return self.dict.get(key, default)

class PtxPrinterDialog:
    def __init__(self, allprojects, settings_dir):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(os.path.dirname(__file__), "ptxprint.glade"))
        self.builder.connect_signals(self)
        self.addCR("cb_digits", 0)
        self.addCR("cb_columns", 0)
        self.addCR("cb_script", 0)
        self.addCR("cb_chapfrom", 0)
        self.addCR("cb_chapto", 0)
        self.addCR("cb_blendedXrefCaller", 0)

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

        dia = self.builder.get_object("dlg_multiBookSelector")
        dia.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        self.logbuffer = StreamTextBuffer()
        self.builder.get_object("tv_logging").set_buffer(self.logbuffer)
        self.mw = self.builder.get_object("ptxprint")
        self.projects = self.builder.get_object("ls_projects")
        self.settings_dir = settings_dir
        self.ptsettings = None
        self.booklist = []
        self.processScript = None
        self.FrontPDFs = None
        self.BackPDFs = None
        self.watermarks = None
        for p in allprojects:
            self.projects.append([p])

    def run(self, callback):
        self.callback = callback
        self.mw.show_all()
        Gtk.main()

    def addCR(self, name, index):
        v = self.builder.get_object(name)
        setattr(self, name, v)
        c = Gtk.CellRendererText()
        v.pack_start(c, True)
        v.add_attribute(c, "text", index)

    def parse_fontname(self, font):
        m = re.match(r"^(.*?),?\s*((?:[^,\s]+\s+)*)(\d+(?:\.\d+)?)$", font)
        if m:
            styles = m.group(2).strip().split()
            if not m.group(1):
                return [styles[0], styles[1:], m.group(3)]
            else:
                return [m.group(1), styles, m.group(3)]
        else:
            return [font, [], 0]

    def get(self, wid, sub=0, asstr=False):
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
            val = w.get_font_name()
            v = val if asstr else self.parse_fontname(val)
        elif wid.startswith("c_"):
            v = w.get_active()
        elif wid.startswith("s_"):
            v = w.get_value()
        return v

    def set(self, wid, value):
        w = self.builder.get_object(wid)
        if wid.startswith("cb_"):
            model = w.get_model()
            e = w.get_child()
            if e is not None and isinstance(e, Gtk.Entry):
                e.set_text(value)
            else:
                for i, v in enumerate(model):
                    if v[w.get_id_column()] == value:
                        w.set_active_id(value)
                        w.emit("changed")
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

    def getBooks(self):
        if self.get('c_onebook'):
            return [self.get('cb_book')]
        elif len(self.booklist):
            return self.booklist
        else:
            return self.get('t_booklist').split()

    def onDestroy(self, btn):
        Gtk.main_quit()

    def onOK(self, btn):
        self.callback(self)

    def onCancel(self, btn):
        self.onDestroy(btn)

    def onScriptChanged(self, cb_script):
        # If there is a matching digit style for the script that has just been set, then turn that on (but it can be overridden later).
        try:
            self.cb_digits.set_active_id(self.get('cb_script'))
        except:
            self.cb_digits.grab_focus()  # this doesn't appear to do anything yet!

    def onFontChange(self, fbtn):
        font = fbtn.get_font_name()
        (family, style, size) = self.parse_fontname(font)
        style = [s.lower() for s in style if s not in ("Regular", "Medium")]
        label = self.builder.get_object("l_font")
        for s in ('bold', 'italic', 'bold italic'):
            sid = s.replace(" ", "")
            w = self.builder.get_object("f_"+sid)
            f = TTFont(family, " ".join(style + s.split()))
            fname = family + ", " + f.style + " " + size
            w.set_font_name(fname)
            # print(s, fname, f.extrastyles)
            if 'bold' in f.extrastyles:
                self.set("s_{}embolden".format(sid), 2)
            if 'italic' in f.extrastyles:
                self.set("s_{}slant".format(sid), 0.27)

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

    def onClickedIncludeFootnotes(self, c_includeFootnotes):
        status = self.get("c_includeFootnotes")
        for c in ("c_fnautocallers", "t_fncallers", "c_fnomitcaller", "c_fnpageresetcallers", "c_fnparagraphednotes"):
            self.builder.get_object(c).set_sensitive(status)
        
    def onClickedIncludeXrefs(self, c_includeXrefs):
        status = self.get("c_includeXrefs")
        for c in ("c_xrautocallers", "t_xrcallers", "c_xromitcaller", "c_xrpageresetcallers", "c_paragraphedxrefs"):
            self.builder.get_object(c).set_sensitive(status)

    def onPageGutterChanged(self, c_pagegutter):
        status = self.get("c_pagegutter")
        gtr = self.builder.get_object("s_pagegutter")
        gtr.set_sensitive(status)
        if status:
            gtr.grab_focus() 

    def onColumnsChanged(self, cb_Columns):
        status = self.get("cb_columns") == "Double"
        for c in ("c_verticalrule", "l_gutterWidth", "s_colgutterfactor"):
            self.builder.get_object(c).set_sensitive(status)

    def onBookSelectorChange(self, c_onebook):
        status = self.get("c_onebook")
        cmb = self.builder.get_object("c_combine")
        cmb.set_sensitive(not status)
        toc = self.builder.get_object("c_autoToC") # Ensure that we're not trying to build a ToC for a single book!
        toc.set_sensitive(not status)
        toc.set_active(False)
        for c in ("l_chapfrom", "cb_chapfrom", "l_chapto", "cb_chapto"):
            self.builder.get_object(c).set_sensitive(status)
            
    def onFigsChanged(self, c_includefigs):
        status = self.get("c_includefigs")
        for c in ("c_figexclwebapp", "c_figplaceholders", "c_fighiderefs"):
            self.builder.get_object(c).set_sensitive(status)

    def onInclFrontMatterChanged(self, c_inclFrontMatter):
        self.builder.get_object("btn_selectFrontPDFs").set_sensitive(self.get("c_inclFrontMatter"))
        # self.builder.get_object("l_frontMatterPDFs").set_sensitive(self.get("c_inclFrontMatter"))

    def onInclBackMatterChanged(self, c_inclBackMatter):
        self.builder.get_object("btn_selectBackPDFs").set_sensitive(self.get("c_inclBackMatter"))
        # self.builder.get_object("l_backMatterPDFs").set_sensitive(self.get("c_inclBackMatter"))
            
    def onApplyWatermarkChanged(self, c_applyWatermark):
        self.builder.get_object("btn_selectWatermarkPDF").set_sensitive(self.get("c_applyWatermark"))
        # self.builder.get_object("l_watermarkPDF").set_sensitive(self.get("c_applyWatermark"))
    
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
        
    def onUseModsTexClicked(self, c_useModsTex):
        self.builder.get_object("btn_editModsTeX").set_sensitive(self.get("c_useModsTex"))
        
    def onUseModsStyClicked(self, c_useModsSty):
        self.builder.get_object("btn_editModsSty").set_sensitive(self.get("c_useModsSty"))
        
    def onChooseBooksClicked(self, btn):
        dia = self.builder.get_object("dlg_multiBookSelector")
        mbs_grid = self.builder.get_object("mbs_grid")
        mbs_grid.forall(mbs_grid.remove)
        lsbooks = self.builder.get_object("ls_books")
        self.alltoggles = []
        for i, b in enumerate(lsbooks):
            tbox = Gtk.ToggleButton(b[0])
            tbox.show()
            self.alltoggles.append(tbox)
            mbs_grid.attach(tbox, i // 20, i % 20, 1, 1)
        response = dia.run()
        if response == Gtk.ResponseType.OK:
            self.booklist = [b.get_label() for b in self.alltoggles if b.get_active()]
            t_booklist = " ".join(self.booklist)
        dia.hide()  

    def onClickmbs_all(self, btn):
        for b in self.alltoggles:
            b.set_active(True)

    def onClickmbs_OT(self, btn):
        for b in self.alltoggles:
            if b.get_label() in allbooks[0:39]:
                b.set_active(True)

    def onClickmbs_NT(self, btn):
        for b in self.alltoggles:
            if b.get_label() in allbooks[39:66]:
                b.set_active(True)

    def onClickmbs_DC(self, btn):
        for b in self.alltoggles:
            if b.get_label() in allbooks[66:84]:
                b.set_active(True)

    def onClickmbs_xtra(self, btn):
        for b in self.alltoggles:
            if b.get_label() in allbooks[84:]:
                b.set_active(True)

    def onClickmbs_none(self, btn):
        for b in self.alltoggles:
            b.set_active(False)

    def _setchap(self, ls, start, end):
        ls.clear()
        for c in range(start, end+1):
            ls.append([str(c)])

    def onBookChange(self, cb_book):
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
        self.prjid = self.get("cb_project")
        self.ptsettings = None
        lsbooks = self.builder.get_object("ls_books")
        lsbooks.clear()
        if not self.prjid:
            return
        self.ptsettings = ParatextSettings(self.settings_dir, self.prjid)
        bp = self.ptsettings['BooksPresent']
        for i, b in enumerate(allbooks):
            if i < len(bp) and bp[i] == "1":
                lsbooks.append([b])
        cb_bk = self.builder.get_object("cb_book")
        cb_bk.set_active(0)
        font_name = self.ptsettings['DefaultFont'] + ", " + self.ptsettings['DefaultFontSize']
        self.set('f_body', font_name)
        configfile = os.path.join(self.settings_dir, self.prjid, "ptxprint.cfg")
        if os.path.exists(configfile):
            info = Info(self, self.settings_dir, self.ptsettings)
            config = configparser.ConfigParser()
            config.read(configfile)
            info.loadConfig(self, config)

    def onEditChangesFile(self, cb_prj):
        self.prjid = self.get("cb_project")
        changesfile = os.path.join(self.settings_dir, self.prjid, "PrintDraftChanges.txt")
        if os.path.exists(changesfile):
            os.startfile(changesfile)

    def onEditModsTeX(self, cb_prj):
        self.prjid = self.get("cb_project")
        modstexfile = os.path.join(self.settings_dir, self.prjid, "PrintDraft", "PrintDraft-mods.tex")
        if os.path.exists(modstexfile):
            os.startfile(modstexfile)

    def onEditModsSty(self, cb_prj):
        self.prjid = self.get("cb_project")
        modsstyfile = os.path.join(self.settings_dir, self.prjid, "PrintDraft", "PrintDraft-mods.sty")
        if os.path.exists(modsstyfile):
            os.startfile(modsstyfile)

    def onSelectScriptClicked(self, btn_selectScript):
        CustomScript = self.fileChooser("Select a Custom Script file", 
                filters = {"Executable Scripts": {"patterns": "*.bat", "mime": "application/bat"}},
                # ),("*.sh", "mime": "application/x-sh")
                multiple = False)
        if FrontPDFs is not None:
            self.FrontPDFs = FrontPDFs
            selectFrontPDFs.set_tooltip_text("\n".join('{}'.format(s) for s in FrontPDFs))
        else:
            self.FrontPDFs = None
            selectFrontPDFs.set_tooltip_text("")
            self.builder.get_object("btn_selectFrontPDFs").set_sensitive(False)
            self.builder.get_object("c_inclFrontMatter").set_active(False)


        win = FileChooserWindow()
        if fcFilepath != None:
            self.builder.get_object("l_script2process").set_text("Sorry, this hasn't been implemented yet!")
            # self.builder.get_object("l_script2process").set_text("\n".join('{}'.format(s) for s in path))
        else:
            for c in ("btn_selectScript", "c_processScriptBefore", "c_processScriptAfter", "l_script2process"):
                self.builder.get_object(c).set_sensitive(False)
            self.builder.get_object("c_processScript").set_active(False)

    def onFrontPDFsClicked(self, btn_selectFrontPDFs):
        FrontPDFs = self.fileChooser("Select one or more PDF(s) for FRONT matter", 
                filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                multiple = True)
        if FrontPDFs is not None:
            self.FrontPDFs = FrontPDFs
            selectFrontPDFs.set_tooltip_text("\n".join('{}'.format(s) for s in FrontPDFs))
        else:
            self.FrontPDFs = None
            selectFrontPDFs.set_tooltip_text("")
            self.builder.get_object("btn_selectFrontPDFs").set_sensitive(False)
            self.builder.get_object("c_inclFrontMatter").set_active(False)

    def onBackPDFsClicked(self, btn_selectBackPDFs):
        BackPDFs = self.fileChooser("Select one or more PDF(s) for BACK matter", 
                filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                multiple = True)
        if BackPDFs is not None:
            self.BackPDFs = BackPDFs
            selectBackPDFs.set_tooltip_text("\n".join('{}'.format(s) for s in BackPDFs))
        else:
            self.BackPDFs = None
            selectBackPDFs.set_tooltip_text("")
            self.builder.get_object("btn_selectBackPDFs").set_sensitive(False)
            self.builder.get_object("c_inclBackMatter").set_active(False)

    def onWatermarkPDFclicked(self, btn_selectWatermarkPDF):
        watermarks = self.fileChooser("Select Watermark PDF file", 
                filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                multiple = False)
        if watermarks is not None:
            self.watermarks = watermarks[0]
            selectWatermarkPDF.set_tooltip_text(watermarks[0])
        else:
            self.watermarks = None
            selectWatermarkPDF.set_tooltip_text("")
            self.builder.get_object("btn_selectWatermarkPDF").set_sensitive(False)
            self.builder.get_object("c_applyWatermark").set_active(False)

    def ontv_sizeallocate(self, atv, dummy):
        b = atv.get_buffer()
        it = b.get_iter_at_offset(-1)
        atv.scroll_to_iter(it, 0, False, 0, 0)

    def fileChooser(self, title, filters = None, multiple = True, folder = False):
        dialog = Gtk.FileChooserDialog(title, None,
            (Gtk.FileChooserAction.SELECT_FOLDER if folder else Gtk.FileChooserAction.OPEN),
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_default_size(1000, 600)
        dialog.set_select_multiple(multiple)
        if len(filters):
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
            fcFilepath = dialog.get_filenames()
        dialog.destroy()
        return fcFilepath

class Info:
    _mappings = {
        "project/id":               (None, lambda w,v: w.get("cb_project")),
        "project/book":             ("cb_book", None),
        # "project/frontincludes":    (None, lambda w,v: "\n".join('\\includepdf{{{}}}'.format(s) for s in w.builder.get_object("tb_frontPDFs").get_text().split("\n"))),
        # "project/watermarkpdf":     (None, lambda w,v: re.sub(r"\\","/", w.watermarks) if w.watermarks is not None else "A5-Draft.pdf"),
        "project/frontincludes":    (None, lambda w,v: "\n".join('\\includepdf{{"{}"}}'.format(s)) for s in FrontPDFs if FrontPDFs is not None else ""),
        "project/backincludes":     (None, lambda w,v: "\n".join('\\includepdf{{"{}"}}'.format(re.sub(r"\\","/",s)) for s in BackPDFs)),
        "project/usechangesfile":   ("usePrintDraftChanges", lambda w,v :"true" if v else "false"),
        "project/processscript":    ("c_processScript", lambda w,v :"true" if v else "false"),

        "paper/height":             (None, lambda w,v: re.sub(r"^.*?,\s*(.+?)\s*(?:\(.*|$)", r"\1", w.get("cb_pagesize")) or "210mm"),
        "paper/width":              (None, lambda w,v: re.sub(r"^(.*?)\s*,.*$", r"\1", w.get("cb_pagesize")) or "148mm"),
        "paper/pagesize":           ("cb_pagesize", None),
        "paper/ifwatermark":          ("c_applyWatermark", lambda w,v: "" if v else "%"),
        "paper/watermarkpdf":       (None, lambda w,v: re.sub(r"\\","/", w.watermarks) if w.watermarks is not None else "A5-Draft.pdf"),
        "paper/ifcropmarks":        ("c_cropmarks", lambda w,v :"true" if v else "false"),
        "paper/ifverticalrule":     ("c_verticalrule", lambda w,v :"true" if v else "false"),
        "paper/margins":            ("s_margins", lambda w,v: round(v) or "14"),
        "paper/topmarginfactor":    ("s_topmarginfactor", lambda w,v: round(v, 2) or "1.15"),
        "paper/bottommarginfactor": ("s_bottommarginfactor", lambda w,v: round(v, 2) or "1.15"),
        "paper/sidemarginfactor":   ("s_sidemarginfactor", lambda w,v: round(v, 2) or "1.00"),
        "paper/ifaddgutter":        ("c_pagegutter", lambda w,v :"true" if v else "false"),
        "paper/gutter":             ("s_pagegutter", lambda w,v: round(v) or "14"),
        #"paper/columns":            ("cb_columns", lambda w,v: "1" if v == "Single" else "2"),
        "paper/columns":            ("cb_columns", lambda w,v: w.builder.get_object('cb_columns').get_active_id()),
        "paper/fontfactor":         ("s_fontsize", lambda w,v: round((v / 12), 3) or "1.000"),

        "paragraph/linespacing":    ("s_linespacing", lambda w,v: round(v, 1)),

        "document/toc":             ("c_autoToC", lambda w,v: "" if v else "%"),
        "document/toctitle":        ("t_tocTitle", lambda w,v: v or ""),
        "document/chapfrom":        ("cb_chapfrom", lambda w,v: w.builder.get_object("cb_chapfrom").get_active_id()),
        "document/chapto":          ("cb_chapto", lambda w,v: w.builder.get_object("cb_chapto").get_active_id()),
        "document/colgutterfactor": ("s_colgutterfactor", lambda w,v: round(v) or "15"),
        "document/ifrtl":           ("c_rtl", lambda w,v :"true" if v else "false"),
        "document/iflinebreakon":   ("c_linebreakon", lambda w,v: "" if v else "%"),
        # "document/script":        ("cb_script", lambda w,v: "mymr"),
        "document/script":          ("cb_script", lambda w,v: ";script="+w.builder.get_object('cb_script').get_active_id().lower() if w.builder.get_object('cb_script').get_active_id() != "Zyyy" else ""),
        "document/digitmapping":    ("cb_digits", lambda w,v: ";mapping="+v.lower()+"digits" if v != "Default" else ""),
        "document/linebreaklocale": ("t_linebreaklocale", lambda w,v: v or ""),
        "document/ch1pagebreak":    ("c_ch1pagebreak", lambda w,v: "true" if v else "false"),
        "document/ifomitchapternum": ("c_omitchapternumber", lambda w,v: "true" if v else "false"),
        "document/ifomitallchapters": ("c_omitchapternumber", lambda w,v: "" if v else "%"),
        "document/ifomitverseone":  ("c_omitverseone", lambda w,v: "true" if v else "false"),
        "document/ifomitallverses": ("c_omitallverses", lambda w,v: "" if v else "%"),
        "document/ifomitallversetext": ("c_omitallverseText", lambda w,v: "true" if v else "false"),
        "document/iffigures":       ("c_includefigs", lambda w,v :"true" if v else "false"),
        "document/iffigexclwebapp": ("c_figexclwebapp", lambda w,v: "true" if v else "false"),
        "document/iffigplaceholders": ("c_figplaceholders", lambda w,v :"true" if v else "false"),
        "document/iffighiderefs":   ("c_fighiderefs", lambda w,v :"true" if v else "false"),
        "document/ifjustify":       ("c_justify", lambda w,v: "true" if v else "false"),
        "document/crossspacecntxt": ("cb_crossSpaceContextualization", lambda w,v: "0" if v == "None" else "1" if v == "Some" else "2"),
        "document/hangpoetry":      ("c_hangpoetry", lambda w,v: "" if v else "%"),
        "document/preventorphans":  ("c_preventorphans", lambda w,v: "true" if v else "false"),
        "document/preventwidows":   ("c_preventwidows", lambda w,v: "true" if v else "false"),
        "document/supresssectheads": ("c_omitSectHeads", lambda w,v: "true" if v else "false"),
        "document/supressparallels": ("c_omitParallelRefs", lambda w,v: "true" if v else "false"),
        "document/supressbookintro": ("c_omitBookIntro", lambda w,v: "true" if v else "false"),
        "document/supressintrooutline": ("c_omitIntroOutline", lambda w,v: "true" if v else "false"),
        "document/supressindent":   ("c_omit1paraIndent", lambda w,v: "false" if v else "true"),

        "header/headerposition":    ("s_headerposition", lambda w,v: round(v, 2) or "0.50"),
        "header/footerposition":    ("s_footerposition", lambda w,v: round(v, 2) or "0.50"),
        "header/ifomitrhchapnum":   ("c_omitrhchapnum", lambda w,v :"true" if v else "false"),
        "header/ifverses":          ("c_hdrverses", lambda w,v :"true" if v else "false"),
        "header/ifrhrule":          ("c_rhrule", lambda w,v: "" if v else "%"),
        "header/ruleposition":      ("s_rhruleposition", lambda w,v: v or "10"),
        "header/hdrleftinner":      ("cb_hdrleft", lambda w,v: v or "-empty-"),
        "header/hdrcenter":         ("cb_hdrcenter", lambda w,v: v or "-empty-"),
        "header/hdrrightouter":     ("cb_hdrright", lambda w,v: v or "-empty-"),
        "header/mirrorlayout":      ("c_mirrorpages", lambda w,v: "true" if v else "false"),
        
        "footer/includefooter":     ("c_runningFooter", lambda w,v :"true" if v else "false"),
        "footer/ftrcenter":         ("t_runningFooter", lambda w,v: v if w.get("c_runningFooter") else ""),

        "notes/ifomitfootnoterule": (None, lambda w,v: "%" if w.get("c_footnoterule") else ""),
        "notes/blendfnxr":          ("c_blendfnxr", lambda w,v :"true" if v else "false"),

        "notes/includefootnotes":   ("c_includeFootnotes", lambda w,v: "%" if v else ""),
        "notes/fncallers":          ("t_fncallers", lambda w,v: v if w.get("c_fnautocallers") else ""),
        "notes/fnresetcallers":     ("c_fnpageresetcallers", lambda w,v: "" if v else "%"),
        "notes/fnomitcaller":       ("c_fnomitcaller", lambda w,v: "%" if v else ""),
        "notes/fnparagraphednotes": ("c_fnparagraphednotes", lambda w,v: "" if v else "%"),

        "notes/includexrefs":       ("c_includeXrefs", lambda w,v: "%" if v else ""),
        "notes/xrcallers":          ("t_xrcallers", lambda w,v: v if w.get("c_xrautocallers") else ""),
        "notes/xrresetcallers":     ("c_xrpageresetcallers", lambda w,v: "" if v else "%"),
        "notes/xromitcaller":       ("c_xromitcaller", lambda w,v: "%" if v else ""),
        "notes/xrparagraphednotes": ("c_paragraphedxrefs", lambda w,v: "" if v else "%"),

        "fontbold/fakeit":          ("c_fakebold", lambda w,v :"true" if v else "false"),
        "fontitalic/fakeit":        ("c_fakeitalic", lambda w,v :"true" if v else "false"),
        "fontbolditalic/fakeit":    ("c_fakebolditalic", lambda w,v :"true" if v else "false"),
        "fontbold/embolden":        ("s_boldembolden", lambda w,v: ";embolden={:.2f}".format(v) if v != 0.00 and w.get("c_fakebold") else ""),
        "fontitalic/embolden":      ("s_italicembolden", lambda w,v: ";embolden={:.2f}".format(v) if v != 0.00 and w.get("c_fakeitalic") else ""),
        "fontbolditalic/embolden":  ("s_bolditalicembolden", lambda w,v: ";embolden={:.2f}".format(v) if v != 0.00 and w.get("c_fakebolditalic") else ""),
        "fontbold/slant":           ("s_boldslant", lambda w,v: ";slant={:.4f}".format(v) if v != 0.0000 and w.get("c_fakebold") else ""),
        "fontitalic/slant":         ("s_italicslant", lambda w,v: ";slant={:.4f}".format(v) if v != 0.0000 and w.get("c_fakeitalic") else ""),
        "fontbolditalic/slant":     ("s_bolditalicslant", lambda w,v: ";slant={:.4f}".format(v) if v != 0.0000 and w.get("c_fakebolditalic") else ""),
    }
    _fonts = {
        "fontregular/name": "f_body",
        "fontbold/name": "f_bold",
        "fontitalic/name": "f_italic",
        "fontbolditalic/name": "f_bolditalic"
    }
    _hdrmappings = {
        "First Reference":  r"\firstref",
        "Last Reference":   r"\lastref",
        "Page Number":      r"\pagenumber",
        "Reference Range":  r"\rangeref",
        "-empty-":          r"\empty"
    }
    _settingmappings = {
        "notes/xrcallers": "crossrefs",
        "notes/fncallers": "footnotes"
    }

    def __init__(self, printer, path, ptsettings=None):
        self.ptsettings = ptsettings
        self.changes = None
        self.localChanges = None
        self.dict = {"/ptxpath": path}
        for k, v in self._mappings.items():
            val = printer.get(v[0]) if v[0] is not None else None
            if v[1] is not None:
                self.dict[k] = v[1](printer, val)
        self.processFonts(printer)
        self.processHdrFtr(printer)
        self.makelocalChanges(printer)

    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def processFonts(self, printer):
#        import pdb;pdb.set_trace()
        for p, wid in self._fonts.items():
            (family, style, size) = printer.get(wid)
            f = TTFont(family, " ".join(style))
            if 'Silf' in f:
                engine = "/GR"
            else:
                engine = ""
            s = ""
            if len(style):
                s = "/" + "".join(x[0].upper() for x in style)
            self.dict[p] = family + engine + s

    def processHdrFtr(self, printer):
        mirror = printer.get('c_mirrorpages')
        for side in ('left', 'center', 'right'):
            v = printer.get("cb_hdr" + side)
            t = self._hdrmappings.get(v, v)
            # I'm not sure if there is a more elegant/shorter/Pythonic way of doing this; but this works!
            if side == 'left':
                if mirror:
                    self.dict['header/even{}'.format('right')] = t
                else:
                    self.dict['header/even{}'.format(side)] = t
            elif side == 'right':
                if mirror:
                    self.dict['header/even{}'.format('left')] = t
                else:
                    self.dict['header/even{}'.format(side)] = t
            else: # centre
                self.dict['header/even{}'.format(side)] = t
            
            self.dict['header/odd{}'.format(side)] = t

    def asTex(self, template="template.tex"):
 #       import pdb;pdb.set_trace()
        for k, v in self._settingmappings.items():
            if self.dict[k] == "":
                self.dict[k] = self.ptsettings.dict.get(v, "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z")
        res = []
        with open(os.path.join(os.path.dirname(__file__), template)) as inf:
            for l in inf.readlines():
                if l.startswith(r"\ptxfile"):
                    for f in self.dict['project/books']:
                        res.append("\\ptxfile{{{}}}\n".format(os.path.abspath(f)))
                else:
                    res.append(l.format(**self.dict))
        return "".join(res)

    def convertBook(self, bk, outdir, prjdir):
        if self.ptsettings is None:
            self.ptsettings = ParatextSettings(prjdir)
        if self.changes is None and self.dict['project/usechangesfile']:  # TO-DO: check that this is doing what it should 
            self.changes = self.readChanges(os.path.join(prjdir, 'PrintDraftChanges.txt'))
        customsty = os.path.join(prjdir, 'custom.sty')
        if not os.path.exists(customsty):
            open(customsty, "w").close()
        fbkfm = self.ptsettings['FileNameBookNameForm']
        bknamefmt = fbkfm.replace("MAT","{bkid}").replace("41","{bknum:02d}") + \
                    self.ptsettings['FileNamePostPart']
        fname = bknamefmt.format(bkid=bk, bknum=books.get(bk, 0))
        infname = os.path.join(prjdir, fname)
        if self.changes is not None or self.localChanges is not None:
            outfname = os.path.join(outdir, fname)
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:]
            with open(infname, "r", encoding="utf-8") as inf:
                dat = inf.read()
                for c in self.changes + self.localChanges:
                    if c[0] is None:
                        dat = c[1].sub(c[2], dat)
                    else:
                        newdat = [c[0].split(dat)]
                        for i in range(1, len(newdat), 2):
                            newdat[i] = c[1].sub(c[2], newdat[i])
                        dat = "".join(newdat)
            with open(outfname, "w", encoding="utf-8") as outf:
                outf.write(dat)
            return outfname
        else:
            return infname

    def readChanges(self, fname):
        changes = []
        if not os.path.exists(fname):
            return []
        with open(fname, "r", encoding="utf-8") as inf:
            for l in inf.readlines():
                l = l.strip().replace(u"\uFEFF", "")
                l = re.sub(r"\s*#.*$", "", l)
                if not len(l):
                    continue
                m = re.match(r"^(['\"])(.*?)(?<!\\)\1\s*>\s*(['\"])(.*?)(?<!\\)\3", l)
                if m:
                    # print(m.group(2).encode("utf-8") + " > " + m.group(4).encode("utf-8"))
                    changes.append((None, regex.compile(m.group(2), flags=regex.M), m.group(4)))
                    continue
                m = re.match(r"^in\s+(['\"])(.*?)(?<!\\)\1\s*:\s*(['\"])(.*?)(?<!\\)\3\s*>\s*(['\"])(.*?)(?<!\\)\5", l)
                if m:
                    changes.append((regex.compile("("+m.group(2)+")", flags=regex.M), regex.compile(m.group(4), flags=regex.M), m.group(6)))
        if not len(changes):
            return None
        return changes
            
    def makelocalChanges(self, printer):
        self.localChanges = []
        
        # This section handles PARTIAL books (from chapter X to chapter Y)
        if printer.get("c_onebook"):
            bk = printer.get("cb_book")
            first = int(printer.get("cb_chapfrom"))
            last = int(printer.get("cb_chapto"))
            if first > 1:
                self.localChanges.append((None, regex.compile(r"\\c 1 ?\r?\n.+(?=\\c {} ?\r?\n)".format(first), flags=regex.S), ""))
            if last < int(chaps.get(bk)):
                self.localChanges.append((None, regex.compile(r"\\c {} ?\r?\n.+".format(last+1), flags=regex.S), ""))
            
        # Glossary Word markup: We always want to strip out the 2nd word (which links to the Glossary book)
        # BUT how to best mark up the actual glossary word for user? Give user some good options in the UI.
        if True: 
        #	Remove the second half of the \w word-in-text|glossary-form-of-word\w*  Should we mark ⸤glossary⸥ words like this?
            self.localChanges.append((None, regex.compile(r"\\w (.+?)(\|.+?)?\\w\*", flags=regex.M), r"\u2E24\1\u2E25"))   # Drop 2nd half of Glossary words
        
        if not printer.get("c_includefigs"):
            self.localChanges.append((None, regex.compile(r"\\fig .*?\\fig\*", flags=regex.M), ""))             # Drop ALL Figures
        else:
            self.localChanges.append((None, regex.compile(r"\.[Tt][Ii][Ff]", flags=regex.M), ".jpg"))           # Change all TIFs to JPGs
            if printer.get("c_fighiderefs"):
                self.localChanges.append((None, regex.compile(r"(\\fig .*?)(\d+\:\d+(\-\d+)?)(.*?\\fig\*)", flags=regex.M), r"\1\4")) # remove ch:vs ref from caption
        
        if printer.get("c_omitBookIntro"):
            self.localChanges.append((None, regex.compile(r"\\i(s|m|mi|p|pi|li\d?|pq|mq|pr|b|q\d?) .+?\r?\n", flags=regex.M), "")) # Drop Introductory matter

        if printer.get("c_omitIntroOutline"):
            self.localChanges.append((None, regex.compile(r"\\(iot|io\d) [^\\]+", flags=regex.M), ""))          # Drop ALL Intro Outline matter
            self.localChanges.append((None, regex.compile(r"\\ior .+?\\ior\*\s?\r?\n", flags=regex.M), ""))     # and remove Intro Outline References

        if printer.get("c_omitSectHeads"):
            self.localChanges.append((None, regex.compile(r"\\s .+", flags=regex.M), ""))                       # Drop ALL Section Headings

        if printer.get("c_omitParallelRefs"):
            self.localChanges.append((None, regex.compile(r"\\r .+", flags=regex.M), ""))                       # Drop ALL Parallel Passage References

        if printer.get("c_blendfnxr"):  # this needs further testing before deleting the 4 older RegExs
            self.localChanges.append((None, regex.compile(r"\\x(\s.+?)\\xo(\s\d+:\d+) \\xt(.+?)\\x\*", flags=regex.M), r"\\f\1\\fr\2 \\ft\3\\f*"))
            # To merge/blend \f and \x together, simply change all (\x to \f) (\xo to \fr) (\xq to \fq) (\xt to \ft) and (\f* to \x*)
            # self.localChanges.append((None, regex.compile(r"\\x . ", flags=regex.M), r"\\f # "))
            # self.localChanges.append((None, regex.compile(r"\\x\* ", flags=regex.M), r"\\f* "))
            # self.localChanges.append((None, regex.compile(r"\\xq ", flags=regex.M), r"\\fq "))
            # self.localChanges.append((None, regex.compile(r"\\xt ", flags=regex.M), r"\\ft "))
        
        if printer.get("c_preventorphans"): 
            # Keep final two words of \q lines together [but this doesn't work if there is an \f or \x at the end of the line] 
            self.localChanges.append((None, regex.compile(r"(\\q\d?(\s?\r?\n?\\v)?( \S+)+) (\S+\s*\n)", flags=regex.M), r"\1\u00A0\4"))   

        if printer.get("c_preventwidows"):
            # Push the verse number onto the next line (using NBSP) if there is a short widow word (3 characters or less) at the end of the line
            self.localChanges.append((None, regex.compile(r"(\\v \d+ [\w][\w]?[\w]?) ", flags=regex.M), r"\1\u00A0")) 

        if printer.get("c_ch1pagebreak"):
            self.localChanges.append((None, regex.compile(r"(\\c 1 ?\r?\n)", flags=regex.M), r"\pagebreak\r\n\1"))

        # if printer.get("c_glueredupwords"):  # broken??? at present as it 
            # self.localChanges.append((None, regex.compile(r"(?<=[ ])(\w\w\w+) *\1(?=[\s,.!?])", flags=regex.M), r"\1\u00A0\1")) # keep reduplicated words together
            
        for c in range(1,3):
            if not printer.get("c_usetoc{}".format(c)):
                self.localChanges.append((None, regex.compile(r"(\\toc{} .+)".format(c), flags=regex.M), r""))
            
            # self.builder.get_object(c).set_sensitive(status)
        
        # if True:
            # self.localChanges.append((None, regex.compile(r"(\\toc3 .+)", flags=regex.M), r""))
            # self.localChanges.append((None, regex.compile(r"(\\c\s1\s?\r?\n)", flags=regex.S), r"\skipline\n\hrule\r\n\1")) # this didn't work. I wonder why.

        if printer.get("c_omitallverseText"):
            self.localChanges.append((None, regex.compile(r"\\c 1 ?\r?\n.+".format(first), flags=regex.S), ""))
            
        return self.localChanges
        # Examples: from textPreprocess.py RaPuMa
        # Change cross reference into footnotes
        #contents = re.sub(ur'\\x(\s.+?)\\xo(\s\d+:\d+)(.+?)\\x\*', ur'\\f\1\\fr\2 \\ft\3\\f*', contents)

        # Insert horizontal rule after intro section
        #contents = re.sub(ur'(\\c\s1\r\n)', ur'\skipline\n\hrule\r\n\1', contents)

        # Insert a chapter label marker with zwsp to center the chapter number
        #contents = re.sub(ur'(\\c\s1\r\n)', ur'\cl \u200b\r\n\1', contents)

    def createConfig(self, printer):
        config = configparser.ConfigParser()
        for k, v in self._mappings.items():
            if v[0] is None:
                continue
            (sect, key) = k.split("/")
            if not config.has_section(sect):
                config.add_section(sect)
            val = printer.get(v[0], asstr=True)
            if k in self._settingmappings:
                # print("Testing {} against '{}'".format(k, val))
                if val == "" or val == self.ptsettings.dict.get(self._settingmappings[k], ""):
                    continue
            config.set(sect, key, str(val))
        for k, v in self._fonts.items():
            (sect, key) = k.split("/")
            if not config.has_section(sect):
                config.add_section(sect)
            config.set(sect, key, printer.get(v, asstr=True))
        return config

    def loadConfig(self, printer, config):
        for sect in config.sections():
            for opt in config.options(sect):
                key = "{}/{}".format(sect, opt)
                if key in self._mappings:
                    v = self._mappings[key]
                    #print(sect + "/" + opt + ": " + v[0])
                    val = None
                    if v[0] is None:
                        continue
                    if v[0].startswith("cb_") or v[0].startswith("t_") or v[0].startswith("f_"):
                        val = config.get(sect, opt)
                    if v[0].startswith("s_"):
                        val = float(config.get(sect, opt))
                        #printer.set(v[0], round(config.get(sect, opt)),2)
                    elif v[0].startswith("c_"):
                        val = config.getboolean(sect, opt)
                    if val is not None:
                        self.dict[key] = val
                        printer.set(v[0], val)
                elif key in self._fonts:
                    v = self._fonts[key]
                    printer.set(v, config.get(sect, opt))
        for k, v in self._settingmappings.items():
            (sect, name) = k.split("/")
            try:
                val = config.get(sect, name)
            except configparser.NoOptionError:
                printer.set(self._mappings[k][0], self.ptsettings.dict.get(v, ""))
                self.dict[k] = self.ptsettings.get(v, "")

