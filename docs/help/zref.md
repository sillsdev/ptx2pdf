# zref
## Summary
A milestone that inserts the scripture-reference of the specified `\zlabel`.
## Examples
```
\ef + \fk John the Baptist \ft  Jesus' cousin and herald, who gathered 
a subtantial following before pointing out Jesus.  For further discussion, see note on \zref|JohnBaptist\*.\ef*
```

## Description
The `\zlabel` milestone remembers the page number and chapter-verse reference (from the last run) for a given piece of text. (which can be in e.g. a normal paragraph, a note,  a caption or a sidebar). This milestone inserts the scripture-verse reference into the text 

The `show` attribute instructs XeTeX what to actually show. E.g. if the reference  is known to be within the same book, then it may be decided there is no need to include the book name. Except that spaces are not preserved, unrecognised items in the string are repeated exactly. Recognised characters are:

* `b` - replaced by the book name
* `c` - replaced by the chapter number
* `v` - replaced by the verse number 
* `_` - replaced by a space.  (This is underscore character U+005F LOW LINE).

## Attributes
* `label="id"` The id of the label being referenced.
* `show="format"` The default value is `b_c:v`.
## See also
* [zpage](zpage.md) - the page number reference of a label
* [zlabel](zlabel.md) - label a piece of text.
