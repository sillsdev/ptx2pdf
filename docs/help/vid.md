# vid
## Summary
Tell the code where the next bit of text is from.
## Examples
`\vid|GEN 5:6\*
`\vid|ref="GEN 5:6" h="Genesis"\*

## Description
In certain circumstances, mainly in modules, XeTeX may have no idea what book
or chapter a given paragraph is from. That makes it impossible for it to produce a
correct header or determine which triggers, images, etc. should be included
when it meets e.g. `\v 10` This milestone is provided to supply that
information.
 
## Attributes
* `ref` The book reference in "GEN 4:2" format. As a concession to human habits, `.` is accepted in ptxprint as a chapter-verse separator as well as `:`, while the standard may be more strict on this matter.
* `h` The name of the book for running headers, as normally found in `\h` lines.
