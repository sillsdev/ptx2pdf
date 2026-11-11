#!/usr/bin/env python3
# Page filler for polyglots (side by side glots). See docs/dev/PolyglotFiller.md

import logging, re, itertools, math
from collections import Counter
from ptxprint.page_filler import PTXFiller, TypesetterSolver, Hooks, GrowList, EngineState, \
                                 HumanFixRequest, expansion_limits
from ptxprint.parlocs import ParInfo
from ptxprint.texlog import readUnderfills
from ptxprint.utils import refSort, ProgressEvent
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SliceOutcome:
    heights:    tuple       # per glot height (pt) in glot order: its text plus what TeX adds to align the slice
    cost:       float       # badness of the paragraph shapes above their unadjusted shapes
    imbalance:  float       # whitespace where its glots end, in column-lines (see empty_lines)
    badness:    float       # cost + imbalance_cost(imbalance)
    assignment: tuple       # ((pid, delta), ...) for paragraphs not at their unadjusted shape

    @property
    def height(self):
        return max(self.heights)

def end_gaps(pages, baselines, glots):
    """ Per glot, lines of gap where a slice ends: on its last page, the longest glot's part
        less this glot's (a glot with nothing there has the whole of it as a gap).
        pages[page][glot] = content height (pt) """
    last = pages[max(pages)]
    top = max(last.get(g, 0) for g in glots)
    return [(top - last.get(g, 0)) / baselines[g] for g in glots]

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

    # The first failing page matters most (the user fixes it, and maybe all that follows, by
    # hand), so pages before any failure get more effort than pages after one.
    page_budget = 24            # most layout runs spent filling one page (after a failure)
    backtrack_budget = 12       # most layout runs spent on each earlier page when backtracking
    refill_budget = 8           # most runs filling a page again from a start a backtrack gave it
    early_max_budget = 80       # before any page has failed: most runs for a page,
    early_backtrack_budget = 16 # per earlier page when backtracking,
    early_refill_budget = 10    # and to refill from a new start
    relax_caps = (2, 4)         # if a page runs out of candidates, try again allowing looser shapes
    per_net = 3                 # combos kept for each net height change of a page's slices
    per_dh = 3                  # outcomes kept for each height change of one slice (differing in which glots change)
    budget_per_par = 2          # extra layout runs a page gets for each paragraph on it that can change
    max_budget = 60
    max_candidates = 2000       # most candidates listed for a page
    pull_lines = 2              # lines of space the next slice needs to start on a page
    crossing_budget = 1         # most layout runs spent evening the ends of a slice crossing a page
    early_crossing_budget = 2   # the same before any page has failed
    min_carry = 2               # fewest lines of a paragraph carried over a page

    def solve(self, state, start_page=-1, stop=True, restart=False, book=None):
        self.restarting = restart
        if restart:
            self._match_adjlist_ids(state)
        return super().solve(state, start_page=start_page, stop=stop, restart=restart, book=book)

    def _match_adjlist_ids(self, state):
        """ The adjlist writes a paragraph without a parnum as [1], but its id here is [] """
        known = set(self.paragraph_order)
        def fix(pid):
            if pid not in known and pid.endswith("[1]") and pid[:-3] + "[]" in known:
                return pid[:-3] + "[]"
            return pid
        state.paragraph_params = {fix(k): v for k, v in state.paragraph_params.items()}
        self.shape_cache = {(fix(k), d): v for (k, d), v in self.shape_cache.items()}
        self.probe_cache = {fix(k): v for k, v in self.probe_cache.items()}

    @property
    def early(self):
        """ Before the first failed page """
        return not self.failed_pages

    def run_forward(self, state, page, start_page, stop):
        """ Fill pages in order (design section 4). Each page is tried with candidate combos,
            ordered by a note free model and re-ordered by what each layout run measures, and
            is committed full or, failing that, with the best layout measured for it. """
        printer = self.hooks.printer
        printer.report(state)
        self.failed_pages = []
        self.page_memo = {}     # (page, start key) -> {combo signature: gap measured}
        cur = state
        p = 0
        self.floor = 0          # pages before this are not changed (on a restart, the user's)
        if getattr(self, 'restarting', False) and cur.layout.first_failing_page is not None:
            p = self.floor = cur.layout.first_failing_page
            logger.log(15, f"{self.bk}: restarting at page {p+1}")
        while True:
            if p >= len(cur.layout.pages) - 1 and not cur.layout.complete:
                more = self._layout(cur.paragraph_params, cur, p + 2)   # measure this page and the next
                if more is None:
                    break
                cur = more
            if p >= len(cur.layout.pages) - 1:
                break           # the last page may be short
            self.printbk(self.bk, p, total=len(cur.layout.pages))
            if self._page_short(cur, p):
                before = cur
                cur = self.fill_page(cur, p)
                if p in self.failed_pages and p > self.floor and p - 1 not in self.failed_pages:
                    self.failed_pages.remove(p)     # still early while backtracking for it
                    back = self.backtrack(before, p)
                    self.failed_pages.append(p)
                    if back is not None:
                        self.failed_pages.remove(p)
                        cur = back
                        if self._page_short(cur, p):
                            cur = self.fill_page(cur, p)
                if stop and p in self.failed_pages:
                    final = self._layout(cur.paragraph_params, cur, -1) or cur
                    final.failures = self.failed_pages
                    printer.report(final)
                    return HumanFixRequest(final, p + 1, f"Cannot fill page {p+1}")
            cur = self.balance_and_check(cur, p)
            evened = self.balance_crossing(cur, p)
            if evened is not None:
                cur = evened
            self.hooks.progress(ProgressEvent(self.bk, p + 1, "badpage" if p in self.failed_pages else "goodpage",
                                              "", len(cur.layout.pages)))
            p += 1
            if self.hooks.cancelled:
                return HumanFixRequest(cur, p, "Stopped")
        # Filling a page may reset slices balanced on the pages before it (a backtrack): balance
        # every page again (the last too, which needs no filling), now that where pages break
        # is settled
        before = self.itercount
        q = self.floor
        while q < len(cur.layout.pages):
            if q >= len(cur.layout.pages) - 1 and not cur.layout.complete:
                more = self._layout(cur.paragraph_params, cur, q + 2)     # a layout that reaches q
                if more is None:
                    break
                cur = more
            cur = self.balance_and_check(cur, q)
            # a page filled after the slice crossing onto it was evened may have moved its end
            evened = self.balance_crossing(cur, q, single_only=True)
            if evened is not None:
                cur = evened
            q += 1
        logger.log(15, f"{self.bk}: final balance took {self.itercount - before} runs")
        cur.failures = self.failed_pages
        # The report, adjlist and PDF need a layout of the whole book
        final = self._layout(cur.paragraph_params, cur, -1)
        if final is not None:
            final.failures = self.failed_pages
            final.wholebook = True      # so the filler needn't lay it out again
            cur = final
        printer.report(cur)
        return cur

    def _layout(self, params, state, last_page):
        """ Run a layout with params as far as last_page (-1 for the whole book) """
        layout = self.hooks.run_layout(self, params, state.float_anchors, -1, last_page)
        if layout is None:
            return None
        self.itercount += 1
        return EngineState(params, state.float_anchors, layout, self.hooks.printer.parlocs, 0)

    def _key(self, state, page):
        """ Where page starts, per glot: (first paragraph, its lines on the page) """
        return self.hooks.get_page_para_key(page, state=state)

    def _tried(self, state, page):
        """ {combo signature: gap measured} for page starting as it does in state """
        return self.page_memo.setdefault((page, self._key(state, page)), {})

    def _gap(self, state, page):
        """ Lines short per glot on page (all 0 if full) """
        glots = self.hooks.printer.glots
        if page >= len(state.layout.pages):
            return None
        free = state.layout.pages[page].column_free_lines
        return list(free) if free else [0] * len(glots)

    def _page_short(self, state, page):
        gap = self._gap(state, page)
        return gap is not None and any(x > 0 for x in gap)

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

    def page_candidates(self, state, page, gap=None):
        """ All combos for page with their predicted effect.
            Returns [(effects per glot (pt), net slice change (pt), change in badness, combo, desc)] """
        glots = self.hooks.printer.glots
        self.prepare_slices(state.parlocs)
        params = state.paragraph_params
        on_page = {sl: pg for sl, pg in self.sliceheights.items() if page in pg}
        if not on_page:
            return []
        last = max(on_page)
        crossing = page + 1 in on_page[last]
        # slices wholly on the page (the last too if it does not cross): every height change
        whole = [sl for sl, pg in on_page.items() if set(pg) == {page} and (sl != last or not crossing)]
        # a slice continuing from the previous page: its paragraphs wholly on this page can change
        # without moving the break, changing this page's part of the slice
        top = [sl for sl, pg in on_page.items() if min(pg) < page and sl != last]
        totals = {0: [(0., {}, ())]}        # net change -> up to per_net (dbad, combo, desc), cheapest first
        for sl in top + whole:
            if sl in top:
                opts = self._partial_options(sl, page, params)
            else:
                cur = self.current_outcome(sl, params)
                pids = [p for g in glots for p in self.slicepars.get(sl, {}).get(g, [])]
                best = {}       # (height change, per glot change) -> cheapest
                for o in self.slice_outcomes(sl, params):
                    dh = round(o.height - cur.height)
                    if dh == 0:
                        continue
                    sig = (dh, tuple(round(a - b) for a, b in zip(o.heights, cur.heights)))
                    if sig not in best or o.badness - cur.badness < best[sig][0]:
                        best[sig] = (o.badness - cur.badness, o)
                opts = {}
                for (dh, sig), (dbad, o) in sorted(best.items(), key=lambda x: x[1][0]):
                    lst = opts.setdefault(dh, [])
                    if len(lst) < self.per_dh:
                        lst.append((dbad, self._combo(pids, o.assignment, params)))
            new = {k: list(v) for k, v in totals.items()}
            for tot, entries in totals.items():
                for dh, slst in opts.items():
                    for sbad, scombo in slst:
                        lst = new.setdefault(tot + dh, [])
                        for dbad, combo, desc in entries:
                            lst.append((dbad + sbad, {**combo, **scombo}, desc + (f"s{sl}{dh:+d}",)))
            for k in new:
                new[k] = sorted(new[k], key=lambda x: (x[0], len(x[1])))[:self.per_net]
            totals = new
        # the last slice, per short glot: its lines on this page (a full glot's change only
        # alters what spills to the next page). Filling each short glot to the foot of the page
        # leaves the slice level there.
        private = {g: [(0, 0., {})] for g in glots}
        for i, g in enumerate(glots):
            if gap is not None and gap[i] <= 0:
                continue
            pids = [p for p in self.slicepars.get(last, {}).get(g, []) if page in self.parpages.get(p, ())]
            cur = {p: self.current_delta(p, params) for p in pids}
            curtot = sum(cur.values())
            curcost = sum(self.shape_cost(p, d) or 0. for p, d in cur.items())
            for tot, (cost, assign) in self._glot_options(pids).items():
                if tot != curtot:
                    private[g].append((tot - curtot, cost - curcost, self._combo(pids, assign, params)))
        b = self.baselines
        res = []
        for net, entries in totals.items():
            for dbad, combo, desc in entries:
                for choice in itertools.product(*[private[g] for g in glots]):
                    effects = [net + ch[0] * b[g] for g, ch in zip(glots, choice)]
                    # a last slice that ends here, changed glot by glot, must end level: at the
                    # foot of the page, each glot's gap filled exactly
                    if not crossing and gap is not None and any(ch[0] for ch in choice) \
                            and any(abs(e - n * b[g]) >= 0.5 * b[g] for e, n, g in zip(effects, gap, glots)):
                        continue
                    c = dict(combo)
                    pbad = dbad
                    pdesc = list(desc)
                    for g, ch in zip(glots, choice):
                        c.update(ch[2])
                        pbad += ch[1]
                        if ch[0]:
                            pdesc.append(f"{g}{ch[0]:+d}")
                    if not c:
                        continue
                    res.append((effects, net, pbad, c, " ".join(pdesc), " ".join(desc)))
                    if len(res) >= self.max_candidates:
                        return res
        return res

    def _partial_options(self, sl, page, params):
        """ For slice sl continuing onto page from the one before: {change in its height on this
            page (pt): (change in badness, combo)}, using only its paragraphs wholly on this page """
        glots = self.hooks.printer.glots
        per = []
        fixed = []      # per glot, whether its paragraphs not wholly on this page are changed
        for g in glots:
            allpids = self.slicepars.get(sl, {}).get(g, [])
            pids = [p for p in allpids if self.parpages.get(p) == {page}]
            fixed.append(any(p not in pids and self.current_delta(p, params) for p in allpids))
            cur = {p: self.current_delta(p, params) for p in pids}
            curtot = sum(cur.values())
            curcost = sum(self.shape_cost(p, d) or 0. for p, d in cur.items())
            curtext = self.text_delta(cur.items())
            per.append([(tot - curtot, cost - curcost, self._combo(pids, assign, params), bool(assign),
                         self.text_delta(assign) - curtext)
                        for tot, (cost, assign) in self._glot_options(pids).items()])
        # this page's part of the slice: its text
        text0 = self.content(sl, {page})
        # where the slice ends on this page, its glots' parts should end level
        ends = max(self.sliceheights.get(sl, {page: None})) == page
        def imbalance(text):
            return self.empty_lines(text) if ends else 0
        imb0 = imbalance(text0)
        best = {}
        for choice in itertools.product(*per):
            text = [t + ch[4] for t, ch in zip(text0, choice)]
            dh = round(max(text) - max(text0))
            if dh == 0:
                continue
            if ends and not self.allowed(text, [f or ch[3] for f, ch in zip(fixed, choice)], sl):
                continue
            dbad = sum(ch[1] for ch in choice) + self.imbalance_cost(imbalance(text), sl) - self.imbalance_cost(imb0, sl)
            sig = (dh, tuple(ch[0] for ch in choice))
            if sig not in best or dbad < best[sig][0]:
                combo = {}
                for ch in choice:
                    combo.update(ch[2])
                best[sig] = (dbad, combo)
        opts = {}
        for (dh, sig), v in sorted(best.items(), key=lambda x: x[1][0]):
            lst = opts.setdefault(dh, [])
            if len(lst) < self.per_dh:
                lst.append(v)
        return opts

    def _priority(self, cand, gap, crossing, response):
        """ How promising a candidate looks: distance from the nearer of growing to fill the
            gap or shrinking enough to pull in more, then badness. response scales predicted
            effects per glot by what layout runs on this page have measured. """
        glots = self.hooks.printer.glots
        b = self.baselines
        maxb = max(b[g] for g in glots)
        effects, net, dbad, combo, desc, slicedesc = cand
        eff = [e * response[i] for i, e in enumerate(effects)]
        grow = sum(abs(e - gap[i] * b[g]) / b[g] if gap[i] > 0 else max(0., -e) / b[g]
                   for i, (g, e) in enumerate(zip(glots, eff)))
        pull = self.pull_lines * maxb + max(gap[i] * b[g] for i, g in enumerate(glots))
        shrink = max(0., net + pull) / maxb + 0.5 * max(0., -net - pull) / maxb if net < 0 else 1000.
        # each try of the same slice changes moves its other variants down a step
        return (round(min(grow, shrink) * 2) / 2 + self._slicetries.get(slicedesc, 0), dbad)

    def fill_page(self, state, page):
        """ Try combos on page until it is full or its budget is spent; commit the result """
        self.prepare_slices(state.parlocs)
        # foreach slice on the page count the paragraphs in it that can change shape
        movable = sum(1 for sl, pg in self.sliceheights.items() if page in pg
                      for g in self.hooks.printer.glots for p in self.slicepars.get(sl, {}).get(g, [])
                      if page in self.parpages.get(p, ()) and self.shape_deltas.get(p))
        budget = min(self.early_max_budget if self.early else self.max_budget,
                     self.page_budget + self.budget_per_par * movable)
        gap, dbad, new, desc = self.try_fill(state, page, budget)
        if gap > 0:
            self.failed_pages.append(page)
        return new

    def try_fill(self, state, page, budget):
        """ Try combos on page, at most budget layout runs, until it is full.
            Returns (lines short, change in badness, best state, description) """
        glots = self.hooks.printer.glots
        gap0 = self._gap(state, page)
        memo = self._tried(state, page)
        self.cap_scale = 1      # used in page_candidates
        cands = [c for c in self.page_candidates(state, page, gap0) if frozenset(c[3].items()) not in memo]
        self._slicetries = {}
        on_page = [sl for sl, pg in self.sliceheights.items() if page in pg]
        crossing = bool(on_page) and page + 1 in self.sliceheights[max(on_page)]
        response = [1.] * len(glots)
        observed = [[] for g in glots]
        best = (sum(gap0), 0., state, "none")
        tried = 0
        logger.log(15, f"p{page+1}: gap {gap0}, {len(cands)} candidates ({len(memo)} tried before from this start)")
        relax = list(self.relax_caps)
        while tried < budget:
            if not cands:
                # Out of candidates: a looser paragraph is better than a failed page
                if not relax or best[0] == 0:
                    break
                scale = self.cap_scale = relax.pop(0)
                cands = [c for c in self.page_candidates(state, page, gap0) if frozenset(c[3].items()) not in memo]
                self.cap_scale = 1
                logger.log(15, f"p{page+1}: {len(cands)} more candidates with the shape cap x{scale}")
                continue
            cands.sort(key=lambda c: self._priority(c, gap0, crossing, response))
            effects, net, dbad, combo, desc, slicedesc = cands.pop(0)
            self._slicetries[slicedesc] = self._slicetries.get(slicedesc, 0) + 1
            params = dict(state.paragraph_params)
            for p, d in combo.items():
                params[p] = self.shape_cache[(p, d)][:2]
            new = self._layout(params, state, page + 2)
            tried += 1
            if new is None:
                continue
            gap = self._gap(new, page)
            memo[frozenset(combo.items())] = gap
            ffp = new.layout.first_failing_page
            broke = ffp is not None and ffp < page and ffp not in self.failed_pages and not self._page_short(state, ffp)
            logger.log(15, f"p{page+1} try {desc}: predicted {[round(e, 1) for e in effects]} -> gap {gap}{' breaks p%d' % (ffp+1) if broke else ''}")
            if gap is None or broke:
                continue
            for i, g in enumerate(glots):           # measured response to predicted effects
                if abs(effects[i]) >= 1:
                    observed[i].append((gap0[i] - gap[i]) * self.baselines[g] / effects[i])
                    response[i] = max(0., min(2., sum(observed[i]) / len(observed[i])))
            score = (sum(gap), dbad)
            if score < best[:2]:
                best = (sum(gap), dbad, new, desc)
            if sum(gap) == 0:
                break
        logger.log(15, f"p{page+1}: {'filled' if best[0] == 0 else 'failed, best gap %d' % best[0]} by {best[3]} after {tried} runs")
        return best

    def backtrack(self, state, page):
        """ page can't be filled from its own slices: change where an earlier page ends instead,
            keeping the pages between full. Looks up to the backtrack setting back for a change
            that fills page; failing that, takes the best improvement found one page back.
            Each run measures all the pages involved. Returns a better state or None. """
        glots = self.hooks.printer.glots
        gap0 = self._gap(state, page)
        need = max(gap0[i] * self.baselines[g] for i, g in enumerate(glots))
        seen = {self._key(state, page)}     # starts of page already measured
        improved = None
        tried = 0
        depth = int(self.backtrack_depth) if self.early else 1
        for target in range(page - 1, max(self.floor - 1, page - 1 - depth), -1):
            if target in self.failed_pages:
                break
            memo = self._tried(state, target)
            cands = [c for c in self.page_candidates(state, target, [0] * len(glots))
                     if c[1] != 0 and frozenset(c[3].items()) not in memo]
            samestart = set()           # net changes that gave page a start already seen
            def order(c):
                # growth pushes material on towards the short page: try it first, nearest the need
                return (c[1] in samestart, c[1] < 0, abs(abs(c[1]) - need), c[2])
            n = 0
            while cands and n < (self.early_backtrack_budget if self.early else self.backtrack_budget):
                cands.sort(key=order)
                effects, net, dbad, combo, desc, slicedesc = cands.pop(0)
                params = dict(state.paragraph_params)
                for p, d in combo.items():
                    params[p] = self.shape_cache[(p, d)][:2]
                new = self._layout(params, state, page + 2)
                n += 1
                tried += 1
                if new is None:
                    continue
                memo[frozenset(combo.items())] = self._gap(new, target)
                if any(self._page_short(new, q) for q in range(target, page)):
                    continue
                key = self._key(new, page)
                if key in seen:
                    samestart.add(net)
                    continue
                seen.add(key)
                gap = self._gap(new, page)
                logger.log(15, f"p{page+1} back on p{target+1} {desc}: gap {gap}")
                if gap is None:
                    continue
                if sum(gap) > 0:
                    # a new start for page: try filling it from there
                    before = self.itercount
                    rgap, rdbad, rnew, rdesc = self.try_fill(new, page,
                                    self.early_refill_budget if self.early else self.refill_budget)
                    tried += self.itercount - before
                    if rgap < sum(gap):
                        gap, new = [0] * len(glots) if rgap == 0 else self._gap(rnew, page), rnew
                if sum(gap) == 0:
                    logger.log(15, f"p{page+1}: backtrack to p{target+1} filled it after {tried} runs")
                    return new
                if target == page - 1 and sum(gap) < sum(gap0) and (improved is None or sum(gap) < improved[0]):
                    improved = (sum(gap), new)
        logger.log(15, f"p{page+1}: backtrack {'improved to gap %d' % improved[0] if improved else 'found nothing'} after {tried} runs")
        return improved[1] if improved else None

    def balance_page(self, state, page, params):
        """ Give each slice wholly on page a same height outcome with less badness (better
            balance at no cost to the page). Changes params; returns the changes made as
            [(slice, outcome, {pid: its params before})]. """
        glots = self.hooks.printer.glots
        self.prepare_slices(state.parlocs)
        changes = []
        for sl, pg in self.sliceheights.items():
            if set(pg) != {page}:
                continue
            cur = self.current_outcome(sl, params)
            o = self._same_height(sl, params, cur)
            if o is None and self.single_gap(sl, cur.imbalance):
                # a 1 line gap is worse than a looser paragraph: allow looser shapes, as filling does
                self.cap_scale = self.relax_caps[0]
                o = self._same_height(sl, params, cur)
                self.cap_scale = 1
            if o is not None:
                pids = [p for g in glots for p in self.slicepars.get(sl, {}).get(g, [])]
                changes.append((sl, o, {p: params.get(p) for p in pids}))
                self.apply_outcome(o, params, pids)
                logger.log(15, f"p{page+1} balance s{sl}: badness {cur.badness:.2f} -> {o.badness:.2f}")
        return changes

    def _same_height(self, sl, params, cur):
        """ The best outcome of slice sl with its current height and less badness, or None """
        # glots' text extents differ by fractions of a point; less than a quarter line is no change
        tol = 0.25 * max(self.baselines[g] for g in self.hooks.printer.glots)
        for o in self.slice_outcomes(sl, params):
            if abs(o.height - cur.height) < tol and o.badness < cur.badness - 0.01:
                return o
        return None

    def balance_and_check(self, cur, p):
        """ Balance the slices on page p of cur (balance_page) and lay it out again to check.
            Same height is not quite no change (breaks, notes), so the result is kept only if no
            page done so far that was full has become short. Returns the new state. """
        params = dict(cur.paragraph_params)
        if not self.balance_page(cur, p, params):
            return cur
        checked = self._layout(params, cur, p + 2)
        if checked is None or self._shortened(checked, p):
            logger.log(15, f"p{p+1}: balance changes undone, they made a page short")
            return cur
        return checked

    def _shortened(self, state, p):
        """ Whether a page up to p that was full is short in state """
        return any(self._page_short(state, q) for q in range(p + 1) if q not in self.failed_pages)

    def balance_crossing(self, state, page, single_only=False):
        """ The slice running from page onto the next: if its glots end unevenly there, one
            column has a gap at the top of the next page that no underfill shows. Try the
            outcomes that even its ends, changing its paragraphs that reach the next page.
            single_only: only if its ends are a line apart. Returns a better state or None. """
        glots = self.hooks.printer.glots
        self.prepare_slices(state.parlocs)
        on_page = [sl for sl, pg in self.sliceheights.items() if page in pg]
        if not on_page:
            return None
        sl = max(on_page)
        pages = self.sliceheights[sl]
        if max(pages) <= page:
            return None
        b = self.baselines
        upto = {g: sum(v.get(g, 0) for q, v in pages.items() if q <= page) for g in glots}
        total = {g: sum(v.get(g, 0) for v in pages.values()) for g in glots}

        endtext = self.content(sl, {max(pages)})
        # a glot whose text fills its column on page (it runs on, or ends at the foot of the page
        # level with one that does) gains or loses lines where the slice ends
        ontext = self.content(sl, {page})
        runs_on = [total[g] - upto[g] > 0.5 * b[g] or t >= max(ontext) - 0.5 * b[g]
                   for g, t in zip(glots, ontext)]

        def end_heights(delta):
            """ Predicted text heights per glot where the slice ends, if its glots gain delta (pt):
                a glot running on over the page gains or loses it at its end, its column on page
                being full. None if a glot would carry fewer than min_carry lines over: TeX's widow
                and club penalties would not set it so, and what it would do instead is not
                predicted. Nor may one glot have nothing there while another has some: the
                others would start the page alone. """
            res = []
            for g, e0, d, on in zip(glots, endtext, delta, runs_on):
                e = e0 + d
                if on and 0.5 * b[g] < e < (self.min_carry - 0.5) * b[g]:
                    return None
                res.append(max(0., e))
            empty = [e < 0.5 * b[g] for g, e in zip(glots, res)]
            if any(empty) and not all(empty):
                return None
            return res

        def measured(st):
            """ Imbalance where the slice ends in st """
            self.prepare_slices(st.parlocs)
            pg = self.sliceheights.get(sl)
            if not pg:
                return 0
            return self.empty_lines(self.content(sl, {max(pg)}))

        cur_imb = self.empty_lines(self.content(sl, {max(pages)}))     # as measured
        if cur_imb == 0 or single_only and not self.single_gap(sl, cur_imb):
            return None
        params = state.paragraph_params
        # its paragraphs that reach the next page move where it ends. Shrinking one wholly on page
        # just changes page (and text pulled back brings its notes with it), but growing one in a
        # glot that runs on to the next page pushes a line over, as that glot's column is full.
        movable = {}
        growable = {}       # pid: fewest lines it may have (relative to its unadjusted shape)
        for g in glots:
            movable[g] = []
            crosses = runs_on[glots.index(g)]
            for p in self.slicepars.get(sl, {}).get(g, []):
                pp = self.parpages.get(p, {-1})
                if min(pp) >= page and max(pp) > page:
                    movable[g].append(p)
                elif crosses and pp == {page}:
                    movable[g].append(p)
                    growable[p] = min(0, self.current_delta(p, params))
        allpids = [p for g in glots for p in movable[g]]
        # a gap at the top of a page is worse than a looser paragraph, as when filling a page
        self.cap_scale = self.relax_caps[0]
        options = [self._glot_options(movable[g], growable) for g in glots]
        curcosts = {p: self.shape_cost(p, self.current_delta(p, params)) for g in glots for p in movable[g]}
        self.cap_scale = 1
        cur = {g: sum(self.current_delta(p, params) for p in movable[g]) for g in glots}
        curcost = sum(curcosts[p] or 0. for p in allpids)
        # changes to its other paragraphs count too in whether a glot is changed
        fixed = [any(p not in movable[g] and self.current_delta(p, params)
                     for p in self.slicepars.get(sl, {}).get(g, [])) for g in glots]
        cands = []
        for tots in itertools.product(*[o.keys() for o in options]):
            hts = end_heights([(t - cur[g]) * b[g] for g, t in zip(glots, tots)])
            if hts is None or not self.allowed(hts, [f or bool(o[t][1]) for f, o, t in zip(fixed, options, tots)], sl):
                continue
            imb = self.empty_lines(hts)
            if self.imbalance_cost(imb, sl) >= self.imbalance_cost(cur_imb, sl):
                continue
            dbad = sum(o[t][0] for o, t in zip(options, tots)) - curcost \
                    + self.imbalance_cost(imb, sl) - self.imbalance_cost(cur_imb, sl)
            if dbad < -0.01:
                cands.append((dbad, imb, tuple(pd for o, t in zip(options, tots) for pd in o[t][1])))
        cands.sort(key=lambda c: (c[0], len(c[2])))
        if not cands:
            logger.log(15, f"p{page+1} even s{sl} end: imbalance {cur_imb}, nothing to try")
        nextgap = sum(self._gap(state, page + 1) or [0])
        for dbad, imb, assign in cands[:self.early_crossing_budget if self.early else self.crossing_budget]:
            combo = self._combo(allpids, assign, params)
            if not combo:
                continue
            newparams = dict(params)
            for p, d in combo.items():
                newparams[p] = self.shape_cache[(p, d)][:2]
            new = self._layout(newparams, state, max(pages) + 2)
            if new is None:
                continue
            got = measured(new)
            # no page done may go short, nor the next page get shorter: it may then not fill
            shorter = sum(self._gap(new, page + 1) or [0]) - nextgap
            short = [q for q in range(page + 1) if q not in self.failed_pages and self._page_short(new, q)]
            better = self.imbalance_cost(got, sl) < self.imbalance_cost(cur_imb, sl)
            ok = better and shorter <= 0 and not short
            why = "" if ok else f", undone ({'not evened' if not better else 'p%d short' % (short[0]+1) if short else 'next page %+d' % shorter})"
            logger.log(15, f"p{page+1} even s{sl} end: {combo} imbalance {cur_imb} -> predicted {imb}, "
                           f"measured {got}{why}")
            if ok:
                return new
        return None

    def _glot_options(self, pids, growonly={}):
        """ Returns {total delta: (cost, ((pid, delta), ...))}, the cheapest way to change the
            lines of these paragraphs by each total, from their unadjusted shapes. growonly
            {pid: delta} keeps those paragraphs at that delta or more. Headings are left as they
            are: a gap is better than making one wrap differently. """
        res = {0: (0., ())}
        for p in pids:
            if self.hooks.is_header(p):
                continue
            opts = [(d, c) for d in self.shape_deltas.get(p, ())
                    if d >= growonly.get(p, d) and (c := self.shape_cost(p, d)) is not None]
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
        return max(self.hooks.badness_balance_maxbad * self.maxbad_scale, self.imbalance_weight()) * getattr(self, 'cap_scale', 1)

    def imbalance_weight(self):
        """ Badness of the first line of imbalance in a slice: what balancing it exactly is worth """
        return self.hooks.badness_imbalance_weight * self.imbalance_scale

    def empty_lines(self, hts):
        """ The whitespace glots with heights hts (pt) leave where a slice ends, in column-lines
            (a line of the largest baseline across a column of the glots' mean width): each
            glot's gap below the tallest times its column width, to a tenth of a line """
        glots = self.hooks.printer.glots
        widths = [self.colwidths.get(g) or 1. for g in glots]
        top = max(hts)
        area = sum((top - h) * w for h, w in zip(hts, widths))
        return round(area / (max(self.baselines[g] for g in glots) * sum(widths) / len(widths)), 1)

    def content(self, sl, pages=None):
        """ Per glot, the height of slice sl's text (see get_slicecontent), summed over pages """
        parts = self.slicecontent.get(sl, {})
        return [sum(v.get(g, 0) for p, v in parts.items() if pages is None or p in pages)
                for g in self.hooks.printer.glots]

    def _heights(self, sl, cont, text):
        """ Per glot heights (pt) slice sl would have with text heights text, where cont is its
            text now. TeX sets the glots of a slice to its tallest, so the slice changes height
            by what its tallest text does; each glot is its text plus that common offset. """
        box = max(sum(pg.get(g, 0) for pg in self.sliceheights.get(sl, {}).values())
                  for g in self.hooks.printer.glots)
        off = box - max(cont)
        return tuple(t + off for t in text)

    def text_delta(self, assign):
        """ The change in text height (pt) of setting paragraphs as in assign ((pid, delta), ...) """
        return sum(d * self.parbase.get(p, 0.) for p, d in assign)

    def allowed(self, hts, changed, sl):
        """ Whether slice sl, its glots' text with heights hts, changed (per glot) from their
            unadjusted shapes, may be set so: each changed glot ends level with the slice (unless
            the user fills slices regardless), and a change never leaves a 1 line gap that looks
            like a mistake (see single_gap) """
        if not any(changed):
            return True
        if not self.hooks.fill_slices and not self.levelled(hts, changed):
            return False
        return not self.single_gap(sl, self.empty_lines(hts))

    def single_gap(self, sl, imb):
        """ Whether imb lines of whitespace where slice sl ends is a 1 line gap that looks like a
            mistake. Not in a slice of headings, nor above one (the slice before a heading): they
            have space above them anyway, so a little more does no harm and is better than forcing
            a heading onto another line or a paragraph to stretch. Nor if the
            user fills slices as much as possible regardless (pbpolyfillslices). """
        return 0.5 <= imb < 1.5 and not self.hooks.fill_slices and sl not in self.headgaps

    def levelled(self, hts, changed):
        """ Whether every glot whose paragraphs are changed (changed, per glot) ends within half
            a line of the top: a glot is stretched or shrunk to end level with its slice, or not
            at all, so a gap is never just narrowed """
        tol = 0.5 * max(self.baselines[g] for g in self.hooks.printer.glots)
        top = max(hts)
        return not any(c and top - h > tol for h, c in zip(hts, changed))

    def imbalance_cost(self, imb, sl):
        """ Badness of imb lines of imbalance where slice sl ends. A gap costs imbalance_weight
            for its first line and its own smaller amount for each further one: less whitespace
            is better. A 1 line gap that looks like a mistake (see single_gap) costs twice
            imbalance_weight, and at least the loosest shape that may level it (see balance_page),
            so any shape that can level it does. A 1 line gap in a slice of headings, or above
            one, costs nothing: it is better than making a heading wrap differently. """
        if imb < 0.5 or imb < 1.5 and sl in self.headgaps:
            return 0
        if self.single_gap(sl, imb):
            cap = max(self.hooks.badness_balance_maxbad * self.maxbad_scale, self.imbalance_weight())
            return max(2 * self.imbalance_weight(), self.relax_caps[0] * cap)
        return self.imbalance_weight() + self.hooks.badness_imbalance_narrow * self.imbalance_scale * max(0, imb - 1)

    def shape_cost(self, pid, d):
        """ Badness of paragraph pid at line delta d above its unadjusted shape, or None if unusable """
        if d == 0:
            return 0.
        sc = self.shape_cache.get((pid, d))
        base = self.shape_cache.get((pid, 0))
        b0 = base[2] if base is not None and base[2] is not None else 0.
        # relative to its own unadjusted shape: in narrow columns everything starts loose
        if sc is None or sc[2] is None or sc[2] - b0 > self.maxbad():
            return None
        return max(0., sc[2] - b0) + self.balance_change_cost

    def current_outcome(self, sl, params):
        """ The SliceOutcome of slice sl as currently laid out """
        glots = self.hooks.printer.glots
        pids = self.slicepars.get(sl, {})
        cont = self.content(sl)
        hts = self._heights(sl, cont, cont)
        assign = tuple((p, d) for g in glots for p in pids.get(g, []) if (d := self.current_delta(p, params)))
        cost = sum(self.shape_cost(p, d) or 0. for p, d in assign)
        imb = self.empty_lines(cont)
        return SliceOutcome(hts, cost, imb, cost + self.imbalance_cost(imb, sl), assign)

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
        cont = self.content(sl)
        neutral = [c - self.text_delta((p, self.current_delta(p, params)) for p in pids.get(g, []))
                   for g, c in zip(glots, cont)]
        res = []
        options = [self._glot_options(pids.get(g, [])) for g in glots]
        for tots in itertools.product(*[o.keys() for o in options]):
            chosen = [o[t][1] for o, t in zip(options, tots)]
            text = [n + self.text_delta(ch) for n, ch in zip(neutral, chosen)]
            if not self.allowed(text, [bool(ch) for ch in chosen], sl):
                continue
            cost = sum(o[t][0] for o, t in zip(options, tots))
            imb = self.empty_lines(text)
            res.append(SliceOutcome(self._heights(sl, cont, text), cost, imb,
                                    cost + self.imbalance_cost(imb, sl), tuple(pd for ch in chosen for pd in ch)))
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
        self.sliceheights, self.baselines, self.colwidths = printer.get_sliceheights(parlocs)
        missing = [g for g in printer.glots if g not in self.baselines]
        if missing:     # a layout with no slices of a glot (or none at all): use any baseline
            dflt = max(self.baselines.values(), default=0.) or float(printer.view.get("s_linespacing") or 12.)
            self.baselines.update({g: dflt for g in missing})
        self.slicecontent, self.parbase = printer.get_slicecontent(parlocs)
        self.headslices = printer.get_headslices(parlocs)
        # slices whose gaps are by a heading: headings, and the slice just before one
        order = sorted(self.sliceheights)
        self.headgaps = self.headslices | {a for a, b in zip(order, order[1:]) if b in self.headslices}
        self.shape_deltas = {}      # pid -> line deltas it has shapes for
        for (pid, d) in self.shape_cache:
            if d:
                self.shape_deltas.setdefault(pid, []).append(d)
        self.slicepars = {}
        self.parpages = {}      # pid -> set of pages (0 based) it is on
        for p in parlocs:
            if isinstance(p, ParInfo) and p.slice:
                self.slicepars.setdefault(p.slice, {}).setdefault(p.glot, []).append(p.pid())
                self.parpages[p.pid()] = set(r.pagenum - 1 for r in p.rects)


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

    def solve(self, bk, stop=False, restart=False, chapters=None):
        self.glots = list(self.glotviews().keys())
        logger.log(15, f"{bk}: glot settings {self.glot_settings()}")
        return super().solve(bk, stop=stop, restart=restart, chapters=chapters)

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
        """ Returns (heights, baselines, widths) for a layout (default the latest):
                heights[slice][page][glot] = column height (pt) of that glot in that page slice,
                    as TeX set it (glots padded to align; see get_slicecontent for the text)
                baselines[glot] = baselineskip (pt)
                widths[glot] = column width (pt) """
        heights = {}
        baselines = {}
        widths = {}
        for pnum, g, ci in (parlocs or self.parlocs).polycols:
            if not ci.slice:
                continue
            pg = heights.setdefault(ci.slice, {}).setdefault(pnum - 1, {})
            pg[g] = pg.get(g, 0) + ci.height + ci.depth
            if ci.baseline:
                baselines[g] = ci.baseline
            widths[g] = max(widths.get(g, 0.), ci.width)
        return heights, baselines, widths

    def get_slicecontent(self, parlocs=None):
        """ Returns (content, parbase) for a layout (default the latest):
                content[slice][page][glot] = height (pt) from the top of that glot's first
                    paragraph in that page slice to the bottom of its last: where its text is.
                    Unlike the column heights, this sees space TeX adds to align the glots
                    (above a heading that wraps to fewer lines than in another glot).
                parbase[pid] = the paragraph's baselineskip (pt) """
        ext = {}
        parbase = {}
        for p in (parlocs or self.parlocs):
            if not isinstance(p, ParInfo) or not p.slice or not p.rects:
                continue
            parbase[p.pid()] = p.baseline
            for r in p.rects:
                if r.col < 0:       # not a column of text
                    continue
                e = ext.setdefault((p.slice, r.pagenum - 1, p.glot), [r.ystart, r.yend])
                e[0] = max(e[0], r.ystart)
                e[1] = min(e[1], r.yend)
        content = {}
        for (sl, pg, g), (top, bot) in ext.items():
            content.setdefault(sl, {}).setdefault(pg, {})[g] = top - bot
        return content, parbase

    def get_headslices(self, parlocs=None):
        """ The slices of a layout (default the latest) whose paragraphs are all headings """
        heads = {}
        for p in (parlocs or self.parlocs):
            if isinstance(p, ParInfo) and p.slice:
                heads[p.slice] = heads.get(p.slice, True) and self.isheader(p.mrk)
        return {sl for sl, h in heads.items() if h}

    def report(self, state):
        """ Summarise per glot underfill and slice balance for the current layout """
        heights, baselines, widths = self.get_sliceheights()
        content, parbase = self.get_slicecontent()
        # a gap in a slice of headings, or just above one, does no harm: not counted
        heads = self.get_headslices()
        order = sorted(heights)
        heads |= {a for a, b in zip(order, order[1:]) if b in heads}
        npages = self.parlocs.numPages()
        crossing = [s for s, v in heights.items() if len(v) > 1]
        imbalance = Counter()       # slices wholly on a page with every glot: imbalance in lines -> count
        for s, v in heights.items():
            if len(v) > 1 or s in heads:
                continue
            h = content.get(s, {}).get(list(v)[0], {})
            if any(g not in h for g in self.glots):
                continue
            hts = [h[g] for g in self.glots]
            imbalance[round((max(hts) - min(hts)) / max(baselines[g] for g in self.glots))] += 1
        holes = {}      # page -> lines of gap per glot where a slice crossing onto it ends
        for s, v in heights.items():
            if len(v) > 1 and s not in heads and all(g in baselines for g in self.glots):
                gaps = [int(x + 0.05) for x in end_gaps(v, baselines, self.glots)]
                if any(gaps):
                    holes.setdefault(max(v), []).append(gaps)
        underfull = {i: self.underfills[i] for i in range(npages) if self.underfills[i] is not None}
        for i, u in underfull.items():
            logger.log(15, f"{self.bk} page {i+1}: underfill " + ", ".join(f"{g}={n}" for g, n in zip(self.glots, u)))
        logger.log(15, f"{self.bk}: slice imbalance (lines: count) {sorted(imbalance.items())}")
        print(f"\n{self.bk}: {npages} pages, {len(heights)} slices ({len(crossing)} cross a page), "
              f"imbalance (lines:slices, not counting {len(heads)} of or before headings) {' '.join(f'{k}:{v}' for k, v in sorted(imbalance.items()))}, "
              f"{len(underfull)} pages underfilled: "
              + " ".join(f"{i+1}[" + ",".join(f"{g}{n}" for g, n in zip(self.glots, u) if n) + "]"
                         for i, u in underfull.items()), flush=True)
        print(f"{self.bk}: {sum(sum(x) for h in holes.values() for x in h)} lines of gap at slice ends "
              f"after a page break (not before headings): " + " ".join(f"{i+1}[" + ",".join(f"{g}{n}" for x in h for g, n in zip(self.glots, x) if n) + "]"
                                                   for i, h in sorted(holes.items())), flush=True)
