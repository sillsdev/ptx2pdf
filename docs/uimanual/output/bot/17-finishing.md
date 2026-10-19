# Finishing tab

## What this tab is for

The **Finishing** tab controls what happens to the PDF *after* the pages have been typeset. Come here when you are getting ready to send the book to a printer, or when you want to print it yourself as a folded booklet.

On this tab you can:

* choose the **PDF Output Format** that your printer asks for (for example CMYK or black and white);
* add **crop marks** and a **watermark** (such as the word "DRAFT");
* print the pages as a **booklet** (two or more pages on each sheet of paper, in the right order for folding);
* **compare** the new PDF with an older one, to see exactly what changed;
* keep older copies of the PDF, and store your settings inside the PDF.

The **Finishing** tab is shown in the **Default** and **Full** views. Some settings are only shown in the **Full** view. This is noted for each setting below.

Most settings on this tab do not change the layout of the text. They change the finished PDF file. You must click **Print** (make the PDF again) before a change is visible.

### Some print-shop words in simple terms

* **Trim size** – the size of the finished book page, after the printer cuts it. In PTXprint this is the **Page Size** on the **Layout** tab.
* **Crop marks** (also called trim marks) – thin lines in the corners, outside the page, that show the printer where to cut.
* **Bleed** – a picture or colour that goes right to the edge of the page. The printer needs it to go a little *past* the cut line (usually about 3 mm), so that no white strip shows if the cut is not exact.
* **RGB** – the colours used by screens (Red, Green, Blue).
* **CMYK** – the four inks used by most colour printing presses (Cyan, Magenta, Yellow and blacK). Many printers ask for CMYK files.
* **Grayscale (B/W)** – only black ink, in shades of grey.
* **Spot colour** – one extra, ready-mixed ink (often a Pantone colour) used in addition to black, for example red for the words of Jesus or for headings.
* **PDF/X** – a type of PDF made for printing. It contains everything the printer needs (fonts, colour information) and nothing that could cause problems.
  * **PDF/X-1a** – the older, strict type. All colours must be CMYK (or grey/spot) and there may be no transparency (see-through effects). Many printing presses still ask for this.
  * **PDF/X-4** – the newer type. It allows RGB colours with colour profiles and transparency. Many modern printers and digital (print-on-demand) printers accept it.
* **PDF/A** – a type of PDF made for keeping documents for a very long time (archiving).
* **Imposition** – arranging several book pages on one large sheet of paper, so that after folding and cutting the pages come out in the right order.
* **Signature** – a group of sheets that are folded together and sewn or glued into the book as one unit.

If your printer gives you a list of requirements, read it carefully. Look for: trim size, bleed, crop marks (yes or no), colour (CMYK, grey, or RGB), and PDF type (PDF/X-1a or PDF/X-4). Then set these on the **Layout** tab and on this tab. If you are not sure, ask the printer for a sample "print-ready PDF specification".

## PDF Details

This area controls the type of PDF that PTXprint makes. (This area is shown in the **Default** and **Full** views. Some settings are only in the **Full** view.)

### PDF Output Format

Choose the format that matches how the book will be used:

* **Screen (Quickest)** – the normal choice while you are still working on the book. PTXprint makes the PDF directly, with no extra processing. Use this for checking and proof-reading.
* **Digital-RGB** – a PDF/X-4 file in RGB colours. Good for reading on screen, for sharing as an e-book, and for printing on an office or home printer.
* **Digital-CMYK (Transparency)** – a PDF/X-4 file for printers who want CMYK but can accept transparency.
* **Print-CMYK** – a PDF/X-1a file with all colours turned into CMYK. Use this for a commercial printing press that asks for PDF/X-1a or CMYK.
* **Print-Gray (B/W)** – a PDF/X-1a file in black and shades of grey only. Use this for a book printed only in black ink. Coloured text and pictures are turned into grey.
* **Print-Spot** – black plus one spot colour. Any colour close to the **Color Hue** you choose is printed with the spot ink; everything else is printed in black and grey. The **Color Hue** and **Tolerance (%)** settings are only active when you choose this format.

