import gettext
import locale, codecs, traceback
import os, sys, re, pathlib
import xml.etree.ElementTree as et
from inspect import currentframe
from struct import unpack
import contextlib, appdirs, pickle, gzip
from subprocess import check_output

DataVersion = 2

# For future Reference on how Paratext treats this list:
# G                                     M M                         RT                P        X      FBO    ICGTND          L  OT X NT DC  -  X Y  -  Z  --  L
# E                                     A A                         EO                S        X      RAT    NNLDDA          A  
# N                                     L T                         VB                2        ABCDEFGTKH    TCOXXG          O  39+1+27+18+(8)+7+3+(4)+6+(10)+1 = 124
# 1111111111111111111111111111111111111110111111111111111111111111111111111111111111111000000001111111111000011111100000000001  CompleteCanon (all books possible)

# 0000000001111111111222222222233333333334444444444555555555566666666667777777777888888888899999999991AAAAAAAAAABBBBBBBBBBCCCC
# 1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890012345678901234567890123
#                                                                                                    0
_bookslist = """GEN|50 EXO|40 LEV|27 NUM|36 DEU|34 JOS|24 JDG|21 RUT|4 1SA|31 2SA|24 1KI|22 2KI|25 1CH|29 2CH|36 EZR|10 NEH|13
        EST|10 JOB|42 PSA|150 PRO|31 ECC|12 SNG|8 ISA|66 JER|52 LAM|5 EZK|48 DAN|12 HOS|14 JOL|3 AMO|9 OBA|1 JON|4 MIC|7 NAM|3
        HAB|3 ZEP|3 HAG|2 ZEC|14 MAL|4 ZZZ|0
        MAT|28 MRK|16 LUK|24 JHN|21 ACT|28 ROM|16 1CO|16 2CO|13 GAL|6 EPH|6 PHP|4 COL|4
        1TH|5 2TH|3 1TI|6 2TI|4 TIT|3 PHM|1 HEB|13 JAS|5 1PE|5 2PE|3 1JN|5 2JN|1 3JN|1 JUD|1 REV|22
        TOB|14 JDT|16 ESG|10 WIS|19 SIR|51 BAR|6 LJE|1 S3Y|1 SUS|1 BEL|1 1MA|16 2MA|15 3MA|7 4MA|18 1ES|9 2ES|16 MAN|1 PS2|1
        ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 XXA|999 XXB|999 XXC|999 XXD|999 XXE|999 XXF|999 XXG|999 FRT|0 BAK|999 OTH|999 XXS|0 ZZZ|0 
        ZZZ|0 ZZZ|0 INT|999 CNC|999 GLO|999 TDX|999 NDX|999 DAG|14 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 LAO|1"""
        
_hebOrder = ["GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "1SA", "2SA", "1KI", "2KI", "ISA", "JER", "EZK", "HOS", "JOL", "AMO",
             "OBA", "JON", "MIC", "NAM", "HAB", "ZEP", "HAG", "ZEC", "MAL", "PSA", "PRO", "JOB", "SNG", "RUT", "LAM", "ECC", "EST", 
             "DAN", "EZR", "NEH", "1CH", "2CH"]
             
_endBkCodes = {'XXG':'100', 'FRT':'A0', 'BAK':'A1', 'OTH':'A2', 'INT':'A7', 'CNC':'A8', 'GLO':'A9',
               'TDX':'B0', 'NDX':'B1', 'DAG':'B2', 'LAO':'C3', 'XXS': '101'} 

_allbooks = ["FRT", "INT", 
            "GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT", "1SA", "2SA", "1KI", "2KI", "1CH", "2CH", "EZR", "NEH", "EST",
            "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER", "LAM", "EZK", "DAN", "HOS", "JOL", "AMO", "OBA", "JON", "MIC", "NAM",
            "HAB", "ZEP", "HAG", "ZEC", "MAL", 
            "TOB", "JDT", "ESG", "WIS", "SIR", "BAR", "LJE", "S3Y", "SUS", "BEL", 
            "1MA", "2MA", "3MA", "4MA", "1ES", "2ES", "MAN", "PS2", "DAG", "LAO",
            "MAT", "MRK", "LUK", "JHN", "ACT", "ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI", "TIT",
            "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV", 
            "XXA", "XXB", "XXC", "XXD", "XXE", "XXF", "XXG", "XXS",
            "GLO", "TDX", "NDX", "CNC", "OTH", "BAK"]

