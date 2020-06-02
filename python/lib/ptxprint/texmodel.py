import configparser, re, os, gi #, time
from datetime import datetime
from shutil import copyfile
from pathlib import Path
import regex
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ptxprint.font import TTFont
from ptxprint.ptsettings import chaps, books, bookcodes, oneChbooks
from ptxprint.snippets import FancyIntro, PDFx1aOutput, AlignedDiglot, FancyBorders
from ptxprint.runner import checkoutput

pdfre = re.compile(r".+[\\/](.+)\.pdf")

def universalopen(fname, rewrite=False):
    """ Opens a file with the right codec from a small list and perhaps rewrites as utf-8 """
    fh = open(fname, "r", encoding="utf-8")
    try:
        fh.readline()
        fh.seek(0)
        return fh
    except ValueError:
        pass
    fh = open(fname, "r", encoding="utf-16")
    fh.readline()
    fh.seek(0)
    if rewrite:
        dat = fh.readlines()
        fh.close()
        with open(fname, "w", encoding="utf-8") as fh:
            for d in dat:
                fh.write(d)
        fh = open(fname, "r", encoding="utf-8", errors="ignore")
    return fh

ModelMap = {
    "L":                        ("c_diglotAutoAligned", lambda w,v: "L" if v else ""),
    #"config/name":              ("ecb_savedConfig", lambda w,v: v or "default"),
    "config/notes":             ("t_configNotes", lambda w,v: v or ""),
    "config/pwd":               ("t_invisiblePassword", lambda w,v: v or ""),

    # "project/id":               ("fcb_project", None),
    "project/hideadvsettings":  ("c_hideAdvancedSettings", None),
    "project/showlayouttab":    ("c_showLayoutTab", None),
    "project/showbodytab":      ("c_showBodyTab", None),
    "project/showheadfoottab":  ("c_showHeadFootTab", None),
    "project/showpicturestab":  ("c_showPicturesTab", None),
    "project/showadvancedtab":  ("c_showAdvancedTab", None),
    "project/showviewertab":    ("c_showViewerTab", None),
    "project/showdiglottab":    ("c_showDiglotTab", None),
    "project/showborderstab":   ("c_showBordersTab", None),
    "project/keeptempfiles":    ("c_keepTemporaryFiles", None),
    "project/pdfx1acompliant":  ("c_PDFx1aOutput", None),
    "project/blockexperimental": ("c_experimental", lambda w,v: "" if v else "%"),
    "project/multiplebooks":    ("c_multiplebooks", None),
    "project/combinebooks":     ("c_combine", None),
    "project/book":             ("ecb_book", None),
    "project/booklist":         ("t_booklist", lambda w,v: v or ""),
    "project/ifinclfrontpdf":   ("c_inclFrontMatter", None),
    "project/frontincludes":    ("btn_selectFrontPDFs", lambda w,v: "\n".join('\\includepdf{{{}}}'.format(s.as_posix()) \
                                 for s in w.FrontPDFs) if (w.get("c_inclFrontMatter") and w.FrontPDFs is not None and w.FrontPDFs != 'None') else ""),
    "project/ifinclbackpdf":    ("c_inclBackMatter", None),
    "project/backincludes":     ("btn_selectBackPDFs", lambda w,v: "\n".join('\\includepdf{{{}}}'.format(s.as_posix()) \
                                 for s in w.BackPDFs) if (w.get("c_inclFrontMatter") and w.BackPDFs is not None and w.BackPDFs != 'None') else ""),
    "project/useprintdraftfolder": ("c_useprintdraftfolder", lambda w,v :"true" if v else "false"),
    "project/processscript":    ("c_processScript", None),
    "project/runscriptafter":   ("c_processScriptAfter", None),
    "project/selectscript":     ("btn_selectScript", lambda w,v: w.customScript.as_posix() if w.customScript is not None else ""),
    "project/usechangesfile":   ("c_usePrintDraftChanges", lambda w,v :"true" if v else "false"),
    "project/ifusemodstex":     ("c_useModsTex", lambda w,v: "" if v else "%"),
    "project/ifusecustomsty":   ("c_useCustomSty", lambda w,v: "" if v else "%"),
    "project/ifusemodssty":     ("c_useModsSty", lambda w,v: "" if v else "%"),
    "project/ifstarthalfpage":  ("c_startOnHalfPage", lambda w,v :"true" if v else "false"),
    "project/randompicposn":    ("c_randomPicPosn", None),
    "project/showlinenumbers":  ("c_showLineNumbers", None),

    "paper/height":             ("ecb_pagesize", lambda w,v: re.sub(r"^.*?,\s*(.+?)\s*(?:\(.*|$)", r"\1", v) or "210mm"),
    "paper/width":              ("ecb_pagesize", lambda w,v: re.sub(r"^(.*?)\s*,.*$", r"\1", v) or "148mm"),
    "paper/pagesize":           ("ecb_pagesize", None),
    "paper/ifwatermark":        ("c_applyWatermark", None),
    "paper/watermarkpdf":       ("btn_selectWatermarkPDF", lambda w,v: '\def\PageBorder{{"{}"}}'.format(w.watermarks.as_posix()) \
                                 if (w.get("c_applyWatermark") and w.watermarks is not None and w.watermarks != 'None') else ""),
    "paper/ifcropmarks":        ("c_cropmarks", lambda w,v :"true" if v else "false"),  
    "paper/ifverticalrule":     ("c_verticalrule", lambda w,v :"true" if v else "false"),
    "paper/margins":            ("s_margins", lambda w,v: round(v) or "14"),
    "paper/topmarginfactor":    ("s_topmarginfactor", lambda w,v: round(v, 2) or "1.60"),
    "paper/bottommarginfactor": ("s_bottommarginfactor", lambda w,v: round(v, 2) or "1.00"),
    "paper/sidemarginfactor":   ("s_sidemarginfactor", lambda w,v: round(v, 2) or "1.00"),
    "paper/ifaddgutter":        ("c_pagegutter", lambda w,v :"true" if v else "false"),
    "paper/gutter":             ("s_pagegutter", lambda w,v: round(v) or "0"),
    "paper/colgutteroffset":    ("s_colgutteroffset", lambda w,v: "{:.1f}".format(v) or "0.0"),
    "paper/columns":            ("c_doublecolumn", lambda w,v: "2" if v else "1"),
    "paper/fontfactor":         ("s_fontsize", lambda w,v: round((v / 12), 3) or "1.000"),

    "fancy/showborderstab":     ("c_showBordersTab", None),
    "fancy/enableborders":      ("c_borders", lambda w,v: "" if v else "%"),
    "fancy/pageborder":         ("c_inclPageBorder", lambda w,v: "" if v else "%"),
    "fancy/pageborderpdf":      ("btn_selectPageBorderPDF", lambda w,v: w.pageborder.as_posix() \
                                            if (w.pageborder is not None and w.pageborder != 'None') \
                                            else get("/ptxprintlibpath")+"/A5 page border.pdf"),
    "fancy/sectionheader":      ("c_inclSectionHeader", lambda w,v: "" if v else "%"),
    "fancy/sectionheaderpdf":   ("btn_selectSectionHeaderPDF", lambda w,v: w.sectionheader.as_posix() \
                                            if (w.sectionheader is not None and w.sectionheader != 'None') \
                                            else get("/ptxprintlibpath")+"/A5 section head border.pdf"),
    "fancy/decorationpdf":      (None, lambda w,v: get("/ptxprintlibpath")+"/decoration.pdf"),
    "fancy/versedecorator":     ("c_inclVerseDecorator", lambda w,v: "" if v else "%"),
    "fancy/versedecoratorpdf":  ("btn_selectVerseDecorator", lambda w,v: w.versedecorator.as_posix() \
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
    "paragraph/ifomithyphen":   ("c_omitHyphen", lambda w,v: "" if v else "%"),
    "paragraph/ifnothyphenate": ("c_hyphenate", lambda w,v: "%" if v else ""),
    "paragraph/ifusefallback":  ("c_useFallbackFont", None),
    "paragraph/missingchars":   ("t_missingChars", lambda w,v: v or ""),

    "document/title":           (None, lambda w,v: w.ptsettings.get('FullName', "")),
    "document/subject":         ("t_booklist", lambda w,v: v if w.get("c_multiplebooks") else w.get("ecb_book")),
    "document/author":          (None, lambda w,v: w.ptsettings.get('Copyright', "")),
    # "document/author":          (None, lambda w,v: re.sub('"?</?p>"?','',w.ptsettings.get('Copyright', "")).strip('"')),

    "document/startpagenum":    ("s_startPageNum", lambda w,v: int(v) or "1"),
    "document/toc":             ("c_autoToC", lambda w,v: "" if v else "%"),
    "document/toctitle":        ("t_tocTitle", lambda w,v: v or ""),
    "document/usetoc1":         ("c_usetoc1", None),
    "document/usetoc2":         ("c_usetoc2", None),
    "document/usetoc3":         ("c_usetoc3", None),
    "document/chapfrom":        ("fcb_chapfrom", None),
    "document/chapto":          ("fcb_chapto", None),
    "document/colgutterfactor": ("s_colgutterfactor", lambda w,v: round(v*3) or "12"), # Hack to be fixed
    "document/ifrtl":           ("fcb_textDirection", lambda w,v:"true" if v == "Right-to-Left" else "false"),
    "document/toptobottom":     ("fcb_textDirection", lambda w,v: "" if v == "Top-to-Bottom (LTR)" else "%"),
    "document/iflinebreakon":   ("c_linebreakon", lambda w,v: "" if v else "%"),
    "document/linebreaklocale": ("t_linebreaklocale", lambda w,v: v or ""),
    "document/script":          ("fcb_script", lambda w,v: ":script="+v.lower() if v != "Zyyy" else ""),
    "document/digitmapping":    ("fcb_digits", lambda w,v: ':mapping=mappings/'+v+'digits' if v != "Default" else ""),
    "document/ch1pagebreak":    ("c_ch1pagebreak", None),
    "document/marginalverses":  ("c_marginalverses", lambda w,v: "" if v else "%"),
    "document/columnshift":     ("s_columnShift", lambda w,v: v or "16"),
    "document/ifomitchapternum":   ("c_omitchapternumber", lambda w,v: "true" if v else "false"),
    "document/ifomitallchapters":  ("c_omitchapternumber", lambda w,v: "" if v else "%"),
    "document/ifomitsinglechnum":  ("c_omitChap1ChBooks", lambda w,v: v),
    "document/ifomitverseone":  ("c_omitverseone", lambda w,v: "true" if v else "false"),
    "document/ifomitallverses": ("c_omitallverses", lambda w,v: "" if v else "%"),
    "document/ifmainbodytext":  ("c_mainBodyText", None),
    "document/glueredupwords":  ("c_glueredupwords", None),
    "document/ifinclfigs":      ("c_includeillustrations", lambda w,v: "true" if v else "false"),
    "document/iffigfrmtext":    ("c_includefigsfromtext", None),
    "document/iffigexclwebapp": ("c_figexclwebapp", None),
    "document/iffigskipmissing": ("c_skipmissingimages", None),
    "document/iffigplaceholders": ("c_figplaceholders", lambda w,v: "true" if v else "false"),
    "document/iffighiderefs":   ("c_fighiderefs", None),
    "document/usesmallpics":    ("c_useLowResPics", lambda w,v :"" if v else "%"),
    "document/uselargefigs":    ("c_useHighResPics", lambda w,v :"" if v else "%"),
    "document/customfiglocn":   ("c_useCustomFolder", lambda w,v :"" if v else "%"),
    "document/exclusivefolder": ("c_exclusiveFiguresFolder", None),
    "document/customfigfolder": ("btn_selectFigureFolder", lambda w,v: w.customFigFolder.as_posix() if w.customFigFolder is not None else ""),
    "document/imagetypepref":   ("t_imageTypeOrder", None),
    "document/ifusepiclist":    ("c_usePicList", lambda w,v :"" if v else "%"),
    "document/spacecntxtlztn":  ("ecb_spaceCntxtlztn", lambda w,v: "0" if v == "None" else "1" if v == "Some" else "2"),
    "document/glossarymarkupstyle":  ("fcb_glossaryMarkupStyle", None),
    "document/filterglossary":  ("c_filterGlossary", None),
    "document/hangpoetry":      ("c_hangpoetry", lambda w,v: "" if v else "%"),
    "document/preventorphans":  ("c_preventorphans", None),
    "document/preventwidows":   ("c_preventwidows", None),
    "document/supresssectheads": ("c_omitSectHeads", None),
    "document/supressparallels": ("c_omitParallelRefs", None),
    "document/supressbookintro": ("c_omitBookIntro", None),
    "document/supressintrooutline": ("c_omitIntroOutline", None),
    "document/supressindent":   ("c_omit1paraIndent", lambda w,v: "false" if v else "true"),
    "document/ifhidehboxerrors": ("c_showHboxErrorBars", lambda w,v :"%" if v else ""),
    "document/elipsizemptyvs":  ("c_elipsizeMissingVerses", None),
    "document/ifspacing":       ("c_spacing", lambda w,v :"" if v else "%"),
    "document/spacestretch":    ("s_maxSpace", lambda w,v : str((int(v) - 100) / 100.)),
    "document/spaceshrink":     ("s_minSpace", lambda w,v : str((100 - int(v)) / 100.)),
    "document/ifcolorfonts":    ("c_colorfonts", lambda w,v: "%" if v else ""),

    "document/ifchaplabels":    ("c_useChapterLabel", lambda w,v: "%" if v else ""),
    "document/clabelbooks":     ("t_clBookList", lambda w,v: v.upper()),
    "document/clabel":          ("t_clHeading", None),
    "document/clsinglecol":     ("c_clSingleColLayout", None),

    "document/ifdiglot":        ("c_diglot", lambda w,v : "" if v else "%"),
    "document/ifaligndiglot":   ("c_diglotAutoAligned", lambda w,v: "" if v else "%"),
    "document/diglotalignment": ("fcb_diglotAlignment", None),
    "document/diglotprifraction": ("s_diglotPriFraction", lambda w,v : round((v/100), 3) or "0.550"),
    "document/diglotsecfraction": ("s_diglotPriFraction", lambda w,v : round(1 - (v/100), 3) or "0.450"),
    "document/diglotsecprj":    ("fcb_diglotSecProject", None),
    "document/diglotswapside":  ("c_diglotSwapSide", lambda w,v: v),
    "document/diglotsepnotes":  ("c_diglotSeparateNotes", lambda w,v: "true" if v else "false"),
    "document/diglotsecconfig": ("ecb_diglotSecConfig", None),
    "document/diglotnormalhdrs": ("c_diglotHeaders", lambda w,v :"" if v else "%"),

    "header/headerposition":    ("s_headerposition", lambda w,v: round(v, 2) or "1.00"),
    "header/footerposition":    ("s_footerposition", lambda w,v: round(v, 2) or "1.00"),
    "header/ifomitrhchapnum":   ("c_omitrhchapnum", lambda w,v :"true" if v else "false"),
    "header/ifverses":          ("c_hdrverses", lambda w,v :"true" if v else "false"),
    "header/chvseparator":      ("c_sepColon", lambda w,v : ":" if v else "."),
    "header/ifrhrule":          ("c_rhrule", lambda w,v: "" if v else "%"),
    "header/ruleposition":      ("s_rhruleposition", lambda w,v: v or "10"),
    "header/hdrleft":           ("ecb_hdrleft", lambda w,v: v or "-empty-"),
    "header/hdrcenter":         ("ecb_hdrcenter", lambda w,v: v or "-empty-"),
    "header/hdrright":          ("ecb_hdrright", lambda w,v: v or "-empty-"),
    "header/mirrorlayout":      ("c_mirrorpages", lambda w,v: "true" if v else "false"),
    
    "footer/ftrcenter":         ("ecb_ftrcenter", lambda w,v: v or "-empty-"),
    "footer/ifftrtitlepagenum": ("c_pageNumTitlePage", lambda w,v: "" if v else "%"),
    "footer/ifprintConfigName": ("c_printConfigName", lambda w,v: "" if v else "%"),

    "notes/iffootnoterule":     ("c_footnoterule", lambda w,v: "%" if v else ""),
    "notes/ifblendfnxr":        ("c_blendfnxr", lambda w,v :"true" if v else "false"),
    "notes/blendedxrmkr":       ("fcb_blendedXrefCaller", None),

    "notes/includefootnotes":   ("c_includeFootnotes", lambda w,v: "%" if v else ""),
    "notes/iffnautocallers":    ("c_fnautocallers", lambda w,v :"true" if v else "false"),
    "notes/fncallers":          ("t_fncallers", lambda w,v: v if w.get("c_fnautocallers") else ""),
    "notes/fnresetcallers":     ("c_fnpageresetcallers", lambda w,v: "" if v else "%"),
    "notes/fnomitcaller":       ("c_fnomitcaller", lambda w,v: "%" if v else ""),
    "notes/fnparagraphednotes": ("c_fnparagraphednotes", lambda w,v: "" if v else "%"),
    "notes/addcolon":           ("c_addColon", None),
    "notes/keepbookwithrefs":   ("c_keepBookWithRefs", None),
    "notes/glossaryfootnotes":  ("c_glossaryFootnotes", None),

    "notes/includexrefs":       ("c_includeXrefs", lambda w,v: "%" if v else ""),
    "notes/ifxrautocallers":    ("c_xrautocallers", lambda w,v :"true" if v else "false"),
    "notes/xrcallers":          ("t_xrcallers", lambda w,v: v if w.get("c_xrautocallers") else ""),
    "notes/xrresetcallers":     ("c_xrpageresetcallers", lambda w,v: "" if v else "%"),
    "notes/xromitcaller":       ("c_xromitcaller", lambda w,v: "%" if v else ""),
    "notes/xrparagraphednotes": ("c_paragraphedxrefs", lambda w,v: "" if v else "%"),

    "notes/abovenotespace":     ("s_abovenotespace", lambda w,v: "{:.3f}".format(float(v))),
    "notes/fnfontsize":         ("s_fnfontsize", lambda w,v: "{:.3f}".format(float(v))),
    "notes/fnlinespacing":      ("s_fnlinespacing", lambda w,v: "{:.3f}".format(float(v))),
    "notes/internotespace":     ("s_internote", lambda w,v: "{:.3f}".format(float(v))),

    "fontregular":              ("bl_fontR", lambda w,v: v[0]),
    "fontbold":                 ("bl_fontB", lambda w,v: v[0]),
    "fontitalic":               ("bl_fontI", lambda w,v: v[0]),
    "fontbolditalic":           ("bl_fontBI", lambda w,v: v[0]),
    "fontextraregular":         ("bl_fontExtraR", lambda w,v: v[0]),
    "versenumfont":             ("bl_verseNumFont", lambda w,v: v[0]),
    "font/features":            ("t_fontfeatures", None),
    "font/usegraphite":         ("c_useGraphite", None),
    "fontbold/fakeit":          ("c_fakebold", None),
    "fontitalic/fakeit":        ("c_fakeitalic", None),
    "fontbolditalic/fakeit":    ("c_fakebolditalic", None),
    "fontbold/embolden":        ("s_boldembolden", lambda w,v: ":embolden={:.2f}".format(v) if v != 0.00 and w.get("c_fakebold") else ""),
    "fontitalic/embolden":      ("s_italicembolden", lambda w,v: ":embolden={:.2f}".format(v) if v != 0.00 and w.get("c_fakeitalic") else ""),
    "fontbolditalic/embolden":  ("s_bolditalicembolden", lambda w,v: ":embolden={:.2f}".format(v) if v != 0.00 and w.get("c_fakebolditalic") else ""),
    "fontbold/slant":           ("s_boldslant", lambda w,v: ":slant={:.4f}".format(v) if v != 0.0000 and w.get("c_fakebold") else ""),
    "fontitalic/slant":         ("s_italicslant", lambda w,v: ":slant={:.4f}".format(v) if v != 0.0000 and w.get("c_fakeitalic") else ""),
    "fontbolditalic/slant":     ("s_bolditalicslant", lambda w,v: ":slant={:.4f}".format(v) if v != 0.0000 and w.get("c_fakebolditalic") else ""),
    "snippets/fancyintro":      ("c_prettyIntroOutline", None),
    "snippets/pdfx1aoutput":    ("c_PDFx1aOutput", None),
    "snippets/alignediglot":    ("c_diglotAutoAligned", None),
    "snippets/fancyborders":    ("c_borders", None),
}

class TexModel:
    _peripheralBooks = ["FRT", "INT", "GLO", "TDX", "NDX", "CNC", "OTH", "BAK", "XXA", "XXB", "XXC", "XXD", "XXE", "XXF", "XXG"]
    _fonts = {
        "fontregular":              ("bl_fontR", None, None, None),
        "fontbold":                 ("bl_fontB", "c_fakebold", "fontbold/embolden", "fontbold/slant"),
        "fontitalic":               ("bl_fontI", "c_fakeitalic", "fontitalic/embolden", "fontitalic/slant"),
        "fontbolditalic":           ("bl_fontBI", "c_fakebolditalic", "fontbolditalic/embolden", "fontbolditalic/slant"),
        "fontextraregular":         ("bl_fontExtraR", None, None, None),
        "versenumfont":             ("bl_verseNumFont", None, None, None)
    }
    _hdrmappings = {
        "First Reference":  r"\firstref",
        "Last Reference":   r"\lastref",
        "Page Number":      r"\pagenumber",
        "Reference Range":  r"\rangeref",
        "-empty-":          r"\empty"
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
        "snippets/alignediglot":          ("c_diglotAutoAligned", AlignedDiglot),
        "snippets/fancyborders":          ("c_borders", FancyBorders)
    }
    _settingmappings = {
        "notes/xrcallers": "crossrefs",
        "notes/fncallers": "footnotes"
    }

    def __init__(self, printer, path, ptsettings, prjid=None):
        self.printer = printer
        self.ptsettings = ptsettings
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
        if self.prjid is not None:
            self.dict['project/id'] = self.prjid
        if self.printer is not None:
            self.update()

    def update(self):
        """ Update model from UI """
        self.updatefields(ModelMap.keys())
        if self.asBool("project/useprintdraftfolder"):
            base = os.path.join(self.dict["/ptxpath"], self.dict["project/id"])
            docdir = os.path.join(base, 'PrintDraft')
        else:
            base = printer.working_dir
            docdir = base
        self.dict["document/directory"] = os.path.abspath(docdir).replace("\\","/")
        self.dict['project/adjlists'] = os.path.join(self.printer.configPath(), "AdjLists/").replace("\\","/")
        self.dict['project/piclists'] = os.path.join(self.printer.working_dir, "tmpPicLists/").replace("\\","/")
        self.dict['project/id'] = self.printer.prjid
        self.dict['config/name'] = self.printer.configId
        self.readFonts(self.printer)
        self.processFonts(self.printer)
        self.processHdrFtr(self.printer)
        # sort out caseless figures folder. This is a hack
        for p in ("Figures", "figures"):
            picdir = os.path.join(base, p)
            if os.path.exists(picdir):
                break
        self.dict["project/picdir"] = picdir.replace("\\","/")
        # Look in local Config folder for ptxprint-mods.tex, and drop back to shared/ptxprint if not found 
        fpath = os.path.join(self.printer.configPath(), "ptxprint-mods.tex")
        if not os.path.exists(fpath):
            fpath = os.path.join(self.dict["/ptxpath"], self.dict["project/id"], "shared", "ptxprint", "ptxprint-mods.tex")
        self.dict['/modspath'] = fpath.replace("\\","/")

    def updatefields(self, a):
        global get
        def get(k): return self[k]
        for k in a:
            v = ModelMap[k]
            val = self.printer.get(v[0]) if v[0] is not None else None
            if v[1] is not None:
                self.dict[k] = v[1](self.printer, val)
            else:
                self.dict[k] = val

    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def asBool(self, key, true=None, false=None):
        val = self.dict.get(key, None)
        if val is None:
            return False
        elif true is not None:
            return val == true
        elif false is not None:
            return val != false
        elif isinstance(val, bool):
            return val
        elif val == "%" or val == "false":
            return False
        else:
            return True

    def readFonts(self, printer):
        for k, v in self._fonts.items():
            finfo = printer.get(v[0])
            # print(k, v[0], finfo)
            for i, a in enumerate(("name", "style")):
                self.dict[k+"/"+a] = finfo[i]

    def processFonts(self, printer):
        """ Update model fonts from UI """
        for p in self._fonts.keys():
            if p in self.dict:
                del self.dict[p]
        frn = self.dict.get("fontregular/name", "")
        if frn is None or frn == "":
            self.dict["fontregular/name"] = "Arial"     # Fallback
        for p in ['fontregular'] + list(self._fonts.keys()):
            if p in self.dict:
                continue
            name = self.dict.get(p+"/name", "")
            style = self.dict.get(p+"/style", "")
            f = TTFont(name, style)
            # print(p, wid, f.filename, f.family, f.style)
            if f.filename is None and p != "fontregular" and self._fonts[p][1] is not None:
                regname = self.dict["fontregular/name"]
                regstyle = self.dict["fontregular/style"]
                f = TTFont(regname, regstyle)
                if printer is not None:
                    printer.set(self._fonts[p][1], True)
                    printer.set(self._fonts[p][0], (name, style))
                    self.updatefields([self._fonts[p][2]])
                    # print("Setting {} to {}".format(p, reg))
            if 'Silf' in f and self.asBool("font/usegraphite"):
                engine = "/GR"
            else:
                engine = ""
            fname = f.family
            if f.style is not None and len(f.style):
                fname = f.family + " " + f.style.title()
            self.dict[p] = fname
            self.dict[p+"/engine"] = engine
        featstring = self.dict["font/features"]
        if featstring is not None and len(featstring):
            if printer is not None:
                printer.set(ModelMap["font/features"][0], featstring)
            f.features = {}
            for l in re.split(r'\s*[,;:]\s*|\s+', featstring):
                if '=' in l:
                    k, v = l.split('=')
                    f.features[k.strip()] = v.strip()
            if len(f.features):
                self.dict['font/texfeatures'] = ":"+ ":".join("{0}={1}".format(f.feats.get(fid, fid),
                                                f.featvals.get(fid, {}).get(int(v), v)) for fid, v in f.features.items())
            else:
                self.dict['font/texfeatures'] = ""
        else:
            self.dict['font/texfeatures'] = ""
        
    def processHdrFtr(self, printer):
        """ Update model headers from model UI read values """
        v = self.dict["footer/ftrcenter"]
        self.dict['footer/oddcenter'] = self._hdrmappings.get(v,v)
        mirror = self.asBool("header/mirrorlayout")
        for side in ('left', 'center', 'right'):
            v = self.dict["header/hdr"+side]
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
                self.dict[k] = self.ptsettings.dict.get(v, "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z")
        res = []
        self.dict['jobname'] = jobname
        with universalopen(os.path.join(os.path.dirname(__file__), template)) as inf:
            for l in inf.readlines():
                if l.startswith(r"\ptxfile"):
                    res.append("\\PtxFilePath={"+filedir.replace("\\","/")+"/}\n")
                    for i, f in enumerate(self.dict['project/bookids']):
                        fname = self.dict['project/books'][i]
                        if self.asBool('document/ifomitsinglechnum') and \
                           self.dict['document/ifomitchapternum'] == "false" and \
                           f in oneChbooks:
                            res.append("\\OmitChapterNumbertrue\n")
                            res.append("\\ptxfile{{{}}}\n".format(fname))
                            res.append("\\OmitChapterNumberfalse\n")
                        elif self.dict['paper/columns'] == '2' and \
                             self.dict['document/clsinglecol'] and \
                             f in self.dict['document/clabelbooks']:
                            res.append("\\BodyColumns=1\n")
                            res.append("\\ptxfile{{{}}}\n".format(fname))
                            res.append("\\BodyColumns=2\n")
                        else:
                            res.append("\\ptxfile{{{}}}\n".format(fname))
                elif l.startswith(r"%\extrafont"):
                    spclChars = re.sub(r"\\[uU]([0-9a-fA-F]{4,6})", lambda m:chr(int(m.group(1), 16)), self.dict["paragraph/missingchars"])
                    # print(spclChars.split(' '), [len(x) for x in spclChars.split(' ')])
                    if self.dict["paragraph/ifusefallback"] and len(spclChars):
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
                    else:
                        res.append("% No special/missing characters specified for fallback font")
                elif l.startswith(r"%\snippets"):
                    for k, c in self._snippets.items():
                        if self.printer is None:
                            v = self.asBool(k)
                        else:
                            v = self.printer.get(c[0])
                            self.dict[k] = "true" if v else "false"
                        if v:
                            if c[1].processTex:
                                res.append(c[1].texCode.format(**self.dict))
                            else:
                                res.append(c[1].texCode)
                else:
                    res.append(l.format(**self.dict))
        return "".join(res).replace("\OmitChapterNumberfalse\n\OmitChapterNumbertrue\n","")

    def runConversion(self, infpath, outdir):
        outfpath = infpath
        if self.dict['project/processscript'] and self.dict['project/selectscript']:
            outfpath = os.path.join(outdir, os.path.basename(infpath))
            doti = outfpath.rfind(".")
            if doti > 0:
                outfpath = outfpath[:doti] + "-conv" + outfpath[doti:]
            cmd = [self.dict["project/selectscript"], infpath, outfpath]
            checkoutput(cmd) # dont't pass cmd as list when shell=True
        return outfpath

    def convertBook(self, bk, outdir, prjdir):
        if self.changes is None:
            if self.asBool('project/usechangesfile'):
                self.changes = self.readChanges(os.path.join(prjdir, 'PrintDraftChanges.txt'))
            else:
                self.changes = []
        printer = self.printer
        self.makelocalChanges(printer, bk)
        customsty = os.path.join(prjdir, 'custom.sty')
        if not os.path.exists(customsty):
            open(customsty, "w").close()
        fbkfm = self.ptsettings['FileNameBookNameForm']
        fprfx = self.ptsettings['FileNamePrePart'] or ""
        fpost = self.ptsettings['FileNamePostPart'] or ""
        bknamefmt = fprfx + fbkfm.replace("MAT","{bkid}").replace("41","{bkcode}") + fpost
        fname = bknamefmt.format(bkid=bk, bkcode=bookcodes.get(bk, 0))
        infpath = os.path.join(prjdir, fname)
        if not self.dict['project/runscriptafter']:
            infpath = self.runConversion(infpath, outdir)
        outfname = os.path.basename(infpath)
        # outfname = fname
        doti = outfname.rfind(".")
        if doti > 0:
            outfname = outfname[:doti] + "-draft" + outfname[doti:]
        outfpath = os.path.join(outdir, outfname)
        with universalopen(infpath) as inf:
            dat = inf.read()
            if self.changes is not None or self.localChanges is not None:
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
        if self.dict['project/runscriptafter']:
            bn = os.path.basename(self.runConversion(outfpath, outdir))
        else:
            bn = os.path.basename(outfpath)

        if '-conv' in bn:
            newname = re.sub("(\-draft\-conv|\-conv\-draft|\-conv)", "-draft", bn)
            copyfile(os.path.join(outdir, bn), os.path.join(outdir, newname))
            os.remove(os.path.join(outdir, bn))
            return newname
        else:
            return bn

    def readChanges(self, fname):
        changes = []
        if not os.path.exists(fname):
            return []
        qreg = r'(?:"((?:[^"\\]|\\.)*?)"|' + r"'((?:[^'\\]|\\.)*?)')"
        with universalopen(fname) as inf:
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
                    regex.compile((m.group(3) or m.group(4)), flags=regex.M), (m.group(5) or m.group(6) or "")))
        if not len(changes):
            return None
        if self.printer is not None and self.printer.get("c_tracing"):
            print("List of PrintDraftChanges:-------------------------------------------------------------")
            report = "\n".join("{} -> {}".format(p[1].pattern, p[2]) for p in changes)
            if getattr(self.printer, "logger", None) is not None:
                self.printer.logger.insert_at_cursor(v)
            else:
                try:
                    print(report)
                except UnicodeEncodeError:
                    print("Unable to print details of PrintDraftChanges.txt")
        return changes

    def makelocalChanges(self, printer, bk):
        self.localChanges = []
        if bk == "GLO" and self.dict['document/filterglossary']:
            self.filterGlossary(printer)
        first = int(self.dict["document/chapfrom"])
        last = int(self.dict["document/chapto"])
        
        # This section handles PARTIAL books (from chapter X to chapter Y)
        if self.asBool("document/ifchaplabels", true="%"):
            clabel = self.dict["document/clabel"]
            clbooks = self.dict["document/clabelbooks"].split()
            # print("Chapter label: '{}' for '{}' with {}".format(clabel, " ".join(clbooks), bk))
            if len(clabel) and (not len(clbooks) or bk in clbooks):
                self.localChanges.append((None, regex.compile(r"(\\c 1)(?=\s*\r?\n|\s)", flags=regex.S), r"\\cl {}\n\1".format(clabel)))
        if not self.asBool("project/multiplebooks"):
            if first > 1:
                self.localChanges.append((None, regex.compile(r"\\c 1 ?\r?\n.+(?=\\c {} ?\r?\n)".format(first), flags=regex.S), ""))
            if last < int(chaps.get(bk)):
                self.localChanges.append((None, regex.compile(r"\\c {} ?\r?\n.+".format(last+1), flags=regex.S), ""))

        # Throw out the known "nonpublishable" markers and their text (if any)
            self.localChanges.append((None, regex.compile(r"\\(usfm|ide|rem|sts|restore|pubinfo) .+?\r?\n", flags=regex.M), ""))

        # If a printout of JUST the book introductions is needed (i.e. no scripture text) then this option is very handy
        if not self.asBool("document/ifmainbodytext"):
            self.localChanges.append((None, regex.compile(r"\\c 1 ?\r?\n.+".format(first), flags=regex.S), ""))

        # Elipsize ranges of MISSING/Empty verses in the text (if 3 or more verses in a row are empty...) 
        if self.asBool("document/elipsizemptyvs"):
            self.localChanges.append((None, regex.compile(r"\\v (\d+)([-,]\d+)? ?\r?\n(\\v (\d+)([-,]\d+)? ?\r?\n){1,}", flags=regex.M), r"\\v \1-\4 {...} "))
            # self.localChanges.append((None, regex.compile(r"(\r?\n\\c \d+ ?)(\r?\n\\v 1)", flags=regex.M), r"\1\r\n\\p \2"))
            self.localChanges.append((None, regex.compile(r" (\\c \d+ ?)(\r?\n\\v 1)", flags=regex.M), r" \r\n\1\r\n\\p \2"))
            # self.localChanges.append((None, regex.compile(r"(\{\.\.\.\}) (\\c \d+ ?)\r?\n\\v", flags=regex.M), r"\1\r\n\2\r\n\\p \\v"))
            self.localChanges.append((None, regex.compile(r"(\\c \d+ ?(\r?\n)+\\p (\r?\n)?\\v [\d-]+ \{\.\.\.\} ?(\r?\n)+)(?=\\c)", flags=regex.M), r"\1\\m {...}\r\n"))

        # Probably need to make this more efficient for multi-book and lengthy glossaries (cache the GLO & changes reqd etc.)
        if self.asBool("notes/glossaryfootnotes"):
            self.makeGlossaryFootnotes(printer, bk)

        # Glossary Word markup: Remove the second half of the \w word|glossary-form\w* and apply chosen glossary markup
        v = self.dict["document/glossarymarkupstyle"]
        gloStyle = self._glossarymarkup.get(v, v)
        self.localChanges.append((None, regex.compile(r"\\w (.+?)(\|.+?)?\\w\*", flags=regex.M), gloStyle))
        
        # Remember to preserve \figs ... \figs for books that can't have PicLists (due to no ch:vs refs in them)
        if self.asBool("document/ifinclfigs") and (self.asBool("document/iffigfrmtext") or bk in self._peripheralBooks):
            # Remove any illustrations which don't have a |p| 'loc' field IF this setting is on
            if self.asBool("document/iffigexclwebapp"):
                self.localChanges.append((None, regex.compile(r'(?i)\\fig ([^|]*\|){3}([aw]+)\|[^\\]*\\fig\*', flags=regex.M), ''))  # USFM2
                self.localChanges.append((None, regex.compile(r'(?i)\\fig [^\\]*\bloc="[aw]+"[^\\]*\\fig\*', flags=regex.M), ''))    # USFM3

            figChangeList = self.figNameChanges(printer, bk)
            if len(figChangeList):
                missingPics = []
                for origfn,tempfn in figChangeList:
                    origfn = re.escape(origfn)
                    if tempfn != "":
                        # print("(?i)(\\fig .*?\|){}(\|.+?\\fig\*)".format(origfn), "-->", tempfn)
                        self.localChanges.append((None, regex.compile(r"(?i)(\\fig .*?\|){}(\|.+?\\fig\*)".format(origfn), \
                                                     flags=regex.M), r"\1{}\2".format(tempfn)))                               #USFM2
                        self.localChanges.append((None, regex.compile(r'(?i)(\\fig .*?src="){}(" .+?\\fig\*)'.format(origfn), \
                                                     flags=regex.M), r"\1{}\2".format(tempfn)))                               #USFM3
                    else:
                        if self.asBool("document/iffigskipmissing"):
                            # print("(?i)(\\fig .*?\|){}(\|.+?\\fig\*)".format(origfn), "--> Skipped!!!!")
                            self.localChanges.append((None, regex.compile(r"(?i)\\fig .*?\|{}\|.+?\\fig\*".format(origfn), flags=regex.M), ""))     #USFM2
                            self.localChanges.append((None, regex.compile(r'(?i)\\fig .*?src=\"{}\" .+?\\fig\*'.format(origfn), flags=regex.M), "")) #USFM3

            if self.asBool("document/iffighiderefs"): # del ch:vs from caption 
                self.localChanges.append((None, regex.compile(r"(\\fig [^\\]+?\|)([0-9:.\-,\u2013\u2014]+?)(\\fig\*)", \
                                          flags=regex.M), r"\1\3"))   # USFM2
                self.localChanges.append((None, regex.compile(r'(\\fig .+?)(ref=\"\d+[:.]\d+([-,\u2013\u2014]\d+)?\")(.*?\\fig\*)', \
                                          flags=regex.M), r"\1\4"))   # USFM3
        else: # Drop ALL Figures
            self.localChanges.append((None, regex.compile(r"\\fig .*?\\fig\*", flags=regex.M), ""))
        
        if self.asBool("document/supressbookintro"): # Drop Introductory matter
            self.localChanges.append((None, regex.compile(r"\\i(s|m|mi|p|pi|li\d?|pq|mq|pr|b|q\d?) .+?\r?\n", flags=regex.M), "")) 

        if self.asBool("document/supressintrooutline"): # Drop ALL Intro Outline matter & Intro Outline References
            # Wondering whether we should restrict this to just the GEN...REV books (as some xtra books only use \ixx markers for content)
            self.localChanges.append((None, regex.compile(r"\\(iot|io\d) [^\\]+", flags=regex.M), ""))
            self.localChanges.append((None, regex.compile(r"\\ior .+?\\ior\*\s?\r?\n", flags=regex.M), ""))

        if self.asBool("document/supresssectheads"): # Drop ALL Section Headings (which also drops the Parallel passage refs now)
            self.localChanges.append((None, regex.compile(r"\\[sr] .+", flags=regex.M), ""))

        if self.asBool("document/supressparallels"): # Drop ALL Parallel Passage References
            self.localChanges.append((None, regex.compile(r"\\r .+", flags=regex.M), ""))

        if self.asBool("notes/ifblendfnxr"):
            xrefCaller = self.dict["notes/blendedxrmkr"]
            # To merge/blend \f and \x together, simply change all (\x to \f) (\xo to \fr) and so on...
            self.localChanges.append((None, regex.compile(r"\\x . ", flags=regex.M), r"\\f {} ".format(xrefCaller)))
            self.localChanges.append((None, regex.compile(r"\\x\* ", flags=regex.M), r"\\f* "))
            self.localChanges.append((None, regex.compile(r"\\xq ", flags=regex.M), r"\\fq "))
            self.localChanges.append((None, regex.compile(r"\\xt ", flags=regex.M), r"\\ft "))

        if self.asBool("document/preventorphans"): # Prevent orphans at end of *any* paragraph [anything that isn't followed by a \v]
            # self.localChanges.append((None, regex.compile(r" ([^\\ ]+?) ([^\\ ]+?\r?\n)(?!\\v)", flags=regex.S), r" \1\u00A0\2"))
            # OLD RegEx: Keep final two words of \q lines together [but doesn't work if there is an \f or \x at the end of the line] 
            self.localChanges.append((None, regex.compile(r"(\\q\d?(\s?\r?\n?\\v)?( \S+)+( (?!\\)[^\\\s]+)) (\S+\s*\n)", \
                                            flags=regex.M), r"\1\u00A0\5"))

        if self.asBool("document/preventwidows"):
            # Push the verse number onto the next line (using NBSP) if there is
            # a short widow word (3 characters or less) at the end of the line
            self.localChanges.append((None, regex.compile(r"(\\v \d+([-,]\d+)? [\w]{1,3}) ", flags=regex.M), r"\1\u00A0")) 

        if self.asBool("document/ch1pagebreak"):
            self.localChanges.append((None, regex.compile(r"(\\c 1 ?\r?\n)", flags=regex.M), r"\pagebreak\r\n\1"))

        if self.asBool("document/glueredupwords"): # keep reduplicated words together
            self.localChanges.append((None, regex.compile(r"(?<=[ ])(\w{3,}) \1(?=[\s,.!?])", flags=regex.M), r"\1\u00A0\1")) 
        
        if self.asBool("notes/addcolon"): # Insert a colon between \fq (or \xq) and following \ft (or \xt)
            self.localChanges.append((None, regex.compile(r"(\\[fx]q .+?):* ?(\\[fx]t)", flags=regex.M), r"\1: \2")) 
        
        if self.asBool("notes/keepbookwithrefs"): # keep Booknames and ch:vs nums together within \xt and \xo 
            self.localChanges.append((regex.compile(r"(\\[xf]t [^\\]+)"), regex.compile(r"(?<!\\[fx][rto]) (\d+[:.]\d+([-,]\d+)?)"), r"\u00A0\1"))
            self.localChanges.append((regex.compile(r"(\\[xf]t [^\\]+)"), regex.compile(r"( .) "), r"\1\u00A0"))

        # keep \xo & \fr refs with whatever follows (i.e the bookname or footnote) so it doesn't break at end of line
        self.localChanges.append((None, regex.compile(r"(\\(xo|fr) (\d+[:.]\d+([-,]\d+)?)) "), r"\1\u00A0"))

        # Paratext marks no-break space as a tilde ~
        self.localChanges.append((None, regex.compile(r"~", flags=regex.M), r"\u00A0")) 

        # Remove the + of embedded markup (xetex handles it)
        self.localChanges.append((None, regex.compile(r"\\\+", flags=regex.M), r"\\"))  
            
        for c in range(1,4): # Remove any \toc lines that we don't want appearing in the Table of Contents
            if not self.asBool("document/usetoc{}".format(c)):
                self.localChanges.append((None, regex.compile(r"(\\toc{} .+)".format(c), flags=regex.M), ""))

        # Insert a rule between end of Introduction and start of body text (didn't work earlier, but might work now)
        # self.localChanges.append((None, regex.compile(r"(\\c\s1\s?\r?\n)", flags=regex.S), r"\\par\\vskip\\baselineskip\\hskip-\\columnshift\\hrule\\vskip 2\\baselineskip\n\1"))

        # Apply any changes specified in snippets
        for k, c in self._snippets.items():
            if self.printer is None:
                v = self.asBool(k)
            else:
                v = self.printer.get(c[0])
                self.dict[k] = "true" if v else "false"
            if v: # if the c_checkbox is true then extend the list with those changes
                if k == "snippets/fancyintro" and bk in self._peripheralBooks: # Only allow fancyIntros for scripture books
                    pass
                else:
                    self.localChanges.extend(c[1].regexes)

        if self.printer is not None and self.printer.get("c_tracing"):
            print("List of Local Changes:----------------------------------------------------------")
            report = "\n".join("{} -> {}".format(p[1].pattern, p[2]) for p in self.localChanges)
            if getattr(printer, "logger", None) is not None:
                printer.logger.insert_at_cursor(v)
            else:
                print(report)
        return self.localChanges

    def figNameChanges(self, printer, bk):
        if printer is None:
            return([])
        figlist = []
        figchngs = []
        prjid = self.dict['project/id']
        prjdir = os.path.join(self.ptsettings.basedir, prjid)
        picdir = os.path.join(self['document/directory'], 'tmpPics').replace("\\","/")
        fname = printer.getBookFilename(bk, prjdir)
        infpath = os.path.join(prjdir, fname)
        extOrder = printer.getExtOrder()
        with universalopen(infpath) as inf:
            dat = inf.read()
            inf.close()
            figlist += re.findall(r"(?i)\\fig .*?\|(.+?\.(?=jpg|tif|png|pdf)...)\|.+?\\fig\*", dat)    # Finds USFM2-styled markup in text:
            figlist += re.findall(r'(?i)\\fig .+src="(.+?\.(?=jpg|tif|png|pdf)...)" .+?\\fig\*', dat)  # Finds USFM3-styled markup in text:
            for f in figlist:
                found = False
                for ext in extOrder:
                    tmpf = self.newBase(f)+"."+ext
                    fname = os.path.join(picdir, tmpf)
                    if os.path.exists(fname):
                        figchngs.append((f,tmpf))
                        found = True
                        break
                if not found:
                    figchngs.append((f,"")) 
        return(figchngs)

    def base(self, fpath):
        return os.path.basename(fpath)[:-4]

    def codeLower(self, fpath):
        cl = re.findall(r"(?i)_?((?=cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib)..\d{5})[abc]?$", self.base(fpath))
        if cl:
            return cl[0].lower()
        else:
            return ""

    def newBase(self, fpath):
        clwr = self.codeLower(fpath)
        if len(clwr):
            return clwr
        else:
            return re.sub('[()&+,. ]', '_', self.base(fpath).lower())

    def generateNestedStyles(self):
        prjid = self.dict['project/id']
        prjdir = os.path.join(self.ptsettings.basedir, prjid)
        nstyfname = os.path.join(prjdir, "PrintDraft", "NestedStyles.sty") # hack to be fixed later
        nstylist = []
        if self.asBool("document/ifomitallverses"):
            nstylist.append("##### Remove all verse numbers\n\\Marker v\n\\TextProperties nonpublishable\n\n")

        if not self.asBool("notes/includefootnotes"):
            nstylist.append("##### Set Footnote Size and Line Spacing\n")
            for m in ['fr', 'fq', 'fk', 'ft', 'f']:
                nstylist.append("\\Marker {}\n\\FontSize {}\n".format(m, self.dict['notes/fnfontsize']))
            nstylist.append("\\LineSpacing {}pt plus 2pt\n".format(self.dict['notes/fnlinespacing']))
            nstylist.append("\\Justification Left\n\n")
        else:
            nstylist.append("##### Remove all footnotes\n\\Marker f\n\\TextProperties nonpublishable\n\n")

        if not self.asBool("notes/includexrefs"):
            nstylist.append("##### Set Cross-reference Size and Line Spacing\n")
            for m in ['xo', 'xq', 'xdc', 'xt', 'x']:
                nstylist.append("\\Marker {}\n\\FontSize {}\n".format(m, self.dict['notes/fnfontsize']))
            nstylist.append("\\LineSpacing {}pt plus 2pt\n".format(self.dict['notes/fnlinespacing']))
            nstylist.append("\\Justification Left\n\n")
        else:
            nstylist.append("##### Remove all cross-references\n\\Marker x\n\\TextProperties nonpublishable\n\n")

        nstylist.append("##### Adjust poetic indents\n")
        m = ["\Marker", "\LeftMargin", "\FirstLineIndent"]
        if self.dict["paper/columns"] == "2": # Double Column layout so use smaller indents
            v = [["q", "0.60", "-0.45"], ["q1", "0.60", "-0.45"], ["q2", "0.60", "-0.225"], 
                 ["q3", "0.60", "-0.112"], ["q4", "0.60", "-0.0"]]
        else: # Single column layout, so use larger (USFM.sty default) indents
            v = [["q", "1.25", "-1.00"], ["q1", "1.25", "-1.00"], ["q2", "1.25", "-0.75"],
                 ["q3", "1.25", "-0.5"], ["q4", "1.25", "-0.25"]]
        r = [list(zip(m, x)) for x in v]
        for mkr in r:
            for l in range(0,3):
                nstylist.append("{} {}\n".format(mkr[l][0],mkr[l][1]))
            nstylist.append("\\Justification left\n\n")

        if True: # need to qualify this (look in USFM for a \cl and if it exists, then don't do this)
            nstylist.append("# The descriptive heading is typically considered VerseText, but then often formatted as a heading.\n")
            nstylist.append("# We need to change the TextType so that Print Draft will handle it correctly beside drop-caps.\n")
            nstylist.append("\\Marker d\n\\TextType Section\n\\SpaceBefore 0\n\n")

        for k, c in self._snippets.items():
            if self.printer is None:
                v = self.asBool(k)
            else:
                v = self.printer.get(c[0])
                self.dict[k] = "true" if v else "false"
            if v: # if the c_checkbox is true then add the stylesheet snippet for that option
                nstylist.append(c[1].styleInfo+"\n")

        if nstylist == []:
            if os.path.exists(nstyfname):
                os.remove(nstyfname)
            return []
        else:
            os.makedirs(os.path.join(prjdir, "PrintDraft"), exist_ok=True)
            with open(nstyfname, "w", encoding="utf-8") as outf:
                outf.write("".join(nstylist))
            return [nstyfname]

    def makeGlossaryFootnotes(self, printer, bk):
        # Glossary entries for the key terms appearing like footnotes
        prjid = self.dict['project/id']
        prjdir = os.path.join(self.ptsettings.basedir, prjid)
        fname = printer.getBookFilename("GLO", prjdir)
        infname = os.path.join(prjdir, fname)
        if os.path.exists(infname):
            with universalopen(infname, rewrite=True) as inf:
                dat = inf.read()
                ge = re.findall(r"\\p \\k (.+)\\k\* (.+)\r?\n", dat) # Finds all glossary entries in GLO book
                if ge is not None:
                    for g in ge:
                        gdefn = regex.sub(r"\\xt (.+)\\xt\*", r"\1", g[1])
                        self.localChanges.append((None, regex.compile(r"(\\w (.+\|)?{} ?\\w\*)".format(g[0]), flags=regex.M), \
                                                                     r"\1\\f + \\fq {}: \\ft {}\\f* ".format(g[0],gdefn)))

    def filterGlossary(self, printer):
        # Only keep entries that have appeared in this collection of books
        glossentries = []
        prjid = self.dict['project/id']
        prjdir = os.path.join(self.ptsettings.basedir, prjid)
        for bk in printer.getBooks():
            if bk not in TexModel._peripheralBooks:
                fname = printer.getBookFilename(bk, prjid)
                fpath = os.path.join(prjdir, fname)
                if os.path.exists(fpath):
                    with universalopen(fpath) as inf:
                        sfmtxt = inf.read()
                    glossentries += re.findall(r"\\w .*?\|?([^\|]+?)\\w\*", sfmtxt)
        fname = printer.getBookFilename("GLO", prjdir)
        infname = os.path.join(prjdir, fname)
        if os.path.exists(infname):
            with universalopen(infname, rewrite=True) as inf:
                dat = inf.read()
                ge = re.findall(r"\\p \\k (.+)\\k\* .+\r?\n", dat) # Finds all glossary entries in GLO book
        for delGloEntry in [x for x in ge if x not in list(set(glossentries))]:
            self.localChanges.append((None, regex.compile(r"\\p \\k {}\\k\* .+\r?\n".format(delGloEntry), flags=regex.M), ""))

