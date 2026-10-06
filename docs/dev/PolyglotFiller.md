# Polyglot Page Filler — Design

Status: **draft design**. Nothing here is implemented yet.

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
* Each heading block is its own slice. Heading slices put their alignment
  space at the top, so the heading sits on the text below it. Other slices
  put it at the bottom. Space at the top of a heading slice is kept at the top
  of a page, because the tallest glot reaches the top and the others sit below
  it. It is ordinary slice imbalance.
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
effect (see 4.2).

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

### 4.1 Phase 1: balance slices

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

### 4.2 Phase 2: balance pages

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
* New `balance_slices()` (phase 1), called from `solve` before
  `run_forward`.
* `generate_combos` is replaced by a move generator in the order of 4.2.
* `run_forward`, `attempt_page` and `repair` are kept. They work with pages,
  start keys and combos and do not depend on what a combo contains. They
  count in frames rather than physical pages.
* Paragraph ordering across glots and the exact form of backtrack keys are
  implementation details.

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
* `colcount` misses the last page and starts a new glot at 1.
* `Poly@colstop` does not reset `polycol`.
* Rects carry no slice identity.
* `refre` and `chapre` expect `C.V`. Diglot refs may use `C:V`
  (`ptx-stylesheet.tex:1020`) and then parse as chapter 0.

### 6.3 `page_filler.py` and adjlists

* `get_pidmap`, `col2_first`, `LayoutRunResult.next_bad`, `parselog` and float
  repositioning assume monoglot columns.
* `createAdjs` writes keys without a glot letter. Expansion limits,
  `isheader` and `pid_isjustified` read only the primary view.
* The adjlist format already allows a glot letter after the book. There is
  one `.adj` per merged book (`…-diglot.SFM.adj`).
* **Unconfirmed:** TeX's diglot `\dc@rref` uses both `:` and `.`
  (`ptx-stylesheet.tex:1020` against `ptx-triggers.tex:273`). Needs checking
  with a real diglot run.

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

1. **TeX output.** For each page slice and each glot, write to parlocs:
   * the slice id, on every `\@Poly@colstart` and `\@Poly@colstop`;
   * content height and allocated height (for the last slice on the page,
     the glot's available height after notes), giving the slice underfill;
   * the glot's baseline;
   * whether the alignment space is at the top (headings) or the bottom.

   A glot's frame underfill is then the underfill of its last page slice. No
   page-level record or frame marker is needed.
2. **parlocs fixes** listed in 6.2, and reading of the new records.
3. **Per-glot settings** available to the filler.
4. **Adjlist keys** with glot letters, and the `:`/`.` question resolved.

## 8. Open questions

* Exact parlocs record formats, and where each is written in
  `ptx-diglot.tex`.
* Confirm that the slice stack is shared across both pages of a two-page
  frame.
* Whether phase 2 needs safeguards against repeatedly undoing phase 1 work,
  for example a cap on balance-breaking moves per frame.
