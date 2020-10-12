# Category file

```\categorysheet{filename}```

A category file is an extended stylesheet format that defines the properties of zero or more categories  of ```\esb```  extended study matter panels (or boxes).
http://ubs-icap.org/chm/usfm/3.0/notes_study/categories.html
While ```\stylesheet``` may fail to crash when given a category file, results will be unexpected, as ```\stylesheet``` does not cancel categories 
at start or exit.
For convenience, a category file MAY also define paragraph / character styling that will be applied  to the box content. Markers within such a 
category block / file do not need any special naming sequence, this is done automatically.

A method for defining paragraph / character styling outside of a category sheet manually (```\Marker category:people:p``` etc) or via a 
normal stylesheet files also exists:

\StyleCategory{People}{
 \stylesheetL{people-styles-romIntl.sty} % styles for International Rromani Alphabet
 \stylesheetR{people-styles-rmyRo.sty} % styles for Romanian-spelling Vlax Romani 
}


Categories may, according to USFM-3.0 standards, be applied to other types of material, e.g. footnotes, in which case they apply the 
only the relevant paragraph and character styling. 

```\esb```  boxes may have a colour, which may be transparent (allowing a whole-page background image or decoration to show through). They 
may also have their own watermark or background image.
```
% A Work-in-progress, and aspirational document. I.e. this may change, and no features are at present guaranteed to be present!
% 
% This file might eventually become the standard template for a category file
% The format is single much like that of a stylesheet.

\Category people
% The identifier of this category. This command also imposes default values on parameters.

%\Position option
% Options: t, tl, tr, ti, to,  b, bl, br, bi, bo, h, p, F, P  and B
% Default: bl
% I.e. any image position may be specified. 
% B indicates that this box goes below any notes on the page (b normally comes above notes).
% 
%\Scale  value(0-1)
% Default: 1
% Width of the box relative to the nominal size of the containing box.

%\Breakable option
% Options: t, f
% Default: f
% Should the contents of this box be forced to be on one page or can it be broken?

%\BgColour value(0-1) value(0-1) value(0.1)
% 3 values (0-1) for red, green and blue. With \Alpha below, this defines the colour of the \esb box
% Note that by default an \esb box has no background colour, so not setting a value here is not the same as setting a value to white. 
% Setting this to white will overwrite any background image. (For Americans, \BgColor is an acceptable alias).

%\Alpha value(0-1)
% The transparency or alpha value of the background colour: 0 is transparent, 1 is solid.

%\FgImage        picturename.jpg
% Default: no image
% Name of a foreground image.  The foreground image will appear in the defined place for all occurances of \esb boxes in this category.
% Note that JPEG has no transparency, use PDF images for line art / transparent images above a coloured background.

%\FgImagePos     option
% Options: any valid pgpos, plus: sl, sr, si, so
% Default: cl
% t and b are reinterpreted to mean the top and bottom of the box. Other out-of line image formats are invalid.  
% sl and sr position the image to one side of the text, without the text  returning to normal size after the image as would happen with a cutout.

%\FgImageScale  value(0-1)
% Width of the image relatve to the size of the size of the containing box.
% Default: 0.2

%\BgImage      
%\BgImageScale   
% The same meanings as the Fg images, but for a background (watermark) image. 
% Background images are horizontally and vertically centred, there is no \BgImagePos command.

%\BgImageLow option
% Options: t,f
% Should a background image come below or above the colour. Line art PDFs may
% display better above the colour layer, as the colour layer will not wash them
% out, but .JPGs are probably better below.

%\BorderWidth measurement
% Default: 0.5pt
% Define the thickness of the border-line around the box

%\BorderColour value(0-1) value(0-1) value(0.1)
% Default: 0 0 0 (Black)
%3 values (0-1) for red, green and blue components of the border-line arount the box

%\BorderTop option
%\BorderBottom option
%\BorderLeft option
%\BorderRight option
%\BorderInner option
%\BorderOuter option
%\BorderAll option
% Options: t,f
% Default: \BorderAll t
% Which of the 4 possible borders will have a line.
% Six internal flags are set by these options which are processed in order.
% (e.g. the flag for the left border on odd pages will be altered by
% \BorderAll, \BorderLeft or \BorderInner) For 'Book opens on the left'
% publications (Right-to-left languages, but complicated by diglots), the
% inner/outer processing requires that \BookOpenLefttrue is specified before
% the category sheet is processed.


%\EndCategory
% Cancels the current category (sets the value to empty). This is used
% internally, before and after the categorysheet is defined and is not normally
% necesary. Placing it in a categorysheet file means that until the next \Category,
% any stylesheet commands behave as though in a normal stylesheet, and options given 
% above file apply to \esb boxes without a specified category.
```

## Thoughts
- I would suggest a different separator between the category and the marker. How about `|` or `:`. I can see ```_``` being popular in user markers.
DG reply:  Accepted, how about ```category:people:p```, ```category:history:p```, etc?

- I suggest we add `\Marker` support within a `\category` block, without needing to use the separator. This allows us to change the separator if things go wrong.
DG reply: This is meant to be what the document says.  Manually including the separator is for `\Marker` support outside the `\categorysheet` file.

- Do we need  a special `\categorysheet` command? The real deal is the `\Category` command that turns on the goodies.

DG reply: I thought about this qn. `\categorysheet` is a convenience function that calls \CategoryEnd before and after processing. Without that, 
once `\c@tegory` is set will remain in effect, I guess  until the first
`\ptxfile`. I want that feature (`\stylesheet` not cancelling categories), so
that for categorised footnote styling, (etc?) this sort of approach is permitted:

```
\StyleCategory{People}{
 \stylesheetL{people-styles-romIntl.sty} % styles for International Rromani Alphabet
 \stylesheetR{people-styles-rmyRo.sty} % styles for Romanian-spelling Vlax Romani 
}
```

- Might we add some border options?
DG reply: Yes. Some done, please criticise. As above, I'm imagining \vrules just outside the box, 
reducing the box size by the appropriate line width(s).

DG qn: At present, the default-setting code that gets called by \Category means
that there's no sane way to have a secondary categorysheet that overrides some
previously defined values. Might that be a feature someone would want?

