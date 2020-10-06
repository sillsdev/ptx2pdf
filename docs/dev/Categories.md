# Category file

```\categorysheet{filename}```

A category file is an extended stylesheet format that defines the properties of zero or more categories  of ```\esb```  extended study matter panels (or boxes).
While ```\stylesheet``` may fail to crash when given a category file, results will be unexpected.
For convenience, a category file MAY also define paragraph / character styling that will be applied  to the box content,
but another method for defining these (```\Marker category_p``` etc) (will) also exist.

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
% The identifier of this category

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
% Setting this to white will overwrite any background image.

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

%\BgImage      
%\BgImageScale   
% The same meanings as the Fg images, but for a background (watermark) image. 
% Background images are horizontally and vertically centred, there is no \BgImagePos command.

%\BgImageLow option
% Options: t,f
% Should a background image come below or above the colour. Line art PDFs may
% display better above the colour layer, as the colour layer will not wash them
% out, but .JPGs are probably better below.

%\EndCategory
% Cancels the current category (sets the value to empty). This is used
% internally, before and after the categorysheet is defined and is not normally
% necesary. Placing it in a categorysheet file means that until the next \Category,
% any stylesheet commands behave as though in a normal stylesheet, and options given 
% above file apply to \esb boxes without a specified category.
```
