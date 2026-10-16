# Layout tab

## What this tab is for

The **Layout** tab sets the shape of every page. Here you choose the page size, the margins (the empty space around the text), one or two columns, the size of the main text and the space between lines.

Come here when you start a new publication, when the printer tells you the page size, or when the text does not fit the number of pages you want. Most settings on this tab change the whole book. After you change them, click **Print** again to see the new result.

Some words used in this chapter:

* **pt (point)** – a small unit used for type. 1 pt is about 0.35 mm. 72 pt is about one inch (25.4 mm).
* **Baseline** – the invisible line that the letters sit on.
* **Line spacing** – the distance from the baseline of one line to the baseline of the next line.
* **Gutter** – an extra empty space. A *binding gutter* is extra space at the spine of the book. A *column gutter* is the space between two columns of text.
* **Text area** – the part of the page where the main text goes. The margins are outside it.

## Page Setup

This area holds the most important settings: **Page Size**, **Base Font Size (pt)**, **Base Line Spacing (pt)**, **Base Indent**, the binding gutter and the page-layout options.

### Page size

Choose a size from the **Page Size** list, or type your own. Type the width first, then a comma, then the height, for example `148mm, 210mm`. You can use `mm`, `cm` or `in`. Ask your printer for the exact trim size (the size of the finished, cut page) before you start, because changing the page size later moves every line.

### Font size and line spacing (and how they work together)

Two numbers control how big the text is and how close the lines are:

* **Base Font Size (pt)** is the size of the letters in normal paragraphs. All other text (headings, footnotes, verse numbers and so on) is sized *relative to* this number. So if you make the base font bigger, the headings and footnotes also grow by the same proportion.
* **Base Line Spacing (pt)** is the distance from one line to the next. It is normally bigger than the font size, so that the lines do not touch. For example, 11 pt text with 14 pt line spacing is a common choice.

The **Lock Ratio** box (ticked by default) joins these two numbers together:

* When **Lock Ratio** is ticked and you change the font size, PTXprint changes the line spacing by the same proportion. For example, if you have 11 pt text on 14 pt spacing and you change the font to 12 pt, the line spacing becomes about 15.3 pt. The page keeps the same "look", only bigger.
* It also works the other way round. If you change the line spacing, PTXprint changes the font size.
* When **Lock Ratio** is not ticked, you can change each number on its own. Use this when you want more (or less) space between the lines but the same size letters.
* When you tick **Lock Ratio** again, PTXprint remembers the ratio between the two numbers *as they are now*.

The line spacing decides how many lines fit on a page. PTXprint shows an estimate next to **Lines Per Page**.

### Lines Per Page and the fine-tune buttons

The **Lines Per Page** number is calculated from the page height, the top and bottom margins and the line spacing. It is updated when you change any of these.

* If the number is **blue**, a whole number of lines fits the text area. There is no wasted space.
* If the number is **red**, the text area holds a whole number of lines plus a part of a line. That part of a line is empty space at the bottom of each page.

When the number is red, three small "fine-tune" buttons (with an icon of justified lines) become active. One is next to **Base Line Spacing (pt)**. The other two are next to the top and bottom margin settings in the **Margins** area. Each button makes a small change so that a whole number of lines fits:

* If more than half a line is spare, the change makes room for one more line.
* If less than half a line is spare, the change spreads the same number of lines a little further apart (or makes the margin a little larger).

Click only **one** of the three buttons. Choose the setting you are most willing to change: the line spacing, the top margin, or the bottom margin. The number then turns blue and the buttons become grey again.

Be careful: if **Lock Ratio** is ticked, the line-spacing fine-tune button also changes the font size a little. If you want to keep the font size exactly, untick **Lock Ratio** first, or use one of the margin buttons instead.

### Binding gutter, Outer Gutter and Mirror Pages

* **Binding Gutter (mm)** adds extra space to the inner edge of each page (the edge near the spine). This is added to the **Side Margin Width**. Thick books need more, because the pages curve into the spine. The gutter changes sides on odd and even pages, so it is always at the spine.
* **Outer Gutter** moves that extra space to the outer edge instead. This is used for journaling or wide-margin Bibles, where readers write notes in the outer margin.
* **Mirror Pages** makes odd and even pages mirror each other. The header items that are on the left of a right-hand page appear on the right of a left-hand page, so they stay on the outer (or inner) edge. In a diglot (two-language) layout it also keeps the primary text on the inner side, near the spine.

Whether the gutter swaps sides on odd and even pages is controlled by **Double Sided Layout**, on the **Advanced** tab, **Other** tab, in **Page Layout and Spacing**. It is normally on.

### Align Text to Baseline / Variable Line Spacing

This is a switch with **Align Text to Baseline** on the left and **Variable Line Spacing** on the right.

* **Align Text to Baseline** (the switch to the left, the normal setting) puts every line on a fixed grid. Lines on the front and back of a sheet line up exactly. This is important for thin Bible paper, where the text on the other side can show through. The cost is that some columns may end with an empty line or two. You fix these by hand with the page-filling tools in the PDF Preview.
* **Variable Line Spacing** (the switch to the right) lets PTXprint stretch the space between lines a little so that every column is filled to the bottom. This is good for quick drafts and for thicker paper. Front-to-back alignment is lost, and the whole book will re-flow when you change it.

When you switch to **Variable Line Spacing**, PTXprint also ticks **Fill Columns** and **Allow Unbalanced Columns** for you. How much the lines may stretch or shrink is set on the **Advanced** tab, **Other** tab, in **Page Layout and Spacing**.

### Notelines (journaling layout)

**Notelines** prints ruled lines in a wide margin, so readers can write their own notes. When you tick it, PTXprint also ticks **Binding Gutter** and **Outer Gutter**, and sets the gutter to 40 mm if it was smaller than 30 mm. A colour button appears so you can choose the colour of the lines. More noteline settings (spacing, offset, type) are on the **Advanced** tab, **Other** tab, in **Page Layout and Spacing**.

### Margin Notes

**Margin Notes Col Width (mm)** creates an extra column at the side of the text. Footnotes, cross-references and (if you choose) section headings can be placed in this column, beside the verse they belong to. Ticking it here only creates the space. To put notes there, choose **Side Margin** as the position on the **Notes+Refs** tab. To put headings there, tick **In Margin** on the **Body** tab.

