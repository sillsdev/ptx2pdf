# Problems and solutions

## How to use this chapter

This chapter lists common problems. They are grouped by the kind of problem. Each problem is written the way users often describe it. Under each one you find **Why this happens** and **What to do**.

Before you look for your problem, try these three quick checks. They solve many problems:

1. **Print again.** Most changes appear in the PDF only after you click **Print (Make PDF)**.
2. **Check the view level.** A setting can be hidden but still turned on. Click **☰** › **View Level** › **Full View** to see every setting.
3. **Check the configuration name.** Look at **Name** on the **Basic** tab. Are you working in the configuration you think you are?

In this chapter, "pt" means point. 1 pt is about 0.35 mm.

## Printing fails or no PDF appears

### Nothing happens when I click Print, or the status line says "No books to print"

**Why this happens:** No book is selected, or the book list is empty.

**What to do:**

1. On the **Basic** tab, in **What to Print**, click **Single Book** and choose a book.
2. Or click **Select Multiple Books...**, choose books and click **OK**.
3. Click **Print (Make PDF)** again.

### The status line says "One of more fonts have not been set yet"

**Why this happens:** No font has been chosen for the main text.

**What to do:**

1. Open the **Fonts+Script** tab.
2. Click **Select Font...** next to **Regular** and choose a font.
3. Click **Print (Make PDF)**.

### The status line says "Printing busy"

**Why this happens:** PTXprint is still busy making a PDF.

**What to do:**

1. Wait until the progress bar has finished.
2. Then click **Print (Make PDF)** again.

### PTXprint says "Cannot update PDF file while it is locked!"

**Why this happens:** The old PDF is open in another program (for example Adobe Reader). PTXprint cannot replace a file that is open.

**What to do:**

1. Close the PDF in the other program.
2. Click **Yes** to try again.
3. To avoid this in future, click **☰** › **Show PDF** › **Preview Pane**. The preview does not lock the file.

### The Print (Make PDF) and Save buttons are greyed out

**Why this happens:** PTXprint cannot print yet. For example, no project is selected, or a diglot has a row with no project or configuration.

**What to do:**

1. Read the message in the status line above the bottom bar.
2. Choose a project on the **Basic** tab.
3. For a diglot, check that every row on the **Diglot** tab has a **Project** and a **Configuration**.

### An error window says "Failed to create: … .pdf"

**Why this happens:** The typesetting program stopped because of an error. The window shows the last lines of the log and, often, a hint. The hint is the most useful part. The table below explains the most common hints.

**What to do:**

1. Read the hint in the error window. Find it in the table below and follow the advice.
2. Note any "References to check" or "File(s) to check" at the end of the message. They tell you where to look.
3. If you changed a setting just before the error, change it back and print again.
4. For more detail, open the **View+Edit** tab, **XeTeX Log** sub-tab, and scroll to the end. Error lines start with `!`.
5. If you still cannot fix it, click **Tidy Up** on the **Help** tab and print again. If that does not help, make an archive with **Create Archive...** on the **Help** tab and send it to support.

