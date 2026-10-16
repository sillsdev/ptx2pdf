# The main window, menu and view levels

## What this part of PTXprint is for

The main window is where you do all your work in PTXprint. It has three parts:

* **The tabs** across the top (**Basic**, **Layout**, **Fonts+Script**, **Body** and so on). Each tab holds one group of settings.
* **The ☰ main menu** button at the top-right corner, next to the tabs. It holds settings about PTXprint itself, not about your book: how to show the PDF, the **View Level**, the interface **Language**, and links to **Donate** and **Give Feedback**.
* **The bar at the bottom of the window**. It holds the **Search for settings** box, the button to open the output folder, the **Quick Run** and **Layout Only** check boxes, and the **Save**, **Print (Make PDF)** and **Quit** buttons.

This chapter also explains three ideas that you need everywhere in PTXprint: **configurations**, **view levels**, and how PTXprint **saves** your settings.

## Projects and configurations

A **project** is a Paratext project – the Scripture text that you want to print. You choose the project on the **Basic** tab, in the **Project** list.

A **configuration** (also called a "layout" or "config") is a named set of PTXprint settings for one project. One project can have many configurations. For example, you can have one configuration called `Default` for a draft, one called `NT_A5` for a small New Testament, and one called `Large_Print`. Each configuration remembers its own page size, fonts, pictures, styles, front matter and so on.

* Every project has a configuration called **Default**. You cannot delete or lock it, but you can reset it.
* You choose, create, lock, copy and delete configurations on the **Basic** tab, in the **Layout Configuration** area. See the chapter about the Basic tab.
* PTXprint keeps the configurations inside the Paratext project folder. So when you use **Send/Receive** in Paratext, other people on the team get the same configurations.

## How PTXprint saves your settings

* Click **Save** (or press **Ctrl+S**) to save the settings of the current configuration.
* Click **Print (Make PDF)** (or press **Ctrl+P**). PTXprint **always saves** the settings first, and then makes the PDF.
* When you choose a **different project** in the **Project** list, PTXprint saves the current configuration first.
* When you choose a **different configuration** in the **Layout Configuration** list, PTXprint does **not** save the current one first. Click **Save** before you change to another configuration, or your recent changes are lost.
* **Quit** closes PTXprint **without saving**. If you want to keep your changes, click **Save** or **Print (Make PDF)** before you click **Quit**.
* If a configuration is **locked** with a password, PTXprint does not save changes to it. You can still change settings on the screen and make a PDF, but the changes are not kept.

Some things are remembered for you (the user) and not for the configuration: the view level, the interface language, the **Show PDF** choice and the **Quick Run** setting. These stay the same for all projects and configurations.

## View levels

PTXprint has hundreds of settings. Most people need only a few of them. So PTXprint can hide the settings that you do not need. This is the **view level**. There are four view levels:

| View level | What you see | Good for |
|---|---|---|
| **Mini** | Only the **Basic**, **Layout**, **Fonts+Script** and **Help** tabs, and only the most important settings on them: project, books, configuration name, page size, font size, two columns, the main font. | A first look at PTXprint, or a quick draft. |
| **Basic** | Adds the **Body**, **Notes+Refs**, **Header+Footer** and **Pictures** tabs, and more settings on each tab (margins, line spacing, bold and italic fonts, the **Import Settings** button…). | Most simple publications. |
| **Default** | Adds the **Diglot**, **Tabs+Borders**, **Styles**, **Advanced**, **View+Edit**, **Peripherals**, **Publications** and **Finishing** tabs, and many more settings on all tabs. | Most typesetters. This is the view level that PTXprint uses the first time it starts. |
| **Full** | Shows every setting, including the **Printers** tab. | Experienced users who need special settings. |

**How to change the view level:** click the **☰** button (top-right), point to **View Level**, and click **Mini View**, **Basic View**, **Default View** or **Full View**. The current level is shown in blue and bold in that list. The change happens at once. You do not need to restart PTXprint.

**Hidden settings still work.** When you change to a lower view level, PTXprint only *hides* the settings. It does not change them. A hidden setting keeps its value, it is still saved with the configuration, and it still changes the PDF. For example, if you turned on pictures or a diglot in the **Default** view and then change to the **Mini** view, the pictures or the diglot will still be in the PDF, even though you cannot see the tab. If the PDF looks different from what you expect, change to the **Full** view and check the settings again.

