#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, Tuple, List, Optional, Union, Any
import heapq, re, os, logging, random
from bisect import bisect
from ptxprint.parlocs import Paragraphs
from ptxprint.adjlist import AdjList
from ptxprint.runjob import RunJob
from ptxprint.utils import refSort
from usfmtc.usfmparser import Grammar

logger = logging.getLogger(__name__)

# -----------------------------
# BASIC TYPES
# -----------------------------

ParagraphRef = Any
VerseRef = Any
PageIndex = int
Expansion = float
Stretch = int
ParamSig = Tuple[Expansion, Stretch]
LineKey = Tuple[ParagraphRef, Expansion, Stretch]
BadKey  = Tuple[ParagraphRef, Expansion, Stretch]

def cmp(x, y):
    return -1 if x < y else 0 if x == y else 1

# -----------------------------
# LAYOUT RESULTS
# -----------------------------

@dataclass
class PageState:
    page_index: int
    column_free_lines: Tuple[int, ...]  # e.g. (0,) or (-1, 0)

@dataclass
class LayoutRunResult:
    pages: List[PageState]
    first_failing_page: Optional[PageIndex]
    paragraph_total_lines: Dict[ParagraphRef, int]  # p -> total lines in this run

    def _cmp(self, other):
        res = cmp(self.first_failing_page, other.first_failing_page)
        if res == 0:
            res = cmp(sorted(self.paragraph_total_lines.items()), sorted(other.paragraph_total_lines.items()))
        if res == 0:
            res = cmp(self.pages, other.pages)
        return res

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __eq__(self, other):
        return self._cmp(other) == 0

# -----------------------------
# ENGINE STATE
# -----------------------------

@dataclass
class EngineState:
    paragraph_params: Dict[ParagraphRef, ParamSig]
    float_anchors: Dict[Any, VerseRef]
    layout: LayoutRunResult

    def _cmp(self, other):
        res = cmp(self.layout, other.layout)
        if res == 0:
            res = cmp(sorted(self.paragraph_params.items()), sorted(other.paragraph_params.items()))
        return res

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __eq__(self, other):
        return self._cmp(other) == 0

# -----------------------------
# SOLVE RESULT
# -----------------------------

@dataclass
class HumanFixRequest:
    page: PageIndex
    message: str

@dataclass
class SolveResult:
    state: Optional[EngineState] = None
    human_fix: Optional[HumanFixRequest] = None

# -----------------------------
# HOOKS YOU IMPLEMENT
# -----------------------------

class Hooks:

    def __init__(self, printer):
        self.printer = printer

    def run_layout(self,
                   paragraph_params: Dict[ParagraphRef, ParamSig],
                   float_anchors: Dict[Any, VerseRef]) -> LayoutRunResult:
        self.printer.run(paragraph_params, float_anchors)
        pages = []
        firstbad = None
        for i in range(self.printer.parlocs.numPages()):
            u = self.printer.underfills[i+1]
            if firstbad is None and (isinstance(u, list) or u is not None):
                firstbad = i
            pages.append(PageState(i, u))
        plines = self.printer.get_plines()
        return LayoutRunResult(pages, firstbad, plines)

    def get_rect_paragraphs_for_pages(self,
                                        first: PageIndex,
                                        last: PageIndex) -> List[ParagraphRef]:
        return self.printer.get_pids_on_pages(first, last)

    def is_header_at_column_start(self,
                                  paragraph: ParagraphRef,
                                  layout: LayoutRunResult) -> bool:
        """True if paragraph is first content in column and in a header block."""
        return self.printer.isheader_column_start(paragraph)

    def is_header(self, paragraph: ParagraphRef):
        return self.printer.pid_isheader(paragraph)

    def design_badness(self,
                       paragraph: ParagraphRef,
                       expansion: float,
                       stretch: int) -> float:
        res = ((1 - expansion) * 100) ** 2 if expansion < 1 else (expansion - 1) * 100
        res += stretch * stretch * 10
        return res

# -----------------------------
# SOLVER
# -----------------------------

