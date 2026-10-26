# 18. Finishing tab

## 18.1 What this tab is for

The **Finishing** tab controls what happens to the PDF *after* the pages are typeset. Come here when you prepare the book for a printer, or want to print it yourself as a folded booklet.

On this tab you can:

* choose the **PDF Output Format** your printer asks for (for example CMYK or black and white);
* add **crop marks** and a **watermark** (such as the word "DRAFT");
* print the pages as a **booklet** (two or more pages on each sheet, in the right order for folding);
* **compare** the new PDF with an older one, to see exactly what changed;
* keep older copies of the PDF, and store your settings inside the PDF.

The tab is shown in the **Basic**, **Regular** and **Full** views. In **Basic** it shows only the booklet (pages per sheet) settings and **Compare PDFs**; more settings appear in **Regular**, and some only in **Full**.

Most settings here do not change the text layout, only the finished PDF file. Click **Print** (make the PDF again) to see a change.

### Some print-shop words in simple terms

* **Trim size** – the size of the finished book page, after the printer cuts it. In PTXprint this is the **Page Size** on the **Layout** tab.
* **Crop marks** (also called trim marks) – thin lines in the corners, outside the page, that show the printer where to cut.
* **Bleed** – a picture or colour that goes right to the edge of the page. It must go a little *past* the cut line (usually about 3 mm), so that no white strip shows if the cut is not exact.
* **RGB** – the colours used by screens (Red, Green, Blue).
* **CMYK** – the four inks used by most colour printing presses (Cyan, Magenta, Yellow and blacK). Many printers ask for CMYK files.
* **Grayscale (B/W)** – only black ink, in shades of grey.
* **Spot colour** – one extra, ready-mixed ink (often a Pantone colour) used in addition to black, for example red for the words of Jesus or for headings.
* **PDF/X** – a type of PDF made for printing. It contains everything the printer needs (fonts, colour information) and nothing that could cause problems.
  * **PDF/X-1a** – the older, strict type. All colours must be CMYK (or grey/spot) and there may be no transparency (see-through effects). Many printing presses still ask for this.
  * **PDF/X-4** – the newer type. It allows RGB colours with colour profiles and transparency. Many modern and digital (print-on-demand) printers accept it.
* **PDF/A** – a type of PDF made for keeping documents for a very long time (archiving).
* **Imposition** – arranging several book pages on one large sheet, so that after folding and cutting the pages come out in the right order.
* **Signature** – a group of sheets that are folded together and sewn or glued into the book as one unit.

If your printer gives you a list of requirements, look for: trim size, bleed, crop marks (yes or no), colour (CMYK, grey, or RGB), and PDF type (PDF/X-1a or PDF/X-4). Set these on the **Layout** tab and on this tab. If you are not sure, ask the printer for a sample "print-ready PDF specification".

## 18.2 PDF Details

This area sets the type of PDF that PTXprint makes. (Shown in the **Regular** and **Full** views; some settings only in **Full**.)

### PDF Output Format

Choose the format that matches how the book will be used:

* **Screen (Quickest)** – the normal choice while you work on the book. No extra processing. Use it for checking and proof-reading.
* **Digital-RGB** – PDF/X-4 in RGB colours. For reading on screen, sharing as an e-book, and printing on an office or home printer.
* **Digital-CMYK (Transparency)** – PDF/X-4 for printers who want CMYK but accept transparency.
* **Print-CMYK** – PDF/X-1a with all colours turned into CMYK. For a commercial printing press that asks for PDF/X-1a or CMYK.
* **Print-Gray (B/W)** – PDF/X-1a in black and shades of grey only, for a book printed only in black ink. Coloured text and pictures become grey.
* **Print-Spot** – black plus one spot colour. Colours close to the **Color Hue** are printed with the spot ink; everything else in black and grey. **Color Hue** and **Tolerance (%)** are only active with this format.

Formats other than **Screen** need extra processing after the PDF is made. This takes more time, especially with many pictures. The status bar shows a note about this.

PTXprint adds an ending to the PDF file name to show the format: **_RGB**, **_CMYK-Transparent**, **_CMYK**, **_BW** or **_Spot**. **Screen** adds nothing. So the files do not overwrite each other.

