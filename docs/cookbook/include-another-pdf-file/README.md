#### Navigation

[Home](../../home/README.md)  | [Installation](../../installation/README.md) | [Quick Start](../../quick-start/README.md) | [Documentation](../../documentation/README.md) | [Cookbook ](../README.md) 

[Cookbook >](../README.md) 

# <span class="entry-title">Include another PDF file</span>

## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

How can I include a pdf file?

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">

Use the \includepdf command in your project file, like this:



```% sample ptx2pdf-project file

\input paratext2.tex % first we \input the ptx2pdf macro package
\input GLW-setup.txt % then we \input the setup file

\includepdf{mytitlepage.pdf} % this is how we include another pdf file

\ptxfile{Intro-GLW.sfm} % we use \ptxfile to input the sfm files
\ptxfile{43-JHN-GLW.sfm}
\ptxfile{62-1JN-GLW.sfm}
\ptxfile{63-2JN-GLW.sfm}
\ptxfile{64-3JN-GLW.sfm}  
  
\end % and this is how we end this file
```



This is a convenient way to include title-pages or other material that cannot (easily) be made using SFMs. It can also be used to make simple multi script booklets.



## <a name="TOC-Solution"></a><a name="TOC-Source">Source</a>


paratext2.tex



<small>Updated on <abbr class="updated" title="2012-01-06T15:12:55.365Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">2</span>)</small>  

