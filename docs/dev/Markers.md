# Markers

USFM markers are based on SFM markers but there is a clear syntax to them, and
further, within the paratext macros we have extra structure to allow stylesheets
to describe styles associated with markers.

The proposed marker syntax for use within a stylesheet is:

```
marker:     '\' markerexp ('+' markerexp)*
markerexp:  (constraints '|')? tag
constraints: categories | msattrs | attrs | creditbox | periph | id
categories: category (':' category)* ('|' (msattrs | attrs))?
msattrs:    msattribute (':' msattribute)* ('|' attrs)?
attrs:      attribute (':' attribute)*
category: 'cat:' catval
msattribute: 'ms:' attkey ('=' attval)?
attribute: 'att:' attkey
creditbox: 'x-credit:box=' catval
periph: 'periph:' catval ('|' (categories | msattrs | attrs))?
id:     'id:' catval ('|' (periph | categories | msattrs | attrs))?
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

In a marker sequence the order is child `+` parent.

```
usfmarker: '\' '+'? tag '*'?
```

Consider in a diglot context `cat:inl|ms:qt|p` this might expand to try all of
cat:inl|ms:qt|pR,cat:inl|ms:qt|p,cat:inl|pR,cat:inl|p,ms:qt|pR,ms:qt|p,pR,p

`id:` tests for the id of the book (`MAT`, `XXS`, etc.).

`periph:` specifies which peripheral the marker occurs in.


