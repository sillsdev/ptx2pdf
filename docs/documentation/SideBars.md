# Sidebars
Sidebars (`\esb`) are boxes of text (or other USFM elements). They act as miniature pages, which may have a background colour, and which may be transparent (allowing a whole-page background image or decoration to show through). They may also have
borders and their own watermark or background image, and a foreground image such as a logo that would further identify the type of information being presented (e.g. a scroll for historic notes, or a compass for geographical notes).

Although the USFM standard is silent on this matter, PTXprint allows sidebars to nest. This means that any element that the typesetter might want to have a background image, border, etc. can be expressed through a suitable sidebar. E.g. a white background for an ISBN barcode is best provided by a sidebar.

## Styling options for side bars
The USFM standard suggests `\esb \cat people\cat* ....`   to be the opening of  a sidebar. The styling is thus associated with a sub-category of `\esb`. Paratext does not appear to have a format for indicating such styling in the stylesheet, and PTXprint thus had to invent one:  
`\Marker cat:people|esb`  Most of this document discusses the styling optins for the sidebar. However, first the styling of paragraphs, etc. will be addressed:

##Styling markers within sidebars
A feature of sidebars is that it is normal for styling to be different inside them. E.g. font size may be smaller, the font face may be different, etc.
the stylesheet format for items within the stylesheet is to prefix them with the category prefix of the enclosing sidebar. i.e. `\Marker cat:people|p`

### Shorthand for formatting multiple paragraph/character styles.
PTXprint also defines the 'sidebar formatting group' format:
 `\Category people`, which is ended by `\EndCategory`
Opening the group both starts styling entries for `cat:people|esb` but also interprets any subsequent `\Marker p` entries as though they were prefixed with the category prefix for that sidebar. 

## Specific Sidebar layout and formatting

### Position
```
\Position option
```

* Options: `t`, `tl`, `tr`, `ti`, `to`,  `b`, `bl`, `br`, `bi`, `bo`, `h`, `p`, `F`, `P`  or `B`

Default: b
The position for this class of side-bars.  Any image position may be specified. For detail of the meaning, see the [Figures documentation](figures.md) 
`B` indicates that this box goes below any notes on the page (b normally comes above notes).

* As with images, `h`, `p`, `F` and `P` can all be further specified with a horizontal position (`l`, `r` or `c` for left, right, centre respectively).

* `F` and `P`  can also have a vertical position relative to the pages. The vertical positions 
that are shared with images are `t`, `b`, `c` for top, bottom, centre respectively. An additional 
'vertical position' that can be specified is 'f', for 'fill'. This calculates the space needed 
for borders and padding, and then tells TeX to expand the text contents to fill the page. This is 
very useful for cover-pages, etc., where the TeX command `\vfill` can be used provide stretch.

E.g.: `\Postion Fcf` will stretch the box vertically to occupy the entire paper, whereas `Position Fcc` will 
center the box on the page taking up as little space as possible.

Note that `h` and `p` sidebars, if they have  no background colour or images, and are not positioned 
horizontally
may be permitted to break across pages.
 
###Size 
`\Scale  value(0-1)`

* Default: 1

Width of the box relative to the nominal size of the containing column or box (like the scale="..." `\fig` parameter).

### Sidebar category logo
`\FgImage`   `picturename.jpg`

* Default: no image

Name of a foreground image.  The foreground image will appear in the defined place for all occurances of \esb boxes in this category.
Note that JPEG has no transparency, use PDF images for line art / transparent images above a coloured background.


\FgImagePos     option

* Options for above/below text: `t`  or `tc` (top, centre) , `tl` (top, left), `tr` (top, right), `ti` (top inner), `to` (top outer)  or `b_` (bottom...)
* Options for beside text: `sl` (side: left), `slt` (side: left, top), `slc` (side: left, centre) , `slb`  (side: left, bottom), `s_` (side: left/inner/outer, ...). 
* Options for interacting with text: `cl` (cutout left), `cl2` (cutout left, starting 2 lines below top), `c_` (cutout, left/inner/outer ...).
* Default: cl

The (default) cutout position leaves the least white-space. the `t` and `b` series of options position the image in a horizontal bar of space that is as tall as the image, the `s` series position the image in a vertical space as wide as the image, reducing the width as if the cutout continued the whole height of the side-bar.


`\FgImageScale`  value(0-1)
Width of the image relatve to the size of the size of the containing box.
Default: 0.2

### Background colour and image
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


`\BgImage`      
Background images are intended to form a water-mark or fancy border and are
horizontally and vertically centred, there is no ```\BgImagePos``` command. 

\BgImageScale  0.5
\BgImageScale  0.9x0.9
\BgImageScale  x0.7
Background Images can be scaled relative to the width of the box (top format), to both 
dimensions of the box, or only to the height (bottom format).

`\BgImageOversize` option

* Options: ignore shrink distort crop
* Default: ignore

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
a transparent background may display better above the colour layer, as the colour 
layer will not then wash them out, but .JPGs are probably better below, as .JPG images do not have transparency.

