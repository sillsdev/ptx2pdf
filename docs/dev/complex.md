# Complex polyglot layouts
Up/down diglots are a special case of multi-row diglot, which in turn are a special case of  rows-of-columns polyglots, such as that below. (here showing a double-page spread, with mirroring):

![ ](mirrored.svg  "Mirrored triglot (LR/A)")

In turn, rows-of-columns polyglots are, in-turn, a special case of multipage,rows-of-columns. Here is an overkill example of that (unmirrored):

![ ](complex.svg  "(LR/A,BC/DEF),G/H")

While it is expected that single-page layouts will be more popular than 2-page layouts, and  such a multi-page layout as shown will never be used in a formally printed edition, there would be use-cases for a translation consultant or pastor who wanted to have, say, greek/hebrew, and several national and international translations available as well as the vernacular text. 

Experience gained while developing the polyglot-simplepages layout was that the coding effort needed for an N-page layout compared to a 2-page layout  is trivial, as long as the design goals are thought-through well. Thus it is deemed more appropriate to develop for the N-page layouts even if the expected use cases are rare.

## The question of repeated columns
There are 2 potential varieties of multi-page,rows-of-columns layouts: those in
which a particular transation *only* occurs in a single column, vs those where one text is split betwen several different 'windows'. This includes double-column layout is desired for one translation, or, equally, when it is desired to spread an interlinear across muliple pages.

Note that there are some arrangements deemed to be unreasonable. Without a *rigid* page layout it is simply not possible for TeX to produce a layout in which a single flow of text changes its column width.

 Algorithms for both of these are given below.

The same  boxes and variables for each displayed cell will be needed. These will need a 'display identifier' to identify them.

Much of the existing code assumes that the display identifier is a** single upper case letter**. Deviating from this would add considerably to the programming task.

### Algorithm 1. No repeated columns in layout:
#### Notes:

Use source  identifiers as display identifiers. 

   * per source: box: original galley
   * per source: last cut length, 
   * per source: box: Cut text (sub-galley) and remainder
   * per source: box: processed text
   * per row: box: page content, accepted content.

If the processed box is accepted, then at pageout, the remainder becomes the original galley until there is no more material to check in a given chunk.

#### Algorithm
* Read chunks
* Until chunks empty:
  * For each page of output:
    * determine column lengths and hence calculate page size
    * if overshoot (without inserts) is long, determine good ratio to split all galleys by.
    * Process galleys
    * Until it fits:
      * determine overshoot find longest column(s) per row. 
      * Trim line(s) from them and re-process.
      * (check end-verses if included are *similar*)
      * repeat
    * add to row-boxes or (if full) output page
    
### Algorithm 2. Repeated columns may exist 

Use column identifiers as display identifiers for the first column
encountered (Note this depends on reading direction). Follow-on columns are
mapped to otherwise unused upper case letters. E.g. second A (mnemnoically A2)  which maps to e.g. U). The mnemnonic mapping is
defined as the column definition is read, and to aid debugging, it is 
should be a permanent assignment. (e.g. no matter if other layouts are used, A2 is always  U, once defined that way.) 

If a new page-layout description is given, there are 2 options:
 to discard the
intermediate assignments or to leave them as-is. Debugging ease suggests
leaving them as-is. The corolory of this is that  the code must disconnect the mapping if less columns are provided in the new mapping.

* Read chunks
  * determine max column lengths for each row (maybe without inserts), and hence calculate size for combined page-set. Compare with current space.
  * if overshoot is long, determine good ratio to initially split all galleys by.
  * Until all pages in the page-set fit:
    * split multi-location columns in halves (or thirds, etc as appropriate)
    * build or calculate (revised) pages
    * determine overshoot of longest column per row or page
    * trim line(s) from end of galley.
    * (check end-verses if included are *similar*)
    * repeat
  * output page 

### Processing of the intermediate mapping and Mirrored diglot 
As it is by no means unheard of for there to be different translations to
display, say between OT and NT, it makes sense that 'pseudo' columns should not
be chosen from the first unused letter at the start of the alphabet, but from
the end.  

 If L2->Z and L3->Y, the intermediate staging can be set up with
\def\f@llow@nL{Z} \def\f@llow@nZ{Y} 
\def\f@llowingZ{L} \def\f@llowingY{L}

The existance or not of \f@llow@nL is then used to populate the 'original
galley' for Z and then in turn Y as the respective remainder box is emptied.  
When all is acceptable, \f@llowingZ is used to fill L.
\f@llow@nL (etc) can also be used to identify columns that must be re-worked in the case a column needs shortening.

For a mirrored diglot, the display-reversal code must use the  mapping
appropriately. i.e. a book bound for LTR readers (e.g. English-speaking
audience) might have
`\polyglotcolumns{LLA/R}`, with L2->Z
The forward and back display sequence is then: LZA/R and ALZ/R. For RTL readers,
the forward and back display sequence will be: ZLA/R and AZL/R.

### Multiple chunks and alternative displays with repeated columns
If  `\f@llow@nL` is defined for a given column, then the question of chunking  becomes very important.  Compare with a layout `LR/A`,  and the page contents coming as 2 chunks (L~1~,L~2~, R~1~,R~2~, etc) then (without repeating columns), the result would be expected to be 
with L~2~ below L~1~, and so on.  However, if L~1~ has been split into multiple columns, (L  and Z), then the reading order will be entirely unintuitive. 

![](2chunks.svg  "Chunk alignment for layout LR/A")



# Whitespace removal or verse tracking
In 1xN layout, then verse tracking is easily possible, as the column heights can be adjusted. In any other layout there will be whitespace when the column lengths disagree. There are several processing options:

Starting on a page with avail left, htL+max(ht(L),ht(R)) > avail.

*    No verses:  Calc factor= avail / ( ht(L) + max(ht(R),ht(A)) )  initial guess: factor * ht(L) to L, etc. If inserts reduce avail, shrink one or both by something and repeat.
*    Verses, strict parallel: as before, but the galley contents are tweaked until botmarks agree +/- 1 verse before each run.
*    Verses, loose parallel: If ht(R) and ht(A) don't agree very well, allow their botmarks to get out of sync by, say, 3 verses.
*    Verses, min whitespace:  if ht(R) and ht(A) don't agree, then try to make it that they do, pushing all R/A imbalance to the  end of the chunk.

In this, I'm assuming that the notes for L go on the bottom of the L column, or all the notes are merged.
l