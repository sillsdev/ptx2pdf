# Tabs+Borders tab

## What this tab is for

This tab adds two kinds of decoration to a publication:

* **Thumb Tabs** – coloured blocks printed at the outer edge of the page, with a short book name in them. When the book is closed, the reader can see the blocks on the edge of the paper and open the book near the right Bible book. They are useful in long publications such as a whole Bible or a New Testament.
* **Ornamental Decorations** – decorative borders and graphics: a border around the page or the text, a graphic behind section headings, a decoration at the end of each book, decorated verse numbers, and borders around book titles. Some cultures value such decoration highly in Scripture publications.

Each area is collapsed until you tick its checkbox: until then you only see a short description. The tab name shows **Tabs** and **Borders**, and each word turns blue when that feature is on. The **Tabs+Borders** tab is shown in the **Default** and **Full** views.

The **Border Settings** dialog is also described in this chapter. It controls the look of a border (lines, ornaments, colours and padding). You open it from the **Styles** tab, with the **Borders...** button (see **Border Settings dialog** below).

In this chapter, "pt" means point. 1 pt is about 0.35 mm. Thumb tab sizes are in mm.

## Thumb Tabs

Tick **Thumb Tabs** to show the settings.

**Where the tabs go.** PTXprint gives each Scripture book a tab position, counting down from the top of the page. The first book gets position 1 (at the top), the next book position 2, and so on. When the positions run out, the next book starts again at the top. Front matter, glossaries and other non-Scripture books do not get a tab. The positions are worked out from all the books in the multiple-book list on the main window, even if you print only one book. So a tab for Mark is in the same place whether you print the whole NT or only Mark.

**Size.** **Height** and **Length** are in mm.

* For normal (not rotated) tabs, **Height** is how tall the tab is along the edge of the page, and **Length** is how far it reaches in from the edge.
* For rotated tabs (**Rotate Tabs** ticked), **Length** runs along the edge of the page, and **Height** is how far the tab reaches in from the edge.

**Number of Tab Positions** is how many tabs fit down the page. PTXprint calculates it from the page height, the top and bottom margins and the tab size, and recalculates it whenever these change. If you make it bigger, the tabs overlap. If you make it smaller, they spread apart.

**Grouped Tabs.** Many Bible books are short. If every book had its own position, there would be too many positions. You can make neighbouring short books share one position. Type the book codes of each group with spaces between them, and put `;` between groups. Each book still has its own name in the tab. Click the **Grouped Tabs** button to get PTXprint's default groups back.

**Restart Tabs at MAT** starts a new cycle of positions at Matthew, so the New Testament tabs start again at the top of the page.

**Rotate Tabs** turns the text so it runs along the edge of the page. This works well with narrow margins and longer names. When it is ticked, the drop-down list next to it chooses which way the text faces on left and right pages. The preview on the tab shows how the tabs will look on facing pages.

**Only Show on Odd Pages** prints the tabs only on right-hand (odd) pages. Use this for thin paper, so the tab on the back of the page does not show through.

**Tab text and colour.** By default the tab text is the short book name from the `\toc3` line of each book. **Tab Color** sets the colour of the block. The text colour, font and size come from the style: click **Edit Style** to change them on the **Styles** tab. Tabs usually use a dark block with white or light text.

The **\toc3** and **\zthumbtab** options choose where the tab text comes from (see the control notes). If the **Table of Contents** on the **Peripherals** tab is switched on but does not use `\toc3`, PTXprint selects **\zthumbtab** and greys out both options.

## Ornamental Decorations

Tick **Ornamental Decorations** to show the settings. Then tick each kind of decoration you want. A file name next to a **Select...** button shows which graphic is used. When you choose a file, the checkbox for that decoration is ticked for you. The **Select...** buttons open PTXprint's own folder of border art, but you can pick a PDF file from anywhere.

### Section Headings

This puts a decoration on section headings. There are two methods:

* **PDF border (Legacy)** – a PDF graphic is placed behind each section heading (`\s`, `\s1` and `\s2`). Choose the file with **Select...**. **Scale** changes its size (1 = the size of the graphic). **Shift** moves it up (negative values) or down (positive values), in pt. The graphic does not grow with the heading, so make sure each heading fits inside it, also when a heading needs two lines. You may need to add space before and after headings on the **Styles** tab.
* **Dynamic Border** – PTXprint draws a box around each heading block, and the box grows and shrinks with the heading. It is controlled by the special style `cat:headingsbox|esb`. Click the link to open that style on the **Styles** tab, where you can set its background colour and border (with the **Borders...** button).

### Border

This puts a border on the pages. There are three kinds:

* **PDF border (Legacy)** – a PDF graphic is placed on every page, for example a frame. Choose the file with **Select...**. If **Full page** is ticked, the graphic is stretched to the full page size. Otherwise it is stretched only to the page size without the binding gutter.
* **Dynamic Border** – PTXprint draws a border around the Bible text on each page. Introductions, footnotes and other peripheral material are outside the border. The border can be plain, double or made of ornaments. It is controlled by the `textborder` style on the **Styles** tab (in the **Other** category). Change it there with the **Borders...** button in **Sidebar Settings**.
* **Page Border** – meant to place a border of the same size on every page, whatever the content. It is controlled by the `\pageborder` style. If you do not get the result you want, use **Dynamic Border** or **PDF border (Legacy)** instead.

A border takes space. You will probably need to make the margins larger on the **Layout** tab so the border does not touch the text or the edge of the paper.

### End of Book Decoration

This adds a small graphic after the last verse of each Scripture book. Choose the PDF file with **Select...**. PTXprint suggests its own `decoration.pdf` graphic.

### Verse Number Decorator

This puts a decoration around every verse number. There are two methods:

* **End of Ayah** – uses the "End of Ayah" character (Unicode U+06DD) from the font, with the verse number inside it. This is common in Arabic-script publications. The font must contain this character. Tick **Move Ayah** to move the decorated number to the end of each verse instead of the start. The `\vp` link opens the style used for the moved numbers.
* **Verse Border Graphic** – uses a small PDF graphic (for example a star) behind each verse number. Choose it with **Select...**. Use **Scale** to change its size and **Shift** to move it up (positive values) or down (negative values), in pt.

The `\v` link opens the verse number style. You may need a smaller font size or a different colour for the numbers so they fit inside the decoration.

### Book Title Borders

This draws a border around the book title (`\mt1` and `\mt2`). It is controlled by the special style `cat:titlebox|esb`. Click the link to open the style on the **Styles** tab and change its colours and border.

## Border Settings dialog

The **Border Settings** dialog sets how a border looks. It belongs to a style on the **Styles** tab. To open it, select the style (for example a sidebar style, `textborder`, `cat:headingsbox|esb` or `cat:titlebox|esb`), open **Sidebar Settings**, and click **Borders...**. Click **OK** to save the changes in that style, or **Cancel** to leave the style as it was.

**Borders** area:

* **Type of Border** – **None**, **Plain (single)** (one line), **Double** (two lines) or **Ornamental** (a pattern of ornaments). Most other settings are greyed out when **None** is chosen.
* **Left**, **Right**, **Top**, **Bottom**, **Inner**, **Outer** – which sides get a border. Use **Inner** and **Outer** instead of **Left** and **Right** if the border should follow the binding (inner = the side near the spine). Ticking **Inner** or **Outer** unticks **Left** and **Right**, and the other way round.
* **Border Width (pt)** – how wide the whole border is. For ornamental borders use at least 10 pt.
* **Line Thickness (pt)** – how thick the lines that make up a **Double** or **Ornamental** border are.
* **Line Color** – the colour of the lines.
* **Fill Color** – the colour that fills a **Double** or **Ornamental** border.
* **Select Ornamental Border** (only for **Ornamental**) – which ornament pattern to use. Click **Ornamental Border Style** to open the ornaments catalogue (a PDF) and see what the patterns look like.

**Padding** area. There are two kinds of padding, on two tabs:

* **Box** – the space between the edge of the box (its background colour) and the text inside it.
* **Border** – the space between the inside edge of the border and the box inside it.

Each tab has four values in a cross: top, bottom, left (or inner) and right (or outer), in pt. Tick **Uniform Box Padding** or **Uniform Border Padding** to use the top value for all four sides; the other three are then greyed out. Negative values are allowed. The picture in the dialog shows the effect.

## Common tasks

### Add thumb tabs to a Bible or New Testament

1. On the main window, select all the books in the multiple-book list.
2. On the **Tabs+Borders** tab, tick **Thumb Tabs**.
3. Set **Height** and **Length** (for example 8 mm and 15 mm).
4. Choose a dark **Tab Color**.
5. Click **Edit Style** and set a light text colour (for example white) for the tab text.
6. Print and look at the outer edge of the pages.

### Let short books share a tab position

1. Tick **Thumb Tabs**.
2. Click the **Grouped Tabs** button to load PTXprint's default groups. Or type your own groups in the **Grouped Tabs** box, for example `PHM TIT; 1JN 2JN 3JN JUD`.
3. Print. Each group uses one position, but each book keeps its own name.

### Make the text in the tabs run along the page edge

1. Tick **Rotate Tabs**.
2. In the drop-down list next to it, choose how the text should face, for example **Each Facing Outward**.
3. Check the preview on the tab, then print.

### Start the New Testament tabs at the top again

1. Tick **Restart Tabs at MAT**.
2. Print.

### Put a decorative border around the Bible text

1. Tick **Ornamental Decorations**.
2. Tick **Border** and choose **Dynamic Border**.
3. Go to the **Styles** tab and select the `textborder` style (in the **Other** category).
4. Open **Sidebar Settings** and click **Borders...**.
5. Choose the **Type of Border** (for example **Ornamental**), the ornament, the **Border Width** (at least 10 pt for ornaments) and the colours. Click **OK**.
6. On the **Layout** tab, make the margins larger if the border is too close to the text or the paper edge.
7. Print.

### Use a ready-made PDF frame on every page

1. Tick **Ornamental Decorations**, then **Border**.
2. Choose **PDF border (Legacy)**.
3. Click **Select...** and choose the PDF file.
4. Tick **Full page** if the frame should cover the whole page.
5. Make the margins larger on the **Layout** tab if needed, then print.

### Decorate the verse numbers

1. Tick **Ornamental Decorations**, then **Verse Number Decorator**.
2. Choose **Verse Border Graphic** and click **Select...** to choose a small PDF graphic. (For Arabic script, you can choose **End of Ayah** instead.)
3. Print. If the number does not fit, change **Scale** and **Shift**, or click the `\v` link to make the verse numbers smaller.

### Add a graphic at the end of each book

1. Tick **Ornamental Decorations**, then **End of Book Decoration**.
2. Click **Select...** and choose a PDF graphic.
3. Print.

### Put a border around book titles or section headings

1. Tick **Ornamental Decorations**.
2. Tick **Book Title Borders**, or tick **Section Headings** and choose **Dynamic Border**.
3. Click the style link (`cat:titlebox|esb` or `cat:headingsbox|esb`). The **Styles** tab opens with that style selected.
4. Change the background colour, and click **Borders...** in **Sidebar Settings** to change the border.
5. Print.

## Common problems

**I cannot see the thumb tab or ornament settings.**
These areas are collapsed until their checkbox is ticked. Tick **Thumb Tabs** or **Ornamental Decorations**. If the whole tab is missing, change the view level to **Default** or **Full**.

**The thumb tabs overlap each other, or there are big gaps between them.**
Change **Number of Tab Positions** (larger = closer together and may overlap, smaller = further apart), or change **Height** (or **Length** for rotated tabs). Group short books in **Grouped Tabs**, or tick **Restart Tabs at MAT**. Remember that PTXprint recalculates **Number of Tab Positions** when you change the tab size, page size or margins.

**My value for Number of Tab Positions keeps changing.**
PTXprint recalculates it whenever the tab size, page size or margins change. Set the size first, then adjust this number last.

**The thumb tab is blank.**
The book has no `\toc3` line, or it has an empty `\zthumbtab` line. If the table of contents does not use `\toc3`, the `\toc3` text is removed and cannot be used for the tabs. On the **Peripherals** tab, include `\toc3` in the table of contents, or add the tab text with `\zthumbtab` in the book (in Paratext).

**The \toc3 and \zthumbtab options are greyed out.**
The table of contents on the **Peripherals** tab is on but does not use `\toc3`. Tick `\toc3` there to make both options available again.

**When I print one book, its tab is not at the top.**
This is on purpose. The tab position is calculated from all the books in the multiple-book list, so each book's tab stays in the same place in every print.

**I cannot change the colour of the tab text with Tab Color.**
**Tab Color** sets only the colour of the block. Click **Edit Style** and change the text colour of the style there.

**Message: "Warning: Could not locate decorative PDF(s)".**
A decoration is ticked but its PDF file is missing or was moved. Click the **Select...** button for that decoration and choose the file again, or untick the decoration.

**The border touches or covers the text.**
Make the margins larger on the **Layout** tab. For a dynamic border, also increase the padding in the **Border Settings** dialog.

**The ornamental border looks broken or squashed.**
Make the **Border Width** at least 10 pt in the **Border Settings** dialog.

**The section heading graphic does not fit the heading.**
Change **Scale** and **Shift**. If headings are sometimes two lines long, use **Dynamic Border** instead of **PDF border (Legacy)**.

**The decorated verse numbers show empty boxes.**
With **End of Ayah**, the font does not have the End of Ayah character (U+06DD). Choose a font that has it, or use **Verse Border Graphic**.

**The verse number does not fit inside the verse graphic.**
Increase **Scale**, adjust **Shift**, or click the `\v` link and make the verse number font smaller.

**A Select... button or a Shift/Scale box is greyed out.**
These belong to **PDF border (Legacy)** or **Verse Border Graphic**. Choose that option first.

**Clicking the \textborder or \pageborder link does nothing.**
Go to the **Styles** tab yourself and select the `textborder` style (or the page border style) from the list.

## Settings reference: Tabs+Borders tab

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Border Settings (dialog)

#### OK