_allbkmap = {k: i for i, k in enumerate(_allbooks)} 

allbooks = [b.split("|")[0] for b in _bookslist.split()] # if b != "ZZZ|0"]
books = dict((b.split("|")[0], i) for i, b in enumerate(_bookslist.split()) if b[-2:] != "|0")
bookcodes = dict((b.split("|")[0], "{:02d}".format(i+1)) for i, b in enumerate(_bookslist.split()[:99]) if b[-2:] != "|0")
bookcodes.update(_endBkCodes)
chaps = dict(b.split("|") for b in _bookslist.split())
oneChbooks = [b.split("|")[0] for b in _bookslist.split() if b[-2:] == "|1"]

APP = 'ptxprint'

chgsHeader = """# This (changes.txt) file is for configuration-specific changes (which will not affect other saved configurations).
# Other generic project-wide changes can be specified in PrintDraftChanges.txt).
# Note that the 'inlcude' statement on the next line imports those (legacy/generic) project-wide changes.
include "../../../PrintDraftChanges.txt"
"""

_ = gettext.gettext
__file__ = os.path.abspath(__file__)

lang = None

def setup_i18n(i18nlang):
    global lang    
    localedir = os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__))), "mo")
    if i18nlang is not None:
        os.environ["LANG"] = i18nlang
        lang = i18nlang
    else:
        lang, enc = locale.getdefaultlocale(("LANG", "LANGUAGE"))
    enc = "UTF-8"
    if sys.platform.startswith('win'):
        from ctypes import cdll, windll
        from ctypes.util import find_msvcrt
        putenv('LANG', lang)
        msvcrt = find_msvcrt()
        msvcrtname = str(msvcrt).split('.')[0] if '.' in msvcrt else str(msvcrt)
        cdll.LoadLibrary(msvcrt)._putenv('LANG={}'.format(lang))        
        windll.kernel32.SetEnvironmentVariableW("LANG", lang)
        libintl = cdll.LoadLibrary("libintl-8.dll")
        libintl.bindtextdomain(APP, localedir)
        libintl.textdomain(APP)
        locale.setlocale(locale.LC_ALL, '')
    else:
        locale.setlocale(locale.LC_ALL, (lang, enc))
        locale.bindtextdomain(APP, localedir)
    # print(f"Lang = ({lang}, {enc}) from {i18nlang} and LANG={os.environ['LANG']}")
    gettext.bindtextdomain(APP, localedir=localedir)
    gettext.textdomain(APP)
    if "_" in lang:
        lang = lang[:lang.find("_")].lower()
    
def putenv(k, v):
    if sys.platform.startswith('win'):
        from ctypes import cdll
        from ctypes.util import find_msvcrt
        cdll.msvcrt._putenv('{}={}'.format(k, v))
    os.putenv(k, v)
    
def getlang():
    global lang
    return lang.replace('-','_').split('_')

def f_(s):
    frame = currentframe().f_back
    return eval("f'{}'".format(_(s)), frame.f_locals, frame.f_globals)

def refKey(r, info=""):
    m = re.match(r"^(\d?\D+)?\s*(\d*)\.?(\d*)(\S*?)(\s+.*)?$", r)
    if m:
        bkid = m.group(1) or ""
        return (books.get(bkid[:3], 99)+1, int(m.group(2) or 0), int(m.group(3) or 0), bkid[3:], info, m.group(4), m.group(5) or "")
    else:
        return (100, 0, 0, r, info, "", "")

def coltotex(s):
    vals = s[s.find("(")+1:-1].split(",")
    try:
        return "x"+"".join("{:02X}".format(int(x)) for x in vals[:3])
    except (ValueError, TypeError):
        return ""

def coltoonemax(s):
    try:
        if "," in s:
            return [float(x)/256. for x in s[s.find("(")+1:-1].split(",")]
        elif " " in s:
            return [float(x) for x in s.split(" ")]
        else:
            return [0.8, 0.8, 0.8]
    except (ValueError, TypeError):
        return [0.8, 0.8, 0.8]
        
