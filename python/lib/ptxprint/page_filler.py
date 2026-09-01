#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, Tuple, Any, Iterator, List, Set, Deque, Optional, Union, Generator, Iterable, Literal
from collections import deque, defaultdict
from configparser import ConfigParser
import heapq, re, os, logging, random, itertools, argparse, threading, queue as _queue
import statistics, math
from bisect import bisect
import multiprocessing as mp
from math import sqrt, log10
from time import time, asctime, sleep
from ptxprint.parlocs import Paragraphs, ParInfo
from ptxprint.adjlist import AdjList
from ptxprint.runjob import RunJob, unlockme
from ptxprint.utils import refSort, bookcodes, f_, ProgressEvent, _
from ptxprint.view import ViewModel
from ptxprint.project import ProjectList
from ptxprint.utils import BuildParams
from ptxprint.xdv.xdvspaces import XdvSpaceMeasure
from usfmtc.usfmparser import Grammar
from usfmtc.reference import chaps, RefList

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
    if x is None:
        return -1
    elif y is None:
        return 1
    return -1 if x < y else 0 if x == y else 1

bkltrs = "".join([chr(x) for (a, b) in [(65, 91), (97, 123), (33, 65)] for x in range(a, b)])

def printbk(bk, page):
    bkc = bkltrs[int(bookcodes[bk])-1] if bk is not None else ""
    print(bkc+str(page), flush=True, end="")

all_probes = [(1.0, -1), (1.0, 1), (0.98, -1), (0.97, -1), (0.96, -1), (1.0, 0)]

# -----------------------------
# LAYOUT RESULTS
# -----------------------------

@dataclass
class PageState:
    page_index: int
    column_free_lines: Tuple[int, ...]  # e.g. (0,) or (-1, 0)


@dataclass
class FigurePlacement:
    fid:    str
    pid:    str
    col:    int
    lines:  int

@dataclass
class LayoutRunResult:
    pages: List[PageState]
    first_failing_page: Optional[PageIndex]
    paragraph_total_lines: Dict[ParagraphRef, int]  # p -> total lines in this run
    paragraph_pages: Dict[ParagraphRef, List[Dict[PageIndex, ColMask]]]
    page_figures: Dict[PageIndex, List[FigurePlacement]]
    result: int

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

    def next_bad(self, page=None):
        if page is None:
            page = (-1 if self.first_failing_page is None else self.first_failing_page) + 1
        for i in range(page, len(self.pages)):
            u = self.pages[i].column_free_lines
            if u is not None and u not in ([0], [0,0]):
                res = i
                break
        else:
            res = None
        self.first_failing_page = res
        return res

# -----------------------------
# ENGINE STATE
# -----------------------------

@dataclass
class EngineState:
    paragraph_params: Dict[ParagraphRef, ParamSig]
    float_anchors: Dict[Any, VerseRef]
    layout: LayoutRunResult
    parlocs: Paragraphs
    page: int
    passed: bool = False
    failures: Optional[list] = None
    complete: bool = False

    def _cmp(self, other):
        res = cmp(self.layout, other.layout)
        if res == 0:
            res = cmp(sorted(self.paragraph_params.items()), sorted(other.paragraph_params.items()))
        return res

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __eq__(self, other):
        return self._cmp(other) == 0

    def numPages(self):
        return self.parlocs.numPages()

# -----------------------------
# SOLVE RESULT
# -----------------------------

@dataclass
class HumanFixRequest:
    state: EngineState
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

    badness_stretch_tolerance   = 80   # avoid ±2
    badness_spacing_tolerance   = 20   # paragraph spacing distortion
    badness_shrink_preference   = 10   # + = prefer shrink, - = prefer stretch
    badness_header_aversion     = 60   # avoid headers
    badness_justification       = 20   # cost of being justified
    badness_line_density_factor = 1.0  # wide vs narrow text
    badness_line_weight         = 12
    badness_lastline_weight     = 20
    badness_tex_weight          = 12

    def __init__(self, printer, state):
        self.printer = printer
        self.basestate = state
        for a in (("spacing_tolerance", "pbspacingtol"),
                  ("expansion_factor", "pbexpbad"),
                  ("expansion_cost", "pbexpcost"),
                  ("contrast_factor", "pbcontrast")):
            val = float(printer.view.get("s_"+a[1]))
            logger.debug(f"{a}, {val}")
            setattr(self, "badness_"+a[0], val)
        vals = {k: getattr(self, k) for k in dir(self) if k.startswith("badness")}
        logger.log(15, f"Badness parameters = {vals}")

    def run_layout(self,
                   solver: Optional["Typesetter"],
                   paragraph_params: Dict[ParagraphRef, ParamSig],
                   float_anchors: Dict[Any, VerseRef],
                   base_page: int,
                   last_page: int,
                   prompt: str = ".",
                   genfiles: bool = False) -> LayoutRunResult:
        try:
            runres = self.printer.run_layout(solver, paragraph_params, float_anchors, last_page, prompt=prompt, genfiles=genfiles)
        except FileNotFoundError as e:
            logger.warn(f"run_layout failed {e}")
            return None
        pages = []
        firstbad = None
        for i in range(self.printer.parlocs.numPages()):
            u = self.printer.underfills[i]
            if firstbad is None and u is not None and len(u) and u not in ([0], [0,0]) and i > base_page:
                firstbad = i
            pages.append(PageState(i, u))
        plines = self.printer.get_plines()
        pmap = self.printer.get_pidmap()
        logger.log(15, f"{firstbad=}")
        res = LayoutRunResult(pages, firstbad, plines, pmap, [], runres)
        return res

    def get_paragraphs_for_pages(self,
                                        first: PageIndex,
                                        last: PageIndex,
                                        state = None) -> List[ParagraphRef]:
        if state is None:
            state = self.basestate
        res = [p for p, v in state.layout.paragraph_pages.items()
                    if any(k in range(first, last+1) for k in v.keys())]
        return res

    def get_lines_for_para_page(self, para: ParagraphRef, page: PageIndex):
        return self.printer.get_lines_para_page(para, page)

    def get_paras_for_col(self, page, col, state=None):
        if state is None:
            state = self.basestate
        return state.layout.get_pars(page, col)

    def get_first_page_for_para(self, para):
        return self.printer.get_paragraph_start_page(para)

    def chap_from_page(self, pnum):
        i = bisect(self.chapters, pnum)
        logging.log(15, f"page={pnum}, chapter={i}")
        return i

    def get_previous(self, pid, page=None):
        return self.printer.get_previous(pid, page=page)

    @property
    def cancelled(self):
        return self.printer.cancelled

    def is_header_at_column_start(self,
                                  paragraph: ParagraphRef,
                                  layout: LayoutRunResult) -> bool:
        """True if paragraph is first content in column and in a header block."""
        return self.printer.isheader_column_start(paragraph)

    def is_header(self, paragraph: ParagraphRef):
        return self.printer.pid_isheader(paragraph)

    def analyse_bw(self, testfn, page):
        self.printer.analyse_bw(testfn, page)

    def get_para(self, pid):
        return self.printer.get_para(pid)

    def append_stats(self, w):
        self.printer.stats.append(w)

    def progress(self, pevent):
        self.printer.progress(pevent)

