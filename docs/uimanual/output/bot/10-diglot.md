# 13. Diglot tab (two or more languages)

## 13.1 What this tab is for

A **diglot** is a publication with two texts side by side on the page. The texts can be two languages, two scripts of the same language, or two translations. A **polyglot** has three or more texts. PTXprint lines the texts up so that the same verses (or paragraphs) start at the same height in each column.

Each text in a diglot comes from its own Paratext project and uses its own PTXprint configuration. The configuration you have open when you tick **Diglot (or Polyglot)** becomes the **primary** text (code **L**). The other texts are **secondary** texts (code **R**, then **A**, **B**, **C** …). The primary configuration controls the page: page size, margins, headers and footers, and most layout settings. Each secondary configuration controls how its own text looks: its fonts, font size, line spacing, footnotes and so on.

Come to this tab to turn a configuration into a diglot, choose the other project(s), set the column widths, and choose how the texts are merged (joined together). The **Diglot** tab is shown in the **Regular** and **Full** views only. When **Diglot (or Polyglot)** is ticked, the tab name turns blue.

**Important:** turning a diglot on cannot simply be undone. Before you start, go to the **Basic** tab, **Layout Configuration** area, and use **Save As** to make a new configuration for the diglot, so your normal (single-text) configuration stays as it is.

## 13.2 Diglot (or Polyglot)

The **Diglot (or Polyglot)** checkbox is in the frame title. All other settings on the tab are hidden until it is ticked.

When you tick it:

1. PTXprint asks you to confirm. Click **Yes** to continue, or **No** to stop.
2. A table appears with two rows: **L** (your current project and configuration) and **R** (empty).
3. PTXprint opens the **Project** list for the **R** row so you can choose the secondary project.
4. On the **Layout** tab, **Two Column Layout** is ticked and greyed out. A diglot always uses two (or more) columns. The gutter (the space between the columns) and **Vertical Rule in Gutter** on the **Layout** tab now control the space and the line between the texts.

If you later untick the box, PTXprint does not turn the diglot off. Instead it opens the **Save As Monoglot** dialog (see below).

## 13.3 The texts table

The table lists one row for each text. Left-click a cell to change it. Right-click anywhere in the table to open a menu. You can have up to 9 texts (codes L, R, A–G).

The columns are:

* **Code** – the letter that identifies this text (L, R, A, B …). L is always the primary text and cannot be changed. The cell is shaded with the background colour of that text, if one is set.
* **1|2** – which page of an open book the text goes on: **1** = the left page, **2** = the right page. For a normal side-by-side diglot, leave every text on **1**. Put texts on **2** only if you want them on the facing page (see **Layout** below).
* **Project** – the Paratext project for this text. You cannot change it for the L row.
* **Configuration** – which PTXprint configuration of that project to use. The list shows the configurations that exist for the project you chose. A project and configuration pair can only be used once in the table.
* **Captions** – tick to print this text's picture captions under shared pictures. The L text always shows its captions.
* **Font Size** and **Spacing** – the font size and line spacing (in pt; 1 pt is about 0.35 mm) for this text. These are the same values as **Font Size** and **Line Spacing** on the **Layout** tab of that text's configuration. Changing them here changes them there.
* **% Width** – how much of the page width this text takes. The values for all texts on the same page must add up to 100. If they do not, the numbers turn red and bold.
* **Weight** – how much this text counts when PTXprint decides where to line the texts up. Leave the values equal unless you have a reason to change them.

The right-click menu has these items:

* **Add a row/text** – adds another text (this makes a polyglot). Choose its **Project** and **Configuration** next.
* **Move Up** / **Move Down** – change the order of the extra texts. The L and R rows cannot be moved.
* **Copy Font Size to All** / **Copy Spacing to All** – copy the value of the selected row to every row.
* **Distribute Widths** – share the width evenly between all texts on the same page as the selected row.
* **Delete Row** – remove the selected text. The L and R rows cannot be deleted.
* **Edit Settings…** – switch the whole PTXprint window to the selected secondary text's configuration, so you can change its fonts and other settings (see **Changing the settings of a secondary text** below). Not available for the L row.
* **Set Color…** – choose a light background colour (shading) behind this text's column. This can help readers find the right text.
* **Remove All Colors** – remove the shading from all texts.