The formats other than **Screen** need extra processing after the PDF is made. This takes more time, especially when the book has many pictures. PTXprint shows a note in the status bar about this.

PTXprint adds a short ending to the PDF file name, so you can see which format a file has: **_RGB**, **_CMYK-Transparent**, **_CMYK**, **_BW** or **_Spot**. **Screen** adds nothing.

When you choose **Print-CMYK**, **Print-Gray** or **Print-Spot** and thumb tabs are turned on, PTXprint turns on **Only Show on Odd Pages** for the thumb tabs (on the **Tabs+Borders** tab), and tells you in the status bar.

### Other PDF settings

* **Crop Marks** adds cut lines around every page. To make room for them, PTXprint makes each PDF page larger by 0.5 inch (about 12.7 mm) on every side. Only turn this on if your printer asks for crop marks. Many print-on-demand printers do *not* want them.
* **Number of Previous PDFs to be Kept** keeps older copies of your PDF (with **_1**, **_2** … at the end of the name). You need at least 1 to use **Compare PDFs** with the previous version.
* **Include Config Settings Within PDF** stores your settings inside the PDF file. Later, you (or someone else) can load the settings back from this PDF, using **Import Settings**.
* **Archive (PDF/A-4)** makes a PDF that is better for long-term storage. (Only in the **Full** view.)
* **Extract Color Inserts** and **Extra XDV Processing** are special tools. (Only in the **Full** view.)
* **Apply Watermark PDF** puts a PDF (for example "DRAFT") on every page.

## Booklet Pagination

This area lets you print several book pages on one larger sheet of paper, arranged so that you can fold the sheets into a booklet. This is called imposition. (This area is shown in the **Basic**, **Default** and **Full** views. Some settings are only in the **Full** view.)

* **Pages Per Spread** – how many book pages go on *one side* of a sheet. **1-up (No booklet)** is the normal setting: one page per PDF page. **2-up** is a normal folded booklet: for example, A5 pages on A4 paper. **4-up** and **8-up** put more pages on bigger sheets, for printers who fold the sheet more than once.
* **Physical Paper Size** – the size of the sheet you will print on. For 2-up, it is normally twice the page size (A5 pages → A4 sheet).
* **Sheets Per Signature**, **Fold Cut Margin (mm)** and **Fold First** are for professional binding. (Only in the **Full** view.) Leave them at their starting values unless the printer tells you what to use.

When **Pages Per Spread** is more than 1-up:

* the signature settings become active;
* **Scale to fit** is greyed out;
* the **Finishing** tab label changes colour, to remind you that the PDF will be imposed;
* the PDF file name gets an extra ending, such as **_2up**;
* crop marks (if ticked) are drawn on the large sheet, not on each page.

When **Pages Per Spread** is **1-up**, you can tick **Scale to fit**. Then PTXprint enlarges or shrinks each page so that it fits the **Physical Paper Size**, centred on the sheet.

If the pages do not fit on the paper you chose, PTXprint shows a **Paper Size Error**. Choose a larger **Physical Paper Size** or a smaller number of pages per spread.

## Compare PDFs

This area makes a "diff" PDF that shows what changed between the new PDF and an older one. This is very useful after a late correction: you can quickly check that only the expected pages changed. (The two colour settings are only shown in the **Full** view. **Show Max Diff Pages** is shown in the **Default** and **Full** views.)

How it works:

1. PTXprint keeps a copy of the previous PDF (the file ending **_1.pdf**), as long as **Number of Previous PDFs to be Kept** is 1 or more.
2. When **Compare PDFs** is ticked and you click **Print**, PTXprint makes the new PDF and then compares it with the old one.
3. If it finds differences, it makes a file ending **_diff.pdf** and opens it. Added or moved text is shown in one colour; removed text or old positions in another colour.
4. If there are no differences, the status bar says **No differences found**.

By default PTXprint compares with the previous PDF (**Previous PDF (_1)**). Click **Select...** to compare with any other PDF instead, for example the PDF you sent for the last proof check.

## Common tasks

### Make a PDF for a commercial printer who asks for PDF/X-1a in CMYK

