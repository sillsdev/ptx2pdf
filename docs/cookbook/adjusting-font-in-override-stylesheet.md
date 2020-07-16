#### Navigation

[Home](../home/README.md)  | [Installation](../installation/README.md) | [Quick Start](../quick-start/README.md) | [Documentation](../documentation/README.md) | [Cookbook ](README.md)

[Cookbook >](README.md)


# Adjusting font in override stylesheet


## <a name="TOC-Problem">Problem</a>


How can I override the style definition given by USFM.STY, e.g. set marker ip to Bold or a font name?

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">To load an "override stylesheet" after your main usfm.sty just use two \stylesheet commands in your job or setup file, e.g.:


```
\stylesheet{usfm.sty}
\stylesheet{MyStylesheet-mods.sty}
```


This allows you to have a main stylesheet that is shared between all versions and stays untouched, and have a project-specific customization stylesheet.

The modifications stylesheet contains just the markers/attributes that you want to override:


```
\Bold
```



or a fontname:

```
\Marker ip
\FontName Lateef:script=arab
```



It doesn't have to provide full redefinitions of the styles; the attributes you don't mention will retain their existing values from the main stylesheet.



<small>Updated on <abbr class="updated" title="2012-01-06T15:22:16.761Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">5</span>)</small>