With **Print-CMYK**, **Print-Gray** or **Print-Spot**, if thumb tabs are on, PTXprint turns on **Only Show on Odd Pages** for the thumb tabs (on the **Tabs+Borders** tab) and tells you in the status bar.

### Other PDF settings

* **Crop Marks** adds cut lines around every page. To make room, each PDF page becomes 0.5 inch (about 12.7 mm) larger on every side. Only turn this on if your printer asks for crop marks. Many print-on-demand printers do *not* want them.
* **Number of Previous PDFs to be Kept** keeps older copies of your PDF (with **_1**, **_2** … at the end of the name).
* **Include Config Settings Within PDF** stores your settings inside the PDF, so they can be loaded back with **Import Settings**.
* **Archive (PDF/A-4)** makes a PDF that is better for long-term storage. (Only in the **Full** view.)
* **Extract Color Inserts** and **Extra XDV Processing** are special tools. (Only in the **Full** view.)
* **Apply Watermark PDF** puts a PDF (for example "DRAFT") on every page.

## 18.3 Booklet Pagination

Print several book pages on one larger sheet, arranged so that you can fold the sheets into a booklet (imposition). (Shown in the **Basic**, **Regular** and **Full** views; some settings only in **Full**.)

* **Pages Per Spread** – how many book pages go on *one side* of a sheet.
* **Physical Paper Size** – the size of the sheet you print on.
* **Sheets Per Signature**, **Fold Cut Margin (mm)** and **Fold First** are for professional binding. Leave them at their starting values unless the printer tells you what to use.

When **Pages Per Spread** is more than 1-up:

* the signature settings become active;
* **Scale to fit** is greyed out;
* the **Finishing** tab label changes colour, to remind you that the PDF will be imposed;
* the PDF file name gets an extra ending, such as **_2up**;
* crop marks (if ticked) are drawn on the large sheet, not on each page.

If the pages do not fit on the chosen paper, PTXprint shows a **Paper Size Error**. Choose a larger **Physical Paper Size** or fewer pages per spread.

## 18.4 Compare PDFs

This makes a "diff" PDF that shows what changed between the new PDF and an older one. It is very useful after a late correction, to check that only the expected pages changed.

**Compare PDFs**, **Select...**, **Only Show Pages With Differences** and **Show Max Diff Pages** are shown in the **Regular** and **Full** views. The colours (**New Text**, **Old Text**), **Ignore When Comparing** (**Headers + Footers**, **Side Margins**), **Start Page Offset** and **Smart Check** are only in the **Full** view.

How it works:

1. While **Compare PDFs** is ticked, PTXprint always keeps the previous PDF (ending **_1.pdf**), even if **Number of Previous PDFs to be Kept** is 0.
2. On **Print**, PTXprint makes the new PDF and compares it, page by page, with the old one. By default that is the previous PDF (**Previous PDF (_1)**). Click **Select...** to compare with any other PDF, for example the one you sent for the last proof check.
3. If it finds differences, it makes a file ending **_diff.pdf**. A **Diff** tab appears in the PDF Preview window (if you use your own PDF program, the diff PDF opens there). Each diff page is a picture of the new page with the changes in colour: added (or moved-in) things in the **New Text** colour (blue at first); removed (or moved-away) things in the **Old Text** colour (red at first).
4. If no diff PDF is made, the status line at the bottom of the window says why, and the message stays there. For example: **No differences found**, or **Nothing to compare with yet: make a change and print again** (no previous PDF yet). See **Common problems** for the other messages.

What PTXprint compares:

* Only the finished page (the trim size). Crop marks and bleed are left out, so a PDF with crop marks and the same PDF without them are the same.
* Very tiny differences (a speck, or a letter moved a small fraction of a pixel) are not counted.
* If one PDF has more pages, the extra pages are compared with an empty page, so they count as differences.
* Both PDFs must have the same page size. If not, PTXprint shows an error and the status line says **Cannot compare PDFs: the pages are different sizes**.

Options for special cases (only in the **Full** view):

