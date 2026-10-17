# Polyglot Page Filler — Design

Status: section 4 (the second design) is implemented in patch 07; the first
design (section 9) was patches 05 to 06b.

This document describes how to extend the page filler
(`python/lib/ptxprint/page_filler.py`) from monoglot (one and two column)
layouts to polyglots, by subclassing `PTXFiller` and `TypesetterSolver`.

## 1. Background: the monoglot filler

A monoglot page is a set of columns. Each column is a stack of rectangles, and
each rectangle belongs to a paragraph. Paragraphs may span columns and pages.

The solver adjusts paragraphs (expansion `e`, stretch/looseness `s`) to change
their line counts by small deltas (±1, ±2):

* Probing (`initial_probes`, `evaluate_paragraph_probe`, `collect_probes`)
  builds `probe_cache[pid][(e, s)] -> delta` and
  `shape_cache[(pid, delta)] -> (e, s, badness)`.
* `generate_combos` chooses combinations of paragraph deltas (a combo is
  `paragraph -> delta`) whose summed effect on each column (`col_deltas`
  against `collengths`) fills an underfilled page.
* Page fullness comes from `Underfill[A|B]` lines in the TeX log.
* `run_forward`, `attempt_page` and `repair` drive the page-by-page search with
  backtracking, using a page start key (first paragraph, lines on the page).
* Results are written to an AdjList.

Due to footnotes, a paragraph delta does not guarantee a page delta.

## 2. The polyglot model

### 2.1 Slices

A polyglot page is a single vertical stack of **slices**. Only side-by-side
glots are in scope, so the stack is a simple list. The stacked `L/R`
"complex" layout is out of scope; its plugin does not exist in `src/`.

* A slice holds the same material in every glot. It is a usfmerge sync group:
  `\polyglotcolumn L … \polyglotcolumn R … \polyglotendcols`.
* A slice may span pages. A **page slice** is the intersection of a slice
  and a page. It consists of a list of rectangles for each glot.
* **A paragraph lies within exactly one slice.** It may be split at a page
  boundary, but never across slices. When a merge mode (e.g. `scores-verse`)
  needs to split a source paragraph, it is split into separate paragraphs
  before typesetting, so this always holds.
* The height of a slice that does not cross a page boundary is the maximum of
  its glots' content heights.
* A glot may be empty in a slice, and then has no rectangles in it. This is
  common in heading slices, where only some glots have the heading (e.g. BSB
  section heads against a Greek text without them). An empty glot has height
  0 in that slice.
* A heading block is normally its own slice. Heading slices put their
  alignment space at the top, so the heading sits on the text below it. Other
  slices put it at the bottom. Space at the top of a heading slice is kept at
  the top of a page, because the tallest glot reaches the top and the others
  sit below it. It is ordinary slice imbalance.
* A heading that exists in only some glots can also fall inside a body slice,
  when the merge does not split it out (JHN 5:15–16, `\s1` in L only). It is
  then just more content in that glot of the slice.
* Figures are in their own slices, typically page width or two side by side.
  A figure slice is tied to the page holding its anchors and never crosses a
  page boundary. Moving anchors is possible in principle, as in monoglot, but
  is out of scope.

### 2.2 Baselines

