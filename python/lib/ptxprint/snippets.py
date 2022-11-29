import re, os
import regex
from .texmodel import universalopen
from .ptsettings import bookcodes
from .utils import pycodedir, htmlprotect

class Snippet:
    order = 0
    regexes = []
    processTex = False
    texCode = ""
    takesDiglot = False

class PDFx1aOutput(Snippet):

    def generateTex(self, model, diglotSide=""):
        res = r"""
\bgroup
\catcode`\#=12 
\catcode`\@=11 \catcode`\^^M=10 \deactiv@tecustomch@rs
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
            model.dict["/iccfpath"] = os.path.join(libpath, "sRGB.icc").replace("\\","/")
            extras['_iccnumcols'] = "3"
        if pdftype == "Gray":
            model.dict['/iccfpath'] = os.path.join(libpath, "default_gray.icc").replace("\\","/")
            extras['_iccnumcols'] = "1"
        else:
            extras['_iccnumcols'] = "4"
        extras['_gtspdfaid'] = "      <pdfaid:part>1</pdfaid:part>\n      <pdfaid:conformance>B</pdfaid:conformance>\n"
        extras['rtlview'] = " /ViewerPreferences <</Direction /R2L>>" if model['document/ifrtl'] == "true" else ""
        for a in ('author', 'title', 'subject'):
            extras['_gtf'+a] = htmlprotect(model.dict['document/'+a])
        if model['document/printarchive']:
            res += "\XeTeXgenerateactualtext=1\n"
        return res.format(**{**model.dict, **extras}) + "\n"
    
class FancyIntro(Snippet):
    texCode = r"""
\sethook{before}{ior}{\leaders\hbox to 0.8em{\hss.\hss}\hfill}

"""

class Diglot(Snippet):
    processTex = True
    texCode = r"""
\def\regularR{{"{diglot/fontregular}{diglot/docscript}"}}
\def\boldR{{"{diglot/fontbold}"}}
\def\italicR{{"{diglot/fontitalic}{diglot/docscript}"}}
\def\bolditalicR{{"{diglot/fontbolditalic}{diglot/docscript}"}}

\def\DiglotLeftFraction{{{document/diglotprifraction}}}
\def\DiglotRightFraction{{{document/diglotsecfraction}}}

%\addToLeftHooks{{\FontSizeUnit={paper/fontfactor}pt}}
%\addToRightHooks{{\FontSizeUnit={diglot/fontfactor}pt}}
\FontSizeUnitR={diglot/fontfactor}pt
\def\LineSpacingFactorR{{{diglot/linespacingfactor}}}
\def\AfterChapterSpaceFactorR{{{diglot/afterchapterspace}}}
\def\AfterVerseSpaceFactorR{{{diglot/afterversespace}}}
\addToLeftHooks{{\RTL{document/ifrtl}}}
\addToRightHooks{{\RTL{diglot/ifrtl}}}
%{diglot/iflinebreakon}\XeTeXlinebreaklocaleR "{diglot/linebreaklocale}"
\diglotSwap{document/diglotswapside}
{diglot/interlinear}\expandafter\def\csname complex-rb\endcsname{{\ruby{project/ruby}{{rb}}{{gloss}}}}
{diglot/ifletter}\newskip\intercharskipR \intercharskipR=0pt plus {diglot/letterstretch:.2f}em minus {diglot/lettershrink:.2f}em
{diglot/ifletter}\def\letterspaceR{{\leavevmode\nobreak\hskip\intercharskipR}}
{diglot/ifletter}\DefineActiveChar{{^^^^fdd1}}{{\letterspaceR}}
\catcode `@=12

"""

class FancyBorders(Snippet):
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
{%E%fancy/sectionheader}\squashgridboxfalse

{%E%fancy/versedecoratorisfile}\newbox\versestarbox%D%
{%E%fancy/versedecoratorisfile}\setbox\versestarbox%D%=\hbox{{\XeTeXpdffile "{%E%fancy/versedecoratorpdf}" scaled {%E%fancy/versedecoratorscale} \relax}}
{%E%fancy/versedecoratorisfile}\def\AdornVerseNumber%D%#1{{\beginL\rlap{{\hbox to \wd\versestarbox%D%{{\hfil #1\hfil}}}}%
{%E%fancy/versedecoratorisfile}    \raise {%E%fancy/versedecoratorshift}pt\copy\versestarbox%D%\endL}}
{%E%fancy/versedecoratorisayah}\catcode`@=11\catcode`-=11\catcode`\~=12\lccode`\~=32\lowercase{{%
{%E%fancy/versedecoratorisayah} \def\vp #1\vp*{{\edef\temp{{#1}}\x@\spl@tverses\temp --\relax
{%E%fancy/versedecoratorisayah}  \ch@rstyle{{vp}}~\plainv@rse\ch@rstylepls{{vp}}*\kern 2\FontSizeUnit}}}}
{%E%fancy/versedecoratorisayah}\catcode`@=12\catcode`=12
{%E%fancy/versedecoratorisayah}\def\AdornVerseNumber%D%#1{{\hbox{{\char"06DD #1}}}}
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
    texCode = """
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