1. On the **Layout** tab, check that the **Page Size** is the trim size the printer wants.
2. On the **Finishing** tab, in the **PDF Details** area, set **PDF Output Format** to **Print-CMYK**.
3. Tick **Crop Marks** only if the printer asks for crop marks.
4. Make sure **Pages Per Spread** is **1-up (No booklet)**. Printers do their own imposition.
5. Click **Print**. The new PDF name ends with **_CMYK**.

### Make a black-and-white PDF for printing

1. On the **Finishing** tab, set **PDF Output Format** to **Print-Gray (B/W)**.
2. Click **Print**. All colours in text and pictures become shades of grey. The file name ends with **_BW**.

### Print an A5 booklet on A4 paper on an office printer

1. On the **Layout** tab, set the page size to A5.
2. On the **Finishing** tab, in **Booklet Pagination**, set **Pages Per Spread** to **2-up**.
3. Set **Physical Paper Size** to **210mm, 297mm (A4)**.
4. Click **Print**. The new PDF (ending **_2up**) has two pages side by side on each A4 sheet, in booklet order.
5. Print it double-sided. For 2-up, choose "flip on short edge" in your printer settings. Print one or two test sheets first.
6. Fold the stack of sheets in the middle and staple along the fold.

### Use a paper size that is not in the list

1. Click in the **Physical Paper Size** box and type the width and height, separated by a comma. For example: `203mm, 330mm`.
2. You can use mm or in.

### See what changed since the last PDF

1. On the **Finishing** tab, check that **Number of Previous PDFs to be Kept** is at least 1.
2. Tick **Compare PDFs** (or press Ctrl+R).
3. Make your corrections, then click **Print**.
4. The "diff" PDF opens and shows the changes in colour. Untick **Compare PDFs** when you are finished.

### Compare with an older proof, not just the last run

1. In the **Compare PDFs** area, click **Select...** and choose the older PDF.
2. Tick **Compare PDFs** and click **Print**.
3. To go back to comparing with the previous run, click **Select...** again and click **Cancel** in the file dialog.

### Put "DRAFT" on every page

1. In the **PDF Details** area, tick **Apply Watermark PDF**.
2. Click **Select...** next to it. PTXprint opens its own folder of watermarks. Choose the one that matches your page size (for example **A5-Draft.pdf**).
3. Click **Print**.

### Send your settings to someone else inside the PDF

1. Tick **Include Config Settings Within PDF** (it is ticked by default).
2. Click **Print** and send the PDF.
3. The other person can load your settings from that PDF using **Import Settings** (see the chapter on importing settings).

## Common problems

**The colours look different in the printed book from on screen.**
Screens use RGB. Printing presses use CMYK, which cannot show some bright colours. Choose **Print-CMYK** (or the format your printer asks for), click **Print**, and check the result before you send it. Ask the printer for a printed proof if colour is important.

**Making the PDF is now very slow.**
A **PDF Output Format** other than **Screen** needs extra processing, especially for pictures. While you are still editing, use **Screen (Quickest)**. Change to the final format only for the last PDF. Also, **Compare PDFs** adds time, because it renders the pages as images.

**The PDF pages are bigger than my page size.**
**Crop Marks** is ticked. Crop marks add 0.5 inch (about 12.7 mm) on each side of every page. Untick **Crop Marks** if the printer did not ask for them.

**The PDF is two pages per sheet, or the file name ends with _2up.**
**Pages Per Spread** is not set to **1-up (No booklet)**. Set it back to **1-up** for a normal PDF. Commercial printers almost always want single pages (1-up).

**I see a "Paper Size Error" message.**
The book pages do not fit on the **Physical Paper Size** with the chosen **Pages Per Spread**. Choose a larger sheet or fewer pages per spread.

**"Scale to fit" is greyed out.**
It only works with **1-up (No booklet)**. Set **Pages Per Spread** to **1-up**.

**"Sheets Per Signature", "Fold Cut Margin" and "Fold First" are greyed out or missing.**
They are only active when **Pages Per Spread** is 2-up or more, and they are only shown in the **Full** view.

**"Color Hue" and "Tolerance" are greyed out.**
They are only used for **Print-Spot**. Set **PDF Output Format** to **Print-Spot** first.

