[+d_styles]::

Typesetting is nothing if text cannot be styled. The PTX macros have the
concepts of character styles, paragraph styles and note styles (for footnotes,
etc.). In addition styles may be stacked, thus a run of text in one character
style may be embedded in a run of another style, such that anything not
specifically defined in the inner style is interpretted as coming from the outer
style, which may in turn derive the information from an outer paragraph style.

A USFM text is marked up in terms of styled runs of text witch rules about how
runs are closed. Each run starts with a marker that sets up the style.
Internally in the PTX macros, each style marker has parameters associated with
it, e.g. `fontsize` which the macros can then query when they need to set such
things in the typesetting process.

There is also a fourth category of marker in USFM: a milestone. While milestones
may take parameters following them in text, they are not opened and closed,
they simply do their thing when they occur and life continues after them. The
world may be a different place, but they do not create a new style environment
for anything to embed in, for example. Typical examples are `\c` and `\v`.

## Stylesheet

A core principle of character, paragraph and note styling, in the PTX macros is
the use of a stylesheet file, which, being in a SFM format, can simply be
executed as a special kind of TeX file. Stylesheets are executed and the
information in them is stored as parameters on a style marker. The core macros
for defining these use the `\csname` mechanism in TeX to construct a token and
then to define the value of the expansion of that token.

[=csty_defparam]::

The corresponding macro for looking up a parameter is, at its core, very simple.
But the additional needs of diglot processing, where a parameter value is
different depending on which side of the diglot is being processed, add to the
complexity:

[=csty_getparam]::

Now we come to the long list of markers that can occur in stylesheet. We have to
support everything that is allowed to occur in a stylesheet. Unfortunately, if
an unknown marker occurs in a stylesheet, processing stops at that point in the
stylesheet and no further stylesheets will load. We define some key macros to
start with: The `\Marker` identifier starts the definition or additional
definition of a marker. We define a default empty font for the marker and just
collect the marker for use in all future definitions.

[=csty_definition_setup]::

Each marker follows a common pattern of skipping whitespace and capturing the
rest of the line, even if it is expected to be empty or the marker is being
ignored.

[=csty_definitions]::

The `StyleType` marker (1) makes reference to `\m@kestyle` and is the way that
the PTX macros decide what kind of style this is: character, paragraph or note.
Each style type is processed very differently. `\message` is a TeX primitive
that outputs the contents to the console and log file but puts a space after
rather than a newline. We clear any font associated with the marker and then
call the type appropriate definition for the marker. In each case we create a
defintion for the marker token that calls the appropriate style routine. In the
case of character styles we also create a handler for the emebdeed form of the
character style that is prefixed by `+`.

[=csty_makestyle]::

A stylesheet is read and processed line by line (2). We start by ensuring digits
are treated as digits rather than letters. In general, in a USFM we don't treat
digits as numbers, but simply as text that is to be output. But here we need to
store digits as digits so that we can do numeric processing on them elsewhere in
the system. It is very hard to change the category of a token once it is set.
There are markers in the stylesheet
that correspond to various default font markers in the code. We need to store
those current values away and redefine the font marker tokens to stylesheet
routines, at least for the duration of reading a stylesheet. Next (1) we open
the stylesheet file and turn on the 'keep reading' flag. But if the file is
empty or failed to open, we flag an error and don't read the file.

If the file
is good to go we inform the user and tell TeX not to add anything to the end of
each line read. USFM stylesheets use `#` as a comment character. We will do the
same for this file. This means we can't define any macros with parameters for
the moment, but that's fine because we don't want to.
Inside the read and process loop we read a line from the file (2) and then do
that line. If the file is now at its end we clear the keep going flag and if we
are to keep going, we repeat the loop. Once the loop is completed we reset the
end of line insertion; close the file and get back `#` for macro definitions.

Finally, even if we don't read the file, we put back the saved tokens since we
don't need those routines outside of stylesheet reading.

[=csty_stylesheet]::

### Style Categories
A complicating issue for styles is that USFM version 2.1 introduced the concept 
of categories  for `\esb` blocks and `\ef` extended / enhanced footnotes.
Any number of categories may be defined, and it is relatively clear that while
not altering the semantic meaning of the markers, they change the appearence.
I.e. each category potentially represents an alternative set of styles. 

Further complicating issues is that a category is selected once, within the `\esb`, 
`\ef` (and potentially other elements), without any overt end marker. 

Two variables are maintained, the category that the user has typed (```\c@tegory```) 
and the representation of that category as a style-prefix (```\c@tprefix```). At the time
of writing, that prefix is ```cat:\c@tegory|```, i.e. for a category of people and a marker of 
fq, as demonstrated in the current USFM3.0 documentation, the stylesheet entry 
will begin: 
```
\Marker cat:people|fq
```

This category prefix is also used in the style-processing hooks, enabling the specification of 
hook code that is only executed for markers in a particular style, maintaining the principle that 
most anything that can be specified as a marker style can also be specified as a hook.

While not actually a marker style, the hooks normally associated with style marker are run at the 
beginning and end of a category's scope, in the normal manner.  For this to function correctly, 
the ```\cat ...\cat*``` directive must occur inside a simple group[^1].  The footnote code functions as such, as do 
character styles and ```\esb ....\esb*``` groups.