# -----------------------------
# SOLVER
# -----------------------------

UNKNOWN = object()
IMPOSSIBLE = object()

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

    lookahead = 10

    def __init__(self, hooks, pids, expand=1., minexp=0.95, maxexp=1.05):
        self.hooks = hooks
        self.paragraph_order = pids
        self.expand = expand
        self.minexp = minexp
        self.maxexp = maxexp
        self.probe_cache: Dict[[Any], Dict[Tuple[float, int], int]] = {}
        self.shape_cache: Dict[Tuple[Any, int], Tuple(float, int, float)] = {}
        self.probe_params = {}
        self.baseline_lines: Dict[Any, int] = {}
        self.base_params = {p: (expand, 0) for p in self.paragraph_order}
        self.tried = set()
        self.itercount = 0
        self.frozen_paragraphs = set()
        self.noprobe = False
        self.bk = None
        self.all_probes = [(expand, -1), (minexp, -1), ((minexp + expand) / 2, -1),
                (maxexp, 1), (maxexp, 0), (expand, 0)]

    def solve(self, state, start_page:int=-1, stop:bool=True, restart:bool=False, book=None):
        self.bk = book
        self.init_state = state
        logger.log(15, f"{state.layout.paragraph_pages=}")
        if not self.baseline_lines:
            self.baseline_lines = dict(state.layout.paragraph_total_lines)
        if state.layout.first_failing_page is None:
            return state
        if restart:
            logger.debug(state.layout.first_failing_page)
            self.base_params = {}
            for p, v in state.paragraph_params.items():
                if self.hooks.get_first_page_for_para(p) <= state.layout.first_failing_page:
                    self.base_params[p] = v
            state.paragraph_params = dict(self.base_params)
        else:
            self.base_params = dict(state.paragraph_params)
        self.collect_probes(state.layout, self.paragraph_order, self.base_params, isbase=True, page=start_page)
        page = start_page + 1
        self.numpages = state.numPages()
        if self.numpages <= 2 * self.lookahead:
            npages = self.numpages - page + 1
        else:
            npages = self.lookahead
        try:
            layout = self.initial_probes(state, page, npages, restart=restart)
        except TimeoutError:
            return HumanFixRequest(state, page, "Stopped" if self.hooks.cancelled else "Timed out")
        state = EngineState(self.init_state.paragraph_params, state.float_anchors, layout, self.hooks.printer.parlocs, 0)
        testloop = 10000
        failed_pages = []
        while True:
            layout = state.layout
            # if layout.first_failing_page < page:
            #     return None
            nextpage = layout.first_failing_page
            logger.log(15, f"{page=}, {nextpage=}, is completed {state.complete}")
            if nextpage is None or nextpage == page:
                if state.complete:
                    logger.log(15, f"solve_complete pages=%s, underfills=%s", len(layout.pages),
                            str({i: lp.column_free_lines for i, lp in enumerate(layout.pages) if lp.column_free_lines is not None}))
                    # state = self.run_layout(self.base_params, state, {}, page, start_page)
                    state.failures = failed_pages
                    self.hooks.progress(ProgressEvent(book, (page or 0) + 1, "complete", f"Failed: {' '.join(str(p) for p in failed_pages)}" if failed_pages else None, self.numpages))
                    return state
                else:
                    nextpage = state.numPages() - 1
                    if state.numPages() - page >= 9 and self.numpages > 2 * self.lookahead:
                        layout = self.initial_probes(state, page, 10)
                        state = EngineState(self.init_state.paragraph_params, state.float_anchors, layout, self.hooks.printer.parlocs, page)
            page = nextpage
            try:
                state = self.solve_page(state, page, start_page)
            except TimeoutError:
                return HumanFixRequest(state, page + 1, "Stopped" if self.hooks.cancelled else "Timed out")
            if not state.passed:
                if state.layout.first_failing_page is not None and state.complete and state.layout.first_failing_page < page:
                    if page < testloop:
                        logger.log(15, f"{getattr(self, 'bk', 'UNK')}: {testloop=} page {state.layout.first_failing_page}")
                        testloop = min(page, testloop)
                        continue
                    else:
                        logger.log(15, f"{self.bk}: {page=} >= {testloop=} and bail")
                        return HumanFixRequest(state, page + 1, f"Caught in loop {testloop}..{page}")
                if stop:
                    return HumanFixRequest(state, page + 1, f"Couldn't solve page {page}")
                else:
                    while state.layout.first_failing_page is not None and state.layout.first_failing_page == page:
                        state.layout.next_bad()
                    failed_pages.append(page)
                    if state.layout.first_failing_page is None and state.complete:
                        return HumanFixRequest(state, page + 1, f"Failed: {' '.join(str(p) for p in failed_pages)}")
                    self.hooks.progress(ProgressEvent(book, page + 1, "badpage", "", self.numpages))
                    paras = self.get_candidate_paragraphs(state, page)
                    logger.warning(f"Could not solve page {page+1} after {paras[0] if len(paras) else 'UNK'} trying {(state.layout.first_failing_page or 0)+1}")
                    start_page = state.layout.first_failing_page or state.numPages() + 1
                    continue
            elif state.layout.first_failing_page is not None:
                self.hooks.progress(ProgressEvent(book, state.layout.first_failing_page, "goodpage", "", self.numpages))
            solved = self.hooks.get_paragraphs_for_pages(page, page)
            #self.frozen_paragraphs.update(solved)
            self.init_state = state

    def solve_page(self, state, page, start):
        self.tried.clear()
        if page >= state.numPages():
            state = self.run_layout(self.base_params, state, {}, page, start)
        paragraphs = self.get_candidate_paragraphs(state, page)
        page_base_params = dict(self.base_params)
        # logger.log(15, f"shape_cache={','.join('+'.join((str(k), str(v))) for k, v in self.shape_cache.items() if k[1] != 0)}")
        # logger.log(15, f"candidates={paragraphs}")
        combos = self.generate_combos(paragraphs, state, page)
        printbk(self.bk, page)
        startcount = self.itercount
        for combo in combos:
            if self.hooks.cancelled:
                raise TimeoutError("Stopped")
            if not combo and self.itercount > 0:
                continue
            key = tuple(sorted(combo.items()))
            if key in self.tried:
                logger.log(12, f"tried cache hit {key=}")
                continue
            if self.itercount - startcount > 200:
                break
            self.tried.add(key)
            if page < len(state.layout.pages) and state.layout.pages[page].column_free_lines is not None \
                    and any(x > 5 for x in state.layout.pages[page].column_free_lines):
                logger.log(15, f"Failing page for large gap")
                break
            new_state = self.run_layout(page_base_params, state, combo, page, start)
            if page < len(new_state.layout.pages):
                free = new_state.layout.pages[page].column_free_lines
            else:
                free = None
            if new_state.layout.first_failing_page is not None and new_state.layout.first_failing_page < page:
                logger.log(15, f"{state.layout.first_failing_page=} < {page} set it to {new_state.layout.first_failing_page}")
                state.layout.first_failing_page = new_state.layout.first_failing_page
                continue
            if not self.noprobe and (free is None or all(x == 0 for x in free)):
                lpars = state.layout.get_pars(page)
                pps = state.layout.paragraph_pages[lpars[-1]]
                if len(pps) > 1 and lpars[-1] in self.probe_params:
                    self.noprobe = True
                    new_state = self.run_layout(page_base_params, state, combo, page, start)
                    logger.log(15, f"Test run for good page, without probes {new_state.layout.first_failing_page=}")
                    self.noprobe = False
                    free = new_state.layout.pages[page].column_free_lines
            if new_state.layout.first_failing_page is None or new_state.layout.first_failing_page > page or free is None or not len(free) or all(x == 0 for x in free):
                logger.log(15, "page_solved page=%s iterations=%s", page, self.itercount)
                logger.log(15, f"Winning params {','.join(str(v) for v in new_state.paragraph_params.items() if v[1] != (1.0, 0))}")
                self.base_params = dict(new_state.paragraph_params)
                new_state.passed = True
                return new_state
            state = new_state
        logger.log(15, "page_failed page=%s", page)
        state = self.run_layout(page_base_params, state, {}, page, start)
        state.passed = False
        return state

    def evaluate_paragraph_probe(self, pid):
        """
        Evaluates candidate expansion probes for a paragraph.
        p_probes values represent relative line deltas (e.g., -2, -1, 0, +1, +2).
        """
        p_probes = self.probe_cache.get(pid, {})
        max_pos_delta = p_probes.get((self.maxexp, 1)) or 0
        max_neg_delta = p_probes.get((self.minexp, -1)) or 0
        pos_low, pos_high = self.expand, self.maxexp
        pos_delta_achieved = 0
        for (exp, strch), delta in p_probes.items():
            if exp <= self.expand or delta is None:
                continue
            if delta > 0:
                pos_high = min(pos_high, exp)
                pos_delta_achieved = max(pos_delta_achieved, delta)
            else:
                pos_low = min(pos_low, exp)

        pos_span = pos_high - pos_low
        pos_done = (pos_span <= 0.01)
        neg_low, neg_high = self.minexp, self.expand
        neg_delta_achieved = 0
        for (exp, strch), delta in p_probes.items():
            if exp >= self.expand or delta is None:
                continue
            if delta < 0:
                neg_low = max(neg_low, exp)
                neg_delta_achieved = min(neg_delta_achieved, delta)
            else:
                neg_low = min(neg_high, exp)

        neg_span = neg_high - neg_low
        neg_done = (neg_span <= 0.01)

        if not pos_done and (neg_done or pos_span >= neg_span):
            low, high = pos_low, pos_high
            dir_sign = 1
            achieved_delta = pos_delta_achieved
            get_target_delta = max
            max_bound_delta = max_pos_delta
        elif not neg_done:
            low, high = neg_low, neg_high
            dir_sign = -1
            achieved_delta = neg_delta_achieved
            get_target_delta = min
            max_bound_delta = max_neg_delta
        else:
            return (self.expand, 0, 0)

        stretch_sequence = [0, dir_sign]
        delta_in_shape_cache = (pid, achieved_delta) in self.shape_cache if achieved_delta != 0 else False
        if dir_sign == -1:
            if achieved_delta < 0 or delta_in_shape_cache:
                stretch_sequence.append(-2)
        elif dir_sign == 1:
            if delta_in_shape_cache and abs(max_bound_delta) >= 2:
                stretch_sequence.append(2)

        while True:
            if high - low <= 0.01:
                return (self.expand, 0, 0)
            mid = (low + high) / 2.0
            for strch in stretch_sequence:
                if (mid, strch) not in p_probes:
                    g_low = p_probes.get((low, 0), p_probes.get((low, dir_sign)))
                    g_high = p_probes.get((high, 0), p_probes.get((high, dir_sign)))

                    target_delta = None
                    if g_low is not None and g_high is not None:
                        target_delta = get_target_delta(g_low, g_high)

                    is_target_in_cache = (pid, target_delta) in self.shape_cache if target_delta is not None else False
                    pri = 1 if (is_target_in_cache or (high - low) < 0.02) else 2
                    return (mid, strch, pri)

            cached_vals = [p_probes[mid, s] for s in stretch_sequence if p_probes.get((mid, s)) is not None]
            if not cached_vals:
                best_delta = 0
            else:
                best_delta = max(cached_vals) if dir_sign == 1 else min(cached_vals)
            if (dir_sign == 1 and best_delta > 0) or (dir_sign == -1 and best_delta < 0):
                low = mid
            else:
                high = mid

    def initial_probes(self, state, page, npages, restart=False):
        """
        Executes vectorized full-document layout sweeps.
        Calls evaluate_paragraph_probe(pid) as a completely stateless helper.
        """
        all_pids = self.hooks.get_paragraphs_for_pages(page, page + npages)
        last_page = page + npages
        for a in ((self.minexp, -1), (self.maxexp, 1)):
            sweep_params = {pid: a for pid in all_pids}
            layout = self.hooks.run_layout(self, sweep_params, state.float_anchors, -1, last_page, prompt=",")
            self.collect_probes(layout, all_pids, sweep_params, page=page)

        logging.log(15, f"{self.probe_cache=}, {self.shape_cache=}")
        sweep_count = 0
        while True:
            sweep_count += 1
            sweep_params = {pid: (self.expand, 0) for pid in all_pids}
            requests = {}
            global_max_pri = 0
            pri_counts = {0: 0, 1: 0, 2: 0}
            pri2_pids = []
            for pid in all_pids:
                exp, strch, pri = self.evaluate_paragraph_probe(pid)
                pri_counts[pri] += 1
                if pri > 0:
                    requests[pid] = (exp, strch, pri)
                    if pri > global_max_pri:
                        global_max_pri = pri
                if pri == 2:
                    pri2_pids.append(pid)
            logging.log(15, 
                f"[Sweep #{sweep_count}] Priorities -> Pri2: {pri_counts[2]}, Pri1: {pri_counts[1]}, Pri0: {pri_counts[0]}, {requests=}"
            )
            if global_max_pri != 2:
                logging.log(15, f"[Sweep #{sweep_count}] No Priority 2 probes remaining. Exiting sweep loop.")
                break
            if len(pri2_pids) <= 5:
                logging.log(15, f"[Sweep #{sweep_count}] Active Pri2 Stragglers: {pri2_pids}")
            for pid, (exp, strch, pri) in requests.items():
                sweep_params[pid] = (exp, strch)
            layout = self.hooks.run_layout(self, sweep_params, state.float_anchors, -1, last_page, prompt=",")
            logging.log(15, f"run_layout result = {layout.result}")
            self.collect_probes(layout, all_pids, sweep_params, page=page)
            p = ProgressEvent(self.bk, sweep_count, "probe", "", self.numpages)
            p.total = 10
            self.hooks.progress(p)

        sweep_params = {pid: (self.expand, 0) for pid in all_pids}
        layout = self.hooks.run_layout(self, sweep_params, state.float_anchors, -1, last_page, prompt=",")
        return layout

    def run_layout(self, page_base_params, state, combo, page, start, allpages=False):
        #params = dict(self.base_params)
        mpri = 3
        while mpri == 3:
            params = dict(page_base_params)
            for p, d in combo.items():
                (e, s, bad) = self.shape_cache[(p, d)]
                params[p] = (e, s)
            self.probe_params = dict(params)
            if allpages or self.numpages <= 2 * self.lookahead or self.numpages - page < 1.5 * self.lookahead:
                npages = self.numpages - page + 1
            else:
                npages = self.lookahead
            probe_pids = self.hooks.get_paragraphs_for_pages(page+1, page + npages)
            mpri = 0
            logmodpids = []
            if not self.noprobe:
                for pid in probe_pids:
                    if pid in combo:
                        continue
                    exp, strch, pri = self.evaluate_paragraph_probe(pid)
                    if exp != self.expand or strch != 0:
                        self.probe_params[pid] = (exp, strch)
                        logmodpids.append(pid)
                    if pri == 2 and self.hooks.get_first_page_for_para(pid) == page+1:
                        pri = 3
                    if pri > mpri:
                        mpri = pri
            if mpri == 0:
                if self.numpages <= 2 * self.lookahead or page + npages >= self.numpages:
                    self.noprobe = True
                npages = 2      # need to look ahead ready for the next page to process
            logger.log(15, f"{page}+{npages}, probing={not self.noprobe}, {logmodpids=}, {mpri=}")
            # logger.log(15, "BASE %s", {p:v for p,v in self.base_params.items() if v!=(1.0,0)})
            layout = self.hooks.run_layout(self, self.probe_params, state.float_anchors, start, page+npages)
            self.collect_probes(layout, probe_pids, self.probe_params, page=page)
            if layout is None:
                return None
        self.itercount += 1
        logger.log(15, "layout_run [%s] iter=%s  probe=%s underfill=%s combo=%s",
                page, self.itercount, not self.noprobe,
                str({i: lp.column_free_lines for i, lp in enumerate(layout.pages) if lp.column_free_lines is not None and (page is None or i <= page+2)}),
                combo)
        self.collect_probes(layout, probe_pids, self.probe_params, page=page)
        res = EngineState(params, state.float_anchors, layout, self.hooks.printer.parlocs, page)
        if page + npages >= self.numpages:
            res.complete = True
        return res

    def collect_probes(self, layout, paragraphs, params, isbase=False, page=0):
        def test_para(p, r):
            pid = p.pid()
            e, s = params[pid]
            d = self.probe_cache.get(pid, {}).get((e, s), None)
            if d is None:
                return True
            (eo, so, b) = self.shape_cache.get((p, d), (None, None, None))
            if eo == e and so == s and b is None:
                return True
            return False
        self.hooks.analyse_bw(test_para, page)
        changes = []
        for p in paragraphs:
            e, s = params.get(p, (self.expand, 0))
            par = self.hooks.get_para(p)
            if par is None:
                if p not in self.probe_cache or (e, s) not in self.probe_cache[p]:
                    self.probe_cache.setdefault(p, {})[(e, s)] = None
                continue
            if par.rects is not None:
                blacks = sum(r.black for r in par.rects)
                whites = sum(r.white for r in par.rects)
            else:
                (blacks, whites) = (0, 0)
            whiteness = whites / (blacks + whites + .01)
            badness = self.badness_modify(p, e, s, whiteness, isbase=isbase)
            logging.log(15, f"{p}: ({e}, {s}) {whiteness=:.5f} {badness=:.5f} {whites=} {blacks=}")
            if (p, 0) not in self.shape_cache:
                self.shape_cache[(p,0)] = (self.expand, 0, whiteness)
                self.probe_cache.setdefault(p, {})[(self.expand, 0)] = 0
            base = self.baseline_lines.get(p)
            if base is None:
                logger.log(15, f"{p} missing from base_lines")
                continue
            new = layout.paragraph_total_lines.get(p, None)
            if new is None or p not in params:
                continue
            delta = new - base
            self.probe_cache.setdefault(p, {})[(e, s)] = delta
            if delta == 0:
                continue
            key = (p, delta)
            sc = self.shape_cache.get(key, None)
            if not isbase:
                base_whiteness = self.shape_cache[(p, 0)][2]
                threshold = base_whiteness + (self.hooks.badness_spacing_tolerance * base_whiteness) ** 4
                if whiteness > threshold:
                    logging.log(15, f"{p} ({e}, {s}) {whiteness=} {threshold=} {base_whiteness=}")
                    continue
            d = self.badness_cmp((e, s, badness), sc)
            if d < 0:
                self.shape_cache[key] = (e, s, badness)
                changes.append((key, e, s, badness))
        logging.log(15, f"{changes=}") 

    def generate_combos(self, paragraphs, state, page) -> Generator[Dict[Any, int], None, None]:
        yield {}
        moves = []
        pset = set(paragraphs)
        lpars = state.layout.get_pars(page)
        first_para = lpars[0] if len(lpars) else None
        first_para_adj = 0
        if first_para is not None and page - 1 not in state.layout.paragraph_pages[first_para]:
            first_para = None
        if first_para is not None:
            l = self.hooks.get_lines_for_para_page(first_para, page)
            if state.paragraph_params.get(first_para, (self.expand, 0)) != (self.expand, 0):
                first_para_adj = 1
            elif l == 0:
                pass
            elif l < 4:
                first_para_adj = (1 - l)
        last_para = lpars[-1] if len(lpars) else None
        for (p, d), (e, s, score) in self.shape_cache.items():
            if p not in pset or d == 0 or d is None or p is None or score is None:
                continue
            moves.append((score, p, d))
        moves.sort()
        by_para = {}
        for score, p, d in moves:
            by_para.setdefault(p, []).append((score, d))
        plist = list(by_para.keys())
        max_r = min(5, int(8 / log10(max(5, len(plist)))))
        all_combos = []
        seen_col_sigs = {}
        colfree = state.layout.pages[page].column_free_lines
        logger.log(15, f"{first_para=} {last_para=}, {max_r=}, {colfree=}, {moves=}, {lpars=}")
        if colfree is None:
            collengths = [0, 0]
        elif len(colfree) == 2:
            collengths = [colfree[0], colfree[0]+colfree[1]]
        elif len(colfree) == 1:
            collengths = [colfree[0], colfree[0]]
        count = 0
        for r in range(1, max_r + 1):
            for pars in itertools.combinations(plist, r):
                if state.paragraph_params.get(pars, (self.expand, 0)) != (self.expand, 0):
                    continue
                if count > 100:
                    break
                count += 1
                delta_lists = sorted(by_para[p] for p in pars)
                for choice in itertools.product(*delta_lists):
                    score = sum(s for s, _d in choice) + 0.1 * len(choice)
                    combo = {p: d for p, (s, d) in zip(pars, choice)}
                    # have we done the same net col line change before?
                    col_deltas = [0, 0, 0, 0, 0, 0]
                    # skip if another page has modified this para
                    if any(self.base_params.get(p, (self.expand, 0)) != (self.expand, 0) for p in combo.keys()):
                        continue
                    for p, d in combo.items():
                        if (p, d) not in self.shape_cache:
                            break
                        # mask = 1 = col1, 2 = col2, 3 = both
                        # col_deltas: 0 = first, 1 = both, 2 = last, 3 = col1 only, 4 = col2 only
                        mask = state.layout.paragraph_pages[p].get(page, 0)
                        if mask == 3:
                            col_deltas[1] += d
                        elif p == first_para:
                            if first_para_adj == 1 or first_para_adj < 0 and first_para_adj >= d:
                                break
                            col_deltas[0] += d
                        elif p == last_para and (d > 1 or page+1 in state.layout.paragraph_pages[p]):
                            col_deltas[2] += d
                        elif mask != 0:
                            col_deltas[mask + 2] += d
                        else:
                            logger.log(12, "Can't find mask for {p}")
                            col_deltas[5] += d
                        prev = self.hooks.get_previous(p)
                        preve = self.shape_cache.get((p, combo.get(p, 0)), (self.expand, 0))[0]
                        pe = self.shape_cache[(p, d)][0]
                        score += self.hooks.badness_contrast_factor * abs(pe - preve)
                    else:
                        if collengths[0] > 0 and 0 <= col_deltas[0] + col_deltas[1] + col_deltas[3] < collengths[0]:
                            logger.log(12, f"Rejecting against col 1 {col_deltas} {combo}")
                            continue
                        if collengths[1] > 0 and 0 <= sum(col_deltas) < collengths[1]:
                            logger.log(12, f"Rejecting against col 2 {col_deltas}, {combo}")
                            continue
                        sig = tuple(col_deltas)
                        (oldscore, oldcombo) = seen_col_sigs.get(sig, (10000, None))
                        if score < oldscore:
                            seen_col_sigs[sig] = (score, combo)
                        else:
                            continue
        all_combos = sorted(list(seen_col_sigs.values()), key=lambda x: (x[0], len(x[1])))
        logger.log(12, f"{all_combos=}")
        for _, combo in all_combos:
            yield combo

    def _para_order(self, pid):
        try:
            i = self.paragraph_order.index(pid)
        except ValueError:
            i = len(self.paragraph_order)
        return i

    def get_candidate_paragraphs(self, state, page):
        logger.debug(f"{state.layout.paragraph_pages=}")
        start = max(0, page - 4)
        pars = self.hooks.get_paragraphs_for_pages(page, page, state=state)
        pars.sort(key=self._para_order)
        return pars

    def get_probe_paragraphs(self, page):
        return self.hooks.get_paragraphs_for_pages(page, page + 1)

    def combo_badness(self, combo):
        score = 0
        boundary = False
        for p, d in combo.items():
            (e, s, bad) = self.shape_cache.get((p, d), (None, None, None))
            if e is None:
                score += 1000
            else:
                score += bad
        return score

    def badness_modify(self, p, e, s, badness, isbase=False):
        exp = math.sqrt(abs(self.expand - e))
        badness += self.hooks.badness_expansion_factor * exp * (badness ** 4)
        expxtra = exp * self.hooks.badness_expansion_cost
        if expxtra > 0.:
            badness += expxtra
        is_header = self.hooks.is_header(p)
        if not isbase and is_header:
            badness += 10
        return badness

    def badness_cmp(self, a, b):
        ''' returns -1 if a is better than b, returns 1 if b better than a.
            a, b= (e, s, badness) '''
        if b is None:
            return -1
        if a is None:
            return 1
        ea = abs(a[0] - 1)
        eb = abs(b[0] - 1)
        r = cmp(ea, eb)
        if r != 0:
            return r
        r = cmp(a[2], b[2])
        if r != 0:
            return r
        r = cmp(a[1], b[1])
        return r


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


