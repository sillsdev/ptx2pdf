#!/usr/bin/env python3

from collections import namedtuple
from ptxprint.font import TTFont
from ptxprint.xdv.xdv import XDViFilter
from itertools import groupby

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
        self.currcolour = 0

    def font(self, opcode, fontnum)
        self.currfont = fontnum
        return [fontnum]

    def getfont(self, k):
        # Get a ptxprint.font.TTFont for the given font id
        pass

    def xxx(self, opcode, txt):
        txt = txt.strip()
        if not txt.lower().startswith("ptxp:"):
            return [txt]
        bits = txt.split(" ")
        if bits[0].lower() == "ptxp:diadeclare":
            if bits[2] == "rgb":
                dia = DiaSet(" ".join(bits[1:5]))
                start = 6
            if bits[2] == "cmyk":
                dia = DiaSet(" ".join(bits[1:6]))
                start = 7
            for i in range(start, len(bits)):
                if bits[i].lower().startswith("u+"):
                    diaset.adduni(int(bits[i][2:], 16))
                    continue
                try:
                    gid = int(bits[i])
                except ValueError, TypeError:
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
                self.alldias.setdefault(self.currfont, {})[did] = DiaInstance(self.currfont, diaset.colour, gids)
            self.currdias[did] = self.alldias[self.currfont][did]
            return None
        elif bits[0].lower() == "ptxp:diastop":
            did = 1 if len(bits) < 2 else bits[1]
            if did in self.currdias:
                del self.currdias[did]
            return None

    def xglyphs(self, parm, width, pos, glyphs):
        if not len(self.currdias) and not self.currcolour:
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
                colours.append(0)
        gorder = sort(range(len(glyphs)), key=lambda i:(colours[i] == self.currcolour, -colours[i], i))
        if colours[gorder[-1]] == self.currcolour:
            return (parm, width, pos, glyphs)
        res = []
        for col, grange in groupby(gorder, key=lambda x:colours[x]):
            if len(res):
                self.setColour(col)
            
        


