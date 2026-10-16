# PDF Preview window, layout analysis and page filling

## What this window is for

The **PDF Preview** window shows the PDF that PTXprint has just made. It opens by itself after you click **Print**. You use it to:

* read through the pages, one page or two facing pages (a "spread") at a time;
* find layout problems quickly (for example, pages that are not full, or words with too much space between them);
* fix small layout problems directly on the page. You right-click a paragraph and make it one line shorter or longer, or you right-click a picture and move it or change its size;
* run the **Auto Page Fill** tool, which tries to make every page full by itself.

The Preview window is a separate window. You can keep it open beside the main PTXprint window. Changes that you make in the Preview window are saved with the current configuration.

In this chapter, "pt" means point. One point is about 0.35 mm. "em" is a width equal to the size of the text. For example, in 10 pt text, 1 em is 10 pt.

## Opening and closing the Preview window

* The Preview window opens after each **Print**, if the main menu (☰) > **Show PDF** is set to **Preview Pane**. This is the normal setting. If **Show PDF** is set to **System Viewer**, the PDF opens in your normal PDF program instead. If it is set to **Output Folder**, PTXprint opens the folder that holds the PDF.
* If you close the Preview window with its **X** button, it is only hidden. It comes back the next time you print.
* Click **Show main PTXprint settings** (shortcut **Alt+S**) to bring the main window to the front.
* The title bar shows the PDF file name and the date and time when it was made. Check this to be sure that you are looking at the newest PDF.

The preview has tabs down the left side. **Content** shows your main PDF. **Cover** shows the cover PDF, if you made one. **Diff** shows the comparison PDF, if you used **Compare PDFs**. **Reference** shows reference documents such as the Ornaments Catalogue. Tabs without a PDF are hidden.

## Moving around: pages, spreads and zoom

The top bar of the window has the navigation controls.

* **First**, **Previous**, **Next** and **Last** buttons move through the PDF. In **Book View** they move by a whole spread.
* The page box shows the printed page number. Type a number and press **Enter** to jump to that page.
* The label next to the page box shows how many pages there are. "(15)+52" means 15 front pages (before page 1) and 52 numbered pages.
* Keyboard: **Left/Right arrow** or **Page Up/Page Down** change page. **Ctrl+Home** and **Ctrl+End** go to the first and last page.
* Mouse: turn the mouse wheel to change page. When you are zoomed in, the wheel scrolls the page instead. Hold the middle mouse button and drag to move the page around.
* Zoom: use the **Zoom** box, **Ctrl+mouse wheel** (zooms at the mouse pointer), **Ctrl+Plus** and **Ctrl+Minus**. **Ctrl+F**, **Ctrl+0** or the **Zoom Fit to Screen** button fit the whole page (or spread) in the window.
* For right-to-left books, the arrow buttons and keys are reversed to follow the direction of the book.

**Book View** (Ctrl+B) shows two facing pages side by side, as in a printed book. Page 1 is shown alone because it is a right-hand page. Then pages 2+3, 4+5 and so on are shown together. Use Book View to check that facing pages look balanced.

The **Contents** list on the left shows the bookmarks in the PDF (books, and often chapters). Double-click a line to jump to that page.

## The Content tab: what to show on the preview

These options only change what you see in the preview. They do not change the PDF itself.

* **Adjustments** draws coloured bars on the edges of paragraphs that have been adjusted. A bar on the **left** edge means the paragraph was made smaller (shrunk). A bar on the **right** edge means it was made bigger (expanded). **Blue** means the number of lines was changed. **Red** means the text width was changed (the letters were made a little narrower or wider). Red and blue in stripes means both were changed. A thicker bar means a bigger change. Leave this ticked while you work on the layout.
* **Paragraph Boxes** draws a thin box around every paragraph that you can adjust. This helps you see where one paragraph ends and the next begins, and where to right-click.
* **Guides and Baselines** draws the margins, the header and footer positions and the baselines (the lines on which the text sits). Use it to check that text lines up on the grid.
* **Graph Paper** draws a measuring grid over the page. Click **Settings** next to it to change the units, the number of divisions, the colours and the line thickness.
* **Layout Analysis** looks for typesetting problems and marks them in colour on the page. See the next section.

### Auto-update

When **Auto-update** is ticked, PTXprint makes a new PDF by itself a few seconds after you use the right-click menu on the preview. The delay (normally 3 seconds) is shown as "(3.0s delay)". The delay lets you make several changes one after the other. Each new right-click restarts the delay, so only one print is made at the end. Click the delay text to go to the setting in the main window (**Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings** > **Auto-update Delay (seconds)**).

When **Auto-update** is not ticked, your changes are stored but nothing happens until you click **Print (Update PDF)** (shortcut **Ctrl+P**). The right-click menu then also has a **Print (Update PDF)** item.

## Layout Analysis and finding issues

Tick **Layout Analysis** (on the **Content** tab, in the **Default** and **Full** views) to make PTXprint check the text in the PDF. On a long book this can take some time. A small window says "Analysing text. Press Cancel to stop".

PTXprint can find these kinds of issues. Each is marked on the page with a colour:

| Issue | What it means | Colour on the page |
|---|---|---|
| **Underfilled Pages** | A page (or a column) where the text stops before the bottom margin. One or more lines are empty at the foot. | (no mark; listed only) |
| **Excessive horizontal whitespace** | A space between words (or between letters, if letter spacing is turned on) that is wider than the limit. | light blue-green bar |
| **Vertical rivers of whitespace** | Spaces in several lines, one above the other, that form a white "river" running down through the paragraph. | yellow |
| **Glyph Collisions** | Letters or marks that touch or overlap each other, for example a high mark that hits the line above. | red |
| **Bad Glyphs** | A character that the font does not have. It usually prints as an empty box or a question mark. | purple |

