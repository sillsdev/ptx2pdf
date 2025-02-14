# Figures

Figures overlap the boundary between content and publication information. A
figure is often publication specific. For example, one might expect different
figures in different kinds of publications. There may well be more or less figures in a
print publication than a phone application.

In this section we discuss the layout information in a figure. We look at USFM2
and USFM3 issues and give details about various key attributes. Some of these
are new to ptxprint.

There are several picture line-formats available, depending if you're using USFM3.0 or the earlier standard, and whether a piclist is in use, e.g.:
- Inline USFM2 old: 
```
  \fig_DESC|FILE|SIZE|LOC|COPY|CAP|REF\fig*
```
- Inline USFM 3.0 (example):
```
  \fig The Caption.|src="co00621.jpg" size="span" alt="desc" loc="LOC" ref="1.18"\fig*
```

- Piclist, USFM old and USFM 3.0(example):
```
HEBR 3.9 Description of picture|co00621.jpg|col*0.5|cr2||The people worshipping idols having forgotten God|3:9
HEBR 3.9 The people worshipping idols having forgotten God|src="co00621.jpg" size="col*0.5" pgpos="cr2" ref="3:9" alt="Description of picture"
```

Paratext's  export to print-draft (versions 9.3 and below) removed picture formatting information before it gets to XeTeX.
PTXprint now strips out figure lines from Paratext-created files and generates a USFM-3 piclist from them. The figures are now deemed to be under the control of the (publication-specific) piclist, and modifications are neither returned to paratext nor updated from subsequent modifications in paratext.

The USFM-3 standard is not very useful here; for example, for
the `loc` attribute it says "a list of verses where it might be inserted", while paratext help suggests an entirely different use for this attribute. For size, USFM-3 only 'span' and 'col', with no scaling factor. The ptx2pdf XeTeX macros give better
control on both of these, offering multiple positioning options and if you want
a smaller image than full-page or column-width you can say, e.g. `span*0.6` (see
a later discussion also). They also add the extra sizes 'width', 'page' and 'full'. 
'Full' suppresses headers and footers.

## Attributes

The `loc` attribute is used in different ways, with only one of them being in
conformance with USFM standard:

1.  A scripture reference range at which the figure may be inserted.
2.  A page position (top right or bottom).
3.  A list of media identifiers (p for print, a for application, w for web).

Since USFM3 allows for any number of attributes, we can use different attributes
for these different uses.

1.  The scripture reference remains in the `loc` attribute as per the USFM
    specification.
2.  The page position is stored in the `pgpos` attribute. The format of the
    value is described below.
3.  The media identifiers are stored in the `media` attribute.

USFM2 does not allow for the addition of attributes and therefore ptxprint
parses the `LOC` column to work out how, in effect, to convert it to USFM3. If
the `LOC` column purely consists of `a` or `p` or `w` letters then it is
considered a `media` attribute. If it matches any of the values that a page
position can take, it is considered a `pgpos` attribute. If the value looks like
the start of a scripture reference, then it is a `loc` attribute.

Within the ptx macros, the `LOC` column is always interpreted as a `pgpos`
attribute. In addition, for USFM3, if there is only a `loc` attribute, it is
treated as a `pgpos` attribute for backward compatibility.

### pgpos Attribute

The `pgpos` attribute gives an instruction as to where on the page a figure should
be placed. Given that picture placement is highly specific to a particular
publication, it is advisable not to use `pgpos` in a USFM file itself, but to
use it in a piclist file. It can be used in a USFM file when a piclist is
unavailable, but users should recognise that in a different publication, the
typesetter will almost certainly change the page position.

An example of the `pgpos` attribute may be found in the piclist line shown in
the initial section above. In that line (for the *right* column of a diglot, hence the `R`
after the `HEB`), the picture will be set in a cut-out on the right side of the
column, two lines below the beginning of the paragraph starting at 3:9, with the
picture half a column wide and the text a little distance away. 

In the table below, 'left-align
#### Out of flow positions
These positions do not depend on where the trigger-text is on the page, as they are referenced to the 
physical page.

