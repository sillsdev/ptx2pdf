# Snippets

This file contains a structured list of snippets. Destinations are marked with
different kinds of fences. Thus snippets to go into the .tex or
ptxprint-mods.tex are fenced with `tex`. Items for PrintDraftChanges are marked
by `regex`. Each snippet has a second level title, a description, the code and
then marked with a 3rd level is a section called `Implementation` that describes
how the snippet works, rather than how to use it.

Snippets with an initial 'Technique:' in the name are not true snippets, but are
more descriptive of programming techniques. Ideally this file should be empty.

Notice that this document exists because not everything that people might want
to do is made available in PTXprint via the UI. Should a snippet get so
promoted, it is removed from this file.

## Paragraph Initial Verses

This snippet limits verse numbers so that only the first verse in a paragraph is
shown. It is typically used in conjunction with marginal verses for reader
editions where only limited verse hints are required.

```tex
\newif\iffirstinpara \firstinparatrue
\let\mytv=\printverse
\def\printverse{\iffirstinpara\global\firstinparafalse\mytv\fi}
\def\paramarker#1{\expandafter\let\csname _#1\expandafter\endcsname \csname
#1\endcsname
    \expandafter\gdef\csname #1\endcsname{\global\firstinparatrue\csname
_#1\endcsname}}
\paramarker{p}\paramarker{q1}\paramarker{li}
```

### Implementation

First there is a new if declared that is used to track whether we have started a
new paragraph or not. Then we collect the old printverse function that is used
to print the verse number (whether simply or as a marginal verse). We are going
to wrap this function to only call the original if the paragraph if is true.
This is what the new definition of printverse does. Once the the first verse in
a paragraph is printed, the if is set to false so that no others will be printed
in that paragraph.

Next we need to wrap various paragraph type markers to set the paragraph if. The
`paramarker` function wraps a given marker by storing the old marker as \_marker
and then replace the \marker with code to set the if and call the old \_marker.
We then run this code over various key markers that we want to have verse
numbers on. Notice we don't do this for all paragraph markers, since we aren't
interested in tracking verse numbers in `\\q2` for example.

## Mirror Gutter

This snippet puts the extra gutter margin on the outside of the page rather than
the inside.

```tex
\BookOpenLefttrue
```

### Implementation

This is what happens implicitly when the RTL book order is specified. And it may
have some unforeseen effects in regard to RTL type books.

## Technique: Setting style paramaters in ptxprint-mods.tex

This snippet is less a snippet as a technique. It shows two ways of setting
style parameters from TeX.

```tex
\expandafter\def\csname v:position\endcsname{inner}

\Marker v\relax
\Position inner\relax
```

### Implementation

This first way sets the actual style attribute directly and works even if there
is no .sty markup for the attribute. The second shows how style information can
be specified more like a .sty file, within TeX. Notice that each value is
delimited by `\relax` and that the `\Marker` is necessary to know which style
marker we are setting attributes one.

