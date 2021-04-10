#!/usr/bin/python3

"""ucd

This module contains the basic ucd information for every character in Unicode.

SYNOPSIS:

    from palaso.unicode.ucd import get_ucd
    print(get_ucd(0x0041, 'scx'))

If you want to use your own data file (perhaps the module data is stale) the use
the object interface:

    from palaso.unicode.ucd import UCD
    myucd = UCD(localfile="ucd.nounihan.flat.zip")   # localfile falls back to bundled data
    print(myucd.get(0x0041, 'scx'))
"""

import array, pickle
import xml.etree.ElementTree as et
import os, bz2, zipfile

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
           'InPC', 'vo', 'blk']
_fieldmap = dict((x, i) for i, x in enumerate(_fields))

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


class UCD(list):
    _singletemp = None
    def __new__(cls, localfile=None):
        if cls._singletemp is not None:
            return cls._singletemp
        else:
            cls._singletemp = list.__new__(cls)
        if localfile is None:
            localfile = os.path.join(os.path.dirname(__file__), "ucdata_pickle.bz2")
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
        if enums is None:
            enums = {}
            for k, v in self.enums.items():
                enums[k] = {x: i for i, x in enumerate(v)}
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

    def get(self, cp, key):
        """ Looks up a codepoint and returns the value for a given key. This
            includes mapping enums back to their strings"""
        v = self[cp]
        if v is None:
            raise KeyError("Undefined codepoint {:04X}".format(cp))
        if key == "na":
            return v[key].replace("#", "{:04X}".format(cp))
        return self.enumstr(key, v[key])

    def enumstr(self, key, v):
        """ Returns the string for an enum value given enum name and value """
        if key in self.enums:
            m = self.enums[key]
            return m[v] if v < len(m) else v
        return v

local_ucd = None
def get_ucd(cp, key):
    global local_ucd
    if local_ucd is None:
        local_ucd = UCD()
    try:
        return local_ucd.get(cp, key)
    except KeyError:
        return ""

if __name__ == '__main__':
    import sys, pickle
    from palaso.unicode.ucd import UCD, get_ucd
                
    if len(sys.argv) < 2:
        print(get_ucd(0x0041, "sc"))
        print(get_ucd(0x3400, "na"))
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