Each glot has its own baseline, which may or may not equal another glot's.
The engine snaps the *start* of each slice to a grid (the nearest one, or
possibly L's), which can insert a small gap. Imperfect balance caused by
differing baselines is accepted as the typesetter's design choice.

**Convention:** this design talks in lines with a common baseline. Baseline
differences and slice-start gridding are not precomputed. Layout runs measure
their effect, and tests such as "within one line" are applied per glot
(`free_g / baseline_g`) only at the final check.

### 2.3 Notes

Notes are kept either per glot or full width (spanning the page). This is a
project choice (`document/diglotsepnotes`, emitted as `\diglotSepNotes`), so
within a project one mode may be used throughout and the other never occur.
The filler reads the setting up front and must support both modes. At the bottom of a page, per-glot notes take
space from some glots and not others, so the glots of the last slice on the
page have different available heights. Movement of notes between pages cannot
be predicted, so it is not modelled; as in monoglot, layout runs measure its
effect (see 4.3).

### 2.4 Frames

The unit of filling is a **frame**: one page, or a two-page spread whose pages
share one slice stack (`simplepages`, layouts such as `LR,AB`). Whether a
spread is one frame is a setting. See section 6.4 for how frames are rebuilt
from parlocs.

### 2.5 Consequences

1. **Paragraph shape is independent; page usage is coupled.** A glot's
   paragraph line breaking depends only on that glot. Probing, the probe and
   shape caches, and paragraph badness carry over unchanged, keyed by
   paragraph id, which includes the glot.
2. **The effective delta is non-linear.** The height of a slice is
   `max(h_g + d_g)`. For a single-line change `d_i` to glot `i`:
   * Growing (`d_i = +1`) is significant only if `h_i = max(h_g)`.
   * Shrinking (`d_i = −1`) is significant only if `h_i = max(h_g)` and no
     other glot has that height (`h_i` is the unique maximum). Ties are
     common, so shrinking a slice usually needs every glot at the maximum to
     shrink together.

   Changes larger than one line can also matter for a glot below the
   maximum, if they take it past the maximum.
3. **Slices are sync points.** Material cannot move between slices. The
   levers for a page are the heights of the complete slices on it, and where
   each glot of the straddling slice breaks. Moving a whole slice to the next
   page is never used as a move.

## 3. Goals

In priority order:

1. **Balanced pages.** Every glot reaches the bottom of the frame, to within
   its own baseline. This is the primary aim.
2. **Balanced slices.** Within each slice the glots should end as close
   together as possible. This is an optimisation: slack in a shorter glot is
   imbalance to reduce, usually by stretching the short glot or shrinking the
   long one. It is used to choose between configurations that fill the frame
   equally well.

Clarifications:

* A slice that crosses a page can leave a gap at the top of the next page.
  For example, a slice with L=10 and R=7 lines that breaks at 7 gives L=7,
  R=7 on page n and L=3, R=0 on page n+1. Page n is balanced but the slice
  is not. The gap counts as slice imbalance only; it does not make page n+1
  a bad page.
* Small slices, such as a lone heading or one short paragraph per glot, may
  stay unbalanced. Neighbouring slices take up the slack.
* L is the primary glot, and diglot balancing elsewhere gives each glot a
  voting weight. However, when a ±1 change could go to any of several glots,
  the choice is made by the wanted slice height (shorter or longer) and the
  badness of the adjusted paragraphs, not by voting weight.

## 4. Algorithm

This is the second design. The first (separate slice balancing and page
filling phases, patches 05 to 06b) is kept in section 9, with why it was
replaced.

The principles:

* Footnotes make the effect of a change on a page unpredictable. Notes may be
  set as paragraphs, so moving one note across a page break can change the
  height of the note area by almost anything. So predictions only *order*
  candidate combos; they never exclude one. Only a layout run says whether a
  combo works.
* A page has few slices, so all combinations of their changes can be listed.
  What matters is the order they are tried in and how many layout runs a page
  may use.
* More layout runs are better than trusting predictions: each run is measured
  and the measurement chooses the next candidate.
* Filling pages comes first and slice balance second, but every page is
  balanced as well as it can be, including pages that cannot be filled.

### 4.1 Slices as units

A slice is treated as a monoglot paragraph is. Paragraph probes give each
glot's possible line changes; within a slice these are combined to give, for
each change in slice height, the best way to set the slice's paragraphs: the
lowest badness, counting both the shapes' badness and the slice's imbalance
(the slice outcomes of patch 05b). A slice's height change is in points, not
lines: with glots on different baselines it changes in uneven steps, which
gives more options, and options are what is needed.

Within a slice, gridding plays no part: a slice is its own small gridded
world. Between slices the measured gap is a constant for a configuration (0,
−1 or −3pt in the six test diglots), so slice positions on a page follow from
slice heights.

### 4.2 Page model

How the diglot macros fill a page (`ptx-diglot.tex`), per glot at each sync
point:

1. The glot's material is `\vsplit` to the space left for it
   (`trialheight`, before notes), at the best break by the usual penalties
   (club and widow lines, keep with next).
2. The piece is put through the page builder with inserts on, so its notes go
   in (`trialbox`).
3. Space left = `availht − ht(trialbox)` (less its depth if that is over half
   a baseline). If this is the glot's last material and no break is allowed
   after it, 2 more lines must be left. If the result is overfull by more
   than 0.2 baseline, `trialheight` is reduced by one baseline and the trial
   is run again; under one baseline left, the trial fails and the page is
   full.
4. The page is full when the joint space left is under
   `\DiglotPageFullTest` (by default the largest baseline), counting all
   glots' notes, or when `\vsplit` has already rejected what would fit.

The model used to order candidates follows this, without notes: per glot,
whole lines into the space above the note area measured in the last run; a
slice crossing the page breaks only with at least 2 lines each side; the next
slice starts only if the joint space is at least the largest baseline. Notes
are not modelled at all.

### 4.3 Filling a page

Pages are filled in order. A page's candidates are all combinations of:

* height changes of the slices wholly on the page, in either direction and
  mixed (a +15pt and a −12pt can move where the break falls, and so which
  notes go with it);
* for the slice at the bottom of the page (crossing to the next page or not),
  changes to each glot separately.

Nothing is excluded. Candidates are ordered by how close their net height
change comes to one of two targets, then by badness:

* **grow** by about the page's gap, so that the short glots reach the
  bottom; or
* **shrink** enough to take more from the next page: room for the next slice
  to start (about two of its lines) if the page ends at a slice boundary, or
  more of the crossing slice if one crosses the bottom. Less can be more: a
  shorter page can end up fuller.

Mixed combos are ranked by their net change; their badness, the sum of both
parts, puts them after simpler combos with the same net effect.

After each layout run the measured gap per glot re-orders the remaining
candidates: the next one tried is the one expected to close what is still
missing, and a move that changed a glot by a different amount than expected
scales the expectation for similar moves on this page. A page stops when
every glot is full (less than one of its lines short) or when its budget of
layout runs is used up.

### 4.4 Balance

There is no separate balancing pass over the book: in the first design that
made page filling worse before page filling could start. Instead, once a page
is committed, each of its slices takes any outcome with the same height and
lower badness (better balance at no page cost, since slice positions follow
from heights). This applies to every page, full or not.

### 4.5 Failure and backtracking

If a page cannot be filled within its budget, it is committed with the best
layout measured for it: least underfill first, then best balance. Filling
continues from there, so later pages are still filled and balanced.

Backtracking is the exception: at most one page back, and only when no
change on the failing page itself could help, for example when the gap is
set by what starts the page.

## 5. Class structure

### 5.1 `PolyFiller(PTXFiller)`

* `solve`: reads per-glot settings (expansion and shrink limits, styles,
  `isheader`, justification) from each glot's view, not only the primary.
* `parselog` is replaced by reading per-glot slice measurements from parlocs
  (section 7).
* `get_pidmap` becomes `get_slicemap`: slice → page → glot → (lines,
  underfill), plus paragraph → slice.
* `get_page_para_key` returns one entry per glot: the slice and how far into
  it the glot is at the top of the frame.
* `createAdjs` writes keys with the glot letter on the book, e.g.
  `GENL 1:1 +1`, into one adjlist per merged book.

### 5.2 `PolySolver(TypesetterSolver)`

* Unchanged: `initial_probes`, `evaluate_paragraph_probe`, `collect_probes`,
  the probe and shape caches.
* A combo stays `paragraph -> delta`. Paragraph ids include the glot
  (e.g. `GENR1:1[2]`), not just C:V.
* *(First design, section 9.)* New `balance_slices()` (phase 1), called from `solve` before
  `run_forward`.
* `generate_combos` is replaced by a move generator (first design: the order of 9.2; second: 4.3).
* `run_forward`, `attempt_page` and `repair` are kept. They work with pages,
  start keys and combos and do not depend on what a combo contains. They
  count in frames rather than physical pages.
* Paragraph ordering across glots and the exact form of backtrack keys are
  implementation details.

### 5.3 Status

*(Patch 07)* The second design (section 4) replaces the first. `PolySolver`
has its own `run_forward` (it no longer uses `TypesetterSolver`'s page
search, `attempt_page` or `repair`): `fill_page` with `page_candidates` and
`_priority`, `backtrack` and `balance_page`. Points learnt while building it:

* The shape cap is relative to a paragraph's own unadjusted badness: in
  narrow columns (aArp, A5) many paragraphs start at badness 20 to 30, and an
  absolute cap left whole pages with no candidates.
* A slice continuing from the previous page can still change on this page,
  through its paragraphs wholly on this page; that does not move the break.
* Per glot changes to the last slice are only offered for glots that are
  short; a full glot's change only alters what spills to the next page and
  wasted layout runs.
* Each try of a set of slice changes moves its other variants down the order,
  so the budget is spread over different slice changes.
* Pages are keyed by where they start per glot (first paragraph and its lines
  on the page, `PolyHooks.get_page_para_key`). For each (page, start) the
  combos tried and their measured gaps are kept, so a page reached again with
  the same start skips them.
* Backtracking is a two level search. It goes back up to `s_pbbacktrack`
  pages; each change to an earlier page that keeps the pages between full and
  gives the failing page a new start is followed by trying to fill the
  failing page from there (`refill_budget` runs). A change that fills the page
  is taken; failing that, the best improvement found one page back. Changes
  giving a start already seen move down the order. (Going back further and
  accepting improvements made aArp grow by two pages; accepting only a page
  that was full straight away found too little.)
* Budgets: 24 runs to fill a page plus 2 for each paragraph on it that can
  change (up to 60), 12 per earlier page when backtracking, 8 to refill from
  a new start. Not failing matters more than run count.
* Each slice offers up to 3 outcomes for each height change, differing in
  which glots change (so unbalanced expansions are offered, not only the
  cheapest way to a height), and paragraphs use every line delta their probes
  found, not just ±1 and ±2.

Six test diglots (BSB_1 JAS, aArp TestDiglotA5 JAS, WSGlatin, fr_diglot,
my_judson and HEBWLen RUT): 7 lines short in all (aArp 3, WSGlatin 4) in
about 226 layout runs, against 27 lines in about 480 runs for the first
design. Over 18 books (adding BSB_1 HEB, ROM, MRK and WSGlatin, fr_diglot,
my_judson JON, EST, PHP): about 130 underfilled pages at neutral, 54 lines
short after filling with one outcome per height change and fixed budgets,
39 lines (in about 27% more runs) with several outcomes and budgets scaled
by the paragraphs on a page, mostly 1 or 2 lines of one glot. Some cannot be filled: a big slice
whose glots differ by more lines than shapes can change (my_judson EST, L 9
lines short). Pages that fail take most of the runs (BSB_1 MRK, 57 pages,
about 570 runs; two failing pages about 145 each).

Further changes, for what matters to a user (the first failing page, since
the user fixes it, and maybe all that follows, by hand) and for restarting:

* Balance changes at a page commit are checked with a layout: a same height
  outcome still changes paragraphs, which can move a break or a note. If a
  page done so far that was full becomes short, the changes are undone. This
  moved first failures later (BSB_1 MRK page 2 → 8, aArp JAS none).
* Pages before the first failure get more: up to 80 runs a page, backtracking
  up to `s_pbbacktrack` pages with 16 runs each, 10 to refill. After a
  failure: 24 runs a page and one page back.
* A page that runs out of candidates gets new ones with the shape cap doubled,
  then quadrupled: a looser paragraph is better than a failed page.
* Restart (`--restart`, or Resume in the GUI) starts at the first page that
  is not full and never changes pages before it (no balancing, no
  backtracking into them), so a user's fixes there stay. Adjlist ids for a
  paragraph without a parnum (`X[1]`) are matched to the solver's (`X[]`).
  Tested: after a stopped fill, a restart left all 72 paragraph rows on pages
  before the failure unchanged.
* `--stop` ends at the first page that cannot be filled (`HumanFixRequest`).
* TeX writes a polyglot underfill record only for a gap of at least 0.95 of
  the glot's baseline (the filler's measure, since "used" includes the last
  line's depth). With monoglot's half a baseline, a print reported gaps of
  0.5 to 0.9 line as underfilled pages (BSB_1 HEB: 20 pages, really 1).

18 books: first failing pages BSB_1 HEB 24/26, MRK 8/57, ROM 17/35, fr_diglot
PHP 4/10, my_judson EST 2/16 (a structural L imbalance), WSGlatin EST 2/29,
RUT 14/15; the other 11 books fill completely. 27 lines short in all, about
2100 runs.

The notes below describe the first design's code (patches 05 to 06b).

Patch 04 adds both classes in `python/lib/ptxprint/poly_filler.py`.
`PTXFiller.solver_class` names the solver `PTXFiller.solve` creates.
`multiprint` makes the view first (`make_filler_view`) and creates a
`PolyFiller` when it has `c_diglot`, otherwise a `PTXFiller`. So far:

* Each glot has its own expansion limits, read from its view by
  `expansion_limits(view)` (shared with `PTXFiller`). *(Patch 04b.)* The
  solver asks `limits(pid)` for `(expand, minexp, maxexp)` and `neutral(pid)`
  for an unadjusted paragraph's parameters. `TypesetterSolver` returns its
  one set, and `PolySolver` the set for the pid's glot (`pid_glot`, from the
  ref). `PTXFiller.solve` makes the solver before the initial state, so the
  starting parameters come from `neutral`. The adjlist keeps one centre per
  file, so a glot with a different default gets `expand=` on its rows.