| Hint in the error window | What it usually means | What to do in PTXprint |
|---|---|---|
| "Cannot find the Font specified. Install it, restart PTXprint and try again" | A font in the configuration (on **Fonts+Script**, or in a style) is not installed on this computer. The message may say which marker uses it. | Install the font for all users and restart PTXprint, or choose an installed font on the **Fonts+Script** tab, or in the style named in the message on the **Styles** tab. |
| "Fallback Font issue - set a font on the Fonts+Scripts tab" | **Use Fallback Font** is ticked, but no valid fallback font is chosen. | On the **Fonts+Script** tab, choose a fallback font, or untick **Use Fallback Font**. |
| "Fallback font probably being applied to text in a footnote (not permitted!)" | A character that needs the fallback font is in a footnote. | Choose a Regular font that has the character, or remove the character from the list of fallback characters. |
| "Check if picture file is located in 'Figures', 'local\figures' or a specified folder" | A picture file cannot be found or loaded. | On the **Pictures** tab, look for grey rows and fix the file name or folder. Or tick **Omit Missing Pictures**. |
| "Check if image/PDF file is available on the system" | A front or back matter PDF, a watermark PDF or a picture is missing. | On the **Peripherals** tab check **Front Matter PDF(s)** and **Back Matter PDF(s)**; on the **Finishing** tab check **Apply Watermark PDF**. Choose the file again with **Select...**, or untick the option. |
| "This might be related to a USFM marker error (using an unsupported marker)" | The text has a marker that is wrong or unknown, or a line in a mods file is wrong. | Run **Basic Checks** in Paratext. If you edited `ptxprint-mods.tex` on the **Advanced** tab, untick **Apply Customized Settings (ptxprint-mods.tex)** and print again. |
| "Failed due to an error in the generated USFM file. Run the Basic Checks in Paratext" | The text has a marker error that PTXprint cannot process. | Run **Basic Checks** in Paratext, fix the errors, and print again. If you use a changes file (**Advanced** tab), check the last rule you added. |
| "Uh oh! You've pushed TeX too far! Try turning Hyphenation off" | The job is too big for the typesetting program, often because of a very long hyphenation list. | On the **Fonts+Script** tab, untick **Hyphenate**, or make a shorter list with **Limit Hyphenation List to Words Found in**. Print fewer books at once. |
| "Possible fault in the hyphenation file" | The hyphenation list has a bad entry. | Untick **Hyphenate** on the **Fonts+Script** tab. Click **Import List...** to make the list again. |
| "You may have too many paragraphed footnotes on the page" | There are too many run-on footnotes on one page. | On the **Notes+Refs** tab, tick **Start Each Footnote on a New Line**. |
| "Possibly a missing +/- value in the Adjust List" or "Check for errors in the Adjust List" | A row in the paragraph adjustment list has a wrong value. | On the **View+Edit** tab, **Adj List** sub-tab, check the **Stretch** column. Each value must start with `+` or `-`. Delete the bad row if you are not sure. |
| "One of the settings in the Stylesheet may be missing the units" | A value in a style or an extra stylesheet is not valid. | Undo your last change on the **Styles** tab. On the **Advanced** tab, untick extra stylesheets (**custom.sty**, **ptxprint-mods.sty**) one at a time to find the problem. |
| "Font size setting issue. Check to see if the font size in a style … is incorrect (maybe it is set to 0.00)" | A style near the reference in the message has a font size of 0. | On the **Styles** tab, find the style and set **Font Size Factor** to a normal value, or click the Reset button for that style. |
| "Expecting a number for \Color definition, not a color name" | A colour in a style was written as a word. | On the **Styles** tab, choose the colour again with the **Color** button. |
| "Problem with Formatting Intro Outline" | The right-aligned outline references cause a problem. | On the **Body** tab, untick **Right-align \ior With Tabbed Leaders**. |
| "Sorry! XeTeX was unable to complete the typesetting" | The typesetter could not place the text on a page. This often happens in a diglot, or when a feature is turned on that you forgot about. | For a diglot, first print each text on its own. Check for tabs whose names are blue (for example **Pictures**, **Diglot**, **Tabs+Borders**) and turn off features you do not need. Look for very large pictures. |
| "To fix this error: Use a different font which is not a Variable Font" | The font is a "variable font", which PTXprint cannot use. | Choose a different (normal) font on the **Fonts+Script** tab. |
| "Bad xdvi file, probably failed to load a picture or font" | A picture or font could not be loaded when the PDF was written. | Check missing pictures on the **Pictures** tab and the fonts on the **Fonts+Script** tab. |
| "Possibly a faulty installation" | Files that come with PTXprint are missing. | Install PTXprint again. |
| "Oops! Something unexpected happened…" or "Probably a TeX macro problem" | PTXprint does not recognise the error. | Click **Tidy Up** on the **Help** tab and print again. If it still fails, send an archive (**Create Archive...**) to support and say which setting you changed last. |

### PTXprint says "PDF was created BUT… Layout problems were encountered on page(s)…"

**Why this happens:** The PDF was made, but on the pages listed the typesetter had to break its own rules. The text may run over the bottom margin, or a picture may be lost.

**What to do:**

1. Open the PDF and look at the pages listed in the message.
2. If there is a large picture on or near that page, make it smaller (**Scale** on the **Pictures** tab) or move it (change the **Anchor Ref**).
3. If you made paragraph adjustments on those pages, reset them: in the **PDF Preview** window, right-click a paragraph › **Reset Adjustments** › **Page**.
4. Print again.

### The status line says "Rerun to fix: …"

**Why this happens:** Some things depend on page numbers, for example the table of contents, the picture credits or the margin notes. PTXprint learned new page numbers during this run. This happens most often when **Quick Run** is ticked.

**What to do:**

1. Untick **Quick Run** at the bottom of the window.
2. Click **Print (Make PDF)** again.

### PTXprint says "Unknown book code"

**Why this happens:** The book list has a word that is not a 3-letter USFM book code, for example `John` instead of `JHN`.

**What to do:**

1. On the **Basic** tab, correct the list in **Portions or Multiple Books**. Use codes such as `MAT`, `JHN`, `1CO`.
2. Or click **Select Multiple Books...** and choose the books by clicking.

### Printing takes a very long time

**Why this happens:** Some settings need a lot of extra work: a **PDF Output Format** other than **Screen**, **Compare PDFs**, Strong's numbers in the text, very large cross-reference lists, many high-resolution pictures, or a whole Bible.

**What to do:**

1. While you work, tick **Quick Run** at the bottom of the window.
2. On the **Finishing** tab, use **Screen (Quickest)** until the final PDF. Untick **Compare PDFs** when you do not need it.
3. On the **Pictures** tab, choose **Low Resolution (Smaller File)** or **Use Place-holders** while you work.
4. Print one book at a time, or use **SpeedSlice** in the **PDF Preview** window for long books.

## The PDF does not change

### I changed a setting, but the PDF looks the same

**Why this happens:** There are several possible reasons:

* You did not print again, or the last print failed. The preview still shows the old PDF.
* The PDF is shown in another program that has not reloaded it.
* Another setting overrides yours (for example a style, or an extra stylesheet).
* You changed the settings of a different configuration, or of the secondary text of a diglot.
* **Layout Only** is ticked, so PTXprint did not process the text again.

**What to do:**

1. Click **Print (Make PDF)** and wait for it to finish. Look at the date and time in the title bar of the **PDF Preview** window. It must be the time of your last print.
2. If an error message appeared, fix that first. The old PDF stays on the screen when printing fails.
3. Check **Name** on the **Basic** tab. Is it the configuration you meant to change?
4. If you are working on a diglot, see "My change has no effect in a diglot" below.
5. Untick **Layout Only** and **Quick Run**, and print again.
6. For style and font changes, see "My change on the Styles tab has no effect" below.

