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
may take parameters following them in text, they have are not opened and closed,
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
`*`, which indicates a close marker or a space ` ` that indicates an opening
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
managed to close of a marker some other way, we don't consume the character and
simply jump into the start character style routine itself. Notice that we can
now merge the paths and we differentiate later using the global macro
`\stylet@pe` to differentiate (2). There are two macros that we call to consume
the space or carriage return before calling the start character style (3).

[=cchar_docharstyle]::

### Style Stack

Since character styles can embed inside each other, it is necessary to have a
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

The second component is the marker itself. Thus one might have a stack string of
`C+nd,c+ft,N+f,c+wj,P+p,+,` which says we are in an embedded `\nd` marker inside
a `\ft` inside a footnote that has been called from text within a `\wj`
character style inside a `\p` paragraph. Notice there is always an empty element
at the bottom of the stack to make processing easier.

We define quite a few macros to handle all this. First there are the generic
stack handling macros that work with any kind of stack and then there are the
macros we use specifically for working with the `mcstack` which contains the
style stack we are interested in. The good news is that TeX's parameter matchin
capabilities make handling a stack relatively straightforward. The first three
macros are the core definition for a stack: pop, push, peek. The up and down
macros (1) are for iterating through the stack either from bottom to top (up) or
top to bottom (down). They each call a predefined `\d@` macro. The top macro
calls `\d@` for just the item on the top of the stack. Notice that we don't use
`\n@xt` because too many other macros do and we don't want to clash with them.
The '\cstackrelax` is a macro that `\d@` can be set to to quit out of a stack
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
don't se the flag. Phew!

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






[-d_styles]::
