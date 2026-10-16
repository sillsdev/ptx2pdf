# How do I...? (step-by-step tasks)

## How to use this chapter

This chapter gives short, step-by-step answers to the questions that people ask most often. Each task often uses more than one tab. The tasks are grouped by topic. At the end of each task, **See also** names the chapter that explains the settings in more detail.

Some things to remember for every task:

* Most changes appear in the PDF only after you click **Print (Make PDF)** again.
* PTXprint hides many settings at the lower **view levels**. If you cannot see a tab or a setting named in a task, click the **☰** button (top-right) › **View Level** › **Full View**. Or type the name of the setting in the **Search for settings** box at the bottom-left of the window.
* Click **Save** before you change to another configuration. PTXprint does not save the current configuration when you choose another one.
* "pt" means point. 1 pt is about 0.35 mm.

## Printing: what goes into the PDF

### How do I make a PDF?

1. On the **Basic** tab, choose the **Project**, the configuration (**Name**) and the books.
2. Click **Print (Make PDF)** at the bottom of the window (or press **Ctrl+P**).
3. Wait until the progress bar has finished. The PDF opens in the **PDF Preview** window.

See also: The main window; The Basic tab.

### How do I print one book?

1. On the **Basic** tab, in **What to Print**, click **Single Book**.
2. Choose the book in the list.
3. Click **Print (Make PDF)**.

See also: The Basic tab.

### How do I print only some chapters of a book?

1. On the **Basic** tab, click **Single Book** and choose the book.
2. Type the first chapter in **From Chapter** and the last chapter in **To**.
3. Click **Print (Make PDF)**.

When you choose another book, PTXprint sets the chapters back to the whole book.

See also: The Basic tab.

### How do I print several books?

1. On the **Basic** tab, click **Select Multiple Books...**.
2. Click each book you want, or click a group button such as **New Testament**. Hold **Shift** and click to select all books between two books.
3. Click **OK**.
4. Click **Print (Make PDF)**.

See also: The Basic tab.

### How do I print only some passages (for example Psalm 23 and Luke 15)?

1. On the **Basic** tab, click in the box beside **Portions or Multiple Books** (or press **Ctrl+B**).
2. Type the references with 3-letter book codes, for example `PSA 23; 100 LUK 15:11-32`. You can also type ranges such as `MAT-ACT` or `GEN 1:1-2:3`.
3. Click **Print (Make PDF)**.

Use book codes such as `JHN`, not names such as `John`.

See also: The Basic tab.

### How do I make the PDF faster while I am still working on the layout?

1. At the bottom of the window, tick **Quick Run** (or press **Ctrl+Q**).
2. If you only change layout settings (spacing, margins, styles), also tick **Layout Only** (Default and Full views).
3. When the layout is ready, untick both boxes and click **Print (Make PDF)** again. This makes sure the table of contents and page references are correct.

See also: The main window.

### How do I find the PDF file on my computer?

1. Click the **Open folder containing the PDF** button at the bottom of the window (Default and Full views).
2. Or open the **Help** tab and click the blue link next to **Output PDF Location**.

The PDF name starts with the project name, then the configuration name and the books, for example `ABC_NT_A5_MAT-REV_ptxp.pdf`.

See also: The main window; The Help tab.

### How do I open the PDF in my normal PDF program instead of the preview?

1. Click **☰** › **Show PDF** › **System Viewer**.
2. Or, in the **PDF Preview** window, click **Open the PDF in Default PDF Viewer**.

Close the PDF in the other program before you print again. Otherwise PTXprint cannot replace the file.

See also: The main window; The PDF Preview window.

### How do I get a Bible text to practise with?

1. On the **Basic** tab, open the **Project** list and choose **Import...** (the last item).
2. Click **Install BSB**.
3. PTXprint installs the Berean Standard Bible and opens it.

You can also install a Scripture text bundle (.zip) from the Digital Bible Library or Open.Bible in the same dialog.

See also: The Basic tab.

## Page size, margins and columns

### How do I change the page size (for example to A5)?

1. On the **Layout** tab, in the **Page Setup** area, open the **Page Size** list.
2. Choose a size, for example **148mm, 210mm (A5)**.
3. If the **Lines Per Page** number is red, click one of the fine-tune buttons (see "How do I stop wasting space at the bottom of every page?").
4. Click **Print (Make PDF)**.

Ask your printer for the exact trim size before you start. A change of page size moves every line in the book.

See also: The Layout tab.

### How do I use a page size that is not in the list?

1. On the **Layout** tab, click in the **Page Size** box.
2. Type the width, a comma, and the height, for example `140mm, 216mm`. You can use `mm`, `cm` or `in`.
3. Click **Print (Make PDF)**.

See also: The Layout tab.

### How do I make the margins smaller?

1. On the **Layout** tab, go to the **Margins** area.
2. Make **Side Margin Width (mm)** smaller for the left and right margins.
3. Make **Start of Page to Top of Text (mm)** and **Bottom of Text to End of Page (mm)** smaller for the top and bottom margins.
4. Look at the blue numbers in the margin picture. If one is very small, the header or footer is too close to the edge of the paper.
5. Click **Print (Make PDF)**.

Many printers cannot print closer than about 10 mm to the edge. Ask your printer.

See also: The Layout tab.

### How do I change from two columns to one column (or back)?

1. On the **Layout** tab, tick or untick **Two Column Layout**.
2. For two columns, set **Gutter Width (mm)** (the space between the columns) and choose whether you want a **Vertical Rule in Gutter**.
3. Check **Base Indent**. PTXprint halves or doubles it for you.
4. Click **Print (Make PDF)**.

If **Two Column Layout** is greyed out, a diglot is turned on. A diglot always uses columns.

See also: The Layout tab.

### How do I print some books in one column and the rest in two columns?

1. Change to the **Full** view.
2. On the **Body** tab, in **Other Features**, tick **Use One Column Layout for These Books** (it says **Use Two Column Layout** if the publication is one column).
3. In the box beside it, type the book codes, for example `GLO PSA`.
4. Click **Print (Make PDF)**.

See also: The Body tab.

### How do I add extra space at the spine for binding?

1. On the **Layout** tab, in **Page Setup**, tick **Binding Gutter (mm)**.
2. Type the extra space, for example 5 mm. Thicker books need more. Ask your printer.
3. Leave **Outer Gutter** unticked.
4. Click **Print (Make PDF)**.

See also: The Layout tab.

### How do I stop wasting space at the bottom of every page?

