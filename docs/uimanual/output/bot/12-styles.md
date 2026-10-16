# Styles tab

## What this tab is for

Your Paratext text uses **markers** to say what each piece of text is. A marker is a short code that starts with a backslash. For example, `\p` starts a normal paragraph, `\s1` is a section heading, `\v` is a verse number, `\f` is a footnote and `\nd` is the name of God ("LORD"). These codes are called **USFM markers**.

A **style** is the set of formatting rules for one marker: its font, size, bold or italic, colour, indents, alignment and the space above and below it. The list of all styles is called a **stylesheet**. The **Styles** tab is the style editor. Use it when you want to change how one kind of text looks everywhere in the book. For example: "make all section headings bigger", "make verse numbers red", "put more space above the headings" or "do not print the `\rem` remarks".

The **Styles** tab is only shown in the **Default** and **Full** views. If you do not see it, change the view level (see the chapter about the main window). If the whole tab is greyed out, the setting **Lock UI Layout Settings** on the **Advanced** tab is ticked. Untick it to make changes again.

Many other tabs have small blue links with a marker name (for example next to the verse number or heading settings). Click such a link to jump straight to that marker on the **Styles** tab. The tab label moves a little to show you where you are.

A change on this tab does not show in the PDF until you click **Print (Make PDF)** again. Style changes are saved with the current configuration.

## The marker list

The left side of the tab is a list of all markers. The markers are grouped into categories, for example **Chapters & Verses**, **Paragraphs**, **Poetry**, **Titles & Headings**, **Footnotes**, **Cross References**, **Character Styling** and **Peripheral Materials**. Category names are shown in bold blue. Click the small arrow beside a category to open it. Click a marker to select it. Its settings then appear on the right.

Each line shows the marker code and a short name, for example `s1 - Heading - Section Level 1`. A marker that is drawn with a line through it is set to "not printed" (see **Include Contents of Marker** below).

To find a marker quickly:

* Type in the **Find** box above the list. You can type the marker code (with or without the backslash, for example `s1` or `\s1`) or a word from its name (for example `heading`). After half a second, PTXprint selects the first match, opens the categories that contain matches and colours all matching lines pale peach.
* Click the filter button (the bulleted-list icon next to **Find**) to show only the markers that are really used in the books you have chosen to print. Click it again to show all markers. This makes the list much shorter.

Some markers have numbered levels, for example `\s1`, `\s2` or `\q1`, `\q2`. If you select the plain marker (for example `s` or `q`), PTXprint edits level 1 (`s1` or `q1`). Each level has its own style. A change to `\s1` does not change `\s2`.

Below the marker name and description you see these buttons:

* **Add** – make a new style, based on the selected style.
* **Del** – delete a style that you added yourself.
* Reset (the circular-arrows icon) – remove all your changes to the selected style.
* **Edit** – change the name, description, type and end marker of the style.
* **More Info...** – open the USFM documentation page for this marker on the internet. This link is only shown in the **Full** view, and only when **Disable ALL Internet Use** on the **Advanced** tab is not ticked.

## Bold setting names: what has changed

PTXprint reads several stylesheets, one after the other. Later ones override earlier ones:

1. The standard Paratext stylesheet (you cannot change it).
2. PTXprint's own additions (you cannot change them).
3. The project's `custom.sty`, if there is one. It can be edited from the **Advanced** tab. It also affects how Paratext shows the text.
4. The changes you make on this **Styles** tab, saved with the configuration.
5. `ptxprint-mods.sty`, if there is one. It can be edited from the **Advanced** tab. Because it comes last, it wins over everything else.

When the name of a setting (for example **Font Size Factor** or **Space Before Factor**) is shown in **bold**, it means that you have changed this value on the **Styles** tab. It is now different from the stylesheets underneath. To go back to the original value of one setting, click the bold setting name. To remove all your changes to the whole style, click the Reset (circular-arrows) button.

Hover the mouse over **Why are some parameters bold?** and **How are Stylesheets applied?** at the bottom of the tab for a short reminder.

## Include Contents of Marker

When **Include Contents of Marker** is ticked, the text inside this marker is printed. Untick it to leave that text out of the PDF. The marker then shows with a line through it in the list, and the other settings for it are greyed out. The text stays in your Paratext project. Only the PDF changes.

Some markers, such as `\rem` (remarks) or the identification lines, are not printed by default. Tick **Include Contents of Marker** for them if you do want them in the PDF.

The automatic boxes around headings and titles (`cat:headingsbox|esb` and `cat:titlebox|esb`) and the border around the text (`textborder`) also use this setting. Normally you turn these on from the **Tabs+Borders** tab, which ticks this box for you.

## Character Settings

The **Character Settings** area controls how the letters look.

* **Select Font...** chooses a different font for this marker only. If no font is chosen, the marker uses the main font from the **Fonts+Script** tab. Next to it, PTXprint shows the real size in points (pt – one point is about 0.35 mm) and, if any are used, font changes such as Graphite, stretch, faux bold or slant.
* **Font Size Factor** is the size compared with the **Base Font Size** on the **Layout** tab. 1.0 is the same size, 1.2 is 20% bigger, 0.8 is 20% smaller.
* **Scale Relative to Parent** changes the meaning of the size box. The label then changes to **Font Scale**, and the number is compared with the surrounding text instead of the base font size.
* **Bold**, **Italic**, **SmallCaps**, **Superscript** and **Underline** turn these effects on or off.
* **Raise** moves the text up (or down, with a minus number) by a number of points. It is greyed out when **Superscript** is ticked, because superscript sets its own size and raise.
* **Color** sets the colour of the text.

For the normal paragraph marker `\p`, **Font Size Factor**, **Line Spacing Factor** and **Use Absolute Spacing** are greyed out. The size and line spacing of the main text are set on the **Layout** tab (**Base Font Size** and **Base Line Spacing**).

When the marker is a character marker (a marker that styles a few words inside a paragraph, like `\nd` or `\wj`), PTXprint opens only the **Character Settings** area. For paragraph markers it also opens **Paragraph Settings**. You can always open or close an area yourself by clicking its title.

## Paragraph Settings

The **Paragraph Settings** area controls the shape of the paragraph.

* **Alignment** – how the lines sit between the margins: **Justified** (both edges straight), **Left**, **LeftBal**, **Center**, **Right**, **Inner** or **Outer**. **LeftBal** is left-aligned, but PTXprint also tries to keep the lines, including the last line, of a more even length. **Inner** and **Outer** are mainly for margin notes, cross-references in the margin and headings. For right-to-left scripts, Left and Right are swapped.
* **First Line Indent Factor**, **Left Indent Factor** and **Right Indent Factor** – indents, as a multiple of the **Base Indent** on the **Layout** tab. A negative first line indent makes a "hanging" indent: the first line starts further left than the other lines. Poetry and list markers often use this.
* **Line Spacing Factor** – the space between lines, compared with the base line spacing. Tick **Use Absolute Spacing (in pts)** to give the line spacing as an exact number of points instead. The label then changes to **Baseline**, and PTXprint converts the number for you.
* **Space Before Factor** and **Space After Factor** – extra space above and below the paragraph, as a multiple of the base line spacing. 1.0 is about one empty line. 0.5 is about half a line.
* **Maximum Ragged Space** – for paragraphs that are not justified, how much of the line may stay empty at the ragged edge.

