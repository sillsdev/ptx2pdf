## What this tab is for

Your Paratext text uses **markers** to say what each piece of text is. A marker is a short code that starts with a backslash. For example, `\p` starts a normal paragraph, `\s1` is a section heading, `\v` is a verse number, `\f` is a footnote and `\nd` is the name of God ("LORD"). These are called **USFM markers**.

A **style** is the set of formatting rules for one marker: font, size, bold or italic, colour, indents, alignment and the space above and below. The list of all styles is a **stylesheet**. The **Styles** tab is the style editor. Use it to change how one kind of text looks everywhere, for example "make all section headings bigger", "make verse numbers red", "put more space above the headings" or "do not print the `\rem` remarks".

The tab is only shown in the **Regular** and **Full** views (see the chapter about the main window). If the whole tab is greyed out, **Lock UI Layout Settings** on the **Advanced** tab is ticked; untick it to make changes.

Many other tabs have small blue links with a marker name (for example next to the verse number or heading settings). Click one to jump straight to that marker on the **Styles** tab. The tab label moves a little to show you where you are.

Changes show in the PDF only after you click **Print (Make PDF)** again. Style changes are saved with the current configuration.

## The marker list

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

## Bold setting names: what has changed

PTXprint reads several stylesheets in order. Later ones override earlier ones:

1. The standard Paratext stylesheet (you cannot change it).
2. PTXprint's own additions (you cannot change them).
3. The project's `custom.sty`, if there is one. It can be edited from the **Advanced** tab. It also affects how Paratext shows the text.
4. Your changes on this **Styles** tab, saved with the configuration.
5. `ptxprint-mods.sty`, if there is one. It can be edited from the **Advanced** tab. Because it comes last, it wins over everything else.

A setting name in **bold** (for example **Font Size Factor**) means you changed this value on the **Styles** tab, so it differs from the stylesheets underneath. Click the bold name to go back to the original value of that one setting. Click Reset to remove all your changes to the style.

Hover over **Why are some parameters bold?** and **How are Stylesheets applied?** at the bottom of the tab for a short reminder.

## Include Contents of Marker

Untick it to leave the text of this marker out of the PDF. The marker then has a line through it in the list, and its other settings are greyed out. The text stays in your Paratext project; only the PDF changes.

Some markers, such as `\rem` (remarks) or the identification lines, are not printed by default. Tick this box for them if you want them in the PDF.

The automatic boxes around headings and titles (`cat:headingsbox|esb`, `cat:titlebox|esb`) and the text border (`textborder`) also use this setting. Normally you turn these on from the **Tabs+Borders** tab, which ticks this box for you.

## Character Settings

This area controls how the letters look.

* **Select Font...** – a different font for this marker only; otherwise the main font from the **Fonts+Script** tab is used. Beside it PTXprint shows the real size in points (pt – one point is about 0.35 mm) and any font changes such as Graphite, stretch, faux bold or slant.
* **Font Size Factor** – size compared with the **Base Font Size** on the **Layout** tab: 1.2 is 20% bigger, 0.8 is 20% smaller.
* **Scale Relative to Parent** – the size box becomes **Font Scale**, relative to the surrounding text instead of the base font size.
* **Bold**, **Italic**, **SmallCaps**, **Superscript** and **Underline**.
* **Raise** – moves the text up (or down, with a minus number) in points. Greyed out when **Superscript** is ticked, because superscript sets its own size and raise.
* **Color** – the text colour.

For `\p`, **Font Size Factor**, **Line Spacing Factor** and **Use Absolute Spacing** are greyed out. Set the main text size and line spacing on the **Layout** tab (**Base Font Size** and **Base Line Spacing**).

For a character marker (one that styles a few words inside a paragraph, like `\nd` or `\wj`), PTXprint opens only **Character Settings**. For paragraph markers it also opens **Paragraph Settings**. Click an area's title to open or close it yourself.

## Paragraph Settings

This area controls the shape of the paragraph.

