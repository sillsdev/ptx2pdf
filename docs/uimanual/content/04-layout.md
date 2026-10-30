## What this tab is for

The **Layout** tab sets the shape of every page: page size, margins (the empty space around the text), one or two columns, the size of the main text and the space between lines.

Come here when you start a new publication, when the printer tells you the page size, or when the text does not fit the number of pages you want. Most settings change the whole book. After a change, click **Print** again to see the result.

Some words used in this chapter:

* **pt (point)** – a small unit used for type. 1 pt is about 0.35 mm. 72 pt is about one inch (25.4 mm).
* **Baseline** – the invisible line that the letters sit on.
* **Line spacing** – the distance from the baseline of one line to the baseline of the next.
* **Gutter** – an extra empty space. A *binding gutter* is extra space at the spine of the book. A *column gutter* is the space between two columns of text.
* **Text area** – the part of the page where the main text goes. The margins are outside it.

## Page Setup

This area holds **Page Size**, **Base Font Size (pt)**, **Base Line Spacing (pt)**, **Base Indent**, the binding gutter and the page-layout options.

### Page size

Choose a size from the **Page Size** list, or type your own: width, comma, height, for example `148mm, 210mm`. You can use `mm`, `cm` or `in`. A typed size is saved when you save the configuration (or click **Print**). After that, it is in the list for all your projects. To remove a saved size, select it, right-click in the box and choose **Remove**. Ask your printer for the exact trim size (the size of the finished, cut page) before you start. Changing the page size later moves every line.

### Font size and line spacing (and how they work together)

* **Base Font Size (pt)** is the size of the letters in normal paragraphs. All other text (headings, footnotes, verse numbers and so on) is sized *relative to* it. A bigger base font makes headings and footnotes grow by the same proportion.
* **Base Line Spacing (pt)** is the distance from one line to the next. It is normally bigger than the font size, so that the lines do not touch. 11 pt text with 14 pt line spacing is a common choice.

The **Lock Ratio** box (ticked by default) joins these two numbers:

* When it is ticked and you change the font size, the line spacing changes by the same proportion. For example, 11 pt text on 14 pt spacing changed to 12 pt text gives about 15.3 pt spacing. The page keeps the same "look", only bigger.
* It also works the other way round: changing the line spacing changes the font size.
* When it is not ticked, you can change each number on its own. Use this for more (or less) space between lines with the same size letters.
* When you tick it again, PTXprint keeps the ratio the two numbers have *now*.

The line spacing decides how many lines fit on a page.

### Lines Per Page and the fine-tune buttons

**Lines Per Page** is calculated from the page height, the top and bottom margins and the line spacing. It updates when you change any of these.

* **Blue**: a whole number of lines fits the text area. No space is wasted.
* **Red**: the text area holds a whole number of lines plus part of a line. That part of a line is empty space at the bottom of each page.

When the number is red, three small fine-tune buttons (icon of justified lines) become active. One is next to **Base Line Spacing (pt)**. The other two are next to the top and bottom margins in the **Margins** area. Each makes a small change so that a whole number of lines fits:

* If more than half a line is spare, it makes room for one more line.
* If less than half a line is spare, it spreads the same lines a little further apart (or makes the margin a little larger).

Click only **one** of the three buttons: the one for the setting you are most willing to change. The number turns blue and the buttons become grey again.

If **Lock Ratio** is ticked, the line-spacing button also changes the font size a little. To keep the font size exact, untick **Lock Ratio** first, or use a margin button.

### Binding gutter, Outer Gutter and Mirror Pages

* **Binding Gutter (mm)** adds extra space to the inner edge of each page (near the spine), on top of **Side Margin Width**. Thick books need more, because the pages curve into the spine. The gutter changes sides on odd and even pages, so it is always at the spine.
* **Outer Gutter** moves that extra space to the outer edge, for journaling or wide-margin Bibles where readers write in the outer margin.
* **Mirror Pages** makes odd and even pages mirror each other. Header items on the left of a right-hand page appear on the right of a left-hand page, so they stay on the outer (or inner) edge. In a diglot (two-language) layout it also keeps the primary text on the inner side, near the spine.

Whether the gutter swaps sides on odd and even pages is controlled by **Double Sided Layout** (**Advanced** tab, **Other** tab, **Page Layout and Spacing**). It is normally on.

### Align Text to Baseline / Variable Line Spacing

This is a switch with **Align Text to Baseline** on the left and **Variable Line Spacing** on the right.

