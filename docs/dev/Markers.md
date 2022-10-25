# Markers

USFM markers are based on SFM markers but there is a clear syntax to them, and
further, within the paratext macros we have extra structure to allow stylesheets
to describe styles associated with markers.

The proposed marker syntax for use within a stylesheet is:

```
marker:     '\' markerexp ('+' (tag | ms))*
markerexp:  (constraints '|')? tag | ms
constraints: id | periph | categories
id:     'id:' catval ('|' (periph | categories))?
periph: 'periph:' catval ('|' categories)?
categories: category (':' category)*
category: 'cat:' catval
ms: (defaultval '|')? tag
tag: idchar+
catval: idchar+
defaultval: uniwdchar*
idchar: [a-zA-Z0-9_] | '-'
uniwdchar : [^\s"|+]
```

Notice that the description of a marker here is not the same as is used in USFM
text itself. A usfm marker is much simpler, although including milestones makes
it non trivial.

defaultval above is the content of the default argument of a ranged milestone, without any spaces.

In a marker sequence the order is (grandchild `+`) child `+` parent. The uppermost parent is a paragraph or note style,
i.e. there is no distinction in styling between those originating from a `\q1` and those  from a `\s1`

```
usfmarker: '\' '+'? tag '*'?
```

treat ms as character styles which get carried into the paragraph (and can also
be used on the paragraph)

`id:` tests for the id of the book (`MAT`, `XXS`, etc.).

`periph:` specifies which peripheral the marker occurs in.

x-credit:box=Dark|fig becomes Dark|x-credit

category values and milestone values have whitespace removed. Should category
values have whitespace? Instead treat them as an unordered space separated list.

How milestones interact with other markers is interesting. For example, consider
placing a \\strong-s\\* milestone at the start of a file. Then we could style a
\\wg within that using strong-s+wg. But for a \li, we would use li+strong-s.
The reason is that the strong-s is treated as a character style within a
paragraph (it propagates from paragraph to paragraph automatically). Thus we
style the paragraph using the character style within it, since all content is in
that 'character style', even if we then give that character style paragraph
properties. 