* **Alignment** – **Justified** (both edges straight), **Left**, **LeftBal**, **Center**, **Right**, **Inner** or **Outer**. **LeftBal** is left-aligned, but PTXprint also tries to make the lines, including the last line, more even in length. **Inner** and **Outer** are mainly for margin notes, cross-references in the margin and headings. For right-to-left scripts, Left and Right are swapped.
* **First Line Indent Factor**, **Left Indent Factor**, **Right Indent Factor** – multiples of the **Base Indent** on the **Layout** tab. A negative first line indent makes a "hanging" indent: the first line starts further left than the others. Poetry and list markers often use this.
* **Line Spacing Factor** – compared with the base line spacing. **Use Absolute Spacing (in pts)** gives an exact number of points instead; the label changes to **Baseline** and PTXprint converts the number.
* **Space Before Factor**, **Space After Factor** – extra space above and below, as a multiple of the base line spacing. 1.0 is about one empty line, 0.5 about half a line.
* **Maximum Ragged Space** – for non-justified paragraphs, how much of the line may stay empty at the ragged edge.

## Other Settings

Settings used only by some markers. PTXprint opens the part that fits the selected marker.

* **Note Settings** (footnotes `\f`, cross-references `\x` and similar): style and raise of the caller (the small letter or symbol in the text and at the start of the note), and **Note Blend Into**, which puts these notes together with another kind of note.
* **Table Settings** (table cells `\tc`): where text sits from top to bottom when the cells in a row have different heights.
* **Sidebar Settings** (sidebar categories and the text border): see the next section.

## Sidebars

A **sidebar** is a box of extra text, separate from the Scripture text, for example a study note about a place or a person. In USFM it starts with `\esb`, then a category such as `\cat people\cat*`, and ends with `\esbe`. All sidebars with the same category share one style; for "people" the marker name is `cat:people|esb`. PTXprint also uses sidebar styles itself, for example for the parts of the cover, the automatic boxes around headings and titles, and `cat:box|esb` for simple boxes.

Selecting a sidebar style opens **Sidebar Settings**:

* **Color** and **Alpha** – background colour of the box and how solid it is.
* **Width** – width of the box compared with the column or page.
* **Borders...** – the **Border Settings** dialog (see the **Tabs+Borders** chapter).
* **Foreground Image...** – a small picture (a logo) in each box of this category. See **Sidebar Image Settings** below.
* **Background Image...** – a picture behind the text of the box, like a watermark.
* **Size and Position...** – where the box goes on the page, shown as a short code beside the button.

The text inside a sidebar can have its own styles. For example, paragraphs inside "people" sidebars use `cat:people|p`. If such a style exists, change it like any other style; if not, you can add it (see **Common tasks**).

## Size and Position Settings (dialog)

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

## Sidebar Image Settings (dialog)

Opens from **Foreground Image...** or **Background Image...**; the title shows which.

* **Select...** chooses the image. PDF line art works best over a coloured background, because .jpg images cannot be transparent.
* **Scale** is the size compared with the box. **Maintain Aspect Ratio** keeps the picture's shape (height follows width).
* For a foreground image, choose **Above or Below Text**, **Beside Text** or **Cutout Within Text**, then the exact place in the list beside it.
* For a background image, **Background Image Advanced Settings** set transparency, layer order, what happens if it is too big, and which part of the box it fills.
* To take the image away, click **Remove Image**, then **OK**.

## Add/Edit Style (dialog)

Opens from **Add** or **Edit**. It describes a marker: code, name, description, type and end marker. The formatting itself is then set on the **Styles** tab as usual. Creating markers is an advanced task. Most users only need it for special markers their project already uses (for example markers starting with `z`), or for cases such as a sidebar category.

* **Add**: the new style is a copy of the selected style, with all its settings, also ones not shown on the **Styles** tab, such as the border and padding of a sidebar (box) style. Only marker, name, description, type and end marker come from the dialog. So select a similar marker first.
* **Edit**: the **Marker** box is greyed out (a marker cannot be renamed). For standard USFM markers **Type** is also greyed out.
* **Name** controls where the marker appears in the list, for example `zpeople - Paragraph - Paragraph about people` goes into **Paragraphs**.

## Common tasks

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

## Common problems

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

## Control notes

### @t_styleSearch
Type a marker code (backslash optional, for example `s1` or `\s1`) or part of a name (for example `heading`). After half a second PTXprint selects the first match, opens the categories with matches and colours every matching line pale peach. Clear the box to remove the colouring.

### @btn_styleFilter
The bulleted-list icon next to **Find**. When pressed in, the list shows only markers used in the books chosen for printing, with all categories open. Press again to see all markers. If your text has a USFM error, PTXprint shows an error message instead.

