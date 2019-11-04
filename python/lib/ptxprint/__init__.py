#!/usr/bin/python3

import sys, os, re, regex, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import xml.etree.ElementTree as et
from ptxprint.font import TTFont
import configparser

# For future Reference on how Paratext treats this list:
# G                                    MzM                         RT                P        X      FBO    ICGTND          L  OT z NT DC  -  X Y  -  Z  --  L
# E                                    AzA                         EO                S        X      RAT    NNLDDA          A  
# N                                    LzT                         VB                2        ABCDEFGTKH    TCOXXG          O  39+1+27+18+(8)+7+3+(4)+6+(10)+1 = 124
# 111111111111111111111111111111111111111111111111111111111111111111111111111111111111000000001111111111000011111100000000001  CompleteCanon (all books possible)

_bookslist = """GEN|50 EXO|40 LEV|27 NUM|36 DEU|34 JOS|24 JDG|21 RUT|4 1SA|31 2SA|24 1KI|22 2KI|25 1CH|29 2CH|36 EZR|10 NEH|13
        EST|10 JOB|42 PSA|150 PRO|31 ECC|12 SNG|8 ISA|66 JER|52 LAM|5 EZK|48 DAN|12 HOS|14 JOL|3 AMO|9 OBA|1 JON|4 MIC|7 NAM|3
        HAB|3 ZEP|3 HAG|2 ZEC|14 MAL|4 ZZZ|0
        MAT|28 MRK|16 LUK|24 JHN|21 ACT|28 ROM|16 1CO|16 2CO|13 GAL|6 EPH|6 PHP|4 COL|4 1TH|5 2TH|3 1TI|6 2TI|4 TIT|3 PHM|1
        HEB|13 JAS|5 1PE|5 2PE|3 1JN|5 2JN|1 3JN|1 JUD|1 REV|22
        TOB|14 JDT|16 ESG|10 WIS|19 SIR|51 BAR|6 LJE|1 S3Y|1 SUS|1 BEL|1 1MA|16 2MA|15 3MA|7 4MA|18 1ES|9 2ES|16 MAN|1 PS2|1
        ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0
        XXA|0 XXB|0 XXC|0 XXD|0 XXE|0 XXF|0 XXG|0 FRT|0 BAK|0 OTH|0 
        ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0
        INT|0 CNC|0 GLO|0 TDX|0 NDX|0 DAG|14 
        ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0
        LAO|1"""
allbooks = [b.split("|")[0] for b in _bookslist.split() if b != "ZZZ|0"]
books = dict((b.split("|")[0], i+1) for i, b in enumerate(_bookslist.split()))
chaps = dict(b.split("|") for b in _bookslist.split())