Code | Mnemonic              | Position                                                      | Max. caption width 
---- | -----------------------|-----------------------------------------------------------|-----------------------------------------------
t    | 'Top'                  | Above everything except the header line.                        | across both columns 
b    | 'Bottom'               | Below all verse text (and footnotes in diglot).                 | across both columns 
V    | 'very Bottom'               | Below everything, including footnotes.                 | across both columns 
tl   | 'Top-Left'    [^1]      | At the top of the left-hand [^2] column                          | width of column 
bl   | 'Bottoom-Left'    [^1]  | At the bottom of the left-hand [^2] column                          | width of column 
-----|------------------------|       ***Polyglot  Additions***                              |----------------------------
tL   | 'Top-of-L'	      | At the top of column L (substitute L for R, A, B...)		| width of column
bL   | 'Bottom-of-L'	      | At the top of column L						| width of column

[^1]: Only if two columns are in use. `tr`and `br` of course exist as well.

[^2]: If a diglot is being set inner-outer rather than left/right, then the 'left' column is the inner column. 

####  PTXprint Additional Positions 
Additional positions defined by PTXprint have a 1 or 2 letter code. Some 2 letter codes are then followed by a number, others by another letter.  The first letter can be considered the **class** or type of image placement, the second, the (horizontal) **alignment**. For some position classes, the alignment is optional, in which case the default alignment is centred.

##### Alignment codes
The alignment codes (2nd letter) are:

*  `c` centred 
*  `l` (Left)  or `r` (Right) 
*  `i` (Inner) and `o` (Outer). Where inner means closest to the binding, and outer means furthest from the
binding.

Left and right aligned images have a caption-space the same width as the image. Centred images have a caption space equal to the width of the space they are in.

##### Class codes
In the table below, * is used to indicate any of the alignment positions above, X is used to indicate any alignment except `c`.
The third code is always optional. `#` indicates a number (integer) e.g. 2 or (decimal) e.g. 3.2.   @ indicates that the third parameter is a vertical alignment, for which values can be `t`-top, `b`-bottom, `c`-centre or (for sidebars) `f`- fill page height if possible (stretch vertical spaces).

Class | Mnemonic              | Description
---- | -----------------------|----------------------
h    | 'Here'                 | Line above where defined / before the verse in piclist 
j    | 'Just below'                 | Line below where defined / before the verse in piclist
H | 'HERE as cHaracter' |  In the exact location, as if a character. 
p    | 'Post-paragraph'       | After this paragraph[^4],[^7]
p*#  | 'Post-paragraph'       | After # (integer) paragraphs[^4],[^5] 
cX   | 'Cutout Left'          | A notch/corner cut out of the text, starting at current line 
cX#  | 'Cutout Left'          | A notch starting #(decimal) lines[^6] below the current line
P    | 'Page'                 | An image that replaces the normal text on the page
P*@   | 'Page'                 |  As above, but horizontaly and vertically aligned[^8]
F   | 'Full page'            | The entirety of the paper [^9] 
F*@ | 'Full page'  | The entirety of the paper [^9]  but horizontally and vertically aligned.[^8]

   
[^4]: The 'insert image here' code will be activated at the end of the paragraph.
    
[^5]:     Counting starts at the paragraph containing the verse number or the \fig
    definition. i.e. `pc1` 'after one paragraph' is interpreted as meaning the same as p or pc.)
    `pc2`  means after the next paragraph. This is useful if the verse contains poetry.
    
[^6]: Multi-digit numbers may be specified, but little sanity checking is done.
    The image will *always* be on the same page/column as the anchor (normally 
    a verse);  It may occur off the page's bottom, even if the notch is partly
    or fully on the next. A negative number (e.g. cr-1) will raise the image and
    cut-out, but while this can raise the image into the preceding paragraph, 
    it  cannot make the cutout begin earlier than the paragraph containing the anchor.
    A fractional number (e.g. cr0.2) will adjust the image by a fractional
    amount within the cutout. i.e. cr1.9 will be 0.1 lines higher than cr2. 
    cr1.5 is treated as cr2 (two full-width lines before the image) with an
    adjustment of -0.5lines, cr1.4999 as cr1 with an adjustment of +0.4999 lines.
    
[^7]: Since `p` is also interpretable as a media target, `pc` should always be
    used in USFM-2.
    
[^8]: Use `b` for bottom alignment, or `c` for explicit central vertical alignment. 
    If a vertical alignment is specified, then the image will be the only image
    on the page, even if another image would also fit. If no vertical
    alignment is specified, then the image will normally be centred vertically,
    but an additional image or images may be fitted onto the page if there is space.
    
[^9]: If the image is not the same aspect ratio as the page, or a scaling factor is used, 
    there may be some space. For this reason, the alignment options are available.
    Full page images have no header or footer, and using a caption with them 
    is normally a mistake leading to part of the image or caption. 
    Alignment actively attempts to get the picture/caption to the
    specified edge of the page. ```\FullPageFudgeFactor``` (normally defined to
    be 0pt) is available for tweaking if top alignment does not actually coincide 
    with the top of the image. 

