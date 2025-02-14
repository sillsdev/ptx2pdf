# Sample instructions for use while polyglot is unsupported by the UI.

## Make empty USFM files. e.g. XXA
You can do this either in Paratext or just write an empty file (note that if
you make an empty file, PTXprint might moan a bit).  Each configuration that PTXprint knows about for the diglot must include this file.
**DO NOT** include any output-generating content in it.


## Prepare the input files
You probably want (at least) 3 project/configurations: (a). A diglot of the primary and 
secondary  text (b) a monoglot (or diglot) for the 3rd (and 4th, 5th) text(s) (c) eventually, 
the polyglot configuration.

Make sure that you have a reasonable primary-secondary diglot, in terms of fonts, etc. and then save it under a new name for the polyglot configuration.

Until PTXprint can handle the merge itself, the  polyglot process will not be able to 
regenerate any intermediate files for you, so you *must* run print on all input books/chapters, 
so that ptxprint can  apply Changes.txt, etc and generate a print-ready version of the file.

Repeat the printing step each time you change anything that will affect the final USFM. e.g.  
what to do with `\w`, or updates from Paratext. You will also need to re-merge any changed USFM 
files.

## Tell PTXprint to print that empty USFM file.
I.e. make the polyglot project print that empty file.

## Merge the print-ready SFM files
Assuming that the project is PROJ, the normal diglot is in configuration `diglot` and the other
project is `ALTPRJ` (configuration `diglot`), and this is all going to be in project triglot,
then, 
On linux, the process might look like this:
```
$ cd ~/Paratext8Projects/{PROJ}/local/ptxprint/triglot/
$ usfmerge -m scores -o mergedJHN.usfm  \
		-s ~/src/ptx2pdf/src/ptx2pdf.sty \
		-s ../../../shared/ptxprint/diglot-bt/ptxprint.sty \
		../diglot/44JHNPROJ-diglot.SFM ../diglot/44JHNPROJbtEn-Default.SFM ../../../../ALTPRJ/local/ptxprint/diglot/44JHNALTPRJ-diglot.SFM 
```
The ptx2pdf.sty file is shipped with ptxprint's TeX macros. Hopefully you can find it.
There are plenty of other merge options, see the output of `usfmerge -h`.
Note that the order of merging determines which file is which. The order is L,R,A,B,C...

## Configuration changes
1. Ensure that  `polyglot-simplepages` is loaded as a module (on the advanced tab).
2. Activate `ptxprint-premods.tex` and add this text to it:
```
\newPolyglotCol A
\def\DiglotAFraction{0.01}
\def\regularA{"Charis SIL"}
\def\boldA{"Charis SIL/B"}
\def\italicA{"Charis SIL/I"}
\def\bolditalicA{"Charis SIL/BI"}
```
(replacing the font(s) as appropriate). If you are doing a 4-glot, (or more) add similar lines, replacing each `A` with `B` (4th merged file), `C` (5th merged file) and so on.

3. Activate `ptxprint-mods.tex` and add this text to it.
```
\def\DiglotAFraction{0} 
\polyglotpages{LR}
\setbookhook{end}{final}{\relax\polyglotpages{LRA}
  \setbookhook{end}{final}{\layoutstylebreak\singlecolumn\zcolophon}
  \stylesheetA{../../../../RMYOU/shared/ptxprint/diglot/ptxprint.sty}
  \def\DiglotAFraction{0.33} 
  \def\DiglotLFraction{0.33} 
  \def\DiglotRFraction{0.33} 
  \csname s@tupsizes\endcsname
  \diglottrue
  \lastptxfilefalse
% \ptxfile{mergedMAT.usfm}
  \lastptxfiletrue
  \ptxfile{mergedJHN.usfm}
}
```

If there are files other than XXA included by the configuration, they will be
output with the normal diglot settings of 2 columns and 0 space for column A.
Only after the last file requested from the user-interface will the hand-merged
files be loaded.

The sample above does *not* load `mergedMAT.usfm` (the line is commented out)
and but it does load the `mergedJHN.usfm` file.  Other files should be loaded
in the place that `MAT` is, and the last file should be preceded by
`\lastptxfiletrue` so that the colophon is triggered.

Notice that the hook resets itself (to generate the colophon). Commenting out
that line would be a mistake, as it would cause an infinite loop, with the
hook-code getting triggered by the last 

