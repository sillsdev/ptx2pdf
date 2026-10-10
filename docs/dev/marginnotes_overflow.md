# Margin note overflow: Python plan

Oct 10, 2026 · @Martin

## Goal and scope

When a column's margin notes cannot all fit inside the text block, `marginnotes.py` should push the excess to the top of the next column slot instead of shoving notes off the page. A slot is one column of one page, taken in reading order, so overflow from the first column goes to the second column, and overflow from the last column goes to the first column of the next page.

Python decides every push between runs and writes it into `.marginnotes`. TeX carries those pushes out, holding pushed notes in a global box and drawing them at the top of their target column. The Python plan comes first, then the TeX changes.

The plan was worked out against `sillsdev/ptx2pdf` master: `python/lib/ptxprint/marginnotes.py` and `src/marginnotes.tex`.

## How marginnotes works today

TeX and Python pass one file back and forth. TeX writes where each note landed; Python reads it, works out shifts, and writes the file back for the next TeX run.

1. TeX reads `.marginnotes` at the start of the run (`\@marginnote` lines), storing each note's `:pageno` and `:colno` under `marginnote-<ref>@<marker>`.
2. `\d@marginnote` builds the note box and resolves its side from the style's `\MarginNoteSide` plus a parity: `:pageno` in single-column mode, `:colno` in multi-column mode, or `\pageno` on the first run.
3. `\pl@cemnote` attaches it to the anchor line with `\vadjust`, applying the x and y shifts as kerns, and writes a new `\@marginnote` line at shipout.
4. `tidymarginnotes` (called from `runjob.py`) reads that file, lays out each page, and writes it back. If anything changed, runjob reruns TeX.

The 13 fields of an `\@marginnote` line, and who uses them:

| Field | Written by TeX as | Read by TeX for | Used by Python for |
| --- | --- | --- | --- |
| ref, marker | note identity | the lookup key | identity |
| hpos | the style's side (`\p@s`: left, right, inner, outer) | ignored | resolving side with `getside` |
| vpos | valign (top, bottom, center, inline) | ignored | `boxshift`, i.e. where the box sits around `ypos` |
| gap, width, height, depth | note geometry | ignored | note extents |
| xoffset | x shift applied this run | the x kern | x extents |
| yoffset | y shift applied this run | the y kern | written back as yoffset − yshift |
| pnum | `\the\pageno` at shipout | `:pageno` (side parity) | grouping notes into pages |
| xpos | `\pdflastxpos` | `:colno` (side parity in multi-column) | grouping notes into tracks |
| ypos | `\pdflastypos` | ignored | the note's current y |

The file mixes two units. Lengths (gap, width, height, depth, xoffset, yoffset) are written with a `pt` suffix: TeX writes them via `\the\dimen` (for example `5.0pt`), and Python writes them with five decimals (`5.00000pt`). Positions (`xpos`, `ypos`) are bare integers in sp, taken straight from `\pdflastxpos`/`\pdflastypos` and measured from the bottom-left of the paper, so y grows upward. `readpts` turns both into pt on reading, treating a bare number as sp, and `outfile` writes positions back as `int(pt × 65536)`. `top` and `bot` from `getTextBlockSize` are in pt.

Because `\pdfsavepos` runs inside the `\vadjust` (vertical mode, before the note box), `xpos` is the left edge of the column the anchor sits in. Every note in the same column on a page records the same `xpos`, whatever its width or side. The side, gap, width and x shift all live inside the box, after the position is saved.

## Problems found

Four problems in the current Python need fixing, and the first two are bugs today, independent of overflow.

**1. `outfile` is not idempotent.** It adds the new shift to `yoffset` but writes `ypos` back unchanged, so the file claims the note is still where it was. Run on its own output, the algorithm applies the same shift again. Verified: four overlapping notes gave shifts of 40, 10, −20 and −50pt on every pass, and after three passes the first note's `yoffset` was −120pt instead of −40pt.

**2. Overflow has no outlet.** When a track's notes are taller than `top − bot`, `processpage` pushes them past the bottom, then back up past the top, and logs "Shift out of bounds". Nothing ever moves to another page or column.

