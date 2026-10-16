#!/usr/bin/env python3
# Page filler for polyglots (side by side glots). See docs/dev/PolyglotFiller.md

import logging, re, itertools
from collections import Counter
from ptxprint.page_filler import PTXFiller, TypesetterSolver, GrowList, EngineState, expansion_limits
from ptxprint.parlocs import ParInfo
from ptxprint.texlog import readUnderfills
from ptxprint.utils import refSort

logger = logging.getLogger(__name__)

def pid_glot(pid, default="L"):
    """ The glot letter in a paragraph id, e.g. JASR1.2[1] -> R """
    return refSort(re.sub(r"\[.*$", "", pid))[3] or default


class PolySolver(TypesetterSolver):

    def __init__(self, hooks, pids, **kw):
        self.glot_limits = hooks.printer.glot_settings()    # needed by limits() during init
        super().__init__(hooks, pids, **kw)

    def limits(self, pid):
        """ (expand, minexp, maxexp) of the paragraph's glot """
        return self.glot_limits.get(pid_glot(pid), (self.expand, self.minexp, self.maxexp))

    balance_maxbad = 20         # don't use a paragraph shape worse than this to balance a slice
    balance_change_cost = 0.1   # cost of changing a paragraph at all, to prefer fewer changes

    def run_forward(self, state, page, start_page, stop):
        """ Phase 1 (balance slices) only so far: no page moves. """
        printer = self.hooks.printer
        printer.report(state)
        params, changed = self.balance_slices(state)
        if changed:
            layout = self.hooks.run_layout(self, params, state.float_anchors, -1, -1)
            if layout is not None:
                state = EngineState(params, state.float_anchors, layout, printer.parlocs, 0)
                printer.report(state)
                self.check_balance()
        return state

    def check_balance(self):
        """ Log balanced slices whose measured imbalance differs from the prediction """
        printer = self.hooks.printer
        heights, baselines = printer.get_sliceheights()
        glots = printer.glots
        maxb = max(baselines[g] for g in glots)
        for sl, pred in sorted(self.balance_predicted.items()):
            pages = heights.get(sl, {})
            if len(pages) != 1:
                logger.log(15, f"balance slice {sl}: now crosses a page")
                continue
            h = list(pages.values())[0]
            hts = [h.get(g, 0) for g in glots]
            actual = round((max(hts) - min(hts)) / maxb)
            if actual != pred:
                logger.log(15, f"balance slice {sl}: predicted {pred} lines, measured {actual} ({hts})")

    def _glot_options(self, pids):
        """ Returns {total delta: (cost, ((pid, delta), ...))}, the cheapest way to change the
            lines of these paragraphs by each total. """
        res = {0: (0., ())}
        for p in pids:
            if self.hooks.is_header(p):
                continue
            base = self.shape_cache.get((p, 0))
            b0 = base[2] if base is not None and base[2] is not None else 0.
            opts = []
            for d in (-2, -1, 1, 2):
                sc = self.shape_cache.get((p, d))
                if sc is None or sc[2] is None or sc[2] > self.balance_maxbad:
                    continue
                opts.append((d, max(0., sc[2] - b0) + self.balance_change_cost))
            if not opts:
                continue
            new = dict(res)
            for tot, (c, choice) in res.items():
                for d, cost in opts:
                    k = tot + d
                    if k not in new or c + cost < new[k][0]:
                        new[k] = (c + cost, choice + ((p, d),))
            res = new
        return res

    def balance_slices(self, state):
        """ Phase 1: for each slice wholly on one page with content in every glot, choose
            paragraph deltas from the shape cache that bring its glots closest to the same
            height at the least cost. Returns (params, number of slices changed). """
        printer = self.hooks.printer
        glots = printer.glots
        heights, baselines = printer.get_sliceheights()
        slicepars = {}
        for p in printer.parlocs:
            if isinstance(p, ParInfo) and p.slice:
                slicepars.setdefault(p.slice, {}).setdefault(p.glot, []).append(p.pid())
        params = dict(state.paragraph_params)
        changed = 0
        self.balance_predicted = {}     # slice -> predicted imbalance in lines
        for sl, pages in sorted(heights.items()):
            if len(pages) != 1:
                continue
            h = list(pages.values())[0]
            if any(g not in h for g in glots):
                continue
            maxb = max(baselines[g] for g in glots)
            def imbalance(hts):
                return round((max(hts) - min(hts)) / maxb)
            current = imbalance([h[g] for g in glots])
            if current == 0:
                continue
            options = [self._glot_options(slicepars.get(sl, {}).get(g, [])) for g in glots]
            best = None
            for tots in itertools.product(*[o.keys() for o in options]):
                hts = [h[g] + t * baselines[g] for g, t in zip(glots, tots)]
                cost = sum(o[t][0] for o, t in zip(options, tots))
                score = (imbalance(hts), cost)
                if best is None or score < best[0]:
                    best = (score, tots)
            if best is None or best[0][0] >= current:
                continue
            changed += 1
            for o, t in zip(options, best[1]):
                for p, d in o[t][1]:
                    params[p] = self.shape_cache[(p, d)][:2]
            self.balance_predicted[sl] = best[0][0]
            logger.log(15, f"balance slice {sl}: {current} -> {best[0][0]} lines, cost {best[0][1]:.2f}, "
                           + ", ".join(f"{p}{d:+d}" for o, t in zip(options, best[1]) for p, d in o[t][1]))
        logger.log(15, f"Phase 1 balanced {changed} slices")
        return params, changed


