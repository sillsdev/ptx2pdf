
from ptxprint.xdv.xdv import XDViPositionedReader
import logging

class XdvSpaceMeasure(XDViPositionedReader):

    def __init__(self, fname, parllocs, testfn=None, page=0):
        super().__init__(fname, page=page)
        self.parllocs = parllocs
        self.testfn = testfn
        self.liney = 0.
        self.textend = 0.
        self.currect = None
        self.pindex = page
        logging.log(15, "Init new xdvspace")

    def bop(self, opcode, parm, data):
        self.pindex += 1
        logging.log(15, f"New page {self.pindex}")
        return super().bop(opcode, parm, data)

    def xglyphs(self, opcode, parm, data):
        (p, r, _) = self.parllocs.findPos(self.pindex, self.h, self.v, xdv=True)
        if r is not None and (self.testfn is not None or self.testfn(p, r)):
            if r == self.currect:
                if self.v - self.liney > 0 and  r.xend > self.textend:
                    r.white += r.xend - self.textend + (self.h - r.xstart)
                elif self.h > self.textend:
                    r.white += self.h - self.textend
            bstart = self.h
            res = super().xglyphs(opcode, parm, data)
            self.textend = self.h
            r.black += self.h - bstart
        else:
            res = super().xglyphs(opcode, parm, data)
        oy = self.liney
        if self.liney - self.v < 0 or self.liney - self.v > 50:        # jump back a long way or only forward
            self.liney = self.v
        self.currect = r
        return res

