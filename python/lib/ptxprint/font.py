from ptxprint.runner import fclist, checkoutput
import struct, re, os, sys
# from gi.repository import Pango
from pathlib import Path
from threading import Thread

fontconfig_template = """<?xml version="1.0"?>
<fontconfig>
    {fontsdirs}
    <dir prefix="xdg">fonts</dir>
    <cachedir prefix="xdg">fontconfig</cachedir>
    <include ignore_missing="yes">/etc/fonts/fonts.conf</include>
    <include ignore_missing="yes" prefix="xdg">fontconfig/conf.d</include>
    <include ignore_missing="yes" prefix="xdg">fontconfig/fonts.conf</include>
</fontconfig>
"""

def writefontsconf(archivedir=None):
    inf = {}
    dirs = []
    if sys.platform.startswith("win") or archivedir is not None:
        dirs.append(os.path.join(os.getenv("LOCALAPPDATA", "/"), "Microsoft", "Windows", "Fonts"))
        dirs.append(os.path.abspath(os.path.join(os.getenv("WINDIR", "/"), "Fonts")))
        fname = os.path.join(os.getenv("LOCALAPPDATA", "/"), "SIL", "ptxprint", "fonts.conf")
    if archivedir is not None or not sys.platform.startswith("win"):
        dirs.append("/usr/share/fonts")
        fname = os.path.expanduser("~/.config/ptxprint/fonts.conf")
    if archivedir is not None:
        dirs.append("../shared/fonts")
    else:
        fdir = os.path.join(os.path.dirname(__file__), '..')
        for a in (['..', 'fonts'], ['..', '..', 'fonts'], ['/usr', 'share', 'ptx2pdf', 'fonts']):
            fpath = os.path.join(fdir, *a)
            if os.path.exists(fpath):
                dirs.insert(0, os.path.abspath(fpath))
                break
        else:
            dirs.append(os.path.abspath('fonts'))
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    inf['fontsdirs'] = "\n    ".join("<dir>{}</dir>".format(d) for d in dirs)
    res = fontconfig_template.format(**inf)
    if archivedir is not None:
        return res
    else:
        with open(fname, "w", encoding="utf=8") as outf:
            outf.write(res)
        return fname

#pango_styles = {Pango.Style.ITALIC: "italic",
#    Pango.Style.NORMAL: "",
#    Pango.Style.OBLIQUE: "oblique",
#    Pango.Weight.ULTRALIGHT: "ultra light",
#    Pango.Weight.LIGHT: "light",
#    Pango.Weight.NORMAL: "",
#    Pango.Weight.BOLD: "bold",
#    Pango.Weight.ULTRABOLD: "ultra bold",
#    Pango.Weight.HEAVY: "heavy"
#}

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

def parseFeatString(featstring, defaults={}, langfeats={}):
    feats = {}
    lang = None
    base = defaults
    if featstring is not None and featstring:
        for l in re.split(r'\s*[,;:]\s*|\s+', featstring):
            k, v = l.split("=")
            if k.lower() == "language":
                lang = v.strip()
                base = langfeats.get(lang, base)
            else:
                feats[k.strip()] = v.strip()
    res = base.copy()
    res.update(feats)
    return (lang, res)

class TTFontCache:
    def __init__(self, nofclist=False):
        self.cache = {}
        self.fccache = {}
        self.fontpaths = []
        self.busy = False
        if nofclist:
            return
        self.busy = True
        self.thread = Thread(target=self.loadFcList)
        self.thread.start()

    def wait(self):
        if self.busy:
            self.thread.wait()

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
        if not len(self.cache):
            print("FClist failed:", files)
        self.fccache = {k: v.copy() for k,v in self.cache.items()}
        self.busy = False

    def stylefilter(self, styles):
        currweight = max(styles_order.get(s.title(), 0) for s in styles)
        if currweight == 0:
            return styles
        else:
            res = [s for s in styles if styles_order.get(s.title(), 10) >= currweight]
            return res

    def runFcCache(self):
        dummy = checkoutput(["fc-cache"], path="xetex")
        self.cache = {}
        self.loadFcList()
        for p in self.fontpaths:
            self.addFontDir(p, noadd=True)
        
    def addFontDir(self, path, noadd=False):
        if not noadd:
            self.fontpaths.append(path)
        for fname in os.listdir(path):
            if fname.lower().endswith(".ttf"):
                fpath = os.path.join(path, fname)
                f = TTFont(None, filename=fpath)
                f.usepath = True
                self.cache.setdefault(f.family, {})[f.style] = fpath

    def removeFontDir(self, path):
        self.fontpaths.remove(path)
        allitems = list(self.cache.items())
        for f, c in allitems:
            theseitems = list(c.items())
            for k, v in theseitems:
                if "/" not in os.path.relpath(v, path).replace("\\", "/"):
                    if f not in self.fccache or k not in self.fccache[f]:
                        del c[k]
                    else:
                        c[k] = self.fccache[f][k]
            if not len(c):
                del self.cache[f]

    def fill_liststore(self, ls):
        ls.clear()
        for k, v in sorted(self.cache.items()):
            score = sum(1 for j in ("Regular", "Bold", "Italic", "Bold Italic") if j in v)
            ls.append([k, 700 if score == 4 else 400])

    def fill_cbstore(self, name, cbs):
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

    def iscore(self, name, style=None):
        f = self.fccache.get(name, None)
        if f is None:
            return False
        if style is None or len(style) == 0:
            style = "Regular"
        res = f.get(style, None)
        if res is None and "Oblique" in style:
            res = f.get(style.replace("Oblique", "Italic"), None)
        return res != None

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

OTFeatNames = {
    "aalt": "All Alternates",
    "smcp": "Small Caps",
}
OTInternalFeats = {"ccmp", "kern", "locl", "mark", "mkmk", "rlig"}

