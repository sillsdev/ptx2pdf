
# Application of styling in complex situations

## Drop-cap styling
If `Marker c`'s justification is set to 'right', then the right margin (or,
since rightmargin can't be set negative in the UI, leftmargin if rightmargin is left at
0) specifies where the right-hand edge of the chapter number sits. (relative to
the left margin).

For other justification settings, a non-zero leftmargin moves the left
side of the chapter number relative to the margin.

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

```tex
\q1 The Angels sang <<\qt-s|Angels\*Glory\qt-e\*>>
```
and the `\q1` line of this this (as a paragraph style):

```tex
\qt-s|Angel\*
\q1 Glory to God in the Highest
\q2 And peace on Earth to mankind
\qt-e\*
```

* `\Marker nd+Angel|qt-s+p`
Special styling for when an angel says the name of the LORD, in a standard `\p`-type  paragraph, as  above.
 

* `\Marker cat:special|p` Styling for a special type of paragraph:
`\p\cat special\cat*`


* `\Marker cat:special|Jim|qt-s+p` Extra special styling for 'THIS BIT' in the example below:
`\p\cat special\cat* Jim said <<\qt-s|Jim\*THIS BIT\qt-e\*>>`

### Styling based on book and/or periph
There are times when a certain book (e.g. the glossary) or a certain periph
division (e.g. the imprimatur) should be styled differently. These prefix the
style stack in an analogous manner to categories. The codes for these are
`id:GEN|` and `periph:title|` respectively.
If the USFM is:
```tex
\id FRT
\periph Promotional Page|promo
\ip \cat Main\cat*  The \bk Holy Bible\bk*  is the Word of God, a valuable part
of the life of any Christian's life...
```
Then not leaving anything unspecified, the book name `Holy Bible` is formatted:
```tex
\Marker id:FRT|periph:promo|cat:Main|bk+ip
```

### Style stack boundaries
As paragraph styling does not affect a footnote, the stylestack for inside a footnote ends at the `\f` or `\x`
Similarly, the style-stack in force outside a sidebar does not affect anything inside.

## Double underlining
If underlining is recommended against, double-unlerlineing is doubly so. But it has been asked for, so it is now
implemented. To specify it, pass the *exact* value of 2 to the `\Underline` 'boolean'.
```tex
\Marker wj
\Underline 2
```

Note that while single-underlining of spaces works quite nicely, for double-underlining of spaces the underline must be made from multiple 
line-fragments. These may look ugly on PDF viewers, but hopefully print OK.

###Underlining parameters (TeX file):
```tex
\def\DoubleUnderlineSpaceQuantum{0.05ex} %  how long are the chunks that get added together to underline a variable width space
\def\DoubleUnderlineSep{0.05em} % How separate are the lines
\def\UnderlineLower{0.1em} % How much lower is the (top of the) underline from the decender?
\def\UnderlineThickness{0.05em} % Line thickness
\UnderlineSpacetrue % or false 
```

## Underlining with a character or string
In very odd circumstances, it might be necessary to 'underline' with a
character, or perhaps strike through a piece of text with Xes, etc. to highlight errors.

This may cause gaps between words and spaces due to the difference in length of an integral number of underlining bits and the width of a word or space, and it may be preferable to apply the setting `\UnderlineSpacefalse` either globally or via a hook.

```tex
\Marker ul
\Endmarker ul*
\Underline 
\UnderChar ∿
\StyleType Character

\Marker ul2
\Endmarker ul2*
\Underline 
\UnderChar "∿-"
\StyleType Character

\Marker ul3
\Endmarker ul3*
\Underline 
\UnderChar [\hbox to 2ex{\hfill x\hfill}]
\StyleType Character

\Marker underline+ul
\FontSize 3
\FontName DejaVu Sans
\SpaceBeside -.125
\Color xff0000
%Strike through text with e.g.: \Raise 1ex
```

In the above example, the marker ul 'underlines' with the character U+223F Sine
Wave, and ul2 'underlines' with the string of U+223F and a normal hyphen/minus character. ul3 underlines with the results of a piece of TeX code.
Rather than the literal character, it could have been defined using the XeTeX hexadecimal notation  `^^^^223F` but multi-token constructs such as `\char123` are not accepted in the unquoted form, although they may be used in the quoted or bracketed form.
The relevant font for the characters are set by the underline+ul complex style (or underline+ul2, etc, respectively), which sets the font and colour parameters.
The distance specified by `\UnderlineLower` (see section above) applies. However if, for example, the intention is
to put Xes through the 'underlined' word, the `\Raise` parameter can be used (on the underline+... styling) to accomplish this. In choosing the value here, it should be remembered that the starting point is with the bottom of the word and the top of the underline character, .

In the (ul2) `"`quoted`"` form, a box containing the underlining string is repeated as many times as will fit, with gaps between the copies of the string, so that the end elements reach the end of the word being underlined.