#### Restrictions  / notes on certain picture positions
- p : The delayed picture is saved until the end of the Nth paragraph in a
  certain 'box'. There is no code to have an adjustable stack of boxes 
  but multiple images can now be put into the same after-paragraph box 
  Diglots have a separate boxes for each column.
  
- F : 
   If a caption is used, this will normally be off the page. It may,
     however, still affect the alignment of the image, preventing top / bottom alignment from 
     functioning correctly. Thus captions should *not* be used in connection with full-page 
     images that approach the page edges.
     
- c : The interaction between automatic paragraph breaking, page balancing 
  and cutout positioning can result in loops where the code would not find a
  solution without hysterisis (slop). The addition of hysterisis, however,
  means that different runs of the input may result in different final solutions. 
  If reproducing a file exactly is required, e.g. for archiving, the `.parlocs`
  file should be retained.

  The undersired loop occurs like this:

  Run 1 calculates the position for the cutout, but when cutout is positioned
  during run 2, that moves the anchor, meaning that next time the cutout moves to
  a position that allows the anchor to return to the position it was in during run 1. 

  This is most common when the cutout is anchored late in the paragraph.
  While some hysterisis is already permitted, it may be that this is insufficient for 
  every case.  There are two possible solutions: 
   a. Pick an earlier anchor, with a corresponding increase in the 'after # lines' number.
   b. Use ```\setCutoutSlop```

#### ```\setCutoutSlop``` - defining cutout offset permission.

The TeX code allows a small amount of hysterisis (slop) in the positioning of
cutouts that cannot be placed immediately.  (The default slop is 1 line higher
for chapter numbers, +/- 2 relative to 'perfect' for most other cutouts).  This
might mean, for instance, that if run 1 calculated that an in-cutout image
should ideally start at line 14 in a given paragraph, if on the next run  it
finds the anchor-point has moved and the cutout should now be on line 13 or 15
the code considers this acceptable.  Rather than adjusting the shape of the
paragraph again (which risks moving the anchor point again), an annotation is
made to the `.delayed` file that the image is to raised or lowered relative to
the anchor point to fit into the cutout.  The following command allows
`droppic4` (image number 4, in a cutout analogous to a drop-cap)  to accept
being raised by 3 lines or lowered by two.

```
\setCutoutSlop{droppic4}{3}{2}
```

It is not recommended to try to guess the image count by counting images, 
as sidebars may also increase the number. Furthermore, some numbers may  
be skipped. Instead, the `.delayed` file could be inspected. It will have a 
format similar to this, with only the items which might be subject to these
slop calculations included. The first item after '\DelayedItem` is the 
name that should be supplied to `\setCutoutSlop`.

```
\DelayedItem{dropsidebarBox1}{GEN1.5}{2}{(95.354ptx12@2)R}
\DelayedItem{dropgraphicInSidebar2}{GEN2.12}{1}{(53.677ptx3@1)R}
\RaiseItem{droppic6}{TST1.7-preverse}{2}
\DelayedItem{droppic6}{TST1.7-preverse}{11}{(58.91803ptx8@-4)R}
```

 
## Do the new picture positions conform to examples in the USFM specification?
In some ways, they conform better than the previously available options. USFM
specification indicates that a picture can occur immediately after text, ending
the previous paragraph. This works with *here* picture locations, except that the 
paragraph is not ended.

USFM makes no reference to left or right alignment, nor scaling images, nor
images in cutouts.
 
#### Why might I use unusual positions?
- cl / cr  Small images, perhaps glossary items? Or in a single column printout.
- p  A picture to be set after the final verse of a book, otherwise impossible
  from a piclist. Possibly also for some kind of decorative 'end of section'
  mark.
- hl / hr Handy for a sponsor's or publisher's logo, perhaps?
- H Perhaps a small logo.  Use with large sizes or with a caption is discouraged, as it could easily overwrite text above or distort the grid) 

### size Attribute

Valid values for this attribute are:

- `full`: the entire size of the paper, a page reserved for images.
- `page`: the normal printed area of the page, on a page reserved for images.
- `col`: the width of the current column (only valid for 2 column text or diglot).
- `span`: the width of the normal printed area of the page.
- `width`: the full width of the paper 
- `font`: the current font height (added for position H)
- `line`: the current line height (added for position H)

