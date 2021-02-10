
The old implementation of diglots contains too much special-casing and 
semi-duplicated code. It was also inconsistent in its handling of left and right 
texts, and not sufficuently robust in handling either.

It is hoped that code robustness and consistency will be aided by a new implementation, which 
is also free from semi-duplicated code (using meta-variables rather than hard-coded values).
It is also hoped that a more clearly thought-through algorithm will be of significant 
benefit.

The flow of boxes and penalties is shown in dig2.dia / diglot2.pdf (xetlatex diglot2.tex)

New algorithm (aka diglot2):
 Asumptions: 
 1. Because of figures/notes, etc. any text-chunk may affect other text-chunks on the page.
 2. It is legitimate to re-process any text-chunk that is still in the 'working set'.
 3. If there is space, it is legitimate for an image to lower all text-chunks en-masse. If there is no space, it is 
 legitimate  and prefereable to force a page break in the column that seeks to lower all text chunks en-masse.
 4. It is not permitted to have over-full sections of text.
 5. In vertically aligned multiglots, chunks must start at the same point, but an image or footnote may occupy space 
 in one column when text does so in another column. 
 6. Combinations of penalties and footnotes/inserts may force a previously acceptable set of chunks to become invalid.
 7. Heading chunks are never splittable, and unsplittable chunks are the only sort of chunks that can end with a penalty10000
 8. Heading chunks can have footnotes, but these are rare.

Assumption 2 means that unprocessed (galley) text should be remembered for each
currently-open chunk of text on the page. [DONE]

Assumption 6 means that previously processed and 'closed' chunks may need to be
shifted to the following page. [DONE]

Assumption 7 means that in this case, there is no need (if there are never 
headings with notes) to reprocess the chunk.
However, with the moving of a previously set box (or boxes), the consequence is
that the state of notes should be remembered so that the page can be rolled
back to 'without the final chunk'. [DONE, partially] 

Assumption 8 then probably implies that (unprocessed) galleys should be
remembered not just for each 'currently-open' chunk, but also for 'recently
closed' chunks also.  It is assumed that rolling back of images and other
inserts is NOT required.  [TO DO]



