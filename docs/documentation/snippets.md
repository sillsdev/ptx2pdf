This document exists because not everything that people might want to do is made available 
in PTXprint via the UI. So this file contains a structured list of code snippets which can 
be copied and pasted into the appropriate settings files. There are 4 sections:

* RegEx snippets
* TeX snippets
* Python scripts
* Other techniques

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

Use a horizontal rule (line) after the introductory outline, before the 1st chapter.

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

## Add an alphabetic section header to Strong's reversal index

Just for the XXS book, insert the first letter of each section of verncular renderings
before the block of renderings with their Strong's H and G numbers.

```perl
at XXS "(\\m ?\r?\n(.))" > "\\s - \2 -\n\1"
```

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

## Tabbed indent for glossary or index

When typesetting an indented list, such as a glossary or Strongs index, it looks
neater if the main body starts at the same indent position as the rest of the 
paragraph. In this example, the Strongs number is in bold \\bd ... \\bd\* and
we can add a 'tab' after the Strongs number to make things line up neatly.

```tex
\sethook{start}{bd}{\setbox0=\hbox{9999}\hbox to \wd0\bgroup}
\sethook{end}{bd}{\hfil\egroup}
```

## Display paragraph markers next to each paragraph

A typesetter may use changes.txt to change the paragraph style for typesetting
reasons. It can be helpful to know which paragraph styles are being used for
each paragraph. This snippet adds that capability.

Notice that you will need to define a **character** style called zpmkr to style the marker
text.

[Note that this approach is currently buggy, as it changes the output in certain situations.]

```tex
\catcode`\@=11
\input marginnotes.tex
\newcount\pcount \pcount=0
{\catcode`\~=12 \lccode`\~=32 \lowercase{
\gdef\parmkr{\setbox0=\vbox{\hbox{\ch@rstylepls{zpmkr}~\m@rker\ch@rstylepls{zpmkr}*}}%
    \advance\pcount by 1
    \d@marginnote{0}{\the\pcount}{zpmkr}}
}}
\addtoeveryparhooks{\parmkr}
```

## Forces better calculation of the number of lines 

Sometimes when your apply a +1 to a reference in an AdjList, it ends up doing a +2.
To prevent this unwanted behaviour, you can force a more fine-grained adjustment at
the specific verse location.
```tex
\setcvhook{LUK7.48}{\pretolerance=1}
\setcvhook{LUK8.1}{\pretolerance=100}
```

## Table of Contents right-align column 2

```tex
\deftocalign{2}{r}
```

## Set a larger space before footnote caller in the text

If the space before a footnote caller (defined by style zcf) needs to be
increased, then this can be done by adding the following line.

```tex
\sethook{start}{zcf}{\hskip 0.1em}
```

## Move the qr word up to the end of previous line (if space permits)

Used in poetry and/or song books to allow a short qr word to
move up to the previous word as long as there is adequate space 
(defined here as 0.3em) between the end of the last word, and the
qr word, like 'Selah'.

```tex
\sethook{start}{qr}{\unskip\nobreak\hfill\penalty50\hskip0.3em\hbox{}\nobreak\hfill\hbox\bgroup}
\sethook{end}{qr}{\egroup}
```

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

# Python scripts
The scripts in this section are to demonstrate the kinds of things that are
possible by calling an external script file (.py) and may be enabled by 
the option "Process Text by Custom Script at start/end" on the Advanced tab.

## Process a file before/after PTXprint has processed it

### Line by line

When you need to call an external script to apply changes to the
input file prior to, or even after PTXprint's internal changes.
This handles the input file one line at a time which is fine 
unless you are performing multi-line find/replace operations.

```py
import sys
with open(sys.argv[2], "w", encoding="utf8") as outf:
    with open(sys.argv[1], encoding="utf8") as inf:
        for l in inf.readlines():
            outf.write(l.replace("a", "A"))
```

## Process a file before/after PTXprint has processed it

### Entire file at once, and using the 're' module

When you need to call an external script to apply changes to the
input file prior to, or even after PTXprint's internal changes.
This handles the input file in one go using a couple of RegEx 
substitutions that can also handle multiline changes (flags=re.M)

```py
import sys, re
with open(sys.argv[2], "w", encoding="utf8") as outf:
    with open(sys.argv[1], encoding="utf8") as inf:
        t = inf.read()
        t = re.sub(r"<<\n", "\u00AB", t)
        t = re.sub(r"\n\\m >>", "\u00BB", t, flags=re.M)
        outf.write(t)
```

# Other Techniques

## Creating a fancy front cover with ornaments

This is still a very experimental process, which will hopefully be streamlined
through the PTXprint UI in the near future.

Step 1: Wrap the front cover matter text and logo etc. with this milestone:

```
\esb\cat frontcover\cat*

     [your front cover content markers would be in here]

\esbe
```

Step 2: Paste the keyword 'ornaments' into the Plugins box (on the Advanced tab)


Step 3: Place this snippet into ptxprint-premods.tex

```tex
\stylesheet{standardborders.sty}
```

Step 4: Put these lines in ptxprint-mods.tex

```tex
\SwitchOrnamentsFamily{pgfhan}
\SwitchOrnamentsFamily{vectorian}

% You can either use a GraphicOrnament
% \GraphicOrnament{400}{../../../shared/ptxprint/FullBibleWithFRTmatter/corner_hires.png}
%  OR
% You can use the OrnamentTest.ttf FONT which needs to be in the 
% C:\My Paratext 9 Projects\{PrjID}\shared\fonts folder
\StringOrnament{400}{OrnamentTest}{A}
```

Step 5: Place this block into the ptxprint-mods.sty file:

```tex
\Marker cat:frontcover|esb
\Position Fcf
\BoxPadding 0
\BorderHPadding -50
\BorderVPadding -55
\Border All
\BorderStyle ornaments
\BorderPatternTop 400|||8.0,0||*a,400|h||8.0
\BorderPatternBot 400|v||8.0,0||*a,400|d||8.0
\BorderPatternLeft 0|l|*a
\BorderPatternRight 0|r|*a
\BorderLineWidth 1
\BorderWidth 16
```