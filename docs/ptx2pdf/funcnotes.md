
[+strippt]::
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

[-strippt]::

[+d_sty-defcv]::
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

[-d_sty-defcv]::

[+d_sty-verse]::
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

[-d_sty-verse]::

[+d_sty-chap]::
Most chapter numbers are a drop number. What makes scripture typesetting tricky
is that there are a few drop chapter numbers that occur mid paragraph. Since
USFM says that paragraphs occur under a chapter marker. There is a special
paragraph marker for the non paragraph break: `\nd`. To achieve the cutout we
have verious things to set up in the chapter marker itself. Like the verse
milestone handler, there are two parts of the chapter marker processing. We
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

[-d_sty-chap]::

[+d_sty-chap-setup]::

Here we do the onetime setup for drop chapter numbers. Calculating the proper
size of a dropped chapter numbers is tricky. We start by asking the style for
the size of chapter number. If this is less than twice the main paragraph
fontsize then we calculate an automatic size.

To do this we need to find the ascent of the descent (in box1). We also get the
vertical metrics of all the digits in the chapter font. Notice that to get the
font metrics we tell XeTeX to give us those. Then we switch to have XeTeX give
us true glyph metrics. We clear out the chapter font in anticipation of
recalculating it with a new size. Then we get the x-height of the paragraph
text. Now we have all the external numbers needed to calculate the drop number
size. TeX does fixed point calculations in sp with 1pt having a value of 65536.
The problem with this is if you divide two dimensions you get an integer
division, which is often not very useful. To increase accuracy, we multiple up
by 128 (giving a maximum dimension of 512pt which should be enough for 2 lines
of text). This means keeping track of when we multiply, values are in effect
mulitplied by 2^16 and if a number that is multiplied by 2^16 is divided by
another number multiplied by 2^16 then the result has no multiplier, and so on.
Multiplying numbers by 128 for extra accuracy can either result in having to
divide the result by 128 or multiply it by 512 (2^16 / 2^7).

First we calculate X, which is the distance from the baseline of the second
line to the top of the x-height of the first line. And then we calculate X/C *
128. We also calculate height T the distance from the second line descender to
the first line ascender, based on what the font says about ascenders and
descenders. Next we need CX/T (where C is the point size specified by the
chapter style). We also calculate the maximum depth of the digits scaled if
the maximum height was scaled to fit with top x-height.

If CX/T is less than the maximum height of the digits, or if there is
insufficient room below the baseline for the scaled depth, then use the CX/T to
scale. Otherwise use the maximum height. This is then scaled such that height
will stretch from baseline of the second line to the x-height of the first line.
We know that the whole thing will fit, but we may need to shift the number if
the descender would clash with the line below. We calculate what the shift is.

The dropnumbersize dimension is converted into a string so that it can be stored
as the `\c` font size, as if it were specified in the .sty file.

[-d_sty-chap-setup]::

