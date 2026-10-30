## What this part of PTXprint is for

The main window is where you do all your work in PTXprint. It has three parts:

* **The tabs** across the top (**Basic**, **Layout**, **Fonts+Script**, **Body** and so on). Each tab holds one group of settings.
* **The ☰ main menu** button at the top-left corner, before the first tab. It holds settings about PTXprint itself, not about your book: how to show the PDF, the **View Level**, the interface **Language**, and links to **Donate** and **Give Feedback**.
* **The bar at the bottom of the window**, with the **Search for settings** box, the button to open the output folder, the **Quick Run** and **Layout Only** check boxes, and the **Save**, **Print (Make PDF)** and **Quit** buttons.

This chapter also explains three ideas that you need everywhere in PTXprint: **configurations**, **view levels**, and how PTXprint **saves** your settings.

## Projects and configurations

A **project** is a Paratext project – the Scripture text that you want to print. You choose it on the **Basic** tab, in the **Project** list.

A **configuration** (also called a "layout" or "config") is a named set of PTXprint settings for one project. One project can have many configurations, for example `Default` for a draft, `NT_A5` for a small New Testament, and `Large_Print`. Each configuration remembers its own page size, fonts, pictures, styles, front matter and so on.

* Every project has a configuration called **Default**. You cannot delete it, lock it or copy it to other projects, but you can reset it.
* You choose, create, lock, copy and delete configurations on the **Basic** tab, in the **Layout Configuration** area. See the chapter about the Basic tab.
* PTXprint keeps the configurations inside the Paratext project folder. So when you use **Send/Receive** in Paratext, other people on the team get the same configurations.

## How PTXprint saves your settings

* **Save** (or **Ctrl+S**) saves the settings of the current configuration.
* **Print (Make PDF)** (or **Ctrl+P**) **always saves** the settings first, then makes the PDF.
* When you choose a **different project** in the **Project** list, PTXprint saves the current configuration first.
* When you choose a **different configuration** in the **Layout Configuration** list, PTXprint does **not** save the current one first. Click **Save** before you change, or your recent changes are lost.
* **Quit** closes PTXprint **without saving**. Click **Save** or **Print (Make PDF)** before **Quit** to keep your changes.
* If a configuration is **locked** with a password, PTXprint does not save changes to it. You can still change settings on the screen and make a PDF, but the changes are not kept.

Some things are remembered for you (the user), not for the configuration: the view level, the interface language, the **Show PDF** choice and the **Quick Run** setting. These stay the same for all projects and configurations.

## View levels

PTXprint has hundreds of settings. Most people need only a few. So PTXprint can hide the settings that you do not need. This is the **view level**. There are four view levels:

| View level | What you see | Good for |
|---|---|---|
| **Mini** | Only the **Basic**, **Layout**, **Fonts+Script** and **Help** tabs, and only the most important settings on them: project, books, configuration name, page size, font size, two columns, the main font. | A first look at PTXprint, or a quick draft. |
| **Basic** | Adds the **Body**, **Notes+Refs**, **Header+Footer**, **Pictures**, **Peripherals** and **Finishing** tabs, and more settings on each tab (margins, line spacing, bold and italic fonts, the **Import Settings** button…). On **Peripherals** and **Finishing** it shows only the main settings (table of contents and front matter; pages per sheet and comparing PDFs). | Most simple publications. |
| **Regular** | Adds the **Diglot**, **Tabs+Borders**, **Styles**, **Advanced** and **View+Edit** tabs, and many more settings on all tabs. | Most typesetters. PTXprint uses this level the first time it starts. |
| **Full** | Shows every setting, including the **Publications** and **Printers** tabs. | Experienced users who need special settings. |

**How to change the view level:** click the **☰** button (top-left), point to **View Level**, and click **Mini View**, **Basic View**, **Regular View** or **Full View**. The current level is shown in blue and bold in that list. The change happens at once, without a restart.