**3. The x model is column-relative, not absolute.** `xmin`/`xmax` are `xpos + xoffset ± gap/width`, measured from the column's left edge with no `\hsize`. For right-side notes this is off by a whole column width. It is fine for grouping notes into tracks, but not for placing them. It also adds `xoffset` for both sides, whereas TeX moves left-side notes away from the text by that amount, which is the opposite direction. That never mattered while Python left `xoffset` alone.

**4. Side in multi-column mode is driven by `xpos`.** `\@m@rginnote` derives `:colno` from `xpos`, and `\d@marginnote` uses `:colno` as the side parity in multi-column mode. The file's `hpos` field is ignored by TeX. So today the only way Python could steer a note's side is by rewriting `xpos`, which also corrupts Python's own record of where the anchor is.

## Design decisions

These came out of the discussion; each one closes off an approach that turned out not to work.

1. **The unit of capacity is a column slot, not a page.** Slots run (page N, col 0), (page N, col 1), (page N+1, col 0) in reading order. A single-column page is one slot. Col 0 is always first in reading order, because `\@m@rginnote` already swaps column numbers under `\ifRTL`.
2. **The `.marginnotes` file is a fixed point.** Running the algorithm on its own output must change nothing. This rules out sentinel values such as `ypos` = 0, rewritten page numbers or rewritten sides in the note lines, since those destroy the anchor information Python needs to decide again.
3. **Note lines are anchor state; pushes are separate instruction lines.** Each `\@marginnote` line stays exactly what TeX would write for the anchor. A pushed note gets an extra `\@marginnotepush` line carrying its target. Python ignores push lines on read and regenerates them every pass, so it decides every push again from the true anchor, and no push is sticky.
4. **Python resolves the side; TeX uses it.** For a pushed note, Python writes the resolved `left`/`right` in the push line, so `xpos` no longer has to be faked to steer `:colno`.
5. **Pushed notes form a fixed block at the top of their slot.** They are stacked at their natural height and kept out of `processpage`, with no `yshift`. Native notes on that slot are laid out below the block, so they can never interleave with it.
6. **Python owns the vertical model of a pushed block; TeX owns placement.** TeX stacks held boxes from the top of the slot with no kerns. Python's model must match that stacking exactly, so neither side needs absolute positions from the other.

Rejected along the way:

- **An insert class to carry held notes.** The galley keeps inserts inline, and every trial repagination with `\holdinginserts` = 0 extracts them again, appending duplicates to the insert box. An insert is also unnecessary: the push line gives an absolute target page, so a note never needs to be tied to its anchor's page.
- **A second insert for notes carried over from the previous page.** These notes are already resolved by the time they are carried, so a global box is enough, and it keeps them away from the page builder.
- **Returning held notes to the main vertical list.** The first box on a page takes `\topskip` and keeps interline glue that would otherwise be discarded, so the first text line drops by about a baselineskip.
- **Unpacking `\box255` at shipout to pull notes out.** `\lastbox` loops stop at whatsits and marks, and pages are full of them.
- **Negative y values for pushed notes on the target page.** `processpage` would shift them back into the slot, giving them `yshift` values that TeX would then have to ignore.

## File format

The file keeps its current note lines, with one change to what Python writes in them, and gains one new line type for pushes.

**Note lines** keep all 13 fields as today, always describing the anchor. Python writes them exactly as TeX would after applying Python's shifts:

- `yoffset` = old `yoffset` − `yshift`, as now.
- `ypos` = old `ypos` + `yshift` (new). The note line then says where the note will be, so a second pass finds nothing to move.
- For a pushed note, every field is left as read. `yshift` is 0 for these notes, so the line is unchanged and still describes the anchor.

**Push lines** are new. There is one per pushed note, written after all the note lines:

```
\@marginnotepush{GEN 1:11}{f}{2}{0}{right}
```

The fields are ref, marker, target page, target column, and resolved side (`left`/`right`). TeX reads the whole file before placing anything, so line order doesn't matter to it. Python skips these lines when reading.

TeX uses the target column: it draws each column's stack at the top of that column's box. The side picks which way the note is lapped when TeX builds the box.

**The fixed-point rule.** For any file F that Python writes, reading F and writing again must produce F byte for byte. Two details of units make this harder than it sounds:

- **Round positions to whole sp.** `ypos` + `yshift` is a fractional sp, and `outfile` truncates it with `int()`. The second pass then sees a position up to 1sp away from where the first pass meant it to be, computes a tiny `yshift`, and the five-decimal `yoffset` changes. So Python should round to the nearest sp when writing, and treat any |`yshift`| under 1sp as zero.
- **Compare in Python's own formatting.** A file freshly written by TeX never matches Python's output byte for byte, because TeX writes `5.0pt` where Python writes `5.00000pt`. The change check therefore compares Python's output with the input as Python would format it unchanged, not with the raw text it read.

With both in place, `outfile` reports a change only when a value actually moved. That replaces the current "any non-zero `yshift`" test, which would report a change on every pass once any note is pushed.

## Python changes

The changes follow the pipeline in order: read, build the column grid, assign slots and sides, lay out slot by slot with pushing, then write.

### 1. Inputs

`MarginNotes` (and `tidymarginnotes`) gain one parameter from runjob, `rtl`, which is needed to map x clusters to column numbers and to resolve sides. No column width is needed (see step 5).

The existing `psize`, `top` and `bot` stay.

### 2. Reading

- Parse `\@marginnote` lines as now. Skip `\@marginnotepush` lines; they are regenerated.
- Render the notes as read in Python's own formatting, for the change check in step 9.
- Notes keep their fields untouched. All derived values (column, slot, side, pushed target) go in new attributes that `outfile` never writes into note lines.

### 3. Column grid

Built once per run from raw `xpos` values, separately for odd and even pages, since mirrored margins or a binding gutter make them differ.

1. Cluster each parity's `xpos` values within a small tolerance (2pt).
2. Keep the clusters with the most notes, up to the number of columns (2), and sort them by x.
3. Map them to column numbers: lowest x is col 0 in LTR, highest x is col 0 in RTL.
4. Δ = the difference between the two columns' x. It should agree across parities; if one parity has only one cluster, take the second column from the other parity's Δ.
5. One cluster in total means a single-column book: every page has one slot.

Notes whose `xpos` falls outside the kept clusters (sidebars and other shifted boxes) snap to the nearest column and get a debug log line.

### 4. Slot and side for each note

- **Column:** the nearest grid column to the note's raw `xpos`. This is always the anchor's column, because note lines are never rewritten.
- **Slot:** (page, column), ordered as page × columns + column.
- **Side:** resolved the way `\d@marginnote` does it. The parity is the column in a multi-column book and the page otherwise, combined with `hpos` and `rtl`. This replaces `getside(pnum, hpos)`, which only knows the page.

### 5. Tracks

No change. The existing `get_tracks` already splits a page's notes into non-overlapping collections in x for each side. Columns separate naturally, because each column has its own `xpos`, so each track is one side of one column, which is one slot. The slot loop uses it as it is, including for working out the height of each track's pushed block.

The only point of contact is the side. `get_tracks` sets `n.side` from `getside(pnum, hpos)`, so it must instead use the side resolved in step 4: the push line's side for pushed notes, and column parity in multi-column books.

### 6. The slot loop

`processpages` walks the slots in order, carrying a queue of pushed notes from one slot to the next.

1. **Take the incoming block.** These are the notes pushed into this slot, already in TeX's stacking order: notes pushed from earlier slots first, then document order. Each gets the side resolved for this slot.
2. **Split by track.** Group the block and the slot's native notes into tracks (see step 5).
3. **Fit the block.** For each track, add up block heights (height + depth). If the block alone exceeds `top − bot`, the notes from the first one that doesn't fit onward go to the front of the outgoing queue.
4. **Fit the natives.** Capacity left is `top − bot − H`, where H is the height of the block that stayed. Take natives top-down by `ymax`. The first one that doesn't fit, and all after it, go to the outgoing queue after any block overflow.
5. **Guard oversized notes.** A note taller than a whole slot is left where it is with an error logged, rather than pushed for ever. This guard only applies when the note is first in its slot.
6. **Lay out the natives.** Run `processpage` on the remaining native notes with the track's top lowered by H. Block notes never enter `processpage` and keep `yshift` = 0.
7. **Record pushes.** Each block note that stayed gets its push target: this slot's page, column and resolved side.

A note whose anchor slot has room is never pushed, so a note can come back as soon as space frees up.

### 7. Fixed-side notes in multi-column books

