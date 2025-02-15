
from ptxprint.utils import _, strtobool, asfloat, f2s
from dataclasses import dataclass
from typing import Optional, Callable, Tuple, Union
import logging

logger = logging.getLogger(__name__)

@dataclass(frozen=True)     # frozen not required
class O:
    ident: str
    group: str
    val: Union[Tuple[int, int, int, int, int, int], bool, None]
    output: Union[str, Callable[[str, Union[int, bool, None]], None]]
    name: str
    descr: str
#    _: KW_ONLY      # Everything after this is keyword only
    fn: Optional[Callable[['ViewModel', Union[int, bool, None]], None]] = None
    valfn: Optional[Callable[[str], str]] = None

    # Key to val: (value, min, max, step increment, page increment, digits)
    # Tuple for spinners: (default, lower, upper, stepIncr, pageIncr, decPlaces)
    # "shortName": O("ident", "GRP", (default, lower, upper, stepIncr, pageIncr, decPlaces), "{0}={1}", _("Label"), _("Tooltip")),
texpertOptions = {
    "ptxversion":         O("ptxversion", "LAY", (0, 0, 10, 1, 1, 0), "\\def{0}{{{1}}}", _("Maximum layout version"),
                            _("Maximum layout version to use or 0 for any. Used to maintain backward compatibility when the TeX macros have been changed in newer versions of PTXprint.")),
    "AdvCompatLineSpacing":  O("linespacebase", "LAY", False, "", _("Legacy 1/14 LineSpacing"),
                               _("In the past, SpaceAbove and SpaceBelow were, in effect units of 1/14 of the base line spacing. This has changed so they are now in units of 1/12 of the base line spacing. Enabling this compatibility reverts the units."),
                               valfn=lambda v: str(14 if v else 12)),
    "PageAlign":          O("bookstartpage", "LAY", 
                            {"page": _("Next page"), "multi": _("Same page"), "odd": _("Odd page")}, r"\def{0}{{{1}}}", 
                            _("Where to start a new book"), _("Does a scripture book start on a new page, the same page as the previous book (if <65% of page has been used), or an odd page")),
    "PageFullFactor":     O("pagefullfactor", "LAY", (0.65,  0.30, 0.9, 0.05, 0.05, 2), r"\def\{0}{{1}}", _("Page full factor"), 
                            _("This setting is related to how full a page needs to be to force the next book to start on a new page."),
                            valfn=lambda v: f2s(float(v or "0.65"))),
    "IntroPageAlign":     O("intropagealign", "LAY",
                            {"page": _("Next page"), "multi": _("No page breaks"), "odd": _("On an odd page"), "group": _("Grouped")}, r"\def{0}{{{1}}}",
                            _("Where to start a new intro page"), _("Does an intro page start on a new page, the same page as the previous book, an odd page, or group all adjacent intro pages into an odd paged group")),
    "bottomRag":          O("bottomrag", "LAY", (3, 0, 10, 1, 1, 0), "", _("Unbalanced Lines (Max)"),
                            _("Maximum number of unbalanced lines allowed in 2-column layout. Recommended range 1-5.")),
    "squashgridbox":      O("squashgrid", "LAY", True, "", _("No Top Space"), 
                            _("Don’t insert space above headings at the start of a column")),
    "lastbooknoeject":    O("lastnoeject", "LAY", False, "", _("Suppress pagebreak after bookend-final"), 
                            _("Revert to old behaviour of not ensuring that the whole of the last book is output before back-matter PDFs")),
    "NoteLineXoffset":    O("notelineoffset", "LAY", (3, 0.0, 100.0, 0.1, 2.0, 1), r"\def{0}{{{1}mm}}", _("Noteline offset (mm)"), 
                            _("Gap (mm) between noteline and text")),
    "NoteLineXmargin":    O("notelinemargin", "LAY", (10,0.0,100.0, 0.1, 2.0, 1), r"\def{0}{{{1}mm}}", _("Noteline margin (mm)"), 
                            _("Gap (mm) between noteline and edge of page")),
    "NoteLineRuleType":   O("notelinetype", "LAY", 
                            {"rule": _("Solid line"), "dots": _("Row of dots")}, r"\def{0}{{{1}}}", 
                            _("Noteline type"), _("Sometimes it is preferable to use a series of dots rather than a solid line.")),
    "NoteLineY":          O("noteliney", "LAY", (0, 0.00, 25.00, 0.10, 0.50, 2), r"\def{0}{{{1}mm}}",_("Noteline spacing (mm)"), 
                            _("Line spacing between notelines. When set to 0.00 the default line spacing of the document is used.")),
    "NoteLineLineMajor":  O("notelinemajor", "LAY", (0.5, 0.00, 10.00, 0.01, 0.01, 2), r"\def{0}{{{1}pt}}",_("Noteline width (major)"), 
                            _("Thickness (pt) of major notelines. Specify the colour on the Layout page.")),
                            # _("Thickness (pt) of major notelines. Specify the colour (R G B) with \\def\\NoteLineColMajor{0 0.5 0}")),
    # "NoteLineLineMinor":  O("notelineminor", "LAY", (0.3, 0.00, 10.00, 0.01, 0.01, 2) ,r"\def{0}{{{1}pt}}", _("Noteline width (minor)"), 
                            # _("Thickness (pt) of minor notelines. Specify the colour (R G B) with \\def\\NoteLineColMinor{0.5 0 0")),
    # "NoteLineMajorDiv":   O("notelinediv", "LAY", (0, 0, 100, 1, 5, 0), r"\def{0}{{{1}}}", _("Noteline subdivisions"), 
                            # _("Major noteline happens at the start then every this many lines after.")),

    "versehyphen":        O("vhyphen", "CVS", True, None, _("Margin Verse Hyphens"), _("In marginal verses, do we insert a hyphen between verse ranges?")),
    "versehyphenup":      O("vhyphenup", "CVS", False, None, _("Margin Verse Hyphen on first line"), _("Puts the margin verse range hyphen in bridged verses on the first line not the second")),
    "marginalVerseIsMargin": O("mverseismargin", "CVS", False, None, _("No column space reduction for marginal verses"), _("If false, the space for marginal verses is taken from the column. If true, the space for marginal verses is taken from the margins or rule gutter")),
    "CalcChapSize":       O("calcchapsize", "CVS", True, "", _("Auto Calc Optimum Chapter Size"),
                            _("Attempt to automatically calculate drop chapter number size")),
    "NoHangVerseNumberOne": O("nohangvone", "CVS", True, "", _("Don't hang verse one beside a chapter (in poetry)"),
                              _("Hanging verses into a chapter number can result in clashes, depending on the after-chapter space. If so, then turn off hanging verse numbers for the first verse (in poetry only). ")),
    "HangVA":             O("hangva", "CVS", False, "", _("Alternate verse numbers also hang"),
                            _("If there is an alternative verse and the current verse is hanging, does the alternate hang?")),
    "AfterChapterSpaceFactor":  O("afterchapterspace", "CVS", (0.25, -0.20, 1.0, 0.01, 0.10, 2), r"\def\{0}{{{1}}}", _("After chapter space factor"),
                            _("This sets the gap between the chapter number and the text following. The setting here is a multiple of the main body text size as specified in layout."),
                            valfn=lambda v: f2s(asfloat(v, 0.25) * 12)),
    "AfterVerseSpaceFactor": O("afterversespace", "CVS", (0.15, -0.20, 1.0, 0.01, 0.10, 2), r"\def\{0}{{{1}}}", _("After verse space factor"),
                            _("This sets the gap between the verse number and the text following. The setting here is a multiple of the main body text size as specified in layout."),
                            valfn=lambda v:f2s(asfloat(v, 0.15) * 12)),

    "IndentAtChapter":    O("chapindent", "BDY", False, "", _("Allow Indent Para with Cutouts"),
                            _("Allow indented paragraphs at chapter start with cutouts")),
    "IndentAfterHeading": O("afterheadindent", "BDY", True, "", _("Allow Indent Para After Heading"),
                            _("Allow indented paragraphs following a heading")),
    "maxorphanlength":    O("maxorphanlength", "BDY", (8, 1, 20, 1, 1, 0), "", _("Maximum orphan word length"), _("Maximum length of the word that will erreceived orphan protection at the end of a paragraph")),
    "badspacepenalty":    O("badsppen", "BDY", (100, -10000, 10000, 10, 100, 0), "{0}={1}", _("Bad space penalty"),
                            _("A bad but not impossible place to breal")),
    "OptionalBreakPenalty": O("optbkpen", "BDY", (300, 0, 10000, 10, 100, 0), r"\def{0}{{{1}}}", _("Optional break penalty"),
                              _("Penalty for the optional break")),
    "pretolerance":       O("pretolerance", "BDY", (100, -1, 10000, 10, 100, 0), "{0}={1}", _("Hyphenation threshold"),
                            _("Paragraph badness threshold before trying hyphenation. Set to -1 to always hyphenate")),
    "hyphenpenalty":      O("hyphenpenalty", "BDY", (50, -9999, 10000, 10, 100, 0), "{0}={1}", _("Penalty for inserting hyphen"),
                            _("Hyphenation penalty")),
    "doublehyphendemerits": O("doublehyphendemerits", "BDY", (10000, 0, 1000000, 1000, 10000, 0), "{0}={1}", _("Double hyphenation penalty"),
                              _("Penalty for consecutive hyphenation across two lines")),

    "AdvCompatGlyphMetrics": O("useglyphmetrics", "FNT", False, "", _("Use glyph metrics"),
                               _("PTXprint can use either the actual glyph metrics in a line or the font metrics to calculate line heights and depths. Font metrics gives more consistent results."),
                               valfn = lambda v:"%" if v else ""),
    "usesysfonts":        O("usesysfonts", "FNT", True, "", _("Use system fonts"),
                            _("Use fonts from your system as well as your project")),
    "underlineThickness": O("underlinethickness", "FNT", (0.05,  0.01, 0.5, 0.01, 0.01, 2), r"\def{0}{{{1}}}", _("Underline thickness (em)"),
                            _("This sets the thickness of the text underline, (measured in ems)."),
                            valfn=lambda v: f2s(float(v or "0.05"))),
    "UnderlineLower":     O("underlineposition", "FNT", (0.10, -1.0 , 1.0, 0.01, 0.01, 2), r"\def{0}{{{1}em}}", _("Underline vertical position (em)"),
                            _("This sets how far (in ems) the underline is below the text and what it is relative to. If negative, it is the distance below the baseline. If positive (or zero), it is the distance below the bottom of any descenders."),
                            valfn=lambda v: f2s(float(v or "-0.1"))),

    "MidPageFootnotes":   O("midnotes", "NTS", False, "", _("Mid-Page Footnotes"),
                            _("Should footnotes go before a single-double column transition")),
    "FinalNotesDown":     O("fnotesdown", "NTS", False, "", _("Final Page Notes Down"),
                            _("Push notes on the final page to the bottom of the page")),
    "bookresetcallers":   O("bookresetcallers", "NTS", True, "", _("Reset Callers at Each Book"),
                            _("Re-start the footnote and cross-reference callers at the start of each book")),
    "notesEachBook":      O("neachbook", "NTS", True, "", _("Endnotes at Each Book"),
                            _("Output endnotes at the end of each book")),
    "newparnotes":        O("newparnotes", "NTS", False, "", _("Enhanced paragraphed footnotes"),
                            _("Paragraphed footnotes which allow \\fp to work and also the ifparnotes... controls below. Causes some spacing differences compared to old-style.")),
    "parnoteskillprevdepth": O("parntkillpd", "NTS", True, "", _("Remove depth above paragraphed notes"),
                               _("Kern away (kill) the glyph/font depth of note types before paragraphed notes, using the value of \\prevdepth")),
    "parnoteskilldepth":  O("parntkilldepth", "NTS", False, "", _("Remove depth after paragraphed notes"),
                            _("Kill the depth of (the last row of) paragraphed note styles. Paragraphed notes will use the margin as their baseline.")),
    "parnotesruletopskip": O("parntruletopskip", "NTS", False, "", _("Use grid not font/glyph height at rule"),
                             _("If true, the footnote rule is positioned relative to the hypothetical baseline above the topmost footnote, rather than relative to the glyph/font height.")),
    "parnotesmidtopskip": O("parntmidtopskip", "NTS", True, "", _("Use grid not font/glyph height between notes"),
                            _("If true, then the \\InterNoteSpace is relative to the hypothetical baseline above the topmost footnote, rather than the glyph/font height. \\InterNoteSpace is triggered between note styles.")),
    "FootNoteGlyphMetrics": O("fnxugm", "NTS", False, "", _("Use glyph height not font height in footnotes"),
                              _("Does the note use the font's descender design parameter, or the actual bottom of the glyph. If the former (and depth is not killed), then the bottom of notes have a common baseline across pages. If the latter, then the glyphs sit as close to the bottom margin as they can, which may permit an extra line of text.")),
    "lastnoteinterlinepenalty":  O("lastnoteinterlinep", "NTS", (10000, -9999, 10000, 10, 100, 0), "{0}={1}", _("Last Note: interlinepenalty"),
                                   _("Penalty for breaking between lines of the last footnote.")),
    "lastnotewidowpenalty": O("lastnotewidowp", "NTS", (10000, -9999, 10000, 10, 100, 0), "{0}={1}", _("Last Note: widowpenalty"),
                              _("Extra penalty for breaking at the last line of the last footnote.")),
    "lastnoteclubpenalty":  O("lastnoteclubp", "NTS", (10000, -9999, 10000, 10, 100, 0), "{0}={1}", _("Last Note: clubpenalty"),
                              _("Extra penalty for breaking at the first line of the last footnote.")),
    "lastnoteparpenalty":  O("lastnoteparp", "NTS", (100, -9999, 10000, 10, 100, 0), "{0}={1}", _("Last Note: penalty at par"),
                             _("Penalty for breaking at an explicit footnote-paragraph in the last footnote.")),
    "NoteShaveShortest":  O("nshaveshort", "NTS", (2, 0, 100, 1, 1, 0), r"\def{0}{{{1}}}", _("Split notes: Shortest note to shave"),
                            _("If footnotes might be shaved, how many lines must it be?")),
    "NoteShaveMin":       O("nshavemin", "NTS", (1, 0, 100, 1, 1, 0), r"\def{0}{{{1}}}", _("Split notes: min lines to move."),
                            _("If a footnote is being shaved (split onto next page), what is the minimum number of lines to move?")),
    "NoteShaveStay":      O("nshavestay", "NTS", (1, 0, 100, 1, 1, 0), r"\def{0}{{{1}}}", _("Split notes: note lines to stay"),
                            _("If a footnote is being shaved (split onto next page), how many lines of (all) notes must remain on the page?")),
    "FootnoteMulS":       O("footnotemuls", "NTS", (100, 0, 2100, 1, 1, 0), r"\def{0}{{{1}}}", _("Footnote factor-Single column"),
                            _("To avoid needless cylces/underful pages, what portion of a note's height-estimate should TeX apply when gathering input in single-column mode? (100=10percent)")),
    "FootnoteMulT":       O("footnotemult", "NTS", (100, 0, 2100, 1, 1, 0), r"\def{0}{{{1}}}", _("Footnote factor-Two column"),
                            _("To avoid needless cylces/underful pages, what portion of a note's height-estimate should TeX apply when gathering input in two-column mode? (100=10percent)")),
    "FootnoteMulD":       O("footnotemuld", "NTS", (500, 0, 2100, 1, 1, 0), r"\def{0}{{{1}}}", _("Footnote factor-Diglot"),
                            _("To avoid needless cylces/underful pages, what portion of a note's height-estimate should TeX apply when gathering diglot input? (100=10percent)")),
    "FootnoteMulC":       O("footnotemulc", "NTS", (0, 0, 2100, 1, 1, 0), r"\def{0}{{{1}}}", _("Footnote factor-Centre column"),
                            _("To avoid needless cylces/underful pages, what portion of a note's height-estimate should TeX apply when gathering centre-column notes? (100=10percent)")),

    "VisTrace":           O("vistrace", "DIG", False, "", _("Show Diglot Trace Marks"),
                            _("Insert visible trace marks in diglot output")),
    "VisTraceExtra":      O("vistracex", "DIG", False, "", _("Extra Trace Mark Info"),
                            _("Add extra information to diglot trace marks")),
    "DiglotColourPad":    O("diglotcolourpad", "DIG", (3, -20, 20, 1, 1, 0), r"\def{0}{{{1}pt}}", _("Diglot Shading Padding"),
                            _("The amount of side padding (pt) on the shaded background of a diglot")),

    "figlocleft":         O("figleft", "PIC", True, "", _("Default Figures Top Left"),
                            _("Default figure positions to top left")),
    "CaptionRefFirst":    O("captreffirst", "PIC", False, "", _("Ref Before Caption"),
                            _("Output reference before caption")),
    "CaptionFirst":       O("captfirst", "PIC", False, "", _("Show Caption Before Image"),
                            _("Output caption before image")),
    "cutouterpadding":    O("cutouterpadding", "PIC", (10,  0, 50, 1,  5,  0), r"\def{0}{{{1}}}", _("Space (pt) beside cutout/sidebar"),
                            _("This sets the default gap (pt) between the body text and the side of a figure/sidebar in a cutout.")),
    "FigCaptionAdjust":   O("captionadj", "PIC", (0, -10, 20, 1, 5, 0), r"\def{0}{{{1}pt}}", _("Space between picture & caption"),
                            _("Increase/Reduce the gap between figures and their captions")),
    "DefaultSpaceBeside": O("spbeside", "PIC", (10, 0, 100, 1, 5, 0), r"\def{0}{{{1}pt}}", _("Default space beside picture"),
                            _("Picture horizontal margin*2")),

    "DropActions":        O("noactions", "PDF", False, "", _("No PDF Bookmarks"),
                            _("Don’t output PDF bookmarks")),
    "Actions":            O("actions", "PDF", True, "", _("Allow Active Links in PDF"),
                            _("Make links active inside PDF")),
    "refbookmarks":       O("refbkmks", "PDF", False, None, _("Use Book Codes in PDF Bookmarks"),
                            _("Use book codes instead of book names in bookmarks")),
    "NoTransparency":     O("notransparent", "PDF", False, "", _("Disable Transparency in PDF"),
                            _("Disable transparency output in PDF")),
    "MarkAdjustPoints":   O("showadjpoints", "PDF", False, None, _("Show adjust points"),
                            _("Show adjust points in the margin of the text.")),
    "ParaLabelling":      O("showusfmcodes", "PDF", False, "", _("Show USFM codes"),
                            _("Show the USFM marker of paragraphs.\nNote that displaying these \
                               markers may result in changes to the layout of the text.")),
    "ShowHboxErrorBars":  O("showhboxerrorbars", "PDF", False, "", _("Show Error Bars For Overfull Lines"),
                            _("Enable this option to have TeX make overfull lines stand out."),
                            valfn = lambda v:"%" if v else ""),
    # "ProperCase":         O("lowercase", "PDF", False, "", _("Title"),
                            # _("Description in Tooltip")),

    "UnderlineSpaces":    O("underlnsp", "OTH", True, "", _("Underline Spaces"),
                            _("Underline spaces in underlined runs")),
    "TOCthreetab":        O("tocthreetab", "OTH", True, "", _("Use \\toc3 for Tab Text"),
                            _("Use \\toc3 for tab text if no \\zthumbtab")),
    # "AttrMilestoneMatchesUnattr": O("attrmsmatchunattr", "OTH", False, "", _("Apply Underlying Attributes to Milestones"), _("Should styling specified for a milestone without an attribute be applied to a milestones with an attribute? If true, then styling specified for an e.g. \qt-s\* is also applied to \qt-s|Pilate\*.")),
    "tildenbsp":          O("tildenbsp", "OTH", True, "", _("Tilde is No Break Space"),
                            _("Treat ~ as non breaking space")),
    "removextreflinks":   O("removextreflinks", "OTH", True, "", _("Remove \\ref ... \\ref* links"),
                            _("USFM 3.2 allows additional reference links to be inserted as part of \\xt ... \\xt* markup. This frequently appear in DBL text bundles, but are unhandled by PTXprint. Allow these to be removed from the USFM prior to typesetting.")),
    "BookEndDecorationSkip":   O("bedskip", "OTH", (16, -100, 100, 1, 1, 0), r"\def{0}{{{1}pt}}", _("End decoration skip"),
                                 _("The gap between the end of the book and the book-end decoration")),
    "MarkTriggerPoints":  O("mktrigpts", "OTH", False, "", _("Mark Trigger Points"),
                            _("Display trigger points in output")),
    "vertThumbtabVadj":   O("thumbvvadj", "OTH", (-2, -10, 50, 1, 5, 0), r"\def{0}{{{1}pt}}", _("Thumbtab rotated adjustment"),
                            _("Shift thumbtab text")),
    "ShrinkTextStep":     O("shrinktextstep", "OTH", (2, 1, 5, 1, 1, 0), "", _("Shrink Text Step Value (%)"),
                            _("Step Value to shrink text using right-click context menu adjustment.")),
    "ShrinkTextLimit":    O("shrinktextlimit", "OTH", (90, 75, 95, 1, 1, 0), "", _("Minimum Text Shrink (%)"),
                            _("Limit how much text can shrink to using right-click context menu adjustment.")),
    "ExpandTextStep":     O("expandtextstep", "OTH", (3, 1, 5, 1, 1, 0), "", _("Expand Text Step Value (%)"),
                            _("Step Value to expand text using right-click context menu adjustment.")),
    "ExpandTextLimit":    O("expandtextlimit", "OTH", (110, 105, 125, 1, 1, 0), "", _("Maximum Text Expand (%)"),
                            _("Limit how much text can expand to using right-click context menu adjustment.")),
    "autoUpdateDelay":    O("autoupdatedelay", "OTH", (3, 0.0, 120.0, 0.1, 1.0, 1), "", _("Auto-Update Delay (seconds)"),
                            _("Right-clicking again on the PDF within this time (3 second default) will prevent the Auto-Update from running.")),
}                          # (default, lower, upper, stepIncr, pageIncr, decPlaces)

