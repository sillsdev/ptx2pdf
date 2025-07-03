
from ptxprint.utils import universalopen
from ptxprint.parlocs import readpts
from dataclasses import dataclass, asdict
import re
import logging

logger = logging.getLogger(__name__)

default_weights = {"f": 1, "x": 1, "s": 10, "c": 100, "v": 1000}
allfields = "ref marker hpos vpos gap width height depth xoffset yoffset pnum xpos ypos".split()
mnotelinere = re.compile(r"\\@marginnote" + "".join(r"\{{(?P<{}>.*?)\}}".format(a) for a in allfields))

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
    pnum: int
    xpos: float
    ypos: float
    yshift: float = 0
    side: str = ""

    @property
    def ymin(self):
        return self.ypos - self.depth - self.yoffset

    @property
    def ymax(self):
        return self.ypos + self.height - self.yoffset

    @property
    def xmin(self):
        return self.xpos + self.xoffset + (self.gap if self.side == "right" else -self.width)

    @property
    def xmax(self):
        return self.xpos + self.xoffset + (-self.gap if self.side == "left" else self.width + self.gap)

class Track(list):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def test(self, n):
        if n.xmax < self.left or n.xmin > self.right:
            return False
        return True

    def append(self, n):
        self.left = min(self.left, n.xmin)
        self.right = max(self.right, n.xmax)
        super().append(n)

def getside(pnum, side):
    if side == "inner":
        return "right" if pnum % 2 else "left"
    elif side == "outer":
        return "left" if pnum % 2 else "right"
    return side


class MarginNotes:

    def __init__(self, fpath=None):
        self.pages = []
        self.pheight = 0
        if fpath is not None:
            self.readFile(fpath)

    def readFile(self, fpath):
        with universalopen(fpath) as inf:
            for l in inf.readlines():
                m = mnotelinere.match(l)
                if not m:
                    continue
                data = m.groupdict()
                for a in ("gap", "width", "height", "depth", "xoffset", "yoffset", "xpos", "ypos"):
                    data[a] = readpts(data[a])
                data["pnum"] = int(data["pnum"]) - 1
                note = MarginNote(**data)
                if note.pnum >= len(self.pages):
                    self.pages.extend([[]] * (note.pnum - len(self.pages) + 1))
                self.pages[note.pnum].append(note)

    def processpage(self, pnum, weights=None):
        # co-ordinates are from bottom left of page
        if weights is None:
            weights = default_weights
        tracks = []
        for n in self.pages[pnum]:
            self.pheight = max(self.pheight, n.ymax)
            n.side = getside(pnum, n.hpos)
            for t in tracks:
                if t.test(n):
                    t.append(n)
                    break
            else:
                t = Track(n.xmin, n.xmax)
                tracks.append(t)
                t.append(n)
            lastn = n
        # now position within each track
        for t in tracks:
            t.sort(key=lambda n:(-n.ymax, -n.ymin))
            maxup = 0
            i = 0
            curry = 0
            currc = 0
            currw = 0
            start = 0
            gap = 0
            while i < len(t):
                w = weights.get(t[i].marker, 1)
                if curry == 0:
                    curry = t[i].ymin
                    i += 1
                    continue
                if t[i].ymax > curry:
                    shift = t[i].ymax - curry
                    t[i].yshift -= shift
                    currc += w * shift
                    currw += w
                else:
                    if i > start + 1:
                        currw += weights.get(t[start].marker, 1)
                        shift = currc / currw
                        shift = min(shift, self.pheight - t[start].ymax - t[start].yshift)
                        for j in range(start, i):
                            t[j].yshift += shift
                    currs = 0
                    start = i
                curry = t[i].ymin + t[i].yshift
                i += 1

    def processpages(self, weights=None):
        for i in range(len(self.pages)):
            self.processpage(i, weights)

    def outfile(self, fname):
        changed = False
        with open(fname, "w", encoding="utf-8") as outf:
            for i, p in enumerate(self.pages):
                for n in p:
                    s = asdict(n)
                    s['yoffset'] += -s['yshift']  # + s['yoffset']
                    s['pnum'] += 1
                    if s['yshift'] != 0:
                        changed = True
                    for a in ("xpos", "ypos"):
                        s[a] = str(int(s[a] * 65536))
                    for a in ("gap", "width", "height", "depth", "xoffset", "yoffset"):
                        s[a] = "{:.5f}pt".format(s[a])
                    outf.write("\\@marginnote" + "".join(["{{{}}}".format(s[a]) for a in allfields]) + "\n") 
        return changed
def tidymarginnotes(fpath):
    m = MarginNotes(fpath)
    m.processpages()
    return m.outfile(fpath)