Underfilled pages are always found, even when **Layout Analysis** is off, because PTXprint learns about them from the typesetting itself. The other four need **Layout Analysis**.

**Note:** Layout analysis does not check for widows and orphans (a single line of a paragraph left alone at the top or bottom of a column). You need to look for these yourself.

### Locate... and the issue arrows

Click **Locate...** to choose which kinds of issues the two arrow buttons next to it should find. **Locate...** is only available when **Layout Analysis** is ticked.

* **Locate the previous issue** and **Locate the next issue** jump to the previous or next page that has a ticked kind of issue.
* Hold the mouse over an arrow to see a list of the problem page numbers. The colour of each number shows the kind of issue: red = collisions, light blue = too much space, yellow = rivers, light green = both too much space and rivers, purple = bad glyphs, black = only underfilled. The current page is shown between < and >.
* The arrows are greyed out when there are no issues in that direction.

The limits that decide what counts as an issue are on the main window: **Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings**. Click the **Settings** link next to **Layout Analysis** to go there. The most useful one is **Bad Space minimum width (em)** (normally 1.3). If too many spaces are marked, make it larger. If you set it to 0, PTXprint marks only the worst spaces in the document.

**Layout Analysis** turns itself off when you change book, configuration or project, and in some other cases. Tick it again when you need it.

## Adjusting paragraphs with the right-click menu

PTXprint lets you change how many lines a paragraph uses, without editing the text. This is the main way to fix a page that is too short or too long. It works like this:

* **Lines (blue):** PTXprint asks the typesetter to set the paragraph in one line fewer (-1) or one line more (+1). It does this by putting the line breaks in different places. It can only shrink a paragraph if there is enough space in its lines. Short paragraphs often cannot shrink.
* **Text width (red):** PTXprint makes the letters of the paragraph a little narrower (for example 98%) or a little wider (for example 102%). This makes it easier to lose or gain a line. Small changes are hard to see. Large changes can be seen, so keep them small.

Right-click on a paragraph in the preview. The first line of the menu shows which paragraph you clicked, for example `JHN 3.16 \p +0 100%`. This is the book, the verse where the paragraph starts, the paragraph marker, the current line adjustment and the current text width. Then the menu has these items:

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

**Column** only appears in two-column layouts. **Spread** only appears in **Book View** when two pages are shown. The step sizes and the limits are on the **Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings** (**Shrink Text Step Value**, **Minimum Text Shrink**, **Expand Text Step Value**, **Maximum Text Expand**).

Notes:

* The right-click menu only works on paragraphs that PTXprint can link to a verse reference. Right-clicking in the front matter or on a header often shows no menu.
* A request for -1 line is only a request. If the paragraph cannot lose a line, nothing changes. Then try **Shrink Both**, or choose a different (longer) paragraph on the same page.
* Changing one paragraph moves all the text after it. A page that was fine may change. Work from the front of the book to the back.
* With the mouse shortcuts you can work very fast: Shift+click several paragraphs, wait for the delay, and look at the result.

### Where adjustments are stored: the Adj List

Every adjustment is stored in a list for each book, called the **Adj List** (adjustment list). One row is one paragraph. You can see and edit the list on the main window: **View+Edit** tab > **Adj List**. Choose the book at the top of the tab. The columns are:

* **Book** and **C.V** – the book and the chapter.verse where the paragraph starts.
* **Para** – which paragraph at that verse (1 = the paragraph that contains the verse, 2 = the next one, for example after a heading).
* **Stretch** – the line change (-1, +1, 0 …).
* **Marker** – the paragraph marker (for example `p` or `q1`).
* **Expand** – the text width in percent (100 = normal).
* **Parameters** and **Comment** – extra information. The Auto Page Fill tool writes its measurements here.

The adjustments belong to the current configuration. They are used every time you print with this configuration. The Auto Page Fill tool uses the same list.

### How to undo adjustments

There is no Undo button. Use one of these ways:

* Use the opposite menu item (for example **Expand +1 line** after **Try Shrink -1 line**).
* Right-click the paragraph and choose **Reset Adjustments** > **Paragraph**. Or reset a whole **Column**, **Page**, **Spread** or everything to the **End of Book**.
* On the **View+Edit** tab > **Adj List**, select one or more rows and press **Delete** (or right-click > **Delete Row(s)**). You can also click in the **Stretch** or **Expand** cell and type a new value.

The change appears in the PDF after the next print.

## Moving and resizing pictures with the right-click menu

Right-click on a picture in the preview. The menu shows where the picture is anchored ("Anchored at: MRK 1.10"). An anchor is the verse that the picture is attached to. The menu has:

* **Change Anchor Ref** – opens the **Enter new anchor verse ref** dialog, to attach the picture to a different verse.
* **Frame Size** – **Column**, **Span** (across both columns), **Page** or **Full** (the whole paper). The current choice is marked with ●.
* **Vertical Position** – for example **Top**, **Bottom**, **Center**, **Before Verse**, **After Paragraph**, **Cutout**, **Below Notes**. Only the choices that fit the frame size are shown.
* **Horizontal Position** – for example **Left**, **Right**, **Center**, **Inner**, **Outer**. Not shown for **Span** pictures.
* **Mirror Picture** – **Never**, **Always**, **If on odd page** or **If on even page**.
* **Shrink by 1 line** / **Grow by 1 line** – makes the picture smaller or larger by about one line of text in height.
* **Show Details...** – opens the **Pictures** tab with this picture selected, where you can see all its settings.
* **Edit Caption Style \fig** – opens the **Styles** tab at the caption style.

