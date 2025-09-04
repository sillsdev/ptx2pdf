#!/usr/bin/python3

# Reads xdvi files and outputs a version that can be diffed.

import argparse, os, sys
from struct import unpack
from ptxprint.font import TTFont

opcodes = [("setchar", [], i) for i in range(128)]
opcodes += [
    ("parmop", [1], "setcode"),
    ("parmop", [2], "setcode"),
    ("parmop", [3], "setcode"),
    ("parmop", [-4], "setcode"),
    ("multiparm", [-4]*2, "setrule"),
    ("parmop", [1], "setcode"),
    ("parmop", [2], "setcode"),
    ("parmop", [3], "setcode"),
    ("parmop", [-4], "setcode"),
    ("multiparm", [-4]*2, "setrule"),
    ("simple", [], "nop"),
    ("bop", [4]*11, "bop"),
    ("simple", [], "eop"),       # code 140
    ("push", [], "push"),
    ("pop", [], "pop"),
    ("parmdim", [-1], "right"),
    ("parmdim", [-2], "right"),
    ("parmdim", [-3], "right"),
    ("parmdim", [-4], "right"),
    ("dim", [], "w"),
    ("parmdim", [-1], "w"),
    ("parmdim", [-2], "w"),
    ("parmdim", [-3], "w"),         # code 150
    ("parmdim", [-4], "w"),
    ("dim", [], "x"),
    ("parmdim", [-1], "x"),
    ("parmdim", [-2], "x"),
    ("parmdim", [-3], "x"),
    ("parmdim", [-4], "x"),
    ("parmdim", [-1], "down"),
    ("parmdim", [-2], "down"),
    ("parmdim", [-3], "down"),
    ("parmdim", [-4], "down"),
    ("dim", [], "y"),
    ("parmdim", [-1], "y"),
    ("parmdim", [-2], "y"),
    ("parmdim", [-3], "y"),
    ("parmdim", [-4], "y"),
    ("dim", [], "z"),
    ("parmdim", [-1], "z"),
    ("parmdim", [-2], "z"),
    ("parmdim", [-3], "z"),
    ("parmdim", [-4], "z")]         # code 170
opcodes += [("font", [], i) for i in range(64)]
opcodes += [
    ("font", [1], None),
    ("font", [2], None),
    ("font", [3], None),
    ("font", [4], None),
    ("xxx", [1], None),
    ("xxx", [2], None),
    ("xxx", [3], None),
    ("xxx", [4], None),
    ("fontdef", [1, 4, 4, 4, 1, 1], None),
    ("fontdef", [2, 4, 4, 4, 1, 1], None),
    ("fontdef", [3, 4, 4, 4, 1, 1], None),
    ("fontdef", [4, 4, 4, 4, 1, 1], None),
    ("pre", [1, 4, 4, 4, 1], None),
    ("multiparm", [4]*6 + [2,2], "post"),
    ("multiparm", [4, 1], "postpost"),
    ("unknown", [], None),   # code 250
    ("xpic", [1, 4, 4, 4, 4, 4, 4, 2, 2], None),
    ("xfontdef", [4, 4, 2], None),
    ("xglyphs", [], 1),
    ("xglyphs", [], 0),
    ("parmop", [1], "direction")]

packings = ("bhxi", "BHxI")

