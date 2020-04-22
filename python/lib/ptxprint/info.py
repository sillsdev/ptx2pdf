import configparser, re, os, gi #, time
from datetime import datetime
from shutil import copyfile
import regex
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ptxprint.font import TTFont
from ptxprint.ptsettings import chaps, books, bookcodes, oneChbooks
from ptxprint.snippets import FancyIntro, PDFx1aOutput, FancyBorders

class Info:
    _mappings = {
        # "config/name":              ("cb_savedConfig", lambda w,v: w.builder.get_object("cb_savedConfig").get_active_id()),
        "config/notes":             ("t_configNotes", lambda w,v: v or ""),
        "config/pwd":               ("t_invisiblePassword", lambda w,v: v or ""),

        "project/id":               (None, lambda w,v: w.get("cb_project")),
        "project/hideadvsettings":  ("c_hideAdvancedSettings", lambda w,v: "true" if v else "false"),
        "project/keeptempfiles":    ("c_keepTemporaryFiles", lambda w,v: "true" if v else "false"),
        "project/pdfx1acompliant":  ("c_PDFx1aOutput", lambda w,v: "true" if v else "false"),
        "project/blockexperimental": (None, lambda w,v: "" if w.get("c_experimental") else "%"),
        "project/useptmacros":      ("c_usePTmacros", lambda w,v: "true" if v else "false"),
        "project/ifnotptmacros":    ("c_usePTmacros", lambda w,v: "%" if v else ""),
        "project/multiplebooks":    ("c_multiplebooks", lambda w,v: "true" if v else "false"),
        "project/combinebooks":     ("c_combine", lambda w,v: "true" if v else "false"),
        "project/book":             ("cb_book", None),
        "project/booklist":         ("t_booklist", lambda w,v: v or ""),
        "project/ifinclfrontpdf":   ("c_inclFrontMatter", lambda w,v: "" if v else "%"),
        "project/frontincludes":    ("btn_selectFrontPDFs", lambda w,v: "\n".join('\\includepdf{{{}}}'.format(re.sub(r"\\","/", s)) \
                                                            for s in w.FrontPDFs) if (w.FrontPDFs is not None and w.FrontPDFs != 'None') else ""),
        "project/ifinclbackpdf":    ("c_inclBackMatter", lambda w,v: "" if v else "%"),
        "project/backincludes":     ("btn_selectBackPDFs", lambda w,v: "\n".join('\\includepdf{{{}}}'.format(re.sub(r"\\","/", s)) \
                                                           for s in w.BackPDFs) if (w.BackPDFs is not None and w.BackPDFs != 'None') else ""),
        "project/useprintdraftfolder": ("c_useprintdraftfolder", lambda w,v :"true" if v else "false"),
        "project/processscript":    ("c_processScript", lambda w,v :"true" if v else "false"),
        "project/runscriptafter":   ("c_processScriptAfter", lambda w,v :"true" if v else "false"),
        "project/selectscript":     ("btn_selectScript", lambda w,v: re.sub(r"\\","/", w.CustomScript) if w.CustomScript is not None else ""),
        "project/usechangesfile":   ("c_usePrintDraftChanges", lambda w,v :"true" if v else "false"),
        "project/ifusemodstex":     ("c_useModsTex", lambda w,v: "" if v else "%"),
        "project/ifusecustomsty":   ("c_useCustomSty", lambda w,v: "" if v else "%"),
        "project/ifusemodssty":     ("c_useModsSty", lambda w,v: "" if v else "%"),
        "project/ifusenested":      (None, lambda w,v: "" if (w.get("c_omitallverses") or not w.get("c_includeFootnotes") \
                                                       or not w.get("c_includeXrefs")) or w.get("c_prettyIntroOutline") else "%"),
        "project/ifstarthalfpage":  ("c_startOnHalfPage", lambda w,v :"true" if v else "false"),
        "project/randompicposn":    ("c_randomPicPosn", lambda w,v :"true" if v else "false"),
        "project/showlinenumbers":  ("c_showLineNumbers", lambda w,v :"true" if v else "false"),

        "paper/height":             (None, lambda w,v: re.sub(r"^.*?,\s*(.+?)\s*(?:\(.*|$)", r"\1", w.get("cb_pagesize")) or "210mm"),
        "paper/width":              (None, lambda w,v: re.sub(r"^(.*?)\s*,.*$", r"\1", w.get("cb_pagesize")) or "148mm"),
        "paper/pagesize":           ("cb_pagesize", None),
        "paper/ifwatermark":        ("c_applyWatermark", lambda w,v: "" if v else "%"),
        "paper/watermarkpdf":       ("btn_selectWatermarkPDF", lambda w,v: re.sub(r"\\","/", w.watermarks) \
                                                if (w.watermarks is not None and w.watermarks != 'None') \
                                                else get("/ptxprintlibpath")+"/A5-Draft.pdf"),
        "paper/ifcropmarks":        ("c_cropmarks", lambda w,v :"true" if v else "false"),  
        "paper/ifverticalrule":     ("c_verticalrule", lambda w,v :"true" if v else "false"),
        "paper/margins":            ("s_margins", lambda w,v: round(v) or "14"),
        "paper/topmarginfactor":    ("s_topmarginfactor", lambda w,v: round(v, 2) or "1.60"),
        "paper/bottommarginfactor": ("s_bottommarginfactor", lambda w,v: round(v, 2) or "1.00"),
        "paper/sidemarginfactor":   ("s_sidemarginfactor", lambda w,v: round(v, 2) or "1.00"),
        "paper/ifaddgutter":        ("c_pagegutter", lambda w,v :"true" if v else "false"),
        "paper/gutter":             ("s_pagegutter", lambda w,v: round(v) or "12"),
        "paper/colgutteroffset":    ("s_colgutteroffset", lambda w,v: "{:.1f}".format(v) or "0.0"),
        "paper/columns":            ("c_doublecolumn", lambda w,v: "2" if v else "1"),
        "paper/fontfactor":         ("s_fontsize", lambda w,v: round((v / 12), 3) or "1.000"),

        "fancy/showborderstab":     ("c_showBordersTab", None),
        "fancy/enableborders":      ("c_enableDecorativeElements", lambda w,v: "" if v else "%"),
        "fancy/pageborder":         ("c_inclPageBorder", lambda w,v: "" if v else "%"),
        "fancy/pageborderpdf":      ("btn_selectPageBorderPDF", lambda w,v: re.sub(r"\\","/", w.pageborder) \
                                                if (w.pageborder is not None and w.pageborder != 'None') \
                                                else get("/ptxprintlibpath")+"/A5 page border.pdf"),
        "fancy/sectionheader":      ("c_inclSectionHeader", lambda w,v: "" if v else "%"),
        "fancy/sectionheaderpdf":   ("btn_selectSectionHeaderPDF", lambda w,v: re.sub(r"\\","/", w.sectionheader) \
                                                if (w.sectionheader is not None and w.sectionheader != 'None') \
                                                else get("/ptxprintlibpath")+"/A5 section head border.pdf"),
        "fancy/decorationpdf":      (None, lambda w,v: get("/ptxprintlibpath")+"/decoration.pdf"),
        "fancy/versedecorator":     ("c_inclVerseDecorator", lambda w,v: "" if v else "%"),
        "fancy/versedecoratorpdf":  ("btn_selectVerseDecorator", lambda w,v: re.sub(r"\\","/", w.versedecorator) \
                                                if (w.versedecorator is not None and w.versedecorator != 'None') \
                                                else get("/ptxprintlibpath")+"/Verse number star.pdf"),
        "fancy/versenumsize":       ("s_verseNumSize", lambda w,v: v or "11.00"),

        "paragraph/varlinespacing":    ("c_variableLineSpacing", lambda w,v: "" if v else "%"),
        "paragraph/useglyphmetrics":   ("c_variableLineSpacing", lambda w,v: "%" if v else ""),
        "paragraph/linespacing":       ("s_linespacing", lambda w,v: "{:.3f}".format(v) or "15.000"),
        "paragraph/linespacingfactor": ("s_linespacing", lambda w,v: "{:.3f}".format(float(v or "15") / 14)),
        "paragraph/linemin":           ("s_linespacingmin", lambda w,v: "minus {:.3f}pt".format(w.get("s_linespacing") - v) \
                                                         if v < w.get("s_linespacing") else ""),
        "paragraph/linemax":        ("s_linespacingmax", lambda w,v: "plus {:.3f}pt".format(v - w.get("s_linespacing")) \
                                                         if v > w.get("s_linespacing") else ""),
        "paragraph/ifjustify":      ("c_justify", lambda w,v: "true" if v else "false"),
        "paragraph/ifhyphenate":    ("c_hyphenate", lambda w,v: "" if v else "%"),
        "paragraph/ifnothyphenate": ("c_hyphenate", lambda w,v: "%" if v else ""),
        "paragraph/ifusefallback":  ("c_useFallbackFont", lambda w,v:"true" if v else "false"),
        "paragraph/missingchars":   ("t_missingChars", lambda w,v: v or ""),

        "document/title":           (None, lambda w,v: w.ptsettings.get('FullName', "")),
        "document/subject":         ("t_booklist", lambda w,v: v if w.get("c_multiplebooks") else w.get("cb_book")),
        # "document/author":          (None, lambda w,v: regex.sub("</?p>","",w.ptsettings.get('Copyright', ""))),
        "document/author":          (None, lambda w,v: w.ptsettings.get('Copyright', "")),
        # "document/creator":         (None, lambda w,v: os.getlogin()),  # This is now set to 'PTXprint'

        "document/toc":             ("c_autoToC", lambda w,v: "" if v else "%"),
        "document/toctitle":        ("t_tocTitle", lambda w,v: v or ""),
        "document/usetoc1":         ("c_usetoc1", lambda w,v:"true" if v else "false"),
        "document/usetoc2":         ("c_usetoc2", lambda w,v:"true" if v else "false"),
        "document/usetoc3":         ("c_usetoc3", lambda w,v:"true" if v else "false"),
        "document/chapfrom":        ("cb_chapfrom", lambda w,v: w.builder.get_object("cb_chapfrom").get_active_id()),
        "document/chapto":          ("cb_chapto", lambda w,v: w.builder.get_object("cb_chapto").get_active_id()),
        "document/colgutterfactor": ("s_colgutterfactor", lambda w,v: round(v*3) or "12"), # Hack to be fixed
        "document/ifrtl":           ("cb_textDirection", lambda w,v:"true" if w.builder.get_object("cb_textDirection").get_active_id() \
                                                                              == "Right-to-Left" else "false"),
        "document/toptobottom":     (None, lambda w,v: "" if w.builder.get_object("cb_textDirection").get_active_id() \
                                                                              == "Top-to-Bottom (LTR)" else "%"),
        "document/iflinebreakon":   ("c_linebreakon", lambda w,v: "" if v else "%"),
        "document/linebreaklocale": ("t_linebreaklocale", lambda w,v: v or ""),
        "document/script":          ("cb_script", lambda w,v: ":script="+w.builder.get_object('cb_script').get_active_id().lower() \
                                                  if w.builder.get_object('cb_script').get_active_id() != "Zyyy" else ""),
        "document/digitmapping":    ("cb_digits", lambda w,v: ':mapping=mappings/'+w.get('cb_digits', 1)+'digits' if v != "Default" else ""),
        "document/ch1pagebreak":    ("c_ch1pagebreak", lambda w,v: "true" if v else "false"),
        "document/marginalverses":  ("c_marginalverses", lambda w,v: "" if v else "%"),
        "document/columnshift":     ("s_columnShift", lambda w,v: v or "16"),
        "document/ifomitchapternum":   ("c_omitchapternumber", lambda w,v: "true" if v else "false"),
        "document/ifomitallchapters":  ("c_omitchapternumber", lambda w,v: "" if v else "%"),
        "document/ifomitsinglechnum":  ("c_omitChap1ChBooks", lambda w,v: "true" if v else "false"),
        "document/ifomitverseone":  ("c_omitverseone", lambda w,v: "true" if v else "false"),
        "document/ifomitallverses": ("c_omitallverses", lambda w,v: "" if v else "%"),
        "document/ifmainbodytext":  ("c_mainBodyText", lambda w,v: "true" if v else "false"),
        "document/glueredupwords":  ("c_glueredupwords", lambda w,v :"true" if v else "false"),
        "document/ifinclfigs":      ("c_includeillustrations", lambda w,v :"true" if v else "false"),
        "document/iffigfrmtext":    ("c_includefigsfromtext", lambda w,v :"true" if v else "false"),
        "document/iffigexclwebapp": ("c_figexclwebapp", lambda w,v: "true" if v else "false"),
        "document/iffigskipmissing": ("c_skipmissingimages", lambda w,v: "true" if v else "false"),
        "document/iffigplaceholders": ("c_figplaceholders", lambda w,v :"true" if v else "false"),
        "document/iffighiderefs":   ("c_fighiderefs", lambda w,v :"true" if v else "false"),
        "document/usefigsfolder":   ("c_useLowResPics", lambda w,v :"" if v else "%"),
        "document/uselocalfigs":    ("c_useHighResPics", lambda w,v :"" if v else "%"),
        "document/customfiglocn":   ("c_useCustomFolder", lambda w,v :"" if v else "%"),
        "document/customfigfolder": ("btn_selectFigureFolder", lambda w,v: re.sub(r"\\","/", w.customFigFolder) \
                                                               if w.customFigFolder is not None else ""),
        "document/imagetypepref":   ("t_imageTypeOrder", lambda w,v: v),
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
        "document/ifhidehboxerrors": ("c_showHboxErrorBars", lambda w,v :"%" if v else ""),

        "document/ifdiglot":        ("c_diglot", lambda w,v :"" if v else "%"),
        "document/diglotsettings":  ("l_diglotString", lambda w,v: w.builder.get_object("l_diglotString").get_text() if w.get("c_diglot") else ""),
        "document/diglotpriprj":    ("cb_diglotPriProject", lambda w,v: w.builder.get_object("cb_diglotPriProject").get_active_id()),
        "document/diglotsecprj":    ("cb_diglotSecProject", lambda w,v: w.builder.get_object("cb_diglotSecProject").get_active_id()),
        "document/diglotnormalhdrs": ("c_diglotHeaders", lambda w,v :"" if v else "%"),

        "header/headerposition":    ("s_headerposition", lambda w,v: round(v, 2) or "1.00"),
        "header/footerposition":    ("s_footerposition", lambda w,v: round(v, 2) or "1.00"),
        "header/ifomitrhchapnum":   ("c_omitrhchapnum", lambda w,v :"true" if v else "false"),
        "header/ifverses":          ("c_hdrverses", lambda w,v :"true" if v else "false"),
        "header/chvseparator":      ("c_sepColon", lambda w,v : ":" if v else "."),
        "header/ifrhrule":          ("c_rhrule", lambda w,v: "" if v else "%"),
        "header/ruleposition":      ("s_rhruleposition", lambda w,v: v or "10"),
        "header/hdrleftinner":      ("cb_hdrleft", lambda w,v: v or "-empty-"),
        "header/hdrcenter":         ("cb_hdrcenter", lambda w,v: v or "-empty-"),
        "header/hdrrightouter":     ("cb_hdrright", lambda w,v: v or "-empty-"),
        "header/mirrorlayout":      ("c_mirrorpages", lambda w,v: "true" if v else "false"),
        
        "footer/ftrcenter":         ("cb_ftrcenter", lambda w,v: v or "-empty-"),
        "footer/ifftrtitlepagenum": ("c_pageNumTitlePage", lambda w,v: "" if v else "%"),

        "notes/iffootnoterule":     ("c_footnoterule", lambda w,v: "%" if v else ""),
        "notes/ifblendfnxr":        ("c_blendfnxr", lambda w,v :"true" if v else "false"),
        "notes/blendedxrmkr":       ("cb_blendedXrefCaller", lambda w,v: w.builder.get_object("cb_blendedXrefCaller").get_active_id()),

        "notes/includefootnotes":   ("c_includeFootnotes", lambda w,v: "%" if v else ""),
        "notes/iffnautocallers":    ("c_fnautocallers", lambda w,v :"true" if v else "false"),
        "notes/fncallers":          ("t_fncallers", lambda w,v: v if w.get("c_fnautocallers") else ""),
        "notes/fnresetcallers":     ("c_fnpageresetcallers", lambda w,v: "" if v else "%"),
        "notes/fnomitcaller":       ("c_fnomitcaller", lambda w,v: "%" if v else ""),
        "notes/fnparagraphednotes": ("c_fnparagraphednotes", lambda w,v: "" if v else "%"),
        "notes/glossaryfootnotes":  ("c_glossaryFootnotes", lambda w,v :"true" if v else "false"),

        "notes/includexrefs":       ("c_includeXrefs", lambda w,v: "%" if v else ""),
        "notes/ifxrautocallers":    ("c_xrautocallers", lambda w,v :"true" if v else "false"),
        "notes/xrcallers":          ("t_xrcallers", lambda w,v: v if w.get("c_xrautocallers") else ""),
        "notes/xrresetcallers":     ("c_xrpageresetcallers", lambda w,v: "" if v else "%"),
        "notes/xromitcaller":       ("c_xromitcaller", lambda w,v: "%" if v else ""),
        "notes/xrparagraphednotes": ("c_paragraphedxrefs", lambda w,v: "" if v else "%"),

        "font/features":            ("t_fontfeatures", lambda w,v: v),
        "fontbold/fakeit":          ("c_fakebold", lambda w,v :"true" if v else "false"),
        "fontitalic/fakeit":        ("c_fakeitalic", lambda w,v :"true" if v else "false"),
        "fontbolditalic/fakeit":    ("c_fakebolditalic", lambda w,v :"true" if v else "false"),
        "fontbold/embolden":        ("s_boldembolden", lambda w,v: ":embolden={:.2f}".format(v) if v != 0.00 and w.get("c_fakebold") else ""),
        "fontitalic/embolden":      ("s_italicembolden", lambda w,v: ":embolden={:.2f}".format(v) if v != 0.00 and w.get("c_fakeitalic") else ""),
        "fontbolditalic/embolden":  ("s_bolditalicembolden", lambda w,v: ":embolden={:.2f}".format(v) if v != 0.00 and w.get("c_fakebolditalic") else ""),
        "fontbold/slant":           ("s_boldslant", lambda w,v: ":slant={:.4f}".format(v) if v != 0.0000 and w.get("c_fakebold") else ""),
        "fontitalic/slant":         ("s_italicslant", lambda w,v: ":slant={:.4f}".format(v) if v != 0.0000 and w.get("c_fakeitalic") else ""),
        "fontbolditalic/slant":     ("s_bolditalicslant", lambda w,v: ":slant={:.4f}".format(v) if v != 0.0000 and w.get("c_fakebolditalic") else ""),
    }
    _fonts = {
        "fontregular/name":         ("f_body", None, None, None),
        "fontbold/name":            ("f_bold", "c_fakebold", "fontbold/embolden", "fontbold/slant"),
        "fontitalic/name":          ("f_italic", "c_fakeitalic", "fontitalic/embolden", "fontitalic/slant"),
        "fontbolditalic/name":      ("f_bolditalic", "c_fakebolditalic", "fontbolditalic/embolden", "fontbolditalic/slant"),
        "fontextraregular/name":    ("f_extraRegular", None, None, None),
        "fontfancy/versenumfont":   ("f_verseNumFont", None, None, None)
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
        "with ⸤floor⸥ brackets":   r"\u2E24\1\u2E25",
        "with ⌊floor⌋ characters": r"\u230a\1\u230b",
        "with ⌞corner⌟ characters":r"\u231e\1\u231f",
        "star *before word":       r"*\1",
        "star after* word":        r"\1*",
        "circumflex ^before word": r"^\1",
        "circumflex after^ word":  r"\1^"
    }
    _snippets = {
        "snippets/fancyintro":            ("c_prettyIntroOutline", FancyIntro),
        "snippets/pdfx1aoutput":          ("c_PDFx1aOutput", PDFx1aOutput),
        "snippets/fancyborders":          ("c_enableDecorativeElements", FancyBorders)
    }
    
    def __init__(self, printer, path, prjid = None):
        self.printer = printer
        self.changes = None
        self.localChanges = None
        t = datetime.now()
        tz = t.utcoffset()
        if tz is None:
            tzstr = "Z"
        else:
            tzstr = "{0:+03}'{1:02}'".format(int(tz.seconds / 3600), int((tz.seconds % 3600) / 60))
        libpath = os.path.abspath(os.path.dirname(__file__))
        self.dict = {"/ptxpath": path,
                     "/ptxprintlibpath": libpath,
                     "/iccfpath": os.path.join(libpath, "ps_cmyk.icc").replace("\\","/"),
                     "document/date": t.strftime("%Y%m%d%H%M%S")+tzstr }
        self.prjid = prjid
        self.update()

    def update(self):
        printer = self.printer
        self.updatefields(self._mappings.keys())
        if self.prjid is not None:
            self.dict['project/id'] = self.prjid
        self.dict['project/adjlists'] = os.path.join(printer.configPath(), "AdjLists")
        self.dict['project/piclists'] = os.path.join(printer.configPath(), "PicLists")
        self.processFonts(printer)
        self.processHdrFtr(printer)
        # sort out caseless figures folder. This is a hack
        base = os.path.join(self.dict["/ptxpath"], self.dict["project/id"])
        for p in ("Figures", "figures"):
            picdir = os.path.join(base, p)
            if os.path.exists(picdir):
                break
        self.dict["project/picdir"] = picdir.replace("\\","/")
            

    def updatefields(self, a):
        global get
        def get(k): return self[k]
        for k in a:
            v = self._mappings[k]
            # print(k, v[0])
            val = self.printer.get(v[0]) if v[0] is not None else None
            if v[1] is not None:
                self.dict[k] = v[1](self.printer, val)

    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def processFonts(self, printer):
        silns = "{urn://www.sil.org/ldml/0.1}"
        for p in self._fonts.keys():
            if p in self.dict:
                del self.dict[p]
        for p in ['fontregular/name'] + list(self._fonts.keys()):
            if p in self.dict:
                continue
            wid = self._fonts[p][0]
            f = TTFont(printer.get(wid))
            # print(p, wid, f.filename, f.family, f.style)
            if f.filename is None and p != "fontregular/name" and self._fonts[p][1] is not None:
                reg = printer.get(self._fonts['fontregular/name'][0])
                f = TTFont(reg)
                printer.set(self._fonts[p][1], True)
                printer.set(wid, reg)
                self.updatefields([self._fonts[p][2]])
                # print("Setting {} to {}".format(p, reg))
            d = self.printer.ptsettings.find_ldml('.//special/{1}external-resources/{1}font[@name="{0}"]'.format(f.family, silns))
            featstring = ""
            if d is not None:
                featstring = d.get('features', '')
            if featstring == "":
                featstring = printer.get(self._mappings["font/features"][0])
            if featstring is not None and len(featstring):
                printer.set(self._mappings["font/features"][0], featstring)
                f.features = {}
                for l in re.split(r'\s*[,;:]\s*|\s+', featstring):
                    if '=' in l:
                        k, v = l.split('=')
                        f.features[k.strip()] = v.strip()
                if len(f.features):
                    if p == "fontregular/name":
                        self.dict['font/features'] = ":"+ ":".join("{0}={1}".format(f.feats.get(fid, fid),
                                                    f.featvals.get(fid, {}).get(int(v), v)) for fid, v in f.features.items())
            if 'Silf' in f:
                engine = "/GR"
            else:
                engine = ""
            fname = f.family
            if len(f.style):
                fname = f.family + " " + f.style.title()
            self.dict[p] = fname + engine

    def processHdrFtr(self, printer):
        v = printer.get("cb_ftrcenter")
        self.dict['footer/oddcenter'] = self._hdrmappings.get(v,v)
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

    def asTex(self, template="template.tex", filedir=".", jobname="Unknown"):
        for k, v in self._settingmappings.items():
            if self.dict[k] == "":
                self.dict[k] = self.printer.ptsettings.dict.get(v, "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z")
        res = []
        self.dict['jobname'] = jobname
        with open(os.path.join(os.path.dirname(__file__), template), encoding="utf-8") as inf:
            for l in inf.readlines():
                if l.startswith(r"\ptxfile"):
                    res.append("\\PtxFilePath={"+filedir.replace("\\","/")+"/}\n")
                    for i, f in enumerate(self.dict['project/books']):
                        if self.dict['document/ifomitsinglechnum'] == 'true' and \
                           self.dict['document/ifomitchapternum'] == "false" and \
                           f[2:5] in oneChbooks:
                            res.append("\\OmitChapterNumbertrue\n")
                            res.append("\\ptxfile{{{}}}\n".format(f))
                            res.append("\\OmitChapterNumberfalse\n")
                        else:
                            # print("Else for book: ",f[2:5])
                            res.append("\\ptxfile{{{}}}\n".format(f))
                elif l.startswith(r"%\extrafont"):
                    spclChars = re.sub(r"\\[uU]([0-9a-fA-F]{4,6})", lambda m:chr(int(m.group(1), 16)), self.dict["paragraph/missingchars"])
                    # print(spclChars.split(' '), [len(x) for x in spclChars.split(' ')])
                    if self.dict["paragraph/ifusefallback"] == "true" and len(spclChars):
                        badlist = "\u2018\u2019\u201c\u201d*#%"
                        a = ["".join(chr(ord(c) + 16 if ord(c) < 58 else ord(c) - 23) for c in str(hex(ord(x)))[2:]).lower() for x in spclChars.split(" ")]
                        b = ["".join((c) for c in str(hex(ord(x)))[2:]).lower() for x in spclChars.split(" ")]
                        c = [x for x in zip(a,b) if chr(int(x[1],16)) not in badlist]
                        if not len(c):
                            continue
                        res.append("% for defname @active+ @+digit => 0->@, 1->a ... 9->i A->j B->k .. F->o\n")
                        res.append("% 12 (size) comes from \\p size\n")
                        res.append('\\def\\extraregular{{"{}"}}\n'.format(self.dict["fontextraregular/name"]))
                        res.append("\\catcode`\\@=11\n")
                        res.append("\\def\\do@xtrafont{\\x@\\s@textrafont\\ifx\\thisch@rstyle\\undefined\\m@rker\\else\\thisch@rstyle\\fi}\n")
                        for a,b in c:
                            res.append("\\def\\@ctive{}{{{{\\do@xtrafont {}{}}}}}\n".format(a, '^'*len(b), b))
                            res.append("\\DefineActiveChar{{{}{}}}{{\\@ctive{}}}\n".format( '^'*len(b), b, a))
                        res.append("\\@ctivate\n")
                        res.append("\\catcode`\\@=12\n")
                elif l.startswith(r"%\snippets"):
                    for k, c in self._snippets.items():
                        v = self.printer.get(c[0])
                        if v:
                            if c[1].processTex:
                                res.append(c[1].texCode.format(**self.dict))
                            else:
                                res.append(c[1].texCode)
                else:
                    res.append(l.format(**self.dict))
        return "".join(res).replace("\OmitChapterNumberfalse\n\OmitChapterNumbertrue\n","")

    def convertBook(self, bk, outdir, prjdir):
        if self.changes is None:
            if self.dict['project/usechangesfile'] == "true":
                # if self.changes is None: # Not sure why we aren't doing this every time.
                self.changes = self.readChanges(os.path.join(prjdir, 'PrintDraftChanges.txt'))
            else:
                self.changes = []
        printer = self.printer
        self.makelocalChanges(printer, bk)
        customsty = os.path.join(prjdir, 'custom.sty')
        if not os.path.exists(customsty):
            open(customsty, "w").close()
        fbkfm = self.printer.ptsettings['FileNameBookNameForm']
        fprfx = self.printer.ptsettings['FileNamePrePart'] or ""
        fpost = self.printer.ptsettings['FileNamePostPart'] or ""
        bknamefmt = fprfx + fbkfm.replace("MAT","{bkid}").replace("41","{bkcode}") + fpost
        fname = bknamefmt.format(bkid=bk, bkcode=bookcodes.get(bk, 0))
        infname = os.path.join(prjdir, fname)
        if self.changes is not None or self.localChanges is not None:
            outfname = fname
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:]
            outfpath = os.path.join(outdir, outfname)
            with open(infname, "r", encoding="utf-8") as inf:
                dat = inf.read()
                for c in (self.changes or []) + (self.localChanges or []):
                    if c[0] is None:
                        dat = c[1].sub(c[2], dat)
                    else:
                        newdat = c[0].split(dat)
                        for i in range(1, len(newdat), 2):
                            newdat[i] = c[1].sub(c[2], newdat[i])
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
        qreg = r'(?:"((?:[^"\\]|\\.)*?)"|' + r"'((?:[^'\\]|\\.)*?)')"
        with open(fname, "r", encoding="utf-8") as inf:
            for l in inf.readlines():
                l = l.strip().replace(u"\uFEFF", "")
                l = re.sub(r"\s*#.*$", "", l)
                if not len(l):
                    continue
                m = re.match(r"^"+qreg+r"\s*>\s*"+qreg, l)
                if m:
                    changes.append((None, regex.compile(m.group(1) or m.group(2), flags=regex.M),
                                    m.group(3) or m.group(4) or ""))
                    continue
                m = re.match(r"^in\s+"+qreg+r"\s*:\s*"+qreg+r"\s*>\s*"+qreg, l)
                if m:
                    changes.append((regex.compile("("+(m.group(1) or m.group(2))+")", flags=regex.M), \
                    regex.compile((m.group(3) or m.group(4)), flags=regex.M), (m.group(5) or m.group(6))))
        if not len(changes):
            return None
        if self.printer.get("c_tracing"):
            print("List of PrintDraftChanges:-------------------------------------------------------------")
            report = "\n".join("{} -> {}".format(p[1].pattern, p[2]) for p in changes)
            if getattr(self.printer, "logger", None) is not None:
                self.printer.logger.insert_at_cursor(v)
            else:
                print(report)
        return changes

    def makelocalChanges(self, printer, bk):
        self.localChanges = []
        first = int(printer.get("cb_chapfrom"))
        last = int(printer.get("cb_chapto"))
        
        # This section handles PARTIAL books (from chapter X to chapter Y)
        if not printer.get("c_multiplebooks"):
            if first > 1:
                self.localChanges.append((None, regex.compile(r"\\c 1 ?\r?\n.+(?=\\c {} ?\r?\n)".format(first), flags=regex.S), ""))
            if last < int(chaps.get(bk)):
                self.localChanges.append((None, regex.compile(r"\\c {} ?\r?\n.+".format(last+1), flags=regex.S), ""))

        # Probably need to make this more efficient for multi-book and lengthy glossaries (cache the GLO & changes reqd etc.)
        if printer.get("c_glossaryFootnotes"):
            self.makeGlossaryFootnotes(printer, bk)

        # Glossary Word markup: Remove the second half of the \w word|glossary-form\w* and apply chosen glossary markup
        v = printer.get("cb_glossaryMarkupStyle")
        gloStyle = self._glossarymarkup.get(v, v)
        self.localChanges.append((None, regex.compile(r"\\w (.+?)(\|.+?)?\\w\*", flags=regex.M), gloStyle))

        if printer.get("c_includeillustrations") and printer.get("c_includefigsfromtext"):
            # Remove any illustrations which don't have a |p| 'loc' field IF this setting is on
            if printer.get("c_figexclwebapp"):
                self.localChanges.append((None, regex.compile(r'(?i)\\fig ([^|]*\|){3}([aw]+)\|[^\\]*\\fig\*', flags=regex.M), ''))  # USFM2
                self.localChanges.append((None, regex.compile(r'(?i)\\fig [^\\]*\bloc="[aw]+"[^\\]*\\fig\*', flags=regex.M), ''))    # USFM3

            picChangeList = self.PicNameChanges(printer, bk)
            if len(picChangeList):
                for origfn,tempfn in picChangeList:
                    if tempfn != "":
                        self.localChanges.append((None, regex.compile(r"(?i)(\\fig .*\|){}(\|.+?\\fig\*)".format(origfn), \
                                                     flags=regex.M), r"\1{}\2".format(tempfn)))                               #USFM2
                        self.localChanges.append((None, regex.compile(r'(?i)(\\fig .+?src="{}" .+?\\fig\*)'.format(origfn), \
                                                     flags=regex.M), r"\1{}\2".format(tempfn)))                               #USFM3
                    else:
                        if printer.get("c_skipmissingimages"):
                            self.localChanges.append((None, regex.compile(r"(?i)\\fig .*\|{}\|.+?\\fig\*".format(origfn), flags=regex.M), ""))     #USFM2
                            self.localChanges.append((None, regex.compile(r'(?i)\\fig .+?src="{}" .+?\\fig\*'.format(origfn), flags=regex.M), "")) #USFM3

            if printer.get("c_fighiderefs"): # del ch:vs from caption
                self.localChanges.append((None, regex.compile(r"(\\fig .*?)(\d+[:.]\d+([-,]\d+)?)(.*?\\fig\*)", flags=regex.M), r"\1\4"))
        else: # Drop ALL Figures
            self.localChanges.append((None, regex.compile(r"\\fig .*?\\fig\*", flags=regex.M), ""))
        
        if printer.get("c_omitBookIntro"): # Drop Introductory matter
            self.localChanges.append((None, regex.compile(r"\\i(s|m|mi|p|pi|li\d?|pq|mq|pr|b|q\d?) .+?\r?\n", flags=regex.M), "")) 

        if printer.get("c_omitIntroOutline"): # Drop ALL Intro Outline matter & Intro Outline References
            self.localChanges.append((None, regex.compile(r"\\(iot|io\d) [^\\]+", flags=regex.M), ""))
            self.localChanges.append((None, regex.compile(r"\\ior .+?\\ior\*\s?\r?\n", flags=regex.M), ""))

        if printer.get("c_omitSectHeads"): # Drop ALL Section Headings
            self.localChanges.append((None, regex.compile(r"\\s .+", flags=regex.M), ""))

        if printer.get("c_omitParallelRefs"):# Drop ALL Parallel Passage References
            self.localChanges.append((None, regex.compile(r"\\r .+", flags=regex.M), ""))

        if printer.get("c_blendfnxr"): 
            XrefCaller = printer.get("cb_blendedXrefCaller")
            # To merge/blend \f and \x together, simply change all (\x to \f) (\xo to \fr) and so on...
            self.localChanges.append((None, regex.compile(r"\\x . ", flags=regex.M), r"\\f {} ".format(XrefCaller)))
            self.localChanges.append((None, regex.compile(r"\\x\* ", flags=regex.M), r"\\f* "))
            self.localChanges.append((None, regex.compile(r"\\xq ", flags=regex.M), r"\\fq "))
            self.localChanges.append((None, regex.compile(r"\\xt ", flags=regex.M), r"\\ft "))

        if printer.get("c_preventorphans"): # Prevent orphans at end of *any* paragraph [anything that isn't followed by a \v]
            # self.localChanges.append((None, regex.compile(r" ([^\\ ]+?) ([^\\ ]+?\r?\n)(?!\\v)", flags=regex.S), r" \1\u00A0\2"))
            # OLD RegEx: Keep final two words of \q lines together [but doesn't work if there is an \f or \x at the end of the line] 
            self.localChanges.append((None, regex.compile(r"(\\q\d?(\s?\r?\n?\\v)?( \S+)+( (?!\\)[^\\\s]+)) (\S+\s*\n)", \
                                            flags=regex.M), r"\1\u00A0\5"))

        if printer.get("c_preventwidows"):
            # Push the verse number onto the next line (using NBSP) if there is
            # a short widow word (3 characters or less) at the end of the line
            self.localChanges.append((None, regex.compile(r"(\\v \d+(-\d+)? [\w][\w]?[\w]?) ", flags=regex.M), r"\1\u00A0")) 

        if printer.get("c_ch1pagebreak"):
            self.localChanges.append((None, regex.compile(r"(\\c 1 ?\r?\n)", flags=regex.M), r"\pagebreak\r\n\1"))

        if printer.get("c_glueredupwords"): # keep reduplicated words together
            self.localChanges.append((None, regex.compile(r"(?<=[ ])(\w\w\w+) \1(?=[\s,.!?])", flags=regex.M), r"\1\u00A0\1")) 
        
        if printer.get("c_keepBookWithRefs"): # keep Booknames and ch:vs nums together MH: need help for restricting to \xt and \xo 
            self.localChanges.append((None, regex.compile(r" (\d+:\d+(-\d+)?\))", flags=regex.M), r"\u00A0\1")) 
        
        # Paratext marks no-break space as a tilde ~
        self.localChanges.append((None, regex.compile(r"~", flags=regex.M), r"\u00A0")) 
        # Remove the + of embedded markup (xetex handles it)
        self.localChanges.append((None, regex.compile(r"\\\+", flags=regex.M), r"\\"))  
            
        for c in range(1,4): # Remove any \toc lines that we don't want appearing in the Table of Contents
            if not printer.get("c_usetoc{}".format(c)):
                self.localChanges.append((None, regex.compile(r"(\\toc{} .+)".format(c), flags=regex.M), ""))
        
        # Insert a rule between end of Introduction and start of body text (didn't work earlier, but might work now)
        # self.localChanges.append((None, regex.compile(r"(\\c\s1\s?\r?\n)", flags=regex.S), r"\\par\\vskip\\baselineskip\\hskip-\\columnshift\\hrule\\vskip 2\\baselineskip\n\1"))

        if not printer.get("c_mainBodyText"):
            self.localChanges.append((None, regex.compile(r"\\c 1 ?\r?\n.+".format(first), flags=regex.S), ""))

        # Apply any changes specified in snippets
        for w, c in self._snippets.items():
            if self.printer.get(c[0]): # if the c_checkbox is true then extend the list with those changes
                self.localChanges.extend(c[1].regexes)

        if printer.get("c_tracing"):
            print("List of Local Changes:----------------------------------------------------------")
            report = "\n".join("{} -> {}".format(p[1].pattern, p[2]) for p in self.localChanges)
            if getattr(printer, "logger", None) is not None:
                printer.logger.insert_at_cursor(v)
            else:
                print(report)
        return self.localChanges

    def PicNameChanges(self, printer, bk):
        piclist = []
        pichngs = []
        prjid = self.dict['project/id']
        prjdir = os.path.join(printer.settings_dir, prjid)
        picdir = os.path.join(prjdir, "PrintDraft", "tmpPics")
        fname = printer.getBookFilename(bk, prjdir)
        infname = os.path.join(prjdir, fname)
        # If the preferred image type has been specified, parse that
        imgord = printer.get("t_imageTypeOrder")
        extOrder = []
        if  len(imgord):
            exts = re.findall("([a-z]{3})",imgord.lower())
            for e in exts:
                if e in ["jpg", "png", "pdf"] and e not in extOrder:
                    extOrder += [e]
        if not len(extOrder): # If the user hasn't defined a specifi order then we can assign this
            if printer.get("c_useLowResPics"): # based on whether they want small/compressed image formats
                extOrder = ["jpg", "png", "pdf"] 
            else:                              # or larger high quality uncompresses image formats
                extOrder = ["pdf", "png", "jpg"]
        with open(infname, "r", encoding="utf-8") as inf:
            dat = inf.read()
            inf.close()
            # jpg, tif, png, pdf => [jtp][pdin][gf]
            piclist += re.findall(r"(?i)\\fig .*\|(.+?\.(?=jpg|tif|png|pdf)...)\|.+?\\fig\*", dat)     # Finds USFM2-styled markup in text:
            piclist += re.findall(r'(?i)\\fig .+src="(.+?\.(?=jpg|tif|png|pdf)...)" .+?\\fig\*', dat)  # Finds USFM3-styled markup in text: 
            # piclist = [item.lower() for item in piclist]
            # print(piclist)
            for f in piclist:
                found = False
                basef = f
                basef = re.sub(r"(?i)([a-z][a-z]\d{5})[abc]?\.(jpg|tif|png|pdf)", r"\1",basef)
                basef = re.sub(r"(?i)\.(jpg|tif|png|pdf)", r"",basef)   # This will pick up any non-standard filenames
                for ext in extOrder:
                    tmpf = (basef+"."+ext).lower()
                    fname = os.path.join(picdir,tmpf)
                    if os.path.exists(fname):
                        # print("Found:", f, ">", tmpf)
                        pichngs.append((f,tmpf))
                        found = True
                        break
                if not found:
                    pichngs.append((f,"")) 
        # print(pichngs)
        return(pichngs)

    def _configset(self, config, key, value):
        (sect, k) = key.split("/")
        if not config.has_section(sect):
            config.add_section(sect)
        config.set(sect, k, value)

    def createConfig(self, printer):
        config = configparser.ConfigParser()
        for k, v in self._mappings.items():
            if v[0] is None:
                continue
            val = printer.get(v[0], asstr=True)
            if k in self._settingmappings:
                if val == "" or val == self.printer.ptsettings.dict.get(self._settingmappings[k], ""):
                    continue
            self._configset(config, k, str(val))
        for k, v in self._fonts.items():
            self._configset(config, k, printer.get(v[0], asstr=True))
        for k, v in self._snippets.items():
            self._configset(config, k, str(printer.get(v[0], asstr=True)))
        return config

    def loadConfig(self, printer, config):
        for sect in config.sections():
            for opt in config.options(sect):
                key = "{}/{}".format(sect, opt)
                val = config.get(sect, opt)
                if key in self._mappings:
                    v = self._mappings[key]
                    try: # Safeguarding from changed/missing keys in .cfg
                        if v[0].startswith("cb_") or v[0].startswith("t_") or v[0].startswith("f_") or v[0].startswith("btn_"):
                            pass
                        elif v[0].startswith("s_"):
                            val = float(val)
                        elif v[0].startswith("c_"):
                            val = config.getboolean(sect, opt)
                        else:
                            val = None
                        if val is not None:
                            self.dict[key] = val
                            printer.set(v[0], val)
                    except AttributeError:
                        pass # ignore missing keys 
                elif key in self._fonts:
                    v = self._fonts[key]
                    printer.set(v[0], val)
                elif key in self._snippets:
                    printer.set(self._snippets[key][0], val.lower() == "true")
        for k, v in self._settingmappings.items():
            (sect, name) = k.split("/")
            try:
                val = config.get(sect, name)
            except configparser.NoOptionError:
                printer.set(self._mappings[k][0], self.printer.ptsettings.dict.get(v, ""))
                self.dict[k] = self.printer.ptsettings.get(v, "")
        # Handle specials here:
        printer.CustomScript = self.dict['project/selectscript']
        printer.customFigFolder = self.dict['document/customfigfolder']

        printer.FrontPDFs = self.dict['project/frontincludes'].split("\n")
        if printer.FrontPDFs != None:
            printer.builder.get_object("lb_inclFrontMatter").set_text(",".join(re.sub(r".+[\\/](.+)\.pdf",r"\1",s) for s in printer.FrontPDFs))
        else:
            printer.builder.get_object("lb_inclFrontMatter").set_text("")

        printer.BackPDFs = self.dict['project/backincludes'].split("\n")
        if printer.BackPDFs != None:
            printer.builder.get_object("lb_inclBackMatter").set_text(",".join(re.sub(r".+[\\/](.+)\.pdf",r"\1",s) for s in printer.BackPDFs))
        else:
            printer.builder.get_object("lb_inclBackMatter").set_text("")

