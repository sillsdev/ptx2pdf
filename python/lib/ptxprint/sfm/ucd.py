#!/usr/bin/python3

"""ucd

This module contains the basic ucd information for every character in Unicode.

SYNOPSIS:

    from palaso.unicode.ucd import get_ucd, norm_ucd
    print(get_ucd(0x0041, 'scx'))
    nfc = normal_ucd(astring, "NFC")

If you want to use your own data file (perhaps the module data is stale) the use
the object interface:

    from palaso.unicode.ucd import UCD
    myucd = UCD(localfile="ucd.nounihan.flat.zip")   # localfile falls back to bundled data
    print(myucd.get(0x0041, 'scx'))
"""

import array, pickle
import xml.etree.ElementTree as et
import os, bz2, zipfile
from ptxprint.utils import pycodedir

__all__ = ['get_ucd']
# Unicode data xml attributes
_binfieldnames = """AHex Alpha Bidi_C Bidi_M Cased CE CI Comp_Ex CWCF CWCM CWKCF CWL CWT CWU
    Dash Dep DI Dia Ext Gr_Base Gr_Ext Gr_Link Hex Hyphen IDC Ideo IDS IDSB
    IDST Join_C LOE Lower Math NChar OAlpha ODI OGr_Ext OIDC OIDS OLower OMath
    OUpper Pat_Syn Pat_WS PCM QMark Radical RI SD STerm Term UIdeo Upper VS
    WSpace XIDC XIDS XO_NFC XO_NFD XO_NFKC XO_NFKD"""
_binmap = dict((x, i) for i, x in enumerate(_binfieldnames.split()))
_enumfieldnames = """age blk sc scx bc bpt ccc dt ea gc GCB hst InPC InSC jg jt lb
    NFC_QC NFD_QC NFKC_QC NFKD_QC nt SB vo WB nv JSN"""
_cpfieldnames = """cf dm FC_NFKC lc NFKC_CF scf slc stc suc tc uc bmg bpb"""
_cpfields = set(_cpfieldnames.split())
_fields = ['_b0', 'age', 'na', 'JSN', 'gc', 'ccc', 'dt', 'dm', 'nt', 'nv',
           'bc', 'bpt', 'bpb', 'bmg', 'suc', 'slc', 'stc', 'uc', 'lc', 'tc',
           'scf', 'cf', 'jt', 'jg', 'ea', 'lb', 'sc', 'scx', 'NFKC_CF', 'FC_NFKC', 'InSC',
           'InPC', 'vo', 'blk', 'NFC_QC', 'NFD_QC', 'NFKC_QC', 'NFKD_QC']
_fieldmap = dict((x, i) for i, x in enumerate(_fields))

SBase = 0xAC00
LBase = 0x1100
VBase = 0x1161
TBase = 0x11A7
LCount = 19
VCount = 21
TCount = 28
NCount = 581 # VCount * TCount
SCount = 11039 # NCount * LCount
LBaseEnd = 0x1113
SBaseEnd = 0xD71F
TBaseEnd = 0x11C3

class _Codepoint(tuple):
    """Represents the complete information for a particular codepoint"""
    def __new__(cls, *a, **kw):
        if len(a) == 1 and len(a[0]) == len(_fields):
            return tuple.__new__(cls, a[0])
        if len(kw):
            a = [0] * len(_fields)
            for k, v in kw.items():
                if k in _binmap and v == "Y":
                    #i = _fieldmap['_b'+str(_binmap[k][0])]
                    a[_fieldmap['_b0']] += (1 << _binmap[k])
                elif k in _fieldmap:
                    a[_fieldmap[k]] = v
        return tuple.__new__(cls, a)

    def __getitem__(self, key):
        if key in _fieldmap and key != "_b0":
            return super(_Codepoint, self).__getitem__(_fieldmap[key])
        elif key in _binmap:
            return True if (super(_Codepoint, self).__getitem__(_fieldmap['_b0']) >> _binmap[key]) & 1 else False
        else:
            raise KeyError("Unknown key: {}".format(key))

class _Singleton:
    instances = {}
    def __call__(self, cls):
        inst = self.__class__.instances
        if cls not in inst:
            inst[cls] = cls()
        return inst[cls]

