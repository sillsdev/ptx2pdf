This document exists because not everything that people might want to do is made available 
in PTXprint via the UI. So this file contains a structured list of code snippets which can 
be copied and pasted into the appropriate settings files. There are 3 sections:

* RegEx snippets
* TeX snippets
* Python scripts

Each snippet has a second level title, a description, the code and then
marked with a 3rd level is a section called `Implementation` that describes
how the snippet works, rather than how to use it.

Snippets with an initial 'Technique:' in the name are not true snippets, but are
more descriptive of programming techniques.

Should a snippet get so promoted, it is removed from this file.

# RegEx snippets
The snippets in this section go into the changes.txt or PrintDraftChanges.txt file.
Note that the code fence is marked as `perl` (this would ideally be `regex` but 
syntax highlighting works so much better with a recognised language). 

## Allow linebreaks after in-word hyphens

When the hyphen is a word-forming character in the USFM text, but normally it isn't a 
line-breaking opportunity. But this team wanted to allow a soft-break after hyphens.
We do not want to break in verse ranges, etc. where a hyphen is between digits. 

```perl
'(?<=\s[^\\]*\D)-(?=\D)' > '-\u200B'
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
at GLO '\\p \\k ' > '\\ili \\k '
```

## Mark headers with 3-letter book codes (temporarily)

When working with a script that you cannot read, it is very helpful to place the book code in
the header (using the Alt book name) so that you can navigate easily within the entire NT. But
remember to comment out this expression before your final.

```perl
'(\\id (...).*\n)' > '\1\\h1 \2\r\n'
```

### Implementation

We grab 2 capture groups:
- the entire \id line
- the 3-letter book code

Then we put the 1st group back in and follow it with a new marker \h1 and the 
2nd group (which is the book code) and finally a new line code.

## Force a blank page at the end of the entire NT

Sometimes you just need a blank page after the final text. Change the 'Amen.' to whatever
the last word in Revelation is.

```perl
at REV 22:21 '(Amen.)' >  '\1\n\\pb\n\\p \\bd ~\\bd*'
```

## Fancy book separators from Heading information

Use the Header text for a book's title page along with a language-specific sub-heading.

