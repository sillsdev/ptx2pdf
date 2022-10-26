[+d_setup]::

## Initialising

The first file to be loaded is `paratext2.tex` and it has some initial
definitions and set up that it does. The macros make extensive use of
bidirectional controls and for this we need ETeX and its extensions. This is a
prerequisite and therefore all other ETeX extensions are also available to us.
We also follow the LaTeX convension of using the `@` in internal tokens since
outside of the macros we turn off `@` as a letter, making such tokens
inaccessible. `\expandafter` is a long name for this token and can often occur
very frequently in a short space. It is easier to have a short name for the same
thing. Having a local temporary `if` is useful.

`MSG` is for writing messages to the user. `TRACE` was used in the earliest
debugging, but has been largely replaced by `trace` and `tracing`. But some uses
still persist.

The following two `if`s need to be declared early because they are used during
the declaration of other macros.

[=c_pt_intro]::

Files are timestamped in the cropmarks, if enabled.

The timestamp is not recalculated each call. It is calculated once at the start
of the run.

[=c_timestamp]::

All the other files in the PTX macros system are pulled in early into
`paratext2.tex` before the rest of macros are defined. This allows them to
include their own initialisation early. In some cases, the order in which files
are included is important.

[=c_imports]::

A final setup is to have some fall back fonts defined. It is fully expected that
jobs will override these definitions later:

[=c_fonts-basic]::

### Hooks

The PTX macros have an extensive set of hooks which are token lists that are
executed at appropriate points in the processing.

[=c_define-hooks]::

A CV hook is executed when the verse milestone occurs. The identifier takes the
form of BK1.2 and is based on exactly what the verse milestone value is. The
book is whatever is the book id.

[=csty_define-hooks]::

There are also diglot hooks:

[=cdig_define-hooks]::

Within the style system there are style specific hooks that run at different
points in style processing: before, start, end, after. 

[=csty_sethook]::

Style category (see later) and diglot-side specific hooks are processed in a
defined order, from most general to most specific for the opening markers (before and start),
and the reverse order for the closing markers (end and after).
* Marker
* Diglot-side, marker
* Category, marker
* Category, diglot-side, marker
* and so on.

Thus each of the four points could potentially have several hooks associated with
it, with the more specific hooks able to undo or override changes made by less
specific ones. The code for the opening and closing hooks has been merged, into
`\fillh@@ks` which fills a tokslist using the `\p@ssHooks` list starting at the
csstackup or csstackdown routines appropriately.
For opening hooks (`\op@ninghooks`), the task is simply to executes this token
list and empty it. 
For the closing hooks (`\cl@singhooks`) the situation is a bit more complex. `after` 
hooks must be *defined* while the current paragraph or character style is known, 
but only *executed* after the enclosing group has been exited. 
The final addition to this token list (1) ensures the list is emptied, again globally.

The code (2) checks to see if the token list has actually been necessary (i.e. is 
this an `after` hook) and if not executes the token list, thus keeping code in 
other parts of the macros a little cleaner.

[=csty_hooks]::

### Declarations

Various useful declarations. The parargraph types and positions:

[=cpar_strings]::

From notes we declare `+` and `-` letters:

[=cnote_declare]::

For figures we declare various strings to compare against:

[=cfig_declare]::

### Utility Functions

There are numerous utility functions spread around the code.

When processing USFM text we treat numbers as letters. This protects us from
accidental calculations, etc. We have macros for switching the interpretation of
digits.

[=csty_fndigits]::


### Tracing

The PTX macros have a tracing mechanism by which tracing can be added to any
job. There are various different log traces that are available and a job may
enable as many as it wants. Each trace has an identifier.

[=tracing-codes]::

Within the code, text may be output to a trace using the `\trace` macro that
takes an identifier and the text to output. A user configuration may use the
`tracing` macro with an identifier as its parameter to enable that trace. Each
trace state is held in a token and when `\trace` runs it tests the token for its
identifier to see whether to write out the text or not. If no tracing is enabled
then the whole mechanism is short circuited.

[=tracing]::

## Running

Here we examine the processing of a USFM file. The first step in loading a USFM
file is to do any one time setup. Such setup occurs before the first file is
processed but is also blocked from executing again before any other files in the
job.

### One Time Setup

This code is run once, since the definition is overwritten at the end (1). It
calls various other setup macros which we will examine here. We capture the
current baselineskip as being the default baselineskip for the document. Then we
call the various setup macros and also various hook setup routines. Then we set
a flag to say that we are inside a USFM file. Now we can call the job `init`
hooks.

[=csty_onetime]::

