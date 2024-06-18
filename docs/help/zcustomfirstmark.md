# zcustomfirstmark

## Summary
First mark on the page of a given custom type.
## Examples
```
\def\RHoddleft{\zcustomfirstmark|article\*}
```
## Description
The first explicit *mark* of the given page (or if the page has no marks, the previous page's *bottom mark* is carried over).

See *zcustommark* documentation for details. The value returned will almost certainly be useless except in header/footer/thumbtab processing.

## Attributes
* `type="something"` What sort of custom mark is wanted.
## See also
[zcustommark](zcustommark.md)