* **Start Page Offset** – use this when the two PDFs do not start on the same page, for example when one has a cover or an extra front matter page. Otherwise every page is compared with the wrong one, and everything looks different. A positive number skips pages at the start of the **old** PDF; a negative number skips pages at the start of the **new** PDF. Normally 0.
* **Ignore When Comparing: Headers + Footers** – compares only the area between the top and bottom margins, so running headers, footers and page numbers are not compared. Use it when you only care about the text, for example after you changed the header layout.
* **Ignore When Comparing: Side Margins** – compares only the area of the text columns, so margin notes, side references and thumb tabs are not compared.
* The ignored areas are shaded grey in the diff PDF. These two options are not used when **Pages Per Spread** is more than 1-up, or when **Scale to fit** is ticked, because the pages have then moved on the sheet.
* **Smart Check** – use it after you changed only the margins (for example added a binding gutter, or moved the text block up or down), not the text. Normally every line would then show as different, because it moved. With **Smart Check**, PTXprint first lines up each old page with the new one, and then shows only real changes: changed words, different line breaks, and so on. If the text block changed size, lines break differently, and those changes are still shown. On a page that had to be moved, **Smart Check** is a little less sensitive, so a very small change (such as a comma in place of a full stop) may not be shown.

## 18.5 Common tasks

### Make a PDF for a commercial printer who asks for PDF/X-1a in CMYK

1. On the **Layout** tab, check that the **Page Size** is the trim size the printer wants.
2. On the **Finishing** tab, in the **PDF Details** area, set **PDF Output Format** to **Print-CMYK**.
3. Tick **Crop Marks** only if the printer asks for them.
4. Make sure **Pages Per Spread** is **1-up (No booklet)**. Printers do their own imposition.
5. Click **Print**. The new PDF name ends with **_CMYK**.

### Make a black-and-white PDF for printing

1. Set **PDF Output Format** to **Print-Gray (B/W)**.
2. Click **Print**. The file name ends with **_BW**.

### Print an A5 booklet on A4 paper on an office printer

1. On the **Layout** tab, set the page size to A5.
2. On the **Finishing** tab, in **Booklet Pagination**, set **Pages Per Spread** to **2-up**.
3. Set **Physical Paper Size** to **210mm, 297mm (A4)**.
4. Click **Print**. The new PDF (ending **_2up**) has two pages side by side on each A4 sheet, in booklet order.
5. Print it double-sided. For 2-up, choose "flip on short edge" in your printer settings. Print one or two test sheets first.
6. Fold the stack of sheets in the middle and staple along the fold.

### Use a paper size that is not in the list

Click in the **Physical Paper Size** box and type the width and height, separated by a comma, in mm or in. For example: `203mm, 330mm`.

### See what changed since the last PDF

1. Tick **Compare PDFs** (or press Ctrl+R).
2. Make your corrections, then click **Print**.
3. If there are changes, the **Diff** tab in the PDF Preview shows them in colour. If not, the status line says **No differences found**.
4. Untick **Compare PDFs** when you are finished.

### Compare with an older proof, not just the last run

1. In the **Compare PDFs** area, click **Select...** and choose the older PDF.
2. Tick **Compare PDFs** and click **Print**.
3. If the older PDF has more (or fewer) pages at the start, for example a cover, set **Start Page Offset** so that the pages line up (**Full** view).
4. To go back to comparing with the previous run, click **Select...** again and click **Cancel** in the file dialog.

### Check that only the margins changed, not the text

1. Change to the **Full** view.
2. In the **Compare PDFs** area, tick **Smart Check**. If you also changed the headers or footers, tick **Headers + Footers** under **Ignore When Comparing**.
3. Tick **Compare PDFs** and click **Print**.
4. Only pages where the words or the line breaks changed are shown in the diff PDF.

### Put "DRAFT" on every page

1. In the **PDF Details** area, tick **Apply Watermark PDF**.
2. Click **Select...** next to it and choose the watermark that matches your page size (for example **A5-Draft.pdf**).
3. Click **Print**.

### Send your settings to someone else inside the PDF

1. Tick **Include Config Settings Within PDF** (ticked by default).
2. Click **Print** and send the PDF.
3. The other person loads your settings from that PDF with **Import Settings** (see the chapter on importing settings).

