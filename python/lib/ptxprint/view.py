
import configparser, os, re, regex, random, collections
from ptxprint.texmodel import ModelMap, TexModel
from ptxprint.ptsettings import ParatextSettings, allbooks, books, bookcodes, chaps
from ptxprint.font import TTFont, cachepath, cacheremovepath, FontRef
from ptxprint.utils import _, refKey, universalopen, print_traceback, local2globalhdr, global2localhdr, asfloat
from ptxprint.usfmutils import Sheets, UsfmCollection
from ptxprint.piclist import PicInfo
from ptxprint.styleditor import StyleEditor
import pathlib, os, sys
from configparser import NoSectionError, NoOptionError, _UNSET
from tempfile import NamedTemporaryFile
from zipfile import ZipFile, ZIP_DEFLATED
from io import StringIO
from shutil import rmtree
import datetime, time
import json
from shutil import copyfile, copytree, move

VersionStr = "1.5.14"

pdfre = re.compile(r".+[\\/](.+)\.pdf")

varpaths = (
    ('prjdir', ('settings_dir', 'prjid')),
    ('settingsdir', ('settings_dir',)),
    ('workingdir', ('working_dir',)),
)

FontModelMap = {
    "fontregular": ("bl_fontR", None),
    "fontbold":    ("bl_fontB", None),
    "fontitalic":  ("bl_fontI", None),
    "fontbolditalic": ("bl_fontBI", None),
    "fontextraregular": ("bl_fontExtraR", None)
}

class Path(pathlib.Path):

    _flavour = pathlib._windows_flavour if os.name == "nt" else pathlib._posix_flavour

    @staticmethod
    def create_varlib(aView):
        res = {}
        for k, v in varpaths:
            res[k] = pathlib.Path(*[getattr(aView, x) for x in v])
        res['pdfassets'] = pathlib.Path(os.path.abspath(os.path.dirname(__file__)), 'PDFassets')
        return res

    def __new__(cls, txt, view=None):
        if view is None or not txt.startswith("${"):
            return pathlib.Path.__new__(cls, txt)
        varlib = cls.create_varlib(view)
        k = txt[2:txt.find("}")]
        return pathlib.Path.__new__(cls, varlib[k], txt[len(k)+4:])

    def withvars(self, aView):
        varlib = self.create_varlib(aView)
        bestl = len(str(self))
        bestk = None
        for k, v in varlib.items():
            try:
                rpath = self.relative_to(v)
            except ValueError:
                continue
            if len(str(rpath)) < bestl:
                bestk = k
        if bestk is not None:
            return "${"+bestk+"}/"+rpath.as_posix()
        else:
            return self.as_posix()

posparms = ["alt", "src", "size", "pgpos", "copy", "caption", "ref", "x-xetex", "mirror", "scale"]
pos3parms = ["src", "size", "pgpos", "ref", "copy", "alt", "x-xetex", "mirror", "scale"]

def doError(txt, secondary=None, title=None):
    print(txt)
    if secondary is not None:
        print(secondary)