**Search finds hidden settings.** If you use the **Search for settings** box and choose a setting that is hidden at your view level, PTXprint changes to a higher view level so that it can show you the setting.

## Tab labels and highlighted settings

PTXprint uses colour and bold text to help you see what is turned on or changed:

* The tab that is open now has a light blue background and a bold label.
* Some tab labels turn **blue** when their main feature is turned on. For example: **Pictures** is blue when pictures are included, **Diglot** is blue when the diglot is turned on, **Peripherals** is blue when front matter, back matter PDFs or a table of contents is turned on, **Finishing** is blue when you print more than one page per sheet, and **Advanced** is blue when one of its special files or options (custom script, changes file, extra TeX or style files, interlinear) is turned on. On **Fonts+Script**, the word "Fonts" is blue when coloured text is enabled. On **Notes+Refs**, "Refs" is blue when an extended cross-reference list is used. On **Tabs+Borders**, "Tabs" or "Borders" is blue when thumb tabs or decorative borders are turned on.
* Some number settings (mostly on the **Layout** tab: font size, line spacing, margins, column gutter, header and footer positions and similar) have a label that becomes **bold** when the value is different from the PTXprint default. This helps you see quickly which values you have changed.

## The bottom bar

From left to right, the bar at the bottom of the window has:

* **Search for settings** – type a word to find a setting.
* **Open folder containing the PDF** – opens the output folder. (Default and Full views.)
* **Quick Run** and **Layout Only** – two check boxes that make printing faster.
* **Print** – only appears when you are looking at the secondary text of a diglot.
* **Save**, **Print (Make PDF)** and **Quit**.

Above the bar, a **status line** sometimes appears with a message from PTXprint (for example "No books to print"). Click **Dismiss** to hide it.

When a newer version of PTXprint is available, a **Check for updates...** button can appear at the top-right, next to the ☰ button. (PTXprint checks at most once a day, only on Windows, and only if Internet use is allowed on the **Advanced** tab.)

## The ☰ main menu

* **Show PDF** – choose what happens with the PDF after printing:
  * **Preview Pane** – PTXprint shows the PDF in its own preview window. This is the usual choice. PTXprint can also use the preview for some editing tools.
  * **System Viewer** – the PDF opens in the PDF program on your computer.
  * **Output Folder** – PTXprint opens the folder that holds the PDF.
* **View Level** – see "View levels" above.
* **Language** – the language of the PTXprint menus and labels.
* **Donate** and **Give Feedback** – open a web page.

## Common tasks

### See more (or fewer) settings

1. Click the **☰** button at the top-right of the window.
2. Point to **View Level**.
3. Click **Full View** to see every setting, or **Mini View** to see only the most important ones.

### Find a setting when you do not know which tab it is on

1. Click in the **Search for settings** box at the bottom-left (or press **Ctrl+F**).
2. Type a word, for example `margin` or `footnote`, and press **Enter**.
3. A short list of settings appears above the box. Click the one you want.
4. PTXprint opens the right tab and highlights the setting. If the setting was hidden, PTXprint changes the view level so you can see it.
5. To clear the search, click the small clear icon at the right end of the box.

### Make a PDF

1. On the **Basic** tab, choose the project, the configuration and the books.
2. Click **Print (Make PDF)** (or press **Ctrl+P**).
3. Wait. A progress bar shows that PTXprint is working. When it is finished, the PDF appears (in the preview pane, the system viewer or the output folder, depending on **Show PDF**).

### Make the PDF faster while you work on the layout

1. Tick **Quick Run** (or press **Ctrl+Q**). PTXprint runs the typesetting only once.
2. If you only change layout settings (spacing, margins, styles), you can also tick **Layout Only** (Default and Full views).
3. When the layout is ready, untick **Quick Run** and click **Print (Make PDF)** one more time. This makes sure the table of contents, page references and other details are correct.

### Show the PDF in another program

1. Click **☰** › **Show PDF**.
2. Click **System Viewer**.

### Find the PDF file on your computer

1. Click the **Open folder containing the PDF** button at the bottom of the window (Default and Full views), or choose **☰** › **Show PDF** › **Output Folder**.
2. The folder opens. The PDF files for this project are in it.

