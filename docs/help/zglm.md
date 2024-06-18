# zglm

## Summary
Font selection / character styling for glossary-entry markup.
## Description
Depending on the selected options, PTXprint will typeset `\w temple\w* ` with some kind of marks surrounding it, such as e.g. ⌊temple⌋. The actual marks used, are, however, wrapped in `\+zglm  ... \+zglm*` to remove font-related issues, or allow them to be typeset in a lighter grey, for instance.

