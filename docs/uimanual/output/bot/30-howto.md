# 4. How do I...? (step-by-step tasks)

## 4.1 How to use this chapter

This chapter gives short, step-by-step answers to the questions people ask most often. A task often uses more than one tab. **See also** names the chapter with more detail.

For every task:

* Most changes appear in the PDF only after you click **Print (Make PDF)** again.
* Lower **view levels** hide many settings. If you cannot see a tab or setting, click **☰** (top-left) › **View Level** › **Full View**, or type its name in the **Search for settings** box (bottom-left).
* Click **Save** before you change to another configuration. PTXprint does not save the current configuration when you choose another one.
* "pt" means point. 1 pt is about 0.35 mm.

## 4.2 Printing: what goes into the PDF

### How do I make a PDF?

1. On the **Basic** tab, choose the **Project**, the configuration (**Name**) and the books.
2. Click **Print (Make PDF)** at the bottom of the window (or press **Ctrl+P**).
3. Wait for the progress bar to finish. The PDF opens in the **PDF Preview** window.

See also: Main window; Basic tab.

### How do I print one book?

1. On the **Basic** tab, in **What to Print**, click **Single Book**.
2. Choose the book, then click **Print (Make PDF)**.

See also: Basic tab.

### How do I print only some chapters of a book?

1. On the **Basic** tab, click **Single Book** and choose the book.
2. Type the first chapter in **From Chapter** and the last in **To**.
3. Click **Print (Make PDF)**.

When you choose another book, PTXprint sets the chapters back to the whole book.

See also: Basic tab.

### How do I print several books?

1. On the **Basic** tab, click **Select Multiple Books...**.
2. Click each book, or a group button: **All Books**, **Old Testament**, **New Testament**, **Deuterocanon** or **Extra Material**. Click a group button again to unselect that group. **Toggle Books** reverses the selection and **Reset All** unselects all. Hold **Shift** and click to select all books between two books.
3. Click **OK**, then **Print (Make PDF)**.

See also: Basic tab.

### How do I print only some passages (for example Psalm 23 and Luke 15)?

1. On the **Basic** tab, click in the box beside **Portions or Multiple Books** (or press **Ctrl+B**).
2. Type references with 3-letter book codes, for example `PSA 23; 100 LUK 15:11-32`. Ranges such as `MAT-ACT` or `GEN 1:1-2:3` also work.
3. Click **Print (Make PDF)**.

Use book codes such as `JHN`, not names such as `John`.

See also: Basic tab.

### How do I make the PDF faster while I am still working on the layout?

1. At the bottom of the window, tick **Quick Run** (or press **Ctrl+Q**).
2. If you only change layout settings (spacing, margins, styles), also tick **Layout Only** (Regular and Full views).
3. For the final PDF, untick both and print again, so the table of contents and page references are correct.

See also: Main window.

### How do I find the PDF file on my computer?

Click **Open folder containing the PDF** at the bottom of the window (Regular and Full views), or **☰** › **Show PDF** › **Output Folder**. Or click the blue link next to **Output PDF Location** on the **Help** tab.

The PDF name starts with the project name, then the configuration name and the books, for example `ABC_NT_A5_MAT-REV_ptxp.pdf`.

See also: Main window; Help tab.

### How do I open the PDF in my normal PDF program instead of the preview?

Click **☰** › **Show PDF** › **System Viewer**. Or, in the **PDF Preview** window, click **Open the PDF in Default PDF Viewer**.

Close the PDF in the other program before you print again. Otherwise PTXprint cannot replace the file.

See also: Main window; PDF Preview window.

### How do I get a Bible text to practise with?

1. On the **Basic** tab, open the **Project** list and choose **Import...** (the last item).
2. Click **Install BSB**. PTXprint installs the Berean Standard Bible and opens it.

In the same dialog you can also install a Scripture text bundle (.zip) from the Digital Bible Library or Open.Bible.

See also: Basic tab.

### How do I learn PTXprint with a tutorial?

1. Choose a practice project and configuration (make one with **Save As**). The tutorial changes its settings.
2. On the **Basic** tab, click **Run Tutorial...** (Basic, Regular and Full views) and choose the tutorial file (.json, or a recorded test in a .zip). You may get one from a trainer.
3. A small tutorial window shows the next step, and PTXprint highlights the control it uses.
4. Click **Step** (or press **Space**) for the next step, **Skip** (**S**) to leave it out, **Play** (**P**) to run the steps one after another, or **Run to end**.
5. Close the tutorial window to stop. If PTXprint raised the view level for the tutorial, it changes it back.

See also: Basic tab.

## 4.3 Page size, margins and columns

### How do I change the page size (for example to A5)?

1. On the **Layout** tab, in **Page Setup**, choose a **Page Size**, for example **148mm, 210mm (A5)**.
2. If **Lines Per Page** is red, click one fine-tune button (see "How do I stop wasting space at the bottom of every page?").
3. Click **Print (Make PDF)**.

Ask your printer for the exact trim size before you start. A change of page size moves every line in the book.

See also: Layout tab.

### How do I use a page size that is not in the list?

1. On the **Layout** tab, click in the **Page Size** box.
2. Type the width, a comma, and the height, for example `140mm, 216mm`. You can use `mm`, `cm` or `in`.
3. Click **Print (Make PDF)**.

The size is saved when you save or print. After that it is in the **Page Size** list for all your projects. To remove a saved size, select it, right-click in the box and choose **Remove**.

See also: Layout tab.

### How do I make the margins smaller?

1. On the **Layout** tab, in **Margins**, make **Side Margin Width (mm)** smaller for the left and right margins.
2. Make **Start of Page to Top of Text (mm)** and **Bottom of Text to End of Page (mm)** smaller for the top and bottom.
3. Check the blue numbers in the margin picture. A very small one means the header or footer is too close to the paper edge.
4. Click **Print (Make PDF)**.

Many printers cannot print closer than about 10 mm to the edge. Ask your printer.

See also: Layout tab.

### How do I change from two columns to one column (or back)?

1. On the **Layout** tab, tick or untick **Two Column Layout**.
2. For two columns, set **Gutter Width (mm)** (the space between the columns) and choose whether you want a **Vertical Rule in Gutter**.
3. Check **Base Indent**. PTXprint halves or doubles it for you.
4. Click **Print (Make PDF)**.

If **Two Column Layout** is greyed out, a diglot is on. A diglot always uses columns.

See also: Layout tab.

### How do I print some books in one column and the rest in two columns?

1. Change to the **Full** view.
2. On the **Body** tab, in **Other Features**, tick **Use One Column Layout for These Books** (it says **Use Two Column Layout** if the publication is one column).
3. Type the book codes in the box beside it, for example `GLO PSA`, and print.