class XDviType:
    def __init__(self, fname, diffable=False, glyphnames=False, outfile=None, positions=False):
        self.fonts = {}
        self.file = open(fname, "rb")
        if outfile is None:
            self.ofh = sys.stdout
        else:
            self.ofh = open(outfile, "w", encoding="utf-8")
        self.positions = positions
        self.stack = []
        self.diffable = diffable
        self.glyphnames = glyphnames
        self.pageno = 0
        self.dviratio = 1.
        self.h = 0      # all in dvi units
        self.v = 0
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.currfont = -1
        self.ttfonts = {}

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
        lastparm = None
        while lastparm != "postpost":
            op = self.readval(1, uint=True)
            opc = opcodes[op]
            data = [self.readval((x if x>0 else -x), uint=x>0) for x in opc[1]]
            lastparm = opc[2]
            getattr(self, opc[0])(op, lastparm, data)

    def asdimen(self, value):
        res = value * self.dviratio
        return "{:.2f}pt".format(res)

    def out(self, txt):
        pref = "pg[{}]".format(self.pageno)
        if self.positions:
            pref += "({:.1f},{:.1f})".format(self.h/65536.+72.27, self.v/65536.+72.27)
        self.ofh.write(pref + " " + txt + "\n")
        
    def setchar(self, opcode, parm, data):
        self.out("setchar({})".format(opcode))

    def multiparm(self, opcode, parm, data):
        self.out("{}({}) {}".format(parm, opcode, data))

    def parmop(self, opcode, parm, data):
        self.out("{}({}) [{}]".format(parm, opcode, data[0]))

    def parmdim(self, opcode, parm, data):
        if parm in "wxyz":
            setattr(self, parm, data[0])
        acc = None
        if parm in "wx" or parm == "right":
            acc = 'h'
        elif parm in "yz" or parm == "down":
            acc = 'v'
        if acc is not None:
            setattr(self, acc, getattr(self, acc) + data[0])
            self.out("{}[{}]({}={}) ({}:={})".format(parm, opcode, data[0], self.asdimen(data[0]),
                        acc, self.asdimen(getattr(self, acc))))

    def dim(self, opcode, parm, data):
        if parm in "wx":
            self.h += getattr(self, parm)
            self.out("{}[{}] (h={})".format(parm, opcode, self.asdimen(self.h)))
        elif parm in "yz":
            self.v += getattr(self, parm)
            self.out("{}[{}] (v={})".format(parm, opcode, self.asdimen(self.v)))

    def simple(self, opcode, parm, data):
        self.out("{}".format(parm))

    def push(self, opcode, parm, data):
        self.stack.append([getattr(self, x) for x in "hvwxyz"])
        self.out("{}".format(parm))

    def pop(self, opcode, parm, data):
        vs = self.stack.pop(-1)
        desc = []
        for i,x in enumerate("hvwxyz"):
            setattr(self, x, vs[i])
            desc.append("{}({}={})".format(x, vs[i], self.asdimen(vs[i])))
        self.out("{}({}): ".format(parm, opcode) + " ".join(desc))

    def bop(self, opcode, parm, data):
        self.pageno = data[0]
        self.out("{}({}) [{}]".format(parm, opcode, data[0]))
        for a in "hvwxyz":
            setattr(self, a, 0)

    def font(self, opcode, parm, data):
        if parm is not None:
            data = [parm]
        val = data[0]
        if val in self.fonts:
            self.out("font[{}]({}) [{:04x}]".format(opcode-171, opcode, self.fonts[data[0]][0]))
        self.currfont = val

    def xxx(self, opcode, parm, data):
        txt = self.readbytes(data[0])
        self.out('special({}) "{}"'.format(opcode, txt.decode("utf-8")))

    def fontdef(self, opcode, parm, data):
        (k, c, s, d, a, l) = data
        n = self.readbytes(a+l).decode("utf-8")
        # the k to c mapping may vary across 'identical' files
        res = "fontdef({}) checksum={:04x} sf={:f} name=\"{}\"".format(opcode, c, s / 1000. / d, n)
        self.fonts[k] = (c, n)

    def pre(self, opcode, parm, data):
        (i, n, d, m, k) = data
        x = self.readbytes(k)
        self.dviratio = m * n / d / 1000. / 10000 / 25.4 * 72.27      # map to pt not .0001mm
        res = "pre num={}, den={}, mag={} => ratio={}".format(n, d, m, 1./self.dviratio)
        if not self.diffable:
            res += " " + x.decode("utf-8")
        self.out(res)

    def xfontdef(self, opcode, parm, data):
        (k, points, flags) = data
        plen = self.readval(1, uint=True)
        font_name = self.readbytes(plen).decode("utf-8")
        if self.diffable:
            font_name = os.path.basename(font_name)
        ident = self.readval(4)
        color = self.readval(4) if flags & 0x200 else 0xFFFFFFFF
        if flags & 0x800:       # variations
            nvars = self.readval(2)
            variations = [self.readval(4) for i in range(nvars)]
        else:
            variations = []
        ext = self.readval(4) if flags & 0x1000 else 0
        slant = self.readval(4) if flags & 0x2000 else 0
        embolden = self.readval(4) if flags & 0x4000 else 0
        self.fonts[k]=(ident, font_name)
        self.out('xfontdef[{}]->{} "{}", size={:.2f}pt, flags={:04X}, color={:08X}, vars={}, ext={:.2f}%, slant={}, embolden={}'.format(
                k, ident, font_name, points / 65536., flags, color, variations, ext / 65536. * 100., slant, embolden))

    def _getfont(self, k):
        if k not in self.fonts:
            return None
        if k in self.ttfonts:
            return self.ttfonts[k]
        f = self.fonts[k][1]
        res = getattr(f, 'ttfont', None)
        if res is None:
            res = TTFont(None, style=None, filename=f)
            res.loadttfont()
            self.ttfonts[k] = res
        return res

    def xglyphs(self, opcode, parm, data):
        if parm == 0:
            tlen = self.readval(2)
            txt = self.readbytes(2*tlen).decode("utf-16be")
        else:
            txt = ""
        width = self.readval(4)
        slen = self.readval(2, uint=True)
        #if parm:
        pos = [(self.readval(4), self.readval(4)) for i in range(slen)]
        #else:
        #    pos = [(self.readval(4), 0) for i in range(slen)]
        glyphs = [self.readval(2) for i in range(slen)]
        if self.glyphnames:
            ttf = self._getfont(self.currfont)
            if ttf is not None:
                glyphs = [ttf.ttfont.getGlyphName(g) for g in glyphs]
        res = ["{}@({}={},{})".format(glyphs[i], pos[i][0], self.asdimen(pos[i][0]), pos[i][1]) for i in range(slen)]
        self.out('xglyphs[{:.1f}@{}]: "{}" {}'.format(width/65536., slen, txt, res))
        self.h += width

    def xpic(self, opcode, parm, data):
        box = data.pop(0)
        length = data.pop()
        pageno = data.pop()
        matrix = data[:]
        path = self.readbytes(length).decode("utf-8")
        self.out('xpic "{}"@{} pageno={}, box={}'.format(path, matrix, pageno, box))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile",help="Input xdvi file")
    parser.add_argument("-o","--outfile",help="Output to a file")
    parser.add_argument("-d","--diffable",action="store_true",help="Output a diffable structure")
    parser.add_argument("-n","--glyphnames",action="store_true",help="Output glyph names rather than ids")
    parser.add_argument("-p","--positions",action="store_true",help="Give x,y coordinates for each line")
    args = parser.parse_args()

    dviparser = XDviType(args.infile, diffable=args.diffable, glyphnames=args.glyphnames, outfile=args.outfile, positions=args.positions)
    dviparser.parse()

if __name__ ==  "__main__":
    main()

