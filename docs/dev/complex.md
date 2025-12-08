# Complex polyglot layouts
At present, the XeTeX code allows for vertical alignment of multiple columns. 
The column arrangement can (for polyglots) be defined as a series of letters (`L` - originally the Left column. `R` - originally the Right column, and then `A`, `B`, `C` etc.) The  column order is  set as a string, `LRA` for a default triglot, (becoming `ARL` on mirrored pages),  and if the `polyglot-simplepages` is loaded, the column order might be `LR,AB` for a quad-glot over two pages. This string is interpreted by the layout code to presentation determine order and where the different translations are on which pages. Currently, an entirely blank page is specified by `-`. Eventually, this could be extended so that `-` indicates  a page or section with note lines. 

There have been some requests for up/down diglots, where one translation 
is displayed below another.

Up/down diglots are a special case of multi-row polyglots which in turn are a
special case of two potential layouts: columns-of-columns polytglots or of rows-of- columns polyglots. 

Columns-of-columns polyglots would provide a 
side-by-side arrangement of several quasi-independent columns polyglots.
This does not allow for any columns to be full width,  and the questoin of vertical alignment between chunks in different columns becomes somewhat confused. 

As such, it is assumed that  the more desirable abstraction is that of the rows-of-columns polyglots, 
 such as the `LR/A`layout  (with `/` indicating a new row)  that below (showing a 
double-page spread, with mirroring).  L<sub>1</sub> etc are intended to show  vertical  alignment between the L and R chunks on a given row.

![ ](mirrored.svg  "Mirrored triglot (LR/A)")

Sub-dividing a column vertically (I.e. making the layout to be rows-of-columns-of-columns) is considered to be an unreasonable request at present.

However, taking the concept of abstraction a step further, rows-of-columns polyglots are, in-turn,  a special case of multipage rows-of-columns. 
Experience gained while developing the polyglot-simplepages layout was
 that the coding effort needed for an N-page layout compared to a 2-page 
 layout is trivial, as long as the design goals are thought-through well. Thus it 
 is deemed more appropriate to develop for the N-page layouts even if the 
 expected use-cases are rare.

Here is an overkill example of that (un-mirrored), showing the layout `LR/A,BC/DEF,G/H`:

![ ](complex.svg  "(LR/A,BC/DEF),G/H")

While it is expected that single-page layouts will be more popular than 2-page
layouts, and further, such a multi-page layout as shown will never be used in a
formally printed edition, there would still be use-cases for a translation consultant
or pastor who wanted to have, say, greek/hebrew, and several national and
international translations available as well as the vernacular text.

## The question of repeated columns
There are 2 potential varieties of multi-page,rows-of-columns layouts: 

**(a)** those in
which a particular text *only* occurs in a single column, *vs*  **(b)** those
where one text is split between several different 'windows' or 'displays'. This
second variety includes where a double-column layout is desired for one or more of the  texts, or,  equally, when it is desired to have an interlinear text across both pages of a 2 page layout, with other translations above/below it. 

Algorithms for both of these layouts will be considered below. One user has already asked if it would be possible to have one translation being in a 2 column layout at the top of the page, with another 2 translations below it.

That seems possible, but  there are some arrangements that, while seeming plausible, need to be  rapidly rejected out of hand.  It is simply not possible for XeTeX to produce a layout in which 
a single flow of text changes its column width without a *rigid* page layout,  or simulating one with multiple additional runs, as are required for  figures in cutouts.  If each page needed only a single re-run (probably unlikely) the number of job re-runs needed would scale as  O(2<sup>N</sup>) (N being the page count).

### "Accounting" issues.
The boxes and variables for each displayed column will be needed as at present, and  these will need a 'display identifier' to identify them.
Too much of the existing code assumes that the display identifier is a
**single upper case letter**. Deviating from this would add considerably to the  programming task.  The suggested approach is as follows:

* Use column identifiers as display identifiers for the first column,
encountered (Note this depends on LTR or RTL reading direction). Follow-on columns are 
mapped to otherwise unused upper case letters. E.g. second A (mnemonically A2)  which maps to e.g. U). The mnemonic mapping is
defined as the column definition is read, and to aid debugging, it is 
should be a permanent assignment. (e.g. no matter if other layouts are used, A2 is always  U, once defined that way.) 