* **Align Text to Baseline** (left, the normal setting) puts every line on a fixed grid. Lines on the front and back of a sheet line up exactly. This matters on thin Bible paper, where the other side shows through. But some columns may end with an empty line or two. You fix these by hand with the page-filling tools in the PDF Preview.
* **Variable Line Spacing** (right) stretches the space between lines a little so that every column is filled to the bottom. Good for quick drafts and thicker paper. Front-to-back alignment is lost, and the whole book re-flows when you change it.

Switching to **Variable Line Spacing** also ticks **Fill Columns** and **Allow Unbalanced Columns**. How much lines may stretch or shrink is set on the **Advanced** tab, **Other** tab, **Page Layout and Spacing**.

### Notelines (journaling layout)

**Notelines** prints ruled lines in a wide margin for readers' own notes. Ticking it also ticks **Binding Gutter** and **Outer Gutter**, and sets the gutter to 40 mm if it was under 30 mm. A colour button appears for the line colour. More noteline settings (spacing, offset, type) are on the **Advanced** tab, **Other** tab, **Page Layout and Spacing**.

### Margin Notes

**Margin Notes Col Width (mm)** creates an extra column beside the text. Footnotes, cross-references and (if you choose) section headings can go in it, beside their verse. Ticking it only creates the space. To put notes there, choose **Side Margin** as the position on the **Notes+Refs** tab. To put headings there, tick **In Margin** on the **Body** tab.

The column is normally on the right (or outer) edge. In a one-column layout, tick **Margin Notes on Left/Inner** to put it on the left (or inner) edge.

If too many notes do not fit beside the text in one column, PTXprint moves the extra notes to the top of the margin column of the next column or page. This happens by itself; there is no setting for it. Check those pages in the PDF Preview, because a moved note is no longer beside its verse.

These settings are shown in the **Regular** and **Full** views.

## Two Column Layout

Tick **Two Column Layout** for two columns of main text; untick it for one. When you change this, PTXprint halves (two columns) or doubles (one column) **Base Indent**, because a narrow column needs a smaller indent.

Most settings in this area only work with two columns:

* **Gutter Width (mm)** – the space between the columns. 4 mm is common.
* **Vertical Rule in Gutter** – a thin line down the middle of the gutter.
* **Adjust Top (pt)** – moves the top of that line up (negative) or down (positive). Greyed out until **Vertical Rule in Gutter** is ticked.
* **Allow Unbalanced Columns** – lets the two columns on a page end at different heights, by up to a set number of lines.

**Thickness of Rule (pt)** also works in one column, because it also sets the horizontal rule under the header.

A diglot (two languages side by side) needs two columns, so the **Two Column Layout** box is then greyed out.

## Margins

The **Margins** area sets the empty space around the text, and the position of the header (the line at the top of the page, often with the book name and page number) and the footer (the line at the bottom).

### The margin diagram and its colours

Next to the margin settings is a small picture of a page. It shows one or two columns, the vertical rule and the header rule, as you have set them. Coloured arrows show what each number measures:

* **Orange** – **Side Margin Width (mm)**: from the edge of the page to the text.
* **Red** (top) – **Start of Page to Top of Text (mm)**: the top margin.
* **Red** (bottom) – **Bottom of Text to End of Page (mm)**: the bottom margin.
* **Purple** (top) – **Bottom of Header to Top of Text (pt)**: header-to-text gap.
* **Purple** (bottom) – **Bottom of Text to Top of Footer (pt)**: text-to-footer gap.
* **Green** – **Space between Rule and Top of Text (pt)**: rule-to-text gap.
* **Blue** – two values PTXprint calculates (you cannot type in them): top of page to header, and footer to bottom of page.

When the mouse is over a margin box, the picture shows only that box's arrow.

Margins are in **mm**, but the header and footer gaps are in **pt**.

### Header and footer position

The header sits *inside* the top margin, and the footer normally sits *inside* the bottom margin. So a bigger header gap moves the header up towards the page edge. Watch the blue numbers: if one becomes very small (or negative), the header or footer is too close to the edge and may be cut off when the book is trimmed.

Tick **Place Footer Text Above the Bottom Margin** to put the footer inside the text area instead of in the margin.

Tick **Horizontal Rule** to draw a line under the header. Set its position with **Space between Rule and Top of Text (pt)**.

To see the margins, header and footer areas on the page, tick **Guides and Baselines** on the **Content** tab of the **PDF Preview** window.

