## What this tab is for

This tab adds two kinds of decoration:

* **Thumb Tabs** – coloured blocks at the outer edge of the page, with a short book name in them. When the book is closed, the reader sees the blocks on the edge of the paper and can open the book near the right Bible book. They are useful in long publications such as a whole Bible or a New Testament.
* **Ornamental Decorations** – a border around the page or the text, a graphic behind section headings, a decoration at the end of each book, decorated verse numbers, and borders around book titles. Some cultures value such decoration highly in Scripture publications.

Each area is collapsed until you tick its checkbox; until then you only see a short description. The tab name shows **Tabs** and **Borders**, and each word turns blue when that feature is on. The tab is shown in the **Regular** and **Full** views.

This chapter also describes the **Border Settings** dialog, which sets the look of a border (lines, ornaments, colours and padding). You open it from the **Styles** tab with the **Borders...** button.

"pt" means point; 1 pt is about 0.35 mm. Thumb tab sizes are in mm.

## Thumb Tabs

**Where the tabs go.** Each Scripture book gets a tab position, counting down from the top of the page: the first book at position 1 (top), the next at position 2, and so on. When the positions run out, the next book starts again at the top. Front matter, glossaries and other non-Scripture books get no tab. Positions are worked out from all the books in the multiple-book list on the main window, even if you print only one book. So the tab for Mark is in the same place whether you print the whole NT or only Mark.

**Size.** For normal tabs, **Height** is the size along the page edge and **Length** is how far the tab reaches in from the edge. For rotated tabs it is the other way round.

**Number of Tab Positions** is how many tabs fit down the page. PTXprint recalculates it from the page height, the top and bottom margins and the tab size whenever these change. Bigger = tabs overlap; smaller = tabs spread apart.

**Grouped Tabs.** Many Bible books are short, so giving each its own position would need too many positions. Neighbouring short books can share one position, and each still has its own name in the tab. The **Grouped Tabs** button restores PTXprint's default groups.

**Restart Tabs at MAT** starts a new cycle at Matthew, so the New Testament tabs start again at the top.

**Rotate Tabs** turns the text to run along the page edge (good for narrow margins and longer names). The drop-down list next to it chooses which way the text faces on left and right pages. The preview on the tab shows facing pages.

**Only Show on Odd Pages** is for thin paper, so a tab on the back of the page does not show through.

**Tab text and colour.** By default the tab text is the short book name from each book's `\toc3` line. **Tab Color** sets only the block colour. The text colour, font and size come from the style: click **Edit Style** to change them on the **Styles** tab. Tabs usually use a dark block with white or light text.

The **\toc3** and **\zthumbtab** options choose where the tab text comes from. If the **Table of Contents** on the **Peripherals** tab is on but does not use `\toc3`, PTXprint selects **\zthumbtab** and greys out both options.

## Ornamental Decorations

Tick each kind of decoration you want. A file name next to a **Select...** button shows which graphic is used. Choosing a file ticks that decoration's checkbox for you. The **Select...** buttons open PTXprint's own border-art folder, but you can pick a PDF file from anywhere.

### Section Headings

* **PDF border (Legacy)** – a PDF graphic behind each `\s`, `\s1` and `\s2` heading. **Scale**: 1 = the graphic's own size. **Shift**: in pt, positive = up, negative = down. The graphic does not grow with the heading, so make sure every heading fits, also two-line headings. You may need more space before and after headings on the **Styles** tab.
* **Dynamic Border** – a box around each heading block that grows and shrinks with the heading. It is controlled by the special style `cat:headingsbox|esb`; the link opens it on the **Styles** tab, where you set its background colour and border (**Borders...** button).

### Border

* **PDF border (Legacy)** – a PDF graphic (for example a frame) on every page. It is stretched to the full page if **Full page** is ticked, otherwise to the page size without the binding gutter.
* **Dynamic Border** – a border around the Bible text on each page. Introductions, footnotes and other peripheral material are outside it. It can be plain, double or ornamental. It is controlled by the `textborder` style (**Styles** tab, **Other** category); change it with the **Borders...** button in **Sidebar Settings**.
* **Page Border** – meant to place a border of the same size on every page, whatever the content, controlled by the `\pageborder` style. If you do not get the result you want, use **Dynamic Border** or **PDF border (Legacy)**.

A border takes space, so you will probably need larger margins on the **Layout** tab so it does not touch the text or the paper edge.

### End of Book Decoration

A small graphic after the last verse of each Scripture book. PTXprint suggests its own `decoration.pdf`.

### Verse Number Decorator

* **End of Ayah** – the verse number inside the font's "End of Ayah" character (U+06DD), common in Arabic script. The font must contain this character. **Move Ayah** moves the decorated number to the end of the verse; the `\vp` link opens the style for the moved numbers.
* **Verse Border Graphic** – a small PDF graphic (for example a star) behind each verse number, adjusted with **Scale** and **Shift** (pt, positive = up).

