import os, sys, re, subprocess, time
from PIL import Image
from io import BytesIO as cStringIO
from shutil import copyfile, rmtree, copy2, copystat
from threading import Thread
from ptxprint.runner import call, checkoutput
from ptxprint.texmodel import TexModel
from ptxprint.ptsettings import ParatextSettings
from ptxprint.view import ViewModel, VersionStr, refKey
from ptxprint.font import getfontcache, fontconfig_template_nofc
from ptxprint.usfmerge import usfmerge2
from ptxprint.texlog import summarizeTexLog
from ptxprint.utils import _, universalopen, print_traceback, coltoonemax, nonScriptureBooks, \
        saferelpath, runChanges, convert2mm, pycodedir, _outputPDFtypes, startfile
from ptxprint.pdf.fixcol import fixpdffile, compress, outpdf
from ptxprint.pdf.pdfsig import make_signatures, buildPagesTree
from ptxprint.pdf.pdfsanitise import split_pages
from ptxprint.pdf.procpdf import procpdf
from ptxprint.pdfrw import PdfReader, PdfWriter
from ptxprint.pdfrw.errors import PdfError, log
from ptxprint.pdfrw.objects import PdfDict, PdfString, PdfArray, PdfName, IndirectPdfDict, PdfObject
from ptxprint.toc import TOC, generateTex
from ptxprint.unicode.ducet import tailored
from ptxprint.reference import RefList
from ptxprint.transcel import transcel, outtriggers
from ptxprint.xdv.colouring import procxdv
from usfmtc.versification import Versification
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

_errmsghelp = {
"! Argument":                            _("Probably a TeX macro problem - contact support, or post a bug report"),
"! TeX capacity exceeded, sorry":        _("Uh oh! You've pushed TeX too far! Try turning Hyphenation off, or contact support."),
"! Paratext stylesheet":                 _("Check if the stylesheet specified on the Advanced tab exists."),
"! Unable to load picture":              _("Check if picture file is located in 'Figures', 'local\\figures' or a\n" +\
                                           "specified folder. Also try the option 'Omit Missing Pictures'"),
"! Unable to load picture or PDF file":  _("Check if image/PDF file is available on the system.\n" +
                                           "If you have specified one or more Front/Back matter PDFs or a Watermark PDF\n" +
                                           "then ensure that the PDF(s) exist(s); OR uncheck those options (Advanced tab)."),
"! Missing control sequence inserted.":  _("Fallback font probably being applied to text in a footnote (not permitted!)"),
"\\colorhex #1->\\count 1=#1":           _("Expecting a number for \\Color definition, not a color name. (e.g. \\Color xff7f7f)"),
"! Missing number, treated as zero.":    _("Possibly a missing +/- value in the Adjust List (see View+Edit tab).\n" +
                                           "  OR\nMaybe related to USFM3 illustration markup"),
"! Undefined control sequence.":         _("This might be related to a USFM marker error (using an unsupported marker).\n" +\
                                           "Try running 'Basic Checks' in Paratext to validate markers.\n" +\
                                           "It could also be related to an unrecognized setting in ptxprint_mods.tex"),
"! Illegal unit of measure (pt inserted).":    _("One of the settings in the Stylesheet may be missing the units.\n" +\
                                           "To confirm that this is a stylesheet issue, temporarily turn off Stylesheets.\n" +\
                                           "Then, check any recent changes to the Stylesheets (on Advanced tab) and try again."),
"! File ended while scanning use of \\parse@djline.":  ("Check for errors in the Adjust List (see View+Edit tab)."),
"! File ended while scanning use of":    _("Try turning off various settings on the Advanced tab."),
"! Output loop---25 consecutive dead cycles.":  _("Sorry! XeTeX was unable to complete the typesetting.\n" +\
                                           "* If creating a Diglot, ensure both texts can print successfully\n" +\
                                           "  before merging them as a Diglot print. And ensure that there\n" +\
                                           "  aren't any large chunks of missing text in either of the projects.\n" +\
                                           "* Also check that you haven't inadvertently left certain settings on\n" +\
                                           "  from a previous session (Pictures, Diglot, Borders - which will show\n" +\
                                           "  in blue if these features are currently enabled)."),
"! Paratext stylesheet":                 _("Try turning off the ptxprint-mods stylesheet"),
"! File ended while scanning use of \\iotableleader.": _("Problem with Formatting Intro Outline\n" +\
                                           "Try disabling option 'Right-Align \\ior with tabbed leaders' on the Body tab"),
"! Emergency stop.":                     _("Probably a TeX macro problem - contact support, or post a bug report"),
"! Not a letter.":                       _("Possible fault in the hyphenation file\n" +\
                                           "Try turning off Hyphenate option located on the Fonts+Scripts tab"),
"! Font \\extrafont":                     _("Fallback Font issue - set a font on the Fonts+Scripts tab.\n" +\
                                           "(Turn off the option 'Use Fallback Font' or specify a valid font)"),
"! Font":                                _("Font related issue. The most likely reason for this error is that\n" +\
                                          "the selected font has not been installed for all users. See FAQ."),
"! Improper `at' size":                  _("Font size setting issue. Check to see if the font size in a style\n" +\
                                          "in or near the reference below is incorrect (maybe it is set to 0.00)."),
"! Too many }'s":                        _("Possibly a TeX macro issue - contact support, or post a bug report"),
"! This can't happen (page)":            _("Possibly a TeX macro issue - contact support, or post a bug report"),
"! I can't find file `paratext2.tex'.":  _("Possibly a faulty installation."),
"! I can't find file `ptx-tracing.tex'.": _("Possibly a faulty installation."),
"Runaway argument?":                     _("Unknown issue. Possibly related to Right-aligned tabbed leaders. " +\
                                           "Try turning off various settings on the Advanced Tab."),
"Unknown":                               _("Oops! Something unexpected happened causing this unhandled error.\n" +\
                                           "Try using the 'Tidy Up' button on the Help tab and then try again.\n" +\
                                           "If you are still unable to proceed, use the 'Create Archive...' button\n" +\
                                           "on the Help tab to create a .zip file. Send it to your PTXprint support person\n" +\
                                           "for further assistance. Please include a description of the problem, and if\n" +\
                                           "known, state which setting was changed since it last worked.")
}

_pdfmodes = {
    'rgb': ("Screen", "Digital"),
    'cmyk': ("CMYK", "Transparency")
}

def base(fpath):
    doti = fpath.rfind(".")
    return os.path.basename(fpath[:doti])

# https://sites.google.com/a/lci-india.org/typesetting/home/illustrations/where-to-find-illustrations
def codeLower(fpath):
    cl = re.findall(r"(?i)_?((?=ab|cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib)..\d{5})[abcABC]?$", base(fpath))
    if cl:
        return cl[0].lower()
    else:
        return ""

def newBase(fpath):
    clwr = codeLower(fpath)
    if len(clwr):
        return clwr
    else:
        return re.sub('[()&+,.;: ]', '_', base(fpath).lower())

_diglotprinter = {
"_diglotcustomsty":         "c_useCustomSty",
"_diglotmodsty":            "c_useModsSty",
"_diglotincludefn":         "c_includeFootnotes",
"_diglotincludexr":         "c_includeXrefs"
}

