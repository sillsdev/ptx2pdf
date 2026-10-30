## What this window is for

The **PDF Preview** window shows the PDF that PTXprint has just made. It opens by itself after you click **Print**. Use it to:

* read through the pages, one page or two facing pages (a "spread") at a time;
* find layout problems quickly (for example pages that are not full, or words with too much space between them);
* fix small layout problems on the page: right-click a paragraph to make it one line shorter or longer, or right-click a picture to move it or change its size;
* run the **Auto Page Fill** tool, which tries to make every page full by itself.

It is a separate window that you can keep open beside the main window. Changes made here are saved with the current configuration.

In this chapter, "pt" means point (about 0.35 mm). "em" is a width equal to the text size; in 10 pt text, 1 em is 10 pt.

## Opening and closing the Preview window

* The window opens after each **Print** if the main menu (☰) > **Show PDF** is set to **Preview Pane** (the normal setting). With **System Viewer** the PDF opens in your normal PDF program instead; with **Output Folder**, PTXprint opens the folder that holds the PDF.
* Closing the window with its **X** button only hides it. It comes back the next time you print.
* **Show main PTXprint settings** (**Alt+S**) brings the main window to the front.
* The title bar shows the PDF file name and the date and time it was made. Check this to be sure you see the newest PDF.

The preview has tabs down the left side. **Content** shows your main PDF. **Cover** shows the cover PDF, if you made one. **Diff** shows the comparison PDF, if you used **Compare PDFs** (on the **Finishing** tab) and differences were found. If there was nothing to compare with, or no differences, there is no **Diff** tab: the preview shows the new PDF, and the status line in the main window says why. **Reference** shows reference documents such as the Ornaments Catalogue. Tabs without a PDF are hidden.

## Moving around: pages, spreads and zoom

The navigation controls are in the top bar.

* **First**, **Previous**, **Next** and **Last** move through the PDF; in **Book View** by a whole spread.
* The page box shows the printed page number. Type a number and press **Enter** to jump there.
* The label next to the page box shows the page count. "(15)+52" means 15 front pages (before page 1) and 52 numbered pages.
* Keyboard: **Left/Right arrow** or **Page Up/Page Down** change page. **Ctrl+Home** and **Ctrl+End** go to the first and last page.
* Mouse: the wheel changes page; when zoomed in, it scrolls the page instead. Drag with the middle mouse button to move the page around.
* Zoom: the **Zoom** box, **Ctrl+mouse wheel** (zooms at the mouse pointer), **Ctrl+Plus** and **Ctrl+Minus**. **Ctrl+F**, **Ctrl+0** or **Zoom Fit to Screen** fit the whole page (or spread) in the window.
* For right-to-left books, the arrow buttons and keys are reversed to follow the book.

**Book View** (Ctrl+B) shows two facing pages side by side, as in a printed book. Page 1 is shown alone because it is a right-hand page; then 2+3, 4+5 and so on. Use it to check that facing pages look balanced.

The **Contents** list on the left shows the PDF bookmarks (books, and often chapters). Double-click a line to jump to that page.

## The Content tab: what to show on the preview

These options only change the preview, not the PDF.

* **Adjustments** draws coloured bars on the edges of adjusted paragraphs. **Left** edge = shrunk; **right** edge = expanded. **Blue** = the number of lines was changed. **Red** = the text width was changed (letters a little narrower or wider). Red and blue stripes = both. A thicker bar means a bigger change. Leave this ticked while you work on the layout.
* **Paragraph Boxes** draws a thin box around every adjustable paragraph, so you see where each paragraph begins and ends, and where to right-click.
* **Guides and Baselines** draws the margins, the header and footer positions and the baselines (the lines the text sits on).
* **Graph Paper** draws a measuring grid over the page. **Settings** next to it changes the units, number of divisions, colours and line thickness.
* **Layout Analysis** marks typesetting problems in colour on the page. See the next section.

### Auto-update

When **Auto-update** is ticked, PTXprint makes a new PDF by itself a few seconds after you use the right-click menu. The delay (normally 3 seconds) is shown as "(3.0s delay)". It lets you make several changes in a row: each new right-click restarts the delay, so only one print is made at the end. Click the delay text to go to the setting (**Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings** > **Auto-update Delay (seconds)**).

