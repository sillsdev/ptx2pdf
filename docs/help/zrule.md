# zrule

## Summary
Draw a horizontal line (plain, double or ornamental), for example as  part of a sidebar, or below a section heading.

## Examples
```tex
\zrule\* % Simple rule, properties from stylesheet
\zrule|0.7\* % A simple rule with an unusual width
\zrule|cat="undersection"\* % Specific category of rule from stylesheet
\zrule|width="0.3" align="l" thick="5pt" raise="6pt"\* % Left-aligned thick rule
\zrule|style="double" thick="10pt" width="0.5"\*

```
## Description
A milestone to draw a rule. In general terms, any border-related style setting applies to zrules, including style, colour(s) and thickness.  (`BorderPatternTop` defines the pattern used by ornamental rules, but if `standardborders.sty` is included, then a number of ornamental rule styles are supplied).

### Rule styles and categories
 zrules for specific uses can have separate categories, which are styled with `cat:type|zrule`. If there is no `cat=` attribute, the currently active category will be applied, i.e. rules in a sidebar of category `history` will be considered to be of that category if no other is supplied.

The upper rule in the sample below simply applies a style of `double`. The lower rule makes use of the additional controls available in the stylesheet, to define the line and fill colours for the double rule, and the line thickness.

![](imgs/20240123-112136.png)

###
## Attributes
* `cat="whatever"`  - use the rule parameters set up for `cat:whatever|zrule`
* `width="0.3"` - use the specified fraction of the column width. If not supplied, then the rule width is determined by `\zrule`'s left and right margin.
* `thick="3pt"` - control the thickness of the rule
* `raise="0.5pt"` - The rule should be `6pt` above the baseline.
* `style` - valid values are `plain`, `double` and (if *ornaments* plugin is used), `ornaments`. Other styles may also become available.
* `align="c"` - horizontal alignment. Values are `l` (left), `r` (right) and `c` (centred). Left and right may be reversed in right-to-left scripts.

## See also
[Ornament catalogue](../documentation/OrnamentsCatalogue.pdf)

