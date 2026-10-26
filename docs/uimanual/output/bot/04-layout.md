# 7. Layout tab

## 7.1 What this tab is for

The **Layout** tab sets the shape of every page: page size, margins (the empty space around the text), one or two columns, the size of the main text and the space between lines.

Come here when you start a new publication, when the printer tells you the page size, or when the text does not fit the number of pages you want. Most settings change the whole book. After a change, click **Print** again to see the result.

Some words used in this chapter:

* **pt (point)** – a small unit used for type. 1 pt is about 0.35 mm. 72 pt is about one inch (25.4 mm).
* **Baseline** – the invisible line that the letters sit on.
* **Line spacing** – the distance from the baseline of one line to the baseline of the next.
* **Gutter** – an extra empty space. A *binding gutter* is extra space at the spine of the book. A *column gutter* is the space between two columns of text.
* **Text area** – the part of the page where the main text goes. The margins are outside it.

## 7.2 Page Setup

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

## 7.3 Two Column Layout

Tick **Two Column Layout** for two columns of main text; untick it for one. When you change this, PTXprint halves (two columns) or doubles (one column) **Base Indent**, because a narrow column needs a smaller indent.

Most settings in this area only work with two columns:

* **Gutter Width (mm)** – the space between the columns. 4 mm is common.
* **Vertical Rule in Gutter** – a thin line down the middle of the gutter.
* **Adjust Top (pt)** – moves the top of that line up (negative) or down (positive). Greyed out until **Vertical Rule in Gutter** is ticked.
* **Allow Unbalanced Columns** – lets the two columns on a page end at different heights, by up to a set number of lines.

**Thickness of Rule (pt)** also works in one column, because it also sets the horizontal rule under the header.

A diglot (two languages side by side) needs two columns, so the **Two Column Layout** box is then greyed out.

## 7.4 Margins

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

## 7.5 Change the Grid Settings dialog (graph paper)

PTXprint can show a "graph paper" grid over the pages in the **PDF Preview**, to measure things such as a margin or a picture.

Open the **PDF Preview**, go to its **Content** tab and tick **Graph Paper**. Click **Settings** next to it to open the **Change the Grid Settings** dialog. There you choose:

* **Major Units** – centimetres or inches between the thicker (major) lines, plus their colour and thickness.
* **Minor Divisions** – how many thinner lines between two major lines, plus their colour and thickness.
* **Place Grid** – **Whole Page**, **In Margin Areas** or **Only in Text Area**.

## 7.6 Lock UI Layout Settings

When the typesetting is almost finished, you can protect the layout from accidental changes. On the **Advanced** tab, **Main** tab, **General** area, tick **Lock UI Layout Settings**. (This is only shown in the **Full** view.)

While it is ticked, most of the **Layout** tab is greyed out (page size, font size, line spacing, columns, gutter, margins and more). The whole **Fonts+Script** tab and the **Styles** tab are also greyed out. Untick it to make changes again.

## 7.7 Common tasks

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

## 7.8 Common problems

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

## 7.9 Settings reference

### Change the Grid Settings (dialog)

#### OK

Button · Regular+ · `btn_guides_ok`

Redraws the PDF Preview with the new grid (shown only if **Graph Paper** is ticked).

#### Cancel

Button · Regular+ · `btn_guides_cancel`

Closes the dialog. The grid in the preview is not redrawn.

#### Grid Settings

##### Major Units – Grid: Major line color

Colour · Regular+ · `col_gridMajor` · cfg `grid/majorcolor`

> The color of the major (thicker) grid lines.

A strong colour (for example red) makes the major lines easy to count.

##### Minor Divisions – Grid: Minor line color

Colour · Regular+ · `col_gridMinor` · cfg `grid/minorcolor`

> The color of the minor (thinner) grid lines between the major lines.

A light colour keeps the text readable under the grid.

##### Major Units – Grid: Major line thickness

