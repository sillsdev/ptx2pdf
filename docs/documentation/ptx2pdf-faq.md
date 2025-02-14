# PTX2PDF Macros FAQ

## Style Sheets

### How does the \Color entry work?

There are two ways to reference a color using the \Color marker:

- Prefix a 6 digit hex number with x as in x400000. The 6 digits are interpreted in pairs RRGGBB.
- An integer is interpreted as a 24 bit number with the upper 8 bits as B, then G, then R. This
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
- For the main text, no `\BaseLine` has been set.
- For any paragraph style, no `\BaseLine` (or `\LineSpace`) has been set in the style sheet.
- The paragraph style has been used before. Once a paragraph style (or font) has been used,
it will not be recalculated.


### I shrunk my verse numbers and now they're just floating in the middle of the line
In your configuration .tex file, you need to adjust this measurement.
``` 
\def\SuperscriptRaise{0.85ex}% default 0.85ex, measured in terms of the scaled down font. (an x is 1ex high)
```
For the change to be effective, it must occur before any stylesheet is read.
There is also individual control within the stylesheet over the amount raised.
E.g. the stylesheet could contain:
```
\Raise  1ex
``` 
Note that for ```\Raise``` to be effective, the
```\Superscript``` needs to come before ```\Raise```, otherwise its value will
be overwritten by the value of ```\SuperscriptRaise```

### What Style properties are there?

This is a list of the various style properties and some notes on how they are used.
Only those markers that do something and are not simply ignored by the ptx macros are listed.
Notice that markers are case dependent.

 Marker       | Description