**Compare PDFs does not show anything, or says there is nothing to compare.**
There must be an older PDF to compare with. Check that **Number of Previous PDFs to be Kept** is at least 1, and click **Print** once without comparing, so that a previous copy exists. If you used **Select...**, check that the chosen file still exists.

**The watermark is missing or in the wrong place.**
The watermark PDF should have the same page size as your book. Choose a file that matches your page size. If the watermark file was moved or deleted, PTXprint warns you that it cannot find it. Click **Select...** again.

**The maps (or other insert pages) are missing from my PDF.**
**Extract Color Inserts** is ticked. These pages were saved as separate PDF files next to the main PDF. Untick it if you want them inside the main PDF.

**Thumb tabs now appear only on odd pages.**
When you chose **Print-CMYK**, **Print-Gray** or **Print-Spot**, PTXprint turned on **Only Show on Odd Pages** for thumb tabs. You can change it back on the **Tabs+Borders** tab.

## Settings reference: Finishing tab

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Finishing tab › Booklet Pagination

#### Physical Paper Size

- **Where:** Finishing tab › Booklet Pagination
- **Type:** Drop-down list
- **Description:** Pagination: Physical paper size
- **View level:** Default and Full views
- **Choices:** 420mm, 594mm (A2); 297mm, 420mm (A3); 210mm, 297mm (A4); 17in, 22in (ANSI C); 11in, 17in (ANSI B); 8.5in, 11in (Letter); 353mm, 500mm (B3); 250mm, 353mm (B4); 176mm, 250mm (B5)

**Tooltip (the text shown when you hover the mouse over it):**

> If the required size is not displayed, then just type the required page width and height separated by a comma.
>
> For example: 203mm, 330mm (Foolscap)
>
> This is the actual size of the sheet of paper on which multiple pages will be printed. For example, if printing an A5-sized booklet, the actual sheet of paper that you print on will be 2x the A5-sized page, which is an A4-sized sheet of paper.

**Explanation:**

The size of the paper that goes into the printer, not the size of the book page. It is only used when **Pages Per Spread** is 2-up or more, or when **Scale to fit** is ticked. For a 2-up booklet, choose a sheet that is twice the book page (A5 book → A4 sheet; Letter-half book → Letter sheet). You can type any size as "width, height", for example `203mm, 330mm`. If the pages do not fit, you get a **Paper Size Error** when you print.

*(Internal ID: `ecb_sheetSize` · Config key: `finishing/sheetsize`)*

#### Pages Per Spread

- **Where:** Finishing tab › Booklet Pagination
- **Type:** Drop-down list
- **Description:** Pagination: Pages per spread (booklet printing)
- **View level:** Default and Full views
- **Choices:** 1-up (No booklet); 2-up; 4-up; 8-up

**Tooltip (the text shown when you hover the mouse over it):**

> How many pages will be printed on one side of the physical paper?
>
> For example, for an A5-sized booklet, 2 pages will fit on each side, making a total of 4 pages on a single sheet.

**Explanation:**

**1-up (No booklet)** makes a normal PDF with one book page on each PDF page. This is what commercial and print-on-demand printers want. **2-up** makes a simple folded booklet that you can print yourself on double-sided paper. **4-up** and **8-up** are for sheets that are folded twice or three times, usually by a print shop. When this is more than 1-up, the PDF file name gets an ending like **_2up**, and the signature settings become active.

*(Internal ID: `fcb_pagesPerSpread` · Config key: `finishing/pgsperspread`)*

#### Scale to fit

- **Where:** Finishing tab › Booklet Pagination
- **Type:** Checkbox (not ticked by default)
- **Description:** Pagination: Scale to fit
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Only available when Pages per Spread is 1-up. Enable this option to scale every page (up or down) so that it fits the Physical Paper Size (set on this tab), centred on the sheet.

**Explanation:**

Only active when **Pages Per Spread** is **1-up**. PTXprint enlarges or shrinks every page so that it fits the **Physical Paper Size**, and centres it on the sheet. Use it, for example, to print an A5 proof on A4 paper with larger text. The book layout does not change; only the final PDF is scaled.

