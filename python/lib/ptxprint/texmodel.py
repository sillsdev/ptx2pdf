import configparser, re, os, traceback, sys
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
                            chaps, books, bookcodes, allbooks, oneChbooks, asfloat, f2s, cachedData, pycodedir, \
                            runChanges
from ptxprint.dimension import Dimension
import ptxprint.scriptsnippets as scriptsnippets
from ptxprint.interlinear import Interlinear
from ptxprint.reference import Reference, RefRange, RefList, RefSeparators, AnyBooks
from ptxprint.xrefs import Xrefs
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
    "config/gitversion":        ("_gitversion", None),
    "config/name":              ("_cfgid", None),
    "config/filterpics":        ("c_filterPicList", None),
    "config/autosave":          ("c_autoSave", None),

    "project/id":               ("_prjid", None),
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
    "project/when2processscript": ("r_when2processScript", None),
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
    "project/autotaghebgrk":    ("c_autoTagHebGrk", None),
    "project/interlinear":      ("c_interlinear", lambda w,v: "" if v else "%"),
    "project/interlang":        ("t_interlinearLang", None),
    "project/ruby":             ("c_ruby", lambda w,v : "t" if v else "b"),
    "project/plugins":          ("t_plugins", lambda w,v: v or ""),
    "project/license":          ("ecb_licenseText", None),
    "project/copyright":        ("t_copyrightStatement", lambda w,v: re.sub(r"\\u([0-9a-fA-F]{4})",
                                                                   lambda m: chr(int(m.group(1), 16)), v).replace("//", "\u2028") if v is not None else ""),
    "project/iffrontmatter":    ("c_frontmatter", lambda w,v: "" if v else "%"),
    "project/periphpagebreak":  ("c_periphPageBreak", None),
    "project/colophontext":     ("txbf_colophon", lambda w,v: re.sub(r"\\u([0-9a-fA-F]{4})",
                                                                   lambda m: chr(int(m.group(1), 16)), v) if v is not None else ""),
    "project/ifcolophon":       ("c_colophon", lambda w,v: "" if v else "%"),
    "project/pgbreakcolophon":  ("c_standAloneColophon", lambda w,v: "" if v else "%"),
    "project/sectintros":       ("c_useSectIntros", None),

    "paper/height":             ("ecb_pagesize", lambda w,v: re.sub(r"^.*?[,xX]\s*(.+?)\s*(?:\(.*|$)", r"\1", v or "210mm")),
    "paper/width":              ("ecb_pagesize", lambda w,v: re.sub(r"^(.*?)\s*[,xX].*$", r"\1", v or "148mm")),
    "paper/pagesize":           ("ecb_pagesize", None),
    "paper/weight":             ("s_paperWeight", None),
    "paper/thickness":          ("s_paperThickness", None),
    "paper/ifwatermark":        ("c_applyWatermark", lambda w,v: "" if v else "%"),
    "paper/watermarkpdf":       ("btn_selectWatermarkPDF", lambda w,v: w.watermarks.as_posix() \
                                 if (w.get("c_applyWatermark") and w.watermarks is not None and w.watermarks != 'None') else ""),
    "paper/cropmarks":          ("c_cropmarks", None),  
    "paper/ifgrid":             ("c_grid", lambda w,v :"" if v else "%"),
    "paper/ifverticalrule":     ("c_verticalrule", lambda w,v :"true" if v else "false"),
    "paper/margins":            ("s_margins", lambda w,v: round(float(v)) if v else "12"),
    "paper/topmargin":          ("s_topmargin", None),
    "paper/bottommargin":       ("s_bottommargin", None),
    "paper/headerpos":          ("s_headerposition", None),
    "paper/footerpos":          ("s_footerposition", None),
    "paper/rulegap":            ("s_rhruleposition", None),

    "paper/ifaddgutter":        ("c_pagegutter", lambda w,v :"true" if v else "false"),
    "paper/ifoutergutter":      ("c_outerGutter", lambda w,v :"true" if v else "false"),
    "paper/gutter":             ("s_pagegutter", lambda w,v: round(float(v)) if v else "0"),
    "paper/colgutteroffset":    ("s_colgutteroffset", lambda w,v: "{:.1f}".format(float(v)) if v else "0.0"),
    "paper/columns":            ("c_doublecolumn", lambda w,v: "2" if v else "1"),
    "paper/bottomrag":          ("s_bottomRag", None),
    "paper/fontfactor":         ("s_fontsize", lambda w,v: f2s(float(v) / 12, dp=8) if v else "1.000"),
    "paper/lockfont2baseline":  ("c_lockFontSize2Baseline", None),

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
    "paragraph/linespacebase":     ("c_AdvCompatLineSpacing", lambda w,v: 14 if v else 12),
    "paragraph/useglyphmetrics":   ("c_AdvCompatGlyphMetrics", lambda w,v: "%" if v else ""),
    "paragraph/ifjustify":      ("c_justify", lambda w,v: "true" if v else "false"),
    "paragraph/ifhyphenate":    ("c_hyphenate", lambda w,v: "" if v else "%"),
    "paragraph/ifomithyphen":   ("c_omitHyphen", lambda w,v: "" if v else "%"),
    "paragraph/ifhyphlimitbks": ("c_hyphenLimitBooks", None),
    "paragraph/ifsylhyphens":   ("c_addSyllableBasedHyphens", None),
    "paragraph/ifnothyphenate": ("c_hyphenate", lambda w,v: "%" if v else ""),
    "paragraph/ifusefallback":  ("c_useFallbackFont", None),
    "paragraph/missingchars":   ("t_missingChars", lambda w,v: v or ""),

    "document/sensitive":       ("c_sensitive", None),
    "document/title":           (None, lambda w,v: "[Unknown]" if w.get("c_sensitive") else w.ptsettings.get('FullName', "[Unknown]")),
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
    "document/chapfrom":        ("t_chapfrom", lambda w,v: str(round(float(v))) if v else "1"),
    "document/chapto":          ("t_chapto", lambda w,v: str(round(float(v))) if v else "999"),
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
    "document/ifshowversenums": ("c_verseNumbers", lambda w,v: "" if v else "%"),
    "document/afterchapterspace": ("s_afterChapterSpace", lambda w,v: f2s(asfloat(v, 0.25) * 12)),
    "document/afterversespace": ("s_afterVerseSpace", lambda w,v: f2s(asfloat(v, 0.15) * 12)),
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
    "document/diffcolayout":        ("c_differentColLayout", None),
    "document/diffcolayoutbooks":   ("t_differentColBookList", None),
    "document/cloptimizepoetry":    ("c_optimizePoetryLayout", None),

    "document/ifdiglot":            ("c_diglot", lambda w,v : "" if v else "%"),
    "document/diglotprifraction":   ("s_diglotPriFraction", lambda w,v : round((float(v)/100), 3) if v is not None else "0.550"),
    "document/diglotsecfraction":   ("s_diglotPriFraction", lambda w,v : round(1 - (float(v)/100), 3) if v is not None else "0.450"),
    "document/diglotsecprj":        ("fcb_diglotSecProject", None),
    "document/diglotpicsources":    ("fcb_diglotPicListSources", None),
    "document/diglot2captions": ("c_diglot2captions", None),
    "document/diglotswapside":  ("c_diglotSwapSide", lambda w,v: "true" if v else "false"),
    "document/diglotsepnotes":  ("c_diglotSeparateNotes", lambda w,v: "true" if v else "false"),
    "document/diglotsecconfig": ("ecb_diglotSecConfig", None),
    "document/diglotmergemode": ("c_diglotMerge", lambda w,v: "simple" if v else "doc"),
    "document/diglotadjcenter": ("c_diglotAdjCenter", None),
    "document/diglotheaders":   ("c_diglotHeaders", None),
    "document/diglotnotesrule": ("c_diglotNotesRule", lambda w,v: "true" if v else "false"),
    "document/diglotjoinvrule": ("c_diglotJoinVrule", lambda w,v: "true" if v else "false"),

    "document/hasnofront_":        ("c_frontmatter", lambda w,v: "%" if v else ""),
    "document/noblankpage":        ("c_periphSuppressPage", None),
    "document/cutouterpadding":    ("s_cutouterpadding", None),
    "document/underlinethickness": ("s_underlineThickness", lambda w,v: float(v or "0.05")),
    "document/underlineposition":  ("s_underlinePosition", lambda w,v: float(v or "-0.1")),
    "document/pagefullfactor":     ("s_pageFullFactor", lambda w,v: float(v or "0.65")),
    
    "document/onlyshowdiffs":   ("c_onlyDiffs", None),
    "document/diffcolor":       ("col_diffColor", None),
    "document/diffpdf":         ("btn_selectDiffPDF", lambda w,v: w.diffPDF.as_posix() \
                                 if (w.diffPDF is not None and w.diffPDF != 'None') else ""),
    "document/printarchive":    ("c_printArchive", None),

    "document/keepversions":    ("s_keepVersions", None),
    "document/settingsinpdf":   ("c_inclSettingsInPDF", None),
    "document/spinethickness":  ("s_spineThickness", None),
    "document/rotatespinetext": ("fcb_rotateSpineText", None),
    
    "finishing/pgsperspread":   ("fcb_pagesPerSpread", None),
    "finishing/scaletofit":     ("c_scaleToFit", None),
    "finishing/sheetsize":      ("ecb_sheetSize", None),
    "finishing/sheetsinsigntr": ("s_sheetsPerSignature", None),
    "finishing/foldcutmargin":  ("s_foldCutMargin", None),
    "finishing/inclsettings":   ("c_inclSettingsInPDF", None),
    "finishing/spotcolor":      ("col_spotColor", None),
    "finishing/spottolerance":  ("s_spotColorTolerance", None),
    
    "header/ifshowbook":        ("c_rangeShowBook", lambda w,v :"false" if v else "true"),
    "header/ifshowchapter":     ("c_rangeShowChapter", lambda w,v :"false" if v else "true"),
    "header/ifshowverse":       ("c_rangeShowVerse", lambda w,v :"true" if v else "false"),
    "header/chvseparator":      ("r_CVsep", lambda w,v : ":" if v == "colon" else "."),
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
    "footer/noinkinmargin":     ("c_AdvCompatFtrInMargin", lambda w,v :"false" if v else "true"),
    "notes/frverseonly":        ("c_frVerseOnly", None),

    "notes/includefootnotes":   ("c_includeFootnotes", lambda w,v: "%" if v else ""),
    "notes/fneachnewline":      ("c_fneachnewline", lambda w,v: "%" if v else ""),
    "notes/fnoverride":         ("c_fnOverride", None),
    "notes/iffnautocallers":    ("c_fnautocallers", lambda w,v :"true" if v else "false"),
    "notes/fncallers":          ("t_fncallers", lambda w,v: v if w.get("c_fnautocallers") else ""),
    "notes/fnresetcallers":     ("c_fnpageresetcallers", lambda w,v: "" if v else "%"),
    "notes/fnomitcaller":       ("c_fnomitcaller", lambda w,v: "%" if v else ""),

    "notes/includexrefs":       ("c_includeXrefs", lambda w,v: "%" if v else ""),
    "notes/showextxrefs":       ("c_extendedXrefs", None),
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
    "notes/xrcolalign":         ("c_xrSideAlign", lambda w,v: "true" if v else "false"),
    "notes/ifxrexternalist":    ("c_useXrefList", lambda w,v: "%" if v else ""),
    "notes/xrlistsource":       ("fcb_xRefExtListSource", None),
    "notes/xrextlistsource":    ("fcb_xRefExtListSource", None),
    "notes/xrfilterbooks":      ("fcb_filterXrefs", None),
    "notes/xrverseonly":        ("c_xoVerseOnly", None),
    "notes/addcolon":           ("c_addColon", None),
    "notes/keepbookwithrefs":   ("c_keepBookWithRefs", None),
    "notes/glossaryfootnotes":  ("c_glossaryFootnotes", None),
    "notes/fnpos":              ("r_fnpos", None),
    "notes/columnnotes_":       ("r_fnpos", lambda w,v: "true" if v == "column" else "false"),
    "notes/endnotes_":          ("r_fnpos", lambda w,v: "" if v == "endnotes" else "%"),

    "notes/iffootnoterule":     ("c_footnoterule", lambda w,v: "%" if v else ""),
    "notes/ifxrefrule":         ("c_xrefrule", lambda w,v: "%" if v else ""),
    "notes/ifstudynoterule":    ("c_studynoterule", lambda w,v: "%" if v else ""),

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

    "notes/snruleposn":         ("fcb_snHorizPosn", None),
    "notes/snruleindent":       ("s_snIndent", None),
    "notes/snrulethick":        ("s_snThick", None),
    "notes/snrulelength":       ("s_snLength", None),
    "notes/belowstudyrulespace": ("s_snBelowSpace", None),
    "notes/abovestudyspace":    ("s_snAboveSpace", None),
    
    "notes/internotespace":     ("s_internote", lambda w,v: f2s(float(v or 3))),

    "notes/horiznotespacemin":  ("s_notespacingmin", lambda w,v: f2s(float(v)) if v is not None else "7"),
    "notes/horiznotespacemax":  ("s_notespacingmax", lambda w,v: f2s(float(v)) if v is not None else "27"),

    "studynotes/includextfn":     ("c_extendedFnotes", lambda w,v: "" if v else "%"),
    "studynotes/showcallers":     ("c_ef_showCallers", lambda w,v: "%" if v else ""),
    "studynotes/colgutterfactor": ("s_ef_colgutterfactor", lambda w,v: round(float(v or 4)*3)), # Hack to be fixed?
    "studynotes/ifverticalrule":  ("c_ef_verticalrule", lambda w,v :"true" if v else "false"),
    "studynotes/internote":       ("s_ef_internote", lambda w,v: "{:.1f}".format(float(v)) if v else "0.0"),
    "studynotes/colgutteroffset": ("s_ef_colgutteroffset", lambda w,v: "{:.1f}".format(float(v)) if v else "0.0"),
  # "studynotes/bottomrag":       ("s_ef_bottomRag", lambda w,v: str(int(v or 0)+0.95)),
    "studynotes/includesidebar":  ("c_sidebars", None),
    "studynotes/filtercats":      ("c_filterCats", None),

    "document/fontregular":     ("bl_fontR", lambda w,v,s: v.asTeXFont(s.inArchive) if v else ""),
    "document/fontbold":        ("bl_fontB", lambda w,v,s: v.asTeXFont(s.inArchive) if v else ""),
    "document/fontitalic":      ("bl_fontI", lambda w,v,s: v.asTeXFont(s.inArchive) if v else ""),
    "document/fontbolditalic":  ("bl_fontBI", lambda w,v,s: v.asTeXFont(s.inArchive) if v else ""),
    "document/fontextraregular":("bl_fontExtraR", lambda w,v,s: v.asTeXFont(s.inArchive) if v else ""),

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
    "thumbtabs/thumbtextmkr":   ("r_thumbText", None),
    "thumbtabs/restart":        ("c_thumbrestart", None),
    "thumbtabs/groups":         ("t_thumbgroups", None),

    "scripts/mymr/syllables":   ("c_scrmymrSyllable", None),
    "scripts/arab/lrcolon":     ("c_scrarabrefs", None),
    "scripts/indic/syllables":  ("c_scrindicSyllable", None),
    "scripts/indic/showhyphen": ("c_scrindicshowhyphen", None),

    "strongsndx/showintext":    ("c_strongsShowInText", None),
    "strongsndx/showall":       ("c_strongsShowAll", None),
    "strongsndx/shownums":      ("c_strongsShowNums", None),
    "strongsndx/showhebrew":    ("c_strongsHeb", None),
    "strongsndx/showgreek":     ("c_strongsGrk", None),
    "strongsndx/showindex":     ("c_strongsNdx", None),
    "strongsndx/sourcelang":    ("c_strongsSrcLg", None),
    "strongsndx/transliterate": ("c_strongsTranslit", None),
    "strongsndx/renderings":    ("c_strongsRenderings", None),
    "strongsndx/definitions":   ("c_strongsDefn", None),
    "strongsndx/keyvrsrefs":    ("c_strongsKeyVref", None),
    "strongsndx/fallbackprj":   ("fcb_strongsFallbackProj", None),
    "strongsndx/majorlang":     ("fcb_strongsMajorLg", None),
    "strongsndx/nocomments":    ("c_strongsNoComments", None),
    "strongsndx/wildcards":     ("fcb_strongswildcards", None),
    "strongsndx/raglines":      ("s_strongRag", None),
    "strongsndx/ndxbookid":     ("fcb_strongsNdxBookId", None),
    "strongsndx/twocols":       ("c_strongs2cols", None),
    "strongsndx/openineditor":  ("c_strongsOpenIndex", None),
    
    "color/spotcolrange":       ("s_spotColorTolerance", None),
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
    _bookinserts = (("GEN-REV", "intbible"), ("GEN-MAL", "intot"), ("GEN-DEU", "intpent"), ("JOS-EST", "inthistory"),
                    ("JOB-SNG", "intpoetry"), ("ISA-MAL", "intprophecy"), ("TOB-LAO", "intdc"), 
                    ("MAT-REV", "intnt"), ("MAT-JHN", "intgospel"), ("ROM-PHM", "intepistles"), ("HEB-REV", "intletters"))
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
        "ai": r"\1",                # "As is (pass|through)":                    
        "no": r"\1",                # "None":                    
        None: r"\1",                # None:                      
        "bd": r"\\bd \1\\bd*",      # "format as bold":          
        "it": r"\\it \1\\it*",      # "format as italics":       
        "bi": r"\\bdit \1\\bdit*",  # "format as bold italics":  
        "em": r"\\em \1\\em*",      # "format with emphasis":    
        "ww":  r"\\w \1\\w*",       # "\w ...\w* char style":  
        # Note that these glossary markers can be styled with \zglm 
        # But this doesn't work if fallback font is turned on for these chars
        "fb": r"\\zglm \u2E24\\zglm*\1\\zglm \u2E25\\zglm*",    # "with ⸤floor⸥ brackets":   
        "fc": r"\\zglm \u230a\\zglm*\1\\zglm \u230b\\zglm*",    # "with ⌊floor⌋ characters": 
        "cc": r"\\zglm \u231e\\zglm*\1\\zglm \u231f\\zglm*",    # "with ⌞corner⌟ characters":
        "sb": r"*\1",               # "star *before word":       
        "sa": r"\1*",               # "star after* word":        
        "cb": r"^\1",               # "circumflex ^before word": 
        "ca":  r"\1^"               # "circumflex after^ word":  
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

    _specialchars = {
        '*': 'asterisk',
        '%': 'percent',
        '#': 'hash',
        '$': 'dollar',
        '&': 'ampersand',
        '^': 'circumflex'
    }
        # '|': 'pipe'

    def __init__(self, printer, path, ptsettings, prjid=None, inArchive=False):
        from ptxprint.view import VersionStr, GitVersionStr
        self.VersionStr = VersionStr
        self.GitVersionStr = GitVersionStr
        self.printer = printer
        self.ptsettings = ptsettings
        self.inArchive = inArchive
        self.changes = None
        self.localChanges = None
        self.debug = False
        self.interlinear = None
        self.imageCopyrightLangs = {}
        self.frontperiphs = None
        self.xrefs = None
        self.inserts = {}
        self.usedfiles = {}
        libpath = pycodedir()
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
        base = os.path.join(self.dict["/ptxpath"], self.dict["project/id"])
        docdir = os.path.join(base, 'local', 'ptxprint', self.printer.configName())
        return docdir, base

    def update(self):
        """ Update model from UI """
        j = os.path.join
        rel = lambda x, y:os.path.relpath(x, y).replace("\\", "/")
        self.printer.setDate()  # Update date/time to now
        cpath = self.printer.configPath(self.printer.configName())
        rcpath = self.printer.configPath("")
        self.updatefields(ModelMap.keys())
        self.dict['project/id'] = self.printer.prjid
        docdir, base = self.docdir()
        self.dict["document/directory"] = "." # os.path.abspath(docdir).replace("\\","/")
        self.dict['project/adjlists'] = rel(j(cpath, "AdjLists"), docdir).replace("\\","/") + "/"
        self.dict['project/triggers'] = rel(j(cpath, "triggers"), docdir).replace("\\","/") + "/"
        self.dict['project/piclists'] = rel(j(self.printer.working_dir, "tmpPicLists"), docdir).replace("\\","/") + "/"
        self.dict['config/name'] = self.printer.configId
        self.dict['/ptxrpath'] = rel(self.dict['/ptxpath'], docdir)
        self.dict['/cfgrpath'] = rel(cpath, docdir)
        self.dict['/ptxprint_version'] = self.VersionStr
        self.dict['/ptxprint_gitversion'] = self.GitVersionStr
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
        self.dict['notes/abovenotetotal'] = f2s(float(self.dict['notes/abovenotespace'] or 0)
                                                          + float(self.dict['notes/belownoterulespace'] or 0))
        # print(", ".join("{}={}".format(a, self.dict["fancy/versedecorator"+a]) for a in ("", "type", "isfile", "isayah")))
        
        a = self.printer.get('fcb_gridOffset')
        if a == 'margin':
            vals = (self.dict["paper/margins"], self.dict["paper/topmargin"])
        else:
            vals = ("0.0", "0.0")
        (self.dict["grid/xoffset_"], self.dict["grid/yoffset_"]) = vals
        for a in ('project/frontfile', 'project/ptxprintstyfile_', 'diglot/ptxprintstyfile_'):
            if a not in self.dict:
                self.dict[a] = ''

        if self.dict.get('paper/cropmarks', False) and int(self.dict.get('finishing/pgsperspread', 1)) < 2:
            self.dict['paper/ifcropmarks'] = "true"
        else:
            self.dict['paper/ifcropmarks'] = "false"
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
        notemap = {'fn': 'note', 'xr': 'xref', 'sn': 'study'}
        fnrule = None
        enrule = None
        endnotes = []
        for a in ('fn', 'xr'):
            if self.dict['notes/{}pos'.format(a)] == 'endnote':
                enrule = a if enrule is None else enrule
                endnotes.append(r"\NoteAtEnd{{{}}}".format(a[0]))
            elif fnrule is None:
                fnrule = a
        for a in (('Foot', fnrule), ('End', enrule), ('Study', 'sn')):
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
                dat.append(r"\Above{}NoteSpace={:.1f} pt".format(a[0] if a[0] != "Foot" else "", aspace))
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
        if self.dict['footer/ifftrtitlepagenum'] == "":
            self.dict['footer/titleevencenter'] = self.dict['footer/titleoddcenter'] = self._addLR('\\pagenumber', pri)
        elif self.dict['footer/ifprintconfigname'] == "":
            self.dict['footer/titleevencenter'] = self.dict['footer/titleoddcenter'] = self.dict['config/name']
        else:
            self.dict['footer/titleevencenter'] = self.dict['footer/evencenter']
            self.dict['footer/titleoddcenter'] = self.dict['footer/oddcenter']

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

            if side == "center" and diglot and self.dict["document/diglotadjcenter"]:
                for a in ('header/odd', 'header/even', 'footer/odd', 'footer/even',
                          'footer/titleeven', 'footer/titleodd', 'header/noVeven', 'header/noVodd'):
                    b = (a+"{}").format(side)
                    if 'even' in a:
                        self.dict[b] = (rhfil if mirror ^ swap else lhfil) \
                                    + self.dict[b] + (lhfil if mirror ^ swap else rhfil)
                    else:
                        self.dict[b] = (rhfil if swap else lhfil) + self.dict[b] + (lhfil if swap else rhfil)

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

    def _getinsert(self, bk):
        res = []
        bki = bookcodes.get(bk, 200)
        for b, i in self._bookinserts:
            r = [bookcodes[s] for s in b.split("-")]
            if i not in self.inserts and r[0] <= bki <= r[1]:
                self.inserts[i] = bk
                t = self._doperiph(i)
                if t != "":
                    res.append(t)
        return "\n".join(res)

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
        self.dict['project/colophontext'] = re.sub(r'://', r':/ / ', self.dict['project/colophontext']).replace("//","\u2028")
        self.dict['project/colophontext'] = re.sub(r"(?i)(\\zimagecopyrights)([A-Z]{2,3})", \
                lambda m:m.group(0).lower(), self.dict['project/colophontext'])
        with universalopen(os.path.join(pycodedir(), template)) as inf:
            for l in inf.readlines():
                if l.startswith(r"%\ptxfile"):
                    res.append(r"\PtxFilePath={"+os.path.relpath(filedir, docdir).replace("\\","/")+"/}")
                    for i, f in enumerate(self.dict['project/bookids']):
                        fname = self.dict['project/books'][i]
                        if self.dict.get('project/sectintros'):
                            inserttext = self._getinsert(f)
                            if len(inserttext):
                                res.append(r"\prepusfm\n{}\unprepusfm\n".format(inserttext))
                        if extra != "":
                            fname = re.sub(r"^([^.]*).(.*)$", r"\1"+extra+r".\2", fname)
                        if i == len(self.dict['project/bookids']) - 1 and self.dict['project/ifcolophon'] == "":
                            res.append(r"\lastptxfiletrue")
                            if self.dict['project/pgbreakcolophon'] != '%':
                                res.append(r"\endbooknoejecttrue")
                        if not resetPageDone and f not in self._peripheralBooks: 
                            if not self.dict['document/noblankpage']:
                                res.append(r"\ifodd\pageno\else\emptyoutput \fi")
                            res.append(r"\pageno={}".format(self.dict['document/startpagenum']))
                            resetPageDone = True
                        if not self.asBool('document/ifshow1chbooknum') and \
                           self.asBool('document/ifshowchapternums', '%') and \
                           f in oneChbooks:
                            res.append(r"\OmitChapterNumbertrue")
                            res.append(r"\ptxfile{{{}}}".format(fname))
                            res.append(r"\OmitChapterNumberfalse")
                        elif self.dict['document/diffcolayout'] and \
                                    f in self.dict['document/diffcolayoutbooks']:
                            cols = self.dict['paper/columns']
                            res.append(r"\BodyColumns={}".format('2' if cols == '1' else '1'))
                            res.append(r"\ptxfile{{{}}}".format(fname))
                            res.append(r"\BodyColumns={}".format(cols))
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
                        res.append(r"\activ@tecustomch@rs")
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
                            res.append(sclass.tex(self.printer))
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
                    for k, e in (('toctitle', 'document/toctitle'),):
                        res.append(r"\defzvar{{{}}}{{{}}}".format(k, self.dict[e]))
                else:
                    res.append(l.rstrip().format(**self.dict))
        return "\n".join(res).replace("\\OmitChapterNumberfalse\n\\OmitChapterNumbertrue\n","")

    def _doperiph(self, k):
        if self.frontperiphs is None:
            for a in ('FRT', 'INT'):
                frtfile = os.path.join(self.printer.settings_dir, self.printer.prjid, self.printer.getBookFilename(a))
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
        return self.frontperiphs.get(k, "")

    def createFrontMatter(self, outfname):
        self.dict['project/frontfile'] = os.path.basename(outfname)
        infpath = self.printer.configFRT()
        bydir = os.path.join(pycodedir(), "images").replace("\\", "/")
        fmt = self.dict['snippets/pdfoutput']
        cmyk = fmt in ('CMYK', 'PDF/X-1A', 'PDF/A-1')
        if os.path.exists(infpath):
            fcontent = []
            with open(infpath, encoding="utf-8") as inf:
                seenperiph = False
                for l in inf.readlines():
                    if l.strip().startswith(r"\periph"):
                        l = r"\pb" if self.dict['project/periphpagebreak'] and seenperiph else ""
                        seenperiph = True
                    l = re.sub(r"\\zgetperiph\s*\|([^\\\s]+)\s*\\\*", lambda m:self._doperiph(m[1]), l)
                    l = re.sub(r"\\zbl\s*\|(\d+)\\\*", lambda m: "\\b\n" * int(m.group(1)), l)
                    l = re.sub(r"\\zccimg\s*(.*?)(?:\|(.*?))?\\\*",
                            lambda m: r'\fig |src="'+bydir+"/"+m.group(1)+("_cmyk" if cmyk else "") \
                                     + '.jpg" copy="None" ' + m.group(2)+ r'\fig*', l)
                    l = re.sub(r'(\\fig .*?src=")(.*?)(".*?\\fig\*)', lambda m:m.group(1)+m.group(2).replace("\\","/")+m.group(3), l)
                    fcontent.append(l.rstrip())
            with open(outfname, "w", encoding="utf-8") as outf:
                outf.write("\n".join(fcontent))

    def flattenModule(self, infpath, outdir, usfm=None):
        outfpath = os.path.join(outdir, os.path.basename(infpath))
        doti = outfpath.rfind(".")
        if doti > 0:
            outfpath = outfpath[:doti] + "-flat" + outfpath[doti:]
        usfms = self.printer.get_usfms()
        try:
            mod = Module(infpath, usfms, self, usfm=usfm)
            res = mod.parse()
        except SyntaxError as e:
            return (None, e)
        if usfm is not None:
            return res
        with open(outfpath, "w", encoding="utf-8") as outf:
            outf.write(sfm.generate(res))
        return outfpath

    def runConversion(self, infpath, outdir):
        outfpath = infpath
        script = self.dict['project/selectscript']
        if self.dict['project/processscript'] and script:
            outfpath = os.path.join(outdir, os.path.basename(infpath))
            doti = outfpath.rfind(".")
            if doti > 0:
                outfpath = outfpath[:doti] + "-conv" + outfpath[doti:]
            cmd = [script, infpath, outfpath]
            if script.lower().endswith(".bat") and sys.platform == "win32":
                cmd = [os.environ.get('COMSPEC', 'cmd.exe'), '/c'] + cmd
            else:
                hasrun = False
                with open(script, encoding="utf-8") as scriptf:
                    l = scriptf.readline().replace("\uFEFF", "")
                    if script.lower().endswith(".py") or re.match(r"^#!.*?(?<=[ /!])python", l):
                        scriptf.seek(0)
                        sys._argv = sys.argv
                        sys.argv = [script, infpath, outfpath]
                        exec(scriptf.read())
                        sys.argv = sys._argv
                        hasrun = True
                if not hasrun:
                    checkoutput(cmd) # dont't pass cmd as list when shell=True
        return outfpath

    def convertBook(self, bk, chaprange, outdir, prjdir, isbk=True, letterspace="\uFDD0"):
        try:
            isCanon = int(bookcodes.get(bk, 100)) < 89
        except ValueError:
            isCanon = False
        printer = self.printer
        if self.changes is None:
            if self.asBool('project/usechangesfile'):
                # print("Applying PrntDrftChgs:", os.path.join(prjdir, 'PrintDraftChanges.txt'))
                #cpath = self.printer.configPath(self.printer.configName())
                #self.changes = self.readChanges(os.path.join(cpath, 'changes.txt'), bk)
                self.changes = self.readChanges(os.path.join(printer.configPath(printer.configName()), 'changes.txt'), bk)
            else:
                self.changes = []
        draft = "-" + (printer.configName() or "draft")
        self.makelocalChanges(printer, bk, chaprange=(chaprange if isbk else None))
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
        if self.dict['project/when2processscript'] == "before":
            infpath = self.runConversion(infpath, outdir)
        outfname = os.path.basename(infpath)
        outindex = self.usedfiles.setdefault(outfname, 0)
        outextra = str(outindex) if outindex > 0 else ""
        self.usedfiles[outfname] = outindex + 1
        # outfname = fname
        doti = outfname.rfind(".")
        if doti > 0:
            outfname = outfname[:doti] + draft + outextra + outfname[doti:]
        os.makedirs(outdir, exist_ok=True)
        outfpath = os.path.join(outdir, outfname)
        codepage = self.ptsettings.get('Encoding', 65001)
        with universalopen(infpath, cp=codepage) as inf:
            dat = inf.read()

        doc = None
        if chaprange is None and self.dict["project/bookscope"] == "single":
            chaprange = RefList((RefRange(Reference(bk, int(float(self.dict["document/chapfrom"])), 0),
                                 Reference(bk, int(float(self.dict["document/chapto"])), 200)), ))

        logger.debug(f"Converting {bk} {chaprange=}")
        if chaprange is None or not isbk or not len(chaprange) or \
            (chaprange[0].first.chap < 2 and len(chaprange) == 1 and \
                (chaprange[0].last.chap >= int(chaps[bk]) or chaprange[0].last.chap == 0)):
            doc = None
        else:
            doc = self._makeUSFM(dat.splitlines(True), bk)
            if doc is not None:
                doc = doc.getsubbook(chaprange)

        if self.interlinear is not None:
            if doc is None:
                doc = self._makeUSFM(dat.splitlines(True), bk)
            linelengths = [len(x) for x in dat.splitlines(True)]
            if doc is not None:
                doc.calc_PToffsets()
                self.interlinear.convertBk(bk, doc, linelengths)
                if len(self.interlinear.fails):
                    refs = RefList(self.interlinear.fails)
                    refs.simplify()
                    printer.doError("The following references need to be reapproved: " + str(refs),
                                    show=not printer.get("c_quickRun"))
                    self.interlinear.fails = []
        elif bk.lower().startswith("xx"):
            if doc is None:
                doc = self._makeUSFM(dat.splitlines(True), bk)
            if doc is not None:
                doc.doc = self.flattenModule(infpath, outfpath, usfm=doc)

        if self.changes is not None and len(self.changes):
            if doc is not None:
                dat = str(doc)
                logger.log(5, "Unparsing text to run user changes\n"+dat)
                doc = None
            dat = runChanges(self.changes, bk, dat)
            #self.analyzeImageCopyrights(dat)

        if self.dict['project/canonicalise'] \
                    or not self.asBool("document/bookintro") \
                    or not self.asBool("document/introoutline")\
                    or self.asBool("document/hidemptyverses"):
            if doc is None:
                doc = self._makeUSFM(dat.splitlines(True), bk)
            if doc is not None:
                if not self.asBool("document/bookintro") or not self.asBool("document/introoutline"):
                    logger.debug("stripIntro")
                    doc.stripIntro(not self.asBool("document/bookintro"), not self.asBool("document/introoutline"))
                if self.asBool("document/hidemptyverses"):
                    logger.debug("stripEmptyChVs")
                    doc.stripEmptyChVs(ellipsis=self.asBool("document/elipsizemptyvs"))

        if self.dict['fancy/endayah'] == "":
            if doc is None:
                doc = self._makeUSFM(dat.splitlines(True), bk)
            logger.debug("versesToEnd")
            doc.versesToEnd()

        if self.dict["strongsndx/showintext"] and self.dict["notes/xrlistsource"].startswith("strongs") \
                    and self.dict["notes/ifxrexternalist"] and isCanon:
            if doc is None:
                doc = self._makeUSFM(dat.splitlines(True), bk)
            logger.debug("Add strongs numbers to text")
            doc.addStrongs(printer.getStrongs(), self.dict["strongsndx/showall"])
            
        if doc is not None and getattr(doc, 'doc', None) is not None:
            dat = str(doc)
            logger.log(5, "Unparsing text to run local changes\n"+dat)

        if self.localChanges is not None:
            dat = runChanges(self.localChanges, bk, dat)

        with open(outfpath, "w", encoding="utf-8") as outf:
            outf.write(dat)
        if self.dict['project/when2processscript'] == "after":
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
        # import pdb; pdb.set_trace()
        syntaxErrors = []
        try:
            doc = Usfm(txtlines, self.sheets)
            while len(doc.doc) > 1:
                if isinstance(doc.doc[0], sfm.Text):
                    doc.doc.pop(0)
                else:
                    break
            if len(doc.doc) != 1:
                raise ValueError("Badly formed USFM. Probably missing a \\id line")
            doc.normalise()
        except SyntaxError as e:
            syntaxErrors.append("{} {} line:{}".format(self.prjid, bk, str(e).split('line', maxsplit=1)[1]))
        except Exception as e:
            syntaxErrors.append("{} {} Error({}): {}".format(self.prjid, bk, type(e), str(e)))
            traceback.print_exc()
        if len(syntaxErrors):
            dlgtitle = "PTXprint [{}] - USFM Text Error!".format(self.VersionStr)
            # print(syntaxErrors[0])
            # logger.info(syntaxErrors[0])
            errbits = re.match(r"(\S+) (...) line: (\d+),\d+\s*\[(.*?)\]: orphan marker (\\.+?)", syntaxErrors[0])
            if errbits is not None:
                self.printer.doError("Syntax Error warning: ",        
                    secondary=_("Examine line {} in {} on the 'Final SFM' tab of the View+Edit " + \
                        "page to determine the cause of this issue related to marker: {} as found in the markers: {}.").format(
                                errbits[3], errbits[2], errbits[5], errbits[4]) + \
                        "\n\n"+_("This warning was triggered due to 'Auto-Correct USFM' being " + \
                        "enabled on the Advanced tab but is due to an orphaned marker. " + \
                        "It means the marker does not belong in that position, or it " + \
                        "is missing a valid parent marker."), title=dlgtitle,
                        show=not self.printer.get("c_quickRun"))
            else:
                prtDrft = _("And check if a faulty rule in changes.txt has caused the error(s).") if self.asBool("project/usechangesfile") else ""
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
                m = re.match(r"^\s*include\s+(['\"])(.*?)\1", l)
                if m:
                    changes.extend(self.readChanges(os.path.join(os.path.dirname(fname), m.group(2)), bk))
                    continue
                # test for "at" command
                m = re.match(r"^\s*at\s+(.*?)\s+(?=in|['\"])", l)
                if m:
                    atref = RefList.fromStr(m.group(1), context=AnyBooks)
                    for r in atref.allrefs():
                        if r.chap == 0:
                            atcontexts.append((r.book, None))
                        elif r.verse == 0:
                            atcontexts.append((r.book, regex.compile(r"(?<=\\c {}\D).*?(?=$|\\[cv]\s)".format(r.chap), flags=regex.S)))
                        else:
                            atcontexts.append((r.book, regex.compile(r"\\c {}\D(?:[^\\]|\\(?!c\s))*?\K\\v {}\D.*?(?=$|\\[cv]\s)".format(r.chap, r.verse), flags=regex.S|regex.V1)))
                    l = l[m.end():].strip()
                else:
                    atcontexts = [None]
                # test for 1+ "in" commands
                while True:
                    m = re.match(r"^\s*in\s+"+qreg+r"\s*:\s*", l)
                    if not m:
                        break
                    try:
                        contexts.append(regex.compile(m.group(1) or m.group(2), flags=regex.M))
                    except re.error as e:
                        self.printer.doError("Regular expression error: {} in changes file at line {}".format(str(e), i+1),
                                             show=not self.printer.get("c_quickRun"))
                        break
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
                        try:
                            changes.append((context, regex.compile(m.group(1) or m.group(2), flags=regex.M),
                                        m.group(3) or m.group(4) or ""))
                        except re.error as e:
                            self.printer.doError("Regular expression error: {} in changes file at line {}".format(str(e), i+1),
                                                 show=not self.printer.get("c_quickRun"))
                            break
                    continue
        return changes

    def makelocalChanges(self, printer, bk, chaprange=None):
        #self.changes.append((None, regex.compile(r"(?<=\\[^\\\s]+)\*(?=\S)", flags=regex.S), "* "))
        if self.printer is not None and self.printer.get("c_tracing"):
            print("List of changes.txt:-------------------------------------------------------------")
            report = "\n".join("{} -> {}".format(p[1].pattern, p[2]) for p in self.changes)
            if getattr(self.printer, "logger", None) is not None:
                self.printer.logger.insert_at_cursor(v)
            else:
                try:
                    print(report)
                except UnicodeEncodeError:
                    print("Unable to print details of changes.txt")
        self.localChanges = []
        script = self.dict["document/script"]
        if len(script):
            sscript = getattr(scriptsnippets, script[8:].lower(), None)
            if sscript is not None:
                self.localChanges.extend(sscript.regexes(self.printer))
        if bk == "GLO" and self.dict['document/filterglossary']:
            self.filterGlossary(printer)
        
        # Fix things that other parsers accept and we don't
        self.localChanges.append((None, regex.compile(r"(\\[cv] [^ \\\r\n]+)(\\)", flags=regex.S), r"\1 \2"))
        
        # Remove empty \h markers (might need to expand this list and loop through a bunch of markers)
        self.localChanges.append((None, regex.compile(r"(\\h ?\r?\n)", flags=regex.S), r""))
        
        # This section handles PARTIAL books (from chapter X to chapter Y)
        if self.asBool("document/ifchaplabels", true="%"):
            clabel = self.dict["document/clabel"]
            clbooks = self.dict["document/clabelbooks"].split()
            if len(clabel) and (not len(clbooks) or bk in clbooks):
                self.localChanges.append((None,
                                          regex.compile(r"(\\c )", flags=regex.S), "\\cl {}\n\\1".format(clabel)))
                
        # Throw out the known "nonpublishable" markers and their text (if any)
        self.localChanges.append((None, regex.compile(r"\\(usfm|ide|rem|sts|restore|pubinfo)( .*?)?\n(?=\\)", flags=regex.M), ""))

        ############ Temporary (to be removed later) ########%%%%
        # Throw out \esb ... \esbe blocks if Study Bible Sidebars are not wanted
        if not self.asBool("studynotes/includesidebar"):
            self.localChanges.append((None, regex.compile(r"\\esb.+?\\esbe", flags=regex.S), ""))
        ############ Temporary (to be removed later) ########%%%%
        
        if self.asBool("studynotes/includextfn"):
            if self.dict["studynotes/showcallers"] == "%":
                self.localChanges.append((None, regex.compile(r"\\ef \- ", flags=regex.S), "\\ef + "))
            else:
                self.localChanges.append((None, regex.compile(r"\\ef . ", flags=regex.S), "\\ef - "))
        else:
            self.localChanges.append((None, regex.compile(r"\\ef( .*?)\\ef\*", flags=regex.S), ""))

        if self.asBool("notes/showextxrefs"):
            self.localChanges.append((None, regex.compile(r"\\ex", flags=regex.S), r"\\x"))
        else:
            self.localChanges.append((None, regex.compile(r"\\ex( .*?)\\ex\*", flags=regex.S), ""))
        
        # If a printout of JUST the book introductions is needed (i.e. no scripture text) then this option is very handy
        if not self.asBool("document/ifmainbodytext"):
            self.localChanges.append((None, regex.compile(r"\\c .+", flags=regex.S), ""))

        # Probably need to make this more efficient for multi-book and lengthy glossaries (cache the GLO & changes reqd etc.)
        if self.asBool("notes/glossaryfootnotes"):
            self.makeGlossaryFootnotes(printer, bk)

        # Glossary Word markup: Remove the second half of the \w word|glossary-form\w* and apply chosen glossary markup
        v = self.dict["document/glossarymarkupstyle"]
        gloStyle = self._glossarymarkup.get(v, v)
        if v is not None and v != 'ai':
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
            self.localChanges.append((None, regex.compile(r"\\[sr]\d? .+", flags=regex.M), ""))

        if not self.asBool("document/parallelrefs"): # Drop ALL Parallel Passage References
            self.localChanges.append((None, regex.compile(r"\\r .+", flags=regex.M), ""))

        if self.asBool("document/preventorphans"): # Prevent orphans at end of *any* paragraph
            self.localChanges.append((None, regex.compile(r"(\\q\d?(\s?\r?\n?\\v)?( \S+)+( (?!\\)[^\\\s]{1,6})) ([\S]{1,9}\s*\n)", \
                                            flags=regex.M), r"\1\u2000\5"))
            self.localChanges.append((None, regex.compile(r"(?<=\\[^ctm][^\\]+)(\s+[^ 0-9\\\n\u2000\u00A0]{1,6}) ([^ 0-9\\\n\u2000\u00A0]{1,8}\n(?:\\[pmqsc]|$))", flags=regex.S), r"\1\u2000\2"))

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

        # HELP NEEDED from MH to fix this section up again.
        # Keep book number together with book name "1 Kings", "2 Samuel" within \xt and \xo
        self.localChanges.append((self.make_contextsfn(None, regex.compile(r"(\\[xf]t\s[^\\]+)")),
                        regex.compile(r"(\d)\s(\p{L})"), r"\1\u00A0\2"))
                        
        # Temporary fix to stop blowing up when \fp is found in notes (need a longer term TeX solution from DG or MH)
        self.localChanges.append((None, regex.compile(r"\\fp ", flags=regex.M), r" --- ")) 
        
        if self.asBool("notes/keepbookwithrefs"): # keep Booknames and ch:vs nums together within \xt and \xo
            self.localChanges.append((self.make_contextsfn(None, regex.compile(r"(\\[xf]t\s[^\\]+)")),
                                    regex.compile(r"(\d?[^\s\d\-\\,;]{3,}[^\\\s]*?)\s(\d+[:.]\d+(-\d+)?)"), r"\1\u2000\2"))
            self.localChanges.append((self.make_contextsfn(None, regex.compile(r"(\\[xf]t\s[^\\]+)")),
                                    regex.compile(r"(\s.) "), r"\1\u2000")) # Ensure no floating single chars in note text
        
        # keep \xo & \fr refs with whatever follows (i.e the bookname or footnote) so it doesn't break at end of line
        self.localChanges.append((None, regex.compile(r"(\\(xo|fr) (\d+[:.]\d+([-,]\d+)?)) "), r"\1\u00A0"))

        for c in ("fn", "xr"):
            # Force all footnotes/x-refs to be either '+ ' or '- ' rather than '*/#'
            if self.asBool("notes/{}override".format(c)):
                t = "+" if self.asBool("notes/if{}autocallers".format(c)) else "-"
                self.localChanges.append((None, regex.compile(r"\\{} ([^\\\s]+)".format(c[0])), r"\\{} {}".format(c[0],t)))
            # Remove the [spare] space after a note caller if the caller is omitted AND if after a digit (verse number).
            if self.asBool("notes/{}omitcaller".format(c)):
                self.localChanges.append((None, regex.compile(r"(\d )(\\[{0}] - .*?\\[{0}]\*)\s+".format(c[0])), r"\1\2"))

        if self.asBool("notes/frverseonly"):
            self.localChanges.append((None, regex.compile(r"\\fr \d+[:.](\d+)"), r"\\fr \1"))

        if self.asBool("notes/xrverseonly"):
            self.localChanges.append((None, regex.compile(r"\\xo \d+[:.](\d+)"), r"\\xo \1"))

        # Paratext marks no-break space as a tilde ~
        self.localChanges.append((None, regex.compile(r"~", flags=regex.M), r"\u00A0")) 

        # Paratext marks forced line breaks as //
        # self.localChanges.append((None, regex.compile(r"//", flags=regex.M), r"\u2028"))  

        # Convert hyphens from minus to hyphen
        self.localChanges.append((None, regex.compile(r"(?<!\\(?:f|x|ef|fe)\s)((?<=\s)-|-(?=\s))", flags=regex.M), r"\u2011"))

        # Wrap Hebrew and Greek words in appropriate markup to avoid tofu
        if self.asBool("project/autotaghebgrk"):
            if self.dict["document/script"][8:].lower() != "hebr":
                self.localChanges.append((None, regex.compile(r"(?<!\\wh\s*)([\u0590-\u05FF\uFB1D-\uFB4F]+)", flags=regex.M), r"\\+wh \1\\+wh*"))
            if self.dict["document/script"][8:].lower() != "grek":
                self.localChanges.append((None, regex.compile(r"(?<!\\wg\s*)([\u0370-\u03FF\u1F00-\u1FFF]+)", flags=regex.M), r"\\+wg \1\\+wg*"))

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
        # Remove any spaces before the \ior*
        self.localChanges.append((None, regex.compile(r"\s+(?=\\ior\*)", flags=regex.M), r"")) 
        # Escape special codes % and $ that could be in the text itself
        self.localChanges.append((None, regex.compile(r"(?<!\\\S*|\\[fx]\s)([{}])(\s?)".format("".join(self._specialchars)),
                                                      flags=regex.M), lambda m:"\\"+self._specialchars[m.group(1)]+("\\space " if m.group(2) else " "))) 

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
                # Note that this will only pick up the first para of glossary entries
                ge = re.findall(r"\\\S+ \\k (.+)\\k\* (.+?)\r?\n", dat) # Finds all glossary entries in GLO book
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
                ge = re.findall(r"\\\S+ \\k (.+)\\k\* .+?\r?\n", dat) # Finds all glossary entries in GLO book
        for delGloEntry in [x for x in ge if x not in list(set(glossentries))]:
            self.localChanges.append((None, regex.compile(r"\\\S+ \\k {}\\k\* .+?\r?\n".format(delGloEntry), flags=regex.M), ""))

    def analyzeImageCopyrights(self):
        if self.dict['project/iffrontmatter'] == "":
            try:
                with open(self.printer.configFRT(), encoding="utf-8") as inf:
                    txt = inf.read()
            except FileNotFoundError:
                return
        else:
            txt = self.dict['project/colophontext']
        for m in re.findall(r"(?i)\\(\S+).*?\\zimagecopyrights([A-Z]{2,3})?", txt):
            self.imageCopyrightLangs[m[1].lower() if m[1] else "en"] = m[0]
        return

    def generateEmptyImageCopyrights(self):
        self.analyzeImageCopyrights()
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
        self.analyzeImageCopyrights()
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

    def createXrefTriggers(self, bk, prjdir, outpath):
        if self.xrefs is None:
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
            localfile = None
            xrsrc = self.dict['notes/xrlistsource']
            if xrsrc == "strongs_proj":
                localfile = os.path.join(self.printer.settings_dir, self.printer.prjid, "TermRenderings.xml")
                if not os.path.exists(localfile):
                    localfile = None
            if xrsrc[-1] in "0123456789":
                listsize = int(xrsrc[-1])
                xrsrc = xrsrc[:-2]
            else:
                listsize = 0
            logger.debug(f"Create Xrefs: {bk=} {xrsrc=}, {localfile=}, {outpath=}")
            self.xrefs = Xrefs(self, filters, prjdir,
                    self.dict['project/selectxrfile'] if self.dict['notes/xrlistsource'] == 'custom' else None,
                    listsize, xrsrc, localfile, self.dict['strongsndx/shownums'], self.dict['notes/xrverseonly'])
        self.xrefs.process(bk, outpath, usfm=self.printer.get_usfms().get(bk))