## Change the Grid Settings dialog (graph paper)

PTXprint can show a "graph paper" grid over the pages in the **PDF Preview**, to measure things such as a margin or a picture.

Open the **PDF Preview**, go to its **Content** tab and tick **Graph Paper**. Click **Settings** next to it to open the **Change the Grid Settings** dialog. There you choose:

* **Major Units** – centimetres or inches between the thicker (major) lines, plus their colour and thickness.
* **Minor Divisions** – how many thinner lines between two major lines, plus their colour and thickness.
* **Place Grid** – **Whole Page**, **In Margin Areas** or **Only in Text Area**.

## Lock UI Layout Settings

When the typesetting is almost finished, you can protect the layout from accidental changes. On the **Advanced** tab, **Main** tab, **General** area, tick **Lock UI Layout Settings**. (This is only shown in the **Full** view.)

While it is ticked, most of the **Layout** tab is greyed out (page size, font size, line spacing, columns, gutter, margins and more). The whole **Fonts+Script** tab and the **Styles** tab are also greyed out. Untick it to make changes again.

## Common tasks

### How do I change the page size?

1. On the **Layout** tab, **Page Setup** area, click the **Page Size** list.
2. Choose a size, for example **148mm, 210mm (A5)**, or type width, comma, height, for example `140mm, 216mm`.
3. If **Lines Per Page** is red, click one fine-tune button (see the next task).
4. Click **Print**.

### How do I stop wasting space at the bottom of every page?

1. On the **Layout** tab, look at **Lines Per Page** (shown in the **Regular** and **Full** views).
2. If it is red, click one fine-tune button: next to **Base Line Spacing (pt)**, or in the **Margins** area next to the top or bottom margin. Choose the setting you are most willing to change.
3. The number turns blue. Click **Print**.

### How do I make the text bigger or smaller without changing the look of the page?

1. On the **Layout** tab, make sure **Lock Ratio** is ticked.
2. Change **Base Font Size (pt)**. The line spacing changes with it.
3. If **Lines Per Page** is red, click one fine-tune button.
4. Click **Print**.

### How do I put more space between the lines but keep the same letter size?

1. On the **Layout** tab, untick **Lock Ratio**.
2. Make **Base Line Spacing (pt)** larger, for example from 14 to 15.
3. Tick **Lock Ratio** again if you want the new ratio kept.
4. Click **Print**.

### How do I change between one and two columns?

1. On the **Layout** tab, tick or untick **Two Column Layout**.
2. For two columns, set **Gutter Width (mm)** and choose whether you want **Vertical Rule in Gutter**.
3. Check **Base Indent**. PTXprint changes it automatically, but you may want to adjust it.
4. Click **Print**.

### How do I add extra space at the spine for binding?

1. On the **Layout** tab, **Page Setup** area, tick **Binding Gutter (mm)**.
2. Type the extra space in the box beside it, for example 5 mm. Ask your printer how much your book's thickness needs.
3. Leave **Outer Gutter** unticked.
4. Click **Print**.

### How do I make a journaling (wide-margin) Bible?

1. On the **Layout** tab, tick **Notelines** (shown in the **Regular** and **Full** views). PTXprint ticks **Binding Gutter** and **Outer Gutter** and sets a wide gutter (at least 40 mm).
2. Change the gutter width if needed, and choose the line colour with the colour button.
3. Click **Print**.

### How do I put footnotes and cross-references in the side margin?

1. On the **Layout** tab, tick **Margin Notes Col Width (mm)** and type the column width.
2. On the **Notes+Refs** tab, set the position of footnotes and/or cross-references to **Side Margin**.
3. For section headings in the margin too, tick **In Margin** on the **Body** tab.
4. For the column on the left (or inner) edge, tick **Margin Notes on Left/Inner** (one column only).
5. Click **Print**.

### How do I see a measuring grid on the page?

1. Click **Print** so that the **PDF Preview** opens.
2. On the preview's **Content** tab, tick **Graph Paper**.
3. Click **Settings** next to it to change units, colours and where the grid is drawn. Click **OK**.

## Common problems

### Almost everything on the Layout tab is greyed out

**Cause:** **Lock UI Layout Settings** is ticked. This also greys out the whole **Fonts+Script** tab and the **Styles** tab.

**What to do:** Change the view level to **Full**. On the **Advanced** tab, **Main** tab, **General** area, untick **Lock UI Layout Settings**.