Next to the table, a small picture shows how the texts will sit on the page, using the widths and colours from the table.

## 13.4 Layout

The **Layout** text box describes where each text goes. PTXprint fills it in for you from the **1|2** column, so most people never need to type in it.

* Letters next to each other share a page, side by side. **LR** means L on the left and R on the right of every page.
* A comma starts the next page of the spread. **L,R** means L fills the left page and R fills the facing right page.
* A hyphen **-** is a page with no Bible text.

Every code in the table must appear in the layout, and L and R must always be there. If the layout has a problem, the preview shows a red **Layout Error** box with the reason, for example "Missing: A", "L or R missing", "Spaces not allowed" or "Comma required for multi-page spread". The check runs when you leave the box.

## 13.5 Merging mode

Before printing, PTXprint merges the texts into one file, in "chunks" that should line up across the columns. **Merging mode** chooses how the chunks are made:

* **Chapter Verse** – lines the texts up on chapters and verses. Only offered for a diglot (two texts).
* **Scored** – the default. It uses a scoring method and also tries to line up paragraphs where the verse numbers match. This usually gives the best result.
* **Scored (Chapter)** – like **Scored**, but always lines up at the start of each chapter.
* **Scored (Verse)** – like **Scored**, but lines up at every verse. This can leave many small gaps.

For a polyglot (three or more texts), only the three **Scored** options are offered.

## 13.6 Column widths and auto-balance

Two texts rarely take the same amount of space. One language may need 20% more words than the other. If both columns are 50% wide, the shorter text has white space under every chunk. To fix this, give the longer text more width in the **% Width** column (for example 55 and 45), or make its font size or line spacing a little smaller.

The **Auto-calculate optimum widths of diglot columns** button does this for you. It prints the job 10 or more times, trying widths near the current ones, and keeps the widths that give the fewest pages. So select one short book on the main window before you click it. The button only works for a diglot with exactly two texts, and only when the **Print** button is available. When it has finished, the button is released, and you can use it again (for example after you change a font size).

## 13.7 Notes, headers and other options

* **Separate Notes in Two Columns** (ticked by default) keeps each text's footnotes under its own column. If you untick it, the footnotes of all texts are put together in one notes area, one after another. This can be useful when only one of the texts has footnotes.
* **Vertical Rule in Notes Area** draws a line between the separate notes columns. **Join with Rule Above** makes this line meet the line between the text columns, so there is no small gap. The text-column line itself is **Vertical Rule in Gutter** on the **Layout** tab.
* **Adjust Center Header Based on Column Widths** moves the centre part of the header (and footer) so that it sits above the gutter, when the two columns have different widths.
* **Use Serial Layout for These Books** lists books that should not be merged. For these books PTXprint prints the whole book in the primary text, then the whole book in the secondary text, one after the other. Use this for front matter, introductions, glossaries and other back matter. The default list is **FRT BAK GLO XXA XXB**.

## 13.8 Changing the settings of a secondary text

The look of each secondary text (fonts, font size, line spacing, footnote settings, styles, and so on) comes from its own configuration. To change it:

1. On the **Diglot** tab, right-click the row of that text and choose **Edit Settings…**.
2. The PTXprint window now shows the secondary project and configuration. The big **Print** button changes to **Return to Primary**. A small **Print** button appears next to it.
3. Change the settings you need, for example on the **Fonts+Scripts** tab or the **Styles** tab.
4. If you want to check this text by itself, click the small **Print** button. It makes a PDF of the secondary text only.
5. Click **Return to Primary** to go back to the primary configuration. Then click **Print** to make the diglot PDF.

Some settings always come from the primary configuration, whatever the secondary configuration says. These include the page size, margins, header and footer positions, the footnote rule, where cross-references go, page breaks before chapter 1, book introductions and the outline, parallel passage references and the chapter range. The page border and the centre footer of the secondary text are also turned off. So change these in the primary configuration.

## 13.9 What happens to pictures, notes and headers

