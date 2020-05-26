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
then `\FontSize` will be quietly ignored). 
The value may be a float, thus `\FontScale 0.8`, for example. 

With `\riskyscalefontfalse` ptx2pdf macros will interpret a \FontScale 
relative to the size of the \p font. This should be boring and always work.
If `\riskyscalefontrue`, the font size it is scaled 
as being a multiplier against the current font size of the text the style is
being processed. 

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

Unfortunately, a font is only set up once once, the first time it's used, so the
above won't to have `\nd` scale in all circumstances. The first time it is used will 
define the font size all future occasions.  **However, all is not lost!** 
if hooks are automaticly  replacing `\nd` with `\s1nd`, `\s2nd` `\fnd`, etc (or
some other scheme), and these are all copies of the above (perhaps with a
`\Bold`) then `\riskyscalefonttrue` should work exactly as desired. Until it's
used in an context that didn't have the hooks set up.

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
\\SmallCap    | blank enables, "-" disables. Only works with fonts with a +smcp feature
\\LineSpacing | also BaseLine. Dimension of line spacing, can include glue
\\StyleType   | "paragraph", "character", "note"

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

TeX breaks pages based on some notion of how bad a page break is. This in turn
is based on how full the page is. The ptx macros further work to ensure that
columns balance by shortening the page until they do. Therefore, when TeX comes
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
  read after the previous line is matched against the current reference being
  processed as text.
- There can only be one line for any given reference. Having two means the
  second is not matched, the file gets out of sync and all subsequent lines
  are not read.

In addition, TeX has a limitation that you cannot have more than one picture
in the same position on the page, anchored to the same line in the text,
whether or not they come from a piclist or inline \\fig. Thus
for a very short verse that may not span a line boundary, or if you have two
\\fig elements very close together in the text, one may be lost.

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