`\BgImageAlpha` value(0-1)

Transparency or alpha value of the background image: 0 is transparent, 1 is
solid. This is useful for e.g. turning black lines into a paler shade. Note that this 
will allow the background colour to show through, even if the image is above
the background layer, so on a green background black will become a darker
shade of green, not grey.

`\BgImageColor` value(0-1) value(0-1) value(0-1) 
`\BgImageColor` x7f7f7f
`\BgImageColour` value(0-1) value(0-1) value(0-1) 
`\BgImageColour` x7f7fef
Some (rare) PDF line-art images do not set the colour of their lines, relying
instead on the 'default' colour, which is normally black. This control sets the
default colour to something other than black, and thus such images can be
recoloured with this option. If (as most PDF images do) the image defines its
own colour, this option will have no visible effect at all. It is also possible
that an image will *partly* contain colour information, but only starting part
way through the file, a situation that might produce unexpected results.
Colours are either specified as 3 decimal numbers or as a hexadecimal number.
In both cases the sequence is Red, Green, Blue.

### Padding  the background
`\BoxLPadding` measurement
`\BoxRPadding` measurement
`\BoxTPadding` measurement
`\BoxBPadding` measurement

If a coloured background is used, this is how much that box should be larger than the enclosed text.
Measurement is interpreted as being in points (72.27pt = 1 inch), and should not have a unit attached.
Left, Right, Top and Bottom padding can be controlled separately, with historic/convenience  
single commands `\BoxHPadding`  and `\BoxVPadding` setting (respectively) both
Horizontal and Vertical parameters in a single command. 
All four dimensions can be set with `\BoxPadding`.


Related to box padding, the (global) TeX boolean control `\BoxLikeBordertrue`
(new default) and `\BoxLikeBorderfalse` (old default) determine how sidebars
with coloured backgrounds but no borders are treated. If `\BoxLikeBordertrue`
is set, then the presence of non-zero box-padding will do things like move
side-aligned text away from the page margin. If it is false, then the presence
of absence of a small amount of box padding will not normally affect
the positioning of text. (Though it may shift following text a line lower)

### Border-related Parameters

`\Border` options

 * Options: are one or more of these (separated by a space): None Top Bottom Left Right Inner Outer All

Which of the 4 possible borders will have a line.
Six internal flags: top, bottom, odd-left, even-left, odd-right, even-right
are set by these options which are processed in order.  (e.g. the flag for the
left border on odd pages will be altered by All, Left or Inner).
For 'Book opens on the left'  publications (Right-to-left languages, but complicated by diglots), the
inner/outer processing requires that `\BookOpenLefttrue` is specified before the category sheet is processed.

The option None clears all borders set until now. Thus:
`\Border All None Left`
 is the same as "\Border None Left". "\Border Left" will retain any previously set or inherited values,
 while adding a Left-hand border.
`\BorderWidth` measurement
Default: 0.5
Define the thickness of the border around the box, measured in pt.

`\BorderColour` value(0-1) value(0-1) value(0.1)
`\BorderColor` value(0-1) value(0-1) value(0.1)
`\BorderColour` x00ff00
`\BorderColor` x34ff12
 Default: 0 0 0 (Black)
The 3 values (0-1) for red, green and blue components of the (optional) border-line around the box 
Colours are either specified as 3 decimal numbers (0.0-1.0) or as a hexadecimal number.
In both cases the sequence is Red, Green, Blue.


`\BorderStyle` option

* Options: `plain`|`double`
* Options with plugin: `ornaments`
* Default: `plain`

Normal borders are of style `plain`. The style `double` is also available, which gives a border that has double-line. The `ornaments` 
plugin provides for more complex ornaments.

`\BorderFillColour` and `\BorderFillColor`
Certain border styles have a region or regions that can be filled, e.g. the space between the 2 lines of borderstyle `double`

`\BorderLineWidth` measurement
Where relevant (e.g. the `double` and `ornaments` border styles), this
determines the thickness of the lines that are used to draw the border.  Thus
in `double` style, there will be two lines of width equal to the specified
amount with a gap or filled region (see `\BorderFillColour`), and the *total*
width of the border will be `\BorderWidth`.


`\BorderTPadding` measurement
`\BorderBPadding` measurement
`\BorderLPadding` measurement
`\BorderRPadding` measurement
Default: 0

This measurement (in points) specifies how much further out the (inside) edge of
the border is from from the (outside) of the surrounded item (the nominal
coloured box, in the case of side-bars).
This can be negative in which case the border will overwrite the coloured box
(or text margins).

Left, Right, Top and Bottom can all be controlled separately. For historic / convenience reasons, 
multiple values can be set at once, with  `\BorderHPadding` `\BorderVPadding` each setting two 
measurements, and `\BorderPadding` setting all four.

### On-grid or off grid
`\SidebarGridding option`

* Options: `normal`, `smart`, `none`, `orig`.

