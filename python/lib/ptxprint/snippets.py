import re, os
import regex
from .texmodel import universalopen
from .ptsettings import bookcodes
from .utils import pycodedir, htmlprotect, saferelpath

class Snippet:
    order = 0
    regexes = []
    processTex = False
    texCode = ""
    takesDiglot = False

class PDFx1aOutput(Snippet):

    def generateTex(self, model, diglotSide=""):
        docdir,docdirbase=model.docdir()
        res = r"""
\bgroup
\catcode`\#=12 
\catcode`\@=11 \catcode`\^^M=10 \activ@tecustomch@rs\deactiv@tecustomch@rs
\special{{pdf:docinfo<<
/Title({document/title})%
/Subject({document/subject})%
/Author({document/author})%
/Creator(PTXprint {/ptxprint_gitversion} ({config/name}))%
/CreationDate(D:{pdfdate_})%
/ModDate(D:{pdfdate_})%
/Producer(XeTeX)%
/Trapped /False
{_gtspdfx}>> }}
\message{{snippet 1}}%
\special{{pdf:fstream @OBJCVR ({/iccfpath})}}
\special{{pdf:put @OBJCVR <</N {_iccnumcols}>>}}
%\special{{pdf:close @OBJCVR}}
\special{{pdf:stream @OBJCMR (
<x:xmpmeta xmlns:x="adobe:ns:meta/">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-ref-syntax-ns#"
       xmlns:xmp="http://ns.adobe.com/xap/1.0/"
       xmlns:dc="http://purl.org/dc/elements/1.1/"
       xmlns:pdf="http://ns.adobe.com/pdf/1.3/"
       xmlns:pdfaid="http://www.aiim.org/pdfa/ns/id/"
       xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/"
       xmlns:pdfxid="http://www.npes.org/pdfx/ns/id/">
      <rdf:Description rdf:about="" xmlns:pdfaExtension="http://www.aiim.org/pdfa/ns/extension/" xmlns:pdfaSchema="http://www.aiim.org/pdfa/ns/schema#" xmlns:pdfaProperty="http://www.aiim.org/pdfa/ns/property#">
        <pdfaExtension:schemas>
          <rdf:Bag>
            <rdf:li rdf:parseType="Resource">
              <pdfaSchema:namespaceURI>http://ns.adobe.com/pdf/1.3/</pdfaSchema:namespaceURI>
              <pdfaSchema:prefix>pdf</pdfaSchema:prefix>
              <pdfaSchema:schema>Adobe PDF Schema</pdfaSchema:schema>
              <pdfaSchema:property>
                <rdf:Seq>
                  <rdf:li rdf:parseType="Resource">
                    <pdfaProperty:category>internal</pdfaProperty:category>
                    <pdfaProperty:description>Trapped property</pdfaProperty:description>
                    <pdfaProperty:name>Trapped</pdfaProperty:name>
                    <pdfaProperty:valueType>Boolean</pdfaProperty:valueType>
                  </rdf:li>
                </rdf:Seq>
              </pdfaSchema:property>
            </rdf:li>
            <rdf:li rdf:parseType="Resource">
              <pdfaSchema:namespaceURI>http://ns.adobe.com/xap/1.0/mm/</pdfaSchema:namespaceURI>
              <pdfaSchema:prefix>xmpMM</pdfaSchema:prefix>
              <pdfaSchema:schema>XMP Media Management Schema</pdfaSchema:schema>
              <pdfaSchema:property>
                <rdf:Seq>
                  <rdf:li rdf:parseType="Resource">
                    <pdfaProperty:category>internal</pdfaProperty:category>
                    <pdfaProperty:description>UUID based identifier for specific incarnation of a document</pdfaProperty:description>
                    <pdfaProperty:name>InstanceID</pdfaProperty:name>
                    <pdfaProperty:valueType>URI</pdfaProperty:valueType>
                  </rdf:li>
                </rdf:Seq>
              </pdfaSchema:property>
            </rdf:li>
            <rdf:li rdf:parseType="Resource">
              <pdfaSchema:namespaceURI>http://www.aiim.org/pdfa/ns/id/</pdfaSchema:namespaceURI>
              <pdfaSchema:prefix>pdfaid</pdfaSchema:prefix>
              <pdfaSchema:schema>PDF/A ID Schema</pdfaSchema:schema>
              <pdfaSchema:property>
                <rdf:Seq>
                  <rdf:li rdf:parseType="Resource">
                    <pdfaProperty:category>internal</pdfaProperty:category>
                    <pdfaProperty:description>Part of PDF/A standard</pdfaProperty:description>
                    <pdfaProperty:name>part</pdfaProperty:name>
                    <pdfaProperty:valueType>Integer</pdfaProperty:valueType>
                  </rdf:li>
                  <rdf:li rdf:parseType="Resource">
                    <pdfaProperty:category>internal</pdfaProperty:category>
                    <pdfaProperty:description>Amendment of PDF/A standard</pdfaProperty:description>
                    <pdfaProperty:name>amd</pdfaProperty:name>
                    <pdfaProperty:valueType>Text</pdfaProperty:valueType>
                  </rdf:li>
                  <rdf:li rdf:parseType="Resource">
                    <pdfaProperty:category>internal</pdfaProperty:category>
                    <pdfaProperty:description>Conformance level of PDF/A standard</pdfaProperty:description>
                    <pdfaProperty:name>conformance</pdfaProperty:name>
                    <pdfaProperty:valueType>Text</pdfaProperty:valueType>
                  </rdf:li>
                  <rdf:li rdf:parseType="Resource">
                    <pdfaProperty:category>internal</pdfaProperty:category>
                    <pdfaProperty:description>PDF/X version</pdfaProperty:description>
                    <pdfaProperty:name>GTS_PDFXVersion</pdfaProperty:name>
                    <pdfaProperty:valueType>Text</pdfaProperty:valueType>
                  </rdf:li>
                </rdf:Seq>
              </pdfaSchema:property>
            </rdf:li>
          </rdf:Bag>
        </pdfaExtension:schemas>
      </rdf:Description>
      <rdf:Description rdf:about="">
        <dc:creator>
          <rdf:Seq>
            <rdf:li>{_gtfauthor}</rdf:li>
          </rdf:Seq>
        </dc:creator>
        <xmp:CreateDate>{xmpdate_}</xmp:CreateDate>
        <xmp:ModifyDate>{xmpdate_}</xmp:ModifyDate>
        <xmp:MetadataDate>{xmpdate_}</xmp:MetadataDate>
        <xmp:CreatorTool>PTXprint ({config/name})</xmp:CreatorTool>
        <xmpMM:DocumentID>uuid:5589311-bbc3-4ac7-9aaf-fc8ab4739b3c</xmpMM:DocumentID>
        <xmpMM:RenditionClass>default</xmpMM:RenditionClass>
        <xmpMM:VersionID>1</xmpMM:VersionID>
        <pdfxid:GTS_PDFXVersion>PDF/X-4</pdfxid:GTS_PDFXVersion>
        <dc:title>
          <rdf:Alt>
            <rdf:li xml:lang="x-default">{_gtftitle}</rdf:li>
          </rdf:Alt>
        </dc:title>
        <dc:description>
          <rdf:Alt>
            <rdf:li xml:lang="x-default">{_gtfsubject}</rdf:li>
          </rdf:Alt>
        </dc:description>
        <pdf:Producer>XeTeX</pdf:Producer>
        <pdf:Trapped>False</pdf:Trapped>
{_gtspdfaid}      </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>)}}
\special{{pdf:put @OBJCMR <</Type /Metadata /Subtype /XML>>}}
\special{{pdf:docview <<
/Metadata @OBJCMR{rtlview}
/OutputIntents [ <<
/Type/OutputIntent
/S/GTS_PDFX
/OutputCondition (An Unknown print device)
/OutputConditionIdentifier (Custom)
/Info (Boilerplate null output intent)
/DestOutputProfile @OBJCVR
/RegistryName (http://www.color.og)
>> <<
/Type/OutputIntent
/S/GTS_PDFA1
/OutputCondition (An Unknown print device)
/OutputConditionIdentifier (Custom)
/Info (Boilerplate null output intent)
/DestOutputProfile @OBJCVR
/RegistryName (http://www.color.og)
>> ]
>>}}
\egroup
\catcode`\#=6\catcode`\@=11 \activ@tecustomch@rs
"""
# /MarkInfo <</Marked /False>>

        extras = {'_gtspdfx': '', '_gtspdfaid': ''}
        pdftype = model['snippets/pdfoutput'] or "Screen"
        libpath = pycodedir()
        if pdftype in ("Screen", "Transparent", "Digital" ):
            extras['_gtspdfx'] = "/GTS_PDFXVersion(PDF/X-4)%\n"
        else:
            extras['_gtspdfx'] = "/GTS_PDFXVersion(PDF/X-1a:2003)%\n/GTS_PDFXConformance(PDF/X-1a:2003)%\n"
            res += "\\Actionsfalse\n"
        if pdftype in ("Screen", "Digital"):
            model.dict["/iccfpath"] = saferelpath(os.path.join(libpath, "sRGB.icc"),docdir).replace("\\","/")
            extras['_iccnumcols'] = "3"
        if pdftype == "Gray":
            model.dict['/iccfpath'] = saferelpath(os.path.join(libpath, "default_gray.icc"),docdir).replace("\\","/")
            extras['_iccnumcols'] = "1"
        else:
            extras['_iccnumcols'] = "4"
        extras['_gtspdfaid'] = "      <pdfaid:part>1</pdfaid:part>\n      <pdfaid:conformance>B</pdfaid:conformance>\n"
        extras['rtlview'] = " /ViewerPreferences <</Direction /R2L>>" if model['cover/rtlbookbinding'] == "true" else ""
        for a in ('author', 'title', 'subject'):
            extras['_gtf'+a] = htmlprotect(model.dict['document/'+a])
        if model['document/printarchive']:
            res += "\\XeTeXgenerateactualtext=1\n"
        return res.format(**{**model.dict, **extras}) + "\n"
    
