# Categories

Categories add an additional dimension to styling. While there are not may *contexts* in which they may be officially applied (USFM 3.0 allows only `\ef` and `\esb`), they allow alternative styles for almost all styling elements.
[http://ubs-icap.org/chm/usfm/3.0/notes_study/categories.html]

In the XeTeX macros, categories can apply to most markers. Normally they will be enclosed by another marker. Some
markers form an explict enclosure (such as footnotes, cross-references and
side-bars), others form an implicit enclosure, (such as tables), where the end marker 
is implicitly provided by the following paragraph style.  Paragraph styles (and section headers) 
can now also have categories applied to them. In this case starting the category creates 
an implicit enclosure, which is ended by the next paragraph style.

## Applying a category to a paragraph
```
\p \cat 98\cat* This paragraph could be set using an alternative font  configuration  that 
reduces the font width to 0.98 of the normal size. Note that there is nothing magic about the 
numbers, the numbers are just a label.
```
The style sheet might then read:
```
\Marker cat:98|p
\FontName GentiumPlus:extend=0.98
```
Alternatively, if the desire is to apply category 98 to *all* paragraph styles, the stylesheet can specify this:
```
\Marker cat:98|*
\FontName GentiumPlus:extend=0.98
```

Parameters for paragraph styles are looked up in the following order:
`cat:98|p`, `cat:98:*`, `p`, with the first match winning. 

### `*` and character styles
Style sheet entries like the above with `\Marker cat:98|*` do not apply to
character styles. This is to avoid unexpected problems.
If the `*` applied to all character styles as well as all paragraph styles, 
then when formatting, say `\nd`, it  would look for parameters in this order:
`cat:98|nd`, `cat:98:*`, `nd`.
And this would mean that any special font selection for that style would be 
lost in such paragraphs. If it were necessary to apply the font expansion to 
this character class,  then an approach such as this would be necessary:

```
\Marker nd
\FontName Zapf Chancery

\Marker cat:98|nd
\FontName Zapf Chancery:extend=0.98
```


## Applying a category to a block of  headings and sidebars
A heading block (`\s..`) in the main body text may *seem* to form an
implicit enclosure, but as it is made of individual paragraphs there is no way
to access this. Either every paragraph (`\mt`, `\mr1`, `\s1`, `\r`) 
must have a specified `\cat` or an inline sidebar with `\Position h` (see below
and (SideBars.md)[SideBars.md]) can be constructed to enclose the text.

```
\esb \cat PossibleAddition\cat*
\s The Woman Caught in Adultery
\sr John 8:1-11
\esb*
```


### Categorised paragraphs vs paragraphs in sidebars
The key similarities and differences between a sidebar and a paragraph with a category are as follows:

1. A paragraph style with a category can inherit or change any and all parameters from the 'main' style.
2. All paragraphs within a sidebar have the category of the sidebar
3. A sidebar has special formatting for the sidebar itself, specifying things
   like background colour, the position on the page, (similarly to figures) and other parameters.
4. Most sidebar options prevent the bar from splitting across page boundaries or column breaks.

## Applying a category to footnotes
```
\f + \cat History\cat* \fr 1:1 \fq Babylon \ft though initially not as important as other places, it eventually 
became one of the main powers of the Ancient Near East.\f*
```
Note that the `\cat` must occur after the caller. If placed later (e.g. after
the footnote reference), then expect behaviour to be undefined.

## Applying a category to tables
```
\tr\cat Special\cat*
\tr \th1 Day \th2 Tribe \th3 Leader
\tr \tcr1 1st \tc2 Judah \tc3 Nahshon son of Amminadab
\tr \tcr1 2nd \tc2 Issachar \tc3 Nethanel son of Zuar
\tr \tcr1 3rd \tc2 Zebulun \tc3 Eliab son of Helon
\tr \tcr1 4th \tc2 Reuben \tc3 Elizur son of Shedeur
\tr \tcr1 5th \tc2 Simeon \tc3 Shelumiel son of Zurishaddai
\p
```
The category should be specified immediately after the first `\tr` marker,  and applies to all rows and cells.
I.e. in the above example, 
```
\Marker cat:Special|tcr1
\FontName Andika
\Color x00ff00
```
Will display the 1st cell in green (if colour output is enabled),  and using the `Andika` literacy font. (Discuss with your 
scripture use consultant and local typesetting experts whether this is at all advisable).

## Styling mechanisms

There are three mechanisms available for category-specific styling. The user may pick and choose as seems most appropriate.


### \stylesheet
TeX file:
```
\stylesheet{filename.sty}
```

Styling may either be done with on a specific marker or multiple markers, e.g. this sets the styling for the  marker ```\esb``` in in category ```History```:
```
\Marker cat:History|esb
\BgColour 1 0 0 
\Alpha 0.1
```

For multiple markers, the full format is:
```
\Category History
\Marker p
. . .

\Marker esb 
. . .
\EndCategory
```

Multiple categories may be defined in this manner, however failing to include the final ```\EndCategory``` is an error.

### \categorysheet
TeX file:
```
\categorysheet{filename.sty}
```

A category sheet is just a stylesheet with some shorthands. By loading it with the ```\categorysheet``` command, there is no need for the final ```\EndCategory```.
  that defines the properties of zero or more categories and serves as a shorthand, removing the need 
for certain extra commands. It takes the format:
```
\Category people
\BgColour 1 0 0
\Alpha  0.3

\Marker \p
\Justification center

```

The initial ```\Category``` implicitly  sets the currently active marker to ```\esb```, so after ```\Category``` there is no requirement to include ```\Marker esb```.


### \StyleCategory
This approach allows the loading of a particular pre-defined style sheets which themselves have no categorisation.

For example, for  styling notes of the form: 
```
\ef - \cat People\cat*\fr 1.2-6a: \fq Tamar: \ft Bore her twin sons out of wedlock (Gen 38.6-30).\ef*
```
In the hypothetical example below, the language-group represented by the left (inner) column do
not accept the use of green text for styling humans names, prefering red. 
Those represented by the right column consider that all living creatures named
in Scripture should be in green.

The TeX file might be:

```
\StyleCategory{People}{
 \stylesheetL{red-fq.sty} % 
 \stylesheetR{green-fq.sty} %
}
\StyleCategory{SpiritualBeing}{
 \stylesheet{green-fq.sty} % 
}
```