The `size` attribute has been extended to support scaling. Following the `col`
or `span` values, there may be an optional `*` followed by scale factor, with
1.0 being the unity scaling.  The separate `scale` attribute is to be preferred in USMF3 files. For example in a piclist:

```
RUT 4.11 Boaz addresses the crowd|07.jpeg|span*0.6|t|Artist McArty| You are witnesses |Ruth 4:10|rotated 3|
```
The `span*0.6` says the figure should be scaled to span the page and then scaled
down to 60% of that size.

### scale Attribute

While in USFM2 the `size` attribute position has been extended to support a
scale factor via `*`. This is not ideal and in USFM3 it is better to separate
the scale factor into its own `scale` attribute. This value is a multiplier that
scales an image after its size has been established via the `size` attribute. A
value of `1.0` implies no size change.

### x-spacebeside Attribute 

An image in a cutout needs some space beside it, so that the text does not touch the image.
This can be controlled globally by putting a different distance in the the configuration 
parameter `\def\DefaultSpaceBeside{10pt}` If a particular figure needs a different value,
this can be controlled by setting the x-spacebeside USFM3 attribute. e.g.
`x-spacebeside="15pt"` This attribute is only relevant for figures in cutouts.
Sidebars in cutouts may set the `\SpaceBeside` value in the appropriate
stylesheet. Note that the code currently assumes no one will have a cutout 'foreground' image in a sidebar that is itself in a cutout, and uses
`\SpaceBeside` for both cutouts. The image-specific `x-spacebeside` setting can override this.

#### x-spacebeside in pgpos "H"
Similarly to cutouts, the `H` (HERE/cHaracter-like) page position normally needs some extra space so that it does not touch text. The  values  mentioned above all apply. If the pgpos is `"H"` or `"Hc"`, then that additional space is evenly distributed on both sides of the image. If pgpos is `Hl` or `Hr` then the additional space is all on one side.

### x-spacebefore and x-spaceafter Attributes - Additional whitespace
Figures by default have a small amount of space  above or below them (0.3 and
0.5 of the main lineskip respectively), depending where the caption is (the space 
taking the place of the caption). Additionally they may have additional
whitespace before and after them. This is controlled by the 
USFM-3 parameters `x-spacebefore` and `x-spaceafter`. Alternatively, the
stylesheet parameters `\SpaceBefore` and `\SpaceAfter` will alter the 
default value for all matching figures inserted via the `\fig` mechanism
(including figures from piclists). 
Sidebars similarly have these stylesheet
parameters.  

'Matching figures' above means that figure location (pgpos value) should be specified:

```
\Marker loc:cr|fig
\SpaceBefore 0
\SpaceAfter 0
\SpaceBeside 15
```

### x-edgeadjust Attribute
 `x-edgeadjust` moves the image relative to the margin, like indentation does to text.  As the same units are used, a figure 
with `x-edgeadjust="0.25"`and  `pgpos="hl"` will align with the left-hand edge of a paragraph with an indentation of 0.25. 
Negative numbers will cause the image to extend into the respective margin. Note that sidebars can be similarly adjusted 
via their `\FirstLineIndent` parameter

### x-xetex Attribute - Rotation control and PDF page selection 
#### Rotation
To allow further transforming of images when inserting into the publication,
ptxprint and the ptx macros support an optional 7th column in a USFM2 `\fig`
element, which corresponds to the `x-xetex` USFM3 attribute. It consists of a
space separated list of items. If the item is of the form key=value, it is interpreted, 
otherwise it is passed on to the ```\XeTeXpicFile``` or ```\XeTeXpdfFile```  

- `rotated` _degrees_ Rotates the image anticlockwise the given number of degrees.
- `rotate=edge` Rotates the image so the top is at the outside  edge of the page.
- `rotate=binding` Rotates the image so the top is at the binding edge.
- `rotate=odd=_degrees_` Rotates the image anticlockwise by the given number of degrees on odd pages.
- `rotate=even=_degrees_` Rotates the image anticlockwise by the given number of degrees on even pages.

For example, in the piclist entry from the previous section, the image is rotated anticlockwise by 3 degrees.

As yet, there is no mechanism to rotate the caption with the picture.

#### PDF page selection
The `x-xetex` attribute can also be used to select which page of a multipage PDF file is chosen to provide an image. It can be combined with rotation  E.g.  `x-xetex="rotate=binding page=2"`  would select the second page of the PDF and rotate it so the image 'up' is at the binding.

### media Attribute