Number · Regular+ · `s_gridMajorThick` · cfg `grid/majorthickness`

> Specify the thickness of the major lines.

In pt. Small values such as 0.2 are usually enough.

##### Minor Divisions – Grid: Minor line thickness

Number · Regular+ · `s_gridMinorThick` · cfg `grid/minorthickness`

> Specify the line thickness of the minor divisions.

In pt. Keep it at or below the major thickness so the two kinds of line look different.

##### Minor Divisions – Grid: Number of minor divisions

Number · Regular+ · `s_gridMinorDivisions` · cfg `grid/divisions`, `grid/xyadvance`

> Specify the number of minor divisions there should be between the thicker (major) lines. Recommendations: 2, 5, or 10 for centimeters, and 3, 4, 6, or 12 for inches.

With **Centimeters**, 5 gives 2 mm squares and 10 gives 1 mm squares.

##### Place Grid – Grid: Reload default values

Button · Regular+ · `btn_resetGrid`

> Clicking this button will refresh the default Grid settings:  
> Centimeters with 5 divisions (2mm each), red major and light blue minor lines (0.2pt thickness), over the whole page.

Puts all grid settings back to the defaults listed in the tooltip.

##### Major Units – Grid: Select major units

Drop-down · Regular+ · `fcb_gridUnits` · cfg `grid/units`  
Choices: Centimeters | Inches

> The grid can use Centimeters or Inches as the major units.

Use the unit your printer or publisher uses for their measurements.

##### Place Grid – Grid: Starting position (page or margin)

Drop-down · Regular+ · `fcb_gridOffset` · cfg `grid/xyoffset`  
Choices: Whole Page | In Margin Areas | Only in Text Area

> The grid can start at the top-left corner of the Page, or at the top-left Margin.
>
> Depending on what you are trying to measure, it can be helpful to position the grid at the top-left corner of the page, or margins.

**Whole Page** starts at the top-left corner of the page: best for measuring margins. **Only in Text Area** starts at the corner of the text: best for measuring things in the text, such as pictures. **In Margin Areas** draws the grid only in the margins, so the text stays clear.

### Layout

#### Two Column Layout

Checkbox, on · Mini+ · `c_doublecolumn` · cfg `paper/columns`  
Also: One or two column layout · Greyed out by: “Lock UI Layout Settings”

> Tick to set the main text in two columns; untick for a single column.
>
> If this setting is checked on, but inactive, it is due to Diglot being active (which obviously must use the Two Column layout).
>
> If you get an unexpected result, check the "Use One/Two Column Layout ..." setting near the end of the Body tab which is only accessible when using the Full View mode.

Switching re-flows the whole book and halves or doubles **Base Indent**.

#### Page Setup

##### Binding Gutter (mm)

Checkbox, off · Basic+ · `c_pagegutter` · cfg `paper/ifaddgutter`  
Also: Use binding gutter · Greyed out by: “Lock UI Layout Settings”

> This is the amount of space to be given on the inner edge of each page for binding (millimeters).
>
> However, if Outer Gutter is enabled this extra space will appear on the outside edge of each page. This can be useful for a journaling layout.

Thick books need more space because the pages curve into the binding. Ask your printer for a value. **Notelines** ticks this for you.

##### Binding gutter amount

Number · Basic+ · `s_pagegutter` · cfg `paper/gutter`  
Values: -200–200 · Needs: “Binding Gutter (mm)” · Greyed out by: “Lock UI Layout Settings”

> This amount is added to the ‘Side Margin Width’ amount to the inner edge (or outside edge, if you check ‘Outer Gutter’).

In mm. A few mm is common for a normal book; 40 mm or more for a journaling layout.

##### Base Line Spacing (pt) – Base line spacing

Number · Basic+ · `s_linespacing` · cfg `paragraph/linespacing`  
Values: 4–100 (default 14) · Greyed out by: “Lock UI Layout Settings”

