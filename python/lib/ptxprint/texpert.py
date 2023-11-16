
from ptxprint.utils import _, strtobool, asfloat
import logging

logger = logging.getLogger(__name__)

texpertOptions = {
#    "versehyphen":        ["vhyphen", True, "", _("Margin Verse Hyphens"), _("In marginal verses, do we insert a hyphen between verse ranges?")],
    "bookresetcallers":   ["bookresetcallers", True, "", _("Reset Callers at Each Book"), _("Re-start the footnote and cross-reference callers at the start of each book")],
    "notesEachBook":      ["neachbook", True, "", _("Endnotes at Each Book"), _("Output endnotes at the end of each book")],
    "FinalNotesDown":     ["fnotesdown", False, "", _("Final Page Notes Down"), _("Push notes on the final page to the bottom of the page")],
    "MarkTriggerPoints":  ["mktrigpts", False, "", _("Mark Trigger Points"), _("Display trigger points in output")],
    "MidPageFootnotes":   ["midnotes", False, "", _("Mid-Page Footnotes"), _("Should footnotes go before a single-double column transition")],
    "squashgridbox":      ["squashgrid", True, "", _("No Top Space"), _("Don’t insert space above headings at the start of a column")],
    "IndentAtChapter":    ["chapindent", False, "", _("Allow Indent Para with Cutouts"), _("Allow indented paragraphs at chapter start with cutouts")],
    "IndentAfterHeading": ["afterheadindent", True, "", _("Allow Indent Para After Heading"), _("Allow indented paragraphs following a heading")],
    "DropActions":        ["noactions", False, "", _("No PDF Bookmarks"), _("Don’t output PDF bookmarks")],
    "Actions":            ["actions", True, "", _("Allow Active Links in PDF"), _("Make links active inside PDF")],
    "refbookmarks":       ["refbkmks", False, "", _("Use Book Codes in PDF Bookmarks"), _("Use book codes instead of book names in bookmarks")],
    "NoTransparency":     ["notransparent", False, "", _("Disable Transparency in PDF"), _("Disable transparency output in PDF")],
    "figlocleft":         ["figleft", True, "", _("Default Figures Top Left"), _("Default figure positions to top left")],
    "CaptionRefFirst":    ["captreffirst", False, "", _("Ref Before Caption"), _("Output reference before caption")],
    "CaptionFirst":       ["captfirst", False, "", _("Show Caption Before Image"), _("Output caption before image")],
    "TOCthreetab":        ["tocthreetab", True, "", _("Use \\toc3 for Tab Text"), _("Use \\toc3 for tab text if no \\zthumbtab")],
    "VisTrace":           ["vistrace", False, "", _("Show Diglot Trace Marks"), _("Insert visible trace marks in diglot output")],
    "VisTraceExtra":     ["vistracex", False, "", _("Extra Trace Mark Info"), _("Add extra information to diglot trace marks")],
    "UnderlineSpaces":    ["underlnsp", True, "", _("Underline Spaces"), _("Underline spaces in underlined runs")],
    "newparnotes":      ["newparnotes", False, "", _("Enhanced paragraphed footnotes"), _("Paragraphed footnotes which allow \\fp to work and also the ifparnotes... controls below. Causes some spacing differences compared to old-style.")],
    "parnoteskillprevdepth": ["parntkillpd", True, "", _("Remove depth above paragraphed notes"),_("Kern away (kill) the glyph/font depth of note types before paragraphed notes, using the value of \\prevdepth")],
    "parnoteskilldepth":   ["parntkilldepth", False, "", _("Remove depth after paragraphed notes"), _("Kill the depth of (the last row of) paragraphed note styles. Paragraphed notes will use the margin as their baseline.")],
    "parnotesruletopskip":   ["parntruletopskip", False, "", _("Use grid not font/glyph height at rule"),_("If true, the footnote rule is positioned relative to the hypothetical baseline above the topmost footnote, rather than relative to the glyph/font height.")],
    "parnotesmidtopskip":   ["parntmidtopskip", True, "", _("Use grid not font/glyph height between notes"),_("If true, then the \\InterNoteSpace is relative to the hypothetical baseline above the topmost footnote, rather than the glyph/font height. \\InterNoteSpace is triggered between note styles.")],
    "FootNoteGlyphMetrics": ["fnxugm", False, "", _("Use glyph height not font height in footnotes"),_("Does the note use the font's descender design parameter, or the actual bottom of the glyph. If the former (and depth is not killed), then the bottom of notes have a common baseline across pages. If the latter, then the glyphs sit as close to the bottom margin as they can, which may permit an extra line of text.")],
    # "AttrMilestoneMatchesUnattr": ["attrmsmatchunattr", False, "", _("Apply Underlying Attributes to Milestones"), _("Should styling specified for a milestone without an attribute be applied to a milestones with an attribute? If true, then styling specified for an e.g. \qt-s\* is also applied to \qt-s|Pilate\*.")],
    "CalcChapSize":       ["calcchapsize", True, "", _("Auto Calc Optimum Chapter Size"), _("Attempt to automatically calculate drop chapter number size")],
    "tildenbsp":          ["tildenbsp", True, "", _("Tilde is No Break Space"), _("Treat ~ as non breaking space")],
    # Tuple for spinners: (default, lower, upper, stepIncr, pageIncr)
    "pretolerance":       ["pretolerance", (100, -1, 10000, 10, 100), "{0}={1}", _("Hyphenation threshold"), _("Paragraph badness threshold before trying hyphenation. Set to -1 to always hyphenate")],
    "hyphenpenalty":      ["hyphenpenalty", (50, -9999, 10000, 10, 100), "{0}={1}", _("Penalty for inserting hyphen"), _("Hyphenation penalty")],
    "vertThumbtabVadj":   ["thumbvvadj", (-2., -10, 50, 1,5), "{0}={1}pt", _("Thumbtab rotated adjustment"), _("Shift thumbtab text")],
    "FigCaptionAdjust":   ["captionadj", (0., -10, 20, 1, 5), "\\def{0}{{{1}pt}}", _("Space between picture & caption"), _("Increase/Reduce the gap between figures and their captions")],
    "DefaultSpaceBeside": ["spbeside", (10., 0, 100, 1, 5), "\\def{0}{{{1}pt}}", _("Default space beside picture"), _("Picture horizontal margin*2")],
    "OptionalBreakPenalty": ["optbkpen", (300, 0, 10000, 10, 100), "\\def{0}{{{1}}}", _("Optional break penalty"), _("Penalty for the optional break")],
    "badspacepenalty":    ["badsppen", (100, -10000, 10000, 10, 100), "{0}={1}", _("Bad space penalty"), _("A bad but not impossible place to breal")]
}