## Other Settings

The **Other Settings** area holds settings that are used only by some markers. PTXprint opens the part that fits the marker you selected.

* **Note Settings** (for footnotes `\f`, cross-references `\x` and similar notes): the style and raise of the caller (the small letter or symbol in the text and at the start of the note), and **Note Blend Into**, which puts these notes together with another kind of note.
* **Table Settings** (for table cells `\tc`): how text sits from top to bottom in a cell when the cells in a row have different heights.
* **Sidebar Settings** (for sidebar categories, and for the text border): see the next section.

## Sidebars

A **sidebar** is a box of extra text, for example a study note about a place or a person, separate from the Scripture text. In USFM a sidebar starts with `\esb`, then a category such as `\cat people\cat*`, and ends with `\esbe`. All sidebars with the same category share one style. The style for the category "people" has the marker name `cat:people|esb`. PTXprint itself also uses sidebar styles, for example for the parts of the cover, for the automatic boxes around headings and titles, and `cat:box|esb` for simple boxes.

When you select a sidebar style, the **Sidebar Settings** area opens:

* **Color** and **Alpha** – the background colour of the box and how solid it is (0 = clear, 1 = solid).
* **Width** – the width of the box compared with the column or page. 1 is the full width. 0.5 is half the width.
* **Borders...** – opens the **Border Settings** dialog for lines and ornaments around the box (see the **Tabs+Borders** chapter).
* **Foreground Image...** – adds a small picture (a logo) inside each box of this category. See **Sidebar Image Settings** below.
* **Background Image...** – adds a picture behind the text of the box, like a watermark.
* **Size and Position...** – where the box goes on the page. The result is shown as a short code in the box beside the button.

The text inside a sidebar can have its own styles. For example, the paragraphs inside the "people" sidebars use the marker `cat:people|p`. If such a style exists, you can change it like any other style. If not, you can add it (see **Common tasks**).

## Size and Position Settings (dialog)

This dialog opens from **Size and Position...** in the **Sidebar Settings** area. (The same dialog is also used for maps on the **Pictures** tab.) A small picture shows roughly where the box will go.

1. Choose the **Frame Size** first: **Column Width**, **Span Width** (across all columns), **Page (in Margins)** or **Page (to Edge)**.
2. Then choose the **Vertical Position**. The choices depend on the frame size:
   * Column width: **Top**, **Bottom**, **Before Verse**, **After Paragraph** or **Cutout**.
   * Span width: **Top**, **Bottom** or **Below Notes** (below the footnotes).
   * Page sizes: **Top**, **Center**, **Fill** (stretch the box to fill the page) or **Bottom**.
3. Then choose the **Horizontal Position**. **Center** is only offered for page sizes and for **Before Verse** and **After Paragraph**. For **Span Width** this list is greyed out.
4. For **After Paragraph** and **Cutout** you can set **Number of Lines** (for After Paragraph it becomes "Number of paragraphs"). A positive number moves the box down, a negative number moves it up.

Click **OK** to save the position.

A **cutout** is a notch in the text: the text flows around the box at the side of the column.

## Sidebar Image Settings (dialog)

This dialog opens from **Foreground Image...** or **Background Image...**. The title shows which one you are setting.

* Click **Select...** to choose an image (.jpg, .png or .pdf). Line art in PDF format works best over a coloured background, because .jpg images cannot be transparent.
* **Scale** sets the size of the image compared with the box. Tick **Maintain Aspect Ratio** to keep the shape of the picture (the height then follows the width).
* For a foreground image, choose where it goes in the box: **Above or Below Text**, **Beside Text** or **Cutout Within Text**, then choose the exact place in the list beside your choice.
* For a background image, the **Background Image Advanced Settings** set its transparency, layer order, what happens if it is too big, and what part of the box it should fill.
* Click **Remove Image** and then **OK** to take the image away.

## Add/Edit Style (dialog)

This dialog opens from **Add** or **Edit** on the **Styles** tab. Use it to describe a marker: its code, name, description, type and end marker. The formatting itself (font, size, spacing) is then set on the **Styles** tab as usual. Creating new markers is an advanced task. Most users only need it for special markers that their project already uses (for example markers starting with `z`), or for special cases such as a sidebar category.

* When you click **Add**, the new style starts as a copy of the style that is selected. So first select a similar marker, then click **Add**.
* When you click **Edit**, the **Marker** box is greyed out, because you cannot rename a marker. For standard USFM markers the **Type** is also greyed out.
* The **Name** controls where the marker appears in the list. Use the form `marker - Category - short description`, for example `zpeople - Paragraph - Paragraph about people`. The middle part places the marker in a category (for example `Paragraph` goes into **Paragraphs**). When you type in **Marker**, PTXprint updates the start of the name for you.

## Common tasks

### Find the style for some text

1. Open the **Styles** tab.
2. If you do not know the marker, look at the text in Paratext with the "Unformatted" view, or on the **View+Edit** tab in PTXprint, to see which marker is in front of it.
3. Type the marker code (for example `s1`) or a word (for example `heading`) in the **Find** box.
4. Or click the filter button next to **Find** to see only the markers used in your books.

### Make section headings bigger and bold

1. On the **Styles** tab, type `s1` in **Find**.
2. In **Character Settings**, change **Font Size Factor**, for example from 1.0 to 1.2.
3. Tick **Bold**.
4. Click **Print (Make PDF)**.

### Put more space above and below headings

1. Select the heading marker (for example `s1`).
2. In **Paragraph Settings**, increase **Space Before Factor** (for example to 1.0) and **Space After Factor** (for example to 0.5).
3. Print again and check the result.

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
3. Change **First Line Indent Factor** or **Left Indent Factor** if needed. These are multiples of the **Base Indent** on the **Layout** tab.

### Leave some text out of the PDF

1. Select the marker, for example `rem` or a study-note marker.
2. Untick **Include Contents of Marker**.
3. The marker now has a line through it in the list. Print again.

### Undo changes to a style

* To undo one setting: click its bold name.
* To undo all changes to the style: click the Reset (circular-arrows) button.

### Give a sidebar category a coloured background

1. Find the style for the category, for example type `esb` in **Find**. If your category (for example "people") has no style yet, select `cat:box|esb`, click **Add**, type `cat:people|esb` in **Marker**, give it a **Name** and click **OK**.
2. In **Other Settings › Sidebar Settings**, click the **Color** button and choose a light colour. Set **Alpha** (for example 0.5).
3. Click **Size and Position...** to choose where the box goes, and **Borders...** for a border.
4. Print again.

## Common problems

**My change on the Styles tab has no effect.**
* You may have changed the wrong marker. Check which marker the text really uses (for example `\s2` instead of `\s1`, or `\q2` instead of `\q1`). Each level has its own style.
* A more specific style may win. For example, a style for `cat:people|p` is used for paragraphs inside "people" sidebars instead of `p`.
* The file `ptxprint-mods.sty` (edited from the **Advanced** tab) is applied last and may set the same value.
* You did not print again. Click **Print (Make PDF)**.

**The Font Size Factor and Line Spacing boxes are greyed out.**
You have selected `\p`. Change the main text size and line spacing on the **Layout** tab (**Base Font Size** and **Base Line Spacing**).

