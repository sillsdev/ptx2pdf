# PTX2PDF Macros FAQ

## Style Sheets

### How does the \Color entry work?

There are two ways to reference a color using the \Color marker:

- Prefix a 6 digit hex number with x as in x400000. The 6 digits are interpretted in pairs RRGGBB.
- An integer is interpretted as a 24 bit number with the upper 8 bits as B, then G, then R. This
  is opposite to the RGB most people are used to.

Thus `\Color x400000` is dark red, while the corresponding `\Color 4194304` is dark blue.

The ptx2pdf macros do not interpret the \ColorName at this time.

Color text may be turned off globally by setting `\ColorFontsfalse`.

### Why does TeX stop processing a .sty file half way through?

TeX will stop processing a stylesheet file if it finds an error in it. There are a number
of ways a seemingly correct .sty file may stop processing:

- TeX interprets markers case sensitively, unlike Paratext that does not. The casing
  of a marker must match that of how Paratext would output it.
- TeX may not know of a particular marker you add. It cannot ignore markers it
  does not know about.

To aid in debugging .sty file issues. If you insert `\tracing{s}` in your .tex file
before it processes a .sty file, you will see analysis tracing in the .log file
from which you may be able to work out where it went wrong.

### How can I set a \FontSize relative to the size of the text 

Use `\FontScale` instead of `\FontSize`  (if `\FontScale` is defined, 
then `\FontSize` will be quietly ignored, for character styles). 
The value may be a float, thus `\FontScale 0.8`, for example. 

The font size  is scaled as being a multiplier against the current font size of
the text the style is being processed.  

The following is an example of a smallcaps character style:

```
\Marker nd
\EndMarker nd*
\StyleType character
\FontScale 1
\SmallCaps
```

Notice that this should only be used in a custom stylesheet, because other tools
will not recognise it.

