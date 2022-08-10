
import configparser, os, re, regex, random, collections
from ptxprint.texmodel import ModelMap, TexModel, Borders
from ptxprint.ptsettings import ParatextSettings
from ptxprint.font import TTFont, cachepath, cacheremovepath, FontRef, getfontcache, writefontsconf
from ptxprint.utils import _, refKey, universalopen, print_traceback, local2globalhdr, chgsHeader, \
                            global2localhdr, asfloat, allbooks, books, bookcodes, chaps, f2s, pycodedir, Path, \
                            get_gitver, getcaller
from ptxprint.usfmutils import Sheets, UsfmCollection, Usfm, Module
from ptxprint.piclist import PicInfo, PicChecks
from ptxprint.styleditor import StyleEditor
from ptxprint.xrefs import generateStrongsIndex
from ptxprint.pdfrw.pdfreader import PdfReader
from ptxprint.reference import RefList, RefRange, Reference
import ptxprint.scriptsnippets as scriptsnippets
import ptxprint.pdfrw.errors
import os, sys
from configparser import NoSectionError, NoOptionError, _UNSET
from tempfile import NamedTemporaryFile
from zipfile import ZipFile, ZIP_DEFLATED, ZipInfo
from io import StringIO
from shutil import rmtree
import datetime, time
import json, logging
from shutil import copyfile, copytree, move
from difflib import Differ

logger = logging.getLogger(__name__)

VersionStr = "2.2.10"
GitVersionStr = "2.2.10"
ConfigVersion = "2.09"

pdfre = re.compile(r".+[\\/](.+\.pdf)")

gitdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.git')
if os.path.exists(gitdir):
    GitVersionStr = get_gitver(gitdir=gitdir, version=VersionStr)

FontModelMap = {
    "fontregular": ("bl_fontR", None),
    "fontbold":    ("bl_fontB", None),
    "fontitalic":  ("bl_fontI", None),
    "fontbolditalic": ("bl_fontBI", None),
    "fontextraregular": ("bl_fontExtraR", None)
}

posparms = ["alt", "src", "size", "pgpos", "copy", "caption", "ref", "x-xetex", "mirror", "scale"]
pos3parms = ["src", "size", "pgpos", "ref", "copy", "alt", "x-xetex", "mirror", "scale"]

def doError(txt, secondary=None, **kw):
    print(txt)
    logger.error(txt)
    if secondary is not None:
        print(secondary)
        logger.error(txt)