def textocol(s):
    if s is None:
        vals = [0, 0, 0]
    elif s.startswith("x"):
        try:
            vals = [int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16)]
        except (ValueError, TypeError):
            vals = [0, 0, 0]
    elif " " in s:
        vals = [int(float(x) * 255) for x in s.split(" ")]
    elif "rgb" in s:
        vals = [float(x) for x in s[s.find("(")+1:-1].split(",")]
    else:
        try:
            v = int(s)
        except (ValueError, TypeError):
            v = 0
        vals = []
        while v:
            vals.append(v % 256)
            v //= 256
        vals.extend([0] * (3 - len(vals)))
    return "rgb({0},{1},{2})".format(*vals)

_wincodepages = {
    'cp950' : 'big5',
    'cp951' : 'big5hkscs',
    'cp20932': 'euc_jp',
    'cp954':  'euc_jp',
    'cp20866': 'ko18_r',
    'cp20936': 'gb2312',
    'cp10000': 'mac_roman',
    'cp10002': 'big5',
    'cp10006': 'mac_greek',
    'cp10007': 'mac_cyrillic',
    'cp10008': 'gb2312',
    'cp10029': 'mac_latin2',
    'cp10079': 'mac_iceland',
    'cp10081': 'mac_turkish',
    'cp1200':  'utf_16_le',
    'cp1201':  'utf_16_be',
    'cp12000': 'utf_32',
    'cp12001': 'utf_32_be',
    'cp65000': 'utf_7',
    'cp65001': 'utf_8'
}
_wincodepages.update({"cp{}".format(i+28590) : "iso8859_{}".format(i) for i in range(2, 17)})

def wincpaliases(enc):
    if enc in _wincodepages:
        return codecs.lookup(_wincodepages[enc])
    return None

codecs.register(wincpaliases)

def universalopen(fname, rewrite=False, cp=65001):
    """ Opens a file with the right codec from a small list and perhaps rewrites as utf-8 """
    encoding = "cp{}".format(cp) if str(cp) != "65001" else "utf-8"
    fh = open(fname, "r", encoding=encoding)
    try:
        fh.readline()
        fh.seek(0)
        return fh
    except ValueError:
        pass
    try:
        fh = open(fname, "r", encoding="utf-16")
        fh.readline()
        failed = False
    except UnicodeError:
        failed = True
    if failed:
        try:
            fh = open(fname, 'r', encoding="cp1252")
            fh.readline()
            failed = False
        except UnicodeError:
            return None
    fh.seek(0)
    if rewrite:
        dat = fh.readlines()
        fh.close()
        with open(fname, "w", encoding="utf-8") as fh:
            for d in dat:
                fh.write(d)
        fh = open(fname, "r", encoding="utf-8", errors="ignore")
    return fh

def print_traceback():
    traceback.print_stack()

if sys.platform == "linux":

    def openkey(path, doError=None):
        basepath = os.path.expanduser("~/.config/paratext/registry/LocalMachine/software")
        valuepath = os.path.join(basepath, path.lower(), "values.xml")
        if not os.path.exists(valuepath):
            return None
        doc = et.parse(valuepath)
        return doc

    def queryvalue(base, value):
        res = base.getroot().find('.//value[@name="{}"]'.format(value))
        if res is None:
            return ""
        else:
            return res.text

elif sys.platform == "win32":
    import winreg

    def openkey(path):
        try:
            k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\\" + path.replace("/", "\\"))
        except FileNotFoundError:
            k = None
        return k

    def queryvalue(base, value):
        return winreg.QueryValueEx(base, value)[0]

def pycodedir():
    return os.path.abspath(os.path.dirname(__file__))

def pt_bindir():
    res = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
    return res

def get_ptsettings():
    pt_settings = None
    ptob = openkey("Paratext/8")
    if ptob is None:
        tempstr = ("C:\\My Paratext {} Projects" if sys.platform == "win32" else
                    os.path.expanduser("~/Paratext{}Projects"))
        for v in ('9', '8'):
            path = tempstr.format(v)
            if os.path.exists(path):
                pt_settings = path
    else:
        pt_settings = queryvalue(ptob, 'Settings_Directory')
    return pt_settings