> Base Line spacing in points (pts). Change to increase or decrease space between lines of text.
>
> This is the base line spacing for default paragraph text.

A bigger value gives fewer lines per page. If **Lock Ratio** is ticked, changing this also changes **Base Font Size (pt)**. Line spacing for other paragraph types (for example footnotes) is set relative to this on the **Styles** tab.

##### Page Size – Page size setting

Drop-down · Mini+ · `ecb_pagesize` · cfg `paper/height`, `paper/width`, `paper/pagesize`  
Choices: 210mm, 297mm (A4) | 148mm, 210mm (A5) | 105mm, 148mm (A6) | 176mm, 250mm (B5) | 125mm, 176mm (B6) | 210mm, 280mm (PA4) | 140mm, 210mm (PA5) | 105mm, 140mm (PA6) | 8.5in, 11in (Letter) | 5.5in, 8.5in (1/2 Letter) | 5.25in, 8.25in (133x210mm) | 5.8in, 8.7in (147x221mm) | 6in, 9in (152x229mm) | 184.6mm, 271.6mm (A4 with cropmarks) | 165mm, 234mm (KBS max page) · Greyed out by: “Lock UI Layout Settings”

> Type required page width and height,  
>      for example:    148mm, 208mm or select from the list of preset values. A size you type is saved for use in all projects. To remove one, right-click it and choose Remove.

The finished (trimmed) page size. You can use mm, cm or in. A typed size is saved when you save the configuration. Set this before detailed page work, because every page re-flows when it changes.

##### Base Font Size (pt) – Base font size

Number · Mini+ · `s_fontsize` · cfg `paper/fontfactor`  
Values: 2–36 (default 11) · Greyed out by: “Lock UI Layout Settings”

> Set the point size of the main body text.
>
> This is the base font size for default paragraph text. All other font sizes are calculated (according to their factor size) based on this value.

Headings, footnotes, verse numbers and other text grow or shrink with it. 9–12 pt is typical for Bibles. If **Lock Ratio** is ticked, changing this also changes **Base Line Spacing (pt)**.

##### Base Indent – Base paragraph indent

Number · Regular+ · `s_indentUnit` · cfg `document/indentunit`  
Greyed out by: “Lock UI Layout Settings”

> The amount by which paragraphs should be indented (inches). This also affects poetry indentation. (default=1, min=0, max=4)
>
> The space by which paragraphs should be indented (inches). This also affects poetry indentation. Note that for a single-column text this value needs to be higher than for two-column texts, and the value updates automatically when you change from 1 to 2 columns, and vice versa.

0.5 inch is about 13 mm. Each paragraph style uses a multiple of this value. PTXprint halves it when you switch to two columns and doubles it when you switch to one.

##### 99.9

Label · Regular+ · `l_linesOnPage`

> This is an approximate calculation of the most number of lines that will fit on a page. An exact count is difficult due to ascent and descent values of the main body font.

Blue: a whole number of lines fits. Red: part of a line is wasted at the bottom of each page; click one fine-tune button. The estimate uses page height, top and bottom margins, line spacing and the font. It does not know about headings, pictures or footnotes.

##### Lines Per Page

Label · Regular+ · `l_linesOnPageLabel`

> This is an approximate calculation of the most number of lines that will fit on a page. An exact count is difficult due to ascent and descent values of the main body font.

Label for the estimate beside it.

##### Tweak line spacing (auto adjust)

Button · Regular+ · `btn_adjust_spacing`  
Greyed out by: “Lock UI Layout Settings”

> Fine Tune Line Spacing:
>
> This button is only active when PTXprint has a suggestion to shrink or expand the line spacing slightly to minimise wasted vertical space on the page. Click to accept the suggestion.
>
> If there is more than half a line of 'spare' space on the page then the line-spacing will decrease slightly to fit one more line of text on the page.
>
> If there is less than half a line of 'spare' space on the page then the line-spacing will increase slightly to fill the page more evenly (with the same number of lines of text).
>
> If you prefer to keep the exact line spacing specified, then do NOT click this option. Instead, use the similar button to adjust either the Top or Bottom Margin.
>
> Note: if Lock Ratio is ticked, the font size will also change slightly.

