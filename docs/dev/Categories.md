# Categories

Categories add an additional dimension to styling. While there are not may *contexts* in which they may be officially applied (USFM 3.0 allows only `\ef` and
`\esb`), they allow alternative styles for almost all styling elements.
[http://ubs-icap.org/chm/usfm/3.0/notes_study/categories.html]

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