class ViewModel:
    _attributes = {
        # modelname: (attribute, isMultiple, label)
        "project/frontincludes":    ("FrontPDFs", True, "lb_inclFrontMatter"),
        "project/backincludes":     ("BackPDFs", True, "lb_inclBackMatter"),
        "project/selectscript":     ("customScript", False, "btn_selectScript"),
        "project/selectxrfile":     ("customXRfile", False, "btn_customXrFile"),
        "project/modulefile":       ("moduleFile", False, "lb_bibleModule"),
        "paper/watermarkpdf":       ("watermarks", False, "lb_applyWatermark"),
        "fancy/pageborderpdf":      ("pageborder", False, "lb_inclPageBorder"),
        "fancy/sectionheaderpdf":   ("sectionheader", False, "lb_inclSectionHeader"),
        "fancy/endofbookpdf":       ("endofbook", False, "lb_inclEndOfBook"),
        "fancy/versedecoratorpdf":  ("versedecorator", False, "lb_inclVerseDecorator"),
        "document/diffPDF":         ("diffPDF", False, "lb_diffPDF"),
        "document/customfigfolder": ("customFigFolder", False, "lb_selectFigureFolder"),
        "document/customoutputfolder": ("customOutputFolder", False, None)
    }
    _settingmappings = {
        "notes/xrcallers": "crossrefs",
        "notes/fncallers": "footnotes"
    }
    _activekeys = {
        "document/diglotsecprj": "updateDiglotConfigList"
    }

    def __init__(self, settings_dir, workingdir, userconfig, scriptsdir, args=None):
        self.settings_dir = settings_dir        # ~/Paratext8Projects
        self.working_dir = workingdir           # . or ~/Paratext8Projects/<prj>/PrintDraft
        self.userconfig = userconfig
        self.scriptsdir = scriptsdir
        self.args = args
        self.ptsettings = None
        self.FrontPDFs = None
        self.BackPDFs = None
        self.diffPDF = None
        self.customScript = None
        self.customXRfile = None
        self.moduleFile = None
        self.DBLfile = None
        self.watermarks = None
        self.pageborder = None
        self.sectionheader = None
        self.endofbook = None
        self.versedecorator = None
        self.customFigFolder = None
        self.customOutputFolder = None
        self.prjid = None
        self.configId = None
        self.diglotView = None
        self.isDiglot = False
        self.isDisplay = False
        self.tempFiles = []
        self.usfms = None
        self.picinfos = None
        self.picChecksView = PicChecks(self)
        self.loadingConfig = False
        self.styleEditor = StyleEditor(self)
        self.triggervcs = False
        self.copyrightInfo = {}
        self.pubvars = {}
        self.strongsvars = {}
        self.bookrefs = None
        self.font2baselineRatio = 1.
        self.docreatediff = False

        # private to this implementation
        self.dict = {}

    def setup_ini(self):
        self.setDate()

    def setDate(self):
        t = datetime.datetime.now()
        zd = datetime.timedelta(seconds=-(time.altzone if time.daylight else time.timezone))
        tzhrs = zd.days * 24 + (zd.seconds // 3600)
        tzmins = (zd.seconds % 3600) // 60
        
        if tzhrs == 0:
            tzstr = "Z"
        else:
            tzstr = "{0:+03}'{1:02}'".format(tzhrs, tzmins)
        self.set("_pdfdate", t.strftime("%Y%m%d%H%M%S")+tzstr)
        self.set("_date", t.strftime("%Y-%m-%d %H:%M:%S ")+tzstr)
        self.set("_xmpdate", t.strftime("%Y-%m-%dT%H:%M:%S")+tzstr.replace("'", ":").rstrip(":"))

    def doError(self, txt, secondary=None, **kw):
        print(txt)
        if secondary is not None:
            print(secondary)

    def doStatus(self, txt=""):
        if txt:
            print("Status: ", txt)

    def waitThread(self, thread):
        thread.wait()

    def setPrintBtnStatus(self, idnty, txt=""):
        self.doStatus(txt)
        
    def msgQuestion(self, q1, q2, default=False):
        print("Answering \"no\" to: " + q1)
        print(q2)
        return default

    def resetToInitValues(self):
        if self.ptsettings is not None and self.ptsettings.dir == "right":
            self.set("fcb_textDirection", "rtl")

    def parse_fontname(self, font):
        m = re.match(r"^(.*?)(\d+(?:\.\d+?)?)$", font)
        if m:
            return [m.group(1), int(m.group(2))]
        else:
            return [font, 0]

    def get(self, wid, default=None, sub=0, asstr=False, skipmissing=False):
        return self.dict.get(wid, default)

    def set(self, wid, value, skipmissing=False):
        if wid.startswith("s_"):
            self.dict[wid] = f2s(float(value))
        else:
            self.dict[wid] = value

    def getvar(self, k, dest=None):
        if dest is None:
            return self.pubvars.get(k, "")
        elif dest == "strongs":
            return self.strongsvars.get(k, "")

    def setvar(self, k, v, dest=None):
        if dest is None:
            self.pubvars[k] = v
        elif dest == "strongs":
            self.strongsvars[k] = v

    def allvars(self, dest=None):
        if dest is None:
            return self.pubvars.keys()
        elif dest == "strongs":
            return self.strongsvars.keys()

    def clearvars(self):
        self.pubvars = {}

    def baseTeXPDFnames(self, bks=None, diff=False):
        if bks is None:
            bks = self.getBooks(files=True)
        cfgname = self.configName()
        if self.working_dir == None:
            self.working_dir = os.path.join(self.settings_dir, self.prjid, "local", "ptxprint", cfgname)
        if cfgname is None:
            cfgname = ""
        else:
            cfgname = "-" + cfgname
        if len(bks) > 1:
            fname = "ptxprint{}-{}_{}{}".format(cfgname, bks[0], bks[-1], self.prjid)
        elif "." in bks[0]:
            fname = "ptxprint{}-{}{}".format(cfgname, os.path.splitext(os.path.basename(bks[0]))[0], self.prjid)
        else:
            fname = "ptxprint{}-{}{}".format(cfgname, bks[0], self.prjid)
            
        if diff:
            return [fname, fname+"_diff"]
        else:
            return [fname]
        
    def _bookrefsBooks(self, bl, local):
        res = RefList()
        if not local:
            self.bookrefs = bl
        for r in bl:
            if not len(res) or r.first.book != res[-1]:
                res.append(r.first.book)
        return res

    def getBooks(self, scope=None, files=False, local=False):
        if scope is None:
            scope = self.get("r_book")
        if scope == "module":
            if self.moduleFile is None:
                return []
            res = Path(self.moduleFile).as_posix()
            return [res] if files and res else []
        elif scope != "single" and not local and self.bookrefs is not None:
            return self._bookrefsBooks(self.bookrefs, True)
        bl = RefList.fromStr(self.get("ecb_booklist", ""))
        if scope == "single" or not len(bl):
            bk = self.get("ecb_book")
            if bk:
                bname = self.getBookFilename(bk, self.prjid)
                if bname is not None and os.path.exists(os.path.join(self.settings_dir, self.prjid, bname)):
                    fromchap = round(float(self.get("t_chapfrom") or "0"))
                    tochap = round(float(self.get("t_chapto") or "200"))
                    res = RefList((RefRange(Reference(bk, fromchap, 0), Reference(bk, tochap, 200)), ))
                    return self._bookrefsBooks(res, local)
            return []
        elif scope == "multiple":
            res = RefList()
            self.bookrefs = RefList()
            for b in bl:
                bname = self.getBookFilename(b.first.book, self.prjid)
                if os.path.exists(os.path.join(self.settings_dir, self.prjid, bname)):
                    if b.first.book == "FRT":
                        self.switchFRTsettings()
                    else:
                        res.append(b)
            res.simplify()
            return self._bookrefsBooks(res, local)
        else:
            # return self.booklist
            return []
            
    def switchFRTsettings(self):
        frtpath = self.configFRT()
        if not os.path.exists(frtpath) or os.path.getsize(frtpath) == 0:
            self.doError(_("FRT must not be included in the list of books"), \
                secondary = _("The 'Front Matter' option has now been enabled for you " + \
                              "on the Peripherals page and the contents of Paratext's " + \
                              "FRT book has been copied to the PTXprint settings " + \
                              "location for this publication. It can be edited if " + \
                              "needed on the View+Edit page."))
            self.set("c_frontmatter", self.generateFrontMatter(frtype="paratext"))

    def getAllBooks(self):
        ''' Returns a dict of all books in the project bkid: bookfile_path '''
        if self.prjid is None:
            return {}
        prjdir = os.path.join(self.settings_dir, self.prjid)
        res = {}
        for bk in allbooks:
            f = self.getBookFilename(bk)
            fp = os.path.join(prjdir, f)
            if os.path.exists(fp):
                res[bk] = fp
        return res

    def _getPtSettings(self, prjid=None):
        if self.ptsettings is None and self.prjid is not None:
            self.ptsettings = ParatextSettings(self.settings_dir, self.prjid)
        if prjid is None:
            prjid = self.prjid
        if prjid != self.prjid:
            ptsettings = ParatextSettings(self.settings_dir, prjid)
        else:
            ptsettings = self.ptsettings
        return ptsettings

    def getBookFilename(self, bk, prjid=None):
        if bk is None or any(x in "./\\" for x in bk):
            return None
        ptsettings = self._getPtSettings(prjid)
        if ptsettings is None:
            return None
        return ptsettings.getBookFilename(bk)

    def getScriptSnippet(self):
        script = self.get("fcb_script")
        gclass = getattr(scriptsnippets, script.lower(), None)
        if gclass is None:
            gclass = getattr(scriptsnippets, 'ScriptSnippet')
        return gclass

    def setFont(self, btn, name, style):
        self.dict[btn+"/name"] = name
        self.dict[btn+"/style"] = style

    def onFontChanged(self, fbtn):
        font_info = self.get("bl_fontR")
        if font_info is None:
            return
        f = font_info.getTtfont()
        silns = "{urn://www.sil.org/ldml/0.1}"
        if not len(font_info.feats):
            d = self.ptsettings.find_ldml('.//special/{1}external-resources/{1}font[@name="{0}"]'.format(f.family, silns))
            if d is not None:
                featstring = d.get('features', '')
                font_info.updateFeats(featstring)
        for s in ('Bold', 'Italic', 'Bold Italic'):
            sid = "".join(x[0] for x in s.split())
            esid = s.lower().replace(" ", "")
            w = "bl_font"+sid
            nf = font_info.fromStyle(bold="Bold" in s, italic="Italic" in s)
            # print(f"onFontChanged {w} {nf}")
            if nf is not None:
                self.set(w, nf)

    def getFont(self, style="regular"):
        ctl = FontModelMap.get("font"+style, None)
        if ctl is None:
            return None
        return self.get(ctl[0])

    def updateFont2BaselineRatio(self):
        self.font2baselineRatio = float(self.get("s_fontsize")) / float(self.get("s_linespacing"))
    
    def onNumTabsChanged(self, *a):
        if self.loadingConfig:
            return False
        (marginmms, topmarginmms, bottommarginmms, headerpos, footerpos, rulerpos, headerlabel, footerlabel) = self.getMargins()
        self.set("l_margin2header1", "{}mm".format(f2s(headerlabel, 1)))
        return True

    def getMargins(self):
        def asmm(v): return v * 25.4 / 72.27
        hfont = self.styleEditor.getval("h", "FontName")
        if hfont is None:
            hfont = self.get("bl_fontR")
            if hfont is None:
                return (0, 0, 0, 0, 0, 0, 0, 0)
        hfont = hfont.getTtfont()
        #fontheight = 1. + float(font.descent) / font.upem
        hfontheight = float(hfont.ascent) / hfont.upem
        fontsizemms = asmm(float(self.get("s_fontsize")))
        linespacemms = asmm(float(self.get("s_linespacing")))
        hfontsizemms = asfloat(self.styleEditor.getval("h", "FontSize"), 1.) * fontsizemms
        marginmms = float(self.get("s_margins"))
        # in the macros, topmargin is set to topmargin - baselineskip + 12*FontSizeUnit
        # Reverse that here, so that what appears on the page is what they ask for.
        topmarginmms = float(self.get("s_topmargin")) + linespacemms - fontsizemms
        bottommarginmms = float(self.get("s_bottommargin"))
        # specified topmargin subtract 0.7 * hfontsize which the macros add in
        headerposmms = float(self.get("s_topmargin")) - asmm(float(self.get("s_headerposition"))) - 0.7 * hfontsizemms
        footerposmms = float(self.get("s_footerposition"))
        # report top of TeX headerbox then add that box back on and remove the 'true' height of the font
        headerlabel = headerposmms - (hfontheight - 0.7) * hfontsizemms
        footerlabel = (bottommarginmms - footerposmms - hfontheight * hfontsizemms) * 72.27 / 25.4
        # simply subtract ruler gap from header gap
        rulerposmms = asmm(float(self.get("s_headerposition")) - float(self.get("s_rhruleposition")))
        return (marginmms, topmarginmms, bottommarginmms, headerposmms, footerposmms, rulerposmms, headerlabel, footerlabel)

    def updateSavedConfigList(self):
        pass

    def updateDiglotConfigList(self):
        pass

    def updateBookList(self):
        pass

    def setPrjid(self, prjid, saveCurrConfig=False, loadConfig=True, readConfig=True):
        return self.updateProjectSettings(prjid, configName="Default", saveCurrConfig=saveCurrConfig, readConfig=loadConfig)

    def setConfigId(self, configid, saveCurrConfig=False, force=False, loadConfig=True):
        return self.updateProjectSettings(self.prjid, saveCurrConfig=saveCurrConfig, configName=configid, forceConfig=force, readConfig=loadConfig)

    def applyConfig(self, oldcfg, newcfg, action=None, moving=False, newprj=None, nobase=False):
        oldp = self.configPath(cfgname=oldcfg, makePath=False)
        newp = self.configPath(cfgname=newcfg, makePath=False, prjid=newprj)
        if action is None:
            if os.path.exists(newp):
                return False
            action = 0
        self.triggervcs = True
        os.makedirs(newp, exist_ok=True)
        jobs = {'ptxprint.cfg': (self._copyfile, self._mergecfg),
                'ptxprint.sty': (self._copyfile, self._mergesty),
                'ptxprint-mods.sty': (self._copyfile, self._mergesty),
                'ptxprint-premods.tex': (self._copyfile, self._mergetxt),
                'ptxprint-mods.tex': (self._copyfile, self._mergetxt),
                'changes.txt': (self._copyfile, self._mergetxt),
                'FRTlocal.sfm': (self._copyfile, self._mergetxt),
                'PicLists': (self._copydir, self._mergenothing),
                'AdjLists': (self._copydir, self._mergenothing)}
        if newprj is not None:
            del jobs['AdjLists']
        else:
            jobs["{}-{}.piclist".format(self.prjid, oldcfg)] = (self._copyfile, self._mergenothing, "{}-{}.piclist".format(self.prjid, newcfg))
        for f, a in jobs.items():
            srcp = os.path.join(oldp, f)
            destp = os.path.join(newp, a[2] if len(a) > 2 else f)
            mergep = os.path.join(newp, 'base', a[2] if len(a) > 2 else f)
            os.makedirs(os.path.dirname(mergep), exist_ok=True)
            if os.path.exists(srcp):
                a[action](srcp, destp, mergep, moving=moving, oldcfg=oldcfg, newcfg=newcfg, newprj=newprj, nobase=nobase)
        return True

    def _copyfile(self, srcp, destp, mergep, moving=False, nobase=False, **kw):
        if moving:
            move(srcp, destp)
            if not nobase:
                move(srcp, mergep)
        else:
            copyfile(srcp, destp)
            if not nobase:
                copyfile(srcp, mergep)

    def _copydir(self, srcp, destp, mergep, moving=False, oldcfg="", newcfg="", **kw):
        if moving:
            move(srcp, destp)
        else:
            os.makedirs(destp, exist_ok=True)
            for p in os.listdir(srcp):
                op = p.replace(oldcfg, newcfg)
                copyfile(os.path.join(srcp, p), os.path.join(destp, op))

    def _mergenothing(self, srcp, destp, mergep, **kw):
        pass

    def _mergecfg(self, srcp, destp, mergep, **kw):
        configs = []
        for a in (destp, srcp, mergep):
            config = configparser.ConfigParser()
            with open(a, encoding="utf-8", errors="ignore") as inf:
                config.read_file(inf)
            configs.append(config)
        (this, new, base) = configs
        for sect in this.sections():
            allopts = set(this.options(sect))
            if base.has_section(sect):
                allopts.update(base.options(sect))
            if new.has_section(sect):
                allopts.update(new.options(sect))
            for opt in allopts:
                if config.has_option(sect, opt) and (not base.has_option(sect, opt)
                        or config.get(sect, opt) != base.get(sect, opt)):
                    continue
                if new.has_option(sect, opt):
                    this.set(sect, opt, new.get(sect, opt))
        copyfile(srcp, mergep)
        with open(destp, "w", encoding="utf-8") as outf:
            this.write(outf)

    def _mergesty(self, srcp, destp, mergep, oldcfg="", newcfg="", newprj=None, **kw):
        srcse = StyleEditor(self)
        srcse.load(self.getStyleSheets(oldcfg))
        destse = StyleEditor(self)
        destse.load(self.getStyleSheets(newcfg, prjid=newprj))
        mergese = StyleEditor(self)
        mergese.load(self.getStyleSheets(newcfg, prjid=newprj, subdir="base"))
        destse.merge(mergese, srcse)
        with open(destp, "w", encoding="utf-8") as outfh:
            destse.output_diffile(outfh, inArchive=True)
        copyfile(srcp, mergep)

    def _mergetxt(self, srcp, destp, mergep, **kw):
        lines = []
        for a in (srcp, destp, mergep):
            with open(a, encoding="utf-8") as inf:
                lines.append(list(inf.readlines()))
        this = [x for x in Differ().compare(lines[2], lines[0]) if x[0] != "?"]
        other = [x for x in Differ().compare(lines[2], lines[1]) if x[0] != "?"]
        ti = 0
        oi = 0
        res = []
        while ti < len(this) and oi < len(other):
            if this[ti] == other[oi] and this[ti][0] in " +":  # both normal or insert the same
                res.append(this[ti][2:])
                ti += 1
                oi += 1
            elif this[ti][2:] == other[oi][2:] and (this[ti][0] == "-" or other[oi][0] == "-"):
                ti += 1
                oi += 1
            elif this[ti][0] == "+": # and other[oi][0] == " ": default clash = this wins
                res.append(this[ti][2:])
                ti += 1
            elif other[oi][0] == "+" and this[ti][0] == " ":
                res.append(other[oi][2:])
                oi += 1
        res.extend([x[2:] for x in this[ti:]])
        res.extend([x[2:] for x in other[oi:]])
        with open(destp, "w", encoding="utf-8") as outf:
            outf.write("".join(res))
        copyfile(srcp, mergep)

    def updateProjectSettings(self, prjid, saveCurrConfig=False, configName=None, forceConfig=False, readConfig=None):
        logger.debug(f"Changing project to {prjid or self.get('fcb_project')} from {self.prjid}, {configName=} from {getcaller(1)}")
        currprj = self.prjid
        if currprj is None or currprj != prjid:
            if currprj is not None and saveCurrConfig:
                self.writeConfig()
                self.updateSavedConfigList()
                self.set("t_savedConfig", "")
                self.set("t_configNotes", "")
                fdir = os.path.join(self.settings_dir, currprj, "shared", "fonts")
                if os.path.exists(fdir):
                    cacheremovepath(fdir)
            self.ptsettings = None
            self.prjid = self.get("fcb_project") if prjid is None else prjid
            self.configId = "Default"
            if self.prjid:
                self.ptsettings = ParatextSettings(self.settings_dir, self.prjid)
                self.updateBookList()
            if not self.prjid:
                return False
            fdir = os.path.join(self.settings_dir, self.prjid, 'shared', 'fonts')
            if os.path.exists(fdir):
                cachepath(fdir)
            if readConfig is not False:
                readConfig = True
        if readConfig is None:
            readConfig = False
        if readConfig or self.configId != configName:
            self.resetToInitValues()
            if currprj == self.prjid:
                if configName == "Default":
                    self.applyConfig(None, configName, moving=True)
                else:
                    self.applyConfig(self.configId, configName)
            self.working_dir = os.path.join(self.settings_dir, self.prjid, "local", "ptxprint", configName)
            oldVersion = self.readConfig(cfgname=configName)
            self.styleEditor.load(self.getStyleSheets(configName))
            self.updateStyles(oldVersion)
            if oldVersion >= 0 or forceConfig:
                self.configId = configName
            if readConfig:  # project changed
                self.usfms = None
                self.get_usfms()
            self.onNumTabsChanged()
            self.readCopyrights()
            self.picChecksView.init(basepath=self.configPath(cfgname=None), configid=self.configId)
            self.picinfos = None
            self.loadPics(mustLoad=False)
            return oldVersion >= 0
        else:
            return True

    def get_usfms(self):
        if self.usfms is None:
            self.usfms = UsfmCollection(self.getBookFilename, 
                            os.path.join(self.settings_dir, self.prjid),
                            Sheets(self.getStyleSheets()))
        return self.usfms

    def getDialogTitle(self):
        prjid = self.get("fcb_project")
        if prjid is None:
            return _("PTXprint {} - Bible Layout for Everyone!").format(VersionStr)
        else:
            bks = self.getBooks(files=True)
            if len(bks) == 2:
                bks = bks[0] + "," + bks[1]
            elif len(bks) <= 4:
                bks = ",".join(bks)
            elif len(bks) > 4:
                bks = bks[0] + "," + bks[1] + "..." + bks[-2] + "," + bks[-1]
            else:
                try:
                    bks = bks[0]
                except IndexError:
                    bks = _("No book selected!")
            cfg = ":" + self.get("ecb_savedConfig", "")
            cfg = ":" + cfg if (not self.get("c_diglot") and self.get("c_doublecolumn", False)) else cfg
            prjcfg = "{}{}".format(prjid, cfg) 
            if self.get("c_diglot"):
                cfg2 = ":" + self.get("ecb_diglotSecConfig", "")
                prjcfg2 = "{}{}".format(self.get("fcb_diglotSecProject", "!NoSecPrj!"), cfg2) 
                prjcfg = "[{} + {}]".format(prjcfg, prjcfg2)
            return "PTXprint {}  -  {}  ({})".format(VersionStr, prjcfg, bks)

    def readCopyrights(self):
        with open(os.path.join(pycodedir(), "picCopyrights.json"), encoding="utf-8", errors="ignore") as inf:
            self.copyrightInfo = json.load(inf)
        fname = os.path.join(self.settings_dir, self.prjid, "shard", "ptxprint", "picCopyrights.json")
        if os.path.exists(fname):
            with open(fname, encoding="utf-8", errors="ignore") as inf:
                try:
                    cupdates = json.load(inf)
                    self.copyrightInfo.update(cupdates)
                except json.decode.JSONDecodeError as e:
                    self.doError(_("Json parsing error in {}").format(fname),
                                 secondary = _("{} at line {} col {}").format(e.msg, e.lineno, e.colno))

    def picMedia(self, src):
        if self.copyrightInfo is None:
            self.readCopyrights()
        m = re.match(self.getPicRe(), src)
        if m is not None and m.group(1).lower() in self.copyrightInfo['copyrights']:
            media = self.copyrightInfo['copyrights'][m.group(1).lower()]['media']
            return (media['default'], media['limit'])
        return (None, None)
    
    def configFRT(self):
        return os.path.join(self.configPath(self.configName()), "FRTlocal.sfm")

    def configName(self):
        return self.configId or None

    def configPath(self, cfgname=None, prjid=None, makePath=True):
        if prjid is None:
            prjid = self.prjid
        if self.settings_dir is None or prjid is None:
            return None
        prjdir = os.path.join(self.settings_dir, prjid, "shared", "ptxprint")
        if cfgname is not None and len(cfgname):
            prjdir = os.path.join(prjdir, cfgname)
        if makePath:
            os.makedirs(prjdir,exist_ok=True)
        return prjdir

    def configLocked(self):
        return self.get("t_invisiblePassword") != ""

    def readConfig(self, cfgname=None):
        if cfgname is None:
            cfgname = self.configName() or ""
        path = os.path.join(self.configPath(cfgname, makePath=False), "ptxprint.cfg")
        if not os.path.exists(path):
            return -1
        config = configparser.ConfigParser()
        with open(path, encoding="utf-8", errors="ignore") as inf:
            config.read_file(inf)
        (oldversion, forcerewrite) = self.versionFwdConfig(config, cfgname)
        self.loadingConfig = True
        self.localiseConfig(config)
        self.loadConfig(config)
        if self.get("ecb_book") == "":
            self.set("ecb_book", list(self.getAllBooks().keys())[0])
        if self.get("c_diglot") and not self.isDiglot:
            self.diglotView = self.createDiglotView()
        else:
            self.setPrintBtnStatus(2)
            self.diglotView = None
        self.loadingConfig = False
        if self.get("bl_fontR", skipmissing=True) is None:
            fname = self.ptsettings.get('DefaultFont', 'Arial')
            font = FontRef(fname, "")
            self.set("bl_fontR", font)
        # clear generated pictures
        for f in ("tmpPics", "tmpPicLists"):
            path2del = os.path.join(self.working_dir, f)
            if os.path.exists(path2del):
                try:
                    rmtree(path2del)
                    os.makedirs(path2del, exist_ok=True)
                except (OSError, PermissionError):
                    pass
        if forcerewrite:
            self.writeConfig(cfgname=cfgname)
        return oldversion

    def writeConfig(self, cfgname=None, force=False):
        if not force and self.configLocked():
            return
        if cfgname is None:
            cfgname = self.configName() or ""
        path = os.path.join(self.configPath(cfgname=cfgname, makePath=True), "ptxprint.cfg")
        config = self.createConfig()
        self.globaliseConfig(config)
        with open(path, "w", encoding="utf-8") as outf:
            config.write(outf)
        if self.triggervcs:
            with open(os.path.join(self.settings_dir, self.prjid, "unique.id"), "w") as outf:
                outf.write("ptxprint-{}".format(datetime.datetime.now().isoformat(" ")))
            self.triggervcs = False

    def _configset(self, config, key, value, update=True):
        if "/" in key:
            (sect, k) = key.split("/", maxsplit=1)
        else:
            (sect, k) = (key, "")
        if not config.has_section(sect):
            config.add_section(sect)
            hasval = False
        else:
            hasval = config.has_option(sect, k)
        if isinstance(value, bool):
            value = "true" if value else "false"
        if update or not hasval:
            config.set(sect, k, value)

    def createConfig(self):
        def sortkeys(x):
            k, v = x
            if k in self._activekeys:
                return (0, k, v)
            else:
                return (1, k, v)
        if self.get("_version", skipmissing=True) is None:
            self.set("_version", ConfigVersion)
        self.set("_gitversion", GitVersionStr)
        for a in (("_prjid", self.prjid), ("_cfgid", self.configName())):
            self.set(a[0], a[1])
        config = configparser.ConfigParser()
        for k, v in sorted(ModelMap.items(), key=sortkeys):
            if v[0] is None or k.endswith("_"):
                continue
            if k in self._attributes:
                v = self._attributes[k]
                val = getattr(self, v[0])
                if val is None:
                    continue
                if v[1]:
                    val = "\n".join(x.withvars(self) for x in val)
                else:
                    val = val.withvars(self)
            elif v[0].startswith("bl_"):
                    vfont = self.get(v[0], skipmissing=True)
                    if vfont is None:
                        continue
                    val = vfont.asConfig()
            else:
                if v[0] is None:
                    continue
                val = self.get(v[0], asstr=True, skipmissing=True)
            if k in self._settingmappings:
                if val == "" or val == self.ptsettings.dict.get(self._settingmappings[k], ""):
                    continue
            self._configset(config, k, str(val) if val is not None else "", update=False)
        for k in self.allvars():
            self._configset(config, "vars/"+str(k), self.getvar(str(k)), update=False)
        for k in self.allvars(dest="strongs"):
            self._configset(config, "strongsvars/"+str(k), self.getvar(str(k), dest="strongs"), update=False)
        return config

    def _config_get(self, config, section, option, conv=None, fallback=_UNSET, **kw):
        try:
            v = config.get(section, option, **kw)
        except (NoSectionError, NoOptionError):
            if fallback is _UNSET:
                raise
            return fallback
        if conv is None:
            return v
        if v == "" and fallback is not _UNSET:
            return fallback
        return conv(v)

    def versionFwdConfig(self, config, cfgname):
        version = self._config_get(config, "config", "version", conv=float, fallback=ConfigVersion)
        forcerewrite = False
        v = float(version)
        if v < 0.9:
            try:
                self._configset(config, "document/ifshowchapternums", not config.getboolean("document", "ifomitchapternum", fallback=False))
                self._configset(config, "document/ifshowversenums", not config.getboolean("document", "ifomitallverses", fallback=False))
                self._configset(config, "document/bookintro", not config.getboolean("document", "supressbookintro", fallback=False))
                self._configset(config, "document/introoutline", not config.getboolean("document", "supressintrooutline", fallback=False))
                self._configset(config, "document/firstparaindent", not config.getboolean("document", "supressindent", fallback=False))
                self._configset(config, "document/sectionheads", not config.getboolean("document", "supresssectheads", fallback=False))
                self._configset(config, "document/parallelrefs", not config.getboolean("document", "supressparallels", fallback=False))
            except:
                pass
        if v < 1.2:
            bl = self._config_get(config, "project", "booklist")
            self._configset(config, "project/bookscope", "multiple" if len(bl) else "single")
        if v < 1.201:
            for d in ('PicLists', 'AdjLists'):
                p = os.path.join(self.configPath(cfgname), d)
                if not os.path.exists(p):
                    continue
                for f in os.listdir(p):
                    if "-draft" in f:
                        newf = os.path.join(p, f.replace("-draft", "-"+cfgname))
                        if not os.path.exists(newf):
                            move(os.path.join(p, f), newf)
        if v < 1.290:
            path = os.path.join(self.configPath(cfgname), "ptxprint.sty")
            if not os.path.exists(path):
                modpath = os.path.join(self.configPath(cfgname), "ptxprint-mods.sty")
                if os.path.exists(modpath):
                    move(modpath, path)
                    with open(modpath, "w") as outf:
                        pass
        if v < 1.400:
            indent = config.getfloat("document", "indentunit", fallback="2.000")
            if indent == 2.0 and config.getboolean("paper", "columns", fallback=True):
                    self._configset(config, "document/indentunit", "1.000")
        if v < 1.403:   # no need to bump version for this and merge this with a later version test
            f = os.path.join(self.configPath(cfgname), "NestedStyles.sty")
            if os.path.exists(f):
                os.remove(f)
        if v < 1.404:
            self._configset(config, "fancy/versedecoratorshift", "-5")
        if v < 1.502:
            if not config.has_option("document", "includimg"):
                self._configset(config, "document/includeimg", config.get("snippets", "imgcredits", fallback="false"))
            colophontext = config.get("project", "colophontext", fallback="").replace("zCopyright", "zcopyright")\
                            .replace("zImageCopyrights", "zimagecopyrights").replace("zLicense", "zlicense")
            self._configset(config, "project/colophontext", colophontext)
        if v < 1.503:
            marginmms = config.getfloat("paper", "margins")
            self._configset(config, "paper/topmargin", f2s(config.getfloat("paper", "topmarginfactor", fallback=1.0) * marginmms))
            self._configset(config, "paper/headerpos", f2s(config.getfloat("paper", "topmarginfactor", fallback=1.0) * marginmms \
                        - config.getfloat("header", "headerposition", fallback=1.0) * marginmms\
                        - config.getfloat("paper", "fontfactor") * 25.4 / 72.27))
            self._configset(config, "paper/bottommargin", f2s(config.getfloat("paper", "bottommarginfactor", fallback=1.0) * marginmms))
            self._configset(config, "paper/footerpos", f2s(config.getfloat("header", "footerposition", fallback=1.0) * marginmms))
            self._configset(config, "paper/rulegap", f2s(config.getfloat("header", "ruleposition", fallback=0.)))
        if v < 1.504:
            try:
                self._configset(config, "notes/fneachnewline", not config.getboolean("notes", "fnparagraphednotes", fallback=False))
                self._configset(config, "notes/xreachnewline", not config.getboolean("notes", "xrparagraphednotes", fallback=False))
            except:
                pass
        if v < 1.601:
            # invert right and left in Justification in styles
            pass
        if v < 1.602:
            self._configset(config, "notes/belownoterulespace", "3.0")
            self._configset(config, "notes/abovenotespace", f2s(config.getfloat("notes", "abovenotespace", fallback=6.0) - 3.0))
        if v < 1.7:
            if config.getboolean("document", "pdfx1aoutput", fallback=False):
                self._configset(config, "document/pdfoutput", "PDF/X-1A")
        if v < 1.9:
            val = self._config_get(config, "scrmymr", "syllables", fallback="")
            self._configset(config, "scripts/mymr/syllables", config.getboolean("scrmymr", "syllables", fallback=False) if val else False)
        if v < 1.93:
            self._configset(config, "notes/xrcolside", "3")
        if v < 1.94:
            self._configset(config, "document/ifshow1chbooknum", not config.getboolean("document", "ifomitsinglechnum", fallback=False))
            self._configset(config, "header/ifshowchapter", not config.getboolean("header", "ifomitrhchapnum", fallback=False))
            self._configset(config, "header/ifshowverse", config.getboolean("header", "ifverses", fallback=False))
            self._configset(config, "header/ifshowbook", True)
        if v < 1.95:
            self._configset(config, "paper/bottomrag", "0")
        if v < 1.96:
            self._configset(config, "notes/r_fnpos", "normal")
            self._configset(config, "project/uilevel", "4" if config.getboolean("project", "hideadvsettings", fallback=True) else "6")
            digmap = config.get("document", "digitmapping", fallback="Default")
            if digmap != "Default":
                for a in ('regular', 'bold', 'bolditalic', 'italic'):
                    f = config.get("document", "font{}".format(a), fallback="||||")
                    bits = f.split("|")
                    if len(bits) < 3:
                        bits += [] * (3-len(bits))
                    bits.append("mapping=mappings/{}digits".format(digmap.lower()))
                    f = "|".join(bits)
                    self._configset(config, "document/font{}".format(a), f)
            for a in ('fn', 'xr'):
                self._configset(config, "notes/{}pos".format(a), "page")
                self._configset(config, "notes/{}ruleposn".format(a), "1")
                self._configset(config, "notes/{}ruleindent".format(a), "0")
                self._configset(config, "notes/{}rulelength".format(a), "100")
                self._configset(config, "notes/{}rulethick".format(a), "0.4")
        if v < 1.97:
            ls = ''
            gm = ''
            if config.getboolean("paragraph", "linespacebase", fallback=False):
                self._configset(config, "paragraph/linespacebase", False)
                ls = "   * Legacy 1/14 LineSpacing\n"
            if config.getboolean("paragraph", "useglyphmetrics", fallback=False):
                self._configset(config, "paragraph/useglyphmetrics", False)
                gm = "   * Use glyph metrics\n"
            if len(ls+gm) > 0:
                self.doError("Warning: Compatibility Settings Changed", 
                    secondary="We noticed the following setting(s) were turned ON:\n" + ls + gm + \
                              "We have turned these settings OFF on the Advanced page due to the confusion it caused people. " + \
                              "Note that compatibility settings will change your layout. If you need to keep the layout as it " + \
                              "is then turn the compatibility setting(s) back ON. We will not do this again." + \
                              "\n\n(Ignore this minor warning if you don't understand it)")
                forcerewrite = True

        if v < 2.06:
            self._configset(config, "document/diffcolayout", not config.getboolean("document", "clsinglecol", fallback=False))
            diffcolbooks = config.get("document", "clsinglecolbooks", fallback="FRT INT PSA PRO BAK GLO")
            self._configset(config, "document/diffcolayoutbooks", diffcolbooks)
        if v < 2.07:
            if config.getboolean("project", "usechangesfile", fallback=False):
                cfile = os.path.join(self.configPath(cfgname), "changes.txt")
                if not os.path.exists(cfile):
                    with open(cfile, "w", encoding="utf-8") as outf:
                        outf.write(chgsHeader)
        if v < 2.08:
            if config.get("snippets", "pdfoutput", fallback="None") == "None":
                self._configset(config, "snippets/pdfoutput", "Screen")
        # print(f"{forcerewrite} {v} {ConfigVersion} {cfgname} {self.configPath(cfgname)}")

        if v < 2.09:
            if config.get("finish", "pgsperspread", fallback="None") == "None":
                self._configset(config, "finishing/pgsperspread", "1")
            if config.get("paper", "cropmarks", fallback="None") == "None":
                self._configset(config, "paper/cropmarks", config.getboolean("paper", "ifcropmarks", fallback=False))
        self._configset(config, "config/version", ConfigVersion)
            
        styf = os.path.join(self.configPath(cfgname), "ptxprint.sty")
        if not os.path.exists(styf):
            with open(styf, "w", encoding="utf-8") as outf:
                outf.write("# This file left intentionally blank\n")
        return (v, forcerewrite)

    def localiseConfig(self, config):
        for a in ("header/hdrleft", "header/hdrcenter", "header/hdrright", "footer/ftrcenter"):
            (sect, opt) = a.split("/")
            s = config.get(sect, opt, fallback=None)
            if s:
                s = global2localhdr(s)
                config.set(sect, opt, s)

    def globaliseConfig(self, config):
        for a in ("header/hdrleft", "header/hdrcenter", "header/hdrright", "footer/ftrcenter"):
            (sect, opt) = a.split("/")
            s = config.get(sect, opt, fallback=None)
            if s:
                s = local2globalhdr(s)
                config.set(sect, opt, s)

    def loadConfig(self, config, setv=None, setvar=None, dummyload=False):
        if setv is None:
            def setv(k, v): self.set(k, v, skipmissing=True)
            def setvar(opt, val, dest): self.setvar(opt, val, dest=dest)
            self.clearvars()
        for sect in config.sections():
            # if sect == "paper":
                # import pdb; pdb.set_trace()
            for opt in config.options(sect):
                key = "{}/{}".format(sect, opt)
                val = config.get(sect, opt)
                if key in ModelMap:
                    v = ModelMap[key]
                    if val == "None":
                        val = None
                    if key in self._attributes:
                        w = self._attributes[key]
                        if w[1]:
                            val = val.split("\n") if val is not None else []
                            val = [Path(x, self) for x in val if x is not None]
                            if w[2] is not None:
                                setv(w[2], ", ".join(pdfre.sub(r"\1", x.as_posix()) for x in val))
                        else:
                            val = Path(val, self) if val is not None else None
                            if w[2] is not None and val is not None:
                                setv(w[2], pdfre.sub(r"\1", val.as_posix()))
                        if not dummyload:
                            setattr(self, w[0], val)
                    else:
                        try: # Safeguarding from changed/missing keys in .cfg  or v[0].startswith("f_") 
                            if v[0].startswith("s_"):
                                val = float(val) if val is not None and val != '' else 0
                            elif v[0].startswith("c_"):
                                val = config.getboolean(sect, opt) if val else False
                            elif v[0].startswith("bl_"):
                                val = FontRef.fromConfig(val)
                            if val is not None:
                                setv(v[0], val)
                        except AttributeError:
                            pass # ignore missing keys
                elif sect == "vars":
                    setvar(opt, val or "", None)
                elif sect == "strongsvars":
                    setvar(opt, val or "", "strongs")
                elif sect in FontModelMap:
                    v = FontModelMap[sect]
                    if v[0].startswith("bl_") and opt == "name":    # legacy
                        vname = re.sub(r"\s*,?\s+\d+\s*$", "", val) # strip legacy style and size
                        vstyle = config.get(sect, "style", fallback="")
                        vfeats = {}
                        if config.get(sect, "fakeit", fallback="False").lower() == "true":
                            for a in ("embolden", "slant"):
                                v = config.getfloat(sect, a, fallback=0.)
                                if v != 0.:
                                    vfeats[a] = v
                        vf = FontRef(vname, vstyle, feats=vfeats)
                        vf.updateFeats(config.get("font", "features", fallback=""), keep=True)
                        vf.isGraphite = config.getboolean("font", "usegraphite", fallback=False)
                        # print(FontModelMap[sect][0], vf)
                        setv(FontModelMap[sect][0], vf)
                if key in self._activekeys:
                    getattr(self, self._activekeys[key])()
        for k, v in self._settingmappings.items():
            (sect, name) = k.split("/")
            try:
                val = config.get(sect, name)
            except configparser.NoOptionError:
                setv(ModelMap[k][0], self.ptsettings.dict.get(v, ""))
        if not dummyload and self.get("c_thumbtabs"):
            self.updateThumbLines()
        self.updateFont2BaselineRatio()

    def updateStyles(self, version):
        if version < 0:
            return
        if version < 1.601:
           if self.get("fcb_textDirection", "") == "rtl":
                for k in self.styleEditor.allStyles():
                    j = self.styleEditor.getval(k, 'Justification')
                    if j == "Right":
                        self.styleEditor.setval(k, 'Justification', 'Left')
                    elif j == "Left":
                        self.styleEditor.setval(k, 'Justification', 'Right')
        elif version < 1.602:
            for a in "fx":
                for b in "klmopqrtvw":
                    v = self.styleEditor.getval(a+b, 'FontSize', None)
                    if v is not None:
                        self.styleEditor.setval(a+b, 'FontSize', None)
                        self.styleEditor.setval(a+b, 'FontScale', v)

        if self.get('r_xrpos') == "blend":
            self.styleEditor.setval('x', 'NoteBlendInto', 'f')
        else:
            self.styleEditor.setval('x', 'NoteBlendInto', None)


    def editFile_delayed(self, *a):
        pass

    def saveStyles(self, force=False):
        if not force and self.configLocked():
            return
        fname = os.path.join(self.configPath(self.configName(), makePath=True), "ptxprint.sty")
        with open(fname, "w", encoding="Utf-8") as outf:
            self.styleEditor.output_diffile(outf)

    def savePics(self, fromdata=True, force=False):
        if not force and self.configLocked():
            return
        if self.picinfos is not None and self.picinfos.loaded:
            self.picinfos.out(os.path.join(self.configPath(self.configName()),
                                    "{}-{}.piclist".format(self.prjid, self.configName())))
        self.picChecksView.writeCfg(os.path.join(self.settings_dir, self.prjid), self.configName())

    def loadPics(self, mustLoad=True, fromdata=True):
        if self.loadingConfig:
            return
        if self.picinfos is None:
            self.picinfos = PicInfo(self)
        else:
            self.savePics(fromdata=fromdata)
            self.picinfos.clear(self)
        if not self.get("c_includeillustrations"):
            return
        if self.diglotView is None:
            res = self.picinfos.load_files(self)
        else:
            res = self.picinfos.load_files(self, suffix="L")
            digpicinfos = PicInfo(self.diglotView)
            if digpicinfos.load_files(self.diglotView, suffix="R"):
                self.picinfos.merge("L", "R", digpicinfos, mergeCaptions=self.get("c_diglot2captions", False))
        if res:
            self.savePics(fromdata=fromdata)
        elif mustLoad:
            self.onGeneratePicListClicked(None)
            
    def onGeneratePicListClicked(self, btn):
        pass

    def getPicRe(self):
        r = r"(?i)_?(" + "|".join(sorted(self.copyrightInfo['copyrights'].keys(), key=lambda x:(-len(x), x))) \
                + ")(\d+)([a-z]*)"
        return r

    def getDraftFilename(self, bk, ext=".piclist"):
        fname = self.getBookFilename(bk, self.prjid)
        if fname is None:
            return None
        cname = "-" + (self.configName() or "Default")
        doti = fname.rfind(".")
        res = fname[:doti] + cname + fname[doti:] + ext if doti > 0 else fname + cname + ext
        return res

    def getAdjListFilename(self, bk, ext=".adj"):
        fname = self.getBookFilename(bk, self.prjid)
        if fname is None:
            return None
        cname = "-" + (self.configName() or "Default")
        if self.get("c_diglot"):
            cname = cname + "-diglot"
        doti = fname.rfind(".")
        res = fname[:doti] + cname + fname[doti:] + ext if doti > 0 else fname + cname + ext
        return res

    def generateFrontMatter(self, frtype="basic", inclcover=False):
        destp = self.configFRT()
        if frtype == "basic":
            srcp = os.path.join(pycodedir(), "FRTtemplateBasic.txt")
        elif frtype == "advanced":
            srcp = os.path.join(pycodedir(), "FRTtemplateAdvanced.txt")
        elif frtype == "paratext":
            fname = self.getBookFilename("FRT", self.prjid)
            if fname is None:
                return False
            srcp = os.path.join(self.settings_dir, self.prjid, fname)
            
        copyfile(srcp, destp)
        return True

    def generateHyphenationFile(self):
        listlimit = 63929  # 65520 # 32749
        prjid = self.get("fcb_project") # self.dict['project/id']
        prjdir = os.path.join(self.settings_dir, self.prjid)
        infname = os.path.join(self.ptsettings.basedir, prjid, 'hyphenatedWords.txt')
        outfname = os.path.join(self.ptsettings.basedir, prjid, "shared", "ptxprint", 'hyphen-{}.tex'.format(prjid))
        hyphenatedWords = []
        if not os.path.exists(infname):
            m1 = _("Failed to Generate Hyphenation List")
            m2 = _("{} Paratext Project's Hyphenation file not found:\n{}").format(prjid, infname)
        else:
            m2b = ""
            m2c = ""
            m2d = ""
            z = 0
            nohyphendata = []
            with universalopen(infname) as inf:
                for l in inf.readlines()[8:]: # Skip over the Paratext header lines
                    l = l.strip().replace(u"\uFEFF", "")
                    l = re.sub(r"[*\",;:!?']", "", l) # to be continued...
                    l = re.sub(r"-", "\u2010", l)
                    l = re.sub(r"=", "-", l)
                    # Paratext doesn't seem to allow segments of 1 character to be hyphenated  (for example: a-shame-d) 
                    # (so there's nothing to filter them out, because they don't seem to exist!)
                    # Also need to strip out words with punctuation chars (eg. Burmese \u104C .. \u104F)
                    if "-" in l:
                        if regex.search(r'[^\p{L}\p{M}\-\u200C\u200D]', l):
                            z += 1
                        else:
                            if l[0] != "-" and len(l) > 5:
                                hyphenatedWords.append(l)
                    elif "\u2010" not in l:
                        lng = len(l)
                        if lng > 9:
                            nohyphendata.append(l)
            c = len(hyphenatedWords)
            if c >= listlimit:
                hyphwords = set([x.replace("-", "") for x in hyphenatedWords])
                acc = {}
                usfms = self.get_usfms()
                for bk in self.getBooks():
                    u = usfms.get(bk)
                    u.getwords(init=acc, constrain=hyphwords)
                hyphcounts = {k:acc.get(k.replace("-",""), 0) for k in hyphenatedWords}
                hyphenatedWords = [k for k, v in sorted(hyphcounts.items(), key = lambda x: (-x[1], -len(x[0])))][:listlimit]
                m2b = _("\n\nThat is too many for XeTeX! List truncated to longest {} words found in the active sources.").format(len(hyphenatedWords))
            hyphenatedWords.sort(key = lambda s: s.casefold())
            outlist = '\\catcode"200C=11\n\\catcode"200D=11\n\\hyphenation{' + "\n".join(hyphenatedWords) + "}"
            with open(outfname, "w", encoding="utf-8") as outf:
                outf.write(outlist)
            if len(hyphenatedWords) > 1:
                m1 = _("Hyphenation List Generated")
                m2a = _("{} hyphenated words were gathered\nfrom Paratext's Hyphenation Word List.").format(c)
                if z > 0:
                    m2c = _("\n\nNote: {} words containing non-Letters and non-Marks").format(z) + \
                            _("\n(ZWJ, ZWNJ, etc.) have not been included in the hyphenation list.")
                if len(nohyphendata) > 0:
                    m2d = _("\n\n{} words were at least 10 characters long but had no hyphenation marked").format(len(nohyphendata))
                m2 = m2a + m2b + m2c + m2d
            else:
                m1 = _("Hyphenation List was NOT Generated")
                m2 = _("No valid words were found in Paratext's Hyphenation List")
        self.doError(m1, m2)

    def onFindMissingCharsClicked(self, btn_findMissingChars):
        count = collections.Counter()
        prjid = self.get("fcb_project")
        prjdir = os.path.join(self.settings_dir, prjid)
        bks = self.getBooks()
        for bk in bks:
            fname = self.getBookFilename(bk, prjid)
            fpath = os.path.join(prjdir, fname)
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as inf:
                    # Strip out all markers themselves, and English content fields
                    sfmtxt = inf.read()
                    sfmtxt = re.sub(r'\\id .+?\r?\n', '', sfmtxt)
                    sfmtxt = re.sub(r'\\rem .+?\r?\n', '', sfmtxt)
                    # throw out illustration markup, BUT keep the caption text (USFM2 + USFM3)
                    sfmtxt = re.sub(r'\\fig (.*\|){5}([^\\]+)?\|[^\\]+\\fig\*', '\2', sfmtxt) 
                    sfmtxt = re.sub(r'\\fig ([^\\]+)?\|.*src=[^\\]+\\fig\*', '\1', sfmtxt) 
                    sfmtxt = re.sub(r'\\[+a-z]+\d?\*? ?', '', sfmtxt) # remove all \sfm codes
                    sfmtxt = re.sub(r'[0-9]', '', sfmtxt) # remove all digits
                    bkcntr = collections.Counter(sfmtxt)
                    count += bkcntr
        # slist = sorted(count.items(), key=lambda pair: pair[0])
        # f = TTFont(*self.get("bl_fontR"))
        f = self.get("bl_fontR").getTtfont()
        allchars = ''.join([i[0] for i in count.items()])
        if self.get("fcb_glossaryMarkupStyle") == "fb":
            allchars += "\u2e24\u2e25"
        if self.get("fcb_glossaryMarkupStyle") == "fc":
            allchars += "\u230a\u230b"
        if self.get("fcb_glossaryMarkupStyle") == "cc":
            allchars += "\u231e\u231f"
        missing = f.testcmap(allchars)
        self.set("t_missingChars", ' '.join(missing))
        return missing

    def onFontExtraRclicked(self, bl_fontExtraR):
        self.getFontNameFace("bl_fontExtraR")
        finfor = self.get('bl_fontR')
        finfoe = self.get('bl_fontExtraR')
        if finfor.name == finfoe.name:
            self.doError(_("The Fallback Font needs to be something other than the Regular Font."),
                         _("Please select a different Font."))
        else:
            f = finfoe.getTtfont()
            msngchars = self.get("t_missingChars") # .split(" ")
            msngchars = spclChars = re.sub(r"\\[uU]([0-9a-fA-F]{4,6})", lambda m:chr(int(m.group(1), 16)), msngchars)
            stillmissing = f.testcmap(msngchars)
            if len(stillmissing):
                self.doError(_("The Fallback Font just selected does NOT support all the missing characters listed."),
                             _("Please select a different Font."))

    def getExtOrder(self):
        # If the preferred image type(s) has(have) been specified, parse that string
        imgord = self.get("t_imageTypeOrder").lower()
        extOrder = re.sub("[ ,;/><]"," ",imgord).split()
        if not len(extOrder): # If the user hasn't defined a specific order then we can assign this
            if self.get("c_useLowResPics"): # based on whether they prefer small/compressed image formats
                extOrder = ["jpg", "jpeg", "png", "tif", "tiff", "bmp", "pdf"] 
            else:                              # or prefer larger high quality uncompressed image formats
                extOrder = ["pdf", "bmp", "tiff", "tif", "png", "jpeg", "jpg"] # reverse order
        return extOrder

    def finished(self):
        pass

    def incrementProgress(self, val=None):
        pass

    def getStyleSheets(self, cfgname=None, generated=False, prjid=None, subdir=""):
        if prjid is None:
            prjid = self.prjid
        if prjid is None:
            return []
        res = []
        if cfgname is None:
            cfgname = self.configName()
        cpath = self.configPath(cfgname=cfgname, makePath=False, prjid=prjid)
        rcpath = self.configPath("", makePath=False, prjid=prjid)
        res.append(os.path.join(self.scriptsdir, "ptx2pdf.sty"))
        if self.get('c_useCustomSty'):
            res.append(os.path.join(self.settings_dir, prjid, "custom.sty"))
        if self.get('c_useModsSty'):
            for p in (cpath, rcpath):
                fp = os.path.join(p, subdir, "ptxprint-mods.sty")
                if os.path.exists(fp):
                    res.append(fp)
                    break
        res.append(os.path.join(cpath, subdir, "ptxprint.sty"))
        return res

    def _getArchiveFiles(self, books, prjid=None, cfgid=None):
        sfiles = {'c_useCustomSty': "custom.sty",
                  # should really parse changes.txt and follow the include chain, sigh
                  'c_usePrintDraftChanges': "PrintDraftChanges.txt",
                  None: "picChecks.txt"}
        res = {}
        cfgchanges = {}
        tmpfiles = []
        pictures = set()
        if prjid is None:
            prjid = self.prjid
        if cfgid is None:
            cfgid = self.configName()
        cfpath = "shared/ptxprint/"
        if cfgid is not None:
            cfpath += cfgid+"/"
        basecfpath = self.configPath(cfgname=cfgid, prjid=prjid)
        interlang = self.get("t_interlinearLang") if self.get("c_interlinear") else None

        # pictures and texts
        fpath = os.path.join(self.settings_dir, prjid)
        scope = self.get("r_book")
        if scope == "module":
            bk = books[0]
            res[os.path.join(fpath, bk)] = os.path.basename(bk)
            cfgchanges['btn_chooseBibleModule'] = (Path("${prjdir}/"+os.path.basename(bk)), "moduleFile")
            cfgchanges['lb_bibleModule'] = os.path.basename(bk)
            usfms = self.get_usfms()
            mod = Module(os.path.join(fpath, bk), usfms=usfms)
            books.extend(mod.getBookRefs())
        for bk in books:
            fname = self.getBookFilename(bk, prjid)
            if fname is not None:
                res[os.path.join(fpath, fname)] = os.path.basename(fname)
            if interlang is not None:
                intpath = "Interlinear_{}".format(interlang)
                intfile = "{}_{}.xml".format(intpath, bk)
                res[os.path.join(fpath, intpath, intfile)] = os.path.join(intpath, intfile)
        exclFigsFolder = self.get("c_exclusiveFiguresFolder")
        self.picinfos.getFigureSources(exclusive=exclFigsFolder)
        if self.get("c_useCustomFolder"):
            cfgchanges["btn_selectFigureFolder"] = (Path("${prjdir}/figures"), "customFigFolder")
            cfgchanges["c_useCustomFolder"] = (False, None)
        pathkey = 'src path'
        for f in (p[pathkey] for p in self.picinfos.values() if pathkey in p and p['anchor'][:3] in books):
                res[f] = "figures/"+os.path.basename(f)
        xrfile = self.get("btn_selectXrFile")
        if xrfile is not None:
            res[xrfile] = os.path.basename(xrfile)
            cfgchanges["btn_selectXrFile"] = res[xrfile]

        # piclists
        piclstpath = os.path.join(basecfpath, "PicLists")
        picbks = set(self.getDraftFilename(bk) for x in books)
        if os.path.exists(piclstpath):
            for pic in os.listdir(piclstpath):
                if pic.endswith(".piclist") and pic in picbks:
                    res[os.path.join(piclstpath, pic)] = cfpath+"PicLists/"+pic
        jobpiclistfs = ["{}-{}.piclist".format(prjid, cfgid), "picChecks.txt"]
        for jobpiclistf in jobpiclistfs:
            jobpiclist = os.path.join(basecfpath, jobpiclistf)
            if os.path.exists(jobpiclist):
                res[jobpiclist] = cfpath+jobpiclistf

        # borders
        for k, v in Borders.items():
            if self.get(k):
                islist = v[2].startswith("\\")
                fname = getattr(self, v[0], (None if islist else v[2]))
                if v[0] == "watermark" and fname is None:
                    fname = "A5-CopyrightWatermark.pdf"
                # print(f"{k=}, {v=}, {fname=}")
                if fname is None: continue
                if not isinstance(fname, (list, tuple)):
                    fname = [fname]
                for f in fname:
                    res[f.as_posix()] = "shared/ptxprint/"+f.name
                    # print(f"{f.as_posix()=}, {f.name=}")

        # fonts
        for k, v in TexModel._fonts.items():
            if v[1] is None or self.get(v[1]):
                font_info = self.get(v[0])
                if font_info is None: continue
                f = font_info.getTtfont()
                if f.filename is None: continue
                fname = os.path.basename(f.filename)
                res[f.filename] = "shared/fonts/"+fname
                
        for k, v in self.styleEditor.sheet.items():
            font_info = v.get(' font', self.styleEditor.basesheet.get(k, {}).get(' font', None))
            if font_info is not None:
                f = font_info.getTtfont()
                if f.filename is None: continue
                fname = os.path.basename(f.filename)
                res[f.filename] = "shared/fonts/"+fname

        if prjid:
            mdir = os.path.join(self.settings_dir, prjid, "shared", "fonts", "mappings")
            if os.path.exists(mdir):
                for f in os.listdir(mdir):
                    if f == ".uuid":
                        continue
                    res[os.path.join(mdir, f)] = "shared/fonts/mappings/"+f

        # sidebar images
        mystyles = self.styleEditor.copy()
        for k, v in mystyles.sheet.items():
            for a in ('BgImage', 'FgImage'):
                val = v.get(a, mystyles.basesheet.get(k, {}).get(a, None))
                if val is not None:
                    fname = os.path.basename(val)
                    res[val] = "figures/"+fname
                    mystyles.setval(k, a, "../../../figures/"+fname)


        tempfile = NamedTemporaryFile("w", encoding="utf-8", newline=None, delete=False)
        mystyles.output_diffile(tempfile, inArchive=True)
        tempfile.close()
        res[tempfile.name] = cfpath+"ptxprint.sty"
        tmpfiles.append(tempfile.name)

        # config files - take the whole tree even if not needed
        for dp, dn, fn in os.walk(basecfpath):
            op = os.path.join(cfpath, os.path.relpath(dp, basecfpath))
            for f in fn:
                if f not in ('ptxprint.sty', 'ptxprint.cfg') or dp != basecfpath:
                    res[os.path.join(dp, f)] = os.path.join(op, f)
        sp = os.path.join(self.settings_dir, prjid, 'shared', 'ptxprint')
        for f in os.listdir(sp):
            fp = os.path.join(sp, f)
            if os.path.isfile(fp):
                res[fp] = os.path.join('shared', 'ptxprint', f)

        # special config files not in config tree
        for t, b in sfiles.items():
            if isinstance(t, str) and not self.get(t): continue
            c = [b] if isinstance(b, str) else b
            for a  in c:
                s = os.path.join(self.settings_dir, prjid, a)
                if os.path.exists(s):
                    res[s] = a

        if interlang is not None:
            res[os.path.join(fpath, 'Lexicon.xml')] = 'Lexicon.xml' 

        script = self.customScript
        if script: # is not None and len(script):
            res[script] = os.path.basename(script)
            cfgchanges["btn_selectScript"] = os.path.join(self.settings_dir, prjid, os.path.basename(script))

        pts = self._getPtSettings(prjid=prjid)
        ptres = pts.getArchiveFiles()
        res.update(ptres)
        return (res, cfgchanges, tmpfiles)

    def createDiglotView(self):
        self.setPrintBtnStatus(2)
        prjid = self.get("fcb_diglotSecProject")
        cfgid = self.get("ecb_diglotSecConfig")
        if prjid is None or cfgid is None:
            digview = None
        else:
            digview = ViewModel(self.settings_dir, self.working_dir, self.userconfig, self.scriptsdir)
            digview.isDiglot = True
            digview.setPrjid(prjid)
            if cfgid is None or cfgid == "" or not digview.setConfigId(cfgid):
                digview = None
        if digview is None:
            self.setPrintBtnStatus(2, _("No Config found for Diglot"))
        else:
            digview.isDiglot = True
        return digview

    def createArchive(self, filename=None):
        if filename is None:
            filename = os.path.join(self.configPath(self.configName()), "ptxprintArchive.zip")
        if not filename.lower().endswith(".zip"):
            filename += ".zip"
        try:
            zf = ZipFile(filename, mode="w", compression=ZIP_DEFLATED)  # need at least python 3.7 for: compresslevel=9
        except OSError:
            self.doError(_("Error: Cannot create Archive!"), secondary=_("The ZIP file seems to be open in another program."))
            return
        self._archiveAdd(zf, self.getBooks(files=True))
        if self.diglotView is not None:
            self.diglotView._archiveAdd(zf, self.getBooks(files=True), parent=self.prjid)
            pf = "{}/local/ptxprint/{}/diglot.sty".format(self.prjid, self.configName())
            ipf = os.path.join(self.settings_dir, pf)
            if os.path.exists(ipf):
                zf.write(ipf, pf)
        from ptxprint.runjob import RunJob
        runjob = RunJob(self, self.scriptsdir, self.args, inArchive=True)
        runjob.doit(noview=True)
        res = runjob.wait()
        temps = []
        found = False
        for a in (".pdf", ):
            for d in ('', '..'):
                for x in self.tempFiles:
                    f = os.path.join(os.path.dirname(x), d, os.path.basename(x).replace(".xdv", a))
                    if not found and os.path.exists(f):
                        temps.append(f)
                        break
        for f in set(self.tempFiles + runjob.picfiles + temps):
            pf = os.path.join(self.working_dir, f)
            if os.path.exists(pf):
                outfname = os.path.relpath(pf, self.settings_dir)
                zf.write(pf, outfname)
        ptxmacrospath = self.scriptsdir
        for dp, d, fs in os.walk(ptxmacrospath):
            for f in fs:
                if f[-4:].lower() in ('.tex', '.sty', '.tec') and f != "usfm.sty":
                    zf.write(os.path.join(dp, f), self.prjid+"/src/"+os.path.join(os.path.relpath(dp, ptxmacrospath), f))
        self._archiveSupportAdd(zf, [x for x in self.tempFiles if x.endswith(".tex")])
        zf.close()
        if res:
            self.doError(_("Warning: The print job failed, and so the archive is incomplete"))
        self.finished()
        
    def _archiveAdd(self, zf, books, parent=None):
        prjid = self.prjid
        cfgid = self.configName()
        entries, cfgchanges, tmpfiles = self._getArchiveFiles(books, prjid=prjid, cfgid=cfgid)
        for k, v in entries.items():
            if os.path.exists(k):
                if parent is not None and 'shared/fonts' in v:
                    zf.write(k, arcname=parent + "/" + v)
                zf.write(k, arcname=prjid + "/" + v)
        tmpcfg = {}
        for k,v in cfgchanges.items():
            if len(v) == 2 and v[1] is not None:
                tv = getattr(self, v[1])
                setattr(self, v[1], v[0])
            else:
                tv = None
            tmpcfg[k] = (self.get(k), tv)
            self.set(k, str(v if len(v) != 2 else v[0]))
        config = self.createConfig()
        configstr = StringIO()
        config.write(configstr)
        zf.writestr(prjid + "/shared/ptxprint/" + (cfgid + "/" if cfgid else "") + "ptxprint.cfg",
                    configstr.getvalue())
        configstr.close()
        for k, v in tmpcfg.items():
            self.set(k, str(v[0]))
            if v[1] is not None:
                setattr(self, cfgchanges[k][1], v[1])
        for f in tmpfiles:
            os.unlink(f)

    def _archiveSupportAdd(self, zf, texfiles):
        addfonts = ['SourceCodePro-Regular.ttf']
        for a in addfonts:
            fpath = getfontcache().get('Source Code Pro')
            if fpath is None:
                continue
            zf.write(fpath, arcname="{}/shared/fonts/{}".format(self.prjid, os.path.basename(fpath)))

        # create a fontconfig
        zf.writestr("{}/fonts.conf".format(self.prjid), writefontsconf(archivedir=True))
        scriptlines = ["#!/bin/sh", "cd local/ptxprint/{}".format(self.configName())]
        for t in texfiles:
            if t.endswith("_FRT.tex"):
                continue
            scriptlines.append("hyph_size=32749 stack_size=32768 FONTCONFIG_FILE=`pwd`/../../../fonts.conf TEXINPUTS=../../../src:. xetex {}".format(os.path.basename(t)))
        zinfo = ZipInfo("{}/runtex.sh".format(self.prjid))
        zinfo.external_attr = 0o755 << 16
        zinfo.create_system = 3
        zf.writestr(zinfo, "\n".join(scriptlines))
        batfile = r"""@echo off
REM To run this batch script (in Windows) change the extension 
REM from .txt to .bat and then type: runtex.bat <Enter>
cd local\\ptxprint\\{0}
for %%i in (xetex.exe) do set truetex=%%~$PATH:i
if "%truetex%" == "" set truetex=C:\\Program Files\\PTXprint\\xetex\\bin\\xetex.exe
set FONTCONFIG_FILE=%cd%\\..\\..\\..\\fonts.conf
set TEXINPUTS=.;%cd%\\..\\..\\..\\src\\;
set hyph_size=32749
set stack_size=32768""".format(self.configName())
        for t in texfiles:
            if t.endswith("_FRT.tex"):
                continue
            batfile += '\nif exist "%truetex%" "%truetex%" {}\ncd ..\..\..'.format(os.path.basename(t))
        zf.writestr("{}/runtex.txt".format(self.prjid), batfile)

    def createSettingsZip(self, outf):
        res = ZipFile(outf, "w", compression=ZIP_DEFLATED)
        sdir = self.configPath(self.configName())
        for d in (None, 'AdjLists'):
            ind = sdir if d is None else os.path.join(sdir, d)
            if not os.path.exists(ind):
                continue
            for f in os.listdir(ind):
                fpath = os.path.realpath(os.path.join(ind, f))
                if os.path.isfile(fpath):
                    res.write(fpath, f if d is None else os.path.join(d, f))
        return res

    def updateThumbLines(self):
        munits = float(self.get("s_margins"))
        unitConv = {'mm':1, 'cm':10, 'in':25.4, '"':25.4}
        m = re.match(r"^.*?[,xX]\s*([\d.]+)(\S+)\s*(?:.*|$)", self.get("ecb_pagesize"))
        if m:
            pageheight = float(m.group(1)) * unitConv.get(m.group(2), 1)
        else:
            pageheight = 210
        tfactor = float(self.get("s_topmargin"))
        bfactor = float(self.get("s_bottommargin"))
        tabsheight = pageheight - tfactor - bfactor   # in mm
        tabsheight -= 20 * 25.4 / 72.27                          # from default \TabsStart + \TabsEnd (in pt)
        if self.get("c_thumbrotate"):
            tabheight = float(self.get("s_thumblength") or 10)
        else:
            tabheight = float(self.get("s_thumbheight") or 4)
        newnum = int(tabsheight / tabheight)
        self.set("s_thumbtabs", newnum)

    def generateStrongs(self, bkid="XXA", cols=2):
        outfile = os.path.join(self.settings_dir, self.prjid, self.getBookFilename(bkid))
        onlylocal = self.get("c_strongsLocal")
        localfile = os.path.join(self.settings_dir, self.prjid, "TermRenderings.xml")
        if not os.path.exists(localfile):
            localfile = None
        generateStrongsIndex(bkid, cols, outfile, localfile, onlylocal, self._getPtSettings(), self)