Only active when **Lines Per Page** is red. To keep the font size exact, untick **Lock Ratio** first or use a margin fine-tune button.

##### Outer Gutter

Checkbox, off · Regular+ · `c_outerGutter` · cfg `paper/ifoutergutter`  
Also: Place gutter on outer edge of page · Needs: “Binding Gutter (mm)” · Greyed out by: “Lock UI Layout Settings”

> An Outer Gutter can be used to create additional whitespace (for notes etc.) on the OUTER edge of each page as commonly seen in a journaling layout.

You still need a normal side margin for the spine.

##### Lock Ratio

Checkbox, on · Regular+ · `c_lockFontSize2Baseline` · cfg `paper/lockfont2baseline`  
Also: Lock ratio of font size to line spacing · Greyed out by: “Lock UI Layout Settings”

> Lock the ratio of the Base Font Size to the Base Line Spacing so that the spacing grows/shrinks according to the size of the font; or the font size changes when the spacing changes.

When you tick it again, the current ratio is kept. While ticked, the line-spacing fine-tune button also changes the font size.

##### Align Text to Baseline – Align Text to Baseline Grid (On-Grid/Off-Grid)

Switch · Basic+ · `c_noGrid` · cfg `document/nogrid`

> For high quality typesetting it is best practice to Align the Text to the (baseline) Grid. This ensures consistent line spacing and front-to-back registration.
>
> However, for quick draft printouts or typesetting for thicker paper, Variable Line Spacing mode enables vertical justification which fills each column of text as needed to use up the entire page.
>
> Warning: This is a major 'mode' change. Everything will shift as a result. Consider carefully before changing this setting.
>
> For high quality typesetting it is best practice to Align the Text to the Baseline (i.e. on grid). This ensures consistent line spacing and front-to-back registration.
>
> Note that this may leave larger empty spaces at the end of pages which will need to be manually adjusted using the Adjust List.

Left (**Align Text to Baseline**): every line on a fixed grid; best for final Bibles on thin paper. Right (**Variable Line Spacing**): line spacing stretches to fill columns; best for drafts and thick paper. Switching right also ticks **Fill Columns** and **Allow Unbalanced Columns**.

##### Fill Columns

Checkbox, off · Basic+ · `c_variableLineSpacing` · cfg `document/varlinespacing`  
Also: Variable/Increased Line Spacing · Needs: “noGrid”

> A small increase in the (vertical) line spacing allows the text to stretch to fill the entire column.
>
> This is called vertical justification and is useful for Draft Printouts where the page can be filled without manual intervention to eliminate unwanted gaps at the end of columns. The setting 'Allow Unbalanced Columns' automatically gets enabled when you choose this setting.
>
> Allowing a small increase in the (vertical) line spacing allows the text to stretch vertically to fill the entire column.
>
> This will also enable 'Fill Columns', but you can turn that off to see how much extra space there is at the end of each column.
>
> Warning: This will cause major changes to the layout of the entire document. It will also place headings exactly rather than rounding to the nearest number of lines.
>
> Do NOT use this setting if doing final typesetting for thin Bible paper as front-to-back registration is not enforced with Variable Line Spacing.

Ticked automatically when you move the switch to **Variable Line Spacing**. The stretch allowed is set on the **Advanced** tab, **Other** tab, **Page Layout and Spacing**.

##### Notelines

Checkbox, off · Regular+ · `c_noteLines` · cfg `paper/notelines`, `paper/ifnotelines_`

> Include ruled margins to provide space for personal notes, reflections, and artwork. Typically called 'Journaling Bibles' or 'Wide-Margin Bibles'.
>
> Hint: Set the Binding Gutter to a larger value (>40mm) and enable Outer Gutter. Other settings to control the appearance and spacing of the Notelines are in the 'Page Layout and Spacing' section of the Advanced > Other tab.

