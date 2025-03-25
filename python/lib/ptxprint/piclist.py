
from ptxprint.utils import refSort, universalopen, print_traceback, nonScriptureBooks
from threading import Thread
import configparser
import regex, re, logging
import os, re, random, sys
import appdirs, traceback

logger = logging.getLogger(__name__)

posparms = ["alt", "src", "size", "pgpos", "copy", "caption", "ref", "x-xetex", "mirror", "scale"]
pos3parms = ["src", "size", "pgpos", "ref", "copy", "alt", "x-xetex", "mirror", "scale", "media", 
             "x-credit", "x-creditrot", "x-creditbox", "x-creditpos", "captionR", "refR", "srcref"]

_defaults = {
    'scale':    "1.000"
}

_parmCategories = {
    "Caption": ["caption", "captionR"],
    "SizePosn": ["pgpos", "mirror", "scale"],
    "CopyRight": ["copy"]
}

_creditcomps = {'x-creditpos': 0, 'x-creditrot': 1, 'x-creditbox': 2}

def newBase(fpath):
    doti = fpath.rfind(".")
    f = os.path.basename(fpath[:doti] if doti >= 0 else fpath)
    cl = re.findall(r"(?i)_?((?=ab|cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib)..\d{5})[abcABC]?$", f)
    if cl:
        return cl[0].lower()
    else:
        return re.sub(r'[()&+,.;: \-]', '_', f.lower())


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
        self.cfgShared = configparser.ConfigParser(interpolation=None)
        self.cfgProject = configparser.ConfigParser(interpolation=None)
        self.parent = parent
        self.src = None
        self.changed = False

    def _init_default(self, cfg, prefix):
        if not cfg.has_section('DEFAULT'):
            for k, v in _checks.items():
                t, n = k.split("_")
                if n.startswith(prefix):
                    cfg['DEFAULT'][n] = v

    def init(self, basepath):
        if basepath is None:
            return
        self.cfgShared.read(os.path.join(basepath, self.sharedfname), encoding="utf-8")
        self._init_default(self.cfgShared, "pic")
        self.cfgProject.read(os.path.join(basepath, self.parent.cfgid, self.pubfname), encoding="utf-8")
        self._init_default(self.cfgProject, "pub")

    def writeCfg(self, basepath, configid):
        if len(self.cfgShared) < 2 or configid is None:     # always a default
            return False
        self.savepic()
        for a in ((None, self.sharedfname, self.cfgShared), (configid, self.pubfname, self.cfgProject)):
            p = os.path.join(basepath, a[0]) if a[0] else basepath
            for s in a[2].sections():
                hasdata = False
                for n,o in a[2].items(section=s):
                    if a[2].has_option("DEFAULT", n) and o == a[2].get("DEFAULT", n):
                        a[2].remove_option(s, n)
                    else:
                        hasdata = True
                if not hasdata:
                    a[2].remove_section(s)
            with open(os.path.join(p, a[1]), "w", encoding="utf-8") as outf:
                a[2].write(outf)
        res = self.changed
        self.changed = False
        return res

    def loadpic(self, src):
        if self.src == newBase(src):
            return
        self.src = newBase(src)
        for (cfg, n, v, k) in self._allFields():
            val = cfg.get(self.src, n, fallback=v)
            if n == "picreverse" and val == "unknown":
                val = "OK"
            self.parent.set(k, val, mod=False)
        # MH - this doesn't seem to be working
        self.parent.set("txbf_picNotes", self.cfgProject.get(self.src, "notes", fallback=""), mod=False)
        for cfg in (self.cfgShared, self.cfgProject):
            if cfg.getboolean(self.src, "approved", fallback=False):
                self.parent.set("t_pubInits", cfg.get(self.src, "approved_by", fallback=""), mod=False)
                self.parent.set("t_pubApprDate", cfg.get(self.src, "approved_date", fallback=""), mod=False)
                self.parent.set("r_pubapprove", "scopeAny" if cfg == self.cfgProject else "scopeProject", mod=False)
                self.parent.set('c_pubApproved', True, mod=False)
                break
        else: # this happens if we never got to the break above (neither was found)
            self.parent.set('c_pubApproved', False, mod=False)
        self.onReverseRadioChanged()
        self.changed = False

    def savepic(self):
        if self.src is None:
            return False
        for (cfg, n, defval, k) in self._allFields():
            val = self.parent.get(k)
            if val is None or not val:
                continue
            if not cfg.has_section(self.src):
                cfg.add_section(self.src)   # otherwise add a section/src first
                self.changed = True
            self.changed = self.changed or cfg.get(self.src, n) != val
            cfg.set(self.src, n, val)   # update the existing entry if it already exists
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
            
    def onReverseRadioChanged(self, mod=True):
        r = self.parent.get("r_picreverse")
        self.parent.builder.get_object("fcb_plMirror").set_sensitive(False)
        if r == "always":
            self.parent.set("fcb_plMirror", "both", mod=mod)
        elif r == "never":
            self.parent.set("fcb_plMirror", "None", mod=mod)
        else: # unlock the control
            self.parent.builder.get_object("fcb_plMirror").set_sensitive(True)

    def getCreditInfo(self, src):
        text = self.cfgShared.get(src, "piccredit", fallback=None)
        res = None
        if text is not None:
            crstr = self.cfgShared.get(src, "piccreditbox", fallback="")
            m = re.match(r"^([tcb]?[lcrio]?),(-?9?0?|None),(\w*)$", crstr)
            if m:
                #res = ["" if x.lower() == "none" else x for x in m.groups()]
                res = ["" if x is None else x for x in m.groups()]
                if not res[1] or res[1].lower() == "none":
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
            self.changed = True