*(Internal ID: `c_scaleToFit` · Config key: `finishing/scaletofit`)*

#### Sheets Per Signature

- **Where:** Finishing tab › Booklet Pagination
- **Type:** Number box
- **Description:** Pagination: Sheets per signature (pages per form)
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> A signature is a collection of pages folded and bound together as a unit. A signature may be made up of multiple sheets.
>
> If unsure, leave this setting at 0 to indicate that the publication will not be bound using separate signatures.

**Explanation:**

How many sheets of paper are folded together into one signature (one group of pages in the book). 0 means the whole book is one group, like a stapled booklet. Only change this if your printer or binder tells you how many sheets they put in each signature. Only active when **Pages Per Spread** is 2-up or more.

*(Internal ID: `s_sheetsPerSignature` · Config key: `finishing/sheetsinsigntr`)*

#### Fold Cut Margin (mm)

- **Where:** Finishing tab › Booklet Pagination
- **Type:** Number box
- **Description:** Pagination: Minimum fold cut margin
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> The minimum width of the area to be cut after folding of the signature. Measured in millimeters (mm).

**Explanation:**

Extra space (in mm) left at the folds of a signature, where the paper will be cut after folding. Only needed for 4-up and 8-up sheets that are folded and then trimmed. Use the value your printer gives you. Leave it at 0 for a simple 2-up booklet.

*(Internal ID: `s_foldCutMargin` · Config key: `finishing/foldcutmargin`)*

#### Fold First

- **Where:** Finishing tab › Booklet Pagination
- **Type:** Checkbox (not ticked by default)
- **Description:** Pagination: Fold First
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> If you are imposing for a printer with a folding machine, then you want to fold first and then cut. This, for example makes a folded sheet that is part of a signature consist of two sets of sequential pages.

**Explanation:**

Changes the page order on the sheet to suit a print shop that folds the sheets first and cuts them after. Leave it unticked unless the printer asks for "fold first". Only active when **Pages Per Spread** is 2-up or more.

*(Internal ID: `c_foldFirst` · Config key: `finishing/foldfirst`)*

#### Create Cover as a Separate PDF

- **Where:** Finishing tab › Booklet Pagination
- **Type:** Checkbox (ticked by default)
- **Description:** Pagination: Create the cover as a stand-alone PDF
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> This option is only available if Create Cover is enabled on the Cover tab. Enable this option if you plan to print the outer (wrapper) cover separately from the book's content. This is often the case if cardstock, or a colour cover is used.

**Explanation:**

Most printers print the cover on different paper (thicker card, or colour) from the inside pages, so they want the cover as its own PDF file. When PTXprint makes a cover, it saves the cover pages in a separate PDF whose name ends with **_cover.pdf**.

*(Internal ID: `c_coverSeparatePDF` · Config key: `cover/makeseparatePDF`)*

### Finishing tab

#### Booklet Pagination

- **Where:** Finishing tab
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Whether you need a simple booklet or a more complex signature, these options allow plenty of scope.

#### Compare PDFs

- **Where:** Finishing tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Create 'diff' to Compare PDFs
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Enable this option to generate a PDF showing the differences between the current PDF and the selected previous version (see 'Compare With a Previous PDF' below).
>
> If any differences are found, it should open the "Diff" PDF in the default PDF viewer.
>
> Shortcut: Ctrl-R

**Explanation:**

When ticked, every **Print** also makes a "diff" PDF that shows the differences between the new PDF and the comparison PDF (see **Select...** in the **Compare PDFs** area). The diff PDF opens automatically. Untick it when you no longer need it, because comparing adds time to each print. When you untick it, PTXprint deletes the old diff file.

*(Internal ID: `c_createDiff`)*

### Finishing tab › Compare PDFs

#### Select...

- **Where:** Finishing tab › Compare PDFs
- **Type:** Button
- **Description:** Compare PDFs: Select previous PDF to compare with
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Select a particular PDF file to be compared against the current output PDF. If you just want to compare output to the previous run, then click Cancel in the File Open dialog to reset the filename (which will then default to _1).

**Explanation:**

