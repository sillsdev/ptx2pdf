#!/usr/bin/python3

import sys, os, re, regex, gi, random
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import xml.etree.ElementTree as et
from ptxprint.font import TTFont
from ptxprint.runner import StreamTextBuffer
# from PIL import Image
import configparser
import traceback

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
_allscripts = { "Zyyy" : "Default", "Adlm" : "Adlam", "Afak" : "Afaka", "Aghb" : "Caucasian Albanian", "Ahom" : "Ahom, Tai Ahom", 
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
_alldigits = [ "Default", "Arabic-Farsi", "Arabic-Hindi", "Bengali", "Burmese", "Devanagari", "Gujarati", "Gurmukhi", "Kannada", 
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
        self.addCR("cb_script", 0)
        self.addCR("cb_chapfrom", 0)
        self.addCR("cb_chapto", 0)
        self.addCR("cb_blendedXrefCaller", 0)
        self.addCR("cb_glossaryMarkupStyle", 0)

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
        self.CustomScript = None
        self.FrontPDFs = None
        self.BackPDFs = None
        self.watermarks = None
        self.customFigFolder = None
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
        m = re.match(r"^(.*?)(\d+(?:\.\d+)?)$", font)
        if m:
            return [m.group(1), int(m.group(2))]
        else:
            return [font, 0]

    def get(self, wid, sub=0, asstr=False):
        # print(wid) # This is useful for troubleshooting errors with getting (misnamed) widgets
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
            # print("setting font {} to {}".format(wid, value))
            w.set_font_name(value)
            w.emit("font-set")
        elif wid.startswith("c_"):
            w.set_active(value)
        elif wid.startswith("s_"):
            w.set_value(value)
        elif wid.startswith("btn_"):
            w.set_tooltip_text(value)

    def getBooks(self):
        if not self.get('c_multiplebooks'):
            return [self.get('cb_book')]
        elif len(self.booklist):
            return self.booklist
        else:
            return self.get('t_booklist').split()

    def getBookFilename(self, bk, prjdir):
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

    def onVariableLineSpacingClicked(self, c_variableLineSpacing):
        status = self.get("c_variableLineSpacing")
        for c in ("s_linespacingmin", "s_linespacingmax", "l_min", "l_max"):
            self.builder.get_object(c).set_sensitive(status)

    def onUseIllustrationsClicked(self, c_includeillustrations):
        status = self.get("c_includeillustrations")
        for c in ("c_includefigsfromtext", "c_usePicList", "l_useFolder", "c_useFiguresFolder", "c_useLocalFiguresFolder", "c_useCustomFolder",
                  "c_convertTIFtoPNG", "btn_selectFigureFolder", "l_useFiguresFolder", "l_useLocalFiguresFolder",
                  "c_figexclwebapp", "c_figplaceholders", "c_fighiderefs"):
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
        self.GenerateNestedStyles(None)
        
    def onClickedIncludeXrefs(self, c_includeXrefs):
        status = self.get("c_includeXrefs")
        for c in ("c_xrautocallers", "t_xrcallers", "c_xromitcaller", "c_xrpageresetcallers", "c_paragraphedxrefs"):
            self.builder.get_object(c).set_sensitive(status)
        self.GenerateNestedStyles(None)

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
        
    def onUseModsTexClicked(self, c_useModsTex):
        self.builder.get_object("btn_editModsTeX").set_sensitive(self.get("c_useModsTex"))
        
    def onUseModsStyClicked(self, c_useModsSty):
        self.builder.get_object("btn_editModsSty").set_sensitive(self.get("c_useModsSty"))
        
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
            mbs_grid.attach(tbox, i // 20, i % 20, 1, 1)
        response = dia.run()
        if response == Gtk.ResponseType.OK:
            self.booklist = [b.get_label() for b in self.alltoggles if b.get_active()]
            bl.set_text(" ".join(b for b in self.booklist))
            self.builder.get_object("c_multiplebooks").set_active(True)
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
        if FrontPDFs is not None:
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
        if BackPDFs is not None:
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
        if watermarks is not None:
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
        for bk in self.getBooks():
            prjid = self.get("cb_project")
            prjdir = os.path.join(self.settings_dir, self.prjid)
            tmpdir = os.path.join(prjdir, 'PrintDraft') if self.get("c_useprintdraftfolder") else r"C:\temp"  # args.directory
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
                        # print(f[0]+"|"+f[1]+"|"+f[5]+f[6])
                        picfname = re.sub(r"\.[Tt][Ii][Ff]",".jpg",f[0])           # Change all TIFs to JPGs
                        pageposn = random.choice(_picposn.get(f[1], f[1]))    # Randomize location of illustrations on the page (tl,tr,bl,br)
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
                        # print(m)
                        for f in m:
                            picfname = re.sub(r"\.[Tt][Ii][Ff]",".jpg",f[1])           # Change all TIFs to JPGs
                            pageposn = random.choice(_picposn.get(f[2], f[2]))    # Randomize location of illustrations on the page (tl,tr,bl,br)
                            piclist.append(bk+" "+re.sub(r":",".", f[3])+" |"+picfname+"|"+f[2]+"|"+pageposn+"||"+f[0]+"|"+f[3]+"\n")
                if len(m):
                    plpath = os.path.join(prjdir, "PrintDraft\PicLists")
                    if not os.path.exists(plpath):
                        os.mkdir(plpath)
                    if not os.path.exists(outfname):
                        # print("Outfname: ", outfname)
                        with open(outfname, "w", encoding="utf-8") as outf:
                            outf.write("".join(piclist))
                    else:
                        print("PicList file already exists (this will NOT be overwritten): " + outfname)
                # else:
                    # print(r"No illustrations \fig ...\fig* found in book/file!") # This needs to the log/console: 

    def onGenerateParaAdjList(self, btn_generateParaAdjList):
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
                        print("Adj List already exists (this will NOT be overwritten): " + outfname)

    def GenerateNestedStyles(self, c_omitallverses):
        prjid = self.get("cb_project")
        prjdir = os.path.join(self.settings_dir, self.prjid)
        nstyfname = os.path.join(prjdir, "PrintDraft/NestedStyles.sty")
        nstylist = []
        if self.get("c_omitallverses"):
            nstylist.append("##### Remove all verse numbers\n\\Marker v\n\\TextProperties nonpublishable\n\n")
        if not self.get("c_includeFootnotes"):
            nstylist.append("##### Remove all footnotes\n\\Marker f\n\\TextProperties nonpublishable\n\n")
        if not self.get("c_includeXrefs"):
            nstylist.append("##### Remove all cross-references\n\\Marker x\n\\TextProperties nonpublishable\n\n")
        with open(nstyfname, "w", encoding="utf-8") as outf:
            outf.write("".join(nstylist))

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
                os.startfile(adjfname)
            # else:
                # print("You need to generate the file first!")
        else:
            adjfname = self.fileChooser("Select an Adjust file to edit", 
                    filters = {"Adjust files": {"pattern": "*.adj", "mime": "none"}},
                    multiple = True)
            if adjfname is not None:
                if os.path.exists(adjfname):
                    os.startfile(adjfname)

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
                os.startfile(picfname)
            # else:
                # print("You need to generate the file first!")
        else:
            picfname = self.fileChooser("Select a PicList file to edit", 
                    filters = {"PicList files": {"pattern": "*.piclist", "mime": "none"}},
                    multiple = True)
            if picfname is not None:
                if os.path.exists(picfname):
                    os.startfile(picfname)
    
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

    # def convertTIFtoPNG(self, adjfname):
        # if os.path.splitext(os.path.join(root, adjfname))[1].lower() == ".tif":
            # if os.path.isfile(os.path.splitext(os.path.join(root, adjfname))[0] + ".png"):
                # print("A PNG file already exists for {}".format(adjfname))
            # else:
                # outputfile = os.path.splitext(os.path.join(root, adjfname))[0] + ".png"
                # try:
                    # im = Image.open(os.path.join(root, adjfname))
                    # print("Converting TIF for {}".format(adjfname))
                    # if im.mode == "CMYK":
                        # im = im.convert("Gray")
                    # im.save(outputfile, "PNG")
                # except Exception, e:
                    # print(e)

class Info:
    _mappings = {
        "project/id":               (None, lambda w,v: w.get("cb_project")),
        "project/hideadvancedsettings": ("c_hideAdvancedSettings", lambda w,v: "true" if v else "false"),
        "project/useptmacros":      ("c_usePTmacros", lambda w,v: "true" if v else "false"),
        "project/multiplebooks":    ("c_multiplebooks", lambda w,v: "true" if v else "false"),
        # "project/choosebooks":      ("btn_chooseBooks", lambda w,v: v or ""),
        "project/combinebooks":     ("c_combine", lambda w,v: "true" if v else "false"),
        "project/book":             ("cb_book", None),
        "project/booklist":         ("t_booklist", lambda w,v: v or ""),
        "project/ifinclfrontpdf":   ("c_inclFrontMatter", lambda w,v: "true" if v else "false"),
        "project/frontincludes":    ("btn_selectFrontPDFs", lambda w,v: "\n".join('\\includepdf{{"{}"}}'.format(re.sub(r"\\","/", s)) for s in w.FrontPDFs) if w.FrontPDFs is not None else ""),
        "project/ifinclbackpdf":    ("c_inclBackMatter", lambda w,v: "true" if v else "false"),
        "project/backincludes":     ("btn_selectBackPDFs", lambda w,v: "\n".join('\\includepdf{{"{}"}}'.format(re.sub(r"\\","/", s)) for s in w.BackPDFs) if w.BackPDFs is not None else ""),
        "project/useprintdraftfolder": ("c_useprintdraftfolder", lambda w,v :"true" if v else "false"),
        "project/processscript":    ("c_processScript", lambda w,v :"true" if v else "false"),
        "project/runscriptafter":   ("c_processScriptAfter", lambda w,v :"true" if v else "false"),
        "project/selectscript":     ("btn_selectScript", lambda w,v: re.sub(r"\\","/", w.CustomScript) if w.CustomScript is not None else ""),
        "project/usechangesfile":   ("c_usePrintDraftChanges", lambda w,v :"true" if v else "false"),
        "project/ifusemodstex":     ("c_useModsTex", lambda w,v: "" if v else "%"),
        "project/ifusemodssty":     ("c_useModsSty", lambda w,v: "" if v else "%"),
        "project/ifusenested":      (None, lambda w,v: "" if (w.get("c_omitallverses") or not w.get("c_includeFootnotes") or not w.get("c_includeXrefs")) else "%"),
        # "project/ifprettyOutline":  ("c_prettyIntroOutline", lambda w,v :"true" if v else "false"),
        # "project/ifstarthalfpage":  ("c_startOnHalfPage", lambda w,v :"true" if v else "false"),

        "paper/height":             (None, lambda w,v: re.sub(r"^.*?,\s*(.+?)\s*(?:\(.*|$)", r"\1", w.get("cb_pagesize")) or "210mm"),
        "paper/width":              (None, lambda w,v: re.sub(r"^(.*?)\s*,.*$", r"\1", w.get("cb_pagesize")) or "148mm"),
        "paper/pagesize":           ("cb_pagesize", None),
        "paper/ifwatermark":        ("c_applyWatermark", lambda w,v: "" if v else "%"),
        "paper/watermarkpdf":       ("btn_selectWatermarkPDF", lambda w,v: re.sub(r"\\","/", w.watermarks) if w.watermarks is not None else "A5-Draft.pdf"),
        "paper/ifcropmarks":        ("c_cropmarks", lambda w,v :"true" if v else "false"),  
        "paper/ifverticalrule":     ("c_verticalrule", lambda w,v :"true" if v else "false"),
        "paper/margins":            ("s_margins", lambda w,v: round(v) or "14"),
        "paper/topmarginfactor":    ("s_topmarginfactor", lambda w,v: round(v, 2) or "1.15"),
        "paper/bottommarginfactor": ("s_bottommarginfactor", lambda w,v: round(v, 2) or "1.15"),
        "paper/sidemarginfactor":   ("s_sidemarginfactor", lambda w,v: round(v, 2) or "1.00"),
        "paper/ifaddgutter":        ("c_pagegutter", lambda w,v :"true" if v else "false"),
        "paper/gutter":             ("s_pagegutter", lambda w,v: round(v) or "14"),
        "paper/columns":            ("c_doublecolumn", lambda w,v: "2" if v else "1"),
        "paper/fontfactor":         ("s_fontsize", lambda w,v: round((v / 12), 3) or "1.000"),

        "paragraph/linespacing":    ("s_linespacing", lambda w,v: round((v / 12), 3)),  # This needs to change now as it is (pts) rather than a factor of the Font size.
        "paragraph/ifjustify":       ("c_justify", lambda w,v: "true" if v else "false"),
        "paragraph/ifhyphenate":     ("c_hyphenate", lambda w,v: "true" if v else "false"),

        "document/toc":             ("c_autoToC", lambda w,v: "" if v else "%"),
        "document/toctitle":        ("t_tocTitle", lambda w,v: v or ""),
        "document/usetoc1":         ("c_usetoc1", lambda w,v :"true" if v else "false"),
        "document/usetoc2":         ("c_usetoc2", lambda w,v :"true" if v else "false"),
        "document/usetoc3":         ("c_usetoc3", lambda w,v :"true" if v else "false"),
        "document/chapfrom":        ("cb_chapfrom", lambda w,v: w.builder.get_object("cb_chapfrom").get_active_id()),
        "document/chapto":          ("cb_chapto", lambda w,v: w.builder.get_object("cb_chapto").get_active_id()),
        "document/colgutterfactor": ("s_colgutterfactor", lambda w,v: round(v) or "15"),
        # "document/colbalancing":    ("cb_colbalancing", lambda w,v: w.builder.get_object('cb_colbalancing').get_active_id()),
        "document/ifrtl":           ("c_rtl", lambda w,v :"true" if v else "false"),
        "document/iflinebreakon":   ("c_linebreakon", lambda w,v: "" if v else "%"),
        "document/linebreaklocale": ("t_linebreaklocale", lambda w,v: v or ""),
        "document/script":          ("cb_script", lambda w,v: ";script="+w.builder.get_object('cb_script').get_active_id().lower() if w.builder.get_object('cb_script').get_active_id() != "Zyyy" else ""),
        "document/digitmapping":    ("cb_digits", lambda w,v: ";mapping="+v.lower()+"digits" if v != "Default" else ""),
        "document/ch1pagebreak":    ("c_ch1pagebreak", lambda w,v: "true" if v else "false"),
        # "document/marginalverses":  ("c_marginalverses", lambda w,v: "true" if v else "false"),
        "document/ifomitchapternum":  ("c_omitchapternumber", lambda w,v: "true" if v else "false"),
        "document/ifomitallchapters": ("c_omitchapternumber", lambda w,v: "" if v else "%"),
        "document/ifomitverseone":  ("c_omitverseone", lambda w,v: "true" if v else "false"),
        "document/ifomitallverses": ("c_omitallverses", lambda w,v: "" if v else "%"),
        "document/ifomitallversetext": ("c_omitallverseText", lambda w,v: "true" if v else "false"),
        "document/glueredupwords":  ("c_glueredupwords", lambda w,v :"true" if v else "false"),
        "document/ifinclfigs":      ("c_includeillustrations", lambda w,v :"true" if v else "false"),
        "document/iffigfrmtext":    ("c_includefigsfromtext", lambda w,v :"true" if v else "false"),
        "document/iffigexclwebapp": ("c_figexclwebapp", lambda w,v: "true" if v else "false"),
        "document/iffigskipmissing": ("c_skipmissingimages", lambda w,v: "true" if v else "false"),
        "document/iffigplaceholders": ("c_figplaceholders", lambda w,v :"true" if v else "false"),
        "document/iffighiderefs":   ("c_fighiderefs", lambda w,v :"true" if v else "false"),
        "document/usefigsfolder":   ("c_useFiguresFolder", lambda w,v :"" if v else "%"),
        "document/uselocalfigs":    ("c_useLocalFiguresFolder", lambda w,v :"" if v else "%"),
        "document/customfiglocn":   ("c_useCustomFolder", lambda w,v :"" if v else "%"),
        "document/customfigfolder": ("btn_selectFigureFolder", lambda w,v: re.sub(r"\\","/", w.customFigFolder) if w.customFigFolder is not None else ""),
        "document/ifusepiclist":    ("c_usePicList", lambda w,v :"" if v else "%"),
        "document/spacecntxtlztn":  ("cb_spaceCntxtlztn", lambda w,v: "0" if v == "None" else "1" if v == "Some" else "2"),
        "document/glossarymarkupstyle":  ("cb_glossaryMarkupStyle", lambda w,v: w.builder.get_object("cb_glossaryMarkupStyle").get_active_id()),
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

        "notes/iffootnoterule":     ("c_footnoterule", lambda w,v: "%" if v else ""),
        "notes/ifblendfnxr":        ("c_blendfnxr", lambda w,v :"true" if v else "false"),
        "notes/blendedxrmkr":       ("cb_blendedXrefCaller", lambda w,v: w.builder.get_object("cb_blendedXrefCaller").get_active_id()),

        "notes/includefootnotes":   ("c_includeFootnotes", lambda w,v: "%" if v else ""),
        "notes/iffnautocallers":    ("c_fnautocallers", lambda w,v :"true" if v else "false"),
        "notes/fncallers":          ("t_fncallers", lambda w,v: v if w.get("c_fnautocallers") else ""),
        "notes/fnresetcallers":     ("c_fnpageresetcallers", lambda w,v: "" if v else "%"),
        "notes/fnomitcaller":       ("c_fnomitcaller", lambda w,v: "%" if v else ""),
        "notes/fnparagraphednotes": ("c_fnparagraphednotes", lambda w,v: "" if v else "%"),

        "notes/includexrefs":       ("c_includeXrefs", lambda w,v: "%" if v else ""),
        "notes/ifxrautocallers":    ("c_xrautocallers", lambda w,v :"true" if v else "false"),
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
    _glossarymarkup = {
        "None":                    r"\1",
        "format as bold":          r"\\bd \1\\bd*",
        "format as italics":       r"\\it \1\\it*",
        "format as bold italics":  r"\\bdit \1\\bdit*",
        "format with emphasis":    r"\\em \1\\em*",
        "bottom ⸤half⸥ brackets":  r"\\u2E24\1\\u2E25", # Question for MH - using this option makes it crash with an encoding issue. Help!
        "star *before word":       r"*\1",
        "star after* word":        r"\1*",
        "circumflex ^before word": r"^\1",
        "circumflex after^ word":  r"\1^"
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
        # traceback.print_stack(limit=3)
        for p, wid in self._fonts.items():
            f = TTFont(printer.get(wid))
            if 'Silf' in f:
                engine = "/GR"
            else:
                engine = ""
            s = ""
            if len(f.style):
                s = "/" + "".join(x[0].upper() for x in f.style)
            self.dict[p] = f.family + engine + s

    def processHdrFtr(self, printer):
        mirror = printer.get('c_mirrorpages')
        for side in ('left', 'center', 'right'):
            v = printer.get("cb_hdr" + side)
            t = self._hdrmappings.get(v, v)
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

    def texfix(self, path):
        return path.replace(" ", r"\ ")

    def asTex(self, template="template.tex", filedir="."):
 #       import pdb;pdb.set_trace()
        for k, v in self._settingmappings.items():
            if self.dict[k] == "":
                self.dict[k] = self.ptsettings.dict.get(v, "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z")
        res = []
        with open(os.path.join(os.path.dirname(__file__), template)) as inf:
            for l in inf.readlines():
                if l.startswith(r"\ptxfile"):
                    res.append("\\PtxFilePath={"+filedir+"/}\n")
                    le = len(self.dict['project/books'])
                    # if le > 1:
                        # res.append("\\lastptxfilefalse")
                    for i, f in enumerate(self.dict['project/books']):
                        # if i+1 == le and i > 0:
                            # res.append("\\lastptxfilefalse")
                        res.append("\\ptxfile{{{}}}\n".format(f))

                else:
                    res.append(l.format(**self.dict))
        return "".join(res)

    def convertBook(self, bk, outdir, prjdir):
        if self.ptsettings is None:
            self.ptsettings = ParatextSettings(prjdir)
        if self.changes is None and self.dict['project/usechangesfile'] == "true":
            self.changes = self.readChanges(os.path.join(prjdir, 'PrintDraftChanges.txt'))
        else:
            self.changes = []
        customsty = os.path.join(prjdir, 'custom.sty')
        if not os.path.exists(customsty):
            open(customsty, "w").close()
        fbkfm = self.ptsettings['FileNameBookNameForm']
        bknamefmt = fbkfm.replace("MAT","{bkid}").replace("41","{bknum:02d}") + \
                    self.ptsettings['FileNamePostPart']
        fname = bknamefmt.format(bkid=bk, bknum=books.get(bk, 0))
        infname = os.path.join(prjdir, fname)
        if self.changes is not None or self.localChanges is not None:
            outfname = fname
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:]
            outfpath = os.path.join(outdir, outfname)
            with open(infname, "r", encoding="utf-8") as inf:
                dat = inf.read()
                for c in self.changes + self.localChanges:
                    if c[0] is None:
                        dat = c[1].sub(c[2], dat)
                    else:
                        newdat = [c[0].split(dat)]
                        for i in range(1, len(newdat), 2):
                            # print("i: ", i)
                            newdat[i] = c[  1].sub(c[2], newdat[i])
                        dat = "".join(newdat)
            with open(outfpath, "w", encoding="utf-8") as outf:
                outf.write(dat)
            return outfname
        else:
            return fname

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
                    continue  # This change in my PrintDraftChanges.txt is causing it to fail
                    # in "\\w .+?\\w\*": "\|.+?\\w\*" > "\w*"
                m = re.match(r"^in\s+(['\"])(.*?)(?<!\\)\1\s*:\s*(['\"])(.*?)(?<!\\)\3\s*>\s*(['\"])(.*?)(?<!\\)\5", l)
                if m:
                    changes.append((regex.compile("("+m.group(2)+")", flags=regex.M), regex.compile(m.group(4), flags=regex.M), m.group(6)))
                    # print("Appended in Group 2: ", m)
        if not len(changes):
            return None
        return changes
            
    def makelocalChanges(self, printer):
        self.localChanges = []
        first = int(printer.get("cb_chapfrom"))
        last = int(printer.get("cb_chapto"))
        
        # This section handles PARTIAL books (from chapter X to chapter Y)
        if not printer.get("c_multiplebooks"):
            bk = printer.get("cb_book")
            if first > 1:
                self.localChanges.append((None, regex.compile(r"\\c 1 ?\r?\n.+(?=\\c {} ?\r?\n)".format(first), flags=regex.S), ""))
            if last < int(chaps.get(bk)):
                self.localChanges.append((None, regex.compile(r"\\c {} ?\r?\n.+".format(last+1), flags=regex.S), ""))
            
        # Glossary Word markup: Remove the second half of the \w word|glossary-form\w* and apply chosen glossary markup
        v = printer.get("cb_glossaryMarkupStyle")
        gloStyle = self._glossarymarkup.get(v, v)
        self.localChanges.append((None, regex.compile(r"\\w (.+?)(\|.+?)?\\w\*", flags=regex.M), gloStyle))

        if printer.get("c_includeillustrations") and printer.get("c_includefigsfromtext"):
            self.localChanges.append((None, regex.compile(r"\.[Tt][Ii][Ff]", flags=regex.M), ".jpg"))           # Change all TIFs extensions to JPGs
            if printer.get("c_fighiderefs"):
                self.localChanges.append((None, regex.compile(r"(\\fig .*?)(\d+\:\d+([-,]\d+)?)(.*?\\fig\*)", flags=regex.M), r"\1\4")) # remove ch:vs ref from caption
        else:
            self.localChanges.append((None, regex.compile(r"\\fig .*?\\fig\*", flags=regex.M), ""))             # Drop ALL Figures
        
        if printer.get("c_omitBookIntro"):
            self.localChanges.append((None, regex.compile(r"\\i(s|m|mi|p|pi|li\d?|pq|mq|pr|b|q\d?) .+?\r?\n", flags=regex.M), "")) # Drop Introductory matter

        if printer.get("c_omitIntroOutline"):
            self.localChanges.append((None, regex.compile(r"\\(iot|io\d) [^\\]+", flags=regex.M), ""))          # Drop ALL Intro Outline matter
            self.localChanges.append((None, regex.compile(r"\\ior .+?\\ior\*\s?\r?\n", flags=regex.M), ""))     # and remove Intro Outline References

        if printer.get("c_omitSectHeads"):
            self.localChanges.append((None, regex.compile(r"\\s .+", flags=regex.M), ""))                       # Drop ALL Section Headings

        if printer.get("c_omitParallelRefs"):
            self.localChanges.append((None, regex.compile(r"\\r .+", flags=regex.M), ""))                       # Drop ALL Parallel Passage References

        if printer.get("c_blendfnxr"): 
            XrefCaller = printer.get("cb_blendedXrefCaller")
            # To merge/blend \f and \x together, simply change all (\x to \f) (\xo to \fr) (\xq to \fq) (\xt to \ft) and (\f* to \x*)
            self.localChanges.append((None, regex.compile(r"\\x . ", flags=regex.M), r"\\f {} ".format(XrefCaller)))
            self.localChanges.append((None, regex.compile(r"\\x\* ", flags=regex.M), r"\\f* "))
            self.localChanges.append((None, regex.compile(r"\\xq ", flags=regex.M), r"\\fq "))
            self.localChanges.append((None, regex.compile(r"\\xt ", flags=regex.M), r"\\ft "))

        if printer.get("c_preventorphans"): 
            # Keep final two words of \q lines together [but this doesn't work if there is an \f or \x at the end of the line] 
            self.localChanges.append((None, regex.compile(r"(\\q\d?(\s?\r?\n?\\v)?( \S+)+( (?!\\)\S+)) (\S+\s*\n)", flags=regex.M), r"\1\u00A0\5"))   

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
                    if v[0].startswith("cb_") or v[0].startswith("t_") or v[0].startswith("f_") or v[0].startswith("btn_"):
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