* `parsestatus` gives `underfills[page]` = lines per glot, in glot order,
  or `None` when every glot is full. TeX skips the end of a book, as in
  monoglot.
* `get_slicemap` gives `slices[slice][page][glot]` = lines and
  `parslice[pid]` = slice.
* After each layout run, duplicate paragraph ids are reported.
* `PolySolver` probes as `TypesetterSolver` does. `run_forward` then runs
  phase 1 and reports; it makes no page moves yet.
* *(Patch 05)* Phase 1, `balance_slices`: for each slice wholly on one page
  with content in every glot, `_glot_options` gives per glot the cheapest
  set of paragraph deltas for each total line change. Costs are shape
  badness above the paragraph's unadjusted shape, plus
  `balance_change_cost` per changed paragraph. Headers and shapes worse
  than `balance_maxbad` are skipped. Glot heights are the measured page slice
  heights (`ht + dp` from `\@Poly@colstart`, kept in `Paragraphs.polycols`)
  plus delta × the glot's baseline. The combination with the least
  imbalance, in whole lines of the largest baseline, and then the lowest
  cost is used, if it improves the slice. One layout run follows, and
  `check_balance` logs any slice whose measured imbalance differs from the
  prediction. On BSB_1 Diglot_NT JHN it balanced 60 slices. Single-page
  slices went from 23 level (85 measured) to 67 (84), with no mispredictions
  (10 slices now cross a page), and the book went from 66 to 65 pages.