Although normally a font is only set up once once (the first time it's used)
fonts with ```\FontScale``` are a treated specially and scaling now works correctly.
Normally, ```\FontScale 1``` is most useful for nested styles, i.e  ```\+nd```.

For **paragraph styles** `\FontScale` works a little differently. Rather than being relative to the 
previously active style, `\FontScale` multiplies the paragraph's `\FontSize` parameter or, if that is not 
defined the standard default of 12 x `\FontSizeUnit`.


### How do nesting styles work?
Consider this example:
```
\s The angel of \+nd Lord\+nd* speaks
```
The macros now support full cascading character styling. For the most part, this is straightforward.
The value is set from the paragraph or note base and then is potentially reset by any active character
styles above that.

In the case of fontsize, things are little more complex:
- `\fontscale` takes precedence over `\fontsize`. Thus if a style specifies a fontscale, that is
  used in preference to a character style below it (nearer to the base) setting a `\fontsize`.
- Specifying a fontsize will set the fontsize, unless that fontsize is the same as the fontsize
  specified for `\p`, in which case it is treated as `\fontscale 1`.

### I'm altering `\LineSpacingFactor` but it's not having any effect.
\LineSpacingFactor only gets used in the following circumstance:
- For the main text, no \baseline has been set.
- For any paragraph style, no \BaseLine (or \LineSpace) has been set in the style sheet.
- The paragraph style has been used before. Once a paragraph style (or font) has been used,
it will not be recalculated.


### I shrunk my verse numbers and now they're just floating in the middle of the line
In your configuration .tex file, you need to adjust this number.
``` 
\SuperscriptRaise{0.85ex} % note that this is in terms of the scaled-down superscript font size
```

### What Style properties are there?

This is a list of the various style properties and some notes on how they are used.
Only those markers that do something and are not simply ignored, by the ptx macros are listed.
Notice that markers are case dependent.

 Marker       | Description
------------- | -----------
\\Color       | decimal B * 65536 + G * 256 + R, or xRRGGBB hex digits
\\Endmarker   | ignored
\\TextType    | "title", "section" or "other" paragraph grouping
\\TextProperties | "nonpublishable" blocks text output
\\FontName    | font name to pass to font specification
\\FontSize    | actual font size is \\FontSize * \\FontSizeUnit
\\FontScale   | Scaled font size relative to the current font (e.g. \p)
\\FirstLineIndent | First line indent * \\IndentUnit
\\LeftMargin  | Left margin * \\IndentUnit
\\RightMargin | Right margin * \\IndentUnit
\\Italic      | blank enables, "-" disables
\\Bold        | blank enables, "-" disables
\\Superscript | blank enables, "-" disables
\\Regular     | Disables italic, bold, superscript
\\SpaceBefore | Space before paragraph * \\VerticalSpaceFactor * \\LineSpacingFactor * \\FontSizeUnit
\\SpaceAfter  | Space after paragraph * \\VerticalSpaceFactor * \\LineSpacingFactor * \\FontSizeUnit
\\Justification | "center", "left", "right" anything else is fully justified
\\CallerStyle | marker to style the body text caller
\\CallerRaise | dimension to raise the body text caller
\\NoteCallerStyle | marker to style the in note caller
\\NoteCallerRaise | dimension to raise the in note caller
\\NoteBlendInto   | name of note type marker to merge these notes into that class
\\SmallCap    | blank enables, "-" disables. Only works with fonts with a +smcp feature
\\LineSpacing | also BaseLine. Dimension of line spacing, can include glue. *Units are required*
\\StyleType   | "paragraph", "character", "note"

These styles are used by other programs but have no action in the macros:

 Marker         | Description
 -------------- | -----------
 \\Name         | UI name of the marker
 \\Description  | Descriptive text of the marker
 \\OccursUnder  | List of markers, this marker may nest under
 \\Rank         |
 \\Underline    | We don't do underlining. It's not pretty
 \\NotRepeatable |
 \\ColorName    | Color names are not supported. Use \\Color instead

### How do Tables of Contents work?

XeTeX produces a .toc file that contains one row per entry marked by a \\tr. Each
non empty \\toc entry in a file is output with the first marked with \\tc1 and the
second with \\tc2 and so on. The file entry on a line is a \\tcr marker followed by
the current column number and then the page number. For example

```
\tr \tc1 First Book of Samuel\tc2 1 Samuel\tcr3 137
\tr \tc1 2 Samuel\tcr2 179
```

Notice how 2SA had an empty \\toc1 entry. This will mess things up.

The ptx macros have special handling for `\\tr`, `\\tc`_x_ (`\\tc1`, `\\tc2`, etc.)
and `\\tcr`_x_. Similar handling
is done for `\\th`_x_ and `\\thr`_x_. The 'r' suffix says to right align by default rather
than left align. A table starts with a `\\tr` and ends with the next start of paragraph or
end of file. The number _x_ specifies the column number in the table and table columns
have their widths calculated automatically to fit the page. Each cell may be styled
according to its marker character style. The default font is specified in the \\tr style.


## Layout

### Why are there sometimes big gaps at the bottoms of pages?

The TeX macros work hard to balance columns in two column text. Sometimes it
is not possible to balance well. One option is to always balance however bad
the break is. But this would often end up with very short pages. A fallback
has been added that allows columns to be unbalanced if the break would result in
a short page. This is felt preferable to give something reasonable in hard cases.
It is still possible to get a short page if one has poorly located pictures.

The rest of this answer considers how to improve page breaks to ensure that columns
stay balanced.

TeX breaks pages based on some notion of how bad a page break is. This in turn
is based on how full the page is. The ptx macros further work to ensure that
columns balance by shortening the page until they do. Therefore, when TeX would
up with a relatively short page, it is the best page break it can come up with
based on the knowledge it has, which is pretty limited and the constraints it is under.

There are various controls a typesetter can use to adjust a page break.

- Adjust the amount of stretch in interword spaces. This gives TeX much more scope
  for changing the size of paragraphs, which feeds into the next control.
- Use the .adj file to increase or sometimes decrease a paragraph by a line. Notice
  that you can ask for a line increase or decrease, but that doesn't mean that
  TeX will give it to you. It will if it can, but not if the resulting paragraph
  is so ugly that TeX can't stand it!
- Move pictures around using a piclist file.

In terms of analysing why TeX broke a page where it did, there are various things
to think about:

1.  Footnotes and figures are anchored to the line in which they occur, so moving
    such a line across a page boundary moves the other stuff with it.
2.  TeX is a good Christian, it will avoid creating widows or orphans, so if you have
    3 lines left of a paragraph on a next page, you can’t pull 2 back across.
3.  Headings also take the first two lines of the following paragraph with them,
    for reason 2.
4.  For every line you take from column 2 to column 1, TeX needs to pull *exactly*
    2 lines from the next page, in such a way that it doesn't leave a single orphan
    line on that page.

It is strongly advince to only start addressing page breaking once everything else
about a layout is exactly as wanted in terms of headers and footers, point size
and spacing, styles, pictures, etc. Otherwise if you change anything after that,
you will almost inevitable have to go through and refix page breaks later.


### What limitations are there on the use of piclist files?

Piclist files allow an external file to associate pictures with verse references
in a file. Each entry is of the form: _bk_ _C.V_ _figure info_. There are some
limitations on a piclist file:

- References must be in order. A subsequent line in the piclist file is only
  read after the previous line is matched against the current reference being  processed as text.
- There can only be one line for any given reference (except diglots, which can match on left and right). Having two means the   second is not matched, the file gets out of sync and all subsequent lines  are not read.

In addition, TeX has a limitation that you cannot have more than one picture
in the same position on the page, anchored to the same line in the text,
whether or not they come from a piclist or inline \\fig. Thus
for a very short verse that may not span a line boundary, or if you have two
\\fig elements very close together in the text, one may be lost.

### Can I scale / rotate / crop / transform an image?
You may **scale** and **rotate** images. Cropping and other image transformations need to happen in an external  tool. This is from a piclist. ```\pic```  lines are somewhat similar
```
RUT 4.11 Boaz addresses the crowd|07.jpeg|span*0.6|t|Artist McArty| You are witnesses |Ruth 4:10|rotate 3|
```
This instructs XeTeX to put image 07.jpeg by Arist McArty (Boaz addresses the crowd) at the top of the page containing Ruth 4:11, and with the caption "(Ruth 4:10) You are witnesses". It goes on to say it should have a width of 0.6 of the span (the combined width of both columns, another measurement is `col`, the column width), and that it should be rotated three degrees anti-clockwise. 

**N.B.**  The size of the image is set before rotation. If you want an  image to fit the page width after rotation 90degrees, and before rotation the image is  twice as high as it is wide, then you will need to give its width as ```span*2.0```

There is no mechanism to rotate the caption.

### How do I change the font / fontsize for a caption?
Captions are set using the style defined for ```\Marker fig```. Edit the style in the stylesheet.

### How do I change the font / fontsize for the reference part of the caption, including the brackets?
You probably can't, sorry. The brackets are put around as part of the XeTeX code, without any font-changing code. Instead, leave the reference parameter empty and see below.


### How do I change the font / fontsize for part of the text of a caption?
This is tricky. The normal font-selecting code cannot work.  The solution comes in two varieties:
- Direct font specification. In the ```.tex``` file, put a TeX font definition, like:
```
\font\mySmallCap="Gentium Plus:smcp" at 10.3pt
```
and in caption in the piclist (it will probably only  work there), put something like: ```The {\mySmallCap Lord} spoke to Abraham.```

- Using an already-used font:
Fonts are remembered as you go along, but the naming scheme keeps on changing as the developers add more capability. The font name might be as simple as ```font<s2>``` (font for paragraph style s2) or it might be ```font<ndL-12.0>``` (font used for the divine name on the left side of a diglot, when the font was previously 12.0 ```\FontSizeUnit```s). You cannot just specify such complex names, you need to wrap them up in ```\csname ...  \endcsname```.  ```The {\csname font<ndL-12.0>\endcsname Lord} spoke to Abraham.```

To find out the names that fonts are saved as, put \tracing{F} into your .tex file and read the logfile, looking for lines like:


### // doesn't work in my caption. How do I make the line break in the right place?
This probably only works in a piclist. If the piclist line is:
```
RUT 4.2 Boaz talks to kinsman-redeemer|06.jpeg|span*0.8|t|Arty McArtful|O Boaz del duma \penalty -1000\ le răskumpărătoresa|Rut 4:1|rotated 0
```
Then ```\penalty -1000``` is telling XeTeX that after ```duma`` is a really amazingly good place
to break. The slash after the 1000 means it shouldn't eat the space that comes
next. If you put -2000 in there, you'll probably force a line break.


### Can I use a top-left or top-right image in a diglot?

Yes. It probably makes most sense to use **both**, for top images. Using the piclist you can even specify the same verse. Assign one ```tl```, the other ```tr```.  If you get a message about the tl being converted to t, you probably have \BodyColumns=1. Diglot doesn't currently care (eventually it may mean something else), at the moment you have two.
	

### Could pictures float onto pages other than their anchor?

It would be really hard for the ptx macros to work out when and how to float
pictures onto other pages. It is hard to know when to move a picture to another
page. When does it make the page better? How far should a picture float away 
from its anchor?

### How can I format the page number?

The page number is usually output as part of a header or footer. As such it can
be formatted using style markers. For example:

```
\def\RHoddright{\pgnum \pagenumber\pgnum*}
```
where \\pgnum is defined as a character style:
```
\Marker pgnum
\StyleType character
\FontSize 9
\Bold
```

By default elements in the heading row are styled according to the `\h` marker.

### How does \AboveNoteSpace work?

This value is used to ensure space above the footnotes area. The footnote rule
is inserted halfway up that space.

### My tables look terrible.

The table support in the macros is not great, but it can do a reasonable job.
The important marker to consider is the styling of the `\tr` marker, which drives
much of the column spacing. Each cell is given `\LeftMargin` and `\RightMargin`
from the `\tr` marker and these values are multiplied by the `\IndentUnit` which
defaults to 1in. This can result in really wide margins for a table. The `\FirstLineIndent`
is also used. It is advisable therefore to reduce the values found in USFM.sty. For
example:

```
\Marker tr
\LeftMargin 0.1
\RightMargin 0.1
\FirstLineIndent 0
```

Table column widths are calculated by measuring the widest cell in each column, including
the header and then trying to share out spare width and averaging the resulting lack over
all the columns. The results are OK but could be better.
