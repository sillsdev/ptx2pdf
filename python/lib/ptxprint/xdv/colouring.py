#!/usr/bin/env python3

from collections import namedtuple
from ptxprint.font import TTFont
from ptxprint.xdv.xdv import XDViReader, XDViWriter, XDViFilter
from itertools import groupby
import logging

logger = logging.getLogger(__name__)

class DiaSet:
    def __init__(self):
        self.colour = [0]
        self.gids = set()
        self.unicodes = set()
        self.gnames = set()

    def set_colour(self, colour):
        self.colour = colour

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
        self.currdias = set()
        self.currfont = -1
        self.currcolour = [0]

    def _getfont(self, k):
        f = self.rdr.fonts[k]
        res = getattr(f, 'ttfont', None)
        if res is None:
            res = TTFont(None, style=None, filename=f.name)
            f.ttfont = res
        return res

    def _ensurediaset(self, did):
        if did not in self.diasets:
            self.diasets[did] = DiaSet()
        return self.diasets[did]

    def xxx(self, opcode, txt):
        txt = txt.strip()
        if not txt.lower().startswith("ptxp:"):
            return [txt]
        bits = txt.split(" ")
        cmd = bits[0].lower()
        if cmd == "ptxp:diacolour":
            ds = self._ensurediaset(bits[1])
            if bits[2] == "rgb":
                diaset = ds.set_colour(bits[2:6])
            elif bits[2] == "cmyk":
                diaset = ds.set_colour(bits[2:7])
            return None
        elif cmd == "ptxp:diaglyphs":
            ds = self._ensurediaset(bits[1])
            for i in range(2, len(bits)):
                if bits[i].lower().startswith("u+"):
                    if "-" in bits[i]:
                        (start, end) = bits[i][2:].split("-")
                    else:
                        start = bits[i][2:]
                        end = start
                    try:
                        us = int(start, 16)
                        ue = int(end, 16) + 1
                    except ValueError:
                        continue
                    for i in range(us, ue):
                        ds.adduni(i)
                    continue
                try:
                    gid = int(bits[i])
                except (ValueError, TypeError):
                    gid = None
                if gid is not None:
                    ds.addgid(gid)
                    continue
                ds.addgname(bits[i].lstrip("/"))
            return None
        elif bits[0].lower() == "ptxp:diastart":
            logger.debug(f"{bits}")
            self.currdias.update(bits[1:])
            self.font(None, self.currfont)      # trigger glyph analysis
            return None
        elif bits[0].lower() == "ptxp:diastop":
            logger.debug(f"{bits}")
            for did in bits[1:]:
                self.currdias.discard(did)
            return None

    def font(self, opcode, fontnum):
        self.currfont = fontnum
        font = self._getfont(self.currfont)
        if font is None:
            return [fontnum]
        for did in self.currdias:
            if self.currfont not in self.alldias or did not in self.alldias[self.currfont]:
                diaset = self.diasets.get(did, None)
                if diaset is None:
                    continue
                gids = font.getgids(diaset.unicodes, diaset.gnames, diaset.gids)
                self.alldias.setdefault(self.currfont, {})[did] = DiaInstance(self.currfont, diaset.colour, gids)
        return [fontnum]

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
            for k in self.currdias:
                v = self.alldias.get(self.currfont, {}).get(k, None)
                if v is None or v.font != self.currfont:
                    continue
                if g in v.gids:
                    colours.append(v.colour)
                    break
            else:
                colours.append([0])
        gorder = sorted(range(len(glyphs)), key=lambda i:(colours[i] == self.currcolour, colours[i], i))
        logger.debug(f"xglyphs {self.currfont} for {self.currdias} is {[colours[g] for g in gorder]}")
        if not any(colours[g] != self.currcolour for g in gorder):
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