class BeamTypesetterSolver:
    def __init__(self,
                 paragraphs: List[ParagraphRef],
                 hooks: Hooks,
                 init_layout: LayoutRunResult,
                 max_backtrack_pages: int = 5,
                 beam_width: int = 6,
                 lookahead_sample: int = 6):
        self.paragraphs = paragraphs
        self.init_layout = init_layout
        self.hooks = hooks
        self.max_backtrack = max_backtrack_pages
        self.beam = beam_width
        self.lookahead = lookahead_sample
        self.line_cache: Dict[LineKey, int] = {}
        self.bad_cache: Dict[BadKey, float] = {}

    def solve_book(self) -> SolveResult:
        base = {p: (1.0,0) for p in self.paragraphs}
        for pid, lines in self.init_layout.paragraph_total_lines.items():
            self.line_cache[(pid,1.0,0)] = lines
        state = EngineState(base, {}, self.init_layout)
        if self.init_layout.first_failing_page is None:
            return SolveResult(state=state)
        return self._search(state)

    def _search(self, start:EngineState) -> SolveResult:
        openq=[]
        heapq.heappush(openq, (0, start))
        visited = set()
        count = 0
        while openq:
            _,state = heapq.heappop(openq)
            fail = state.layout.first_failing_page
            if fail is None:
                return SolveResult(state=state)
            for back in range(self.max_backtrack + 1):
                paras = self.hooks.get_rect_paragraphs_for_pages(max(0, fail-back), fail+1)
                moves = self._candidate_moves(state, paras, back)
                for new_params in moves:
                    merged = self._merge(state.paragraph_params, new_params)
                    #speculative = self._speculate(merged, fail)
                    speculative = merged
                    count += 1
                    logger.info(f"Running [{count}] for page {fail}: {speculative}")
                    layout = self.hooks.run_layout(speculative, state.float_anchors)
                    for pid, lines in layout.paragraph_total_lines.items():
                        e, s = speculative.get(pid, (1.0,0))
                        self.line_cache[(pid, e, s)] = lines
                    new_state = EngineState(speculative, state.float_anchors, layout)
                    #key=tuple(sorted(speculative.items()))
                    key = self._normalize(speculative)
                    if key in visited: continue
                    visited.add(key)
                    score = self._score(new_state)
                    heapq.heappush(openq, (score, new_state))
                if moves: break
        return SolveResult(human_fix = HumanFixRequest(
                    page = start.layout.first_failing_page,
                    message = "Unable to solve automatically"
        ))

    def _candidate_moves(self, state, paras, back):
        moves = []
        for p in paras:
            pid = p
            e, s = state.paragraph_params.get(pid, (1.0,0))
            current_lines = state.layout.paragraph_total_lines.get(pid)
            candidates = [(round(e-0.01, 2), s), (round(e-0.02, 2), s)]
            if self.hooks.is_header_at_column_start(p, state.layout):
                if back >= 1 and s < 2:
                    candidates.append((e, s+1))  # last-resort line sink
                else:
                    continue
            if s > -1: candidates.append((e, s-1))
            for ne, ns in candidates:
                cached = self.line_cache.get((pid, ne, ns), None)
                if cached is not None and cached == current_lines:
                    continue
                moves.append({pid: (ne, ns)})
        random.shuffle(moves)
        return moves[:self.beam]

    def _speculate(self, params, fail):
        out = dict(params)
        paras = self.hooks.get_rect_paragraphs_for_pages(fail+1, fail+4)
        count = 0
        for p in paras:
            if count >= self.lookahead: break
            pid = p
            if pid in out: continue
            for e, s in [(0.98,-1), (0.96,-1), (1.0,1)]:
                if (pid, e, s) not in self.line_cache:
                    out[pid] = (e, s)
                    count += 1
                    break
        return out

    def _normalize(self, params):
        out = {}
        for p in self.paragraphs:
            v = params.get(p, (1.0, 0))
            if v != (1.0, 0):
                out[p] = v
        return tuple(sorted(out.items()))

    def _merge(self,a,b):
        c = dict(a); c.update(b); return c

    def _score(self,state):
        fail = state.layout.first_failing_page
        if fail is None: return -1e9
        page = state.layout.pages[fail]
        deficit = sum(abs(x) for x in page.column_free_lines if x<0)
        bad = 0
        for pid, (e, s) in state.paragraph_params.items():
            if (pid, e, s) not in self.bad_cache:
                p = next(x for x in self.paragraphs if x == pid)
                self.bad_cache[(pid, e, s)] = self.hooks.design_badness(p, e, s)
            bad += self.bad_cache[(pid, e, s)]
        return fail*1000 + deficit*10 + bad

#---------

