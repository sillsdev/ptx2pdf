# 13. Styles tab

## 13.1 What this tab is for

Your Paratext text uses **markers** to say what each piece of text is. A marker is a short code that starts with a backslash. For example, `\p` starts a normal paragraph, `\s1` is a section heading, `\v` is a verse number, `\f` is a footnote and `\nd` is the name of God ("LORD"). These are called **USFM markers**.

A **style** is the set of formatting rules for one marker: font, size, bold or italic, colour, indents, alignment and the space above and below. The list of all styles is a **stylesheet**. The **Styles** tab is the style editor. Use it to change how one kind of text looks everywhere, for example "make all section headings bigger", "make verse numbers red", "put more space above the headings" or "do not print the `\rem` remarks".

The tab is only shown in the **Regular** and **Full** views (see the chapter about the main window). If the whole tab is greyed out, **Lock UI Layout Settings** on the **Advanced** tab is ticked; untick it to make changes.

Many other tabs have small blue links with a marker name (for example next to the verse number or heading settings). Click one to jump straight to that marker on the **Styles** tab. The tab label moves a little to show you where you are.

Changes show in the PDF only after you click **Print (Make PDF)** again. Style changes are saved with the current configuration.

## 13.2 The marker list

The left side lists all markers, grouped into categories such as **Chapters & Verses**, **Paragraphs**, **Poetry**, **Titles & Headings**, **Footnotes**, **Cross References**, **Character Styling** and **Peripheral Materials** (category names in bold blue). Click the small arrow beside a category to open it. Click a marker to show its settings on the right.

Each line shows the marker code and a short name, for example `s1 - Heading - Section Level 1`. A marker drawn with a line through it is not printed (see **Include Contents of Marker**).

To find a marker quickly, use the **Find** box or the filter button next to it (see the control notes). The filter makes the list much shorter.

Some markers have numbered levels, for example `\s1`, `\s2` or `\q1`, `\q2`. Selecting the plain marker (`s` or `q`) edits level 1 (`s1` or `q1`). Each level has its own style: a change to `\s1` does not change `\s2`.

Below the marker name and description are these buttons:

* **Add** – make a new style as a copy of the selected style.
* **Del** – delete a style that you added yourself.
* Reset (circular-arrows icon) – remove all your changes to the selected style. Greyed out for styles that you added yourself.
* **Edit** – change the name, description, type and end marker.
* **More Info...** – open the USFM documentation page for this marker on the internet. Only shown in the **Full** view, and only when **Disable ALL Internet Use** on the **Advanced** tab is not ticked.

## 13.3 Bold setting names: what has changed

PTXprint reads several stylesheets in order. Later ones override earlier ones:

1. The standard Paratext stylesheet (you cannot change it).
2. PTXprint's own additions (you cannot change them).
3. The project's `custom.sty`, if there is one. It can be edited from the **Advanced** tab. It also affects how Paratext shows the text.
4. Your changes on this **Styles** tab, saved with the configuration.
5. `ptxprint-mods.sty`, if there is one. It can be edited from the **Advanced** tab. Because it comes last, it wins over everything else.

A setting name in **bold** (for example **Font Size Factor**) means you changed this value on the **Styles** tab, so it differs from the stylesheets underneath. Click the bold name to go back to the original value of that one setting. Click Reset to remove all your changes to the style.

Hover over **Why are some parameters bold?** and **How are Stylesheets applied?** at the bottom of the tab for a short reminder.

## 13.4 Include Contents of Marker

Untick it to leave the text of this marker out of the PDF. The marker then has a line through it in the list, and its other settings are greyed out. The text stays in your Paratext project; only the PDF changes.

Some markers, such as `\rem` (remarks) or the identification lines, are not printed by default. Tick this box for them if you want them in the PDF.

The automatic boxes around headings and titles (`cat:headingsbox|esb`, `cat:titlebox|esb`) and the text border (`textborder`) also use this setting. Normally you turn these on from the **Tabs+Borders** tab, which ticks this box for you.

## 13.5 Character Settings

This area controls how the letters look.

* **Select Font...** – a different font for this marker only; otherwise the main font from the **Fonts+Script** tab is used. Beside it PTXprint shows the real size in points (pt – one point is about 0.35 mm) and any font changes such as Graphite, stretch, faux bold or slant.
* **Font Size Factor** – size compared with the **Base Font Size** on the **Layout** tab: 1.2 is 20% bigger, 0.8 is 20% smaller.
* **Scale Relative to Parent** – the size box becomes **Font Scale**, relative to the surrounding text instead of the base font size.
* **Bold**, **Italic**, **SmallCaps**, **Superscript** and **Underline**.
* **Raise** – moves the text up (or down, with a minus number) in points. Greyed out when **Superscript** is ticked, because superscript sets its own size and raise.
* **Color** – the text colour.

For `\p`, **Font Size Factor**, **Line Spacing Factor** and **Use Absolute Spacing** are greyed out. Set the main text size and line spacing on the **Layout** tab (**Base Font Size** and **Base Line Spacing**).

For a character marker (one that styles a few words inside a paragraph, like `\nd` or `\wj`), PTXprint opens only **Character Settings**. For paragraph markers it also opens **Paragraph Settings**. Click an area's title to open or close it yourself.

## 13.6 Paragraph Settings

This area controls the shape of the paragraph.