```perl
'(?ms)(\\h )(.+?\r?\n)(.+?)(\r?\n)(\\mt)' > '\1\2\3\4\\zgap|2in\\*\4\\mt \2\\is The New Testament in Wakawaka\4\\zrule\\*\4\\pb\4\5'
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

Use a horizontal rule (line) after the introductory outline, before the 1st chapter.

```perl
'(\\c 1 ?\r?\n)' > '\\zrule\\*\r\n\1 '
```

## Add a rule before the introductory outline

Just for the gospel of Mark, insert a page break BEFORE the title of the Introductory Outline.

```perl
at MRK '(\\iot Outline)' > '\pb\r\n\1' 
```

## Insert pagebreak at specific location

Push a particular section heading in the TDX book onto the next page.

```perl
at TDX '(\\s1 Parables Jesus Told)' > '\\pb\r\n\1'
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
at EPH 6:13 '(armed soldier.)' > '\1\\fig Soldier with armour|alt="Map Creator soldier with armour" src="ESG Armor of God(v2).png" size="col" ref="6:14-18"\\fig*'
```

## Auto lengthen poetry

A team has nice and short \\q1 and \\q2 lines in their text which work great for 2-col layouts.
But for a single column layout, we would like to merge all \\q2 into the previous \\q1, and then
turn every other \\q1 into a \\q2 to make it look like poetry.

```perl
'\\q2 ' > ''
'(\\q1(?:[^\\]|(\\[fx]).*?\2\*|\\v)+?)\\q1' > '\1\\q2'
```

### Implementation

First we delete all the \\q2 lines merging them into their preceding \\q1 lines.
Then we match 2 adjacent \\q1 paragraphs. To do that we have to skip \\f \\x and \\v
when searching for 2 adjacent \\q1 paragraphs. We do this with a big old \|or\| whose
elements are: 
- non backslash character
- \\f or \\x upto their corresponding \\f\* \\x\*
- \\v 

## Add an alphabetic section header to Strong's reversal index

Just for the XXS book, insert the first letter of each section of verncular renderings
before the block of renderings with their Strong's H and G numbers.

```perl
at XXS '(\\m ?\r?\n(.))' > '\\s - \2 -\n\1'
```

## Suppress introductory material for *some* books, but keep it for others

I would like most intro material (stuff before \c 1) to print. But in a few back matter books, 
there is intro material which is fine for apps, but not needed in a printed book.

Here is the trick to suppress these in specific books. Just add this line to your changes.txt 
file and replace BAK,XXA,XXE with whichever books you want the intro material stripped from.

```perl
at BAK,XXA,XXE '\\i[so]\d?\s.+\r?\n' > ''
```

## Add a toc2 for each chapter

We want a TOC entry for each chapter rather than just the book. To make it even
better, don't include an extra entry for chapter 1

```
'(\\h\s*)(.*?)(\r?\n)' > '\1\2\3$set{bk,\2}'
'(\\c\s*)(\d\d+|[2-9])(\s+)' > '\1\2\3\\toc2 $var{bk} \2\n'
```

This uses two change functions, which are identified by \$ and then the function
name. Parameters are a comma separated list within { }. The first line collects the \\h value which is
the book name used in the header. This will be inserted before each chapter
number as part of the TOC. The second line matches a chapter with number > 1 and
outputs the same chapter and then a toc2 line involving the book and chapter.

# TeX Snippets
The snippets in this section go into the ptxprint-mods.tex file.

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

## Technique: Kerning digits in a chapter number

Digits are typically designed to be monospaced so that they layout out nicely in
tables. But in some scripts, some digits are significantly narrower than others
and it would be nice to kern those digits more tightly in chapter numbers. This
is only really noticeable in the book of Psalms.

To do this we create some magic characters that will insert the negative kerns:

```tex
\catcode"005E=7
\catcode"E123=\active
\def^^^^e123{\nobreak\kern-0.2em\relax}
\catcode"E124=\active
\def^^^^e124{\nobreak\kern-0.4em\relax}
```

In effect we are making two negative spaces. Now in the changes file we want to
insert those special spaces around the digits 0 and 1 for chapter numbers.

```perl
at PSA "\\c\s(\d*[10]\d*)" > "\\c \1\n\\cp \\beginL \1 \\endL\n"
in "\\cp\s+\\beginL \d+ \\endL": "([01])" > "\uE123\1\uE123"
"\uE123\uE123" > "\uE124"
```

The first rule copies the chapter number to a published chapter string if it
contains a 0 or a 1. It also marks it as being output left to right, since
Arabic digits are output left to right in right to left text. The second rule
takes that publishable chapter and inserts a negative space before and after
ever 0 or 1 in the string. The last rule merges adjacent pairs of negative widths
into a single doubly narrow width.

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

## Tabbed indent for glossary or Strong's index

When typesetting an indented list, such as a glossary or Strongs index, it looks
neater if the main body starts at the same indent position as the rest of the 
paragraph. In this example, the Strongs number is in bold \\bd ... \\bd\* and
we can add a 'tab' after the Strongs number to make things line up neatly. 
Note that the \setbookhook restricts this change to just the 'XXS' book.

```tex
\setbookhook{start}{XXS}{
 \sethook{start}{bd}{\setbox0=\hbox{9999}\hbox to \wd0\bgroup}
 \sethook{end}{bd}{\hfil\egroup}}