Ticking it also ticks **Binding Gutter** and **Outer Gutter**, and sets the gutter to 40 mm if it was under 30 mm. A colour button appears beside it.

##### Set the color of the Notelines.

Colour · not shown · `col_noteLines` · cfg `paper/majornlcolor`

> Set the color of the Notelines.

Shown only when **Notelines** is ticked. A light grey or light colour does not distract from the text.

##### Mirror Pages

Checkbox, on · Basic+ · `c_mirrorpages` · cfg `header/mirrorlayout`  
Also: Mirror page layout · Greyed out by: “Lock UI Layout Settings”

> Mirror Pages makes use of an Inner+Outer layout. This will make the left page header the inner header and the right page header will be shown on the outer edge (i.e. headers on odd and even pages are mirrored).
>
> Behaviour for Diglots:  
> Note that when creating a Diglot, this will place the primary text as the Inner text (closest to the spine), and the secondary text as the Outer text (closest to the edge of the page).
>
> If you always want the Primary text on the left and Secondary text on the right regardless of whether it is an odd or even page, then turn off this option.

For example, the page number stays on the outer edge of both left and right pages.

##### Margin Notes Col Width (mm)

Checkbox, off · Regular+ · `c_useMarginNotes` · cfg `paper/ifmarginnotes`, `document/marginnotes`  
Also: Place Footnotes, Cross-references and Headings in Margin

> Enabling this will allow Notes (footnotes and/or cross-references) and optionally Headings (and their corresponding Parallel Passage references) to be place in a wider margin area in a way that makes them easier to access by the reader.

This only makes the space. For footnotes or cross-references, choose **Side Margin** on the **Notes+Refs** tab. For headings, tick **In Margin** on the **Body** tab.

##### Margin Notes Column Width

Number · Regular+ · `s_marginNotesWidth` · cfg `paper/marginnoteswidth`, `document/marginnoteswidth`  
Needs: “Margin Notes Col Width (mm)”

> This is the width (mm) of the additional column which contains the Margin Notes (Footnotes, Cross-references and/or Section Headings).

Make it wide enough for a few short words per line. The main text becomes narrower by this amount.

##### Margin Notes on Left/Inner

Checkbox, off · Regular+ · `c_marginNotesInner` · cfg `document/marginnotesinner`  
Also: Place Margin Notes on Left/Inner edge of page · Needs: “Margin Notes Col Width (mm)”

> Margin Notes are normally placed on the Right/Outer edge of the page. But this can be changed for single column layouts to appear on the Left/Inner edge if needed. (Not available for two-column layouts.)

PTXprint unticks it when you switch to two columns.

#### Two Column Layout

##### Gutter Width (mm) – Gutter width for two column layout

Number · Basic+ · `s_colgutterfactor` · cfg `document/colgutterfactor`  
Values: 1–40 (default 4) · Needs: “Two Column Layout” · Greyed out by: “Lock UI Layout Settings”

> This is the space between the text of the two columns (measured in millimeters).
>
> This is the space (mm) between the text of the two columns.

A **Vertical Rule in Gutter** is drawn in the middle of this space. 3–6 mm is common.

##### Adjust Top (pt) – Adjust top of vertical rule

Number · Regular+ · `s_colgutteroffset` · cfg `paper/colgutteroffset`  
Values: -50–50 (default 3)

> This setting raises (using a negative value) or lowers (using a positive value) the starting point of the vertical rule between columns. (Value in pts).

Use it if the line starts too close to the header rule or too far from the first line of text. Greyed out unless **Two Column Layout** and **Vertical Rule in Gutter** are both ticked.

##### Thickness of Rule (pt) – Rule (line) Thickness

Number · Regular+ · `s_ruleThickness` · cfg `document/rulethickness`  
Values: 0.01–1 (default 0.4)

