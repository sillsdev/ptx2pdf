
from ptxprint.utils import refKey, universalopen, print_traceback
from ptxprint.texmodel import TexModel
from threading import Thread
import configparser
import regex, re
import os, re, random, sys

posparms = ["alt", "src", "size", "pgpos", "copy", "caption", "ref", "x-xetex", "mirror", "scale"]
pos3parms = ["src", "size", "pgpos", "ref", "copy", "alt", "x-xetex", "mirror", "scale", "media", 
             "x-credit", "x-creditrot", "x-creditbox", "x-creditpos", "captionR", "refR"]

_defaults = {
    'scale':    "1.000"
}

_creditcomps = {'x-creditpos': 0, 'x-creditrot': 1, 'x-creditbox': 2}

def newBase(fpath):
    doti = fpath.rfind(".")
    f = os.path.basename(fpath[:doti])
    cl = re.findall(r"(?i)_?((?=ab|cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib)..\d{5})[abcABC]?$", f)
    if cl:
        return cl[0].lower()
    else:
        return re.sub('[()&+,.;: \-]', '_', f.lower())


_checks = {
    "r_picclear":       "unknown",
    "fcb_picaccept":    "Unknown",
    "r_picreverse":     "OK",
    "fcb_pubusage":     "Unknown",
    "r_pubclear":       "unchecked",
    "r_pubnoise":       "unchecked",
    "fcb_pubaccept":    "Unknown",
    "t_piccreditbox":   "",
    "l_piccredit":      ""
}

