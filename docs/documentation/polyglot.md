
# Multipage polyglot

Example control file:
```
\def\pluginlist{polyglot-simplepages}
\input paratext2.tex

\diglottrue
\newPolyglotCol A
\polyglotpages{LR,A}
\def\DiglotLFraction{0.55} % In case texts fit better with unequal columns
\def\DiglotRFraction{0.45} 
\def\DiglotAFraction{1} 
\diglotSepNotestrue
\diglotBalNotesfalse

\stylesheet{usfm-sb.sty} % Generic stylesheet, applicable to all columns
\stylesheetA{colA.sty} % Column specific styling
.
.
```

If `polyglot-simplepages` is included in the (comma separated) list of plugins
to load, in the first line  of the example above, then multi-page polyglot
pages become a possibility. It is the ```\polyglotpages{LR,A}``` 
command that actually specifies whether multipage polyglot 
*will* be used or not.  ```\polyglotpages{LAR}```  would merely redefine the column order 
(as would ```\def\diglot@list{LAR}``` would, without loading the plugin).

The appropriate `\newPolyglotCol` must have been given for each newly defined
column, before `\polyglotpages` is called.  

```\polyglotpages{LA,BC,RDE,-}``
would define four pages to output. 
There should not be spaces in the comma separated list. These pages are
numbered 0,1,2,3 internally. The fourth page with a content of `-` is blank in
terms of Biblical text, but it may
(eventually) be used as a target for images, side-bars, etc.  

If the number of polyglot pages is even then the code will ensure that the initial page (page 0) of any set
starts on an even number, using the (internal) `\need@evenpage` macro which uses  the user-available `\EmptyPage`.
The difference between ```\polyglotpages{LA,BC,RDE,-}``` and ```\polyglotpages{LA,BC,RDE}``` is thus twofold: each set 
of the the former will be always start on an even page number (even if there is monoglot text before-hand or a full-page 
page picture) and the set will take 4 pages; the second will start on any page number, and ignore any problems 
this might cause with binding, but it is more economical for printing if the text
will be printed single-sided for wall-mounting (or making a scroll??).


