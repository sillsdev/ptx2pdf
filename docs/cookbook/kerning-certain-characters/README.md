#### Navigation

[Home](../home/README.md)  | [Installation](../installation/README.md) | [Quick Start](../quick-start/README.md) | [Documentation](../documentation/README.md) | [Cookbook ](../documentation/README.md) 

[Cookbook >](../README.md) 

# <span class="entry-title">Kerning certain characters</span>

## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

I would like to decrease the kerning between the period and several different letters in my language, these letters take several combinations of diacritics. I would like to make this happen through out the Scripture portion that I am typesetting?

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">

The "proper" way to do it would be to put the kerning you want into the font. A possible macro-level workaround might be to use character classes and the inter-character token insertion feature. If you do something like:

```
\XeTeXinterchartokenstate=1  
  
\XeTeXcharclass `a = 4 % class of letters where . is to be kerned closer
\XeTeXcharclass `e = 4
\XeTeXcharclass `i = 4
\XeTeXcharclass `o = 4
\XeTeXcharclass `u = 4  
  
\XeTeXcharclass `. = 5 % assign a separate class to the period itself  
  
\XeTeXinterchartoks 4 5 = {\kern-0.1em} % kern whenever classes 4 and 5 are adjacent
```

... then you'll get an extra kern between any of those vowels and a following period. (Replace these example chars with the ones you're really interested in, of course. You can also specify them as Unicode character numbers rather than using the back-quote and a literal character, if that's more convenient.) To ignore certain diacritics for this purpose, assign them the class 256.

Character classes range from 0..255 (and 256 for "ignore"); I started from 4 here simply because the xetex format file preassigns some CJK characters to classes 1..3.

All this assumes that you're running XeTeX 0.997, as earlier releases did not have the inter-character tokens feature.



<small>Updated on <abbr class="updated" title="2012-01-06T15:19:14.916Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">2</span>)</small>  

