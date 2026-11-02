# Polyglot Page Filler — Design

The polyglot page filler (`python/lib/ptxprint/poly_filler.py`) extends the
monoglot filler (`page_filler.py`) to side-by-side polyglots by subclassing
`PTXFiller` (`PolyFiller`) and `TypesetterSolver` (`PolySolver`).
`multiprint` creates a `PolyFiller` when the view has `c_diglot`.

## 1. Background: the monoglot filler

A monoglot page is a set of columns, each a stack of paragraph rectangles.
The solver adjusts paragraphs (expansion `e`, stretch/looseness `s`) to change
their line counts by small deltas:

* Probing (`initial_probes`, `evaluate_paragraph_probe`, `collect_probes`)
  builds `probe_cache[pid][(e, s)] -> delta` and
  `shape_cache[(pid, delta)] -> (e, s, badness)`.
* Combos (`paragraph -> delta`) are chosen to fill underfilled pages, page by
  page, with backtracking keyed on where each page starts.
* Results are written to an AdjList.

Footnotes mean a paragraph delta does not guarantee a page delta.

## 2. The polyglot model

### 2.1 Slices

A polyglot page is a vertical stack of **slices**. Only side-by-side glots are
in scope.

* A slice holds the same material in every glot: a usfmerge sync group,
  `\polyglotcolumn L … \polyglotcolumn R … \polyglotendcols`.
* A slice may span pages. A **page slice** is its part on one page.
* **A paragraph lies within exactly one slice.** It may break at a page, never
  across slices. Merge modes that split a source paragraph split it before
  typesetting.
* A slice is as tall as its tallest glot. A glot may be empty in a slice
  (common in heading slices, where only some glots have the heading).
* A heading block is normally its own slice, with its alignment space at the
  top; other slices put it at the bottom. A heading in only some glots can
  also fall inside a body slice (JHN 5:15–16), as more content in that glot.
* Figures are in their own slices, tied to the page holding their anchors.
  Moving anchors is out of scope.

### 2.2 Baselines

Each glot has its own baseline. The engine snaps the start of each slice to a
grid, which can insert a small gap. Imperfect balance from differing baselines
is accepted. Within a slice gridding plays no part; between slices the gap is
a constant for a configuration, so slice positions on a page follow from slice
heights.

### 2.3 Notes

Notes are per glot or full width (`document/diglotsepnotes`). Per-glot notes
give the glots of the last slice on a page different available heights. Note
movement between pages cannot be predicted (notes may be set as paragraphs),
so it is never modelled: layout runs measure it.

### 2.4 Frames

The unit of filling is a **frame**: one page, or a two-page spread sharing one
slice stack (`simplepages`, e.g. `LR,AB`). See 5.4.

### 2.5 Consequences

1. **Paragraph shape is independent; page usage is coupled.** Probing and the
   caches carry over unchanged, keyed by paragraph id, which includes the glot.
2. **A slice's height is `max(h_g)`.** Growing a glot matters for the page
   only if it is (or becomes) the tallest; shrinking only if it is the unique
   tallest.
3. **Slices are sync points.** Material cannot move between slices. The levers
   for a page are the heights of its slices and where each glot of the slice
   crossing the bottom breaks.

## 3. Goals

In priority order:

1. **Balanced pages.** Every glot reaches the bottom of the frame, to within
   its own baseline.
2. **Balanced slices.** Within each slice the glots end level. A glot is
   stretched or shrunk only to end level with its slice, so a gap is never
   just narrowed (a 1 line gap made by stretching looks like a mistake; a gap
   left alone does not). Between layouts that fill the frame equally well,
   less whitespace is better.

Whitespace is an area in column-lines (a line of the largest baseline across a
column of the glots' mean width), so glots of different widths count fairly.
`pbpolyimbalance` is what levelling a slice is worth, `pbpolyimbnarrow` what
each further line of whitespace costs.

* A slice crossing a page can leave a gap at the top of the next page (L=10,
  R=7 breaking at 7 leaves L=3, R=0 over the page). That counts as slice
  imbalance, not as a bad page.
* Small slices (a lone heading, one short paragraph per glot) may stay
  unbalanced.

## 4. Algorithm

Principles:

* Predictions only *order* candidates; they never exclude one. Only a layout
  run says whether a change works (footnotes make effects unpredictable).
* A page has few slices, so all combinations of their changes can be listed.
  What matters is the order they are tried in and the budget of layout runs.
* Filling pages comes first and slice balance second, but every page is
  balanced as well as it can be, including pages that cannot be filled.

### 4.1 Slices as units

A slice is treated as a monoglot paragraph is. Paragraph probes give each
glot's possible line changes; within a slice these are combined into
**outcomes** (`slice_outcomes`): for each change in slice height, the ways to
set its paragraphs, ranked by badness (shape badness above each paragraph's
unadjusted shape, plus the cost of the imbalance left). Up to 3 outcomes per
height change are kept, differing in which glots change. Height changes are in
points: glots on different baselines give uneven steps, and so more options.

The shape cap is relative to a paragraph's own unadjusted badness: in narrow
columns many paragraphs start loose.

### 4.2 Page model

The diglot macros (`ptx-diglot.tex`) fill a page per glot at each sync point:
`\vsplit` the glot's material to the space left (club, widow and keep rules
apply), add its notes, and check what is left. A page is full when the joint
space left is under `\DiglotPageFullTest` (by default the largest baseline).
Diglot keeps about one baseline spare at the foot, so TeX writes a polyglot
underfill record only for a gap of at least 0.95 of the glot's baseline.

