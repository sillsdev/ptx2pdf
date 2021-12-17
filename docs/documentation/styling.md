
# Application of styling in complex situations

## Stack-based styling
Consider this example piece of USFM:
```tex
\s The Angel of the \nd Lord\nd* talks to Joshua
\p
\v 1 The Angel of the \nd Lord\nd* said, <<\qt-s|Angel\*Thus says the \nd Lord\nd* ...
```

Styling of items such as `\p` and ```\nd``` are relatively simple matters, and are controlled easily via the 
ptxprint user interface. However, there are several more complex cases, some of
which may be made necessary by practical compromises. For example if the
alphabet has unusual characters, there may not (yet) be a font that includes
all letters, exists in bold *and* has the small-caps feature.  It may thus be
necessary to select an alternative font for `\nd` in section headings. This
document attempts to address such issues. The reader is assumed to be familiar
with the sylesheeet format. For most of the examples only the 1st line of the
stylesheet is given.


### A brief introduction to the style stack. 
The XeTeX code has a concept of a 'style stack', a pile of  styles that are active at any moment in time. Consider this fragment:
```tex
\p
\v 1 The Angel of the \nd Lord\nd* said, <<\qt-s|Angel\*Thus says the \nd Lord\nd* ...
```

As processing moves through the text above, the stack takes the following values, `+` can be read as "added to"

|  |  Style stack | Text |
| --- | --- |--- | 
| 1. | `p`                   |
| 2. |`v + p`                | [1]
| 3 . | `p`                   | [The Angel of the]
| 4. | `nd + p`               | [Lord]
| 5. | `p`                    | [said]
| 6. | ```Angel\|qt-s + p```  |  [Thus says the]    
| 7. | ```nd + Angel\|qt-s + p``` | [Lord]
|  8. | ```Angel\|qt-s + p``` |

Normally, the styling is additive, that is to say if the style stack is `v + p`
then the styling from `\v` is added to (or supersedes)  the styling for `\p`,
and so if, for instance `\v` specifies that verse numbers will be green, then
they will also be green in a red-letter 'words of Jesus' section.
 
Occasionally it is useful to specify a particular styling for not just the
very top stack entry, but the top two or three entries (in the given sample, for example, an `\nd` inside 
the `\qt-s`), or even the entire style stack.  This is possible by specifying the style stack 
(with no spaces) in the style sheet, as in the examples below.

### Style-stack based styling examples

```tex
\Marker nd+s1
\FontName Charis SIL
\SmallCaps
\Bold
```
This selects `Charis SIL` for character style `\nd` when in an `\s1`  paragraph.


* `\Marker Angels|qt-s+q1` 
Specify the styling for poetic (`\q1`) angel voices. If the paragraph starts
inside the milestone's range, then both paragraph styling and character styling can
be specified. Otherwise, just the character styling will be affected.
I.e. this can affect both this (as a character style):
```
\q1 The Angels sang <<\qt-s|Angels\*Glory\qt-e\*>>
```
and the `\q1` line of this this (as a paragraph style):
```tex
\qt-s|Angel\*
\q1 Glory to God in the Highest
\q2 And peace on Earth to mankind
\qt-e\*
```

* `\Marker nd+Angel|qt-s+p `
Special styling for when an angel says the name of the LORD, in a standard `\p`-type  paragraph.

* `\Marker cat:special|p` Styling for a special type of paragraph:
`\p\cat special\cat* `


* `\Marker cat:special|Jim|qt-s+p` Extra special styling for 'THIS BIT' in the example below:
```\p\cat special\cat* Jim said <<\qt-s|Jim\*THIS BIT\qt-e\*>>```

### Style stack boundaries
As paragraph styling does not affect a footnote, the stylestack for inside a footnote ends at the `\f` or `\x`
Similarly, the style-stack in force outside a sidebar does not affect anything inside.

