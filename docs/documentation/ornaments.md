# Ornamental borders

## General introduction

This 'plugin' provides access to ornamental borders around sidebars. 
Eventually it is expected that it will also provide page-borders and 
ornamental separator lines.

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
entirely irrelevant to using the ornaments with PTXprint.

### What this plugin adds
The ornaments plugin can be instructed to stretch, repeat, or optionally exclude 
ornaments to hopefully provide a pleasing result no matter what the final size
of the side-bar is.

## Setup
It is necessary to install the LaTeX package, but there is no requirement 
to install any of its dependencies for this task.
[https://ctan.org/pkg/pgfornament](https://ctan.org/pkg/pgfornament)

## Loading 
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


