# Ornamental borders and separators

## General introduction

This 'plugin' provides access to ornamental borders around sidebars,  
ornamental separator lines and (probably incomplete support) for ornamental
page-borders (note that these extend beyond the normal text area).

### Sources of ornaments
#### pgfornament package
There is a LaTeX package called pgfornament (based on an earlier package 
psvectorian), which provides access to pen-and-ink style vector-based artwork
such as ornamental borders. Some of the artwork is unsuitable for use in
scripture or scripture-based products, but, chosen carefully with a view to
local cultural preferences, some of them may be of use.  The 
original Victorian-era inspired 'vectorian' illustrations fall into categories 
of geometric and botanical drawings, corner-pieces, linear features, animals,
hands, and objects. 

Recent versions (1.2, Oct 2020) of the package now also include the
pgfornament-han images, from LianTse Lim and Chennan Zhang, to provide some of
the traditional patterns of the Han style using the same mechanism.

Adding alternative graphical elements is also possible. Each
'ornament' resides in its own file, (but with dimensions defined separately).
The images are loaded on use and transcribed (as vector drawings) into the PDF
file. 

The stroke colour, stroke-width and fill colour may be selected at load-time.
The current code provides for borders arround sidebars, with the parameters
described within the style sheet.

PTXprint now includes the ornaments from version 1.2 of the package.

#### Locally defined ornaments
Simple lines and other features can easily be hand-coded, using the same
mechanisms as above. For future-compatability these have been given negative
numbers.  (See section on additional ornaments, below).

#### Border or dingbat fonts
There are two mechanisms to access font-based border elements. Either:
- a character or string from a specific font may be assigned an ornament number.
- If most elements are from a global 'Ornament font', the desired string may
be specified in the pattern string, instead of an ornament number. (Internally, this 
auto-generates an ornament number). 

If font-based elements are used, then only the (fill) colour can be specified.

### This does not implement pgf!
While using the images from the above packages, the  ornament-including code is
in no way intended to be a version of the large and complex pgf-drawing
enviromnment. It only replicates fragments of code that are necessary to
draw the ornaments in PDFs. Almost all of the documentation from the latex package is
therefore entirely irrelevant to using the ornaments with PTXprint.

### What this plugin adds
The ornaments plugin can be instructed to stretch or repeat ornaments to
hopefully provide a pleasing result, no matter what the final size of the
side-bar is.  Repeated elements can have matching or dissimilar counts.
Counts determined from the top of the box can be re-used by other edges.

## Using the module
At present the PTXprint user-interface has no way to select plugins, not even
on the advanced tab.  For the plugin to function, it must be loaded manually,
and until some bugs are worked out with auto-loading, it must be loaded before
any style files are loaded. The ptxprint-premods.tex file should include the
line:
```
\input ornaments
```

PTXprint must also be instructed about where the ornament files live on your local filesystem, 
via the TEXINPUTS enviromnent variable. E.g. on linux you might need to enter:
```
export TEXINPUTS=.:/usr/lib/ptx2pdf/src:/usr/share/texlive/texmf-dist/tex/latex/pgfornament/:/usr/share/texlive/texmf-dist/tex/generic/pgfornament/vectorian/
ptxprint
```

## Specifying that a border or sidebar should use ornaments
The relevant stylesheet entry to use the ornaments package is
```
\BorderStyle ornaments
```
This is true for rules and for sidebars. 

## The Ornament Catalogue
See [OrnamentsCatalogue.pdf](OrnamentsCatalogue.pdf).

## Configuring a border for a sidebar
### Ornament specification
Each ornament that builds part of the border is specified by four parameters. The parameters are separated by vertical bars `|`, and may be ommitted. 

 1. Ornament number  (or string for font-based ornaments)
 2. Rotation/mirroring
 3. Stretch or repeat instructions.
 4. Scaling.

Trailing vertical bars may be ommitted. Thus if there is no rotation,
stretching, repetition or scaling, an ornament may be specified by just its
number.  Ornaments are normally set so that their height (width for
vertical sides) matches the border thickness.  
Corner elements normaly need to be larger than this, and 
scaling is used to ajusted their size to something appropriate.

If a string is specified, it must be enclosed in straight double quotes (`"thus"`).
Specifying a string in the ornament specification is a shorthand which autogenerates a 
new ornament number if there's no matching string already been used. Such ornaments always use the 
font named by `\StringOrnamentFont`.

#### Rotation and mirroring
 -  `u` 0° rotation (up becomes Up)
 - `v` Vertical mirror  (up becomes down)
 - `h` Horizontal mirror (left becomes right)
 - `d` 180° rotation (up becomes Down, left becomes right)
 - `l` 90° rotation anticlockwise (up becomes Left)
 - `r` 90° rotation clockise (up becomes Right)
 - `L` 90° rotation anticlockwise, then mirror (up becomes Left, left becomes top)
 - `R` 90° rotation clockise, then mirror (up becomes Right, right becomes top)