[^1]: TeX has several types of groupings: vbox groups, (various) hbox groups,
  and also so-called simple groups (`{...}` or `\bgroup ... \egroup`) and
  semi-simple groups (`\begingroup ... \endgroup`).  These last two types can both 
  contain macros, text, etc. and behave only slightly differently in some very
  specific contexts (e.g. in typesetting maths). One notable difference is that
  they must nest correctly, or they will trigger an error. 
  This fact is used to ensure that hook code that does not
  balance correctly (e.g. has a `\bgroup` but no corresponding `\egroup`) is
  caught quickly.

The code relies on this in the following way. First, once any before-hooks have
been executed a semi-simple group (1) is entered. Then after the start-hooks, a
simple group (2) is entered, and an `\aftergroup` command provided. 
Assuming there is nothing very strange in the USFM, the simple group from (2) will be 
ended at the end of footnote or end of `\esb` block. Thus we subvert the grouping 
commands provided by other parts of the macros.

This (externally provided) `\egroup` closes the simple group begun earlier (2)
and also triggers the expansion of the `\@ndc@t` macro, which runs the end
hooks,  closes the semi-simple group (3) and finally (4) provides an `\egroup` to
replace the one we borrowed from the external code.

In the case when ```\cat ...\cat*``` is called when `\c@tegory` is not empty (5),
there are two possible scenarios: a category is already defined for the 
present box or a category is currently defined for an enclosing box, e.g. 
this is defining a category for a footnote inside  an `\esb` block. It is
presently considered that a second category within the same level of block is a
violation of the USFM specification. In the case of nesting, no specific action
is needed.

[=csty_category]::


## Character Styles

The lowest level styling is character styling. Paragraph and note styling both
also require character styling. There are two kinds of character styles in USFM
that only differ in how they start and finish. Normal character styles may only
occur inside paragraph styles and when they start, they close any active
character styles. Embedded character styles may occur within other character
styles and are either closed by a closing marker or the start of a new normal
character style. Likewise normal character styles may be closed explicitly with
a closing marker or by the start of a new normal character styles. It is obvious
that a new paragraph style will close all open character and paragraph styles.

There are two entry points for character styles corresponding to their types. In
each case we need to capture whatever comes after the marker, whether it is a
```*```, which indicates a close marker or a space that indicates an opening
marker. We treat end of line as a space here. We set up the catcodes for space
and end of line and then capture the next token (which is immediately after the
marker) and store it in `\n@xt`. We can then call another macro to process the
result and that macro can use `\n@xt` to decide what to do.

[=cchar_charstyle]::

The following macros need to test for space and end of line (which in TeX is
stored as a carriage return character U+000D). But those are so necessary in
defining the macros that we can't just test for them. Instead we use a trick
that encapsulates the macro definitions in a `\lowercase`. TeX lowercases all
the `other` characters, but has already ignored all the whitespace characters in
collecting tokens, so now we can safely have whitespace tokens in the result. We
achieve this by specifying two other characters that map to space and carriage
return when lowercased, and then use those inside the `\lowercase`.

[=cchar_docharstyle_intro]::

The two types of character style macros (1) are very similar as we track down the
two paths. We start by treating space and carriage return as space. Notice that
we don't treat carriage return as a carriage return because we don't want a
double line break to be considered a paragraph break. Instead we treat
everything as one very long line, until we get to the end of the character
style. Next we start testing `\n@xt` which contains the character after the
style marker. If it is `*` then call the end character style routine. Notice we
reuse `\n@xt` here. Otherwise we call an appropriate macro according to the type
of space following the marker. If there is no space, but somehow they have
managed to close a marker some other way, we don't consume the character and
simply jump into the start character style routine itself. Notice that we can
now merge the paths and we differentiate later using the global macro
`\stylet@pe` to differentiate (2). There are two macros that we call to consume
the space or carriage return before calling the start character style (3).

The third special case is introduced by /milestones/ in the USFM-3 standard.
These have one of three possible formats:
```
\ts-s ...\* 
\ts-e ...\*
\ts ...\*
```
Each one of these may optionally have attributes consisting of a nameless (default) parameter and 
then any foo="bar" style parameters.
While it is not clearly prohibited, it seems unlikely that they will contain any actual text prior 
to the attribute mark (```|```).  But in any case, the ```-s``` or ```-e``` flags must be treated as start and end markers.

[=cchar_docharstyle]::

### Style Stack

Since character styles can embed inside each other, and paragraphs can 
embed (or stack) within a side-bar, it is necessary to have a
stack of currently open styles. TeX doesn't have a stack or array type, so we
use strings instead. Stack items are separated by a comma `,` and are stored
with the top of the stack first in the string. Within each
item the two components are separated by a plus `+`. The first component is the
style type:

Type  Description
----- -----------
 c    Embeded character style
 C    Normal non emebded character style
 P    Paragraph style
 N    Note
 t    caTegory (` \ef \cat people\cat* .... \ef*`) 
 s    SideBar (`\esb \cat History\cat* \p .... \esb*`) 
 m    USFM milestone group (` \qt-s[attributes]\* .... \qt-e\* `)  


The second component is the marker itself. Thus one might have a stack string of
`C+nd,c+ft,N+f,c+wj,P+p,+,` which says we are in an embedded `\nd` marker inside
a `\ft` inside a footnote that has been called from text within a `\wj`
character style inside a `\p` paragraph. Notice there is always an empty element
at the bottom of the stack to make processing easier.

