#### Navigation

[Home](../home/README.md)  | Installation | [Quick Start](../quick-start/README.md) | [Documentation](../documentation/README.md) | [Cookbook ](../cookbook/README.md)



# Installation
To use ptx2pdf you need (a) XeTeX and (b) the ptx2pdf macro package. If you don't have XeTeX installed you need to do that first.

## <a name="TOC-Installing-XeTeX">Installing XeTeX</a>

<a name="TOC-Installing-XeTeX">The most convenient way to setup a TeX system is through installing TeX Live. TeX Live is available for all major platforms, though Mac users might want to use MacTeX and Windows users might be interested in using the MikTeX distribution.

If you don't want a full blown TeX distribution on your machine, you might want to use this[minimal Windows XeTeX distribution](https://bitbucket.org/hindlemail/xetexnuget/src/default/PutXetexFolderInHere/) based on W32TeX. This distribution contains the ptx2pdf macros, so you don't need to install them as described below.

</a>

## <a name="TOC-Installing-ptx2pdf">Installing ptx2pdf</a>

<a name="TOC-Installing-ptx2pdf">The ptx2pdf macros are held in a GitHub (version control) repository. You can access this in several ways:

1.  With a web browser, go to [https://github.com/sillsdev/ptx2pdf](https://github.com/sillsdev/ptx2pdf). Here, you can view the individual files, access their revision history, etc.
2.  At that page, click the "Clone or Download" link. This will download an archive "ptx2pdf-master.zip" containing all the macro files.

Next step is to place the macro files at the appropriate place in your texmf tree. This would typically be something like ```~/<user>/Library/texmf/tex/ptx2pdf/``` (Mac) or ```/usr/share/texmf/tex/ptx2pdf/``` (Linux) or ```winpath``` (Windows).
</a>

<a name="TOC-Installing-ptx2pdf"></a></td>


<small>Updated on Sep 4, 2019 by <span class="author"><span class="vcard">Bobby de Vos</span> </span>(Version <span class="sites:revision">7</span>)</small>