1. On the **Layout** tab, look at the **Lines Per Page** number (Default and Full views).
2. If it is red, part of a line is left empty at the bottom of each page.
3. Click **one** fine-tune button: next to **Base Line Spacing (pt)**, or next to the top or bottom margin in the **Margins** area.
4. The number turns blue. Click **Print (Make PDF)**.

If **Lock Ratio** is ticked, the line-spacing button also changes the font size a little. Use a margin button if you want to keep the font size.

See also: The Layout tab.

### How do I make a journaling Bible with a wide margin for notes?

1. On the **Layout** tab, tick **Notelines** (Default and Full views).
2. PTXprint ticks **Binding Gutter** and **Outer Gutter** and sets a wide gutter (at least 40 mm).
3. Change the gutter width if needed, and choose the line colour with the colour button.
4. Click **Print (Make PDF)**.

See also: The Layout tab; The Advanced tab.

## Fonts and text size

### How do I change the font?

1. On the **Fonts+Script** tab, click the **Select Font...** button next to **Regular**.
2. Type part of the font name in the search box, and click the font.
3. Click **OK**. PTXprint fills in **Bold**, **Italic** and **Bold Italic** from the same font family.
4. Click **Print (Make PDF)**.

If you want a different bold or italic font, choose it **after** the Regular font. Choosing the Regular font again replaces the other three.

See also: The Fonts+Script tab.

### How do I make the text bigger or smaller?

1. On the **Layout** tab, in **Page Setup**, make sure **Lock Ratio** is ticked.
2. Change **Base Font Size (pt)**. The line spacing changes with it, so the page keeps the same look.
3. If **Lines Per Page** turns red, click one fine-tune button.
4. Click **Print (Make PDF)**.

All other text (headings, footnotes, verse numbers) grows or shrinks by the same proportion.

See also: The Layout tab.

### How do I put more space between the lines but keep the same letter size?

1. On the **Layout** tab, untick **Lock Ratio**.
2. Make **Base Line Spacing (pt)** larger, for example from 14 to 15.
3. Tick **Lock Ratio** again if you want to keep the new ratio.
4. Click **Print (Make PDF)**.

See also: The Layout tab.

### How do I change the size or font of one kind of text (for example section headings or footnotes)?

1. Open the **Styles** tab (Default and Full views).
2. Type the marker in the **Find** box, for example `s1` for section headings, `f` for footnotes or `v` for verse numbers.
3. In **Character Settings**, change **Font Size Factor** (1.0 = normal size, 1.2 = 20% bigger). Tick **Bold** or **Italic** if you want.
4. To use a different font for this marker only, click **Select Font...**.
5. Click **Print (Make PDF)**.

Each level has its own style: a change to `s1` does not change `s2`.

See also: The Styles tab.

### How do I fix empty boxes (missing characters) in the PDF?

1. On the **Basic** tab, select as many books as possible.
2. On the **Fonts+Script** tab, tick **Use Fallback Font** (Default and Full views).
3. Click **Find Missing Characters**. PTXprint lists the characters that the Regular font does not have.
4. Click **Select Font...** next to the list and choose a font that has these characters. If the label turns red, that font does not have them all either.
5. Click **Print (Make PDF)**.

A better solution is often a Regular font that has your whole alphabet.

See also: The Fonts+Script tab; Problems and solutions.

### How do I get real bold and italic instead of fake ones?

1. On the **Fonts+Script** tab, look at the **Bold**, **Italic** and **Bold Italic** buttons. A style in brackets, for example *(bold)*, is faked by PTXprint.
2. Click **Select Font...** for **Regular** and choose a font family that has all four typefaces. In the **Pick a Font** list, these families are shown in **bold**.
3. Or click the **Select Font...** button for **Bold** (or **Italic**) and choose a real bold (or italic) typeface from another family.
4. Click **Print (Make PDF)**.

See also: The Fonts+Script tab.

### How do I print numbers in my own script's digits?

1. On the **Fonts+Script** tab, click the **Script for Numbers** link.
2. In the **Pick a Font** dialog, choose your script in **Digit mapping**.
3. Click **OK**, then **Print (Make PDF)**.
4. Check that the font has those digits. If not, you will see empty boxes.

See also: The Fonts+Script tab.

### How do I print some text in colour (for example red verse numbers)?

1. On the **Styles** tab, find the marker, for example `v` for verse numbers or `wj` for the words of Jesus.
2. Click the button next to **Color** and choose a colour.
3. PTXprint ticks **Enable Colored Text (as Specified in Stylesheet)** on the **Fonts+Script** tab. Keep it ticked.
4. Click **Print (Make PDF)**.

See also: The Styles tab; The Fonts+Script tab.

## Scripts, languages and hyphenation

### How do I set up a right-to-left script (for example Arabic or Hebrew)?

1. On the **Fonts+Script** tab, choose a font made for your script.
2. In **Writing System**, set **Text Flow Direction** to **Right-to-Left**. PTXprint ticks **RTL Book Binding** for you.
3. Set **Text Script** to your script, for example **Arabic** or **Hebrew**.
4. If the font needs Graphite, click **Select Font...** for **Regular**, tick **Graphite Rendering**, and click **OK**.
5. Click **Print (Make PDF)**.

See also: The Fonts+Script tab.

### How do I set up a script that has no spaces between words (for example Thai or Khmer)?

1. On the **Fonts+Script** tab, set **Text Script** to your script.
2. If your text marks word breaks with `/` (Thai, Lao, Myanmar, Tai Tham, New Tai Lue), nothing more is needed. The `/` marks become invisible break points.
3. Otherwise, tick **Specify Line Break Locale** and type the code, for example `th`, `km`, `my`, `zh`, `ja` or `ko` (Default and Full views).
4. Click **Print (Make PDF)**.

See also: The Fonts+Script tab.

### How do I turn on hyphenation?

1. In Paratext, approve the hyphenation points in the Wordlist tool.
2. On the **Fonts+Script** tab, in **Hyphenation**, click **Import List...**.
3. Click **OK** in the **Create Hyphenation List** dialog and read the message. It tells you how many words were used.
4. Tick **Hyphenate**.
5. Click **Print (Make PDF)**.

If the list is empty, untick **Only Use Approved Hyphenation Words** in the dialog and try again.

See also: The Fonts+Script tab.

### How do I choose a different form of a letter that my font offers?

1. On the **Fonts+Script** tab, click **Select Font...** for **Regular**.
2. Click **Select Features...**.
3. Choose your language in **Language** (if it is listed). Then tick or choose the feature you want.
4. Click **OK** in both dialogs, then **Print (Make PDF)**.

