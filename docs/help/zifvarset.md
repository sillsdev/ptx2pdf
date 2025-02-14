# zifvarset

## Summary
Test if the zvar is set and set conditional markers (ztruetext,zfalsetext) appropriately.

## Examples
```
\zifvarset|var="isbn" emptyok="F"\*
\ztruetext
 \esb \cat ISBNbox\cat* \pc \zISBNbarcode|var="isbn" height="medium"\* \esbe
 \zgap|10pt\*
\ztruetext*
```
## Description
Decide if `\ztruetext` or `\zfalsetext` is ignored or not.
The above example, (from the default contents of back-covers), includes a
barcode in a sidebar if the zvar `isbn` has been set. Otherwise, that
(potential) content is entirely ignored.

## Attributes
* `var="isbn"` - variable to test
* `emptyok="T"` - Does a set but empty variable count as true? If this parameter is given but not `"F"`, then setting the zvar to an empty value counts as it being set. If it is set to "F", then an empty value is considered undefined.

## See also
* Documentation on [Conditional text](conditional.md)
* [ztruetext](ztruetext.md)
* [zfalsetext](zfalsetext.md)
* [zvar](zvar.md)