When **Auto-update** is not ticked, your changes are stored but nothing happens until you click **Print (Update PDF)** (**Ctrl+P**). The right-click menu then also has a **Print (Update PDF)** item.

## Layout Analysis and finding issues

Tick **Layout Analysis** (on the **Content** tab, **Regular** and **Full** views) to check the text in the PDF. On a long book this takes some time. A small window says "Analysing text. Press Cancel to stop".

PTXprint can find these issues:

| Issue | What it means | Colour on the page |
|---|---|---|
| **Underfilled Pages** | A page (or a column) where the text stops before the bottom margin. One or more lines are empty at the foot. | (no mark; listed only) |
| **Excessive horizontal whitespace** | A space between words (or between letters, if letter spacing is on) that is wider than the limit. | light blue-green bar |
| **Vertical rivers of whitespace** | Spaces in several lines, one above the other, that form a white "river" down through the paragraph. | yellow |
| **Glyph Collisions** | Letters or marks that touch or overlap, for example a high mark that hits the line above. | red |
| **Bad Glyphs** | A character that the font does not have. It usually prints as an empty box or a question mark. | purple |

Underfilled pages are always found, even when **Layout Analysis** is off, because PTXprint learns about them from the typesetting. The other four need **Layout Analysis**.

**Note:** Layout analysis does not check for widows and orphans (a single line of a paragraph alone at the top or bottom of a column). Look for these yourself.

### Locate... and the issue arrows

**Locate...** (only available when **Layout Analysis** is ticked) chooses which kinds of issues the two arrow buttons find.

* **Locate the previous issue** and **Locate the next issue** jump to the previous or next page with a ticked kind of issue.
* Hold the mouse over an arrow to see the problem page numbers. The colour shows the kind: red = collisions, light blue = too much space, yellow = rivers, light green = both too much space and rivers, purple = bad glyphs, black = only underfilled. The current page is shown between < and >.
* The arrows are greyed out when there are no issues in that direction.

The limits that decide what counts as an issue are on the main window: **Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings**. The **Settings** link next to **Layout Analysis** goes there. The most useful one is **Bad Space minimum width (em)** (normally 1.3). If too many spaces are marked, make it larger. At 0, PTXprint marks only the worst spaces in the document.

**Layout Analysis** turns itself off when you change book, configuration or project, and in some other cases. Tick it again when you need it.

## Adjusting paragraphs with the right-click menu

You can change how many lines a paragraph uses without editing the text. This is the main way to fix a page that is too short or too long:

* **Lines (blue):** PTXprint asks the typesetter to set the paragraph in one line fewer (-1) or one more (+1), by putting the line breaks in different places. It can only shrink a paragraph if its lines have enough space. Short paragraphs often cannot shrink.
* **Text width (red):** PTXprint makes the letters a little narrower (for example 98%) or wider (for example 102%). This makes it easier to lose or gain a line. Small changes are hard to see; large ones can be seen, so keep them small.

Right-click a paragraph in the preview. The first menu line shows which paragraph you clicked, for example `JHN 3.16 \p +0 100%`: the book, the verse where the paragraph starts, the paragraph marker, the current line adjustment and the current text width. The menu items are:

| Menu item | What it does | Mouse shortcut |
|---|---|---|
| **Try Shrink -1 line** (or **Yes! Shrink -1 line**) | Asks for one line fewer. The number in brackets is the new line count. | Shift + left-click |
| **Shrink Text** | Makes the letters narrower by one step (normally 1%), down to the limit (normally 95%). | Ctrl + left-click |
| **Shrink Both** | Makes the letters narrower (about half of the room left before the limit) and asks for one line fewer. | Ctrl + Shift + left-click |
| **Expand +1 line** | Asks for one more line. | Shift + right-click |
| **Expand Text** | Makes the letters wider by one step, up to the limit (normally 105%). | Ctrl + right-click |
| **Expand Both** | Makes the letters wider and asks for one more line. | Ctrl + Shift + right-click |
| **Reset Adjustments** > **Paragraph** / **Column** / **Page** / **Spread** / **End of Book** | Removes the adjustments from this paragraph, or from all paragraphs in this column, page, spread, or from here to the end of the book. | Ctrl or Shift + middle-click resets the paragraph |
| **SpeedSlice** | Opens the SpeedSlice dialog (see below). Only for `\p` and `\m` paragraphs, and not in diglots. | |
| **Edit Style \p** (or other marker) | Opens the **Styles** tab with this paragraph's style selected. | |
| **Jump to Ref in Paratext** | Shows this verse in Paratext (Windows only). | |
| **Zoom to Fit** | Fits the page in the window (Ctrl+F). | |
| **Print (Update PDF)** | Makes a new PDF now. Only shown when **Auto-update** is off. | |

