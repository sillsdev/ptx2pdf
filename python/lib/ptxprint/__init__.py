#!/usr/bin/python3

import sys, os, re, regex, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import xml.etree.ElementTree as et
from ptxprint.font import TTFont
import configparser

_bookslist = """GEN|50 EXO|40 LEV|27 NUM|36 DEU|34 JOS|24 JDG|21 RUT|4 1SA|31 2SA|24 1KI|22 2KI|25 1CH|29 2CH|36 EZR|10 NEH|13
        EST|10 JOB|42 PSA|150 PRO|31 ECC|12 SNG|8 ISA|66 JER|52 LAM|5 EZK|48 DAN|12 HOS|14 JOL|3 AMO|9 OBA|1 JON|4 MIC|7 NAM|3
        HAB|3 ZEP|3 HAG|2 ZEC|14 MAL|4 ZZZ|0
        MAT|28 MRK|16 LUK|24 JHN|21 ACT|28 ROM|16 1CO|16 2CO|13 GAL|6 EPH|6 PHP|4 COL|4 1TH|5 2TH|3 1TI|6 2TI|4 TIT|3 PHM|1
        HEB|13 JAS|5 1PE|5 2PE|3 1JN|5 2JN|1 3JN|1 JUD|1 REV|22
        TOB|0 JDT|0 ESG|0 WIS|0 DIR|0 BAR|0 LJE|0 S3Y|0 SUS|0 BEL|0 1MA|0 2MA|0 3MA|0 4MA|0 1ES|0 2ES|0 MAN|0 PS2|0
        ODA|0 PSS|0"""
allbooks = [b.split("|")[0] for b in _bookslist.split() if b != "ZZZ|0"]
books = dict((b.split("|")[0], i+1) for i, b in enumerate(_bookslist.split()))
chaps = dict(b.split("|") for b in _bookslist.split())

#print("allbooks(list)---------------------------------------------------")
#print(allbooks)
#print("books(dict)---------------------------------------------------")
#print(books)
#print("chaps(dict)---------------------------------------------------")
#print(chaps)
#print("---------------------------------------------------")

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
            print(s, fname, f.extrastyles)
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
        if self.get("cb_columns") == "2":
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
        if self.get("c_figs"):
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

    def onXyzChanged(self, c_button):
        print(c_button)
        if c_button.get_active():
            rhr.set_sensitive(True)
            rhr.grab_focus()
        else:
            rhr.set_sensitive(False)

#    def onXyzChanged(self, c_Xyz):
#        abc = self.builder.get_object("t_TxYz")
#        if self.get("c_Xyz"):
#            abc.set_sensitive(True)
#            abc.grab_focus() 
#        else:   
#            abc.set_sensitive(False)
    def onClickChooseBooks(self, btn):
        #Do something to bring up the Book Selector dialog
        print("This should bring up the 'dlg_multiBookSelector' dialog to select one or more books")
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
            print(self.booklist)
        dia.hide()

    def onClickmbs_all(self, btn):
        print(self)
        for b in self.alltoggles:
            b.set_active(True)
        
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
        