class ViewModel:
    _attributes = {
        # modelname: (attribute, isMultiple, label)
        "project/frontincludes":    ("FrontPDFs", True, "lb_inclFrontMatter"),
        "project/backincludes":     ("BackPDFs", True, "lb_inclBackMatter"),
        "project/selectscript":     ("customScript", False, None),
        "project/modulefile":       ("moduleFile", False, "lb_bibleModule"),
        "paper/watermarkpdf":       ("watermarks", False, "lb_applyWatermark"),
        "fancy/pageborderpdf":      ("pageborder", False, "lb_inclPageBorder"),
        "fancy/sectionheaderpdf":   ("sectionheader", False, "lb_inclSectionHeader"),
        "fancy/endofbookpdf":       ("endofbook", False, "lb_inclEndOfBook"),
        "fancy/versedecoratorpdf":  ("versedecorator", False, "lb_inclVerseDecorator"),
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
        self.fixed_wd = workingdir != None
        self.working_dir = workingdir           # . or ~/Paratext8Projects/<prj>/PrintDraft
        self.userconfig = userconfig
        self.scriptsdir = scriptsdir
        self.args = args
        self.ptsettings = None
        self.FrontPDFs = None
        self.BackPDFs = None
        self.customScript = None
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
        self.isDisplay = False
        self.tempFiles = []
        self.usfms = None
        self.picinfos = None
        self.loadingConfig = False
        self.styleEditor = StyleEditor(self)
        self.triggervcs = False
        self.copyrightInfo = {}

        # private to this implementation
        self.dict = {}
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

    def doError(self, txt, secondary=None, title=None):
        print(txt)
        if secondary is not None:
            print(secondary)

    def msgQuestion(self, q1, q2):
        print("Answering \"no\" to: " + q1)
        print(q2)
        return False

    def resetToInitValues(self):
        pass

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
            self.dict[wid] = "{:.3f}".format(float(value))
        else:
            self.dict[wid] = value

    def baseTeXPDFnames(self, bks=None, force_combine=False):
        if bks is None:
            bks = self.getBooks(files=True)
        if self.working_dir == None:
            self.working_dir = os.path.join(self.settings_dir, self.prjid, 'PrintDraft')
        cfgname = self.configName()
        if cfgname is None:
            cfgname = ""
        else:
            cfgname = "-" + cfgname
        if len(bks) > 1:
            if force_combine or self.get("c_combine"):
                fname = "ptxprint{}-{}_{}{}".format(cfgname, bks[0], bks[-1], self.prjid)
            else:
                return sum((self.baseTeXPDFnames(bks=[bk]) for bk in bks), [])
        elif "." in bks[0]:
            fname = "ptxprint{}-{}{}".format(cfgname, os.path.splitext(os.path.basename(bks[0]))[0], self.prjid)
        else:
            fname = "ptxprint{}-{}{}".format(cfgname, bks[0], self.prjid)
        return [fname]
        
    def getBooks(self, scope=None, files=False):
        bl = self.get("t_booklist", "").split()
        if scope is None:
            scope = self.get("r_book")
        if scope == "single":
            return [self.get("ecb_book")]
        elif scope == "multiple" and len(bl):
            blst = []
            for b in bl:
                bname = self.getBookFilename(b, self.prjid)
                if os.path.exists(os.path.join(self.settings_dir, self.prjid, bname)):
                    blst.append(b)
            return blst
        elif scope == "module":
            if self.moduleFile is None:
                return []
            res = self.moduleFile.as_posix()
            # res = self.get("btn_chooseBibleModule")
            return [res] if files and res else []
        else:
            # return self.booklist
            return []

    def getAllBooks(self):
        ''' Returns a dict of all books in the project bkid: bookfile_path '''
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
        if any(x in "./\\" for x in bk):
            return None
        ptsettings = self._getPtSettings(prjid)
        fbkfm = ptsettings['FileNameBookNameForm']
        bknamefmt = (ptsettings['FileNamePrePart'] or "") + \
                    fbkfm.replace("MAT","{bkid}").replace("41","{bkcode}") + \
                    (ptsettings['FileNamePostPart'] or "")
        fname = bknamefmt.format(bkid=bk, bkcode=bookcodes.get(bk, 0))
        return fname

    def setFont(self, btn, name, style):
        self.dict[btn+"/name"] = name
        self.dict[btn+"/style"] = style

    def onFontChanged(self, fbtn):
        font_info = self.get("bl_fontR")
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

    def onNumTabsChanged(self, *a):
        if self.loadingConfig:
            return False
        (marginmms, topmarginmms, bottommarginmms, headerpos, footerpos, rulerpos, headerlabel, footerlabel) = self.getMargins()
        self.set("l_margin2header1", "{:.3f}mm".format(headerlabel))
        # self.set("l_margin2footer", "{:.1f}pt".format(footerlabel))
        return True

    def getMargins(self):
        def asmm(v): return v * 25.4 / 72.27
        hfont = self.styleEditor.getval("h", " font")
        if hfont is None:
            hf = self.get("bl_fontR")
            if hf is not None:
                hfont = hf.getTtfont()
            else:
                return (0, 0, 0, 0, 0, 0, 0, 0)
        #fontheight = 1. + float(font.descent) / font.upem
        hfontheight = float(hfont.ascent) / hfont.upem
        fontsizemms = asmm(float(self.get("s_fontsize")))
        linespacemms = asmm(float(self.get("s_linespacing")))
        hfontsizemms = asfloat(self.styleEditor.getval("h", "FontSize"), 12.) / 12. * fontsizemms
        marginmms = float(self.get("s_margins"))
        # in the macros, topmargin is set to topmargin - baselineskip + 12*FontSizeUnit
        # Reverse that here, so that what appears on the page is what they ask for.
        topmarginmms = float(self.get("s_topmargin")) + linespacemms - fontsizemms
        bottommarginmms = float(self.get("s_bottommargin"))
        # specified topmargin subtract 0.7 * hfontsize which the macros add in
        headerposmms = float(self.get("s_topmargin")) - asmm(float(self.get("s_headerposition"))) - 0.7 * hfontsizemms
        footerposmms = float(self.get("s_footerposition"))
        headerlabel = headerposmms - hfontheight * hfontsizemms
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

    def setPrjid(self, prjid, saveCurrConfig=False):
        return self.updateProjectSettings(prjid, configName="Default", saveCurrConfig=saveCurrConfig)

    def setConfigId(self, configid, saveCurrConfig=False, force=False):
        return self.updateProjectSettings(self.prjid, saveCurrConfig=saveCurrConfig, configName=configid, forceConfig=force)

    def _copyConfig(self, oldcfg, newcfg, moving=False):
        oldp = self.configPath(cfgname=oldcfg, makePath=False)
        newp = self.configPath(cfgname=newcfg, makePath=False)
        if not os.path.exists(newp):
            self.triggervcs = True
            os.makedirs(newp)
            jobs = {k:k for k in('ptxprint-mods.sty', 'ptxprint.sty', 'ptxprint-mods.tex',
                                 'ptxprint.cfg', 'PicLists', 'AdjLists')}
            jobs["{}-{}.piclist".format(self.prjid, oldcfg)] = "{}-{}.piclist".format(self.prjid, newcfg)
            for f, n in jobs.items():
                srcp = os.path.join(oldp, f)
                destp = os.path.join(newp, n)
                if os.path.exists(srcp):
                    if moving:
                        move(srcp, destp)
                    elif os.path.isdir(srcp):
                        os.makedirs(destp, exist_ok=True)
                        for p in os.listdir(srcp):
                            op = re.sub(r"-[^-]+\.", "-"+newcfg+".", p)
                            copyfile(os.path.join(srcp, p), os.path.join(destp, op))
                    else:
                        copyfile(srcp, destp)

    def updateProjectSettings(self, prjid, saveCurrConfig=False, configName=None, forceConfig=False, readConfig=False):
        currprj = self.prjid
        currcfg = self.configId
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
            if not self.fixed_wd:
                self.working_dir = os.path.join(self.settings_dir, self.prjid, 'PrintDraft')
            fdir = os.path.join(self.settings_dir, self.prjid, 'shared', 'fonts')
            if os.path.exists(fdir):
                cachepath(fdir)
            readConfig = True
        if readConfig or self.configId != configName:
            self.resetToInitValues()
            if configName == "Default":
                self._copyConfig(None, configName, moving=True)
            if currprj != self.prjid:
                self._copyConfig("Default", configName)
            else:
                self._copyConfig(self.configId, configName)
            res = self.readConfig(cfgname=configName)
            self.styleEditor.load(self.getStyleSheets(configName))
            if res or forceConfig:
                self.configId = configName
            if readConfig:  # project changed
                self.onNumTabsChanged()
                self.usfms = None
                self.get_usfms()
            self.readCopyrights()
            self.loadPics()
            return res
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
            return _("PTXprint {} - Bible Layout for Everyone!     Start by selecting a project to work with...").format(VersionStr)
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
            return "PTXprint {}   -  {} ({}) {}".format(VersionStr, prjid, bks, self.get("ecb_savedConfig") or "")

    def readCopyrights(self):
        with open(os.path.join(os.path.dirname(__file__), "picCopyrights.json"), encoding="utf-8", errors="ignore") as inf:
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
            return False
        config = configparser.ConfigParser()
        with open(path, encoding="utf-8", errors="ignore") as inf:
            config.read_file(inf)
        self.versionFwdConfig(config, cfgname)
        self.loadingConfig = True
        self.localiseConfig(config)
        self.loadConfig(config)
        if self.get("ecb_book") == "":
            self.set("ecb_book", list(self.getAllBooks().keys())[0])
        if self.get("c_diglot"):
            self.diglotView = self.createDiglotView()
        else:
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
        return True

    def writeConfig(self, cfgname=None):
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

    def _configset(self, config, key, value):
        if "/" in key:
            (sect, k) = key.split("/", maxsplit=1)
        else:
            (sect, k) = (key, "")
        if not config.has_section(sect):
            config.add_section(sect)
        if isinstance(value, bool):
            value = "true" if value else "false"
        config.set(sect, k, value)

    def createConfig(self):
        def sortkeys(x):
            k, v = x
            if k in self._activekeys:
                return (0, k, v)
            else:
                return (1, k, v)
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
            self._configset(config, k, str(val) if val is not None else "")
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
        version = self._config_get(config, "config", "version", conv=float, fallback=0.0)
        v = float(version)
        if v < 0.9:
            try:
                self._configset(config, "document/ifshowchapternums", not config.getboolean("document", "ifomitchapternum"))
                self._configset(config, "document/ifshowversenums", not config.getboolean("document", "ifomitallverses"))
                self._configset(config, "document/bookintro", not config.getboolean("document", "supressbookintro"))
                self._configset(config, "document/introoutline", not config.getboolean("document", "supressintrooutline"))
                self._configset(config, "document/firstparaindent", not config.getboolean("document", "supressindent"))
                self._configset(config, "document/sectionheads", not config.getboolean("document", "supresssectheads"))
                self._configset(config, "document/parallelrefs", not config.getboolean("document", "supressparallels"))
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
                    config.set("document", "indentunit", "1.000")
        if v < 1.403:   # no need to bump version for this and merge this with a later version test
            f = os.path.join(self.configPath(cfgname), "NestedStyles.sty")
            if os.path.exists(f):
                os.remove(f)
            config.set("paragraph", "linespacebase", "True")
        if v < 1.404:
            config.set("fancy", "versedecoratorshift", "-5")
        if v < 1.502:
            if not config.has_option("document", "includimg"):
                config.set("document", "includeimg", config.get("snippets", "imgcredits", fallback="false"))
            colophontext = config.get("project", "colophontext", fallback="").replace("zCopyright", "zcopyright")\
                            .replace("zImageCopyrights", "zimagecopyrights").replace("zLicense", "zlicense")
            config.set("project", "colophontext", colophontext)
        if v < 1.503:
            marginmms = config.getfloat("paper", "margins")
            config.set("paper", "topmargin", "{:.3f}".format(config.getfloat("paper", "topmarginfactor") * marginmms))
            config.set("paper", "headerpos", "{:.3f}".format(config.getfloat("paper", "topmarginfactor") * marginmms \
                        - config.getfloat("header", "headerposition") * marginmms\
                        - config.getfloat("paper", "fontfactor") * 25.4 / 72.27))
            config.set("paper", "bottommargin", "{:.3f}".format(config.getfloat("paper", "bottommarginfactor") * marginmms))
            config.set("paper", "footerpos", "{:.3f}".format(config.getfloat("header", "footerposition") * marginmms))
            config.set("paper", "rulegap", "{:.3f}".format(config.getfloat("header", "ruleposition")))
        if v < 1.504:
            try:
                self._configset(config, "notes/fneachnewline", not config.getboolean("notes", "fnparagraphednotes"))
                self._configset(config, "notes/xreachnewline", not config.getboolean("notes", "xrparagraphednotes"))
            except:
                pass
        if v < 1.505:
            config.set("paragraph", "useglyphmetrics", "True")
            config.set("config", "version", "1.505")

        styf = os.path.join(self.configPath(cfgname), "ptxprint.sty")
        if not os.path.exists(styf):
            with open(styf, "w", encoding="utf-8") as outf:
                outf.write("# This file left intentionally blank\n")

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

    def loadConfig(self, config):
        def setv(k, v): self.set(k, v, skipmissing=True)
        for sect in config.sections():
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
                                setv(w[2], ",".join(pdfre.sub(r"\1", x.as_posix()) for x in val))
                        else:
                            val = Path(val, self) if val is not None else None
                            if w[2] is not None and val is not None:
                                setv(w[2], pdfre.sub(r"\1", val.as_posix()))
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
        if self.get("c_thumbtabs"):
            self.updateThumbLines()

    def editFile_delayed(self, *a):
        pass

    def saveStyles(self, force=False):
        if not force and self.configLocked():
            return
        fname = os.path.join(self.configPath(self.configName(), makePath=True), "ptxprint.sty")
        regularfont = self.get("bl_fontR")
        root = os.path.join(self.settings_dir, self.prjid, "PrintDraft")
        with open(fname, "w", encoding="Utf-8") as outf:
            self.styleEditor.output_diffile(outf, regular=regularfont, root=root)

    def savePics(self, force=False):
        if not force and self.configLocked():
            return
        if self.picinfos is not None and self.picinfos.loaded:
            self.picinfos.out(os.path.join(self.configPath(self.configName()),
                                    "{}-{}.piclist".format(self.prjid, self.configName())))

    def loadPics(self):
        if self.loadingConfig:
            return
        if self.picinfos is None:
            self.picinfos = PicInfo(self)
        else:
            self.savePics()
            self.picinfos.clear(self)
        if not self.get("c_includeillustrations"):
            return
        if self.diglotView is None:
            self.picinfos.load_files()
        else:
            self.picinfos.load_files(suffix="L")
            self.picinfos.load_files(suffix="R", prjdir=os.path.join(self.settings_dir, self.diglotView.prjid),
                                     prj=self.diglotView.prjid, cfg=self.diglotView.configName())

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

    def generateAdjList(self):
        existingFilelist = []
        booklist = self.getBooks()
        diglot  = self.get("c_diglot")
        prjid = self.get("fcb_project")
        secprjid = ""
        if diglot:
            secprjid = self.get("fcb_diglotSecProject")
            if secprjid is not None:
                secprjdir = os.path.join(self.settings_dir, secprjid)
            else:
                self.doError(_("No Secondary Project Set"), secondary=_("In order to generate an AdjList for Diglots, the \n"+
                                                                    "Secondary project must be set on the Diglot+Border tab."))
                return
        prjdir = os.path.join(self.settings_dir, self.prjid)
        for bk in booklist:
            fname = self.getDraftFilename(bk, ext=".adj")
            outfname = os.path.join(self.configPath(self.configName()), "AdjLists", fname)
            if os.path.exists(outfname):
                existingFilelist.append(re.split(r"\\|/",outfname)[-1])
        if len(existingFilelist):
            q1 = _("One or more Paragraph Adjust file(s) already exist!")
            q2 = "\n".join(existingFilelist)+_("\n\nDo you want to OVERWRITE the above-listed file(s)?")
            if not self.msgQuestion(q1, q2):
                return
        for bk in booklist:
            tmplist = []
            fname = self.getBookFilename(bk)
            outfname = os.path.join(self.configPath(self.configName()),
                                    "AdjLists", self.getDraftFilename(bk, ext=".adj"))
            adjlist = []
            flist = [os.path.join(prjdir, fname)]
            if diglot: 
                secfname = self.getBookFilename(bk, secprjid)
                flist += [os.path.join(secprjdir, secfname)]
            if len(flist) == 2:
                sfx = 'L'
            else:
                sfx = ""
            for infname in flist:
                if len(flist) == 2 and infname == flist[1]:
                    sfx = 'R'
                with open(infname, "r", encoding="utf-8") as inf:
                    dat = inf.read()
                    # It would be good to make this more inclusive (\p \m \q1 \q2 etc.) 
                    # and also include \s Section Heads as comments to help show whichs paragraphs are within a single section
                    m = re.findall(r"\\p ?\r?\n\\v (\S+)",dat)
                    if m is not None:
                        prv = 0
                        ch = 1
                        for v in m:
                            iv = int(re.sub(r"^(\d+).*?$", r"\1", v), 10)
                            if iv < prv:
                                ch = ch + 1
                            srtchvs = "{:0>3}{:0>3}{}".format(ch,v,sfx)
                            tmplist.append(srtchvs+"\u0009"+bk+sfx+" "+str(ch)+"."+v+" +0")
                            prv = iv
            if len(tmplist):
                for al in sorted(tmplist):
                    adjlist.append(al.split("\u0009")[1]+"\n")
            adjpath = os.path.join(self.configPath(self.configName()), "AdjLists")
            os.makedirs(adjpath, exist_ok=True)
            with open(outfname, "w", encoding="utf-8") as outf:
                outf.write("".join(adjlist))

    def generateHyphenationFile(self):
        listlimit = 27836 # 32749
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
            z = 0
            with universalopen(infname) as inf:
                for l in inf.readlines()[8:]: # Skip over the Paratext header lines
                    l = l.strip().replace(u"\uFEFF", "")
                    l = re.sub(r"\*", "", l)
                    l = re.sub(r"-", "\u2010", l)
                    l = re.sub(r"=", "-", l)
                    # Paratext doesn't seem to allow segments of 1 character to be hyphenated  (for example: a-shame-d) 
                    # (so there's nothing to filter them out, because they don't seem to exist!)
                    if "-" in l:
                        if "\u200C" in l or "\u200D" in l or "'" in l: # Temporary workaround until we can figure out how
                            z += 1                                     # to allow ZWNJ and ZWJ to be included as letters.
                        elif re.search(r'\d', l):
                            pass
                        else:
                            if l[0] != "-":
                                hyphenatedWords.append(l)
            c = len(hyphenatedWords)
            if c >= listlimit:
                hyphwords = set([x.replace("-", "") for x in hyphenatedWords])
                sheets = usfmutils.load_stylesheets(self.getStyleSheets())
                acc = {}
                for bk in self.getBooks():
                    f = os.path.join(self.prjdir, self.getBookFilename(bk, self.prjdir))
                    u = usfmutils.Usfm(f, stylesheets=sheets)
                    u.getwords(init=acc, constrain=hyphwords)
                if len(acc) >= listlimit:
                    shortlist = [k for k, v in sorted(acc.items(), key=lambda x:(-x[1], -len(x[0])))][:listlimit]
                else:
                    shortlist = sorted(acc.keys())
                m2b = "\n\nThat is too many for XeTeX! List truncated to longest {} words found in the active sources.".format(len(shortlist))
                hyphenatedWords = shortlist
            hyphenatedWords.sort(key = lambda s: s.casefold())
            outlist = '\\catcode"200C=11\n\\catcode"200D=11\n\\hyphenation{' + "\n".join(hyphenatedWords) + "}"
            with open(outfname, "w", encoding="utf-8") as outf:
                outf.write(outlist)
            if len(hyphenatedWords) > 1:
                m1 = _("Hyphenation List Generated")
                m2a = _("{} hyphenated words were gathered\nfrom Paratext's Hyphenation Word List.").format(c)
                if z > 0:
                    m2c = _("\n\nNote for Indic languages that {} words containing ZWJ").format(z) + \
                            _("\nand ZWNJ characters have been left off the hyphenation list.")
                m2 = m2a + m2b + m2c
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
        if self.get("fcb_glossaryMarkupStyle") == "with ⸤floor⸥ brackets":
            allchars += "\u2e24\u2e25"
        if self.get("fcb_glossaryMarkupStyle") == "with ⌊floor⌋ characters":
            allchars += "\u230a\u230b"
        if self.get("fcb_glossaryMarkupStyle") == "with ⌞corner⌟ characters":
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

    def getStyleSheets(self, cfgname=None, generated=False):
        if self.prjid is None:
            return []
        res = []
        if cfgname is None:
            cfgname = self.configName()
        cpath = self.configPath(cfgname=cfgname, makePath=False)
        rcpath = self.configPath("", makePath=False)
        res.append(os.path.join(self.scriptsdir, "ptx2pdf.sty"))
        if self.get('c_useCustomSty'):
            res.append(os.path.join(self.settings_dir, self.prjid, "custom.sty"))
        if self.get('c_useModsSty'):
            for p in (cpath, rcpath):
                fp = os.path.join(p, "ptxprint-mods.sty")
                if os.path.exists(fp):
                    res.append(fp)
                    break
        res.append(os.path.join(cpath, "ptxprint.sty"))
        return res

    def _getArchiveFiles(self, books, includeTemps, prjid=None, cfgid=None):
        sfiles = {'c_useCustomSty': ("custom.sty", False),
                  'c_useModsSty': ("ptxprint-mods.sty", True),
                  'c_useModsTex': ("ptxprint-mods.tex", True),
                  'c_usePrintDraftChanges': ("PrintDraftChanges.txt", False),
                  None: ("picChecks.txt", False)}
        borders = {'c_inclPageBorder': 'pageborder',
                   'c_inclSectionHeader': 'sectionheader',
                   'c_inclEndOfBook': 'endofbook',
                   'c_inclVerseDecorator': 'versedecorator'}
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
        for bk in books:
            fname = self.getBookFilename(bk, prjid)
            if fname is None:
                scope = self.get("r_books")
                if scope == "module":
                    res[os.path.join(fpath, bk)] = os.path.basename(bk)
                    cfgchanges['btn_chooseBibleModule'] = os.path.basename(fname)
            else:
                res[os.path.join(fpath, fname)] = os.path.basename(fname)
            if interlang is not None:
                intpath = "Interlinear_{}".format(interlang)
                intfile = "{}_{}.xml".format(intpath, bk)
                res[os.path.join(fpath, intpath, intfile)] = os.path.join(intpath, intfile)
        self.picinfos.getFigureSources(exclusive=self.get("c_exclusiveFiguresFolder"))
        pathkey = 'src path'
        for f in (p[pathkey] for p in self.picinfos.values() if pathkey in p):
                res[f] = "figures/"+os.path.basename(f)

        # adjlists
        adjpath = os.path.join(basecfpath, "AdjLists")
        adjbks = set(self.getDraftFilename(bk, ext=".adj") for x in books)
        if os.path.exists(adjpath):
            for adj in os.listdir(adjpath):
                if adj.endswith(".adj") and adj in adjbks:
                    res[os.path.join(adjpath, adj)] = cfpath+"AdjLists/"+adj

        # piclists
        piclstpath = os.path.join(basecfpath, "PicLists")
        picbks = set(self.getDraftFilename(bk) for x in books)
        if os.path.exists(piclstpath):
            for pic in os.listdir(piclstpath):
                if pic.endswith(".piclist") and pic in picbks:
                    res[os.path.join(piclstpath, pic)] = cfpath+"PicLists/"+pic
        jobpiclistfs = ["{}-{}.piclist".format(prjid, cfgid), "picChecks.txt"]
        if not includeTemps:
            jobpiclistfs += ["ptxprint.sty"]
        for jobpiclistf in jobpiclistfs:
            jobpiclist = os.path.join(basecfpath, jobpiclistf)
            if os.path.exists(jobpiclist):
                res[jobpiclist] = cfpath+jobpiclistf

        # borders
        if self.get('c_borders'):
            for k, v in borders.items():
                if self.get(k):
                    fname = getattr(self, v)
                    # print(k, v, fname)
                    if fname is None: continue
                    res[fname.as_posix()] = "shared/ptxprint/"+fname.name

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

        if includeTemps:
            regularfont = self.get("bl_fontR")
            tempfile = NamedTemporaryFile("w", encoding="utf-8", newline=None, delete=False)
            self.styleEditor.output_diffile(tempfile, regular=regularfont, inArchive=True)
            tempfile.close()
            res[tempfile.name] = cfpath+"ptxprint.sty"
            tmpfiles.append(tempfile.name)

        # config files
        for t, a in sfiles.items():
            if isinstance(t, str) and not self.get(t): continue
            if a[1]:
                s = os.path.join(basecfpath, a[0])
                d = cfpath + a[0]
            else:
                s = os.path.join(self.settings_dir, prjid, a[0])
                d = a[0]
            if os.path.exists(s):
                res[s] = d

        if self.get("c_useModsTex"):
            loaded = False
            if cfgid is not None:
                p = os.path.join(self.settings_dir, prjid, 'shared', 'ptxprint', cfgid, 'ptxprint-mods.tex')
                loaded = os.path.exists(p)
            if not loaded:
                p = os.path.join(self.settings_dir, prjid, 'shared', 'ptxprint', 'ptxprint-mods.tex')
                if os.path.exists(p):
                    res[p] = "shared/ptxprint/ptxprint-mods.tex"
        if interlang is not None:
            res[os.path.join(fpath, 'Lexicon.xml')] = 'Lexicon.xml' 

        script = self.get("btn_selectScript")
        if script is not None and len(script):
            res[script] = os.path.basename(script)
            cfgchanges["btn_selectScript"] = os.path.join(self.settings_dir, prjid, os.path.basename(script))

        hyphenfpath = os.path.join(self.settings_dir, prjid, "shared", "ptxprint")
        hyphentpath = "shared/ptxprint/"
        hyphenfile = "hyphen-{}.tex".format(self.prjid)
        if os.path.exists(os.path.join(hyphenfpath, hyphenfile)):
            res[os.path.join(hyphenfpath, hyphenfile)] = hyphentpath + hyphenfile

        pts = self._getPtSettings(prjid=prjid)
        ptres = pts.getArchiveFiles()
        res.update(ptres)
        return (res, cfgchanges, tmpfiles)

    def createDiglotView(self):
        prjid = self.get("fcb_diglotSecProject")
        cfgid = self.get("ecb_diglotSecConfig")
        if prjid is None or cfgid is None:
            return None
        digview = ViewModel(self.settings_dir, self.working_dir, self.userconfig, self.scriptsdir)
        digview.setPrjid(prjid)
        if cfgid is not None and cfgid != "":
            digview.setConfigId(cfgid)
        return digview

    def createArchive(self, filename=None):
        includeTemps = self.get("c_archiveTemps")
        if filename is None:
            filename = os.path.join(self.configPath(self.configName()), "ptxprintArchive.zip")
        if not filename.lower().endswith(".zip"):
            filename += ".zip"
        try:
            zf = ZipFile(filename, mode="w", compression=ZIP_DEFLATED)  # need at least python 3.7 for: compresslevel=9
        except OSError:
            self.doError(_("Error: Cannot create Archive!"), secondary=_("The ZIP file seems to open in another program."))
            return
        self._archiveAdd(zf, self.getBooks(files=True), includeTemps)
        if self.diglotView is not None:
            self.diglotView._archiveAdd(zf, self.getBooks(files=True), includeTemps)
        if includeTemps:
            from ptxprint.runjob import RunJob
            runjob = RunJob(self, self.scriptsdir, self.args, inArchive=True)
            runjob.doit()
            temps = [x.replace(".xdv", ".pdf") for x in self.tempFiles if x.endswith(".xdv")]
            for f in self.tempFiles + temps:
                pf = os.path.join(self.working_dir, f)
                if os.path.exists(pf):
                    outfname = os.path.relpath(pf, self.settings_dir)
                    zf.write(pf, outfname)
            ptxmacrospath = self.scriptsdir
            for f in os.listdir(ptxmacrospath):
                if f.endswith(".tex") or f.endswith(".sty"):
                    zf.write(os.path.join(ptxmacrospath, f), self.prjid+"/src/"+f)
            mappingfile = self.get("fcb_digits")
            if mappingfile is not None and mappingfile != "Default":
                mappingfile = mappingfile.lower()+"digits.tec"
                mpath = os.path.join(ptxmacrospath, "mappings", mappingfile)
                if os.path.exists(mpath):
                    zf.write(mpath, self.prjid+"/src/mappings/"+mappingfile)
        zf.close()

    def _archiveAdd(self, zf, books, includeTemps):
        prjid = self.prjid
        cfgid = self.configName()
        entries, cfgchanges, tmpfiles = self._getArchiveFiles(books, includeTemps, prjid=prjid, cfgid=cfgid)
        for k, v in entries.items():
            if os.path.exists(k):
                zf.write(k, arcname=prjid + "/" + v)
        tmpcfg = {}
        for k,v in cfgchanges.items():
            tmpcfg[k] = self.get(k)
            self.set(k, v)
        config = self.createConfig()
        configstr = StringIO()
        config.write(configstr)
        zf.writestr(prjid + "/shared/ptxprint/" + (cfgid + "/" if cfgid else "") + "ptxprint.cfg",
                    configstr.getvalue())
        configstr.close()
        for k, v in tmpcfg.items():
            self.set(k, v)
        for f in tmpfiles:
            os.unlink(f)

    def updateThumbLines(self):
        munits = float(self.get("s_margins"))
        unitConv = {'mm':1, 'cm':10, 'in':25.4, '"':25.4}
        m = re.match(r"^.*?,\s*([\d.]+)(\S+)\s*(?:.*|$)", self.get("ecb_pagesize"))
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