First we set up various sizes. Setting the body baseline involves setting the
baselineskip and the `\le@dingunit` and the vertical space unit. If the
baselineskip is too small then set it to $14 * {\rm LineSpaceFactor} * {\rm FontSizeUnit}$.
The LineSpaceFactor is usually 1.0 which given the fontsize for `\p` is
typically 12 in the stylesheet, gives us a text size to leading of 12 units on
14 units where units are the FontSizeUnit. If the `baseline` parameter for `\p`
is not set, then set it. This applies to diglot sided versions too.

So to set up sizes we set up the baselineskip and set `lineskiplimit` to
something pretty hugely negative which means that `lineskip` will not kick in
unless someone asks for that. We set the baselineskip from the `\p` style, even
if we've just set it. We set the amount of space to add to the top of a column
to be a baseline. We calculate the gutter width and the total textwidth
available to us. We also calculate the width of a double column column. We do
the same for the diglot column widths. We set the actual textwidth (`hsize`) to
be the single column width minus 2 columnshifts. `columnshift` is usually 0 for
single column text, so this is merely calculating how much text width we have
for 2 columns or 1 single column. We calculate the real margin dimensions and
from that the textheight, which we then set as the page breaking page height. We
set up the physical page size for the PDF file and then reset the vsize to
textheight.

[=csty_setupsizes]::

There are a number of special case USFM markers that do more than simply switch
styles and style types. These often need special handling. We declare them here.

The whole definition is grouped in a group with `\obeylines` to enable us to
access `^^M` end of line character. `\h` is used to indicate the book name as
printed in headings and elsewhere. Since we are collecting a string, we turn off
all the active characters and then use pattern matching to capture the rest of
the line as the book name. Which variable is set depends on diglot sides.

The `\cl` chapter label has two modes of usage. If it occurs anywhere than
between a `\c` and the following paragraph start, it is treated as a global
setting. Otherwise it is simply a paragraph style that clears any drop chapter
number. Collecting the chapter label globally is almost identical to processing
`\h`.

The `\id` line is generaly useful to collect, particularly to output as part of
any cropmarks. In addition we collect the first up to 3 characters as the book
id. Again we do the same trick for handling the id line. In addition we convert
space back to its normal interpretation and so any initial or final space will
be ignored.

`\fig` simply captures its contents and then calls `\d@figure` with that
contents (1). `\nb` is a special non-breaking paragraph marker and needs special
handling which we redirect to here.

[=csty_addspecialhooks]::

### Processing USFM

Reading a USFM file involves setting up for a new book. We start by ensuring
that one time setup code is run and if creating a diglot we set up the various
baselines for the left and right text.

Which routine to use for gridding a box. There is a diglot specific one and one
for when we want to lose extra space at the top of a column and one for when we
want to keep it. The user can set `squashgridboxfalse` to keep the extra space.

We then clear the chapter labels and clear the style stack. Initialising the
paragraph styles involves clearing all the flags for which type of paragraph we
are in now:

[=cpar_init]::

And initialising the notes involves clearing all the note boxes and supporting
skips, etc.

[=csty_ptxfile_intro]::

Now we can load the file. But with each usfm file there may be associated
supporting files. There is the paragraph adjustments file and the pictures list
file that a user may create. Also there is the picture pages file that says
where every picture is in the job and we reload that for each file.

A USFM file is not a TeX file and so many of the characters do not have the same
interpretation in a USFM file as they do in a TeX file. Most characters are
treated as `other` meaning that they are just treated as text with no special
interpretation. `~` is treated as active since it usually means a non-breaking
space. `_` is treated as a letter so that it may occur in SFM markers. `/` is
active in that a double slash is treated as a line break while a single slash is
just that.

[=csty_slash]::

We also turn on all the active characters because we want to process them in the
text. Digits become letters (since we don't want to do any maths with them). Now
we open the file. If it is at the end of file, i.e. it failed to open, then our
action is to report the fault. Otherwise our action is to have TeX interpret the
file. OK do the action!

[=csty_ptxfile_start]::

Once the file is processed we need to tidy up. We close any open character
styles and stop skipping any text. We finish any open tables and close off the
diglot. We run any `bookend` hooks. And then we undo all our character setup for
reading the file. We make digits digits again. We get back our comment character
and turn off special characters. We give back characters their normal TeX
interpretation. If we processing the last file in a job then we close the
piclist, otherwise we keep it open until the next job starts. We close the
adjustments list file and reset more characters. We go to single column and
force a page break. This page break may not actually result in a page break if
we are running books together. If we are forcing a true break, then we shipout
any partial box remaining and clear up from that. Finally we simply say: we are
in single column normal text mode now. And with that we return to the driving
.tex file.

[=csty_ptxfile_end]::


[-d_setup]::