We define quite a few macros to handle all this. First there are the generic
stack handling macros that work with any kind of stack and then there are the
macros we use specifically for working with the `mcstack` which contains the
style stack we are interested in. The good news is that TeX's parameter matching
capabilities make handling a stack relatively straightforward. The first three
macros are the core definition for a stack: pop, push, peek. The up and down
macros (1) are for iterating through the stack either from bottom to top (up) or
top to bottom (down). They each call a predefined `\d@` macro. The top macro
calls `\d@` for just the item on the top of the stack. Notice that we don't use
`\n@xt` because too many other macros do and we don't want to clash with them.
The `\cstackrelax` is a macro that `\d@` can be set to to quit out of a stack
iteration early.

[=csty_stack]::

Now we use these macros to implement a concrete stack for styles. Using the
stack macros with a particular stack is just complicated enough to warrant its
own set of macros.

[=csty_mstack]::

This allows us to describe how starting a regular character style can close all
currently open character styles. `\end@allcharstyles` iterates the stack top
down calling the macro that tests whether that stack item is a character style.
Notice that the way the stack macros work, if the stack changes during
processing, the processing itself is not affected because the whole stack is
passed to the first macro and then the parameter list is chopped as it iterates,
with no further reference to the stack itself. Note also the use of
`\cstackrelax` once a non character style is encountered. This stops any more
iteration of the stack and potentially closing styles that should not be closed.

[=cchar_endallcharstyles]::

As an example of scanning a stack, `end@allcharstyles` is a good first example
and worth analysing. The `\mcdown`, `\mctop` and `\mcup` macros all use the
`\d@` macro to do their per item work. The use, therefore of the macros is one
of setting the `\d@` macro and calling the appropriate routine. The `\d@` is
then called with each item in turn. Since the style stack structures each item
as type `+` tag, we can use parameter pattern matching to break apart the
structure. When `\d@` is called, the stack macros append the item with `\E` as a
delimiting token to aid in pattern matching. Inside the macro we store the type
in a temporary macro to make testing it easier. String matching in TeX is a pain
and just deciding whether the value is empty (which happens with the bottom of
the stack which has an empty sentinal item) involves storing the value. We test
if it is empty, and ignore the item. If the type is `c` (for embedded character
style) then simply close the character style. We do the same for a normal type
`C` character style as well (since we are closing all character styles). If the
type is anything else, then we want to stop any further processing. We do this
be resetting the `\d@` macro to the `\cstackrelax` macro that simply does
nothing with the item.

The other key macros involving the stack are those for getting the current value
of a parameter. `getmcp@ram` and its corresponding `R` specific version for
diglots, starts at the bottom of the stack (1) and sets the parameter each time a
style is encountered that sets that parameter. Well it's more complex than that
because it takes into account whether the item on the stack is a paragraph or
note style in which case the result is force reset. (1) After running the stack, the
result is in a global `r@s` which is then stored in `p@ram` as the normal return
value from such macros.

There is also a macro for getting the value of a parameter if the top of stack
is of the given type, else looking back through the stack for a value. This is
like the `getmcp@ram` but allows the top of stack to trump the value, even if
none, if it is of the right type. And there is a diglot R version of the macro
too.

[=csty_getmcparam]::

A more complex question is what is the current font size. This involves
considering the `fontscale` parameter as well as `fontsize`. (3) Again we
iterate the stack from the bottom to the top. But for each item if it is a
parameter or note then get its fontsize. If undefined, default to 12. We say
everything is in pt just so we can deal with a dimension, but we will strip off
the pt later. If the item is a character style then get its fontscale (1). If
the fontscale is not 1, then simply use it to multiply the current size (2) Also
get the font size and if the fontsize is not set or is the same as the `p`
paragraph style (system default), then use the scale otherwise set the font
size. Then go round again until we have a final result.

[=csty_getmcfontsize]::

### Processing Character Styles

Now that we have a style stack, we use it everywhere.

#### Start

On starting a new character style run, the first thing the routine does is to
push the new character style information on the style stack. It then tests
whether the style marker is marking text that is publishable. That is that we
actually want to output the text in this run. This involves seeing if the string
`nonpublishable` is in the properties parameter for this marker. This is done
using TeX's macro pattern matching. We get the parameter and then assemble a
string of the parameter value followed by `nonpublishable!`. Then we match for
`nonpublishable` and the sentinal `!`. If the parameter value has nonpublishable
in it, then that first nonpublishable will match the `nonpublishable` in the
macro parameter match and there will be something after that (at least the
`nonpublishable` we appended to the parameter) in `#2` and so the parameter
contained `nonpublishable` and we can set the flag, else there is nothing and we
don't set the flag. Phew!

[=csty_testpublishability]::

Returning to starting a character style. If the text is not to be published (1)
we group it up into an hbox which we will dump later. But we don't have to do
anything regarding setting up any styling. We do start a new group, because all
character styles start a new group. While grouping is a way to handle a style
hiearchy, it doesn't allow interrogating of style information above us in the
groups. We also track the currently open style in the group.

(2) Normally we do want to publish the text and to do that we need to be in
horizontal mode, since this is character styling and not paragraph styling. If
there is a `before` hook for this style, we execute that. If we are in a diglot,
we set which side we are on and perhaps run a per side `before` hook. Then we
start the group that contains the character style. We set the current style and
then set the font for the style. Rather than take a long excursus into how a
font is set, we will address that later. There are various depth counters that
we update, which are hang overs from before we had a full style stack. We find
out whether this run is to be raised text. (3) If it is then we need to collect
the text in a box that we can raise. This limits raised text because no line
breaks can occur within a raised text run.

Now that we are in the character style, we run the `start` hook if it is
present, and if in a diglot, set the side and run any side specific start hook.

[=cchar_startcharstyle]::

#### End

