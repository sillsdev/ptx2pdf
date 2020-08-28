import regex
from .texmodel import universalopen

class PDFx1aOutput():
    regexes = []
    styleInfo = ""
    processTex = True
    texCode = r"""
\special{{pdf:docinfo<<
/Title({document/title})%
/Subject({document/subject})%
/Author({document/author})%
/Creator(PTXprint ({config/name}))%
/CreationDate(D:{pdfdate_})%
/ModDate(D:{pdfdate_})%
/Producer(XeTeX)%
/Trapped /False
/GTS_PDFXVersion(PDF/X-1:2001)%
/GTS_PDFXConformance(PDF/X-1a:2001)%
>> }} 
\special{{pdf:fstream @OBJCVR ({/iccfpath})}}
\special{{pdf:put @OBJCVR <</N 4>>}}
%\special{{pdf:close @OBJCVR}}
\special{{pdf:docview <<
/OutputIntents [ <<
/Type/OutputIndent
/S/GTS_PDFX
/OutputCondition (An Unknown print device)
/OutputConditionIdentifier (Custom)
/DestOutputProfile @OBJCVR
/RegistryName (http://www.color.og)
>> ] >>}} 
    """
    
class FancyIntro():
    _regexbits = [(r'\\io2 ', r'\\io1 \u00A0\u00A0\u00A0\u00A0\u00A0\u00A0'), # Temporary fix for \io2 and \io3 so table doesn't break!
               (r'\\io3 ', r'\\io1 \u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0'),
               (r'(\\iot .+?)\r?\n', r'\1\r\n\iotable\r\n\makedigitsother\r\n\catcode`{=1\r\n\catcode`}=2\r\n'),
               (r'\\io1 ', r'\iotableleader{'),
               (r' \\ior ', r'}{'),
               (r' ?\\ior\*', r'}'),
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

    processTex = False
    texCode = r"""
% Enable commands with digits in them to be processed
\catcode`@=11
\def\makedigitsother{\m@kedigitsother}
\def\makedigitsletters{\m@kedigitsletters}
\catcode `@=12
\def\iotableleader#1#2{#1\leaders\hbox to 0.8em{\hss.\hss}\hfill#2\par}%
"""

class Diglot():
    regexes = []
    styleInfo = ""
    processTex = True
    texCode = r"""
\def\regularR{{"{diglot/fontregular}{diglot/fontregeng}{diglot/texfeatures}{diglot/docscript}{diglot/docdigitmapping}"}}
\def\boldR{{"{diglot/fontbold}{diglot/fontboldeng}{diglot/texfeatures}{diglot/docscript}{diglot/docdigitmapping}{diglot/boldembolden}{diglot/boldslant}"}}
\def\italicR{{"{diglot/fontitalic}{diglot/fontitaleng}{diglot/texfeatures}{diglot/docscript}{diglot/docdigitmapping}{diglot/italembolden}{diglot/italslant}"}}
\def\bolditalicR{{"{diglot/fontbolditalic}{diglot/fontbolditaleng}{diglot/texfeatures}{diglot/docscript}{diglot/docdigitmapping}{diglot/bolditalembolden}{diglot/boldital/slant}"}}

\def\DiglotLeftFraction{{{document/diglotprifraction}}}
\def\DiglotRightFraction{{{document/diglotsecfraction}}}

{diglot/colorfonts}\ColorFontsfalse
%\addToLeftHooks{{\FontSizeUnit={paper/fontfactor}pt}}
%\addToRightHooks{{\FontSizeUnit={diglot/fontfactor}pt}}
\FontSizeUnitR={diglot/fontfactor}pt
\def\LineSpacingFactorR{{{diglot/linespacingfactor}}}
\addToLeftHooks{{\RTL{document/ifrtl}}}
\addToRightHooks{{\RTL{diglot/ifrtl}}}
%{diglot/iflinebreakon}\XeTeXlinebreaklocaleR "{diglot/linebreaklocale}"
%{diglot/useglyphmetrics}\XeTeXuseglyphmetricsR=0
\diglotLtrue
\catcode `@=12

"""

class FancyBorders():
    regexes = []
    styleInfo = lambda m: (r"""
# need a smaller verse number to fit in the stars
\Marker v
\FontSize {fancy/versenumsize}
""".format(**m.dict) if m['fancy/versedecorator'] != "%" else "") + (r"""
\Marker s
\FontSize 10
\SpaceAfter 2
\LeftMargin .3
\RightMargin .3
""" if m['fancy/sectionheader'] != "%" else "") + r"""
# \Marker p
# \FontSize 12

# \Marker mt2
# \Regular

# \Marker iref
# \Endmarker iref*
# \Name (iref...iref*) Introduction reference
# \OccursUnder ip
# \TextType Other
# \TextProperties paragraph publishable vernacular
# \StyleType Character
# \FontSize 12

# footnotes will use the 'fcaller' style for the caller, smaller text
# \Marker f
# \CallerStyle fcaller
# \FontSize 9

# footnote caller is superscript (even though verse numbers are not)
# \Marker fcaller
# \Endmarker fcaller*
# \StyleType character
# \Superscript
# \FontSize 11

# \Marker fr
# \FontSize 9
# \Regular

# \Marker fk
# \Endmarker fk*
# \FontSize 9
# \Regular
# \Bold

# \Marker ft
# \FontSize 9
"""

    processTex = True
    texCode = r"""
% Define this to add a border to all pages, from a PDF file containing the graphic
%   "scaled <factor>" adjusts the size (1000 would keep the border at its original size)
% Can also use "xscaled 850 yscaled 950" to scale separately in each direction,
%   or "width 5.5in height 8in" to scale to a known size
{fancy/pageborder}\def\PageBorder{{"{fancy/pageborderpdf}" width {paper/width} height {paper/height}}}

{fancy/endofbook}\newbox\decorationbox
{fancy/endofbook}\setbox\decorationbox=\hbox{{\XeTeXpdffile "{fancy/endofbookpdf}"\relax}}
{fancy/endofbook}\def\z{{\par\nobreak\vskip 16pt\centerline{{\copy\decorationbox}}}}

{fancy/sectionheader}\newbox\sectionheadbox
{fancy/sectionheader}\def\placesectionheadbox{{%
{fancy/sectionheader}  \ifvoid\sectionheadbox % set up the \sectionheadbox box the first time it's needed
{fancy/sectionheader}    \global\setbox\sectionheadbox=\hbox{{\XeTeXpdffile "{fancy/sectionheaderpdf}"\relax}}%
{fancy/sectionheader}    \global\setbox\sectionheadbox=\hbox to \hsize% \hsize is the line width
{fancy/sectionheader}        {{\hss \box\sectionheadbox \hss}}% so now the graphic will be centered
{fancy/sectionheader}    \global\setbox\sectionheadbox=\vbox to 0pt
{fancy/sectionheader}        {{\kern-21pt % adjust value of \kern here to shift graphic up or down
{fancy/sectionheader}         \box\sectionheadbox \vss}}% now we have a box with zero height
{fancy/sectionheader}  \fi
{fancy/sectionheader}  \vadjust{{\copy\sectionheadbox}}% insert the graphic below the current line
{fancy/sectionheader}  \vrule width 0pt height 0pt depth 0.5em
{fancy/sectionheader}}}
{fancy/sectionheader}\sethook{{start}}{{s}}{{\placesectionheadbox}}

% The following code puts the verse number inside a star
%
{fancy/versedecorator}\newbox\versestarbox
{fancy/versedecorator}\setbox\versestarbox=\hbox{{\XeTeXpdffile "{fancy/versedecoratorpdf}"\relax}}

% capture the verse number in a box (surrounded by \hfil) which we overlap with star
{fancy/versedecorator}\newbox\versenumberbox
{fancy/versedecorator}\sethook{{start}}{{v}}{{\setbox\versenumberbox=\hbox to \wd\versestarbox\bgroup\hfil}}
{fancy/versedecorator}\sethook{{end}}{{v}}{{\hfil\egroup
{fancy/versedecorator} \beginL % ensure TeX is "thinking" left-to-right for the \rlap etc
{fancy/versedecorator}   \rlap{{\raise1pt\box\versenumberbox}}\lower4pt\copy\versestarbox
{fancy/versedecorator} \endL}}

% Replace the ptx2pdf macro which prints out the verse number, so that we can
% kern between numbers or change the font size, if necessary
{fancy/versedecorator}\catcode`\@=11   % allow @ to be used in the name of ptx2pdf macro we have to override
{fancy/versedecorator}\def\printv@rse{{\expandafter\getversedigits\v@rsefrom!!\end\printversedigits}}
{fancy/versedecorator}\catcode`\@=12   % return to normal function

{fancy/versedecorator}\def\getversedigits#1#2#3#4\end{{\def\digitone{{#1}}\def\digittwo{{#2}}\def\digitthree{{#3}}}}

{fancy/versedecorator}\font\smallversenums="{versenumfont}" at {fancy/versenumsize}pt
{fancy/versedecorator}\def\exclam{{!}}
{fancy/versedecorator}\def\printversedigits{{%
{fancy/versedecorator}  \beginL
{fancy/versedecorator}  \ifx\digitthree\exclam
{fancy/versedecorator}    \digitone
{fancy/versedecorator}    \ifx\digittwo\exclam\else
{fancy/versedecorator}      \ifnum\digitone=1\kern-0.1em
{fancy/versedecorator}      \else\kern-0.05em\fi
{fancy/versedecorator}      \digittwo
{fancy/versedecorator}    \fi
{fancy/versedecorator}  \else
{fancy/versedecorator}    \smallversenums
{fancy/versedecorator}    \digitone
{fancy/versedecorator}    \kern-0.12em \digittwo
{fancy/versedecorator}    \kern-0.08em \digitthree
{fancy/versedecorator}  \fi
{fancy/versedecorator}  \endL}}
"""

    unusedStuff = r"""
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
    \kern-0.1em \digittwo      % digit one will always be '1' in 3-digit chap nums
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

class ImgCredits():
    regexes = None
    styleInfo = None
    processTex = False
    texCode = ""

def generateCredits(picpagesFile, sensitive=False):
    with universalopen(picpagesFile) as inf:
        dat = inf.read()

    artpgs = {}
    m = re.findall(r"\\figonpage\{(\d+)\}\{\d+\}\{.*?((?=ab|cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib)..)\d{5}.+?", dat)
    if len(m):
        for f in m:
            artpgs.setdefault(f[1], []).append(int(f[0]))

    artstr = {
    "cn" : ("© 1996 David C. Cook.", "© DCC."),
    "co" : ("© 1996 David C. Cook.", "© DCC."),
    "hk" : ("by Horace Knowles\n© The British & Foreign Bible Society, 1954, 1967, 1972, 1995.", "© BFBS, 1995."),
    "lb" : ("by Louise Bass\n© The British & Foreign Bible Society, 1994.", "© BFBS, 1994."),
    "bk" : ("by Horace Knowles revised by Louise Bass\n©The British & Foreign Bible Society, 1994.", "© BFBS, 1994."),
    "ba" : ("used by permission of Louise Bass.", ""),
    "dy" : ("by Carolyn Dyk, © 2001 Wycliffe Bible Translators, Inc.\nand licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.", ""),
    "gt" : ("by Gordon Thompson © 2012 Wycliffe Bible Translators Inc.\nand licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 3.0 Australia License.", ""),
    "dh" : ("by David Healey © 2012 Wycliffe Bible Translators Inc.\nand licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 3.0 Australia License.", ""),
    "mh" : ("by Michael Harrar © 2012 Wycliffe Bible Translators Inc.\nand licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 3.0 Australia License.", ""),
    "mn" : ("used by permission of Muze Tshilombo.", ""),
    "wa" : ("by Graham Wade, © United Bible Societies, 1989.", ""),
    "dn" : ("by Darwin Dunham, © United Bible Societies, 1989.", ""),
    "ib" : ("Illustrations by Farid Faadil. Copyright © by Biblica, Inc.\nUsed by permission. All rights reserved worldwide.", "")
    }
    crdts = []
    for art, pgs in artpgs.items():
        if len(pgs):
            pgs = sorted(set(pgs))
            if len(pgs) == 1:
                pl = ""
                pgstr = "on page {} ".format(str(pgs[0]))
            else:
                pl = "s"
                pgstr = "on pages {} and {} ".format(", ".join(str(p) for p in pgs[:-1]), str(pgs[-1]))
            
            if art in artstr.keys():
                if sensitive and len(artstr[art][1]):
                    cpystr = artstr[art][1]
                else:
                    cpystr = artstr[art][0]
                crdts += ["\\pc Illustration{} {}{}\n".format(pl, pgstr, cpystr)]
            else:
                crdts += ["\\rem Warning: No copyright statement found for: {} image{} {}\n".format(art.upper(), pl, pgstr)]
    return "\n".join(crdts) if len(crdts) else ""