**Pictures.** Pictures come from each text's own picture list. If both texts have the same picture file at the same verse, PTXprint prints it once. The primary caption is used, and the secondary caption is added if **Captions** is ticked for that text. If a picture is only in one text, or uses a different file, it is printed in that text's column. Pictures are not shared in the books listed in **Use Serial Layout for These Books**, because those books are printed one text after the other. There, each text keeps its own pictures and captions. On the **Pictures** tab, the picture list shows the secondary caption in the **Sec.Caption** column, and pictures that belong only to a secondary text have the text's code after the book code in the anchor (for example **MATR 5.3**).

**Notes.** Whether a text has footnotes and cross-references depends on that text's own configuration (its **Notes+Refs** settings). The layout of the notes area (separate or together, rules) is set on this tab.

**Headers and footers.** The headers and footers are set in the primary configuration, on the **Header+Footer** tab. When diglot is on, each header part has **Pri** and **Sec** buttons. Choose **Pri** to use the primary text (its references and its font) for that part, or **Sec** to use the secondary text. If **Mirror Pages** is ticked on the **Layout** tab, the texts also swap sides on even pages, so each text stays on the same side relative to the binding.

**Front matter.** The **Generate Front Matter** dialog (Peripherals tab) offers a **DIGLOT** template when diglot is on.

## 13.10 Auto Page Fill for diglots and polyglots (experimental)

The **Auto Page Fill** tool in the PDF Preview window (see the chapter on the PDF Preview window) also works for a diglot or polyglot. When **Diglot (or Polyglot)** is ticked, PTXprint uses a special version of the tool. It tries to fill each page, and it also tries to keep the texts side by side at the same height, so that each chunk ends at about the same line in every column. This version is new and experimental. Check the result carefully, and fix the pages it could not fill by hand.

On the **Advanced** tab, **Other** sub-tab, in the **Automatic Page Filler** area, **The cost of imbalance in a polyglot slice** sets how important it is that the columns end at the same height. A higher value makes the tool try harder to keep the columns even. A lower value lets it accept columns of different heights if the paragraphs look better. This setting is only used for diglots and polyglots.

## 13.11 Save As Monoglot

You cannot just switch a diglot off, because that would lose all the diglot settings. When you untick **Diglot (or Polyglot)**, the **Save As Monoglot** dialog opens instead:

* Click **Cancel** to keep the diglot as it is.
* Or type a name for a new configuration and click **OK**. PTXprint saves a copy of the current settings under that name, with diglot turned off, and opens it. Your diglot configuration is left unchanged.

## 13.12 Common tasks

### Set up a diglot

1. Make sure both projects print well on their own. Each one needs a PTXprint configuration you are happy with (fonts, styles, notes).
2. Open the primary project. On the **Basic** tab, in the **Layout Configuration** area, click **Save As** and give the diglot its own configuration name (for example `Diglot`).
3. On the **Diglot** tab, tick **Diglot (or Polyglot)**. Click **Yes** in the message.
4. In the **R** row, choose the secondary **Project**, then its **Configuration**.
5. Check that **% Width** is 50 and 50 (or another pair that adds up to 100).
6. Leave **Merging mode** on **Scored**.
7. On the main window, choose one short book that exists in both projects. Click **Print**.
8. Look at the result. Then balance the widths (see below) and adjust the headers on the **Header+Footer** tab.

### Change the font of the secondary text

1. On the **Diglot** tab, right-click the **R** row and choose **Edit Settings…**.
2. Go to the **Fonts+Scripts** tab and change the font.
3. Click **Return to Primary**.
4. Click **Print**.

To change only the font size or line spacing, you do not need to switch: type the new value in the **Font Size** or **Spacing** cell of that row.

### Balance the columns so there is less white space

1. Print a short book and see which column has the most white space.
2. Give the longer text more width: for example **% Width** 55 for L and 45 for R. Make sure the two numbers add up to 100.
3. Print again and compare the page count.
4. Or select one short book and click **Auto-calculate optimum widths of diglot columns**. Wait until it has finished all its print runs.

### Add a third text (polyglot)

1. Right-click in the table and choose **Add a row/text**. A new row (code **A**) appears.
2. Choose its **Project** and **Configuration**.
3. Right-click a row and choose **Distribute Widths**, so all three texts share the page.
4. Check that the **Layout** box contains all the codes (for example **LRA**).
5. Print.

### Put the two texts on facing pages

1. In the **R** row, change **1|2** to **2**.
2. Check that the **Layout** box now shows **L,R**.
3. Set **% Width** to 100 for each text (each one has a page to itself).
4. Print.

