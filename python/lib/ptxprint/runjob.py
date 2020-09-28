import os, sys, re, subprocess
from PIL import Image
from io import BytesIO as cStringIO
from shutil import copyfile, rmtree
from threading import Thread
from ptxprint.runner import call, checkoutput
from ptxprint.texmodel import TexModel, universalopen
from ptxprint.ptsettings import ParatextSettings
from ptxprint.view import ViewModel, VersionStr, refKey
from ptxprint.font import getfontcache
from ptxprint.usfmerge import usfmerge
from ptxprint.utils import _

_errmsghelp = {
"! TeX capacity exceeded, sorry":        "Uh oh! You've pushed TeX too far! Try turning Hyphenation off, or contact support.\n",
"! Paratext stylesheet":                 "Check if the stylesheet specified on the Advanced tab exists.\n",
"! Unable to load picture":              "Check if picture file is located in 'Figures', 'local\\figures' or a\n" +\
                                         "specified folder. Also try the option 'Omit Missing Pictures'\n",
"! Unable to load picture or PDF file":  "Check if image/PDF file is available on the system.\n" +
                                         "If you have specified one or more Front/Back matter PDFs or a Watermark PDF\n" +
                                         "then ensure that the PDF(s) exist(s); OR uncheck those options (Advanced tab).\n",
"! Missing control sequence inserted.":  "Fallback font probably being applied to text in a footnote (not permitted!)\n",
"! Missing number, treated as zero.":    "Related to USFM3 illustration markup\n",
"! Undefined control sequence.":         "This is related to a USFM marker error (such as an unsupported marker)\n" +\
                                         "Try 'Run Basic Checks' in Paratext\n",
"! Illegal unit of measure (pt inserted).":    "One of the settings in the Stylesheet may be missing the units.\n" +\
                                         "To confirm that this is a stylesheet issue, temporarily turn off Stylesheets.\n" +\
                                         "Then, check any recent changes to the Stylesheets (on Advanced tab) and try again.\n",
"! File ended while scanning use of":    "Try turning off PrintDraftChanges.txt and both Stylesheets on Advanced tab.\n",
"! Output loop---25 consecutive dead cycles.":  "Unknown cause. Try changing one or more settings or contact support.\n",
"! Paratext stylesheet":                 "Try turning off the ptxprint-mods stylesheet\n",
"! File ended while scanning use of \iotableleader.": "Problem with Formatting Intro Outline\n" +\
                                         "Try disabling option 'Right-Align \ior with tabbed leaders' on the Body tab\n",
"! Emergency stop.":                     "Probably a TeX macro problem - contact support, or post a bug report\n",
"! Not a letter.":                       "Possible fault in the hyphenation file\n" +\
                                         "Try turning off Hyphenate option located on the Body tab\n",
"! Font \extrafont":                     "Fallback Font issue - set a font on the Body tab.\n" +\
                                         "(Turn off the option 'Use Fallback Font' or specify a valid font)\n",
"! Font":                                "Font related issue. The most likely reason for this error is that\n" +\
                                         "the selected font has not been installed for all users. See FAQ.\n",
"! Too many }'s":                        "Possibly a TeX macro issue - contact support, or post a bug report\n",
"! This can't happen (page)":            "Possibly a TeX macro issue - contact support, or post a bug report\n",
"! I can't find file `paratext2.tex'.":  "Possibly a faulty installation.\n",
"! I can't find file `ptx-tracing.tex'.":"Possibly a faulty installation.\n",
"Runaway argument?":                     "Unknown issue. Maybe related to Right-aligned tabbed leaders\n" +\
                                         "Try turning off PrintDraftChanges.txt and both Stylesheets\n",
"Unknown":                               "Sorry, there is no diagnostic help for this error.\n" +\
                                         "Ensure that the Basic Checks (in Paratext) pass for all books in list.\n" +\
                                         "Try turning off various settings, and disable Changes or Stylesheets.\n" +\
                                         "If peripheral books are selected, try excluding those."
}
# \def\LineSpacingFactor{{{paragraph/linespacingfactor}}}
# \def\VerticalSpaceFactor{{1.0}}
# \baselineskip={paragraph/linespacing}pt {paragraph/varlinespacing} {paragraph/linemax} {paragraph/linemin}
# \XeTeXinterwordspaceshaping = {document/spacecntxtlztn}
# %\extrafont  %% This will be replaced by code for the fallback fonts to be used for special/missing characters