OTLangs = {
  "aa": "AFR", "aae": "SQI", "aao": "ARA", "aat": "SQI", "ab": "ABK", "abh": "ARA",
  "abq": "ABA", "abs": "CPP", "abv": "ARA", "acf": "FAN", "acf": "CPP", "acm": "ARA",
  "acq": "ARA", "acr": "ACR", "acr": "MYN", "acw": "ARA", "acx": "ARA", "acy": "ARA",
  "ada": "DNG", "adf": "ARA", "adp": "DZN", "aeb": "ARA", "aec": "ARA", "af": "AFK",
  "afb": "ARA", "afs": "CPP", "agu": "MYN", "ahg": "AGW", "aht": "ATH", "aig": "CPP",
  "aii": "SWA", "aii": "SYR", "aiw": "ARI", "ajp": "ARA", "ak": "AKA", "akb": "AKB",
  "akb": "BTK", "aln": "SQI", "als": "SQI", "am": "AMH", "amf": "HBN", "amw": "SYR",
  "an": "ARG", "aoa": "CPP", "apa": "ATH", "apc": "ARA", "apd": "ARA", "apj": "ATH",
  "apk": "ATH", "apl": "ATH", "apm": "ATH", "apw": "ATH", "ar": "ARA", "arb": "ARA",
  "arn": "MAP", "arq": "ARA", "ars": "ARA", "ary": "MOR", "ary": "ARA", "arz": "ARA",
  "as": "ASM", "atj": "RCR", "atv": "ALT", "auj": "BBR", "auz": "ARA", "av": "AVR",
  "avl": "ARA", "ay": "AYM", "ayc": "AYM", "ayh": "ARA", "ayl": "ARA", "ayn": "ARA",
  "ayp": "ARA", "ayr": "AYM", "az": "AZE", "azb": "AZB", "azb": "AZE", "azd": "NAH",
  "azj": "AZE", "azn": "NAH", "azz": "NAH", "ba": "BSH", "bad": "BAD0", "bah": "CPP",
  "bai": "BML", "bal": "BLI", "bbc": "BBC", "bbc": "BTK", "bbj": "BML", "bbp": "BAD0",
  "bbz": "ARA", "bcc": "BLI", "bci": "BAU", "bcl": "BIK", "bcq": "BCH", "bcr": "ATH",
  "be": "BEL", "bea": "ATH", "beb": "BTI", "bem": "BEM", "ber": "BBR", "bew": "CPP",
  "bfl": "BAD0", "bfq": "BAD", "bft": "BLT", "bfu": "LAH", "bfy": "BAG", "bg": "BGR",
  "bgn": "BLI", "bgp": "BLI", "bgq": "BGQ", "bgq": "RAJ", "bgr": "QIN", "bhb": "BHI",
  "bhk": "BIK", "bhr": "MLG", "bi": "BIS", "bi": "CPP", "bin": "EDO", "biu": "QIN",
  "bjn": "MLY", "bjo": "BAD0", "bjq": "MLG", "bjs": "CPP", "bjt": "BLN", "bko": "BML",
  "bla": "BKF", "ble": "BLN", "blk": "BLK", "blk": "KRN", "bln": "BIK", "bm": "BMB",
  "bmm": "MLG", "bn": "BEN", "bo": "TIB", "bpd": "BAD0", "bpl": "CPP", "bpq": "CPP",
  "bqi": "LRC", "bqk": "BAD0", "br": "BRE", "bra": "BRI", "brc": "CPP", "bs": "BOS",
  "btb": "BTI", "btd": "BTD", "btd": "BTK", "btj": "MLY", "btm": "BTM", "btm": "BTK",
  "bto": "BIK", "bts": "BTS", "bts": "BTK", "btx": "BTX", "btx": "BTK", "btz": "BTZ",
  "btz": "BTK", "bum": "BTI", "bve": "MLY", "bvu": "MLY", "bwe": "KRN", "bxk": "LUH",
  "bxo": "CPP", "bxp": "BTI", "bxr": "RBU", "byn": "BIL", "byv": "BYV", "byv": "BML",
  "bzc": "MLG", "bzj": "CPP", "bzk": "CPP", "ca": "CAT", "caa": "MYN", "cac": "MYN",
  "caf": "CRR", "caf": "ATH", "cak": "CAK", "cak": "MYN", "cbk": "CBK", "cbk": "CPP",
  "cbl": "QIN", "ccl": "CPP", "ccm": "CPP", "cco": "CCHN", "ccq": "ARK", "cdo": "ZHS",
  "ce": "CHE", "cek": "QIN", "cey": "QIN", "cfm": "HAL", "cfm": "QIN", "ch": "CHA",
  "chf": "MYN", "chj": "CCHN", "chk": "CHK0", "chn": "CPP", "chp": "CHP", "chp": "SAY",
  "chp": "ATH", "chq": "CCHN", "chz": "CCHN", "ciw": "OJB", "cjy": "ZHS", "cka": "QIN",
  "ckb": "KUR", "ckn": "QIN", "cks": "CPP", "ckt": "CHK", "ckz": "MYN", "clc": "ATH",
  "cld": "SYR", "cle": "CCHN", "clj": "QIN", "clt": "QIN", "cmn": "ZHS", "cmr": "QIN",
  "cnb": "QIN", "cnh": "QIN", "cnk": "QIN", "cnl": "CCHN", "cnp": "ZHS", "cnr": "SRB",
  "cnt": "CCHN", "cnu": "BBR", "cnw": "QIN", "co": "COS", "coa": "MLY", "cob": "MYN",
  "coq": "ATH", "cpa": "CCHN", "cpe": "CPP", "cpf": "CPP", "cpi": "CPP", "cpx": "ZHS",
  "cqd": "HMN", "cqu": "QUH", "cqu": "QUZ", "cr": "CRE", "crh": "CRT", "cri": "CPP",
  "crj": "ECR", "crj": "YCR", "crj": "CRE", "crk": "WCR", "crk": "YCR", "crk": "CRE",
  "crl": "ECR", "crl": "YCR", "crl": "CRE", "crm": "MCR", "crm": "LCR", "crm": "CRE",
  "crp": "CPP", "crs": "CPP", "crx": "CRR", "crx": "ATH", "cs": "CSY", "csa": "CCHN",
  "csh": "QIN", "csj": "QIN", "cso": "CCHN", "csp": "ZHS", "csv": "QIN", "csw": "NCR",
  "csw": "NHC", "csw": "CRE", "csy": "QIN", "ctc": "ATH", "ctd": "QIN", "cte": "CCHN",
  "cth": "QIN", "ctl": "CCHN", "cts": "BIK", "ctu": "MYN", "cu": "CSL", "cuc": "CCHN",
  "cv": "CHU", "cvn": "CCHN", "cwd": "DCR", "cwd": "TCR", "cwd": "CRE", "cy": "WEL",
  "czh": "ZHS", "czo": "ZHS", "czt": "QIN", "da": "DAN", "dao": "QIN", "dap": "NIS",
  "dcr": "CPP", "de": "DEU", "den": "SLA", "den": "ATH", "dep": "CPP", "dgo": "DGO",
  "dgo": "DGR", "dgr": "ATH", "dhd": "MAW", "dib": "DNK", "dik": "DNK", "din": "DNK",
  "dip": "DNK", "diq": "DIQ", "diq": "ZZA", "diw": "DNK", "dje": "DJR", "djk": "CPP",
  "djr": "DJR0", "dks": "DNK", "dng": "DUN", "doi": "DGR", "drh": "MNG", "drw": "DRI",
  "drw": "FAR", "dsb": "LSB", "dty": "NEP", "dup": "MLY", "dv": "DIV", "dv": "DHV",
  "dwk": "KUI", "dwu": "DUJ", "dwy": "DUJ", "dyu": "JUL", "dz": "DZN", "ee": "EWE",
  "ekk": "ETI", "eky": "KRN", "el": "ELL", "emk": "EMK", "emk": "MNK", "emy": "MYN",
  "en": "ENG", "enb": "KAL", "enf": "FNE", "enh": "TNE", "eo": "NTO", "es": "ESP",
  "esg": "GON", "esi": "IPK", "esk": "IPK", "et": "ETI", "eto": "BTI", "eu": "EUQ",
  "eve": "EVN", "evn": "EVK", "ewo": "BTI", "eyo": "KAL", "fa": "FAR", "fab": "CPP",
  "fan": "FAN0", "fan": "BTI", "fat": "FAT", "fat": "AKA", "fbl": "BIK", "ff": "FUL",
  "ffm": "FUL", "fi": "FIN", "fil": "PIL", "fj": "FJI", "flm": "HAL", "flm": "QIN",
  "fmp": "FMP", "fmp": "BML", "fng": "CPP", "fo": "FOS", "fpe": "CPP", "fr": "FRA",
  "fub": "FUL", "fuc": "FUL", "fue": "FUL", "fuf": "FTA", "fuf": "FUL", "fuh": "FUL",
  "fui": "FUL", "fuq": "FUL", "fur": "FRL", "fuv": "FUV", "fuv": "FUL", "fy": "FRI",
  "ga": "IRI", "gaa": "GAD", "gac": "CPP", "gan": "ZHS", "gax": "ORO", "gaz": "ORO",
  "gbm": "GAW", "gce": "ATH", "gcf": "CPP", "gcl": "CPP", "gcr": "CPP", "gd": "GAE",
  "gda": "RAJ", "ggo": "GON", "gha": "BBR", "ghk": "KRN", "gho": "BBR", "gib": "CPP",
  "gil": "GIL0", "gju": "RAJ", "gkp": "GKP", "gkp": "KPL", "gl": "GAL", "gld": "NAN",
  "gn": "GUA", "gnb": "QIN", "gno": "GON", "gnw": "GUA", "gom": "KOK", "goq": "CPP",
  "gox": "BAD0", "gpe": "CPP", "grr": "BBR", "grt": "GRO", "gru": "SOG", "gsw": "ALS",
  "gu": "GUJ", "gug": "GUA", "gui": "GUA", "guk": "GMZ", "gul": "CPP", "gun": "GUA",
  "gv": "MNX", "gwi": "ATH", "gyn": "CPP", "ha": "HAU", "haa": "ATH", "hae": "ORO",
  "hak": "ZHS", "har": "HRI", "hca": "CPP", "he": "IWR", "hea": "HMN", "hi": "HIN",
  "hji": "MLY", "hlt": "QIN", "hma": "HMN", "hmc": "HMN", "hmd": "HMN", "hme": "HMN",
  "hmg": "HMN", "hmh": "HMN", "hmi": "HMN", "hmj": "HMN", "hml": "HMN", "hmm": "HMN",
  "hmp": "HMN", "hmq": "HMN", "hmr": "QIN", "hms": "HMN", "hmw": "HMN", "hmy": "HMN",
  "hmz": "HMN", "hne": "CHH", "hnj": "HMN", "hno": "HND", "ho": "HMO", "ho": "CPP",
  "hoc": "HO ", "hoi": "ATH", "hoj": "HAR", "hoj": "RAJ", "hr": "HRV", "hra": "QIN",
  "hrm": "HMN", "hsb": "USB", "hsn": "ZHS", "ht": "HAI", "ht": "CPP", "hu": "HUN",
  "huj": "HMN", "hup": "ATH", "hus": "MYN", "hwc": "CPP", "hy": "HYE0", "hy": "HYE",
  "hyw": "HYE", "hz": "HER", "ia": "INA", "iby": "IJO", "icr": "CPP", "id": "IND",
  "id": "MLY", "ida": "LUH", "idb": "CPP", "ie": "ILE", "ig": "IBO", "igb": "EBI",
  "ihb": "CPP", "ii": "YIM", "ijc": "IJO", "ije": "IJO", "ijn": "IJO", "ijs": "IJO",
  "ik": "IPK", "ike": "INU", "ikt": "INU", "in": "IND", "in": "MLY", "ing": "ATH",
  "inh": "ING", "io": "IDO", "is": "ISL", "it": "ITA", "itz": "MYN", "iu": "INU",
  "iw": "IWR", "ixl": "MYN", "ja": "JAN", "jac": "MYN", "jak": "MLY", "jam": "JAM",
  "jam": "CPP", "jax": "MLY", "jbe": "BBR", "jbn": "BBR", "jgo": "BML", "ji": "JII",
  "jkm": "KRN", "jkp": "KRN", "jv": "JAV", "jvd": "CPP", "jw": "JAV", "ka": "KAT",
  "kaa": "KRK", "kab": "KAB0", "kab": "BBR", "kam": "KMB", "kar": "KRN", "kbd": "KAB",
  "kby": "KNR", "kca": "KHK", "kca": "KHS", "kca": "KHV", "kcn": "CPP", "kdr": "KRM",
  "kdt": "KUY", "kea": "KEA", "kea": "CPP", "kek": "KEK", "kek": "MYN", "kex": "KKN",
  "kfa": "KOD", "kfr": "KAC", "kfx": "KUL", "kfy": "KMN", "kg": "KON0", "kha": "KSI",
  "khb": "XBD", "khk": "MNG", "kht": "KHT", "kht": "KHN", "ki": "KIK", "kiu": "KIU",
  "kiu": "ZZA", "kj": "KUA", "kjb": "MYN", "kjh": "KHA", "kjp": "KJP", "kjp": "KRN",
  "kjt": "KRN", "kk": "KAZ", "kkz": "ATH", "kl": "GRN", "kln": "KAL", "km": "KHM",
  "kmb": "MBN", "kmr": "KUR", "kmv": "CPP", "kmw": "KMO", "kn": "KAN", "knc": "KNR",
  "kng": "KON0", "knj": "MYN", "knn": "KOK", "ko": "KOR", "ko": "KOH", "koi": "KOP",
  "koi": "KOM", "koy": "ATH", "kpe": "KPL", "kpp": "KRN", "kpv": "KOZ", "kpv": "KOM",
  "kpy": "KYK", "kqs": "KIS", "kqy": "KRT", "kr": "KNR", "krc": "KAR", "krc": "BAL",
  "kri": "KRI", "kri": "CPP", "krt": "KNR", "kru": "KUU", "ks": "KSH", "ksh": "KSH0",
  "kss": "KIS", "ksw": "KSW", "ksw": "KRN", "ktb": "KEB", "ktu": "KON", "ktw": "ATH",
  "ku": "KUR", "kuu": "ATH", "kuw": "BAD0", "kv": "KOM", "kvb": "MLY", "kvl": "KRN",
  "kvq": "KRN", "kvr": "MLY", "kvt": "KRN", "kvu": "KRN", "kvy": "KRN", "kw": "COR",
  "kww": "CPP", "kwy": "KON0", "kxc": "KMS", "kxd": "MLY", "kxf": "KRN", "kxk": "KRN",
  "kxl": "KUU", "kxu": "KUI", "ky": "KIR", "kyu": "KYU", "kyu": "KRN", "la": "LAT",
  "lac": "MYN", "lad": "JUD", "lb": "LTZ", "lbe": "LAK", "lbj": "LDK", "lbl": "BIK",
  "lce": "MLY", "lcf": "MLY", "ldi": "KON0", "lg": "LUG", "li": "LIM", "lif": "LMB",
  "lir": "CPP", "liw": "MLY", "liy": "BAD0", "lkb": "LUH", "lko": "LUH", "lks": "LUH",
  "lld": "LAD", "lmn": "LAM", "ln": "LIN", "lna": "BAD0", "lnl": "BAD0", "lo": "LAO",
  "lou": "CPP", "lri": "LUH", "lrm": "LUH", "lrt": "CPP", "lsm": "LUH", "lt": "LTH",
  "ltg": "LVI", "lto": "LUH", "lts": "LUH", "lu": "LUB", "lus": "MIZ", "lus": "QIN",
  "luy": "LUH", "luz": "LRC", "lv": "LVI", "lvs": "LVI", "lwg": "LUH", "lzh": "ZHT",
  "lzz": "LAZ", "mai": "MTH", "mak": "MKR", "mam": "MAM", "mam": "MYN", "man": "MNK",
  "max": "MLY", "max": "CPP", "mbf": "CPP", "mcm": "CPP", "mct": "BTI", "mdf": "MOK",
  "mdy": "MLE", "men": "MDE", "meo": "MLY", "mfa": "MFA", "mfa": "MLY", "mfb": "MLY",
  "mfe": "MFE", "mfe": "CPP", "mfp": "CPP", "mg": "MLG", "mh": "MAH", "mhc": "MYN",
  "mhr": "LMA", "mhv": "ARK", "mi": "MRI", "min": "MIN", "min": "MLY", "mk": "MKD",
  "mkn": "CPP", "mku": "MNK", "ml": "MAL", "ml": "MLR", "mlq": "MLN", "mlq": "MNK",
  "mmr": "HMN", "mn": "MNG", "mnc": "MCH", "mnh": "BAD0", "mnk": "MND", "mnk": "MNK",
  "mnp": "ZHS", "mns": "MAN", "mnw": "MON", "mo": "MOL", "mod": "CPP", "mop": "MYN",
  "mpe": "MAJ", "mqg": "MLY", "mr": "MAR", "mrh": "QIN", "mrj": "HMA", "ms": "MLY",
  "msc": "MNK", "msh": "MLG", "msi": "MLY", "msi": "CPP", "mt": "MTS", "mtr": "MAW",
  "mud": "CPP", "mui": "MLY", "mup": "RAJ", "muq": "HMN", "mvb": "ATH", "mve": "MAW",
  "mvf": "MNG", "mwk": "MNK", "mwq": "QIN", "mwr": "MAW", "mww": "MWW", "mww": "HMN",
  "my": "BRM", "mym": "MEN", "myq": "MNK", "myv": "ERZ", "mzb": "BBR", "mzs": "CPP",
  "na": "NAU", "nag": "NAG", "nag": "CPP", "nan": "ZHS", "naz": "NAH", "nb": "NOR",
  "nch": "NAH", "nci": "NAH", "ncj": "NAH", "ncl": "NAH", "ncx": "NAH", "nd": "NDB",
  "ne": "NEP", "nef": "CPP", "ng": "NDG", "ngl": "LMW", "ngm": "CPP", "ngo": "SXT",
  "ngu": "NAH", "nhc": "NAH", "nhd": "GUA", "nhe": "NAH", "nhg": "NAH", "nhi": "NAH",
  "nhk": "NAH", "nhm": "NAH", "nhn": "NAH", "nhp": "NAH", "nhq": "NAH", "nht": "NAH",
  "nhv": "NAH", "nhw": "NAH", "nhx": "NAH", "nhy": "NAH", "nhz": "NAH", "niq": "KAL",
  "niv": "GIL", "njt": "CPP", "njz": "NIS", "nkx": "IJO", "nl": "NLD", "nla": "BML",
  "nle": "LUH", "nln": "NAH", "nlv": "NAH", "nn": "NYN", "nn": "NOR", "nnh": "BML",
  "nnz": "BML", "no": "NOR", "nod": "NTA", "npi": "NEP", "npl": "NAH", "nqo": "NKO",
  "nr": "NDB", "nsk": "NAS", "nsu": "NAH", "nue": "BAD0", "nuu": "BAD0", "nuz": "NAH",
  "nv": "NAV", "nv": "ATH", "nwe": "BML", "ny": "CHI", "nyd": "LUH", "nyn": "NKL",
  "oc": "OCI", "oj": "OJB", "ojc": "OJB", "ojg": "OJB", "ojs": "OCR", "ojs": "OJB",
  "ojw": "OJB", "okd": "IJO", "oki": "KAL", "okm": "KOH", "okr": "IJO", "om": "ORO",
  "onx": "CPP", "oor": "CPP", "or": "ORI", "orc": "ORO", "orn": "MLY", "orr": "IJO",
  "ors": "MLY", "ory": "ORI", "os": "OSS", "otw": "OJB", "oua": "BBR", "pa": "PAN",
  "pap": "PAP0", "pap": "CPP", "pbt": "PAS", "pbu": "PAS", "pce": "PLG", "pck": "QIN",
  "pcm": "CPP", "pdu": "KRN", "pea": "CPP", "pel": "MLY", "pes": "FAR", "pey": "CPP",
  "pga": "ARA", "pga": "CPP", "pi": "PAL", "pih": "PIH", "pih": "CPP", "pis": "CPP",
  "pkh": "QIN", "pko": "KAL", "pl": "PLK", "pll": "PLG", "pln": "CPP", "plp": "PAP",
  "plt": "MLG", "pml": "CPP", "pmy": "CPP", "poc": "MYN", "poh": "POH", "poh": "MYN",
  "pov": "CPP", "ppa": "BAG", "pre": "CPP", "prs": "DRI", "prs": "FAR", "ps": "PAS",
  "pse": "MLY", "pst": "PAS", "pt": "PTG", "pub": "QIN", "puz": "QIN", "pwo": "PWO",
  "pwo": "KRN", "pww": "KRN", "qu": "QUZ", "qub": "QWH", "qub": "QUZ", "quc": "QUC",
  "quc": "MYN", "qud": "QVI", "qud": "QUZ", "quf": "QUZ", "qug": "QVI", "qug": "QUZ",
  "quh": "QUH", "quh": "QUZ", "quk": "QUZ", "qul": "QUH", "qul": "QUZ", "qum": "MYN",
  "qup": "QVI", "qup": "QUZ", "qur": "QWH", "qur": "QUZ", "qus": "QUH", "qus": "QUZ",
  "quv": "MYN", "quw": "QVI", "quw": "QUZ", "qux": "QWH", "qux": "QUZ", "quy": "QUZ",
  "qva": "QWH", "qva": "QUZ", "qvc": "QUZ", "qve": "QUZ", "qvh": "QWH", "qvh": "QUZ",
  "qvi": "QVI", "qvi": "QUZ", "qvj": "QVI", "qvj": "QUZ", "qvl": "QWH", "qvl": "QUZ",
  "qvm": "QWH", "qvm": "QUZ", "qvn": "QWH", "qvn": "QUZ", "qvo": "QVI", "qvo": "QUZ",
  "qvp": "QWH", "qvp": "QUZ", "qvs": "QUZ", "qvw": "QWH", "qvw": "QUZ", "qvz": "QVI",
  "qvz": "QUZ", "qwa": "QWH", "qwa": "QUZ", "qwc": "QUZ", "qwh": "QWH", "qwh": "QUZ",
  "qws": "QWH", "qws": "QUZ", "qwt": "ATH", "qxa": "QWH", "qxa": "QUZ", "qxc": "QWH",
  "qxc": "QUZ", "qxh": "QWH", "qxh": "QUZ", "qxl": "QVI", "qxl": "QUZ", "qxn": "QWH",
  "qxn": "QUZ", "qxo": "QWH", "qxo": "QUZ", "qxp": "QUZ", "qxr": "QVI", "qxr": "QUZ",
  "qxt": "QWH", "qxt": "QUZ", "qxu": "QUZ", "qxw": "QWH", "qxw": "QUZ", "rag": "LUH",
  "ral": "QIN", "rbb": "PLG", "rbl": "BIK", "rcf": "CPP", "rif": "RIF", "rif": "BBR",
  "rki": "ARK", "rm": "RMS", "rmc": "ROY", "rmf": "ROY", "rml": "ROY", "rmn": "ROY",
  "rmo": "ROY", "rmw": "ROY", "rmy": "RMY", "rmy": "ROY", "rmz": "ARK", "rn": "RUN",
  "ro": "ROM", "rom": "ROY", "rop": "CPP", "rtc": "QIN", "ru": "RUS", "rue": "RSY",
  "rw": "RUA", "rwr": "MAW", "sa": "SAN", "sah": "YAK", "sam": "PAA", "sc": "SRD",
  "scf": "CPP", "sch": "QIN", "sci": "CPP", "sck": "SAD", "scs": "SCS", "scs": "SLA",
  "scs": "ATH", "sd": "SND", "sdc": "SRD", "sdh": "KUR", "sdn": "SRD", "sds": "BBR",
  "se": "NSM", "seh": "SNA", "sek": "ATH", "sez": "QIN", "sfm": "HMN", "sg": "SGO",
  "sgc": "KAL", "sgw": "CHG", "shi": "SHI", "shi": "BBR", "shl": "QIN", "shu": "ARA",
  "shy": "BBR", "si": "SNH", "siz": "BBR", "sjd": "KSM", "sjo": "SIB", "sjs": "BBR",
  "sk": "SKY", "skg": "MLG", "skr": "SRK", "skw": "CPP", "sl": "SLV", "sm": "SMO",
  "sma": "SSM", "smj": "LSM", "smn": "ISM", "sms": "SKS", "smt": "QIN", "sn": "SNA0",
  "so": "SML", "spv": "ORI", "spy": "KAL", "sq": "SQI", "sr": "SRB", "src": "SRD",
  "srm": "CPP", "srn": "CPP", "sro": "SRD", "srs": "ATH", "ss": "SWZ", "ssh": "ARA",
  "st": "SOT", "sta": "CPP", "stv": "SIG", "su": "SUN", "suq": "SUR", "sv": "SVE",
  "svc": "CPP", "sw": "SWK", "swb": "CMR", "swc": "SWK", "swh": "SWK", "swn": "BBR",
  "swv": "MAW", "syc": "SYR", "ta": "TAM", "taa": "ATH", "taq": "TMH", "taq": "BBR",
  "tas": "CPP", "tau": "ATH", "tcb": "ATH", "tce": "ATH", "tch": "CPP", "tcp": "QIN",
  "tcs": "CPP", "tcy": "TUL", "tcz": "QIN", "tdx": "MLG", "te": "TEL", "tec": "KAL",
  "tem": "TMN", "tez": "BBR", "tfn": "ATH", "tg": "TAJ", "tgh": "CPP", "tgj": "NIS",
  "tgx": "ATH", "th": "THA", "tht": "ATH", "thv": "TMH", "thv": "BBR", "thz": "TMH",
  "thz": "BBR", "ti": "TGY", "tia": "BBR", "tig": "TGR", "tjo": "BBR", "tk": "TKM",
  "tkg": "MLG", "tl": "TGL", "tmg": "CPP", "tmh": "TMH", "tmh": "BBR", "tmw": "MLY",
  "tn": "TNA", "tnf": "DRI", "tnf": "FAR", "to": "TGN", "tod": "TOD0", "toi": "TNG",
  "toj": "MYN", "tol": "ATH", "tor": "BAD0", "tpi": "TPI", "tpi": "CPP", "tr": "TRK",
  "trf": "CPP", "tru": "TUA", "tru": "SYR", "ts": "TSG", "tt": "TAT", "ttc": "MYN",
  "ttm": "ATH", "ttq": "TMH", "ttq": "BBR", "tuu": "ATH", "tuy": "KAL", "tvy": "CPP",
  "tw": "TWI", "tw": "AKA", "txc": "ATH", "txy": "MLG", "ty": "THT", "tyv": "TUV",
  "tzh": "MYN", "tzj": "MYN", "tzm": "TZM", "tzm": "BBR", "tzo": "TZO", "tzo": "MYN",
  "ubl": "BIK", "ug": "UYG", "uk": "UKR", "uki": "KUI", "uln": "CPP", "unr": "MUN",
  "ur": "URD", "urk": "MLY", "usp": "MYN", "uz": "UZB", "uzn": "UZB", "uzs": "UZB",
  "vap": "QIN", "ve": "VEN", "vi": "VIT", "vic": "CPP", "vkk": "MLY", "vkp": "CPP",
  "vkt": "MLY", "vls": "FLE", "vmw": "MAK", "vo": "VOL", "wa": "WLN", "wbm": "WA ",
  "wbr": "WAG", "wbr": "RAJ", "wea": "KRN", "wes": "CPP", "weu": "QIN", "wlc": "CMR",
  "wle": "SIG", "wlk": "ATH", "wni": "CMR", "wo": "WLF", "wry": "MAW", "wsg": "GON",
  "wuu": "ZHS", "xal": "KLM", "xal": "TOD", "xan": "SEK", "xh": "XHS", "xmg": "BML",
  "xmm": "MLY", "xmm": "CPP", "xmv": "MLG", "xmw": "MLG", "xnr": "DGR", "xpe": "XPE",
  "xpe": "KPL", "xsl": "SSL", "xsl": "SLA", "xsl": "ATH", "xst": "SIG", "xup": "ATH",
  "xwo": "TOD", "yaj": "BAD0", "ybb": "BML", "ybd": "ARK", "ydd": "JII", "yi": "JII",
  "yih": "JII", "yo": "YBA", "yos": "QIN", "yua": "MYN", "yue": "ZHH", "za": "ZHA",
  "zch": "ZHA", "zdj": "CMR", "zeh": "ZHA", "zen": "BBR", "zgb": "ZHA", "zgh": "ZGH",
  "zgh": "BBR", "zgm": "ZHA", "zgn": "ZHA", "zh": "ZHS", "zhd": "ZHA", "zhn": "ZHA",
  "zlj": "ZHA", "zlm": "MLY", "zln": "ZHA", "zlq": "ZHA", "zmi": "MLY", "zmz": "BAD0",
  "zne": "ZND", "zom": "QIN", "zqe": "ZHA", "zsm": "MLY", "zu": "ZUL", "zum": "LRC",
  "zyb": "ZHA", "zyg": "ZHA", "zyj": "ZHA", "zyn": "ZHA", "zyp": "QIN", "zzj": "ZHA",
}