In the (ul3) `[`bracketed`]` form,  an alternative fill strategy is used, which leaves gaps at the end of the underlining if there's not a perfect match, but does not insert gaps between the underlining characters.
Either quoted or bracketed forms may include TeX code.

The (ul) unquoted form is only applicable to single characters, and the code has been written to perform a special handling for such characters: the font is queried about the bounds of the inked portion of the glyph (difference between the ink and the normal space around the letter), and any reported horizontal spacing is removed.  Assuming the font information is  correct, this means that ink of the underlining characters will touch one another. As with the bracketed form, 'spare' space is inserted at either end of the underlined word.

If some overlap between underline characters is required (or additional separation), such as to make the 'sine wave' join up, this can be accomplished with `\SpaceBeside`  parameter, which adds / removes the specified amount of space on *both* sides of the glyph.
Unlike normal use (where scaling is to the indentation unit, the base unit for this factor is the width of the character).

The `\SpaceBeside` parameter is also applicable to the bracketed form, where the base unit is the natural width of the string or code.

The quoted form currently ignores `\SpaceBeside`, as the relative positioning
of the characters should be expected to change from word to word anyway.

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
(because there is no ```\Marker Pilate|qt-s``` entry in the stylesheet overriding the value(s) of the default, and there is just the single milestone in force). If this fall-back to the unattributed style is not desired the command:
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

# Style stack precedence (search sequence).
Consider:

```tex
\p Jesus said, <<\wj It is written, <You shall not put the \+nd Lord\+nd*...
```
The innermost `Lord` has a style stack of `nd+wj+p`. When styling is considered there is a well-defined *order* in which items will be checked for.
The simple order would be `nd`, `wj`, `p`. But `wj` might have a more specific variant `wj+p` which should be checked for before the `wj`. Thus, 
for this example the search-order is for styles defined for: `nd+wj+p`, `nd+wj`, `nd`, `wj+p`, `wj`, `p`. For most parameters, this sequence is read left-to-right, and the first definition encountered  is the one that applies.  E.g. if the stylesheet defines a colour for `nd+wj` that is the colour that will apply, unless there's something defined for `nd+wj+p`. A colour defined for `wj+p` will (in this situation) only apply outside the `nd+wj+p`.  The situation for font sizes and features is somewhat more complex, but the sequence is still obeyed. 


At present, there is no option to *skip* a level of the stack. (i.e. `nd+p` is
not an option for styling this text).

If for some reason this portion of text were being quoted in a side bar:

```tex
\esb \cat Temptation\cat*
\p Jesus said, <<\wj It is written, <You shall not put the \+nd Lord\+nd*...
\esbe
```
Then as each style-stack entry could be be preceded by the category information, the full  style stack emtry would be:
`cat:Temptation|nd+wj+p`, and the order of precedence,  (the search-list for `\Marker` entries)  would be:
with category: `cat:Temptation|nd+wj+p`, `cat:Temptation|nd+wj`, `cat:Temptation|nd`, `cat:Temptation|wj+p`, `cat:Temptation|wj`, `cat:Temptation|p`, `nd+wj+p`, `nd+wj`, `nd`, `wj+p`, `wj`, `p`



### `\StackComplexity`
A complex style-stack can always be specified in **full**. However, otherwise
there is a limit placed on how complex shortened look-ups are allowed to be.
This limit is set by:
```tex
\def\StackComplexity{3}
```

This results in a search-list that is:
 *  Full stack
 *  Top stack item with [`\StackComplexity` ... 0] extra items following
 *  Next stack item with [`\StackComplexity` ... 0] extra items following
 *  etc. 

