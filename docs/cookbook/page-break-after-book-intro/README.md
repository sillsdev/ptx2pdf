#### Navigation

[Home](../home/README.md)  | [Installation](../installation/README.md) | [Quick Start](../quick-start/README.md) | [Documentation](../documentation/README.md) | [Cookbook ](../documentation/README.md) 

[Cookbook >](../README.md) 


# <span class="entry-title">Page break after book intro</span>


## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

I would like to find a way to automatically make a page break after a book's introduction section? (I don't want to have to edit the source and put an \eject in.)

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">

If the introduction is long enough to warrant a page break put it in a separate SFM file, which means you get a page break automatically because \ptxfile always starts a fresh page.

Is there a title at the start of the actual Scripture text? If there is something like \mt here, you could put \pagebreak (not a bare \eject) into the {before} hook for it.

</a></div>



<small>Updated on <abbr class="updated" title="2012-01-06T15:21:25.409Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">2</span>)</small>  