There are two end
character style macros. The normal close macro has to close all open character
styles, while the plus close macro only needs to close the currently open
character style. Each routine starts by analysing the top item on the stack. The
normal routine tests that the top of stack contains a character style, while the
plus routine tests that the style is of the right name. If either test fails an
error is output and the actual work of closing the character style is not done.
Otherwise each routine passes off the work of closing the character style to a
common routine.

[=cchar_endstyle]::
USFM-3 Milestones make use of the ```\\*``` "self-closing marker" as their 
distinguishing feature. Plain TeX defines ```\\*``` as a discretionary multplication 
sign (i.e. if the line breaks here, put in a multiplication sign), and that definition
has (until now) has survived. Presumably / hopefully it's not commonly used in 
USFM otherwise! We define it as (a) calling a macro and (b) closing the character style.

The routine to handle ending character styles is encapsulated in a `\lowercase`
so that it can use a `\\` as a character in an error message. The first thing is
to collect the current character style from top of the style stack. Assuming it
is defined, if we are in a mode where we are skipping nonpublishable text,
simply close off that group, which then stops the collecting of data into the
hbox. And since we don't want to output the hbox, we need do nothing. Otherwise
we need to put things back to how they were before the character style started.
We start by doing any diglot side specific `end` hook, or a normal end hook.
Then we look to see if we were being raised. If we were then we end the group
that collects the data in the box and then raise that box by the amount of the
raise. _Do we need a better box than box0 here?_. (1) Next we collect the `after`
hook so that we can run it outside the group for the character style. We also
collect any diglot side specific `after` hook. Then we update the nesting counts
and (2) close the character style. Then we run the after hooks.

Finally regardless of whether the style was publishable or not, we pop the style
stack.

[=cchar_endcharstyle]::

### Setting the Font

TeX was written before the prevalence of scalable font technology. Therefore a
TeX font is created at a particular size and colour.

#### Colours

Processing the `color` style property is not simple. There are two ways of
describing a colour in USFM (apart from `\Colorname` which is not yet
supported). The first is with an `x` prefix as 6 hex digits, with each pair
giving a brightness for each of Red, Green and Blue. The other is as a decimal
that if in hex would have 6 digits, but here the pairs represent Blue, Green and
Red!

The entry point is the `\ParseColor` macro (1) that takes a `color` property and
parses into a `r@s` result as a 6 digit hex RGB value. Parsing the `x` type is
easy. But the purely numeric value is more interesting. We call `colorhex` to do
the mathematics of shifting and adding values to get the right RGB decimal
value. Then we call the `hex` routine to convert a decimal number to hex. The
hex routine needs to pad the value to 6 digits with initial 0s.

[=cchar_parsecolor]::

A key macro needed in setting a font is giving it a name by which to reference
it. This is basically the style name along with the size of the text the style
is being used at. Since fonts are
instantiated at a particular size the size is included in the name. Taking the
top item from the stack we test to see if it is the same as passed to the macro.
If it is then get the font size for this run otherwise get the font size for the
marker passed in, defaulting it to 12. We could well be doing this within
another stack operation, so we keep and restore any old value for `d@`.

[=cchar_getfontname]::

Setting the font starts by getting a name for the font and set the side for
diglot. Fonts are cached by name and if there is no font for the given name then
we need to make one. We set up references to the main fonts, which are diglot
side specific, hence the references. We get the name of the font if there is one
for this style. If not then we work out which of the standard fonts to use based
on `Bold` and `Italic` settings for the style. (1) We then look at the `smallcaps`
parameter and if present add the small caps feature to the font description. (+) If
there is color for this style, then parse it and add a color attribute to the
font description. (+) Next we calculate a size for this font. Starting with the
calculated fontsize for this style in its context. Then for superscript we use a
`fontfactor` parameter, which we multiply the calculated font size by. (+) At this
point we have a sufficient description to instantiate the font. This is done
directly into the cache.

One thing we can do is to change the default space stretch and shrink factors
for this particular font. This allows the user to change the stretchiness of
spaces in this font. We do that by setting appropriate `fontdimen` values. (+) Once
this is all completed, we simply instantiate the font from the cache, whether or
not we created a new cache entry. So for most cases where the font has already
been created, this runs pretty quickly.

[=cchar_setfont]::

In many texts, there are extra characters in the text that are not in the main
body text font. For these we want to switch to a different font just for that
character. We use an _extra font_ for this. The font instantiation is simpler
than for a main font, but it still involves a cache and the creation of a font
description.

[=cchar_extrafont]::

## Paragraph Styles

One of the characteristics of Bible typesetting is that the resulting book is
long and so is often printed on thin paper. This results in visual bleed through
of text from one side of the paper to the other. To maximise contrast, it is
best if text on one side is in the same place as text on the other side of the
page. Thus between line space on each side aligns and remains white rather than
turning grey. To achieve this _backing up_, text is typeset on a grid. The PTX
macros work hard to maintain this grid wherever possible.

Paragraphs in the PTX macros are grouped into a title block, headings blocks,
intro paragraphs and
body paragraphs. The blocks are groups of paragraphs that are then spaced in
order to keep the following body paragraphs on the grid.

Starting at the top, a paragraph style marker calls the `\p@rstyle` routine with
the marker tag. The start of a new paragraph implicitly ends a previous
paragraph. The first part of handling a paragraph marker, therefore, is closing
the previous paragraph. As with character styles, a marker may be marked
`nonpublishable` and the contents will be grouped into a box and dumped. If the
user has specified any parstylehooks, these are executed here just before the
end of the paragraph. Only empty paragraphs do not finish in horizontal mode. We
undo any paragraph final space and then close off all open character styles.