## 18.6 Common problems

**The colours look different in the printed book from on screen.**
Screens use RGB. Printing presses use CMYK, which cannot show some bright colours. Choose **Print-CMYK** (or the format your printer asks for), click **Print**, and check the result before you send it. Ask the printer for a printed proof if colour is important.

**Making the PDF is now very slow.**
Formats other than **Screen** need extra processing, especially for pictures. Use **Screen (Quickest)** while editing, and the final format only for the last PDF. **Compare PDFs** also adds time, because it renders the pages as images.

**The PDF pages are bigger than my page size.**
**Crop Marks** is ticked: it adds 0.5 inch (about 12.7 mm) on each side of every page. Untick it if the printer did not ask for crop marks.

**The PDF is two pages per sheet, or the file name ends with _2up.**
Set **Pages Per Spread** back to **1-up (No booklet)** for a normal PDF. Commercial printers almost always want single pages (1-up).

**I see a "Paper Size Error" message.**
The book pages do not fit on the **Physical Paper Size** with the chosen **Pages Per Spread**. Choose a larger sheet or fewer pages per spread.

**"Scale to fit" is greyed out.**
It only works with **1-up (No booklet)**. Set **Pages Per Spread** to **1-up**.

**"Sheets Per Signature", "Fold Cut Margin" and "Fold First" are greyed out or missing.**
They are only active when **Pages Per Spread** is 2-up or more, and only shown in the **Full** view.

**"Color Hue" and "Tolerance" are greyed out.**
Set **PDF Output Format** to **Print-Spot** first.

**Compare PDFs does not show a diff PDF.**
The status line at the bottom of the window says what happened:

* **No differences found** – the two PDFs look the same.
* **Nothing to compare with yet: make a change and print again** – there is no previous PDF yet. Click **Print** once more; from then on there is one.
* **Cannot find the PDF to compare with: ...** – the file you chose with **Select...** is not there any more. Choose it again.
* **Cannot compare PDFs: the pages are different sizes** – the page size changed (for example on the **Layout** tab). Only pages of the same size can be compared.
* **No pages could be compared. Check the Start Page Offset** – the offset skips more pages than one of the PDFs has. Make it smaller.
* **No differences found, but the old Diff PDF is open and cannot be removed** – close the old diff PDF in your PDF program.

If the chosen comparison PDF is missing, PTXprint goes back to **Previous PDF (_1)** (when the configuration opens, when you tick **Compare PDFs**, or when you print) and says so in the status line.

**Every page shows as changed in the diff PDF.**
The pages are probably not lined up. If one PDF has an extra page at the start (for example a cover), set **Start Page Offset**. If you changed only the margins or the gutter, tick **Smart Check**. If only the headers, footers or page numbers changed, tick **Headers + Footers** under **Ignore When Comparing**. (These options are in the **Full** view.)

**The extra pages at the end show as changed.**
This is correct: extra pages are compared with an empty page.

**The watermark is missing or in the wrong place.**
Choose a watermark PDF with the same page size as your book. If the watermark file was moved or deleted, PTXprint warns you that it cannot find it. Click **Select...** again.

**The maps (or other insert pages) are missing from my PDF.**
**Extract Color Inserts** is ticked, so these pages were saved as separate PDF files next to the main PDF. Untick it to keep them in the main PDF.

**Thumb tabs now appear only on odd pages.**
Choosing **Print-CMYK**, **Print-Gray** or **Print-Spot** turned on **Only Show on Odd Pages** for thumb tabs. You can change it back on the **Tabs+Borders** tab.

## 18.7 Settings reference

### Finishing

#### Booklet Pagination

Label · Basic+

> Whether you need a simple booklet or a more complex signature, these options allow plenty of scope.

#### Compare PDFs

Checkbox, off · Basic+ · `c_createDiff`  
Also: Create 'diff' to Compare PDFs

> Enable this option to generate a PDF showing the differences between the current PDF and the selected previous version (see 'Compare With a Previous PDF' below).
>
> If any differences are found, it should open the "Diff" PDF in the default PDF viewer.
>
> Shortcut: Ctrl-R