A note whose `hpos` is `left` or `right` keeps that side wherever it goes, so pushing it into a column where that side faces the gutter would put it between the columns. Such a note is pushed only to slots where its side is an outer edge. In LTR that means `left` goes only to col 0 and `right` only to col 1; RTL is the mirror image. Slots in between are skipped.

### 8. `processpage`

- Takes a per-track top instead of always `self.top`.
- Works on native notes only.
- Keeps its current weighting and settling logic. Its out-of-bounds error now only fires for a single oversized note, since everything else has been made to fit.

### 9. Writing

- **Note lines:** written for every note in file order, with `yoffset` −= `yshift` and `ypos` += `yshift`. Pushed notes have `yshift` = 0, so their lines are unchanged.
- **Push lines:** written after all note lines, one per pushed note, in TeX stacking order.
- **Change check:** `outfile` returns true only if the new text differs from that rendering of the input (see File format). If a note sits in the same place two runs running, no rerun is triggered.

### 10. Callers

`runjob.py` passes `rtl` through `tidymarginnotes`. No other caller constructs `MarginNotes`.

## Edge cases and open questions

None of these needs special handling in the first version. Overflow is rare, at about two pages per Bible, so simple rules are enough.

**Decided**

- **Mixed pages need nothing extra.** The two-column study-note section is itself an insert and takes no margin notes, so only the single-column text above it has any. That page is one slot. Python doesn't know how tall the single-column block is, so it uses `top − bot` as usual; if notes run down beside the study notes, that is acceptable.
- **Overflow may cross book boundaries.** Python doesn't know where books end, so a book's last-page overflow can land in the next book. Given how rare overflow is, that's acceptable. A later option is for TeX to write book boundaries into `.marginnotes` so pushes can stop there.
- **All markers can be pushed.** Chapter/verse numbers and notes are normally in different tracks, so chapter/verse numbers shouldn't overflow. No marker is excluded.

**Handled by the plan**

- **Layout mode at paragraph time.** TeX decides whether to use `:pageno` or `:colno` according to `\c@rrentcols` when the paragraph is built. Pushed notes avoid this, because the push line supplies the side directly.
- **Other users of `:pageno`.** `ptx-para-style.tex` and `ptxplus-marginalverses.tex` read the stored page number. Because note lines are no longer rewritten, they are unaffected.
- **Diglot.** Each language's columns form extra clusters. The grid's "keep 2 clusters" becomes "keep the expected number of columns", once we know what diglot pages look like.
- **Pages with no notes.** These still exist as slots, and their column positions come from the grid for their parity.
- **Overflow past the last page with notes.** The queue simply continues onto later pages. If it runs off the end of the document, TeX warns about the leftovers at the end.
- **Notes already shifted by an earlier run.** Ordering uses current `ymax`, and capacity uses only heights, so earlier shifts don't affect what gets pushed.

## Testing plan

The Python can be tested on synthetic `.marginnotes` files before any TeX exists. Test files stub `ptxprint.utils.universalopen` and `ptxprint.parlocs.readpts`, so the module loads without GTK.

| Test | Checks |
| --- | --- |
| Fixed point | For every case below, read → write → read → write gives the same bytes, and the second `outfile` returns false. |
| Double-shift regression | The four-note case that currently gives a `yoffset` of −120pt after three passes stays at −40pt. |
| Single column overflow | The excess goes to the next page, the block sits at the top with `yshift` 0, and natives lie below it. |
| Two columns | Col 0 overflow goes to col 1 on the same page, col 1 overflow to col 0 of the next page, and push lines carry the right side. |
| RTL | Same as two columns, with column numbering and sides mirrored. |
| Cascade | A block too big for its slot passes its tail on, ahead of that slot's own overflow. |
| Oversized note | A note taller than a slot stays put, logs an error, and doesn't stop later notes being pushed. |
| Fixed-side notes | `left`/`right` notes skip slots where their side faces the gutter. |
| Coming back | Deleting notes from an overfull slot makes the next pass write no push lines. |
| Column grid | Mirrored margins, a sidebar outlier, a single-column book, and a parity with only one column present. |

After the TeX side exists, the end-to-end check is a real project with dense notes. It should converge in the same number of runs as today plus at most one, with no notes outside the text block.

## TeX changes

The TeX side needs no inserts. It is one global box of held notes, a dedupe table, a macro for push lines, a held branch in `\pl@cemnote`, and one release macro called from the output routines. TeX never decides that a note overflows; it carries out the pushes Python wrote.