> This sets the thickness (pt) of rules (lines) in the document. This includes the horizontal rule between the header and the text, the vertical column gutter rule and the study notes inter-column rule.

Stays available in a one-column layout, because it also sets the header rule.

##### Vertical Rule in Gutter

Checkbox, on · Mini+ · `c_verticalrule` · cfg `paper/ifverticalrule`  
Needs: “Two Column Layout”

> Check this option to include a center line between the two columns.

Many Bibles use it.

##### Allow Unbalanced Columns

Checkbox, off · Basic+ · `c_allowUnbalanced` · cfg `paper/allowunbalanced`  
Needs: “Two Column Layout”

> Check this option to allow a different number of lines in each column. This is especially important when using Variable Line Spacing mode and you are trying to Fill Columns.
>
> To alter the maximum number of Unbalanced Lines at the end of a page, visit the Advanced page, select the Other tab, and expand the Page Layout and Spacing section.
>
> If this setting is highlighted in orange it means that the above-mentioned setting was set to 0 (rendering this setting inactive), and has now been increased to the default value of 3.

Very useful with **Variable Line Spacing**. The maximum difference is **Unbalanced Lines (Max)** on the **Advanced** tab, **Other** tab, **Page Layout and Spacing**.

#### Margins

##### Bottom of Header to Top of Text (pt) – Header spacing

Number · Regular+ · `s_headerposition` · cfg `paper/headerpos`  
Values: -20–99 (default 15) · Greyed out by: “Lock UI Layout Settings”

> This setting determines the vertical positioning of the header line by setting the amount of space between the header and the top of the text. (pts)
>
> The top of the main text area is 1 base line spacing above the base line of the first line of the body text.
>
> The space (pt) between the bottom of the header and the top of the main text area. Note that the first line actually starts a little bit below where the main text area starts.
>
> The top of the main text area is 1 base line spacing above the base line of the first line of the body text.

The header sits inside the top margin, so a bigger value moves it up towards the page edge. Watch the blue number in the diagram.

##### Bottom of Text to Top of Footer (pt) – Footer position

Number · Regular+ · `s_footerposition` · cfg `paper/footerpos`  
Greyed out by: “Lock UI Layout Settings”

> This setting can be used to increase/decrease the space between the end of the text and the footer line.
>
> The distance (pt) from the bottom of the text area to the TOP of the footer (including ascenders).

The footer normally sits inside the bottom margin, so a bigger value moves it down towards the page edge. Watch the blue number in the diagram.

##### Bottom of Text to End of Page (mm) – Bottom margin

Number · Basic+ · `s_bottommargin` · cfg `paper/bottommargin`  
Values: 0.5–99 (default 10.5) · Greyed out by: “Lock UI Layout Settings”

> The distance (mm) from the bottom of the main text area to the bottom of the page.
>
> The bottom of the main text area is calculated from the descender of the final line of text (including any footnotes).

The footer sits in this space (unless **Place Footer Text Above the Bottom Margin** is ticked). Changing it changes **Lines Per Page**.

##### Side Margin Width (mm) – Side margin width

Number · Basic+ · `s_margins` · cfg `paper/margins`  
Values: 0.5–200 (default 12) · Greyed out by: “Lock UI Layout Settings”

> The distance (mm) from the edge of the page to the start of the text area. Note that the left and right (or inner and outer) margins are set to be identical. If you require a greater inner margin, then set the Binding Gutter above.

10–15 mm is common.

##### Space between Rule and Top of Text (pt) – Space between horizontal rule and main text area

Number · Basic+ · `s_rhruleposition` · cfg `paper/rulegap`  
Values: -100–100 · Needs: “Horizontal Rule” · Greyed out by: “Lock UI Layout Settings”

> The space (pt) between the horizontal rule and the top of the main text area. Note that the first line actually starts a little bit below where the main text area starts.
>
> The top of the main text area is 1 base line spacing above the base line of the first line of the body text.

