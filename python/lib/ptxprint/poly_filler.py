#!/usr/bin/env python3
# Page filler for polyglots (side by side glots). See docs/dev/PolyglotFiller.md

import logging, re, itertools, math
from collections import Counter
from ptxprint.page_filler import PTXFiller, TypesetterSolver, Hooks, GrowList, EngineState, \
                                 HumanFixRequest, expansion_limits
from ptxprint.parlocs import ParInfo
from ptxprint.texlog import readUnderfills
from ptxprint.utils import refSort
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SliceOutcome:
    heights:    tuple       # per glot content height (pt), in glot order
    cost:       float       # badness of the paragraph shapes above their unadjusted shapes
    imbalance:  int         # (max - min) height in lines of the largest baseline
    badness:    float       # cost + imbalance weight * imbalance
    assignment: tuple       # ((pid, delta), ...) for paragraphs not at their unadjusted shape

    @property
    def height(self):
        return max(self.heights)

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

    balance_change_cost = 0.1   # cost of changing a paragraph at all, to prefer fewer changes

    max_page_candidates = 60    # most combos generate_combos offers for a page
    mixed_candidates = 5        # how many slice moves to also try with private fix ups
    max_slices = 3              # most slices changed together by a slice move
    pull_lines = 2              # lines of space the next slice needs to start on a page

    def run_forward(self, state, page, start_page, stop):
        """ Phase 1 (balance slices), then phase 2: fill pages using TypesetterSolver's
            page by page search with the polyglot move generator. """
        printer = self.hooks.printer
        printer.report(state)
        params, changed = self.balance_slices(state)
        if changed:
            layout = self.hooks.run_layout(self, params, state.float_anchors, -1, -1)
            if layout is not None:
                state = EngineState(params, state.float_anchors, layout, printer.parlocs, 0)
                printer.report(state)
                self.check_balance()
        self.base_params = dict(state.paragraph_params)
        self.init_state = state
        self.numpages = state.numPages()
        res = super().run_forward(state, page, start_page, stop)
        final = res.state if isinstance(res, HumanFixRequest) else res
        if int(printer.view.get("s_stopat") or 0):
            # The last layout may have stopped early; the report, adjlist and PDF need the whole book
            layout = self.hooks.run_layout(self, final.paragraph_params, final.float_anchors, -1, -1)
            if layout is not None:
                final.layout = layout
                final.parlocs = printer.parlocs
        printer.report(final)
        return res

    def repair(self, state, page, start, avoid_key, floor=0):
        """ Note which page the repair is for and what it needs, so earlier full pages
            are only offered moves that push material the right way """
        if getattr(self, 'repairing', None) is not None:
            return super().repair(state, page, start, avoid_key, floor=floor)
        failing = page + 1
        free = state.layout.pages[failing].column_free_lines if failing < len(state.layout.pages) else None
        self.repairing = (failing, free)
        try:
            return super().repair(state, page, start, avoid_key, floor=floor)
        finally:
            self.repairing = None

    def _combo(self, pids, assignment, params):
        """ The combo that sets paragraphs pids as in assignment (others unadjusted),
            leaving out those already set that way """
        chosen = dict(assignment)
        res = {}
        for p in pids:
            d = chosen.get(p, 0)
            if d == self.current_delta(p, params):
                continue
            if (p, d) not in self.shape_cache:      # only (p, 0) can be missing
                self.shape_cache[(p, d)] = self.neutral(p) + (None,)
            res[p] = d
        return res

    def generate_combos(self, paragraphs, state, page):
        """ Phase 2 candidate combos for page, best guess first. Notes make the effect of a
            change unpredictable, so the predictions only order the candidates; each is judged
            by its layout run. The slice data is taken now, since layouts run while we yield. """
        yield {}
        if page >= len(state.layout.pages):
            return
        free = state.layout.pages[page].column_free_lines
        glots = self.hooks.printer.glots
        if not free:
            free = [0] * len(glots)     # a full page: backtracking wants it to end differently
        self.prepare_slices(state.parlocs)
        params = state.paragraph_params
        b = self.baselines
        maxb = max(b[g] for g in glots)
        need = {g: free[i] for i, g in enumerate(glots)}       # lines short per glot
        short = [g for g in glots if need[g] > 0]
        full = not short
        on_page = {sl: pg for sl, pg in self.sliceheights.items() if page in pg}
        if not on_page:
            return
        last = max(on_page)     # slice ids increase down the page
        complete = [sl for sl, pg in on_page.items() if set(pg) == {page} and sl != last]
        cands = []      # (distance in lines, change in badness, effect, combo, description)

        # Private moves: a short glot gets more (or fewer) lines in the last slice on the page,
        # whether that slice crosses the bottom or not
        private = {}    # glot -> [(change in lines, change in badness, combo)]
        for sl in (last,):
            for g in (glots if full else short):
                pids = [p for p in self.slicepars.get(sl, {}).get(g, []) if page in self.parpages.get(p, ())]
                cur = {p: self.current_delta(p, params) for p in pids}
                curtot = sum(cur.values())
                curcost = sum(self.shape_cost(p, d) or 0. for p, d in cur.items())
                for tot, (cost, assign) in self._glot_options(pids).items():
                    change = tot - curtot
                    if change == 0:
                        continue
                    combo = self._combo(pids, assign, params)
                    private.setdefault(g, []).append((change, cost - curcost, combo))
                    if full or change >= need[g]:
                        dist = change - need[g] if not full else 10 if (getattr(self, 'repairing', None) and change < 0) else 0
                        cands.append((dist, cost - curcost, ("p", g, change), combo, f"{g} s{sl} {change:+d}"))

        # Slice moves: slices wholly on the page change height, moving everything below them.
        # Per slice, the cheapest outcome for each height change.
        crossing = page + 1 in on_page[last]
        movable = complete + ([] if crossing or set(on_page[last]) != {page} else [last])
        options = {}        # slice -> {height change (pt, rounded): (change in badness, combo, imbalance)}
        for sl in movable:
            cur = self.current_outcome(sl, params)
            pids = [p for g in glots for p in self.slicepars.get(sl, {}).get(g, [])]
            opts = options.setdefault(sl, {})
            for o in self.slice_outcomes(sl, params):
                dh = round(o.height - cur.height)
                if dh == 0:
                    continue
                dbad = o.badness - cur.badness
                combo = self._combo(pids, o.assignment, params)
                if dh not in opts or dbad < opts[dh][0]:
                    opts[dh] = (dbad, combo, o.imbalance)

        # Combine up to max_slices slices, all growing or all shrinking (a page is a single column
        # of slices, so doing both is unlikely to help): total height change -> (change in badness,
        # combo, description)
        totals = {0: (0., {}, ())}
        for sign in (1, -1):
            part = {0: (0., {}, ())}
            for sl in movable:
                if sl == last and sign > 0:
                    continue    # growing the last slice only pushes its tallest glot off the page
                new = dict(part)
                for tot, (dbad, combo, desc) in part.items():
                    if len(desc) >= self.max_slices:
                        continue
                    for dh, (sbad, scombo, imb) in options.get(sl, {}).items():
                        if dh * sign <= 0:
                            continue
                        k = tot + dh
                        if k not in new or dbad + sbad < new[k][0]:
                            new[k] = (dbad + sbad, {**combo, **scombo}, desc + (f"s{sl} {dh:+d}pt",))
                part = new
            totals.update({k: v for k, v in part.items() if k != 0})

        repairing = getattr(self, 'repairing', None)
        helped = None       # lines the page being repaired for is short, if this page is before it
        if full and repairing is not None and page < repairing[0] and repairing[1] and any(repairing[1]):
            helped = max(repairing[1]) * maxb
        if full:
            # Any change in where the page ends, cheapest first. When repairing for a later
            # short page, growth usually helps (it pushes more material onto that page), so
            # try that first; but notes and slice boundaries make it no rule.
            for tot, (dbad, combo, desc) in totals.items():
                if tot == 0:
                    continue
                dist = 0 if helped is None else abs(tot - helped) / maxb + (10 if tot < 0 else 0)
                cands.append((dist, dbad, ("f", tot), combo, " + ".join(desc)))
            totals = {}
        # Growth: push the short glots' ends down; a full glot just spills more
        target = min((need[g] * b[g] for g in short), default=0)
        growth = []
        for tot, (dbad, combo, desc) in totals.items():
            if tot <= 0:
                continue
            dist = abs(tot - target) / maxb
            growth.append((dist, dbad, tot, combo, desc))
            if tot >= target - 0.5 * maxb:
                cands.append((dist, dbad, ("g", tot), combo, " + ".join(desc)))

        # Pull in: if the page ends at a slice boundary, shrink enough for the next slice to start
        if not crossing and not full:
            gap = min(need[g] * b[g] for g in glots)
            pull = max(maxb, self.pull_lines * maxb - gap)
            for tot, (dbad, combo, desc) in totals.items():
                if tot >= 0:
                    continue
                dist = max(0., pull + tot) / maxb + 0.5 * max(0., -tot - pull) / maxb
                cands.append((dist, dbad, ("u", tot), combo, "pull " + " + ".join(desc)))

        # Mixed: growth plus private fix ups for what it leaves short
        growth.sort(key=lambda m: (round(m[0]), m[1]))
        for dist, dbad, dh, combo, desc in growth[:self.mixed_candidates]:
            mixed = dict(combo)
            err = 0.
            desc = list(desc)
            for g in short:
                rest = round((need[g] * b[g] - dh) / b[g])
                if rest <= 0 or g not in private:
                    err += abs(min(rest, 0))
                    continue
                best = min(private[g], key=lambda x: (abs(x[0] - rest), x[1]))
                mixed.update(best[2])
                dbad += best[1]
                err += abs(best[0] - rest)
                desc.append(f"{g} {best[0]:+d}")
            if len(desc) > 1 and err == 0:
                cands.append((err, dbad, ("m",) + tuple(desc), mixed, " + ".join(desc)))

        # Try the cheapest way to get each predicted effect first, then the dearer alternatives
        # As monoglot: only the cheapest way to each predicted effect
        cands.sort(key=lambda c: (round(c[0]), c[1]))
        firsts, effects = [], set()
        for c in cands:
            if c[2] not in effects:
                firsts.append(c)
                effects.add(c[2])
        seen = set()
        n = 0
        maxr = int(self.hooks.badness_maxr)
        for dist, dbad, effect, combo, desc in firsts:
            key = tuple(sorted(combo.items()))
            if not combo or key in seen or len(combo) > maxr:
                continue
            seen.add(key)
            logger.log(15, f"p{page+1} candidate {desc}: dist {dist:.1f} dbad {dbad:.2f}")
            yield combo
            n += 1
            if n >= self.max_page_candidates:
                break

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
            lines of these paragraphs by each total, from their unadjusted shapes. """
        res = {0: (0., ())}
        for p in pids:
            if self.hooks.is_header(p):
                continue
            opts = [(d, c) for d in (-2, -1, 1, 2) if (c := self.shape_cost(p, d)) is not None]
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

    def current_delta(self, pid, params):
        """ The line delta of a paragraph's current parameters, relative to its unadjusted shape """
        v = params.get(pid, self.neutral(pid))
        if v == self.neutral(pid):
            return 0
        return self.probe_cache.get(pid, {}).get(v) or 0

    maxbad_scale = 20           # shape badness: most usable shapes are under 2, loose ones over 20
    imbalance_scale = 10        # badness of a line of imbalance, well above what good shapes cost

    def maxbad(self):
        """ Paragraph shapes worse than this are not used to change a slice """
        return self.hooks.badness_balance_maxbad * self.maxbad_scale

    def imbalance_weight(self):
        """ Badness of one line of imbalance in a slice """
        return self.hooks.badness_imbalance_weight * self.imbalance_scale

    def shape_cost(self, pid, d):
        """ Badness of paragraph pid at line delta d above its unadjusted shape, or None if unusable """
        if d == 0:
            return 0.
        sc = self.shape_cache.get((pid, d))
        if sc is None or sc[2] is None or sc[2] > self.maxbad():
            return None
        base = self.shape_cache.get((pid, 0))
        b0 = base[2] if base is not None and base[2] is not None else 0.
        return max(0., sc[2] - b0) + self.balance_change_cost

    def current_outcome(self, sl, params):
        """ The SliceOutcome of slice sl as currently laid out """
        glots = self.hooks.printer.glots
        pages = self.sliceheights.get(sl, {})
        pids = self.slicepars.get(sl, {})
        hts = tuple(sum(pg.get(g, 0) for pg in pages.values()) for g in glots)
        assign = tuple((p, d) for g in glots for p in pids.get(g, []) if (d := self.current_delta(p, params)))
        cost = sum(self.shape_cost(p, d) or 0. for p, d in assign)
        imb = round((max(hts) - min(hts)) / max(self.baselines[g] for g in glots))
        return SliceOutcome(hts, cost, imb, cost + self.imbalance_weight() * imb, assign)

    def slice_outcomes(self, sl, params):
        """ All the ways the paragraphs of slice sl can be set, as SliceOutcomes sorted by
            badness. Heights are for the whole slice (all its pages). params gives the shapes
            the current layout was made with. """
        printer = self.hooks.printer
        glots = printer.glots
        pages = self.sliceheights.get(sl, {})
        if not pages:
            return []
        pids = self.slicepars.get(sl, {})
        neutral = {}
        for g in glots:
            h = sum(pg.get(g, 0) for pg in pages.values())
            cur = sum(self.current_delta(p, params) for p in pids.get(g, []))
            neutral[g] = h - cur * self.baselines.get(g, 0)
        maxb = max(self.baselines[g] for g in glots)
        weight = self.imbalance_weight()
        options = [self._glot_options(pids.get(g, [])) for g in glots]
        res = []
        for tots in itertools.product(*[o.keys() for o in options]):
            hts = tuple(neutral[g] + t * self.baselines[g] for g, t in zip(glots, tots))
            cost = sum(o[t][0] for o, t in zip(options, tots))
            imb = round((max(hts) - min(hts)) / maxb)
            assign = tuple(pd for o, t in zip(options, tots) for pd in o[t][1])
            res.append(SliceOutcome(hts, cost, imb, cost + weight * imb, assign))
        res.sort(key=lambda x: (x.badness, len(x.assignment)))
        return res

    def slice_range(self, sl, params):
        """ (minimum height, lowest badness outcome, maximum height) of a slice, in points """
        outcomes = self.slice_outcomes(sl, params)
        if not outcomes:
            return None
        hts = [o.height for o in outcomes]
        return (min(hts), outcomes[0], max(hts))

    def fit_slice(self, sl, params, lo, hi):
        """ The lowest badness outcome of slice sl whose height is in [lo, hi] points, or None """
        for o in self.slice_outcomes(sl, params):
            if lo <= o.height <= hi:
                return o
        return None

    def apply_outcome(self, outcome, params, pids):
        """ Set the paragraphs pids to the shapes in outcome (unlisted ones to unadjusted) """
        chosen = dict(outcome.assignment)
        for p in pids:
            d = chosen.get(p, 0)
            params[p] = self.neutral(p) if d == 0 else self.shape_cache[(p, d)][:2]

    def prepare_slices(self, parlocs=None):
        """ Gather the per slice data from a layout (default the latest) """
        printer = self.hooks.printer
        if parlocs is None:
            parlocs = printer.parlocs
        self.sliceheights, self.baselines = printer.get_sliceheights(parlocs)
        self.slicepars = {}
        self.parpages = {}      # pid -> set of pages (0 based) it is on
        for p in parlocs:
            if isinstance(p, ParInfo) and p.slice:
                self.slicepars.setdefault(p.slice, {}).setdefault(p.glot, []).append(p.pid())
                self.parpages[p.pid()] = set(r.pagenum - 1 for r in p.rects)

    def balance_slices(self, state):
        """ Phase 1: give each slice wholly on one page, with content in every glot, its lowest
            badness outcome if that is better than how it is now.
            Returns (params, number of slices changed). """
        glots = self.hooks.printer.glots
        self.prepare_slices()
        params = dict(state.paragraph_params)
        changed = 0
        self.balance_predicted = {}     # slice -> predicted imbalance in lines
        for sl, pages in sorted(self.sliceheights.items()):
            if len(pages) != 1 or any(g not in list(pages.values())[0] for g in glots):
                continue
            now = self.current_outcome(sl, params)
            best = self.slice_outcomes(sl, params)[0]
            if best.badness >= now.badness:
                continue
            changed += 1
            self.apply_outcome(best, params, [p for g in glots for p in self.slicepars.get(sl, {}).get(g, [])])
            self.balance_predicted[sl] = best.imbalance
            logger.log(15, f"balance slice {sl}: {now.imbalance} -> {best.imbalance} lines, "
                           f"badness {now.badness:.2f} -> {best.badness:.2f}, "
                           + ", ".join(f"{p}{d:+d}" for p, d in best.assignment))
        logger.log(15, f"Phase 1 balanced {changed} slices")
        return params, changed


class PolyHooks(Hooks):

    def get_page_para_key(self, page, col=None, state=None):
        """ Per glot, the first paragraph on the page and its lines there """
        printer = self.printer
        plocs = printer.parlocs if state is None else state.parlocs
        first = {}
        for p, r in (plocs.getParas(page + 1) or []):
            if isinstance(p, ParInfo) and p.glot not in first:
                first[p.glot] = p.pid()
        return tuple((first.get(g), printer.get_lines_para_page(first[g], page, state=state) if g in first else 0)
                     for g in printer.glots)


class PolyFiller(PTXFiller):

    solver_class = PolySolver
    hooks_class = PolyHooks

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
            # Used includes the last line's depth, so only whole lines of gap can be filled
            lines = math.floor((avail - used) / baseline + 0.05)
            if lines <= 0:
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

    def get_sliceheights(self, parlocs=None):
        """ Returns (heights, baselines) for a layout (default the latest):
                heights[slice][page][glot] = content height (pt) of that glot in that page slice
                baselines[glot] = baselineskip (pt) """
        heights = {}
        baselines = {}
        for pnum, g, ci in (parlocs or self.parlocs).polycols:
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
