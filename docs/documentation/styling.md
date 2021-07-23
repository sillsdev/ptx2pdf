
# Application of styling in complex situations
Consider this example piece of USFM:
```
\s The Angel of the \nd Lord\nd* talks to Joshua
\p
\v 1 The Angel of the \nd Lord\nd* said, <<\qt-s|Angel\*Thus says the \nd Lord\nd* ...
```

Styling of items such as `\p` and ```\nd``` are relatively simple matters, and are controlled easily via the 
ptxprint user interface. However, there are several more complex cases, some of which may be caused by 
practical compromises. For example if the alphabet has unusual characters, there may not (yet) be a 
font that includes all letters, exists in bold and has the small-caps feature. 
It may thus be necessary to select an alternative font for `\nd` in section
headings. This document attempts to address such issues.

## Styling of ranged milestones
Milestones such as `\qt-s \* ... \qt-e \*` define a range of text that cuts
across normal boundaries of paragraphs or character styles. Attributes of milestones
are not normally used for *content*, but can be used to define a styling.
```
\Marker Angel|qt-s
\Color x00FF00

\Marker qt-s
\Color x00007f
```

With the above custom stylesheet then: 
* The USFM code ```\qt-s|Angel\* ... \qt-e\*``` will mark all text bright green;
* the USFM code ```\qt-s\* ... \qt-e\*``` will mark all text dark blue (matching the unattributed definition);
* the USFM code ```\qt-s|Pilate\* ... \qt-e\*``` will normally mark all text dark blue
(because there is no ```\Marker Pilate|qt-s``` entry in the stylesheet overriding the value(s) of the default). If this fall-back to the unattributed style is not desired the command:
```
\AttrMilestoneMatchesUnattrfalse
```
may be given in the `ptxprint-mods.tex` file. Note that this affects all milestones.

## Styling of character styles with attributes
Attributes of character styles may contain content (e.g. a gloss for `\rb`, captions for images), or
non-content information such as a hyperlink (e.g. ```\w disciple|link-href="#disciple"\w*```). It might seem desirable to style `\w` differently 
depending on whether there is a link associated with it or not, but *by the time that is known* the styling has already been 
defined and applied. Thus, to accomplish this end, it makes more sense to
define a custom character style and make use `PrintDraftChanges.txt` file to apply that in  the relevant situations.

Content-defining attributes   (which  don't follow the example of image captions and use the style associated with the marker) are styled using 
the custom style-sheet such as this example for the `gloss` attribute of the `\rb` USFM marker:
```
\Marker gloss|rb
\FontSize ....
```
### Control of link-underlining
The macros recognise two types of links (document-internal links, termed GoTo
links, and external web addresses, termed URL links) which may be marked in
different manners. The current default values are:
```
\def\GOTOLinkBorderstyle{/S/U/W 1} % Underline
\def\GOTOLinkBorderCol{.9 .5 .5}% pale red
\def\URLLinkBorderstyle{/S/U/W 1} % Underline
\def\URLLinkBorderCol{.5 .5 .5}% Gry
```
If  `URLLinkBorderCol` is set to empty, then no attempt to set the colour will be made, and the PDF reader's default colour (black, probably) will be used. To have no underline, make the width 0: `/W 0`.
  
The PDF reference, third edition describes the following options:

|    Code  | Description |
| -------- | ------------ |
|`/S/S`    |Solid - a solid line around the link|
|`/S/D`    |Dashed - a dashed line around the link|
|`/S/U`    |Underline |
|`/D [3 2]`|The dashed pattern (three point dashes, two point gaps)|
|`/W 1`    | Width of the line (1 point).|
|`/S/B`    |Beveled or embossed rectangle that appears to be above the surface.|
|`/S/I`    |Inset or engraved rectangle that appears to be below the surface.|

Note that the last two of these do not seem very widely supported, and that 
combinations of the above (e.g. dashed underline) are not possible.

## A brief introduction to the style stack. 
The XeTeX code has a concept of a 'style stack', a pile of  styles that may are active at any moment in time.

As processing moves through the text above, the stack takes the following values, `+` can be read as "added to"
1. `p`
2. `v + p`
3. `p`
4. `nd + p`
5. `p`
6. `Angel|qt-s + p`
7. `nd + Angel|qt-s + p`
8. `Angel|qt-s + p`

Occaisionally it is useful to specify a particular styling for not just the very top stack entry, but 
the top two (in the given example, an `\nd` following the `\qt-s`), or even the entire style stack.
This is possible using the method below.


###