* **Alignment** – **Justified** (both edges straight), **Left**, **LeftBal**, **Center**, **Right**, **Inner** or **Outer**. **LeftBal** is left-aligned, but PTXprint also tries to make the lines, including the last line, more even in length. **Inner** and **Outer** are mainly for margin notes, cross-references in the margin and headings. For right-to-left scripts, Left and Right are swapped.
* **First Line Indent Factor**, **Left Indent Factor**, **Right Indent Factor** – multiples of the **Base Indent** on the **Layout** tab. A negative first line indent makes a "hanging" indent: the first line starts further left than the others. Poetry and list markers often use this.
* **Line Spacing Factor** – compared with the base line spacing. **Use Absolute Spacing (in pts)** gives an exact number of points instead; the label changes to **Baseline** and PTXprint converts the number.
* **Space Before Factor**, **Space After Factor** – extra space above and below, as a multiple of the base line spacing. 1.0 is about one empty line, 0.5 about half a line.
* **Maximum Ragged Space** – for non-justified paragraphs, how much of the line may stay empty at the ragged edge.

## 13.7 Other Settings

Settings used only by some markers. PTXprint opens the part that fits the selected marker.

* **Note Settings** (footnotes `\f`, cross-references `\x` and similar): style and raise of the caller (the small letter or symbol in the text and at the start of the note), and **Note Blend Into**, which puts these notes together with another kind of note.
* **Table Settings** (table cells `\tc`): where text sits from top to bottom when the cells in a row have different heights.
* **Sidebar Settings** (sidebar categories and the text border): see the next section.

## 13.8 Sidebars

A **sidebar** is a box of extra text, separate from the Scripture text, for example a study note about a place or a person. In USFM it starts with `\esb`, then a category such as `\cat people\cat*`, and ends with `\esbe`. All sidebars with the same category share one style; for "people" the marker name is `cat:people|esb`. PTXprint also uses sidebar styles itself, for example for the parts of the cover, the automatic boxes around headings and titles, and `cat:box|esb` for simple boxes.

Selecting a sidebar style opens **Sidebar Settings**:

* **Color** and **Alpha** – background colour of the box and how solid it is.
* **Width** – width of the box compared with the column or page.
* **Borders...** – the **Border Settings** dialog (see the **Tabs+Borders** chapter).
* **Foreground Image...** – a small picture (a logo) in each box of this category. See **Sidebar Image Settings** below.
* **Background Image...** – a picture behind the text of the box, like a watermark.
* **Size and Position...** – where the box goes on the page, shown as a short code beside the button.

The text inside a sidebar can have its own styles. For example, paragraphs inside "people" sidebars use `cat:people|p`. If such a style exists, change it like any other style; if not, you can add it (see **Common tasks**).

## 13.9 Size and Position Settings (dialog)

Opens from **Size and Position...** in **Sidebar Settings**. (The same dialog is used for maps on the **Pictures** tab.) A small picture shows roughly where the box will go.

1. Choose the **Frame Size** first: **Column Width**, **Span Width** (across all columns), **Page (in Margins)** or **Page (to Edge)**.
2. Then the **Vertical Position**. The choices depend on the frame size:
   * Column width: **Top**, **Bottom**, **Before Verse**, **After Paragraph** or **Cutout**.
   * Span width: **Top**, **Bottom** or **Below Notes**.
   * Page sizes: **Top**, **Center**, **Fill** or **Bottom**.
3. Then the **Horizontal Position**. **Center** is only offered for page sizes and for **Before Verse** and **After Paragraph**. For **Span Width** this list is greyed out.
4. For **After Paragraph** and **Cutout** you can set **Number of Lines** (for After Paragraph it becomes "Number of paragraphs").

Click **OK** to save.

A **cutout** is a notch in the text: the text flows around the box at the side of the column.

## 13.10 Sidebar Image Settings (dialog)

Opens from **Foreground Image...** or **Background Image...**; the title shows which.

* **Select...** chooses the image. PDF line art works best over a coloured background, because .jpg images cannot be transparent.
* **Scale** is the size compared with the box. **Maintain Aspect Ratio** keeps the picture's shape (height follows width).
* For a foreground image, choose **Above or Below Text**, **Beside Text** or **Cutout Within Text**, then the exact place in the list beside it.
* For a background image, **Background Image Advanced Settings** set transparency, layer order, what happens if it is too big, and which part of the box it fills.
* To take the image away, click **Remove Image**, then **OK**.

## 13.11 Add/Edit Style (dialog)

Opens from **Add** or **Edit**. It describes a marker: code, name, description, type and end marker. The formatting itself is then set on the **Styles** tab as usual. Creating markers is an advanced task. Most users only need it for special markers their project already uses (for example markers starting with `z`), or for cases such as a sidebar category.

* **Add**: the new style is a copy of the selected style, with all its settings, also ones not shown on the **Styles** tab, such as the border and padding of a sidebar (box) style. Only marker, name, description, type and end marker come from the dialog. So select a similar marker first.
* **Edit**: the **Marker** box is greyed out (a marker cannot be renamed). For standard USFM markers **Type** is also greyed out.
* **Name** controls where the marker appears in the list, for example `zpeople - Paragraph - Paragraph about people` goes into **Paragraphs**.

## 13.12 Common tasks

### Find the style for some text

1. If you do not know the marker, look at the text in Paratext with the "Unformatted" view, or on the **View+Edit** tab, to see which marker is in front of it.
2. On the **Styles** tab, type the marker code (for example `s1`) or a word (for example `heading`) in **Find**.
3. Or click the filter button to see only the markers used in your books.

### Make section headings bigger and bold

1. Type `s1` in **Find**.
2. In **Character Settings**, change **Font Size Factor**, for example from 1.0 to 1.2.
3. Tick **Bold**.
4. Click **Print (Make PDF)**.

### Put more space above and below headings

