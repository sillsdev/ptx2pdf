# zvar
## Summary
Use a variable.
## Examples
```
\mt1 \zvar|booktitle\*
\zISBNbarcode|isbn="zvar::isbn"\*
```
## Description
PTXprint allows 'variables' to be set in the finishing tab, which are in turn
provided to XeTeX via the control file (e.g. with lines like `\defzvar{isbn}{0123-456-789}`).
The value can either be expanded into text (via the `\zvar` milestone) or into
the attribute of another milestone (by setting the value of an attribute to the variable's name prefixed by `zvar::`).
Variable names may not contain spaces, but values may.
## See also
* [Conditional code](conditional.md)
