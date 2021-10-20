import configparser, re, os, gi, traceback
from shutil import copyfile
from pathlib import Path
from functools import reduce
from inspect import signature
import regex
from ptxprint.font import TTFont
from ptxprint.runner import checkoutput
from ptxprint import sfm
from ptxprint.sfm import usfm, style, Text
from ptxprint.usfmutils import Usfm, Sheets, isScriptureText, Module
from ptxprint.utils import _, universalopen, localhdrmappings, pluralstr, multstr, coltoonemax, \
                            chaps, books, bookcodes, allbooks, oneChbooks, asfloat, f2s, cachedData
from ptxprint.dimension import Dimension
import ptxprint.scriptsnippets as scriptsnippets
from ptxprint.interlinear import Interlinear
from ptxprint.reference import Reference, RefRange, RefList, RefSeparators, AnyBooks
import logging

logger = logging.getLogger(__name__)

# After universalopen to resolve circular import. Kludge
from ptxprint.snippets import FancyIntro, PDFx1aOutput, Diglot, FancyBorders, ThumbTabs, Colophon, Grid

def loosint(x):
    try:
        return int(x)
    except (ValueError, TypeError):
        return 0

ModelMap = {
    "L_":                       ("c_diglot", lambda w,v: "L" if v else ""),
    "R_":                       ("c_diglot", lambda w,v: "R" if v else ""),
    "date_":                    ("_date", None),
    "pdfdate_":                 ("_pdfdate", None),
    "xmpdate_":                 ("_xmpdate", None),
    "ifusediglotcustomsty_":    ("_diglotcustomsty", lambda w,v: "%" if not v else ""),
    "ifusediglotmodsty_":       ("_diglotmodsty", lambda w,v: "%" if not v else ""),
    "ifdiglotincludefootnotes_":("_diglotinclfn", lambda w,v: "%" if not v else ""),
    "ifdiglotincludexrefs_":    ("_diglotinclxr", lambda w,v: "%" if not v else ""),
    "transparency_":            ("fcb_outputFormat", lambda w,v: "false" if v in (None, "None", "PDF/X-4") else "true"),

    "config/notes":             ("t_configNotes", lambda w,v: v or ""),
    "config/pwd":               ("t_invisiblePassword", lambda w,v: v or ""),
    "config/version":           ("_version", None),

    # "project/hideadvsettings":  ("c_showAdvancedOptions", lambda w,v: not v),
    "project/bookscope":        ("r_book", None),
    "project/uilevel":          ("fcb_uiLevel", None),
    "project/book":             ("ecb_book", None),
    "project/modulefile":       ("btn_chooseBibleModule", lambda w,v: v.replace("\\","/") if v is not None else ""),
    "project/booklist":         ("ecb_booklist", lambda w,v: v or ""),
    "project/ifinclfrontpdf":   ("c_inclFrontMatter", None),
    "project/frontincludes":    ("btn_selectFrontPDFs", lambda w,v: "\n".join('\\includepdf{{{}}}'.format(s.as_posix()) \
                                 for s in w.FrontPDFs) if (w.get("c_inclFrontMatter") and w.FrontPDFs is not None
                                                                                      and w.FrontPDFs != 'None') else ""),
    "project/ifinclbackpdf":    ("c_inclBackMatter", None),
    "project/backincludes":     ("btn_selectBackPDFs", lambda w,v: "\n".join('\\includepdf{{{}}}'.format(s.as_posix()) \
                                 for s in w.BackPDFs) if (w.get("c_inclBackMatter") and w.BackPDFs is not None
                                                                                    and w.BackPDFs != 'None') else ""),
    "project/processscript":    ("c_processScript", None),
    "project/runscriptafter":   ("c_processScriptAfter", None),
    "project/selectscript":     ("btn_selectScript", lambda w,v: w.customScript.as_posix() if w.customScript is not None else ""),
    "project/selectxrfile":     ("btn_selectXrFile", None),
    "project/usechangesfile":   ("c_usePrintDraftChanges", lambda w,v :"true" if v else "false"),
    "project/ifusemodstex":     ("c_useModsTex", lambda w,v: "" if v else "%"),
    "project/ifusepremodstex":  ("c_usePreModsTex", lambda w,v: "" if v else "%"),
    "project/ifusecustomsty":   ("c_useCustomSty", lambda w,v: "" if v else "%"),
    "project/ifusemodssty":     ("c_useModsSty", lambda w,v: "" if v else "%"),
    "project/ifstarthalfpage":  ("c_startOnHalfPage", lambda w,v :"true" if v else "false"),
    "project/randompicposn":    ("c_randomPicPosn", None),
    "project/canonicalise":     ("c_canonicalise", None),
    "project/interlinear":      ("c_interlinear", lambda w,v: "" if v else "%"),
    "project/interlang":        ("t_interlinearLang", None),
    "project/ruby":             ("c_ruby", lambda w,v : "t" if v else "b"),
    "project/license":          ("ecb_licenseText", None),
    "project/copyright":        ("t_copyrightStatement", lambda w,v: re.sub(r"\\u([0-9a-fA-F]{4})",
                                                                   lambda m: chr(int(m.group(1), 16)), v) if v is not None else ""),
    "project/iffrontmatter":    ("c_frontmatter", lambda w,v: "" if v else "%"),
    "project/periphpagebreak":  ("c_periphPageBreak", None),
    "project/colophontext":     ("txbf_colophon", lambda w,v: re.sub(r"\\u([0-9a-fA-F]{4})",
                                                                   lambda m: chr(int(m.group(1), 16)), v) if v is not None else ""),
    "project/ifcolophon":       ("c_colophon", lambda w,v: "" if v else "%"),
    "project/pgbreakcolophon":  ("c_standAloneColophon", lambda w,v: "" if v else "%"),

    "paper/height":             ("ecb_pagesize", lambda w,v: re.sub(r"^.*?[,xX]\s*(.+?)\s*(?:\(.*|$)", r"\1", v or "210mm")),
    "paper/width":              ("ecb_pagesize", lambda w,v: re.sub(r"^(.*?)\s*[,xX].*$", r"\1", v or "148mm")),
    "paper/pagesize":           ("ecb_pagesize", None),
    "paper/ifwatermark":        ("c_applyWatermark", lambda w,v: "" if v else "%"),
    "paper/watermarkpdf":       ("btn_selectWatermarkPDF", lambda w,v: w.watermarks.as_posix() \
                                 if (w.get("c_applyWatermark") and w.watermarks is not None and w.watermarks != 'None') else ""),
    "paper/ifcropmarks":        ("c_cropmarks", lambda w,v :"true" if v else "false"),  
    "paper/ifgrid":             ("c_grid", lambda w,v :"" if v else "%"),
    "paper/ifverticalrule":     ("c_verticalrule", lambda w,v :"true" if v else "false"),
    "paper/margins":            ("s_margins", lambda w,v: round(float(v)) if v else "12"),
    "paper/topmargin":          ("s_topmargin", None),
    "paper/bottommargin":       ("s_bottommargin", None),
    "paper/headerpos":          ("s_headerposition", None),
    "paper/footerpos":          ("s_footerposition", None),
    "paper/rulegap":            ("s_rhruleposition", None),

    "paper/ifaddgutter":        ("c_pagegutter", lambda w,v :"true" if v else "false"),
    "paper/gutter":             ("s_pagegutter", lambda w,v: round(float(v)) if v else "0"),
    "paper/colgutteroffset":    ("s_colgutteroffset", lambda w,v: "{:.1f}".format(float(v)) if v else "0.0"),
    "paper/columns":            ("c_doublecolumn", lambda w,v: "2" if v else "1"),
    "paper/bottomrag":          ("s_bottomRag", lambda w,v: str(int(v or 0)+0.95)),
    "paper/fontfactor":         ("s_fontsize", lambda w,v: f2s(float(v) / 12, dp=8) if v else "1.000"),

    "grid/gridlines":           ("c_gridLines", lambda w,v: "\doGridLines" if v else ""),
    "grid/gridgraph":           ("c_gridGraph", lambda w,v: "\doGraphPaper" if v else ""),
    "grid/majorcolor":          ("col_gridMajor", None),
    "majorcolor_":              ("col_gridMajor", lambda w,v: "{:.2f} {:.2f} {:.2f}".format(*coltoonemax(v)) if v else "0.8 0.8 0.8"),
    "grid/minorcolor":          ("col_gridMinor", None),
    "minorcolor_":              ("col_gridMinor", lambda w,v: "{:.2f} {:.2f} {:.2f}".format(*coltoonemax(v)) if v else "0.8 1.0 1.0"),
    "grid/majorthickness":      ("s_gridMajorThick", None),
    "grid/minorthickness":      ("s_gridMinorThick", None),
    "grid/units":               ("fcb_gridUnits", None),
    "grid/divisions":           ("s_gridMinorDivisions", lambda w,v: int(float(v)) if v else "10"),
    "grid/xyadvance":           ("s_gridMinorDivisions", lambda w,v: (1 / max(asfloat(v, 4), 1)) if v else "0.25"),
    "grid/xyoffset":            ("fcb_gridOffset", None),
    
    "fancy/enableborders":      ("c_borders", lambda w,v: "" if v else "%"),
    "fancy/pageborder":         ("c_inclPageBorder", lambda w,v: "" if v else "%"),
    "fancy/pageborderfullpage": ("c_borderPageWide", lambda w,v: "" if v else "%"),
    "fancy/pagebordernfullpage_": ("c_borderPageWide", lambda w,v: "%" if v else ""),
    "fancy/pageborderpdf":      ("btn_selectPageBorderPDF", lambda w,v: w.pageborder.as_posix() \
                                            if (w.pageborder is not None and w.pageborder != 'None') \
                                            else get("/ptxprintlibpath")+"/A5 page border.pdf"),
    "fancy/sectionheader":      ("c_inclSectionHeader", lambda w,v: "" if v else "%"),
    "fancy/sectionheaderpdf":   ("btn_selectSectionHeaderPDF", lambda w,v: w.sectionheader.as_posix() \
                                            if (w.sectionheader is not None and w.sectionheader != 'None') \
                                            else get("/ptxprintlibpath")+"/A5 section head border.pdf"),
    "fancy/sectionheadershift": ("s_inclSectionShift", lambda w,v: float(v or "0")),
    "fancy/sectionheaderscale": ("s_inclSectionScale", lambda w,v: int(float(v or "1.0")*1000)),
    "fancy/endofbook":          ("c_inclEndOfBook", lambda w,v: "" if v else "%"),
    "fancy/endofbookpdf":       ("btn_selectEndOfBookPDF", lambda w,v: w.endofbook.as_posix() \
                                            if (w.endofbook is not None and w.endofbook != 'None') \
                                            else get("/ptxprintlibpath")+"/decoration.pdf"),
    "fancy/versedecorator":     ("c_inclVerseDecorator", lambda w,v: "" if v else "%"),
    "fancy/versedecoratortype": ("r_decorator", None),
    "fancy/versedecoratorpdf":  ("btn_selectVerseDecorator", lambda w,v: w.versedecorator.as_posix() \
                                            if (w.versedecorator is not None and w.versedecorator != 'None') \
                                            else get("/ptxprintlibpath")+"/Verse number star.pdf"),
    "fancy/versedecoratorshift":   ("s_verseDecoratorShift", lambda w,v: float(v or "0")),
    "fancy/versedecoratorscale":   ("s_verseDecoratorScale", lambda w,v: int(float(v or "1.0")*1000)),
    "fancy/endayah":            ("c_decorator_endayah", lambda w,v: "" if v else "%"), # In the UI this is "Move Ayah"

    "paragraph/linespacing":       ("s_linespacing", lambda w,v: f2s(float(v), dp=8) if v else "15"),
    "paragraph/linespacebase":  ("c_AdvCompatLineSpacing", lambda w,v: 14 if v else 12),
    "paragraph/useglyphmetrics":   ("c_AdvCompatGlyphMetrics", lambda w,v: "%" if v else ""),
    "paragraph/ifjustify":      ("c_justify", lambda w,v: "true" if v else "false"),
    "paragraph/ifhyphenate":    ("c_hyphenate", lambda w,v: "" if v else "%"),
    "paragraph/ifomithyphen":   ("c_omitHyphen", lambda w,v: "" if v else "%"),
    "paragraph/ifnothyphenate": ("c_hyphenate", lambda w,v: "%" if v else ""),
    "paragraph/ifusefallback":  ("c_useFallbackFont", None),
    "paragraph/missingchars":   ("t_missingChars", lambda w,v: v or ""),

    "document/sensitive":       ("c_sensitive", None),
    "document/title":           (None, lambda w,v: "" if w.get("c_sensitive") else w.ptsettings.get('FullName', "")),
    "document/subject":         ("ecb_booklist", lambda w,v: v if w.get("r_book") == "multiple" else w.get("ecb_book")),
    "document/author":          (None, lambda w,v: "" if w.get("c_sensitive") else w.ptsettings.get('Copyright', "")),

    "document/startpagenum":    ("s_startPageNum", lambda w,v: int(float(v)) if v else "1"),
    "document/multibook":       ("r_book_multiple", lambda w,v: "" if v else "%"),
    "document/toc":             ("c_autoToC", lambda w,v: "" if v else "%"),
    "document/toctitle":        ("t_tocTitle", lambda w,v: v or ""),
    "document/usetoc1":         ("c_usetoc1", lambda w,v: "true" if v else "false"),
    "document/usetoc2":         ("c_usetoc2", lambda w,v: "true" if v else "false"),
    "document/usetoc3":         ("c_usetoc3", lambda w,v: "true" if v else "false"),
    "document/tocleaders":      ("fcb_leaderStyle", None),
    "document/chapfrom":        ("s_chapfrom", lambda w,v: int(float(v)) if v else "1"),
    "document/chapto":          ("s_chapto", lambda w,v: int(float(v)) if v else "999"),
    "document/colgutterfactor": ("s_colgutterfactor", lambda w,v: round(float(v or 4)*3)), # Hack to be fixed
    "document/ifrtl":           ("fcb_textDirection", lambda w,v:"true" if v == "rtl" else "false"),
    "document/toptobottom":     ("fcb_textDirection", lambda w,v: "" if v == "ttb" else "%"),
    "document/iflinebreakon":   ("c_linebreakon", lambda w,v: "" if v else "%"),
    "document/linebreaklocale": ("t_linebreaklocale", lambda w,v: v or ""),
    "document/script":          ("fcb_script", lambda w,v: ":script="+v.lower() if v and v != "Zyyy" else ""),
    "document/ch1pagebreak":    ("c_ch1pagebreak", None),
    "document/marginalverses":  ("c_marginalverses", lambda w,v: "" if v else "%"),
    "document/columnshift":     ("s_columnShift", lambda w,v: v or "16"),
    "document/ifshowchapternums": ("c_chapterNumber", lambda w,v: "%" if v else ""),
    "document/showxtrachapnums":  ("c_showNonScriptureChapters", None),
    "document/ifshow1chbooknum": ("c_show1chBookNum", None),
    "document/ifomitverseone":  ("c_omitverseone", lambda w,v: "true" if v else "false"),
    "document/ifshowversenums":   ("c_verseNumbers", lambda w,v: "%" if v else ""),
    "document/ifmainbodytext":  ("c_mainBodyText", None),
    "document/glueredupwords":  ("c_glueredupwords", None),
    "document/ifinclfigs":      ("c_includeillustrations", lambda w,v: "true" if v else "false"),
    "document/ifusepiclist":    ("c_includeillustrations", lambda w,v :"" if v else "%"),
    "document/iffigexclwebapp": ("c_figexclwebapp", None),
    "document/iffigskipmissing": ("c_skipmissingimages", None),
    "document/iffigcrop":       ("c_cropborders", None),
    "document/iffigplaceholders": ("c_figplaceholders", lambda w,v: "true" if v else "false"),
    "document/iffigshowcaptions": ("c_fighidecaptions", lambda w,v: "false" if v else "true"),
    "document/iffighiderefs":   ("c_fighiderefs", None),
    "document/picresolution":   ("r_pictureRes", None),
    "document/customfiglocn":   ("c_useCustomFolder", lambda w,v :"" if v else "%"),
    "document/exclusivefolder": ("c_exclusiveFiguresFolder", None),
    "document/customfigfolder": ("btn_selectFigureFolder", lambda w,v: w.customFigFolder.as_posix() \
                                                                       if w.customFigFolder is not None else ""),
    "document/imagetypepref":   ("t_imageTypeOrder", None),
    "document/glossarymarkupstyle":  ("fcb_glossaryMarkupStyle", None),
    "document/filterglossary":  ("c_filterGlossary", None),
    "document/hangpoetry":      ("c_hangpoetry", lambda w,v: "" if v else "%"),
    "document/preventorphans":  ("c_preventorphans", None),
    "document/preventwidows":   ("c_preventwidows", None),
    "document/sectionheads":    ("c_sectionHeads", None),
    "document/parallelrefs":    ("c_parallelRefs", None),
    "document/bookintro":       ("c_bookIntro", None),
    "document/introoutline":    ("c_introOutline", None),
    "document/indentunit":      ("s_indentUnit", lambda w,v: round(float(v or "1.0"), 1)),
    "document/firstparaindent": ("c_firstParaIndent", lambda w,v: "true" if v else "false"),
    "document/ifhidehboxerrors": ("c_showHboxErrorBars", lambda w,v :"%" if v else ""),
    "document/hidemptyverses":  ("c_hideEmptyVerses", None),
    "document/elipsizemptyvs":  ("c_elipsizeMissingVerses", None),
    "document/ifspacing":       ("c_spacing", lambda w,v :"" if v else "%"),
    "document/spacestretch":    ("s_maxSpace", lambda w,v : str((int(float(v or 150)) - 100) / 100.)),
    "document/spaceshrink":     ("s_minSpace", lambda w,v : str((100 - int(float(v or 66))) / 100.)),
    "document/ifletter":        ("c_letterSpacing", lambda w,v: "" if v else "%"),
    "document/letterstretch":   ("s_letterStretch", lambda w,v: float(v or "5.0") / 100.),
    "document/lettershrink":    ("s_letterShrink", lambda w,v: float(v or "1.0") / 100.),
    "document/ifcolorfonts":    ("c_colorfonts", lambda w,v: "%" if v else ""),

    "document/ifchaplabels":    ("c_useChapterLabel", lambda w,v: "%" if v else ""),
    "document/clabelbooks":     ("t_clBookList", lambda w,v: v.upper() if v else ""),
    "document/clabel":          ("t_clHeading", None),
    "document/clsinglecol":     ("c_singleColLayout", None),
    "document/clsinglecolbooks":    ("t_singleColBookList", None),
    "document/cloptimizepoetry":    ("c_optimizePoetryLayout", None),

    "document/ifdiglot":            ("c_diglot", lambda w,v : "" if v else "%"),
    "document/diglotprifraction":   ("s_diglotPriFraction", lambda w,v : round((float(v)/100), 3) if v is not None else "0.550"),
    "document/diglotsecfraction":   ("s_diglotPriFraction", lambda w,v : round(1 - (float(v)/100), 3) if v is not None else "0.450"),
    "document/diglotsecprj":    ("fcb_diglotSecProject", None),
    "document/diglotpicsources":    ("fcb_diglotPicListSources", None),
    "document/diglot2captions": ("c_diglot2captions", None),
    "document/diglotswapside":  ("c_diglotSwapSide", lambda w,v: "true" if v else "false"),
    "document/diglotsepnotes":  ("c_diglotSeparateNotes", lambda w,v: "true" if v else "false"),
    "document/diglotsecconfig": ("ecb_diglotSecConfig", None),
    "document/diglotmergemode": ("c_diglotMerge", lambda w,v: "simple" if v else "doc"),
    "document/diglotadjcenter": ("c_diglotAdjCenter", None),
    "document/diglotnotesrule": ("c_diglotNotesRule", lambda w,v: "true" if v else "false"),
    "document/diglotjoinvrule": ("c_diglotJoinVrule", lambda w,v: "true" if v else "false"),

    "document/hasnofront_":     ("c_frontmatter", lambda w,v: "%" if v else ""),

    "header/ifshowbook":        ("c_rangeShowBook", lambda w,v :"false" if v else "true"),
    "header/ifshowchapter":     ("c_rangeShowChapter", lambda w,v :"false" if v else "true"),
    "header/ifshowverse":       ("c_rangeShowVerse", lambda w,v :"true" if v else "false"),
    "header/chvseparator":      ("c_sepColon", lambda w,v : ":" if v else "."),
    "header/ifrhrule":          ("c_rhrule", lambda w,v: "" if v else "%"),
    "header/hdrleftside":       ("r_hdrLeft", None),
    "header/hdrleft":           ("ecb_hdrleft", lambda w,v: v or "-empty-"),
    "header/hdrcenterside":     ("r_hdrCenter", None),
    "header/hdrcenter":         ("ecb_hdrcenter", lambda w,v: v or "-empty-"),
    "header/hdrrightside":      ("r_hdrRight", None),
    "header/hdrright":          ("ecb_hdrright", lambda w,v: v or "-empty-"),
    "header/mirrorlayout":      ("c_mirrorpages", lambda w,v: "true" if v else "false"),
    
    "footer/ftrcenterside":     ("r_ftrCenter", None),
    "footer/ftrcenter":         ("ecb_ftrcenter", lambda w,v: v or "-empty-"),
    "footer/ifftrtitlepagenum": ("c_pageNumTitlePage", lambda w,v: "" if v else "%"),
    "footer/ifprintconfigname": ("c_printConfigName", lambda w,v: "" if v else "%"),
    # "footer/noinkinfooter":     ("c_noInkFooter", None),

    "notes/includefootnotes":   ("c_includeFootnotes", lambda w,v: "%" if v else ""),
    "notes/fneachnewline":      ("c_fneachnewline", lambda w,v: "%" if v else ""),
    "notes/fnoverride":         ("c_fnOverride", None),
    "notes/iffnautocallers":    ("c_fnautocallers", lambda w,v :"true" if v else "false"),
    "notes/fncallers":          ("t_fncallers", lambda w,v: v if w.get("c_fnautocallers") else ""),
    "notes/fnresetcallers":     ("c_fnpageresetcallers", lambda w,v: "" if v else "%"),
    "notes/fnomitcaller":       ("c_fnomitcaller", lambda w,v: "%" if v else ""),

    "notes/includexrefs":       ("c_includeXrefs", lambda w,v: "%" if v else ""),
    "notes/xreachnewline":      ("c_xreachnewline", lambda w,v: "%" if v else ""),
    "notes/xroverride":         ("c_xrOverride", None),
    "notes/ifxrautocallers":    ("c_xrautocallers", lambda w,v :"true" if v else "false"),
    "notes/xrcallers":          ("t_xrcallers", lambda w,v: v if w.get("c_xrautocallers") else ""),
    "notes/xrresetcallers":     ("c_xrpageresetcallers", lambda w,v: "" if v else "%"),
    "notes/xromitcaller":       ("c_xromitcaller", lambda w,v: "%" if v else ""),

    "notes/xrlocation":         ("r_xrpos", lambda w,v: r"" if v == "centre" else "%"),
    "notes/xrpos":              ("r_xrpos", None),
    "notes/xrcolside":          ("fcb_colXRside", None),
    "notes/xrcentrecolwidth":   ("s_centreColWidth", lambda w,v: int(float(v)) if v else "60"),
    "notes/xrguttermargin":     ("s_xrGutterWidth", lambda w,v: "{:.1f}".format(float(v)) if v else "2.0"),
    "notes/xrcolrule":          ("c_xrColumnRule", lambda w,v: "true" if v else "false"),
    "notes/xrcolbottom":        ("c_xrColumnBottom", lambda w,v: "true" if v else "false"),
    "notes/ifxrexternalist":    ("c_useXrefList", lambda w,v: "%" if v else ""),
    "notes/xrlistsource":       ("r_xrSource", None),
    "notes/xrlistsize":         ("s_xrSourceSize", lambda w,v: int(float(v)) if v else "3"),
    "notes/xrfilterbooks":      ("fcb_filterXrefs", None),
    "notes/addcolon":           ("c_addColon", None),
    "notes/keepbookwithrefs":   ("c_keepBookWithRefs", None),
    "notes/glossaryfootnotes":  ("c_glossaryFootnotes", None),
    "notes/fnpos":              ("r_fnpos", None),
    "notes/columnnotes_":       ("r_fnpos", lambda w,v: "true" if v == "column" else "false"),
    "notes/endnotes_":          ("r_fnpos", lambda w,v: "" if v == "endnotes" else "%"),

    "notes/iffootnoterule":     ("c_footnoterule", lambda w,v: "%" if v else ""),
    "notes/ifxrefrule":         ("c_xrefrule", lambda w,v: "%" if v else ""),

    "notes/abovenotespace":     ("s_fnAboveSpace", None),
    "notes/belownoterulespace": ("s_fnBelowSpace", None),
    "notes/fnruleposn":         ("fcb_fnHorizPosn", None),
    "notes/fnruleindent":       ("s_fnIndent", None),
    "notes/fnrulelength":       ("s_fnLength", None),
    "notes/fnrulethick":        ("s_fnThick", None),
    
    "notes/abovexrefspace":     ("s_xrAboveSpace", None),
    "notes/belowxrefrulespace": ("s_xrBelowSpace", None),
    "notes/xrruleposn":         ("fcb_xrHorizPosn", None),
    "notes/xrruleindent":       ("s_xrIndent", None),
    "notes/xrrulelength":       ("s_xrLength", None),
    "notes/xrrulethick":        ("s_xrThick", None),
    
    "notes/internotespace":     ("s_internote", lambda w,v: f2s(float(v or 3))),

    "notes/horiznotespacemin":  ("s_notespacingmin", lambda w,v: f2s(float(v)) if v is not None else "7"),
    "notes/horiznotespacemax":  ("s_notespacingmax", lambda w,v: f2s(float(v)) if v is not None else "27"),

    "document/fontregular":              ("bl_fontR", lambda w,v,s: v.asTeXFont(s.inArchive) if v else ""),
    "document/fontbold":                 ("bl_fontB", lambda w,v,s: v.asTeXFont(s.inArchive) if v else ""),
    "document/fontitalic":               ("bl_fontI", lambda w,v,s: v.asTeXFont(s.inArchive) if v else ""),
    "document/fontbolditalic":           ("bl_fontBI", lambda w,v,s: v.asTeXFont(s.inArchive) if v else ""),
    "document/fontextraregular":         ("bl_fontExtraR", lambda w,v,s: v.asTeXFont(s.inArchive) if v else ""),
    "snippets/fancyintro":      ("c_prettyIntroOutline", None),
    "snippets/pdfoutput":       ("fcb_outputFormat", None),
    "snippets/diglot":          ("c_diglot", lambda w,v: True if v else False),
    "snippets/fancyborders":    ("c_borders", None),
    "document/includeimg":      ("c_includeillustrations", None),
    "thumbtabs/ifthumbtabs":    ("c_thumbtabs", None),
    "thumbtabs/numtabs":        ("s_thumbtabs", None),
    "thumbtabs/length":         ("s_thumblength", None),
    "thumbtabs/height":         ("s_thumbheight", None),
    "thumbtabs/background":     ("col_thumbback", None),
    "thumbtabs/rotate":         ("c_thumbrotate", None),
    "thumbtabs/rotatetype":     ("fcb_rotateTabs", None),
    "thumbtabs/thumbiszthumb":  ("c_thumbIsZthumb", None),
    "thumbtabs/restart":        ("c_thumbrestart", None),
    "thumbtabs/groups":         ("t_thumbgroups", None),

    "scripts/mymr/syllables":   ("c_scrmymrSyllable", None),
}

