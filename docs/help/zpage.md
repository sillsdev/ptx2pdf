# zpage

## Summary
A milestone that inserts the page number of the specified `\zlabel`.
## Examples
```
\ef + \fk John the Baptist \ft  Jesus' cousin and herald, who gathered 
a subtantial following before pointing out Jesus.  For further discussion, see sidebar 
on page \zpage|JohnBaptist\*.\ef*
```

## Description
The `\zlabel` milestone remembers the page number and verse reference (from the last run) for a given piece of text. (which can be in e.g. a normal paragraph, a note,  a caption or a sidebar). This milestone inserts the page number into the text.
## Attributes
* `label="id"` The id of the label being referenced.
## See also
* [zref](zref.md) - the chapter-verse reference of a label
* [zlabel](zlabel.md) - label a piece of text.