The media attribute consists of a string of single letter media types for which
this figure is intended. It is currently ignored in the ptx macros and all
images are included.

- `a` Include in scripture applications, like Scripture App Builder.
- `p` Include in print publications.
- `w` Include in web page presentations of the text.

### mirror Attribute

Sometimes the people in the picture are just looking the wrong way. Sometimes it
would be good to have the picture mirrored. In fact you might want it mirrored
only on left, or right pages or both. The `mirror` tells the ptx macros when
to mirror the picture. The possible values are:

- `odd` Mirror on odd pages
- `even` Mirror on even pages
- `both` Mirror on all pages 
NB: the odd/even behaviour requires a second XeTeX run to get things right.

### Credit Attributes

While not part of USFM, the XeTeX code recognises the following USFM-3 style attributes 
to over-print a small piece of text on the image, intended for giving credit to the artist. (while the following is 
true at the time of writing, the 'ink is not dry' and there will probably be changes).
- `x-credit="© A.Artist"` The text to print.
- `x-creditpos="to"` The position in which the text should go. Two letters are
  expected, the first being vertical position (t/c/b for top, bottom, centre),
  the second being horizontal (l/c/r/i/o for left, centre, right, inner, outer).  (here: top,
  and the edge closest to the outer-edge of the book).  (Default: `ti`)
- `x-creditrot="-90"` Rotation of the credit text (Default: depends on the location of the text. 
 At left and right edges, the text is rotated so that the text is bottom-to-edge).
- `x-creditbox="value"` Should the text be printed inside a box or not. The following values are understood:
   * A value of "true" (or "t") indicates that a box of the styling-defined  colour should be applied, or white if there is none.
   * A value of comprising of three numbers (e.g. "0.5 0.5 1.0") represents the Red, Green and Blue components of the box colour.
   This is simple but not a recommended approach as changing this styling element can quickly become time consuming.
   * Any other string (e.g. `x-creditbox="dark"`) specifies a particular styling set for the credit.

#### Styling of credit 
Similarly to other attributes, the  displayed attribute `x-credit` of marker
`\fig` can be styled in the following manner (by the XeTeX code, don't expect
this to work with Paratext or another program!):

```
\Marker x-credit|fig
\Font Andika
\FontSize 5
\Background 0.5 0.5 0.5

\Marker x-credit:box=dark|fig
\Font Andika
\FontSize 5
\Color xFFFFFE
\Background x1E1E3E

\Marker whitetext|x-credit
\Color xFFFFFE
\Background -
```

In the above, the normal fontsize (6 `\FontSizeUnit`s) is overridden, and the
font specified to be `Andika`. If a box is to be used, the default white is
replaced with a 50% gray, specified as 0.5 red, 0.5 green, 0.5 blue.

The second `\Marker` set specifies that for credits specified with
```x-creditbox="dark"```, a dark blue-gray box is written with (almost) white text on
it.  XeTeX's driver software treats pure white (`xFFFFFF`) for fonts as a magic
value meaning no colour change, so specifying pure white text does not
work.  Note the use of hexadecimal notation is possible only in the style file. 
It is not understood in the ```\fig``` line as the presence of spaces are used
to distinguish between a colour and a style label.

The third set demonstrates the alternative, shorthand styling name for the marker, 
and also that there's no need to re-specify the default parameters (defined by
```\Marker x-credit|fig```, and the special value of `-` for the `\Background`
parameter cancels the box for `creditbox="whitetext"` I.e.  there will be no
box for this item.

#### Moving the position of the credit box.
It was found that when positioned at the putative exact edge of an image, the
background box of the credit fails to fully hide the edge of the figure. The
exact reason for this has not been determined, and it may be deprendent on
XeTeX, graphics format or perhaps the PDF viewer.

To avoid a tiny sliver of the image showing, a small offset is given by the
configuration parameters `\FigCreditOverEdgeH` and `\FigCreditOverEdgeV`. These
move the credit and its box past where edge of the figure would be expected to
be, in the horizontal and vertical dimension respectively. 
They are global values, affecting the credits on any figures.

```
\FigCreditOverEdgeH=0.07pt
\FigCreditOverEdgeV=0.07pt
```

It was then realised that more significant values of these parameters might potentially
move the credit outside the area of the figure entirely. This effect can now be
utilised to control the position of all or of particular
credit box styles.  At present there is no per-image control.
Moving the text in a vertical dimension relative to the text
is set using the `\SpaceBefore` stylesheet value (adjusting
FigCreditOverEdgeH if the angle is +/-90 or FigCreditOverEdgeV otherwise) and similarly 
`\SpaceBeside` (overrides FigCreditOverEdgeV or FigCreditOverEdgeH), 
shifting the box sidewise relative to the text (unlike the values above,
positive values will shift it towards the center of the figure).

