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

1) One of the problems of a text like this is whether we need to turn off `\wj` for
subheadings. One way around this is explicitly colour text that doesn't change
colour for `wj`. Thus verse numbers and subheadings might get `\Color #000000`.

2) The above assumes that `\wj-s` takes on the attributes of `\wj`. DJG's
original understanding of the USFM standard was that this was true, but a 2nd
re-read convinced him it wasn't. He's now confused about what is intended in the
standard. ```\qt-s \* ...\qt-e\* ``` while quoted text as in who is saying what, seems
distinct to ```\qt``` 'quoted text from the Old Testament'.

The milestone certainly gets a different treatment to the character stle in the style sheet.


### Actor Script Markup

This is a similar problem to the words of Jesus but with the extra issue of
parameterised milestones:

```
\v 15 He sad to them, \qt-s |Jesus\* "But who do you say that I am?"\qt-e\*
\v 16 Simon Peter replied, \qt-s |Peter\* "You are the Christ, the Son of the
living God."\qt-e\*
```

### Unchecked work

This has been raised on the paratext help page. Someone wanted to use a
milestone to mark unchecked work. 

In this example, ```\ip``` may have a colour associated with it, let's assume
it's grey. And that ```\sts|unchecked```  is coloured blue.
("Dear friends, we've done some revision, what do you think of the text in blue,
is it OK?").

```
\c 1
\ip Checked intro text
\sts-s |unchecked\*
However this bit isn't checked

\ip A whole unchecked paragraph

\sts-e\*
```
#### Discussion

The example above for the words of Jesus *implicitly assumes* that an ```\s```
within a milestone block is above (takes precedece over) the milestone marker.  

The transition from ```\ip``` to milestone markup assumes that the
milestone's markup takes precedence over the the paragraph style.

Things are fine up to this point. However, by the logic that gives ```\s```
precedence over the milestone, any font-styling applied by the mid-milestone 
```\ip``` will override the milestone's formatting, giving the impression that
"A whole uncheced paragraph" is original text.

This could be solved by:
1. Stacking (```\Marker sts+ip```)
2. Some additional clue or category being given to the code so that some
milestones always 'float' to the top of the stack (```\sts```) while others 
(```\qt```) remain in their normal position. 
3. A CSS-like `important` flag on some parameters.

Of these options, (1) is on the roadmap, but requires thought / checking of the
uses of the markers, to determine if it might be useful. (2) would be 
relatively easy to code. (3) would be fully flexible but complex to code /
troubleshoot.

### Table of Contents

Table of contents generation in TeX is a bit of a pain because there is no start
or finish marker to the complete table, so it is not possible to add a top level
category. So one approach might be:

```
\tr \cat toc\cat* \tc1 Matthew \tc2 MAT \tcr3 12
\tr \cat toc\cat* \tc1 Mark    \tc2 MRK \tcr3 75
```

Alternatively, an 'inline' `\esb` could be used, could be used to delimit the
table.

## Markup Actions

### Simple Milestone

A simple milestone is unparameterised and used for simple character styling. For
example `\wj-s\*` to start a block of words of Jesus that can span multiple
paragraphs ending with `\wj-e\*`.

These might be styled in various methods:
```
1.  \Marker wj-s
2.  \Marker ms:wj
3.  \Marker ms:|wj
4.  \Marker ms:wj|*
```

Approach 1 is the simplest in terms of the user just adding styling to an
existing miletone marker description. The question is whether it scales well or
whether it needs to. Approach 2 is half-way to being consistent with the
category-style mark-up initially used for milestones.

Approach 3 is fully conformant with a model that supports approach 2
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

We have gone with with approach one and with there being nothing syntactic about
the structure of a basic milestone marker. Thus `wj-s` is just a milestone
`wj-s` that happens to have an ending milestone `wj-e`. It is the presence of
the endmarker that indicates that the milestones are paired. Nothing about the
structure of the marker.

### Default Parameterised Milestone

This is a milestone that takes a default attribute. For example `\qt-s
|Jesus\*`.

```
1.  \Marker qt-Jesus
2.  \Marker qt-s-Jesus
3.  \Marker ms:Jesus|qt-s
4.  \Marker ms:who=Jesus|qt-s
5.  \Marker Jesus|qt-s
```

Approach 1 looks easy but there are a number of moving parts here, not least
that this wouldn't work for `\qt-s |s\*` since that would be indistinguishable
with `\qt-s\*`. But this may not be important. 
Approach 2 is the current implementation.
Approach 3 is in keeping with category-markup and a generalised milestone marker model.
Approach 4 is suggested by the Milestones with multiple attributes below.
Approach 5 carries the unmarked content without needing extra namespace
handling.

[MH] I like both 4 & 5 and suggest we support both with 4 taking precedence over
5. 

### Milestones with Multiple Attributes

This is where a milestone is explicitly attributed with multiple attributes. For
a hypothetical example: `\qt-s |who=Jesus|style=story\*`.

```
1.  \Marker qt-Jesus-story
2.  \Marker qt-s-Jesus-story
3.  \Marker ms:who=Jesus;style=story|qt
4.  \Marker ms:Jesus;style=story|qt
```

Approach 1 extends the approach 1 for the default parameterised milestone, approach 2 similarly. It
raises a number of questions: how do we map from named attributes to an ordered
list of unnamed attributes? (see the solution below)

Approach 3 is precise but still suffers from the
ordering question. In addition, does this mean that `ms:who="Jesus"|qt` would need to be
supported for `\qt-s |Jesus\*` as well? 

Approach 4 is a compromise, leaving the automatic (default) parameter unspecified, by specifying others.

The ordering issue can be dealt with by defining the 'cannonical order' as being 
the order of attributes within the stylesheet. This however leaves user-defined 
additional attributes in an undefined random order. Hopefully, however, a user who 
wishes to defined their own attributes and used them for styling is also capable 
of supplying their own ```\Attributes``` list in the stylesheet, and so 
this should not be an issue if documented.

However, in all of this, it is assumed to be incorrect to apply the (unique) id fields to such a list.

One important consideration is whether there is ever a use-case for a multiply 
parameterised milestones at all.

### Default Attributed Character Style

This is where attributes are used in a character style using default attributes.
Some attributes are expected to appear in the flow of the text (eg ```\rb
name|gloss \rb*```) while others are not (e.g. ```\w word | lemma \w*```).

For those where the text should appear, for example ```\wit word|agloss\wit*```
the text content is assumed to be styled with the normal marker `\wit`.
The question is how do we style the `agloss` text?

```
1.  \Marker at:wit
2.  \Marker at:gloss|wit
3.  \Marker wit-gloss
4.  \Marker wit:gloss
5.  \Marker wit(gloss)
6.  \Marker gloss|wit
```

Method 1 is deficient, not making any distinction between potential values e.g.:
```\w word | strong="124" lemma="something" \w*``` Method two is thus preferred 
over method 1.

Method 3. is simple and bears a striking similarlity to the simplest milestone
format, but while in milestones it was the *content* of the
attribute that defined the marker, here the content is displayed and the styling
is applied based on the *attribute* type. This may become confusing to people, hence 
methods 4 and 5 are suggested.

Method 6 follows on from method 5 for the simply parameterised milestone. Since
a marker can't be both a character style and a milestone in this way, we can
re-use the principle. Notice that whereas for the milestone the text before the
`|` is the content of an attribute, for the character style it is the attribute
name itself.

[MH] I like method 6 along with method 2 with method 2 taking precedence. Method
2 allows for multiply defined fields as for `\wit name|gloss="gloss"
morph="morphbreak"\wit*

```
1.  \Marker at:gloss;morph|wit
```

#### Disussion
While there are going to be distinct layouts for different markers/attributes there are some 
comonalities.
1. Colour size / position should be applied.

2. Full processing of these fragments as though they were full character styles
is NOT desirable, as that would clash with attribute parsing.

3. Disabling of display should be possible (i.e Publishable should be obeyed for
these semi-styles)

4. Some marker-specific layout options are going to be necessary, e.g.
colon-parsing for ruby glosses, as described in the USFM 3 docs.

5. A word-generic stacking mechanism may nonetheless be useful e.g. someone may 
want Strong's numbers or lemma  on a ```\w``` to be above/below the word rather
than a superscript. Also, of course multi-line interlinear text. It should not
be necessary to rewrite the USFM to apply these layout options.

### Active Categories: Containing Block

This is where a `\cat` occurs inside a block.  How do we refer to the styling of
the containing block? For example: 
```\esb \cat People\cat* \p  text \esbe```

```
1. \Marker cat:People|esb
```

This is only relevant to ```\esb``` blocks at present.

### Active Categories: Markers within the Block

This is for the markers in the categorised block (e.g. a footnote or sidebar).
For example: ```\esb \cat People\cat* \p \esbe```. Notice that the precise block
type is not of concern here.

```
1.  \Marker cat:People|p
```

Method 1 is the method in use in the current code. If there is no styling for
the specific value, the normal values for ```\p``` (etc) are used. 