Shown by the green arrow in the margin diagram.

##### Start of Page to Top of Text (mm) – Top margin

Number · Basic+ · `s_topmargin` · cfg `paper/topmargin`  
Values: 0.5–200 (default 18) · Greyed out by: “Lock UI Layout Settings”

> The distance (mm) from the top of the page to the top of the main text area. Note that the first line actually starts a little bit below where the main text area starts.
>
> The top of the main text area is 1 base line spacing above the base line of the first line of the body text.

The header sits in this space. Changing it changes **Lines Per Page**.

##### Tweak top margin (auto adjust)

Button · Regular+ · `btn_adjust_top`  
Greyed out by: “Lock UI Layout Settings”

> Fine Tune Top Margin:
>
> This button is only active when PTXprint has a suggestion to shrink or expand the top margin slightly to minimise wasted vertical space on the page. Click to accept the suggestion.
>
> If there is more than half a line of 'spare' space on the page then the top margin will decrease slightly to fit one more line of text on the page.
>
> If there is less than half a line of 'spare' space on the page then the top margin will increase slightly to fill the page more evenly (with the same number of lines of text).
>
> If you prefer to keep the exact top margin specified, then do NOT click this option. Instead, use the similar button to adjust either the Line Spacing or Bottom Margin.

Only active when **Lines Per Page** is red. Use it to keep line spacing and font size exactly as they are.

##### Tweak bottom margin (auto adjust)

Button · Regular+ · `btn_adjust_bottom`  
Greyed out by: “Lock UI Layout Settings”

> Fine Tune Bottom Margin:
>
> This button is only active when PTXprint has a suggestion to shrink or expand the bottom margin slightly to minimise wasted vertical space on the page. Click to accept the suggestion.
>
> If there is more than half a line of 'spare' space on the page then the bottom margin will decrease slightly to fit one more line of text on the page.
>
> If there is less than half a line of 'spare' space on the page then the bottom margin will increase slightly to fill the page more evenly (with the same number of lines of text).
>
> If you prefer to keep the exact bottom margin specified, then do NOT click this option. Instead, use the similar button to adjust either the Line Spacing or Top Margin.

Only active when **Lines Per Page** is red. Use it to keep line spacing, font size and top margin exactly as they are.

##### Place Footer Text Above the Bottom Margin

Checkbox, off · Regular+ · `c_noinkinmargin` · cfg `footer/noinkinmargin`  
Also: Don't place footer in the margin area · Greyed out by: “Lock UI Layout Settings”

> Normally the footer page number sits in the bottom margin.
>
> However if you need the page number to be placed above the bottom margin (where the text would normally flow until) then enable this option.

Use it when the printer needs the whole margin empty. The text area becomes a little shorter.

##### 8.5mm

Label · Regular+ · `l_footer2edge`  
Greyed out by: “Lock UI Layout Settings”

> The distance (mm) from the edge of the page to the bottom of the footer area.

Calculated; you cannot type in it. Shown by the blue arrow at the bottom of the diagram. If it is very small, the footer may be cut off when the pages are trimmed.

##### Horizontal Rule

Checkbox, off · Basic+ · `c_rhrule` · cfg `header/ifrhrule`  
Greyed out by: “Lock UI Layout Settings”

> Check this option to add a horizontal line under the page header, before the main body text begins.

Set its position with **Space between Rule and Top of Text (pt)** and its thickness with **Thickness of Rule (pt)**.

##### 8.5mm

Label · Regular+ · `l_margin2header`  
Greyed out by: “Lock UI Layout Settings”

> The distance (mm) from the top of the page to the top of the header area. Note that due to the ascent of the font, the header text actually starts a little bit below the top of the header area.

Calculated; you cannot type in it. Shown by the blue arrow at the top of the diagram. If it is very small or negative, make the top margin larger or the header gap smaller.
