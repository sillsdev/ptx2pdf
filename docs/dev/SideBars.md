% A Work-in-progress, and aspirational document. I.e. this may change, and no features are at present guaranteed to be present!
% 
# Styling for side bars

```\esb```  boxes may have a colour, which may be transparent (allowing a
whole-page background image or decoration to show through). They may also have
their own watermark or background image, and a foreground image such as a logo 
that would further identify the type of information being presented (e.g. a scroll for 
historic notes, or a map for geographical notes).
```

```\Category people```
The identifier of this category. This command imposes default values on parameters.
Subsequent modifications to a style should be done using the alternative format:

```\Marker cat:people|esb```


```\Position option```
* Options: `t`, `tl`, `tr`, `ti`, `to`,  `b`, `bl`, `br`, `bi`, `bo`, `h`, `p`, `F`, `P`  or `B`
* Default: bl
The position for this class of side-bars.  Any image position may be specified. 
`B` indicates that this box goes below any notes on the page (b normally comes above notes).
 
```\Scale  value(0-1)```
* Default: 1
Width of the box relative to the nominal size of the containing box.

`\Breakable option`   *!!!DO NOT USE!!!*
*  Options: T, F, value(0-1)
*  Default: F
*  Incompatible with: Background images; Alpha.
Should the contents of this box be forced to be on one page or can it be broken? (Not compatible with background images)
With a background colour, the box will be broken into sections and these sections will be added one chunk at a time.
If a value is given, this is the smallest fraction of the pageheight that the sections will be, if 't' is given, the fraction 
will be 0.2 of the page height. If splitting a given chunk of the box is impossible, the algorithm will increase the chunk-size until 
 a break IS possible. 

*NB:* Breakable triggers a bug in the page output mechanism and *things go  horribly wrong* if this option is used.

`\BgColour option` 
`\BgColor option` 
* Option: `F`, `T`, `value`(0-1) `value`(0-1) `value`(0.1)
Disable (F) or reenable (T)  any background colour set earlier (or inherited). Alternatively 
3 values (0-1) for red, green and blue may be specified.

With `\Alpha` below, this defines the colour of the \esb box.
Note that by default an \esb box has no background colour, so not setting a value here is
not the same as setting a value to white. 
Setting this to white will overwrite any background image. (For Americans, \BgColor is an acceptable alias).

`\Alpha` value(0-1)
* Incompatible with: Breakable.
The transparency or alpha value of the background colour: 0 is transparent, 1 is solid. While tempting, purpose of alpha is not
to obtain pastel colours, but to allow a background colour to be used in conjunction with a background image. Using `\Alpha`
with `\Breakable` is a usage error, that produces ugly stripes where the chunks overlap due to descenders (the amount  of p or q).

`\FgImage`   `picturename.jpg`
* Default: no image
Name of a foreground image.  The foreground image will appear in the defined place for all occurances of \esb boxes in this category.
Note that JPEG has no transparency, use PDF images for line art / transparent images above a coloured background.


\FgImagePos     option
* Options for above/below text: `t`  or `tc` (top, centre) , `tl` (top, left), `tr` (top, right), `ti` (top inner), `to` (top outer)  or `b_` (bottom...)
* Options for beside text: `sl` (side: left), `slt` (side: left, top), `slc` (side: left, centre) , `slb`  (side: left, bottom), `s_` (side: left/inner/outer, ...). 
* Options for interacting with text: `cl` (cutout left), `cl2` (cutout left, starting 2 lines below top), `c_` (cutout, left/inner/outer ...).
* Default: cl

The (default) cutout position leaves the least white-space. the `t` and `b` series of options position the image in a horizontal bar of space that is as tall as the image, the `s` series position the image in a vertical space as wide as the image, reducing the width as if the a cutout continued the whole height of the side-bar.


`\FgImageScale`  value(0-1)
Width of the image relatve to the size of the size of the containing box.
Default: 0.2

`\BgImage`      
Background images are intended to form a water-mark or fancy border and are
horizontally and vertically centred, there is no ```\BgImagePos``` command. 

\BgImageScale  0.5
\BgImageScale  0.9x0.9
\BgImageScale  x0.7
Background Images can be scaled relative to the width of the box (top format), to both 
dimensions of the box, or only to the height (bottom format).

`\BgImageOversize` option
Options: ignore shrink distort crop
Default: ignore
If the background image size is specified with a single dimension (height or
width) and the unspecified dimension ends up being too large for a given
sidebar then there are four possible behaviours:
 * Ignore the problem, allowing the image to appear outside the box [current behaviour]
 * Shrink the image without distorting the image's aspect ratio [planned]
 * Shrink the image in the over-sized dimension, distorting the aspect ratio [planned]
 * Crop the edges of the image [may be possible eventually]

`\BgImageLow`  option
* Options: `t`, `f`
* Default: `t`
Only relevant where there is both a background image *and* a background colour, this defines 
the order they are put on the page.  Should a background image come below or above the colour. Line art PDFs with
a tranpsarent background may display better above the colour layer, as the colour 
layer will not then wash them out, but .JPGs are probably better below, as .JPG images do not have transparency.

```\BgImageAlpha`` value(0-1)
Transparency or alpha value of the background image: 0 is transparent, 1 is
solid. This is useful for e.g. turning black lines into a paler shade. Note that this 
will allow the background colour to show through, even if the image is above
the background layer, so on a green background black will become a darker
shade of green, not grey.