The model used to order candidates follows this without notes: whole lines
per glot, a crossing slice breaks only with at least 2 lines each side, and
the next slice starts only if there is at least the largest baseline left.

### 4.3 Filling a page

Pages are filled in order. A page's candidates are all combinations of height
changes of its slices (either direction, mixed), plus per-glot changes to the
slice at the bottom for glots that are short. They are ordered by how close
their net height change comes to one of two targets, then by badness:

* **grow** by about the page's gap; or
* **shrink** enough to take more from the next page (room for the next slice
  to start, or more of the crossing slice). Less can be more.

After each layout run the measured gap re-orders the rest: the next try is the
one expected to close what is still missing, and moves that changed a glot by
more or less than expected scale the expectation for similar moves. A page
stops when every glot is full or its budget is spent: 24 runs plus 2 per
changeable paragraph (up to 60), and up to 80 before any page has failed. If
it runs out of candidates, the shape cap is doubled, then quadrupled: a looser
paragraph is better than a failed page.

Pages are keyed by where they start per glot (`get_page_para_key`); the combos
tried from a start and their measured gaps are kept, so a page reached again
from the same start skips them.

### 4.4 Balance

Balance is judged by where each glot's **text** is (`get_slicecontent`: from
the top of its first paragraph to the bottom of its last), not by column
heights: TeX pads the shorter glots of a slice, and in a heading slice puts
the space above the shorter heading, so equal columns can hide a blank line.
A paragraph changed by d lines changes its glot's text by d times its own
baseline.

Once a page is committed, each slice on it takes any outcome with the same
height and lower badness, checked by a layout run and undone if a page done so
far goes short. Once every page is filled, every page is balanced again,
since backtracking can reset earlier balancing.

Rules for changing a slice (`allowed`, `levelled`):

* A glot's paragraphs change only to make it end level with the slice; no
  change may leave a 1 line gap.
* A 1 line gap left as it is costs at least the loosest shape allowed to fix
  it (twice the shape cap), so any shape that can level it does.
* Headings never change shape to balance. A 1 line gap in a slice of
  headings, or in the slice just above one, costs nothing and is not reported:
  headings have space above them anyway.
* `pbpolyfillslices` (off by default) fills slices regardless: gaps may be
  narrowed, even to 1 line.

**Slices crossing the page** (`balance_crossing`). If the glots of a slice
crossing the bottom end unevenly on the next page, the shorter one leaves a
gap at the top of that page, which TeX's underfill does not see. Once a page
is committed, the filler tries a few outcomes that even the slice's ends,
changing its paragraphs that reach the next page, or that grow a glot whose
column is full on this page (growing it pushes a line over). These outcomes
may use shapes up to twice the shape cap. A change is kept if the measured
ends are more even, no page done goes short and the next page is no shorter.
Not predicted: carrying fewer than 2 lines of a glot over the page (TeX would
not), or leaving one glot with nothing on the next page while another has
some. When the next page is filled, changing that slice there counts the
imbalance at its end, so the fill does not undo the evening.

### 4.5 Failure, backtracking and restart

* A page that cannot be filled is committed with its best measured layout
  (least underfill, then best balance), and filling continues.
* Backtracking goes back up to `s_pbbacktrack` pages (one after a failure). A
  change to an earlier page that keeps the pages between full and gives the
  failing page a new start is followed by refilling it; a change that fills
  it is taken, failing that the best improvement one page back.
* `--restart` (Resume in the GUI) starts at the first page that is not full
  and never changes pages before it, so a user's fixes stay.
* `--stop` ends at the first page that cannot be filled.
* `fill -b "MAT 1-11"` fills only those chapters.

## 5. Implementation notes