def get_gitver():
    res = check_output(["git", "describe", "--long"]).decode("utf-8", errors="ignore")
    return res.strip()

headermappings = {
    "First Reference":           r"\firstref",
    "Last Reference":            r"\lastref",
    "Reference Range":           r"\rangeref",
    "Page Number":               r"\pagenumber",
    "Book (\h)":                 r"\book",
    "Book Alt (\h1)":            r"\bookalt",
    "Time (HH:MM)":              r"\hrsmins",
    "Date (YYYY-MM-DD)":         r"\isodate",
    "-empty-":                   r"\empty"
}

def localhdrmappings():
    return {
        _("First Reference"):           r"\firstref",
        _("Last Reference"):            r"\lastref",
        _("Reference Range"):           r"\rangeref",
        _("Page Number"):               r"\pagenumber",
        _("Book (\h)"):                 r"\book",
        _("Book Alt (\h1)"):            r"\bookalt",
        _("Time (HH:MM)"):              r"\hrsmins",
        _("Date (YYYY-MM-DD)"):         r"\isodate",
        _("-empty-"):                   r"\empty"
    }

def local2globalhdr(s):
    revglobal = {v:k for k,v in headermappings.items()}
    mkr = localhdrmappings().get(s, None)
    if mkr is not None:
        return revglobal.get(mkr, mkr)
    else:
        return s

def global2localhdr(s):
    revlocal = {v:k for k,v in localhdrmappings().items()}
    mkr = headermappings.get(s, None)
    if mkr is not None:
        return revlocal.get(mkr, mkr)
    else:
        return s

def asfloat(v, d):
    try:
        return float(v)
    except (ValueError, TypeError):
        return d

def pluralstr(s, l):
    """CLDR plural rules"""
    if len(l) == 0:
        return ""
    elif len(l) == 1:
        return l[0]
    elif str(len(l)) in s:
        return s[str(len(l))].format(*l)
    if "end" in s:
        curr = s["end"].format(l[-2], l[-1])
        l = l[:-2]
    if "middle" in s:
        while len(l) > 1:
            curr = s["middle"].format(l.pop(), curr)
    if "start" in s:
        curr = s["start"].format(l[0], curr)
    elif "middle" in s:
        curr = s["middle"].format(l[0], curr)
    return curr

def multstr(template, lang, num, text, addon=""):
    if str(num) in template:
        res = template[str(num)].format(text)
    elif num > 1 and "mult" in template:
        res = template["mult"].format(text)
    else:
        res = ""
    if len(addon):
        res += " " + addon
    return res

def f2s(x, dp=3) :
    res = ("{:." + str(dp) + "f}").format(x)
    if res.endswith("." + ("0" * dp)) :
        return res[:-dp-1]
    res = re.sub(r"0*$", "", res)
    if res == "":
        res = "0"
    return res

def cachedData(filepath, fn):
    cfgdir = appdirs.user_cache_dir("ptxprint", "SIL")
    os.makedirs(cfgdir, exist_ok=True)
    cfgfilepath = os.path.join(cfgdir, os.path.basename("{}.pickle_{}.gz".format(filepath, DataVersion)))
    if os.path.exists(cfgfilepath):
        with contextlib.closing(gzip.open(cfgfilepath, "rb")) as inf:
            return pickle.load(inf)
    testbase = os.path.basename("{}.pickle".format(filepath))
    for l in os.listdir(cfgdir):
        if l.startswith(testbase):
            os.unlink(os.path.join(cfgdir, l))
    with open(filepath, "r", encoding="utf8") as inf:
        res = fn(inf)
    with contextlib.closing(gzip.open(cfgfilepath, "wb")) as outf:
        pickle.dump(res, outf)
    return res

def xdvigetpages(xdv):
    with open(xdv, "rb") as inf:
        inf.seek(-12, 2)
        dat = inf.read(12).rstrip(b"\xdf")
        postamble = unpack(">I", dat[-5:-1])[0]
        inf.seek(postamble, 0)
        dat = inf.read(5)
        lastpage = unpack(">I", dat[1:])[0]
        inf.seek(lastpage, 0)
        dat = inf.read(5)
        res = unpack(">I", dat[1:])[0]
    return res