def widgetName(opt):
    t = opt.val
    if isinstance(t, bool):
        pref = "c_"
    elif isinstance(t, tuple):
        pref = "s_"
    elif isinstance(t, dict):
        pref = "fcb_"
    return pref + opt.ident

class TeXpert:
    section = "texpert"

    @classmethod
    def saveConfig(self, config, view):
        for opt in texpertOptions.values():
            n = widgetName(opt)
            v = view.get(n)
            if n.startswith("c_") and v is None:
                v = opt.val
            if n.startswith("c_"):
                incl = v != opt.val
            elif n.startswith("s_"):
                incl = v != str(opt.val[0])
            elif n.startswith("fcb_"):
                incl = v != list(opt.val.keys())[0]
            else:
                incl = False
            if incl:
                view._configset(config, "{}/{}".format(self.section, opt.ident), v)

    @classmethod
    def loadConfig(self, config, view):
        for opt in texpertOptions.values():
            n = widgetName(opt)
            default = opt.val
            if isinstance(default, (tuple, list)):
                default = default[0]
            if n.startswith("c_"):
                v = strtobool(config.get(self.section, opt.ident, fallback=default))
            elif n.startswith("s_"):
                v = asfloat(config.get(self.section, opt.ident, fallback=default), default)
            elif n.startswith("fcb_"):
                default = list(opt.val.keys())[0]
                v = config.get(self.section, opt.ident, fallback=default)
            else:
                v = None
            if v is not None:
                view.set(n, v, skipmissing=True)

    @classmethod
    def generateOutput(self, opt, k, v, default=None):
        out = opt.output
        if out is None:
            out=default
        if callable(out):
            return out(k, v)
        elif isinstance(out, str):
            return out.format("\\"+k, v)
        return ("")

    @classmethod
    def generateTeX(self, view):
        res = []
        for k, opt in texpertOptions.items():
            n = widgetName(opt)
            v = view.get(n)
            if opt.valfn:
                v = opt.valfn(v)
            logger.debug(f"TeXpert({n})={v} was {opt.val}")
            if n.startswith("c_"):
                if v is not None and opt.val != v:
                    res.append(self.generateOutput(opt, k, v,
                                default=lambda k,v: "\\{}{}".format(k, "true" if v else "false")))
            elif n.startswith("s_"):
                if v is not None and float(v) != opt.val[0]:
                    res.append(self.generateOutput(opt, k, v))
            elif n.startswith("fcb_"):
                if v is not None and v != list(opt.val.keys())[0]:
                    res.append(self.generateOutput(opt, k, v))
        return "\n".join(res)

    @classmethod
    def opts(self):
        for k, opt in texpertOptions.items():
            yield (k, opt, widgetName(opt))

    @classmethod
    def hasopt(self, n):
        return n in texpertOptions
