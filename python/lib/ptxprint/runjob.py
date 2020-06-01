import os, sys, re, subprocess
import img2pdf
from shutil import copyfile, rmtree
from ptxprint.runner import call, checkoutput
from ptxprint.texmodel import TexModel, universalopen
from ptxprint.ptsettings import ParatextSettings
from ptxprint.view import ViewModel, VersionStr

_errmsghelp = {
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
"! Output loop---25 consecutive dead cycles.":  "Unknown issue.\n",
"! Paratext stylesheet":                 "Try turning off the PrintDraft-mods stylesheet\n",
"! File ended while scanning use of \iotableleader.": "Problem with Formatting Intro Outline\n" +\
                                         "Try disabling option 'Right-Align \ior with tabbed leaders' on the Body tab\n",
"! Emergency stop.":                     "Probably a TeX macro problem - contact support, or post a bug report\n",
"! Not a letter.":                       "Possible fault in the hyphenation file\n" +\
                                         "Try turning off Hyphenate option located on the Body tab\n",
"! Font":                                "Font related issue - details unknown\n(Report this rare error please)\n",
"! Too many }'s":                        "Serious TeX macro issue - contact support, or post a bug report\n",
"! This can't happen (page)":            "Serious TeX macro issue - contact support, or post a bug report\n",
"! I can't find file `paratext2.tex'.":  "Possibly a faulty installation.\n",
"! I can't find file `ptx-tracing.tex'.":"Possibly a faulty installation.\n",
"Runaway argument?":                     "Unknown issue. Maybe related to Right-aligned tabbed leaders\n" +\
                                         "Try turning off PrintDraftChanges.txt and both Stylesheets\n",
"Unknown":                               "Sorry! No diagnostic help is available for this error.\n" +\
                                         "Try turning off all Advanced settings & disable Changes and Stylesheets\n",
}
# \def\LineSpacingFactor{{{paragraph/linespacingfactor}}}
# \def\VerticalSpaceFactor{{1.0}}
# \baselineskip={paragraph/linespacing}pt {paragraph/varlinespacing} {paragraph/linemax} {paragraph/linemin}
# \XeTeXinterwordspaceshaping = {document/spacecntxtlztn}
# %\extrafont  %% This will be replaced by code for the fallback fonts to be used for special/missing characters

def base(fpath):
    return os.path.basename(fpath)[:-4]

# https://sites.google.com/a/lci-india.org/typesetting/home/illustrations/where-to-find-illustrations
# We could build the credit text too if we wanted to (and perhaps a list of pg numbers on which the pictures were found)
def codeLower(fpath):
    cl = re.findall(r"(?i)_?((?=cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib)..\d{5})[abc]?$", base(fpath))
    if cl:
        return cl[0].lower()
    else:
        return ""

def newBase(fpath):
    clwr = codeLower(fpath)
    if len(clwr):
        return clwr
    else:
        return re.sub('[()&+,. ]', '_', base(fpath).lower())

_diglot = {
"diglot/colorfonts" :       "document/ifcolorfonts",
"diglot/ifrtl" :            "document/ifrtl",
"diglot/fontfactor" :       "paper/fontfactor",
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
}

