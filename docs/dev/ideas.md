
### Flip based on odd/even pages.

* Sometimes a typesetter decides pictures are better facing the spine. Currently 
flipping an image needs an outside tool.

* LaTeX's graphics package allows reflection of an image left/right and up/down.

Other than fiddling about with position, the  code seems to boil down to:
```
\def\Gscale@start{\special{pdf: /S \Gscale@x\space \Gscale@y\space << }}
\def\Gscale@end{\special{pdf: /S \space >> }}
```

If (post 1.0) we combined that with (yet another) \fig parameter: x-mirror="odd" / mirror="even" / mirror="always", it could go from "that's a complete pain" for a typesetter to implement to "no big deal". 


### Save image pages

+ for above to work properly, it is necessary for the final page number to be known. (Rather than just the pave number at the time the piclist entry is triggered
+ for automated / assisted copyright statements the page number is also needed.


### Publishing information / Front/back cover / spine elements?
So far, only "inside pages" being set. Is cover / publishing information out of scope? All possible in XeTeX, but not 'easy'. E.g.a sparate run making use of color / graphicx  XeLaTeX packages may make more sence.
There is some barcode-creating code available (one package uses secial fonts, but DG found anoter piece of code that uses vrules).