See "Compare PDFs" in this chapter. If no differences are found, the status line says why. Untick it when you no longer need it, because comparing adds time to each print. Unticking it hides the **Diff** tab in the preview.

#### Booklet Pagination

##### Physical Paper Size – Pagination: Physical paper size

Drop-down · Basic+ · `ecb_sheetSize` · cfg `finishing/sheetsize`  
Choices: 420mm, 594mm (A2) | 297mm, 420mm (A3) | 210mm, 297mm (A4) | 17in, 22in (ANSI C) | 11in, 17in (ANSI B) | 8.5in, 11in (Letter) | 353mm, 500mm (B3) | 250mm, 353mm (B4) | 176mm, 250mm (B5)

> If the required size is not displayed, then just type the required page width and height separated by a comma.
>
> For example: 203mm, 330mm (Foolscap)
>
> This is the actual size of the sheet of paper on which multiple pages will be printed. For example, if printing an A5-sized booklet, the actual sheet of paper that you print on will be 2x the A5-sized page, which is an A4-sized sheet of paper.

The paper that goes into the printer, not the book page. Only used when **Pages Per Spread** is 2-up or more, or when **Scale to fit** is ticked. For a 2-up booklet, choose a sheet twice the book page (A5 book → A4 sheet; Letter-half book → Letter sheet). Units can be mm or in. If the pages do not fit, you get a **Paper Size Error** when you print.

##### Pages Per Spread – Pagination: Pages per spread (booklet printing)

Drop-down · Basic+ · `fcb_pagesPerSpread` · cfg `finishing/pgsperspread`  
Choices: 1-up (No booklet) | 2-up | 4-up | 8-up

> How many pages will be printed on one side of the physical paper?
>
> For example, for an A5-sized booklet, 2 pages will fit on each side, making a total of 4 pages on a single sheet.

**1-up (No booklet)** is a normal PDF, one book page per PDF page; commercial and print-on-demand printers want this. **2-up** is a simple folded booklet (for example A5 pages on A4) that you can print yourself double-sided. **4-up** and **8-up** are for sheets folded two or three times, usually by a print shop. Above 1-up, the file name gets an ending like **_2up** and the signature settings become active.

##### Scale to fit

Checkbox, off · Regular+ · `c_scaleToFit` · cfg `finishing/scaletofit`  
Also: Pagination: Scale to fit

> Only available when Pages per Spread is 1-up. Enable this option to scale every page (up or down) so that it fits the Physical Paper Size (set on this tab), centred on the sheet.

Use it, for example, to print an A5 proof on A4 paper with larger text. The book layout does not change; only the final PDF is scaled.

##### Sheets Per Signature – Pagination: Sheets per signature (pages per form)

Number · Full · `s_sheetsPerSignature` · cfg `finishing/sheetsinsigntr`

> A signature is a collection of pages folded and bound together as a unit. A signature may be made up of multiple sheets.
>
> If unsure, leave this setting at 0 to indicate that the publication will not be bound using separate signatures.

0 means the whole book is one group, like a stapled booklet. Only change it if your printer or binder tells you how many sheets go in each signature. Only active when **Pages Per Spread** is 2-up or more.

##### Fold Cut Margin (mm) – Pagination: Minimum fold cut margin

Number · Full · `s_foldCutMargin` · cfg `finishing/foldcutmargin`

> The minimum width of the area to be cut after folding of the signature. Measured in millimeters (mm).

Only needed for 4-up and 8-up sheets that are folded and then trimmed. Use the value your printer gives you. Leave it at 0 for a simple 2-up booklet.

##### Fold First

Checkbox, off · Full · `c_foldFirst` · cfg `finishing/foldfirst`  
Also: Pagination: Fold First

> If you are imposing for a printer with a folding machine, then you want to fold first and then cut. This, for example makes a folded sheet that is part of a signature consist of two sets of sequential pages.

Changes the page order on the sheet. Leave it unticked unless the printer asks for "fold first". Only active when **Pages Per Spread** is 2-up or more.

##### Create Cover as a Separate PDF