Note that while `\SpaceBefore` is normally measured in lines and `\SpaceBeside` in points,
 here both is interpreted as a measurement in points.  e.g.:
```
\Marker Outside|x-credit
\Color x000000
\Background -
\SpaceBefore 5
\SpaceBeside 3
 
\Marker x-credit
\SpaceBefore 0
\SpaceBeside 5
```
would mean that a  'vertical' credit box (rotation 90 degrees) selected with
x-creditbox="Outside" is pushed 5pt beyond the left or right edge of the
figure, and shifted 3pt in from the upper or lower edge, while other credit
boxes sit on the outer edge of the figure like normal, but are shifted along the
edge by 5 pt.


## Piclist files

Piclist files are a way of describing which figures should go where in a
publication without having to edit the USFM text itself. There are the preferred
way of specifying the figures to include in a publication.

Since the ptx macros will include figures from both a piclist file and from
`\fig` elements in the text, `\fig` elements are typically stripped from the
USFM file before being processed by the ptx macros. This is why Paratext strips
figures from the USFM passed to print draft. Ptxprint is more nuanced and has
options as to how a user would like figures handled.

A piclist file takes the same filename as the USFM file being processed by the
ptx macros but with an added extension of `.piclist` and in the Piclist folder,
specified to the macros. Ptxprint handles all this for the user.

Historically, piclists have used the TeX style comments, which meant that
percentage signs needed to be escaped `\%` to appear in the output. More
recently, there have been two changes to this: lines starting with a hash sign
(`#`) are now treated as comment lines. A hash sign is *not* treated as a
comment sign otherwise.  If, when the piclist is read `\PiclistLitPcttrue` has
been set, then percentage signs are treated as letters. If is not set (the 
default for the macros, but PTXprint now sets it), then
they retain their normal meaning in TeX, i.e. ignore the rest of the line.
Escaping a percentage sign needlessly does not cause problems.

There are two methods to read a piclist, in 'slurp' mode (`\picslurptrue`, the
default) where the entire file is read at once or the traditional mode
(`\picslurpfalse`) where the specification for only one picture is held in
memory at a time.  The traditional mode requires that pictures occur in the correct 
order (difficult in diglots, where the sequence of verses is not always
obvious) and errors in the reference (e.g. 'NUM 11.2' instead of 'NUM 11.2-3') 
are fairly easily identified because no pictures will be read after an unmatched
reference.

In 'slurp' mode, the there is no requirement that pictures occur in order. 
The code will count images defined vs images used, and give a list of unused
references if all are not used.

A piclist file has a strict format:

- Each entry is on a single line.
- Any characters after a % character are ignored
- Blank lines consisting only of whitespace (after % comment removal) are
  ignored.
- A piclist entry consists of an anchor reference followed by the contents of a
  `\fig` element (without the `\fig` markers) USFM2 or USFM3 format may be used.
- If processed with `\picslurpfalse` (see above), piclist entries must be in the  order they 
  will be met in reading the input. The ptx macros will read the next
  entry and if the anchor reference entry is before or equal to the anchor reference entry
  of the previous entry, it and all future piclist entries will be ignored.

Multiple lines *may* reference the same reference. In this case they will be
processed in strict order of definition. It is up to the user to ensure that
the combinations do not trigger an unprintable page.

### Anchor references
- The anchor for a chapter/verse reference is of the form ```_bk_ _C_._V_```,
  where ```_bk_``` is the 3 letter (all-caps) book identifier. The ```_C_```
  and ```_V_``` are chapter and verse references. The verse reference must 
  exactly match what comes after the `\v` tag. 
  The _bk_ may also have a 4th letter of `R` or `L` to indicate which side in a
  diglot is being referenced. Lack of a 4th letter implies it may be matched
  while processing either column, and the user has no preference about
  which font, etc. are used (normally `L` will match it first, but this is not guaranteed).
