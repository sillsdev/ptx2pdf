

### Publishing information / Front/back cover / spine elements?
So far, only "inside pages" being set. Is cover / publishing information out of scope? All possible in XeTeX, but not 'easy'. E.g.a sparate run making use of color / graphicx  XeLaTeX packages may make more sence.
There is some barcode-creating code available (one package uses secial fonts, but some years ago DG found another piece of code that uses vrules).

Someone was working on producing covers. It would be good to get them involved and merge efforts.

### Missing pics:

Longer term, we should check that the number of images the code read is the same as the number of printed images (which it can check  by re-reading the notepages file).

------------------

### \vp (published verse number)

Ideally if present, this should be used instead of the contents of \v.
Processing that without complex look-ahead is hard. 

Storing the verse number to use later would require some kind of trigger for use and there is no 'everychar' to serve as a trigger.

It may be easier to remove items from the list and rebuild it. After a verse number, the hlist might be (\showlists output:)

 \hbox(9.0044+1.85887)x4.91309, shifted -4.17241
 .\font<v-12.0> 2
 \kern 2.0
 \mark{rūtu:1:2}
 \penalty 10000
 \glue 0.0
 
A decorated verse should also be within a box. 

\unglue \unpenalty  gets us to the mark. If the mark were positioned earlier, we could then \unkern\setbox0=\lastbox and effectively remove the verse number.
The \mark cannot be simply positioned earlier, as there's a \llap\bgroup ...}  {... egroup code to parse the verse number.
The solution to this would be replace the \ll@p\bgroup with something that
makes a box with the group, which is then (optionally) set in a llap but with the marker already positioned. Not a hard change, but need to make sure the mark and the 
box don't get separated. \vp contents would need to be decorated, etc.

------------------

### \w word|glossary entry\w* and other |attributes.

USFM3.0 has added the | symbol to several character styles. The most useful one is \w,  (the lemma [default] attribute of a \w ... \w* could trigger the
inclusion of glossary entries, for example). But in any case, their presence should be parsed and not cause processing errors.


----------------
### Milestones
The syntax: \foo ...\* is taken in usfm to indicate a milestone, a non-printable indication of some kind of context type. 

Script marked with \qt-s |who="Jesus"\* .... \qt-e\* might be used to mark up scripts applying different colouration for alternate speakers, for instance.
One method of using these might be to apply hooks based on milestones.

-----------------

### Categories
\esb \cat People \cat*  
\esb*
  Might be added to  sidebars, etc, and is expected to alter formatting of any/all elements in the study matter. These in some way give an attribute (see above) to 
blocks of extended study material.
\cat may  appear within footnotes too. There should be some (pseudo stylesheet?) method of applying styling to elements in a given category.