**Hidden settings still work.** A lower view level only *hides* settings. A hidden setting keeps its value, is still saved with the configuration, and still changes the PDF. For example, if you turned on pictures or a diglot in the **Regular** view and then change to the **Mini** view, the pictures or the diglot are still in the PDF, though you cannot see the tab. If the PDF looks different from what you expect, change to the **Full** view and check the settings again.

**Search finds hidden settings.** If you choose a setting in **Search for settings** that is hidden at your view level, PTXprint changes to a higher view level to show it.

## Tab labels and highlighted settings

PTXprint uses colour and bold text to show what is turned on or changed:

* The open tab has a light blue background and a bold label.
* Some tab labels turn **blue** when their main feature is turned on:
  * **Pictures** – pictures are included.
  * **Diglot** – the diglot is turned on.
  * **Peripherals** – front matter, back matter PDFs or a table of contents is turned on.
  * **Finishing** – more than one page per sheet.
  * **Advanced** – one of its special files or options (custom script, changes file, extra TeX or style files, interlinear) is turned on.
  * **Fonts+Script** – the word "Fonts" is blue when coloured text is enabled.
  * **Notes+Refs** – "Refs" is blue when an extended cross-reference list is used.
  * **Tabs+Borders** – "Tabs" or "Borders" is blue when thumb tabs or decorative borders are turned on.
* Some number settings (mostly on the **Layout** tab: font size, line spacing, margins, column gutter, header and footer positions and similar) have a label that becomes **bold** when the value is different from the PTXprint default. So you can see quickly which values you have changed.

## The bottom bar

From left to right, the bar at the bottom of the window has:

* **Search for settings** – type a word to find a setting.
* **Open folder containing the PDF** – opens the output folder. (Regular and Full views.)
* **Quick Run** and **Layout Only** – two check boxes that make printing faster.
* **Print** – only appears when you are looking at the secondary text of a diglot.
* **Save**, **Print (Make PDF)** and **Quit**.

Above the bar, a **status line** sometimes shows a message from PTXprint (for example "No books to print"). Click **Dismiss** to hide it.

When a newer version of PTXprint is available, a **Check for updates...** button can appear at the top-left, just to the right of the ☰ button. (PTXprint checks at most once a day, only on Windows, and only if Internet use is allowed on the **Advanced** tab.)

## The ☰ main menu

* **Show PDF** – what happens with the PDF after printing:
  * **Preview Pane** – PTXprint shows the PDF in its own preview window. This is the usual choice. PTXprint can also use the preview for some editing tools.
  * **System Viewer** – the PDF opens in the PDF program on your computer.
  * **Output Folder** – PTXprint opens the folder that holds the PDF.
* **View Level** – see "View levels" above.
* **Language** – the language of the PTXprint menus and labels.
* **Donate** and **Give Feedback** – open a web page.

## Common tasks

### See more (or fewer) settings

Click **☰** › **View Level** › **Full View** to see every setting, or **Mini View** to see only the most important ones.

### Find a setting when you do not know which tab it is on

1. Click in the **Search for settings** box at the bottom-left (or press **Ctrl+F**).
2. Type a word, for example `margin` or `footnote`, and press **Enter**.
3. A short list of settings appears above the box. Click the one you want.
4. PTXprint opens the right tab and highlights the setting. If the setting was hidden, PTXprint changes the view level so you can see it.
5. To clear the search, click the small clear icon at the right end of the box.

### Make a PDF

1. On the **Basic** tab, choose the project, the configuration and the books.
2. Click **Print (Make PDF)** (or press **Ctrl+P**).
3. Wait. A progress bar shows that PTXprint is working. Then the PDF appears (in the preview pane, the system viewer or the output folder, depending on **Show PDF**).

### Make the PDF faster while you work on the layout

1. Tick **Quick Run** (or press **Ctrl+Q**).
2. If you only change layout settings (spacing, margins, styles), you can also tick **Layout Only** (Regular and Full views).
3. When the layout is ready, untick **Quick Run** and click **Print (Make PDF)** one more time, so that the table of contents, page references and other details are correct.

### Show the PDF in another program

Click **☰** › **Show PDF** › **System Viewer**.

