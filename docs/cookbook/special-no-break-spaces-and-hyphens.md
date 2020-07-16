#### Navigation

[Home](../home/README.md)  | [Installation](../installation/README.md) | [Quick Start](../quick-start/README.md) | [Documentation](../documentation/README.md) | [Cookbook ](README.md)

[Cookbook >](README.md)

# <span class="entry-title">Special no-break spaces and hyphens</span>


## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

I need to keep words together or to control the way a line breaks.

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">

Use one of the following Unicode characters (Ptx2pdf handles these automatically, also in TOC and PDF bookmarks.):

*   ~      TILDE (treated as no-break space)
*   U+00A0 NO-BREAK SPACE
*   U+00AD SOFT HYPHEN
*   U+200B ZERO WIDTH SPACE
*   U+2060 WORD JOINER
*   U+FEFF ZERO WIDTH NO-BREAK SPACE
*   U+2011 NON-BREAKING HYPHEN

</a>

## <a name="TOC-Solution"></a><a name="TOC-Source">Source</a>


paratext2.tex


<small>Updated on <abbr class="updated" title="2020-07-16T14:15+03:00">Jul 16, 2020</abbr> by <span class="author"><span class="vcard">David Gardner</span> </span>(Version <span class="sites:revision">2</span>)</small>