### Change the language of PTXprint

1. Click **Save** first, so you do not lose changes.
2. Click **☰** › **Language** and click a language.
3. PTXprint closes its window and opens it again in the new language, with the same project and configuration.

## Common problems

### A tab or setting that I used before has disappeared

**Likely cause:** The view level is lower than before. **What to do:** Click **☰** › **View Level** › **Default View** or **Full View**. Or type the name of the setting in **Search for settings**.

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

**What to do:** Go to the **Fonts+Script** tab and choose a font for the main text.

### The table of contents or page numbers in the PDF are wrong

**Likely cause:** **Quick Run** is ticked, so PTXprint ran the typesetting only once. **What to do:** Untick **Quick Run** and print again.

### My change to the text in Paratext does not appear in the PDF

**Likely cause:** In most cases, PTXprint notices that the text changed and processes it again, even when **Layout Only** is ticked. If it does not, **Layout Only** may be stopping it. **What to do:** Untick **Layout Only** and print again.

### The changes I make are not kept

**Likely cause:** The configuration is locked with a password. A locked configuration is not saved. **What to do:** On the **Basic** tab, click the lock button and enter the password to unlock it. Or use **Save As** to make a new configuration.

## Settings reference: The main window, menu and view levels

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Main menu (top-right ☰ button)

#### Show PDF

- **Where:** Main menu (top-right ☰ button)
- **Type:** Menu button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Choose how the PDF is shown after printing: in the preview pane, in your system's PDF viewer, or by opening the output folder.

**Explanation:**

Opens a small list with three choices: **Preview Pane**, **System Viewer** and **Output Folder**. The choice in blue is the current one. When you click a choice, PTXprint uses it at once to show the last PDF, and it remembers the choice for all projects. **Preview Pane** is the best choice for most people, because PTXprint can then update the preview itself and the PDF file is not kept open by another program.

*(Internal ID: `btn_menu_showPDF`)*

#### View Level

- **Where:** Main menu (top-right ☰ button)
- **Type:** Menu button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Choose how many settings PTXprint shows. Hidden settings keep their values and still take effect.

**Explanation:**

Opens the list of view levels: **Mini View**, **Basic View**, **Default View** and **Full View**. The current level is shown in blue. The view level only changes which settings you can *see*. Hidden settings keep their values and still change the PDF. PTXprint remembers the view level for you (not for each configuration). The first time PTXprint starts, it uses the **Default View**.

*(Internal ID: `btn_menu_level`)*

#### Language

- **Where:** Main menu (top-right ☰ button)
- **Type:** Menu button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Change the language of the PTXprint user interface.

**Explanation:**

Opens the list of languages for the PTXprint interface. The current language is shown in blue. When you choose another language, PTXprint closes and opens its window again in that language, with the same project and configuration. Click **Save** first, because unsaved changes are not kept. This only changes the PTXprint menus and labels, not the language of your book.

*(Internal ID: `btn_menu_lang`)*

#### Donate

- **Where:** Main menu (top-right ☰ button)
- **Type:** Button
- **Description:** Donate toward PTXprint Development
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> PTXprint is a tool that is freely available to all without any restrictions. Our aim is to help people get the Scriptures out to people in formats that work best for their local context.
>
> Click to contribute toward the ongoing development and maintenance of tools by SIL Global's Language Technology Developers so that others can also benefit.
>
> https://give.sil.org/campaign/725128/donate

**Explanation:**

Opens the SIL donation web page in your web browser. If **Disable ALL Internet Use** is ticked on the **Advanced** tab, PTXprint shows a message instead of opening the page.

*(Internal ID: `btn_menu_donate`)*

#### Give Feedback

- **Where:** Main menu (top-right ☰ button)
- **Type:** Button
- **Description:** Link to PTXprint Feedback Form (Google Form)
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Psst! Can we have 5 minutes of your time? You could help us make PTXprint better!
>
> The developers of PTXprint would love to know how this tool is being used. What is your favorite feature? Are there any annoyances? Tell us what you like, or don't like. Tell us what you dream for in the future.
>
> Click this button to fill in the Google form or type this in a browser: https://tiny.cc/ptxprintfeedback

**Explanation:**

