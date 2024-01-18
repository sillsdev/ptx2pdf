# zlabel
## Summary
Remember the page number for this place
## Examples

```
\ef + \cat people\cat* \fk Herod\ft `\zlabel|HerodANote\*Herod Antipas should not be confused with.... (see note for \zref|label="HerodGnote"\*) on page \zpage|label="HerodGnote"\*) \ef*

```
## Description
A milestone which produces no output but asks XeTeX to remember the page and verse-reference that this occurs on (writing it to a reference file). The label can then be used in future runs to insert the page (`\zpage`) or scripture reference (`\zref`) that the label occurrred on.
## Attributes
* id="uniqueID" 
## See also
[zref](zref.md)
[zpage](zpage.md)
