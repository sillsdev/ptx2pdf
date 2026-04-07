#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, Tuple, Any, Iterator, List, Set, Deque, Optional, Union, Generator, Iterable
from collections import deque, defaultdict
from configparser import ConfigParser
import heapq, re, os, logging, random, itertools, argparse, threading
import multiprocessing as mp
from math import sqrt, log10
from time import time, asctime
from ptxprint.parlocs import Paragraphs, ParInfo
from ptxprint.adjlist import AdjList
from ptxprint.runjob import RunJob, unlockme
from ptxprint.utils import refSort, bookcodes
from ptxprint.view import ViewModel
from ptxprint.project import ProjectList
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
class BuildParams:
    prjtree: ProjectList
    config: ConfigParser
    macrosdir: str
    args: argparse.Namespace
    pid: str
    guid: str
    cfgid: str
    scriptsdir: str
    loglevel: int
    timeout: int

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

    badness_stretch_tolerance   = 80   # avoid ±2
    badness_spacing_tolerance   = 1    # paragraph spacing distortion
    badness_shrink_preference   = 20   # + = prefer shrink, - = prefer stretch
    badness_header_aversion     = 60   # avoid headers
    badness_line_density_factor = 1.0  # wide vs narrow text
    badness_line_weight         = 12
    badness_lastline_weight     = 2
    badness_tex_weight          = 12

    def __init__(self, printer, state):
        self.printer = printer
        self.basestate = state
        vals = {k: getattr(self, k) for k in dir(self) if k.startswith("badness")}
        logger.log(15, f"Badness parameters = {vals}")

    def run_layout(self,
                   solver: Optional["Typesetter"],
                   paragraph_params: Dict[ParagraphRef, ParamSig],
                   float_anchors: Dict[Any, VerseRef],
                   base_page: int) -> LayoutRunResult:
        try:
            self.printer.run_layout(solver, paragraph_params, float_anchors)
        except FileNotFoundError as e:
            print(f"run_layout failed {e}")
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
        res = LayoutRunResult(pages, firstbad, plines, pmap, [])
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
                       delta: int,
                       result: bool = False) -> float:

        import math

        isshrink = delta < 0
        bigdelta = abs(delta) > 1
        distortion = abs(expansion - 1.0)

        p = self.printer.get_para(paragraph)
        rtl = self.printer.rtl
        pwidth = p.lastwidth if p is not None else 0.
        if rtl:
            pwidth = 1.0 - pwidth
        tex_badness = self.printer.badnesses.get(paragraph, 0)
        lines = self.basestate.layout.paragraph_total_lines.get(paragraph, 0)
        is_header = self.printer.pid_isheader(paragraph)
        is_just = self.printer.pid_isjustified(paragraph)

        res = 0.0

        # --- 1. Base cost per line change (asymmetric) ---
        # Prefer removing lines slightly over adding, especially for short paragraphs
        short_factor = (20 / min(lines + 1, 20)) ** 0.5

        if delta > 0 and is_just:
            res += self.badness_shrink_preference * delta * short_factor   # adding lines is more visible
        elif delta < 0:
            res -= delta * short_factor  # removing lines less visible

        # --- 2. Concentration penalty (multiple line changes in same paragraph) ---
        if abs(delta) >= 2:
            res += 25 * (abs(delta) - 1) * short_factor

        # --- 3. Spacing distortion (expansion/compression across paragraph) ---
        density = self.badness_line_density_factor
        res += self.badness_spacing_tolerance * (distortion * 100) ** 2

        # --- 4. Effort to cause line change (pwidth-driven, your correct model) ---
        if delta != 0:
            if delta > 0:
                effort = 1.0 - pwidth   # short line = hard to stretch
            else:
                effort = pwidth         # short line = hard to shrink

            res += self.badness_lastline_weight * (effort ** 4) * short_factor * abs(stretch)

        # --- 5. Wrong-direction penalty (soft guidance, not dominant) ---
        PIVOT = 0.7
        if delta > 0:
            wrongness = max(0.0, PIVOT - pwidth)
        elif delta < 0:
            wrongness = max(0.0, pwidth - (1.0 - PIVOT))
        else:
            wrongness = 0.0

        res += 0.5 * self.badness_spacing_tolerance * (wrongness ** 2) * short_factor * abs(stretch)

        # --- 6. Short paragraph sensitivity ---
        #line_penalty = self.badness_line_weight * ((20 / min(lines + 1, 20)) ** 0.5 - 1)
        #res += line_penalty

        # --- 7. TeX paragraph badness (log-compressed) ---
        # Only apply if modifying paragraph
        #if delta != 0 and tex_badness > 0:
        #    res += 10 * math.log10(1 + tex_badness)

        # --- 8. Header penalty ---
        if is_header:
            if pwidth >= 0.9:
                res += self.badness_header_aversion * (1.0 - pwidth)
            else:
                res += self.badness_header_aversion

        if not result:
            logger.log(
                15,
                f"{paragraph=}, {expansion=}, {stretch=}, {delta=}, "
                f"{lines=}, {pwidth=:.3f}, {tex_badness=}, {res=:.2f}"
            )

        return res

    def progress(self, pindex, itercount):
        # print(f"Starting page {pindex} after {itercount} iterations")
        pass

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
        self.bk = None

    def solve(self, state, start_page:int=-1, stop:bool=True, restart:bool=False, book=None, found=None):
        self.bk = book
        self.init_state = state
        if not self.baseline_lines:
            self.baseline_lines = dict(state.layout.paragraph_total_lines)
        if restart:
            self.base_params = dict(state.paragraph_params)
        page = start_page + 1
        layout = self.initial_probes(state, page, restart=restart, found=found)
        state.layout = layout
        wantprobe = False
        testloop = 10000
        failed_pages = []
        while True:
            layout = state.layout
            # if layout.first_failing_page < page:
            #     return None
            page = layout.first_failing_page
            if page is None:
                logger.log(15, f"solve_complete pages=%s, underfills=%s", len(layout.pages),
                        str({i: lp.column_free_lines for i, lp in enumerate(layout.pages) if lp.column_free_lines is not None}))
                state.failures = failed_pages
                return state
            self.hooks.progress(page, self.itercount)
            oldstate = state
            try:
                state = self.solve_page(state, page, start_page)
            except TimeoutError:
                return HumanFixRequest(page, "Timed out")
            if not state.passed:
                if state.layout.first_failing_page is not None and state.layout.first_failing_page < page:
                    if page < testloop:
                        logger.log(15, f"{testloop=} page {state.layout.first_failing_page}")
                        testloop = min(page, testloop)
                        wantprobe = not self.noprobe
                        self.noprobe = True
                        continue
                    else:
                        logger.log(15, f"{page=} >= {testloop=} and bail")
                        return HumanFixRequest(page, "Caught in page loop")
                if stop:
                    return HumanFixRequest(page, "Couldn't solve page")
                else:
                    while state.layout.first_failing_page is not None and state.layout.first_failing_page == page:
                        state.layout.next_bad()
                    if state.layout.first_failing_page is None:
                        return HumanFixRequest(page, "Couldn't solve all the pages")
                    failed_pages.append(page)
                    paras = self.get_candidate_paragraphs(state, page)
                    logger.warning(f"Could not solve page {page+1} after {paras[0] if len(paras) else 'UNK'} trying {state.layout.first_failing_page+1}")
                    start_page = state.layout.first_failing_page
                    continue
            solved = self.hooks.get_paragraphs_for_pages(page, page)
            #self.frozen_paragraphs.update(solved)
            self.init_state = state

    def solve_page(self, state, page, start):
        self.tried.clear()
        paragraphs = self.get_candidate_paragraphs(state, page)
        page_base_params = dict(self.base_params)
        # logger.log(15, f"shape_cache={','.join('+'.join((str(k), str(v))) for k, v in self.shape_cache.items() if k[1] != 0)}")
        # logger.log(15, f"candidates={paragraphs}")
        combos = self.generate_combos(paragraphs, state, page)
        printbk(self.bk, page)
        startcount = self.itercount
        for combo in combos:
            if not combo and self.itercount > 0:
                continue
            key = tuple(sorted(combo.items()))
            if key in self.tried:
                logger.log(12, f"tried cache hit {key=}")
                continue
            self.tried.add(key)
            if page < len(state.layout.pages) and state.layout.pages[page].column_free_lines is not None \
                    and any(x > 5 for x in state.layout.pages[page].column_free_lines) \
                    and self.itercount - startcount > 200:
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
                self.noprobe = True
                new_state = self.run_layout(page_base_params, state, combo, page, start)
                logger.log(12, f"Test run for good page, without probes {new_state.layout.first_failing_page=}")
                self.noprobe = False
                free = new_state.layout.pages[page].column_free_lines
            if new_state.layout.first_failing_page is None or new_state.layout.first_failing_page > page or free is None or not len(free) or all(x == 0 for x in free):
                logger.log(15, "page_solved page=%s iterations=%s", page, self.itercount)
                logger.log(15, f"Winning params {",".join(str(v) for v in new_state.paragraph_params.items() if v[1] != (1.0, 0))}")
                self.base_params = dict(new_state.paragraph_params)
                new_state.passed = True
                return new_state
            state = new_state
        logger.log(15, "page_failed page=%s", page)
        state = self.run_layout(page_base_params, state, {}, page, start)
        state.passed = False
        return state

    def initial_probes(self, state, page, restart=False, found=None):
        paragraphs = self.paragraph_order
        unity = (1.0, 0)
        probes = all_probes[:6]
        newstate = state
        for e, s in probes:
            if found is not None and (e, s) in found:
                continue
            params = dict(state.paragraph_params)
            for p in paragraphs:
                if (e, s) != unity or not restart or params.get(p, unity) == unity:
                    params[p] = (e, s)
            layout = self.hooks.run_layout(self, params, state.float_anchors, -1)
            self.itercount += 1
            logger.log(15, "probe_run iter=%s e=%s s=%s", self.itercount, e, s)
            self.collect_probes(layout, paragraphs, params)
        return layout

    def run_layout(self, page_base_params, state, combo, page, start):
        params = dict(page_base_params)
        #params = dict(self.base_params)
        for p, d in combo.items():
            params[p] = self.shape_cache[(p, d)]
        probe_params = dict(params)
        ps = state.layout.get_pars(page)
        last_para = ps[-1] if ps is not None and len(ps) else None
        if not self.noprobe and last_para is not None:
            found_any = False
            for p in self.paragraph_order[self._para_order(last_para) + 2:]:
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
        # logger.log(15, "BASE %s", {p:v for p,v in self.base_params.items() if v!=(1.0,0)})
        layout = self.hooks.run_layout(self, probe_params, state.float_anchors, start)
        if layout is None:
            return None
        self.itercount += 1
        logger.log(15, "layout_run [%s] iter=%s  probe=%s underfill=%s combo=%s",
                page, self.itercount, not self.noprobe,
                str({i: lp.column_free_lines for i, lp in enumerate(layout.pages) if lp.column_free_lines is not None and i <= page+2}),
                combo)
        self.collect_probes(layout, layout.paragraph_total_lines.keys(), probe_params)
        return EngineState(params, state.float_anchors, layout, self.hooks.printer.parlocs)

    def collect_probes(self, layout, paragraphs, params):
        for p in paragraphs:
            base = self.baseline_lines.get(p)
            if base is None:
                logger.log(15, f"{p} missing from base_lines")
                continue
            new = layout.paragraph_total_lines.get(p, None)
            if new is None or p not in params:
                continue
            delta = new - base
            e, s = params[p]
            #logger.log(15, f"{p} {base=}, {delta=}, ({e=}, {s=})")
            self.probe_cache[(p, e, s)] = delta
            key = (p, delta)
            bad = self.hooks.design_badness(p, e, s, delta, result=True)
            sc = self.shape_cache.get(key, None)
            if sc is None or bad < self.hooks.design_badness(p, sc[0], sc[1], delta, result=True):
                self.shape_cache[key] = (e, s)

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
            if state.paragraph_params.get(first_para, (1.0, 0)) != (1.0, 0):
                first_para_adj = 1
            elif l == 0:
                pass
            elif l < 4:
                first_para_adj = (1 - l)
        last_para = lpars[-1] if len(lpars) else None
        for (p, d), (e, s) in self.shape_cache.items():
            if p not in pset or d == 0:
                continue
            score = self.hooks.design_badness(p, e, s, d)
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
        logger.log(15, f"{first_para=} {last_para=}, {max_r=}, {colfree=}, {moves=}")
        if colfree is None:
            collengths = [0, 0]
        elif len(colfree) == 2:
            collengths = [colfree[0], colfree[0]+colfree[1]]
        elif len(colfree) == 1:
            collengths = [colfree[0], colfree[0]]
        for r in range(1, max_r + 1):
            for pars in itertools.combinations(plist, r):
                if state.paragraph_params.get(pars, (1.0, 0)) != (1.0, 0):
                    continue
                delta_lists = sorted(by_para[p] for p in pars)
                for choice in itertools.product(*delta_lists):
                    score = sum(s for s, _ in choice) + 5 * len(choice)
                    combo = {p: d for p, (s, d) in zip(pars, choice)}
                    # have we done the same net col line change before?
                    col_deltas = [0, 0, 0, 0, 0, 0]
                    # skip if another page has modified this para
                    if any(self.base_params.get(p, (1.0, 0)) != (1.0, 0) for p in combo.keys()):
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
            (e, s) = self.shape_cache.get((p, d), (None, None))
            if e is None:
                score += 1000
            else:
                score += self.hooks.design_badness(p, e, s, d)
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

    reunderfill = re.compile(r"^Underfill\[(\S+?)\]:\s+\[(\d+)\]\s+ht=([\d.]+)pt,\s+space=([\d.]+?)pt,\s+baseline=([\d.]+)pt")

    def __init__(self, build_params, nid):
        super().__init__()
        self.nid = nid
        self.timedout = False
        self.view = ViewModel(*[getattr(build_params, x) for x in ('prjtree config macrosdir args'.split())])
        self.view.setup_ini()
        self.view.setPrjid(build_params.pid, build_params.guid, loadConfig=False, startup=True)
        self.view.setConfigId(build_params.cfgid)
        self.rtl = self.view.get("fcb_textDirection", "") == "rtl"
        self.macrosdir = build_params.scriptsdir
        self.view.project.ext = None
        if nid is not None:
            self.view.project.ext = f"pbuild{nid}"
            d = self.view.project.printPath(self.view.cfgid)
            if os.path.exists(d):
                for f in os.listdir(d):
                    fp = os.path.join(d, f)
                    if os.path.isfile(fp):
                        os.unlink(fp)

    def solve(self, bk, stop=False, restart=False):
        self.bk = bk        # needed by run()
        if bk not in self.view.getAllBooks().keys():
            return None
        self.view.set("c_allowUnbalanced", True)
        self.view.set("r_book", "single")
        self.view.set("ecb_book", bk)
        # suppress peripherals
        for a in """c_inclFrontMatter c_autoToC c_useSectIntros c_frontmatter c_inclMaps
                    c_colophon c_inclBackMatter c_extradvproc c_inclSettingsInPDF c_applyWatermark
                    c_cropmarks c_extractInserts c_printArchive""".split():
            self.view.set(a, False)
        self.view.set("fcb_pagesPerSpread", 1)
        self.view.set("fcb_outputFormat", "Screen")
        self.view.savePics()
        self.view.saveStyles()
        self.hooks = Hooks(self, None)
        self.job = None
        if restart:
            #printbk(bk, -1)
            adjlist = self.view.get_adjlist(bk, save=False)
            parms = adjlist.get_params()
        else:
            parms = {}
        unlockme()
        init_layout = self.hooks.run_layout(None, parms, {}, -1)
        if init_layout is None:
            return (False, f"Failed: {bk}")
        if restart and init_layout.first_failing_page is None:
            return (True, f"Complete {bk} Already good")
        pids = list(init_layout.paragraph_pages.keys())
        logger.log(15, f"lastwidths={', '.join(f'{p}={self.get_para(p).lastwidth:.2f}' for p in pids if isinstance(p, ParInfo))}")
        state = EngineState(parms if restart else {p: (1.0, 0) for p in pids}, [], init_layout, self.parlocs)
        self.hooks.basestate = state
        print(f"Solving {bk}")
        starttime = time()
        solver = TypesetterSolver(self.hooks, pids)
        found_probes = set()
        if restart:
            for r in adjlist.liststore:
                if not r[6]:
                    continue
                for a in range(-2, 3):
                    k = f"{'p' if a > 0 else 'm'}{abs(a)}"
                    v = adjlist._parseTriggersFromComment(k, r[6])
                    if len(v) and (m := re.match(r"^(\d+)([+-]\d)?", v[0])):
                        e = int(m.group(1)) / 100
                        s = int(m.group(2)) if m.group(2) else 0
                        key = r[1] + f"[{r[2]}]" if r[2] else "[1]"
                        solver.shape_cache[(key, a)] = (e, s)
                        found_probes.add((e, s))
        res = solver.solve(state, start_page=-1, stop=stop, restart=restart, book=bk, found=found_probes)
        endtime = time()
        unlockme()
        self.job.pdffile = os.path.join(re.sub(r"\.\./?", "", os.path.dirname(self.job.pdffile)),
                os.path.basename(self.job.pdffile))
        self.job.xdvtopdf(self.job.outfname, self.job.pdffile)
        if isinstance(res, HumanFixRequest):
            retval = (False, f"{res.message} at {bk} page {res.page} after {endtime-starttime}s")
        else:
            retval = (True, f"Complete {bk}, failures={res.failures}, after {solver.itercount} runs after {endtime-starttime}s")
        return retval
        
    def run_layout(self, solver, parparms, floats, genfiles=False):
        if self.timedout:
            raise TimeoutError()
        tname = self.view.getLocalTriggerFilename(self.bk)
        fname = self.view.getAdjListFilename(self.bk)
        adjfname = os.path.join(self.view.project.srcPath(self.view.cfgid), "AdjLists", fname)
        self.adjs = AdjList(100, 95, 105, fname=adjfname)
        logger.log(12, f"{parparms=}")
        for s, p in parparms.items():
            (r, para) = self.pidkey(s)
            self.adjs.setval(s[:3], f"{r[1]}.{r[2]}{r[5]}", para, p[1], None, expand=int(p[0]*100), append=True)
            if solver is not None:
                key = f"{s[:3]}{r[1]}.{r[2]}{r[5]}"
                for a in range(-2, 3):
                    if a == 0:
                        continue
                    keyv = f"{'p' if a > 0 else 'm'}{abs(a)}"
                    if (s, a) in solver.shape_cache:
                        e, t = solver.shape_cache[(s, a)]
                        v = f"{int(e*100)}" if t == 0 else f"{int(e*100)}{t:+1d}"
                        self.adjs.addTrigger(key, v, key=keyv, append=False)
                    else:
                        self.adjs.addTrigger(key, None, key=keyv, append=False)
        self.adjs.createAdjlist()
        tname = self.view.getLocalTriggerFilename(self.bk)
        tpath = os.path.join(self.view.project.printPath(self.view.cfgid), tname)
        self.adjs.createTriggerlist(fname=tpath)

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
        return (refSort(m.group(1)), int(m.group(2) or 0))

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

    def get_paragraph_start_page(self, pid):
        p = self.parlocs[self.pidmap[pid]]
        return min([r.pagenum for r in p.rects]) - 1

    def get_paragraph_end_page(self, pid):
        p = self.parlocs[self.pidmap[pid]]
        return max([r.pagenum for r in p.rects]) - 1

    def get_lines_para_page(self, pid, page):
        p = self.parlocs[self.pidmap[pid]]
        for r in p.rects:
            if r.pagenum == page + 1:
                return r.lines
        return 0

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
            for l in inf.readlines():
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

    def read_badnesses(self):
        xdvname = self.job.outfname.replace(".tex", ".xdv")
        xdvreader = SpacingOddities(xdvname, parent=self.parlocs,
                                    fontsize=float(self.view.get("s_fontsize", 1)))
        for (opcode, data) in xdvreader.parse():
            pass
        self.parlocs.getnbadspaces()


