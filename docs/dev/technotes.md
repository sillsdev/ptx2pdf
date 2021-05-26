
## Technical Documents

### Reset footnote callers each page.
 This can be used in diglot, but it is unsupported. Results may vary. The
reason is that when diglot turns the note instruction into letters it has only
a vague idea if a particular chunk of text will go on page X or if it will be
shifted to page X+1. If for some reason a chunk of text that might have fitted
is pushed onto the next page, they will not be reset correctly. There is probably a 
fix needed to the code.

### Why we don't split footnotes.
By default, TeX is able to split footnotes. In some circumstances this might be
desireable, for instance when there are very long footnotes on a page. However,
there is a fundamental feature of TeX that means that we cannot discard a galley (as is 
done by the page balancer, diglot column-arranger, etc) without that saving the 'cut-off' 
portion of the foot-note onto the next page. There is no way to purge that page
from within the output routines, (nor, that I know of, to purge it on exit from the 
output routine) so splitting a footnote results in duplication of content.

Example of what happens if note breaking is allowed. Imagine the footnote is like this:
```
1. line one
2. line two.
3. line three
``` 

TeX breaks the note before line 3. Line 3 is added to the next line. The galley is rejected 
and the space for text body is shrunk. It's slightly better, but TeX still
breaks the note at line 3, so the next page now has 2 copies of line 3.  The
next cycle, TeX breaks the note before line 2. Lines 2 and three are added at
the top of the new page. Before any text is added to the next page, it now looks like:
```
\insert{2. line two.
3. line three}
\insert{3. line three}
\insert{3. line three}
```
This break is also rejected, so the the whole note is rejected. The next page will 
now contain the caller and the footnote will appear like this:

```
2. line two.
3. line three
3. line three
3. line three
1. line one
2. line two.
3. line three
```


## Plugins
The idea of plugins is to reduce loading time and memory requirements for those that don't need rarely used features.
It is envisaged that plugins will be for output-related changes, not input-related changes.
I.e. a modification that alters code to add fancy borders would be a candidate for being a plugins, 
but code that implements part of the the USFM standard should not be, to reduce unexpected problems for users.

Possibly this principle means that ptx-triggers, ptx-pic-list and ptx-adj-list should be plugins.
However, these are now a core part of ptxprint and so won't be considered for plugins. Marginal verses, 
however, might be a good candidate.

Extensions are requested by defining `\pluginlist` to a comma-separated list. e.g. 
```
\def\pluginlist{polyglot-simplepages,borders-doubleruled}
```

ptx-plugins.tex includes a list of plugins for processing `\def\pluginlist{all}` 
Correct sequencing should be done in that macro.

However, if a plugin requires one or more other plugins, this should be indicated like this:
```
\plugins@needed{polyglot-simplepages,borders-font}
```

The only-written plugin so far, `polyglot-simplepages` includes this re-insertion prevention wrapper. Other plugins should also 
include similar code. 
```
\plugin@startif{polyglot-simplepages}
.  .  .
\plugin@endif
```

This expands to:
```
\ifcsname polyglot-simplepages@plugin@lo@ded\endcsname\else
\let\polyglot-simplepages@plugin@lo@ded\empty
. . .
\fi
```

In both cases, the filename (without the .tex) should exactly match the plugin name, otherwise the automatic inclusion by `\plugins@needed` will fail.

