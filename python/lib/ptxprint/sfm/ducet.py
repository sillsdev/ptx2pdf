#!/usr/bin/python3
import re, os
from struct import pack, unpack
import pickle, bz2

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
                    self.implicits.append((int(start, 16), int(end, 16), int(base, 16)))
                    continue
                k, v = line.split(";", 1)
                key = "".join(chr(int(x, 16)) for x in k.rstrip().split())
                vals = []
                vs = re.findall(r"\[([.*])([0-9a-fA-F]{4})\.([0-9a-fA-F]{4})\.([0-9a-fA-F]{4})\]\s*", v.lstrip())
                for vm in vs:
                    vals.append(b"".join(pack(">H", int(x, 16)) for x in vm[1:]))
                self[key] = b"".join(vals)

    def lookup(self, s):
        return self[s]

    def sortkey(self, txt, level=0):
        res = []
        colls = []
        currk = ""
        for c in txt:
            if currk+c in self:
                currk += c
                continue
            if not currk:
                continue
            colls.append(self.lookup(currk))
            currk = c
        if currk:
            colls.append(self.lookup(currk))
        for i in range(0, level or 3):
            res.append(b"".join(bytes(a) for k in colls for a in zip(k[2*i::6], k[2*i+1::6]) if a != (0,0)))
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
        k = ducet.sortkey(re.sub(r"\\u([0-9A-Fa-f]{4,6})", lambda m:chr(int(m[1], 16)), sys.argv[1]))
        print(strkey(k))