### Style stack precedence (itteration sequence).
Consider:
```tex
\p Jesus said, <<\wj It is written, <You shall not put the \+nd Lord\+nd*...
```
The innermost `Lord` has a style stack of `nd+wj+p`. When styling is considered there is a well-defined *order* in which items will be checked for.
As a  this example it is `nd+wj+p`, `nd+wj`, `nd`, `wj+p`, `wj`, `p`. For most parameters, this sequence is read left-to-right, and the first definition encountered  is the one that applies. E.g. if the stylesheet defines a colour for `nd+wj` that is the colour that will apply, unless there's something defined for `nd+wj+p`. A colour defined for `wj+p` will (in this case) only apply outside the `nd+wj+p`.  The situation for font sizes and features is somewhat more complex, but the sequence is still obeyed.

**Much though it might be wanted** at present there is no option to *skip* a level of the stack. (i.e. `nd+p` is not an option for styling this text).

If for some reason this portion of text were being quoted in a side bar
```tex
\esb \cat Temptation\cat*
\p Jesus said, <<\wj It is written, <You shall not put the \+nd Lord\+nd*...
\esbe
```
Then as each style-stack entry could be be preceeded by the category information, the full  style stack emtry would be:
`cat:Temptation|nd+wj+p`, and the order of precedence,  (the search-list for `\Marker` entries)  would be:
with category: `cat:Temptation|nd+wj+p`, `cat:Temptation|nd+wj`, `cat:Temptation|nd`, `cat:Temptation|wj+p`, `cat:Temptation|wj`, `cat:Temptation|p`, `nd+wj+p`, `nd+wj`, `nd`, `wj+p`, `wj`, `p`



### `\StackComplexity`
A complex style-stack can always be specified in **full**. However, otherwise there is a limit placed on how complex the look-up is allowed to be. This limit is set by `
``tex
\def\StackComplexity{3}
```
This results in a search-list that is:
*) Full stack
*) Top stack item with [`\StactComplexity`-1 ... 0] extra items following
*) Next stack item with [`\StactComplexity`-1 ... 0] extra items following
*) etc. 

E.g. Consider this example, (in which the `\ts-s` milestone  has been enhanced with an additional attribute zwho, put at the start of the list (making it the styling-related attribute, see below):

```tex
\ts-s|zwho="Alice"\*
...
\p Jesus said, <<\qt-s|Jesus\* It is written, \+bd <You shall not put the \+nd Lord\+nd*...
```

As milestones always 'float' above the paragraph mark, then for this example, the full style stack for `Lord` will be `nd+bd+Jesus|qt-s+Alice|ts-s+p`
If `\StackComplexity` were **2**  then  the search list would be:

 * Full list: `nd+bd+Jesus|qt-s+Alice|ts-s+p`
 * starting nd with [1,0] extra:  `nd+bd`, `nd`,
 * starting bd with [1,0] extra:  `bd+Jesus|qt-s`, `bd`
 * starting `Jesus|qt-s` with [1,0] extra: `Jesus|qt-s+Alice|ts`,`Jesus|qt-s`
 * starting `Alice|ts-s` woth [1,0] extra:  `Alice|ts-s+p`, `Alice|ts`
 * starting `p` with [1,0] extra: p
 
With the default of **3**, then the fragment of the search list for `nd` would be `nd+bd+Jesus|qt-s`, `nd+bd`, `nd`


## Styling of ranged milestones with and without attributes
Milestones such as `\qt-s \* ... \qt-e \*` define a range of text that cuts
across normal boundaries of paragraphs or character styles. Attributes of milestones
are not normally used for *content*, but the first item in the `\Attributes` list can be used to define styling.

```tex
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
```tex
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
```tex
\Marker gloss|rb
\FontSize ....
```
### Control of link-underlining
The macros recognise two types of links (document-internal links, termed GoTo
links, and external web addresses, termed URL links) which may be marked in
different manners. The current default values are:
```tex
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
