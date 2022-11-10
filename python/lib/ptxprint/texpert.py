
from ptxprint.utils import _
import logging

logger = logging.getLogger(__name__)

texpertOptions = {
#    "versehyphen":        ["vhyphen", True, "", _("Margin Verse Hyphens"), _("In marginal verses, do we insert a hyphen between verse ranges?")],
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
    # "AttrMilestoneMatchesUnattr": ["attrmsmatchunattr", False, "", _("Apply Underlying Attributes to Milestones"), _("Should styling specified for a milestone without an attribute be applied to a milestones with an attribute? If true, then styling specified for an e.g. \qt-s\* is also applied to \qt-s|Pilate\*.")],
    "CalcChapSize":       ["calcchapsize", True, "", _("Auto Calc Optimum Chapter Size"), _("Attempt to automatically calculate drop chapter number size")],
    "tildenbsp":          ["tildenbsp", True, "", _("Tilde is No Break Space"), _("Treat ~ as non breaking space")],

    "vertThumbtabVadj":   ["thumbvvadj", -2., "{0}={1}pt", _("Thumbtab rotated adjustment"), _("Shift thumbtab text")],
    "DefaultSpaceBeside": ["spbeside", 10., "\\def{0}{{{1}pt}}", _("Default space beside picture"), _("Picture horizontal margin*2")],
    "OptionalBreakPenalty": ["optbkpen", 300, "\\def{0}{{{1}}}", _("Optional break penalty"), _("Penalty for the optional break")],
    "badspacepenalty":    ["badsppen", 100, "{0}={1}", _("Bad space penalty"), _("A bad but not impossible place to breal")]
}

def widgetName(opt):
    t = opt[1]
    if isinstance(t, bool):
        pref = "c_"
    elif isinstance(t, (float, int)):
        pref = "s_"
    return pref + opt[0]

class TeXpert:
    section = "texpert"

    @classmethod
    def saveConfig(self, config, view):
        for opt in texpertOptions.values():
            n = widgetName(opt)
            v = view.get(n)
            if v != opt[1]:
                view._configset(config, "{}/{}".format(self.section, opt[0]), v)

    @classmethod
    def loadConfig(self, config, view):
        for opt in texpertOptions.values():
            n = widgetName(opt)
            if n.startswith("c_"):
                v = config.getboolean(self.section, opt[0], fallback=opt[1])
            elif n.startswith("s_"):
                v = config.getfloat(self.section, opt[0], fallback=opt[1])

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
                if v is not None and float(v) != opt[1]:
                    res.append(opt[2].format("\\"+k, v))
        return "\n".join(res)

    @classmethod
    def opts(self):
        for k, opt in texpertOptions.items():
            yield (k, opt, widgetName(opt))



