#!/usr/bin/env python3

# Parses xdv
from struct import unpack, pack
class Font:
    def __init__(self, fname):
        self.name = fname

opcodes = [("setchar", [], i) for i in range(128)]
opcodes += [
    ("parmop", [1], "setcode"),
    ("parmop", [2], "setcode"),
    ("parmop", [3], "setcode"),
    ("parmop", [-4], "setcode"),
    ("multiparm", [-4]*2, "setrule"),
    ("parmop", [1], "putcode"),
    ("parmop", [2], "putcode"),
    ("parmop", [3], "putcode"),
    ("parmop", [-4], "putcode"),
    ("multiparm", [-4]*2, "setrule"),
    ("simple", [], "nop"),
    ("bop", [4]*11, "bop"),
    ("simple", [], "eop"),       # code 140
    ("push", [], "push"),
    ("pop", [], "pop"),
    ("parmop", [-1], "right"),
    ("parmop", [-2], "right"),
    ("parmop", [-3], "right"),
    ("parmop", [-4], "right"),
    ("simple", [], "w"),
    ("parmop", [-1], "w"),
    ("parmop", [-2], "w"),
    ("parmop", [-3], "w"),         # code 150
    ("parmop", [-4], "w"),
    ("simple", [], "x"),
    ("parmop", [-1], "x"),
    ("parmop", [-2], "x"),
    ("parmop", [-3], "x"),
    ("parmop", [-4], "x"),
    ("parmop", [-1], "down"),
    ("parmop", [-2], "down"),
    ("parmop", [-3], "down"),
    ("parmop", [-4], "down"),
    ("simple", [], "y"),
    ("parmop", [-1], "y"),
    ("parmop", [-2], "y"),
    ("parmop", [-3], "y"),
    ("parmop", [-4], "y"),
    ("simple", [], "z"),
    ("parmop", [-1], "z"),
    ("parmop", [-2], "z"),
    ("parmop", [-3], "z"),
    ("parmop", [-4], "z")]         # code 170
opcodes += [("font", [], i) for i in range(64)]
opcodes += [
    ("font", [1], None),
    ("font", [2], None),
    ("font", [3], None),
    ("font", [4], None),
    ("xxx", [1], None),
    ("xxx", [2], None),     # code 240
    ("xxx", [3], None),
    ("xxx", [4], None),
    ("fontdef", [1, 4, 4, 4, 1, 1], None),
    ("fontdef", [2, 4, 4, 4, 1, 1], None),
    ("fontdef", [3, 4, 4, 4, 1, 1], None),
    ("fontdef", [4, 4, 4, 4, 1, 1], None),
    ("pre", [1, 4, 4, 4, 1], None),
    ("multiparm", [4]*6 + [2,2], "post"),
    ("multiparm", [4, 1], "postpost"),
    ("simple", [], "reflect"),   # code 250     BEGIN_REFLECT
    ("simple", [], "unreflect"),
    ("xfontdef", [4, 4, 2], None),
    ("xglyphs", [], 1),
    ("xglyphs", [], 0),
    ("parmop", [1], "direction")]

packings = ("bhxi", "BHxI")