class TypesetterSolver:
    def __init__(self,
                 paragraphs: List[ParagraphRef],
                 hooks: Hooks,
                 init_layout: LayoutRunResult,
                 max_backtrack_pages: int = 5,
                 beam_width: int = 6,
                 lookahead_sample: int = 6):
        self.paragraphs = paragraphs
        self.hooks = hooks
        self.init_layout = init_layout
        self.max_backtrack = max_backtrack_pages
        self.beam = beam_width
        self.line_cache: Dict[LineKey, int] = {}
        self.bad_cache: Dict[BadKey, float] = {}
        self.impact: Dict[ParagraphRef, int] = {}
        self.para_map = {p:p for p in paragraphs}
        self.runcount = 0

    def solve_book(self) -> SolveResult:
        params = {p:(1.0,0) for p in self.paragraphs}
        for pid, lines in self.init_layout.paragraph_total_lines.items():
            self.line_cache[(pid,1.0,0)] = lines
        state = EngineState(params, {}, self.init_layout)
        while True:
            fail = state.layout.first_failing_page
            if fail is None: return SolveResult(state=state)
            fixed = self._repair_page(state, fail)
            if fixed is None:
                return SolveResult(human_fix=HumanFixRequest(page=fail, message="Unable to automatically fix page"))
            state = fixed

    def _repair_page(self, state:EngineState, page:int):
        best_state = None
        best_score = float("inf")
        current_deficit = self._page_deficit(state.layout, page)
        for back in range(self.max_backtrack+1):
            paras = self.hooks.get_rect_paragraphs_for_pages(max(0, page-back), page+1)
            paras = sorted(paras, key=lambda p: -self.impact.get(p,0))
            moves = self._candidate_moves(state, paras, back)
            for change in moves:
                pid = next(iter(change))
                new_params = self._merge(state.paragraph_params, change)
                self.runcount += 1
                logger.info(f"Run {self.runcount}, Page {page}. {new_params}")
                layout = self.hooks.run_layout(new_params, state.float_anchors)
                new_deficit = self._page_deficit(layout, page)
                if new_deficit >= current_deficit: continue
                score = new_deficit + self._design_cost(new_params)
                if score < best_score:
                    best_score = score
                    best_state = EngineState(new_params, state.float_anchors, layout)
                    self.impact[pid] = self.impact.get(pid,0) + 1
            if best_state: break
        return best_state

    def _candidate_moves(self, state, paras, back):
        moves = []
        for pid in paras:
            if self.hooks.is_header(pid):
                continue
            e, s = state.paragraph_params.get(pid, (1.0, 0))
            if self.hooks.is_header_at_column_start(pid, state.layout):
                if back >= 1 and s < 2 and self._changes_lines(pid, e, s+1):
                    moves.append({pid:(e, s+1)})
                continue
            for ne in (round(e-0.01, 2), round(e-0.01, 2)):
                if self._changes_lines(pid, ne, s):
                    moves.append({pid: (ne, s)})
            if s > -1 and self._changes_lines(pid, e, s-1):
                moves.append({pid:(e, s-1)})
        return moves[:self.beam]

    def _changes_lines(self, pid, e, s):
        base = self.line_cache.get((pid,1.0,0))
        new = self.line_cache.get((pid,e,s))
        if new is None: return True
        return new != base

    def _page_deficit(self, layout, page):
        p = layout.pages[page]
        return sum(abs(x) for x in p.column_free_lines if x < 0)

    def _design_cost(self, params):
        bad = 0
        for pid, (e, s) in params.items():
            key = (pid, e, s)
            if key not in self.bad_cache:
                p = self.para_map[pid]
                self.bad_cache[key] = self.hooks.design_badness(p, e, s)
            bad += self.bad_cache[key]
        return bad

    def _merge(self, a, b):
        c = dict(a)
        c.update(b)
        return c

#---------

class GrowList(list):
    def __setitem__(self, index, value):
        self._ensure(index)
        super().__setitem__(index, value)
    def __getitem__(self, index):
        if index >= len(self):
            return None
        return super().__getitem__(index) or default
    def _ensure(self, index):
        if index >= len(self):
            self.extend([None] * (index - len(self) + 1))