See also: The Fonts+Script tab.

### How do I print an interlinear text (glosses under each word)?

1. In Paratext, approve the interlinear glosses.
2. Change to the **Full** view.
3. On the **Advanced** tab, **Main** sub-tab, **General** area, tick **Interlinear**.
4. In the box beside it, type the language code of the glosses, for example `en`.
5. Click **Print (Make PDF)**.

See also: The Advanced tab.

## Making the text fit

### How do I make the book fit on fewer pages?

Try one or more of these, one at a time. Print after each change and compare the page count.

1. On the **Layout** tab, make **Base Font Size (pt)** a little smaller (with **Lock Ratio** ticked).
2. On the **Layout** tab, make the margins a little smaller, or tick **Two Column Layout**.
3. On the **Fonts+Script** tab, in **Spacing Adjustments**, make **Min/Shrink** (Between Words) a little smaller.
4. On the **Notes+Refs** tab, untick **Start Each Footnote on a New Line**. On the **Cross-References** sub-tab, choose **Blend with Footnotes**.
5. On the **Pictures** tab, make large pictures smaller with **Scale**, or use **Column Width** instead of **Span Width**.
6. On the **Advanced** tab, **Other** sub-tab, **Page Layout and Spacing**, set **Where to start a new book** to **Same page**.
7. In the **PDF Preview** window, shrink paragraphs on short last pages (see "How do I fix a page that is not full?").

See also: The Layout tab; The Fonts+Script tab; The Notes+Refs tab.

### How do I fit more text on each line?

1. On the **Fonts+Script** tab, in **Spacing Adjustments**, make **Min/Shrink** (Between Words) a little smaller.
2. Or click **Select Font...** for **Regular** and set **Stretch** a little below 1.00, for example 0.97.
3. Click **Print (Make PDF)** and check that the text is still easy to read.

See also: The Fonts+Script tab.

### How do I start each book on a right-hand page?

1. Change to the **Default** or **Full** view.
2. On the **Advanced** tab, **Other** sub-tab, open **Page Layout and Spacing**.
3. Set **Where to start a new book** to **Odd page**.
4. Click **Print (Make PDF)**. PTXprint adds blank pages where needed.

See also: The Advanced tab.

### How do I let a new book start on the same page as the end of the previous book?

1. On the **Advanced** tab, **Other** sub-tab, open **Page Layout and Spacing**.
2. Set **Where to start a new book** to **Same page**.
3. If a book still starts on a new page, increase **Page full factor** a little (for example from 0.65 to 0.75).
4. Click **Print (Make PDF)**.

See also: The Advanced tab.

## Scripture text: headings, numbers and other content

### How do I remove (or add back) the section headings?

1. On the **Body** tab, in **Include Scripture Text**, untick **Headings** to remove them, or tick it to print them.
2. Click **Print (Make PDF)**.

When **Headings** is unticked, the parallel passage references are removed too.

See also: The Body tab.

### How do I hide the verse numbers or the chapter numbers?

1. On the **Body** tab, untick **Verse Numbers** or **Chapter numbers**.
2. Click **Print (Make PDF)**.

The numbers are not printed, but PTXprint still knows the verses. So the header references still work.

See also: The Body tab.

### How do I show verse number 1 at the start of each chapter?

1. On the **Body** tab, untick **Hide First Verse Number** (Default and Full views).
2. Click **Print (Make PDF)**.

See also: The Body tab.

### How do I leave out the book introductions?

1. On the **Body** tab, in **Beginning and Ending Material**, untick **Book Introductions**.
2. Untick **Introductory Outlines** too if you also want to remove the outline.
3. Click **Print (Make PDF)**.

To print **only** the introductions, untick **Include Scripture Text** instead. Remember to tick it again later.

See also: The Body tab.

### How do I print a draft that has many untranslated verses?

1. On the **Body** tab, in **Include Scripture Text**, tick **Hide Empty Verses**.
2. Tick **Show '...'** if readers should see where text is missing.
3. Click **Print (Make PDF)**.

See also: The Body tab.

### How do I print "Psalm 1", "Psalm 2" … instead of big chapter numbers?

1. Change to the **Full** view.
2. On the **Body** tab, in **Other Features**, tick **Use Special Features for These Books**.
3. In the box beside it, type `PSA`. (An empty box means **all** books.)
4. In **Chapter Label**, type the word for "Psalm" in your language.
5. Click **Print (Make PDF)**.

See also: The Body tab.

### How do I put the verse numbers in the margin?

1. On the **Body** tab, tick **Marginal Verses**.
2. In **Position on Page**, choose **Left**, **Right**, **Inner** or **Outer**.
3. In **Col Width (pts)**, type a width that fits the longest verse number, for example 12–16.
4. Click **Print (Make PDF)**.

See also: The Body tab.

### How do I change how glossary words are marked in the text?

1. On the **Body** tab, in **Other Features**, open **Glossary Word Appearance**.
2. Choose a style, for example **format as bold** or **star \*before word**.
3. Click **Print (Make PDF)**.

See also: The Body tab.

### How do I leave out one kind of text (for example remarks or a special marker)?

1. On the **Styles** tab, find the marker in the **Find** box.
2. Untick **Include Contents of Marker**. The marker is now shown with a line through it.
3. Click **Print (Make PDF)**.

The text stays in Paratext. Only the PDF changes.

See also: The Styles tab.

## Footnotes and cross-references

### How do I hide all footnotes?

1. On the **Notes+Refs** tab, **Footnotes** sub-tab, untick **Include Footnotes**.
2. Click **Print (Make PDF)**.

See also: The Notes+Refs tab.

### How do I remove (or add back) the cross-references?

1. On the **Notes+Refs** tab, **Cross-References** sub-tab, untick (or tick) **Include Cross-References (From Project Text)**.
2. If **Use External List of Cross-References** is ticked, untick it too to remove all cross-references.
3. Click **Print (Make PDF)**.

See also: The Notes+Refs tab.

### How do I put the footnotes at the end of each book?

1. On the **Notes+Refs** tab, **Footnotes** sub-tab, under **Placement of Footnotes**, choose **End of Book**.
2. Click **Print (Make PDF)**. The notes appear after the last chapter of each book.

See also: The Notes+Refs tab.

### How do I start each footnote on a new line?

