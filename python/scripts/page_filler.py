#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, Tuple, Any, Iterator, List, Set, Deque, Optional, Union, Generator, Iterable
from collections import deque, defaultdict
import heapq, re, os, logging, random, itertools
from math import sqrt, log10
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
ColMask = int
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
    paragraph_pages: Dict[ParagraphRef, List[Dict[PageIndex, ColMask]]]

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

    def get_pars(self, page, n=None):
        if n is None:
            return [k for k, v in self.paragraph_pages.items() if page in v]
        else:
            return [k for k, v in self.paragraph_pages.items() if (v.get(page, 0) & (n + 1)) != 0]

    def par_col(self, pid):
        return self.pages[self.paragraph_pages[pid]][1]

# -----------------------------
# ENGINE STATE
# -----------------------------

@dataclass
class EngineState:
    paragraph_params: Dict[ParagraphRef, ParamSig]
    float_anchors: Dict[Any, VerseRef]
    layout: LayoutRunResult
    parlocs: Paragraphs
    passed: bool = False

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

    def __init__(self, printer, state):
        self.printer = printer
        self.basestate = state

    def run_layout(self,
                   paragraph_params: Dict[ParagraphRef, ParamSig],
                   float_anchors: Dict[Any, VerseRef]) -> LayoutRunResult:
        self.printer.run(paragraph_params, float_anchors)
        pages = []
        firstbad = None
        for i in range(self.printer.parlocs.numPages()):
            u = self.printer.underfills[i+1]
            if firstbad is None and u is not None and u not in ([0], [0,0]):
                firstbad = i
            pages.append(PageState(i, u))
        plines = self.printer.get_plines()
        pmap = self.printer.get_pidmap()
        logger.info(f"{firstbad=}")
        return LayoutRunResult(pages, firstbad, plines, pmap)

    def get_paragraphs_for_pages(self,
                                        first: PageIndex,
                                        last: PageIndex,
                                        state = None) -> List[ParagraphRef]:
        if state is None:
            state = self.basestate
        res = [p for p, v in state.layout.paragraph_pages.items()
                    if any(k in range(first, last+1) for k in v.keys())]
        return res

    def get_paras_for_col(self, page, col, state=None):
        if state is None:
            state = self.basestate
        return state.layout.get_pars(page, col)

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
                       stretch: int,
                       result: bool = False) -> float:
        # try to guess how bad a paragraph would be
        isshrink = stretch < 0 or expansion < 1
        pwidth = self.printer.get_para(paragraph).lastwidth
        lines = self.basestate.layout.paragraph_total_lines[paragraph]
        res = 0 if isshrink else 20
        res += 5 * ((2 * stretch) ** 4) / lines
        res += min(0, 25*((1. - pwidth) if isshrink else pwidth) - lines)
        if result:
            res += 0 if (0.1 < pwidth < 0.9) else 50
        res += ((1 - expansion) * 100) ** 2
        res += 100 * self.printer.pid_isheader(paragraph)
        return res

    def progress(self, pindex, itercount):
        print(f"Starting page {pindex} after {itercount} iterations")

# -----------------------------
# SOLVER
# -----------------------------

UNKNOWN = object()
IMPOSSIBLE = object()

ParamSig = Tuple[float, int]
ParagraphRef = Any
Combo = Tuple[Tuple[ParagraphRef, int], ...]

DELTA_ORDER = [-1, -2, 1, 2]
BEAM_LIMIT = 1000
EXPANSION_ORDER = [1.0, 0.98, 0.97, 1.03, 0.96, 0.94, 1.05]


class DeltaCache:

    def __init__(self) -> None:
        self.data: Dict[Tuple[ParagraphRef, int], Any] = {}

    def get(self, p: ParagraphRef, d: int) -> Any:
        return self.data.get((p, d), UNKNOWN)

    def set(self, p: ParagraphRef, d: int, val: Any) -> None:
        self.data[(p, d)] = val


class ShapeCache:

    def __init__(self) -> None:
        self.data: Dict[Tuple[ParagraphRef, float, int], int] = {}

    def tested(self, p: ParagraphRef, e: float, s: int) -> bool:
        return (p, e, s) in self.data

    def set(self, p: ParagraphRef, e: float, s: int, d: int) -> None:
        self.data[(p, e, s)] = d

    def get(self, p: ParagraphRef, e: float, s: int) -> Optional[int]:
        return self.data.get((p, e, s))


