#### Navigation

[Home](../../home/README.md)  | [Installation](../../installation/README.md) | [Quick Start](../../quick-start/README.md) | [Documentation](../../documentation/README.md) | [Cookbook ](../README.md)

[Cookbook >](../README.md)


# <span class="entry-title">Updating XeTeX in TeXLive (Windows)</span>


## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

How can I update XeTeX to the latest version (I use TeXLive on Windows)?

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">

Listed below are the steps I followed to successfully update the version of XeTeX in my TeX Live installation.

Some details: I started with TeX Live 2007, standard installation, with files located at C:\TeXLive2007\. It has XeTeX 0.996, and I wanted to update to XeTeX 0.997 which has support for the \includepdf macro.

</a>

*   Download the latest "xetex-dev" package from Akira's [W32TeX page](http://w32tex.org/):</a>
    *   <a name="TOC-Solution">go to </a>[http://www.fsci.fuk.kindai.ac.jp/kakuto/win32-ptex/web2c75-e.html](http://www.fsci.fuk.kindai.ac.jp/kakuto/win32-ptex/web2c75-e.html) (no longer available)
    *   scroll down to XeTeX-DEV for W32 (0.997)
    *   click on link to download the file [ xetex-dev-w32.tar.bz2 ]

*  Uncompress the .tar.bz2 file, making sure to maintain the folder structure

   *   not all Windows compression programs can handle this type of file, try 7-zip.org or bzip.org

*  Open the \bin folder at the top of that folder structure and select and copy all files

     *   14 files in my case, all *.dll and *.exe files

*  Go to C:\TeXLive2007\bin\win32 folder and paste

     *   This will replace 13 files (3 of which were identical, but that's not a problem)
     *   One file wasn't in the \win32 folder before, icudt38.dll, so it will just paste

*  Go to a command prompt and type "fmtutil --byfmt xetex".
*  Now you should be able to use the new version (0.997) of XeTeX

    *   The first time I ran XeTeX it took quite a while - rebuilding some databases



<small>Updated on Aug 26, 2019 by Lorna Evans</small>
