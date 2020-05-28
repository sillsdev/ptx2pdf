
import configparser, os, re
from .texmodel import ModelMap
from .ptsettings import ParatextSettings, allbooks, books, bookcodes, chaps
from .font import TTFont
from pathlib import Path

VersionStr = "0.7.0 beta"

pdfre = re.compile(r".+[\\/](.+)\.pdf")

class ViewModel:
    _attributes = {
        # modelname: (attribute, isMultiple, label)
        "project/frontincludes":    ("FrontPDFs", True, "lb_inclFrontMatter"),
        "project/backincludes":     ("BackPDFs", True, "lb_inclBackMatter"),
        "project/selectscript":     ("CustomScript", False, None),
        "paper/watermarkpdf":       ("watermarks", False, "lb_applyWatermark"),
        "fancy/pageborderpdf":      ("pageborder", False, "lb_inclPageBorder"),
        "fancy/sectionheaderpdf":   ("sectionheader", False, "lb_inclSectionHeader"),
        "fancy/versedecoratorpdf":  ("versedecorator", False, "lb_inclVerseDecorator"),
        "document/customfigfolder": ("customFigFolder", False, None)
    }
    _settingmappings = {
        "notes/xrcallers": "crossrefs",
        "notes/fncallers": "footnotes"
    }

    def __init__(self, allprojects, settings_dir, working_dir=None):
        self.settings_dir = settings_dir
        self.working_dir = working_dir
        self.config_dir = None
        self.ptsettings = None
        self.booklist = []
        self.CustomScript = None
        self.FrontPDFs = None
        self.BackPDFs = None
        self.watermarks = None
        self.pageborder = None
        self.sectionheader = None
        self.versedecorator = None
        self.customFigFolder = None
        self.prjid = None

        # private to this implementation
        self.dict = {}

    def doError(self, txt, secondary=None):
        print(txt)
        if secondary is not None:
            print(secondary)

    def msgQuestion(self, q1, q2):
        print("Answering \"no\" to: " + q1)
        print(q2)
        return False

    def parse_fontname(self, font):
        m = re.match(r"^(.*?)(\d+(?:\.\d+)?)$", font)
        if m:
            return [m.group(1), int(m.group(2))]
        else:
            return [font, 0]

    def get(self, wid, sub=0, asstr=False):
        if wid.startswith("bl_"):
            return (self.dict.get(wid + " name", None), self.dict.get(wid + " style", None))
        return self.dict.get(wid, None)

    def set(self, wid, value):
        if wid.startswith("bl_"):
            self.setFont(wid, *value)
        self.dict[wid] = value

    def configName(self):
        cfgName = re.sub('[^-a-zA-Z0-9_()/: ]+', '', self.get("ecb_savedConfig")).strip(" ")
        return cfgName

    def getBooks(self):
        bl = self.get("t_booklist").split()
        if not self.get('c_multiplebooks'):
            return [self.get("ecb_book")]
        elif len(bl):
            blst = []
            for b in bl:
                if os.path.exists(os.path.join(self.settings_dir, self.prjid, (self.getBookFilename(b, self.prjid)))):
                    blst.append(b)
            return blst
        else:
            # return self.booklist
            return []

    def getBookFilename(self, bk, prjid):
        if self.ptsettings is None:
            self.ptsettings = ParatextSettings(self.settings_dir, self.prjid)
        fbkfm = self.ptsettings['FileNameBookNameForm']
        bknamefmt = (self.ptsettings['FileNamePrePart'] or "") + \
                    fbkfm.replace("MAT","{bkid}").replace("41","{bkcode}") + \
                    (self.ptsettings['FileNamePostPart'] or "")
        fname = bknamefmt.format(bkid=bk, bkcode=bookcodes.get(bk, 0))
        return fname

    def setFont(self, btn, name, style):
        self.dict[btn+"/name"] = name
        self.dict[btm+"/style"] = style

    def onFontChanged(self, fbtn):
        font_info = self.get("bl_fontR")
        f = TTFont(*font_info)
        if "Silf" in f:
            self.set("c_useGraphite", True)
        else:
            self.set("c_useGraphite", False)
        silns = "{urn://www.sil.org/ldml/0.1}"
        d = self.ptsettings.find_ldml('.//special/{1}external-resources/{1}font[@name="{0}"]'.format(f.family, silns))
        if d is not None:
            featstring = d.get('features', '')
            self.set("t_fontfeatures", featstring)
        for s in ('Bold', 'Italic', 'Bold Italic'):
            sid = "".join(x[0] for x in s.split())
            esid = s.lower().replace(" ", "")
            w = "bl_font"+sid
            nf = TTFont(f.family, style = " ".join(s.split()))
            if nf.filename is None:
                styles = s.split()
                if len(styles) > 1:
                    bf = TTFont(f.family, style=styles[0])
                    if bf.filename is not None:
                        self.set("s_{}embolden".format(esid), 0)
                        styles.pop(0)
                    else:
                        bf = f
                else:
                    bf = f
                self.set(w, (bf.family, bf.style))
                self.set("c_fake"+esid, True)
                for t in styles:
                    if t == 'Bold':
                        self.set("s_{}embolden".format(esid), 2)
                    elif t == 'Italic':
                        self.set("s_{}slant".format(esid), 0.15)
            else:
                self.set(w, (nf.family, nf.style))
                self.set("c_fake"+esid, False)

    def updateSavedConfigList(self):
        pass

    def updateBookList(self):
        pass

    def updateProjectSettings(self, saveCurrConfig=False):
        currprj = self.prjid
        if currprj is not None and saveCurrConfig:
            self.writeConfig()
            self.updateSavedConfigList()
            self.set("t_savedConfig", "")
            self.set("t_configNotes", "")
        self.prjid = self.get("fcb_project")
        print("prjid=",self.prjid)
        self.ptsettings = None
        lsbooks = self.builder.get_object("ls_books")
        if self.prjid:
            self.ptsettings = ParatextSettings(self.settings_dir, self.prjid)
            self.updateBookList()
        if not self.prjid:
            return
        if self.get("c_useprintdraftfolder"):
            self.working_dir = os.path.join(self.settings_dir, self.prjid, 'PrintDraft')
        else:
            self.working_dir = '.'
        return self.readConfig()

    def getDialogTitle(self):
        prjid = "  -  " + self.get("fcb_project")
        if self.get('c_combine'):
            bks = self.get('t_booklist').split()
        else:
            bks = [self.get('t_book')]
        if len(bks) == 2:
            bks = bks[0] + "," + bks[1]
        elif len(bks) > 2:
            bks = bks[0] + "..." + bks[-1]
        else:
            try:
                bks = bks[0]
            except IndexError:
                bks = "No book selected!"
        return "PTXprint [{}] {} ({}) {}".format(VersionStr, prjid, bks, self.get("ecb_savedConfig") or "")

    def configPath(self, cfgname=None, makePath=False):
        if self.settings_dir is None or self.prjid is None:
            return None
        prjdir = os.path.join(self.settings_dir, self.prjid, "shared", "ptxprint")
        if cfgname is not None and len(cfgname):
            prjdir = os.path.join(prjdir, cfgname)
        if makePath:
            os.makedirs(prjdir,exist_ok=True)
        return prjdir

    def readConfig(self, cfgname=None):
        if cfgname is None:
            cfgname = self.configName()
        path = os.path.join(self.configPath(cfgname), "ptxprint.cfg")
        if not os.path.exists(path):
            return False
        config = configparser.ConfigParser()
        config.read(path, encoding="utf-8")
        self.loadConfig(None, config)
        return True

    def writeConfig(self, cfgname=None):
        if cfgname is None:
            cfgname = self.configName()
        path = os.path.join(self.configPath(cfgname=cfgname, makePath=True), "ptxprint.cfg")
        config = self.createConfig()
        with open(path, "w", encoding="utf-8") as outf:
            config.write(outf)

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
        config = configparser.ConfigParser()
        for k, v in ModelMap.items():
            if v[0] is None:
                continue
            if k in self._attributes:
                v = self._attributes[k]
                val = getattr(self, v[0])
                if val is None:
                    continue
                if v[1]:
                    val = "\n".join(x.as_posix() for x in val)
                else:
                    val = val.as_posix()
            elif v[0].startswith("bl_"):
                val = self.get(v[0])
                self._configset(config, k+"/name", val[0] or "")
                self._configset(config, k+"/style", val[1] or "")
                continue
            else:
                if v[0] is None:
                    continue
                val = self.get(v[0], asstr=True)
            if k in self._settingmappings:
                if val == "" or val == self.ptsettings.dict.get(self._settingmappings[k], ""):
                    continue
            self._configset(config, k, str(val))
        return config

    def loadConfig(self, printer, config):
        for sect in config.sections():
            for opt in config.options(sect):
                key = "{}/{}".format(sect, opt)
                val = config.get(sect, opt)
                if key in ModelMap:
                    v = ModelMap[key]
                    if key in self._attributes:
                        w = self._attributes[key]
                        if val == "None":
                            val = None
                        if w[1]:
                            val = val.split("\n") if val is not None else []
                            val = [Path(x) for x in val if x is not None]
                            if w[2] is not None:
                                self.set(w[2], ",".join(pdfre.sub(r"\1", x.as_posix()) for x in val))
                        else:
                            val = Path(val) if val is not None else None
                            if w[2] is not None and val is not None:
                                self.set(w[2], pdfre.sub(r"\1", val.as_posix()))
                        setattr(self, w[0], val)
                    else:
                        try: # Safeguarding from changed/missing keys in .cfg  or v[0].startswith("f_") 
                            if v[0].startswith("s_"):
                                val = float(val)
                            elif v[0].startswith("c_"):
                                val = config.getboolean(sect, opt)
                            if val is not None:
                                self.set(v[0], val)
                        except AttributeError:
                            pass # ignore missing keys 
                elif sect in ModelMap:
                    v = ModelMap[sect]
                    if v[0].startswith("bl_") and opt == "name":
                        vname = re.sub(r"\s*,?\s+\d+\s*$", "", val) # strip legacy style and size
                        vstyle = config.get(sect, "style", fallback="")
                        self.set(ModelMap[sect][0], (vname, vstyle))
        for k, v in self._settingmappings.items():
            (sect, name) = k.split("/")
            try:
                val = config.get(sect, name)
            except configparser.NoOptionError:
                self.set(ModelMap[k][0], self.ptsettings.dict.get(v, ""))

    def GeneratePicList(self, booklist):
        # Format of lines in pic-list file: BBB C.V desc|file|size|loc|copyright|caption|ref
        # MRK 1.16 fishermen...catching fish with a net.|hk00207b.png|span|b||Jesus calling the disciples to follow him.|1.16
        _picposn = {
            "col":      ("tl", "tr", "bl", "br"),
            "span":     ("t", "b")
        }
        existingFilelist = []
        prjid = self.get("fcb_project")
        prjdir = os.path.join(self.settings_dir, self.prjid)
        for bk in booklist:
            fname = self.getBookFilename(bk, prjid)
            outfname = os.path.join(self.configPath(), "PicLists", fname)
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:] + ".piclist"
            if os.path.exists(outfname):
                existingFilelist.append(outfname.split("/")[-1])
        if len(existingFilelist):
            q1 = "One or more PicList file(s) already exist!"
            q2 = "\n".join(existingFilelist)+"\n\nDo you want to OVERWRITE the above-listed file(s)?"
            if not self.msgQuestion(q1, q2):
                return
        for bk in booklist:
            fname = self.getBookFilename(bk, prjid)
            infname = os.path.join(prjdir, fname)
            outfname = os.path.join(self.configPath(), "PicLists", fname)
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:] + ".piclist"
            piclist = []
            piclist.append("% PicList Generated by PTXprint.\n")
            piclist.append("% Location   |Image Name|Img.Size|Position on Page||Illustration|Ref.\n")
            piclist.append("% book ch.vs |filename.ext|span/col|t/b/tl/tr/bl/br||Caption Text|ch:vs\n")
            piclist.append("%   (See end of list for more help for trouble-shooting)\n\n")
            with open(infname, "r", encoding="utf-8") as inf:
                dat = inf.read()
                # Finds USFM2-styled markup in text:
                #                0         1       2     3     4              5       
                # \\fig .*?\|(.+?\....)\|(....?)\|(.+)?\|(.+)?\|(.+)?\|(\d+[\:\.]\d+([\-,\u2013\u2014]\d+)?)\\fig\*
                # \fig |CN01684b.jpg|col|||key-kālk arsi manvan yēsunaga tarval|9:2\fig*
                #           0         1  2 3          4                          5  
                # BKN \5 \|\0\|\1\|tr\|\|\4\|\5
                # MAT 9.2 bringing the paralyzed man to Jesus|CN01684b.jpg|col|tr||key-kālk arsi manvan yēsunaga tarval|9:2
                m = re.findall(r"\\fig .*?\|(.+?\....)\|(....?)\|(.+)?\|(.+)?\|(.+)?\|(\d+[\:\.]\d+([\-,\u2013\u2014]\d+)?)\\fig\*", dat)
                if len(m):
                    for f in m:
                        picfname = f[0]
                        extn = picfname[-4:]
                        picfname = re.sub('[()&+,. ]', '_', picfname)[:-4]+extn
                        if self.get("c_randomPicPosn"):
                            pageposn = random.choice(_picposn.get(f[1], f[1]))    # Randomize location of illustrations on the page (tl,tr,bl,br)
                        else:
                            pageposn = (_picposn.get(f[1], f[1]))[0]              # use the t or tl (first in list)
                        piclist.append(bk+" "+re.sub(r":",".", f[5])+" |"+picfname+"|"+f[1]+"|"+pageposn+"||"+f[4]+"|"+f[5]+"\n")
                else:
                    # If none of the USFM2-styled illustrations were found then look for USFM3-styled markup in text 
                    # (Q: How to handle any additional/non-standard xyz="data" ? Will the .* before \\fig\* take care of it adequately?)
                    #         0              1               2                  3      [4]
                    # \\fig (.+?)\|src="(.+?\....)" size="(....?)" ref="(\d+[:.]\d+([-,\u2013\u2014]\d+)?)".*\\fig\*
                    # \fig hāgartun saṅga dūtal vaḍkval|src="CO00659B.TIF" size="span" ref="21:16"\fig*
                    #                   0                         1                2          3  [4]
                    # BKN \3 \|\1\|\2\|tr\|\|\0\|\3
                    # GEN 21.16 an angel speaking to Hagar|CO00659B.TIF|span|t||hāgartun saṅga dūtal vaḍkval|21:16
                    m = re.findall(r'\\fig (.*?)\|src="(.+?\....)" size="(....?)" ref="(\d+[:.]\d+([-,\u2013\u2014]\d+)?)".*\\fig\*', dat)
                    if len(m):
                        for f in m:
                            picfname = f[1]
                            extn = picfname[-4:]
                            picfname = re.sub('[()&+,. ]', '_', picfname)[:-4]+extn
                            if self.get("c_randomPicPosn"):
                                pageposn = random.choice(_picposn.get(f[2], f[2]))     # Randomize location of illustrations on the page (tl,tr,bl,br)
                            else:
                                pageposn = (_picposn.get(f[2], f[2]))[0]               # use the t or tl (first in list)
                            piclist.append(bk+" "+re.sub(r":",".", f[3])+" |"+picfname+"|"+f[2]+"|"+pageposn+"||"+f[0]+"|"+f[3]+"\n")
                if len(m):
                    piclist.append("\n% If illustrations are not appearing in the output PDF, check:\n")
                    piclist.append("%   a) The Location Reference on the left is very particular, so check\n")
                    piclist.append("%      (i) Only use '.' as the ch.vs separator\n")
                    piclist.append("%      (ii) Ensure there is a space after the verse and before the first |\n")
                    piclist.append("%      (iii) Verse Refs must match the text itself? e.g. Change MRK 4.2-11 to be MRK 4.2\n")
                    piclist.append("%   b) Does the illustration exist in 'Figures' or 'Local/Figures' or another specified folder?\n")
                    piclist.append("%   c) Position on Page for a 'span' image only allows 't'=top or 'b'=bottom\n")
                    piclist.append("% Other Notes:\n")
                    piclist.append("%   d) To (temporarily) remove an illustration prefix the line with % followed by a space\n")
                    piclist.append("%   e) To scale an image use this notation: span*.7  or  col*1.3)\n")
                    plpath = os.path.join(self.configPath(), "PicLists")
                    os.makedirs(plpath, exist_ok=True)
                    with open(outfname, "w", encoding="utf-8") as outf:
                        outf.write("".join(piclist))

    def GenerateAdjList(self):
        existingFilelist = []
        booklist = self.getBooks()
        prjid = self.get("fcb_project")
        prjdir = os.path.join(self.settings_dir, self.prjid)
        for bk in booklist:
            fname = self.getBookFilename(bk, prjid)
            outfname = os.path.join(self.configPath(), "AdjLists", fname)
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:] + ".adj"
            if os.path.exists(outfname):
                existingFilelist.append(outfname.split("/")[-1])
        if len(existingFilelist):
            q1 = "One or more Paragraph Adjust file(s) already exist!"
            q2 = "\n".join(existingFilelist)+"\n\nDo you want to OVERWRITE the above-listed file(s)?"
            if not self.msgQuestion(q1, q2):
                return
        for bk in booklist:
            fname = self.getBookFilename(bk, prjid)
            infname = os.path.join(prjdir, fname)
            outfname = os.path.join(self.configPath(), "AdjLists", fname)
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:] + ".adj"
            adjlist = []
            with open(infname, "r", encoding="utf-8") as inf:
                dat = inf.read()
                # It would be good to make this more inclusive (\p \m \q1 \q2 etc.) 
                # and also include \s Section Heads as comments to help show whichs paragraphs are within a single section
                m = re.findall(r"\\p ?\r?\n\\v (\S+)",dat)
                if m is not None:
                    prv = 0
                    ch = 1
                    for v in m:
                        iv = int(re.sub(r"^(\d+)", "\1", v))
                        if iv < prv:
                            ch = ch + 1
                        adjlist.append(bk+" "+str(ch)+"."+v+" +0\n")
                        prv = iv
                    adjpath = os.path.join(self.configPath(), "AdjLists")
                    os.makedirs(adjpath, exist_ok=True)
                    with open(outfname, "w", encoding="utf-8") as outf:
                        outf.write("".join(adjlist))

    def onDiglotSettingsChanged(self, btn):
        if not self.get("c_diglot"):
            DiglotStringL = ""
            DiglotStringR = ""
            return
        # MH: We need to decide whether we place the secPDF in its own folder 
        #(or whether we put it into the Pri Printdraft folder) - and fix the hardcoded 'PrintDraft" paths!
        secprjid = self.get("ecb_diglotSecProject")
        # I'm not sure if there's a better way to handle this - looking for the already-created Secondary diglot file
        sectmpdir = os.path.join(self.settings_dir, secprjid, 'PrintDraft') if self.get("c_useprintdraftfolder") else self.working_dir
        jobs = self.getBooks()
        if len(jobs) > 1:
            secfname = os.path.join(sectmpdir, "ptxprint-{}_{}{}.pdf".format(jobs[0], jobs[-1], secprjid)).replace("\\","/")
        else:
            secfname = os.path.join(sectmpdir, "ptxprint-{}{}.pdf".format(jobs[0], secprjid)).replace("\\","/")
        # TO DO: We need to be able to GET the page layout values from the PRIMARY project
        # (even when creating the Secondary PDF so that the dimensions match).
        PageWidth = int(re.split("[^0-9]",re.sub(r"^(.*?)\s*,.*$", r"\1", self.get("ecb_pagesize")))[0]) or 148
        
        Margins = self.get("s_margins")
        MiddleGutter = self.get("s_colgutterfactor")
        BindingGutter = self.get("s_pagegutter")
        priFraction = self.get("s_diglotPriFraction")
        PriColWid = PageWidth * priFraction / 100

        SecColWid = PageWidth - PriColWid - MiddleGutter - BindingGutter - (2 * Margins)

        # Calc Pri Settings (right side of page; or outer if mirrored)
        # PriColWid = self.get("s_PriColWidth")
        PriSideMarginFactor = 1
        PriBindingGutter = PageWidth - Margins - PriColWid - Margins

        # Calc Sec Settings (left side of page; or inner if mirrored)
        # SecColWid = PageWidth - PriColWid - MiddleGutter - BindingGutter - (2 * Margins)
        SecSideMarginFactor = (PriColWid + Margins + MiddleGutter) / Margins
        SecRightMargin = PriColWid + Margins + MiddleGutter
        
        SecBindingGutter = PageWidth - (2 * SecRightMargin) - SecColWid 

        PriPercent = round((PriColWid / (PriColWid + SecColWid) * 100),1)
        hdr = ""
        if self.get("c_diglotHeaders"):
            hdr = r"""
\def\RHoddleft{\rangeref}
\def\RHoddcenter{\empty}
\def\RHoddright{\empty}
\def\RHevenleft{\empty}
\def\RHevencenter{\empty}
\def\RHevenright{\rangeref}"""
        DiglotStringR = "%% SECONDARY PDF settings"+ \
                       "\n\MarginUnit={}mm".format(Margins)+ \
                       "\n\BindingGuttertrue"+ \
                       "\n\BindingGutter={:.2f}mm".format(SecBindingGutter)+ \
                       "\n\def\SideMarginFactor{{{:.2f}}}".format(SecSideMarginFactor)+ \
                       "\n\BodyColumns=1" + hdr
        if self.get("c_diglotHeaders"):
            hdr = r"""
\def\RHoddleft{\pagenumber}
\def\RHoddcenter{\empty}
\def\RHoddright{\rangeref}
\def\RHevenleft{\rangeref}
\def\RHevencenter{\empty}
\def\RHevenright{\pagenumber}"""
        DiglotStringL = "%% PRIMARY (+ SECONDARY) PDF settings"+ \
                       "\n\MarginUnit={}mm".format(Margins)+ \
                       "\n\BindingGuttertrue"+ \
                       "\n\BindingGutter={:.2f}mm".format(PriBindingGutter)+ \
                       "\n\def\SideMarginFactor{{{:.2f}}}".format(PriSideMarginFactor)+ \
                       "\n\BodyColumns=1"+ \
                       "\n\def\MergePDF{" + secfname + "}" + hdr
        self.set("l_diglotStringL", DiglotStringL)
        self.set("l_diglotStringR", DiglotStringR)
        
    def checkSFMforFancyIntroMarkers(self):
        unfitBooks = []
        prjid = self.get("fcb_project")
        prjdir = os.path.join(self.settings_dir, prjid)
        bks = self.getBooks()
        for bk in bks:
            if bk not in Info._peripheralBooks:
                fname = self.getBookFilename(bk, prjid)
                fpath = os.path.join(self.settings_dir, prjid, fname)
                if os.path.exists(fpath):
                    with open(fpath, "r", encoding="utf-8") as inf:
                        sfmtxt = inf.read()
                    # Put strict conditions on the format (including only valid \ior using 0-9, not \d digits from any script)
                    # This was probably too restrictive, but is a great RegEx: \\ior ([0-9]+(:[0-9]+)?[-\u2013][0-9]+(:[0-9]+)?) ?\\ior\*
                    if regex.search(r"\\iot .+\r?\n(\\io\d .+\\ior [0-9\-:.,\u2013\u2014 ]+\\ior\* ?\r?\n)+\\c 1", sfmtxt, flags=regex.MULTILINE) \
                       and len(regex.findall(r"\\iot",sfmtxt)) == 1: # Must have exactly 1 \iot per book 
                        pass
                    else:
                        unfitBooks.append(bk)
        return unfitBooks

    def onFindMissingCharsClicked(self, btn_findMissingChars):
        count = collections.Counter()
        prjdir = os.path.join(self.settings_dir, self.prjid)
        bks = self.getBooks()
        for bk in bks:
            fname = self.getBookFilename(bk, prjid)
            fpath = os.path.join(prjdir, fname)
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as inf:
                    # Strip out all markers themselves, and English content fields
                    sfmtxt = inf.read()
                    sfmtxt = regex.sub(r'\\id .+?\r?\n', '', sfmtxt)
                    sfmtxt = regex.sub(r'\\rem .+?\r?\n', '', sfmtxt)
                    # throw out illustration markup, BUT keep the caption text (USFM2 + USFM3)
                    sfmtxt = regex.sub(r'\\fig (.*\|){5}([^\\]+)?\|[^\\]+\\fig\*', '\2', sfmtxt) 
                    sfmtxt = regex.sub(r'\\fig ([^\\]+)?\|.*src=[^\\]+\\fig\*', '\1', sfmtxt) 
                    sfmtxt = regex.sub(r'\\[a-z]+\d?\*? ?', '', sfmtxt) # remove all \sfm codes
                    sfmtxt = regex.sub(r'[0-9]', '', sfmtxt) # remove all digits
                    bkcntr = collections.Counter(sfmtxt)
                    count += bkcntr
        # slist = sorted(count.items(), key=lambda pair: pair[0])
        f = TTFont(*self.builder.get("bl_fontR"))
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
        if finfor[0] == finfoe[0]:
            doError("The Fallback Font should to be DIFFERENT from the Regular Font.",
                    "Please select a different Font.")
        else:
            f = TTFont(*finfoe)
            msngchars = self.builder.get("t_missingChars") # .split(" ")
            msngchars = spclChars = re.sub(r"\\[uU]([0-9a-fA-F]{4,6})", lambda m:chr(int(m.group(1), 16)), msngchars)
            stillmissing = f.testcmap(msngchars)
            if len(stillmissing):
                doError("The Fallback Font just selected does NOT support all the missing characters listed.",
                        "Please select a different Font.")