class TypesetterSolver:

    def __init__(self, hooks, pids):
        self.hooks = hooks
        self.paragraph_order = pids
        self.probe_cache: Dict[Tuple[Any, float, int], int] = {}
        self.shape_cache: Dict[Tuple[Any, int], ParamSig] = {}
        self.baseline_lines: Dict[Any, int] = {}
        self.base_params = {p: (1.0, 0) for p in self.paragraph_order}
        self.tried = set()
        self.itercount = 0
        self.frozen_paragraphs = set()
        self.noprobe = False

    def solve(self, state, start_page: int = 0):
        self.init_state = state
        if not self.baseline_lines:
            self.baseline_lines = dict(state.layout.paragraph_total_lines)
        page = start_page
        self.initial_probes(state, page)
        wantprobe = False
        testloop = 10000
        while True:
            layout = state.layout
            if layout.first_failing_page is None:
                logger.info("solve_complete pages=%s", len(layout.pages))
                return state
            # if layout.first_failing_page < page:
            #     return None
            if not self.noprobe and layout.first_failing_page != page + 1:
                self.noprobe = True
                logger.info(f"Intermediate processing of {page+1}, with no probes")
                state = self.run_layout(self.base_params, state, {}, page + 1)
                layout = state.layout
                if layout.first_failing_page > page:
                    self.noprobe = False
                else:
                    wantprobe = True
            page = layout.first_failing_page
            self.hooks.progress(page, self.itercount)
            oldstate = state
            state = self.solve_page(state, page)
            if not state.passed:
                if oldstate.layout.first_failing_page == page - 1:
                    if page != testloop:
                        logger.info(f"{testloop=} page {state.layout.first_failing_page}")
                        testloop = min(page, testloop)
                        wantprobe = not self.noprobe
                        self.noprobe = True
                        continue
                if not self.noprobe:
                    logger.info(f"Loop with no probe for page {state.layout.first_failing_page}")
                    wantprobe = True
                    self.noprobe = True
                    continue
                return HumanFixRequest(page, "Couldn't solve page")
            solved = self.hooks.get_paragraphs_for_pages(page, page)
            self.frozen_paragraphs.update(solved)
            self.init_state = state
            if wantprobe:
                self.noprobe = False
                wantprobe = False

    def solve_page(self, state, page):
        self.tried.clear()
        paragraphs = self.get_candidate_paragraphs(page)
        page_base_params = dict(self.base_params)
        # logger.info(f"shape_cache={','.join('+'.join((str(k), str(v))) for k, v in self.shape_cache.items() if k[1] != 0)}")
        # logger.info(f"candidates={paragraphs}")
        combos = self.generate_combos(paragraphs, state, page)
        for combo in combos:
            if not combo and self.itercount > 0:
                continue
            key = tuple(sorted(combo.items()))
            if key in self.tried:
                continue
            if state.layout.pages[page].column_free_lines is not None \
                    and state.layout.pages[page].column_free_lines[0] == 0 \
                    and any(state.layout.paragraph_pages[p].get(page, 0) == 1 for p in combo.keys()):
                continue
            self.tried.add(key)
            new_state = self.run_layout(page_base_params, state, combo, page)
            free = new_state.layout.pages[page].column_free_lines
            if new_state.layout.first_failing_page is not None and new_state.layout.first_failing_page < page:
                state.layout.first_failing_page = new_state.layout.first_failing_page
                continue
            if free is None or all(x == 0 for x in free):
                logger.info("page_solved page=%s iterations=%s", page, self.itercount)
                logger.info(f"Winning params {",".join(str(v) for v in new_state.paragraph_params.items() if v[1] != (1.0, 0))}")
                self.base_params = dict(new_state.paragraph_params)
                new_state.passed = True
                return new_state
            state = new_state
        logger.info("page_failed page=%s", page)
        state.passed = False
        return state

    def initial_probes(self, state, page):
        paragraphs = self.paragraph_order
        probes = [(1.0, -1), (1.0, 1), (0.98, -1), (0.97, -1), (0.96, -1)]
        for e, s in probes:
            params = dict(state.paragraph_params)
            for p in paragraphs:
                if p not in self.frozen_paragraphs:
                    params[p] = (e, s)
            # logger.info(f"{params=}")
            layout = self.hooks.run_layout(params, state.float_anchors)
            self.itercount += 1
            logger.info("probe_run iter=%s e=%s s=%s", self.itercount, e, s)
            self.collect_probes(layout, paragraphs, params)

    def run_layout(self, page_base_params, state, combo, page):
        params = dict(page_base_params)
        #params = dict(self.base_params)
        for p, d in combo.items():
            params[p] = self.shape_cache[(p, d)]
        probe_params = dict(params)
        last_para = state.layout.get_pars(page)[-1]
        if not self.noprobe:
            found_any = False
            for p in self.paragraph_order[self.paragraph_order.index(last_para) + 2:]:
                if probe_params.get(p, (10, 10)) != (1.0, 0):
                    continue
                found = False
                for s in range(0, 3):
                    if found:
                        break
                    for e in range(99, 94, -1):
                        if (p, e/100, -s) not in self.probe_cache:
                            probe_params[p] = (e/100, -s)
                            found = True
                            break
                    if not found:
                        for e in range(101, 105):
                            if (p, e/100, s) not in self.probe_cache:
                                probe_params[p] = (e/100, s)
                                found = True
                                break
                found_any |= found
            if not found_any:
                self.noprobe = True
        # logger.info("BASE %s", {p:v for p,v in self.base_params.items() if v!=(1.0,0)})
        layout = self.hooks.run_layout(probe_params, state.float_anchors)
        self.itercount += 1
        logger.info("layout_run [%s] iter=%s  probe=%s combo=%s", page, self.itercount, not self.noprobe, str(combo))
