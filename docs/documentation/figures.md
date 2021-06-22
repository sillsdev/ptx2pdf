# Figures

Figures overlap the boundary between content and publication information. A
figure is often publication specific. For example, one might expect different
figures in different kinds of publications. There may well be more figures in a
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

Paratext's export to print-draft removes picture formatting information before
it gets to XeTeX. PTXprint leaves the formatting intact, and assumes you've got
it (mostly) right.  The USFM standard is not very useful here; for example, for
the `loc` attribute it says "a list of verses where it might be inserted", and
for size it offers only 'span' and 'col'. The ptx2pdf XeTeX macros give better
control on both of these, offering multiple positioning options and if you want
a smaller image than full-page or column-width you can say, e.g. `span*0.6` (see
a later discusion also). They also add the extra sizes 'page' and 'full'. 
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

Within the ptx macros, the `LOC` column is always interpretted as a `pgpos`
attribute. In addition, for USFM3, if there is only a `loc` attribute, it is
treated as a `pgpos` attribute for backward compatibility.

### pgpos Attribute

The `pgpos` attribute gives a suggestion as to where on the page a figure should
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

In the table below, 'left-aligned' means that the left hand edge of the image is
lined up with the left-hand image of (unindented) paragraph text.

The page positions listed below are now available. For each **position code** given
with `l` (Left), **you may also specify**: `r` (Right), `i` (Inner) and `o` (Outer).
`i` is replaced with `l` on odd-numbered pages, and `r` on even numbered pages. In a 
diglot when the `mirrored` columns are in use ('left' text is always inner, the
'right' text outer), you probably don't want to use `ti` or `to` for picture placement.


Code | Mnemnonic              | Position                                                      | Max. caption width 
---- | -----------------------|-----------------------------------------------------------|-----------------------------------------------
t    | 'Top'                  | Above everything except the header line.                        | across both columns 
b    | 'Bottom'               | Below all verse text (and footnotes in diglot).                 | across both columns 
tl   | 'Top-Left'    [1]      | At the top of the left-hand [2] column                          | width of column 
bl   | 'Bottoom-Left'    [1]  | At the bottom of the left-hand [2] column                          | width of column 
-----|------------------------|       ***Experimental Additions***                              |----------------------------
h    | 'Here'                 | Where defined / before the verse in piclist[3], centred       | width of column
hc   | 'Here',centred         | Where defined / before the verse in piclist[3], centred       | width of column
hl   | 'Here',Left            | Where defined / before the verse in piclist[3], left-aligned  | same width as image
p    | 'Post-paragraph'       | After this paragraph[4,7], centred                              | width of column
pc   | 'Post-paragraph', centred  | After this paragraph[4], centred                            | width of column
pl   | 'Post-paragraph, Left' | After this paragraph[4], left-aligned                           | same width as image
pc#  | 'Post-paragraph'       | After # paragraphs[4,5], centred                                | width of column
pl#  | 'Post-paragraph, Left' | After # paragraphs[4,5], left-aligned                           | width of column
cl   | 'Cutout Left'          | A notch/corner cut out of the text, starting at current line    | same width as image
cl#  | 'Cutout Left'          | A notch starting # lines[6] below the current line              | same width as image
P    | 'Page'                 | An image that replaces the normal text on the page              | width of page
Pc   | 'Page', centred        | An image that replaces the normal text on the page              | width of page
Pct  | 'Page', centred, top[8] | An image that replaces the normal text on the page              | width of page
Pl   | 'Page', left           | An image that replaces the normal text on the page, left-aligned | width of page
Plt  | 'Page', left, top[8]   | An image that replaces the normal text on the page, left-aligned | width of page
F    | 'Full page'            | The entirety of the paper [9]                                    | width of paper, may be off the page.
Flt | 'Full page', as above  | The entirety of the paper [9] pushed to whatever edge is indicated   | width of paper, may be off the page.
-----|------------------------|       ***Polyglot  Additions***                              |----------------------------
tL   | 'Top-of-L'	      | At the top of column L (substitute L for R, A, B...)		| width of column
bL   | 'Bottom-of-L'	      | At the top of column L						| width of column