(1) We write out the current position on the page to a `.parlocs` file. This
file is used to work out whether the layout has changed significantly between
runs. Notice that the position is not written immediately. A `\write` command
actually stores a _whatsit_ in the page. This zero sized item is generally
ignored until the page containing it is shipped out. When the item reachs the
point of being written to the output file, it is executed. At that point the
`\pdflastposx`, etc. are expanded (and known) and the actual position on the
page is output to the `.parlocs` file.

Now we finish the paragraph. Calling `\par` involves more than having TeX finish
the paragraph. We will examine that in a moment. After closing the paragraph, we
look at the depth of the last line. If it is above 0pt, we collect it, else we
set the collection to an impossible value.

(2) If we are in a paragraph that includes a dropped chapter number in the
middle (from `\nb`) then we need to store the number of lines in the paragraph.
We do that in `.parlocs` file using a `\write` as in (1). But we need to expand
the `\prevgraf` at this point and not have its expansion delayed until shipping
time. This is done by a chain of expandafter commands. Each expandafter first
expands another expandafter all the way to the `\the\prevgraf` which gets
expanded, and then the rest of the tokens are unwound and the `write` executed.

If there is only one line in the paragraph, that isn't enough to hold a dropped
chapter number, which needs 2 lines and so we inhibit any page break at this
point and tell the next paragraph it has a dropped chapter number to include.
Otherwise we clear the flag.

[=cpar_parstyle_intro]::