class PicChecks:

    sharedfname = "picInfo.txt"
    pubfname = "picChecks.txt"

    def __init__(self, parent):
        self.cfgShared = configparser.ConfigParser()
        self.cfgProject = configparser.ConfigParser()
        self.parent = parent
        self.src = None

    def _init_default(self, cfg, prefix):
        if not cfg.has_section('DEFAULT'):
            for k, v in _checks.items():
                t, n = k.split("_")
                if n.startswith(prefix):
                    cfg['DEFAULT'][n] = v

    def init(self, basepath, configid):
        if basepath is None or configid is None:
            return
        self.cfgShared.read(os.path.join(basepath, self.sharedfname), encoding="utf-8")
        self._init_default(self.cfgShared, "pic")
        self.cfgProject.read(os.path.join(basepath, configid, self.pubfname), encoding="utf-8")
        self._init_default(self.cfgProject, "pub")

    def writeCfg(self, basepath, configid):
        if len(self.cfgShared) < 2 or configid is None:     # always a default
            return
        self.savepic()
        basep = os.path.join(basepath, "shared", "ptxprint")
        for a in ((None, self.sharedfname, self.cfgShared), (configid, self.pubfname, self.cfgProject)):
            p = os.path.join(basep, a[0]) if a[0] else basep
            os.makedirs(p, exist_ok=True)
            with open(os.path.join(p, a[1]), "w", encoding="utf-8") as outf:
                a[2].write(outf)

    def loadpic(self, src):
        if self.src == newBase(src):
            return
        self.src = newBase(src)
        for (cfg, n, v, k) in self._allFields():
            val = cfg.get(self.src, n, fallback=v)
            if n == "picreverse" and val == "unknown":
                val = "OK"
            self.parent.set(k, val)
        # MH - this doesn't seem to be working
        self.parent.set("txbf_picNotes", self.cfgProject.get(self.src, "notes", fallback=""))
        for cfg in (self.cfgShared, self.cfgProject):
            if cfg.getboolean(self.src, "approved", fallback=False):
                self.parent.set("t_pubInits", cfg.get(self.src, "approved_by", fallback=""))
                self.parent.set("t_pubApprDate", cfg.get(self.src, "approved_date", fallback=""))
                self.parent.set("r_pubapprove", "scopeAny" if cfg == self.cfgProject else "scopeProject")
                self.parent.set('c_pubApproved', True)
                break
        else: # this happens if we never got to the break above (neither was found)
            self.parent.set('c_pubApproved', False)
        self.onReverseRadioChanged()

    def savepic(self):
        if self.src is None:
            return
        for (cfg, n, defval, k) in self._allFields():
            val = self.parent.get(k)
            if val is None or not val:
                continue
            try:
                cfg.set(self.src, n, val)   # update the existing entry if it already exists
            except configparser.NoSectionError:
                cfg.add_section(self.src)   # otherwise add a section/src first
                cfg.set(self.src, n, val)   # and then throw in the values
        val = self.parent.get("c_pubApproved")
        cfg = self.cfgShared if self.parent.get("r_pubapprove") == "scopeAny" else self.cfgProject
        ocfg = self.cfgProject if self.parent.get("r_pubapprove") == "scopeAny" else self.cfgShared
        if val:
            cfg.set(self.src, "approved_by", self.parent.get("t_pubInits"))
            cfg.set(self.src, "approval_date", self.parent.get("t_pubApprDate"))
            cfg.set(self.src, "approved", "true")
        else:
            cfg.set(self.src, "approved", "false")
        ocfg.set(self.src, "approved", "false")
        self.cfgProject.set(self.src, "notes", self.parent.get("txbf_picNotes"))

    def filter(self, src, filt):
        if filt == 0:       # All
            return True
        elif filt == 3:     # Approved
            return self.cfgShared.getboolean(src, "approved", fallback=False) \
                or self.cfgProject.getboolean(src, "approved", fallback=False)
        else:
            vals = [cfg.get(src, n, fallback=v) == v for (cfg, n, v, _) in self._allFields()]
            if filt == 1:     # All unknown/unchecked
                return all(vals)
            elif filt == 2:     # Any unknown/unchecked
                return any(vals)
            return True

    def _allFields(self):
        for k, v in _checks.items():
            t, n = k.split("_")
            cfg = self.cfgShared if n.startswith("pic") else self.cfgProject
            yield(cfg, n, v, k)
            
    def onReverseRadioChanged(self):
        r = self.parent.get("r_picreverse")
        self.parent.builder.get_object("fcb_plMirror").set_sensitive(False)
        if r == "always":
            self.parent.set("fcb_plMirror", "both")
        elif r == "never":
            self.parent.set("fcb_plMirror", "None")
        else: # unlock the control
            self.parent.builder.get_object("fcb_plMirror").set_sensitive(True)

    def getCreditInfo(self, src):
        text = self.cfgShared.get(src, "piccredit", fallback=None)
        res = None
        if text is not None:
            crstr = self.cfgShared.get(src, "piccreditbox", fallback="")
            m = re.match(r"^([tcb]?[lcrio]?),(-?9?0?|None),(\w*)$", crstr)
            if m:
                res = ["" if x.lower() == "none" else x for x in m.groups()]
                if not res[1]:
                    res[1] = "0"
        return (text, res)
        
    # def allSrcs(self):
        # return set(list(self.cfgShared.keys()) + list(self.cfgProject.keys()))
        
    def setMultiCreditOverlays(self, srcs, crdtxt, crdtbox, copysrc):
        srcseries = re.findall(r"(?i)_?((?=ab|cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib)..\d{5})[abcABC]?", copysrc)
        if len(srcseries):
            for k in srcs:
                kseries = re.findall(r"(?i)_?((?=ab|cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib)..\d{5})[abcABC]?", k)
                if len(kseries) and kseries[0][:3].lower() == srcseries[0][:3].lower():
                    k = newBase(k)
                    if self.parent.get('c_plCreditOverwrite') or not self.cfgShared.get(k, 'piccredit', fallback=''):
                        if not self.cfgShared.has_section(k):
                            self.cfgShared.add_section(k)
                        self.cfgShared.set(k, 'piccredit', crdtxt)
                        self.cfgShared.set(k, 'piccreditbox', crdtbox)

