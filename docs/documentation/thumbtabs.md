# Thumb-tabs
## Introduction
Sometimes it is a useful thing for a reader to have an indication of where they
are in the book (in this case, which biblical book within scripture). While
actual cut index holes are probably not affordable, a block of ink that
extends all the way to the the edge of the page can usually be visible from a
closed or partly open book, and serves a similar purpose. By default, the
abbreviated book name (```\toc3``` from the USFM file) is written in white on a
black box.  

The USFM extension ```\zthumbtab`` can be used to set an alternative 
value for the thumbtab contents. If a book's header contains a ```\zthumbtab``` entry, 
then ```\toc3``` will not set the thumbtab contents. An empty ```\zthumbtab``` entry 
specifies that there should be no text in the thumbtab for that book.

By default the font styling from the `toc3` entry in the stylesheet is used.  If crop-marks are used, the box extends into the area that is expected to be cropped by a few pt.

## How placement is calculated
Thumb-tab placement on the vertical axis is a simple case of determining the space available and dividing it between how many tabs are expected. If three tabs are expected (```\NumTabs=3```), tabs with index 1 will be at the top of the defined area, those with index 3 at the bottom, and those with index 2 in exact middle. There is no attempt made to prevent tabs from different books overlapping somewhat or having significant gaps between them. The height of tabs **is** taken into account in setting the limits (i.e. the uppermost edge of the first thumb tab and the lowermost edge of the last thumbtab are at the positions specified).

For a volume containing all 39 books of the OT, on A5 paper (21 cm, ~8inches high before margins are accounted for), in a single run, the differnce between tab positions calculated in this manner is around 12pt. Thus a 'perfect staircase', without overlap or repetition, while perhaps aesthetically pleasing is probably only achievable if 2 letter abbreviations and a small font are used. However this goal will certainly be problematic if longer short-forms are required by the readership, either from the point of view of readbility (text being far too small when using 'tall' tabs with rotated text), excessive margins (if the text is not rotated), or usability as three  or more 'cycles' of tabs become necessary to fit a more reasonable 40-50pt tab height with rotated text.

## Basic use parameters
There is only one command necessary to begin using the 
* \setthumbtab{`GEN`}{`1`} - generate a page-edge thumb-tab for all pages in the book of Genesis, containing the ``\toc3`` text if that is set. The code (```GEN``` in the example) must be an exact match of the code used in the USFM `\id` marker.  
All `\setthumbtab` commands should be placed before the first `\ptxfile{}`. Sequencing with style-files, etc. is not significant.
It may be useful to have a separate file listing tab positions and related settings, included with ```\input{filename.tex}```.  
The second parameter is a number (```1``` in the example) or the special value ```\relax```. It is termed the index number in this documentation and (together with parameters below) controls the vertical position of the tabs for the given book, with 1 being nearest the top of the page.  There is no requirement that the  index number follow the order of books, but readers will probably expect them to.  It may be appropriate to re-start the sequence at the transition from Old Testament to New Testament. (default - no thumb-tab) 

### Set up parameters
* \TabsStart=```10pt``` Distance between the upper edge of the topmost thumb-tab and the top margin of the page (text area). Negative values may be given to extend tabs into the upper margin.
* \TabsEnd=```10pt``` Distance between the lower edge of the lowermost thumb-tab and the bottom page margin (text area). Negative values may be given to extend tabs into the lower margins.
* \tabheight=```50pt``` Vertical dimension of the thumbtab. (default 50pt).
* \tabwidth=```25pt``` Vertical dimension of the thumbtab. (default 15pt).
* \def\tabBoxCol{```0.2 0.3 0.2```} colour definition for the thumb-tab, the 3 numbers representing red, green and blue in the range of 0 (black), 0.5 (half)  to 1 (fully lit). (Default ```0 0 0```).
* \def\tabFontCol{```0.5 1 0.5```} colour definition for the thumb-tab, the 3 numbers representing red, green and blue in the range of 0 (black), 0.5 (half)  to 1 (fully lit). (Default ```1 1 1```).
* \TabRotationNormal```true``` When this is true, then when the ```\tabheight``` > ```\tabwidth``` the text on the tab will be rotated, and otherwise it will be horizontal. If false, the logic is inverted. This may be useful to force horizontal text in tall tabs, or if the assumption that the text is wider than it is tall is incorrect.

* \setthumbtab{`PSA`}{\relax} - The special value `\relax` for the index-number will unset the thumb-tab for the given id (Psalms in this example), set by an earlier \setthumbtab command. To create blank thumb tabs, see below, this control entirely disables the tab, as if no `\setthumbtab` command had been given. It is intended for when a standard thumbtab file is used but there is no desire for a tab for a certain book in a speecific publication. E.g. In a publication of Psalms+NT, when the NT resets counting, it may be felt unnecessary or confusing to have a thumb-tab for the book of Psalms.

* \TOCthreetab```true``` - if false, then thumb-tabs will not have their content from  the `\toc3` entry. This will leave the tab blank unless set via the custom USFM marker ```\zthumbtab```. (default = true)


### Advanced use
* \def\ThumbTabStyle{```toc3```} - use specified marker for selecting the font, size, weight, etc.  (default = toc3)
 
* \NumTabs=```5``` - Pre-set / reset the number of tabs between which the available space will be divided. Normally there is no need to adjust this number, as ```\setthumbtab{ZEC}{39}``` will set it to 39 unless it is already larger than that. 

One valid use-case for manually setting \NumTabs is if index numbers reset to 1 between Old and New testaments. It may then be appropriate to include ```\NumTabs=27``` before Matthew is included, so that the NT tabs cover the same distance (in bigger steps). If it is set to one, then an error is likely. Setting it to zero disables all thumb-tabs.

Another use-case is to print tabs on what will be a multi-publication series, and just call \setthumbtab{}{} for the book 
being prepared at the moment.  However, in the case it might still be better to use the common-file approach.

**Warning** If this number is set below the index number for a given book, then that tab will go beyond the limits set for them or even off the page. 
Setting \NumTabs artificially high will mean that tabs are pushed to the upper portion of the page. If this is desired, however, it is normally more appropriate to alter `\TabsEnd`.

#### Individual tab settings
* \setthumbtabFg{`PSA`}{0 1 0.8} - Override the default foreground colour `\tabFontCol` for the given book.
* \setthumbtabBg{`REV`}{0.3 0.3 0} - Override the default background colour `\tabBoxCol` for the given book.


#### Control over position of text within the box
The box position is controlled as described as above. The controls below position the text within the box.

* \let\horizThumbtabContents=```\TabTxtCentred``` Override the normal placement rule for text in horizontally oriented tabs, in order that they be centred in the thumb tab.  (Options:`\TabTxtFarFromEdge`, `\TabTxtCentred`, `\TabTxtNearToEdge`). Default is `\TabTxtFarFromEdge`, putting the text far from the edge of the paper, to allow for  cropping errors.

* \let\vertThumbtabContents=```\TabTxtFarFromEdge``` Override the normal placement rule for text in vertically oriented tabs, in order that they not be positioned centrally in the box before being rotated. As in vertically oriented tabs the text is rotated so the bottom of letters are towards the page-edge, the example puts the text at the bottom of the thumb tab. Correspondingly, setting it to `\TabTxtNearToEdge` will put the text at the top of the thumbtab. (Options:`\TabTxtFarFromEdge`, `\TabTxtCentred`, `\TabTxtNearToEdge`). Default is `\TabTxtCentred`.

* \def\vertThumbtabVadj{```-3pt```} (default `-2pt`).
* \def\horizThumbtabVadj{```1sp```} (default `1sp`).
 Adjust the text 'vertically' (relative to normal text orientation) in a horizontally and  vertically aligned thumbtab. The value ```1sp``` is a special value instructing the code to centre the text vertically in the box (taking into account descenders and risers).  If the value is positive, this is the distance to raise the text above the box's baseline. If the value is negative, it indicates the distance from the top of the box to the top of the text. 


