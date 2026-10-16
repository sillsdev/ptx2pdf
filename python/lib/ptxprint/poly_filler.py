#!/usr/bin/env python3
# Page filler for polyglots (side by side glots). See docs/dev/PolyglotFiller.md

import logging
from collections import Counter
from ptxprint.page_filler import PTXFiller, TypesetterSolver, GrowList, expansion_limits
from ptxprint.parlocs import ParInfo
from ptxprint.texlog import readUnderfills

logger = logging.getLogger(__name__)


class PolySolver(TypesetterSolver):

    def run_forward(self, state, page, start_page, stop):
        """ No moves yet: report the probed starting layout. """
        self.hooks.printer.report(state)
        return state


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
        settings = self.glot_settings()
        logger.log(15, f"{bk}: glot settings {settings}")
        if len(set(settings.values())) > 1:
            # The solver only knows one set of limits so far
            logger.warning(f"{bk}: glots have different expansion limits {settings}; using the primary's")
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

    def report(self, state):
        """ Summarise per glot underfill and slice balance for the current layout """
        slices, parslice = self.get_slicemap()
        npages = self.parlocs.numPages()
        crossing = [s for s, v in slices.items() if len(v) > 1]
        imbalance = Counter()
        for s, v in slices.items():
            if len(v) > 1:
                continue
            lines = list(v.values())[0]
            counts = [lines.get(g, 0) for g in self.glots]
            imbalance[max(counts) - min(counts)] += 1
        underfull = {i: self.underfills[i] for i in range(npages) if self.underfills[i] is not None}
        for i, u in underfull.items():
            logger.log(15, f"{self.bk} page {i+1}: underfill " + ", ".join(f"{g}={n}" for g, n in zip(self.glots, u)))
        logger.log(15, f"{self.bk}: slice imbalance (lines: count) {sorted(imbalance.items())}")
        print(f"\n{self.bk}: {npages} pages, {len(slices)} slices ({len(crossing)} cross a page), "
              f"{len(underfull)} pages underfilled: "
              + " ".join(f"{i+1}[" + ",".join(f"{g}{n}" for g, n in zip(self.glots, u) if n) + "]"
                         for i, u in underfull.items()), flush=True)