### @tv_Styles
Category lines are bold blue. A line through a marker means it is not printed.

### @c_styTextProperties
Tick it to print markers hidden by default, such as `\rem`. For the heading box, title box and text border, the **Tabs+Borders** tab sets this for you.

### @l_url_usfm
Opens in your web browser. For some interface languages the page goes through an automatic translation, unless **Only Use English Links** is ticked on the **Advanced** tab. Shown only in the **Full** view when internet use is allowed. Greyed out for combined or custom markers.

### @btn_styAdd
The copy includes all settings (also border and padding of box styles). Then fill in the **Add/Edit Style** dialog. Advanced.

### @btn_styDel
For standard styles nothing happens.

### @btn_styReset
The circular-arrows button. To reset one setting, click its bold name instead. Reset keeps the name, description and end marker. Greyed out for styles you created, because they have no underlying values to go back to.

### @btn_styEdit
Change name, description, type or end marker. The marker code cannot be changed.

### @bl_font_styFontName
With no font chosen, the marker uses the main font from the **Fonts+Script** tab. When a font is set, the **Font** label is bold; click it to go back to the main font.

### @s_styFontSize
0.8 is smaller, 1.5 bigger. The real size in points is shown under the font button. With **Scale Relative to Parent** ticked, this becomes **Font Scale**, relative to the surrounding text.

### @c_styFontScale
Use it when the size should follow the surrounding text, for example a character style that is always 80% of its paragraph. The size box label changes to **Font Scale**.

### @c_styFaceBold
If the font has no real bold face, PTXprint may use a faux (computer-made) bold, depending on the **Fonts+Script** tab settings.

### @c_styFaceItalic
If the font has no real italic face, a computer-made slant may be used.

### @c_styFaceSuperscript
Used for verse numbers or footnote callers.

### @c_stySmallCap
Prints lowercase letters as small capitals. Needs a font that supports them, and only has an effect in scripts with upper and lower case. Often used for `\nd` (LORD).

### @s_styRaise
A negative number moves the text down. Use small values. Raised text cannot break across lines, so use it only for short text.

### @col_styColor
The colour code is shown next to the label. Choosing a colour also ticks **Enable Colored Text** on the **Fonts+Script** tab; if that is later unticked, the colour does not print. Click the bold **Color** label to remove your colour.

### @c_styFaceUnderline
Underlines the text of this marker.

### @l_styActualFontSize
Worked out from **Font Size Factor** and **Base Font Size**. Information only.

### @l_styFontFeats
Empty when there are no changes. Information only.

### @fcb_styJustification
**LeftBal** is left-aligned with more even line lengths. **Inner** and **Outer** depend on which side of the page or column the text is on. Click the bold **Alignment** label to undo your change.

### @s_styFirstLineIndent
1 is a normal paragraph indent, 0 is none. A negative value gives a hanging indent, often used for poetry and lists. For sidebars it moves the whole box sideways.

### @s_styLeftMargin
Indents the whole paragraph. Use it for poetry levels, quotations and lists.

### @s_styRightMargin
Indents the whole paragraph from the right (left for right-to-left text).

### @s_styLineSpacing
1.0 is the same as **Base Line Spacing**. With **Use Absolute Spacing** ticked, the label changes to **Baseline**. Greyed out for `\p`.

### @c_styAbsoluteLineSpacing
PTXprint converts the value when you tick or untick it, and keeps only the new kind, so you can switch back and forth safely. A fixed value does not change when you later change the base line spacing. Greyed out for `\p`.

### @s_stySpaceBefore
1.0 is about one empty line. Headings often use 0.5 to 1.5.

### @s_stySpaceAfter
1.0 is about one empty line.

### @s_styNonJustifiedFill
Default 0.25 (a quarter of the line). Larger values allow more uneven lines; smaller values make lines more even but may stretch word spaces.

### @s_styCallerRaise
Leave it at 0 unless the caller sits too high or too low.

### @s_styNoteCallerRaise
The caller at the start of the note itself.

### @t_styCallerStyle
Type the marker code without the backslash. Advanced.

### @t_styNoteCallerStyle
Type the marker code without the backslash. Advanced.

### @t_NoteBlendInto
The blended notes keep their own style. The **Notes+Refs** tab sets this for cross-references when you blend them with footnotes, so normally you type nothing here.

### @fcb_stytcVpos
**Gridded Center** keeps the text on whole lines so it lines up with the other cells.