By default the comparison is with the previous run (**Previous PDF (_1)**). Use this button to choose a different PDF, such as the proof you sent for checking last month. The label becomes bold to remind you that a special file is selected. Click **Cancel** in the file dialog to go back to the previous run.

*(Internal ID: `btn_selectDiffPDF` · Config key: `document/diffpdf`)*

#### Only Show Pages With Differences

- **Where:** Finishing tab › Compare PDFs
- **Type:** Checkbox (ticked by default)
- **Description:** Compare PDFs: Only show pages with differences
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> When comparing two PDF files the resulting "Diff" PDF can get rather large. This option reduces the size of the PDF by not including any identical pages. This also saves time as you don't need to search through a lengthy PDF to find out what might have changed.

**Explanation:**

Leave this ticked. Then the diff PDF contains only the pages that changed, so it is small and quick to check. Untick it only if you want to see every page, changed or not.

*(Internal ID: `c_onlyDiffs` · Config key: `document/onlyshowdiffs`)*

#### Show New Text or Position in

- **Where:** Finishing tab › Compare PDFs
- **Type:** Colour picker
- **Description:** Compare PDFs:
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Use this color to show anything that has been added (or moved to the current location) in the new PDF.
>
> Set the color to use when differences are found between the old and the new PDFs.
>
> Use this color to show anything that has been added (or moved to the current location) in the new PDF.

**Explanation:**

The colour used in the diff PDF for new things: text that was added, or text that moved to this place. Choose a colour that is easy to tell apart from the **Show Old Text or Position in** colour.

*(Internal ID: `col_ndiffColor` · Config key: `document/ndiffcolor`)*

#### Show Old Text or Position in

- **Where:** Finishing tab › Compare PDFs
- **Type:** Colour picker
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Use this color to show anything that has been deleted (or moved from the previous location) in the old PDF.
>
> Set the color to use when differences are found between the old and the new PDFs.
>
> Use this color to show anything that has been deleted (or moved from the previous location) in the old PDF.

**Explanation:**

The colour used in the diff PDF for old things: text that was removed, or the place where moved text used to be. Choose a colour that is easy to tell apart from the **Show New Text or Position in** colour.

*(Internal ID: `col_odiffColor` · Config key: `document/odiffcolor`)*

#### Show Max Diff Pages

- **Where:** Finishing tab › Compare PDFs
- **Type:** Number box
- **Description:** Compare PDFs: Set maximum diff pages to show
- **View level:** Default and Full views
- **Values:** from 1 to 999, default 20

**Tooltip (the text shown when you hover the mouse over it):**

> The PDF showing differences between the old and the new contains images that make the resulting file rather large. Use this option to limit the number of "Diff" pages created. This will also potentially speed up the process.

**Explanation:**

The highest number of changed pages that are put into the diff PDF. Each diff page is an image, so many pages make a large file and take time. The default of 20 is usually enough. Increase it if you expect many pages to change, for example after a change that moves text across the whole book.

*(Internal ID: `s_diffpages` · Config key: `document/diffpages`)*

### Finishing tab › PDF Details

#### PDF Output Format

- **Where:** Finishing tab › PDF Details
- **Type:** Drop-down list
- **Description:** PDF output format (Screen, RGB, CMYK, B/W, spot)
- **View level:** Default and Full views
- **Choices:** Screen (Quickest); Digital-RGB; Digital-CMYK (Transparency); Print-CMYK; Print-Gray (B/W); Print-Spot

**Tooltip (the text shown when you hover the mouse over it):**

> Select the appropriate standard for the output format to optimize the PDF for its intended purpose.
>
> Screen (fastest, no post processing) Digital-RGB (for screens and local printing, PDF/X-4) Digital-CMYK (CMYK, PDF/X-4) Print-CMYK, Print-Gray (B/W), Print-Spot (for professional printers, PDF/X-1a:2003)
>
> Note: Tick 'Archive' to also comply with the archive standard PDF/A-4.

**Explanation:**