def base(fpath):
    doti = fpath.rfind(".")
    return os.path.basename(fpath[:doti])

# https://sites.google.com/a/lci-india.org/typesetting/home/illustrations/where-to-find-illustrations
def codeLower(fpath):
    cl = re.findall(r"(?i)_?((?=ab|cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib)..\d{5})[abc]?$", base(fpath))
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

_diglot = {
"ifusediglotcustomsty_":    "project/ifusecustomsty",
"ifusediglotmodsty_":       "project/ifusemodssty",
"diglot/colorfonts" :       "document/ifcolorfonts",
"diglot/ifrtl" :            "document/ifrtl",
"diglot/fontfactor" :       "paper/fontfactor",
"diglot/linespacingfactor": "paragraph/linespacingfactor",
"diglot/iflinebreakon" :    "document/iflinebreakon",
"diglot/linebreaklocale" :  "document/linebreaklocale",
"diglot/useglyphmetrics" :  "paragraph/useglyphmetrics",

"diglot/fontregular" :      "fontregular",
"diglot/fontregeng" :       "fontregular/engine",
"diglot/texfeatures" :      "font/texfeatures",
"diglot/docscript" :        "document/script",
"diglot/docdigitmapping" :  "document/digitmapping",
                            
"diglot/fontbold" :         "fontbold",
"diglot/fontboldeng" :      "fontbold/engine",
"diglot/boldembolden" :     "fontbold/embolden",
"diglot/boldslant" :        "fontbold/slant",
                            
"diglot/fontitalic" :       "fontitalic",
"diglot/fontitaleng" :      "fontitalic/engine",
"diglot/italembolden" :     "fontitalic/embolden",
"diglot/italslant" :        "fontitalic/slant",
                            
"diglot/fontbolditalic" :   "fontbolditalic",
"diglot/fontbolditaleng" :  "fontbolditalic/engine",
"diglot/bolditalembolden" : "fontbolditalic/embolden",
"diglot/boldital/slant" :   "fontbolditalic/slant",

"diglot/ifshowversenums" :  "document/ifshowversenums",
"diglot/includefootnotes" : "notes/includefootnotes",
"diglot/fnfontsize" :       "notes/fnfontsize",
"diglot/fnlinespacing" :    "notes/fnlinespacing",
"diglot/includexrefs" :     "notes/includexrefs",
"diglot/ifblendfnxr" :      "notes/ifblendfnxr"
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
    def __init__(self, printer, scriptsdir, macrosdir, userconfig, args):
        self.scriptsdir = scriptsdir
        self.macrosdir = macrosdir
        self.printer = printer
        self.userconfig = userconfig
        self.tempFiles = []
        self.tmpdir = "."
        self.maxRuns = 1
        self.changes = None
        self.args = args
        self.res = 0
        self.thread = None
        self.busy = False

    def doit(self):
        if not lockme(self):
            return False
        self.texfiles = []
        info = TexModel(self.printer, self.args.paratext, self.printer.ptsettings, self.printer.prjid)
        info.debug = self.args.debug
        self.tempFiles = []
        self.prjid = info.dict["project/id"]
        self.prjdir = os.path.join(self.args.paratext, self.prjid)
        if self.prjid is None or not len(self.prjid):     # can't print no project
            return
        self.texfiles += info.generateNestedStyles()
        self.tmpdir = os.path.join(self.prjdir, 'PrintDraft') if info.asBool("project/useprintdraftfolder") \
                                                                 or self.args.directory is None else self.args.directory
        os.makedirs(self.tmpdir, exist_ok=True)
        jobs = self.printer.getBooks()

        self.books = []
        if self.printer.get("c_onlyRunOnce"):
            self.maxRuns = 1
        else:
            self.maxRuns = 5
        self.changes = None
        self.checkForMissingDecorations(info)
        if info.asBool("document/ifinclfigs"):
            self.texfiles += self.gatherIllustrations(info, jobs, self.args.paratext)
        
        if info.asBool("project/combinebooks"):
            joblist = [jobs]
        else:
            joblist = [[j] for j in jobs]

        isDiglot = self.printer.get("c_diglot")
        if isDiglot:
            digfraction = info.dict["document/diglotprifraction"]
            digprjid = info.dict["document/diglotsecprj"]
            digcfg = info.dict["document/diglotsecconfig"]
            digprjdir = os.path.join(self.args.paratext, digprjid)
            if digprjid is None or not len(digprjid):     # can't print no project
                return
            digptsettings = ParatextSettings(self.args.paratext, digprjid)
            digprinter = ViewModel(self.args.paratext, self.printer.working_dir, self.userconfig, self.macrosdir)
            digprinter.setPrjid(digprjid)
            if digcfg is not None and digcfg != "":
                digprinter.setConfigId(digcfg)
            diginfo = TexModel(digprinter, self.args.paratext, digptsettings, digprjid)
            self.texfiles += sum((self.digdojob(j, info, diginfo, digprjid, digprjdir) for j in joblist), [])
        else: # Normal (non-diglot)
            self.texfiles += sum((self.dojob(j, info) for j in joblist), [])

    def done_job(self, outfname, info):
        # Work out what the resulting PDF was called
        cfgname = info['config/name']
        if cfgname is not None and cfgname != "":
            cfgname = "-"+cfgname
        else:
            cfgname = ""
        pdfname = os.path.join(self.tmpdir, outfname.replace(".tex", ".pdf"))
#        if len(jobs) > 1 and info.asBool("project/combinebooks"):
#            pdfname = os.path.join(self.tmpdir, "ptxprint{}-{}_{}{}.pdf".format(cfgname, jobs[0], jobs[-1], self.prjid))
#        else:
#            pdfname = os.path.join(self.tmpdir, "ptxprint{}-{}{}.pdf".format(cfgname, jobs[0], self.prjid))
        # Check the return code to see if generating the PDF was successful before opening the PDF
        print(pdfname)
        if self.res == 0:
            if self.printer.isDisplay and os.path.exists(pdfname):
                if sys.platform == "win32":
                    os.startfile(pdfname)
                elif sys.platform == "linux":
                    subprocess.call(('xdg-open', pdfname))
                # Only delete the temp files if the PDF was created AND the user did NOT select to keep them
            if not info.asBool("project/keeptempfiles"):
                self.removeTempFiles(self.texfiles)
            else:
                self.printer.tempFiles = self.texfiles

            if not self.args.print: # We don't want pop-up messages if running in command-line mode
                fname = os.path.join(self.tmpdir, pdfname.replace(".pdf", ".log"))
                if os.path.exists(fname):
                    with open(fname, "r", encoding="utf-8", errors="ignore") as logfile:
                        log = logfile.read() # unlike other places, we *do* want the entire log file
                    badpgs = re.findall(r'(?i)SOMETHING BAD HAPPENED on page (\d+)\.', "".join(log))
                    if len(badpgs):
                        print(_("Layout problems were encountered on page(s): ") + ", ".join(badpgs))
                        self.printer.doError(_("PDF was created BUT..."),
                            secondary=_("Layout problems were encountered on page(s): ") + ",".join(badpgs) + \
                                  _("\n\nTry changing the PicList and/or AdjList settings to solve issues."), \
                                  title=_("PTXprint [{}] - Warning!").format(VersionStr),
                            threaded=True)

        elif not self.args.print: # We don't want pop-up messages if running in command-line mode
            finalLogLines = self.parseLogLines()
            self.printer.doError(_("Failed to create: ")+re.sub(r".+[\\/](.+\.pdf)",r"\1",pdfname),
                    secondary="".join(finalLogLines[-20:]), title="PTXprint [{}] - Error!".format(VersionStr))
            self.printer.onIdle(self.printer.showLogFile)
        self.printer.finished()
        self.busy = False
        unlockme()

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
            with open(fname, "r", encoding="utf-8") as inf:
                res = "".join(inf.readlines())
            return res
        except FileNotFoundError:
            return ""

    def parseLogLines(self):
        # it did NOT finish successfully, so help them troubleshoot what might have gone wrong:
        finalLogLines = self.loglines[-30:-10]
        foundmsg = False
        finalLogLines.append("-"*90+"\n")
        for l in finalLogLines:
            if l[:1] == "!" and not foundmsg:
                for m in sorted(_errmsghelp.keys(),key=len, reverse=True):
                    if m in l:
                        if l[:-1] != m:
                            finalLogLines.append("{}\n".format(m))
                        finalLogLines.append(_errmsghelp[m])
                        foundmsg = True
                        break
        if not foundmsg:
            finalLogLines.append(_errmsghelp["Unknown"])
        books = re.findall(r"\d\d(...){}.+?\....".format(self.prjid), "".join(finalLogLines))
        if len(books):
            book = " in {}".format(books[-1])
        else:
            book = ""
        refs = re.findall(r"([1-9]\d{0,2}[.:][1-9]\d{0,2}[^0-9])", "".join(finalLogLines))
        if len(refs):
            finalLogLines.append("\nReferences to check{}: {}".format(book, " ".join(refs)))

        texmrkrs = [r"\fi", "\if", "\ifx", "\\box", "\\hbox", "\\vbox", "\else", "\\book", "\\par",
                     "\\edef", "\\gdef", "\\dimen" "\\hsize", "\\relax"]
        allmrkrs = re.findall(r"(\\[a-z0-9]{0,5})[ *\r\n.]", "".join(finalLogLines[-8:]))
        mrkrs = [x for x in allmrkrs if x not in texmrkrs]
        if 0 < len(mrkrs) < 7:
            if "\ef" in mrkrs or "\ex" in mrkrs:
                finalLogLines.append("Sorry, Study Bible Markup (\ef \ex etc.) is not yet supported!")
            # else:
                # finalLogLines.append("\nMarkers to check: {}".format(", ".join(mrkrs)))

        files = re.findall(r'(?i)([^\\/\n."= ]*?\.(?=jpg|jpeg|tif|tiff|bmp|png|pdf)....?)', "".join(finalLogLines))
        if len(files):
            finalLogLines.append("\nFile(s) to check: {}".format(", ".join(files)))
        return finalLogLines

    def dojob(self, jobs, info, logbuffer=None):
        donebooks = []
        for b in jobs:
            out = info.convertBook(b, self.tmpdir, self.prjdir)
            donebooks.append(out)
        self.books += donebooks
        info["project/bookids"] = jobs
        info["project/books"] = donebooks
        return [os.path.join(self.tmpdir, out)] + self.sharedjob(jobs, info, logbuffer=logbuffer)

    def digdojob(self, jobs, info, diginfo, digprjid, digprjdir, logbuffer=None):
        texfiles = []
        donebooks = []
        digdonebooks = []
        _digSecSettings = ["paper/pagesize", "paper/height", "paper/width", "paper/margins",
                           "paper/sidemarginfactor", "paper/topmarginfactor", "paper/bottommarginfactor",
                           "header/headerposition", "header/footerposition", "header/ruleposition",
                           "document/ch1pagebreak", "document/bookintro", "document/introoutline", 
                           "document/parallelrefs", "document/elipsizemptyvs", "notes/iffootnoterule",
                           "notes/ifblendfnxr", "notes/includefootnotes", "notes/includexrefs", 
                           "notes/fnparagraphednotes", "notes/xrparagraphednotes", "document/filterglossary", 
                           "document/chapfrom", "document/chapto", "document/ifcolorfonts"]
        diginfo["project/bookids"] = jobs
        diginfo["project/books"] = digdonebooks
        diginfo["document/ifdiglot"] = "%"
        diginfo["footer/ftrcenter"] = "-empty-"
        diginfo["footer/ifftrtitlepagenum"] = "%"
        diginfo["fancy/pageborder"] = "%"
        diginfo["document/clsinglecol"] = False
        diginfo["snippets/diglot"] = False
        docdir = os.path.join(info["/ptxpath"], info["project/id"], "PrintDraft")
        for k in _digSecSettings:
            diginfo[k]=info[k]
        syntaxErrors = []
        for b in jobs:
            out = info.convertBook(b, self.tmpdir, self.prjdir)
            digout = diginfo.convertBook(b, self.tmpdir, digprjdir)
            donebooks.append(out)
            digdonebooks.append(digout)
            
            # Now merge the secondary text (right) into the primary text (left) 
            left = os.path.join(self.tmpdir, out)
            right = os.path.join(self.tmpdir, digout)
            outFile = re.sub(r"^([^.]*).(.*)$", r"\1-diglot.\2", left)
            logFile = os.path.join(self.tmpdir, "ptxprint-merge.log")

            sheetsa = info.printer.getStyleSheets()
            sheetsb = diginfo.printer.getStyleSheets()
            try:
                usfmerge(left, right, outFile, stylesheetsa=sheetsa, stylesheetsb=sheetsb)
            except IndexError as e:
                syntaxErrors.append("{} {} line:{}".format(self.prjid, b, str(e)))
            except Exception as e:
                print(self.prjid, b, str(e).split('line', maxsplit=1)[1])
                syntaxErrors.append("{} {} line:{}".format(self.prjid, b, str(e).split('line', maxsplit=1)[1]))
            for f in [left, right, outFile, logFile]:
                texfiles += [os.path.join(self.tmpdir, f)]
        if len(syntaxErrors):
            self.printer.doError(_("Failed to merge texts due to a Syntax Error:"),
            secondary="\n".join(syntaxErrors)+_("\n\nIf original USFM text is correct, then check "+ \
                                                    "if PrintDraftChanges.txt has caused the error(s)."),
            title=_("PTXprint [{}] - Diglot Merge Error!").format(VersionStr))

        info["project/bookids"] = jobs
        info["project/books"] = donebooks
        self.books += digdonebooks

        # Pass all the needed parameters for the snippet from diginfo to info
        for k,v in _diglot.items():
            info[k]=diginfo[v]
            # print(k, v, diginfo[v])
        info["document/diglotcfgrpath"] = os.path.relpath(diginfo.printer.configPath(diginfo.printer.configName()), docdir).replace("\\","/")
        texfiles += info.generateNestedStyles(diglot=True)
        texfiles += self.sharedjob(jobs, info, logbuffer=logbuffer, extra="-diglot")
        return texfiles

    def sharedjob(self, jobs, info, prjid=None, prjdir=None, logbuffer=None, extra=""):
        if prjid is None:
            prjid = self.prjid
        if prjdir is None:
            prjdir = self.prjdir
        cfgname = info['config/name']
        if cfgname is None or cfgname == "":
            cfgname = ""
        else:
            cfgname = "-" + cfgname
        if len(jobs) > 1:
            outfname = "ptxprint{}-{}_{}{}.tex".format(cfgname, jobs[0], jobs[-1], prjid)
        else:
            outfname = "ptxprint{}-{}{}.tex".format(cfgname, jobs[0], prjid)
        info.update()
        with open(os.path.join(self.tmpdir, outfname), "w", encoding="utf-8") as texf:
            texf.write(info.asTex(filedir=self.tmpdir, jobname=outfname.replace(".tex", ""), extra=extra))
        os.putenv("hyph_size", "32749")     # always run with maximum hyphenated words size (xetex is still tiny ~200MB resident)
        os.putenv("stack_size", "32768")    # extra input stack space (up from 5000)
        ptxmacrospath = os.path.abspath(os.path.join(self.scriptsdir, "..", "..", "src"))
        if not os.path.exists(ptxmacrospath):
            for b in (getattr(sys, 'USER_BASE', '.'), sys.prefix):
                if b is None:
                    continue
                ptxmacrospath = os.path.abspath(os.path.join(b, 'ptx2pdf'))
                if os.path.exists(ptxmacrospath):
                    break

        pathjoin = (";" if sys.platform=="win32" else ":").join
        envtexinputs = os.getenv("TEXINPUTS")
        texinputs = [envtexinputs] if envtexinputs is not None and len(envtexinputs) else []
        texinputs += [os.path.abspath(self.tmpdir), ptxmacrospath]
        if sys.platform != "win32":
            texinputs += ["/usr/share/ptx2pdf/texmacros"]
        os.putenv('TEXINPUTS', pathjoin(texinputs))
        # print("TEXINPUTS=",os.getenv('TEXINPUTS'))
        miscfonts = getfontcache().fontpaths
        miscfonts.append(ptxmacrospath)
        miscfonts.append(os.path.join(prjdir, "shared"))
        if len(miscfonts):
            os.putenv("MISCFONTS", pathjoin(miscfonts))
        self.thread = Thread(target=self.run_xetex, args=(outfname, info, logbuffer))
        self.busy = True
        self.thread.start()
        return [os.path.join(self.tmpdir, outfname)]

    def wait(self):
        if self.busy:
            self.thread.join()
        return self.res

    def run_xetex(self, outfname, info, logbuffer):
        numruns = self.maxRuns
        while numruns > 0:
            self.printer.incrementProgress()
            if info["document/toc"] != "%":
                tocdata = self.readfile(os.path.join(self.tmpdir, outfname.replace(".tex", ".toc")))
            cmd = ["xetex", "--halt-on-error"]
            if self.args.testing:
                cmd += ["-no-pdf"]
            runner = call(cmd + [outfname], cwd=self.tmpdir, logbuffer=logbuffer)
            if isinstance(runner, subprocess.Popen) and runner is not None:
                try:
                    runner.wait(self.args.timeout)
                except subprocess.TimeoutExpired:
                    print("Timed out!")
                self.res = runner.returncode
            else:
                self.res = runner
            print("cd {}; xetex {} -> {}".format(self.tmpdir, outfname, self.res))
            logfname = outfname.replace(".tex", ".log")
            (self.loglines, rerun) = self.parselog(os.path.join(self.tmpdir, logfname), rerunp=True, lines=300)
            info.printer.editFile_delayed(logfname, "wrk", "scroll_XeTeXlog", False)
            if self.res:
                break
            elif info["document/toc"] != "%" and not rerun:
                tocndata = self.readfile(os.path.join(self.tmpdir, outfname.replace(".tex", ".toc")))
                rerun = tocdata != tocndata
                if rerun:
                    print(_("Rerunning because the Table of Contents was updated"))
                else:
                    break
            elif rerun:
                print(_("Rerunning because inline chapter numbers moved"))
            else:
                break
            numruns -= 1
        print("Done")
        self.done_job(outfname, info)

    def checkForMissingDecorations(self, info):
        deco = {"pageborder" :     "Page Border",
                "sectionheader" :  "Section Heading",
                "endofbook" :      "End of Book",
                "versedecorator" : "Verse Number"}
        warnings = []
        if info.asBool("fancy/enableborders"):
            for k,v in deco.items():
                if info.asBool("fancy/"+k):
                    f = info.dict["fancy/{}pdf".format(k)] or ""
                    if not os.path.exists(f):
                        warnings += ["{} Decorator\n{}\n\n".format(v, f)]
            if len(warnings):
                self.printer.doError(_("Warning: Could not locate decorative PDF(s):"),
                        secondary="\n".join(warnings))

    def gatherIllustrations(self, info, jobs, ptfolder):
        pageRatios = self.usablePageRatios(info)
        tmpPicpath = os.path.join(self.printer.working_dir, "tmpPics")
        folderList = ["tmpPics", "tmpPicLists"] 
        try:
            self.removeTmpFolders(self.printer.working_dir, folderList, mkdirs=True)
        except PermissionError:
            print("Warning: Couldn't Remove Temporary Folders - is a temp file open?")
            
        def carefulCopy(p, src, tgt):
            ratio = pageRatios[0 if p['size'].startswith("span") else 1]
            return self.carefulCopy(ratio, src, tgt)
        missingPics = []
        res = []
        for j in jobs:
            pi, mp = self.printer.generateNProcPicLists(j, \
                                os.path.join(self.printer.working_dir, "tmpPicLists"), carefulCopy, isTemp=True)
            missingPics += mp
            res += [v['dest file'] for v in pi.values() if 'dest file' in v]
            
        if len(missingPics):
            missingPicList = ["{}".format(", ".join(list(set(missingPics))))]
            self.printer.set("l_missingPictureCount", "({} Missing)".format(len(set(missingPics))))
            self.printer.set("l_missingPictureString", "Missing Pictures: {}".format("\n".join(missingPicList)))
        else:
            self.printer.set("l_missingPictureCount", "(0 Missing)")
            self.printer.set("l_missingPictureString", "")
        return res

    def convertToJPGandResize(self, ratio, infile, outfile):
        white = (255, 255, 255, 255)
        with open(infile,"rb") as inf:
            rawdata = inf.read()
        newinf = cStringIO(rawdata)
        im = Image.open(newinf)
        try:
            p = im.load()
            onlyRGBAimage = im.convert('RGBA')
            iw = im.size[0]
            ih = im.size[1]
        except OSError:
            print(_("Failed to convert (image) file:"), srcpath)
            return
        # print("Orig ih={} iw={}".format(ih, iw))
        # print("iw/ih = ", iw/ih)
        if iw/ih < ratio:
            # print(infile)
            newWidth = int(ih * ratio)
            newimg = Image.new("RGBA", (newWidth, ih), color=white)
            newimg.alpha_composite(onlyRGBAimage, (int((newWidth-iw)/2),0))
            iw = newimg.size[0]
            ih = newimg.size[1]
            # print(">>>>>> Resized: ih={} iw={}".format(ih, iw))
            onlyRGBimage = newimg.convert('RGB')
            onlyRGBimage.save(outfile)
        else:
            onlyRGBimage = onlyRGBAimage.convert('RGB')
            onlyRGBimage.save(outfile)

    def carefulCopy(self, ratio, srcpath, tgtfile):
        tmpPicPath = os.path.join(self.printer.working_dir, "tmpPics")
        tgtpath = os.path.join(tmpPicPath, tgtfile)
        try:
            im = Image.open(srcpath)
            iw = im.size[0]
            ih = im.size[1]
        except OSError:
            print(("Failed to get size of (image) file:"), srcpath)
            return srcpath
        # If either the source image is a TIF (or) the proportions aren't right for page dimensions 
        # then we first need to convert to a JPG and/or pad with which space on either side
        if iw/ih < ratio or os.path.splitext(srcpath)[1].lower().startswith(".tif"): # (.tif or .tiff)
            tgtpath = os.path.splitext(tgtpath)[0]+".jpg"
            try:
                self.convertToJPGandResize(ratio, srcpath, tgtpath)
            except: # MH: Which exception should I try to catch?
                print(_("Error: Unable to convert/resize image!\nImage skipped:"), srcpath)
                return srcpath
        else:
            try:
                copyfile(srcpath, tgtpath)
            except OSError:
                print(_("Error: Unable to copy {}\n       image to {} in tmpPics folder"), srcpath, tgtpath)
                return srcpath
        return tgtpath

    def removeTempFiles(self, texfiles):
        notDeleted = []
        # MH: Should we try to remove the generated Nested files (now that they are stored along with the config)?
        # What impact does that have on Paratext's S/R (cluttering)
        # n = os.path.join(self.tmpdir, "NestedStyles.sty")
        # if os.path.exists(n):
            # try:
                # os.remove(n)
            # except:
                # notDeleted += [n]
        for extn in ('delayed','parlocs','notepages', 'tex', 'log'):
            for t in set(texfiles):
                delfname = os.path.join(self.tmpdir, t.replace(".tex", "."+extn))
                if os.path.exists(delfname):
                    try:
                        os.remove(delfname)
                    except OSError:
                        notDeleted += [delfname]
        for f in self.books:
            delfname = os.path.join(self.tmpdir, f)
            if os.path.exists(delfname):
                try:
                    os.remove(delfname)
                except OSError:
                    notDeleted += [delfname]
        folderList = ["tmpPics", "tmpPicLists"] 
        notDeleted += self.removeTmpFolders(self.tmpdir, folderList)
        if len(notDeleted):
            self.printer.doError(_("Warning: Could not delete\ntemporary file(s) or folder(s):"),
                    secondary="\n".join(set(notDeleted)))

    def removeTmpFolders(self, base, delFolders, mkdirs=False):
        notDeleted = []
        for p in delFolders:
            path2del = os.path.join(base, p)
            if os.path.exists(path2del):
                try:
                    rmtree(path2del)
                except OSError:
                    notDeleted += [path2del]
            if mkdirs:
                os.makedirs(path2del)
        return notDeleted

    def usablePageRatios(self, info):
        pageHeight = self.convert2mm(info.dict["paper/height"])
        pageWidth = self.convert2mm(info.dict["paper/width"])
        # print("pageHeight =", pageHeight, "  pageWidth =", pageWidth)
        margin = self.convert2mm(info.dict["paper/margins"])
        # print("margin =", margin)
        sideMarginFactor = float(info.dict["paper/sidemarginfactor"])
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

    def convert2mm(self, measure):
        _unitConv = {'mm':1, 'cm':10, 'in':25.4, '"':25.4}
        units = _unitConv.keys()
        num = float(re.sub(r"([0-9\.]+).*", r"\1", str(measure)))
        unit = str(measure)[len(str(num)):].strip(" ")
        return (num * _unitConv[unit]) if unit in units else num
