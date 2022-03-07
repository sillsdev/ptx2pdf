# Snippets

This file contains a structured list of snippets. Destinations are marked with
different kinds of fences. Thus snippets to go into the .tex or
ptxprint-mods.tex are fenced with `tex`. Items for PrintDraftChanges are marked
by `perl` (Ideally `regex` but syntax highlighting works so much better with a
recognised language). Each snippet has a second level title, a description, the code and
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
\let\mytv=\defaultprintverse
\lowercase{\def\marginverse{\iffirstinpara\global\firstinparafalse\mytv\fi}}
\def\paramarker#1{\expandafter\global\expandafter\let\csname _#1\expandafter\endcsname \csname #1\endcsname
    \expandafter\gdef\csname #1\endcsname{\firstinparatrue\csname _#1\endcsname}}
\paramarker{p}\paramarker{q1}\paramarker{li}
\let\defaultprintverse=\marginverse
```

### Implementation

First there is a new `if` declared that is used to track whether we have started a
new paragraph or not. Then we collect the old default printverse function that is used
to print the verse number (whether simply or as a marginal verse). We are going
to wrap this function to only call the original if the paragraph if is true.
This is what the new definition of printverse does. Once the the first verse in
a paragraph is printed, the if is set to false so that no others will be printed
in that paragraph.

Next we need to wrap various paragraph type markers to set the paragraph if. The
`paramarker` function wraps a given marker by storing the old marker as `_marker`
and then replace the \\marker with code to set the if and call the old `_marker`.
We then run this code over various key markers that we want to have verse
numbers on. Notice we don't do this for all paragraph markers, since we aren't
interested in tracking verse numbers in `\\q2` for example.

## Mirror Gutter

[Note that this snippet is now redundant as the Layout page has an
option for an "Outer Gutter"]
This snippet puts the extra gutter margin on the outside of the page rather than
the inside. 

```tex
\BookOpenLefttrue
```

### Implementation

This is what happens implicitly when the RTL book order is specified. And it may
have some unforeseen effects in regard to RTL type books.

## Technique: Setting style parameters in ptxprint-mods.tex

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

## Auto lengthen poetry

A team has nice and short \\q1 and \\q2 lines in their text which work great for 2-col layouts.
But for a single column layout, we would like to merge all \\q2 into the previos \\q1, and then
turn every other \\q1 into a \\q2 to make it look like poetry.

```perl
"\\q2 " > ""
"(\\q1(?:[^\\]|(\\[fx]).*?\2\*|\\v)+?)\\q1" > "\1\\q2"
```

### Implementation

First we delete all the \\q2 lines merging them into their preceding \\q1 lines.
Then we match 2 adjacent \\q1 paragraphs. To do that we have to skip \\f \\x and \\v
when searching for 2 adjacent \\q1 paragraphs. We do this with a big old \|or\| whose
elements are: 
- non backslash character
- \\f or \\x upto their corresponding \\f\* \\x\*
- \\v 

## Allow linebreaks after in-word hyphens

When the hyphen is a word-forming character in the USFM text, but normally it isn't a 
line-breaking opportunity. But this team wanted to allow a soft-break after hyphens.
We do not want to break in verse ranges, etc. where a hyphen is between digits. 

```perl
"(?<=\s[^\\]*\D)-(?=\D)" > "-\u200B"
```

### Implementation

The regex starts with a look-behind assertion. To understand this consider the engine
matching the hyphen after the look-behind assertion. When it matches it then checks the
look-behind assertion (i.e. does the string preceding the hyphen match that sub-expression.
The look-behind assertion checks that there is a space followed by no marker followed by 
a non digit immediately before the hyphen. Then, after the hyphen there is a look-ahead
assertion which in this case is a non-digit \\D. And we replace just the hyphen (since
the look-ahead assertion is not included in the match), with a hyphen followed by a 
zero-width space which allows a line break.

## Make glossary entries list items

Paratext very unhelpfully forces glossary items to use the \\p marker which is less than
ideal for a list of glossary items. This replaces the \\p with \\ili only in the GLO book.
(This doesn't yet handle multi-paragraph entries.)

```perl
at GLO "\\p \\k " > "\\ili \\k "
```

## Make each chapter start on a new page

If you are wanting to produce a kid's chapter book of scripture with each chapter starting
on a new page, then set the chapter label to something appropriate, like 'Chapter' and apply
this rule to force a new page before the chapter begins, followed by a short rule under the
chapter title.

```perl
"(\\c \d+)" > "\\pb\n\1\n\\zrule|\\*"
```

## Fancy book separators from Heading information

Use the Header text for a book's title page along with a language-specific sub-heading.

```perl
"(?ms)(\\h )(.+?\r?\n)(.+?)(\r?\n)(\\mt)" > "\1\2\3\4\\zgap|2in\\*\4\\mt \2\\is The New Testament in Wakawaka\4\\zrule\\*\4\\pb\4\5"
```

### Implementation

We grab 4 capture groups:
- the header marker
- the header contents
- intermediate lines
- a new line - which is useful to generate OS-specific new lines
- the \\mt marker - which will be preceded with all the new info
Then we assemble the output string that we need using those components. 
We also throw in some vertical space, a horizontal rule followed by a pagebreak.

## Add a rule after the intro (for all books)

Use a hoizontal rule (line) after the introductory outline, before the 1st chapter.

```perl
'(\\c 1 ?\r?\n)' > '\\zrule\\*\r\n\1 '
```

## Add a rule before the introductory outline

Just for the gospel of Mark, insert a page break BEFORE the title of the Introductory Outline.

```perl
at MRK "(\\iot Outline)" > "\pb\r\n\1" 
```

## Insert pagebreak at specific location

Push a particular section heading in the TDX book onto the next page.

```perl
at TDX "(\\s1 Parables Jesus Told)" > "\\pb\r\n\1"
```

## Make the ending of \\ior markers consistent

Remove any trailing space at the end of the \\ior marker to eliminate a jagged right edge 
when justified for a fancy intro outline table.

```perl
' (\\ior\*)' > '\1'
```

## Insert picture at a particular reference

Usually pictures are defined in the USFM text, or added manually in the PicList. But if you need to 
insert pictures through the specified changes, then this trick is useful.

```perl
at EPH 6:13 "(armed soldier.)" > '\1\\fig Soldier with armour|alt="Map Creator soldier with armour" src="ESG Armor of God(v2).png" size="col" ref="6:14-18"\\fig*'
```

## Add an alphabetic section header to Strong's reversal index

Just for the XXS book, insert the first letter of each section of verncular renderings
before the block of renderings with their Strong's H and G numbers.

```perl
at XXS "(\\m ?\r?\n(.))" > "\\s - \2 -\n\1"
```

## Adjust the underline position and thickness

The default underline parameters might need to be tweaked based on the script, font and leading.

```tex
\Marker pn\relax\Underline \relax
\def\UnderlineLower{-0.1em}\def\UnderlineThickness{0.05em}
```

## Exclude certain chapters from being printed

Many teams translate some of the Psalms and want to print them out without all the intermediate
Psalms (which may be drafted but unchecked). This snippet allows for specified chapters to be dropped.

```perl
at PSA "(?s)\\c (3|5|9|24|119|142)[ \r\n].+?(?=\\c)" > ""
```