class Worker(mp.Process):

    def __init__(self, task_queue, results_queue, build_params, log_config, nid, stop=False):
        super().__init__()
        self.task_queue = task_queue
        self.results_queue = results_queue
        self.build_params = build_params
        self.log_config = log_config
        self.nid = nid
        self.stop = stop

    def _setup_logger(self, bk):
        if self.build_params.loglevel is None:
            return
        ext = f"pbuild{self.nid}" if self.nid is not None else None
        project = self.build_params.prjtree.findProject(self.build_params.pid)
        log_dir = project.printPath(self.build_params.cfgid, ext=ext)
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"ptxprint_{bk}.log")

        logging.basicConfig(filename=log_file, filemode="w", encoding="utf-8",
                force=True, **self.log_config)
        logging.info(f"Opened log file {asctime()}")

    def run(self):
        printer = PTXprinter(self.build_params, self.nid)
        while True:
            bk = self.task_queue.get()
            if bk is None:
                break
            self._setup_logger(bk)
            printer.timedout = False
            if self.build_params.timeout is not None:
                def trigger_timeout():
                    printer.timedout = True
                watchdog = threading.Timer(self.build_params.timeout, trigger_timeout)
                watchdog.start()
            res = printer.solve(bk, stop=self.stop, restart=self.build_params.args.restart)
            if self.build_params.timeout is not None:
                watchdog.cancel()
            if res is None:     # skip absent book
                self.results_queue.put((bk, self.nid, f"{bk} does not exist"))
            else:
                self.results_queue.put((bk, self.nid, *res))
            logging.info(f"Finished {asctime()}")


    def runview(self):
        view = ViewModel(self.prjtree, self.config, self.scriptsdir, self.args)
        view.setup_ini()
        view.setPrjid(self.pid, self.guid, loadConfig=False, startup=True)
        view.setConfigId(self.cfgid)
        view.set("ecb_booklist", self.args.books)
        view.set("r_book", "multiple")
        runjob = RunJob(view, self.scriptsdir, self.macrosdir, self.args)
        runjob.nothreads = True
        runjob.silent = True
        runjob.doit(noview=True, noaction=False)


