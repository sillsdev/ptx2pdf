# zcustomtopmark

## Summary
Starting mark on the page of a given custom type.
## Examples
```
\def\RHoddleft{\zcustomtopmark|article\*}
```
## Description
The *top mark* of the given page is the previous page's *bottom mark*. A *bottom mark* is the last **mark** on a given page (or if the page has no marks, the *bottom mark* is the *top mark *carried over from the previous one).

See *zcustommark* documentation for details. The value returned will almost certainly be useless except in header/footer/thumbtab processing.

## Attributes
* `type="something"` What sort of custom mark is wanted.
## See also
[zcustommark](zcustommark.md)
