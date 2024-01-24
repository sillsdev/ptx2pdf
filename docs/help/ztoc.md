# ztoc

## Summary
Include a table of contents
## Examples
```
\ztoc|nt\*
```
## Description
This milestone imports table of contents data.
` \ztoc|keyword\*`  Where &lt;keyword&gt; can be replaced with:

*  main – primary, all-inclusive table of contents, in order of occurance.
*  pre – any book prior to scripture (FRT, INT)
*  ot – only Old Testament books are listed
*  heb - OT books sorted according to the Hebrew TaNaKh
*  dc – only Deutero Canonical books are listed
*  nt – only New Testament books are listed
*  post – books that occur after REV (GLO, BAK, TDX, NDX, XXA-G)
*  sorta – alphabetical (main) list sorted by \toc1
*  sortb – alphabetical (main) list sorted by \toc2
*  sortc – alphabetical (main) list sorted by \toc3

The data for `main` is produced directly by the previous XeTeX runs. Other collations / selections are performed by the PTXprint (python) code.

## Attributes
* `id` - which sort of TOC is desired.