class PolyFiller(PTXFiller):

    solver_class = PolySolver

    def glotviews(self):
        """ glot letter -> view, primary first """
        res = {"L": self.view}
        res.update(self.view.diglotViews)
        return res

    def glot_settings(self):
        """ glot letter -> (expand, minexp, maxexp) """
        return {g: expansion_limits(v) for g, v in self.glotviews().items()}

    def solve(self, bk, stop=False, restart=False):
        self.glots = list(self.glotviews().keys())
        logger.log(15, f"{bk}: glot settings {self.glot_settings()}")
        return super().solve(bk, stop=stop, restart=restart)

    def run_layout(self, *a, **kw):
        res = super().run_layout(*a, **kw)
        pids = Counter(p.pid() for p in self.parlocs if isinstance(p, ParInfo))
        dups = [k for k, v in pids.items() if v > 1]
        if dups:
            logger.warning(f"{self.bk}: paragraph ids not unique: {dups[:10]}")
        return res

    def parsestatus(self, fname):
        """ underfills[page] = [lines per glot, in glot order] or None if all full """
        self.underfills = GrowList()
        glots = getattr(self, 'glots', None) or ["L"]
        for (pnum, glot, avail, used, baseline) in readUnderfills(fname):
            if pnum <= 0:       # roman numbered (negative) pages are not filled
                continue
            if glot not in glots:
                logger.warning(f"Unexpected underfill column {glot} on page {pnum}")
                continue
            pnum = self.parlocs.pnums.get(pnum, pnum) - 1
            lines = int((avail - used) / baseline + 0.4)
            if lines == 0:
                continue
            v = self.underfills[pnum] or [0] * len(glots)
            v[glots.index(glot)] = lines
            self.underfills[pnum] = v

    def get_slicemap(self):
        """ Returns (slices, parslice):
                slices[slice][page][glot] = lines of that glot's paragraphs in that page slice
                parslice[pid] = slice
            Pages are 0 based. A glot missing from a page slice is empty there. """
        slices = {}
        parslice = {}
        for p in self.parlocs:
            if not isinstance(p, ParInfo) or not p.slice:
                continue
            parslice[p.pid()] = p.slice
            for r in p.rects:
                pg = slices.setdefault(p.slice, {}).setdefault(r.pagenum - 1, {})
                pg[p.glot] = pg.get(p.glot, 0) + r.lines
        return slices, parslice

    def get_sliceheights(self):
        """ Returns (heights, baselines):
                heights[slice][page][glot] = content height (pt) of that glot in that page slice
                baselines[glot] = baselineskip (pt) """
        heights = {}
        baselines = {}
        for pnum, g, ci in self.parlocs.polycols:
            if not ci.slice:
                continue
            pg = heights.setdefault(ci.slice, {}).setdefault(pnum - 1, {})
            pg[g] = pg.get(g, 0) + ci.height + ci.depth
            if ci.baseline:
                baselines[g] = ci.baseline
        return heights, baselines

    def report(self, state):
        """ Summarise per glot underfill and slice balance for the current layout """
        heights, baselines = self.get_sliceheights()
        npages = self.parlocs.numPages()
        crossing = [s for s, v in heights.items() if len(v) > 1]
        imbalance = Counter()       # slices wholly on a page with every glot: imbalance in lines -> count
        for s, v in heights.items():
            if len(v) > 1:
                continue
            h = list(v.values())[0]
            if any(g not in h for g in self.glots):
                continue
            hts = [h[g] for g in self.glots]
            imbalance[round((max(hts) - min(hts)) / max(baselines[g] for g in self.glots))] += 1
        underfull = {i: self.underfills[i] for i in range(npages) if self.underfills[i] is not None}
        for i, u in underfull.items():
            logger.log(15, f"{self.bk} page {i+1}: underfill " + ", ".join(f"{g}={n}" for g, n in zip(self.glots, u)))
        logger.log(15, f"{self.bk}: slice imbalance (lines: count) {sorted(imbalance.items())}")
        print(f"\n{self.bk}: {npages} pages, {len(heights)} slices ({len(crossing)} cross a page), "
              f"imbalance (lines:slices) {' '.join(f'{k}:{v}' for k, v in sorted(imbalance.items()))}, "
              f"{len(underfull)} pages underfilled: "
              + " ".join(f"{i+1}[" + ",".join(f"{g}{n}" for g, n in zip(self.glots, u) if n) + "]"
                         for i, u in underfull.items()), flush=True)
