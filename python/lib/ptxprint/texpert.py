
from ptxprint.utils import _, strtobool, asfloat
from dataclasses import dataclass
from typing import Optional, Callable
import logging

logger = logging.getLogger(__name__)

@dataclass(frozen=True)     # frozen not required
class O:
    ident: str
    val: tuple[int, int, int, int, int] | bool | None
    output: str | Callable[[str, int | bool | None], None]
    name: str
    descr: str
    fn: Optional[Callable[['ViewModel', (int | bool | None)], None]] = None

# for s_, (value, min, max, step increment, page increment)
texpertOptions = {
#    "versehyphen":        O("vhyphen", True, "", _("Margin Verse Hyphens"), _("In marginal verses, do we insert a hyphen between verse ranges?")),
    "ptxversion":         O("ptxversion", (0, 0, 10, 1, 1), "\\def{0}{{{1}}}", _("Maximum layout version"), _("Maximum layout version to use or 0 for any. Used to maintain backward compatibility when the TeX macros have been changed in newer versions of PTXprint.")),
    # "AdvCompatLineSpacing": O("linespacebase", False, "*** Help *** Need a lambda fn here ***", _("Legacy 1/14 LineSpacing"), _("In the past, SpaceAbove and SpaceBelow were, in effect units of 1/14 of the base line spacing. This has changed so they are now in units of 1/12 of the base line spacing. Enabling this compatibility reverts the units.")),
    # "AdvCompatGlyphMetrics":  O("useglyphmetrics", False, "*** Help *** Need a lambda fn here ***", _("Use glyph metrics"), _("PTXprint can use either the actual glyph metrics in a line or the font metrics to calculate line heights and depths. Font metrics gives more consistent results.")),
    "bookresetcallers":   O("bookresetcallers", True, "", _("Reset Callers at Each Book"), _("Re-start the footnote and cross-reference callers at the start of each book")),
    "PageAlign":          O("bookstartpage", {"page": _("Next page"), "multi": _("Same page"), "odd": _("Odd page")}, r"\def{0}{{{1}}}", _("Where to start a new book"), _("Does a scripture book start on a new page, the same page as the previous book (if <65% of page has been used), or an odd page")),
    "IntroPageAlign":     O("intropagealign", {"page": _("Next page"), "multi": _("No page breaks"), "odd": _("On an odd page"), "group": _("Grouped")}, r"\def{0}{{{1}}}", _("Where to start a new intro page"), _("Does an intro page start on a new page, the same page as the previous book, an odd page, or group all adjacent intro pages into an odd paged group")),
    "usesysfonts":        O("usesysfonts", True, "", _("Use system fonts"), _("Use fonts from your system as well as your project")),
    "notesEachBook":      O("neachbook", True, "", _("Endnotes at Each Book"), _("Output endnotes at the end of each book")),
    "FinalNotesDown":     O("fnotesdown", False, "", _("Final Page Notes Down"), _("Push notes on the final page to the bottom of the page")),
    "MarkTriggerPoints":  O("mktrigpts", False, "", _("Mark Trigger Points"), _("Display trigger points in output")),
    "MidPageFootnotes":   O("midnotes", False, "", _("Mid-Page Footnotes"), _("Should footnotes go before a single-double column transition")),
    "squashgridbox":      O("squashgrid", True, "", _("No Top Space"), _("Don’t insert space above headings at the start of a column")),
    "IndentAtChapter":    O("chapindent", False, "", _("Allow Indent Para with Cutouts"), _("Allow indented paragraphs at chapter start with cutouts")),
    "IndentAfterHeading": O("afterheadindent", True, "", _("Allow Indent Para After Heading"), _("Allow indented paragraphs following a heading")),
    "NoHangVerseNumberOne": O("nohangvone", True, "", _("Don't hang verse one beside a chapter"), _("Hanging verses into a chapter number can result in clases, depending on the after-chapter space.")),
    "HangVA":             O("hangva", False, "", _("Alternate verse numbers also hang"), _("If there is an alternative verse and the current verse is hanging, does the alternate hang?")),
    "DropActions":        O("noactions", False, "", _("No PDF Bookmarks"), _("Don’t output PDF bookmarks")),
    "Actions":            O("actions", True, "", _("Allow Active Links in PDF"), _("Make links active inside PDF")),
    "refbookmarks":       O("refbkmks", False, "", _("Use Book Codes in PDF Bookmarks"), _("Use book codes instead of book names in bookmarks")),
    "NoTransparency":     O("notransparent", False, "", _("Disable Transparency in PDF"), _("Disable transparency output in PDF")),
    "figlocleft":         O("figleft", True, "", _("Default Figures Top Left"), _("Default figure positions to top left")),
    "CaptionRefFirst":    O("captreffirst", False, "", _("Ref Before Caption"), _("Output reference before caption")),
    "CaptionFirst":       O("captfirst", False, "", _("Show Caption Before Image"), _("Output caption before image")),
    "TOCthreetab":        O("tocthreetab", True, "", _("Use \\toc3 for Tab Text"), _("Use \\toc3 for tab text if no \\zthumbtab")),
    "VisTrace":           O("vistrace", False, "", _("Show Diglot Trace Marks"), _("Insert visible trace marks in diglot output")),
    "VisTraceExtra":     O("vistracex", False, "", _("Extra Trace Mark Info"), _("Add extra information to diglot trace marks")),
    "UnderlineSpaces":    O("underlnsp", True, "", _("Underline Spaces"), _("Underline spaces in underlined runs")),
    "newparnotes":      O("newparnotes", False, "", _("Enhanced paragraphed footnotes"), _("Paragraphed footnotes which allow \\fp to work and also the ifparnotes... controls below. Causes some spacing differences compared to old-style.")),
    "parnoteskillprevdepth": O("parntkillpd", True, "", _("Remove depth above paragraphed notes"),_("Kern away (kill) the glyph/font depth of note types before paragraphed notes, using the value of \\prevdepth")),
    "parnoteskilldepth":   O("parntkilldepth", False, "", _("Remove depth after paragraphed notes"), _("Kill the depth of (the last row of) paragraphed note styles. Paragraphed notes will use the margin as their baseline.")),
    "parnotesruletopskip":   O("parntruletopskip", False, "", _("Use grid not font/glyph height at rule"),_("If true, the footnote rule is positioned relative to the hypothetical baseline above the topmost footnote, rather than relative to the glyph/font height.")),
    "parnotesmidtopskip":   O("parntmidtopskip", True, "", _("Use grid not font/glyph height between notes"),_("If true, then the \\InterNoteSpace is relative to the hypothetical baseline above the topmost footnote, rather than the glyph/font height. \\InterNoteSpace is triggered between note styles.")),
    "FootNoteGlyphMetrics": O("fnxugm", False, "", _("Use glyph height not font height in footnotes"),_("Does the note use the font's descender design parameter, or the actual bottom of the glyph. If the former (and depth is not killed), then the bottom of notes have a common baseline across pages. If the latter, then the glyphs sit as close to the bottom margin as they can, which may permit an extra line of text.")),
    # "AttrMilestoneMatchesUnattr": O("attrmsmatchunattr", False, "", _("Apply Underlying Attributes to Milestones"), _("Should styling specified for a milestone without an attribute be applied to a milestones with an attribute? If true, then styling specified for an e.g. \qt-s\* is also applied to \qt-s|Pilate\*.")),
    "CalcChapSize":       O("calcchapsize", True, "", _("Auto Calc Optimum Chapter Size"), _("Attempt to automatically calculate drop chapter number size")),
    "tildenbsp":          O("tildenbsp", True, "", _("Tilde is No Break Space"), _("Treat ~ as non breaking space")),
    "lastbooknoeject":          O("lastnoeject", False, "", _("Suppress pagebreak after bookend-final"), _("Revert to old behaviour of not ensuring that the whole of the last book is output before back-matter PDFs")),
    # Tuple for spinners: (default, lower, upper, stepIncr, pageIncr)
    "pretolerance":       O("pretolerance", (100, -1, 10000, 10, 100), "{0}={1}", _("Hyphenation threshold"), _("Paragraph badness threshold before trying hyphenation. Set to -1 to always hyphenate")),
    "hyphenpenalty":      O("hyphenpenalty", (50, -9999, 10000, 10, 100), "{0}={1}", _("Penalty for inserting hyphen"), _("Hyphenation penalty")),
    "doublehyphendemerits":      O("doublehyphendemerits", (10000, 0, 1000000, 1000, 10000), "{0}={1}", _("Double hyphenation penalty"), _("Penalty for consecutive hyphenation across two lines")),
    "vertThumbtabVadj":   O("thumbvvadj", (-2., -10, 50, 1,5), "\\def{0}{{{1}pt}}", _("Thumbtab rotated adjustment"), _("Shift thumbtab text")),
    "FigCaptionAdjust":   O("captionadj", (0., -10, 20, 1, 5), "\\def{0}{{{1}pt}}", _("Space between picture & caption"), _("Increase/Reduce the gap between figures and their captions")),
    "DefaultSpaceBeside": O("spbeside", (10., 0, 100, 1, 5), "\\def{0}{{{1}pt}}", _("Default space beside picture"), _("Picture horizontal margin*2")),
    "OptionalBreakPenalty": O("optbkpen", (300, 0, 10000, 10, 100), "\\def{0}{{{1}}}", _("Optional break penalty"), _("Penalty for the optional break")),
    "badspacepenalty":    O("badsppen", (100, -10000, 10000, 10, 100), "{0}={1}", _("Bad space penalty"), _("A bad but not impossible place to breal")),
    "lastnoteinterlinepenalty":  O("lastnoteinterlinep", (10000, -9999, 10000, 10, 100), "{0}={1}", _("Last Note: interlinepenalty"), _("Penalty for breaking between lines of the last footnote.")),
    "lastnotewidowpenalty":  O("lastnotewidowp", (10000, -9999, 10000, 10, 100), "{0}={1}", _("Last Note: widowpenalty"), _("Extra penalty for breaking at the last line of the last footnote.")),
    "lastnoteclubpenalty":  O("lastnoteclubp", (10000, -9999, 10000, 10, 100), "{0}={1}", _("Last Note: clubpenalty"), _("Extra penalty for breaking at the first line of the last footnote.")),
    "lastnoteparpenalty":  O("lastnoteparp", (100, -9999, 10000, 10, 100), "{0}={1}", _("Last Note: penalty at par"), _("Penalty for breaking at an explicit footnote-paragraph in the last footnote.")),
    "NoteShaveShortest":  O("nshaveshort", (2, 0, 100, 1, 1), r"\def{0}{{{1}}}", _("Split notes: Shortest note to shave"), _("If footnotes might be shaved, how many lines must it be?")),
    "NoteShaveMin":  O("nshavemin", (1, 0, 100, 1, 1), r"\def{0}{{{1}}}", _("Split notes: min lines to move."), _("If a footnote is being shaved (split onto next page), what is the minimum number of lines to move?")),
    "NoteShaveStay":  O("nshavestay", (1, 0, 100, 1, 1), r"\def{0}{{{1}}}", _("Split notes: note lines to stay"), _("If a footnote is being shaved (split onto next page), how many lines of (all) notes must remain on the page?")),
    "FootnoteMulS":  O("footnotemuls", (100, 0, 2100, 1, 1), r"\def{0}{{{1}}}", _("Footnote factor-Single column"), _("To avoid needless cylces/underful pages, what portion of a note's height-estimate should TeX apply when gathering input in single-column mode? (100=10percent)")),
    "FootnoteMulT":  O("footnotemult", (100, 0, 2100, 1, 1), r"\def{0}{{{1}}}", _("Footnote factor-Two column"), _("To avoid needless cylces/underful pages, what portion of a note's height-estimate should TeX apply when gathering input in two-column mode? (100=10percent)")),
    "FootnoteMulD":  O("footnotemuld", (500, 0, 2100, 1, 1), r"\def{0}{{{1}}}", _("Footnote factor-Diglot"), _("To avoid needless cylces/underful pages, what portion of a note's height-estimate should TeX apply when gathering diglot input? (100=10percent)")),
    "FootnoteMulC":  O("footnotemulc", (0, 0, 2100, 1, 1), r"\def{0}{{{1}}}", _("Footnote factor-Centre column"), _("To avoid needless cylces/underful pages, what portion of a note's height-estimate should TeX apply when gathering centre-column notes? (100=10percent)")),
    "BookEndDecorationSkip":   O("bedskip", (16, -100, 100, 1,1), "\\def{0}{{{1}pt}}", _("End decoration skip"), _("The gap between the end of the book and the book-end decoration")),
    "DiglotColourPad":   O("diglotcolourpad", (3, -20, 20, 1,1), "\\def{0}{{{1}pt}}", _("Diglot Shading Padding"), _("The amount of side padding (pt) on the shaded background of a diglot")),
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