Opens a short online form where you can tell the PTXprint developers what you like, what is difficult, and what you would like in the future. It needs Internet access (see **Disable ALL Internet Use** on the **Advanced** tab).

*(Internal ID: `btn_menu_feedback`)*

### Main window

#### Basic

- **Where:** Main window
- **Type:** Label
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Select the Project and Book(s), to be used to create the PDF file.
>
> You can also Save/Share Configuration settings.

**Explanation:**

The **Basic** tab. Here you choose the project, the configuration and the books to print. It is always visible.

*(Internal ID: `lb_Basic`)*

#### Layout

- **Where:** Main window
- **Type:** Label
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Page Setup, Font Size and Line Spacing. Margins, Columns and Rules (lines).

**Explanation:**

The **Layout** tab: page size, font size, line spacing, margins, columns and rules. Some number labels on this tab become bold when you change the value from the default.

*(Internal ID: `lb_Layout`)*

#### Fonts+Script

- **Where:** Main window
- **Type:** Label
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Basic Fonts and Advanced Font options. Also a range of Advanced typography settings to support any Writing System. Advanced Spacing Settings. Fallback fonts for characters missing in primary font.

**Explanation:**

The **Fonts+Script** tab: the fonts and the writing-system (script) settings. The word "Fonts" in the tab label turns blue when coloured text is enabled.

*(Internal ID: `lb_Font`)*

#### Body

- **Where:** Main window
- **Type:** Label
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Main settings to control the beginning and ending of books, and options for what should be included in the Main Body of text. Also settings for special books.

**Explanation:**

The **Body** tab: what goes into the main text and how books and chapters start. Hidden in the **Mini** view.

*(Internal ID: `lb_Body`)*

#### Notes+Refs

- **Where:** Main window
- **Type:** Label
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Control how Footnotes, Cross-references, Study Notes and Questions should appear.

**Explanation:**

The **Notes+Refs** tab: footnotes, cross-references and study notes. The word "Refs" in the label turns blue when an extended cross-reference list is used. Hidden in the **Mini** view.

*(Internal ID: `lb_NotesRefs`)*

#### Header+Footer

- **Where:** Main window
- **Type:** Label
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Adjust the content of headers and footers.

**Explanation:**

The **Header+Footer** tab: what appears at the top and bottom of each page. Hidden in the **Mini** view.

*(Internal ID: `lb_HeadFoot`)*

#### Pictures

- **Where:** Main window
- **Type:** Label
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Manipulate the pictures to be used in the publication. Control everything from quality to position, from captions to copyrights.

**Explanation:**

The **Pictures** tab. The label turns blue when pictures are included in the PDF. Hidden in the **Mini** view, but pictures that are turned on are still printed.

*(Internal ID: `lb_Pictures`)*

#### Diglot

- **Where:** Main window
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Create a diglot publication by selecting a secondary project and configuration.

**Explanation:**

The **Diglot** tab, for printing two (or more) texts side by side. The label turns blue when the diglot is turned on. Only shown in the **Default** and **Full** views.

*(Internal ID: `lb_Diglot`)*

#### Tabs+Borders

- **Where:** Main window
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Settings for thumb-tabs and options to add decorative borders or embellishments to the text.

**Explanation:**

The **Tabs+Borders** tab: thumb tabs at the page edge and decorative borders. "Tabs" or "Borders" in the label turns blue when that feature is turned on. Only shown in the **Default** and **Full** views.

*(Internal ID: `lb_TabsBorders`)*

#### Styles

- **Where:** Main window
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Edit style information of markers without having to edit the USFM stylesheet files.

**Explanation:**

The **Styles** tab, where you change how each USFM marker looks (font, size, spacing, colour…). Only shown in the **Default** and **Full** views.

*(Internal ID: `lb_StyleEditor`)*

#### Advanced

- **Where:** Main window
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Define stylesheets, tex macros, front and back matter PDFs, watermarks and various other advanced settings including interlinear (& ruby text) output.

**Explanation:**

The **Advanced** tab: special files and options for experienced users, and the **Disable ALL Internet Use** option. The label turns blue when one of its special options is turned on (for example a custom script, a changes file, extra TeX or style files, or interlinear output). Only shown in the **Default** and **Full** views.

*(Internal ID: `lb_Advanced`)*

#### View+Edit

