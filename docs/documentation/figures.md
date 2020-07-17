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
a later discusion also).

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

In the above pic-list line, (for the *right* column of a diglot, hence the `R`
after the `HEB`), the picture will be set in a cut-out on the right side of the
column, two lines below the beginning of the paragraph starting at 3:9, with the
picture half a column wide and the text a little distance away.  This may
*force* a paragraph at this point.

In the table below, 'left-aligned' means that the left hand edge of the image is
lined up with the left-hand image of (unindented) paragraph text.

The following page positions are now available:

Code | Mnemnonic              | Position                                                      | Caption position / width 
---- | -----------------------|-----------------------------------------------------------|-----------------------------------------------
t    | 'Top'                  | Above everything except the header line.                        | Centred across both columns 
b    | 'Bottom'               | Below all verse text and footnotes.                             | Centred across both columns 
tl   | 'Top-Left' [1]         | At the top of the left-hand [2] column                          | Centred within column 
tr   | 'Top-Right' [1]        | At the top of the right-hand [2] column                         | Centred within column 
bl   | 'Bottom-Left' [1]      | At the bottom of the left-hand [2] column                       | Centred within column 
br   | 'Bottom-Right' [1]     | At the bottom of the right-hand [2] column                      | Centred within column 
-----|------------------------|       ***Experimental Additions***                              |----------------------------
h    | 'Here'                 | Where defined / before the verse in piclist[3,4], centred       | Centred within column
hc   | 'Here',centred         | Where defined / before the verse in piclist[3,4], centred       | Centred within column
hl   | 'Here',Left            | Where defined / before the verse in piclist[3,4], left-aligned  | Centred below image, and the same width
hr   | 'Here',Right           | Where defined / before the verse in piclist[3,4], right-aligned | Centred below image, and the same width
p    | 'Post-paragraph'       | After this paragraph[4,7], centred                              | Centred within column
pc   | 'Post-paragraph', centred  | After this paragraph[4], centred                            | Centred within column
pr   | 'Post-paragraph, Right'| After this paragraph[4], right-aligned                          | Centred below image, and the same width
pl   | 'Post-paragraph, Left' | After this paragraph[4], left-aligned                           | Centred below image, and the same width
pc#  | 'Post-paragraph'       | After # paragraphs[4,5], centred                                | Centred within column
pr#  | 'Post-paragraph, Right'| After # paragraphs[4,5], right-aligned                          | Centred below image, and the same width
pl#  | 'Post-paragraph, Left' | After # paragraphs[4,5], left-aligned                           | Centred below image, and the same width
cl   | 'Cutout Left'          | In the top-left corner of this paragraph [3]                    | Centred below image, and the same width
cr   | 'Cutout Right'         | In the top-right corner of this paragraph [3]                   | Centred below image, and the same width
cl#  | 'Cutout Left'          | In a notch # lines[6] below the top of this paragraph [3]       | Centred below image, and the same width
cr#  | 'Cutout Right'         | In a notch # lines[6] below the top of this paragraph [3]       | Centred below image, and the same width

Notes:
[1] If two columns are in use.
[2] If a diglot is being set inner-outer rather than left/right, then the 'left' column is the inner column. 
[3] *Here*  and *cutout* images need to start at a new paragraph. If the
    specified location is not a paragraph boundary, a new paragraph will be forced.
[4] The 'insert image here' code will be activated at the end of the paragraph.
    Counting starts at the paragraph containing the verse number or the \fig
    definition.
[5] pc1 'after one paragraph' is interpreted as meaning the same as p or pc (the
    c is assumed if no number is specified, but required if supplying a number), pc2
    means after the next paragraph. This is useful if the verse contains poetry.
[6] Multi-digit numbers may be specified, but little sanity checking is done.
    The image will be on the same page as the calling verse (or off the page's
    bottom), even if the notch is partly or fully on the next. A negative number
    (e.g. cr-1) will raise the image and shorten the cut-out, but will not make
    space above.
[7] Since `p` is also interprettable as a media target, `pc` should always be
    used in SFM2 instead.


At the time of writing (15 Jul 2020), there are some very recently-fixed bugs.
Assuming your copy is more recent than this, please report any recurrance.
- p  : The post-paragraph code seems to function well as long as the paragraph
  does not cross a page boundary. If it did in diglot, then the picture was
  always set at the top of the left-hand text of the follow-on page.  Hopefully
  this has now been solved.
- h and p :  Following text may have problems with grid alignment, but this is hopefully solved.

#### Do the new picture positions conform to examples in the USFM specification?
In some ways, they conform better than the previously available options. USFM
specification indicates that a picture can occur immediately after text, ending
the previous paragraph. This works with *here* and *cutout* picture locations,
(the 'automatic' paragraph style for text surrounding the cutout is intended to
be the same as the previous paragraph style, but until further testing reveals
this to be 100% reliable, sensible users will supply their own style marker).
USFM makes no reference to left or right alignment, nor scaling images, nor
images in cutouts.
 
#### Why might I use unusual positions?
- cl / cr  Small images, perhaps glossary items?
- p  A picture to be set after the final verse of a book, otherwise impossible
  from a piclist. Possibly also for some kind of decorative 'end of section'
  mark.
- hl / hr Handy for a sponsor's or publisher's logo, perhaps?

### span Attribute

The `size` attribute has been extended to support scaling. Following the `col`
or `span` values, there may be an optional `*` followed by scale factor, with
1.0 being the unity scaling. For example in a piclist:

```
RUT 4.11 Boaz addresses the crowd|07.jpeg|span*0.6|t|Artist McArty| You are witnesses |Ruth 4:10|rotated 3|
```
The `span*0.6` says the figure should be scaled to span the page and then scaled
down to 60% of that size.

### x-xetex Attribute

To allow further transforming of images when inserting into the publication,
ptxprint and the ptx macros support an optional extra column in a USFM2 `\fig`
element, which corresponds to the `x-xetex` USFM3 attribute. It consists of a
space separated list of image specifications:

- rotated _degrees_ Rotates the image anticlockwise the given number of degrees.

For example, in the piclist entry from the previous section, the image is
rotated anticlockwise by 3 degrees.

There is no mechanism to rotate the caption with the picture.

### media Attribute

The media attribute consists of a string of single letter media types for which
this figure is intended. It is currently ignored in the ptx macros and all
images are included.

- a Include in scripture applications, like Scripture App Builder.
- p Include in print publications.
- w Include in web page presentations of the text.

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

A piclist file has a strict format:

- Each entry is on a single line.
- Any characters after a % character are ignored
- Blank lines consisting only of whitespace (after % comment removal) are
  ignored.
- A piclist entry consists of an anchor reference followed by the contents of a
  `\fig` element (without the `\fig` markers) USFM2 or USFM3 format may be used.
- Piclist entries must be in reference order. The ptx macros will read the next
  entry and if the anchor reference entry is before or equal to the anchor reference entry
  of the previous entry, it and all future piclist entries will be ignored.
- The anchor reference is of the form _bk_ _C_._V_, where _bk_ is the 3 letter
  (all-caps) book identifier. The _C_ and _V_ are chapter and verse references.
  The _bk_ may also have a 4th letter of `R` or `L` to indicate which side in a
  diglot is being referenced. Lack of a 4th letter implies it may be matched
  while processing either column, and the user has no preference about
  which font, etc. are used (normally `L` will match it first, but this is not guaranteed).


