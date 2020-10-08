[+d_milestones]::

Milestones do not fit into the style hierarchy since they do not style text so
much as insert text at a point in the document. They have no concept of opening
and closing since they are a single event. The primary two milestones we examine
are chapter and verse markers.

## Chapters

We define the `\c` macro as part of the one time setup that runs when the first
sfm file is processed.
Most chapter numbers are a drop number. What makes scripture typesetting tricky
is that there are a few drop chapter numbers that occur mid paragraph. Since
USFM says that paragraphs occur under a chapter marker. There is a special
paragraph marker for the non paragraph break: `\nb`. To achieve the cutout we
have verious things to set up in the chapter marker itself. We start by
squirrelling away the `\c` paragraph style. After this, there are two parts
to the chapter marker processing. We
start with the pattern matching chapter that collects the chapter number and
processes it.

If we are currently not outputting any text, due to it not being publishable,
for example. we are in a dumping group. We need to close that group for now and
get back to normal paragraph land. We collect the chapter number for references.
We also collect the chapter number text (e.g. from `\cp`) for output. We clear
the verse number since we are at the start of a chapter. If we omit chapter
numbers then we are done. Otherwise, if there is a chapter label then use the
appropriate one for diglot and output the `\cl` paragraph style with the chapter
label followed by the chapter label text.

The actual `\c` macros is pretty simple. We make digits into digits and call the
pattern matching chapter macro. We also define `\cp` to simply pattern match and
capture the chapter number as the chapter number text.

[=csty_chapdef]::

### Drop chapter number size

Drop chapter numbers need to be of the right size and users almost never get the
number right. It is better to calculate it. But calculating the proper
size of a dropped chapter numbers is tricky. The aim is to have a chapter number
that stretches from the baseline on the second line to the top of the x-height
of the first line. But if the digits have descenders then we need to test
whether the descenders will go below the descender of the second line. If so
then we calculate the drop chapter to fit into the space range from the
descender of the 2nd line to the ascender of the 1st line, and then shift them
to fit.

We start by getting the currently specified fontsize for dropped chapter
numbers. Then we find the ascent and the descent of the main paragraph font
(in box1) (1). We also get the
vertical metrics of all the digits in the chapter font at the fontsize for the
chapter marker. Notice that to get the
font metrics we tell XeTeX to give us those. Then we switch to have XeTeX give
us true glyph metrics. We clear out the chapter font in anticipation of
recalculating it with a new size. Then we get the x-height of the paragraph
text (2). Now we have all the external numbers needed to calculate the drop number
size.

TeX does fixed point calculations in sp with 1pt having a value of 65536.
The problem with this is if you divide two dimensions you get an integer
division, which is often not very useful. To increase accuracy, we multiple up
by 128 (giving a maximum dimension of 512pt which should be enough for 2 lines
of text). This means keeping track of when we multiply, values are in effect
mulitplied by $2^{16}$ and if a number that is multiplied by $2^{16}$ is divided by
another number multiplied by $2^{16}$ then the result has no multiplier, and so on.
Multiplying numbers by 128 for extra accuracy can either result in having to
divide the result by 128 or multiply it by $512 = (2^{16} / 2^7)$.

The calculation is in 3 sections. The second section does a default calculation
of the new chapter size needed to get the height of the digits to fit from the
baseline of the second line to the x-height of the first. The first section
calculates a notional height to pass into that scaling. In the normal case where
there is no depth to speak off, this value is the height of the digits. But if
there is a problem, then we scaled the height of the digits such that the final
result comes out being the total height from the descender of the second line to
the ascent of the first. The final section calculates any shift needed for
digits with large depths.

(2) First we calculate X, which is the distance from the baseline of the second
line to the top of the x-height of the first line. And then we calculate X/C *
128. We also calculate height T, the distance from the second line descender to
the first line ascender, based on what the font says about ascenders and
descenders. Next we need CX/T (where C is the point size specified by the
chapter style). This is the height the digits would have to be to fit into T
rather than X. We also calculate the maximum depth of the digits scaled if
the maximum height was scaled to fit with top x-height.

If CX/T is less than the maximum height of the digits, or if there is
insufficient room below the baseline for the scaled depth, then use the CX/T to
scale. Otherwise use the digits height. (3) This is then scaled such that height
will stretch from the baseline of the second line to the x-height of the first line.
We know that the whole thing will fit, but we may need to shift the number if
the descender would clash with the line below (4). We calculate what the shift is.

The dropnumbersize dimension is converted into a string so that it can be stored
as the `\c` font size, as if it were specified in the .sty file.

For diglots we need to store the drop chap number size for each side. _There is
work to be done here_