### Find the PDF file on your computer

Click the **Open folder containing the PDF** button at the bottom of the window (Regular and Full views), or choose **☰** › **Show PDF** › **Output Folder**. The folder with the PDF files for this project opens.

### Change the language of PTXprint

1. Click **Save** first, so you do not lose changes.
2. Click **☰** › **Language** and click a language.
3. PTXprint closes its window and opens it again in the new language, with the same project and configuration.

## Common problems

### A tab or setting that I used before has disappeared

**Likely cause:** The view level is lower than before. **What to do:** Click **☰** › **View Level** › **Regular View** or **Full View**. Or type the name of the setting in **Search for settings**.

### The PDF has pictures (or a diglot, borders, thumb tabs…) but I cannot find the setting

**Likely cause:** The setting was turned on in a higher view level, and now that tab is hidden. Hidden settings still work. **What to do:** Change to **Full View** and turn the feature off on its tab.

### I lost my changes after I chose another configuration

**Likely cause:** PTXprint does not save the current configuration when you choose another one in the **Layout Configuration** list. **What to do:** Always click **Save** (or **Print (Make PDF)**) before you change to another configuration.

### I lost my changes after I clicked Quit

**Likely cause:** **Quit** does not save. **What to do:** Click **Save** before **Quit**.

### The Print (Make PDF) and Save buttons are greyed out

**Likely cause:** PTXprint cannot print yet. For example, no project is selected, or another problem is shown in the status line. **What to do:** Read the message in the status line above the bottom bar. Choose a project on the **Basic** tab and fix the problem that is described.

### PTXprint says "Cannot update PDF file while it is locked!"

**Likely cause:** The old PDF is still open in another PDF program, so PTXprint cannot replace it. **What to do:** Close the PDF in the other program and click to try again. To avoid this, use **☰** › **Show PDF** › **Preview Pane**.

### PTXprint says "No books to print"

**Likely cause:** No book is selected, or the book list is empty. **What to do:** On the **Basic** tab, in **What to Print**, choose a book or click **Select Multiple Books...**.

### PTXprint says "One or more fonts have not been set yet"

**What to do:** On the **Fonts+Script** tab, choose a font for the main text.

### The table of contents or page numbers in the PDF are wrong

**Likely cause:** **Quick Run** is ticked, so PTXprint ran the typesetting only once. **What to do:** Untick **Quick Run** and print again.

### My change to the text in Paratext does not appear in the PDF

**Likely cause:** PTXprint usually notices that the text changed and processes it again, even when **Layout Only** is ticked. If it does not, **Layout Only** may be stopping it. **What to do:** Untick **Layout Only** and print again.

### The changes I make are not kept

**Likely cause:** The configuration is locked with a password, so it is not saved. **What to do:** On the **Basic** tab, click the lock button and enter the password to unlock it. Or use **Save As** to make a new configuration.

## Control notes

### @btn_menu_showPDF
The current choice is shown in blue. When you click a choice, PTXprint uses it at once to show the last PDF, and remembers it for all projects. **Preview Pane** is best for most people: PTXprint can then update the preview itself, and no other program keeps the PDF file open.

### @btn_menu_level
The current level is shown in blue. PTXprint remembers the view level for you, not for each configuration. The first time PTXprint starts, it uses the **Regular View**.

### @btn_menu_lang
The current language is shown in blue. When you choose another language, PTXprint closes and opens its window again in that language, with the same project and configuration. PTXprint saves your settings first (a locked configuration is not saved). This changes only the PTXprint menus and labels, not the language of your book.

### @btn_menu_donate
Opens the SIL donation web page in your web browser. If **Disable ALL Internet Use** is ticked on the **Advanced** tab, PTXprint shows a message instead.

### @btn_menu_feedback
Opens the feedback form in your web browser. It needs Internet access (see **Disable ALL Internet Use** on the **Advanced** tab).

### @lb_Basic
Choose the project, the configuration and the books here. Always visible.

### @lb_Layout
Some number labels on this tab become bold when you change the value from the default.