These settings are shown in the **Default** and **Full** views.

## Two Column Layout

Tick **Two Column Layout** to set the main text in two columns. Untick it for one column. When you change this, PTXprint halves (for two columns) or doubles (for one column) the **Base Indent** for you, because a narrow column needs a smaller indent.

The settings in the **Two Column Layout** area only work when there are two columns:

* **Gutter Width (mm)** – the space between the two columns. 4 mm is a common value.
* **Vertical Rule in Gutter** – draws a thin line down the middle of the gutter.
* **Adjust Top (pt)** – moves the top of that line up (negative number) or down (positive number).
* **Thickness of Rule (pt)** – how thick the lines are.
* **Allow Unbalanced Columns** – lets the two columns on a page end at different heights, by up to a set number of lines.

If you make a diglot (two languages side by side), PTXprint needs the two-column layout, so the **Two Column Layout** box is greyed out.

## Margins

The **Margins** area sets the empty space around the text, and the position of the header (the line at the top of the page, often with the book name and page number) and the footer (the line at the bottom).

### The margin diagram and its colours

Next to the margin settings there is a small picture of a page. It shows one or two columns, the vertical rule, and the horizontal rule under the header, as you have set them. Coloured arrows show what each number measures:

* **Orange** – **Side Margin Width (mm)**: from the edge of the page to the text.
* **Red** (top) – **Start of Page to Top of Text (mm)**: the top margin.
* **Red** (bottom) – **Bottom of Text to End of Page (mm)**: the bottom margin.
* **Purple** (top) – **Bottom of Header to Top of Text (pt)**: the gap between the header and the text.
* **Purple** (bottom) – **Bottom of Text to Top of Footer (pt)**: the gap between the text and the footer.
* **Green** – **Space between Rule and Top of Text (pt)**: the gap between the horizontal rule and the text.
* **Blue** – two numbers that PTXprint calculates for you (you cannot type in them): the distance from the top of the page to the header, and from the footer to the bottom of the page.

When you move the mouse over one of the margin boxes, the picture shows only the arrow for that box. This helps you see which space you are changing.

Note that the margins are measured in **mm**, but the header and footer gaps are measured in **pt**.

### Header and footer position

The header sits *inside* the top margin, and the footer normally sits *inside* the bottom margin. So if you make the header gap bigger, the header moves up towards the edge of the page. Watch the blue numbers: if one becomes very small (or negative), the header or footer is too close to the edge of the page and may be cut off when the book is trimmed.

Tick **Place Footer Text Above the Bottom Margin** if you want the footer inside the text area instead of in the margin.

Tick **Horizontal Rule** to draw a line under the header. Then use **Space between Rule and Top of Text (pt)** to set its position.

To see the margins, header and footer areas on the page, tick **Guides and Baselines** on the **Content** tab of the **PDF Preview** window.

## Change the Grid Settings dialog (graph paper)

PTXprint can show a "graph paper" grid over the pages in the **PDF Preview**. This helps you measure things on the page, for example to check a margin or the size of a picture.

To turn it on, open the **PDF Preview**, go to its **Content** tab and tick **Graph Paper**. To change how it looks, click **Settings** next to it. This opens the **Change the Grid Settings** dialog. There you can choose:

* **Major Units** – centimetres or inches between the thicker (major) lines, plus the colour and thickness of those lines.
* **Minor Divisions** – how many thinner lines there are between two major lines, plus their colour and thickness. For centimetres, 2, 5 or 10 work well. For inches, 3, 4, 6 or 12 work well.
* **Place Grid** – draw the grid over the **Whole Page**, only **In Margin Areas**, or **Only in Text Area**.

Click **OK** to apply the settings. The preview is redrawn with the new grid (if **Graph Paper** is ticked).

## Lock UI Layout Settings

When the typesetting is almost finished, you can protect the layout from accidental changes. On the **Advanced** tab, **Main** tab, in the **General** area, tick **Lock UI Layout Settings**. (This is only shown in the **Full** view.)

While it is ticked, most of the **Layout** tab is greyed out (page size, font size, line spacing, columns, gutter, margins and more). The whole **Fonts+Script** tab and the **Styles** tab are also greyed out. Untick it to make changes again.

## Common tasks

### How do I change the page size?

1. On the **Layout** tab, in the **Page Setup** area, click the **Page Size** list.
2. Choose a size, for example **148mm, 210mm (A5)**.
3. Or type your own size: width, comma, height. For example `140mm, 216mm`.
4. Check the **Lines Per Page** number. If it is red, use one fine-tune button (see the next task).
5. Click **Print** to see the result.

### How do I stop wasting space at the bottom of every page?

1. On the **Layout** tab, look at the **Lines Per Page** number. (This is shown in the **Default** and **Full** views.)
2. If it is red, decide which setting you are most willing to change: the line spacing, the top margin or the bottom margin.
3. Click the fine-tune button next to that setting (next to **Base Line Spacing (pt)**, or in the **Margins** area next to the top or bottom margin).
4. The number turns blue.
5. Click **Print**.

### How do I make the text bigger or smaller without changing the look of the page?

1. On the **Layout** tab, make sure **Lock Ratio** is ticked.
2. Change **Base Font Size (pt)**. The line spacing changes with it.
3. If **Lines Per Page** is red, click one fine-tune button.
4. Click **Print**.

### How do I put more space between the lines but keep the same letter size?

1. On the **Layout** tab, untick **Lock Ratio**.
2. Make **Base Line Spacing (pt)** larger, for example from 14 to 15.
3. Tick **Lock Ratio** again if you want the new ratio to be kept.
4. Click **Print**.

### How do I change between one and two columns?

1. On the **Layout** tab, tick or untick **Two Column Layout**.
2. If you chose two columns, set **Gutter Width (mm)** and decide whether you want a **Vertical Rule in Gutter**.
3. Check **Base Indent**. PTXprint changes it automatically, but you may want to adjust it.
4. Click **Print**.

### How do I add extra space at the spine for binding?

