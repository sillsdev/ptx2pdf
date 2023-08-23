# Abandonware: list of known bugs and unfinished code.

## \XformOrnamentstrue \holdXobjectstrue/false
Intention is to use xform objects (a pdf 'save this as a graphic' capability)
to shrink/simplify the PDF file.  Current problems are:

### Problem with use and definition sequencing.

 For some reason, despite the log file claiming that the use is 
always after definition, that is not the sequence either in the output box or the xdv file. 
Presumably this is something about deep nesting of code inside box definitions, or something similar.
This is true for held objects (not outputting them in the current stream, but putting them into a global box
used at shipout) or in-stream cases.

----------------


# List of unimplemented ideas

## Background colour  for section titles
## Background colour for normal paragraphs
coloured breakable/ normal paragraphs, could extend parlocs file to mark top left / bottom right of each column.

Current background to character styles cannot be simply applied to whole paragraphs, as anything other than an 
box or a space breaks the box-unrolling process.

The 'solution' would be that any code that does something clever, be that a
special, a mark, insert, etc. would have to be aware of the background-box,
ending it and restarting the backgrouding process.