1. Select the heading marker (for example `s1`).
2. In **Paragraph Settings**, increase **Space Before Factor** (for example to 1.0) and **Space After Factor** (for example to 0.5).
3. Print again and check.

### Change the colour of verse numbers

1. Select the marker `v` (in **Chapters & Verses**).
2. Click the colour button next to **Color** and choose a colour.
3. PTXprint ticks **Enable Colored Text** on the **Fonts+Script** tab for you. Keep it ticked, or the colour will not print.

### Use a different font for one kind of text

1. Select the marker, for example `nd` (name of God).
2. Click **Select Font...** and choose the font and face.
3. To go back to the main font, click the bold **Font** label.

### Center a paragraph or change its indent

1. Select the marker (for example `pc`, or `q1` for poetry).
2. In **Paragraph Settings**, choose an **Alignment**, for example **Center**.
3. Change **First Line Indent Factor** or **Left Indent Factor** if needed.

### Leave some text out of the PDF

1. Select the marker, for example `rem` or a study-note marker.
2. Untick **Include Contents of Marker**. The marker now has a line through it.
3. Print again.

### Undo changes to a style

* One setting: click its bold name.
* All changes: click Reset. (For a style that you added yourself, Reset is greyed out. Change the settings back by hand, or delete the style with **Del**.)

### Give a sidebar category a coloured background

1. Find the style for the category, for example type `esb` in **Find**. If your category (for example "people") has no style yet, select `cat:box|esb`, click **Add**, type `cat:people|esb` in **Marker**, give it a **Name** and click **OK**.
2. In **Other Settings › Sidebar Settings**, click **Color** and choose a light colour. Set **Alpha** (for example 0.5).
3. Click **Size and Position...** to choose where the box goes, and **Borders...** for a border.
4. Print again.

## 13.13 Common problems

**My change on the Styles tab has no effect.**
* You may have changed the wrong marker. Check which marker the text really uses (for example `\s2` instead of `\s1`, or `\q2` instead of `\q1`).
* A more specific style may win. For example, `cat:people|p` is used for paragraphs inside "people" sidebars instead of `p`.
* `ptxprint-mods.sty` (edited from the **Advanced** tab) is applied last and may set the same value.
* You did not print again.

**The Font Size Factor and Line Spacing boxes are greyed out.**
You have selected `\p`. Change **Base Font Size** and **Base Line Spacing** on the **Layout** tab.

**The whole Styles tab is greyed out.**
Untick **Lock UI Layout Settings** on the **Advanced** tab.

**I cannot see the Styles tab.**
It is hidden in the **Mini** and **Basic** views. Change to **Regular** or **Full**.

**I set a colour, but the text is still black.**
Tick **Enable Colored Text** on the **Fonts+Script** tab.

**I chose Justified, but the text is not justified.**
**Justify Paragraphs** on the **Body** tab is not ticked, so **Justified** is treated as **Left**.

**Some text is in the wrong font.**
The style for that marker has its own font (its **Font** label is bold). Click the bold label to go back to the main font. If the font has no bold or italic face, PTXprint may make a faux (computer-made) bold or slant; this is shown next to the font size.

**Some text is missing from the PDF.**
**Include Contents of Marker** may be unticked for that marker (it has a line through it). Tick it.

**The Raise box is greyed out.**
**Superscript** is ticked. Superscript sets its own raise.

**The Del button does nothing.**
Only styles you added yourself can be deleted. Use Reset to remove your changes to a standard style.

**The More Info... link is missing or greyed out.**
It is only shown in the **Full** view, and only when internet use is allowed on the **Advanced** tab. Combined or custom markers have no documentation page, so the link is greyed out.

## 13.14 Settings reference

### Size and Position Settings (dialog)

#### OK

Button · Mini+ · `button1`

Saves the size and position and closes the dialog.

#### Cancel

Button · Mini+ · `button2`

Closes the dialog without changing the position.

#### Frame Size – Sidebar: Frame size

Drop-down · Regular+ · `fcb_sbSize`  
Choices: Column Width | Span Width | Page (in Margins) | Page (to Edge)

> The frame size determines the boundaries of where the sidebar will appear on the page.
>
> Span Width only allows a Top or Bottom vertical placement.
>
> Column Width allows several other more precise placement options: Before Verse, After Paragraph, or Cutout; and these can have Left/Inner or Right/Outer Horizontal positioning set.
>
> Page (in Margins) is intended for sidebars that will cover an entire page (i.e. preventing any scripture text from being on that page), but will still show the header.
>
> Page (to Edge) is intended for sidebars to fill the entire page, with no margins at all.
>
> When using single column layout, there is no difference between Column Width and Span Width.
>
> The frame size determines how large the sidebar will appear on the page.
>
> Span Width only allows a Top or Bottom vertical placement. Column Width allows several other more precise placement options: Before Verse, After Paragraph, or Cutout; and these can have Left/Inner or Right/Outer Horizontal positioning set.
>
> When using single column layout, there is no difference between Column Width and Span Width.

Choose this first; it changes the choices in the other lists. **Span Width** can also be **Below Notes**. The page sizes are for boxes that take a whole page, for example on covers.

#### Vertical Position – Sidebar: Vertical position

Drop-down · Regular+ · `fcb_sbPgPos`  
Choices: Top | Bottom | Below Notes | Before Verse | After Paragraph | Cutout | Fill