[=csty_dropchap]::

### Stripping pt dimension

One of the trickier processes in TeX is string processing. This is because TeX
doesn't work in terms of strings, but of tokens. The text TeX reads is broken
into tokens and tokens have category codes. So a token `a` with catcode 12
(other) is a different token to the token `a` with catcode 11 (letter).

The `\the` command in TeX can be used to expand out many things, including a
dimension. The TeXbook says that the output of `\the` is a sequence of tokens
each with catcode 12. Thus a dimension is a sequence of tokens corresponding to
the size of the dimension in points followed by `p`~12 and `t`~12. If we want to
strip off the `pt` to get back to just a string that can be output say in a
`\special`, then we have some processing to do.

This code has to use quite a few TeX processing tricks to do what is basically a
very simple string processing job. The core is `\@strip@pt` which consumes
everything after it up to the first `p`~12 `t`~12 as parameter 1. Everything
after that is stored in parameter 2 up to the sentinel `\E`. The sentinel can be
any defined token.

What makes the definition of this macro tricky is that normally `p`, in TeX
code, has a catcode of 11. So how do we use both a `p`~11 in the macro name and
`p`~12 in the parameter pattern match? The trick is to use the `\lowercase`
macro that lower cases everything within it, while not changing its catcode.
Thus, since we don't need the letter `P` for any other purpose, we can
temporarily give it a catcode of 12 (also for `T`) and then use them in the
parameter pattern. Then we lower case the whole thing and we get what we want.

But, this is not sufficient for our needs. Passing the output of `\the` to our
new macro is no easy feat. So to make things easier we write a macro that calls
`\the` and passes its output to our `\@strip@pt`. This involves expanding all
kinds of things. Starting from the right hand end, we need to expand `\@pt` to
get the fallback `p`~12 and `t`~12 in case they are not in the output of `\the`.
We also need to expand `\the #1` to get the text of the passed token. The result
is that scary looking `\strip@pt` which gets used in `\special` commands.

[=csty_strippt]::

### Making a chapter box

When a paragraph starts with a drop chapter number we need to make a box for the
chapter number. For this we need box metrics to be based on the glyphs themselves
and not on the font metrics. We then create a default macro for printing the
chapter number. There is a user defineable hook `\PrepChapterNumber` that can
redefine that `\printchapter` macro to style the chapter number text
appropriately. Then we create a box with the font set to the drop chapter size
and font and print the chapter number.

If the chpater needs to be rotated, for example, for vertical text, then we do
that here. In a vertical context, we still want the chapter numbers to be
presented horizontally across two lines. To do this we have to rotate the
chapter numbers so that when the whole page is rotated, they end up horizontal
again. In addition, the space after the chapter number, therefore, has to come
under the chapter numbers. In our calculations:

dimen value
----- -----
 0    Height of the chapter box. The width of the new box
 1    Height + depth of chapter box plus `\AfterChapterSpaceFactor`. The height of the rotated box 
 2    Half the heigh - width of the chapter box. The amount to shift the chapter box

Then we create the box and rotate it. Then we set the height of the box to the
width of the chapter box and the width to the new height, because height and
width get swapped in anticipation of rotation.

Otherwise and normally, we lower the chapter box by a baselineskip (adjusted by any
special dropnumber raise) and then insert the `\AfterChapterSpaceFactor`.
Finally we tidy up to set the glyph metrics back to the user setting. We need to
collect the width of the cutout we need to make and we clear any depth to the
box we created.

[=cpar_makechapterbox]::

### Processing chapter in a paragraph

When a paragraph starts, in the `\everypar` macro there is a section that
handles what happens if we have encountered the start of a chapter before this
paragraph started. It first checks that this paragraph is a `VerseText` type
paragraph and not a section header, for example. Then, assuming the text is
publishable, it makes the chapter box. Then depending on directionality, we
choose which cutout function to use.

If there is no left margin, for example in a normal paragraph, we call the
cutout function with the width of the chapter box. Each cutout is numbered
sequentially and when a cutout is made it simply defines the various tokens for
that cutout number. These will be used later in dealing with cutouts.

We also see that cancelling a cutout is as simple as resetting the cutout count.
The cutout count is reset after all the cutouts for a paragraph are processed,
so the count rarely gets very high.

[=ccut_cutout]::

If, on the other hand, there is a margin, for example in poetry (1) then we need
to calculate the actual indent of the first line. If this is less than the width
of the chapter number then we insert a cutout of the difference in width for the
first line and a cutout for the difference in width between the margin (the
indent of the second line) for one line for the second line. There is no need to
do this if the margin is greater than the width of the width of the chapter box.
But if the first line indent is wider than the chapter box then we simply widen
the chapter box to the first line indent 

