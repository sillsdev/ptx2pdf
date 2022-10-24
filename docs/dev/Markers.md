# Markers

USFM markers are based on SFM markers but there is a clear syntax to them, and
further, within the paratext macros we have extra structure to allow stylesheets
to describe styles associated with markers.

The proposed marker syntax for use within a stylesheet is:

```
marker:     '\' markerexp ('+' (tag | ms))*
markerexp:  (constraints '|')? tag | ms
constraints: categories | periph | id | creditbox 
categories: category (':' category)*
category: 'cat:' catval
ms: (defaultval '|')? tag
creditbox: 'x-credit:box=' catval
periph: 'periph:' catval ('|' categories)?
id:     'id:' catval ('|' (periph | categories))?
tag: idchar+
catval: idchar+
attkey: idchar+
attval: uniwdchar*
defaultval: uniwdchar*
idchar: [a-zA-Z0-9_] | '-'
uniwdchar : [^\s"|+]
```

Notice that the description of a marker here is not the same as is used in USFM
text itself. A usfm marker is much simpler, although including milestones makes
it non trivial.

In a marker sequence the order is child `+` parent.

```
usfmarker: '\' '+'? tag '*'?
```

treat ms as character styles which get carried into the paragraph (and can also
be used on the paragraph)

`id:` tests for the id of the book (`MAT`, `XXS`, etc.).

`periph:` specifies which peripheral the marker occurs in.

x-credit:box=Dark|fig becomes Dark|x-credit



