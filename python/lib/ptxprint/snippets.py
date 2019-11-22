import regex

class FancyIntro():
    _regexbits = [(r'\\io2 ', r'\\io1 \u00A0\u00A0\u00A0\u00A0\u00A0\u00A0'), # Temporary fix for \io2 and \io3 so table doesn't break!
               (r'\\io3 ', r'\\io1 \u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0'),
               (r'(\\iot .+?)\r?\n', r'\1\r\n\iotable\r\n\makedigitsother\r\n\catcode`{=1\r\n\catcode`}=2\r\n'),
               (r'\\io1 ', r'\iotableleader{'),
               (r' \\ior ', r'}{'),
               (r' \\ior\*', r'}'),
               (r'\\c 1\r?\n', r'\catcode`{=11 \catcode`}=11\r\n\makedigitsletters\r\n\c 1\r\n')] # Assumes no markers between last \io1 line & \c 1
    regexes = [(None, regex.compile(r[0], flags=regex.S), r[1]) for r in _regexbits]

    styleInfo = r"""
\Marker iotable
\Name iotable - Introduction - Outline Table
\Description Introduction outline text in a table format
\OccursUnder id
\Rank 6
\TextType Other
\TextProperties paragraph publishable vernacular level_1
\StyleType paragraph
\FontSize 12
\LeftMargin 0
\RightMargin .5
\FirstLineIndent .5
"""
# Indent is in inches

    texCode = r"""
% Enable commands with digits in them to be processed
\catcode`@=11
\def\makedigitsother{\m@kedigitsother}
\def\makedigitsletters{\m@kedigitsletters}
\catcode `@=12
\def\iotableleader#1#2{#1\leaders\hbox to 0.8em{\hss.\hss}\hfill#2\par}%
"""

class FancyBorders(): # Not sure how much of this is needed (perhaps it can be cut down to the basics)
    regexes = []
    styleInfo = r"""
# need a smaller verse number to fit in the stars
\Marker v
\FontSize 8

\Marker s
\FontSize 10
\SpaceAfter 2
\LeftMargin .3
\RightMargin .3
# DLR changed LeftMargin and RightMargin from .25 to .3 to avoid long section title from hitting border.

\Marker p
\FontSize 12

\Marker mt2
\Regular

\Marker iref
\Endmarker iref*
\Name (iref...iref*) Introduction reference
\OccursUnder ip
\TextType Other
\TextProperties paragraph publishable vernacular
\StyleType Character
\FontSize 12

# footnotes will use the 'fcaller' style for the caller, smaller text
\Marker f
\CallerStyle fcaller
\FontSize 9

# footnote caller is superscript (even though verse numbers are not)
\Marker fcaller
\Endmarker fcaller*
\StyleType character
\Superscript
\FontSize 11

\Marker fr
\FontSize 9
\Regular

\Marker fk
\Endmarker fk*
\FontSize 9
\Regular
\Bold

\Marker ft
\FontSize 9
"""