See also: Body tab.

### How do I add extra space at the spine for binding?

1. On the **Layout** tab, in **Page Setup**, tick **Binding Gutter (mm)**.
2. Type the extra space, for example 5 mm. Thicker books need more. Ask your printer.
3. Leave **Outer Gutter** unticked, and print.

See also: Layout tab.

### How do I stop wasting space at the bottom of every page?

1. On the **Layout** tab, look at **Lines Per Page** (Regular and Full views). If it is red, part of a line is empty at the bottom of each page.
2. Click **one** fine-tune button: next to **Base Line Spacing (pt)**, or next to the top or bottom margin in **Margins**.
3. The number turns blue. Click **Print (Make PDF)**.

If **Lock Ratio** is ticked, the line-spacing button also changes the font size a little. Use a margin button to keep the font size.

See also: Layout tab.

### How do I make a journaling Bible with a wide margin for notes?

1. On the **Layout** tab, tick **Notelines** (Regular and Full views).
2. PTXprint ticks **Binding Gutter** and **Outer Gutter** and sets a wide gutter (at least 40 mm).
3. Change the gutter width if needed, choose the line colour with the colour button, and print.

See also: Layout tab; Advanced tab.

## 4.4 Fonts and text size

### How do I change the font?

1. On the **Fonts+Script** tab, click **Select Font...** next to **Regular**.
2. Type part of the font name in the search box, and click the font.
3. Click **OK**. PTXprint fills in **Bold**, **Italic** and **Bold Italic** from the same family.
4. Click **Print (Make PDF)**.

Choose a different bold or italic font **after** the Regular font. Choosing the Regular font again replaces the other three.

See also: Fonts+Script tab.

### How do I make the text bigger or smaller?

1. On the **Layout** tab, in **Page Setup**, make sure **Lock Ratio** is ticked.
2. Change **Base Font Size (pt)**. The line spacing changes with it.
3. If **Lines Per Page** turns red, click one fine-tune button, then print.

All other text (headings, footnotes, verse numbers) changes by the same proportion.

See also: Layout tab.

### How do I put more space between the lines but keep the same letter size?

1. On the **Layout** tab, untick **Lock Ratio**.
2. Make **Base Line Spacing (pt)** larger, for example from 14 to 15.
3. Tick **Lock Ratio** again if you want to keep the new ratio, and print.

See also: Layout tab.

### How do I change the size or font of one kind of text (for example section headings or footnotes)?

1. Open the **Styles** tab (Regular and Full views).
2. Type the marker in **Find**, for example `s1` for section headings, `f` for footnotes or `v` for verse numbers.
3. In **Character Settings**, change **Font Size Factor** (1.0 = normal, 1.2 = 20% bigger). Tick **Bold** or **Italic** if you want.
4. For a different font for this marker only, click **Select Font...**.
5. Click **Print (Make PDF)**.

Each level has its own style: a change to `s1` does not change `s2`. To undo all your changes to a style, click its Reset (circular-arrows) button.

See also: Styles tab.

### How do I fix empty boxes (missing characters) in the PDF?

1. On the **Basic** tab, select as many books as possible.
2. On the **Fonts+Script** tab, tick **Use Fallback Font** (Regular and Full views).
3. Click **Find Missing Characters**. PTXprint lists the characters that the Regular font does not have.
4. Click **Select Font...** next to the list and choose a font that has them. If the label turns red, that font lacks some of them too.
5. Click **Print (Make PDF)**.

A Regular font that has your whole alphabet is often the better solution.

See also: Fonts+Script tab; Problems and solutions.

### How do I get real bold and italic instead of fake ones?

1. On the **Fonts+Script** tab, look at the **Bold**, **Italic** and **Bold Italic** buttons. A style in brackets, for example *(bold)*, is faked.
2. Click **Select Font...** for **Regular** and choose a family that has all four typefaces. **Pick a Font** shows these families in **bold**.
3. Or click **Select Font...** for **Bold** (or **Italic**) and choose a real bold (or italic) typeface from another family.
4. Click **Print (Make PDF)**.

See also: Fonts+Script tab.

### How do I print numbers in my own script's digits?

1. On the **Fonts+Script** tab, click the **Script for Numbers** link.
2. In **Pick a Font**, choose your script in **Digit mapping**. Click **OK**, then print.
3. Check that the font has those digits. If not, you will see empty boxes.

See also: Fonts+Script tab.

### How do I print some text in colour (for example red verse numbers)?

1. On the **Styles** tab, find the marker, for example `v` (verse numbers) or `wj` (words of Jesus).
2. Click the button next to **Color** and choose a colour.
3. PTXprint ticks **Enable Colored Text (as Specified in Stylesheet)** on the **Fonts+Script** tab. Keep it ticked.
4. Click **Print (Make PDF)**.

See also: Styles tab; Fonts+Script tab.

## 4.5 Scripts, languages and hyphenation

### How do I set up a right-to-left script (for example Arabic or Hebrew)?

1. On the **Fonts+Script** tab, choose a font made for your script.
2. In **Writing System**, set **Text Flow Direction** to **Right-to-Left**. PTXprint ticks **RTL Book Binding**.
3. Set **Text Script**, for example **Arabic** or **Hebrew**.
4. If the font needs Graphite, click **Select Font...** for **Regular**, tick **Graphite Rendering**, and click **OK**.
5. Click **Print (Make PDF)**.

See also: Fonts+Script tab.

### How do I set up a script that has no spaces between words (for example Thai or Khmer)?

1. On the **Fonts+Script** tab, set **Text Script** to your script.
2. If your text marks word breaks with `/` (Thai, Lao, Myanmar, Tai Tham, New Tai Lue), nothing more is needed. The `/` marks become invisible break points.
3. Otherwise, tick **Specify Line Break Locale** (Regular and Full views) and type the code, for example `th`, `km`, `my`, `zh`, `ja` or `ko`.
4. Click **Print (Make PDF)**.

See also: Fonts+Script tab.

### How do I turn on hyphenation?

1. In Paratext, approve the hyphenation points in the Wordlist tool.
2. On the **Fonts+Script** tab, in **Hyphenation**, click **Create List...**.
3. Click **OK** in the **Create List** dialog. The message says how many words were used.
4. Tick **Hyphenate**, and print.

If the list is empty, untick **Only Use Approved Hyphenation Words** in the dialog and try again.

See also: Fonts+Script tab.

### How do I choose a different form of a letter that my font offers?

1. On the **Fonts+Script** tab, click **Select Font...** for **Regular**, then **Select Features...**.
2. Choose your language in **Language** (if listed). Then tick or choose the feature.
3. Click **OK** in both dialogs, then print.

