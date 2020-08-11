# Controlling Spaces

TeX's paragraph breaking algorithm is powerful. It does its best to make
paragraphs look nice, integrating hyphenation and concepts such as adjacent line
balancing. But it can also be hard to control, especially if someone is wanting
to improve the look of their text.

This document is for those who find that they have overfull lines or who think
that the paragraph breaking they are seeing is just not good enough. It gets
into the nitty gritty of such things as _tolerance_ and _emergencystretch_ and
the stretchiness of glue. It is probable that only typesetters will want to read
this document.

## Introduction

It is not the place of this document to recreate chapter 14 of the TeXbook. But
we will glean information from it.

For each possible line, TeX calculates the cost of breaking the paragraph in a
way that causes a line break at a particular point in the paragraph. It then
calculates that across the whole paragraph and chooses the path of line breaks
that results in the lowest cost paragraph. There are all kinds of extra costs
that TeX brings in different contexts, like doublehyphendemerits that adds extra
cost to have two lines hyphenated, and the like. We won't cover those here. Our
main concerns is the controls that affect things like the width of spaces on a
line or overfull lines.

## Badness

The core cost of a line break is measured in terms of badness.

> The badness of a line is an integer that is approximately 100 times the cube
> of the ratio by which the glue inside the line must stretch or shrink to make
> and hbox of the required size. For example, if the line has a total
> shrinkability of 10 points, and if the glue is being compressed by a total of
> 9 points, the badness is computed to be 73 (100 x (9/10)^3); similarly a line
> that stretches by twice its total stretchability has a badness of 800.

Badness is clipped at 10000. In addition, if a line is too long and would need
to shrink by a glue ratio of > 1 (e.g. 11 points in the above example), TeX
gives the line a badness of 10001. This effectively stops overfull lines, except
in an absolute emergency, which we will come to.

The key control for telling TeX with a line break with a given badness is
acceptable or not is the setting of `\tolerance`. Most TeX macro packages for
languages like English with good hyphenation support, short words, long lines,
etc. set `\tolerance` to 200. Any line worse than that is rejected. But because
of the variety of languages we deal with, the ParaTExt macros set `\tolerance`
to 9000. This allows a space to grow by up to 4.5 times its maximum stretch.
This should give most lines plenty of wiggle room, especially if there is more
than one space on a line.

For example, Charis' space is 0.3 em wide. So at 11pt, a Charis space is 3.3pt.
The default stretchiness of a space is 50% of the width of a space, which
effectively makes a space into a piece of glue that is 3.3pt plus 1.65pt minus
1.1pt. This means that the maximum width of a space on the line is 3.3pt + 4.5 *
1.65pt which is 9.9pt. Not much for a single space, but it is probably about 3
characters width. In the case of normal language text in which words are say
around 10 chars wide, a typical double column line would have 4-5 spaces on it.
This gives TeX 8.8pt - 39.6pt of space stretchiness. That's 31pt, which is
around 10 characters of flexibility on a line, which should be enough for most
words, even without hyphenation.

But what if that isn't enough and TeX finds itself with a really long word that
it can't fit on a line? Then TeX enters its emergency paragraph breaking mode
where it starts getting a whole lot more relaxed about spaces. In this pass, TeX
in adds the `\emergencystretch` dimension of stretchability to a line. The
default in the ParaTExt macros is 1 inch. Thus in addition to the 31pt of
stretchiness, TeX now has an extra 72pt, at no extra cost, to work with. Now it
has 103pt of wiggle room, which is around 30 characters. Of course there may be
less spaces on such a line, but still that's a lot of space stretchiness to get
a non-overfull line break. If TeX uses all of that, and there are 4 spaces on
the line, then each line is going to be (39.6 + 72)/4 = 27.9pt which is a super
wide space, but at least there is no overfull line.

But what if this still isn't enough? There are a couple of options open to us.
The first is to increase the stretchiness of a space. This can be done within
ptxprint, allow the maximum width to increase to 499% and also decrease the
minimum width to say 50%. This makes a Charis space at 11pt a piece of glue that
is 3.3pt plus 13.3pt minus 1.65pt. This allows a single space to grow to 63pt
before any emergency stretch kicks in.

It is also possible to increase
`\emergencystretch` for those worst case scenarios. The problem here is that if
the emergency pass runs, then the emergencystretch is added at no extra cost
which can result in TeX preferring an extra wide space on a line over a hyphen
break, for example. So changing `\emergencystretch` should be done with care.
This also explains why the ParaTExt macros don't make \emergencystretch large,
otherwise if someone wants to stretch a paragraph that has been through an
emergency pass, they may find all the space added on the first few lines which
will look terrible while TeX things they are fine.

Do bear in mind through all this that even with lots of stretchiness, TeX will
still do its best to come up with the best looking lines it can. Increased space
stretchiness makes it easier for TeX to widen and shrink spaces at the expense
of other things like hyphenation. There is no one set of values fits all, hence
the ability to change them.

## Strategies

What are some strategies for handling bad lines:

- Find a way to break long words. There are various ways of adding discretionary
  hyphen (or even non-hyphen) breaks into words. There are hyphenation tables,
  soft hyphens (U+00AD) inserted by changes or manually.
- Increase the stretchiness of spaces
- Increase `\emergencystretch`

More radical approaches include increasing the shrinkage between base
characters. It is not wise to add stretchy space between characters because if
the glue ratio ends up being large, those spaces can become very obvious and
look like normal spaces. Increasing such shrinkage is unlikely to help address
the long words issue since even allowing 0.1pt shrinkage across say 50
characters will only give 5pt extra of wriggle room.