#                ",".join("{}+{}".format(i, str(p.column_free_lines)) for i,p in enumerate(layout.pages) if p.column_free_lines is not None))
        self.collect_probes(layout, layout.paragraph_total_lines.keys(), probe_params)
        return EngineState(params, state.float_anchors, layout, self.hooks.printer.parlocs)

    def collect_probes(self, layout, paragraphs, params):
        for p in paragraphs:
            base = self.baseline_lines.get(p)
            if base is None:
                logger.info(f"{p} missing from base_lines")
                continue
            new = layout.paragraph_total_lines[p]
            delta = new - base
            if p not in params:
                continue
            e, s = params[p]
            #logger.info(f"{p} {base=}, {delta=}, ({e=}, {s=})")
            self.probe_cache[(p, e, s)] = delta
            key = (p, delta)
            bad = self.hooks.design_badness(p, e, s, result=True)
            sc = self.shape_cache.get(key, None)
            if sc is None or bad < self.hooks.design_badness(p, sc[0], sc[1], result=True):
                self.shape_cache[key] = (e, s)

    def generate_combos(self, paragraphs, state, page) -> Generator[Dict[Any, int], None, None]:
        yield {}
        moves = []
        pset = set(paragraphs)
        first_para = state.layout.get_pars(page)[0]
        if page - 1 not in state.layout.paragraph_pages[first_para]:
            first_para = None
        last_para = state.layout.get_pars(page)[-1]
        for (p, d), (e, s) in self.shape_cache.items():
            if p not in pset or d == 0:
                continue
            score = self.hooks.design_badness(p, e, s)
            moves.append((score, p, d))
        moves.sort()
        by_para = {}
        for score, p, d in moves:
            by_para.setdefault(p, []).append((score, d))
        plist = list(by_para.keys())
        max_r = min(5, int(6 / log10(min(5, len(plist)))))
        all_combos = []
        seen_col_sigs = {}
        for r in range(1, max_r + 1):
            for pars in itertools.combinations(plist, r):
                if state.paragraph_params.get(pars, (1.0, 0)) != (1.0, 0):
                    continue
                delta_lists = [by_para[p] for p in pars]
                for choice in itertools.product(*delta_lists):
                    score = sum(s for s, _ in choice) + 5 * len(choice)
                    combo = {p: d for p, (_, d) in zip(pars, choice)}
                    # have we done the same net col line change before?
                    col_deltas = [0, 0, 0, 0, 0]
                    for p, d in combo.items():
                        mask = state.layout.paragraph_pages[p].get(page, 0)
                        if mask == 3:
                            col_deltas[1] = d
                        elif p == first_para:
                            col_deltas[0] = d
                        elif p == last_para and (d > 1 or page+1 in state.layout.paragraph_pages[p]):
                            col_deltas[2] = d
                        elif mask != 0:
                            col_deltas[mask + 2] += d
                    else:
                        sig = tuple(col_deltas)
                        if score < seen_col_sigs.get(sig, 10000):
                            seen_col_sigs[sig] = score
                        else:
                            continue
                        
                   # if any(state.layout.paragraph_pages[p].get(page, 0) == 3 \
                   #         or page+1 in state.layout.paragraph_pages[p] for p in pars):
                   #     score *= 0.4
                   # if first_para is not None and any(first_para == p for p in pars):
                   #     score *= 1.5
                    all_combos.append((score, combo))
        all_combos.sort(key=lambda x: (x[0], len(x[1])))
        for _, combo in all_combos:
            yield combo

    def get_candidate_paragraphs(self, page):
        start = max(0, page - 4)
        pars = self.hooks.get_paragraphs_for_pages(page, page, state=self.init_state)
        pars.sort(key=self.paragraph_order.index)
        return pars

    def get_probe_paragraphs(self, page):
        return self.hooks.get_paragraphs_for_pages(page, page + 1)

    def combo_badness(self, combo):
        score = 0
        boundary = False
        for p, d in combo.items():
            (e, s) = self.shape_cache.get((p, d), (None, None))
            if e is None:
                score += 1000
            else:
                score += self.hooks.design_badness(p, e, s)
        return score


