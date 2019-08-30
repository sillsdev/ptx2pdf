#### Navigation

[Home](../../home/README.md)  | [Installation](../../installation/README.md) | [Quick Start](../../quick-start/README.md) | [Documentation](../../documentation/README.md) | [Cookbook ](../README.md)

[Cookbook >](../README.md)


# <span class="entry-title">Creating a booklet</span>


## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">I would like to create a booklet, can ptx2pdf do that for me?
</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">Ptx2pdf does not provide this functionality. It's recommend to format the document as individual pages, then post-processing the PDF. There are a few tools you could use:</a>

*  Typeset the the pdf (without cropmarks!) and print it using Adobe Readers "booklet option". (See the "Booklet printing" option of the Page Scaling pop-up in the Print dialog).</a>
*  Typeset the the pdf (without cropmarks!) and use [pdfbklt](https://metacpan.org/pod/Text::PDF) (a perl-script).
*  There's a LaTeX package "pdfpages" that can do this; see the description of the "signature" option in the pdfpages documentation. (This requires a regular LaTeX installation, though, not a minimal Scripture-only XeTeX setup.)

<small>Updated on <abbr class="updated" title="2011-05-18T20:13:08.593Z">May 18, 2011</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">2</span>)</small>