* If a new page-layout description is given, there are 2 options:
 to discard the intermediate assignments or to leave them as-is. Debugging ease suggests leaving them as-is. The corollary of this is that  the code must disconnect the mapping if less columns are provided in the new mapping.
* A new page-layout description must trigger a page break and output of all pending material, or it might not be printed.


### Multiple chunks and alternative displays with repeated columns
If  a given column is repeated, then the question of responding to a new chunk
becomes very important.  Compare with a layout `LR/A`,  and the page contents
coming as 2 chunks (L<sub>1</sub>,L<sub>2</sub>, R<sub>1</sub>,R<sub>2</sub>, etc) then (without repeating
columns), the result would be expected to be 
with L<sub>2</sub> below L<sub>1</sub>, and so on, much like with the current diglot code - once
a chunk or chunk-fragment is defined, it is fixed, and either occurs on the
page or it does not (say because it is a section heading and the following
chunk won't fit).
  However, if L<sub>1</sub> has been split into 
multiple columns, (L and Z), then duplicating this behaviour will result in 
the reading order being entirely unintuitive:

![](2chunks.svg  "Chunk alignment for layout LR/A")

If the second chunks L<sub>2</sub> and A<sub>2</sub> were not present in the input (or did not
fit on the page, either due to space available or other factors, such as them
being headings), then the principle of unused space being at the bottom of the
page would say dividing L~1a~ and L~1b~ as in  the crossed-out middle
figure above was correct *in that first chunk*.  If they *are* present, then
L<sub>1</sub> must be merged and re-broken (combined notes) or the galley reprocessed (per-column footnotes).

### Summary for repeated columns
Thus it is necessary that if a column is repeated, then:

1. There is *no* column synchronisation for columns that appear more than 
once in a  page-set, except (possibly) the end-verse.
2. Consideration on positioning of footnotes may alter how the algorithm behaves. 
3.  The full galley (or processed galley, see efficiency possibilities **E<sub>1</sub>**, and **E<sub>2</sub>** below) 
for all split columns must be preserved between chunks, in case a following chunk is added. 
4. The processed column(s) / (page state) must be preserved between chunks and *still be
 available* after the new chunk is processed, in case the new chunk does not 
 fit. This is potentially more significant than the current state-reset on a chunk being pulled onto the next page.
5. **E<sub>3</sub>**  and  **E<sub>4</sub>** below suggest that *potential* solutions for all columns might need to be saved to reduce the page-rebuilding time.
6. Probably other things I've not thought of yet.
## Common elements for (all forms of) polyglot
There are certain  parts of the algorithms that the processing that stand unchanged, or only need some minor tweaking for the different algorithms.

### Common algorithm for pre-layout portions:

* Read a set of chunks, saving  any discardable spacing after the chunk
* Determine (based on penalty before end-of-chunk contents) if this chunk is **conditional**  or **unconditional**. (An unconditional chunk can be last item on the page, a *conditional* one must migrate to the next page if it is not followed by other content). Any conditional chunk appended to another conditional chunk will make a combined conditional chunk.

### Common algorithm for dealing with full page / rejected chunk 

* If the chunk set  fits:
    * If the page is full: 
        * output page, reset `avail`
     * else:
        * Save current page state as **unconditional** or **conditional**.
              *  If *unconditional*, simply apend box (es), save result and make conditional state void.
              *  If there was a previous conditional state, combine that with new conditional state, possibly using any saved spacing.
* Else, if it does not fit:
    * reject galley for this page.
    * Assuming there's unconditional matter left on the page from previous  cycles, output it. 
    * If the previous chunk was conditional, and was all that was on the page, output that old conditional matter, with a warning that the page should have been unprintable. 
    * Start the new page with any left-over conditional matter.

## Algorithm 1. No repeated columns in layout:
### Notes:

Use source  identifiers as display identifiers, as at present. 

   * per source: box: original galley
   * per source: last cut length, 
   * per source: box: Cut text (sub-galley) and remainder
   * per source: box: processed text
   * per row: box: page content, accepted content.

If the processed box is accepted, then at pageout, the remainder becomes the original galley until there is no more material to check in a given chunk.

### Layout Algorithm

* Until chunks empty:
  * For each page of output:
    * determine column lengths and hence calculate page size
    * if overshoot (without inserts) is long, determine good ratio to split all galleys by.
    * Process galleys
    * Until it fits or chunk rejected for page:
        * determine overshoot find longest column(s) per row. 
        * Trim line(s) from them and re-process.
        * (check end-verses if included are *similar*)
        * repeat
    * Respond appropriately to full  page / rejected chunk (see above)
  * determine spacing needed for alignment (and preserving baseline).
  * loop end
  * add to row-boxes or (if full) output page
    
## Algorithm 2. Repeated columns may exist 
### Notes
Use source  identifiers as display identifiers, as at present. 

   * per source: box: original galley and excess
   * per source: last cut length 
   * per output box: Cut text (sub-galley) and remainder
   * per output box: processed text
   * per row: box: page content, accepted content.

### Layout Algorithm

* For each repeated  column, merge old chunk contents with new.
* Until chunks are empty:
    * determine max column lengths for each row (maybe without inserts), and hence calculate size for combined page-set. Compare with current space.
    *  if overshoot is long, determine good ratio to initially split all galleys by.
    *  Until all pages in the page-set fit or galley rejected:
        * split multi-location columns in halves (or thirds, etc as appropriate)
        * build or calculate (revised) pages 
        * determine overshoot of longest column per row or page 
        * (if there are verses and this isn't the last display of a repeated column, check end-verses are *similar*)
        * adjust split-point or galley length appropriately, build list of chunks to reprocess.o(*decision depends on presence of notes and how they are being handled*)
        * repeat
    * Respond appropriately to full  page / rejected chunk (see below)
    * determine spacing needed for alignment (and preserving baseline).
    * loop end
 * repeat


### Processing of the intermediate mapping and Mirrored polyglots 
As it is by no means unheard of for there to be different translations to
display, say between OT and NT, it makes sense that 'pseudo' columns should 
not be chosen from the first unused letter at the start of the alphabet, but from the end. 

 If `L2->Z` and `L3->Y`, the intermediate staging can be set up with
`\def\f@llow@nL{Z} \def\f@llow@nZ{Y}` 
`\def\f@llowingZ{L} \def\f@llowingY{L}`

The existence or not of `\f@llow@nL` is then used to populate the 'original
galley' for Z and then in turn Y as the respective remainder box is emptied.  
When all is acceptable, \f@llowingZ is used to fill L.
\f@llow@nL (etc) can also be used to identify columns that must be re-worked in the case a column needs shortening.

For a mirrored diglot, the display-reversal code must use the  mapping
appropriately. i.e. a book bound for LTR readers (e.g. English-speaking
audience) might have
`\polyglotpages{LLA/R}`, with L2->Z
The forward and back display sequence is then: LZA/R and ALZ/R. For RTL readers,
the forward and back display sequence will be: ZLA/R and AZL/R.
kj
## Footnotes and repeated columns
It is worth considering what to do with footnotes. If the repeated
columns are on  separate pages, then it would make sense for the note to be 
(a) directly under its column, or (b) in with other notes at the bottom of
each respective page.

If, however, the repeated columns are on the same page, it might be argued
that a third option-exists: (c) to place notes at the end of the final column
on the page. This question needs more thought and can almost certainly be
resolved later. However, options (b) and (c) do raise the more efficient 
possibility (**E<sub>1</sub>**) of *not* always needing a new trial if adjusting the break-point
between columns, only when the processing changes one page to the next in the
page-set.

## Other efficiency gains possible
* **E<sub>2</sub>**  When a column contains no notes or other inserts, then trimming the column cannot add more notes. Thus vsplit is sufficient, and  there is no need to reprocess the content.
* **E<sub>3</sub>** Rather than successively trimming one line from the galley at a time before reprocessing, a binary search pattern could be used. This would, however, require some modification of the loop, changing from 'first fill that fits' to a more complex method of scoring.
* **E<sub>4</sub>** Cache old results rather than discard them. Rationale: with the potential for multiple solutions inherent in a page with multiple texts, the code is performing, in effect, a multivariable optimisation, in which returning to a previously tested state for one or more columns might be the best solution. Eg. After run *N*, the page is too long by 1 line, with the  longer columns being `L` and `A`. `L` is shortened by 1 line and reprocessed removing a long footnote, producing a large gap. A better solution is to shorten `A`, return `L` to what it was at run *N*.   This need for back-tracking also strongly implies that the algorithm given above is overly simplistic.

## Scoring 
* **E<sub>5</sub>**  *If notes are not per-column, or as an initial phase*, then a table of vsplit length -> final verse and layout acceptability  could be generated for each column. This can be used generate a preference-score for different arrangements to try actually expanding. E.g.: in a given chunk of text, (one version including a section heading),  for the layout `LL/RR`, having  573.99 pt of space, we might consider:

| Col/Cut-length|Max length|Unbalance|Final_verse|Note length
|-------|----------|------|---|---|
L/286.9958pt|283.6716pt|23.6621pt|13||
L/272.9958pt|266.37476pt|21.01367pt|12
L/258.9958pt|251.72633pt|6.36525pt|11
L/244.9958pt|237.07791pt|21.01367pt|10
R/286.9958pt|274.65793pt|29.29684pt|14
R/272.9958pt|260.0095pt|0.0pt|14
R/258.9958pt|245.36108pt|0.0pt|14
R/244.9958pt|230.71266pt|0.0pt|12

If whitespace has a *cost* of 1/pt  on any side, and 20/pt of unbalance within the chunk, and out-of-sync verses have a cost of 50, then we get the following scores:

|Pattern|v-R|v-L|Whitespace|total cost|Comment|
|------------|--------------|---------|-|-|-|
L/286.9958pt,R/244.9958pt|12|13|2.20468pt|1204|Fullest page, but unbalanced (see L/286.99  above)
L/272.9958pt,R/258.9958pt|12|14|4.8531pt|1093
L/272.9958pt,R/244.9958pt|12|12|19.50153pt|1060| Matching verses, but unbalanced column
L/258.9958pt,R/272.9958pt|11|14|4.8531pt|380
L/258.9958pt,R/258.9958pt|11|14|19.50153pt|388
L/258.9958pt,R/244.9958pt|11|12|34.14995pt|355 | Only 1 verse different
L/244.9958pt,R/286.9958pt|10|14|4.8531pt|2597
L/244.9958pt,R/272.9958pt|10|14|19.50153pt|1140
L/244.9958pt,R/258.9958pt|10|14|34.14995pt|1147
L/244.9958pt,R/244.9958pt|10|12|48.79837pt|1115

Clearly, the different scoring weights will decide which option is preferred by the algorithm.
Further testing will show if one or other of the parameters would be better
squared. (A difference of 1 verse, or 1 line of whitespace doesn't matter much,
but avoiding the text becoming 5 verses out of sync, or a solution leaving quarter of a
page of whitespace are worth quite a lot of imbalance on 1 column if there are many.


# Whitespace removal *vs* verse tracking
In 1xN layout, then verse tracking is easily possible, as the column heights
can be adjusted. In any other layout there will be whitespace when the 
column lengths disagree. For a layout `L/RA`, there are several processing options. 
Users might well have a preference, and so the scoring parameters should be accessible. Perhaps some 'standard values' should be made available.

Starting on a page with avail left, `ht(L)+max(ht(R),ht(A)) > avail`.

*    **No verse info**:  Calculate `factor= avail / ( ht(L) + max(ht(R),ht(A)) )`  initial guess: `factor * ht(L)`  for `L`, etc. If inserts reduce `avail`, shrink one or more row heights  by something and repeat. 
*    **Verses, strict parallel**: as before, but the galley contents are tweaked until botmarks agree +/- 1 verse before each run.
*    **Verses, loose parallel**: If `ht(R)` and `ht(A)` don't agree very well, allow their botmarks to get out of sync by, say, 3 verses.
*    **Verses, min whitespace**:  if `ht(R)` and `ht(A)` don't agree, then try to make it that they do, pushing all R/A imbalance to the  end of the chunk.


# Considerations for splitting L/RR,L/AA 
Any time content is  moved from L1 to L2 that might move a note or other
insert. A full split is more efficient if we know that there are notes/inserts.
If all the notes/inserts are in the first half, then a full split on L1 is
appropriate and a minimal split appropriate on L2. Therefore, we want at least
a partial list of line-no/insert measurements.

# Summary of necessary routines
* Process layout string and reversal string [DONE]  [TESTED]
     *  add/remove follow-on connections and create relevant boxes / dims
     * self-check routine
* Identify which inputs end up in repeated columns, especially cross-page.
* Something to determine possible split heights [DONE]
* Determine total galley lengths
* Split into sub-galleys, with chaining through follow-ons
* Analyse how inserts affect layout 
* Determine initial split lengths **COMPLEX**
 

