#!/usr/bin/python3
import re, os
from struct import pack, unpack
import pickle, bz2, copy
from ptxprint.sfm.ucd import normal_ucd

NONIGNORE = 0
BLANK = 1
SHIFT = 2
SHIFTTRIM = 3

zeroce = b"\00"*10


class DUCET(dict):
    def __init__(self, localfile=None, basedict=None):
        if basedict is not None:
            super().__init__(basedict)
        if localfile is None:
            localfile = os.path.join(os.path.dirname(__file__), "allkeys.txt")
        self.implicits = []
        self.specials = {   'first tertiary ignorable': (0, 0, 0),
                            'last tertiary ignorable': (0, 0, 0),
                            'first secondary ignorable': (0, 0, 0),
                            'last secondary ignorable': (0, 0, 0x1F),   # not really, but highest tertiary value
                            'first primary ignorable': (0, 0x20, 0),
                            'last primary ignorable': (0, 0, 0),    # calculated
                            'first variable': (0x0200, 0, 0),
                            'last variable': (0, 0, 0),     # calculated
                            'first regular': (0xFFFF, 0, 0),    # calculated
                            'last regular': (0, 0, 0),      # calculated
                            'last implicit': (0xFCC1, 0, 0),     # 0xFBC0 + 0x10FFFF >> 15
                            'first trailing': (0xFCC2, 0, 0),   # next after last implicit
                            'last trailing': (0xFFFC, 0, 0)
                        }
        self.parameters = { 'alternate': 'non-ignorable',
                            'maxVariable': 'punct',
                            'normalization': 'off',
                            'strength': '3',
                            'backwards': '0',
                            'caseLevel': 'off',
                            'caseFirst': 'off',
                            'numericOrdering': 'off',
                            'hiraganaQ': 'off',
                            'supressContractions': '',
                            'optimize': '',
                            'reorder': ''
                          }
        if basedict is not None:
            return
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
                self[key] = (b"".join(vals), vs[0][0] == '*')
                ce = tuple(int(x, 16) for x in vs[0][1:])
                if vs[0][0] == "*" and ce > self.specials['last variable']:
                    self.specials['last variable'] = ce
                if vs[0][0] == "." and ce < self.specials['first regular']:
                    self.specials['first regular'] = ce
                if ce[0] < 0xFFF0 and ce > self.specials['last regular']:
                    self.specials['last regular'] = ce
                if ce[0] == 0 and ce[1] > self.specials['last primary ignorable'][1]:
                    self.specials['last primary ignorable'] = (0, ce[1], 0)
                     
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
        txt = normal_ucd(txt, 'NFD')
        currk = txt[0]
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

def _splitkey(key):
    res = [[]]
    for i in range(0, len(key), 2):
        if key[i:i+2] == b"\00\00":
            res.append([])
        else:
            res[-1].append(key[i:i+2])
    return [b"".join(r) for r in res]

def _makekey(bits):
    maxe = max(len(x) for x in bits)
    res = b"".join(b"".join(bits[i][j:j+2] if j < len(bits[i]) else b"\00\00" for i in range(3)) \
                        for j in range(0, maxe, 2))
    return res

def tailored(tailoring, ducet=None):
    if ducet is None:
        ducet = _get_local_ducet()
    res = copy.copy(ducet)
    expressions = tailoring.split('&')
    for exp in expressions:
        e = exp.strip()
        if not len(e):
            continue
        bits = re.split(r"(<+|=)", e)
        lastbase = None
        lastcmp = 0
        if len(bits) & 1 != 0:
            bits += [""]
        before = 0
        for b, o in zip(bits[::2], bits[1::2]):
            base = b.strip().replace('\\', '')
            nextcmp = 4 if o == "=" else len(o)
            done = False
            end = 0
            for m in re.finditer(r"\s*\[\s*(.*?)\s*\]\s*", base):
                s = m.group(1)
                end = m.end()
                a = re.match(r"before\s+(\d)", s)
                if a:
                    before = int(a.group(1))            # We need to do something with this
                elif s in res.specials:
                    if lastbase is None:
                        lastbase = b"".join(pack(">H", x) for x in res.specials[s])
                        done = True
                else:
                    a = re.match(r"(\S+)\s+(\S+)", s)
                    if a and a.group(1) in res.parameters:
                        res.parameters[a.group(1)] = a.group(2)
            if done:
                lastcmp = nextcmp
                continue
            base = base[end:].strip()
            (newkey, exp) = base.split("/",1) if "/" in base else (base, "")
            if lastbase is not None:
                basebits = _splitkey(lastbase)[:3]
                if lastcmp == 4:
                    pass
                for i, startk in enumerate(('first trailing', 'last primary ignorable', 'last secondary ignorable')):
                    start = res.specials[startk]
                    if lastcmp == i + 1:
                        lastp = unpack(">H", basebits[i][-2:])[0]
                        if (lastp > start[i]):
                            basebits[i] = basebits[i][:-2] + pack(">H", lastp+1)
                        else:
                            basebits[i] += pack(">H", start[i]+1)
                        break
                if exp:
                    expbits = _splitkey(res.sortkey(exp))[:3]
                    newbits = [basebits[i] + expbits[i] for i in range(len(basebits))]
                else:
                    newbits = basebits
                basekey = _makekey(newbits)
                res[newkey] = (basekey, False)
                for i in range(2,len(newkey)):
                    if newkey[0:i] not in res:
                        a = _splitkey(res.sortkey(newkey[0:i-1]))[:3]
                        b = _splitkey(res.sortkey(newkey[i-1]))[:3]
                        nkey = [a[i] + b[i] for i in range(3)]
                        res[newkey[0:i]] = _makekey(nkey)
                # print("{}={}".format(repr(newkey), strkey(res.sortkey(newkey))))
                lastbase = b"\00\00".join(basebits)
            else:
                lastbase = res.sortkey(newkey)
            lastcmp = nextcmp
    return res

local_ducet = None
def _get_local_ducet():
    global local_ducet
    if local_ducet is None:
        local_ducet = DUCET()
    return local_ducet

def get_sortkey(s, level=0, variable=NONIGNORE, ducet=None):
    if ducet is None:
        ducet = _get_local_ducet()
    return ducet.sortkey(s, level, variable=variable)

def strkey(key):
    return ".".join("{:04X}".format(*unpack(">H", e)) for e in (bytes(a) for a in zip(key[::2], key[1::2])))


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        ducet = _get_local_ducet()
        k = ducet.sortkey(re.sub(r"\\u([0-9A-Fa-f]{4,6})", lambda m:chr(int(m[1], 16)), sys.argv[1]), variable=SHIFTTRIM)
        # print(strkey(k))
        t = tailored(ducet, "&C<cs<<<cS<<<Cs<<<CS &cs<<<ccs/cs<<<ccS/cS<<<cCs/Cs<<<cCS/CS")