### @lb_Font
The word "Fonts" in the tab label turns blue when coloured text is enabled.

### @lb_Body
What goes into the main text, and how books and chapters start.

### @lb_NotesRefs
The word "Refs" in the label turns blue when an extended cross-reference list is used.

### @lb_HeadFoot
What appears at the top and bottom of each page.

### @lb_Pictures
The label turns blue when pictures are included in the PDF. In the **Mini** view the tab is hidden, but pictures that are turned on are still printed.

### @lb_Diglot
For printing two (or more) texts side by side. The label turns blue when the diglot is turned on.

### @lb_TabsBorders
"Tabs" or "Borders" in the label turns blue when that feature is turned on.

### @lb_StyleEditor
Change how each USFM marker looks (font, size, spacing, colour…).

### @lb_Advanced
Also holds the **Disable ALL Internet Use** option. The label turns blue when one of its special options is turned on (for example a custom script, a changes file, extra TeX or style files, or interlinear output).

### @lb_Viewer
Look at and edit the front matter, adjust lists, log files and the processed text.

### @lb_Peripherals
Front matter, table of contents, back matter and variables. The label turns blue when front matter, front or back PDFs, or an automatic table of contents is turned on. In the **Basic** view it shows only the table of contents and front matter settings.

### @lb_Publications
Define several publications from one configuration and print them together.

### @lb_Cover
This tab is normally not shown in the main window.

### @lb_Finishing
The label turns blue when more than one page per sheet is chosen. In the **Basic** view it shows only the pages-per-sheet and compare-PDF settings.

### @lb_Printers
The **Printers** tab.

### @lb_Help
Links to folders and to online help. Always visible.

### @lb_Logging
This tab is normally not shown in the main window.

### @btn_menu
The **☰** button at the top-left of the window. It opens the main menu (**Show PDF**, **View Level**, **Language**, **Donate**, **Give Feedback**). Always visible.

### @btn_download_update
Only appears when PTXprint has found a newer version. Opens the download page in your web browser. PTXprint checks for updates at most once a day, only on Windows, and only when Internet use is allowed.

### @btn_dismissStatusLine
Hides the status message above the bottom bar. When the message shows Unicode character codes, this button is called **Copy to Clipboard** and copies the message before it hides it.

### @t_find
Press **Enter** (or click the magnifying-glass icon) to search. Click a result: PTXprint opens the right tab, highlights the setting and, if needed, raises the view level so you can see it. Click the clear icon at the right end of the box to remove the highlight. Short, simple words (for example `margin`, `caption`, `verse`) work best. While PTXprint is printing, this box shows "Processing...".

### @btn_openFolder
Opens the folder in your file manager. In views where this button is hidden, use **☰** › **Show PDF** › **Output Folder**.

### @c_quickRun
Without it, PTXprint runs the typesetting several times (up to 5) so that the table of contents, cross-page details and page layout are correct. With it, it runs only once. Tick it while you try out settings. Untick it for the final PDF. PTXprint remembers this setting for you, not for the configuration.

### @c_noupdate
Faster when you only change layout, spacing or style settings. Settings that change the text include which books, footnotes, or verse numbers to include. If you tick it while the colophon is turned on, PTXprint turns the colophon off.

### @b_print2ndDiglotText
Only appears when the main window shows the secondary project of a diglot (after you switch to it on the **Diglot** tab).

### @btn_saveConfig
Saves all settings of the current configuration, including hidden ones. You do not need it before **Print (Make PDF)**, because printing saves too. Greyed out when PTXprint cannot print (for example when no project is selected) and when the configuration is locked. If you typed a new name in the configuration name box on the **Basic** tab, **Save** creates a new configuration with that name.

### @b_print
First checks that there are books to print and that the main font is set. If an old PDF with the same name is open in another program, PTXprint asks you to close it. While PTXprint is printing, you cannot start another print. When you are looking at the secondary text of a diglot, this button is called **Return to Primary**.

### @b_close
Click **Save** first if you want to keep your changes.