**The whole Styles tab is greyed out.**
**Lock UI Layout Settings** on the **Advanced** tab is ticked. Untick it.

**I cannot see the Styles tab.**
The tab is hidden in the **Mini** and **Basic** views. Change to the **Default** or **Full** view.

**I set a colour, but the text is still black.**
**Enable Colored Text** on the **Fonts+Script** tab is not ticked. Tick it.

**I chose Justified, but the text is not justified.**
**Justify Paragraphs** on the **Body** tab is not ticked. Then **Justified** is treated as **Left**.

**Some text is in the wrong font.**
The style for that marker has its own font (its **Font** label is bold). Click the bold **Font** label to go back to the main font. If the font has no bold or italic face, PTXprint may make a faux (computer-made) bold or slant. This is shown next to the font size.

**Some text is missing from the PDF.**
**Include Contents of Marker** may be unticked for that marker (it has a line through it in the list). Tick it.

**The Raise box is greyed out.**
**Superscript** is ticked. Superscript sets its own raise.

**The Del button does nothing.**
You can only delete styles that you added yourself. Standard styles cannot be deleted. Use the Reset button to remove your changes instead.

**The More Info... link is missing or greyed out.**
It is only shown in the **Full** view, and only when internet use is allowed on the **Advanced** tab. For combined or custom markers there is no documentation page, so the link is greyed out.

## Settings reference: Styles tab

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Size and Position Settings (dialog)

#### OK