### I changed the font size and the line spacing changed too (or the other way round)

**Cause:** **Lock Ratio** is ticked (the normal setting).

**What to do:** Untick **Lock Ratio** before you change one number on its own.

### I clicked the line-spacing fine-tune button and my font size changed

**Cause:** **Lock Ratio** is ticked, so the font size follows the line spacing.

**What to do:** Untick **Lock Ratio** and type your font size again. Then use the fine-tune button again, or use the top or bottom margin button instead.

### The fine-tune buttons are greyed out

**Cause:** **Lines Per Page** is already a whole number (blue), so there is nothing to fix. They are also greyed out when **Lock UI Layout Settings** is ticked.

### The fine-tune buttons and Lines Per Page are not visible

**Cause:** They are only shown in the **Regular** and **Full** views. Change the view level from the main menu.

### I cannot untick Two Column Layout

**Cause:** A diglot (two languages) is set up. A diglot needs two columns.

### The Base Indent changed by itself

**Cause:** Switching between one and two columns halves or doubles the indent.

**What to do:** Type the indent you want after you change the number of columns.

### "Margin Notes on Left/Inner" is greyed out

**Cause:** It only works with one column, and only when **Margin Notes Col Width (mm)** is ticked.

### Margin notes do not appear even though I ticked Margin Notes

**Cause:** The Layout tab setting only makes the space.

**What to do:** On the **Notes+Refs** tab, choose **Side Margin** for footnotes and/or cross-references.

### The header or footer is too close to the edge of the page

**Cause:** The header or footer gap is large compared with the top or bottom margin. The header and footer sit inside the margins.

**What to do:** Check the blue numbers in the margin diagram. Make the top (or bottom) margin larger, or make **Bottom of Header to Top of Text (pt)** (or **Bottom of Text to Top of Footer (pt)**) smaller.

### Columns end at different heights, or there are gaps at the bottom of columns

**Cause:** With **Align Text to Baseline**, lines sit on a fixed grid, so some columns can end early.

**What to do:** For a draft, move the switch to **Variable Line Spacing**. For a final Bible on thin paper, keep **Align Text to Baseline** and fix the pages with the page-filling tools in the PDF Preview. In two columns, **Allow Unbalanced Columns** also lets the columns end at different heights.

### The binding gutter is always on the same side of the page

**Cause:** **Double Sided Layout** is off (**Advanced** tab, **Other** tab, **Page Layout and Spacing**). Or **Outer Gutter** is ticked, which moves the gutter to the outside edge.

### The Notelines colour button is missing

**Cause:** It is only shown when **Notelines** is ticked.

## Control notes

### @btn_guides_ok
Redraws the PDF Preview with the new grid (shown only if **Graph Paper** is ticked).

### @btn_guides_cancel
Closes the dialog. The grid in the preview is not redrawn.

### @col_gridMajor
A strong colour (for example red) makes the major lines easy to count.

### @col_gridMinor
A light colour keeps the text readable under the grid.

### @s_gridMajorThick
In pt. Small values such as 0.2 are usually enough.

### @s_gridMinorThick
In pt. Keep it at or below the major thickness so the two kinds of line look different.

### @s_gridMinorDivisions
With **Centimeters**, 5 gives 2 mm squares and 10 gives 1 mm squares.

### @btn_resetGrid
Puts all grid settings back to the defaults listed in the tooltip.

### @fcb_gridUnits
Use the unit your printer or publisher uses for their measurements.

### @fcb_gridOffset
**Whole Page** starts at the top-left corner of the page: best for measuring margins. **Only in Text Area** starts at the corner of the text: best for measuring things in the text, such as pictures. **In Margin Areas** draws the grid only in the margins, so the text stays clear.

### @c_pagegutter
Thick books need more space because the pages curve into the binding. Ask your printer for a value. **Notelines** ticks this for you.

### @s_pagegutter
In mm. A few mm is common for a normal book; 40 mm or more for a journaling layout.

### @s_linespacing
A bigger value gives fewer lines per page. If **Lock Ratio** is ticked, changing this also changes **Base Font Size (pt)**. Line spacing for other paragraph types (for example footnotes) is set relative to this on the **Styles** tab.

### @ecb_pagesize
The finished (trimmed) page size. You can use mm, cm or in. A typed size is saved when you save the configuration. Set this before detailed page work, because every page re-flows when it changes.