We can now clear the flag to say there is an outstanding chapter number to
process. If there is no indent at a chapter number then clear the flag to insert
a first line indent. And set that dropped number processing is needed in
subsequence paragraphs. This will get cleared if the paragraph has more than 1
line. Finally output a PDF bookmark for the chapter.

[=cpar_parstyle_chapter]::

Inserting the PDF bookmark for a chapter is only complicated by diglots. The
normal case we output a PDF destination for the bk.chapter and an outline entry
for the book (or id) space chapter.

[=cpar_pdfchaptermark]::

### Dropped chapter numbers in a paragraph

In the rare case that this paragraph follows a single line paragraph containing
a chapter cutout, drop any cutouts in this paragraph and prepare to recalculate.
Againt we choose the appropriate side for the cutout and, as per the chapter
processing above, we test for a margin. With no margin, we simply insert a
single line cutout (since the first line was in the previous paragraph). If
there is a margin, then we find the first line indent. If it is less than the
chapterbox width then insert an appropriately sized cutout just for the first
line. Now that the chapter box has been consumed vertically, we can clear the
dropped number flag. No further paragraphs need get involved in this chapter
number cutout. Also disable hanging verses for this paragraph.

[=cpar_parstyle_drop]::

### Delayed chapter numbers

In many paragraphings of the Bible, there are paragraphs where the chapter break
occurs within a paragraph. This is difficult to model in USFM and instead of
keeping the paragraph unbroken, USFM marks a notional paragraph break and then
starts a special `\nb` paragraph that is special since it carries on the
previous paragraph. This is handled in the PTX macros with a special `\parstyle`
that doesn't actually break the paragraph. Remember that the `\parstyle` macro
has the job of closing the old paragraph as well as starting a new one. We have
the advantage, then of not needing to do either of those actions. Instead we
need to set up for a cutout in the middle of a paragraph, for the chapter
number. Given we cannot be sure that the paragraph will not be broken by a
column or page break, we store the desired position of the cutout in a special
`.delayed` file and reread that in a subsequent run. This means the job needs to
be re run if there is not already a `\.delayed` file (and that that file is in
sync with this file).

After this initial test where we simply tell the user they need to re run, if
necessary, we make sure we are already in horizontal mode and insert a strut (4) to
ensure the line height at this point is appropriate for inserting a chapter box
(1). We are processing the chapter number now, so there is no need to annoy
other paragraphs with this. If the text is not publishable then dump the chapter
box. Otherwise, we make the chapter box and insert the appropriate end of the
line skip after it. Now we look up how many lines down in the paragraph we need
to go to insert the cutout. This gets output during the shipout and so is
measured against the top of the paragraph or column.  Then we make a cutout on
the appropriate side. The cutout is shifted down by the previously read delay.

The actual chapter box is output as a `\vadjust`, which inserts a vbox after
the current line. By setting the vbox to a height of 0pt, it adds no extra
height to the line on the page. Inside the box we have to shift from the current
position after the previous line up by the depth and then further up to the top
of the chapter box. Then we look for any further raise and if so go up by that
or a single line. Then we create a left or right aligned line of the chapterbox
and insert whatever shrink or stretch will keep the box 0 height. Finally we
also we insert PDF outline entries for the book, if needed, and the chapter.

Next (3) we save the position in the output and capture the book and chapter in
a string that we can expand into the `write` command to the paragraph locations
(`.parlocs`) file with the this position in the page. These will get read in on
the next run to calculate the number of lines to shift the cutout down. Finally
we say: the next paragraph may need to deal with a cutout.

(4) A strut is simply a 0 width box with the height and depth corresponding to
the ascent and descent of the current font.

[=cpar_ptxnb]::

## Verses

A verse marker is a milestone and as such doesn't fit the normal character,
paragraph, note style category. It needs special handline. First we keep the
stylesheet `\v` marker definition for when we need to style the verse number
itself. Then we define a pattern matching macro to match the space and the verse
number text followed by a space. The verse number text is normally simply a
verse number, but verse numbers can include briding verses and partial verses.
Only one space is consumed after the verse number text.

The job of this pattern matching macro is to do the work of a verse number. That
is to run any pre verse hooks. Then is splits up the verse number text into from
and too verses. The calling macro may have set `\cancelfirstversetrue` in which
case we assume it was correct and don't output anything. If we are typesetting
vertical text we may want to rotate verse numbers to their horizontal
orientation. We do that here by inserting a hbox and using special commands to
rotate it. Otherwise we take the more normal route. We treat the styling of the
verse number text as a nested character style. We start that style, then print
the verse number, which can include addorning it with directionality and even
putting it inside a figure. And then we finish the nested style.