------------- | -----------
\\BaseLine    | (see also LineSpacing.) Dimension of line spacing. An absolute measure that can include glue. (e.g. `12pt plus 1pt minus 1pt`). *Units are required*
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
\\Superscript | blank enables, "-" disables. Equivalent to \FontExpand \SuperscriptFactor, \Raise \SuperscriptRaise.
\\Raise       | specifies a dimension to raise the text by. Be careful, this can't handle whole paragraphs and will not allow line breaking within the text so marked.
\\Regular     | Disables italic, bold, superscript
\\SpaceBefore | Space before paragraph ( actual value is this * \\VerticalSpaceFactor * \\LineSpacingFactor * \\FontSizeUnit)
\\SpaceAfter  | Space after paragraph (actual value is this * \\VerticalSpaceFactor * \\LineSpacingFactor * \\FontSizeUnit)
\\Justification | "center", "left", "right" anything else is fully justified
\\CallerStyle | marker to style the body text caller
\\CallerRaise | dimension to raise the body text caller
\\NoteCallerStyle | marker to style the in note caller
\\NoteCallerRaise | dimension to raise the in note caller
\\NoteBlendInto   | name of note type marker to merge these notes into that class
\\SmallCap    | blank enables, "-" disables. Only works with fonts with a +smcp feature
\\LineSpacing | (see also BaseLine.) Dimension of line spacing, as a proportion of the default line spacing. I.e. actual measurement is \\LineSpacing * \\LineSpaceBase * \\LineSpacingFactor * \\FontSizeUnit<sup id="a1">[1](#f1)</sup>
\\StyleType   | "paragraph", "character", "note"
\\ztexFontFeatures | TeX style font feature settings to append to the font name specification when a font is instantiated
\\ztexFontGrSpace | the \XeTeXinterwordspaceshaping value to use when this marker is active.
\\Underline    | We don't recommend underlining, it's not pretty. If set to 2, then double underlining is applied. <sup id="a2">[2](#f2)</sup> 
\\Background   | Apply a background colour 'highlight'. <sup>[2](#f2)</sup> 
\\Outline      | Draw the outline of letters. A line of (this * \\FontSizeUnit) is drawn on all stroke-lines in the font, and then the normal 'fill' is then reapplied, as some fonts have strokes that cross fills. Final outline thickness will thus be half the given thickness.p<sup>[2](#f2)</sup> 
\\OutlineColour| Colour for the outlining. As \\Colour<sup>[2](#f2)</sup> 
\\Shadow       | x-shift y-shift, offset of 'shadow', as a ration to the font size. (E.g. \\Shadow 0.05 -0.05)<sup>[2](#f2)</sup> 
\\ShadowColour | Colour for the shadow. As \\Colour<sup>[2](#f2)</sup> 


<b id="f1">[1]</b>: Because the default mapping of fontsize to linespacing is hardwired to \\LineSpaceBase /12, a full line is \\LineSpaceBase * fontsize units (* \\LineSpacingFactor).
This is all calculated internally to the macros. LineSpacing of 1.0 is the same as the default linespacing. [↩](#a1)
<b id="f2">[2]</b>: The Underline, Background, Outline and Shadow effects are *not* for general use. They prevent any hyphenation and are *best* applied to character styles rather than paragraph styles. Also, they interact very badly with verse numbers, footnotes, any special spacing, or other formatting.
 They **may** be applied to paragraph styles, but it should be understood that at present when applied at a paragraph level, the effects are applied to each word after it has been typeset and colour has been applied. Expect unintuitive results, e.g. if the character settings specify a colour, then there is no way for paragraph-level settings to override that, and the colour will apply to both outline and shadow. 
If the outline and shadow are instead set as part of the character style, then the code can make appropriate adjustments.


These styles are used by other programs but have no action in the macros:

 Marker         | Description
 -------------- | -----------
 \\Name         | UI name of the marker
 \\Description  | Descriptive text of the marker
 \\OccursUnder  | List of markers, this marker may nest under
 \\Rank         |
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

## Figures

For information on using the `\fig` element in USFM and the layout controls, see [figures.md]. The questions here are specific to formatting issues associated with figures.

### How do I change the font / fontsize for a caption?
Captions are set using the style defined for `\Marker fig`. Edit the style in the stylesheet.

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

### Can I put a picture in a footnote?
No.

### // doesn't work in my caption. How do I make the line break in the right place?
This probably only works in a piclist. If the piclist line is:
```
RUT 4.2 Boaz talks to kinsman-redeemer|06.jpeg|span*0.8|t|Arty McArtful|O Boaz del duma \penalty -1000\ le raskumparatoresa|Rut 4:1|rotated 0
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

In some error situations, the picture will not be on the same page as the anchor in a diglot. This is normally because trying to do that would have made the page too big. It is usually accompanied with other errors and possibly the page overflowing.


## Headers and footers

###Can I have Roman numerals for preface material and normal (arabic) numerals for the scripture text?
Certainly!
In the .tex file, before you include any front-matter, include:
```
\pageno=-1
```
And before you start with the scripture text, include:
```
\pageno=1
```

###What controls are there (from TeX) over the header and footer? 

There are a series of definable macros that the TeX macros pick from to build the header and footer. These have 
the form ```\def\RHoddcenter{value}```,  *value* may contain either text, other macros (normally the header/footer macros such as ```\date``` or ```\pagenumber```), or a combination of both.

The name describes the vertical position, the page-type and the position.  The two vertical positions on the page are: RH (running header) and RF (running footer).
The types of pages are: 
- title - A page containing the title of a book
- odd, even - a page containing normal biblical text (critically, numbered verses), with odd and even page numbers respectively.
- noVodd, noVeven - a page that is neither a title page nor a page with numbered verses, e.g. introductions and glossary pages.

The  three horizontal positions are (left, center, right).

Thus there are *thirty* possible locations that may be defined.

### What are the most common header and footer macros?

You probably need to use at least two of these:
 - ```\pagenumber``` Page number (in standard -arabic- numerals if ```\pageno``` is positive, in lower-case roman numerals if negative).
 - ```\pagenumberL``` Page number (in standard -arabic- numerals if ```\pageno``` is positive, in lower-case roman numerals if negative), using font from left diglot column.
 - ```\pagenumberR``` Page number (in standard -arabic- numerals if ```\pageno``` is positive, in lower-case roman numerals if negative), using font from right diglot column.

 - ```\firstref``` first verse on the page (e.g. Genesis 1:1)
 - ```\firstrefL``` first verse on the page from the left column of a diglot (e.g. Genesis 1:1)
 - ```\firstrefR``` first verse on the page from the right column of a diglot (e.g. Genesis 1:1)

 - ```\lastref``` last verse on the page (e.g. John 3:17)
 - ```\lastrefL``` last verse on the page from the left column of a diglot (e.g. John 3:17)
 - ```\lastrefR``` last verse on the page from the right column of a diglot (e.g. John 3:17)

 - ```\rangeref``` The range of verses on the page (E.g. Genesis 1:1 - 2:2)
 - ```\rangerefL``` The range of verses on the page from the left column of a diglot (E.g. Genesis 1:1 - 2:2)
 - ```\rangerefR``` The range of verses on the page from the right column of a diglot (E.g. Genesis 1:1 - 2:2)

Note that the diglot versions above include side-specific font-switching code appropriate for the data they are presenting.
The not-diglot ```\firstref```,```\rangeref``` and  ```\lastref```  may include
references from either side (or both for ```\rangeref```) and should not be
used in a diglot publication if the two sides use different fonts.
 
### I need to put a date / timestamp in the header / footer
 - ```\hrsmins``` Time that the XeTeX run started (e.g. 17:35)
 - ```\usdate``` Ambiguous U.S.-style date (month/day/year)  e.g. "12/24/2020"
 - ```\ukdate```  Ambiguous U.K.-style date (day/month/year) e.g. "24/12/2020"
 - ```\isodate``` Unambiguous ISO-style date (year-month-day) e.g. "2020-04-01"
 - ```\timestamp``` Time code as displayed when  cropmarks are in use. e.g. "2020.12.24 :: 17:37"
 - ```\number\year.\ROMANnumeral\month.\number\day ``` (Hungarian-style date, upper case roman numerals for month, e.g. 2020.XII.24)
 - ```Draft: \number\day/\romannumeral\month/\number\year. ``` (Another unusual date format, with prefix "Draft: 24/xii/2020")


### I'm setting a diglot and the fonts switch around 
To ensure a particular font, use the ```\headfootL{}``` and ```\headfootR{}``` macros, putting the text inside the curly-brackets. e.g.: ```\headfootL{Draft: \isodate}```. Similarly to the verse reference macros above, ```\hrsmins```, ```\timestamp```  and the date macros now have ....L and ...R variants as a convenience. 

## Marginal Verses

It is possible to have verse numbers printed in a left of text margin.

Sometimes, where there is a short verse, two verse numbers appear in the same
line. This causes a crash between the two marginal verse numbers. One way around
this is to tell the ptx macros to bridge two verses. This can be done using, for
example:

```
\bridgeVerses ROM3.17-18.
```
The structure of this command is very precise. The book must be the 3 letter
book id. The chapter must be included even for single chapter books. The
separator between the chapter and verse must be a period. The number after the
hyphen must be the next verse after the first verse and there must be a final
period to complete the specification. Apart from all that, this is a very
convenient way to bridge verses without having to edit the source text. It may
also be used not in a marginal verses context.


### My scripture text includes `//` but it is being ignored.
The USFM `//` 'option line break' can be used in poetry or headings to indicate
a good place to break a line.  In the understanding of ptx2pdf this has a very specific 
meaning:
* It is *optional*, it  does *not* force a line break. 
* It *only* breaks a line, and in a justified paragraph, it does not do anything to 
insert extra space at the end of the line. Using it in a justified paragraph is
probably a mistake.
* It dissuades TeX from using any other break-point.
* It does not allow a break that is not permitted by other settings.

This last one may be quite significant. At the time of writing, the distance 
between the un-justified edge of a half-justified (ragged-right or ragged left)  
paragraph and the column edge is allowed to be between 0 and 0.25 of the column 
width (plus any fixed margin), this gap is called the right fill or right-skip 
(or left-skip) (Technically, in TeX, the right-skip is both the fixed 
right-hand margin plus the variable 'fill').  If the user-supplied `//` 
suggests a break that half way across the page, then as that is suggesting a 
line-break that would need the the right-skip to stretch to half the column 
width. As that is  outside the permitted range for the right-skip, the 
user-supplied break will be ignored.

In this example the lines all USFM lines contain a `//` after 'q':
[Visual demonstration](NonJustifiedFill.png)

In the first section ('verses' 16 and 17) the default limit of 0.25 is used 
(note that this default is adjused for `\q`, `\q1`, `\q2` and `\q3` in `ptx2pdf.sty`).
Even though there is a suggested break after q, the code chooses a break after 
'can' if the line does not fit on the page.

In the second section, the stylesheet option has been given the line:
```tex
\NonJustifiedFill 0.5
```
The normal width of the text  puts the q past the mid-point of the line,
(or can expand to do so), and thus the break is permissible.  If the line needs 
to break then this will be a (very) highly favoured break-point, though of 
course others are also possible. If the line does not need to break then it 
will not.  Choosing a longer distance (e.g 0.75 or higher), will significantly  
reduce the 'loosness' of the line (amount of stretch applied to the spaces), 
visible in in the example with the 'q' moved almost its whole width, but will 
favour unfilled lines in the text.

TeX's line breaking algorithm resists finding breaks where there are large 
amounts of 'stretch'. The global definition `\def\OptionalBreakPenalty{150}` 
provides a tuning parameter for the line-breaking algorithm on paragraphs with 
optional breaks.  Increasing the number makes the breaks more likely to occur 
at only the specified point; reducing it means it is more possible that TeX 
will choose an alternative one, and allow other considerations (like avoiding 
hyphenation if possible) to play their normal role.

