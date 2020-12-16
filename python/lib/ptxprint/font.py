from ptxprint.runner import fclist, checkoutput
import struct, re, os
from gi.repository import Pango
from pathlib import Path
from threading import Thread

pango_styles = {Pango.Style.ITALIC: "italic",
    Pango.Style.NORMAL: "",
    Pango.Style.OBLIQUE: "oblique",
    Pango.Weight.ULTRALIGHT: "ultra light",
    Pango.Weight.LIGHT: "light",
    Pango.Weight.NORMAL: "",
    Pango.Weight.BOLD: "bold",
    Pango.Weight.ULTRABOLD: "ultra bold",
    Pango.Weight.HEAVY: "heavy"
}

styles_order = {
    "Regular": 1,
    "Bold": 2,
    "Italic": 3,
    "Bold Italic": 4
}

def num2tag(n):
    if n < 0x200000:
        return str(n)
    else:
        return struct.unpack('4s', struct.pack('>L', n))[0].replace(b'\000', b'').decode()

class TTFontCache:
    def __init__(self, nofclist=False):
        self.cache = {}
        self.fontpaths = []
        self.busy = False
        if nofclist:
            return
        self.busy = True
        self.thread = Thread(target=self.loadFcList)
        self.thread.start()

    def loadFcList(self):
        files = checkoutput(["fc-list", ":file"], path="xetex")
        for f in files.split("\n"):
            if ": " not in f:
                continue
            try:
                (path, full) = f.strip().split(": ")
                if ":style=" in full:
                    (name, style) = full.split(':style=')
                else:
                    name = full
                    style = ""
                if "," in name:
                    names = name.split(",")
                else:
                    names = [name]
                if "," in style:
                    styles = style.split(",")
                else:
                    styles = [style]
            except ValueError:
                raise SyntaxError("Can't parse: {}".format(f).encode("unicode_escape"))
            styles = self.stylefilter(styles)
            for n in names:
                for s in styles:
                    self.cache.setdefault(n, {})[s] = path
        self.busy = False

    def stylefilter(self, styles):
        currweight = max(styles_order.get(s.title(), 0) for s in styles)
        if currweight == 0:
            return styles
        else:
            res = [s for s in styles if styles_order.get(s.title(), 10) >= currweight]
            return res

    def runFcCache(self):
        if self.busy:
            self.thread.join()
        dummy = checkoutput(["fc-cache"], path="xetex")
        self.cache = {}
        self.loadFcList()
        for p in self.fontpaths:
            self.addFontDir(p)
        
    def addFontDir(self, path):
        if self.busy:
            self.thread.join()
        self.fontpaths.append(path)
        for fname in os.listdir(path):
            if fname.lower().endswith(".ttf"):
                fpath = os.path.join(path, fname)
                f = TTFont(None, filename=fpath)
                f.usepath = True
                self.cache.setdefault(f.family, {})[f.style] = fpath

    def removeFontDir(self, path):
        if self.busy:
            self.thread.join()
        self.fontpaths.remove(path)
        allitems = list(self.cache.items())
        for f, c in allitems:
            theseitems = list(c.items())
            for k, v in theseitems:
                if "/" not in os.path.relpath(v, path).replace("\\", "/"):
                    del c[k]
            if not len(c):
                del self.cache[f]

    def fill_liststore(self, ls):
        if self.busy:
            self.thread.join()
        ls.clear()
        for k, v in sorted(self.cache.items()):
            score = sum(1 for j in ("Regular", "Bold", "Italic", "Bold Italic") if j in v)
            ls.append([k, 700 if score == 4 else 400])

    def fill_cbstore(self, name, cbs):
        if self.busy:
            self.thread.join()
        cbs.clear()
        v = self.cache.get(name, None)
        if v is None:
            return
        for k in sorted(v.keys(), key=lambda k:(styles_order.get(k, len(styles_order)), k)):
            cbs.append([k])

    def get(self, name, style=None):
        if self.busy:
            self.thread.join()
        f = self.cache.get(name, None)
        if f is None:
            return f
        if style is None or len(style) == 0:
            style = "Regular"
        res = f.get(style, None)
        if res is None and "Oblique" in style:
            res = f.get(style.replace("Oblique", "Italic"), None)
        return res

fontcache = None
def initFontCache(nofclist=False):
    global fontcache
    if fontcache is None:
        fontcache = TTFontCache(nofclist=nofclist)
    return fontcache
    # print(sorted(fontcache.cache.items()))

def cachepath(p, nofclist=False):
    global fontcache
    if fontcache is None:
        fontcache = TTFontCache(nofclist=nofclist)
    fontcache.addFontDir(p)

