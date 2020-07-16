#### Navigation

[Home](../home/README.md)  | [Installation](../installation/README.md) | [Quick Start](../quick-start/README.md) | [Documentation](../documentation/README.md) | [Cookbook ](README.md)

[Cookbook >](README.md)


# <span class="entry-title">Adjusting space after chapter number</span>


## <a name="TOC-Problem">Problem</a>

Is there a way of controlling the amount of indentation of text after a chapter number? I have a chapter number which covers two lines (default?) and would like to indent the first two lines further than they are at present. I have tried enabling IndentAtChaptertrue, but this only effects the first line.

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

There's a parameter called \AfterChapterSpaceFactor that might help; try

```
\def\AfterChapterSpaceFactor{10}
```

and see what happens. (Default is 3\. It is related to the `\FontSizeUnit`, so it scales with the text.)


<small>Updated on <abbr class="updated" title="2012-01-06T15:00:15.050Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">8</span>)</small>
