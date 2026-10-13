
from ptxprint.utils import universalopen
from ptxprint.parlocs import readpts
from dataclasses import dataclass
from collections import defaultdict
import re, math
import logging

logger = logging.getLogger(__name__)

# See docs/dev/marginnotes_overflow.md for the design.
#
# Note lines (\@marginnote) always describe a note's anchor, as TeX would write
# them. Notes that do not fit in their column slot are pushed to the top of a
# later slot by writing an extra \@marginnotepush line. Push lines are never
# read as state: every pass decides every push again from the anchors, so
# running on our own output changes nothing.
#
# Coordinates are TeX's \pdflastxpos/\pdflastypos: the origin is the bottom
# left of the paper and y grows upwards. So top > bot, a note's ymax is its
# top edge, and moving a note down the page makes its y smaller.

default_weights = {"f": 1, "x": 1, "s": 10, "c": 100, "v": 1000, 'esb': 10}
allfields = "ref marker hpos vpos gap width height depth xoffset yoffset pnum xpos ypos".split()
lengthfields = ("gap", "width", "height", "depth", "xoffset", "yoffset")
posfields = ("xpos", "ypos")
mnotelinere = re.compile(r"\\@marginnote" + "".join(r"\{{(?P<{}>.*?)\}}".format(a) for a in allfields))
pushfields = "ref marker page col side".split()
mpushlinere = re.compile(r"\\@marginnotepush" + "".join(r"\{{(?P<{}>.*?)\}}".format(a) for a in pushfields))

SP = 65536.
coltolerance = 2.       # pt within which xpos values belong to the same column

def tosp(v):
    return int(round(v * SP))

def fmtpt(v):
    if math.fabs(v) < 5e-6:     # avoid -0.00000pt
        v = 0.
    return "{:.5f}pt".format(v)

@dataclass
class MarginNote:
    ref: str
    marker: str
    hpos: str
    vpos: str
    gap: float
    width: float
    height: float
    depth: float
    xoffset: float
    yoffset: float
    pnum: int           # \pageno, as in the file
    xpos: float         # left edge of the anchor's column
    ypos: float         # position of the note as placed this run
    yshift: float = 0   # shift from the anchor decided by layout
    side: str = ""      # resolved side in the slot the note is drawn in
    anchor: float = 0   # ypos + yoffset: where the note sits with no shift
    col: int = 0        # column of the anchor
    xbase: float = 0    # column x used for grouping notes into tracks
    order: tuple = ()   # document order
    push: tuple = None  # (page, col, side) if pushed
    inline: str = ""    # the note line as read, in our formatting

    def boxshift(self, istop):
        if self.vpos == "top":
            return self.height if istop else self.depth
        elif self.vpos == "center":
            return (self.height + self.depth) / 2.
        else:   # bottom, inline
            return 0. if istop else self.depth + self.height

    @property
    def extent(self):
        return self.height + self.depth

    @property
    def ymin(self):
        return self.anchor - self.boxshift(False)

    @property
    def ymax(self):
        return self.anchor + self.boxshift(True)

    @property
    def xmin(self):
        return self.xbase + self.xoffset + (self.gap if self.side == "right" else -self.width)

    @property
    def xmax(self):
        return self.xbase + self.xoffset + (-self.gap if self.side == "left" else self.width + self.gap)

@dataclass
class Block:
    ''' A run of notes t[start:end] in a track, stacked with no gaps '''
    start: int
    end: int
    height: float       # total height + depth of the notes
    weight: float       # total weight of the notes
    wtop: float         # sum of weight * the block top that puts each note at its anchor

    def place(self, top, bot):
        ''' Returns the y of the top of the block. y grows upwards, so the
            block's bottom is at place() - height. '''
        p = self.wtop / self.weight             # weighted mean of where the notes want the top to be
        p = max(p, bot + self.height)           # keep the bottom at or above bot
        return min(p, top)                      # keep the top at or below top, oversized blocks stay at the top

    def merge(self, other):
        ''' Appends the block below us. Its notes now sit self.height lower in the block,
            so the top that puts them at their anchors is self.height higher. '''
        self.end = other.end
        self.wtop += other.wtop + other.weight * self.height
        self.weight += other.weight
        self.height += other.height

class Track(list):
    def __init__(self, left, right, side):
        self.left = left
        self.right = right
        self.side = side

    def test(self, n):
        if n.side != self.side or n.xmax < self.left or n.xmin > self.right:
            return False
        return True

    def append(self, n):
        self.left = min(self.left, n.xmin)
        self.right = max(self.right, n.xmax)
        super().append(n)

def _cluster(xs):
    ''' Returns [(centre, count)] of runs of xs within coltolerance of each other '''
    res = []
    for x in sorted(xs):
        if res and x - res[-1][2] <= coltolerance:
            res[-1][0] += x
            res[-1][1] += 1
            res[-1][2] = x
        else:
            res.append([x, 1, x])
    return [(s / c, c) for s, c, _ in res]