def widgetName(opt):
    t = opt[1]
    if isinstance(t, bool):
        pref = "c_"
    elif isinstance(t, tuple):
        pref = "s_"
    return pref + opt[0]

class TeXpert:
    section = "texpert"

    @classmethod
    def saveConfig(self, config, view):
        for opt in texpertOptions.values():
            n = widgetName(opt)
            v = view.get(n)
            if n.startswith("c_") and v is None:
                v = False
            if v != opt[1]:
                view._configset(config, "{}/{}".format(self.section, opt[0]), v)

    @classmethod
    def loadConfig(self, config, view):
        for opt in texpertOptions.values():
            if not config.has_option(self.section, opt[0]):
                continue
            n = widgetName(opt)
            default = opt[1]
            if isinstance(default, (tuple, list)):
                default = default[0]
            if n.startswith("c_"):
                v = strtobool(config.get(self.section, opt[0], fallback=default))
            elif n.startswith("s_"):
                v = asfloat(config.get(self.section, opt[0], fallback=default), default)
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
            logger.debug(f"TeXpert({n})={v} was {opt[1]}")
            if n.startswith("c_"):
                if v is not None and opt[1] != v:
                    res.append(f'\\{k}{"true" if v else "false"}')
            elif n.startswith("s_"):
                if v is not None and float(v) != opt[1][0]:
                    res.append(opt[2].format("\\"+k, v))
        return "\n".join(res)

    @classmethod
    def opts(self):
        for k, opt in texpertOptions.items():
            yield (k, opt, widgetName(opt))

    @classmethod
    def hasopt(self, n):
        return n in texpertOptions