### My text changes in Paratext do not appear in the PDF

**Why this happens:** Normally PTXprint notices that the text changed. If **Layout Only** is ticked, it may not process the text again. Picture captions are a special case: PTXprint uses its own picture list.

**What to do:**

1. Save the text in Paratext.
2. Untick **Layout Only** at the bottom of the PTXprint window and click **Print (Make PDF)**.
3. For picture captions, click **Refresh List** on the **Pictures** tab.
4. If you use **SpeedSlice**, make sure it is not hiding the part that you changed.

### My changes are not kept after I close PTXprint, or Save does nothing

**Why this happens:** **Quit** does not save. Or the configuration is locked with a password. A locked configuration is never saved, not even when you print.

**What to do:**

1. Click **Save** (or **Print (Make PDF)**) before you click **Quit**.
2. If **Save**, **Delete** and **Notes** are greyed out, the configuration is locked. On the **Basic** tab, click the lock button and type the password to unlock it.
3. Or click **Save As** and make a new, unlocked configuration.

### The PDF has only a few chapters, or it starts in the middle of a book

**Why this happens:** **SpeedSlice** is still turned on. Or **From Chapter** and **To** limit the chapters.

**What to do:**

1. In the **PDF Preview** window, right-click a `\p` or `\m` paragraph, choose **SpeedSlice** and click **Disable**.
2. On the **Basic** tab, check **From Chapter** and **To**.
3. Print again.

## Text and fonts

### Some letters print as empty boxes (☐) or question marks

**Why this happens:** The font does not have a shape for these characters.

**What to do:**

1. On the **Fonts+Script** tab, tick **Use Fallback Font** (Default and Full views).
2. Click **Find Missing Characters** to see which characters are missing.
3. Click **Select Font...** next to the list and choose a font that has them.
4. Or choose a different **Regular** font that supports your whole alphabet.
5. If only numbers are boxes, check **Digit mapping** in the **Pick a Font** dialog. Set it to **Default** if the font has no digits for that script.
6. In the **PDF Preview** window, tick **Layout Analysis**. Purple marks show missing characters.

### Bold or italic text looks fake (thick, blurred or slanted wrongly)

**Why this happens:** The font family has no real bold or italic typeface, so PTXprint makes one from the regular letters. The button on the **Fonts+Script** tab shows the style in brackets, for example *(bold)*.

**What to do:**

1. On the **Fonts+Script** tab, click **Select Font...** for **Regular** and choose a family that is shown in **bold** in the list. These families have all four typefaces.
2. Or click **Select Font...** for **Bold** or **Italic** and choose a real bold or italic font.
3. Or, in the **Pick a Font** dialog, change **Embolden** and **Slant** to make the fake style look better.

### Some text is in the wrong font

**Why this happens:** The style for that kind of text has its own font. Or the characters come from the fallback font. In a diglot, the header can use the font of the other text.

**What to do:**

1. On the **Styles** tab, find the marker of that text. If the **Font** label is bold, the style has its own font. Click the bold label to go back to the main font.
2. On the **Fonts+Script** tab, check **Use Fallback Font** and the characters in its list.
3. In a diglot, on the **Header+Footer** tab, choose **Pri** or **Sec** for each part of the header.
4. If you chose a new **Regular** font, check **Bold**, **Italic** and **Bold Italic** again.

### My font is not in the list

**Why this happens:** The font is not installed, or it was installed only for one user, or PTXprint has not refreshed its list.

**What to do:**

1. Install the font for all users.
2. On the **Fonts+Script** tab, click **Refresh Font List**.
3. If it is still missing, restart PTXprint.

### Letters do not join, or vowel marks are in the wrong place

**Why this happens:** **Text Script** is wrong, or the font needs Graphite.

**What to do:**

1. On the **Fonts+Script** tab, set **Text Script** to your script.
2. If the font is a Graphite font, click **Select Font...** for **Regular**, tick **Graphite Rendering**, and click **OK**.
3. Print again.

### Hyphenation does not work

**Why this happens:** There is no hyphenation list, the list is empty, **Hyphenate** is not ticked, or **Between Letters** spacing is turned on.

**What to do:**

1. On the **Fonts+Script** tab, click **Import List...** and read the message. It says how many words were used.
2. If the number is 0, untick **Only Use Approved Hyphenation Words** and click **OK** again, or approve words in the Paratext Wordlist.
3. Tick **Hyphenate**.
4. Make sure **Between Letters** in **Spacing Adjustments** is unticked.
5. Print again.

### Long lines do not break in Thai, Khmer, Myanmar, Chinese or similar scripts

**Why this happens:** PTXprint does not know where it may break a line.

**What to do:**

1. On the **Fonts+Script** tab, set **Text Script** to your script.
2. Tick **Specify Line Break Locale** and type the language code, for example `th`, `km`, `my` or `zh`.
3. Or mark the break points with `/` in the text (Thai, Lao, Myanmar, Tai Tham, New Tai Lue).

### Coloured text prints in black

**Why this happens:** **Enable Colored Text (as Specified in Stylesheet)** is not ticked, or the **PDF Output Format** is **Print-Gray (B/W)**.

**What to do:**

1. On the **Fonts+Script** tab, tick **Enable Colored Text (as Specified in Stylesheet)**.
2. On the **Finishing** tab, check **PDF Output Format**.