* `orig` Attempts to preserve the original spacing, before this control was added. The only option that (always) obeys a heading's `BeforeSpace` at the start of the sidebar. It is therefore usually better than `normal` or `smart` for boxed headings or titles.
* `normal` treats the top of the sidebar like the top of the page (removing "wasted" space from SpaceBefore) and  (except for cutouts) adjusts the position of the final line of text so that it is on-grid.
* `none` disables all attempts to keep the text on-grid. Headings in the side-bar are spaced exactly according to their SpaceBefore and SpaceAfter controls, with none of the normal automatic grid correction. The exception to this is that SpaceBefore is normally ignored at the top of the sidebar. Setting the global boolean `\SidebarGriddingNoneKeepSpaceBeforetrue` means that the SpaceBefore value is never discarded at the top of the sidebar. The boolean is locally set for in the code that automatically starts `titlebox` and `headingsbox` sidebars when they are enabled, meaning this option may be a good choice for those styles.
* `smart` puts the final line of text on-grid like `normal` if the sidebar is an integer number of baselines high (i.e. the body paragraphs are all set with `LineSpacing 1`, but does not otherwise.

The considerations in selecting the best option are as follows:

* For existing publications, any changes might cause problems - use `orig` in this case.
* Sidebars in cutouts should probably use `none`.
* (Long) sidebars that use the standard baseline should be expected to keep back-to-back registration, for clarity on thin paper. Use `normal` or `orig`
* For sidebars that always use a non-standard baseline, registration is a non-issue, and it may be preferable to select `none`.
* For very short sidebars, back-to-back registration is less of an issue.
* For sidebar styles that occasionally contain paragraph styles with unusual baselines, but often tend towards being long, `smart`  is probably to be prefered.
* `normal` or `orig` should be used if the paragraphs use the standard baseline but the sidebar often starts with rules, `\b` or `\zgap`   that would cause `smart` to ignore gridding.
* For the automatic titlebox and headingsbox sidebars,  only `orig` and `none` obey the heading-style's `SpaceBefore` parameter, which may be a significant decision factor.

#### Comparison of options with normal and shrunk linespace

| Option | Result with linespacing of 1| Result with linespacing of 0.9|
| -- | -- | -- |
| `orig`| ![](imgs/on_SidebarGridding-orig.png) |![](imgs/off_SidebarGridding-orig.png "SidebarGridding orig") |
| `normal`| ![](imgs/on_SidebarGridding-normal.png) |![](imgs/off_SidebarGridding-normal.png "SidebarGridding normal") |
| `smart`| ![](imgs/on_SidebarGridding-smart.png) |![](imgs/off_SidebarGridding-smart.png "SidebarGridding smart") |
| `none`| ![](imgs/on_SidebarGridding-none.png) |![](imgs/off_SidebarGridding-none.png "SidebarGridding none") |


The above show that using `smart` reduces the space used on the page by a line in this case. `none` further affects the space used, by altering the internal layout within the sidebar, but it the issue of lost back-to-back registration means that it is probably unsuitable for longer sidebars.

Note: all of the comparisons above used `\XeTeXuseglyphmetrics=1` and a `BorderPadding` of 1. Not making use of glyph-based metrics would have caused a noticable increase in the spacing.

#### Comparison of headingsbox 

| Option | Result|
| -- | -- |
|  `normal`|  ![ ](./imgs/headingsbox-normal.jpg  "SidebarGridding normal") |
|  `smart`|  ![ ](imgs/headingsbox-smart.jpg  "SidebarGridding smart") |
|  `orig`: | ![ ](imgs/headingsbox-orig.jpg  "SidebarGridding orig") |
|  `none` | ![ ](imgs/headingsbox-none.jpg  "SidebarGridding none") |

The above were all created using `\s1` with `\SpaceBefore 4` and `\SpaceAfter 4`, and these sidebar settings:
```
\Marker cat:headingsbox|esb
\TextProperties publishable
\SidebarGridding normal
\BorderWidth 4
\BorderPadding 1
\BoxPadding 0
\BorderStyle ornaments
\BorderRef  Han4
\BorderFillColour .5 .5 .5
\BgColor 0.50 0.50 0
```
### Other options
`\Breakable option`   **!!!DO NOT USE!!!**

*  Options: T, F, value(0-1)
*  Default: F
*  Incompatible with: Background images.

Should the contents of this box be forced to be on one page or can it be broken? (Not compatible with background images)
With a background colour, the box will be broken into sections and these sections will be added one chunk at a time. Descenders 
may be lost at these joints if a non-transparent background colour is given.

If a value is given, rather than a simple 't', this is the smallest fraction of the pageheight that the sections will be, if 't' is given, the fraction 
will be 0.2 of the page height. If splitting a given chunk of the box is impossible, the algorithm will increase the chunk-size until 
 a break IS possible. 

*NB:* Breakable in out-of-body positions triggers a bug in the page output
mechanism and *things go  horribly wrong* if this option is used.

## Ending the category

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