varpaths = (
    ('prjdir', ('settings_dir', 'prjid')),
    ('settingsdir', ('settings_dir',)),
    ('workingdir', ('working_dir',)),
)

class Path(pathlib.Path):

    _flavour = pathlib._windows_flavour if os.name == "nt" else pathlib._posix_flavour

    @staticmethod
    def create_varlib(aView):
        res = {}
        for k, v in varpaths:
            res[k] = pathlib.Path(*[getattr(aView, x) for x in v])
        res['pdfassets'] = pathlib.Path(pycodedir(), 'PDFassets')
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

def brent(left, right, mid, fn, tol, log=None, maxiter=20):
    '''Brent method, see Numerical Recipes in C Ed. 2 p404'''
    GOLD = 0.3819660
    a = left
    b = right
    e = 0.
    x = w = v = mid
    fw = fv = fx = fn(mid)
    for i in range(maxiter):
        xm = 0.5 * (a + b)
        t1 = tol * abs(x) + 1e-8
        t2 = 2 * t1
        if abs(x - xm) <= t2 - 0.5 * (b - a):
            return x
        if abs(e) > t1:
            r = (x - w) * (fx - fv)
            q = (x - v) * (fx - fw)
            p = (x - v) * q - (x - w) * r
            q = 2 * (q - r)
            if q > 0:
                p = -p
            q = abs(q)
            etemp = e
            e = d
            if abs(p) > abs(0.5 * q * etemp) or p <= q * (a -x ) or p >= q * (b - x):
                e = a - x if x >= xm else b - x
                d = GOLD * e
            else:
                d = p / q
                u = x + d
                if u - a < t2 or b - u < t2:
                    return xm
        else:
            e = a - x if x >= xm else b - x
            d = GOLD * e
        u = x + d if abs(x) >= t1 else x + (t1 if d > 0. else -t1)
        fu = fn(u)
        if fu is None:
            fu = fx + d
        if log is not None:
            log.append((u, fu))
        if fu <= fx:
            if u >= x:
                a = x
            else:
                b = x
            v = w; w = x; x = u
            fv = fw; fw = fx; fx = fu
        else:
            if u < x:
                a = u
            else:
                b = u
            if fu <= fw or w == x:
                v = w; w = u
                fv = fw; fw = fu
            elif fu <= fv or v == x or v == w:
                v = u
                fv = fu
    return xm

# MLCS algorithm by Gareth Rees from https://codereview.stackexchange.com/questions/90194/multiple-longest-common-subsequence-another-algorithm

from bisect import bisect

def mlcs(strings):
    """Return a long common subsequence of the strings.
    Uses a greedy algorithm, so the result is not necessarily the
    longest common subsequence.

    """
    if not strings:
        raise ValueError("mlcs() argument is an empty sequence")
    strings = list(set(strings)) # deduplicate
    alphabet = set.intersection(*(set(s) for s in strings))

    # indexes[letter][i] is list of indexes of letter in strings[i].
    indexes = {letter:[[] for _ in strings] for letter in alphabet}
    for i, s in enumerate(strings):
        for j, letter in enumerate(s):
            if letter in alphabet:
                indexes[letter][i].append(j)

    # pos[i] is current position of search in strings[i].
    pos = [len(s) for s in strings]

    # Generate candidate positions for next step in search.
    def candidates():
        for letter, letter_indexes in indexes.items():
            distance, candidate = 0, []
            for ind, p in zip(letter_indexes, pos):
                i = bisect.bisect_right(ind, p - 1) - 1
                q = ind[i]
                if i < 0 or q > p - 1:
                    break
                candidate.append(q)
                distance += (p - q)**2
            else:
                yield distance, letter, candidate

    result = []
    while True:
        try:
            # Choose the closest candidate position, if any.
            _, letter, pos = min(candidates())
        except ValueError:
            return ''.join(reversed(result))
        result.append(letter)

def binsearch(arr, v, fn):
    low = 0
    high = len(arr) - 1
    mid = 0
    while low <= high:
        mid = (high + low) // 2
        res = fn(arr, mid, v)
        if res < 0:
            low = mid + 1
        elif res > 0:
            high = mid - 1
        else:
            return mid
    return mid