class ParatextSettings:
    def __init__(self, basedir, prjid):
        self.dict = {}
        doc = et.parse(os.path.join(basedir, prjid, "Settings.xml"))
        for c in doc.getroot():
            self.dict[c.tag] = c.text

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
        self.mw = self.builder.get_object("ptxprint")
        self.projects = self.builder.get_object("ls_projects")
        self.settings_dir = settings_dir
        self.ptsettings = None
        self.booklist = []
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

    def onFontChange(self, fbtn):
        font = fbtn.get_font_name()
        (family, style, size) = self.parse_fontname(font)
        style = [s.lower() for s in style if s not in ("Regular", "Medium")]
        label = self.builder.get_object("l_font")
        # label.set_text(font) # No longer used after re-doing the UI
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
        lb = self.builder.get_object("l_embolden")
        ls = self.builder.get_object("l_slant")
        if self.get("c_fakebold") or self.get("c_fakeitalic") or self.get("c_fakebolditalic"):
            lb.set_sensitive(True)
            ls.set_sensitive(True)
        else:
            lb.set_sensitive(False)
            ls.set_sensitive(False)

    def onFakeboldClicked(self, c_fakebold):
        bdb = self.builder.get_object("s_boldembolden")
        bds = self.builder.get_object("s_boldslant")
        if self.get("c_fakebold"):
            bdb.set_sensitive(True)
            bds.set_sensitive(True)
        else:
            bdb.set_sensitive(False)
            bds.set_sensitive(False)
        self.updateFakeLabels()
        
    def onFakeitalicClicked(self, c_fakeitalic):
        itb = self.builder.get_object("s_italicembolden")
        its = self.builder.get_object("s_italicslant")
        if self.get("c_fakeitalic"):
            itb.set_sensitive(True)
            its.set_sensitive(True)
        else:
            itb.set_sensitive(False)
            its.set_sensitive(False)
        self.updateFakeLabels()

    def onFakebolditalicClicked(self, c_fakebolditalic):
        bib = self.builder.get_object("s_bolditalicembolden")
        bis = self.builder.get_object("s_bolditalicslant")
        if self.get("c_fakebolditalic"):
            bib.set_sensitive(True)
            bis.set_sensitive(True)
        else:
            bib.set_sensitive(False)
            bis.set_sensitive(False)
        self.updateFakeLabels()

    def onClickedIncludeFootnotes(self, c_includeFootnotes):
        fna = self.builder.get_object("c_fnautocallers")
        fnc = self.builder.get_object("t_fncallers")
        fno = self.builder.get_object("c_fnomitcaller")
        fnr = self.builder.get_object("c_fnpageresetcallers")
        fnp = self.builder.get_object("c_fnparagraphednotes") 
        if self.get("c_includeFootnotes"):
            fna.set_sensitive(True)
            fnc.set_sensitive(True)
            fno.set_sensitive(True)
            fnr.set_sensitive(True)
            fnp.set_sensitive(True)
        else:
            fna.set_sensitive(False)
            fnc.set_sensitive(False)
            fno.set_sensitive(False)
            fnr.set_sensitive(False)
            fnp.set_sensitive(False)
        
    def onClickedIncludeXrefs(self, c_includeXrefs):
        xra = self.builder.get_object("c_xrautocallers")
        xrc = self.builder.get_object("t_xrcallers")
        xro = self.builder.get_object("c_xromitcaller")
        xrr = self.builder.get_object("c_xrpageresetcallers")
        xrp = self.builder.get_object("c_paragraphedxrefs") 
        if self.get("c_includeXrefs"):
            xra.set_sensitive(True)
            xrc.set_sensitive(True)
            xro.set_sensitive(True)
            xrr.set_sensitive(True)
            xrp.set_sensitive(True)
        else:
            xra.set_sensitive(False)
            xrc.set_sensitive(False)
            xro.set_sensitive(False)
            xrr.set_sensitive(False)
            xrp.set_sensitive(False)

    def onColumnsChanged(self, cb_Columns):
        vrul = self.builder.get_object("c_verticalrule")
        gtrl = self.builder.get_object("l_gutterWidth")
        gtrw = self.builder.get_object("s_colgutterfactor")
        if self.get("cb_columns") == "Double":
            vrul.set_sensitive(True)
            gtrl.set_sensitive(True)
            gtrw.set_sensitive(True)
        else:
            vrul.set_sensitive(False)
            gtrl.set_sensitive(False)
            gtrw.set_sensitive(False)

    def onBookSelectorChange(self, c_onebook):
        cmb = self.builder.get_object("c_combine")
        lcf = self.builder.get_object("l_chapfrom")
        ccf = self.builder.get_object("cb_chapfrom")
        lct = self.builder.get_object("l_chapto")
        cct = self.builder.get_object("cb_chapto")
        if self.get("c_onebook"):
            cmb.set_sensitive(False)
            lcf.set_sensitive(True)
            ccf.set_sensitive(True)
            lct.set_sensitive(True)
            cct.set_sensitive(True)
        else:
            cmb.set_sensitive(True)
            lcf.set_sensitive(False)
            ccf.set_sensitive(False)
            lct.set_sensitive(False)
            cct.set_sensitive(False)
            
    def onFigsChanged(self, c_figs):
        xcl = self.builder.get_object("c_figexclwebapp")
        plc = self.builder.get_object("c_figplaceholders")
        hdr = self.builder.get_object("c_fighiderefs")
        if self.get("c_includefigs"):
            xcl.set_sensitive(True)
            plc.set_sensitive(True)
            hdr.set_sensitive(True)
        else:
            xcl.set_sensitive(False)
            plc.set_sensitive(False)
            hdr.set_sensitive(False)

    def onPreprocessChanged(self, c_preprocess):
        pre = self.builder.get_object("fc_preprocess")
        if self.get("c_preprocess"):
            pre.set_sensitive(True)
        else:
            pre.set_sensitive(False)

    def onInclFrontMatterChanged(self, c_inclFrontMatter):
        fcfm = self.builder.get_object("fc_frontMatter")
        if self.get("c_inclFrontMatter"):
            fcfm.set_sensitive(True)
        else:
            fcfm.set_sensitive(False)

    def onApplyWatermarkChanged(self, c_applyWatermark):
        fcwm = self.builder.get_object("fc_watermark")
        if self.get("c_applyWatermark"):
            fcwm.set_sensitive(True)
        else:
            fcwm.set_sensitive(False)
    
    def onInclBackMatterChanged(self, c_inclBackMatter):
        fcbm = self.builder.get_object("fc_backMatter")
        if self.get("c_inclBackMatter"):
            fcbm.set_sensitive(True)
        else:
            fcbm.set_sensitive(False)
            
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

    def onClickChooseBooks(self, btn):
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
            # print(self.booklist)
        dia.hide()

    def onClickmbs_all(self, btn):
        for b in self.alltoggles:
            b.set_active(True)

    def onClickmbs_OT(self, btn):
        for b in self.alltoggles[:39]:   # This isn't right yet (as it depends on which books are in the Project!
            b.set_active(True)

    def onClickmbs_NT(self, btn):
        for b in self.alltoggles[39:66]:    # This isn't right yet (as it depends on which books are in the Project!
            b.set_active(True)

    def onClickmbs_DC(self, btn):
        for b in self.alltoggles[66:74]:    # This isn't right yet (as it depends on which books are in the Project!
            b.set_active(True)

    def onClickmbs_xtra(self, btn):
        for b in self.alltoggles[76:]:    # This isn't right yet (as it depends on which books are in the Project!
            b.set_active(True)

    def onClickmbs_none(self, btn):
        for b in self.alltoggles:
            b.set_active(False)
                
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

    def onEditPythonFile(self, widget):
        pyScript = "??????????????"
        # print(pyScript)
        if os.path.exists(pyScript):
            os.startfile(pyScript)