### My change on the Styles tab has no effect

**Why this happens:** You changed a different marker or level (for example `s1` instead of `s2`). Or another style or stylesheet wins. Or a setting on another tab controls it.

**What to do:**

1. Check which marker the text really uses. On the **Styles** tab, click the filter button next to **Find** to show only markers used in your books.
2. Remember that `\p` gets its size and line spacing from the **Layout** tab (**Base Font Size** and **Base Line Spacing**).
3. If you chose **Justified** but the text is ragged, tick **Justify Paragraphs** on the **Body** tab.
4. On the **Advanced** tab, check whether **Apply Stylesheet Overrides (ptxprint-mods.sty)** is ticked. It is applied last and may set the same value.
5. Print again.

### Some text is missing from the PDF

**Why this happens:** A setting removes it. For example **Include Contents of Marker** is unticked for its style, or a setting on the **Body** tab removes headings, introductions or empty verses.

**What to do:**

1. On the **Styles** tab, look for the marker. A marker with a line through it is not printed. Tick **Include Contents of Marker**.
2. On the **Body** tab, check **Book Introductions**, **Introductory Outlines**, **Include Scripture Text**, **Headings**, **Parallel Passage Refs** and **Hide Empty Verses**.
3. For study notes, tick **Extended Footnotes (\ef)** on the **Notes+Refs** tab (Full view).

## Layout and spacing

### There is white space at the bottom of every page

**Why this happens:** The text area does not hold a whole number of lines. The part of a line that is left over is empty on every page.

**What to do:**

1. On the **Layout** tab, look at **Lines Per Page** (Default and Full views). If it is red, this is the cause.
2. Click **one** fine-tune button: next to **Base Line Spacing (pt)**, or next to the top or bottom margin.
3. The number turns blue. Print again.

### Some pages or columns end early, with empty lines at the bottom

**Why this happens:** With **Align Text to Baseline**, all lines sit on a fixed grid. The typesetter will not leave one line of a paragraph alone at the top or bottom of a page, it keeps a heading with the next lines, and it keeps pictures and notes with their verse. So sometimes a page ends one or more lines early.

**What to do:**

1. Do this last, when all other settings are final.
2. In the **PDF Preview** window, right-click a paragraph on this page or the page before, and choose **Try Shrink -1 line** to pull text up. Or choose **Expand +1 line** on the page before to push a line down.
3. Or use the **Auto Page Fill** tool (the lightning icon in the **PDF Preview** window).
4. If a picture is near the gap, move it or make it smaller.
5. For a quick draft, on the **Layout** tab, move the switch to **Variable Line Spacing**. This fills the columns, but the lines no longer line up on both sides of the paper.

### The last page of a book has only a few lines

**Why this happens:** The book is just a little too long to end on the page before.

**What to do:**

1. In the **PDF Preview** window, find paragraphs in the last few pages whose last line is short.
2. Right-click each one and choose **Try Shrink -1 line** (or **Shrink Both**) until the lines move back.
3. Or use the **Auto Page Fill** tool.
4. If many lines must move, make a small change for the whole book (for example a slightly smaller **Base Font Size** or a slightly smaller **Min/Shrink** in **Spacing Adjustments** on the **Fonts+Script** tab). Then check all pages again.
5. On the **Advanced** tab, **Other** sub-tab, **Page Layout and Spacing**, **Where to start a new book** set to **Same page** lets the next book start on the same page.

### I asked to shrink a paragraph, but nothing changed

**Why this happens:** The paragraph has no room to lose a line. This is common for short paragraphs, or when the last line is almost full. Or the PDF has not been updated yet.

**What to do:**

1. Wait a few seconds if **Auto-update** is ticked, or click **Print (Update PDF)**.
2. Right-click again and choose **Shrink Both**.
3. Or try a longer paragraph on the same page, or on the page before.

### Fixing one page broke a later page

**Why this happens:** Every change moves all the text after it.

**What to do:**

1. Work from the front of the book to the back.
2. Fix the first problem page, then use **Locate the next issue** in the **PDF Preview** window.
3. Make all other layout changes (fonts, margins, pictures) **before** you adjust paragraphs.

### Text looks squashed, stretched or has big gaps between words

**Why this happens:** Paragraph adjustments or the page filler made the letters narrower or wider. Or the word spacing range is too wide. Or **Keep Repeated Words Together** or **Prevent Orphan Words** forces bad line breaks.

**What to do:**

1. In the **PDF Preview** window, tick **Adjustments** to see which paragraphs were changed (coloured bars). Reset the worst ones (right-click › **Reset Adjustments** › **Paragraph**).
2. On the **Advanced** tab, **Other** sub-tab, **Preview Pane: Adjustment and Analysis Settings**, raise **Minimum Text Shrink** (for example to 97%) and lower **Maximum Text Expand** (for example to 103%).
3. On the **Fonts+Script** tab, check **Between Words** in **Spacing Adjustments**. A very high **Max/Stretch** allows big gaps.
4. Turn on hyphenation to give the lines more break points.

### Almost everything on the Layout, Fonts+Script and Styles tabs is greyed out

**Why this happens:** **Lock UI Layout Settings** is ticked.

**What to do:**

1. Change to the **Full** view.
2. On the **Advanced** tab, **Main** sub-tab, **General** area, untick **Lock UI Layout Settings**.