The `\v` link opens the verse number style. You may need a smaller font size or another colour so the numbers fit inside the decoration.

### Book Title Borders

A border around the book title (`\mt1` and `\mt2`), controlled by the special style `cat:titlebox|esb`. The link opens it on the **Styles** tab to change its colours and border.

## Border Settings dialog

The dialog belongs to a style on the **Styles** tab. To open it, select the style (for example a sidebar style, `textborder`, `cat:headingsbox|esb` or `cat:titlebox|esb`), open **Sidebar Settings**, and click **Borders...**. **OK** saves the changes in that style; **Cancel** leaves the style as it was.

**Borders** area:

* **Type of Border** – **None**, **Plain (single)** (one line), **Double** (two lines) or **Ornamental** (a pattern of ornaments).
* **Left**, **Right**, **Top**, **Bottom**, **Inner**, **Outer** – which sides get a border. Use **Inner**/**Outer** if the border should follow the binding (inner = near the spine). Ticking **Inner** or **Outer** unticks **Left** and **Right**, and the other way round.
* **Border Width**, **Line Thickness**, **Line Color**, **Fill Color**, and **Select Ornamental Border** (the pattern, only for **Ornamental**) – see the control notes. **Ornamental Border Style** opens the ornaments catalogue (a PDF).

**Padding** area, on two tabs:

* **Box** – space between the edge of the box (its background colour) and the text inside it.
* **Border** – space between the inside edge of the border and the box inside it.

Each tab has four values in a cross: top, bottom, left (or inner) and right (or outer), in pt. **Uniform Box Padding** / **Uniform Border Padding** use the top value for all four sides and grey out the other three. Negative values are allowed. The picture in the dialog shows the effect.

## Common tasks

### Add thumb tabs to a Bible or New Testament

1. On the main window, select all the books in the multiple-book list.
2. On the **Tabs+Borders** tab, tick **Thumb Tabs**.
3. Set **Height** and **Length** (for example 8 mm and 15 mm).
4. Choose a dark **Tab Color**.
5. Click **Edit Style** and set a light text colour (for example white).
6. Print and look at the outer edge of the pages.

### Let short books share a tab position

1. Tick **Thumb Tabs**.
2. Click the **Grouped Tabs** button for the default groups, or type your own in the **Grouped Tabs** box, for example `PHM TIT; 1JN 2JN 3JN JUD`.
3. Print. Each group uses one position, but each book keeps its own name.

### Make the text in the tabs run along the page edge

1. Tick **Rotate Tabs**.
2. In the drop-down list next to it, choose how the text faces, for example **Each Facing Outward**.
3. Check the preview on the tab, then print.

### Start the New Testament tabs at the top again

Tick **Restart Tabs at MAT** and print.

### Put a decorative border around the Bible text

1. Tick **Ornamental Decorations**, then **Border**, and choose **Dynamic Border**.
2. On the **Styles** tab, select the `textborder` style (in the **Other** category).
3. Open **Sidebar Settings** and click **Borders...**.
4. Choose the **Type of Border** (for example **Ornamental**), the ornament, the **Border Width** (at least 10 pt for ornaments) and the colours. Click **OK**.
5. On the **Layout** tab, make the margins larger if the border is too close to the text or the paper edge.
6. Print.

### Use a ready-made PDF frame on every page

1. Tick **Ornamental Decorations**, then **Border**.
2. Choose **PDF border (Legacy)**, click **Select...** and choose the PDF file.
3. Tick **Full page** if the frame should cover the whole page.
4. Make the margins larger on the **Layout** tab if needed, then print.

### Decorate the verse numbers

1. Tick **Ornamental Decorations**, then **Verse Number Decorator**.
2. Choose **Verse Border Graphic** and click **Select...** to choose a small PDF graphic. (For Arabic script, you can choose **End of Ayah** instead.)
3. Print. If the number does not fit, change **Scale** and **Shift**, or click the `\v` link to make the verse numbers smaller.

### Add a graphic at the end of each book

1. Tick **Ornamental Decorations**, then **End of Book Decoration**.
2. Click **Select...**, choose a PDF graphic, and print.

### Put a border around book titles or section headings

1. Tick **Ornamental Decorations**.
2. Tick **Book Title Borders**, or tick **Section Headings** and choose **Dynamic Border**.
3. Click the style link (`cat:titlebox|esb` or `cat:headingsbox|esb`). The **Styles** tab opens with that style selected.
4. Change the background colour, and click **Borders...** in **Sidebar Settings** to change the border.
5. Print.

## Common problems

**I cannot see the thumb tab or ornament settings.**
Tick **Thumb Tabs** or **Ornamental Decorations**. If the whole tab is missing, change the view level to **Regular** or **Full**.

**The thumb tabs overlap each other, or there are big gaps between them.**
Change **Number of Tab Positions** (larger = closer and may overlap, smaller = further apart), or change **Height** (or **Length** for rotated tabs). Group short books in **Grouped Tabs**, or tick **Restart Tabs at MAT**.

**My value for Number of Tab Positions keeps changing.**
PTXprint recalculates it whenever the tab size, page size or margins change. Set those first, then adjust this number last.

**The thumb tab is blank.**
The book has no `\toc3` line, or it has an empty `\zthumbtab` line. If the table of contents does not use `\toc3`, the `\toc3` text is removed and cannot be used for the tabs. On the **Peripherals** tab, include `\toc3` in the table of contents, or add the tab text with `\zthumbtab` in the book (in Paratext).

**The \toc3 and \zthumbtab options are greyed out.**
The table of contents on the **Peripherals** tab is on but does not use `\toc3`. Tick `\toc3` there.

**When I print one book, its tab is not at the top.**
This is on purpose: positions come from all the books in the multiple-book list, so each tab stays in the same place in every print.

**I cannot change the colour of the tab text with Tab Color.**
**Tab Color** sets only the block. Click **Edit Style** and change the text colour there.

**Message: "Warning: Could not locate decorative PDF(s)".**
A decoration is ticked but its PDF file is missing or was moved. Choose the file again with that decoration's **Select...** button, or untick the decoration.

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
Choose **PDF border (Legacy)** or **Verse Border Graphic** first.

**Clicking the \pageborder link does nothing.**
This link does not open the style. Go to the **Styles** tab and select the page border style yourself. (The **\textborder** link does open the `textborder` style.)

## Control notes

### @c_thumbtabs
Only Scripture books get tabs. Thumb tabs are printed to the edge of the paper, so they need a printer that can print or trim to the edge.

### @s_thumbheight
Normal tabs: size along the page edge. Rotated tabs: how far the tab reaches in. Changing it recalculates **Number of Tab Positions** (for normal tabs).

### @s_thumblength
Normal tabs: how far the tab reaches in; make it long enough for the longest book name. Rotated tabs: size along the page edge. Changing it recalculates **Number of Tab Positions** (for rotated tabs).

### @s_thumbtabs
PTXprint overwrites your value when the page height, margins or tab size change. After the last position, the next book starts again at the top.

### @col_thumbback
A dark colour shows well on the edge of the closed book.

### @c_thumbrotate
Allows longer names in narrow margins. When ticked, the orientation list next to it becomes available.

### @fcb_rotateTabs
Outward and inward face opposite ways on left and right pages; the other two turn both pages the same way.

### @t_thumbgroups
Books not listed get their own position.

### @btn_resetTabGroups
The default groups include `RUT 1SA`, the Minor Prophets in two groups, and the short letters. Any groups you typed are lost.

### @c_thumbrestart
Use it in a whole Bible, so the New Testament has its own run of tabs.

### @c_tabsOddOnly
Better on thin paper, where a tab printed on both sides can show through.

### @r_thumbText_toc3
The usual choice.

### @r_thumbText_zthumbtab
Use it if the tab text should differ from `\toc3`. Add the `\zthumbtab` line to each book's header in Paratext. With this option, **Edit Style** opens the `\zthumbtab` style.

### @lb_style_toc3
Change the text colour, font and size there. Changing the `\toc3` style may also change how `\toc3` text looks elsewhere, such as in the table of contents.

### @c_useOrnaments
Most decorations need extra space, so check the margins and heading spacing after you print.

### @c_inclSectionHeader
Choose **PDF border (Legacy)** for a fixed graphic or **Dynamic Border** for a box that fits the heading.

### @r_sectHead_legacy
It does not grow with the heading, so it suits headings that are always one line.

### @r_sectHead_dynamic
PTXprint makes the `cat:headingsbox|esb` style active for you. Use the link to change it.

### @btn_selectSectionHeaderPDF
Chooses the section heading PDF graphic. The file name appears next to the button.

### @s_inclSectionShift
Same direction as **Shift** for the verse graphic. Change it in small steps (for example 2 pt) and print to check.

In older versions of PTXprint this worked the other way round. When you open a configuration saved by an older version, PTXprint changes the sign for you, so the graphic stays in place. A configuration saved by this version and opened in an older PTXprint moves the graphic the other way.

### @s_inclSectionScale
0.8 = 80%, 1.2 = 120%.

### @lb_style_cat:headingsbox|esb
On the **Styles** tab set the background colour and, with **Borders...**, the border of the box around headings.

### @c_inclPageBorder
Choose one of the three kinds below it.

### @r_border_pdf
Choose the graphic with **Select...**. It is stretched to the page without the binding gutter, or to the whole page if **Full page** is ticked.

### @r_border_text
Its look comes from the `textborder` style (**Styles** tab, **Other** category); PTXprint makes that style active for you. Change it with **Borders...** in **Sidebar Settings**.

### @r_border_page
If you do not get the result you want, use **Dynamic Border** or **PDF border (Legacy)**.

### @btn_selectPageBorderPDF
Chooses the page border PDF. It starts in PTXprint's border-art folder.

### @c_borderPageWide
If unticked, the graphic is stretched to the page size without the binding gutter.

### @lb_style_textborder
Change the border there with **Borders...** in **Sidebar Settings**.

### @lb_style_pageborder
Refers to the `\pageborder` style. (Clicking it does not open the style; see **Common problems**.)

### @c_inclEndOfBook
Front matter, glossaries and other non-Scripture books do not get it.

### @btn_selectEndOfBookPDF
Chooses the end-of-book PDF. It is centred below the last line of each book.

### @c_inclVerseDecorator
**End of Ayah** uses a character from the font; **Verse Border Graphic** uses a small PDF graphic.

### @r_decorator_ayah
The character is U+06DD. If the font lacks it you see empty boxes. **Move Ayah** puts the number at the end of the verse.

### @c_decorator_endayah
As is usual in Arabic-script layout. When ticked, the `\vp` link becomes available to style the moved numbers.

### @lb_style_vp
`\vp` is used for the verse numbers when **Move Ayah** is ticked.

### @r_decorator_file
Choose it with **Select...**; adjust with **Scale** and **Shift**.

### @btn_selectVerseDecorator
Chooses the verse number PDF. PTXprint suggests its own star graphic.

### @s_verseDecoratorShift
Use small steps, for example 0.5 pt.

### @s_verseDecoratorScale
Make it bigger if two- or three-digit verse numbers do not fit.

### @lb_style_v
Change the font size, colour and position of the verse numbers there so they fit the decoration.

### @c_inclTitleBorders
PTXprint makes the `cat:titlebox|esb` style active for you. Use the link below to change its look.

### @lb_style_cat:titlebox|esb
Change the background colour there, and use **Borders...** in **Sidebar Settings** for the border.

### @fcb_sbBorderStyle
With **None**, most other settings in the dialog are greyed out. **Line Thickness** and **Fill Color** are only used for **Double** and **Ornamental**; the ornament list only for **Ornamental**.

### @c_sbBorder_lhs
Ticking it unticks **Inner** and **Outer**. Use **Left** and **Right** when the border does not need to follow the binding.

### @c_sbBorder_rhs
Ticking it unticks **Inner** and **Outer**.

### @c_sbBorder_top
Draws the border along the top.

### @c_sbBorder_bot
Draws the border along the bottom.

### @c_sbBorder_inn
Near the spine, so it changes between left and right pages. Ticking it unticks **Left** and **Right**.

### @c_sbBorder_out
Away from the spine. Ticking it unticks **Left** and **Right**.

### @s_sbBorderWidth
For **Plain** this is the thickness of the line.

### @s_sbBorderLineWidth
For **Double** and **Ornamental** borders (default 0.3 pt). Greyed out for **Plain (single)**.

### @col_sbBorderColor
The colour of the border lines.

### @col_sbBorderFillColor
Fills a **Double** or **Ornamental** border. Greyed out for **Plain (single)**.

### @fcb_sbBorderOrnament
**Han** patterns are traditional Chinese-style designs; **Vectorian** and **v…** patterns are Victorian-style. See them in the catalogue (**Ornamental Border Style** link). Only available when **Type of Border** is **Ornamental**.

### @lb_openOrnamentsCatalog
Pages 4–7 show the ornamental borders in the list.

### @s_sbBoxPadT
Space between the top edge of the box and the text. With **Uniform Box Padding** it is used for all four sides.

### @s_sbBoxPadB
Bottom padding of the box.

### @s_sbBoxPadL
Left (or inner) padding of the box.

### @s_sbBoxPadR
Right (or outer) padding of the box.

### @c_boxPadSymmetrical
Greys out the bottom, left and right boxes.

### @s_sbBdrPadT
Top padding between the border and the box. With **Uniform Border Padding** it is used for all four sides. A negative value makes the box reach under the border.

### @s_sbBdrPadB
Bottom padding between the border and the box.

### @s_sbBdrPadL
Left (or inner) padding between the border and the box.

### @s_sbBdrPadR
Right (or outer) padding between the border and the box.

### @c_bdrPadSymmetrical
Greys out the bottom, left and right boxes.

### @btn_border_ok
Saves the border settings in the selected style and closes the dialog.

### @btn_border_cancel
Closes the dialog without changing the style.