Use **Screen (Quickest)** while you work. Choose the final format only when you make the PDF for the printer: **Print-CMYK** for a printer that asks for PDF/X-1a or CMYK; **Print-Gray (B/W)** for black-ink-only books; **Print-Spot** for black plus one extra ink; **Digital-RGB** for screens, e-books and office printers (PDF/X-4). The non-Screen formats take longer to make, especially with many pictures. Each format adds its own ending to the file name (for example **_CMYK**), so the files do not overwrite each other.

*(Internal ID: `fcb_outputFormat` · Config key: `transparency_`, `snippets/pdfoutput`)*

#### PDF Output Format

- **Where:** Finishing tab › PDF Details
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Select the appropriate standard for the output format to optimize the PDF for its intended purpose.
>
> Screen (fastest, no post processing) Digital-RGB (for screens and local printing, PDF/X-4) Digital-CMYK (CMYK, PDF/X-4) Print-CMYK, Print-Gray (B/W), Print-Spot (for professional printers, PDF/X-1a:2003)
>
> Note: Tick 'Archive' to also comply with the archive standard PDF/A-4.

#### Crop Marks

- **Where:** Finishing tab › PDF Details
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable crop marks
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Some printers require crop marks on the PDF to show where the page should be trimmed after binding.

**Explanation:**

Adds cut marks at the corners of each page. PTXprint makes each PDF page 0.5 inch (about 12.7 mm) larger on every side to make room for them. Only tick this if your printer asks for crop marks; many print-on-demand printers reject files with crop marks because the page size is then wrong. When **Pages Per Spread** is 2-up or more, the marks are drawn on the large sheet instead.

*(Internal ID: `c_cropmarks` · Config key: `paper/cropmarks`)*

#### Number of Previous PDFs to be Kept

- **Where:** Finishing tab › PDF Details
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** default 1

**Tooltip (the text shown when you hover the mouse over it):**

> By default, PTXprint only keeps one previous PDF (named ..._1.pdf). Up to 20 previous versions can be kept. Compare PDFs uses the _1 PDF unless you select another one, so keep at least 1.
>
> By keeping previous versions of the PDF, it is possible to compare the final output of the PDFs. Up to 20 previous versions can be kept.
>
> If you need to keep a PDF around longer, then manually rename it so that it can be compared to at a later date.

**Explanation:**

Before each new PDF is made, PTXprint copies the old one to a file ending **_1.pdf** (and the older ones to **_2.pdf**, **_3.pdf** …). **Compare PDFs** uses the **_1** file, so keep this at 1 or more if you want to compare. Older versions are deleted when the number is reached, so rename a PDF yourself if you must keep it.

*(Internal ID: `s_keepVersions` · Config key: `document/keepversions`)*

#### Include Config Settings Within PDF

- **Where:** Finishing tab › PDF Details
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> All the configuration settings (including the PTXprint styles, AdjLists, changes.txt, and related .tex files) can be included within the PDF in order to maintain a record of what settings were used to create that PDF. Later, these settings can be retrieved from the PDF to set up an identical configuration. This is also a way to share config settings with other users.

**Explanation:**

Stores your configuration (settings, styles, AdjLists, changes and related files) inside the PDF file. The PDF looks the same. It is a good record of how the PDF was made. You or another person can load these settings back with **Import Settings**, choosing the PDF as the source. Leave it ticked unless you have a reason not to share your settings with the PDF.

*(Internal ID: `c_inclSettingsInPDF` · Config key: `document/settingsinpdf`, `finishing/inclsettings`)*

#### Archive (PDF/A-4)

- **Where:** Finishing tab › PDF Details
- **Type:** Checkbox (not ticked by default)
- **Description:** Include unicode text within PDF (to help with archiving)
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Check this option to include the Unicode text in the PDF which is a good practice for final print and long-term archiving. PDF/A-4 is the currently preferred archival format.

**Explanation:**

Makes a PDF that follows the PDF/A-4 archive standard. The text in the PDF can then be searched and copied correctly as Unicode, which is good for long-term storage and for digital libraries. Only tick it if you need an archive PDF; it is not needed for normal printing.

*(Internal ID: `c_printArchive` · Config key: `document/printarchive`)*

#### Color Hue

- **Where:** Finishing tab › PDF Details
- **Type:** Colour picker
- **Description:** Spot color hue
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> If a spot color is needed then select the closest hue. Colors close to this hue are printed with the spot ink; everything else in black/gray. Tell your printer which ink to use.