- The anchor for a key term (e.g. ```\k This (Odd) Term\k*```) is the book and
  the exact text (including punctuation) between `\k` and ```\k*```, but excluding
  any spaces. (i.e.  in the above example it will be ```_bk_ This(Odd)Term```
- The anchor for a stand-alone milestones is the book and the ```id```
  attribute for that marker e.g. ```\zfiga |id="rabbit123\*``` will trigger piclist 
  entries starting ```_bk_ rabbit123```  If ```id``` is the default attribute
  (as it is for ```\zfiga```, the shorter form ```\zfiga|rabbit123\*``` may also be used 
  in the USFM. Note that at present only stand-alone milestones trigger figure 
  inclusion, but there is nothing particularly magic about `\zfiga`, it's just a 'neutral' 
  stand-alone milestone.
- The anchor for the beginning of a book is ```_bk_ bookstart``` This anchor point was added to 
  allow the placement of whole-page images before any content of the book.
- A second or subsequent paragraph within a verse or keyterm entry, or after a stand-alone 
  milestone may be referenced  by appending a separator (by default an equals
  sign) and a number. e.g. ```_bk_ 1.2=3``` will trigger on the third paragraph
  within verse 2 of chapter 1. The following should be noted: 
  - There is only one paragraph counter which is reset at each change of
    trigger. Thus the above example *will not* trigger if there
    is no 3rd paragraph before the next verse number, nor will it trigger if some other
    potential anchor occurs.
  - As the first paragraph of the verse / key term is the one containing  that
    item, a suffix of ```=1``` is normally an invalid trigger point and will never match.
    The exception to this is when a *stand-alone milestone* **immediately** follows a paragraph break. 
    In that case the trigger will activate just before the first piece of actual text after the milestone, assuming there is some.
  - The code assumes that *any* occurrence of the separator in the piclist reference 
    means that what follows is a paragraph number. Using some other separator is now 
    supported, with the restriction that (a) it should not be expected to occur 
    in normal text of a type that might crop up in a key term. (b) it must not contain characters 
    with a special meaning within TeX (e.g. `#`, `$`, `%`, `{`, `}`). Multiple character separators 
    are permissible. The command  below (to be included in the `.tex` file
    before any piclists, etc. are loaded) sets the separator to be the sequence
    `=@=`, in case a simple = sign is used in the text of a keyword. Piclists would
    then need to specify paragraphs in form ```_bk_ 1.2=@=3``` A sequence of rare
    letters, such as `zqz` could also be used, provided none of these letters has been 
    declared active, e.g. by declaring that they should use the fallback font.
```
\SetTriggerParagraphSeparator{=@=}
```
### Reuse of piclist entries.
If it is desirable to have a particular piclist entry (including caption)
multiple times, then the following steps must be taken: 
1. Read the piclist to discover what TeX thinks the identity of image is - the anchor reference, and image number (starting at 1) at that anchor reference.
2. Inform TeX that the image is one that should be kept, in the controlling TeX file (or `ptxprint-mods.tex`). The format for this is either:	
  a. `\KeepFigure{`book`}{`Reference`}{`image Nr`}`
  b. `\KeepFigure{`book`}{`Reference`}{}`  (for all images on a given reference), or
  c. The boolean `\KeepAllFigurestrue`  Which prevents TeX from tidying up after itself everywhere.
3. Modify the USFM to trigger reuse the image. For an image triggered initially by `\zfiga`, then that simply means repeating the relevant `\zfiga` line.
For other images, e.g. those triggered from `\k`, or a specific chapter-verse, 
the `\zfiga` code must be identified. Some examples are given below:

```tex
\KeepFigure{MAT}{1.1}{1} % First figure in piclist at Matthew 1:1, or  \zfiga|1.1\* in MAT
\KeepFigure{GLO}{Borogroves}{2} % 2nd figure triggered by \zfiga|Borogroves\* in GLO
\KeepFigure{GLO}{k.Brillig}{1} % Triggered \k Brillig\* or \zfiga|k.Brillig\* in GLO
```

Note that while it is possible to select a subset of images triggered from a given 
anchor point (verse or other reference), there is no mechanism available for
reordering them. Nor is there any way to defend against reordering of multiple
images at the same anchor point within the piclist, if something (e.g. the
python code) alters the order.

## Captions

### Caption before the image
To position captions above the image rather than below, add this line to the .tex file:
```
\CaptionFirsttrue
```

### Reference before the caption text
To position the reference before the caption text, add this line to the .tex file:
```
\CaptionRefFirsttrue
```

### Decoration of the reference
 By default the reference (if present) follows the catption and is in (rounded) brackets. The code for this is:
```
\def\DecorateRef#1{(#1)}
```

An alternative definition of ```\DecorateRef``` could be given, in the .tex file, e.g.:
`\def\DecorateRef#1{#1}`
would give no decoration, and 
```
\def\DecorateRef#1{\emdash\NBSP #1}
```
would put an em-dash (unicode U-2014) and a non-breaking space before the reference. (`\emdash`, `\endash`, and various types of 
spaces such as `\NBSP`, `\EMSPACE`, `\THINSPACE`  are defined in the macros).

### Caption Alignment 
Captions are normally centred. If for some reason left-justified or right-justified captions are required, this can be controlled 
in the normal manner in the style sheet, via the `fig` marker, even though officially the marker is officially a character style, not a paragraph style:

```
\Marker fig
\Justification left
\LeftMargin 0.125

```
The text will align to the standard page edge, unless the margins are modified
as above. There is no support for controlling indentation of the first line or
other paragraphing style elements.

### Caption Gap Adjustment
The gap between the caption and the figure can be adjusted globally by the following definition:
```
\def\FigCaptionAdjust{0.0pt}
```
Per-image category adjustments are also possible. See below. 
### Caption font and size

As noted above, caption styling is controlled via the `fig` marker in the stylesheet. Font-related styles can be selected in the normal manner.
For multi-line captions, the line spacing may be controlled by modification of `\LineSpacing` (in the same scalable units as parameter `\FontSize`) or 
`\BaseLine` (units must be supplied).

### No Captions and references at all
```
\DoCaptionsfalse
```

## Image Categories
### Borders and backgrounds
If the (non-standard) `cat` attribute (e.g. `cat="myborder"`)  is specified in the piclist (or USFM3 attribute list), then sidebar-like borders and background colours may be specified for the image.
The border or frame is positioned relative to the image itself (i.e. excluding the caption).
For example:
![](imgs/rose_border.png)


was selected with `cat="dblborder"` and used these style settings:
```
\Marker cat:dblborder|fig
\BorderStyle double
\Border All
\BorderWidth 3
\BorderColour xff0000
\BoxPadding 4
\BorderPadding 0
\BgColour x0000ff 
\Alpha 0.1
```
The double-line style border uses a red (`xff0000`) line and the default black fill. As the `\BorderLineWidth` has not been specified, the default of 1/3 of the border thickness is selected for these red lines.
The inner edge of the border separated from the outer edge of the 'background' box by 0 points (`\BorderPadding 0`) and that pale (`\Alpha 0.1`)  blue (`\x0000ff`) box extends 4pt  (`BoxPadding 4`) out from the image.

With negative `\BorderPadding` values, and high `\BoxPadding` it is possible to position the border inside the box, and even leave sufficient bottom padding for the background colour to  make space for the caption too.

### Caption controls
Borders are not the only thing that may be altered by an image category. The styling parameter `\SpaceBetween` allows control of the gap between the caption and the image. Negative values can move the catpion into the background box, border or even onto the image.

This makes it possible to apply a caption to a full-page map, for instance.

Font-related style options (fontname, size, bold, italic, etc) and also justification and margin settings also take effect, but this would normally be avoided for the sake of consistent appearance.

### Image Credit controls
The image category also applies to the credit box, allowing it to
be moved and coloured so that there is no clash with the border or background:

```
\Marker cat:ornborder|x-credit|fig
\Outline 1
\OutlineColour xffff00
\SpaceBeside 8
```

### Complex example
This example shows the transparency in the  classic 'Ghostscript tiger' image,
an inset caption and and  an ornamental (`Vectorian2`) frame set fully inside
the background box. 
![](imgs/tiger_border.png)
```
\Marker cat:ornborder|fig
\BorderStyle Vectorian2
\BorderLineWidth 0.5
\Border All
\BorderWidth 15
\BorderColour x007f00
\BorderFillColour xcfcf7f
\BgColour x7f7fc0
\BorderPadding -25
\BoxBPadding 44
\SpaceBetween -4.5
\Justification Right
\LeftMargin 1.1
\RightMargin 0.5
\FontScale 0.7
\Alpha 0.5

```

The piclist entry is:
```
TST 2.5 The Ghostscript tiger in a PDF file [Fcb]|pgpos="tr" src="tiger.pdf" ref="" size="col" scale="1" x-credit="Ghostscript" cat="ornborder"
```

## Figures in footnotes
In general, footnote processing is not compatible with figures. However, the following observations have been made:

 * A footnote with `pgpos="H"` (i.e. in-text) may occur in paragraphed and non-paragraphed notes.
 * A footnote with `pgpos="h"` can occur in non-paragraphed footnotes.