What happens when `\par` is executed? Before we actually close the paragraph, we
adjust its parshape to include any cutouts. How cutouts work is delayed to
[here](#cutouts). We then call any `end` hooks for the marker, be they for the
diglot side or more generally. Now we can finally close off the paragraph.

The first thing we need to do in the next paragraph is carry over any remaining
cutout from the previous paragraph. For example, if the just closed paragraph
was only one line long, then we need to carry over one line of cutout to the
next paragraph. Finally if there are any post paragraph pictures, we should
output those. See [Figures](#figures) for more details.

[=cpar_par]::

Meanwhile, back in `\p@rstyle` we are ready to start the new paragraph. We first
need to find out whether text in this style is publishable. If it is not then we
break the paragraph now, because it will be empty when the next paragraph starts
and so will not be in horizontal mode and so will not close the paragraph
normally. Then we start a new box to place the contents of the paragraph. The
minimum needed is to set the current paragraph marker and indicate that we are
skipping.

The rest of this massive routine is treated as the else to this question of
publishability. If the text is publishable, then we have a lot of work to do.
While the paragraph has been closed by TeX, we are still processing the old
paragraph. We first need to see if there is any space to insert below the
previous paragraph. If so, then if we are in a heading block then do not allow a
page break at this point. Headings stick together and to their following
paragraph. (1) Then we insert the space.

Next we reset the paragraph style to its defaults. This is a relatively
straightforward routine. It resets the left and right and parfill skips and the
paragraph indent, ready for being set for the new paragraph.

[=cpar_resetparstyle]::

The next step is to pop the style stack ready to start the new paragraph. But
first we check that the top of stack does indeed correspond to the paragraph we
are closing. Then we pop the stack (2). Next we run any `after` hooks for the
marker we are closing. And finally we are done with the old paragraph.

We store the new marker as the current paragraph marker and we push it onto the
style stack. Then we run any `before` hooks for this new marker.

[=cpar_parstyle_after]::

But we are not done with the old paragraph quite yet. We need to work out if
there is a transition between blocks. E.g. from a heading block to normal body
text paragraphs. We start by testing to see if we are starting an intro
paragraph.

[=cpar_testintro]::

Also if we are in a table and that table is in the context of an introduction
then we are also an intro paragraph. The next step is to use the `type`
parameter of our marker to work out what type of paragraph we are. We clear the
`he@dingstyle` flag to its default and look up the type of the paragraph and for
each type we do what needs to be done. If it is `title` then set the reference
mark to the sentinal `title` to indicate that we are on a title page and not to
output headers and footers. This also applies to diglot marks. If we are not in
a title block already but we are in a headings block, then finish the headings
block. Now start a title block (which does nothing if we are already in a title
block) and set that we are in a title block.

(1) If, on the other hand, this is a `section` type headings paragraph then if
we are in a title headings block then we need to close that to start a new
headings block. If we are an introductory text marker as well as being a
heading, then perhaps start the introductory text (from the title block),
otherwise we are a body text heading and so we may need to start body text. Then
we set the flag to say we are in a heading style. For body text type markers, we
treat paragraphs of type `other` as headings. In introductory text they are
normal introductory text markers. If the paragraph type is anything else then if
it is an introductory marker then make sure we are introductory text else make
sure we are in body text.

(2) Now that we have set the major mode of text we are in (title, intro, body),
we can deal with headings. If we are starting a heading style paragraph then are
we already in a headings block. If so, set the baselineskip for the new style,
but other than that do nothing. Just keep going. On the other hand, if we are
not in headings block, we better start one.

At the start of a new headings block, we collect the space before the first
paragraph (this paragraph) so that we can make sure the space is removed at the
top of a column. Although in titles we don't remove any space at the top of a
page because titles always come at the top of a page and we want all that lovely
whitespace to make the title heading stand out. Then we start a new headings box
to collect the paragraphs in. Then we set the baselineskip for the marker and
make it impossible to break a page inside a headings block. We also turn off
line breaking at hyphens. People should not be writing books in heading blocks!
Finally we say "no page break here".

If, though, this is not a heading style paragraph and we are in a headings block
then we need to end the headings block. We cover this in [Gridding](#gridding).

Now we can insert the before space for a paragraph. If there is before space
then if we are in a heading then don't break. If we are not the first paragraph
in a headings block then `nsp@cebefore` will be true. In this case we don't want
to add any extra space to pull such paragraphs apart. The space above in this
context is implicitly saying: only space above for the first heading in a block.
Unless the space above is negative. Then the implicit assumption is that we only
want the space above to act if the the paragraph is not the first, because we
want to pull lines closer together when grouped. Mind you since we are using the
default here, we do allow initial paragraphs to have negative space before, just like
we do for non heading styles.

And so we come to the start of the paragraph. Finally!

[=cpar_parstyle_transition]::

There are a number of routines, referenced above, to describe before we continue.
Each of the paragraph modes needs to siwtch to the appropriate number of
columns. For each mode start we first test to see if we are already in that
mode. If we are not, then if we are not creating a diglot, we test to see if twe
have to change the number of columns and if so we call the appropriate column
switching routine. These are described in the Output Routines chapter. Then we
set the flag for the mode. In the case of starting the body text then we also
suggest that this is a good place to break a page and we insert a blank line
before the main body text starts.

[=cpar_starttypes]::


### Gridding

Heading blocks often involve text of different sizes and baselines and so takes
the text off grid. We group all this off grid text into a block and then insert
space above the block to ensure that body text following the block is back on
grid.

Following closing any paragraph, ending headings may involve cutouts (_why?!_)
Thus we make any needed and close the paragraph and close the box containing the
headings. Next we reset line spacing to that for the default `\p` styling and
then call the routine to expand the box to be an integral number of lines tall.
The resulting box is output and we reset the various flags associated with
headings.

[=cpar_endheadings]::

There are two `gridb@x` routines. The first is the earliest gridding function
and does not remove space at the top of a page. Both functions use the
`\killd@scenders` routine. This removes any depth from the last line in the box.
This is a bit of an undertaking. We unpack the box and get hold of any final
skip and the final penalty so that we can put them back afterwards. Then we get
the lastbox and its depth. We then clear the depth of that box and reassemble
the box by putting back the adapted box, any penalty and final skip. All this is
bundled into the returned vbox.

[=cpar_killdescenders]::

The first gridbox routine works by inserting just enough blank lines to cover
the box and then overlays the headings box over that, thus extending the box
upwards by enough space to get the next paragraph back on the grid. We start by
collecting the box. If this is a picture box then we insert a little extra
border space. Next we measure the box for its height and
depth and start another dimension that will increase until it surpasses the
measurement. If this is a picture we insert an extra blank line. This is because
by default the starting point of the cursor is one line below the bottom of the
previous paragraph due to the start of a new paragraph and its baselineskip. But
a picture is not in the main text and so the cursor starts one line up and we
need to insert a line to compensate.

(1) Now we start the main loop and while our increasing dimension is smaller
than the box size we insert lines. Each time we insert line, we also insert a
penalty to stop any page breaking. Once we have enough lines inserted, we create
a box that first inserts
a kern to shift us back up to the top of the headings box (which isn't back to
where we started) and then expand the headings box. Finally we insert that box
and stop any page break after it.

[=cpar_gridbox1]::

The second gridbox routine is the default routine (2) and there is a control
that is used once to set the gridbox routine.

There is a mathematical macro whose job is to calculate how much space we would
need to add to a dimension to give a result that is an integral number of
another dimension. The macro relies on integer mathematics to do its job. Thus
we divide the input by the gridsize and then multiply it again to bring it down
to a integral number of gridlines. Then we subtract that result from the
original value. Finally we add that to the gridsize and return the result.

The approach this gridding box uses to have a different amount of space at the
top of a page than within the page is to remember that TeX removes any initial
vskip at the start of a page. Thus we want to have an initial vskip which is the
difference between the gridded height of the box at the top of a page and the
gridded height of a box within a page.

TeX remembers the depth of the previous box output and sets the inter line
spacing based on that and the baselineskip. But we don't want to set the space
to the baseline of the first line after the headings box based on that. We the
adjustment set to 0. But we have captured the depth of the last line of the
previous paragraph in `\lastdepth` so we can use it later. Here we tell TeX to
pretend that the last paragraph had a depth of 0.

Next we set a box to either the box or the box without
descenders. Then we set the baseline for the default paragraph style. We now
take the height of the box and the baseline for the grid size and calculate how
much to add to its height and store that (in `dimen2`). This is the space to
allocate when not at the top of a page. Now we do the same thing again but
this time we reduce the height of the box by the headingtopspace. I.e. we want
the space to allocate at the top of a page. We subtract the adjustment from the
main box adjustment. Now `dimen2` holds the main box adjustment minus the top of
page adjustment. We now add the headingtopspace to that and that gives us how
much space we want when not at the top of a page, and so in out initial vksip.
We also have the grid adjustment for within the page, in `dimen0`. (1)
If we are not a picture box, we also need to remove any depth from the text
above. Since we are only interested in this mid page we want that adjustment to
disappear at the top of a page so we reduce the space by that depth.

Now we output the calculated values. If we are in a diglot, we don't want the
top space skipped, so we use a kern rather than a skip for the initial space.
Then we kern by the mid page grid adjustment. Since we have added the
headingtopspace to the initial space, we need to remove it from the contents of
the box, we undo the skip by skipping by its negative and then comes the heading
box, in which the first item will be the headingtopspace (net result 0). Finally
we inhibit page breaking after the heading box, and we are done.

[=cpar_gridbox2]::

### Every Paragraph

The next part of the paragraph style routine is to specify what will happen when
the first characters appear in the paragraph. We delay because we want all the
character styling setup to be done, etc. So we declare a routine at this point
that TeX will call when switching into horizontal mode.

If there are any `\addtoeveryparhooks` and there are some core ones (See
adjustments and table of contents), run those hooks now. `\pdfsavepos` tells
XeTeX to save the current position (the start of the paragraph) so that it can
be accessed later via `\pdflastposx`, etc. And we also write out the position we
just saved, when the paragraph is finally shipped out. The next step is to work
out what the right and left skips are. These are the skips that are inserted at
the left and right of each line when the paragraph is completed. For right to
left text, everything is swapped. The default is 0pt on either side to give
fully justified text. If the user has chosen ragged right (or non justified
paragraphs) then the appropriate end line skip is set to allow up to $1/4$ of a
column width of rag.

Based on the `justification` parameter for the paragraph style we now set the,
in effect, start and end of line skips. For centered text we set both skips to
be stretchy glue up to a column width each. For left justified we set the right
skip to stretch up to $1/4$ column. And if this is right to left then do not add
any extra stretch to after the end of a paragraph. Likewise the opposite for
right justified text.

Now we get the margins for the paragraph (1). They are used to increase the
appropriate side skips by a fixed amount. We also set up some of the basic
character styling by setting the font for this marker. We assume this is a
normal paragraph and we allow normal paragraph indentation. That may not hold to
the end of the setting up this paragraph. More setting up calls for a PDF
outline bookmark if we have changed book (which is unlikely), and getting 
the first line indent for the paragraph.

[=cpar_parstyle_start]::

Reading the code linearly, the next part of thie paragraph style routine is
concerned with drop chapter number support. We will discuss that as part of
[Milestones](#milestones).

The last part of the `everypar` routine sets up the initial indentation. If
there is a first line indent we need to analyse whether we still do actually
allow first line indentation. If the indentation is negative, then yes.
Otherwise we don't allow first line indentation if IndentAfterHeading is not
true. If we are actually going to do the indentation, we manually insert the
indentation (1). If there is a chapter number box, then we shift backwards by
its width and insert it. We set the flag to say we are in a paragraph and then
run any `start` hook for the paragraph marker. This also applies to diglot side
specific `start` hooks. If there is a chapter number in this paragraph we
disable marginal verses around the drop chap. Finally we say we are no longer
starting up the paragraph. That brings us to the end of the macro that is run
when the paragraph text starts. And that brings us to the end of a very long
`\if` that started way back whether this parargraph is publishable or not.

[=cpar_parstyle_final]::

### PDF Bookmark

At various points in the code, a call is made to `\pdfb@@kmark` to possibly
insert an outline entry for the start of a book. The choice of which routine to
use is diglot governed. We examine only the monoglot version, with the right
diglot alternative being nearly identical apart from which variable is used. If
the book is the same the previous book, then there is no book transition and no
output is needed. OTherwise we stop any drop number for this paragraph (_why?_)
and create a PDF outline entry for the book.

[=cpar_pdfbookmark]::

## Note Styles

Dealing with note styles starts long before a note is encountered. When a style
marker is identified as a note style marker, we need to create an insert for
that kind of note. We start by setting a flag to say that as far as we know, we
are a new class. We also store the identifier (marker) for the class so that the
checking process can test against it.
Then we iterate through all the existing classes to see if any of them are the
same as the marker. If not, then we allocate the class.

For each class we call the `\ch@ckifcl@ss` which tests to see if the class
identifier in question is the same as the marker we are making a class for. If
it is then we indicate that this is not a new class.

Allocating a class is where the note class is actually made. We add the
execution `\\<marker>` to the list of note class tokens for rapid iterating
through all the note classes, just as we did for `\ch@ckifcl@ss`. Then we create
an insert for the note (or two in the case of diglot). Creating a new note is
simply a matter of creating a `newinsert` for the class. The problem is that
`newinsert` cannot be called from inside a macro. So we have to `\let` another
token be the content of `\newinsert` and call that instead. Sigh.

[=cnote_makenote]::

### Start Notes

When a note style marker is encountered we call `\n@testyle`. Note styles are
closed just like character styles. In this routine we analyse the character
after the marker to test for `*` or anything else (including space). Although
what follows a start marker is expected to be only a space. On entry to the
routine, we capture the marker and set up space as a normal character and then
use `\futurelet` to grab the next token (read character) after the marker. This
then calls into `\don@tstyle` which analyses the grabbed token. If it is a `*`
then we call the `\endn@testyle` else we call `\startn@testyle`.

[=cnote_notestyle]::

We use the lowercase trick on `\startn@testyle` to handle the space following
the marker. This has an unfortunate side effect that we can't use capital
letters for anything important in the macro. So we get around this by creating a
macro for our uppercase string, and since the definition is outside
`\lowercase`, no lowercasing happens.

We start the note style, like so many others, by testing to see if the text in
the note is publishable. If it is not then we open a whole nest of groups that
correspond to the groups that get created for a publishable marker. The first
group encapsulates resettting paragraph controls, via `\resetp@rstyle` (1) (In
the next code fragment). Then
we clear the tokens to execute after the note. Then if we are inside a heading,
we create a new group to correspond to the box that is created to delay the
output of notes. Then we create a box to capture the notes contents and turn on
note skipping. We are inside a note and we set a flag to say whether there was
space before this note.

[=cnote_startnote_start]::

Otherwise this note is publishable and we have to do something about it. The
first step is that, because of the caller, we need to be in horizontal mode.
Then we get the `notebase` parameter of the note. This allows someone to specify
that a different note class will receive the contents of notes of this marker.
For example if they want to merge `\f` footnotes and `\x` cross references. If
nothing is specified, then use this marker as the note class.

If there is a `before` hook to run, then run it. Now capture the function's
parameter which is the caller character for this note. If the caller is a `+`
then we need to auto generate the caller. We do this by incrementing the caller
index and inserting the caller at that index. Otherwise if the caller is a `-`
then no caller is output, otherwise use the caller character itself.

We start a group for the note and its caller. We collect any `after` hook for
the note. Was there some space before the note, then flag the need later. Then
we reset the paragrph style within the note group for the note text itself. (1)

The core of note handling is a call to `\m@kenote`. The parameters to that macro
are themselves token sequences. Notice that the sequences are not expanded until
inside that macro. The first parameter is the note class into which the note
will go. The second is the note marker. The third is the code to insert the
caller into the main text. This code also sets up the paragraph for the note
text. The default style for the caller is `\v` unless specified for the note.
The caller is then created in a box, which might be empty if the caller content
is empty. The content of the box is character styled by the callerstyle.
In addition to the superscript of the callerstyle, there is the callerraise. If
set then raise the box by that amount.

The fourth parameter contains the code to insert the note's caller as a box. If
there is a notecaller style then use that to style the mark. In addition use the
notecallerraise to raise the box.

Calling `\m@kenote` is the same as starting a footnote in plain TeX. The macro
returns with us inside the note insert. So we begin a new group and flag that we
are inside a note now. If there is a `start` hook for the note, we execute that
here and skip any following spaces.

[=cnote_startnote]::

The `\m@kenote` macro parallels the footnote moacro in plain TeX. It's job is to
output the caller into the main text. If we are at the start of a paragraph (why
should we) then use the default space width otherwise continue with the existing
space glue. If we are in a heading then output the caller in that place in the
heading, but append the actual insert to the end of the headings. This reduces
any pressure to break a page within a headings bloxk by placing all the page
length cost at the end of the headings block. If we are in a chapter box then
append the ntoe to the chapternote. Otherwise just output the caller as normal.
Now set the spacefactor for the text inside the footnote and call to setup the
note insert, which may get wrapped. Notice that if there is no notecallerstyle
then simply use the same caller as in the main text.

[=c_makenote]::

This is where we actually start making the note itself. We are passed the target
note class, the note marker and the code for the caller box. To set up, we set
the flag to say we are in a note and we clear the `next` token ready for the end
of the routine. We capture the note class into which the note is going, with
appropriate diglot adaptation. Then we start the insert. An insert is a vbox
that is inserted into the main contribution list before the main text line it is
part of. The insert starts a vbox and we start a group for it.

### Ending Notes

When we come to close off a note we need to end all the active character styles.
Then if we are skipping this note, then don't run any `end` hook. Then we close
off the note group, which closes the footnote and executes any `aftergroup` code
it has. Then if we are in a heading, there is an extra level of grouping to
collect all the notes in a heading block at the end. We clear some flags.

Very often users in effect type a space both before a note marker and also after
the end of the closing note marker. We only want one of those spaces, so if
there was a space before the starting marker, skip any space following the
closing note marker. The `after` hooks were collected when the note started and
are executed here. Finally we end the whole group that was created when we
started this note and perhaps skip any following spaces.

[=cnote_endnote]::

### Paragraphed Notes

There are two kinds of notes: paragraphed notes are grouped into a single
paragraph while separate notes are output one per paragraph. We test to see
which kind of note class this is. Setting paragraphed notes is a user option for
a class.

[=c_paragraphedNotes]::

We set up the text width for the note. For paragraphed notes, we set the text
width to infinite otherwise we use the current textwidth. Then we reduce the
width by the column shift (since notes are shifted by the column shift, for
marginal verse numbers). The linepenalty says how hard we do not want footnotes
to split across a page boundary. This is a plain TeX parameter which defaults to
100. The `\floatingpenalty` is set to the maximum of 10000, saying we do not
want notes spread across pages. We reset all the side and space skips. We set
the baseline based on the target note, not the marker, since all notes in a
class should have the same baselineskip.

### Separate Notes

If these are separate notes, then create full height strutbox and if the height
of that box is less than the baselineskip then skip by the difference between
that height and the baselineskip. Now we start the paragraph in the note. In a
diglot we insert any side hooks. If we are right to left then insert right to
left start before whatever is already output.

We now test to see if we want callers in this note type. If so then create a box
from the note caller and output it. If it has width then add a small kern of
.2em after it. This is not user configurable.

Now we push this note type onto the style stack and set the font. Finally we
collect the bgroup that follows the call and call plain TeX's footnote handling
routine. 

[=c_vmakenote]::

`\fo@t` is a plain TeX macro and is described in the TeXbook, but in summary, in
our context, it calls `\@foot` after then end of the note style. Our `\@foot`
first ensures no skip at the end of paragraphed notes. This is because we are
merely collecting the note into an hbox inside a vbox. For separate notes, we
include a strut to ensure an appropriate size for the last line. Then we close
of the horizontal mode and close the styling group we started for the note. Next
we check that the style stack is in good order and then pop it.

[=c_foot]::

[-d_styles]::