class FancyIntro(Snippet):
    texCode = r"""
\sethook{before}{ior}{\leaders\hbox to 0.8em{\hss.\hss}\hfill}

"""

class Diglot(Snippet):
    processTex = True

# \diglotSwap{document/diglotswapside}
    def generateTex(self, model, diglotSide=""):
        baseCode = r"""
\def\DiglotLFraction{{{poly/fraction}}}
\addToSideHooks{{{s_}}}{{\RTL{document/ifrtl}}}
{notes/includefootnotes}\expandafter\def\csname f{s_}:properties\endcsname{{nonpublishable}}
{notes/includexrefs}\expandafter\def\csname x{s_}:properties\endcsname{{nonpublishable}}
\let\language{s_}=\langund
\should@xist{{}}{{f{s_}}}
\should@xist{{}}{{x{s_}}}
\catcode `@=12
\polyglotpages{{{document/diglotlayout}}}
\def\DiglotCaptions{{{diglotcaptions_}}}
"""
        persideCode = r"""
% Setup Diglot {s_}
{diglot[project/ifusecustomsty]}\stylesheet{s_}{{{diglot[/ptxpath]}/custom.sty}}
\stylesheet{s_}{{{diglot[/cfgrpath]}/ptxprint.sty}} % Right side (secondary) styles
{diglot[project/ifusemodssty]}\stylesheet{s_}{{{diglot[/cfgrpath]}/ptxprint-mods.sty}} % Right-side/Diglot Secondary stylesheet override settings
\def\Diglot{s_}Fraction{{{diglot[poly/fraction]}}}
\addToSideHooks{{{s_}}}{{\RTL{diglot[document/ifrtl]}}}
\def\regular{s_}{{"{diglot[document/fontregular]}{diglot[document/script]}"}}
\def\bold{s_}{{"{diglot[document/fontbold]}"}}
\def\italic{s_}{{"{diglot[document/fontitalic]}{diglot[document/script]}"}}
\def\bolditalic{s_}{{"{diglot[document/fontbolditalic]}{diglot[document/script]}"}}
\FontSizeUnit{s_}={diglot[paper/fontfactor]}pt
%\RTL{s_}{diglot[document/ifrtl]}
\def\LineSpacingFactor{s_}{{{diglot[paragraph/linespacingfactor]}}}
\def\AfterChapterSpaceFactor{s_}{{{diglot[texpert/afterchapterspace]}}}
\def\AfterVerseSpaceFactor{s_}{{{diglot[texpert/afterversespace]}}}
\IndentUnit{s_}={diglot[document/indentunit]}in
\newskip\intercharskip{s_} \intercharskip{s_}=0pt plus {diglot[document/letterstretch]:.4f}em minus {diglot[document/lettershrink]:.4f}em
\def\intercharspace{s_}{{\leavevmode\nobreak\hskip\intercharskip{s_}}}
\addToSideHooks{{{s_}}}{{\XeTeXinterchartokenstate={diglot[document/letterspace]}}}
{diglot[project/interlinear]}\expandafter\def\csname complex-rb\endcsname{{\ruby{diglot[project/ruby]}{{rb}}{{gloss}}}}
{diglot[document/ifdiglotcolour]}\SetDiglotBGColour{{{s_}}}{{{diglot[document/diglotcolour]}}}{{}}
{diglot[notes/includefootnotes]}\expandafter\def\csname f{s_}:properties\endcsname{{nonpublishable}}
{diglot[notes/includexrefs]}\expandafter\def\csname x{s_}:properties\endcsname{{nonpublishable}}
\makeatletter
\should@xist{{}}{{f{s_}}}
\should@xist{{}}{{x{s_}}}
\newlanguage\language{s_} \language\language{s_}
{diglot[paragraph/ifhavehyphenate]}{diglot[paragraph/ifhyphenate]}\bgroup\liter@lspecials\input "{diglot[/cfgrpath]}/hyphen-{diglot[project/id]}.tex" \egroup
\catcode"FDEE=1 \catcode"FDEF=2
\def\zcopyright{s_}﷮{diglot[project/copyright]}﷯
\def\zlicense{s_}﷮{diglot[project/license]}﷯
\makeatother
"""

        layout = model.dict["document/diglotlayout"]
        if not layout:
            layout = "L"+"".join(model.dict["diglots_"].keys())
            model.dict["document/diglotlayout"] = layout
        res = baseCode.format(s_="L", **model.dict)
        for k, v in model.dict["diglots_"].items():
            v.dict["isNotR_"] = "%" if k == "R" else ""
            res += persideCode.format(diglot=v.dict, s_=k, **model.dict)
        # res += "\n" + r"\def\addInt{" + "\n"
        # for a in (("L", "project/intfile"), ("R", "diglot/intfile")):
            # res += r"\zglot|{0}\*{1}".format(a[0], model.dict[a[1]]) + "\n"
        # res += r"\zglot|\*}" + "\n"
        return res

