#### Navigation

[Home](../home/README.md)  | [Installation](../installation/README.md) | [Quick Start](../quick-start/README.md) | [Documentation](../documentation/README.md) | [Cookbook ](../cookbook/README.md) 

[Cookbook >](../README.md) 

# <span class="entry-title">Special no-break spaces and hyphens</span>


## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

I need to keep words together or to control the way a line breaks.

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">

Use one of the following Unicode characters (Ptx2pdf handles these automatically, also in TOC and PDF bookmarks.):

*   U+00A0 NO-BREAK SPACE
*   U+00AD SOFT HYPHEN
*   U+200B ZERO WIDTH SPACE
*   U+2060 WORD JOINER
*   U+FEFF ZERO WIDTH NO-BREAK SPACE
*   U+2011 NON-BREAKING HYPHEN

</a>

## <a name="TOC-Solution"></a><a name="TOC-Source">Source</a>


paratext2.tex


<small>Updated on <abbr class="updated" title="2012-01-06T15:46:44.567Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">2</span>)</small>  