class PTXprinter:

    reunderfill = re.compile(r"^Underfill\[(\S+?)\]:\s+\[(\d+)\]\s+ht=([\d.]+)pt,\s+space=(\S+)pt,\s+baseline=(\S+)pt")

    def __init__(self, view, bk):
        self.job = None
        self.rtl = False    # not always
        self.view = view
        self.bk = bk

    def solve(self):
        self.view.savePics()
        self.view.saveStyles()
        self.hooks = Hooks(self)
        init_layout = self.hooks.run_layout({}, {})
        pids = self.get_pids()
        solver = TypesetterSolver(pids, self.hooks, init_layout)
        res = solver.solve_book()
        if isinstance(res, HumanFixRequest):
            print(f"{res.message} at {res.page}")
        
    def get_pids(self):
        return [p.pid() for p in self.parlocs]

    def get_pids_on_pages(self, first, last):
        res = set()
        for i in range(first, last + 1):
            for p, r in self.parlocs.getParas(i, inclast=True):
                res.add(p.pid())
        return sorted(res, key=self.pidkey)

    def pidkey(self, pid):
        m = re.match(r"^(.*?)(?:\[(.*?)\])?$", pid)
        return (refSort(m.group(1)), int(m.group(2) or 0))

    def get_plines(self):
        plines = {}
        for p in self.parlocs:
            plines[p.pid()] = p.lines     # do we need to munge p.ref?
        return plines

    def get_para_ind(self, pid):
        x = self.pidkey(pid)
        return bisect(self.parlocs, x, key=lambda p:p.sortKey()[1:])

    def isheader_column_start(self, pid):
        pi = self.get_para_ind(pid)
        p = self.parlocs[pi]
        pnum = p.rects[0].pagenum
        if self.parlocs[self.parlocs.pindex[pnum]].pid() == pid:
            return self.isheader(p.mrk)
        return False

    def pid_isheader(self, pid):
        pind = self.get_para_ind(pid)
        p = self.parlocs[pind]
        return self.isheader(p.mrk)

    def isheader(self, mrk):
        return Grammar.marker_categories.get(mrk, '') == "sectionpara"

    def run(self, parparms, floats):
        tname = self.view.getLocalTriggerFilename(self.bk)
        fname = self.view.getAdjListFilename(self.bk)
        adjfname = os.path.join(self.view.project.srcPath(self.view.cfgid), "AdjLists", fname)
        self.adjs = AdjList(100, 95, 105, fname=adjfname)
        for s, p in parparms.items():
            (r, para) = self.pidkey(s)
            self.adjs.setval(r[0], f"{r[1]}.{r[2]}", para, p[1], None, expand=p[0], append=True)
        self.adjs.createAdjlist()

        if self.job is None:
            self.job = RunJob(self.view, self.view.scriptsdir, self.view.scriptsdir, self.view.args)
            self.job.norun = True
            self.job.doit(noview=True)

        self.job.run_xetex(self.job.outfname, self.job.pdffile)
        parlocsfile = self.job.outfname.replace(".tex", ".parlocs")
        self.parlocs = Paragraphs()
        self.parlocs.readParlocs(parlocsfile, self.rtl)
        logfile = self.job.outfname.replace(".tex", ".log")
        self.parselog(logfile)

    def parselog(self, fname):
        self.underfills = GrowList()
        with open(fname, encoding="utf-8") as inf:
            for l in inf.readlines():
                m = self.reunderfill.match(l)
                if m:
                    pnum = int(m.group(2))
                    side = 0 if m.group(1) == "A" else 1
                    lines = int((float(m.group(4)) - float(m.group(3))) / float(m.group(5)) + 0.1)
                    v = self.underfills[pnum]
                    if side:
                        if isinstance(v, list) and len(v) == 1:
                            v = v + [lines]
                        elif isinstance(v, int):
                            v = [v] + [lines]
                        else:
                            v = [0, lines]
                    elif isinstance(v, list):
                            v[0] = lines
                    else:
                            v = lines
                    self.underfills[pnum] = v

    def read_badnesses(self):
        xdvname = self.job.outfname.replace(".tex", ".xdv")
        xdvreader = SpacingOddities(xdvname, parent=self.parlocs,
                                    fontsize=float(self.view.get("s_fontsize", 1)))
        for (opcode, data) in xdvreader.parse():
            pass
        self.parlocs.getnbadspaces()
        

def main():
    from ptxprint.main import main as ptxmain
    view = ptxmain(doitfn=None, argsline=None, retview=True)
    bks = view.getBooks()
    if len(bks):
        bk = bks[0]
        printer = PTXprinter(view, bk)
        printer.solve()

if __name__ == "__main__":
    main()