* *(Patch 05b)* Slices are described by outcomes. `slice_outcomes(slice,
  params)` lists every assignment of the slice's paragraph shapes as a
  `SliceOutcome`: per glot heights (pt) for the whole slice, cost (sum over
  changed paragraphs of badness above the unadjusted shape, plus
  `balance_change_cost` each), imbalance (lines of the largest baseline),
  `badness = cost + imbalance weight × imbalance`, and the
  assignment. Assignments are relative to unadjusted shapes, so they don't
  depend on the current state; heights are measured from the current layout
  less the current deltas. `slice_range` gives (min height, lowest badness
  outcome, max height), and `fit_slice(lo, hi)` the lowest badness outcome
  whose height (tallest glot) is in range. Phase 1 gives a single-page slice
  its lowest badness outcome when that beats `current_outcome`. The weight
  and the shape cap are `Hooks` settings that are factors of about 1, like
  the other filler settings, so users need not think in shape badness
  units: the cap is `badness_balance_maxbad` (1.0) × `PolySolver.maxbad_scale`
  (20) and a line of imbalance costs `badness_imbalance_weight` (1.0) ×
  `imbalance_scale` (10). On JHN most probed shapes have badness under 2 and
  loose ones are over 20, with little between, so the cap sits in the gap. With these values phase 1 makes the same choices as patch 05 on
  JAS (12 slices) and JHN (60). For a slice crossing the page, phase 2 will
  want the part on the page, `min(h_g, available)` per glot, and the overall
  badness of the two-part slice (`fit_slice_page`, still to come).