These changes are stored in the picture list (on the **Pictures** tab), not in the Adj List. If the message "Image Anchor Not Found" appears, PTXprint cannot match the picture to a row in the picture list.

### Enter new anchor verse ref (dialog)

Type the new verse in the form `JHN 3.16` (book code, space, chapter.verse). The **OK** button only becomes active when the reference is in the right form, and when there is not already a picture at that verse. A red message explains what is wrong.

## SpeedSlice: work on one part of a long book quickly

Each print of a long book (for example Psalms or Isaiah) can take a long time. When you are fixing the layout of pages in the middle of such a book, you must wait for the whole book after every change. **SpeedSlice** solves this. It tells PTXprint to typeset only a "slice" of the book: it starts at the page you are working on and continues for a few chapters. Then each print is fast.

To open it, right-click on a `\p` or `\m` paragraph near the top of the page where you want the slice to begin, and choose **SpeedSlice**. (It is not available for diglots.) The dialog has:

* **Reference for Start of Slice** – filled in from the paragraph you clicked. Either type a chapter (for example `JHN 4`) to start at the beginning of that chapter, or type the last verse on the page before (for example `GEN 3:23`).
* **First Word on This Page** – if you gave a verse, type the first word that appears on the page where the slice should start. PTXprint skips all the text before that word. The word must be typed exactly as it appears in the text.
* **Slice Marker (usually \m)** – the paragraph marker that the slice starts with. Normally `\m` (a paragraph without a first-line indent), because the page usually starts in the middle of a paragraph.
* **Length of Slice (in chapters)** – how many chapters to include (1–10, normally 3).

Click **Enable** to use the slice. Click **Disable** to turn it off and go back to printing the whole book.

**Important:** SpeedSlice stays on until you turn it off. While it is on, your PDF contains only the slice. The page numbers in the slice are not the real page numbers. Always **Disable** the slice before you make the final PDF.

## Auto Page Fill and the progress monitor

The **Auto Page Fill** tool tries to make every page of every book full, so that the text reaches the bottom margin on every page. It uses the same two methods that you use by hand: it changes the number of lines in some paragraphs and the width of their text. It does not move pictures, and it does not stretch the space between lines. It stores its results in the Adj List, so you can see them and change them later.

The tool does not guess. It really typesets each book many times, and measures the result each time. This takes a lot of computer power and time: from minutes for a short book to hours for a whole Bible. It uses several processor cores at once.

To open the tool, click **Show/hide Page Fill tool with progress monitor** (the lightning icon) at the top of the Preview window (**Default** and **Full** views). The **PTXprint: Page Filler** window opens. It has one coloured bar for each book that is set to print. It has these buttons:

* **Start Fill** – starts filling from the beginning of each book. It starts from no adjustments, so it replaces the adjustments that are already in the Adj List for these books (including the ones you made by hand).
* **Resume Fill** – keeps the existing adjustments and continues from the first page in each book that is not full. A book that is already full is marked "Already Filled".
* **Stop!** – stops the job. Each book stops after its current test run. This can take a short time.
* **Color Key** – shows what each colour of bar means.
* **Settings** – opens the settings for the filler on the main window (**Advanced** tab > **Other** > **Automatic Page Filler**).

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

When all books have finished, PTXprint makes a new PDF, and the preview shows the result. Then use **Locate the next issue** (with **Underfilled Pages** ticked) to find the pages that the tool could not fill, and fix them by hand.

The settings on the **Automatic Page Filler** group decide how hard the tool tries (speed) and how good the text must look (quality):

* **Time limit for the whole job (minutes)** – normally 180.
* **Earlier pages to retry** – if a page cannot be filled, the tool goes back this many pages and tries a different layout there (normally 4). Higher = fewer failed pages, but slower. 0 = fastest.
* **Paragraphs to adjust on each page** – normally 6. Higher = more pages filled, but each page takes longer.
* **Widest word space allowed (× text size)** – normally 1.0. Lower = better-looking text, but more pages may fail.
* **Keep paragraphs close to normal width**, **Penalise shrink or stretch** and **Keep neighbouring paragraphs alike** – fine control of which changes the tool prefers.

The text width limits come from **Minimum Text Shrink** and **Maximum Text Expand** (normally 95% and 105%). The number of books worked on at the same time comes from **Maximum parallel processes** (**Advanced** > **Other** > **Page Layout and Spacing**).

## The buttons at the bottom of the window

* **Show Report Information** – makes a report about the current configuration and opens it in your web browser. The button changes colour when the report has warnings or errors, and its tooltip gives a summary.
* **Open the PDF in Default PDF Viewer** – opens the PDF in your normal PDF program.
* **Open folder containing the PDF** – opens the output folder in your file manager.
* **Save the PDF with a different name** – saves a copy of the PDF anywhere you like.
* **Print the PDF on paper** – sends the PDF to a printer that is connected to your computer.

## Common tasks

### Find and fix a page that is not full (manual method)

