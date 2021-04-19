

### Publishing information / Front/back cover / spine elements?
So far, only "inside pages" being set. Is cover / publishing information out of scope? All possible in XeTeX, but not 'easy'. E.g.a sparate run making use of color / graphicx  XeLaTeX packages may make more sence.
There is some barcode-creating code available (one package uses secial fonts, but some years ago DG found another piece of code that uses vrules).

Someone was working on producing covers. It would be good to get them involved and merge efforts.

-----------------

### Background colour  for section titles
### Background colour for normal paragraphs
coloured breakable/ normal paragraphs, could extend parlocs file to mark top left / bottom right of each column.

Consider lifting magic from conText? - No, context doesn't do breakable blocks, so we have that functionality.

----------------

### On-the-fly generation / inclusion of heading or page borders
 pgfornaments looks like it may be a good starting point. A bit too latex-focussed, 
but pgf itself is plaintex - friendly

-----------------

### PDF-X/1a
(if that's the right code).
Needs us to use no colour or cmyk.
rgb->cmyk is device-dependent, but the actual maths is not too complex. Option 1 would be for X1a, people must specify colour in cmyk 
Option 2 is auto-conversion using e.g. method described in latex xcolor.sty's documentation.
Option 3 is for ptxprint to convert.
Options 1 and 3 demand that tex macros know colours are specified in CMYK, 
Option 2 needs the conversion parameters to be specified in a tex-readable form.

Colours are specified in the following places:
a) FontColor (xRRGGBB or r+256*(g+256*b) -> \font...:color=RRGGBB 
  There is no way to specify CMYK in a \font definition, however the macros COULD be modified to use \special{color: cmyk ...}
b) Images (not addressable in macros)
c) Colour of tabs (r g b)
d) Background colour for side-bars