# Q.for MH: I'm wondering about how to make this repetitve block of code into a callable funtion with parameters (or looping through a list)
        printer.watermarks = self.dict['paper/watermarkpdf']
        if printer.watermarks != None:
            printer.builder.get_object("lb_applyWatermark").set_text(re.sub(r".+[\\/](.+)\.pdf",r"\1",printer.watermarks))
        else:
            printer.builder.get_object("lb_applyWatermark").set_text("")

        printer.pageborder = self.dict['fancy/pageborderpdf']
        if printer.pageborder != None:
            printer.builder.get_object("lb_inclPageBorder").set_text(re.sub(r".+[\\/](.+)\.pdf",r"\1",printer.pageborder))
        else:
            printer.builder.get_object("lb_inclPageBorder").set_text("")

        printer.sectionheader = self.dict['fancy/sectionheaderpdf']
        if printer.sectionheader != None:
            printer.builder.get_object("lb_inclSectionHeader").set_text(re.sub(r".+[\\/](.+)\.pdf",r"\1",printer.sectionheader))
        else:
            printer.builder.get_object("lb_inclSectionHeader").set_text("")

        printer.versedecorator = self.dict['fancy/versedecoratorpdf']
        if printer.versedecorator != None:
            printer.builder.get_object("lb_inclVerseDecorator").set_text(re.sub(r".+[\\/](.+)\.pdf",r"\1",printer.versedecorator))
        else:
            printer.builder.get_object("lb_inclVerseDecorator").set_text("")

        # update UI to reflect the world it is in 
        # [Comment: this is turning things off even though the file exists. Probably running before the prj has been set?]
        prjdir = os.path.join(printer.settings_dir, printer.prjid)
        if printer.get("c_useCustomSty"):
            if not os.path.exists(os.path.join(prjdir, "custom.sty")):
                printer.set("c_useCustomSty", False)
        for (f, c) in (("PrintDraft-mods.sty", "c_useModsSty"),
                       ("ptxprint-mods.tex", "c_useModsTex")):
            if printer.get(c):
                if not os.path.exists(os.path.join(printer.working_dir, f)):
                    printer.set(c, False)
        self.update()

    def GenerateNestedStyles(self):
        prjid = self.dict['project/id']
        prjdir = os.path.join(self.printer.settings_dir, prjid)
        nstyfname = os.path.join(self.printer.working_dir, "NestedStyles.sty")
        nstylist = []
        if self.printer.get("c_omitallverses"):
            nstylist.append("##### Remove all verse numbers\n\\Marker v\n\\TextProperties nonpublishable\n\n")
        if not self.printer.get("c_includeFootnotes"):
            nstylist.append("##### Remove all footnotes\n\\Marker f\n\\TextProperties nonpublishable\n\n")
        if not self.printer.get("c_includeXrefs"):
            nstylist.append("##### Remove all cross-references\n\\Marker x\n\\TextProperties nonpublishable\n\n")

        for w, c in self._snippets.items():
            if self.printer.get(c[0]): # if the c_checkbox is true then add the stylesheet snippet for that option
                nstylist.append(c[1].styleInfo+"\n")

        if nstylist == []:
            if os.path.exists(nstyfname):
                os.remove(nstyfname)
        else:
            with open(nstyfname, "w", encoding="utf-8") as outf:
                outf.write("".join(nstylist))

    def createHyphenationFile(self):
        listlimit = 32749
        prjid = self.dict['project/id']
        infname = os.path.join(self.printer.settings_dir, prjid, 'hyphenatedWords.txt')
        outfname = os.path.join(self.printer.working_dir, 'hyphen-{}.tex'.format(prjid))
        hyphenatedWords = []
        if not os.path.exists(infname):
            m1 = "Sorry! - Failed to Generate Hyphenation List"
            m2 = "{} Paratext Project's Hyphenation file not found:\n{}".format(prjid, infname)
        else:
            m2b = ""
            m2c = ""
            z = 0
            with open(infname, "r", encoding="utf-8") as inf:
                for l in inf.readlines()[8:]: # Skip over the Paratext header lines
                    l = l.strip().replace(u"\uFEFF", "")
                    l = re.sub(r"\*", "", l)
                    l = re.sub(r"=", "-", l)
                    # Paratext doesn't seem to allow segments of 1 character to be hyphenated  (for example: a-shame-d) 
                    # (so there's nothing to filter them out, because they don't seem to exist!)
                    if "-" in l:
                        if "\u200C" in l or "\u200D" in l or "'" in l: # Temporary workaround until we can figure out how
                            z += 1                                     # to allow ZWNJ and ZWJ to be included as letters.
                        elif re.search('\d', l):
                            pass
                        else:
                            if l[0] != "-":
                                hyphenatedWords.append(l)
            c = len(hyphenatedWords)
            if c >= listlimit:
                m2b = "\n\nThat is too many for XeTeX! List truncated to longest {} words.".format(listlimit)
                hyphenatedWords.sort(key=len,reverse=True)
                shortlist = hyphenatedWords[:listlimit]
                hyphenatedWords = shortlist
            hyphenatedWords.sort(key = lambda s: s.casefold())
            outlist = '\catcode"200C=11\n\catcode"200D=11\n\hyphenation{' + "\n".join(hyphenatedWords) + "}"
            with open(outfname, "w", encoding="utf-8") as outf:
                outf.write(outlist)
            if len(hyphenatedWords) > 1:
                m1 = "Hyphenation List Generated"
                m2a = "{} hyphenated words were gathered\nfrom Paratext's Hyphenation Word List.".format(c)
                if z > 0:
                    m2c = "\n\nNote for Indic languages that {} words containing ZWJ".format(z) + \
                            "\nand ZWNJ characters have been left off the hyphenation list." 
                m2 = m2a + m2b + m2c
            else:
                m1 = "Sorry - Hyphenation List was NOT Generated"
                m2 = "No valid words were found in Paratext's Hyphenation List"
        dialog = Gtk.MessageDialog(parent=None, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.ERROR, \
                                    buttons=Gtk.ButtonsType.OK, message_format=m1)
        dialog.format_secondary_text(m2)
        dialog.run()
        dialog.destroy()

    def makeGlossaryFootnotes(self, printer, bk):
        # Glossary entries for the key terms appearing like footnotes
        prjid = self.dict['project/id']
        prjdir = os.path.join(printer.settings_dir, prjid)
        fname = printer.getBookFilename("GLO", prjdir)
        infname = os.path.join(prjdir, fname)
        if os.path.exists(infname):
            with open(infname, "r", encoding="utf-8") as inf:
                dat = inf.read()
                ge = re.findall(r"\\p \\k (.+)\\k\* (.+)\r?\n", dat) # Finds all glossary entries in GLO book
                if ge is not None:
                    for g in ge:
                        gdefn = regex.sub(r"\\xt (.+)\\xt\*", r"\1", g[1])
                        # print(r"(\\w (.+\|)?{} ?\\w\*)".format(f[0]), " --> ", r"\1\f + \fq {} \ft {}...\f* ".format(g[0],g[1][:20]))
                        self.localChanges.append((None, regex.compile(r"(\\w (.+\|)?{} ?\\w\*)".format(g[0]), flags=regex.M), \
                                                                     r"\1\\f + \\fq {}: \\ft {}\\f* ".format(g[0],gdefn)))