1. On the **Notes+Refs** tab, **Footnotes** sub-tab, tick **Start Each Footnote on a New Line**.
2. For cross-references, tick **Start Each Cross-Reference on a New Line** on the **Cross-References** sub-tab.
3. Click **Print (Make PDF)**.

Notes on new lines use more space.

See also: The Notes+Refs tab.

### How do I change the footnote callers (the small letters or symbols)?

1. On the **Notes+Refs** tab, **Footnotes** sub-tab, make sure **Show Callers** is ticked.
2. In the box beside it, type the marks separated by commas, with no spaces, for example `*,†,‡,§`.
3. If some notes still show other marks, tick **Override hidden/automatic Footnote caller settings**.
4. Tick **Reset Callers on Page** if the sequence should start again on each page.
5. Click **Print (Make PDF)**. If the reset does not look right, print a second time.

See also: The Notes+Refs tab.

### How do I save space by mixing cross-references with the footnotes?

1. On the **Notes+Refs** tab, **Cross-References** sub-tab, under **Placement of Cross-References**, choose **Blend with Footnotes**.
2. Make sure **Include Footnotes** is ticked on the **Footnotes** sub-tab.
3. Click **Print (Make PDF)**.

See also: The Notes+Refs tab.

### How do I add a column of cross-references from a ready-made list?

1. Change to the **Full** view.
2. On the **Notes+Refs** tab, **Cross-References** sub-tab, tick **Use External List of Cross-References**.
3. Under **Placement of Cross-References**, choose **Column Cross-References**.
4. In **Source for References**, choose a list in **External Refs**, for example **Standard list**.
5. In **Include Refs for Books in**, choose which books the references may point to, for example **New Testament**.
6. Click **Print (Make PDF)**.

See also: The Notes+Refs tab.

### How do I put footnotes in the side margin, next to their verse?

1. On the **Layout** tab, tick **Margin Notes Col Width (mm)** and type the width of the margin column (Default and Full views).
2. On the **Notes+Refs** tab, set **Placement of Footnotes** (and/or **Placement of Cross-References**) to **Side Margin**.
3. Click **Print (Make PDF)**.

See also: The Layout tab; The Notes+Refs tab.

## Pictures and maps

### How do I print the pictures that are in my Paratext text?

1. Change to the **Default** or **Full** view.
2. On the **Pictures** tab, **Global Options** sub-tab, tick **Include Pictures (illustrations)**.
3. Click **Generate...**. If a dialog opens, choose **Append Pictures to PicList From These Books**, keep **Protect existing PicList settings** ticked, and click **OK**.
4. Look for grey rows in the picture table. A grey row means PTXprint cannot find that picture file.
5. Click **Print (Make PDF)**.

See also: The Pictures tab.

### How do I add a new picture from the illustration catalogue?

1. On the **Pictures** tab, click **Show Catalogue...**. If you have no image set yet, choose one to download first.
2. Choose the **Image Set**. Type a word in **Search**, or check **Limit to Range of References**, then click **Search + Update Images**.
3. Click the pictures you want, then click **Add Images to PicList**.
4. On the **Details** sub-tab, type a **Caption** for each new picture and check its **Anchor Ref**.
5. Click **Print (Make PDF)**.

See also: The Pictures tab.

### How do I make a picture bigger or smaller?

1. On the **Pictures** tab, click the picture's row in the table, then open the **Details** sub-tab.
2. Change **Frame Size** (**Column Width**, **Span Width**, **Page (in Margins)** or **Page (to Edge)**).
3. Change **Scale**. 100% is the full width of the frame.
4. Click **Print (Make PDF)**.

Or, in the **PDF Preview** window, right-click the picture and choose **Shrink by 1 line** or **Grow by 1 line**. If the row in the table is red, the picture is too tall for the page. Make the **Scale** smaller.

See also: The Pictures tab; The PDF Preview window.

### How do I change where a picture sits on the page?

1. Select the picture in the table and open the **Details** sub-tab.
2. Set **Frame Size** first, then **Vertical Position** (for example **Top** or **Bottom**), then **Horizontal Position** (for example **Left**, **Right**, **Inner** or **Outer**).
3. Click **Print (Make PDF)**.

Or, in the **PDF Preview** window, right-click the picture and choose **Vertical Position** or **Horizontal Position**.

See also: The Pictures tab; The PDF Preview window.

### How do I move a picture to an earlier or later page?

1. Select the picture and open the **Details** sub-tab.
2. Change **Anchor Ref** to a verse a few verses earlier (to move it back) or later (to move it forward). Keep the dot: `LUK 2.7`.
3. Click **Print (Make PDF)**.

Or right-click the picture in the **PDF Preview** window and choose **Change Anchor Ref**.

See also: The Pictures tab; The PDF Preview window.

### How do I make the text flow around a small picture?