* *(Patch 06)* Phase 2 reuses `TypesetterSolver.run_forward`, `attempt_page`
  and `repair`. `PolySolver.run_forward` runs phase 1, sets `base_params` and
  `init_state` from it, hands over, and ends with a full layout if the last
  one stopped at a chapter (`s_stopat`), so the report, adjlist and PDF cover
  the book. `PolyHooks.get_page_para_key` gives the page start key per glot.
  `generate_combos` is the move generator. Footnotes make effects
  unpredictable, so predictions only order candidates; each is judged by its
  layout run. Candidates, from a snapshot of the attempt's own parlocs:
  private moves (a glot of the page's last slice, crossing or not, gets more
  or fewer lines); slice moves (slices wholly on the page change height,
  combined up to `max_slices`, all growing or all shrinking, since a page is
  one column of slices); pull in (if the page ends at a slice boundary, shrink
  by about `pull_lines` lines so the next slice can start); and mixed (a
  growth plus private fix ups). A full page also gets candidates, any change
  in where it ends, cheapest first, which is what lets backtracking work. The
  cheapest candidate for each predicted effect is tried first; a combo may
  change at most `badness_maxr` paragraphs. Underfill lines are rounded down
  (`parsestatus`), since "used" includes the last line's depth and part of a
  line can't be filled. Result on six diglots (BSB_1 JAS, aArp TestDiglotA5
  JAS, WSGlatin, fr_diglot, my_judson and HEBWLen RUT): all pages filled
  except 3 of WSGlatin's, but BSB_1 and aArp took 255 and 349 layout runs.