class FancyBorders(Snippet):
    takesDiglot = True
    def generateTex(self, texmodel, diglotSide=""):
        res = r"""
% Define this to add a border to all pages, from a PDF file containing the graphic
%   "scaled <factor>" adjusts the size (1000 would keep the border at its original size)
% Can also use "xscaled 850 yscaled 950" to scale separately in each direction,
%   or "width 5.5in height 8in" to scale to a known size
{fancy/pageborders}{fancy/pageborder}{fancy/pageborderfullpage}\def\PageBorder{{"{fancy/pageborderpdf}" width {paper/width} height {paper/height}}}
{fancy/pageborders}{fancy/pageborder}{fancy/pagebordernfullpage_}\def\PageBorder{{"{fancy/pageborderpdf}" width {paper/pagegutter} height {paper/height}}}

{fancy/endofbook}\newbox\decorationbox
{fancy/endofbook}\setbox\decorationbox=\hbox{{\XeTeXpdffile "{fancy/endofbookpdf}"\relax}}
{fancy/endofbook}\def\zBookEndDecoration{{\par\nobreak\vbox{{\kern \BookEndDecorationSkip\centerline{{\copy\decorationbox}}}}}}
{fancy/endofbook}\def\zautoBookEndDecoration{{\iffilehasverses \zBookEndDecoration\fi}}


"""
        if texmodel.dict.get("_isDiglot", False):
            repeats = [("L", texmodel)] + list(texmodel.dict["diglots_"].items())
        else:
            repeats = [("", texmodel)]
        for k, v in repeats:
            res += r"""
{fancy/sectionheader}\newbox\sectionheadbox%D%
{fancy/sectionheader}\def\placesectionheadbox%D%{{%
{fancy/sectionheader}  \ifvoid\sectionheadbox%D% % set up the \sectionheadbox box the first time it's needed
{fancy/sectionheader}    \global\setbox\sectionheadbox%D%=\hbox to \hsize{{\hss \XeTeXpdffile "{fancy/sectionheaderpdf}" scaled {fancy/sectionheaderscale} \relax\hss}}%
{fancy/sectionheader}    \global\setbox\sectionheadbox%D%=\vbox to 0pt
{fancy/sectionheader}        {{\kern-\ht\sectionheadbox%D% \kern {fancy/sectionheadershift}pt \box\sectionheadbox \vss}}
{fancy/sectionheader}  \fi
{fancy/sectionheader}  \vadjust{{\copy\sectionheadbox}}%
{fancy/sectionheader}}}
{fancy/sectionheader}\sethook{{start}}{{s%D%}}{{\placesectionheadbox}}
{fancy/sectionheader}\sethook{{start}}{{s1%D%}}{{\placesectionheadbox}}
{fancy/sectionheader}\sethook{{start}}{{s2%D%}}{{\placesectionheadbox}}
{fancy/sectionheader}\squashgridboxfalse

{fancy/versedecoratorisfile}\newbox\versestarbox%D%
{fancy/versedecoratorisfile}\setbox\versestarbox%D%=\hbox{{\XeTeXpdffile "{fancy/versedecoratorpdf}" scaled {fancy/versedecoratorscale} \relax}}
{fancy/versedecoratorisfile}\def\AdornVerseNumber%D%#1{{\beginL\rlap{{\hbox to \wd\versestarbox%D%{{\hfil #1\hfil}}}}%
{fancy/versedecoratorisfile}    \raise {fancy/versedecoratorshift}pt\copy\versestarbox%D%\endL}}
{fancy/versedecoratorisayah}\catcode`@=11\catcode`-=11\catcode`\~=12\lccode`\~=32\lowercase{{%
{fancy/versedecoratorisayah} \def\vp #1\vp*{{\edef\temp{{#1}}\x@\spl@tverses\temp --\relax
{fancy/versedecoratorisayah}  \ch@rstyle{{vp}}~\plainv@rse\ch@rstylepls{{vp}}*\kern 2\FontSizeUnit}}}}
{fancy/versedecoratorisayah}\catcode`@=12\catcode`=12
{fancy/versedecoratorisayah}\def\AdornVerseNumber%D%#1{{\hbox{{\char"06DD #1}}}}
""".replace("%D%", k)
        return res.format(**v.dict)

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
        texlines.append("\\TabsOddOnly{}".format("true" if model["thumbtabs/tabsoddonly"] else "false"))
        if rotate:
            rottype = int(model["thumbtabs/rotatetype"]) - 1
            texlines.append("\\TabTopToEdgeOdd{}".format("true" if rottype & 1 else "false"))
            texlines.append("\\TabTopToEdgeEven{}".format("true" if 0 < rottype < 3 else "false"))
        texlines.append("\\tab{}={:.2f}mm".format("width" if rotate else "height", height))
        texlines.append("\\tab{}={:.2f}mm".format("height" if rotate else "width", width))
        return "\n".join(texlines)+"\n"

