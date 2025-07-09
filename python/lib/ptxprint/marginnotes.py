
from ptxprint.utils import universalopen
from ptxprint.parlocs import readpts
from dataclasses import dataclass, asdict
import numpy as np
import re
import logging

logger = logging.getLogger(__name__)

default_weights = {"f": 1, "x": 1, "s": 10, "c": 100, "v": 1000}
allfields = "ref marker hpos vpos gap width height depth xoffset yoffset pnum xpos ypos".split()
mnotelinere = re.compile(r"\\@marginnote" + "".join(r"\{{(?P<{}>.*?)\}}".format(a) for a in allfields))

def simplex_method(c, A, b, fixed):
    """
    Solves a linear programming problem using the simplex method.

    Args:
        c: Coefficients of the objective function (numpy array).
        A: Coefficients of the constraints (numpy array).
        b: Right-hand side values of the constraints (numpy array).

    Returns:
        A tuple containing:
            - The optimal objective function value (float).
            - The optimal solution vector (numpy array).
    """
    num_vars = len(c)
    num_constraints = len(b)

    # Convert inequalities to equations by adding slack variables
    A = np.hstack((A, np.eye(num_constraints)))
    c = np.hstack((c, np.zeros(num_constraints)))

    # Initialize tableau
    tableau = np.vstack((np.hstack((A, b.reshape(-1, 1))),
                         np.hstack((c.reshape(1, -1), np.array([[0]])))))
    while True:
        # Find pivot column (most negative entry in the last row)
        pivot_column_index = np.argmin(tableau[-1, :-1])
        if tableau[-1, pivot_column_index] >= 0:
            break  # Optimal solution found

        # Find pivot row (minimum non-negative ratio)
        ratios = tableau[:-1, -1] / tableau[:-1, pivot_column_index]
        ratios[tableau[:-1, pivot_column_index] <= 0] = np.inf
        # insert other bounds constraints (fixed row indices) here
        ratios[tableau[fixed, pivot_column_index] != 0] = np.inf
        pivot_row_index = np.argmin(ratios)

        # Check for unbounded solution
        if np.all(tableau[:-1, pivot_column_index] <= 0):
            return "Unbounded solution", None

        # Perform pivoting (Gauss-Jordan elimination)
        pivot_value = tableau[pivot_row_index, pivot_column_index]
        tableau[pivot_row_index, :] /= pivot_value
        for i in range(tableau.shape[0]):
            if i != pivot_row_index:
                multiplier = tableau[i, pivot_column_index]
                tableau[i, :] -= multiplier * tableau[pivot_row_index, :]

    # Extract solution
    optimal_value = tableau[-1, -1]
    solution = np.zeros(num_vars)
    for i in range(num_vars):
        if any(tableau[:-1, i] == 1) and all(tableau[:-1, i] == 0):
             solution[i] = tableau[np.where(tableau[:-1, i] == 1)[0][0], -1]
        return optimal_value, solution


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
        return self.ypos - self.depth # - self.yoffset

    @property
    def ymax(self):
        return self.ypos + self.height # - self.yoffset

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

    def get_tracks(self, pnum):
        ''' Returns a list of noninteracting list of notes, the max height
            position of a note '''
        tracks = []
        pheight = 0
        for n in self.pages[pnum]:
            pheight = max(pheight, n.ymax)
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
        return (tracks, pheight)

    def processpage(self, pnum, weights=None):
        # co-ordinates are from bottom left of page
        if weights is None:
            weights = default_weights
        tracks, self.pheight = self.get_tracks(pnum)
        # now position within each track
        for t in tracks:
            # t.sort(key=lambda n:(-n.ymax, -n.ymin))
            maxup = 0
            i = 0
            curry = 0
            currc = 0
            currw = 0
            start = 0
            gap = 0
            while i < len(t) + 1:
                if i < len(t):
                    w = weights.get(t[i].marker, 1)
                if i < len(t) and curry == 0:
                    curry = t[i].ymin
                    i += 1
                    continue
                if i < len(t) and t[i].ymax > curry:
                    shift = t[i].ymax - curry
                    t[i].yshift -= shift
                    currc += w * shift
                    currw += w
                else:
                    if i > start + 1:
                        currw += weights.get(t[start].marker, 1)
                        shift = currc / currw
                        shift = min(shift, self.pheight - t[start].ymax - t[start].yshift)
                        if t[i-1].ymin + t[i-1].yshift + shift < 0:
                            shift = -(t[i-1].ymin + t[i-1].yshift)
                        for j in range(start, i):
                            t[j].yshift += shift
                    currs = 0
                    start = i
                if i < len(t):
                    curry = t[i].ymin + t[i].yshift
                i += 1
        return

    def simplexpage(self, pnum, weights=None):
        if weights is None:
            weights = default_weights
        tracks, pheight = self.get_tracks(pnum)
        for t in tracks:
            cs = [weights.get(n.marker, 1) for n in t]
            c = np.array(cs + cs)
            N = len(t)
            As = []
            laste = pheight
            bs = []
            fixeds = []
            for i, n in enumerate(t):
                fixeds.append(1 if weights.get(n.marker, 1) > 1e10 else 0)
                constraints = [0] * 2 * N
                constraints[i] = -1
                constraints[i+N] = 1
                if i > 0:
                    constraints[i-1] = 1
                    constraints[i-1+n] = -1
                As.append(constraints)
                bs.append(laste - n.ymax)
                laste = n.ymin
            A = np.array(As)
            b = np.array(bs)
            fixed = np.array(fixeds)
            val, sol = simplex_method(c, A, b, fixed)
            for i, n in enumerate(t):
                n.yshift = sol[i] - sol[i+N]

    def processpages(self, weights=None):
        for i in range(len(self.pages)):
            self.processpage(i, weights)
            # self.simplexpage(i, weights)

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
