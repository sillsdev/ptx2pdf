
from ptxprint.utils import universalopen
from ptxprint.parlocs import readpts
from dataclasses import dataclass, asdict
import numpy as np
import re, math
import logging

logger = logging.getLogger(__name__)

default_weights = {"f": 1, "x": 1, "s": 10, "c": 100, "v": 1000, 'esb': 10}
allfields = "ref marker hpos vpos gap width height depth xoffset yoffset pnum xpos ypos".split()
mnotelinere = re.compile(r"\\@marginnote" + "".join(r"\{{(?P<{}>.*?)\}}".format(a) for a in allfields))

def simplex_method(c, A, b):
    """
    Solves a linear programming minimization problem using the simplex method.

    Args:
        c: Coefficients of the objective function (numpy array).
        A: Coefficients of the constraints (numpy array).
        b: Right-hand side values of the constraints (numpy array).

    Returns:
        A tuple containing:
            - The optimal objective function value (float).
            - The optimal solution vector (numpy array).
    """
    c = c.astype(float)
    A = A.astype(float)
    b = b.astype(float)
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
        # ratios[tableau[fixed, pivot_column_index] != 0] = np.inf
        pivot_row_index = np.argmin(ratios)

        # Check for unbounded solution
        # if np.all(tableau[:-1, pivot_column_index] <= 0):
        if np.all(ratios == np.info):
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
        col = tableau[:-1, i]
        if np.count_nonzero(col) == 1 and np.max(col) == 1:
            r = np.argmax(col)
            solution[i] = tableau[r, -1]
        #if any(tableau[:-1, i] == 1) and all(tableau[:-1, i] == 0):
        #     solution[i] = tableau[np.where(tableau[:-1, i] == 1)[0][0], -1]
    return optimal_value, solution[:num_vars]


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
    ypos: float         # position of the top of the box
    yshift: float = 0
    side: str = ""

    def boxshift(self, istop):
        if self.vpos in ("bottom", "inline"):
            return 0. if istop else self.depth + self.height
        elif self.vpos == "top":
            return self.height if istop else self.depth
        elif self.vpos == "center":
            return (self.height + self.depth) / 2.

    @property
    def ymin(self):
        return self.ypos - self.boxshift(False) # - self.yoffset

    @property
    def ymax(self):
        return self.ypos + self.boxshift(True)  # - self.yoffset

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

    def __init__(self, fpath=None, psize=597.5, top=28.5, bot=28.5):
        self.pages = []
        self.psize = psize
        self.top = top
        self.bot = bot
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
                while note.pnum >= len(self.pages):
                    self.pages.append([])
                self.pages[note.pnum].append(note)

    def get_tracks(self, pnum):
        ''' Returns a list of noninteracting list of notes, the max height
            position of a note '''
        tracks = []
        for n in self.pages[pnum]:
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
        return tracks

    def processpage(self, pnum, weights=None, maxshift=1000):
        # co-ordinates are from bottom left of page
        if weights is None:
            weights = default_weights
        tracks = self.get_tracks(pnum)
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
            # refactor to include fixed blocks with local regions between
            while i < len(t) + 1:                       # work top of page to bottom
                if i < len(t):
                    w = weights.get(t[i].marker, 1)
                if i < len(t) and curry == 0:
                    curry = t[i].ymin                   # track current bottom
                    start = i                           # new block
                    i += 1
                    continue
                if i < len(t) and t[i].ymax > curry:    # in a block
                    shift = t[i].ymax - curry           # shift us to not collide
                    t[i].yshift -= shift
                    currc += w * shift                  # track weighted cost
                    currw += w
                else:                                   # end of block. Now shift the block back up based on weighted costs
                    if i > start + 1 or i == len(t) and curry < self.bot:
                        islast = True
                        currw += weights.get(t[start].marker, 1)
                        shift = float(currc / currw)            # the heavier the weight the more the corrective shift back
                        shift = min(shift, self.top - t[start].ymax - t[start].yshift)  # don't shift off the top of the page
                        if t[i-1].ymin + t[i-1].yshift + shift < self.bot:              # if shift would result in stuff off the bottom
                            shift = self.bot - t[i-1].ymin - t[i-1].yshift                  # increase shift
                            islast = False
                            if math.fabs(shift) > maxshift:
                                logger.error(f"Shift {shift} out of bounds ({maxshift}) on page {pnum} around {t[i-1].ref} ({t[i-1].ymin}-{t[i-1].ymax}+{t[i-1].yshift})")
                        for j in range(i-1, start-1, -1):
                            if islast and -t[j].yshift < shift:     # if we can hit original position, do it
                                shift = max(0, -t[j].yshift)        # don't make matters worse (more shifting away)
                            islast = False
                            t[j].yshift += shift

                        # Now scan up the page to see what we need to push up. Basically the same algorithm inverted
                        if start > 0 and t[start].ymax + t[start].yshift > t[start-1].ymin + t[start-1].yshift:
                            currt = t[start].ymax + t[start].yshift
                            k = start - 1
                            shiftu = 0
                            currc = 0
                            currw = 0
                            islast = True
                            # identify which notes need to move up and shift them up
                            while k >= 0 and currt > t[k].ymin + t[k].yshift:
                                shiftu = currt - t[k].ymin - t[k].yshift
                                t[k].yshift += shiftu
                                currt = t[k].ymax + t[k].yshift
                                k -= 1
                            start = k
                            currw = 0
                            currc = 0
                            # now calculate weighted cost and so shift for the whole block from bottom to top
                            for j in range(i-1, k-1, -1):
                                w = weights.get(t[j].marker, 1)
                                currw += w
                                currc += t[j].yshift * w
                            shift = -float(currc / currw)
                            shift = max(shift, self.bot - t[i-1].ymin - t[i-1].yshift)      # don't shift off the bottom of the page
                            if start >= 0 and t[start].ymax + t[start].yshift + shift > self.top:       # if upward shift would push us over the top
                                shift = self.top - t[start].ymax - t[start].yshift                      # increase downward shift to match
                                islast = False
                            # now apply updated shift to the whole block top to bottom (since bottom is tight from last shifts)
                            for j in range(start, i):
                                if islast and -t[j].yshift > shift:
                                    shift = min(0, -t[j].yshift)
                                islast = False
                                t[j].yshift += shift
                    currs = 0
                    if 0 < i < len(t) and t[i].ymax + t[i].yshift < t[i-1].ymin + t[i-1].yshift:
                        start = i
                if i < len(t):
                    curry = t[i].ymin + t[i].yshift
                elif curry < self.bot - 1:
                    logger.error(f"Page {t[i-1].pnum} with {len(t)} at {i}({t[i-1].ref}) too full to fit everything")
                i += 1
        return

    def simplexpage(self, pnum, weights=None, min_spacing = 1):
        r""" Express the collision problem as a linear programming problem:
            Minimize \sum w_i \dot t_i
            Subject to -s_i \lteq t_i , s_i \lteq t_i
            Let L_i = ymax + s_i ; R_i = ymin + s_i
            We require L_i \gteq R_j + \delta OR L_j \gteq R_i + \delta
            Refactoring to remove the OR requires a large value M and z_{ij} \elementof \{0, 1\}
                L_i \gteq R_j + \delta - M \dot z_{ij}
                L_j \gteq R_i + \delta - M \dot (1 - z_{ij})
            For fixed node j we also say
                L_i \lteq L_j - \epsilon  or   L_i \gteq R_j + \epsilon
        """
        if weights is None:
            weights = default_weights
        tracks, pheight = self.get_tracks(pnum)
        for t in tracks:
            N = len(t)
            def s(i): return i
            def st(i): return i + N
            def sd(i): return i + 2 * N

            c = np.zeros(N * 3)
            for i, n in enumerate(t):
                c[st(i)] = weights.get(n.marker, 1)

            A = []
            b = []
            # 1. |s_i| ≤ t_i → s_i - t_i ≤ 0 and -s_i - t_i ≤ 0
            for i, n in enumerate(t):
                row1 = np.zeros(N * 3)
                row1[s(i)] = 1
                row1[st(i)] = -1
                A.append(row1)
                b.append(0)

                row2 = np.zeros(N * 3)
                row2[s(i)] = -1
                row2[st(i)] = -1
                A.append(row2)
                b.append(0)

            # 2. Fixed constraints: s_i = 0 → s_i ≤ 0 and -s_i ≤ 0
            for i, n in enumerate(t):
                if c[st(i)] > 10000:
                    row1 = np.zeros(N * 3)
                    row1[s(i)] = 1
                    A.append(row1)
                    b.append(0)

                    row2 = np.zeros(N * 3)
                    row2[s(i)] = -1
                    A.append(row2)
                    b.append(0)

            # 3. Non-overlap constraints
            for i in range(N):
                for j in range(i+1, N):
                    row = np.zeros(N * 3)
                    row[s(i)] = 1
                    row[s(j)] = -1
                    rhs = t[i].ymin - t[j].ymax - min_spacing
                    A.append(row)
                    b.append(rhs)

            A = np.array(A)
            b = np.array(b)
            val, sol = simplex_method(c, A, b)
            for i, n in enumerate(t):
                n.yshift = sol[i]

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
                    s['yoffset'] += -s['yshift']  # + s['yoffset']  # amount of push down
                    s['pnum'] += 1
                    if s['yshift'] != 0:
                        changed = True
                    for a in ("xpos", "ypos"):
                        s[a] = str(int(s[a] * 65536))
                    for a in ("gap", "width", "height", "depth", "xoffset", "yoffset"):
                        if math.fabs(s[a]) > 32766:
                            logger.error(f"Dimension [{a}] on page {i} of {s[a]}pt too large in {s['ref']}")
                            s[a] = 0
                        s[a] = "{:.5f}pt".format(s[a])
                    outf.write("\\@marginnote" + "".join(["{{{}}}".format(s[a]) for a in allfields]) + "\n") 
        return changed

def tidymarginnotes(fpath, **kw):
    m = MarginNotes(fpath, **kw)
    m.processpages()
    return m.outfile(fpath)