class Info:
    _mappings = {
        "project/id":               (None, lambda w,v: w.get("cb_project")),
        "project/book":             ("cb_book", None),
        "paper/height":             (None, lambda w,v: re.sub(r"^.*?, \s*(.+?)\s*(?:\(.*|$)", r"\1", w.get("cb_pagesize")) or "210mm"),
        "paper/width":              (None, lambda w,v: re.sub(r"^(.*?)\s*,.*$", r"\1", w.get("cb_pagesize")) or "148mm"),
        "paper/pagesize":           ("cb_pagesize", None),
        "paper/ifcropmarks":        ("c_cropmarks", lambda w,v :"true" if v else "false"),
        "paper/ifverticalrule":     ("c_verticalrule", lambda w,v :"true" if v else "false"),
        "paper/margins":            ("s_margins", lambda w,v: round(v) or "14"),
        "paper/topmarginfactor":    ("s_topmarginfactor", lambda w,v: round(v, 2) or "1.15"),
        "paper/bottommarginfactor": ("s_bottommarginfactor", lambda w,v: round(v, 2) or "1.15"),
        #\def\SideMarginFactor{{1.0}} % not needed/wanted at this point
        #"paper/gutter":            ("s_pagegutter", lambda w,v: round(v) or "14"),

        "paper/columns":            ("cb_columns", lambda w,v: v),
#        "paper/fontfactor":         (None, lambda w,v: float(w.get("f_body")[2]) / 12),  # This is now its own spin button for FONT SIZE
        "paper/fontfactor":         ("s_fontsize", lambda w,v: round((v / 12), 3) or "1.000"),

        "paragraph/linespacing":    ("s_linespacing", lambda w,v: round(v, 1)),

        "document/colgutterfactor": ("s_colgutterfactor", lambda w,v: round(v) or "15"),
        "document/ifrtl":           ("c_rtl", lambda w,v :"true" if v else "false"),
        "document/iflinebreakon":   ("c_linebreakon", lambda w,v: "" if v else "%"),
        "document/linebreaklocale": ("t_linebreaklocale", lambda w,v: v or ""),
        "document/ifomitchapternum": ("c_omitchapternumber", lambda w,v: "true" if v else "false"),
        "document/ifomitverseone":  ("c_omitverseone", lambda w,v: "true" if v else "false"),
        "document/iffigures":       ("c_figs", lambda w,v :"true" if v else "false"),
        "document/iffigexclwebapp": ("c_figexclwebapp", lambda w,v: "true" if v else "false"),
        "document/iffigplaceholders": ("c_figplaceholders", lambda w,v :"true" if v else "false"),
        "document/iffighiderefs":   ("c_fighiderefs", lambda w,v :"true" if v else "false"),
        "document/ifjustify":       ("c_justify", lambda w,v: "true" if v else "false"),
        "document/hangpoetry":      ("c_hangpoetry", lambda w,v: "" if v else "%"),

        "header/headerposition":    ("s_headerposition", lambda w,v: round(v, 2) or "0.50"),
        "header/footerposition":    ("s_footerposition", lambda w,v: round(v, 2) or "0.50"),
        "header/ifomitrhchapnum":   ("c_omitrhchapnum", lambda w,v :"true" if v else "false"),
        "header/ifverses":          ("c_hdrverses", lambda w,v :"true" if v else "false"),
        "header/ifrhrule":          ("c_rhrule", lambda w,v: "" if v else "%"),
        "header/ruleposition":      ("s_rhruleposition", lambda w,v: v or "10"),

        "footer/draft":             ("t_draft", lambda w,v: v),
        "footer/comment":           (None, lambda w,v: v),

        "notes/ifomitfootnoterule": (None, lambda w,v: "%" if w.get("c_footnoterule") else ""), # opposite as one says show other omit

        # if c_fnautocallers is false then fncallers needs to be set to empty {} - HOW TO DO THAT?
        "notes/fncallers":          ("t_fncallers", lambda w,v: v or "*"),
        "notes/fnresetcallers":     ("c_fnpageresetcallers", lambda w,v: "" if v else "%"),
        "notes/fnomitcaller":       ("c_fnomitcaller", lambda w,v: "" if v else "%"),
        "notes/fnparagraphednotes": (None, lambda w,v: "" if w.get("c_fnomitcaller") else "%"),

        # if c_xrautocallers is false then xrcallers needs to be set to empty {} - HOW TO DO THAT?
        "notes/xrcallers":          ("t_xrcallers", lambda w,v: v or "+"),
        "notes/xrresetcallers":     ("c_xrpageresetcallers", lambda w,v: "" if v else "%"),
        "notes/xromitcaller":       ("c_xromitcaller", lambda w,v: "" if v else "%"),
        "notes/xrparagraphednotes": (None, lambda w,v: "" if w.get("c_xromitcaller") else "%"),
        "fontbold/embolden":       ("s_boldembolden", lambda w,v: ";embolden={:.2f}".format(v) if v > 0. else ""),
        "fontitalic/embolden":     ("s_italicembolden", lambda w,v: ";embolden={:.2f}".format(v) if v > 0. else ""),
        "fontbolditalic/embolden": ("s_bolditalicembolden", lambda w,v: ";embolden={:.2f}".format(v) if v > 0. else ""),
        "fontbold/slant":          ("s_boldslant", lambda w,v: ";slant={:.4f}".format(v) if v > 0. else ""),
        "fontitalic/slant":        ("s_italicslant", lambda w,v: ";slant={:.4f}".format(v) if v > 0. else ""),
        "fontbolditalic/slant":    ("s_bolditalicslant", lambda w,v: ";slant={:.4f}".format(v) if v > 0. else ""),
    }
    _fonts = {
        "fontregular/name": "f_body",
        "fontbold/name": "f_bold",
        "fontitalic/name": "f_italic",
        "fontbolditalic/name": "f_bolditalic"
    }
    _hdrmappings = {                         # These aren't being saved/remembered yet in the UI!
        "First Reference":  r"\firstref",
        "Last Reference":   r"\lastref",
        "Page Number":      r"\pagenumber",
        "Reference Range":  r"\rangeref",
        "-empty-":          r"\empty"
    }

    def __init__(self, printer, path, ptsettings=None):
        self.ptsettings = ptsettings
        self.changes = None
        self.dict = {"/ptxpath": path}
        for k, v in self._mappings.items():
            val = printer.get(v[0]) if v[0] is not None else None
            if v[1] is not None:
                self.dict[k] = v[1](printer, val)
        self.processFonts(printer)
        self.processHdrFtr(printer)
        self.processCallers(printer)

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
            if True or mirror:   # This doesn't seem to be doing the mirroring (just copying from odd to even)
                self.dict['header/even{}'.format(side)] = t
            self.dict['header/odd{}'.format(side)] = t

    def processCallers(self, printer):
        default = "a b c d e f g h i j k l m n o p q r s t u v w x y z"
        self.dict['footnotes/callers'] = \
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
        if self.changes is None:
            self.changes = self.readChanges(os.path.join(prjdir, 'PrintDraftChanges.txt'))
        customsty = os.path.join(prjdir, 'custom.sty')
        if not os.path.exists(customsty):
            open(customsty, "w").close()
        fbkfm = self.ptsettings['FileNameBookNameForm']
        bknamefmt = fbkfm.replace("MAT","{bkid}").replace("41","{bknum:02d}") + \
                    self.ptsettings['FileNamePostPart']
        fname = bknamefmt.format(bkid=bk, bknum=books.get(bk, 0))
        infname = os.path.join(prjdir, fname)
        if self.changes is not None:
            outfname = os.path.join(outdir, fname)
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:]
            with open(infname, "r", encoding="utf-8") as inf:
                dat = inf.read()
                for c in self.changes:
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
                    changes.append((None, regex.compile(m.group(2), flags=regex.M), m.group(4)))
                    continue
                m = re.match(r"^in\s+(['\"])(.*?)(?<!\\)\1\s*:\s*(['\"])(.*?)(?<!\\)\3\s*>\s*(['\"])(.*?)(?<!\\)\5", l)
                if m:
                    changes.append((regex.compile("("+m.group(2)+")", flags=regex.M), regex.compile(m.group(4), flags=regex.M), m.group(6)))
        if not len(changes):
            return None
        return changes

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
                    if v[0] is None:
                        continue
                    if v[0].startswith("cb_") or v[0].startswith("t_") or v[0].startswith("f_"):
                        printer.set(v[0], config.get(sect, opt))
                    if v[0].startswith("s_"):
                        printer.set(v[0], round(config.get(sect, opt)),2)
                    elif v[0].startswith("c_"):
                        printer.set(v[0], config.getboolean(sect, opt))
                elif key in self._fonts:
                    v = self._fonts[key]
                    printer.set(v, config.get(sect, opt))
