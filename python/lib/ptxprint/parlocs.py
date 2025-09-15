import os, re, ctypes, math, heapq
import logging
from dataclasses import dataclass, InitVar, field
from ptxprint.utils import refSort
from ptxprint.xdv.spacing_oddities import Line, Rivers
from typing import Tuple

logger = logging.getLogger(__name__)

def readpts(s):
    s = re.sub(r"(?:\s*(?:plus|minus)\s+[-\d.]+\s*(?:pt|in|sp|em))+$", "", s)
    if s.endswith("pt"):
        return float(s[:-2])
    elif s.endswith("in"):
        return float(s[:-2]) * 72
    elif s.endswith("sp"):
        return float(s[:-2]) / 65536.
    else:
        try:
            return float(s) / 65536.
        except ValueError:
            return 0

@dataclass
class ParRect:
    pagenum:    int
    xstart:     float
    ystart:     float       # top of paragraph, 0 is bottom of page. Usually > yend
    xend:       float = 0.
    yend:       float = 0.  # bottom of paragraph
    dests:      InitVar[None] = None
    lastdest:   InitVar[None] = None
    firstdest:  InitVar[None] = None
    xdvlines:   InitVar[None] = None
    
    def __str__(self):
        return f"{self.pagenum} ({self.xstart},{self.ystart}-{self.xend},{self.yend})"

    def __repr__(self):
        return self.__str__()

    def get_dest(self, x, y, baseline):
        if self.dests is None or baseline is None:
            return None
        ydiff = None
        xdiff = None
        curra = None
        for a in self.dests:
            logger.log(5, f"Testing ({x}, {y}) against {a}")
            if a[1][1] > y and (ydiff is None or a[1][1] - y < ydiff):
                ydiff = a[1][1] - y
                curra = a
            if ydiff is not None and ydiff < baseline and a[1][1] > y and a[1][0] <= x and (xdiff is None or x - a[1][0] < xdiff):
                xdiff = x - a[1][0]
                curra = a
        res = None if curra is None else curra[0]
        logger.log(5, f"Found {curra}")
        return res


@dataclass
class ParDest:
    name:       str
    pagenum:    int
    x:          float
    y:          float

    def __gt__(self, other):
        return self.y < other.y or self.y == other.y and self.x > other.x

    def __lt__(self, other):
        return self.y > other.y or self.y == other.y and self.x < other.x

@dataclass
class ParInfo:
    ref:        str
    partype:    str
    mrk:        str
    baseline:   float
    rects:      InitVar[None] = None
    lines:      int = 0

    def __str__(self):
        return f"{self.ref}[{getattr(self, 'parnum', '')}] {self.lines} @ {self.baseline} {self.rects}"

    def __repr__(self):
        return self.__str__()

    def sortKey(self):
        return (self.rects[-1].pagenum, refSort(self.ref), getattr(self, 'parnum', 0))

@dataclass
class FigInfo:
    ref:    str
    src:    str
    size:   (int, int)
    limit:  bool
    wide:   bool
    rects:  InitVar[None] = None

    def __str__(self):
        return f"Pic({self.ref})[{self.src}]({self.size[0]}x{self.size[1]}) {self.rects}"

    def __repr__(self):
        return self.__str__()

    def sortKey(self):
        return (self.rects[-1].pagenum, refSort(self.ref), 0)       # must sort with ParInfo

@dataclass
class BadSpace:
    pnum:   int
    line:   Line
    pos:    Tuple[float, float]
    width:  float
    widthem:    float

    def __lt__(self, other):
        return self.width < other.width

class ParlocLinesIterator:
    def __init__(self, fname):
        self.fname = fname
        self.collection = []
        self.replay = False

    def __iter__(self):
        if self.fname is not None and os.path.exists(self.fname):
            with open(self.fname, encoding="utf-8") as inf:
                self.lines = inf.readlines()
        else:
            self.lines = []
        return self

    def __next__(self):
        if self.replay:
            if len(self.collection):
                return self.collection.pop(0)
            else:
                self.replay = False
        if not len(self.lines):
            raise StopIteration
        return self.lines.pop(0)

    def collectuntil(self, limit, lines):
        self.collection = lines
        while len(self.lines):
            l = self.lines.pop(0)
            self.collection.append(l)
            if l.startswith(limit):
                break

    def startreplay(self):
        if len(self.collection):
            self.replay = True
            logger.log(7, "Starting replay of {len(self.collection)} lines")



