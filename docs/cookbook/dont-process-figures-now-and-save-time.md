#### Navigation

[Home](../home/README.md)  | [Installation](../installation/README.md) | [Quick Start](../quick-start/README.md) | [Documentation](../documentation/README.md) | [Cookbook ](README.md)

[Cookbook >](README.md)

# <span class="entry-title">Don't process figures now and save time</span>


## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

Since image processing takes a lot of time, can I temporarily "switch figures off"?

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">

Yes, use the "figure placeholders" mode, which will read your picture definitions but just print a rectangular frame with the filename, rather than the actual graphic. If you put:

`\FigurePlaceholderstrue`

in your control file, you'll get this mode; the text layout will be unaffected. Obviously, you'll need to see the actual figures at certain points in the process, but you may be able to do much of the paging in this mode, and it'll be much faster.

</a></div>

<a name="TOC-Solution"></a></td>



<small>Updated on <abbr class="updated" title="2012-01-06T15:05:30.736Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">4</span>)</small>
