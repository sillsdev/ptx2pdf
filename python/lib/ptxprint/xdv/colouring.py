#!/usr/bin/env python3

from collections import namedtuple
from ptxprint.font import TTFont
from ptxprint.xdv.xdv import XDViReader, XDViWriter, XDViFilter
from itertools import groupby
import logging

logger = logging.getLogger(__name__)

class DiaSet:
    def __init__(self, colour):
        self.colour = colour
        self.gids = set()
        self.unicodes = set()
        self.gnames = set()

    def adduni(self, uni):
        self.unicodes.add(uni)

    def addgid(self, gid):
        self.gids.add(gid)

    def addgname(self, gname):
        self.gnames.add(gname)

DiaInstance = namedtuple("DiaInstance", ["font", "colour", "gids"])

class PTXPxdviFilter(XDViFilter):
    def __init__(self, rdr, wrtr):
        super().__init__(rdr, wrtr)
        self.diasets = {}
        self.alldias = {}
        self.currdias = {}
        self.currfont = -1
        self.currcolour = [0]

    def font(self, opcode, fontnum):
        self.currfont = fontnum
        return [fontnum]

    def getfont(self, k):
        f = self.rdr.fonts[k]
        res = getattr(f, 'ttfont', None)
        if res is None:
            res = TTFont(None, style=None, filename=f.name)
            f.ttfont = res
        return res

    def xxx(self, opcode, txt):
        txt = txt.strip()
        if not txt.lower().startswith("ptxp:"):
            return [txt]
        bits = txt.split(" ")
        if bits[0].lower() == "ptxp:diadeclare":
            if bits[2] == "rgb":
                diaset = DiaSet(bits[2:6])
                start = 6
            elif bits[2] == "cmyk":
                diaset = DiaSet(bits[2:7])
                start = 7
            for i in range(start, len(bits)):
                if bits[i].lower().startswith("u+"):
                    diaset.adduni(int(bits[i][2:], 16))
                    continue
                try:
                    gid = int(bits[i])
                except (ValueError, TypeError):
                    gid = None
                if gid is not None:
                    diaset.addgid(gid)
                    continue
                diaset.addgname(bits[i].lstrip("/"))
            self.diasets[bits[1]] = diaset
            return None
        elif bits[0].lower() == "ptxp:diastart":
            did = 1 if len(bits) < 2 else bits[1]
            if self.currfont not in self.alldias or did not in self.alldias[self.currfont]:
                diaset = self.diasets.get(did, None)
                font = self.getfont(self.currfont)
                if font is None or diaset is None:
                    return None
                gids = font.getgids(diaset.unicodes, diaset.gnames, diaset.gids)
                logger.debug(f"diastart(f{did}): f{gids=}")
                self.alldias.setdefault(self.currfont, {})[did] = DiaInstance(self.currfont, diaset.colour, gids)
            self.currdias[did] = self.alldias[self.currfont][did]
            return None
        elif bits[0].lower() == "ptxp:diastop":
            did = 1 if len(bits) < 2 else bits[1]
            if did in self.currdias:
                del self.currdias[did]
            return None

    def _setColour(self, col):
        if col == self.currcolour:
            return
        txts = []
        if self.currcolour != [0]:
            txts.append("color pop")
        if col != [0]:
            txts.append("color push " + " ".join(col))
        for t in txts:
            self.wrtr.xxx(0, t)
        self.currcolour = col
        

    def xglyphs(self, opcode, parm, width, pos, glyphs):
        if not len(self.currdias) and self.currcolour == [0]:
            return (parm, width, pos, glyphs)
        colours = []
        for i, g in enumerate(glyphs):
            for v in self.currdias.values():
                if v.font != self.currfont:
                    continue
                if g in v.gids:
                    colours.append(v.colour)
                    break
            else:
                colours.append([0])
        gorder = sorted(range(len(glyphs)), key=lambda i:(colours[i] == self.currcolour, colours[i], i))
        if colours[gorder[0]] == self.currcolour:
            return (parm, width, pos, glyphs)
        res = []
        groups = [(a[0], list(a[1])) for a in groupby(gorder, key=lambda x:colours[x])]
        for i, (col, grange) in enumerate(groups):
            ids = list(grange)
            self._setColour(col)
            poso = [pos[j] for j in grange]
            glypho = [glyphs[j] for j in grange]
            self.wrtr.xglyphs(opcode, parm, width if i == len(groups) - 1 else 0, poso, glypho)
        return None

def procxdv(inxdv, outxdv):
    reader = XDViReader(inxdv)
    writer = XDViWriter(outxdv)
    filt = PTXPxdviFilter(reader, writer)
    filt.process()
    writer.finish()

def main():
    import sys

    if len(sys.argv) < 3:
        print ("xdv.py infile outfile\nDoes full copy to an identical file")
    proc(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