class Picture:

    keycount = 1
    picposns = { "L": {"col":  ("tl", "bl"),             "span": ("t", "b")},
                 "R": {"col":  ("tr", "br"),             "span": ("b", "t")},
                 "":  {"col":  ("tl", "tr", "bl", "br"), "span": ("t", "b")},
                 "B": {"col":  ("tl", "tr", "bl", "br"), "span": ("t", "b")}}
    stripsp_re = re.compile(r"^(\S+\s+\S+)\s+.*$")

    def __init__(self, **kw):
        self.fields = kw.copy()
        self.key = "p{:03d}".format(self.keycount)
        self.__class__.keycount += 1

    def __getitem__(self, k):
        return self.fields[k]

    def __setitem__(self, k, v):
        self.fields[k] = v

    def __delitem__(self, k):
        del self.fields[k]

    def __contains__(self, k):
        return k in self.fields

    def __iter__(self):
        return self.fields.__iter__()

    def copy(self):
        return Picture(**self.fields)

    def get(self, k, default):
        return self.fields.get(k, default)

    def sync(self, other, suffix=None):
        ''' are they the same picture, if so update caption and return True '''
        if self.get('srcref', self['anchor']) == other.get('srcref', other['anchor']) \
                    and self.get('src', '') == other.get('src', ''):
            if suffix:
                caption = other.get('caption'+suffix, other.get('caption', None))
                if caption is not None:
                    self['caption'+suffix] = caption
            return True
        return False

    def outstr(self, bks=[], skipkey=None, usedest=False, media=None, checks=None, picMedia=None, hiderefs=False):
        line = []
        if (len(bks) and self['anchor'][:3] not in bks) or (skipkey is not None and self.get(skipkey, False)):
            return ("", "", "")
        if usedest:
            p3p = ["destfile"] + pos3parms[1:]
        else:
            p3p = pos3parms
        mediaval = self.get('media', None)
        if mediaval is None or mediaval == '' and picMedia is not None:
            mediaval = picMedia(self.get('src', ""))[0]
        if media is not None and mediaval is not None and media not in mediaval:
            return ("", "", "")
        if picMedia is not None and mediaval == picMedia(self.get('src', ""))[0]:
            mediaval = None
        outk = self.stripsp_re.sub(r"\1", self['anchor'])
        credittxt, creditbox = checks.getCreditInfo(newBase(self.get('src', ""))) if checks is not None else (None, None)
        line = []
        for i, x in enumerate(p3p):
            val = self.get(x, None)
            if x in _defaults and _defaults[x] == val:
                continue
            elif usedest and hiderefs and x == "ref":
                continue
            elif x == "scale" and float(self.get(x, 1.0)) == 1.0:
                continue
            elif x == "media":
                val = mediaval
            elif x == "x-credit":
                val = credittxt
            elif x in _creditcomps:
                if creditbox is None:
                    continue
                val = creditbox[_creditcomps[x]]
            if not val:
                continue
            line.append('{}="{}"'.format(pos3parms[i], val))
        return (outk, self.get('caption', ''), " ".join(line))

    def set_destination(self, fn=lambda x,y,z:z, keys=None, cropme=False, srcfkey="srcpath"):
        if self.get('crop', False) == cropme and 'destfile' in self:
            return
        if keys is not None and self['anchor'][:3] not in keys:
            return
        if (fpath := self.get(srcfkey, None)) is None:
            return
        # print(fpath)
        origExt = os.path.splitext(fpath)[1]
        nB = newBase(self.get('src', ""))
        if not nB:
            logger.warn(f"src missing: {self.fields}")
        self.destfile = fn(self, self[srckey], nB+origExt.lower())
        self.crop = cropme
        v = self.get('media', "")
        if len(v) and 'p' not in v:
            self.disabled = True

    def anchor_matches(self, src, bk=None):
        if self.get('src', None) != src:
            return None
        if bk is not None and not self['anchor'].startswith(bk):
            return None
        return self['anchor']

    def clear_src_paths(self):
        for a in ('srcpath', 'destpath'):
            try:
                del self[a]
            except AttributeError:
                continue

    def set_position(self, cols=1, randomize=False, suffix=""):
        if cols == 1: # Single Column layout so change all tl+tr > t and bl+br > b
            if self.get('pgpos', None) is not None:
                self['pgpos'] = re.sub(r"([tb])[lr]", r"\1", self['pgpos'])
            elif randomize:
                self['pgpos'] = random.choice(self.picposns[suffix]['span'])
            else:
                self['pgpos'] = "t"
        elif getattr(self, 'pgpos', None) is None:
            posns = self.picposns[suffix].get(self.get('size', 'col'), self.picposns[suffix]["col"])
            if randomize:
                self['pgpos'] = random.choice(posns)
            else:
                self['pgpos'] = posns[0]

    def set_destination(self, fn=lambda x,y,z:z, keys=None, cropme=False):
        if self.get(' crop', False) == cropme and 'destfile' in self:
            return
        if keys is not None and self['anchor'][:3] not in keys:
            return
        nB = newBase(self.get('src', ""))
        if not nB:
            logger.warn(f"src missing: {self.fields}")
        if 'srcpath' not in self:
            return
        fpath = self['srcpath']
        # print(fpath)
        origExt = os.path.splitext(fpath)[1]
        self['destfile'] = fn(self, self['srcpath'], nB+origExt.lower())
        self[' crop'] = cropme
        if 'media' in self and len(self['media']) and 'p' not in self['media']:
            self['disabled'] = True

    def _fixPicinfo(self): # USFM2 to USFM3 converter
        if (p := self.get('pgpos', None)) is not None:
            if all(x in "apw" for x in p):
                self['media'] = p
                del self['pgpos']
            elif re.match(r"^[tbhpc][lrc]?[0-9]?$", p):
                self['media'] = 'p'
            else:
                self['loc'] = p
                del self['pgpos']
        if (p := self.get('size', None)) is not None:
            m = re.match(r"(col|span|page|full)(?:\*(\d+(?:\.\d*)))?$", p)
            if m:
                self['size'] = m[1]
                if m[2] is not None and len(m[2]):
                    self['scale'] = m[2]