See also: Fonts+Script tab.

### How do I print an interlinear text (glosses under each word)?

1. In Paratext, approve the interlinear glosses.
2. Change to the **Full** view.
3. On the **Advanced** tab, **Main** sub-tab, **General** area, tick **Interlinear** and type the language code of the glosses beside it, for example `en`.
4. Click **Print (Make PDF)**.

See also: Advanced tab.

## 4.6 Making the text fit

### How do I make the book fit on fewer pages?

Try these one at a time. Print after each change and compare the page count.

1. **Layout** tab: make **Base Font Size (pt)** a little smaller (with **Lock Ratio** ticked).
2. **Layout** tab: make the margins a little smaller, or tick **Two Column Layout**.
3. **Fonts+Script** tab, **Spacing Adjustments**: make **Min/Shrink** (Between Words) a little smaller.
4. **Notes+Refs** tab: untick **Start Each Footnote on a New Line**. On the **Cross-References** sub-tab, choose **Blend with Footnotes**.
5. **Pictures** tab: make large pictures smaller with **Scale**, or use **Column Width** instead of **Span Width**.
6. **Advanced** tab, **Other** sub-tab, **Page Layout and Spacing**: set **Where to start a new book** to **Same page**.
7. **PDF Preview** window: shrink paragraphs on short last pages (see "How do I fix a page that is not full?").

See also: Layout tab; Fonts+Script tab; Notes+Refs tab.

### How do I fit more text on each line?

1. On the **Fonts+Script** tab, in **Spacing Adjustments**, make **Min/Shrink** (Between Words) a little smaller.
2. Or click **Select Font...** for **Regular** and set **Stretch** a little below 1.00, for example 0.97.
3. Print and check that the text is still easy to read.

See also: Fonts+Script tab.

### How do I start each book on a right-hand page?

1. Change to the **Regular** or **Full** view.
2. On the **Advanced** tab, **Other** sub-tab, open **Page Layout and Spacing**.
3. Set **Where to start a new book** to **Odd page**, and print. PTXprint adds blank pages where needed.

See also: Advanced tab.

### How do I let a new book start on the same page as the end of the previous book?

1. On the **Advanced** tab, **Other** sub-tab, open **Page Layout and Spacing**.
2. Set **Where to start a new book** to **Same page**.
3. If a book still starts on a new page, increase **Page full factor** a little (for example from 0.65 to 0.75), and print.

See also: Advanced tab.

## 4.7 Scripture text: headings, numbers and other content

### How do I remove (or add back) the section headings?

On the **Body** tab, in **Include Scripture Text**, untick (or tick) **Headings**, and print. Unticking **Headings** also removes the parallel passage references.

See also: Body tab.

### How do I hide the verse numbers or the chapter numbers?

On the **Body** tab, untick **Verse Numbers** or **Chapter numbers**, and print. The header references still work.

See also: Body tab.

### How do I show verse number 1 at the start of each chapter?

On the **Body** tab, untick **Hide First Verse Number** (Regular and Full views), and print.

See also: Body tab.

### How do I leave out the book introductions?

1. On the **Body** tab, in **Beginning and Ending Material**, untick **Book Introductions**.
2. Also untick **Introductory Outlines** to remove the outline. Then print.

To print **only** the introductions, untick **Include Scripture Text** instead. Remember to tick it again later.

See also: Body tab.

### How do I print a draft that has many untranslated verses?

1. On the **Body** tab, in **Include Scripture Text**, tick **Hide Empty Verses**.
2. Tick **Show '...'** if readers should see where text is missing. Then print.

See also: Body tab.

### How do I print "Psalm 1", "Psalm 2" … instead of big chapter numbers?

1. Change to the **Full** view.
2. On the **Body** tab, in **Other Features**, tick **Use Special Features for These Books**.
3. Type `PSA` in the box beside it. (An empty box means **all** books.)
4. In **Chapter Label**, type the word for "Psalm" in your language, and print.

For the books in this list you can also tick **Optimize Layout for Poetry Books**. It lets the columns end at different heights, which often removes large white gaps in Psalms.

See also: Body tab.

### How do I put the verse numbers in the margin?

1. On the **Body** tab, tick **Marginal Verses**.
2. In **Position on Page**, choose **Left**, **Right**, **Inner** or **Outer**.
3. In **Col Width (pts)**, type a width that fits the longest verse number, for example 12–16. Then print.

See also: Body tab.

### How do I change how glossary words are marked in the text?

1. On the **Body** tab, in **Other Features**, open **Glossary Word Appearance**.
2. Choose a style, for example **format as bold**, **star \*before word**, or **star \*before and after\*** for a star on both sides.
3. Click **Print (Make PDF)**.

See also: Body tab.

### How do I leave out one kind of text (for example remarks or a special marker)?

1. On the **Styles** tab, find the marker in **Find**.
2. Untick **Include Contents of Marker**. The marker is now shown with a line through it. Then print.

The text stays in Paratext. Only the PDF changes.

See also: Styles tab.

## 4.8 Footnotes and cross-references

### How do I hide all footnotes?

On the **Notes+Refs** tab, **Footnotes** sub-tab, untick **Include Footnotes**, and print.

See also: Notes+Refs tab.

### How do I remove (or add back) the cross-references?

1. On the **Notes+Refs** tab, **Cross-References** sub-tab, untick (or tick) **Include Cross-References (From Project Text)**.
2. To remove all cross-references, also untick **Use External List of Cross-References** if it is ticked. Then print.

See also: Notes+Refs tab.

### How do I put the footnotes at the end of each book?

On the **Notes+Refs** tab, **Footnotes** sub-tab, under **Placement of Footnotes**, choose **End of Book**, and print. The notes appear after the last chapter of each book.

See also: Notes+Refs tab.

### How do I start each footnote on a new line?

1. On the **Notes+Refs** tab, **Footnotes** sub-tab, tick **Start Each Footnote on a New Line**.
2. For cross-references, tick **Start Each Cross-Reference on a New Line** on the **Cross-References** sub-tab. Then print.

Notes on new lines use more space.

See also: Notes+Refs tab.

### How do I change the footnote callers (the small letters or symbols)?

1. On the **Notes+Refs** tab, **Footnotes** sub-tab, make sure **Show Callers** is ticked.
2. In the box beside it, type the marks separated by commas, with no spaces, for example `*,†,‡,§`.
3. If some notes still show other marks, tick **Override hidden/automatic Footnote caller settings**.
4. Tick **Reset Callers on Page** if the sequence should start again on each page.
5. Print. If the reset does not look right, print a second time.