**Column** only appears in two-column layouts. **Spread** only appears in **Book View** when two pages are shown. The step sizes and limits are on the **Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings** (**Shrink Text Step Value**, **Minimum Text Shrink**, **Expand Text Step Value**, **Maximum Text Expand**).

Notes:

* The menu only works on paragraphs that PTXprint can link to a verse reference. Right-clicking in the front matter or on a header often shows no menu.
* -1 line is only a request. If the paragraph cannot lose a line, nothing changes. Then try **Shrink Both**, or a different (longer) paragraph on the same page.
* Changing one paragraph moves all the text after it, so a page that was fine may change. Work from the front of the book to the back.
* With the mouse shortcuts you can work very fast: Shift+click several paragraphs, wait for the delay, and look at the result.

### Where adjustments are stored: the Adj List

Every adjustment is stored in a list for each book, the **Adj List** (adjustment list), one row per paragraph. You can see and edit it on the main window: **View+Edit** tab > **Adj List** (choose the book at the top). The columns are:

* **Book** and **C.V** – the book and the chapter.verse where the paragraph starts.
* **Para** – which paragraph at that verse (1 = the paragraph that contains the verse, 2 = the next one, for example after a heading).
* **Stretch** – the line change (-1, +1, 0 …).
* **Marker** – the paragraph marker (for example `p` or `q1`).
* **Expand** – the text width in percent (100 = normal).
* **Parameters** and **Comment** – extra information. The Auto Page Fill tool writes its measurements here.

The adjustments belong to the current configuration and are used every time you print with it. The Auto Page Fill tool uses the same list.

### How to undo adjustments

There is no Undo button. Instead:

* Use the opposite menu item (for example **Expand +1 line** after **Try Shrink -1 line**).
* Right-click the paragraph and choose **Reset Adjustments** > **Paragraph** (or a whole **Column**, **Page**, **Spread**, or everything to the **End of Book**).
* On the **View+Edit** tab > **Adj List**, select rows and press **Delete** (or right-click > **Delete Row(s)**). Or click a **Stretch** or **Expand** cell and type a new value.

The change appears in the PDF after the next print.

## Moving and resizing pictures with the right-click menu

Right-click a picture in the preview. The menu shows its anchor ("Anchored at: MRK 1.10"), the verse the picture is attached to. The menu has:

* **Change Anchor Ref** – opens the **Enter new anchor verse ref** dialog, to attach the picture to a different verse.
* **Frame Size** – **Column**, **Span** (across both columns), **Page** or **Full** (the whole paper). The current choice is marked with ●.
* **Vertical Position** – for example **Top**, **Bottom**, **Center**, **Before Verse**, **After Paragraph**, **Cutout**, **Below Notes**. Only choices that fit the frame size are shown.
* **Horizontal Position** – for example **Left**, **Right**, **Center**, **Inner**, **Outer**. Not shown for **Span** pictures.
* **Mirror Picture** – **Never**, **Always**, **If on odd page** or **If on even page**.
* **Shrink by 1 line** / **Grow by 1 line** – makes the picture about one text line smaller or larger in height.
* **Show Details...** – opens the **Pictures** tab with this picture selected, to see all its settings.
* **Edit Caption Style \fig** – opens the **Styles** tab at the caption style.

These changes are stored in the picture list (on the **Pictures** tab), not in the Adj List. The message "Image Anchor Not Found" means PTXprint cannot match the picture to a row in the picture list.

### Enter new anchor verse ref (dialog)

Type the new verse as `JHN 3.16` (book code, space, chapter.verse). **OK** only becomes active when the reference is in the right form and no picture is already at that verse. A red message explains what is wrong.

## SpeedSlice: work on one part of a long book quickly

Each print of a long book (for example Psalms or Isaiah) can take a long time. When you fix pages in the middle of such a book, you must wait for the whole book after every change. **SpeedSlice** typesets only a "slice": it starts at the page you are working on and continues for a few chapters. Each print is then fast.