1. **Print** the book. The Preview window opens.
2. Click **Locate...** (tick **Layout Analysis** on the **Content** tab first if it is greyed out) and make sure **Underfilled Pages** is ticked.
3. Click **Locate the next issue**. The preview jumps to the first page that is not full.
4. Look at the page (and the page before it). Find a long paragraph whose last line is nearly full. That paragraph can easily gain a line. Or find a paragraph whose last line is very short. That paragraph can easily lose a line.
5. To pull text up from the next page onto this page, shrink a paragraph on this page or on the page before: **Shift + left-click** on it (or right-click > **Try Shrink -1 line**). To push text down, expand a paragraph: **Shift + right-click** (or **Expand +1 line**).
6. Wait for the auto-update (a few seconds). Check the result.
7. If nothing changed, try **Shrink Both**, or choose another paragraph. Then click **Locate the next issue** again.

### Make a paragraph one line shorter

1. Right-click on the paragraph in the preview.
2. Choose **Try Shrink -1 line**. The number in brackets is the number of lines you are asking for.
3. If the paragraph does not get shorter, right-click again and choose **Shrink Both** (narrower text and one line less).

### Remove adjustments that you do not want

1. Right-click on a paragraph on the page.
2. Choose **Reset Adjustments**, then **Paragraph**, **Column**, **Page**, **Spread** or **End of Book**.
3. Or: on the main window, go to **View+Edit** > **Adj List**, choose the book, select the rows and press **Delete**. Then **Print**.

### Fill all pages automatically

1. On the **Basic** tab, choose the books that you want to fill.
2. In the Preview window, click the lightning icon (**Show/hide Page Fill tool with progress monitor**).
3. Click **Start Fill** for a fresh start, or **Resume Fill** to keep the adjustments that are already there.
4. Wait. Watch the coloured bars. You can keep using the computer, but it may be slow.
5. When it has finished, a new PDF appears. Use **Locate the next issue** to check the pages that could not be filled (orange bars), and fix them by hand.

### Check the page for spacing problems, collisions and missing characters

1. On the **Content** tab, tick **Layout Analysis**. Wait for the analysis to finish.
2. Look for coloured marks on the page: red = collisions, purple = missing characters, yellow = rivers, light blue-green = wide spaces.
3. Click **Locate...** and tick only the issue types you want to deal with now.
4. Use **Locate the previous issue** and **Locate the next issue** to go from page to page.

### Move a picture or change its size

1. Right-click on the picture in the preview.
2. Choose **Frame Size**, **Vertical Position**, **Horizontal Position** or **Mirror Picture**, and choose the new value. Or choose **Shrink by 1 line** / **Grow by 1 line**.
3. To attach the picture to a different verse, choose **Change Anchor Ref**, type the new verse (for example `MRK 2.4`) and click **OK**.

### Work quickly on pages in the middle of a long book

1. Go to the page you want to work on.
2. Right-click on a `\p` or `\m` paragraph at the top of that page and choose **SpeedSlice**.
3. Check the reference. Type the first word on the page in **First Word on This Page**. Leave **Slice Marker** as `\m`. Set **Length of Slice** (for example 3 chapters).
4. Click **Enable**. The next PDF contains only the slice.
5. Make your adjustments. They are stored in the Adj List and also apply to the full book.
6. When you have finished, right-click a `\p` or `\m` paragraph again, choose **SpeedSlice** and click **Disable**. Print again to get the full book.

### See two facing pages together

1. On the **Content** tab, tick **Book View** (or press **Ctrl+B**).
2. Use the arrows to move one spread at a time.

## Common problems

**The right-click menu does not appear, or it has no shrink/expand items.**
The menu needs information that PTXprint writes during printing. Print once with the current configuration. The menu only appears on paragraphs that have a verse reference, so it does not work on most front matter, headers or footers. Right-click on the body text of a paragraph.

**I chose "Try Shrink -1 line" but the paragraph did not change.**
The paragraph has no room to lose a line. This is common for short paragraphs, or when the last line is already nearly full. Try **Shrink Both**, or shrink a longer paragraph on the same page. Also check that **Auto-update** is ticked, or click **Print (Update PDF)**.

**My changes do not appear in the PDF.**
If **Auto-update** is not ticked, you must click **Print (Update PDF)** (Ctrl+P). If it is ticked, wait for the delay (normally 3 seconds). Each new right-click restarts the delay.

**Fixing one page broke another page.**
Every change moves the text that follows it. Work from the front of the book to the back. Fix the first problem page first, then use **Locate the next issue**.

**The Locate... button and the issue arrows are greyed out.**
**Locate...** needs **Layout Analysis** to be ticked (on the **Content** tab, **Default** or **Full** view). The arrows are greyed out when no issue of a ticked type is found in that direction. Underfilled pages can be found without Layout Analysis.

**Layout Analysis has turned itself off.**
PTXprint turns it off when you change book, configuration or project, and after some other changes (for example one/two columns). Tick it again.

**Too many spaces (or almost none) are marked as bad.**
Change **Bad Space minimum width (em)** on the **Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings**. A larger value marks fewer spaces.

**My PDF only has a few chapters, or starts in the middle of the book.**
**SpeedSlice** is still enabled. Right-click a `\p` or `\m` paragraph, choose **SpeedSlice** and click **Disable**. Then print again.

**Start Fill removed the adjustments I made by hand.**
**Start Fill** starts again from nothing for each book. Use **Resume Fill** if you want to keep the existing adjustments.

**The page filler has been running for a very long time.**
Filling is slow, especially for long books such as Psalms. You can click **Stop!**. Pages that are already filled keep their adjustments. To make it faster next time, lower **Earlier pages to retry** or **Paragraphs to adjust on each page** in **Advanced** > **Other** > **Automatic Page Filler**.