class MarginNotes:

    def __init__(self, fpath=None, psize=597.5, top=28.5, bot=28.5, rtl=False, ncols=2, quiet=False):
        self.notes = []
        self.inpushes = []
        self.pushes = []
        self.psize = psize
        self.top = top
        self.bot = bot
        self.rtl = rtl
        self.maxcols = ncols
        self.ncols = 1
        self.grid = {0: [0.], 1: [0.]}
        self.quiet = quiet
        if fpath is not None:
            self.readFile(fpath)

    def _error(self, *a):
        if self.quiet:
            logger.debug(*a)
        else:
            logger.error(*a)

    def readFile(self, fpath):
        with universalopen(fpath) as inf:
            for l in inf.readlines():
                m = mpushlinere.match(l)
                if m:       # only kept for the change check
                    self.inpushes.append(m.groupdict())
                    continue
                m = mnotelinere.match(l)
                if not m:
                    continue
                data = m.groupdict()
                for a in lengthfields + posfields:
                    data[a] = readpts(data[a])
                data["pnum"] = int(data["pnum"])
                note = MarginNote(**data)
                note.anchor = tosp(note.ypos + note.yoffset) / SP
                note.inline = self.noteline(note)
                self.notes.append(note)

    def noteline(self, n, ypos=None, yoffset=None):
        s = {a: getattr(n, a) for a in allfields}
        if ypos is not None:
            s['ypos'] = ypos
            s['yoffset'] = yoffset
        for a in posfields:
            s[a] = str(tosp(s[a]))
        for a in lengthfields:
            if math.fabs(s[a]) > 32766:
                self._error(f"Dimension [{a}] on page {n.pnum} of {s[a]}pt too large in {n.ref}")
                s[a] = 0
            s[a] = fmtpt(tosp(s[a]) / SP)     # TeX and we spell the same sp differently
        return "\\@marginnote" + "".join("{{{}}}".format(s[a]) for a in allfields) + "\n"

    def pushline(self, p):
        return "\\@marginnotepush" + "".join("{{{}}}".format(p[a]) for a in pushfields) + "\n"

    def buildgrid(self):
        ''' Works out the x of each column, per page parity, from the notes' xpos '''
        xs = {0: [], 1: []}
        for n in self.notes:
            xs[n.pnum % 2].append(n.xpos)
        grids = {}
        for p, v in xs.items():
            cl = sorted(_cluster(v), key=lambda c: (-c[1], c[0]))[:self.maxcols]
            grids[p] = sorted(c[0] for c in cl)
        self.ncols = max(1, max(len(g) for g in grids.values()))
        if self.ncols > 1:
            deltas = [g[-1] - g[0] for g in grids.values() if len(g) == self.ncols]
            delta = sum(deltas) / len(deltas)
            for p, g in grids.items():
                other = grids[1-p]
                if len(g) == 0:
                    grids[p] = list(other)
                elif len(g) == 1 and len(other) == self.ncols:
                    # which column is this? Take the nearer one in the other parity
                    i = min(range(self.ncols), key=lambda i: abs(other[i] - g[0]))
                    grids[p] = [g[0] + (j - i) * delta / (self.ncols - 1) for j in range(self.ncols)]
        else:
            for p, g in grids.items():
                if not len(g):
                    grids[p] = grids[1-p] or [0.]
        self.grid = grids
        logger.debug(f"Marginnotes column grid: {self.ncols} columns, {self.grid}")

    def colof(self, n):
        g = self.grid[n.pnum % 2]
        i = min(range(len(g)), key=lambda i: abs(g[i] - n.xpos))
        if abs(g[i] - n.xpos) > coltolerance:
            logger.debug(f"Marginnote {n.ref}@{n.marker} on page {n.pnum} at x={n.xpos} is outside the column grid {g}")
        return self.ncols - 1 - i if self.rtl else i

    def colx(self, pnum, col):
        g = self.grid[pnum % 2]
        return g[self.ncols - 1 - col if self.rtl else col]

    def resolveside(self, hpos, pnum, col):
        ''' As \\d@marginnote does it. Outer is right on odd pages (or columns)
            and left on even ones. RTL swaps them and inner is the opposite of outer. '''
        if hpos in ("outer", "inner"):
            parity = (col if self.ncols > 1 else pnum) + int(self.rtl) + int(hpos == "outer")
            return ("right", "left")[parity % 2]
        return hpos if hpos in ("left", "right") else "left"

    def eligible(self, n, col):
        ''' Can the note be drawn in this column without facing the gutter? '''
        if self.ncols == 1 or n.hpos in ("inner", "outer"):
            return True
        side = self.resolveside(n.hpos, n.pnum, col)
        if col == 0:
            return side == ("right" if self.rtl else "left")
        elif col == self.ncols - 1:
            return side == ("left" if self.rtl else "right")
        return False

    def get_tracks(self, notes):
        ''' Returns a list of noninteracting lists of notes '''
        tracks = []
        for n in notes:
            for t in tracks:
                if t.test(n):
                    t.append(n)
                    break
            else:
                t = Track(n.xmin, n.xmax, n.side)
                tracks.append(t)
                t.append(n)
        return tracks

    def processpage(self, t, top, pnum, weights=None):
        ''' Lays out a track of notes, sorted top down, between top and self.bot.
            Colliding notes form blocks placed at their weighted mean position,
            so the heavier the weight the less a note moves. '''
        if weights is None:
            weights = default_weights
        bot = self.bot
        blocks = []
        for i, n in enumerate(t):
            w = weights.get(n.marker, 1)
            blocks.append(Block(i, i+1, n.extent, w, w * n.ymax))
            # while the block above reaches down into this one, merge them
            while len(blocks) > 1 and blocks[-2].place(top, bot) - blocks[-2].height < blocks[-1].place(top, bot):
                blocks[-2].merge(blocks.pop())
        for b in blocks:
            p = b.place(top, bot)
            if p - b.height < bot - 1. / SP:
                self._error(f"Page {pnum} too full to fit everything around {t[b.end-1].ref}")
            for n in t[b.start:b.end]:
                n.yshift = p - n.ymax
                p -= n.extent

    def processslot(self, pnum, col, natives, queue, weights=None):
        ''' Places the queue of notes pushed into this slot and the slot's own
            notes. Returns the queue of notes pushed on to the next slot. '''
        cap = self.top - self.bot
        block = [n for n in queue if self.eligible(n, col)]
        for n in block:
            n.side = self.resolveside(n.hpos, pnum, col)
            n.xbase = self.colx(pnum, col)
        # pushed notes are stacked from the top of the slot, one stack per side
        kept = []
        stackh = {}
        for side in ("left", "right"):
            used = 0
            for n in (b for b in block if b.side == side):
                if used + n.extent > cap and used > 0:
                    stackh[side] = used
                    break
                if used + n.extent > cap:
                    self._error(f"Margin note {n.ref} {n.marker} is too tall to fit on page {pnum}")
                kept.append(n)
                used += n.extent
            else:
                stackh[side] = used
        keptids = set(id(n) for n in kept)
        for n in sorted(kept, key=lambda n: n.order):
            n.push = (pnum, col, n.side)
            n.yshift = 0
            self.pushes.append(n)
        outgoing = [n for n in queue if id(n) not in keptids]

        overflow = []
        for t in self.get_tracks(natives):
            t.sort(key=lambda n: (-n.ymax, n.order))
            h = stackh.get(t.side, 0)
            used = 0
            for i, n in enumerate(t):
                if used + n.extent > cap - h:
                    if i == 0 and h == 0:       # too tall for any slot, so leave it here
                        self._error(f"Margin note {n.ref} {n.marker} is too tall to fit on page {pnum}")
                    else:
                        overflow.extend(t[i:])
                        del t[i:]
                        break
                used += n.extent
            self.processpage(t, self.top - h, pnum, weights)
        for n in overflow:
            n.yshift = 0
        return outgoing + sorted(overflow, key=lambda n: n.order)

    def processpages(self, weights=None):
        self.pushes = []
        if not len(self.notes):
            return
        self.buildgrid()
        slots = defaultdict(list)
        for i, n in enumerate(self.notes):
            n.col = self.colof(n)
            n.side = self.resolveside(n.hpos, n.pnum, n.col)
            n.xbase = n.xpos
            n.yshift = 0
            n.push = None
            n.order = (n.pnum, n.col, i)
            slots[(n.pnum, n.col)].append(n)
        pnum, col = min(slots.keys())
        last = max(slots.keys())
        queue = []
        extra = 0
        while (pnum, col) <= last or queue:
            if (pnum, col) > last:
                extra += 1
                if extra > 1000:
                    self._error(f"Margin notes still to place after page {pnum}: {', '.join(n.ref for n in queue)}")
                    for n in queue:
                        n.push = None
                    break
            queue = self.processslot(pnum, col, slots.get((pnum, col), []), queue, weights)
            col += 1
            if col >= self.ncols:
                col = 0
                pnum += 1

    def intext(self):
        ''' The file as read, in our formatting '''
        return "".join(n.inline for n in self.notes) + "".join(self.pushline(p) for p in self.inpushes)

    def outtext(self):
        res = []
        for n in self.notes:
            if n.push is not None:
                res.append(n.inline)
            else:
                final = tosp(n.anchor + n.yshift) / SP
                res.append(self.noteline(n, ypos=final, yoffset=n.anchor - final))
        for n in self.pushes:
            res.append(self.pushline({"ref": n.ref, "marker": n.marker, "page": n.push[0],
                                      "col": n.push[1], "side": n.push[2]}))
        return "".join(res)

    def outfile(self, fname):
        ''' Writes the file and returns whether anything changed '''
        text = self.outtext()
        with open(fname, "w", encoding="utf-8") as outf:
            outf.write(text)
        return text != self.intext()

def tidymarginnotes(fpath, **kw):
    m = MarginNotes(fpath, **kw)
    m.processpages()
    return m.outfile(fpath)