E.g. Consider this example, (in which the `\ts-s` milestone  has been enhanced with an additional attribute zwho, put at the start of the list (making it the styling-related attribute, see below):

```tex
\ts-s|zwho="Alice"\*
...
\p Jesus said, <<\qt-s|Jesus\* It is written, \+bd <You shall not put the \+nd Lord\+nd*...
```

As milestones always 'float' above the paragraph mark, then for this example, the fully specified style stack for `Lord` will be `nd+bd+Jesus|qt-s+Alice|ts-s+p`
If `\StackComplexity` were **2**  then  the search list would be:

 * Full list: `nd+bd+Jesus|qt-s+Alice|ts-s+p`
 * starting nd with [2,1,0] extra:  `Jesus|qt-s+nd+bd`,`nd+bd`, `nd`,
 * starting bd with [2,1,0] extra:  `bd+Jesus|qt-s+Alice|ts-s`, `bd+Jesus|qt-s`, `bd`
 * starting `Jesus|qt-s` with [2,1,0] extra: `Jesus|qt-s+Alice|ts-s+p`, `Jesus|qt-s+Alice|ts-s`,`Jesus|qt-s`
 * starting `Alice|ts-s` with [2,1,0] extra:  `Alice|ts-s+p`, `Alice|ts`
 * starting `p` with [2,1,0] extra: p
 
With the default of **3**, then the fragment of the search list for `nd` would be `nd+bd+Jesus|qt-s+Alice|ts-s`,`nd+bd+Jesus|qt-s`, `nd+bd`, `nd`.

The above is all correct if the toggle `\AttrMilestoneMatchesUnattrfalse` has 
been set. The *default* settings, however, allow the styling of the (top-most) 
attributed milestone by an unattributed style (see example below), so in that 
situation, the final list of styles checked in the above is:

`nd+bd+Jesus|qt-s+Alice|ts-s+p`, `nd+bd+Jesus|qt-s+Alice|ts-s`, `nd+bd+qt-s+Alice|ts-s`, `nd+bd+Jesus|qt-s`, `nd+bd+qt-s`, `nd+bd`, `nd+bd`, `nd`, `bd+Jesus|qt-s+Alice|ts-s+p`, `bd+qt-s+Alice|ts-s+p`, `bd+Jesus|qt-s+Alice|ts-s`, `bd+qt-s+Alice|ts-s`, `bd+Jesus|qt-s`, `bd+qt-s`, `bd`, `Jesus|qt-s+Alice|ts-s+p`, `Jesus|qt-s+Alice|ts-s+p`, `Jesus|qt-s+Alice|ts-s`, `Jesus|qt-s+Alice|ts-s`, `Jesus|qt-s`, `Alice|ts-s+p`, `Alice|ts-s+p`, `Alice|ts-s`, `p`

Once the above list has been determined, it is rapidly reduced again, by comparing to styles that have actually figured in a stylesheet. That reduced list is then cached for future use.


## Font features  and possibly unexpected behaviour for FontScale
For most parameters, processing the list stops at the first encountered value. For `\ztexFontFeatures`, `Bold` and `Italic` (and any others
 other values affected by `\Regular`), processing of the search-list continues until a `\Regular` is encountered, allowing  italic and bold to be specified by 
different markers but still combine.

When the `\FontScale` parameter is interpreted, then (just like each 'simple' marker style multiplies the value obtained so far), similarly each matching complex style **will also** multiply the value so-far, there is no *replacement* of values elsewhere in the search list.
Thus if the stylesheet contains this:
```
\Marker v+wj
\FontScale 0.8

\Marker v 
\FontScale 0.8

\Marker p
\FontSize 12
```

Then the base-size (before the reduction for superscript is applied) for a marker `\v` will be `0.8*12 = 9.6``FontSizeUnits`, but the stylesheet has specified that for a `\v` inside text marked as being the words of Jesus, the base size will be `0.8*0.8*12 = 7.68` `FontSizeUnits`.

Font features can be specified in two manners, old style, where the exact fontfeatures are set:
```
\Marker v
\ztexFontFeatures :embolden=.1
```
or *new* style, where the features are added to (`+[features]`) or subtracted from  (-[features]) the currently in-force 
feature set. (Or set without referral to earlier settings: `=[features]`)
```
\Marker nd
\ztexFontFeatures +[smcp,extend=1.1] 
```
Using the new style description, the final feature list is built up from features from the paragraph style or outer character style, with 
additions and subtractions.  Multiple changes to the feature list can be specified on the same line. The different actions should be separated by a space, and features within the brackets by commas. E.g.:
```
\Marker zitalic-sc-s
\EndMarker zitalic-sc-e
\StyleType Milestone
\ztexFontFeatures +[smcp,slant=.2] -[embolden]
```
Will add the small-caps and slant features and remove any embolden feature
currently in force, but as no `=[...]` is given, no change will be made to `extend` or other features.

### Special rules for extend
Normally, if a feature such as `slant` is included in a paragraph style and
then specified in the `+[features]` of a character style, then the character
style's `slant` setting will take priority. One exception to this is `extend`,
where it is assumed that the correct behaviour is to 
maintain the visual relationship between characters outside and inside the
character style, and thus the final result is the *multiplication* of the
`extend` parameters. If previous `extend` has been removed (`-[extend] +[extend=1.2]` or
`=[extend=1.2]`) then there is no pre-existing value to multiply with.

If a pre-press paragraph balancing / fitting rule is in place (`\p^95`), then
this applies (multiplies) all styles in the paragraph, so that it can be of use no matter
what styles have been applied or where.
If it is desired to **not** rescale the text for some reason, then the old method of 
setting the `extend` value in the stylesheet to shrink/expand a custom paragraph
style can be used. (e.g. `p_95` with has a stylesheet-defined `extend` feature). 
The parameter give this way *can* be overridden by character style.

Character styles can now also take the `\ft^102` format, which is of particular
use in footnotes. Note that the footnote style *itself* cannot accept the
notation, as the potential for confusion seems much too probable. The extend
parameter applies strictly to the character style, and is not continued by
other character styles on a given line, except where nesting is used.