See also: Notes+Refs tab.

### How do I save space by mixing cross-references with the footnotes?

1. On the **Notes+Refs** tab, **Cross-References** sub-tab, under **Placement of Cross-References**, choose **Blend with Footnotes**.
2. Make sure **Include Footnotes** is ticked on the **Footnotes** sub-tab, and print.

See also: Notes+Refs tab.

### How do I add a column of cross-references from a ready-made list?

1. Change to the **Full** view.
2. On the **Notes+Refs** tab, **Cross-References** sub-tab, tick **Use External List of Cross-References**.
3. Under **Placement of Cross-References**, choose **Column Cross-References**.
4. In **Source for References**, choose a list in **External Refs**, for example **Standard list**.
5. In **Include Refs for Books in**, choose which books the references may point to, for example **New Testament**. Then print.

See also: Notes+Refs tab.

### How do I put footnotes in the side margin, next to their verse?

1. On the **Layout** tab, tick **Margin Notes Col Width (mm)** (Regular and Full views) and type the width of the margin column.
2. On the **Notes+Refs** tab, set **Placement of Footnotes** (and/or **Placement of Cross-References**) to **Side Margin**. Then print.

See also: Layout tab; Notes+Refs tab.

## 4.9 Pictures and maps

### How do I print the pictures that are in my Paratext text?

1. Change to the **Regular** or **Full** view.
2. On the **Pictures** tab, **Global Options** sub-tab, tick **Include Pictures (illustrations)**.
3. Click **Generate...**. If a dialog opens, choose **Append Pictures to PicList From These Books**, keep **Protect existing PicList settings** ticked, and click **OK**.
4. Look for grey rows in the picture table. A grey row means PTXprint cannot find that picture file.
5. Click **Print (Make PDF)**.

See also: Pictures tab.

### How do I add a new picture from the illustration catalogue?

1. On the **Pictures** tab, click **Show Catalogue...**. If you have no image set yet, download one first.
2. Choose the **Image Set**. Type a word in **Search**, or check **Limit to Range of References**, then click **Search + Update Images**.
3. Click the pictures you want, then **Add Images to PicList**.
4. On the **Details** sub-tab, type a **Caption** for each new picture and check its **Anchor Ref**. Then print.

See also: Pictures tab.

### How do I make a picture bigger or smaller?

1. On the **Pictures** tab, click the picture's row, then open the **Details** sub-tab.
2. Change **Frame Size** (**Column Width**, **Span Width**, **Page (in Margins)** or **Page (to Edge)**).
3. Change **Scale**. 100% is the full width of the frame. Then print.

Or, in the **PDF Preview** window, right-click the picture and choose **Shrink by 1 line** or **Grow by 1 line**. A red row in the table means the picture is too tall for the page: make **Scale** smaller.

See also: Pictures tab; PDF Preview window.

### How do I change where a picture sits on the page?

1. Select the picture in the table and open the **Details** sub-tab.
2. Set **Frame Size** first, then **Vertical Position** (for example **Top** or **Bottom**), then **Horizontal Position** (for example **Left**, **Right**, **Inner** or **Outer**). Then print.

Or, in the **PDF Preview** window, right-click the picture and choose **Vertical Position** or **Horizontal Position**.

See also: Pictures tab; PDF Preview window.

### How do I move a picture to an earlier or later page?

1. Select the picture and open the **Details** sub-tab.
2. Change **Anchor Ref** to a verse a few verses earlier (to move it back) or later (to move it forward). Keep the dot: `LUK 2.7`. Then print.

Or right-click the picture in the **PDF Preview** window and choose **Change Anchor Ref**.

See also: Pictures tab; PDF Preview window.

### How do I make the text flow around a small picture?