class Colophon(Snippet):
    order = 10
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

class Grid(Snippet):
    regexes = []
    processTex = True
    texCode = r"""
\def\GraphPaperX{{{grid/xyadvance}{grid/units}}}
\def\GraphPaperY{{{grid/xyadvance}{grid/units}}}
\def\GraphPaperXoffset{{{grid/xoffset_}mm}}
\def\GraphPaperYoffset{{{grid/yoffset_}mm}}
\def\GraphPaperMajorDiv{{{grid/divisions}}}
\def\GraphPaperLineMajor{{{grid/majorthickness}pt}}
\def\GraphPaperLineMinor{{{grid/minorthickness}pt}}
\def\GraphPaperColMajor{{{majorcolor_}}} % Colour (R G B)
\def\GraphPaperColMinor{{{minorcolor_}}} % Colour (R G B)
"""
    takesDiglot = False

class ParaLabelling(Snippet):
    processTex = True
    texCode = r'''
\catcode`\@=11
\input marginnotes.tex
\newcount\pcount \pcount=0
{{\catcode`\~=12 \lccode`\~=32 \lowercase{{
\gdef\parmkr{{\setbox0=\vbox{{\hbox{{\ch@rstylepls{{zpmkr}}~\m@rker\ch@rstylepls{{zpmkr}}*}}}}%
    \advance\pcount by 1
    \d@marginnote{{0}}{{\the\pcount}}{{zpmkr}}{{left}}}}
}}
\addtoeveryparhooks{{\parmkr}}
'''