class XDViReader:
    def __init__(self, fname, diffable=False):
        self.fonts = {}
        self.fname = fname
        self.diffable = diffable
        self.pageno = 0
        self.file = None

    def __enter__(self):
        self.file = open(self.fname, "rb")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.file is not None:
            self.file.close()
            self.file = None

    def __iter__(self):
        return self

    def __next__(self):
        op = self.readval(1, uint=True)
        opc = opcodes[op]
        data = [self.readval((x if x>0 else -x), uint=x>0) for x in opc[1]]
        return (op, opc, data)

    def readbytes(self, num):
        return self.file.read(num)

    def readval(self, size, uint=False):
        d = self.readbytes(size)
        if size == 3:
            if uint:
                s = unpack(">"+packings[1][1]+packings[1][0], d)
                res = s[0] * 256 + s[1]
            else:
                s = unpack(">"+packings[0][1]+packings[1][0], d)
                res = s[0] * 256 + (s[1] if s[0] > 0 else -s[1])
        else:
            res = unpack(">"+packings[1 if uint else 0][size-1], d)[0]
        return res

    def parse(self):
        selfopen = False
        if self.file is None:
            selfopen = True
            self.__enter__()
        for (op, opc, data) in self:
            res = getattr(self, opc[0])(op, opc[2], data) 
            yield (op, res)
            if opc[2] == "postpost":
                break
        if selfopen:
            self.__exit__(None, None, None)
            self.file = None

    def out(self, txt):
        # print(("pg[{}] ".format(self.pageno) + txt).encode("utf-8"))
        pass

    def setchar(self, opcode, parm, data):
        if len(data):
            return (data[0],)
        else:
            return (opcode,)

    def multiparm(self, opcode, parm, data):
        return (parm, data)

    def parmop(self, opcode, parm, data):
        return (parm, data[0])

    def simple(self, opcode, parm, data):
        return (parm,)
    
    def push(self, opcode, parm, data):
        return parm, data

    def pop(self, opcode, parm, data):
        return parm, data

    def bop(self, opcode, parm, data):
        self.pageno = data[0]
        return data

    def font(self, opcode, parm, data):
        if parm is not None:
            data = [parm]
        self.currfont = data[0]
        return (data[0],)

    def xxx(self, opcode, parm, data):
        txt = self.readbytes(data[0])
        return (txt.decode("utf-8"),)

    def fontdef(self, opcode, parm, data):
        (k, c, s, d, a, l) = data
        n = self.readbytes(a+l).decode("utf-8")
        font = Font(n)
        font.size = self.mag * s / 1000. / d if d != 0 else 0
        font.checksum = c
        self.fonts[k] = font
        return (k, c, s, d, a, l, n)

    def pre(self, opcode, parm, data):
        (i, n, d, m, k) = data
        x = self.readbytes(k)
        self.mag = m
        self.denom = d
        # self.out("pre num={}, den={}, mag={} {}".format(n, d, m, x))
        # the k to c mapping may vary across 'identical' files
        # self.out("fontdef({}) checksum={:04x} sf={:f} name=\"{}\"".format(opcode, c, s / 1000. / d, n))
        return (i, n, d, m, x) 

    def xfontdef(self, opcode, parm, data):
        (k, points, flags) = data
        plen = self.readval(1, uint=True)
        font_name = self.readbytes(plen).decode("utf-8")
        if self.diffable:
            font_name = os.path.basename(font_name)
        font = Font(font_name)
        font.points = points
        font.ident = self.readval(4)
        font.color = self.readval(4) if flags & 0x200 else 0xFFFFFFFF
        if flags & 0x800:       # variations
            nvars = self.readval(2)
            font.variations = [self.readval(4) for i in range(nvars)]
        else:
            font.variations = []
        font.ext = self.readval(4) if flags & 0x1000 else 0
        font.slant = self.readval(4) if flags & 0x2000 else 0
        font.embolden = self.readval(4) if flags & 0x4000 else 0
        self.fonts[k]=font
        return (k, font)
        # self.out('xfontdef[{}] "{}", size={}, flags={:04X}, color={:08X}, vars={}, ext={}, slant={}, embolden={}'.format(
        #          ident, font_name, points, flags, color, variations, ext, slant, embolden))

    def xglyphs(self, opcode, parm, data):
        if parm == 0:
            tlen = self.readval(2)
            txt = self.readbytes(2*tlen).decode("utf-16be")
        else:
            txt = b""
        width = self.readval(4)
        slen = self.readval(2, uint=True)
        pos = [(self.readval(4), self.readval(4)) for i in range(slen)]
        glyphs = [self.readval(2) for i in range(slen)]
        return (parm, width, pos, glyphs, txt)
        # res = ["{}@({},{})".format(glyphs[i], *pos[i]) for i in range(slen)]
        # self.out("xglyphs: {}".format(res))

