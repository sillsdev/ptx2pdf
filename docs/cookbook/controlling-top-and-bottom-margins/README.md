#### Navigation

[Home](../home/README.md)  | [Installation](../installation/README.md) | [Quick Start](../quick-start/README.md) | [Documentation](../documentation/README.md) | [Cookbook ](../cookbook/README.md) 

[Cookbook >](../README.md) 


# <span class="entry-title">Controlling top and bottom margins</span>


## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

1.  I have a PDF border for my document, but I want to make the bottom margin a little larger, so it doesn't run into my border.
2.  It appears to me that the top/bottom margins specify the limits of the text including the header and footer. So how can you specify the distance between the header and the body text (and same for footer)?

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">

1.  Use \BottomMarginFactor in ptx-stylesheet.tex if you want to control top and bottom separately. (If you leave it undefined, the macros will re-use the top factor for both.) So, \TopMarginFactor (and \BottomMarginFactor, if separately specified) will relate just to the margins of the body text area, independent of headers and footers.  

2.  The parameters \HeaderPosition and \FooterPosition (with defaults of 0.5) controls the position of the header and footer. These are also in terms of \MarginUnit, and give the position of the baseline of the header/footer relative to the top/bottom edge of the paper (not the text area).

\RHruleposition (position of rule under the running head) measures from the baseline of the header (rather than upwards from the text area). This is a simple dimension, not a relative "factor".  
</a>

## <a name="TOC-Solution"></a><a name="TOC-Source">Source</a>


ptx-stylesheet.tex


<small>Updated on <abbr class="updated" title="2012-01-06T15:23:58.980Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">5</span>)</small>  