# -------------


class GrowList(list):
    def __setitem__(self, index, value):
        self._ensure(index)
        super().__setitem__(index, value)
    def __getitem__(self, index):
        if index >= len(self):
            return None
        return super().__getitem__(index) or None
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
        self.view.set("c_allowUnbalanced", True)

    def solve(self):
        self.view.savePics()
        self.view.saveStyles()
        self.hooks = Hooks(self, None)
        init_layout = self.hooks.run_layout({}, {})
        pids = list(init_layout.paragraph_pages.keys())
        logger.info(f"lastwidths={', '.join(f'{p}={self.get_para(p).lastwidth:.2f}' for p in pids)}")
        state = EngineState({p: (1.0, 0) for p in pids}, [], init_layout, self.parlocs)
        self.hooks.basestate = state
        solver = TypesetterSolver(self.hooks, pids)
        res = solver.solve(state, 0)
        if isinstance(res, HumanFixRequest):
            print(f"{res.message} at {res.page}")
        else:
            print(f"Complete afer {solver.itercount} runs")
        
    def get_pidmap(self):
        res = {}
        for p in self.parlocs:
            for r in p.rects:
                c = res.setdefault(p.pid(), {}).get(r.pagenum - 1, 0)
                res[p.pid()][r.pagenum - 1] = c | (r.col + 1)
        return res

    def get_pids_on_pages(self, first, last, state=None):
        if state is None:
            plocs = self.parlocs
        else:
            plocs = state.parlocs
        res = set()
        colmask = {}
        for i in range(first + 1, last + 2):
            for p, r in plocs.getParas(i, inclast=True):
                res.add(p.pid())
                colmask[p.pid()] = colmask.get(p.pid(), 0) | (r.col + 1)
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
        return self.pidmap[pid]

    def get_para(self, pid):
        return self.parlocs[self.pidmap[pid]]

    def get_paragraph_start_page(self, pid):
        p = self.parlocs[self.pidmap[pid]]
        return min([r.pagenum for r in p.rects]) - 1

    def get_paragraph_end_page(self, pid):
        p = self.parlocs[self.pidmap[pid]]
        return max([r.pagenum for r in p.rects]) - 1

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
        return Grammar.marker_categories.get(mrk, '') in ("sectionpara", "title")

    def run(self, parparms, floats):
        tname = self.view.getLocalTriggerFilename(self.bk)
        fname = self.view.getAdjListFilename(self.bk)
        adjfname = os.path.join(self.view.project.srcPath(self.view.cfgid), "AdjLists", fname)
        self.adjs = AdjList(100, 95, 105, fname=adjfname)
        for s, p in parparms.items():
            (r, para) = self.pidkey(s)
            self.adjs.setval(s[:3], f"{r[1]}.{r[2]}", para, p[1], None, expand=int(p[0]*100), append=True)
        self.adjs.createAdjlist()
        tname = self.view.getLocalTriggerFilename(self.bk)
        tpath = os.path.join(self.view.project.printPath(self.view.cfgid), tname)
        self.adjs.createTriggerlist(fname=tpath)

        if self.job is None:
            self.job = RunJob(self.view, self.view.scriptsdir, self.view.scriptsdir, self.view.args)
            self.job.norun = True
            self.job.nopdf = True
            self.job.silent = True
            self.job.doit(noview=True)
            self.job.maxRuns = 1

        self.job.run_xetex(self.job.outfname, self.job.pdffile)
        parlocsfile = self.job.outfname.replace(".tex", ".parlocs")
        self.parlocs = Paragraphs()
        self.parlocs.readParlocs(parlocsfile, self.rtl)
        self.pidmap = {p.pid(): i for i, p in enumerate(self.parlocs)}
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
                            v = [lines]
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