```

### Implementation

We create a hook that stores the content of the marker in an hbox. The width of
this book could be just set to a fixed width as in replacing one line with:

```tex
\sethook{start}{bd}{\hbox to 1in\bgroup}
```

But rather than having to calculate the width of the box for every change in
point size, we measure the width of 4 digits and use that width to set the width
of the hbox containing the Strong's number (which is always 4 digits or less).

## Forces better calculation of the number of lines 

Sometimes when your apply a +1 to a reference in an AdjList, it ends up doing a +2.
To prevent this unwanted behaviour, you can force a more fine-grained adjustment at
the specific verse location.
```tex
\setcvhook{LUK7.48}{\pretolerance=1}
\setcvhook{LUK8.1}{\pretolerance=100}
```

### Implementation

Setting `\pretolerance=1` forces the paragraph builder to do the extra passes it
might not have done otherwise, to give a more accurate result. And then we
reset the value for the next paragraph and following.

## Nudge chapter number down at \nb chapters

The Burmese digit 6 rises rather high and crashes into the previous
line when an \nb (no-break para) is used after a \c chapter. This
snippet demonstrates how to lower the \nb chapter number by a smidgen
for the given references (in this example: JHN 16, 2CO 6, HEB 6).

```tex
\expandafter\def\csname raise-chapter.JHN16.0\endcsname{-0.3}
\expandafter\def\csname raise-chapter.2CO6.0\endcsname{-0.3}
\expandafter\def\csname raise-chapter.HEB6.0\endcsname{-0.3}
```

## Horiz rule to fill left and right edges of \s2 titles

```tex
\sethook{start}{s2}{\leaders\vrule height 2.5pt depth -2.25pt \hfill \kern.3em\null}
\sethook{end}{s2}{\kern.3em\leaders\vrule height 2.5pt depth -2.25pt \hfill \null}
```

## This applies the specified rounded rectangular box to bridged verses

```tex
\SeparateVerseAdornmentsfalse
\newbox\stretchedversestarbox
\setbox\stretchedversestarbox=\hbox{\XeTeXpdffile 'c:/pathtofile/BridgedVerseRoundedBox.pdf' scaled 760 \relax}
\def\AdornVerseNumber#1{\beginL\rlap{\hbox to \ifadorningrange\wd\stretchedversestarbox\else\wd\versestarbox\fi{\hfil #1\hfil}}%
    \raise -4.5pt\ifadorningrange\copy\stretchedversestarbox\else\copy\versestarbox\fi\endL}
```

## Table of Contents right-align column 2

```tex
\deftocalign{2}{r}
```

## Add extra  TOC entries 

Additional TOC entries can be specified to appear before or after an automatic table of
contents. As this is done by seting values that are used while `\ztoc` runs, it must occur 
*before* the call to ztoc:

```tex
\ztocafter\tr \tc1 Maps\tc2 \tcr3 479\ztocafter*
  OR
\ztocafter\tr \tc1 Unusual animals mentioned in scripture\tc2 (animals)\tcr3 483\ztocafter*

\ztoc|main\*

```
For the 'before' variant, you must set the style of the table:
```tex
For before
\ztocbefore\tr \cat toc\cat*\tc1 Index\tc2\tcr3 i\ztocbefore*

