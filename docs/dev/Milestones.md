# Extended Markers

This document discusses different schemes for encoding different aspects of
marker semantic styling into the style `\Marker` entry.

## Use Cases

It would be helpful to have some driving use cases to consider.

### Words of Jesus

The words of Jesus can run to multiple paragraphs

```
\p
\v 2 And he opened his mouth and taught them, saying:
\p
\v 3 \wj-s\* "Blessed are the poor in spirit, for theirs is the kingdom of heaven.
\p
\v 4 "Blessed are those who mourn, for they shall be comforted.
 ...
\c 7
 ...
\s Build Your House on the Rock
\p
 ...
\v 27 ... and it fell, and great was the fall of it."\wj-e\*
```

#### Discussion

One of the problems of a text like this is whether we need to turn off `\wj` for
subheadings. One way around this is explicitly colour text that doesn't change
colour for `wj`. Thus verse numbers and subheadings might get `\Color #000000`.

### Actor Script Markup

This is a similar problem to the words of Jesus but with the extra issue of
parameterised milestones:

```
\v 15 He sad to them, \qt-s |Jesus\* "But who do you say that I am?"\qt-e\*
\v 16 Simon Peter replied, \qt-s |Peter\* "You are the Christ, the Son of the
living God."\qt-e\*
```
### Table of Contents

Table of contents generation in TeX is a bit of a pain because there is no start
or finish marker to the complete table, so it is not possible to add a top level
category. So one approach might be:

```
\tr \cat toc\cat* \tc1 Matthew \tc2 MAT \tcr3 12
\tr \cat toc\cat* \tc1 Mark    \tc2 MRK \tcr3 75
```


## Markup Actions

### Simple Milestone

A simple milestone is unparameterised and used for simple character styling. For
example `\wj-s\*` to start a block of words of Jesus that can span multiple
paragraphs ending with `\wj-e\*`.

```
1.  wj-s
2.  ms:wj
3.  ms:|wj
4.  ms:wj|*
```

Approach 1 is the simplest in terms of the user just adding styling to an
existing miletone marker description. The question is whether it scales well or
whether it needs to. Approach 2 is half-way to being consistent with other
milestones. Approach 3 is fully conformant with a model that supports approach 2
in the next question, but it is very unwieldy.

Approach 4 takes a different path and describes how markers with a milestone
grouping should be styled. Thus one could more explicitly style `ms:wj|p` with
the wildcard `ms:wj|*` as the fallback, before considering the `p` marker. Would
this imply having to give all the paragraph styling for `ms:wj|p` or would both
`p` and `ms:wj|p` be processed inside a '\p \wj-s\* text \wj-e\*` block? It is
addressing the nastiness of something like `wj-s+p` or worse `ms:Jesus|qt+p`.
But the question remains how often does one want to change the styling of one
marker inside another other than with regard to the character styling a
milestone marker might add.

### Default Parameterised Milestone

This is a milestone that takes a default attribute. For example `\qt-s
|Jesus\*`.

```
1.  qt-Jesus
2.  ms:Jesus|qt
```

Approach 1 looks easy but there are a number of moving parts here, not least
that this wouldn't work for `\qt-s |s\*` since that would be indistinguishable
with `\qt-s\*`. But this may not be important. Approach 2 is in keeping with
default attributes and a generalised milestone marker model.

### Multiply Parameterised Milestone

This is where a milestone is explicitly attributed with multiple attributes. For
a hypothetical example: `\qt-s |who=Jesus|style=story\*`.

```
1.  qt-Jesus-story
2.  ms:who=Jesus;style=story|qt
```

Approach 1 extends the approach 1 for the default parameterised milestone. It
raises a number of questions: how do we map from named attributes to an ordered
list of unnamed attributes? Approach 2 is precise but still suffers from the
ordering question. In addition, does this mean that `ms:who=Jesus|qt` is to be
supported for `\qt-s |Jesus\*` as well?

### Default Attributed Character Style

This is where attributes are used in a character style using default attributes.
For example `\wit word|agloss\wit*`. The first, unattributed text content is
assumed to be marked with `\wit`. The question is how do we style the `agloss`
text?

```
1.  at:wit
2.  at:gloss|wit
```

### Active Categories: Containing Block

This is where a `\cat` occurs inside a block. How do we refer to the styling of
the containing block? For example: `\ecbs \cat People\cat* \p \ecbe`

```
1.  cat:People|ecbs
```

### Active Categories: Markers within the Block

This is for the markers in the categorised block. For example: `\ecbs \cat
People\cat* \p \ecbe`. Notice that the precised block type is not of concern
here.

```
1.  cat:People|p
```