Notes:
[1] Only if two columns are in use.
[2] If a diglot is being set inner-outer rather than left/right, then the 'left' column is the inner column. 
[3] *Here*  images need to start at a new paragraph. If the
    specified location is not a paragraph boundary, a new paragraph will be forced.
[4] The 'insert image here' code will be activated at the end of the paragraph.
    Counting starts at the paragraph containing the verse number or the \fig
    definition.
[5] pc1 'after one paragraph' is interpreted as meaning the same as p or pc (the
    c is assumed if no number is specified, but required if supplying a number), pc2
    means after the next paragraph. This is useful if the verse contains poetry.
[6] Multi-digit numbers may be specified, but little sanity checking is done.
    The image will *always* be on the same page/column as the anchor (normally 
    a verse);  It may occur off the page's bottom, even if the notch is partly
    or fully on the next. A negative number (e.g. cr-1) will raise the image and
    cut-out, but while this can raise the image into the preceeding paragraph, 
    it  cannot make the cutout begin earlier than the paragraph containing the anchor.
[7] Since `p` is also interpretable as a media target, `pc` should always be
    used in SFM2 instead.
[8] Use `b` for bottom alignment, or `c` for explicit central vertical alignment. 
[9] If the image is not the same aspect ratio as the page, or a scaling factor is used, 
    there may be some space. For this reason, the alignment options are available.
    Full page images have no header or footer, there is no attempt made to keep
    the caption on the page.  Alignment actively attempts to get the picture to the
    specified edge of the page. ```\FullPageFudgeFactor``` (normally defined to
    be -2pt) is available for tweaking if top alignment does not actually coincide 
    with the image. 

#### Restrictions  / notes on certain picture positions
- p : The delayed picture is saved until the end of the Nth paragraph in a
  certain 'box'. There is no code to have either an adjustable stack of boxes 
  or multiple images in the box. (But diglots have a second box for the
  right/outer text).  If an attempt is made to put a second picture into the
  box while it still contains the first, the first picture will be lost.
- F : 
  -  If a caption is used, this will normally be off the page. It may,
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
cutouts.  (1 line higher for chapter numbers, +/- 2 relative to 'perfect' for other cutouts).
This might mean, for instance, that if run 1 calculated that an
in-cutout image should ideally start at line 14 in a given paragraph, if on 
the next run  it finds the anchor-point has moved and the cutout should now be
on line 13 or 15 the code considers this acceptable.  Rather than adjusting the
shape of the paragraph again (which risks moving the anchor point again), an annotation 
is made to the `.parlocs` file that the image is to raised or lowered relative to the 
anchor point to fit into the cutout.
The following allows `droppic4` (image number 4, in a cutout analagous to
a drop-cap)  to accept being raised by 3 lines or lowered by two.

```
\setCutoutSlop{droppic4}{3}{2}
```

#### Do the new picture positions conform to examples in the USFM specification?
In some ways, they conform better than the previously available options. USFM
specification indicates that a picture can occur immediately after text, ending
the previous paragraph. This works with *here* picture locations,
(the 'automatic' paragraph style for text surrounding the image is intended to
be the same as the previous paragraph style, but until further testing reveals
this to be 100% reliable, sensible users will supply their own style marker).
USFM makes no reference to left or right alignment, nor scaling images, nor
images in cutouts.
 
#### Why might I use unusual positions?
- cl / cr  Small images, perhaps glossary items? Or in a single column printout.
- p  A picture to be set after the final verse of a book, otherwise impossible
  from a piclist. Possibly also for some kind of decorative 'end of section'
  mark.
- hl / hr Handy for a sponsor's or publisher's logo, perhaps?

### size Attribute

The `size` attribute has been extended to support scaling. Following the `col`
or `span` values, there may be an optional `*` followed by scale factor, with
1.0 being the unity scaling. For example in a piclist:

```
RUT 4.11 Boaz addresses the crowd|07.jpeg|span*0.6|t|Artist McArty| You are witnesses |Ruth 4:10|rotated 3|
```
The `span*0.6` says the figure should be scaled to span the page and then scaled
down to 60% of that size.

### scale Attribute

While in USFM2 the `size` attribute position has been extended to support a
scale factor via `*`. This is not ideal and in USFM3 it is better to separate
the scale factor into its own `scale` attribute. This value is a multipler that
scales an image after its size has been established via the `size` attribute. A
value of `1.0` implies no size change.

### x-xetex Attribute - Rotation control

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
Similarly to other attributes, the  displayed attribute `x-credit` of marker `\fig` can be styled in the following manner (by
the XeTeX code, don't expect this to work with Paratext or another program!):

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

\Marker x-credit:box=whitetext|fig
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

The third set demonstrates that there's no need to re-specify the default
parameters (defined by ```\Marker x-credit|fig```, and the special value of `-`
for the `\Background` parameter cancels the box for `creditbox="whitetext"` I.e. 
there will be no box for this item.


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

There are two methods to read a piclist, in 'slurp' mode (`\picslurptrue`, the
new default) where the entire file is read at once or the traditional mode
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
  the exact text (including punctuation) between `\k` and `\k*`, but excluding
  any spaces. (i.e.  in the above example it will be ```_bk_ This(Odd)Term```
- The anchor for a stand-alone milestones is the book and the ```id```
  attribute for that marker e.g. ```\zfiga |id="rabbit123\*``` will trigger piclist 
  entries starting ```_bk_ rabbit123```  If ```id``` is the default attribute
  (as it is for ```\zfiga```, the shorter form ```\zfiga|rabbit123``` may also be used 
  in the USFM. Note that at present only stand-alone milestones trigger figure 
  inclusion.
- A second or subsequent paragraph within a verse or keyterm entry may be referenced 
  by appending a separator (by default an equals sign) and a number. e.g. ```_bk_ 1.2=3``` will 
  trigger on the third paragraph within verse 2 of chapter 1. The following should be noted: 
  - There is only one paragraph counter which is reset at each change of
    trigger. Thus the above example *will not* trigger if there
    is no 3rd paragraph before the next verse number, nor will it trigger if some other
    potential marker occurs.  
  - As the first paragraph of the verse / key term is the one containing  that
    item, a suffix of ```=1``` is an invalid trigger point and will never match.
  - The code assumes that *any* occurance of the separator in the piclist reference 
    means that what follows is a paragraph number. Using some other separator is now 
    supported, with the restriction that (a) it sould not be expected to occur 
    in normal text of a type that might crop up in a key term. (b) it must not contain characters 
    with a special meaning within TeX (e.g. `#`, `$`, `%`, `{`, `}`). Multiple character separators 
    are permissible. The command  below (to be included in the `.tex` file before any piclists, etc. are loaded) sets the separator to be the sequence `=@=`, in case a simple = sign is used in the text of a keyword. Piclists would then need to specify paragraphs in form ```_bk_ 1.2=@=3```
```
\SetTriggerParagraphSeparator{=@=}
```


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
 By default the reference (if present) folows the catption and is in (rounded) brackets. The code for this is:
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
Captions are normally centred. If for some reason left-justified or right-justified captions are required, this can be controled 
in the normal manner in the style sheet, via the `fig` marker, even though officially the marker is officially a character style, not a paragraph style:

```
\Marker fig
\Justification left
\LeftMargin 0.125

```
The text will align to the standard page edge, unless the margins are modified
as above. There is no support for controlling indentation of the first line or
other paragraphing style elements.

### Caption font and size

As noted above, caption styling is controled via the `fig` marker in the stylesheet. Font-related styles can be selected in the normal manner.
For multi-line captions, the line spacing may be controlled by modification of `\LineSpacing` (in the same scaleable units as parameter `\FontSize`) or 
`\BaseLine` (units must be supplied).

### No Captions and references at all
```
\DoCaptionsfalse
```