class XDViPositionedReader(XDViReader):
    """ Keeps track of where we are. Positions are in pt """
    def __init__(self, fname, diffable=False):
        super().__init__(fname, diffable=diffable)
        self.stack = []
        self.dviratio = 1.
        self.h = 0
        self.v = 0
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

    def topt(self, value):
        return value * self.dviratio

    def pre(self, opcode, parm, data):
        (i, n, d, m, x) = super().pre(opcode, parm, data)
        self.dviratio = m * n / d / 1000. / 10000 / 25.4 * 72.27      # map to pt not .0001mm
        return (i, n, d, m, x)

    def parmop(self, opcode, parm, data):
        prev_v = self.v
        if parm in "wxyz":
            setattr(self, parm, self.topt(data[0]))
        acc = None
        if parm in "wx" or parm == "right":
            acc = 'h'
        elif parm in "yz" or parm == "down":
            acc = 'v'
        if acc is not None:
            setattr(self, acc, getattr(self, acc) + self.topt(data[0]))
        return super().parmop(opcode, parm, data)

    def simple(self, opcode, parm, data):
        prev_v = self.v
        if parm in "wx":
            self.h += self.topt(getattr(self, parm))
        elif parm in "yz":            
            self.v += getattr(self, parm)
            # note: this was the problem, it converted self.y to points before adding (y is already in points)
        return super().simple(opcode, parm, data)

    def push(self, opcode, parm, data):
        self.stack.append([getattr(self, x) for x in "hvwxyz"])
        return super().push(opcode, parm, data)

    def pop(self, opcode, parm, data):
        vs = self.stack.pop(-1)
        desc = []
        for i,x in enumerate("hvwxyz"):
            setattr(self, x, vs[i])
        return super().pop(opcode, parm, data)

    def bop(self, opcode, parm, data):
        for a in "hvwxyz":
            setattr(self, a, 72.27 if a in "hv" else 0.)
        return (opcode, parm, data)

    def xfontdef(self, opcode, parm, data):
        k, font = super().xfontdef(opcode, parm, data)
        font.points = self.topt(font.points)
        return (k, font)

    def xglyphs(self, opcode, parm, data):
        (parm, width, pos, glyphs, txt) = super().xglyphs(opcode, parm, data)
        self.h += self.topt(width)
        return (parm, width, pos, glyphs, txt)