#### Stretching and/or repeating
 - `x` use `\xleaders` to fill the space.
 - `-` Stretch the ornament.

*Variable-based repetition*. 

  - `?A`	Repeat A times, where A is 0 or 1
  - `*A`	Repeat A times, where A >= 0
  - `+A`   Repeat A times, where A > 0
  - `(M,N)A` Repeat A times, where A>= M and A<=N
  - `"A`	Repeat A times, using the same range for A as was last given (ditto marks)
  - `=A`	Repeat A times, don't adjust A from previous sides.

If conflicting definitions of the range are given, then the **last range defined**
will take priority. Variables with *upper* case request a simple repetition,
variables with *lower* case indicate that the ornament is allowed to stretch 
as well as repeat.

The code determines the natural length of objects using the same variable, and
then determines the values of the variables that give the best result (minimum 
stretch or shrink required).

#### Scaling
The value of 1.0 means that for a horizontal border piece the element will 
match the border-width. A value of `>1.0` means that the element will 
appear larger than the requested border size, and a value `<1.0` means that the 
element will be smaller. For *rules* the scaled ornaments aline along 
the centre-line of the rule; for border objects the alingment edge  is away 
from the centre, thus the corner pieces (which must be inculded in the top and bottom 
patterns (and are often set with a scaling of 1.5-2.5), extend into the edges.

##### Worked example
Let us suppose that an ornamental rule border should be made of 4 ornaments,
(1,2,3,4), having natural lengths of 10pt, 13pt, 11pt and 15pt respectively.
Further, it has been decided that the rule should be symmetrical, and elements
1 and 3 should occur an equal number of times. The user writes the pattern below
(shown here on separate lines and indented, purely for clarity, in reality it should be 
a simple comma-separated list):
```
1||*A
 2||+B
  3||+A
   4||?c
  3|h|"A
 2|h|*B
1|h|"A
```
Then the final ranges are A(1 or more), B(0 or more), C(0 or 1). The length of the 
border will be:
```
A*(10+11+11+10) + B*(13+13) + C*15
```
With a single stretchable component, ornament 4. The minimum length is 42pt (A=1,
other variables 0). If a border of 50pt is requested, then ornament C will be 
used to fill the missing 8pt of available space, but it will be shrunk to 8/15 of its 
natural length. 

If a border of 158 points is requested:

 A | B | C |  Stretchy? | Stretch/Shrink
---|---|---|------------|-------------
 3 | 1 | 1 |    Yes     |  -9pt
 3 | 1 | 0 |    No      |  6pt
 3 | 0 | 1 |    Yes     |  16pt
 2 | 3 | 0 |    No      |  -4pt
 2 | 2 | 1 |    Yes     | 7pt
 2 | 1 | 1 |    Yes     | 33pt
 1 | 4 | 1 |	Yes	| -3pt
 1 | 4 | 0 |	No	| 12pt
 0 | 6 | 0 | 	No 	| 2pt
 0 | 6 | 1 | 	Yes	| -12pt


Although the combination (0,6,0) only has 2pt of stretch required, the lack of
stretchiness means that the combination (1,4,1) wins. If combination (0,6,0)
were chosen, then there would be 2pt of whitespace in the border/rule, which is 
highly undesirable. 


### The border pattern
As a general rule, a pattern should *always* contain some stretch, even if this
is by stretchable spacing elements.
The border pattern is a comma-separated list of ornaments defined as above.
Example:
```
\BorderPatternTop 39|||2.5,0|||0.2,88||-,0||*A,39|h||2.5
```
This rule states that the top border is made up with:
 * The corner piece ornament 39 (scaled to  2.5 the border thickness),
 * A small rigid space, 0.2 border thicknesses
 * Linear ornament 88, stretched,
 * Any number of spaces.
 * Corner piece ornament 39, flipped horizontally and scaled to 2.5.

The other borders are specified as below:
```
\BorderPatternBot 39|v||2.5,0||*,88|h|-,0||-,39|d||2.5
\BorderPatternLeft 0|||0.2,88|l|-,0|l|*A,-2|l|*A,0|l|*A
\BorderPatternRight 0|l|*A,-2|r|*A,0|r|*A,88|r|-
```

### Other styling options
`\BorderFillColour` Where the ornament has a fill colour, what should that be? (the special value `none` means no fill)
`\BorderLineWidth` Defines the line thickness of the 'pen'

#### Ornamental Rules
The `\zrule\*` horizontal rule's pattern is defined using `\BorderPatternTop`.
It also  accepts the following options:

`\VerticalAlign`  Accepted values `t` (top), `b` (bottom), and `c` (center).
Normally ornaments for rules are aligned centrally (i.e. if an element is
scaled, then its centre will used). Other choices can be imposed using parameter. 
`\Raise`  Lift the bottom edge (of unscaled ornaments) from the baseline.

#### Page Borders
In the style sheet: 
```
\Marker textborder
\TextProperties publishable
\BorderStyle vectorian1
```
For a given book, the marker can be prefixed as normal e.g.: ```\Marker id:MAT|textborder ``` will work.
borders are not put on title sections or on negative page numbers.
Setting the `nonpublishable` property will disable text borders.


## Using the pgfhan ornaments througout the document
The pgfhan ornament set may be selected by adding this line to
`ptx-premods.tex` file (after `ornaments.tex` has been loaded). 
 ```
\def\OrnamentsFamily{pgfhan}
```

## Using both ornament sets in the same document
In the situation that some parts of the document need one family of ornaments
and other parts need another, that switching can be done using this command (in
one of the `.tex` file):
```
\SwitchOrnamentsFamily{pgfhan}
```
Further, the stylesheet can include:
```
\BorderStyleExtra pgfhan
```
for a border or zrule, which calls the above.

This command attempts to load the relevant dimension set for the specified
family. If it is successful, then the `\OrnamentsFamily` value will be altered.
Subsequent calls with the same family specified will not bother to re-load the
file, instead the loaded settings will be remembered.
If loading the file is unsuccessful, a warning message will be produced and the
original family will remain selected. 

Note that while the caching of settings mentioned above means that the command
can be used to switch to a previously-loaded ornament family by a hook or
milestone or stylesheet, it *cannot* be used to perform the initial loading
without reassigning all relevant catcodes, which it does not do at present.
Thus if such switching is expected, the `.tex` file that sets up the hooks
should switch to all expected families in turn.

## Additional ornaments
These ornaments have been defined in addition to the ornaments provided by the LaTeX package:
 - (0)	A square space
 - (-1) A simple horizontal line across the middle of a square space 
 - (-2)	A simple horizontal line across the middle of a rectangular space 1 high and 2 wide.
 - (-3)	A simple horizontal line across the middle of a rectangular space 1 high and 5 wide.

### Font-based ornaments
The following defines two new font-based ornaments. An ornament thus defined
will be drawn using the fill colour, and will have no separate stroke or
stroke-colour. It will scale and position just as other ornaments, (ignoring
any font-defined baseline). The ornament may be mixed with ornaments from any
other source, (including other fonts), and may be stretched, rotated, mirrored, etc 
just like other ornaments. Numerical font positions may be given by the
(strange) XeTeX notation of four carets followed by a four digit hexadecimal
number. Multiple such characters may be used in a single string, as can any `\TeX` macros that 
are acceptable for within a simple horizontal box (`\hbox`). 


```
\StringOrnament{402}{AGA Arabesque Desktop}{^^^^f057}
\StringOrnament{403}{Times New Roman}{<-+=+->}
\StringOrnament{403}{URW Chancery L}{\TeX}
```

If selecting ornaments as part of the pattern is preferred (and they all come from the same 
`\StringOrnamentFont`), **and no TeX macros or primitives** are going to be used,
 then the font to be used can be specified thus: (in the `ptx-premods.tex` file):
```
\def\StringOrnamentFont{AGA Arabesque Desktop}
```

And the stylesheet can include the string-pattern, enclosed in straight double-quotes:
```
\BorderPatternTop "^^^^f051"|||1.02,"^^^^f057"||*a,"^^^^f045"|||1.02
```

Behind the scenes, this checks for previous use of the string, and if it has not
been used, calls `\StringOrnament` using the `\StringOrnamentFont`.

### Defining additional ornaments
Ornament -1, for example, is defined as follows:
```
\LocalOrnament{-1}{10}{10}{\m 0.0 5 \l 10 5 \k } % A centred line.
```
The parameters to  `\LocalOrnament` are {ornament number} {x dimension} {y dimension} {code}
Code elements recognised are:

 - `\m X Y` Move to X,Y
 - `\l X Y` Line from the current point to X,Y
 - `\r X1 Y1 X2 Y2` Rectangle (X1,Y1) to (X2,Y2)
 - `\c X1 Y1 X2 Y2 X3 y3` A bezier curve from the current point to (X3,Y3), using (X1,Y1) and (X2,Y2) as control points.
 - `\o` Close path
 - `\k`	Stroke
 - `\s`	Fill and stroke (or just stroke if there's no fill colour)
 - `\i` Clip to path
 
## Installation of updated ornaments
PTXprint now includes the ornaments from version 1.2 of the package. The full
package is here:
[https://ctan.org/pkg/pgfornament](https://ctan.org/pkg/pgfornament). No
dependencies are needed, indeed much of the package itself is irrelevant for use with these macros,
as the ornaments.tex plugin replicates the needed functions.  Only files
`*.pgf` and `*.code.tex` are required.

## Debugging options
If the flag `\boxorntrue` is set (in the .tex file or via a hook), then 
ornaments will be displayed with a frame around them.

