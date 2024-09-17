
from ptxprint.utils import _, strtobool, asfloat, f2s
from dataclasses import dataclass, KW_ONLY
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
    "PageFullFactor":     O("pagefullfactor", "LAY", (0.65,  0.30, 0.9, 0.05, 0.05, 2), "\def\{0}{{1}}", _("Page full factor"), 
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

#    "versehyphen":        O("vhyphen", "CVS", True, "", _("Margin Verse Hyphens"), _("In marginal verses, do we insert a hyphen between verse ranges?")),
    "CalcChapSize":       O("calcchapsize", "CVS", True, "", _("Auto Calc Optimum Chapter Size"),
                            _("Attempt to automatically calculate drop chapter number size")),
    "NoHangVerseNumberOne": O("nohangvone", "CVS", True, "", _("Don't hang verse one beside a chapter"),
                              _("Hanging verses into a chapter number can result in clases, depending on the after-chapter space.")),
    "HangVA":             O("hangva", "CVS", False, "", _("Alternate verse numbers also hang"),
                            _("If there is an alternative verse and the current verse is hanging, does the alternate hang?")),
    "afterChapterSpace":  O("afterchapterspace", "CVS", (0.25, -0.20, 1.0, 0.01, 0.10, 2), "{0}={1}", _("After chapter space factor"),
                            _("This sets the gap between the chapter number and the text following. The setting here is a multiple of the main body text size as specified in layout."),
                            valfn=lambda v: f2s(asfloat(v, 0.25) * 12)),
    "afterVerseSpace":    O("afterversespace", "CVS", (0.15, -0.20, 1.0, 0.01, 0.10, 2), "{0}={1}", _("After verse space factor"),
                            _("This sets the gap between the verse number and the text following. The setting here is a multiple of the main body text size as specified in layout."),
                            valfn=lambda v:f2s(asfloat(v, 0.15) * 12)),

    "IndentAtChapter":    O("chapindent", "BDY", False, "", _("Allow Indent Para with Cutouts"),
                            _("Allow indented paragraphs at chapter start with cutouts")),
    "IndentAfterHeading": O("afterheadindent", "BDY", True, "", _("Allow Indent Para After Heading"),
                            _("Allow indented paragraphs following a heading")),
    "badspacepenalty":    O("badsppen", "BDY", (100, -10000, 10000, 10, 100, 0), "{0}={1}", _("Bad space penalty"),
                            _("A bad but not impossible place to breal")),
    "OptionalBreakPenalty": O("optbkpen", "BDY", (300, 0, 10000, 10, 100, 0), "\\def{0}{{{1}}}", _("Optional break penalty"),
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
    "underlineThickness": O("underlinethickness", "FNT", (0.05,  0.01, 0.5, 0.01, 0.01, 2), "{0}={1}", _("Underline thickness (em)"),
                            _("This sets the thickness of the text underline, (measured in ems)."),
                            valfn=lambda v: f2s(float(v or "0.05"))),
    "underlinePosition":  O("underlineposition", "FNT", (0.10, -1.0 , 1.0, 0.01, 0.01, 2), "{0}={1}", _("Underline vertical position (em)"),
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
    "DiglotColourPad":    O("diglotcolourpad", "DIG", (3, -20, 20, 1, 1, 0), "\\def{0}{{{1}pt}}", _("Diglot Shading Padding"),
                            _("The amount of side padding (pt) on the shaded background of a diglot")),

    "figlocleft":         O("figleft", "PIC", True, "", _("Default Figures Top Left"),
                            _("Default figure positions to top left")),
    "CaptionRefFirst":    O("captreffirst", "PIC", False, "", _("Ref Before Caption"),
                            _("Output reference before caption")),
    "CaptionFirst":       O("captfirst", "PIC", False, "", _("Show Caption Before Image"),
                            _("Output caption before image")),
    "cutouterpadding":    O("cutouterpadding", "PIC", (10.0,  0.0, 50.0, 1.0,  5.0,  0), "{0}={1}", _("Space (pt) beside cutout/sidebar"),
                            _("This sets the default gap (pt) between the body text and the side of a figure/sidebar in a cutout.")),
    "FigCaptionAdjust":   O("captionadj", "PIC", (0., -10, 20, 1, 5, 0), "\\def{0}{{{1}pt}}", _("Space between picture & caption"),
                            _("Increase/Reduce the gap between figures and their captions")),
    "DefaultSpaceBeside": O("spbeside", "PIC", (10., 0, 100, 1, 5, 0), "\\def{0}{{{1}pt}}", _("Default space beside picture"),
                            _("Picture horizontal margin*2")),

    "DropActions":        O("noactions", "PDF", False, "", _("No PDF Bookmarks"),
                            _("Don’t output PDF bookmarks")),
    "Actions":            O("actions", "PDF", True, "", _("Allow Active Links in PDF"),
                            _("Make links active inside PDF")),
    "refbookmarks":       O("refbkmks", "PDF", False, "", _("Use Book Codes in PDF Bookmarks"),
                            _("Use book codes instead of book names in bookmarks")),
    "NoTransparency":     O("notransparent", "PDF", False, "", _("Disable Transparency in PDF"),
                            _("Disable transparency output in PDF")),

    "UnderlineSpaces":    O("underlnsp", "OTH", True, "", _("Underline Spaces"),
                            _("Underline spaces in underlined runs")),
    "TOCthreetab":        O("tocthreetab", "OTH", True, "", _("Use \\toc3 for Tab Text"),
                            _("Use \\toc3 for tab text if no \\zthumbtab")),
    # "AttrMilestoneMatchesUnattr": O("attrmsmatchunattr", "OTH", False, "", _("Apply Underlying Attributes to Milestones"), _("Should styling specified for a milestone without an attribute be applied to a milestones with an attribute? If true, then styling specified for an e.g. \qt-s\* is also applied to \qt-s|Pilate\*.")),
    "tildenbsp":          O("tildenbsp", "OTH", True, "", _("Tilde is No Break Space"),
                            _("Treat ~ as non breaking space")),
    "BookEndDecorationSkip":   O("bedskip", "OTH", (16, -100, 100, 1, 1, 0), "\\def{0}{{{1}pt}}", _("End decoration skip"),
                                 _("The gap between the end of the book and the book-end decoration")),
    "MarkTriggerPoints":  O("mktrigpts", "OTH", False, "", _("Mark Trigger Points"),
                            _("Display trigger points in output")),
    "vertThumbtabVadj":   O("thumbvvadj", "OTH", (-2., -10, 50, 1, 5, 0), "\\def{0}{{{1}pt}}", _("Thumbtab rotated adjustment"),
                            _("Shift thumbtab text")),
}

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
    def generateTeX(self, view):
        res = []
        for k, opt in texpertOptions.items():
            n = widgetName(opt)
            v = view.get(n)
            logger.debug(f"TeXpert({n})={v} was {opt.val}")
            if n.startswith("c_"):
                if v is not None and opt.val != v:
                    if callable(opt.output):
                        res.append(opt.output(k, v))
                    elif isinstance(opt.output, str):
                        res.append(opt.output.format("\\"+k, v))
                    else:
                        res.append(f'\\{k}{"true" if v else "false"}')
            elif n.startswith("s_"):
                if v is not None and float(v) != opt.val[0]:
                    res.append(opt.output.format("\\"+k, v))
            elif n.startswith("fcb_"):
                if v is not None and v != list(opt.val.keys())[0]:
                    res.append(opt.output.format("\\"+k, v))
        return "\n".join(res)

    @classmethod
    def opts(self):
        for k, opt in texpertOptions.items():
            yield (k, opt, widgetName(opt))

    @classmethod
    def hasopt(self, n):
        return n in texpertOptions