### The font size changed when I changed the line spacing (or the other way round)

**Why this happens:** **Lock Ratio** is ticked on the **Layout** tab. It keeps the two numbers in the same proportion.

**What to do:**

1. Untick **Lock Ratio**.
2. Type the font size and line spacing you want.

### The header or footer is cut off, or too close to the edge of the paper

**Why this happens:** The header and footer sit inside the top and bottom margins. If the gap between the header and the text is large, the header moves towards the edge.

**What to do:**

1. On the **Layout** tab, look at the blue numbers in the margin picture.
2. Make **Start of Page to Top of Text (mm)** (or **Bottom of Text to End of Page (mm)**) larger.
3. Or make **Bottom of Header to Top of Text (pt)** (or **Bottom of Text to Top of Footer (pt)**) smaller.

### My PDF suddenly looks different, but I did not change anything on the main tabs

**Why this happens:** A setting on the **Advanced** tab may have been changed, or an extra file (changes file, mods file) may be turned on. Someone else on the team may have changed the configuration through Paratext Send/Receive.

**What to do:**

1. Open the **Advanced** tab, **Other** sub-tab, and click the filter button. Only groups with changed settings are shown. Changed settings have **bold** labels.
2. On the **Main** sub-tab, check which boxes are ticked in **Text Processing & Stylesheets**.
3. Check the **Notes** box on the **Basic** tab for comments from the team.

### Coloured marks, bars or codes appear in the margins of my PDF

**Why this happens:** A proof-reading option is turned on.

**What to do:**

1. On the **Advanced** tab, **Other** sub-tab, **PDF Options, Covers, Show/Hide**, untick the "show" options (for example **Show adjust points**, **Show USFM codes**, **Show Error Bars For Overfull Lines**, **Mark Trigger Points**).
2. In the **Diglot** group, untick **Show Diglot Trace Marks**.

Note: the coloured bars and boxes in the **PDF Preview** window (**Adjustments**, **Paragraph Boxes**, **Layout Analysis**) are only on the screen. They are not in the PDF.

## Pictures

### No pictures appear in the PDF

**Why this happens:** Pictures are turned off, or the picture list (PicList) is empty, or place-holders are used.

**What to do:**

1. On the **Pictures** tab, **Global Options**, tick **Include Pictures (illustrations)**.
2. Change to the **Default** view so you can see the picture table. If it is empty, click **Generate...**. PTXprint uses only the pictures in its list, not the `\fig` lines in Paratext directly.
3. Make sure **Use Place-holders (Smallest PDF File)** is not chosen.
4. On the **Details** sub-tab, check that **Print** is ticked under **Media** for the pictures.

### Some pictures are missing

**Why this happens:** PTXprint cannot find the picture file (the row in the table is grey), or the picture's book is not being printed, or **Image Types** excludes the file type.

**What to do:**

1. On the **Pictures** tab, look for grey rows. Check the **Filename**.
2. Put the file in the project's `figures` or `local\figures` folder, or tick **Use Other Location** and choose the folder with **Picture Folder...**.
3. Clear the **Image Types** box if it only lists some types.
4. After printing, look at the missing-pictures count and list on **Global Options**. **Omit Missing Pictures** skips missing files without an error, so it can hide the problem.

### A picture is on the wrong page or in the wrong place

**Why this happens:** A picture goes on the page of its anchor verse only if there is room. If there is no room, it moves to a later page. Large pictures move more often.

**What to do:**

1. In the **PDF Preview** window, right-click the picture and choose **Change Anchor Ref**. Choose a verse a little earlier (or later).
2. Or right-click and choose a different **Vertical Position** or **Horizontal Position**.
3. Make the picture smaller with **Shrink by 1 line**, or with **Scale** on the **Pictures** tab, **Details** sub-tab.
4. Print again.

### A picture row is red in the table

**Why this happens:** At this size and scale the picture is too tall to fit on the page.

**What to do:**

1. On the **Details** sub-tab, make **Scale** smaller.
2. Or change **Frame Size** from **Span Width** to **Column Width**.

### I cannot choose the picture position I want

**Why this happens:** The position lists depend on each other. For example, **Span Width** only allows **Top**, **Bottom** and **Below Notes**, and no horizontal position.

**What to do:**

1. Choose **Frame Size** first, then **Vertical Position**, then **Horizontal Position**.

### My caption changes in Paratext do not show

**Why this happens:** PTXprint keeps its own copy of the captions in the picture list.

**What to do:**

1. On the **Pictures** tab, click **Refresh List**. The size and position settings stay the same.
2. Print again.

### The picture credits are missing or wrong

**Why this happens:** The colophon or front matter has no `\zimagecopyrights`, or a picture is not from a known illustration series, or the page numbers are not yet known.

**What to do:**

1. On the **Peripherals** tab, tick **Colophon at End of Publication** and check that the text contains `\zimagecopyrights`. Or put `\pc \zimagecopyrights` in the front matter.
2. On the **Pictures** tab, **Details** sub-tab, type the credit in **Copyright Attribution** for pictures that do not show **Automatic**.
3. Click **Print (Make PDF)** twice.

### The message "Image Anchor Not Found" appears when I right-click a picture

**Why this happens:** PTXprint cannot match the picture in the PDF to a row in the picture list. This can happen after the list was changed.

**What to do:**

1. Print again so the preview matches the current picture list.
2. Then make the change on the **Pictures** tab, **Details** sub-tab.

