# Categories

Categories add an additional dimension to styling. While there are not may *contexts* in which they may be officially applied (USFM 3.0 allows only `\ef` and `\esb`), they allow alternative styles for almost all styling elements.
[http://ubs-icap.org/chm/usfm/3.0/notes_study/categories.html]

In the XeTeX macros, categories need to be enclosed by another marker. Some
markers form an explict enclosure (such as footnotes, cross-references and
side-bars), others form an implicit enclosure, (such as tables), where the end marker 
is implicitly provided by the following paragraph style. 

Normal paragraph styles do *not* form any kind of an enclosure. 
## Applying a category to  headings and sidebars
A heading block (`\s..`) in the main body text may *seem* to form an
implicit enclosure, but at the time of writing, the enclosure is not complete,
and there is a persistance of category data beyond the heading block. Such
behaviour is not fully defined and should in no way be relied on. The correct
method to apply categorisation 
to a heading block is to define an inline sidebar with `\Position h` (see below and (SideBars.md)[SideBars.md]).
```
\esb \cat PossibleAddition\cat*
\s The Woman Caught in Adultery
\sr John 8:1-11
\esb*
```
As well as special formatting for the sidebar itself, (specifying the position
on the page, similarly to figures and other parameters), all markers within the
sidebar can have alternative values. Note that many of the options prevent a sidebar from 
existing on both sides of a page or column break.


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



