
from ptxprint.xdv.xdv import XDViPositionedReader, opcodes
import logging

class XdvSpaceMeasure(XDViPositionedReader):

    def __init__(self, fname, parllocs, testfn=None, page=0, trackp=False):
        super().__init__(fname, page=page)
        self.parllocs = parllocs
        self.testfn = testfn
        self.liney = 0.
        self.textend = 0.
        self.currect = None
        self.pindex = page
        self.trackp = trackp
        logging.log(15, "Init new xdvspace")

    #def __next__(self):
    #    op = self.readval(1, uint=True)
    #    opc = opcodes[op]
    #    data = [self.readval((x if x>0 else -x), uint=x>0) for x in opc[1]]
    #    res = (op, opc, data)
    #    if self.trackp:
    #        logging.log(15, f"{opc[0]}[{op}] = {data}")
    #    return res

    def bop(self, opcode, parm, data):
        self.pindex = data[0]
        logging.log(15, f"New page {self.pindex}")
        return super().bop(opcode, parm, data)

    def _skip_xglyphs(self, opcode, parm, data):
        if parm == 0:
            tlen = self.readval(2)
            self.fpos += 2 * tlen
        width = self.readval(4)
        slen = self.readval(2)
        self.fpos += 10 * slen
        self.h += self.topt(width)
        return (parm, width, [], [], "")

    def xglyphs(self, opcode, parm, data):
        (p, r, _) = self.parllocs.findPos(self.pindex, self.h, self.v, xdv=True)
        fsize = self.fonts[self.currfont].points
        if self.currect is not None and r != self.currect:
            if self.currect.lines <= 1:
                self.currect.parwhite += (max(0, self.currect.xend - self.textend)) / self.oldfsize
            if self.trackp:
                logging.log(15, f"{self.currect.xend=} {self.textend=} {self.currect.parwhite=}")
            self.textend = 0.
            self.currect = r
            self.liney = self.v
            self.textend = self.h
        bstart = self.h
        otextend = self.textend
        if r is not None and (self.testfn is None or self.testfn(p, r)):
            if r == self.currect:
                if self.v - self.liney > p.baseline * 0.7:
                    r.parwhite += (max(0, r.xend - self.textend) + max(0, self.h - r.xstart)) / fsize
                    if self.trackp:
                        logging.log(15, f"{p.pid()}: {r.xend}-{self.textend} = {r.parwhite=}")
                elif self.h > self.textend and self.h > self.textend:
                    r.white += (self.h - self.textend) / fsize
                    r.nspaces += 1
            res = self._skip_xglyphs(opcode, parm, data)
            r.black += (self.h - bstart) / fsize
            self.textend = self.h
        else:
            res = self._skip_xglyphs(opcode, parm, data)
        if p is not None and self.trackp:
            logging.log(15, f"{p.pid()}: ({self.h}, {self.v}) from ({otextend}, {self.liney}) {r=} lines={r.lines if r is not None else 0}, width={self.h-bstart} -> {res}")
        elif self.trackp:
            logging.log(15, f"Unknown para at {self.h}, {self.v} from {self.liney}")
        oy = self.liney
        if self.liney - self.v < 0 or self.liney - self.v > 50:        # jump back a long way or only forward
            self.liney = self.v
        self.currect = r
        self.oldfsize = fsize
        return (parm, 0, [], [], "")        # we don't care about the actual data

