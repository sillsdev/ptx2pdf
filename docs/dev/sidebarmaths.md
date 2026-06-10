# Sidebar maths
### Purpose
This document is an attempt to document the different supplied and derived parameters that affect border layouts and sidebar dimensions. i.e. it will hopefully become a quick-reference to developers if something is going wrong.

## Padding: Borders, boxes and text
* The text is in the middle (unsurprisingly).
* The background-colour box (if present) extends past the edge of the text. `\BoxPadding` and sub-values defines how far the box edge is from the text.
* The border goes around the coloured box `\BorderPadding` and subvalues define how far the inside edge of the border is from the edge of the background box. If the desire is for the border to be fully or partially inside the box, then the negative `\BorderPadding` can do this.
* IF the border is touching the edge of the paper/etc, then `\BorderMargin` specifies empty space outside the border. I.e. for a full page sidebar this allows the border to not be touching the edge of the paper. 

### User-defined values
Stylesheet | getsbp@ram  | TeX value | Default | typical expansion
---------------|--------| --------|----------|------
\BorderWidth | borderwidth |\b@drwidth | \defaultBorderWidth|  0
\BoxTPadding | boxtpadding |\fb@tpadding | \fb@dfltpad |  5pt
\BoxBPadding | boxbpadding |\fb@bpadding | \fb@dfltpad|  5pt
\BoxLPadding | boxlpadding |\fb@lpadding| \fb@dfltpad|  5pt
\BoxRPadding | boxrpadding |\fb@rpadding| \fb@dfltpad|  5pt
\BorderTPadding | bordertpadding |\border@tpadding | 0pt*| 0pt
\BorderBPadding | borderbpadding |\border@bpadding |0pt*|  0pt
\BorderLPadding | borderlpadding |\border@lpadding |0pt*| 0pt
\BorderRPadding | borderrpadding |\border@rpadding |0pt*|  0pt
\BorderTMargin | bordertmargin |\border@tmargin | 0pt| 0pt
\BorderBMargin | borderbmargin |\border@bmargin |0pt|  0pt
\BorderLMargin | borderlmargin |\border@lmargin |0pt| 0pt
\BorderRMargin | borderrmargin |\border@rmargin |0pt|  0pt

Notes:
* For a page-filling sidebar, such as a cover, the default is `-\b@drwidth pt`.
The default definitions to the defaults above are: `\def\fb@dfltpad{1}`
`\def\defaultBorderWidth{0}`

### Controls:
`\BoxLikeBordertrue` - normal behaviour. If set to false, then old behaviour is selected, and the box does not contribute vertical space.

## Calculated parameters
These are almost universally globally defined and wrapped in `\the\dimexpr... \relax`, which is removed for brevity. Many include `\ifx\b@drtop\tr@e ...\fi` or similar, which  tests whether a border is being drawn at the top (or other) edge. These have be expressed as BDR()
Others include `\ifb@dr@t@os`, which further tests whether the border is outside the box, (and implicitly includes the BDR() test). These tests have been expressed as OUT()

TeX id|Description|Calculation|Notes
---------|------------|----------------|-----
\b@dr@top@pad | Distance between top of text and outside of border.|  `\fb@tpadding  +\border@tpadding`  BDR(`+ \b@drwidth pt`)| `0pt` if (no border at all and filling page) or \BoxLikeBorderfalse
\b@dr@bot@pad | Distance between bottom of text and outside of border. |`\fb@bpadding  +\border@bpadding` \BDR(`+ \b@drwidth pt`) | `0pt` if (no border at all and filling page) or \BoxLikeBorderfalse
\b@dr@left@pad | Distance between edge of text and outside of border| `\fb@lpadding` BDR(`\border@lpadding + \b@drwidth pt)` |`0pt` if \BoxLikeBorderfalse and no border at all.
\b@dr@right@pad | Distance between edge of text and outside of border| `\fb@rpadding` BDR(` +\border@rpadding + \b@drwidth pt`)|`0pt` if \BoxLikeBorderfalse and no border at all.
\b@dr@top@edge|Outer edge of the border or box, relative to text| OUT(`\border@tpadding + \b@drwidth pt`)   `+\fb@tpadding` 
\b@dr@bot@edge|Outer edge of border or box, relative to text|OUT( `\border@bpadding + \b@drwidth pt`)  `+\fb@bpadding`
\b@x@lunpad|Left border relative to box|OUT(`-\b@drwidth pt -\border@lpadding`)
\b@x@runpad|Right border relative to box|BDR(`-\b@drwidth pt -\border@rpadding`)
\b@xintadj|Internal adjustment|` \b@dr@top@edge - \b@dr@top@pad`|There was a time when boxintadj occured between the border and the text, and boxextadj occurred outside the border. This no longer seems  true.
\b@xextadj|Adjust above and below the box so that the top of the box is at the page top|` \ifdim\border@bpadding< -\b@drwidth pt` BDR{bottom}(`-\b@drwidth pt  -\border@bpadding`) `\else 0pt \fi` | Surely this should be looking at BDR{top} and tpadding?