class Info:
    _mappings = {
        "project/id":               (None, lambda w,v: w.get("cb_project")),
        "project/book":             ("cb_book", None),
        "paper/height":             (None, lambda w,v: re.sub(r"^.*?, \s*(.+?)\s*(?:\(.*|$)", r"\1", w.get("cb_pagesize")) or "210mm"),
        "paper/width":              (None, lambda w,v: re.sub(r"^(.*?)\s*,.*$", r"\1", w.get("cb_pagesize")) or "148mm"),
        "paper/pagesize":           ("cb_pagesize", None),
        "paper/watermark":          ("c_applyWatermark", lambda w,v: "" if v else "%"),
        "paper/watermarkpdf":       ("fc_watermark", lambda w,v: "Draft.pdf" or ""),
        "paper/ifcropmarks":        ("c_cropmarks", lambda w,v :"true" if v else "false"),
        "paper/ifverticalrule":     ("c_verticalrule", lambda w,v :"true" if v else "false"),
        "paper/margins":            ("s_margins", lambda w,v: round(v) or "14"),
        "paper/topmarginfactor":    ("s_topmarginfactor", lambda w,v: round(v, 2) or "1.15"),
        "paper/bottommarginfactor": ("s_bottommarginfactor", lambda w,v: round(v, 2) or "1.15"),
        #\def\SideMarginFactor{{1.0}} % not needed/wanted at this point
        #"paper/gutter":            ("s_pagegutter", lambda w,v: round(v) or "14"),

        "paper/columns":            ("cb_columns", lambda w,v: "1" if v == "Single" else "2"),
#        "paper/fontfactor":         (None, lambda w,v: float(w.get("f_body")[2]) / 12),  # This is now its own spin button for FONT SIZE
        "paper/fontfactor":         ("s_fontsize", lambda w,v: round((v / 12), 3) or "1.000"),

        "paragraph/linespacing":    ("s_linespacing", lambda w,v: round(v, 1)),

        "document/colgutterfactor": ("s_colgutterfactor", lambda w,v: round(v) or "15"),
        "document/ifrtl":           ("c_rtl", lambda w,v :"true" if v else "false"),
        "document/iflinebreakon":   ("c_linebreakon", lambda w,v: "" if v else "%"),
        # "document/script":          ("cb_script", lambda w,v: ";script="+v.lower() if len(v) else ""),
        # "document/script":          "mymr",
        "document/digitmapping":    ("cb_digits", lambda w,v: ";mapping="+v.lower()+"digits" if len(v) else ""),

        "document/linebreaklocale": ("t_linebreaklocale", lambda w,v: v or ""),
        "document/ifomitchapternum": ("c_omitchapternumber", lambda w,v: "true" if v else "false"),
        "document/ifomitallchapters": ("c_omitchapternumber", lambda w,v: "" if v else "%"),
        "document/ifomitverseone":  ("c_omitverseone", lambda w,v: "true" if v else "false"),
        "document/ifomitallverses": ("c_omitallverses", lambda w,v: "" if v else "%"),  # This also needs \Marker v \FontSize 0.0001 to be set in .sty file
        "document/iffigures":       ("c_includefigs", lambda w,v :"true" if v else "false"),
        "document/iffigexclwebapp": ("c_figexclwebapp", lambda w,v: "true" if v else "false"),
        "document/iffigplaceholders": ("c_figplaceholders", lambda w,v :"true" if v else "false"),
        "document/iffighiderefs":   ("c_fighiderefs", lambda w,v :"true" if v else "false"),
        "document/ifjustify":       ("c_justify", lambda w,v: "true" if v else "false"),
        "document/crossspacecntxt": ("cb_crossSpaceContextualization", lambda w,v: "0" if v == "None" else "1" if v == "Some" else "2"),
        "document/hangpoetry":      ("c_hangpoetry", lambda w,v: "" if v else "%"),
        "document/supresssectheads": ("c_omitSectHeads", lambda w,v: "true" if v else "false"),
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
        
        "footer/ftrcenter":         ("t_runningFooter", lambda w,v: v if w.get("c_runningFooter") else ""),

        "notes/ifomitfootnoterule": (None, lambda w,v: "%" if w.get("c_footnoterule") else ""),
        "notes/blendfnxr":          ("c_blendfnxr", lambda w,v :"true" if v else "false"),

        "notes/fncallers":          ("t_fncallers", lambda w,v: v if w.get("c_fnautocallers") else ""),
        "notes/fnresetcallers":     ("c_fnpageresetcallers", lambda w,v: "" if v else "%"),
        "notes/fnomitcaller":       ("c_fnomitcaller", lambda w,v: "%" if v else ""),
        "notes/fnparagraphednotes": ("c_fnparagraphednotes", lambda w,v: "" if v else "%"),

        "notes/xrcallers":          ("t_xrcallers", lambda w,v: v if w.get("c_xrautocallers") else ""),
        "notes/xrresetcallers":     ("c_xrpageresetcallers", lambda w,v: "" if v else "%"),
        "notes/xromitcaller":       ("c_xromitcaller", lambda w,v: "%" if v else ""),
        "notes/xrparagraphednotes": ("c_paragraphedxrefs", lambda w,v: "" if v else "%"),

        "fontbold/fakeit":          ("c_fakebold", lambda w,v :"true" if v else "false"),
        "fontitalic/fakeit":        ("c_fakeitalic", lambda w,v :"true" if v else "false"),
        "fontbolditalic/fakeit":    ("c_fakebolditalic", lambda w,v :"true" if v else "false"),
        # Comment from MP to MH: I have built in some limits into the glade interface, but *do* allow for -ve values, so any non-zero value is OK
        # For example, we have a very heavy, but beautiful "bold" font, but need it to be lighter so a -2.0 embolden makes it about right
        # Having tried this out, I'm now wondering whether this is true or not. I can't get -ve Embolden values to work at all now. (but -ve Italics works!)
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
    _hdrmappings = {                         # TO-DO! These aren't being saved/remembered yet in the UI!
        "First Reference":  r"\firstref",
        "Last Reference":   r"\lastref",
        "Page Number":      r"\pagenumber",
        "Reference Range":  r"\rangeref",
        "-empty-":          r"\empty"
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
        self.processCallers(printer)
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

    def processCallers(self, printer):
        default = "a b c d e f g h i j k l m n o p q r s t u v w x y z"
        self.dict['notes/fncallers'] = \
                ",".join(self.ptsettings.get('CallerSequence', default).split())

    def asTex(self, template="template.tex"):
 #       import pdb;pdb.set_trace()
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
        if self.changes is None:  # AND if "c_usePrintDraftChanges" is active
            self.changes = self.readChanges(os.path.join(prjdir, 'PrintDraftChanges.txt'))
        customsty = os.path.join(prjdir, 'custom.sty')
        if not os.path.exists(customsty):
            open(customsty, "w").close()
        fbkfm = self.ptsettings['FileNameBookNameForm']
        bknamefmt = fbkfm.replace("MAT","{bkid}").replace("41","{bknum:02d}") + \
                    self.ptsettings['FileNamePostPart']
        fname = bknamefmt.format(bkid=bk, bknum=books.get(bk, 0))
        infname = os.path.join(prjdir, fname)
        if self.changes is not None: # OR if self.localChanges is not None
            outfname = os.path.join(outdir, fname)
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:]
            with open(infname, "r", encoding="utf-8") as inf:
                dat = inf.read()
                for c in self.changes + self.localChanges:  # Is there a better/neater way of doing this?
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
                    # print(m.group(2) + " > " + m.group(4))
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
        if not printer.get("c_includefigs"):
            self.localChanges.append((None, regex.compile(r"\\fig .*?\\fig\*", flags=regex.M), ""))             # Drop ALL Figures
        else:
            self.localChanges.append((None, regex.compile(r"\.[Tt][Ii][Ff]", flags=regex.M), ".jpg"))           # Change all TIFs to JPGs
            if printer.get("c_fighiderefs"):
                self.localChanges.append((None, regex.compile(r"(\\fig .*?)(\d+\:\d+(\-\d+)?)(.*?\\fig\*)", flags=regex.M), r"\1\4")) # remove ch:vs ref from caption
        
        if printer.get("c_omitBookIntro"):
            self.localChanges.append((None, regex.compile(r"\\i(s|m|mi|p|pi|li\d?|pq|mq|pr|b|q\d?) [^\\]+", flags=regex.M), "")) # Drop Introductory matter

        if printer.get("c_omitIntroOutline"):
            self.localChanges.append((None, regex.compile(r"\\(iot|io\d) [^\\]+", flags=regex.M), ""))          # Drop ALL Intro Outline matter
            self.localChanges.append((None, regex.compile(r"\\ior .+?\\ior\*", flags=regex.M), ""))             # and remove Intro Outline References

        if printer.get("c_omitSectHeads"):
            self.localChanges.append((None, regex.compile(r"\\s .+", flags=regex.M), ""))                       # Drop ALL Section Headings

        if not printer.get("c_includeFootnotes"):
            self.localChanges.append((None, regex.compile(r"\\f .+?\\f\*", flags=regex.M), ""))                 # Drop ALL Footnotes

        if not printer.get("c_includeXrefs"):
            self.localChanges.append((None, regex.compile(r"\\x .+?\\x\*", flags=regex.M), ""))                 # Drop ALL Cross-references

        if printer.get("c_blendfnxr"): # this is a bit of a hack, but it works! (any better ideas?) - we could at least make it a single RegEx instead of 4!
            # To merge/blend \f and \x together, simply change all (\x to \f) (\xo to \fr) (\xq to \fq) (\xt to \ft) and (\f* to \x*)
            self.localChanges.append((None, regex.compile(r"\\x . ", flags=regex.M), r"\\f # "))
            self.localChanges.append((None, regex.compile(r"\\x\* ", flags=regex.M), r"\\f* "))
            self.localChanges.append((None, regex.compile(r"\\xq ", flags=regex.M), r"\\fq "))
            self.localChanges.append((None, regex.compile(r"\\xt ", flags=regex.M), r"\\ft "))
        
        if printer.get("c_preventorphans"): 
            # Keep final two words of \q lines together [but this doesn't work if there is an \f or \x at the end of the line] 
            self.localChanges.append((None, regex.compile(r"(\\q\d?(\s?\r?\n?\\v)?( \S+)+) (\S+\s*\n)", flags=regex.M), r"\1\u00A0\4"))   
            # Push the verse number onto the next line if there is a short widow word at the end of the line
            self.localChanges.append((None, regex.compile(r"(\d [\S][\S]?) ", flags=regex.M), r"\1\u00A0")) 

        # if True:
            # self.localChanges.append((None, regex.compile(r"(?<=[ ])(\S\S\S+)[- ]*\1(?=[\s,.!?])", flags=regex.M), r"\1\u00A0\1")) # keep reduplicated words together

        return self.localChanges

    def createConfig(self, printer):
        config = configparser.ConfigParser()
        for k, v in self._mappings.items():
            if v[0] is None:
                continue
            (sect, key) = k.split("/")
            if not config.has_section(sect):
                config.add_section(sect)
            val = printer.get(v[0], asstr=True)
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
                    if v[0] is None:
                        continue
                    if v[0].startswith("cb_") or v[0].startswith("t_") or v[0].startswith("f_"):
                        printer.set(v[0], config.get(sect, opt))
                    if v[0].startswith("s_"):
                        printer.set(v[0], float(config.get(sect, opt)))
                        #printer.set(v[0], round(config.get(sect, opt)),2)
                    elif v[0].startswith("c_"):
                        printer.set(v[0], config.getboolean(sect, opt))
                elif key in self._fonts:
                    v = self._fonts[key]
                    printer.set(v, config.get(sect, opt))
