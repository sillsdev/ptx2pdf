# 14. Tabs+Borders tab

## 14.1 What this tab is for

This tab adds two kinds of decoration:

* **Thumb Tabs** – coloured blocks at the outer edge of the page, with a short book name in them. When the book is closed, the reader sees the blocks on the edge of the paper and can open the book near the right Bible book. They are useful in long publications such as a whole Bible or a New Testament.
* **Ornamental Decorations** – a border around the page or the text, a graphic behind section headings, a decoration at the end of each book, decorated verse numbers, and borders around book titles. Some cultures value such decoration highly in Scripture publications.

Each area is collapsed until you tick its checkbox; until then you only see a short description. The tab name shows **Tabs** and **Borders**, and each word turns blue when that feature is on. The tab is shown in the **Regular** and **Full** views.

This chapter also describes the **Border Settings** dialog, which sets the look of a border (lines, ornaments, colours and padding). You open it from the **Styles** tab with the **Borders...** button.

"pt" means point; 1 pt is about 0.35 mm. Thumb tab sizes are in mm.

## 14.2 Thumb Tabs

**Where the tabs go.** Each Scripture book gets a tab position, counting down from the top of the page: the first book at position 1 (top), the next at position 2, and so on. When the positions run out, the next book starts again at the top. Front matter, glossaries and other non-Scripture books get no tab. Positions are worked out from all the books in the multiple-book list on the main window, even if you print only one book. So the tab for Mark is in the same place whether you print the whole NT or only Mark.

**Size.** For normal tabs, **Height** is the size along the page edge and **Length** is how far the tab reaches in from the edge. For rotated tabs it is the other way round.

**Number of Tab Positions** is how many tabs fit down the page. PTXprint recalculates it from the page height, the top and bottom margins and the tab size whenever these change. Bigger = tabs overlap; smaller = tabs spread apart.

**Grouped Tabs.** Many Bible books are short, so giving each its own position would need too many positions. Neighbouring short books can share one position, and each still has its own name in the tab. The **Grouped Tabs** button restores PTXprint's default groups.

**Restart Tabs at MAT** starts a new cycle at Matthew, so the New Testament tabs start again at the top.

**Rotate Tabs** turns the text to run along the page edge (good for narrow margins and longer names). The drop-down list next to it chooses which way the text faces on left and right pages. The preview on the tab shows facing pages.

**Only Show on Odd Pages** is for thin paper, so a tab on the back of the page does not show through.

**Tab text and colour.** By default the tab text is the short book name from each book's `\toc3` line. **Tab Color** sets only the block colour. The text colour, font and size come from the style: click **Edit Style** to change them on the **Styles** tab. Tabs usually use a dark block with white or light text.

The **\toc3** and **\zthumbtab** options choose where the tab text comes from. If the **Table of Contents** on the **Peripherals** tab is on but does not use `\toc3`, PTXprint selects **\zthumbtab** and greys out both options.

## 14.3 Ornamental Decorations

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

## 14.4 Border Settings dialog

The dialog belongs to a style on the **Styles** tab. To open it, select the style (for example a sidebar style, `textborder`, `cat:headingsbox|esb` or `cat:titlebox|esb`), open **Sidebar Settings**, and click **Borders...**. **OK** saves the changes in that style; **Cancel** leaves the style as it was.

**Borders** area:

* **Type of Border** – **None**, **Plain (single)** (one line), **Double** (two lines) or **Ornamental** (a pattern of ornaments).
* **Left**, **Right**, **Top**, **Bottom**, **Inner**, **Outer** – which sides get a border. Use **Inner**/**Outer** if the border should follow the binding (inner = near the spine). Ticking **Inner** or **Outer** unticks **Left** and **Right**, and the other way round.
* **Border Width**, **Line Thickness**, **Line Color**, **Fill Color**, and **Select Ornamental Border** (the pattern, only for **Ornamental**) – see the control notes. **Ornamental Border Style** opens the ornaments catalogue (a PDF).

**Padding** area, on two tabs:

* **Box** – space between the edge of the box (its background colour) and the text inside it.
* **Border** – space between the inside edge of the border and the box inside it.

Each tab has four values in a cross: top, bottom, left (or inner) and right (or outer), in pt. **Uniform Box Padding** / **Uniform Border Padding** use the top value for all four sides and grey out the other three. Negative values are allowed. The picture in the dialog shows the effect.

## 14.5 Common tasks

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

## 14.6 Common problems

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

## 14.7 Settings reference

### Border Settings (dialog)

#### OK

Button · Regular+ · `btn_border_ok`

Saves the border settings in the selected style and closes the dialog.

#### Cancel

Button · Regular+ · `btn_border_cancel`

Closes the dialog without changing the style.

#### Borders

##### Left – Borders dialog: Show LEFT border

Checkbox, on · Regular+ · `c_sbBorder_lhs`

Ticking it unticks **Inner** and **Outer**. Use **Left** and **Right** when the border does not need to follow the binding.

##### Right

Checkbox, on · Regular+ · `c_sbBorder_rhs`  
Also: Borders dialog: Show RIGHT border

Ticking it unticks **Inner** and **Outer**.

##### Top

Checkbox, on · Regular+ · `c_sbBorder_top`  
Also: Borders dialog: Show TOP border

Draws the border along the top.

##### Bottom

Checkbox, on · Regular+ · `c_sbBorder_bot`  
Also: Borders dialog: Show BOTTOM border

Draws the border along the bottom.

##### Outer

Checkbox, off · Regular+ · `c_sbBorder_out`  
Also: Borders dialog: Show OUTER border

Away from the spine. Ticking it unticks **Left** and **Right**.

##### Inner – Borders dialog: Show INNER border

Checkbox, off · Regular+ · `c_sbBorder_inn`

Near the spine, so it changes between left and right pages. Ticking it unticks **Left** and **Right**.

##### Border Width (pt) – Borders dialog: Border width

Number · Regular+ · `s_sbBorderWidth`  
Values: 0.1–200 (default 2)

> Specify how wide the border should be. Note that for ornamental borders this value needs to be at least 10pt.

For **Plain** this is the thickness of the line.

##### Line Color – Borders dialog: Border line color

Colour · Regular+ · `col_sbBorderColor`

> Sets the line color for this border.

The colour of the border lines.

##### Type of Border – Borders dialog: Border type

Drop-down · Regular+ · `fcb_sbBorderStyle`  
Choices: None | Plain (single) | Double | Ornamental

> None, a plain (single) line, a double line, or an ornamental pattern.

With **None**, most other settings in the dialog are greyed out. **Line Thickness** and **Fill Color** are only used for **Double** and **Ornamental**; the ornament list only for **Ornamental**.

##### Borders dialog: Ornamental border

Drop-down · Regular+ · `fcb_sbBorderOrnament`  
Choices: Han1 | Han2 | Han3 | Han4 | Han5 | Vectorian1 | Vectorian2 | Vectorian3 | Vectorian4 | v85 | v85r | v85out | v86c | v86out | v88 | v88r | v88c | v88out

> A selection of ornamental borders are available to choose from, or a custom-made border may be applied.

**Han** patterns are traditional Chinese-style designs; **Vectorian** and **v…** patterns are Victorian-style. See them in the catalogue (**Ornamental Border Style** link). Only available when **Type of Border** is **Ornamental**.

##### Fill Color – Borders dialog: Border fill color

Colour · Regular+ · `col_sbBorderFillColor`

> Sets the fill color for this border.

Fills a **Double** or **Ornamental** border. Greyed out for **Plain (single)**.

##### Ornamental Border Style

Link · Regular+ · `lb_openOrnamentsCatalog`  
Also: Show the Ornaments Catalog

> Click to open a PDF containing a catalog of the various Ornamental Borders (pgs 4-7).

Pages 4–7 show the ornamental borders in the list.

##### Line Thickness (pt) – Borders dialog: Border Line Thickness

Number · Regular+ · `s_sbBorderLineWidth`

> Specify the thickness of the lines which make up the border.

For **Double** and **Ornamental** borders (default 0.3 pt). Greyed out for **Plain (single)**.

#### Padding

##### Box

###### All/Top (pt)

Label · Regular+

> Top padding (pts). When Uniform Box Padding is ticked, this value is used for all four sides.

###### Borders dialog: Box padding bottom

Number · Regular+ · `s_sbBoxPadB`  
Values: -200–200 (default 8) · Greyed out by: “Uniform Box Padding”

> The space (pts) between the edge of background box (or figure, if any) and the edge of the text in the box.

Bottom padding of the box.

###### Bottom (pt) – Borders dialog: Box padding right

Number · Regular+ · `s_sbBoxPadR`  
Values: -200–200 (default 8) · Greyed out by: “Uniform Box Padding”

> The space (pts) between the edge of background box (or figure, if any) and the edge of the text in the box.
>
> The vertical space (pts) between the top/bottom borders (if any) and the text contained within the box.

Right (or outer) padding of the box.

###### Left/Inner (pt) – Borders dialog: Box padding top

Number · Regular+ · `s_sbBoxPadT`  
Values: -200–200 (default 8)

> The space (pts) between the edge of background box (or figure, if any) and the edge of the text in the box.
>
> The horizontal space (pts) between the left/right borders (if any) and the text contained within the box.

Space between the top edge of the box and the text. With **Uniform Box Padding** it is used for all four sides.

###### Borders dialog: Box padding left

Number · Regular+ · `s_sbBoxPadL`  
Values: -200–200 (default 8) · Greyed out by: “Uniform Box Padding”

> The space (pts) between the edge of background box (or figure, if any) and the edge of the text in the box.

Left (or inner) padding of the box.

###### Right/Outer (pt)

Label · Regular+

> The horizontal space (pts) between the left/right borders (if any) and the text contained within the box.

###### Uniform Box Padding

Checkbox, off · Regular+ · `c_boxPadSymmetrical`

> Use the same value for the Top, Bottom, Left, and Right padding.

Greys out the bottom, left and right boxes.

##### Border

###### All/Top (pt)

Label · Regular+

> Top padding (pts). When Uniform Border Padding is ticked, this value is used for all four sides.

###### Borders dialog: Border padding bottom

Number · Regular+ · `s_sbBdrPadB`  
Values: -200–200 (default 8) · Greyed out by: “Uniform Border Padding”

> The space between the inside edge of the border and the outside edge of the box inside it.

Bottom padding between the border and the box.

###### Bottom (pt) – Borders dialog: Border padding right

Number · Regular+ · `s_sbBdrPadR`  
Values: -200–200 (default 8) · Greyed out by: “Uniform Border Padding”

> The space between the inside edge of the border and the outside edge of the box inside it.
>
> The vertical space (pts) between the top/bottom borders (if any) and the text contained within the box.

Right (or outer) padding between the border and the box.

###### Left/Inner (pt) – Borders dialog: Border padding top

Number · Regular+ · `s_sbBdrPadT`  
Values: -200–200 (default 8)

> The space between the inside edge of the border and the outside edge of the box inside it.
>
> The horizontal space (pts) between the left/right borders (if any) and the text contained within the box.

Top padding between the border and the box. With **Uniform Border Padding** it is used for all four sides. A negative value makes the box reach under the border.

###### Borders dialog: Border padding left

Number · Regular+ · `s_sbBdrPadL`  
Values: -200–200 (default 8) · Greyed out by: “Uniform Border Padding”

> The space between the inside edge of the border and the outside edge of the box inside it.

Left (or inner) padding between the border and the box.

###### Right/Outer (pt)

Label · Regular+

> The horizontal space (pts) between the left/right borders (if any) and the text contained within the box.

###### Uniform Border Padding

Checkbox, off · Regular+ · `c_bdrPadSymmetrical`

> Use the same value for the Top, Bottom, Left, and Right padding.

Greys out the bottom, left and right boxes.

### Tabs+Borders

#### Thumb Tabs

Checkbox, off · Regular+ · `c_thumbtabs` · cfg `thumbtabs/ifthumbtabs`  
Also: Enable thumb tabs · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> Thumb Tabs are sometimes used in longer publications to help the user find a scripture book more easily. By default these use the \toc3 element in a USFM file to provide the text for the tab. Note: If only a single book is currently selected, it will place the Thumb Tab relative to ALL the books listed in the multiple book list.

Only Scripture books get tabs. Thumb tabs are printed to the edge of the paper, so they need a printer that can print or trim to the edge.

#### Ornamental Decorations

Checkbox, off · Regular+ · `c_useOrnaments` · cfg `snippets/fancyborders`  
Also: Ornamental Decorations: Enable decorative borders, rules and verses · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Enable this option to make use of ornamental borders, rules & verses.
>
> Some cultures place a high value on such decorative features in scripture publications.

Most decorations need extra space, so check the margins and heading spacing after you print.

#### Thumb Tabs

##### Height – Thumb tabs: Height

Number · Regular+ · `s_thumbheight` · cfg `thumbtabs/height`  
Values: 3–20 (default 8) · Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> The height of the Thumb Tab measured in millimeters (mm).

Normal tabs: size along the page edge. Rotated tabs: how far the tab reaches in. Changing it recalculates **Number of Tab Positions** (for normal tabs).

##### Tab Color – Thumb tabs: Tab color

Colour · Regular+ · `col_thumbback` · cfg `thumbtabs/background`  
Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> The background color of the tabs. Use a dark color here and set the light text color with the Edit Style link.
>
> Thumb Tabs usually use a dark color for the background with a light color (or white) for the foreground text.
>
> The background color is set here, but the foreground text color needs to be set by clicking the Edit Style link.

A dark colour shows well on the edge of the closed book.

##### Rotate Tabs

Checkbox, off · Regular+ · `c_thumbrotate` · cfg `thumbtabs/rotate`  
Also: Thumb tabs: Rotate tabs · Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> Rotates the tabs so that the text runs along the edge of the page. This works well for narrow margins, but may result in fewer tab positions per page.

Allows longer names in narrow margins. When ticked, the orientation list next to it becomes available.

##### Number of Tab Positions – Thumb tabs: Number of tab positions

Number · Regular+ · `s_thumbtabs` · cfg `thumbtabs/numtabs`  
Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> How many tabs can there be down a page. This is automatically calculated from the Height (or Length when rotated), Page size and Margins. If any of these change then this value will be updated. Increasing it, makes tabs overlap. Reducing it spreads them apart.

PTXprint overwrites your value when the page height, margins or tab size change. After the last position, the next book starts again at the top.

##### Length – Thumb tabs: Length

Number · Regular+ · `s_thumblength` · cfg `thumbtabs/length`  
Values: 3–40 (default 15) · Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> The length of the Thumb Tab measured in millimeters (mm).

Normal tabs: how far the tab reaches in; make it long enough for the longest book name. Rotated tabs: size along the page edge. Changing it recalculates **Number of Tab Positions** (for rotated tabs).

##### Grouped Tabs – Thumb tabs: Tabs grouped by books

Text box · Regular+ · `t_thumbgroups` · cfg `thumbtabs/groups`  
Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> List book IDs of short books to be grouped together at the same tab position. Use spaces between book IDs, and use ; to separate groups. There is no need to list all the book IDs here - only the special ones which need to share the same tab position.
>
> For example: PHM TIT; 1JN 2JN 3JN JUD
>
> When several shorter adjacent books occur, it is common to group them together to use the same tab position (but still have differently named tabs).

Books not listed get their own position.

##### Length – Thumb tabs: Rotate options

Drop-down · Regular+ · `fcb_rotateTabs` · cfg `thumbtabs/rotatetype`  
Choices: Each Facing Outward | Each Facing Inward | Rotate Both Anticlockwise | Rotate Both Clockwise · Needs: “Rotate Tabs”, “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> If you choose to Rotate the tabs, there are various options as to how these should be oriented. The preview (right) will show how these will appear on facing pages.

Outward and inward face opposite ways on left and right pages; the other two turn both pages the same way.

##### Restart Tabs at MAT

Checkbox, off · Regular+ · `c_thumbrestart` · cfg `thumbtabs/restart`  
Also: Thumb tabs: Restart tabs at New Testament · Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> Normally books will follow sequentially and if the next tab would be off the bottom of the page, then it will be set to the top for a new cycle of tabs. Setting this starts a new cycle at the start of the New Testament (Matthew).

Use it in a whole Bible, so the New Testament has its own run of tabs.

##### Grouped Tabs – Thumb tabs: Reload default book groups

Button · Regular+ · `btn_resetTabGroups`  
Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> Clicking this button will replace the Grouped Tabs list with the default groups.

The default groups include `RUT 1SA`, the Minor Prophets in two groups, and the short letters. Any groups you typed are lost.

##### \toc3

Radio · Regular+ · `r_thumbText_toc3` · cfg `thumbtabs/thumbtextmkr=toc3`  
Also: Thumb tabs: Use \toc3 text · Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> By default, Thumb Tabs use the content and styling of the \toc3 marker.
>
> Note that this setting is interconnected with the Table of Contents settings on the Peripherals tab. If \toc3 is not included in the ToC, then this option will be disabled. So it is recommended to use \toc3 as your thumbtab text and include it in the Table of Contents.

The usual choice.

##### \zthumbtab

Radio · Regular+ · `r_thumbText_zthumbtab` · cfg `thumbtabs/thumbtextmkr=zthumbtab`  
Also: Thumb tabs: Use \zthumbtab text · Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> By default, Thumb Tabs use the content and styling of the \toc3 marker. If you prefer different content and/or styling for the tabs, then this  
> \zthumbtab option needs to be enabled, and the thumbtab names entered into your USFM text.
>
> Note that this setting is interconnected with the Table of Contents settings on the Peripherals tab. If \toc3 is not included in the ToC, then you are forced to use the \zthumbtab setting here. For that reason it is highly recommended to use \toc3 as your thumbtab text and include it in the Table of Contents.
>
> The USFM extension \zthumbtab can be used to set an alternative value for the thumbtab contents. If a book's header contains a \zthumbtab entry, then  
> \toc3 will not be used as the thumbtab contents. An empty \zthumbtab entry specifies that there should be no text in the thumbtab for that book.

Use it if the tab text should differ from `\toc3`. Add the `\zthumbtab` line to each book's header in Paratext. With this option, **Edit Style** opens the `\zthumbtab` style.

##### Edit Style

Link · Regular+ · `lb_style_toc3`  
Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> Click to jump to the appropriate (\toc3 or \zthumbtab) marker in the style editor to change the formatting of the thumb tabs.

Change the text colour, font and size there. Changing the `\toc3` style may also change how `\toc3` text looks elsewhere, such as in the table of contents.

##### Only Show on Odd Pages

Checkbox, off · Regular+ · `c_tabsOddOnly` · cfg `thumbtabs/tabsoddonly`  
Also: Thumb tabs: Only Show on Odd Pages · Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> When printing thumb tabs on thin paper, it is preferable to only print these tabs on a single side of the page (the odd pages).

Better on thin paper, where a tab printed on both sides can show through.

#### Ornamental Decorations

##### Section Headings

Checkbox, off · Regular+ · `c_inclSectionHeader` · cfg `fancy/sectionheader`  
Also: Enable decorative section headings · Needs: “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Section Headings may be adorned with a special graphic. Ensure that there is adequate space - both horizontal as well as vertical to make sure all headings fit.

Choose **PDF border (Legacy)** for a fixed graphic or **Dynamic Border** for a box that fits the heading.

##### Border

Checkbox, off · Regular+ · `c_inclPageBorder` · cfg `fancy/pageborders`  
Also: Enable decorative borders · Needs: “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> There are different kinds of borders that can be applied to the publication.
>
> Note that if you use a border, it is likely that you will need to adjust the margins to make it fit.

Choose one of the three kinds below it.

##### End of Book Decoration

Checkbox, off · Regular+ · `c_inclEndOfBook` · cfg `fancy/endofbook`  
Also: Enable end of book decoration · Needs: “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> The end of each book may be adorned with a special graphic.

Front matter, glossaries and other non-Scripture books do not get it.

##### Verse Number Decorator

Checkbox, off · Regular+ · `c_inclVerseDecorator` · cfg `fancy/versedecorator`  
Also: Enable decorative verse numbers · Needs: “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Verse numbers can be decorated using either of the options shown below.

**End of Ayah** uses a character from the font; **Verse Border Graphic** uses a small PDF graphic.

##### Book Title Borders

Checkbox, off · Regular+ · `c_inclTitleBorders` · cfg `fancy/booktitleborder`  
Also: Enable dynamic title borders · Needs: “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Dynamic borders can be applied to book titles (\mt1 and \mt2). Styling can be adjusted using the link below.

PTXprint makes the `cat:titlebox|esb` style active for you. Use the link below to change its look.

##### Section Headings

###### Select...

Button · Regular+ · `btn_selectSectionHeaderPDF` · cfg `fancy/sectionheaderpdf`  
Also: Select decorative section headings · Needs: “PDF border (Legacy)”, “Section Headings”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

Chooses the section heading PDF graphic. The file name appears next to the button.

###### Shift – Decorative section headings: Vertical shift

Number · Regular+ · `s_inclSectionShift` · cfg `fancy/sectionheadershift`  
Values: -50–50 · Needs: “PDF border (Legacy)”, “Section Headings”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Vertical shift in pts of the section box image.  
>   + values shift the box upwards  
>   - values shift the box downwards

Same direction as **Shift** for the verse graphic. Change it in small steps (for example 2 pt) and print to check.

In older versions of PTXprint this worked the other way round. When you open a configuration saved by an older version, PTXprint changes the sign for you, so the graphic stays in place. A configuration saved by this version and opened in an older PTXprint moves the graphic the other way.

###### Scale – Decorative section headings: Scale

Number · Regular+ · `s_inclSectionScale` · cfg `fancy/sectionheaderscale`  
Needs: “PDF border (Legacy)”, “Section Headings”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Scale section header image. 1.0 = its own size,  
> 0.5 = half size, 2.0 = double size.

0.8 = 80%, 1.2 = 120%.

###### PDF border (Legacy)

Radio · Regular+ · `r_sectHead_legacy` · cfg `fancy/sectionborder=legacy`, `fancy/sectionbordertype=legacy`  
Needs: “Section Headings”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Place a PDF graphic behind each section heading (\s, \s1, \s2). Use Select... to choose it, and Scale/Shift to fit it.

It does not grow with the heading, so it suits headings that are always one line.

###### Dynamic Border

Radio · Regular+ · `r_sectHead_dynamic` · cfg `fancy/sectionborder=dynamic`, `fancy/sectionbordertype=dynamic`  
Needs: “Section Headings”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Draw a box around each section heading that grows with the heading. Its look is set by the cat:headingsbox|esb style.

PTXprint makes the `cat:headingsbox|esb` style active for you. Use the link to change it.

###### \cat:headingsbox|esb

Link · Regular+ · `lb_style_cat:headingsbox|esb`  
Needs: “Dynamic Border”, “Section Headings”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> If Section Headings sometimes extend to more than one line, then a static PDF section heading is unlikely to work. Instead, a dynamically generated decorative section heading needs to be set up to grow/shrink with the content of the heading. Use this link to show the special style, which needs to be enabled and defined.

On the **Styles** tab set the background colour and, with **Borders...**, the border of the box around headings.

##### Border

###### Select...

Button · Regular+ · `btn_selectPageBorderPDF` · cfg `fancy/pageborderpdf`  
Also: Select decorative borders · Needs: “PDF border (Legacy)”, “Border”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

Chooses the page border PDF. It starts in PTXprint's border-art folder.

###### Full page

Checkbox, off · Regular+ · `c_borderPageWide` · cfg `fancy/pageborderfullpage`, `fancy/pagebordernfullpage_`  
Also: Decorative borders: Expand to fill page · Needs: “PDF border (Legacy)”, “Border”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> If set, the border is expanded to the full page. Otherwise it is expanded only to the gutter margins.

If unticked, the graphic is stretched to the page size without the binding gutter.

###### \textborder

Link · Regular+ · `lb_style_textborder`  
Needs: “Dynamic Border”, “Border”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Click to edit the properties of the Text Border (which is controlled by the \textborder style on the Styles tab).

Change the border there with **Borders...** in **Sidebar Settings**.

###### PDF border (Legacy)

Radio · Regular+ · `r_border_pdf` · cfg `fancy/pageborder`  
Needs: “Border”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Use an existing PDF Border for the entire publication.

Choose the graphic with **Select...**. It is stretched to the page without the binding gutter, or to the whole page if **Full page** is ticked.

###### Dynamic Border

Radio · Regular+ · `r_border_text` · cfg `fancy/pagebordertype=text`  
Needs: “Border”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Place a decorative border only around the Scripture text (excludes introductions, footnotes and other peripheral material).

Its look comes from the `textborder` style (**Styles** tab, **Other** category); PTXprint makes that style active for you. Change it with **Borders...** in **Sidebar Settings**.

###### Page Border

Radio · Regular+ · `r_border_page` · cfg `fancy/pagebordertype=page`  
Needs: “Border”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Place a uniform-sized decorative border on every page regardless of content.

If you do not get the result you want, use **Dynamic Border** or **PDF border (Legacy)**.

###### \pageborder

Link · Regular+ · `lb_style_pageborder`  
Needs: “Page Border”, “Border”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Click to edit the properties of the Page Border (which is controlled by the \pageborder style on the Styles tab).

Refers to the `\pageborder` style. (Clicking it does not open the style; see **Common problems**.)

##### End of Book Decoration

###### Select...

Button · Regular+ · `btn_selectEndOfBookPDF` · cfg `fancy/endofbookpdf`  
Also: Select end of book decoration · Needs: “End of Book Decoration”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

Chooses the end-of-book PDF. It is centred below the last line of each book.

##### Verse Number Decorator

###### End of Ayah

Radio · Regular+ · `r_decorator_ayah` · cfg `fancy/versedecoratortype=ayah`  
Also: Decorative verse numbers: Use end of Ayah · Needs: “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Use the End of Ayah character in the font to decorate the verse number.

The character is U+06DD. If the font lacks it you see empty boxes. **Move Ayah** puts the number at the end of the verse.

###### Verse Border Graphic

Radio · Regular+ · `r_decorator_file` · cfg `fancy/versedecoratortype=file`  
Also: Decorative verse numbers: Use verse border graphic · Needs: “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Use a PDF graphic to decorate the verse number. You may need to also adjust the font properties to ensure the verse numbers fit within the graphic.

Choose it with **Select...**; adjust with **Scale** and **Shift**.

###### \vp

Link · Regular+ · `lb_style_vp`  
Needs: “Move Ayah”, “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Click to edit the \vp marker's properties on the Styles tab.

`\vp` is used for the verse numbers when **Move Ayah** is ticked.

###### Select...

Button · Regular+ · `btn_selectVerseDecorator` · cfg `fancy/versedecoratorpdf`  
Also: Select verse border graphic · Needs: “Verse Border Graphic”, “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

Chooses the verse number PDF. PTXprint suggests its own star graphic.

###### Shift – Verse border graphic: Vertical shift

Number · Regular+ · `s_verseDecoratorShift` · cfg `fancy/versedecoratorshift`  
Values: -20–20 · Needs: “Verse Border Graphic”, “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Vertical shift in pts of the verse decorator image.  
>   + values shift the decorator upwards  
>   - values shift the decorator downwards

Use small steps, for example 0.5 pt.

###### Scale – Verse border graphic: Scale

Number · Regular+ · `s_verseDecoratorScale` · cfg `fancy/versedecoratorscale`  
Needs: “Verse Border Graphic”, “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Scale verse decorator image. 1.0 = its own size,  
> 0.5 = half size, 2.0 = double size.

Make it bigger if two- or three-digit verse numbers do not fit.

###### Move Ayah

Checkbox, off · Regular+ · `c_decorator_endayah` · cfg `fancy/endayah`  
Also: Decorative verse numbers: Move Ayah to end of verse · Needs: “End of Ayah”, “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> This option moves the Ayah to the end of the verse.

As is usual in Arabic-script layout. When ticked, the `\vp` link becomes available to style the moved numbers.

###### \v

Link · Regular+ · `lb_style_v`  
Needs: “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Click to edit the \v marker's properties on the Styles tab.

Change the font size, colour and position of the verse numbers there so they fit the decoration.

##### Book Title Borders

###### \cat:titlebox|esb

Link · Regular+ · `lb_style_cat:titlebox|esb`  
Needs: “Book Title Borders”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Adjust the styling of the dynamic borders around book titles.

Change the background colour there, and use **Borders...** in **Sidebar Settings** for the border.