To open it, right-click a `\p` or `\m` paragraph near the top of the page where the slice should begin, and choose **SpeedSlice**. (Not available for diglots.) The dialog has:

* **Reference for Start of Slice** – filled in from the paragraph you clicked. Type either a chapter (for example `JHN 4`) to start at the beginning of that chapter, or the last verse on the page before (for example `GEN 3:23`).
* **First Word on This Page** – if you gave a verse, type the first word on the page where the slice should start. PTXprint skips all the text before that word.
* **Slice Marker (usually \m)** – the paragraph marker the slice starts with.
* **Length of Slice (in chapters)** – how many chapters to include.

**Enable** turns the slice on. **Disable** turns it off and goes back to printing the whole book.

**Important:** SpeedSlice stays on until you turn it off. While it is on, your PDF contains only the slice, and its page numbers are not the real page numbers. Always **Disable** the slice before you make the final PDF.

## Auto Page Fill and the progress monitor

The **Auto Page Fill** tool tries to fill every page of every book, so that the text reaches the bottom margin. It uses the same two methods you use by hand: it changes the number of lines in some paragraphs and the width of their text. It does not move pictures or stretch the space between lines. It stores its results in the Adj List, where you can see and change them later.

The tool does not guess. It really typesets each book many times and measures the result each time. This takes a lot of computer power and time: from minutes for a short book to hours for a whole Bible. It uses several processor cores at once.

To open it, click **Show/hide Page Fill tool with progress monitor** (the lightning icon) at the top of the Preview window (**Regular** and **Full** views). The **PTXprint: Page Filler** window has one coloured bar for each book set to print, and these buttons:

* **Start Fill** – fills from the beginning of each book, starting from no adjustments. It replaces the adjustments already in the Adj List for these books (including those you made by hand).
* **Resume Fill** – keeps the existing adjustments and continues from the first page in each book that is not full. A book that is already full is marked "Already Filled".
* **Stop!** – stops the job. Each book stops after its current test run, which can take a short time.
* **Color Key** – shows what each bar colour means.
* **Settings** – opens the filler settings on the main window (**Advanced** tab > **Other** > **Automatic Page Filler**).

The bottom of the window shows the time used and how busy the processor is (CPU). The bar colours mean:

| Colour | Meaning |
|---|---|
| Grey | Not yet started |
| Grey-blue | Probing – first measurements of what each paragraph can do |
| Sky blue | Filling in progress |
| Tan / light brown | Filling in progress, but some pages could not be filled |
| Green | Complete – all pages filled |
| Orange | Incomplete – some pages could not be filled |
| Red | Failed – an error or the time limit was reached |
| Light yellow | Already filled – nothing to do |
| Peach | No page data – the book was skipped and may need attention |

When all books have finished, PTXprint makes a new PDF and the preview shows it. Then use **Locate the next issue** (with **Underfilled Pages** ticked) to find the pages the tool could not fill, and fix them by hand.

The **Automatic Page Filler** settings decide how hard the tool tries (speed) and how good the text must look (quality):

* **Time limit for the whole job (minutes)** – normally 180.
* **Earlier pages to retry** – if a page cannot be filled, the tool goes back this many pages and tries a different layout there (normally 4). Higher = fewer failed pages, but slower. 0 = fastest.
* **Paragraphs to adjust on each page** – normally 6. Higher = more pages filled, but each page takes longer.
* **Widest word space allowed (× text size)** – normally 1.0. Lower = better-looking text, but more pages may fail.
* **Keep paragraphs close to normal width**, **Penalise shrink or stretch** and **Keep neighbouring paragraphs alike** – fine control of which changes the tool prefers.

The text width limits come from **Minimum Text Shrink** and **Maximum Text Expand** (normally 95% and 105%). The number of books worked on at the same time comes from **Maximum parallel processes** (**Advanced** > **Other** > **Page Layout and Spacing**).

## The buttons at the bottom of the window

* **Show Report Information** – makes a report about the current configuration and opens it in your web browser.
* **Open the PDF in Default PDF Viewer** – opens the PDF in your normal PDF program.
* **Open folder containing the PDF** – opens the output folder in your file manager.
* **Save the PDF with a different name** – saves a copy of the PDF anywhere you like.
* **Print the PDF on paper** – sends the PDF to a printer connected to your computer.