After that we insert a standard amount of space after the verse number. Notice this
isn't glue because we do not allow a line break here.

The outer calling macro has started a new group for all this styling and we can
close that here. Now that we have output the verse number text, we insert a mark
for the headers and footers, and anything else that wants it, giving the current
reference. Then we run any verse hooks. These differ from the pre verse hooks.
We declare what our current reference is and then insert a magic piece of glue
that is the smallest size possible. [I'm not sure why this is here. 0.5sp is
smaller than TeX can hold and nothing seems to reference it. Is it redundant?]

[=csty_defv]::

When we actually encounter a verse milestone we need to enter horizontal mode
and to do that we need to remember what the current paragraph marker is so that
we can put it back later. The default is to print the verse number (since
usually we not at verse 1). The start of a chapter is marked by setting a
sentinel spacefactor, which we then indicate in the text with a 0 width kern.
Since we are at the start of the chapter we may set cancelfirstverse.

If the paragraph style has marked for a hanging verse number then insert an
`llap` in front of the verse number text. This sits the verse contents to the
left of the left margin. We then open the versenumber text group and call the
verse number text output macro.

[=csty_verse]::

### Hanging Verses

Hanging verses are for indented paragraphs and hange the verse as if the
paragraph had no indent. A typical use is with poetry where the verse numbers
hang left for indented poetry. There are various user controls here. The
starting point for this code is `\printv@rse` (1) which is executed to make a
printable verse number. The usual case is to use `\simpleprintv@rse` (2). This
prepares the from verse number using `\AdornVerseNumber` (3) which allows for
any modification of the verse number. If there is a bridge verse range then
`\simpleprintv@rse` inserts the emdash and the adorned final verse of the range.
The result is therefore a simple string.

For hanging verses we use `\hangprintv@rse`. This does not actually hang the
verse left, that is done higher up, but it prepares the verse number or bridge
for hanging. For a normal, non-bridge verse we simply adorn it and return. But
for bridged verses we want to stack the bridge. We calculate twice the
superscript factor of the baselineskip and we set the baselineskip to the
baseline of `\v` if set. We also calculate the space between the two lines as
the superscript minus the baseline (which is negative).
Then we create a box containing a dash and the final
verse number of a bridge. Then we build a top hanging vbox containing two boxes
on top of each other, the first is the adorned initial verse number, right
aligned. Then we insert the calculated gap between lines and the second box is
the final verse box we just created.

[=csty_hangverse]::

The actual hanging of the verse is done in the definition of `\v` with a `\llap`
prefix that puts the box to the left of the start of the line after the indent.

### Marginal Verses

Marginal verses, on the other hand, are a very different animal. They are set
into the margin of the text. Or in our case a `\columnshift` space that is
inserted at the start of the column. Thus the verse numbers are removed from the
text and then pulled out for easy visual identification. They also limit the
breakup in the flow of the text. Marginal verses are enabled by including the
file `ptxplus-marginalverses.tex` after `paratext2.tex` in a driving .tex file.

First we see how the new code will be integrated into the main macros. We
replace the re-directed `\v` by ptx-stylesheet to our new `\myv`. This much
simpler verse handler copies some of the `\v` in terms of ensuring we are in
horizontal mode and clears cancelling the first verse. If we are at the start of
a chapter then insert the special kern to help `\x`. If we omit verse one then
cancel the first verse. Then we start the group for the verse and set digits
back to digits and call our `\marginverse`.

To hook this in we set up our `\initmyverse` which moves `\@V` away so that we
can use it later and sets `\v` to `\myv` to hook in. This then gets added as an
initialisation hook that executes after ptx-stylesheet cv hook. And we also set
up to use hangprintv@rse to handle verses and bridge verses.

[=cmargin_init]::

The `marginverse` macro is inside a `\lowercase` with handling for space and
`\*`. It collects the verse number text and calls any preverse hooks. It then
splits the verse text into from and to verse components. Then it sets the verse
in the styling for the verse. Then it measures the height of the box plus the
descent of the font. It now redirects `\everypar` since we intend to create a
paragraph. It now does much of the work of `\v` in setting the marks
for the verse and running any verse hooks. It also defines the current
reference. Now it inserts the verse box is a `\vadjust`. Inside the box it sets
the baseline to that of `\v` or the current baselineskip. It now moves the box
up by the height + depth we just calculated and creates a box that is the left
aligned box while removing the boxes to get back to the basic structure of the
two boxes. Then it adds space for the `\AfterVerseSpaceFactor`. It sets the
height of this box to the height + depth calculated. It now says not to insert a
line break and puts the magic space in the text and resets `\everypar`