### Data

- **`\m@rginpending`:** a global vbox of every held note not yet drawn, in stacking order. Each entry is a `\penalty` carrying the note's serial number, followed by the lapped note box.
- **`mnheld@<serial>`:** the entry's key (`<ref>@<marker>`), target page and target column.
- **`mnlatest@<ref>@<marker>`:** the latest serial appended for that note, for deduplication.
- **One stack box per column,** filled at release and emptied when drawn.
- **A per-page flag** recording that this page's release has run, cleared at shipout.

### 1. Reading push lines

`\@marginnotepush{ref}{marker}{page}{col}{side}` is defined before `.marginnotes` is read. It stores `:pushpage`, `:pushcol` and `:pushside` under the note's existing `marginnote-<ref>@<marker>` prefix. Note lines are handled exactly as now, and `\wr@tet@mp` still writes the style's `\p@s`, which keeps Python's file a fixed point.

### 2. Building a pushed note

In `\d@marginnote`, a note with `:pushside` set takes that side instead of computing one from `:pageno` or `:colno`. Then the held branch of `\pl@cemnote`:

1. Builds the note lapped horizontally against the current `\hsize`, exactly as now, but without the `\vbox to 0pt` valign wrapper. The box keeps its natural height and depth, which is what Python's block height assumes.
2. Appends it to `\m@rginpending` after a `\penalty` holding the next serial number, then records `mnheld@<serial>` and updates `mnlatest@<ref>@<marker>`.
3. Puts only the anchor marker in the flow: `\writem@rginnote` between the usual cancelling kerns, with no box. The file therefore keeps recording the anchor's real page and position, and Python decides again on the next pass.

The append happens once per note. `\pl@cemnote` runs when a paragraph is broken into lines, and the galley's trial repaginations copy existing nodes without running macros again. Appending this early is safe because release depends only on the absolute target page. For inline notes, the append happens in `\pl@cemnote` itself; only the marker goes through `\m@rgincollect`.

### 3. Release

One macro, `\m@rginovfout`, is called from each of the six output sites: full and partial page output for each number of columns. It acts only at the first output for a page, whether that creates a partial box or outputs the whole page, and the released notes go out with the content being output at that point. Later outputs for the same page do nothing, so nothing is ever added to an existing partial box. A per-page flag, set when the notes are drawn and cleared at shipout, handles this.

1. Walk `\m@rginpending` from the bottom, taking each box with `\lastbox` and its serial with `\lastpenalty`.
2. Drop any entry whose serial is not the latest for its key. Duplicates can only come from a paragraph typeset twice, and either copy is the same note.
3. If the target page is ≤ `\pageno`, put the entry into its target column's stack; otherwise, put it into the new pending box. Prepending in both cases while walking bottom-up keeps the original order. The existing list-handling helpers in `ptx-output.tex` can do this.
4. Clear the `mnheld` record for each released entry.

A target page that has already passed, because the text reflowed, is released at the next shipout; the following run corrects it.

### 4. Drawing

In that first output, each column's stack is drawn at the top of that column's box, before its content: `\vbox to 0pt{\offinterlineskip\unvbox<stack>\vss}\nointerlineskip`. The notes were lapped against the column `\hsize`, so each lap lands on that column's outer edge. Single-column output has only col 0. The top of the column box must be the same y as Python's `top`, which comes from `getTextBlockSize`.

### 5. End of document

If `\m@rginpending` is not empty at the end, write a one-line warning. Overflow is rare, so this should hardly ever fire.

### Known limits

- Negative page numbers are not supported; margin notes aren't used there.
- Diglot is not supported yet; it will need its own release and drawing sites.
- A note anchored in single-column text and pushed onto a two-column page laps against the full text width.
- After a reflow, a note can be misplaced for one run until Python's next pass corrects it, as already happens with sides and shifts.
- A stack for col 1 has nowhere to go if a page's first output is single-column. Pages that receive overflow aren't expected to be mixed, so this is not handled.

### To check while implementing

- [ ] Find the six output sites (full and partial page output for each number of columns).
- [ ] Confirm the column box's top matches Python's `top` on single-column, two-column and mixed pages.
- [ ] Confirm the release walk preserves the order Python assumed: notes from earlier slots first, then document order.