class PicInfo(dict):

    srcfkey = 'src path'
    stripsp_re = re.compile(r"^(\S+\s+\S+)\s+.*$")

    def __init__(self, model):
        self.clear(model)
        self.inthread = False
        self.keycounter = 0
        self.mode = None

    def clear(self, model=None):
        super().clear()
        if model is not None:
            self.model = model
            self.prj = model.prjid
            if self.model.prjid is None:
                self.basedir = self.model.settings_dir
            else:
                self.basedir = os.path.join(self.model.settings_dir, model.prjid)
            self.config = model.configName()
        self.loaded = False
        self.srchlist = []

    def load_files(self, parent, suffix=""):
        if self.inthread:
            return False
        else:
            self.thread = None
        prjdir = self.basedir
        prj = self.prj
        cfg = self.config
        if prjdir is None or prj is None or cfg is None:
            return False
        preferred = os.path.join(prjdir, "shared/ptxprint/{1}/{0}-{1}.piclist".format(prj, cfg))
        if os.path.exists(preferred):
            self.read_piclist(preferred, suffix=suffix)
            self.loaded = True
            return True
        places = ["shared/ptxprint/{}.piclist".format(prj)]
        plistsdir = os.path.join(prjdir, "shared", "ptxprint", cfg, "PicLists")
        if os.path.exists(plistsdir):
            places += ["shared/ptxprint/{0}/PicLists/{1}".format(cfg, x) \
                        for x in os.listdir(plistsdir) if x.lower().endswith(".piclist")]
        havepiclists = False
        for f in places:
            p = os.path.join(prjdir, f)
            if os.path.exists(p):
                self.read_piclist(p, suffix=suffix)
                havepiclists = True
        self.loaded = True
        if not havepiclists:
            self.inthread = True
            self.threadUsfms(parent, suffix)
            # self.thread = Thread(target=self.threadUsfms, args=(suffix,))
            return False
        return True

    def merge(self, tgtpre, srcpre, indat=None, mergeCaptions=True):
        if indat is None:
            indat = self
        tgts = {}
        for k, v in self.items():
            if v['anchor'][3:].startswith(tgtpre):
                tgts.setdefault(v['anchor'][:3] + v['anchor'][3+len(tgtpre):], []).append(v)
        for k, v in list(indat.items()):
            if v['anchor'][3:].startswith(srcpre):
                a = v['anchor'][:3]+v['anchor'][3+len(srcpre):]
                if mergeCaptions:
                    for s in tgts.get(a, []):
                        if s.get('src', '') == v.get('src', ''):
                            if v.get('caption', '') != '':
                                s['caption'+srcpre] = v.get('caption', '')
                            if v.get('ref', '') != '':
                                s['ref'+srcpre] = v['ref']
                            break
                del indat[k]

    def threadUsfms(self, parent, suffix):
        bks = self.model.getAllBooks()
        for bk, bkp in bks.items():
            if os.path.exists(bkp):
                self.read_sfm(bk, bkp, parent, suffix=suffix)
        self.set_positions(cols=2, randomize=True, suffix=suffix)
        self.model.savePics()
        self.inthread = False

    def _fixPicinfo(self, vals): # USFM2 to USFM3 converter
        p = vals['pgpos']
        if all(x in "apw" for x in p):
            vals['media'] = p
            del vals['pgpos']
        elif re.match(r"^[tbhpc][lrc]?[0-9]?$", p):
            vals['media'] = 'p'
        else:
            vals['loc'] = p
            del vals['pgpos']
        p = vals['size']
        m = re.match(r"(col|span|page|full)(?:\*(\d+(?:\.\d*)))?$", p)
        if m:
            vals['size'] = m[1]
            if m[2] is not None and len(m[2]):
                vals['scale'] = m[2]
        return vals

    def newkey(self, suffix=""):
        self.keycounter += 1
        return "pic{}{}".format(suffix, self.keycounter)

    def read_piclist(self, fname, suffix=""):
        if not os.path.exists(fname):
            return
        with universalopen(fname) as inf:
            for l in (x.strip() for x in inf.readlines()):
                if not len(l) or l.startswith("%"):
                    continue
                m = l.split("|")
                r = m[0].split(maxsplit=2)
                if suffix.startswith("B"):
                    s = r[0][3:4] or suffix[1:]
                else:
                    s = suffix
                if len(r) > 1:
                    k = "{}{} {}".format(r[0][:3], s, r[1])
                else:
                    k = "{}{}".format(r[0], s)
                pic = {'anchor': k, 'caption': r[2] if len(r) > 2 else ""}
                self[self.newkey(suffix)] = pic
                if len(m) > 6: # must be USFM2, so|grab|all|the|different|pieces!
                    for i, f in enumerate(m[1:]):
                        if i < len(posparms)-1:
                            pic[posparms[i+1]] = f
                    self._fixPicinfo(pic)
                else: # otherwise USFM3, so find all the named params
                    for d in re.findall(r'(\S+)\s*=\s*"([^"]+)"', m[-1]):
                        pic[d[0]] = d[1]
        self.rmdups()

    def read_sfm(self, bk, fname, parent, suffix="", media=None):
        isperiph = bk in TexModel._peripheralBooks
        with universalopen(fname) as inf:
            dat = inf.read()
            blocks = ["0"] + re.split(r"\\c\s+(\d+)", dat)
            for c, t in zip(blocks[0::2], blocks[1::2]):
                if isperiph:
                    m = re.findall(r"(?ms)\\fig(.*?)\|(.+?\.....?)\|(col|span)[^|]*\|([^\\]+?)?\\fig\*", dat)
                    if len(m):
                        for i, f in enumerate(m):
                            r = "{}{} p{:03d}".format(bk, suffix, i+1)
                            pic = {'anchor': r, 'caption':f[0].strip(), 'src': f[1], 'size': f[2]}
                            key = self.newkey(suffix)
                            self[key] = pic
                    continue
                for v in re.findall(r"(?s)(?<=\\v )(\d+[abc]?(?:[,-]\d+?[abc]?)?) ((?:.(?!\\v ))+)", t):
                    lastv = v[0]
                    s = v[1]
                    key = None
                    m = regex.findall(r"(?ms)\\fig (.*?)\|(.+?\.....?)\|(....?)\|([^\\]+?)?\|([^\\]+?)?"
                                   r"\|([^\\]+?)?\|([^\\]+?)?\\fig\*", s)
                    if len(m):
                        # print("usfm2:", lastv, m)
                        for f in m:     # usfm 2
                            r = "{}{} {}.{}".format(bk, suffix, c, lastv)
                            pic = {'anchor': r, 'caption':f[5].strip()}
                            key = self.newkey(suffix)
                            self[key] = pic
                            for i, v in enumerate(f):
                                pic[posparms[i]] = v
                            self._fixPicinfo(pic)
                    m = regex.findall(r'(?ms)\\fig ([^\\]*?)\|([^\\]+)\\fig\*', s)
                    if len(m):
                        # print("usfm3:", lastv, m)
                        for i, f in enumerate(m):     # usfm 3
                            # lastv = f[0] or lastv
                            if "|" in f[1]:
                                break
                            a = ("p", "", "{:03d}".format(i+1)) if isperiph else (c, ".", lastv)
                            r = "{}{} {}{}{}".format(bk, suffix, *a)
                            pic = {'caption':f[0].strip(), 'anchor': r}
                            key = self.newkey(suffix)
                            self[key] = pic
                            labelParams = re.findall(r'([a-z]+?="[^\\]+?")', f[1])
                            for l in labelParams:
                                k,v = l.split("=")
                                pic[k.strip()] = v.strip('"')
                            if 'media' not in pic:
                                default, limit = parent.picMedia(pic.get('src', ''))
                                pic['media'] = 'paw' if default is None else default
                                    

    def out(self, fpath, bks=[], skipkey=None, usedest=False, media=None, checks=None):
        ''' Generate a picinfo file, with given date.
                bks is a list of 3 letter bkids only to include. If empty, include all.
                skipkey if set will skip a record if there is a non False value associated with skipkey
                usedest says to use dest file rather than src as the file source in the output'''
        if not len(self):
            return
        self.rmdups()
        hiderefs = self.model.get("c_fighiderefs")
        if usedest:
            p3p = ["dest file"] + pos3parms[1:]
        else:
            p3p = pos3parms
        lines = []
        for k, v in sorted(self.items(),
                           key=lambda x: refKey(x[1]['anchor'], info=x[1]['anchor'][3:4])):
            if (len(bks) and v['anchor'][:3] not in bks) or (skipkey is not None and v.get(skipkey, False)):
                continue
            outk = self.stripsp_re.sub(r"\1", v['anchor'])
            credittxt, creditbox = checks.getCreditInfo(newBase(v['src'])) if checks is not None else (None, None)
            line = []
            for i, x in enumerate(p3p):
                if x in _defaults and _defaults[x] == v.get(x, None):
                    continue
                elif usedest and hiderefs and x == "ref":
                    continue
                elif x == "scale" and float(v.get(x, 1.0)) == 1.0:
                    continue
                elif x == "media":
                    val = v.get(x, None)
                    if val is None or val == '':
                        val = self.model.picMedia(v.get('src', ''))[0]
                    if media is not None and val is not None and media not in val:
                        break
                    if val == self.model.picMedia(v.get('src', ''))[0]:
                        continue
                elif x == "x-credit":
                    if credittxt is None:
                        continue
                    val = credittxt
                elif x in _creditcomps:
                    if creditbox is None:
                        continue
                    val = creditbox[_creditcomps[x]]
                    if not val:
                        continue
                elif x not in v:
                    continue
                else:
                    val = v[x]
                    if not val:
                        continue
                line.append('{}="{}"'.format(pos3parms[i], val))
            else:
                lines.append("{} {}|".format(outk, v.get('caption', ''))+ " ".join(line))
        if len(lines):
            dat = "\n".join(lines)+"\n"
            with open(fpath, "w", encoding="utf-8") as outf:
                outf.write(dat)
        elif os.path.exists(fpath):
            os.unlink(fpath)

    def rmdups(self): # MH {checking I understand this right} Does this assume we can't have 2 pics with the same anchor?
        ''' Makes sure there are not two entries with the same anchor and same image source'''
        allkeys = {}
        for k,v in self.items():
            allkeys.setdefault(self.stripsp_re.sub(r"\1", v['anchor']), []).append(k)
        for k, v in allkeys.items():
            if len(v) == 1:
                continue
            srcset = set()
            for pk in v:
                s = self[pk].get('src', None)
                if s is not None:
                    if s in srcset:
                        del self[pk]
                    else:
                        srcset.add(s)

    def build_searchlist(self):
        if self.model.get("c_useCustomFolder"):
            self.srchlist = [self.model.customFigFolder]
        else:
            self.srchlist = []
            chkpaths = []
            for d in ("local", ""):
                if sys.platform.startswith("win"):
                    chkpaths += [os.path.join(self.basedir, d, "figures")]
                else:
                    chkpaths += [os.path.join(self.basedir, x, y+"igures") for x in (d, d.title()) for y in "fF"]
            for p in chkpaths:
                if os.path.exists(p) and len(os.listdir(p)) > 0:
                    for dp, _, fn in os.walk(p): 
                        if len(fn): 
                            self.srchlist += [dp]
        self.extensions = []
        extdflt = {x:i for i, x in enumerate(["jpg", "jpeg", "png", "tif", "tiff", "bmp", "pdf"])}
        imgord = self.model.get("t_imageTypeOrder").lower()
        extuser = re.sub("[ ,;/><]"," ",imgord).split()
        self.extensions = {x:i for i, x in enumerate(extuser) if x in extdflt}
        if not len(self.extensions):   # If the user hasn't defined any extensions 
            # self.extensions = extdflt  # then we can assign defaults
            if self.model.get("r_pictureRes_Low"):
                self.extensions = extdflt
            else:
                self.extensions = {x:i for i, x in enumerate(["tif", "tiff", "png", "jpg", "jpeg", "bmp", "pdf"])}
                

    def getFigureSources(self, filt=newBase, key='src path', keys=None, exclusive=False, data=None, mode=None):
        ''' Add source filename information to each figinfo, stored with the key '''
        if data is None:
            data = self
        # if self.srchlist is None: # or not len(self.srchlist):
        self.build_searchlist()
        res = {}
        newfigs = {}
        for k, f in data.items():
            if 'src' not in f:
                continue
            if keys is not None and f['anchor'][:3] not in keys:
                continue
            newk = filt(f['src']) if filt is not None else f['src']
            newfigs.setdefault(newk, []).append(k)
        for srchdir in self.srchlist:
            if srchdir is None or not os.path.exists(srchdir):
                continue
            if exclusive:
                search = [(srchdir, [], os.listdir(srchdir))]
            else:
                search = os.walk(srchdir)
            for subdir, dirs, files in search:
                for f in files:
                    doti = f.rfind(".")
                    origExt = f[doti:].lower()
                    if origExt[1:] not in self.extensions:
                        continue
                    filepath = os.path.join(subdir, f)
                    nB = filt(f) if filt is not None else f
                    if nB not in newfigs:
                        continue
                    for k in newfigs[nB]:
                        if 'dest file' in data[k]:
                            if mode == self.mode:
                                continue
                            else:
                                del data[k]['dest file']
                        if key in data[k]:
                            old = self.extensions.get(os.path.splitext(data[k][key])[1].lower()[1:], 10000)
                            new = self.extensions.get(os.path.splitext(filepath)[1].lower()[1:], 10000)
                            if new < old:
                                data[k][key] = filepath
                            elif old == new and (self.model.get("r_pictureRes_Low") \
                                                != bool(os.path.getsize(data[k][key]) < os.path.getsize(filepath))):
                                data[k][key] = filepath
                        else:
                            data[k][key] = filepath
        self.mode = mode
        return data

    def set_positions(self, cols=1, randomize=False, suffix="", isBoth=False):
        picposns = { "L": {"col":  ("tl", "bl"),             "span": ("t", "b")},
                     "R": {"col":  ("tr", "br"),             "span": ("b", "t")},
                     "":  {"col":  ("tl", "tr", "bl", "br"), "span": ("t", "b")}}
        isdblcol = self.model.get("c_doublecolumn")
        if self.model.get('c_diglot') or self.model.isDiglot:
            cols = 2 if isBoth else 1
        for k, v in self.items():
            if cols == 1: # Single Column layout so change all tl+tr > t and bl+br > b
                if 'pgpos' in v:
                    v['pgpos'] = re.sub(r"([tb])[lr]", r"\1", v['pgpos'])
                elif randomize:
                    v['pgpos'] = random.choice(picposns[suffix]['span'])
                else:
                    v['pgpos'] = "t"
            elif 'pgpos' not in v:
                posns = picposns[suffix].get(v.get('size', 'col'), picposns[suffix]["col"])
                if randomize:
                    v['pgpos'] = random.choice(posns)
                else:
                    v['pgpos'] = posns[0]
            
    def set_destinations(self, fn=lambda x,y,z:z, keys=None, cropme=False):
        for v in self.values():
            if v.get(' crop', False) == cropme and 'dest file' in v:
                continue            # no need to regenerate
            if keys is not None and v['anchor'][:3] not in keys:
                continue
            nB = newBase(v['src'])
            if self.srcfkey not in v:
                continue
            fpath = v[self.srcfkey]
            # print(fpath)
            origExt = os.path.splitext(fpath)[1]
            v['dest file'] = fn(v, v[self.srcfkey], nB+origExt.lower())
            v[' crop'] = cropme
            if 'media' in v and len(v['media']) and 'p' not in v['media']:
                v['disabled'] = True

    def updateView(self, view, bks=None, filtered=True):
        if self.inthread:
            #GObject.timeout_add_seconds(1, self.updateView, view, bks=bks, filtered=filtered)
            print_traceback()
        view.load(self, bks=bks if filtered else None)
        
    def clearSrcPaths(self):
        self.build_searchlist()
        for k, v in self.items():
            for a in ('src path', 'dest file'):
                v.pop(a, None)

    def clearDests(self):
        for k, v in self.items():
            v.pop('dest file', None)

    def getAnchor(self, src, bk=None):
        for k, v in self.items():
            if v.get('src', None) != src:
                continue
            if bk is not None and not v['anchor'].startswith(bk):
                continue
            return v['anchor']
        return None

def PicInfoUpdateProject(model, bks, allbooks, picinfos, suffix="", random=False, cols=1, doclear=True, clearsuffix=False):
    newpics = PicInfo(model)
    newpics.read_piclist(os.path.join(model.settings_dir, model.prjid, 'shared',
                                      'ptxprint', "{}.piclist".format(model.prjid)))
    delpics = set()
    if doclear:
        picinfos.clear()
    for bk in bks:
        bkf = allbooks.get(bk, None)
        if bkf is None or not os.path.exists(bkf):
            continue
        for k in [k for k,v in newpics.items() if v['anchor'][:3] == bk and (clearsuffix or (suffix != "" and v['anchor'][4] == suffix))]:
            del newpics[k]
        for k in [k for k,v in picinfos.items() if v['anchor'][:3] == bk and (clearsuffix or (suffix != "" and v['anchor'][4] == suffix))]:
            del picinfos[k]
        newpics.read_sfm(bk, bkf, model, suffix=suffix)
        newpics.set_positions(randomize=random, suffix=suffix, cols=cols, isBoth=not clearsuffix)
        for k, v in newpics.items():
            if v['anchor'][:3] == bk:
                picinfos[k+suffix] = v
    picinfos.loaded = True