def cacheremovepath(p):
    global fontcache
    if fontcache is not None:
        fontcache.removeFontDir(p)

def fccache():
    global fontcache
    if fontcache is not None:
        fontcache.runFcCache()
    return fontcache

def getfontcache():
    return initFontCache()

class TTFont:
    cache = {}

    def __new__(cls, name, style="", **kw):
        if name is not None:
            k = "{}|{}".format(name, style)
            res = TTFont.cache.get(k, None)
        else:
            res = None
        if res is None:
            res = super(TTFont, cls).__new__(cls)
        return res

    def __init__(self, name, style="", filename=None):
        if hasattr(self, 'family'):     # already init from cache
            return
        self.extrastyles = ""
        self.family = name
        self.style = style
        if filename is not None:
            self.filename = Path(os.path.abspath(filename))
        else:
            fname = fontcache.get(name, style)
            self.filename = Path(os.path.abspath(fname)) if fname is not None else None
        self.feats = {}
        self.featvals = {}
        self.names = {}
        self.ttfont = None
        self.usepath = False
        if self.filename is not None:
            if self.readfont():
                self.family = self.names.get(1, self.family)
                self.style = self.names.get(2, self.style)
                self.style = " ".join(x.title() for x in self.style.split())
                if self.style.lower() == "regular":
                    self.style = ""
            else:                       # corrupted font so dump it
                self.dict = {}
                self.filename = None
        else:
            self.dict = {}
        # print([name, self.family, self.style, self.filename])
        k = "{}|{}".format(self.family, self.style)
        if k not in TTFont.cache:
            TTFont.cache[k] = self

    def readfont(self):
        self.dict = {}
        if self.filename == "":
            return
        with open(self.filename, "rb") as inf:
            dat = inf.read(12)
            (_, numtables) = struct.unpack(">4sH", dat[:6])
            dat = inf.read(numtables * 16)
            for i in range(numtables):
                (tag, csum, offset, length) = struct.unpack(">4sLLL", dat[i * 16: (i+1) * 16])
                try:
                    self.dict[tag.decode("ascii")] = [offset, length]
                except UnicodeDecodeError:      # messed up tag
                    return False
            self.readNames(inf)
            self.readFeat(inf)
        return True

    def readFeat(self, inf):
        self.feats = {}
        self.featvals = {}
        self.featnames = {}
        self.featvalnames = {}
        if 'Feat' not in self.dict:
            return
        inf.seek(self.dict['Feat'][0])
        data = inf.read(self.dict['Feat'][1])
        (version, subversion) = struct.unpack(">HH", data[:4])
        numFeats, = struct.unpack(">H", data[4:6])
        for i in range(numFeats):
            if version >= 2:
                (fid, nums, _, offset, flags, lid) = struct.unpack(">LHHLHH", data[12+16*i:28+16*i])
            else:
                (fid, nums, offset, flags, lid) = struct.unpack(">HHLHH", data[12+12*i:24+12*i])
            featname = self.names.get(lid, "")
            fidstr = num2tag(fid)
            self.feats[num2tag(fid)] = featname
            self.featnames[featname] = fidstr
            valdict = {}
            valnamedict = {}
            self.featvals[fidstr] = valdict
            self.featvalnames[fidstr] = valnamedict
            for j in range(nums):
                val, lid = struct.unpack(">HH", data[offset + 4*j:offset + 4*(j+1)])
                vname = self.names.get(lid, "")
                valdict[val] = vname
                valnamedict[vname] = val
            
    def readNames(self, inf):
        self.names = {}
        if 'name' not in self.dict:
            return
        inf.seek(self.dict['name'][0])
        data = inf.read(self.dict['name'][1])
        fmt, n, stringOffset = struct.unpack(b">HHH", data[:6])
        stringData = data[stringOffset:]
        data = data[6:]
        for i in range(n):
            if len(data) < 12:
                break
            (pid, eid, lid, nid, length, offset) = struct.unpack(b">HHHHHH", data[12*i:12*(i+1)])
            # only get unicode strings (US English)
            if (pid == 0 and lid == 0) or (pid == 3 and (eid < 2 or eid == 10) and lid == 1033):
                self.names[nid] = stringData[offset:offset+length].decode("utf_16_be")

    def style2str(self, style):
        return pango_styles.get(style, str(style))

    def __contains__(self, k):
        return k in self.dict

    def fname(self):
        res = self.family
        if len(self.extrastyles):
            return res + " " + " ".join(self.extrastyles)
        else:
            return res

    def loadttfont(self):
        from fontTools import ttLib
        if self.ttfont is None:
            self.ttfont = ttLib.TTFont(self.filename)

    def testcmap(self, chars):
        self.loadttfont()
        cmap = self.ttfont['cmap']
        b=cmap.getBestCmap()
        return [c for c in chars if ord(c) not in b and ord(c) > 32]