### 5.1 Classes

* `PolyFiller(PTXFiller)`: per-glot settings (expansion limits via
  `expansion_limits(view)` for each glot's view), `parsestatus` (underfill per
  glot per page), `get_sliceheights`, `get_slicecontent`, `get_headslices`,
  `report`.
* `PolySolver(TypesetterSolver)`: `limits(pid)` and `neutral(pid)` per glot;
  its own `run_forward` with `fill_page` / `page_candidates` / `_priority`,
  `backtrack`, `balance_page` / `balance_and_check` and `balance_crossing`.
* `PolyHooks.get_page_para_key`: the page start key, per glot.

### 5.2 TeX records

parlocs gets, per page slice and glot:

```
\@Poly@colstart{ht}{dp}{wd}{x}{y}{glot}{slice}{baselineskip}{t|b}
\@Poly@colstop{x}{y}{glot}{slice}
```

`slice` is `\p@lysl@ce`, advanced at the start of `\polyglotendcols` (before
`\pr@sideswitch`). `t`/`b` is where the alignment space goes. Per glot
underfill goes to the `.status` file as
`\st@underfill{page}{glot}{avail}{used}{glot baselineskip}`; `used` includes
the last line's depth.

### 5.3 parlocs and adjlists

* `ParInfo.slice` / `FigInfo.slice` give a paragraph's slice; a page slice is
  `(rect.pagenum, par.slice)`. `ParRect.col` counts slices on the page, not
  physical columns.
* Paragraph ids include the glot (`JHNL1.6[1]`). Headings after `\c` are
  `JHNL2.0`; material before the first `\c` is `start`.
* `C:V` and `C.V` are equivalent: readers accept both, adjlists are written
  with `.` (`JHNL 1.6 +1`), anything shown to users uses `:`. A paragraph with
  no parnum is `X[1]` in the adjlist and `X[]` in the solver.
* One adjlist per merged book: `AdjLists/<book file>-<cfg>-diglot.<ext>.adj`.
  It has one centre per file, so a glot with a different default expansion
  gets `expand=` on its rows.

### 5.4 Two-page frames (`src/polyglot-simplepages.tex`)

`\polyglotpages{LR,AB}` makes a frame of two physical pages (on mirrored
frames written in reverse). Parlocs has no frame marker: frames start on even
pages, so frame = page // 2, and the pages of one frame carry the same slice
ids. Notes, and so available heights, are per physical page. Not yet
supported by the filler.

## 6. Tried and did not work

* **Balancing all slices first, then filling pages** (the first design):
  balancing without knowing where pages break made filling worse (BSB_1 JHN:
  27 underfilled pages before it, 40 after).
* **Filtering candidates by predicted effect** instead of only ordering them:
  predictions miss TeX's page decisions and notes, so pages failed and the
  search ping-ponged between neighbouring pages.
* **Deeper backtracking, or accepting only a page full straight away**: aArp
  grew two pages, or too little was found.
* **Counting gaps at the top of a page as lines short** so the page search
  works on them: many cannot be fixed by paragraph shapes, and fr_diglot RUT
  took 472 runs instead of 35.
* **Slack for the next page's gap** when evening a crossing slice: more short
  pages.
* **Evening crossing slices in the final pass without limit**: undid other
  balancing and made JHN 66% slower; the final pass only evens ends a line
  apart.
* **Heading machinery** (making headings wrap differently to level a slice,
  learning their height effects, trading slice heights on a page): unneeded
  once 1 line gaps in headings were made free.
* **Look-ahead**: keeping an evening that shortens the next page if a few runs
  can fill it. Fewer gaps, but failed pages later on, since a shrink moves
  every later page break.
* **Never shrinking below the shape a page's own fill gave a paragraph**:
  fixed the case it targeted (MAT p50) but blocked a good shrink elsewhere
  (MAT p45) and cost more runs.
* **Filling the slice above a heading** like any other slice: aArp MAT one
  page shorter, but BSB_1 JHN failed a page that otherwise fills.

## 7. Open questions

* Evening a crossing slice predicts that shrinking a glot pulls a line back
  from the next page. When that line carries a note caller whose note will
  not fit, the shrink comes off this page instead (aArp MAT p49/50). The
  prediction should know about note callers.
* Glots with different baselines cannot end exactly level; a leftover under a
  line of a glot's own baseline is counted as a gap (BSB_1: 11pt and 12pt).
* Confirm that the slice stack is shared across both pages of a two-page
  frame, and support frames in the filler.
* Per-paragraph expansion limits set by users through the adjlist (see
  `limits(pid)`), which would also remove the per-glot `expand=` noise.
