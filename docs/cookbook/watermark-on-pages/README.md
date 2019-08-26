#### Navigation

[Home](../home/README.md)  | [Installation](../installation/README.md) | [Quick Start](../quick-start/README.md) | [Documentation](../documentation/README.md) | [Cookbook ](../cookbook/README.md) 

[Cookbook >](../README.md) 


# <span class="entry-title">Watermark on pages</span>

## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

Is there a way to print a watermark on all pages?

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">Put whatever watermark you like into a PDF file by itself – you'll want it fairly light gray, probably, if it's going to go behind all the text. Then just add something like:

```
\def\PageBorder{mywatermark.pdf}
```

to the setup file, and the specified PDF file will be added behind each page. You can add options to resize it, etc:

```
\def\PageBorder{mywatermark.pdf scaled 2000 rotated 45}
```

(the "scaled" factor is relative to 1000, so this would be double the original image size).

</a>

## <a name="TOC-Solution"></a><a name="TOC-Source">Source</a>

<a name="TOC-Source">

ptx-cropmarks.tex



<small>Updated on <abbr class="updated" title="2012-01-06T16:11:54.537Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">2</span>)</small>  