_fontstylemap = {
    '': '',
    'Regular': '',
    'Bold': '/B',
    'Italic': '/I',
    'Bold Italic': '/BI',
    'Oblique': '/I',
    'Bold Oblique': 'BI'
}

FontRef = None

class FontRef:
    def __init__(self, name, style, isGraphite=False, isCtxtSpace=False, feats=None):
        self.name = name
        self.style = style
        self.isGraphite = isGraphite
        self.isCtxtSpace = isCtxtSpace
        self.feats = feats.copy() if feats is not None else {}

    def __repr__(self):
        return str(type(self)) + self.asConfig()

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if self is None or other is None:
            return False
        if self.name != other.name or self.style != other.style or self.isGraphite != other.isGraphite:
            return False
        return self.feats == other.feats

    @classmethod
    def fromTeXStyle(cls, style, regular=None):
        name = style.get('fontname', None)
        if name is not None:
            isCtxtSpace = style.get("ztexFontGrSpace", "0") != "0"
            res = cls(name, "", isCtxtSpace=isCtxtSpace)
            feats = style.get('ztexFontFeatures', None)
            if feats is None:
                return res
            m = re.match("/([^/:;,]+)", feats)
            while m is not None:
                val = m.group(1)
                if val == "GR":
                    res.isGraphite = True
                for k, v in _fontstylemap.items():
                    if "/"+val == v:
                        res.styles = k
                feats = feats[m.endpos:]
                m = re.match("/([^/:;,]+)", feats)
            if not len(feats):
                return res
            f = res.getTtfont()
            res.feats = {}
            for feat in re.split(r"\s*:\s*", feats):
                key, val = re.split("\s*=\s*", feat)
                fid = f.featnames.get(key, key)
                fval = f.featvalnames.get(fid, {}).get(val, val)
                res.feats[fid] = fval
            return res
        if regular is None:
            return None
        res = regular.copy(cls)
        for a in ('Bold', 'Italic'):
            if a in style:
                if style[a] == "-" and a in res.style:
                    res.style = res.style.replace(a, "").strip()
                elif a not in res.style:
                    res.style.append((" " if len(res.style) else "") + a)
        return res

    @classmethod
    def fromConfig(cls, txt):
        bits = txt.split("|")
        isCtxtSpace = "False"
        if len(bits) < 4:
            (name, styles, isGraphite) = bits
        else:
            (name, styles, isGraphite) = bits[:3]
            if bits[3] not in ('True', 'False'):
                featlist = bits[3:]
            else:
                isCtxtSpace = bits[3]
                featlist = bits[4:]
        feats = {}
        if len(featlist):
            for s in featlist:
                if len(s):
                    k, v = s.split("=")
                    feats[k] = v
        return cls(name, styles, isGraphite.lower()=="true", isCtxtSpace.lower()=="true", feats)

    @classmethod
    def fromDialog(cls, name, style, isGraphite, isCtxtSpace, featstring, bi):
        res = cls(name, style, isGraphite, isCtxtSpace, None)
        res.updateFeats(featstring)
        if bi is not None:
            for i, a in enumerate(("embolden", "slant")):
                if float(bi[i]) > 0.0001:
                    res.feats[a] = bi[i]
        return res

    @classmethod
    def fromTeXStyle(cls, style):
        if 'FontName' in style:
            name = style['FontName']
            styles = []
            for a in ("Bold", "Italic"):
                if a in name:
                    name = name.replace(a, "")
                    styles.append(a)
            res = cls(name.strip(), " ".join(styles), isCtxtSpace=(style.get("ztexFontGrSpace", "0")=="0"))
            res.updateTeXFeats(style.get("ztexFontFeatures", ""))
            return res
        return None

    def copy(self, cls=None):
        res = (cls or FontRef)(self.name, self.style, self.isGraphite, self.isCtxtSpace, self.feats)
        return res

    def updateFeats(self, featstring, keep=False):
        if not keep:
            self.feats = {}
        if featstring is not None and featstring:
            for l in re.split(r'\s*[,;:]\s*|\s+', featstring):
                k, v = l.split("=")
                self.feats[k.strip()] = v.strip()

    def updateTeXFeats(self, featstring, keep=False):
        if not keep:
            self.feats = {}
        if not featstring:
            return
        while len(featstring) and featstring[0] == "/":
            m = re.match("/([^:;,/]+)", featstring)
            if m.group(1).lower() == "gr":
                self.isGraphite = True
            featstring = featstring[m.endpos:]
        if not featstring:
            return
        f = fontcache.get(self.name)
        if f is None:
            return
        for l in re.split(r"[,;:]", featstring):
            k, v = s.split("=")
            key = f.featnames.get(k.strip(), k.strip())
            val = f.featvalnames.get(key, {}).get(v.strip(), v.strip())
            self.feats[key] = val

    def fromStyle(self, bold=False, italic=False):
        newstyle = []
        if bold:
            newstyle.append("Bold")
        if italic:
            newstyle.append("Italic")
        if not len(newstyle):
            newstyle.append("Regular")
        s = " ".join(newstyle)
        f = fontcache.get(self.name, s)
        # print(f"fromStyle: {self}, {s}, {f}")
        if f is not None:
            return FontRef(self.name, s, self.isGraphite, self.isCtxtSpace, self.feats)
        res = self.copy()
        if bold:
            f = fontcache.get(self.name, "Bold")
            if f is not None:
                res.style = "Bold"
                if italic and 'slant' not in res.feats:
                    res.feats['slant'] = 0.15
                elif not italic and 'slant' in res.feats:
                    del res.feats['slant']
                if 'embolden' in res.feats:
                    del res.feats['embolden']
                return res
        if italic:
            f = fontcache.get(self.name, "Italic")
            if f is not None:
                res.style = "Italic"
                if bold and 'embolden' not in res.feats:
                    res.feats['embolden'] = 2
                elif not bold and 'embolden' in res.feats:
                    del res.feats['embolden']
                if 'slant' in res.feats:
                    del res.feats['slant']
                return res
        f = fontcache.get(self.name)
        # print(f"restyling: {self.name}")
        if f is None:
            return None
        res.style = None
        if bold and 'embolden' not in res.feats:
            res.feats['embolden'] = 2
        if not bold and 'embolden' in res.feats:
            del res.feats['embolden']
        if italic and 'slant' not in res.feats:
            res.feats['slant'] = 0.15
        elif not italic and 'slant' in res.feats:
            del res.feats['slant']
        return res

    def getTtfont(self):
        return TTFont(self.name, self.style)

    def getFake(self, name):
        return self.feats.get(name, None)

    def _getTeXComponents(self):
        if self.style is not None and len(self.style):
            s = _fontstylemap.get(self.style, None)
            name = self.name + (" "+self.style if s is None else "")
        else:
            name = self.name
            s = None
        if not s and not len(self.feats) and not self.isGraphite:
            return (name, [], [])

        f = self.getTtfont()
        sfeats = [] if s is None else [s]
        if self.isGraphite:
            sfeats.append("/GR")
        feats = []
        for k, v in self.feats.items():
            if k in ('embolden', 'slant'):
                feats.append((k, v))
                continue
            feats.append((f.feats.get(k, k), f.featvals.get(k, {}).get(int(v), v)))
        return (name, sfeats, feats)

    def updateTeXStyle(self, style, regular=None):
        res = []
        if regular is not None and self.name == regular.name:
            for a in ("Bold", "Italic"):
                x = a in regular.style
                y = a in self.style
                if x and not y:
                    style[a] = "-"
                elif y and not x:
                    style[a] = ""
                elif x:
                    del style[a]
        else:
            (name, sfeats, feats) = self._getTeXComponents()
            # print(f"updateTeXStyle: {name}, {sfeats}, {feats}")
            style['FontName'] = name
            if len(feats) or len(sfeats):
                style["ztexFontFeatures"] = "".join(sfeats) + (":" if len(sfeats) else "") \
                                            + ":".join("=".join(map(str, f)) for f in feats)
            if self.isCtxtSpace:
                style["ztexFontGrSpace"] = "2"

    def asTeXFont(self):
        (name, sfeats, feats) = self._getTeXComponents()
        res = [name, "".join(sfeats)]
        if feats is not None and len(feats):
            res.append(":" + ":".join("=".join(map(str, f)) for f in feats))
        return "".join(res)

    def asConfig(self):
        if self.feats is not None:
            featstr = "|".join("{}={}".format(k, v) for k, v in self.feats.items())
        else:
            featstr = ""
        res = [self.name, self.style or "", ("true" if self.isGraphite else "false"), featstr]
        return "|".join(res)

    def asFeatStr(self):
        return ", ".join("{}={}".format(k, v) for k, v in self.feats.items() if k not in ("embolden", "slant"))

    def asPango(self, fallbacks, size=None):
        fb = ("," + ",".join(fallbacks)) if len(fallbacks) else ""
        res = "{}{} {}".format(self.name, fb, self.style)
        return res + (" "+size if size is not None else "")

    