## Notes and cross-references

### Footnote or cross-reference settings are greyed out

**Why this happens:** Most settings need another setting first.

**What to do:**

1. Tick **Include Footnotes** on the **Notes+Refs** tab, **Footnotes** sub-tab.
2. For the caller box, tick **Show Callers**.
3. **End of Column** needs **Two Column Layout** on the **Layout** tab.
4. **Side Margin** needs **Margin Notes Col Width (mm)** on the **Layout** tab.
5. The **Source for References** settings need **Use External List of Cross-References** (Full view).

### The callers in the PDF are not the ones I typed

**Why this happens:** Each note in Paratext can ask for no caller (`\f -`) or a fixed caller. PTXprint obeys that.

**What to do:**

1. On the **Notes+Refs** tab, tick **Override hidden/automatic Footnote caller settings** (or the cross-reference version).
2. Print again.

### The cross-reference placement changed by itself

**Why this happens:** PTXprint keeps the footnote and cross-reference placements in step. For example, if you choose **End of Column** for one, the other changes too.

**What to do:**

1. After you change one placement, check both the **Footnotes** and the **Cross-References** sub-tabs.

### Changing the cross-reference rule settings does nothing

**Why this happens:** PTXprint draws only one rule above the notes at the bottom of the page. It uses the footnote rule settings, unless the footnotes are at the **End of Book**.

**What to do:**

1. Change the rule on the **Footnotes** sub-tab instead.

### The footnotes run into the footer

**What to do:**

1. On the **Notes+Refs** tab, **Footnotes** sub-tab, make **Space Above Rule** larger.
2. Or, on the **Layout** tab, make **Bottom of Text to Top of Footer (pt)** larger.

### Margin notes do not appear

**Why this happens:** **Margin Notes Col Width (mm)** on the **Layout** tab only makes the space. The notes must also be sent there.

**What to do:**

1. On the **Notes+Refs** tab, set **Placement of Footnotes** (and/or **Placement of Cross-References**) to **Side Margin**.
2. For headings in the margin, tick **In Margin** on the **Body** tab.

### The external cross-references show the wrong book names

**Why this happens:** PTXprint uses the short book names from the Paratext project's **Scripture Reference Settings** (these should match the `\toc3` lines).

**What to do:**

1. Correct the book names in Paratext.
2. Print again.

## Diglot

### My change has no effect in a diglot

**Why this happens:** Each text in a diglot has its own configuration. Fonts, font size, styles and notes of the second text come from its own (secondary) configuration. Page settings (page size, margins, header and footer positions, the footnote rule and others) always come from the primary configuration.

**What to do:**

1. To change the second text's fonts, styles or notes: on the **Diglot** tab, right-click its row and choose **Edit Settings…**. Make the change, then click **Return to Primary**.
2. To change page size, margins or headers: make sure you are in the primary configuration (the big button says **Print (Make PDF)**, not **Return to Primary**).
3. Print again from the primary configuration.

### The big button says "Return to Primary" instead of "Print"

**Why this happens:** You are looking at the secondary configuration of a diglot (after **Edit Settings…**).

**What to do:**

1. Click **Return to Primary**.
2. Then click **Print (Make PDF)**. (The small **Print** button prints only the secondary text.)

### PTXprint says "These books are not available in the secondary diglot project"

**Why this happens:** You selected a book that the second project does not have.

**What to do:**

1. On the **Basic** tab, select only books that are in every project of the diglot.

### PTXprint says "Failed to merge texts due to a Syntax Error" (Diglot Merge Error)

**Why this happens:** One of the texts has a marker error.

**What to do:**

1. Run **Basic Checks** in Paratext for every project in the diglot. Fix the errors.
2. If you use a changes file (**Advanced** tab), check that a rule has not caused the error.
3. Print each text on its own first, then the diglot.

### The status line says "No Config found for diglot", or Print is greyed out

**Why this happens:** A row on the **Diglot** tab has no project or configuration.

**What to do:**

1. On the **Diglot** tab, choose a **Project** and then a **Configuration** in every row.

### The diglot columns have big gaps, or the texts do not line up well

**Why this happens:** One text needs more space than the other.

**What to do:**

1. Give the longer text more **% Width** (for example 55 and 45), or a smaller font size or line spacing in its row.
2. Try **Auto-calculate optimum widths of diglot columns** with one short book selected.
3. Try another **Merging mode**, for example **Scored (Chapter)** or **Chapter Verse**.

### The % Width numbers are red

**Why this happens:** The widths of the texts on one page do not add up to 100.

**What to do:**

1. Change the numbers, or right-click a row and choose **Distribute Widths**.

### I cannot untick Diglot (or Polyglot)

**Why this happens:** This is on purpose, so that you do not lose your diglot settings. PTXprint opens the **Save As Monoglot** dialog instead.

**What to do:**

1. Type a new configuration name and click **OK**. PTXprint opens a one-text copy. The diglot configuration stays as it was.

### Two Column Layout on the Layout tab is greyed out

**Why this happens:** A diglot always uses columns, so PTXprint ticks this box and locks it while the diglot is on.

## Headers, footers and page numbers

### There is no header on the first page of a book

**Why this happens:** This is normal. PTXprint does not print a header (or the rule under it) on the page where a book starts.

**What to do:**

1. To have a page number on that page, tick **Print Page Number at Bottom of Intro Page(s)** on the **Header+Footer** tab (Default and Full views).

