#### Navigation

[Home](../../home/README.md)  | [Installation](../../installation/README.md) | [Quick Start](../../quick-start/README.md) | [Documentation](../../documentation/README.md) | [Cookbook ](../README.md) 

[Cookbook >](../README.md) 


# <span class="entry-title">Fake bold or italic</span>

## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

Is there a way to "fake" bold or italics?

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>


Yes, but use it with moderation: often the results can be quite ugly.

*   **For fake italic** there is the slant option.

```
\def\italic{"Charis SIL:slant=0.2"}
```
	
will give you "slanted Roman" instead of the real Charis SIL Italic. Note that a negative "slant" factor will skew the font the other way; that might be useful if you're dealing with a right-to-left script. 
	

*   **For fake bold**, use the embolden option.

```
\def\bold{"Charis SIL:embolden=2"}
```

The "emboldening factor" can be varied depending how much thickening you want, but 2 is probably a reasonable start. It scales in proportion to the font size.




<small>Updated on <abbr class="updated" title="2012-01-06T15:25:46.941Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">3</span>)</small>  