- **Where:** Main window
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> View and edit various control and log files. Examine final SFM output and tweak adjust lists.

**Explanation:**

The **View+Edit** tab, where you can look at and edit the front matter, adjust lists, log files and the processed text. Only shown in the **Default** and **Full** views.

*(Internal ID: `lb_Viewer`)*

#### Peripherals

- **Where:** Main window
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Define what material should be placed before and/or after the main scripture pages.

**Explanation:**

The **Peripherals** tab: front matter, table of contents, back matter and variables. The label turns blue when front matter, front or back PDFs, or an automatic table of contents is turned on. Only shown in the **Default** and **Full** views.

*(Internal ID: `lb_Peripherals`)*

#### Publications

- **Where:** Main window
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Define several publications (each with its own books, titles and other variables) from this one configuration, and print them all in one go.

**Explanation:**

The **Publications** tab, where you can define several publications from one configuration and print them together. Only shown in the **Default** and **Full** views.

*(Internal ID: `lb_Publications`)*

#### Cover

- **Where:** Main window
- **Type:** Label
- **View level:** Not normally shown

**Tooltip (the text shown when you hover the mouse over it):**

> Set parameters for the cover of the publication.

**Explanation:**

The label of the **Cover** tab. This tab is normally not shown in the main window.

*(Internal ID: `lb_Cover`)*

#### Finishing

- **Where:** Main window
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Options to control pagination, PDF output format and compare output with a previous PDF.

**Explanation:**

The **Finishing** tab: pagination for printing several pages on one sheet, PDF output format, and comparing with an earlier PDF. The label turns blue when more than one page per sheet is chosen. Only shown in the **Default** and **Full** views.

*(Internal ID: `lb_Finishing`)*

#### Printers

- **Where:** Main window
- **Type:** Label
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Estimate printing costs, compare printers and check the book thickness. Some printers also give live quotations and take orders.

**Explanation:**

The **Printers** tab. It is only shown in the **Full** view.

*(Internal ID: `lb_Printers`)*

#### Help

- **Where:** Main window
- **Type:** Label
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Links to useful folders and online resources. Where to obtain help from others.

**Explanation:**

The **Help** tab, with links to folders and to online help. It is always visible.

*(Internal ID: `lb_Help`)*

#### Log

- **Where:** Main window
- **Type:** Label
- **View level:** Not normally shown

**Tooltip (the text shown when you hover the mouse over it):**

> Display the output log from XeTeX processing.

**Explanation:**

The label of the **Log** tab. This tab is normally not shown in the main window.

*(Internal ID: `lb_Logging`)*

#### btn_menu

- **Where:** Main window
- **Type:** Menu button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Explanation:**

The **☰** button at the top-right of the window. Click it to open the main menu (**Show PDF**, **View Level**, **Language**, **Donate**, **Give Feedback**). It is always visible.

*(Internal ID: `btn_menu`)*

#### Check for updates...

- **Where:** Main window
- **Type:** Button
- **View level:** Not normally shown

**Tooltip (the text shown when you hover the mouse over it):**

> A newer version of PTXprint is available. Click to visit download page on the website.

**Explanation:**

This button only appears when PTXprint has found a newer version. Click it to open the PTXprint download page in your web browser. PTXprint checks for updates at most once a day, only on Windows, and only when Internet use is allowed.

*(Internal ID: `btn_download_update`)*

#### Dismiss

- **Where:** Main window
- **Type:** Button
- **View level:** Not normally shown

**Tooltip (the text shown when you hover the mouse over it):**

> Hide this message.

**Explanation:**

Hides the status message above the bottom bar. When the message shows Unicode character codes, this button is called **Copy to Clipboard** and copies the message before it hides it.

*(Internal ID: `btn_dismissStatusLine`)*

#### Find help

- **Where:** Main window
- **Type:** Text box
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Type in a word to search for a setting that you can't locate. A short list of relevant topics will appear above. Select a topic to jump to the appropriate setting which will be highlighted.
>
> Shortcut: Ctrl-F

**Explanation:**

Type a word and press **Enter** (or click the magnifying-glass icon). A list of matching settings appears above the box. Click one to go to it; PTXprint opens the right tab, highlights the setting and, if needed, raises the view level so you can see it. Click the clear icon at the right end of the box to remove the highlight. Short, simple words (for example `margin`, `caption`, `verse`) work best. While PTXprint is printing, this box shows "Processing...".