class PTXFiller:

    reunderfill = re.compile(r"^Underfill\[(\S+?)\]:\s+\[(\d+?)\]\s+ht=([\d.]+?)pt,\s+space=([\d.]+?)pt,\s+baseline=([\d.]+)pt")

    def __init__(self, build_params, nid, progress_q=None):
        super().__init__()
        self.nid = nid
        self.timedout = False
        self.cancelled = False
        self.progress_queue = progress_q
        self.view = ViewModel(*[getattr(build_params, x) for x in ('prjtree config macrosdir args'.split())])
        self.view.setup_ini()
        self.view.setPrjid(build_params.pid, build_params.guid, loadConfig=False, startup=True)
        self.view.setConfigId(build_params.cfgid)
        self.rtl = self.view.get("fcb_textDirection", "") == "rtl"
        self.macrosdir = build_params.scriptsdir
        self.view.project.ext = None
        self.stats = []
        if nid is not None:
            self.view.project.ext = f"pbuild{nid}"
            d = self.view.project.printPath(self.view.cfgid)
            if os.path.exists(d):
                import time as _time
                for f in os.listdir(d):
                    fp = os.path.join(d, f)
                    if not os.path.isfile(fp):
                        continue
                    for attempt in range(4):
                        try:
                            os.unlink(fp)
                            break
                        except PermissionError:
                            if attempt < 3:
                                _time.sleep(0.5)
                            else:
                                logger.warning(f"Cannot delete {fp} — file still locked; skipping")

    def solve(self, bk, stop=False, restart=False):
        self.bk = bk        # needed by run()
        if bk not in self.view.getAllBooks().keys():
            return None
        #def _print(level, s, *a):
        #    print(bk+": "+(s % a))
        #logger.log = _print
        self.view.set("c_allowUnbalanced", True)
        self.view.set("r_book", "single")
        self.view.set("ecb_book", bk)
        # suppress peripherals
        for a in """c_inclFrontMatter c_autoToC c_frontmatter c_inclMaps c_useSectIntros c_makeCoverPage
                    c_colophon c_inclBackMatter c_extradvproc c_inclSettingsInPDF c_applyWatermark
                    c_cropmarks c_extractInserts c_printArchive""".split():
            self.view.set(a, False)
        self.view.set("fcb_pagesPerSpread", 1)
        self.view.set("fcb_outputFormat", "Screen")
        self.view.savePics()
        self.view.saveStyles()
        self.hooks = Hooks(self, None)
        self.job = None
        self.hascash = False
        #print(f"Filling {bk}")
        if restart:
            adjlist = self.view.get_adjlist(bk, save=False)
            parms = adjlist.get_params()
        else:
            parms = {}
        unlockme()
        font_info = self.view. get("bl_fontR")
        try:
            self.expand = float(font_info.feats.get('extend', "1"))
        except ValueError:
            self.expand = 1
        try:
            self.minexp = float(self.view.get("s_shrinktextlimit", "95")) / 100
        except ValueError:
            self.minexp = 0.95 * self.expand
        try:
            self.maxexp = float(self.view.get("s_maxtextlimit", "105")) / 100
        except ValueError:
            self.maxexp = 1.05 * self.expand
        init_layout = self.hooks.run_layout(None, parms, {}, -1, -1, genfiles=True)
        self.init_adjs = self.adjs
        if init_layout is None:
            printbk(bk, "!")
            return (False, f"Failed: {bk}")
        #print(f"Init laid out {bk}")
        if restart and init_layout.first_failing_page is None:
            np = self.parlocs.numPages()
            if np > 0:
                self.progress(ProgressEvent(bk, np, "already_filled", total=np))
                printbk(bk, "\u2713")
                return (True, f"Complete {bk} Already good")
            else:
                self.progress(ProgressEvent(bk, 0, "failed", msg="No page data"))
                printbk(bk, "x")
                return (False, f"Failed: {bk} No page data")
        pids = list(init_layout.paragraph_pages.keys())
        logger.log(15, f"lastwidths={', '.join(f'{p}={self.get_para(p).lastwidth:.2f}' for p in pids if isinstance(p, ParInfo))}")
        state = EngineState(parms if restart else {p: (self.expand, 0) for p in pids}, [], init_layout, self.parlocs, 0)
        self.hooks.basestate = state
        self.hooks.chapters = self.parlocs.chapters
        starttime = time()
        #print(f"Solving {bk}")
        solver = TypesetterSolver(self.hooks, pids, expand=self.expand, minexp=self.minexp, maxexp=self.maxexp)
        if restart:
            solver.shape_cache, solver.probe_cache = adjlist.get_cache()
        res = solver.solve(state, start_page=-1, stop=stop, restart=restart, book=bk)
        if isinstance(res, HumanFixRequest):
            state = res.state
            page = res.page
        else:
            state = res
            page = state.page
        if self.filter_params(state.paragraph_params, solver, page):
            self.createAdjs(state.paragraph_params, solver)
        endtime = time()
        unlockme()
        self.job.pdffile = os.path.join(re.sub(r"\.\./?", "", os.path.dirname(self.job.pdffile)),
                os.path.basename(self.job.pdffile))
        self.job.xdvtopdf(self.job.outfname, self.job.pdffile)
        logger.log(15, f"shape_cache={solver.shape_cache}")
        if isinstance(res, HumanFixRequest):
            retval = (False, f"{res.message} at {bk} page {res.page} after {endtime-starttime}s")
            self.progress(ProgressEvent(bk, res.page, 'failed', res.message, -1))
            printbk(bk, "T")
        else:
            retval = (True, f"Complete {bk}, failures={res.failures}, after {solver.itercount} runs after {endtime-starttime}s")
            msg = f"Failed: {' '.join(str(x) for x in res.failures)}" if res.failures else _("All done")
            self.progress(ProgressEvent(bk, 0, "complete", msg, -1))
            printbk(bk, "Y")
        if len(self.stats):
            print(f"\n{bk}: mean={statistics.mean(self.stats)}, median={statistics.median(self.stats)}, sd={statistics.stdev(self.stats)}, quantiles={statistics.quantiles(self.stats)}")
        return retval
        
    def createAdjs(self, parparms, solver, lastchap=0):
        def mkkey(s):
            (r, para) = self.pidkey(s)
            key = f"{r[5]}" if r[1] == 0 and r[5] else f"{r[1]}.{r[2]}{r[5]}"
            return key, para
        def getchap(key):
            c, _d = key.split('.', 1) if '.' in key else (key, None)
            try:
                c = int(c)
            except ValueError:
                c = 0
            return c
        tname = self.view.getLocalTriggerFilename(self.bk)
        fname = self.view.getAdjListFilename(self.bk)
        adjfname = os.path.join(self.view.project.srcPath(self.view.cfgid), "AdjLists", fname)
        if not hasattr(self, 'init_adjs'):
            self.adjs = AdjList(int(self.expand*100), int(self.minexp*100), int(self.maxexp*100), fname=adjfname, gtk=None)
        else:
            self.adjs = self.init_adjs.copy()
        logger.log(12, f"{self.bk}: {parparms=}")
        for s, p in parparms.items():
            key, para = mkkey(s)
            c = getchap(key)
            if lastchap == 0 or lastchap > int(c):
                self.adjs.setval(self.bk, key, para, p[1], None, expand=int(p[0]*100), append=True)
        if solver is not None:
            for s in solver.paragraph_order:
                key, para = mkkey(s)
                c = getchap(key)
                if lastchap != 0 and lastchap <= int(c):
                    break
                for a in range(-2, 3):
                    if a == 0:
                        continue
                    keyv = f"{'p' if a > 0 else 'm'}{abs(a)}"
                    if (s, a) in solver.shape_cache:
                        e, t, badness = solver.shape_cache[(s, a)]
                        v = f"{int(e*100)}" if t == 0 else f"{int(e*100)}{t:+1d}"
                        # print(f"{s}@{a}={e},{t} into {key},{keyv}={v}")
                    else:
                        v = None
                    self.adjs.setdb(self.bk + " " + key, keyv, v)
        self.adjs.createAdjlist()
        tname = self.view.getLocalTriggerFilename(self.bk)
        tpath = os.path.join(self.view.project.printPath(self.view.cfgid), tname)
        self.adjs.createTriggerlist(fname=tpath)

    def run_layout(self, solver, parparms, floats, lastpage, genfiles=False, prompt="."):
        if self.timedout:
            raise TimeoutError()
        if lastpage <= 0 or getattr(self, 'parlocs', None) is None:
            stopchap = 0
        else:
            stopchap = self.hooks.chap_from_page(lastpage) + 1
        self.view.set("s_stopat", stopchap)
        logging.log(15, f"{stopchap=}")
        self.createAdjs(parparms, solver, lastchap=stopchap)
        if self.job is None:
            self.job = RunJob(self.view, self.view.scriptsdir, self.macrosdir, self.view.args)
            self.job.norun = True
            self.job.nopdf = True
            self.job.silent = True
            self.job.doit(noview=True, noaction=not genfiles)
            self.job.maxRuns = 1

        if floats is not None and len(floats):
            piclist = self.view.picinfos.copy()
            for k, v in floats.items():
                key = re.sub(r"-preverse$", "", k)
                if v.ref is not None:
                    p = piclist.pop(key)
                    piclist[v.ref] = p
                if v.col is not None:
                    p = piclist.get(key, None)
                    if p is None:
                        continue
                    pos = p['pgpos']
                    if v.col == 2:
                        pos = pos[0] + "r" if pos in ("tl", "bl") else pos
                    elif v.col == 1:
                        pos = pos[0] + "l" if pos in ("tr", "br") else pos
                    p['pgpos'] = pos
            self.job.piclist = piclist
        else:
            self.job.piclist = None

        if not hasattr(self.job, 'outfname'):
            raise FileNotFoundError(self.view.getBooks())
        self.job.run_xetex(self.job.outfname, self.job.pdffile)
        parlocsfile = self.job.outfname.replace(".tex", ".parlocs")
        self.parlocs = Paragraphs()
        self.parlocs.readParlocs(parlocsfile, self.rtl)
        self.pidmap = {p.pid(): i for i, p in enumerate(self.parlocs) if isinstance(p, ParInfo)}
        self.badnesses = {p.pid(): p.badness for p in self.parlocs if isinstance(p, ParInfo)}
        logfile = self.job.outfname.replace(".tex", ".log")
        self.parselog(logfile)
        print(".", flush=True, end="")
        return self.job.res

    def progress(self, pEvent):
        if self.progress_queue is None:
            return
        if not pEvent.total:
            np = self.parlocs.numPages()
            pEvent.total = np
        self.progress_queue.put(pEvent)

    def get_pidmap(self):
        res = {}
        for p in self.parlocs:
            if not isinstance(p, ParInfo):
                continue
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
        s = m.group(1)
        if s.startswith("k."):
            s = "k." + re.sub(r"[^a-zA-Z0-9]", "", s[2:])
        try:
            c = int(m.group(2) or 0)
        except ValueError:
            c = 0
        return (refSort(s), c)

    def get_plines(self):
        plines = {p.pid(): p.lines for p in self.parlocs if isinstance(p, ParInfo)}
        return plines

    def get_para_ind(self, pid):
        return self.pidmap.get(pid, len(self.parlocs))

    def get_para(self, pid):
        pindex = self.pidmap.get(pid, None)
        if pindex is not None and pindex < len(self.parlocs):
            return self.parlocs[pindex]
        return None

    def get_previous(self, pid, page=None):
        pindex = self.pidmap.get(pid)
        if pindex is None:
            return None
        while pindex > 0:
            pindex -= 1
            p = self.parlocs[pindex]
            if isinstance(p, ParInfo):
                if page is None:
                    return p.pid()
                elif page in self.pidmap[p.pid()]:
                    return p.pid()
                else:
                    return None
        return None

    def get_paragraph_start_page(self, pid):
        p = self.get_para(pid)
        if p is None:
            return 1000000
        return min([r.pagenum for r in p.rects]) - 1

    def get_paragraph_end_page(self, pid):
        p = self.get_para(pid)
        if p is None:
            return 1000000
        return max([r.pagenum for r in p.rects]) - 1

    def get_lines_para_page(self, pid, page):
        p = self.get_para(pid)
        if p is None:
            return 0
        res = 0
        for r in p.rects:
            if r.pagenum == page + 1:
                res += r.lines
        return res

    def isheader_column_start(self, pid):
        pi = self.get_para_ind(pid)
        if pi < len(self.parlocs):
            p = self.parlocs[pi]
            pnum = p.rects[0].pagenum
            if self.parlocs[self.parlocs.pindex[pnum]].pid() == pid:
                return self.isheader(p.mrk)
        return False

    def pid_isheader(self, pid):
        pind = self.get_para_ind(pid)
        if pind < len(self.parlocs):
            p = self.parlocs[pind]
            return self.isheader(p.mrk)
        return False

    def pid_isjustified(self, pid):
        pind = self.get_para_ind(pid)
        if pind < len(self.parlocs):
            p = self.parlocs[pind]
            just = self.view.styleEditor.getval(p.mrk, 'justification', None)
            if just is not None and just.lower() != 'justified':
                return False
        return True

    def isheader(self, mrk):
        return Grammar.marker_categories.get(mrk, '') in ("sectionpara", "title")

    def parselog(self, fname):
        self.underfills = GrowList()
        with open(fname, encoding="utf-8") as inf:
            for i, l in enumerate(inf.readlines()):
                m = self.reunderfill.match(l)
                if m:
                    pnum = int(m.group(2))
                    pnum = self.parlocs.pnums.get(pnum, pnum) - 1
                    side = 0 if m.group(1) == "A" else 1
                    lines = int((float(m.group(4)) - float(m.group(3))) / float(m.group(5)) + 0.1)
                    if lines > 5:
                        logger.log(15, f"{m.groups()=}, {lines=}")
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
                elif l.startswith("Underfill"):
                    logger.warn(f"Unparsed underfill {l} at line {i+1}")

    def read_badnesses(self):
        xdvname = self.job.outfname.replace(".tex", ".xdv")
        xdvreader = SpacingOddities(xdvname, parent=self.parlocs,
                                    fontsize=float(self.view.get("s_fontsize", 1)))
        for (opcode, data) in xdvreader.parse():
            pass
        self.parlocs.getnbadspaces()

    def filter_params(self, params, solver, page):
        if page is None:
            page = -1
        res = False
        lastp = 0
        for pid, (e, s) in list(params.items()):
            p = self.get_paragraph_end_page(pid) or lastp
            lastp = p
            if p <= page:
                continue
            params[pid] = (self.expand, 0)
            res = True
        return res

    def analyse_bw(self, testfn, page):
        xdvname = self.job.outfname.replace(".tex", ".xdv")
        xdv = XdvSpaceMeasure(xdvname, self.parlocs, testfn=testfn, page=max(page, 0))
        for (opcode, data) in xdv.parse():
            pass
        