One macro it does use is a `\marginremovehboxes` which unpacks all the `\hboxes`
in the box.

_This does seem a rather long winded way of doing this_

[=cmargin_verse]::

## Cutouts

The whole handling of delayed cutouts gets involved in various parts of
paragraph processing. We have already seen how the details of a cutout are
defined. Cutouts get inserted at the end of a paragraph.

The objective of the `\makecutouts` routine is to create a `parshape` for the
current paragraph. We start by calculating how many lines go into our parshape.
If there are hanging indents, then start there. Then iterate through all
the cutouts and increasing the line account accordingly. Then we create the
parshape we are building (1). To do this we iterate over the number of lines
just calculated and calculate the indent and width for the line. Thankfully the
width is just the standard width minus the indent (2). For a normal hangindent
line we use the `\hangindent`. But then there is look at the cutouts, which may
modify the indent and width for this particular line. At the end inside the loop
we append the indent and width to the list and outside the loop, set the
parshape.

[=ccut_makecutouts]::

Calculating what the cutout impact on a particular line involves iterating
through all the active cutouts looking for any that impact this line. If one
does then we get the cut width and reduce the width by that width and if the
cutout is on the left, we reduce the indent.

[=ccut_cutthisline]::

Having decided what cutouts may occur on a paragraph, there is also the
question of carrying over any incomplete cutouts from one paragraph to the next.
The routine iterates the cutouts and creates a new cutouts list containing any
incomplete cutouts from the old list. For each old cutout it checks to see if
the cutout needs to carry over, in which case it changes the `after` and `lines`
accordingly (`after` = 0, for example) and replaces them in a new list (which
cannot be longer than the old list).

[=ccut_carryover]::

### Parlocs and Delayed Cutouts

Calculating where delayed cutouts go involves two auxiliary files. The
`.delayed` file contains entries for each delayed chapter number (i.e. `\nb`
paragraph). The `.parlocs` gives the x, y position of the start and end of each
paragraph on a page. It also gives the number of lines in a paragraph that has
a dropped number in it.

Managing the parlocs files are done together. We open the `.delayed` file to
read, and if it is present delay the reading until we have closed the test
opening. Then we may just `input` the file. We don't read the `.parlocs` file
here, we just open it for output. We attach this routine to the list of routines
to run at initialisation

[=cpar_initparlocs]::

Closing up the parlocs file is somewhat the opposite of initialising it. For
this we close the written `.parlocs` file and then set up to read it. We open
the `.delayed` file for writing and then read the `.parlocs` file and process
it, which will write things to the `.delayed` file which we close after we have
finished reading the `.parlocs` file. And we do this at the end of the job.

[=cpar_finishparlocs]::

The next set of macros work together to work out what the delayed parameters
should be for a delayed dropped number. Each routine is called from the
`.parlocs` file.

The `\@parstart` indicates the start of a paragraph and takes the x and y
coordinates of the start of the paragraph. We are only interested in the y
coordinate.

The `\@parend` indicates the end of a paragraph and from this we are only really
interested if there is a pending chapter number. If there is then we assume that
the dropped number position is less than one column from the end of the
paragraph. If we are in the same column then calculate the number of lines from
the chapter location to the end of the paragraph. _(This needs work)_

The macro that actually causes output to the `.delayed` file is `\@parlines`
which lists how many lines are in the cutout. The y value, which is in lines, is
adjusted according to the number of lines needed and then a `.delayed` entry is
written to that file and the pending chapter and book are cleared.

[=cpar_parloccmds]::

When a `\nb` type paragraph is encountered, this outputs a `\@delayedchapter`
entry in the `.parlocs` file and this uses the last paragraph end and chapter
position to insert a cutout half way up paragraph. If the paragraph start is
lower than the chapter position, then assume a different column or page. In that
case collect the book and chapter and then wait for a `\@parlines` to sort
things out. Otherwise do the line calculation and output the delayed chapter
information.

[=cpar_delayedchap]::

Ideally we do not want to change the delayed chapter if we can avoid it because
it will trigger a re-run of the job and that takes time. So we compare the
information we are expected to write against what we read last time. If the
`delay` value, which is the number of lines down, is the same, then we assume
everything else is the same and carry on. Otherwise we test to see if we have
shifted by 1 line. If so then we can use the RaiseChapter to do the dirty deed.
But that triggers a rerun, as does really using the DelayeChapter. And finally
we write out the information to the `.delayed` file.

[=cpar_writedelayed]::






[-d_milestones]::