\ztocafter....
```

## Two Columns Table of Contents

This snippet can be used for the contents peripheral in FRTlocal.SFM:

```tex
\periph Table of Contents|id="contents"
\mt \zvar|contentsheader\*
\is Old Testament
\zgap|-18pt\*
\doublecolumns
\ztoc|ot\*
\singlecolumn
\is ~
\is New Testament
\zgap|-18pt\*
\doublecolumns
\ztoc|nt\*
\b
\ztoc|post\*
\singlecolumn
```

The negative zgap amount may need adjusting according to taste, and the headings
will need translating.

## Set a larger space before footnote caller in the text

If the space before a footnote caller (defined by style zcf) needs to be
increased, then this can be done by adding the following line.

```tex
\sethook{start}{zcf}{\hskip 0.1em}
```

## Don't break before q2 and friends

This snippet keeps q1 based groups of poetry lines together. Insert into the
ptxprint-mods.tex.

```tex
\sethook{before}{q2}{\nobreak}
\sethook{before}{q3}{\nobreak}
```

### Implementation

The `before` hook is run after the previous paragraph is finished. We assume the
previous paragraph is a q1. `\\nobreak` tells TeX not to allow a page break at
this position. If you have long sequences of q2 without a q1, then be careful
because you may have page break problems. Notice that the use of the `before`
hook does not interfere with the `start` hooks used for hanging verse numbers.


## Move the qr word up to the end of previous line (if space permits)

Used in poetry and/or song books to allow a short qr word to
move up to the previous word as long as there is adequate space 
(defined here as 0.3em) between the end of the last word, and the
qr word, like 'Selah'.

```tex
\sethook{start}{qr}{\unskip\nobreak\hfill\penalty50\hskip0.3em\hbox{}\nobreak\hfill\hbox\bgroup}
\sethook{end}{qr}{\egroup}
```

### Implementation

This trick comes from the TeXbook. Since, at a linebreak spaces are removed,
this snippet replaces the space before the 'Selah' with a fill to push it right
and then a recommendation not to break here `\penalty50`. The `\hskip0.3em` only
appears if there is no linebreak before the Selah, and guarantees a minimum
space between the 'Selah' and the end of the text in the paragraph. Then we insert a zero width
non breaking space in the form of `\hbox{}`, with a nobreak and the necessary
fill followed by the box containing the 'Selah' or whatever is marked.

In effect TeX chooses between two text runs depending on whether it needs to
insert a line break:

```tex
\nobreak\hfill
\hbox{}\hfill\hbox{
```

if the line breaks (at the \break). Or with no break:

```text
\nobreak\hfill\hskip0.3em\hbox{}\hfill\hbox{
```

Notice the two `\hfill`s with the ensured space floating between them. But who
cares, since everything is invisible. In both cases, the box is pushed to the
right of the page.


## Show bridged verses at the start of chapters

Generally people do not want to show the verse number for verse 1 at the start
of a chapter. But they may want to show a bridged verse in such a situation.
This snippet shows how to achieve this.

```tex
\catcode`\@=11
\addtopreversehooks{\ifc@ncelfirstverse
    \spl@tprintableverse
    \ifx\v@rsefrom\v@rseto\else\c@ncelfirstversefalse\fi
  \fi}
```

### Implementation

Since we are digging into the internals of the ptx macros, we need access to
internal variables. So we enable @ as a letter for use in macro names.

Next we add a new preverse hook. This macro will be run just before printing (or
not printing) any verse number. If printing the verse is currently disabled
(i.e. at the start of a chapter where verse 1 has been disabled), then let's
test to see if we have a bridged verse. First split the printable verse number
into its components (versefrom and verseto). Then if the two do not compare the
same then cancel the cancelling of verse printing. I.e. print the verse.

## Avoid two marginal verses crashing into each other

It is possible to have verse numbers printed in a left of text margin. This is 
referred to as Marginal verses.

Sometimes, where there is a short verse, two verse numbers appear in the same
line. This causes a crash between the two marginal verse numbers. One way around
this is to tell the ptx macros to bridge two verses and depending on the horizontal
space available may cause the verses to stack vertically. This can be done using, 
for example:

```tex
\bridgeVerses ACT13.30-31.
\bridgeVerses ACT23.26-27.
\bridgeVerses ROM1.22-23.
\bridgeVerses ROM3.15-16.
```

The structure of this command is very precise. The book must be the 3 letter
book id. The chapter must be included even for single chapter books. The
separator between the chapter and verse must be a period. The number after the
hyphen must be the next verse after the first verse and there must be a final
period to complete the specification. Apart from all that, this is a very
convenient way to bridge verses without having to edit the source text. It may
also be used not in a marginal verses context.

Also note that if you want to suppress the hyphen that normally comes between 
bridged verses, you can turn off the verse hyphen in this context with this
line which should be placed before the \bridgeVerses lines:

```tex
\versehyphenfalse
```

## Change Strong's numbers from the 4-digit cell into a 4-in-a-line number

The 4-digit cell numbers for Strong's cross-references are a very handy and compact
form, but these are not searchable in the PDF. If you want to see the 'unpacked'
version of these numbers then add a new style \\myxts which can be styled as needed
and add this snippet.

```tex
\catcode`\@=11
\def\mystrong#1{\get@ttribute{strong}\ifx\attr@b\relax\else\cstyle{#1}{\attr@b}\fi}
\sethook{start}{xts}{\ifinn@te\proc@strong{xts}\else\mystrong{myxts}\fi}

% or use this sethook instead if you want ALL Strong's numbers to 
% be 4-in-a-line strings instead of a 4-digit cell (even in the xref column).
%\sethook{start}{xts}{\mystrong{myxts}}
```

### Implementation

The `\mystrong` macro gets hold of the Strong's number from the attribute and
then formats it according to the character style marker passed as `#1`. Then we
replace the start hook for xts (which previously just called internal code to
process the Strong's number). This new hook decides whether we are in the cross
reference `\ifinn@te` and if so, calls the normal internal code, otherwise we
are in the main text and so `\mystrong` should be called.

Of course if you always want inline numbers even in cross references, then the
hook can be simplified and `\mystrong` always called.

## Special page numbering for a book
I need the page number for the glossary to restart numbering at one, and
be prefixed with G- 
```tex
\setbookhook{GLO}{start}{\pageno=1 \def\pagenumber{G-\folio}}
```

First, we reset the page number to one,  and then redefine the macro that
prints the pagenumber.  (`\folio` prints lower case roman numerals if the page
number is negative, and numbers starting from 1 if positive).

## Move colophon to after included pages
The first line replaces the normal colophon including code with code that will output the 
page. The second line puts the normal colophon including code after any included documents.
```
\sethook{bookend}{final}{\layoutstylebreak\pagebreak}
\sethook{final}{afterincludes}{\layoutstylebreak\singlecolumn\zcolophon}
```

## Side Aligned Notes

It is possible with the PTXprint macros to have notes side aligned in the side
margins. Until we have a button for that, here is how you can achieve it. We
will put the cross references in the margin while keeping the footnotes as notes
in the text.

First set up the margins to be wide enough for the notes. Getting this right
takes some thought because too much and your columns get too narrow and too
narrow and the notes all wrap and look bad. To be honest A5 is probably too
narrow a page to get 2 columns and side notes in. Something like 9" x 6" is
probably better. But for single column, it should be fine. For single column
layout we add extra space typically to the outer margin. For double column, the
inner and outer margins are typically the same, and true gutters can be used to
account for binding. For single column, to set up the
margins, set the margin width to be the inner margin including its binding gutter. Then
set the gutter to be the extra space you want on the outer page and enable the
"Outer Gutter". For example, a margin of 15mm, a binding gutter of 36mm.

The TeX magic is relatively simple:

```tex
\catcode`\@=11
\marginaln@te{x}
\marginnotesgap = 6pt
\marginnoteswidth = \dimexpr 1.5in + \marginnotesgap
\def\MarginNoteSide{outer}
```
We need to allow @ in names so we catcode @ to be a letter. Then we say that we
want `x` to be treated as a marginal note. The marginnotesgap is the space
between the edge of the note at the text. How far from the text should the notes
be. The marginnoteswidth is the width of the marginnote including its gap. Here
I have said I want a 1.5in note and then added the gap on. We can say where we
want the margin notes: inner, outer, left, right

Enabling decorations isn't essential (and we hope to remove the need) but it
does quieten some errors.

If you use quick print, that only runs the job once, you may find that side
notes crash into each other. A quick reprint doesn't fix this. To get the notes
correctly positioned you need to run a full non quick print.


## Fancy headers

There is a style of headers in which each page has the page number on the outer
edge and before it the rangeref separated by a |. This snippet examines how to
do that. Rather than using the built in header support, it is easier to
implement using tex snippets in ptxprint-mods.tex.

The first step is to create the headers:

```tex
\def\RHevenleft{\ifx\pagenumber\relax\else\pnum\pagenumber\pnum*\quad
\|\quad\it\rangeref\it*\fi}
\def\RHoddright{\ifx\pagenumber\relax\else\it\rangeref\it*\quad
\|\quad\pnum\pagenumber\pnum*\fi}
```

The two headers used are the left side on even pages and right side on odd
pages, thus putting the headers on the outside of the pages. In addition, the
left header is the opposite way round to the right header. Thus the left header
starts with the pagenumber and then has the rangeref, while the right header
simply inverts those. This example also uses its own special character style to
style the pagenumber (bold) and then italicises the rangeref.

Why is there an if around the whole thing? In the situation where we turn off
page numbers (`\\nopagenums`), we don't want the | being output (since usually
in that case rangeref returns nothing as well).

This covers most of the Bible well, but what about the glossary. It would be
nice if the glossary showed the first and last entry of a page in its header.
For this we need to set the header just for the GLO book:

```tex
\def\zGLOHeaders{%
    \gdef\RHnoVevenleft{\pnum\pagenumber\pnum*\quad\|\quad
        \it\zcustomfirstmark|type="k"\*\space\emdash\space
        \zcustombotmark|type="k"\*\it*}%
    \gdef\RHnoVoddright{\it*\zcustomfirstmark|type="k"\*\space
        \emdash\space\zcustombotmark|type="k"\*\it*\quad\|\quad
        \pnum\pagenumber\pnum*}%
}
\def\zNoGLOHeaders{\gdef\RHnoVevenleft{}\gdef\RHnoVoddright{}}

\setbookhook{start}{GLO}{\zGLOHeaders}
\setbookhook{after}{GLO}{\zNoGLOHeaders}
```

We define the headers in a macro so that we can run the macro at the start of
the GLO book, and then run another macro to clear them at the end. The macro
defines two headers: left for even pages and right for odd pages. The same as
for the main scripture text. But since we aren't in a scripture text we use the
`noV` headers. Notice that we use the `after` hook to turn off the headers. This
is because the `after` hook runs as late as possible, after any final page
content has been output.

The contents of the header is similar to the main headers, but instead of a
rangeref, we need to query some marks. TeX has a system of marks which can be
inserted anywhere on a page, and contain text that can be queried for. In this
case, the TeX macros magically capture the contents of the \\k entry into a mark
called `k`. We can then ask for the first mark and last mark on the page in the
header.

## Glossary keyword headers

In the glossary book it can be helpful to have the first and last keywords on a
page in the running headers. This snippet implements that.

The macro consists of a macro to define the running headers at the start of the
book with another macro to undefine them again at the end.

```tex
\def\zGLOHeaders{%
    \gdef\RHnoVevenleft{\pagenumber\quad\|\quad \it
        \zcustomfirstmark|type="k"\*\space\emdash\space\zcustombotmark|type="k"\*\it*}%
    \gdef\RHnoVoddright{\it\zcustomfirstmark|type="k"\*\space\emdash\space
        \zcustombotmark|type="k"\*\it*\quad\|\quad \pagenumber}%
}
\def\zNoGLOHeaders{\gdef\RHnoVevenleft{}\gdef\RHnoVoddright{}}

% Turn on Glossary headers at start of GLO and turn them off at the very end of the book
\setbookhook{start}{GLO}{\zGLOHeaders}
\setbookhook{after}{GLO}{\zNoGLOHeaders}
```

### Implementation

TeX has a system of marks which can be inserted anywhere on a page. Then one can
query for the value of the first or last mark on a page. We query the `k` mark
using `\\zcustomfirstmark|type="k"\\*` for the first mark and
`\\zcustombotmark|type="k"\\*` for the last mark. The PTX TeX macros kindly
insert the mark for us for every occurrence of `\\k`.

Notice that the macro uses the `\\it` style for the keyword. This may be adapted
to taste. Likewise the pagenumber may be put into a different header location,
etc.

To hook the running header definitions into the typesetting, we define a hook to
be run at the start of the GLO file which defines the headers which will be used
in the book. Notice that we use the `noV` type headers since there is no verse
text in a GLO file. Likewise, after the GLO book finishes, we run a macro to
undefine the header macros.


## 3 Column Concordance

This snippet assumes a concordance has been created in the XXS book using
Concordance Builder (which comes with Paratext).

It is not uncommon to set back of the bible concordances in 3 columns. But note
that while that means it takes up only half the number of pages a 2 column
concordance does, the text often needs to be half the size. One way around the
smaller point size is to generate the concordance with a narrower column width.

There is quite a bit to do in this snippet. First we have to restructure the
output XXS to something that PTXprint would prefer to work with. Second we have
to set up the styles and third we have to capture the components of a line to
lay them out appropriately.

### Implementation

Here is a typical changes.txt that someone might use for a concordance (whether
2 or 3 column):

```perl
sections ("initial")
"//\\t " > "\\pz \\zpa ~ "
"//" > "\\pz "
"\\t " > " " 

"\\zpa-xb " > "\\zpa "
"\\zpa-xb\*"> ""
"\\zpa-xc\*" > ""
"\\zpa-xc " > "\\zpb "
"\\zpa-xv\*" > "\\zpb*\\zpa*"
"\\zpa-xv " > ""

"\\c .*?[\r\n]" > ""

sections ("default")
'(\\id.*?\n)' > '\1\\threebody\n'
# '\\s ' > '\n\\r\n\\zrule|width="1.0" align="c" thick="0.5pt" color="0.5 0.5 0.5"\\*\n\\s '
'\\ip.*?\n' > '\n'

"\\p " > "\\s2 "

"See Also" > "~\u2003\u2192 "
```

The first line `sections ("initial")` tells PTXprint to process these changes
before parsing the USFM into USX. We put these changes here because we want to
change some of the markers and don't want to have to define the old markers that
are being changed in our style sheet just so that the USFM parser can be kept
happy. The output from Concordance Builder (CB) is quirky and each line is
simply a suggested line break on the previous line. It would be much more
sensible to have a paragraph for each entry line. So we convert each line to a
`\pz` paragraph. Notice that if the line starts with a tab (indicated by the
special marker `\t`) we simply say that this starts the book name entry as a
space. A reference is held in a `\zpa` character style and the chapter verse
part in a sub character style (\zpb). Thus for example the first line becomes
the second in:

```tex
//\t \zpa-xc 6\zpa-xc*:\zpa-xv 7\zpa-xv*\t vālek būtkun teṇḍsi pūḍle \bd //adikār\bd* sītor.

\pz \zpa ~ \zpb 6:7\zpb*\zpa* vālek būtkun teṇḍsi pūḍle \bd adikār\bd* sītor.
```

The next lines in the initial section convert the zpa-xb, zpa-xc, and xpa-xv
marked text into the zpa, zpb structure I have preferred, as can be seen in the
example above. Finally we remove any chapter markers because who needs those?

The default section is where we do our typesetting. We insert the `\threebody`
marker to indicate that we want this book typeset in 3 columns. If you want two
columns, you don't need this line. There is an example if inserting a line
above headings commented out. We also delete the spurious introductory paragraph
added by CB. Of course if you put real content there, then you don't need this
line.

The XXS file uses `\p` to mark the keyword heading for each group of cross
references. This would be better as a header, so we convert it to '\s2`, but you
can use whatever subsection marker you want. We also convert the string "See
Also" into a wide space followed by an arrow which works better across
languages.

Now we can start typesetting. Bear in mind that some styles (e.g. `\s2` here)
may need to be styled just for the concordance. This can be done by creating a
new style with a prefix as in `id:CNC|s2` thus protecting the existing `\s2`
style that may be used elsewhere. We will also want to use a much smaller text
size for the '\pz' and '\s2' paragraphs, especially if we are typsetting in 3
columns.

### TeX

In our example we would like to style the reference with the book on the left
and the CV on the right. This means that the book stands out and if there is no
book, the CV has a natural position against the entry text. First some
TeX:

```tex
\sethook{start}{zpa}{\hbox to 4.5em\bgroup}
\sethook{end}{zpa}{\egroup\hskip 0.3em}
\sethook{start}{zpb}{\hfil}


\def\zCNCHeaders{%
    \gdef\RHnoVevenleft{\trace{ma}{header
left}\pnum\pagenumber\pnum*\quad\|\quad
\it\zcustomfirstmark|type="k"\*\space\emdash\space\zcustombotmark|type="k"\*\it*}%
    \gdef\RHnoVoddright{\it\zcustomfirstmark|type="k"\*\space\emdash\space\zcustombotmark|type="k"\*\it*\quad\|\quad
\pnum\pagenumber\pnum*}%
}
\def\zNoCNCHeaders{\gdef\RHnoVevenleft{}\gdef\RHnoVoddright{}}

% Turn on Glossary headers at start of CNC and turn them off at the very end of
% the book
\setbookhook{start}{CNC}{\zCNCHeaders}
\setbookhook{after}{CNC}{\zNoCNCHeaders}
```

This snippet does two things. The first three lines position the book and
reference to the left of the entry text. The first line says to create a box
4.5em wide and collect the contents of the `\zpa` character style. The value
4.5em is something you will probably need to change according to the maximum
width of a reference. We use em as the units here so that the box size is
somewhat resiliant with respect to overall text size changes. The second line is
what closes off this box and ensures a suitable gap between the reference and
the entry text. The third line says that on starting the CV part of the
reference insert a space filler that pushes the book and CV parts apart.

The second part of the TeX code provides the running header content.  This code
is identical to that found in the Fancy Headers snippet above with just GLO
changed to CNC.


## Coloured diacritics

PTXprint includes code to process the generated xdv file between its creation by
TeX and its being converted into PDF. This allows us to support other
`\specials`. One such set of specials allows for the colouring of particular
glyphs in a font. This can be used to colour diacritics, for example.

First, PTXprint needs to be told to turn on the extra xdv processing. Since this
slows the printing chain, it is worth only enabling it when needed. This is done
by enabling extra xdv processing on the finishing page. The following snippet
shows how diacritic colouring might be enabled in verse paragraphs:

```tex
\input ptx-arab-colouring.tex
\def\dialist{PATone PAVowel}
\def\diastart{\special{ptxp:diastart \dialist}}
\def\diastop{\special{ptxp:diastop \dialist}}
\catcode`\@=11
\sethook{before}{p}{\marks\m@rknumc@l{\diastart}\diastart}
\sethook{after}{p}{\marks\m@rknumc@l{\diastop}\diastop}
```

There are a number of diacritic lists declared in ptx-arab-colouring.tex and we
will use some of them. We list them by defining a macro with a list of them.
Then we create macros with the specials we will need later. We hook into the
styling system by inserting the special before the paragraph starts. We also
need to place the special in a mark so that it will be inserted at the start of
each column. This is important since XeTeX outputs columns in a left to right
order, even if the text is right to left, thus outputting column 2 before column 1.
And of course, we need to clean up at the end of the paragraph.

Alternatively you may want to colour the whole file (if scripture) as in:

```tex
\input ptx-arab-colouring.tex
\def\dialist{PATone PAVowel PAHonorific}
%\special{ptxp:diacolour PAVowel 0.9 0 0}
\def\diastart{\special{ptxp:diastart \dialist}}
\def\diastop{\special{ptxp:diastop \dialist}}
\addtostartptxhooks{\ifscripturebook\diastart\fi}
\addtoendptxhooks{\ifscripturebook\diastop\fi}
\sethook{start}{nd}{\special{ptxp:diapause}}
\sethook{end}{nd}{\special{ptxp:diaunpause}}
```

Every file we check to see if it is scripture and if so turn on diacritic
colouring and off at the end of the file. Also, we want to colour the name of
deity and pause the diacritic colouring for that word. No need for column marks
here.

### Implementation

The real work of colouring the diacritics is done in a special xdv processor.
XeTeX produces a DVI file with an extension of .xdv. This is an intermediate
format between XeTeX and PDF. All the glyphs and their positions and special
instructions are in this file. When the extra xdv processing is enabled,
PTXprint processes this file to use the ptxp:dia type specials to insert
colouring specials around the glyphs to be coloured, which, in turn, when the
xdv is converted to PDF end up with coloured glyphs.

There are 6 specials that the process interprets:

**ptxp:dialist** has a first parameter of a diacritic list id (e.g. PATone).
Then follows a list of glyphs, these can be glyph names as found in the font,
numeric glyph ids (not sure why anyone would use these) or `U+` followed by a
USV in hex and even a range of USVs by `U+` usv `-` usv, which includes the
inclusive range of unicode codepoints. Notice that the list is turned into the
actual glyph ids when we know what font we are using. The diacritic lists are
designed for sharing between jobs. The glyph names used in such lists are very
font family specific and may require the input of the font designer of the font.
Fonts can ligate diacritics with bases, which makes it impossible to colour just
the diacritic. So not all fonts and sequences may work well.

**ptxp:diacolour** this has the same first parameter as ptxp:dialist. Then
follows the parameters for a `colour` special, which can be `rgb` and 3 floats
between 0 and 1. inclusive for red, green and blue. Or `cmyk` and 4 floats for cyan,
yellow, magenta and black. This allows a particular dialist to be coloured
differently in different jobs.

**ptxp:diastart** is followed by a list of diacritic list ids and enables them
until they are disabled.

**ptxp:diastop** is followed by a list of diacritic list ids to be disabled.

**ptxp:diapause** turns off all diacritic colouring but remembers the settings
ready to turn them back on again. This means that if there is no diacritic
colouring active, then nothing gets turned on and off.

**ptxp:diaunpause** turn back on the diacritic colouring for the corresponding
balanced ptxp:diapause. These pair using a stack.


# Python scripts
The scripts in this section are to demonstrate the kinds of things that are
possible by calling an external script file (.py) and may be enabled by 
the option 'Process Text by Custom Script at start/end' on the Advanced tab.

## Process a file before/after PTXprint has processed it

### Line by line

When you need to call an external script to apply changes to the
input file prior to, or even after PTXprint's internal changes.
This handles the input file one line at a time which is fine 
unless you are performing multi-line find/replace operations.

```py
import sys
with open(sys.argv[2], 'w', encoding='utf8') as outf:
    with open(sys.argv[1], encoding='utf8') as inf:
        for l in inf.readlines():
            outf.write(l.replace('a', 'A'))
```

## Process a file before/after PTXprint has processed it

### Entire file at once, and using the 're' module

When you need to call an external script to apply changes to the
input file prior to, or even after PTXprint's internal changes.
This handles the input file in one go using a couple of RegEx 
substitutions that can also handle multiline changes (flags=re.M)

```py
import sys, re
with open(sys.argv[2], 'w', encoding='utf8') as outf:
    with open(sys.argv[1], encoding='utf8') as inf:
        t = inf.read()
        t = re.sub(r'<<\n', '\u00AB', t)
        t = re.sub(r'\n\\m >>', '\u00BB', t, flags=re.M)
        outf.write(t)
```

