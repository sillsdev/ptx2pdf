# Markers

USFM markers are based on SFM markers but there is a clear syntax to them, and
further, within the paratext macros we have extra structure to allow stylesheets
to describe styles associated with markers.

The proposed marker syntax for use within a stylesheet is:

```
marker: '\' markerexp ('+' markerexp)*
markerexp: (constraints '|')? tag
constraints: (category (':' category)* ':')?
             (msattribute (':' msattribute)* ':')?
             (attribute (':' attribute)* ':')?
category: 'cat:' catval
msattribute: 'ms:' attkey '=' attval
attribute: 'att:' attkey
tag: idchar+
catval: idchar+
attkey: idchar+
attval: uniwdchar*
idchar: [a-zA-Z0-9_] | '-'
uniwdchar : [^\s"|+]
```

Notice that the description of a marker here is not the same as is used in USFM
text itself. A usfm marker is much simpler, although including milestones makes
it non trivial.

```
usfmarker: '\' '+'? tag '*'?
```


