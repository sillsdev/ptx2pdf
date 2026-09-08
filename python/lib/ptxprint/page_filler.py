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
    paragraph_pages: Dict[ParagraphRef, List[Dict[PageIndex, ColMask]]]     # pidmap
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
                  ("contrast_factor", "pbcontrast"),
                  ("backtrack", "pbbacktrack"),
                  ("maxr", "pbmaxr")):
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

    def get_lines_for_para_page(self, para: ParagraphRef, page: PageIndex, state=None):
        return self.printer.get_lines_para_page(para, page, state=state)

    def get_paras_for_col(self, page, col, state=None):
        if state is None:
            state = self.basestate
        return state.layout.get_pars(page, col)

    def get_first_page_for_para(self, para):
        return self.printer.get_paragraph_start_page(para)

    def get_page_para_key(self, page, state=None):
        p = self.printer.get_page_first_pid(page, state=state)
        r = self.printer.get_lines_para_page(p, page, state=state)
        return (p, r)

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

    def analyse_bw(self, testfn, page, trackp=False):
        self.printer.analyse_bw(testfn, page, trackp=trackp)

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

    def __init__(self, hooks, pids, expand=1., minexp=0.95, maxexp=1.05, backtrack=None):
        self.hooks = hooks
        self.paragraph_order = pids
        self.expand = expand
        self.minexp = minexp
        self.maxexp = maxexp
        self.backtrack_depth = hooks.badness_backtrack if backtrack is None else backtrack
        self.regression_depth = self.backtrack_depth
        self.probe_cache: Dict[[Any], Dict[Tuple[float, int], int]] = {}
        self.shape_cache: Dict[Tuple[Any, int], Tuple(float, int, float)] = {}
        self.probe_params = {}
        self.full_probe = True
        self.baseline_lines: Dict[Any, int] = {}
        self.base_params = {p: (expand, 0) for p in self.paragraph_order}
        self.tried = set()
        self.itercount = 0
        self.frozen_paragraphs = set()
        self.noprobe = False
        self.bk = None
        self.all_probes = [(expand, -1), (minexp, -1), ((minexp + expand) / 2, -1),
                (maxexp, 1), (maxexp, 0), (expand, 0)]

    def printbk(self, bk, page, progress=True, total=None):
        bkc = bkltrs[int(bookcodes[bk])-1] if bk is not None else ""
        print(bkc+str(page), flush=True, end="")
        if progress:
            pe = ProgressEvent(bk, page, "page", "")
            pe.total = total or self.numpages
            self.hooks.progress(pe)

    def solve(self, state, start_page: int = -1, stop: bool = True, restart: bool = False, book=None):
        """Top-level entry point: set up base params from a possible
        restart, run the initial lookahead probe, then drive the
        page-by-page solve forward.
            state: current EngineState.
            start_page: page already known-good to start after.
            stop: give up with HumanFixRequest on first unfixable page
                otherwise keep going
            restart: Continue from an existing paragraph configuration
            book: book being typeset, for progress reporting.
        Returns final EngineState, or a HumanFixRequest.
        """
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
        self.low_water = max(0, page - self.backtrack_depth)
        self.numpages = state.numPages()
        npages = (self.numpages - page + 1) if self.full_probe or self.numpages <= 2 * self.lookahead else self.lookahead
        try:
            layout = self.initial_probes(state, page, npages, restart=restart)
        except TimeoutError:
            return HumanFixRequest(state, page, "Stopped" if self.hooks.cancelled else "Timed out")

        state = EngineState(self.init_state.paragraph_params, state.float_anchors, layout,
                             self.hooks.printer.parlocs, 0)
        self.searched_start_keys = {}
        self.tried_combos = {}
        self.page_base_params = {}
        self.failed_starts = {}
        self.failed_pages = []
        return self.run_forward(state, page, start_page, stop)

    def run_forward(self, state, page, start_page, stop):
        """Drive the page-by-page solve from `page` onward, repairing
        earlier pages on failure and falling back to stop/skip-forward
        handling when repair can't fix things.
            state: current EngineState.
            page: page to start from.
            start_page: starting page for run_layout probes.
            stop: give up with HumanFixRequest on first unfixable page
                if True; skip it and keep going if False.
            Returns final EngineState, or a HumanFixRequest.
        """
        while True:
            # Find the next page that actually needs typesetting, or
            # detect completion / extend the lookahead probe.
            layout = state.layout
            nextpage = layout.first_failing_page
            logger.log(15, f"{page=}, {nextpage=}, is completed {state.complete}")
            if nextpage is None or nextpage == page:
                if state.complete:
                    logger.log(15, "solve_complete pages=%s, underfills=%s",
                               len(layout.pages),
                               str({i: lp.column_free_lines for i, lp in enumerate(layout.pages)
                                    if lp.column_free_lines is not None}))
                    state.failures = self.failed_pages
                    self.hooks.progress(ProgressEvent(
                        self.bk, (page or 0) + 1, "complete",
                        f"Failed: {' '.join(str(p) for p in self.failed_pages)}" if self.failed_pages else None,
                        self.numpages))
                    return state
                nextpage = state.numPages() - 1 if nextpage is None else nextpage + 1

            # don't reanalyse starting on a page we've already given up on
            while nextpage in self.failed_pages:
                if nextpage >= state.numPages() - 1:
                    state.failures = self.failed_pages
                    return state
                nextpage += 1

            # probe starting at the new page
            if not self.full_probe and state.numPages() - nextpage >= self.lookahead \
                                   and self.numpages >= 2 * self.lookahead:
                layout = self.initial_probes(state, nextpage, 10, progress=False)
                state = EngineState(self.init_state.paragraph_params, state.float_anchors,
                                     layout, self.hooks.printer.parlocs, nextpage)
            page = nextpage
            if self.low_water < page - self.backtrack_depth:
                self.low_water = page - self.backtrack_depth

            if page in self.failed_pages:
                # already given up on this page -- don't re-attempt it, and if there's nowhere 
                # left to go, we're as done as we're going to get.
                if page >= state.numPages() - 1:
                    return state
                state.layout.first_failing_page = page
                while state.layout.first_failing_page is not None and state.layout.first_failing_page == page:
                    state.layout.next_bad()
                continue

            try:
                new_state, ok = self.attempt_page(state, page, start_page)
            except TimeoutError:
                return HumanFixRequest(state, page + 1, "Stopped" if self.hooks.cancelled else "Timed out")

            if ok:
                # we're good for this page
                state = new_state
                self.hooks.progress(ProgressEvent(self.bk, state.layout.first_failing_page or state.numPages(),
                                                "goodpage", "", self.numpages))
                self.init_state = state
                continue

            # did we mess up something earlier?
            if new_state.layout.first_failing_page is not None and new_state.layout.first_failing_page < page:
                target, avoid_key, max_depth = new_state.layout.first_failing_page, None, self.regression_depth
            else:
                # backtrack and try a previous page to help us do better
                target = page - 1
                avoid_key = self.hooks.get_page_para_key(page, state=state)
                max_depth = self.backtrack_depth

            try:
                state, fixed = self.repair(state, target, start_page,
                                            avoid_key=avoid_key, floor=self.low_water)
            except TimeoutError:
                msg = "Stopped" if self.hooks.cancelled else "Timed out"
                self.hooks.progress(ProgressEvent(self.bk, page, "failed", msg, self.numpages))
                return HumanFixRequest(state, page, msg)

            if fixed:
                continue

            # Couldn't fix `page` -- ordinary failed-page handling.
            state.layout.first_failing_page = page
            while state.layout.first_failing_page is not None and state.layout.first_failing_page == page:
                state.layout.next_bad()
            self.failed_pages.append(page)
            if state.layout.first_failing_page is None and state.complete:
                msg = f"Failed: {' '.join(str(p) for p in self.failed_pages)}"
                self.hooks.progress(ProgressEvent(self.bk, page+1, "complete", msg))
                return HumanFixRequest(state, page + 1, msg)
            if state.layout.first_failing_page is None or state.layout.first_failing_page > page:
                self.hooks.progress(ProgressEvent(self.bk, page + 1, "badpage", "", self.numpages))
            start_page = state.layout.first_failing_page or state.numPages() + 1
            continue

    def attempt_page(self, state, page, start, avoid_key=None):
        """Search `page` for a sufficient combo.
            state: current EngineState.
            page: page to solve.
            start: starting page for run_layout probes.
            avoid_key: if given, reject candidates whose resulting
                start key for page + 1 equals this, or is already
                known-dead in self.failed_starts.
            Returns (new_state, success)
        """
        if page >= state.numPages():
            state = self.run_layout(self.base_params, state, {}, page, start)

        page_base_params = self.page_base_params.get(page, dict(self.base_params))
        self.printbk(self.bk, page)
        startcount = self.itercount

        for combo in self.next_combination(state, page):
            if self.hooks.cancelled:
                raise TimeoutError("Stopped")
            if not combo and self.itercount > 0:
                continue
            if self.itercount - startcount > 200:
                break

            new_state = self.run_layout(page_base_params, state, combo, page, start)

            if page < len(new_state.layout.pages):
                free = new_state.layout.pages[page].column_free_lines
            else:
                free = None

            if free is not None and any(x > 5 for x in free):
                logger.log(15, "Skipping combo for large gap")
                continue

            if (new_state.layout.first_failing_page is not None
                    and new_state.layout.first_failing_page < page):
                logger.log(15, f"Rejecting combo: invalidates earlier page "
                                f"{new_state.layout.first_failing_page} < {page}")
                continue

            if avoid_key is not None:
                next_key = self.hooks.get_page_para_key(page + 1, state=new_state)
                if next_key == avoid_key or next_key in self.failed_starts.get(page + 1, set()):
                    continue

            if not self.noprobe and (free is None or all(x == 0 for x in free)):
                lpars = state.layout.get_pars(page)
                pps = state.layout.paragraph_pages[lpars[-1]]
                if len(pps) > 1 and lpars[-1] in self.probe_params:
                    self.noprobe = True
                    new_state = self.run_layout(page_base_params, state, combo, page, start)
                    logger.log(15, f"Test run for good page, without probes "
                                    f"{new_state.layout.first_failing_page=}")
                    self.noprobe = False
                    free = new_state.layout.pages[page].column_free_lines
                if (new_state.layout.first_failing_page is not None
                        and new_state.layout.first_failing_page < page):
                    logger.log(15, "Rejecting combo: noprobe retest invalidates "
                                   f"earlier page {new_state.layout.first_failing_page} < {page}")
                    continue

            if (new_state.layout.first_failing_page is None
                    or new_state.layout.first_failing_page > page
                    or free is None or not len(free) or all(x == 0 for x in free)):
                logger.log(15, "page_solved page=%s iterations=%s", page, self.itercount)
                logger.log(15, f"Winning params {','.join(str(v) for v in new_state.paragraph_params.items() if v[1] != (1.0, 0))}")
                self.base_params = dict(new_state.paragraph_params)
                new_state.passed = True
                return new_state, True

            state = new_state

        logger.log(15, "page_failed page=%s", page)
        self.failed_starts.setdefault(page, set()).add(self.hooks.get_page_para_key(page, state=state))
        state = self.run_layout(page_base_params, state, {}, page, start)
        state.passed = False
        return state, False

    def repair(self, state, page, start, avoid_key, floor=0):
        """Try to give `page` a different combo, cascading backward
        (floor: page 0) if it has none left.
            state: current EngineState.
            page: page to repair.
            start: starting page for run_layout probes.
            avoid_key: carry-over key page's new combo must not
                reproduce for page + 1 (None = no filter).
            max_depth: counts down depth to 0 (None = unbounded).
            Returns (state, success)
        """
        if page < floor:
            return state, False

        state, ok = self.attempt_page(state, page, start, avoid_key=avoid_key)
        if ok:
            return state, True   # attempt_page already committed base_params correctly

        earlier_avoid_key = self.hooks.get_page_para_key(page, state=state)
        return self.repair(state, page - 1, start,
                            avoid_key=earlier_avoid_key,
                            floor=floor)

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
                pos_low = max(pos_low, exp)

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
                neg_high = min(neg_high, exp)

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

    def initial_probes(self, state, page, npages, restart=False, progress=True):
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
            if progress:
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
            if allpages or self.full_probe or self.numpages <= 2 * self.lookahead \
                        or self.numpages - page < 1.5 * self.lookahead:
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
                if self.full_probe or self.numpages <= 2 * self.lookahead \
                                   or page + npages >= self.numpages:
                    self.noprobe = True
                npages = 2      # need to look ahead ready for the next page to process
            logger.log(15, f"{page}+{npages}, probing={not self.noprobe}, {mpri=}")
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
        if not self.noprobe:
            self.collect_probes(layout, probe_pids, self.probe_params, page=page)
        res = EngineState(params, state.float_anchors, layout, self.hooks.printer.parlocs, page)
        if page + npages >= self.numpages:
            res.complete = True
        return res

    def collect_probes(self, layout, paragraphs, params, isbase=False, page=0):
        def test_para(p, r):
            pid = p.pid()
            e, s = params.get(pid, (None, None))
            d = self.probe_cache.get(pid, {}).get((e, s), None)
            if d is None:
                return True     # not in the cache get data
            # we've probed this before
            (eo, so, b) = self.shape_cache.get((pid, d), (None, None, None))
            if eo == e and so == s and b is None:
                return True     # but if we have no badness then we want this
            return False
        e, s = params.get(list(params.keys())[len(params.keys()) // 2])
        self.hooks.analyse_bw(test_para, page, trackp=e == 1.025)
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
                parwhites = sum(r.parwhite / max(1, r.lines - 1) for r in par.rects)
                nwhites = sum(r.nspaces for r in par.rects)
            else:
                (blacks, whites, parwhites, nwhites) = (0, 0, 0, 0)
            # whiteness = whites / (blacks + whites + .01)
            whiteness = whites / (nwhites + 0.01)
            badness = self.badness_modify(p, e, s, whiteness, parwhites, isbase=isbase)
            if e == 1.025:
                logging.log(15, f"{p}: ({e}, {s}) {whiteness=:.5f} {badness=:.5f} {parwhites=} {whites=} {blacks=}")
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
                if parwhites < 0.01:
                    base_whiteness = self.shape_cache[(p, 0)][2]
                    # threshold = base_whiteness + (self.hooks.badness_spacing_tolerance * base_whiteness) ** 4
                    threshold = self.hooks.badness_spacing_tolerance
                    if whiteness > threshold:
                        logging.log(15, f"{p} ({e}, {s}) {whiteness=} {threshold=} {base_whiteness=}")
                        continue
            d = self.badness_cmp((e, s, badness), sc)
            if d < 0:
                self.shape_cache[key] = (e, s, badness)
                changes.append((key, e, s, badness))
        logging.log(15, f"{changes=}") 

    def next_combination(self, state, page):
        """Candidate combos for `page`, cheapest first. Resumes past
        combos already tried under this page's current start key;
        starts fresh if the key has changed since last searched.
            state: current EngineState.
            page: page to generate combos for.
        Returns combo dicts.
        """
        key = self.hooks.get_page_para_key(page, state=state)
        seen = self.searched_start_keys.setdefault(page, set())
        if key not in seen:
            seen.add(key)
            self.tried_combos[page] = set()
            self.page_base_params[page] = dict(self.base_params)
        tried = self.tried_combos[page]
        paragraphs = self.get_candidate_paragraphs(state, page)
        for combo in self.generate_combos(paragraphs, state, page):
            ckey = tuple(sorted(combo.items()))
            if ckey in tried:
                continue
            tried.add(ckey)
            yield combo

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
            l = self.hooks.get_lines_for_para_page(first_para, page, state=state)
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
        max_r = min(int(self.hooks.badness_maxr / log10(max(5, len(plist)))), len(plist))
        all_combos = []
        seen_col_sigs = {}
        colfree = state.layout.pages[page].column_free_lines if page < len(state.layout.pages) else None
        logger.log(15, f"{first_para=} {last_para=}, {max_r=}, {colfree=}, {moves=}")
        if colfree is None:
            collengths = [0, 0]
        elif len(colfree) == 2:
            collengths = [colfree[0], colfree[0]+colfree[1]]
        elif len(colfree) == 1:
            collengths = [colfree[0], colfree[0]]
        count = 0
        maxscore = 10000
        for r in range(1, max_r + 1):
            for pars in itertools.combinations(plist, r):
                if state.paragraph_params.get(pars, (self.expand, 0)) != (self.expand, 0):
                    continue
                delta_lists = sorted(by_para[p] for p in pars)
                for choice in itertools.product(*delta_lists):
                    score = sum(s for s, d in choice) + 0.1 * len(choice)
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
        logger.log(15, f"{all_combos=}")
        for _, combo in all_combos[:200]:       # 200 tests for a page better be enough!
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

    def badness_modify(self, p, e, s, badness, parbadness, isbase=False):
        exp = math.sqrt(abs(self.expand - e))
        badness += self.hooks.badness_expansion_factor * exp * badness
        expxtra = 10 * (e - self.expand) * self.hooks.badness_expansion_cost
        if expxtra > 0.:
            badness += expxtra
        # badness += math.sqrt(parbadness)
        badness += parbadness
        is_header = self.hooks.is_header(p)
        if not isbase and is_header:
            badness += 10
        return badness

    def badness_cmp(self, a, b):
        ''' returns -1 if a is better than b, returns 1 if b better than a.
            a, b = (e, s, badness) '''
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

    def printbk(self, bk, page, progress=True):
        bkc = bkltrs[int(bookcodes[bk])-1] if bk is not None else ""
        print(bkc+str(page), flush=True, end="")
        if progress:
            self.hooks.progress(ProgressEvent(bk, None, "page", ""))

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
            self.printbk(bk, "!")
            return (False, f"Failed: {bk}")
        #print(f"Init laid out {bk}")
        if restart and init_layout.first_failing_page is None:
            np = self.parlocs.numPages()
            if np > 0:
                self.progress(ProgressEvent(bk, np, "already_filled", total=np))
                self.printbk(bk, "\u2713", progress=False)
                return (True, f"Complete {bk} Already good")
            else:
                self.progress(ProgressEvent(bk, 0, "failed", msg="No page data"))
                self.printbk(bk, "x", progress=False)
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
            self.printbk(bk, "T", progress=False)
        else:
            retval = (True, f"Complete {bk}, failures={res.failures}, after {solver.itercount} runs after {endtime-starttime}s")
            msg = f"Failed: {' '.join(str(x) for x in res.failures)}" if res.failures else _("All done")
            self.progress(ProgressEvent(bk, 0, "complete", msg, -1))
            self.printbk(bk, "Y", progress=False)
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
        plocs = self.parlocs if state is None else state.parlocs
        res = set()
        colmask = {}
        for i in range(first + 1, last + 2):
            for p, r in plocs.getParas(i, inclast=True):
                res.add(p.pid())
                colmask[p.pid()] = colmask.get(p.pid(), 0) | (r.col + 1)
        return sorted(res, key=self.pidkey)

    def get_page_first_pid(self, page, state=None):
        plocs = self.parlocs if state is None else state.parlocs
        pfirst = None
        res = 0
        for p, r in plocs.getParas(page+1, inclast=True):
            if pfirst is None:
                return p.pid()
        return None

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

    def get_para_ind(self, pid, state=None):
        if state is not None:
            parlocs = state.parlocs
            pidmap = {p.pid(): i for i, p in enumerate(parlocs)}
        else:
            parlocs = self.parlocs
            pidmap = self.pidmap
        pindex = pidmap.get(pid, None)
        return pindex

    def get_para(self, pid, state=None):
        pindex = self.get_para_ind(pid, state=state)
        parlocs = self.parlocs if state is None else state.parlocs
        if pindex is not None and pindex < len(parlocs):
            return parlocs[pindex]
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

    def get_lines_para_page(self, pid, page, state=None):
        p = self.get_para(pid, state=state)
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

    def analyse_bw(self, testfn, page, trackp=False):
        xdvname = self.job.outfname.replace(".tex", ".xdv")
        xdv = XdvSpaceMeasure(xdvname, self.parlocs, testfn=testfn, page=max(page, 0), trackp=trackp)
        for (opcode, data) in xdv.parse():
            pass
        