*(Internal ID: `t_find`)*

#### Open folder containing the PDF

- **Where:** Main window
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Open the folder which contains the PDF file(s) created for this project.

**Explanation:**

Opens the project's PTXprint output folder in your file manager. The PDF files that PTXprint made for this project are in this folder. Only shown in the **Default** and **Full** views; in other views you can use **☰** › **Show PDF** › **Output Folder**.

*(Internal ID: `btn_openFolder`)*

#### Quick Run

- **Where:** Main window
- **Type:** Checkbox (ticked by default)
- **Description:** Quick run (to speed up process)
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Enabling this option will give quicker output, but it may be less refined.
>
> PTXprint needs to rerun the typesetting process in order to ensure the Table of Contents & other dynamically updated details are accurate.
>
> Shortcut: Ctrl-Q

**Explanation:**

When ticked, PTXprint runs the typesetting only once. Without it, PTXprint runs the typesetting several times (up to 5) so that the table of contents, cross-page details and page layout are correct. Tick it while you are trying out settings. Untick it for the final PDF. PTXprint remembers this setting for you, not for the configuration.

*(Internal ID: `c_quickRun`)*

#### Layout Only

- **Where:** Main window
- **Type:** Checkbox (ticked by default)
- **Description:** Layout Only (skip USFM processing)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Re-runs page layout without regenerating or processing USFM scripture content.
>
> Useful for quick layout tweaks (+1 / −1 spacing or style changes).
>
> PTXprint still re-processes the USFM when the text has changed in Paratext, or when you change a setting that affects the text (the box then shows a dash until the next successful print).
>
> This setting is not saved with the configuration.

**Explanation:**

When ticked, PTXprint skips the step that prepares the USFM text, and only does the page layout again. This is faster when you only change layout, spacing or style settings. PTXprint still prepares the text again when it is needed, for example when the text in Paratext has changed, or when you change a setting that changes the text (such as which books, footnotes, or verse numbers to include). In that case, the box shows a dash until the next successful print. This setting is not saved with the configuration. If you tick it while the colophon is turned on, PTXprint turns the colophon off. Only shown in the **Default** and **Full** views.

*(Internal ID: `c_noupdate`)*

#### Print

- **Where:** Main window
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> The configuration displayed now is for the secondary project of the Diglot. You can use this button to create a PDF with just the secondary text to check the settings specified.
>
> Use the larger 'Return to Primary' button to get back to the primary project in order to print a diglot with both texts.

**Explanation:**

This **Print** button only appears when the main window is showing the secondary project of a diglot (after you switch to it on the **Diglot** tab). It makes a PDF of only the secondary text, so you can check its settings. At this time the large print button is called **Return to Primary**; click that to go back to the primary project and print the full diglot.

*(Internal ID: `b_print2ndDiglotText`)*

#### Save

- **Where:** Main window
- **Type:** Button
- **Description:** Save configuration
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Save current settings in named Configuration (set on the Basic tab).
>
> Shortcut: Ctrl-S

**Explanation:**

Saves all settings of the current configuration, including the hidden ones. You do not need to click it before **Print (Make PDF)**, because printing saves too. It is greyed out when PTXprint cannot print (for example when no project is selected) and when the configuration is locked. If you have typed a new name in the configuration name box on the **Basic** tab, **Save** creates a new configuration with that name.

*(Internal ID: `btn_saveConfig`)*

#### Print (Make PDF)

- **Where:** Main window
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Create the PDF as specified (automatically saves settings).
>
> Shortcut: Ctrl-P

**Explanation:**

Saves the settings and then makes the PDF. It checks first that there are books to print and that the main font is set. If an old PDF with the same name is open in another program, PTXprint asks you to close it. While PTXprint is printing, you cannot start another print. When you are looking at the secondary text of a diglot, this button is called **Return to Primary**.

*(Internal ID: `b_print`)*

#### Quit

- **Where:** Main window
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Close PTXprint without saving.
>
> Shortcut: Ctrl-W

**Explanation:**

Closes PTXprint **without saving** the settings. Click **Save** first if you want to keep your changes.

*(Internal ID: `b_close`)*