class XDViWriter:
    def __init__(self, fname):
        self.fname = fname
        self.outf = open(fname, "wb")
        self.lastbop = 0xFFFFFFFF

    def outbytes(self, b):
        self.outf.write(b)

    def outval(self, size, val, uint=False):
        if size == 3:
            if uint:
                d = pack(">"+packings[1][1]+packings[1][0], val // 256, val & 255)
            else:
                d = pack(">"+packings[0][1]+packings[1][0], -(-val // 256) if val < 0 else val // 256, 
                                                            (-val & 255) if val < 0 else (val & 255))
        else:
            d = pack(">"+packings[1 if uint else 0][size-1], val)
        self.outf.write(d)

    def outopcode(self, opcode):
        self.outval(1, opcode, uint=True)

    def outop(self, opcode, data):
        opc = opcodes[opcode]
        self.outopcode(opcode)
        for x, d in zip(opc[1], data):
            self.outval((x if x > 0 else -x), d, uint=x>0)

    def finish(self):
        l = self.outf.tell() % 4
        if l == 0:
            extra = 4
        else:
            extra = 8 - l
        self.outbytes(b"\xDF"*extra)
        self.outf.close()
        

    def setchar(self, opcode, char):
        if char < 129:
            self.outop(char, [])
        else:
            self.outop(opcode, [char])

    def multiparm(self, opcode, parm, *data):
        if parm == "post":
            self.postpos = self.outf.tell()
            data[0][0] = self.lastbop
        if parm == "postpost":
            data[0][0] = self.postpos
        self.outop(opcode, data[0])

    def parmop(self, opcode, parm, val):
        self.outop(opcode, [val])

    def simple(self, opcode, parm):
        self.outop(opcode, [])

    def bop(self, opcode, pageno, *data):
        res = list(data)
        res[-1] = self.lastbop
        self.lastbop = self.outf.tell()
        self.outop(opcode, [pageno] + res)

    def font(self, opcode, fontnum):
        if fontnum < 64:
            opcode = fontnum + 171
            self.outop(opcode, [])
            return
        elif fontnum < 0x100:
            opcode = 235
        elif fontnum < 0x10000:
            opcode = 236
        elif fontnum < 0x1000000:
            opcode = 237
        else:
            opcode = 238
        self.outop(opcode, [fontnum])

    def xxx(self, opcode, txt):
        data = txt.encode("utf-8")
        if len(data) < 0x100:
            opcode = 239
        elif len(data) < 0x10000:
            opcode = 240
        elif len(data) < 0x1000000:
            opcode = 241
        else:
            opcode = 242
        self.outop(opcode, [len(data)])
        self.outbytes(data)

    def fontdef(self, opcode, k, c, s, d, a, l, n):
        self.outop(opcode, [k, c, s, d, a, l])
        self.outbytes(n.encode("utf-8"))

    def pre(self, opcode, i, n, d, m, x):
        self.outop(opcode, [i, n, d, m, len(x)])
        self.outbytes(x)

    def xfontdef(self, opcode, k, font):
        flags = 0
        flags |= 0x200 if font.color != 0xFFFFFFFF else 0
        flags |= 0x800 if len(font.variations) else 0
        flags |= 0x1000 if font.ext else 0
        flags |= 0x2000 if font.slant else 0
        flags |= 0x4000 if font.embolden else 0
        self.outop(opcode, [k, font.points, flags])
        name = font.name.encode("utf-8")
        self.outval(1, len(name), uint=True)
        self.outbytes(name)
        self.outval(4, font.ident)
        if flags & 0x200:
            self.outval(4, font.color)
        if flags & 0x800:
            self.outval(2, len(font.variations))
            for v in self.variations:
                self.outval(4, v)
        if flags & 0x1000:
            self.outval(4, font.ext)
        if flags & 0x2000:
            self.outval(4, font.slant)
        if flags & 0x4000:
            self.outval(4, font.embolden)

    def xglyphs(self, opcode, parm, width, pos, glyphs, txt):
        self.outopcode(253 if parm else 254)
        if parm == 0:
            txtb = txt.encode("utf-16be")
            tlen = len(txtb)
            self.outval(2, tlen // 2)
            self.outbytes(txtb)
        self.outval(4, width)
        slen = len(glyphs)
        self.outval(2, slen, uint=True)
        for p in pos:
            self.outval(4, p[0])
            self.outval(4, p[1])
        for g in glyphs:
            self.outval(2, g)


class XDViFilter:
    def __init__(self, rdr, wrtr):
        self.rdr = rdr
        self.wrtr = wrtr

    def process(self):
        for (opcode, data) in self.rdr.parse():
            opc = opcodes[opcode]
            if hasattr(self, opc[0]):
                data = getattr(self, opc[0])(opcode, *data)
                if data is None:            # allow filter to stop output for this op
                    continue
            getattr(self.wrtr, opc[0])(opcode, *data)


def main():
    import sys

    if len(sys.argv) < 3:
        print ("xdv.py infile outfile\nDoes full copy to an identical file")
    reader = XDViReader(sys.argv[1])
    writer = XDViWriter(sys.argv[2])
    filt = XDViFilter(reader, writer)
    filt.process()
    writer.finish()

if __name__ == "__main__":
    main()

