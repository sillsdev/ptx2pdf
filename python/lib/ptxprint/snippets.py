import re, os
import regex
from .texmodel import universalopen
from .ptsettings import bookcodes

class Snippet:
    regexes = []
    processTex = False
    texCode = ""
    takesDiglot = False

class PDFx1aOutput(Snippet):
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
/Type/OutputIntent
/S/GTS_PDFX
/OutputCondition (An Unknown print device)
/OutputConditionIdentifier (Custom)
/DestOutputProfile @OBJCVR
/RegistryName (http://www.color.og)
>> ] >>}}

"""
    
class FancyIntro(Snippet):
    texCode = r"""
\sethook{before}{ior}{\leaders\hbox to 0.8em{\hss.\hss}\hfill}

"""

class Diglot(Snippet):
    processTex = True
    texCode = r"""
\def\regularR{{"{diglot/fontregular}{diglot/docscript}{diglot/docdigitmapping}"}}
\def\boldR{{"{diglot/fontbold}{diglot/docdigitmapping}"}}
\def\italicR{{"{diglot/fontitalic}{diglot/docscript}{diglot/docdigitmapping}"}}
\def\bolditalicR{{"{diglot/fontbolditalic}{diglot/docscript}{diglot/docdigitmapping}"}}

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
\diglotSwap{document/diglotswapside}
\diglotLtrue
\catcode `@=12

"""

class FancyBorders(Snippet):
    processTex = True
    takesDiglot = True
    def generateTex(self, texmodel, diglotSide=""):
        res = r"""
% Define this to add a border to all pages, from a PDF file containing the graphic
%   "scaled <factor>" adjusts the size (1000 would keep the border at its original size)
% Can also use "xscaled 850 yscaled 950" to scale separately in each direction,
%   or "width 5.5in height 8in" to scale to a known size
{fancy/pageborder}{fancy/pageborderfullpage}\def\PageBorder{{"{fancy/pageborderpdf}" width {paper/width} height {paper/height}}}
{fancy/pageborder}{fancy/pagebordernfullpage_}\def\PageBorder{{"{fancy/pageborderpdf}" width {paper/pagegutter} height {paper/height}}}

{fancy/endofbook}\newbox\decorationbox
{fancy/endofbook}\setbox\decorationbox=\hbox{{\XeTeXpdffile "{fancy/endofbookpdf}"\relax}}
{fancy/endofbook}\def\z{{\par\nobreak\vskip 16pt\centerline{{\copy\decorationbox}}}}

"""
        if texmodel.dict.get("_isDiglot", False):
            repeats = [("L", ""), ("R", "diglot")]
        else:
            repeats = [("", "")]
        for replaceD, replaceE in repeats:
            res += r"""
{%E%fancy/sectionheader}\newbox\sectionheadbox%D%
{%E%fancy/sectionheader}\def\placesectionheadbox%D%{{%
{%E%fancy/sectionheader}  \ifvoid\sectionheadbox%D% % set up the \sectionheadbox box the first time it's needed
{%E%fancy/sectionheader}    \global\setbox\sectionheadbox%D%=\hbox to \hsize{{\hss \XeTeXpdffile "{%E%fancy/sectionheaderpdf}" scaled {%E%fancy/sectionheaderscale} \relax\hss}}%
{%E%fancy/sectionheader}    \global\setbox\sectionheadbox%D%=\vbox to 0pt
{%E%fancy/sectionheader}        {{\kern-\ht\sectionheadbox%D% \kern {%E%fancy/sectionheadershift}pt \box\sectionheadbox \vss}}
{%E%fancy/sectionheader}  \fi
{%E%fancy/sectionheader}  \vadjust{{\copy\sectionheadbox}}%
{%E%fancy/sectionheader}}}
{%E%fancy/sectionheader}\sethook{{start}}{{s%D%}}{{\placesectionheadbox}}
{%E%fancy/sectionheader}\sethook{{start}}{{s1%D%}}{{\placesectionheadbox}}
{%E%fancy/sectionheader}\sethook{{start}}{{s2%D%}}{{\placesectionheadbox}}

{%E%fancy/versedecorator}\newbox\versestarbox%D%
{%E%fancy/versedecorator}\setbox\versestarbox%D%=\hbox{{\XeTeXpdffile "{%E%fancy/versedecoratorpdf}" scaled {%E%fancy/versedecoratorscale} \relax}}
{%E%fancy/versedecorator}\def\AdornVerseNumber%D%#1{{\beginL\rlap{{\hbox to \wd\versestarbox%D%{{\hfil #1\hfil}}}}%
{%E%fancy/versedecorator}    \raise {%E%fancy/versedecoratorshift}pt\copy\versestarbox%D%\endL}}
""".replace("%D%", replaceD).replace("%E%", replaceE)
        return res.format(**texmodel.dict)

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

def parsecol(s):
    vals = s[s.find("(")+1:-1].split(",")
    return " ".join("{:.3f}".format(float(v)/255) for v in vals)

class ThumbTabs(Snippet):
    def generateTex(self, model):
        numtabs = int(float(model["thumbtabs/numtabs"]))
        texlines = ["\\NumTabs={}".format(numtabs)]

        # Analyse grouped tabs
        groups = model["thumbtabs/groups"].split(";")
        allgroupbks = {}
        grouplists = []
        for i, g in enumerate(groups):
            a = g.strip().split()
            grouplists.append(a)
            for b in a:
                allgroupbks[b] = i
        groups = [g.strip().split() for g in groups]

        # calculate book index
        restartmat = model["thumbtabs/restart"]
        books = {}
        start = 1
        for b in model.printer.getBooks(scope="multiple"):
            c = bookcodes.get(b, "C0")
            if c[0] not in "0123456789" or int(c) > 85:
                continue
            bkdone = False
            if b in allgroupbks:
                for a in grouplists[allgroupbks[b]]:
                    if a in books:
                        index = books[a]
                        bkdone = True
                        break
            if not bkdone:
                if start > numtabs or (b == "MAT" and restartmat):
                    start = 1
                index = start
                start += 1
            books[b] = index
            texlines.append(f"\\setthumbtab{{{b}}}{{{index}}}")
        bcol = parsecol(model["thumbtabs/background"])
        texlines.append("\\def\\tabBoxCol{{{}}}".format(bcol))
        try:
            height = float(model["thumbtabs/height"])
        except (ValueError, TypeError):
            height = 8.

        try:
            width = float(model["thumbtabs/length"])
        except (ValueError, TypeError):
            width = 15.
        rotate = model["thumbtabs/rotate"]
        texlines.append("\\TabAutoRotatefalse")
        texlines.append("\\TabRotationNormal{}".format("false" if rotate else "true"))
        if rotate:
            rottype = int(model["thumbtabs/rotatetype"]) - 1
            texlines.append("\\TabTopToEdgeOdd{}".format("true" if rottype & 1 else "false"))
            texlines.append("\\TabTopToEdgeEven{}".format("true" if 0 < rottype < 3 else "false"))
        texlines.append("\\tab{}={:.2f}mm".format("width" if rotate else "height", height))
        texlines.append("\\tab{}={:.2f}mm".format("height" if rotate else "width", width))
        return "\n".join(texlines)+"\n"

class Colophon(Snippet):
    processTex = True
    texCode = """
\\catcode"FDEE=1 \\catcode"FDEF=2
\\prepusfm
\\def\\zcolophon\uFDEE
\\esb\\cat colophon\\cat*
\\bigskip
{project/colophontext}
\\esbe \uFDEF
\\unprepusfm

"""