**The text looks squashed or stretched after page filling.**
Make the range smaller: raise **Minimum Text Shrink** (for example to 97%) and lower **Maximum Text Expand** (for example to 103%). Lower **Widest word space allowed** for less space between words. Then run the fill again. You can also look at the coloured bars (tick **Adjustments**) to find paragraphs with large changes and reset them.

**The Preview window has gone.**
It was closed or hidden. Print again, or check that the main menu (☰) > **Show PDF** is set to **Preview Pane**.

**The preview shows an old PDF.**
Check the date and time in the title bar. If the last print failed, the old PDF is still shown. Look at the message at the bottom of the main window.

**Most of the controls described here are missing.**
Many of them (**Layout Analysis**, **Locate...**, the issue arrows, **Auto-update**, the Auto Page Fill button) only appear in the **Default** and **Full** views. Change the view level in the main menu (☰).

## Settings reference: PDF Preview window, layout analysis and page filling

Every control in this part of PTXprint is listed below, grouped by where it appears.

### PDF Preview > Issue types popup

#### Bad Glyphs

- **Where:** PDF Preview > Issue types popup
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Explanation:**

Finds pages where the font has no shape for a character. Such characters usually print as an empty box. This is often caused by a wrong font, or by a character that was typed by mistake (for example a wrong Unicode character). Fix it by choosing a font that has the character, or by correcting the text in Paratext. Marked in purple on the page.

*(Internal ID: `c_findBadGlyphs`)*

#### Glyph Collisions

- **Where:** PDF Preview > Issue types popup
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Explanation:**

Finds pages where letters or marks touch or overlap, for example a tall diacritic that hits the line above. Marked in red. The sensitivity is controlled by **Collision Detection Padding (pt)** and **Precise collisions** on the **Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings**. If you find collisions, you may need more line spacing, or a different font.

*(Internal ID: `c_findCollisions`)*

#### Excessive horizontal whitespace

- **Where:** PDF Preview > Issue types popup
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Explanation:**

Finds pages with a space between words that is wider than **Bad Space minimum width (em)** (normally 1.3 em). Wide spaces are common in short lines and in narrow columns. Marked with a light blue-green bar. Hyphenation, a slightly smaller font, or **Shrink Text** / **Expand Text** on the paragraph can help.

*(Internal ID: `c_findWhitespace`)*

#### Vertical rivers of whitespace

- **Where:** PDF Preview > Issue types popup
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Explanation:**

Finds pages with "rivers": spaces in several lines that sit one above the other and make a white stripe down through the text. Marked in yellow. To remove a river, change the line breaks in the paragraph, for example with **Shrink Text** or **Expand Text** from the right-click menu.

*(Internal ID: `c_findRivers`)*

#### Underfilled Pages

- **Where:** PDF Preview > Issue types popup
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Explanation:**

Finds pages where a column ends before the bottom margin. This is the most common issue. It is found from the typesetting log, so it works even when **Layout Analysis** is off. Fix these pages with the right-click shrink/expand items, or with the Auto Page Fill tool. The last page of a book is often short; that is normal.

*(Internal ID: `c_findUnbalanced`)*

### PDF Preview (dialog)

#### Zoom

- **Where:** PDF Preview (dialog)
- **Type:** Number box
- **View level:** All view levels (Mini, Basic, Default, Full)
- **Values:** from 10 to 1000, default 100

**Tooltip (the text shown when you hover the mouse over it):**

> Zoom Shortcuts:  
> Ctrl + F - fit to screen Ctrl + Plus - zoom in Ctrl + Minus - zoom out Ctrl + 0 - fit to screen Ctrl + Scrollwheel - change zoom level

**Explanation:**

The zoom in percent (100 = actual size). Usually it is easier to use **Ctrl+mouse wheel**, which zooms at the mouse pointer, or **Ctrl+F** to fit the page. Values above 800 are limited to 800.

*(Internal ID: `s_pdfZoomLevel` · Config key: `config/pdfzoomlevel`)*

#### Zoom Fit to Screen

