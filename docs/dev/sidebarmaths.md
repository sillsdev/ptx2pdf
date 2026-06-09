# Sidebar maths
### Purpose
This document is an attempt to document the different supplied and derived parameters that affect border layouts and sidebar dimensions. i.e. it will hopefully become a quick-reference to developers if something is going wrong.

## Padding: Borders, boxes and text
* The text is in the middle (unsurprisingly).
* The background-colour box (if present) extends past the edge of the text. `\BoxPadding` and sub-values defines how far the box edge is from the text.
* The border goes around the coloured box `\BorderPadding` and subvalues define how far the inside edge of the border is from the edge of the background box.

### User-defined values
Stylesheet | getsbp@ram  | TeX value | Default | typical expansion
---------------|--------| --------|----------|------
\BorderWidth | borderwidth |\b@drwidth | \defaultBorderWidth|  0
\BoxTPadding | boxtpadding |\fb@tpadding | \fb@dfltpad |  5pt
\BoxBPadding | boxbpadding |\fb@bpadding | \fb@dfltpad|  5pt
\BoxLPadding | boxlpadding |\fb@lpadding| \fb@dfltpad|  5pt
\BoxRPadding | boxrpadding |\fb@rpadding| \fb@dfltpad|  5pt
\BorderTPadding | bordertpadding |\border@tpadding | 0pt*| 0pt
\BorderBPadding | borderbpadding |\border@tpadding |0pt*|  0pt
\BorderLPadding | borderlpadding |\border@tpadding |0pt*| 0pt
\BorderRPadding | borderrpadding |\border@tpadding |0pt*|  0pt

Notes:
* For a page-filling sidebar, such as a cover, the default is `-\b@drwidth pt`.
The default definitions to the defaults above are: `\def\fb@dfltpad{1}`
`\def\defaultBorderWidth{0}`

### Controls:
`\BoxLikeBordertrue` - normal behaviour. If set to false, then old behaviour is selected, and the box does not contribute vertical space.

## Calculated parameters
These are almost universally globally defined and wrapped in `\the\dimexpr... \relax`, which is removed for brevity. Many include `\ifx\b@drtop\tr@e ...\fi` or similar, which  tests whether a border is being drawn at the top (or other) edge. These have be expressed as BDR()

TeX id|Description|Calculation|Notes
---------|------------|----------------|-----
\b@dr@top@pad | Distance between top of text and outside of border.|  `\fb@tpadding  +\border@tpadding`  BDR(`+ \b@drwidth pt`)| `0pt` if (no border at all and filling page) or \BoxLikeBorderfalse
\b@dr@bot@pad | Distance between bottom of text and outside of border. |`\fb@bpadding  +\border@bpadding` \BDR(`+ \b@drwidth pt`) | `0pt` if (no border at all and filling page) or \BoxLikeBorderfalse
\b@dr@left@pad | Distance between edge of text and outside of border| `\fb@lpadding` BDR(`\border@lpadding + \b@drwidth pt)` |`0pt` if \BoxLikeBorderfalse and no border at all.
\b@dr@right@pad | Distance between edge of text and outside of border| `\fb@rpadding` BDR(` +\border@rpadding + \b@drwidth pt`)|`0pt` if \BoxLikeBorderfalse and no border at all.
\b@dr@top@edge|Outer edge of the border or box, relative to text| `\ifdim  \border@tpadding > -\b@drwidth pt` `\border@tpadding + \b@drwidth pt`  `\fi`  `+\fb@tpadding` 
\b@dr@bot@edge|Outer edge of border or box, relative to text|`\ifdim  \border@bpadding > -\b@drwidth pt`   `\border@bpadding + \b@drwidth pt` `\fi`  `+\fb@bpadding`
\b@x@lunpad|Left border relative to box|BDR(`-\b@drwidth pt -\border@lpadding`)
\b@x@runpad|Right border relative to box|BDR(`-\b@drwidth pt -\border@rpadding`)
\b@xintadj|Internal adjustment|` \b@dr@top@edge - \b@dr@top@pad`|There was a time when boxintadj occured between the border and the text, and boxextadj occurred outside the border. This no longer seems  true.
\b@xextadj|Adjust above and below the box so that the top of the box is at the page top|` \ifdim\border@bpadding< -\b@drwidth pt` BDR{bottom}(`-\b@drwidth pt  -\border@bpadding`) `\else 0pt \fi` | Surely this should be looking at BDR{top} and tpadding?
