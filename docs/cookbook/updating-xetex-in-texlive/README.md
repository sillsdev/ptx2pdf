#### Navigation

[Home](../../home/README.md)  | [Installation](../../installation/README.md) | [Quick Start](../../quick-start/README.md) | [Documentation](../../documentation/README.md) | [Cookbook ](../README.md)

[Cookbook >](../README.md)


# <span class="entry-title">Updating XeTeX in TeX Live (Windows)</span>


## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

How can I update XeTeX to the latest version (I use TeX Live on Windows)?

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">

If you have a TeX Live installation as installed by the TeX Live installer,
run `tlmgr update --self --all`

If you have a mini installation based on W32TeX then continue reading.
</a>

*   Download the latest W32TeX build using the CTAN mirror from Akira's [W32TeX page](http://w32tex.org/): You will need the following files.

    *   dvipdfm-w32.tar.xz
    *   latex.tar.xz
    *   mftools.tar.xz
    *   pdftex-w32.tar.xz
    *   platex.tar.xz
    *   ptex-w32.tar.xz
    *   web2c-lib.tar.xz
    *   web2c-w32.tar.xz
    *   xetex-w32.tar.xz

*   For further validation, you can download these files from the other mirrors,
    and compare the files using a diff tool or checksums.
    There are often differences in the downloaded files between the different mirrors,
    probably because the W32TeX project builds very frequently (perhaps daily),
    and it takes some time for the mirrors to be updated.

*   You could pick and choose the latest file from among the mirrors
    (which is not entirely possible as some of the mirrors do not display timestamps,
    and of those timestamps that are displayed the timezone of the mirror might
    make the timestamp seem different, even for the same time of building the tarball).
    This is not recommended, as you might get files from two different builds of W32TeX.
    Therefore, update your installation with files all from the same mirror.

*  Uncompress the .tar.xz files, making sure to maintain the folder structure

   *   not all Windows compression programs can handle this type of file, try 7-zip.org
   *   Linux users can use `tar -Jxf filename.tar.xz`

*  Use a directory diff tool (such as WinMerge, meld, or kdiff3) to compare the \bin and \share folders,
   and copy the files that differ.
   You don't want to copy all the files, as that will substantially increase the size of your mini installation.

     *   You may have to adjust the directory names and file locations, as these change due to Tex Live development.
     *   In the `\bin` folder, there are two files that have a version number in them
         (X indicating a digit), `icudtXX.dll` and `kpathseaXXX.dll`. You will need to remove the older file, and add the newer file.

*  You might need to run `fmtutil --byfmt xetex`, although XeTeX may do this for you when you first run XeTeX.

*  The first time XeTeX runs it might take quite a while - rebuilding some font databases.



<small>Updated on Aug 30, 2019 by Bobby de Vos</small>