Checkbox, on · Full · `c_coverSeparatePDF` · cfg `cover/makeseparatePDF`  
Also: Pagination: Create the cover as a stand-alone PDF

> This option is only available if Create Cover is enabled on the Cover tab. Enable this option if you plan to print the outer (wrapper) cover separately from the book's content. This is often the case if cardstock, or a colour cover is used.

The cover file name ends with **_cover.pdf**. Printers often print the cover on different paper (thicker card, or colour) from the inside pages.

#### Compare PDFs

##### Select...

Button · Basic+ · `btn_selectDiffPDF` · cfg `document/diffpdf`  
Also: Compare PDFs: Select previous PDF to compare with

> Select a particular PDF file to be compared against the current output PDF. If you just want to compare output to the previous run, then click Cancel in the File Open dialog to reset the filename (which will then default to _1).

Use it to compare with, for example, the proof you sent for checking last month. The label becomes bold while a special file is selected. If the chosen file is later moved or deleted, PTXprint goes back to **Previous PDF (_1)** by itself and says so in the status line. The two PDFs must have the same page size.

##### Only Show Pages With Differences

Checkbox, on · Basic+ · `c_onlyDiffs` · cfg `document/onlyshowdiffs`  
Also: Compare PDFs: Only show pages with differences

> When comparing two PDF files the resulting "Diff" PDF can get rather large. This option reduces the size of the PDF by not including any identical pages. This also saves time as you don't need to search through a lengthy PDF to find out what might have changed.

Leave it ticked, so the diff PDF is small and quick to check. Untick it only to see every page.

##### Compare PDFs:

Colour · Full · `col_ndiffColor` · cfg `document/ndiffcolor`

> Use this color to show anything that has been added (or moved to the current location) in the new PDF.

Blue at first. Choose a colour that is easy to tell apart from the **Old Text** colour.

##### New Text

Label · Full · `l_ndiffNew`  
Also: Compare PDFs: Colour of new text

> Set the color to use when differences are found between the old and the new PDFs.
>
> Use this color to show anything that has been added (or moved to the current location) in the new PDF.

Label for the new-text colour button above it.

##### Use this color to show anything that has been deleted (or mo...

Colour · Full · `col_odiffColor` · cfg `document/odiffcolor`

> Use this color to show anything that has been deleted (or moved from the previous location) in the old PDF.

Also marks the place where moved text used to be. Red at first. Choose a colour that is easy to tell apart from the **New Text** colour.

##### Show Max Diff Pages – Compare PDFs: Set maximum diff pages to show

Number · Regular+ · `s_diffpages` · cfg `document/diffpages`  
Values: 1–999 (default 20)

> The PDF showing differences between the old and the new contains images that make the resulting file rather large. Use this option to limit the number of "Diff" pages created. This will also potentially speed up the process.

Each diff page is an image, so many pages make a large file and take time. Increase it if you expect many pages to change, for example after a change that moves text across the whole book.

##### Headers + Footers

Checkbox, off · Full · `c_diffIgnoreHeadFoot` · cfg `document/diffignoretopbottom`  
Also: Compare PDFs: Ignore headers and footers

> Only compare the text area of each page, and ignore the margins above and below it: running headers, footers and page numbers.
>
> The ignored areas are shaded in the "Diff" PDF.

The margin sizes come from the **Layout** tab. Use it when the header or footer changed on every page but you only want to see text changes. Not used when **Pages Per Spread** is more than 1-up or **Scale to fit** is ticked.

##### Side Margins

Checkbox, off · Full · `c_diffIgnoreSides` · cfg `document/diffignoresides`  
Also: Compare PDFs: Ignore margin notes and thumb tabs

> Only compare the text area of each page, and ignore the margins to the left and right of it:  
> margin notes and references, thumb tabs, etc.
>
> The ignored areas are shaded in the "Diff" PDF.

PTXprint uses the place where the text columns actually are on each page of the new PDF. Ignored areas are shaded grey. Not used when **Pages Per Spread** is more than 1-up or **Scale to fit** is ticked.

##### Start Page Offset – Compare PDFs: Page offset

Number · Full · `s_diffOffset` · cfg `document/diffoffset`  
Values: -999–999