### The header references are empty on some pages

**Why this happens:** This is normal on pages without verses, for example introduction or glossary pages.

### The header shows the last verse where I expected the first verse

**Why this happens:** **Mirror Pages** is ticked on the **Layout** tab. On left-hand pages PTXprint swaps **First Reference** and **Last Reference**, and also swaps **Inner** and **Outer**.

**What to do:**

1. Choose the other item on the **Header+Footer** tab.
2. Or untick **Mirror Pages** on the **Layout** tab if every page should look the same.

### My own header text prints wrongly, or the PDF fails after I typed a header

**Why this happens:** In the header and footer boxes, spaces and the characters `# % & ^ ~ \` need a backslash before them.

**What to do:**

1. Type `\ ` (a backslash and a space) for each space, for example `DRAFT\ \isodate`.
2. Type `\#`, `\%` and so on for those characters.

### The page numbers do not start at the number I set

**Why this happens:** **Starting Page Number (for Scripture Books)** applies at the first Scripture book, when the front matter uses its own page numbering. If the front matter uses normal page numbers, the numbering continues from the front matter.

**What to do:**

1. Check the page number codes (`\nopagenums`, `\resetpagenums`, `\dopagenums`) in the front matter on the **View+Edit** tab (advanced).

### The table of contents is empty or has wrong page numbers

**Why this happens:** PTXprint needs a first run to learn the page numbers. With **Quick Run** it runs only once.

**What to do:**

1. Untick **Quick Run**.
2. Make sure **Table of Contents** is ticked on the **Peripherals** tab, and the front matter contains `\ztoc|main\*`.
3. Click **Print (Make PDF)** again.

### A variable prints as "<Type Value Here>"

**Why this happens:** The front matter uses a variable that has no value yet.

**What to do:**

1. On the **Peripherals** tab, type a value for it in the **Variables and Values** table.
2. Print again.

### The front matter does not appear in the PDF

**What to do:**

1. On the **Peripherals** tab, tick **Local Front Matter**.
2. Print again.

### My front matter changes disappeared

**Why this happens:** **Generate** on the **Front Matter** sub-tab replaces the whole front matter. **Refresh** also throws away unsaved changes. There is no Undo.

**What to do:**

1. Type the changes again.
2. In future, copy important text to a safe place before you click **Generate**.

### The cover was turned off by itself

**Why this happens:** PTXprint turns off **Create Cover Page** when you untick **Local Front Matter**. The status line says "The Cover is disabled because Local Front Matter is turned off."

**What to do:**

1. On the **Peripherals** tab, tick **Local Front Matter**, then tick **Create Cover Page** again.

### The colophon is missing

**Why this happens:** **Colophon at End of Publication** is unticked. PTXprint unticks it when you tick **Local Front Matter**, and when **Layout Only** is ticked.

**What to do:**

1. On the **Peripherals** tab, tick **Colophon at End of Publication** again.
2. Untick **Layout Only** at the bottom of the window, and print again.

## Settings and configurations

### I lost my changes after I chose another configuration

**Why this happens:** When you choose another configuration in **Name**, PTXprint does **not** save the current one.

**What to do:**

1. Always click **Save** (or **Print (Make PDF)**) before you change configuration.
2. The lost changes cannot be recovered. Make them again.

(When you choose a different **Project**, PTXprint does save the current configuration first.)

### I deleted a configuration and now PDFs of other configurations are gone

**Why this happens:** When you delete a configuration (not **Default**) and click **Yes**, PTXprint deletes that configuration's settings. It also empties the project's whole output folder: the folder shown as **Output PDF Location** on the **Help** tab. That folder holds the PDFs and temporary files of **all** configurations of the project, not only the deleted one.

The settings of the other configurations are **not** affected. Only the output files are removed.

**What to do:**

1. Open each configuration you need and click **Print (Make PDF)**. PTXprint makes the PDFs again.
2. In future, before you delete a configuration, copy the PDFs you want to keep to another folder. Click **Open folder containing the PDF** to find them.
3. Final PDFs that you send to a printer should always be kept in a separate folder of their own.

### I clicked Reset and all my settings in Default are gone

**Why this happens:** For the **Default** configuration, the **Delete** button is replaced by **Reset**. **Reset** does not ask first. It sets every setting of **Default** back to the PTXprint defaults, and it removes the saved files of **Default** (including its front matter and picture list).

**What to do:**

1. If the settings are in a PDF made with **Include Config Settings Within PDF**, use **Import Settings...** on the **Basic** tab to bring them back from that PDF.
2. Or import them from another configuration, or from a ZIP archive.
3. In future, use **Save As** to keep your work in a named configuration, not in **Default**.

### The lock button is greyed out

**Why this happens:** The **Default** configuration cannot be locked.

**What to do:**

1. Use **Save As** to make a named configuration, then lock that one.

### I cannot unlock my configuration

**Why this happens:** The password is wrong. If you clicked **Cancel** in the lock dialog, PTXprint may have locked the configuration with an empty password.

**What to do:**

1. Click the lock button and type the password.
2. If that does not work, click the lock button, leave the password box empty and click **OK**.
3. If you cannot unlock it, use **Save As** to make a new, unlocked copy.

### The OK button in "Save Current Configuration As..." is greyed out

**Why this happens:** The name is empty, has spaces or special characters, or is already used.

**What to do:**