class RunJob:
    def __init__(self, printer, scriptsdir):
        self.scriptsdir = scriptsdir
        self.printer = printer
        self.tempFiles = []
        self.tmpdir = "."
        self.maxRuns = 1
        self.changes = None

    def doit(self, args):
        info = TexModel(self.printer, args.paratext, self.printer.ptsettings, self.printer.prjid)
        self.tempFiles = []
        self.prjid = info.dict["project/id"]
        self.prjdir = os.path.join(args.paratext, self.prjid)
        if self.prjid is None or not len(self.prjid):     # can't print no project
            return
        self.tempFiles += info.generateNestedStyles()
        invPW = self.printer.get("t_invisiblePassword")
        if invPW == None or invPW == "" or self.printer.configName() == "": # This config is unlocked
            # So it it safe/allowed to save the current config
            self.printer.writeConfig()
        # else:
            # print("Current Config is Locked, so changes have NOT been saved")
        self.tmpdir = os.path.join(self.prjdir, 'PrintDraft') if info.asBool("project/useprintdraftfolder") else args.directory
        os.makedirs(self.tmpdir, exist_ok=True)
        jobs = self.printer.getBooks()
        info["diglot/fzysettings"] = ""

        self.books = []
        if self.printer.get("cb_onlyRunOnce"):
            self.maxRuns = 1
        else:
            self.maxRuns = 5
        self.changes = None
        if info.asBool("document/ifinclfigs") and not info.asBool("document/ifdiglot"):
            self.gatherIllustrations(jobs)

        if info.asBool("project/combinebooks"):
            joblist = [jobs]
        else:
            joblist = [[j] for j in jobs]

        isDiglot = self.printer.get("c_diglot")
        if isDiglot:
            digfraction = info.dict["document/diglotprifraction"]
            digprjid = info.dict["document/diglotsecprj"]
            digcfg = info.dict["document/diglotsecconfig"]
            digprjdir = os.path.join(args.paratext, digprjid)
            if digprjid is None or not len(digprjid):     # can't print no project
                return
            digptsettings = ParatextSettings(args.paratext, digprjid)
            digprinter = ViewModel(args.paratext, self.printer.working_dir)
            digprinter.setPrjid(digprjid)
            if digcfg is not None and digcfg != "":
                digprinter.setConfigId(digcfg)
            diginfo = TexModel(digprinter, args.paratext, digptsettings, digprjid)
            texfiles = sum((self.digdojob(j, info, diginfo, digprjid, digprjdir) for j in joblist), [])
        else: # Normal (non-diglot)
            texfiles = sum((self.dojob(j, info) for j in joblist), [])

        # Work out what the resulting PDF was called
        if len(jobs) > 1 and info.asBool("project/combinebooks"):
            pdfname = os.path.join(self.tmpdir, "ptxprint-{}_{}{}.pdf".format(jobs[0], jobs[-1], self.prjid))
        else:
            pdfname = os.path.join(self.tmpdir, "ptxprint-{}{}.pdf".format(jobs[0], self.prjid))
        # Check the return code to see if generating the PDF was successful before opening the PDF
        if self.res == 0:
            if self.printer.isDisplay and os.path.exists(pdfname):
                if sys.platform == "win32":
                    os.startfile(pdfname)
                elif sys.platform == "linux":
                    subprocess.call(('xdg-open', pdfname))
                # Only delete the temp files if the PDF was created AND the user did NOT select to keep them
            if not info.asBool("project/keeptempfiles"):
                self.removeTempFiles(texfiles)
        elif not args.print: # We don't want pop-up messages if running in command-line mode
            finalLogLines = self.parseLogLines()
            self.printer.doError("Failed to create: "+re.sub(r".+[\\/](.+\.pdf)",r"\1",pdfname),
                    secondary="".join(finalLogLines[-20:]), title="PTXprint [{}] - Error!".format(VersionStr))

    def parselog(self, fname, rerunp=False, lines=20):
        loglines = []
        rerunres = False
        with open(fname, "r", encoding="utf-8", errors="ignore") as logfile:
            try:
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
        # it did NOT finish successfully, so help them troubleshoot what went wrong:
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
            finalLogLines.append("\nReferences to check{}: {}".format(book, ", ".join(refs)))

        texmrkrs = [r"\fi", "\if", "\\par", "\\relax"]
        allmrkrs = re.findall(r"(\\[a-z0-9]{0,5})[ *\r\n.]", "".join(finalLogLines[-8:]))
        mrkrs = [x for x in allmrkrs if x not in texmrkrs]
        if len(mrkrs):
            finalLogLines.append("\nMarkers to check: {}".format(", ".join(mrkrs)))

        files = re.findall(r'(?i)([^\\/\n."= ]*?\.(?=jpg|tif|png|pdf)...)', "".join(finalLogLines))
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
        return self.sharedjob(jobs, info, logbuffer=logbuffer)

    def digdojob(self, jobs, info, diginfo, digprjid, digprjdir, logbuffer=None):
        texfiles = []
        donebooks = []
        digdonebooks = []
        # need to set either -v -c -p depending on what kind of merge is needed
        alnmnt = info.dict["document/diglotalignment"]
        if alnmnt.startswith("Not"):
            alignParam = "None"
        elif alnmnt.endswith("Chapters"):
            alignParam = "-c"
        elif alnmnt.endswith("Paragraphs"):
            alignParam = "-p"
        elif alnmnt.endswith("Verses"):
            alignParam = "-v"
        else:
            alignParam = ""
        if True: # alnmnt.startswith("No"):
            _digSecSettings = ["paper/pagesize", "paper/height", "paper/width", "paper/margins",
                               "paper/sidemarginfactor", "paper/topmarginfactor", "paper/bottommarginfactor",
                               "paper/fontfactor", "header/headerposition", "header/footerposition", "header/ruleposition",
                               "document/ch1pagebreak", "document/supressbookintro", "document/supressintrooutline", 
                               "document/supressparallels", "document/elipsizemptyvs", "notes/iffootnoterule", 
                               "notes/ifblendfnxr", "notes/includefootnotes", "notes/includexrefs", 
                               "notes/fnparagraphednotes", "notes/xrparagraphednotes", "document/filterglossary", 
                               "document/chapfrom", "document/chapto", "document/ifcolorfonts"]
            diginfo["project/bookids"] = jobs
            diginfo["project/books"] = digdonebooks
            diginfo["document/ifaligndiglot"] = "%"
            diginfo["footer/ftrcenter"] = "-empty-"
            diginfo["footer/ifftrtitlepagenum"] = "%"
            diginfo["fancy/pageborder"] = "%"
            diginfo["document/clsinglecol"] = False
            diginfo["snippets/alignediglot"] = False
            print("_digSecSettings = ", _digSecSettings)
            print("----------Passing info settings to diginfo-----------")
            for k in _digSecSettings:
                print("{} = {}".format(k, info[k]))
                diginfo[k]=info[k]
            print("-----------------------------------------------------")
        for b in jobs:
            out = info.convertBook(b, self.tmpdir, self.prjdir)
            digout = diginfo.convertBook(b, self.tmpdir, digprjdir)
            donebooks.append(out)
            digdonebooks.append(digout)
            
            if alignParam != "None":
                # Now run the Perl script to merge the secondary text (right) into the primary text (left) 
                left = os.path.join(self.tmpdir, out)
                right = os.path.join(self.tmpdir, digout)
                tmpFile = os.path.join(self.tmpdir, "primaryText.tmp")
                logFile = os.path.join(self.tmpdir, "ptxprint-merge.log")
                copyfile(left, tmpFile)

                # Usage: diglotMerge.exe [-mode|options] LeftFile RightFile
                # Read LeftFile and RightFile, merging them according to the selected mode)
                 # Mode may be any ONE of :
                 # -l     :Left master: splitting right page at each left text paragraph
                 # -r     :Right master: splitting left page at each right text paragraph
                 # -v     :matching verses (default)
                 # -c     :matching chapters
                 # -p     :matching paragraph breaks
                # Options are:
                 # -left file        : Log to file
                # -right 11:25-25:12   Only ouput specified range
                # -s      Split off section headings into a separate chunk (makes verses line up)
                # -C      If ?? is used, consider the chapter mark to be a heading
                # -o file : Output to file
                
                if sys.platform == "win32":
                    cmd = [os.path.join(self.scriptsdir, "diglotMerge.exe")]
                elif sys.platform == "linux":  # UNTESTED code
                    p = os.path.join(self.scriptsdir, "diglot_merge.pl")
                    cmd = ['perl', p]  # need to work out where the .pl file will live)
                cmdparms = ['-o', left, alignParam, '-L', 'ptxprint-merge.log', '-s', '-l', tmpFile, right] 
                r = checkoutput(cmd + cmdparms)
                for f in [left, right, tmpFile, logFile]:
                    texfiles += [os.path.join(self.tmpdir, f)]

                # if r != 0:  # Not sure how to check/interpret the return codes from diglotMerge.exe
                    # print("Failed to merge the Primary and Secondary files! Result code: {}".format(r))
                # else:
                    # print("SUCCESSFULLY merged the Primary and Secondary files!")
                    # os.remove(tmpFile) # maybe this should only be done at the end when others are also deleted
        info["project/bookids"] = jobs
        info["project/books"] = donebooks
        self.books += digdonebooks

        if alnmnt.startswith("No"):
            # First create Secondary PDF
            diginfo["diglot/fzysettings"] = self.generateFzyDiglotSettings(jobs, info, None, primary=False)
            print("Sec:", diginfo["diglot/fzysettings"])
            texfiles += self.sharedjob(jobs, diginfo, prjid=digprjid, prjdir=digprjdir, fzy=True)
            # Now Primary (along with Secondary merged in with it)
            info["diglot/fzysettings"] = self.generateFzyDiglotSettings(jobs, info, digprjid, primary=True)
            print("Pri:", info["diglot/fzysettings"])
            texfiles += self.sharedjob(jobs, info)
        else:
            # Pass all the needed parameters for the snippet from diginfo to info
            for k,v in _diglot.items():
                info[k]=diginfo[v]
                # print(k, v, diginfo[v])
            texfiles += self.sharedjob(jobs, info, logbuffer=logbuffer)
        return texfiles

    def generateFzyDiglotSettings(self, jobs, info, secprjid, primary=True):
        switchSides = info.asBool("document/diglotswapside")
        pageWidth = int(re.split("[^0-9]",re.sub(r"^(.*?)\s*,.*$", r"\1", info.dict["paper/pagesize"]))[0]) or 148
        margin = int(info.dict["paper/margins"]) # self.get("s_margins")
        print("margin:", margin)
        # margin = 12
        middleGutter = int(info.dict["document/colgutterfactor"])/3 # self.get("s_colgutterfactor")
        bindingGutter = int(info.dict["paper/gutter"]) # self.get("s_pagegutter")
        print("bindingGutter:", bindingGutter)
        # bindingGutter = 0
        if switchSides: # Primary on RIGHT/OUTER
            priFraction = float(info.dict["document/diglotprifraction"]) # self.get("s_diglotPriFraction")
            priColWidth = (pageWidth  - middleGutter - bindingGutter - (2 * margin)) * priFraction # / 100
            secColWidth = pageWidth - priColWidth - middleGutter - bindingGutter - (2 * margin)
            # Calc Pri Settings (right side of page; or outer if mirrored)
            priSideMarginFactor = 1
            pribindingGutter = pageWidth - margin - priColWidth - margin
            # Calc Sec Settings (left side of page; or inner if mirrored)
            secSideMarginFactor = (priColWidth + margin + middleGutter) / margin
            secRightMargin = priColWidth + margin + middleGutter
            secbindingGutter = pageWidth - (2 * secRightMargin) - secColWidth 
        else: # Primary on LEFT/INNER
            priFraction = 1 - float(info.dict["document/diglotprifraction"]) # self.get("s_diglotPriFraction")
            priColWidth = (pageWidth  - middleGutter - bindingGutter - (2 * margin)) * priFraction # / 100
            secColWidth = pageWidth - priColWidth - middleGutter - bindingGutter - (2 * margin)
            # Calc Pri Settings (left side of page; or inner if mirrored)
            secSideMarginFactor = 1
            secbindingGutter = pageWidth - margin - priColWidth - margin
            # Calc Sec Settings (right side of page; or outer if mirrored)
            priSideMarginFactor = (priColWidth + margin + middleGutter) / margin
            priRightMargin = priColWidth + margin + middleGutter
            pribindingGutter = pageWidth - (2 * priRightMargin) - secColWidth 
        hdr = ""
        if not primary:
            if info.asBool("document/diglotnormalhdrs"):
                if switchSides: # Primary on RIGHT/OUTER
                    hdr = r"""
\def\RHoddleft{\rangeref}
\def\RHoddcenter{\empty}
\def\RHoddright{\empty}
\def\RHevenleft{\empty}
\def\RHevencenter{\empty}
\def\RHevenright{\rangeref}"""
                else: # Primary on LEFT/INNER
                    hdr = r"""
\def\RHoddright{\rangeref}
\def\RHoddcenter{\empty}
\def\RHoddleft{\empty}
\def\RHevenright{\empty}
\def\RHevencenter{\empty}
\def\RHevenleft{\rangeref}"""
                
            digFzyCfg = "%% SECONDARY PDF settings"+ \
                        "\n\MarginUnit={}mm".format(margin)+ \
                        "\n\BindingGuttertrue"+ \
                        "\n\BindingGutter={:.2f}mm".format(secbindingGutter)+ \
                        "\n\def\SideMarginFactor{{{:.2f}}}".format(secSideMarginFactor)+ \
                        "\n\BodyColumns=1" + hdr
                        # We also need to be able to overide the page layout values from the PRIMARY project
                        # (even when creating the Secondary PDF so that the dimensions match).
        else:
            if len(jobs) > 1:
                secfname = os.path.join(self.tmpdir, "ptxprint-{}_{}{}.pdf".format(jobs[0], jobs[-1], secprjid)).replace("\\","/")
            else:
                secfname = os.path.join(self.tmpdir, "ptxprint-{}{}.pdf".format(jobs[0], secprjid)).replace("\\","/")
            if info.asBool("document/diglotnormalhdrs"):
                if switchSides: # Primary on RIGHT/OUTER
                    hdr = r"""
\def\RHoddleft{\pagenumber}
\def\RHoddcenter{\empty}
\def\RHoddright{\rangeref}
\def\RHevenleft{\rangeref}
\def\RHevencenter{\empty}
\def\RHevenright{\pagenumber}"""
                else: # Primary on LEFT/INNER
                    hdr = r"""
\def\RHoddright{\pagenumber}
\def\RHoddcenter{\empty}
\def\RHoddleft{\rangeref}
\def\RHevenright{\rangeref}
\def\RHevencenter{\empty}
\def\RHevenleft{\pagenumber}"""
            digFzyCfg = "%% PRIMARY (+ SECONDARY) PDF settings"+ \
                        "\n\MarginUnit={}mm".format(margin)+ \
                        "\n\BindingGuttertrue"+ \
                        "\n\BindingGutter={:.2f}mm".format(pribindingGutter)+ \
                        "\n\def\SideMarginFactor{{{:.2f}}}".format(priSideMarginFactor)+ \
                        "\n\BodyColumns=1"+ \
                        "\n\def\MergePDF{" + secfname + "}" + hdr
        return digFzyCfg

    def sharedjob(self, jobs, info, prjid=None, prjdir=None, fzy=False, logbuffer=None):
        numruns = self.maxRuns
        if prjid is None:
            prjid = self.prjid
        if prjdir is None:
            prjdir = self.prjdir
        if len(jobs) > 1:
            outfname = "ptxprint-{}_{}{}.tex".format(jobs[0], jobs[-1], prjid)
        else:
            outfname = "ptxprint-{}{}.tex".format(jobs[0], prjid)
        if not fzy:
            info.update()
        with open(os.path.join(self.tmpdir, outfname), "w", encoding="utf-8") as texf:
            # print({k:v for k,v in info.dict.items() if k.startswith("diglot")})
            texf.write(info.asTex(filedir=self.tmpdir, jobname=outfname.replace(".tex", "")))
        os.putenv("hyph_size", "32749")     # always run with maximum hyphenated words size (xetex is still tiny ~200MB resident)
        os.putenv("stack_size", "32768")    # extra input stack space (up from 5000)
        ptxmacrospath = os.path.abspath(os.path.join(self.scriptsdir, "..", "..", "src"))
        print("ptxmacrospath:", ptxmacrospath)
        if not os.path.exists(ptxmacrospath):
            for b in (getattr(sys, 'USER_BASE', '.'), sys.prefix):
                if b is None:
                    continue
                ptxmacrospath = os.path.abspath(os.path.join(b, 'ptx2pdf'))
                if os.path.exists(ptxmacrospath):
                    break
        # if info['project/useptmacros'] == "false":
        if True:
            envtexinputs = os.getenv("TEXINPUTS")
            texinputs = [envtexinputs] if envtexinputs is not None and len(envtexinputs) else []
            texinputs += [os.path.abspath(self.tmpdir), ptxmacrospath]
            os.putenv('TEXINPUTS', (";" if sys.platform=="win32" else ":").join(texinputs))
            print("TEXINPUTS=",os.getenv('TEXINPUTS'))
        elif sys.platform == "linux":
            if not os.getenv('TEXINPUTS'):
                mdirs = args.macros or "/usr/lib/Paratext8/xetex/share/texmf-dist/tex/ptx2pdf:/usr/lib/Paratext9/xetex/share/texmf-dist/tex/ptx2pdf"
                os.putenv('TEXINPUTS', ".:" + mdirs)
        os.putenv("MISCFONTS", ptxmacrospath)
        while numruns > 0:
            print("numruns=", numruns)
            if info["document/toc"] != "%":
                tocdata = readfile(os.path.join(self.tmpdir, outfname.replace(".tex", ".toc")))
            runner = call(["xetex", "--halt-on-error", outfname], cwd=self.tmpdir, logbuffer=logbuffer)
            if isinstance(runner, subprocess.Popen) and runner is not None:
                try:
                    runner.wait(args.timeout)
                except subprocess.TimeoutExpired:
                    print("Timed out!")
                self.res = runner.returncode
            else:
                self.res = runner
            print("cd {}; xetex {} -> {}".format(self.tmpdir, outfname, self.res))
            (self.loglines, rerun) = self.parselog(os.path.join(self.tmpdir, outfname.replace(".tex", ".log")), rerunp=True, lines=300)
            if self.res:
                break
            elif info["document/toc"] != "%" and not rerun:
                tocndata = readfile(os.path.join(self.tmpdir, outfname.replace(".tex", ".toc")))
                rerun = tocdata != tocndata
                if rerun:
                    print("Rerunning because the Table of Contents was updated")
                else:
                    break
            elif rerun:
                print("Rerunning because inline chapter numbers moved")
            else:
                break
            numruns -= 1
        print("Done")
        return [outfname]

    def gatherIllustrations(self, jobs):
        tmpPicpath = os.path.join(self.printer.working_dir, "tmpPics")
        folderList = ["tmpPics", "tmpPicLists"] 
        self.removeTmpFolders(self.printer.working_dir, folderList)
        if self.printer.get("c_useCustomFolder"):
            srchlist = [self.printer.customFigFolder]
        else:
            srchlist = []
        if not self.printer.get("c_exclusiveFiguresFolder"):
            if sys.platform == "win32":
                srchlist += [os.path.join(self.prjdir, "figures")]
                srchlist += [os.path.join(self.prjdir, "local", "figures")]
            elif sys.platform == "linux":
                chkpaths = []
                for d in ("local", "figures"):
                    chkpaths += [os.path.join(self.prjdir, x) for x in (d, d.title())]
                for p in chkpaths:
                    if os.path.exists(p):
                        srchlist += [p]
        extensions = []
        extdflt = ["jpg", "png", "pdf", "tif"]
        extuser = re.sub("(pdf|tif)", "pdf tif",self.printer.get("t_imageTypeOrder").lower())
        extuser = re.findall("([a-z]{3})",extuser)
        extensions = [x for x in extdflt if x in extuser]
        if not len(extensions):   # If the user hasn't defined any extensions 
            extensions = extdflt  # then we can assign defaults
        fullnamelist = []

        for bk in jobs:
            fname = self.printer.getBookFilename(bk, self.prjdir)
            if self.printer.get("c_usePicList") and bk not in TexModel._peripheralBooks: # Read the PicList to get a list of needed illustrations
                doti = fname.rfind(".")
                if doti > 0:
                    plfname = fname[:doti] + "-draft" + fname[doti:] + ".piclist"
                piclstfname = os.path.join(self.printer.configPath(makePath=False), "PicLists", plfname)
                if os.path.exists(piclstfname):
                    with universalopen(piclstfname, rewrite=True) as inf:
                        dat = inf.read()
                        # MAT 19.13 |CN01771C.jpg|col|tr||Bringing the children to Jesus|19:13
                        fullnamelist += re.findall(r"(?i)\|(.+?\.(?=jpg|tif|png|pdf)...)\|", dat)
            else:
                infname = os.path.join(self.prjdir, fname)
                with universalopen(infname) as inf:
                    dat = inf.read()
                    inf.close() # Look for USFM2 and USFM3 type inline \fig ... \fig* illustrations
                    fullnamelist += re.findall(r"(?i)\\fig .*?\|(.+?(?!\d{5}[a-c]?).+?\.(?=jpg|tif|png|pdf)...)\|.+?\\fig\*", dat)
                    fullnamelist += re.findall(r'(?i)\\fig .*?src="(.+?\.(?=jpg|tif|png|pdf)...)" .+?\\fig\*', dat) 
        newBaseList = [newBase(f) for f in fullnamelist]

        os.makedirs(tmpPicpath, exist_ok=True)
        for srchdir in srchlist:
            if srchdir != None and os.path.exists(srchdir):
                if self.printer.get("c_exclusiveFiguresFolder"):
                    for file in os.listdir(srchdir):
                        origExt = file[-4:].lower()
                        if origExt[1:] in extensions:
                            filepath = os.path.join(srchdir, file)
                            if newBase(filepath) in newBaseList:
                                self.carefulCopy(filepath, newBase(filepath)+origExt.lower())
                else: # Search all subfolders as well
                    for subdir, dirs, files in os.walk(srchdir):
                        if subdir != "tmpPics": # Avoid recursively scanning the folder we are copying to!
                            for file in files:
                                origExt = file[-4:].lower()
                                if origExt[1:] in extensions:
                                    filepath = subdir + os.sep + file
                                    if newBase(filepath) in newBaseList:
                                        # print(filepath, "-->", newBase(filepath)+origExt.lower())
                                        self.carefulCopy(filepath, newBase(filepath)+origExt.lower())

        missingPics = []
        missingPicList = []
        if self.printer.get("c_usePicList"): # Write out new tmpPicLists
            extOrder = self.printer.getExtOrder()
            for bk in jobs:
                fname = self.printer.getBookFilename(bk, self.prjdir)
                if self.printer.get("c_usePicList"): # Read the PicList to get a list of needed illustrations
                    doti = fname.rfind(".")
                    if doti > 0:
                        plfname = fname[:doti] + "-draft" + fname[doti:] + ".piclist"
                    # Now write out the new PicList to a temp folder
                    piclstfname = os.path.join(self.printer.configPath(cfgname=self.printer.configId, makePath=False), "PicLists", plfname)
                    if os.path.exists(piclstfname):
                        with universalopen(piclstfname) as inf:
                            dat = inf.read()
                            dat = re.sub(r"(?m)%.+?\r?\n", "", dat) # Throw out all comments
                            for f in fullnamelist:
                                ext = f[-4:].lower()
                                if ext[1:] == "tif":
                                    ext = ".pdf"
                                tmpPicfname = newBase(f)+ext
                                if os.path.exists(os.path.join(tmpPicpath, tmpPicfname)):
                                    dat = re.sub(re.escape(f), tmpPicfname, dat)  # might need to wrap the f in |filename.tif|
                                else:
                                    found = False
                                    for ext in extOrder:
                                        tmpPicfname = newBase(f)+"."+ext
                                        if os.path.exists(os.path.join(tmpPicpath, tmpPicfname)):
                                            dat = re.sub(re.escape(f), tmpPicfname, dat)
                                            found = True
                                            break
                                    if not found:
                                        missingPics.append(f[:-4])
                                        if self.printer.get("c_skipmissingimages"):
                                            dat = re.sub(r"(?im)(^.*{})".format(re.escape(f)), r"% \1", dat)

                            if self.printer.get("c_fighiderefs"): # del refs (ch:vs-vs) from figure caption
                                dat = re.sub(r"\|(\d+[:.]\d+([-,\u2013\u2014]\d+)?)\r?\n".format(re.escape(f)), "|\n", dat)
                            if not self.printer.get("c_doublecolumn"): # Single Column layout so change all tl+tr > t and bl+br > b
                                dat = re.sub(r"\|([tb])[lr]\|", r"|\1|", dat)

                            tmpiclstpath = os.path.join(self.printer.working_dir, "tmpPicLists")
                            tmpiclstfname = os.path.join(tmpiclstpath, plfname)
                            os.makedirs(tmpiclstpath, exist_ok=True)
                            dat = "% Temporary PicList generated by PTXprint - DO NOT EDIT\n"+dat
                            with open(tmpiclstfname, "w", encoding="utf-8") as outf:
                                outf.write(dat)
            if len(missingPics):
                missingPicList += ["{}".format(", ".join(list(set(missingPics))))]
        if len(missingPicList):
            self.printer.set("l_missingPictureString", "Missing Pictures:\n"+"{}".format("\n".join(missingPicList)))
        else:
            self.printer.set("l_missingPictureString", "(No Missing Pictures)")
        
    def carefulCopy(self, srcpath, tgtfile):
        tmpPicPath = os.path.join(self.printer.working_dir, "tmpPics")
        tgtpath = os.path.join(tmpPicPath, tgtfile)
        if srcpath[-4:].lower() == ".tif":
            tempPDFname = os.path.join(tmpPicPath, "tempPDF.pdf")
            tgtpath = tgtpath[:-4]+".pdf"
            with open(tempPDFname,"wb") as f:
                try:
                    f.write(img2pdf.convert(srcpath))
                    srcpath = tempPDFname
                except:
                    return
        if not os.path.exists(tgtpath):
            copyfile(srcpath, tgtpath)
        else:
            if self.printer.get("c_useLowResPics"): # we want to use the smallest available file
                if os.path.getsize(srcpath) < os.path.getsize(tgtpath):
                    copyfile(srcpath, tgtpath)
            else:                              # we want to use the largest file available
                if os.path.getsize(srcpath) > os.path.getsize(tgtpath):
                    copyfile(srcpath, tgtpath)
        try:
            os.remove(tempPDFname)
        except:
            pass

    def removeTempFiles(self, texfiles):
        notDeleted = []
        n = os.path.join(self.tmpdir, "NestedStyles.sty")
        if os.path.exists(n):
            try:
                os.remove(n)
            except:
                notDeleted += [n]
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
            self.printer.doError("Warning: Could not delete\ntemporary file(s) or folder(s):",
                    secondary="\n".join(set(notDeleted)))

    def removeTmpFolders(self, base, delFolders):
        notDeleted = []
        for p in delFolders:
            path2del = os.path.join(base, p)
            if os.path.exists(path2del):
                try:
                    rmtree(path2del)
                except OSError:
                    notDeleted += [path2del]
        return notDeleted