### @s_fontsize
Headings, footnotes, verse numbers and other text grow or shrink with it. 9–12 pt is typical for Bibles. If **Lock Ratio** is ticked, changing this also changes **Base Line Spacing (pt)**.

### @s_indentUnit
0.5 inch is about 13 mm. Each paragraph style uses a multiple of this value. PTXprint halves it when you switch to two columns and doubles it when you switch to one.

### @l_linesOnPage
Blue: a whole number of lines fits. Red: part of a line is wasted at the bottom of each page; click one fine-tune button. The estimate uses page height, top and bottom margins, line spacing and the font. It does not know about headings, pictures or footnotes.

### @l_linesOnPageLabel
Label for the estimate beside it.

### @btn_adjust_spacing
Only active when **Lines Per Page** is red. To keep the font size exact, untick **Lock Ratio** first or use a margin fine-tune button.

### @c_outerGutter
You still need a normal side margin for the spine.

### @c_lockFontSize2Baseline
When you tick it again, the current ratio is kept. While ticked, the line-spacing fine-tune button also changes the font size.

### @c_noGrid
Left (**Align Text to Baseline**): every line on a fixed grid; best for final Bibles on thin paper. Right (**Variable Line Spacing**): line spacing stretches to fill columns; best for drafts and thick paper. Switching right also ticks **Fill Columns** and **Allow Unbalanced Columns**.

### @c_variableLineSpacing
Ticked automatically when you move the switch to **Variable Line Spacing**. The stretch allowed is set on the **Advanced** tab, **Other** tab, **Page Layout and Spacing**.

### @c_noteLines
Ticking it also ticks **Binding Gutter** and **Outer Gutter**, and sets the gutter to 40 mm if it was under 30 mm. A colour button appears beside it.

### @col_noteLines
Shown only when **Notelines** is ticked. A light grey or light colour does not distract from the text.

### @c_mirrorpages
For example, the page number stays on the outer edge of both left and right pages.

### @c_useMarginNotes
This only makes the space. For footnotes or cross-references, choose **Side Margin** on the **Notes+Refs** tab. For headings, tick **In Margin** on the **Body** tab.

### @s_marginNotesWidth
Make it wide enough for a few short words per line. The main text becomes narrower by this amount.

### @c_marginNotesInner
PTXprint unticks it when you switch to two columns.

### @s_colgutterfactor
A **Vertical Rule in Gutter** is drawn in the middle of this space. 3–6 mm is common.

### @s_colgutteroffset
Use it if the line starts too close to the header rule or too far from the first line of text. Greyed out unless **Two Column Layout** and **Vertical Rule in Gutter** are both ticked.

### @s_ruleThickness
Stays available in a one-column layout, because it also sets the header rule.

### @c_verticalrule
Many Bibles use it.

### @c_allowUnbalanced
Very useful with **Variable Line Spacing**. The maximum difference is **Unbalanced Lines (Max)** on the **Advanced** tab, **Other** tab, **Page Layout and Spacing**.

### @c_doublecolumn
Switching re-flows the whole book and halves or doubles **Base Indent**.

### @s_headerposition
The header sits inside the top margin, so a bigger value moves it up towards the page edge. Watch the blue number in the diagram.

### @s_footerposition
The footer normally sits inside the bottom margin, so a bigger value moves it down towards the page edge. Watch the blue number in the diagram.

### @s_bottommargin
The footer sits in this space (unless **Place Footer Text Above the Bottom Margin** is ticked). Changing it changes **Lines Per Page**.

### @s_margins
10–15 mm is common.

### @s_rhruleposition
Shown by the green arrow in the margin diagram.

### @s_topmargin
The header sits in this space. Changing it changes **Lines Per Page**.

### @btn_adjust_top
Only active when **Lines Per Page** is red. Use it to keep line spacing and font size exactly as they are.

### @btn_adjust_bottom
Only active when **Lines Per Page** is red. Use it to keep line spacing, font size and top margin exactly as they are.

### @c_noinkinmargin
Use it when the printer needs the whole margin empty. The text area becomes a little shorter.

### @l_footer2edge
Calculated; you cannot type in it. Shown by the blue arrow at the bottom of the diagram. If it is very small, the footer may be cut off when the pages are trimmed.

### @c_rhrule
Set its position with **Space between Rule and Top of Text (pt)** and its thickness with **Thickness of Rule (pt)**.

### @l_margin2header
Calculated; you cannot type in it. Shown by the blue arrow at the top of the diagram. If it is very small or negative, make the top margin larger or the header gap smaller.