class MultiView:
    # look like a ViewModel
    def __init__(self, prjtree, userconfig, scriptsdir, args=None, odir=None):
        self.prjtree = prjtree
        self.config = {section: dict(userconfig[section]) for section in userconfig.sections()}
        self.macrosdir = scriptsdir
        self.scriptsdir = odir
        self.args = args
        self.loglevel = None
        self.timeout = args.timeout if args.timeout > 0 else None
        if self.args.logging:
            try:
                self.loglevel = int(args.logging)
            except ValueError:
                self.loglevel = getattr(logging, args.logging.upper(), None)

    def setup_ini(self):
        pass

    def set(self, key, value):
        if key == "ecb_booklist":
            allbooks = RefList(value, bookranges=True)
            allbooks.simplify(bookranges=True)
            self.books = [r.book for r in allbooks]

    def setPrjid(self, pid, guid, **kw):
        self.pid = pid
        self.guid = guid

    def setConfigId(self, cfgid, **kw):
        self.cfgid = cfgid

    # OpportunisticScheduler
    def bklen(self, bk):
        return chaps[bk]

    def initScheduler(self, numproc, log_config):
        if numproc is None:
            numproc = mp.cpu_count() - 2    # we run each cpu pretty hard
        self.numproc = numproc
        self.task_list = self.books
        self.build_params = BuildParams(*[getattr(self, a) for a in 'prjtree config'
                    ' macrosdir args pid guid cfgid scriptsdir loglevel timeout'.split(' ')])
        self.log_config = log_config

    def add_job(self, bk):
        self.task_list.append(bk)

    def run_all(self, stop=False):
        mp.set_start_method('spawn', force=True)
        self.task_list.sort(key=self.bklen, reverse=True)   # longest first
        input_q = mp.Queue()
        results_q = mp.Queue()
        for t in self.task_list:
            input_q.put(t)
        for _ in range(self.numproc):
            input_q.put(None)

        if self.numproc == 1:
            worker = Worker(input_q, results_q, self.build_params, self.log_config, None, stop=stop)
            worker.run()
        else:
            workers = [Worker(input_q, results_q, self.build_params, self.log_config, i, stop=stop) for i in range(self.numproc)]
            for w in workers:
                w.start()

        results = []
        for _ in range(len(self.task_list)):
            results.append(results_q.get())

        if self.numproc != 1:
            for w in workers:
                w.join()
        return results

def add_cli_args(parser):
    parser.add_argument("-j", "--jobs", type=int, default=1, help="Number of multiprocessing jobs to run")
    parser.add_argument("-S", "--stop", action="store_true", default=False, help="Stop book at first bad page")
    parser.add_argument("-r", "--restart", action="store_true", default=False, help="Start with the current adjustments")
    for a in parser._actions:
        if a.dest == "timeout":
            a.default = 0
            break

def get_logging_params():
    root = logging.getLogger()
    handler = root.handlers[0] if root.handlers else None
    params = {
        'level': root.getEffectiveLevel(),
        'format': None,
        'datefmt': None,
    }
    if handler:
        if handler.formatter:
            params['format'] = handler.formatter._fmt
            params['datefmt'] = handler.formatter.datefmt
    return params

def main():
    from ptxprint.main import main as ptxmain
    view = ptxmain(doitfn=None, argsline=None, retview=True, argsfn=add_cli_args, viewClass=MultiView)
    log_config = get_logging_params()
    view.initScheduler(view.args.jobs, log_config)
    results = view.run_all(view.args.stop)
    print("\n".join(str(r) for r in sorted(results, key=lambda a:(int(bookcodes.get(a[0], 100)),) + a)))

if __name__ == "__main__":
    main()