* *(Patch 06b)* Fewer layout runs, as monoglot does it: only the cheapest
  combo for each predicted effect is tried, and on a page with underfill only
  combos predicted to cover the need (plus pull in shrinks). `repair` records
  the page it is repairing for and its need; earlier full pages then try
  growth first (it pushes material onto the short page), closest to the need,
  and shrinks after. Filtering instead of ordering, or capping the candidates
  per repaired page, lost filled pages. Runs: BSB_1 JAS 255 → 136, aArp JAS
  349 → 239, others unchanged except my_judson RUT (16 → 77 runs, 1 page
  left underfilled, from repair ping-pong). Most runs are spent backtracking
  between neighbouring pages, which suggests the move predictions are often
  wrong; measuring predicted against measured effects is the next step.

## 6. Findings from the current code

### 6.1 TeX (`src/ptx-diglot.tex`)

* `\polyglotendcols` runs trials (`\diglot@run@trials`) that `\vsplit` each
  glot's content to `availhtX`. Overflow is kept in `excessX` and carried to
  the next page.
* `@prepare@layout@simplecols` computes the joint delta so the next slice
  starts below the tallest glot (an `@gridone` variant exists).
* `\dglt@calc@vailht` = textheight − partials − joint delta − notes − inserts.
  A page is full when availht < `\DiglotPageFullTest` or any glot has excess.
* **Diglot mode writes no `Underfill` log lines.** New output is required.
* `\@Poly@colstart{ht}{dp}{wd}{x}{y}{X}` and `\@Poly@colstop{x}{y}{X}` are
  written to `.parlocs` once per glot per page slice.

### 6.2 `parlocs.py`

* `ParInfo.glot` is set from `Poly@colstart`.
* `ParRect.col` is a running count of slices on the page for that glot, not a
  physical column.
* `colcount` misses the last page and starts a new glot at 1. *(Fixed in
  patch 02. It is the highest 0-based column start index on any page, so
  for polyglot it counts slices per page, not columns. Its only user,
  `layout_checks`, is disabled.)*
* `Poly@colstop` does not reset `polycol`. *(Fixed in patch 02: it returns to
  `L`. Outside slices there are only page records, `noteid`, and at the end
  of a book a monoglot `\@colstart`/`\@colstop`.)*
* Rects carry no slice identity. *(Fixed in patch 02: `ParInfo.slice` and
  `FigInfo.slice`, 0 when not polyglot. A paragraph lies in one slice, and a
  slice keeps its id across a page break, so all its rects share the
  paragraph's slice and rects carry none of their own: a page slice is
  `(rect.pagenum, par.slice)`. The reader warns if a paragraph continues in
  a different slice.)*
* `refre` and `chapre` expect `C.V`. Diglot refs may use `C:V`
  (`ptx-stylesheet.tex:1020`) and then parse as chapter 0. *(Fixed in patch
  02: both accept either separator.)*
* Heading paragraphs before the first verse have the ref `start` with no
  book or glot, so their pid (`start[n]`) is not unique across glots.
  *(Fixed in patch 03 for headings after `\c`: on `\c` a diglot set
  `\c@rref` but not `\dc@rref`, which adjustments and parlocs use, so such
  headings kept the previous chapter's last verse, e.g. `JHNL1.51` for the
  chapter 2 heading. They are now `JHNL2.0` as in monoglot. Material before
  the first `\c` is still `start`, as in monoglot.)*

### 6.3 `page_filler.py` and adjlists

* `get_pidmap`, `col2_first`, `LayoutRunResult.next_bad`, `parselog` and float
  repositioning assume monoglot columns.
* `createAdjs` writes keys without a glot letter. Expansion limits,
  `isheader` and `pid_isjustified` read only the primary view.
* The adjlist format already allows a glot letter after the book. There is
  one `.adj` per merged book (`…-diglot.SFM.adj`).
* `C:V` and `C.V` are equivalent, but some contexts require one. Readers
  accept both. Adjlists are always written with `.` (`JHNL 1.1 +1`).
  Anything shown to users uses `:`. In a real diglot run (BSB_1 Diglot_NT,
  JHN) every parlocs ref uses `.` (e.g. `JHNL1.1`). TeX matches adjustments
  against `\dc@rref`, which `\@v@` sets with `:`, but `\ch@ckadjustments`
  resets it with `.` (`\settrig@refcv`) before matching.
