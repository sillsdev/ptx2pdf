# marginversemarker
## Summary
What to use to mark verse transitions when marginal verses are in use.
## Examples (ptxprint-mods.tex)
```
\def\marginversemarker{*} % Mark verse transitions with a *
\def\marginversemarker{} % Do not mark verse transitions
```
## Description
Sometimes, when using marginal verses, it is still desired to mark the verse transition.
This macro specifies what content to use to mark the transition. Styling (including font selection, if 
so desired) is via the style `zmvm`. 

## Related Controls
By default, a verse at the start of a paragraph makes no mark. To change that use:
```
\noparstartmvmfalse % Don't suppress margin verse marks at the start of a paragraph
```

Even though verses immediately after a chapter number might be suppressed, the margin verse marker can still occur:

```
\keepmarginversemarkertrue % Don't suppress margin verse marks when verse numbers would be suppressed.
```

## See also
[Style for margin verse markers -- zmvm](zmvm.md)