> Top: Above everything except the header line Bottom: Below all verse text (and footnotes in diglot) Before Verse: 'Here' where defined or before its Anchor Ref After Paragraph: After this paragraph Cutout: A notch/corner cut out of the text, starting at current line Below Notes: Below the footnotes (Span Width only) Fill: Stretch to fill the page (page sizes only)
>
> The above options may have other positioning parameters such as: Left, Right, Center, no. of lines (up or down).
>
> Top: Above everything except the header line Bottom: Below all verse text (and footnotes in diglot) Before Verse: 'Here' where defined or before its Anchor Ref After Paragraph: After this paragraph Cutout: A notch/corner cut out of the text, starting at current line
>
> The above options may have other positioning parameters such as: Left, Right, Center, no. of lines (up or down).

**After Paragraph** can go later with **Number of Lines**. **Cutout** makes the text flow around the box.

#### Horizontal Position – Sidebar: Horizontal position

Drop-down · Regular+ · `fcb_sbHoriz`  
Choices: Left | Center | Right | Inner | Outer | -

> The options available here change based on the Frame Size and Vertical Position settings. So if you can't find an option you are looking for, then check those settings first.

Inner = spine side, Outer = edge side. Greyed out for **Span Width**.

#### Number of Lines – Sidebar/map: Lines to adjust vertically

Number · Regular+ · `s_sbLines`  
Values: -24–24

> Some vertical position options allow a sidebar to be moved up or down by a number of lines or paragraphs.
>
> -Negative (minus) values specify to move UP. +Positive (plus) values specify to move DOWN.
>
> Negative counts for cutouts raise the sidebar, but the cutout will not affect earlier paragraphs. Note that negative and fractional paragraph counts are invalid.

For **After Paragraph** it counts paragraphs (whole numbers only); for **Cutout** it counts lines. Greyed out for other positions.

### Sidebar Image Settings (dialog)

#### Remove Image

Button · Regular+ · `btn_removeSBimage`  
Also: Sidebar FG/BG: Remove image

Then click **OK** to remove the image from this sidebar style.

#### OK

Button · Regular+ · `btn_image_ok`

Saves the image settings. With no image file chosen, the image is removed.

#### Cancel

Button · Regular+ · `btn_image_cancel`

Closes the dialog without changing anything.

#### Sidebar Foreground/Background

##### Select...

Button · Regular+ · `btn_sbSelectFile`  
Also: Sidebar FG/BG: Select an image

> Choose the image file (JPG, PNG or PDF).

The file name is shown next to the button.

##### Scale – Sidebar FG/BG: Scale of image

Number · Regular+ · `s_sbi_scaleWidth`  
Values: 0.01–2 (default 1)

> Specify how much the image should be scaled horizontally.

Relative to the box width. With **Maintain Aspect Ratio** it is also used for the height.

##### Scale – Sidebar FG/BG: Height of image

Number · Regular+ · `s_sbi_scaleHeight`  
Values: 0.01–2 (default 1) · Greyed out by: “Maintain Aspect Ratio”

> Specify how much the image should be scaled vertically.

Relative to the box height. Setting width and height separately can stretch the picture.

##### Maintain Aspect Ratio

Checkbox, on · Regular+ · `c_sbi_lockRatio`  
Also: Sidebar FG/BG: Maintain aspect ratio

> Scale the width and height the same so that the image maintains its proportions.

Untick it only to set the height separately.

##### Foreground Image Position Within Sidebar

###### Sidebar foreground image: Beside text options

Drop-down · Regular+ · `fcb_sbi_posn_beside`  
Choices: Left | Inner | Right | Outer | Left Top | Inner Top | Right Top | Outer Top | Left Centre | Inner Centre | Right Centre | Outer Centre | Left Bottom | Inner Bottom | Right Bottom | Outer Bottom · Needs: “Beside Text”

> Which side of the sidebar text the foreground image goes on (Left, Inner, Right or Outer), and whether it sits at the top, centre or bottom of that side.

Used with **Beside Text**.

###### Above or Below Text

Radio · Regular+ · `r_sbiPosn_above`  
Also: Sidebar foreground image: Above or below text

The image gets its own strip. Choose the exact place in the list beside it.

###### Beside Text

Radio · Regular+ · `r_sbiPosn_beside`  
Also: Sidebar foreground image: Beside text

The image gets its own column; the text is narrower for the full height of the box.

###### Cutout Within Text

Radio · Regular+ · `r_sbiPosn_cutout`  
Also: Sidebar foreground image: Cutout within sidebar

The text flows around the image. This leaves the least empty space.

###### Sidebar foreground image: Above or below options

Drop-down · Regular+ · `fcb_sbi_posn_above`  
Choices: Top | Top-Left | Top-Inner | Top-Centre | Top-Right | Top-Outer | Bottom | Bottom-Left | Bottom-Inner | Bottom-Centre | Bottom-Right | Bottom-Outer · Needs: “Above or Below Text”

> Where the foreground image goes when it is placed in its own strip above or below the sidebar text: Top or Bottom, and Left, Inner, Centre, Right or Outer.

Used with **Above or Below Text**.

###### Sidebar foreground image: Cutout position options

Drop-down · Regular+ · `fcb_sbi_posn_cutout`  
Choices: Left | Inner | Right | Outer · Needs: “Cutout Within Text”

> Which side of the sidebar text the cutout for the foreground image is on.

Used with **Cutout Within Text**.

###### Start N Lines Below Top – Sidebar foreground image: Adjust cutout position

Number · Regular+ · `s_sbiCutoutLines`  
Needs: “Cutout Within Text”

> The number of lines below the top of the sidebar text where the cutout for the foreground image starts.

Keeps the image away from the first lines, for example below a heading inside the box.

##### Background Image Advanced Settings

###### Background Image Transparency – Sidebar background image: Transparency (alpha)

Number · Regular+ · `s_sbiAlpha`

