# Ornamental borders and separators

## General introduction

This 'plugin' provides access to ornamental borders around sidebars. 
ornamental separator lines.
Eventually it is expected that it will also provide page-borders.

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
The images are loaded on use and transcribed (as vector drawing) into the PDF
file. 

The stroke colour, stroke-width and fill colour may be selected at load-time.
The current code provides for borders arround sidebars, with the parameters
described within the style sheet.

### Ignore other documentation: what this is not
While using the images from the above packages, the  ornament-including code is
in no way intended to be a version of the large and complex pgf-drawing
enviromnment. It only replicates fragments of code that are necessary to
draw the ornaments in PDFs. Most of the documentation in the latex package is
therefore entirely irrelevant to using the ornaments with PTXprint.

### What this plugin adds
The ornaments plugin can be instructed to stretch or repeat ornaments to
hopefully provide a pleasing result, no matter what the final size of the
side-bar is.  Repeated elements can have matching or dissimilar counts.
Counts determined from the top of the box can be re-used by other edges.

## Installation
It is necessary to install the LaTeX package, but there is no requirement 
to install any of its dependencies for this task.
[https://ctan.org/pkg/pgfornament](https://ctan.org/pkg/pgfornament)

## Using the module
At present ptxprint has no way to select plugins, not even on the advanced tab.
For the plugin to function, it must be loaded manually, and until some bugs 
are worked out with auto-loading, it must be loaded before style files are
loaded. The ptxprint-premods.tex file should include the line:
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
\Borderstyle ornaments
```
This is true for rules and for sidebars.

## Configuring a border for a sidebar
### Ornament specification
Each ornament that builds part of the border is specified by four parameters. The parameters are separated by vertical bars `|`, and may be ommitted. 

 1. Ornament number  
 2. Rotation/mirroring
 3. Stretch or repeat instructions.
 4. Scaling.

Trailing vertical bars may be ommitted. Thus if there is no rotation,
stretching, repetition or scaling, an ornament may be specified by just its
number.  Ornaments are normally set so that their height (width for
vertical sides) matches the border thickness.  
Corner elements normaly need to be larger than this, and 
scaling is used to ajusted their size to something appropriate.

#### Rotation and mirroring
 `u` 0° rotation (up becomes Up)
 `v` Vertical mirror  (up becomes down)
 `h` Horizontal mirror (left becomes right)
 `d` 180° rotation (up becomes Down, left becomes right)
 `l` 90° rotation anticlockwise (up becomes Left)
 `r` 90° rotation clockise (up becomes Right)
 `L` 90° rotation anticlockwise, then mirror (up becomes Left, left becomes top)
 `R` 90° rotation clockise, then mirror (up becomes Right, right becomes top)

#### Stretching or repeating
(At present there is no stretch *and* repeat)

 `x` use `\xleaders` to fill the space.
 `-` Stretch the ornament.

*Variable-based repetition*. If conflicting definitions of the range are given, then the last range defined 
will take priority.
 
 `?A`	Repeat A times, where A is 0 or 1
 `*A`	Repeat A times, where A >= 0
 `+A`   Repeat A times, where A > 0
 `(M,N)A` Repeat A times, where A>= M and A<=N
 `"A`	Repeat A times, using the same range for A as was last given (ditto marks)
 `=A`	Repeat A times, don't adjust A.

### The border pattern
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

## Additional ornaments
These ornaments have been defined in addition to the ornaments provided by the LaTeX package
 (0)	A square space
 (-1) 	A simple horizontal line across the middle of a square space 
 (-2)	A simple horizontal line across the middle of a rectangular space 1 high and 2 wide.
 (-3)	A simple horizontal line across the middle of a rectangular space 1 high and 5 wide.

### Defining additional ornaments
Ornament -1, for example, is defined as follows:
```
\LocalOrnament{-1}{10}{10}{\m 0.0 5 \l 10 5 \k } % A centred line.
```
The parameters to  `\LocalOrnament` are {ornament number} {x dimension} {y dimension} {code}
Code elements recognised are:

 `\m X Y` Move to X,Y
 `\l X Y` Line from the current point to X,Y
 `\r X1 Y1 X2 Y2` Rectangle (X1,Y1) to (X2,Y2)
 `\c X1 Y1 X2 Y2 X3 y3` A bezier curve from the current point to (X3,Y3), using (X1,Y1) and (X2,Y2) as control points.
 `\o` Close path
 `\k`	Stroke
 `\s`	Fill and stroke (or just stroke if there's no fill colour)
 `\i` Clip to path
 

## Debugging options
If the flag `\boxorntrue` is set (in the .tex file or via a hook), then 
ornaments will be displayed with a frame around them.