## Common tasks

### Find and fix a page that is not full (manual method)

1. **Print** the book. The Preview window opens.
2. Click **Locate...** (tick **Layout Analysis** on the **Content** tab first if it is greyed out) and make sure **Underfilled Pages** is ticked.
3. Click **Locate the next issue**. The preview jumps to the first page that is not full.
4. Look at the page (and the page before it). A long paragraph whose last line is nearly full can easily gain a line. A paragraph whose last line is very short can easily lose a line.
5. To pull text up from the next page, shrink a paragraph on this page or the page before: **Shift + left-click** it (or right-click > **Try Shrink -1 line**). To push text down, expand a paragraph: **Shift + right-click** (or **Expand +1 line**).
6. Wait for the auto-update (a few seconds) and check the result.
7. If nothing changed, try **Shrink Both**, or another paragraph. Then click **Locate the next issue** again.

### Make a paragraph one line shorter

1. Right-click the paragraph in the preview.
2. Choose **Try Shrink -1 line**. The number in brackets is the number of lines you are asking for.
3. If the paragraph does not get shorter, right-click again and choose **Shrink Both** (narrower text and one line less).

### Remove adjustments that you do not want

1. Right-click a paragraph on the page.
2. Choose **Reset Adjustments**, then **Paragraph**, **Column**, **Page**, **Spread** or **End of Book**.
3. Or: on the main window, go to **View+Edit** > **Adj List**, choose the book, select the rows and press **Delete**. Then **Print**.

### Fill all pages automatically

1. On the **Basic** tab, choose the books to fill.
2. In the Preview window, click the lightning icon (**Show/hide Page Fill tool with progress monitor**).
3. Click **Start Fill** for a fresh start, or **Resume Fill** to keep the existing adjustments.
4. Wait and watch the coloured bars. You can keep using the computer, but it may be slow.
5. When it has finished, a new PDF appears. Use **Locate the next issue** to check the pages that could not be filled (orange bars), and fix them by hand.

### Check the page for spacing problems, collisions and missing characters

1. On the **Content** tab, tick **Layout Analysis**. Wait for the analysis to finish.
2. Look for coloured marks: red = collisions, purple = missing characters, yellow = rivers, light blue-green = wide spaces.
3. Click **Locate...** and tick only the issue types you want to deal with now.
4. Use **Locate the previous issue** and **Locate the next issue** to go from page to page.

### Move a picture or change its size

1. Right-click the picture in the preview.
2. Choose **Frame Size**, **Vertical Position**, **Horizontal Position** or **Mirror Picture**, and the new value. Or choose **Shrink by 1 line** / **Grow by 1 line**.
3. To attach the picture to a different verse, choose **Change Anchor Ref**, type the new verse (for example `MRK 2.4`) and click **OK**.

### Work quickly on pages in the middle of a long book

1. Go to the page you want to work on.
2. Right-click a `\p` or `\m` paragraph at the top of that page and choose **SpeedSlice**.
3. Check the reference. Type the first word on the page in **First Word on This Page**. Leave **Slice Marker** as `\m`. Set **Length of Slice** (for example 3 chapters).
4. Click **Enable**. The next PDF contains only the slice.
5. Make your adjustments. They are stored in the Adj List and also apply to the full book.
6. When finished, right-click a `\p` or `\m` paragraph, choose **SpeedSlice** and click **Disable**. Print again to get the full book.

### See two facing pages together

1. On the **Content** tab, tick **Book View** (or press **Ctrl+B**).
2. Use the arrows to move one spread at a time.

## Common problems

**The right-click menu does not appear, or it has no shrink/expand items.**
The menu needs information that PTXprint writes during printing. Print once with the current configuration. The menu only appears on paragraphs that have a verse reference, so it does not work on most front matter, headers or footers. Right-click the body text of a paragraph.

**I chose "Try Shrink -1 line" but the paragraph did not change.**
The paragraph has no room to lose a line. This is common for short paragraphs, or when the last line is already nearly full. Try **Shrink Both**, or shrink a longer paragraph on the same page. Also check that **Auto-update** is ticked, or click **Print (Update PDF)**.