> If the two PDFs do not start on the same page (for example one has a cover or extra front matter), then pages would be compared with the wrong ones. Use this to line them up.
>
> A positive number skips that many pages at the start of the older PDF. A negative number skips that many pages at the start of the new PDF.

Example: the old proof had a cover page and the new PDF does not. Page 2 of the old PDF must then be compared with page 1 of the new one, so set 1. If the **new** PDF has the extra page, use -1. If no pages are left to compare, the status line says **No pages could be compared. Check the Start Page Offset**.

##### Smart Check

Checkbox, off · Full · `c_diffSmart` · cfg `document/diffsmart`  
Also: Compare PDFs: Smart Check (ignore a moved text block)

> Compare the text, not where it sits on the page.
>
> Use this when the margins have been changed but the text itself has not. For example, a binding gutter has been added and the left and right margins reduced so that the text block stays the same size. Or the top margin has been increased and the bottom margin reduced by the same amount.
>
> Normally everything on the page would show up as different because it has all moved. With Smart Check, each page of the old PDF is first moved to line up with the new one (left and right pages can move in opposite directions), so only real differences are shown: changed wording, different line breaks, etc.
>
> If the text block has changed size then the lines will wrap differently, and those differences are still shown.
>
> Note: on a page that had to be moved, Smart Check is a little less sensitive than a normal comparison, so a very small change (such as one comma replacing a full stop) might not be reported.

Page numbers and headers that did not move are still matched where they were. Leave it unticked for a normal comparison, because on a page that had to be moved a very small change (such as one comma) may be missed. See "Compare PDFs" in this chapter.

##### Old Text

Label · Full · `l_ndiffOld`  
Also: Compare PDFs: Colour of old text

> Set the color to use when differences are found between the old and the new PDFs.
>
> Use this color to show anything that has been deleted (or moved from the previous location) in the old PDF.

Label for the colour button above it, used for removed (or moved-away) text. (Its tooltip wrongly describes the colour for *new* text.)

#### PDF Details

##### PDF Output Format – PDF output format (Screen, RGB, CMYK, B/W, spot)

Drop-down · Regular+ · `fcb_outputFormat` · cfg `snippets/pdfoutput`  
Choices: Screen (Quickest) | Digital-RGB | Digital-CMYK (Transparency) | Print-CMYK | Print-Gray (B/W) | Print-Spot

> Select the appropriate standard for the output format to optimize the PDF for its intended purpose.
>
> Screen (fastest, no post processing) Digital-RGB (for screens and local printing, PDF/X-4) Digital-CMYK (CMYK, PDF/X-4) Print-CMYK, Print-Gray (B/W), Print-Spot (for professional printers, PDF/X-1a:2003)
>
> Note: Tick 'Archive' to also comply with the archive standard PDF/A-4.

Use **Screen (Quickest)** while you work, and the final format only for the printer's PDF. See "PDF Output Format" in this chapter for each choice.

##### PDF Output Format

Label · Regular+

> Select the appropriate standard for the output format to optimize the PDF for its intended purpose.
>
> Screen (fastest, no post processing) Digital-RGB (for screens and local printing, PDF/X-4) Digital-CMYK (CMYK, PDF/X-4) Print-CMYK, Print-Gray (B/W), Print-Spot (for professional printers, PDF/X-1a:2003)
>
> Note: Tick 'Archive' to also comply with the archive standard PDF/A-4.

##### Crop Marks

Checkbox, off · Regular+ · `c_cropmarks` · cfg `paper/cropmarks`  
Also: Enable crop marks

> Some printers require crop marks on the PDF to show where the page should be trimmed after binding.

Many print-on-demand printers reject files with crop marks, because the page size is then wrong. With **Pages Per Spread** at 2-up or more, the marks are drawn on the large sheet.

##### Number of Previous PDFs to be Kept

Number · Regular+ · `s_keepVersions` · cfg `document/keepversions`

> By default, PTXprint only keeps one previous PDF (named ..._1.pdf). Up to 20 previous versions can be kept. Compare PDFs uses the _1 PDF unless you select another one, so keep at least 1.
>
> By keeping previous versions of the PDF, it is possible to compare the final output of the PDFs. Up to 20 previous versions can be kept.
>
> If you need to keep a PDF around longer, then manually rename it so that it can be compared to at a later date.