1. On the **Layout** tab, in the **Page Setup** area, tick **Binding Gutter (mm)**.
2. Type the extra space in the box beside it, for example 5 mm. Ask your printer how much is needed for the thickness of your book.
3. Leave **Outer Gutter** unticked.
4. Click **Print**.

### How do I make a journaling (wide-margin) Bible?

1. On the **Layout** tab, tick **Notelines**. (This is shown in the **Default** and **Full** views.)
2. PTXprint ticks **Binding Gutter** and **Outer Gutter** and sets a wide gutter (at least 40 mm).
3. Change the gutter width if needed, and choose the line colour with the colour button.
4. Click **Print**.

### How do I put footnotes and cross-references in the side margin?

1. On the **Layout** tab, tick **Margin Notes Col Width (mm)** and type the width of the margin column.
2. On the **Notes+Refs** tab, set the position of footnotes and/or cross-references to **Side Margin**.
3. If you also want section headings in the margin, tick **In Margin** on the **Body** tab.
4. Click **Print**.

### How do I see a measuring grid on the page?

1. Click **Print** so that the **PDF Preview** opens.
2. On the **Content** tab of the preview, tick **Graph Paper**.
3. Click **Settings** next to it to change units, colours and where the grid is drawn.
4. Click **OK**.

## Common problems

### Almost everything on the Layout tab is greyed out

**Cause:** **Lock UI Layout Settings** is ticked. This also greys out the whole **Fonts+Script** tab and the **Styles** tab.

**What to do:** Change the view level to **Full**. On the **Advanced** tab, **Main** tab, **General** area, untick **Lock UI Layout Settings**.

### I changed the font size and the line spacing changed too (or the other way round)

**Cause:** **Lock Ratio** is ticked. This is the normal setting.

**What to do:** Untick **Lock Ratio** before you change one of the two numbers on its own.

### I clicked the line-spacing fine-tune button and my font size changed

**Cause:** **Lock Ratio** is ticked, so the font size follows the line spacing.

**What to do:** Untick **Lock Ratio** and type your font size again. Then use the fine-tune button again, or use the top or bottom margin fine-tune button instead.

### The fine-tune buttons are greyed out

**Cause:** The **Lines Per Page** number is already a whole number (blue). There is nothing to fix. The buttons are also greyed out when **Lock UI Layout Settings** is ticked.

### The fine-tune buttons and Lines Per Page are not visible

**Cause:** They are only shown in the **Default** and **Full** views.

**What to do:** Change the view level from the main menu.

### I cannot untick Two Column Layout

**Cause:** A diglot (two languages) is set up. A diglot needs two columns.

### The Base Indent changed by itself

**Cause:** When you switch between one and two columns, PTXprint halves or doubles the indent.

**What to do:** Type the indent you want after you change the number of columns.

### "Margin Notes on Left/Inner" is greyed out

**Cause:** It only works with one column. It is also greyed out until **Margin Notes Col Width (mm)** is ticked.

### Margin notes do not appear even though I ticked Margin Notes

**Cause:** The Layout tab setting only makes the space. You must also send the notes there.

**What to do:** On the **Notes+Refs** tab, choose **Side Margin** for footnotes and/or cross-references.

### The header or footer is too close to the edge of the page

**Cause:** The header gap or footer gap is large compared with the top or bottom margin. The header and footer sit inside the margins.

**What to do:** Look at the blue numbers in the margin diagram. Make the top (or bottom) margin larger, or make **Bottom of Header to Top of Text (pt)** (or **Bottom of Text to Top of Footer (pt)**) smaller.

### Columns end at different heights, or there are gaps at the bottom of columns

**Cause:** With **Align Text to Baseline**, lines sit on a fixed grid, so some columns can end early.

**What to do:** For a draft, move the switch to **Variable Line Spacing**. For a final Bible on thin paper, keep **Align Text to Baseline** and fix the pages with the page-filling tools in the PDF Preview. In two columns, **Allow Unbalanced Columns** also lets the columns end at different heights.

### The binding gutter is always on the same side of the page

**Cause:** **Double Sided Layout** has been turned off on the **Advanced** tab, **Other** tab, **Page Layout and Spacing**. Or **Outer Gutter** is ticked, which moves the gutter to the outside edge.

### The Notelines colour button is missing

**Cause:** It is only shown when **Notelines** is ticked.

## Settings reference: Layout tab

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Change the Grid Settings (dialog)

#### OK