### Keep the introduction and glossary as whole books

1. In **Use Serial Layout for These Books**, type the book codes, with spaces between them, for example `FRT INT GLO BAK`.
2. Print. These books are printed one after the other (primary first, then secondary) instead of side by side.

### Shade the background of each text

1. Right-click the row of a text and choose **Set Color…**.
2. Choose a light colour and click **OK**.
3. Repeat for the other texts if you want. To remove all shading, right-click and choose **Remove All Colors**.

### Turn a diglot back into a normal (single-text) configuration

1. Untick **Diglot (or Polyglot)**. The **Save As Monoglot** dialog opens.
2. Type a new configuration name (letters, numbers, `-`, `_` and brackets only, no spaces).
3. Click **OK**. PTXprint opens the new single-text configuration. The diglot configuration is still there if you need it again.

## 13.13 Common problems

**The Print button is greyed out, or the status bar says "No Config found for diglot".**
The secondary row has no valid project or configuration. In the **R** row (and any other rows), choose a **Project** and then a **Configuration**.

**Error: "These books are not available in the secondary diglot project".**
You selected a book that the secondary project does not have. Select only books that exist in every project. (Books listed in **Use Serial Layout for These Books** are not checked.)

**Error: "Failed to merge texts due to a Syntax Error" (Diglot Merge Error).**
One of the texts has a marker error. Run the Basic Checks in Paratext for every project in the diglot. If you use a changes file (on the **Advanced** tab), check that a rule there has not caused the error.

**The texts do not line up well, or there are big gaps under each chunk.**
Try another **Merging mode** (for example **Scored (Chapter)** or **Chapter Verse**). Change the **% Width** so the longer text gets more space, or reduce its font size or line spacing. Try **Auto-calculate optimum widths of diglot columns**. To fill the pages after that, you can try the **Auto Page Fill** tool in the PDF Preview window (experimental for diglots; see above).

**The % Width numbers are red.**
The widths of the texts on one page do not add up to 100. Change them, or right-click and choose **Distribute Widths**.

**The layout preview shows a red "Layout Error".**
Read the message in the box. Usually a code is missing from the **Layout** box, or the **1|2** column does not match the layout (texts on page 2 must come after the comma). Change the **1|2** values and PTXprint will rebuild the layout.

**I cannot untick Diglot (or Polyglot).**
This is on purpose. PTXprint opens the **Save As Monoglot** dialog so your diglot settings are not lost. Give a new name and click **OK** to get a single-text configuration.

**Two Column Layout on the Layout tab is greyed out.**
A diglot always uses columns, so PTXprint ticks this box and locks it while diglot is on.

**I changed the secondary text's font (or margins) but nothing changed.**
Fonts and other text settings must be changed in the secondary configuration: use **Edit Settings…**, then **Return to Primary**. Page size, margins, header positions and similar page settings always come from the primary configuration, so change those there.

**The big button says "Return to Primary" instead of "Print".**
You are looking at a secondary configuration (after **Edit Settings…**). Click **Return to Primary**, then **Print**. The small **Print** button prints only the secondary text.

**The secondary text has no footnotes.**
Footnotes and cross-references are switched on or off in each text's own configuration. Use **Edit Settings…** for that text and check its notes settings.

**The secondary caption is missing under a picture.**
Tick **Captions** in that text's row. Also check that both texts use the same picture file at the same verse; otherwise PTXprint treats them as two different pictures. In books listed in **Use Serial Layout for These Books**, pictures are not shared, so each text shows only its own caption.

**A picture is printed twice.**
The two texts probably have the same picture with a different file name or at a different verse. On the **Pictures** tab, make the entries match, or remove the picture from one text.

**The header shows the references of only one text.**
On the **Header+Footer** tab, choose **Pri** or **Sec** for each part of the header. For example, use **Pri** for the left part and **Sec** for the right part.

**The primary text is on the left on some pages and on the right on others.**
**Mirror Pages** is ticked on the **Layout** tab. With it, the columns swap on even pages. Untick it if you want the primary text always on the left.

**The Auto-calculate button is greyed out.**
It only works with exactly two texts, and only when printing is possible. (In older versions the button could stay pressed after one run until PTXprint was restarted. This is fixed.)

