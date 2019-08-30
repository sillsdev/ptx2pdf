#### Navigation

[Home](../../home/README.md)  | [Installation](../../installation/README.md) | [Quick Start](../../quick-start/README.md) | [Documentation](../../documentation/README.md) | [Cookbook ](../README.md)

[Cookbook >](../README.md)


# <span class="entry-title">Reset page numbering</span>

## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

Is there some way to reset page numbering after, say, the end of the introductory stuff or between one section of introduction (say, a foreword) and another (say, a preface)?

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>



You should be able to say:

```
\pageno = 1
```


(or another number) in between \ptxfile commands in your main project file.

**Note:** You would use "\pageno" (from Plain TeX) to assign the number, whereas you use "\pagenumber" (defined by the ptx2pdf macros) to actually print the number (e.g., in the running header). It will not work to put \pageno=... **within** a USFM file, so to do this you'd need to make sure each section of the introductory material is in a separate file, then see above.



<small>Updated on <abbr class="updated" title="2012-01-06T15:36:28.036Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">2</span>)</small>
