#### Navigation

[Home](../home/README.md)  | [Installation](../installation/README.md) | [Quick Start](../quick-start/README.md) | [Documentation](../documentation/README.md) | [Cookbook ](../cookbook/README.md) 

[Cookbook >](../README.md) 


# <span class="entry-title">Making shorter or longer paragraphs</span>



## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

How can I make a paragraph shorter or longer?

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">

Make an adjustment file containing:

`BBB C.V ADJ [n]`


*   **BBB** is the book code (GEN, EXO, MAT, etc)
*   **C.V** is the chapter.verse reference
*   **ADJ** is the paragraph-length adjustment to be applied here (+1, +2, -1, etc)
*   **[n]** is an optional index of paragraph within the verse, default is 1

`JHN 3.1 +2`


Make sure the adjustment file has the correct name, so that it will automatically be found. The correct name is: <font face="'courier new', monospace">[name of ptx file].adj</font>

`47-JHN-U.PTX.adj`


## <a name="TOC-Solution"></a><a name="TOC-Source">Source</a>



ptx-adj-list.tex



<small>Updated on <abbr class="updated" title="2012-01-06T15:44:07.190Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">2</span>)</small>  