**The Chapter Verse merging mode is missing.**
You have three or more texts. Only the **Scored** modes work for a polyglot.

**The Diglot tab is missing.**
The tab is only shown in the **Regular** and **Full** views. Change the view level.

## 13.14 Settings reference

### Save As Monoglot... (dialog)

#### OK

Button · Regular+ · `btn_disableDiglot_ok`

Saves the current settings under the new name with diglot turned off, and opens that new configuration. The diglot configuration is not changed. Greyed out until you type a valid new name.

#### Cancel

Button · Regular+ · `btn_disableDiglot_cancel`

Closes the dialog. The configuration stays a diglot and nothing is changed.

#### Save as a new Configuration (which will be a monoglot) – Enter a name for the configuration to be saved

Text box · Regular+ · `t_newMonoglotConfigName`

> Enter a name for the configuration to be saved.
>
> Note that only Roman/Latin names are supported using: a-z A-Z, 0-9, parentheses, underscores and hyphens. Spaces are not permitted.

If the name is not allowed, or a configuration with that name already exists, a message appears and **OK** stays greyed out.

### Diglot

#### Diglot (or Polyglot)

Checkbox, off · Regular+ · `c_diglot` · cfg `document/ifdiglot`, `document/ifndiglot`, `snippets/diglot`  
Also: Enable diglot or discript publication · Shown when: “Diglot (or Polyglot)”

> A Diglot publication contains two languages, or scripts, or texts.
>
> A Polyglot contains more than two. Right-click in the table below to add other texts to the list.
>
> Tip: use Save As first. Unticking this later does not simply switch back; it offers to save a single-text copy of the configuration under a new name.

The open configuration becomes the primary (L) text. Make a separate configuration with **Save As** (on the **Basic** tab) first. When it is ticked, **Two Column Layout** on the **Layout** tab is ticked and locked.

#### Diglot (or Polyglot)

##### Use Default Header Settings for Diglot

Checkbox, off · Regular+ · `c_diglotHeaders` · cfg `document/diglotheaders`  
Also: Diglot: Use default header settings · Needs: “Diglot (or Polyglot)” · Shown when: “Diglot (or Polyglot)”

> Checking this option will override the header settings and place the Reference Ranges on the outer edges and Page Number in (or near) the middle.

This checkbox is normally hidden. In this version it is saved with the configuration but it does not change the printed headers. Set the headers on the **Header+Footer** tab instead, using the **Pri** and **Sec** buttons for each part.

##### Adjust Center Header Based on Column Widths

Checkbox, off · Regular+ · `c_diglotAdjCenter` · cfg `document/diglotadjcenter`  
Also: Diglot: Adjust center header horizontal position · Needs: “Diglot (or Polyglot)” · Shown when: “Diglot (or Polyglot)”

> If the column widths of the two sides of the diglot are unequal, PTXprint can ensure that the content of the center header matches the position of the gutter (space between the two different columns).

The centre header and footer move towards the gutter instead of staying in the middle of the page. With equal widths it makes no difference.

##### Separate Notes in Two Columns

Checkbox, on · Regular+ · `c_diglotSeparateNotes` · cfg `document/diglotsepnotes`  
Also: Diglot: Keep notes in distinct columns · Needs: “Diglot (or Polyglot)” · Shown when: “Diglot (or Polyglot)”

> If this option is disabled, the footnotes from both sides of the diglot get merged together and are interspersed one after the other.
>
> Depending on the scripts and text direction, this may or may not be desirable. If in doubt, leave this option checked ON.

Untick it when only one text has notes; the notes then go in one shared area, in the order they are met. Unticking it greys out **Vertical Rule in Notes Area** and **Join with Rule Above**.

##### Layout

Text box · Regular+ · `t_layout` · cfg `document/diglotlayout`  
Needs: “Diglot (or Polyglot)” · Shown when: “Diglot (or Polyglot)”

> The Layout string describes how the various texts should appear on the page(s).
>
> All of the texts listed in the table above must be mentioned. The comma represents the next page. A forward slash / will put one text under the other on the same page (this is still to come and cannot be used yet).

PTXprint fills this in from the **1|2** column of the table, so you seldom need to type here. Letters together share a page; a comma starts the facing page; a hyphen is a page with no text. Spaces are not allowed. If you use `/`, PTXprint reports "Complex layouts are not yet supported".