* *(Patch 03)* `createAdjs` writes the glot letter after the book
  (`JHNL 1.6 +1`), taken from `refSort(pid)[3]`; monoglot output is
  unchanged. `AdjList` already reads and writes glot letters, and its
  `get_params` keys (`JHNL1.6[1]`) match parlocs pids. TeX opens
  `AdjLists/<book file>-<cfg>-diglot.<ext>.adj` for a merged book, which is
  what `getAdjListFilename` gives when `c_diglot` is set. Tested: an entry
  for one glot changes only that glot's paragraph at that ref.

### 6.4 Two-page frames (`src/polyglot-simplepages.tex`)

* `\polyglotpages{LR,AB}` makes a frame of two physical pages: in normal
  order the first holds L+R and the second A+B.
* The slice stack appears to be shared across the frame: each slice is laid
  out once, and each page shows its own glots' columns at the same height
  (`\@@do@simplepage@` runs the simplecols routine once per page). This needs
  confirming.
* Each page is shipped out separately, so parlocs has an ordinary `\@pgstart`
  per physical page and no frame marker.
* On mirrored frames (`\ifdiglotInnerOuter` or `\ifdiglotSwap`) the pages are
  written in reverse order, so the first physical page may hold A+B.
* Top inserts are forced to equal height across all glots of the frame.
* Two-page frames start on an even page (`\zNeedEvenPage`).

Frames are rebuilt without a marker. The frame size is known from the layout
and two-page frames start on even pages, so frame = page // 2. Blank padding
pages carry no slices and are skipped. Slice ids confirm the grouping: the
pages of one frame carry the same slice ids, while neighbouring frames share
at most the slice that crosses between them. The glot letters on the rects
show which page of a mirrored frame holds which glots. Notes, and so each
glot's available height, are per physical page. Page numbers from parlocs,
the page-to-chapter map (`hooks.chapters`), `s_stopat` and progress reporting
must be translated to frames.

## 7. Prerequisites

Before the solver work:

1. **TeX output.** Done (patch 01). For each page slice and each glot, parlocs
   has:

   ```
   \@Poly@colstart{ht}{dp}{wd}{x}{y}{glot}{slice}{baselineskip}{t|b}
   \@Poly@colstop{x}{y}{glot}{slice}
   ```

   * `ht + dp` is the glot's content height in this page slice. (Before
     patch 01 these were expanded at shipout, so every record on a page held
     the glot's last slice's values.)
   * `slice` is `\p@lysl@ce`, advanced at the very start of
     `\polyglotendcols`, so it counts usfmerge sync groups from 1. It must
     come before `\pr@sideswitch`, because ordinary chunks are prepared inside
     that call, while heading chunks are prepared in the trials after it.
   * `t` means the alignment space is at the top (all-heading chunk), `b` at
     the bottom.

   A glot's available height cannot be recorded per slice: `availhtX` is the
   trial's vsplit target and excludes notes, and separate notes are placed with
   glue, so the bottom of a glot's text area has no position to save. Instead
   each page writes one underfill record per glot to the `.status` file,
   reusing the monoglot record with the glot letter as the column:

   ```
   \st@underfill{page}{glot}{avail}{used}{glot baselineskip}
   ```

   * `avail` = `\textheight` − inserts − that glot's notes (plus
     `\AboveNoteSpace`), or the combined notes when notes are not separate.
   * `used` = text height up to the last sync point + the glot's content
     since then (`@curXht`). It includes the last line's depth, unlike
     monoglot's `\ht\colA`. It equals the text top minus the glot's last
     colstop in parlocs.
   * As in monoglot, nothing is written when the gap is under half the glot's
     baseline, and nothing for the empty page flushed at the end of a book.

   Diglot keeps about one baseline spare at the foot
   (`\dglt@calc@vailhttail` subtracts `\@minb@seline`), so many pages show a
   one-line underfill.
2. **parlocs fixes** listed in 6.2, and reading of the new records. Done
   (patch 02).
3. **Per-glot settings** available to the filler.
4. **Adjlist keys** with glot letters, written with `.` (see 6.3). Done
   (patch 03).

## 8. Open questions

* Confirm that the slice stack is shared across both pages of a two-page
  frame.
* *(First design)* Whether phase 2 needs safeguards against repeatedly
  undoing phase 1 work, for example a cap on balance-breaking moves per
  frame. (The second design has no separate phase 1.)
* How big a page's budget of layout runs should be, and whether it should
  depend on how short the page is.
