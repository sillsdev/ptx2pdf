#### Navigation

[Home](../home/README.md)  | [Installation](../installation/README.md) | [Quick Start](../quick-start/README.md) | Documentation | [Cookbook ](../cookbook/README.md)


# Documentation

A [PDF](../documentation/ptx2pdf-MacroSetupParameters.pdf?attredirects=0/index.html) version of this document is also available.

## Contents

-  [**1** Paratext Stylesheet](#TOC-Paratext-Stylesheet)
-  [**2** Page Setup](#TOC-Page-Setup)
    -  [**2.1** Dimensions](#ptx2pdf-MacroSetupParameters-Dimensions)
    -  [**2.2** Crop Marks](#ptx2pdf-MacroSetupParameters-CropMarks)
    -  [**2.3** Margins](#ptx2pdf-MacroSetupParameters-Margins)
    -  [**2.4** Columns](#ptx2pdf-MacroSetupParameters-Columns)
-  [**3** Fonts](#ptx2pdf-MacroSetupParameters-Fonts)
    -  [**3.1** Faces](#ptx2pdf-MacroSetupParameters-Faces)
-  [**4** Text Spacing](#ptx2pdf-MacroSetupParameters-TextSpacing)
-  [**5** Chapters & Verses](#ptx2pdf-MacroSetupParameters-Chapters&Verses)
-  [**6** Running Header/Footer](#ptx2pdf-MacroSetupParameters-RunningHeader/Footer)
    -  [**6.1** Header/Footer Position](#ptx2pdf-MacroSetupParameters-Header/FooterPosition)
    -  [**6.2** Odd Header](#ptx2pdf-MacroSetupParameters-OddHeader)
    -  [**6.3** Even Header](#ptx2pdf-MacroSetupParameters-EvenHeader)
    -  [**6.4** Title-page Header](#ptx2pdf-MacroSetupParameters-TitlepageHeader)
    -  [**6.5** Front-/Back-matter Header](#ptx2pdf-MacroSetupParameters-NoVpage)
    -  [**6.6** Odd, Even, and Title-page Footer](#ptx2pdf-MacroSetupParameters-Odd,Even,andTitlepageFooter)
    -  [**6.8** Header Contents](#ptx2pdf-MacroSetupParameters-HeaderContent)
    -  [**6.7** Other Header Setup](#ptx2pdf-MacroSetupParameters-OtherHeaderSetup)
-  [**7** Other](#ptx2pdf-MacroSetupParameters-Other)
-  [**8** Notes](#ptx2pdf-MacroSetupParameters-Notes)
-  [**9** Illustrations (Figures)](#ptx2pdf-MacroSetupParameters-Illustrations(Figures))
-  [**10** Thumb Tabs](#ptx2pdf-MacroSetupParameters-Tabs)
-  [**11** Hooks](#ptx2pdf-MacroSetupParameters-Hooks)
-  [**12** Introduction markers](#ptx2pdf-MacroSetupParameters-IntroMarkers)
-  [**12** Grid and Graphpaper](#ptx2pdf-MacroSetupParameters-Graphpaper)

   [**A.1** Appendix: Common OpenType script tags](#ptx2pdf-MacroSetupParameters-Appendix:CommonOpenTypescripttags)

Text in ```gray``` represents the portion of the setup parameter syntax which can be configured by the typesetter. Where applicable, default values are indicated in parentheses at the end of the definition.

## <a name="TOC-Paratext-Stylesheet">Paratext Stylesheet</a>

<a name="TOC-Paratext-Stylesheet">

*   \stylesheet{```usfm.sty```} – Define the Paratext stylesheet to be used as a basis for formatting (default=usfm.sty)

You can read multiple stylesheets (to override primary stylesheet values)
For example:

*   \stylesheet{```mods.sty```}

In the file ```mods.sty```, add standard Paratext marker style definition parameters to override the default stylesheet definitions provided through \stylesheet{...} (above). Note that the first stylesheet is only loaded if it is used. Also, you cannot change fonts in subsequent stylesheets. Fonts are only loaded once at the beginning of the process.

</a>

<div style="border-width:1px"><a name="TOC-Paratext-Stylesheet"></a>

<div><a name="TOC-Paratext-Stylesheet">

```
\Marker s1
\Justification Left

\Marker r
\Justification Left
```


## <a name="TOC-Paratext-Stylesheet"></a><a name="TOC-Page-Setup">Page Setup</a>


### <a name="TOC-Page-Setup"></a><a name="ptx2pdf-MacroSetupParameters-Dimensions">Dimensions</a>

<a name="ptx2pdf-MacroSetupParameters-Dimensions">

*   \PaperWidth=```148.5mm``` – Page width (default = 148.5mm – A5)
*   \PaperHeight=```210mm``` – Page height (default = 210mm – A5)

</a>

### <a name="ptx2pdf-MacroSetupParameters-Dimensions"></a><a name="ptx2pdf-MacroSetupParameters-CropMarks">Crop Marks</a>

<a name="ptx2pdf-MacroSetupParameters-CropMarks">

*   \CropMarks```true``` – Add crops marks to the PDF output? (default = false)

</a>

### <a name="ptx2pdf-MacroSetupParameters-CropMarks"></a><a name="ptx2pdf-MacroSetupParameters-Margins">Margins</a>

<a name="ptx2pdf-MacroSetupParameters-Margins">

*   \MarginUnit=```12mm``` – Basic unit for margins; changing this will alter them all. (default = 1in)

<div style="margin-left:20px">

**Note:** The following top and bottom margin settings adjust the the size of margins around the body text area. You will need to keep in mind that adequate space needs to be provided for and headers and/or footers.

</div>

*   \def\TopMarginFactor{```1.15```} – Relative size of the top margin based on MarginUnit (default = 1.0)
*   \def\BottomMarginFactor{```1.0```} – Relative size of the bottom margin based on MarginUnit. If undefined, the \TopMarginFactor will be used for both top and bottom margins.

*   \def\SideMarginFactor{```1.0```} – Relative size of side margin based on MarginUnit (default = 0.7)
*   \BindingGutter=```4mm``` – Amount for an additional margin on the binding side of the page (default = 5mm)
    *   \BindingGutter```true``` must be specified for the \BindingGutter amount to be applied (default = false)

</a>

### <a name="ptx2pdf-MacroSetupParameters-Margins"></a><a name="ptx2pdf-MacroSetupParameters-Columns">Columns</a>

<a name="ptx2pdf-MacroSetupParameters-Columns">

*   \TitleColumns=```1``` – Number of columns used to typeset the main title (default = 1)
*   \IntroColumns=```1``` – Number of columns used to typeset introduction material. Introduction material is defined by USFM markers beginning with \i (default = 1)
*   \BodyColumns=```1``` – Number of columns used to typeset the body text (default = 1)
*   \def\ColumnGutterFactor{```15```} – Used to set the size of the gutter between columns; relative to font size
*   \ColumnGutterRule```true``` – Place a vertical line between the columns in the column gutter? (default = false)

</a>

## <a name="ptx2pdf-MacroSetupParameters-Columns"></a><a name="ptx2pdf-MacroSetupParameters-Fonts">Fonts</a>

<a name="ptx2pdf-MacroSetupParameters-Fonts">

*   \FontSizeUnit=```0.75``` – Scaling factor for interpreting font sizes in the stylesheet. Changing this will scale all text proportionately (default = 0.9)

</a>

### <a name="ptx2pdf-MacroSetupParameters-Fonts"></a><a name="ptx2pdf-MacroSetupParameters-Faces">Faces</a>

<a name="ptx2pdf-MacroSetupParameters-Faces">

*   \def\regular{```"Times New Roman"```} – Font to use for text where the marker does not define a font style in the Paratext stylesheet (result is "plain" text)
*   \def\bold{```"Times New Roman/B"```} – Font to use for text where the marker is defined as "\Bold" in the Paratext stylesheet
*   \def\italic{```"Times New Roman/I"```} – Font to use for text where the marker is defined as "\Italic" in the Paratext stylesheet
*   \def\bolditalic{```"Times New Roman/BI"```} – Font to use for text where the marker is defined as "\Bold" + "\Italic" in the Paratext stylesheet

For Mac OS X, use the Postscript Name or Full Name in quotes from Font Book's Font Info.

Script specific features for fonts supporting the selected script can be enabled by adding a "script=" parameter to the end of the font name. For example, in the case of typesetting Arabic script, we might have:
     \def\regular{```"Scheherazade:script=arab"```}

</a>

<a name="ptx2pdf-MacroSetupParameters-Faces">The script parameter is an OpenType script tag. A list of common script tags is presented in an</a> [appendix](#ptx2pdf-MacroSetupParameters-Appendix:CommonOpenTypescripttags) at the end of this document.)

You can also specify a font definition like this directly in a stylesheet marker definition. For example:

```
     \Marker p
     \FontName Scheherazade:script=arab
```

## <a name="ptx2pdf-MacroSetupParameters-TextSpacing">Text Spacing</a>


*   \def\LineSpacingFactor{```1```} – Scaling factor used to adjust line spacing (leading); relative to font size (default = 1.2)
*   \def\VerticalSpaceFactor{```1.0```} – Scaling factor used to adjust amount of vertical spaces applied for usfm.sty SpaceBefore and SpaceAfter values (default = 0.2}

</a>

## <a name="ptx2pdf-MacroSetupParameters-Chapters&amp;Verses">Chapters & Verses</a>

*   \OmitVerseNumberOne```true``` – Omit the first verse number in every chapter? (default = false)
*   \OmitChapterNumber```true``` – Omit the chapter numbers of the book. (Often used for one-chapter books. (default = false)
*   \OmitChapterNumberRH```true``` – Omit the chapter numbers in the running header (RH). (default = false)
*   \def\AdornVerseNumber#1{```(```#1```)```} – Put parentheses around the verse number (which is represented by #1)
*   \def\AfterVerseSpaceFactor{```0```} – Remove extra space after verse numbers, when you have set them to be "invisible", or a very small size, such as \Marker v \FontSize 0.0001
*   ```\def\MakeChapterLabel#1#2{#1\ #2}```   – If there is a global (before `\c 1`) `\cl`, how should that be combined with the chapter number. The default is to put the label (`#1`) before the number (`#2`). Altering this macro would to `\def\MakeChapterLabel#1#2{#2. #1}`  will make Hungarian-style numbering (`23. Zsoltár`) the default rather than English-style (`Psalm 23`).

## <a name="ptx2pdf-MacroSetupParameters-RunningHeader/Footer">Running Header/Footer</a>

### <a name="ptx2pdf-MacroSetupParameters-Header/FooterPosition">Header/Footer Position</a>

*   \def\HeaderPosition{```0.7```} – Position of the baseline of the header relative to the top edge of the paper (not the text area) (default = 0.5)
*   \def\FooterPosition{```0.5```} – Position of the baseline of the footer relative to the bottom edge of the paper (not the text area) (default = 0.5)

The following parameters are used to specify the information to include in the running header (at top of pages, except title pages). Set the items to print at left/center/right of odd and even pages separately.

</a>

### <a name="ptx2pdf-MacroSetupParameters-OddHeader">Odd Header</a>

<a name="ptx2pdf-MacroSetupParameters-OddHeader">
Headers for normal pages with an odd page number, e.g.:
*   \def\RHoddleft{```\empty```}
*   \def\RHoddcenter{```\rangeref```}
*   \def\RHoddright{```\pagenumber```}

</a>

### <a name="ptx2pdf-MacroSetupParameters-EvenHeader">Even Header</a>

<a name="ptx2pdf-MacroSetupParameters-EvenHeader">
Headers for normal pages with an even page number, e.g.:
*   \def\RHevenleft{```\pagenumber```}
*   \def\RHevencenter{```\rangeref```}
*   \def\RHevenright{```\empty```}

</a>

### <a name="ptx2pdf-MacroSetupParameters-TitlepageHeader">Title-page Header</a>

<a name="ptx2pdf-MacroSetupParameters-TitlepageHeader">
Headers for pages that start with the title of a book. e.g.:

*   \def\RHtitleleft{```\empty```}
*   \def\RHtitlecenter{```\empty```}
*   \def\RHtitleright{```\empty```}

</a>

### <a name="ptx2pdf-MacroSetupParameters-NoVpage">Front / back matter Header</a>


Headers for a page that has neither verses nor titles, e.g. a glossary.

*   \def\RHnoVoddleft{```\empty```}
*   \def\RHnoVoddcenter{```\empty```}
*   \def\RHnoVoddright{```\pagenumber```}
*   \def\RHnoVevenleft{```\pagenumber```}
*   \def\RHnoVevencenter{```\empty```}
*   \def\RHnoVevenright{```\empty```}

### <a name="ptx2pdf-MacroSetupParameters-Odd,Even,andTitlepageFooter">Footers</a>

For control over the footer, fifteen similar ```\def``` commands are available, beginning with ```\RF``` instead of ```\RH```.

### <a name="ptx2pdf-MacroSetupParameters-HeaderContent">Header/Footer Content macros</a>

Any appropriate combination of text and TeX macros may be used in the header or footer slots. The following are provided for 
convenience.

*   ```\rangeref``` – Scripture reference of the range of text on the page
*   ```\firstref``` – reference of the first verse on the page
*   ```\lastref``` – reference of the last verse on the page
*   ```\pagenumber``` – the page number
*   ```\empty``` – print nothing in this position
*   ```\usdate```, ```\ukdate```, ```\isodate``` - dates in various formats. (See FAQ for more examples)
*   ```\hrsmins``` - the time of day 


Literal text can also be included (e.g., to add dashes around a centered page number, ```\\def\RFtitlecenter{- \pagenumber -}```).


### <a name="ptx2pdf-MacroSetupParameters-OtherHeaderSetup">Other Header Setup</a>


*   \RHruleposition=```6pt``` – Position of a rule below the running header (default = 10pt)
*   \VerseRefs```true``` – Whether to include verse numbers in header/footer references, or only chapter numbers (default = false)

## <a name="ptx2pdf-MacroSetupParameters-Other">Other</a>

*   \IndentAfterHeading```true``` – Remove paragraph indentation on the first paragraph after a section heading (default = false)
*   ```\def\TPILB{\hfil This Page Intentionally Left Blank}``` Message to appear on intentionally empty pages. The `\hfil` at the start will centre a single line of text. (default empty). 
*  `\EmptyPage` – Insert an intentionally empty page. The macro `\TPILB` will be used to provide any filler content.  Headers and footers will be the `...noV...` versions.

</a>

## <a name="ptx2pdf-MacroSetupParameters-Notes">Notes</a>

<a name="ptx2pdf-MacroSetupParameters-Notes">

*   \AutoCallerStartChar=```97``` – Unicode value of first character to use for auto-generated callers (default = 97 = 'a')
*   \AutoCallerNumChars```26``` – Number of caller characters to generate before restarting sequence (default = 26)
*   \AutoCallers{f|x}{callers csv} – Make the specified note class use a specific sequence of symbols
    *   \AutoCallers{```f```}{```*,+,¶,§,**,++,¶¶,§§```}
    *   \AutoCallers{```x```}{} (this configuration would suppress callers for cross-references)
*   \NumericCallers{```f```} – Make the note class use numeric (instead of alphabetic) callers (specify f _or_ x)
*   \PageResetCallers{```f```} – Restart numbering for the notes class on each page (specify f _or_ x)
*   \OmitCallerInNote{```x```} – To omit callers from the note class at the bottom of the page (specify f _or_ x)
*   \ParagraphedNotes{```x```} – Format the note class as a single paragraph, with larger space between note items (specify f _or_ x)
*   \NoteCallerWidth=```1.2ex``` - Adjust 'standard' width of a footnote-caller in notes area. A small amount of space is added to narrow callers, centering them in a space of this width, so that they and their note text align nicely in the footer. Wider callers take their natural size, without any padding. (default ```1.1ex```) (Control added 22 Sept. 2020)

### End notes
*   \NoteAtEnd{```f```} – To make the specified note class an endnote (default: only ```fe``` 'endnotes' are endnotes). 
*   \notesEachBook```false``` – To place endnotes at the end of the entire volume rather than (default) the end of individual books.(default=true)
*   \def\EndNoteRuleWidth{```0.5```} –  Fraction of column width to make the rule above automatically inserted endnotes (default =```0.5```)
*   \def\EndNoteRuleThickness{```0.4pt```} – Thickness of the rule above automatically inserted endnotes (default=```0.4pt```)
*   \def\AboveEndNoteRule{```14 pt```} – Space between the body text and the  end-note separator line.
*   \def\BelowEndNoteRule{```10 pt```} – Space between the separator line and the start of the end-notes. If this and `\EndNoteRuleAbove` add up to a whole number, then (with the default definition for `\EndNoteSeparator`) then gridding will be preserved. I.e. the macros will not ensure the above end note rule will keep to the grid.

#### Custom end-note use
*   \zplaceallnotes – Non-standard USFM marker to place any currently-waiting endnotes (with preceding endnote rule and spacing, if there are any endnotes).
*   \zpostendnoterule – Non-standard USFM marker to place an endnote rule, positioned 0.5 lineskips above the baseline.   This might be wanted, for example, if endnotes are put mid-text, or within a mid-text side-bar. If no endnotes were found during the last call to ```\zplaceallnotes```, this produces no output.
*   \zendnoterule – Non-standard USFM marker to unconditionally place the (pre-) endnote rule (with surrounding spacing) at this place (for use before the command below)
*   \zplacenotes-```X``` – Non-standard USFM marker to place endnotes of a particular type collected until now. E.g. If ```\fe``` notes are endnotes, ```\zplacenotes-fe``` will place those notes at the specified place.  This *does not* change the flag used by ```\zpostendnoterule```. 
*  \ztestnotes-```X``` – Non-standard USFM marker to *test* for currently-waiting end-notes of a particular type, and  set or unset the flag used by ```\zpostendnoterule```. Note that the behaviour of this command is not the same as the logic of ```\zplaceallnotes```, which tests to see if *any* end-note has contents. Also note that after the contents have been placed on the page, the end-note is not waiting by definition, therefore this should only be used before the relevant ```\zplacenotes-X```

### Footnote rule control
_For now_, if you want to change the appearance of (or remove) the footnote rule, redefine \def\footnoterule

*   \def\footnoterule{} – No footnote rule will be applied if the definition is empty (as in this example)
*   \def\EndNoteSeparator{} – No endnote rule will be placed if the definition is empty (as in this example). Alternatively the definition might include an image.

</a>

## <a name="ptx2pdf-MacroSetupParameters-Illustrations(Figures)">Illustrations (Figures)</a>

<a name="ptx2pdf-MacroSetupParameters-Illustrations(Figures)">

*   \IncludeFigures```true``` – Output illustrations (figures) marked in the text with USFM <tt>\fig...\fig*</tt> markup? (default = true)

*   \FigurePlaceholders```false``` – Operate in "figure placeholders" mode? If true, the macros will read your picture definitions, but only render a rectangular frame containing the text of the filename, rather than the actual graphic. (default = false)

</a>

## <a name="ptx2pdf-MacroSetupParameters-Tabs">Table of Contents control </a>
* \GenerateTOC[title]{filename} - where [title] is optional, default is "Table of Contents"
 Writes TOC entries from \toc1, \toc2, \toc3 markers to the given file, which can be used directly with \ptxfile{...}
 or renamed and edited as needed to customize the TOC.
* \useTOCone```true``` - Include parameter of `\toc1` (Full name) in above table of contents file. (default = true)
* \useTOtwo```true``` - Include  `\toc2` (Short name) in from above table of contents file. (default = true)
* \useTOCthree```true``` - Include `\toc3` (Abbreviation) in from above table of contents file. (default = true)


## <a name="ptx2pdf-MacroSetupParameters-Tabs">Thumb tabs</a>

See <a href="thumbtabs.md">the feature-specific documentation</a> for a more extensive discussion.
 
* \setthumbtab{`GEN`}{`1`} - generate a page-edge thumb-tab for all pages in the book of Genesis. The code (```GEN``` in the example) must be an exact match of the code used in the USFM `\id` marker.  All `\setthumbtab` commands should be complete before the first `\ptxfile` is loaded. The number (```1``` in the example), is termed `index number` in this documentation and (together with parameters below) controls the vertical position of the tabs for the given book, with 1 being nearest the top of the page.  
* \def\tabBoxCol{```0.2 0.3 0.2```} colour definition for the thumb-tab, the 3 numbers representing red, green and blue in the range of 0 (black), 0.5 (half)  to 1 (fully lit). (Default ```0 0 0```).
* \def\tabFontCol{```0.5 1 0.5```} colour definition for the thumb-tab, the 3 numbers representing red, green and blue in the range of 0 (black), 0.5 (half)  to 1 (fully lit). (Default ```1 1 1```).
* \tabheight=```50pt``` Vertical dimension of the thumbtab. (default 50pt).
* \tabwidth=```25pt``` Vertical dimension of the thumbtab. (default 15pt).
* \TabRotationNormal```true``` When this is true, then when the ```\tabheight``` > ```\tabwidth``` the text on the tab will be rotated, and otherwise it will be horizontal. If false, the logic is inverted. This may be useful to force horizontal text in tall tabs, or if the assumption that the text is wider than it is tall is incorrect.

* \setthumbtab{`PSA`}{} - Undo an earlier \setthumbtab command. 
* \setthumbtabFg{`PSA`}{0 1 0.8} - Override the default foreground colour `\tabFontCol` for the given book.
* \setthumbtabBg{`REV`}{0.3 0.3 0} - Override the default background colour `\tabBoxCol` for the given book.

* \TOCthreetab```true``` - if false, then thumb-tabs will not have their content from  the `\toc3` entry. This will leave the tab blank unless set via the custom USFM marker ```\zthumbtab```. (default = true)
* \def\ThumbTabStyle{```toc3```} - use specified marker for selecting the font, size, weight, etc.  (default = toc3)
* \NumTabs=```5``` - Pre-set / reset the number of tabs between which the available space will be divided. Normally there is no need to set this number, as ```\setthumbtab{ZEC}{39}``` will set it to 39 unless it is already larger than that.  
* \TabsStart=```10pt``` Distance between the upper edge of the topmost thumb-tab and the top margin of the page (text area). Negative values may be given to extend tabs into the upper margin.
* \TabsEnd=```10pt``` Distance between the lower edge of the lowermost thumb-tab and the bottom page margin (text area). Negative values may be given to extend tabs into the lower margins.
* \def\TabBleed{```1pt```} - Amount the tab goes over the edge of the page. (default 1pt)


## ><a name="ptx2pdf-MacroSetupParameters-Hooks">Hooks</a>

<a name="ptx2pdf-MacroSetupParameters-Hooks">

Hooks can insert something (text, or any valid TeX instruction/control sequence) to the output, at selected marker (style) location(s).

*   \sethook{location}{marker}{insert}
    Example: \sethook{```start```}{```s1```}{```~```}

    Valid locations are:
    *   before – prior to the start of the par or style run containing the selected style text (before its definition is applied)
    *   after – after the end of the par or style run containing the selected style text (after its definition is terminated)
    *   start – before the start of the selected style text (but after the paragraph or character style definition is applied)
    *   end – after the end of the selected style text (but before the paragraph or character style definition is terminated)

</a></div>


A useful hook is the command to "hang" verse numbers into the paragraph indent, often wanted on poetry styles:
     \sethook{```start```}{```q1```}{```\hangversenumber```}
     \sethook{```start```}{```q2```}{```\hangversenumber```}

This allows a verse number at the beginning of a paragraph to be typeset "hanging" into the paragraph indent, so that the text itself starts at the usual indent position. This is often used with poetic sections (\q# markers), so that the actual text stays neatly aligned for lines both with and without verse numbers.

## <a name=#ptx2pdf-MacroSetupParameters-IntroMarkers">Introductory Markers</a>
Introductory markers (those starting i, such as `\ip`) are used for book introductions 
and are often set in a full-width single column, even when the verse text is in
dual columns. The code has, until now, assumed that this should always be the case.
However, some introductory markers have a dual role, and serve as bridging text
or chapter introductions. In this use-case they should *not* trigger a swap to 
single column mode.  In normal scripture, it is thus appropriate that -
after the first chapter mark has been met - this swapping between dual and
single column mode should be prevented.

A complication is that in a Paratext module, it is very possible that multiple 
books appear in a given USFM file, and in this case it would appropriate that
introductory markers exit from dual column mode, and return to single column
mode.  The XeTeX macros are unable to decide on their own how the markers are
being used. The following setup parameters will hopefully help.

* \introAmbigious{```iex```} –  The marker specified will not initiate any
  swapping between single or double columns (in either direction). This also means
  it should not ever be the first marker in a book introduction. (default: only
  `\iex` has been declared ambiguous, as it is sometimes used for bridging
  material).
 
* ```\ReenterIntroOKtrue``` – old behaviour, a marker starting i (introductory
marker) will start single-column text, unless it's been declared ambiguous like
\iex was as a stop-gap measure (this approach presents its own problems -
ambiguous markers will not start single-column text at the start of a book
either).

* ```\ReenterIntroOKfalse``` – chapter numbers set an internal flag to true.
Once this flag is set, then all markers are treated as body-text markers. The
problematic ambiguous markers are no longer treated as ambiguous, (except for
```\tr```). The internal flag is set to false at the start of a book.


## <a name="#ptx2pdf-MacroSetupParameters-Graphpaper"> Graph-paper and Grid</a>

Sometimes it is useful to display a graph-paper-like measurement grid or  the
grid which the text is (should be) layed out to.
 * ```\def\doLines{\doGraphPaper}``` Display graph-paper
 * ```\def\doLines{\doGridLines}``` Display gridlines
 * ```\def\doLines{\doGraphPaper\doGridLines}``` Display both gridlines and graphpaper

The grid is set up using the page parameters, and the graph-paper as below. If
any of these are changed part-way through a control-file (e.g. line spacing is altered 
before the start of the glossary) then the (cached) 'background page' should be
cleared, so that the old page is not reused.
```
  \setbox\gp@box=\box\voidb@x
```
### Graph-paper setup
 * ```\def\GraphPaperX{2mm}``` Horizontal spacing of the the grid lines on the graph-paper
 * ```\def\GraphPaperY{2mm}``` Vertical spacing of the grid lines on the graph-paper
 * ```\def\GraphPaperMajorDiv{5}``` Every fifth division will be styled as a major division.
 * ```\def\GraphPaperXoffset{0.0cm}```	Start (and stop) of the graph-paper relative to the nearest horizontal edge
 * ```\def\GraphPaperYoffset{0.0cm}```	Start (and stop) of the graph-paper relative to the nearest vertical edge
 * ```\def\GraphPaperLineMajor{0.6pt}``` Width of a major graph-paper line
 * ```\def\GraphPaperColMajor{0.8 0.6 0.6} ```  Colour a major graph-paper line (R G B)
 * ```\def\GraphPaperLineMinor{0.3pt}```Width of a minor graph-paper line
 * ```\def\GraphPaperColMinor{0.85 0.85 1.0} ```  Colour a minor graph-paperline (R G B)
 * ```\def\GridPaperLineMajor{0.6pt}``` Width of a major grid-paper line
 * ```\def\GridPaperColMajor{0.8 0.6 0.6} ```  Colour of of a major grid-paper line
 * ```\def\GridPaperLineMinor{0.3pt}``` Width of a minor grid-paperline
 * ```\def\GridPaperColMinor{0.85 0.85 1.0}```   Colour of a minor grid-paper line (R G B)
 
* * *

<a name="ptx2pdf-MacroSetupParameters-scriptTags"></a>

<a name="ptx2pdf-MacroSetupParameters-scriptTags"></a>

### <a name="ptx2pdf-MacroSetupParameters-scriptTags"></a><a name="ptx2pdf-MacroSetupParameters-Appendix:CommonOpenTypescripttags">Appendix: Common OpenType script tags</a>

<a name="ptx2pdf-MacroSetupParameters-Appendix:CommonOpenTypescripttags">

<table class="sites-layout-name-one-column sites-layout-hbox" cellspacing="0">

<tbody>

<tr>

<th>Tag</th>

<th>Script</th>

</tr>

<tr>

<td>arab</td>

<td>Arabic</td>

</tr>

<tr>

<td>armn</td>

<td>Armenian</td>

</tr>

<tr>

<td>beng</td>

<td>Bengali</td>

</tr>

<tr>

<td>bopo</td>

<td>Bopomofo</td>

</tr>

<tr>

<td>cans</td>

<td>Canadian Syllabics</td>

</tr>

<tr>

<td>cher</td>

<td>Cherokee</td>

</tr>

<tr>

<td>hani</td>

<td>CJK Ideographic</td>

</tr>

<tr>

<td>cyrl</td>

<td>Cyrillic</td>

</tr>

<tr>

<td>deva</td>

<td>Devanagari</td>

</tr>

<tr>

<td>ethi</td>

<td>Ethiopic</td>

</tr>

<tr>

<td>geor</td>

<td>Georgian</td>

</tr>

<tr>

<td>grek</td>

<td>Greek</td>

</tr>

<tr>

<td>gujr</td>

<td>Gujarati</td>

</tr>

<tr>

<td>guru</td>

<td>Gurmukhi</td>

</tr>

<tr>

<td>jamo</td>

<td>Hangul Jamo</td>

</tr>

<tr>

<td>hang</td>

<td>Hangul</td>

</tr>

<tr>

<td>hebr</td>

<td>Hebrew</td>

</tr>

<tr>

<td>kana</td>

<td>Hiragana</td>

</tr>

<tr>

<td>knda</td>

<td>Kannada</td>

</tr>

<tr>

<td>kana</td>

<td>Katakana</td>

</tr>

<tr>

<td>khmr</td>

<td>Khmer</td>

</tr>

<tr>

<td>lao</td>

<td>Lao</td>

</tr>

<tr>

<td>mlym</td>

<td>Malayalam</td>

</tr>

<tr>

<td>mong</td>

<td>Mongolian</td>

</tr>

<tr>

<td>mymr</td>

<td>Myanmar</td>

</tr>

<tr>

<td>orya</td>

<td>Oriya</td>

</tr>

<tr>

<td>sinh</td>

<td>Sinhala</td>

</tr>

<tr>

<td>syrc</td>

<td>Syriac</td>

</tr>

<tr>

<td>taml</td>

<td>Tamil</td>

</tr>

<tr>

<td>telu</td>

<td>Telugu</td>

</tr>

<tr>

<td>thaa</td>

<td>Thaana</td>

</tr>

<tr>

<td>thai</td>

<td>Thai</td>

</tr>

<tr>

<td>tibt</td>

<td>Tibetan</td>

</tr>

<tr>

<td>yi</td>

<td>Yi</td>

</tr>

</tbody>

</table>

</a></div>


<a name="ptx2pdf-MacroSetupParameters-Appendix:CommonOpenTypescripttags">
<small>Updated on <abbr class="updated" title="2011-05-18T19:45:59.877Z">May 18, 2011</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">8</span>)</small>

* * *



**Attachments (1)**

</a>

<div class="hentry attachment" id="https://sites.google.com/feeds/content/icapmail.org/ptx2pdf/4849046698044518104"><a name="ptx2pdf-MacroSetupParameters-Appendix:CommonOpenTypescripttags"></a>

[ptx2pdf-MacroSetupParameters.pdf](ptx2pdf-MacroSetupParameters.pdf) - on <abbr class="updated" title="2011-05-17T19:48:01.362Z">May 17, 2011</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">1</span>)
</div>