Before each new PDF, the old one is copied to **_1.pdf** (older ones to **_2.pdf**, **_3.pdf** …). While **Compare PDFs** is ticked, the **_1** file is kept even if this is 0. Versions beyond the number are deleted, so rename a PDF yourself if you must keep it.

##### Include Config Settings Within PDF

Checkbox, on · Regular+ · `c_inclSettingsInPDF` · cfg `document/settingsinpdf`, `finishing/inclsettings`

> All the configuration settings (including the PTXprint styles, AdjLists, changes.txt, and related .tex files) can be included within the PDF in order to maintain a record of what settings were used to create that PDF. Later, these settings can be retrieved from the PDF to set up an identical configuration. This is also a way to share config settings with other users.

The PDF looks the same. To load the settings back, use **Import Settings** with the PDF as the source. Leave it ticked unless you do not want to share your settings with the PDF.

##### Archive (PDF/A-4)

Checkbox, off · Full · `c_printArchive` · cfg `document/printarchive`  
Also: Include unicode text within PDF (to help with archiving)

> Check this option to include the Unicode text in the PDF which is a good practice for final print and long-term archiving. PDF/A-4 is the currently preferred archival format.

The PDF text can then be searched and copied correctly as Unicode, which helps digital libraries. Not needed for normal printing.

##### Color Hue – Spot color hue

Colour · Full · `col_spotColor` · cfg `finishing/spotcolor`

> If a spot color is needed then select the closest hue. Colors close to this hue are printed with the spot ink; everything else in black/gray. Tell your printer which ink to use.

For example the red used for headings. Tell your printer which ink (for example which Pantone number) to use for this colour. Only active with **Print-Spot**.

##### Tolerance (%) – Spot color tolerance

Number · Full · `s_spotColorTolerance` · cfg `finishing/spottolerance`, `color/spotcolrange`

> To match the Spot Color Hue exactly, set this to 0%. If text in similar colors are also to be set to this Spot Color, then select an acceptable tolerance range (suggested default is 15%).
>
> Note that this will include similar colors either side (e.g. -15% to +15%) of the selected hue.

Increase it if some coloured items come out grey; decrease it if items that should be grey come out in the spot colour. Only active with **Print-Spot**.

##### Extract Color Inserts

Checkbox, off · Full · `c_extractInserts` · cfg `finishing/extractinserts`  
Also: Extract Color Insert pages (as separate PDFs)

> Extract the special peripheral materials named 'maps' or 'insert_*' as separate PDFs to be printed in color and inserted manually during the binding process.
>
> Note that the cover is always extracted.

The new files end with the insert name, for example **_maps.pdf**. The extracted pages are removed from the main PDF. Use it when colour pages are printed separately and added during binding.

##### Extra XDV Processing

Checkbox, off · Full · `c_extraxdvproc` · cfg `finishing/extraxdvproc`  
Also: Extra XDV processing (before creating final PDF)

> Enable processing of the intermediate xdv file for such things as coloured diacritics.

Leave it unticked unless a feature you use needs it, because it makes printing slower.

##### Apply Watermark PDF

Checkbox, off · Regular+ · `c_applyWatermark` · cfg `paper/ifwatermark`  
Also: Finishing: Apply watermark

> A watermark can be applied to all pages of the publication. The file must be a PDF and should ideally have the same dimensions as the publication being printed.

For example "DRAFT" or a copyright notice, so that nobody mistakes a proof for the finished book. Untick it before you make the final PDF for the printer.

##### Select...

Button · Regular+ · `btn_selectWatermarkPDF` · cfg `paper/watermarkpdf`  
Also: Finishing: Select watermark to apply · Needs: “Apply Watermark PDF”

> Choose the watermark PDF file. It should ideally be the same size as the book page.

Opens PTXprint's own folder of ready-made watermarks (for example **A4-Draft.pdf**, **A5-Draft.pdf**, **A5-CopyrightWatermark.pdf**). Choose one that matches your page size, or your own one-page PDF from anywhere on your computer.