- **Where:** Size and Position Settings (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Explanation:**

Saves the chosen size and position, and closes the dialog.

*(Internal ID: `button1`)*

#### Cancel

- **Where:** Size and Position Settings (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Explanation:**

Closes the dialog without changing the position.

*(Internal ID: `button2`)*

#### Frame Size

- **Where:** Size and Position Settings (dialog)
- **Type:** Drop-down list
- **Description:** Sidebar: Frame size
- **View level:** Default and Full views
- **Choices:** Column Width; Span Width; Page (in Margins); Page (to Edge)

**Tooltip (the text shown when you hover the mouse over it):**

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

**Explanation:**

Choose this first, because it changes the choices in the other lists. **Column Width** gives the most placement options. **Span Width** goes across all columns and can only be at the top, bottom or below the notes. The two page sizes are for boxes that take a whole page, for example on covers. In a one-column layout, Column Width and Span Width are the same.

*(Internal ID: `fcb_sbSize`)*

#### Vertical Position

- **Where:** Size and Position Settings (dialog)
- **Type:** Drop-down list
- **Description:** Sidebar: Vertical position
- **View level:** Default and Full views
- **Choices:** Top; Bottom; Below Notes; Before Verse; After Paragraph; Cutout; Fill

**Tooltip (the text shown when you hover the mouse over it):**

> Top: Above everything except the header line Bottom: Below all verse text (and footnotes in diglot) Before Verse: 'Here' where defined or before its Anchor Ref After Paragraph: After this paragraph Cutout: A notch/corner cut out of the text, starting at current line Below Notes: Below the footnotes (Span Width only) Fill: Stretch to fill the page (page sizes only)
>
> The above options may have other positioning parameters such as: Left, Right, Center, no. of lines (up or down).
>
> Top: Above everything except the header line Bottom: Below all verse text (and footnotes in diglot) Before Verse: 'Here' where defined or before its Anchor Ref After Paragraph: After this paragraph Cutout: A notch/corner cut out of the text, starting at current line
>
> The above options may have other positioning parameters such as: Left, Right, Center, no. of lines (up or down).

**Explanation:**

Choose where the box goes from top to bottom. **Before Verse** puts it where it is in the text. **After Paragraph** puts it after the current paragraph (or later, with **Number of Lines**). **Cutout** makes the text flow around the box. **Below Notes** (span width only) puts it under the footnotes. **Fill** (page sizes only) stretches the box to fill the page.

*(Internal ID: `fcb_sbPgPos`)*

#### Horizontal Position

- **Where:** Size and Position Settings (dialog)
- **Type:** Drop-down list
- **Description:** Sidebar: Horizontal position
- **View level:** Default and Full views
- **Choices:** Left; Center; Right; Inner; Outer; -

**Tooltip (the text shown when you hover the mouse over it):**

> The options available here change based on the Frame Size and Vertical Position settings. So if you can't find an option you are looking for, then check those settings first.

**Explanation:**

Choose the side: Left, Right, Inner (spine side), Outer (edge side) or Center. If the side you want is not offered, change **Frame Size** or **Vertical Position** first. Greyed out for **Span Width**.

*(Internal ID: `fcb_sbHoriz`)*

#### Number of Lines

- **Where:** Size and Position Settings (dialog)
- **Type:** Number box
- **Description:** Sidebar/map: Lines to adjust vertically
- **View level:** Default and Full views
- **Values:** from -24 to 24

**Tooltip (the text shown when you hover the mouse over it):**

> Some vertical position options allow a sidebar to be moved up or down by a number of lines or paragraphs.
>
> -Negative (minus) values specify to move UP. +Positive (plus) values specify to move DOWN.
>
> Negative counts for cutouts raise the sidebar, but the cutout will not affect earlier paragraphs. Note that negative and fractional paragraph counts are invalid.

**Explanation:**

Only available for **After Paragraph** (then it counts paragraphs, whole numbers only) and **Cutout** (then it counts lines). Positive numbers move the box down, negative numbers move it up. For other positions it is greyed out.

*(Internal ID: `s_sbLines`)*

### Sidebar Image Settings (dialog)

#### Remove Image

- **Where:** Sidebar Image Settings (dialog)
- **Type:** Button
- **Description:** Sidebar FG/BG: Remove image
- **View level:** Default and Full views

**Explanation:**

Clears the chosen image. Then click **OK** to remove the image from this sidebar style.

*(Internal ID: `btn_removeSBimage`)*

#### OK

- **Where:** Sidebar Image Settings (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Saves the image settings for this sidebar style. If no image file is chosen, the image is removed.

*(Internal ID: `btn_image_ok`)*

#### Cancel

- **Where:** Sidebar Image Settings (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog without changing anything.

*(Internal ID: `btn_image_cancel`)*

### Sidebar Image Settings (dialog) › Sidebar Foreground/Background

#### Select...

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background
- **Type:** Button
- **Description:** Sidebar FG/BG: Select an image
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Choose the image file (JPG, PNG or PDF).

**Explanation:**

Choose the image file (.jpg, .png or .pdf). The file name is shown next to the button.

*(Internal ID: `btn_sbSelectFile`)*

#### Scale

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background
- **Type:** Number box
- **Description:** Sidebar FG/BG: Scale of image
- **View level:** Default and Full views
- **Values:** from 0.01 to 2, default 1

**Tooltip (the text shown when you hover the mouse over it):**

> Specify how much the image should be scaled horizontally.

**Explanation:**

The size of the image compared with the width of the sidebar box. If **Maintain Aspect Ratio** is ticked, this value is also used for the height.

*(Internal ID: `s_sbi_scaleWidth`)*

#### Scale

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background
- **Type:** Number box
- **Description:** Sidebar FG/BG: Height of image
- **View level:** Default and Full views
- **Values:** from 0.01 to 2, default 1
- **Greyed out when:** “Maintain Aspect Ratio” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Specify how much the image should be scaled vertically.

**Explanation:**

The size of the image compared with the height of the box. Greyed out while **Maintain Aspect Ratio** is ticked. Changing width and height separately can stretch the picture.

*(Internal ID: `s_sbi_scaleHeight`)*

#### Maintain Aspect Ratio

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background
- **Type:** Checkbox (ticked by default)
- **Description:** Sidebar FG/BG: Maintain aspect ratio
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Scale the width and height the same so that the image maintains its proportions.

**Explanation:**

Keep this ticked so the picture keeps its shape. Untick it only if you want to set the height separately.

*(Internal ID: `c_sbi_lockRatio`)*

### Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Foreground Image Position Within Sidebar

#### Sidebar foreground image: Beside text options

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Foreground Image Position Within Sidebar
- **Type:** Drop-down list
- **View level:** Default and Full views
- **Choices:** Left; Inner; Right; Outer; Left Top; Inner Top; Right Top; Outer Top; Left Centre; Inner Centre; Right Centre; Outer Centre; Left Bottom; Inner Bottom; Right Bottom; Outer Bottom
- **Only available when:** “Beside Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Which side of the sidebar text the foreground image goes on (Left, Inner, Right or Outer), and whether it sits at the top, centre or bottom of that side.

**Explanation:**

The place of the image when **Beside Text** is chosen: which side (left, inner, right, outer), and optionally top, centre or bottom of that side.

*(Internal ID: `fcb_sbi_posn_beside`)*

#### Above or Below Text

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Foreground Image Position Within Sidebar
- **Type:** Radio button
- **Description:** Sidebar foreground image: Above or below text
- **View level:** Default and Full views

**Explanation:**

Puts the foreground image in its own strip above or below the text of the box. Then choose the exact place in the list beside it.

*(Internal ID: `r_sbiPosn_above`)*

#### Beside Text

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Foreground Image Position Within Sidebar
- **Type:** Radio button
- **Description:** Sidebar foreground image: Beside text
- **View level:** Default and Full views

**Explanation:**

Puts the foreground image in its own column beside the text of the box. The text is narrower for the full height of the box.

*(Internal ID: `r_sbiPosn_beside`)*

#### Cutout Within Text

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Foreground Image Position Within Sidebar
- **Type:** Radio button
- **Description:** Sidebar foreground image: Cutout within sidebar
- **View level:** Default and Full views

**Explanation:**

Puts the foreground image in a notch in the text of the box, so the text flows around it. This leaves the least empty space.

*(Internal ID: `r_sbiPosn_cutout`)*

#### Sidebar foreground image: Above or below options

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Foreground Image Position Within Sidebar
- **Type:** Drop-down list
- **View level:** Default and Full views
- **Choices:** Top; Top-Left; Top-Inner; Top-Centre; Top-Right; Top-Outer; Bottom; Bottom-Left; Bottom-Inner; Bottom-Centre; Bottom-Right; Bottom-Outer
- **Only available when:** “Above or Below Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Where the foreground image goes when it is placed in its own strip above or below the sidebar text: Top or Bottom, and Left, Inner, Centre, Right or Outer.

**Explanation:**

The place of the image when **Above or Below Text** is chosen: top or bottom, and left, inner, centre, right or outer.

*(Internal ID: `fcb_sbi_posn_above`)*

#### Sidebar foreground image: Cutout position options

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Foreground Image Position Within Sidebar
- **Type:** Drop-down list
- **View level:** Default and Full views
- **Choices:** Left; Inner; Right; Outer
- **Only available when:** “Cutout Within Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Which side of the sidebar text the cutout for the foreground image is on.

**Explanation:**

The side of the cutout when **Cutout Within Text** is chosen: left, inner, right or outer.

*(Internal ID: `fcb_sbi_posn_cutout`)*

#### Start N Lines Below Top

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Foreground Image Position Within Sidebar
- **Type:** Number box
- **Description:** Sidebar foreground image: Adjust cutout position
- **View level:** Default and Full views
- **Values:** default 2
- **Only available when:** “Cutout Within Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> The number of lines below the top of the sidebar text where the cutout for the foreground image starts.

**Explanation:**

How many lines below the top of the box the cutout for the image starts. Use it to keep the image away from the first lines of text, for example below a heading inside the box.

*(Internal ID: `s_sbiCutoutLines`)*

### Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Background Image Advanced Settings

#### Background Image Transparency

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Background Image Advanced Settings
- **Type:** Number box
- **Description:** Sidebar background image: Transparency (alpha)
- **View level:** Default and Full views
- **Values:** default 0.5

**Tooltip (the text shown when you hover the mouse over it):**

> Transparency or alpha value of the background image: 0 is transparent, 1 is solid. This is useful for turning black lines into a paler shade.
>
> Note that this will allow the background colour to show through, even if the image is above the background layer, so on a green background black will become a darker shade of green, not grey.

**Explanation:**

How solid the background image is: 0 is invisible and 1 is solid. A value such as 0.3 makes a watermark that does not make the text hard to read.

*(Internal ID: `s_sbiAlpha`)*

#### Color

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Background Image Advanced Settings
- **Type:** Colour picker
- **Description:** Sidebar background image: Color
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Some (rare) PDF line-art images do not set the colour of their lines, relying instead on the 'default' colour, which is normally black. This control sets the default colour to something other than black, and thus such images can be recoloured with this option. If (as most PDF images do) the image defines its own colour, this option will have no visible effect at all. It is also possible that an image will *partly* contain colour information, but only starting part way through the file, a situation that might produce unexpected results.

**Explanation:**

Changes the colour of the lines of a few simple PDF line-art images. Most images have their own colours, and then this has no effect.

*(Internal ID: `col_sbiBgColor`)*

#### Background Image Transparency

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Background Image Advanced Settings
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Transparency or alpha value of the background image: 0 is transparent, 1 is solid. This is useful for turning black lines into a paler shade.
>
> Note that this will allow the background colour to show through, even if the image is above the background layer, so on a green background black will become a darker shade of green, not grey.

#### Layer Order

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Background Image Advanced Settings
- **Type:** Drop-down list
- **Description:** Sidebar background image: Order of layers
- **View level:** Default and Full views
- **Choices:** In Front of Background; Behind Background

**Tooltip (the text shown when you hover the mouse over it):**

> Only relevant where there is both a background image  
> *and* a background color. Set whether the background image should come above or behind the color. Line art PDFs with a transparent background may display better above the color layer, as the color layer will not then wash them out, but .JPGs are probably better behind, as .JPG images do not have transparency.
>
> Only relevant where there is both a background image  
> *and* a background color. Set whether the background image should come above or behind the color. Line art PDFs with a tranpsarent background may display better above the color layer, as the color layer will not then wash them out, but .JPGs are probably better behind, as .JPG images do not have transparency.

**Explanation:**

Only matters when the box has both a background colour and a background image. **In Front of Background** puts the image on top of the colour; this is good for PDF line art. **Behind Background** puts it under the colour; this is better for .jpg photos.

*(Internal ID: `fcb_sbiLayerOrder`)*

#### If Image Is Oversized

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Background Image Advanced Settings
- **Type:** Drop-down list
- **Description:** Sidebar background image: Oversize management
- **View level:** Default and Full views
- **Choices:** Ignore (overflows frame); Shrink (maintains ratio); Squash (distorts ratio); Crop (unimplemented)

**Tooltip (the text shown when you hover the mouse over it):**

> Select what action should be taken if the background image size is specified with a single dimension (height or width) and the unspecified dimension ends up being too large for a given sidebar.

**Explanation:**

What happens if the image is too big for the box. **Ignore** lets it stick out of the box. **Shrink** makes it smaller and keeps its shape. **Squash** makes it fit and may change its shape. **Crop** is not working yet.

*(Internal ID: `fcb_sbiOversize`)*

#### Crop Offset

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Background Image Advanced Settings
- **Type:** Text box
- **Description:** Sidebar background image: Crop offset (XxY)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Crop offset in the format XxY (e.g. 10x20). Only used when Oversize is set to Crop. Shifts the cropped region by X points horizontally and Y points vertically.

**Explanation:**

Only for the **Crop** choice in **If Image Is Oversized**, which is not working yet. Leave it empty.

*(Internal ID: `t_sbiBgCropOfs`)*

#### Scale To

- **Where:** Sidebar Image Settings (dialog) › Sidebar Foreground/Background › Background Image Advanced Settings
- **Type:** Drop-down list
- **Description:** Sidebar background image: Scale Image to Inner/Outer/Bleed area
- **View level:** Default and Full views
- **Choices:** bleed: overflow the page into the cropped area; colbleed: overflow the page into the cropped area as much as the colours do (normally images bleed less); inner: the area that text could cover (vertically this extends to the inner edge of the border); outer: the outermost of the coloured box or the border; border: the outer edge of the border; box: the coloured box

**Tooltip (the text shown when you hover the mouse over it):**

> Select where the image should extend to.

**Explanation:**

Which area of the box the background image is sized to: the text area (**inner**), the coloured box (**box**), the border (**border**), the outermost of these (**outer**), or out past the page edge (**bleed** and **colbleed**, mainly for covers).

*(Internal ID: `fcb_sbiScaleTo`)*

### Add/Edit Style (dialog)

#### OK

- **Where:** Add/Edit Style (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Saves the style details. A new style is added to the list and selected, ready for you to set its formatting.

*(Internal ID: `btn_sty_ok`)*

#### Cancel

- **Where:** Add/Edit Style (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog without adding or changing a style.

*(Internal ID: `btn_sty_cancel`)*

#### Description

- **Where:** Add/Edit Style (dialog)
- **Type:** Label
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> You can say what you like here to describe the purpose of the style.

#### ⚠️Marker

- **Where:** Add/Edit Style (dialog)
- **Type:** Text box
- **Description:** Add/Edit marker dialog: Marker (code)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The marker code without the backslash, e.g. zpeople. It can only be set when adding a new style.

**Explanation:**

The marker code, without the backslash, for example `zpeople` or `cat:people|esb`. You can only type here when adding a new style. If you leave it empty and click **OK**, nothing is created.

*(Internal ID: `t_styMarker`)*

#### Add/Edit marker dialog: Marker description

- **Where:** Add/Edit Style (dialog)
- **Type:** Text area
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> You can say what you like here to describe the purpose of the style.

**Explanation:**

A longer description of what the marker is for. It is only for your information.

*(Internal ID: `textv_styDesc`)*

#### Name

- **Where:** Add/Edit Style (dialog)
- **Type:** Label
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Consists of: Marker..Endmarker - Group - short description and helps to place the marker in the tree listing all markers.

#### Name

- **Where:** Add/Edit Style (dialog)
- **Type:** Text box
- **Description:** Add/Edit marker dialog: Marker name (short description)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Consists of: Marker..Endmarker - Group - short description and helps to place the marker in the tree listing all markers.

**Explanation:**

A name in the form `marker - Category - short description`. The middle part decides in which category of the marker list the style appears (for example `Paragraph`, `Character`, `Heading`). PTXprint updates the start of the name when you type a marker code.

*(Internal ID: `t_styName`)*

#### End Marker

- **Where:** Add/Edit Style (dialog)
- **Type:** Text box
- **Description:** Add/Edit marker dialog: End Marker (code)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> If the closing marker for this marker is not the same as the marker followed by a * then enter it here. For example, with paired milestones, do not create a new milestone just specify the closing milestone marker here.

**Explanation:**

Usually leave this empty. For character and note markers PTXprint adds the end marker for you (the marker followed by `*`). For a pair of milestone markers, type the closing milestone here.

*(Internal ID: `t_styEndMarker`)*

#### ⚠️Type

- **Where:** Add/Edit Style (dialog)
- **Type:** Drop-down list
- **Description:** Add/Edit marker dialog: Marker type
- **View level:** Default and Full views
- **Choices:** Header; Title; Introduction; Introduction Character; Section Paragraph; Verse Paragraph; Character; List; List Character; Milestone; Standalone Milestone; Other Paragraph; Cross Reference; Cross Reference Character; Footnote; Footnote Character; Cell; Attribute; Identification; Internal

**Tooltip (the text shown when you hover the mouse over it):**

> [Required] This tells PTXprint what kind of marker this is.
>
> [Required] This tells PTXprint what kind of a marker this is.

**Explanation:**

Required. Tells PTXprint what kind of marker this is, for example **Verse Paragraph** for a body text paragraph, **Section Paragraph** for a heading, **Character** for a few words inside a paragraph, or **Footnote**. It cannot be changed for standard USFM markers.

*(Internal ID: `fcb_styType`)*

#### [Required] This tells PTXprint how to layout data in this ma...

- **Where:** Add/Edit Style (dialog)
- **Type:** Text box
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> [Required] This tells PTXprint how to layout data in this marker. For normal, vernacular body text, use VerseText. If this is part of a heading, use Section. If it is part of the title block of a book, use Title. NoteText makes this a kind of footnote, like \x.

### Styles tab

#### Find

- **Where:** Styles tab
- **Type:** Search box
- **Description:** Find style
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> If you are not sure which category your marker can be found under, then use this Search tool to find the marker you need.

**Explanation:**

Type a marker code (the backslash is optional) or part of a marker's name. PTXprint waits half a second, then selects the first match, opens the categories that contain matches and colours every matching line pale peach. Clear the box to remove the colouring.

*(Internal ID: `t_styleSearch`)*

#### Enable (or disable) the filter to only show markers that are...

- **Where:** Styles tab
- **Type:** Toggle button (not ticked by default)
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Enable (or disable) the filter to only show markers that are in use in the current set of books.

**Explanation:**

This button has a bulleted-list icon. When it is pressed in, the list shows only the markers that are used in the books currently chosen for printing, and all categories are opened. Press it again to see all markers. If your text has a USFM error, PTXprint shows an error message instead.

*(Internal ID: `btn_styleFilter`)*

#### tv_Styles

- **Where:** Styles tab
- **Type:** Table
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Explanation:**

The list of all markers, grouped by category (bold blue lines). Click a marker to show its settings on the right. A line through a marker means it is not printed (**Include Contents of Marker** is unticked).

*(Internal ID: `tv_Styles`)*

#### Include Contents of Marker

- **Where:** Styles tab
- **Type:** Checkbox (ticked by default)
- **Description:** Styles: Include marker contents in PDF
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Uncheck this option to set the marker to "non-publishable" so the contents of this marker will not be included in the output.

**Explanation:**

Untick to leave all text inside this marker out of the PDF. Tick it to print markers that are hidden by default, such as `\rem`. For the automatic heading box, title box and text border, PTXprint sets this box for you when you turn those features on or off on the **Tabs+Borders** tab.

*(Internal ID: `c_styTextProperties`)*

### Styles tab › Include Contents of Marker

#### More Info...

- **Where:** Styles tab › Include Contents of Marker
- **Type:** Link
- **View level:** Not normally shown
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Explanation:**

Opens the official USFM documentation page for the selected marker in your web browser. For some interface languages, the page is opened through an automatic translation, unless **Only Use English Links** is ticked on the **Advanced** tab. Shown only in the **Full** view and when internet use is allowed. Greyed out for combined or custom markers.

*(Internal ID: `l_url_usfm`)*

#### Add

- **Where:** Styles tab › Include Contents of Marker
- **Type:** Button
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Find a style within the appropriate section which is similar to the new style you wish to create. Then click this Add button to create a new style based on the currently selected style.

**Explanation:**

Creates a new style. Select a similar existing style first, because the new style starts as a copy of it. Then fill in the **Add/Edit Style** dialog. This is an advanced task.

*(Internal ID: `btn_styAdd`)*

#### Del

- **Where:** Styles tab › Include Contents of Marker
- **Type:** Button
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to delete this style (only styles you have added can be deleted). Warning: There is no confirmation or undo!

**Explanation:**

Deletes the selected style, without asking. It only works for styles that you added yourself; for standard styles nothing happens.

*(Internal ID: `btn_styDel`)*

#### Click to remove all changes made to this style, returning it...

- **Where:** Styles tab › Include Contents of Marker
- **Type:** Button
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to remove all changes made to this style, returning it to the values in the underlying stylesheets.

**Explanation:**

The circular-arrows button. It removes all changes you have made on this tab to the selected style, so it goes back to the values from the underlying stylesheets. To reset only one setting, click that setting's bold name instead. Be careful with styles you created yourself: Reset also clears the settings you gave them.

*(Internal ID: `btn_styReset`)*

#### Edit

- **Where:** Styles tab › Include Contents of Marker
- **Type:** Button
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to Edit additional properties for this style.

**Explanation:**

Opens the **Add/Edit Style** dialog for the selected style, so you can change its name, description, type or end marker. The marker code itself cannot be changed here.

*(Internal ID: `btn_styEdit`)*

#### Hover-help

- **Where:** Styles tab › Include Contents of Marker
- **Type:** Label
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Hover over these help topics to gain a greater understanding about how the Styles editor works.

#### Why are some parameters bold?

- **Where:** Styles tab › Include Contents of Marker
- **Type:** Label
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> When a setting's name is in bold it indicates that the value is different from what is in the stylesheet.
>
> Note that you can click on a bold setting name of any parameter to RESET it to the stylesheet value.

#### How are Stylesheets applied?

- **Where:** Styles tab › Include Contents of Marker
- **Type:** Label
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

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

### Styles tab › Include Contents of Marker › Character Settings

#### Select Font...

- **Where:** Styles tab › Include Contents of Marker › Character Settings
- **Type:** Button
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Explanation:**

Opens the font picker to choose a font just for this marker. If you choose nothing, the marker uses the main font from the **Fonts+Script** tab. When a font is set, the **Font** label is bold; click the bold label to go back to the main font.

*(Internal ID: `bl_font_styFontName`)*

#### Font Size Factor

- **Where:** Styles tab › Include Contents of Marker › Character Settings
- **Type:** Number box
- **Description:** Styles: Font size factor
- **View level:** Default and Full views
- **Values:** from 0.1 to 50, default 1
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This is a factor or proportion of the base font size. So 1.0 is the same as the base font size from the Layout tab. (Not available for \p, which always uses the Base Font Size.)

**Explanation:**

1.0 means the same size as the **Base Font Size** on the **Layout** tab; 0.8 is smaller and 1.5 is bigger. The real size in points is shown under the font button. Greyed out for `\p`, whose size is the base font size. If **Scale Relative to Parent** is ticked, this box becomes **Font Scale** and is relative to the surrounding text.

*(Internal ID: `s_styFontSize`)*

#### Scale Relative to Parent

- **Where:** Styles tab › Include Contents of Marker › Character Settings
- **Type:** Checkbox (not ticked by default)
- **Description:** Styles: Scale relative to parent
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Normally the Font Size is relative to the Base Font Size (Layout tab). Tick this to make it relative to the size of the surrounding text instead. Note that  
> \p has a FontSize of 12 in the underlying stylesheet.

**Explanation:**

Tick this when the size should follow the surrounding text, for example for a character style that should always be 80% of whatever paragraph it is in. When ticked, the size box label changes to **Font Scale**.

*(Internal ID: `c_styFontScale`)*

#### Bold

- **Where:** Styles tab › Include Contents of Marker › Character Settings
- **Type:** Checkbox (not ticked by default)
- **Description:** Styles: Bold
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Explanation:**

Makes the text of this marker bold. If the font has no real bold face, PTXprint may use a faux (computer-made) bold, depending on the settings on the **Fonts+Script** tab.

*(Internal ID: `c_styFaceBold`)*

#### Italic

- **Where:** Styles tab › Include Contents of Marker › Character Settings
- **Type:** Checkbox (not ticked by default)
- **Description:** Styles: Italic
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Explanation:**

Makes the text of this marker italic. If the font has no real italic face, a computer-made slant may be used.

*(Internal ID: `c_styFaceItalic`)*

#### Superscript

- **Where:** Styles tab › Include Contents of Marker › Character Settings
- **Type:** Checkbox (not ticked by default)
- **Description:** Styles: Superscript
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The superscript option overrides these settings:  
>    Font Size Factor is set to 0.75  
>    Raise is set to 0.85 times the x-height of the font (which  
>    defaults to 1/2 the ascent if not specified in the font).

**Explanation:**

Makes the text small and raised, as for verse numbers or footnote callers. While it is ticked, the **Raise** box is greyed out.

*(Internal ID: `c_styFaceSuperscript`)*

#### SmallCaps

- **Where:** Styles tab › Include Contents of Marker › Character Settings
- **Type:** Checkbox (not ticked by default)
- **Description:** Styles: Smallcaps
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Explanation:**

Prints lowercase letters as small capital letters. This needs a font that supports small capitals, and it only has an effect in scripts that have upper and lower case. It is often used for `\nd` (LORD).

*(Internal ID: `c_stySmallCap`)*

#### Raise

- **Where:** Styles tab › Include Contents of Marker › Character Settings
- **Type:** Number box
- **Description:** Styles: Raise
- **View level:** Default and Full views
- **Values:** from -50 to 50
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Superscript”, “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> How much to raise the text (in pts).

**Explanation:**

Moves the text up by this many points (a negative number moves it down). Use small values. Raised text cannot break across lines, so use it only for short pieces of text.

*(Internal ID: `s_styRaise`)*

#### Color: x001122

- **Where:** Styles tab › Include Contents of Marker › Character Settings
- **Type:** Colour picker
- **Description:** Styles: Color
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Sets text color for text in this style.

**Explanation:**

Click to choose a text colour. The colour code is shown next to the label. When you choose a colour, PTXprint also ticks **Enable Colored Text** on the **Fonts+Script** tab; if that box is later unticked, the colour does not print. Click the bold **Color** label to remove your colour.

*(Internal ID: `col_styColor`)*

#### Underline

- **Where:** Styles tab › Include Contents of Marker › Character Settings
- **Type:** Checkbox (not ticked by default)
- **Description:** Styles: Underline
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Note that underlining in printed scripture text is actively discouraged.

**Explanation:**

Underlines the text of this marker. Underlining is usually avoided in printed Scripture.

*(Internal ID: `c_styFaceUnderline`)*

#### 11.7pt (↑6.6 ↓2.2)

- **Where:** Styles tab › Include Contents of Marker › Character Settings
- **Type:** Label
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Calculated absolute point size given the current Base Font Size (which is set on the Layout tab).
>
> The (↑Ascender ↓Descender) values from the base line for this font are provided for reference.

**Explanation:**

Shows the real font size in points (pt, about 0.35 mm) for this marker, worked out from the **Font Size Factor** and the **Base Font Size**. The arrows show how far the font's letters reach above and below the line. This is information only.

*(Internal ID: `l_styActualFontSize`)*

#### GR stretch=95% bold=1.8 ital=0.15

- **Where:** Styles tab › Include Contents of Marker › Character Settings
- **Type:** Label
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> If any modifications to the typeface have been selected, then they will be displayed here.
>
> GR= Graphite has been enabled stretch= (or shrink) font horizontally bold= embolden value (faux bold) ital= slant value (faux italics)

**Explanation:**

Shows any special changes to the font for this marker: GR (Graphite), stretch, faux bold or slant. It is empty when there are none. This is information only.

*(Internal ID: `l_styFontFeats`)*

### Styles tab › Include Contents of Marker › Paragraph Settings

#### Alignment

- **Where:** Styles tab › Include Contents of Marker › Paragraph Settings
- **Type:** Drop-down list
- **Description:** Styles: Paragraph alignment
- **View level:** Default and Full views
- **Choices:** Justified; Left; LeftBal; Center; Right; Inner; Outer
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

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

**Explanation:**

Choose how the lines line up. **Justified** gives straight edges on both sides (only if **Justify Paragraphs** is ticked on the **Body** tab). **LeftBal** is left-aligned with more even line lengths. **Inner** and **Outer** depend on which side of the page or column the text is on. Click the bold **Alignment** label to undo your change.

*(Internal ID: `fcb_styJustification`)*

#### First Line Indent Factor

- **Where:** Styles tab › Include Contents of Marker › Paragraph Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -50 to 50
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This is multiplied by the Base Paragraph Indent value (specified on the Layout tab) to get the final indentation amount.

**Explanation:**

Indent of the first line, as a multiple of the **Base Indent** on the **Layout** tab. 1 is a normal paragraph indent, 0 is no indent. A negative value gives a hanging indent, often used for poetry and lists. For sidebars this moves the whole box sideways.

*(Internal ID: `s_styFirstLineIndent`)*

#### Left Indent Factor

- **Where:** Styles tab › Include Contents of Marker › Paragraph Settings
- **Type:** Number box
- **Description:** Styles: Left indent
- **View level:** Default and Full views
- **Values:** from -100 to 100
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This is multiplied by the Base Paragraph Indent value (specified on the Layout tab) to get the final indentation amount.
>
> When the Writing system text flow direction is Right-to-Left the interpretation of Left and Right is swapped.

**Explanation:**

Indent of the left side of the whole paragraph, as a multiple of the **Base Indent**. Use it for poetry levels, quotations and lists. For right-to-left text it is the right side.

*(Internal ID: `s_styLeftMargin`)*

#### Right Indent Factor

- **Where:** Styles tab › Include Contents of Marker › Paragraph Settings
- **Type:** Number box
- **Description:** Styles: Right indent
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This is multiplied by the Base Paragraph Indent value (specified on the Layout tab) to get the final indentation amount.
>
> When the Writing system text flow direction is Right-to-Left the interpretation of Left and Right is swapped.

**Explanation:**

Indent of the right side of the whole paragraph, as a multiple of the **Base Indent**. For right-to-left text it is the left side.

*(Internal ID: `s_styRightMargin`)*

#### Line Spacing Factor

- **Where:** Styles tab › Include Contents of Marker › Paragraph Settings
- **Type:** Number box
- **Description:** Styles: Line spacing
- **View level:** Default and Full views
- **Values:** default 1
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This is a proportion of the base line spacing. So 1.0 is the same as the base line spacing from the Layout tab. If Absolute Spacing is set, then this value is the line spacing in pts.

**Explanation:**

Line spacing for this paragraph type, compared with the **Base Line Spacing** on the **Layout** tab. 1.0 is the same. If **Use Absolute Spacing** is ticked, the label changes to **Baseline** and the number is in points. Greyed out for `\p`.

*(Internal ID: `s_styLineSpacing`)*

#### Use Absolute Spacing (in pts)

- **Where:** Styles tab › Include Contents of Marker › Paragraph Settings
- **Type:** Checkbox (not ticked by default)
- **Description:** Styles: Use absolute line spacing
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The Line Spacing is usually calculated as a factor of the Font Size. If you prefer to specify an exact/absolute line spacing (in points), then enable this option.

**Explanation:**

Tick to give the line spacing as a fixed number of points instead of a factor. PTXprint converts the current value when you tick or untick it. A fixed value does not change when you change the base line spacing later. Greyed out for `\p`.

*(Internal ID: `c_styAbsoluteLineSpacing`)*

#### Space Before Factor

- **Where:** Styles tab › Include Contents of Marker › Paragraph Settings
- **Type:** Number box
- **Description:** Styles: Space before
- **View level:** Default and Full views
- **Values:** from -1 to 5
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Amount of space to insert before the paragraph. The actual space is this factor multiplied by the base line spacing from the Layout tab.

**Explanation:**

Extra space above the paragraph, as a multiple of the base line spacing. 1.0 is about one empty line. Headings often use 0.5 to 1.5.

*(Internal ID: `s_stySpaceBefore`)*

#### Space After Factor

- **Where:** Styles tab › Include Contents of Marker › Paragraph Settings
- **Type:** Number box
- **Description:** Styles: Space after
- **View level:** Default and Full views
- **Values:** from -1 to 5
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Amount of space to insert after the paragraph. The actual space is this factor multiplied by the base line spacing from the Layout tab.

**Explanation:**

Extra space below the paragraph, as a multiple of the base line spacing. 1.0 is about one empty line.

*(Internal ID: `s_stySpaceAfter`)*

#### Maximum Ragged Space

- **Where:** Styles tab › Include Contents of Marker › Paragraph Settings
- **Type:** Number box
- **Description:** Styles: Maximum ragged (fill) space
- **View level:** Default and Full views
- **Values:** default 0.25
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> How much of the column-width can be empty space at a non-justified edge? This affects mid-paragraph line-breaking and may cause stretching of other spacing if the line would be too short otherwise. It does not stop the final line of a paragraph from being shorter.
>
> This value is set as the proportion of the column width, with sensible values being with the range of 0.20 to 0.75 (where 1.00 represents the entire column width). Discretionary breaks (//) will be ignored if breaking there would leave more than this much space.

**Explanation:**

Only matters for paragraphs that are not justified. The default 0.25 means up to a quarter of the line may stay empty at the ragged edge. Larger values allow more uneven lines; smaller values make lines more even but may stretch the spaces between words.

*(Internal ID: `s_styNonJustifiedFill`)*

### Styles tab › Include Contents of Marker › Other Settings › Note Settings

#### Caller Raise

- **Where:** Styles tab › Include Contents of Marker › Other Settings › Note Settings
- **Type:** Number box
- **Description:** Note settings: Caller raise
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Raise the caller in the main text by this number of points.

**Explanation:**

How many points the note caller in the main text is raised. Leave it at 0 unless the caller sits too high or too low.

*(Internal ID: `s_styCallerRaise`)*

#### Note Caller Raise

- **Where:** Styles tab › Include Contents of Marker › Other Settings › Note Settings
- **Type:** Number box
- **Description:** Note settings: Note caller raise
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Raise the caller in the note by this number of points.

**Explanation:**

How many points the caller at the start of the note itself is raised.

*(Internal ID: `s_styNoteCallerRaise`)*

#### Caller Style

- **Where:** Styles tab › Include Contents of Marker › Other Settings › Note Settings
- **Type:** Text box
- **Description:** Note settings: Caller style
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The style which is used to style the caller in the main text. If none is specified then  
> \v is used.

**Explanation:**

Type the marker code of the style to use for the caller in the main text (without the backslash). If empty, the verse number style is used. Advanced.

*(Internal ID: `t_styCallerStyle`)*

#### Note Caller Style

- **Where:** Styles tab › Include Contents of Marker › Other Settings › Note Settings
- **Type:** Text box
- **Description:** Note settings: Note caller style
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The style which is used to style the caller in the note itself. If none is specified then  
> \v is used.

**Explanation:**

Type the marker code of the style to use for the caller at the start of the note. If empty, the verse number style is used. Advanced.

*(Internal ID: `t_styNoteCallerStyle`)*

#### Note Blend Into Style

- **Where:** Styles tab › Include Contents of Marker › Other Settings › Note Settings
- **Type:** Text box
- **Description:** Note settings: Note blend into style
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Insert the notes of the marker being defined into the collection of notes in the marker specified here.
>
> For example, if when defining the \x style, if this value was set to f then all cross references would be blended into the \f footnotes.

**Explanation:**

Type the code of another note type (for example `f`) to print these notes together with those notes, while keeping their own style. The **Notes+Refs** tab sets this for cross-references when you choose to blend them with footnotes, so normally you do not need to type anything here.

*(Internal ID: `t_NoteBlendInto`)*

### Styles tab › Include Contents of Marker › Other Settings › Table Settings

#### Table settings: Vertical position of \tc markers

- **Where:** Styles tab › Include Contents of Marker › Other Settings › Table Settings
- **Type:** Drop-down list
- **View level:** Default and Full views
- **Choices:** Top; Center; Bottom; Gridded Center
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Where text sits vertically in a table cell that is shorter than the tallest cell in the row. Gridded Center keeps the text on whole lines.

**Explanation:**

For table cells: where the text sits when a cell has fewer lines than the tallest cell in the row. **Top**, **Center** or **Bottom**. **Gridded Center** centres the text but keeps it on whole lines, so it lines up with the other cells.

*(Internal ID: `fcb_stytcVpos`)*

### Styles tab › Include Contents of Marker › Other Settings › Sidebar Settings

#### Color

- **Where:** Styles tab › Include Contents of Marker › Other Settings › Sidebar Settings
- **Type:** Colour picker
- **Description:** Sidebar settings: Color
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Sets the background color for the sidebar.
>
> Background shading color.

**Explanation:**

The background colour of this sidebar category. Choose a light colour so the text stays easy to read. Click the bold **Color** label to remove your change.

*(Internal ID: `col_sb_backColor`)*

#### Alpha

- **Where:** Styles tab › Include Contents of Marker › Other Settings › Sidebar Settings
- **Type:** Number box
- **Description:** Sidebar settings: Alpha (transparency)
- **View level:** Default and Full views
- **Values:** default 0.5
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The transparency or alpha value of the background colour:  
> 0 is transparent, 1 is solid.

**Explanation:**

How solid the sidebar background colour is: 0 is clear and 1 is solid. A value below 1 lets a background image or page decoration show through.

*(Internal ID: `s_sbAlpha`)*

#### Width

- **Where:** Styles tab › Include Contents of Marker › Other Settings › Sidebar Settings
- **Type:** Number box
- **Description:** Sidebar settings: Width
- **View level:** Default and Full views
- **Values:** from 0.25 to 2.5, default 1
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Sidebar width as a proportion of the column/page width (1.0 = full width,  
> 0.5 = half width).

**Explanation:**

The width of the sidebar compared with the column (or page) width that is chosen in **Size and Position**. 1 is the full width; 0.5 is half. Narrow boxes are useful for cutouts.

*(Internal ID: `s_sbWidth`)*

#### Borders...

- **Where:** Styles tab › Include Contents of Marker › Other Settings › Sidebar Settings
- **Type:** Button
- **Description:** Sidebar settings: Borders
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click for additional settings to control the look of borders for this category of sidebar.

**Explanation:**

Opens the **Border Settings** dialog for the selected sidebar category: border lines, colours, padding and ornaments. See the **Tabs+Borders** chapter.

*(Internal ID: `btn_sbBorders`)*

#### Foreground Image...

- **Where:** Styles tab › Include Contents of Marker › Other Settings › Sidebar Settings
- **Type:** Button
- **Description:** Sidebar settings: Foreground image settings
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click for additional settings to use a foreground image for this category of sidebar.

**Explanation:**

Opens **Sidebar Image Settings** for a foreground image: a small picture, such as a logo, shown in every box of this category (for example a scroll for history notes).

*(Internal ID: `btn_sbFGIDia`)*

#### Background Image...

- **Where:** Styles tab › Include Contents of Marker › Other Settings › Sidebar Settings
- **Type:** Button
- **Description:** Sidebar settings: Background image settings
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click for additional settings to use a background image for this category of sidebar.

**Explanation:**

Opens **Sidebar Image Settings** for a background image: a picture behind the text of the box, like a watermark.

*(Internal ID: `btn_sbBGIDia`)*

#### t_sbPgPos

- **Where:** Styles tab › Include Contents of Marker › Other Settings › Sidebar Settings
- **Type:** Text box
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Explanation:**

Shows the position code that **Size and Position...** made, for example `t` (top), `bl` (bottom left), `cr2` (cutout on the right, 2 lines down) or `Pcf` (whole page, filled). Use the **Size and Position...** button rather than typing here.

*(Internal ID: `t_sbPgPos`)*

#### Size and Position...

- **Where:** Styles tab › Include Contents of Marker › Other Settings › Sidebar Settings
- **Type:** Button
- **View level:** Default and Full views
- **Only available when:** “Include Contents of Marker” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Choose the frame size and position of this category of sidebar on the page.

**Explanation:**

Opens the **Size and Position Settings** dialog, where you choose the frame size and the place of the sidebar on the page with a preview picture.

*(Internal ID: `btn_sbSizePosition`)*