# For this to work at all, we need a way to dynamically insert (user-customizable) PDF files 
# into the code below or at least point to these ones with a relative path that is reliable.
# decoration.pdf
# A5 section head border.pdf
# Verse number star.pdf

    texCode = r"""
\TitleColumns=1
\IntroColumns=1
\BodyColumns=1

% Define this to add a border to all pages, from a PDF file containing the graphic
%   "scaled <factor>" adjusts the size (1000 would keep the border at its original size)
% Can also use "xscaled 850 yscaled 950" to scale separately in each direction,
%   or "width 5.5in height 8in" to scale to a known size
\def\PageBorder{"A5 page border.pdf" width 148.5mm height 210mm}
%\def\PageBorder{}

\newbox\decorationbox
\setbox\decorationbox=\hbox{\XeTeXpdffile "decoration.pdf"\relax}
\def\z{\par\nobreak\vskip 16pt\centerline{\copy\decorationbox}}

\newbox\sectionheadbox
\def\placesectionheadbox{%
  \ifvoid\sectionheadbox % set up the \sectionheadbox box the first time it's needed
    \global\setbox\sectionheadbox=\hbox{\XeTeXpdffile "A5 section head border.pdf" \relax}%
    \global\setbox\sectionheadbox=\hbox to \hsize% \hsize is the line width
        {\hss \box\sectionheadbox \hss}% so now the graphic will be centered
    \global\setbox\sectionheadbox=\vbox to 0pt
        {\kern-21pt % adjust value of \kern here to shift graphic up or down
         \box\sectionheadbox \vss}% now we have a box with zero height
  \fi
  \vadjust{\copy\sectionheadbox}% insert the graphic below the current line
  \vrule width 0pt height 0pt depth 0.5em
}

\sethook{start}{s}{\placesectionheadbox}


%
% The following code puts the verse number inside a star
%
\newbox\versestarbox
\setbox\versestarbox=\hbox{\XeTeXpdffile "Verse number star.pdf"\relax}

% capture the verse number in a box (surrounded by \hfil) which we overlap with star
\newbox\versenumberbox
\sethook{start}{v}{\setbox\versenumberbox=\hbox to \wd\versestarbox\bgroup\hfil}
\sethook{end}{v}{\hfil\egroup
 \beginL % ensure TeX is "thinking" left-to-right for the \rlap etc
   \rlap{\raise1pt\box\versenumberbox}\lower4pt\copy\versestarbox
 \endL}

% Replace the ptx2pdf macro which prints out the verse number, so that we can
% kern between numbers or change the font size, if necessary
\catcode`\@=11   % allow @ to be used in the name of ptx2pdf macro we have to override
\def\printv@rse{\expandafter\getversedigits\v@rsefrom!!\end\printversedigits}
\catcode`\@=12   % return to normal function

\def\getversedigits#1#2#3#4\end{\def\digitone{#1}\def\digittwo{#2}\def\digitthree{#3}}

\font\smallversenums="Charis SIL" at 7pt
\def\exclam{!}
\def\printversedigits{%
  \beginL
  \ifx\digitthree\exclam
    \digitone
    \ifx\digittwo\exclam\else
      \ifnum\digitone=1\kern-0.1em
      \else\kern-0.05em\fi
      \digittwo
    \fi
  \else
    \smallversenums
    \digitone
    \kern-0.12em \digittwo
    \kern-0.08em \digitthree
  \fi
  \endL}

% Some code to allow us to kern chapter numbers
\def\PrepChapterNumber{\expandafter\getchapdigits\printchapter!!\end \def\printchapter{\printchapdigits}}

\def\getchapdigits#1#2#3#4\end{\def\digitone{#1}\def\digittwo{#2}\def\digitthree{#3}}

\def\exclam{!}
\def\printchapdigits {%
  \beginL
  \ifx\digitthree\exclam
    \digitone
    \ifx\digittwo\exclam\else
      \ifnum\digitone=1\kern-0.1em\fi
      \digittwo
    \fi
  \else
    \digitone
    \kern-0.1em \digittwo	% digit one will always be '1' in 3-digit chap nums
    \kern-0.05em \digitthree
  \fi
  \endL}

% Define the \b tag
%\def\b{\par\vskip\baselineskip}
\def\b{\par\vskip 10pt}

% Make sure that \q2 lines are not separated from their previous \q1 lines
% (Individual quote lines should probably use \q, but may use \q1 at times)
\sethook{before}{q2}{\nobreak}

% This seems to help prevent footnotes from breaking across pages
\interfootnotelinepenalty=10000

% don't allow line breaks at explicit hyphens
\exhyphenpenalty=10000

\catcode`\?=\active % make question mark an active character
\def?{\unskip    % remove preceding glue (space)
     \kern0.2em  % generate a non-breaking space
     \char`\?{}}% print the question mark; extra {} is so TeX won't absorb the following space

\catcode`\!=\active \def!{\unskip\kern0.2em\char`\!{}} % exclamation
% \catcode`\:=\active \def:{\unskip\kern0.2em\char`\:{}} % colon
\catcode`\;=\active \def;{\unskip\kern0.2em\char`\;{}} % semicolon
\catcode`\”=\active \def”{\unskip\kern0.2em\char`\”{}} % closing quote
\catcode`\»=\active \def»{\unskip\kern0.2em\char`\»{}} % closing guillemet

% non-breaking space on both sides of double quote
%\catcode`\"=\active \def"{\unskip\kern0.2em \char`\"\kern0.2em\ignorespaces}

\catcode`\“=\active % make opening quote active
\def“{\char`\“% print the opening quote
     \kern0.2em % generate a non-breaking space
     \ignorespaces} % and ignore any following space in the text
\catcode`\«=\active \def«{\char`\«\kern0.2em\ignorespaces} % opening guillemet

% Make colon definition inactive in \fr, because we don't want preceding space
\sethook{start}{fr}{\catcode`\:=12}
\sethook{end}{fr}{\catcode`\:=\active}
% Also inside the \iref and \gref markers
\sethook{start}{iref}{\catcode`\:=12}
\sethook{end}{iref}{\catcode`\:=\active}
\sethook{start}{gref}{\catcode`\:=12}
\sethook{end}{gref}{\catcode`\:=\active}
"""
