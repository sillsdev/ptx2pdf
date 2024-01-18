# zmakeinsert

## Summary
Post-processing instruction: flag the current periph as a section to be pulled from the normal print-run separately and manually re-inserted. 
## Examples
```
\periph Map section|id="maps"
\zmakeinsert|colourmaps\*
```

## Description
It is not unusual to have certain pages being 'plates', also known in as 'inserts', that are printed with a different technology to the normal pages of the print run. E.g. full-colour pages when the main print run is printed black and white have been a feature of some books for well over 50 years.
Printing such pages in the black and white page-run would lead to wasted paper or complex and error-prone selection of pages.

Although TeX will only create a single PDF file, this milestone sets flags in the PDF output that the post-processing stages of PTXprint will use to exclude these pages of the PDF from the main file into separate files (named according to the id given), so that they can be sent to a different printing process.

Note that this milestone only has any effect in a periphery section, and while a given periphery may includes another, then it is equally ignored in such included peripheries.

## Attributes
* `id="fileSubName"`
* `nopagecount="T"` Disable the page counts
## See also