1. Select the picture. On the **Details** sub-tab, set **Frame Size** to **Column Width**.
2. Set **Vertical Position** to **Cutout** and **Horizontal Position** to **Left** or **Right** (or **Inner**/**Outer**).
3. Set **Scale** to about 40%.
4. Set **Number of Lines** to the line where the picture should start (0 = first line of the paragraph).
5. Click **Print (Make PDF)**.

See also: The Pictures tab.

### How do I use high-quality pictures for the final PDF?

1. Put the high-resolution files in the project's `local\figures` folder, or tick **Use Other Location** and click **Picture Folder...** to choose their folder.
2. On the **Pictures** tab, **Global Options**, choose **High Resolution (Larger File)**.
3. Click **Print (Make PDF)** and check that the missing-pictures count is 0.

See also: The Pictures tab.

### How do I make a small PDF to send by email?

1. On the **Pictures** tab, **Global Options**, choose **Low Resolution (Smaller File)**.
2. For an even smaller file, choose **Use Place-holders (Smallest PDF File)**. Each picture becomes an empty box.
3. On the **Finishing** tab, make sure **PDF Output Format** is **Screen (Quickest)**.
4. Click **Print (Make PDF)**.

See also: The Pictures tab; The Finishing tab.

### How do I add maps?

1. On the **Pictures** tab, click **Add Maps...** (or on the **Peripherals** tab, tick **Include Maps** and click **Add Maps...**).
2. Check **Book Code for Maps** (usually **XXM**).
3. Click **Select Map...** and choose the map file. Type a **Caption** if you want one.
4. Click **Size and Position...** to choose the frame size and position.
5. Click **Add Another Map** for the next map, or **OK - Done!** to finish.
6. Click **Print (Make PDF)**.

See also: The Pictures tab; The Peripherals tab.

### How do I print the copyright credits for the pictures?

1. Change to the **Default** or **Full** view.
2. On the **Peripherals** tab, tick **Colophon at End of Publication**. The colophon text normally contains `\zimagecopyrights` already. If not, add it on its own line as `\pc \zimagecopyrights`. (Or put the same line on the copyright page of the front matter.)
3. On the **Pictures** tab, **Details** sub-tab, check each picture. For known illustration series PTXprint shows **Automatic**. For other pictures, type the credit in **Copyright Attribution**.
4. Click **Print (Make PDF)** twice. PTXprint needs the first run to find the page of each picture.

See also: The Pictures tab; The Peripherals tab; The View+Edit tab.

### How do I print a small credit line on top of a picture?

1. Select the picture on the **Pictures** tab and open the **Details** sub-tab.
2. Click **© ...**. The **Illustration Credit Overlay** dialog opens.
3. Type the **Image Credit Text** and choose the position.
4. Click **OK**, then **Print (Make PDF)**.

See also: The Pictures tab.

## Diglot (two texts side by side)

### How do I make a diglot (two languages side by side)?

1. Make sure both projects print well on their own.
2. Open the primary project. On the **Basic** tab, click **Save As** and give the diglot its own configuration name, for example `Diglot`.
3. On the **Diglot** tab (Default and Full views), tick **Diglot (or Polyglot)**. Click **Yes** in the message.
4. In the **R** row of the table, choose the second **Project**, then its **Configuration**.
5. Check that the **% Width** values add up to 100 (for example 50 and 50).
6. Choose one short book that is in both projects, and click **Print (Make PDF)**.

See also: The Diglot tab.

### How do I change the column widths in a diglot?

1. On the **Diglot** tab, click the **% Width** cell of each text and type a new value, for example 55 and 45. The numbers must add up to 100.
2. Click **Print (Make PDF)** and compare the number of pages.
3. Or select one short book and click **Auto-calculate optimum widths of diglot columns**. It prints many times, so it takes a while.

Give more width to the text that needs more space.

See also: The Diglot tab.

### How do I change the font of the second text in a diglot?

1. On the **Diglot** tab, right-click the **R** row and choose **Edit Settings…**.
2. The window now shows the second text's configuration. Go to the **Fonts+Script** tab and change the font.
3. Click **Return to Primary** (the big button at the bottom).
4. Click **Print (Make PDF)**.

To change only the font size or line spacing, type it in the **Font Size** or **Spacing** cell of that row on the **Diglot** tab.

See also: The Diglot tab.

### How do I put the two texts on facing pages?

1. On the **Diglot** tab, in the **R** row, change **1|2** to **2**.
2. Check that the **Layout** box shows **L,R**.
3. Set **% Width** to 100 for each text.
4. Click **Print (Make PDF)**.

See also: The Diglot tab.

### How do I add a third text (polyglot)?

1. On the **Diglot** tab, right-click in the table and choose **Add a row/text**.
2. Choose the **Project** and **Configuration** for the new row.
3. Right-click a row and choose **Distribute Widths**.
4. Click **Print (Make PDF)**.

See also: The Diglot tab.

### How do I turn a diglot back into a normal (one text) configuration?

1. On the **Diglot** tab, untick **Diglot (or Polyglot)**. The **Save As Monoglot** dialog opens.
2. Type a new configuration name (no spaces) and click **OK**.
3. PTXprint opens the new one-text configuration. The diglot configuration is still there.

See also: The Diglot tab.

## Thumb tabs, borders and decorations

### How do I add thumb tabs?

1. On the **Basic** tab, select all the books of the publication (multiple books).
2. On the **Tabs+Borders** tab (Default and Full views), tick **Thumb Tabs**.
3. Set **Height** and **Length** (for example 8 mm and 15 mm).
4. Choose a dark **Tab Color**.
5. Click **Edit Style** and set a light text colour, for example white.
6. Click **Print (Make PDF)**.

See also: The Tabs+Borders tab.

### How do I put a decorative border around the text?

1. On the **Tabs+Borders** tab, tick **Ornamental Decorations**, then **Border**.
2. Choose **Dynamic Border**.
3. Go to the **Styles** tab and select the `textborder` style (in the **Other** category).
4. In **Sidebar Settings**, click **Borders...**. Choose the **Type of Border**, the colours and the **Border Width** (at least 10 pt for ornaments). Click **OK**.
5. On the **Layout** tab, make the margins larger if the border is too close to the text or the edge of the paper.
6. Click **Print (Make PDF)**.

For a ready-made frame, choose **PDF border (Legacy)** in step 2 and click **Select...** to choose the PDF.

See also: The Tabs+Borders tab; The Styles tab.

### How do I add a decoration at the end of each book?

1. On the **Tabs+Borders** tab, tick **Ornamental Decorations**, then **End of Book Decoration**.
2. Click **Select...** and choose a PDF graphic.
3. Click **Print (Make PDF)**.

See also: The Tabs+Borders tab.

### How do I put a border around book titles or section headings?

1. On the **Tabs+Borders** tab, tick **Ornamental Decorations**.
2. Tick **Book Title Borders**, or tick **Section Headings** and choose **Dynamic Border**.
3. Click the style link next to it. The **Styles** tab opens.
4. Choose a background colour, and click **Borders...** in **Sidebar Settings** for the border.
5. Click **Print (Make PDF)**.

See also: The Tabs+Borders tab.

### How do I decorate the verse numbers?

1. On the **Tabs+Borders** tab, tick **Ornamental Decorations**, then **Verse Number Decorator**.
2. Choose **Verse Border Graphic** and click **Select...** to choose a small PDF graphic. (For Arabic script you can choose **End of Ayah**.)
3. Click **Print (Make PDF)**. Change **Scale** and **Shift** if the number does not fit.

See also: The Tabs+Borders tab.

## Front matter, back matter and covers

### How do I add a title page, copyright page and table of contents?

1. On the **Peripherals** tab, tick **Local Front Matter**. If there is no front matter yet, PTXprint makes a **BASIC** one. It has a title page, a page with copyright and licence, and a table of contents.
2. In the **Variables and Values** table on the **Peripherals** tab, type the values, for example the **maintitle** and **subtitle**.
3. Click **Print (Make PDF)** twice. The table of contents needs two runs.

See also: The Peripherals tab; The View+Edit tab.

### How do I start the front matter from a different template?

1. Change to the **Default** or **Full** view.
2. On the **View+Edit** tab, click the **Front Matter** sub-tab.
3. Click **Generate**. Choose **BASIC**, **ADVANCED**, **DIGLOT** or **PARATEXT** (a copy of the FRT book in Paratext), and click **OK**.
4. Click **Edit Variables...** and fill in the values.
5. Click **Print (Make PDF)**.

**Warning:** **Generate** replaces all of the front matter that is there now. If you have already changed the front matter, click **Cancel**.

See also: The View+Edit tab.

### How do I change the text of the title page?

1. On the **View+Edit** tab, click the **Front Matter** sub-tab.
2. If the line says `\mt1 \zvar|maintitle\*`, the title comes from a variable. Click **Edit Variables...** and change the value of **maintitle**.
3. If the line has normal text, change the text in the editor.
4. Click outside the text area to save, then click **Print (Make PDF)**.

See also: The View+Edit tab; The Peripherals tab.

### How do I set the copyright and licence text?

1. Change to the **Default** or **Full** view.
2. On the **Basic** tab, click **Copyright & Licensing** to open it.
3. Type the copyright text (type `(c)` for ©), or click **Reload copyright from Paratext project**.
4. Choose or type the **License**.
5. Make sure the front matter or the colophon contains `\zcopyright` and `\zlicense`. The BASIC template already has them.
6. Click **Print (Make PDF)**.

See also: The Basic tab; The View+Edit tab.

### How do I turn on the table of contents?

1. On the **Peripherals** tab, tick **Table of Contents** and type the heading in the **Title** box beside it.
2. Choose which book names to show (`\toc1`, `\toc2`, `\toc3`) and the **Leaders** (the dots between the name and the page number) (Default and Full views).
3. Make sure the front matter contains `\ztoc|main\*`. The BASIC template already has it.
4. Click **Print (Make PDF)** twice.

See also: The Peripherals tab; The View+Edit tab.

### How do I add a colophon at the end of the book?

1. Change to the **Default** or **Full** view.
2. On the **Peripherals** tab, tick **Colophon at End of Publication**.
3. Change the text in the colophon box if needed. The button beside it reloads the default text.
4. Tick **Force Page Break Before Colophon** if it must start on a new page.
5. Click **Print (Make PDF)**.

When you tick **Local Front Matter**, PTXprint may untick the colophon. Check it again after you change the front matter setting.

See also: The Peripherals tab.

### How do I add an existing PDF at the front or the back of the book?

1. Change to the **Default** or **Full** view.
2. On the **Peripherals** tab, tick **Front Matter PDF(s)** (or **Back Matter PDF(s)**).
3. Click **Select...** beside it and choose one or more PDF files.
4. Click **Print (Make PDF)**.

Make the PDF pages the same size as your book pages.

See also: The Peripherals tab.

### How do I make a cover?

1. Change to the **Default** or **Full** view.
2. On the **Peripherals** tab, make sure **Local Front Matter** is ticked. (The cover is turned off when it is not.)
3. Tick **Create Cover Page**.
4. Click **Cover Wizard...** and follow the steps. The Peripherals tab chapter explains each step of the wizard.
5. Click **Print (Make PDF)**. The cover is shown on the **Cover** tab of the **PDF Preview** window.

The cover spine must be as wide as the book is thick. The **Printers** tab (Full view) gives an estimate of the thickness. Ask your printer for the exact spine width.

See also: The Peripherals tab; The Printers tab.

## Headers, footers and page numbers

### How do I put the page number in the outer corner and the references in the centre?

1. On the **Layout** tab, in **Page Setup**, tick **Mirror Pages**.
2. On the **Header+Footer** tab, set **Outer (Right)** to **Page Number**.
3. Set **Center** to **Reference Range**.
4. Set **Inner (Left)** to **-empty-**.
5. Click **Print (Make PDF)**.

See also: The Header+Footer tab.

### How do I mirror the headers for double-sided printing?

1. On the **Layout** tab, in **Page Setup**, tick **Mirror Pages**.
2. On the **Header+Footer** tab, use **Inner (Left)** for the spine side and **Outer (Right)** for the page-edge side.
3. Click **Print (Make PDF)**.

With **Mirror Pages** ticked, the inner and outer items change sides on left-hand pages. PTXprint also swaps **First Reference** and **Last Reference** on left-hand pages.

See also: The Header+Footer tab; The Layout tab.

### How do I show verse numbers in the header references?

1. Change to the **Default** or **Full** view.
2. On the **Header+Footer** tab, under **Include in References**, make sure **Chapter** is ticked.
3. Tick **Verse**, and choose **Colon (ch:vs)** or **Period (ch.vs)**.
4. Click **Print (Make PDF)**.

See also: The Header+Footer tab.

### How do I put the page number at the bottom of the page?

1. On the **Header+Footer** tab, set **Center Footer** to **Page Number**.
2. Set the header place that had **Page Number** to **-empty-**.
3. Click **Print (Make PDF)**.

See also: The Header+Footer tab.

### How do I add "DRAFT" and the date to every page?

1. On the **Header+Footer** tab, open **Center Footer**.
2. Choose **Printed on YYYY-MM-DD**, or type `DRAFT\ \isodate` in the box. (Type `\ ` – a backslash and a space – for each space.)
3. Click **Print (Make PDF)**.

For a large "DRAFT" across each page, use a watermark (see "How do I put DRAFT across every page?").

See also: The Header+Footer tab.

### How do I start the page numbers at a given number?

1. Change to the **Default** or **Full** view.
2. On the **Header+Footer** tab, in **Other**, set **Starting Page Number (for Scripture Books)**, for example to 101.
3. Click **Print (Make PDF)**.

In the front matter you can also use `\resetpagenums` (advanced; see the View+Edit chapter).

See also: The Header+Footer tab; The View+Edit tab.

### How do I print a page number on the first page of each book?

1. Change to the **Default** or **Full** view.
2. On the **Header+Footer** tab, in **Other**, tick **Print Page Number at Bottom of Intro Page(s)**.
3. Click **Print (Make PDF)**.

PTXprint never prints a header on the first page of a book. This setting puts the page number in the footer of that page.

See also: The Header+Footer tab.

### How do I put a line under the header?

1. On the **Layout** tab, in the **Margins** area, tick **Horizontal Rule**.
2. Set **Space between Rule and Top of Text (pt)**.
3. Click **Print (Make PDF)**.

See also: The Layout tab.

## Fixing the page layout

### How do I fix a page that is not full (too much white space at the bottom)?

1. Click **Print (Make PDF)**. The **PDF Preview** window opens.
2. Go to the page. Or tick **Layout Analysis** on the **Content** tab, click **Locate...**, tick **Underfilled Pages**, and click **Locate the next issue**.
3. Find a paragraph on this page or the page before whose last line is very short.
4. Right-click it and choose **Try Shrink -1 line** (or **Shift + left-click** it). This pulls text up from the next page.
5. Wait a few seconds for the PDF to update (if **Auto-update** is ticked), or click **Print (Update PDF)**.
6. If nothing changed, try **Shrink Both**, or try another paragraph.

Do this last, after all other layout settings are final. Work from the front of the book to the back.

See also: The PDF Preview window.

### How do I fix a page that is too full (make text go to the next page)?

1. In the **PDF Preview** window, find a paragraph on that page whose last line is nearly full.
2. Right-click it and choose **Expand +1 line** (or **Shift + right-click** it).
3. Wait for the update, then check this page and the following pages.

See also: The PDF Preview window.

### How do I fill all pages automatically?

1. On the **Basic** tab, choose the books to fill.
2. Click **Print (Make PDF)** once.
3. In the **PDF Preview** window, click the lightning icon (**Show/hide Page Fill tool with progress monitor**) (Default and Full views).
4. Click **Start Fill** for a fresh start, or **Resume Fill** to keep the adjustments that are already there.
5. Wait. This can take from minutes to hours.
6. When it has finished, use **Locate the next issue** to find the pages that could not be filled, and fix them by hand.

**Start Fill** removes your earlier adjustments for these books. Use **Resume Fill** to keep them.

See also: The PDF Preview window.

### How do I undo paragraph adjustments?

1. In the **PDF Preview** window, right-click the paragraph.
2. Choose **Reset Adjustments**, then **Paragraph**, **Column**, **Page**, **Spread** or **End of Book**.
3. Or, on the **View+Edit** tab, **Adj List** sub-tab, choose the book, select the rows and press **Delete**.
4. Click **Print (Make PDF)**.

See also: The PDF Preview window; The View+Edit tab.

### How do I work quickly on pages in the middle of a long book?

1. In the **PDF Preview** window, go to the page.
2. Right-click a `\p` or `\m` paragraph at the top of the page and choose **SpeedSlice**.
3. Type the first word on the page in **First Word on This Page**, and set **Length of Slice** (for example 3 chapters).
4. Click **Enable**. Now each print makes only this part of the book.
5. When you have finished, open **SpeedSlice** again and click **Disable**. Then print the whole book.

Always disable SpeedSlice before you make the final PDF.

See also: The PDF Preview window.

### How do I find spacing problems, letters that touch, or missing characters?

1. In the **PDF Preview** window, on the **Content** tab, tick **Layout Analysis**.
2. Look at the coloured marks: red = letters that touch, purple = missing characters, yellow = rivers of white space, light blue-green = wide spaces.
3. Click **Locate...** and tick the kinds of issue you want. Then use the arrow buttons to go from page to page.

See also: The PDF Preview window.

### How do I see two facing pages together?

1. In the **PDF Preview** window, tick **Book View** (or press **Ctrl+B**).

See also: The PDF Preview window.

## Preparing the PDF for a printer

### How do I make a print-ready PDF for a commercial printer (PDF/X, CMYK)?

1. Ask the printer for their requirements: trim size, colour (CMYK, grey or RGB), PDF type (PDF/X-1a or PDF/X-4), crop marks and bleed.
2. On the **Layout** tab, check that **Page Size** is the trim size.
3. On the **Pictures** tab, choose **High Resolution (Larger File)**.
4. On the **Finishing** tab, in **PDF Details**, set **PDF Output Format**. For PDF/X-1a in CMYK, choose **Print-CMYK**. For PDF/X-4, choose **Digital-CMYK (Transparency)** or **Digital-RGB**.
5. Tick **Crop Marks** only if the printer asks for them.
6. Make sure **Pages Per Spread** is **1-up (No booklet)**.
7. Click **Print (Make PDF)**. The PDF name ends with the format, for example **_CMYK**.

See also: The Finishing tab.

### How do I make a black-and-white PDF for printing?

1. On the **Finishing** tab, set **PDF Output Format** to **Print-Gray (B/W)**.
2. Click **Print (Make PDF)**. The file name ends with **_BW**.

See also: The Finishing tab.

### How do I add crop marks?

1. On the **Finishing** tab, in **PDF Details**, tick **Crop Marks**.
2. Click **Print (Make PDF)**.

Each PDF page becomes 0.5 inch (about 12.7 mm) larger on every side, to make room for the marks. Many print-on-demand printers do not want crop marks.

See also: The Finishing tab.

### How do I set the bleed for the cover?

1. Change to the **Default** or **Full** view.
2. On the **Advanced** tab, **Other** sub-tab, open **PDF Options, Covers, Show/Hide**.
3. Set **Cover Bleed (mm)** to the value your printer asks for (often 3–5 mm).
4. Click **Print (Make PDF)**.

See also: The Advanced tab; The Finishing tab.

### How do I print an A5 booklet on A4 paper?

1. On the **Layout** tab, set **Page Size** to A5.
2. On the **Finishing** tab, in **Booklet Pagination**, set **Pages Per Spread** to **2-up**.
3. Set **Physical Paper Size** to **210mm, 297mm (A4)**.
4. Click **Print (Make PDF)**. The new PDF ends with **_2up**.
5. Print it double-sided ("flip on short edge"). Fold the sheets in the middle and staple.

Commercial printers want single pages (**1-up**), not a booklet.

See also: The Finishing tab.

### How do I put "DRAFT" across every page?

1. On the **Finishing** tab, in **PDF Details**, tick **Apply Watermark PDF**.
2. Click **Select...** beside it and choose a watermark that matches your page size, for example **A5-Draft.pdf**.
3. Click **Print (Make PDF)**.

See also: The Finishing tab.

### How do I see what changed since the last PDF?

1. On the **Finishing** tab, check that **Number of Previous PDFs to be Kept** is at least 1.
2. Tick **Compare PDFs** (or press **Ctrl+R**).
3. Make your corrections, then click **Print (Make PDF)**.
4. A "diff" PDF opens. It shows the changes in colour. If nothing changed, the status line says **No differences found**.

See also: The Finishing tab.

### How do I get a price estimate for printing?

1. Make the PDF of the whole book first, so that the page count is right.
2. Change to the **Full** view and open the **Printers** tab.
3. Check **Pages** and **Trim size**. Type the number of **Copies**, and choose **Interior**, **Binding** and **Currency**.
4. Read the **Est. per copy** column. These are estimates only. Always ask the printer for a real quotation.

See also: The Printers tab.

## Configurations and settings

### How do I save my settings as a new configuration?

1. Click **Save** first, so the new configuration starts from your latest settings.
2. On the **Basic** tab, in **Layout Configuration**, click the **Save As** button (the icon next to **Name**).
3. Type a name, for example `NT_A5`. Use only letters, numbers, `(`, `)`, `_` and `-`. No spaces.
4. Click **OK**. PTXprint changes to the new configuration. The old one stays as it was.

See also: The Basic tab.

### How do I change to another configuration without losing my changes?

1. Click **Save** (or **Print (Make PDF)**, which also saves).
2. On the **Basic** tab, choose the other configuration in **Name**.

See also: The Basic tab; The main window.

### How do I copy a configuration to other projects?

1. Click **Save**.
2. On the **Basic** tab, click the **Copy configuration to other projects** button (Default and Full views).
3. Click the target project(s).
4. Choose **Do NOT Replace Existing Config** (the safe choice the first time), and click **OK**.
5. Choose the target project in **Project** and check the copied configuration.

See also: The Basic tab.

### How do I get back the settings that were used to make a PDF?

1. On the **Basic** tab, click **Import Settings...**.
2. Click **PDF file (with embedded settings) or ZIP archive file**, then **Select...**, and choose the PDF.
3. Under **Target**, choose **A New/Existing Project and/or Configuration** and type a new configuration name, for example `FromPDF`.
4. Make sure **Everything** is ticked (Default and Full views).
5. Click **OK**.

This only works if the PDF was made with **Include Config Settings Within PDF** ticked on the **Finishing** tab.

See also: Importing settings; The Finishing tab.

### How do I import settings from a ZIP archive?

1. On the **Basic** tab, click **Import Settings...**.
2. Click **PDF file (with embedded settings) or ZIP archive file**, then **Select...**, and choose the ZIP file.
3. Choose the **Target** configuration. A new name is safest.
4. Tick **Everything**, or only the groups you want.
5. Click **OK**.

See also: Importing settings.

### How do I copy only some settings (for example only the pictures or the headers) from another configuration?

1. On the **Basic** tab, click **Import Settings...**.
2. Click **A Previously Saved Configuration** and choose the source **Project** and **Configuration**.
3. Change to the **Default** view if needed, and untick **Everything**.
4. Tick only the group you want, for example **Pictures**, or **Other** and then **Header+Footer settings** on the **Other** tab.
5. Click **OK**.

There is no Undo. If you are not sure, import into a new configuration first.

See also: Importing settings.

### How do I lock a configuration so nobody changes it?

1. On the **Basic** tab, choose the configuration in **Name** (not **Default** – it cannot be locked).
2. Click the **lock** button.
3. Type a password and click **OK**. Remember the password.

To unlock, click the lock button again and type the same password.

See also: The Basic tab.

### How do I protect a finished layout from accidental changes?

1. Change to the **Full** view.
2. On the **Advanced** tab, **Main** sub-tab, **General** area, tick **Lock UI Layout Settings**. Most of the **Layout**, **Fonts+Script** and **Styles** settings are now greyed out.
3. Also tick **Lock XeTeX Layout Level** if future PTXprint versions must give exactly the same layout.
4. Untick these boxes when you need to change the layout again.

See also: The Advanced tab.

### How do I delete a configuration I do not need?

1. First copy any PDFs you want to keep to another folder. Click **Open folder containing the PDF** to find them. (See the warning below.)
2. On the **Basic** tab, choose the configuration in **Name**.
3. Click **Delete**, then **Yes**.

**Warning:** when you delete a configuration, PTXprint also empties the project's output folder (the **Output PDF Location** on the **Help** tab). This folder holds the PDFs and temporary files of **all** configurations of this project. The settings of the other configurations are not affected. You can make their PDFs again by printing.

See also: The Basic tab; Problems and solutions.

### How do I go back to the PTXprint default settings?

1. To reset the **Default** configuration: choose **Default** in **Name** and click **Reset** (Default and Full views). PTXprint does not ask first.
2. To reset another configuration: click **Import Settings...** and then **RESET**. Then click **Save** if you want to keep the result.

See also: The Basic tab; Importing settings.

## Finding settings and getting help

### How do I find a setting that I cannot see?

1. Click in the **Search for settings** box at the bottom-left of the window (or press **Ctrl+F**).
2. Type a word, for example `margin` or `footnote`, and press **Enter**.
3. Click the setting in the list. PTXprint opens the right tab and highlights it. If the setting was hidden, PTXprint changes the view level.

See also: The main window.

### How do I see more (or fewer) settings?

1. Click the **☰** button at the top-right of the window.
2. Point to **View Level**.
3. Click **Mini View**, **Basic View**, **Default View** or **Full View**.

Hidden settings still work and still change the PDF.

See also: The main window.

### How do I send my project to the support team?

1. Choose the project, configuration and only the book(s) that show the problem.
2. If the problem is not about pictures, untick **Include Pictures (illustrations)** on the **Pictures** tab to make the file smaller.
3. On the **Help** tab, click **Create Archive...**.
4. Choose where to save the ZIP file and click **Save**. PTXprint prints again and then makes the ZIP file.
5. Email the ZIP file to **ptxprint_support@sil.org** with a description of the problem, your PTXprint version (from **About**) and screenshots.

The archive contains the text of your project. If the text is sensitive, ask your project leader first.

See also: The Help tab.

### How do I check the last PDF for warnings and errors?

1. Click **Print (Make PDF)**.
2. On the **Help** tab, click **Create Report...** (or click **Show Report Information** in the **PDF Preview** window).
3. The report opens in your web browser. Read the warnings and errors.

See also: The Help tab; The PDF Preview window.

### How do I change the language of PTXprint's menus?

1. Click **Save**.
2. Click **☰** › **Language** and choose a language.
3. PTXprint opens again in the new language.

See also: The main window.

### How do I use projects from another Paratext folder?

1. On the **Help** tab, click **Change...** next to **Base Projects Directory**.
2. Choose a folder that PTXprint found, or click **Browse for a different folder…**. Choose the folder that *contains* the project folders.
3. Click **Use Selected**, then choose a project on the **Basic** tab.

See also: The Help tab.

### How do I free up disk space?

1. On the **Help** tab, click **Tidy Up**.
2. PTXprint deletes temporary working folders. Your settings and PDF files are kept.

See also: The Help tab.