- **Where:** Change the Grid Settings (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog and redraws the PDF Preview with the new grid settings (the grid is shown if **Graph Paper** is ticked).

*(Internal ID: `btn_guides_ok`)*

#### Cancel

- **Where:** Change the Grid Settings (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog. The grid in the preview is not redrawn.

*(Internal ID: `btn_guides_cancel`)*

### Change the Grid Settings (dialog) › Grid Settings

#### Major Units

- **Where:** Change the Grid Settings (dialog) › Grid Settings
- **Type:** Colour picker
- **Description:** Grid: Major line color
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The color of the major (thicker) grid lines.

**Explanation:**

Choose the colour of the thicker (major) grid lines. A strong colour (for example red) makes the major lines easy to count. Ignore the tooltip text about Thumb Tabs; it does not apply here.

*(Internal ID: `col_gridMajor` · Config key: `grid/majorcolor`, `majorcolor_`)*

#### Minor Divisions

- **Where:** Change the Grid Settings (dialog) › Grid Settings
- **Type:** Colour picker
- **Description:** Grid: Minor line color
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The color of the minor (thinner) grid lines between the major lines.

**Explanation:**

Choose the colour of the thinner lines between the major lines. A light colour keeps the text readable under the grid. Ignore the tooltip text about Thumb Tabs; it does not apply here.

*(Internal ID: `col_gridMinor` · Config key: `grid/minorcolor`, `minorcolor_`)*

#### Major Units

- **Where:** Change the Grid Settings (dialog) › Grid Settings
- **Type:** Number box
- **Description:** Grid: Major line thickness
- **View level:** Default and Full views
- **Values:** default 0.2

**Tooltip (the text shown when you hover the mouse over it):**

> Specify the thickness of the major lines.

**Explanation:**

How thick (in pt) the major grid lines are. Small values such as 0.2 are usually enough.

*(Internal ID: `s_gridMajorThick` · Config key: `grid/majorthickness`)*

#### Minor Divisions

- **Where:** Change the Grid Settings (dialog) › Grid Settings
- **Type:** Number box
- **Description:** Grid: Minor line thickness
- **View level:** Default and Full views
- **Values:** default 0.1

**Tooltip (the text shown when you hover the mouse over it):**

> Specify the line thickness of the minor divisions.

**Explanation:**

How thick (in pt) the minor grid lines are. Keep it at or below the major thickness so the two kinds of line look different.

*(Internal ID: `s_gridMinorThick` · Config key: `grid/minorthickness`)*

#### Minor Divisions

- **Where:** Change the Grid Settings (dialog) › Grid Settings
- **Type:** Number box
- **Description:** Grid: Number of minor divisions
- **View level:** Default and Full views
- **Values:** default 12

**Tooltip (the text shown when you hover the mouse over it):**

> Specify the number of minor divisions there should be between the thicker (major) lines. Recommendations: 2, 5, or 10 for centimeters, and 3, 4, 6, or 12 for inches.

**Explanation:**

How many small squares there are between two major lines. With **Centimeters**, 5 gives 2 mm squares and 10 gives 1 mm squares. With **Inches**, 3, 4, 6 or 12 are useful.

*(Internal ID: `s_gridMinorDivisions` · Config key: `grid/divisions`, `grid/xyadvance`)*

#### Place Grid

- **Where:** Change the Grid Settings (dialog) › Grid Settings
- **Type:** Button
- **Description:** Grid: Reload default values
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Clicking this button will refresh the default Grid settings:  
> Centimeters with 5 divisions (2mm each), red major and light blue minor lines (0.2pt thickness), over the whole page.

**Explanation:**

Puts the grid settings back to the defaults: centimetres, 5 divisions, the grid over the whole page, red major lines and light blue minor lines, both 0.2 pt thick.

*(Internal ID: `btn_resetGrid`)*

#### Major Units

- **Where:** Change the Grid Settings (dialog) › Grid Settings
- **Type:** Drop-down list
- **Description:** Grid: Select major units
- **View level:** Default and Full views
- **Choices:** Centimeters; Inches

**Tooltip (the text shown when you hover the mouse over it):**

> The grid can use Centimeters or Inches as the major units.

**Explanation:**

Choose whether the major lines are 1 cm or 1 inch apart. Use the unit your printer or publisher uses for their measurements.

*(Internal ID: `fcb_gridUnits` · Config key: `grid/units`)*

#### Place Grid

- **Where:** Change the Grid Settings (dialog) › Grid Settings
- **Type:** Drop-down list
- **Description:** Grid: Starting position (page or margin)
- **View level:** Default and Full views
- **Choices:** Whole Page; In Margin Areas; Only in Text Area

**Tooltip (the text shown when you hover the mouse over it):**

> The grid can start at the top-left corner of the Page, or at the top-left Margin.
>
> Depending on what you are trying to measure, it can be helpful to position the grid at the top-left corner of the page, or margins.

**Explanation:**

Choose where the grid is drawn. **Whole Page** starts at the top-left corner of the page and is best for measuring margins. **Only in Text Area** starts at the corner of the text and is best for measuring things inside the text, such as pictures. **In Margin Areas** draws the grid only in the margins, so the text stays clear.

*(Internal ID: `fcb_gridOffset` · Config key: `grid/xyoffset`)*

### Layout tab › Page Setup

#### Binding Gutter (mm)

- **Where:** Layout tab › Page Setup
- **Type:** Checkbox (not ticked by default)
- **Description:** Use binding gutter
- **View level:** Basic, Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This is the amount of space to be given on the inner edge of each page for binding (millimeters).
>
> However, if Outer Gutter is enabled this extra space will appear on the outside edge of each page. This can be useful for a journaling layout.

**Explanation:**

Tick this to add extra space at the spine (inner edge) of every page, on top of the side margin. Thick books need more space because the pages curve into the binding. Ask your printer for a value. **Notelines** ticks this for you.

*(Internal ID: `c_pagegutter` · Config key: `paper/ifaddgutter`)*

#### Binding gutter amount

- **Where:** Layout tab › Page Setup
- **Type:** Number box
- **View level:** Basic, Default and Full views
- **Values:** from -200 to 200
- **Only available when:** “Binding Gutter (mm)” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This amount is added to the ‘Side Margin Width’ amount to the inner edge (or outside edge, if you check ‘Outer Gutter’).

**Explanation:**

The amount of extra space (mm) for the binding gutter. It is added to **Side Margin Width (mm)** on the inner edge (or the outer edge if **Outer Gutter** is ticked). For a normal book, a few mm is common. For a journaling layout, 40 mm or more is common. It is greyed out until **Binding Gutter (mm)** is ticked.

*(Internal ID: `s_pagegutter` · Config key: `paper/gutter`)*

#### Base Line Spacing (pt)

- **Where:** Layout tab › Page Setup
- **Type:** Number box
- **Description:** Base line spacing
- **View level:** Basic, Default and Full views
- **Values:** from 4 to 100, default 14
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Base Line spacing in points (pts). Change to increase or decrease space between lines of text.
>
> This is the base line spacing for default paragraph text.

**Explanation:**

The distance (pt) from one line of normal text to the next. A bigger value gives more space between lines and fewer lines per page. If **Lock Ratio** is ticked, changing this also changes **Base Font Size (pt)**. Line spacing for other kinds of paragraph (for example footnotes) is set relative to this in the **Styles** tab.

*(Internal ID: `s_linespacing` · Config key: `paragraph/linespacing`)*

#### Page Size

- **Where:** Layout tab › Page Setup
- **Type:** Drop-down list
- **Description:** Page size setting
- **View level:** All view levels (Mini, Basic, Default, Full)
- **Choices:** 210mm, 297mm (A4); 148mm, 210mm (A5); 105mm, 148mm (A6); 176mm, 250mm (B5); 125mm, 176mm (B6); 210mm, 280mm (PA4); 140mm, 210mm (PA5); 105mm, 140mm (PA6); 8.5in, 11in (Letter); 5.5in, 8.5in (1/2 Letter); 5.25in, 8.25in (133x210mm); 5.8in, 8.7in (147x221mm); 6in, 9in (152x229mm); 184.6mm, 271.6mm (A4 with cropmarks); 165mm, 234mm (KBS max page)
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Type required page width and height,  
>      for example:    148mm, 208mm or select from the list of preset values.

**Explanation:**

The size of the finished (trimmed) page. Choose a preset or type width, comma, height, for example `148mm, 210mm`. You can use mm, cm or in. Get this right before you do detailed page work, because every page will re-flow when it changes.

*(Internal ID: `ecb_pagesize` · Config key: `paper/height`, `paper/width`, `paper/pagesize`)*

#### Base Font Size (pt)

- **Where:** Layout tab › Page Setup
- **Type:** Number box
- **Description:** Base font size
- **View level:** All view levels (Mini, Basic, Default, Full)
- **Values:** from 2 to 36, default 11
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Set the point size of the main body text.
>
> This is the base font size for default paragraph text. All other font sizes are calculated (according to their factor size) based on this value.

**Explanation:**

The size (pt) of the letters in normal paragraphs. Headings, footnotes, verse numbers and other text are sized relative to this, so they all grow or shrink together. Typical values are 9–12 pt for Bibles. If **Lock Ratio** is ticked, changing this also changes **Base Line Spacing (pt)**.

*(Internal ID: `s_fontsize` · Config key: `paper/fontfactor`)*

#### Base Indent

- **Where:** Layout tab › Page Setup
- **Type:** Number box
- **Description:** Base paragraph indent
- **View level:** Default and Full views
- **Values:** default 0.8
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The amount by which paragraphs should be indented (inches). This also affects poetry indentation. (default=1, min=0, max=4)
>
> The space by which paragraphs should be indented (inches). This also affects poetry indentation. Note that for a single-column text this value needs to be higher than for two-column texts, and the value updates automatically when you change from 1 to 2 columns, and vice versa.

**Explanation:**

The basic indent for paragraphs and poetry lines. It is measured in inches (so 0.5 is about 13 mm). Each paragraph style uses a multiple of this value. PTXprint halves it when you switch to two columns and doubles it when you switch to one column.

*(Internal ID: `s_indentUnit` · Config key: `document/indentunit`)*

#### 99.9

- **Where:** Layout tab › Page Setup
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This is an approximate calculation of the most number of lines that will fit on a page. An exact count is difficult due to ascent and descent values of the main body font.

**Explanation:**

The estimated number of lines of normal text that fit in the text area. Blue means a whole number of lines fits. Red means part of a line is wasted at the bottom of each page; use one of the fine-tune buttons to fix it. The estimate uses the page height, top and bottom margins, line spacing and the font. It cannot know about headings, pictures or footnotes.

*(Internal ID: `l_linesOnPage`)*

#### Lines Per Page

- **Where:** Layout tab › Page Setup
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This is an approximate calculation of the most number of lines that will fit on a page. An exact count is difficult due to ascent and descent values of the main body font.

**Explanation:**

The label for the **Lines Per Page** estimate next to it.

*(Internal ID: `l_linesOnPageLabel`)*

#### Tweak line spacing (auto adjust)

- **Where:** Layout tab › Page Setup
- **Type:** Button
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

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

**Explanation:**

Changes **Base Line Spacing (pt)** slightly so that a whole number of lines fits the page. It is only active when **Lines Per Page** is red. If **Lock Ratio** is ticked, the font size changes a little too. If you do not want that, untick **Lock Ratio** first or use a margin fine-tune button.

*(Internal ID: `btn_adjust_spacing`)*

#### Outer Gutter

- **Where:** Layout tab › Page Setup
- **Type:** Checkbox (not ticked by default)
- **Description:** Place gutter on outer edge of page
- **View level:** Default and Full views
- **Only available when:** “Binding Gutter (mm)” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> An Outer Gutter can be used to create additional whitespace (for notes etc.) on the OUTER edge of each page as commonly seen in a journaling layout.

**Explanation:**

Puts the binding-gutter space on the outer edge of each page instead of the spine. Use this for journaling or wide-margin Bibles. You still need a normal side margin for the spine. It is greyed out until **Binding Gutter (mm)** is ticked.

*(Internal ID: `c_outerGutter` · Config key: `paper/ifoutergutter`)*

#### Lock Ratio

- **Where:** Layout tab › Page Setup
- **Type:** Checkbox (ticked by default)
- **Description:** Lock ratio of font size to line spacing
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Lock the ratio of the Base Font Size to the Base Line Spacing so that the spacing grows/shrinks according to the size of the font; or the font size changes when the spacing changes.

**Explanation:**

When ticked, **Base Font Size (pt)** and **Base Line Spacing (pt)** keep the same ratio: change one and PTXprint changes the other. When unticked, you can change each one on its own. When you tick it again, the current ratio is the one that is kept. It also affects the line-spacing fine-tune button.

*(Internal ID: `c_lockFontSize2Baseline` · Config key: `paper/lockfont2baseline`)*

#### Align Text to Baseline

- **Where:** Layout tab › Page Setup
- **Type:** Switch
- **Description:** Align Text to Baseline Grid (On-Grid/Off-Grid)
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> For high quality typesetting it is best practice to Align the Text to the (baseline) Grid. This ensures consistent line spacing and front-to-back registration.
>
> However, for quick draft printouts or typesetting for thicker paper, Variable Line Spacing mode enables vertical justification which fills each column of text as needed to use up the entire page.
>
> Warning: This is a major 'mode' change. Everything will shift as a result. Consider carefully before changing this setting.
>
> For high quality typesetting it is best practice to Align the Text to the Baseline (i.e. on grid). This ensures consistent line spacing and front-to-back registration.
>
> Note that this may leave larger empty spaces at the end of pages which will need to be manually adjusted using the Adjust List.

**Explanation:**

This switch chooses between two layout modes. To the left (**Align Text to Baseline**), every line sits on a fixed grid: best for final Bibles on thin paper. To the right (**Variable Line Spacing**), the space between lines can stretch so that columns are filled: best for drafts and thick paper. Changing this re-flows the whole book. Switching to the right also ticks **Fill Columns** and **Allow Unbalanced Columns**.

*(Internal ID: `c_noGrid` · Config key: `document/nogrid`)*

#### Fill Columns

- **Where:** Layout tab › Page Setup
- **Type:** Checkbox (not ticked by default)
- **Description:** Variable/Increased Line Spacing
- **View level:** Basic, Default and Full views
- **Only available when:** “noGrid” is selected

**Tooltip (the text shown when you hover the mouse over it):**

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

**Explanation:**

Lets PTXprint stretch the line spacing a little so that each column reaches the bottom of the page. It is only available when the switch is on **Variable Line Spacing**, and it is ticked automatically when you move the switch there. Untick it to see how much empty space would be left at the bottom of each column. The amount of stretch allowed is set on the **Advanced** tab, **Other** tab, **Page Layout and Spacing**.

*(Internal ID: `c_variableLineSpacing` · Config key: `document/varlinespacing`)*

#### Notelines

- **Where:** Layout tab › Page Setup
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Include ruled margins to provide space for personal notes, reflections, and artwork. Typically called 'Journaling Bibles' or 'Wide-Margin Bibles'.
>
> Hint: Set the Binding Gutter to a larger value (>40mm) and enable Outer Gutter. Other settings to control the appearance and spacing of the Notelines are in the 'Page Layout and Spacing' section of the Advanced > Other tab.

**Explanation:**

Prints ruled lines in a wide margin for readers' notes (a journaling Bible). Ticking it also ticks **Binding Gutter** and **Outer Gutter** and sets the gutter to 40 mm if it was less than 30 mm. A colour button appears beside it. More noteline settings are on the **Advanced** tab, **Other** tab, **Page Layout and Spacing**.

*(Internal ID: `c_noteLines` · Config key: `paper/notelines`, `paper/ifnotelines_`)*

#### Set the color of the Notelines.

- **Where:** Layout tab › Page Setup
- **Type:** Colour picker
- **View level:** Not normally shown

**Tooltip (the text shown when you hover the mouse over it):**

> Set the color of the Notelines.

**Explanation:**

The colour of the notelines. This button is only shown when **Notelines** is ticked. A light grey or a light colour is usual, so the lines do not distract from the text.

*(Internal ID: `col_noteLines` · Config key: `paper/majornlcolor`, `majornlcolor_`)*

#### Mirror Pages

- **Where:** Layout tab › Page Setup
- **Type:** Checkbox (ticked by default)
- **Description:** Mirror page layout
- **View level:** Basic, Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Mirror Pages makes use of an Inner+Outer layout. This will make the left page header the inner header and the right page header will be shown on the outer edge (i.e. headers on odd and even pages are mirrored).
>
> Behaviour for Diglots:  
> Note that when creating a Diglot, this will place the primary text as the Inner text (closest to the spine), and the secondary text as the Outer text (closest to the edge of the page).
>
> If you always want the Primary text on the left and Secondary text on the right regardless of whether it is an odd or even page, then turn off this option.

**Explanation:**

Makes left and right pages mirror each other. With it ticked, the header items you set for a right-hand page are swapped to the other side on a left-hand page, so (for example) the page number is always on the outer edge. In a diglot, it keeps the primary text on the inner side, near the spine. Untick it if you want the primary text always on the left.

*(Internal ID: `c_mirrorpages` · Config key: `header/mirrorlayout`)*

#### Margin Notes Col Width (mm)

- **Where:** Layout tab › Page Setup
- **Type:** Checkbox (not ticked by default)
- **Description:** Place Footnotes, Cross-references and Headings in Margin
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Enabling this will allow Notes (footnotes and/or cross-references) and optionally Headings (and their corresponding Parallel Passage references) to be place in a wider margin area in a way that makes them easier to access by the reader.

**Explanation:**

Creates an extra column at the side of the text for notes and, if you choose, section headings. This only makes the space. To place footnotes or cross-references there, choose **Side Margin** on the **Notes+Refs** tab. To place headings there, tick **In Margin** on the **Body** tab.

*(Internal ID: `c_useMarginNotes` · Config key: `paper/ifmarginnotes`, `document/marginnotes`)*

#### Margin Notes Column Width

- **Where:** Layout tab › Page Setup
- **Type:** Number box
- **View level:** Default and Full views
- **Only available when:** “Margin Notes Col Width (mm)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This is the width (mm) of the additional column which contains the Margin Notes (Footnotes, Cross-references and/or Section Headings).

**Explanation:**

The width (mm) of the margin-notes column. It must be wide enough for a few short words per line. The main text becomes narrower by this amount. It is greyed out until **Margin Notes Col Width (mm)** is ticked.

*(Internal ID: `s_marginNotesWidth` · Config key: `paper/marginnoteswidth`, `document/marginnoteswidth`)*

#### Margin Notes on Left/Inner

- **Where:** Layout tab › Page Setup
- **Type:** Checkbox (not ticked by default)
- **Description:** Place Margin Notes on Left/Inner edge of page
- **View level:** Default and Full views
- **Only available when:** “Margin Notes Col Width (mm)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Margin Notes are normally placed on the Right/Outer edge of the page. But this can be changed for single column layouts to appear on the Left/Inner edge if needed. (Not available for two-column layouts.)

**Explanation:**

Puts the margin-notes column on the left (or inner, near the spine) edge instead of the right (or outer) edge. It only works with one column. It is greyed out for two-column layouts, and PTXprint unticks it when you switch to two columns.

*(Internal ID: `c_marginNotesInner` · Config key: `document/marginnotesinner`)*

### Layout tab › Two Column Layout

#### Gutter Width (mm)

- **Where:** Layout tab › Two Column Layout
- **Type:** Number box
- **Description:** Gutter width for two column layout
- **View level:** Basic, Default and Full views
- **Values:** from 1 to 40, default 4
- **Only available when:** “Two Column Layout” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This is the space between the text of the two columns (measured in millimeters).
>
> This is the space (mm) between the text of the two columns.

**Explanation:**

The space (mm) between the two columns of text. If you use a **Vertical Rule in Gutter**, the line is drawn in the middle of this space. 3–6 mm is common. It is greyed out for a one-column layout.

*(Internal ID: `s_colgutterfactor` · Config key: `document/colgutterfactor`)*

#### Adjust Top (pt)

- **Where:** Layout tab › Two Column Layout
- **Type:** Number box
- **Description:** Adjust top of vertical rule
- **View level:** Default and Full views
- **Values:** from -50 to 50, default 3
- **Only available when:** “Vertical Rule in Gutter”, “Two Column Layout” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This setting raises (using a negative value) or lowers (using a positive value) the starting point of the vertical rule between columns. (Value in pts).

**Explanation:**

Moves the top end of the vertical rule between the columns. A negative value makes the line start higher; a positive value makes it start lower. Use this if the line starts too close to the header rule or too far from the first line of text.

*(Internal ID: `s_colgutteroffset` · Config key: `paper/colgutteroffset`)*

#### Thickness of Rule (pt)

- **Where:** Layout tab › Two Column Layout
- **Type:** Number box
- **Description:** Rule (line) Thickness
- **View level:** Default and Full views
- **Values:** from 0.01 to 1, default 0.4
- **Only available when:** “Two Column Layout” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This sets the thickness (pt) of rules (lines) in the document. This includes the horizontal rule between the header and the text, the vertical column gutter rule and the study notes inter-column rule.

**Explanation:**

How thick (pt) the rules (lines) in the document are. This includes the vertical rule between columns and the horizontal rule under the header. It is greyed out in a one-column layout, even though it also affects the header rule.

*(Internal ID: `s_ruleThickness` · Config key: `document/rulethickness`)*

#### Vertical Rule in Gutter

- **Where:** Layout tab › Two Column Layout
- **Type:** Checkbox (ticked by default)
- **View level:** All view levels (Mini, Basic, Default, Full)
- **Only available when:** “Two Column Layout” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Check this option to include a center line between the two columns.

**Explanation:**

Draws a thin vertical line in the middle of the space between the two columns. Many Bibles use it. It only works with two columns.

*(Internal ID: `c_verticalrule` · Config key: `paper/ifverticalrule`)*

#### Allow Unbalanced Columns

- **Where:** Layout tab › Two Column Layout
- **Type:** Checkbox (not ticked by default)
- **View level:** Basic, Default and Full views
- **Only available when:** “Two Column Layout” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Check this option to allow a different number of lines in each column. This is especially important when using Variable Line Spacing mode and you are trying to Fill Columns.
>
> To alter the maximum number of Unbalanced Lines at the end of a page, visit the Advanced page, select the Other tab, and expand the Page Layout and Spacing section.
>
> If this setting is highlighted in orange it means that the above-mentioned setting was set to 0 (rendering this setting inactive), and has now been increased to the default value of 3.

**Explanation:**

Lets the two columns on a page end at different heights, instead of forcing them to be exactly the same length. This is very useful with **Variable Line Spacing**. The maximum difference in lines is set by **Unbalanced Lines (Max)** on the **Advanced** tab, **Other** tab, **Page Layout and Spacing**. If that value was 0, PTXprint sets it to 3 and highlights this box in orange to tell you.

*(Internal ID: `c_allowUnbalanced` · Config key: `paper/allowunbalanced`)*

### Layout tab

#### Two Column Layout

- **Where:** Layout tab
- **Type:** Checkbox (ticked by default)
- **Description:** One or two column layout
- **View level:** All view levels (Mini, Basic, Default, Full)
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Tick to set the main text in two columns; untick for a single column.
>
> If this setting is checked on, but inactive, it is due to Diglot being active (which obviously must use the Two Column layout).
>
> If you get an unexpected result, check the "Use One/Two Column Layout ..." setting near the end of the Body tab which is only accessible when using the Full View mode.

**Explanation:**

Tick for two columns of text; untick for one. Switching re-flows the whole book and also halves or doubles **Base Indent**. It is greyed out (ticked) when a diglot is set up. Some books can be set differently; see the "Use One/Two Column Layout" setting near the end of the **Body** tab (only in the **Full** view).

*(Internal ID: `c_doublecolumn` · Config key: `paper/columns`)*

### Layout tab › Margins

#### Bottom of Header to Top of Text (pt)

- **Where:** Layout tab › Margins
- **Type:** Number box
- **Description:** Header spacing
- **View level:** Default and Full views
- **Values:** from -20 to 99, default 15
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This setting determines the vertical positioning of the header line by setting the amount of space between the header and the top of the text. (pts)
>
> The top of the main text area is 1 base line spacing above the base line of the first line of the body text.
>
> The space (pt) between the bottom of the header and the top of the main text area. Note that the first line actually starts a little bit below where the main text area starts.
>
> The top of the main text area is 1 base line spacing above the base line of the first line of the body text.

**Explanation:**

The gap (pt) between the bottom of the header and the top of the text area. The header sits inside the top margin, so a bigger value moves the header up towards the top edge of the page. Watch the blue number in the diagram so the header does not get too close to the edge.

*(Internal ID: `s_headerposition` · Config key: `paper/headerpos`)*

#### Bottom of Text to Top of Footer (pt)

- **Where:** Layout tab › Margins
- **Type:** Number box
- **Description:** Footer position
- **View level:** Default and Full views
- **Values:** default 10.5
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This setting can be used to increase/decrease the space between the end of the text and the footer line.
>
> The distance (pt) from the bottom of the text area to the TOP of the footer (including ascenders).

**Explanation:**

The gap (pt) between the bottom of the text and the top of the footer. The footer normally sits inside the bottom margin, so a bigger value moves the footer down towards the bottom edge. Watch the blue number in the diagram.

*(Internal ID: `s_footerposition` · Config key: `paper/footerpos`)*

#### Bottom of Text to End of Page (mm)

- **Where:** Layout tab › Margins
- **Type:** Number box
- **Description:** Bottom margin
- **View level:** Basic, Default and Full views
- **Values:** from 0.5 to 99, default 10.5
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The distance (mm) from the bottom of the main text area to the bottom of the page.
>
> The bottom of the main text area is calculated from the descender of the final line of text (including any footnotes).

**Explanation:**

The bottom margin (mm): from the bottom of the text area to the bottom edge of the page. The footer is placed inside this space (unless **Place Footer Text Above the Bottom Margin** is ticked). Changing it changes **Lines Per Page**.

*(Internal ID: `s_bottommargin` · Config key: `paper/bottommargin`)*

#### Side Margin Width (mm)

- **Where:** Layout tab › Margins
- **Type:** Number box
- **Description:** Side margin width
- **View level:** Basic, Default and Full views
- **Values:** from 0.5 to 200, default 12
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The distance (mm) from the edge of the page to the start of the text area. Note that the left and right (or inner and outer) margins are set to be identical. If you require a greater inner margin, then set the Binding Gutter above.

**Explanation:**

The margin (mm) at the left and right of the text. The two sides are always the same. To get more space at the spine, use **Binding Gutter (mm)** instead of making this bigger. 10–15 mm is common.

*(Internal ID: `s_margins` · Config key: `paper/margins`)*

#### Space between Rule and Top of Text (pt)

- **Where:** Layout tab › Margins
- **Type:** Number box
- **Description:** Space between horizontal rule and main text area
- **View level:** Basic, Default and Full views
- **Values:** from -100 to 100
- **Only available when:** “Horizontal Rule” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The space (pt) between the horizontal rule and the top of the main text area. Note that the first line actually starts a little bit below where the main text area starts.
>
> The top of the main text area is 1 base line spacing above the base line of the first line of the body text.

**Explanation:**

The gap (pt) between the horizontal rule under the header and the top of the text area. It is greyed out until **Horizontal Rule** is ticked. Note that the first line of text actually starts a little below the top of the text area.

*(Internal ID: `s_rhruleposition` · Config key: `paper/rulegap`)*

#### Start of Page to Top of Text (mm)

- **Where:** Layout tab › Margins
- **Type:** Number box
- **Description:** Top margin
- **View level:** Basic, Default and Full views
- **Values:** from 0.5 to 200, default 18
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The distance (mm) from the top of the page to the top of the main text area. Note that the first line actually starts a little bit below where the main text area starts.
>
> The top of the main text area is 1 base line spacing above the base line of the first line of the body text.

**Explanation:**

The top margin (mm): from the top edge of the page to the top of the text area. The header is placed inside this space. Changing it changes **Lines Per Page**.

*(Internal ID: `s_topmargin` · Config key: `paper/topmargin`)*

#### Tweak top margin (auto adjust)

- **Where:** Layout tab › Margins
- **Type:** Button
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Fine Tune Top Margin:
>
> This button is only active when PTXprint has a suggestion to shrink or expand the top margin slightly to minimise wasted vertical space on the page. Click to accept the suggestion.
>
> If there is more than half a line of 'spare' space on the page then the top margin will decrease slightly to fit one more line of text on the page.
>
> If there is less than half a line of 'spare' space on the page then the top margin will increase slightly to fill the page more evenly (with the same number of lines of text).
>
> If you prefer to keep the exact top margin specified, then do NOT click this option. Instead, use the similar button to adjust either the Line Spacing or Bottom Margin.

**Explanation:**

Changes the top margin slightly so that a whole number of lines fits the page. It is only active when **Lines Per Page** is red. Use it when you want to keep your line spacing and font size exactly as they are.

*(Internal ID: `btn_adjust_top`)*

#### Tweak bottom margin (auto adjust)

- **Where:** Layout tab › Margins
- **Type:** Button
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Fine Tune Bottom Margin:
>
> This button is only active when PTXprint has a suggestion to shrink or expand the bottom margin slightly to minimise wasted vertical space on the page. Click to accept the suggestion.
>
> If there is more than half a line of 'spare' space on the page then the bottom margin will decrease slightly to fit one more line of text on the page.
>
> If there is less than half a line of 'spare' space on the page then the bottom margin will increase slightly to fill the page more evenly (with the same number of lines of text).
>
> If you prefer to keep the exact bottom margin specified, then do NOT click this option. Instead, use the similar button to adjust either the Line Spacing or Top Margin.

**Explanation:**

Changes the bottom margin slightly so that a whole number of lines fits the page. It is only active when **Lines Per Page** is red. Use it when you want to keep your line spacing, font size and top margin exactly as they are.

*(Internal ID: `btn_adjust_bottom`)*

#### Place Footer Text Above the Bottom Margin

- **Where:** Layout tab › Margins
- **Type:** Checkbox (not ticked by default)
- **Description:** Don't place footer in the margin area
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Normally the footer page number sits in the bottom margin.
>
> However if you need the page number to be placed above the bottom margin (where the text would normally flow until) then enable this option.

**Explanation:**

Normally the footer (for example the page number) is printed in the bottom margin. Tick this to print it above the bottom margin, inside the area where the text would normally go. Use this when the printer needs the whole margin to be empty. The text area becomes a little shorter.

*(Internal ID: `c_noinkinmargin` · Config key: `footer/noinkinmargin`)*

#### 8.5mm

- **Where:** Layout tab › Margins
- **Type:** Label
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The distance (mm) from the edge of the page to the bottom of the footer area.

**Explanation:**

A calculated value (you cannot type in it): the distance from the bottom of the footer to the bottom edge of the page. It is shown by the blue arrow at the bottom of the diagram. If it is very small, the footer may be cut off when the pages are trimmed.

*(Internal ID: `l_footer2edge`)*

#### Horizontal Rule

- **Where:** Layout tab › Margins
- **Type:** Checkbox (not ticked by default)
- **View level:** Basic, Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Check this option to add a horizontal line under the page header, before the main body text begins.

**Explanation:**

Draws a horizontal line under the header, across the text width. Use **Space between Rule and Top of Text (pt)** to set its position and **Thickness of Rule (pt)** to set its thickness.

*(Internal ID: `c_rhrule` · Config key: `header/ifrhrule`)*

#### 8.5mm

- **Where:** Layout tab › Margins
- **Type:** Label
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The distance (mm) from the top of the page to the top of the header area. Note that due to the ascent of the font, the header text actually starts a little bit below the top of the header area.

**Explanation:**

A calculated value (you cannot type in it): the distance from the top edge of the page to the top of the header. It is shown by the blue arrow at the top of the diagram. If it is very small or negative, make the top margin larger or the header gap smaller.

*(Internal ID: `l_margin2header`)*