##### Merging mode – Diglot/Polyglot: Merging Mode

Drop-down · Regular+ · `fcb_diglotMerge` · cfg `document/diglotmergemode`  
Choices: Chapter Verse | Scored | Scored (Chapter) | Scored (Verse) · Needs: “Diglot (or Polyglot)” · Shown when: “Diglot (or Polyglot)”

> When the different texts of a diglot are merged, there are various algorithms which may be used to obtain the best overall result:
>
> * Chapter Verse - aligns on chapters and verses
>
> * Scored - an alternative algorithm which uses weighted scores  
>   and tries to align paragraphs when the verse numbers match
>
> * Scored (Chapter) - as a minimum, forces alignment at chapter breaks
>
> * Scored (Verse) - as a minimum, forces alignment at each verse, which  
>   can result in a lot of breaks!
>
> Note that for polyglots, only the Scored options are available to be used.

Start with **Scored**. If chapters drift out of line, try **Scored (Chapter)**. Use **Scored (Verse)** only when other modes fail, because it can leave many gaps.

##### When the different texts of a diglot are merged, there are v...

Text box · Regular+  
Needs: “Diglot (or Polyglot)” · Shown when: “Diglot (or Polyglot)”

> When the different texts of a diglot are merged, there are various algorithms which may be used to obtain the best overall result:
>
> * Chapter Verse - aligns on chapters and verses
>
> * Scored - an alternative algorithm which uses weighted scores  
>   and tries to align paragraphs when the verse numbers match
>
> * Scored (Chapter) - as a minimum, forces alignment at chapter breaks
>
> * Scored (Verse) - as a minimum, forces alignment at each verse, which  
>   can result in a lot of breaks!
>
> Note that for polyglots, only the Scored options are available to be used.

##### Auto-calculate optimum widths of diglot columns

Toggle, off · Regular+ · `btn_adjust_diglot`  
Needs: “Diglot (or Polyglot)” · Shown when: “Diglot (or Polyglot)”

> Auto calculate primary percentage by trying to reduce the page count. This will run your print job up to 10 times or more, so choose a small book to run on. It will attempt to find the best balance of column widths near to the current % Width values. Only available for a diglot with two texts.

It changes only the **% Width** of the L and R rows. It is greyed out for polyglots and when printing is not possible. When the runs are finished (or if an error stops them), the button is released, so you can click it again.

##### Use Serial Layout for These Books – List of diglot books not to be merged, to come one after the other

Text box · Regular+ · `t_diglotSerialBooks` · cfg `document/diglotserialbooks`  
Needs: “Diglot (or Polyglot)” · Shown when: “Diglot (or Polyglot)”

> Some books (e.g. Introduction, Glossary, Back Matter, etc.) in a diglot publication should not be merged to appear side-by-side, but instead need to occur one after the other.
>
> Add the 3-letter book codes for any books that should not be merged. These will appear one after the other.

Separate the codes with spaces. The primary version is printed in full, then the secondary version. The default is **FRT BAK GLO XXA XXB**. Pictures in these books are not shared between the texts: each text keeps its own pictures and captions.

##### Separate Notes in Two Columns

###### Vertical Rule in Notes Area

Checkbox, off · Regular+ · `c_diglotNotesRule` · cfg `document/diglotnotesrule`  
Also: Diglot: Vertical rule in notes area · Needs: “Separate Notes in Two Columns”, “Diglot (or Polyglot)” · Shown when: “Diglot (or Polyglot)”

> Add a vertical rule between the two sides of the notes area of the diglot.

Often used together with **Vertical Rule in Gutter** on the **Layout** tab, which draws the line between the text columns.

###### Join with Rule Above

Checkbox, off · Regular+ · `c_diglotJoinVrule` · cfg `document/diglotjoinvrule`  
Also: Diglot: Join notes rule with gutter rule · Needs: “Separate Notes in Two Columns”, “Vertical Rule in Notes Area”, “Diglot (or Polyglot)” · Shown when: “Diglot (or Polyglot)”

> To prevent a small gap in the line allow the vertical line to extend down into the notes area.

Makes one continuous line from the gutter line down through the notes area.
