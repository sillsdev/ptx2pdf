% A Work-in-progress, and aspirational document. I.e. this may change, and no features are at present guaranteed to be present!
% 
# Styling for side bars

```\esb```  boxes may have a colour, which may be transparent (allowing a
whole-page background image or decoration to show through). They may also have
their own watermark or background image.

```

\Category people
% The identifier of this category. This command imposes default values on parameters.
% Subsequent modifications to a style should be done using the alternative format

\Marker cat:people|esb


%\Position option
% Options: t, tl, tr, ti, to,  b, bl, br, bi, bo, h, p, F, P  and B
% Default: bl
% I.e. any image position may be specified. 
% B indicates that this box goes below any notes on the page (b normally comes above notes).
% 
%\Scale  value(0-1)
% Default: 1
% Width of the box relative to the nominal size of the containing box.

%\Breakable option   !!!DO NOT USE
% Options: T, F, value(0-1)
% Default: F
% Should the contents of this box be forced to be on one page or can it be broken? (Not compatible with background images)
% With a background colour, the box will be broken into sections and these sections will be added one chunk at a time.
% If a value is given, this is the smallest fraction of the pageheight that the sections will be, if 't' is given, the fraction 
% will be 0.2 of the page height. If splitting a given chunk of the box is impossible, the algorithm will increase the chunk-size until 
% a break IS possible. 
% NB: Breakable triggers a bug in the page output mechanism and things go gets things horribly wrong

%\BgColour F, T, value(0-1) value(0-1) value(0.1)
% Disable (F) or reenable (T)  any background colour set earlier (or inherited) 
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
% Default: 0.5
% Define the thickness of the border-line around the box, Measured in FontSizeUnits (normal text is 12 FontSizeUnits)

%\BorderColour value(0-1) value(0-1) value(0.1)
%\BorderColor value(0-1) value(0-1) value(0.1)
% Default: 0 0 0 (Black)
%3 values (0-1) for red, green and blue components of the border-line arount the box

%\Border options
% Options are one or more of these (separated by a space): None Top Bottom Left Right Inner Outer All
% Which of the 4 possible borders will have a line.
% Six internal flags are set by these options which are processed in order.
% (e.g. the flag for the left border on odd pages will be altered by
% All, Left or Inner).
% For 'Book opens on the left'  publications (Right-to-left languages, but complicated by diglots), the
% inner/outer processing requires that \BookOpenLefttrue is specified before
% the category sheet is processed.
%
% The opion None clears all borders set until now. Thus:
%   \Border All None Left
% is the same as "\Border None Left". "\Border Left" will retain any previously set or inherited values,
% While adding a Left-hand border.

%\EndCategory
% Cancels the current category (sets the value to empty). This is used
% internally, before and after the categorysheet is defined and is not 
% necesary if the stylesheet is loaded by \categorysheet.
% Placing it in a categorysheet file means that until the next \Category,
% any stylesheet commands behave as though in a normal stylesheet, and options given 
% above file will apply to \esb boxes without a specified category.
```

## Thoughts

- Do we need  a special `\categorysheet` command? The real deal is the `\Category` command that turns on the goodies.

- Might we add some border options?
DG reply: Yes. Some done, please criticise. As above, I'm imagining \vrules just outside the box, 
reducing the box size by the appropriate line width(s).

DG qn: At present, the default-setting code that gets called by \Category means
that there's no sane way to have a secondary categorysheet that overrides some
previously defined values. Might that be a feature someone would want?

TODO:
1) boxes
2) FGfigures
3) BGfigures
4) Refactor so that the one-time setup only gets triggered once.
```
