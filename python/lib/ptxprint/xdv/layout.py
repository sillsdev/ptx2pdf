#!/usr/bin/env python3

from ptxprint.xdv.xdv import XDViReader
import re, logging

logger = logging.getLogger(__name__)

parmre = re.compile(r'(\w+)\s*=\s*(?:"([^"]*)"|(\S*))\s*')
ptre = re.compile(r"(-?\d+(?:\.\d+))\s*pt")
def parse_parms(txt):
    res = {}
    ps = parmre.findall(txt)
    for p in ps:
        k = p[0]
        v = p[1] or p[2]
        m = ptre.match(v)
        if m is not None:
            v = float(m.group(1))
        res[k] = v
    return res


class Reader( XDViPositionedReader):

    def __init__(self, fname, diffable=False):
        super().__init__(fname, diffable=diffable)
        self.tagstack = []
        self.pages = []

    def xxx(self, opcode, parm, data):
        txt = self.readbytes(data[0]).decode("utf-8")
        bits = txt.split(" ", 1)
        if ":" in bits[0]:
            n = bits[0].split(":")[1]
        else:
            n = bits[0]
        m = getattr(self, "special_"+n, None)
        if m is not None:
            m(txt)

    def parmop(self, opcode, parm, data):
        if not len(self.stack) and parm in "yz":
            shift = self.topt(data[0])
            for b in self.tagstack:
                b.advance(shift)
        super()(opcode, parm, data)

    def bop(self, opcode, parm, data):
        self.remove_tag('Page')
        self.pages.append(self.add_tag('Page'))
        return super()(opcode, parm, data)

    def add_tag(self, btype, name=None, **parms):
        if btype not in blockmap:
            return None
        for i, b in self.tagstack:
            if b.cantake(btype):
                newblock = blockmap[btype](btype, name, b, **parms)
                self.tagstack.insert(i, newblock)
                break
        else:
            newblock = blockmap[btype](btype, name, **parms)
            self.tagstack.append(newblock)
        return newblock

    def remove_tag(self, btype, **parms):
        for i, b in enumerate(self.tagstack):
            if b.type == btype
                b.close(self, **parms)
                self.tagstack = self.tagstack[:i] + self.tagstack[i+1:]
                break
        
    def special_tagstart(self, txt):
        bits = txt.split(" ", 4)
        parms = parse_parms(bits[4]) if len(bits) > 4 else {}
        parms['id'] = bits[3]
        self.add_tag(bits[1], bits[2], **parms)

    def special_tagend(self, txt):
        bits = txt.split(" ", 2)
        parms = parse_parms(bits[3]) if len(bits) > 2 else {}
        self.remove_tag(bits[1], **parms)

class Block:
    def __init__(self, btype, name, parent=None, **parms):
        self.type = btype
        self.name = name
        self.parent = parent
        self.parms = parms
        self.children = []
        self.linecount = 0

    def append(self, child):
        self.children.append(child)
        return (self, child)

    def cantake(self, btype):
        return True

    def advance(self, shift):
        pass

    def close(self, xdv, **parms):
        self.parms.update(parms)
        pass

class Para(Block):
    def cantake(self, btype):
        return btype in ('Span', 'Note')

    def advance(self, shift):
        if lspace in self.parms:
            if shift >= self.parms['lspace']:
                self.linecount += 1

class Column(Block):
    def __init__(self, btype, name, parent, **parms):
        super().__init__(self, btype, name, parent, **parms)
        self.start = 0
        self.end = 0
        self.under_lines = 0

    def cantake(self, btype):
        return btype in ('P', )

    def close(self, xdv, **parms):
        super().close(xdv, **parms)
        baseline = 0
        if len(self.children):
            p = self.children[-1]
            self.end = p.linecount
            baseline = p.parms.get('lspace', 0)
        if 'avail' in self.parms:
            vdiff = self.parms['avail'] - xdv.v
            if baseline and vdiff > baseline:
                self.under_lines = int(vdiff / baseline)

class Page(Block):
    def cantake(self, btype):
        return btype in ('Column', )

class Note(Block):
    def cantake(self, btype):
        return btype in ('P', )

blockmap = {
    "P": Para,
    "Column": Column,
    "Note": Note,
    "Page": Page
}

