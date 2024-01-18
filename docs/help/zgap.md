# zgap
## Summary
Milestone to insert a vertical gap
## Examples
```
\zgap|5em* % 5 font-heights in the current font.
\zgap|dimension="4\baselineskip"\* % Exactly 4 lines
\zgap|dimension="45pt plus 10pt minus 20pt"\* % A stretchable and shrinkable space, for covers, etc.
\zgap|-5pt\* % negative space.
```
## Description
This milestone inserts a gap. It includes no provision for keeping the gridding or anything else clever like that. The gap cannot break across pages, and will not be removed if it occurs at the top of the page.

## Attributes
 * `dimension` -  any measurement TeX measurement.
## See also