_diglot = {
"diglot/ifusecustomsty_":    "project/ifusecustomsty",
"diglot/ifusemodsty_":       "project/ifusemodssty",
"diglot/ifincludefootnotes_":"notes/includefootnotes",
"diglot/ifincludexrefs_":    "notes/includexrefs",
"diglot/ifhavehyphenate_":   "paragraph/ifhavehyphenate",
"diglot/ifhyphenate_":       "paragraph/ifhyphenate",

"diglot/intfile":           "project/intfile",
# "diglot/colorfonts" :       "document/ifcolorfonts",
"diglot/diglotcolour":      "document/diglotcolour",
"diglot/ifdiglotcolour_":   "document/ifdiglotcolour",
"diglot/ifrtl" :            "document/ifrtl",
"diglot/ifshow1chbooknum":  "document/ifshow1chbooknum",
"diglot/fontfactor" :       "paper/fontfactor",
"diglot/linespacingfactor": "paragraph/linespacingfactor",
"diglot/afterchapterspace": "texpert/afterchapterspace",
"diglot/afterversespace":   "texpert/afterversespace",
"diglot/iflinebreakon" :    "document/iflinebreakon",
"diglot/linebreaklocale" :  "document/linebreaklocale",

"diglot/ifletter":          "document/ifletter",
"diglot/letterspace":       "document/letterspace",
"diglot/letterstretch":     "document/letterstretch",
"diglot/lettershrink":      "document/lettershrink",

"diglot/docscript" :        "document/script",
# "diglot/docdigitmapping" :  "document/digitmapping",
"diglot/interlinear":       "project/interlinear",
                            
"diglot/fontregular" :      "document/fontregular",
"diglot/fontbold" :         "document/fontbold",
"diglot/fontitalic" :       "document/fontitalic",
"diglot/fontbolditalic" :   "document/fontbolditalic",
"diglot/ifshowversenums" :  "document/ifshowversenums",
"diglot/indentunit":        "document/indentunit",
"diglot/ifrtl":             "document/ifrtl",
"diglot/xrlocation" :       "notes/xrlocation",

"diglot/copyright":         "project/copyright",
"diglot/license":           "project/license",
"diglot/ptxprintstyfile_":  "project/ptxprintstyfile_",

"diglotfancy/versedecorator":       "fancy/versedecorator",
"diglotfancy/versedecoratorpdf":    "fancy/versedecoratorpdf",
"diglotfancy/versedecoratorshift":  "fancy/versedecoratorshift",
"diglotfancy/versedecoratorscale":  "fancy/versedecoratorscale",
"diglotfancy/versedecoratorisfile": "fancy/versedecoratorisfile",
"diglotfancy/versedecoratorisayah": "fancy/versedecoratorisayah",
"diglotfancy/endayah":              "fancy/endayah",
"diglotfancy/sectionheader":        "fancy/sectionheader",
"diglotfancy/sectionheadershift":   "fancy/sectionheadershift",
"diglotfancy/sectionheaderscale":   "fancy/sectionheaderscale",
"diglotfancy/sectionheaderpdf":     "fancy/sectionheaderpdf",
}

_joblock = None
def lockme(job):
    global _joblock
    if _joblock is not None:
        return False
    _joblock = job
    return True

def unlockme():
    global _joblock
    _joblock = None

def isLocked():
    global _joblock
    return _joblock is not None

