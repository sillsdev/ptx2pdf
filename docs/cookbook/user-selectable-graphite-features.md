#### Navigation

[Home](../home/README.md)  | [Installation](../installation/README.md) | [Quick Start](../quick-start/README.md) | [Documentation](../documentation/README.md) | [Cookbook ](README.md)

[Cookbook >](README.md)


# <span class="entry-title">User selectable Graphite features</span>

## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

Does XeTeX support user-selectable Graphite font features and how are they accessed?

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">

Yes. They're accessed by adding the feature names and settings required to the font name, just like AAT features (and unlike OpenType features, which don't have names, only tags). So for example, as a plain XeTeX font declaration, you might say:

<div>

```
\font\charis = "Charis SIL/GR:
     Uppercase Eng alternates=Capital N with tail;
     Literacy alternates=True" at 12pt
...
\charis This is some sample text....
```

</div>

to load and use Charis with a couple of specific features. For ptx2pdf, you'd simply include the feature settings in the font name defined for \regular, \bold, etc.

To find out the names of the features supported by a font, you can consult the font's documentation, look in the user interface of an application that provides full Graphite feature support, or run the "feature-info.tex" file through XeTeX, editing it to specify the font you want to know about. This will generate a PDF that reports the font's available feature names and settings.



<small>Updated on <abbr class="updated" title="2012-01-06T16:09:00.064Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">3</span>)</small>
