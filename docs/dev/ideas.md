
### Flip based on odd/even pages.

* Sometimes a typesetter decides pictures are better facing the spine. Currently 
flipping an image needs an outside tool.

* LaTeX's graphics package allows reflection of an image left/right and up/down.

Other than fiddling about with position, the  code seems to boil down to:
```
\def\Gscale@start{\special{pdf: /S \Gscale@x\space \Gscale@y\space << }}
\def\Gscale@end{\special{pdf: /S \space >> }}
```

If (post 1.0) we combined that with (yet another) \fig parameter: mirror="odd" / mirror="even" / mirror="always", it could go from "that's a complete pain" for a typesetter to implement to "no big deal". 