**My changes do not appear in the PDF.**
If **Auto-update** is not ticked, click **Print (Update PDF)** (Ctrl+P). If it is ticked, wait for the delay (normally 3 seconds). Each new right-click restarts the delay.

**Fixing one page broke another page.**
Every change moves the text after it. Work from the front of the book to the back: fix the first problem page first, then use **Locate the next issue**.

**The Locate... button and the issue arrows are greyed out.**
**Locate...** needs **Layout Analysis** (on the **Content** tab, **Regular** or **Full** view). The arrows are greyed out when no issue of a ticked type is found in that direction. Underfilled pages can be found without Layout Analysis.

**Layout Analysis has turned itself off.**
It turns off when you change book, configuration or project, and after some other changes (for example one/two columns). Tick it again.

**Too many spaces (or almost none) are marked as bad.**
Change **Bad Space minimum width (em)** on the **Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings**. A larger value marks fewer spaces.

**My PDF only has a few chapters, or starts in the middle of the book.**
**SpeedSlice** is still enabled. Right-click a `\p` or `\m` paragraph, choose **SpeedSlice** and click **Disable**. Then print again.

**Start Fill removed the adjustments I made by hand.**
**Start Fill** starts again from nothing for each book. Use **Resume Fill** to keep the existing adjustments.

**The page filler has been running for a very long time.**
Filling is slow, especially for long books such as Psalms. You can click **Stop!**; pages already filled keep their adjustments. To make it faster next time, lower **Earlier pages to retry** or **Paragraphs to adjust on each page** in **Advanced** > **Other** > **Automatic Page Filler**.

**The text looks squashed or stretched after page filling.**
Make the range smaller: raise **Minimum Text Shrink** (for example to 97%) and lower **Maximum Text Expand** (for example to 103%). Lower **Widest word space allowed** for less space between words. Then run the fill again. You can also tick **Adjustments** to find paragraphs with large changes and reset them.

**The Preview window has gone.**
It was closed or hidden. Print again, or check that the main menu (☰) > **Show PDF** is set to **Preview Pane**.

**The preview shows an old PDF.**
Check the date and time in the title bar. If the last print failed, the old PDF is still shown. Read the message at the bottom of the main window.

**Most of the controls described here are missing.**
Many of them (**Layout Analysis**, **Locate...**, the issue arrows, **Auto-update**, the Auto Page Fill button) only appear in the **Regular** and **Full** views. Change the view level in the main menu (☰).

## Control notes

### @c_findBadGlyphs
Finds characters the font has no shape for (marked purple). Often caused by a wrong font, or a character typed by mistake (for example a wrong Unicode character). Fix it by choosing a font that has the character, or by correcting the text in Paratext.

### @c_findCollisions
Finds letters or marks that touch or overlap (marked red). The sensitivity is set by **Collision Detection Padding (pt)** and **Precise collisions** on the **Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings**. Collisions may need more line spacing, or a different font.

### @c_findWhitespace
Finds word spaces wider than **Bad Space minimum width (em)** (normally 1.3 em), marked with a light blue-green bar. Common in short lines and narrow columns. Hyphenation, a slightly smaller font, or **Shrink Text** / **Expand Text** on the paragraph can help.

### @c_findRivers
Finds "rivers" (marked yellow). To remove one, change the line breaks in the paragraph, for example with **Shrink Text** or **Expand Text** from the right-click menu.

### @c_findUnbalanced
The most common issue. Found from the typesetting log, so it works even when **Layout Analysis** is off. Fix with the right-click shrink/expand items or the Auto Page Fill tool. The last page of a book is often short; that is normal.

### @s_pdfZoomLevel
100 = actual size. **Ctrl+mouse wheel** (zooms at the pointer) or **Ctrl+F** (fit) is usually easier.

### @btn_zoom_fit
Fits the whole spread in **Book View**.

### @l_pdfPgsSprds
Only a label ("Pages:" before the page count). Its tooltip lists the page-moving shortcuts.

### @btn_page_first
In a count like "(15)+52", the number in brackets is the pages before page 1 (for example title page and contents); the second number is the numbered pages.

### @btn_page_previous
One spread in **Book View**. Same as **Left arrow** or **Page Up**. Reversed in a right-to-left book.

### @t_pgNum
Type the printed page number (the number on the page, not the position in the PDF file) and press **Enter**. If that page does not exist, the preview goes to the nearest page.