class UCD(list):
    _singletemp = None
    def __new__(cls, localfile=None):
        if cls._singletemp is not None:
            return cls._singletemp
        else:
            cls._singletemp = list.__new__(cls)
        if localfile is None:
            localfile = os.path.join(pycodedir(), "sfm", "ucdata_pickle.bz2")
        if not os.path.exists(localfile):
            res = cls._singletemp
        elif localfile.endswith(".bz2"):
            with bz2.open(localfile, "rb") as inf:
                res = pickle.load(inf)
        elif localfile.endswith(".pickle"):
            with open(localfile, "rb") as inf:
                res = pickle.load(inf)
        else:
            res = cls._singletemp
        cls._singletemp = None
        return res

    def __init__(self, localfile=None):
        if localfile is None:
            return
        elif localfile.endswith(".xml"):
            with open(localfile) as inf:
                enums = self._preproc(inf)
                inf.seek(0)
                self._loadxml(inf, enums=enums)
        elif localfile.endswith('.zip'):
            with zipfile.ZipFile(localfile, 'r') as z:
                firstf = z.namelist()[0]
                with z.open(firstf) as inf:
                    enums = self._preproc(inf)
                with z.open(firstf) as inf:
                    self._loadxml(inf, enums=enums)

    def _loadxml(self, fh, enums=None):
        self.comps = {}
        self.komps = {}
        if enums is None:
            enums = {}
            for k, v in self.enums.items():
                enums[k] = {x: i for i, x in enumerate(v)}
        dtcan = enums['dt']['can']
        for (ev, e) in et.iterparse(fh, events=['start']):
            if ev == 'start' and e.tag.endswith('char'):
                d = dict(e.attrib)
                if 'cp' in d:
                    firstcp = d.pop('cp')
                    lastcp = firstcp
                elif 'first-cp' in d:
                    firstcp = d.pop('first-cp')
                    lastcp = d.pop('last-cp')
                for n in _cpfields:
                    if n not in d or d[n] == "#":
                        d[n] = ""
                    d[n] = "".join(chr(int(x, 16)) for x in d[n].split())
                for n, v in enums.items():
                    if n in d:
                        d[n] = v[d[n]]
                dat = _Codepoint(**d)
                firsti = int(firstcp, 16)
                lasti = int(lastcp, 16)
                if lasti >= len(self):
                    self.extend([None] * (lasti - len(self) + 1))
                if d['dm'] != "":
                    s = d['dm']
                    if d['dt'] == dtcan:
                        self.comps[s] = chr(firsti)
                    else:
                        self.komps[s] = chr(firsti)
                for i in range(firsti, lasti+1):
                    self[i] = dat
        return self

    def _preproc(self, filename):
        enums = {}
        for e in _enumfieldnames.split():
            enums[e] = {}
        for (ev, e) in et.iterparse(filename, events=['start']):
            if e.tag.endswith('char'):
                for n, v in enums.items():
                    val = e.get(n, None)
                    if val is not None:
                        v.setdefault(val, len(v))
        self.enums = {}
        for k, v in enums.items():
            self.enums[k] = sorted(v.keys(), key=lambda x:v[x])
        return enums

    def get(self, cp, key, noenum=False):
        """ Looks up a codepoint and returns the value for a given key. This
            includes mapping enums back to their strings"""
        v = self[cp]
        if v is None:
            raise KeyError("Undefined codepoint {:04X}".format(cp))
        if key == "na":
            return v[key].replace("#", "{:04X}".format(cp))
        return v[key] if noenum else self.enumstr(key, v[key])

    def enumstr(self, key, v):
        """ Returns the string for an enum value given enum name and value """
        if key in self.enums:
            m = self.enums[key]
            return m[v] if v < len(m) else v
        return v

    def isnormalized(self, txt, normtype):
        # Treat MAYBE as NO
        if not len(txt):
            return True
        qck = normtype+'_QC'
        tv = self.enums[qck].index('N')
        def testc(v):
            return v[qck] == tv
        if not all(testc(self[ord(c)]) for c in txt):
            return False
        lastccc = self.get(ord(txt[0]), "ccc")
        for i in range(1, len(txt)):
            nextccc = self.get(ord(txt[i]), "ccc")
            if nextccc < lastccc and nextccc != 0:
                return False
            lastccc = nextccc
        return True

    def nfd(self, txt, compat=False):
        def jamox(c):
            i = ord(c) - SBase
            l = LBase + (i // NCount)
            v = VBase + (i % NCount) // TCount
            t = TBase + i % TCount
            return chr(l) + chr(v) + (chr(t) if t > TBase else "")
        if compat:
            def expand(c):
                if SBase <= c < SBaseEnd:
                    return jamox(c), False
                r = self.get(c, 'dm', chr(c))
                return r, r != c
        else:
            dtnone = self.enums["dt"].index("can")
            def expand(c):
                if SBase <= c < SBaseEnd:
                    return jamox(c), False
                elif self.get(c, "dt", noenum=True) == dtnone:
                    return self.get(c, "dm"), True
                else:
                    return chr(c), False
        def expandcode(c):
            s, decomp = expand(c)
            if decomp:
                return "".join(expandcode(ord(c)) for c in s)
            else:
                return s
        flat = list("".join(expandcode(ord(c)) for c in txt))

        # sort by ccc order
        ccs = [int(self.get(ord(c), "ccc")) for c in flat]
        for i in range(1, len(flat)):
            if ccs[i] < ccs[i-1] and ccs[i] > 0:
                j = i - 1
                while j > 0 and ccs[i] < ccs[j-1]:
                    j -= 1
                ccs.insert(j, ccs.pop(i))
                flat.insert(j, flat.pop(i))
        return "".join(flat)

    def _combjamo(self, curr):
        l = ord(curr[0]) - LBase
        v = ord(curr[1]) - VBase
        if len(curr) > 2:
            t = ord(curr[2]) - TBase
        else:
            t = 0
        code = SBase + (l * VCount + v) * TCount + t
        return chr(code)

    def nfc(self, txt, compat=False):
        flat = self.nfd(txt, compat=compat)
        comps = self.komps if compat else self.comps
        stack = []
        curr = ""
        res = []
        injamo = False
        for c in flat:
            if injamo and LBaseEnd <= ord(c) < TBaseEnd:
                curr += c
                continue
            elif LBase <= ord(c) < LBaseEnd:
                if injamo:
                    res.append(self._combjamo(curr))
                    curr = ""
                else:
                    res.append(curr + "".join(stack))
                stack.clear()
                curr = c
                injamo = True
                continue
            elif injamo:
                res.append(self._combjamo(curr))
                injamo = False
                curr = ""
                # fall through

            if curr + c in comps:
                curr = comps[curr+c]
            elif int(self.get(ord(c), 'ccc')) > 0:
                stack.append(c)
            else:
                res.append(curr + "".join(stack))
                stack.clear()
                curr = c
        res.append(curr + "".join(stack))
        return "".join(res)

    def normalize(self, txt, form="NFC"):
        form = form.upper()
        if self.isnormalized(txt, form):
            return txt
        if form == "NFC":
            return self.nfc(txt)
        elif form == "NFD":
            return self.nfd(txt)
        elif form == "NFKC":
            return self.nfc(txt, compat=True)
        elif form == "NFKD":
            return self.nfd(txt, compat=True)
        return txt
        

local_ucd = None
def _getucd():
    return _Singleton()(UCD)

def get_ucd(cp, key):
    lcd = _Singleton()(UCD)
    try:
        return lcd.get(cp, key)
    except KeyError:
        return ""

def normal_ucd(txt, mode="NFC"):
    return _Singleton()(UCD).normalize(txt, mode)

if __name__ == '__main__':
    import sys, pickle
    from ptxprint.sfm.ucd import UCD, get_ucd, normal_ucd
    from timeit import timeit

    def struni(s):
        return " ".join("{:04X}".format(ord(c)) for c in s)

    if len(sys.argv) < 2:
        print(get_ucd(0x0041, "sc"))
        print(get_ucd(0x3400, "na"))
        s = "\u212B\u0324"
        snfd = normal_ucd(s, "NFD")
        snfc = normal_ucd(s, "NFC")
        #print(timeit('snfc = normal_ucd("\u212B\u0324", "NFC")', setup='from ptxprint.sfm.ucd import normal_ucd; normal_ucd("A")'))
        print("orig={}, nfd={}, nfc={}".format(struni(s), struni(snfd), struni(snfc)))
    else:
        try:
            cp = int(sys.argv[1], 16)
        except ValueError:
            cp = None
        if cp is not None:
            print(get_ucd(cp, sys.argv[2]))
        else:
            ucdata = UCD(localfile=sys.argv[1])
            if sys.argv[2].endswith(".bz2"):
                outf = bz2.open(sys.argv[2], "wb")
            else:
                outf = open(sys.argv[2], "wb")
            pickle.dump(ucdata, outf)
            outf.close()