> Transparency or alpha value of the background image: 0 is transparent, 1 is solid. This is useful for turning black lines into a paler shade.
>
> Note that this will allow the background colour to show through, even if the image is above the background layer, so on a green background black will become a darker shade of green, not grey.

About 0.3 makes a watermark that does not make the text hard to read.

###### Color – Sidebar background image: Color

Colour · Regular+ · `col_sbiBgColor`

> Some (rare) PDF line-art images do not set the colour of their lines, relying instead on the 'default' colour, which is normally black. This control sets the default colour to something other than black, and thus such images can be recoloured with this option. If (as most PDF images do) the image defines its own colour, this option will have no visible effect at all. It is also possible that an image will *partly* contain colour information, but only starting part way through the file, a situation that might produce unexpected results.

Works only for a few simple PDF line-art images; most images have their own colours, and then this has no effect.

###### Background Image Transparency

Label · Regular+

> Transparency or alpha value of the background image: 0 is transparent, 1 is solid. This is useful for turning black lines into a paler shade.
>
> Note that this will allow the background colour to show through, even if the image is above the background layer, so on a green background black will become a darker shade of green, not grey.

###### Layer Order – Sidebar background image: Order of layers

Drop-down · Regular+ · `fcb_sbiLayerOrder`  
Choices: In Front of Background | Behind Background

> Only relevant where there is both a background image  
> *and* a background color. Set whether the background image should come above or behind the color. Line art PDFs with a transparent background may display better above the color layer, as the color layer will not then wash them out, but .JPGs are probably better behind, as .JPG images do not have transparency.
>
> Only relevant where there is both a background image  
> *and* a background color. Set whether the background image should come above or behind the color. Line art PDFs with a tranpsarent background may display better above the color layer, as the color layer will not then wash them out, but .JPGs are probably better behind, as .JPG images do not have transparency.

In front: good for PDF line art. Behind: better for .jpg photos.

###### If Image Is Oversized – Sidebar background image: Oversize management

Drop-down · Regular+ · `fcb_sbiOversize`  
Choices: Ignore (overflows frame) | Shrink (maintains ratio) | Squash (distorts ratio) | Crop (unimplemented)

> Select what action should be taken if the background image size is specified with a single dimension (height or width) and the unspecified dimension ends up being too large for a given sidebar.

**Ignore** lets the image stick out of the box. **Shrink** keeps its shape. **Squash** may change its shape. **Crop** is not working yet.

###### Crop Offset – Sidebar background image: Crop offset (XxY)

Text box · Regular+ · `t_sbiBgCropOfs`

> (Not available yet: cropping is still to be implemented.)
>
> Crop offset in the format XxY (e.g. 10x20). Only used when Oversize is set to Crop. Shifts the cropped region by X points horizontally and Y points vertically.

Crop is not working yet. Leave it empty.

###### Scale To – Sidebar background image: Scale Image to Inner/Outer/Bleed area

Drop-down · Regular+ · `fcb_sbiScaleTo`  
Choices: bleed: overflow the page into the cropped area | colbleed: overflow the page into the cropped area as much as the colours do (normally images bleed less) | inner: the area that text could cover (vertically this extends to the inner edge of the border) | outer: the outermost of the coloured box or the border | border: the outer edge of the border | box: the coloured box

> Select where the image should extend to.

