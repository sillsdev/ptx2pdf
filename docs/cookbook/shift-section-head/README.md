#### Navigation

[Home](../../home/README.md)  | [Installation](../../installation/README.md) | [Quick Start](../../quick-start/README.md) | [Documentation](../../documentation/README.md) | [Cookbook ](../README.md) 

[Cookbook >](../README.md) 


# <span class="entry-title">Shift section head</span>

## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

How do I adjust the position of the section headers so that they are visually a little bit closer to the text below?

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>


You should be able to achieve this by adjusting the \SpaceAfter for the heading style. The space above it will change to compensate, so as to maintain the text grid afterwards. When the macros do a heading (or group of headings), they try to keep the \SpaceAfter at the value you've specified, and if they need to add "padding" for alignment, that goes before the heading.


<small>Updated on <abbr class="updated" title="2012-01-06T15:37:59.059Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">2</span>)</small>  

