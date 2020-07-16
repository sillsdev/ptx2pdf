#### Navigation

[Home](../home/README.md)  | [Installation](../installation/README.md) | [Quick Start](../quick-start/README.md) | [Documentation](../documentation/README.md) | [Cookbook ](README.md)

[Cookbook >](README.md)


# <span class="entry-title">Suppressing v output or x output</span>

## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

How can I suppressing the \v output (e.g. not print verse numbers)? Or \x output, e.g. not printing the cross-references?

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">

Character-style SFMs support "\TextProperties nonpublishable". So you can now suppress verse numbers simply by putting:

```
\Marker v
\TextProperties nonpublishable
```

in a stylesheet file. (I don't know if Paratext would object to finding this in its stylesheet; but in any case, you shouldn't be modifying the main USFM stylesheet for things like this; put them in a local override file that is loaded after the main stylesheet.)

Note SFMs also support this option. This could be useful, for example, if you've got cross-references for the whole Bible coded with \x .... \x*, but want to print a portion (e.g., just a Gospel) without x-refs; no need to modify the USFM file, just add:

```
\Marker x
\TextProperties nonpublishable
```


to a custom stylesheet override, and they'll disappear from the output.

</a>

### <a name="TOC-Solution"></a><a name="TOC-Source">Source</a>



ptx-stylesheet.tex


<small>Updated on <abbr class="updated" title="2012-01-06T15:56:14.418Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">2</span>)</small>