class RunJob:

    def __init__(self, printer, scriptsdir, macrosdir, args, inArchive=False):
        self.scriptsdir = scriptsdir
        self.printer = printer
        self.macrosdir = macrosdir
        self.tempFiles = []
        self.picfiles = []
        self.tmpdir = "."
        self.maxRuns = 1
        self.changes = None
        self.args = args
        self.res = 0
        self.thread = None
        self.busy = False
        self.ispdfxa = "Screen"
        self.inArchive = inArchive
        self.noview = False
        self.nothreads = False
        # self.oldversions = 1
        self.docreatediff = False
        # self.onlydiffs = True
        # self.diffPdf = None
        self.rerunReasons = []
        self.coverfile = None

    def fail(self, txt):
        self.printer.set("l_statusLine", txt)
        self.printer.finished(False)
        self.busy = False
        unlockme()

    def doit(self, noview=False):
        if not lockme(self):
            return False
        self.noview = noview
        self.texfiles = []
        if self.printer.ptsettings is None:
            self.fail(_("Illegal Project"))
            return
        self.printer.loadHyphenation()
        self.printer.incrementProgress(True, stage="pr")
        info = TexModel(self.printer, self.printer.ptsettings, self.printer.prjid, inArchive=self.inArchive)
        info.debug = self.args.debug
        self.tempFiles = []
        self.prjid = info.dict["project/id"]
        configid = info.dict["config/name"]
        self.prjdir = self.printer.project.path
        if self.prjid is None or not len(self.prjid):     # can't print no project
            return
        self.tmpdir = self.printer.project.printPath(configid)
        os.makedirs(self.tmpdir, exist_ok=True)
        bks = self.printer.getBooks(files=True)
        jobs = []       # [(bkid/module_path, False) or (RefList, True)] 
        if self.printer.bookrefs is None:
            jobs = [(b, False) for b in bks]
        else:
            lastbook = None
            for r in self.printer.bookrefs:
                if r.first.book != lastbook:
                    jobs.append((RefList((r, )), True))
                    lastbook = r.first.book
                else:
                    jobs[-1][0].append(r)

        logger.debug(f"{jobs=}")
        reasons = info.prePrintChecks()
        if len(reasons):
            self.fail(", ".join(reasons))
            return
        if not len(jobs):
            self.fail(_("No books to print"))
            return

        self.books = []
        self.maxRuns = 1 if self.printer.get("c_quickRun") else (self.args.runs or 5)
        self.changes = None
        # set values based on UI components
        self.ispdfxa = self.printer.get("fcb_outputFormat") or "Screen"
        self.docreatediff = self.printer.docreatediff
        if not self.inArchive:
            self.checkForMissingDecorations(info)
        
        if True: # info.asBool("project/combinebooks"):
            joblist = [jobs]
        else:
            joblist = [[j] for j in jobs]

        captions = []
        diginfos = {}
        info["diglotcaptions_"] = ""
        if len(self.printer.diglotViews):
            for k, dv in self.printer.diglotViews.items():
                if dv is None:
                    dv = self.printer.createDiglotView(k)
                if dv is None:
                    continue
                dv.loadHyphenation()
                # digfraction = info.dict["document/diglotprifraction"]
                # digprjid = info.dict["document/diglotsecprj"]
                # digcfg = info.dict["document/diglotsecconfig"]
                digcfg = self.printer.polyglots.get(k, None)
                if digcfg.captions:
                    captions.append(k)
                digprjdir = dv.project.path
                digptsettings = ParatextSettings(digprjdir)
                diginfos[k] = TexModel(dv, digptsettings, dv.prjid, inArchive=self.inArchive, diglotbinfo=info, digcfg=digcfg)
                reasons = diginfos[k].prePrintChecks()
                if len(reasons):
                    self.fail(", ".join(reasons) + " in diglot secondary")
                    return
                digbooks = dv.getAllBooks()
                badbooks = set()
                for j in joblist:
                    allj = set(r[0][0].first.book for r in j if r[1])
                    j[:] = [b for b in j if b[1] and b[0][0].first.book in digbooks]
                    badbooks.update(allj - set(r[0][0].first.book for r in j if r[1]))
                if len(badbooks):
                    self.printer.doError("These books are not available in the secondary diglot project", " ".join(sorted(badbooks)),
                                         show=not self.printer.get("c_quickRun"))
                    self.printer.finished(False)
                    self.busy = False
                    unlockme()
                    return
            info["diglotcaptions_"] = "".join(captions)
            self.texfiles += sum((self.digdojob(j, info, diginfos) for j in joblist), [])
        else: # Normal (non-diglot)
            self.texfiles += sum((self.dojob(j, info) for j in joblist), [])
        self.printer.tempFiles = self.texfiles  # Always do this now - regardless!
        return self.res

    def dojob(self, jobs, info):
        donebooks = []
        # import pdb; pdb.set_trace()
        for i, j in enumerate(jobs):
            if len(jobs) >= 5 and i % (len(jobs) // 5) == 0:
                info.printer.incrementProgress(True, stage="pr")
            b = j[0][0].first.book if j[1] else j[0]
            logger.debug(f"Converting {b} in {self.tmpdir} from {self.prjdir}")
            try:
                out = info.convertBook(b, j[0], self.tmpdir, self.prjdir, j[1], bkindex=i)
            except FileNotFoundError as e:
                self.printer.doError(str(e))
                out = None
            if out is None:
                continue
            outpath = os.path.join(self.tmpdir, out)
            triggers = {}
            if info["notes/ifxrexternalist"]:
                triggers = info.createXrefTriggers(b, self.prjdir, triggers)
            if info.dict.get("studynotes/txlinclquestions", False):
                triggers = transcel(triggers, b, self.prjdir, info.dict.get("studynotes/txllangtag", "en-US"),
                                    overview=info.dict.get("studynotes/txloverview", False),
                                    boldover=info.dict.get("studynotes/txlboldover", True),
                                    numberedQs=info.dict.get("studynotes/txlnumbered", True),
                                    showRefs=info.dict.get("studynotes/txlshowrefs", False),
                                    usfm=self.printer.get_usfms().get(b))
            if len(triggers):
                outtriggers(triggers, b, outpath+".triggers")
            else:
                try:
                    os.remove(outpath+".triggers")
                except FileNotFoundError:
                    pass
            donebooks.append(out)
        if not len(donebooks):
            unlockme()
            return []
        self.books += donebooks
        info["project/bookids"] = [r[0][0].first.book if r[1] else "MOD" for r in jobs]
        info["project/books"] = donebooks
        res = self.sharedjob(jobs, info, False)
        if info['notes/ifxrexternalist']:
            res += [os.path.join(self.tmpdir, out+".triggers") for out in donebooks]
        return [os.path.join(self.tmpdir, out) for out in donebooks] + res

    def digdojob(self, jobs, info, diginfos):
        _digSecSettings = ["paper/pagesize", "paper/height", "paper/width", "paper/margins",
                           "paper/topmarginfactor", "paper/bottommarginfactor",
                           "paper/headerposition", "paper/footerposition", "paper/ruleposition",
                           "document/ch1pagebreak", "document/bookintro", "document/introoutline", 
                           "document/parallelrefs", "document/elipsizemptyvs", "notes/iffootnoterule",
                           "notes/xrlocation",
                           "notes/fneachnewline", "notes/xreachnewline", "document/filterglossary", 
                           "document/chapfrom", "document/chapto", "document/ifcolorfonts", "document/ifshow1chbooknum"]
        sheets = {}
        keyarr = ["L"]
        outfname = info.printer.baseTeXPDFnames([r[0][0].first.book if r[1] else r[0] for r in jobs])[0] + ".tex"
        info.dict.setdefault("diglots_", {})
        for k, diginfo in diginfos.items():
            texfiles = []
            digdonebooks = []
            diginfo["project/bookids"] = [r[0][0].first.book for r in jobs if r[1]]
            diginfo["project/books"] = digdonebooks
            diginfo["document/ifdiglot"] = "%"
            diginfo["footer/ftrcenter"] = "-empty-"
            diginfo["footer/ifftrtitlepagenum"] = "%"
            diginfo["fancy/pageborder"] = "%"
            diginfo["document/diffcolayout"] = False
            diginfo["snippets/diglot"] = False
            docdir = info["/ptxdocpath"]
            for s in _digSecSettings:
                diginfo[s]=info[s]
            syntaxErrors = []

            # create differential ptxprint.sty
            cfgname = info['config/name']
            outstyname = os.path.join(self.tmpdir, f"diglot_{k}.sty")
            with open(outstyname, "w", encoding="utf-8") as outf:
                diginfo.printer.styleEditor.output_diffile(outf, basesheet=info.printer.styleEditor.asStyle(None),
                                                           sheet=diginfo.printer.styleEditor.asStyle(None))
            diginfo["project/ptxprintstyfile_"] = outstyname.replace("\\", "/")

            logger.debug('Diglot processing jobs: {}'.format(jobs))
            if k == "R":
                sheets['L'] = info.printer.getStyleSheets()
            sheets[k] = diginfo.printer.getStyleSheets()
            keyarr.append(k)
            if diginfo['project/iffrontmatter'] != '%' or diginfo["project/sectintros"]:
                texfiles.append(diginfo.addInt(os.path.join(self.tmpdir, outfname.replace(".tex", "_INTR.SFM"))))
            diginfo["cfgrpath_"] = saferelpath(diginfo.printer.project.srcPath(diginfo.printer.cfgid), docdir).replace("\\","/")
            info.dict["diglots_"][k] = diginfo

        donebooks = []
        versification = None
        reversifyinfo = None
        # breakpoint()
        if info.dict['texpert/reversify']:
            vf = info.printer.ptsettings.versification
            if vf is not None:
                versification = Versification(os.path.join(info.printer.project.path, vf))
            reversifyinfo = (versification, info.dict['texpert/showvpvrse'], info.dict['texpert/showvpchap'])
        for j in jobs:
            b = j[0][0].first.book if j[1] else j[0]
            # logger.debug(f"Diglot[{k}]({b}): f{self.tmpdir} from f{self.prjdir}") # broken (missing k)
            inputfiles = []
            left = None
            for k, diginfo in diginfos.items():
                digprjdir = diginfo.printer.project.path
                try:
                    out = None
                    if not len(inputfiles):
                        out = info.convertBook(b, j[0], self.tmpdir, self.prjdir, j[1])
                        left = os.path.join(self.tmpdir, out)
                        inputfiles.append(left)
                        texfiles.append(left)
                    digout = diginfo.convertBook(b, j[0], self.tmpdir, digprjdir, j[1], reversify=reversifyinfo)
                    right = os.path.join(self.tmpdir, digout)
                    inputfiles.append(right)
                    texfiles.append(right)
                except FileNotFoundError as e:
                    self.printer.doError(str(e))
                    out = None
                    digout = None
                if out is not None:
                    donebooks.append(out)
                if digout is None:
                    continue
                else:
                    diginfo["project/books"].append(digout)
                    self.books.append(digout)
            if left and b not in nonScriptureBooks:
                # Now merge the secondary text (right) into the primary text (left) 
                outFile = re.sub(r"^([^.]*).(.*)$", r"\1-diglot.\2", left)
                if len(donebooks):
                    donebooks[-1] = os.path.basename(outFile)
                logFile = os.path.join(self.tmpdir, "ptxprint-merge.log")

                mode = info["document/diglotmergemode"]
                if mode in ('True', 'False') or not mode:
                    mode = "doc"
                sync = "normal"
                if "-" in mode:
                    (mode, sync) = mode.split("-")
                logger.debug(f"usfmerge2({inputfiles}) -> {outFile} with {logFile=} {mode=} {sync=}")
                # Do we ask the merge process to write verification files? (use diff -Bws to confirm they are they same as the input)
                debugmerge = logger.getEffectiveLevel() <= 5 
                usfmerge2(inputfiles, keyarr, outFile, stylesheets=sheets, mode=mode, synchronise=sync, debug=debugmerge, changes=info.changes.get("merged", []), book=b)
                texfiles += [outFile, logFile]

        
        if not len(donebooks): # or not len(digdonebooks):
            unlockme()
            return []

        if len(syntaxErrors):
            prtDrft = _("And check if a faulty rule in PrintDraftChanges.txt has caused the error(s).") if info["project/usechangesfile"] else ""
            self.printer.doError(_("Failed to merge texts due to a Syntax Error:"),
                secondary="\n".join(syntaxErrors)+"\n\n"+_("Run the Basic Checks in Paratext to ensure there are no Marker errors "+ \
                "in either of the diglot projects. If this error persists, try running the Schema Check in Paratext as well.") + " " + prtDrft,
                title=_("PTXprint [{}] - Diglot Merge Error!").format(VersionStr), copy2clip=True)

        info["project/bookids"] = [r[0][0].first.book for r in jobs if r[1]]
        info["project/books"] = donebooks
        logger.debug(f"{donebooks=}")

        # Pass all the needed parameters for the snippet from diginfo to info
        for k,v in _diglotprinter.items():
            info.printer.set(k, diginfo.printer.get(v))
        info["_isDiglot"] = True
        res = self.sharedjob(jobs, info, diglots=True)
        texfiles += res
        return texfiles

    def sharedjob(self, jobs, info, prjid=None, prjdir=None, extra="", diglots=False):
        logger.debug(f"in runjob sharedjob usesysfonts: {info['texpert/usesysfonts']}")
        nosysfonts = not info['texpert/usesysfonts'] or self.args.nofontcache
        genfiles = []
        if prjid is None:
            prjid = self.prjid
        if prjdir is None:
            prjdir = self.prjdir
        cfgname = info['config/name']
        if cfgname is None or cfgname == "":
            cfgname = ""
        else:
            cfgname = "-" + cfgname
        outfname = info.printer.baseTeXPDFnames([r[0][0].first.book if r[1] else r[0] for r in jobs])[0] + ".tex"
        info.update(None)
        if info['project/iffrontmatter'] != '%':
            frtfname = os.path.join(self.tmpdir, outfname.replace(".tex", "_FRT.SFM"))
            info.createFrontMatter(frtfname)
            genfiles.append(frtfname)
        if info["project/sectintros"]:
            genfiles.append(info.addInt(os.path.join(self.tmpdir, outfname.replace(".tex", "_INT.SFM"))))
            if diglots:
                addintlist = [r"\diglottrue\zglot|L\*"+info["project/intfile"]]
                for k in self.printer.diglotViews.keys():
                    diginfo = info.dict["diglots_"][k]
                    genfiles.append(diginfo.addInt(os.path.join(self.tmpdir, outfname.replace(".tex", f"_INT{k}.SFM"))))
                    addintlist.append(f"\\zglot|{k}\\*"+diginfo["project/intfile"])
                addintlist.append(r"\zglot|\*")
                info["project/intfile"] = "".join(addintlist)
        info["document/piclistfile"] = ""
        if info.asBool("document/ifinclfigs"):
            self.printer.incrementProgress(stage="gp")
            self.picfiles = self.gatherIllustrations(info, jobs, prjdir, diglots=diglots)
            # self.texfiles += self.gatherIllustrations(info, jobs, self.args.paratext)
        texfiledat = info.asTex(filedir=self.tmpdir, jobname=outfname.replace(".tex", ""), extra=extra, diglots=diglots)
        with open(os.path.join(self.tmpdir, outfname), "w", encoding="utf-8") as texf:
            texf.write(texfiledat)
        genfiles += [os.path.join(self.tmpdir, outfname.replace(".tex", x)) for x in (".tex", ".xdv")]
        if self.inArchive:
            return genfiles
        os.putenv("hyph_size", "65521")     # always run with maximum prime hyphenated words size (xetex is still tiny ~200MB resident)
        # os.putenv("extra_mem_bot", "5000000")    # extra main memory on top of 5M
        os.putenv("stack_size", "32768")    # extra input stack space (up from 5000)
        # os.putenv("save_size", "1000000")    # extra increase save stack from 80000
        os.putenv("pool_size", "12500000")  # Double conventional pool size for big jobs (Full Bible with xrefs)
        os.putenv("max_print_line", "32767")    # Allow long error messages
        ptxmacrospath = os.path.abspath(self.macrosdir)
        ptxmacrobase = os.path.join(pycodedir(), 'ptx2pdf')
        if not os.path.exists(ptxmacrobase):
            ptxmacrobase = os.path.join(pycodedir(), "..", "..", "..", "src")
        if not os.path.exists(ptxmacrospath) or not os.path.exists(os.path.join(ptxmacrospath, "paratext2.tex")):
            ptxmacrospath = os.path.abspath(ptxmacrobase)
        if not os.path.exists(ptxmacrospath):
            for b in (getattr(sys, 'USER_BASE', '.'), sys.prefix):
                if b is None:
                    continue
                ptxmacrospath = os.path.abspath(ptxmacrobase)
                if os.path.exists(ptxmacrospath):
                    break

        pathjoiner = (";" if sys.platform.startswith("win") else ":")
        envtexinputs = os.getenv("TEXINPUTS")
        texinputs = envtexinputs.split(pathjoiner) if envtexinputs is not None and len(envtexinputs) else []
        for a in (os.path.abspath(self.tmpdir), ptxmacrospath):
            if a not in texinputs:
                texinputs.append(a+"//")
        miscfonts = getfontcache().fontpaths[:]
        if sys.platform.startswith("win") and not nosysfonts:
            a = "/usr/share/ptx2pdf/texmacros"
            if a not in texinputs:
                texinputs.append(a)
            miscfonts.append("/usr/share/ptx2pdf/texmacros")
        miscfonts.append(os.path.join(ptxmacrospath, '..', 'fonts'))
        miscfonts.append(os.path.join(self.tmpdir, "fonts"))
        sfonts = os.path.join(self.prjdir, "shared", "fonts")
        miscfonts.append(sfonts)
        miscfonts.append(ptxmacrospath)     # for mappings/ which must be in the fonts path
        if len(miscfonts):
            if nosysfonts:
                fcs = "\n    ".join(['<dir>{}</dir>'.format(d) for d in miscfonts])
                with open(os.path.join(self.tmpdir, 'fonts.conf'), "w") as outf:
                    outf.write(fontconfig_template_nofc.format(fontsdirs=fcs))
                os.putenv("FONTCONFIG_FILE", os.path.join(self.tmpdir, "fonts.conf"))
                logger.debug(f"FONTCONFIG_FILE={os.path.join(self.tmpdir, 'fonts.conf')}")
                os.putenv("MISCFONTS", pathjoiner.join((ptxmacrospath, sfonts)))
            else:
                os.putenv("MISCFONTS", pathjoiner.join(miscfonts))
        logger.debug(f"MISCFONTS={pathjoiner.join(miscfonts)}")
        logger.debug("TEXINPUTS={} becomes {}".format(os.getenv('TEXINPUTS'), pathjoiner.join(texinputs)))
        logger.debug(f"{pathjoiner.join(miscfonts)=}")
        os.putenv('TEXINPUTS', pathjoiner.join(texinputs))
        os.chdir(self.tmpdir)
        outpath = os.path.join(self.tmpdir, '..', outfname[:-4])
        pdfext = _outputPDFtypes.get(self.printer.get("fcb_outputFormat", "")) or ""
        pdfext = "_" + pdfext if len(pdfext) else ""
        pdffile = outpath + "{}.pdf".format(pdfext)
        logger.debug(f"{pdffile} exists({os.path.exists(pdffile)})")
        oldversions = int(self.printer.get('s_keepVersions', '0'))
        if oldversions > 0:
            for c in range(oldversions, 0, -1):
                opdffile = pdffile[:-4] + "_{}.pdf".format(c)
                ipdffile = pdffile[:-4] + "_{}.pdf".format(c-1) if c > 1 else pdffile
                if os.path.exists(opdffile):
                    os.remove(opdffile)
                if os.path.exists(ipdffile):
                    logger.debug(f"Rename {ipdffile} to {opdffile}")
                    try:
                        copy2(ipdffile, opdffile)
                        copystat(ipdffile, opdffile)
                    except OSError as e:
                        log.error(f"Failed to copy: {ipdffile} to {opdffile}")
        if self.nothreads:
            self.run_xetex(outfname, pdffile, info)
        else:
            self.thread = Thread(target=self.run_xetex, args=(outfname, pdffile, info))
            self.busy = True
            logger.debug("sharedjob: Starting thread to run xetex")
            self.thread.start()
            info.printer.waitThread(self.thread)
        self.done_job(outfname, pdffile, info)
        return genfiles

    def wait(self):
        logger.debug("Waiting for thread: {}, {}".format(self.busy, isLocked()))
        if self.busy:
            self.thread.join()
        unlockme()
        return self.res

    def getxdvname(self, texfname, info):
        if info["finishing/extraxdvproc"]:
            res = texfname.replace(".tex", "_proc.xdv")
        else:
            res = texfname.replace(".tex", ".xdv")
        return res

    def processxdv(self, inxdv, outxdv, info):
        procxdv(inxdv, outxdv)

    def run_xetex(self, outfname, pdffile, info):
        numruns = 0
        cachedata = {}
        cacheexts = {"toc":     (_("table of contents"), True), 
                    "picpages": (_("image copyrights"), False), 
                    "parlocs":  (_("chapter positions"), True)}
        for a in cacheexts.keys():
            cachedata[a] = self.readfile(os.path.join(self.tmpdir, outfname.replace(".tex", "."+a)))
        while numruns < self.maxRuns:
            self.printer.incrementProgress(stage="lo", run=numruns)
            commentstr = " ".join([
                    "date="+datetime.today().isoformat(),
                    "ptxprint_version="+VersionStr,
                    "run="+str(numruns)])
            cmd = ["xetex", "-halt-on-error", "-interaction=nonstopmode",
                   '-output-comment="'+commentstr+'"', "-no-pdf"]
            if self.forcedlooseness is None:
                action = outfname
            else:
                action = r"\def\ForcedLooseness{{{}}}\input {}".format(self.forcedlooseness, outfname)
            logger.debug(f"Running: {cmd} {action}")
            runner = call(cmd + [action], cwd=self.tmpdir)
            if isinstance(runner, subprocess.Popen) and runner is not None:
                try:
                    #runner.wait(self.args.timeout)
                    runner.wait()
                except subprocess.TimeoutExpired:
                    print("Timed out!")
                self.res = runner.returncode
            elif isinstance(runner, subprocess.CompletedProcess):
                self.res = runner.returncode
                logger.debug(f"{runner.stdout.decode('UTF-8')}")
            else:
                self.res = runner
            print("cd {}; xetex {} -> {}".format(self.tmpdir, outfname, self.res))
            logfname = outfname.replace(".tex", ".log")
            (self.loglines, rerun) = self.parselog(os.path.join(self.tmpdir, logfname), rerunp=True, lines=300)
            info.printer.editFile_delayed(logfname, "wrk", "tb_XeTeXlog", False)
            numruns += 1
            self.rerunReasons = []
            tocfname = os.path.join(self.tmpdir, outfname.replace(".tex", ".toc"))
            if self.res > 0:
                rerun = False
                if os.path.exists(tocfname):
                    os.remove(tocfname)
                break
            rererun = rerun
            for a in cacheexts.keys():
                testdata = cachedata[a]
                fpath = os.path.join(self.tmpdir, outfname.replace(".tex", "."+a))
                cachedata[a] = self.readfile(fpath)
                if testdata != cachedata[a]:
                    if numruns >= self.maxRuns or not cacheexts[a][1]:
                        self.rerunReasons.append(cacheexts[a][0])
                    else:
                        print(_("Rerunning because the {} changed").format(cacheexts[a][0]))
                        rererun = True
                        break
            delayed = os.path.join(self.tmpdir, outfname.replace(".tex", ".delayed"))
            if not rerun and os.path.exists(delayed):
                with open(delayed, encoding="utf-8") as inf:
                    for l in inf.readlines():
                        if l.startswith(r"\Rerun{"):
                            rerun = True
                            print(_("Rerunning because the delayed file asked us to"))
                            break
            if os.path.exists(tocfname):
                tailoring = self.printer.ptsettings.getCollation()
                ducet = tailored(tailoring.text) if tailoring else None
                bklist = self.printer.getBooks()
                copyfile(tocfname, tocfname.replace(".", "_org."))
                toc = TOC(tocfname)
                newtoc = generateTex(toc.createtocvariants(bklist, ducet=ducet))
                with open(tocfname, "w", encoding="utf-8") as outf:
                    outf.write(newtoc)
            if not rererun:
                break

        if not self.res:
            self.printer.incrementProgress(stage="xp")
            tmppdf = self.procpdfFile(outfname, pdffile, info)
            if info["finishing/extraxdvproc"]:
                self.processxdv(outfname.replace(".tex", ".xdv"), self.getxdvname(outfname, info), info)
            cmd = ["xdvipdfmx", "-E", "-V", str(self.args.pdfversion / 10.), "-C", "16", "-v", "-o", tmppdf]
            #if self.ispdfxa == "PDF/A-1":
            #    cmd += ["-z", "0"]
            if self.args.extras & 7:
                cmd.insert(-2, "-" + ("v" * (self.args.extras & 7)))
            with open(outfname.replace(".tex", ".xdvi_log"), "w") as outf:
                runner = call(cmd + [self.getxdvname(outfname, info)], cwd=self.tmpdir, stdout=outf, stderr=outf)
            logger.debug(f"Running: {cmd} for {outfname}")
            if self.args.extras & 1:
                print(f"Subprocess return value: {runner}")
            if isinstance(runner, subprocess.Popen) and runner is not None:
                try:
                    runner.wait()
                    #runner.wait(self.args.timeout)
                except subprocess.TimeoutExpired:
                    print("Timed out!")
                self.res = 4 if runner.returncode else 0
                logger.debug(f"{runner.stdout.decode('UTF-8')}")
            elif isinstance(runner, subprocess.CompletedProcess):
                self.res = 4 if runner.returncode else 0
                logger.debug(f"{runner.stdout}")
            else:
                self.res = 4 if runner else 0
            self.printer.incrementProgress(stage="fn") #Suspect that this was causing it to SegFault (but no idea why)
            if self.res == 0 and not self.procpdf(outfname, pdffile, info, cover=info['cover/makecoverpage'] != '%'):
                self.res = 3
        print("Done")

    def done_job(self, outfname, pdfname, info):
        # Work out what the resulting PDF was called
        startname = None
        logger.debug(f"done_job: {outfname}, {pdfname}, {self.res=}")
        cfgname = info['config/name']
        if cfgname is not None and cfgname != "":
            cfgname = "-"+cfgname
        else:
            cfgname = ""
        if pdfname is not None:
            print(pdfname)
        self.printer.set("l_statusLine", "")
        print(f"{self.res=}")
        if self.res == 0:
            if self.printer.docreatediff:
                basename = self.printer.get("btn_selectDiffPDF")
                if basename == _("Previous PDF (_1)"):
                    basename = None
                ndiffcolor = self.printer.get("col_ndiffColor")
                odiffcolor = self.printer.get("col_odiffColor")
                onlydiffs = self.printer.get("c_onlyDiffs")
                diffpages = int(self.printer.get("s_diffpages") or 0)
                logger.debug(f"diffing from: {basename=} {pdfname=}")
                if basename is None or len(basename):
                    diffname = self.createDiff(pdfname, basename, outfname=self.args.diffoutfile, dpi=self.args.diffdpi,
                                color=odiffcolor, onlydiffs=onlydiffs, oldcolor=ndiffcolor, limit=diffpages)
                    if diffname is not None and not self.noview and self.printer.isDisplay and os.path.exists(diffname):
                        self.printer.onShowPDF(path=diffname)
                        if diffname == pdfname:
                            self.printer.set("l_statusLine", _("No differences found"))
                self.printer.docreatediff = False
            elif not self.noview and self.printer.isDisplay and os.path.exists(pdfname):
                if self.printer.isCoverTabOpen():
                    startname = self.coverfile or pdfname
                else:
                    startname = pdfname

            fname = os.path.join(self.tmpdir, os.path.basename(outfname).replace(".tex", ".log"))
            logger.debug(f"Testing log file {fname}")
            if os.path.exists(fname):
                with open(fname, "r", encoding="utf-8", errors="ignore") as logfile:
                    log = logfile.read()
                smry, msgList, ufPages = summarizeTexLog(log)
                if not self.noview and not self.args.print:
                    self.printer.ufCurrIndex = 0
                    self.printer.ufPages = ufPages
                    sl = self.printer.builder.get_object("l_statusLine")
                    sl.set_text("")
                    sl.set_tooltip_text("")
                if smry["E"] + smry["W"] > 0:
                    summaryLine = f"XeTeX Log Summary: Info: {smry['I']}   Warn: {smry['W']}   Error: {smry['E']}"
                    msgs = "\n".join(msgList)
                    print("{}\n{}".format(summaryLine, msgs))
                    if not self.noview and not self.args.print:
                        if len(msgList) == 1 and "underfilled" in msgs:
                            if "," not in msgs and "-" not in msgs:
                                msgs = re.sub(_("pages"), _("page"), msgs)
                            sl.set_text(msgs)
                            sl.set_tooltip_text(msgs)
                            chkmsg = (_("Check pages:") + msgs.split(':')[1][:50].rstrip("0123456789- ")+" ...") if len(msgs) > 50 else msgs
                            if "," not in chkmsg and "-" not in chkmsg:
                                chkmsg = re.sub(_("pages"), _("page"), chkmsg)
                            self.printer.set("l_statusLine", chkmsg)
                        else:
                            sl.set_text(summaryLine)
                            sl.set_tooltip_text(msgs)
                            self.printer.set("l_statusLine", summaryLine)
                    with open(fname, "a", encoding="utf-8", errors="ignore") as logfile:
                        logfile.write(f"\n{summaryLine}\n{msgs}")
            
                if not self.noview and not self.args.print: # We don't want pop-up messages if running in command-line mode
                    badpgs = re.findall(r'(?i)SOMETHING BAD HAPPENED on page (\d+)\.', "".join(log))
                    if len(badpgs):
                        print(_("Layout problems were encountered on page(s): ") + ", ".join(badpgs))
                        self.printer.doError(_("PDF was created BUT..."),
                            secondary=_("Layout problems were encountered on page(s): ") + ",".join(badpgs) + \
                                  _("\n\nTry changing the PicList and/or AdjList settings to solve issues."), \
                            title=_("PTXprint [{}] - Warning!").format(VersionStr),
                            threaded=True)
            if not self.noview and startname is not None:
                    self.printer.onShowPDF(path=startname)

        elif self.res == 3:
            self.printer.doError(_("Failed to create: ")+re.sub(r"\.tex",r".pdf",outfname),
                    secondary=_("Faulty PDF, could not parse"),
                    title="PTXprint [{}] - Error!".format(VersionStr), threaded=True)
        elif self.res == 4:
            logpath = os.path.join(self.tmpdir, outfname.replace(".tex", ".xdvi_log"))
            if os.path.exists(logpath):
                with open(logpath) as inf:
                    loglines = inf.readlines()
                    if "xdvipdfmx:fatal: Invalid font: -1 (0)\n" in loglines:
                        loglines.append("\n" + _("To fix this error: Use a different font which is not a Variable Font."))
            else:
                loglines = [_("Bad xdvi file, probably failed to load a picture or font")]
            self.printer.doError(_("Failed to create: ")+re.sub(r"\.tex",r".pdf",outfname),
                    secondary="".join(loglines[-12:]),
                    title="PTXprint [{}] - Error!".format(VersionStr), threaded=True)
        elif not self.noview and not self.args.print: # We don't want pop-up messages if running in command-line mode
            finalLogLines = self.parseLogLines()
            self.printer.doError(_("Failed to create: ")+re.sub(r"\.tex",r".pdf",outfname),
                    secondary="".join(finalLogLines[:30]), title="PTXprint [{}] - Error!".format(VersionStr),
                    threaded=True, copy2clip=True)
            self.printer.onIdle(self.printer.showLogFile)
        if len(self.rerunReasons) and self.printer.get("l_statusLine") == "":
            self.printer.set("l_statusLine", _("Rerun to fix: ") + ", ".join(self.rerunReasons))
        self.printer.finished(self.res == 0)
        self.busy = False
        if not self.noview and not self.args.print and self.printer.isDisplay:
            self.printer.builder.get_object("dlg_preview").present()
            spnr = self.printer.builder.get_object("spin_preview")
            if spnr.props.active:  # Check if the spinner is running
                spnr.stop()                
        logger.debug("done_job: Finishing thread")
        unlockme()
        if not self.noview and not self.args.print:
            self.printer.builder.get_object("t_find").set_placeholder_text("Search for settings")

    def parselog(self, fname, rerunp=False, lines=20):
        loglines = []
        rerunres = False
        if not os.path.exists(fname):
            return (loglines, rerunres)
        try:
            with open(fname, "r", encoding="utf-8", errors="ignore") as logfile:
                for i, l in enumerate(logfile.readlines()):
                    if rerunp and l.startswith("PARLOC: Rerun."):
                        rerunres = True
                    loglines.append(l)
                    if len(loglines) > lines:
                        loglines.pop(0)
        except:
            loglines.append("Logfile missing: "+fname)
        return (loglines, rerunres)

    def readfile(self, fname):
        try:
            with open(fname, "r", encoding="utf-8", errors="ignore") as inf:
                res = "".join(inf.readlines())
            return res
        except FileNotFoundError:
            return ""

    def parseLogLines(self):
        # it did NOT finish successfully, so help them troubleshoot what might have gone wrong:
        l = len(self.loglines)
        s = 40 if l > 40 else l
        e = 0
        for i in range(1, s):
            if self.loglines[-i].startswith("Here is how much of TeX's memory you used:"):
                e = i
            if self.loglines[-i].startswith("!"):
                s = i
        finalLogLines = []
        for l in self.loglines[-s:-e]:
            if len(l.strip()):
                finalLogLines.append(l.replace("   ", " "))
        foundmsg = False
        finalLogLines.append("-"*90+"\n")
        for l in reversed(finalLogLines):
            # if l[:1] == "!" and not foundmsg:
            if not foundmsg:
                for m in sorted(_errmsghelp.keys(),key=len, reverse=True):
                    if m in l or l.startswith(m):
                        finalLogLines.append(_errmsghelp[m]+"\n")
                        foundmsg = True
                        break
        if not foundmsg:
            # Try summarizing Log file:
            smry, msgList, ufPages = summarizeTexLog('\n'.join(finalLogLines))
            if smry["E"] > 0:
                msgs = "\n".join(msgList)
                finalLogLines.append(msgs)
            else: # Catch all else kind of message.
                finalLogLines.append(_errmsghelp["Unknown"])
        books = re.findall(r"\d\d(...){}.+?\....".format(self.prjid), "".join(finalLogLines))
        if len(books):
            book = " in {}".format(books[-1])
        else:
            book = ""
        refs = re.findall(r"([1-9]\d{0,2}[.:][1-9]\d{0,2}[^0-9])", "".join(finalLogLines))
        if len(refs):
            finalLogLines.append("References to check{}: {}".format(book, " ".join(refs)))

        texmrkrs = [r"\fi", r"\if", r"\ifx", r"\box", r"\hbox", r"\vbox", r"\else", r"\book", r"\par",
                     r"\edef", r"\gdef", r"\dimen", r"\hsize", r"\relax"]
        allmrkrs = re.findall(r"(\\[a-z0-9]{0,5})[ *\r\n.]", "".join(finalLogLines[-8:]))
        mrkrs = [x for x in allmrkrs if x not in texmrkrs]
        if 0 < len(mrkrs) < 7:
            if len(set(mrkrs) & set([r"\ef", r"\ex", r"\cat", r"\esb"])):
                finalLogLines.append(_("There might be a marker issue in the Extended Study Notes"))

        files = re.findall(r'(?i)([^\\/\n."= ]*?\.(?=jpg|jpeg|tif|tiff|bmp|png|pdf)....?)', "".join(finalLogLines))
        if len(files):
            finalLogLines.append("File(s) to check: {}".format(", ".join(files)))
        return finalLogLines

    def procpdfFile(self, outfname, pdffile, info):
        opath = outfname.replace(".tex", ".prepress.pdf")
        if self.ispdfxa != "Screen":
            return opath
        elif info['finishing/pgsperspread'] is not None and int(info['finishing/pgsperspread']) > 1:
            return opath
        elif info['finishing/inclsettings']:
            return opath
        elif info['cover/makecoverpage'] != '%':
            return opath
        return pdffile

    def procpdf(self, outfname, pdffile, info, **kw):
        for a in ('spotcolor', 'spottolerance', 'pgsperspread', 'sheetsize', 'sheetsinsigntr', 'foldcutmargin', 'foldfirst', 'inclsettings', 'paper/cropmarks', 'document/ifrtl'):
            if '/' in a:
                kw[a[a.find("/")+1:]] = info[a]
            else:
                kw[a] = info['finishing/'+a]
        kw['date'] = info["pdfdate_"]
        def doSettingsZip(zio):
            z = info.printer.createSettingsZip(zio)
            report = checkoutput(["xetex", "--version"], path='xetex')
            z.writestr("_runinfo.txt", report)
            z.close()
        self.coverfile = procpdf(outfname, pdffile, self.ispdfxa, self.printer.doError, doSettingsZip, **kw)
        if self.coverfile is False:
            self.coverfile = None
            return False
        return True

    def createDiff(self, pdfname, basename, outname=None, **kw):
        from ptxprint.pdf.pdfdiff import createDiff
        outname = pdfname[:-4] + "_diff.pdf" if outname is None else outname
        othername = pdfname[:-4] + "_1.pdf" if basename is None else basename
        logger.debug(f"diffing {othername} exists({os.path.exists(othername)}) and {pdfname} exists({os.path.exists(pdfname)})")
        res = createDiff(pdfname, othername, outname, self.printer.doError, **kw)
        if res == 2:
            self.res = 2
        if not str(res).endswith('_diff.pdf'):
            outname = pdfname
        return outname

    def checkForMissingDecorations(self, info):
        deco = {"pageborder" :     "Page Border",
                "sectionheader" :  "Section Heading",
                "endofbook" :      "End of Book",
                "versedecorator" : "Verse Number"}
        warnings = []
        if info.asBool("fancy/enableornaments"):
            for k,v in deco.items():
                if info.asBool("fancy/"+k):
                    ftype = "fancy/{}type".format(k)
                    if ftype not in info.dict or info[ftype] == "file":
                        f = info.dict["fancy/{}pdf".format(k)] or ""
                        if not os.path.exists(f):
                            warnings += ["{} Decorator\n{}\n\n".format(v, f)]
        if info.asBool("paper/ifwatermark"):
            f = info["paper/watermarkpdf"]
            if not os.path.exists(f):
                warnings += ["Watermark\n{}\n\n".format(f)]
        if len(warnings):
            self.printer.doError(_("Warning: Could not locate decorative PDF(s):"),
                    secondary="\n".join(warnings))

    def gatherIllustrations(self, info, jobs, ptfolder, diglots=False):
        self.printer.incrementProgress(stage="gp")
        logger.debug(f"Gathering illustrations: {self.printer.picinfos}")
        picinfos = self.printer.picinfos
        pageRatios = self.usablePageRatios(info)
        tmpPicpath = os.path.join(self.printer.project.printPath(self.printer.cfgid), "tmpPics")
        if not os.path.exists(tmpPicpath):
            picinfos.clear_destinations()
            os.makedirs(tmpPicpath)
        folderList = ["tmpPics", "tmpPicLists"] 
        cropme = info['document/iffigcrop']
        def carefulCopy(p, src, tgt):
            ratio = pageRatios[0 if p['size'].startswith("span") else 1] if p.get('pgpos', 'N') in 'tbhp' else None
            logger.debug(f"carefulcopy {src} -> {tgt} @ {ratio}")
            return self.carefulCopy(ratio, src, tgt, cropme)
        missingPics = []
        if info['document/ifinclfigs'] == 'false':
            # print("NoFigs")
            return []
        picinfos.build_searchlist()
        books = [r[0][0].first.book if r[1] else r[0] for r in jobs] + ["FRT","COV"]
        exclusive = self.printer.get("c_exclusiveFiguresFolder")
        fldr      = self.printer.get("lb_selectFigureFolder", "") if self.printer.get("c_useCustomFolder") else ""
        imgorder  = self.printer.get("t_imageTypeOrder")
        lowres    = self.printer.get("r_pictureRes") == "Low"
        picinfos.srchlist = None
        for j in books:
            logger.debug(f"getsrc&dest for {j}")
            picinfos.getFigureSources(keys=j, exclusive=exclusive, mode=self.ispdfxa,
                                      figFolder=fldr, imgorder=imgorder, lowres=lowres)
            picinfos.set_destinations(fn=carefulCopy, keys=j, cropme=cropme)
        logger.debug(f"{books=}, {[x.fields for x in picinfos.pics.values()]}")
        missingPics = [v['src'] for v in picinfos.get_pics() if v['anchor'][:3] in books and 'destfile' not in v and 'src' in v]
        res = [os.path.join("tmpPics", v['destfile']) for v in picinfos.get_pics() if 'destfile' in v]
        outfname = info.printer.baseTeXPDFnames([r[0][0].first.book if r[1] else r[0] for r in jobs])[0] + ".piclist"
        localPicInfos = picinfos.copy()
        logger.debug(f"{outfname=}, localPicInfos= {[x.fields for x in localPicInfos.pics.values()]}")
        for k, v in list(localPicInfos.items()):
            m = v.get('media', '')
            key = v.get('anchor', '')[:3]
            if m and 'p' not in m:
                del localPicInfos[k]
                continue
            if t := v.get('caption', ''):
                v['caption'] = runChanges(info.changes.get('default', []), key+'CAP', t)
            if t := v.get('ref', ''):
                v['ref'] = runChanges(info.changes.get('default', []), key+'REF', t)
            if diglots:
                for s, dinfo in info['diglots_'].items():
                    if (t := v.get(f'caption{s}', '')):
                        v[f'caption{s}'] = runChanges(dinfo.changes.get('default', []), key+'CAP', t)
                    if (t := v.get(f'ref{s}', '')):
                        v[f'ref{s}'] = runChanges(dinfo.changes.get('default', []), key+'REF', t)
        localPicInfos.out(os.path.join(self.tmpdir, outfname), bks=books, skipkey="disabled", usedest=True, media='p', checks=self.printer.picChecksView)
        res.append(outfname)
        info["document/piclistfile"] = outfname

        if len(missingPics):
            missingPicList = ["{}".format(", ".join(list(set(missingPics))))]
            self.printer.set("l_missingPictureCount", _("({} Missing)").format(len(set(missingPics))))
            self.printer.set("l_missingPictureString", _("Missing Pictures: {}").format("\n".join(missingPicList)))
            logger.debug("Missing Pictures: {}".format("\n".join(missingPicList)))
        else:
            self.printer.set("l_missingPictureCount", _("(0 Missing)"))
            self.printer.set("l_missingPictureString", "")
        self.printer.incrementProgress(stage="lo")
        logger.debug("Illustrations gathered")
        return res

    def getBorder(self, box, start, end, fn):
        if start > end:
            it = range(box[start]-1, box[end]-1, -1)
        else:
            it = range(box[start], box[end])
        otheri = 0 if (start & 1) else 1
        others = box[otheri]
        othere = box[otheri+2]
        for t in it:
            score = sum(fn(t, i) for i in range(others, othere))
            # 8 = 256 * 5% (approx)
            if score > 8 * (othere - others):
                break
        return t

    def cropBorder(self, im):
        try:
            bwim = im.convert("L").load()
        except OSError:
            return im
        box = im.getbbox()
        cbox = []
        cbox.append(self.getBorder(box, 0, 2, lambda x, y: bwim[x, y]))
        cbox.append(self.getBorder(box, 1, 3, lambda y, x: bwim[x, y]))     # top is 0
        cbox.append(self.getBorder(box, 2, 0, lambda x, y: bwim[x, y]))
        cbox.append(self.getBorder(box, 3, 1, lambda y, x: bwim[x, y]))
        cbox = tuple(cbox)
        if cbox != box:
            return im.crop(cbox)
        return im

    def convertToJPGandResize(self, ratio, infile, outfile, cropme):
        if self.ispdfxa in _pdfmodes['cmyk'] and not self.printer.get("c_figplaceholders"):
            fmt = "CMYK"
        else:
            fmt = "RGB"
        with open(infile,"rb") as inf:
            rawdata = inf.read()
        newinf = cStringIO(rawdata)
        im = Image.open(newinf)
        if cropme:
            im = self.cropBorder(im)
        p = im.load()
        iw = im.size[0]
        ih = im.size[1]
        if ratio is not None and iw/ih < ratio or im.mode == "RGBA":
            onlyRGBAimage = im.convert("RGBA") if im.mode != "RGBA" else im
            newWidth = int(ih * ratio) if ratio is not None and iw/ih < ratio else iw
            compimg = Image.new("RGBA", (newWidth, ih), color=(255, 255, 255, 255))
            compimg.alpha_composite(onlyRGBAimage, (int((newWidth-iw)/2),0))
            iw = compimg.size[0]
            ih = compimg.size[1]
            newimage = compimg.convert(fmt)
        elif im.mode != fmt:
            newimage = im.convert(fmt)
        else:
            newimage = im
        if fmt == "CMYK":
            newimage = self.cmytocmyk(newimage)
        newimage.save(outfile)
        return True

    def cmytocmyk(self, im):
        #for y in range(im.height):
        #    for x in range(im.width):
        #        im.putpixel((x, y), self._cmytocmyk(*im.getpixel((x, y))))
        #return im
        img = np.asarray(im).copy()
        if img.shape[-1] == 3:
            z = np.zeros((img.shape[0], img.shape[1], 1), dtype=np.uint8)
            img.concatenate((img, z), axis=3)
            return im
        dk = img.min(axis=2, where = [True, True, True, False], initial=255)
        dko = 255 - dk
        newk = img[:,:,3] + dk
        bigmask = newk[:,:] > 255
        dk[bigmask] = dko[bigmask]
        newk[bigmask] = 255
        img[:,:,3] = newk
        for i in range(3):
            img[:,:,i] -= dk 
        res = Image.fromarray(img.astype(np.uint8), 'CMYK')
        return res

    @staticmethod
    def _cmytocmyk(c, m, y, k):
        dk = min(c, m, y)
        if dk + k > 255:
            dk = 255 - k
            k = 255
        else:
            k += dk
        return (c - dk, m - dk, y - dk, k)

    def carefulCopy(self, ratio, srcpath, tgtfile, cropme):
        tmpPicPath = os.path.join(self.printer.project.printPath(self.printer.cfgid), "tmpPics")
        tgtpath = os.path.join(tmpPicPath, tgtfile)
        if os.path.splitext(srcpath)[1].lower().startswith(".pdf"):
            log.setLevel(logging.CRITICAL)
            trailer = PdfReader(srcpath)
            writer = PdfWriter(tgtpath)
            writer.trailer = trailer
            writer.write()
            return os.path.basename(tgtpath)
        try:
            im = Image.open(srcpath)
            iw = im.size[0]
            ih = im.size[1]
        except OSError:
            print(("Failed to get size of (image) file:"), srcpath)
        # If either the source image is a TIF (or) the proportions aren't right for page dimensions 
        # then we first need to convert to a JPG and/or pad with which space on either side
        if cropme or (ratio is not None and iw/ih < ratio) \
                  or os.path.splitext(srcpath)[1].lower() in (".tif", ".tiff", ".png"):
            tgtpath = os.path.splitext(tgtpath)[0]+".jpg"
            #try:
            self.convertToJPGandResize(ratio, srcpath, tgtpath, cropme)
            #except: # MH: Which exception should I try to catch?
            #    print(_("Error: Unable to convert/resize image!\nImage skipped:"), srcpath)
            #    return os.path.basename(tgtpath)
        else:
            try:
                copyfile(srcpath, tgtpath)
            except OSError:
                print(_("Error: Unable to copy {}\n       image to {} in tmpPics folder"), srcpath, tgtpath)
                return os.path.basename(tgtpath)
        return os.path.basename(tgtpath)

    def usablePageRatios(self, info):
        pageHeight = convert2mm(info.dict["paper/height"])
        pageWidth = convert2mm(info.dict["paper/width"])
        # print("pageHeight =", pageHeight, "  pageWidth =", pageWidth)
        margin = convert2mm(info.dict["paper/margins"])
        # print("margin =", margin)
        sideMarginFactor = 1.0
        middleGutter = float(info.dict["document/colgutterfactor"])/3
        bindingGutter = float(info.dict["paper/gutter"]) if info.asBool("paper/ifaddgutter") else 0
        topMarginFactor = info.dict["paper/topmarginfactor"]
        bottomMarginFactor = info.dict["paper/bottommarginfactor"]
        lineSpacingFactor = float(info.dict["paragraph/linespacingfactor"])
        # print("lineSpacingFactor=", lineSpacingFactor)
        # ph = pageheight, pw = pagewidth
        # print("margin={} topMarginFactor={} bottomMarginFactor={}".format(margin, topMarginFactor, bottomMarginFactor))
        ph = pageHeight - (margin * float(topMarginFactor)) - (margin * float(bottomMarginFactor)) - 22
        pw1 = pageWidth - bindingGutter - (2*(margin*sideMarginFactor))                       # single-col layout
        if info.dict["paper/columns"] == "2":
            pw2 = int(pageWidth - middleGutter - bindingGutter - (2*(margin*sideMarginFactor)))/2 # double-col layout & span images
        else:
            pw2 = pw1
        # print("Usable ph: {}mm".format(ph), "     Usable 1-col pw1: {}mm   Usable 2-col pw2: {}mm".format(pw2, pw1))
        pageRatios = (pw1/ph, pw2/ph)
        # print("Page Ratios = ", pageRatios)
        return pageRatios