### @btn_page_next
One spread in **Book View**. Same as **Right arrow** or **Page Down**.

### @btn_page_last
Same as **Ctrl+End**.

### @btn_findButton
The choices are **Bad Glyphs**, **Glyph Collisions**, **Excessive horizontal whitespace**, **Vertical rivers of whitespace** and **Underfilled Pages**. Tick only the kinds you want to work on now.

### @btn_seekPage2fill_previous
Hold the mouse over it to see the problem pages, coloured by kind of issue.

### @btn_seekPage2fill_next
The button you use most when fixing the layout: fix a page, then click this to go to the next problem. Hold the mouse over it to see the problem pages.

### @b_reprint
Same as **Print** on the main window. Needed when **Auto-update** is off, or after you change settings on the main window.

### @btn_prvAutoFill
Opening the **PTXprint: Page Filler** window starts nothing; use **Start Fill** or **Resume Fill** there. The job can take a long time and uses a lot of processor power.

### @btn_showSettings
Use it to go back and change settings.

### @btn_prvReport
The report lists possible problems, for example the number of underfilled pages. The button changes colour when there are warnings or errors, and its tooltip then gives a short summary.

### @btn_prvOpen
Use it to search the text or print with that program.

### @btn_prvOpenFolder
Use it to find the PDF to send to someone.

### @btn_prvSaveAs
The original PDF stays where it is. PTXprint remembers the last folder you used.

### @btn_prvPrint
For proof copies. For the final book, send the PDF to the printing company.

### @c_updatePDF
Applies to shrink, expand, reset, picture changes and so on. Ticking it also starts an update straight away. Untick it if each print takes a long time and you want to make many changes first; then click **Print (Update PDF)** when ready.

### @l_updateDelay
Seconds PTXprint waits after your last right-click change. Click it to go to **Auto-update Delay (seconds)** on the **Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings**. Make it longer if printing starts before you have finished your changes.

### @c_bkView
Page 1 is shown alone. Use it to check that facing pages look balanced and end at the same height. Untick it for a larger view of one page.

### @c_pdfadjoverlay
A thicker bar means a bigger change. Shows paragraphs adjusted by you or by the Auto Page Fill tool.

### @c_pdfparabounds
Shows where each paragraph starts and ends, so you know where to right-click. Preview only.

### @c_gridLines
Use it to check that text sits on the line grid and headers and footers are in the right place.

### @c_gridGraph
Use it to measure positions and sizes, for example of pictures or margins. **Settings** next to it changes the grid.

### @lb_adjustGrid
Opens the **Change the Grid Settings** dialog: grid units, divisions, offset, colours and line thickness.

### @c_layoutAnalysis
Also makes **Locate...** available. It takes some time on large PDFs and runs again after each print while ticked. It turns itself off when you change book or configuration.

### @l_analysisSettings
There you set the limits for what is marked, for example **Bad Space minimum width (em)** and the river detection settings.

### @tv_pdfContents
Double-click a line to jump to that page. With only one book, its list is opened out automatically.

### @btn_anc_ok
Moves the picture to the new verse and updates the picture list. Only active when the reference is valid and no other picture uses that verse.

### @btn_anc_cancel
Closes the dialog without changing the anchor.

### @t_newAnchor
Format: book code, a space, chapter.verse. A colon is changed to a full stop for you. For a diglot, the book code can include the side letter (for example `JHNR 3.16`).

### @btn_slice_ok
The next print contains only the slice. Turn it off before you make the final PDF.

### @btn_slice_cancel
Use it when you have finished working on the slice.

### @t_sliceRef
Filled in from the paragraph you right-clicked. A chapter only (for example `PSA 45`) starts at the start of that chapter. With a verse (for example `GEN 3:23`) you must also fill in **First Word on This Page**.

### @t_sliceWord
PTXprint looks for this word after the verse in **Reference for Start of Slice** and skips everything before it. Type it exactly as in the text (same spelling and letters). If the word is not found, the slice cannot start there.

### @t_sliceMkr
`\m` is a paragraph with no first-line indent, which matches a page that starts in the middle of a paragraph.

### @s_sliceLength
A short slice prints faster. Make it long enough for all the pages you want to work on. In books with long chapters, 1 or 2 may be enough.
