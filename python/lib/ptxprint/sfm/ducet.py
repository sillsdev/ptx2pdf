#!/usr/bin/python3
import re, os
from struct import pack, unpack
import pickle, bz2
from ptxprint.sfm.ucd import normal_ucd

NONIGNORE = 0
BLANK = 1
SHIFT = 2
SHIFTTRIM = 3

zeroce = b"\00"*10


class DUCET(dict):
    def __init__(self, localfile=None):
        if localfile is None:
            localfile = os.path.join(os.path.dirname(__file__), "allkeys.txt")
        self.implicits = []
        with open(localfile) as inf:
            for l in inf.readlines():
                line = l.split("#", 1)[0].rstrip()
                if not line or line.startswith("@version"):
                    continue
                if line.startswith("@implicitweights "):
                    chrange, base = line[17:].split(";")
                    start, end = chrange.split("..")
                    basev = pack(">H", int(base, 16))
                    starti = int(start, 16)
                    for i in range(starti, int(end, 16)+1):
                        key = chr(i)
                        self[key] = basev + b"\00\00\00\00" + pack(">H", i - starti + 0x8000) + b"\00\00\00\00"
                    continue
                k, v = line.split(";", 1)
                key = "".join(chr(int(x, 16)) for x in k.rstrip().split())
                vals = []
                vs = re.findall(r"\[([.*])([0-9a-fA-F]{4})\.([0-9a-fA-F]{4})\.([0-9a-fA-F]{4})\]\s*", v.lstrip())
                for vm in vs:
                    vals.append(b"".join(pack(">H", int(x, 16)) for x in vm[1:]))
                self[key] = (b"".join(vals), vm[0][0] == '*')

    def __getitem__(self, k):
        if k in self:
            return super().get(k)
        elif len(k) == 1:
            return pack(">H", (ord(k) >> 15) + 0xFBC0) + b"\00\00\00\00"
        return None

    def _shifttest(self, val, variable, l4, folvar):
        zero = b"\00"*4
        if variable == BLANK:
            return zero
        if val[0] == 0 and val[1] == 0:     # ignorable
            if val[4] == 0 and val[5] == 0:
                return zero
            elif folvar:
                return zero
            elif variable == SHIFTTRIM:
                return zero
            else:
                return b"\00\00\377\377"    # FFFF
        elif folvar:
            return b"\00\00" + bytes(val[:2])
        elif variable == SHIFTTRIM:
            return zero
        else:
            return b"\00\00\377\377"
        

    def lookup(self, s, variable, folvar=False):
        val, var = self[s]
        l4 = pack(">L", ord(s[0])+0x1000000)
        if variable in (BLANK, SHIFT, SHIFTTRIM):
            if var:
                folvar = True
            res = []
            for x in range(0, len(val), 6):
                if var:
                    res.append(b"\00"*6 + self._shifttest(val[x:x+6], variable, l4, var))
                elif folvar and val[x:x+2] == (0, 0):
                    res.append(zeroce)
                else:
                    folvar = False
                    # not sure what l4 for should be SHIFT/SHIFTTRIM
                    res.append(bytes(val[x:x+6]) + (b"\00\00\377\377" if variable == SHIFT else b"\00"*4))
            return (b"".join(res), folvar)
        else:
            return (b"".join(bytes(val[x:x+6]) + l4 for x in range(0, len(val), 6)), False)

    def sortkey(self, txt, level=0, back=-1, variable=NONIGNORE):
        if not len(txt):
            return b""
        res = []
        colls = []
        currk = txt[0]
        txt = normal_ucd(txt, 'NFD')
        folvar = False
        for c in txt[1:]:
            if currk+c in self:
                currk += c
                continue
            (ce, folvar) = self.lookup(currk, variable, folvar)
            colls.append(ce)
            currk = c
        if currk:
            (ce, folvar) = self.lookup(currk, variable, folvar)
            colls.append(ce)
        for i in range(0, level or 5):
            if back == i:
                res.append(b"".join(bytes(a) for k in colls for a in reversed(zip(k[2*i::10], k[2*i+1::10])) if a != (0,0)))
            else:
                res.append(b"".join(bytes(a) for k in colls for a in zip(k[2*i::10], k[2*i+1::10]) if a != (0,0)))
        return b"\00\00".join(res)

local_ducet = None
def _get_local_ducet():
    global local_ducet
    if local_ducet is None:
        local_ducet = DUCET()
    return local_ducet

def get_sortkey(s, level=0):
    return _get_local_ducet().sortkey(s, level)

def strkey(key):
    return ".".join("{:04X}".format(*unpack(">H", e)) for e in (bytes(a) for a in zip(key[::2], key[1::2])))


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        ducet = _get_local_ducet()
        k = ducet.sortkey(re.sub(r"\\u([0-9A-Fa-f]{4,6})", lambda m:chr(int(m[1], 16)), sys.argv[1]), variable=SHIFTTRIM)
        print(strkey(k))