### @col_sb_backColor
Choose a light colour so the text stays easy to read. Click the bold **Color** label to remove your change.

### @s_sbAlpha
A value below 1 lets a background image or page decoration show through.

### @s_sbWidth
Relative to the frame chosen in **Size and Position**. Narrow boxes are useful for cutouts.

### @btn_sbBorders
Border lines, colours, padding and ornaments. See the **Tabs+Borders** chapter.

### @btn_sbFGIDia
A foreground image is shown in every box of this category, for example a scroll for history notes.

### @btn_sbBGIDia
A background image sits behind the text of the box, like a watermark.

### @t_sbPgPos
Examples: `t` (top), `bl` (bottom left), `cr2` (cutout on the right, 2 lines down), `Pcf` (whole page, filled). Use the **Size and Position...** button rather than typing here.

### @btn_sbSizePosition
The dialog has a preview picture.

### @fcb_sbSize
Choose this first; it changes the choices in the other lists. **Span Width** can also be **Below Notes**. The page sizes are for boxes that take a whole page, for example on covers.

### @fcb_sbPgPos
**After Paragraph** can go later with **Number of Lines**. **Cutout** makes the text flow around the box.

### @fcb_sbHoriz
Inner = spine side, Outer = edge side. Greyed out for **Span Width**.

### @s_sbLines
For **After Paragraph** it counts paragraphs (whole numbers only); for **Cutout** it counts lines. Greyed out for other positions.

### @button1
Saves the size and position and closes the dialog.

### @button2
Closes the dialog without changing the position.

### @btn_sbSelectFile
The file name is shown next to the button.

### @s_sbi_scaleWidth
Relative to the box width. With **Maintain Aspect Ratio** it is also used for the height.

### @s_sbi_scaleHeight
Relative to the box height. Setting width and height separately can stretch the picture.

### @c_sbi_lockRatio
Untick it only to set the height separately.

### @r_sbiPosn_above
The image gets its own strip. Choose the exact place in the list beside it.

### @fcb_sbi_posn_above
Used with **Above or Below Text**.

### @r_sbiPosn_beside
The image gets its own column; the text is narrower for the full height of the box.

### @fcb_sbi_posn_beside
Used with **Beside Text**.

### @r_sbiPosn_cutout
The text flows around the image. This leaves the least empty space.

### @fcb_sbi_posn_cutout
Used with **Cutout Within Text**.

### @s_sbiCutoutLines
Keeps the image away from the first lines, for example below a heading inside the box.

### @s_sbiAlpha
About 0.3 makes a watermark that does not make the text hard to read.

### @col_sbiBgColor
Works only for a few simple PDF line-art images; most images have their own colours, and then this has no effect.

### @fcb_sbiLayerOrder
In front: good for PDF line art. Behind: better for .jpg photos.

### @fcb_sbiOversize
**Ignore** lets the image stick out of the box. **Shrink** keeps its shape. **Squash** may change its shape. **Crop** is not working yet.

### @t_sbiBgCropOfs
Crop is not working yet. Leave it empty.

### @fcb_sbiScaleTo
**inner** = text area, **box** = coloured box, **border** = border, **outer** = outermost of these, **bleed**/**colbleed** = past the page edge (mainly for covers).

### @btn_removeSBimage
Then click **OK** to remove the image from this sidebar style.

### @btn_image_ok
Saves the image settings. With no image file chosen, the image is removed.

### @btn_image_cancel
Closes the dialog without changing anything.

### @t_styMarker
For example `zpeople` or `cat:people|esb`. If empty when you click **OK**, nothing is created.

### @textv_styDesc
For your information only.

### @t_styName
Form: `marker - Category - short description`. The middle part (for example `Paragraph`, `Character`, `Heading`) decides the category in the list. PTXprint updates the start of the name when you type a marker code.

### @t_styEndMarker
Usually leave it empty: for character and note markers PTXprint adds the marker followed by `*`. For a pair of milestone markers, type the closing milestone here.

### @fcb_styType
For example **Verse Paragraph** for body text, **Section Paragraph** for a heading, **Character** for words inside a paragraph, or **Footnote**. Cannot be changed for standard USFM markers.

### @btn_sty_ok
A new style is added to the list and selected, ready for formatting.

### @btn_sty_cancel
Closes the dialog without adding or changing a style.
