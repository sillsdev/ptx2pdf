# zlistentry
Make an entry for a list-of-things
## Summary
A list of things (e.g. tables, figures, prayers) is much like a table of contents. It can included into the publication 
just like a table of contents, by specifying the list-type to [`\ztoc`](ztoc.md).
The list of figures is populated automatically, using the caption.

## Example
```
\zlistentry|type="PRAY" title="Paul's prayer for the church at Colossae"\*
```

## New entries
The macro `\DefineListOf{type}{comment}{style}` can be used to associate a new type of list. At present, the 2nd parameter is not used except as a comment.
The `style` parameter serves like `\cat style\cat*` for the generated table. 
Using \zlistentry without ever using `\DefineListOf` will not crash, but the table will be treated as a style `toc` (table of contents).

## Predefined entries
```
\DefineListOf{FIG}{List of Figures}{lot}
\DefineListOf{TAB}{List of Tables}{lot}
\DefineListOf{PRAY}{List of Prayers}{lot}
```

## Attributes
* `type` -- the type of list.
* `title` -- the entry


