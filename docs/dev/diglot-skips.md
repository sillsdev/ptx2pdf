# Skips and kerns in diglot

Diglot (and polyglot) makes very considerable use of vsplit and trial-runs. It also has two baselineskips to contend with.

## Gridding principles in diglot.
As a design intent, the diglot code has (barring bugs and very early trials)
aimed to follow the following principles:

1a) An external program is responsible for deciding what pieces of text should
be aligned. The diglot code does not assume this role itself. It does not care
if alignment is done on matching chapters, matching verses, matching paragraph
breaks where verse numbers are in agreement (or other alignment patterns where
the verses getting totally out of synchronisation).

1b) Unless section titles are in separate chunks, there will be no alignmnent
of any following text. 

2a) Chunk-starts align the baselines of both (all) columns.

2b) Page-tops align the the baselines of both (all) columns.

3) Each uninterrupted chunk of text should be regularly spaced, according to it's own grid.

4) 2 'touching' paragraphs across a chunk boundary should maintain that grid.
This may mean that if the left column is shorter than the right one in one
chunk, the right hand grid will be preserved, if the next chunk has a longer
left column, the grid will be preserved for that chunk-transition. Principle
(2) prevents both chunks maintaining grid unless both sides have the same baseline.

5) Each chunk (each column in each chunk) is separated from the next by a special 
kind of page break that forces it into the alignment part of diglot. Attempts are made to 
preserve 'no-break' rules *within* the layout part, but stretch, etc. is not preserved.

## Topskip splittopskip and chunks
Each time TeX retrieves what it considers a 'page' of content, it attempts to
add space to make a distance of  `\topskip` between the baseline of the text and the top of
the column. If the text is higher than the baseline, then this space is zero.
It has recently been realised that TeX does not ever add negative topskip. This
causes gridding-loss if topskip is too small. 

Each time TeX splits a piece of vertical matter, it uses `\splittopskip`
instead of `\topskip`.  The result is approximately the same. Space added by splittopskip 
can never be negative.

However, eTeX added and extension to add `\savingvdiscards` control along with 
`\splitdiscards` and `\pagediscards`, which allow the  (otherwise lost)
baselineskip to be recovered.

Solution:

Thus: at a split, `\splittopskip` can be set to `0pt` and the spacing needed to
preserve the original grid can be recovered. 
If baseline recovery is required, the relevant baselineskip should be subtracted.

At a 'page' (chunk top), there is no guaranteed way to preserve grid unless
topskip is set sufficiently high. This should then be *subtracted* at each recovery of 
box255.

A new dimension `\truetopskip` has been added, defaulting to \baselineskip.
This should be *added* at the top of the page. At the top of a normal page, 
`\baselineskip` should be added.