class Piclist:

    srcfkey = 'srcpath'
    stripsp_re = re.compile(r"^(\S+\s+\S+)\s+.*$")

    def __init__(self, model=None, diglot=False):
        self.pics = {}
        self.model = model
        self.clear(model)
        self.inthread = False
        self.keycounter = 0
        self.mode = None
        self.suffix = ""
        self.isdiglot = diglot

    def __str__(self):
        return "\n".join("{}: {}".format(k, v.fields) for k, v in self.pics.items())

    def copy(self):
        res = Piclist(self.model, diglot=self.isdiglot)
        for p in self.pics.values():
            c = p.copy()
            res.pics[c.key] = c
        return res
        
    def clear(self, model=None):
        self.model = model
        if model is not None:
            if model.project is not None:
                self.prj = model.project.prjid
                self.basedir = self.model.project.path
                self.config = model.cfgid
        self.loaded = False
        self.srchlist = []

    def __delitem__(self, k):
        del self.pics[k]

    def __setitem__(self, k, v):
        self.pics[k] = v

    def remove(self, p):
        if p.key in self.pics:
            del self.pics[p.key]

    def get_pics(self):
        return self.pics.values()

    def items(self):
        return self.pics.items()

    def clear_bks(self, bks):
        for p in list(self.pics.values()):
            if p['anchor'][:3] in bks:
                self.remove(p)

    def add_picture(self, pic, suffix=None, sync=False):
        if not sync:
            for p in self.pics.values():
                if p.sync(pic, suffix=suffix):
                    return
        self.pics[pic.key] = pic

    def addpic(self, suffix="", **kw):
        m = kw['anchor'].split(' ', 1)
        suffix = suffix or ""
        kw['anchor'] = m[0] + suffix + " " + m[1]
        p = Picture(**kw)
        self.add_picture(p)

    def get(self, k, default):
        return self.pics.get(k, default)

    def load_files(self, parent, force=False, base=None, suffix="L"):
        """ Read pictures from a project either from a piclist file or the SFM files """
        if self.loaded and not force:
            return True
        if self.inthread or self.basedir is None or self.prj is None or self.config is None:
            return False
        self.thread = None
        preferred = os.path.join(self.basedir, "shared/ptxprint/{1}/{0}-{1}{2}.piclist".format(self.prj,
                    self.config, "-diglot" if self.isdiglot else ""))
        if os.path.exists(preferred):
            self.read_piclist(preferred)
            self.loaded = True
            return True
        if self.isdiglot and base is not None:
            self.merge(base, suffix)
            self.loaded = True
            return False    # Tell the parent there is more to do
        if not self.isdiglot:
            self.inthread = True
            self.threadUsfms(parent)
            self.loaded = True
            # self.thread = Thread(target=self.threadUsfms, args=(suffix,))
            return True
        return True

    def read_piclist(self, fname):
        """ Read piclist file """
        if isinstance(fname, str):
            if not os.path.exists(fname):
                return
            inf = universalopen(fname, cp=self.model.ptsettings.get('Encoding', 65001) \
                                                        if self.model is not None else 65001)
        else:
            inf = fname
        logger.debug(f"{fname=} {self.loaded=}")
        # logger.debug("".join(traceback.format_stack()))
        for l in (x.strip() for x in inf.readlines()):
            if not len(l) or l.startswith("%"):
                continue
            m = l.split("|")
            r = m[0].split(" ", 2)
            pic = {'anchor': "{} {}".format(r[0] if self.isdiglot else r[0][:3], r[1]), 'caption': r[2] if len(r) > 2 else ""}
            if len(m) > 6: # must be USFM2, so|grab|all|the|different|pieces!
                for i, f in enumerate(m[1:]):
                    if i < len(posparms)-1:
                        pic[posparms[i+1]] = f
                picture = Picture(**pic)
                picture._fixPicinfo()
            else: # otherwise USFM3, so find all the named params
                for d in re.findall(r'(\S+)\s*=\s*"([^"]+)"', m[-1]):
                    pic[d[0]] = d[1]
                picture = Picture(**pic)
            self.add_picture(picture)
        if isinstance(fname, str):
            inf.close()
        self.rmdups()

    def threadUsfms(self, parent, nosave=False):
        bks = self.model.getAllBooks()
        for bk, bkp in bks.items():
            if os.path.exists(bkp):
                self.read_sfm(bk, bkp, parent)
        self.set_positions(cols=2, randomize=True)
        if not nosave:
            self.model.savePics()
        self.inthread = False

    def _getanchor(self, m, txt, i, currentk):
        # returns anchor components. For k: ("k.<val>", "", "="+paranum); p: ("p", "", paranum)
        if m is None:
            rextras = {}
            fend = len(txt)
        else:
            rextras = {"endpos": m.start(0)}
            fend = m.start(0)
        t = regex.match(r"\\k\s(.*?)\\k\*.*?$", txt, regex.R|regex.S, **rextras)
        if t:
            res = ("k." + t.group(1).replace(" ", ""), "", "", "")
        elif currentk is not None:
            res = (currentk, "", "", "="+str(i+1) if i > 0 else "")
        else:
            res = ("p", "", "{:03d}".format(i+1), "")
        return res

    def _readpics(self, txt, bk, c, lastv, isperiph, parent, parcount=0, fn=None, sync=False):
        # logger.debug(f"Reading pics for {bk}")
        koffset = 0
        currentk = None
        for s in re.split(r"\\(?:m[st][e]?|i(?:mt[e]?|ex|[bemopqs])|s[dpr]|c[ld]|[pqrs])\d?\s", txt):
            parcount += 1
            for b in ((r"(?ms)\\fig (.*?)\|(.+?\.....?)\|(....?)\|([^\\]+?)?\|([^\\]+?)?\|([^\\]+?)?\|([^\\]+?)?\\fig\*", False),
                      (r'(?ms)\\fig ([^\\]*?)\|([^\\]+)\\fig\*', True)):
                m = list(regex.finditer(b[0], s))
                if len(m):
                    for i, f in enumerate(m):
                        if bk == "GLO":
                            a = self._getanchor(f, s, parcount - koffset, currentk)
                        else:
                            a = ("p", "", "{:03d}".format(i+1), ("="+str(parcount)) if parcount - koffset > 1 else "") if isperiph else (c, ".", lastv, "")
                        r = "{} {}{}{}{}".format(bk, *a)
                        # anchor is editable. srcref is the original location in the file to synchronise between glots, etc.
                        pic = {'anchor': r, 'caption':(f.group(1 if b[1] else 6) or "").strip(), 'srcref': r}
                        if bk == 'GLO':
                            pic.update(pgpos="p", scale="0.7")
                        if b[1]:    # usfm 3
                            labelParams = re.findall(r'([a-z]+?="[^\\]+?")', f.group(2))
                            for l in labelParams:
                                k,v = l.split("=")
                                pic[k.strip()] = v.strip('"')
                            if 'media' not in pic:
                                default, limit = parent.picMedia(pic.get('src', ''), pic.get('loc', ''))
                                pic['media'] = 'paw' if default is None else default
                            picture = Picture(**pic)
                        else:       # usfm 2
                            for j, v in enumerate(f.groups()):
                                if v is not None:
                                    pic[posparms[j]] = v
                            picture = Picture(**pic)
                            picture._fixPicinfo()
                        if fn is not None:
                            fn(picture)
                        else:
                            self.add_picture(picture, sync=sync)
                    break
            else:
                if bk == "GLO":
                    a = self._getanchor(None, s, parcount - koffset, None)
                    if a[0].startswith("k"):
                        koffset = parcount
                        currentk = a[0]

    def read_sfm(self, bk, fname, parent, media=None, sync=False, fn=None):
        isperiph = bk in nonScriptureBooks
        with universalopen(fname, cp=self.model.ptsettings.get('Encoding', 65001) \
                            if self.model is not None else 65001) as inf:
            dat = inf.read()
            if isperiph:
                self._readpics(dat, bk, 0, None, isperiph, parent, sync=sync)
            else:
                blocks = ["0"] + re.split(r"\\c\s+(\d+)", dat)
                for c, t in zip(blocks[0::2], blocks[1::2]):
                    m = re.match("(.*?)\\v ", t, re.S)
                    if m is not None:
                        s = m.group(1)
                        self._readpics(s, bk, c, 0, isperiph, parent, sync=sync)
                    for v in re.findall(r"(?s)(?<=\\v )(\d+[abc]?(?:[,-]\d+?[abc]?)?) ((?:.(?!\\v ))+)", t):
                        lastv = v[0]
                        s = v[1]
                        key = None
                        self._readpics(s, bk, c, lastv, isperiph, parent, sync=sync, fn=fn)

    def rmdups(self): # MH {checking I understand this right} Does this assume we can't have 2 pics with the same anchor?
        ''' Makes sure there are not two entries with the same anchor and same image source'''
        anchormap = {}
        for p in self.pics.values():
            if p.get('anchor', None):
              anchormap.setdefault(p['anchor'], []).append(p)
        for v in [a for a in anchormap.values() if len(a) > 1]:
            dups = {}
            for p in v:
                if 'src' in p:
                    dups.setdefault(p['src'], []).append(p)
            for d in [v for v in dups.values() if len(v) > 1]:
                for p in d[1:]:
                    self.remove(p)

    def build_searchlist(self, figFolder=None, exclusive=False, imgorder="", lowres=True):
        self.srchlist = [figFolder] if figFolder is not None else []
        chkpaths = []
        for d in ("local", ""):
            if sys.platform.startswith("win"):
                chkpaths += [os.path.join(self.basedir, d, "figures")]
            else:
                chkpaths += [os.path.join(self.basedir, x, y+"igures") for x in (d, d.title()) for y in "fF"]
        for p in chkpaths:
            if os.path.exists(p) and len(os.listdir(p)) > 0:
                if exclusive:
                    self.srchlist.append(p)
                else:
                    for dp, _, fn in os.walk(p): 
                        if len(fn): 
                            self.srchlist.append(dp)
        uddir = os.path.join(appdirs.user_data_dir("ptxprint", "SIL"), "imagesets")
        if os.path.isdir(uddir):
            self.srchlist.append(uddir)
        self.extensions = []
        extdflt = {x:i for i, x in enumerate(["jpg", "jpeg", "png", "tif", "tiff", "bmp", "pdf"])}
        extuser = re.sub("[ ,;/><]"," ",imgorder.lower()).split()
        self.extensions = {x:i for i, x in enumerate(extuser) if x in extdflt}
        if not len(self.extensions):   # If the user hasn't defined any extensions 
            if lowres:
                self.extensions = extdflt
            else:
                self.extensions = {x:i for i, x in enumerate(["tif", "tiff", "png", "jpg", "jpeg", "bmp", "pdf"])}
        logger.debug(f"{self.srchlist=} {self.extensions=}")

    def getFigureSources(self, filt=newBase, key='srcpath', keys=None, exclusive=False,
                               data=None, mode=None, figFolder=None, imgorder="", lowres=False):
        ''' Add source filename information to each figinfo, stored with the key '''
        if data is None:
            data = self.pics.values()
        if self.srchlist is None or not len(self.srchlist):
            self.build_searchlist(figFolder=figFolder, exclusive=exclusive, imgorder=imgorder, lowres=lowres)
        res = {}
        newfigs = {}
        for f in data:
            if 'src' not in f:
                continue
            if keys is not None and f['anchor'][:3] not in keys:
                continue
            newk = filt(f['src']) if filt is not None else f['src']
            newfigs.setdefault(newk, []).append(f)
        logger.debug(f"{newfigs=}")
        for srchdir in self.srchlist:
            if srchdir is None or not os.path.exists(srchdir):
                continue
            if exclusive:
                search = [(srchdir, [], os.listdir(srchdir))]
            else:
                search = os.walk(srchdir, followlinks=True, topdown=True)
            for subdir, dirs, files in search:
                for f in files:
                    nB = filt(f) if filt is not None else f
                    # logger.debug(f"{nB=} {nB in newfigs} {f=}")
                    if nB not in newfigs:
                        continue
                    doti = f.rfind(".")
                    origExt = f[doti:].lower()
                    if origExt[1:] not in self.extensions:
                        continue
                    filepath = os.path.join(subdir, f)
                    for p in newfigs[nB]:
                        if 'destfile' in p:
                            if mode == self.mode:
                                continue
                            else:
                                del p['destfile']
                        if key in p:
                            old = self.extensions.get(os.path.splitext(p[key])[1].lower()[1:], 10000)
                            new = self.extensions.get(os.path.splitext(filepath)[1].lower()[1:], 10000)
                            if new < old:
                                p[key] = filepath
                            elif old == new and lowres != bool(os.path.getsize(p[key]) < os.path.getsize(filepath)):
                                p[key] = filepath
                        else:
                            p[key] = filepath
        self.mode = mode
        return data

    def out(self, fpath, bks=[], skipkey=None, usedest=False, media=None, checks=None, hiderefs=False):
        ''' Generate a picinfo file, with given date.
                bks is a list of 3 letter bkids only to include. If empty, include all.
                skipkey if set will skip a record if there is a non False value associated with skipkey
                usedest says to use destfile rather than src as the file source in the output'''
        if not len(self.pics):
            return
        self.rmdups()
        lines = []
        pMedia = self.model.picMedia if self.model else None
        for p in sorted(self.pics.values(), key=lambda x:refSort(x['anchor'], info=['anchor'][3:4])):
            (k, caption, vals) = p.outstr(bks=bks, skipkey=skipkey, usedest=usedest, media=media,
                                          checks=checks, hiderefs=hiderefs,
                                          picMedia=pMedia, loc=p.get('loc', '')))
            if k:
                lines.append("{} {}|{}".format(k, caption, vals))

        if len(lines):
            logger.debug(f"Saving pics to {fpath} with {len(lines)} lines")
            dat = "\n".join(lines)+"\n"
            with open(fpath, "w", encoding="utf-8") as outf:
                outf.write(dat)
        elif os.path.exists(fpath):
            os.unlink(fpath)

    def updateView(self, view, bks=None, filtered=True):
        # if self.inthread:
            #GObject.timeout_add_seconds(1, self.updateView, view, bks=bks, filtered=filtered)
            # print_traceback()
        view.load(self, bks=bks if filtered else None)

    def clearSrcPaths(self):
        self.build_searchlist()
        for v in self.pics.values():
            for a in ('srcpath', 'destfile'):
                if a in v:
                    del v[a]

    def merge(self, pics, suffix, mergeCaptions=True, bkanchors=False, nonMergedBooks=None):
        ''' Used for merging piclists from monoglot into diglot (self) based on srcref and src image '''
        def stripsuffix(a):
            m = a.split(" ", 1)
            return m[0][:3] + ("" if bkanchors else (" " + m[1]))
        tgts = {}
        for v in self.get_pics():
            tgts.setdefault(stripsuffix(v['anchor']), []).append(v)
        merged = set()
        for v in pics.get_pics():
            removeme = False
            m = v['anchor'].split(" ", 1)
            addme = True
            for s in tgts.get(stripsuffix(v['anchor']), []):
                sra = s.get('srcref', '')
                srb = v.get('srcref', '')
                if newBase(s.get('src', '')) == newBase(v.get('src', '')) \
                            and (sra == '' or srb == '' or sra == srb):
                    if nonMergedBooks is None or m[0][:3] in nonMergedBooks:
                        if v['anchor'] != s['anchor'] + suffix:
                            continue
                    if mergeCaptions:
                        if v.get('caption', '') != '':
                            s['caption'+suffix] = v['caption']
                        if v.get('ref', '') != '':
                            s['ref'+suffix] = v['ref']
                    addme = False
                    break
            if addme:
                sn = v.copy()
                sn['anchor'] = m[0] + suffix + " " + m[1]
                self.pics[sn.key] = sn
                merged.add(sn.key)
        for v in list(self.get_pics()):
            m = v['anchor'].split(" ")
            if m[0][3:] == suffix and v.key not in merged:
                self.remove(v)
        self.rmdups()

    def merge_fields(self, other, fields, extend=False, removeOld=False):
        anchored = {}
        for k, v in self.items():
            anchored.setdefault(v['anchor'], []).append(k)
        for k, v in other.items():
            best = None
            for lk in anchored.get(v['anchor'], []):
                lv = self.pics[lk]
                if lv.get('src', '') == v.get('src', '') and lv.get('srcref', '') == v.get('srcref', ''):
                    best = lk
                elif best is None:
                    best = lk
            if best is not None:
                anchored[v['anchor']].remove(best)
                self.pics[best].update({f: v[f] for f in fields if f in v})
                for a in ("scale", "mirror", "x-xetex"):
                    if a in fields and a not in v and a in self.pics[best]:
                        del self.pics[best][a]
            elif extend:
                self.add_picture(v.copy())
        if removeOld:
            for l in anchored.values():
                for k in l:
                    del self.pics[k]

    def read_books(self, bks, allbooks, random=False, cols=2, sync=False):
        def posn(pic):
            pic.set_position(cols=cols, randomize=random)
            return pic

        if not sync:
            self.clear_bks(bks)
            def addpic(pic):
                self.pics[pic.key] = posn(pic)
        else:
            def addpic(pic):
                for p in self.pics.values():
                    if p.sync(pic):
                        return
                self.pics[pic.key] = posn(pic)

        for bk in bks:
            bkf = allbooks.get(bk, None)
            if bkf is None or not os.path.exists(bkf):
                continue
            self.read_sfm(bk, bkf, self.model, sync=sync, fn=addpic)

    def set_positions(self, cols=1, randomize=False, suffix=""):
        for v in self.pics.values():
            v.set_position(cols=cols, randomize=randomize, suffix=suffix)

    def set_destinations(self, fn=lambda x,y,z:z, keys=None, cropme=False):
        for v in self.pics.values():
            v.set_destination(fn=fn, keys=keys, cropme=cropme)

    def clear_destinations(self):
        for v in self.pics.values():
            if 'destfile' in v:
                del v['destfile']

    def getAnchor(self, src, bk):
        for p in self.pics.values():
            if p.get('src', None) != src:
                continue
            if bk is not None and not p['anchor'].startswith(bk):
                continue
            res = p['anchor']
            break
        else:
            res = None
        return res

    def find(self, **kw):
        ''' find all the pics (so returns a list) whose attributes match those given '''
        res = []
        for p in self.pics.values():
            for k, v in kw.items():
                if p.get(k, None) != v:
                    break
            else:
                res.append(p)
        return res