**inner** = text area, **box** = coloured box, **border** = border, **outer** = outermost of these, **bleed**/**colbleed** = past the page edge (mainly for covers).

### Add/Edit Style (dialog)

#### OK

Button · Regular+ · `btn_sty_ok`

A new style is added to the list and selected, ready for formatting.

#### Cancel

Button · Regular+ · `btn_sty_cancel`

Closes the dialog without adding or changing a style.

#### Description

Label · Mini+

> You can say what you like here to describe the purpose of the style.

#### ⚠️Marker – Add/Edit marker dialog: Marker (code)

Text box · Regular+ · `t_styMarker`

> The marker code without the backslash, e.g. zpeople. It can only be set when adding a new style.

For example `zpeople` or `cat:people|esb`. If empty when you click **OK**, nothing is created.

#### Add/Edit marker dialog: Marker description

Text area · Regular+ · `textv_styDesc`

> You can say what you like here to describe the purpose of the style.

For your information only.

#### Name

Label · Mini+

> Consists of: Marker..Endmarker - Group - short description and helps to place the marker in the tree listing all markers.

#### Name – Add/Edit marker dialog: Marker name (short description)

Text box · Regular+ · `t_styName`

> Consists of: Marker..Endmarker - Group - short description and helps to place the marker in the tree listing all markers.

Form: `marker - Category - short description`. The middle part (for example `Paragraph`, `Character`, `Heading`) decides the category in the list. PTXprint updates the start of the name when you type a marker code.

#### End Marker – Add/Edit marker dialog: End Marker (code)

Text box · Regular+ · `t_styEndMarker`

> If the closing marker for this marker is not the same as the marker followed by a * then enter it here. For example, with paired milestones, do not create a new milestone just specify the closing milestone marker here.

Usually leave it empty: for character and note markers PTXprint adds the marker followed by `*`. For a pair of milestone markers, type the closing milestone here.

#### ⚠️Type – Add/Edit marker dialog: Marker type

Drop-down · Regular+ · `fcb_styType`  
Choices: Header | Title | Introduction | Introduction Character | Section Paragraph | Verse Paragraph | Character | List | List Character | Milestone | Standalone Milestone | Other Paragraph | Cross Reference | Cross Reference Character | Footnote | Footnote Character | Cell | Attribute | Identification | Internal

> [Required] This tells PTXprint what kind of marker this is.
>
> [Required] This tells PTXprint what kind of a marker this is.

For example **Verse Paragraph** for body text, **Section Paragraph** for a heading, **Character** for words inside a paragraph, or **Footnote**. Cannot be changed for standard USFM markers.

#### [Required] This tells PTXprint how to layout data in this ma...

Text box · Regular+

> [Required] This tells PTXprint how to layout data in this marker. For normal, vernacular body text, use VerseText. If this is part of a heading, use Section. If it is part of the title block of a book, use Title. NoteText makes this a kind of footnote, like \x.

### Styles

#### Find – Find style

Search box · Regular+ · `t_styleSearch`  
Greyed out by: “Lock UI Layout Settings”

> If you are not sure which category your marker can be found under, then use this Search tool to find the marker you need.

Type a marker code (backslash optional, for example `s1` or `\s1`) or part of a name (for example `heading`). After half a second PTXprint selects the first match, opens the categories with matches and colours every matching line pale peach. Clear the box to remove the colouring.

#### Enable (or disable) the filter to only show markers that are...

Toggle, off · Regular+ · `btn_styleFilter`  
Greyed out by: “Lock UI Layout Settings”

> Enable (or disable) the filter to only show markers that are in use in the current set of books.

The bulleted-list icon next to **Find**. When pressed in, the list shows only markers used in the books chosen for printing, with all categories open. Press again to see all markers. If your text has a USFM error, PTXprint shows an error message instead.

#### tv_Styles

Table · Regular+ · `tv_Styles`  
Greyed out by: “Lock UI Layout Settings”

Category lines are bold blue. A line through a marker means it is not printed.

#### Include Contents of Marker

Checkbox, on · Regular+ · `c_styTextProperties`  
Also: Styles: Include marker contents in PDF · Greyed out by: “Lock UI Layout Settings”

> Uncheck this option to set the marker to "non-publishable" so the contents of this marker will not be included in the output.

Tick it to print markers hidden by default, such as `\rem`. For the heading box, title box and text border, the **Tabs+Borders** tab sets this for you.

#### Include Contents of Marker

##### More Info...

Link · not shown · `l_url_usfm`  
Greyed out by: “Lock UI Layout Settings”

Opens in your web browser. For some interface languages the page goes through an automatic translation, unless **Only Use English Links** is ticked on the **Advanced** tab. Shown only in the **Full** view when internet use is allowed. Greyed out for combined or custom markers.

##### Add

Button · Regular+ · `btn_styAdd`  
Greyed out by: “Lock UI Layout Settings”

> Find a style within the appropriate section which is similar to the new style you wish to create. Then click this Add button to create a new style based on the currently selected style.

The copy includes all settings (also border and padding of box styles). Then fill in the **Add/Edit Style** dialog. Advanced.

##### Del

Button · Regular+ · `btn_styDel`  
Greyed out by: “Lock UI Layout Settings”

> Click to delete this style (only styles you have added can be deleted). Warning: There is no confirmation or undo!

For standard styles nothing happens.

##### Click to remove all changes made to this style, returning it...

Button · Regular+ · `btn_styReset`  
Greyed out by: “Lock UI Layout Settings”

> Click to remove all changes made to this style, returning it to the values in the underlying stylesheets.

The circular-arrows button. To reset one setting, click its bold name instead. Reset keeps the name, description and end marker. Greyed out for styles you created, because they have no underlying values to go back to.

##### Edit

Button · Regular+ · `btn_styEdit`  
Greyed out by: “Lock UI Layout Settings”

> Click to Edit additional properties for this style.

Change name, description, type or end marker. The marker code cannot be changed.

##### Hover-help

Label · Regular+  
Greyed out by: “Lock UI Layout Settings”

> Hover over these help topics to gain a greater understanding about how the Styles editor works.

##### Why are some parameters bold?

Label · Regular+  
Greyed out by: “Lock UI Layout Settings”

> When a setting's name is in bold it indicates that the value is different from what is in the stylesheet.
>
> Note that you can click on a bold setting name of any parameter to RESET it to the stylesheet value.

##### How are Stylesheets applied?

Label · Regular+  
Greyed out by: “Lock UI Layout Settings”

> Stylesheets are applied in this order with later settings overriding earlier settings:
>
> usfm_sb.sty is the underlying Paratext stylesheet (uneditable).
>
> ptx2pdf.sty contains PTXprint application modifications to make things work better (uneditable).
>
> Optional: custom.sty contains style modifications that are project-wide and also affect display of text within Paratext itself (can be edited from the Advanced tab). Typically used to add project-specific markers.
>
> ptxprint.sty contains the config's settings as edited by this Styles editor.
>
> Optional: ptxprint-mods.sty can be edited from the Advanced tab. Because it comes last, it takes priority.

##### Character Settings

###### Select Font...

Button · Regular+ · `bl_font_styFontName`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

With no font chosen, the marker uses the main font from the **Fonts+Script** tab. When a font is set, the **Font** label is bold; click it to go back to the main font.

###### Font Size Factor – Styles: Font size factor

Number · Regular+ · `s_styFontSize`  
Values: 0.1–50 (default 1) · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> This is a factor or proportion of the base font size. So 1.0 is the same as the base font size from the Layout tab. (Not available for \p, which always uses the Base Font Size.)

0.8 is smaller, 1.5 bigger. The real size in points is shown under the font button. With **Scale Relative to Parent** ticked, this becomes **Font Scale**, relative to the surrounding text.

###### Scale Relative to Parent

Checkbox, off · Regular+ · `c_styFontScale`  
Also: Styles: Scale relative to parent · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Normally the Font Size is relative to the Base Font Size (Layout tab). Tick this to make it relative to the size of the surrounding text instead. Note that  
> \p has a FontSize of 12 in the underlying stylesheet.

Use it when the size should follow the surrounding text, for example a character style that is always 80% of its paragraph. The size box label changes to **Font Scale**.

###### Bold

Checkbox, off · Regular+ · `c_styFaceBold`  
Also: Styles: Bold · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

If the font has no real bold face, PTXprint may use a faux (computer-made) bold, depending on the **Fonts+Script** tab settings.

###### Italic

Checkbox, off · Regular+ · `c_styFaceItalic`  
Also: Styles: Italic · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

If the font has no real italic face, a computer-made slant may be used.

###### Superscript

Checkbox, off · Regular+ · `c_styFaceSuperscript`  
Also: Styles: Superscript · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> The superscript option overrides these settings:  
>    Font Size Factor is set to 0.75  
>    Raise is set to 0.85 times the x-height of the font (which  
>    defaults to 1/2 the ascent if not specified in the font).

Used for verse numbers or footnote callers.

###### SmallCaps

Checkbox, off · Regular+ · `c_stySmallCap`  
Also: Styles: Smallcaps · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

Prints lowercase letters as small capitals. Needs a font that supports them, and only has an effect in scripts with upper and lower case. Often used for `\nd` (LORD).

###### Raise – Styles: Raise

Number · Regular+ · `s_styRaise`  
Values: -50–50 · Needs: “Include Contents of Marker” · Greyed out by: “Superscript”, “Lock UI Layout Settings”

> How much to raise the text (in pts).

A negative number moves the text down. Use small values. Raised text cannot break across lines, so use it only for short text.

###### Color: x001122 – Styles: Color

Colour · Regular+ · `col_styColor`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Sets text color for text in this style.

The colour code is shown next to the label. Choosing a colour also ticks **Enable Colored Text** on the **Fonts+Script** tab; if that is later unticked, the colour does not print. Click the bold **Color** label to remove your colour.

###### Underline

Checkbox, off · Regular+ · `c_styFaceUnderline`  
Also: Styles: Underline · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Note that underlining in printed scripture text is actively discouraged.

Underlines the text of this marker.

###### 11.7pt (↑6.6 ↓2.2)

Label · Regular+ · `l_styActualFontSize`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Calculated absolute point size given the current Base Font Size (which is set on the Layout tab).
>
> The (↑Ascender ↓Descender) values from the base line for this font are provided for reference.

Worked out from **Font Size Factor** and **Base Font Size**. Information only.

###### GR stretch=95% bold=1.8 ital=0.15

Label · Regular+ · `l_styFontFeats`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> If any modifications to the typeface have been selected, then they will be displayed here.
>
> GR= Graphite has been enabled stretch= (or shrink) font horizontally bold= embolden value (faux bold) ital= slant value (faux italics)

Empty when there are no changes. Information only.

##### Paragraph Settings

###### Alignment – Styles: Paragraph alignment

Drop-down · Regular+ · `fcb_styJustification`  
Choices: Justified | Left | LeftBal | Center | Right | Inner | Outer · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> If text is justified but Justify Paragraphs is turned off on the Body tab then an alignment of Justified here is treated as Left, (and maybe swapped if Right-to-Left).
>
> When the Writing system text flow direction is Right-to-Left the interpretation of Left and Right is swapped. Top-to-Bottom flow is treated as Left-to-Right.
>
> Inner vs Outer (used for Marginal Notes, Xrefs or Headings)  
>   Inner = closer to the center:  
>     In a 2-column layout: closer to the space between columns.  
>     In a 1-column layout: closer to the spine of the page spread.  
>   Outer = further from the center:  
>     In a 2-column layout: closer to the outer edge of the page.  
>     In a 1-column layout: closer to the outer edge of the page spread.  
>   Note: Marginal notes cannot switch sides mid-paragraph  
>              if the page or column changes.

**LeftBal** is left-aligned with more even line lengths. **Inner** and **Outer** depend on which side of the page or column the text is on. Click the bold **Alignment** label to undo your change.

###### First Line Indent Factor

Number · Regular+ · `s_styFirstLineIndent`  
Values: -50–50 · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> This is multiplied by the Base Paragraph Indent value (specified on the Layout tab) to get the final indentation amount.

1 is a normal paragraph indent, 0 is none. A negative value gives a hanging indent, often used for poetry and lists. For sidebars it moves the whole box sideways.

###### Left Indent Factor – Styles: Left indent

Number · Regular+ · `s_styLeftMargin`  
Values: -100–100 · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> This is multiplied by the Base Paragraph Indent value (specified on the Layout tab) to get the final indentation amount.
>
> When the Writing system text flow direction is Right-to-Left the interpretation of Left and Right is swapped.

Indents the whole paragraph. Use it for poetry levels, quotations and lists.

###### Right Indent Factor – Styles: Right indent

Number · Regular+ · `s_styRightMargin`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> This is multiplied by the Base Paragraph Indent value (specified on the Layout tab) to get the final indentation amount.
>
> When the Writing system text flow direction is Right-to-Left the interpretation of Left and Right is swapped.

Indents the whole paragraph from the right (left for right-to-left text).

###### Line Spacing Factor – Styles: Line spacing

Number · Regular+ · `s_styLineSpacing`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> This is a proportion of the base line spacing. So 1.0 is the same as the base line spacing from the Layout tab. If Absolute Spacing is set, then this value is the line spacing in pts.

1.0 is the same as **Base Line Spacing**. With **Use Absolute Spacing** ticked, the label changes to **Baseline**. Greyed out for `\p`.

###### Use Absolute Spacing (in pts)

Checkbox, off · Regular+ · `c_styAbsoluteLineSpacing`  
Also: Styles: Use absolute line spacing · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> The Line Spacing is usually calculated as a factor of the Font Size. If you prefer to specify an exact/absolute line spacing (in points), then enable this option.

PTXprint converts the value when you tick or untick it, and keeps only the new kind, so you can switch back and forth safely. A fixed value does not change when you later change the base line spacing. Greyed out for `\p`.

###### Space Before Factor – Styles: Space before

Number · Regular+ · `s_stySpaceBefore`  
Values: -1–5 · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Amount of space to insert before the paragraph. The actual space is this factor multiplied by the base line spacing from the Layout tab.

1.0 is about one empty line. Headings often use 0.5 to 1.5.

###### Space After Factor – Styles: Space after

Number · Regular+ · `s_stySpaceAfter`  
Values: -1–5 · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Amount of space to insert after the paragraph. The actual space is this factor multiplied by the base line spacing from the Layout tab.

1.0 is about one empty line.

###### Maximum Ragged Space – Styles: Maximum ragged (fill) space

Number · Regular+ · `s_styNonJustifiedFill`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> How much of the column-width can be empty space at a non-justified edge? This affects mid-paragraph line-breaking and may cause stretching of other spacing if the line would be too short otherwise. It does not stop the final line of a paragraph from being shorter.
>
> This value is set as the proportion of the column width, with sensible values being with the range of 0.20 to 0.75 (where 1.00 represents the entire column width). Discretionary breaks (//) will be ignored if breaking there would leave more than this much space.

Default 0.25 (a quarter of the line). Larger values allow more uneven lines; smaller values make lines more even but may stretch word spaces.

##### Other Settings › Note Settings

###### Caller Raise – Note settings: Caller raise

Number · Regular+ · `s_styCallerRaise`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Raise the caller in the main text by this number of points.

Leave it at 0 unless the caller sits too high or too low.

###### Note Caller Raise – Note settings: Note caller raise

Number · Regular+ · `s_styNoteCallerRaise`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Raise the caller in the note by this number of points.

The caller at the start of the note itself.

###### Caller Style – Note settings: Caller style

Text box · Regular+ · `t_styCallerStyle`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> The style which is used to style the caller in the main text. If none is specified then  
> \v is used.

Type the marker code without the backslash. Advanced.

###### Note Caller Style – Note settings: Note caller style

Text box · Regular+ · `t_styNoteCallerStyle`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> The style which is used to style the caller in the note itself. If none is specified then  
> \v is used.

Type the marker code without the backslash. Advanced.

###### Note Blend Into Style – Note settings: Note blend into style

Text box · Regular+ · `t_NoteBlendInto`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Insert the notes of the marker being defined into the collection of notes in the marker specified here.
>
> For example, if when defining the \x style, if this value was set to f then all cross references would be blended into the \f footnotes.

The blended notes keep their own style. The **Notes+Refs** tab sets this for cross-references when you blend them with footnotes, so normally you type nothing here.

##### Other Settings › Table Settings

###### Table settings: Vertical position of \tc markers

Drop-down · Regular+ · `fcb_stytcVpos`  
Choices: Top | Center | Bottom | Gridded Center · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Where text sits vertically in a table cell that is shorter than the tallest cell in the row. Gridded Center keeps the text on whole lines.

**Gridded Center** keeps the text on whole lines so it lines up with the other cells.

##### Other Settings › Sidebar Settings

###### Color – Sidebar settings: Color

Colour · Regular+ · `col_sb_backColor`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Sets the background color for the sidebar.
>
> Background shading color.

Choose a light colour so the text stays easy to read. Click the bold **Color** label to remove your change.

###### Alpha – Sidebar settings: Alpha (transparency)

Number · Regular+ · `s_sbAlpha`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> The transparency or alpha value of the background colour:  
> 0 is transparent, 1 is solid.

A value below 1 lets a background image or page decoration show through.

###### Width – Sidebar settings: Width

Number · Regular+ · `s_sbWidth`  
Values: 0.25–2.5 (default 1) · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Sidebar width as a proportion of the column/page width (1.0 = full width,  
> 0.5 = half width).

Relative to the frame chosen in **Size and Position**. Narrow boxes are useful for cutouts.

###### Borders...

Button · Regular+ · `btn_sbBorders`  
Also: Sidebar settings: Borders · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Click for additional settings to control the look of borders for this category of sidebar.

Border lines, colours, padding and ornaments. See the **Tabs+Borders** chapter.

###### Foreground Image...

Button · Regular+ · `btn_sbFGIDia`  
Also: Sidebar settings: Foreground image settings · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Click for additional settings to use a foreground image for this category of sidebar.

A foreground image is shown in every box of this category, for example a scroll for history notes.

###### Background Image...

Button · Regular+ · `btn_sbBGIDia`  
Also: Sidebar settings: Background image settings · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Click for additional settings to use a background image for this category of sidebar.

A background image sits behind the text of the box, like a watermark.

###### t_sbPgPos

Text box · Regular+ · `t_sbPgPos`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

Examples: `t` (top), `bl` (bottom left), `cr2` (cutout on the right, 2 lines down), `Pcf` (whole page, filled). Use the **Size and Position...** button rather than typing here.

###### Size and Position...

Button · Regular+ · `btn_sbSizePosition`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Choose the frame size and position of this category of sidebar on the page.

The dialog has a preview picture.