* With `limits(pid)` the limits are per paragraph. Users could set them for
  individual paragraphs, perhaps by extending the adjlist (e.g. min/max
  expansion alongside `expand=`), and the filler would keep to them when
  probing. To consider: the syntax in the comment field, how it fits with the
  per-file centre and range, showing it in the adjlist view, and whether TeX
  needs to know (probably not: it only limits the filler's search). The
  centre is already a problem for polyglots: an adjlist has one centre per
  file, taken from the primary, so a glot whose default expansion differs
  gets `expand=` written on every one of its rows. Per-glot (or
  per-paragraph) defaults in the adjlist would remove that noise.

## 9. History: the first algorithm

The first design (patches 05 to 06b) had two phases. Its text is kept here.

### 9.1 Phase 1: balance slices (first design)

For a slice that does not cross a page boundary, each glot's height is the
sum of its paragraphs' lines plus fixed spacing. Notes are handled elsewhere,
and there are no `\vadjust` or `\nobreak` effects. Phase 1 can therefore be
computed from probe data alone:

* For each slice, choose paragraph deltas per glot (from `shape_cache`) that
  bring the glots closest to equal at the lowest badness. This is a small
  knapsack problem per slice and needs no layout runs.
* Balancing is best effort. If a slice cannot balance, leave it.
* One layout run checks the result. That run also shows which slices cross a
  page boundary; those belong to phase 2.

The result is the starting configuration for phase 2, replacing the
all-default `base_params`. Phase 1 is cheap, so phase 2 can rerun it on the
slices around a page it has just changed.

### 9.2 Phase 2: balance pages (first design)

Let `u_g` be glot `g`'s underfill at the bottom of the frame. The frame is
balanced when `u_g` is less than one of glot `g`'s lines for every glot. A
paragraph change is one of two kinds:

* **Private move:** a change to glot `g` within the slice that crosses the
  bottom of the frame. It affects only glot `g` on this page (and its
  leftover on the next page).
* **Shared move:** a change to a slice wholly on the frame that changes the
  slice's height by Δ. Everything below it moves by Δ in every glot. Glots
  that carry on past the bottom are unaffected on this page apart from how
  much spills over; glots that finish early lose or gain Δ of gap. A change
  to a glot that does not set its slice's height has no page effect and only
  changes slice balance.

A combo must satisfy, for every glot:

```
shared + private_g ≈ u_g
```

This generalises the monoglot per-column test (`col_deltas` against
`collengths`), with one column per glot plus a shared component.

Starting from balanced slices, moves are tried in this order:

1. **Private moves.** Cheap, independent per glot, and aimed directly at each
   glot's gap.
2. **Shared moves that keep balance:** change every glot of a slice by the
   same amount, so the slice grows or shrinks and stays balanced. Its cost is
   the sum of the paragraph badnesses.
3. **Shared moves that break balance:** grow one glot of a balanced slice.
   This is a last resort because it undoes phase 1 work.

The effect of each combo is confirmed by a layout run, which also accounts
for notes moving and slice-start gridding.

#### Footnotes

Footnotes make the equation above approximate at best. Only text that crosses
the page boundary changes where notes go, but when it does, its notes move
with it, and how much note text moves cannot be predicted (notes may split
across pages, and note breaking depends on the whole note area). So:

* A private move's effect on `u_g` may be less than, more than, or opposite
  to its text delta.
* A shared move of Δ affects each glot differently (Δ_g), depending on the
  notes attached to the lines each glot pushes across the boundary.
* With full-width notes all glots share one note area, so every move is
  effectively shared. In this mode the move generator does not rely on the
  private/shared distinction for page effects; it still prefers private
  moves for their lower cost to slice balance.

The equation is therefore used only to generate and rank candidate combos,
ignoring notes. Note effects are never precalculated: each candidate is
judged by its layout run, as in monoglot. A combo whose measured effect
differs from the model shows that glot's boundary is note-sensitive on this
page, which can be used to reorder the remaining candidates for that page.

### 9.3 Why it was replaced

* Phase 1 balanced slices without knowing where pages break, which made page
  filling worse (BSB_1 JHN: 27 underfilled pages before it, 40 after), and
  phase 2 then spent layout runs undoing it.
* Phase 2 predicted each move's effect from line deltas and then filtered
  candidates by the prediction. The predictions miss TeX's page decisions
  (the one baseline back off, the two line rule, the full page threshold) and
  notes, so pages failed and the search backtracked between neighbouring
  pages: on six test diglots everything filled except three WSGlatin pages,
  but BSB_1 and aArp JAS took 136 and 239 layout runs (monoglot JAS takes
  about 12). Filtering, capping and ordering changes moved the cost between
  books rather than removing it.