1. Read the message below the box.
2. Use only letters a–z and A–Z, numbers, `(`, `)`, `_` and `-`.

### Import Settings says "Cannot find any settings to import from the selected file"

**Why this happens:** The PDF was made without **Include Config Settings Within PDF** (on the **Finishing** tab), or with a very old PTXprint version.

**What to do:**

1. Use another source, for example a ZIP archive made with **Create Archive...**, or a saved configuration.
2. In future, keep **Include Config Settings Within PDF** ticked on the **Finishing** tab.

### I imported only one group of settings, but everything changed

**Why this happens:** **Everything** was still ticked. In the **Basic** view the **Everything** tab is hidden, but it is still ticked.

**What to do:**

1. Change to the **Default** view.
2. Open **Import Settings...** again and untick **Everything** before you tick the groups you want.

### Imported styles did not change

**Why this happens:** PTXprint only updates styles that you have not changed in the target configuration.

**What to do:**

1. In the **Import Settings** dialog, tick **Override ALL Style Settings**.

### A setting changed by itself

**Why this happens:** Some settings change other settings to keep them working together. For example:

* **Hyphenate** unticks **Between Letters**.
* **Right-to-Left** ticks **RTL Book Binding**.
* **Variable Line Spacing** ticks **Fill Columns** and **Allow Unbalanced Columns**.
* Changing between one and two columns halves or doubles the **Base Indent**.
* **Print-CMYK**, **Print-Gray** and **Print-Spot** tick **Only Show on Odd Pages** for thumb tabs.
* The footnote and cross-reference placements change together.
* **Local Front Matter** unticks the colophon.

**What to do:**

1. Read the status line. PTXprint often tells you what it changed.
2. Change the setting back if you need to.

## I cannot find a setting

### A tab or setting that I used before has disappeared

**Why this happens:** The view level is lower than before. Lower view levels hide many settings.

**What to do:**

1. Click **☰** › **View Level** › **Default View** or **Full View**.
2. Or type the name of the setting in the **Search for settings** box (bottom-left, or press **Ctrl+F**). If the setting is hidden, PTXprint changes the view level for you.

### The PDF has pictures (or a diglot, borders, thumb tabs …) but I cannot find the setting

**Why this happens:** The feature was turned on in a higher view level. Hidden settings still work.

**What to do:**

1. Change to **Full View**.
2. Look for tabs whose names are blue. A blue tab name means a feature on that tab is turned on.
3. Turn the feature off on that tab.

### A setting is greyed out

**Why this happens:** It needs another setting first, or another setting blocks it. Common examples:

| Greyed-out setting | What it needs |
|---|---|
| Almost all of **Layout**, **Fonts+Script** and **Styles** | Untick **Lock UI Layout Settings** (**Advanced** tab, Full view). |
| **Save**, **Delete**, **Notes** | Unlock the configuration (lock button on the **Basic** tab). |
| **Two Column Layout** | Diglot is on. A diglot always uses columns. |
| **Verse** (header references) | Tick **Chapter** first. |
| **Pri** / **Sec** (header) | Turn on **Diglot (or Polyglot)**. |
| **Parallel Passage Refs** | Tick **Headings** on the **Body** tab. |
| **Hanging Poetry Verse Numbers** | Untick **Marginal Verses**. |
| **Between Letters** | Untick **Interlinear** on the **Advanced** tab. |
| **End of Column** (notes) | Tick **Two Column Layout**. |
| **Side Margin** (notes) | Tick **Margin Notes Col Width (mm)** on the **Layout** tab. |
| An **Edit...** button on the **Advanced** tab | Tick the check box for that file first. |
| **Scale to fit** (Finishing) | Set **Pages Per Spread** to **1-up**. |
| **Color Hue**, **Tolerance** | Choose **Print-Spot** as **PDF Output Format**. |
| **Locate...** (PDF Preview) | Tick **Layout Analysis**. |
| Fine-tune buttons (Layout) | **Lines Per Page** is already blue. Nothing to fix. |
| **Mirror** (picture) | Choose **OK to mirror** on the picture's **Checklist** sub-tab. |
| **Generate** (Front Matter) | Unlock the configuration. |
| **Include Transcelerator Questions** | The project needs Transcelerator data. |

**What to do:**

1. Hover the mouse over the greyed-out setting. The tooltip often explains it.
2. Look at the table above, and see the chapter about that tab.

### The Help tab has very few links, or links do not open

**Why this happens:** **Disable ALL Internet Use** is ticked on the **Advanced** tab. PTXprint shows "Internet Access Disabled" when you click a web link.

**What to do:**

1. On the **Advanced** tab, **Main** sub-tab, **General** area, untick **Disable ALL Internet Use**.

### PTXprint does not show my projects

**Why this happens:** The **Base Projects Directory** points to the wrong folder.

**What to do:**

1. On the **Help** tab, click **Change...** next to **Base Projects Directory**.
2. Choose the folder that *contains* your Paratext project folders, and click **Use Selected**.

## Getting more help

If your problem is not in this chapter:

1. Read the **Common problems** section in the chapter for the tab you are using.
2. On the **Help** tab, click **Create Report...** and read the warnings and errors.
3. Ask the **Support Agent** or the **PTXprint User Community** (links on the **Help** tab).
4. Make an archive with **Create Archive...** (choose only the book that shows the problem), and email it to **ptxprint_support@sil.org** with a clear description, your PTXprint version and screenshots.
