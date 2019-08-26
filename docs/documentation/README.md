# Navigation

[Cookbook](../cookbook/README.md) | Documentation | [Home](../home/README.md)  | [Installation](../installation/README.md) | [Quick Start](../quick-start/README.md)


### Documentation

A [PDF](../documentation/ptx2pdf-MacroSetupParameters.pdf?attredirects=0/index.html) version of this document is also available.  

#### Contents

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
    -  [**6.5** Odd, Even, and Title-page Footer](#ptx2pdf-MacroSetupParameters-Odd,Even,andTitlepageFooter)
    -  [**6.6** Other Header Setup](#ptx2pdf-MacroSetupParameters-OtherHeaderSetup)
-  [**7** Other](#ptx2pdf-MacroSetupParameters-Other)
-  [**8** Notes](#ptx2pdf-MacroSetupParameters-Notes)
-  [**9** Illustrations (Figures)](#ptx2pdf-MacroSetupParameters-Illustrations(Figures))
-  [**10** Hooks](#ptx2pdf-MacroSetupParameters-Hooks)
    -  [**10.1** Appendix: Common OpenType script tags](#ptx2pdf-MacroSetupParameters-Appendix:CommonOpenTypescripttags)



Text in <span style="color:rgb(255,0,0)">red</span> represents the portion of the setup parameter syntax which can be configured by the typesetter. Where applicable, default values are indicated in parentheses at the end of the definition.

## <a name="TOC-Paratext-Stylesheet">Paratext Stylesheet</a>

<a name="TOC-Paratext-Stylesheet">

*   \stylesheet{<font color="red">usfm.sty</font>} – Define the Paratext stylesheet to be used as a basis for formatting (default=usfm.sty)

You can read multiple stylesheets (to override primary stylesheet values)  
For example:

*   \stylesheet{<font color="red">mods.sty</font>}

In the file <font color="red">mods.sty</font>, add standard Paratext marker style definition parameters to override the default stylesheet definitions provided through \stylesheet{...} (above). Note that the first stylesheet is only loaded if it is used. Also, you cannot change fonts in subsequent stylesheets. Fonts are only loaded once at the beginning of the process.

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

*   \PaperWidth=<font color="red">148.5mm</font> – Page width (default = 148.5mm – A5)
*   \PaperHeight=<font color="red">210mm</font> – Page height (default = 210mm – A5)

</a>

### <a name="ptx2pdf-MacroSetupParameters-Dimensions"></a><a name="ptx2pdf-MacroSetupParameters-CropMarks">Crop Marks</a>

<a name="ptx2pdf-MacroSetupParameters-CropMarks">

*   \CropMarks<font color="red">true</font> – Add crops marks to the PDF output? (default = false)

</a>

### <a name="ptx2pdf-MacroSetupParameters-CropMarks"></a><a name="ptx2pdf-MacroSetupParameters-Margins">Margins</a>

<a name="ptx2pdf-MacroSetupParameters-Margins">

*   \MarginUnit=<font color="red">12mm</font> – Basic unit for margins; changing this will alter them all. (default = 1in)

<div style="margin-left:20px">

**Note:** The following top and bottom margin settings adjust the the size of margins around the body text area. You will need to keep in mind that adequate space needs to be provided for and headers and/or footers.

</div>

*   \def\TopMarginFactor{<font color="red">1.15</font>} – Relative size of the top margin based on MarginUnit (default = 1.0)
*   \def\BottomMarginFactor{<font color="red">1.0</font>} – Relative size of the bottom margin based on MarginUnit. If undefined, the \TopMarginFactor will be used for both top and bottom margins.  

*   \def\SideMarginFactor{<font color="red">1.0</font>} – Relative size of side margin based on MarginUnit (default = 0.7)
*   \BindingGutter=<font color="red">4mm</font> – Amount for an additional margin on the binding side of the page (default = 5mm)
    *   \BindingGutter<font color="red">true</font> must be specified for the \BindingGutter amount to be applied (default = false)

</a>

### <a name="ptx2pdf-MacroSetupParameters-Margins"></a><a name="ptx2pdf-MacroSetupParameters-Columns">Columns</a>

<a name="ptx2pdf-MacroSetupParameters-Columns">

*   \TitleColumns=<font color="red">1</font> – Number of columns used to typeset the main title (default = 1)
*   \IntroColumns=<font color="red">1</font> – Number of columns used to typeset introduction material. Introduction material is defined by USFM markers beginning with \i (default = 1)
*   \BodyColumns=<font color="red">1</font> – Number of columns used to typeset the body text (default = 1)
*   \def\ColumnGutterFactor{<font color="red">15</font>} – Used to set the size of the gutter between columns; relative to font size
*   \ColumnGutterRule<font color="red">true</font> – Place a vertical line between the columns in the column gutter? (default = false)

</a>

## <a name="ptx2pdf-MacroSetupParameters-Columns"></a><a name="ptx2pdf-MacroSetupParameters-Fonts">Fonts</a>

<a name="ptx2pdf-MacroSetupParameters-Fonts">

*   \FontSizeUnit=<font color="red">0.75</font> – Scaling factor for interpreting font sizes in the stylesheet. Changing this will scale all text proportionately (default = 0.9)

</a>

### <a name="ptx2pdf-MacroSetupParameters-Fonts"></a><a name="ptx2pdf-MacroSetupParameters-Faces">Faces</a>

<a name="ptx2pdf-MacroSetupParameters-Faces">

*   \def\regular{<font color="red">"Times New Roman"</font>} – Font to use for text where the marker does not define a font style in the Paratext stylesheet (result is "plain" text)
*   \def\bold{<font color="red">"Times New Roman/B"</font>} – Font to use for text where the marker is defined as "\Bold" in the Paratext stylesheet
*   \def\italic{<font color="red">"Times New Roman/I"</font>} – Font to use for text where the marker is defined as "\Italic" in the Paratext stylesheet
*   \def\bolditalic{<font color="red">"Times New Roman/BI"</font>} – Font to use for text where the marker is defined as "\Bold" + "\Italic" in the Paratext stylesheet

For Mac OS X, use the Postscript Name or Full Name in quotes from Font Book's Font Info.

Script specific features for fonts supporting the selected script can be enabled by adding a "script=" parameter to the end of the font name. For example, in the case of typesetting Arabic script, we might have:  
     \def\regular{<font color="red">"Scheherazade:script=arab"</font>}

</a>

<a name="ptx2pdf-MacroSetupParameters-Faces">The script parameter is an OpenType script tag. A list of common script tags is presented in an</a> [appendix](#ptx2pdf-MacroSetupParameters-Appendix:CommonOpenTypescripttags) at the end of this document.)  

You can also specify a font definition like this directly in a stylesheet marker definition. For example:  

```
     \Marker p  
     \FontName Scheherazade:script=arab
```

## <a name="ptx2pdf-MacroSetupParameters-TextSpacing">Text Spacing</a>

<a name="ptx2pdf-MacroSetupParameters-TextSpacing">

*   \def\LineSpacingFactor{<font color="red">1</font>} – Scaling factor used to adjust line spacing (leading); relative to font size (default = 1.2)
*   \def\VerticalSpaceFactor{<font color="red">1.0</font>} – Scaling factor used to adjust amount of vertical spaces applied for usfm.sty SpaceBefore and SpaceAfter values (default = 0.2}

</a>

## <a name="ptx2pdf-MacroSetupParameters-TextSpacing"></a><a name="ptx2pdf-MacroSetupParameters-Chapters&amp;Verses">Chapters & Verses</a>

<a name="ptx2pdf-MacroSetupParameters-Chapters&amp;Verses">

*   \OmitVerseNumberOne<font color="red">true</font> – Omit the first verse number in every chapter? (default = false)
*   \OmitChapterNumber<font color="red">true</font> – Omit the chapter numbers of the book. (Often used for one-chapter books. (default = false)
*   \OmitChapterNumberRH<font color="red">true</font> – Omit the chapter numbers in the running header (RH). (default = false)
*   \def\AdornVerseNumber#1{<font color="red">(</font>#1<font color="red">)</font>} – Put parentheses around the verse number (which is represented by #1)
*   \def\AfterVerseSpaceFactor{<font color="red">0</font>} – Remove extra space after verse numbers, when you have set them to be "invisible", or a very small size, such as \Marker v \FontSize 0.0001

</a>

## <a name="ptx2pdf-MacroSetupParameters-Chapters&amp;Verses"></a><a name="ptx2pdf-MacroSetupParameters-RunningHeader/Footer">Running Header/Footer</a>

<a name="ptx2pdf-MacroSetupParameters-RunningHeader/Footer"></a>

### <a name="ptx2pdf-MacroSetupParameters-RunningHeader/Footer"></a><a name="ptx2pdf-MacroSetupParameters-Header/FooterPosition">Header/Footer Position</a>

<a name="ptx2pdf-MacroSetupParameters-Header/FooterPosition">

*   \def\HeaderPosition{<font color="red">0.7</font>} – Position of the baseline of the header relative to the top edge of the paper (not the text area) (default = 0.5)
*   \def\FooterPosition{<font color="red">0.5</font>} – Position of the baseline of the footer relative to the bottom edge of the paper (not the text area) (default = 0.5)

The following parameters are used to specify the information to include in the running header (at top of pages, except title pages). Set the items to print at left/center/right of odd and even pages separately.

</a>

### <a name="ptx2pdf-MacroSetupParameters-Header/FooterPosition"></a><a name="ptx2pdf-MacroSetupParameters-OddHeader">Odd Header</a>

<a name="ptx2pdf-MacroSetupParameters-OddHeader">

*   \def\RHoddleft{<font color="red">\empty</font>}
*   \def\RHoddcenter{<font color="red">\rangeref</font>}
*   \def\RHoddright{<font color="red">\pagenumber</font>}

</a>

### <a name="ptx2pdf-MacroSetupParameters-OddHeader"></a><a name="ptx2pdf-MacroSetupParameters-EvenHeader">Even Header</a>

<a name="ptx2pdf-MacroSetupParameters-EvenHeader">

*   \def\RHevenleft{<font color="red">\pagenumber</font>}
*   \def\RHevencenter{<font color="red">\rangeref</font>}
*   \def\RHevenright{<font color="red">\empty</font>}

</a>

### <a name="ptx2pdf-MacroSetupParameters-EvenHeader"></a><a name="ptx2pdf-MacroSetupParameters-TitlepageHeader">Title-page Header</a>

<a name="ptx2pdf-MacroSetupParameters-TitlepageHeader">

*   \def\RHtitleleft{<font color="red">\empty</font>}
*   \def\RHtitlecenter{<font color="red">\empty</font>}
*   \def\RHtitleright{<font color="red">\empty</font>}

</a>

### <a name="ptx2pdf-MacroSetupParameters-TitlepageHeader"></a><a name="ptx2pdf-MacroSetupParameters-Odd,Even,andTitlepageFooter">Odd, Even, and Title-page Footer</a>

<a name="ptx2pdf-MacroSetupParameters-Odd,Even,andTitlepageFooter">

Nine similar \def commands are available, beginning with \RF instead of \RH.

**Header/Footer Content Parameters**  

*   \rangeref – Scripture reference of the range of text on the page
*   \firstref – reference of the first verse on the page
*   \lastref – reference of the last verse on the page
*   \pagenumber – the page number
*   \empty – print nothing in this position

</a>

<div><a name="ptx2pdf-MacroSetupParameters-Odd,Even,andTitlepageFooter">

Literal text can also be included (e.g., to add dashes around a centered page number, like <font color="red">- \pagenumber -</font>).

</a>

### <a name="ptx2pdf-MacroSetupParameters-Odd,Even,andTitlepageFooter"></a><a name="ptx2pdf-MacroSetupParameters-OtherHeaderSetup">Other Header Setup</a>

<a name="ptx2pdf-MacroSetupParameters-OtherHeaderSetup">

*   \RHruleposition=<font color="red">6pt</font> – Position of a rule below the running header (default = 10pt)
*   \VerseRefs<font color="red">true</font> – Whether to include verse numbers in header/footer references, or only chapter numbers (default = false)

</a>

## <a name="ptx2pdf-MacroSetupParameters-OtherHeaderSetup"></a><a name="ptx2pdf-MacroSetupParameters-Other">Other</a>

<a name="ptx2pdf-MacroSetupParameters-Other">

*   \IndentAfterHeading<font color="red">true</font> – Remove paragraph indentation on the first paragraph after a section heading (default = false)

</a>

## <a name="ptx2pdf-MacroSetupParameters-Other"></a><a name="ptx2pdf-MacroSetupParameters-Notes">Notes</a>

<a name="ptx2pdf-MacroSetupParameters-Notes">

*   \AutoCallerStartChar=<font color="red">97</font> – Unicode value of first character to use for auto-generated callers (default = 97 = 'a')
*   \AutoCallerNumChars<font color="red">26</font> – Number of caller characters to generate before restarting sequence (default = 26)
*   \AutoCallers{f|x}{callers csv} – Make the specified note class use a specific sequence of symbols
    *   \AutoCallers{<font color="red">f</font>}{<font color="red">*,+,¶,§,**,++,¶¶,§§</font>}
    *   \AutoCallers{<font color="red">x</font>}{} (this configuration would suppress callers for cross-references)
*   \NumericCallers{<font color="red">f</font>} – Make the note class use numeric (instead of alphabetic) callers (specify f _or_ x)
*   \PageResetCallers{<font color="red">f</font>} – Restart numbering for the notes class on each page (specify f _or_ x)
*   \OmitCallerInNote{<font color="red">x</font>} – To omit callers from the note class at the bottom of the page (specify f _or_ x)
*   \ParagraphedNotes{<font color="red">x</font>} – Format the note class as a single paragraph, with larger space between note items (specify f _or_ x)

_For now_, if you want to change the appearance of (or remove) the footnote rule, redefine \def\footnoterule

*   \def\footnoterule{} – No footnote rule will be applied if the definition is empty (as in this example)

</a>

## <a name="ptx2pdf-MacroSetupParameters-Notes"></a><a name="ptx2pdf-MacroSetupParameters-Illustrations(Figures)">Illustrations (Figures)</a>

<a name="ptx2pdf-MacroSetupParameters-Illustrations(Figures)">

*   \IncludeFigures<font color="red">true</font> – Output illustrations (figures) marked in the text with USFM <tt>\fig...\fig*</tt> markup? (default = true)

*   \FigurePlaceholders<font color="red">false</font> – Operate in "figure placeholders" mode? If true, the macros will read your picture definitions, but only render a rectangular frame containing the text of the filename, rather than the actual graphic. (default = false)

</a>

## <a name="ptx2pdf-MacroSetupParameters-Illustrations(Figures)"></a><a name="ptx2pdf-MacroSetupParameters-Hooks">Hooks</a>

<a name="ptx2pdf-MacroSetupParameters-Hooks">

Hooks can insert something (text, or any valid TeX instruction/control sequence) to the output, at selected marker (style) location(s).

*   \sethook{location}{marker}{insert}  
    Example: \sethook{<font color="red">start</font>}{<font color="red">s1</font>}{<font color="red">~</font>}  

    Valid locations are:
    *   before – prior to the start of the par or style run containing the selected style text (before its definition is applied)
    *   after – after the end of the par or style run containing the selected style text (after its definition is terminated)
    *   start – before the start of the selected style text (but after the paragraph or character style definition is applied)
    *   end – after the end of the selected style text (but before the paragraph or character style definition is terminated)

</a></div>


A useful hook is the command to "hang" verse numbers into the paragraph indent, often wanted on poetry styles:  
     \sethook{<font color="red">start</font>}{<font color="red">q1</font>}{<font color="red">\hangversenumber</font>}  
     \sethook{<font color="red">start</font>}{<font color="red">q2</font>}{<font color="red">\hangversenumber</font>}  

This allows a verse number at the beginning of a paragraph to be typeset "hanging" into the paragraph indent, so that the text itself starts at the usual indent position. This is often used with poetic sections (\q# markers), so that the actual text stays neatly aligned for lines both with and without verse numbers.  

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

<a name="ptx2pdf-MacroSetupParameters-Appendix:CommonOpenTypescripttags"></a></div>

<a name="ptx2pdf-MacroSetupParameters-Appendix:CommonOpenTypescripttags"></a></div>

<a name="ptx2pdf-MacroSetupParameters-Appendix:CommonOpenTypescripttags"></a></div>

<a name="ptx2pdf-MacroSetupParameters-Appendix:CommonOpenTypescripttags"></a></div>

<a name="ptx2pdf-MacroSetupParameters-Appendix:CommonOpenTypescripttags">  
<small>Updated on <abbr class="updated" title="2011-05-18T19:45:59.877Z">May 18, 2011</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">8</span>)</small>  

* * *


<div><a name="ptx2pdf-MacroSetupParameters-Appendix:CommonOpenTypescripttags">
	
**Attachments (1)**  

</a>

<div class="hentry attachment" id="https://sites.google.com/feeds/content/icapmail.org/ptx2pdf/4849046698044518104"><a name="ptx2pdf-MacroSetupParameters-Appendix:CommonOpenTypescripttags"></a>

[ptx2pdf-MacroSetupParameters.pdf](ptx2pdf-MacroSetupParameters.pdf) - on <abbr class="updated" title="2011-05-17T19:48:01.362Z">May 17, 2011</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">1</span>)</div>