OTToLangs = {}
for k, v in sorted(OTLangs.items()):
    OTToLangs.setdefault(v, []).append(k)

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

    def __init__(self, name, style=None, filename=None):
        if hasattr(self, 'family'):     # already init from cache
            return
        if style is None:
            style = ""
        self.extrastyles = ""
        self.family = name
        self.style = style
        if filename is not None:
            self.filename = Path(os.path.abspath(filename))
        else:
            fname = initFontCache().get(name, style)
            self.filename = Path(os.path.abspath(fname)) if fname is not None else None
        self.iscore = initFontCache().iscore(name, style)
        self.feats = {}
        self.featvals = {}
        self.names = {}
        self.ttfont = None
        self.usepath = False
        self.ascent = 0.
        self.descent = 0.
        self.upem = 1
        self.isGraphite = False
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
            self.readSill(inf)
            self.readOTFeats(inf)
            self.readOTLangs(inf)
            self.readhhea(inf)
            self.readhead(inf)
        self.isGraphite = 'Silf' in self.dict
        return True

    def readFeat(self, inf):
        self.feats = {}
        self.featvals = {}
        self.featnames = {}
        self.featvalnames = {}
        self.featdefaults = {}
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
            if nums < 1:
                continue
            featname = self.names.get(lid, "")
            fidstr = num2tag(fid)
            self.feats[fidstr] = featname
            self.featnames[featname] = fidstr
            valdict = {}
            valnamedict = {}
            self.featvals[fidstr] = valdict
            self.featvalnames[fidstr] = valnamedict
            self.featdefaults[fidstr] = 0
            for j in range(nums):
                val, lid = struct.unpack(">HH", data[offset + 4*j:offset + 4*(j+1)])
                vname = self.names.get(lid, "")
                valdict[val] = vname
                valnamedict[vname] = val
                if j == 0:
                    self.featdefaults[fidstr] = val

    def readSill(self, inf):
        self.grLangs = {}
        self.langfeats = {}
        if 'Sill' not in self.dict:
            return
        inf.seek(self.dict['Sill'][0])
        data = inf.read(12)
        numlangs = struct.unpack(">H", data[4:6])[0]
        data = inf.read(8 * numlangs)
        for i in range(numlangs):
            tagnum, numsettings, o = struct.unpack(">LHH", data[i*8:i*8+8])
            langtag = num2tag(tagnum)
            self.grLangs[langtag] = langtag
            self.langfeats[langtag] = {}
            inf.seek(self.dict['Sill'][0] + o)
            setdat = inf.read(numsettings * 8)
            for j in range(numsettings):
                fnum, value = struct.unpack(">LH", setdat[j*8:j*8+6])
                self.langfeats[langtag][num2tag(fnum)] = value

    def make_tooltip(self, feat, nid, tid, sid, parmCount):
        if tid or sid:
            txt = self.names.get(tid, "")
            stxt = self.names.get(sid, "")
            if len(stxt):
                txt += ("\n" if len(txt) else "") + \
                       " -> ".join('<span font_family="{}" font_features="{}={}">{}</span>'.format(self.family, feat, i, stxt) for i in range(parmCount+1))
        else:
            txt = ""
        return txt

    def readOTFeats(self, inf):
        self.otFeats = {}
        self.otVals = {}
        self.tipFeats = {}
        for a in ('GSUB', 'GPOS'):
            if a not in self.dict:
                continue
            inf.seek(self.dict[a][0]+6)
            data = inf.read(2)
            featOffset = struct.unpack(">H", data)[0]
            inf.seek(self.dict[a][0]+featOffset)
            data = inf.read(2)
            featCount = struct.unpack(">H", data)[0]
            data = inf.read(featCount * 6)
            for i in range(featCount):
                tagnum, o = struct.unpack(">LH", data[i*6:(i+1)*6])
                feat = num2tag(tagnum)
                if feat in OTInternalFeats:
                    continue
                inf.seek(self.dict[a][0]+featOffset+o)
                dataf = inf.read(2)
                po = struct.unpack(">H", dataf)[0]
                if po != 0 and (feat.startswith("cv") or feat.startswith("ss")):
                    inf.seek(self.dict[a][0]+featOffset+o+po)
                    dataf = inf.read(8)
                    _, nid, tid, sid = struct.unpack(">HHHH", dataf)
                    self.otFeats[feat] = self.names.get(nid, feat)
                    if feat.startswith("cv"):
                        dataf = inf.read(8)
                        parmCount, parmid = struct.unpack(">HH", dataf[:4])
                        self.tipFeats[feat] = self.make_tooltip(feat, nid, tid, sid, parmCount)
                        valdict = {i+1: self.names.get(parmid+i, str(i)) for i in range(parmCount)}
                        valdict[0] = "Off"
                        self.otVals[feat] = valdict
                    else:
                        self.tipFeats[feat] = self.make_tooltip(feat, nid, tid, sid, 1)
                else:
                    self.otFeats[feat] = OTFeatNames.get(feat, feat)

    def readOTLangs(self, inf):
        self.otLangs = {}
        for a in ('GSUB', 'GPOS'):
            if a not in self.dict:
                continue
            inf.seek(self.dict[a][0]+4)
            data = inf.read(2)
            scrOffset = struct.unpack(">H", data)[0]
            inf.seek(self.dict[a][0]+scrOffset)
            data = inf.read(2)
            scrCount = struct.unpack(">H", data)[0]
            data = inf.read(scrCount * 6)
            for i in range(scrCount):
                _, langOffset = struct.unpack(">LH", data[i*6:(i+1)*6])
                inf.seek(self.dict[a][0]+scrOffset+langOffset)
                datal = inf.read(4)
                _, langCount = struct.unpack(">HH", datal)
                datal = inf.read(6*langCount)
                for j in range(langCount):
                    tagnum, _ = struct.unpack(">LH", datal[j*6:(j+1)*6])
                    tag = num2tag(tagnum).rstrip()
                    for l in OTToLangs.get(tag, ["hbot-"+tag]):
                        self.otLangs[l] = l
            
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

    def readhhea(self, inf):
        inf.seek(self.dict['hhea'][0])
        data = inf.read(8)
        self.ascent, self.descent = struct.unpack(b">Hh", data[4:])

    def readhead(self, inf):
        inf.seek(self.dict['head'][0])
        data = inf.read(20)
        self.upem = struct.unpack(b">H", data[18:])[0]

    # def style2str(self, style):
    #     return pango_styles.get(style, str(style))

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
    def __init__(self, name, style, isGraphite=False, isCtxtSpace=False, feats=None, lang=None):
        self.name = name
        self.style = style
        self.isGraphite = isGraphite
        self.isCtxtSpace = isCtxtSpace
        self.feats = feats.copy() if feats is not None else {}
        self.lang = lang

    def __repr__(self):
        return str(type(self)) + self.asConfig()

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if self is None or other is None:
            return False
        if self.name != other.name or self.style != other.style or self.isGraphite != other.isGraphite:
            return False
        if self.lang != other.lang:
            return False
        return self.feats == other.feats

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
        lang = None
        if len(featlist):
            for s in featlist:
                if len(s):
                    k, v = s.split("=")
                    if k == "language":
                        lang = v
                    else:
                        feats[k] = v
        return cls(name, styles, isGraphite.lower()=="true", isCtxtSpace.lower()=="true", feats, lang)

    @classmethod
    def fromDialog(cls, name, style, isGraphite, isCtxtSpace, featstring, bi):
        res = cls(name, style, isGraphite, isCtxtSpace)
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
            if name.startswith("[") and name.endswith("]") and os.path.exists(name[1:-1]):
                f = TTFont(None, filename=name[1:-1])
                name = f.family
            styles = []
            for a in ("Bold", "Italic"):
                if a in name:
                    name = name.replace(a, "")
                    styles.append(a)
            res = cls(name.strip(), " ".join(styles), isCtxtSpace=(style.get("ztexFontGrSpace", "0")!="0"))
            res.updateTeXFeats(style.get("ztexFontFeatures", ""))
            return res
        return None

    def copy(self, cls=None):
        res = (cls or FontRef)(self.name, self.style, self.isGraphite, self.isCtxtSpace, self.feats)
        return res

    def updateFeats(self, featstring, keep=False):
        (lang, feats) = parseFeatString(featstring)
        if not keep:
            self.feats = {}
            self.lang = None
        if self.lang is None or lang is not None:
            self.lang = lang
        self.feats.update(feats)

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
        f = TTFont(self.name, self.style)
        if f is None:
            return
        for l in re.split(r"[,;:]", featstring):
            if not len(l):
                continue
            k, v = l.split("=")
            if k.strip().lower() == "language":
                self.lang = v.strip()
                continue
            elif self.isGraphite:
                key = f.featnames.get(k.strip(), k.strip())
                val = f.featvalnames.get(key, {}).get(v.strip(), v.strip())
            else:
                key = k.strip().lstrip("+")
                val = v.strip()
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

    def _getTeXComponents(self, inarchive=False, root=None):
        f = self.getTtfont()
        self.isGraphite = self.isGraphite and f.isGraphite
        s = None
        if f.filename is not None and not f.iscore:
            if inarchive:
                fname = f"../shared/fonts/{f.filename.name}"
            elif root is not None:
                fname = os.path.relpath(f.filename, root)
            else:
                fname = f.filename.as_posix()
            name = "[{}]".format(fname)
        elif self.style is not None and len(self.style):
            s = _fontstylemap.get(self.style, None)
            name = self.name + (" "+self.style if s is None else "")
        else:
            name = self.name
        if not s and not len(self.feats) and not self.isGraphite:
            return (name, [], [])

        sfeats = [] if s is None else [s]
        if self.isGraphite:
            sfeats.append("/GR")
        feats = []
        for k, v in self.feats.items():
            if k in ('embolden', 'slant'):
                feats.append((k, v))
                continue
            if self.isGraphite:
                feats.append((f.feats.get(k, k), f.featvals.get(k, {}).get(int(v), v)))
            else:
                feats.append(("+"+k, v))
        return (name, sfeats, feats)

    def updateTeXStyle(self, style, regular=None, inArchive=False, root=None):
        res = []
        if regular is not None and self.name == regular.name:
            for a in ("Bold", "Italic"):
                x = a in (regular.style or "")
                y = a in (self.style or "")
                if x and not y:
                    style[a] = "-"
                elif y and not x:
                    style[a] = ""
                elif x:
                    del style[a]
        else:
            (name, sfeats, feats) = self._getTeXComponents(inarchive=inArchive, root=root)
            # print(f"updateTeXStyle: {name}, {sfeats}, {feats}")
            style['FontName'] = name
            if len(feats) or len(sfeats):
                ztexs = []
                initcolon = True
                if len(sfeats):
                    ztexs.append("".join(sfeats))
                    initcolon = False
                if self.lang is not None:
                    ztexs.append("language={}".format(self.lang))
                if len(feats):
                    ztexs.extend("=".join(map(str, f)) for f in feats)
                style["ztexFontFeatures"] = (":" if initcolon else "") + ":".join(ztexs)
            else:
                style.pop("ztexFontFeatures", None)

            if self.isCtxtSpace and self.isGraphite:
                style["ztexFontGrSpace"] = "2"
            else:
                style.pop("ztexFontGrSpace", None)

    def asTeXFont(self, inarchive=False):
        (name, sfeats, feats) = self._getTeXComponents(inarchive)
        res = [name, "".join(sfeats)]
        if self.lang is not None:
            res.append(":language={}".format(self.lang))
        res.append(":" + ":".join("=".join(map(str, f)) for f in feats))
        return "".join(res)

    def asConfig(self):
        if self.feats is not None:
            featstr = "|".join("{}={}".format(k, v) for k, v in self.feats.items())
        else:
            featstr = ""
        res = [self.name, self.style or "", ("true" if self.isGraphite else "false"), featstr]
        if self.lang is not None:
            res.append("language={}".format(self.lang))
        return "|".join(res)

    def asFeatStr(self):
        res = ["{}={}".format(k, v) for k, v in self.feats.items() if k not in ("embolden", "slant")]
        if self.lang is not None:
            res.append("language={}".format(self.lang))
        return ", ".join(res)

    def asPango(self, fallbacks, size=None):
        fb = ("," + ",".join(fallbacks)) if len(fallbacks) else ""
        res = "{}{} {}".format(self.name, fb, self.style)
        return res + (" "+size if size is not None else "")

    