Borders = {'c_inclPageBorder':      ('pageborder', 'fancy/pageborderpdf', 'A5 page border.pdf'),
           'c_inclSectionHeader':   ('sectionheader', 'fancy/sectionheaderpdf', 'A5 section head border.pdf'),
           'c_inclEndOfBook':       ('endofbook', 'fancy/endofbookpdf', 'decoration.pdf'),
           'c_inclVerseDecorator':  ('versedecorator', 'fancy/versedecoratorpdf', 'Verse number star.pdf'),
           'c_inclFrontMatter':     ('FrontPDFs', 'project/frontincludes', '\\includepdf{{{}}}'),
           'c_inclBackMatter':      ('BackPDFs', 'project/backincludes', '\\includepdf{{{}}}'),
           'c_applyWatermark':      ('watermarks', 'paper/watermarkpdf', r'\def\MergePDF{{"{}"}}')
}


class TexModel:
    _peripheralBooks = ["FRT", "INT", "GLO", "TDX", "NDX", "CNC", "OTH", "BAK", "XXA", "XXB", "XXC", "XXD", "XXE", "XXF", "XXG"]
    _fonts = {
        "fontregular":              ("bl_fontR", None, None, None, None),
        "fontbold":                 ("bl_fontB", None, "c_fakebold", "fontbold/embolden", "fontbold/slant"),
        "fontitalic":               ("bl_fontI", None, "c_fakeitalic", "fontitalic/embolden", "fontitalic/slant"),
        "fontbolditalic":           ("bl_fontBI", None, "c_fakebolditalic", "fontbolditalic/embolden", "fontbolditalic/slant"),
        "fontextraregular":         ("bl_fontExtraR", "c_useFallbackFont", None, None, None),
    }
    _mirrorRL = {r'\lastref':    r'\firstref',
                 r'\firstref':   r'\lastref'
    }
    _swapRL = {'left':   'right',
               'center': 'center',
               'right':  'left'
    }
    _glossarymarkup = {
        "no": r"\1",                # "None":                    
        None: r"\1",                # None:                      
        "bd": r"\\bd \1\\bd*",      # "format as bold":          
        "it": r"\\it \1\\it*",      # "format as italics":       
        "bi": r"\\bdit \1\\bdit*",  # "format as bold italics":  
        "em": r"\\em \1\\em*",      # "format with emphasis":    
        "fb": r"\u2E24\1\u2E25",    # "with ⸤floor⸥ brackets":   
        "fc": r"\u230a\1\u230b",    # "with ⌊floor⌋ characters": 
        "cc": r"\u231e\1\u231f",    # "with ⌞corner⌟ characters":
        "sb": r"*\1",               # "star *before word":       
        "sa": r"\1*",               # "star after* word":        
        "cb": r"^\1",               # "circumflex ^before word": 
        "ca":  r"\1^",              # "circumflex after^ word":  
        "ww":  r"\\w \1\\w*"        # "\w ...\w* char style":  
    }
    _snippets = {
        "snippets/fancyintro":            ("c_prettyIntroOutline", None, FancyIntro),
        "snippets/pdfoutput":             ("fcb_outputFormat", lambda x: True, PDFx1aOutput),
        "snippets/diglot":                ("c_diglot", None, Diglot),
        "snippets/fancyborders":          ("c_borders", None, FancyBorders),
        "snippets/thumbtabs":             ("c_thumbtabs", None, ThumbTabs),
        "snippets/colophon":              ("c_colophon", None, Colophon),
        "snippets/grid":                  ("c_grid", None, Grid)
    }
    _settingmappings = {
        "notes/xrcallers": "crossrefs",
        "notes/fncallers": "footnotes"
    }
    _crossRefInfo = None

    _periphids = {
        "title page": "title",
        "half title page": "halftitle",
        "promotional page": "promo",
        "imprimatur": "imprimatur",
        "publication data": "pubdata",
        "foreword": "foreword",
        "preface": "preface",
        "table of contents": "contents",
        "alphabetical contents": "alphacontents",
        "table of abbreviations": "abbreviations",
        "bible introduction": "intbible",
        "old testament introduction": "intot",
        "pentateuch introduction": "intpent",
        "history introduction": "inthistory",
        "poetry introduction": "intpoetry",
        "prophecy introduction": "intprophesy",
        "deuterocanon introduction": "intdc",
        "new testament introduction": "intnt",
        "gospels introduction": "intgospels",
        "epistles introduction": "intepistles",
        "letters introduction": "intletters",
        "chronology": "chron",
        "weights and measures": "measures",
        "map index": "maps",
        "lxx quotes in nt": "lxxquotes",
        "cover": "cover",
        "spine": "spine"
    }

    _tocleaders = [
        "",
        r"\hskip .5pt .\hskip .5pt",
        r"\hskip 3pt .\hskip 3pt",
        r"\hskip 6pt \emdash\hskip 3pt",
        r"\hrule"
    ]

    def __init__(self, printer, path, ptsettings, prjid=None, inArchive=False):
        from ptxprint.view import VersionStr
        self.VersionStr = VersionStr
        self.printer = printer
        self.ptsettings = ptsettings
        self.inArchive = inArchive
        self.changes = None
        self.localChanges = None
        self.debug = False
        self.interlinear = None
        self.imageCopyrightLangs = {}
        self.frontperiphs = None
        libpath = os.path.abspath(os.path.dirname(__file__))
        self.dict = {"/ptxpath": str(path).replace("\\","/"),
                     "/ptxprintlibpath": libpath.replace("\\","/"),
                     "/iccfpath": os.path.join(libpath, "default_cmyk.icc").replace("\\","/"),
                     "/ptx2pdf": self.printer.scriptsdir.replace("\\", "/")}
        self.prjid = prjid
        if self.prjid is not None:
            self.dict['project/id'] = self.prjid
        self._hdrmappings = localhdrmappings()
        if self.printer is not None:
            self.sheets = Sheets(self.printer.getStyleSheets(generated=True))
            self.update()

    def docdir(self):
        if self.asBool("project/useprintdraftfolder"):
            base = os.path.join(self.dict["/ptxpath"], self.dict["project/id"])
            docdir = os.path.join(base, 'local', 'ptxprint', self.printer.configName())
        else:
            base = self.printer.working_dir
            docdir = base
        return docdir, base

    def update(self):
        """ Update model from UI """
        j = os.path.join
        rel = lambda x, y:os.path.relpath(x, y).replace("\\", "/")
        self.printer.setDate()  # Update date/time to now
        cpath = self.printer.configPath(self.printer.configName())
        rcpath = self.printer.configPath("")
        self.updatefields(ModelMap.keys())
        docdir, base = self.docdir()
        self.dict["document/directory"] = "." # os.path.abspath(docdir).replace("\\","/")
        self.dict['project/adjlists'] = rel(j(cpath, "AdjLists"), docdir).replace("\\","/") + "/"
        self.dict['project/triggers'] = rel(j(cpath, "triggers"), docdir).replace("\\","/") + "/"
        self.dict['project/piclists'] = rel(j(self.printer.working_dir, "tmpPicLists"), docdir).replace("\\","/") + "/"
        self.dict['project/id'] = self.printer.prjid
        self.dict['config/name'] = self.printer.configId
        self.dict['/ptxrpath'] = rel(self.dict['/ptxpath'], docdir)
        self.dict['/cfgrpath'] = rel(cpath, docdir)
        self.processHdrFtr(self.printer)
        # sort out caseless figures folder. This is a hack
        for p in ("Figures", "figures"):
            picdir = j(base, p)
            if os.path.exists(picdir):
                break
        self.dict["project/picdir"] = rel(picdir, docdir).replace("\\","/")
        # Look in local Config folder for ptxprint-mods.tex, and drop back to shared/ptxprint if not found
        fpath = j(cpath, "ptxprint-mods.tex")
        if not os.path.exists(fpath):
            fpath = j(rcpath, "ptxprint-mods.tex")
        self.dict['/modspath'] = rel(fpath, docdir).replace("\\","/")
        fpath = j(cpath, "ptxprint-premods.tex")
        if not os.path.exists(fpath):
            fpath = j(rcpath, "ptxprint-premods.tex")
        self.dict['/premodspath'] = rel(fpath, docdir).replace("\\","/")
        if "document/diglotcfgrpath" not in self.dict:
            self.dict["document/diglotcfgrpath"] = ""
        self.dict['paragraph/linespacingfactor'] = f2s(float(self.dict['paragraph/linespacing']) \
                    / self.dict["paragraph/linespacebase"] / float(self.dict['paper/fontfactor']), dp=8)
        self.dict['paragraph/ifhavehyphenate'] = "" if os.path.exists(os.path.join(self.printer.configPath(""), \
                                                       "hyphen-"+self.dict["project/id"]+".tex")) else "%"
        # forward cleanup. If ask for ptxprint-mods.tex but don't have it, copy PrintDraft-mods.tex
        if self.dict["project/ifusemodssty"] == "":
            modspath = os.path.join(cpath, "ptxprint-mods.sty")
            if not os.path.exists(modspath):
                spath = os.path.join(docdir, "PrintDraft-mods.sty")
                if os.path.exists(spath):
                    copyfile(spath, modspath)
        self.dict["paper/pagegutter"] = "{:.2f}mm".format(Dimension(self.dict["paper/width"]).asunits("mm") \
                        - (self.dict["paper/gutter"] if self.dict["paper/ifaddgutter"] == "true" else 0.))
        if self.dict["project/interlinear"] != "%":
            self.interlinear = Interlinear(self.dict["project/interlang"],
                                            os.path.join(self.dict["/ptxpath"], self.dict["project/id"]))
        regfont = self.printer.get("bl_fontR")
        if regfont is not None:
            self.dict["document/spacecntxtlztn"] = "2" if regfont.isCtxtSpace else "0"
            self.calculateMargins()
        if self.inArchive:
            for b, a in Borders.items():
                if self.dict[a[1]] is None or not self.dict[a[1]]:
                    continue
                islist = a[2].startswith("\\")
                fname = getattr(self.printer, a[0], (None if islist else a[2]))
                if fname is None:
                    fname = Path("." if islist else a[2])
                if islist and not isinstance(fname, (list, tuple)):
                    fname = [fname]
                if islist:
                    self.dict[a[1]] = "\n".join(a[2].format("../shared/ptxprint/{}".format(f.name)) for f in fname)
                else:
                    self.dict[a[1]] = "../shared/ptxprint/{}".format(fname.name)
        if self.dict["fancy/versedecorator"] != "%":
            self.dict["fancy/versedecoratorisfile"] = "" if self.dict["fancy/versedecoratortype"] == "file" else "%"
            self.dict["fancy/versedecoratorisayah"] = "" if self.dict["fancy/versedecoratortype"] == "ayah" else "%"
        else:
            self.dict["fancy/versedecoratorisfile"] = "%"
            self.dict["fancy/versedecoratorisayah"] = "%"
        self.dict['notes/abovenotetotal'] = f2s(float(self.dict['notes/abovenotespace'])
                                                          + float(self.dict['notes/belownoterulespace']))
        # print(", ".join("{}={}".format(a, self.dict["fancy/versedecorator"+a]) for a in ("", "type", "isfile", "isayah")))
        
        a = self.printer.get('fcb_gridOffset')
        if a == 'margin':
            vals = (self.dict["paper/margins"], self.dict["paper/topmargin"])
        else:
            vals = ("0.0", "0.0")
        (self.dict["grid/xoffset_"], self.dict["grid/yoffset_"]) = vals
        self.dict['project/frontfile'] = ''

        if self.dict.get('document/tocleaders', None) is None:
            self.dict['document/tocleaders'] = 0
        self.dict['document/iftocleaders'] = '' if int(self.dict['document/tocleaders'] or 0) > 0 else '%'
        self.dict['document/tocleaderstyle'] = self._tocleaders[int(self.dict['document/tocleaders'] or 0)]
        self.calcRuleParameters()

    def updatefields(self, a):
        global get
        def get(k): return self[k]
        for k in a:
            v = ModelMap[k]
            val = self.printer.get(v[0], skipmissing=k.startswith("scripts/")) if v[0] is not None else None
            if v[1] is None:
                self.dict[k] = val
            else:
                try:
                    sig = signature(v[1])
                    if len(sig.parameters) == 2:
                        self.dict[k] = v[1](self.printer, val)
                    else:
                        self.dict[k] = v[1](self.printer, val, self)
                except Exception as e:
                    raise type(e)("In TeXModel with key {}, ".format(k) + str(e))

    def calcRuleParameters(self):
        notemap = {'fn': 'note', 'xr': 'xref'}
        fnrule = None
        enrule = None
        endnotes = []
        for a in ('fn', 'xr'):
            if self.dict['notes/{}pos'.format(a)] == 'endnote':
                enrule = a if enrule is None else enrule
                endnotes.append(r"\NoteAtEnd{{{}}}".format(a[0]))
            elif fnrule is None:
                fnrule = a
        for a in (('Foot', fnrule), ('End', enrule)):
            dat = []
            if a[1] is not None:
                pos = int(self.dict['notes/{}ruleposn'.format(a[1])] or 0)
                left = "\hskip {:.2f} mm".format(float(self.dict['notes/{}ruleindent'.format(a[1])] or 0.))
                right = r"\hss"
                if pos == 2 or pos == 4:      # Right or Outer
                    right, left = (left, right)
                elif pos == 5:
                    left = r"\hss"
                if pos < 3 or pos == 5:         # Left, Right or Centre
                    dat.append(r"\def\{}NoteRuleLeftIndent{{{}}}".format(a[0], left))
                    dat.append(r"\def\{}NoteRuleRightIndent{{{}}}".format(a[0], right))
                else:
                    dat.append(r"\def\{}NoteRuleLeftIndent{{\ifodd\pageno {}\else {}\fi}}".format(a[0], left, right))
                    dat.append(r"\def\{}NoteRuleRightIndent{{\ifodd\pageno {}\else {}\fi}}".format(a[0], right, left))
                dat.append(r"\def\{}NoteRuleThickness{{{} pt}}".format(a[0], self.dict['notes/{}rulethick'.format(a[1])] or "0.4"))
                dat.append(r"\def\{}NoteRuleWidth{{{:.2f}}}".format(a[0], float(self.dict['notes/{}rulelength'.format(a[1])] or 100.)/100))
                bspace = float(self.dict['notes/below{}rulespace'.format(notemap[a[1]])] or 0.)
                dat.append(r"\def\Below{}NoteRuleSpace{{{:.1f} pt}}".format(a[0], bspace))
                aspace = float(self.dict['notes/above{}space'.format(notemap[a[1]])] or 0.) + bspace
                dat.append(r"\Above{}NoteSpace={:.1f} pt".format(a[0] if a[1] != "fn" else "", aspace))
            self.dict['noterules/{}'.format(a[0].lower())] = "\n".join(dat)
        self.dict['noterules/endnotemarkers'] = "\n".join(endnotes)

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

    def prePrintChecks(self):
        reasons = []
        for a in ('regular', 'bold', 'italic', 'bolditalic'):
            # print("Checking {}: {}".format(a, self.dict['document/font{}'.format(a)]))
            if not self.dict['document/font{}'.format(a)]:
                reasons.append(_("Missing font ({})").format(a))
            break
        return reasons

    def processHdrFtr(self, printer):
        """ Update model headers from model UI read values """
        diglot = True if self.dict["document/ifdiglot"] == "" else False
        v = self.dict["footer/ftrcenter"]
        pri = self.dict["footer/ftrcenterside"] == "Pri" 
        t = self._hdrmappings.get(v, v)
        if diglot:
            t = self._addLR(t, pri)
            swap = self.dict['document/diglotswapside'] == 'true'
            ratio = float(self.dict['document/diglotprifraction'])
            # print(f"{ratio=}")
            if ratio > 0.5:
                lhfil = "\\hskip 0pt plus {}fil".format(f2s(ratio/(1-ratio)-1))
                rhfil = ""
            else:
                rhfil = "\\hskip 0pt plus {}fil".format(f2s((1-ratio)/ratio-1))
                lhfil = ""
        self.dict['footer/oddcenter'] = t
        self.dict['footer/evencenter'] = t

        mirror = self.asBool("header/mirrorlayout")
        for side in ('left', 'center', 'right'):
            v = self.dict["header/hdr"+side]
            pri = self.dict["header/hdr"+side+"side"] == "Pri"
            t = self._hdrmappings.get(v, v)
            if diglot:
                t = self._addLR(t, pri)
            self.dict['header/odd{}'.format(side)] = t
            if mirror:
                self.dict['header/even{}'.format(self._swapRL[side])] = self.mirrorHeaders(t, diglot)
            else:
                self.dict['header/even{}'.format(side)] = t
            if side == "center" and diglot and self.dict["document/diglotadjcenter"]:
                self.dict['header/odd{}'.format(side)] = (rhfil if swap else lhfil) \
                                    + self.dict['header/odd{}'.format(side)] + (lhfil if swap else rhfil)
                self.dict['header/even{}'.format(side)] = (rhfil if mirror ^ swap else lhfil) \
                                    + self.dict['header/even{}'.format(side)] + (lhfil if mirror ^ swap else rhfil)
                self.dict['footer/odd{}'.format(side)] = (rhfil if swap else lhfil) \
                                    + self.dict['footer/odd{}'.format(side)] + (lhfil if swap else rhfil)
                self.dict['footer/even{}'.format(side)] = (rhfil if mirror ^ swap else lhfil) \
                                    + self.dict['footer/even{}'.format(side)] + (lhfil if mirror ^ swap else rhfil)
                
            if t.startswith((r'\first', r'\last', r'\range')): # ensure noVodd + noVeven is \empty
                self.dict['header/noVodd{}'.format(side)] = r'\empty'
            else:
                self.dict['header/noVodd{}'.format(side)] = t  # copy the other header as is
            if mirror:
                if t.startswith((r'\first', r'\last', r'\range')):
                    self.dict['header/noVeven{}'.format(self._swapRL[side])] = r'\empty'
                else:
                    self.dict['header/noVeven{}'.format(self._swapRL[side])] = self.mirrorHeaders(t, diglot)
            else:
                if t.startswith((r'\first', r'\last', r'\range')): # ensure noVodd + noVeven is \empty
                    self.dict['header/noVeven{}'.format(side)] = r'\empty'
                else:
                    self.dict['header/noVeven{}'.format(side)] = t 

    def _addLR(self, t, pri):
        if t in [r"\firstref", r"\lastref", r"\rangeref", r"\pagenumber", r"\hrsmins", r"\isodate" \
                 r"\book", r"\bookalt"]:                
            if pri:
                t = t+'L'
            else:
                t = t+'R'
        elif t == r"\empty":
            pass
        else:
            if pri:
                t = "\headfootL{{{}}}".format(t)
            else:
                t = "\headfootR{{{}}}".format(t)
        return t

    def mirrorHeaders(self, h, dig=False):
        if dig and h.endswith(("L", "R")):
            try:
                return self._mirrorRL[h[:-1]]+h[-1:]
            except KeyError:
                return h
        else:
            try:
                return self._mirrorRL[h]
            except KeyError:
                return h

    def calculateMargins(self):
        (marginmms, topmarginmms, bottommarginmms, headerposmms, footerposmms,
         ruleposmms, headerlabel, footerlabel) = self.printer.getMargins()
        self.dict["paper/topmarginfactor"] = f2s(topmarginmms / marginmms)
        self.dict["paper/bottommarginfactor"] = f2s(bottommarginmms / marginmms)
        self.dict["paper/headerposition"] = f2s(headerposmms / marginmms)
        self.dict["paper/footerposition"] = f2s(footerposmms / marginmms)
        self.dict["paper/ruleposition"] = f2s(ruleposmms * 72.27 / 25.4)
        
    def texfix(self, path):
        return path.replace(" ", r"\ ")

    def asTex(self, template="template.tex", filedir=".", jobname="Unknown", extra=""):
        for k, v in self._settingmappings.items():
            if self.dict[k] == "":
                self.dict[k] = self.ptsettings.dict.get(v, "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z")
        res = []
        resetPageDone = False
        docdir, docbase = self.docdir()
        self.dict['jobname'] = jobname
        self.dict['document/imageCopyrights'] = self.generateImageCopyrightText()
                # if self.dict['document/includeimg'] else self.generateEmptyImageCopyrights()
        self.dict['project/colophontext'] = re.sub(r'://', r':/ / ', self.dict['project/colophontext'])
        self.dict['project/colophontext'] = re.sub(r"(?i)(\\zimagecopyrights)([A-Z]{2,3})", \
                lambda m:m.group(0).lower(), self.dict['project/colophontext'])
        with universalopen(os.path.join(os.path.dirname(__file__), template)) as inf:
            for l in inf.readlines():
                if l.startswith(r"%\ptxfile"):
                    res.append(r"\PtxFilePath={"+os.path.relpath(filedir, docdir).replace("\\","/")+"/}")
                    for i, f in enumerate(self.dict['project/bookids']):
                        fname = self.dict['project/books'][i]
                        if extra != "":
                            fname = re.sub(r"^([^.]*).(.*)$", r"\1"+extra+r".\2", fname)
                        if i == len(self.dict['project/bookids']) - 1 and self.dict['project/ifcolophon'] == "":
                            res.append(r"\lastptxfiletrue")
                            if self.dict['project/pgbreakcolophon'] != '%':
                                res.append(r"\endbooknoejecttrue")
                        if not resetPageDone and f not in self._peripheralBooks:
                            res.append(r"\ifodd\pageno\else\catcode`\@=11 \shipwithcr@pmarks{\vbox{}}\catcode`\@=12 \fi")
                            res.append(r"\pageno={}".format(self.dict['document/startpagenum']))
                            resetPageDone = True
                        if not self.asBool('document/ifshow1chbooknum') and \
                           self.asBool('document/ifshowchapternums', '%') and \
                           f in oneChbooks:
                            res.append(r"\OmitChapterNumbertrue")
                            res.append(r"\ptxfile{{{}}}".format(fname))
                            res.append(r"\OmitChapterNumberfalse")
                        elif self.dict['paper/columns'] == '2' and \
                             self.dict['document/clsinglecol'] and \
                             f in self.dict['document/clsinglecolbooks']:
                            res.append(r"\BodyColumns=1")
                            res.append(r"\ptxfile{{{}}}".format(fname))
                            res.append(r"\BodyColumns=2")
                        else:
                            res.append(r"\ptxfile{{{}}}".format(fname))
                elif l.startswith(r"%\extrafont") and self.dict["document/fontextraregular"]:
                    spclChars = re.sub(r"\[uU]([0-9a-fA-F]{4,6})", lambda m:chr(int(m.group(1), 16)),
                                                                            self.dict["paragraph/missingchars"])
                    # print(spclChars.split(' '), [len(x) for x in spclChars.split(' ')])
                    if self.dict["paragraph/ifusefallback"] and len(spclChars):
                        badlist = "\u2018\u2019\u201c\u201d*#%"
                        specials = spclChars.replace(" ", "").encode("raw_unicode_escape").decode("raw_unicode_escape")
                        a = ["".join(chr(ord(c) + 16 if ord(c) < 58 else ord(c) - 23)
                             for c in str(hex(ord(x)))[2:]).lower() for x in specials]
                        b = ["".join((c) for c in str(hex(ord(x)))[2:]).lower() for x in specials]
                        c = [x for x in zip(a,b) if chr(int(x[1],16)) not in badlist]
                        if not len(c):
                            continue
                        res.append(r"% for defname @active+ @+digit => 0->@, 1->a ... 9->i A->j B->k .. F->o")
                        res.append(r"% 12 (size) comes from \p size")
                        res.append(r'\def\extraregular{{"{}"}}'.format(self.dict["document/fontextraregular"]))
                        res.append(r"\catcode`\@=11")
                        res.append(r"\def\do@xtrafont{\x@\s@textrafont\ifx\thisch@rstyle\undefined\m@rker\else\thisch@rstyle\fi}")
                        for a,b in c:
                            res.append(r"\def\@ctive{}{{\leavevmode{{\do@xtrafont {}{}}}}}".format(a, '^'*len(b), b))
                            res.append(r"\DefineActiveChar{{{}{}}}{{\@ctive{}}}".format( '^'*len(b), b, a))
                        res.append(r"\@ctivate")
                        res.append(r"\catcode`\@=12")
                    else:
                        res.append(r"% No special/missing characters specified for fallback font")
                elif l.startswith(r"%\horiznotespacing"):
                    mins = float(self.dict["notes/horiznotespacemin"])
                    maxs = float(self.dict["notes/horiznotespacemax"])
                    tgts = mins + ((maxs - mins) / 3)
                    minus = tgts - mins
                    plus = maxs - tgts
                    res.append(r"\internoteskip={}pt plus {}pt minus {}pt".format(f2s(tgts), f2s(plus), f2s(minus)))
                elif l.startswith(r"%\optimizepoetry"):
                    bks = self.dict["document/clabelbooks"]
                    if self.dict["document/ifchaplabels"] == "%" and len(bks):
                        for bk in bks.split(" "):
                            if bk in self.dict['project/bookids']:
                                res.append((r"\setbookhook{{start}}{{{}}}{{\gdef\BalanceThreshold{{3}}\clubpenalty=50"
                                            + r"\widowpenalty=50}}").format(bk))
                                res.append((r"\setbookhook{{end}}{{{}}}{{\gdef\BalanceThreshold{{0}}\clubpenalty=10000"
                                            + r"\widowpenalty=10000}}").format(bk))
                elif l.startswith(r"%\snippets"):
                    for k, c in sorted(self._snippets.items(), key=lambda x: x[1][2].order):
                        if c[1] is None:
                            v = self.asBool(k)
                        else:
                            v = c[1](self.dict[k])
                        if v:
                            fn = getattr(c[2], 'generateTex', None)
                            if fn is not None:
                                res.append(fn(v, self))
                            elif c[2].processTex:
                                res.append(c[2].texCode.format(**self.dict))
                            else:
                                res.append(c[2].texCode)
                    script = self.dict["document/script"]
                    if len(script) > 0:
                        sclass = getattr(scriptsnippets, script[8:].lower(), None)
                        if sclass is not None:
                            res.append(sclass.tex(self))
                    res.append("""
\\catcode"FDEE=1 \\catcode"FDEF=2
\\prepusfm
\\def\\zcopyright\uFDEE{project/copyright}\uFDEF
\\def\\zlicense\uFDEE{project/license}\uFDEF
""".format(**self.dict))
                    if "diglot/copyright" in self.dict:
                        res.append("\\def\\zcopyrightR\uFDEE{}\uFDEF".format(self.dict["diglot/copyright"]))
                    res.append("\\unprepusfm")
                elif l.startswith(r"%\defzvar"):
                    for k in self.printer.allvars():
                        res.append(r"\defzvar{{{}}}{{{}}}".format(k, self.printer.getvar(k)))
                    for k, e in (('contentsheader', 'document/toctitle'),):
                        res.append(r"\defzvar{{{}}}{{{}}}".format(k, self.dict[e]))
                else:
                    res.append(l.rstrip().format(**self.dict))
        return "\n".join(res).replace("\\OmitChapterNumberfalse\n\\OmitChapterNumbertrue\n","")

    def _doperiph(self, m):
        if self.frontperiphs is None:
            frtfile = os.path.join(self.printer.settings_dir, self.printer.prjid, self.printer.getBookFilename("FRT"))
            self.frontperiphs = {}
            if not os.path.exists(frtfile):
                return ""
            with open(frtfile, encoding="utf-8") as inf:
                mode = 0        # default
                currperiphs = []
                currk = None
                for l in inf.readlines():
                    ma = re.match(r'\\periph\s+([^|]+)(?:\|\s*(?:id\s*=\s*"([^"]+)|(\S+)))', l)
                    if ma:
                        if mode == 1:    # already collecting so save
                            self.frontperiphs[currk] = "\n".join(currperiphs)
                        currk = ma[2] or ma[3]
                        if not currk:
                            currk = self._periphids.get(m[1].lower(), m[1].lower())
                        currperiphs = []
                        mode = 1
                    elif mode == 1:
                        if r"\periph" in l:
                            mode = 0
                        else:
                            currperiphs.append(l.rstrip())
                if currk is not None:
                    self.frontperiphs[currk] = "\n".join(currperiphs)
        k = m[1]
        if k in self.frontperiphs:
            return self.frontperiphs[k]
        else:
            return ""

    def createFrontMatter(self, outfname):
        self.dict['project/frontfile'] = os.path.basename(outfname)
        infpath = self.printer.configFRT()
        if os.path.exists(infpath):
            fcontent = []
            with open(infpath, encoding="utf-8") as inf:
                seenperiph = False
                for l in inf.readlines():
                    if l.strip().startswith(r"\periph"):
                        l = r"\pb" if self.dict['project/periphpagebreak'] and seenperiph else ""
                        seenperiph = True
                    l = re.sub(r"\\zperiphfrt\s*\|([^\\\s]+)\s*\\\*", self._doperiph, l)
                    l = re.sub(r"\\zbl\s*\|(\d+)\\\*", lambda m: "\\b\n" * int(m.group(1)), l)
                    l = re.sub(r'(\\fig .*?src=")(.*?)(".*?\\fig\*)', lambda m:m.group(1)+m.group(2).replace("\\","/")+m.group(3), l)
                    fcontent.append(l.rstrip())
            with open(outfname, "w", encoding="utf-8") as outf:
                outf.write("\n".join(fcontent))

    def flattenModule(self, infpath, outdir):
        outfpath = os.path.join(outdir, os.path.basename(infpath))
        doti = outfpath.rfind(".")
        if doti > 0:
            outfpath = outfpath[:doti] + "-flat" + outfpath[doti:]
        usfms = self.printer.get_usfms()
        try:
            mod = Module(infpath, usfms)
            res = mod.parse()
        except SyntaxError as e:
            return (None, e)
        with open(outfpath, "w", encoding="utf-8") as outf:
            outf.write(sfm.generate(res))
        return outfpath

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

    def runChanges(self, changes, bk, dat):
        # import pdb; pdb.set_trace()
        for c in changes:
            logger.debug("Change: {}".format(c))
            if c[0] is None:
                dat = c[1].sub(c[2], dat)
            elif isinstance(c[0], str):
                if c[0] == bk:
                    dat = c[1].sub(c[2], dat)
            else:
                def simple(s):
                    return c[1].sub(c[2], s)
                dat = c[0](simple, bk, dat)
        return dat

    def convertBook(self, bk, chaprange, outdir, prjdir, letterspace="\uFDD0"):
        if self.changes is None:
            if self.asBool('project/usechangesfile'):
                # print("Applying PrntDrftChgs:", os.path.join(prjdir, 'PrintDraftChanges.txt'))
                self.changes = self.readChanges(os.path.join(prjdir, 'PrintDraftChanges.txt'), bk)
            else:
                self.changes = []
        printer = self.printer
        draft = "-" + (self.printer.configName() or "draft")
        self.makelocalChanges(printer, bk, chaprange=chaprange)
        customsty = os.path.join(prjdir, 'custom.sty')
        if not os.path.exists(customsty):
            self.dict["/nocustomsty"] = "%"
        else:
            self.dict["/nocustomsty"] = ""
        fname = printer.getBookFilename(bk)
        if fname is None:
            infpath = os.path.join(prjdir, bk)  # assume module
            infpath = self.flattenModule(infpath, outdir)
            if isinstance(infpath, tuple) and infpath[0] is None:
                self.printer.doError("Failed to flatten module text (due to a Syntax Error?):",        
                secondary=str(infpath[1]), 
                title="PTXprint [{}] - Canonicalise Text Error!".format(self.VersionStr),
                show=not self.printer.get("c_quickRun"))
                return None
        else:
            infpath = os.path.join(prjdir, fname)
        if not self.dict['project/runscriptafter']:
            infpath = self.runConversion(infpath, outdir)
        outfname = os.path.basename(infpath)
        # outfname = fname
        doti = outfname.rfind(".")
        if doti > 0:
            outfname = outfname[:doti] + draft + outfname[doti:]
        outfpath = os.path.join(outdir, outfname)
        codepage = self.ptsettings.get('Encoding', 65001)
        with universalopen(infpath, cp=codepage) as inf:
            dat = inf.read()

            doc = None
            if self.interlinear is not None:
                doc = self._makeUSFM(dat.splitlines(True), bk)
                linelengths = [len(x) for x in dat.splitlines(True)]
                if doc is not None:
                    doc.calc_PToffsets()
                    self.interlinear.convertBk(bk, doc, linelengths)
                    if len(self.interlinear.fails):
                        printer.doError("The following references need to be reapproved: " + " ".join(self.interlinear.fails),
                                        show=not printer.get("c_quickRun"))
                        self.interlinear.fails = []

            if self.changes is not None and len(self.changes):
                if doc is not None:
                    dat = str(doc)
                    doc = None
                dat = self.runChanges(self.changes, bk, dat)
                self.analyzeImageCopyrights(dat)

            if self.dict['project/canonicalise'] or self.dict['document/ifletter'] == "" \
                        or not self.asBool("document/bookintro") \
                        or not self.asBool("document/introoutline")\
                        or self.asBool("document/hidemptyverses"):
                if doc is None:
                    doc = self._makeUSFM(dat.splitlines(True), bk)
                if doc is not None:
                    if not self.asBool("document/bookintro") or not self.asBool("document/introoutline"):
                        doc.stripIntro(not self.asBool("document/bookintro"), not self.asBool("document/introoutline"))
                    if self.asBool("document/hidemptyverses"):
                        doc.stripEmptyChVs(ellipsis=self.asBool("document/elipsizemptyvs"))

            if self.dict['fancy/endayah'] == "":
                if doc is None:
                    doc = self._makeUSFM(dat.splitlines(True), bk)
                doc.versesToEnd()
                
            if doc is not None and getattr(doc, 'doc', None) is not None:
                dat = str(doc)

            if self.localChanges is not None:
                dat = self.runChanges(self.localChanges, bk, dat)

        with open(outfpath, "w", encoding="utf-8") as outf:
            outf.write(dat)
        if self.dict['project/runscriptafter']:
            bn = os.path.basename(self.runConversion(outfpath, outdir))
        else:
            bn = os.path.basename(outfpath)

        if '-conv' in bn:
            newname = re.sub(r"(\{}\-conv|\-conv\{}|\-conv)".format(draft, draft), draft, bn)
            copyfile(os.path.join(outdir, bn), os.path.join(outdir, newname))
            os.remove(os.path.join(outdir, bn))
            return newname
        else:
            return bn
            
    def _makeUSFM(self, txtlines, bk):
        syntaxErrors = []
        import pdb; pdb.set_trace()
        try:
            doc = Usfm(txtlines, self.sheets)
            doc.normalise()
        except SyntaxError as e:
            syntaxErrors.append("{} {} line:{}".format(self.prjid, bk, str(e).split('line', maxsplit=1)[1]))
        except Exception as e:
            syntaxErrors.append("{} {} Error({}): {}".format(self.prjid, bk, type(e), str(e)))
            traceback.print_exc()
        if len(syntaxErrors):
            dlgtitle = "PTXprint [{}] - USFM Text Error!".format(self.VersionStr)
            errbits = re.match(r"(\S+) (...) line: (\d+),\d+: orphan marker (\\.+?)", syntaxErrors[0])
            if errbits is not None:
                self.printer.doError("Syntax Error warning: ",        
                    secondary=_("Examine line {} in {} on the 'Final SFM' tab of the View+Edit " + \
                        "page to determine the cause of this issue related to marker: {}.").format(errbits[3], errbits[2], errbits[4]) + \
                        "\n\n"+_("This warning was triggered due to 'Auto-Correct USFM' being " + \
                        "enabled on the Advanced tab but is due to an orphaned marker. " + \
                        "It means the marker does not belong in that position, or it " + \
                        "is missing a valid parent marker."), title=dlgtitle,
                        show=not self.printer.get("c_quickRun"))
            else:
                prtDrft = _("And check if a faulty rule in PrintDraftChanges.txt has caused the error(s).") if self.asBool("project/usechangesfile") else ""
                self.printer.doError(_("Failed to normalize texts due to a Syntax Error: "),        
                    secondary="\n".join(syntaxErrors)+"\n\n"+_("Run the Basic Checks in Paratext to ensure there are no Marker errors "+ \
                    "in either of the diglot projects. If this error persists, try running the Schema Check in Paratext as well.") + " " + prtDrft,
                    title=dlgtitle, show=not self.printer.get("c_quickRun"))
                    
            return None
        else:
            return doc  

    def make_contextsfn(self, bk, *changes):
        # functional programmers eat your hearts out
        def makefn(reg, currfn):
            if currfn is not None:
                def compfn(fn, b, s):
                    def domatch(m):
                        return currfn(lambda x:fn(x.group(0)), m.group(0))
                    return reg.sub(domatch, s) if bk is None or b == bk else s
            else:
                def compfn(fn, b, s):
                    return reg.sub(lambda m:fn(m.group(0)), s) if bk is None or b == bk else s
            return compfn
        return reduce(lambda currfn, are: makefn(are, currfn), reversed([c for c in changes if c is not None]), None)

    def readChanges(self, fname, bk):
        changes = []
        if not os.path.exists(fname):
            return []
        qreg = r'(?:"((?:[^"\\]|\\.)*?)"|' + r"'((?:[^'\\]|\\.)*?)')"
        with universalopen(fname) as inf:
            for i, l in enumerate(inf.readlines()):
                l = l.strip().replace(u"\uFEFF", "")
                l = re.sub(r"\s*#.*$", "", l)
                if not len(l):
                    continue
                contexts = []
                atcontexts = []
                try:
                    # test for "at" command
                    m = re.match(r"^\s*at\s+(.*?)\s+(?=in|['\"])", l)
                    if m:
                        atref = RefList.fromStr(m.group(1), context=AnyBooks)
                        for r in atref.allrefs():
                            if r.chap == 0:
                                atcontexts.append((r.book, None))
                            elif r.verse == 0:
                                atcontexts.append((r.book, regex.compile(r"(?<=\\c {}(?=\D)).*?($|\\[cv] )".format(r.chap), flags=regex.S)))
                            else:
                                atcontexts.append((r.book, regex.compile(r"(?<=\\c {}(?=\D)(?:.(?!\\c))*?)\\v {} .*?($|\\[cv] )".format(r.chap, r.verse), flags=regex.S)))
                        l = l[m.end():].strip()
                    else:
                        atcontexts = [None]
                    # test for 1+ "in" commands
                    while True:
                        m = re.match(r"^\s*in\s+"+qreg+r"\s*:\s*", l)
                        if not m:
                            break
                        contexts.append(regex.compile(m.group(1) or m.group(2), flags=regex.M))
                        l = l[m.end():].strip()
                    # capture the actual change
                    m = re.match(r"^"+qreg+r"\s*>\s*"+qreg, l)
                    if m:
                        for at in atcontexts:
                            if at is None:
                                context = self.make_contextsfn(None, *contexts) if len(contexts) else None
                            elif len(contexts) or at[1] is not None:
                                context = self.make_contextsfn(at[0], at[1], *contexts)
                            else:
                                context = at[0]
                            changes.append((context, regex.compile(m.group(1) or m.group(2), flags=regex.M),
                                            m.group(3) or m.group(4) or ""))
                        continue
                except re.error as e:
                    self.printer.doError("Regular expression error: {} in changes file at line {}".format(str(e), i+1),
                                         show=not self.printer.get("c_quickRun"))
        return changes

    def makelocalChanges(self, printer, bk, chaprange=None):
        script = self.dict["document/script"]
        if len(script):
            sscript = getattr(scriptsnippets, script[8:].lower(), None)
            if sscript is not None:
                self.changes.extend(sscript.regexes(self))
        if self.printer is not None and self.printer.get("c_tracing"):
            print("List of PrintDraftChanges:-------------------------------------------------------------")
            report = "\n".join("{} -> {}".format(p[1].pattern, p[2]) for p in self.changes)
            if getattr(self.printer, "logger", None) is not None:
                self.printer.logger.insert_at_cursor(v)
            else:
                try:
                    print(report)
                except UnicodeEncodeError:
                    print("Unable to print details of PrintDraftChanges.txt")
        self.localChanges = []
        if bk == "GLO" and self.dict['document/filterglossary']:
            self.filterGlossary(printer)
        if chaprange is not None:
            first, last = chaprange
        elif self.dict["project/bookscope"] == "single":
            first = int(float(self.dict["document/chapfrom"]))
            last = int(float(self.dict["document/chapto"]))
        else:
            first, last = (-1, -1)
        
        # Fix things that other parsers accept and we don't
        self.localChanges.append((None, regex.compile(r"(\\[cv] [^ \\\r\n]+)(\\)", flags=regex.S), r"\1 \2"))
        
        # Remove empty \h markers (might need to expand this list and loop through a bunch of markers)
        self.localChanges.append((None, regex.compile(r"(\\h ?\r?\n)", flags=regex.S), r""))
        
        # This section handles PARTIAL books (from chapter X to chapter Y)
        if self.asBool("document/ifchaplabels", true="%"):
            clabel = self.dict["document/clabel"]
            clbooks = self.dict["document/clabelbooks"].split()
            # print("Chapter label: '{}' for '{}' with {}".format(clabel, " ".join(clbooks), bk))
            if len(clabel) and (not len(clbooks) or bk in clbooks):
                self.localChanges.append((None, regex.compile(r"(\\c 1)(?=\s*\r?\n|\s)", flags=regex.S), r"\\cl {}\n\1".format(clabel)))
                
        # if self.dict["project/bookscope"] == "single":
        if first > 1:
            self.localChanges.append((None, regex.compile(r"\\c 1 ?\r?\n.+(?=\\c {} ?\r?\n)".format(first), flags=regex.S), ""))
        if last >=0 and last < int(chaps.get(bk, 999)):
            self.localChanges.append((None, regex.compile(r"\\c {} ?\r?\n.+".format(last+1), flags=regex.S), ""))

        # Throw out the known "nonpublishable" markers and their text (if any)
        self.localChanges.append((None, regex.compile(r"\\(usfm|ide|rem|sts|restore|pubinfo)( .*?)?\n(?=\\)", flags=regex.M), ""))

        # If a printout of JUST the book introductions is needed (i.e. no scripture text) then this option is very handy
        if not self.asBool("document/ifmainbodytext"):
            self.localChanges.append((None, regex.compile(r"\\c 1 ?\r?\n.+".format(first), flags=regex.S), ""))

        # Probably need to make this more efficient for multi-book and lengthy glossaries (cache the GLO & changes reqd etc.)
        if self.asBool("notes/glossaryfootnotes"):
            self.makeGlossaryFootnotes(printer, bk)

        # Glossary Word markup: Remove the second half of the \w word|glossary-form\w* and apply chosen glossary markup
        v = self.dict["document/glossarymarkupstyle"]
        gloStyle = self._glossarymarkup.get(v, v)
        if v is not None:
            if gloStyle is not None and len(v) == 2: # otherwise skip over OLD Glossary markup definitions
                self.localChanges.append((None, regex.compile(r"\\\+?w ((?:.(?!\\\+w\*))+?)(\|[^|]+?)?\\\+?w\*", flags=regex.M), gloStyle))

        if self.asBool("notes/includexrefs"): # This seems back-to-front, but it is correct because of the % if v
            self.localChanges.append((None, regex.compile(r'(?i)\\x .+?\\x\*', flags=regex.M), ''))
            
        if self.asBool("document/ifinclfigs") and bk in self._peripheralBooks:
            # Remove any illustrations which don't have a |p| 'loc' field IF this setting is on
            if self.asBool("document/iffigexclwebapp"):
                self.localChanges.append((None, regex.compile(r'(?i)\\fig ([^|]*\|){3}([aw]+)\|[^\\]*\\fig\*', flags=regex.M), ''))  # USFM2
                self.localChanges.append((None, regex.compile(r'(?i)\\fig [^\\]*\bloc="[aw]+"[^\\]*\\fig\*', flags=regex.M), ''))    # USFM3
            def figtozfiga(m):
                a = self.printer.picinfos.getAnchor(m.group(1), bk)
                if a is None:
                    return ""
                ref = re.sub(r"^\S+\s+", r"", a)
                return "\\zfiga|{}\\*".format(ref)
            self.localChanges.append((None, regex.compile(r'\\fig.*?src="([^"]+?)".*?\\fig\*', flags=regex.M), figtozfiga))
            self.localChanges.append((None, regex.compile(r'\\fig(?: .*?)?\|(.*?)\|.*?\\fig\*', flags=regex.M), figtozfiga))

            if self.asBool("document/iffighiderefs"): # del ch:vs from caption 
                self.localChanges.append((None, regex.compile(r"(\\fig [^\\]+?\|)([0-9:.\-,\u2013\u2014]+?)(\\fig\*)", \
                                          flags=regex.M), r"\1\3"))   # USFM2
                self.localChanges.append((None, regex.compile(r'(\\fig .+?)(ref=\"\d+[:.]\d+([-,\u2013\u2014]\d+)?\")(.*?\\fig\*)', \
                                          flags=regex.M), r"\1\4"))   # USFM3
        else:
            # Strip out all \figs from the USFM as an internally generated temp PicList will do the same job
            self.localChanges.append((None, regex.compile(r'\\fig[\s|][^\\]+?\\fig\*', flags=regex.M), ""))

        if not self.asBool("document/sectionheads"): # Drop ALL Section Headings (which also drops the Parallel passage refs now)
            self.localChanges.append((None, regex.compile(r"\\[sr] .+", flags=regex.M), ""))

        if not self.asBool("document/parallelrefs"): # Drop ALL Parallel Passage References
            self.localChanges.append((None, regex.compile(r"\\r .+", flags=regex.M), ""))

        if self.asBool("document/preventorphans"): # Prevent orphans at end of *any* paragraph
            self.localChanges.append((None, regex.compile(r"(\\q\d?(\s?\r?\n?\\v)?( \S+)+( (?!\\)[^\\\s]{,6})) ([\S]{,9}\s*\n)", \
                                            flags=regex.M), r"\1\u2000\5"))
            self.localChanges.append((None, regex.compile(r"(?<=\\[^tm][^\\]+)(\s+[^ 0-9\\\n\u2000\u00A0]{,6}) ([^ 0-9\\\n\u2000\u00A0]{,8}\n(?:\\[pmqsc]|$))", flags=regex.S), r"\1\u2000\2"))

        if self.asBool("document/preventwidows"):
            # Push the verse number onto the next line (using NBSP) if there is
            # a short widow word (3 characters or less) at the end of the line
            self.localChanges.append((None, regex.compile(r"(\\v \d+([-,]\d+)? [\w]{1,3}) ", flags=regex.M), r"\1\u00A0")) 

        # By default, HIDE chapter numbers for all non-scripture (Peripheral) books (unless "Show... is checked)
        if not self.asBool("document/showxtrachapnums") and bk in TexModel._peripheralBooks:
            self.localChanges.append((None, regex.compile(r"(\\c \d+ ?\r?\n)", flags=regex.M), ""))

        if self.asBool("document/ch1pagebreak"):
            self.localChanges.append((None, regex.compile(r"(\\c 1 ?\r?\n)", flags=regex.M), r"\pagebreak\r\n\1"))

        if self.asBool("document/glueredupwords"): # keep reduplicated words together
            self.localChanges.append((None, regex.compile(r"(?<=[ ])(\w{3,}) \1(?=[\s,.!?])", flags=regex.M), r"\1\u2000\1")) 
        
        if self.asBool("notes/addcolon"): # Insert a colon between \fq (or \xq) and following \ft (or \xt)
            self.localChanges.append((None, regex.compile(r"(\\[fx]q .+?):* ?(\\[fx]t)", flags=regex.M), r"\1: \2")) 
        
        if self.asBool("notes/keepbookwithrefs"): # keep Booknames and ch:vs nums together within \xt and \xo 
            self.localChanges.append((self.make_contextsfn(None, regex.compile(r"(\\[xf]t [^\\]+)")),
                                    regex.compile(r"(\d?[^\s\d\-\\,;]{3,}[^\\\s]*?) (\d+[:.]\d+)"), r"\1\u2000\2"))
            self.localChanges.append((self.make_contextsfn(None, regex.compile(r"(\\[xf]t [^\\]+)")),
                                    regex.compile(r"( .) "), r"\1\u2000")) # Ensure no floating single chars in note text

        # keep \xo & \fr refs with whatever follows (i.e the bookname or footnote) so it doesn't break at end of line
        self.localChanges.append((None, regex.compile(r"(\\(xo|fr) (\d+[:.]\d+([-,]\d+)?)) "), r"\1\u00A0"))

        for c in ("fn", "xr"):
            # Force all footnotes/x-refs to be either '+ ' or '- ' rather than '*/#'
            if self.asBool("notes/{}override".format(c)):
                t = "+" if self.asBool("notes/if{}autocallers".format(c)) else "-"
                self.localChanges.append((None, regex.compile(r"\\{} .".format(c[0])), r"\\{} {}".format(c[0],t)))
            # Remove the [spare] space after a note caller if the caller is omitted AND if after a digit (verse number).
            if self.asBool("notes/{}omitcaller".format(c)):
                self.localChanges.append((None, regex.compile(r"(\d )(\\[{0}] - .*?\\[{0}]\*)\s+".format(c[0])), r"\1\2"))

        # Paratext marks no-break space as a tilde ~
        self.localChanges.append((None, regex.compile(r"~", flags=regex.M), r"\u00A0")) 

        # Paratext marks forced line breaks as //
        self.localChanges.append((None, regex.compile(r"//", flags=regex.M), r"\u2028"))  

        # Convert hyphens from minus to hyphen
        self.localChanges.append((None, regex.compile(r"(?<!\\[fx]\s)((?<=\s)-|-(?=\s))", flags=regex.M), r"\u2011"))

        if self.asBool("document/toc") and self.asBool("document/multibook"):
            # Only do this IF the auto Table of Contents is enabled AND there is more than one book
            for c in range(1,4): # Remove any \toc lines that we don't want appearing in the ToC
                if not self.asBool("document/usetoc{}".format(c)):
                    self.localChanges.append((None, regex.compile(r"(\\toc{} .+)".format(c), flags=regex.M), ""))

        # Add End of Book decoration PDF to Scripture books only if FancyBorders is enabled and .PDF defined
        if self.asBool("fancy/enableborders") and self.asBool("fancy/endofbook") and bk not in self._peripheralBooks \
           and self.dict["fancy/endofbookpdf"].lower().endswith('.pdf'):
            self.localChanges.append((None, regex.compile(r"\Z", flags=regex.M), r"\r\n\z"))
        
        # Insert a rule between end of Introduction and start of body text (didn't work earlier, but might work now)
        # self.localChanges.append((None, regex.compile(r"(\\c\s1\s?\r?\n)", flags=regex.S), r"\\par\\vskip\\baselineskip\\hskip-\\columnshift\\hrule\\vskip 2\\baselineskip\n\1"))

        # Apply any changes specified in snippets
        for k, c in sorted(self._snippets.items(), key=lambda x: x[1][2].order):
            if self.printer is None:
                v = self.asBool(k) if c[1] is None else c[1](self.dict[k])
            elif c[1] is None:
                v = self.printer.get(c[0])
                self.dict[k] = "true" if v else "false"
            else:
                self.dict[k] = self.printer.get(c[0])
                v = c[1](self.dict[k])
            if v: # if the c_checkbox is true then extend the list with those changes
                if k == "snippets/fancyintro" and bk in self._peripheralBooks: # Only allow fancyIntros for scripture books
                    pass
                else:
                    self.localChanges.extend(c[2].regexes)

        ## Final tweaks
        # Strip out any spaces either side of an en-quad 
        self.localChanges.append((None, regex.compile(r"\s?\u2000\s?", flags=regex.M), r"\u2000")) 
        # Change double-spaces to singles
        self.localChanges.append((None, regex.compile(r" {2,}", flags=regex.M), r" ")) 
        # Escape special codes % and $ that could be in the text itself
        self.localChanges.append((None, regex.compile(r"([%$])", flags=regex.M), r"\\\1")) 

        if self.printer is not None and self.printer.get("c_tracing"):
            print("List of Local Changes:----------------------------------------------------------")
            report = "\n".join("{} -> {}".format(p[1].pattern, p[2]) for p in self.localChanges)
            if getattr(printer, "logger", None) is not None:
                printer.logger.insert_at_cursor(v)
            else:
                print(report)
        return self.localChanges

    def base(self, fpath):
        doti = fpath.rfind(".")
        return os.path.basename(fpath[:doti])

    def codeLower(self, fpath):
        cl = re.match(self.printer.getPicRe()+"$", self.base(fpath))
        if cl:
            return cl[0].lower()
        else:
            return ""

    def newBase(self, fpath):
        clwr = self.codeLower(fpath)
        if len(clwr):
            return clwr
        else:
            return re.sub('[()&+,.;: ]', '_', self.base(fpath).lower())

    def makeGlossaryFootnotes(self, printer, bk):
        # Glossary entries for the key terms appearing like footnotes
        prjid = self.dict['project/id']
        prjdir = os.path.join(self.ptsettings.basedir, prjid)
        fname = printer.getBookFilename("GLO", prjdir)
        infname = os.path.join(prjdir, fname)
        if os.path.exists(infname):
            with universalopen(infname, rewrite=True) as inf:
                dat = inf.read()
                ge = re.findall(r"\\p \\k (.+)\\k\* (.+)\r?\n", dat) # Finds all glossary entries in GLO book (may need to add \ili)
                if ge is not None:
                    for g in ge:
                        gdefn = re.sub(r"\\xt (.+)\\xt\*", r"\1", g[1])
                        self.localChanges.append((None, regex.compile(r"(\\w (.+\|)?{} ?\\w\*)".format(g[0]), flags=regex.M), \
                                                                     r"\1\\f + \\fq {}: \\ft {}\\f* ".format(g[0],gdefn)))

    def filterGlossary(self, printer):
        # Only keep entries that have appeared in this collection of books
        glossentries = []
        prjid = self.dict['project/id']
        prjdir = os.path.join(self.dict["/ptxpath"], prjid)
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

    def analyzeImageCopyrights(self, txt):
        for m in re.findall(r"(?i)\\(\S+).*?\\zimagecopyrights([A-Z]{2,3})?", txt):
            self.imageCopyrightLangs[m[1].lower() if m[1] else "en"] = m[0]
        return

    def generateEmptyImageCopyrights(self):
        self.analyzeImageCopyrights(self.dict['project/colophontext'])
        res = [r"\def\zimagecopyrights{}"]
        for k in self.imageCopyrightLangs.keys():
            res.append(r"\def\zimagecopyrights{}{{}}".format(k))
        return "\n".join(res)

    def generateImageCopyrightText(self):
        artpgs = {}
        mkr='pc'
        sensitive = self['document/sensitive']
        picpagesfile = os.path.join(self.docdir()[0], self['jobname'] + ".picpages")
        crdts = []
        cinfo = self.printer.copyrightInfo
        self.analyzeImageCopyrights(self.dict['project/colophontext'])
        if os.path.exists(picpagesfile):
            with universalopen(picpagesfile) as inf:
                dat = inf.read()

            # \figonpage{304}{56}{cn01617.jpg}{tl}{© David C. Cook Publishing Co, 1978.}{x170.90504pt}
            rematch = r"\\figonpage\{(\d+)\}\{\d+\}\{(?:" + self.printer.getPicRe() + "|(.*?))\.[^}]+\}\{.*?\}\{(.*?)?\}\{.+?\}"
            m = re.findall(rematch, dat)
            msngPgs = []
            customStmt = []
            if len(m):
                for f in m:
                    if not len(f) or not f[0] or f[5] == "None":
                        continue
                    a = 'co' if f[1] == 'cn' else f[1] # merge Cook's OT & NT illustrations together
                    if a == '' and f[5] != '':
                        artpgs.setdefault(f[5], []).append(int(f[0]))
                    elif a == '':
                        artpgs.setdefault('zz', []).append(int(f[0]))
                        msngPgs += [f[0]] 
                    else:
                        artpgs.setdefault(a, []).append(int(f[0]))
            artistWithMost = ""
            if len(artpgs):
                artpgcmp = [a for a in artpgs if a != 'zz']
                if len(artpgcmp):
                    artistWithMost = max(artpgcmp, key=lambda x: len(set(artpgs[x])))

        langs = set(self.imageCopyrightLangs.keys())
        langs.add("en")
        for lang in sorted(langs):
            crdtsstarted = False
            if os.path.exists(picpagesfile):
                hasOut = False
                mkr = self.imageCopyrightLangs.get(lang, "pc")
                rtl = lang in cinfo['rtl']
                if rtl == (self.dict['document/ifrtl'] == "false"):
                    mkr += "\\begin" + ("R" if rtl else "L")
                crdts.append("\\def\\zimagecopyrights{}{{%".format(lang.lower()))
                crdtsstarted = True
                plstr = cinfo["plurals"].get(lang, cinfo["plurals"]["en"])
                cpytemplate = cinfo['templates']['imageCopyright'].get(lang,
                                        cinfo['templates']['imageCopyright']['en'])
                for art, pgs in artpgs.items():
                    if art != artistWithMost and art != 'zz':
                        if len(pgs):
                            pgs = sorted(set(pgs))
                            plurals = pluralstr(plstr, pgs)
                            artinfo = cinfo["copyrights"].get(art, {'copyright': {'en': art}, 'sensitive': {'en': art}})
                            if artinfo is not None and (art in cinfo['copyrights'] or len(art) > 5):
                                artstr = artinfo["copyright"].get(lang, artinfo["copyright"]["en"])
                                if sensitive and "sensitive" in artinfo:
                                    artstr = artinfo["sensitive"].get(lang, artinfo["sensitive"]["en"])
                                cpystr = multstr(cpytemplate, lang, len(pgs), plurals, artstr.replace("_", "\u00A0"))
                                crdts.append("\\{} {}".format(mkr, cpystr))
                            else:
                                crdts.append(_("\\rem Warning: No copyright statement found for: {} on pages {}")\
                                                .format(art.upper(), pluralstr))
                            hasOut = True
                if len(msngPgs):
                    plurals = pluralstr(plstr, msngPgs)
                    template = cinfo['templates']['imageExceptions'].get(lang,
                                        cinfo['templates']['imageExceptions']['en'])
                    exceptPgs = " " + multstr(template, lang, len(msngPgs), plurals)
                else:
                    exceptPgs = ""

                if len(artistWithMost):
                    artinfo = cinfo["copyrights"].get(artistWithMost, 
                                {'copyright': {'en': artistWithMost}, 'sensitive': {'en': artistWithMost}})
                    if artinfo is not None and (artistWithMost in cinfo["copyrights"] or len(artistWithMost) > 5):
                        pgs = artpgs[artistWithMost]
                        plurals = pluralstr(plstr, pgs)
                        artstr = artinfo["copyright"].get(lang, artinfo["copyright"]["en"])
                        if sensitive and "sensitive" in artinfo:
                            artstr = artinfo["sensitive"].get(lang, artinfo["sensitive"]["en"])
                        if not hasOut:
                            template = cinfo['templates']['allIllustrations'].get(lang,
                                cinfo['templates']['allIllustrations']['en'])
                        else:
                            template = cinfo['templates']['exceptIllustrations'].get(lang,
                                cinfo['templates']['exceptIllustrations']['en'])
                        cpystr = template.format(artstr.replace("_", "\u00A0") + exceptPgs)
                        crdts.append("\\{} {}".format(mkr, cpystr))
            if self.dict['notes/ifxrexternalist']:
                if self.dict['notes/xrlistsource'] == "standard":
                    msg = "\\{} {}".format(mkr, cinfo['templates']['openbible.info'].get(lang,
                                cinfo['templates']['openbible.info']['en']).replace("_", "\u00A0"))
                else:
                    msg = getattr(self, 'xrefcopyright', None)
                if msg is not None:
                    if not crdtsstarted:
                        crdts.append("\\def\\zimagecopyrights{}{{%".format(lang.lower()))
                        crdtsstarted = True
                    crdts.append(msg)
            if crdtsstarted:
                crdts.append("}")
        if len(crdts):
            crdts.append("\\let\\zimagecopyrights=\\zimagecopyrightsen")
        return "\n".join(crdts)

    def _getVerseRanges(self, sfm, bk):
        class Result(list):
            def __init__(self):
                super().__init__(self)
                self.chap = 0

        def process(a, e):
            if isinstance(e, (str, Text)):
                return a
            if e.name == "c":
                a.chap = int(e.args[0])
            elif e.name == "v" and "-" in e.args[0]:
                m = re.match(r"^(\d+)-(\d+)", e.args[0])
                if m is not None:
                    first = int(m.group(1))
                    last = int(m.group(2))
                    a.append(RefRange(Reference(bk, a.chap, first), Reference(bk, a.chap, last)))
            for c in e:
                process(a, c)
            return a
        return reduce(process, sfm, Result())

    def _iterref(self, ra, allrefs):
        curr = ra.first.copy()
        while curr <= ra.last:
            if curr in allrefs:
                yield curr
                curr.verse += 1
            else:
                curr.chap += 1
                curr.verse = 1

    def _addranges(self, results, ranges):
        for ra in ranges:
            acc = RefList()
            for r in self._iterref(ra, results):
                acc.extend(results[r])
                del results[r]
            if len(acc):
                results[ra] = acc

    def createXrefTriggers(self, bk, prjdir, outpath):
        cfilter = self.dict['notes/xrfilterbooks']
        if cfilter == "pub":
            bl = self.printer.get("ecb_booklist", "").split()
            filters = set(bl)
        elif cfilter == "prj":
            filters = set(self.printer.getAllBooks().keys())
        elif cfilter == "all":
            filters = None
        elif cfilter == "ot":
            filters = allbooks[:39]
        elif cfilter == "nt":
            filters = allbooks[40:67]
        if filters is not None and len(filters) == 0:
            filters = None
        if self.dict['notes/xrlistsource'] == "custom":
            self.xrefdat = {}
            # import pdb; pdb.set_trace()
            with open(self.dict['project/selectxrfile']) as inf:
                for l in inf.readlines():
                    if '=' in l:
                        (k, v) = l.split("=", maxsplit=1)
                        if k.strip() == "attribution":
                            self.xrefcopyright = v.strip()
                    v = RefList()
                    for d in re.sub(r"[{}]", "", l).split():
                        v.extend(RefList.fromStr(d.replace(".", " "), marks="+"))
                    k = v.pop(0)
                    self.xrefdat[k] = [v]
        else:       # standard
            if self._crossRefInfo == None:
                def procxref(inf):
                    results = {}
                    for l in inf.readlines():
                        d = l.split("|")
                        v = [RefList.fromStr(s) for s in d]
                        results[v[0][0]] = v[1:]
                    return results
                self.__class__._crossRefInfo = cachedData(os.path.join(os.path.dirname(__file__), "cross_references.txt"), procxref)
            self.xrefdat = self.__class__._crossRefInfo
        results = {}
        for k, v in self.xrefdat.items():
            if k.first.book != bk:
                continue
            outl = v[0]
            if len(v) > 1 and self.dict['notes/xrlistsize'] > 1:
                outl = sum(v[0:self.dict['notes/xrlistsize']], RefList())
            results[k] = outl
        fname = self.printer.getBookFilename(bk)
        if fname is None:
            return
        infpath = os.path.join(prjdir, fname)
        with open(infpath) as inf:
            try:
                sfm = Usfm(inf, self.sheets)
            except:
                sfm = None
            if sfm is not None:
                ranges = self._getVerseRanges(sfm.doc, bk)
                self._addranges(results, ranges)
        class NoBook:
            @classmethod
            def getLocalBook(cls, s, level=0):
                return ""
        def usfmmark(ref, txt):
            if ref.mark == "+":
                return r"\+it {}\+it*".format(txt)
            return txt
        addsep = RefSeparators(books="; ", chaps=";\u200B", verses=",\u200B", bkcv="\u2000", mark=usfmmark)
        dotsep = RefSeparators(cv=".", onechap=True)
        template = "\n\\AddTrigger {book}{dotref}\n\\x - \\xo {colnobook} \\xt {refs}\\x*\n\\EndTrigger\n"
        with open(outpath + ".triggers", "w", encoding="utf-8") as outf:
            for k, v in sorted(results.items()):
                if filters is not None:
                    v.filterBooks(filters)
                v.sort()
                v.simplify()
                if not len(v):
                    continue
                info = {
                    "book":         k.first.book,
                    "dotref":       k.str(context=NoBook, addsep=dotsep),
                    "colnobook":    k.str(context=NoBook),
                    "refs":         v.str(self.ptsettings, addsep=addsep)
                }
                outf.write(template.format(**info))