- **Where:** PDF Preview (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Zoom Fit to Screen

**Explanation:**

Fits the whole page, or the whole spread in **Book View**, in the window. Same as **Ctrl+F** or **Ctrl+0**.

*(Internal ID: `btn_zoom_fit`)*

#### Page/Spread

- **Where:** PDF Preview (dialog)
- **Type:** Label
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Shortcuts:  
> Left-Arrow (or PgUp) - previous page/spread Right-Arrow (or PgDn) - next page/spread Ctrl+Home - First page/spread Ctrl+End - Last page/spread Mouse Scroll also changes pages Ctrl+Mouse Scroll Zooms in/out

**Explanation:**

Only a label. It shows "Pages:" before the page count. Hold the mouse over it to see the keyboard and mouse shortcuts for moving between pages.

*(Internal ID: `l_pdfPgsSprds`)*

#### (15)+52

- **Where:** PDF Preview (dialog)
- **Type:** Button
- **Description:** First page (or spread)
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> First page (or spread)
>
> Negative page numbers refer to the peripheral pages before the main text begins on Page 1.
>
> Shortcuts:  
> Left-Arrow (or PgUp) - previous page/spread Right-Arrow (or PgDn) - next page/spread Ctrl+Home - First page/spread Ctrl+End - Last page/spread Mouse Scroll also changes pages Ctrl+Mouse Scroll Zooms in/out

**Explanation:**

Goes to the first page (or spread). The label next to the page box shows the page count. When it reads like "(15)+52", the number in brackets is the number of pages before page 1 (for example title page and contents), and the second number is the number of numbered pages.

*(Internal ID: `btn_page_first`)*

#### Previous page (or spread)

- **Where:** PDF Preview (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Previous page (or spread)

**Explanation:**

Goes back one page, or one spread in **Book View**. Same as **Left arrow** or **Page Up**. In a right-to-left book the direction is reversed.

*(Internal ID: `btn_page_previous`)*

#### Type page number to jump to

- **Where:** PDF Preview (dialog)
- **Type:** Text box
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Type page number to jump to.
>
> Shortcuts:  
> Left-Arrow (or PgUp) - previous page/spread Right-Arrow (or PgDn) - next page/spread Ctrl+Home - First page/spread Ctrl+End - Last page/spread Mouse Scroll also changes pages Ctrl+Mouse Scroll Zooms in/out

**Explanation:**

Shows the current page number and lets you jump to a page. Type the printed page number (the number on the page, not the position in the PDF file) and press **Enter**. If that page number does not exist, the preview goes to the nearest page.

*(Internal ID: `t_pgNum`)*

#### Next page (or spread)

- **Where:** PDF Preview (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Next page (or spread)

**Explanation:**

Goes forward one page, or one spread in **Book View**. Same as **Right arrow** or **Page Down**.

*(Internal ID: `btn_page_next`)*

#### Last page (or spread)

- **Where:** PDF Preview (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Last page (or spread)

**Explanation:**

Goes to the last page (or spread). Same as **Ctrl+End**.

*(Internal ID: `btn_page_last`)*

#### Locate...

- **Where:** PDF Preview (dialog)
- **Type:** Menu button
- **Description:** Select which types of issues to highlight
- **View level:** Default and Full views
- **Only available when:** “Layout Analysis” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> The next/previous issue arrows will jump to pages with issues to be resolved. You can choose which kinds of issues to deal with.
>
> Note: It is only enabled when Layout Analysis is active. Without it, the arrows only jump to underfilled pages.

**Explanation:**

Opens a small list where you tick which kinds of issues the two arrow buttons should find: **Bad Glyphs**, **Glyph Collisions**, **Excessive horizontal whitespace**, **Vertical rivers of whitespace** and **Underfilled Pages**. Tick only the kinds you want to work on now. Greyed out until **Layout Analysis** is ticked.

*(Internal ID: `btn_findButton`)*

#### Locate the previous issue

- **Where:** PDF Preview (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Locate previous page with issues.

**Explanation:**

Jumps to the previous page that has an issue of a ticked kind. Hold the mouse over the button to see the list of problem pages, coloured by kind of issue.

*(Internal ID: `btn_seekPage2fill_previous`)*

#### Locate the next issue

- **Where:** PDF Preview (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Locate next page with issues.

**Explanation:**

Jumps to the next page that has an issue of a ticked kind. This is the button you will use most when fixing the layout: fix a page, then click this to go to the next problem. Hold the mouse over the button to see the list of problem pages.

*(Internal ID: `btn_seekPage2fill_next`)*

#### Print (Update PDF)

- **Where:** PDF Preview (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Update the PDF
>
> Shortcut: Ctrl-P

**Explanation:**

Makes a new PDF with the current settings and adjustments. It is the same as **Print** on the main window. Shortcut: **Ctrl+P**. You need it when **Auto-update** is off, or after you change settings on the main window.

*(Internal ID: `b_reprint`)*

#### Show/hide the Page Filler with progress monitor

- **Where:** PDF Preview (dialog)
- **Type:** Toggle button (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Show/hide the Page Filler with progress monitor

**Explanation:**

Shows or hides the **PTXprint: Page Filler** window (the Auto Page Fill tool and its progress monitor). Opening the window does not start anything. You start the job with **Start Fill** or **Resume Fill** in that window. The job can take a long time and uses a lot of processor power.

*(Internal ID: `btn_prvAutoFill`)*

#### Show main PTXprint settings

- **Where:** PDF Preview (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Show the main PTXprint dialog with all the settings. Shortcut: Alt+S

**Explanation:**

Brings the main PTXprint window to the front, so that you can change settings. Shortcut: **Alt+S**.

*(Internal ID: `btn_showSettings`)*

#### Show Report Information

- **Where:** PDF Preview (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Display a report on the current configuration.

**Explanation:**

Makes a report on the current configuration and opens it in your web browser. The report lists possible problems, for example the number of underfilled pages. The button changes colour when there are warnings or errors, and its tooltip then gives a short summary.

*(Internal ID: `btn_prvReport`)*

#### Open the PDF in Default PDF Viewer

- **Where:** PDF Preview (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Open the PDF in the system's default PDF viewer (e.g. Evince, Acrobat or SumatraPDF).

**Explanation:**

Opens the PDF in the PDF program that your computer normally uses. Use it when you want to search the text or print with that program.

*(Internal ID: `btn_prvOpen`)*

#### Preview Pane: Open folder containing the PDF

- **Where:** PDF Preview (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Open the folder which contains the PDF file(s) created for this project.

**Explanation:**

Opens the folder where PTXprint saves the PDF files for this project. Use it to find the PDF to send to someone.

*(Internal ID: `btn_prvOpenFolder`)*

#### Save the PDF with a different name

- **Where:** PDF Preview (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Save a COPY of this PDF with a new name and/or different folder.

**Explanation:**

Saves a copy of the PDF with a new name or in a different folder. The original PDF stays where it is. PTXprint remembers the last folder you used.

*(Internal ID: `btn_prvSaveAs`)*

#### Print the PDF on paper

- **Where:** PDF Preview (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Print the PDF on paper using a physical printer connected to this device.

**Explanation:**

Prints the PDF on a printer connected to your computer. This is for proof copies. For the final book, send the PDF to the printing company.

*(Internal ID: `btn_prvPrint`)*

### PDF Preview (dialog) › Content tab

#### Auto-update

- **Where:** PDF Preview (dialog) › Content tab
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> When enabled, this re-creates the PDF after making changes using the (right-click) context menu options.
>
> Note that there is a short delay enabling you to make several adjustments one after the other before the update is triggered. This delay can be adjusted by clicking on the value shown here or refer to: Advanced > Other > Preview Pane: Adjustment and Analysis Settings.

**Explanation:**

When ticked, PTXprint makes a new PDF by itself a short time after you use the right-click menu on the preview (shrink, expand, reset, picture changes and so on). Ticking it also starts an update straight away. When it is not ticked, your changes are stored, and you click **Print (Update PDF)** when you are ready. Untick it if each print takes a long time and you want to make many changes first.

*(Internal ID: `c_updatePDF` · Config key: `config/updatePDF`)*

#### (3.0s delay)

- **Where:** PDF Preview (dialog) › Content tab
- **Type:** EventBox
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> When enabled, this re-creates the PDF after making changes using the (right-click) context menu options.
>
> Note that there is a short delay enabling you to make several adjustments one after the other before the update is triggered. This delay can be adjusted by clicking on the value shown here or refer to: Advanced > Other > Preview Pane: Adjustment and Analysis Settings.

#### (3.0s delay)

- **Where:** PDF Preview (dialog) › Content tab
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> When enabled, this re-creates the PDF after making changes using the (right-click) context menu options.
>
> Note that there is a short delay enabling you to make several adjustments one after the other before the update is triggered. This delay can be adjusted by clicking on the value shown here or refer to: Advanced > Other > Preview Pane: Adjustment and Analysis Settings.

**Explanation:**

Shows how many seconds PTXprint waits after your last right-click change before it makes a new PDF. Click it to go to the **Auto-update Delay (seconds)** setting on the **Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings**. Make the delay longer if the print starts before you have finished your changes.

*(Internal ID: `l_updateDelay`)*

#### Book View

- **Where:** PDF Preview (dialog) › Content tab
- **Type:** Checkbox (ticked by default)
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Toggle between a single page view and a book (spread) view. Shortcut: Ctrl + B

**Explanation:**

Shows two facing pages side by side, like an open book (shortcut **Ctrl+B**). Page 1 is shown alone. Use it to check that facing pages look balanced and end at the same height. Untick it to see one page at a time, which gives a larger view.

*(Internal ID: `c_bkView`)*

#### Adjustments

- **Where:** PDF Preview (dialog) › Content tab
- **Type:** Checkbox (ticked by default)
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Show color-coded lines on the left and right edges of paragraphs to indicate the kind of shrink or stretch that has been applied as well as the amount (thickness of line).
>
> These adjustment annotations are not part of the PDF, but are only overlaid on the text to help refine the layout.
>
> Key:
>
> Left=shrink       Right=expand
>
> blue=shrink/expand lines red=shrink/expand text
>
> Interleaved red+blue indicates that both lines and text have been shrunk (or both expanded).

**Explanation:**

Draws coloured bars on the edges of adjusted paragraphs. Left edge = shrunk, right edge = expanded. Blue = number of lines changed, red = text width changed. A thicker bar means a bigger change. The bars are only in the preview, never in the PDF. Use this to see quickly which paragraphs have been adjusted by you or by the Auto Page Fill tool.

*(Internal ID: `c_pdfadjoverlay`)*

#### Paragraph Boxes

- **Where:** PDF Preview (dialog) › Content tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Show Paragraph Boxes
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Draw boxes around the boundaries of all adjustable paragraphs.

**Explanation:**

Draws a thin box around each paragraph that you can adjust. This shows you where each paragraph starts and ends, so you know where to right-click. Shown only in the preview.

*(Internal ID: `c_pdfparabounds`)*

#### Guides and Baselines

- **Where:** PDF Preview (dialog) › Content tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Show guides and baselines
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This option displays various guides (showing margins, headers and footers) as well as the baselines of the body text.

**Explanation:**

Draws guide lines on the preview: the margins, the header and footer positions, and the baselines of the body text. Use it to check that the text sits on the line grid and that headers and footers are in the right place.

*(Internal ID: `c_gridLines` · Config key: `grid/gridlines`)*

#### Graph Paper

- **Where:** PDF Preview (dialog) › Content tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Show grid (graph paper)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> If the standard Rules and Guides are inadequate you can generate a graph-paper-like grid behind the text. This may be useful for precise measuring.

**Explanation:**

Draws a graph-paper grid over the preview page. Use it to measure positions and sizes, for example of pictures or margins. Click **Settings** next to it to change the grid.

*(Internal ID: `c_gridGraph` · Config key: `grid/gridgraph`)*

#### Settings

- **Where:** PDF Preview (dialog) › Content tab
- **Type:** Label
- **Description:** Graph Paper Settings
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Change the graph paper settings.

**Explanation:**

Opens the **Change the Grid Settings** dialog. There you can set the grid units, divisions, offset, colours and line thickness for **Graph Paper**.

*(Internal ID: `lb_adjustGrid`)*

#### Layout Analysis

- **Where:** PDF Preview (dialog) › Content tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Perform Layout Analysis of the text to highlight issues
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This option analyzes the text to highlight layout issues:  
> - character collisions  
> - missing glyphs (bad glyphs)  
> - excessive horizontal space  
> - vertical rivers of space

**Explanation:**

Checks the text of the PDF for typesetting problems and marks them on the page: wide spaces, rivers, collisions and missing characters (bad glyphs). It also makes the **Locate...** button available. The check takes some time on large PDFs. It is done again after each print while it is ticked. It turns itself off when you change book or configuration.

*(Internal ID: `c_layoutAnalysis`)*

#### Settings

- **Where:** PDF Preview (dialog) › Content tab
- **Type:** Label
- **Description:** Layout Analysis Settings
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Click to show the Advanced > Other settings to adjust the parameters which control what should get highlighted as an issue.

**Explanation:**

Opens the main window at the **Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings**. There you set the limits that decide what is marked as an issue, for example **Bad Space minimum width (em)** and the river detection settings.

*(Internal ID: `l_analysisSettings`)*

#### Contents

- **Where:** PDF Preview (dialog) › Content tab
- **Type:** Table
- **View level:** All view levels (Mini, Basic, Default, Full)

**Explanation:**

Lists the bookmarks in the PDF, usually the books and often the chapters. Double-click a line to jump to that page. If there is only one book, its list is opened out automatically.

*(Internal ID: `tv_pdfContents`)*

### Enter new anchor verse ref (dialog)

#### OK

- **Where:** Enter new anchor verse ref (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Moves the picture to the new anchor verse and updates the picture list. It is only active when the reference is valid and no other picture uses that verse.

*(Internal ID: `btn_anc_ok`)*

#### Cancel

- **Where:** Enter new anchor verse ref (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog without changing the anchor.

*(Internal ID: `btn_anc_cancel`)*

#### Anchor Ref

- **Where:** Enter new anchor verse ref (dialog)
- **Type:** Text box
- **Description:** Enter a new anchor verse
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Enter the new anchor verse reference (e.g. JHN 3.16)

**Explanation:**

Type the verse that the picture should be attached to, in the form `JHN 3.16` (book code, a space, chapter.verse). A colon is changed to a full stop for you. For a diglot, the book code can include the side letter (for example `JHNR 3.16`). The picture then appears near that verse.

*(Internal ID: `t_newAnchor`)*

### SpeedSlice (dialog)

#### Enable

- **Where:** SpeedSlice (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Print only this slice of the book (for quick layout work).

**Explanation:**

Turns SpeedSlice on with the values in the dialog. The next print contains only the slice. Remember to turn it off before you make the final PDF.

*(Internal ID: `btn_slice_ok`)*

#### Disable

- **Where:** SpeedSlice (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Turn SpeedSlice off, so that the whole book is printed next time.

**Explanation:**

Turns SpeedSlice off. The next print contains the whole book again. Use this when you have finished working on the slice.

*(Internal ID: `btn_slice_cancel`)*

#### Reference for Start of Slice

- **Where:** SpeedSlice (dialog)
- **Type:** Text box
- **Description:** Slice Dialog: Enter reference to begin SpeedSlice
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Either enter a chapter number to begin with (e.g. JHN 4) or enter the last verse on the preceding page (e.g. GEN 3:23) to begin the slice. Previous content will be skipped over.
>
> SpeedSlice stays on until you click Disable in this dialog.

**Explanation:**

Where the slice starts. It is filled in from the paragraph you right-clicked. Type a chapter only (for example `PSA 45`) to start at the start of that chapter. Or type the last verse on the previous page (for example `GEN 3:23`); then you must also fill in **First Word on This Page**.

*(Internal ID: `t_sliceRef` · Config key: `slice/ref`)*

#### First Word on This Page

- **Where:** SpeedSlice (dialog)
- **Type:** Text box
- **Description:** Slice Dialog: Enter first word on page
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Enter the first word on this page (where the Slice will begin).

**Explanation:**

The first word on the page where the slice should begin. PTXprint looks for this word after the verse in **Reference for Start of Slice** and skips everything before it. Type it exactly as it appears in the text (same spelling and letters). If the word is not found, the slice cannot start at that place.

*(Internal ID: `t_sliceWord` · Config key: `slice/word`)*

#### Slice Marker (usually \m)

- **Where:** SpeedSlice (dialog)
- **Type:** Text box
- **Description:** Slice Dialog: Enter beginning marker
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> What USFM marker needs to be used at the beginning of the Slice? (almost always \m)

**Explanation:**

The paragraph marker that PTXprint puts at the start of the slice. Use `\m` in almost all cases. `\m` is a paragraph with no first-line indent, which matches a page that starts in the middle of a paragraph.

*(Internal ID: `t_sliceMkr` · Config key: `slice/marker`)*

#### Length of Slice (in chapters)

- **Where:** SpeedSlice (dialog)
- **Type:** Number box
- **Description:** Slice Dialog: Length of Slice
- **View level:** Default and Full views
- **Values:** from 1 to 10, default 3

**Tooltip (the text shown when you hover the mouse over it):**

> Roughly how many chapters should the Slice contain?

**Explanation:**

How many chapters the slice contains (1 to 10). A short slice prints faster. Make it long enough to include all the pages you want to work on. In books with long chapters, 1 or 2 chapters may be enough.

*(Internal ID: `s_sliceLength` · Config key: `slice/length`)*
