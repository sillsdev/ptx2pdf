
# Navigation
[Cookbook](../cookbook/README.md) | [Documentation](../documentation/README.md) | [Home](../home/README.md)  | [Installation](../installation/README.md) | Quick Start


### Quick Start

To get started with ptx2pdf you need XeTeX and the ptx2pdf macro package installed. (Instructions can be found here.) We have a sample project that can be downloaded here - [ptx2pdf-sample-GLW.zip](../quick-start/ptx2pdf-sample-GLW.zip?attredirects=0/index.html)  

A typical ptx2pdf project consists of:  

*   project file, this is the tex file that contains the references to all the files that are needed,
*   setup file, this is a txt file that contains the user defined setups,
*   usfm.sty, the standard USFM style sheet,
*   one or more sfm file(s) containing the formated scripture(s)

## <a name="TOC-The-project-file-e.g.-GLW.tex">The project file, e.g. GLW.tex</a>

<a name="TOC-The-project-file-e.g.-GLW.tex">This file links the macros and the style sheet and the actual scripture file(s). The sample project file looks like this:  

```
% sample ptx2pdf-project file

\input paratext2.tex % first we \input the ptx2pdf macro package
\input GLW-setup.txt % then we \input the setup file

\ptxfile{Intro-GLW.sfm} % we use \ptxfile to input the sfm files
\ptxfile{43-JHN-GLW.sfm}
\ptxfile{62-1JN-GLW.sfm}
\ptxfile{63-2JN-GLW.sfm}
\ptxfile{64-3JN-GLW.sfm}

\end % and this is how we end this file
```

</a>

## <a name="TOC-The-project-file-e.g.-GLW.tex"></a><a name="TOC-The-setup-file-e.g.-GLW-setup.txt">The setup file, e.g. GLW-setup.txt</a>

<a name="TOC-The-setup-file-e.g.-GLW-setup.txt">This file contains the user accessible setups for this project. The sample project setup file looks like this:  

```
% GLW-setup
%
% Paratext-to-PDF converter setup for GLW example
%
% This file defines some basic parameters that control the format of the output

% Dimensions of A5 paper
\PaperWidth=148.5mm
\PaperHeight=210mm

\CropMarkstrue

% Basic unit for margins; changing this will alter them all
\MarginUnit=.75in

% Relative sizes of margins, based on the unit above
\def\TopMarginFactor{1.0}
\def\BottomMarginFactor{1.0}
\def\SideMarginFactor{0.75}

% Fonts to use for "plain", "bold", "italic", and "bold italic" from the Paratext stylesheet
% (they need not really be italic, etc, of course)
\def\regular{"Charis SIL"}
\def\bold{"Charis SIL/B"}
\def\italic{"Charis SIL/I"}
\def\bolditalic{"Charis SIL/BI"}

% Use right-to-left layout mode
%\RTLtrue

% Unit for font sizes in the stylesheet; changing this will scale all text proportionately
\FontSizeUnit=0.8pt

% Scaling factor used to adjust line spacing, relative to font size
\def\LineSpacingFactor{1.05}
\def\VerticalSpaceFactor{1.0}

% Information to include in the running header (at top of pages, except first)
% We set the items to print at left/center/right of odd and even pages separately
% Possible contents:
%   \rangeref = Scripture reference of the range of text on the page;
%   \firstref = reference of the first verse on the page)
%   \lastref = reference of the last verse on the page)
%   \pagenumber = the page number
%   \empty = print nothing in this position
\def\RHoddleft{\empty}
\def\RHoddcenter{\empty}
\def\RHoddright{\rangeref}

\def\RHevenleft{\rangeref}
\def\RHevencenter{\empty}
\def\RHevenright{\empty}

\def\RHtitleleft{\empty}
\def\RHtitlecenter{\empty}
\def\RHtitleright{\empty}

\def\RFoddcenter{\pagenumber}
\def\RFevencenter{\pagenumber}
\def\RFtitlecenter{\pagenumber}

\VerseRefstrue % whether to include verse number in running head, or only chapter

\OmitVerseNumberOnetrue % whether to skip printing verse number 1 at start of chapter
%\IndentAtChaptertrue % whether to use paragraph indent at drop-cap chapter numbers

\AutoCallers{f}{*,?,?,¶,§}
\PageResetCallers{f}  
%\NumericCallers{f}
%\OmitCallerInNote{f}

\ParagraphedNotes{x} % reformat \x notes as a single paragraph

\TitleColumns=1
\IntroColumns=1
\BodyColumns=2

\def\ColumnGutterFactor{15} % gutter between double cols, relative to font size

%\BindingGuttertrue % add extra margin of \BindingGutter on binding side
%\BindingGutter=10pt
%\DoubleSidedfalse

% Define the Paratext stylesheet to be used as a basis for formatting
\stylesheet{usfm.sty}
\stylesheet{GLW-custom.sty} % here we load a custom style sheet overriding some of the defaults
```


## <a name="TOC-The-setup-file-e.g.-GLW-setup.txt"></a><a name="TOC-Typesetting-GLW.tex">Typesetting GLW.tex</a>

<a name="TOC-Typesetting-GLW.tex">To typeset GLW.tex open the file in your standard TeX editor to typeset or type in terminal: </a> 

```xetex GLW.tex```



<a name="TOC-Typesetting-GLW.tex">



<small>Updated on <abbr class="updated" title="2011-05-17T19:37:25.726Z">May 17, 2011</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">4</span>)</small>  

* * *

**Attachments (1)**  

[ptx2pdf-sample-GLW.zip](ptx2pdf-sample-GLW.zip) - on <abbr class="updated" title="2011-05-17T19:28:42.086Z">May 17, 2011</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">1</span>)