class PopplerDest(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("page_num", ctypes.c_int),
        ("left", ctypes.c_double),
        ("bottom", ctypes.c_double),
        ("right", ctypes.c_double),
        ("top", ctypes.c_double),
        ("zoom", ctypes.c_double),
        ("named_dest", ctypes.c_char_p),
        ("change_left", ctypes.c_uint, 1),
        ("change_top", ctypes.c_uint, 1),
        ("change_zoom", ctypes.c_uint, 1),
    ]


class Paragraphs(list):
    parlinere = re.compile(r"^\\@([a-zA-Z@]+)\s*\{(.*?)\}\s*$")

    def readParlocs(self, fname, rtl=False):
        self.pindex = []
        self.pnums = {}
        self.pnumorder = []
        self.pheights = []
        self.dests = {}
        if fname is None:
            return
        currp = None
        currpic = None
        currr = None
        endpar = True
        inpage = False
        pnum = 0
        lastyend = 0
        polycol = "L"
        currps = {polycol: None}
        colinfos = {}
        innote = False
        pwidth = 0.
        lines = ParlocLinesIterator(fname)
        for l in lines:
            m = self.parlinere.match(l)
            if not m:
                continue
            logger.log(5, l[:-1])
            c = m.group(1)
            p = m.group(2).split("}{")
            if c == "pgstart":          # pageno, available height, pagewidth, pageheight
                pnum += 1
                npnum = int(p[0])
                if npnum not in self.pnums:
                    self.pnums[npnum] = pnum
                self.pnumorder.append(npnum)
                if len(p) > 3:
                    pwidth = readpts(p[2])
                    pheight = readpts(p[3])
                else:
                    pwidth = 0.
                    pheight = 0.
                self.pindex.append(len(self))
                self.pheights.append(pheight)
                inpage = True
                #cinfo = [readpts(x) for x in p[1:4]]
                #if len(cinfo) > 2:
                #    colinfos[polycol] = [cinfo[0], 0, cinfo[1], 0, cinfo[2]]
                lastyend = 0
            elif c == "parpageend":     # bottomx, bottomy, type=bottomins, notes, verybottomins, pageend
                pginfo = [readpts(x) for x in p[:2]] + [p[2]]
                inpage = False
            elif c == "colstart":       # col height, col depth, col width, topx, topy
                cinfo = [readpts(x) for x in p]
                logger.log(5, f"Test replay: {lines.replay} {pwidth=} width={cinfo[2]} left={cinfo[3]}")
                if rtl and not lines.replay and ((pwidth == 0. and cinfo[3] > cinfo[2]) or (cinfo[3] + cinfo[2]) * 2 < pwidth):
                    # right column. So swap it
                    logger.debug(f"Start column swap at {cinfo}")
                    lines.collectuntil("\\@colstop", [l])
                    continue
                colinfos[polycol] = cinfo
                if currps.get(polycol, None) is not None:
                    if currr is not None and currr.yend == 0:
                        currps[polycol].rects.pop()
                    currr = ParRect(pnum, cinfo[3], cinfo[4])
                    currps[polycol].rects.append(currr)
                lastyend = 0
            elif c == "colstop" or c == "Poly@colstop":     # bottomx, bottomy [, polycode]
                if currr is not None:
                    cinfo = colinfos.get(polycol, None)
                    currr.xend = cinfo[3] + cinfo[2] if cinfo is not None else readpts(p[0])
                    currr.yend = readpts(p[1])
                    currr = None
                colinfos[polycol] = None
                lines.startreplay()
                lastyend = 0
            elif c == "parstart":       # mkr, baselineskip, partype=section etc., startx, starty
                if len(p) == 5:
                    p.insert(0, "")
                logger.log(5, f"Starting para {p[0]}")
                cinfo = colinfos.get(polycol, None)
                if cinfo is None or len(cinfo) < 4:
                    continue
                if currr is not None:
                    currr.xend = cinfo[3]
                    currr.yend = readpts(p[5])
                currp = ParInfo(p[0], p[1], p[2], readpts(p[3]))
                currp.rects = []
                ystart = min(readpts(p[5]) + currp.baseline, lastyend or 1000000)
                currr = ParRect(pnum, cinfo[3], ystart)
                currp.rects.append(currr)
                currps[polycol] = currp
                self.append(currp)
            elif c == "parend":         # badness, bottomx, bottomy
                cinfo = colinfos.get(polycol, None)
                ps = currps.get(polycol, None)
                if ps is None or not len(ps.rects):
                    continue
                if currr is None:
                    currr = ps.rects[-1]
                if cinfo is None or currr is None:
                    continue
                currr.xend = cinfo[3] + cinfo[2]    # p[1] is xpos of last char in par
                if len(p) > 2:
                    ps.lines = int(p[0])
                    currr.yend = readpts(p[2])
                else:
                    currr.yend = readpts(p[1])
                if len(p) > 3:
                    currr.yend -= readpts(p[3])
                lastyend = currr.yend
                endpar = True
            elif c == "parlen":         # ref, parnum, numlines, marker, adjustment
                if not endpar or not inpage:
                    continue
                endpar = False
                currp = currps.get(polycol, None)
                if currp is None:
                    continue
                currp.lastref = p[0]
                if "k." in p[0]:
                    currp.ref = p[0]
                currp.parnum = int(p[1])
                currp.lines = int(p[2]) # this seems to be the current number of lines in para
                # currp.badness = p[4]  # current p[4] = p[1] = parnum (badness not in @parlen yet)
                logger.log(5, f"Stopping para {p[0]}")
                currps[polycol] = None
                currr = None
            elif c == "Poly@colstart": # height, depth, width, topx, topy, polycode
                polycol = p[5]
                colinfos[polycol] = [readpts(x) for x in p[:-1]]
                cinfo = colinfos[polycol]
                if polycol not in currps:
                    currps[polycol] = None
                if currps[polycol] is not None:
                    currr = ParRect(pnum, cinfo[3], cinfo[4])
                    currps[polycol].rects.append(currr)
            elif c == "parpicstart":     # ref, src (filename or type), x, y
                cinfo = colinfos.get(polycol, None)
                if cinfo is None or len(cinfo) < 4:
                    cinfo = None
                xstart = readpts(p[2]) if cinfo is None else cinfo[3]
                if currr is not None:
                    currr.yend = readpts(p[3])
                    currr.xend = xstart
                currpic = FigInfo(p[0], p[1], (0, 0), False, False)
                currpic.rects = []
                currr = ParRect(pnum, xstart, readpts(p[3]))
                currpic.rects.append(currr)
                self.append(currpic)
                lastyend = 0
            elif c == "parpicstop":     # ref, src (filename or type), width, height, x, y
                currpic = None
                cinfo = colinfos.get(polycol, None)
                if currr is None:
                    continue
                currr.xend = currr.xstart + readpts(p[2])
                currr.yend = currr.ystart - readpts(p[3])
                if currp is not None:
                    currpr = currr
                    if not len(currp.rects) or currp.rects[-1].xend > 0:
                        currr = ParRect(pnum, currpr.xstart, currpr.yend)
                        currp.rects.append(currr)
                    else:
                        currr = currp.rects[-1]
                        currr.xstart = currpr.xstart
                        currr.ystart = currpr.yend
                else:
                    currr = None
                lastyend = 0
            elif c == "parpicsize":
                if len(p) < 4:
                    (w, h) = readpts(p[0]), readpts(p[1])
                else:
                    (w, h) = readpts(p[2]), readpts(p[3])
                    # if p[0] == "height":
                    #     (w, h) = (h, w)
                    if currpic is not None:
                        currpic.size = (w, h)
                        if p[0] == "width":
                            currpic.wide = True
                        if p[1] == "heightlimit":
                            currpic.limit = True
                
            # "parnote":        # type, callerx, callery
            # "notebox":        # type, width, height
            # "parlines":       # numlines in previous paragraph (occurs after @parlen)
            # "nontextstart":   # x, y
            # "nontextstop":    # x, y
        self.sort(key=lambda x:x.sortKey())
        logger.log(7, f"{self.pindex=}  parlocs=" + "\n".join([str(p) for p in self]))
        logger.debug(f"{self.pnums=}, {self.pnumorder=}")
        
    def isEmpty(self):
        return not len(self.pindex)
        
    def _iterRectsPage(self, pnum):
        if pnum > len(self.pindex): # need some other test here 
            return
        e = self.pindex[pnum] if pnum < len(self.pindex) else len(self)
        for p in self[max(self.pindex[pnum-1]-2, 0):e+2]:       # expand by number of glots
            for i,r in enumerate(p.rects):
                if r.pagenum != pnum:
                    continue
                yield p, r

    def findPos(self, pnum, x, y, rtl=False, endx = None):
        """ Given page index (not folio) returns (ParDest, ParRect) covering the given x, y """
        # just iterate over paragraphs on this page
        for p, r in self._iterRectsPage(pnum):
            logger.log(7, f"Testing {r} against ({x},{y})")
            if r.ystart >=y and r.yend <= y:
                if r.xstart <= x and x <= r.xend:
                    return (p, r, r.get_dest(x, y, getattr(p, 'baseline', None)))
                if endx != None:
                    if r.xstart <= endx and endx <= r.xend:
                        return (p, r, r.get_dest(x, y, getattr(p, 'baseline', None)))
                    if x <= r.xstart and r.xend <= endx:
                        return (p, r, r.get_dest(x, y, getattr(p, 'baseline', None)))
        return (None, None, None)

    def getyrects(self, pnum, y):
        res = []
        if not len(self.pheights):
            return []
        y = (self.pheights[pnum-1] if pnum > 0 and pnum <= len(self.pheights) else self.pheights[-1]) - y
        return [r for p, r in self._iterRectsPage(pnum) if r.ystart >= y and r.yend <= y]

    def getParas(self, pnum, inclast=False):
        ''' Iterates all ParDest, ParRect on page with given index '''
        if pnum > len(self.pindex):
            return
        e = self.pindex[pnum] if pnum < len(self.pindex) else len(self)

        start = max(self.pindex[pnum-1], 0)
        if inclast and pnum > 1:        # pnum is 1 based
            done = False
            for p in self[start:-1:-1]:
                for r in reversed(p.rects):
                    if r.pagenum == pnum - 1:
                        yield (p, r)
                        done = True
                        break
                if done:
                    break
        start = max(start - 2, 0)
        for p in self[start:e+2]:
            for r in p.rects:
                if r.pagenum == pnum:
                    yield (p, r)

    def getParasByColumnOrParref(self, pnum=None, parref=None, column=None):
        """Returns paragraphs from a specific column on a page OR all paragraphs 
        in the same column as a given paragraph reference. This is a generator."""
        if parref:
            if not hasattr(parref, "rects") or not parref.rects:
                return
            pnum = parref.rects[0].pagenum

        if not pnum or pnum >= len(self.pindex):
            return
        x_values = [r.xstart for p, r in self.getParas(pnum)]
        
        if not x_values:
            return  # No paragraphs found, exit early
        threshold = (min(x_values) + max(x_values)) / 2
        if parref and column is None:
            column = 1 if parref.rects[0].xstart < threshold else 2
        for p, r in self.getParas(pnum):
            if (column == 1 and r.xstart < threshold) or (column == 2 and r.xstart >= threshold):
                yield (p, r)

    def get_folio(self, pindex):
        ''' Given a page index, return the folio for it '''
        if self.pnumorder is None or not len(self.pnumorder):
            return pindex
        if pindex is None or pindex > len(self.pnumorder):
            return None
        else:
            return self.pnumorder[pindex - 1]

    def load_dests(self, doc):
        dests_tree = doc.create_dests_tree()
        n = dests_tree.node_first()
        self.dests = {}
        while n is not None:
            adest = ctypes.cast(n.value(), ctypes.POINTER(PopplerDest)).contents
            akey = ctypes.cast(n.key(), ctypes.c_char_p).value
            self.dests.setdefault(adest.page_num, []).append(ParDest(str(akey.decode("utf-8").replace(".", " ").replace(":", ".") if akey else ""), adest.page_num, adest.left, adest.top))
            n = n.next()
        dests_tree.destroy()
        logger.debug(f"{len(self.dests)=}")

    def load_page(self, doc, page, pindex):
        currlast = None
        for p, r in self.getParas(pindex, inclast=True):
            logger.log(5, f"load_page processing {p=} {r=}")
            if r.pagenum < pindex:
                opg = doc.get_page(r.pagenum)
                if r.dests is None and opg is not None:
                    self.load_page(doc, opg, r.pagenum)
                currlast = max(r.dests)
                continue
            if r.dests is None:
                r.dests = [(currlast.name, (r.xstart, r.ystart))] if currlast is not None else []
            else:
                continue
            for a in self.dests.get(pindex, []):
                if a.x >= r.xstart and a.x <= r.xend and a.y >= r.yend and a.y <= r.ystart:
                    r.dests.append((a.name, (a.x, a.y)))
                    currlast = max(currlast, a) if currlast is not None else a

    def addxdvline(self, line, pindex, inrect=None):
        if inrect is None:
            x = line.glyph_clusters[0].glyphs[0][0]
            end = line.glyph_clusters[-1].glyphs[-1][2]
            y = line.vstart
            pheight = self.pheights[pindex - 1] if pindex <= len(self.pheights) else self.pheights[-1]
            inpar, inrect, _ = self.findPos(pindex, x, pheight - y, endx = end)
            if inrect is None:
                #print(f"{pindex}@({x},{pheight-y})")
                return
            ypos = pheight - 0.1 * y - 0.9 * line.vmax
            if inrect.ystart < ypos or inrect.yend > ypos:
                return
        if inrect.xdvlines is None:
            inrect.xdvlines = []
        inrect.xdvlines.append(line)

    def allxdvlines(self):
        for p in self:
            for r in p.rects:
                if r.xdvlines is not None:
                    for l in r.xdvlines:
                        yield (l, p, r)

    def getnbadspaces(self, n=0):
        if n == 0:
            n = int(math.sqrt(len(self))) * 4
        curr = 1        # don't go below 1em
        res = []
        for l, p, r in self.allxdvlines():
            # [[pnum, pos(x,y), width]]
            spaces = sorted([BadSpace(r.pagenum, l, *b) for b in l.has_badspace(curr)], key=lambda s:s.width, reverse=True)
            for s in spaces:
                if not len(res):
                    res.append(s)
                elif res[0] < s:
                    if len(res) >= n:
                        heapq.heapreplace(res, s)
                    else:
                        heapq.heappush(res, s)
        return res

    def _getlines(self, pnum):
        for p, r in self.getParas(pnum):
            if r.xdvlines is None:
                continue
            yield from r.xdvlines

    def getbadspaces(self, pnum, threshold, char_threshold):
        for l in self._getlines(pnum):
            spaces = l.has_badspace(threshold, char_threshold)
            for s in spaces:
                yield BadSpace(pnum, l, *s)
            
    def getcollisions(self, pnum):
        for l in self._getlines(pnum):
            collisions = l.has_collisions()
            for c in collisions:
                #print(c)
                yield c
                
    def getrivers(self, pnum, **kw):
        rivers = Rivers(**kw)
        for l in self._getlines(pnum):
            rivers.add_line(l)
        page_rivers = rivers.all_rivers()
        return page_rivers

    # wanted bits 0 = spaces, 1 = collisions, 2 = rivers
    def getstats(self, wanted, threshold, char_threshold):
        collisions = set()
        spaces = set()
        rivers = set()
        for pnum in range(len(self.pindex)):
            for l in self._getlines(pnum):
                if (wanted & 1) == 1 and pnum not in spaces:
                    s = l.has_badspace(threshold, char_threshold)
                    if len(s):
                        spaces.add(pnum)
                if (wanted & 2) == 2 and pnum not in collisions:
                    c = l.has_collisions()
                    if len(c):
                        collisions.add(pnum)
                if ((wanted & 2) == 0 or pnum in collisions) \
                        and ((wanted & 1) == 0 or pnum in spaces):
                    break
            if (wanted & 4) == 4:
                r = self.getrivers(pnum)
                if len(r):
                    rivers.add(pnum)
        return (sorted(spaces), sorted(collisions), sorted(rivers))
            
            