- **Where:** Border Settings (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog and saves the border settings in the selected style.

*(Internal ID: `btn_border_ok`)*

#### Cancel

- **Where:** Border Settings (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog without changing the style.

*(Internal ID: `btn_border_cancel`)*

### Border Settings (dialog) › Borders

#### Left

- **Where:** Border Settings (dialog) › Borders
- **Type:** Checkbox (ticked by default)
- **Description:** Borders dialog: Show LEFT border
- **View level:** Default and Full views

**Explanation:**

Draws the border on the left side. Ticking it unticks **Inner** and **Outer**. Use **Left** and **Right** when the border does not need to follow the binding.

*(Internal ID: `c_sbBorder_lhs`)*

#### Right

- **Where:** Border Settings (dialog) › Borders
- **Type:** Checkbox (ticked by default)
- **Description:** Borders dialog: Show RIGHT border
- **View level:** Default and Full views

**Explanation:**

Draws the border on the right side. Ticking it unticks **Inner** and **Outer**.

*(Internal ID: `c_sbBorder_rhs`)*

#### Top

- **Where:** Border Settings (dialog) › Borders
- **Type:** Checkbox (ticked by default)
- **Description:** Borders dialog: Show TOP border
- **View level:** Default and Full views

**Explanation:**

Draws the border along the top.

*(Internal ID: `c_sbBorder_top`)*

#### Bottom

- **Where:** Border Settings (dialog) › Borders
- **Type:** Checkbox (ticked by default)
- **Description:** Borders dialog: Show BOTTOM border
- **View level:** Default and Full views

**Explanation:**

Draws the border along the bottom.

*(Internal ID: `c_sbBorder_bot`)*

#### Outer

- **Where:** Border Settings (dialog) › Borders
- **Type:** Checkbox (not ticked by default)
- **Description:** Borders dialog: Show OUTER border
- **View level:** Default and Full views

**Explanation:**

Draws the border on the outer side (the side away from the spine). Ticking it unticks **Left** and **Right**.

*(Internal ID: `c_sbBorder_out`)*

#### Inner

- **Where:** Border Settings (dialog) › Borders
- **Type:** Checkbox (not ticked by default)
- **Description:** Borders dialog: Show INNER border
- **View level:** Default and Full views

**Explanation:**

Draws the border on the inner side (the side near the spine). This side changes between left and right pages. Ticking it unticks **Left** and **Right**.

*(Internal ID: `c_sbBorder_inn`)*

#### Border Width (pt)

- **Where:** Border Settings (dialog) › Borders
- **Type:** Number box
- **Description:** Borders dialog: Border width
- **View level:** Default and Full views
- **Values:** from 0.1 to 200, default 2

**Tooltip (the text shown when you hover the mouse over it):**

> Specify how wide the border should be. Note that for ornamental borders this value needs to be at least 10pt.

**Explanation:**

The total width of the border, in pt. For **Plain** this is the thickness of the line. For **Ornamental**, use at least 10 pt so the ornaments are drawn properly.

*(Internal ID: `s_sbBorderWidth`)*

#### Line Color

- **Where:** Border Settings (dialog) › Borders
- **Type:** Colour picker
- **Description:** Borders dialog: Border line color
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Sets the line color for this border.

**Explanation:**

The colour of the border lines.

*(Internal ID: `col_sbBorderColor`)*

#### Type of Border

- **Where:** Border Settings (dialog) › Borders
- **Type:** Drop-down list
- **Description:** Borders dialog: Border type
- **View level:** Default and Full views
- **Choices:** None; Plain (single); Double; Ornamental

**Tooltip (the text shown when you hover the mouse over it):**

> None, a plain (single) line, a double line, or an ornamental pattern.

**Explanation:**

Chooses the kind of border: **None**, **Plain (single)**, **Double** or **Ornamental**. With **None**, most other settings in the dialog are greyed out. **Line Thickness** and **Fill Color** are only used for **Double** and **Ornamental**; the ornament list only for **Ornamental**.

*(Internal ID: `fcb_sbBorderStyle`)*

#### Borders dialog: Ornamental border

- **Where:** Border Settings (dialog) › Borders
- **Type:** Drop-down list
- **View level:** Default and Full views
- **Choices:** Han1; Han2; Han3; Han4; Han5; Vectorian1; Vectorian2; Vectorian3; Vectorian4; v85; v85r; v85out; v86c; c86out; v88; v88r; v88c; v88out

**Tooltip (the text shown when you hover the mouse over it):**

> A selection of ornamental borders are available to choose from, or a custom-made border may be applied.

**Explanation:**

Chooses the ornament pattern. The **Han** patterns are traditional Chinese-style designs; the **Vectorian** and **v…** patterns are Victorian-style designs. Open the catalogue with the **Ornamental Border Style** link to see them. Only available when **Type of Border** is **Ornamental**.

*(Internal ID: `fcb_sbBorderOrnament`)*

#### Fill Color

- **Where:** Border Settings (dialog) › Borders
- **Type:** Colour picker
- **Description:** Borders dialog: Border fill color
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Sets the fill color for this border.

**Explanation:**

The colour that fills a **Double** or **Ornamental** border. It is greyed out for **Plain (single)**.

*(Internal ID: `col_sbBorderFillColor`)*

#### Ornamental Border Style

- **Where:** Border Settings (dialog) › Borders
- **Type:** Link
- **Description:** Show the Ornaments Catalog
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Click to open a PDF containing a catalog of the various Ornamental Borders (pgs 4-7).

**Explanation:**

Opens the ornaments catalogue (a PDF). Pages 4–7 show the ready-made ornamental borders you can choose in the list.

*(Internal ID: `lb_openOrnamentsCatalog`)*

#### Line Thickness (pt)

- **Where:** Border Settings (dialog) › Borders
- **Type:** Number box
- **Description:** Borders dialog: Border Line Thickness
- **View level:** Default and Full views
- **Values:** default 0.3

**Tooltip (the text shown when you hover the mouse over it):**

> Specify the thickness of the lines which make up the border.

**Explanation:**

The thickness of the lines that draw a **Double** or **Ornamental** border, in pt (the default is 0.3 pt). It is greyed out for **Plain (single)**.

*(Internal ID: `s_sbBorderLineWidth`)*

### Border Settings (dialog) › Padding › Box tab

#### All/Top (pt)

- **Where:** Border Settings (dialog) › Padding › Box tab
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Top padding (pts). When Uniform Box Padding is ticked, this value is used for all four sides.

#### Borders dialog: Box padding bottom

- **Where:** Border Settings (dialog) › Padding › Box tab
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -200 to 200, default 8
- **Greyed out when:** “Uniform Box Padding” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The space (pts) between the edge of background box (or figure, if any) and the edge of the text in the box.

**Explanation:**

The bottom padding of the box, in pt. Greyed out when **Uniform Box Padding** is ticked.

*(Internal ID: `s_sbBoxPadB`)*

#### Bottom (pt)

- **Where:** Border Settings (dialog) › Padding › Box tab
- **Type:** Number box
- **Description:** Borders dialog: Box padding right
- **View level:** Default and Full views
- **Values:** from -200 to 200, default 8
- **Greyed out when:** “Uniform Box Padding” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The space (pts) between the edge of background box (or figure, if any) and the edge of the text in the box.
>
> The vertical space (pts) between the top/bottom borders (if any) and the text contained within the box.

**Explanation:**

The right (or outer) padding of the box, in pt. Greyed out when **Uniform Box Padding** is ticked.

*(Internal ID: `s_sbBoxPadR`)*

#### Left/Inner (pt)

- **Where:** Border Settings (dialog) › Padding › Box tab
- **Type:** Number box
- **Description:** Borders dialog: Box padding top
- **View level:** Default and Full views
- **Values:** from -200 to 200, default 8

**Tooltip (the text shown when you hover the mouse over it):**

> The space (pts) between the edge of background box (or figure, if any) and the edge of the text in the box.
>
> The horizontal space (pts) between the left/right borders (if any) and the text contained within the box.

**Explanation:**

The top padding of the box: the space between the top edge of the box and the text, in pt. When **Uniform Box Padding** is ticked, this value is used for all four sides.

*(Internal ID: `s_sbBoxPadT`)*

#### Borders dialog: Box padding left

- **Where:** Border Settings (dialog) › Padding › Box tab
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -200 to 200, default 8
- **Greyed out when:** “Uniform Box Padding” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The space (pts) between the edge of background box (or figure, if any) and the edge of the text in the box.

**Explanation:**

The left (or inner) padding of the box, in pt. Greyed out when **Uniform Box Padding** is ticked.

*(Internal ID: `s_sbBoxPadL`)*

#### Right/Outer (pt)

- **Where:** Border Settings (dialog) › Padding › Box tab
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The horizontal space (pts) between the left/right borders (if any) and the text contained within the box.

#### Uniform Box Padding

- **Where:** Border Settings (dialog) › Padding › Box tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Use the same value for the Top, Bottom, Left, and Right padding.

**Explanation:**

Uses the top value for all four sides of the box padding, and greys out the other three boxes.

*(Internal ID: `c_boxPadSymmetrical`)*

### Border Settings (dialog) › Padding › Border tab

#### All/Top (pt)

- **Where:** Border Settings (dialog) › Padding › Border tab
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Top padding (pts). When Uniform Border Padding is ticked, this value is used for all four sides.

#### Borders dialog: Border padding bottom

- **Where:** Border Settings (dialog) › Padding › Border tab
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -200 to 200, default 8
- **Greyed out when:** “Uniform Border Padding” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The space between the inside edge of the border and the outside edge of the box inside it.

**Explanation:**

The bottom padding between the border and the box, in pt. Greyed out when **Uniform Border Padding** is ticked.

*(Internal ID: `s_sbBdrPadB`)*

#### Bottom (pt)

- **Where:** Border Settings (dialog) › Padding › Border tab
- **Type:** Number box
- **Description:** Borders dialog: Border padding right
- **View level:** Default and Full views
- **Values:** from -200 to 200, default 8
- **Greyed out when:** “Uniform Border Padding” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The space between the inside edge of the border and the outside edge of the box inside it.
>
> The vertical space (pts) between the top/bottom borders (if any) and the text contained within the box.

**Explanation:**

The right (or outer) padding between the border and the box, in pt. Greyed out when **Uniform Border Padding** is ticked.

*(Internal ID: `s_sbBdrPadR`)*

#### Left/Inner (pt)

- **Where:** Border Settings (dialog) › Padding › Border tab
- **Type:** Number box
- **Description:** Borders dialog: Border padding top
- **View level:** Default and Full views
- **Values:** from -200 to 200, default 8

**Tooltip (the text shown when you hover the mouse over it):**

> The space between the inside edge of the border and the outside edge of the box inside it.
>
> The horizontal space (pts) between the left/right borders (if any) and the text contained within the box.

**Explanation:**

The top padding between the border and the box inside it, in pt. When **Uniform Border Padding** is ticked, this value is used for all four sides. A negative value makes the box reach under the border.

*(Internal ID: `s_sbBdrPadT`)*

#### Borders dialog: Border padding left

- **Where:** Border Settings (dialog) › Padding › Border tab
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -200 to 200, default 8
- **Greyed out when:** “Uniform Border Padding” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The space between the inside edge of the border and the outside edge of the box inside it.

**Explanation:**

The left (or inner) padding between the border and the box, in pt. Greyed out when **Uniform Border Padding** is ticked.

*(Internal ID: `s_sbBdrPadL`)*

#### Right/Outer (pt)

- **Where:** Border Settings (dialog) › Padding › Border tab
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The horizontal space (pts) between the left/right borders (if any) and the text contained within the box.

#### Uniform Border Padding

- **Where:** Border Settings (dialog) › Padding › Border tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Use the same value for the Top, Bottom, Left, and Right padding.

**Explanation:**

Uses the top value for all four sides of the border padding, and greys out the other three boxes.

*(Internal ID: `c_bdrPadSymmetrical`)*

### Tabs+Borders tab › Thumb Tabs

#### Height

- **Where:** Tabs+Borders tab › Thumb Tabs
- **Type:** Number box
- **Description:** Thumb tabs: Height
- **View level:** Default and Full views
- **Values:** from 3 to 20, default 8
- **Only available when:** “Thumb Tabs” is selected
- **Hidden until:** “Thumb Tabs” is ticked
- **This tab/section appears when:** “Thumb Tabs”, “Ornamental Decorations” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The height of the Thumb Tab measured in millimeters (mm).

**Explanation:**

For normal tabs this is the size of the tab along the page edge. For rotated tabs it is how far the tab reaches in from the edge. Changing it makes PTXprint recalculate **Number of Tab Positions** (for normal tabs).

*(Internal ID: `s_thumbheight` · Config key: `thumbtabs/height`)*

#### Tab Color

- **Where:** Tabs+Borders tab › Thumb Tabs
- **Type:** Colour picker
- **Description:** Thumb tabs: Tab color
- **View level:** Default and Full views
- **Only available when:** “Thumb Tabs” is selected
- **Hidden until:** “Thumb Tabs” is ticked
- **This tab/section appears when:** “Thumb Tabs”, “Ornamental Decorations” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The background color of the tabs. Use a dark color here and set the light text color with the Edit Style link.
>
> Thumb Tabs usually use a dark color for the background with a light color (or white) for the foreground text.
>
> The background color is set here, but the foreground text color needs to be set by clicking the Edit Style link.

**Explanation:**

The colour of the tab block. Choose a dark colour so the edge of the closed book shows it well. The text colour is set in the style (use **Edit Style**).

*(Internal ID: `col_thumbback` · Config key: `thumbtabs/background`)*

#### Rotate Tabs

- **Where:** Tabs+Borders tab › Thumb Tabs
- **Type:** Checkbox (not ticked by default)
- **Description:** Thumb tabs: Rotate tabs
- **View level:** Default and Full views
- **Only available when:** “Thumb Tabs” is selected
- **Hidden until:** “Thumb Tabs” is ticked
- **This tab/section appears when:** “Thumb Tabs”, “Ornamental Decorations” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Rotates the tabs so that the text runs along the edge of the page. This works well for narrow margins, but may result in fewer tab positions per page.

**Explanation:**

Turns the tab text so it runs along the page edge. This allows longer names in narrow margins, but each tab then takes more space along the edge, so fewer positions fit. When ticked, the orientation list next to it becomes available.

*(Internal ID: `c_thumbrotate` · Config key: `thumbtabs/rotate`)*

#### Number of Tab Positions

- **Where:** Tabs+Borders tab › Thumb Tabs
- **Type:** Number box
- **Description:** Thumb tabs: Number of tab positions
- **View level:** Default and Full views
- **Only available when:** “Thumb Tabs” is selected
- **Hidden until:** “Thumb Tabs” is ticked
- **This tab/section appears when:** “Thumb Tabs”, “Ornamental Decorations” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> How many tabs can there be down a page. This is automatically calculated from the Height (or Length when rotated), Page size and Margins. If any of these change then this value will be updated. Increasing it, makes tabs overlap. Reducing it spreads them apart.

**Explanation:**

How many tab positions there are from the top to the bottom of the page. PTXprint calculates it from the page height, margins and tab size, and overwrites your value when one of these changes. After the last position, the next book starts again at the top.

*(Internal ID: `s_thumbtabs` · Config key: `thumbtabs/numtabs`)*

#### Length

- **Where:** Tabs+Borders tab › Thumb Tabs
- **Type:** Number box
- **Description:** Thumb tabs: Length
- **View level:** Default and Full views
- **Values:** from 3 to 40, default 15
- **Only available when:** “Thumb Tabs” is selected
- **Hidden until:** “Thumb Tabs” is ticked
- **This tab/section appears when:** “Thumb Tabs”, “Ornamental Decorations” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The length of the Thumb Tab measured in millimeters (mm).

**Explanation:**

For normal tabs this is how far the tab reaches in from the page edge; make it long enough for the longest book name. For rotated tabs it is the size along the page edge. Changing it makes PTXprint recalculate **Number of Tab Positions** (for rotated tabs).

*(Internal ID: `s_thumblength` · Config key: `thumbtabs/length`)*

#### Grouped Tabs

- **Where:** Tabs+Borders tab › Thumb Tabs
- **Type:** Text box
- **Description:** Thumb tabs: Tabs grouped by books
- **View level:** Default and Full views
- **Only available when:** “Thumb Tabs” is selected
- **Hidden until:** “Thumb Tabs” is ticked
- **This tab/section appears when:** “Thumb Tabs”, “Ornamental Decorations” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> List book IDs of short books to be grouped together at the same tab position. Use spaces between book IDs, and use ; to separate groups. There is no need to list all the book IDs here - only the special ones which need to share the same tab position.
>
> For example: PHM TIT; 1JN 2JN 3JN JUD
>
> When several shorter adjacent books occur, it is common to group them together to use the same tab position (but still have differently named tabs).

**Explanation:**

Lists books that share one tab position. Use spaces between book codes and `;` between groups, for example `PHM TIT; 1JN 2JN 3JN JUD`. Only list the books that should share; other books get their own position.

*(Internal ID: `t_thumbgroups` · Config key: `thumbtabs/groups`)*

#### Length

- **Where:** Tabs+Borders tab › Thumb Tabs
- **Type:** Drop-down list
- **Description:** Thumb tabs: Rotate options
- **View level:** Default and Full views
- **Choices:** Each Facing Outward; Each Facing Inward; Rotate Both Anticlockwise; Rotate Both Clockwise
- **Only available when:** “Rotate Tabs”, “Thumb Tabs” is selected
- **Hidden until:** “Thumb Tabs” is ticked
- **This tab/section appears when:** “Thumb Tabs”, “Ornamental Decorations” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> If you choose to Rotate the tabs, there are various options as to how these should be oriented. The preview (right) will show how these will appear on facing pages.

**Explanation:**

Chooses which way rotated text faces on left and right pages: both facing outward, both facing inward, or both turned the same way (anticlockwise or clockwise). The preview on the tab shows the result. It is only available when **Rotate Tabs** is ticked.

*(Internal ID: `fcb_rotateTabs` · Config key: `thumbtabs/rotatetype`)*

#### Restart Tabs at MAT

- **Where:** Tabs+Borders tab › Thumb Tabs
- **Type:** Checkbox (not ticked by default)
- **Description:** Thumb tabs: Restart tabs at New Testament
- **View level:** Default and Full views
- **Only available when:** “Thumb Tabs” is selected
- **Hidden until:** “Thumb Tabs” is ticked
- **This tab/section appears when:** “Thumb Tabs”, “Ornamental Decorations” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Normally books will follow sequentially and if the next tab would be off the bottom of the page, then it will be set to the top for a new cycle of tabs. Setting this starts a new cycle at the start of the New Testament (Matthew).

**Explanation:**

Starts the tab positions again at the top for Matthew. Use it in a whole Bible, so the New Testament has its own run of tabs.

*(Internal ID: `c_thumbrestart` · Config key: `thumbtabs/restart`)*

#### Grouped Tabs

- **Where:** Tabs+Borders tab › Thumb Tabs
- **Type:** Button
- **Description:** Thumb tabs: Reload default book groups
- **View level:** Default and Full views
- **Only available when:** “Thumb Tabs” is selected
- **Hidden until:** “Thumb Tabs” is ticked
- **This tab/section appears when:** “Thumb Tabs”, “Ornamental Decorations” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Clicking this button will replace the Grouped Tabs list with the default groups.

**Explanation:**

Replaces the **Grouped Tabs** text with PTXprint's default groups (for example `RUT 1SA`, the Minor Prophets in two groups, and the short letters). Any groups you typed are lost.

*(Internal ID: `btn_resetTabGroups`)*

#### \toc3

- **Where:** Tabs+Borders tab › Thumb Tabs
- **Type:** Radio button
- **Description:** Thumb tabs: Use \toc3 text
- **View level:** Default and Full views
- **Only available when:** “Thumb Tabs” is selected
- **Hidden until:** “Thumb Tabs” is ticked
- **This tab/section appears when:** “Thumb Tabs”, “Ornamental Decorations” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> By default, Thumb Tabs use the content and styling of the \toc3 marker.
>
> Note that this setting is interconnected with the Table of Contents settings on the Peripherals tab. If \toc3 is not included in the ToC, then this option will be disabled. So it is recommended to use \toc3 as your thumbtab text and include it in the Table of Contents.

**Explanation:**

Uses the short book name from `\toc3` as the tab text. This is the usual choice. If the table of contents on the **Peripherals** tab is on, keep `\toc3` included there, or this option is not available.

*(Internal ID: `r_thumbText_toc3` · Config key: `thumbtabs/thumbtextmkr=toc3`)*

#### \zthumbtab

- **Where:** Tabs+Borders tab › Thumb Tabs
- **Type:** Radio button
- **Description:** Thumb tabs: Use \zthumbtab text
- **View level:** Default and Full views
- **Only available when:** “Thumb Tabs” is selected
- **Hidden until:** “Thumb Tabs” is ticked
- **This tab/section appears when:** “Thumb Tabs”, “Ornamental Decorations” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> By default, Thumb Tabs use the content and styling of the \toc3 marker. If you prefer different content and/or styling for the tabs, then this  
> \zthumbtab option needs to be enabled, and the thumbtab names entered into your USFM text.
>
> Note that this setting is interconnected with the Table of Contents settings on the Peripherals tab. If \toc3 is not included in the ToC, then you are forced to use the \zthumbtab setting here. For that reason it is highly recommended to use \toc3 as your thumbtab text and include it in the Table of Contents.
>
> The USFM extension \zthumbtab can be used to set an alternative value for the thumbtab contents. If a book's header contains a \zthumbtab entry, then  
> \toc3 will not be used as the thumbtab contents. An empty \zthumbtab entry specifies that there should be no text in the thumbtab for that book.

**Explanation:**

Choose this if the tab text should differ from `\toc3`. The tab text is then taken from a `\zthumbtab` line in each book's header (added in Paratext). An empty `\zthumbtab` line gives a tab with no text. With this option, **Edit Style** opens the `\zthumbtab` style.

*(Internal ID: `r_thumbText_zthumbtab` · Config key: `thumbtabs/thumbtextmkr=zthumbtab`)*

#### Edit Style

- **Where:** Tabs+Borders tab › Thumb Tabs
- **Type:** Link
- **View level:** Default and Full views
- **Only available when:** “Thumb Tabs” is selected
- **Hidden until:** “Thumb Tabs” is ticked
- **This tab/section appears when:** “Thumb Tabs”, “Ornamental Decorations” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to jump to the appropriate (\toc3 or \zthumbtab) marker in the style editor to change the formatting of the thumb tabs.

**Explanation:**

Opens the style used for the tab text (`\toc3`, or `\zthumbtab` if that option is chosen) on the **Styles** tab. Change the text colour, font and size there. Note that changing the `\toc3` style may also change how `\toc3` text looks in other places, such as the table of contents.

*(Internal ID: `lb_style_toc3`)*

#### Only Show on Odd Pages

- **Where:** Tabs+Borders tab › Thumb Tabs
- **Type:** Checkbox (not ticked by default)
- **Description:** Thumb tabs: Only Show on Odd Pages
- **View level:** Default and Full views
- **Only available when:** “Thumb Tabs” is selected
- **Hidden until:** “Thumb Tabs” is ticked
- **This tab/section appears when:** “Thumb Tabs”, “Ornamental Decorations” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> When printing thumb tabs on thin paper, it is preferable to only print these tabs on a single side of the page (the odd pages).

**Explanation:**

Prints the tabs only on odd (right-hand) pages. This is better on thin paper, where a tab printed on both sides can show through.

*(Internal ID: `c_tabsOddOnly` · Config key: `thumbtabs/tabsoddonly`)*

### Tabs+Borders tab

#### Thumb Tabs

- **Where:** Tabs+Borders tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable thumb tabs
- **View level:** Default and Full views
- **This tab/section appears when:** “Thumb Tabs”, “Ornamental Decorations” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Thumb Tabs are sometimes used in longer publications to help the user find a scripture book more easily. By default these use the \toc3 element in a USFM file to provide the text for the tab. Note: If only a single book is currently selected, it will place the Thumb Tab relative to ALL the books listed in the multiple book list.

**Explanation:**

Turns thumb tabs on and shows their settings. Tabs are only given to Scripture books, and their positions are calculated from all the books in the multiple-book list, even when you print a single book. Thumb tabs are printed to the edge of the paper, so they need a printer that can print or trim to the edge.

*(Internal ID: `c_thumbtabs` · Config key: `thumbtabs/ifthumbtabs`)*

#### Ornamental Decorations

- **Where:** Tabs+Borders tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Ornamental Decorations: Enable decorative borders, rules and verses
- **View level:** Default and Full views
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Enable this option to make use of ornamental borders, rules & verses.
>
> Some cultures place a high value on such decorative features in scripture publications.

**Explanation:**

Turns on the ornament features and shows their settings. Then tick each kind of decoration you want. Most decorations need extra space, so check the margins and heading spacing after you print.

*(Internal ID: `c_useOrnaments` · Config key: `snippets/fancyborders`)*

### Tabs+Borders tab › Ornamental Decorations › Section Headings

#### Select...

- **Where:** Tabs+Borders tab › Ornamental Decorations › Section Headings
- **Type:** Button
- **Description:** Select decorative section headings
- **View level:** Default and Full views
- **Only available when:** “PDF border (Legacy)”, “Section Headings”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Explanation:**

Opens a file chooser for the section heading graphic (a PDF file). The name of the chosen file appears next to the button. It is only available with **PDF border (Legacy)**.

*(Internal ID: `btn_selectSectionHeaderPDF` · Config key: `fancy/sectionheaderpdf`)*

#### Shift

- **Where:** Tabs+Borders tab › Ornamental Decorations › Section Headings
- **Type:** Number box
- **Description:** Decorative section headings: Vertical shift
- **View level:** Default and Full views
- **Values:** from -50 to 50
- **Only available when:** “PDF border (Legacy)”, “Section Headings”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Vertical shift in pts of the section box image.  
>   - values shift the box upwards  
>   + values shift the box downwards

**Explanation:**

Moves the section heading graphic up or down, in pt. Negative values move it up, positive values move it down. Change it in small steps (for example 2 pt) and print to check.

*(Internal ID: `s_inclSectionShift` · Config key: `fancy/sectionheadershift`)*

#### Scale

- **Where:** Tabs+Borders tab › Ornamental Decorations › Section Headings
- **Type:** Number box
- **Description:** Decorative section headings: Scale
- **View level:** Default and Full views
- **Values:** default 1
- **Only available when:** “PDF border (Legacy)”, “Section Headings”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Scale section header image. 1.0 = its own size,  
> 0.5 = half size, 2.0 = double size.

**Explanation:**

Changes the size of the section heading graphic. 1 is the graphic's own size, 0.8 is 80%, 1.2 is 120%.

*(Internal ID: `s_inclSectionScale` · Config key: `fancy/sectionheaderscale`)*

#### PDF border (Legacy)

- **Where:** Tabs+Borders tab › Ornamental Decorations › Section Headings
- **Type:** Radio button
- **View level:** Default and Full views
- **Only available when:** “Section Headings”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Place a PDF graphic behind each section heading (\s, \s1, \s2). Use Select... to choose it, and Scale/Shift to fit it.

**Explanation:**

Places a fixed PDF graphic behind each section heading (`\s`, `\s1`, `\s2`). Choose the graphic with **Select...** and adjust it with **Scale** and **Shift**. It does not grow with the heading, so it suits headings that are always one line.

*(Internal ID: `r_sectHead_legacy` · Config key: `fancy/sectionborder=legacy`, `fancy/sectionbordertype=legacy`)*

#### Dynamic Border

- **Where:** Tabs+Borders tab › Ornamental Decorations › Section Headings
- **Type:** Radio button
- **View level:** Default and Full views
- **Only available when:** “Section Headings”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Draw a box around each section heading that grows with the heading. Its look is set by the cat:headingsbox|esb style.

**Explanation:**

Draws a box around each heading block that grows with the heading. Its look comes from the `cat:headingsbox|esb` style; PTXprint makes that style active for you when this option is chosen. Use the link to change it.

*(Internal ID: `r_sectHead_dynamic` · Config key: `fancy/sectionborder=dynamic`, `fancy/sectionbordertype=dynamic`)*

#### \cat:headingsbox|esb

- **Where:** Tabs+Borders tab › Ornamental Decorations › Section Headings
- **Type:** Link
- **View level:** Default and Full views
- **Only available when:** “Dynamic Border”, “Section Headings”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> If Section Headings sometimes extend to more than one line, then a static PDF section heading is unlikely to work. Instead, a dynamically generated decorative section heading needs to be set up to grow/shrink with the content of the heading. Use this link to show the special style, which needs to be enabled and defined.

**Explanation:**

Opens the `cat:headingsbox|esb` style on the **Styles** tab. There you can set the background colour and, with the **Borders...** button, the border of the box around headings. It is only available with **Dynamic Border**.

*(Internal ID: `lb_style_cat:headingsbox|esb`)*

### Tabs+Borders tab › Ornamental Decorations

#### Section Headings

- **Where:** Tabs+Borders tab › Ornamental Decorations
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable decorative section headings
- **View level:** Default and Full views
- **Only available when:** “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Section Headings may be adorned with a special graphic. Ensure that there is adequate space - both horizontal as well as vertical to make sure all headings fit.

**Explanation:**

Adds a decoration to section headings. Choose **PDF border (Legacy)** for a fixed graphic or **Dynamic Border** for a box that fits the heading. Make sure there is enough space around headings so they fit inside the decoration.

*(Internal ID: `c_inclSectionHeader` · Config key: `fancy/sectionheader`)*

#### Border

- **Where:** Tabs+Borders tab › Ornamental Decorations
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable decorative borders
- **View level:** Default and Full views
- **Only available when:** “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> There are different kinds of borders that can be applied to the publication.
>
> Note that if you use a border, it is likely that you will need to adjust the margins to make it fit.

**Explanation:**

Adds a border to the pages. Choose one of the three kinds below it. You will usually need larger margins on the **Layout** tab.

*(Internal ID: `c_inclPageBorder` · Config key: `fancy/pageborders`)*

#### End of Book Decoration

- **Where:** Tabs+Borders tab › Ornamental Decorations
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable end of book decoration
- **View level:** Default and Full views
- **Only available when:** “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The end of each book may be adorned with a special graphic.

**Explanation:**

Adds a decoration after the last verse of each Scripture book. Choose the graphic with **Select...**. Front matter, glossaries and other non-Scripture books do not get it.

*(Internal ID: `c_inclEndOfBook` · Config key: `fancy/endofbook`)*

#### Verse Number Decorator

- **Where:** Tabs+Borders tab › Ornamental Decorations
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable decorative verse numbers
- **View level:** Default and Full views
- **Only available when:** “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Verse numbers can be decorated using either of the options shown below.

**Explanation:**

Decorates every verse number. Choose **End of Ayah** (a character from the font) or **Verse Border Graphic** (a small PDF graphic).

*(Internal ID: `c_inclVerseDecorator` · Config key: `fancy/versedecorator`)*

#### Book Title Borders

- **Where:** Tabs+Borders tab › Ornamental Decorations
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable dynamic title borders
- **View level:** Default and Full views
- **Only available when:** “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Dynamic borders can be applied to book titles (\mt1 and \mt2). Styling can be adjusted using the link below.

**Explanation:**

Draws a border around the book title (`\mt1` and `\mt2`). PTXprint makes the `cat:titlebox|esb` style active for you. Use the link below to change its look.

*(Internal ID: `c_inclTitleBorders` · Config key: `fancy/booktitleborder`)*

### Tabs+Borders tab › Ornamental Decorations › Border

#### Select...

- **Where:** Tabs+Borders tab › Ornamental Decorations › Border
- **Type:** Button
- **Description:** Select decorative borders
- **View level:** Default and Full views
- **Only available when:** “PDF border (Legacy)”, “Border”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Explanation:**

Opens a file chooser for the page border graphic (a PDF file). It starts in PTXprint's border-art folder. It is only available with **PDF border (Legacy)**.

*(Internal ID: `btn_selectPageBorderPDF` · Config key: `fancy/pageborderpdf`)*

#### Full page

- **Where:** Tabs+Borders tab › Ornamental Decorations › Border
- **Type:** Checkbox (not ticked by default)
- **Description:** Decorative borders: Expand to fill page
- **View level:** Default and Full views
- **Only available when:** “PDF border (Legacy)”, “Border”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> If set, the border is expanded to the full page. Otherwise it is expanded only to the gutter margins.

**Explanation:**

Stretches the PDF border graphic to the whole page. If unticked, the graphic is stretched to the page size without the binding gutter. It is only available with **PDF border (Legacy)**.

*(Internal ID: `c_borderPageWide` · Config key: `fancy/pageborderfullpage`, `fancy/pagebordernfullpage_`)*

#### \textborder

- **Where:** Tabs+Borders tab › Ornamental Decorations › Border
- **Type:** Link
- **View level:** Default and Full views
- **Only available when:** “Dynamic Border”, “Border”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the properties of the Text Border (which is controlled by the \textborder style on the Styles tab).

**Explanation:**

Meant to take you to the `textborder` style that controls the **Dynamic Border**. If it does not open the style, go to the **Styles** tab and select `textborder` (in the **Other** category). It is only available with **Dynamic Border**.

*(Internal ID: `lb_style_textborder`)*

#### PDF border (Legacy)

- **Where:** Tabs+Borders tab › Ornamental Decorations › Border
- **Type:** Radio button
- **View level:** Default and Full views
- **Only available when:** “Border”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Use an existing PDF Border for the entire publication.

**Explanation:**

Places a PDF graphic (for example a decorative frame) on every page. Choose it with **Select...**. The graphic is stretched to the page (or to the page without the binding gutter, unless **Full page** is ticked).

*(Internal ID: `r_border_pdf` · Config key: `fancy/pageborder`)*

#### Dynamic Border

- **Where:** Tabs+Borders tab › Ornamental Decorations › Border
- **Type:** Radio button
- **View level:** Default and Full views
- **Only available when:** “Border”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Place a decorative border only around the Scripture text (excludes introductions, footnotes and other peripheral material).

**Explanation:**

Draws a border around the Bible text area of each page, leaving out introductions, footnotes and other material. Its look comes from the `textborder` style on the **Styles** tab (in the **Other** category); PTXprint makes that style active for you. Change it with the **Borders...** button in **Sidebar Settings**.

*(Internal ID: `r_border_text` · Config key: `fancy/pagebordertype=text`)*

#### Page Border

- **Where:** Tabs+Borders tab › Ornamental Decorations › Border
- **Type:** Radio button
- **View level:** Default and Full views
- **Only available when:** “Border”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Place a uniform-sized decorative border on every page regardless of content.

**Explanation:**

Meant to put a border of the same size on every page, whatever is on it, controlled by the `\pageborder` style. If you do not get the result you want, use **Dynamic Border** or **PDF border (Legacy)**.

*(Internal ID: `r_border_page` · Config key: `fancy/pagebordertype=page`)*

#### \pageborder

- **Where:** Tabs+Borders tab › Ornamental Decorations › Border
- **Type:** Link
- **View level:** Default and Full views
- **Only available when:** “Page Border”, “Border”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the properties of the Page Border (which is controlled by the \pageborder style on the Styles tab).

**Explanation:**

Refers to the `\pageborder` style that controls the **Page Border** option. It is only available with **Page Border**.

*(Internal ID: `lb_style_pageborder`)*

### Tabs+Borders tab › Ornamental Decorations › End of Book Decoration

#### Select...

- **Where:** Tabs+Borders tab › Ornamental Decorations › End of Book Decoration
- **Type:** Button
- **Description:** Select end of book decoration
- **View level:** Default and Full views
- **Only available when:** “End of Book Decoration”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Explanation:**

Opens a file chooser for the end-of-book graphic (a PDF file). The graphic is centred below the last line of each book.

*(Internal ID: `btn_selectEndOfBookPDF` · Config key: `fancy/endofbookpdf`)*

### Tabs+Borders tab › Ornamental Decorations › Verse Number Decorator

#### End of Ayah

- **Where:** Tabs+Borders tab › Ornamental Decorations › Verse Number Decorator
- **Type:** Radio button
- **Description:** Decorative verse numbers: Use end of Ayah
- **View level:** Default and Full views
- **Only available when:** “Verse Number Decorator”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Use the End of Ayah character in the font to decorate the verse number.

**Explanation:**

Puts each verse number inside the End of Ayah character (U+06DD) of the font. The font must contain this character, otherwise you see empty boxes. Use **Move Ayah** to place the number at the end of the verse.

*(Internal ID: `r_decorator_ayah` · Config key: `fancy/versedecoratortype=ayah`)*

#### Verse Border Graphic

- **Where:** Tabs+Borders tab › Ornamental Decorations › Verse Number Decorator
- **Type:** Radio button
- **Description:** Decorative verse numbers: Use verse border graphic
- **View level:** Default and Full views
- **Only available when:** “Verse Number Decorator”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Use a PDF graphic to decorate the verse number. You may need to also adjust the font properties to ensure the verse numbers fit within the graphic.

**Explanation:**

Places a small PDF graphic behind each verse number. Choose it with **Select...** and adjust it with **Scale** and **Shift**. You may need to change the verse number font size or colour so the number fits inside.

*(Internal ID: `r_decorator_file` · Config key: `fancy/versedecoratortype=file`)*

#### \vp

- **Where:** Tabs+Borders tab › Ornamental Decorations › Verse Number Decorator
- **Type:** Link
- **View level:** Default and Full views
- **Only available when:** “Move Ayah”, “Verse Number Decorator”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the \vp marker's properties on the Styles tab.

**Explanation:**

Opens the `\vp` style on the **Styles** tab. This style is used for the verse numbers when **Move Ayah** is ticked.

*(Internal ID: `lb_style_vp`)*

#### Select...

- **Where:** Tabs+Borders tab › Ornamental Decorations › Verse Number Decorator
- **Type:** Button
- **Description:** Select verse border graphic
- **View level:** Default and Full views
- **Only available when:** “Verse Border Graphic”, “Verse Number Decorator”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Explanation:**

Opens a file chooser for the verse number graphic (a PDF file). PTXprint suggests its own star graphic. It is only available with **Verse Border Graphic**.

*(Internal ID: `btn_selectVerseDecorator` · Config key: `fancy/versedecoratorpdf`)*

#### Shift

- **Where:** Tabs+Borders tab › Ornamental Decorations › Verse Number Decorator
- **Type:** Number box
- **Description:** Verse border graphic: Vertical shift
- **View level:** Default and Full views
- **Values:** from -20 to 20
- **Only available when:** “Verse Border Graphic”, “Verse Number Decorator”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Vertical shift in pts of the verse decorator image.  
>   + values shift the decorator upwards  
>   - values shift the decorator downwards

**Explanation:**

Moves the verse graphic up or down, in pt. Positive values move it up, negative values move it down. Use small steps, for example 0.5 pt.

*(Internal ID: `s_verseDecoratorShift` · Config key: `fancy/versedecoratorshift`)*

#### Scale

- **Where:** Tabs+Borders tab › Ornamental Decorations › Verse Number Decorator
- **Type:** Number box
- **Description:** Verse border graphic: Scale
- **View level:** Default and Full views
- **Values:** default 1
- **Only available when:** “Verse Border Graphic”, “Verse Number Decorator”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Scale verse decorator image. 1.0 = its own size,  
> 0.5 = half size, 2.0 = double size.

**Explanation:**

Changes the size of the verse graphic. 1 is its own size. Make it bigger if two- or three-digit verse numbers do not fit.

*(Internal ID: `s_verseDecoratorScale` · Config key: `fancy/versedecoratorscale`)*

#### Move Ayah

- **Where:** Tabs+Borders tab › Ornamental Decorations › Verse Number Decorator
- **Type:** Checkbox (not ticked by default)
- **Description:** Decorative verse numbers: Move Ayah to end of verse
- **View level:** Default and Full views
- **Only available when:** “End of Ayah”, “Verse Number Decorator”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This option moves the Ayah to the end of the verse.

**Explanation:**

Moves the decorated verse number from the start to the end of each verse, as is usual in Arabic-script layout. It is only available with **End of Ayah**. When ticked, the `\vp` link becomes available to style the moved numbers.

*(Internal ID: `c_decorator_endayah` · Config key: `fancy/endayah`)*

#### \v

- **Where:** Tabs+Borders tab › Ornamental Decorations › Verse Number Decorator
- **Type:** Link
- **View level:** Default and Full views
- **Only available when:** “Verse Number Decorator”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the \v marker's properties on the Styles tab.

**Explanation:**

Opens the `\v` (verse number) style on the **Styles** tab, where you can change the font size, colour and position of the verse numbers so they fit the decoration.

*(Internal ID: `lb_style_v`)*

### Tabs+Borders tab › Ornamental Decorations › Book Title Borders

#### \cat:titlebox|esb

- **Where:** Tabs+Borders tab › Ornamental Decorations › Book Title Borders
- **Type:** Link
- **View level:** Default and Full views
- **Only available when:** “Book Title Borders”, “Ornamental Decorations” is selected
- **Hidden until:** “Ornamental Decorations” is ticked
- **This tab/section appears when:** “Ornamental Decorations”, “Thumb Tabs” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Adjust the styling of the dynamic borders around book titles.

**Explanation:**

Opens the `cat:titlebox|esb` style on the **Styles** tab. Change the background colour there, and use **Borders...** in **Sidebar Settings** to change the border.

*(Internal ID: `lb_style_cat:titlebox|esb`)*