**Explanation:**

Only active when **PDF Output Format** is **Print-Spot**. Choose the colour (hue) of the spot ink, for example the red used for headings. Text and graphics with a similar colour are printed with the spot ink; everything else becomes black and grey. Tell your printer which ink (for example, which Pantone number) they should use for this colour.

*(Internal ID: `col_spotColor` · Config key: `finishing/spotcolor`)*

#### Tolerance (%)

- **Where:** Finishing tab › PDF Details
- **Type:** Number box
- **Description:** Spot color tolerance
- **View level:** Full view only
- **Values:** default 15

**Tooltip (the text shown when you hover the mouse over it):**

> To match the Spot Color Hue exactly, set this to 0%. If text in similar colors are also to be set to this Spot Color, then select an acceptable tolerance range (suggested default is 15%).
>
> Note that this will include similar colors either side (e.g. -15% to +15%) of the selected hue.

**Explanation:**

Only active when **PDF Output Format** is **Print-Spot**. Sets how close a colour must be to the **Color Hue** to be printed with the spot ink. 0% means only exactly that hue. The default of 15% also catches slightly different shades. Increase it if some coloured items come out grey; decrease it if items that should be grey come out in the spot colour.

*(Internal ID: `s_spotColorTolerance` · Config key: `finishing/spottolerance`, `color/spotcolrange`)*

#### Extract Color Inserts

- **Where:** Finishing tab › PDF Details
- **Type:** Checkbox (not ticked by default)
- **Description:** Extract Color Insert pages (as separate PDFs)
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Extract the special peripheral materials named 'maps' or 'insert_*' as separate PDFs to be printed in color and inserted manually during the binding process.
>
> Note that the cover is always extracted.

**Explanation:**

Takes special pages out of the main PDF and saves them as separate PDF files: maps, and peripheral pages whose name starts with "insert_". The new file names end with the name of the insert, for example **_maps.pdf**. Use this when colour pages are printed separately and added to the book during binding. The extracted pages are removed from the main PDF.

*(Internal ID: `c_extractInserts` · Config key: `finishing/extractinserts`)*

#### Extra XDV Processing

- **Where:** Finishing tab › PDF Details
- **Type:** Checkbox (not ticked by default)
- **Description:** Extra XDV processing (before creating final PDF)
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Enable processing of the intermediate xdv file for such things as coloured diacritics.

**Explanation:**

Runs an extra processing step before the final PDF is made. It is needed only for a few special features, such as coloured diacritics. Leave it unticked unless a feature you use asks for it, because it makes printing slower.

*(Internal ID: `c_extraxdvproc` · Config key: `finishing/extraxdvproc`)*

#### Apply Watermark PDF

- **Where:** Finishing tab › PDF Details
- **Type:** Checkbox (not ticked by default)
- **Description:** Finishing: Apply watermark
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> A watermark can be applied to all pages of the publication. The file must be a PDF and should ideally have the same dimensions as the publication being printed.

**Explanation:**

Adds a watermark PDF behind every page, for example the word "DRAFT" or a copyright notice. This is helpful for proof copies, so that nobody mistakes them for the finished book. Untick it before you make the final PDF for the printer. The watermark PDF should have the same page size as your book.

*(Internal ID: `c_applyWatermark` · Config key: `paper/ifwatermark`)*

#### Select...

- **Where:** Finishing tab › PDF Details
- **Type:** Button
- **Description:** Finishing: Select watermark to apply
- **View level:** Default and Full views
- **Only available when:** “Apply Watermark PDF” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Choose the watermark PDF file. It should ideally be the same size as the book page.

**Explanation:**

Only active when **Apply Watermark PDF** is ticked. Opens PTXprint's own folder of ready-made watermarks (for example **A4-Draft.pdf**, **A5-Draft.pdf**, **A5-CopyrightWatermark.pdf**). Choose one that matches your page size, or choose your own one-page PDF from anywhere on your computer.

*(Internal ID: `btn_selectWatermarkPDF` · Config key: `paper/watermarkpdf`)*