1. Select the picture. On the **Details** sub-tab, set **Frame Size** to **Column Width**.
2. Set **Vertical Position** to **Cutout** and **Horizontal Position** to **Left** or **Right** (or **Inner**/**Outer**).
3. Set **Scale** to about 40%.
4. Set **Number of Lines** to the line where the picture should start (0 = first line of the paragraph). Then print.

See also: Pictures tab.

### How do I use high-quality pictures for the final PDF?

1. Put the high-resolution files in the project's `local\figures` folder, or tick **Use Other Location** and click **Picture Folder...** to choose their folder.
2. On the **Pictures** tab, **Global Options**, choose **High Resolution (Larger File)**.
3. Print and check that the missing-pictures count is 0.

See also: Pictures tab.

### How do I make a small PDF to send by email?

1. On the **Pictures** tab, **Global Options**, choose **Low Resolution (Smaller File)**. For an even smaller file, choose **Use Place-holders (Smallest PDF File)**: each picture becomes an empty box.
2. On the **Finishing** tab, make sure **PDF Output Format** is **Screen (Quickest)**. Then print.

See also: Pictures tab; Finishing tab.

### How do I add maps?

1. On the **Pictures** tab, click **Add Maps...** (or on the **Peripherals** tab, tick **Include Maps** and click **Add Maps...**).
2. Check **Book Code for Maps** (usually **XXM**).
3. Click **Select Map...** and choose the map file. Type a **Caption** if you want one.
4. Click **Size and Position...** to choose the frame size and position.
5. Click **Add Another Map** for the next map, or **OK - Done!** to finish. Then print.

See also: Pictures tab; Peripherals tab.

### How do I print the copyright credits for the pictures?

1. Change to the **Regular** or **Full** view.
2. On the **Peripherals** tab, tick **Colophon at End of Publication**. Its text normally contains `\zimagecopyrights`. If not, add the line `\pc \zimagecopyrights` (or put it on the copyright page of the front matter).
3. On the **Pictures** tab, **Details** sub-tab, check each picture. Known illustration series show **Automatic**. For other pictures, type the credit in **Copyright Attribution**.
4. Print twice. The first run finds the page of each picture.

See also: Pictures tab; Peripherals tab; View+Edit tab.

### How do I print a small credit line on top of a picture?

1. Select the picture on the **Pictures** tab and open the **Details** sub-tab.
2. Click **© ...**. The **Illustration Credit Overlay** dialog opens.
3. Type the **Image Credit Text**, choose the position, click **OK**, and print.

See also: Pictures tab.

## 4.10 Diglot (two texts side by side)

### How do I make a diglot (two languages side by side)?

1. Make sure both projects print well on their own.
2. Open the primary project. On the **Basic** tab, click **Save As** and give the diglot its own configuration name, for example `Diglot`.
3. On the **Diglot** tab (Regular and Full views), tick **Diglot (or Polyglot)**. Click **Yes** in the message.
4. In the **R** row of the table, choose the second **Project**, then its **Configuration**.
5. Check that the **% Width** values add up to 100 (for example 50 and 50).
6. Choose one short book that is in both projects, and print.

See also: Diglot tab.

### How do I change the column widths in a diglot?

1. On the **Diglot** tab, click the **% Width** cell of each text and type a new value, for example 55 and 45. The numbers must add up to 100.
2. Print and compare the number of pages. Give more width to the text that needs more space.
3. Or select one short book and click **Auto-calculate optimum widths of diglot columns** (diglots with exactly two texts). It prints many times, so it takes a while.

See also: Diglot tab.

### How do I change the font of the second text in a diglot?

1. On the **Diglot** tab, right-click the **R** row and choose **Edit Settings…**.
2. The window now shows the second text's configuration. On the **Fonts+Script** tab, change the font.
3. Click **Return to Primary** (the big button at the bottom), then print.

To change only the font size or line spacing, type it in the **Font Size** or **Spacing** cell of that row on the **Diglot** tab.

See also: Diglot tab.

### How do I print the captions of both texts under a shared picture?

1. On the **Diglot** tab, tick **Captions** in the row of the secondary text. (The **L** text always shows its captions.)
2. Make sure both texts use the same picture file at the same verse. Only then is the picture shared.
3. Print.

Pictures are not shared in the books listed in **Use Serial Layout for These Books**.

See also: Diglot tab.

### How do I put the two texts on facing pages?

1. On the **Diglot** tab, in the **R** row, change **1|2** to **2**.
2. Check that the **Layout** box shows **L,R**.
3. Set **% Width** to 100 for each text, and print.

See also: Diglot tab.

### How do I add a third text (polyglot)?

1. On the **Diglot** tab, right-click in the table and choose **Add a row/text**.
2. Choose the **Project** and **Configuration** for the new row.
3. Right-click a row and choose **Distribute Widths**, then print.

See also: Diglot tab.

### How do I turn a diglot back into a normal (one text) configuration?

1. On the **Diglot** tab, untick **Diglot (or Polyglot)**. The **Save As Monoglot** dialog opens.
2. Type a new configuration name (no spaces) and click **OK**.
3. PTXprint opens the new one-text configuration. The diglot configuration is still there.

See also: Diglot tab.

## 4.11 Thumb tabs, borders and decorations

### How do I add thumb tabs?

1. On the **Basic** tab, select all the books of the publication.
2. On the **Tabs+Borders** tab (Regular and Full views), tick **Thumb Tabs**.
3. Set **Height** and **Length** (for example 8 mm and 15 mm), and choose a dark **Tab Color**.
4. Click **Edit Style** and set a light text colour, for example white. Then print.

See also: Tabs+Borders tab.

### How do I put a decorative border around the text?

1. On the **Tabs+Borders** tab, tick **Ornamental Decorations**, then **Border**.
2. Choose **Dynamic Border**.
3. Click the **\textborder** link. The **Styles** tab opens with the `textborder` style.
4. In **Sidebar Settings**, click **Borders...**. Choose the **Type of Border**, the colours and the **Border Width** (at least 10 pt for ornaments). Click **OK**.
5. On the **Layout** tab, make the margins larger if the border is too close to the text or the paper edge. Then print.

For a ready-made frame, choose **PDF border (Legacy)** in step 2 and click **Select...** to choose the PDF.

See also: Tabs+Borders tab; Styles tab.

### How do I add a decoration at the end of each book?

On the **Tabs+Borders** tab, tick **Ornamental Decorations**, then **End of Book Decoration**. Click **Select...**, choose a PDF graphic, and print.

See also: Tabs+Borders tab.

### How do I put a border around book titles or section headings?

1. On the **Tabs+Borders** tab, tick **Ornamental Decorations**.
2. Tick **Book Title Borders**, or tick **Section Headings** and choose **Dynamic Border**.
3. Click the style link next to it. The **Styles** tab opens.
4. Choose a background colour, and click **Borders...** in **Sidebar Settings** for the border. Then print.

With **PDF border (Legacy)** for section headings, **Shift** moves the graphic: a positive number moves it up.

See also: Tabs+Borders tab.

### How do I decorate the verse numbers?

1. On the **Tabs+Borders** tab, tick **Ornamental Decorations**, then **Verse Number Decorator**.
2. Choose **Verse Border Graphic** and click **Select...** to choose a small PDF graphic. (For Arabic script you can choose **End of Ayah**.)
3. Print. Change **Scale** and **Shift** if the number does not fit.

See also: Tabs+Borders tab.

## 4.12 Front matter, back matter and covers

### How do I add a title page, copyright page and table of contents?

1. On the **Peripherals** tab, tick **Local Front Matter**. If there is no front matter yet, PTXprint makes a **BASIC** one: a title page, a copyright and licence page, and a table of contents.
2. In the **Variables and Values** table, type the values, for example **maintitle** and **subtitle**.
3. Print twice. The table of contents needs two runs.

See also: Peripherals tab; View+Edit tab.

### How do I start the front matter from a different template?

1. Change to the **Regular** or **Full** view.
2. On the **View+Edit** tab, click the **Front Matter** sub-tab.
3. Click **Generate**. Choose **BASIC**, **ADVANCED**, **DIGLOT** or **PARATEXT** (a copy of the FRT book in Paratext), and click **OK**.
4. Click **Edit Variables...**, fill in the values, and print.

**Warning:** **Generate** replaces all of the current front matter. If you have already changed it, click **Cancel**.

See also: View+Edit tab.

### How do I change the text of the title page?

1. On the **View+Edit** tab, click the **Front Matter** sub-tab.
2. If the line says `\mt1 \zvar|maintitle\*`, the title comes from a variable. Click **Edit Variables...** and change **maintitle**.
3. If the line has normal text, change it in the editor.
4. Click outside the text area to save, then print.

See also: View+Edit tab; Peripherals tab.

### How do I set the copyright and licence text?

1. Change to the **Regular** or **Full** view.
2. On the **Basic** tab, click **Copyright & Licensing** to open it.
3. Type the copyright text (type `(c)` for ©), or click **Reload copyright from Paratext project**.
4. Choose or type the **License**.
5. Make sure the front matter or the colophon contains `\zcopyright` and `\zlicense` (the BASIC template has them). Then print.

See also: Basic tab; View+Edit tab.

### How do I turn on the table of contents?

1. On the **Peripherals** tab, tick **Table of Contents** and type the heading in the **Title** box beside it.
2. Choose which book names to show (`\toc1`, `\toc2`, `\toc3`) and the **Leaders** (the dots between the name and the page number) (Regular and Full views).
3. Make sure the front matter contains `\ztoc|main\*` (the BASIC template has it).
4. Print twice.

See also: Peripherals tab; View+Edit tab.

### How do I add a colophon at the end of the book?

1. Change to the **Regular** or **Full** view.
2. On the **Peripherals** tab, tick **Colophon at End of Publication**.
3. Change the text in the colophon box if needed. The button beside it reloads the default text.
4. Tick **Force Page Break Before Colophon** if it must start on a new page. Then print.

When you tick **Local Front Matter** or **Layout Only**, PTXprint unticks the colophon. Check it again afterwards.

See also: Peripherals tab.

### How do I add an existing PDF at the front or the back of the book?

1. Change to the **Regular** or **Full** view.
2. On the **Peripherals** tab, tick **Front Matter PDF(s)** (or **Back Matter PDF(s)**).
3. Click **Select...** beside it and choose one or more PDF files. Then print.

Several files are added in alphabetical order of their file names. Name them `01-title.pdf`, `02-preface.pdf` and so on to control the order. Make the PDF pages the same size as your book pages.

See also: Peripherals tab.

### How do I make a cover?

1. Change to the **Regular** or **Full** view.
2. On the **Peripherals** tab, tick **Local Front Matter** (a cover needs it), then tick **Create Cover Page**.
3. Click **Cover Wizard...**. If the message **Existing cover settings found** appears, click **Delete and Continue** to start a new cover, or **Cancel (keep my settings)** to keep the old cover (the wizard then does not open).
4. Go through the steps: book and spine, picture, background, front cover text, spine text, back cover. Click **Finish** on the **Review** step.
5. Print. The cover is a separate PDF whose name ends with **_cover**. It is shown on the **Cover** tab of the **PDF Preview** window.

**Finish** replaces the cover sections of the front matter, and puts the title, subtitle, language name and ISBN into the variables table. PTXprint keeps your wizard answers, so you can open the wizard again later to change the cover. To fine-tune colours, borders or pictures, click **Front Cover**, **Spine**, **Back Cover** or **Cover Spread** on the **Peripherals** tab.

The spine must be as wide as the book is thick. The wizard can work it out from the page count and paper, and the **Printers** tab (Full view) gives an estimate. Ask your printer for the exact spine width.

See also: Peripherals tab; Printers tab.

## 4.13 Headers, footers and page numbers

### How do I put the page number in the outer corner and the references in the centre?

1. On the **Layout** tab, in **Page Setup**, tick **Mirror Pages**.
2. On the **Header+Footer** tab, set **Outer (Right)** to **Page Number**, **Center** to **Reference Range**, and **Inner (Left)** to **-empty-**.
3. Click **Print (Make PDF)**.

See also: Header+Footer tab.

### How do I mirror the headers for double-sided printing?

1. On the **Layout** tab, in **Page Setup**, tick **Mirror Pages**.
2. On the **Header+Footer** tab, use **Inner (Left)** for the spine side and **Outer (Right)** for the page-edge side. Then print.

With **Mirror Pages** ticked, the inner and outer items change sides on left-hand pages, and **First Reference** and **Last Reference** are swapped there.

See also: Header+Footer tab; Layout tab.

### How do I show verse numbers in the header references?

1. Change to the **Regular** or **Full** view.
2. On the **Header+Footer** tab, under **Include in References**, make sure **Chapter** is ticked.
3. Tick **Verse**, choose **Colon (ch:vs)** or **Period (ch.vs)**, and print.

See also: Header+Footer tab.

### How do I put the page number at the bottom of the page?

1. On the **Header+Footer** tab, set **Center Footer** to **Page Number**.
2. Set the header place that had **Page Number** to **-empty-**, and print.

See also: Header+Footer tab.

### How do I add "DRAFT" and the date (or time) to every page?

1. On the **Header+Footer** tab, open **Center Footer** (or a header place).
2. Choose **Printed on YYYY-MM-DD**, **Date (YYYY-MM-DD)**, **Time (HH:MM)**, or **Date and Time** (useful when you print several drafts on one day).
3. Or type your own text, for example `DRAFT\ \isodate`. Type `\ ` (a backslash and a space) for each space.
4. Click **Print (Make PDF)**. The date and time are those of printing.

For a large "DRAFT" across each page, use a watermark (see "How do I put DRAFT across every page?").

See also: Header+Footer tab.

### How do I start the page numbers at a given number?

1. Change to the **Regular** or **Full** view.
2. On the **Header+Footer** tab, in **Other**, set **Starting Page Number (for Scripture Books)**, for example to 101, and print.

In the front matter you can also use `\resetpagenums` (advanced; see the View+Edit chapter).

See also: Header+Footer tab; View+Edit tab.

### How do I print a page number on the first page of each book?

1. Change to the **Regular** or **Full** view.
2. On the **Header+Footer** tab, in **Other**, tick **Print Page Number at Bottom of Intro Page(s)**, and print.

PTXprint never prints a header on the first page of a book. This setting puts the page number in its footer.

See also: Header+Footer tab.

### How do I put a line under the header?

On the **Layout** tab, in **Margins**, tick **Horizontal Rule**, set **Space between Rule and Top of Text (pt)**, and print.

See also: Layout tab.

## 4.14 Fixing the page layout

### How do I fix a page that is not full (too much white space at the bottom)?

1. Print. The **PDF Preview** window opens.
2. Go to the page. Or tick **Layout Analysis** on the **Content** tab, click **Locate...**, tick **Underfilled Pages**, and click **Locate the next issue**.
3. Find a paragraph on this page or the page before whose last line is very short.
4. Right-click it and choose **Try Shrink -1 line** (or **Shift + left-click** it). This pulls text up from the next page.
5. Wait a few seconds for the update (if **Auto-update** is ticked), or click **Print (Update PDF)**.
6. If nothing changed, try **Shrink Both**, or another paragraph.

Do this last, when all other layout settings are final. Work from the front of the book to the back.

See also: PDF Preview window.

### How do I fix a page that is too full (make text go to the next page)?

1. In the **PDF Preview** window, find a paragraph on that page whose last line is nearly full.
2. Right-click it and choose **Expand +1 line** (or **Shift + right-click** it).
3. Wait for the update, then check this page and the following pages.

See also: PDF Preview window.

### How do I fill all pages automatically?

1. On the **Basic** tab, choose the books to fill, and print once.
2. In the **PDF Preview** window, click the lightning icon (**Show/hide Page Fill tool with progress monitor**) (Regular and Full views).
3. Click **Start Fill** for a fresh start, or **Resume Fill** to keep the existing adjustments. **Start Fill** removes your earlier adjustments for these books.
4. Wait. This can take from minutes to hours.
5. When it has finished, use **Locate the next issue** to find pages that could not be filled, and fix them by hand.

The tool also works for a diglot or polyglot (experimental). It then also tries to keep the columns at the same height. **The cost of imbalance in a polyglot slice** (**Advanced** tab › **Other** › **Automatic Page Filler**) sets how important that is. Check the result carefully.

See also: PDF Preview window; Diglot tab.

### How do I undo paragraph adjustments?

1. In the **PDF Preview** window, right-click the paragraph.
2. Choose **Reset Adjustments**, then **Paragraph**, **Column**, **Page**, **Spread** or **End of Book**.
3. Or, on the **View+Edit** tab, **Adj List** sub-tab, choose the book, select the rows and press **Delete**.
4. Click **Print (Make PDF)**.

See also: PDF Preview window; View+Edit tab.

### How do I work quickly on pages in the middle of a long book?

1. In the **PDF Preview** window, go to the page.
2. Right-click a `\p` or `\m` paragraph at the top of the page and choose **SpeedSlice** (not available for diglots).
3. Type the first word on the page in **First Word on This Page**, and set **Length of Slice** (for example 3 chapters).
4. Click **Enable**. Now each print makes only this part of the book.
5. When you have finished, open **SpeedSlice** again and click **Disable**. Then print the whole book.

Always disable SpeedSlice before you make the final PDF.

See also: PDF Preview window.

### How do I find spacing problems, letters that touch, or missing characters?

1. In the **PDF Preview** window, on the **Content** tab, tick **Layout Analysis**.
2. Look at the coloured marks: red = letters that touch, purple = missing characters, yellow = rivers of white space, light blue-green = wide spaces.
3. Click **Locate...** and tick the kinds of issue you want. Use the arrow buttons to go from page to page.

See also: PDF Preview window.

### How do I see two facing pages together?

In the **PDF Preview** window, tick **Book View** (or press **Ctrl+B**).

See also: PDF Preview window.

## 4.15 Preparing the PDF for a printer

### How do I make a print-ready PDF for a commercial printer (PDF/X, CMYK)?

1. Ask the printer for their requirements: trim size, colour (CMYK, grey or RGB), PDF type (PDF/X-1a or PDF/X-4), crop marks and bleed.
2. On the **Layout** tab, check that **Page Size** is the trim size.
3. On the **Pictures** tab, choose **High Resolution (Larger File)**.
4. On the **Finishing** tab, in **PDF Details**, set **PDF Output Format**. For PDF/X-1a in CMYK, choose **Print-CMYK**. For PDF/X-4, choose **Digital-CMYK (Transparency)** or **Digital-RGB**.
5. Tick **Crop Marks** only if the printer asks for them.
6. Make sure **Pages Per Spread** is **1-up (No booklet)**.
7. Print. The PDF name ends with the format, for example **_CMYK**.

See also: Finishing tab.

### How do I make a black-and-white PDF for printing?

On the **Finishing** tab, set **PDF Output Format** to **Print-Gray (B/W)**, and print. The file name ends with **_BW**.

See also: Finishing tab.

### How do I add crop marks?

On the **Finishing** tab, in **PDF Details**, tick **Crop Marks**, and print.

Each PDF page becomes 0.5 inch (about 12.7 mm) larger on every side, to make room for the marks. Many print-on-demand printers do not want crop marks.

See also: Finishing tab.

### How do I set the bleed for the cover?

1. Change to the **Regular** or **Full** view.
2. On the **Advanced** tab, **Other** sub-tab, open **PDF Options, Covers, Show/Hide**.
3. Set **Cover Bleed (mm)** to the value your printer asks for (often 3–5 mm), and print.

See also: Advanced tab; Finishing tab.

### How do I print an A5 booklet on A4 paper?

1. On the **Layout** tab, set **Page Size** to A5.
2. On the **Finishing** tab, in **Booklet Pagination**, set **Pages Per Spread** to **2-up**.
3. Set **Physical Paper Size** to **210mm, 297mm (A4)**.
4. Print. The new PDF ends with **_2up**.
5. Print it double-sided ("flip on short edge"). Fold the sheets in the middle and staple.

Commercial printers want single pages (**1-up**), not a booklet.

See also: Finishing tab.

### How do I put "DRAFT" across every page?

1. On the **Finishing** tab, in **PDF Details**, tick **Apply Watermark PDF**.
2. Click **Select...** and choose a watermark that matches your page size, for example **A5-Draft.pdf**. Then print.

See also: Finishing tab.

### How do I see what changed since the last PDF?

1. On the **Finishing** tab, tick **Compare PDFs** (or press **Ctrl+R**). PTXprint now always keeps the previous PDF (**_1.pdf**), even if **Number of Previous PDFs to be Kept** is 0.
2. Make your corrections, then print.
3. If there are differences, the **Diff** tab of the **PDF Preview** window shows them in colour: added text in the **New Text** colour (blue at first), removed text in the **Old Text** colour (red at first). Otherwise the status line says why, for example **No differences found**.
4. Untick **Compare PDFs** when you have finished. It makes printing slower.

See also: Finishing tab.

### How do I compare with an older proof, or ignore changes in the margins or headers?

1. To compare with an older PDF (not the last run), click **Select...** in the **Compare PDFs** area and choose it. To go back to the last run, click **Select...** and then **Cancel**.
2. Change to the **Full** view for these options:
   * **Start Page Offset** – when one PDF has extra pages at the start (for example a cover). A positive number skips pages of the **old** PDF, a negative number skips pages of the **new** PDF.
   * **Ignore When Comparing: Headers + Footers** or **Side Margins** – those areas are not compared (shaded grey in the diff PDF). Not used with booklets (more than 1-up) or **Scale to fit**.
   * **Smart Check** – after you changed only the margins or gutter, it lines up each old page with the new one and shows only real changes (words, line breaks).
3. Tick **Compare PDFs** and print.

Both PDFs must have the same page size.

See also: Finishing tab.

### How do I get a price estimate for printing?

1. Make the PDF of the whole book first, so that the page count is right.
2. Change to the **Full** view and open the **Printers** tab.
3. Check **Pages** and **Trim size**. Type the number of **Copies**, and choose **Interior**, **Binding** and **Currency**.
4. Read the **Est. per copy** column. These are estimates only. Always ask the printer for a real quotation.

See also: Printers tab.

## 4.16 Configurations and settings

### How do I save my settings as a new configuration?

1. Click **Save** first, so the new configuration starts from your latest settings.
2. On the **Basic** tab, in **Layout Configuration**, click the **Save As** button (the icon next to **Name**).
3. Type a name, for example `NT_A5`. Use only letters, numbers, `(`, `)`, `_` and `-`. No spaces.
4. Click **OK**. PTXprint changes to the new configuration. The old one stays as it was.

See also: Basic tab.

### How do I replace an existing configuration with my current settings?

1. Click **Save**, then click the **Save As** button on the **Basic** tab.
2. Type the name of the configuration to replace, and tick **Replace it if it already exists**.
3. Click **OK**. PTXprint deletes the old configuration and saves the current settings in its place. This cannot be undone.

The **Default** configuration can never be replaced. The box is unticked each time the dialog opens.

See also: Basic tab.

### How do I change to another configuration without losing my changes?

1. Click **Save** (or **Print (Make PDF)**, which also saves).
2. On the **Basic** tab, choose the other configuration in **Name**.

See also: Basic tab; Main window.

### How do I copy a configuration to other projects?

1. Choose the configuration (not **Default** – it is never copied) and click **Save**.
2. On the **Basic** tab, click **Copy configuration to other projects** (Regular and Full views).
3. Click the target project(s).
4. Choose **Do NOT Replace Existing Config** (the safe choice the first time).
5. Leave **Keep each project's own language-specific variables** ticked, so each project keeps its own titles and language name. Click **OK**.
6. Choose the target project in **Project** and check the copied configuration.

Adjust lists (paragraph adjustments) are not copied.

See also: Basic tab.

### How do I get back the settings that were used to make a PDF?

1. On the **Basic** tab, click **Import Settings...**.
2. Click **PDF file (with embedded settings) or ZIP archive file**, then **Select...**, and choose the PDF.
3. Under **Target**, choose **A New/Existing Project and/or Configuration** and type a new configuration name, for example `FromPDF`. PTXprint ticks **Everything** for a new name.
4. Click **OK**.

This only works if the PDF was made with **Include Config Settings Within PDF** ticked on the **Finishing** tab.

See also: Importing settings; Finishing tab.

### How do I import settings from a ZIP archive?

1. On the **Basic** tab, click **Import Settings...**.
2. Click **PDF file (with embedded settings) or ZIP archive file**, then **Select...**, and choose the ZIP file.
3. Choose the **Target** configuration. A new name is safest.
4. Tick **Everything**, or only the groups you want (into an existing configuration). Click **OK**.

See also: Importing settings.

### How do I copy only some settings (for example only the pictures or the headers) from another configuration?

1. On the **Basic** tab, click **Import Settings...**.
2. Click **A Previously Saved Configuration** and choose the source **Project** and **Configuration**.
3. Choose an **existing** target configuration. (For a new name PTXprint always imports everything.)
4. Change to the **Regular** view if needed, and untick **Everything**.
5. Tick only the group you want, for example **Pictures**, or **Other** and then **Header+Footer settings** on the **Other** tab. Click **OK**.

There is no Undo. If you are not sure, first try it on a copy made with **Save As**.

See also: Importing settings.

### How do I lock a configuration so nobody changes it?

1. On the **Basic** tab, choose the configuration in **Name** (not **Default** – it cannot be locked).
2. Click the **lock** button, type a password (it cannot be empty), and click **OK**. Remember the password.

To unlock, click the lock button again and type the same password. **Cancel** never locks or unlocks.

See also: Basic tab.

### How do I protect a finished layout from accidental changes?

1. Change to the **Full** view.
2. On the **Advanced** tab, **Main** sub-tab, **General** area, tick **Lock UI Layout Settings**. Most **Layout**, **Fonts+Script** and **Styles** settings are now greyed out.
3. Also tick **Lock XeTeX Layout Level** if future PTXprint versions must give exactly the same layout.
4. Untick these boxes when you need to change the layout again.

See also: Advanced tab.

### How do I delete a configuration I do not need?

1. On the **Basic** tab, choose the configuration in **Name**.
2. Click **Delete**. Check that the message names the right configuration, then click **Yes**.
3. PTXprint changes to **Default** and deletes the settings and working files of the old configuration. This cannot be undone.

The PDFs you made from it stay in the output folder. Other configurations are not touched.

See also: Basic tab.

### How do I go back to the PTXprint default settings?

* **Default** configuration: choose **Default** in **Name** and click **Reset** (Regular and Full views; it replaces **Delete**). PTXprint does not ask first. It also removes the files of **Default**, such as its styles and picture list.
* Another configuration: click **Import Settings...** and then **RESET**. Style settings are not reset. Click **Save** if you want to keep the result.

See also: Basic tab; Importing settings.

## 4.17 Finding settings and getting help

### How do I find a setting that I cannot see?

1. Click in the **Search for settings** box at the bottom-left (or press **Ctrl+F**).
2. Type a word, for example `margin` or `footnote`, and press **Enter**.
3. Click the setting in the list. PTXprint opens the right tab, highlights the setting, and raises the view level if needed.

See also: Main window.

### How do I see more (or fewer) settings?

Click **☰** (top-left) › **View Level** › **Mini View**, **Basic View**, **Regular View** or **Full View**.

Hidden settings still work and still change the PDF.

See also: Main window.

### How do I send my project to the support team?

1. Choose the project, configuration and only the book(s) that show the problem.
2. If the problem is not about pictures, untick **Include Pictures (illustrations)** on the **Pictures** tab to make the file smaller.
3. On the **Help** tab, click **Create Archive...**.
4. Choose where to save the ZIP file and click **Save**. PTXprint prints again and then makes the ZIP file.
5. Email it to **ptxprint_support@sil.org** with a description of the problem, your PTXprint version (from **About**) and screenshots.

The archive contains the text of your project. If the text is sensitive, ask your project leader first.

See also: Help tab.

### How do I check the last PDF for warnings and errors?

1. Click **Print (Make PDF)**.
2. On the **Help** tab, click **Create Report...** (or **Show Report Information** in the **PDF Preview** window).
3. The report opens in your web browser. Read the warnings and errors.

See also: Help tab; PDF Preview window.

### How do I change the language of PTXprint's menus?

Click **☰** › **Language** and choose a language. PTXprint saves the configuration and opens again in the new language, with the same project and configuration.

See also: Main window.

### How do I use projects from another Paratext folder?

1. On the **Help** tab, click **Change...** next to **Base Projects Directory**.
2. Choose a folder that PTXprint found, or click **Browse for a different folder…**. Choose the folder that *contains* the project folders.
3. Click **Use Selected**, then choose a project on the **Basic** tab.

See also: Help tab.

### How do I free up disk space?

On the **Help** tab, click **Tidy Up**. PTXprint deletes temporary working folders. Your settings and PDF files are kept.

See also: Help tab.