`\BgImageColor` value(0-1) value(0-1) value(0-1) 
`\BgImageColour` value(0-1) value(0-1) value(0-1) 
Some (rare) PDF line-art images do not set the colour of their lines, relying
instead on the 'default' colour, which is normally black. This control sets the
default colour to something other than black, and thus such images can be
recoloured with this option. If (as most PDF images do) the image defines its
own colour, this option will have no visible effect at all. It is also possible
that an image will *partly* contain colour information, but only starting part
way through the file, a situation that might produce unexpected results.

`\BorderWidth` measurement
Default: 0.5
Define the thickness of the border-line around the box, measured in FontSizeUnits (unless extensive stylesheet 
modification has been done, normal body text is 12 FontSizeUnits.

`\BorderColour` value(0-1) value(0-1) value(0.1)
`\BorderColor` value(0-1) value(0-1) value(0.1)
` Default: 0 0 0 (Black)
The 3 values (0-1) for red, green and blue components of the border-line arount the box [*Unimplemented*]

`\Border` options
* Options: are one or more of these (separated by a space): None Top Bottom Left Right Inner Outer All
Which of the 4 possible borders will have a line.
Six internal flags: top, bottom, odd-left, even-left, odd-right, even-right
are set by these options which are processed in order.  (e.g. the flag for the
left border on odd pages will be altered by All, Left or Inner).
For 'Book opens on the left'  publications (Right-to-left languages, but complicated by diglots), the
inner/outer processing requires that `\BookOpenLefttrue` is specified before the category sheet is processed.

The opion None clears all borders set until now. Thus:
`\Border All None Left`
 is the same as "\Border None Left". "\Border Left" will retain any previously set or inherited values,
 while adding a Left-hand border.

`\EndCategory`
Cancels the current category (sets the value to empty). 
Placing `\EndCategory` in a categorysheet file means that until the next \Category,
any stylesheet commands will behave as though in a normal stylesheet, and any category 
options listed above  will apply to \esb boxes without a specified category.

If the stylesheet is loaded by `\categorysheet`, then is used internally,
before and after the categorysheet is read, and is not normally necesary.

The `\stylesheet` command should issues a warning if `\Category` is used without an
`\EndCategory` command towards the end of the file. However, there is no need to place
`\EndCategory` before a `\Category` instruction, as no formal grouping occurs.

The `\StyleCategory` command assumes that the styling fragments contain neither 
`\Category` nor `\EndCategory` 


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
