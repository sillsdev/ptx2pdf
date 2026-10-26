# PTXprint User Interface Manual (AI support edition)

Generated 2026-10-26 from the PTXprint source code and the explanations in docs/uimanual/content.

## Notes for the AI support assistant

* This manual covers every setting in the PTXprint window: chapters explain each tab, then a
  *Settings reference* lists every control under headings that give its location
  (tab or dialog › area › setting).
* Most users are **not technical**, and many speak English as a second or third language. Answer in
  short, simple sentences with click-by-click steps, using the on-screen names exactly as written here.
* **Never tell users to edit ptxprint.cfg, .sty or .tex files, or run commands.** Every answer must
  work in the PTXprint window. If something cannot be done there, say so and suggest
  ptxprint_support@sil.org.
* If a user cannot find a setting, check its view level: many settings are hidden in the Mini and
  Basic views (see "View levels"). Some settings are greyed out or hidden until another one is turned on.

### How to read a setting

```
##### <on-screen label>
<type>[, on/off by default] · <view level> · `<internal ID>` · cfg `<config key>`
<extra facts, separated by ·>
> <tooltip>
<explanation>
```

* **View level** – the lowest view that shows it: `Mini+` (all views), `Basic+`, `Regular+`, or
  `Full` (Full view only). `not shown` = hidden in all views; `experimental` = only in experimental mode.
* **Extra facts** – `Values:` range and default · `Choices:` options in a list · `Also:` the setting's
  descriptive name · `Beside:` the label next to it · `Needs:` only usable when that setting is on/selected ·
  `Greyed out by:` unusable while that setting is ticked · `Hidden until:` that box is ticked ·
  `Shown when:` the tab/area appears when that box is ticked.
* Quoted text (`>`) is the tooltip; the paragraph after it is a plain-language explanation.
* The internal ID and config key are for support staff, to match a line in a user's settings file or
  log to the place in the window. Do not ask users about them.


## Contents

1. **About this manual**
   - 1.1 What PTXprint is
   - 1.2 Who this manual is for
   - 1.3 How this manual is organised
   - 1.4 How to read a settings-reference entry
   - 1.5 A short note about view levels
2. **Getting started with PTXprint**
   - 2.1 About this chapter
   - 2.2 Before you start
   - 2.3 Open PTXprint
   - 2.4 Choose the project and the configuration
   - 2.5 Choose the books
   - 2.6 Make your first PDF
   - 2.7 Look at the PDF in the preview
   - 2.8 Change a few common things
   - 2.9 Keep different settings for different outputs
   - 2.10 How PTXprint saves your settings
   - 2.11 Where the PDF is saved
   - 2.12 When something goes wrong
   - 2.13 What to read next
3. **The main window, menu and view levels**
   - 3.1 What this part of PTXprint is for
   - 3.2 Projects and configurations
   - 3.3 How PTXprint saves your settings
   - 3.4 View levels
   - 3.5 Tab labels and highlighted settings
   - 3.6 The bottom bar
   - 3.7 The ☰ main menu
   - 3.8 Common tasks
   - 3.9 Common problems
   - 3.10 Settings reference (Main menu (top-right ☰ button), Main window)
4. **Basic tab**
   - 4.1 What this tab is for
   - 4.2 Project
   - 4.3 Layout Configuration
   - 4.4 What to Print
   - 4.5 Dialogs on this tab
   - 4.6 Common tasks
   - 4.7 Common problems
   - 4.8 Settings reference (Import Scripture... (dialog), Save Current Configuration As... (dialog), Select Books To Export to PDF (dialog), Copy Configuration To... (dialog), Lock/Unlock Configuration (dialog), Basic)
5. **Layout tab**
   - 5.1 What this tab is for
   - 5.2 Page Setup
   - 5.3 Two Column Layout
   - 5.4 Margins
   - 5.5 Change the Grid Settings dialog (graph paper)
   - 5.6 Lock UI Layout Settings
   - 5.7 Common tasks
   - 5.8 Common problems
   - 5.9 Settings reference (Change the Grid Settings (dialog), Layout)
6. **Fonts+Script tab**
   - 6.1 What this tab is for
   - 6.2 Font Configuration
   - 6.3 Pick a Font (and Typeface) dialog
   - 6.4 Use Fallback Font
   - 6.5 Writing System
   - 6.6 Hyphenation
   - 6.7 Spacing Adjustments
   - 6.8 Add Tatweel (kashida) Rules dialog
   - 6.9 Common tasks
   - 6.10 Common problems
   - 6.11 Settings reference (Create List (dialog), Add Tatweel (kashida) Rules (dialog), Pick a Font (and Typeface) (dialog), Select Font Features... (dialog), Fonts+Script)
7. **Body tab**
   - 7.1 What this tab is for
   - 7.2 Beginning and Ending Material
   - 7.3 Include Scripture Text
   - 7.4 Other Features
   - 7.5 Common tasks
   - 7.6 Common problems
   - 7.7 Settings reference (Body)
8. **Notes+Refs tab**
   - 8.1 What this tab is for
   - 8.2 Footnotes
   - 8.3 Cross-References
   - 8.4 Study Notes + Questions
   - 8.5 Generate Strong's Index dialog
   - 8.6 Common tasks
   - 8.7 Common problems
   - 8.8 Settings reference (Generate Strong's Index... (dialog), Notes+Refs)
9. **Header+Footer tab**
   - 9.1 What this tab is for
   - 9.2 Header
   - 9.3 Other
   - 9.4 Footer
   - 9.5 Common tasks
   - 9.6 Common problems
   - 9.7 Settings reference (Header+Footer)
10. **Pictures tab**
   - 10.1 What this tab is for
   - 10.2 The picture table (PicList)
   - 10.3 Global Options
   - 10.4 Details
   - 10.5 Checklist
   - 10.6 Generate PicList dialog
   - 10.7 Select Images dialog (the catalogue)
   - 10.8 Download & Install Image Sets dialog
   - 10.9 Illustration Credit Overlay dialog
   - 10.10 Add Map dialog
   - 10.11 Common tasks
   - 10.12 Common problems
   - 10.13 Settings reference (Generate PicList (dialog), Select Images... (dialog), Download & Install Image Sets (dialog), Illustration Credit Overlay (dialog), Add Map (dialog), Pictures)
11. **Diglot tab (two or more languages)**
   - 11.1 What this tab is for
   - 11.2 Diglot (or Polyglot)
   - 11.3 The texts table
   - 11.4 Layout
   - 11.5 Merging mode
   - 11.6 Column widths and auto-balance
   - 11.7 Notes, headers and other options
   - 11.8 Changing the settings of a secondary text
   - 11.9 What happens to pictures, notes and headers
   - 11.10 Auto Page Fill for diglots and polyglots (experimental)
   - 11.11 Save As Monoglot
   - 11.12 Common tasks
   - 11.13 Common problems
   - 11.14 Settings reference (Save As Monoglot... (dialog), Diglot)
12. **Tabs+Borders tab**
   - 12.1 What this tab is for
   - 12.2 Thumb Tabs
   - 12.3 Ornamental Decorations
   - 12.4 Border Settings dialog
   - 12.5 Common tasks
   - 12.6 Common problems
   - 12.7 Settings reference (Border Settings (dialog), Tabs+Borders)
13. **Styles tab**
   - 13.1 What this tab is for
   - 13.2 The marker list
   - 13.3 Bold setting names: what has changed
   - 13.4 Include Contents of Marker
   - 13.5 Character Settings
   - 13.6 Paragraph Settings
   - 13.7 Other Settings
   - 13.8 Sidebars
   - 13.9 Size and Position Settings (dialog)
   - 13.10 Sidebar Image Settings (dialog)
   - 13.11 Add/Edit Style (dialog)
   - 13.12 Common tasks
   - 13.13 Common problems
   - 13.14 Settings reference (Size and Position Settings (dialog), Sidebar Image Settings (dialog), Add/Edit Style (dialog), Styles)
14. **Advanced tab**
   - 14.1 What this tab is for
   - 14.2 Before you change anything here
   - 14.3 Main sub-tab: Text Processing & Stylesheets
   - 14.4 Main sub-tab: General
   - 14.5 Main sub-tab: Capture tests?
   - 14.6 Other sub-tab: the TeXpert settings
   - 14.7 Common tasks
   - 14.8 Common problems
   - 14.9 Settings reference (Advanced)
15. **View+Edit tab**
   - 15.1 What this tab is for
   - 15.2 The sub-tabs: which files you may edit
   - 15.3 The buttons at the top of the tab
   - 15.4 The Generate button
   - 15.5 The Generate Front Matter dialog
   - 15.6 The front matter and its special codes (advanced)
   - 15.7 The Adj List (adjustment list)
   - 15.8 Common tasks
   - 15.9 Common problems
   - 15.10 Settings reference (Generate Front Matter (dialog), View+Edit)
16. **Peripherals tab (front and back matter)**
   - 16.1 What this tab is for
   - 16.2 Cover
   - 16.3 Front Matter PDF(s) and Back Matter PDF(s)
   - 16.4 Table of Contents
   - 16.5 Local Front Matter
   - 16.6 Maps
   - 16.7 Colophon at End of Publication
   - 16.8 Variables and Values
   - 16.9 Common tasks
   - 16.10 Common problems
   - 16.11 Settings reference (Peripherals)
17. **Publications tab**
   - 17.1 What this tab is for
   - 17.2 The list of publications
   - 17.3 The buttons
   - 17.4 Printing the publications
   - 17.5 Common tasks
   - 17.6 Common problems
   - 17.7 Settings reference (Publications)
18. **Finishing tab**
   - 18.1 What this tab is for
   - 18.2 PDF Details
   - 18.3 Booklet Pagination
   - 18.4 Compare PDFs
   - 18.5 Common tasks
   - 18.6 Common problems
   - 18.7 Settings reference (Finishing)
19. **Printers tab**
   - 19.1 What this tab is for
   - 19.2 Book & Job Specification
   - 19.3 The printer list
   - 19.4 The printer details panels
   - 19.5 Common tasks
   - 19.6 Common problems
   - 19.7 Settings reference (Printers)
20. **PDF Preview window, layout analysis and page filling**
   - 20.1 What this window is for
   - 20.2 Opening and closing the Preview window
   - 20.3 Moving around: pages, spreads and zoom
   - 20.4 The Content tab: what to show on the preview
   - 20.5 Layout Analysis and finding issues
   - 20.6 Adjusting paragraphs with the right-click menu
   - 20.7 Moving and resizing pictures with the right-click menu
   - 20.8 SpeedSlice: work on one part of a long book quickly
   - 20.9 Auto Page Fill and the progress monitor
   - 20.10 The buttons at the bottom of the window
   - 20.11 Common tasks
   - 20.12 Common problems
   - 20.13 Settings reference (PDF Preview > Issue types popup, PDF Preview (dialog), Enter new anchor verse ref (dialog), SpeedSlice (dialog))
21. **Importing settings**
   - 21.1 What this dialog is for
   - 21.2 Source of Settings
   - 21.3 Target
   - 21.4 What to import: the category tabs
   - 21.5 RESET
   - 21.6 Common tasks
   - 21.7 Common problems
   - 21.8 Settings reference (Import Settings... (dialog))
22. **Help tab and getting support**
   - 22.1 What this tab is for
   - 22.2 Links and Help
   - 22.3 How to ask for help
   - 22.4 Log tab
   - 22.5 About dialog
   - 22.6 Common tasks
   - 22.7 Common problems
   - 22.8 Settings reference (Help, Log)
23. **How do I...? (step-by-step tasks)**
   - 23.1 How to use this chapter
   - 23.2 Printing: what goes into the PDF
   - 23.3 Page size, margins and columns
   - 23.4 Fonts and text size
   - 23.5 Scripts, languages and hyphenation
   - 23.6 Making the text fit
   - 23.7 Scripture text: headings, numbers and other content
   - 23.8 Footnotes and cross-references
   - 23.9 Pictures and maps
   - 23.10 Diglot (two texts side by side)
   - 23.11 Thumb tabs, borders and decorations
   - 23.12 Front matter, back matter and covers
   - 23.13 Headers, footers and page numbers
   - 23.14 Fixing the page layout
   - 23.15 Preparing the PDF for a printer
   - 23.16 Configurations and settings
   - 23.17 Finding settings and getting help
24. **Problems and solutions**
   - 24.1 How to use this chapter
   - 24.2 Printing fails or no PDF appears
   - 24.3 The PDF does not change
   - 24.4 Text and fonts
   - 24.5 Layout and spacing
   - 24.6 Pictures
   - 24.7 Notes and cross-references
   - 24.8 Diglot
   - 24.9 Headers, footers and page numbers
   - 24.10 Settings and configurations
   - 24.11 Comparing PDFs
   - 24.12 I cannot find a setting
   - 24.13 Getting more help
25. **Glossary of terms**
   - 25.1 How to use this glossary
   - 25.2 1–9
   - 25.3 A
   - 25.4 B
   - 25.5 C
   - 25.6 D
   - 25.7 E
   - 25.8 F
   - 25.9 G
   - 25.10 H
   - 25.11 I
   - 25.12 J
   - 25.13 K
   - 25.14 L
   - 25.15 M
   - 25.16 N
   - 25.17 O
   - 25.18 P
   - 25.19 Q
   - 25.20 R
   - 25.21 S
   - 25.22 T
   - 25.23 U
   - 25.24 V
   - 25.25 W
   - 25.26 X
   - 25.27 Z


# 1. About this manual

## 1.1 What PTXprint is

PTXprint makes print-ready PDF files of Scripture. It takes the text from a Paratext project and
lays it out on pages: with columns, headings, chapter and verse numbers, footnotes,
cross-references, pictures, headers and footers. You can use the PDF for checking and
proofreading, or send it to a printer to make a book.

PTXprint uses a typesetting program called **XeTeX** to place every letter and line on the page.
You never need to use XeTeX yourself. You make all your choices in the PTXprint window, and
PTXprint tells XeTeX what to do.

PTXprint never changes your Paratext text. It reads the text, makes a temporary copy, and
typesets that copy. To correct the words of the text, use Paratext.

## 1.2 Who this manual is for

This manual is for everyone who uses the PTXprint window: translators, typesetters, project
leaders and support staff. You do not need to know about typesetting or computers.

* Every instruction can be done in the PTXprint window. You never need to edit files by hand or
  type commands.
* Sections marked **advanced** explain how to type special codes in the few places where
  PTXprint gives you a text box for them (for example the front matter). You can skip them until
  you need them.
* Technical words are explained the first time they appear in a chapter, and listed in the
  **Glossary of terms** at the end.

## 1.3 How this manual is organised

Two general chapters come first. Then there is one chapter for each tab of the PTXprint window,
in the same order as the tabs. Then come chapters about the PDF Preview window, importing settings
and getting help. The manual ends with step-by-step tasks, solutions to problems, and a glossary.

1. **About this manual** – this chapter.
2. **Getting started with PTXprint** – a first walk-through: from opening PTXprint to your first PDF.
3. **The main window, menu and view levels** – the parts of the window, configurations, view
   levels, and how PTXprint saves your settings.
4. **Basic tab** – choose the project, the configuration and the books to print.
5. **Layout tab** – page size, margins, columns, font size and line spacing.
6. **Fonts+Script tab** – fonts, writing system, hyphenation and spacing.
7. **Body tab** – what is printed from each book (introductions, headings, verse numbers…).
8. **Notes+Refs tab** – footnotes, cross-references and study notes.
9. **Header+Footer tab** – the running header and footer, and page numbers.
10. **Pictures tab** – illustrations and maps.
11. **Diglot tab (two or more languages)** – two or more texts side by side.
12. **Tabs+Borders tab** – thumb tabs and decorative borders.
13. **Styles tab** – the look of each kind of text (each USFM marker).
14. **Advanced tab** – settings for experienced users.
15. **View+Edit tab** – front matter, the adjustment list, and the files PTXprint makes.
16. **Peripherals tab (front and back matter)** – front matter, table of contents, colophon, maps and covers.
17. **Publications tab** – a list of publications that you can print together.
18. **Finishing tab** – PDF type for the printer, crop marks, booklets and comparing PDFs.
19. **Printers tab** – price estimates and orders from print companies.
20. **PDF Preview window, layout analysis and page filling** – look at the PDF and fix the layout of pages.
21. **Importing settings** – copy settings from a PDF, an archive or another configuration.
22. **Help tab and getting support** – find your files, and ask for help.
23. **How do I...? (step-by-step tasks)** – short instructions for common jobs.
24. **Problems and solutions** – what to do when something goes wrong.
25. **Glossary of terms** – the meaning of the words used in this manual.

Most tab chapters have the same parts:

* **What this tab is for** – when you would use the tab.
* One section for each area of the tab, using the names you see on the screen.
* **Common tasks** – numbered steps for the things people do most often.
* **Common problems** – what you see, why it happens, and what to change.
* **Settings reference** – every setting on the tab (see below).

## 1.4 How to read a settings-reference entry

At the end of each tab chapter, the **Settings reference** lists every setting (check box, list,
number box, button and so on) in that part of PTXprint. The settings are grouped by tab or dialog,
then by area, for example *Layout › Page Setup*. Each heading is the setting's name on the
screen. If it has no name, the heading is the label beside it, or a short description.

Each entry has these parts:

* **First line** – the kind of control (for example Checkbox, Radio, Number, Drop-down, Button,
  Text box, Colour or Link). For a check box, **on** means it is ticked by default and **off**
  means it is not. Then the lowest view level that shows the setting: **Mini+** (all views),
  **Basic+**, **Regular+**, or **Full** (only the Full view).
* **Second line** (only when needed) – more facts, separated by dots:
  * **Values** – for a number: the lowest and highest number, and the default.
  * **Choices** – the items in a list.
  * **Also** – a longer, descriptive name for the setting.
  * **Beside** – the label next to the control on the screen.
  * **Needs** – the setting can only be used when that other setting is turned on.
  * **Greyed out by** – the setting cannot be used while that other setting is ticked.
  * **Hidden until** – the setting is not shown until that check box is ticked.
  * **Shown when** – the tab or area only appears when that check box is ticked.
* **Tooltip** – the help text PTXprint shows when you hold the mouse over the setting, shown as a
  quotation.
* **Explanation** – in plain words: what the setting does, when to use it, a sensible value, and
  what to watch out for.

If you cannot find a setting in the window, check its view level, then **Needs**,
**Hidden until** and **Shown when**.

## 1.5 A short note about view levels

PTXprint has hundreds of settings, but most people need only a few. So PTXprint can hide the
settings you do not need. This is the **view level**. There are four: **Mini** (fewest settings),
**Basic**, **Regular** and **Full** (every setting).

To change the view level, click the **☰** button at the top-right of the window, point to
**View Level**, and choose a level.

A hidden setting still works. It keeps its value and still changes the PDF. So if the PDF does
not look as you expect, change to the **Full** view and check the settings again.

A note such as "(Regular and Full views)" tells you which view levels show a setting. For more,
see the chapter **The main window, menu and view levels**.


# 2. Getting started with PTXprint

## 2.1 About this chapter

This chapter is for people who use PTXprint for the first time. It takes you step by step from
opening PTXprint to your first PDF. Then it shows how to change a few common things, and how to
keep different sets of settings for different kinds of output.

You do not need to read the rest of the manual first. Each step tells you which chapter to read
for more.

In this chapter, "pt" means point. One point is about 0.35 mm. Font sizes and line spacing are
given in points.

## 2.2 Before you start

Check these things before you open PTXprint:

1. **You have a Paratext project** on this computer. PTXprint prints its text. If you use
   Send/Receive in Paratext, do a Send/Receive first, so that you have the latest text.
2. **The text has no serious marker errors.** PTXprint uses the USFM markers in the text (for
   example `\p` for a paragraph or `\v` for a verse). Run the Basic Checks in Paratext. Marker
   errors can stop PTXprint or give strange results.
3. **The fonts are installed** on this computer **for all users**. If a font is installed only
   for one user, PTXprint may not find it.
4. **No project, but you want to practise?** PTXprint can install a sample English Bible (the
   Berean Standard Bible) for you. See "Get a text to practise with" in the **Basic tab** chapter.

## 2.3 Open PTXprint

1. Start PTXprint like other programs on your computer, for example from the Windows Start menu.
2. The main PTXprint window opens. It has:
   * **tabs** across the top (**Basic**, **Layout**, **Fonts+Script** and others). Each tab holds
     one group of settings;
   * the **☰** button at the top-right, for the main menu;
   * a **bar at the bottom** with the **Save**, **Print (Make PDF)** and **Quit** buttons.

The first time PTXprint starts, it uses the **Regular** view level, which shows most tabs and
settings. If the window looks too full, click **☰**, point to **View Level**, and click
**Basic View** or **Mini View**. Hidden settings still work. See the chapter **The main window,
menu and view levels**.

If your projects are not in the **Project** list, PTXprint may be looking in the wrong folder. See
"Use projects from another Paratext folder" in the chapter **Help tab and getting support**.

## 2.4 Choose the project and the configuration

Everything starts on the **Basic** tab.

1. Click the **Basic** tab.
2. In the **Project** list, choose your Paratext project. PTXprint shows the full name of the
   project next to the list.
3. In the **Layout Configuration** area, look at the **Name** list. The first time, it shows
   **Default**.

A **configuration** is a named set of PTXprint settings for one project: page size, fonts,
pictures and so on. Every project has a configuration called **Default**. You can make more later
(see "Keep different settings for different outputs" below). For now, use **Default**.

## 2.5 Choose the books

On the **Basic** tab, in the **What to Print** area:

1. Click **Single Book**.
2. Choose a book from the list. For your first PDF, choose a short book (for example Ruth, Jonah,
   Philippians or Jude), because it prints quickly.
3. To print only some chapters, type the first chapter in **From Chapter** and the last chapter in
   **To**.

To print several books, click **Select Multiple Books...**, click the books you want, and click
**OK**. See the **Basic tab** chapter for more ways to choose books and passages.

## 2.6 Make your first PDF

1. Click **Print (Make PDF)** at the bottom right of the window (or press **Ctrl+P**).
2. PTXprint saves your settings, then makes the PDF. A progress bar shows that it is working. This
   takes from a few seconds to a few minutes, depending on the number of books and pictures.
3. When PTXprint has finished, the **PDF Preview** window opens and shows the PDF.

If a message appears instead of the PDF, read it carefully. Two common messages at the start are:

* **"No books to print"** – no book is selected. Choose a book on the **Basic** tab.
* **"One or more fonts have not been set yet"** – on the **Fonts+Script** tab, choose a font for
  the main text (see "Change the main font" below).

## 2.7 Look at the PDF in the preview

The **PDF Preview** window shows the pages of your PDF.

* To move from page to page, use the arrow buttons at the top, the **Left/Right arrow** keys, or
  the mouse wheel.
* To make the page bigger or smaller, use the **Zoom** box, or hold **Ctrl** and turn the mouse
  wheel.
* Tick **Book View** (or press **Ctrl+B**) to see two facing pages side by side, as in a printed
  book.
* The title bar shows the name of the PDF file and the time it was made. Check it, so you know
  you are looking at the newest PDF.
* Click **Show main PTXprint settings** (or press **Alt+S**) to go back to the main window.

Closing the Preview window only hides it. It comes back the next time you print. The Preview
window can also find layout problems and fix them. See the chapter **PDF Preview window, layout
analysis and page filling**.

## 2.8 Change a few common things

After each change, click **Print (Make PDF)** again to see the result.

### Change the page size

1. Click the **Layout** tab.
2. In the **Page Setup** area, open the **Page Size** list.
3. Choose a size, for example **148mm, 210mm (A5)**. Or type your own size: the width, a comma,
   then the height, for example `140mm, 216mm`.

Ask your printer for the exact page size (the "trim size") before you do a lot of work. If you
change the page size later, every line of the book moves.

### Change the main font

1. Click the **Fonts+Script** tab.
2. In the **Font Configuration** area, click the **Select Font...** button next to **Regular**.
3. The **Pick a Font (and Typeface)** dialog opens. Type part of the font name in the search box,
   then click the font in the list.
4. Click **OK**.

PTXprint then fills in the **Bold**, **Italic** and **Bold Italic** fonts from the same font
family. If some characters print as empty boxes, the font does not have those characters. See the
**Fonts+Script tab** chapter.

### Change the font size

1. Click the **Layout** tab.
2. In the **Page Setup** area, change **Base Font Size (pt)**. For example, 11 pt is a common size
   for the main text.

When **Lock Ratio** is ticked (the normal setting), PTXprint changes the **Base Line Spacing (pt)**
with the font size, so the page keeps the same look. Headings, footnotes and verse numbers also
grow or shrink with the main text. See the **Layout tab** chapter.

### Change between one and two columns

1. Click the **Layout** tab.
2. Tick **Two Column Layout** for two columns, or untick it for one column.

PTXprint changes the **Base Indent** for you when you change the number of columns.

### Turn pictures on or off

The **Pictures** tab is not shown in the **Mini** view. If you cannot see it, click **☰** ›
**View Level** › **Basic View** (or higher).

1. Click the **Pictures** tab.
2. On the **Global Options** sub-tab, tick **Include Pictures (illustrations)** to print the
   pictures, or untick it to leave them out.

The first time you turn pictures on, PTXprint needs a list of the pictures (the PicList). It makes
this list from the `\fig` entries in your Paratext text. See "Show the pictures that are in the
Paratext text" in the **Pictures tab** chapter. For a draft, choose **Low Resolution (Smaller
File)** on the same sub-tab, so that the PDF stays small.

## 2.9 Keep different settings for different outputs

You often need more than one kind of PDF from the same project. For example:

* a **draft** for checking, with wide spacing, "DRAFT" on each page and small pictures;
* a **final** PDF for the printer, with high-quality pictures and the PDF type that the printer
  asks for.

Do not change one configuration back and forth. Make a separate configuration for each kind of
output. Each configuration remembers its own settings.

### Make a new configuration

1. Click **Save** at the bottom of the window, so that your latest changes are kept.
2. On the **Basic** tab, in the **Layout Configuration** area, click the **Save As** button (the
   icon next to the **Name** list).
3. The **Save Current Configuration As...** dialog opens. Type a name, for example `Draft` or
   `Final_A5`. Use only letters, numbers, brackets `( )`, underscores `_` and hyphens `-`. No
   spaces.
4. Click **OK**. PTXprint makes the new configuration as a copy of the current settings, and
   changes to it.
5. Now change the settings for this kind of output. The other configuration stays as it was.

### Change to another configuration

1. Click **Save** first. PTXprint does **not** save the current configuration when you choose
   another one.
2. On the **Basic** tab, choose the configuration in the **Name** list.

You can lock a finished configuration with a password, so that nobody changes it by mistake. See
"Protect a finished configuration" in the **Basic tab** chapter.

## 2.10 How PTXprint saves your settings

* **Save** (or **Ctrl+S**) saves the settings of the current configuration.
* **Print (Make PDF)** always saves the settings first, then makes the PDF.
* When you choose a different **project**, PTXprint saves the current configuration first.
* When you choose a different **configuration**, PTXprint does **not** save first.
* **Quit** closes PTXprint **without saving**. Click **Save** before you click **Quit**.

PTXprint keeps the configurations inside the Paratext project. So when you use Send/Receive in
Paratext, the other people on your team get the same configurations.

## 2.11 Where the PDF is saved

PTXprint saves the PDF inside the Paratext project, in a folder called `local\ptxprint`. This
folder is not shared by Send/Receive. The file name is made from the project code, the
configuration name and the books, for example `ABC_Default_JHN_ptxp.pdf`.

To open the folder, do one of these:

* Click the **Open folder containing the PDF** button in the bar at the bottom of the main window
  (**Regular** and **Full** views).
* On the **Help** tab, click the blue link next to **Output PDF Location**.
* In the PDF Preview window, click **Open folder containing the PDF**.

PTXprint makes the PDF again each time you print, with the same name. To keep a PDF (for example
the one you sent to a consultant), copy it to another folder, or click **Save the PDF with a
different name** in the PDF Preview window.

## 2.12 When something goes wrong

* **Read the message.** PTXprint shows a message in a window, or in the status line above the
  bottom bar. It often tells you what to change.
* **Check the view level.** If a tab or setting has disappeared, the view level may be too low.
  Click **☰** › **View Level** › **Full View**. Or type the name of the setting in the
  **Search for settings** box at the bottom-left of the window.
* **Check the "Common problems" section** of the chapter about the tab you were using.
* **Look in the chapter "Problems and solutions"** for problems that are not about one tab.
* **Ask for help.** The chapter **Help tab and getting support** explains how to ask the Support
  Agent, the PTXprint User Community, or the support team, and how to make an archive file that
  the support team can use to see your problem.

## 2.13 What to read next

* **The main window, menu and view levels** – more about configurations, view levels and saving.
* **Basic tab** and **Layout tab** – the most important settings for every publication.
* **How do I...? (step-by-step tasks)** – short instructions for many common jobs.


# 3. The main window, menu and view levels

## 3.1 What this part of PTXprint is for

The main window is where you do all your work in PTXprint. It has three parts:

* **The tabs** across the top (**Basic**, **Layout**, **Fonts+Script**, **Body** and so on). Each tab holds one group of settings.
* **The ☰ main menu** button at the top-right corner, next to the tabs. It holds settings about PTXprint itself, not about your book: how to show the PDF, the **View Level**, the interface **Language**, and links to **Donate** and **Give Feedback**.
* **The bar at the bottom of the window**, with the **Search for settings** box, the button to open the output folder, the **Quick Run** and **Layout Only** check boxes, and the **Save**, **Print (Make PDF)** and **Quit** buttons.

This chapter also explains three ideas that you need everywhere in PTXprint: **configurations**, **view levels**, and how PTXprint **saves** your settings.

## 3.2 Projects and configurations

A **project** is a Paratext project – the Scripture text that you want to print. You choose it on the **Basic** tab, in the **Project** list.

A **configuration** (also called a "layout" or "config") is a named set of PTXprint settings for one project. One project can have many configurations, for example `Default` for a draft, `NT_A5` for a small New Testament, and `Large_Print`. Each configuration remembers its own page size, fonts, pictures, styles, front matter and so on.

* Every project has a configuration called **Default**. You cannot delete it, lock it or copy it to other projects, but you can reset it.
* You choose, create, lock, copy and delete configurations on the **Basic** tab, in the **Layout Configuration** area. See the chapter about the Basic tab.
* PTXprint keeps the configurations inside the Paratext project folder. So when you use **Send/Receive** in Paratext, other people on the team get the same configurations.

## 3.3 How PTXprint saves your settings

* **Save** (or **Ctrl+S**) saves the settings of the current configuration.
* **Print (Make PDF)** (or **Ctrl+P**) **always saves** the settings first, then makes the PDF.
* When you choose a **different project** in the **Project** list, PTXprint saves the current configuration first.
* When you choose a **different configuration** in the **Layout Configuration** list, PTXprint does **not** save the current one first. Click **Save** before you change, or your recent changes are lost.
* **Quit** closes PTXprint **without saving**. Click **Save** or **Print (Make PDF)** before **Quit** to keep your changes.
* If a configuration is **locked** with a password, PTXprint does not save changes to it. You can still change settings on the screen and make a PDF, but the changes are not kept.

Some things are remembered for you (the user), not for the configuration: the view level, the interface language, the **Show PDF** choice and the **Quick Run** setting. These stay the same for all projects and configurations.

## 3.4 View levels

PTXprint has hundreds of settings. Most people need only a few. So PTXprint can hide the settings that you do not need. This is the **view level**. There are four view levels:

| View level | What you see | Good for |
|---|---|---|
| **Mini** | Only the **Basic**, **Layout**, **Fonts+Script** and **Help** tabs, and only the most important settings on them: project, books, configuration name, page size, font size, two columns, the main font. | A first look at PTXprint, or a quick draft. |
| **Basic** | Adds the **Body**, **Notes+Refs**, **Header+Footer**, **Pictures**, **Peripherals** and **Finishing** tabs, and more settings on each tab (margins, line spacing, bold and italic fonts, the **Import Settings** button…). On **Peripherals** and **Finishing** it shows only the main settings (table of contents and front matter; pages per sheet and comparing PDFs). | Most simple publications. |
| **Regular** | Adds the **Diglot**, **Tabs+Borders**, **Styles**, **Advanced** and **View+Edit** tabs, and many more settings on all tabs. | Most typesetters. PTXprint uses this level the first time it starts. |
| **Full** | Shows every setting, including the **Publications** and **Printers** tabs. | Experienced users who need special settings. |

**How to change the view level:** click the **☰** button (top-right), point to **View Level**, and click **Mini View**, **Basic View**, **Regular View** or **Full View**. The current level is shown in blue and bold in that list. The change happens at once, without a restart.

**Hidden settings still work.** A lower view level only *hides* settings. A hidden setting keeps its value, is still saved with the configuration, and still changes the PDF. For example, if you turned on pictures or a diglot in the **Regular** view and then change to the **Mini** view, the pictures or the diglot are still in the PDF, though you cannot see the tab. If the PDF looks different from what you expect, change to the **Full** view and check the settings again.

**Search finds hidden settings.** If you choose a setting in **Search for settings** that is hidden at your view level, PTXprint changes to a higher view level to show it.

## 3.5 Tab labels and highlighted settings

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

## 3.6 The bottom bar

From left to right, the bar at the bottom of the window has:

* **Search for settings** – type a word to find a setting.
* **Open folder containing the PDF** – opens the output folder. (Regular and Full views.)
* **Quick Run** and **Layout Only** – two check boxes that make printing faster.
* **Print** – only appears when you are looking at the secondary text of a diglot.
* **Save**, **Print (Make PDF)** and **Quit**.

Above the bar, a **status line** sometimes shows a message from PTXprint (for example "No books to print"). Click **Dismiss** to hide it.

When a newer version of PTXprint is available, a **Check for updates...** button can appear at the top-right, next to the ☰ button. (PTXprint checks at most once a day, only on Windows, and only if Internet use is allowed on the **Advanced** tab.)

## 3.7 The ☰ main menu

* **Show PDF** – what happens with the PDF after printing:
  * **Preview Pane** – PTXprint shows the PDF in its own preview window. This is the usual choice. PTXprint can also use the preview for some editing tools.
  * **System Viewer** – the PDF opens in the PDF program on your computer.
  * **Output Folder** – PTXprint opens the folder that holds the PDF.
* **View Level** – see "View levels" above.
* **Language** – the language of the PTXprint menus and labels.
* **Donate** and **Give Feedback** – open a web page.

## 3.8 Common tasks

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

## 3.9 Common problems

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

## 3.10 Settings reference

### Main menu (top-right ☰ button)

#### Show PDF

Menu button · Mini+ · `btn_menu_showPDF`

> Choose how the PDF is shown after printing: in the preview pane, in your system's PDF viewer, or by opening the output folder.

The current choice is shown in blue. When you click a choice, PTXprint uses it at once to show the last PDF, and remembers it for all projects. **Preview Pane** is best for most people: PTXprint can then update the preview itself, and no other program keeps the PDF file open.

#### View Level

Menu button · Mini+ · `btn_menu_level`

> Choose how many settings PTXprint shows. Hidden settings keep their values and still take effect.

The current level is shown in blue. PTXprint remembers the view level for you, not for each configuration. The first time PTXprint starts, it uses the **Regular View**.

#### Language

Menu button · Mini+ · `btn_menu_lang`

> Change the language of the PTXprint user interface.

The current language is shown in blue. When you choose another language, PTXprint closes and opens its window again in that language, with the same project and configuration. PTXprint saves your settings first (a locked configuration is not saved). This changes only the PTXprint menus and labels, not the language of your book.

#### Donate

Button · Mini+ · `btn_menu_donate`  
Also: Donate toward PTXprint Development

> PTXprint is a tool that is freely available to all without any restrictions. Our aim is to help people get the Scriptures out to people in formats that work best for their local context.
>
> Click to contribute toward the ongoing development and maintenance of tools by SIL Global's Language Technology Developers so that others can also benefit.
>
> https://give.sil.org/campaign/725128/donate

Opens the SIL donation web page in your web browser. If **Disable ALL Internet Use** is ticked on the **Advanced** tab, PTXprint shows a message instead.

#### Give Feedback

Button · Mini+ · `btn_menu_feedback`  
Also: Link to PTXprint Feedback Form (Google Form)

> Psst! Can we have 5 minutes of your time? You could help us make PTXprint better!
>
> The developers of PTXprint would love to know how this tool is being used. What is your favorite feature? Are there any annoyances? Tell us what you like, or don't like. Tell us what you dream for in the future.
>
> Click this button to fill in the Google form or type this in a browser: https://tiny.cc/ptxprintfeedback

Opens the feedback form in your web browser. It needs Internet access (see **Disable ALL Internet Use** on the **Advanced** tab).

### Main window

#### Basic

Label · Mini+ · `lb_Basic`

> Select the Project and Book(s), to be used to create the PDF file.
>
> You can also Save/Share Configuration settings.

Choose the project, the configuration and the books here. Always visible.

#### Layout

Label · Mini+ · `lb_Layout`

> Page Setup, Font Size and Line Spacing. Margins, Columns and Rules (lines).

Some number labels on this tab become bold when you change the value from the default.

#### Fonts+Script

Label · Mini+ · `lb_Font`

> Basic Fonts and Advanced Font options. Also a range of Advanced typography settings to support any Writing System. Advanced Spacing Settings. Fallback fonts for characters missing in primary font.

The word "Fonts" in the tab label turns blue when coloured text is enabled.

#### Body

Label · Basic+ · `lb_Body`

> Main settings to control the beginning and ending of books, and options for what should be included in the Main Body of text. Also settings for special books.

What goes into the main text, and how books and chapters start.

#### Notes+Refs

Label · Basic+ · `lb_NotesRefs`

> Control how Footnotes, Cross-references, Study Notes and Questions should appear.

The word "Refs" in the label turns blue when an extended cross-reference list is used.

#### Header+Footer

Label · Basic+ · `lb_HeadFoot`

> Adjust the content of headers and footers.

What appears at the top and bottom of each page.

#### Pictures

Label · Basic+ · `lb_Pictures`

> Manipulate the pictures to be used in the publication. Control everything from quality to position, from captions to copyrights.

The label turns blue when pictures are included in the PDF. In the **Mini** view the tab is hidden, but pictures that are turned on are still printed.

#### Diglot

Label · Regular+ · `lb_Diglot`

> Create a diglot publication by selecting a secondary project and configuration.

For printing two (or more) texts side by side. The label turns blue when the diglot is turned on.

#### Tabs+Borders

Label · Regular+ · `lb_TabsBorders`

> Settings for thumb-tabs and options to add decorative borders or embellishments to the text.

"Tabs" or "Borders" in the label turns blue when that feature is turned on.

#### Styles

Label · Regular+ · `lb_StyleEditor`

> Edit style information of markers without having to edit the USFM stylesheet files.

Change how each USFM marker looks (font, size, spacing, colour…).

#### Advanced

Label · Regular+ · `lb_Advanced`

> Define stylesheets, tex macros, front and back matter PDFs, watermarks and various other advanced settings including interlinear (& ruby text) output.

Also holds the **Disable ALL Internet Use** option. The label turns blue when one of its special options is turned on (for example a custom script, a changes file, extra TeX or style files, or interlinear output).

#### View+Edit

Label · Regular+ · `lb_Viewer`

> View and edit various control and log files. Examine final SFM output and tweak adjust lists.

Look at and edit the front matter, adjust lists, log files and the processed text.

#### Peripherals

Label · Basic+ · `lb_Peripherals`

> Define what material should be placed before and/or after the main scripture pages.

Front matter, table of contents, back matter and variables. The label turns blue when front matter, front or back PDFs, or an automatic table of contents is turned on. In the **Basic** view it shows only the table of contents and front matter settings.

#### Publications

Label · Full · `lb_Publications`

> Define several publications (each with its own books, titles and other variables) from this one configuration, and print them all in one go.

Define several publications from one configuration and print them together.

#### Cover

Label · not shown · `lb_Cover`

> Set parameters for the cover of the publication.

This tab is normally not shown in the main window.

#### Finishing

Label · Basic+ · `lb_Finishing`

> Options to control pagination, PDF output format and compare output with a previous PDF.

The label turns blue when more than one page per sheet is chosen. In the **Basic** view it shows only the pages-per-sheet and compare-PDF settings.

#### Printers

Label · Full · `lb_Printers`

> Estimate printing costs, compare printers and check the book thickness. Some printers also give live quotations and take orders.

The **Printers** tab.

#### Help

Label · Mini+ · `lb_Help`

> Links to useful folders and online resources. Where to obtain help from others.

Links to folders and to online help. Always visible.

#### Log

Label · not shown · `lb_Logging`

> Display the output log from XeTeX processing.

This tab is normally not shown in the main window.

#### btn_menu

Menu button · Mini+ · `btn_menu`

The **☰** button at the top-right of the window. It opens the main menu (**Show PDF**, **View Level**, **Language**, **Donate**, **Give Feedback**). Always visible.

#### Check for updates...

Button · not shown · `btn_download_update`

> A newer version of PTXprint is available. Click to visit download page on the website.

Only appears when PTXprint has found a newer version. Opens the download page in your web browser. PTXprint checks for updates at most once a day, only on Windows, and only when Internet use is allowed.

#### Dismiss

Button · not shown · `btn_dismissStatusLine`

> Hide this message.

Hides the status message above the bottom bar. When the message shows Unicode character codes, this button is called **Copy to Clipboard** and copies the message before it hides it.

#### Find help

Text box · Mini+ · `t_find`

> Type in a word to search for a setting that you can't locate. A short list of relevant topics will appear above. Select a topic to jump to the appropriate setting which will be highlighted.
>
> Shortcut: Ctrl-F

Press **Enter** (or click the magnifying-glass icon) to search. Click a result: PTXprint opens the right tab, highlights the setting and, if needed, raises the view level so you can see it. Click the clear icon at the right end of the box to remove the highlight. Short, simple words (for example `margin`, `caption`, `verse`) work best. While PTXprint is printing, this box shows "Processing...".

#### Open folder containing the PDF

Button · Regular+ · `btn_openFolder`

> Open the folder which contains the PDF file(s) created for this project.

Opens the folder in your file manager. In views where this button is hidden, use **☰** › **Show PDF** › **Output Folder**.

#### Quick Run

Checkbox, on · Mini+ · `c_quickRun`  
Also: Quick run (to speed up process)

> Enabling this option will give quicker output, but it may be less refined.
>
> PTXprint needs to rerun the typesetting process in order to ensure the Table of Contents & other dynamically updated details are accurate.
>
> Shortcut: Ctrl-Q

Without it, PTXprint runs the typesetting several times (up to 5) so that the table of contents, cross-page details and page layout are correct. With it, it runs only once. Tick it while you try out settings. Untick it for the final PDF. PTXprint remembers this setting for you, not for the configuration.

#### Layout Only

Checkbox, on · Regular+ · `c_noupdate`  
Also: Layout Only (skip USFM processing)

> Re-runs page layout without regenerating or processing USFM scripture content.
>
> Useful for quick layout tweaks (+1 / −1 spacing or style changes).
>
> PTXprint still re-processes the USFM when the text has changed in Paratext, or when you change a setting that affects the text (the box then shows a dash until the next successful print).
>
> This setting is not saved with the configuration.

Faster when you only change layout, spacing or style settings. Settings that change the text include which books, footnotes, or verse numbers to include. If you tick it while the colophon is turned on, PTXprint turns the colophon off.

#### Print

Button · Mini+ · `b_print2ndDiglotText`

> The configuration displayed now is for the secondary project of the Diglot. You can use this button to create a PDF with just the secondary text to check the settings specified.
>
> Use the larger 'Return to Primary' button to get back to the primary project in order to print a diglot with both texts.

Only appears when the main window shows the secondary project of a diglot (after you switch to it on the **Diglot** tab).

#### Save

Button · Mini+ · `btn_saveConfig`  
Also: Save configuration

> Save current settings in named Configuration (set on the Basic tab).
>
> Shortcut: Ctrl-S

Saves all settings of the current configuration, including hidden ones. You do not need it before **Print (Make PDF)**, because printing saves too. Greyed out when PTXprint cannot print (for example when no project is selected) and when the configuration is locked. If you typed a new name in the configuration name box on the **Basic** tab, **Save** creates a new configuration with that name.

#### Print (Make PDF)

Button · Mini+ · `b_print`

> Create the PDF as specified (automatically saves settings).
>
> Shortcut: Ctrl-P

First checks that there are books to print and that the main font is set. If an old PDF with the same name is open in another program, PTXprint asks you to close it. While PTXprint is printing, you cannot start another print. When you are looking at the secondary text of a diglot, this button is called **Return to Primary**.

#### Quit

Button · Mini+ · `b_close`

> Close PTXprint without saving.
>
> Shortcut: Ctrl-W

Click **Save** first if you want to keep your changes.


# 4. Basic tab

## 4.1 What this tab is for

The **Basic** tab is the first tab in PTXprint. You come here to:

* choose the **project** (the Paratext project with the Scripture text),
* choose, save, lock, copy or delete a **configuration** (a named set of settings),
* choose **what to print** – one book, part of a book, several books, or a Bible module,
* check the **copyright and license** statement for the publication.

Start here every time. Most other settings depend on the project and configuration that you choose here.

## 4.2 Project

Choose your Paratext project in the **Project** list. PTXprint shows the full name of the project next to the list.

* When you change to another project, PTXprint first saves the current configuration. Then it opens the configuration that you last used with the new project (or **Default**).
* The last item in the **Project** list is a blue **Import...** item. It opens the **Import Scripture...** dialog. Use it when you have a Scripture text bundle (a .zip file) but not a Paratext project, or to install the sample text (the Berean Standard Bible).

### Copyright & Licensing

(Regular and Full views.) Click **Copyright & Licensing** to open the area. It has two parts:

* **Copyright** – the copyright statement. PTXprint fills it in from the Paratext project settings. You can change it here. Click **Reload copyright from Paratext project** to get the Paratext text back.
* **License** – choose one of the Creative Commons licenses, **All Rights Reserved**, or type your own license.

PTXprint puts these texts into the front matter (for example on the back of the title page) through the variables `\zcopyright` and `\zlicense`. Special codes work in both boxes: `(c)` becomes ©, `(r)` becomes ®, `(tm)` becomes ™, `~` is a non-breaking space, and `//` forces a new line.

## 4.3 Layout Configuration

A **configuration** (or layout) is a named set of settings. One project can have many configurations, for example one for a draft and one for the final book. See the chapter about the main window for more about configurations and saving.

* **Name** – the list of saved configurations. Choose one to load its settings. Or type a new name here and click **Save** to make a new configuration. Use only the letters a–z and A–Z, numbers, brackets `( )`, underscores `_` and hyphens `-`. No spaces.
* The **Save As** button (an icon next to the name) opens the **Save Current Configuration As...** dialog.
* The **lock** button locks or unlocks the configuration with a password.
* The **Copy configuration to other projects** button opens the **Copy Configuration To...** dialog. (Regular and Full views.) It is greyed out for the **Default** configuration, because **Default** is never copied to other projects.
* **Delete** removes the selected configuration. For the **Default** configuration, this button is replaced by **Reset**.
* **Import Settings...** opens the **Import Settings** dialog, to bring in settings from a PDF, a ZIP archive, or another configuration. See the chapter "Importing settings". (Basic, Regular and Full views.)
* **Run Tutorial...** steps through a tutorial file on the current project and configuration. See "Run a tutorial" below. (Basic, Regular and Full views.)
* **Notes** – an optional description of the configuration, for you and your team. (Basic, Regular and Full views.)

When you choose another configuration in the **Name** list, PTXprint does **not** save the current one. Click **Save** first.

## 4.4 What to Print

Choose one of three ways to say what goes into the PDF:

* **Single Book** – choose one book in the list. To print only part of the book, type chapter numbers in **From Chapter** and **To**. When you choose a new book, PTXprint sets the chapters to the whole book.
* **Portions or Multiple Books** – click **Select Multiple Books...** to choose books by clicking them, or type a list in the box. You can type book codes (`MAT MRK LUK JHN`), book ranges (`MAT-REV`) and references (`JHN 2:1-12`, `PSA 23; 100; 117`, `GEN 1:1-2:3`). Use the 3-letter USFM codes (for example `JHN`, not `John`). Press **Ctrl+B** to jump to this box.
* **Bible Module** – print a Paratext module (a .sfm file that lists passages to include). Click **Choose...** to select the module file. Click **Edit...** to see it on the **View+Edit** tab. (Bible Module: Basic, Regular and Full views; **Edit...**: Regular and Full.)

If you type in **From Chapter** or **To**, PTXprint changes to **Single Book**. If you type in the book list, PTXprint changes to **Portions or Multiple Books**.

The FRT (front matter) book is not in the book lists. Set up the front matter on the **Peripherals** tab instead.

## 4.5 Dialogs on this tab

### Save Current Configuration As...

Opens when you click the **Save As** button. Type a name in **Configuration Name** and click **OK**. PTXprint makes a new configuration with a copy of the current settings, saves it, and changes to it. **OK** stays greyed out until the name is valid. A message below the box says if the name has spaces or special characters, or if a configuration with that name already exists.

If the name already exists, you can tick **Replace it if it already exists**. Then PTXprint deletes the old configuration and saves the current settings in its place. The **Default** configuration can never be replaced. The box is unticked each time the dialog opens, so you must choose to replace each time.

Tip: Click **Save** before **Save As...**, so that the new configuration starts from your latest settings.

### Lock/Unlock Configuration

Opens when you click the **lock** button. Locking protects a configuration so that nobody changes or deletes it by mistake.

* **To lock:** type a password (up to 16 characters) and click **OK**. PTXprint saves the configuration and then locks it. The lock icon changes, and dots appear in the box next to the name.
* **To unlock:** click the lock button again, type the same password, and click **OK**. If the password is wrong, the configuration stays locked and the status line says "Incorrect password".
* You must type a password to lock. If the box is empty, PTXprint does not lock the configuration and asks you for a password.
* **Cancel** (or closing the dialog) never locks or unlocks anything.
* While a configuration is locked, **Save**, **Delete** and **Notes** are greyed out, and PTXprint does not save changes (not even when you print). You can still try out settings and print, but the changes are not kept.
* You cannot lock the **Default** configuration.

### Copy Configuration To...

Opens when you click the **Copy configuration to other projects** button. Use it when several projects need the same layout (for example, a series of New Testaments in related languages).

1. Click the projects that should receive a copy of the current configuration. The current project is shown in black and cannot be chosen. The **Recent** list at the bottom shows your selection, and remembers your last 10 selections.
2. Choose what to do if a target project already has a configuration with the same name:
   * **Do NOT Replace Existing Config** – skip those projects. Use this the first time you copy.
   * **Merge Configurations From Both** – combine the two. Settings that were changed in the target project since the first copy are kept.
   * **Overwrite With Recent Changes** – settings that were changed in this (source) project replace the target settings.
3. Leave **Keep each project's own language-specific variables** ticked (the normal choice), so that each target project keeps its own titles and language name. Untick it only if the target projects should get the same values as this project.
4. Click **OK**.

The **Default** configuration is never copied, and the button is greyed out while **Default** is selected. Use **Save As** to give the configuration a name first.

PTXprint copies the saved files of the configuration: the settings, the styles, the changes and TeX files, and the front matter. Adjust lists (paragraph adjustments) are not copied, because they belong to one text. Click **Save** before you copy, so that the copy has your latest settings.

### Select Books To Export to PDF

Opens when you click **Select Multiple Books...**. Each book in the project is a button. Click a button to select or unselect that book. Hold **Shift** and click another book to select or unselect all books between the two. The buttons at the side select groups: **All Books**, **Old Testament**, **New Testament**, **Deuterocanon**, **Extra Material**, **Toggle Books** (reverse the selection), and **Reset All** (unselect all). A group button selects all books of that group. If they are all selected already, it unselects them. Click **OK**. PTXprint puts the books in the book list in normal Bible order. You can then change the order by typing in the list.

### Import Scripture...

Opens when you choose **Import...** at the end of the **Project** list. There are two ways to get a text:

* **Install BSB** – installs the Berean Standard Bible that comes with PTXprint. It is good for practice and as a second text in a diglot.
* **Step 1 – Step 3** – install a Scripture text bundle (.zip):
  1. Download a bundle from the **Primary DBL site** (Digital Bible Library – you must log in) or the **Open.Bible site**. Choose a bundle that has the text (not only audio). The USX format is best.
  2. Click **Locate...** and choose the .zip file.
  3. Check the project name in **Assign a Name for the Project** and click **OK**.

PTXprint creates the new project in a folder called `_PTXprint` inside your Paratext projects folder, and opens it.

### Please Confirm...

PTXprint asks you to confirm before something that cannot be undone:

* **"You are about to REMOVE the '...' configuration"** – appears when you click **Delete**. It names the configuration. Click **Yes** to delete it, or **No** to keep it. Its settings and working files are deleted. PDF files that you made from it are **not** deleted.
* **"You are about to CREATE a diglot (or polyglot) configuration"** – appears when you turn on a diglot. PTXprint suggests that you first use **Save As...** to make a new configuration for the diglot.

## 4.6 Common tasks

### Start a new publication from an existing configuration

1. In **Project**, choose the project.
2. In **Name**, choose the configuration that is closest to what you want.
3. Click **Save** (so that the latest settings are on disk).
4. Click the **Save As** button. Type a new name (for example `NT_A5`) and click **OK**.
5. Now change the settings. The old configuration stays as it was.

### Print one book, or part of a book

1. Click **Single Book** and choose the book in the list.
2. To print only some chapters, type the first chapter in **From Chapter** and the last chapter in **To**.
3. Click **Print (Make PDF)**.

### Print several books, or selected passages

1. Click **Select Multiple Books...**, click the books you want (or click **New Testament**), then click **OK**.
2. Or type in the book list, for example `MAT-ACT` or `PSA 23; 100; 117 LUK 15:11-32`.
3. Click **Print (Make PDF)**.

### Protect a finished configuration

1. Choose the configuration in **Name** (not **Default**).
2. Click the **lock** button.
3. Type a password and click **OK**. Remember the password.

### Use the same layout for another project

1. Click **Save**.
2. Click the **Copy configuration to other projects** button. (Regular or Full view. The configuration must not be **Default**.)
3. Click the target project(s).
4. Choose **Do NOT Replace Existing Config**, leave **Keep each project's own language-specific variables** ticked, and click **OK**.
5. In **Project**, choose the target project and check the copied configuration.

### Set or correct the copyright statement

1. Change to the **Regular** or **Full** view if needed.
2. Click **Copyright & Licensing** to open it.
3. Type the copyright text (type `(c)` for ©), or click **Reload copyright from Paratext project**.
4. Choose or type the **License**.

### Get a text to practise with

1. Open the **Project** list and choose **Import...** (the last item).
2. Click **Install BSB**. PTXprint installs and opens the BSB project.

### Delete a configuration that you do not need

1. Choose it in **Name**.
2. Click **Delete**. Check that the message names the right configuration, then click **Yes**.
3. PTXprint changes to the **Default** configuration and deletes the settings and working files of the old one. The PDF files that you made from it stay in the output folder.

### Run a tutorial

A tutorial is a file with a list of steps (a .json file, or a recorded test in a .zip file). You may get one from a trainer.

1. Choose the project and configuration to practise on. The tutorial makes its changes there, so use a practice configuration (for example make one with **Save As**).
2. Click **Run Tutorial...** and choose the tutorial file.
3. A small tutorial window opens. It shows the next step, and PTXprint highlights the control that the step uses.
4. Click **Step** (or press **Space**) to do the next step, **Skip** (or **S**) to leave it out, or **Play** (or **P**) to do the steps one after another. **Run to end** does all the remaining steps.
5. Close the tutorial window to stop. If the tutorial needed a higher view level, PTXprint changes the view level while it runs and changes it back when you close the window.

## 4.7 Common problems

### My recent changes were lost when I chose another configuration

**Cause:** Choosing another configuration in the **Name** list does not save the current one. **What to do:** Always click **Save** before you change configurations.

### The lock button is greyed out

**Cause:** The **Default** configuration cannot be locked. **What to do:** Use **Save As** to make a named configuration, then lock that one.

### I cannot save, and Delete and Notes are greyed out

**Cause:** The configuration is locked. **What to do:** Click the lock button and enter the password, or use **Save As** to make a new, unlocked copy.

### There is a Reset button instead of Delete

**Cause:** The **Default** configuration is selected. It cannot be deleted, so **Reset** is shown instead. Be careful: **Reset** asks no question. It at once sets all settings of the Default configuration back to the PTXprint defaults, and deletes the files in the Default configuration folder. Other configurations are not changed.

### The OK button in "Save Current Configuration As..." is greyed out

**Cause:** The name is empty, has spaces or special characters, or is already used. **What to do:** Read the message below the box. Use only letters a–z and A–Z, numbers, `(`, `)`, `_` and `-`.

### PTXprint says "Unknown book code"

**Cause:** The book list has a word that is not a 3-letter USFM book code (for example `John`). **What to do:** Use the codes, for example `JHN`, `MAT`, `1CO`.

### I cannot find the FRT book in the list

**Cause:** PTXprint does not list FRT as a book. **What to do:** Set up front matter on the **Peripherals** tab.

### The Primary DBL site and Open.Bible site links do not work

**Cause:** **Disable ALL Internet Use** is ticked on the **Advanced** tab. **What to do:** Untick it, or download the bundle another way and use **Locate...**.

### Copyright & Licensing or Copy configuration are missing, or Reset is greyed out

**Cause:** They are only available in the **Regular** and **Full** views. **What to do:** Click **☰** › **View Level** › **Regular View**.

### The Copy configuration to other projects button is greyed out

**Cause:** The **Default** configuration is selected. PTXprint never copies **Default** to other projects. **What to do:** Use **Save As** to save the settings under another name, then copy that configuration.

## 4.8 Settings reference

### Import Scripture... (dialog)

#### OK

Button · Regular+ · `btn_dbl_ok`

Installs the bundle chosen with **Locate...**, using the name in **Assign a Name for the Project**, and opens the new project. Greyed out until the name is valid and not already used.

#### Cancel

Button · Regular+ · `btn_dbl_cancel`

Closes the dialog without installing anything. PTXprint goes back to the project that was open before.

#### Install BSB

Button · Mini+ · `b_installBSB`

> The Berean Standard Bible is a Public Domain English Bible. It is bundled with PTXprint but needs to be installed in your Projects folder.
>
> This is a good training project and can also be used in diglots.

Installs the BSB as a project called `BSB` in your projects folder, opens it and closes the dialog. No internet is needed. Use it to practise, to try out settings, or as the second text in a diglot.

#### Locate...

Button · Basic+ · `btn_locateDBLbundle`  
Also: Locate DBL bundle

> After downloading a scripture text bundle (.zip) file you need to tell PTXprint where the .zip file is located so that it can install it as a special resource project.

Opens a file chooser in the `Bundles` folder of your Paratext projects folder. PTXprint then shows the file name and suggests a project name from the bundle (adding a number if that name is already used). Shortcut: **Alt+O**.

#### Step 3 Assign a Name for the Project – Assign a name to a DBL bundle

Text box · Basic+ · `t_DBLprojName`

> PTXprint will create this project within a subfolder called '_PTXprint'. Use a short name (8 characters or fewer is best) for the new project. Do not use the name of an existing Project.

PTXprint suggests a name from the bundle. Use no spaces or special characters. A message appears below the box if the name cannot be used.

#### Primary DBL site

Link · Basic+ · `lb_DBLdownloads`  
Also: Visit the Digital Bible Library to download a DBL Scripture bundle

> There are hundreds of Scripture bundles available at the Digital Bible Library website which you may download and use in a publication. You must log in to the site in order to access resources.
>
> Use resources which contain the text (not just the audio) and preferably select the USX download option.
>
> Note: If this option is disabled, it is due to the "Disable ALL Internet Use" option which has been set on the General section of the Advanced tab.

Opens the Digital Bible Library website in your browser.

#### Open.Bible site

Link · Basic+ · `lb_openBible`  
Also: Visit the Open.Bible site to download a Scripture bundle

> There are hundreds of Scripture bundles at the Open.Bible website which you may download and use in a publication.
>
> Use resources which contain the text (not just the audio) and preferably select the USX download option.
>
> Note: If this option is disabled, it is due to the "Disable ALL Internet Use" option which has been set on the General section of the Advanced tab.
>
> If you don't already have a Scripture Text Bundle, then you can download a USX or USFM text bundle from an online scripture repository.

Opens the Open.Bible website in your browser. Its bundles are openly licensed.

### Save Current Configuration As... (dialog)

#### OK

Button · Basic+ · `btn_cfg_ok`

Creates the new configuration, saves it, and changes to it. Greyed out until the name is valid.

#### Cancel

Button · Basic+ · `btn_cfg_cancel`

Closes the dialog. No new configuration is made.

#### Configuration Name – Enter a name for the configuration to be saved

Text box · Basic+ · `t_configName`

> Enter a name for the configuration to be saved.
>
> Note that only Roman/Latin names are supported using: a-z A-Z, 0-9, parentheses, underscores and hyphens. Spaces are not permitted.

Use a short, clear name such as `NT_A5` or `Draft_2col`. Letters with accents are not allowed. The message below the box says if the name is not valid or already exists. Write longer descriptions in **Notes** on the Basic tab.

#### Replace it if it already exists

Checkbox, off · Basic+ · `c_overwriteConfig`

> If a configuration with this name already exists, delete it and save the current settings in its place. (Useful for tests and tutorials that make a fresh copy each time they run.)

Leave it unticked in normal use; then PTXprint does not accept a name that already exists. When ticked, the old configuration is deleted when you click **OK**, and this cannot be undone. If you type the name of the configuration that you are in, PTXprint makes it again from the configuration it was first copied from (if PTXprint knows it), or else just saves it.

### Select Books To Export to PDF (dialog)

#### OK

Button · Regular+ · `btn_mbs_ok`

Puts the selected books in the book list, in normal Bible order. PTXprint changes to **Portions or Multiple Books** if any books are selected.

#### Cancel

Button · Regular+ · `btn_mbs_cancel`

Closes the book selector without changing the book list.

#### All Books

Button · Mini+ · `b_mbsAll`

> Click to turn ALL books on/off.

If all books are already selected, it unselects them all.

#### Old Testament

Button · Mini+ · `b_mbsOT`

> Click to turn OT books on/off.

If they are all selected already, it unselects them. Other books are not changed.

#### New Testament

Button · Mini+ · `b_mbsNT`

> Click to turn NT books on/off.

If they are all selected already, it unselects them. Other books are not changed.

#### Deuterocanon

Button · Mini+ · `b_mbsDC`

> Click to turn DC books on/off.

If they are all selected already, it unselects them. Other books are not changed.

#### Extra Material

Button · Mini+ · `b_mbsXtra`

> Click to turn Extra books on/off.

Extra books are for example the glossary (GLO), the indexes (TDX, NDX) and XXA–XXG. If they are all selected already, it unselects them. Other books are not changed.

#### Toggle Books

Button · Mini+ · `b_mbsToggle`

> Click to toggle ALL books. Those which are selected will be deselected, and the unselected ones will be selected.

For example, click **New Testament** and then **Toggle Books** to select everything except the New Testament.

#### Reset All

Button · Mini+ · `b_mbsNone`

> Click to turn OFF all books.

Use it to start your selection again.

#### Why is FRT not listed?

Label · Mini+

> The FRT book in Paratext contains front matter for a publication. Visit the Peripherals page to set up front matter for this publication.

### Copy Configuration To... (dialog)

#### OK

Button · Regular+ · `btn_mps_ok`

Copies the current configuration to all selected projects, using the option you chose. The copy uses the saved files, so click **Save** in the main window before you open this dialog.

#### Cancel

Button · Regular+ · `btn_mps_cancel`

Closes the dialog. Nothing is copied.

#### Recent

Drop-down · Regular+ · `ecb_mpsTargets`

> Shows selected target projects. Pick a previous selection from the dropdown, or select projects in the grid above.

You can also type project names here, separated by spaces. PTXprint remembers your last 10 selections, which helps when you copy to the same group of projects again and again.

#### Do NOT Replace Existing Config

Radio · Regular+ · `r_copyConfig_noReplace`  
Also: Copy Config: Do NOT Replace Existing Config

> Selecting this option will prevent any changes overwriting an existing configuration of the same name in the target project(s).
>
> This option is usually used when copying a configuration to other projects for the first time.

Projects that already have a configuration with this name are left unchanged. The safest choice.

#### Merge Configurations From Both

Radio · Regular+ · `r_copyConfig_merge`  
Also: Copy Config: MERGE Configurations From Both

> Selecting this option will MERGE the settings from the source configuration with the identically named configuration in the target project. Any changes that were made to the target project's configuration since it was first shared will be kept (i.e. modified target settings are retained if there is a clash of settings).

Settings not changed in the target are updated from this project.

#### Overwrite With Recent Changes

Radio · Regular+ · `r_copyConfig_overwrite`  
Also: Copy Config: OVERWRITE With Recent Changes

> Selecting this option will REPLACE (or overwrite) any settings in the identically named configuration in the target project IF those settings were changed in the source project since the configuration was first shared. (i.e. if both source and target projects modified a setting, then the source project's setting will "win").

Use it when this project is the "master" layout for a group of projects.

#### Keep each project's own language-specific variables

Checkbox, on · Regular+ · `c_copyConfig_skipVars`  
Also: Copy Config: Keep target project's own variables

> When checked, the variable values (such as the main title, subtitle and language name, and the Strong's index titles) are NOT copied, so each target project keeps its own. A configuration that is new to a target project starts without them, rather than with the source project's values.
>
> Uncheck this to copy these values as well.

The variables are listed on the **Peripherals** tab. After the copy, fill them in on each target project that did not have this configuration before.

### Lock/Unlock Configuration (dialog)

#### OK

Button · Regular+ · `btn_pw_ok`

Locks the configuration with the password you typed, or unlocks it if the password matches. If the configuration is not locked and the box is empty, nothing is locked and PTXprint asks for a password. If the password is wrong, the configuration stays locked and the status line says so.

#### Cancel

Button · Regular+ · `btn_pw_cancel`

Closes the dialog. Nothing is locked or unlocked, and the password box is cleared.

#### Enter Password – Enter password for config

Text box · Mini+ · `t_password`

> Enter a password of up to 16 characters to lock/unlock this saved configuration.

PTXprint stores only a coded form of the password. If you forget it, you cannot unlock the configuration in PTXprint, so keep it somewhere safe.

### Basic

#### Layout Configuration

Label · Mini+

> A Layout (or Config) is a collection of settings that can be saved. By naming and saving a layout you can recall those settings later.

#### Project

##### Project ID – Paratext project code

Drop-down · Mini+ · `fcb_project`  
Choices: Unknown

When you change the project, PTXprint saves the current configuration first and opens the last configuration you used with the new project. The last item, **Import...** (in blue), opens the **Import Scripture...** dialog.

##### Copyright & Licensing

Label · Regular+

> It is important to include copyright and license statements on every publication. By default this will be set according to the Paratext project settings, but you can edit it here if needed by expanding the section below.

##### Copyright & Licensing

###### Copyright

Label · Regular+

> It is important to include a copyright statement on every publication. By default this will be set according to the Paratext project settings, but you can edit it here if needed.

###### License – License details

Drop-down · Regular+ · `ecb_licenseText` · cfg `project/license`  
Choices: This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND). | This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC). | This work is licensed under a Creative Commons Attribution-Sharealike 4.0 International License (CC BY-SA). | This work is licensed under a Creative Commons Attribution 4.0 International License (CC BY). | All Rights Reserved.

> Select one of these licenses, or type a different license.
>
> Note: There are several shortcuts you can use:  
>    (c) --> ©  the copyright sign  
>    (r) --> ®  to denote registered trademarks  
>    (tm) --> ™  to denote trademarks in general
>
> Other special codes converted at print time:  
> Use ~ where a non-breaking space is needed. Use // to force a line break (:// in URLs is not changed).
>
> For more detailed information about the various Creative Commons licenses, refer to:  
> https://creativecommons.org/licenses/
>
> Select one of these licenses, or type a different license.
>
> Note: There are several shortcuts you can use:  
>    (c) --> ©  the copyright sign  
>    (r) --> ®  to denote registered trademarks  
>    (tm) --> ™  to denote trademarks in general
>
> Other special codes converted at print time:  
> use ~ for places where a non-breaking space is needed use // where a line break needs to be forced but :// used in URLs will still be preserved
>
> For more detailed information about the various Creative Commons licenses, refer to:  
> https://creativecommons.org/licenses/

Used in the front matter through `\zlicense`. Ask your organization which license to use.

###### Copyright text entry

Text area · Regular+ · `textv_copyright`

> It is important to include a copyright statement on every publication. Note: There are several shortcuts you can use:  
>    (c) --> ©  the copyright sign  
>    (r) --> ®  to denote registered trademarks  
>    (tm) --> ™  to denote trademarks in general
>
> Other special codes converted at print time:  
> Use ~ where a non-breaking space is needed. Use // to force a line break (:// in URLs is not changed).

PTXprint fills it from the Paratext project settings when it is empty. `(c)`, `(r)` and `(tm)` change to ©, ® or ™ as you type. Used in the front matter through `\zcopyright`.

###### Reload copyright from Paratext project

Button · Regular+ · `btn_resetCopyright`

> Clicking this button will reload the Copyright Statement from the Paratext project settings.

If Paratext has no copyright statement, PTXprint shows a message in the status line.

#### Layout Configuration

##### Notes – (Optional) Notes about configuration

Text box · Basic+ · `t_configNotes` · cfg `config/notes`

> Optional: Provide a description about the saved/shared configuration named above.

For example "A5 NT for village distribution, 2 columns". Saved with the configuration, so other team members see it after Send/Receive. Greyed out when the configuration is locked.

##### Name

Text box · Basic+ · `t_invisiblePassword` · cfg `config/pwd`

> Dots indicate that a password has been set for this configuration.

Empty when the configuration is not locked. You cannot type here; use the lock button.

##### Name – Lock configuration

Button · Mini+ · `btn_lockunlock`

> When Config is UNLOCKED:  
> Click to set a password to prevent anyone from accidentally changing the saved settings or deleting the configuration.
>
> When Config is LOCKED:  
> Click to enter the password to unlock this configuration and allow changes to be saved or the configuration to be deleted.
>
> Note that the Default config cannot be locked.

Opens the **Lock/Unlock Configuration** dialog. The icon shows whether the configuration is locked.

##### Name – Copy configuration to other projects

Button · Regular+ · `btn_copyToTargetProj`

> A saved configuration can be copied to other Paratext projects in order to avoid having to manually re-create all the same settings for a similar project.
>
> Save first: the saved files are copied. Adjust lists are not copied.

Opens the **Copy Configuration To...** dialog. Greyed out when **Default** is selected (hold the mouse over the button to see why).

##### Name

Drop-down · Mini+ · `ecb_savedConfig`  
Choices: Default

> Select a previously-saved layout configuration to retrieve those settings.
>
> Note: changes to the current configuration are not saved automatically when you switch. Save first to keep them.
>
> When the Paratext project is shared through Send/Recv, all saved layout configurations will also be made available to other PTXprint users of the same Paratext project.
>
> Alternatively, select a previously-saved layout configuration to retrieve settings.

Choose a configuration to load its settings. Click **Save** first.

##### Enter a name for the layout configuration to be saved.

Text box · Mini+ · `t_savedConfig`

> Enter a name for the layout configuration to be saved.
>
> Note that only Roman/Latin names are supported using: a-z A-Z, 0-9, parentheses, underscores and hyphens.
>
> Longer descriptions may be typed into the Notes field below.

The text part of the configuration **Name** box. Type a new name and click **Save** to create a new configuration from the current settings. Characters that are not allowed (such as spaces) are removed.

##### gtk-save-as

Button · Mini+ · `b_saveAsNewConfig`

> Save the current settings as a new Configuration.
>
> When the Paratext project is shared through Send/Recv, all saved configurations will be also made available to other PTXprint users of the same Paratext project.

Opens the **Save Current Configuration As...** dialog. The new configuration starts with the current settings, including unsaved changes. Use it to start a new publication from an existing one, or to make an unlocked copy of a locked configuration.

##### Delete

Button · Basic+ · `btn_deleteConfig`  
Also: Delete configuration

> Delete this Saved Configuration
>
> This also deletes the corresponding subfolder of temporary files in the local\ptxprint folder but does not delete the previously created PDF files which will remain in that folder.

Deletes the selected configuration after you click **Yes** in the **Please Confirm...** dialog. The dialog names the configuration, so check the name. PTXprint first changes to the **Default** configuration, then deletes the settings and working files of the old one. Other configurations are not touched. This cannot be undone. If some files cannot be deleted (for example because they are open in another program), the status line lists them. For the **Default** configuration you see **Reset** instead. Greyed out when the configuration is locked, and in the **Mini** view.

##### Reset

Button · Regular+ · `btn_resetDefaults`

> Reset the Default configuration to PTXprint's default settings.
>
> Warning: this also deletes the files kept in the Default configuration folder (such as styles, picture list, adjust lists and front matter). There is no confirmation.

Only shown when the **Default** configuration is selected. PDF files are kept. The status line confirms when the reset is done. Use it only when you really want to start again. Greyed out in the **Mini** and **Basic** views.

##### Name – Import settings from PDFs, ZIP files or other Configurations

Button · Basic+ · `btn_importSettings`

> Open the Import Settings dialog to select options for importing settings from other PDFs, ZIP archives, or different project configurations.
>
> By default, imported settings are applied to the current project and configuration. However, you can also choose to import them into other projects or export them to an external folder.

In the dialog you also choose which groups of settings to bring in. See the chapter "Importing settings".

##### Run Tutorial...

Button · Basic+ · `btn_runTutorial`

> Step through a tutorial on the current project and configuration: a list of actions saved as .json from the test replay window, or the actions in a recorded test (.zip).

Opens a file chooser for the tutorial file, then a small tutorial window. The steps really change the settings, so use a practice configuration. See "Run a tutorial" in this chapter.

#### What to Print

##### Single book chooser

Drop-down · Mini+ · `ecb_book` · cfg `project/book`  
Choices: NONE

Used when **Single Book** is selected. When you choose a book, PTXprint sets **From Chapter** to 1 and **To** to the last chapter of that book, and changes to **Single Book**.

##### Select Multiple Books...

Button · Mini+ · `btn_chooseBooks`  
Also: Multiple book selector

> Select one or more Biblical books to be printed from the project.

Opens the **Select Books To Export to PDF** dialog. Shortcut: **Alt+O**.

##### Bible Module

Radio · Basic+ · `r_book_module` · cfg `project/bookscope=module`  
Also: Bible module selector

> Print a Paratext Bible module (a .sfm file that lists the passages to include).

The module file is usually in the project's `Modules` folder. Choose it with **Choose...**.

##### Portions or Multiple Books

Radio · Mini+ · `r_book_multiple` · cfg `document/multibook`  
Also: Choose books or enter ranges to print

> Print several books, or the passages listed in the box.

Use it for several books, a range such as `MAT-REV`, or selected passages such as `PSA 23; 100`. PTXprint changes to this option when you type in the book list or pick books with **Select Multiple Books...**.

##### Single Book

Radio · Mini+ · `r_book_single` · cfg `project/bookscope=single`  
Also: Single book selector

> Print one book, or a range of its chapters.

Use **From Chapter** and **To** for a range of chapters.

##### Use 3-letter USFM book codes (e.g. JHN, not John; MRK, not M...

Drop-down · Mini+ · `ecb_booklist` · cfg `project/booklist`, `document/subject`

> Use 3-letter USFM book codes (e.g. JHN, not John; MRK, not Mark).
>
> A list of references can be entered if printing less than an entire book or chapter, or if you need to include portions from several books. For example:  
>   JHN 2:1-12  
>   MRK 1-5  
>   PSA 23; 100; 117  
>   EXO 20:12-17 MAT 5:3-11  
>   GEN 1:1-2:3 PSA 23:1-end LUK 15:11-32 GLO  
>   GEN 24:1-17; 24:22-30  
>   MAT-REV
>
> If working on several books, use the Select Multiple Books... button to select them. For example:  
>   LUK ACT GLO NDX prints Luke, Acts, Glossary and Names Index. The list is editable, so books can be re-ordered if need be (for example, for the Hebrew canon).
>
> Shortcut: Ctrl-B

Separate items with spaces. Books print in the order you type. The drop-down remembers your recent lists.

##### Multiple books editable list entry

Text box · Mini+

> Use 3-letter USFM book codes (e.g. JHN, not John; MRK, not Mark).
>
> A list of references can be entered if printing less than an entire book or chapter, or if you need to include portions from several books. For example:  
>   JHN 2:1-12  
>   MRK 1-5  
>   PSA 23; 100; 117  
>   EXO 20:12-17 MAT 5:3-11  
>   GEN 1:1-2:3 PSA 23:1-end LUK 15:11-32 GLO  
>   GEN 24:1-17; 24:22-30  
>   MAT-REV
>
> If working on several books, use the Select Multiple Books... button to select them. For example:  
>   LUK ACT GLO NDX prints Luke, Acts, Glossary and Names Index. The list is editable, so books can be re-ordered if need be (for example, for the Hebrew canon).
>
> Shortcut: Ctrl-B

##### From Chapter

Text box · Mini+ · `t_chapfrom` · cfg `document/chapfrom`

> If you want to print less than the entire book, enter the chapter number to start at.

Only numbers are allowed. If you type a number below 1 or above the last chapter, PTXprint corrects it. Typing here selects **Single Book**.

##### To

Text box · Mini+ · `t_chapto` · cfg `document/chapto`

> If you want to print less than the entire book, enter the chapter number to end with.

PTXprint corrects numbers that are too high or lower than **From Chapter**. Typing here selects **Single Book**.

##### Choose...

Button · Basic+ · `btn_chooseBibleModule` · cfg `project/modulefile`  
Also: Bible module chooser button

Opens a file chooser (in the project's `Modules` folder) to select the module .sfm file. The file name is then shown next to the button and **Bible Module** is selected. If you cancel, PTXprint changes back to **Single Book**. Shortcut: **Alt+O**.

##### Edit...

Button · Regular+ · `btn_editModule`  
Also: Edit Bible module

> Switch to the View+Edit tab to show the selected Bible module.

Only works after you have chosen a module. You can look at the module there or change it.


# 5. Layout tab

## 5.1 What this tab is for

The **Layout** tab sets the shape of every page: page size, margins (the empty space around the text), one or two columns, the size of the main text and the space between lines.

Come here when you start a new publication, when the printer tells you the page size, or when the text does not fit the number of pages you want. Most settings change the whole book. After a change, click **Print** again to see the result.

Some words used in this chapter:

* **pt (point)** – a small unit used for type. 1 pt is about 0.35 mm. 72 pt is about one inch (25.4 mm).
* **Baseline** – the invisible line that the letters sit on.
* **Line spacing** – the distance from the baseline of one line to the baseline of the next.
* **Gutter** – an extra empty space. A *binding gutter* is extra space at the spine of the book. A *column gutter* is the space between two columns of text.
* **Text area** – the part of the page where the main text goes. The margins are outside it.

## 5.2 Page Setup

This area holds **Page Size**, **Base Font Size (pt)**, **Base Line Spacing (pt)**, **Base Indent**, the binding gutter and the page-layout options.

### Page size

Choose a size from the **Page Size** list, or type your own: width, comma, height, for example `148mm, 210mm`. You can use `mm`, `cm` or `in`. A typed size is saved when you save the configuration (or click **Print**). After that, it is in the list for all your projects. To remove a saved size, select it, right-click in the box and choose **Remove**. Ask your printer for the exact trim size (the size of the finished, cut page) before you start. Changing the page size later moves every line.

### Font size and line spacing (and how they work together)

* **Base Font Size (pt)** is the size of the letters in normal paragraphs. All other text (headings, footnotes, verse numbers and so on) is sized *relative to* it. A bigger base font makes headings and footnotes grow by the same proportion.
* **Base Line Spacing (pt)** is the distance from one line to the next. It is normally bigger than the font size, so that the lines do not touch. 11 pt text with 14 pt line spacing is a common choice.

The **Lock Ratio** box (ticked by default) joins these two numbers:

* When it is ticked and you change the font size, the line spacing changes by the same proportion. For example, 11 pt text on 14 pt spacing changed to 12 pt text gives about 15.3 pt spacing. The page keeps the same "look", only bigger.
* It also works the other way round: changing the line spacing changes the font size.
* When it is not ticked, you can change each number on its own. Use this for more (or less) space between lines with the same size letters.
* When you tick it again, PTXprint keeps the ratio the two numbers have *now*.

The line spacing decides how many lines fit on a page.

### Lines Per Page and the fine-tune buttons

**Lines Per Page** is calculated from the page height, the top and bottom margins and the line spacing. It updates when you change any of these.

* **Blue**: a whole number of lines fits the text area. No space is wasted.
* **Red**: the text area holds a whole number of lines plus part of a line. That part of a line is empty space at the bottom of each page.

When the number is red, three small fine-tune buttons (icon of justified lines) become active. One is next to **Base Line Spacing (pt)**. The other two are next to the top and bottom margins in the **Margins** area. Each makes a small change so that a whole number of lines fits:

* If more than half a line is spare, it makes room for one more line.
* If less than half a line is spare, it spreads the same lines a little further apart (or makes the margin a little larger).

Click only **one** of the three buttons: the one for the setting you are most willing to change. The number turns blue and the buttons become grey again.

If **Lock Ratio** is ticked, the line-spacing button also changes the font size a little. To keep the font size exact, untick **Lock Ratio** first, or use a margin button.

### Binding gutter, Outer Gutter and Mirror Pages

* **Binding Gutter (mm)** adds extra space to the inner edge of each page (near the spine), on top of **Side Margin Width**. Thick books need more, because the pages curve into the spine. The gutter changes sides on odd and even pages, so it is always at the spine.
* **Outer Gutter** moves that extra space to the outer edge, for journaling or wide-margin Bibles where readers write in the outer margin.
* **Mirror Pages** makes odd and even pages mirror each other. Header items on the left of a right-hand page appear on the right of a left-hand page, so they stay on the outer (or inner) edge. In a diglot (two-language) layout it also keeps the primary text on the inner side, near the spine.

Whether the gutter swaps sides on odd and even pages is controlled by **Double Sided Layout** (**Advanced** tab, **Other** tab, **Page Layout and Spacing**). It is normally on.

### Align Text to Baseline / Variable Line Spacing

This is a switch with **Align Text to Baseline** on the left and **Variable Line Spacing** on the right.

* **Align Text to Baseline** (left, the normal setting) puts every line on a fixed grid. Lines on the front and back of a sheet line up exactly. This matters on thin Bible paper, where the other side shows through. But some columns may end with an empty line or two. You fix these by hand with the page-filling tools in the PDF Preview.
* **Variable Line Spacing** (right) stretches the space between lines a little so that every column is filled to the bottom. Good for quick drafts and thicker paper. Front-to-back alignment is lost, and the whole book re-flows when you change it.

Switching to **Variable Line Spacing** also ticks **Fill Columns** and **Allow Unbalanced Columns**. How much lines may stretch or shrink is set on the **Advanced** tab, **Other** tab, **Page Layout and Spacing**.

### Notelines (journaling layout)

**Notelines** prints ruled lines in a wide margin for readers' own notes. Ticking it also ticks **Binding Gutter** and **Outer Gutter**, and sets the gutter to 40 mm if it was under 30 mm. A colour button appears for the line colour. More noteline settings (spacing, offset, type) are on the **Advanced** tab, **Other** tab, **Page Layout and Spacing**.

### Margin Notes

**Margin Notes Col Width (mm)** creates an extra column beside the text. Footnotes, cross-references and (if you choose) section headings can go in it, beside their verse. Ticking it only creates the space. To put notes there, choose **Side Margin** as the position on the **Notes+Refs** tab. To put headings there, tick **In Margin** on the **Body** tab.

The column is normally on the right (or outer) edge. In a one-column layout, tick **Margin Notes on Left/Inner** to put it on the left (or inner) edge.

If too many notes do not fit beside the text in one column, PTXprint moves the extra notes to the top of the margin column of the next column or page. This happens by itself; there is no setting for it. Check those pages in the PDF Preview, because a moved note is no longer beside its verse.

These settings are shown in the **Regular** and **Full** views.

## 5.3 Two Column Layout

Tick **Two Column Layout** for two columns of main text; untick it for one. When you change this, PTXprint halves (two columns) or doubles (one column) **Base Indent**, because a narrow column needs a smaller indent.

Most settings in this area only work with two columns:

* **Gutter Width (mm)** – the space between the columns. 4 mm is common.
* **Vertical Rule in Gutter** – a thin line down the middle of the gutter.
* **Adjust Top (pt)** – moves the top of that line up (negative) or down (positive). Greyed out until **Vertical Rule in Gutter** is ticked.
* **Allow Unbalanced Columns** – lets the two columns on a page end at different heights, by up to a set number of lines.

**Thickness of Rule (pt)** also works in one column, because it also sets the horizontal rule under the header.

A diglot (two languages side by side) needs two columns, so the **Two Column Layout** box is then greyed out.

## 5.4 Margins

The **Margins** area sets the empty space around the text, and the position of the header (the line at the top of the page, often with the book name and page number) and the footer (the line at the bottom).

### The margin diagram and its colours

Next to the margin settings is a small picture of a page. It shows one or two columns, the vertical rule and the header rule, as you have set them. Coloured arrows show what each number measures:

* **Orange** – **Side Margin Width (mm)**: from the edge of the page to the text.
* **Red** (top) – **Start of Page to Top of Text (mm)**: the top margin.
* **Red** (bottom) – **Bottom of Text to End of Page (mm)**: the bottom margin.
* **Purple** (top) – **Bottom of Header to Top of Text (pt)**: header-to-text gap.
* **Purple** (bottom) – **Bottom of Text to Top of Footer (pt)**: text-to-footer gap.
* **Green** – **Space between Rule and Top of Text (pt)**: rule-to-text gap.
* **Blue** – two values PTXprint calculates (you cannot type in them): top of page to header, and footer to bottom of page.

When the mouse is over a margin box, the picture shows only that box's arrow.

Margins are in **mm**, but the header and footer gaps are in **pt**.

### Header and footer position

The header sits *inside* the top margin, and the footer normally sits *inside* the bottom margin. So a bigger header gap moves the header up towards the page edge. Watch the blue numbers: if one becomes very small (or negative), the header or footer is too close to the edge and may be cut off when the book is trimmed.

Tick **Place Footer Text Above the Bottom Margin** to put the footer inside the text area instead of in the margin.

Tick **Horizontal Rule** to draw a line under the header. Set its position with **Space between Rule and Top of Text (pt)**.

To see the margins, header and footer areas on the page, tick **Guides and Baselines** on the **Content** tab of the **PDF Preview** window.

## 5.5 Change the Grid Settings dialog (graph paper)

PTXprint can show a "graph paper" grid over the pages in the **PDF Preview**, to measure things such as a margin or a picture.

Open the **PDF Preview**, go to its **Content** tab and tick **Graph Paper**. Click **Settings** next to it to open the **Change the Grid Settings** dialog. There you choose:

* **Major Units** – centimetres or inches between the thicker (major) lines, plus their colour and thickness.
* **Minor Divisions** – how many thinner lines between two major lines, plus their colour and thickness.
* **Place Grid** – **Whole Page**, **In Margin Areas** or **Only in Text Area**.

## 5.6 Lock UI Layout Settings

When the typesetting is almost finished, you can protect the layout from accidental changes. On the **Advanced** tab, **Main** tab, **General** area, tick **Lock UI Layout Settings**. (This is only shown in the **Full** view.)

While it is ticked, most of the **Layout** tab is greyed out (page size, font size, line spacing, columns, gutter, margins and more). The whole **Fonts+Script** tab and the **Styles** tab are also greyed out. Untick it to make changes again.

## 5.7 Common tasks

### How do I change the page size?

1. On the **Layout** tab, **Page Setup** area, click the **Page Size** list.
2. Choose a size, for example **148mm, 210mm (A5)**, or type width, comma, height, for example `140mm, 216mm`.
3. If **Lines Per Page** is red, click one fine-tune button (see the next task).
4. Click **Print**.

### How do I stop wasting space at the bottom of every page?

1. On the **Layout** tab, look at **Lines Per Page** (shown in the **Regular** and **Full** views).
2. If it is red, click one fine-tune button: next to **Base Line Spacing (pt)**, or in the **Margins** area next to the top or bottom margin. Choose the setting you are most willing to change.
3. The number turns blue. Click **Print**.

### How do I make the text bigger or smaller without changing the look of the page?

1. On the **Layout** tab, make sure **Lock Ratio** is ticked.
2. Change **Base Font Size (pt)**. The line spacing changes with it.
3. If **Lines Per Page** is red, click one fine-tune button.
4. Click **Print**.

### How do I put more space between the lines but keep the same letter size?

1. On the **Layout** tab, untick **Lock Ratio**.
2. Make **Base Line Spacing (pt)** larger, for example from 14 to 15.
3. Tick **Lock Ratio** again if you want the new ratio kept.
4. Click **Print**.

### How do I change between one and two columns?

1. On the **Layout** tab, tick or untick **Two Column Layout**.
2. For two columns, set **Gutter Width (mm)** and choose whether you want **Vertical Rule in Gutter**.
3. Check **Base Indent**. PTXprint changes it automatically, but you may want to adjust it.
4. Click **Print**.

### How do I add extra space at the spine for binding?

1. On the **Layout** tab, **Page Setup** area, tick **Binding Gutter (mm)**.
2. Type the extra space in the box beside it, for example 5 mm. Ask your printer how much your book's thickness needs.
3. Leave **Outer Gutter** unticked.
4. Click **Print**.

### How do I make a journaling (wide-margin) Bible?

1. On the **Layout** tab, tick **Notelines** (shown in the **Regular** and **Full** views). PTXprint ticks **Binding Gutter** and **Outer Gutter** and sets a wide gutter (at least 40 mm).
2. Change the gutter width if needed, and choose the line colour with the colour button.
3. Click **Print**.

### How do I put footnotes and cross-references in the side margin?

1. On the **Layout** tab, tick **Margin Notes Col Width (mm)** and type the column width.
2. On the **Notes+Refs** tab, set the position of footnotes and/or cross-references to **Side Margin**.
3. For section headings in the margin too, tick **In Margin** on the **Body** tab.
4. For the column on the left (or inner) edge, tick **Margin Notes on Left/Inner** (one column only).
5. Click **Print**.

### How do I see a measuring grid on the page?

1. Click **Print** so that the **PDF Preview** opens.
2. On the preview's **Content** tab, tick **Graph Paper**.
3. Click **Settings** next to it to change units, colours and where the grid is drawn. Click **OK**.

## 5.8 Common problems

### Almost everything on the Layout tab is greyed out

**Cause:** **Lock UI Layout Settings** is ticked. This also greys out the whole **Fonts+Script** tab and the **Styles** tab.

**What to do:** Change the view level to **Full**. On the **Advanced** tab, **Main** tab, **General** area, untick **Lock UI Layout Settings**.

### I changed the font size and the line spacing changed too (or the other way round)

**Cause:** **Lock Ratio** is ticked (the normal setting).

**What to do:** Untick **Lock Ratio** before you change one number on its own.

### I clicked the line-spacing fine-tune button and my font size changed

**Cause:** **Lock Ratio** is ticked, so the font size follows the line spacing.

**What to do:** Untick **Lock Ratio** and type your font size again. Then use the fine-tune button again, or use the top or bottom margin button instead.

### The fine-tune buttons are greyed out

**Cause:** **Lines Per Page** is already a whole number (blue), so there is nothing to fix. They are also greyed out when **Lock UI Layout Settings** is ticked.

### The fine-tune buttons and Lines Per Page are not visible

**Cause:** They are only shown in the **Regular** and **Full** views. Change the view level from the main menu.

### I cannot untick Two Column Layout

**Cause:** A diglot (two languages) is set up. A diglot needs two columns.

### The Base Indent changed by itself

**Cause:** Switching between one and two columns halves or doubles the indent.

**What to do:** Type the indent you want after you change the number of columns.

### "Margin Notes on Left/Inner" is greyed out

**Cause:** It only works with one column, and only when **Margin Notes Col Width (mm)** is ticked.

### Margin notes do not appear even though I ticked Margin Notes

**Cause:** The Layout tab setting only makes the space.

**What to do:** On the **Notes+Refs** tab, choose **Side Margin** for footnotes and/or cross-references.

### The header or footer is too close to the edge of the page

**Cause:** The header or footer gap is large compared with the top or bottom margin. The header and footer sit inside the margins.

**What to do:** Check the blue numbers in the margin diagram. Make the top (or bottom) margin larger, or make **Bottom of Header to Top of Text (pt)** (or **Bottom of Text to Top of Footer (pt)**) smaller.

### Columns end at different heights, or there are gaps at the bottom of columns

**Cause:** With **Align Text to Baseline**, lines sit on a fixed grid, so some columns can end early.

**What to do:** For a draft, move the switch to **Variable Line Spacing**. For a final Bible on thin paper, keep **Align Text to Baseline** and fix the pages with the page-filling tools in the PDF Preview. In two columns, **Allow Unbalanced Columns** also lets the columns end at different heights.

### The binding gutter is always on the same side of the page

**Cause:** **Double Sided Layout** is off (**Advanced** tab, **Other** tab, **Page Layout and Spacing**). Or **Outer Gutter** is ticked, which moves the gutter to the outside edge.

### The Notelines colour button is missing

**Cause:** It is only shown when **Notelines** is ticked.

## 5.9 Settings reference

### Change the Grid Settings (dialog)

#### OK

Button · Regular+ · `btn_guides_ok`

Redraws the PDF Preview with the new grid (shown only if **Graph Paper** is ticked).

#### Cancel

Button · Regular+ · `btn_guides_cancel`

Closes the dialog. The grid in the preview is not redrawn.

#### Grid Settings

##### Major Units – Grid: Major line color

Colour · Regular+ · `col_gridMajor` · cfg `grid/majorcolor`

> The color of the major (thicker) grid lines.

A strong colour (for example red) makes the major lines easy to count.

##### Minor Divisions – Grid: Minor line color

Colour · Regular+ · `col_gridMinor` · cfg `grid/minorcolor`

> The color of the minor (thinner) grid lines between the major lines.

A light colour keeps the text readable under the grid.

##### Major Units – Grid: Major line thickness

Number · Regular+ · `s_gridMajorThick` · cfg `grid/majorthickness`

> Specify the thickness of the major lines.

In pt. Small values such as 0.2 are usually enough.

##### Minor Divisions – Grid: Minor line thickness

Number · Regular+ · `s_gridMinorThick` · cfg `grid/minorthickness`

> Specify the line thickness of the minor divisions.

In pt. Keep it at or below the major thickness so the two kinds of line look different.

##### Minor Divisions – Grid: Number of minor divisions

Number · Regular+ · `s_gridMinorDivisions` · cfg `grid/divisions`, `grid/xyadvance`

> Specify the number of minor divisions there should be between the thicker (major) lines. Recommendations: 2, 5, or 10 for centimeters, and 3, 4, 6, or 12 for inches.

With **Centimeters**, 5 gives 2 mm squares and 10 gives 1 mm squares.

##### Place Grid – Grid: Reload default values

Button · Regular+ · `btn_resetGrid`

> Clicking this button will refresh the default Grid settings:  
> Centimeters with 5 divisions (2mm each), red major and light blue minor lines (0.2pt thickness), over the whole page.

Puts all grid settings back to the defaults listed in the tooltip.

##### Major Units – Grid: Select major units

Drop-down · Regular+ · `fcb_gridUnits` · cfg `grid/units`  
Choices: Centimeters | Inches

> The grid can use Centimeters or Inches as the major units.

Use the unit your printer or publisher uses for their measurements.

##### Place Grid – Grid: Starting position (page or margin)

Drop-down · Regular+ · `fcb_gridOffset` · cfg `grid/xyoffset`  
Choices: Whole Page | In Margin Areas | Only in Text Area

> The grid can start at the top-left corner of the Page, or at the top-left Margin.
>
> Depending on what you are trying to measure, it can be helpful to position the grid at the top-left corner of the page, or margins.

**Whole Page** starts at the top-left corner of the page: best for measuring margins. **Only in Text Area** starts at the corner of the text: best for measuring things in the text, such as pictures. **In Margin Areas** draws the grid only in the margins, so the text stays clear.

### Layout

#### Two Column Layout

Checkbox, on · Mini+ · `c_doublecolumn` · cfg `paper/columns`  
Also: One or two column layout · Greyed out by: “Lock UI Layout Settings”

> Tick to set the main text in two columns; untick for a single column.
>
> If this setting is checked on, but inactive, it is due to Diglot being active (which obviously must use the Two Column layout).
>
> If you get an unexpected result, check the "Use One/Two Column Layout ..." setting near the end of the Body tab which is only accessible when using the Full View mode.

Switching re-flows the whole book and halves or doubles **Base Indent**.

#### Page Setup

##### Binding Gutter (mm)

Checkbox, off · Basic+ · `c_pagegutter` · cfg `paper/ifaddgutter`  
Also: Use binding gutter · Greyed out by: “Lock UI Layout Settings”

> This is the amount of space to be given on the inner edge of each page for binding (millimeters).
>
> However, if Outer Gutter is enabled this extra space will appear on the outside edge of each page. This can be useful for a journaling layout.

Thick books need more space because the pages curve into the binding. Ask your printer for a value. **Notelines** ticks this for you.

##### Binding gutter amount

Number · Basic+ · `s_pagegutter` · cfg `paper/gutter`  
Values: -200–200 · Needs: “Binding Gutter (mm)” · Greyed out by: “Lock UI Layout Settings”

> This amount is added to the ‘Side Margin Width’ amount to the inner edge (or outside edge, if you check ‘Outer Gutter’).

In mm. A few mm is common for a normal book; 40 mm or more for a journaling layout.

##### Base Line Spacing (pt) – Base line spacing

Number · Basic+ · `s_linespacing` · cfg `paragraph/linespacing`  
Values: 4–100 (default 14) · Greyed out by: “Lock UI Layout Settings”

> Base Line spacing in points (pts). Change to increase or decrease space between lines of text.
>
> This is the base line spacing for default paragraph text.

A bigger value gives fewer lines per page. If **Lock Ratio** is ticked, changing this also changes **Base Font Size (pt)**. Line spacing for other paragraph types (for example footnotes) is set relative to this on the **Styles** tab.

##### Page Size – Page size setting

Drop-down · Mini+ · `ecb_pagesize` · cfg `paper/height`, `paper/width`, `paper/pagesize`  
Choices: 210mm, 297mm (A4) | 148mm, 210mm (A5) | 105mm, 148mm (A6) | 176mm, 250mm (B5) | 125mm, 176mm (B6) | 210mm, 280mm (PA4) | 140mm, 210mm (PA5) | 105mm, 140mm (PA6) | 8.5in, 11in (Letter) | 5.5in, 8.5in (1/2 Letter) | 5.25in, 8.25in (133x210mm) | 5.8in, 8.7in (147x221mm) | 6in, 9in (152x229mm) | 184.6mm, 271.6mm (A4 with cropmarks) | 165mm, 234mm (KBS max page) · Greyed out by: “Lock UI Layout Settings”

> Type required page width and height,  
>      for example:    148mm, 208mm or select from the list of preset values. A size you type is saved for use in all projects. To remove one, right-click it and choose Remove.

The finished (trimmed) page size. You can use mm, cm or in. A typed size is saved when you save the configuration. Set this before detailed page work, because every page re-flows when it changes.

##### Base Font Size (pt) – Base font size

Number · Mini+ · `s_fontsize` · cfg `paper/fontfactor`  
Values: 2–36 (default 11) · Greyed out by: “Lock UI Layout Settings”

> Set the point size of the main body text.
>
> This is the base font size for default paragraph text. All other font sizes are calculated (according to their factor size) based on this value.

Headings, footnotes, verse numbers and other text grow or shrink with it. 9–12 pt is typical for Bibles. If **Lock Ratio** is ticked, changing this also changes **Base Line Spacing (pt)**.

##### Base Indent – Base paragraph indent

Number · Regular+ · `s_indentUnit` · cfg `document/indentunit`  
Greyed out by: “Lock UI Layout Settings”

> The amount by which paragraphs should be indented (inches). This also affects poetry indentation. (default=1, min=0, max=4)
>
> The space by which paragraphs should be indented (inches). This also affects poetry indentation. Note that for a single-column text this value needs to be higher than for two-column texts, and the value updates automatically when you change from 1 to 2 columns, and vice versa.

0.5 inch is about 13 mm. Each paragraph style uses a multiple of this value. PTXprint halves it when you switch to two columns and doubles it when you switch to one.

##### 99.9

Label · Regular+ · `l_linesOnPage`

> This is an approximate calculation of the most number of lines that will fit on a page. An exact count is difficult due to ascent and descent values of the main body font.

Blue: a whole number of lines fits. Red: part of a line is wasted at the bottom of each page; click one fine-tune button. The estimate uses page height, top and bottom margins, line spacing and the font. It does not know about headings, pictures or footnotes.

##### Lines Per Page

Label · Regular+ · `l_linesOnPageLabel`

> This is an approximate calculation of the most number of lines that will fit on a page. An exact count is difficult due to ascent and descent values of the main body font.

Label for the estimate beside it.

##### Tweak line spacing (auto adjust)

Button · Regular+ · `btn_adjust_spacing`  
Greyed out by: “Lock UI Layout Settings”

> Fine Tune Line Spacing:
>
> This button is only active when PTXprint has a suggestion to shrink or expand the line spacing slightly to minimise wasted vertical space on the page. Click to accept the suggestion.
>
> If there is more than half a line of 'spare' space on the page then the line-spacing will decrease slightly to fit one more line of text on the page.
>
> If there is less than half a line of 'spare' space on the page then the line-spacing will increase slightly to fill the page more evenly (with the same number of lines of text).
>
> If you prefer to keep the exact line spacing specified, then do NOT click this option. Instead, use the similar button to adjust either the Top or Bottom Margin.
>
> Note: if Lock Ratio is ticked, the font size will also change slightly.

Only active when **Lines Per Page** is red. To keep the font size exact, untick **Lock Ratio** first or use a margin fine-tune button.

##### Outer Gutter

Checkbox, off · Regular+ · `c_outerGutter` · cfg `paper/ifoutergutter`  
Also: Place gutter on outer edge of page · Needs: “Binding Gutter (mm)” · Greyed out by: “Lock UI Layout Settings”

> An Outer Gutter can be used to create additional whitespace (for notes etc.) on the OUTER edge of each page as commonly seen in a journaling layout.

You still need a normal side margin for the spine.

##### Lock Ratio

Checkbox, on · Regular+ · `c_lockFontSize2Baseline` · cfg `paper/lockfont2baseline`  
Also: Lock ratio of font size to line spacing · Greyed out by: “Lock UI Layout Settings”

> Lock the ratio of the Base Font Size to the Base Line Spacing so that the spacing grows/shrinks according to the size of the font; or the font size changes when the spacing changes.

When you tick it again, the current ratio is kept. While ticked, the line-spacing fine-tune button also changes the font size.

##### Align Text to Baseline – Align Text to Baseline Grid (On-Grid/Off-Grid)

Switch · Basic+ · `c_noGrid` · cfg `document/nogrid`

> For high quality typesetting it is best practice to Align the Text to the (baseline) Grid. This ensures consistent line spacing and front-to-back registration.
>
> However, for quick draft printouts or typesetting for thicker paper, Variable Line Spacing mode enables vertical justification which fills each column of text as needed to use up the entire page.
>
> Warning: This is a major 'mode' change. Everything will shift as a result. Consider carefully before changing this setting.
>
> For high quality typesetting it is best practice to Align the Text to the Baseline (i.e. on grid). This ensures consistent line spacing and front-to-back registration.
>
> Note that this may leave larger empty spaces at the end of pages which will need to be manually adjusted using the Adjust List.

Left (**Align Text to Baseline**): every line on a fixed grid; best for final Bibles on thin paper. Right (**Variable Line Spacing**): line spacing stretches to fill columns; best for drafts and thick paper. Switching right also ticks **Fill Columns** and **Allow Unbalanced Columns**.

##### Fill Columns

Checkbox, off · Basic+ · `c_variableLineSpacing` · cfg `document/varlinespacing`  
Also: Variable/Increased Line Spacing · Needs: “noGrid”

> A small increase in the (vertical) line spacing allows the text to stretch to fill the entire column.
>
> This is called vertical justification and is useful for Draft Printouts where the page can be filled without manual intervention to eliminate unwanted gaps at the end of columns. The setting 'Allow Unbalanced Columns' automatically gets enabled when you choose this setting.
>
> Allowing a small increase in the (vertical) line spacing allows the text to stretch vertically to fill the entire column.
>
> This will also enable 'Fill Columns', but you can turn that off to see how much extra space there is at the end of each column.
>
> Warning: This will cause major changes to the layout of the entire document. It will also place headings exactly rather than rounding to the nearest number of lines.
>
> Do NOT use this setting if doing final typesetting for thin Bible paper as front-to-back registration is not enforced with Variable Line Spacing.

Ticked automatically when you move the switch to **Variable Line Spacing**. The stretch allowed is set on the **Advanced** tab, **Other** tab, **Page Layout and Spacing**.

##### Notelines

Checkbox, off · Regular+ · `c_noteLines` · cfg `paper/notelines`, `paper/ifnotelines_`

> Include ruled margins to provide space for personal notes, reflections, and artwork. Typically called 'Journaling Bibles' or 'Wide-Margin Bibles'.
>
> Hint: Set the Binding Gutter to a larger value (>40mm) and enable Outer Gutter. Other settings to control the appearance and spacing of the Notelines are in the 'Page Layout and Spacing' section of the Advanced > Other tab.

Ticking it also ticks **Binding Gutter** and **Outer Gutter**, and sets the gutter to 40 mm if it was under 30 mm. A colour button appears beside it.

##### Set the color of the Notelines.

Colour · not shown · `col_noteLines` · cfg `paper/majornlcolor`

> Set the color of the Notelines.

Shown only when **Notelines** is ticked. A light grey or light colour does not distract from the text.

##### Mirror Pages

Checkbox, on · Basic+ · `c_mirrorpages` · cfg `header/mirrorlayout`  
Also: Mirror page layout · Greyed out by: “Lock UI Layout Settings”

> Mirror Pages makes use of an Inner+Outer layout. This will make the left page header the inner header and the right page header will be shown on the outer edge (i.e. headers on odd and even pages are mirrored).
>
> Behaviour for Diglots:  
> Note that when creating a Diglot, this will place the primary text as the Inner text (closest to the spine), and the secondary text as the Outer text (closest to the edge of the page).
>
> If you always want the Primary text on the left and Secondary text on the right regardless of whether it is an odd or even page, then turn off this option.

For example, the page number stays on the outer edge of both left and right pages.

##### Margin Notes Col Width (mm)

Checkbox, off · Regular+ · `c_useMarginNotes` · cfg `paper/ifmarginnotes`, `document/marginnotes`  
Also: Place Footnotes, Cross-references and Headings in Margin

> Enabling this will allow Notes (footnotes and/or cross-references) and optionally Headings (and their corresponding Parallel Passage references) to be place in a wider margin area in a way that makes them easier to access by the reader.

This only makes the space. For footnotes or cross-references, choose **Side Margin** on the **Notes+Refs** tab. For headings, tick **In Margin** on the **Body** tab.

##### Margin Notes Column Width

Number · Regular+ · `s_marginNotesWidth` · cfg `paper/marginnoteswidth`, `document/marginnoteswidth`  
Needs: “Margin Notes Col Width (mm)”

> This is the width (mm) of the additional column which contains the Margin Notes (Footnotes, Cross-references and/or Section Headings).

Make it wide enough for a few short words per line. The main text becomes narrower by this amount.

##### Margin Notes on Left/Inner

Checkbox, off · Regular+ · `c_marginNotesInner` · cfg `document/marginnotesinner`  
Also: Place Margin Notes on Left/Inner edge of page · Needs: “Margin Notes Col Width (mm)”

> Margin Notes are normally placed on the Right/Outer edge of the page. But this can be changed for single column layouts to appear on the Left/Inner edge if needed. (Not available for two-column layouts.)

PTXprint unticks it when you switch to two columns.

#### Two Column Layout

##### Gutter Width (mm) – Gutter width for two column layout

Number · Basic+ · `s_colgutterfactor` · cfg `document/colgutterfactor`  
Values: 1–40 (default 4) · Needs: “Two Column Layout” · Greyed out by: “Lock UI Layout Settings”

> This is the space between the text of the two columns (measured in millimeters).
>
> This is the space (mm) between the text of the two columns.

A **Vertical Rule in Gutter** is drawn in the middle of this space. 3–6 mm is common.

##### Adjust Top (pt) – Adjust top of vertical rule

Number · Regular+ · `s_colgutteroffset` · cfg `paper/colgutteroffset`  
Values: -50–50 (default 3)

> This setting raises (using a negative value) or lowers (using a positive value) the starting point of the vertical rule between columns. (Value in pts).

Use it if the line starts too close to the header rule or too far from the first line of text. Greyed out unless **Two Column Layout** and **Vertical Rule in Gutter** are both ticked.

##### Thickness of Rule (pt) – Rule (line) Thickness

Number · Regular+ · `s_ruleThickness` · cfg `document/rulethickness`  
Values: 0.01–1 (default 0.4)

> This sets the thickness (pt) of rules (lines) in the document. This includes the horizontal rule between the header and the text, the vertical column gutter rule and the study notes inter-column rule.

Stays available in a one-column layout, because it also sets the header rule.

##### Vertical Rule in Gutter

Checkbox, on · Mini+ · `c_verticalrule` · cfg `paper/ifverticalrule`  
Needs: “Two Column Layout”

> Check this option to include a center line between the two columns.

Many Bibles use it.

##### Allow Unbalanced Columns

Checkbox, off · Basic+ · `c_allowUnbalanced` · cfg `paper/allowunbalanced`  
Needs: “Two Column Layout”

> Check this option to allow a different number of lines in each column. This is especially important when using Variable Line Spacing mode and you are trying to Fill Columns.
>
> To alter the maximum number of Unbalanced Lines at the end of a page, visit the Advanced page, select the Other tab, and expand the Page Layout and Spacing section.
>
> If this setting is highlighted in orange it means that the above-mentioned setting was set to 0 (rendering this setting inactive), and has now been increased to the default value of 3.

Very useful with **Variable Line Spacing**. The maximum difference is **Unbalanced Lines (Max)** on the **Advanced** tab, **Other** tab, **Page Layout and Spacing**.

#### Margins

##### Bottom of Header to Top of Text (pt) – Header spacing

Number · Regular+ · `s_headerposition` · cfg `paper/headerpos`  
Values: -20–99 (default 15) · Greyed out by: “Lock UI Layout Settings”

> This setting determines the vertical positioning of the header line by setting the amount of space between the header and the top of the text. (pts)
>
> The top of the main text area is 1 base line spacing above the base line of the first line of the body text.
>
> The space (pt) between the bottom of the header and the top of the main text area. Note that the first line actually starts a little bit below where the main text area starts.
>
> The top of the main text area is 1 base line spacing above the base line of the first line of the body text.

The header sits inside the top margin, so a bigger value moves it up towards the page edge. Watch the blue number in the diagram.

##### Bottom of Text to Top of Footer (pt) – Footer position

Number · Regular+ · `s_footerposition` · cfg `paper/footerpos`  
Greyed out by: “Lock UI Layout Settings”

> This setting can be used to increase/decrease the space between the end of the text and the footer line.
>
> The distance (pt) from the bottom of the text area to the TOP of the footer (including ascenders).

The footer normally sits inside the bottom margin, so a bigger value moves it down towards the page edge. Watch the blue number in the diagram.

##### Bottom of Text to End of Page (mm) – Bottom margin

Number · Basic+ · `s_bottommargin` · cfg `paper/bottommargin`  
Values: 0.5–99 (default 10.5) · Greyed out by: “Lock UI Layout Settings”

> The distance (mm) from the bottom of the main text area to the bottom of the page.
>
> The bottom of the main text area is calculated from the descender of the final line of text (including any footnotes).

The footer sits in this space (unless **Place Footer Text Above the Bottom Margin** is ticked). Changing it changes **Lines Per Page**.

##### Side Margin Width (mm) – Side margin width

Number · Basic+ · `s_margins` · cfg `paper/margins`  
Values: 0.5–200 (default 12) · Greyed out by: “Lock UI Layout Settings”

> The distance (mm) from the edge of the page to the start of the text area. Note that the left and right (or inner and outer) margins are set to be identical. If you require a greater inner margin, then set the Binding Gutter above.

10–15 mm is common.

##### Space between Rule and Top of Text (pt) – Space between horizontal rule and main text area

Number · Basic+ · `s_rhruleposition` · cfg `paper/rulegap`  
Values: -100–100 · Needs: “Horizontal Rule” · Greyed out by: “Lock UI Layout Settings”

> The space (pt) between the horizontal rule and the top of the main text area. Note that the first line actually starts a little bit below where the main text area starts.
>
> The top of the main text area is 1 base line spacing above the base line of the first line of the body text.

Shown by the green arrow in the margin diagram.

##### Start of Page to Top of Text (mm) – Top margin

Number · Basic+ · `s_topmargin` · cfg `paper/topmargin`  
Values: 0.5–200 (default 18) · Greyed out by: “Lock UI Layout Settings”

> The distance (mm) from the top of the page to the top of the main text area. Note that the first line actually starts a little bit below where the main text area starts.
>
> The top of the main text area is 1 base line spacing above the base line of the first line of the body text.

The header sits in this space. Changing it changes **Lines Per Page**.

##### Tweak top margin (auto adjust)

Button · Regular+ · `btn_adjust_top`  
Greyed out by: “Lock UI Layout Settings”

> Fine Tune Top Margin:
>
> This button is only active when PTXprint has a suggestion to shrink or expand the top margin slightly to minimise wasted vertical space on the page. Click to accept the suggestion.
>
> If there is more than half a line of 'spare' space on the page then the top margin will decrease slightly to fit one more line of text on the page.
>
> If there is less than half a line of 'spare' space on the page then the top margin will increase slightly to fill the page more evenly (with the same number of lines of text).
>
> If you prefer to keep the exact top margin specified, then do NOT click this option. Instead, use the similar button to adjust either the Line Spacing or Bottom Margin.

Only active when **Lines Per Page** is red. Use it to keep line spacing and font size exactly as they are.

##### Tweak bottom margin (auto adjust)

Button · Regular+ · `btn_adjust_bottom`  
Greyed out by: “Lock UI Layout Settings”

> Fine Tune Bottom Margin:
>
> This button is only active when PTXprint has a suggestion to shrink or expand the bottom margin slightly to minimise wasted vertical space on the page. Click to accept the suggestion.
>
> If there is more than half a line of 'spare' space on the page then the bottom margin will decrease slightly to fit one more line of text on the page.
>
> If there is less than half a line of 'spare' space on the page then the bottom margin will increase slightly to fill the page more evenly (with the same number of lines of text).
>
> If you prefer to keep the exact bottom margin specified, then do NOT click this option. Instead, use the similar button to adjust either the Line Spacing or Top Margin.

Only active when **Lines Per Page** is red. Use it to keep line spacing, font size and top margin exactly as they are.

##### Place Footer Text Above the Bottom Margin

Checkbox, off · Regular+ · `c_noinkinmargin` · cfg `footer/noinkinmargin`  
Also: Don't place footer in the margin area · Greyed out by: “Lock UI Layout Settings”

> Normally the footer page number sits in the bottom margin.
>
> However if you need the page number to be placed above the bottom margin (where the text would normally flow until) then enable this option.

Use it when the printer needs the whole margin empty. The text area becomes a little shorter.

##### 8.5mm

Label · Regular+ · `l_footer2edge`  
Greyed out by: “Lock UI Layout Settings”

> The distance (mm) from the edge of the page to the bottom of the footer area.

Calculated; you cannot type in it. Shown by the blue arrow at the bottom of the diagram. If it is very small, the footer may be cut off when the pages are trimmed.

##### Horizontal Rule

Checkbox, off · Basic+ · `c_rhrule` · cfg `header/ifrhrule`  
Greyed out by: “Lock UI Layout Settings”

> Check this option to add a horizontal line under the page header, before the main body text begins.

Set its position with **Space between Rule and Top of Text (pt)** and its thickness with **Thickness of Rule (pt)**.

##### 8.5mm

Label · Regular+ · `l_margin2header`  
Greyed out by: “Lock UI Layout Settings”

> The distance (mm) from the top of the page to the top of the header area. Note that due to the ascent of the font, the header text actually starts a little bit below the top of the header area.

Calculated; you cannot type in it. Shown by the blue arrow at the top of the diagram. If it is very small or negative, make the top margin larger or the header gap smaller.


# 6. Fonts+Script tab

## 6.1 What this tab is for

The **Fonts+Script** tab controls *how the letters look* and *how the writing system behaves*: the fonts, the script (writing system), the writing direction, hyphenation and spacing.

Come here when you start a new publication, when some characters print as empty boxes, when your language uses a non-Latin script (for example Arabic, Devanagari, Myanmar, Thai or Chinese), or when you need to hyphenate long words.

Some words used in this chapter:

* **Font** – a set of letter shapes, for example *Charis SIL* or *Gentium Plus*.
* **Typeface** (or face) – one style of a font: Regular, Bold, Italic or Bold Italic.
* **Script** – a writing system, for example Latin, Arabic, Devanagari, Myanmar or Han (Chinese).
* **Glyph** – the shape the font draws for a character.
* **Font feature** – an option built into a font, for example a different shape for one letter, or different digits.
* **Tofu** – the empty box ☐ printed when the font has no shape for a character.
* **Hyphenation** – breaking a long word at the end of a line and continuing it on the next line.
* **pt (point)** – a small unit used for type. 1 pt is about 0.35 mm.

If the whole tab is greyed out, **Lock UI Layout Settings** is ticked on the **Advanced** tab (see the **Layout tab** chapter).

## 6.2 Font Configuration

PTXprint uses four fonts for the main text: **Regular**, **Bold**, **Italic** and **Bold Italic**. Each has a **Select Font...** button that shows the font now in use.

* Choose the **Regular** font first. Each time you click **OK** in the **Pick a Font** dialog for **Regular**, PTXprint fills in **Bold**, **Italic** and **Bold Italic** from the same family, with the same features and options. So choose a different bold or italic font only *after* you have finished with Regular.
* If the family has no bold or italic typeface, PTXprint *fakes* it (makes the letters thicker or slanted). The button then shows the style in brackets, for example *(bold)*. Faked styles are usable, but a real typeface looks better.
* If your Paratext project's language settings name font features for this font, PTXprint uses them when you choose it (unless you have already set features).
* Only the **Regular** button is shown in the **Mini** view. The other three are shown from the **Basic** view upwards.

Click **Refresh Font List** if a newly installed font is not in the list.

**Enable Colored Text (as Specified in Stylesheet)** prints text in colour where a style asks for it (for example red letters for the words of Jesus). If it is not ticked, all text is black.

**Script for Numbers** is a link that opens the **Pick a Font** dialog with **Digit mapping** highlighted (see below).

## 6.3 Pick a Font (and Typeface) dialog

This dialog opens when you click any **Select Font...** button.

1. Type part of the font name in the search box.
2. Click a font in the list. Fonts shown in **bold** have all four typefaces.
3. Choose the **Typeface**.
4. Change other options if needed, then click **OK**.

If a font is missing from the list, it may not be installed for all users. Install it, then click **Refresh Font List** on the **Fonts+Script** tab.

The other options are:

* **Fake Bold/Italic** – make bold and/or italic from the regular typeface. **Embolden** sets how much thicker; **Slant** sets how much the letters lean (0.15 is a normal italic slant; negative leans the other way).
* **Stretch** – make all letters wider (above 1.00) or narrower (below 1.00). 0.95 makes text 5% narrower, so more fits on a line. Use small changes only; the letter shapes become distorted.
* **Graphite Rendering** – use SIL's Graphite technology. Tick it only for fonts made for Graphite that need it (the font's documentation says so). Ticking or unticking it clears the font features.
* **Contextual Spaces** – tick only if the font itself changes the width of spaces depending on the letters around them. When ticked for the Regular font, **Between Letters** spacing is not used.
* **Font features** (text box) and **Select Features...** – turn special options in the font on or off.
* **Digit mapping** – print numbers in another script's digits.

### Digit mapping (numbers in your own script)

Many scripts have their own digits, for example Arabic-Indic ٠١٢٣, Devanagari ०१२३, Myanmar ၀၁၂၃ or Thai ๐๑๒๓. If your text uses the Western digits 0–9 but you want your script's digits, choose your script in **Digit mapping**. PTXprint then changes the digits when it prints, for numbers in that font (for example chapter and verse numbers).

* Check that your font has these digits. If not, you will see empty boxes.
* When you change **Text Script**, PTXprint also tries to choose the matching digit mapping. Check it.
* If your text already contains your script's digits, leave **Digit mapping** on **Default**.

### Select Font Features dialog

**Select Features...** lists the selected font's features as tick boxes and drop-down lists. Hover over a feature name to see a short description (when the font gives one).

* **Language** – choose a language the font knows. Some fonts use different letter shapes for different languages. Choosing one sets the features to that language's defaults.
* With **Graphite Rendering** ticked you see the font's Graphite features; otherwise its OpenType features.
* **OK** writes your choices into the font features text box, for example `language=ur, cv12=1`. Only features you changed from the default are written.

Choosing a different font in the list clears the font features.

## 6.4 Use Fallback Font

Some fonts do not contain every character in your text, for example special quotation marks or the glossary markers. These print as empty boxes (tofu). A *fallback font* is a second font used only for those characters.

1. Tick **Use Fallback Font**.
2. Click **Find Missing Characters**. PTXprint checks the books selected on the **Basic** tab against the Regular font and lists the missing characters. Select as many books as possible first. If nothing is missing, PTXprint tells you and unticks **Use Fallback Font**.
3. Click **Select Font...** next to the list and choose a font that has these characters. If the label turns **red**, that font lacks some of them too; choose another.

You can add characters to the list by hand, separated by spaces. You can type a character code as `\u` plus four hex digits, for example `\u2E24`. Straight and curly quotation marks (‘ ’ “ ”) and `*`, `#` and `%` are ignored by the fallback font.

These settings are shown in the **Regular** and **Full** views.

## 6.5 Writing System

This area tells PTXprint how your script works. It is very important for non-Latin scripts.

### Text Flow Direction

* **Left-to-Right** – for example Latin, Cyrillic, Devanagari, Ethiopic, Thai and Myanmar.
* **Right-to-Left** – for example Arabic, Hebrew, Syriac and Thaana. This also ticks **RTL Book Binding**.
* **Top-to-Bottom (and Left-to-Right)** – vertical text, with the lines going from left to right.

### RTL Book Binding

A right-to-left book is bound on the right and opens from the "back" (as seen by a left-to-right reader). Tick **RTL Book Binding** so that the binding gutter, the page order in PDF viewers and the cover are correct for such a book.

### Text Script

**Text Script** tells the font which script rules to use. These rules join letters (for example in Arabic), place vowel marks and other marks, and reorder letters where needed (for example in Indic scripts).

* If **Text Script** is **Default** when a project is opened, PTXprint tries to detect the script. Check that it is right.
* The right script also switches on extra processing that PTXprint has for some scripts (see below).
* For most Latin-script languages, leave it on **Default** or **Latin**.

### Additional Script Settings...

This button opens a small dialog with extra options for some scripts:

* **Myanmar (Burmese)** – **Syllable line breaking**: break lines between syllables, not only at spaces.
* **Malayalam, Tamil, Sinhala, Telugu, Kannada, Oriya** – **Syllable line breaking**: break long words between syllables. **Show Hyphen**: print a hyphen where a word is broken (if not ticked, the break is invisible).
* **Arabic** – **First verse on left**: how verse references are written.
* **Han (Simplified)** and **Han (Traditional)** – **Enabling horizontal gridding**: align chapter numbers with the character grid and remove spaces before verses. **Automatic halfwidth punctuation pairs**: two punctuation marks together share the width of one full character.

### Scripts that do not use spaces between words

Some scripts (for example Thai, Lao, Khmer, Myanmar, Tai Tham, New Tai Lue, Chinese and Japanese) do not put spaces between words. PTXprint must know where it may break a line. There are two ways:

* **Mark break points in the text with "/".** For Thai, Lao, Myanmar, Tai Tham (Lanna) and New Tai Lue, when **Text Script** is set to that script, each `/` becomes an invisible break point. The `/` is not printed.
* **Use a line-break dictionary.** Tick **Specify Line Break Locale** and type a code: `th` (Thai), `km` (Khmer), `my` (Myanmar), `zh` (Chinese), `ja` (Japanese), `ko` (Korean), or `gr` for the line-breaking rules inside a Graphite font. Choosing a Han, Japanese or Korean script in **Text Script** fills this in for you.

These options are shown in the **Regular** and **Full** views.

## 6.6 Hyphenation

PTXprint can hyphenate using your Paratext project's hyphenation list. In Paratext, the Wordlist tool suggests where words can be broken, and you approve the suggestions. PTXprint turns that list into one it can use.

1. Click **Create List...**. The **Create List** dialog opens.
2. Choose the options (see below) and click **OK**. A message says how many words were used.
3. Tick **Hyphenate**.
4. Click **Print**.

Create the list again only when the Paratext hyphenation list changes.

Ticking **Hyphenate** unticks **Between Letters** in **Spacing Adjustments**, because letter spacing stops hyphenation from working well. The status bar tells you this.

**Omit '-'Hyphen** makes the hyphen invisible, for scripts that break words but show no hyphen.

**Make Hyphens Non-Breaking** stops lines breaking at hyphens already in the text. Create the hyphenation list again after you change this.

### Create List dialog (hyphenation)

* **Only Use Approved Hyphenation Words** (ticked by default) – use only words whose break points you approved in Paratext. Untick it to include Paratext's unchecked guesses. If the list comes out empty, try unticking this.
* **Limit Hyphenation List to Words Found in** – use only words in the books you are printing (listed beside it). Use it when the full list is too long.
* **Add Syllable-Based Hyphenated Words** – only for scripts where **Syllable line breaking** is ticked in **Additional Script Settings...**. Adds break points for more words using the syllable rules.
* **Advanced** – limits on which words are added: **Minimum affix**, **Minimum length** and **Min non-hyphen**.

## 6.7 Spacing Adjustments

When text is justified (both edges straight), PTXprint stretches or shrinks the spaces in each line. This area controls how much.

* **Between Words** – the smallest (**Min/Shrink**) and largest (**Max/Stretch**) space between words, as a percentage of a normal space. A lower minimum fits more words on a line. A higher maximum lets lines stretch more. Too low makes words hard to separate; too high leaves big gaps ("rivers" of white space).
* **Between Letters** – also lets PTXprint add or remove a very small amount of space between letters, as a percentage of the font size. Keep the numbers small. Use it only when really needed: it can make text look uneven and stops hyphenation from working well.

**Between Letters** is greyed out when **Interlinear & Code** is ticked on the **Advanced** tab. It is not used when **Contextual Spaces** is ticked for the Regular font, and it is unticked when you tick **Hyphenate**.

These settings are shown in the **Regular** and **Full** views.

## 6.8 Add Tatweel (kashida) Rules dialog

In Arabic script, a *tatweel* (also *kashida*, the character ـ) is a joining stroke that makes a word longer, to make lines look better or to fill a line. This dialog writes a *change rule* that adds tatweels to one word at one verse. The rule goes into the project's changes file (changes.txt), which PTXprint applies every time it prints.

To open it (advanced): on the **View+Edit** tab, open the changes file. In the **Code Snippets** area at the side, click **Arabic**, then **Add Tatweels**.

1. In Paratext (or anywhere), copy the word or short phrase to lengthen (up to 60 characters). The dialog fills in **Word / Phrase** from the clipboard. On Windows, it also fills in **Reference** from the current Paratext reference.
2. Check the **Reference**.
3. Set **Tatweels to insert**.
4. Click in **Word / Phrase** where the tatweels should go and press **Ctrl+`** (Ctrl and the grave-accent key). Repeat for other places.
5. Check the rule in **The rule to be added to Changes.txt**. It looks like `at REF 'original' > 'new'`.
6. Click **Insert Rule**. The rule is added at the cursor in the file open on the **View+Edit** tab.
7. Save the file and click **Print**.

## 6.9 Common tasks

### How do I change the main font?

1. On the **Fonts+Script** tab, **Font Configuration**, click **Select Font...** next to **Regular**.
2. Type part of the font name, click the font, and click **OK**.
3. Check the **Bold**, **Italic** and **Bold Italic** buttons. A style in brackets will be faked.
4. Click **Print**.

### How do I get rid of empty boxes (tofu) in the printed text?

1. Select all the books on the **Basic** tab.
2. Follow the steps in **Use Fallback Font** above.
3. Click **Print**.

### How do I print numbers in my own script's digits?

1. On the **Fonts+Script** tab, click the **Script for Numbers** link (or **Select Font...** for **Regular**).
2. Choose your script in **Digit mapping**.
3. Click **OK**, then **Print**. Check that the font has those digits.

### How do I set up a right-to-left script (for example Arabic or Hebrew)?

1. On the **Fonts+Script** tab, choose a font made for your script.
2. In **Writing System**, set **Text Flow Direction** to **Right-to-Left**. **RTL Book Binding** is ticked for you.
3. Set **Text Script** to your script (for example **Arabic** or **Hebrew**).
4. If your font needs Graphite (for example some Nastaliq fonts), open **Select Font...**, tick **Graphite Rendering** and click **OK**.
5. Click **Print**.

### How do I set up a script that has no spaces between words?

1. On the **Fonts+Script** tab, set **Text Script** to your script.
2. If your text marks word breaks with `/` (Thai, Lao, Myanmar, Tai Tham, New Tai Lue), nothing more is needed.
3. Otherwise, tick **Specify Line Break Locale** and type the code (for example `th`, `km`, `my`, `zh`, `ja` or `ko`).
4. For Myanmar or Indic scripts, consider **Syllable line breaking** in **Additional Script Settings...**.
5. Click **Print**.

### How do I turn on hyphenation?

1. Make sure hyphenation points have been approved in the Paratext Wordlist.
2. Follow the steps in **Hyphenation** above.

### How do I choose a different form of a letter that the font offers?

1. Click **Select Font...** for **Regular**, then **Select Features...**.
2. Choose your language in **Language** (if listed), then tick or choose the feature.
3. Click **OK** in both dialogs, then **Print**. PTXprint copies the Regular font's features to the Bold, Italic and Bold Italic fonts.

### How do I fit more text on each line?

1. In **Spacing Adjustments**, make **Min/Shrink** (Between Words) a little smaller.
2. Or, in the **Pick a Font** dialog, set **Stretch** slightly below 1.00 (for example 0.97).
3. Click **Print** and check that the text is still easy to read.

## 6.10 Common problems

### The whole Fonts+Script tab is greyed out

**Cause:** **Lock UI Layout Settings** is ticked on the **Advanced** tab.

**What to do:** Change to the **Full** view. On the **Advanced** tab, **Main** tab, **General** area, untick **Lock UI Layout Settings**.

### Some characters print as empty boxes

**Cause:** The Regular font does not contain those characters.

**What to do:** Use **Use Fallback Font** and **Find Missing Characters**, or choose a Regular font that supports your whole character set.

### My font is not in the list

**Cause:** The font is not installed, was installed only for one user, or the list has not been refreshed.

**What to do:** Install the font for all users, then click **Refresh Font List**.

### Bold or italic looks thick, blurred or slanted wrongly

**Cause:** The font has no real bold or italic, so PTXprint fakes it (the style is in brackets on the button).

**What to do:** Choose a family with real bold and italic typefaces, or change **Embolden** and **Slant** in the **Pick a Font** dialog.

### Letters do not join, or marks are in the wrong place

**Cause:** **Text Script** may be wrong, or the font needs Graphite rendering.

**What to do:** Set **Text Script** to your script. For a Graphite font, tick **Graphite Rendering** in the **Pick a Font** dialog.

### Additional Script Settings... is greyed out

**Cause:** The script in **Text Script** has no extra options.

### Long lines do not break in Thai, Khmer, Myanmar, Chinese and similar scripts

**Cause:** PTXprint does not know where it may break the line.

**What to do:** Set **Text Script**, and either mark breaks with `/` (Thai, Lao, Myanmar, Tai Tham, New Tai Lue) or tick **Specify Line Break Locale** and type the language code.

### Hyphenation does not work

* No list was created. Click **Create List...** first.
* The list is empty because no words are approved in Paratext. Untick **Only Use Approved Hyphenation Words** and create the list again, or approve words in Paratext.
* **Between Letters** is ticked. Untick it.
* **Hyphenate** is not ticked.

### Between Letters is greyed out

**Cause:** **Interlinear & Code** is ticked on the **Advanced** tab. The two cannot be used together.

### Font features I set have disappeared

**Cause:** Choosing another font, or ticking or unticking **Graphite Rendering**, clears the features.

**What to do:** Set the features again after choosing the font and the Graphite option.

### Numbers print as boxes after choosing a digit mapping

**Cause:** The font does not have the digits for that script.

**What to do:** Choose a font that has these digits, or set **Digit mapping** back to **Default**.

### Text is printed in black even though styles have colours

**Cause:** **Enable Colored Text (as Specified in Stylesheet)** is not ticked.

## 6.11 Settings reference

### Create List (dialog)

#### OK

Button · Regular+ · `btn_gnr8pl_ok1`

Creates the list and shows how many words were used. Read the message: it tells you if the list was empty or had to be shortened.

#### Cancel

Button · Regular+ · `btn_gnr8pl_cancel1`

Closes the dialog without creating a list.

#### When Creating Hyphenation List

##### Add Syllable-Based Hyphenated Words

Checkbox, off · Regular+ · `c_addSyllableBasedHyphens` · cfg `paragraph/ifsylhyphens`  
Also: Append syllable-based hyphenated words to hyphen list

> This advanced hybrid option is only available if Syllable Line Breaking has been enabled under Additional Script Settings for Complex Scripts.
>
> If enabled, it will use Syllable Line Breaking to hyphenate words from the books selected so that a combination of manually-marked hyphenation along with automated hyphenation is possible.

Syllable line breaking is available for Myanmar and some Indic scripts. Use this when Paratext's list covers only some words.

##### Limit Hyphenation List to Words Found in

Checkbox, off · Regular+ · `c_hyphenLimitBooks` · cfg `paragraph/ifhyphlimitbks`  
Also: Limit hyphenation list to only include words in active books

> Normally ALL hyphenated words from ALL books are included in PTXprint's hyphenated wordlist.
>
> However, if the list of hyphenated words is too long (greater than 63929 words) then you can prioritize which words to include by enabling this option to only use words from the books being printed.
>
> Note that if there are too many words in the Paratext hyphenation file, PTXprint will automatically prioritize the list created for XeTeX based on frequency.

The books are listed beside this option.

##### Only Use Approved Hyphenation Words

Checkbox, on · Regular+ · `c_hyphenApprovedWords` · cfg `paragraph/ifhyphapproved`  
Also: Only use words where hyphenation points have been approved in Paratext

> The Paratext WordList tool guesses hyphenation points based on syllable structure and patterns in the language.
>
> However, it expects the user to (i) check and, if appropriate, (ii) approve the suggested hyphenation points (by clicking the check mark making it appear green).
>
> Normally only the approved hyphenated words will be used when creating the hyphenation list for PTXprint/TeX to use.
>
> However, if you wish to include ALL words (regardless of their approval status) then disable this option.

The safe choice. If you untick it, check the printed result carefully.

##### Advanced

###### Minimum affix

Number · Regular+ · `s_hyphMinprefix`  
Values: 1–10 (default 3)

> Do not add any words to the hyphenation list that include an optional hyphen less than this number of characters at the beginning or end of the word.

Stops very short pieces (one or two letters) being left at the end of a line or carried to the next. The default of 3 is usually good.

###### Minimum length

Number · Regular+ · `s_hyphMinWord`  
Values: 3–50 (default 7)

> The minimum word length (including optional hyphens) that will be added to the hyphenation list.

Only words longer than this are added. Short words rarely need to be broken.

###### Min non-hyphen

Number · Regular+ · `s_hyphMinBlock`  
Values: 1–50 (default 9)

> Minimum word length for a word to block hyphenation.

PTXprint counts long words that have no break points, but at present this number does not change the list created. Leave it at the default.

### Add Tatweel (kashida) Rules (dialog)

#### Insert Rule

Button · Regular+ · `btn_tatweel_insertRule`

Inserts the rule at the cursor in the file open on the **View+Edit** tab. Make sure that file is the changes file, and save it afterwards.

#### Close

Button · Regular+ · `btn_tatweel_close`

Closes the dialog and stops it watching the clipboard.

#### Reference – Tatweel Dialog: Enter reference

Text box · Regular+ · `t_tatweelRef`

> Enter the verse reference where the word is located.
>
> (Note that the reference is automatically updated from the current Paratext reference.)

For example `GEN 1:1`. On Windows it updates each time you copy a new word. The rule only changes the word at this reference.

#### Word / Phrase – Tatweel Dialog: Enter word or phrase to be lengthened

Text box · Regular+ · `t_tatweelText`

> Enter the word to be lengthened and place the cursor at the location and use shortcut Ctrl-` (Ctrl-grave) to insert Tatweels. Repeat at other words and/or locations.
>
> (Note that this box is automatically updated from the clipboard if the word/phrase is 60 characters or less).

The "before" part of the rule is the text you copied, so copy the exact word from the text; do not just type it here.

#### Tatweels to insert – Tatweel Dialog: Number of Tatweels to insert

Number · Regular+ · `s_tatweelLength`  
Values: 1–20

> How many Tatweels should be inserted at the current cursor location?

Applies each time you press **Ctrl+`**. Start with 1 or 2 and check the printed result.

#### The rule to be added to Changes.txt

Text box · Regular+ · `t_tatweelPreview`

> The rule to be added to Changes.txt

Form: `at REF 'original' > 'new'`. Check it before you click **Insert Rule**.

### Pick a Font (and Typeface) (dialog)

#### OK

Button · Regular+ · `btn_font_ok`

Uses the selected font, typeface and options for the button you clicked.

#### Cancel

Button · Regular+ · `btn_font_cancel`

Closes the dialog without changing the font.

#### Choose a font from the installed fonts. Fonts shown in BOLD ...

Table · Mini+ · `tv_fontFamily`

> Choose a font from the installed fonts. Fonts shown in BOLD have all 4 typefaces.
>
> If you cannot locate the desired font in this list, then it is quite likely that it has not been installed "For all Users" in the Windows system.

Choosing a different font clears the font features.

#### Typeface – Font Selection Dialog: Typeface

Drop-down · Mini+ · `fcb_fontFaces`  
Choices: Regular | Bold | Italic | Bold Italic

> Fonts which have all 4 typefaces (regular, bold, italic, and bold-italic) are shown in BOLD in the list above.
>
> If you cannot locate the desired font in this list, then it is quite likely that it has not been installed "For all Users" in the Windows system.

Normally **Regular** for the Regular button, **Bold** for the Bold button, and so on. Some fonts also offer faces such as Light or Semibold.

#### Font Selection Dialog: Find a font

Search box · Mini+ · `t_fontSearch`

> Type the start of a font name to jump to it in the list.

Part of the name is enough.

#### Fake Bold/Italic

Checkbox, off · Basic+ · `c_fontFake`  
Also: Font Selection Dialog: Fake bold or italic typeface

> If the font you are using doesn't have multiple typefaces (such as Bold, Italic and Bold-Italic) then you can "fake" these by adding boldness and/or slant to the regular typeface.

Use it only when the font has no real bold or italic. PTXprint also fakes missing styles automatically; the font button then shows the style in brackets.

#### Stretch – Font Selection Dialog: Stretch (or shrink) font setting

Number · Regular+ · `s_fontExtend`  
Values: 0.5–2 (default 1)

> The shapes of the characters can be stretched (larger) or condensed (smaller) to occupy more horizontal space, or less (shrink text).  
> 1.00 = 100% = normal  
> 0.95 =   95% = shrink text  
> 1.05 = 105% = expand text

Small changes (0.95–1.05) can help fit text; large changes distort the letters. A value set for the Regular font is copied to Bold, Italic and Bold Italic.

#### Font Selection Dialog: Selected font features

Text box · Regular+ · `t_fontFeatures`

> You can enable/disable any font features for the selected font. For example:  
> smcp=1, cv12=2 Use 'Select Features...' to choose them from a list.

May also contain `language=xx`. The easy way to fill it is **Select Features...**. It is cleared when you choose a different font or change **Graphite Rendering**.

#### Contextual Spaces

Checkbox, off · Regular+ · `c_fontCtxtSpaces`  
Also: Font Selection Dialog: Use contextual spaces

> Set this option if the font changes the width of spaces depending on the text around them.

Tick only if the font's documentation says so. When ticked for the Regular font, PTXprint switches off **Between Letters** spacing.

#### Graphite Rendering

Checkbox, off · Regular+ · `c_fontGraphite`  
Also: Font Selection Dialog: Use Graphite rendering

> If you require this font to use SIL's Graphite Rendering technology, then enable this.
>
> Changing this clears the font features.

Replaces the normal (OpenType) rendering. Some complex-script fonts work best, or only, with Graphite. When ticked, **Select Features...** shows Graphite features.

#### Select Features...

Button · Regular+ · `btn_fontFeatures`  
Also: Font Selection Dialog: Select font features

> Choose font features (and the language) from a list of those this font supports.

Works on the font selected in the list. Shows Graphite features if **Graphite Rendering** is ticked, otherwise OpenType features.

#### Digit mapping – Font Selection Dialog: Digit (number) script mapping

Drop-down · Regular+ · `fcb_fontdigits`  
Choices: Default | Arabic-Hindi | Arabic-Farsi | Burmese

> All known unicode-encoded number/digit systems are catered for. So if you don't want to use the Latin/Arabic numbers [0-9], you can pick the appropriate script here. (Make sure the font you are using supports these digits too.)

For example Arabic-Indic, Devanagari, Myanmar or Thai. Use it when the text contains 0–9 but the publication should show your script's digits. Leave it on **Default** if the text already has the right digits. The list holds many more scripts than the four shown above.

#### Fake Bold/Italic

##### Embolden – Font Selection Dialog: Fake bold setting

Number · Basic+ · `s_fontBold`  
Needs: “Fake Bold/Italic”

> If the required font doesn't have a BOLD typeface, you can use this setting to create the BOLD effect. (For example, setting Embolden to 1.6 would thicken the Regular typeface making it appear as bold.)

Larger numbers give thicker letters. Check the result in print: too much makes letters fill in.

##### Slant – Font Selection Dialog: Fake italic setting

Number · Basic+ · `s_fontItalic`  
Values: -1–1 (default 0.15) · Needs: “Fake Bold/Italic”

> If the required font does not have an ITALIC typeface, you can use this setting to create the ITALIC effect. (For example, setting Slant to 0.15 would slant the Regular typeface by 15% making it appear as italic.)

A negative value leans the letters the other way. 0 means no slant.

### Select Font Features... (dialog)

#### OK

Button · Regular+ · `btn_feats_ok`

Writes the changed features into the font features box of the **Pick a Font** dialog. Only features that differ from the default are written.

#### Cancel

Button · Regular+ · `btn_feats_cancel`

Closes the dialog without changing the features.

#### Language

Drop-down · Regular+ · `fcb_featsLangs`

> Choose the language the font should use. Some fonts change letter shapes for particular languages.

Choosing a language also sets the features to that language's defaults.

### Fonts+Script

#### Use Fallback Font

Checkbox, off · Regular+ · `c_useFallbackFont` · cfg `paragraph/ifusefallback`  
Greyed out by: “Lock UI Layout Settings”

> This setting is used to prevent "tofu" boxes [] in the printed text. If the primary font is missing any special characters (for example curly quotes), then an alternative "fallback" font can be used to ensure that they are displayed properly.

Then use **Find Missing Characters** and choose a fallback font. **Find Missing Characters** ticks or unticks this automatically.

#### Font Configuration

##### Select Font...

Button · Mini+ · `bl_fontR` · cfg `document/fontregular`  
Also: Select Regular font · Greyed out by: “Lock UI Layout Settings”

> Click to select the main font for the publication. Note that the font chooser dialog also has a number of other options for setting advanced font features and, if needed, Graphite rendering.

Choose it first. Each time you click **OK** for it, PTXprint fills in Bold, Italic and Bold Italic from the same family with the same features, replacing any you chose by hand. All styles that do not name their own font use this font. Font features listed in your Paratext language settings are used too.

##### Select Font...

Button · Basic+ · `bl_fontB` · cfg `document/fontbold`  
Also: Select Bold font · Greyed out by: “Lock UI Layout Settings”

> If you see the style in parentheses (bold) this indicates that PTXprint could not locate the bold style and will fake the style.

Filled in automatically when you choose the Regular font.

##### Select Font...

Button · Basic+ · `bl_fontI` · cfg `document/fontitalic`  
Also: Select Italic font · Greyed out by: “Lock UI Layout Settings”

> If you see the style in parentheses (italic) this indicates that PTXprint could not locate the italic style and will fake the style.

Filled in automatically when you choose the Regular font.

##### Select Font...

Button · Basic+ · `bl_fontBI` · cfg `document/fontbolditalic`  
Also: Select Bold Italic font · Greyed out by: “Lock UI Layout Settings”

> If you see either of the styles in parentheses (bold) or (italic) this indicates that PTXprint could not locate the style and will fake the bold-italic style.

Filled in automatically when you choose the Regular font.

##### Refresh Font List button

Button · Regular+ · `btn_refreshFonts`  
Greyed out by: “Lock UI Layout Settings”

> Refresh Font List:  
> If you have recently installed a font but it doesn't show in the font list, then try clicking this button to refresh the list.
>
> If it still doesn't show up, then try re-installing the font (in Windows, locate the font file, then right-click on it and select "Install For All Users").
>
> And remember to Refresh the Font List again.

Reloads the font list from the computer.

##### Enable Colored Text (as Specified in Stylesheet)

Checkbox, off · Regular+ · `c_colorfonts` · cfg `document/ifcolorfonts`  
Greyed out by: “Lock UI Layout Settings”

> The marker specifications in stylesheets also include the \Color parameter. If this option is checked, then these settings will be used to produce colored text output. For example the \wj Words of Jesus\wj* marker might specify \Color Red which will only take effect if this option is also enabled - otherwise all text will appear in black.

Also covers coloured headings or any other colour set in the styles. Check with your printer whether colour printing is possible and what it costs.

##### Script for Numbers

Link · Regular+ · `lb_NumberScript`  
Greyed out by: “Lock UI Layout Settings”

> To change the script for numbers, click here to locate the Digit Mapping setting at the end of the Font selection dialog.

Opens the dialog for the Regular font.

#### Use Fallback Font

##### Find Missing Characters

Button · Regular+ · `btn_findMissingChars`  
Also: Find Missing Characters button · Needs: “Use Fallback Font” · Greyed out by: “Lock UI Layout Settings”

> If the primary font is missing any characters (special punctuation, quotes or glossary markers), then these can be listed here, and handled using the Font specified below.
>
> It is recommended that you select as many scripture books as available before using this tool to find missing characters.
>
> Note that the following characters are reserved and are ignored by the Fallback font functionality:  
>            \u2018 \u2019 \u201c \u201d * # %

Digits and markers are not checked. If characters are missing, **Use Fallback Font** is ticked; if not, PTXprint says a fallback font is not needed and unticks it. Hover over the list afterwards to see the character codes.

##### Select Font...

Button · Regular+ · `bl_fontExtraR` · cfg `document/fontextraregular`  
Also: Select font to display missing characters · Needs: “Use Fallback Font” · Greyed out by: “Lock UI Layout Settings”

> Click to select a font to be used as a substitute or "fallback" for the characters listed above which are not in the Regular font.
>
> Select a font to be used as a substitute or "fallback" for the characters listed above which are not in the Regular font.
>
> Note that if the label text is RED, it means that the font currently selected doesn't have all the missing characters either, so it is wise to choose another font.

It must be a different font from the Regular font.

##### Missing Characters

Text box · Regular+ · `t_missingChars` · cfg `paragraph/missingchars`  
Needs: “Use Fallback Font” · Greyed out by: “Lock UI Layout Settings”

> First use the button (on the left) to find any characters missing from the primary font. You may add to this list if needed. Use spaces between items. Note that you can also use \u0ABC codes to enter hard-to-type characters.

Codes can be typed like `\u2E24`. Quotation marks (‘ ’ “ ”) and `*`, `#`, `%` are ignored.

#### Hyphenation

##### Hyphenate

Checkbox, off · Regular+ · `c_hyphenate` · cfg `paragraph/ifhyphenate`, `paragraph/ifnothyphenate`  
Greyed out by: “Lock UI Layout Settings”

> To hyphenate properly you need to first create a Hyphenation List using the 'Create List...' button. This will create a XeTeX hyphenation list from the hyphenation list in Paratext.
>
> Note that for Hyphenation to work properly, the Spacing Adjustments 'Between Letters' option needs to be disabled.

Create the list first. Ticking it unticks **Between Letters** spacing. When unticked, PTXprint does not hyphenate at all.

##### Create List...

Button · Regular+ · `btn_generateHyphenationList`  
Also: Create Hyphenation List · Greyed out by: “Lock UI Layout Settings”

> Click this button to generate a hyphenation list that can be used by XeTeX to optimize hyphenation. This will read Paratext's HyphenatedWords.txt list and create a TeX hyphen list for this language.

Opens the **Create List** dialog. Do this again when the Paratext list changes.

##### Omit '-'Hyphen

Checkbox, off · Regular+ · `c_omitHyphen` · cfg `paragraph/ifomithyphen`  
Also: Omit hyphen from hyphenated words · Greyed out by: “Lock UI Layout Settings”

> Some scripts use hyphenation to break long words onto the next line, BUT don't need to display the actual '-' character. If this option is checked, then "hyphens" will be invisible.

Makes the hyphen at a line break invisible.

##### Make Hyphens Non-Breaking

Checkbox, off · Regular+ · `c_nonBreakingHyphens` · cfg `paragraph/ifnbhyphens`  
Greyed out by: “Lock UI Layout Settings”

> Enable this option to ensure that word-medial hyphens within the text never break across two lines.
>
> By default, lines may break at word-medial hyphens.
>
> If enabled, lines will not break at these hyphens.

Create the hyphenation list again after changing this, because the list is made with the chosen kind of hyphen.

#### Spacing Adjustments

##### Between Words

Checkbox, on · Regular+ · `c_spacing` · cfg `document/ifspacing`  
Also: Spacing Between Words · Greyed out by: “Lock UI Layout Settings”

> The horizontal distance that the space character can use between words is adjustable - and allows a greater degree of flexibility when trying to shrink or grow paragrahs when balancing pages.

Uses the **Min/Shrink** and **Max/Stretch** values. When unticked, standard values are used.

##### Between Letters

Checkbox, on · Regular+ · `c_letterSpacing` · cfg `document/ifletter`, `document/letterspace`  
Also: Spacing Between Letters · Greyed out by: “Interlinear  &  Code”, “Lock UI Layout Settings”

> Enabling letter spacing allows the spaces between characters to be adjusted (usually by a very small percentage). This might help alleviate space problems. Values are in percentage of the text point size and get used everywhere.
>
> Warning: Only use this if really needed! In some cases, enabling this setting will prevent hyphenation from working at all. In other cases it can make the text look very ugly.
>
> Note that if this option is disabled, then it is due to the Interlinear option being set on the Advanced page. These two settings are mutually exclusive.
>
> Letter spacing is also not used if 'Contextual Spaces' is set for the Regular font.

Use it only when needed. PTXprint unticks it when you tick **Hyphenate**.

##### Min/Shrink – Spacing Between Words (Min/Shrink)

Number · Regular+ · `s_minSpace` · cfg `document/spaceshrink`  
Values: 10–200 (default 50) · Needs: “Between Words” · Greyed out by: “Lock UI Layout Settings”

> When justifying paragraphs, and especially when trying to shrink or grow a paragraph to take fewer or more lines, the horizontal distance that a space uses can be adjusted - allowing the text to shrink or grow. Lower values will enable a 'tighter' text and make it more flexible, but keep the readers in mind - and their need to distinguish word-breaks with ease. This value is a % percentage of a normal space width. TeX's default value is 66%.
>
> Minimum size % that a space can shrink to when necessary.

Lower values fit more text on a line, but words may become hard to tell apart. About 50–80 is common.

##### Max/Stretch – Spacing Between Words (Max/Stretch)

Number · Regular+ · `s_maxSpace` · cfg `document/spacestretch`  
Values: 50–999 (default 200) · Needs: “Between Words” · Greyed out by: “Lock UI Layout Settings”

> When justifying paragraphs, and especially when trying to shrink or grow a paragraph to take fewer or more lines, the horizontal distance that a space uses can be adjusted - allowing the text to shrink or grow. Larger values will enable a 'looser' text and make it more flexible to grow, but be careful to avoid 'rivers' or white space in paragraphs. This value is a % percentage of a normal space width. TeX's default value is 150%.
>
> Maximum size % that a space can grow to when necessary.

Higher values let lines stretch more, but can leave big gaps. About 150–200 is common.

##### Spacing Between Letters (Min/Shrink)

Number · Regular+ · `s_letterShrink` · cfg `document/lettershrink`  
Needs: “Between Letters” · Greyed out by: “Interlinear  &  Code”, “Lock UI Layout Settings”

> Values are in percentage of the text point size.

Keep it small (a few percent at most).

##### Spacing Between Letters (Max/Stretch)

Number · Regular+ · `s_letterStretch` · cfg `document/letterstretch`  
Needs: “Between Letters” · Greyed out by: “Interlinear  &  Code”, “Lock UI Layout Settings”

> Values are in percentage of the text point size.

Keep it small.

#### Writing System

##### Text Flow Direction – Text direction (Right-to-left RTL etc)

Drop-down · Basic+ · `fcb_textDirection` · cfg `document/ifrtl`, `document/toptobottom`  
Choices: Left-to-Right | Right-to-Left | Top-to-Bottom (and Left-to-Right) · Greyed out by: “Lock UI Layout Settings”

> Select the direction for the text to flow. Note that the option for "Top to Bottom" lays out the vertical lines left to right.

**Right-to-Left** also ticks **RTL Book Binding**. Changing this changes the whole layout.

##### Text Script

Drop-down · Basic+ · `fcb_script` · cfg `document/script`  
Choices: Latn · Greyed out by: “Lock UI Layout Settings”

> Choose the script of the text. It is used for font shaping, and PTXprint provides additional typesetting functionality for some scripts:  
> Arabic, Myanmar, Thai, Lao, Tai Tham, New Tai Lue, Bengali, Malayalam, Tamil, Sinhala, Telugu, Kannada, Oriya, and Chinese (Han).
>
> If set to "Default", PTXprint tries to detect the script when the project is opened.

For example, it makes `/` a word-break mark in Thai, Lao, Myanmar, Tai Tham and New Tai Lue. Changing it may also change **Digit mapping** and **Specify Line Break Locale**.

##### Additional Script Settings...

Button · Basic+ · `btn_scrsettings`  
Greyed out by: “Lock UI Layout Settings”

> A small number of complex scripts (such as Myanmar, Indic, Arabic & Han) have additional options which can be set individually.

Only active for scripts that have options: Myanmar, Malayalam, Tamil, Sinhala, Telugu, Kannada, Oriya, Arabic, and Han (Simplified and Traditional).

##### Specify Line Break Locale

Checkbox, off · Regular+ · `c_linebreakon` · cfg `document/iflinebreakon`  
Also: Enable Line Break Locale · Greyed out by: “Lock UI Layout Settings”

> Some languages that use complex scripts need dictionary support for line breaking. Note that the dictionary used will be LWC-specific. For example, zh for Chinese, ko for Korean, etc. Note that Graphite fonts can also have line breaking rules which can be enabled by using the gr locale.

For scripts with no spaces between words. Ticked automatically when you choose a Han, Japanese or Korean script.

##### Set Line Break Locale

Text box · Regular+ · `t_linebreaklocale` · cfg `document/linebreaklocale`  
Needs: “Specify Line Break Locale” · Greyed out by: “Lock UI Layout Settings”

> Language code for dictionary-based line breaking (for scripts without spaces between words):  
> ja = Japanese km = Khmer ko = Korean my = Myanmar th = Thai zh = Chinese  
>    OR gr = Graphite

`gr` uses the line-breaking rules built into a Graphite font.

##### RTL Book Binding

Checkbox, off · Regular+ · `c_RTLbookBinding` · cfg `cover/rtlbookbinding`  
Also: Set the binding to Right (for RTL publications) · Greyed out by: “Lock UI Layout Settings”

> Enable this for Right-to-Left publications (so that the book is bound on the right hand side).

Affects where the binding gutter goes, how PDF viewers show the pages, and the cover. Ticked automatically when you choose **Right-to-Left** text direction.


# 7. Body tab

## 7.1 What this tab is for

The **Body** tab controls *what* is printed from each book, and some of *how* the main text looks.
Come here when you want to:

* leave out parts of the text, for example the book introductions, section headings or empty verses;
* hide or show chapter numbers and verse numbers;
* put verse numbers in a column next to the text (marginal verses);
* change how glossary words are marked in the text;
* start chapters on a new page, or print some books in one column and others in two.

Some settings **remove text** before typesetting. Others only **change the appearance** and keep
all the text. This matters. For example, if you hide verse numbers, the running header can still
show chapter and verse references, because the verses are still there. If you untick **Headings**,
the section headings are taken out completely. Each section below says which kind of setting it is.

The tab has three areas: **Beginning and Ending Material**, **Include Scripture Text** and
**Other Features**. Some settings are only shown in the **Regular** or **Full** view.

## 7.2 Beginning and Ending Material

These settings deal with the introduction at the start of each book, and with the glossary.

* **Book Introductions** and **Introductory Outlines** **remove content** when unticked: PTXprint
  takes these paragraphs out before typesetting. Only material before the first chapter is affected.
  * **Book Introductions** covers the introduction paragraphs and headings (`\is`, `\ip`, `\im`, `\ili` …).
  * **Introductory Outlines** covers only the outline (`\io1`–`\io4`, `\iot`, `\ior`).
  * You can print the introduction without the outline, or the outline without the introduction.
* **Right-align \ior With Tabbed Leaders** only changes the appearance of the outline: the reference
  at the end of each outline line goes to the right edge, with dots before it, like a table of
  contents. It does nothing in non-Scripture books.
* **Filter Glossary to Only Include Entries Used in the Text** **removes content** from the
  glossary book (GLO). It only matters when GLO is one of the books you print.
* **Start 1st Chapter on a New Page** and **Start All Other Chapters on a New Page** add page breaks.
  They do not remove text.

## 7.3 Include Scripture Text

The checkbox **Include Scripture Text** is the title of this area. Leave it ticked. Unticking it
**removes** everything from the first chapter onwards in every book, so only the introductions (and
other material before chapter 1) are printed. This is useful for checking the introductions. All
other settings in this area are greyed out while it is unticked.

### What is included

* **Headings** – section headings (`\s`, `\s1`, `\s2` …). Unticking it **removes** all section
  headings and all parallel passage references.
* **Parallel Passage Refs** – the references under some section headings (`\r`), for example
  "(Mark 1:1-8)". Unticking it **removes** them. Greyed out when **Headings** is unticked.
* **Hide Empty Verses** **removes** verses (and whole chapters) that have no text yet, for a draft
  where only part of the book is translated. Tick **Show '...'** as well to show the reader where
  text was left out.
* **Chapter numbers** and **Verse Numbers** only change the **appearance**. When unticked, the
  numbers are not printed, but PTXprint still knows the chapters and verses. So headers, footnotes
  and cross-references still work.

### How the text looks

* **Justify Paragraphs** – ticked gives straight left and right edges. Unticked gives a ragged
  right edge (ragged left for right-to-left scripts).
* **Indent First Paragraph** – when unticked, the first paragraph after a section heading starts at
  the margin.
* **Hide First Verse Number** – hides the "1" of verse 1 after a large (dropped) chapter number, or
  when marginal verses are used.
* **Hanging Poetry Verse Numbers** – the verse number sits to the left of the poetry line, so all
  poetry lines stay lined up.
* **Prevent Verse Widow Words**, **Prevent Orphan Words** and **Keep Repeated Words Together**
  join some words with a space that cannot break. This changes where lines break, not the words.

### Marginal verses

Tick **Marginal Verses** to print verse numbers in a narrow column beside the text. Then choose the
side in **Position on Page** and the column width in **Col Width (pts)**. (A pt, or point, is about
0.35 mm.) While **Marginal Verses** is ticked, **Hanging Poetry Verse Numbers** is turned off and
greyed out.

### Style links

The small links **\s**, **\r**, **\c** and **\v** open the **Styles** tab at that marker, to change
the font, size or spacing of section headings, parallel references, chapter numbers or verse numbers.

## 7.4 Other Features

This area is for special treatment of some books, and for glossary words.

* **Use Special Features for These Books** (Full view only) prints a text label before each chapter
  number, for example "Psalm 1" as a heading, instead of a large dropped number. This is common
  for Psalms. Type the label in **Chapter Label** and the book codes in the list box beside the
  checkbox. **Optimize Layout for Poetry Books** belongs to this group.
* **Use One/Two Column Layout for These Books** (Full view only) lets some books use a different
  number of columns from the rest. The label says "Use One Column" when the publication is two
  columns (set on the **Layout** tab), and "Use Two Column" when it is one column.
* **Glossary Word Appearance** decides how glossary words (`\w ...\w*`) look in the text.
* **Show Chapter Numbers In: Single Chapter Books** and **Non-Scripture Books** decide whether a
  chapter number is printed in one-chapter books (such as Jude) and in peripheral books (such as
  the glossary). For non-Scripture books, unticking **removes** the chapter markers.
* The links **\w** and **\zglm** open the **Styles** tab for the glossary word style and for the
  glossary bracket characters.

## 7.5 Common tasks

### How do I print only the book introductions?

1. On the **Body** tab, untick **Include Scripture Text**.
2. Make sure **Book Introductions** (and **Introductory Outlines**, if wanted) are ticked.
3. Click **Print (Make PDF)**.
4. Tick **Include Scripture Text** again afterwards.

### How do I print a draft that has many untranslated verses?

1. On the **Body** tab, tick **Hide Empty Verses**.
2. If readers should see where text is missing, tick **Show '...'**.
3. Print again.

### How do I remove all section headings?

On the **Body** tab, untick **Headings**. The parallel passage references are removed too; you
cannot keep them without the headings.

### How do I show verse number 1?

On the **Body** tab, untick **Hide First Verse Number** (shown in the **Regular** and **Full** views).

### How do I put the verse numbers in the margin?

1. On the **Body** tab, tick **Marginal Verses**.
2. In **Position on Page**, choose **Left**, **Right**, **Inner** (next to the spine) or **Outer**
   (next to the page edge).
3. In **Col Width (pts)**, give enough width for the longest verse number, for example 12–16.
4. Print and check that numbers like "176" fit.

### How do I print "Psalm 1", "Psalm 2" … instead of large chapter numbers in Psalms?

1. Switch to the **Full** view.
2. On the **Body** tab, in **Other Features**, tick **Use Special Features for These Books**.
3. In the list box, type `PSA`. (An empty list means **all** books.)
4. In **Chapter Label**, type the word for "Psalm" in your language.
5. Print again.

### How do I print the glossary book in one column when the rest is two columns?

1. Switch to the **Full** view.
2. On the **Body** tab, tick **Use One Column Layout for These Books**.
3. In the box beside it, type `GLO`. Separate several books with spaces, for example `GLO PSA`.

### How do I change how glossary words look in the text?

1. On the **Body** tab, in **Other Features**, open **Glossary Word Appearance**.
2. Choose a style, for example **format as bold** or **star \*before word**.
3. For your own formatting, choose **\w ...\w\* char style** and click the **\w** link to edit that
   style on the **Styles** tab.

## 7.6 Common problems

**The parallel references disappeared.**
Cause: **Headings** was unticked. This also unticks and greys out **Parallel Passage Refs**.
Fix: tick **Headings** again, then tick **Parallel Passage Refs**.

**Verse 1 is still printed, although "Hide First Verse Number" is ticked.**
Cause: verse 1 is only hidden after a dropped chapter number (or with marginal verses). If chapters
use a label (for example "Psalm 1") or chapter numbers are hidden, verse 1 can still show.
Fix: check the chapter number settings on this tab.

**"Hanging Poetry Verse Numbers" is greyed out.**
Cause: **Marginal Verses** is ticked. The two cannot be used together.

**"Optimize Layout for Poetry Books" has no effect.**
Cause: it only works for the books listed beside **Use Special Features for These Books**, and only
while that is ticked. If the list is empty, nothing is optimized.
Fix: tick **Use Special Features for These Books** and type the book codes (for example `PSA PRO`).

**The chapter label appears in every book, not only Psalms.**
Cause: the book list beside **Use Special Features for These Books** is empty, which means
"all books". Fix: type the book codes in the list.

**The glossary is still very long after ticking "Filter Glossary…".**
Cause: an entry is kept when its word is marked as a glossary word (`\w ...\w*`) in the books you
print, or inside another kept entry. Words not marked in the text do not count.
Fix: check the glossary markup in Paratext.

**Some lines have large gaps after ticking "Keep Repeated Words Together" or "Prevent Orphan Words".**
Cause: these settings stop the line breaking between some words, so it breaks elsewhere.
Fix: untick the setting, or fix the few bad lines by hand.

**"In Margin" (for headings) is greyed out.**
Cause: it needs **Margin Notes** turned on (on the **Layout** tab) and **Headings** ticked.

**The chapter numbers are missing in the glossary or other peripheral books.**
Cause: by default PTXprint removes chapter numbers from non-Scripture books. Fix: tick
**Non-Scripture Books** under **Show Chapter Numbers In**.

## 7.7 Settings reference

### Body

#### Include Scripture Text

Checkbox, on · Basic+ · `c_mainBodyText` · cfg `document/ifmainbodytext`  
Also: Show or hide scripture text

> Normally you should leave this checked.
>
> BUT... if you require a printout of just the book introductions (usually for the purpose of final checking, or looking for consistency) then this option can be unchecked (to omit the verse text and everything else in the main body).

Unticking it **removes** chapter 1 and everything after it in every book. All other settings in the
**Include Scripture Text** area are greyed out while it is unticked.

#### Beginning and Ending Material

##### Book Introductions

Checkbox, on · Basic+ · `c_bookIntro` · cfg `document/bookintro`  
Also: Enable book introductions (\i..)

> Print the Book Introductions which appear at the beginning of each book. Includes markers like: \is \ip \im \ili etc.

Unticking it **removes** the introduction before typesetting (only material before chapter 1). The
outline is controlled separately by **Introductory Outlines**. Untick it for a "Scripture text only"
edition.

##### Introductory Outlines

Checkbox, on · Basic+ · `c_introOutline` · cfg `document/introoutline`  
Also: Enable introductory outlines

> Print the Introductory Outlines which appear at the beginning of each book. Includes markers: \io1 ... \io4 \ior \iot

Unticking it **removes** only the outline lines and the outline title. The rest of the introduction
stays if **Book Introductions** is ticked. Unticking it also unticks and greys out **Right-align \ior
With Tabbed Leaders**.

##### Right-align \ior With Tabbed Leaders

Checkbox, off · Regular+ · `c_prettyIntroOutline` · cfg `snippets/fancyintro`  
Also: Enable Right-aligned outlines with leaders · Needs: “Introductory Outlines”

> This will right-align and add leader tabs (. . . .) before the \ior numbers for a pretty Intro Outline Table.

Appearance only. Not applied to non-Scripture books.

##### Filter Glossary to Only Include Entries Used in the Text

Checkbox, off · Basic+ · `c_filterGlossary` · cfg `document/filterglossary`

> This option only has an effect if the Glossary (GLO) is one of the books being printed. If you have large glossary with many entries but are only printing a small selection of books, you may benefit from this option which will strip out any entries from the Glossary which are not marked-up in the text of the selected book(s) or chapter(s). i.e. only the \w marked-up\w* entries in the selected books/chapters will show in the glossary. Entries marked up inside a kept entry are also kept.

Use it when you print only a few books with a large glossary. All other entries are **removed** from
the printed glossary.

##### Start All Other Chapters on a New Page

Checkbox, off · Basic+ · `c_pagebreakAllChs` · cfg `document/pagebreakallchs`  
Also: Start every chapter on a new page

> Use this option to force a page break before every chapter. This is most commonly used for testing materials when each chapter needs to be printed and given to a different person.

Every chapter except chapter 1. It can use a lot of paper. To also start chapter 1 on a new page,
tick **Start 1st Chapter on a New Page**.

##### Start 1st Chapter on a New Page

Checkbox, off · Basic+ · `c_ch1pagebreak` · cfg `document/ch1pagebreak`  
Also: Start new page after introduction

> Use this option to automatically make a page break after a book's introduction section. The break will come right before the \c 1 marker.

Use it when the introductions are long, or for a cleaner look.

#### Include Scripture Text

##### Hide First Verse Number

Checkbox, on · Regular+ · `c_omitverseone` · cfg `document/ifomitverseone`  
Needs: “Include Scripture Text”

> It is quite common to hide the first verse number - especially when following a drop-cap chapter number. By default this option is on. If you prefer to see verse number 1, then uncheck this option.
>
> Note: verse 1 is only hidden when it follows a drop-cap chapter number, or when marginal verses are used.

This is the usual style. The verse still exists, so references still work.

##### Keep Repeated Words Together

Checkbox, off · Regular+ · `c_glueredupwords` · cfg `document/glueredupwords`  
Needs: “Include Scripture Text”

> This option encourages re-duplicated words (i.e. those which are intentionally repeated) to come together on the same line by inserting a NoBreakSpace between them (only words of 3 or more letters). For example, "gama gama", or "kala kala" need to be stuck together (with a NBSP) in order to be read meaningfully. However, if there are many of these in the language, then it may create other unwanted typesetting issues. Use with care!

The two words then always stay on the same line. Check the result before you keep it.

##### Indent First Paragraph

Checkbox, on · Regular+ · `c_firstParaIndent` · cfg `document/firstparaindent`  
Also: Indent first paragraph after section heading · Needs: “Include Scripture Text”

> If this option is unchecked, it will make the 1st  
> \p(aragraph) after a Section Heading appear as a \m(argin) paragraph with no indentation.

Unticked is common in many books. Appearance only.

##### Hanging Poetry Verse Numbers

Checkbox, on · Regular+ · `c_hangpoetry` · cfg `document/hangpoetry`  
Also: Use hanging verse number for poetry · Needs: “Include Scripture Text” · Greyed out by: “Marginal Verses”

> Verse numbers for Poetry elements all line up vertically on the margin, and Verse Bridges (3-4) also stack vertically.

Turned off and greyed out when **Marginal Verses** is ticked.

##### Prevent Verse Widow Words

Checkbox, off · Regular+ · `c_preventwidows` · cfg `document/preventwidows`  
Needs: “Include Scripture Text”

> This option prevents short words (of 3 characters or less) from occurring AFTER a verse begins near the end of a line.

Joins the verse number and the short word to the next word, so the verse number does not sit alone
at the end of a line. Changes line breaks only.

##### Prevent Orphan Words

Checkbox, off · Basic+ · `c_preventorphans` · cfg `document/preventorphans`  
Also: Prevent orphan words at end of paragraph or start of line. · Needs: “Include Scripture Text”

> This option limits short words at the ends of paragraphs from occurring on a line on their own. It also prevents short words at the end of sentences from starting on a new line.
>
> The maximum orphan word length can be set in the 'Body Text' section of the Advanced > Other tab.

Changes line breaks only. The maximum "short word" length is **Maximum orphan word length** on
the **Advanced** tab, **Other** tab, **Body Text** area (default 8 letters).

##### Justify Paragraphs

Checkbox, on · Basic+ · `c_justify` · cfg `paragraph/ifjustify`  
Needs: “Include Scripture Text”

> By default the text will be fully justified. If you prefer a ragged edge, then uncheck this option.
>
> Note that a justification setting of "Justify" in a style is subject to this setting.

Ragged text can be easier to read in narrow columns and in languages with long words.

##### Headings

Checkbox, on · Basic+ · `c_sectionHeads` · cfg `document/sectionheads`  
Also: Enable section headings · Needs: “Include Scripture Text”

> Uncheck this option if you don't want to print any Section Headings. Unchecking this option will ALSO uncheck the Parallel Passage Refs.

Removes `\s`, `\s1`, `\s2` … and all `\r` references. Unticking it also turns off **In Margin**.
Ticking it again ticks **Parallel Passage Refs** again.

##### \s

Link · Regular+ · `lb_style_s`  
Needs: “Headings”, “Include Scripture Text”

> Click to edit the marker's properties on the Styles tab.

Change the section heading's font, size, spacing or alignment.

##### In Margin

Checkbox, off · Regular+ · `c_headingInMargin` · cfg `document/headinginmargin`  
Also: Show Section Headings in Margin · Needs: “Include Scripture Text”

> If Margin Notes has been enabled on the Layout Tab, it is possible to also place the Section Headings in the margin. Note that Parallel Passage Refs (if used) will also be placed in the margin area.

Greyed out unless **Margin Notes** (on the **Layout** tab) and **Headings** are both on. In the
version this manual describes, the setting is saved but no part of the typesetting uses it yet, so it
may have no visible effect.

##### Parallel Passage Refs

Checkbox, on · Regular+ · `c_parallelRefs` · cfg `document/parallelrefs`  
Also: Enable parallel passage references · Needs: “Headings”, “Include Scripture Text”

> Uncheck this option to hide all the Parallel Passage References which occur below Section Headings.

Unticking it **removes** the `\r` references. The headings stay.

##### \r

Link · Regular+ · `lb_style_r`  
Needs: “Headings”, “Parallel Passage Refs”, “Include Scripture Text”

> Click to edit the marker's properties on the Styles tab.

Opens the parallel passage reference style (`\r`).

##### Hide Empty Verses

Checkbox, off · Basic+ · `c_hideEmptyVerses` · cfg `document/hidemptyverses`  
Also: Show or hide empty verses · Needs: “Include Scripture Text”

> Do not print any empty chapters or verses. Useful for when only part of the text has been drafted but you still need a printout of whatever has been translated so far.

Turn it off for the final publication, so you do not hide verses by mistake.

##### Show '...'

Checkbox, off · Basic+ · `c_elipsizeMissingVerses` · cfg `document/elipsizemptyvs`  
Also: Show elipsis in place of missing verses · Needs: “Hide Empty Verses”, “Include Scripture Text”

> Indicate using ellipsis that verses and/or entire chapters are missing by placing '...' in the text to alert the reader that some parts of the text have been skipped.

Applies to verses or chapters removed by **Hide Empty Verses**.

##### Marginal Verses

Checkbox, off · Basic+ · `c_marginalverses` · cfg `document/marginalverses`  
Also: Show verse numbers in the margin · Needs: “Include Scripture Text”

> Some language communities prefer the verse numbers to be displayed in a vertical stack NEXT to the text (rather than within the text itself). If that is what is required, check this option and also adjust the width of that column to fit the verse numbers.

**Hanging Poetry Verse Numbers** is turned off. Verse 1 is hidden when **Hide First Verse Number** is
ticked. If two short verses start on the same line, their numbers can collide; you may need to
adjust that paragraph.

##### Position on Page – Horizontal position of marginal verses

Drop-down · Basic+ · `fcb_marginVrsPosn` · cfg `document/marginalposn`  
Choices: Left | Right | Inner | Outer · Needs: “Marginal Verses”, “Include Scripture Text”

> Marginal verses are usually placed on the left of the text, but can be positioned elsewhere if needed.

**Inner** is next to the spine, **Outer** next to the page edge; these change sides on left-hand and
right-hand pages.

##### Col Width (pts) – Column width for marginal verses

Number · Basic+ · `s_columnShift` · cfg `document/columnshift`  
Needs: “Marginal Verses”, “Include Scripture Text”

> This is the amount of space beside the column of text to accommodate marginal verse numbers. (pts)

Make it wide enough for your longest verse number in your verse number font, for example 12–16 pt.
Too small, and the numbers touch the text. Too large, and you lose text space.

##### Chapter numbers

Checkbox, on · Basic+ · `c_chapterNumber` · cfg `document/ifshowchapternums`  
Also: Show chapter numbers · Needs: “Include Scripture Text”

> Uncheck this option to hide all chapter numbers - making the publication read more like an ordinary book.
>
> Note that the 'Single Chapter Books' option lower down (Show Chapter Numbers in:) controls chapter numbers in one-chapter books only.

Appearance only: the chapters still exist, so the running header can still show chapter references.

##### \c

Link · Regular+ · `lb_style_c`  
Needs: “Include Scripture Text”

> Click to edit the marker's properties on the Styles tab.

Change the size, font or colour of chapter numbers.

##### Verse Numbers

Checkbox, on · Basic+ · `c_verseNumbers` · cfg `document/ifshowversenums`  
Also: Show verse numbers · Needs: “Include Scripture Text”

> Uncheck this option to hide all verse numbers - making the publication read more like an ordinary book.

Appearance only: the verses still exist, so headers and notes still work.

##### \v

Link · Regular+ · `lb_style__v`  
Needs: “Include Scripture Text”

> Click to edit the marker's properties on the Styles tab.

Change the font, size, colour or raised position of verse numbers.

#### Other Features

##### Use Special Features for These Books

Checkbox, off · Full · `c_useChapterLabel` · cfg `document/ifchaplabels`  
Also: Enable special features for some books

> Some Poetical books like the Psalms, and maybe even Proverbs look better without drop-cap chapter numbers. Instead, they can use a prefix like "Chapter" or "Psalm" at the start of the chapter. Note: If the text already has one or more \cl markers, then these settings will override what has been set in the text.

Type the label in **Chapter Label** and the books in the list box beside it.

##### List of books with special features enabled

Text box · Full · `t_clBookList` · cfg `document/clabelbooks`  
Needs: “Use Special Features for These Books”

> Add the 3-letter book codes for any books that this "Chapter Label" setting should be applied to.
>
> Note: If this list of books is left empty, then this setting will be applied to ALL books

Separate codes with spaces, for example `PSA PRO`. The same list is used by **Optimize Layout for
Poetry Books**.

##### Chapter Label – Chapter label (for special feature books)

Text box · Full · `t_clHeading` · cfg `document/clabel`  
Needs: “Use Special Features for These Books”

> The chapter “label” to be used when rendering chapter divisions as headings (instead of drop-cap numerals). For example, "Chapter" or "Psalm".
>
> If you want the chapter number to appear centered and above the Section Header WITHOUT any preceding text, then just put the code \ZWNBSP in here. This will insert a Zero Width No-Break Space.

Advanced: `\ZWNBSP` is an invisible character.

##### Use One/Two Column Layout for These Books

Checkbox, off · Full · `c_differentColLayout` · cfg `document/diffcolayout`  
Also: Enable 1 or 2 column layout for certain books

> Some books (e.g. Introduction, Glossary, Psalms, and maybe even Proverbs) look better formatted as single column, even though most of the books are typeset in two column layout. This allows the same publication to have both single and double column layouts.
>
> Add the 3-letter book codes for any books that should be typeset using a different column layout.
>
> Note that if the layout for the entire publication is set to single column, then the books listed here would use double-column layout. Conversely, if the publication is set as double-column (on the layout page) then any books listed here would be set in single-column layout.

The checkbox label changes to show which (one or two columns). A typical use is a two-column Bible
with a one-column glossary.

##### Optimize Layout for Poetry Books

Checkbox, on · Full · `c_optimizePoetryLayout` · cfg `document/cloptimizepoetry`  
Needs: “Use Special Features for These Books”

> Trying to get columns of poetry to balance often creates all sorts of unforeseen issues and unwanted whitespace. This option allows columns to be unbalanced, which might improve the overall look. But note that it also allows Widow and Orphan lines to occur, which is a negative side-effect. It applies only to the books listed above.

Allows single lines at the top or bottom of a column. This often removes large white gaps in poetry
books like Psalms. Other books are not changed. Untick it to keep normal column balancing for the
listed books. It does nothing if the book list is empty.

##### List of books with different column settings

Text box · Full · `t_differentColBookList` · cfg `document/diffcolayoutbooks`  
Needs: “Use One/Two Column Layout for These Books”

> Some books (e.g. Introduction, Glossary, Psalms, and maybe even Proverbs) look better formatted as single column, even though most of the books are typeset in two column layout. This allows the same publication to have both single and double column layouts.
>
> Add the 3-letter book codes for any books that should be typeset using a different column layout.
>
> Note that if the layout for the entire publication is set to single column, then the books listed here would use double-column layout. Conversely, if the publication is set as double-column (on the layout page) then any books listed here would be set in single-column layout.

Separate codes with spaces, for example `GLO` or `PSA PRO`.

##### Glossary Word Appearance – Markup for glossary words in text

Drop-down · Basic+ · `fcb_glossaryMarkupStyle` · cfg `document/glossarymarkupstyle`  
Choices: None | format as bold | format as italics | format as bold italics | format with emphasis | with ⸤floor⸥ brackets | with ⌊floor⌋ characters | with ⌞corner⌟ characters | star *before word | star after* word | star *before and after* | circumflex ^before word | circumflex after^ word | dagger †before word | dagger after† word | double dagger ‡before word | double dagger after‡ word | \w ...\w* char style | \w keep|as is\w*

> Glossary words are marked up with special \w glossary\w* tags. Specify how these words should be highlighted in the printed output.
>
> The final option \w keeps|markup\w* as it is without removing any parameters such as Strong's numbers.
>
> Glossary words may be marked up with \w glossary\w* tags. Specify how these words should appear in the printed output.
>
> If you wish to apply your own custom styling to \w then select the \w ...\w* character style option.

* **None** – plain text.
* **format as bold / italics / bold italics / with emphasis** – the word gets that formatting.
* **with ⸤floor⸥ brackets**, **⌊floor⌋** or **⌞corner⌟ characters** – the word goes between
  these characters. Style them with the **\zglm** link. Your font must contain them.
* **star**, **circumflex**, **dagger** or **double dagger** – a mark before or after the word. For a
  star on both sides, choose **star \*before and after\***.
* **\w ...\w\* char style** – uses the `\w` style from the **Styles** tab, so you can design your own.
* **\w keep|as is\w\*** – keeps extra information such as the glossary form or Strong's numbers.
  Choose it only if another feature needs that (for Strong's numbers, see the **Notes+Refs** tab).

With all choices except the last, any part after a `|` (for example `\w word|glossaryform\w*`) is
removed, so only the word itself is printed.

##### Single Chapter Books

Checkbox, on · Basic+ · `c_show1chBookNum` · cfg `document/ifshow1chbooknum`  
Also: Show chapters in single chapter books

> Select this option to show the 1 at the beginning of books that only have a single chapter (OBA, PHM, 2JN, 3JN, JUD, etc.)

Appearance only. No effect when **Chapter numbers** is unticked.

##### Non-Scripture Books

Checkbox, off · Basic+ · `c_showNonScriptureChapters` · cfg `document/showxtrachapnums`  
Also: Show chapters in non-scripture books

> Peripheral books often have more than one "chapter" but do not need the chapter number to be printed. By default, PTXprint removes the chapter numbers from non-scripture books. If you need it to retain (and show) those chapter numbers then check this option.

Tick it only if those books really need their chapter numbers.

##### \w

Link · Regular+ · `lb_style_w`

> Click to edit the marker's properties on the Styles tab.

Used when **Glossary Word Appearance** is **\w ...\w\* char style**.

##### \zglm

Link · Regular+ · `lb_style_zglm`

> The \zglm style is used to format the floor brackets used in glossary markup.
>
> Click to edit the marker's properties on the Styles tab.

For example, to make the brackets smaller or a different colour.


# 8. Notes+Refs tab

## 8.1 What this tab is for

The **Notes+Refs** tab controls the extra information that sits outside the main Bible text. It has three sub-tabs: **Footnotes**, **Cross-References** and **Study Notes + Questions**. Come here to show or hide notes, change where they appear on the page, change the small marks that point to them, or add thousands of cross-references from a ready-made list.

There are three kinds of notes:

* **Footnotes** (`\f` in the text) explain something about the text. For example: "Some old manuscripts add the words …" or "Hebrew: *son of Adam*". The translation team writes them in Paratext.
* **Cross-references** (`\x` in the text) are only lists of other Bible places about the same thing. For example: "Gen 1:1; Ps 33:6". They can come from the project text, or PTXprint can add them from an external list.
* **Extended notes or study notes** (`\ef` in the text) are longer explanations, like the notes in a study Bible. PTXprint prints them in their own area at the bottom of the page, usually in two columns. Transcelerator comprehension questions are printed in this same area.

Some words used in this chapter:

* **Caller** – the small mark in the Bible text (for example *a*, *b* or †) that tells the reader "there is a note about this". The same mark is usually repeated at the start of the note.
* **Rule** – a thin horizontal line between the Bible text and the notes area.
* **Gutter** – the empty space between two columns.
* **pt** (point) – a small unit of measure. 1 pt is about 0.35 mm, and 72 pt is about 25 mm (1 inch).

The **Notes+Refs** tab is shown in the **Basic** view and above. Many settings are only shown in the **Regular** or **Full** view. External cross-reference lists and extended study notes are only shown in the **Full** view.

## 8.2 Footnotes

On the **Footnotes** sub-tab, the top area decides *whether* footnotes are printed and *where* they go.

* **Include Footnotes** turns all footnotes on or off. When it is off, PTXprint removes every `\f ... \f*` note before it makes the PDF, and most other footnote settings are greyed out.
* **Placement of Footnotes** has these choices:
  * **End of Page** – the normal choice. Notes appear at the bottom of the page where their caller is.
  * **End of Column** – only possible with a **Two Column Layout** (set on the **Layout** tab). The notes are set at the width of one column, at the bottom of the second column.
  * **End of Book** – the notes are collected and printed at the end of each book, as end notes.
  * **Side Margin** – the notes go in a narrow column next to the text, as close as possible to the line with the caller. This is greyed out until you tick **Margin Notes Col Width (mm)** on the **Layout** tab (**Page Setup** area). If you turn margin notes off again, PTXprint moves the footnotes back to **End of Page**.
* **Start Each Footnote on a New Line** – normally short footnotes run on one after the other in one paragraph, which saves a lot of space. Tick this if each note must start on its own line.

### Callers

The caller settings decide which marks are used for footnotes.

* **Show Callers** (in the text) – when ticked, PTXprint uses the sequence of marks in the box next to it. Separate the marks with commas and no spaces, for example `a,b,c,d,e` or `†,‡,§`. The reload button next to the box loads the callers from the Paratext project settings.
* **Show Callers in Notes Area** – repeats the caller at the start of each note, so the reader can find the note that belongs to the mark.
* **Reset Callers on Page** – starts the sequence again at the first mark on every new page.
* **Override hidden/automatic Footnote caller settings** – in Paratext, each footnote says how its caller works: `\f +` (automatic caller), `\f -` (no caller), or a fixed mark. Normally PTXprint obeys the text. When you tick this option, PTXprint uses the **Show Callers** setting for every footnote instead.

### Rule and Space Settings

This area controls the line above the notes area and the space around it. **Space Above Rule** is the space between the last line of Bible text and the rule. **Space Below Rule** is the space between the rule and the first note. Even when the rule is hidden, PTXprint still leaves both spaces. The **Rule Positioning** settings (indent, length, thickness and horizontal position) are only shown in the **Full** view.

PTXprint draws only one rule above the notes at the bottom of the page. Normally it uses the footnote rule settings, even for cross-references. It uses the settings on the **Cross-References** sub-tab only when the footnotes are placed at the **End of Book**.

### Miscellaneous Footnote Settings

This area (only in the **Full** view) has small text changes that PTXprint makes in all notes, and the spacing between notes that run on in one paragraph:

* add a colon after quoted words in a note,
* keep a book name with its chapter and verse numbers,
* turn glossary words into footnotes,
* the minimum and maximum horizontal space between run-on notes,
* the vertical space between the footnote block and the cross-reference block.

## 8.3 Cross-References

The **Cross-References** sub-tab works like the **Footnotes** sub-tab, but it also lets you add cross-references from an external list.

### Where the cross-references come from

* **Include Cross-References (From Project Text)** prints the `\x ... \x*` notes that the team typed in Paratext.
* **Use External List of Cross-References** (only in the **Full** view) adds cross-references from a list that comes with PTXprint, or from your own file. PTXprint changes the book names into the short book names of your project (the abbreviations in the Paratext **Scripture Reference Settings**, which should match the `\toc3` lines). These cross-references have no caller in the text. They are usually used for a study or reference Bible, together with **Column Cross-References**.

You can use both sources at the same time.

### Placement of Cross-References

* **End of Page** – at the bottom of the page.
* **End of Column** – at the bottom of the second column.
* **End of Book** – collected at the end of each book.
* **Below Footnotes** – at the bottom of the page, in a separate block under the footnotes.
* **Blend with Footnotes** – mixed in with the footnotes as one paragraph. This saves space. PTXprint sets the `\x` style so that it joins the footnotes.
* **Column Cross-References** – in a narrow column of their own beside the text, as in many reference Bibles. With a two-column layout the column is between the two text columns. With a one-column layout you can choose the side.
* **Side Margin** – in the margin-notes column, next to the line they belong to. This needs **Margin Notes Col Width (mm)** on the **Layout** tab.

PTXprint keeps the footnote and cross-reference placement in step:

* If you choose **End of Column** for one kind of note, the other kind moves to **End of Column** too. The same happens for **End of Page**.
* If you choose **Column Cross-References**, the footnote placement changes to **End of Column**, and the **Source for References** area opens.
* If you untick **Include Footnotes** while cross-references are **Below Footnotes** or **Blend with Footnotes**, the cross-references move to **End of Page** (or to **Column Cross-References** if you use an external list).

The caller settings (**Show Callers**, **Show Callers in Notes Area**, **Reset Callers on Page**, **Override…**) work the same way as for footnotes.

### Source for References

This area (only in the **Full** view) is active when **Use External List of Cross-References** is ticked.

**External Refs** chooses the list:

* **Standard list (fewest)** to **Standard list (most)** – one large list of more than 340,000 cross-references. People have voted for the references, so the most useful ones come first. The five sizes take more or fewer of them: **(fewest)** gives only the most important references, **(most)** gives the most. Start with **Standard list** and change it if the column is too empty or too full.
* **Strong's list (all)** and **Strong's list (project)** – cross-references grouped by Strong's number (a number for each Hebrew or Greek word). The **(project)** list only uses words that have a rendering in your project's Biblical Terms. These two choices make the **Strong's References** area available.
* **TSK list** – the Treasury of Scripture Knowledge. It is very large.
* **BibleWorks™ list** – about 112,000 cross-references.
* **UBS GNT92 list** and **UBS GNT92 list (DC)** – the United Bible Societies list. Use **(DC)** if you need Deuterocanonical references.
* **Select a Custom list...** – use your own file. Then click **Select...** to choose it.

Hover the mouse over the small information button next to **Select...** to read a description of the chosen list.

**Include Refs for Books in** removes references that point to books your readers do not have. For example, if only the New Testament is translated, choose **New Testament**.

### Strong's References

These settings are only available when the source is one of the Strong's lists. You can show the Strong's numbers in the cross-references and in the Bible text itself, and make an index book with **Generate Index...** (see the **Generate Strong's Index** dialog below).

### Column Cross-References

These settings are only available when the placement is **Column Cross-References**. They set the width of the column, the gutter next to it, the side of the page, the vertical rules, and how the references are placed in the column. The column takes space from the Bible text. A larger page size, or a smaller `\x` font (about 6 pt), can help.

### Rule and Space Settings

These settings are for the cross-reference rule. PTXprint uses them only when footnotes or cross-references are at the **End of Book** (see **Footnotes** above).

## 8.4 Study Notes + Questions

This sub-tab is for study Bibles and for comprehension testing.

### Extended Footnotes (\ef)

Tick **Extended Footnotes (\ef)** (only in the **Full** view) to print the `\ef ... \ef*` study notes from the text. They appear in their own two-column area at the bottom of the page, under the ordinary notes. If this box is not ticked, PTXprint removes all `\ef` notes before it makes the PDF. When it is ticked, the area below shows settings for the gutter, the vertical rule between the columns, callers, and the rule above the study notes.

**Sidebars (\esb ... \esbe)** prints the boxed sidebars of a study Bible. If it is not ticked, PTXprint removes them. The look of sidebars is set on the **Styles** tab and in the sidebar settings.

### Include Transcelerator Questions

Transcelerator is a Paratext plugin from SIL for making comprehension-checking questions. If your project has Transcelerator data, PTXprint can print the translated questions at the bottom of each page, in the same area as study notes. Each question appears near the verse it is about. This is useful for comprehension-testing printouts. The **Example Questions** text shows how your choices will look. If there is no Transcelerator data for the project, the checkbox is greyed out.

### Filter Categories

In a study Bible, notes and sidebars can have a category, for example `\cat History\cat*`. **Filter Categories** (only in the **Full** view) shows a list of the categories in the project, with a tick box for extended notes and for sidebars. In this version, PTXprint does not save this list with the configuration, and it does not use it when it makes the PDF.

## 8.5 Generate Strong's Index dialog

To open this dialog, go to **Notes+Refs** › **Cross-References** and tick **Use External List of Cross-References**. Choose a **Strong's list** in **External Refs**, and then click **Generate Index...**.

The dialog makes a new book (in USFM, the Paratext file format) that lists each Strong's number and information about the word. Readers use it to look up a number they see in the cross-references. You choose:

* which sections to include: Hebrew words, Greek words, and an optional **Reverse Index** (an alphabetical list of words in your language, with their numbers);
* what each entry shows: the Hebrew or Greek word, a transliteration (the word written in Latin letters), your project's term renderings, a key verse reference, the definition and notes;
* what to use when your project has no rendering for a word: a rendering from another project, or a gloss in a major language;
* the headings of the index (in the table), the book to use, and one or two columns.

When you click **Create Index**, PTXprint writes the index into the chosen book of your project (normally **XXS**). **Warning:** anything that was already in that book is replaced. PTXprint then adds the book to the list of books to print and changes the book selection to multiple books. Click **Print** to see it.

The renderings come from your project's Biblical Terms renderings in Paratext. Fill those in first for a useful index.

## 8.6 Common tasks

### Hide all footnotes (or all cross-references)

1. Go to the **Notes+Refs** tab, **Footnotes** sub-tab.
2. Untick **Include Footnotes**.
3. For cross-references, go to the **Cross-References** sub-tab and untick **Include Cross-References (From Project Text)**. If **Use External List of Cross-References** is ticked, untick it too.
4. Click **Print**.

### Change the footnote callers to symbols

1. On **Notes+Refs** › **Footnotes**, make sure **Include Footnotes** and **Show Callers** are ticked.
2. In the box next to **Show Callers**, type the marks, separated by commas with no spaces, for example `*,†,‡,§`. Check that your font has these symbols.
3. If some notes still show other marks, tick **Override hidden/automatic Footnote caller settings**.
4. If you want the sequence to start again on each page, tick **Reset Callers on Page**.
5. Click **Print**. If the reset does not show correctly, click **Print** a second time.

### Put each footnote on its own line

1. On **Notes+Refs** › **Footnotes**, tick **Start Each Footnote on a New Line**.
2. For cross-references, tick **Start Each Cross-Reference on a New Line** on the **Cross-References** sub-tab.

### Move footnotes to the end of each book

1. On **Notes+Refs** › **Footnotes**, under **Placement of Footnotes**, choose **End of Book**.
2. Click **Print**. The notes appear after the last chapter of each book.

### Save space by mixing cross-references with footnotes

1. On **Notes+Refs** › **Cross-References**, under **Placement of Cross-References**, choose **Blend with Footnotes**.
2. Make sure **Include Footnotes** is ticked on the **Footnotes** sub-tab.
3. Click **Print**.

### Make a reference Bible with a column of cross-references

1. Choose the **Full** view.
2. On **Notes+Refs** › **Cross-References**, tick **Use External List of Cross-References**.
3. Under **Placement of Cross-References**, choose **Column Cross-References**.
4. In **Source for References**, choose a list in **External Refs** (for example **Standard list**).
5. In **Include Refs for Books in**, choose which books the references may point to (for example **New Testament**).
6. In **Column Cross-References**, set **Column Width (pts)** (start with 60) and, for a one-column layout, the **Side of page**.
7. Click **Print**. If the column is too full, choose a smaller list. If the text column becomes too narrow, use a larger page size or a smaller `\x` font on the **Styles** tab.

### Print study notes in two columns

1. Choose the **Full** view.
2. On **Notes+Refs** › **Study Notes + Questions**, tick **Extended Footnotes (\ef)**.
3. Adjust **Gutter Width (mm)** and, if you want a line between the columns, tick **Vertical Rule in Gutter**.
4. Click **Print**.

### Add Transcelerator questions to a printout

1. In Paratext, make sure the questions are translated in Transcelerator.
2. On **Notes+Refs** › **Study Notes + Questions**, tick **Include Transcelerator Questions**.
3. Check the **Language Code**. It must be the code of the language the questions were translated into.
4. Choose **Show Overview Questions**, **Number the Questions** and **Include Chapter:Verse References** as needed. Look at **Example Questions** to see the result.
5. Click **Print**.

### Create a Strong's index book

1. Choose the **Full** view. On **Notes+Refs** › **Cross-References**, tick **Use External List of Cross-References**.
2. In **External Refs**, choose **Strong's list (all)** or **Strong's list (project)**.
3. In the **Strong's References** area, click **Generate Index...**.
4. Choose the sections and entry parts you want. Edit the headings in the table if needed.
5. Check **Create Index in Book** (normally **XXS**). Anything already in that book will be replaced.
6. Click **Create Index**, then click **Print**.

## 8.7 Common problems

**The footnote or cross-reference settings are greyed out.**
Most footnote settings need **Include Footnotes**. The caller box and related settings need **Show Callers**. **End of Column** needs **Two Column Layout** on the **Layout** tab. **Side Margin** needs **Margin Notes Col Width (mm)** on the **Layout** tab. The **Source for References** settings need **Use External List of Cross-References**. The **Column Cross-References** settings need the **Column Cross-References** placement.

**I cannot find external cross-references, extended notes or the rule settings.**
These are only shown in the **Full** view. Change the view level and look again.

**The callers in the PDF are not the ones I typed.**
The notes in the text can ask for no caller (`\f -`) or a fixed caller. Tick **Override hidden/automatic Footnote caller settings** (or the cross-reference version), so that PTXprint uses your sequence for every note.

**Reset Callers on Page does not seem to work.**
PTXprint needs to know the page breaks first. Click **Print** a second time.

**The footnotes run into the footer.**
Increase **Space Above Rule (pt)** on the **Footnotes** sub-tab. This makes the page break a little earlier.

**My cross-reference placement changed by itself.**
PTXprint changes the footnote and cross-reference placements together (see "Placement of Cross-References" above). Check both sub-tabs after you change one of them.

**Changing the cross-reference rule settings has no effect.**
They are used only when footnotes are at the **End of Book** (see "Rule and Space Settings" under **Footnotes**). Change the rule on the **Footnotes** sub-tab instead.

**The external cross-references show the wrong book names.**
PTXprint uses the short book names from the Paratext project (**Scripture Reference Settings**, which should match the `\toc3` lines). Correct them in Paratext, then print again.

**Making the PDF is very slow.**
**Show Numbers in the Text** (for Strong's numbers) takes a lot of time. Untick it while you work on the layout. Very large cross-reference lists (for example **TSK list** or **Standard list (most)**) also make the PDF slower.

**Include Transcelerator Questions is greyed out.**
PTXprint cannot find Transcelerator data for this project. Use the Transcelerator plugin in Paratext for this project first. If the box can be ticked but no questions are printed, check that the **Language Code** matches the language the questions were translated into.

**The study notes do not appear.**
Tick **Extended Footnotes (\ef)** on the **Study Notes + Questions** sub-tab (only shown in the **Full** view). If it is not ticked, PTXprint removes all `\ef` notes.

## 8.8 Settings reference

### Generate Strong's Index... (dialog)

#### Create Index

Button · Regular+ · `btn_strong_ok`

> Click to generate the index book (USFM file) which will be appended to the list of books to be printed.
>
> Warning: This will overwrite the existing book/file.

Makes the index book and closes the dialog. PTXprint also changes the book selection to multiple books. Any text already in that book is replaced without another warning.

#### Cancel

Button · Regular+ · `btn_strong_cancel`

Closes the dialog without making an index. Your choices in the dialog are kept.

#### For Strong's Cross References to be most useful to readers, it is highly recommended to include an Index at the end of the publication. Set appropriate options here to create an Index file (in USFM format).

Label · Mini+

> Set the options (below), to create the Index file in a temporary book (XXS, or XXA...XXG). After clicking "Create Index", the generated index book will be appended to the list of books to be printed.

#### Hebrew Words (from the OT)

Checkbox, on · Regular+ · `c_strongsHeb` · cfg `strongsndx/showhebrew`  
Also: Strong's index: Include section for Hebrew words

Lists the Hebrew (Old Testament) Strong's numbers. Untick it if your publication is only the New Testament.

#### Greek Words (from the NT)

Checkbox, on · Regular+ · `c_strongsGrk` · cfg `strongsndx/showgreek`  
Also: Strong's index: Include section for Greek words

Lists the Greek (New Testament) Strong's numbers. Untick it if your publication is only the Old Testament.

#### \li

Link · Regular+ · `lb_style_li+strong-s`

> Click to select this marker on the Styles tab.
>
> Select which components should be included in the Strong's index when it is generated.

The `\li` style is used for each entry in the Strong's index. Change it to adjust the font size or indent of the entries.

#### Reverse Index (alphabetical listing with numbers)

Checkbox, off · Regular+ · `c_strongsNdx` · cfg `strongsndx/showindex`  
Also: Strong's index: Include section for reverse index

> This (optional) section is intended for readers who want to look up a word in their own language to find out the Strong's number.

Comes after the main lists. It lists your project's renderings in alphabetical order, each with its Strong's numbers, sorted with the Paratext project's sorting rules. It can only be made when the project has Biblical Terms renderings.

#### Hebrew or Greek Word

Checkbox, on · Regular+ · `c_strongsSrcLg` · cfg `strongsndx/sourcelang`  
Also: Strong's index entry: Include Hebrew and/or Greek

> The word in the source language(s) can be displayed in the index if useful to readers.

Your font must contain Hebrew and Greek letters, or the words will not show correctly. The `\wh` and `\wg` styles control how these words look.

#### Transliteration (Latin Script)

Checkbox, off · Regular+ · `c_strongsTranslit` · cfg `strongsndx/transliterate`  
Also: Strong's index entry: Include transliteration of source languages

> If the readers are unfamiliar with Greek and Hebrew it may be more useful in some contexts to show the transliterated (romanized) source language words.

The `\wl` style controls how it looks.

#### Term Rendering(s)

Checkbox, on · Regular+ · `c_strongsRenderings` · cfg `strongsndx/renderings`  
Also: Strong's index entry: Include receptor term renderings

> Show the term renderings from the project's Biblical Terms list.

Uses the Biblical Terms renderings in Paratext. This is usually the most useful part of each entry. If a word has no rendering, PTXprint uses the fallback settings below.

#### If No Local Rendering Found

Label · Mini+

> If no local term rendering is found in the Project's list of Biblical Term renderings, then several fallback options are possible:  
> a) Use the renderings from a regional language project b) Use a gloss from one of the majority languages c) Use the Biblical Term's definition (in English)

#### Key Verse Reference

Checkbox, on · Regular+ · `c_strongsKeyVref` · cfg `strongsndx/keyvrsrefs`  
Also: Strong's index entry: Include key verse reference

> The primary book, chapter and verse reference for the entry helps users find the first item in the list of cross-references related to the term.

The `\xt` style controls how it looks.

#### Definition

Checkbox, off · Regular+ · `c_strongsDefn` · cfg `strongsndx/definitions`  
Also: Strong's index entry: Include definitions

> Show the definition in addition to the term rendering(s).

The definition is in English and comes after the renderings. It makes the index longer.

#### \wl

Link · Regular+ · `lb_style_wl+strong-s`

> Click to select this marker on the Styles tab.

Opens the `\wl` style (the transliteration) used in the Strong's index.

#### \xt

Link · Regular+ · `lb_style_xt+strong-s`

> Click to select this marker on the Styles tab.

Opens the `\xt` style (the key verse reference) used in the Strong's index.

#### \wh

Link · Regular+ · `lb_style_wh+strong-s`

> Click to select this marker on the Styles tab.

Opens the `\wh` style (Hebrew words) used in the Strong's index. You can choose a font with Hebrew letters there.

#### \wg

Link · Regular+ · `lb_style_wg+strong-s`

> Click to select this marker on the Styles tab.

Opens the `\wg` style (Greek words) used in the Strong's index. You can choose a font with Greek letters there.

#### Remove (Comments) from Renderings

Checkbox, off · Regular+ · `c_strongsNoComments` · cfg `strongsndx/nocomments`  
Also: Strong's index entry: Remove comments from renderings

> Paratext allows for additional comments or notes to be added (in brackets) after term renderings. Check this option to prevent these from showing in the Strong's index.

Removes any text in round brackets ( ) from the renderings. Readers usually do not need these comments.

#### Wildcard* handling – Strong's index entry: How to handle wildcard* character

Drop-down · Regular+ · `fcb_strongswildcards` · cfg `strongsndx/wildcards`  
Choices: Keep wildcard* | Remove wildcard | Change to hyphen-

> The asterisk * is used as a matching wildcard in Term Renderings. If you prefer for this not to be displayed, select an appropriate option.

A wildcard such as `bless*` matches several word forms. **Change to hyphen-** prints a hyphen instead of the `*`.

#### tv_strvarEdit

Table · Regular+ · `tv_strvarEdit`

A table of the headings PTXprint uses in the index: the title of the book (`index_book_title`), the Hebrew and Greek section titles, and the title of the reverse index. Click a value to type the heading in your language.

#### Create Index in Book – Strong's index: Extra book code to be used

Drop-down · Regular+ · `fcb_strongsNdxBookId` · cfg `strongsndx/ndxbookid`  
Choices: XXS | XXA | XXB | XXC | XXD | XXE | XXF | XXG

> Select the temporary book to be used for the generated Strong's Cross Reference Index.
>
> By default, an extra book XXS is used to store the index. But if you prefer to use one of the other standard Paratext books XXA...XXG then select it here, but be aware that it will overwrite whatever is in that book without prior warning.

**XXS** is the default. Choose a book you do not use for anything else, because its contents are replaced.

#### Two Column Layout

Checkbox, on · Regular+ · `c_strongs2cols` · cfg `strongsndx/twocols`  
Also: Strong's index: Use 2-column layout

> Using a two column layout for the index is highly recommended, but if you prefer a one column layout, uncheck this option.

Recommended, because the entries are short. Untick it for one column.

#### Open Index File in Editor

Checkbox, off · Regular+ · `c_strongsOpenIndex` · cfg `strongsndx/openineditor`  
Also: Strong's index: Open index file after creating it

> Check this option to open the generated file in a text editor after the Index has been created.

Use it to check the new index file.

#### Unbalanced Lines (max) – Strong's index: Allow unbalanced lines

Number · Regular+ · `s_strongRag` · cfg `strongsndx/raglines`  
Needs: “Two Column Layout”

> By default (when this is set to 0) PTXprint will balance the number of lines used in each column. Sometimes this results in large empty spaces at the end of a page.
>
> Increasing this number (recommended range 1-4) will allow up to that many unbalanced lines on the page.

A value of 1 to 4 can avoid large empty spaces.

#### Notes

Checkbox, off · Regular+ · `c_strongsNotes` · cfg `strongsndx/notes`

> This is the Description field from the project's Biblical Terms renderings.

Adds this description text to each index entry. It is saved with the configuration, like the other settings in this dialog.

#### If No Local Rendering Found:

##### Use the Term Rendering from a Fallback Project

Label · Mini+

> Select the project to search within for a term rendering for entries which do not have a local rendering.

##### Use Major Language Gloss – Strong's index: Use major language gloss (if no rendering found)

Drop-down · Regular+ · `fcb_strongsMajorLg` · cfg `strongsndx/majorlang`  
Choices: None | English | French | Indonesian | Portuguese | Spanish

> If all else fails, you can display the gloss in a major language.

Used only when there is no rendering in your project or in the fallback project. Choose **None** to leave these words without a gloss.

##### Use Major Language Gloss

Label · Mini+

> If all else fails, you can display the gloss in a major language.

##### Use the Term Rendering from a Fallback Project – Strong's index: Use fallback project (if no rendering found)

Drop-down · Regular+ · `fcb_strongsFallbackProj` · cfg `strongsndx/fallbackprj`

> Select the project to search within for a term rendering for entries which do not have a local rendering.

For example, a project in a regional language. PTXprint uses its Biblical Terms renderings for words with no rendering in your project.

### Notes+Refs

#### Footnotes

##### Show Callers in Notes Area

Checkbox, on · Regular+ · `c_fnomitcaller` · cfg `notes/fnomitcaller`  
Also: Show footnote callers in notes area · Needs: “Include Footnotes”, “Show Callers in the Text”

> Usually the "Caller" symbol is also shown in the notes area which helps the reader quickly find the footnote from the text.

Untick it to print the note without the mark. This saves a little space.

##### Reset Callers on Page

Checkbox, on · Regular+ · `c_fnpageresetcallers` · cfg `notes/fnresetcallers`  
Also: Reset footnote callers on each page · Needs: “Include Footnotes”, “Show Callers in the Text”

> If this is checked, then the sequence of callers starts again from the 1st item in the list of callers specified.
>
> Note that this feature doesn't always take effect straight away. You may need to hit Print a second time before it applies.

This keeps the callers short when you use symbols.

##### Show Callers in the Text

Checkbox, on · Regular+ · `c_fnautocallers` · cfg `notes/iffnautocallers`  
Also: Show Footnote Callers in the Text · Needs: “Include Footnotes”

> A "Caller" is a symbol (in the text) which alerts the reader that there is further information (in this case a footnote at the bottom of the page). Ideally, the caller should be distinct from the rest of the text, so a symbol works well if supported by the font. Otherwise the letters of the alphabet can be used.
>
> Separate callers with a comma (no spaces). For example: a,b,c,d,e,f,g,h, etc. or:  †,‡,§,∥,#    or: ✶,☆,✦,✪
>
> If you do not see the callers you are expecting in the PDF, then try using the "Override..." setting above.

When not ticked, the caller box is greyed out and no automatic caller sequence is used. Together with **Override hidden/automatic Footnote caller settings**, unticking it removes the callers from all footnotes.

##### Footnote Caller Sequence Entry

Text box · Regular+ · `t_fncallers` · cfg `notes/fncallers`  
Needs: “Include Footnotes”, “Show Callers in the Text”

> These callers should automatically be loaded from the settings in the Paratext project, but can be modified here if needed. (Use the button on the right to reload them if needed.)
>
> Separate callers with a comma (no spaces). For example: a,b,c,d,e,f,g,h, etc. or:  †,‡,§,∥,#    or: ✶,☆,✦,✪

When the sequence reaches the end, it starts again. Make sure your font has the symbols you type.

##### Reload footnote callers from Paratext

Button · Regular+ · `btn_resetFNcallers`  
Needs: “Include Footnotes”, “Show Callers in the Text”

> Clicking this button will reload the footnote callers from the Paratext project settings.
>
> If the callers have not been defined in the Paratext project, or are already showing, then a default set will appear.

PTXprint's own default sequence is `a,b,c,d,e,f,✶,☆,✦,✪,†,‡,§`.

##### Override hidden/automatic Footnote caller settings

Checkbox, off · Regular+ · `c_fnOverride` · cfg `notes/fnoverride`  
Also: Override Footnote Settings in Text · Needs: “Include Footnotes”

> The Footnotes specified in Paratext use  
> \f +(plus) to cycle through the callers, or \f - (minus) to omit the caller.
>
> If this option is enabled, the Show Callers settings below will override whatever has been specified within the text itself.

Use this when the callers in the PDF do not follow your settings. PTXprint changes every footnote to `\f +` if **Show Callers** is ticked, or to `\f -` if it is not.

##### Start Each Footnote on a New Line

Checkbox, off · Basic+ · `c_fneachnewline` · cfg `notes/fneachnewline`  
Needs: “Include Footnotes”

> Normally footnotes are arranged one after the other to form a block of text. But if you require each footnote to start on its own new line then set this option.

This uses more space than run-on notes. When both this and **Start Each Cross-Reference on a New Line** are ticked, the horizontal spacing settings are greyed out, because they are only used for run-on notes.

##### \f

Link · Regular+ · `lb_style_f`  
Needs: “Include Footnotes”

> Click to edit the Footnote properties on the Styles tab.

Change the font size, line spacing and other footnote properties there.

##### End of Book

Radio · Regular+ · `r_fnpos_endnote` · cfg `notes/fnpos=endnote`, `notes/columnnotes_=endnote`, `notes/endnotes_=endnote`, `notes/fnmarginal_=endnote`  
Also: Placement of footnotes: End notes · Needs: “Include Footnotes”

> This option will prevent footnotes showing on each page, but will gather them together and place them all at the end of the book.

Use this when there are few notes or when you want clean pages.

##### End of Column

Radio · Regular+ · `r_fnpos_column` · cfg `notes/fnpos=column`, `notes/columnnotes_=column`, `notes/endnotes_=column`, `notes/fnmarginal_=column`  
Also: Placement of footnotes: End of column · Needs: “Two Column Layout”, “Include Footnotes”

> Use this option (only available in 2-column layout) to show the footnotes at the end of the 2nd column of text.
>
> Footnotes and cross-references at the foot of the page are kept together, so changing this may also change where the cross-references are placed.

The notes are set at the width of one column. If cross-references are at **End of Page**, they also move to **End of Column**.

##### End of Page

Radio · Regular+ · `r_fnpos_normal` · cfg `notes/fnpos=normal`, `notes/columnnotes_=normal`, `notes/endnotes_=normal`, `notes/fnmarginal_=normal`  
Also: Placement of footnotes: End of page · Needs: “Include Footnotes”

> Footnotes (and cross-references) are usually placed at the end of each page.

The usual choice. If cross-references are at **End of Column**, they move to **End of Page** too.

##### Include Footnotes

Checkbox, on · Basic+ · `c_includeFootnotes` · cfg `notes/includefootnotes`

> Select whether footnotes should be included.
>
> The specific settings for these are located on the Footnotes tab.

Unticked, all footnotes are left out of the PDF. They stay in your Paratext project. Most footnote settings are then greyed out. Cross-references set to **Below Footnotes** or **Blend with Footnotes** move to another placement.

##### Only show verse numbers from \fr

Checkbox, off · Regular+ · `c_frVerseOnly` · cfg `notes/frverseonly`

> The footnote reference \fr usually includes the chapter & verse number like this 3:16. If you prefer to hide the chapter, so that only 16 is shown, then enable this option.

This saves space, because the chapter is usually clear from the page.

##### Side Margin

Radio · Regular+ · `r_fnpos_margin` · cfg `notes/fnpos=margin`, `notes/columnnotes_=margin`, `notes/endnotes_=margin`, `notes/fnmarginal_=margin`  
Also: Placement of footnotes: Side Margin · Needs: “Margin Notes Col Width (mm)”

> This option will place footnotes (and optionally also the Cross-references and Section Headings) in a column next to the text and align them as closely as possible vertically to their caller.
>
> This option is only available if Margin Notes has been enabled on the Layout Tab.

If you turn margin notes off, the footnotes go back to **End of Page**.

##### Rule and Space Settings

###### Space Above Rule (pt) – Space above footnote rule

Number · Regular+ · `s_fnAboveSpace` · cfg `notes/abovenotespace`  
Values: -50–50 (default 6)

> The vertical space between the main text body and the footnote rule.
>
> Note: if you make this value less than the descenders of the last lines of text, then the footnotes will push down into the footer area. If you see this happening, increase this value to trigger an earlier page break to solve the problem.
>
> The vertical space between the body text and the area containing footnotes and cross-references.
>
> If the Footnote Rule is not shown, the vertical space will still be calculated as the Space Above plus the Space Below (the imaginary) Rule.

Also increase it if the notes look too close to the text. Negative values are possible but rarely useful.

###### Space Below Rule (pt) – Space below footnote rule

Number · Regular+ · `s_fnBelowSpace` · cfg `notes/belownoterulespace`  
Values: -50–50 (default 2) · Needs: “Show Footnote Rule”

> This is the vertical space/gap (pts) between the rule and the footnotes.

PTXprint adds this space even when the rule is hidden.

###### Show Footnote Rule

Checkbox, on · Regular+ · `c_footnoterule` · cfg `notes/iffootnoterule`

> This is the horizontal rule separating the body text from the footnote area.

This rule is also used above cross-references at the bottom of the page. Untick it for a cleaner look. The space above and below is kept.

###### Rule Positioning and Parameters – Footnote rule: Indent

Number · Full · `s_fnIndent` · cfg `notes/fnruleindent`  
Needs: “Show Footnote Rule”

> Distance (mm) to move the rule in from the side chosen in Horizontal Position.

Use 0 for no indent.

###### Rule Positioning and Parameters – Footnote rule: Length

Number · Full · `s_fnLength` · cfg `notes/fnrulelength`  
Values: 20–100 (default 100) · Needs: “Show Footnote Rule”

> The length of the rule as a percentage of the column/page width.

Short rules of 20 to 40 are common in books.

###### Rule Positioning and Parameters – Footnote rule: Line Thickness

Number · Full · `s_fnThick` · cfg `notes/fnrulethick`  
Values: 0.1–2 (default 0.5) · Needs: “Show Footnote Rule”

> The thickness of the rule.

The value is in pt. Use a smaller value, like 0.3, for a lighter line.

###### Rule Positioning and Parameters – Footnote rule: Horizontal position

Drop-down · Full · `fcb_fnHorizPosn` · cfg `notes/fnruleposn`  
Choices: Left | Right | Inner | Outer | Center · Needs: “Show Footnote Rule”

> Which side of the column the rule is aligned to:  
> Left, Right, Center, Inner (spine side) or Outer. Inner and Outer swap sides on odd and even pages. This only matters when the Length is less than 100%.
>
> These settings control the rule (horizontal line) above the notes: its indent (mm), its length (% of the column width), its thickness (pt) and which side of the column it is aligned to.

Positions a footnote rule that is shorter than 100%.

##### Miscellaneous Footnote Settings

###### Add a Colon ':' After \fq and \xq

Checkbox, off · Full · `c_addColon` · cfg `notes/addcolon`  
Also: Add colon after quoted text in notes

> Some projects prefer to separate the Quoted text from the footnote text with a colon ':' which helps keep the elements visually distinct.

For example "*light*: Or *brightness*". Use it if your team does not type the colon in the notes.

###### Keep Book Names and Refs Together

Checkbox, on · Full · `c_keepBookWithRefs` · cfg `notes/keepbookwithrefs`

> This option inserts a space that discourages line breaks between the book name and the Ch:Vs refs so that they don't get split across lines.
>
> It also prevents single letters being left at the end of a line in note text.
>
> Note:  This setting currently has no effect on cross-references imported from external lists.

For example, "John 3:16" stays on one line.

###### Show All Glossary Entries as Footnotes

Checkbox, off · Full · `c_glossaryFootnotes` · cfg `notes/glossaryfootnotes`

> Glossary entries for ALL marked-up Biblical Terms on each page can be made to appear as footnotes.
>
> Glossary words are marked like \w word\w* in the USFM text file. Only the first paragraph of each glossary entry is used.
>
> This feature is extremely useful when producing printouts for comprehension testing (where  Key Biblical Terms in the passage which have Glossary Entries also need to be checked for understanding).

The entries come from the GLO book. This adds many footnotes.

###### Horizontal Space Separating Notes – Minimum Horizontal Space Separating Notes

Number · Full · `s_notespacingmin` · cfg `notes/horiznotespacemin`  
Values: 2–20 (default 5)

> This spacing is set in points (pts). Changing this will increase or decrease the MINIMUM horizontal space between notes that have been run together.
>
> The horizontal space between notes that are being run together as a single paragraph can be set here. The default space is calculated as 33% between min & max values.
>
> For example if min=6pt and max=15pt then the default horizontal space between notes would be 9pt.
>
> If this control is disabled, it is because both the Footnotes and Cross-References have been set to start on a new line. (see \f and \x settings above).

The maximum must be larger, so PTXprint adjusts **Maximum Space** when you change this.

###### Horizontal Space Separating Notes – Maximum Horizontal Space Separating Notes

Number · Full · `s_notespacingmax` · cfg `notes/horiznotespacemax`  
Values: 5–40 (default 25)

> This spacing is set in points (pts). Changing this will increase or decrease the MAXIMUM horizontal space between notes that have been run together.

PTXprint stretches or shrinks the space to fill lines. A larger range gives PTXprint more freedom.

###### Vertical Space Between Footnotes and xRefs (pt) – Vertical Space Between Footnotes and xRefs

Number · Full · `s_internote` · cfg `notes/internotespace`  
Needs: “Column Cross-References” · Greyed out by: “Blend with Footnotes”

> When Footnotes and Cross-references are not blended together in the same block then the Footnotes appear in one block and the Cross-references in another block just below them. This setting (pts) lets you adjust the vertical space between these two sections.

The default is 3.5.

#### Cross-References

##### End of Book

Radio · Regular+ · `r_xrpos_endnote` · cfg `notes/xrlocation=endnote`, `notes/xrpos=endnote`, `notes/xrmarginal_=endnote`  
Also: Placement of cross-references: As End Notes

> This option will prevent cross-references showing on each page, but will gather them together and place them all at the end of the book.

Collected and printed at the end of each book.

##### End of Column

Radio · Regular+ · `r_xrpos_column` · cfg `notes/xrlocation=column`, `notes/xrpos=column`, `notes/xrmarginal_=column`  
Also: Placement of cross-references: End of column

> Use this option (only available in 2-column layout) to show the cross-references at the end of the 2nd column of text.
>
> Footnotes and cross-references at the foot of the page are kept together, so changing this may also change where the footnotes are placed.

Needs a two-column layout. If footnotes are at **End of Page**, they also move to **End of Column**.

##### End of Page

Radio · Regular+ · `r_xrpos_normal` · cfg `notes/xrlocation=normal`, `notes/xrpos=normal`, `notes/xrmarginal_=normal`  
Also: Placement of cross-references: End of page

> Cross-references are usually placed at the end of each page.

If footnotes are at **End of Column**, they move to **End of Page** too.

##### Start Each Cross-Reference on a New Line

Checkbox, off · Basic+ · `c_xreachnewline` · cfg `notes/xreachnewline`

> Normally cross-references are arranged one after the other to form a block of text. But if you require each cross-reference to start on its own new line then set this option.

This uses more space than run-on notes. When both this and **Start Each Footnote on a New Line** are ticked, the horizontal spacing settings on the **Footnotes** sub-tab are greyed out.

##### Override hidden/automatic Cross-reference caller settings

Checkbox, off · Regular+ · `c_xrOverride` · cfg `notes/xroverride`  
Also: Override Cross-Reference Settings in Text

> Cross-references specified in Paratext use  
> \x +(plus) to cycle through the callers, or \x - (minus) to omit the caller.
>
> If this option is enabled, the Show Callers settings below will override whatever has been specified within the text itself.

PTXprint uses `\x +` for every cross-reference if **Show Callers** is ticked, and `\x -` (no caller) if it is not.

##### Show Callers in the Text

Checkbox, on · Regular+ · `c_xrautocallers` · cfg `notes/ifxrautocallers`  
Also: Show Cross-Reference Callers in the Text

> A "Caller" is a symbol (in the text) which alerts the reader that there is further information (in this case a cross-reference at the bottom of the page). Some people prefer not to indicate cross-references in the text itself, but just to include them at the bottom of the page.
>
> Separate callers with a comma (no spaces). For example: a,b,c,d,e,f,g,h, etc. or:  †,‡,§,∥,#    or: ✶,☆,✦,✪
>
> If you do not see the callers you are expecting in the PDF, then try using the "Override..." setting above.

To show no cross-reference callers in the text at all, untick this and tick **Override…**.

##### Cross-Reference Caller Sequence Entry

Text box · Regular+ · `t_xrcallers` · cfg `notes/xrcallers`  
Needs: “Show Callers in the Text”

> These callers should automatically be loaded from the settings in the Paratext project, but can be modified here if needed. (Use the button on the right to reload them if needed.)
>
> Separate callers with a comma (no spaces). For example: a,b,c,d,e,f,g,h, etc. or:  †,‡,§,∥,#    or: ✶,☆,✦,✪

Choose marks that are different from the footnote callers, so readers can tell the two kinds of notes apart.

##### Reload cross-reference callers from Paratext

Button · Regular+ · `btn_resetXRcallers`  
Needs: “Show Callers in the Text”

> Clicking this button will reload the cross-ref callers from the Paratext project settings.
>
> If the callers have not been defined in the Paratext project, or are already showing, then a default set will appear.

PTXprint's default sequence is `†,‡,§,∥,#`.

##### Show Callers in Notes Area

Checkbox, on · Regular+ · `c_xromitcaller` · cfg `notes/xromitcaller`  
Also: Show cross-reference callers in notes area · Needs: “Show Callers in the Text”

> Usually the "Caller" symbol is also shown in the notes area which helps the reader quickly find the cross-reference from the text.

Untick it to save a little space.

##### Reset Callers on Page

Checkbox, on · Regular+ · `c_xrpageresetcallers` · cfg `notes/xrresetcallers`  
Also: Reset cross-reference callers on each page · Needs: “Show Callers in the Text”

> If this is checked, then the sequence of callers starts again from the 1st item in the list of callers specified.
>
> Note that this feature doesn't always take effect straight away. You may need to hit Print a second time before it applies.

Works like **Reset Callers on Page** for footnotes.

##### \x

Link · Regular+ · `lb_style_x`

> Click to edit the Cross-Reference properties on the Styles tab.

For column cross-references, a small size (about 6 pt) is often needed.

##### Below Footnotes

Radio · Regular+ · `r_xrpos_below` · cfg `notes/xrlocation=below`, `notes/xrpos=below`, `notes/xrmarginal_=below`  
Also: Placement of cross-references: Below footnotes

> Cross-references will be listed in a separate block underneath the footnotes (rather than combined along with the footnotes as a single paragraph).

**Vertical Space Between Footnotes and xRefs** sets the gap between the two blocks.

##### Blend with Footnotes

Radio · Regular+ · `r_xrpos_blend` · cfg `notes/xrlocation=blend`, `notes/xrpos=blend`, `notes/xrmarginal_=blend`  
Also: Placement of cross-references: Blend with footnotes

> To save space in the footnote area, you can combine the  footnotes and cross-references as a single paragraph (rather than the cross- references appearing in a separate block underneath the footnotes). If this option is used, the Cross-References can only have one type of caller (rather than a sequence) which must be specified above.

This saves space. PTXprint sets the `\x` style on the **Styles** tab so that it joins the footnotes.

##### Column Cross-References

Radio · Regular+ · `r_xrpos_centre` · cfg `notes/xrlocation=centre`, `notes/xrpos=centre`, `notes/xrmarginal_=centre`  
Also: Placement of cross-references: Vertical column

> When there are numerous cross-references (usually when using an external list of references) then it may be useful to place them in their own column.
>
> The cross references will appear in a narrow vertical column similar to a study/reference Bible layout.

With a two-column layout the column is between the text columns. With one column, choose the side in **Side of page**. Choosing this sets footnotes to **End of Column** and opens the **Source for References** area. Set the width and other settings in the **Column Cross-References** area.

##### Use External List of Cross-References

Checkbox, off · Full · `c_useXrefList` · cfg `notes/ifxrexternalist`

> Instead of using a handful of cross-references as specified within the project's USFM text, you can select an external list containing many 1000's of cross-references. These will automatically be localized into the project's language using the  
> \toc3 values specified in the Paratext project settings (See: Scripture reference settings...)
>
> This feature is usually used for Study or Reference Bibles in conjunction with the 'Column Cross-References' placement option.

The list can also be your own file. Choose it in **Source for References**. The added references have no caller in the text. When ticked, the **Cross-References** sub-tab name is highlighted.

##### Show Extended Cross-References

Checkbox, off · Full · `c_extendedXrefs` · cfg `notes/showextxrefs`

> Study Bibles can (optionally) use extended cross-references (\ex) which can be displayed along with other kinds of cross-references.

When it is not ticked, PTXprint removes all `\ex ... \ex*` notes.

##### Include Cross-References (From Project Text)

Checkbox, on · Basic+ · `c_includeXrefs` · cfg `notes/includexrefs`  
Also: Include cross-references (from project)

> Select whether cross-references from the project's text should be included.
>
> The specific settings for these are located on the Cross-References tab.

This does not affect cross-references from an external list.

##### Only show verse numbers from \xo

Checkbox, off · Regular+ · `c_xoVerseOnly` · cfg `notes/xrverseonly`

> The cross-reference origin \xo usually includes the chapter & verse number like this 3:16. If you prefer to hide the chapter, so that only 16 is shown, then enable this option.

This also applies to cross-references from external lists. For a bridged verse (two or more verses joined), the whole range is shown, for example `13-14`.

##### Side Margin

Radio · Regular+ · `r_xrpos_margin` · cfg `notes/xrlocation=margin`, `notes/xrpos=margin`, `notes/xrmarginal_=margin`  
Also: Placement of cross-references: Side Margin · Needs: “Margin Notes Col Width (mm)”

> This option will place references (and optionally also the Footnotes and Section Headings) in a column next to the text and align them as closely as possible vertically to their caller.
>
> This option is only available if Margin Notes has been enabled on the Layout Tab.

If you turn margin notes off, the cross-references go back to **End of Page**.

##### Source for References

###### Include Refs for Books in – Include references for which category of books

Drop-down · Full · `fcb_filterXrefs` · cfg `notes/xrfilterbooks`  
Choices: Whole Bible | Paratext Project | This Publication | New Testament | Old Testament · Needs: “Use External List of Cross-References”

> The various cross-reference lists often contain hundreds of 1000s of references. You may want to only include target references that are currently available to your readers by selecting a subset of Biblical books.
>
> So for example, if there is no Old Testament yet, you may want to only include target cross-references to NT Books.
>
> If you select Books in "This Publication", then only cross-references targeting books in the "Portions or Multiple Books" list on the Basic tab will be included.

* **Whole Bible** – keep all references.
* **Paratext Project** – only books that exist in the project.
* **This Publication** – only the books in the list of books to print (**Basic** tab, **What to Print** area).
* **New Testament** or **Old Testament** – only that part of the Bible.

###### External Refs – Select external list of cross-references

Drop-down · Full · `fcb_xRefExtListSource` · cfg `notes/xrlistsource`, `notes/xrextlistsource`  
Choices: Standard list (fewest) | Standard list (fewer) | Standard list | Standard list (more) | Standard list (most) | Strong's list (all) | Strong's list (project) | TSK list | BibleWorks™ list | UBS GNT92 list | UBS GNT92 list (DC) | Select a Custom list... · Needs: “Use External List of Cross-References”

> There are multiple options to choose from if you wish to use an external list of cross-references. Select whichever is most appropriate and the list will automatically be localized to use the abbreviated book names as defined in Paratext's Scripture Reference Settings which should match the \toc3 markers.
>
> The five Standard list sizes take fewer or more references from the same prioritized list (fewest = only the most important ones).

The **Strong's** lists group references by Hebrew and Greek word, and make the **Strong's References** settings available. **Select a Custom list...** makes the **Select...** button available. Larger lists need more space on the page and take longer to process. See **Source for References** above for each list.

###### Select...

Button · Full · `btn_selectXrFile` · cfg `project/selectxrfile`  
Also: Select a custom cross-reference list · Needs: “Use External List of Cross-References”

Chooses your own cross-reference file. It starts in the Paratext `_Cross References` folder. PTXprint can read `.xrf` (the Paratext cross-reference format), `.xre` and `.xml` files. Only available when **External Refs** is **Select a Custom list...**. After you choose a file, hover over the button to see the file name.

###### Standard

Radio · Full · `r_xrSource_standard`  
Also: Source of cross-references: Standard list · Needs: “Use External List of Cross-References”

> The Standard List contains more than 340,000 cross-references which have been prioritized by crowd-sourcing.

Not shown on screen. Its text is the description of the **Standard list** shown by the information button. Choose the list in **External Refs**.

###### Strongs

Radio · Full · `r_xrSource_strongs`  
Also: Source of cross-references: Strong's list · Needs: “Use External List of Cross-References”

> The Strong's List contains a curated subset of cross-references generated from the Strong's Numbers. Optionally an index for these numbers can also be created as an additional book that can be appended to the publication.
>
> Each set of cross-references is indexed by a Hebrew or Greek Strong's number which can be looked up in the (optional) Index which can be generated using the "Generate Index..." button.

Not shown on screen. Its text is the description of the **Strong's** lists shown by the information button. Choose the list in **External Refs**.

###### TSK

Radio · Full · `r_xrSource_tsk`  
Also: Source of cross-references: Treasury of Scripture Knowledge · Needs: “Use External List of Cross-References”

> For generations, the Treasury of Scripture Knowledge has been an enduring cross-reference resource for Bible students worldwide. This highly respected and nearly exhaustive compilation of cross-references was developed by R.A. Torrey from references in the Rev. Thomas Scott's Commentary and the Comprehensive Bible. With nearly 500,000 cross-references it is the most thorough source available.

Not shown on screen. Its text is the description of the **TSK list** shown by the information button. Choose the list in **External Refs**.

###### BibWrx

Radio · Full · `r_xrSource_works`  
Also: Source of cross-references: The Works · Needs: “Use External List of Cross-References”

> The BibleWorks list contains 112,000 cross-references which were formerly part of the BibleWorks software which has been discontinued.

Not shown on screen. Its text is the description of the **BibleWorks™ list** shown by the information button. Choose the list in **External Refs**.

###### UBS

Radio · Full · `r_xrSource_ubs`  
Also: Source of cross-references: UBS GNT92 list · Needs: “Use External List of Cross-References”

> This list contains New Testament and Old Testament references (NO Deuterocanonical  references). Short Bible Reference System, edited by Robert G. Bratcher, (c) 1961 United Bible Societies. This list was used in GNT92. Organizations that have a Paratext license may use this list in their publication without attribution or notifying UBS. All other rights to use this list are reserved.
>
> Use the (DC) list if Deutero Canonical references are needed.

Not shown on screen. Its text is the description of the **UBS GNT92** lists shown by the information button. Choose the list in **External Refs**.

###### Custom

Radio · Full · `r_xrSource_custom`  
Also: Source of cross-references: Custom .xrf list · Needs: “Use External List of Cross-References”

> You can select a specially-curated list of cross-references. For example, it is possible to extract cross-references from another project (in the .xrf file format) to be included here. There is also an .xre format (extended .xrf) and an .xml format which can be used as external cross-references. These formats are explained in the documentation. See the PTXprint documentation (xrefs.md).

Not shown on screen. Its text is the description of a custom list shown by the information button. To use your own list, choose **Select a Custom list...** in **External Refs** and click **Select...**.

###### Hover here to read about the selected cross-reference list.

Button · Full · `btn_infoXrefSource`  
Needs: “Use External List of Cross-References”

> Hover here to read about the selected cross-reference list.

The description gives the size of the list chosen in **External Refs**, where it comes from and any copyright notes.

##### Source for References › Strong's References

###### Show Numbers in the Text

Checkbox, off · Full · `c_strongsShowInText` · cfg `strongsndx/showintext`  
Also: Show Strong's numbers in the text · Needs: “Use External List of Cross-References”

> If the project's Biblical Terms list includes renderings, then it is possible to show Strong's numbers in the text itself, which should make it easier to look up the appropriate cross-references for a word in a Study Bible.
>
> Note that this option is disabled by default as it can clutter the scripture text and will also slow down the production of the PDF.

Uses your project's Biblical Terms renderings. Only for the Strong's lists. It makes the PDF much slower to produce. PTXprint keeps each number on the same line as the word after it, so a number is never left alone at the end of a line. The same text and settings always give the same numbers in the same places, so two PDFs made from the same text can be compared.

###### Show Numbers in Cross-References

Checkbox, on · Full · `c_strongsShowNums` · cfg `strongsndx/shownums`  
Also: Show Strong's numbers in cross-references · Needs: “Use External List of Cross-References”

> If you are generating a localized Strong's index, then it is highly recommended to include the Strong's numbers in the list of cross-references in the text.
>
> But if you only want to show the references without any Strong's numbers, then uncheck this option for a more compact list.

Shows the number in front of each group of references.

###### Generate Index...

Button · Full · `btn_strongsGenerate`  
Also: Generate Index (based on Strong's numbers) · Needs: “Use External List of Cross-References”

> For Strong's Cross References to be most useful, it is recommended to include an Index at the end of the publication. Click this button to set various options to be used to generate the index.

Only available for the Strong's lists. See "Generate Strong's Index dialog" above.

###### Show All Occurrences

Checkbox, off · Full · `c_strongsShowAll` · cfg `strongsndx/showall`  
Also: Show Strong's numbers on every occurrence of a word · Needs: “Show Numbers in the Text”, “Use External List of Cross-References”

> If a particular word occurs more than once in the given verse, each occurrence will be tagged with the Strong's number. If a word matches more than one Strong's number then both will be displayed.
>
> This may be rather confusing for the reader, but could be helpful for a consultant to easily identify overlap issues with the project's Biblical terms renderings.

Meant for a consultant who checks the renderings, rather than for readers.

###### \xts

Link · Full · `lb_style_xts`  
Needs: “Use External List of Cross-References”

> Click to edit the Strong's 4 digit cell number properties on the Styles tab.

The `\xts` style controls how the Strong's numbers look in the cross-references.

##### Source for References › Column Cross-References

###### Column Width (pts) – Column width of column-based cross-references

Number · Full · `s_centreColWidth` · cfg `notes/xrcentrecolwidth`  
Values: 30–150 (default 60) · Needs: “Column Cross-References”

> This sets the width of the centre column in points. Note that 72pts is 1 inch, and increasing the size here will decrease the amount of space available for the 2 columns of scripture text.
>
> Consider using a larger page size if you want to use Centre Column xRefs.
>
> If this centre column isn't wide enough to fit the references, then you should also consider reducing the size of the \x font (to approx 6pt).

If the references do not fit, make the `\x` font smaller rather than the column much wider.

###### Gutter Width (pts) – Gutter width of column-based cross-references

Number · Full · `s_xrGutterWidth` · cfg `notes/xrguttermargin`  
Values: 0.1–20 (default 2) · Needs: “Column Cross-References”

> This sets the space between the main body text and the column of cross-references.

In pt.

###### Side of page – Position of column-based cross-references

Drop-down · Full · `fcb_colXRside` · cfg `notes/xrcolside`  
Choices: Left | Right | Inner | Outer · Needs: “Column Cross-References” · Greyed out by: “Two Column Layout”

> Select where the column of cross-references should be located on the page. Note that the 2-column layout insists on the cross-references being positioned between the columns of text.

For a one-column layout only. **Inner** is near the spine, **Outer** is away from it.

###### Vertical Rule(s) Between Columns

Checkbox, on · Full · `c_xrColumnRule` · cfg `notes/xrcolrule`  
Also: Include a vertical rule between columns · Needs: “Column Cross-References”

> Check this option to include a vertical line separating the text and cross-references.

Draws a thin vertical line.

###### Fill Upward From Bottom of Column

Checkbox, off · Full · `c_xrColumnBottom` · cfg `notes/xrcolbottom`  
Also: Fill cross-references upward from bottom of column · Needs: “Column Cross-References”

> If there are only a small number of cross-references, it may appear better for them to be placed nearer the end (or bottom) of the page. Check this option if you prefer the references to fill the column upward from the end of the page.

Places the references at the bottom of the column instead of the top.

###### Side Align Notes

Checkbox, off · Full · `c_xrSideAlign` · cfg `notes/xrcolalign`  
Also: Align notes to the edge of the main text · Needs: “Column Cross-References”

> For side column notes, should the text of the notes align to the edge of the main text?

When not ticked, the text aligns to the edge of the column.

##### Rule and Space Settings

###### Show Cross-Reference Rule

Checkbox, on · Regular+ · `c_xrefrule` · cfg `notes/ifxrefrule`

> This is the horizontal rule separating the body text from the cross-reference area. (Used only when footnotes or cross-references are placed at the End of Book. Otherwise the Footnote rule settings apply.)

To hide the rule above the bottom-of-page notes, untick **Show Footnote Rule** on the **Footnotes** sub-tab.

###### Space Above Rule (pt) – Space above cross-reference rule

Number · Regular+ · `s_xrAboveSpace` · cfg `notes/abovexrefspace`  
Values: -50–50

> The vertical space between the main text body and the cross-reference rule. (Used only when footnotes or cross-references are placed at the End of Book. Otherwise the Footnote rule settings apply.)
>
> The vertical space between the body text and the area containing cross-references.
>
> If the Cross-Reference Rule is not shown, the vertical space will still be calculated as the Space Above plus the Space Below (the imaginary) Rule.

In other cases, change **Space Above Rule** on the **Footnotes** sub-tab.

###### Space Below Rule (pt) – Space below cross-reference rule

Number · Regular+ · `s_xrBelowSpace` · cfg `notes/belowxrefrulespace`  
Values: -50–50 · Needs: “Show Cross-Reference Rule”

> This is the vertical space/gap (pts) between the rule and the cross-references. (Used only when footnotes or cross-references are placed at the End of Book. Otherwise the Footnote rule settings apply.)

Used only at **End of Book**.

###### Rule Positioning and Parameters – Cross-reference rule: Indent

Number · Full · `s_xrIndent` · cfg `notes/xrruleindent`  
Needs: “Show Cross-Reference Rule”

> Distance (mm) to move the rule in from the side chosen in Horizontal Position. (Used only when footnotes or cross-references are placed at the End of Book. Otherwise the Footnote rule settings apply.)

Works like **Indent** for the footnote rule. Used only at **End of Book**.

###### Rule Positioning and Parameters – Cross-reference rule: Length

Number · Full · `s_xrLength` · cfg `notes/xrrulelength`  
Values: 20–100 · Needs: “Show Cross-Reference Rule”

> The length of the rule as a percentage of the column/page width. (Used only when footnotes or cross-references are placed at the End of Book. Otherwise the Footnote rule settings apply.)

Works like **Length** for the footnote rule. Used only at **End of Book**.

###### Rule Positioning and Parameters – Cross-reference rule: Thickness

Number · Full · `s_xrThick` · cfg `notes/xrrulethick`  
Values: 0.1–2 · Needs: “Show Cross-Reference Rule”

> The thickness of the rule. (Used only when footnotes or cross-references are placed at the End of Book. Otherwise the Footnote rule settings apply.)

In pt. Used only at **End of Book**.

###### Rule Positioning and Parameters – Cross-reference rule: Horizontal position

Drop-down · Full · `fcb_xrHorizPosn` · cfg `notes/xrruleposn`  
Choices: Left | Right | Inner | Outer | Center · Needs: “Show Cross-Reference Rule”

> Which side of the column the rule is aligned to:  
> Left, Right, Center, Inner (spine side) or Outer. Inner and Outer swap sides on odd and even pages. This only matters when the Length is less than 100%. (Used only when footnotes or cross-references are placed at the End of Book. Otherwise the Footnote rule settings apply.)
>
> These settings control the rule (horizontal line) above the notes: its indent (mm), its length (% of the column width), its thickness (pt) and which side of the column it is aligned to.

Positions a cross-reference rule that is shorter than 100%. Used only at **End of Book**.

#### Study Notes + Questions

##### Extended Footnotes (\ef)

Checkbox, off · Full · `c_extendedFnotes` · cfg `studynotes/includextfn`  
Also: Use extended/study footnotes

> Extended Footnotes are the primary means for displaying study notes. These are similar to ordinary footnotes but appear as a 2-column block at the end of each page.

When it is not ticked, PTXprint removes all `\ef` notes from the text before making the PDF. Ticking it shows the layout and rule settings for study notes.

##### Sidebars (\esb ... \esbe)

Checkbox, off · Regular+ · `c_sidebars` · cfg `studynotes/includesidebar`  
Also: Include study note sidebars (\esb)

> Sidebars (\esb ... \esbe) are used to contain larger blocks of topic-specific information.

When it is not ticked, PTXprint removes them. Their appearance is set on the **Styles** tab.

##### Include Transcelerator Questions

Checkbox, off · Basic+ · `c_txlQuestionsInclude` · cfg `studynotes/txlinclquestions`  
Also: Include (Transcelerator) Checking Questions

> Use this option to include questions which have been created with SIL's Transcelerator tool for the purpose of comprehension testing.
>
> These will be displayed at the bottom of the page in the area normally used for Study Notes.
>
> Note that this option is only made available if the Transcelerator plugin's data folder for the project can be located.

Each question is printed near the verse it asks about. Ticking it shows the question settings and an example.

##### Extended Footnotes (\ef)

###### Gutter Width (mm) – Gutter width between columns of extended notes

Number · Full · `s_ef_colgutterfactor` · cfg `studynotes/colgutterfactor`  
Values: 1–40 · Needs: “Extended Footnotes (\ef)” · Hidden until: “Extended Footnotes (\ef)”

> This is the space between the text of the two columns (measured in millimeters).
>
> This is the space (mm) between the text of the two columns.

A larger value makes the notes easier to read but uses more space.

###### Unbalanced Lines (max) – Allow N unbalanced lines in extended notes

Number · Full · `s_ef_bottomRag`  
Needs: “Extended Footnotes (\ef)” · Hidden until: “Extended Footnotes (\ef)”

> PTXprint will attempt to balance the number of lines in each column of the extended notes. Sometimes this results in wasted empty space. Increasing this number (recommended range 1-4) will allow up to that many unbalanced lines in the extended notes area.
>
> By default (when this is set to 0) PTXprint will balance the number of lines used in each column. Sometimes this results in large empty spaces at the end of a page.
>
> Increasing this number (recommended range 1-4) will allow up to that many unbalanced lines on the page. Note that you can still stretch/shrink paragraphs using AdjLists to refine the output by manually balancing pages.

This setting is always greyed out in this version, so you cannot change it.

###### Vertical Space Between Notes – Vertical space between extended/study notes

Number · Full · `s_ef_internote` · cfg `studynotes/internote`  
Values: -20–20 · Needs: “Extended Footnotes (\ef)” · Hidden until: “Extended Footnotes (\ef)”

> This setting (pts) lets you adjust the vertical space between extended footnotes. Usually there is no space between them.

A small value such as 1 or 2 can make separate notes easier to see.

###### Vertical Rule in Gutter

Checkbox, off · Full · `c_ef_verticalrule` · cfg `studynotes/ifverticalrule`  
Also: Vertical rule in study notes area gutter · Needs: “Extended Footnotes (\ef)” · Hidden until: “Extended Footnotes (\ef)”

> Check this option to include a center line between the two columns.

When ticked, **Adjust Top (pt)** becomes available.

###### Adjust Top (pt)

Number · Full · `s_ef_colgutteroffset` · cfg `studynotes/colgutteroffset`  
Values: -50–50 · Needs: “Vertical Rule in Gutter”, “Extended Footnotes (\ef)” · Hidden until: “Extended Footnotes (\ef)”

> This setting raises (using a negative value) or lowers (using a positive value) the starting point of the vertical rule between columns (pt).
>
> This setting raises (using a negative value) or lowers (using a positive value) the starting point of the vertical rule between columns.

Moves only the top end of the line.

###### Show Note Callers

Checkbox, off · Full · `c_ef_showCallers` · cfg `studynotes/showcallers`  
Also: Show study note callers in notes area · Needs: “Extended Footnotes (\ef)” · Hidden until: “Extended Footnotes (\ef)”

> Show callers for extended (study) notes, both in the text and in the notes area. A caller alerts the reader that there is further information (in this case an extended footnote) at the end of the page. As a Study Bible has many such notes, this option is normally turned off for extended footnotes. Note that currently only a,b,c...x,y,z callers are possible for this option.

When not ticked, PTXprint removes the callers of all study notes, even if the text asks for them.

##### Extended Footnotes (\ef) › Rule and Space Settings

###### Rule Positioning and Parameters – Study note rule: Indent

Number · Full · `s_snIndent` · cfg `notes/snruleindent`  
Hidden until: “Extended Footnotes (\ef)”

> Distance (mm) to move the rule in from the side chosen in Horizontal Position.

In mm.

###### Rule Positioning and Parameters – Study note rule: Length

Number · Full · `s_snLength` · cfg `notes/snrulelength`  
Values: 20–100 (default 100) · Hidden until: “Extended Footnotes (\ef)”

> The length of the rule as a percentage of the column/page width.

100 is a full-width line.

###### Rule Positioning and Parameters – Study note rule: Thickness

Number · Full · `s_snThick` · cfg `notes/snrulethick`  
Values: 0.1–2 (default 0.5) · Hidden until: “Extended Footnotes (\ef)”

> The thickness of the rule.

In pt.

###### Rule Positioning and Parameters – Study note rule: Horizontal position

Drop-down · Full · `fcb_snHorizPosn` · cfg `notes/snruleposn`  
Choices: Left | Right | Inner | Outer | Center · Hidden until: “Extended Footnotes (\ef)”

> Which side of the column the rule is aligned to:  
> Left, Right, Center, Inner (spine side) or Outer. Inner and Outer swap sides on odd and even pages. This only matters when the Length is less than 100%.
>
> These settings control the rule (horizontal line) above the notes: its indent (mm), its length (% of the column width), its thickness (pt) and which side of the column it is aligned to.

Positions a study-note rule that is shorter than 100%.

###### Show Study Note Rule

Checkbox, on · Full · `c_studynoterule` · cfg `notes/ifstudynoterule`  
Hidden until: “Extended Footnotes (\ef)”

> This is the horizontal rule separating the body text from the study notes area.

It sits between the ordinary notes (or the text) and the study notes area.

###### Space Above Rule (pt) – Space above study note rule

Number · Full · `s_snAboveSpace` · cfg `notes/abovestudyspace`  
Values: -50–50 (default 6) · Hidden until: “Extended Footnotes (\ef)”

> The vertical space between the main text body and the study note rule.
>
> Note: if you make this value less than the descenders of the last lines of text, then the study notes will push down into the footer area. If you see this happening, increase this value to trigger an earlier page break to solve the problem.
>
> The vertical space between the body text and the area containing study notes.
>
> If the Study Note Rule is not shown, the vertical space will still be calculated as the Space Above plus the Space Below (the imaginary) Rule.

In pt.

###### Space Below Rule (pt) – Space below study note rule

Number · Full · `s_snBelowSpace` · cfg `notes/belowstudyrulespace`  
Values: -50–50 (default 2) · Hidden until: “Extended Footnotes (\ef)”

> This is the vertical space/gap (pts) between the rule and the study notes.

In pt.

##### Include Transcelerator Questions

###### Language Code

Text box · Basic+ · `t_txlQuestionsLang` · cfg `studynotes/txllangtag`  
Needs: “Include Transcelerator Questions” · Hidden until: “Include Transcelerator Questions”

> Enter the language code for the questions to be included. Usually this will be a 3-letter Ethnologue code (but other language tags such as en-US, fr, es are also acceptable).

PTXprint fills this in from the Paratext project's language code when it is empty. It must match the language the questions were translated into in Transcelerator. Questions with no translation in this language are not printed.

###### Show Overview Questions

Checkbox, off · Basic+ · `c_txlQuestionsOverview` · cfg `studynotes/txloverview`  
Also: Transcelerator: Show overview questions · Needs: “Include Transcelerator Questions” · Hidden until: “Include Transcelerator Questions”

> Overview questions are designed to test the general understanding of the passage.

Overview questions ask about a whole passage rather than one verse.

###### Number the Questions

Checkbox, on · Basic+ · `c_txlQuestionsNumbered` · cfg `studynotes/txlnumbered`  
Also: Transcelerator: Number the questions · Needs: “Include Transcelerator Questions” · Hidden until: “Include Transcelerator Questions”

> This option enables the questions to be numbered sequentially for each book.

This makes it easy to talk about a question during testing.

###### Include Chapter:Verse References

Checkbox, off · Basic+ · `c_txlQuestionsRefs` · cfg `studynotes/txlshowrefs`  
Also: Transcelerator: Include ch:vs references · Needs: “Include Transcelerator Questions” · Hidden until: “Include Transcelerator Questions”

> This option enables the questions to include the chapter:verse numbers.
>
> If the questions are also being numbered then the reference will be shown in parentheses (ch:vs).

For example `3:25`, or `13. (3:25)` when the questions are numbered.

###### \ef

Link · Full · `lb_style_ef`  
Needs: “Include Transcelerator Questions” · Hidden until: “Include Transcelerator Questions”

> Click to edit the Extended Footnote properties on the Styles tab.
>
> The line spacing factor will modify the space between the questions.

The `\ef` style controls how study notes and Transcelerator questions look.

##### Filter Categories › Filter Categories

###### tv_sbCatEdit

Table · Full · `tv_sbCatEdit`  
Needs: “Filter Categories”

The categories found in the project's study notes and sidebars, with a tick box for **Extended Footnote (\ef)** and one for **Sidebar (\esb)**. In this version, PTXprint does not save this list and does not use it when it makes the PDF.

###### Add

Button · Full · `b_sb_addcat`  
Also: Add sidebar category to filter · Needs: “Filter Categories”

> Add a new Category.

Type its name in the box that opens.

###### Del

Button · Full · `b_sb_delcat`  
Also: Delete sidebar category from filter · Needs: “Filter Categories”

> Delete the currently selected Category.

Removes the selected category.

###### ↺

Button · Full · `btn_sb_rescanCats`  
Also: Rescan categories to filter sidebars · Needs: “Filter Categories”

> Clicking this button will rescan the project to add any Categories missing from this list.

Searches all books for `\cat ... \cat*` and fills the list again. The list is also filled when you first tick **Filter Categories**.

##### Filter Categories

###### Filter Categories

Checkbox, off · Full · `c_filterCats` · cfg `studynotes/filtercats`  
Also: Filter study note sidebars

> Use this option to restrict certain categories of extended study notes and sidebars from being displayed.

Shows the category list. If the list is empty, PTXprint searches the project for categories. In this version, the filter does not change the PDF.


# 9. Header+Footer tab

## 9.1 What this tab is for

The **Header+Footer** tab decides what is printed in the running header (the line at the top of
each page) and the footer (the line at the bottom). Come here to:

* choose where the page number goes;
* show the references on each page (for example "Matthew 5:3–6:2");
* add a "DRAFT" message, a date or the time;
* choose the page number that the first Scripture book starts with;
* choose what is printed at the bottom of the first page of each book.

The **position** of the header and footer, the rule (line) under the header, and mirrored pages
are set on the **Layout** tab. The font and size of the header text are set by the `\h` style on the
**Styles** tab (click the **\h** link on this tab).

## 9.2 Header

The header has three places: **Inner (Left)**, **Center** and **Outer (Right)**. Each has a
drop-down list: choose a ready-made item or type your own text.

The ready-made items are:

* **-empty-** – nothing.
* **Page Number**.
* **First Reference** – the first verse on the page, for example "John 3:1".
* **Last Reference** – the last verse on the page.
* **Reference Range** – first and last verse together, for example "John 3:1–4:5".
* **Book (\h)** – the book name from the book's `\h` line.
* **Book Alt (\h1)** – the book name from the `\h1` line, if the book has one.
* **Time (HH:MM)**, **Date (YYYY-MM-DD)**, **Date and Time** (for example "2026-10-17 14:52") and
  **Printed on YYYY-MM-DD** (the words "Printed on" and the date) – the time and/or date of printing.
  They are in all three places (and in the footer), and are useful for drafts.

### Mirrored headers

**Mirror Pages** (**Layout** tab, **Page Setup** area) changes how the three places are used.

* **Mirror Pages ticked** (usual for a printed book): "Inner" is next to the spine and "Outer" next to
  the page edge. On right-hand pages (odd numbers) Inner is on the left; on left-hand pages (even
  numbers) Inner is on the right. On left-hand pages PTXprint also swaps **First Reference** and
  **Last Reference**. So with **Last Reference** in **Outer (Right)**, the left-hand page shows its
  *first* verse at its outer edge and the right-hand page its *last* verse. Like a dictionary, the two
  outer edges of an open book then show the range of the whole spread.
* **Mirror Pages unticked**: Left is always left and Right is always right.

### Which pages get a header

* On the **first page of each book** (the page with the book title), the header is empty and no rule
  is drawn.
* On pages without verses (for example the introduction or the glossary), **First Reference**,
  **Last Reference** and **Reference Range** print nothing. Other items, such as the page number,
  still print.

### Reference format

Under **Include in References**, choose what the reference items contain (Regular and Full views):

* **Book** – the book name.
* **Chapter** – the chapter number.
* **Verse** – the verse numbers too. This needs **Chapter**.
* **Chapter-Verse Separator** – **Colon (ch:vs)** or **Period (ch.vs)**.

Most Bibles show only book and chapter, for example "Matthew 5–6", because a chapter is easier to
find when you turn the pages.

### Diglot options

In a diglot (two texts side by side), each place has two small buttons, **Pri** and **Sec**. They
choose whether the item comes from the primary or the secondary text. This decides both the
language of the book names in the references and the font. They are greyed out until you turn on
**Diglot (or Polyglot)** on the **Diglot** tab. (Regular and Full views.)

### Typing your own text (advanced)

Instead of choosing an item, you can type in the box. Mix ordinary words with these codes:

* `\pagenumber` – page number
* `\firstref`, `\lastref`, `\rangeref` – references
* `\book`, `\bookalt` – book name from `\h` or `\h1`
* `\isodate` – the date as YYYY-MM-DD; `\usdate` (month/day/year); `\ukdate` (day/month/year)
* `\hrsmins` – the time (HH:MM)
* `\empty` – nothing

Rules:

* Type a backslash and a space (`\ `) for each space between words, for example `DRAFT\ \isodate`.
* Type a backslash before `# % & ^ ~` and `\`. For example, `This\ is\ page\ \#\pagenumber`
  gives "This is page #1".
* Put square brackets around a code to print brackets: `[\pagenumber]` gives "[12]".

## 9.3 Other

This area is only shown in the **Regular** and **Full** views.

* **Starting Page Number (for Scripture Books)** – the page number of the first page of the first
  Scripture book.
* **Print Page Number at Bottom of Intro Page(s)** and **Print Name of Saved Config on Intro Page(s)**
  choose what goes in the footer of the first page of each book. Only one can be ticked; ticking one
  unticks the other.

## 9.4 Footer

The footer has one place: **Center Footer**. Many Bibles leave it empty and put the page number in
the header. It is useful for a page number at the bottom of every page, or a "DRAFT" message with
the date. Its list has fewer items than the header lists: **-empty-**, **Page Number**,
**Reference Range**, **DRAFT**, **Time (HH:MM)**, **Date (YYYY-MM-DD)**, **Date and Time** and
**Printed on YYYY-MM-DD**. Typing your own text works as for the header.

The footer of the first page of each book follows the **Other** area:

* **Print Page Number at Bottom of Intro Page(s)** ticked: the page number.
* else, **Print Name of Saved Config on Intro Page(s)** ticked: the configuration name.
* else: the same as **Center Footer**.

In a diglot, the **Pri** and **Sec** buttons choose which text's font the footer uses.

To move the footer up or down, use the **Layout** tab, **Margins** area (**Bottom of Text to Top of
Footer** and **Place Footer Text Above the Bottom Margin**).

## 9.5 Common tasks

### How do I put the page number in the outer corner and the references in the center?

1. On the **Layout** tab, in **Page Setup**, tick **Mirror Pages**.
2. On the **Header+Footer** tab, set **Outer (Right)** to **Page Number**, **Center** to
   **Reference Range** and **Inner (Left)** to **-empty-**.
3. Print again.

### How do I show verse numbers in the header references?

1. Switch to the **Regular** or **Full** view.
2. On the **Header+Footer** tab, make sure **Chapter** is ticked, then tick **Verse**.
3. Choose **Colon (ch:vs)** or **Period (ch.vs)**.

### How do I add "DRAFT" and today's date to every page?

1. On the **Header+Footer** tab, open **Center Footer**.
2. Choose **Printed on YYYY-MM-DD** (or **Date and Time** if you print several drafts on one day), or
   type `DRAFT\ \isodate`.
3. Print again. The date is the date of printing.

### How do I start the page numbers at 101?

1. Switch to the **Regular** or **Full** view.
2. On the **Header+Footer** tab, in **Other**, set **Starting Page Number (for Scripture Books)** to 101.
3. Print again.

### How do I put a line under the header?

1. On the **Layout** tab, in the **Margins** area, tick **Horizontal Rule**.
2. Set **Space between Rule and Top of Text (pt)** (a pt, or point, is about 0.35 mm).
3. The rule is not drawn on the first page of each book.

### How do I show the name of my configuration on the printout?

1. Switch to the **Regular** or **Full** view.
2. On the **Header+Footer** tab, in **Other**, tick **Print Name of Saved Config on Intro Page(s)**.
3. The name is printed at the bottom of the first page of each book, instead of the page number.

### How do I set the headers for a diglot?

1. On the **Diglot** tab, turn on **Diglot (or Polyglot)**.
2. On the **Header+Footer** tab, choose an item for each place.
3. For each place, click **Pri** for the primary text (its book names and font), or **Sec** for the
   secondary text.
4. Decide on **Mirror Pages** on the **Layout** tab. With it ticked, the primary text is next to the spine.

## 9.6 Common problems

**There is no header on the first page of a book.**
This is normal: PTXprint prints no header (or rule) on the page where a book starts. Tick **Print
Page Number at Bottom of Intro Page(s)** to have a page number there.

**The header references are empty on the introduction or glossary pages.**
This is normal. Those pages have no verses, so the reference items print nothing. The page number
still prints.

**The header shows the last verse on the left page where I expected the first verse.**
Cause: **Mirror Pages** is ticked, so **First Reference** and **Last Reference** swap on left-hand
pages. Fix: choose the other item, or untick **Mirror Pages** on the **Layout** tab.

**The header is on the wrong side on left-hand pages.**
Cause: with **Mirror Pages** ticked, **Inner** and **Outer** swap sides on left-hand pages. Fix:
untick **Mirror Pages** for the same layout on every page.

**"Verse" is greyed out.**
Cause: **Chapter** is unticked. Tick **Chapter** first.

**The Pri / Sec buttons are greyed out.**
Cause: diglot is not on. Turn on **Diglot (or Polyglot)** on the **Diglot** tab.

**"Print Name of Saved Config" unticked itself.**
Cause: you ticked **Print Page Number at Bottom of Intro Page(s)**. Only one of the two can be used.

**My own header text prints wrongly, or the PDF fails.**
Cause: a space or a special character (`# % & ^ ~ \`) was typed without a backslash before it.
Fix: type `\ ` for spaces and `\#`, `\%` and so on.

**The page numbers do not start at the "Starting Page Number".**
The number is applied when the first Scripture book starts, if the pages before it use the separate
front matter numbering (as PTXprint sets up by default). If the front matter has normal page
numbers, the numbering simply continues from the front matter.

## 9.7 Settings reference

### Header+Footer

#### Header

##### Center – Center page header settings

Drop-down · Basic+ · `ecb_hdrcenter` · cfg `header/hdrcenter`  
Choices: -empty- | Page Number | First Reference | Last Reference | Reference Range | Book (\h) | Book Alt (\h1) | Time (HH:MM) | Date (YYYY-MM-DD) | Date and Time | Printed on YYYY-MM-DD

> The header line on each page can contain the page number, and/or reference(s) in various forms. Select a preset option, or type in a keyword with additional adornments as needed.
>
> For example:  
> \bookalt\ \rangeref   uses the book name from the \h1 alt book header [\pagenumber]    places square brackets around the page number DRAFT\ \isodate\ \hrsmins    gives "DRAFT YYYY-MM-DD HH:MM"  
> -empty-     places nothing in that location
>
> With Mirror Pages on, First Reference and Last Reference are swapped on left-hand (even) pages.
>
> Note that a space and the following certain special characters require a slash '\' to be typed before them:  
>     # % & ^ ~ and \ itself. For example, to get this output:  
>      This is page #1 you would need to enter:  
>      This\ is\ page\ \#\pagenumber

A common choice is **Page Number** or **Reference Range**. The center place does not change sides
with **Mirror Pages**, but **First Reference** and **Last Reference** still swap on left-hand pages.

##### Outer (Right) – Outer (right) page header settings

Drop-down · Basic+ · `ecb_hdrright` · cfg `header/hdrright`  
Choices: -empty- | Page Number | First Reference | Last Reference | Reference Range | Book (\h) | Book Alt (\h1) | Time (HH:MM) | Date (YYYY-MM-DD) | Date and Time | Printed on YYYY-MM-DD

> The header line on each page can contain the page number, and/or reference(s) in various forms. Select a preset option, or type in a keyword with additional adornments as needed.
>
> For example:  
> \bookalt\ \rangeref   uses the book name from the \h1 alt book header [\pagenumber]    places square brackets around the page number DRAFT\ \isodate\ \hrsmins    gives "DRAFT YYYY-MM-DD HH:MM"  
> -empty-     places nothing in that location
>
> With Mirror Pages on, First Reference and Last Reference are swapped on left-hand (even) pages.
>
> Note that a space and the following certain special characters require a slash '\' to be typed before them:  
>     # % & ^ ~ and \ itself. For example, to get this output:  
>      This is page #1 you would need to enter:  
>      This\ is\ page\ \#\pagenumber

With **Mirror Pages** ticked, this is the outer edge: right on right-hand pages, left on left-hand
pages. A common choice is **Page Number** or a reference.

##### Inner (Left) – Inner (left) page header settings

Drop-down · Basic+ · `ecb_hdrleft` · cfg `header/hdrleft`  
Choices: -empty- | Page Number | First Reference | Last Reference | Reference Range | Book (\h) | Book Alt (\h1) | Time (HH:MM) | Date (YYYY-MM-DD) | Date and Time | Printed on YYYY-MM-DD

> The header line on each page can contain the page number, and/or reference(s) in various forms. Select a preset option, or type in a keyword with additional adornments as needed.
>
> For example:  
> \bookalt\ \rangeref   uses the book name from the \h1 alt book header [\pagenumber]    places square brackets around the page number DRAFT\ \isodate\ \hrsmins    gives "DRAFT YYYY-MM-DD HH:MM"  
> -empty-     places nothing in that location
>
> With Mirror Pages on, First Reference and Last Reference are swapped on left-hand (even) pages.
>
> Note that a space and the following certain special characters require a slash '\' to be typed before them:  
>     # % & ^ ~ and \ itself. For example, to get this output:  
>      This is page #1 you would need to enter:  
>      This\ is\ page\ \#\pagenumber

With **Mirror Pages** ticked, this is the inner edge (next to the spine): left on right-hand pages,
right on left-hand pages. Many publications leave it **-empty-**.

##### Pri

Radio · Regular+ · `r_hdrLeft_Pri` · cfg `header/hdrleftside=Pri`  
Also: Use formatting from primary project (inner header) · Needs: “Diglot (or Polyglot)”

> If setting the header for a diglot you will need to specify whether this part of the header (its text and formatting) should come from the Primary (Left) or the Secondary text.
>
> Note: To activate or change this setting, you must first enable Diglot.

References use the primary text's book names, and its header font is used.

##### Sec

Radio · Regular+ · `r_hdrLeft_Sec` · cfg `header/hdrleftside=Sec`  
Also: Use formatting from secondary project (inner header) · Needs: “Diglot (or Polyglot)”

> If setting the header for a diglot you will need to specify whether this part of the header (its text and formatting) should come from the Primary (Left) or the Secondary text.
>
> Note: To activate or change this setting, you must first enable Diglot.

References use the secondary text's book names, and its header font is used.

##### Pri

Radio · Regular+ · `r_hdrCenter_Pri` · cfg `header/hdrcenterside=Pri`  
Also: Use formatting from primary project (center header) · Needs: “Diglot (or Polyglot)”

> If setting the header for a diglot you will need to specify whether this part of the header (its text and formatting) should come from the Primary (Left) or the Secondary text.
>
> Note: To activate or change this setting, you must first enable Diglot.

Primary text's book names and font for the center item.

##### Pri

Radio · Regular+ · `r_hdrRight_Pri` · cfg `header/hdrrightside=Pri`  
Also: Use formatting from primary project (outer header) · Needs: “Diglot (or Polyglot)”

> If setting the header for a diglot you will need to specify whether this part of the header (its text and formatting) should come from the Primary (Left) or the Secondary text.
>
> Note: To activate or change this setting, you must first enable Diglot.

Primary text's book names and font for the outer item.

##### Sec

Radio · Regular+ · `r_hdrCenter_Sec` · cfg `header/hdrcenterside=Sec`  
Also: Use formatting from secondary project (center header) · Needs: “Diglot (or Polyglot)”

> If setting the header for a diglot you will need to specify whether this part of the header (its text and formatting) should come from the Primary (Left) or the Secondary text.
>
> Note: To activate or change this setting, you must first enable Diglot.

Secondary text's book names and font for the center item.

##### Sec

Radio · Regular+ · `r_hdrRight_Sec` · cfg `header/hdrrightside=Sec`  
Also: Use formatting from secondary project (outer header) · Needs: “Diglot (or Polyglot)”

> If setting the header for a diglot you will need to specify whether this part of the header (its text and formatting) should come from the Primary (Left) or the Secondary text.
>
> Note: To activate or change this setting, you must first enable Diglot.

Secondary text's book names and font for the outer item. A common diglot setup is **Pri** for one
side and **Sec** for the other, so each language has its own reference.

##### Chapter

Checkbox, on · Regular+ · `c_rangeShowChapter` · cfg `header/ifshowchapter`

> By default, the chapter number will be included in any references in the header line. If you prefer to suppress that (and just show the book name) then uncheck this option. (Verse numbers can only be shown if Chapter is ticked.)

Example: "Mark 4". Unticking it greys out **Verse**. Unticking can be useful for one-chapter books or
non-Bible publications.

##### Verse

Checkbox, off · Regular+ · `c_rangeShowVerse` · cfg `header/ifshowverse`  
Needs: “Chapter”

> By default only the Book and Chapter number is included in the Header. If you also want to include the verse numbers, then check this option.
>
> Keep in mind that including the verse numbers actually makes it harder to read/absorb when flicking through pages to find the right chapter.

Example: "Mark 4:3–5:2" instead of "Mark 4–5".

##### Colon (ch:vs)

Radio · Regular+ · `r_CVsep_colon` · cfg `header/chvseparator=colon`  
Needs: “Verse”, “Chapter”

> Use a colon (:) to separate chapter & verse numbers in the header reference.

If the Paratext project has its own chapter-verse separator, PTXprint uses that one.

##### Period (ch.vs)

Radio · Regular+ · `r_CVsep_period` · cfg `header/chvseparator=period`  
Needs: “Verse”, “Chapter”

> Use a period (.) to separate chapter & verse numbers in the header reference.

Example: "4.3".

##### Book

Checkbox, on · Regular+ · `c_rangeShowBook` · cfg `header/ifshowbook`

> By default, the book name will be included in any references in the header line. But if you wish to suppress that (and just show the chapter and/or verse numbers) then uncheck this option.

The name comes from the book's `\h` line. Untick it if the book name is already elsewhere in the
header, for example with **Book (\h)**.

##### \h

Link · Regular+ · `lb_style_h`

> Click to edit the marker's properties on the Styles tab.

The `\h` style sets the font, size and colour of the running header text. The footer also follows
it unless changed separately.

#### Other

##### Starting Page Number (for Scripture Books) – Start numbering scripture books from page N

Number · Regular+ · `s_startPageNum` · cfg `document/startpagenum`  
Values: 1–9999 (default 1)

> If the document you are creating needs to be appended to another, you can start the page numbering from where the previous document ends by entering the subsequent page number here. (If the front matter already uses normal page numbers, the numbering just continues instead.)

For example 101. Front matter before the first Scripture book is numbered separately (roman numerals
i, ii, iii … in PTXprint's front matter), and the Scripture numbering then starts at this number.

##### Print Page Number at Bottom of Intro Page(s)

Checkbox, on · Regular+ · `c_pageNumTitlePage` · cfg `footer/ifftrtitlepagenum`  
Also: Print page number at each book's Intro page footer

> Print the page number at the bottom of the first page of each book (the title page, where the header is not shown).
>
> This cannot be used together with 'Print Name of Saved Config on Intro Page(s)'.

That page has no header, so without this it has no page number at all. Ticking this unticks
**Print Name of Saved Config on Intro Page(s)**.

##### Print Name of Saved Config on Intro Page(s)

Checkbox, off · Regular+ · `c_printConfigName` · cfg `footer/ifprintconfigname`  
Also: Print the name of the config on Intro pages' footer

> It may be helpful to print the Name of the Saved Configuration on the first page (of every book) as a reminder for later - as to which settings were used to produce the PDF.
>
> This cannot be used together with 'Print Page Number at Bottom of Intro Page(s)'.

Ticking this unticks **Print Page Number at Bottom of Intro Page(s)**. Untick it for the final
publication.

#### Footer

##### Center Footer – Center page footer settings

Drop-down · Basic+ · `ecb_ftrcenter` · cfg `footer/ftrcenter`  
Choices: -empty- | Page Number | Reference Range | DRAFT | Time (HH:MM) | Date (YYYY-MM-DD) | Date and Time | Printed on YYYY-MM-DD

> It is not considered best-practice to include information in a footer for scripture publications. This is usually better placed in the header. However, if there is a need to have the page number at the footer for all pages (not just the 1st page of each book) then that can be set here. Similarly, you may want to add a DRAFT message and/or date to the end of each page. Note that you can select a preset option OR type your own text as needed.
>
> For example:  
> [\pagenumber]   places square brackets around the page number DRAFT\ \isodate\ \hrsmins   would give "DRAFT YYYY-MM-DD HH:MM"  
> -empty-     places nothing in that location
>
> Note that if you really must have Inner/Outer Footers, these can be set in the ptxprint-mods.tex file.
>
> It is not considered best-practice to include information in a footer for scripture publications. This is usually better placed in the header. However, if there is a need to have the page number at the footer for all pages (not just the 1st page of each book) then that can be set here. Similarly, you may want to add a DRAFT message and/or date to the end of each page. Note that you can select a preset option OR type your own text as needed. Note that if you really must have Inner/Outer Footers, these can be set in the ptxprint-mods.tex file.

On the first page of each book, the **Other** area settings can replace it. **DRAFT** prints the word
"DRAFT". Own text uses the same codes and rules as the header. For drafts, **Date and Time** shows
when each printout was made.

##### Sec

Radio · Regular+ · `r_ftrCenter_Sec` · cfg `footer/ftrcenterside=Sec`  
Also: Use formatting from secondary project (center footer) · Needs: “Diglot (or Polyglot)”

> If setting the footer for a diglot you will need to specify whether this part of the footer (its text and formatting) should come from the Primary (Left) or the Secondary text.

Uses the secondary text's font (and references) for the footer.

##### Pri

Radio · Regular+ · `r_ftrCenter_Pri` · cfg `footer/ftrcenterside=Pri`  
Also: Use formatting from primary project (center footer) · Needs: “Diglot (or Polyglot)”

> If setting the footer for a diglot you will need to specify whether this part of the footer (its text and formatting) should come from the Primary (Left) or the Secondary text.

Uses the primary text's font (and references) for the footer.


# 10. Pictures tab

## 10.1 What this tab is for

Use the **Pictures** tab when your publication has pictures (illustrations) or maps. Here you can:

* turn pictures on or off for the whole publication,
* tell PTXprint where to find the picture files,
* choose the size and position of every picture on the page,
* add or remove pictures, and add maps,
* look for new pictures in a catalogue of Bible illustrations,
* keep track of copyright, permissions and the checking of each picture.

**The PicList.** PTXprint keeps a list of all the pictures for each saved configuration. This list is called the **PicList** (picture list). Each line of the PicList says which picture file to use, where in the text it belongs (the *anchor*), its caption, its size and its position on the page.

When you generate the PicList, PTXprint copies the `\fig ... \fig*` entries from your Paratext books into the PicList. After that, PTXprint uses only the PicList. It ignores the `\fig` entries in the text when it typesets. This means:

* You can place, resize, add and remove pictures in PTXprint **without changing the Paratext text**.
* Each configuration can have different pictures. For example, a full Bible can have a few pictures, and a children's portion can have many.
* Changes you make here are **not** copied back into Paratext. If a caption or picture changes in Paratext, use **Refresh List** or **Generate...** to bring the change into PTXprint.

**View levels.** The Pictures tab is shown from the **Basic** view. In the **Basic** view you only see a few settings on the **Global Options** sub-tab. The picture table, the **Details** and **Checklist** sub-tabs and most buttons are only shown in the **Regular** and **Full** views.

Some words used in this chapter:

* **Anchor** – the place in the text (for example a verse) that a picture belongs to.
* **Caption** – the text printed with the picture, usually below it.
* **Cutout** – a space cut into the side of a paragraph, so that the text flows around a small picture.
* **Span** – the full width of the text area, across both columns.
* **Mirror** – flip a picture from left to right, like in a mirror.
* **Credit overlay** – a small copyright line printed on top of the picture itself.
* **Image set** – a downloadable collection of Bible illustrations that you can use in the catalogue.

## 10.2 The picture table (PicList)

The top half of the tab shows the PicList as a table. Each row is one picture. The columns shown change with the sub-tab: **Global Options** and **Checklist** show only a few columns; **Details** shows them all.

* Click a row to select it. Its settings appear in the **Details** sub-tab below.
* Double-click a row to jump to the **Details** sub-tab.
* You can select several rows at once (use Ctrl or Shift while clicking). Then you can change the size, position, scale or mirror setting of all of them together. Fields that must be different for each picture (anchor, caption, filename, reference) are greyed out while several rows are selected.
* Right-click a row for more actions: copy the `\fig` line for that picture (to paste into Paratext), jump to the reference in Paratext (Windows only), show the picture file in the file manager, copy the file path, or delete the picture(s).
* **Red** text in a row means the picture is probably too tall to fit on the page at this size and scale. Make the **Scale** smaller.
* **Grey** rows mean PTXprint cannot find the picture file. Check the file name and the picture folders (see below).

The buttons next to the table:

* **Add** – add a picture file by hand.
* **Del** – delete the selected picture(s) from the PicList at once (no question is asked).
* **Generate...** – (re)build the PicList from the `\fig` entries in the Paratext books.
* **Refresh List** – update only the captions and references from Paratext.
* **Add Maps...** / **Edit Maps...** – add maps at the end of the publication, and edit the map book.
* **Show Catalogue...** – open the **Select Images** dialog to choose illustrations from an image set.
* **Show Active Books** – show only the pictures of the books you have chosen to print.
* **Image** / **Position** – show either a preview of the picture, or a small drawing of where it will sit on the page.

When the **Checklist** sub-tab is open, the buttons are replaced by a **Filter Checklist** area. Use it to show only the pictures that still need checking, or only the approved ones.

## 10.3 Global Options

This sub-tab has the settings for all the pictures in the publication.

**Include Pictures (illustrations)** is the main switch. When it is not ticked, PTXprint prints no pictures, and most other picture settings are greyed out.

**Resolution.** Paratext usually keeps small, low-quality JPG copies of pictures in the project's `figures` folder. Large, high-quality copies are often kept in the project's `local\figures` folder, so that they are not shared by Send/Receive.

* **Low Resolution (Smaller File)** – PTXprint prefers JPG files, and the smaller file if there are two of the same kind. The PDF is small and easy to email. Use this for drafts and checking.
* **High Resolution (Larger File)** – PTXprint prefers TIF and PNG files, and the larger file. Use this for the final PDF for the printer.
* **Use Place-holders (Smallest PDF File)** – prints an empty box where each picture would go. The layout stays the same, but the PDF is very small.

**What to print.**

* **Omit Pictures Only Meant for Web or App** – leaves out pictures that are not marked for print.
* **Omit Captions** – prints the pictures without any caption.
* **Omit References (ch:vs)** – keeps the captions but removes the chapter:verse reference after them.
* **Omit Missing Pictures** – if a picture file cannot be found, PTXprint skips it and continues. After you print, the number of missing pictures is shown next to this option, and their names are listed at the bottom of the sub-tab.
* **Remove Image Borders** – cuts off thin lines at the edges of pictures. It affects every picture.

**Where PTXprint looks for picture files.** PTXprint searches these folders, and all the folders inside them (unless **Exclude Subfolders** is ticked):

1. the **Picture Folder** you chose (only when **Use Other Location** is ticked),
2. the project's `local\figures` folder,
3. the project's `figures` folder,
4. the image sets you have downloaded (in PTXprint's own data folder).

The PicList only stores the file **name**, not the folder. If several files have the same name (for example `hk00123.jpg` and `hk00123.tif`), **Image Types** decides which one is used. If you leave **Image Types** empty, PTXprint uses JPG first for low resolution and TIF first for high resolution. TIF and PNG pictures are converted to JPG while the PDF is made.

**Permissions.** **Request Access...** (only with **High Resolution**) and **Get Permission...** open online forms that PTXprint fills in with the list of pictures used in this configuration.

## 10.4 Details

This sub-tab shows the settings of the picture selected in the table. It is only shown in the **Regular** and **Full** views.

**Anchor Ref.** The anchor is where the picture belongs in the text. It has a 3-letter book code, a space, and the chapter and verse joined with a dot: `MRK 4.39`. PTXprint puts the picture on the same page as its anchor if there is room. If there is no room, the picture can move to a later page. To move a picture to an earlier or later page, change the anchor by a few verses. Other forms:

* In a diglot, add `L` or `R` to the book code (`MRKL 4.39`) to tie the picture to the primary (L) or secondary (R) text.
* In the glossary, `GLO k.Altar` ties a picture to the glossary entry `\k Altar\k*`. Spaces are removed (`GLO k.JohntheBaptist`).
* `=2` at the end (for example `PSA 23.4=3`) means "the 2nd (or 3rd) paragraph after this anchor". This is useful for poetry.

**Caption, Caption Ref and Filename.** The **Caption** is printed with the picture. The **Caption Ref** is the reference printed after the caption, for example `(4:39)`. It does not have to be the same as the anchor. The **Filename** is the name of the picture file. Changes here are not copied back to Paratext.

**Size and position.** Three settings work together. The choices in each list change with the one before it, so set them in this order:

1. **Frame Size** – how wide the area for the picture is:
   * **Column Width** – the width of one column (in two-column layout).
   * **Span Width** – the full width of the text, across both columns.
   * **Page (in Margins)** – a whole page inside the margins. The page header is still printed.
   * **Page (to Edge)** – the whole sheet of paper, with no margins, header or footer. Do not use a caption with this size.
   In single-column layout, Column Width and Span Width are the same.
2. **Vertical Position** – where the picture goes:
   * **Top** / **Bottom** – at the top or bottom of the page (or column).
   * **Below Notes** – below the footnotes (Span Width only).
   * **Before Verse** – in the text, just before the anchor verse.
   * **After Paragraph** – in the text, after the paragraph that contains the anchor.
   * **Cutout** – in a notch at the side of the paragraph. The text flows around the picture.
   For the page sizes, the choices are **Top**, **Center** and **Bottom** of the page.
3. **Horizontal Position** – **Left**, **Right**, **Inner** (near the binding), **Outer** (near the outside edge) and, where possible, **Center**. It is greyed out (shows **-**) for Span Width.

**Number of Lines** is used only with **Cutout** (how many lines below the start of the paragraph the picture starts; decimals are allowed) and **After Paragraph** (after how many paragraphs).

PTXprint stores the position as a short code (shown in the table's position column). You do not have to type these codes, but they help when you read the table:

| Code | Meaning |
|---|---|
| `t`, `b` | top or bottom of the page, full width |
| `B` | below the footnotes |
| `tl`, `tr`, `bl`, `br` | top or bottom of the left or right column |
| `hl`, `hc`, `hr` | "here" – just before the anchor verse, left, centre or right |
| `pc`, `pl2` | after the paragraph (the number = after that many paragraphs) |
| `cl2`, `cr3` | cutout on the left or right, starting 2 or 3 lines down |
| `P`, `Pt`, `Pb` | a page of its own, centred, at the top or at the bottom |
| `F` | a full page to the edge of the paper |

`i` and `o` (inner and outer) can be used instead of `l` and `r`.

**Scale** makes the picture smaller (or larger) inside its frame. 100% means the full width of the frame. For a cutout, 30–50% is common. If the row turns red, the picture is too tall for the page; make the scale smaller.

**Mirror** flips the picture. Use it, for example, so that people in the picture look into the page and not out of it, or so that an action is done with the right hand. **Odd** and **Even** flip the picture only when it lands on an odd or even page. **Mirror** is greyed out if the **Checklist** sub-tab says **Never mirror** or **Always mirror** for this picture.

**Media (Print, App, Web).** These boxes say where the picture may be used. A picture without **Print** is left out of the PDF. Some boxes are greyed out because the artist's licence does not allow that use. If you untick all three boxes, PTXprint remembers this when you open the project again.

**Copyright.** For the common series of Bible illustrations (for example file names that start with `cn`, `co`, `hk`, `lb`, `bk`, `dy`, `mn` or `wa` followed by five digits), PTXprint knows the copyright text. You see the word **Automatic** instead of a text box. For other pictures, type the credit in **Copyright Attribution**. PTXprint collects all the picture credits, with page numbers, into the colophon when the colophon contains `\zimagecopyrights` (set this on the **Peripherals** tab).

Some artists require a small credit printed **on** each picture. Click **© ...** to open the **Illustration Credit Overlay** dialog.

**Extra** is for advanced options such as rotating a picture (`rotated 90`, `rotate=edge`, `rotate=binding`) or choosing a page of a multi-page PDF (`page=2`).

## 10.5 Checklist

This sub-tab helps the team think about whether each picture is right for the readers. It is only shown in the **Regular** and **Full** views. The answers are stored with the picture's file, not with the anchor. So if the same picture is used twice, both uses share the answers. PTXprint saves the answers, the approval and the notes, and loads them again the next time you open the project.

* **Across Various Publications** – questions about the picture itself: is it clear, is it acceptable in the culture, and may it be mirrored? These answers are shared by all configurations of the project.
* **In This Publication** – questions about this use: why is it here, is it clear in this context, does it carry a wrong meaning, and does its style suit this publication? These answers belong to the current configuration.
* **Consultant Approval** – tick **Approved to be used in**, choose **any publication** or **this publication**, and type the initials and date.
* **Notes About This Picture** – a place to write comments, or to discuss the picture with the consultant.

Use the **Filter Checklist** area above the table to show, for example, only the pictures where some questions are still **Unknown**.

## 10.6 Generate PicList dialog

This dialog opens when you click **Generate...** and a PicList already exists. (If there is no PicList yet, PTXprint makes one at once without asking.)

* **Append Pictures to PicList From These Books** – read the `\fig` entries again only for the books listed (the books selected on the **Basic** tab). Pictures from other books stay as they are.
* **Include Pictures From ALL Books** – read all the books of the project again.
* **Randomly Position Pictures on Page** – give new pictures a random corner (top-left, top-right, bottom-left or bottom-right). Without it, new pictures go top-left in two-column layout and at the top in single-column layout.
* **Protect existing PicList settings** – keep the size and position of pictures that are already in the PicList, and only add new ones. Untick it only if you want to start again from the Paratext text.

## 10.7 Select Images dialog (the catalogue)

Click **Show Catalogue...** to open this dialog. It shows thumbnails of the pictures in an **Image Set**. If you have no image set yet, the **Download & Install Image Sets** dialog opens first.

* Choose the **Image Set** at the top.
* The **Limit to Range of References** box starts with the books you are printing. Only pictures for these references are shown. Clear it to see all pictures.
* Type words in **Search** to find pictures by keyword or title.
* Tick artists in the artist list to show only their pictures.
* Click **Search + Update Images** (or press Enter) after you change the search or references.
* Sort by **Scripture Reference** or by **Frequency of Use**.
* Move the mouse over a picture to see its number, artist, description and references. Right-click a picture to see a larger preview.
* Pictures with a peach-coloured background are already in your PicList.
* Click pictures to select them, then click **Add Images to PicList**.

The new pictures are anchored at their Bible reference, with **Column Width** and top-left position. Then go to the **Details** sub-tab and type a caption for each one.

## 10.8 Download & Install Image Sets dialog

This dialog lists the image sets that PTXprint can download. Tick the sets you want and click **OK**. Sets that are already installed show **Installed** and cannot be ticked. Some sets show their terms of use; you must agree to the terms before the set is installed. You need an internet connection, and some sets are large.

**Install from ZIP file...** installs a set from a ZIP file on your computer. This is useful at a workshop: download the file once and share it. A ZIP file that contains only pictures (and no image-set information) is unpacked into the project's `local\figures` folder.

## 10.9 Illustration Credit Overlay dialog

Open this dialog with the **© ...** button on the **Details** sub-tab. It sets a small credit line that is printed on top of the picture. Some artists (for example David C Cook) require this.

* **Image Credit Text** – the text. Type `(c)` for ©, or `dcc` for the David C Cook credit.
* **Vertical Position** and **Horizontal Position** – which corner or edge of the picture.
* **Rotation** – turn the text to run up or down the side of the picture.
* **Background Box** – no box, a light box or a dark box behind the text, or the name of your own style.
* **Apply to ALL images in this series** – use the same text for all pictures of the same series (the same two letters at the start of the file name).
* **Overwrite any existing settings** – also replace the credit on pictures that already have one.

The credit is stored with the picture file, so it applies in all configurations of the project. The font, size and colour come from the `x-credit` style; click the **\x-credit** link to change it on the **Styles** tab.

## 10.10 Add Map dialog

Click **Add Maps...** to add map pages at the end of the publication.

1. Choose the **Book Code for Maps** (usually **XXM**).
2. Click **Select Map...** and choose the map file.
3. Type a **Caption** if you want one, and set **Scale** and **Rotation**.
4. Click **Size and Position...** to choose the frame size and position (the same dialog is used for sidebars). The code you choose is shown in the box beside it.
5. Click **Add Another Map** to add this map and start the next one, or **OK - Done!** to add it and finish.

PTXprint adds each map to the PicList (anchors `XXM map01`, `XXM map02` ...), writes one page for each map into the map book, ticks **Include Maps** on the **Peripherals** tab, and adds the map book to the list of books to print. Use **Edit Maps...** to look at the map book on the **View+Edit** tab.

## 10.11 Common tasks

### Show the pictures that are in the Paratext text

1. On the **Pictures** tab, **Global Options** sub-tab, tick **Include Pictures (illustrations)**.
2. Make sure the view is **Regular** or **Full** (so that you can see the picture table).
3. Click **Generate...**. If a dialog opens, choose **Append Pictures to PicList From These Books**, keep **Protect existing PicList settings** ticked, and click **OK**.
4. Look for grey rows in the table (missing files) and fix them (see "Common problems").
5. Print.

### Move a picture to another place on the page

1. Select the picture in the table. Open the **Details** sub-tab.
2. Set **Frame Size** first, then **Vertical Position**, then **Horizontal Position**.
3. Click **Position** (beside **Image**) to see a small drawing of the position.
4. Print again to check.

### Move a picture to another page

1. Select the picture and open the **Details** sub-tab.
2. Change the verse in **Anchor Ref** to a few verses earlier (to move it back) or later (to move it forward). Keep the dot between chapter and verse: `LUK 2.7`.
3. Print again.

### Make a picture smaller and let the text flow around it

1. Select the picture. On the **Details** sub-tab, set **Frame Size** to **Column Width**.
2. Set **Vertical Position** to **Cutout** and **Horizontal Position** to **Left** or **Right** (or **Inner**/**Outer**).
3. Set **Scale** to about 40%.
4. Set **Number of Lines** to the line where the picture should start (0 = the first line of the paragraph).
5. Print again.

### Add a new picture from the catalogue

1. Click **Show Catalogue...**.
2. Choose the **Image Set**. Type a word in **Search**, or check the references in **Limit to Range of References**, and click **Search + Update Images**.
3. Click the pictures you want, then click **Add Images to PicList**.
4. For each new picture, type the **Caption** on the **Details** sub-tab, and check the **Anchor Ref**.

### Use high-quality pictures for the final PDF

1. Put the high-resolution files in the project's `local\figures` folder, or tick **Use Other Location** and click **Picture Folder...** to choose their folder.
2. On **Global Options**, choose **High Resolution (Larger File)**.
3. Print, and check that the missing-pictures count is 0.

### Make a small PDF to send by email

1. On **Global Options**, choose **Low Resolution (Smaller File)**.
2. If the file must be even smaller, tick **Use Place-holders (Smallest PDF File)**.

### Print the picture credits in the colophon

1. On the **Peripherals** tab, tick **Colophon at End of Publication**.
2. Make sure the colophon text contains `\zimagecopyrights`.
3. For pictures that do not show **Automatic** on the **Details** sub-tab, type the credit in **Copyright Attribution**.
4. Print. PTXprint lists each artist with the pages of their pictures.

### Add maps at the end of the book

1. Click **Add Maps...**.
2. Follow the steps in the "Add Map dialog" section above.
3. Click **OK - Done!**, then print.

## 10.12 Common problems

**The Pictures tab shows no table, or no Details sub-tab.**
The table and the **Details** and **Checklist** sub-tabs are only shown in the **Regular** and **Full** views. Change the view level. Also check that **Include Pictures (illustrations)** is ticked.

**No pictures appear in the PDF.**
* **Include Pictures (illustrations)** is not ticked. Tick it.
* The PicList is empty. Click **Generate...**. (Pictures in the Paratext text are only used after they are in the PicList.)
* **Use Place-holders** is ticked. Untick it.
* The **Print** box on the **Details** sub-tab is not ticked for these pictures.

**Some pictures are missing.**
* The row is grey in the table: PTXprint cannot find the file. Check the **Filename**. Make sure the file is in the project's `figures` or `local\figures` folder, or tick **Use Other Location** and choose the folder with **Picture Folder...**.
* **Image Types** contains only some types (for example only `TIF`), and the file is a different type. Clear **Image Types**.
* The picture's book is not one of the books you are printing.
* **Omit Missing Pictures** hides the problem. Look at the missing-pictures count and list on **Global Options** after printing.

**A picture I added with Add is not found.**
The PicList stores only the file name. If you chose a file from a folder that PTXprint does not search, copy the file into the project's `local\figures` folder, or set that folder with **Use Other Location**.

**A picture appears on the wrong page.**
A picture at the top or bottom of a page goes on the same page as its anchor only if there is room. Change the **Anchor Ref** by a few verses. Pictures that are too large also move to a later page; reduce the **Scale**.

**I cannot choose the position I want.**
The lists depend on each other. **Span Width** only allows **Top**, **Bottom** and **Below Notes**, and no horizontal position. **Center** is only offered for **Before Verse**, **After Paragraph** and the page sizes. Choose the **Frame Size** first.

**The picture is too big, or the row is red.**
The picture is taller than fits on the page. Reduce the **Scale**, or use **Column Width** instead of **Span Width**.

**A cutout picture jumps between two places each time I print.**
This can happen when the anchor is near the end of a paragraph. Choose an earlier anchor in the same paragraph and increase **Number of Lines**.

**Mirror is greyed out.**
On the **Checklist** sub-tab, **Never mirror** or **Always mirror** is chosen for this picture. Choose **OK to mirror** to use the **Mirror** list again.

**My changes to captions in Paratext do not show.**
PTXprint uses its own PicList. Click **Refresh List** to copy the captions and references again. Your size and position settings stay the same.

**Changes in PTXprint do not appear in Paratext.**
This is normal. PTXprint never changes the Paratext text. To copy a picture into Paratext, right-click its row and choose **Copy \fig String to Clipboard**, then paste it in Paratext.

**The copyright text is missing or wrong.**
* The colophon must contain `\zimagecopyrights` (**Peripherals** tab).
* For pictures that are not from a known series, type the credit in **Copyright Attribution**.
* If **Sensitive Project** is ticked (on the **Advanced** tab), PTXprint uses a shorter credit wording for some artists.
* By default, the most common artist is described as "all other illustrations". To list every artist with all pages, tick **Show comprehensive illustration credits** (on the **Advanced** tab, **Other** sub-tab, in the **Pictures, Figures, Images, Sidebars** area).

**I want the caption above the picture, or the reference before the caption.**
On the **Advanced** tab, **Other** sub-tab, in the **Pictures, Figures, Images, Sidebars** area, tick **Show Caption Before Image** or **Ref Before Caption**.

## 10.13 Settings reference

### Generate PicList (dialog)

#### OK

Button · Regular+ · `btn_gnr8pl_ok`

Generates the PicList with the options chosen in the dialog.

#### Cancel

Button · Regular+ · `btn_gnr8pl_cancel`

Closes the dialog without changing the PicList.

#### When Generating PicList

##### Append Pictures to PicList From These Books

Radio · Mini+ · `r_generate_selected`  
Also: Generate PicList: Append to existing list

> This option will ADD to any existing entries in the PicList and/or replace entries for the book(s) listed below.

Pictures of other books stay as they are. This is the safe choice.

##### Include Pictures From ALL Books

Radio · Mini+ · `r_generate_all`  
Also: Generate PicList: Replace existing list

> This option will REPLACE ALL entries in the existing PicList. Do you really want to do this?
>
> If in doubt, then click Cancel.

If **Protect existing PicList settings** is not ticked, all your changes to sizes and positions are lost.

##### Randomly Position Pictures on Page

Checkbox, on · Mini+ · `c_randomPicPosn` · cfg `project/randompicposn`  
Also: Generate PicList: Randomly position pictures on page

> By default all illustrations are placed in the top-left corner of a page (when double columns are used) and at the top in single column mode.
>
> Checking this option will randomly position the illustrations on the page (using top-left, top-right, bottom-left and bottom-right).
>
> You can change the location of pictures later if needed.

It only affects pictures that have no position yet.

##### Protect existing PicList settings

Checkbox, on · Regular+ · `c_protectPicList`  
Also: Generate PicList: Protect existing PicList settings

> When synchronizing the pictures from the Paratext files with PTXprint's PicList, don't change any of the (layout and size) settings and don't delete any pictures no longer found in the Paratext USFM text.

Only new pictures are added. Keep it ticked unless you want to start again from the Paratext text.

### Select Images... (dialog)

#### Download Image Set...

Button · Regular+ · `btn_getImageSet`  
Also: Download an Image Set from an online source

> If you don't already have appropriate scripture illustrations, then you can download an Image Set which contains low-resolution illustrations for trial publications from one of the links.

Opens the **Download & Install Image Sets** dialog.

#### Request Access...

Button · Regular+ · `btn_requestIllustrations2`

> Request for Access to High Quality Illustrations/Maps in the SIL repository.
>
> Click this button to fill in the form requesting access to the illustrations used in the current publication.
>
> After completing and submitting the online form you should receive an immediate response by email.

The same online form as **Request Access...** on **Global Options**.

#### Add Images to PicList

Button · Regular+ · `btn_imagePicker_ok`  
Also: Add Images to Current Configuration's PicList

> Add the selected images to the current Configuration where an appropriate caption should be added and other image properties selected.

Each picture is anchored at its Bible reference, with **Column Width** and top-left position. Then type a caption for each one on the **Details** sub-tab.

#### Cancel

Button · Regular+ · `btn_imagePicker_cancel`

Closes the catalogue without adding pictures.

#### Limit to Range of References

Text box · Regular+ · `t_artRefRange`

Shows only pictures for these references. It starts with the books you are printing. You can type ranges such as `GEN 1-3; MRK`, with 3-letter book codes. Clear the box to see all pictures in the set. Press Enter or click **Search + Update Images** to apply it.

#### Search – Image Selection Dialog: Search for an image by keyword

Search box · Regular+ · `t_artSearch`

Searches keywords and titles, for example `boat` or `shepherd`. Press Enter or click **Search + Update Images** to apply it. Clear the box to show all pictures again.

#### Image Set

Drop-down · Regular+ · `ecb_artPictureSet`  
Choices: Default

PTXprint remembers your last choice. To get more image sets, click **Download Image Set...**.

#### Enter a name for the configuration to be saved.

Text box · Regular+

> Enter a name for the configuration to be saved.
>
> Note that only Roman/Latin names are supported using: a-z A-Z, 0-9, parentheses, underscores and hyphens.
>
> Longer descriptions may be typed into the Notes field below.

#### Scripture Reference

Radio · Regular+ · `r_imgSort_ref`

> Sort the images according to the canonical order of scripture.

Uses the reference that matches your reference range.

#### Frequency of Use

Radio · Regular+ · `r_imgSort_pop`

> Sort the images based on how often other projects use them. The most popular illustrations appear at the top of the list.

The pictures used most often by other projects come first.

#### tv_artists

Table · Regular+ · `tv_artists`

The artists (picture series) in the image set. Tick one or more to show only their pictures. Untick all of them to show every artist.

#### Search + Update Images

Button · Regular+ · `btn_imgRefresh`

Updates the thumbnails after you change the search words or the reference range. It is only active when something has changed.

#### Print

Checkbox, on · Regular+ · `c_imgMediaP`

> Filter for illustrations that can be used in Print/PDF publications.

At the time of writing, this box does not change which thumbnails are shown.

#### App

Checkbox, off · Regular+ · `c_imgMediaA`

> Filter for illustrations that can be used in mobile phone Apps.

At the time of writing, this box does not change which thumbnails are shown.

#### Web

Checkbox, off · Regular+ · `c_imgMediaW`

> Filter for illustrations that can be used on websites.

At the time of writing, this box does not change which thumbnails are shown.

#### Reference

Label · Regular+ · `lb_imgRefs`

> Note that if a reference only contains a book and chapter number (with no specific verse mentioned), then the illustration will be placed in the middle of the chapter.

The references of the picture under the mouse. The reference in bold is the one PTXprint will use as the anchor. References in red already have this picture in your PicList.

#### Clear Selection

Button · Regular+ · `btn_imgClearSelection`

Unselects all the selected thumbnails, so you can start your choice again.

### Download & Install Image Sets (dialog)

#### OK

Button · Regular+ · `btn_imgSet_ok`

Downloads and installs the ticked image sets. This can take a while. When it is finished, the catalogue opens.

#### Cancel

Button · Regular+ · `btn_imgSet_cancel`

Closes the dialog without downloading anything.

#### Select All / None

Checkbox, off · Regular+ · `c_imgSet_selectAll`

Some sets are large downloads.

#### tv_imagesets

Table · Regular+ · `tv_imagesets`

The image sets that you can download, with artist, style, size and licence. Tick the sets you want, then click **OK**. Sets marked **Installed** cannot be ticked. Hover over a row for more information.

#### Install from ZIP file...

Link · Regular+ · `btn_installFromZip`

> Install an image set from a local ZIP file. Useful for offline installations or shared image sets at workshops (avoids repeated large downloads).

If the set has terms of use, you must agree to them. A ZIP file with only pictures in it is unpacked into the project's `local\figures` folder.

### Illustration Credit Overlay (dialog)

#### OK

Button · Regular+ · `btn_ovrly_ok`

Saves the credit overlay settings for this picture (and for the series, if chosen). The credit is kept even if you close PTXprint without selecting another picture first.

#### Cancel

Button · Regular+ · `btn_ovrly_cancel`

Closes the dialog without changing the credit.

#### Vertical Position – Image credit dialog: Vertical position of text

Drop-down · Regular+ · `fcb_plCreditVpos`  
Choices: Top | Center | Bottom | Fill

Where the credit sits on the picture.

#### Horizontal Position – Image credit dialog: Horizontal position of text

Drop-down · Regular+ · `fcb_plCreditHpos`  
Choices: Left | Center | Right | Inner | Outer

Inner and outer are useful if the picture may be mirrored or appear on both odd and even pages.

#### Background Box – Image credit dialog: Background color

Drop-down · Regular+ · `ecb_plCreditBoxStyle`  
Choices: None | Light | Dark

> Specify the kind of box (Light/Dark background) or enter the name of a style which should be applied. By selecting a (custom) style, you can change multiple parameters at once: font, size and color.

When you open the dialog again, a credit with no box shows **None**.

#### Rotation – Image credit dialog: Rotation of text

Drop-down · Regular+ · `fcb_plCreditRotate`  
Choices: None | Anti-clockwise | Clockwise

> Sometimes the credit text needs to be rotated.

Useful when the credit is at the left or right edge.

#### Image Credit Text – Image credit dialog: Credit (copyright) text

Text box · Regular+ · `t_plCreditText`

> Type the text for the Credit to be overlaid on the image. Note that there are shortcuts:  
>    (c)   --> ©  
>    dcc  --> © David C Cook  
>        or --> © DCC   (if Sensitive Project is set)

Keep it short; it is printed in small letters.

#### Apply to ALL images in this series

Checkbox, off · Regular+ · `c_plCreditApply2all`  
Also: Image credit dialog: Apply to all images in series

> The same Credit Overlay text can be applied to all images that match this illustration's filename (e.g. CN01234.tif, CN05654.tif, etc.) You can then adjust the position, background and rotation for specific illustrations later.
>
> Setting this option will not affect illustrations which already have Credit Overlay settings.

A series is the pictures with the same two letters at the start of the file name, for example all `cn` pictures. To change pictures that already have a credit, also tick **Overwrite any existing settings**.

#### \x-credit

Link · Regular+ · `lb_style_x-credit`

> Click to edit the Credit Overlay properties on the Styles tab.

Change the font, size and colours of all credit overlays there.

#### Overwrite any existing settings

Checkbox, off · Regular+ · `c_plCreditOverwrite`  
Also: Image credit dialog: Overwrite existing values · Needs: “Apply to ALL images in this series”

> WARNING:  
> If this option is checked, it will disregard any previous settings, and overwrite them with the new overlay information, position and other parameters.

Use with care: earlier settings for individual pictures are lost.

### Add Map (dialog)

#### Add Another Map

Button · Regular+ · `btn_mapAddAnother`

> Add as many maps as needed, one at a time.

Adds the current map and clears the form for the next one. Finish with **OK - Done!**, because the map book is only written then.

#### OK - Done!

Button · Regular+ · `btn_addMap`

Adds the current map (if a file is chosen) and finishes. PTXprint writes the map pages into the map book, ticks **Include Maps** on the **Peripherals** tab, and adds the map book to the books to print.

#### Cancel

Button · Regular+ · `btn_gnr8cover_cancel1`

Closes the dialog. The map book is not written. Maps already added with **Add Another Map** may still be in the PicList; delete them there if you do not want them.

#### Book Code for Maps – Maps: Book code to be used to store map details

Drop-down · Regular+ · `fcb_ptxMapBook`  
Choices: XXM | XXA | XXB | XXC | XXD | XXE | XXF | XXG | BAK

> Select the extra book code to be used for the list of maps.
>
> An extra book (e.g. XXM) can be used to store map details. If you prefer to use one of the other standard Paratext books XXA...XXG then select it here. If the book already exists, the new maps are added at the end of it.

**XXM** is the usual choice. Choose another book only if XXM is used for something else.

#### Add Map

##### Scale – Scale Map Size

Number · Regular+ · `s_mapScale`  
Values: 0.01–4 (default 1)

1 means the full size of the frame.

##### Border – Maps: Select Ornamental Border

Drop-down · Regular+ · `fcb_coordBorder`  
Choices: None | Han3 | Map Edge A | Map Edge B

> A selection of ornamental borders are available to choose from, to be drawn around the map.

At the time of writing, PTXprint does not use this setting when it adds the map.

##### Select Map...

Button · Regular+ · `btn_selectMap`  
Also: Maps: Select the map image file

Chooses the map image file (PNG, JPG, PDF or TIF). A preview is shown in the dialog.

##### Caption – Picture: Caption

Text box · Regular+ · `t_mapCaption`

> By default the caption will appear below the picture. To show it above the picture, tick 'Show Caption Before Image' on the Advanced tab (Other sub-tab, Pictures, Figures, Images, Sidebars).
>
> Note that captions are NOT processed by any changes specified in the PrintDraftChanges.txt file.

Optional. Leave it empty if the map fills the whole page to the edge.

##### Rotation – Maps: Rotation of map image

Drop-down · Regular+ · `fcb_mapRotate`  
Choices: None | Anti-clockwise | Clockwise

> Rotate the map image by 90 degrees (anti-clockwise or clockwise) if needed.

Use it for a wide map on a tall page.

##### Size and Position...

Button · Regular+ · `btn_mapSizePosition`

Opens the **Size and Position** dialog to choose the frame size (for example a full page) and the position of the map. The result is shown as a code in the box beside the button.

##### t_mapPgPos

Text box · Regular+ · `t_mapPgPos`

The position code chosen with **Size and Position...**, for example `Pc` (a page of its own, centred).

##### Spread

Checkbox, off · Regular+ · `c_mapSpread`  
Also: Spread Map Out Across Both Pages

> Only enable this option if the map needs to be spread out across both pages.

At the time of writing, PTXprint does not use this setting when it adds the map.

### Pictures

#### tv_picListEdit

Table · Regular+ · `tv_picListEdit`  
Shown when: “Include Pictures (illustrations)”

One row for each picture in this configuration. Double-click a row to open **Details**; right-click it for more actions. Red text means the picture is too tall for the page; a grey row means the file cannot be found.

#### Del

Button · Regular+ · `btn_plDel`  
Also: Delete picture(s) from PicList · Shown when: “Include Pictures (illustrations)”

> Click to immediately delete the currently highlighted picture(s). No confirmation will be asked for!

There is no undo, so check the selection first. It does not change the Paratext text or the picture file.

#### Generate...

Button · Regular+ · `btn_plGenerate`  
Also: Generate the PicList · Shown when: “Include Pictures (illustrations)”

> This button will (re-)generate the PicList from the USFM \fig ... \fig* definitions.
>
> If you just want to (re-)generate the PicList for a single book, then select that book on the Basic tab.

If no PicList exists yet, PTXprint makes it at once; otherwise the **Generate PicList** dialog asks what to do. Use it after pictures are added in Paratext.

#### Add

Button · Regular+ · `btn_plAdd`  
Also: Add picture to PicList · Shown when: “Include Pictures (illustrations)”

> Click to add another picture to the PicList. You will need to fill in all the details in the area below.

PTXprint asks for a picture file, adds a row and opens the **Details** sub-tab. Then type the **Anchor Ref** (for example `JHN 3.16`) and a caption. Only the file name is saved, so the file must be in a folder that PTXprint searches.

#### Refresh List

Button · Regular+ · `btn_refreshCaptions`  
Also: Refresh (reload) picture captions from Paratext · Shown when: “Include Pictures (illustrations)”

> Refresh Captions:  
> If you have edited the picture captions within the Paratext USFM files but those changes are not being reflected here, then click this button to refresh the captions.
>
> Note that only the Captions and Verse Refs will be updated. All other size and position settings will remain unchanged.

Use it after captions are corrected in Paratext.

#### Add Maps...

Button · Regular+ · `btn_addMaps2`  
Also: Add Maps to the Publication · Shown when: “Include Pictures (illustrations)”

> Maps for the end of the publication can be added to one of the XX* books or to the XXM book using this dialog.

Opens the **Add Map** dialog.

#### Edit Maps...

Button · Regular+ · `btn_editMaps2`  
Also: Edit Maps module · Shown when: “Include Pictures (illustrations)”

> Switch to the View+Edit tab to show/edit the Maps module.

Does nothing if the map book (for example XXM) does not exist yet; use **Add Maps...** first.

#### Show Catalogue...

Button · Regular+ · `btn_getPictures`  
Shown when: “Include Pictures (illustrations)”

> Browse the catalogue of commonly used Bible illustrations from a range of different artists.

Opens the **Select Images** dialog, where you add pictures from an image set to the PicList. If no image set is installed, the download dialog opens first.

#### Show Active Books

Checkbox, off · Regular+ · `c_filterPicList` · cfg `config/filterpics`  
Also: Only show pictures used in the set of active books · Shown when: “Include Pictures (illustrations)”

> Select this option to only display the pictures from the books that are currently in focus to be printed. When unchecked, then the list will show pictures from ALL the books in the project that have been added to the PicList. If pictures of a certain book are missing, then you may need to select that book and Generate the PicList details just for *that* book.

The books selected for printing are set on the **Basic** tab. This only changes what you see; it does not delete anything.

#### Image

Radio · Regular+ · `r_image_preview`  
Also: Show preview of pictures · Shown when: “Include Pictures (illustrations)”

> Display the picture currently in focus. Note that this is dependent on the image being located in the specified folder(s).

If the box is empty, PTXprint could not find the picture file. Hover over the preview to see the file path.

#### Position

Radio · Regular+ · `r_image_location`  
Also: Show position of picture on page · Shown when: “Include Pictures (illustrations)”

> Show the relative position of the picture on the page. When Inner/Outer is used, the position displayed represents the odd/right-hand page of a spread.

Use it to check the **Frame Size** and position settings before you print.

#### Global Options

Label · Basic+ · `lb_settings`  
Shown when: “Include Pictures (illustrations)”

> Overview of the Pictures used in the publication.

Settings for every picture: resolution, captions, missing pictures and the picture folders.

#### Details

Label · Regular+ · `lb_details`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Use this tab to change the position, location, size or orientation of the images.
>
> Note: Any changes you make here will NOT be reflected in the Paratext USFM files. So if you are changing an illustration, its caption or frame size (column or span), then it is advisable to do so in Paratext before regenerating the PicList here.

The settings of the picture selected in the table, such as anchor, caption, size and position.

#### Checklist

Label · Regular+ · `lb_checklist`  
Shown when: “Include Pictures (illustrations)”

> This tab encourages you to think through the appropriateness of the pictures used in this publication, as well as other contexts.

Records whether each picture is clear, culturally acceptable and approved. When this sub-tab is open, a **Filter Checklist** area appears above the table.

#### Filter Checklist

##### Filter pictures for checklist

Drop-down · not shown · `fcb_chklstFilter`  
Choices: All | All Unknown / Unchecked | Any Unknown / Unchecked | Approved · Shown when: “Include Pictures (illustrations)”

> The list of pictures can be filtered according to the status of the checking values.

**All Unknown / Unchecked** – no question answered yet. **Any Unknown / Unchecked** – at least one question still open. **Approved** – the approved pictures. Only shown when the **Checklist** sub-tab is open.

##### Exclude Matched

Checkbox, off · not shown · `c_picCheckInvFilter`  
Also: Exclude (don't show) pictures that match filter · Shown when: “Include Pictures (illustrations)”

> Flip the results of the filtered list to exclude any items that match.

For example, choose **Approved** and tick this to see all pictures that are not approved yet.

#### Global Options

##### Include Pictures (illustrations)

Checkbox, off · Basic+ · `c_includeillustrations` · cfg `document/ifinclfigs`, `document/ifusepiclist`, `document/includeimg`  
Shown when: “Include Pictures (illustrations)”

> This setting enables/disables all the other settings relating to pictures.
>
> Note that it is important to provide proper copyright attribution for the illustrations used in a publication, and this can be done very easily using the \zimagecopyrights magic code within the Colophon (see the Peripherals tab for details).

When ticked, PTXprint loads the PicList for this configuration and prints the pictures. When not ticked, the **Details** and **Checklist** sub-tabs are hidden. Turning it on can make printing slower.

##### Include Pictures (illustrations)

###### High Resolution (Larger File)

Radio · Regular+ · `r_pictureRes_High` · cfg `document/picresolution=High`  
Also: Use high-resolution pictures · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> If this option is selected, PTXprint prefers TIF, then PNG, then JPG files (and the larger file if there are two of the same type).
>
> The original higher-quality illustrations are usually larger (.TIF .PNG or .PDF files) and are stored in the local\Figures folder so that they are not shared via Send/Recv. If these are used, the resulting PDF could be very large, and therefore difficult to share electronically, but the image quality will be as good as possible.

Use this for the final print PDF. **Request Access...** is only available with this option.

###### Low Resolution (Smaller File)

Radio · Regular+ · `r_pictureRes_Low` · cfg `document/picresolution=Low`  
Also: Use low-resolution pictures · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Paratext stores low resolution .JPG versions of illustrations in the project's "Figures" folder. If these are used, the file size of the resulting PDF will be relatively small, and therefore easy to share, but the image quality will be low.

Use this for drafts. PTXprint prefers JPG files and, of two files of the same type, the smaller one. Pictures may look blurred when printed.

###### Use Place-holders (Smallest PDF File)

Checkbox, off · Regular+ · `c_figplaceholders` · cfg `document/iffigplaceholders`  
Also: Pictures: Only show empty place-holders · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Use this option to include an empty box wherever illustrations would be placed in the final PDF.
>
> WHY would someone want to do this? It is sometimes necessary to generate the smallest possible PDF file (usually in order to send by e-mail) or to produce a PDF to be printed without illustrations.

The page layout stays the same, so you can check it with a very small PDF. Untick it for the final PDF.

###### Omit Pictures Only Meant for Web or App

Checkbox, on · Regular+ · `c_figexclwebapp` · cfg `document/iffigexclwebapp`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Only allow illustrations with the 'P'rint attribute.
>
> If the illustrations have been marked up with the w/a/p notation, then it is easy to exclude any illustrations that do not have the 'p' attribute.  Note: w= web, a=app, p=print.

Keep it ticked for printed publications.

###### How?

Link · Regular+ · `lb_omitPics`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Open a web page that explains how to mark pictures in Paratext for print, web or app.

Opens a help web page.

###### Omit Captions

Checkbox, off · Regular+ · `c_fighidecaptions` · cfg `document/iffigshowcaptions`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> If you want to suppress the picture captions from being displayed below the picture, then check this option.

Also removes the caption references.

###### Omit References (ch:vs)

Checkbox, off · Regular+ · `c_fighiderefs` · cfg `document/iffighiderefs`  
Needs: “Include Pictures (illustrations)” · Greyed out by: “Omit Captions” · Shown when: “Include Pictures (illustrations)”

> If you only want to suppress the reference part of the caption, then check this option. Note that it is not possible to just have the references without the captions.

The caption text is kept.

###### Omit Missing Pictures ...

Checkbox, on · Regular+ · `c_skipmissingimages` · cfg `document/iffigskipmissing`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Rather than aborting the PDF export process, pre-process the list of illustrations and skip/ignore/remove any which are not found in the specified location of image files.
>
> If Pictures are missing after preparing a PDF, then they will be listed in the section below.

After printing, the number of missing pictures is shown next to this option. Keep it ticked, but check the count before the final print.

###### Remove Image Borders

Checkbox, off · Basic+ · `c_cropborders` · cfg `document/iffigcrop`  
Also: Pictures: Remove Image Borders · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Some images have a thin line on one or more of the edges of the picture. Enable this option to automatically crop these unwanted lines from the edge of pictures. Note that this setting affects ALL images, not just those with lines.

Check that no picture loses part of its content. The pictures are converted to JPG when this is on.

###### Request Access...

Button · Regular+ · `btn_requestIllustrations`  
Needs: “High Resolution (Larger File)”, “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Request Access to High Quality Illustrations/Maps in the SIL repository.
>
> Click this button to fill in the form requesting access to the illustrations used in the current publication.
>
> After completing and submitting the online form you should receive an immediate response by email with a link to download the illustrations (if approved).

PTXprint fills in the project name and the list of pictures. You must add your email and supervisor details.

###### Get Permission...

Button · Regular+ · `btn_requestPermission`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> If you are publishing (i.e. more than 50 copies) any material with illustrations that require prior permission to be obtained before publishing, then click this button to automatically fill in the form requesting permission.
>
> Note that any missing information will need to be filled in on the Peripherals tab before the form can be submitted.
>
> After filling in any remaining details, you will need to submit the Google form and wait for a response.

PTXprint fills in the list of pictures and the publication details. If country, language or number of copies are missing, PTXprint opens the **Peripherals** tab so that you can fill them in first.

###### Use Other Location

Checkbox, off · Basic+ · `c_useCustomFolder` · cfg `document/customfiglocn`  
Also: Use pictures from a particular folder · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> The following locations are scanned for pictures:  
>   My Paratext ... Projects\\figures  
>   My Paratext ... Projects\\local\figures  
>   Users\...\AppData\Local\SIL\ptxprint\imagesets
>
> If your pictures are in a different folder, then enable this option and select a Picture Folder to be scanned in addition to the folders listed above. Note that ALL subfolders are also scanned unless you explicitly enable the 'Exclude Subfolders' option.

When you tick it and no folder is chosen yet, PTXprint asks for the folder.

###### Picture Folder...

Button · Basic+ · `btn_selectFigureFolder` · cfg `document/customfigfolder`  
Also: Select the folder which contains pictures · Needs: “Use Other Location”, “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Select another folder which contains pictures. PTXprint will also scan the selected folder (and all its sub-folders) looking for all the required illustrations in the Picture List.

The chosen folder is shown beside the button.

###### Exclude Subfolders

Checkbox, off · Regular+ · `c_exclusiveFiguresFolder` · cfg `document/exclusivefolder`  
Also: Pictures: Exclusively Use Selected Folder · Needs: “Use Other Location”, “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> PTXprint normally searches all the sub-folders of the specified folder locations for the pictures it needs.
>
> If you would prefer that it only searches in the folder specified directly (and NOT look in any subfolders) then select this option. This should speed up searches for images, but may result in some images not being found at all.

This applies when you print, when you make an archive and when PTXprint looks for the PicList files. The downloaded image sets are still searched fully, because each set is in a subfolder of its own. It is unticked automatically when you untick **Use Other Location**.

###### Image Types – Pictures: Preferred image types

Text box · Regular+ · `t_imageTypeOrder` · cfg `document/imagetypepref`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> If multiple versions of an image are located (hk12345B.jpg, hk12345C.png or hk12345B.tif) then which one of these different image types should be used in the publication?
>
> If in doubt, leave this box empty. Then it will use one of two defaults:
>
> 1. Low Resolution Default Order:  
> JPG PNG TIF BMP PDF  (use JPGs first, if none then PNGs, TIFs etc.)
>
> 2. High Resolution Default Order:  
> TIF PNG JPG BMP PDF (use TIFs first, if none then PNGs, JPGs etc.)
>
> Or manually type in a custom order, for example:  
> PDF TIF PNG (use PDFs first, otherwise TIFs, or PNGs)  
>   or JPG  (only use JPGs - ignore all other file types)  
>   or TIF  (only use TIFs - ignore all other file types)
>
> NOTE: TIF files are converted internally to hi-res JPGs.
>
> You can specify your preference for which kinds of images are used. PTXprint will search multiple locations for any matching images, and use the one that best matches your preferences (if found).
>
> If the box is left empty, it will default to the following search sequences:  
>    jpg > png > tif > bmp > pdf   - for smallest file size or  
>    tif > png > jpg > bmp > pdf   - for largest file size

Separate the types with spaces.

#### Details

##### Anchor Ref – Picture: Anchor reference

Text box · Regular+ · `t_plAnchor`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> The anchor specifies what page in a book a picture will appear on. It appears on the same page as its anchor in the text. You can alter the Anchor Ref by a few verses to change the page on which it appears.
>
> An Anchor Ref must consist of a book code, perhaps followed by L or R (in the case of a diglot), then a space, then an in-book location which contains a dot (period). In a scripture book, the in-book location is Chap.Verse where the Verse matches the \v value precisely. In other books, the in-book location can be anything as long as it is unique in that book and contains a dot (period).
>
> Anchor Refs for Diglots use the L or R suffix on the 3-letter book code to indicate whether the picture is to be associated with the Primary (L) text or the Secondary (R) text.
>
> In the glossary book (GLO) there is special support for \k Keywords\k* where in-book location of k.keyword(s) will anchor a picture to the corresponding term. The in-book location must match the value of the \k Keyword or phrase\k* with its spaces removed. For example,
>
>     GLO k.Altar - would link it to \k Altar\k*  
>     GLO k.JohntheBaptist - would link a picture to  
>                a glossary entry \k John the Baptist\k*
>
> You can copy-and-paste a glossary word or phrase after typing GLO k. and PTXprint will automatically strip the spaces for you.
>
> Where there are no intervening anchors, you can anchor to the Nth paragraph of e.g. poetry or a keyterm definition, by specifying the paragraph number after an = sign. For example, GLO k.Harp=2 or PSA 23.4=3. This can avoid the need to insert an explicit milestone to anchor a cutout if there is a page or column break after the start of the verse.

PTXprint changes `:` into `.` and the book code into capital letters for you. If the anchor is empty, you cannot move to another row. See "Details" above for the diglot, glossary and paragraph forms.

##### Caption Ref – Picture: Caption reference

Text box · Regular+ · `t_plRef`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> The reference in the caption can be a single Ch:Vs or a range of verses 6:17-29. This Caption Ref is different from and independent of the Anchor Ref setting.
>
> By default, the caption will be followed by a Ch:Vs reference in parentheses ( ).
>
> To put the Caption Ref BEFORE the caption text, tick 'Ref Before Caption' on the Advanced tab (Other sub-tab, Pictures, Figures, Images, Sidebars).
>
> To prevent Caption Refs from appearing globally, use the Pictures > Global Options tab option:  
>     'Omit References (ch:vs)'

For example `4:39`.

##### Description: (Alt Text) – Picture: Description (alternative text)

Text box · Regular+ · `t_plAltText`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

A short description of what the picture shows. It helps you recognise the picture in the table. Pictures added from the catalogue get the catalogue title here.

##### Filename – Picture: Image filename

Text box · Regular+ · `t_plFilename`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Note that any changes you make to the filename here will NOT automatically be updated in the Paratext USFM files. Please edit/fit the figure information manually in Paratext if you change things here in PTXprint.

The file name only, without a folder. PTXprint looks for it in the picture folders. Changing it updates the preview and the missing-file check.

##### Copyright Attribution – Picture: Copyright attribution

Text box · Regular+ · `t_plCopyright`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> There are several shortcuts you can use:  
>    (c) --> ©  the copyright sign  
>    (r) --> ®  to denote registered trademarks  
>    (tm) --> ™  to denote trademarks in general
>
> For commonly used series of illustrations, PTXprint can automatically generate the appropriate copyright attribution statement(s) as part of the colophon text.
>
> For other less-known artists' you may enter the appropriate copyright information which is usually in the format of:  
>    by Artist Name © Year, Entity Name and License Type.

Used in the credits that `\zimagecopyrights` prints in the colophon. For known series this box is hidden and **Automatic** is shown instead.

##### Scale – Picture: Scale

Number · Regular+ · `s_plScale`  
Values: 5–200 (default 100) · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> An image (illustration) can be scaled to the given size. This is particularly useful for cutout images, and can prevent them from taking up too much space within the text.

100% fills the frame width. Use 30–60% for cutouts and small pictures. If the row turns red, the picture is too tall for the page; reduce the scale.

##### Vertical Position – Picture: Vertical position

Drop-down · Regular+ · `fcb_plPgPos`  
Choices: Top | Bottom | Below Notes | Before Verse | After Paragraph | Cutout · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Several options here are extensions to the normal USFM markup standard for illustrations and are not expected to work in other software. But PTXprint allows a greater level of control in placing pictures.
>
> Top: Above everything except the header line Bottom: Below all verse text (and footnotes in diglot) Below Notes: Below the footnotes (Span Width only) Before Verse: 'Here' where defined or before its Anchor Ref After Paragraph: After this paragraph Cutout: A notch/corner cut out of the text, starting at current line
>
> The above options may have other positioning parameters such as: Left, Right, Center, no. of lines (up or down).
>
> Several options here are extensions to the normal USFM markup standard for illustrations and are not expected to work in other software. But PTXprint allows a greater level of control in placing pictures.
>
> Top: Above everything except the header line Bottom: Below all verse text (and footnotes in diglot) Before Verse: 'Here' where defined or before its Anchor Ref After Paragraph: After this paragraph Cutout: A notch/corner cut out of the text, starting at current line
>
> The above options may have other positioning parameters such as: Left, Right, Center, no. of lines (up or down).

The choices depend on **Frame Size**: Span Width allows **Top**, **Bottom** and **Below Notes**; Column Width allows **Top**, **Bottom**, **Before Verse**, **After Paragraph** and **Cutout**; the page sizes allow **Top**, **Center** and **Bottom**.

##### Frame Size – Picture: Frame size

Drop-down · Regular+ · `fcb_plSize`  
Choices: Column Width | Span Width | Page (in Margins) | Page (to Edge) · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> The frame size determines the boundaries of where the picture will appear on the page.
>
> Span Width only allows a Top or Bottom vertical placement.
>
> Column Width allows several other more precise placement options: Before Verse, After Paragraph, or Cutout; and these can have Left/Inner or Right/Outer Horizontal positioning set.
>
> Page (in Margins) is intended for pictures that will cover an entire page (i.e. preventing any scripture text from being on that page), but will still show the header.
>
> Page (to Edge) is intended for pictures (or more commonly for maps) to fill the entire page, with no margins at all. Captions should not be used with 'Page (to Edge)' images.
>
> The frame size determines how large the picture will appear on the page.
>
> Span Width only allows a Top or Bottom vertical placement. Column Width allows several other more precise placement options: Before Verse, After Paragraph, or Cutout; and these can have Left/Inner or Right/Outer Horizontal positioning set.
>
> When using single column layout, there is no difference between Column Width and Span Width.

Choose this first, because it changes the choices in **Vertical Position** and **Horizontal Position**. Use **Page (to Edge)** for full-page maps.

##### Horizontal Position – Picture: Horizontal position

Drop-down · Regular+ · `fcb_plHoriz`  
Choices: Left | Center | Right | Inner | Outer | - · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> The options available here change based on the Frame Size and Vertical Position settings. So if you can't find an option you are looking for, then check those settings first.

Inner and outer keep a picture on the same side relative to the binding when pages are mirrored. Greyed out for **Span Width**. **Center** is only offered for **Before Verse**, **After Paragraph** and the page sizes.

##### Mirror

Label · Regular+  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> It is good typesetting practice to make people look outwards from the gutter, so you can set whether the image is to be mirrored just on odd pages or even pages.
>
> Some artists' pictures do not take into account the "dirty left-hand" culture. For example, it would be "awkward" to use a picture where Jesus is healing a person using his LEFT hand! What an insult!
>
> So this option allows the image to be mirrored (on both pages) in order to make the left become right. But you should check carefully to see what other unwanted side effects this mirroring may cause.
>
> Note: This option will be grayed out if the picture has the "Never Mirror" setting checked on the Checklist tab.

##### Mirror – Picture: Mirroring options

Drop-down · Regular+ · `fcb_plMirror`  
Choices: Never | Odd | Even | Always · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Never = The image will never be mirrored Odd = Mirrored only if image ends up on an odd page Even = Mirrored only if image ends up on an even page Always = Always mirrored (regardless of where it ends up)
>
> Note that if this option is grayed out, it is because you have already restricted the mirroring options on the Checklist tab.

**Odd** or **Even** may need the PDF to be made twice to be right. Check the flipped picture carefully: writing in it will be backwards.

##### Number of Lines

Label · Regular+ · `l_plOffsetNum`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Some vertical position options allow a picture to be moved up or down by a number of lines or paragraphs.
>
> -Negative (minus) values specify to move UP. +Positive (plus) values specify to move DOWN.
>
> Negative counts for cutouts raise the image, but the cutout will not affect earlier paragraphs. Note that negative and fractional paragraph counts are invalid.

The label for **Number of Lines**. It changes to "Number of paragraphs" when **Vertical Position** is **After Paragraph**.

##### Number of Lines – Picture: Lines to adjust vertically

Number · Regular+ · `s_plLines`  
Values: -24–24 · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Some vertical position options allow a picture to be moved up or down by a number of lines or paragraphs.
>
> -Negative (minus) values specify to move UP. +Positive (plus) values specify to move DOWN.
>
> Negative counts for cutouts raise the image, but the cutout will not affect earlier paragraphs. Note that negative and fractional paragraph counts are invalid.

Only used with **Cutout** and **After Paragraph**. For a cutout, it is the number of lines below the start of the paragraph where the picture starts (decimals allowed). For **After Paragraph**, it is the number of paragraphs (whole numbers only).

##### Print

Checkbox, off · Regular+ · `c_plMediaP`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Can be used in Print/PDF publications.

Untick it to leave this picture out of print without deleting it from the PicList. Greyed out if the artist's licence does not allow this use. If you untick **Print**, **App** and **Web**, all three stay unticked when you open the project again.

##### App

Checkbox, off · Regular+ · `c_plMediaA`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Can be used in mobile phone Apps.

It does not change the PDF. Greyed out if the artist's licence does not allow this use.

##### Web

Checkbox, off · Regular+ · `c_plMediaW`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Can be used on websites.

It does not change the PDF. Greyed out if the artist's licence does not allow this use.

##### Automatic

Label · Regular+ · `l_autoCopyAttrib`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> If the image is from the recognized set of pictures commonly used in Scripture publications, then there is no need to fill in the Copyright Attribution field, as this will be generated automatically for you.

Shown instead of the **Copyright Attribution** box for a series that PTXprint knows.

##### © ...

Button · Regular+ · `btn_overlayCredit`  
Also: Picture: Credit overlay options · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Credit Overlays... Some artists (e.g. David C Cook) require that each image has a copyright message printed on the image itself. The text and location can be set here.

Opens the **Illustration Credit Overlay** dialog.

##### Automatic – Picture: Credit overlay position and style

Text box · Regular+ · `t_piccreditbox`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Credit overlay position and style

The current overlay settings in short form: position, rotation and box (for example `bl,0,None`). Use the **© ...** button to change them.

##### Caption – Picture: Caption

Text box · Regular+ · `t_plCaption`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> By default the caption will appear below the picture. To show it above the picture, tick 'Show Caption Before Image' on the Advanced tab (Other sub-tab, Pictures, Figures, Images, Sidebars).
>
> Note that captions are NOT processed by any changes specified in the PrintDraftChanges.txt file.

Changes here are not copied back to Paratext.

##### \fig

Link · Regular+ · `lb_style_fig`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Click to edit the Figure Caption properties on the Styles tab.

Change the caption font, size and alignment there.

##### Extra – Picture: Additional attributes

Text box · Regular+ · `t_picXetex`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> One or more optional (x-xetex) attributes can be applied for rotation and/or PDF page selection. For example:  
> rotated 90     - anti-clockwise rotate=edge     - top to outside edge rotate=binding    - top to binding edge page=2     - select page 2 of multi-page PDF
>
> Multiple parameters should be space-separated:  
> rotate=binding page=2

The caption is not rotated.

#### Checklist

##### Questions to Consider

Label · Regular+  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Pictures are best used in situations where:  
> 1. The physical situation is not understood, or not common in the target culture.  
> 2. Where the physical situation is important to understanding the meaning of the passage (e.g., the type of clothing is often not important, but in some passages it might be).  
> 3. Where they help the reader to understand the passage.  
> 4. Where it entices the reader to read the passage.

##### Questions to Consider

###### Across Various Publications

Label · Regular+  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> First consider whether this picture is appropriate and culturally acceptable in any publications for this project.

###### Yes

Radio · Regular+ · `r_picclear_yes`  
Also: Picture checklist: What is happening is clear · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

This answer is shared by all configurations of the project.

###### No

Radio · Regular+ · `r_picclear_no`  
Also: Picture checklist: What is happening is NOT clear · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Is there anything confusing or misleading in this image that the reader might misunderstand if they look at this picture apart from the text? Yes and no are both appropriate answers as some images may need to be seen alongside text in order to be understood.

This answer is shared by all configurations of the project.

###### Unknown

Radio · Regular+ · `r_picclear_unknown`  
Also: Picture checklist: Not checked for clarity · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

The starting value. Pictures with this answer appear in the "Unknown / Unchecked" filters.

###### In This Publication

Label · Regular+  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Now consider whether there are any issues with using this picture in this particular publication (config-specific).

###### Is this image acceptable in your culture? – Picture checklist: Cultural acceptability

Drop-down · Regular+ · `fcb_picaccept`  
Choices: Unknown | Culturally Appropriate | Alien but Acceptable | Inappropriate · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Select the level to which this illustration is acceptable in the receptor culture.
>
> Be sure that there is nothing offensive or inappropriate in this image. This could be the way people are clothed, what actions they are doing, how they are depicted, etc. “Culturally Appropriate” means this image is in a style from this culture or a related one, “Acceptable” means this picture might be from a different culture or in a different style, but there are no issues using it. “Inappropriate” means there are issues that should prevent this image from being used. Answering “Inappropriate” will help avoid this image being used in other publications.

This answer is shared by all configurations of the project.

###### OK to mirror

Radio · Regular+ · `r_picreverse_OK`  
Also: Picture checklist: Can mirror if needed · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> It is fine to mirror the image if needed. It would not change the impact or response of the readers.

The **Mirror** list on the **Details** sub-tab can then be used freely.

###### Never mirror

Radio · Regular+ · `r_picreverse_never`  
Also: Picture checklist: Never mirror · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Ensure that this image is always shown as currently depicted in the preview. Do NOT allow it to be mirrored (reversed).

For example because it contains writing. The **Mirror** list on the **Details** sub-tab is set to **Never** and greyed out.

###### Always mirror

Radio · Regular+ · `r_picreverse_always`  
Also: Picture checklist: Always mirror · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Ensure that this image is always mirrored from what is currently shown in the preview. Therefore actions being done with the left hand will show as being done with the right hand, and vice versa.
>
> Sometimes mirroring (reversing) an image makes it acceptable since a left hand becomes a right hand, etc.
>
> Some artists' pictures do not take into account the "dirty left-hand" culture. For example, it would be "awkward" to use a picture where Jesus is healing a person using his left hand!

The **Mirror** list on the **Details** sub-tab is set to **Always** and greyed out.

###### Is this picture intended for: clarification, story enhancement, filler, unknown? – Picture checklist: Purpose of illustration

Drop-down · Regular+ · `fcb_pubusage`  
Choices: Unknown | Clarification | Story Enhancement | Space Filler · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Select the reason for including the illustration in this particular publication.
>
> Consider how this image is used alongside the text and what function it serves. Maybe it depicts a building or item from a biblical culture, or a scene from a story.

This answer belongs to the current configuration.

###### Yes

Radio · Regular+ · `r_pubclear_yes`  
Also: Picture checklist: What is happening is clear in this context · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

Saved for the current configuration.

###### No

Radio · Regular+ · `r_pubclear_no`  
Also: Picture checklist: What is happening is NOT clear in this context · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Does the image support what the text is saying? As they read the passage does the image help in their understanding?

Consider another picture or another position.

###### Unchecked

Radio · Regular+ · `r_pubclear_unchecked`  
Also: Picture checklist: Not checked for clarity in this context · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

Not checked yet for this publication. This is the starting value.

###### Yes

Radio · Regular+ · `r_pubnoise_yes`  
Also: Picture checklist: Carries wrong meaning in this context · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> For example, do the colors have the same meaning in the local culture? Is there anything in the background that is distracting from the story? Are there any objects, gestures, or other things that imply something unintended or that isn’t in the passage? Are there any anachronisms in the picture (a minaret in Bethlehem)?

Consider changing or removing the picture.

###### No

Radio · Regular+ · `r_pubnoise_no`  
Also: Picture checklist: Carries expected meaning in this context · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

The picture gives the expected meaning here.

###### Is the image appropriate for the publication? – Picture checklist: Appropriateness of illustration

Drop-down · Regular+ · `fcb_pubaccept`  
Choices: Unknown | Culturally Appropriate | Alien but Acceptable | Inappropriate · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Select the appropriateness of the illustration within this publication.
>
> Do the images and their style fit with the type of publication, i.e. Scripture, children’s materials, lectionary, etc.? Are people and actions depicted in acceptable ways?

This answer belongs to the current configuration.

###### Unchecked

Radio · Regular+ · `r_pubnoise_unchecked`  
Also: Picture checklist: Not checked if wrong meaning in this context · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

Not checked yet for this publication. This is the starting value.

###### Consultant Approval

Label · Regular+  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Now consider whether there are any issues with using this picture in this particular publication (config-specific).

###### Picture checklist: Approved by date

Text box · Regular+ · `t_pubApprDate`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> The most recent date that the consultant approval updated.

Type it when you tick **Approved to be used in**.

###### Picture checklist: Approved by initials

Text box · Regular+ · `t_pubInits`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

The initials of the person (usually the consultant) who approved the picture.

###### any publication

Radio · Regular+ · `r_pubapprove_scopeAny`  
Also: Picture checklist: Approved for use in ANY publication · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

Use it when the picture is fine in every context.

###### this publication

Radio · Regular+ · `r_pubapprove_scopeThis`  
Also: Picture checklist: Approved for use in THIS publication · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

The approval is only for the current configuration.

###### Approved to be used in

Checkbox, off · Regular+ · `c_pubApproved`  
Also: Picture checklist: Approved for use · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

Then choose **any publication** or **this publication**, and type the initials and date. Approved pictures appear when you choose **Approved** in **Filter Checklist**.

###### textv_picNotes

Text area · Regular+ · `textv_picNotes`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

Free notes about the selected picture, for example questions for the consultant and the answers. They are saved with the current configuration only. Other configurations have their own notes for the same picture.

###### Notes About This Picture

Label · Regular+  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Use the notes area below to record anything about this picture, or to dialog with the consultant. The notes entered here are saved with this configuration only (other configurations have their own).


# 11. Diglot tab (two or more languages)

## 11.1 What this tab is for

A **diglot** is a publication with two texts side by side on the page. The texts can be two languages, two scripts of the same language, or two translations. A **polyglot** has three or more texts. PTXprint lines the texts up so that the same verses (or paragraphs) start at the same height in each column.

Each text in a diglot comes from its own Paratext project and uses its own PTXprint configuration. The configuration you have open when you tick **Diglot (or Polyglot)** becomes the **primary** text (code **L**). The other texts are **secondary** texts (code **R**, then **A**, **B**, **C** …). The primary configuration controls the page: page size, margins, headers and footers, and most layout settings. Each secondary configuration controls how its own text looks: its fonts, font size, line spacing, footnotes and so on.

Come to this tab to turn a configuration into a diglot, choose the other project(s), set the column widths, and choose how the texts are merged (joined together). The **Diglot** tab is shown in the **Regular** and **Full** views only. When **Diglot (or Polyglot)** is ticked, the tab name turns blue.

**Important:** turning a diglot on cannot simply be undone. Before you start, go to the **Basic** tab, **Layout Configuration** area, and use **Save As** to make a new configuration for the diglot, so your normal (single-text) configuration stays as it is.

## 11.2 Diglot (or Polyglot)

The **Diglot (or Polyglot)** checkbox is in the frame title. All other settings on the tab are hidden until it is ticked.

When you tick it:

1. PTXprint asks you to confirm. Click **Yes** to continue, or **No** to stop.
2. A table appears with two rows: **L** (your current project and configuration) and **R** (empty).
3. PTXprint opens the **Project** list for the **R** row so you can choose the secondary project.
4. On the **Layout** tab, **Two Column Layout** is ticked and greyed out. A diglot always uses two (or more) columns. The gutter (the space between the columns) and **Vertical Rule in Gutter** on the **Layout** tab now control the space and the line between the texts.

If you later untick the box, PTXprint does not turn the diglot off. Instead it opens the **Save As Monoglot** dialog (see below).

## 11.3 The texts table

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

## 11.4 Layout

The **Layout** text box describes where each text goes. PTXprint fills it in for you from the **1|2** column, so most people never need to type in it.

* Letters next to each other share a page, side by side. **LR** means L on the left and R on the right of every page.
* A comma starts the next page of the spread. **L,R** means L fills the left page and R fills the facing right page.
* A hyphen **-** is a page with no Bible text.

Every code in the table must appear in the layout, and L and R must always be there. If the layout has a problem, the preview shows a red **Layout Error** box with the reason, for example "Missing: A", "L or R missing", "Spaces not allowed" or "Comma required for multi-page spread". The check runs when you leave the box.

## 11.5 Merging mode

Before printing, PTXprint merges the texts into one file, in "chunks" that should line up across the columns. **Merging mode** chooses how the chunks are made:

* **Chapter Verse** – lines the texts up on chapters and verses. Only offered for a diglot (two texts).
* **Scored** – the default. It uses a scoring method and also tries to line up paragraphs where the verse numbers match. This usually gives the best result.
* **Scored (Chapter)** – like **Scored**, but always lines up at the start of each chapter.
* **Scored (Verse)** – like **Scored**, but lines up at every verse. This can leave many small gaps.

For a polyglot (three or more texts), only the three **Scored** options are offered.

## 11.6 Column widths and auto-balance

Two texts rarely take the same amount of space. One language may need 20% more words than the other. If both columns are 50% wide, the shorter text has white space under every chunk. To fix this, give the longer text more width in the **% Width** column (for example 55 and 45), or make its font size or line spacing a little smaller.

The **Auto-calculate optimum widths of diglot columns** button does this for you. It prints the job 10 or more times, trying widths near the current ones, and keeps the widths that give the fewest pages. So select one short book on the main window before you click it. The button only works for a diglot with exactly two texts, and only when the **Print** button is available. When it has finished, the button is released, and you can use it again (for example after you change a font size).

## 11.7 Notes, headers and other options

* **Separate Notes in Two Columns** (ticked by default) keeps each text's footnotes under its own column. If you untick it, the footnotes of all texts are put together in one notes area, one after another. This can be useful when only one of the texts has footnotes.
* **Vertical Rule in Notes Area** draws a line between the separate notes columns. **Join with Rule Above** makes this line meet the line between the text columns, so there is no small gap. The text-column line itself is **Vertical Rule in Gutter** on the **Layout** tab.
* **Adjust Center Header Based on Column Widths** moves the centre part of the header (and footer) so that it sits above the gutter, when the two columns have different widths.
* **Use Serial Layout for These Books** lists books that should not be merged. For these books PTXprint prints the whole book in the primary text, then the whole book in the secondary text, one after the other. Use this for front matter, introductions, glossaries and other back matter. The default list is **FRT BAK GLO XXA XXB**.

## 11.8 Changing the settings of a secondary text

The look of each secondary text (fonts, font size, line spacing, footnote settings, styles, and so on) comes from its own configuration. To change it:

1. On the **Diglot** tab, right-click the row of that text and choose **Edit Settings…**.
2. The PTXprint window now shows the secondary project and configuration. The big **Print** button changes to **Return to Primary**. A small **Print** button appears next to it.
3. Change the settings you need, for example on the **Fonts+Scripts** tab or the **Styles** tab.
4. If you want to check this text by itself, click the small **Print** button. It makes a PDF of the secondary text only.
5. Click **Return to Primary** to go back to the primary configuration. Then click **Print** to make the diglot PDF.

Some settings always come from the primary configuration, whatever the secondary configuration says. These include the page size, margins, header and footer positions, the footnote rule, where cross-references go, page breaks before chapter 1, book introductions and the outline, parallel passage references and the chapter range. The page border and the centre footer of the secondary text are also turned off. So change these in the primary configuration.

## 11.9 What happens to pictures, notes and headers

**Pictures.** Pictures come from each text's own picture list. If both texts have the same picture file at the same verse, PTXprint prints it once. The primary caption is used, and the secondary caption is added if **Captions** is ticked for that text. If a picture is only in one text, or uses a different file, it is printed in that text's column. Pictures are not shared in the books listed in **Use Serial Layout for These Books**, because those books are printed one text after the other. There, each text keeps its own pictures and captions. On the **Pictures** tab, the picture list shows the secondary caption in the **Sec.Caption** column, and pictures that belong only to a secondary text have the text's code after the book code in the anchor (for example **MATR 5.3**).

**Notes.** Whether a text has footnotes and cross-references depends on that text's own configuration (its **Notes+Refs** settings). The layout of the notes area (separate or together, rules) is set on this tab.

**Headers and footers.** The headers and footers are set in the primary configuration, on the **Header+Footer** tab. When diglot is on, each header part has **Pri** and **Sec** buttons. Choose **Pri** to use the primary text (its references and its font) for that part, or **Sec** to use the secondary text. If **Mirror Pages** is ticked on the **Layout** tab, the texts also swap sides on even pages, so each text stays on the same side relative to the binding.

**Front matter.** The **Generate Front Matter** dialog (Peripherals tab) offers a **DIGLOT** template when diglot is on.

## 11.10 Auto Page Fill for diglots and polyglots (experimental)

The **Auto Page Fill** tool in the PDF Preview window (see the chapter on the PDF Preview window) also works for a diglot or polyglot. When **Diglot (or Polyglot)** is ticked, PTXprint uses a special version of the tool. It tries to fill each page, and it also tries to keep the texts side by side at the same height, so that each chunk ends at about the same line in every column. This version is new and experimental. Check the result carefully, and fix the pages it could not fill by hand.

On the **Advanced** tab, **Other** sub-tab, in the **Automatic Page Filler** area, **The cost of imbalance in a polyglot slice** sets how important it is that the columns end at the same height. A higher value makes the tool try harder to keep the columns even. A lower value lets it accept columns of different heights if the paragraphs look better. This setting is only used for diglots and polyglots.

## 11.11 Save As Monoglot

You cannot just switch a diglot off, because that would lose all the diglot settings. When you untick **Diglot (or Polyglot)**, the **Save As Monoglot** dialog opens instead:

* Click **Cancel** to keep the diglot as it is.
* Or type a name for a new configuration and click **OK**. PTXprint saves a copy of the current settings under that name, with diglot turned off, and opens it. Your diglot configuration is left unchanged.

## 11.12 Common tasks

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

## 11.13 Common problems

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

## 11.14 Settings reference

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


# 12. Tabs+Borders tab

## 12.1 What this tab is for

This tab adds two kinds of decoration:

* **Thumb Tabs** – coloured blocks at the outer edge of the page, with a short book name in them. When the book is closed, the reader sees the blocks on the edge of the paper and can open the book near the right Bible book. They are useful in long publications such as a whole Bible or a New Testament.
* **Ornamental Decorations** – a border around the page or the text, a graphic behind section headings, a decoration at the end of each book, decorated verse numbers, and borders around book titles. Some cultures value such decoration highly in Scripture publications.

Each area is collapsed until you tick its checkbox; until then you only see a short description. The tab name shows **Tabs** and **Borders**, and each word turns blue when that feature is on. The tab is shown in the **Regular** and **Full** views.

This chapter also describes the **Border Settings** dialog, which sets the look of a border (lines, ornaments, colours and padding). You open it from the **Styles** tab with the **Borders...** button.

"pt" means point; 1 pt is about 0.35 mm. Thumb tab sizes are in mm.

## 12.2 Thumb Tabs

**Where the tabs go.** Each Scripture book gets a tab position, counting down from the top of the page: the first book at position 1 (top), the next at position 2, and so on. When the positions run out, the next book starts again at the top. Front matter, glossaries and other non-Scripture books get no tab. Positions are worked out from all the books in the multiple-book list on the main window, even if you print only one book. So the tab for Mark is in the same place whether you print the whole NT or only Mark.

**Size.** For normal tabs, **Height** is the size along the page edge and **Length** is how far the tab reaches in from the edge. For rotated tabs it is the other way round.

**Number of Tab Positions** is how many tabs fit down the page. PTXprint recalculates it from the page height, the top and bottom margins and the tab size whenever these change. Bigger = tabs overlap; smaller = tabs spread apart.

**Grouped Tabs.** Many Bible books are short, so giving each its own position would need too many positions. Neighbouring short books can share one position, and each still has its own name in the tab. The **Grouped Tabs** button restores PTXprint's default groups.

**Restart Tabs at MAT** starts a new cycle at Matthew, so the New Testament tabs start again at the top.

**Rotate Tabs** turns the text to run along the page edge (good for narrow margins and longer names). The drop-down list next to it chooses which way the text faces on left and right pages. The preview on the tab shows facing pages.

**Only Show on Odd Pages** is for thin paper, so a tab on the back of the page does not show through.

**Tab text and colour.** By default the tab text is the short book name from each book's `\toc3` line. **Tab Color** sets only the block colour. The text colour, font and size come from the style: click **Edit Style** to change them on the **Styles** tab. Tabs usually use a dark block with white or light text.

The **\toc3** and **\zthumbtab** options choose where the tab text comes from. If the **Table of Contents** on the **Peripherals** tab is on but does not use `\toc3`, PTXprint selects **\zthumbtab** and greys out both options.

## 12.3 Ornamental Decorations

Tick each kind of decoration you want. A file name next to a **Select...** button shows which graphic is used. Choosing a file ticks that decoration's checkbox for you. The **Select...** buttons open PTXprint's own border-art folder, but you can pick a PDF file from anywhere.

### Section Headings

* **PDF border (Legacy)** – a PDF graphic behind each `\s`, `\s1` and `\s2` heading. **Scale**: 1 = the graphic's own size. **Shift**: in pt, positive = up, negative = down. The graphic does not grow with the heading, so make sure every heading fits, also two-line headings. You may need more space before and after headings on the **Styles** tab.
* **Dynamic Border** – a box around each heading block that grows and shrinks with the heading. It is controlled by the special style `cat:headingsbox|esb`; the link opens it on the **Styles** tab, where you set its background colour and border (**Borders...** button).

### Border

* **PDF border (Legacy)** – a PDF graphic (for example a frame) on every page. It is stretched to the full page if **Full page** is ticked, otherwise to the page size without the binding gutter.
* **Dynamic Border** – a border around the Bible text on each page. Introductions, footnotes and other peripheral material are outside it. It can be plain, double or ornamental. It is controlled by the `textborder` style (**Styles** tab, **Other** category); change it with the **Borders...** button in **Sidebar Settings**.
* **Page Border** – meant to place a border of the same size on every page, whatever the content, controlled by the `\pageborder` style. If you do not get the result you want, use **Dynamic Border** or **PDF border (Legacy)**.

A border takes space, so you will probably need larger margins on the **Layout** tab so it does not touch the text or the paper edge.

### End of Book Decoration

A small graphic after the last verse of each Scripture book. PTXprint suggests its own `decoration.pdf`.

### Verse Number Decorator

* **End of Ayah** – the verse number inside the font's "End of Ayah" character (U+06DD), common in Arabic script. The font must contain this character. **Move Ayah** moves the decorated number to the end of the verse; the `\vp` link opens the style for the moved numbers.
* **Verse Border Graphic** – a small PDF graphic (for example a star) behind each verse number, adjusted with **Scale** and **Shift** (pt, positive = up).

The `\v` link opens the verse number style. You may need a smaller font size or another colour so the numbers fit inside the decoration.

### Book Title Borders

A border around the book title (`\mt1` and `\mt2`), controlled by the special style `cat:titlebox|esb`. The link opens it on the **Styles** tab to change its colours and border.

## 12.4 Border Settings dialog

The dialog belongs to a style on the **Styles** tab. To open it, select the style (for example a sidebar style, `textborder`, `cat:headingsbox|esb` or `cat:titlebox|esb`), open **Sidebar Settings**, and click **Borders...**. **OK** saves the changes in that style; **Cancel** leaves the style as it was.

**Borders** area:

* **Type of Border** – **None**, **Plain (single)** (one line), **Double** (two lines) or **Ornamental** (a pattern of ornaments).
* **Left**, **Right**, **Top**, **Bottom**, **Inner**, **Outer** – which sides get a border. Use **Inner**/**Outer** if the border should follow the binding (inner = near the spine). Ticking **Inner** or **Outer** unticks **Left** and **Right**, and the other way round.
* **Border Width**, **Line Thickness**, **Line Color**, **Fill Color**, and **Select Ornamental Border** (the pattern, only for **Ornamental**) – see the control notes. **Ornamental Border Style** opens the ornaments catalogue (a PDF).

**Padding** area, on two tabs:

* **Box** – space between the edge of the box (its background colour) and the text inside it.
* **Border** – space between the inside edge of the border and the box inside it.

Each tab has four values in a cross: top, bottom, left (or inner) and right (or outer), in pt. **Uniform Box Padding** / **Uniform Border Padding** use the top value for all four sides and grey out the other three. Negative values are allowed. The picture in the dialog shows the effect.

## 12.5 Common tasks

### Add thumb tabs to a Bible or New Testament

1. On the main window, select all the books in the multiple-book list.
2. On the **Tabs+Borders** tab, tick **Thumb Tabs**.
3. Set **Height** and **Length** (for example 8 mm and 15 mm).
4. Choose a dark **Tab Color**.
5. Click **Edit Style** and set a light text colour (for example white).
6. Print and look at the outer edge of the pages.

### Let short books share a tab position

1. Tick **Thumb Tabs**.
2. Click the **Grouped Tabs** button for the default groups, or type your own in the **Grouped Tabs** box, for example `PHM TIT; 1JN 2JN 3JN JUD`.
3. Print. Each group uses one position, but each book keeps its own name.

### Make the text in the tabs run along the page edge

1. Tick **Rotate Tabs**.
2. In the drop-down list next to it, choose how the text faces, for example **Each Facing Outward**.
3. Check the preview on the tab, then print.

### Start the New Testament tabs at the top again

Tick **Restart Tabs at MAT** and print.

### Put a decorative border around the Bible text

1. Tick **Ornamental Decorations**, then **Border**, and choose **Dynamic Border**.
2. On the **Styles** tab, select the `textborder` style (in the **Other** category).
3. Open **Sidebar Settings** and click **Borders...**.
4. Choose the **Type of Border** (for example **Ornamental**), the ornament, the **Border Width** (at least 10 pt for ornaments) and the colours. Click **OK**.
5. On the **Layout** tab, make the margins larger if the border is too close to the text or the paper edge.
6. Print.

### Use a ready-made PDF frame on every page

1. Tick **Ornamental Decorations**, then **Border**.
2. Choose **PDF border (Legacy)**, click **Select...** and choose the PDF file.
3. Tick **Full page** if the frame should cover the whole page.
4. Make the margins larger on the **Layout** tab if needed, then print.

### Decorate the verse numbers

1. Tick **Ornamental Decorations**, then **Verse Number Decorator**.
2. Choose **Verse Border Graphic** and click **Select...** to choose a small PDF graphic. (For Arabic script, you can choose **End of Ayah** instead.)
3. Print. If the number does not fit, change **Scale** and **Shift**, or click the `\v` link to make the verse numbers smaller.

### Add a graphic at the end of each book

1. Tick **Ornamental Decorations**, then **End of Book Decoration**.
2. Click **Select...**, choose a PDF graphic, and print.

### Put a border around book titles or section headings

1. Tick **Ornamental Decorations**.
2. Tick **Book Title Borders**, or tick **Section Headings** and choose **Dynamic Border**.
3. Click the style link (`cat:titlebox|esb` or `cat:headingsbox|esb`). The **Styles** tab opens with that style selected.
4. Change the background colour, and click **Borders...** in **Sidebar Settings** to change the border.
5. Print.

## 12.6 Common problems

**I cannot see the thumb tab or ornament settings.**
Tick **Thumb Tabs** or **Ornamental Decorations**. If the whole tab is missing, change the view level to **Regular** or **Full**.

**The thumb tabs overlap each other, or there are big gaps between them.**
Change **Number of Tab Positions** (larger = closer and may overlap, smaller = further apart), or change **Height** (or **Length** for rotated tabs). Group short books in **Grouped Tabs**, or tick **Restart Tabs at MAT**.

**My value for Number of Tab Positions keeps changing.**
PTXprint recalculates it whenever the tab size, page size or margins change. Set those first, then adjust this number last.

**The thumb tab is blank.**
The book has no `\toc3` line, or it has an empty `\zthumbtab` line. If the table of contents does not use `\toc3`, the `\toc3` text is removed and cannot be used for the tabs. On the **Peripherals** tab, include `\toc3` in the table of contents, or add the tab text with `\zthumbtab` in the book (in Paratext).

**The \toc3 and \zthumbtab options are greyed out.**
The table of contents on the **Peripherals** tab is on but does not use `\toc3`. Tick `\toc3` there.

**When I print one book, its tab is not at the top.**
This is on purpose: positions come from all the books in the multiple-book list, so each tab stays in the same place in every print.

**I cannot change the colour of the tab text with Tab Color.**
**Tab Color** sets only the block. Click **Edit Style** and change the text colour there.

**Message: "Warning: Could not locate decorative PDF(s)".**
A decoration is ticked but its PDF file is missing or was moved. Choose the file again with that decoration's **Select...** button, or untick the decoration.

**The border touches or covers the text.**
Make the margins larger on the **Layout** tab. For a dynamic border, also increase the padding in the **Border Settings** dialog.

**The ornamental border looks broken or squashed.**
Make the **Border Width** at least 10 pt in the **Border Settings** dialog.

**The section heading graphic does not fit the heading.**
Change **Scale** and **Shift**. If headings are sometimes two lines long, use **Dynamic Border** instead of **PDF border (Legacy)**.

**The decorated verse numbers show empty boxes.**
With **End of Ayah**, the font does not have the End of Ayah character (U+06DD). Choose a font that has it, or use **Verse Border Graphic**.

**The verse number does not fit inside the verse graphic.**
Increase **Scale**, adjust **Shift**, or click the `\v` link and make the verse number font smaller.

**A Select... button or a Shift/Scale box is greyed out.**
Choose **PDF border (Legacy)** or **Verse Border Graphic** first.

**Clicking the \pageborder link does nothing.**
This link does not open the style. Go to the **Styles** tab and select the page border style yourself. (The **\textborder** link does open the `textborder` style.)

## 12.7 Settings reference

### Border Settings (dialog)

#### OK

Button · Regular+ · `btn_border_ok`

Saves the border settings in the selected style and closes the dialog.

#### Cancel

Button · Regular+ · `btn_border_cancel`

Closes the dialog without changing the style.

#### Borders

##### Left – Borders dialog: Show LEFT border

Checkbox, on · Regular+ · `c_sbBorder_lhs`

Ticking it unticks **Inner** and **Outer**. Use **Left** and **Right** when the border does not need to follow the binding.

##### Right

Checkbox, on · Regular+ · `c_sbBorder_rhs`  
Also: Borders dialog: Show RIGHT border

Ticking it unticks **Inner** and **Outer**.

##### Top

Checkbox, on · Regular+ · `c_sbBorder_top`  
Also: Borders dialog: Show TOP border

Draws the border along the top.

##### Bottom

Checkbox, on · Regular+ · `c_sbBorder_bot`  
Also: Borders dialog: Show BOTTOM border

Draws the border along the bottom.

##### Outer

Checkbox, off · Regular+ · `c_sbBorder_out`  
Also: Borders dialog: Show OUTER border

Away from the spine. Ticking it unticks **Left** and **Right**.

##### Inner – Borders dialog: Show INNER border

Checkbox, off · Regular+ · `c_sbBorder_inn`

Near the spine, so it changes between left and right pages. Ticking it unticks **Left** and **Right**.

##### Border Width (pt) – Borders dialog: Border width

Number · Regular+ · `s_sbBorderWidth`  
Values: 0.1–200 (default 2)

> Specify how wide the border should be. Note that for ornamental borders this value needs to be at least 10pt.

For **Plain** this is the thickness of the line.

##### Line Color – Borders dialog: Border line color

Colour · Regular+ · `col_sbBorderColor`

> Sets the line color for this border.

The colour of the border lines.

##### Type of Border – Borders dialog: Border type

Drop-down · Regular+ · `fcb_sbBorderStyle`  
Choices: None | Plain (single) | Double | Ornamental

> None, a plain (single) line, a double line, or an ornamental pattern.

With **None**, most other settings in the dialog are greyed out. **Line Thickness** and **Fill Color** are only used for **Double** and **Ornamental**; the ornament list only for **Ornamental**.

##### Borders dialog: Ornamental border

Drop-down · Regular+ · `fcb_sbBorderOrnament`  
Choices: Han1 | Han2 | Han3 | Han4 | Han5 | Vectorian1 | Vectorian2 | Vectorian3 | Vectorian4 | v85 | v85r | v85out | v86c | v86out | v88 | v88r | v88c | v88out

> A selection of ornamental borders are available to choose from, or a custom-made border may be applied.

**Han** patterns are traditional Chinese-style designs; **Vectorian** and **v…** patterns are Victorian-style. See them in the catalogue (**Ornamental Border Style** link). Only available when **Type of Border** is **Ornamental**.

##### Fill Color – Borders dialog: Border fill color

Colour · Regular+ · `col_sbBorderFillColor`

> Sets the fill color for this border.

Fills a **Double** or **Ornamental** border. Greyed out for **Plain (single)**.

##### Ornamental Border Style

Link · Regular+ · `lb_openOrnamentsCatalog`  
Also: Show the Ornaments Catalog

> Click to open a PDF containing a catalog of the various Ornamental Borders (pgs 4-7).

Pages 4–7 show the ornamental borders in the list.

##### Line Thickness (pt) – Borders dialog: Border Line Thickness

Number · Regular+ · `s_sbBorderLineWidth`

> Specify the thickness of the lines which make up the border.

For **Double** and **Ornamental** borders (default 0.3 pt). Greyed out for **Plain (single)**.

#### Padding

##### Box

###### All/Top (pt)

Label · Regular+

> Top padding (pts). When Uniform Box Padding is ticked, this value is used for all four sides.

###### Borders dialog: Box padding bottom

Number · Regular+ · `s_sbBoxPadB`  
Values: -200–200 (default 8) · Greyed out by: “Uniform Box Padding”

> The space (pts) between the edge of background box (or figure, if any) and the edge of the text in the box.

Bottom padding of the box.

###### Bottom (pt) – Borders dialog: Box padding right

Number · Regular+ · `s_sbBoxPadR`  
Values: -200–200 (default 8) · Greyed out by: “Uniform Box Padding”

> The space (pts) between the edge of background box (or figure, if any) and the edge of the text in the box.
>
> The vertical space (pts) between the top/bottom borders (if any) and the text contained within the box.

Right (or outer) padding of the box.

###### Left/Inner (pt) – Borders dialog: Box padding top

Number · Regular+ · `s_sbBoxPadT`  
Values: -200–200 (default 8)

> The space (pts) between the edge of background box (or figure, if any) and the edge of the text in the box.
>
> The horizontal space (pts) between the left/right borders (if any) and the text contained within the box.

Space between the top edge of the box and the text. With **Uniform Box Padding** it is used for all four sides.

###### Borders dialog: Box padding left

Number · Regular+ · `s_sbBoxPadL`  
Values: -200–200 (default 8) · Greyed out by: “Uniform Box Padding”

> The space (pts) between the edge of background box (or figure, if any) and the edge of the text in the box.

Left (or inner) padding of the box.

###### Right/Outer (pt)

Label · Regular+

> The horizontal space (pts) between the left/right borders (if any) and the text contained within the box.

###### Uniform Box Padding

Checkbox, off · Regular+ · `c_boxPadSymmetrical`

> Use the same value for the Top, Bottom, Left, and Right padding.

Greys out the bottom, left and right boxes.

##### Border

###### All/Top (pt)

Label · Regular+

> Top padding (pts). When Uniform Border Padding is ticked, this value is used for all four sides.

###### Borders dialog: Border padding bottom

Number · Regular+ · `s_sbBdrPadB`  
Values: -200–200 (default 8) · Greyed out by: “Uniform Border Padding”

> The space between the inside edge of the border and the outside edge of the box inside it.

Bottom padding between the border and the box.

###### Bottom (pt) – Borders dialog: Border padding right

Number · Regular+ · `s_sbBdrPadR`  
Values: -200–200 (default 8) · Greyed out by: “Uniform Border Padding”

> The space between the inside edge of the border and the outside edge of the box inside it.
>
> The vertical space (pts) between the top/bottom borders (if any) and the text contained within the box.

Right (or outer) padding between the border and the box.

###### Left/Inner (pt) – Borders dialog: Border padding top

Number · Regular+ · `s_sbBdrPadT`  
Values: -200–200 (default 8)

> The space between the inside edge of the border and the outside edge of the box inside it.
>
> The horizontal space (pts) between the left/right borders (if any) and the text contained within the box.

Top padding between the border and the box. With **Uniform Border Padding** it is used for all four sides. A negative value makes the box reach under the border.

###### Borders dialog: Border padding left

Number · Regular+ · `s_sbBdrPadL`  
Values: -200–200 (default 8) · Greyed out by: “Uniform Border Padding”

> The space between the inside edge of the border and the outside edge of the box inside it.

Left (or inner) padding between the border and the box.

###### Right/Outer (pt)

Label · Regular+

> The horizontal space (pts) between the left/right borders (if any) and the text contained within the box.

###### Uniform Border Padding

Checkbox, off · Regular+ · `c_bdrPadSymmetrical`

> Use the same value for the Top, Bottom, Left, and Right padding.

Greys out the bottom, left and right boxes.

### Tabs+Borders

#### Thumb Tabs

Checkbox, off · Regular+ · `c_thumbtabs` · cfg `thumbtabs/ifthumbtabs`  
Also: Enable thumb tabs · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> Thumb Tabs are sometimes used in longer publications to help the user find a scripture book more easily. By default these use the \toc3 element in a USFM file to provide the text for the tab. Note: If only a single book is currently selected, it will place the Thumb Tab relative to ALL the books listed in the multiple book list.

Only Scripture books get tabs. Thumb tabs are printed to the edge of the paper, so they need a printer that can print or trim to the edge.

#### Ornamental Decorations

Checkbox, off · Regular+ · `c_useOrnaments` · cfg `snippets/fancyborders`  
Also: Ornamental Decorations: Enable decorative borders, rules and verses · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Enable this option to make use of ornamental borders, rules & verses.
>
> Some cultures place a high value on such decorative features in scripture publications.

Most decorations need extra space, so check the margins and heading spacing after you print.

#### Thumb Tabs

##### Height – Thumb tabs: Height

Number · Regular+ · `s_thumbheight` · cfg `thumbtabs/height`  
Values: 3–20 (default 8) · Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> The height of the Thumb Tab measured in millimeters (mm).

Normal tabs: size along the page edge. Rotated tabs: how far the tab reaches in. Changing it recalculates **Number of Tab Positions** (for normal tabs).

##### Tab Color – Thumb tabs: Tab color

Colour · Regular+ · `col_thumbback` · cfg `thumbtabs/background`  
Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> The background color of the tabs. Use a dark color here and set the light text color with the Edit Style link.
>
> Thumb Tabs usually use a dark color for the background with a light color (or white) for the foreground text.
>
> The background color is set here, but the foreground text color needs to be set by clicking the Edit Style link.

A dark colour shows well on the edge of the closed book.

##### Rotate Tabs

Checkbox, off · Regular+ · `c_thumbrotate` · cfg `thumbtabs/rotate`  
Also: Thumb tabs: Rotate tabs · Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> Rotates the tabs so that the text runs along the edge of the page. This works well for narrow margins, but may result in fewer tab positions per page.

Allows longer names in narrow margins. When ticked, the orientation list next to it becomes available.

##### Number of Tab Positions – Thumb tabs: Number of tab positions

Number · Regular+ · `s_thumbtabs` · cfg `thumbtabs/numtabs`  
Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> How many tabs can there be down a page. This is automatically calculated from the Height (or Length when rotated), Page size and Margins. If any of these change then this value will be updated. Increasing it, makes tabs overlap. Reducing it spreads them apart.

PTXprint overwrites your value when the page height, margins or tab size change. After the last position, the next book starts again at the top.

##### Length – Thumb tabs: Length

Number · Regular+ · `s_thumblength` · cfg `thumbtabs/length`  
Values: 3–40 (default 15) · Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> The length of the Thumb Tab measured in millimeters (mm).

Normal tabs: how far the tab reaches in; make it long enough for the longest book name. Rotated tabs: size along the page edge. Changing it recalculates **Number of Tab Positions** (for rotated tabs).

##### Grouped Tabs – Thumb tabs: Tabs grouped by books

Text box · Regular+ · `t_thumbgroups` · cfg `thumbtabs/groups`  
Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> List book IDs of short books to be grouped together at the same tab position. Use spaces between book IDs, and use ; to separate groups. There is no need to list all the book IDs here - only the special ones which need to share the same tab position.
>
> For example: PHM TIT; 1JN 2JN 3JN JUD
>
> When several shorter adjacent books occur, it is common to group them together to use the same tab position (but still have differently named tabs).

Books not listed get their own position.

##### Length – Thumb tabs: Rotate options

Drop-down · Regular+ · `fcb_rotateTabs` · cfg `thumbtabs/rotatetype`  
Choices: Each Facing Outward | Each Facing Inward | Rotate Both Anticlockwise | Rotate Both Clockwise · Needs: “Rotate Tabs”, “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> If you choose to Rotate the tabs, there are various options as to how these should be oriented. The preview (right) will show how these will appear on facing pages.

Outward and inward face opposite ways on left and right pages; the other two turn both pages the same way.

##### Restart Tabs at MAT

Checkbox, off · Regular+ · `c_thumbrestart` · cfg `thumbtabs/restart`  
Also: Thumb tabs: Restart tabs at New Testament · Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> Normally books will follow sequentially and if the next tab would be off the bottom of the page, then it will be set to the top for a new cycle of tabs. Setting this starts a new cycle at the start of the New Testament (Matthew).

Use it in a whole Bible, so the New Testament has its own run of tabs.

##### Grouped Tabs – Thumb tabs: Reload default book groups

Button · Regular+ · `btn_resetTabGroups`  
Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> Clicking this button will replace the Grouped Tabs list with the default groups.

The default groups include `RUT 1SA`, the Minor Prophets in two groups, and the short letters. Any groups you typed are lost.

##### \toc3

Radio · Regular+ · `r_thumbText_toc3` · cfg `thumbtabs/thumbtextmkr=toc3`  
Also: Thumb tabs: Use \toc3 text · Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> By default, Thumb Tabs use the content and styling of the \toc3 marker.
>
> Note that this setting is interconnected with the Table of Contents settings on the Peripherals tab. If \toc3 is not included in the ToC, then this option will be disabled. So it is recommended to use \toc3 as your thumbtab text and include it in the Table of Contents.

The usual choice.

##### \zthumbtab

Radio · Regular+ · `r_thumbText_zthumbtab` · cfg `thumbtabs/thumbtextmkr=zthumbtab`  
Also: Thumb tabs: Use \zthumbtab text · Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> By default, Thumb Tabs use the content and styling of the \toc3 marker. If you prefer different content and/or styling for the tabs, then this  
> \zthumbtab option needs to be enabled, and the thumbtab names entered into your USFM text.
>
> Note that this setting is interconnected with the Table of Contents settings on the Peripherals tab. If \toc3 is not included in the ToC, then you are forced to use the \zthumbtab setting here. For that reason it is highly recommended to use \toc3 as your thumbtab text and include it in the Table of Contents.
>
> The USFM extension \zthumbtab can be used to set an alternative value for the thumbtab contents. If a book's header contains a \zthumbtab entry, then  
> \toc3 will not be used as the thumbtab contents. An empty \zthumbtab entry specifies that there should be no text in the thumbtab for that book.

Use it if the tab text should differ from `\toc3`. Add the `\zthumbtab` line to each book's header in Paratext. With this option, **Edit Style** opens the `\zthumbtab` style.

##### Edit Style

Link · Regular+ · `lb_style_toc3`  
Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> Click to jump to the appropriate (\toc3 or \zthumbtab) marker in the style editor to change the formatting of the thumb tabs.

Change the text colour, font and size there. Changing the `\toc3` style may also change how `\toc3` text looks elsewhere, such as in the table of contents.

##### Only Show on Odd Pages

Checkbox, off · Regular+ · `c_tabsOddOnly` · cfg `thumbtabs/tabsoddonly`  
Also: Thumb tabs: Only Show on Odd Pages · Needs: “Thumb Tabs” · Hidden until: “Thumb Tabs” · Shown when: “Thumb Tabs”, “Ornamental Decorations”

> When printing thumb tabs on thin paper, it is preferable to only print these tabs on a single side of the page (the odd pages).

Better on thin paper, where a tab printed on both sides can show through.

#### Ornamental Decorations

##### Section Headings

Checkbox, off · Regular+ · `c_inclSectionHeader` · cfg `fancy/sectionheader`  
Also: Enable decorative section headings · Needs: “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Section Headings may be adorned with a special graphic. Ensure that there is adequate space - both horizontal as well as vertical to make sure all headings fit.

Choose **PDF border (Legacy)** for a fixed graphic or **Dynamic Border** for a box that fits the heading.

##### Border

Checkbox, off · Regular+ · `c_inclPageBorder` · cfg `fancy/pageborders`  
Also: Enable decorative borders · Needs: “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> There are different kinds of borders that can be applied to the publication.
>
> Note that if you use a border, it is likely that you will need to adjust the margins to make it fit.

Choose one of the three kinds below it.

##### End of Book Decoration

Checkbox, off · Regular+ · `c_inclEndOfBook` · cfg `fancy/endofbook`  
Also: Enable end of book decoration · Needs: “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> The end of each book may be adorned with a special graphic.

Front matter, glossaries and other non-Scripture books do not get it.

##### Verse Number Decorator

Checkbox, off · Regular+ · `c_inclVerseDecorator` · cfg `fancy/versedecorator`  
Also: Enable decorative verse numbers · Needs: “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Verse numbers can be decorated using either of the options shown below.

**End of Ayah** uses a character from the font; **Verse Border Graphic** uses a small PDF graphic.

##### Book Title Borders

Checkbox, off · Regular+ · `c_inclTitleBorders` · cfg `fancy/booktitleborder`  
Also: Enable dynamic title borders · Needs: “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Dynamic borders can be applied to book titles (\mt1 and \mt2). Styling can be adjusted using the link below.

PTXprint makes the `cat:titlebox|esb` style active for you. Use the link below to change its look.

##### Section Headings

###### Select...

Button · Regular+ · `btn_selectSectionHeaderPDF` · cfg `fancy/sectionheaderpdf`  
Also: Select decorative section headings · Needs: “PDF border (Legacy)”, “Section Headings”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

Chooses the section heading PDF graphic. The file name appears next to the button.

###### Shift – Decorative section headings: Vertical shift

Number · Regular+ · `s_inclSectionShift` · cfg `fancy/sectionheadershift`  
Values: -50–50 · Needs: “PDF border (Legacy)”, “Section Headings”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Vertical shift in pts of the section box image.  
>   + values shift the box upwards  
>   - values shift the box downwards

Same direction as **Shift** for the verse graphic. Change it in small steps (for example 2 pt) and print to check.

In older versions of PTXprint this worked the other way round. When you open a configuration saved by an older version, PTXprint changes the sign for you, so the graphic stays in place. A configuration saved by this version and opened in an older PTXprint moves the graphic the other way.

###### Scale – Decorative section headings: Scale

Number · Regular+ · `s_inclSectionScale` · cfg `fancy/sectionheaderscale`  
Needs: “PDF border (Legacy)”, “Section Headings”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Scale section header image. 1.0 = its own size,  
> 0.5 = half size, 2.0 = double size.

0.8 = 80%, 1.2 = 120%.

###### PDF border (Legacy)

Radio · Regular+ · `r_sectHead_legacy` · cfg `fancy/sectionborder=legacy`, `fancy/sectionbordertype=legacy`  
Needs: “Section Headings”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Place a PDF graphic behind each section heading (\s, \s1, \s2). Use Select... to choose it, and Scale/Shift to fit it.

It does not grow with the heading, so it suits headings that are always one line.

###### Dynamic Border

Radio · Regular+ · `r_sectHead_dynamic` · cfg `fancy/sectionborder=dynamic`, `fancy/sectionbordertype=dynamic`  
Needs: “Section Headings”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Draw a box around each section heading that grows with the heading. Its look is set by the cat:headingsbox|esb style.

PTXprint makes the `cat:headingsbox|esb` style active for you. Use the link to change it.

###### \cat:headingsbox|esb

Link · Regular+ · `lb_style_cat:headingsbox|esb`  
Needs: “Dynamic Border”, “Section Headings”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> If Section Headings sometimes extend to more than one line, then a static PDF section heading is unlikely to work. Instead, a dynamically generated decorative section heading needs to be set up to grow/shrink with the content of the heading. Use this link to show the special style, which needs to be enabled and defined.

On the **Styles** tab set the background colour and, with **Borders...**, the border of the box around headings.

##### Border

###### Select...

Button · Regular+ · `btn_selectPageBorderPDF` · cfg `fancy/pageborderpdf`  
Also: Select decorative borders · Needs: “PDF border (Legacy)”, “Border”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

Chooses the page border PDF. It starts in PTXprint's border-art folder.

###### Full page

Checkbox, off · Regular+ · `c_borderPageWide` · cfg `fancy/pageborderfullpage`, `fancy/pagebordernfullpage_`  
Also: Decorative borders: Expand to fill page · Needs: “PDF border (Legacy)”, “Border”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> If set, the border is expanded to the full page. Otherwise it is expanded only to the gutter margins.

If unticked, the graphic is stretched to the page size without the binding gutter.

###### \textborder

Link · Regular+ · `lb_style_textborder`  
Needs: “Dynamic Border”, “Border”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Click to edit the properties of the Text Border (which is controlled by the \textborder style on the Styles tab).

Change the border there with **Borders...** in **Sidebar Settings**.

###### PDF border (Legacy)

Radio · Regular+ · `r_border_pdf` · cfg `fancy/pageborder`  
Needs: “Border”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Use an existing PDF Border for the entire publication.

Choose the graphic with **Select...**. It is stretched to the page without the binding gutter, or to the whole page if **Full page** is ticked.

###### Dynamic Border

Radio · Regular+ · `r_border_text` · cfg `fancy/pagebordertype=text`  
Needs: “Border”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Place a decorative border only around the Scripture text (excludes introductions, footnotes and other peripheral material).

Its look comes from the `textborder` style (**Styles** tab, **Other** category); PTXprint makes that style active for you. Change it with **Borders...** in **Sidebar Settings**.

###### Page Border

Radio · Regular+ · `r_border_page` · cfg `fancy/pagebordertype=page`  
Needs: “Border”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Place a uniform-sized decorative border on every page regardless of content.

If you do not get the result you want, use **Dynamic Border** or **PDF border (Legacy)**.

###### \pageborder

Link · Regular+ · `lb_style_pageborder`  
Needs: “Page Border”, “Border”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Click to edit the properties of the Page Border (which is controlled by the \pageborder style on the Styles tab).

Refers to the `\pageborder` style. (Clicking it does not open the style; see **Common problems**.)

##### End of Book Decoration

###### Select...

Button · Regular+ · `btn_selectEndOfBookPDF` · cfg `fancy/endofbookpdf`  
Also: Select end of book decoration · Needs: “End of Book Decoration”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

Chooses the end-of-book PDF. It is centred below the last line of each book.

##### Verse Number Decorator

###### End of Ayah

Radio · Regular+ · `r_decorator_ayah` · cfg `fancy/versedecoratortype=ayah`  
Also: Decorative verse numbers: Use end of Ayah · Needs: “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Use the End of Ayah character in the font to decorate the verse number.

The character is U+06DD. If the font lacks it you see empty boxes. **Move Ayah** puts the number at the end of the verse.

###### Verse Border Graphic

Radio · Regular+ · `r_decorator_file` · cfg `fancy/versedecoratortype=file`  
Also: Decorative verse numbers: Use verse border graphic · Needs: “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Use a PDF graphic to decorate the verse number. You may need to also adjust the font properties to ensure the verse numbers fit within the graphic.

Choose it with **Select...**; adjust with **Scale** and **Shift**.

###### \vp

Link · Regular+ · `lb_style_vp`  
Needs: “Move Ayah”, “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Click to edit the \vp marker's properties on the Styles tab.

`\vp` is used for the verse numbers when **Move Ayah** is ticked.

###### Select...

Button · Regular+ · `btn_selectVerseDecorator` · cfg `fancy/versedecoratorpdf`  
Also: Select verse border graphic · Needs: “Verse Border Graphic”, “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

Chooses the verse number PDF. PTXprint suggests its own star graphic.

###### Shift – Verse border graphic: Vertical shift

Number · Regular+ · `s_verseDecoratorShift` · cfg `fancy/versedecoratorshift`  
Values: -20–20 · Needs: “Verse Border Graphic”, “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Vertical shift in pts of the verse decorator image.  
>   + values shift the decorator upwards  
>   - values shift the decorator downwards

Use small steps, for example 0.5 pt.

###### Scale – Verse border graphic: Scale

Number · Regular+ · `s_verseDecoratorScale` · cfg `fancy/versedecoratorscale`  
Needs: “Verse Border Graphic”, “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Scale verse decorator image. 1.0 = its own size,  
> 0.5 = half size, 2.0 = double size.

Make it bigger if two- or three-digit verse numbers do not fit.

###### Move Ayah

Checkbox, off · Regular+ · `c_decorator_endayah` · cfg `fancy/endayah`  
Also: Decorative verse numbers: Move Ayah to end of verse · Needs: “End of Ayah”, “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> This option moves the Ayah to the end of the verse.

As is usual in Arabic-script layout. When ticked, the `\vp` link becomes available to style the moved numbers.

###### \v

Link · Regular+ · `lb_style_v`  
Needs: “Verse Number Decorator”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Click to edit the \v marker's properties on the Styles tab.

Change the font size, colour and position of the verse numbers there so they fit the decoration.

##### Book Title Borders

###### \cat:titlebox|esb

Link · Regular+ · `lb_style_cat:titlebox|esb`  
Needs: “Book Title Borders”, “Ornamental Decorations” · Hidden until: “Ornamental Decorations” · Shown when: “Ornamental Decorations”, “Thumb Tabs”

> Adjust the styling of the dynamic borders around book titles.

Change the background colour there, and use **Borders...** in **Sidebar Settings** for the border.


# 13. Styles tab

## 13.1 What this tab is for

Your Paratext text uses **markers** to say what each piece of text is. A marker is a short code that starts with a backslash. For example, `\p` starts a normal paragraph, `\s1` is a section heading, `\v` is a verse number, `\f` is a footnote and `\nd` is the name of God ("LORD"). These are called **USFM markers**.

A **style** is the set of formatting rules for one marker: font, size, bold or italic, colour, indents, alignment and the space above and below. The list of all styles is a **stylesheet**. The **Styles** tab is the style editor. Use it to change how one kind of text looks everywhere, for example "make all section headings bigger", "make verse numbers red", "put more space above the headings" or "do not print the `\rem` remarks".

The tab is only shown in the **Regular** and **Full** views (see the chapter about the main window). If the whole tab is greyed out, **Lock UI Layout Settings** on the **Advanced** tab is ticked; untick it to make changes.

Many other tabs have small blue links with a marker name (for example next to the verse number or heading settings). Click one to jump straight to that marker on the **Styles** tab. The tab label moves a little to show you where you are.

Changes show in the PDF only after you click **Print (Make PDF)** again. Style changes are saved with the current configuration.

## 13.2 The marker list

The left side lists all markers, grouped into categories such as **Chapters & Verses**, **Paragraphs**, **Poetry**, **Titles & Headings**, **Footnotes**, **Cross References**, **Character Styling** and **Peripheral Materials** (category names in bold blue). Click the small arrow beside a category to open it. Click a marker to show its settings on the right.

Each line shows the marker code and a short name, for example `s1 - Heading - Section Level 1`. A marker drawn with a line through it is not printed (see **Include Contents of Marker**).

To find a marker quickly, use the **Find** box or the filter button next to it (see the control notes). The filter makes the list much shorter.

Some markers have numbered levels, for example `\s1`, `\s2` or `\q1`, `\q2`. Selecting the plain marker (`s` or `q`) edits level 1 (`s1` or `q1`). Each level has its own style: a change to `\s1` does not change `\s2`.

Below the marker name and description are these buttons:

* **Add** – make a new style as a copy of the selected style.
* **Del** – delete a style that you added yourself.
* Reset (circular-arrows icon) – remove all your changes to the selected style. Greyed out for styles that you added yourself.
* **Edit** – change the name, description, type and end marker.
* **More Info...** – open the USFM documentation page for this marker on the internet. Only shown in the **Full** view, and only when **Disable ALL Internet Use** on the **Advanced** tab is not ticked.

## 13.3 Bold setting names: what has changed

PTXprint reads several stylesheets in order. Later ones override earlier ones:

1. The standard Paratext stylesheet (you cannot change it).
2. PTXprint's own additions (you cannot change them).
3. The project's `custom.sty`, if there is one. It can be edited from the **Advanced** tab. It also affects how Paratext shows the text.
4. Your changes on this **Styles** tab, saved with the configuration.
5. `ptxprint-mods.sty`, if there is one. It can be edited from the **Advanced** tab. Because it comes last, it wins over everything else.

A setting name in **bold** (for example **Font Size Factor**) means you changed this value on the **Styles** tab, so it differs from the stylesheets underneath. Click the bold name to go back to the original value of that one setting. Click Reset to remove all your changes to the style.

Hover over **Why are some parameters bold?** and **How are Stylesheets applied?** at the bottom of the tab for a short reminder.

## 13.4 Include Contents of Marker

Untick it to leave the text of this marker out of the PDF. The marker then has a line through it in the list, and its other settings are greyed out. The text stays in your Paratext project; only the PDF changes.

Some markers, such as `\rem` (remarks) or the identification lines, are not printed by default. Tick this box for them if you want them in the PDF.

The automatic boxes around headings and titles (`cat:headingsbox|esb`, `cat:titlebox|esb`) and the text border (`textborder`) also use this setting. Normally you turn these on from the **Tabs+Borders** tab, which ticks this box for you.

## 13.5 Character Settings

This area controls how the letters look.

* **Select Font...** – a different font for this marker only; otherwise the main font from the **Fonts+Script** tab is used. Beside it PTXprint shows the real size in points (pt – one point is about 0.35 mm) and any font changes such as Graphite, stretch, faux bold or slant.
* **Font Size Factor** – size compared with the **Base Font Size** on the **Layout** tab: 1.2 is 20% bigger, 0.8 is 20% smaller.
* **Scale Relative to Parent** – the size box becomes **Font Scale**, relative to the surrounding text instead of the base font size.
* **Bold**, **Italic**, **SmallCaps**, **Superscript** and **Underline**.
* **Raise** – moves the text up (or down, with a minus number) in points. Greyed out when **Superscript** is ticked, because superscript sets its own size and raise.
* **Color** – the text colour.

For `\p`, **Font Size Factor**, **Line Spacing Factor** and **Use Absolute Spacing** are greyed out. Set the main text size and line spacing on the **Layout** tab (**Base Font Size** and **Base Line Spacing**).

For a character marker (one that styles a few words inside a paragraph, like `\nd` or `\wj`), PTXprint opens only **Character Settings**. For paragraph markers it also opens **Paragraph Settings**. Click an area's title to open or close it yourself.

## 13.6 Paragraph Settings

This area controls the shape of the paragraph.

* **Alignment** – **Justified** (both edges straight), **Left**, **LeftBal**, **Center**, **Right**, **Inner** or **Outer**. **LeftBal** is left-aligned, but PTXprint also tries to make the lines, including the last line, more even in length. **Inner** and **Outer** are mainly for margin notes, cross-references in the margin and headings. For right-to-left scripts, Left and Right are swapped.
* **First Line Indent Factor**, **Left Indent Factor**, **Right Indent Factor** – multiples of the **Base Indent** on the **Layout** tab. A negative first line indent makes a "hanging" indent: the first line starts further left than the others. Poetry and list markers often use this.
* **Line Spacing Factor** – compared with the base line spacing. **Use Absolute Spacing (in pts)** gives an exact number of points instead; the label changes to **Baseline** and PTXprint converts the number.
* **Space Before Factor**, **Space After Factor** – extra space above and below, as a multiple of the base line spacing. 1.0 is about one empty line, 0.5 about half a line.
* **Maximum Ragged Space** – for non-justified paragraphs, how much of the line may stay empty at the ragged edge.

## 13.7 Other Settings

Settings used only by some markers. PTXprint opens the part that fits the selected marker.

* **Note Settings** (footnotes `\f`, cross-references `\x` and similar): style and raise of the caller (the small letter or symbol in the text and at the start of the note), and **Note Blend Into**, which puts these notes together with another kind of note.
* **Table Settings** (table cells `\tc`): where text sits from top to bottom when the cells in a row have different heights.
* **Sidebar Settings** (sidebar categories and the text border): see the next section.

## 13.8 Sidebars

A **sidebar** is a box of extra text, separate from the Scripture text, for example a study note about a place or a person. In USFM it starts with `\esb`, then a category such as `\cat people\cat*`, and ends with `\esbe`. All sidebars with the same category share one style; for "people" the marker name is `cat:people|esb`. PTXprint also uses sidebar styles itself, for example for the parts of the cover, the automatic boxes around headings and titles, and `cat:box|esb` for simple boxes.

Selecting a sidebar style opens **Sidebar Settings**:

* **Color** and **Alpha** – background colour of the box and how solid it is.
* **Width** – width of the box compared with the column or page.
* **Borders...** – the **Border Settings** dialog (see the **Tabs+Borders** chapter).
* **Foreground Image...** – a small picture (a logo) in each box of this category. See **Sidebar Image Settings** below.
* **Background Image...** – a picture behind the text of the box, like a watermark.
* **Size and Position...** – where the box goes on the page, shown as a short code beside the button.

The text inside a sidebar can have its own styles. For example, paragraphs inside "people" sidebars use `cat:people|p`. If such a style exists, change it like any other style; if not, you can add it (see **Common tasks**).

## 13.9 Size and Position Settings (dialog)

Opens from **Size and Position...** in **Sidebar Settings**. (The same dialog is used for maps on the **Pictures** tab.) A small picture shows roughly where the box will go.

1. Choose the **Frame Size** first: **Column Width**, **Span Width** (across all columns), **Page (in Margins)** or **Page (to Edge)**.
2. Then the **Vertical Position**. The choices depend on the frame size:
   * Column width: **Top**, **Bottom**, **Before Verse**, **After Paragraph** or **Cutout**.
   * Span width: **Top**, **Bottom** or **Below Notes**.
   * Page sizes: **Top**, **Center**, **Fill** or **Bottom**.
3. Then the **Horizontal Position**. **Center** is only offered for page sizes and for **Before Verse** and **After Paragraph**. For **Span Width** this list is greyed out.
4. For **After Paragraph** and **Cutout** you can set **Number of Lines** (for After Paragraph it becomes "Number of paragraphs").

Click **OK** to save.

A **cutout** is a notch in the text: the text flows around the box at the side of the column.

## 13.10 Sidebar Image Settings (dialog)

Opens from **Foreground Image...** or **Background Image...**; the title shows which.

* **Select...** chooses the image. PDF line art works best over a coloured background, because .jpg images cannot be transparent.
* **Scale** is the size compared with the box. **Maintain Aspect Ratio** keeps the picture's shape (height follows width).
* For a foreground image, choose **Above or Below Text**, **Beside Text** or **Cutout Within Text**, then the exact place in the list beside it.
* For a background image, **Background Image Advanced Settings** set transparency, layer order, what happens if it is too big, and which part of the box it fills.
* To take the image away, click **Remove Image**, then **OK**.

## 13.11 Add/Edit Style (dialog)

Opens from **Add** or **Edit**. It describes a marker: code, name, description, type and end marker. The formatting itself is then set on the **Styles** tab as usual. Creating markers is an advanced task. Most users only need it for special markers their project already uses (for example markers starting with `z`), or for cases such as a sidebar category.

* **Add**: the new style is a copy of the selected style, with all its settings, also ones not shown on the **Styles** tab, such as the border and padding of a sidebar (box) style. Only marker, name, description, type and end marker come from the dialog. So select a similar marker first.
* **Edit**: the **Marker** box is greyed out (a marker cannot be renamed). For standard USFM markers **Type** is also greyed out.
* **Name** controls where the marker appears in the list, for example `zpeople - Paragraph - Paragraph about people` goes into **Paragraphs**.

## 13.12 Common tasks

### Find the style for some text

1. If you do not know the marker, look at the text in Paratext with the "Unformatted" view, or on the **View+Edit** tab, to see which marker is in front of it.
2. On the **Styles** tab, type the marker code (for example `s1`) or a word (for example `heading`) in **Find**.
3. Or click the filter button to see only the markers used in your books.

### Make section headings bigger and bold

1. Type `s1` in **Find**.
2. In **Character Settings**, change **Font Size Factor**, for example from 1.0 to 1.2.
3. Tick **Bold**.
4. Click **Print (Make PDF)**.

### Put more space above and below headings

1. Select the heading marker (for example `s1`).
2. In **Paragraph Settings**, increase **Space Before Factor** (for example to 1.0) and **Space After Factor** (for example to 0.5).
3. Print again and check.

### Change the colour of verse numbers

1. Select the marker `v` (in **Chapters & Verses**).
2. Click the colour button next to **Color** and choose a colour.
3. PTXprint ticks **Enable Colored Text** on the **Fonts+Script** tab for you. Keep it ticked, or the colour will not print.

### Use a different font for one kind of text

1. Select the marker, for example `nd` (name of God).
2. Click **Select Font...** and choose the font and face.
3. To go back to the main font, click the bold **Font** label.

### Center a paragraph or change its indent

1. Select the marker (for example `pc`, or `q1` for poetry).
2. In **Paragraph Settings**, choose an **Alignment**, for example **Center**.
3. Change **First Line Indent Factor** or **Left Indent Factor** if needed.

### Leave some text out of the PDF

1. Select the marker, for example `rem` or a study-note marker.
2. Untick **Include Contents of Marker**. The marker now has a line through it.
3. Print again.

### Undo changes to a style

* One setting: click its bold name.
* All changes: click Reset. (For a style that you added yourself, Reset is greyed out. Change the settings back by hand, or delete the style with **Del**.)

### Give a sidebar category a coloured background

1. Find the style for the category, for example type `esb` in **Find**. If your category (for example "people") has no style yet, select `cat:box|esb`, click **Add**, type `cat:people|esb` in **Marker**, give it a **Name** and click **OK**.
2. In **Other Settings › Sidebar Settings**, click **Color** and choose a light colour. Set **Alpha** (for example 0.5).
3. Click **Size and Position...** to choose where the box goes, and **Borders...** for a border.
4. Print again.

## 13.13 Common problems

**My change on the Styles tab has no effect.**
* You may have changed the wrong marker. Check which marker the text really uses (for example `\s2` instead of `\s1`, or `\q2` instead of `\q1`).
* A more specific style may win. For example, `cat:people|p` is used for paragraphs inside "people" sidebars instead of `p`.
* `ptxprint-mods.sty` (edited from the **Advanced** tab) is applied last and may set the same value.
* You did not print again.

**The Font Size Factor and Line Spacing boxes are greyed out.**
You have selected `\p`. Change **Base Font Size** and **Base Line Spacing** on the **Layout** tab.

**The whole Styles tab is greyed out.**
Untick **Lock UI Layout Settings** on the **Advanced** tab.

**I cannot see the Styles tab.**
It is hidden in the **Mini** and **Basic** views. Change to **Regular** or **Full**.

**I set a colour, but the text is still black.**
Tick **Enable Colored Text** on the **Fonts+Script** tab.

**I chose Justified, but the text is not justified.**
**Justify Paragraphs** on the **Body** tab is not ticked, so **Justified** is treated as **Left**.

**Some text is in the wrong font.**
The style for that marker has its own font (its **Font** label is bold). Click the bold label to go back to the main font. If the font has no bold or italic face, PTXprint may make a faux (computer-made) bold or slant; this is shown next to the font size.

**Some text is missing from the PDF.**
**Include Contents of Marker** may be unticked for that marker (it has a line through it). Tick it.

**The Raise box is greyed out.**
**Superscript** is ticked. Superscript sets its own raise.

**The Del button does nothing.**
Only styles you added yourself can be deleted. Use Reset to remove your changes to a standard style.

**The More Info... link is missing or greyed out.**
It is only shown in the **Full** view, and only when internet use is allowed on the **Advanced** tab. Combined or custom markers have no documentation page, so the link is greyed out.

## 13.14 Settings reference

### Size and Position Settings (dialog)

#### OK

Button · Mini+ · `button1`

Saves the size and position and closes the dialog.

#### Cancel

Button · Mini+ · `button2`

Closes the dialog without changing the position.

#### Frame Size – Sidebar: Frame size

Drop-down · Regular+ · `fcb_sbSize`  
Choices: Column Width | Span Width | Page (in Margins) | Page (to Edge)

> The frame size determines the boundaries of where the sidebar will appear on the page.
>
> Span Width only allows a Top or Bottom vertical placement.
>
> Column Width allows several other more precise placement options: Before Verse, After Paragraph, or Cutout; and these can have Left/Inner or Right/Outer Horizontal positioning set.
>
> Page (in Margins) is intended for sidebars that will cover an entire page (i.e. preventing any scripture text from being on that page), but will still show the header.
>
> Page (to Edge) is intended for sidebars to fill the entire page, with no margins at all.
>
> When using single column layout, there is no difference between Column Width and Span Width.
>
> The frame size determines how large the sidebar will appear on the page.
>
> Span Width only allows a Top or Bottom vertical placement. Column Width allows several other more precise placement options: Before Verse, After Paragraph, or Cutout; and these can have Left/Inner or Right/Outer Horizontal positioning set.
>
> When using single column layout, there is no difference between Column Width and Span Width.

Choose this first; it changes the choices in the other lists. **Span Width** can also be **Below Notes**. The page sizes are for boxes that take a whole page, for example on covers.

#### Vertical Position – Sidebar: Vertical position

Drop-down · Regular+ · `fcb_sbPgPos`  
Choices: Top | Bottom | Below Notes | Before Verse | After Paragraph | Cutout | Fill

> Top: Above everything except the header line Bottom: Below all verse text (and footnotes in diglot) Before Verse: 'Here' where defined or before its Anchor Ref After Paragraph: After this paragraph Cutout: A notch/corner cut out of the text, starting at current line Below Notes: Below the footnotes (Span Width only) Fill: Stretch to fill the page (page sizes only)
>
> The above options may have other positioning parameters such as: Left, Right, Center, no. of lines (up or down).
>
> Top: Above everything except the header line Bottom: Below all verse text (and footnotes in diglot) Before Verse: 'Here' where defined or before its Anchor Ref After Paragraph: After this paragraph Cutout: A notch/corner cut out of the text, starting at current line
>
> The above options may have other positioning parameters such as: Left, Right, Center, no. of lines (up or down).

**After Paragraph** can go later with **Number of Lines**. **Cutout** makes the text flow around the box.

#### Horizontal Position – Sidebar: Horizontal position

Drop-down · Regular+ · `fcb_sbHoriz`  
Choices: Left | Center | Right | Inner | Outer | -

> The options available here change based on the Frame Size and Vertical Position settings. So if you can't find an option you are looking for, then check those settings first.

Inner = spine side, Outer = edge side. Greyed out for **Span Width**.

#### Number of Lines – Sidebar/map: Lines to adjust vertically

Number · Regular+ · `s_sbLines`  
Values: -24–24

> Some vertical position options allow a sidebar to be moved up or down by a number of lines or paragraphs.
>
> -Negative (minus) values specify to move UP. +Positive (plus) values specify to move DOWN.
>
> Negative counts for cutouts raise the sidebar, but the cutout will not affect earlier paragraphs. Note that negative and fractional paragraph counts are invalid.

For **After Paragraph** it counts paragraphs (whole numbers only); for **Cutout** it counts lines. Greyed out for other positions.

### Sidebar Image Settings (dialog)

#### Remove Image

Button · Regular+ · `btn_removeSBimage`  
Also: Sidebar FG/BG: Remove image

Then click **OK** to remove the image from this sidebar style.

#### OK

Button · Regular+ · `btn_image_ok`

Saves the image settings. With no image file chosen, the image is removed.

#### Cancel

Button · Regular+ · `btn_image_cancel`

Closes the dialog without changing anything.

#### Sidebar Foreground/Background

##### Select...

Button · Regular+ · `btn_sbSelectFile`  
Also: Sidebar FG/BG: Select an image

> Choose the image file (JPG, PNG or PDF).

The file name is shown next to the button.

##### Scale – Sidebar FG/BG: Scale of image

Number · Regular+ · `s_sbi_scaleWidth`  
Values: 0.01–2 (default 1)

> Specify how much the image should be scaled horizontally.

Relative to the box width. With **Maintain Aspect Ratio** it is also used for the height.

##### Scale – Sidebar FG/BG: Height of image

Number · Regular+ · `s_sbi_scaleHeight`  
Values: 0.01–2 (default 1) · Greyed out by: “Maintain Aspect Ratio”

> Specify how much the image should be scaled vertically.

Relative to the box height. Setting width and height separately can stretch the picture.

##### Maintain Aspect Ratio

Checkbox, on · Regular+ · `c_sbi_lockRatio`  
Also: Sidebar FG/BG: Maintain aspect ratio

> Scale the width and height the same so that the image maintains its proportions.

Untick it only to set the height separately.

##### Foreground Image Position Within Sidebar

###### Sidebar foreground image: Beside text options

Drop-down · Regular+ · `fcb_sbi_posn_beside`  
Choices: Left | Inner | Right | Outer | Left Top | Inner Top | Right Top | Outer Top | Left Centre | Inner Centre | Right Centre | Outer Centre | Left Bottom | Inner Bottom | Right Bottom | Outer Bottom · Needs: “Beside Text”

> Which side of the sidebar text the foreground image goes on (Left, Inner, Right or Outer), and whether it sits at the top, centre or bottom of that side.

Used with **Beside Text**.

###### Above or Below Text

Radio · Regular+ · `r_sbiPosn_above`  
Also: Sidebar foreground image: Above or below text

The image gets its own strip. Choose the exact place in the list beside it.

###### Beside Text

Radio · Regular+ · `r_sbiPosn_beside`  
Also: Sidebar foreground image: Beside text

The image gets its own column; the text is narrower for the full height of the box.

###### Cutout Within Text

Radio · Regular+ · `r_sbiPosn_cutout`  
Also: Sidebar foreground image: Cutout within sidebar

The text flows around the image. This leaves the least empty space.

###### Sidebar foreground image: Above or below options

Drop-down · Regular+ · `fcb_sbi_posn_above`  
Choices: Top | Top-Left | Top-Inner | Top-Centre | Top-Right | Top-Outer | Bottom | Bottom-Left | Bottom-Inner | Bottom-Centre | Bottom-Right | Bottom-Outer · Needs: “Above or Below Text”

> Where the foreground image goes when it is placed in its own strip above or below the sidebar text: Top or Bottom, and Left, Inner, Centre, Right or Outer.

Used with **Above or Below Text**.

###### Sidebar foreground image: Cutout position options

Drop-down · Regular+ · `fcb_sbi_posn_cutout`  
Choices: Left | Inner | Right | Outer · Needs: “Cutout Within Text”

> Which side of the sidebar text the cutout for the foreground image is on.

Used with **Cutout Within Text**.

###### Start N Lines Below Top – Sidebar foreground image: Adjust cutout position

Number · Regular+ · `s_sbiCutoutLines`  
Needs: “Cutout Within Text”

> The number of lines below the top of the sidebar text where the cutout for the foreground image starts.

Keeps the image away from the first lines, for example below a heading inside the box.

##### Background Image Advanced Settings

###### Background Image Transparency – Sidebar background image: Transparency (alpha)

Number · Regular+ · `s_sbiAlpha`

> Transparency or alpha value of the background image: 0 is transparent, 1 is solid. This is useful for turning black lines into a paler shade.
>
> Note that this will allow the background colour to show through, even if the image is above the background layer, so on a green background black will become a darker shade of green, not grey.

About 0.3 makes a watermark that does not make the text hard to read.

###### Color – Sidebar background image: Color

Colour · Regular+ · `col_sbiBgColor`

> Some (rare) PDF line-art images do not set the colour of their lines, relying instead on the 'default' colour, which is normally black. This control sets the default colour to something other than black, and thus such images can be recoloured with this option. If (as most PDF images do) the image defines its own colour, this option will have no visible effect at all. It is also possible that an image will *partly* contain colour information, but only starting part way through the file, a situation that might produce unexpected results.

Works only for a few simple PDF line-art images; most images have their own colours, and then this has no effect.

###### Background Image Transparency

Label · Regular+

> Transparency or alpha value of the background image: 0 is transparent, 1 is solid. This is useful for turning black lines into a paler shade.
>
> Note that this will allow the background colour to show through, even if the image is above the background layer, so on a green background black will become a darker shade of green, not grey.

###### Layer Order – Sidebar background image: Order of layers

Drop-down · Regular+ · `fcb_sbiLayerOrder`  
Choices: In Front of Background | Behind Background

> Only relevant where there is both a background image  
> *and* a background color. Set whether the background image should come above or behind the color. Line art PDFs with a transparent background may display better above the color layer, as the color layer will not then wash them out, but .JPGs are probably better behind, as .JPG images do not have transparency.
>
> Only relevant where there is both a background image  
> *and* a background color. Set whether the background image should come above or behind the color. Line art PDFs with a tranpsarent background may display better above the color layer, as the color layer will not then wash them out, but .JPGs are probably better behind, as .JPG images do not have transparency.

In front: good for PDF line art. Behind: better for .jpg photos.

###### If Image Is Oversized – Sidebar background image: Oversize management

Drop-down · Regular+ · `fcb_sbiOversize`  
Choices: Ignore (overflows frame) | Shrink (maintains ratio) | Squash (distorts ratio) | Crop (unimplemented)

> Select what action should be taken if the background image size is specified with a single dimension (height or width) and the unspecified dimension ends up being too large for a given sidebar.

**Ignore** lets the image stick out of the box. **Shrink** keeps its shape. **Squash** may change its shape. **Crop** is not working yet.

###### Crop Offset – Sidebar background image: Crop offset (XxY)

Text box · Regular+ · `t_sbiBgCropOfs`

> (Not available yet: cropping is still to be implemented.)
>
> Crop offset in the format XxY (e.g. 10x20). Only used when Oversize is set to Crop. Shifts the cropped region by X points horizontally and Y points vertically.

Crop is not working yet. Leave it empty.

###### Scale To – Sidebar background image: Scale Image to Inner/Outer/Bleed area

Drop-down · Regular+ · `fcb_sbiScaleTo`  
Choices: bleed: overflow the page into the cropped area | colbleed: overflow the page into the cropped area as much as the colours do (normally images bleed less) | inner: the area that text could cover (vertically this extends to the inner edge of the border) | outer: the outermost of the coloured box or the border | border: the outer edge of the border | box: the coloured box

> Select where the image should extend to.

**inner** = text area, **box** = coloured box, **border** = border, **outer** = outermost of these, **bleed**/**colbleed** = past the page edge (mainly for covers).

### Add/Edit Style (dialog)

#### OK

Button · Regular+ · `btn_sty_ok`

A new style is added to the list and selected, ready for formatting.

#### Cancel

Button · Regular+ · `btn_sty_cancel`

Closes the dialog without adding or changing a style.

#### Description

Label · Mini+

> You can say what you like here to describe the purpose of the style.

#### ⚠️Marker – Add/Edit marker dialog: Marker (code)

Text box · Regular+ · `t_styMarker`

> The marker code without the backslash, e.g. zpeople. It can only be set when adding a new style.

For example `zpeople` or `cat:people|esb`. If empty when you click **OK**, nothing is created.

#### Add/Edit marker dialog: Marker description

Text area · Regular+ · `textv_styDesc`

> You can say what you like here to describe the purpose of the style.

For your information only.

#### Name

Label · Mini+

> Consists of: Marker..Endmarker - Group - short description and helps to place the marker in the tree listing all markers.

#### Name – Add/Edit marker dialog: Marker name (short description)

Text box · Regular+ · `t_styName`

> Consists of: Marker..Endmarker - Group - short description and helps to place the marker in the tree listing all markers.

Form: `marker - Category - short description`. The middle part (for example `Paragraph`, `Character`, `Heading`) decides the category in the list. PTXprint updates the start of the name when you type a marker code.

#### End Marker – Add/Edit marker dialog: End Marker (code)

Text box · Regular+ · `t_styEndMarker`

> If the closing marker for this marker is not the same as the marker followed by a * then enter it here. For example, with paired milestones, do not create a new milestone just specify the closing milestone marker here.

Usually leave it empty: for character and note markers PTXprint adds the marker followed by `*`. For a pair of milestone markers, type the closing milestone here.

#### ⚠️Type – Add/Edit marker dialog: Marker type

Drop-down · Regular+ · `fcb_styType`  
Choices: Header | Title | Introduction | Introduction Character | Section Paragraph | Verse Paragraph | Character | List | List Character | Milestone | Standalone Milestone | Other Paragraph | Cross Reference | Cross Reference Character | Footnote | Footnote Character | Cell | Attribute | Identification | Internal

> [Required] This tells PTXprint what kind of marker this is.
>
> [Required] This tells PTXprint what kind of a marker this is.

For example **Verse Paragraph** for body text, **Section Paragraph** for a heading, **Character** for words inside a paragraph, or **Footnote**. Cannot be changed for standard USFM markers.

#### [Required] This tells PTXprint how to layout data in this ma...

Text box · Regular+

> [Required] This tells PTXprint how to layout data in this marker. For normal, vernacular body text, use VerseText. If this is part of a heading, use Section. If it is part of the title block of a book, use Title. NoteText makes this a kind of footnote, like \x.

### Styles

#### Find – Find style

Search box · Regular+ · `t_styleSearch`  
Greyed out by: “Lock UI Layout Settings”

> If you are not sure which category your marker can be found under, then use this Search tool to find the marker you need.

Type a marker code (backslash optional, for example `s1` or `\s1`) or part of a name (for example `heading`). After half a second PTXprint selects the first match, opens the categories with matches and colours every matching line pale peach. Clear the box to remove the colouring.

#### Enable (or disable) the filter to only show markers that are...

Toggle, off · Regular+ · `btn_styleFilter`  
Greyed out by: “Lock UI Layout Settings”

> Enable (or disable) the filter to only show markers that are in use in the current set of books.

The bulleted-list icon next to **Find**. When pressed in, the list shows only markers used in the books chosen for printing, with all categories open. Press again to see all markers. If your text has a USFM error, PTXprint shows an error message instead.

#### tv_Styles

Table · Regular+ · `tv_Styles`  
Greyed out by: “Lock UI Layout Settings”

Category lines are bold blue. A line through a marker means it is not printed.

#### Include Contents of Marker

Checkbox, on · Regular+ · `c_styTextProperties`  
Also: Styles: Include marker contents in PDF · Greyed out by: “Lock UI Layout Settings”

> Uncheck this option to set the marker to "non-publishable" so the contents of this marker will not be included in the output.

Tick it to print markers hidden by default, such as `\rem`. For the heading box, title box and text border, the **Tabs+Borders** tab sets this for you.

#### Include Contents of Marker

##### More Info...

Link · not shown · `l_url_usfm`  
Greyed out by: “Lock UI Layout Settings”

Opens in your web browser. For some interface languages the page goes through an automatic translation, unless **Only Use English Links** is ticked on the **Advanced** tab. Shown only in the **Full** view when internet use is allowed. Greyed out for combined or custom markers.

##### Add

Button · Regular+ · `btn_styAdd`  
Greyed out by: “Lock UI Layout Settings”

> Find a style within the appropriate section which is similar to the new style you wish to create. Then click this Add button to create a new style based on the currently selected style.

The copy includes all settings (also border and padding of box styles). Then fill in the **Add/Edit Style** dialog. Advanced.

##### Del

Button · Regular+ · `btn_styDel`  
Greyed out by: “Lock UI Layout Settings”

> Click to delete this style (only styles you have added can be deleted). Warning: There is no confirmation or undo!

For standard styles nothing happens.

##### Click to remove all changes made to this style, returning it...

Button · Regular+ · `btn_styReset`  
Greyed out by: “Lock UI Layout Settings”

> Click to remove all changes made to this style, returning it to the values in the underlying stylesheets.

The circular-arrows button. To reset one setting, click its bold name instead. Reset keeps the name, description and end marker. Greyed out for styles you created, because they have no underlying values to go back to.

##### Edit

Button · Regular+ · `btn_styEdit`  
Greyed out by: “Lock UI Layout Settings”

> Click to Edit additional properties for this style.

Change name, description, type or end marker. The marker code cannot be changed.

##### Hover-help

Label · Regular+  
Greyed out by: “Lock UI Layout Settings”

> Hover over these help topics to gain a greater understanding about how the Styles editor works.

##### Why are some parameters bold?

Label · Regular+  
Greyed out by: “Lock UI Layout Settings”

> When a setting's name is in bold it indicates that the value is different from what is in the stylesheet.
>
> Note that you can click on a bold setting name of any parameter to RESET it to the stylesheet value.

##### How are Stylesheets applied?

Label · Regular+  
Greyed out by: “Lock UI Layout Settings”

> Stylesheets are applied in this order with later settings overriding earlier settings:
>
> usfm_sb.sty is the underlying Paratext stylesheet (uneditable).
>
> ptx2pdf.sty contains PTXprint application modifications to make things work better (uneditable).
>
> Optional: custom.sty contains style modifications that are project-wide and also affect display of text within Paratext itself (can be edited from the Advanced tab). Typically used to add project-specific markers.
>
> ptxprint.sty contains the config's settings as edited by this Styles editor.
>
> Optional: ptxprint-mods.sty can be edited from the Advanced tab. Because it comes last, it takes priority.

##### Character Settings

###### Select Font...

Button · Regular+ · `bl_font_styFontName`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

With no font chosen, the marker uses the main font from the **Fonts+Script** tab. When a font is set, the **Font** label is bold; click it to go back to the main font.

###### Font Size Factor – Styles: Font size factor

Number · Regular+ · `s_styFontSize`  
Values: 0.1–50 (default 1) · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> This is a factor or proportion of the base font size. So 1.0 is the same as the base font size from the Layout tab. (Not available for \p, which always uses the Base Font Size.)

0.8 is smaller, 1.5 bigger. The real size in points is shown under the font button. With **Scale Relative to Parent** ticked, this becomes **Font Scale**, relative to the surrounding text.

###### Scale Relative to Parent

Checkbox, off · Regular+ · `c_styFontScale`  
Also: Styles: Scale relative to parent · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Normally the Font Size is relative to the Base Font Size (Layout tab). Tick this to make it relative to the size of the surrounding text instead. Note that  
> \p has a FontSize of 12 in the underlying stylesheet.

Use it when the size should follow the surrounding text, for example a character style that is always 80% of its paragraph. The size box label changes to **Font Scale**.

###### Bold

Checkbox, off · Regular+ · `c_styFaceBold`  
Also: Styles: Bold · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

If the font has no real bold face, PTXprint may use a faux (computer-made) bold, depending on the **Fonts+Script** tab settings.

###### Italic

Checkbox, off · Regular+ · `c_styFaceItalic`  
Also: Styles: Italic · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

If the font has no real italic face, a computer-made slant may be used.

###### Superscript

Checkbox, off · Regular+ · `c_styFaceSuperscript`  
Also: Styles: Superscript · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> The superscript option overrides these settings:  
>    Font Size Factor is set to 0.75  
>    Raise is set to 0.85 times the x-height of the font (which  
>    defaults to 1/2 the ascent if not specified in the font).

Used for verse numbers or footnote callers.

###### SmallCaps

Checkbox, off · Regular+ · `c_stySmallCap`  
Also: Styles: Smallcaps · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

Prints lowercase letters as small capitals. Needs a font that supports them, and only has an effect in scripts with upper and lower case. Often used for `\nd` (LORD).

###### Raise – Styles: Raise

Number · Regular+ · `s_styRaise`  
Values: -50–50 · Needs: “Include Contents of Marker” · Greyed out by: “Superscript”, “Lock UI Layout Settings”

> How much to raise the text (in pts).

A negative number moves the text down. Use small values. Raised text cannot break across lines, so use it only for short text.

###### Color: x001122 – Styles: Color

Colour · Regular+ · `col_styColor`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Sets text color for text in this style.

The colour code is shown next to the label. Choosing a colour also ticks **Enable Colored Text** on the **Fonts+Script** tab; if that is later unticked, the colour does not print. Click the bold **Color** label to remove your colour.

###### Underline

Checkbox, off · Regular+ · `c_styFaceUnderline`  
Also: Styles: Underline · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Note that underlining in printed scripture text is actively discouraged.

Underlines the text of this marker.

###### 11.7pt (↑6.6 ↓2.2)

Label · Regular+ · `l_styActualFontSize`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Calculated absolute point size given the current Base Font Size (which is set on the Layout tab).
>
> The (↑Ascender ↓Descender) values from the base line for this font are provided for reference.

Worked out from **Font Size Factor** and **Base Font Size**. Information only.

###### GR stretch=95% bold=1.8 ital=0.15

Label · Regular+ · `l_styFontFeats`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> If any modifications to the typeface have been selected, then they will be displayed here.
>
> GR= Graphite has been enabled stretch= (or shrink) font horizontally bold= embolden value (faux bold) ital= slant value (faux italics)

Empty when there are no changes. Information only.

##### Paragraph Settings

###### Alignment – Styles: Paragraph alignment

Drop-down · Regular+ · `fcb_styJustification`  
Choices: Justified | Left | LeftBal | Center | Right | Inner | Outer · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> If text is justified but Justify Paragraphs is turned off on the Body tab then an alignment of Justified here is treated as Left, (and maybe swapped if Right-to-Left).
>
> When the Writing system text flow direction is Right-to-Left the interpretation of Left and Right is swapped. Top-to-Bottom flow is treated as Left-to-Right.
>
> Inner vs Outer (used for Marginal Notes, Xrefs or Headings)  
>   Inner = closer to the center:  
>     In a 2-column layout: closer to the space between columns.  
>     In a 1-column layout: closer to the spine of the page spread.  
>   Outer = further from the center:  
>     In a 2-column layout: closer to the outer edge of the page.  
>     In a 1-column layout: closer to the outer edge of the page spread.  
>   Note: Marginal notes cannot switch sides mid-paragraph  
>              if the page or column changes.

**LeftBal** is left-aligned with more even line lengths. **Inner** and **Outer** depend on which side of the page or column the text is on. Click the bold **Alignment** label to undo your change.

###### First Line Indent Factor

Number · Regular+ · `s_styFirstLineIndent`  
Values: -50–50 · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> This is multiplied by the Base Paragraph Indent value (specified on the Layout tab) to get the final indentation amount.

1 is a normal paragraph indent, 0 is none. A negative value gives a hanging indent, often used for poetry and lists. For sidebars it moves the whole box sideways.

###### Left Indent Factor – Styles: Left indent

Number · Regular+ · `s_styLeftMargin`  
Values: -100–100 · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> This is multiplied by the Base Paragraph Indent value (specified on the Layout tab) to get the final indentation amount.
>
> When the Writing system text flow direction is Right-to-Left the interpretation of Left and Right is swapped.

Indents the whole paragraph. Use it for poetry levels, quotations and lists.

###### Right Indent Factor – Styles: Right indent

Number · Regular+ · `s_styRightMargin`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> This is multiplied by the Base Paragraph Indent value (specified on the Layout tab) to get the final indentation amount.
>
> When the Writing system text flow direction is Right-to-Left the interpretation of Left and Right is swapped.

Indents the whole paragraph from the right (left for right-to-left text).

###### Line Spacing Factor – Styles: Line spacing

Number · Regular+ · `s_styLineSpacing`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> This is a proportion of the base line spacing. So 1.0 is the same as the base line spacing from the Layout tab. If Absolute Spacing is set, then this value is the line spacing in pts.

1.0 is the same as **Base Line Spacing**. With **Use Absolute Spacing** ticked, the label changes to **Baseline**. Greyed out for `\p`.

###### Use Absolute Spacing (in pts)

Checkbox, off · Regular+ · `c_styAbsoluteLineSpacing`  
Also: Styles: Use absolute line spacing · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> The Line Spacing is usually calculated as a factor of the Font Size. If you prefer to specify an exact/absolute line spacing (in points), then enable this option.

PTXprint converts the value when you tick or untick it, and keeps only the new kind, so you can switch back and forth safely. A fixed value does not change when you later change the base line spacing. Greyed out for `\p`.

###### Space Before Factor – Styles: Space before

Number · Regular+ · `s_stySpaceBefore`  
Values: -1–5 · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Amount of space to insert before the paragraph. The actual space is this factor multiplied by the base line spacing from the Layout tab.

1.0 is about one empty line. Headings often use 0.5 to 1.5.

###### Space After Factor – Styles: Space after

Number · Regular+ · `s_stySpaceAfter`  
Values: -1–5 · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Amount of space to insert after the paragraph. The actual space is this factor multiplied by the base line spacing from the Layout tab.

1.0 is about one empty line.

###### Maximum Ragged Space – Styles: Maximum ragged (fill) space

Number · Regular+ · `s_styNonJustifiedFill`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> How much of the column-width can be empty space at a non-justified edge? This affects mid-paragraph line-breaking and may cause stretching of other spacing if the line would be too short otherwise. It does not stop the final line of a paragraph from being shorter.
>
> This value is set as the proportion of the column width, with sensible values being with the range of 0.20 to 0.75 (where 1.00 represents the entire column width). Discretionary breaks (//) will be ignored if breaking there would leave more than this much space.

Default 0.25 (a quarter of the line). Larger values allow more uneven lines; smaller values make lines more even but may stretch word spaces.

##### Other Settings › Note Settings

###### Caller Raise – Note settings: Caller raise

Number · Regular+ · `s_styCallerRaise`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Raise the caller in the main text by this number of points.

Leave it at 0 unless the caller sits too high or too low.

###### Note Caller Raise – Note settings: Note caller raise

Number · Regular+ · `s_styNoteCallerRaise`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Raise the caller in the note by this number of points.

The caller at the start of the note itself.

###### Caller Style – Note settings: Caller style

Text box · Regular+ · `t_styCallerStyle`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> The style which is used to style the caller in the main text. If none is specified then  
> \v is used.

Type the marker code without the backslash. Advanced.

###### Note Caller Style – Note settings: Note caller style

Text box · Regular+ · `t_styNoteCallerStyle`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> The style which is used to style the caller in the note itself. If none is specified then  
> \v is used.

Type the marker code without the backslash. Advanced.

###### Note Blend Into Style – Note settings: Note blend into style

Text box · Regular+ · `t_NoteBlendInto`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Insert the notes of the marker being defined into the collection of notes in the marker specified here.
>
> For example, if when defining the \x style, if this value was set to f then all cross references would be blended into the \f footnotes.

The blended notes keep their own style. The **Notes+Refs** tab sets this for cross-references when you blend them with footnotes, so normally you type nothing here.

##### Other Settings › Table Settings

###### Table settings: Vertical position of \tc markers

Drop-down · Regular+ · `fcb_stytcVpos`  
Choices: Top | Center | Bottom | Gridded Center · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Where text sits vertically in a table cell that is shorter than the tallest cell in the row. Gridded Center keeps the text on whole lines.

**Gridded Center** keeps the text on whole lines so it lines up with the other cells.

##### Other Settings › Sidebar Settings

###### Color – Sidebar settings: Color

Colour · Regular+ · `col_sb_backColor`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Sets the background color for the sidebar.
>
> Background shading color.

Choose a light colour so the text stays easy to read. Click the bold **Color** label to remove your change.

###### Alpha – Sidebar settings: Alpha (transparency)

Number · Regular+ · `s_sbAlpha`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> The transparency or alpha value of the background colour:  
> 0 is transparent, 1 is solid.

A value below 1 lets a background image or page decoration show through.

###### Width – Sidebar settings: Width

Number · Regular+ · `s_sbWidth`  
Values: 0.25–2.5 (default 1) · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Sidebar width as a proportion of the column/page width (1.0 = full width,  
> 0.5 = half width).

Relative to the frame chosen in **Size and Position**. Narrow boxes are useful for cutouts.

###### Borders...

Button · Regular+ · `btn_sbBorders`  
Also: Sidebar settings: Borders · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Click for additional settings to control the look of borders for this category of sidebar.

Border lines, colours, padding and ornaments. See the **Tabs+Borders** chapter.

###### Foreground Image...

Button · Regular+ · `btn_sbFGIDia`  
Also: Sidebar settings: Foreground image settings · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Click for additional settings to use a foreground image for this category of sidebar.

A foreground image is shown in every box of this category, for example a scroll for history notes.

###### Background Image...

Button · Regular+ · `btn_sbBGIDia`  
Also: Sidebar settings: Background image settings · Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Click for additional settings to use a background image for this category of sidebar.

A background image sits behind the text of the box, like a watermark.

###### t_sbPgPos

Text box · Regular+ · `t_sbPgPos`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

Examples: `t` (top), `bl` (bottom left), `cr2` (cutout on the right, 2 lines down), `Pcf` (whole page, filled). Use the **Size and Position...** button rather than typing here.

###### Size and Position...

Button · Regular+ · `btn_sbSizePosition`  
Needs: “Include Contents of Marker” · Greyed out by: “Lock UI Layout Settings”

> Choose the frame size and position of this category of sidebar on the page.

The dialog has a preview picture.


# 14. Advanced tab

## 14.1 What this tab is for

The **Advanced** tab holds settings for experienced users. Most people never need it. Come here when another tab cannot give you the result you need, or when the support team asks you to change a specific setting.

The tab has two sub-tabs:

* **Main** – ways to change the text before it is typeset (a changes file, a processing script), extra stylesheets and TeX settings files, interlinear output, plugins, internet use, and locks that protect a finished layout.
* **Other** – about 125 "TeXpert" settings: fine controls for the typesetting engine, sorted into groups such as **Page Layout and Spacing** or **Footnotes, Cross-references, Study Notes**.

The tab is only shown in the **Regular** and **Full** views. Some **Main** settings are only shown in the **Full** view (noted below).

## 14.2 Before you change anything here

A small change here can move text on many pages. Follow these rules:

1. **Change one setting at a time.** Then print and look at the result. If you change several together, you cannot tell which one caused a change.
2. **Write down the original value** before you change it.
3. **Look for bold labels.** On the **Other** sub-tab, the label of a check box or number box turns **bold** when its value differs from the default. (Drop-down lists do not turn bold.)
4. **To go back to the default value:**
   * Number box: click its bold label.
   * Check box: click the check box again.
   * Drop-down list: choose the first item. The first item is always the default.
5. **Hover over a setting** to see its tooltip. The first line shows the internal name and the default value in square brackets. For a number box the first number in the brackets is the default; the others are the lowest value, highest value and step sizes.

PTXprint saves a TeXpert setting in the configuration only when it differs from the default.

To find a TeXpert setting quickly, type part of its name in the **Search for settings** box at the bottom of the main window (Ctrl+F).

## 14.3 Main sub-tab: Text Processing & Stylesheets

Here you change the text, or how it is styled, with files you edit yourself. Each option has a check box (to turn it on) and an **Edit...** button, which is only active when the box is ticked. **Edit...** opens the file on the **View+Edit** tab, where you can type in it and save it.

These features are for people who understand USFM, regular expressions (a way to describe text patterns) or TeX. Never change these files if you are not sure what you are doing. To turn a file off, untick its box; you do not need to delete the file.

* **Apply Modifications to USFM Text (changes.txt)** – search-and-replace rules applied to a temporary copy of the text before typesetting. Your Paratext project is never changed. `changes.txt` belongs to the current configuration only; `PrintDraftChanges.txt` (in the project folder) applies to all configurations of the project.
* **Apply Customized Settings (ptxprint-mods.tex)** – TeX settings applied after all PTXprint settings, for things PTXprint has no control for. A support person may give you a line to add here.
* **Apply Initial Settings (ptxprint-premods.tex)** – TeX settings applied before the stylesheets and other settings. Rarely needed. (**Full** view only.)
* **Apply Customized Styles (custom.sty)** – the project's own custom stylesheet, the same one Paratext uses. (**Full** view only.)
* **Apply Stylesheet Overrides (ptxprint-mods.sty)** – an extra stylesheet for this configuration that overrides other styles. Most style changes are easier on the **Styles** tab. (**Full** view only.)
* **Process Text With Custom Script at** – runs a program of your own on each book. (**Full** view only.)

PTXprint changes the text in this order:

1. A custom script, if **start** is chosen.
2. The rules in the changes files.
3. **Auto-Correct USFM** and other changes PTXprint makes for settings on other tabs.
4. A custom script, if **end** is chosen.

## 14.4 Main sub-tab: General

Settings that do not fit anywhere else:

* **Sensitive Project** – shortens picture credits and keeps private data out of the PDF.
* **Auto-Correct USFM** – fixes common USFM mistakes and warns about serious ones. Leave it ticked.
* **Interlinear** – prints Paratext interlinear glosses under (or above) each word. (**Full** view only.)
* **Auto-tag Hebrew and Greek words** – marks these words so they use the right font.
* **Only Use English Links** and **Disable ALL Internet Use** – how PTXprint uses the internet.
* **Plugins** – loads extra parts of the typesetting code for special features. (**Full** view only.)
* **Lock XeTeX Layout Level** and **Lock UI Layout Settings** – protect a finished layout from changes. (**Full** view only.)

## 14.5 Main sub-tab: Capture tests?

Only shown in the **Full** view. A developer tool that records what you click to make an automatic test. Normal users do not need it.

## 14.6 Other sub-tab: the TeXpert settings

Click a group name to open or close it. The filter button at the top shows only the groups that have changed settings; it is only active while the **Other** sub-tab is shown.

The sections below follow the groups on the screen.

### Page Layout and Spacing

Where books and introductions start, how two columns are balanced, line spacing, and notelines.

* **Where to start a new book**: next page, same page as the end of the previous book, or next odd (right-hand) page. **Page full factor** sets how full the page can be before the next book is moved to a new page anyway.
* **Where to start a new intro page** does the same for book introductions.
* **Unbalanced Lines (Max)** is only used when **Allow Unbalanced Columns** is ticked on the **Layout** tab.
* **Variable line spacing maximum stretch** and **shrink** are only used when **Fill Columns** is ticked on the **Layout** tab.
* The **Noteline** settings change the lines for hand-written notes, which you turn on (and colour) with **Notelines** on the **Layout** tab.
* **Maximum layout version** and **Legacy 1/14 LineSpacing** keep older projects looking the same after PTXprint is updated.
* **Maximum parallel processes** limits how many jobs run at the same time, for example when the page filler works.

### Chapter and Verse

Space after chapter and verse numbers, the size of large (drop) chapter numbers, hanging verse numbers in poetry, and marginal verse numbers (verse numbers in the margin, set on the **Body** tab).

### Body Text

Paragraph indents, line breaking and hyphenation, and clickable links.

Some of these are "penalties": a number that tells the typesetting engine how much to avoid something. Higher = avoid more strongly. 10000 means "never".

* **Hyphenation threshold**, **Penalty for inserting hyphen** and **Double hyphenation penalty** only matter when hyphenation is on (**Fonts+Script** tab).
* **Maximum orphan word length** is only used when **Prevent Orphan Words** is ticked on the **Body** tab.

### Fonts and Underline

How line heights are measured, whether system fonts can be used, and how underlines look.

### Footnotes, Cross-references, Study Notes

Where notes go on a page, when notes may be split across pages, fine spacing of paragraphed notes, and the gap to margin notes. Many of these interact. Change them only to solve a specific problem, and check several pages after each change.

### Diglot

Only used when you print two or more texts side by side (see the **Diglot** tab): notes, versification, shading, borders, and what happens when a page cannot be printed.

### Pictures, Figures, Images, Sidebars

Default picture position, order of caption and reference, space around pictures and sidebars, and the style of picture credits.

### PDF Options, Covers, Show/Hide

Bookmarks, links and transparency in the PDF, some cover sizes, and "show" options that put helpful marks on the pages while you proofread. Turn all "show" options off before you make the final PDF.

### Preview Pane: Adjustment and Analysis Settings

The PDF Preview window: the auto-update delay, how far the right-click menu can shrink or expand text, and how **Layout Analysis** finds bad spaces, collisions and rivers. A river is a line of white space running down through several lines of text. Changes here take effect in the preview straight away. You can also reach these settings from the PDF Preview window: click the delay text next to **Auto-update**, or the analysis settings link.

### Automatic Page Filler

The page filler tool in the PDF Preview window stretches or shrinks paragraphs a little so each page is filled. These settings balance speed against how good the text looks. **The cost of imbalance in a polyglot slice** is only used for diglot and polyglot projects. See the PDF Preview chapter for how to use the tool.

### Other Miscellaneous Settings

Thumb tab text, the tilde (~) character, unwanted reference links from DBL text, and the space above the end-of-book decoration.

## 14.7 Common tasks

### Apply a search-and-replace rule to the text (advanced)

1. On **Advanced** › **Main** › **Text Processing & Stylesheets**, tick **Apply Modifications to USFM Text (changes.txt)**.
2. Click **Edit...** next to it (or press Shift+Ctrl+C). `changes.txt` opens on the **View+Edit** tab.
3. Add one rule per line. A simple rule looks like `"old text" > "new text"`. The first quoted text is a regular expression, so some characters (such as `.` `(` `[` `\`) have a special meaning.
4. Save the file on the **View+Edit** tab.
5. Click **Print** and check the change in the PDF.

If PTXprint reports an error in the changes file, look at the last rule you added.

### Turn off a changes file or mods file without deleting it

1. Go to **Advanced** › **Main** › **Text Processing & Stylesheets**.
2. Untick the box for that file (for example **Apply Customized Settings (ptxprint-mods.tex)**).
3. Print again. The file stays on disk, so you can tick the box later to use it again.

### Print an interlinear text

1. In Paratext, make sure the interlinear glosses are approved.
2. Change to the **Full** view.
3. On **Advanced** › **Main** › **General**, tick **Interlinear**.
4. In the box next to it, type the gloss language code (for example `en`).
5. Tick **Ruby Text Above** if you want the glosses above the words.
6. Click **Print**.
7. To change the size or colour of the glosses, click the **\gloss|rb** link. For the base text, click **\rb**.

### Protect a finished layout

1. Change to the **Full** view.
2. On **Advanced** › **Main** › **General**, tick **Lock XeTeX Layout Level**. Future PTXprint updates will then use the same layout rules as now.
3. Tick **Lock UI Layout Settings**. The main layout, font and style controls are greyed out, so nobody changes them by accident.
4. Untick these boxes when you need to change the layout again.

### Find out which TeXpert settings have been changed

1. On the **Advanced** tab, click the **Other** sub-tab.
2. Click the filter button at the top. Only the groups with changed settings stay visible, and they open.
3. The bold labels are the changed settings.
4. Click the filter button again to show all groups.

### Put a TeXpert setting back to its default value

1. Find the setting on **Advanced** › **Other**. Its label is bold.
2. Number box: click the bold label. Check box: click the box. Drop-down list: choose the first item.
3. Check that the label is no longer bold, then print again.

### Start each book on a right-hand page

1. Go to **Advanced** › **Other** › **Page Layout and Spacing**.
2. Set **Where to start a new book** to **Odd page**.
3. Print. PTXprint adds blank pages where needed.

### Let books follow each other on the same page

1. Go to **Advanced** › **Other** › **Page Layout and Spacing**.
2. Set **Where to start a new book** to **Same page**.
3. If a book still starts on a new page when you do not want it to, increase **Page full factor** a little (for example from 0.65 to 0.75).

### Mark places that need attention while proofreading

1. Go to **Advanced** › **Other** › **PDF Options, Covers, Show/Hide**.
2. Tick **Show Error Bars For Overfull Lines** to see lines that are too long. Tick **Show USFM codes** to see which marker each paragraph uses.
3. Print and check the PDF.
4. Untick these options before you make the final PDF.

## 14.8 Common problems

**The Advanced tab is missing.** It is only shown in the **Regular** and **Full** views. Change the view level (see the chapter on the main window).

**Some settings on the Main sub-tab are missing** (for example **Interlinear**, **Plugins**, **Process Text With Custom Script at**, or the locks). These are only shown in the **Full** view.

**An Edit... button is greyed out.** Tick the check box for that file first.

**My changes in changes.txt have no effect.** Make sure **Apply Modifications to USFM Text (changes.txt)** is ticked, the file is saved on the **View+Edit** tab, and you printed again. Check that the search text really matches the USFM text, including spaces and markers. Look at the Log tab for messages about the changes file.

**Printing fails after I edited a mods file.** Untick the box for the file you edited (for example **Apply Customized Settings (ptxprint-mods.tex)**) and print again. If the problem goes away, the error is in that file. Undo your last change in it.

**Interlinear printing says some references "need to be reapproved".** The glosses for those verses are not approved in the Paratext Interlinearizer. Approve them in Paratext and print again.

**Between Letters spacing is greyed out on the Fonts+Script tab.** **Interlinear** is ticked on the **Advanced** tab. The two cannot be used together.

**Layout, font and style controls are greyed out.** Untick **Lock UI Layout Settings** on **Advanced** › **Main** › **General** (**Full** view).

**Help links and the update check are missing.** **Disable ALL Internet Use** is ticked. Untick it to let PTXprint use the internet again.

**My PDF suddenly looks different but I did not change anything on the main tabs.** Someone may have changed a TeXpert setting. Open **Advanced** › **Other** and click the filter button to see the changed settings (bold labels). Also check whether a changes file or mods file is ticked on the **Main** sub-tab.

**Unbalanced Lines (Max) or the variable line spacing settings have no effect.** They only work when **Allow Unbalanced Columns** or **Fill Columns** is ticked on the **Layout** tab.

**I changed Use system fonts but nothing happened.** Close and restart PTXprint.

**Coloured marks or labels appear in the margins of my PDF.** One of the "show" options in **PDF Options, Covers, Show/Hide** is ticked (**Show adjust points**, **Mark Trigger Points**, **Show USFM codes**, **Show Error Bars For Overfull Lines**), or **Show Diglot Trace Marks** in the **Diglot** group. Untick it.

## 14.9 Settings reference

### Advanced

#### Other

Label · Regular+ · `l_advOther`

> To balance columns of text on a page it is possible to specify paragraphs adjustments (shrink or expand):
>
> A Paragraph Adjust List needs to be in this format:  
> MRK 2.7 +1    (i.e. expand the para at Mark 2.7 by one line) MRK 3.20 -1   (i.e. shrink the para at Mark 3:20 by one line) %MARK 4.14 +1   (ignore this line - treat it as a comment) MRK 5.8 +2    (i.e. expand the para at Mark 5.8 by two lines) MRK 6.23 +1[2]  (expand the paragraph AFTER the paragraph  
>                               which contains MRK 6.23 e.g. a heading.) etc. Note that adjusting paragraphs needs to be done right at the end when all other settings have been finalized. Otherwise you are likely to have to re-do it all again.

The **Other** sub-tab label. The sub-tab holds the TeXpert settings in groups.

#### Filter: show only sections with non-default settings. Sectio...

Toggle, off · Regular+ · `btn_texpertFilter`

> Filter: show only sections with non-default settings. Sections where all values are default will be hidden. Sections with changed values will be expanded. Disable to restore all sections in collapsed state.

Inside the shown groups, only the changed settings are shown. The quickest way to see what has changed in a configuration. Only works while the **Other** sub-tab is shown.

#### Main

##### Text Processing & Stylesheets

###### Apply Customized Settings (ptxprint-mods.tex)

Checkbox, off · Regular+ · `c_useModsTex` · cfg `project/ifusemodstex`  
Also: Apply customized TeX settings

> This is the normal file for advanced users to configure TeX. This .tex file executes AFTER all the PTXprint settings.

Anything in this file wins over PTXprint's own settings. Use it only when a support person or expert gives you something to put in it. If printing suddenly fails, untick this box first to see whether the file is the cause.

###### Process Text With Custom Script at

Checkbox, off · Full · `c_processScript` · cfg `project/processscript`

> Processes the .usfm file through a program of your choosing. The program is run as `prog infile outfile` where infile is the source .usfm file and outfile the output .usfm that will then be typeset.

Use it for changes too complex for a changes file, such as converting the text to another writing system. Choose the program with **Select...** and when it runs with **start** or **end**. Experienced users only.

###### start

Radio · Full · `r_when2processScript_before` · cfg `project/when2processscript=before`  
Needs: “Process Text With Custom Script at”

> Execute processing script BEFORE running any printdraftchanges, canonicalisation (i.e. Auto-Correct USFM) or local changes which are all specified below.

The script works on the original USFM text. Choose this when your changes-file rules expect the text that the script produces.

###### end

Radio · Full · `r_when2processScript_after` · cfg `project/when2processscript=after`  
Needs: “Process Text With Custom Script at”

> Execute processing script AFTER running any printdraftchanges, canonicalisation (i.e. Auto-Correct USFM) or local changes which are all specified below.

The script then sees the text almost exactly as it will be typeset.

###### Select...

Button · Full · `btn_selectScript` · cfg `project/selectscript`  
Also: Select custom script · Needs: “Process Text With Custom Script at”

Accepts .bat, .exe, .py or .sh. Choosing a file ticks **Process Text With Custom Script at** for you; cancelling without a file turns the option off. Hover over the button to see the chosen file.

###### Apply Modifications to USFM Text (changes.txt)

Checkbox, off · Regular+ · `c_usePrintDraftChanges` · cfg `project/usechangesfile`  
Also: Enable changes.txt to be applied

> If there are changes that you wish to apply to the USFM file(s) prior to producing the printout, then these can be specified in these files:
>
> changes.txt - is used for changes that only apply to the current configuration;
>
> PrintDraftChanges.txt - specifies changes which apply to all configurations, and gets 'included' at the top of changes.txt

Use it to fix small problems in the text for printing only, such as spacing or punctuation. Your Paratext project is not changed. The rules are regular expressions, so test each new rule carefully.

###### Edit...

Button · Regular+ · `btn_editChangesFile`  
Also: Edit changes files · Needs: “Apply Modifications to USFM Text (changes.txt)”

> Switch to the View+Edit tab to show the Changes.txt file in one tab, and PrintDraftChanges.txt in the next tab to the right.
>
> Shortcut: Shift-Ctrl-C

`PrintDraftChanges.txt` opens in the next tab only if the project has one. Save there, then print again.

###### Edit...

Button · Regular+ · `btn_editModsTeX`  
Also: Edit customized TeX settings · Needs: “Apply Customized Settings (ptxprint-mods.tex)”

> Switch to the View+Edit tab to show the ptxprint-mods.tex file.
>
> Shortcut: Shift-Ctrl-T

Save the file there and print again.

###### Edit...

Button · Full · `btn_editModsSty`  
Also: Edit stylesheet overrides · Needs: “Apply Stylesheet Overrides (ptxprint-mods.sty)”

> Switch to the View+Edit tab to show the ptxprint-mods.sty file.
>
> Shortcut: Shift-Ctrl-S

Most style changes are easier and safer on the **Styles** tab.

###### Apply Stylesheet Overrides (ptxprint-mods.sty)

Checkbox, off · Full · `c_useModsSty` · cfg `project/ifusemodssty`

> It is recommended to leave this option unchecked (off) unless you have intentionally customized styles using the ptxprint-mods.sty stylesheet and wish for these to be used by PTXprint.

Most people make style changes on the **Styles** tab instead.

###### Apply Customized Styles (custom.sty)

Checkbox, off · Full · `c_useCustomSty` · cfg `project/ifusecustomsty`  
Also: Apply custom styles

> It is recommended to leave this option unchecked (off) unless you have intentionally customized styles using the custom.sty stylesheet and wish for these to be used by PTXprint.

The same file Paratext uses for its own display. If the file does not exist, nothing changes.

###### Edit...

Button · Full · `btn_editCustomSty`  
Also: Edit custom styles · Needs: “Apply Customized Styles (custom.sty)”

> Switch to the View+Edit tab to show the custom.sty file.
>
> Shortcut: Shift-Ctrl-M

The file is shared with Paratext, so a change here can also change how Paratext shows the text.

###### Edit...

Button · Full · `btn_editScript`  
Also: Edit custom script · Needs: “Process Text With Custom Script at”

> Edit the processing script

Lets you read or change the chosen script. Only active when a script has been selected.

###### Edit...

Button · Full · `btn_editModsPreTex`  
Also: Edit initial TeX settings · Needs: “Apply Initial Settings (ptxprint-premods.tex)”

> Switch to the View+Edit tab to show the ptxprint-premods.tex file.
>
> Shortcut: Shift-Ctrl-P

Opens `ptxprint-premods.tex` for editing.

###### Apply Initial Settings (ptxprint-premods.tex)

Checkbox, off · Full · `c_usePreModsTex` · cfg `project/ifusepremodstex`  
Also: Apply initial TeX settings

> This .tex file is executed BEFORE any stylesheets of other settings are applied. This file is rarely used.

Most changes belong in `ptxprint-mods.tex` instead.

##### General

###### Sensitive Project

Checkbox, off · Regular+ · `c_sensitive` · cfg `document/sensitive`

> In sensitive locations the illustration copyright statement(s) can just contain the appropriate acronyms (e.g. BFBS or DCC) for some artists.
>
> In addition, the PDF's metadata will not contain sensitive project-specific data.

Credits use short names (for example "DCC" instead of the artist's full name) where allowed. Tick it before you make any PDF that will be shared.

###### Auto-Correct USFM

Checkbox, on · Regular+ · `c_canonicalise` · cfg `project/canonicalise`  
Also: Auto-correct common USFM syntax errors

> PTXprint can analyze the USFM files and automatically correct some common errors in syntax. It will also notify you of errors which are likely to cause the print process to fail - giving you helpful feedback about how to fix the issue before re-trying to print.

Fixes are made in a temporary copy. Serious errors show a "USFM Check Error" message with the book and the problem. Untick it only if a support person asks, for example to see whether the check itself causes a problem.

###### Interlinear  &  Code

Checkbox, off · Full · `c_interlinear` · cfg `project/interlinear`  
Also: Interlinear settings

> Convert Paratext's interlinear data text to ruby (glossing) so that an interlinear text can be printed.
>
> Note that  you may need to adjust the following marker styles:  
>   \rb    for the base text  
>   \gloss|rb    for the gloss text
>
> Note that if this Interlinear option is enabled, then the Spacing Adjustments Between Letters (on the Fonts+Scripts page) will be disabled as these two settings are mutually exclusive.

Uses glosses from the Paratext Interlinearizer. You must also type the gloss language code in the box next to it. If some verses have unapproved glosses, PTXprint lists the references to approve in Paratext.

###### Interlinear language code to use. To find which code to use,...

Text box · Full · `t_interlinearLang` · cfg `project/interlang`

> Interlinear language code to use. To find which code to use, look in the project folder for a folder named "Interlinear_xy" where xy is the language code. For example if the interlinear has been glossed into English, then the code would be "en".

Interlinear output only works when this box has a code.

###### Ruby Text Above

Checkbox, off · Full · `c_ruby` · cfg `project/ruby`  
Also: Place Ruby text above words

> Treat ruby text as ruby rather than interlinear text by placing it above the base text rather than below.
>
> Note that  you may need to adjust the following marker styles:  
>   \rb    for the base text  
>   \gloss|rb    for the gloss text Use the shortcut links on the right to locate those styles in the editor.

Like ruby text in East Asian scripts. Only has an effect when **Interlinear** is ticked.

###### \rb

Link · Full · `lb_style_rb`

> Click to jump to the \rb marker in the style editor to change the formatting of the ruby text.

The base text is the words that carry glosses.

###### \gloss|rb

Link · Full · `lb_style_gloss|rb`

> Click to jump to the \gloss|rb marker in the style editor to change the formatting of the glosses for interlinear/ruby text.

Change size, colour or spacing of the glosses there. Glosses are usually smaller than the base text.

###### Only Use English Links

Checkbox, off · Regular+ · `c_useEngLinks`  
Also: Only use English links (do not G-translate) · Greyed out by: “Disable ALL Internet Use”

> When using a non-English interface (such as French, Spanish, Hindi, etc.) most links to external websites get sent via the Google Translate site so that you can read the information in the same language as the selected interface.
>
> Enable this option if Google is blocked in your country, or you simply prefer to read the original page in English.

Useful where Google is blocked.

###### Disable ALL Internet Use

Checkbox, off · Regular+ · `c_noInternet`  
Also: Disable internet use

> PTXprint checks for program updates and also contains links to external sites (mainly from the Styles tab and the Help tab). If this is an issue, then check this option to prevent PTXprint from accessing the internet.

Website links (for example on the **Help** tab) are hidden. Use it where internet use is expensive, slow or not safe. This setting belongs to your computer, not to the configuration.

###### Plugins – List of plugins

Text box · Full · `t_plugins` · cfg `project/plugins`

> Some advanced features load extra code that is not normally needed. List them here if you need to use them. For example, if you are generating a QR code, then you need to add qr to the list of plugins. For a polyglot, you can add polyglot-simplepages

Separate names with commas or spaces. PTXprint loads the plugins for ornaments, polyglot layouts and covers by itself when you use those features. Leave the box empty unless you know you need a plugin.

###### Use Interlinear Punctuation

Checkbox, off · Full · `c_usePunctuation` · cfg `project/interpunc`  
Also: Place Ruby text above words

> Include specifically modified interlinearized punctuation.

Used with **Interlinear**: includes the punctuation stored in the Paratext interlinear data. When unticked, those punctuation entries are left out.

###### Auto-tag Hebrew and Greek words

Checkbox, on · Regular+ · `c_autoTagHebGrk` · cfg `project/autotaghebgrk`

> Auto-tag Hebrew words \wh ... \wh* and Greek words with  \wg ... \wg*
>
> PTXprint can automatically tag all source language words (Hebrew and Greek) with the appropriate markup to ensure they display with the right font and direction for that script.

This avoids empty boxes in place of letters. Leave it ticked unless the project already marks these words itself. Hebrew words are not marked if the project itself uses the Hebrew script; the same applies to Greek.

###### Lock XeTeX Layout Level

Checkbox, off · Full · `c_lockXeTeXLayout` · cfg `config/lockxetexlayout`  
Also: Lock XeTeX Layout Settings

> This feature enables final typesetting to proceed with minimal risk of change to the final layout by locking the TeX macros to use the current layout logic, which will prevent newer functionality from taking effect in the future. This sets the "Maximum Layout Version" value in the TeXpert Hacks section.

Ticking it sets **Maximum layout version** (**Other** › **Page Layout and Spacing**) to the current version, so later updates do not change how your pages break. Use it near the end of a project. Unticking it sets **Maximum layout version** back to 0 (newest rules).

###### Lock UI Layout Settings

Checkbox, off · Full · `c_lockUI4Layout` · cfg `config/lockui4layout`

> This feature enables final typesetting to proceed with minimal risk of change to the final layout by disabling various controls (on the layout, fonts and styles tabs) so that settings can't be accidentally changed while doing final page layout.

Greys out page size, margins, font size, line spacing, columns and gutters, and the whole **Fonts+Script** and **Styles** tabs. Untick it to make changes again.

##### Capture tests?

###### Test recording in progress

Checkbox, off · Full · `c_testrecording`  
Also: Sensitive project

> Record PTXPrint options clicked for use in creating an automated test.
>
> Will stop recording when Save is pressed or the checkbox is unticked and a dialog will allow saving the test in zip format.

When you untick it (or save), PTXprint asks where to save the test zip file. Normal users do not need this.

#### Other

##### Page Layout and Spacing

###### Maximum layout version

Number · Regular+ · `s_ptxversion` · cfg `texpert/ptxversion`  
Values: 0–10 (default 0)

> Maximum layout version to use or 0 for any. Used to maintain backward compatibility when the TeX macros have been changed in newer versions of PTXprint.

Pages sometimes break differently after an update. A value here uses the layout rules of that older version. Normally set it with **Lock XeTeX Layout Level**, not by hand. Some settings depend on it; for example, from version 6 the enhanced paragraphed footnotes are always used.

###### Legacy 1/14 LineSpacing

Checkbox, off · Regular+ · `c_linespacebase` · cfg `texpert/linespacebase`

> In the past, SpaceAbove and SpaceBelow were, in effect units of 1/14 of the base line spacing. This has changed so they are now in units of 1/12 of the base line spacing. Enabling this compatibility reverts the units.

For old projects only. Tick it if an old project's spacing changed after an update and you want the old spacing back.

###### Where to start a new book

Drop-down · Regular+ · `fcb_bookstartpage` · cfg `texpert/bookstartpage`  
Choices: Next page | Same page | Odd page

> Does a scripture book start on a new page, the same page as the previous book (if <65% of page has been used), or an odd page

**Same page** saves paper. **Odd page** adds blank pages where needed. See also **Page full factor**.

###### Page full factor

Number · Regular+ · `s_pagefullfactor` · cfg `texpert/pagefullfactor`  
Values: 0.3–0.9 (default 0.65)

> This setting is related to how full a page needs to be to force the next book to start on a new page.

The part of the page (0.65 = about two thirds). With **Same page**, if the previous book fills more than this, the next book goes to a new page. The same factor is used when single-column text (such as a book title or introduction) is followed by two-column text. A higher value lets more books share a page.

###### Where to start a new intro page

Drop-down · Regular+ · `fcb_intropagealign` · cfg `texpert/intropagealign`  
Choices: Next page | No page breaks | On an odd page | Grouped

> Does an intro page start on a new page, the same page as the previous book, an odd page, or group all adjacent intro pages into an odd paged group

**No page breaks** lets the introduction follow on the same page. **Grouped** keeps adjacent introductions together and starts the group on an odd page.

###### Unbalanced Lines (Max)

Number · Regular+ · `s_bottomrag` · cfg `texpert/bottomrag`  
Values: 0–10 (default 3)

> Maximum number of unbalanced lines allowed in 2-column layout. Recommended range 1-5.

How many lines the two columns may differ at the end of a page or section. 0 forces balanced columns.

###### Variable line spacing maximum stretch

Number · Regular+ · `s_interlinestretch` · cfg `texpert/interlinestretch`  
Values: 0–10 (default 2)

> Maximum stretch to insert between lines in variable line spacing in pts

1 pt is about 0.35 mm. A larger value fills columns more easily, but the line spacing looks less even.

###### Variable line spacing maximum shrink

Number · Regular+ · `s_interlineshrink` · cfg `texpert/interlineshrink`  
Values: 0–3 (default 0.3)

> Maximum shrink to insert between lines in variable line spacing in pts

Keep it small. Lines too close together are hard to read.

###### No Top Space

Checkbox, on · Regular+ · `c_squashgrid` · cfg `texpert/squashgrid`

> Don’t insert space above headings at the start of a column

Keeps the tops of columns level. Untick it for the full space above every heading, even at the top of a column.

###### Suppress pagebreak after bookend-final

Checkbox, off · Regular+ · `c_lastnoeject` · cfg `texpert/lastnoeject`

> Revert to old behaviour of not ensuring that the whole of the last book is output before back-matter PDFs

Normally the last book ends with a page break, so a back-matter PDF starts on a new page. Tick this only to go back to the old behaviour.

###### Noteline offset (mm)

Number · Regular+ · `s_notelineoffset` · cfg `texpert/notelineoffset`  
Values: 0–100 (default 3)

> Gap (mm) between noteline and text

Notelines are turned on with **Notelines** on the **Layout** tab.

###### Noteline margin (mm)

Number · Regular+ · `s_notelinemargin` · cfg `texpert/notelinemargin`  
Values: 0–100 (default 10)

> Gap (mm) between noteline and edge of page

A bigger value keeps the lines from being cut off when the pages are trimmed.

###### Noteline type

Drop-down · Regular+ · `fcb_notelinetype` · cfg `texpert/notelinetype`  
Choices: Solid line | Row of dots

> Sometimes it is preferable to use a series of dots rather than a solid line.

Dots are lighter and disturb the text less.

###### Noteline spacing (mm)

Number · Regular+ · `s_noteliney` · cfg `texpert/noteliney`  
Values: 0–25 (default 0)

> Line spacing between notelines. When set to 0.00 the default line spacing of the document is used.

0 makes the notelines match the text lines. Increase it if readers need more room to write.

###### Noteline width (major)

Number · Regular+ · `s_notelinemajor` · cfg `texpert/notelinemajor`  
Values: 0–10 (default 0.5)

> Thickness (pt) of major notelines. Specify the colour on the Layout page.

Thin lines (0.2 to 0.5) look best.

###### Double Sided Layout

Checkbox, on · Regular+ · `c_doublesided` · cfg `texpert/doublesided`

> This setting can be disabled to turn off inner/outer margins, forcing the inner/outer gutter, and Notelines to always appear on the same side of the printed page.

When ticked, inner and outer margins swap on even pages and the even-page headers and footers are used. Untick it for one-sided printing: every page then uses the same margins and the odd-page header and footer.

###### Maximum parallel processes

Number · Regular+ · `s_maxproc` · cfg `texpert/maxproc`

> The maximum number of parallel processes to use for example when page filling

Also used when you print several publications. The default depends on the number of processors in your computer. Lower it if your computer becomes slow or runs out of memory.

###### Maximum Filling Time (mins)

Number · Regular+ · `s_maxfilltime` · cfg `texpert/maxfilltime`  
Values: 0–100 (default 0)

> Stop page filling a book after this many minutes

We could not confirm that the current code uses this. To limit page filler time, use **Time limit for the whole job (minutes)** in **Automatic Page Filler**.

##### Chapter and Verse

###### Position of marginal verse hyphen if any

Drop-down · Regular+ · `fcb_vhyphenmode` · cfg `texpert/vhyphenmode`  
Choices: Always down | Always up | Up on left | Up on right | No hyphens

> Insert or not a marginal verse hyphen in verse ranges, whether on the first or second line

For a verse range such as 3-4 shown as a marginal verse number. **Up on left** and **Up on right** put the hyphen on the first line only in the left or right margin. Marginal verses are turned on with **Marginal Verses** on the **Body** tab.

###### Gutter space reduction for marginal verses

Checkbox, off · Regular+ · `c_mverseismargin` · cfg `texpert/mverseismargin`

> If false, the space for marginal verses is taken from the column. If true, some space for marginal verses is taken from the margins or rule gutter

Unticked, the column becomes narrower. Ticked, part of the space comes from the margin or the gutter (the space between columns), so the text keeps more width.

###### Auto Calc Optimum Chapter Size

Checkbox, on · Regular+ · `c_calcchapsize` · cfg `texpert/calcchapsize`

> Attempt to automatically calculate drop chapter number size

Makes a large chapter number fill exactly two lines, when the `\c` style is not much larger than the body text. Untick it to set the size yourself on the **Styles** tab.

###### Don't hang verse one beside a chapter (in poetry)

Checkbox, on · Regular+ · `c_nohangvone` · cfg `texpert/nohangvone`

> Hanging verses into a chapter number can result in clashes, depending on the after-chapter space. If so, then turn off hanging verse numbers for the first verse (in poetry only).

Untick it only if the after-chapter space is wide enough and you want verse 1 to hang like the others.

###### Alternate verse numbers also hang

Checkbox, off · Regular+ · `c_hangva` · cfg `texpert/hangva`

> If there is an alternative verse and the current verse is hanging, does the alternate hang?

For alternative verse numbers (`\va`). Most projects do not use them.

###### After chapter space factor

Number · Regular+ · `s_afterchapterspace` · cfg `texpert/afterchapterspace`  
Values: -0.2–1 (default 0.25)

> This sets the gap between the chapter number and the text following. The setting here is a multiple of the main body text size as specified in layout.

0.25 = a quarter of the text size. Increase it if text looks crowded against the chapter number. Negative values move the text closer.

###### After verse space factor

Number · Regular+ · `s_afterversespace` · cfg `texpert/afterversespace`  
Values: -0.2–1 (default 0.15)

> This sets the gap between the verse number and the text following. The setting here is a multiple of the main body text size as specified in layout.

Change it only if verse numbers look too close to the text, or too far from it.

##### Body Text

###### Allow Indent Para with Cutouts

Checkbox, off · Regular+ · `c_chapindent` · cfg `texpert/chapindent`

> Allow indented paragraphs at chapter start with cutouts

Unticked, the lines next to a large chapter number (a cutout) are not indented. Tick it to keep the paragraph's normal indent there.

###### Allow Indent Para After Heading

Checkbox, on · Regular+ · `c_afterheadindent` · cfg `texpert/afterheadindent`

> Allow indented paragraphs following a heading

Untick it to start the first line after a heading at the margin, a common book style.

###### Maximum orphan word length

Number · Regular+ · `s_maxorphanlength` · cfg `texpert/maxorphanlength`  
Values: 1–20 (default 8)

> Maximum length of the word that will receive orphan protection at the end of a paragraph

An orphan word is a short word alone on the last line of a paragraph. With **Prevent Orphan Words** (**Body** tab), PTXprint keeps the last word with the word before it. Longer last words (in characters) can stand alone.

###### Bad space penalty

Number · Regular+ · `s_badsppen` · cfg `texpert/badsppen`  
Values: -10000–10000 (default 100)

> Penalty for a bad (but not impossible) place to break

PTXprint uses "bad" spaces, for example, to keep orphan words with the word before them. Higher = break less likely; 10000 forbids it. A negative value encourages a break.

###### Optional break penalty

Number · Regular+ · `s_optbkpen` · cfg `texpert/optbkpen`  
Values: 0–10000 (default 300)

> Penalty for the optional break

The optional break is the place you mark with `//` in the USFM text. A higher value makes the break more attractive. Change it only if lines break there too often or too seldom.

###### Hyphenation threshold

Number · Regular+ · `s_pretolerance` · cfg `texpert/pretolerance`  
Values: -1–10000 (default 100)

> Paragraph badness threshold before trying hyphenation. Set to -1 to always hyphenate

Hyphenation is tried only for paragraphs that look bad without it. Lower values hyphenate more often. Only matters when hyphenation is on.

###### Penalty for inserting hyphen

Number · Regular+ · `s_hyphenpenalty` · cfg `texpert/hyphenpenalty`  
Values: -9999–10000 (default 50)

> Hyphenation penalty

Higher = fewer hyphens, but possibly wider word spaces. 10000 or more stops hyphenation completely.

###### Double hyphenation penalty

Number · Regular+ · `s_doublehyphendemerits` · cfg `texpert/doublehyphendemerits`  
Values: 0–1e+06 (default 10000)

> Penalty for consecutive hyphenation across two lines

Higher makes two hyphenated lines in a row rarer. The default is already high.

###### Use loc attrib on ref to make a link

Checkbox, on · Regular+ · `c_userefloc` · cfg `texpert/userefloc`

> The ref character style can include an attribute like loc="GEN 1:2". Should this be used to make a clickable link?

Turns `\ref` references into links you can click in the PDF to jump to that verse.

###### Use href-link attrib on jmp to make a link

Checkbox, on · Regular+ · `c_hreflink` · cfg `texpert/hreflink`

> The jmp character style can include an attribute like href-link="https://my.web.site/". Should this be used to make a clickable link?

Untick it for a printed book where active links are not wanted.

###### Box style for URL links

Drop-down · Regular+ · `fcb_urllinkborderstyle` · cfg `texpert/urllinkborderstyle`  
Choices: Underline only | No line | Solid line | Row of dots | Dashed line | Viewer default

> Active web links in PDFs are marked by either a box (solid, dashed or dotted line) or an underline. Your viewer probably has a default setting. Set the colour with \def\URLLinkBorderCol{0.9 0.5 0.5} or similar in ptxprint-mods.tex.

The mark is only visible on screen; it is not printed. The link colour can only be changed by an expert, in `ptxprint-mods.tex`.

###### Box style for GOTO links

Drop-down · Regular+ · `fcb_gotolinkborderstyle` · cfg `texpert/gotolinkborderstyle`  
Choices: Underline only | No line | Solid line | Row of dots | Dashed line | Viewer default

> Active internal links in PDFs are marked by either a box (solid, dashed or dotted line) or an underline. Your viewer probably has a default setting. Set the colour with \def\GOTOLinkBorderCol{0.9 0.5 0.5} or similar in ptxprint-mods.tex.

For links inside the PDF, for example from a cross-reference to a verse. Not printed.

##### Fonts and Underline

###### Use glyph metrics

Checkbox, off · Regular+ · `c_useglyphmetrics` · cfg `texpert/useglyphmetrics`

> PTXprint can use either the actual glyph metrics in a line or the font metrics to calculate line heights and depths. Font metrics gives more consistent results.

Unticked, every line is measured the same way and spacing is even. Ticked, the real letter shapes in each line are used. Leave it unticked unless a support person suggests otherwise.

###### Use system fonts

Checkbox, on · Regular+ · `c_usesysfonts` · cfg `texpert/usesysfonts`

> Use fonts from your system as well as your project. Note that you need to restart PTXprint for this setting to take effect.

Untick it to use only fonts stored with the project, so the result is the same on every computer.

###### Underline thickness (em)

Number · Regular+ · `s_underlinethickness` · cfg `texpert/underlinethickness`  
Values: 0.01–0.5 (default 0.05)

> This sets the thickness of the text underline, (measured in ems).

em = the size of the font. 0.05 is a thin line.

###### Underline vertical position (em)

Number · Regular+ · `s_underlineposition` · cfg `texpert/underlineposition`  
Values: -1–1 (default 0.1)

> This sets how far (in ems) the underline is below the text and what it is relative to. If negative, it is the distance below the baseline. If positive (or zero), it is the distance below the bottom of any descenders.

Descenders are the parts of letters like g and p that go below the baseline (the line letters sit on). Increase it if underlines touch the letters.

###### Underline Spaces

Checkbox, on · Regular+ · `c_underlnsp` · cfg `texpert/underlnsp`

> Underline spaces in underlined runs

Ticked, the underline is unbroken. Untick it to underline only the words.

###### Log font creation

Checkbox, off · Regular+ · `c_logfontusage` · cfg `texpert/logfontusage`

> Create <jobname>.fontusage in the local/ptxprint/<config>/ directory, which will list the page number and exact font definition when each new style is first used.

Useful for finding where an unexpected font comes from. It does not change the PDF. A support person may ask you to turn it on.

##### Footnotes, Cross-references, Study Notes

###### Mid-Page Footnotes

Checkbox, off · Regular+ · `c_midnotes` · cfg `texpert/midnotes`

> Should footnotes go before a single-double column transition

For single-column text (for example an introduction) followed by two-column text. Ticked, the notes of the single-column part come right after it, mid-page. Unticked, all notes go to the bottom of the page.

###### Final Page Notes Down

Checkbox, off · Regular+ · `c_fnotesdown` · cfg `texpert/fnotesdown`

> Push notes on the final page to the bottom of the page

For the last page of a book, where the text may end high. Unticked, the notes follow straight after the text.

###### Reset Callers at Each Book

Checkbox, on · Regular+ · `c_bookresetcallers` · cfg `texpert/bookresetcallers`

> Re-start the footnote and cross-reference callers at the start of each book

Untick it to continue the caller sequence (a, b, c …) across books.

###### Endnotes at Each Book

Checkbox, on · Regular+ · `c_neachbook` · cfg `texpert/neachbook`

> Output endnotes at the end of each book

Untick it to collect all endnotes at the end of the last book.

###### Enhanced paragraphed footnotes

Checkbox, off · Regular+ · `c_newparnotes` · cfg `texpert/newparnotes`

> Paragraphed footnotes which allow \fp to work and also the ifparnotes... controls below. Causes some spacing differences compared to old-style.

Paragraphed footnotes run several notes together in one paragraph. With the current layout version this is always on; the box only matters when **Maximum layout version** is 5 or lower.

###### Remove depth above paragraphed notes

Checkbox, on · Regular+ · `c_parntkillpd` · cfg `texpert/parntkillpd`

> Kern away (kill) the glyph/font depth of note types before paragraphed notes, using the value of \prevdepth

Keeps the space between different note types even. Change it only to solve a specific spacing problem.

###### Remove depth after paragraphed notes

Checkbox, off · Regular+ · `c_parntkilldepth` · cfg `texpert/parntkilldepth`

> Kill the depth of (the last row of) paragraphed note styles. Paragraphed notes will use the margin as their baseline.

Ticked, the last line of paragraphed notes sits on the bottom margin. Unticked, space for letters below the baseline (such as g and p) is kept.

###### Use grid not font/glyph height at rule

Checkbox, off · Regular+ · `c_parntruletopskip` · cfg `texpert/parntruletopskip`

> If true, the footnote rule is positioned relative to the hypothetical baseline above the topmost footnote, rather than relative to the glyph/font height.

The footnote rule is the line above the notes. Unticked, it is placed relative to the height of the letters in the first note. Change it only if the space between rule and notes looks wrong.

###### Use grid not font/glyph height between notes

Checkbox, on · Regular+ · `c_parntmidtopskip` · cfg `texpert/parntmidtopskip`

> If true, then the \InterNoteSpace is relative to the hypothetical baseline above the topmost footnote, rather than the glyph/font height. \InterNoteSpace is triggered between note styles.

For the space between two note types (for example footnotes and cross-references). Ticked gives the same space everywhere. Untick it to measure from the letter height.

###### Use glyph height not font height in footnotes

Checkbox, off · Regular+ · `c_fnxugm` · cfg `texpert/fnxugm`

> Does the note use the font's descender design parameter, or the actual bottom of the glyph. If the former (and depth is not killed), then the bottom of notes have a common baseline across pages. If the latter, then the glyphs sit as close to the bottom margin as they can, which may permit an extra line of text.

Unticked, the last line of notes is at the same height on every page. Ticked, notes sit as low as possible, which sometimes leaves room for an extra line of text.

###### Last Note: interlinepenalty

Number · Regular+ · `s_lastnoteinterlinep` · cfg `texpert/lastnoteinterlinep`  
Values: -9999–10000 (default 10000)

> Penalty for breaking between lines of the last footnote.

10000 = never split the last footnote across pages. Lower values allow a split, which can help fill pages with many notes.

###### Last Note: widowpenalty

Number · Regular+ · `s_lastnotewidowp` · cfg `texpert/lastnotewidowp`  
Values: -9999–10000 (default 10000)

> Extra penalty for breaking at the last line of the last footnote.

For a split that leaves only the last line on the next page. 10000 forbids it.

###### Last Note: clubpenalty

Number · Regular+ · `s_lastnoteclubp` · cfg `texpert/lastnoteclubp`  
Values: -9999–10000 (default 10000)

> Extra penalty for breaking at the first line of the last footnote.

For a split that leaves only the first line on the page. 10000 forbids it.

###### Last Note: penalty at par

Number · Regular+ · `s_lastnoteparp` · cfg `texpert/lastnoteparp`  
Values: -9999–10000 (default 100)

> Penalty for breaking at an explicit footnote-paragraph in the last footnote.

The default 100 allows a split at a note paragraph more easily than mid-paragraph.

###### Split notes: Shortest note to shave

Number · Regular+ · `s_nshaveshort` · cfg `texpert/nshaveshort`  
Values: 0–100 (default 2)

> If footnotes might be shaved, how many lines must it be?

"Shaving" splits a note that does not fit and moves part to the next page. Shorter notes are kept whole.

###### Split notes: min lines to move.

Number · Regular+ · `s_nshavemin` · cfg `texpert/nshavemin`  
Values: 0–100 (default 2)

> If a footnote is being shaved (split onto next page), what is the minimum number of lines to move?

Avoids moving a single lonely line.

###### Split notes: note lines to stay

Number · Regular+ · `s_nshavestay` · cfg `texpert/nshavestay`  
Values: 0–100 (default 2)

> If a footnote is being shaved (split onto next page), how many lines of (all) notes must remain on the page?

Counts lines of all notes.

###### Study note factor-Single column

Number · Regular+ · `s_footnotemulsts` · cfg `texpert/footnotemulsts`  
Values: 0–2100 (default 400)

> To avoid needless cycles/underfull pages, what portion of a study note's height-estimate should TeX apply when gathering input in single-column mode? (100=10percent)

PTXprint guesses how much space study notes need while it collects text for a page. 1000 = 100%. Lower values can give fuller pages but more work; higher values can leave pages underfull. Change it only on advice.

###### Study note factor-Two column

Number · Regular+ · `s_footnotemulstt` · cfg `texpert/footnotemulstt`  
Values: 0–2100 (default 800)

> To avoid needless cycles/underfull pages, what portion of a study note's height-estimate should TeX apply when gathering input in two-column mode? (100=10percent)

Same as **Study note factor-Single column**, for two-column text.

###### Study note factor-Diglot

Number · Regular+ · `s_footnotemulstd` · cfg `texpert/footnotemulstd`  
Values: 0–2100 (default 500)

> To avoid needless cycles/underfull pages, what portion of a study note's height-estimate should TeX apply when gathering diglot input? (100=10percent)

Same as **Study note factor-Single column**, for diglot text.

###### Footnote factor-Single column

Number · Regular+ · `s_footnotemuls` · cfg `texpert/footnotemuls`  
Values: 0–2100 (default 400)

> To avoid needless cycles/underfull pages, what portion of a note's height-estimate should TeX apply when gathering input in single-column mode? (100=10percent)

Same idea for ordinary footnotes. Change it only on advice.

###### Footnote factor-Two column

Number · Regular+ · `s_footnotemult` · cfg `texpert/footnotemult`  
Values: 0–2100 (default 800)

> To avoid needless cycles/underfull pages, what portion of a note's height-estimate should TeX apply when gathering input in two-column mode? (100=10percent)

Change it only on advice.

###### Footnote factor-Diglot

Number · Regular+ · `s_footnotemuld` · cfg `texpert/footnotemuld`  
Values: 0–2100 (default 10)

> To avoid needless cycles/underfull pages, what portion of a note's height-estimate should TeX apply when gathering diglot input? (100=10percent)

Change it only on advice.

###### Footnote factor-Centre column

Number · Regular+ · `s_footnotemulc` · cfg `texpert/footnotemulc`  
Values: 0–2100 (default 1)

> To avoid needless cycles/underfull pages, what portion of a note's height-estimate should TeX apply when gathering centre-column notes? (100=10percent)

For example cross-references between two columns. These notes do not take space from the text column, so the default is very low.

###### Distance of margin notes from text

Number · Regular+ · `s_marginnotesgap` · cfg `texpert/marginnotesgap`  
Values: 0–100 (default 6)

> The size of the gap between the margin notes and the text

A larger number moves margin notes further from the text. Margin notes are turned on, and their width set, on the **Layout** tab, **Page Setup** area (**Margin Notes Col Width (mm)** and **Margin Notes on Left/Inner**).

##### Diglot

###### Balance diglot/polyglot notes

Checkbox, off · Regular+ · `c_diglotbalnotes` · cfg `texpert/diglotbalnotes`

> When there's a note on column R (for example), does that reduce the space from other columns?

Tick it to keep the bottoms of all columns level. Unticked, each column uses its own space.

###### Diglot/polyglot merged paragraphed notes are RTL

Checkbox, off · Regular+ · `c_mergednotesrtl` · cfg `texpert/mergednotesrtl`

> When merged notes are not shown as individual paragraphs, the result must be arranged as though RTL or LTR (however the individual notes are structured). This defines the paragraph alignment.

Tick it when the merged notes should read right-to-left. Getting this wrong arranges the notes badly, so match it to the language of the notes.

###### Adjust Versification of Projects

Checkbox, on · Regular+ · `c_reversify` · cfg `texpert/reversify`

> If versification differs between projects, adjust diglot/polyglot projects to match the primary (L) project.

Keeps matching verses side by side. Leave it ticked unless the projects already use the same versification.

###### Keep existing verse numbers (as \vp)

Checkbox, on · Regular+ · `c_showvpvrse` · cfg `texpert/showvpvrse`

> When adjusting versification, show the original verse numbers in their new (adjusted) location.

Readers then see the verse numbers of their own translation.

###### Show old chapter numbers if changed (in \vp)

Checkbox, on · Regular+ · `c_showvpchap` · cfg `texpert/showvpchap`

> When adjusting versification, show the adjusted chapter numbers (only) if they have changed.

The old chapter number is shown with the verse number.

###### Show Diglot Trace Marks

Checkbox, off · Regular+ · `c_vistrace` · cfg `texpert/vistrace`

> Insert visible trace marks in diglot output

Marks where the column pieces are joined, to find layout problems. Turn it off for the final PDF.

###### Extra Trace Mark Info

Checkbox, off · Regular+ · `c_vistracex` · cfg `texpert/vistracex`

> Add extra information to diglot trace marks. (debugging only - can alter layout)

Debugging only; it can change the layout.

###### Diglot Shading Padding

Number · Regular+ · `s_diglotcolourpad` · cfg `texpert/diglotcolourpad`  
Values: -20–20 (default 3)

> The amount of side padding (pt) on the shaded background of a diglot

Larger extends the shading further beyond the text. Negative values make it narrower than the text.

###### How does text-border behave in diglots?

Drop-down · Regular+ · `fcb_textbordermode` · cfg `texpert/textbordermode`  
Choices: Borders start at body text | Borders include book intros | Wide book intros for per-column textborders

> Historically, diglot text-borders put the border around book introductions. This control allows that (substandard) behaviour to be chosen, and also allows  experimental code to make books with per-column textborders use full-width text for introductory text.

**Borders start at body text** leaves book introductions outside the border. **Borders include book intros** is the old behaviour. **Wide book intros for per-column textborders** is experimental: introductions use the full page width when each column has its own border.

###### Unprintable page recovery.

Number · Regular+ · `s_growunprintable` · cfg `texpert/growunprintable`  
Values: -1–10 (default 2)

> If notes / figures make a page unprintable: -1: immediately stop; 0: print failed contents and try to struggle on; >0 grow page height by up to N lines.

Grown pages may extend into the bottom margin, so check them.

###### Page-full test.

Drop-down · Regular+ · `fcb_pagefulltest` · cfg `texpert/pagefulltest`  
Choices: 1xBiggest baseline | 2xSmallest baseline | 2xBiggest baseline | 3xSmallest baseline

> When a (non-title) chunk has finished, the amount of unused space below which diglot will immediately output a page,  rather than trying to fit the next chunk. (irrespective of how short it is). Higher values encourage underfilled pages, but can prevent orphaning of the 1st line of poetry.

We could not confirm that a change here reaches the typesetting code in the current version.

##### Pictures, Figures, Images, Sidebars

###### Default Figures Top Left

Checkbox, on · Regular+ · `c_figleft` · cfg `texpert/figleft`

> Default figure positions to top left

For two-column pictures with no usable position: PTXprint places them at the top of a column, alternating left and right. Ticked, it starts with the left column.

###### Ref Before Caption

Checkbox, off · Regular+ · `c_captreffirst` · cfg `texpert/captreffirst`

> Output reference before caption

Puts the verse reference before the caption text.

###### Show Caption Before Image

Checkbox, off · Regular+ · `c_captfirst` · cfg `texpert/captfirst`

> Output caption before image

Puts the caption above the picture.

###### Space (pt) beside cutout/sidebar

Number · Regular+ · `s_cutouterpadding` · cfg `texpert/cutouterpadding`  
Values: 0–50 (default 10)

> This sets the default gap (pt) between the body text and the side of a figure/sidebar in a cutout.

A cutout is a space cut into the side of the text. This value is used when a picture or sidebar does not set its own space. **Default space beside picture** sets the same value and wins when changed from its default.

###### Space between picture & caption

Number · Regular+ · `s_captionadj` · cfg `texpert/captionadj`  
Values: -10–20 (default 0)

> Increase/Reduce the gap between figures and their captions

Negative values remove space, in points.

###### Default space beside picture

Number · Regular+ · `s_spbeside` · cfg `texpert/spbeside`  
Values: 0–100 (default 10)

> Picture horizontal margin*2

Horizontal space, in points. Sets the same value as **Space (pt) beside cutout/sidebar**; when changed from its default (10), this one is used.

###### Show comprehensive illustration credits

Checkbox, off · Regular+ · `c_allpicredits` · cfg `texpert/allpicredits`

> Instead of using the catch-all phrasing 'All other illustrations by...' show a comprehensive list of every artist and all pages that contain their illustrations.

Lists every artist with all the pages of their pictures.

##### PDF Options, Covers, Show/Hide

###### No PDF Bookmarks

Checkbox, off · Regular+ · `c_noactions` · cfg `texpert/noactions`

> Don’t output PDF bookmarks

Bookmarks are the list of books and chapters in a PDF viewer's side panel. Some printers ask for a PDF without them.

###### Allow Active Links in PDF

Checkbox, on · Regular+ · `c_actions` · cfg `texpert/actions`

> Make links active inside PDF

For example cross-references and web links. Untick it for a PDF only for printing.

###### Use Book Codes in PDF Bookmarks

Checkbox, off · Regular+ · `c_refbkmks` · cfg `texpert/refbkmks`

> Use book codes instead of book names in bookmarks

Helps when book names are long or in a script the PDF viewer cannot show.

###### Disable Transparency in PDF

Checkbox, off · Regular+ · `c_notransparent` · cfg `texpert/notransparent`

> Disable transparency output in PDF

For printers that cannot handle transparent colours. Each one becomes a solid colour that looks the same on white paper. Anything behind it is then hidden, so check pages with shading or overlapping pictures.

###### Show adjust points

Checkbox, off · Regular+ · `c_showadjpoints` · cfg `texpert/showadjpoints`

> Show adjust points in the margin of the text.

Marks where paragraph adjustments (stretch or shrink from the adjustment list) apply. Turn it off for the final PDF.

###### Mark Trigger Points

Checkbox, off · Regular+ · `c_mktrigpts` · cfg `texpert/mktrigpts`

> Display trigger points in output

Triggers are instructions tied to a verse, such as a picture position or a style change. Turn it off for the final PDF.

###### Show USFM codes

Checkbox, off · Regular+ · `c_showusfmcodes` · cfg `texpert/showusfmcodes`

> Show the USFM markers in the margin beside paragraphs.

Helps you find which style to change on the **Styles** tab. Turn it off for the final PDF.

###### Show Error Bars For Overfull Lines

Checkbox, off · Regular+ · `c_showhboxerrorbars` · cfg `texpert/showhboxerrorbars`

> Enable this option to have TeX make overfull lines stand out.

A black bar at the end of every overfull line. Fix such lines, for example with hyphenation or small text changes. Then turn this off.

###### Spine Overlap onto Back Cover (mm)

Number · Regular+ · `s_spineoverlapback` · cfg `texpert/spineoverlapback`  
Values: 0–50 (default 0)

> If you want the spine graphic or colour to spill over onto the back cover page, then set the amount of overlap here.

Helps hide small errors when the cover is folded. Used when you make a cover on the **Peripherals** tab.

###### Spine Overlap onto Front Cover (mm)

Number · Regular+ · `s_spineoverlapfront` · cfg `texpert/spineoverlapfront`  
Values: 0–50 (default 0)

> If you want the spine graphic or colour to spill over onto the front cover page, then set the amount of overlap here.

Used when you make a cover.

###### Cover Bleed (mm)

Number · Regular+ · `s_bleed` · cfg `texpert/bleed`  
Values: 0–25 (default 5)

> Bleed is the section of artwork that goes beyond where the paper is cut. This ensures that the image goes right to the edge of the cover after it has been trimmed.

Ask your printer how much bleed they need; often 3 to 5 mm.

###### Hard Cover Art Bleed (mm)

Number · Regular+ · `s_artbleed` · cfg `texpert/artbleed`  
Values: 0–25 (default 0)

> Art Bleed is specifically for hard cover binding and is the setting which enables images to go beyond the size of the cover in order to wrap around the hard cover and stuck down under the inner backing sheet.

Leave it at 0 for soft covers. Ask your printer for the right value.

##### Preview Pane: Adjustment and Analysis Settings

###### Auto-update Delay (seconds)

Number · Regular+ · `s_autoupdatedelay` · cfg `texpert/autoupdatedelay`  
Values: 0–120 (default 3)

> Right-clicking again on the PDF within this time (3 second default) will prevent the Auto-update from running.

A right-click adjustment with **Auto-update** on starts a new print after this delay, so you can make several adjustments first. Increase it if you need more time between adjustments.

###### Shrink Text Step Value (%)

Number · Regular+ · `s_shrinktextstep` · cfg `texpert/shrinktextstep`  
Values: 1–5 (default 1)

> Step Value to shrink text using right-click context menu adjustment.

Percent per "shrink text" step.

###### Minimum Text Shrink (%)

Number · Regular+ · `s_shrinktextlimit` · cfg `texpert/shrinktextlimit`  
Values: 85–100 (default 95)

> Limit how much text can shrink to using right-click context menu adjustment.

95 = at most 5% smaller. The page filler also uses this limit. Shrinking too much makes text look crowded.

###### Expand Text Step Value (%)

Number · Regular+ · `s_expandtextstep` · cfg `texpert/expandtextstep`  
Values: 1–5 (default 1)

> Step Value to expand text using right-click context menu adjustment.

Percent per "expand text" step.

###### Maximum Text Expand (%)

Number · Regular+ · `s_expandtextlimit` · cfg `texpert/expandtextlimit`  
Values: 100–115 (default 105)

> Limit how much text can expand to using right-click context menu adjustment.

105 = at most 5% larger.

###### Bad Space minimum width (em)

Number · Regular+ · `s_spaceEms` · cfg `texpert/spaceEms`  
Values: 0–10 (default 1.3)

> Minimum width for a bad space. 0 says to calculate for the 20 worst spaces in the doc

Used by **Layout Analysis** in the PDF Preview window; em = the size of the font. A lower value marks more spaces.

###### Bad intercharacter space minimum width (em)

Number · Regular+ · `s_charSpaceEms` · cfg `texpert/charSpaceEms`  
Values: 0–1 (default 0.3)

> Minimum width for a bad inter character space.

Only used when **Between Letters** spacing is on (**Fonts+Script** tab).

###### Precise collisions

Checkbox, off · Regular+ · `c_collisionPrecise` · cfg `texpert/collisionPrecise`

> Only show precise collisions between glyphs rather than overlapping bounding boxes - slow

Finds fewer false collisions.

###### Collision Detection Padding (pt)

Number · Regular+ · `s_paddingwidth` · cfg `texpert/paddingwidth`  
Values: -1–5 (default 0.5)

> Minimum space between bounding boxes of glyphs before a collision is flagged.

For boxes around letters on different lines. A larger value reports more possible collisions.

###### River Detection Threshold (em)

Number · Regular+ · `s_riverthreshold` · cfg `texpert/riverthreshold`  
Values: 1–1000 (default 3)

> The sum of all the widths in the river must be above this for the river to be detected

Increase it to report only the worst rivers.

###### River Detection minimum required maximum width (em)

Number · Regular+ · `s_riverminmaxwidth` · cfg `texpert/riverminmaxwidth`  
Values: 0.1–5 (default 1)

> Minimum width required for the widest part of the river

In em.

###### River Detection minimum width (em)

Number · Regular+ · `s_riverminwidth` · cfg `texpert/riverminwidth`  
Values: 0.1–5 (default 0.5)

> Minimum width of any space in a river for it to be included

Narrower spaces are not counted as part of a river.

###### River Detection maximum line leading (em)

Number · Regular+ · `s_rivergap` · cfg `texpert/rivergap`  
Values: 0–5 (default 0.4)

> Any lines separated by a gap greater than this will be considered not to be in the same river

In em.

###### River Detection minimum overlap (em)

Number · Regular+ · `s_riveroverlap` · cfg `texpert/riveroverlap`  
Values: -5–5 (default 0.4)

> Minimum overlap in ems required for two spaces above each other to be considered part of the same river

For two spaces on lines above each other.

##### Automatic Page Filler

###### Time limit for the whole job (minutes)

Number · Regular+ · `s_pbtimeout` · cfg `texpert/pbtimeout`  
Values: 0–1000 (default 180)

> The page filler works on all the books together. When this time is reached, the page filler stops. A book that is not finished keeps the pages that are already filled. Usually this affects only the longest book.  
> Higher: more time to find a good layout for every page.

0 means no time limit. Increase it for a long Bible if the longest book does not finish.

###### Earlier pages to retry

Number · Regular+ · `s_pbbacktrack` · cfg `texpert/pbbacktrack`  
Values: 0–10 (default 4)

> If the page filler cannot fill a page, it backtracks to the page before and tries a different layout there. This is the largest number of pages it can backtrack.  
> Higher: fewer failed pages, but much slower.  
> Lower: faster, but more pages may fail. 0 = never backtrack (fastest).  
> Affects: Speed.

How many earlier pages the page filler may go back to try a different layout.

###### Paragraphs to adjust on each page

Number · Regular+ · `s_pbmaxr` · cfg `texpert/pbmaxr`  
Values: 1–10 (default 6)

> The largest number of paragraphs on one page that the page filler may stretch or shrink. Each poetry line (\q1, \q2 …) counts as one paragraph. Each extra paragraph doubles the number of layouts the page filler tries.  
> Higher: more ways to fill each page, so fewer failed pages, but each page takes longer.  
> Lower: faster, but more pages may fail.  
> Affects: Speed.

Keep it low unless many pages fail.

###### Widest word space allowed (× text size)

Number · Regular+ · `s_pbspacingtol` · cfg `texpert/pbspacingtol`  
Values: 0–10 (default 1)

> When the page filler stretches a paragraph, the average space between words must not be wider than this. 1.0 = as wide as the text size. A normal word space is about 0.3 to 0.5.  
> Higher: easier to fill pages, but the text can look too spread out.  
> Lower: tighter, better-looking text, but pages are harder to fill and take longer.  
> Affects: Quality and Speed.

As a part of the text size.

###### Keep paragraphs close to normal width

Number · Regular+ · `s_pbexpbad` · cfg `texpert/pbexpbad`  
Values: 0–10 (default 1)

> The page filler prefers small changes to a paragraph over big changes. This setting controls how strong that preference is. Higher: the page filler tries small changes first, so the text looks more even.  
> Lower: the page filler accepts big changes more easily.  
> Affects: Quality.

Higher values give more even text.

###### Penalise shrink or stretch

Number · Regular+ · `s_pbexpcost` · cfg `texpert/pbexpcost`  
Values: -5–5 (default 1)

> Tells the page filler whether to shrink paragraphs or stretch them when both are possible.  
> Positive numbers: penalise stretching (so the text prefers to shrink more).  
> Negative numbers: penalise shrinking. (so the text prefers to stretch more).  
> 0: no preference.  
> A bigger number (+ or −) means a higher penalty.  
> Affects: Quality.

Applies when both shrinking and stretching would work.

###### Keep neighbouring paragraphs alike

Number · Regular+ · `s_pbcontrast` · cfg `texpert/pbcontrast`  
Values: 0–20 (default 3)

> The page filler compares each paragraph with the paragraph before it. It tries to avoid a very stretched paragraph next to a very shrunk one.  
> Higher: neighbouring paragraphs look more alike, so the page looks more even.  
> Lower: neighbouring paragraphs can look more different.  
> Affects: Quality.

Higher values give a more even page.

###### The cost of imbalance in a polyglot slice

Number · Regular+ · `s_pbpolyimbalance` · cfg `texpert/pbpolyimbalance`  
Values: 0–10 (default 1)

> How bad is it for a polyglot slice to not be balanced. This the multiplier of that cost  
> Only relevant to diglot and polyglot projects

The page filler works on slices: pieces of text that belong together across the columns, such as the same verses in each language. A slice is unbalanced when one column ends lower than another. This sets how much to avoid that, compared with stretching or shrinking paragraphs. Higher: columns end more evenly, but paragraphs may change more. Lower: paragraphs look more even, but one column may end a few lines lower. Change it only if your diglot columns are often uneven after page filling.

##### Other Miscellaneous Settings

###### Use \toc3 for Tab Text

Checkbox, on · Regular+ · `c_tocthreetab` · cfg `texpert/tocthreetab`

> Use \toc3 for tab text if no \zthumbtab

`\toc3` is the short book name. Thumb tabs are set on the **Tabs+Borders** tab.

###### Tilde is No Break Space

Checkbox, on · Regular+ · `c_tildenbsp` · cfg `texpert/tildenbsp`

> Treat ~ as non breaking space

A non-breaking space looks like a normal space, but the line never breaks there. Untick it only if your text needs a real tilde.

###### Remove \ref ... \ref* links

Checkbox, on · Regular+ · `c_removextreflinks` · cfg `texpert/removextreflinks`

> USFM 3.2 allows additional reference links to be inserted as part of \xt ... \xt* markup. This frequently appear in DBL text bundles, but are unhandled by PTXprint. Allow these to be removed from the USFM prior to typesetting.

These `\ref` links inside cross-references come from Digital Bible Library (DBL) text. Only their visible text is kept.

###### End decoration skip

Number · Regular+ · `s_bedskip` · cfg `texpert/bedskip`  
Values: -100–100 (default 16)

> The gap between the end of the book and the book-end decoration

In points. The decoration is turned on in **Ornamental Decorations** on the **Tabs+Borders** tab. Negative values move it up.

###### Thumbtab rotated adjustment

Number · Regular+ · `s_thumbvvadj` · cfg `texpert/thumbvvadj`  
Values: -10–50 (default -2)

> Shift thumbtab text

Moves the text on rotated thumb tabs (in points) to centre it on the tab. Thumb tabs and **Rotate Tabs** are on the **Tabs+Borders** tab.


# 15. View+Edit tab

## 15.1 What this tab is for

The **View+Edit** tab shows the files that PTXprint uses and creates. You can edit two of
them here: the **front matter** (the pages before the Scripture text, such as the title page
and the table of contents) and the **Adj List** (the list of paragraph adjustments).

Come here to:

* create or change the front matter (title page, copyright page, contents page, preface);
* make a paragraph one line longer or shorter so that a page fits better;
* see the text exactly as PTXprint sent it to the typesetting program;
* read the log of the last print run when something went wrong.

The tab is only shown in the **Regular** and **Full** views. In the **Basic** view PTXprint
still uses the front matter and Adj List that you made before.

## 15.2 The sub-tabs: which files you may edit

Each small tab (sub-tab) along the top shows one file.

| Sub-tab | What it shows | Can you edit it here? |
|---|---|---|
| **Front Matter** | The front matter for this configuration (title page, copyright page, contents, and so on). | **Yes.** This is the main place to edit front matter. |
| **Adj List** | A table of paragraph adjustments for the **Book in Focus**. | **Yes.** You can change values in the table. |
| **Final SFM** | The text of one book after PTXprint has applied all its changes, as it was sent to the typesetter. | **No – look only.** It is created again each time you print. |
| **.tex file** | The control file that PTXprint wrote for the last print run. | **No – look only.** |
| **XeTeX Log** | The log (report) of the last print run. | **No – look only.** |
| **Settings** (up to three) | Other settings files that you chose to open from the **Advanced** tab. | Advanced users only – see the **Advanced** tab chapter. |

**Important:** Make changes to the Scripture text in Paratext, not on the **Final SFM**
sub-tab. That file is replaced every time you print.

The **.tex file** and **XeTeX Log** are useful when you ask for help. A supporter may ask you
to look for an error message in the **XeTeX Log**. You do not need to understand these files
to use PTXprint.

Very long log files are cut short on the screen. Click **View/Edit...** to see the whole file
in your computer's text editor.

## 15.3 The buttons at the top of the tab

The buttons change with the open sub-tab. Buttons that do not apply are greyed out.

* **Refresh** reloads the file from the disk. Unsaved changes are lost.
* **Book in Focus** chooses which book is shown (only on **Adj List** and **Final SFM**).
* **Generate** creates new content for the open sub-tab (see below).
* **View/Edit...** opens the file in your computer's own text editor. On the look-only
  sub-tabs it is called **View Only...**.
* **Edit Variables...** (only on **Front Matter**) takes you to the variables table on the
  **Peripherals** tab.
* The information button (only active on **Front Matter**) lists the special codes when you
  hold the mouse over it.
* **Autosave** decides whether changes are saved without asking.
* The slider changes the size of the text in the editing area.

### Saving your changes

When you change the text on an editable sub-tab, the sub-tab name turns red: there are unsaved
changes. PTXprint saves them:

* when you click outside the text area (without asking if **Autosave** is ticked, otherwise
  after asking);
* when you click **Print** while an editable sub-tab is open.

To throw away your changes, click **Refresh** (or press F5) before you click elsewhere.

If the configuration is locked (see the **Basic** tab), you cannot generate or save front
matter, and **Autosave** is turned off.

## 15.4 The Generate button

**Generate** does a different job on each sub-tab:

* **Front Matter** – opens the **Generate Front Matter** dialog, to start the front matter
  from a template.
* **Adj List** – makes a new adjustment list for the books you are printing (see
  **The Adj List** below).
* **Final SFM** – makes the Final SFM file again for the **Book in Focus**.

On the other sub-tabs **Generate** is greyed out.

## 15.5 The Generate Front Matter dialog

Click **Generate** on the **Front Matter** sub-tab and choose one of four starting points:

* **BASIC** – title page, copyright and licence page, table of contents. A good start for
  most projects.
* **ADVANCED** – more sections, with sample English text that you must translate or delete.
* **DIGLOT** – a fuller template for diglot or polyglot publications (two or more languages).
* **PARATEXT** – a copy of the FRT (front matter) book from your Paratext project.

See the control notes below for details of each.

**Warning:** **OK** **replaces** all of the current front matter. Your earlier changes are
lost. If you have worked on your front matter, click **Cancel**.

After **OK**, PTXprint also finds any new variables (`\zvar|...\*` codes) in the new front
matter and adds them to the variables table on the **Peripherals** tab.

## 15.6 The front matter and its special codes (advanced)

The front matter uses USFM markers, as in Paratext (for example `\mt1` for a main title and
`\pc` for a centred paragraph). PTXprint also understands extra codes that start with `\z`,
often called **z-codes**. Hold the mouse over the information button for a short list.

Each configuration has its own front matter. If you make a new configuration, check its
front matter too.

### Sections (periph)

The front matter is divided into sections. Each section starts with a line such as:

    \periph Title Page|id="title"

Each section normally starts on a new page.

If you used the **Cover Wizard** (on the **Peripherals** tab), the cover sections are at the end
of the front matter, after the line `\rem ============= Cover Page Settings =============`. The
wizard replaces these sections each time you click **Finish**. If you change them here, the
wizard asks to delete the old cover settings the next time you open it.

### Text from other settings

* `\zcopyright` – the copyright statement from the **Basic** tab.
* `\zlicense` – the licence statement from the **Basic** tab. (Type it with an **s**.)
* `\zimagecopyrights` – a list of the pictures used, with their pages and copyright credits.
  Add a language code at the end for another language, for example `\zimagecopyrightsfr`
  for French. The list is only correct after you print **twice**, because PTXprint first needs
  to find the page of each picture.

Put these codes after a paragraph marker, for example: `\pc \zcopyright`

### Variables

`\zvar|maintitle\*` is a **variable**: a place-holder for a piece of text. When you print,
PTXprint replaces it with the value from the variables table on the **Peripherals** tab. You
can make up your own names, for example `\zvar|printedby\*`. The values are saved with the
configuration, so two configurations can use the same front matter with different titles.

`\zvar|toctitle\*` is special. It uses the text in the **Table of contents title** box on the
**Peripherals** tab.

### Space and blank lines

* `\zbl|3\*` – inserts 3 blank lines.
* `\zgap|1.5in\*` – inserts a space of the given height (for example `1.5in`, `20mm`, `30pt`).

### Page numbers

* `\nopagenums` – do not print page numbers from here on.
* `\dopagenums` – print page numbers again.
* `\resetpagenums -1` – start the page numbers again. A negative number gives Roman
  numerals (i, ii, iii...).

### Table of contents

`\ztoc|main\*` puts the table of contents here. Instead of `main` you can use:
`pre` (books before the Scripture text), `ot` (Old Testament only), `heb` (Old Testament in
Hebrew order), `dc` (Deuterocanon only), `nt` (New Testament only), `post` (books after
Revelation, such as a glossary), or `sorta`, `sortb`, `sortc` (alphabetical lists sorted by
`\toc1`, `\toc2` or `\toc3`). Also tick **Table of Contents** on the **Peripherals** tab.

### Code Snippets buttons

On the **Front Matter** sub-tab, the buttons under **Code Snippets** list ready-made codes in
groups (for example **Periph+Var**, **Insert**, **ISBN+QR**, **Contents**, **Pages**,
**Diglot**). Put the cursor where you want the code, click a group button, then choose an item.
Hold the mouse over an item to see what it does. The **Settings** sub-tabs have their own
snippet buttons for the type of file that is open.

### Keyboard shortcuts in the front matter editor

* Ctrl+0 or Ctrl+comma – turn the current line into a comment (`\rem`), or back again.
* Ctrl+D – copy (duplicate) the current line.
* Ctrl+L – delete the current line.
* Ctrl+Up / Ctrl+Down – move the current line up or down.
* Ctrl+minus / Ctrl+equals – make the text in the editor smaller or larger.
* Alt+X – show the Unicode values of the selected characters in the status bar.

## 15.7 The Adj List (adjustment list)

Sometimes a page ends badly: for example, one line of a paragraph is alone at the top of the
next page, or the two columns do not end at the same height. You can often fix this by asking
PTXprint to set one paragraph a little tighter (one line less) or looser (one line more).

The **Adj List** is the list of these requests. Each row is one paragraph. The columns are:

* **Book** and **C.V** – the book, chapter and verse where the paragraph is.
* **Para** – which paragraph: 1 is the paragraph that contains the verse, 2 is the next one,
  and so on. This lets you adjust, for example, the paragraph after a heading.
* **Stretch** – the change. `+1` asks for one line more, `-1` for one line less. After
  **Generate**, you also see values such as `+0`, `-0` or `+-0`. These mean "no change
  yet", and show whether the paragraph *can* grow (+) or shrink (-).
* **Marker** – the paragraph marker (for example `p` or `q1`).
* **Expand** – how much the letters are spread out or squeezed, in percent. 100 is normal.
* **Parameters** and **Comment** – extra information.

Click a cell to change its value. To delete rows, select them and press the Delete key, or
right-click and choose **Delete Row(s)**.

For a diglot, the book code has an L or R after it (for example `MATL` and `MATR`) to show
the side.

**Generate** on the **Adj List** sub-tab prints the books three times in the background (normal,
tight, loose) to learn which paragraphs can shrink or grow. This can take some time. If an
Adj List already exists, PTXprint asks whether to replace it (**Yes**), merge the new
information into it (**No** – the safe choice), or do nothing (**Cancel**).

It is usually easier to adjust from the **PDF Preview** window: right-click a paragraph and
choose to shrink or expand it. PTXprint writes those changes into this same Adj List.

**Do paragraph adjustments last.** Any change to fonts, margins, pictures or other layout
settings moves the text, and your adjustments may then be wrong.

## 15.8 Common tasks

### Create front matter for the first time

1. On the **Peripherals** tab, tick **Local Front Matter**. If there is no front matter
   yet, PTXprint makes a BASIC one for you.
2. On the **View+Edit** tab, click the **Front Matter** sub-tab.
3. For a different template, click **Generate**, choose **BASIC**, **ADVANCED**,
   **DIGLOT** or **PARATEXT**, and click **OK**.
4. Click **Edit Variables...** and type the values (title, subtitle and so on) in the
   **Value** column.
5. Click **Print**. If the front matter has a table of contents or picture credits, click
   **Print** again.

### Change the text on the title page

1. On the **View+Edit** tab, click the **Front Matter** sub-tab.
2. If the line says `\mt1 \zvar|maintitle\*`, the title comes from a variable. Click
   **Edit Variables...** and change the value of **maintitle**.
3. If the line contains normal text, change the text directly in the editor.
4. Click outside the text area to save, then click **Print**.

### Add a copyright page with picture credits

1. Open the **Front Matter** sub-tab.
2. Put the cursor where the copyright information should go.
3. Type these lines (or use the **Insert** snippet button):

        \pc \zcopyright
        \pc \zlicense
        \pc \zimagecopyrights

4. Click **Print** twice.

### Make a paragraph one line shorter or longer

1. Finish all other layout settings first.
2. Easiest: in the **PDF Preview** window, right-click the paragraph to shrink or expand it.
3. Or: on the **Adj List** sub-tab, choose the **Book in Focus**, find the paragraph and type
   `-1` or `+1` in the **Stretch** column.
4. Click **Print** and check the result.

### See what text PTXprint actually typeset

1. Click **Print** once, so the file exists.
2. On the **View+Edit** tab, click the **Final SFM** sub-tab.
3. Choose the book in **Book in Focus**.
4. Read the text. Do not edit it – make corrections in Paratext.

### Look at the log after a failed print

1. Click the **XeTeX Log** sub-tab.
2. Scroll to the end. Error messages usually start with `!`.
3. If the log is cut short, click **View Only...** to open the whole file.

## 15.9 Common problems

**My changes to the front matter disappeared.**
You probably clicked **Generate** and then **OK**, which replaces the whole front matter. Or you
clicked **Refresh**, or answered "No" to "Save changes?". There is no undo. Keep a copy of
important text before you generate a new template.

**The front matter does not appear in the PDF.**
Tick **Local Front Matter** on the **Peripherals** tab.

**A variable prints as "<Type Value Here>".**
The variable has no value yet. Type one in the variables table on the **Peripherals** tab.

**The licence statement does not print.**
Check that the code is spelled `\zlicense` (with an **s**).

**The table of contents or the picture credits are empty or wrong.**
PTXprint needs a first print run to find the page numbers. Click **Print** again.

**The View+Edit tab is missing.**
You are using the **Basic** or **Mini** view. Change the view level to **Regular** or
**Full** in the main menu.

**The Generate button is greyed out.**
It does not work on the **.tex file**, **XeTeX Log** and **Settings** sub-tabs. On the
**Front Matter** sub-tab, it is also greyed out when the configuration is locked.

**"The Book in focus is not within scope".**
You clicked **Generate** on the **Adj List** sub-tab, but the **Book in Focus** is not in the
list of books to print. Choose a book that you are printing, or add the book on the
**Basic** tab.

**Paragraph adjustments no longer do what I expected.**
The layout has changed since you made them (for example a new font size or new pictures).
Check the adjustments again, or generate a new Adj List.

## 15.10 Settings reference

### Generate Front Matter (dialog)

#### OK

Button · Regular+ · `btn_gnr8frt_ok`

Replaces the current front matter with the chosen template. Everything you typed before is lost.

#### Cancel

Button · Regular+ · `btn_gnr8frt_cancel`

Closes the dialog and keeps your front matter. Click this if you are not sure.

#### Generate Front Matter

##### BASIC: Front matter contains just a few essentials with publication information

Radio · Regular+ · `r_generateFRT_basic`  
Also: Generate front matter: BASIC (just the essentials)

> This option will create a simple verso page containing essential copyright and licensing information followed by a table of contents.

Contains a title page, a publication data page (copyright, licence and picture credits) and a
table of contents. The titles come from variables such as **maintitle** and **subtitle**, so
you only need to fill in the variables table on the **Peripherals** tab. A good choice for
most first-time users.

##### ADVANCED: template contains several sections (some of which require editing before use)

Radio · Regular+ · `r_generateFRT_advanced`  
Also: Generate front matter: ADVANCED (requires editing)

> This option will create an extensive template with multiple sections (each of which will start on a new page in the final publication). You will need to edit the sample text provided so that it communicates in the required language(s). You can also remove unwanted sections if they are inappropriate for this publication. Note: In order to make this template generic for several different publications in this project, you are encouraged to use \zvar|variables\*  which will be replaced with publication-specific info when printed. For example:  
> \mt1 \zvar|maintitle\*  
> \mt2 \zvar|subtitle\*  
> \pc \zvar|maintitlefr\*  
> \pc \zvar|subtitlefr\*  
> \pc \zvar|languagename\*  
> \pc \zvar|copiesprinted\*

Contains title page, publication data, foreword, preface, table of contents and an
alphabetical contents list. The foreword and preface have sample English text to replace or
delete. It uses more variables (for example **languagename**, **copiesprinted**,
**printedby**), which you fill in on the **Peripherals** tab.

##### Include sections for a separate cover page

Checkbox, on · Regular+ · `c_includeCoverSections` · cfg `project/inclcoverperiphs`  
Also: Generate front matter: Include sections for cover page

> (Not yet implemented) Enable this option if you want to include the following sections (used for creating a cover page):  
> \periph Cover - detailing text and optional picture  
> \periph Spine - text for the spine of the cover

Does nothing yet, ticked or not. To make a cover, use **Create Cover Page** and the
**Cover Wizard...** on the **Peripherals** tab.

##### DIGLOT: template for a Diglot or Polyglot publication (deliberately fuller — delete sections you do not need)

Radio · Regular+ · `r_generateFRT_diglot`  
Also: Generate front matter: DIGLOT (for Diglot/Polyglot publications)

> This option creates a DIGLOT / POLYGLOT front matter template designed for publications with two (or more) languages or scripts. It is deliberately more complete than the BASIC and ADVANCED templates because diglots are inherently complex: two (or more) texts, often two contents lists, two prefaces, sometimes two scripts and two writing directions. Delete the sections you do not need.
>
> Like the ADVANCED template it uses \zvar|variables\* and  
> \zglot|L\* / \zglot|R\* markers for column-specific content, so it requires editing before use and is NOT suitable for use inside Paratext without prior modification.
>
> If this option is disabled, the Diglot setting is not enabled for this configuration.

Has sections for both languages (for example two prefaces taken from each side's INT book)
and also cover sections. Expect to delete several sections.

##### PARATEXT: Make a copy of the Project's FRT book (which may be edited to make use of \zvar|variables\*)

Radio · Regular+ · `r_generateFRT_paratext`  
Also: Generate front matter: PARATEXT (make a local copy)

> This option will create a COPY of the Paratext project's FRT book to be used exclusively by PTXprint. You can edit the front matter to make use of PTXprint-specific  
> \zvar|variables\* but note that none of these edits will be reflected in Paratext. In addition, if you edit the FRT book in Paratext, those changes will not be reflected here until you regenerate this (local) Front Matter.
>
> If option is disabled, it is due to not having a FRT book in the Paratext project (so there is nothing to import).

After the copy, the two are separate: edits in Paratext do not appear here, and edits here do
not go back to Paratext. Generate again to get the new Paratext version. Use this if your team
already keeps good front matter in Paratext.

### View+Edit

#### Refresh

Button · Regular+ · `btn_refreshViewerText`  
Also: Reload current file in view from saved version

> Discard any changes that have been made and restore the contents of this file as it was when last saved.
>
> Shortcut: F5

Use it to throw away unsaved changes, or after you changed the file in an outside editor.
Greyed out on the look-only sub-tabs.

#### Book in Focus – Book in focus for editor (or viewer)

Drop-down · Regular+ · `ecb_examineBook`  
Choices: NONE

> Choose any book (including those which are not currently in the list to be printed.)

Active only on the **Adj List** and **Final SFM** sub-tabs. Always greyed out when printing a
module instead of books.

#### Generate

Button · Regular+ · `btn_Generate`  
Also: Generate ... (context sensitive)

> This button will (re-)generate content for Front Matter, AdjList(s) and Final SFM.
>
> If you only want to (re-)generate an Adj List for a single book, then just select that book on the Basic tab. Otherwise it will (re-)generate a Pic/Adj list for each of the books listed for printing.
>
> Shortcut: Ctrl-G

Opens the **Generate Front Matter** dialog on **Front Matter**, makes a new adjustment list on
**Adj List**, or a fresh Final SFM file for the **Book in Focus** on **Final SFM**. An Adj List
takes three background print runs, so it can be slow for large books.

#### View/Edit...

Button · Regular+ · `btn_viewEdit`  
Also: View (or edit) file in external editor

> You may view (and in some cases edit) the file in your system's text Editor.
>
> Warning: If you edit settings in an external editor, be careful to save them (externally) and then click the refresh button (within PTXprint) before you hit Print. Otherwise you could lose changes that were made.
>
> If nothing happens when you click here, it is probably because you have not associated the file type (.sfm, .piclist, .adjlist, .tex, .log, .sty etc.) with a text editor (such as Notepad or NP++).
>
> Note that any changes to the Final SFM text get overwritten each time you hit Print. So any changes to the text or markers need to be made in Paratext.
>
> Shortcut: Ctrl-E

Easier for long files or for searching. If you change a file there, save it in that editor,
then click **Refresh** in PTXprint before you print. Otherwise PTXprint may save its own older
copy over your changes.

#### Edit Variables...

Button · Regular+ · `btn_editZvars`  
Also: Edit peripheral variables

> If you have used \zvar_variable names in the front matter template, these may be edited on the "Pub. Info" tab. Click this button to show that tab.

Before it switches tabs, it saves the front matter and adds any new `\zvar` names to the
table, so you can type their values. Only shown on the **Front Matter** sub-tab.

#### Use the following codes to include special text in front mat...

Button · Regular+ · `btn_infoViewEdit`

> Use the following codes to include special text in front matter:
>
>   \nopagenums - turn OFF page numbers  
>   \dopagenums - turn ON page number  
>   \resetpagenums # - where # is the page number (setting # to -1 gives roman numerals i,ii,iii,iv,v,...)
>
>   \pc \zcopyright - copyright statement from the Basic tab  
>   \pc \zlicense - license statement from the Basic tab  
>   \pc \zimagecopyrights - generated list of images with copyright attribution  
>   \pc \zimagecopyrightsfr - as above, but localized (fr = French)
>
>   \zbl|3\* - inserts 3 blank lines  
>   \zgap|1.5in\*
>
> To include one or more table of contents:  
>   \ztoc|\* Where  can be replaced with:  
>   main – primary, all-inclusive table of contents  
>   pre – any book prior to scripture (FRT, INT)  
>   ot – only Old Testament books are listed  
>   heb - OT books sorted according to the Hebrew TaNaKh  
>   dc – only Deutero Canonical books are listed  
>   nt – only New Testament books are listed  
>   post – books that occur after REV (GLO, BAK, TDX, NDX, XXA-G)  
>   sorta – alphabetical (main) list sorted by \toc1  
>   sortb – alphabetical (main) list sorted by \toc2  
>   sortc – alphabetical (main) list sorted by \toc3
>
> In addition to the above-mentioned codes, you may specify your own config-specific \zvar|variables\* as place-holders. Click on 'Edit Variables...' to assign values to these variables on the Peripherals tab. For example:  
>   \mt1 \zvar|maintitle\*  
>   \mt2 \zvar|subtitle\*

Only active on the **Front Matter** sub-tab. See "The front matter and its special codes"
in this chapter for a fuller explanation.

#### Autosave

Checkbox, on · Regular+ · `c_autoSave` · cfg `config/autosave`

> Save any changes made below without a confirmation check.

When not ticked, PTXprint asks "Save changes?" when you click outside the text area. Untick it
if you often experiment and want to be asked. Greyed out on the look-only sub-tabs and when
the configuration is locked.

#### Book in Focus – Adjust display font size

Slider · Regular+ · `s_viewEditFontSize` · cfg `config/displayfontsize`  
Values: 8–20 (default 12)

> Use this slider to adjust the size of the text on the View+Edit tab as well as in other locations that use a specialized font or script.
>
> Keyboard Shortcuts:  
>   Ctrl-Minus - shrink text size  
>   Ctrl-Plus - grow text size

Affects only the screen (the editor and some other boxes that use the project font), not the PDF.

#### Adj List

Label · Regular+ · `l_AdjList`

> To balance columns of text on a page it is possible to specify paragraphs adjustments (shrink or expand):
>
> A Paragraph Adjust List needs to be in this format:  
> MRK 2.7 +1    (i.e. expand the para at Mark 2.7 by one line) MRK 3.20 -1   (i.e. shrink the para at Mark 3:20 by one line) %MARK 4.14 +1   (ignore this line - treat it as a comment) MRK 5.8 +2    (i.e. expand the para at Mark 5.8 by two lines) MRK 6.23 +1[2]  (expand the paragraph AFTER the paragraph  
>                               which contains MRK 6.23 e.g. a heading.)
>
> Diglot AdjList also need R or L to be specified after the book code and it is important that L comes before R for the same verse. MATL 3.4 +1 MATR 3.4 -1 MATR 3.11 +2
>
> Keyboard Shortcuts:  
>   Ctrl-1 - makes the current line +1  
>   Ctrl-2 - makes the 2nd para of current line +1[2]  
>     ... etc ...  
>   Ctrl-9 - makes the 9th para of current line +1[9]
>
>   Ctrl-I - shrink current line -1  
>   Ctrl-Grave - ` same as above
>
>   Ctrl-0 - % Comment (or uncomment) the line [it toggles]  
>   Ctrl-Comma - same as above
>
>   Ctrl-D - Duplicate the current line  
>   Ctlr-L - deLete the current line  
>   Ctrl-Up - move the current line up one line  
>   Ctrl-Down - move the current line down one line
>
> Note that adjusting paragraphs needs to be done right at the end when all other settings have been finalized. Otherwise you are likely to have to re-do it all again.

The table shows one row per paragraph for the **Book in Focus**. Type `+1` or `-1` in the
**Stretch** column. See "The Adj List (adjustment list)" in this chapter for the columns.

#### Code Snippets

Label · Regular+ · `l_codeSnippets`

> Use the buttons below to insert various code snippets as required.

The buttons appear on the **Front Matter** and **Settings** sub-tabs. Each opens a menu of
ready-made codes; choose one to insert it at the cursor.

#### More...

Link · Regular+ · `lb_snippets`  
Also: Link to deeper technical help

> Online documentation on a structured list of code snippets which can be copied and pasted into the appropriate settings files.

Mostly for advanced users who work with the settings files on the **Advanced** tab.


# 16. Peripherals tab (front and back matter)

## 16.1 What this tab is for

The **Peripherals** tab controls everything printed **around** the Scripture text:

* the **front matter** – the pages before the Scripture text, such as the title page, the
  copyright page and the table of contents;
* the **back matter** – pages after the Scripture text, such as maps and the colophon;
* a **cover** for the book;
* ready-made PDF files to add at the front or at the back.

The words on the front matter pages are edited on the **View+Edit** tab. The special codes you
can use there (`\zcopyright`, `\ztoc`, `\zvar` and others) are explained in the **View+Edit**
tab chapter. This chapter explains the settings that turn these parts on and off, and the
table of **variables** (values that PTXprint puts into the front matter, such as the main title).

**View levels:** In the **Basic** view this tab shows only **Table of Contents**, **Local
Front Matter** and the variables table. Everything else needs the **Regular** or **Full**
view. When one of the main options on this tab is on, the tab name is shown in a different
colour.

## 16.2 Cover

PTXprint can make a cover: a back cover, a spine (the narrow back edge of a bound book) and a
front cover, all on one wide page (the "cover spread"). The cover is saved in its **own PDF
file**, with the name of the main PDF plus **_cover**. Printers usually print the cover on
different paper, so they want a separate file.

* Tick **Create Cover Page** to make a cover each time you print.
* Click **Cover Wizard...** to design the cover step by step (see below).
* The links **Back Cover**, **Spine**, **Front Cover** and **Cover Spread** open the matching
  style on the **Styles** tab. Each part of the cover is a sidebar (a box) with a background
  colour, background picture, border and other box settings. Use **Cover Spread** for things
  that go across the whole cover, for example one picture behind the back, spine and front.

The text on each part comes from special front matter sections (`coverfront`, `coverspine`,
`coverback`, and `coverwhole` for the whole spread). So the cover needs **Local Front Matter**.
If you untick **Local Front Matter**, PTXprint also unticks **Create Cover Page** and shows a
message. If the front matter has no cover sections, no cover is made. The easiest way to create
them is the **Cover Wizard**.

There is no separate Cover tab in this version. Use the **Cover Wizard** and the four style
links.

### The Cover Wizard

The wizard window shows the steps on the left and a preview of the whole cover on the right.
Use **Next** and **Back** to move between the steps.

If the configuration already has cover settings that the wizard did not make, or that were
changed by hand afterwards, PTXprint first shows **Existing cover settings found**. The wizard
cannot build on these. **Delete and Continue** deletes the old cover styles and sections and
starts a new cover. **Cancel (keep my settings)** keeps them; the wizard does not open.

1. **Book and Spine Setup** – type the approximate number of pages (PTXprint fills this in
   from the last PDF if it can). Choose whether the book has a spine (most books with fewer
   than about 80 pages have no spine text). If it has a spine, choose **Paperback** or
   **Hardcover**, and how to find the spine width: **Automatic** (from the paper weight in gsm
   or the paper thickness in µm) or **Manual** (type the width in mm). Ask your printer for the
   paper thickness if you can. Tick the right-to-left binding option for scripts such as
   Arabic or Hebrew, whose books open on the other side.
2. **Picture / decoration** – choose where the main picture goes (none, whole cover, front
   only, front and spine, back only, back and spine, or separate front and back pictures).
   Choose the file, how it fits (stretch or crop), and its opacity. You can also add a
   decorative border to the front cover.
3. **Background** – white, or a solid colour behind everything. (Gradient shading is not
   available yet.)
4. **Front cover text** – type the title (required before you can go on). You can also add a
   subtitle, the language name and a picture. Each item has a position slider (higher or lower),
   a colour and a size.
5. **Spine text** (only when the book has a spine) – choose what to show (title, subtitle,
   language name), its colour, size, direction and position. (The publisher name on the spine
   is not available yet.)
6. **Back cover** – add a short text (a "blurb"), an ISBN barcode and a logo, and choose
   where they go.
7. **Review** – check the summary and the preview, then click **Finish**.

When you click **Finish**, PTXprint:

* ticks **Local Front Matter** if needed (the cover sections are kept in the front matter);
* writes new cover sections at the end of the front matter, after the line
  `\rem ============= Cover Page Settings =============`. This **replaces** any earlier cover
  sections;
* changes the cover styles (background, border, picture, title colours and sizes);
* puts the title, subtitle, language name and ISBN into the variables **maintitle**,
  **subtitle**, **languagename** and **isbn** in the variables table on this tab;
* saves your wizard answers with the configuration, so you can open the wizard later and make
  changes.

**Cancel** (or closing the window) changes nothing, and your answers go back to what they
were when you opened the wizard.

If the publication is printed from the **Publications** tab, PTXprint works out the spine
width from the page count of each publication (see the **Publications** tab chapter).

## 16.3 Front Matter PDF(s) and Back Matter PDF(s)

Use these when part of the book already exists as a PDF file, for example a title page made in
another program, or maps or an index made elsewhere.

* Tick **Front Matter PDF(s)** and click **Select...** to choose PDF files that go **before**
  the Scripture text.
* Tick **Back Matter PDF(s)** and click **Select...** to choose PDF files that go **after** it.

The chosen file names are shown next to the button. Hold the mouse over **Select...** to see
the full paths. Several files are added in the alphabetical order of their file names (not the
order you clicked them). For a different order, name the files for example `01-title.pdf`,
`02-preface.pdf`. The PDF pages must have the same page size as your publication.

## 16.4 Table of Contents

Tick **Table of Contents** to make a list of the books with their page numbers. It is useful
when you print several books.

* **Title** – the heading, for example "Contents" in your language.
* **Use \toc1 / \toc2 / \toc3** – each book in Paratext has up to three names: `\toc1` (long
  name), `\toc2` (short name) and `\toc3` (abbreviation). Each ticked name becomes one column.
  At least one must be ticked.
* **Leaders** – dots or a line between the book name and the page number.

Where does it appear?

* Without **Local Front Matter**, PTXprint makes its own contents page with your title before
  the Scripture text.
* With **Local Front Matter**, it appears where the front matter has `\ztoc|main\*` (see the
  **View+Edit** tab chapter). The BASIC front matter template already has this code.

The page numbers are only known after typesetting, so PTXprint typesets more than once when you
click **Print**. With **Quick Run** ticked it typesets only once; the status line then says
"Rerun to fix: table of contents", and you must click **Print** again.

## 16.5 Local Front Matter

PTXprint does not print your Paratext project's FRT (front matter) book directly. It keeps its
own copy for each configuration, which you change on the **View+Edit** tab. Tick **Local Front
Matter** to print it. The first time, PTXprint makes a simple front matter (title page,
copyright page and table of contents) if there is none yet.

* **Edit...** opens the **Front Matter** sub-tab of the **View+Edit** tab.
* **Force Page Break at each Periph** – each front matter section (title page, copyright page,
  preface …) starts on a new page.
* **Suppress Blank Page Before Scripture Text** – stops the blank page PTXprint adds so that
  the Scripture text starts on a right-hand page.
* **Use Peripheral Introductory Sections** – see below.

**Note:** Ticking **Local Front Matter** unticks **Colophon at End of Publication**, because
most front matter already has a copyright page. Unticking it ticks the colophon again (and
turns off the cover). Only your own click on **Local Front Matter** does this; opening a
configuration or PTXprint updating the front matter does not change the colophon. Check both
settings after you click one of them.

### Use Peripheral Introductory Sections

Some projects have an INT (introductions) book in Paratext, with sections such as an
introduction to the Old Testament or to the Gospels. Each section starts with a `\periph`
line that has an id. Tick **Use Peripheral Introductory Sections** to put each section in
front of the first book of its group. The ids that PTXprint knows are:

| id | Placed before |
|---|---|
| `intbible` | the first book of the Bible |
| `intot` | the first Old Testament book |
| `intpent` | the first book of the Pentateuch (GEN–DEU) |
| `inthistory` | the first history book (JOS–EST) |
| `intpoetry` | the first poetry book (JOB–SNG) |
| `intprophesy` | the first book of the prophets (ISA–MAL) |
| `intdc` | the first Deuterocanon book |
| `intnt` | the first New Testament book |
| `intgospels` | the first Gospel (MAT–JHN) |
| `intepistles` | the first letter of Paul (ROM–PHM) |
| `intletters` | the first of the other letters (HEB–REV) |

A section is only printed when a book of its group is in the list of books to print.
**Force Page Break at each Periph** also decides whether these sections start on a new page.

## 16.6 Maps

* **Add Maps...** opens the **Add Map** dialog (explained in the **Pictures** tab chapter).
* **Include Maps** adds the map book to the list of books to print.
* **Edit...** shows the map book on the **View+Edit** tab.

## 16.7 Colophon at End of Publication

A colophon is a short text at the very end of the book, for example the copyright, the
licence and the picture credits. Tick **Colophon at End of Publication** to show the text box.
The colophon is printed after the end of the last book.

* Type the colophon in the **Colophon Text** box. You can use USFM markers such as `\pc`
  (centred paragraph) and the codes `\zcopyright`, `\zlicense` and `\zimagecopyrights` (see
  the **View+Edit** tab chapter).
* The reset button below the box puts back the standard colophon.
* **Force Page Break Before Colophon** puts the colophon on a new page.

The picture credits (`\zimagecopyrights`) need the page numbers of the pictures. Click
**Print** a second time to get them right.

## 16.8 Variables and Values

This table lists the **variables** used in the front matter (and in the colophon and cover).
A variable is a place-holder such as `\zvar|maintitle\*`. When you print, PTXprint puts the
value from this table in its place. The values are saved with the configuration, so two
configurations can use the same kind of front matter with different titles.

The table has three columns:

* **Pub** (only in the **Full** view) – makes the variable a field of each publication on the
  **Publications** tab, so each publication can have its own value (for example its own
  title). **maintitle** and **subtitle** are always used there.
* **Name** – the name of the variable. You cannot change it here.
* **Value** – click to change it. Press Enter to keep the new value.

Buttons:

* **Rescan peripheral variables** adds any `\zvar|...\*` codes in the front matter that are
  missing from the table.
* **Add** adds a new variable.
* **Del** deletes the selected variables.

The variable `toctitle` is special: it always uses the **Title** of the **Table of Contents**,
so it is not in this table.

## 16.9 Common tasks

### Add a title page and a copyright page

1. On the **Basic** tab, check the copyright and licence statements.
2. On the **Peripherals** tab, tick **Local Front Matter**. PTXprint makes a simple front
   matter if there is none.
3. In the **Variables and Values** table, click the value of **maintitle** and type the
   title. Do the same for **subtitle** and any other variables.
4. Click **Print**.

To change the layout of these pages, click **Edit...** (see the **View+Edit** tab chapter).

### Add a table of contents

1. On the **Basic** tab, choose **Multiple Books** and the books to print.
2. On the **Peripherals** tab, tick **Table of Contents**.
3. Type the **Title**, for example "Contents" in your language.
4. Tick the book names to use (**\toc1**, **\toc2**, **\toc3**) and choose the **Leaders**.
5. If **Local Front Matter** is ticked, check that the front matter contains
   `\ztoc|main\*` (the BASIC template has it).
6. Click **Print**. If the status line asks you to rerun, click **Print** again.

### Make a cover

1. Tick **Local Front Matter** (a cover needs it).
2. Tick **Create Cover Page**.
3. Click **Cover Wizard...**, go through the steps and click **Finish**.
4. Click **Print**. The cover is saved as a separate PDF whose name ends with **_cover**.
5. To fine-tune colours, borders or pictures, click **Front Cover**, **Spine**, **Back Cover**
   or **Cover Spread** and change the style on the **Styles** tab.

### Add an existing PDF before or after the Scripture text

1. Tick **Front Matter PDF(s)** (or **Back Matter PDF(s)**).
2. Click **Select...** and choose one or more PDF files.
3. Click **Print**.

### Put the copyright and picture credits at the end of the book

1. Tick **Colophon at End of Publication**.
2. If the box is empty, click the reset button under the box to get the standard text.
3. Tick **Force Page Break Before Colophon** if you want it on its own page.
4. Click **Print** twice, so that the picture credits are correct.

### Add your own variable

1. Click **Add**, type a name such as `printedby`, and click **OK**.
2. Click the **Value** of the new row and type the text.
3. On the **View+Edit** tab, put `\zvar|printedby\*` in the front matter where the text
   should appear.

### Insert book group introductions from the INT book

1. In Paratext, give each section of the INT book an id, for example
   `\periph New Testament Introduction|id="intnt"`.
2. On the **Peripherals** tab, tick **Use Peripheral Introductory Sections**.
3. Print a set of books that includes a book of that group (for example MAT for `intnt`).

## 16.10 Common problems

**The cover is not created.**
Check that **Local Front Matter** and **Create Cover Page** are both ticked. The front matter
must contain cover sections: run the **Cover Wizard** and click **Finish** to create them.
The cover is in a **separate** PDF file (name ending in **_cover**), not in the main PDF.

**Create Cover Page became unticked by itself.**
You unticked **Local Front Matter**. A cover cannot be made without it. Tick both again.

**The Cover Wizard button is greyed out.**
Tick **Create Cover Page** first.

**The Finish button in the Cover Wizard is greyed out.**
You must type a title in the front cover step, and be on the last (review) step.

**My hand-made changes to the cover text disappeared.**
**Finish** in the Cover Wizard replaces the cover sections of the front matter. Make the
changes again on the **View+Edit** tab after you use the wizard.

**"Existing cover settings found" when I open the Cover Wizard.**
The configuration has cover styles or sections that the wizard did not make, or that were
changed afterwards. To use the wizard, PTXprint must delete them. Click **Cancel (keep my
settings)** to keep your cover and change it by hand.

**The colophon disappeared after I turned on Local Front Matter.**
Ticking **Local Front Matter** unticks the colophon. Tick the colophon again if you want both.
It is not unticked again unless you click **Local Front Matter** again.

**The table of contents is empty or the page numbers are wrong.**
Click **Print** again (especially if **Quick Run** is ticked). If **Local Front Matter** is
ticked, the front matter must contain `\ztoc|main\*`. Check that at least one of
**\toc1**/**\toc2**/**\toc3** is ticked and that the books have those markers in Paratext.

**A book is missing from the table of contents.**
The book has no text for the ticked `\toc` markers. Add the `\toc1` (or `\toc2`, `\toc3`)
line to the book in Paratext, or tick another `\toc` option.

**The picture credits in the colophon or front matter are wrong or empty.**
Click **Print** a second time. PTXprint needs a first run to find the page of each picture.

**A variable prints as "<Type Value Here>".**
Click its **Value** in the **Variables and Values** table and type the text.

**A variable I deleted came back.**
**Rescan peripheral variables** (and generating front matter) adds every variable used in the
front matter. Remove the `\zvar` code from the front matter first, then delete the row.

**There is a blank page before the Scripture text.**
PTXprint starts the Scripture text on a right-hand page. Tick **Suppress Blank Page Before
Scripture Text** if you do not want this.

**The maps are printed although I do not want them.**
Untick **Include Maps**.

**Most of the settings on this tab are missing.**
You are using the **Basic** view. Change to the **Regular** or **Full** view.

## 16.11 Settings reference

### Peripherals

#### Create Cover Page

Checkbox, off · Regular+ · `c_makeCoverPage` · cfg `cover/makecoverpage`  
Also: Create an outer Cover · Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

> Create a cover (back, spine and front) as a separate PDF file ending in _cover.pdf. Needs Local Front Matter. Use the Cover Wizard... to design it.

The cover pages are taken out of the main PDF. The cover text is kept in cover sections of the
front matter, so unticking **Local Front Matter** unticks this too.

#### Cover Wizard...

Button · Regular+ · `btn_coverGenerate`  
Also: Generate Cover (Basic settings to create a cover) · Needs: “Create Cover Page” · Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

> Creating a cover from nothing takes a lot of effort. This tool enables you to create various kinds of covers which can easily be enhanced.

Leads you through 6 or 7 steps (page count and spine, pictures, background, front text, spine
text, back cover, review) with a live preview. **Finish** writes the cover sections into the
front matter (replacing earlier ones), sets the cover styles, ticks **Local Front Matter** if
needed, and fills in the **maintitle**, **subtitle**, **languagename** and **isbn**
variables. PTXprint asks before it deletes an older cover that the wizard did not make (or
that was changed by hand). **Cancel** keeps everything as it was.

#### Back Cover

Link · Regular+ · `lb_style_cat:coverback|esb`  
Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

> Click to edit the Sidebar properties on the Styles tab for the Back Cover.

Change the background colour, background picture, border or padding there. The back cover
text is in the `coverback` section of the front matter.

#### Spine

Link · Regular+ · `lb_style_cat:coverspine|esb`  
Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

> Click to edit the Sidebar properties on the Styles tab for the Spine.

Change background, border and text direction there. The spine text is in the `coverspine`
section of the front matter.

#### Front Cover

Link · Regular+ · `lb_style_cat:coverfront|esb`  
Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

> Click to edit the Sidebar properties on the Styles tab for the Front Cover.

Change the front background colour or picture, or the border, there. The front cover text is
in the `coverfront` section of the front matter.

#### Cover Spread

Link · Regular+ · `lb_style_cat:coverwhole|esb`  
Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

> Click to edit the Sidebar properties on the Styles tab for the whole Cover Spread (the background behind the back, spine and front).

The bottom layer: the back, spine and front boxes are placed on top of it. Use it for a
background colour or one picture across the whole cover.

#### Front Matter PDF(s)

Checkbox, off · Regular+ · `c_inclFrontMatter` · cfg `project/ifinclfrontpdf`  
Also: Enable import of front matter PDF(s) · Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

> One or more previously created PDF file(s) can be included BEFORE the scripture material being typeset. If more than one file is selected, then these will appear in alphabetical order.
>
> If you are creating an electronic publication and want to add a fancy (colour) cover, then consider designing a cover using the online Canva.com tool.

The pages go before the local front matter too. Use it for pages made in another program. The
pages should have the same page size as the publication.

#### Select...

Button · Regular+ · `btn_selectFrontPDFs` · cfg `project/frontincludes`  
Also: Select front matter PDF(s) to import · Needs: “Front Matter PDF(s)” · Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

Hold the Ctrl key to choose several files. The names are shown next to the button, and the
full paths when you hold the mouse over it. Several files are added in alphabetical order of
their file names. To change the list, click the button again and choose all the files you want.

#### Table of Contents   Title

Checkbox, off · Basic+ · `c_autoToC` · cfg `document/toc`  
Also: Enable table of contents · Shown when: “Table of Contents   Title”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Local Front Matter”, “Colophon at End of Publication”

> This will automatically generate the Table of Contents for all the books included in the publication using one or more of the \toc1, \toc2 and \toc3 fields as specified. The \toc1, \toc2 and \toc3 choices are only applied when "Multiple Books" is set on the Basic tab.
>
> NOTE: PTXprint typesets the text more than once to get the page numbers right, so printing takes longer. (With Quick Run on, click Print a second time.) If Local Front Matter is on, put \ztoc|main\* in the front matter where the ToC should appear.

Without **Local Front Matter**, PTXprint makes its own contents page with the **Title**. With
it, the table appears where the front matter has `\ztoc|main\*`. See "Table of Contents" in
this chapter.

#### Table of contents title

Text box · Basic+ · `t_tocTitle` · cfg `document/toctitle`  
Needs: “Table of Contents   Title” · Shown when: “Table of Contents   Title”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Local Front Matter”, “Colophon at End of Publication”

> The heading for the Table of Contents (for example 'Contents' in your language). It can also be used in the front matter as \zvar|toctitle\*

Write it in the language of the publication. PTXprint uses it on its own contents page.

#### Table of contents: Use \toc1

Checkbox, on · Regular+ · `c_usetoc1` · cfg `document/usetoc1`  
Needs: “Table of Contents   Title” · Shown when: “Table of Contents   Title”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Local Front Matter”, “Colophon at End of Publication”

> Select which of the \toc markers should be included in the generated Table of Contents.

Uses the long book names (`\toc1` in Paratext) as a column. If you untick all three `\toc`
options, PTXprint ticks this one again.

#### Table of contents: Use \toc2

Checkbox, off · Regular+ · `c_usetoc2` · cfg `document/usetoc2`  
Needs: “Table of Contents   Title” · Shown when: “Table of Contents   Title”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Local Front Matter”, “Colophon at End of Publication”

> Select which of the \toc markers should be included in the generated Table of Contents.

Uses the short book names (`\toc2`) as a column, instead of or as well as the long names.

#### Table of contents: Use \toc3

Checkbox, on · Regular+ · `c_usetoc3` · cfg `document/usetoc3`  
Needs: “Table of Contents   Title” · Shown when: “Table of Contents   Title”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Local Front Matter”, “Colophon at End of Publication”

> Select which of the \toc markers should be included in the generated Table of Contents.

Uses the book abbreviations (`\toc3`) as a column. Thumb tabs can also show the `\toc3` text;
when this is unticked, the thumb tab text must come from `\zthumbtab` instead.

#### Leaders – Style of leaders for table of contents

Drop-down · Regular+ · `fcb_leaderStyle` · cfg `document/tocleaders`  
Choices: None | ...................... | . . . . . . . . . . . . . | - - - - - - - - - | ________________ · Needs: “Table of Contents   Title” · Shown when: “Table of Contents   Title”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Local Front Matter”, “Colophon at End of Publication”

> Leaders display dots or a line between the text and the page number. Select the style of leader you wish to apply.

**None** leaves the space empty. Leaders help the reader follow the line across a wide page.

#### Use Peripheral Introductory Sections

Checkbox, off · Regular+ · `c_useSectIntros` · cfg `project/sectintros`  
Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

> Check this option if the INT book contains peripheral divisions (sub-sections) which need to be inserted at the appropriate position between books. For example:  
>   \periph Old Testament Introduction|id="intot"  
>   \periph New Testament Introduction|id="intnt"  
>   \periph Gospels Introduction|id="intgospels"

Uses `\periph` ids such as `intot`, `intnt` or `intgospels` (see the table in this chapter). A
section is only printed if a book of its group is printed. Leave it unticked if your project
has no INT book with such sections.

#### Local Front Matter

Checkbox, off · Basic+ · `c_frontmatter` · cfg `project/iffrontmatter`, `document/hasnofront_`  
Also: Enable (local) front matter · Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

> PTXprint does not directly typeset the FRT book from Paratext. Instead, it uses a "local" PTXprint-specific copy of Paratext's FRT book which can be enhanced by additional codes which are described on the View+Edit tab's Information button.
>
> Note: turning this on turns the Colophon off (you can turn it on again). A cover needs Local Front Matter.

Edited on the **View+Edit** tab. The first time, PTXprint creates a simple front matter if
there is none. Your click to tick it unticks **Colophon at End of Publication**; your click to
untick it ticks the colophon again and turns off **Create Cover Page**. The **Cover Wizard**
ticks this box when you click **Finish**.

#### Edit...

Button · Regular+ · `btn_editFrontMatter`  
Also: View (or edit) front matter · Needs: “Local Front Matter” · Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

Goes to the **Front Matter** sub-tab of the **View+Edit** tab.

#### Force Page Break at each Periph

Checkbox, on · Regular+ · `c_periphPageBreak` · cfg `project/periphpagebreak`  
Also: Front matter: Force page break at each periph section · Needs: “Local Front Matter” · Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

> This option is normally checked so that each different section of the front matter will begin on a new page.

Also applies to each introduction section from the INT book. Untick it only if you want short
sections, such as a copyright notice and a dedication, to share a page.

#### Suppress Blank Page Before Scripture Text

Checkbox, off · Regular+ · `c_periphSuppressPage` · cfg `document/noblankpage`  
Also: Front matter: Suppress blank page at start of scripture text · Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

> By default, the main body of scripture always starts on an odd (right-hand-side) page. PTXprint will automatically insert a pagebreak if needed to make this happen. If you wish to override this behavior, then check this option (to NOT insert a blank page after any front matter material).

Useful for PDFs that are read on screen.

#### Include Maps

Checkbox, off · Regular+ · `c_inclMaps` · cfg `project/inclmaps`  
Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

> Add the map book (usually XXM) to the list of books to print. Use Add Maps... to create the map pages.

Also switches the **Basic** tab to **Multiple Books**. Unticking it removes the map book from
the list. PTXprint saves the configuration each time you change this.

#### Add Maps...

Button · Regular+ · `btn_addMaps1`  
Also: Add Maps to the Publication · Needs: “Include Maps” · Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

> Maps for the end of the publication can be added to one of the XX* books or to the XXM book using this dialog.

Choose map pictures and their captions. PTXprint writes one page for each map into the map
book and adds the maps to the picture list. See the **Pictures** tab chapter for the dialog.

#### Edit...

Button · Regular+ · `btn_editMaps1`  
Also: Edit Maps module · Needs: “Include Maps” · Shown when: “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

> Switch to the View+Edit tab to show/edit the Maps module.

Nothing happens if the map book does not exist yet; use **Add Maps...** first.

#### Colophon at End of Publication

Checkbox, on · Regular+ · `c_colophon` · cfg `project/ifcolophon`  
Also: Enable colophon at end of publication · Shown when: “Colophon at End of Publication”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”

> What is a Colophon? A brief statement containing information about the publication such as the place of publication, the publisher, and the date of publication. This will be printed at the END of the book. Similar to a "biblio-page" or a "copyright-page" at the front of a book.
>
> NOTE: The picture credits (\zimagecopyrights) are only correct after you click Print a second time.

When you tick it and the text box is empty, PTXprint fills in the standard colophon. Ticking
**Local Front Matter** unticks it, so tick it again if you want both.

#### Back Matter PDF(s)

Checkbox, off · Regular+ · `c_inclBackMatter` · cfg `project/ifinclbackpdf`  
Also: Enable import of back matter PDF(s) · Shown when: “Back Matter PDF(s)”, “Front Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

> One or more previously created PDF file(s) can be included AFTER the scripture material being typeset. If more than one file is selected, then these will appear in alphabetical order.

For example a glossary, an index or maps made in another program. The pages should have the
same page size as the publication.

#### Select...

Button · Regular+ · `btn_selectBackPDFs` · cfg `project/backincludes`  
Also: Select back matter PDF(s) to import · Needs: “Back Matter PDF(s)” · Shown when: “Back Matter PDF(s)”, “Front Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication”

Hold the Ctrl key to choose several files. The names are shown next to the button. Several
files are added in alphabetical order of their file names.

#### Rescan peripheral variables

Button · Regular+ · `btn_rescanFRTvars`  
Shown when: “Local Front Matter”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Colophon at End of Publication”

> Clicking this button will rescan the Front Matter for any \zvar|variables\* and add any that are missing to this table of variable names and values.

Saves the front matter first. New variables get the value `<Type Value Here>` (and
**copiesprinted** gets 50). Existing values are not changed. Use it after you add variables
to the front matter by hand.

#### tv_zvarEdit

Table · Basic+ · `tv_zvarEdit`  
Shown when: “Local Front Matter”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Colophon at End of Publication”

Click a **Value** to change it; press Enter to keep it. Tick **Pub** (shown only in the
**Full** view) to give each publication on the **Publications** tab its own value. The
**Name** cannot be changed; to rename a variable, add a new one and delete the old one.

#### Variables and Values

Label · Basic+  
Shown when: “Local Front Matter”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Colophon at End of Publication”

> This table lists the standard set of \zvar|variables\* which can be used as part of front matter and/or colophon. As these \zvar|variables\* are customizable, you can add your own as needed. For example, you may need the \zvar|maintitle\* in more than one language so you can add 'fr' or 'es' to create a new one:  
>   \zvar|maintitlefr\* or you might want to add a custom variable such as:  
>    \zvar|printedby\*
>
> The values of these variables are saved with the config as they might vary from one publication to another.

#### Del

Button · Regular+ · `btn_delzvar`  
Also: Delete a peripheral variable · Shown when: “Local Front Matter”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Colophon at End of Publication”

> Delete the currently selected variable(s).

Select several rows with Ctrl or Shift. A variable that the front matter still uses comes back
at the next rescan.

#### Add

Button · Regular+ · `btn_addzvar`  
Also: Add a peripheral variable · Shown when: “Local Front Matter”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Colophon at End of Publication”

> Add a new variable.

Adds the variable with an empty value. Use only letters, numbers and hyphens (no spaces), for
example `printedby` or `maintitlefr`. Then type its value in the table, and use it in the front
matter as `\zvar|name\*`. Nothing is added if the name already exists.

#### Colophon at End of Publication

##### Colophon Text

Label · Regular+  
Needs: “Colophon at End of Publication” · Hidden until: “Colophon at End of Publication” · Shown when: “Colophon at End of Publication”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”

> Enter your Colophon text here - using standard USFM codes for formatting. You may want to use the reset button to start with a standard set.
>
> You can use the following codes to automatically include special text using the following markers:  
> \zcopyright   - copyright statement from the Basic tab  
> \zlicense     - License text from the Basic tab  
> \zimagecopyrights   - Automatically generated list of images, page numbers and attributions.  
> \zimagecopyrightsfr - as above, but use localized (fr = French) version (es, fr, hu, id, pt, ro available).
>
> \b can be used to insert a blank line between markers if needed.
>
> If using a Left-to-Right script for the colophon in a RTL publication you will need to add \beginL to force the colophon to render LTR. For example:  
>    \pc \beginL \zcopyright  
>    \pc \beginL \zlicense  
>    \pc \beginL \zimagecopyrights
>
> These special codes may also be used in other books such as the front matter book (FRT).
>
> IMPORTANT: You will have to click Print a second time in order to get accurate Image Copyright Attribution.

##### Colophon text entry

Text area · Regular+ · `textv_colophon`  
Needs: “Colophon at End of Publication” · Hidden until: “Colophon at End of Publication” · Shown when: “Colophon at End of Publication”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”

> Note: There are several shortcuts you can use:  
>    (c) --> ©  the copyright sign  
>    (r) --> ®  to denote registered trademarks  
>    (tm) --> ™  to denote trademarks in general
>
> Other special codes converted at print time:  
> use ~ for places where a non-breaking space is needed use // where a line break needs to be forced but :// used in URLs will still be preserved

Start each paragraph with a marker such as `\pc` (centred). `\zcopyright`, `\zlicense` and
`\zimagecopyrights` insert the copyright, the licence and the picture credits. For a
translated picture-credit list, add a language code, for example `\zimagecopyrightsfr`.

##### Clicking this button will reload the default Colophon text m...

Button · Regular+ · `btn_resetColophon`  
Needs: “Colophon at End of Publication” · Hidden until: “Colophon at End of Publication” · Shown when: “Colophon at End of Publication”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”

> Clicking this button will reload the default Colophon text markers which include the Copyright statement tag, the License statement tag, and the Illustration credits tag. Your current colophon text will be replaced.

The standard text is copyright, licence, a blank line and the picture credits. For a diglot it
also includes the copyright of the second language. Your own colophon text is lost.

##### Force Page Break Before Colophon

Checkbox, off · Regular+ · `c_standAloneColophon` · cfg `project/pgbreakcolophon`  
Needs: “Colophon at End of Publication” · Hidden until: “Colophon at End of Publication” · Shown when: “Colophon at End of Publication”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”

> Normally the colophon is inserted at the end of the last page of the last book. If this option is checked, then the colophon will appear at the bottom of a new page at the end of the publication.
>
> In Diglot publications, the colophon always appears on its own page - regardless of this setting.

Without it, the colophon follows the last lines of the last book on the same page (if there
is room).


# 17. Publications tab

## 17.1 What this tab is for

Use this tab to make several similar books from one project with the same design, without
making a new configuration for each. For example: one PDF for each Gospel, or a New Testament
and a separate book of Psalms, each with its own title.

A **publication** here means this configuration, printed with

* its own list of books, and
* its own values for some front matter variables (for example the main title and the
  subtitle).

All other settings (page size, fonts, layout, front matter, cover and so on) come from the
current configuration. Make a list of publications, tick the ones you want, and click
**Print Selected**. PTXprint makes one PDF for each ticked publication.

This tab is only shown in the **Full** view. (In the other views the **Pub** column in the
variables table on the **Peripherals** tab is hidden too.)

## 17.2 The list of publications

The list has three columns:

* **Print** – tick the publications to print. The checkbox in the column heading ticks or
  unticks all at once.
* **Publication ID / Field** – on the first (bold) line of each publication, its name. Under
  it, the names of its fields (variables).
* **Books / Value** – on the bold line, the books to print. Under it, the value of each field
  for this publication.

Click the small arrow beside a publication (or double-click its line) to show or hide its
fields.

To change a value, click it, type the new text and press Enter. You can change:

* the **name** of a publication (bold, second column). Each name must be different. The name
  is also used in the PDF file name, so keep it short and simple;
* the **books** of a publication (bold, third column);
* the **value** of each field.

You cannot change field names here. They come from the variables table on the
**Peripherals** tab (see below).

### The books

Type the books as on the **Basic** tab, for example:

* `MRK` – one book;
* `RUT JON` – several books;
* `MAT-JHN` – a range of books;
* `JHN 1-5` – some chapters of one book.

You can also type the name of a module file (a file that lists which parts of the text to
print). If PTXprint cannot understand the books, the text turns red. Hold the mouse over it
to see what is wrong.

### The fields

Each publication always has the fields **maintitle** and **subtitle**. To add more, tick
**Pub** beside a variable in the **Variables and Values** table on the **Peripherals** tab.
The variable is then added to every publication. Untick **Pub** to remove it again (not
possible for **maintitle** and **subtitle**).

When you print a publication, PTXprint uses its values instead of the values on the
**Peripherals** tab, for that one PDF only. The values on the **Peripherals** tab are not
changed. The front matter (or the cover) must use the variables, for example
`\zvar|maintitle\*` on the title page.

If the book has a cover with a spine, there is also a **pagecount** field: the number of pages
of that publication. PTXprint uses it to work out the spine width for that publication's cover.

## 17.3 The buttons

* **Add** makes a new publication from the current settings.
* **Duplicate** copies the highlighted publication, called "Copy of ...". This is the quickest
  way to make a set: duplicate, then change the name, books and title.
* **Delete** removes the highlighted publication, after asking you.
* **Expand All** / **Collapse All** show or hide the fields of all publications.
* **Print Selected** prints every ticked publication.

The line at the bottom shows how many publications are ticked, and how many have books that
PTXprint cannot understand.

## 17.4 Printing the publications

When you click **Print Selected**, PTXprint:

1. saves the configuration (including the list of publications);
2. checks the books of each ticked publication. If some are wrong, it asks whether to print
   the others and skip these;
3. prints the publications in the background, several at the same time. **Maximum parallel
   processes** on the **Advanced** tab sets how many;
4. opens the folder with the PDFs when all are finished.

Each PDF is named after the project, the configuration and the publication name. The PDFs are
not shown in the PDF preview. Open them from the folder.

**Print Selected** is greyed out while the publications are printing.

Each configuration saves its own list of publications. When you switch configuration, the list
shows the publications of that configuration (empty if it has none).

## 17.5 Common tasks

### Make one PDF for each Gospel

1. On the **Peripherals** tab, tick **Local Front Matter** and check that the title page uses
   `\zvar|maintitle\*` (the standard front matter does).
2. On the **Publications** tab, click **Add**.
3. Click the bold name and type `Matthew`. Click the books and type `MAT`.
4. Open the publication, click the value of **maintitle** and type the title of Matthew in
   your language.
5. Click **Duplicate**. Change the copy's name to `Mark`, its books to `MRK`, and its title.
6. Do the same for Luke and John.
7. Tick all four and click **Print Selected**.

### Give each publication its own value for another variable

1. On the **Peripherals** tab, in the **Variables and Values** table, tick **Pub** beside the
   variable (for example **isbn**).
2. On the **Publications** tab, open each publication and type its value.

### Print only some of the publications

1. Untick all publications with the checkbox in the **Print** column heading.
2. Tick the ones you want.
3. Click **Print Selected**.

### Remove a publication

1. Click the publication (or one of its fields).
2. Click **Delete**, then confirm.

## 17.6 Common problems

**Print Selected is greyed out.**
No publication is ticked, or PTXprint is still printing the last set.

**Duplicate and Delete are greyed out.**
Click a publication in the list first.

**The books are shown in red.**
PTXprint cannot understand the list of books. Hold the mouse over the red text to see the
problem. Use the 3-letter book codes, separated by spaces, for example `GEN EXO`.

**"None of the selected publications can be printed".**
All ticked publications have no books or wrong books. Correct the books.

**All the PDFs have the same title.**
The front matter does not use the variable, or uses a different one. Check that the title
page contains `\zvar|maintitle\*` (see the **View+Edit** tab chapter), and that **Local Front
Matter** is ticked on the **Peripherals** tab.

**A variable is not in the publications.**
Tick **Pub** beside the variable on the **Peripherals** tab (the **Pub** column is only shown
in the **Full** view).

**"A publication called ... already exists".**
Each publication needs a different name.

**The Publications tab is missing.**
Change the view level to **Full**.

**My publications have gone.**
Check that you are using the right configuration. Each configuration keeps its own list.

## 17.7 Settings reference

### Publications

#### Add

Button · Full · `btn_pubAdd`

> Add a new publication, filled in from the current configuration: the books chosen on the Basic tab, and the title, subtitle and other publishable \zvars from the Peripherals tab.

The new publication is ticked for printing. Its books are those chosen on the **Basic** tab (or
the module, or the chapter range). Its name is the main title (or "New publication"); if that
name exists, PTXprint adds a number, for example "(2)".

#### Duplicate

Button · Full · `btn_pubDuplicate`

> Make a complete copy of the highlighted publication, named 'Copy of ...' (Click a publication first.)

Copies all books and values. Greyed out until you click a publication.

#### Delete

Button · Full · `btn_pubDel`

> Delete the highlighted publication (you will be asked to confirm). (Click a publication first.)

Does not delete PDFs that were already made. Greyed out until you click a publication.

#### Expand All

Button · Full · `btn_pubExpandAll`

> Show the details of every publication.

Useful for checking all titles before you print.

#### Collapse All

Button · Full · `btn_pubCollapseAll`

> Hide the details of every publication.

Shows only names and books. Useful when the list is long.

#### tv_publications

Table · Full · `tv_publications`

The bold line of each publication shows the **Print** checkbox, the name and the books; the
lines under it show its fields and values. Click a name, the books or a value to change it;
press Enter to keep the change. Books that PTXprint cannot understand are shown in red.

#### Print Selected

Button · Full · `btn_pubPrint`

> Save the configuration, then create a PDF for each ticked publication (in the background). The folder with the PDFs opens when they are finished.

Prints several publications at the same time. Publications with wrong books are skipped after
asking you. Greyed out when nothing is ticked or while printing.


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


# 19. Printers tab

## 19.1 What this tab is for

The **Printers** tab helps you plan the printing of your book. It gives a rough **price estimate** from several print companies, shows how thick the book will be, and lets you **compare prices** between printers in a graph. For one printer (Pretore), you can also get an exact quotation and start an order from PTXprint.

Come here when the book is nearly finished and you want to know: "About how much will 500 copies cost?", "Which printer is cheapest for this size and number of pages?", or "How thick will the spine be?"

The tab is only shown in the **Full** view.

**Important:** most prices here are *estimates*, calculated from price information collected earlier from each printer. Real prices change, and shipping and taxes are not included. Always get a real quotation from the printer before you decide.

The tab has three parts:

1. **Book & Job Specification** at the top – the facts about your book and print job.
2. The **printer list** – one row per printer, with an estimated price per copy.
3. The **printer details** panel – options and price details for the printer you click in the list.

## 19.2 Book & Job Specification

These settings describe the job, for all printers. Every change recalculates all prices.

* **Pages** – from the most recent PDF you made. You can change it, for example to add pages for front matter that is printed separately.
* **Copies** – how many books to print.
* **Interior** – **Black & white** or **Full color** for the inside pages.
* **Binding** – each printer uses its nearest matching binding. If a printer does not offer your choice, its details panel says so in red.
* **Currency** – the currency for all prices. Exchange rates come from the internet, so prices from printers in other countries can be shown in your currency.
* **Trim size** – the finished page size (in mm), from the page size on the **Layout** tab. You cannot change it here.
* **Thickness** – the estimated book (spine) thickness for the printer selected in the list. It depends on the number of pages, that printer's paper, and the binding. Useful for a cover design, because the spine width must match the book thickness.

## 19.3 The printer list

Each row shows:

* a **Compare** tick box;
* the **Printer** name, its country and web address;
* **Est. per copy** – the estimated price for one copy, at your number of **Copies**.

A small word under the price tells you where it comes from:

* **estimate** – calculated from PTXprint's own price model for that printer.
* **live quote** – from the printer's own system over the internet (Pretore).
* **quote in panel** – this printer gives live quotes only. Open its panel and ask for a quotation.
* **no model yet** – no price information for this printer yet. Use its web link to ask for a price.

When two or more printers have a price, the cheapest is shown in **green**.

Click a printer's row to see its details panel.

**Per Copy** and **Total Job** show the price for the selected printer: for one copy, and for the whole job. The total can be for slightly more copies than you asked for, if that printer rounds the number of copies (see below).

### Compare Prices...

**Compare Prices...** opens the **Multi-Quote Comparison** window: a graph of the price for each printer ticked in the **Compare** column, at 50, 100, 250, 500 and 1000 copies, plus your own number of **Copies**.

In this window you can:

* choose **Price per Copy** or **Total Price**;
* set a **Max Budget**, so that totals above it are left out (tick **No limit** to show everything);
* tick or untick printers under **Show Printers**;
* tick **Show smooth curves** to draw curves instead of straight lines;
* point at a dot to see the exact value.

Printers with no price model cannot be ticked for comparison. For Pretore, PTXprint asks Pretore's server for prices; this needs a Pretore account (see below).

## 19.4 The printer details panels

Each printer has its own panel. Its options only affect that printer's estimate.

### Pothi (India)

* **Paper type** – plain white, plain natural shade, or coated. For black-and-white books the paper does not change the price. Coated paper costs more only with a full-colour interior.
* The panel shows how the price is made up: the **Nearest size** in Pothi's list of book sizes, the base price, the binding adjustment, the colour cost, and the **1-copy price**.
* A row of prices shows the discount for larger orders (1, 50+, 100+, 250+, 500+, 1000+ copies). The price for your number of copies is in bold.
* Red warnings appear if the job breaks Pothi's rules. For example: saddle-stitching only up to 64 pages; soft cover only from 50 to 500 pages; for 1500 or more copies, contact Pothi directly.

### Print Gallery (India)

* **Paper type** – several paper weights (gsm = grams per square metre; a higher number is thicker paper).
* **Lamination** – a thin plastic layer to protect the cover.
* The panel shows the cost of covers, interior, lamination and binding, and how the pages are arranged on Print Gallery's large sheets (**Imposition**).
* Sheets hold 4 pages, so the page count is rounded up to a multiple of 4. A5 books are printed in pairs, so an odd number of copies is rounded up by one. A red note tells you when this happens.
* Stapled binding is not used for books over 100 pages; perfect (glued) binding is priced instead.

### Pretore (Netherlands)

Pretore gives **live quotations** from its own system, and you can start an order from PTXprint. You need a Pretore account and an internet connection.

* **Paper Type**, **Cover Lamination**, **Shrink Wrap** and **Ribbons** (marker ribbons, hardback only) – Pretore's own options.
* **Book Identifier** and **Description** – filled in from the project and the books you print. Both are needed before you can get a quotation or create an order.
* **Account...** – choose your Pretore account, or import an account key file downloaded from the Pretore website. The window has a link to register and download the key.
* **Get Precise Quotation** – asks Pretore for the real price of this job.
* **Create Order** – packs the finished PDF files into a ZIP file and creates an order at Pretore. It shows the order reference, the ZIP file name and the status (**awaiting payment**). The copy button copies the full path of the ZIP file.
* **Complete Order & Payment via website** – opens the Pretore website, where you upload the ZIP file and pay.

Pretore accepts books of 120 to 2000 pages. It does not offer saddle-stitching (it quotes paperback instead), and its price is the same for black-and-white and colour interiors.

### Snowfall Press (United States)

No price information yet, so it is left out of comparisons. Use the link in the panel to ask for a quotation.

## 19.5 Common tasks

### Get a quick price estimate for my book

1. Make the PDF of the whole book first (click **Print**), so that the page count is correct.
2. Change to the **Full** view if the **Printers** tab is not visible.
3. Open the **Printers** tab. Check **Pages** and **Trim size**.
4. Enter the number of **Copies**, and choose **Interior** and **Binding**.
5. Choose your **Currency**.
6. Read the **Est. per copy** column. The cheapest printer is shown in green.

### Compare prices from several printers in a graph

1. Fill in the **Book & Job Specification** as above.
2. Tick **Compare** for each printer you want in the graph.
3. Click **Compare Prices...**.
4. Choose **Price per Copy** or **Total Price**. Point at the dots to read exact prices.

### Find out how thick the book will be (for the cover spine)

1. Fill in **Pages** and **Binding**.
2. Click a printer in the list, then choose its paper in its details panel.
3. Read **Thickness**. Different printers and papers give different thicknesses. Ask the printer for the exact spine width before you finish the cover.

### Order from Pretore

1. Make the final PDF with the format Pretore asks for (see the **Finishing** tab).
2. On the **Printers** tab, click **Pretore** in the list.
3. Click **Account...** and choose or import your account key.
4. Choose the paper and other options. Check **Book Identifier** and **Description**.
5. Click **Get Precise Quotation** and check the price.
6. Click **Create Order**. PTXprint makes the ZIP file and shows the order reference.
7. Click **Complete Order & Payment via website** to upload the ZIP file and pay.

## 19.6 Common problems

**I cannot see the Printers tab.**
Change the view level to **Full**.

**The number of pages is 99, or is wrong.**
**Pages** comes from the last PDF made for the current books; 99 means no PDF yet. Click **Print** first, then come back. Or type the correct number into **Pages**.

**A printer shows "—" and no price.**
Either it has no price model yet (**no model yet**), or it gives live quotes only (**quote in panel**). For Pretore, set up an account and click **Get Precise Quotation**. Also check the red warnings in the printer's panel: the job may be outside that printer's limits.

**Pretore says "No account configured".**
Click **Account...** in the Pretore panel and import the account key file from the Pretore website.

**"Get Precise Quotation" and "Create Order" are greyed out.**
Fill in both **Book Identifier** and **Description**.

**"Create Order" says I must print the job first.**
The ZIP file needs the finished PDF files. Click **Print**, then try again.

**The total is for more copies than I asked for.**
Some printers print in pairs or round the number of copies. A red note in the printer's panel explains this.

**I cannot tick a printer in the Compare column.**
That printer has no price model.

**Prices are shown in the wrong currency, or not converted.**
Exchange rates are downloaded from the internet. Without a connection (or when **Disable ALL Internet Use** is ticked on the **Advanced** tab), prices from another country may be shown in that printer's own currency, or left out of the comparison graph.

## 19.7 Settings reference

### Printers

#### Compare Prices...

Button · Full · `btn_prn_compare`

> Show a graph comparing prices (per copy or total) at several quantities across all the printers ticked in the Compare column above.

For Pretore, this first asks Pretore's server for prices (needs an account and an internet connection). If no ticked printer has a price, no graph appears.

#### Book & Job Specification

##### Thickness

Label · Full

> Spine/book thickness for the currently selected printer, based on its paper stock and binding.

##### Trim size

Label · Full

> Finished page size of the book, from the Layout page settings.

##### Pages

Number · Full · `s_prn_pages`  
Values: 1–9999 (default 200)

> Number of pages in the book. Filled in automatically from the most recently created PDF (99 if no PDF has been made yet), but can be adjusted manually.

Make the PDF first. Change it by hand if the printed book will have more pages than the PDF (for example extra blank pages or separately printed front matter). Printers usually charge per page, so this has a big effect on the price.

##### Copies

Number · Full · `s_prn_copies`  
Values: 1–99999 (default 50)

> How many copies of the book to be printed.

All prices, warnings and the total use this number. More copies usually lower the price per copy; **Compare Prices...** shows this at 50, 100, 250, 500 and 1000 copies.

##### Interior

Drop-down · Full · `fcb_prn_interior`  
Choices: Black & white | Full color

> Whether the inside pages are printed in black & white or full color.

**Full color** is much more expensive at most printers, even if only a few pages have colour. Choose **Black & white** unless the inside really needs colour. Some printers do not change the price for colour (Pretore), and some do not yet have colour prices for every size (a red note tells you).

##### Binding

Drop-down · Full · `fcb_prn_binding`  
Choices: Paperback (soft cover) | Hardcover | Saddle-stitched (stapled)

> Preferred binding style. Each printer maps this onto the nearest option it offers.

Paperback is the usual choice. Hardcover costs more but lasts longer. Saddle-stitched (stapled) is only for thin books; printers limit the pages (for example Pothi: up to 64). If a printer does not offer your choice, its panel says which binding it priced instead. The binding also changes the **Thickness**.

##### Currency

Drop-down · Full · `fcb_prn_currency`

> Currency used to display all quotations and estimates. Prices in other currencies are converted using exchange rates downloaded from the internet (a guide only).

The printer will still charge in its own currency.


# 20. PDF Preview window, layout analysis and page filling

## 20.1 What this window is for

The **PDF Preview** window shows the PDF that PTXprint has just made. It opens by itself after you click **Print**. Use it to:

* read through the pages, one page or two facing pages (a "spread") at a time;
* find layout problems quickly (for example pages that are not full, or words with too much space between them);
* fix small layout problems on the page: right-click a paragraph to make it one line shorter or longer, or right-click a picture to move it or change its size;
* run the **Auto Page Fill** tool, which tries to make every page full by itself.

It is a separate window that you can keep open beside the main window. Changes made here are saved with the current configuration.

In this chapter, "pt" means point (about 0.35 mm). "em" is a width equal to the text size; in 10 pt text, 1 em is 10 pt.

## 20.2 Opening and closing the Preview window

* The window opens after each **Print** if the main menu (☰) > **Show PDF** is set to **Preview Pane** (the normal setting). With **System Viewer** the PDF opens in your normal PDF program instead; with **Output Folder**, PTXprint opens the folder that holds the PDF.
* Closing the window with its **X** button only hides it. It comes back the next time you print.
* **Show main PTXprint settings** (**Alt+S**) brings the main window to the front.
* The title bar shows the PDF file name and the date and time it was made. Check this to be sure you see the newest PDF.

The preview has tabs down the left side. **Content** shows your main PDF. **Cover** shows the cover PDF, if you made one. **Diff** shows the comparison PDF, if you used **Compare PDFs** (on the **Finishing** tab) and differences were found. If there was nothing to compare with, or no differences, there is no **Diff** tab: the preview shows the new PDF, and the status line in the main window says why. **Reference** shows reference documents such as the Ornaments Catalogue. Tabs without a PDF are hidden.

## 20.3 Moving around: pages, spreads and zoom

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

## 20.4 The Content tab: what to show on the preview

These options only change the preview, not the PDF.

* **Adjustments** draws coloured bars on the edges of adjusted paragraphs. **Left** edge = shrunk; **right** edge = expanded. **Blue** = the number of lines was changed. **Red** = the text width was changed (letters a little narrower or wider). Red and blue stripes = both. A thicker bar means a bigger change. Leave this ticked while you work on the layout.
* **Paragraph Boxes** draws a thin box around every adjustable paragraph, so you see where each paragraph begins and ends, and where to right-click.
* **Guides and Baselines** draws the margins, the header and footer positions and the baselines (the lines the text sits on).
* **Graph Paper** draws a measuring grid over the page. **Settings** next to it changes the units, number of divisions, colours and line thickness.
* **Layout Analysis** marks typesetting problems in colour on the page. See the next section.

### Auto-update

When **Auto-update** is ticked, PTXprint makes a new PDF by itself a few seconds after you use the right-click menu. The delay (normally 3 seconds) is shown as "(3.0s delay)". It lets you make several changes in a row: each new right-click restarts the delay, so only one print is made at the end. Click the delay text to go to the setting (**Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings** > **Auto-update Delay (seconds)**).

When **Auto-update** is not ticked, your changes are stored but nothing happens until you click **Print (Update PDF)** (**Ctrl+P**). The right-click menu then also has a **Print (Update PDF)** item.

## 20.5 Layout Analysis and finding issues

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

## 20.6 Adjusting paragraphs with the right-click menu

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

## 20.7 Moving and resizing pictures with the right-click menu

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

## 20.8 SpeedSlice: work on one part of a long book quickly

Each print of a long book (for example Psalms or Isaiah) can take a long time. When you fix pages in the middle of such a book, you must wait for the whole book after every change. **SpeedSlice** typesets only a "slice": it starts at the page you are working on and continues for a few chapters. Each print is then fast.

To open it, right-click a `\p` or `\m` paragraph near the top of the page where the slice should begin, and choose **SpeedSlice**. (Not available for diglots.) The dialog has:

* **Reference for Start of Slice** – filled in from the paragraph you clicked. Type either a chapter (for example `JHN 4`) to start at the beginning of that chapter, or the last verse on the page before (for example `GEN 3:23`).
* **First Word on This Page** – if you gave a verse, type the first word on the page where the slice should start. PTXprint skips all the text before that word.
* **Slice Marker (usually \m)** – the paragraph marker the slice starts with.
* **Length of Slice (in chapters)** – how many chapters to include.

**Enable** turns the slice on. **Disable** turns it off and goes back to printing the whole book.

**Important:** SpeedSlice stays on until you turn it off. While it is on, your PDF contains only the slice, and its page numbers are not the real page numbers. Always **Disable** the slice before you make the final PDF.

## 20.9 Auto Page Fill and the progress monitor

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

## 20.10 The buttons at the bottom of the window

* **Show Report Information** – makes a report about the current configuration and opens it in your web browser.
* **Open the PDF in Default PDF Viewer** – opens the PDF in your normal PDF program.
* **Open folder containing the PDF** – opens the output folder in your file manager.
* **Save the PDF with a different name** – saves a copy of the PDF anywhere you like.
* **Print the PDF on paper** – sends the PDF to a printer connected to your computer.

## 20.11 Common tasks

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

## 20.12 Common problems

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

## 20.13 Settings reference

### PDF Preview > Issue types popup

#### Bad Glyphs

Checkbox, on · Regular+ · `c_findBadGlyphs`

Finds characters the font has no shape for (marked purple). Often caused by a wrong font, or a character typed by mistake (for example a wrong Unicode character). Fix it by choosing a font that has the character, or by correcting the text in Paratext.

#### Glyph Collisions

Checkbox, on · Regular+ · `c_findCollisions`

Finds letters or marks that touch or overlap (marked red). The sensitivity is set by **Collision Detection Padding (pt)** and **Precise collisions** on the **Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings**. Collisions may need more line spacing, or a different font.

#### Excessive horizontal whitespace

Checkbox, on · Regular+ · `c_findWhitespace`

Finds word spaces wider than **Bad Space minimum width (em)** (normally 1.3 em), marked with a light blue-green bar. Common in short lines and narrow columns. Hyphenation, a slightly smaller font, or **Shrink Text** / **Expand Text** on the paragraph can help.

#### Vertical rivers of whitespace

Checkbox, on · Regular+ · `c_findRivers`

Finds "rivers" (marked yellow). To remove one, change the line breaks in the paragraph, for example with **Shrink Text** or **Expand Text** from the right-click menu.

#### Underfilled Pages

Checkbox, on · Regular+ · `c_findUnbalanced`

The most common issue. Found from the typesetting log, so it works even when **Layout Analysis** is off. Fix with the right-click shrink/expand items or the Auto Page Fill tool. The last page of a book is often short; that is normal.

### PDF Preview (dialog)

#### Zoom

Number · Mini+ · `s_pdfZoomLevel` · cfg `config/pdfzoomlevel`  
Values: 10–800 (default 100)

> Zoom Shortcuts:  
> Ctrl + F - fit to screen Ctrl + Plus - zoom in Ctrl + Minus - zoom out Ctrl + 0 - fit to screen Ctrl + Scrollwheel - change zoom level

100 = actual size. **Ctrl+mouse wheel** (zooms at the pointer) or **Ctrl+F** (fit) is usually easier.

#### Zoom Fit to Screen

Button · Regular+ · `btn_zoom_fit`

> Zoom Fit to Screen

Fits the whole spread in **Book View**.

#### Page/Spread

Label · Mini+ · `l_pdfPgsSprds`

> Shortcuts:  
> Left-Arrow (or PgUp) - previous page/spread Right-Arrow (or PgDn) - next page/spread Ctrl+Home - First page/spread Ctrl+End - Last page/spread Mouse Scroll also changes pages Ctrl+Mouse Scroll Zooms in/out

Only a label ("Pages:" before the page count). Its tooltip lists the page-moving shortcuts.

#### (15)+52 – First page (or spread)

Button · Mini+ · `btn_page_first`

> First page (or spread)
>
> Negative page numbers refer to the peripheral pages before the main text begins on Page 1.
>
> Shortcuts:  
> Left-Arrow (or PgUp) - previous page/spread Right-Arrow (or PgDn) - next page/spread Ctrl+Home - First page/spread Ctrl+End - Last page/spread Mouse Scroll also changes pages Ctrl+Mouse Scroll Zooms in/out

In a count like "(15)+52", the number in brackets is the pages before page 1 (for example title page and contents); the second number is the numbered pages.

#### Previous page (or spread)

Button · Mini+ · `btn_page_previous`

> Previous page (or spread)

One spread in **Book View**. Same as **Left arrow** or **Page Up**. Reversed in a right-to-left book.

#### Type page number to jump to

Text box · Mini+ · `t_pgNum`

> Type page number to jump to.
>
> Shortcuts:  
> Left-Arrow (or PgUp) - previous page/spread Right-Arrow (or PgDn) - next page/spread Ctrl+Home - First page/spread Ctrl+End - Last page/spread Mouse Scroll also changes pages Ctrl+Mouse Scroll Zooms in/out

Type the printed page number (the number on the page, not the position in the PDF file) and press **Enter**. If that page does not exist, the preview goes to the nearest page.

#### Next page (or spread)

Button · Mini+ · `btn_page_next`

> Next page (or spread)

One spread in **Book View**. Same as **Right arrow** or **Page Down**.

#### Last page (or spread)

Button · Mini+ · `btn_page_last`

> Last page (or spread)

Same as **Ctrl+End**.

#### Locate...

Menu button · Regular+ · `btn_findButton`  
Also: Select which types of issues to highlight · Needs: “Layout Analysis”

> The next/previous issue arrows will jump to pages with issues to be resolved. You can choose which kinds of issues to deal with.
>
> Note: It is only enabled when Layout Analysis is active. Without it, the arrows only jump to underfilled pages.

The choices are **Bad Glyphs**, **Glyph Collisions**, **Excessive horizontal whitespace**, **Vertical rivers of whitespace** and **Underfilled Pages**. Tick only the kinds you want to work on now.

#### Locate the previous issue

Button · Regular+ · `btn_seekPage2fill_previous`

> Locate previous page with issues.

Hold the mouse over it to see the problem pages, coloured by kind of issue.

#### Locate the next issue

Button · Regular+ · `btn_seekPage2fill_next`

> Locate next page with issues.

The button you use most when fixing the layout: fix a page, then click this to go to the next problem. Hold the mouse over it to see the problem pages.

#### Print (Update PDF)

Button · Mini+ · `b_reprint`

> Update the PDF
>
> Shortcut: Ctrl-P

Same as **Print** on the main window. Needed when **Auto-update** is off, or after you change settings on the main window.

#### Show/hide the Page Filler with progress monitor

Toggle, off · Regular+ · `btn_prvAutoFill`

> Show/hide the Page Filler with progress monitor

Opening the **PTXprint: Page Filler** window starts nothing; use **Start Fill** or **Resume Fill** there. The job can take a long time and uses a lot of processor power.

#### Show main PTXprint settings

Button · Mini+ · `btn_showSettings`

> Show the main PTXprint dialog with all the settings. Shortcut: Alt+S

Use it to go back and change settings.

#### Show Report Information

Button · Regular+ · `btn_prvReport`

> Display a report on the current configuration.

The report lists possible problems, for example the number of underfilled pages. The button changes colour when there are warnings or errors, and its tooltip then gives a short summary.

#### Open the PDF in Default PDF Viewer

Button · Mini+ · `btn_prvOpen`

> Open the PDF in the system's default PDF viewer (e.g. Evince, Acrobat or SumatraPDF).

Use it to search the text or print with that program.

#### Preview Pane: Open folder containing the PDF

Button · Mini+ · `btn_prvOpenFolder`

> Open the folder which contains the PDF file(s) created for this project.

Use it to find the PDF to send to someone.

#### Save the PDF with a different name

Button · Mini+ · `btn_prvSaveAs`

> Save a COPY of this PDF with a new name and/or different folder.

The original PDF stays where it is. PTXprint remembers the last folder you used.

#### Print the PDF on paper

Button · Mini+ · `btn_prvPrint`

> Print the PDF on paper using a physical printer connected to this device.

For proof copies. For the final book, send the PDF to the printing company.

#### Content

##### Auto-update

Checkbox, on · Regular+ · `c_updatePDF` · cfg `config/updatePDF`

> When enabled, this re-creates the PDF after making changes using the (right-click) context menu options.
>
> Note that there is a short delay enabling you to make several adjustments one after the other before the update is triggered. This delay can be adjusted by clicking on the value shown here or refer to: Advanced > Other > Preview Pane: Adjustment and Analysis Settings.

Applies to shrink, expand, reset, picture changes and so on. Ticking it also starts an update straight away. Untick it if each print takes a long time and you want to make many changes first; then click **Print (Update PDF)** when ready.

##### (3.0s delay)

EventBox · Mini+

> When enabled, this re-creates the PDF after making changes using the (right-click) context menu options.
>
> Note that there is a short delay enabling you to make several adjustments one after the other before the update is triggered. This delay can be adjusted by clicking on the value shown here or refer to: Advanced > Other > Preview Pane: Adjustment and Analysis Settings.

##### (3.0s delay)

Label · Regular+ · `l_updateDelay`

> When enabled, this re-creates the PDF after making changes using the (right-click) context menu options.
>
> Note that there is a short delay enabling you to make several adjustments one after the other before the update is triggered. This delay can be adjusted by clicking on the value shown here or refer to: Advanced > Other > Preview Pane: Adjustment and Analysis Settings.

Seconds PTXprint waits after your last right-click change. Click it to go to **Auto-update Delay (seconds)** on the **Advanced** tab > **Other** > **Preview Pane: Adjustment and Analysis Settings**. Make it longer if printing starts before you have finished your changes.

##### Book View

Checkbox, on · Mini+ · `c_bkView`

> Toggle between a single page view and a book (spread) view. Shortcut: Ctrl + B

Page 1 is shown alone. Use it to check that facing pages look balanced and end at the same height. Untick it for a larger view of one page.

##### Adjustments

Checkbox, on · Mini+ · `c_pdfadjoverlay`

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

A thicker bar means a bigger change. Shows paragraphs adjusted by you or by the Auto Page Fill tool.

##### Paragraph Boxes

Checkbox, off · Mini+ · `c_pdfparabounds`  
Also: Show Paragraph Boxes

> Draw boxes around the boundaries of all adjustable paragraphs.

Shows where each paragraph starts and ends, so you know where to right-click. Preview only.

##### Guides and Baselines

Checkbox, off · Regular+ · `c_gridLines` · cfg `grid/gridlines`  
Also: Show guides and baselines

> This option displays various guides (showing margins, headers and footers) as well as the baselines of the body text.

Use it to check that text sits on the line grid and headers and footers are in the right place.

##### Graph Paper

Checkbox, off · Regular+ · `c_gridGraph` · cfg `grid/gridgraph`  
Also: Show grid (graph paper)

> If the standard Rules and Guides are inadequate you can generate a graph-paper-like grid behind the text. This may be useful for precise measuring.

Use it to measure positions and sizes, for example of pictures or margins. **Settings** next to it changes the grid.

##### Settings

Label · Regular+ · `lb_adjustGrid`  
Also: Graph Paper Settings

> Change the graph paper settings.

Opens the **Change the Grid Settings** dialog: grid units, divisions, offset, colours and line thickness.

##### Layout Analysis

Checkbox, off · Regular+ · `c_layoutAnalysis`  
Also: Perform Layout Analysis of the text to highlight issues

> This option analyzes the text to highlight layout issues:  
> - character collisions  
> - missing glyphs (bad glyphs)  
> - excessive horizontal space  
> - vertical rivers of space

Also makes **Locate...** available. It takes some time on large PDFs and runs again after each print while ticked. It turns itself off when you change book or configuration.

##### Settings

Label · Regular+ · `l_analysisSettings`  
Also: Layout Analysis Settings

> Click to show the Advanced > Other settings to adjust the parameters which control what should get highlighted as an issue.

There you set the limits for what is marked, for example **Bad Space minimum width (em)** and the river detection settings.

##### Contents

Table · Mini+ · `tv_pdfContents`

Double-click a line to jump to that page. With only one book, its list is opened out automatically.

### Enter new anchor verse ref (dialog)

#### OK

Button · Regular+ · `btn_anc_ok`

Moves the picture to the new verse and updates the picture list. Only active when the reference is valid and no other picture uses that verse.

#### Cancel

Button · Regular+ · `btn_anc_cancel`

Closes the dialog without changing the anchor.

#### Anchor Ref – Enter a new anchor verse

Text box · Regular+ · `t_newAnchor`

> Enter the new anchor verse reference (e.g. JHN 3.16)

Format: book code, a space, chapter.verse. A colon is changed to a full stop for you. For a diglot, the book code can include the side letter (for example `JHNR 3.16`).

### SpeedSlice (dialog)

#### Enable

Button · Regular+ · `btn_slice_ok`

> Print only this slice of the book (for quick layout work).

The next print contains only the slice. Turn it off before you make the final PDF.

#### Disable

Button · Regular+ · `btn_slice_cancel`

> Turn SpeedSlice off, so that the whole book is printed next time.

Use it when you have finished working on the slice.

#### Reference for Start of Slice – Slice Dialog: Enter reference to begin SpeedSlice

Text box · Regular+ · `t_sliceRef` · cfg `slice/ref`

> Either enter a chapter number to begin with (e.g. JHN 4) or enter the last verse on the preceding page (e.g. GEN 3:23) to begin the slice. Previous content will be skipped over.
>
> SpeedSlice stays on until you click Disable in this dialog.

Filled in from the paragraph you right-clicked. A chapter only (for example `PSA 45`) starts at the start of that chapter. With a verse (for example `GEN 3:23`) you must also fill in **First Word on This Page**.

#### First Word on This Page – Slice Dialog: Enter first word on page

Text box · Regular+ · `t_sliceWord` · cfg `slice/word`

> Enter the first word on this page (where the Slice will begin).

PTXprint looks for this word after the verse in **Reference for Start of Slice** and skips everything before it. Type it exactly as in the text (same spelling and letters). If the word is not found, the slice cannot start there.

#### Slice Marker (usually \m) – Slice Dialog: Enter beginning marker

Text box · Regular+ · `t_sliceMkr` · cfg `slice/marker`

> What USFM marker needs to be used at the beginning of the Slice? (almost always \m)

`\m` is a paragraph with no first-line indent, which matches a page that starts in the middle of a paragraph.

#### Length of Slice (in chapters) – Slice Dialog: Length of Slice

Number · Regular+ · `s_sliceLength` · cfg `slice/length`  
Values: 1–10 (default 3)

> Roughly how many chapters should the Slice contain?

A short slice prints faster. Make it long enough for all the pages you want to work on. In books with long chapters, 1 or 2 may be enough.


# 21. Importing settings

## 21.1 What this dialog is for

The **Import Settings** dialog copies settings from somewhere else into a configuration. Use it when:

* you have a PDF that PTXprint made earlier, and want the same layout again (for example the settings were lost, or the PDF came from another person),
* someone sent you a PTXprint ZIP archive,
* another project or configuration has settings you want to reuse – all of them, or only some groups (for example only the pictures, or only the header and footer).

You can also **extract** the settings from a PDF or ZIP into a normal folder, to look at them.

To open it: on the **Basic** tab, in the **Layout Configuration** area, click **Import Settings...**. (Not shown in the **Mini** view.)

The dialog has three parts: **Source of Settings** (where the settings come from), **Target** (where they go), and a row of **category tabs** (what to bring in).

## 21.2 Source of Settings

Choose one of two sources:

* **PDF file (with embedded settings) or ZIP archive file** – click **Select...** and choose the file.
  * A **PDF** only works if PTXprint made it with **Include Config Settings Within PDF** turned on (on the **Finishing** tab). Otherwise PTXprint says it cannot find any settings in the file.
  * A **ZIP archive** is the kind of file made with **Create Archive...** on the **Help** tab.
* **A Previously Saved Configuration** – choose the **Project** and then the **Configuration** to copy from. Settings are read from the saved files, so if the source is the configuration that is open now, click **Save** first.

## 21.3 Target

Choose where the settings go:

* **A New/Existing Project and/or Configuration** – the usual choice. The current project and configuration are filled in. You can choose another existing project, and another configuration, or type a **new** configuration name. A new configuration starts with the PTXprint defaults, and then the imported settings are added. So for a new name, PTXprint ticks **Everything** and greys out the category boxes. If you then choose an existing configuration again, **Everything** is unticked again (unless you ticked it yourself).
* **An External Folder of Settings** – click **Select...** and choose a folder. PTXprint copies **all** the settings files from the source into that folder. Nothing in your projects is changed. **Everything** is turned on and the category tabs are greyed out.

**OK** stays greyed out until the choices are complete: a file or source configuration, a target folder or target configuration, and at least one category ticked. It is also greyed out when the source and target are the same configuration, and when the target **Project** name you typed is not one of your projects.

## 21.4 What to import: the category tabs

Each tab has a check box in its label: tick it to import that group. Click the tab to see its options.

* **Pictures** – the picture settings and the picture list.
* **Layout** – the page and column layout.
* **Fonts+Script** – fonts and writing-system settings.
* **Styles** – the settings from the **Styles** tab.
* **Other** – other groups that you choose one by one.
* **Everything** – all settings. (Only shown in the **Regular** and **Full** views.)

When **Everything** is ticked, everything is imported, whatever the other boxes say. Untick **Everything** to import only some groups.

### What each category brings in

| Category | What is imported |
|---|---|
| **Pictures** | The general settings of the **Pictures** tab (include pictures, picture folder, resolution, captions shown, placeholders…) and the picture list. With **Import Entire PicList "as is"** the whole list is replaced. With **Import Elements of PicList** only the parts you tick are copied for each picture. |
| **Layout** | Page size, margins (top, bottom, side), mirror pages and binding gutter, number of columns and column gutter, vertical rule between columns, line spacing, note lines, margin notes, and related settings. **Not** the fonts or font size (in **Fonts+Script**) or the header and footer (in **Other** › **Header+Footer settings**). |
| **Fonts+Script** | The main fonts (regular, bold, italic, bold italic, extra), the font size, the fallback font, text direction, script and line-breaking settings, word and letter spacing, coloured text, and script-specific options. Also the fonts set inside individual styles (for styles that the target already has). Styles whose font you changed in the target keep it, unless **Override ALL Style Settings** is ticked. |
| **Styles** | The style settings from the source (the **Styles** tab). Normally only styles that you have **not** changed in the target are updated. **Override ALL Style Settings** updates all styles. The fonts inside styles come with **Fonts+Script**, not with **Styles**. |
| **Other** | Only the groups that you tick on the **Other** tab (see the control notes below). |
| **Everything** | All settings in the source configuration, including the book list, copyright text, diglot and Strong's settings, the whole picture list, styles, front matter, cover, and the special files from the **Advanced** tab. |

### What happens when you click OK

1. PTXprint reads the settings from the source.
2. It changes only the ticked groups in the target configuration.
3. It **saves** the target configuration at once.
4. It opens the target project and configuration, and shows a message such as "Imported Settings into: ABC::NT_A5".

There is no Undo. If you are not sure, import into a **new** configuration name first, and check the result there.

## 21.5 RESET

**RESET** at the bottom of the dialog sets all settings of the **current** configuration back to the PTXprint defaults, at once and without asking. It does not reset the style settings. The dialog stays open, and nothing is saved until you click **Save** or **Print (Make PDF)** (or until an import saves the configuration). Use it when you want the target to have only the imported settings, for example before you import styles.

## 21.6 Common tasks

### Get back the settings that were used for a PDF

1. On the **Basic** tab, click **Import Settings...**.
2. Click **PDF file (with embedded settings) or ZIP archive file**, then **Select...**, and choose the PDF.
3. Under **Target**, click **A New/Existing Project and/or Configuration**. In **Configuration**, type a new name, for example `FromPDF`.
4. Check that **Everything** is ticked. (For a new name, PTXprint ticks it for you. Change to the **Regular** view if you cannot see it.)
5. Click **OK**. PTXprint opens the new configuration with the settings from the PDF.

### Copy only the pictures from another configuration

1. Click **Import Settings...**.
2. Click **A Previously Saved Configuration** and choose the source **Project** and **Configuration**.
3. Check that the **Target** is the configuration you want.
4. Untick **Everything**, **Layout**, **Fonts+Script**, **Styles** and **Other**. Tick **Pictures**.
5. On the **Pictures** tab, choose **Import Entire PicList "as is"**, or **Import Elements of PicList** and tick only what you want (for example **Size, Position, Mirror, Rotation settings**).
6. Click **OK**.

### Copy the header and footer from another configuration

1. Click **Import Settings...** and choose the source configuration.
2. Untick **Everything** and all other categories, and tick **Other**.
3. On the **Other** tab, untick everything except **Header+Footer settings**.
4. Click **OK**.

### Look at the settings inside a PDF or ZIP without changing anything

1. Click **Import Settings...** and choose the PDF or ZIP file as the source.
2. Under **Target**, click **An External Folder of Settings**, then **Select...**, and choose an empty folder.
3. Click **OK**. The settings files are copied into that folder.

### Start a configuration again from defaults, then import styles

1. Open the configuration on the **Basic** tab.
2. Click **Import Settings...**, then **RESET**.
3. Choose the source, untick **Everything**, and tick **Styles** (and other groups you need).
4. Click **OK**.

## 21.7 Common problems

### "Cannot find any settings to import from the selected file"

**Cause:** The PDF was made without **Include Config Settings Within PDF** (on the **Finishing** tab), or with a very old PTXprint version (before 2.3). **What to do:** Use another source, for example a ZIP archive made with **Create Archive...** on the **Help** tab.

### The OK button is greyed out

**Cause:** Something is missing: no file selected, no target folder, no target configuration, no category ticked – or the source and target are the same configuration. **What to do:** Check each part of the dialog.

### Everything was imported, but I ticked only one category

**Cause:** **Everything** was still ticked. In the **Basic** view the **Everything** tab is hidden but still ticked (it is ticked by default). Also, when the target is a **new** configuration or an external folder, PTXprint ticks **Everything** itself and you cannot untick it. **What to do:** Import into an existing configuration. Change to the **Regular** view (**☰** › **View Level** › **Regular View**) and untick **Everything**.

### The styles did not change

**Cause:** Without **Override ALL Style Settings**, only styles still unchanged in the target are updated. **What to do:** Tick **Override ALL Style Settings**, or click **RESET** before you import.

### The font size did not change when I imported Layout

**Cause:** The font size belongs to **Fonts+Script**. **What to do:** Tick **Fonts+Script** too.

### The header and footer did not change when I imported Layout

**Cause:** They belong to **Other** › **Header+Footer settings**. **What to do:** Tick **Other** and **Header+Footer settings**.

### Custom Script is greyed out

**Cause:** The source is a PDF, which does not contain the custom script. **What to do:** Import from a ZIP archive or a saved configuration instead.

### The fonts in some styles did not change

**Cause:** Fonts inside styles come with **Fonts+Script** (not **Styles**), and styles whose font you changed in the target keep their font. **What to do:** Tick **Fonts+Script**. To replace the fonts in all styles, also tick **Override ALL Style Settings**.

### The category boxes are greyed out and Everything is ticked

**Cause:** The target is a configuration that does not exist yet (you typed a new name), or an external folder. A new configuration starts from the PTXprint defaults, so everything is imported. **What to do:** To import only some groups, choose an existing configuration as the target.

## 21.8 Settings reference

### Import Settings... (dialog)

#### RESET

Button · Basic+ · `btn_resetConfig`  
Also: Reset the current Configuration's UI settings

> Warning! This will reset ALL the UI settings for the CURRENT configuration to their default values.
>
> Note that it will NOT reset the Style settings stored in the .sty files.
>
> The reset is not saved until you next save, print, or import with OK.

Resets at once and without asking. See "RESET" in this chapter.

#### OK

Button · Basic+ · `btn_importSettingsOK`

Imports the ticked groups into the target, saves it, and opens it. With an external folder as target, it copies the settings files there instead. Greyed out until the choices are complete. Shortcut: **Alt+Enter**.

#### Cancel

Button · Basic+ · `btn_importCancel`

Closes without importing. (Changes made with **RESET** stay on the screen.) Shortcut: **Ctrl+W**.

#### Pictures

Checkbox, on · Basic+ · `c_impPictures`  
Also: Import Picture Settings

> Import the picture settings and the picture list. Use the Pictures tab of this dialog to choose how the picture list is combined.

Ticking or unticking it opens the **Pictures** tab of the dialog.

#### Layout

Checkbox, on · Basic+ · `c_impLayout`  
Also: Import Layout Settings

> Import page size, margins, columns, line spacing and related settings.

See the table in "What each category brings in". The text on the dialog's **Layout** tab also mentions the header and footer, but they are imported with **Other** › **Header+Footer settings**.

#### Fonts+Script

Checkbox, on · Basic+ · `c_impFontsScript`  
Also: Import Fonts and Script Settings

> Import the font and script settings (Fonts+Scripts tab), including fonts set within individual styles.

Imports fonts inside styles (font name and font features) even when **Styles** is not ticked. Hyphenation settings come with **Other** › **Body Tab settings**, not here.

#### Styles

Checkbox, on · Basic+ · `c_impStyles`  
Also: Import Styles Settings

> Import the style settings (Styles tab), merged into the target configuration.

Font names and font features inside styles are imported only when **Fonts+Script** (or **Everything**) is also ticked.

#### Other

Checkbox, on · Basic+ · `c_impOther`  
Also: Import Other Settings

> Use the Other tab of this dialog to choose more groups of settings. If this is not ticked, none of the boxes on the Other tab are used.

Groups on the **Other** tab include Body, Notes+Refs, Header+Footer, Advanced, Cover, Front +Back Matter and Finishing.

#### Everything

Checkbox, on · Regular+ · `c_impEverything`  
Also: Import All Settings

> Import all settings and files of the source configuration, whatever the other boxes say.

Use it to recreate a configuration from a PDF or ZIP, or to make a full copy. Ticked by default, and ticked again when you open the dialog with no category ticked. Also turned on automatically (with the other boxes greyed out) when the target is an external folder or a new configuration. In the **Basic** view it is hidden but still works.

#### Source of Settings

##### PDF file (with embedded settings) or ZIP archive file

Radio · Basic+ · `r_impSource_pdf`  
Also: Import: From existing PDF file or ZIP archive

> It is possible to import settings from an existing PDF file which was produced earlier by PTXprint. But this only works if the settings are embedded within the PDF. (This is enabled on the Finishing tab).
>
> Importing from a PTXprint ZIP archive (created on the Help tab) is also possible.

Click **Select...** to choose the file.

##### A Previously Saved Configuration

Radio · Basic+ · `r_impSource_config`  
Also: Import: From Saved Configuration

Choosing a project or configuration in the lists below also selects this option.

##### Project – Import: Project name

Drop-down · Basic+ · `fcb_impProject`  
Choices: unknown · Needs: “A Previously Saved Configuration”

> Select the project from which the settings will be imported.

Choosing a project fills the **Configuration** list with its configurations and selects **Default**.

##### Configuration – Import: Project configuration

Drop-down · Basic+ · `ecb_impConfig`  
Choices: (None) · Needs: “A Previously Saved Configuration”

> Select a configuration from the selected project from which the settings will be imported.

Settings are read from the saved files, so save the source configuration first if it is open.

##### Select...

Button · Basic+ · `btn_impSource_pdf`  
Also: Select PDF to import settings from · Needs: “PDF file (with embedded settings) or ZIP archive file”

> Select either a PTXprint PDF or ZIP archive to import the settings from.
>
> Importing from a PDF will only work if the PDF contains the PTXprint configuration settings (as enabled on the Finishing tab).

Starts in the output folder of the current project, where PTXprint keeps its PDFs. If the file has no PTXprint settings, PTXprint shows an error and changes back to **A Previously Saved Configuration**. The chosen file name is shown next to the button.

#### Target

##### An External Folder of Settings

Radio · Basic+ · `r_impTarget_folder`  
Also: Extract settings to an external folder

> Settings can be extracted to an external folder.
>
> This may be useful when examining settings from a different user, or when there is a need to recover lost settings from a known good PDF or Zip archive.

No project is changed. **Everything** is used automatically.

##### A New/Existing Project and/or Configuration

Radio · Basic+ · `r_impTarget_prjcfg`  
Also: Import: Into Project/Configuration

The usual choice. The current project and configuration are filled in when the dialog opens.

##### Project – Import: Project name

Drop-down · Basic+ · `ecb_targetProject`  
Choices: unknown · Needs: “A New/Existing Project and/or Configuration”

> Select an existing project into which the settings will be imported.
>
> Select the project into which the settings will be imported.

You cannot import into a new project. If you type a name that is not one of your projects, **OK** stays greyed out. Choosing a project here also selects **A New/Existing Project and/or Configuration** and fills the **Configuration** list.

##### Select...

Button · Basic+ · `btn_tgtFolder`  
Also: Select target folder for extracted settings · Needs: “An External Folder of Settings”

> Select a folder to save the settings in. This could be in a temporary location from where just the needed settings can be accessed and copied into the appropriate place of an existing config.

Choose an empty folder, so the extracted files are easy to find. The chosen folder is shown next to the button.

##### Configuration

Drop-down · Basic+ · `ecb_targetConfig`  
Choices: Default · Needs: “A New/Existing Project and/or Configuration”

> Choose a configuration from the selected project into which the settings will be imported.  
>   OR Enter a NEW config name which causes a new configuration to be created for the current/new project.
>
> Select a configuration in the selected project into which the settings will be imported.

Importing into a new configuration is the safest way to try an import, because your existing configurations are not changed.

##### Enter a name for the configuration to be saved.

Text box · Basic+ · `t_targetConfig`  
Needs: “A New/Existing Project and/or Configuration”

> Enter a name for the configuration to be saved.
>
> Note that only Roman/Latin names are supported using: a-z A-Z, 0-9, parentheses, underscores and hyphens.

The text part of the target **Configuration** box. No spaces. When you type a new name, PTXprint ticks **Everything** for you.

#### Pictures

##### Import Entire PicList "as is" (overwrite existing PicList)

Radio · Regular+ · `r_impPics_entire`  
Also: Import: Entire PicList "as is" (overwrite existing PicList) · Needs: “Pictures”

> Replace the target's whole picture list with the source's. Pictures only in the target are removed. Use it when the source is the master list.

Pictures that were only in the target are removed.

##### Import Elements of PicList (preserving existing PicList)

Radio · Regular+ · `r_impPics_elements`  
Also: Import: Elements of PicList (preserving existing PicList) · Needs: “Pictures”

> Keep the target's picture list and copy only the parts ticked below, for pictures in both lists.

The parts are captions, size and position, and copyright. **Add Any New Pictures** and **Remove Any Old Pictures** control which pictures are in the list.

##### Captions

Checkbox, off · Regular+ · `c_pic_Captions`  
Needs: “Import Elements of PicList (preserving existing PicList)”, “Pictures”

> Copy the captions and the reference shown with each picture. Leave unticked if the target is in another language.

Also copies the caption of the second text in a diglot. Unticked for another language because the captions would be in the wrong language.

##### Size, Position, Mirror, Rotation settings

Checkbox, on · Regular+ · `c_pic_SizePosn`  
Needs: “Import Elements of PicList (preserving existing PicList)”, “Pictures”

> Copy the size, position, scale, mirroring and rotation of each picture.

Useful when two projects share the same pictures and layout.

##### Copyright Information

Checkbox, on · Regular+ · `c_pic_Copyright`  
Needs: “Import Elements of PicList (preserving existing PicList)”, “Pictures”

> Copy the copyright (credit) information of each picture.

Copies the picture credits.

##### Add Any New Pictures

Checkbox, on · Basic+ · `c_impPicsAddNew`  
Needs: “Pictures”

> Add pictures that are in the source list but not yet in the target list.

Leave it ticked unless you want to keep exactly the pictures the target already has.

##### Remove Any Old Pictures

Checkbox, off · Basic+ · `c_impPicsDelOld`  
Needs: “Pictures”

> Remove pictures from the target list that are not in the source list. Tick it when the source list is the complete, final list.

Use it with a complete, final source list.

#### Styles

##### Override ALL Style Settings

Checkbox, off · Basic+ · `c_sty_OverrideAllStyles`

> Normally only styles that have not been changed in the receiving configuration will be imported. But if you require ALL styles to be updated regardless of whether they have already been modified locally, then enable this option. (This also applies to fonts in styles imported with Fonts+Script.)

Without it, your own style changes in the target are kept.

#### Other

##### Body Tab settings

Checkbox, on · Basic+ · `c_oth_Body`  
Needs: “Other”

> Import the settings of the Body tab.

Includes how books and chapters start, chapter and verse numbers, section headings, hyphenation, glossary markup, and similar.

##### Notes+Refs settings

Checkbox, on · Basic+ · `c_oth_NotesRefs`  
Needs: “Other”

> Import the settings of the Notes+Refs tab.

Footnotes, cross-references, note callers, note rules and study notes.

##### Header+Footer settings

Checkbox, on · Basic+ · `c_oth_HeaderFooter`  
Needs: “Other”

> Import the settings of the Header+Footer tab.

What is shown in the header and footer, and their positions.

##### Thumb Tabs settings

Checkbox, off · Basic+ · `c_oth_ThumbTabs`  
Needs: “Other”

> Import the thumb tab settings (Tabs+Borders tab).

Use it when two configurations or projects should have matching thumb tabs.

##### Overwrite Front Matter

Checkbox, off · Basic+ · `c_oth_OverwriteFrtMatter`  
Needs: “Front +Back Matter”, “Cover settings”, “Other”

> Replace the front matter in the target with the source's, instead of only adding the parts that are missing.

Leave it unticked if the target has its own front matter (for example in another language) that you want to keep.

##### Advanced settings

Checkbox, off · Basic+ · `c_oth_Advanced`  
Needs: “Other”

> This includes everything on the Advanced tab with the exception of Custom Script processing and Customized Styles (custom.sty).

Includes the changes file, the extra TeX files, and the extra style file (merged with the target's). For the custom script, tick **Custom Script**. custom.sty is not imported.

##### Cover settings

Checkbox, off · Basic+ · `c_oth_Cover`  
Needs: “Other”

> Import the cover settings, cover styles and the cover pages of the front matter.

Also turns on decorations, which the cover uses.

##### Front +Back Matter

Checkbox, off · Basic+ · `c_oth_FrontMatter`  
Needs: “Other”

> This includes most of the settings on the Peripherals tab, but not the Variables and Values. Front Matter and also Section Introductions are included in this.

Includes front and back PDFs, table of contents, front matter, colophon and section introductions, plus the source's front matter pages and any variables the target does not have yet. Existing variable values in the target are not changed.

##### Custom Script

Checkbox, off · Basic+ · `c_oth_customScript`  
Needs: “Other”

> This includes the Custom Script processing defined on the Advanced tab.
>
> Note that it is not possible to extract a custom script from a PDF file, which is why this option is sometimes disabled.

Includes whether the script is used and when it runs. PTXprint finds the script in the source (also inside a ZIP made with **Create Archive...**), copies it into the target configuration folder, and points the **Advanced** tab at the copy. For a Python script, other Python files it uses from the same folder are copied too. Greyed out (and unticked) when the source is a PDF.

##### Borders + Decorations

Checkbox, off · Regular+ · `c_oth_Decorate`  
Needs: “Other”

> This includes the various decorative borders and other ornamental features including section headers, end-of-book and verse number decorators.

Includes page borders and the book-title border.

##### Variables + Meta Data

Checkbox, off · Regular+ · `c_oth_Variables`  
Needs: “Other”

> Import the variables (Peripherals tab) and the publication details: copyright statement, licence, colophon and configuration notes. The book selection and any password are not imported.

Variables that the target is missing are also added by **Front +Back Matter**.

##### Texpert Hacks

Checkbox, off · Regular+ · `c_oth_Texpert`  
Needs: “Other”

> Import the expert TeX (TeXpert) settings.

Use it only if you know that the source used special TeX settings.

##### Finishing settings

Checkbox, off · Regular+ · `c_oth_Finish`  
Needs: “Other”

> This includes everything on the Finishing tab.

PDF output format, watermark, crop marks, grid, pages per sheet and sheet size, the compare-PDF settings, and whether settings are included in the PDF.


# 22. Help tab and getting support

## 22.1 What this tab is for

The **Help** tab is where you go when you need help, or need to find your files. It is shown in every view level.

On this tab you can:

* see where PTXprint keeps your PDF and other files, and open those folders;
* open the documentation, training material and the user community website;
* make an **archive** (a ZIP file) of your project to send to the support team;
* make a **report** about the last PDF, with warnings and errors;
* **Tidy Up** temporary files to save disk space;
* change the **Base Projects Directory** (the folder that holds your Paratext projects);
* open the **About** window to see which version of PTXprint you have.

Many links on this tab open web pages. They are only shown when internet use is allowed. If **Disable ALL Internet Use** is ticked on the **Advanced** tab, the internet links and the **About** button are hidden. Untick it to see them again. Some items are only shown in the **Full** view; this is noted for each one.

## 22.2 Links and Help

### Folders

* **Output PDF Location** – the folder where PTXprint saves the PDF files it makes. Click the blue link to open it.
* **Base Projects Directory** – the folder that holds all your Paratext projects. Use **Change...** to choose a different one.
* **PTXprint Program Path** (**Full** view only) – the folder where PTXprint itself is installed.

Everything in the output location is made again each time you print. None of it is part of Paratext Send/Receive. Your settings are kept safely in a different place, inside the project's shared folder.

### Documentation and learning

These links open web pages or documents:

* **Documentation | FAQs | Gallery | Support | Download** – the PTXprint home page. PTXprint does not update itself, so check here for new versions and download them yourself.
* **Learn: How to...** – short articles about common tasks.
* **Training (Videos and Presentations)** – videos on the Paratext website and on Vimeo, and a **Training Presentation** (a large set of Google Slides that trainers can use).
* **Ornaments Catalog** and **Technical Reference** (**Full** view only) – PDF documents that come with PTXprint. They open without internet.
* **Advanced Tech Docs** (**Full** view only) – technical documents for advanced users.
* **Support Agent** – an AI chatbot that answers questions about PTXprint.
* **The PTXprint User Community** – a website where you can ask questions and help other users.
* **Tell us what you think about PTXprint** – a short feedback form.
* **Report an Issue via GitHub** (**Full** view only) – for reporting bugs, if you have a GitHub account.

### Support tools

* **Create Archive...** – makes a ZIP file with everything needed to make your PDF again on another computer.
* **Create Report...** – makes a report page about the last PDF.
* **Tidy Up** – deletes temporary files.
* **About** – shows the version number and the names of the developers.

## 22.3 How to ask for help

If PTXprint does not do what you expect, you can get help here:

1. **Read this manual** and the **Common problems** sections in each chapter.
2. **Ask the Support Agent** (the AI chatbot link on the **Help** tab). It knows this manual and can answer many questions quickly.
3. **Ask the PTXprint User Community** (the community link on the **Help** tab). Other users and the developers read it.
4. **Email the support team** at **ptxprint_support@sil.org**.

### Before you write

* **Use the latest version.** Check the PTXprint home page. Your problem may already be fixed. The **About** button shows your version.
* **Make sure you can repeat the problem.** Note the exact steps: which project, which configuration, which book, and what you clicked.
* **Make the problem small.** If the problem is in one book, print only that book. If pictures are not involved, untick pictures for now.
* **Click Create Report...** and look at the warnings and errors. They may already tell you what is wrong.

### What to send to ptxprint_support@sil.org

Send one email with:

1. **A clear description of the problem.** What did you want? What happened instead? On which page and in which verse? Copy the exact text of any error message.
2. **Your PTXprint version** (from the **About** window) and your operating system (for example Windows 11).
3. **Screenshots.** One of the problem in the PDF, and one of the PTXprint setting you think is involved. Mark the problem area if you can.
4. **The archive ZIP file** made with **Create Archive...** (see below). With it, the support team can make exactly the same PDF on their computer.

### Making a good archive file

1. Select the project and configuration that shows the problem.
2. Choose only the book(s) needed to show the problem. One book is best.
3. If the problem has nothing to do with pictures, untick pictures. Pictures make the archive much larger.
4. On the **Help** tab, click **Create Archive...**.
5. Choose where to save the ZIP file, and click **Save**. PTXprint first prints the PDF again, then collects the files. This can take a while.
6. When it is finished, PTXprint opens the folder that contains the ZIP file.
7. Attach the ZIP file to your email.

The archive includes your settings, the USFM text of the selected books, the fonts, the pictures that are used, the PDF, and PTXprint's own typesetting files. Many email systems do not accept attachments larger than about 20 MB. If your ZIP file is too large, make it smaller (fewer books, no pictures), or share it through a file-sharing service and send the link.

The text of your project is inside the archive. If the text is sensitive, check with your project leader before you send it.

An archive is also useful as a long-term record of how a publication was made.

## 22.4 Log tab

The **Log** tab is not normally shown in PTXprint. To read the messages from the typesetting program, use the **XeTeX Log** tab on the **View+Edit** tab, or use **Create Report...**.

## 22.5 About dialog

The **About** window shows the PTXprint version number, the copyright, a link to the PTXprint home page, the list of developers, and the licence (MIT). Click **Credits** or **License** to see more, and **Close** to return. Give the version number when you ask for help.

The **About** button is only shown when **Disable ALL Internet Use** is unticked on the **Advanced** tab.

## 22.6 Common tasks

### Find the PDF that PTXprint made

On the **Help** tab, click the blue link next to **Output PDF Location**. The folder opens on your computer.

### Send a problem to the support team

1. Follow the steps in **Making a good archive file** above.
2. Email **ptxprint_support@sil.org** with a description, your version number, screenshots and the ZIP file.

### Check the last PDF for problems

1. Click **Print** to make the PDF.
2. On the **Help** tab, click **Create Report...**.
3. The report opens in your web browser. Look at the warnings (for example missing fonts, underfilled pages, or problem markers).

### Free up disk space

On the **Help** tab, click **Tidy Up**. PTXprint deletes the temporary working folders for all configurations of the current project. Your PDF files and settings are kept.

### Use projects from another Paratext folder

1. On the **Help** tab, click **Change...** next to **Base Projects Directory**.
2. In the **Choose Paratext Projects Folder** window, choose one of the folders that PTXprint found, or click **Browse for a different folder…**.
3. Choose the folder that *contains* your project folders, not a single project folder.
4. Click **Use Selected**. PTXprint goes back to the **Basic** tab. Choose a project from the new list.

### Show the internet links on the Help tab

1. Open the **Advanced** tab (shown in the **Regular** and **Full** views).
2. Untick **Disable ALL Internet Use**.
3. Return to the **Help** tab. The links are now shown.

## 22.7 Common problems

**The Help tab has very few links.**
**Disable ALL Internet Use** is ticked on the **Advanced** tab. Untick it to see the links. Some items (for example the **Technical Reference** and the **PTXprint Program Path**) are only shown in the **Full** view.

**A link opens the page in another language, or through Google Translate.**
When PTXprint is in a language other than English, some links go through Google Translate. Tick **Only Use English Links** on the **Advanced** tab to open the original English pages.

**Create Archive... takes a long time.**
PTXprint prints the whole job again before it makes the archive. Choose fewer books, or untick pictures, to make it faster and smaller.

**The archive ZIP file is too big to email.**
Archive only the book that shows the problem. Untick pictures if they are not part of the problem. If it is still too big, use a file-sharing service and send a link.

**"Cannot create Archive!" message.**
The ZIP file is open in another program, or you are saving over a file that is in use. Close the other program, or choose a different file name.

**Tidy Up shows a warning that some folders could not be deleted.**
A file in the folder is still open, for example the PDF in a PDF viewer. Close it and click **Tidy Up** again.

**PTXprint does not show my projects.**
The **Base Projects Directory** may point to the wrong folder. Click **Change...** and choose the folder that contains your Paratext projects.

## 22.8 Settings reference

### Help

#### Links and Help

##### Output PDF Location

Label · Regular+ · `l_working_dir`

> The PDF file created is stored in this folder (but should automatically open in your system's PDF viewer anyway).
>
> Note that ALL the files and subfolders in this location are TEMPORARY and can be deleted. None of these files are included in Paratext's Send/Recv data.

The folder is inside the project, in the local PTXprint folder. Click the blue link beside it to open it. **Tidy Up** deletes the temporary working files in its sub-folders.

##### Training (Videos and Presentations)

Label · not shown · `l_trainingVideos`

> There is a growing range of videos to teach you how to use some of the more advanced features of this very powerful software.

A heading for the training links. Only shown when internet use is allowed.

##### Videos via Paratext

Link · not shown · `lb_trainingOnPTsite`  
Also: Link to training videos on the Paratext website

> There is a growing range of videos to teach you how to use some of the more advanced features of this very powerful software.
>
> The videos on the Paratext site are high-quality and carefully curated, but they may not always cover the latest features available in PTXprint.

Opens the videos in your web browser. Only shown when internet use is allowed.

##### Report a Bug

Label · not shown · `l_reportBugs`

> Found a bug? If you have a GitHub account, report it here. Otherwise email ptxprint_support@sil.org.

A heading for the bug-report link. Only shown in the **Full** view, and only when internet use is allowed.

##### Report an Issue via GitHub

Link · not shown · `lb_reportBugs`  
Also: Link to report an issue with PTXprint

Opens a new issue form on GitHub. You need a GitHub account; without one, email ptxprint_support@sil.org. Only shown in the **Full** view, and only when internet use is allowed.

##### Documentation | FAQs | Gallery | Support | Download

Link · not shown · `lb_homePage`  
Also: Link to PTXprint home page

Opens the PTXprint home page, with documentation, FAQs, a gallery of examples, support information and downloads. Only shown when internet use is allowed.

##### PTXprint Home Page

Label · not shown · `l_homePage`

> PTXprint does not have an auto-updating feature, so you are encouraged to check for new updates at the Home Page. Please ensure you are using the latest version before reporting an issue.

A heading for the home page link. Visit the home page from time to time to download the newest version.

##### Reference Documentation

Label · Regular+ · `l_techFAQ`

> Reference documents for PTXprint:  
> the Ornaments Catalog, the Technical Reference (for advanced users) and, when online, the Advanced Tech Docs.

A heading for the reference documents. Only shown in the **Full** view.

##### Advanced Tech Docs

Link · not shown · `lb_techFAQ`  
Also: Link to deeper technical help

Opens the advanced technical documentation (on GitHub) in your web browser. It is for expert users and often describes things that cannot be set in the PTXprint window. Only shown in the **Full** view, and only when internet use is allowed.

##### PTXprint Program Path

Label · Regular+ · `l_ptxprintdir`

> Among other things, this folder contains:  
> * ReleaseNotes.txt  
> * AboutPTXprint.txt  
> * MIT License.txt

You normally do not need this folder, unless the support team asks for it. Only shown in the **Full** view.

##### Create Archive...

Button · Basic+ · `btn_createZipArchiveXtra`

> Create a ZIPped archive of all the files required to replicate this configuration. Useful for long-term archiving; but also helpful when availing technical support. The job is printed again first, so this may take a while.
>
> Keep the size to a minimum by turning off features (pictures?) that don't affect the issue being reported.
>
> Email the ZIPped archive file to:  
> mailto:ptxprint_support@sil.org

See **Making a good archive file** in this chapter for what to do before you click and what the archive contains.

##### The PTXprint User Community

Link · not shown · `lb_community`  
Also: Link to PTXprint user community site

Opens the PTXprint user community website, where you can search earlier questions, ask your own, and share tips. Only shown when internet use is allowed.

##### Got a Question? Get Help and Support from

Label · not shown · `l_community`

> Scripture Software Community site where you can interact with other PTXprint users and the developers.

A heading for the community link. A good place to ask "How do I…?" questions, because other users may have had the same question.

##### About

Button · not shown · `btn_about`  
Also: About PTXprint

> Discover more about PTXprint.

Opens the **About** window (see **About dialog** above). Only shown when internet use is allowed.

##### Tidy Up

Button · Basic+ · `btn_deleteTempFiles`  
Also: Delete temporary files and folders

> Delete the TEMPORARY working folders of ALL configurations of this project. This will not delete the resulting PDF files, but will save some space by deleting unneeded files.

Your settings are not deleted either. The next print takes a little longer, because PTXprint must make the working files again. If a file is still open in another program, PTXprint warns that some folders could not be deleted.

##### Give Feedback

Label · not shown · `l_giveFeedback`

> Psst! Can we have 5 minutes of your time? You could help us make PTXprint better!
>
> The developers of PTXprint would love to know how this tool is being used. What is your favorite feature? Are there any annoyances? Tell us what you like, or don't like. Tell us what you dream for in the future.

A heading for the feedback link. Only shown when internet use is allowed.

##### Tell us what you think about PTXprint

Link · not shown · `lb_giveFeeback`  
Also: Link to PTXprint Feedback Form (Google Form)

> Click this link to fill in the Google form or type this in a browser: http://tiny.cc/ptxprintfeedback

Opens the feedback form in your web browser. Only shown when internet use is allowed.

##### Videos via Vimeo

Link · not shown · `lb_trainingOnVimeo`  
Also: Link to training videos on the Vimeo platform

> There is a growing range of videos to teach you how to use some of the more advanced features of this very powerful software.
>
> The videos on Vimeo tend to be longer and more detailed, but less polished. However, these videos cover the latest available features.

Opens the videos in your web browser. Only shown when internet use is allowed.

##### Ornaments Catalog

Link · Regular+ · `lb_ornaments_cat`  
Also: Show the Ornaments Catalog

> Click to Open the Ornaments Catalog used for decorating the PDF (refer to the Tabs+Borders settings).

Shows all the decorative ornaments you can use on the **Tabs+Borders** tab. The file comes with PTXprint, so it opens without internet. Only shown in the **Full** view.

##### Technical Reference

Link · Regular+ · `lb_tech_ref`  
Also: Show the Technical Reference document

> Click to open the Technical Reference document. (For advanced users only).

The PDF comes with PTXprint and explains many settings in detail. Only shown in the **Full** view.

##### Learn: How to...

Link · not shown · `lb_learnHowTo`  
Also: Link to the Learn page with How To... articles

Opens the "Learn" page on the PTXprint website, with short How To... articles for common tasks. Only shown when internet use is allowed.

##### Technical Support

Label · Regular+ · `l_techSupport1`

> Before contacting support, make sure that it is possible to replicate the issue. Then use the "Create Archive..." button to make a ZIP file which needs to be emailed to:  
> mailto:ptxprint_support@sil.org

See **How to ask for help** in this chapter.

##### Create Report...

Button · Regular+ · `btn_generateReport`

> Generate a summary report with details about the PDF produced. This contains informational, warning and error messages about fonts, styles, layout and so on.

Opens the report in your web browser. Its sections include project overview, layout, USFM checks, fonts, writing system, peripheral components, output format, files and log analysis. Make the PDF first, so that the report is up to date. It is a good first check before you ask for help, and you can attach it to your email to the support team.

##### Support Agent

Link · not shown · `lb_chatBot`  
Also: Use the PTXprint Support Agent (AI chatbot) to answer your questions instantly

Opens the Support Agent in your web browser. Ask it questions in plain words, for example "How do I make the text two columns?". It answers quickly, but check its answers in PTXprint. Only shown when internet use is allowed.

##### Base Projects Directory

Label · Regular+ · `l_projects_dir`

> The folder that contains all your Paratext project folders. Use Change... to choose a different folder.

PTXprint lists the projects it finds in this folder on the **Basic** tab. Click the link beside it to open the folder.

##### Change...

Button · Regular+ · `btn_changeProjectsDir`

> Use this button to change the Base Projects Directory. For example, to use projects from a different version of Paratext.
>
> Do not select a specific project folder, but the parent folder which contains one or more projects.

Opens the **Choose Paratext Projects Folder** window. It lists the Paratext folders PTXprint found and says which ones contain projects. You can also browse for another folder. After the change, PTXprint returns to the **Basic** tab, so you can choose a project from the new list.

##### Training Presentation

Link · not shown · `lb_masterSlides`  
Also: Link to training presentation slides

> There is an extensive Google Slides presentation which can be used as a reference for training.

Opens the slides in your web browser. Trainers can use them to teach PTXprint. Only shown when internet use is allowed.

### Log

#### tv_logging

Text area · not shown · `tv_logging`

The text area on the **Log** tab, which is not normally shown. See **Log tab** above.


# 23. How do I...? (step-by-step tasks)

## 23.1 How to use this chapter

This chapter gives short, step-by-step answers to the questions people ask most often. A task often uses more than one tab. **See also** names the chapter with more detail.

For every task:

* Most changes appear in the PDF only after you click **Print (Make PDF)** again.
* Lower **view levels** hide many settings. If you cannot see a tab or setting, click **☰** (top-right) › **View Level** › **Full View**, or type its name in the **Search for settings** box (bottom-left).
* Click **Save** before you change to another configuration. PTXprint does not save the current configuration when you choose another one.
* "pt" means point. 1 pt is about 0.35 mm.

## 23.2 Printing: what goes into the PDF

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

## 23.3 Page size, margins and columns

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

## 23.4 Fonts and text size

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

## 23.5 Scripts, languages and hyphenation

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

## 23.6 Making the text fit

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

## 23.7 Scripture text: headings, numbers and other content

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

## 23.8 Footnotes and cross-references

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

## 23.9 Pictures and maps

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

## 23.10 Diglot (two texts side by side)

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

## 23.11 Thumb tabs, borders and decorations

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

## 23.12 Front matter, back matter and covers

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

## 23.13 Headers, footers and page numbers

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

## 23.14 Fixing the page layout

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

## 23.15 Preparing the PDF for a printer

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

## 23.16 Configurations and settings

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

## 23.17 Finding settings and getting help

### How do I find a setting that I cannot see?

1. Click in the **Search for settings** box at the bottom-left (or press **Ctrl+F**).
2. Type a word, for example `margin` or `footnote`, and press **Enter**.
3. Click the setting in the list. PTXprint opens the right tab, highlights the setting, and raises the view level if needed.

See also: Main window.

### How do I see more (or fewer) settings?

Click **☰** (top-right) › **View Level** › **Mini View**, **Basic View**, **Regular View** or **Full View**.

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


# 24. Problems and solutions

## 24.1 How to use this chapter

This chapter lists common problems, grouped by kind, in the words users often use. Each has **Why this happens** and **What to do**.

First try these three quick checks. They solve many problems:

1. **Print again.** Most changes appear in the PDF only after you click **Print (Make PDF)**.
2. **Check the view level.** A setting can be hidden but still turned on. Click **☰** › **View Level** › **Full View** to see every setting.
3. **Check the configuration name.** Look at **Name** on the **Basic** tab. Is it the configuration you think it is?

"pt" means point. 1 pt is about 0.35 mm.

## 24.2 Printing fails or no PDF appears

### Nothing happens when I click Print, or the status line says "No books to print"

**Why this happens:** No book is selected, or the book list is empty.

**What to do:**

1. On the **Basic** tab, in **What to Print**, click **Single Book** and choose a book. Or click **Select Multiple Books...**, choose books and click **OK**.
2. Print again.

### The status line says "One of more fonts have not been set yet"

**Why this happens:** No font has been chosen for the main text.

**What to do:** On the **Fonts+Script** tab, click **Select Font...** next to **Regular**, choose a font, and print.

### The status line says "Printing busy"

**Why this happens:** PTXprint is still making a PDF.

**What to do:** Wait until the progress bar has finished, then print again.

### PTXprint says "Cannot update PDF file while it is locked!"

**Why this happens:** The old PDF is open in another program (for example Adobe Reader), so PTXprint cannot replace it.

**What to do:**

1. Close the PDF in the other program and click **Yes** to try again.
2. To avoid this, click **☰** › **Show PDF** › **Preview Pane**. The preview does not lock the file.

### The Print (Make PDF) and Save buttons are greyed out

**Why this happens:** PTXprint cannot print yet. For example, no project is selected, or a diglot row has no project or configuration.

**What to do:**

1. Read the message in the status line above the bottom bar.
2. Choose a project on the **Basic** tab.
3. For a diglot, check that every row on the **Diglot** tab has a **Project** and a **Configuration**.

### An error window says "Failed to create: … .pdf"

**Why this happens:** The typesetting program stopped because of an error. The window shows the last lines of the log and often a hint. The hint is the most useful part (see the table below).

**What to do:**

1. Find the hint in the table below and follow the advice.
2. Note any "References to check" or "File(s) to check" at the end of the message. They tell you where to look.
3. If you changed a setting just before the error, change it back and print again.
4. For more detail, open the **View+Edit** tab, **XeTeX Log** sub-tab, and scroll to the end. Error lines start with `!`.
5. If you still cannot fix it, click **Tidy Up** on the **Help** tab and print again. If that does not help, send an archive (**Create Archive...** on the **Help** tab) to support.

| Hint in the error window | What it usually means | What to do in PTXprint |
|---|---|---|
| "Cannot find the Font specified. Install it, restart PTXprint and try again" | A font in the configuration (on **Fonts+Script**, or in a style) is not installed. The message may name the marker that uses it. | Install the font for all users and restart PTXprint. Or choose an installed font on **Fonts+Script**, or in the named style on the **Styles** tab. |
| "Fallback Font issue - set a font on the Fonts+Scripts tab" | **Use Fallback Font** is ticked, but no valid fallback font is chosen. | On **Fonts+Script**, choose a fallback font, or untick **Use Fallback Font**. |
| "Fallback font probably being applied to text in a footnote (not permitted!)" | A character that needs the fallback font is in a footnote. | Choose a Regular font that has the character, or remove it from the fallback character list. |
| "Check if picture file is located in 'Figures', 'local\figures' or a specified folder" | A picture file cannot be found or loaded. | On the **Pictures** tab, look for grey rows and fix the file name or folder. Or tick **Omit Missing Pictures**. |
| "Check if image/PDF file is available on the system" | A front or back matter PDF, a watermark PDF or a picture is missing. | Check **Front Matter PDF(s)** and **Back Matter PDF(s)** (**Peripherals**) and **Apply Watermark PDF** (**Finishing**). Choose the file again with **Select...**, or untick the option. |
| "This might be related to a USFM marker error (using an unsupported marker)" | A marker in the text is wrong or unknown, or a line in a mods file is wrong. | Run **Basic Checks** in Paratext. If you edited `ptxprint-mods.tex` (**Advanced** tab), untick **Apply Customized Settings (ptxprint-mods.tex)** and print again. |
| "Failed due to an error in the generated USFM file. Run the Basic Checks in Paratext" | The text has a marker error that PTXprint cannot process. | Run **Basic Checks** in Paratext and fix the errors. If you use a changes file (**Advanced** tab), check the last rule you added. |
| "Uh oh! You've pushed TeX too far! Try turning Hyphenation off" | The job is too big, often because of a very long hyphenation list. | On **Fonts+Script**, untick **Hyphenate**, or make a shorter list with **Limit Hyphenation List to Words Found in**. Print fewer books at once. |
| "Possible fault in the hyphenation file" | The hyphenation list has a bad entry. | Untick **Hyphenate** on **Fonts+Script**. Click **Create List...** to make the list again. |
| "You may have too many paragraphed footnotes on the page" | Too many run-on footnotes on one page. | On **Notes+Refs**, tick **Start Each Footnote on a New Line**. |
| "Possibly a missing +/- value in the Adjust List" or "Check for errors in the Adjust List" | A row in the paragraph adjustment list has a wrong value. | On **View+Edit**, **Adj List** sub-tab, check the **Stretch** column. Each value must start with `+` or `-`. Delete the bad row if you are not sure. |
| "One of the settings in the Stylesheet may be missing the units" | A value in a style or an extra stylesheet is not valid. | Undo your last change on the **Styles** tab. On the **Advanced** tab, untick extra stylesheets (**custom.sty**, **ptxprint-mods.sty**) one at a time to find the problem. |
| "Font size setting issue. Check to see if the font size in a style … is incorrect (maybe it is set to 0.00)" | A style near the reference in the message has font size 0. | On the **Styles** tab, set that style's **Font Size Factor** to a normal value, or click its Reset button. |
| "Expecting a number for \Color definition, not a color name" | A colour in a style was written as a word. | On the **Styles** tab, choose the colour again with the **Color** button. |
| "Problem with Formatting Intro Outline" | The right-aligned outline references cause a problem. | On the **Body** tab, untick **Right-align \ior With Tabbed Leaders**. |
| "Sorry! XeTeX was unable to complete the typesetting" | The typesetter could not place the text on a page. Common in diglots, or when a forgotten feature is on. | For a diglot, first print each text on its own. Check tabs with blue names (for example **Pictures**, **Diglot**, **Tabs+Borders**) and turn off features you do not need. Look for very large pictures. |
| "To fix this error: Use a different font which is not a Variable Font" | The font is a "variable font", which PTXprint cannot use. | Choose a normal font on **Fonts+Script**. |
| "Bad xdvi file, probably failed to load a picture or font" | A picture or font could not be loaded when the PDF was written. | Check missing pictures on **Pictures** and the fonts on **Fonts+Script**. |
| "Possibly a faulty installation" | Files that come with PTXprint are missing. | Install PTXprint again. |
| "Oops! Something unexpected happened…" or "Probably a TeX macro problem" | PTXprint does not recognise the error. | Click **Tidy Up** (**Help** tab) and print again. If it still fails, send an archive to support and say which setting you changed last. |

### PTXprint says "PDF was created BUT… Layout problems were encountered on page(s)…"

**Why this happens:** The PDF was made, but on the listed pages the typesetter had to break its own rules. Text may run over the bottom margin, or a picture may be lost.

**What to do:**

1. Look at the listed pages in the PDF.
2. If there is a large picture on or near that page, make it smaller (**Scale** on the **Pictures** tab) or move it (change the **Anchor Ref**).
3. If you adjusted paragraphs on those pages, reset them: in the **PDF Preview** window, right-click a paragraph › **Reset Adjustments** › **Page**.
4. Print again.

### The status line says "Rerun to fix: …"

**Why this happens:** Some things depend on page numbers (the table of contents, picture credits, margin notes), and PTXprint learned new page numbers during this run. Most common with **Quick Run** ticked.

**What to do:** Untick **Quick Run** at the bottom of the window, and print again.

### PTXprint says "Unknown book code"

**Why this happens:** The book list has a word that is not a 3-letter USFM book code, for example `John` instead of `JHN`.

**What to do:** On the **Basic** tab, correct **Portions or Multiple Books** with codes such as `MAT`, `JHN`, `1CO`. Or click **Select Multiple Books...** and click the books.

### Printing takes a very long time

**Why this happens:** Some settings need much extra work: a **PDF Output Format** other than **Screen**, **Compare PDFs**, Strong's numbers in the text, very large cross-reference lists, many high-resolution pictures, or a whole Bible.

**What to do:**

1. While you work, tick **Quick Run** at the bottom of the window.
2. On the **Finishing** tab, use **Screen (Quickest)** until the final PDF. Untick **Compare PDFs** when you do not need it.
3. On the **Pictures** tab, choose **Low Resolution (Smaller File)** or **Use Place-holders** while you work.
4. Print one book at a time, or use **SpeedSlice** in the **PDF Preview** window for long books.

## 24.3 The PDF does not change

### I changed a setting, but the PDF looks the same

**Why this happens:**

* You did not print again, or the last print failed. The preview still shows the old PDF.
* The PDF is shown in another program that has not reloaded it.
* Another setting overrides yours (for example a style, or an extra stylesheet).
* You changed a different configuration, or the secondary text of a diglot.
* **Layout Only** is ticked, so PTXprint did not process the text again.

**What to do:**

1. Print and wait for it to finish. The date and time in the title bar of the **PDF Preview** window must be the time of your last print.
2. If an error message appeared, fix that first. The old PDF stays on the screen when printing fails.
3. Check **Name** on the **Basic** tab.
4. For a diglot, see "My change has no effect in a diglot" below.
5. Untick **Layout Only** and **Quick Run**, and print again.
6. For style and font changes, see "My change on the Styles tab has no effect" below.

### My text changes in Paratext do not appear in the PDF

**Why this happens:** Normally PTXprint notices that the text changed. With **Layout Only** ticked, it may not process the text again. Picture captions come from PTXprint's own picture list.

**What to do:**

1. Save the text in Paratext.
2. Untick **Layout Only** and print.
3. For picture captions, click **Refresh List** on the **Pictures** tab.
4. If you use **SpeedSlice**, make sure it is not hiding the part that you changed.

### My changes are not kept after I close PTXprint, or Save does nothing

**Why this happens:** **Quit** does not save. Or the configuration is locked. A locked configuration is never saved, not even when you print.

**What to do:**

1. Click **Save** (or **Print (Make PDF)**) before **Quit**.
2. If **Save**, **Delete** and **Notes** are greyed out, the configuration is locked. On the **Basic** tab, click the lock button and type the password.
3. Or click **Save As** and make a new, unlocked configuration.

### The PDF has only a few chapters, or it starts in the middle of a book

**Why this happens:** **SpeedSlice** is still on. Or **From Chapter** and **To** limit the chapters.

**What to do:**

1. In the **PDF Preview** window, right-click a `\p` or `\m` paragraph, choose **SpeedSlice** and click **Disable**.
2. On the **Basic** tab, check **From Chapter** and **To**, and print again.

## 24.4 Text and fonts

### Some letters print as empty boxes (☐) or question marks

**Why this happens:** The font has no shape for these characters.

**What to do:**

1. On the **Fonts+Script** tab, tick **Use Fallback Font** (Regular and Full views).
2. Click **Find Missing Characters** to see which characters are missing.
3. Click **Select Font...** next to the list and choose a font that has them.
4. Or choose a **Regular** font that supports your whole alphabet.
5. If only numbers are boxes, check **Digit mapping** in the **Pick a Font** dialog. Set it to **Default** if the font has no digits for that script.
6. In the **PDF Preview** window, tick **Layout Analysis**. Purple marks show missing characters.

### Bold or italic text looks fake (thick, blurred or slanted wrongly)

**Why this happens:** The font family has no real bold or italic typeface, so PTXprint makes one from the regular letters. The button on the **Fonts+Script** tab shows the style in brackets, for example *(bold)*.

**What to do:**

1. On the **Fonts+Script** tab, click **Select Font...** for **Regular** and choose a family shown in **bold** in the list. These families have all four typefaces.
2. Or click **Select Font...** for **Bold** or **Italic** and choose a real bold or italic font.
3. Or, in **Pick a Font**, change **Embolden** and **Slant** to improve the fake style.

### Some text is in the wrong font

**Why this happens:** The style for that text has its own font, or the characters come from the fallback font. In a diglot, the header can use the font of the other text.

**What to do:**

1. On the **Styles** tab, find the marker. A bold **Font** label means the style has its own font. Click the bold label to go back to the main font.
2. On the **Fonts+Script** tab, check **Use Fallback Font** and the characters in its list.
3. In a diglot, on the **Header+Footer** tab, choose **Pri** or **Sec** for each part of the header.
4. If you chose a new **Regular** font, check **Bold**, **Italic** and **Bold Italic** again.

### My font is not in the list

**Why this happens:** The font is not installed, or only for one user, or PTXprint has not refreshed its list.

**What to do:**

1. Install the font for all users.
2. On the **Fonts+Script** tab, click **Refresh Font List**.
3. If it is still missing, restart PTXprint.

### Letters do not join, or vowel marks are in the wrong place

**Why this happens:** **Text Script** is wrong, or the font needs Graphite.

**What to do:**

1. On the **Fonts+Script** tab, set **Text Script** to your script.
2. For a Graphite font, click **Select Font...** for **Regular**, tick **Graphite Rendering**, and click **OK**. Then print.

### Hyphenation does not work

**Why this happens:** There is no hyphenation list, the list is empty, **Hyphenate** is not ticked, or **Between Letters** spacing is on.

**What to do:**

1. On the **Fonts+Script** tab, click **Create List...** and read the message. It says how many words were used.
2. If the number is 0, untick **Only Use Approved Hyphenation Words** and click **OK** again, or approve words in the Paratext Wordlist.
3. Tick **Hyphenate**. Make sure **Between Letters** in **Spacing Adjustments** is unticked. Then print.

### Long lines do not break in Thai, Khmer, Myanmar, Chinese or similar scripts

**Why this happens:** PTXprint does not know where it may break a line.

**What to do:**

1. On the **Fonts+Script** tab, set **Text Script** to your script.
2. Tick **Specify Line Break Locale** and type the language code, for example `th`, `km`, `my` or `zh`.
3. Or mark the break points with `/` in the text (Thai, Lao, Myanmar, Tai Tham, New Tai Lue).

### Coloured text prints in black

**Why this happens:** **Enable Colored Text (as Specified in Stylesheet)** is not ticked, or **PDF Output Format** is **Print-Gray (B/W)**.

**What to do:** Tick **Enable Colored Text (as Specified in Stylesheet)** on the **Fonts+Script** tab, and check **PDF Output Format** on the **Finishing** tab.

### My change on the Styles tab has no effect

**Why this happens:** You changed a different marker or level (for example `s1` instead of `s2`). Or another style or stylesheet wins. Or a setting on another tab controls it.

**What to do:**

1. Check which marker the text really uses. On the **Styles** tab, click the filter button next to **Find** to show only markers used in your books.
2. `\p` gets its size and line spacing from the **Layout** tab (**Base Font Size** and **Base Line Spacing**).
3. If you chose **Justified** but the text is ragged, tick **Justify Paragraphs** on the **Body** tab.
4. On the **Advanced** tab, check **Apply Stylesheet Overrides (ptxprint-mods.sty)**. It is applied last and may set the same value.
5. Print again.

### Some text is missing from the PDF

**Why this happens:** A setting removes it. For example **Include Contents of Marker** is unticked for its style, or a **Body** tab setting removes headings, introductions or empty verses.

**What to do:**

1. On the **Styles** tab, a marker with a line through it is not printed. Tick **Include Contents of Marker**.
2. On the **Body** tab, check **Book Introductions**, **Introductory Outlines**, **Include Scripture Text**, **Headings**, **Parallel Passage Refs** and **Hide Empty Verses**.
3. For study notes, tick **Extended Footnotes (\ef)** on the **Notes+Refs** tab (Full view).

## 24.5 Layout and spacing

### There is white space at the bottom of every page

**Why this happens:** The text area does not hold a whole number of lines. The left-over part of a line is empty on every page.

**What to do:**

1. On the **Layout** tab, look at **Lines Per Page** (Regular and Full views). If it is red, this is the cause.
2. Click **one** fine-tune button: next to **Base Line Spacing (pt)**, or next to the top or bottom margin.
3. The number turns blue. Print again.

### Some pages or columns end early, with empty lines at the bottom

**Why this happens:** With **Align Text to Baseline**, all lines sit on a fixed grid. The typesetter will not leave one line of a paragraph alone at the top or bottom of a page, keeps a heading with the next lines, and keeps pictures and notes with their verse. So a page sometimes ends one or more lines early.

**What to do:**

1. Do this last, when all other settings are final.
2. In the **PDF Preview** window, right-click a paragraph on this page or the page before and choose **Try Shrink -1 line** to pull text up. Or choose **Expand +1 line** on the page before to push a line down.
3. Or use the **Auto Page Fill** tool (the lightning icon in the **PDF Preview** window).
4. If a picture is near the gap, move it or make it smaller.
5. In poetry books such as Psalms, try **Optimize Layout for Poetry Books** on the **Body** tab (see "Optimize Layout for Poetry Books has no effect").
6. For a quick draft, move the switch on the **Layout** tab to **Variable Line Spacing**. This fills the columns, but the lines no longer line up on both sides of the paper.

### The last page of a book has only a few lines

**Why this happens:** The book is just a little too long to end on the page before.

**What to do:**

1. In the **PDF Preview** window, find paragraphs in the last few pages whose last line is short.
2. Right-click each one and choose **Try Shrink -1 line** (or **Shrink Both**) until the lines move back. Or use the **Auto Page Fill** tool.
3. If many lines must move, make a small change for the whole book (for example a slightly smaller **Base Font Size**, or **Min/Shrink** in **Spacing Adjustments** on **Fonts+Script**). Then check all pages again.
4. To let the next book start on the same page, set **Where to start a new book** to **Same page** (**Advanced** tab, **Other** sub-tab, **Page Layout and Spacing**).

### I asked to shrink a paragraph, but nothing changed

**Why this happens:** The paragraph has no room to lose a line (common for short paragraphs, or when the last line is almost full). Or the PDF has not been updated yet.

**What to do:**

1. Wait a few seconds if **Auto-update** is ticked, or click **Print (Update PDF)**.
2. Right-click again and choose **Shrink Both**.
3. Or try a longer paragraph on the same page, or on the page before.

### Fixing one page broke a later page

**Why this happens:** Every change moves all the text after it.

**What to do:**

1. Make all other layout changes (fonts, margins, pictures) **before** you adjust paragraphs.
2. Work from the front of the book to the back. Fix the first problem page, then use **Locate the next issue** in the **PDF Preview** window.

### Text looks squashed, stretched or has big gaps between words

**Why this happens:** Paragraph adjustments or the page filler made the letters narrower or wider. Or the word spacing range is too wide. Or **Keep Repeated Words Together** or **Prevent Orphan Words** forces bad line breaks.

**What to do:**

1. In the **PDF Preview** window, tick **Adjustments** to see changed paragraphs (coloured bars). Reset the worst ones (right-click › **Reset Adjustments** › **Paragraph**).
2. On the **Advanced** tab, **Other** sub-tab, **Preview Pane: Adjustment and Analysis Settings**, raise **Minimum Text Shrink** (for example to 97%) and lower **Maximum Text Expand** (for example to 103%).
3. On the **Fonts+Script** tab, check **Between Words** in **Spacing Adjustments**. A very high **Max/Stretch** allows big gaps.
4. Turn on hyphenation to give the lines more break points.

### Almost everything on the Layout, Fonts+Script and Styles tabs is greyed out

**Why this happens:** **Lock UI Layout Settings** is ticked.

**What to do:** Change to the **Full** view. On the **Advanced** tab, **Main** sub-tab, **General** area, untick **Lock UI Layout Settings**.

### The font size changed when I changed the line spacing (or the other way round)

**Why this happens:** **Lock Ratio** is ticked on the **Layout** tab. It keeps the two numbers in the same proportion.

**What to do:** Untick **Lock Ratio**, then type the font size and line spacing you want.

### The header or footer is cut off, or too close to the edge of the paper

**Why this happens:** The header and footer sit inside the top and bottom margins. A large gap between the header and the text moves the header towards the edge.

**What to do:**

1. On the **Layout** tab, look at the blue numbers in the margin picture.
2. Make **Start of Page to Top of Text (mm)** (or **Bottom of Text to End of Page (mm)**) larger.
3. Or make **Bottom of Header to Top of Text (pt)** (or **Bottom of Text to Top of Footer (pt)**) smaller.

### My PDF suddenly looks different, but I did not change anything on the main tabs

**Why this happens:** An **Advanced** tab setting may have changed, or an extra file (changes file, mods file) may be on. Someone on the team may have changed the configuration through Paratext Send/Receive.

**What to do:**

1. On the **Advanced** tab, **Other** sub-tab, click the filter button. Only groups with changed settings are shown, with **bold** labels.
2. On the **Main** sub-tab, check which boxes are ticked in **Text Processing & Stylesheets**.
3. Check the **Notes** box on the **Basic** tab for comments from the team.

### Coloured marks, bars or codes appear in the margins of my PDF

**Why this happens:** A proof-reading option is on.

**What to do:**

1. On the **Advanced** tab, **Other** sub-tab, **PDF Options, Covers, Show/Hide**, untick the "show" options (for example **Show adjust points**, **Show USFM codes**, **Show Error Bars For Overfull Lines**, **Mark Trigger Points**).
2. In the **Diglot** group, untick **Show Diglot Trace Marks**.

The coloured bars and boxes in the **PDF Preview** window (**Adjustments**, **Paragraph Boxes**, **Layout Analysis**) are only on the screen, not in the PDF.

### "Optimize Layout for Poetry Books" has no effect

**Why this happens:** It only works for the books listed beside **Use Special Features for These Books** on the **Body** tab, while that box is ticked. With an empty list, nothing is optimized.

**What to do:** Change to the **Full** view. Tick **Use Special Features for These Books** and type the book codes (for example `PSA PRO`) in its list.

## 24.6 Pictures

### No pictures appear in the PDF

**Why this happens:** Pictures are off, or the picture list (PicList) is empty, or place-holders are used.

**What to do:**

1. On the **Pictures** tab, **Global Options**, tick **Include Pictures (illustrations)**.
2. Change to the **Regular** view to see the picture table. If it is empty, click **Generate...**. PTXprint uses only the pictures in its list, not the `\fig` lines in Paratext directly.
3. Make sure **Use Place-holders (Smallest PDF File)** is not chosen.
4. On the **Details** sub-tab, check that **Print** is ticked under **Media**.

### Some pictures are missing

**Why this happens:** PTXprint cannot find the picture file (grey row in the table), or the picture's book is not being printed, or **Image Types** excludes the file type.

**What to do:**

1. On the **Pictures** tab, look for grey rows and check the **Filename**.
2. Put the file in the project's `figures` or `local\figures` folder, or tick **Use Other Location** and choose the folder with **Picture Folder...**. If the file is in a subfolder, make sure **Exclude Subfolders** is unticked.
3. Clear the **Image Types** box if it only lists some types.
4. After printing, check the missing-pictures count and list on **Global Options**. **Omit Missing Pictures** skips missing files without an error, so it can hide the problem.

### A picture is on the wrong page or in the wrong place

**Why this happens:** A picture goes on the page of its anchor verse only if there is room. Otherwise it moves to a later page. Large pictures move more often.

**What to do:**

1. In the **PDF Preview** window, right-click the picture, choose **Change Anchor Ref**, and choose a verse a little earlier (or later).
2. Or right-click and choose another **Vertical Position** or **Horizontal Position**.
3. Make the picture smaller with **Shrink by 1 line**, or with **Scale** on the **Pictures** tab, **Details** sub-tab. Then print.

### A picture row is red in the table

**Why this happens:** At this size and scale the picture is too tall for the page.

**What to do:** On the **Details** sub-tab, make **Scale** smaller, or change **Frame Size** from **Span Width** to **Column Width**.

### I cannot choose the picture position I want

**Why this happens:** The position lists depend on each other. For example, **Span Width** only allows **Top**, **Bottom** and **Below Notes**, and no horizontal position.

**What to do:** Choose **Frame Size** first, then **Vertical Position**, then **Horizontal Position**.

### My caption changes in Paratext do not show

**Why this happens:** PTXprint keeps its own copy of the captions in the picture list.

**What to do:** On the **Pictures** tab, click **Refresh List** (size and position settings stay the same), and print.

### The picture credits are missing or wrong

**Why this happens:** The colophon or front matter has no `\zimagecopyrights`, or a picture is not from a known illustration series, or the page numbers are not yet known.

**What to do:**

1. On the **Peripherals** tab, tick **Colophon at End of Publication** and check that its text contains `\zimagecopyrights`. Or put `\pc \zimagecopyrights` in the front matter.
2. On the **Pictures** tab, **Details** sub-tab, type the credit in **Copyright Attribution** for pictures that do not show **Automatic**.
3. Print twice.

### My picture checks, credits or notes are gone

**Why this happens:** In older PTXprint versions, the **Checklist** answers, credits and picture notes were not read back when a configuration was opened. Saving could then overwrite them. This is fixed now, but answers lost before the fix cannot be recovered.

**What to do:** On the **Pictures** tab, **Checklist** sub-tab (and **Copyright Attribution** on **Details**), enter the lost answers again. They are now kept.

### The message "Image Anchor Not Found" appears when I right-click a picture

**Why this happens:** PTXprint cannot match the picture in the PDF to a row in the picture list, for example after the list changed.

**What to do:** Print again so the preview matches the picture list. Then make the change on the **Pictures** tab, **Details** sub-tab.

## 24.7 Notes and cross-references

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

**What to do:** On the **Notes+Refs** tab, tick **Override hidden/automatic Footnote caller settings** (or the cross-reference version), and print.

### The cross-reference placement changed by itself

**Why this happens:** PTXprint keeps the footnote and cross-reference placements in step. For example, **End of Column** for one changes the other too.

**What to do:** After you change one placement, check both the **Footnotes** and the **Cross-References** sub-tabs.

### Changing the cross-reference rule settings does nothing

**Why this happens:** PTXprint draws only one rule above the notes at the bottom of the page. It uses the footnote rule settings, unless the footnotes are at the **End of Book**.

**What to do:** Change the rule on the **Footnotes** sub-tab instead.

### The footnotes run into the footer

**What to do:** On the **Notes+Refs** tab, **Footnotes** sub-tab, make **Space Above Rule** larger. Or, on the **Layout** tab, make **Bottom of Text to Top of Footer (pt)** larger.

### Margin notes do not appear

**Why this happens:** **Margin Notes Col Width (mm)** on the **Layout** tab only makes the space. The notes must also be sent there.

**What to do:**

1. On the **Notes+Refs** tab, set **Placement of Footnotes** (and/or **Placement of Cross-References**) to **Side Margin**.
2. For headings in the margin, tick **In Margin** on the **Body** tab.

### The external cross-references show the wrong book names

**Why this happens:** PTXprint uses the short book names from the Paratext project's **Scripture Reference Settings** (these should match the `\toc3` lines).

**What to do:** Correct the book names in Paratext, and print again.

## 24.8 Diglot

### My change has no effect in a diglot

**Why this happens:** Each text has its own configuration. The second text's fonts, font size, styles and notes come from its own (secondary) configuration. Page settings (page size, margins, header and footer positions, the footnote rule and others) always come from the primary configuration.

**What to do:**

1. For the second text's fonts, styles or notes: on the **Diglot** tab, right-click its row and choose **Edit Settings…**. Make the change, then click **Return to Primary**.
2. For page size, margins or headers: make sure you are in the primary configuration (the big button says **Print (Make PDF)**, not **Return to Primary**).
3. Print from the primary configuration.

### The big button says "Return to Primary" instead of "Print"

**Why this happens:** You are in the secondary configuration of a diglot (after **Edit Settings…**).

**What to do:** Click **Return to Primary**, then **Print (Make PDF)**. (The small **Print** button prints only the secondary text.)

### PTXprint says "These books are not available in the secondary diglot project"

**Why this happens:** You selected a book that the second project does not have.

**What to do:** On the **Basic** tab, select only books that are in every project of the diglot.

### PTXprint says "Failed to merge texts due to a Syntax Error" (Diglot Merge Error)

**Why this happens:** One of the texts has a marker error.

**What to do:**

1. Run **Basic Checks** in Paratext for every project in the diglot, and fix the errors.
2. If you use a changes file (**Advanced** tab), check that a rule has not caused the error.
3. Print each text on its own first, then the diglot.

### The status line says "No Config found for diglot", or Print is greyed out

**Why this happens:** A row on the **Diglot** tab has no project or configuration.

**What to do:** On the **Diglot** tab, choose a **Project** and then a **Configuration** in every row.

### The diglot columns have big gaps, or the texts do not line up well

**Why this happens:** One text needs more space than the other.

**What to do:**

1. Give the longer text more **% Width** (for example 55 and 45), or a smaller font size or line spacing in its row.
2. Try **Auto-calculate optimum widths of diglot columns** with one short book selected (two texts only).
3. Try another **Merging mode**, for example **Scored (Chapter)** or **Chapter Verse**.
4. Then try the **Auto Page Fill** tool in the **PDF Preview** window (experimental for diglots and polyglots).

### The secondary caption is missing under a picture

**Why this happens:** **Captions** is not ticked in that text's row, or the texts use different picture files or verses, so the picture is not shared. Pictures are never shared in the books listed in **Use Serial Layout for These Books**.

**What to do:** On the **Diglot** tab, tick **Captions** in that text's row. Check that both texts use the same picture file at the same verse.

### The % Width numbers are red

**Why this happens:** The widths of the texts on one page do not add up to 100.

**What to do:** Change the numbers, or right-click a row and choose **Distribute Widths**.

### I cannot untick Diglot (or Polyglot)

**Why this happens:** This is on purpose, so that you do not lose your diglot settings. PTXprint opens the **Save As Monoglot** dialog instead.

**What to do:** Type a new configuration name and click **OK**. PTXprint opens a one-text copy. The diglot configuration stays as it was.

### Two Column Layout on the Layout tab is greyed out

**Why this happens:** A diglot always uses columns, so PTXprint ticks this box and locks it while the diglot is on.

## 24.9 Headers, footers and page numbers

### There is no header on the first page of a book

**Why this happens:** This is normal. PTXprint prints no header (or header rule) on the page where a book starts.

**What to do:** For a page number on that page, tick **Print Page Number at Bottom of Intro Page(s)** on the **Header+Footer** tab (Regular and Full views).

### The header references are empty on some pages

**Why this happens:** This is normal on pages without verses, for example introduction or glossary pages.

### The header shows the last verse where I expected the first verse

**Why this happens:** **Mirror Pages** is ticked on the **Layout** tab. On left-hand pages PTXprint swaps **First Reference** and **Last Reference**, and also **Inner** and **Outer**.

**What to do:** Choose the other item on the **Header+Footer** tab. Or untick **Mirror Pages** if every page should look the same.

### My own header text prints wrongly, or the PDF fails after I typed a header

**Why this happens:** In the header and footer boxes, spaces and the characters `# % & ^ ~ \` need a backslash before them.

**What to do:** Type `\ ` (a backslash and a space) for each space, for example `DRAFT\ \isodate`. Type `\#`, `\%` and so on for those characters.

### The footer shows "<Enter ID>" instead of the time

**Why this happens:** Older PTXprint versions saved the footer item **Time (HH:MM)** wrongly.

**What to do:** Update PTXprint. Configurations with this problem are corrected when they are opened. Then print again.

### The page numbers do not start at the number I set

**Why this happens:** **Starting Page Number (for Scripture Books)** applies at the first Scripture book when the front matter uses its own page numbering. If the front matter uses normal page numbers, numbering continues from the front matter.

**What to do:** Check the page number codes (`\nopagenums`, `\resetpagenums`, `\dopagenums`) in the front matter on the **View+Edit** tab (advanced).

### The table of contents is empty or has wrong page numbers

**Why this happens:** PTXprint needs a first run to learn the page numbers. With **Quick Run** it runs only once.

**What to do:**

1. Untick **Quick Run**.
2. Make sure **Table of Contents** is ticked on the **Peripherals** tab, and the front matter contains `\ztoc|main\*`.
3. Print again.

### A variable prints as "<Type Value Here>"

**Why this happens:** The front matter uses a variable that has no value yet.

**What to do:** On the **Peripherals** tab, type a value in the **Variables and Values** table, and print again.

### The front matter does not appear in the PDF

**What to do:** On the **Peripherals** tab, tick **Local Front Matter**, and print again.

### My front matter changes disappeared

**Why this happens:** **Generate** on the **Front Matter** sub-tab replaces the whole front matter. **Refresh** also throws away unsaved changes. **Finish** in the **Cover Wizard** replaces the cover sections. There is no Undo.

**What to do:** Type the changes again. In future, copy important text to a safe place before you click **Generate**, and make cover text changes after you use the wizard.

### The cover was turned off by itself

**Why this happens:** PTXprint turns off **Create Cover Page** when you untick **Local Front Matter**. The status line says "The Cover is disabled because Local Front Matter is turned off."

**What to do:** On the **Peripherals** tab, tick **Local Front Matter**, then **Create Cover Page** again.

### No cover is made, or the Cover Wizard button is greyed out

**Why this happens:** **Create Cover Page** is not ticked, or the front matter has no cover sections. The cover is also a **separate** PDF (name ending **_cover**), not part of the main PDF.

**What to do:**

1. On the **Peripherals** tab, tick **Local Front Matter** and **Create Cover Page**. The **Cover Wizard...** button then works.
2. Run the **Cover Wizard** and click **Finish** to create the cover sections.
3. Print. Look for the cover on the **Cover** tab of the **PDF Preview** window.

### The Cover Wizard says "Existing cover settings found"

**Why this happens:** The configuration has cover styles or cover sections that the wizard did not make, or that were changed by hand. The wizard cannot build on them.

**What to do:** Click **Delete and Continue** to delete the old cover and start a new one with the wizard. Or click **Cancel (keep my settings)** to keep the cover as it is and change it by hand (the wizard does not open).

### The Finish button in the Cover Wizard is greyed out

**Why this happens:** **Finish** works only on the last (**Review**) step, and only when a title was typed in the front cover step.

**What to do:** Type a title in the front cover step, then go to the **Review** step.

### The colophon is missing

**Why this happens:** **Colophon at End of Publication** is unticked. PTXprint unticks it when you tick **Local Front Matter**, and when you tick **Layout Only**.

**What to do:** On the **Peripherals** tab, tick **Colophon at End of Publication** again. Untick **Layout Only** at the bottom of the window, and print again.

## 24.10 Settings and configurations

### I lost my changes after I chose another configuration

**Why this happens:** When you choose another configuration in **Name**, PTXprint does **not** save the current one. (When you choose another **Project**, it does save first.)

**What to do:** The lost changes cannot be recovered. Make them again. In future, click **Save** (or **Print (Make PDF)**) before you change configuration.

### I deleted a configuration and want to know what is gone

**Why this happens:** **Delete** (after **Yes**) removes the settings and working files of that one configuration. This cannot be undone. PTXprint then changes to **Default**. The PDFs you made are **not** deleted, and other configurations are not touched. (Older PTXprint versions also emptied the output folder of all configurations. This is fixed.)

**What to do:**

1. To get the settings back, use **Import Settings...** on the **Basic** tab with a PDF made with **Include Config Settings Within PDF**, or with a ZIP archive.
2. If the status line lists files that could not be deleted, close them in other programs (for example the PDF viewer).

### I clicked Reset and all my settings in Default are gone

**Why this happens:** For the **Default** configuration, **Delete** is replaced by **Reset** (Regular and Full views). **Reset** does not ask first. It sets every setting of **Default** back to the PTXprint defaults, and removes the saved files of **Default** (including its styles and picture list). Other configurations and PDFs are not changed.

**What to do:**

1. If the settings are in a PDF made with **Include Config Settings Within PDF**, use **Import Settings...** on the **Basic** tab to bring them back.
2. Or import them from another configuration, or from a ZIP archive.
3. In future, use **Save As** to keep your work in a named configuration, not in **Default**.

### The lock button or the Copy configuration button is greyed out

**Why this happens:** The **Default** configuration is selected. It cannot be locked, and it is never copied to other projects.

**What to do:** Use **Save As** to make a named configuration, then lock or copy that one.

### I cannot lock or unlock my configuration

**Why this happens:** To unlock, the password must be the same as when you locked. To lock, the password box must not be empty. **Cancel** never locks or unlocks.

**What to do:**

1. Click the lock button, type the password and click **OK**. If it is wrong, the status line says "Incorrect password".
2. If you cannot unlock it, use **Save As** to make a new, unlocked copy.

### The OK button in "Save Current Configuration As..." is greyed out

**Why this happens:** The name is empty, has spaces or special characters, or is already used.

**What to do:**

1. Read the message below the box. Use only letters a–z and A–Z, numbers, `(`, `)`, `_` and `-`.
2. To replace an existing configuration with that name, tick **Replace it if it already exists**. (**Default** can never be replaced.)

### Copy Configuration changed the titles in the other projects

**Why this happens:** **Keep each project's own language-specific variables** was unticked, so the target projects got this project's titles and language name.

**What to do:** Copy again with that box ticked, or correct the values in the **Variables and Values** table on the **Peripherals** tab of each target project.

### Import Settings says "Cannot find any settings to import from the selected file"

**Why this happens:** The PDF was made without **Include Config Settings Within PDF** (on the **Finishing** tab), or with a very old PTXprint version.

**What to do:** Use another source, for example a ZIP archive made with **Create Archive...**, or a saved configuration. In future, keep **Include Config Settings Within PDF** ticked.

### I imported only one group of settings, but everything changed

**Why this happens:** **Everything** was still ticked. In the **Basic** view the **Everything** tab is hidden but still ticked. Also, when the target is a **new** configuration name or an external folder, PTXprint always ticks **Everything**.

**What to do:**

1. Choose an existing configuration as the target.
2. Change to the **Regular** view, open **Import Settings...** again, and untick **Everything** before you tick the groups you want.

### Imported styles did not change

**Why this happens:** PTXprint only updates styles that you have not changed in the target configuration. The fonts inside styles come with **Fonts+Script**, not with **Styles**.

**What to do:** In the **Import Settings** dialog, tick **Override ALL Style Settings**. For style fonts, also tick **Fonts+Script**.

### A setting changed by itself

**Why this happens:** Some settings change others to keep them working together. For example:

* **Hyphenate** unticks **Between Letters**.
* **Right-to-Left** ticks **RTL Book Binding**.
* **Variable Line Spacing** ticks **Fill Columns** and **Allow Unbalanced Columns**.
* Changing between one and two columns halves or doubles the **Base Indent**.
* **Print-CMYK**, **Print-Gray** and **Print-Spot** tick **Only Show on Odd Pages** for thumb tabs.
* The footnote and cross-reference placements change together.
* **Local Front Matter** and **Layout Only** untick the colophon.
* **Compare PDFs** keeps the previous PDF even if **Number of Previous PDFs to be Kept** is 0.

**What to do:** Read the status line. PTXprint often says what it changed. Change the setting back if you need to.

## 24.11 Comparing PDFs

### Compare PDFs does not show a diff PDF

**Why this happens:** No differences were found, or the comparison could not be made.

**What to do:** Read the status line at the bottom of the window:

* **No differences found** – the two PDFs look the same.
* **Nothing to compare with yet: make a change and print again** – there is no previous PDF yet. Print once more.
* **Cannot find the PDF to compare with: ...** – the file chosen with **Select...** is gone. Choose it again.
* **Cannot compare PDFs: the pages are different sizes** – the page size changed. Only pages of the same size can be compared.
* **No pages could be compared. Check the Start Page Offset** – make **Start Page Offset** smaller.
* **No differences found, but the old Diff PDF is open and cannot be removed** – close the old diff PDF in your PDF program.

### Every page shows as changed in the diff PDF

**Why this happens:** The pages are probably not lined up, or something changed on every page (margins, headers, page numbers).

**What to do:** Change to the **Full** view. On the **Finishing** tab, in **Compare PDFs**:

1. If one PDF has extra pages at the start (for example a cover), set **Start Page Offset**.
2. If you changed only the margins or the gutter, tick **Smart Check**.
3. If only headers, footers or page numbers changed, tick **Headers + Footers** under **Ignore When Comparing**.

Extra pages at the end of the longer PDF always show as changed. This is correct.

## 24.12 I cannot find a setting

### A tab or setting that I used before has disappeared

**Why this happens:** The view level is lower than before. Lower view levels hide many settings. (The **Peripherals** and **Finishing** tabs show only their main settings in the **Basic** view. The **Publications** tab is only in the **Full** view.)

**What to do:**

1. Click **☰** › **View Level** › **Regular View** or **Full View**.
2. Or type the name of the setting in **Search for settings** (bottom-left, or **Ctrl+F**). PTXprint raises the view level if the setting is hidden.

### The PDF has pictures (or a diglot, borders, thumb tabs …) but I cannot find the setting

**Why this happens:** The feature was turned on in a higher view level. Hidden settings still work.

**What to do:**

1. Change to **Full View**.
2. Look for tabs with blue names. A blue tab name means a feature on that tab is on.
3. Turn the feature off on that tab.

### A setting is greyed out

**Why this happens:** It needs another setting first, or another setting blocks it. Common examples:

| Greyed-out setting | What it needs |
|---|---|
| Almost all of **Layout**, **Fonts+Script** and **Styles** | Untick **Lock UI Layout Settings** (**Advanced** tab, Full view). |
| **Save**, **Delete**, **Notes** | Unlock the configuration (lock button on the **Basic** tab). |
| Lock button, **Copy configuration to other projects** | Choose a configuration other than **Default**. |
| **Reset** (Basic tab) | Regular or Full view. |
| **Two Column Layout** | Turn off the diglot. A diglot always uses columns. |
| **Verse** (header references) | Tick **Chapter** first. |
| **Pri** / **Sec** (header) | Turn on **Diglot (or Polyglot)**. |
| **Parallel Passage Refs** | Tick **Headings** on the **Body** tab. |
| **Hanging Poetry Verse Numbers** | Untick **Marginal Verses**. |
| **Optimize Layout for Poetry Books** | Tick **Use Special Features for These Books** (**Body** tab). |
| **Between Letters** | Untick **Interlinear** on the **Advanced** tab. |
| **End of Column** (notes) | Tick **Two Column Layout**. |
| **Side Margin** (notes) | Tick **Margin Notes Col Width (mm)** on the **Layout** tab. |
| An **Edit...** button on the **Advanced** tab | Tick the check box for that file first. |
| **Scale to fit** (Finishing) | Set **Pages Per Spread** to **1-up**. |
| **Color Hue**, **Tolerance** | Choose **Print-Spot** as **PDF Output Format**. |
| **Locate...** (PDF Preview) | Tick **Layout Analysis**. |
| Fine-tune buttons (Layout) | Nothing to fix: **Lines Per Page** is already blue. |
| **Mirror** (picture) | Choose **OK to mirror** on the picture's **Checklist** sub-tab. |
| **Generate** (Front Matter) | Unlock the configuration. |
| **Cover Wizard...** | Tick **Create Cover Page** (**Peripherals** tab). |
| **Auto-calculate optimum widths of diglot columns** | A diglot with exactly two texts, and **Print** must be available. |
| **Custom Script** (Import Settings) | Import from a ZIP archive or a saved configuration, not a PDF. |
| **Include Transcelerator Questions** | The project needs Transcelerator data. |

**What to do:** Hover the mouse over the greyed-out setting; the tooltip often explains it. See also the chapter about that tab.

### The Help tab has very few links, or links do not open

**Why this happens:** **Disable ALL Internet Use** is ticked on the **Advanced** tab. PTXprint shows "Internet Access Disabled" when you click a web link.

**What to do:** On the **Advanced** tab, **Main** sub-tab, **General** area, untick **Disable ALL Internet Use**.

### PTXprint does not show my projects

**Why this happens:** The **Base Projects Directory** points to the wrong folder.

**What to do:** On the **Help** tab, click **Change...** next to **Base Projects Directory**. Choose the folder that *contains* your Paratext project folders, and click **Use Selected**.

## 24.13 Getting more help

If your problem is not in this chapter:

1. Read **Common problems** in the chapter for the tab you are using.
2. On the **Help** tab, click **Create Report...** and read the warnings and errors.
3. Ask the **Support Agent** or the **PTXprint User Community** (links on the **Help** tab).
4. Make an archive with **Create Archive...** (choose only the book that shows the problem), and email it to **ptxprint_support@sil.org** with a clear description, your PTXprint version and screenshots.


# 25. Glossary of terms

## 25.1 How to use this glossary

This glossary explains the technical words and PTXprint words used in this manual, in alphabetical order. Where it helps, it names the chapter that tells you more.

## 25.2 1–9

**1-up, 2-up, 4-up, 8-up** — How many book pages are printed on one side of a sheet. **1-up** is a normal PDF, one page per PDF page. **2-up** puts two pages side by side, for a folded booklet. Set it in **Pages Per Spread** (**Finishing** tab).

## 25.3 A

**Adj List (AdjList, adjustment list)** — The list of paragraph adjustments for each book. Each row asks PTXprint to set one paragraph one line shorter or longer, or with slightly narrower or wider letters. You make adjustments in the PDF Preview window, and see and edit the list on the **View+Edit** tab, **Adj List** sub-tab.

**Adjustment (shrink, expand)** — A small change to one paragraph so that it uses one line less (shrink) or more (expand), or so that its letters are a little narrower or wider. Used to make pages fill well. See the **PDF Preview** chapter.

**Align Text to Baseline** — A layout choice where every line sits on a fixed grid, so the lines on the front and back of a sheet line up. The other choice is **Variable Line Spacing**. See the **Layout** tab.

**Alpha** — How solid a background colour is: 0 is clear (see-through), 1 is fully solid. Used for sidebar backgrounds on the **Styles** tab.

**Anchor (Anchor Ref)** — The place in the text that a picture belongs to, usually a verse, for example `MRK 4.39`. PTXprint tries to put the picture on the same page as its anchor. See the **Pictures** tab.

**Archive (ZIP archive)** — A ZIP file with everything needed to make your PDF again on another computer: settings, text, fonts and pictures. Make it with **Create Archive...** on the **Help** tab, and send it to the support team when you ask for help.

**Auto Page Fill (page filler)** — A tool in the PDF Preview window that tries to make every page full by adjusting paragraphs automatically. It can take a long time. For a diglot or polyglot it also tries to keep the columns at the same height (experimental). See the **PDF Preview** chapter.

**Auto-update** — An option in the PDF Preview window. When ticked, PTXprint makes a new PDF by itself a few seconds after you adjust something in the preview.

## 25.4 B

**Back matter** — The pages after the Scripture text, for example a glossary, maps, an index or a colophon. See the **Peripherals** tab.

**Base Font Size** — The size of the letters in normal paragraphs, in points. All other text sizes (headings, notes, verse numbers) are relative to it. Set it on the **Layout** tab.

**Base Indent** — The normal width of a paragraph indent. Indents on the **Styles** tab are multiples of it. Set it on the **Layout** tab.

**Base Line Spacing** — The normal distance from one line of text to the next, in points. Set it on the **Layout** tab.

**Baseline** — The invisible line that the letters sit on.

**Bible Module** — A Paratext file that lists passages to print together, for example for a lectionary. You can print one from the **Basic** tab.

**Binding gutter** — Extra empty space at the inner edge of each page, near the spine, so the text does not disappear into the binding. See the **Layout** tab.

**Bleed** — A picture or colour that goes past the edge of the page, so no white strip shows if the printer does not cut exactly. Usually about 3 mm. See the **Finishing** tab.

**Blurb** — A short text on the back cover about the book. Add it in the **Cover Wizard**.

**Book code** — The 3-letter code for a book in Paratext and USFM, for example `GEN`, `MAT`, `JHN` or `1CO`. Use these codes when you type book lists in PTXprint.

**Book View** — A way to see two facing pages side by side in the PDF Preview window, as in a printed book.

**BSB (Berean Standard Bible)** — A free English Bible that PTXprint can install for you, for practice or as a second text in a diglot. See the **Basic** tab.

## 25.5 C

**Caller** — The small mark in the text (for example *a*, *b* or †) that tells the reader there is a note. The same mark is often repeated at the start of the note. See the **Notes+Refs** tab.

**Caption** — The text printed with a picture, usually below it. See the **Pictures** tab. In a diglot, a shared picture can show the captions of both texts (**Captions** on the **Diglot** tab).

**Category** — A label that groups study notes or sidebars, for example "people" or "places". All sidebars with the same category share one style.

**Changes file (changes.txt)** — A list of search-and-replace rules that PTXprint applies to a temporary copy of the text before typesetting. The Paratext text is not changed. An advanced feature on the **Advanced** tab.

**Chapter label** — A word printed before each chapter number instead of a large number alone, for example "Psalm 1". Set it on the **Body** tab.

**Character style (character marker)** — A style for a few words inside a paragraph, for example `\nd` (name of God) or `\w` (glossary word). Compare **paragraph style**.

**CMYK** — The four inks used by most colour printing presses: Cyan, Magenta, Yellow and blacK. Many printers ask for a CMYK PDF. Choose it in **PDF Output Format** on the **Finishing** tab.

**Colophon** — A short text at the end of the publication with details about it, for example the copyright, the printer and the picture credits. Turn it on and edit it on the **Peripherals** tab.

**Column Cross-References** — Cross-references printed in a narrow column of their own beside the text, as in many reference Bibles. See the **Notes+Refs** tab.

**Column gutter** — The empty space between two columns of text. See **gutter**.

**Configuration (config, layout)** — A named set of PTXprint settings for one project: page size, fonts, pictures, styles, front matter and so on. One project can have many configurations, for example a draft and a final one. Choose and make configurations on the **Basic** tab.

**Copyright statement** — The text that says who owns the rights to the text. PTXprint takes it from Paratext; you can change it on the **Basic** tab. Print it in the front matter with `\zcopyright`.

**Cover** — The outside of the book: front cover, spine and back cover. PTXprint makes the cover as a separate PDF (name ending **_cover**). See the **Peripherals** tab.

**Cover Wizard** — A step-by-step window on the **Peripherals** tab that designs the cover: spine, picture, background, front, spine and back cover text. **Finish** writes the cover sections into the front matter.

**Credit overlay** — A small copyright line printed on top of a picture. Some artists require it. See the **Pictures** tab.

**Crop marks (trim marks)** — Thin lines outside the corners of each page that show the printer where to cut. Only add them if the printer asks. See the **Finishing** tab.

**Cross-reference** — A note that lists other places in the Bible about the same thing, for example "Gen 1:1; Ps 33:6". In USFM it is marked with `\x`. PTXprint can also add cross-references from an external list. See the **Notes+Refs** tab.

**Cutout** — A space cut into the side of a paragraph, so that the text flows around a small picture or box. See the **Pictures** tab.

## 25.6 D

**DBL (Digital Bible Library)** — An online library of Scripture texts. You can download a text bundle from it and install it in PTXprint (see the **Basic** tab).

**Default configuration** — The configuration called **Default** that every project has. You cannot delete, lock, replace or copy it to other projects, but you can reset it (**Reset** on the **Basic** tab, with no confirmation).

**Diff PDF** — A PDF that shows in colour what changed between a new PDF and an older one (added text in the **New Text** colour, removed text in the **Old Text** colour). Make it with **Compare PDFs** on the **Finishing** tab. **Start Page Offset** lines up PDFs that start on different pages. **Smart Check** ignores lines that only moved because the margins changed.

**Digit mapping** — An option that prints numbers with the digits of another script (for example Arabic-Indic or Devanagari) when the text uses 0–9. Set it in the **Pick a Font** dialog (see the **Fonts+Script** tab).

**Diglot** — A publication with two texts side by side on the page, for example two languages. Each text comes from its own Paratext project. See the **Diglot** tab.

**Drop chapter number** — A large chapter number at the start of a chapter, two or more lines high, with the text beside it.

**Dynamic border** — A border that PTXprint draws around text, a heading or a title, and that grows with its contents. Compare **PDF border**. See the **Tabs+Borders** tab.

## 25.7 E

**em** — A unit of width equal to the size of the text. In 10 pt text, 1 em is 10 pt.

**End of Ayah** — A special character (U+06DD) used in Arabic script to decorate verse numbers. See the **Tabs+Borders** tab.

**Extended note (study note)** — A longer note, as in a study Bible. In USFM it is marked with `\ef`. PTXprint prints extended notes in their own area at the bottom of the page. See the **Notes+Refs** tab.

**External cross-reference list** — A ready-made list of cross-references that comes with PTXprint (or your own list). PTXprint can add these references to the publication. See the **Notes+Refs** tab.

## 25.8 F

**Fake (faux) bold and italic** — Bold or italic letters that PTXprint makes from the regular letters (thicker or slanted), when a font has no real bold or italic typeface.

**Fallback font** — A second font that PTXprint uses only for characters that the main font does not have, so they do not print as empty boxes. See the **Fonts+Script** tab.

**Final SFM** — The text of a book after PTXprint has made all its changes, exactly as sent to the typesetter. You can look at it (but not edit it) on the **View+Edit** tab.

**Font** — A set of letter shapes, for example *Charis SIL* or *Gentium Plus*. A font family usually has four typefaces: Regular, Bold, Italic and Bold Italic.

**Font feature** — An option built into a font, for example another shape for one letter, or different digits. Choose features with **Select Features...** in the **Pick a Font** dialog.

**Footer** — The line at the bottom of each page, outside the main text. It can hold a page number, a date, a time or a short text. See the **Header+Footer** tab.

**Footnote** — A note that explains something about the text. In USFM it is marked with `\f`. It is usually printed at the bottom of the page. See the **Notes+Refs** tab.

**Frame size** — The width of the area for a picture or box: one column, the full width (span), a page inside the margins, or the whole sheet. See the **Pictures** tab.

**Front matter** — The pages before the Scripture text, for example the title page, copyright page, table of contents and preface. In Paratext it is the FRT book. Make and edit it on the **Peripherals** and **View+Edit** tabs.

**FRT** — The book code for front matter. PTXprint does not list it with the other books. Set up the front matter on the **Peripherals** tab instead.

## 25.9 G

**Glossary** — A list of words with their meanings, usually at the end of the publication. Its book code is GLO.

**Glossary word** — A word in the text that has an entry in the glossary. In USFM it is marked with `\w ...\w*`. Choose how glossary words look (bold, a star before, a star before and after, brackets …) in **Glossary Word Appearance** on the **Body** tab.

**Glyph** — The shape that a font draws for a character.

**Glyph collision** — Letters or marks that touch or overlap, for example a high mark that hits the line above. **Layout Analysis** in the PDF Preview window marks these in red.

**Graph Paper** — A measuring grid that PTXprint can draw over the pages in the PDF Preview window. It is not printed in the PDF.

**Graphite** — A "smart font" technology from SIL. Some fonts for complex scripts need it. Tick **Graphite Rendering** in the **Pick a Font** dialog only for fonts made for Graphite.

**Grayscale (B/W)** — Only black ink, in shades of grey. Choose **Print-Gray (B/W)** on the **Finishing** tab for a book printed only in black.

**gsm** — Grams per square metre: the weight of paper. Heavier paper is usually thicker. The **Cover Wizard** can use it to work out the spine width.

**Gutter** — An empty space. The *column gutter* is the space between two columns. The *binding gutter* is extra space at the spine. See the **Layout** tab.

## 25.10 H

**Hanging indent** — A paragraph whose first line starts further left than the other lines. Poetry and lists often use it. Make it with a negative **First Line Indent Factor** on the **Styles** tab.

**Header (running header)** — The line at the top of each page, outside the main text. It often shows the book name, chapter and verse references, and the page number. See the **Header+Footer** tab.

**Hyphenation** — Breaking a long word at the end of a line, usually with a hyphen (-), and continuing it on the next line. PTXprint uses the hyphenation list from Paratext. See the **Fonts+Script** tab.

## 25.11 I

**Image set** — A downloadable collection of Bible illustrations. You can search it in the picture catalogue (**Show Catalogue...** on the **Pictures** tab).

**Imposition** — Arranging several book pages on one large sheet, so that after folding and cutting the pages come out in the right order. See **Booklet Pagination** on the **Finishing** tab.

**Interlinear** — Printing a gloss (a short translation) under or above each word of the text, from the Paratext Interlinearizer. See the **Advanced** tab.

**Introduction (book introduction)** — The text before chapter 1 of a book, with markers such as `\is` and `\ip`. Choose whether to print it on the **Body** tab.

**ISBN** — The international number that identifies a published book. The **Cover Wizard** can print it as a barcode on the back cover, and stores it in the variable **isbn**.

## 25.12 J

**Justification (justified text)** — Text where both the left and right edges of the lines are straight. PTXprint stretches or shrinks the spaces between words to do this. Compare **ragged**. Set it on the **Body** and **Styles** tabs.

## 25.13 K

**Kashida (tatweel)** — A joining stroke (ـ) in Arabic script that makes a word longer. It can be used to make lines look better. See the **Fonts+Script** tab.

## 25.14 L

**Layout Analysis** — A check in the PDF Preview window that looks for layout problems (wide spaces, rivers, collisions and missing characters) and marks them in colour on the page.

**Layout Only** — A check box in the bottom bar. When ticked, PTXprint does not process the text again if only layout settings changed, so printing is faster. It also unticks the colophon.

**Leading** — Another word for line spacing: the distance from the baseline of one line to the baseline of the next. PTXprint calls it **Line Spacing**.

**Line spacing** — See **leading** and **Base Line Spacing**.

**Lines Per Page** — The number of lines of text that fit on a page, shown on the **Layout** tab. Blue when a whole number of lines fits, red when there is wasted space.

**Lock Ratio** — A check box on the **Layout** tab that keeps the font size and line spacing in the same proportion. When you change one, PTXprint changes the other.

**Locked configuration** — A configuration protected with a password, so that nobody changes or deletes it by mistake. See the **Basic** tab.

## 25.15 M

**Margin** — The empty space between the text and the edge of the page. Set the margins on the **Layout** tab.

**Margin notes** — Footnotes, cross-references or headings printed in an extra column at the side of the text, beside their verse. See the **Layout** and **Notes+Refs** tabs.

**Marginal verses** — Verse numbers printed in a narrow column beside the text instead of inside it. Set them on the **Body** tab.

**Marker (USFM marker)** — A short code that starts with a backslash and says what a piece of text is. For example, `\p` starts a paragraph, `\s1` is a section heading, `\v` is a verse number and `\f` is a footnote. Each marker has a style on the **Styles** tab.

**Merging mode** — How PTXprint lines up the texts of a diglot or polyglot: by chapters and verses, or by a scoring method. See the **Diglot** tab.

**Mirror (picture)** — To flip a picture from left to right, as in a mirror. See the **Pictures** tab.

**Mirror Pages** — A setting that makes left-hand and right-hand pages mirror each other, so items stay on the outer (or inner) edge. See the **Layout** and **Header+Footer** tabs.

**Monoglot** — A publication with only one text (not a diglot or polyglot).

## 25.16 N

**Non-breaking space** — A space where PTXprint never breaks the line. The words on each side always stay on the same line.

**Notelines** — Ruled lines printed in a wide margin, so readers can write their own notes. Used for journaling Bibles. See the **Layout** tab.

## 25.17 O

**Odd and even pages** — Right-hand pages have odd numbers (1, 3, 5…). Left-hand pages have even numbers (2, 4, 6…).

**OpenType** — The usual font technology. Most fonts are OpenType fonts. Compare **Graphite**.

**Ornament** — A small decorative pattern or graphic. PTXprint can use ornaments in borders and to decorate pages. See the **Tabs+Borders** tab.

**Orphan** — In typesetting, the first line of a paragraph left alone at the bottom of a column or page. On the **Body** tab, **Prevent Orphan Words** is a different idea: it stops one short word being left alone on the last line of a paragraph. Compare **widow**.

## 25.18 P

**Padding** — Empty space inside a box or border, between the edge and the text. Set it in the **Border Settings** dialog (see the **Tabs+Borders** tab).

**Page filling** — Making the text reach the bottom margin on every page. You do it by adjusting paragraphs in the PDF Preview window, by hand or with **Auto Page Fill**.

**Page size** — See **trim size**. A size you type yourself is saved and offered in the **Page Size** list for all your projects.

**Paragraph style (paragraph marker)** — A style for a whole paragraph, for example `\p` (normal paragraph), `\q1` (poetry) or `\s1` (section heading). Compare **character style**.

**Parallel passage reference** — A reference under a section heading that shows where the same event is told in another book, for example "(Mark 1:1-8)". In USFM it is marked with `\r`.

**Paratext** — The program that translation teams use to write and check Scripture. PTXprint prints the text of a Paratext project.

**PDF border (Legacy)** — A ready-made PDF graphic that PTXprint places behind headings or on every page as a frame. Compare **dynamic border**.

**PDF Preview** — The PTXprint window that shows the PDF after you print. You can also use it to fix the layout. See the **PDF Preview** chapter.

**PDF/A** — A type of PDF made for keeping documents for a very long time (archiving).

**PDF/X** — A type of PDF made for printing. **PDF/X-1a** is the older, strict type (CMYK, no transparency). **PDF/X-4** is newer and allows RGB colours and transparency. See the **Finishing** tab.

**Penalty** — A number that tells the typesetter how much to avoid something, for example breaking a word. Higher means "avoid this more". 10000 means "never". Penalties are TeXpert settings on the **Advanced** tab.

**Periph (peripheral section)** — A section of the front or back matter, for example the title page or the preface. In the front matter each one starts with a `\periph` line.

**Peripheral book** — A book that is not Scripture text, for example front matter (FRT), back matter (BAK), the glossary (GLO) or extra material (XXA, XXB…).

**PicList (picture list)** — The list of all pictures in a configuration. Each line gives the picture file, its anchor, caption, size and position. PTXprint makes it from the `\fig` entries in the text, and then uses only the list. See the **Pictures** tab.

**Placeholder** — An empty box printed where a picture would go. It keeps the layout but makes the PDF very small.

**Polyglot** — A publication with three or more texts side by side. See the **Diglot** tab.

**Primary text** — In a diglot or polyglot, the text of the configuration you started from (code **L**). It controls the page size, margins, headers and footers. Compare **secondary text**.

**Project** — A Paratext project: the Scripture text that you want to print, with its settings. Choose it on the **Basic** tab.

**pt (point)** — A small unit used for type. 1 pt is about 0.35 mm. 72 pt is about one inch (25.4 mm). Font sizes and line spacing are given in points.

**Publication** — The book or booklet that you are making. On the **Publications** tab (Full view only), a publication is a named set of books that you can print together with others.

## 25.19 Q

**Quick Run** — A check box in the bottom bar. PTXprint then runs the typesetting only once, which is faster. Untick it for the final PDF, so page references and the table of contents are correct.

## 25.20 R

**Ragged** — Text where one edge of the lines is not straight (for example ragged right). Compare **justification**.

**Regular expression** — A way to describe patterns of text, used in changes files. An advanced feature.

**Resolution (picture)** — How detailed a picture file is. Low-resolution files are small and good for drafts. High-resolution files are large and needed for printing. Choose on the **Pictures** tab.

**RGB** — The colours used by screens: Red, Green and Blue. Compare **CMYK**.

**River** — A line of white space running down through several lines of text, made by wide word spaces that happen to be one above the other. **Layout Analysis** marks rivers in yellow.

**Right-to-left (RTL)** — Scripts written from right to left, for example Arabic and Hebrew. Set the direction on the **Fonts+Script** tab.

**Rule** — A thin straight line, for example under the header, between columns, or above the notes.

## 25.21 S

**Script** — A writing system, for example Latin, Arabic, Devanagari, Myanmar or Han (Chinese). Set the **Text Script** on the **Fonts+Script** tab.

**Secondary text** — In a diglot or polyglot, each text other than the primary text (codes **R**, **A**, **B**…). Each has its own configuration for its fonts and other text settings.

**Section heading** — A heading inside a book that names the next part of the text. In USFM it is marked with `\s1`, `\s2` and so on.

**Send/Receive** — The Paratext command that shares changes with the rest of the team. PTXprint configurations are shared this way. The PDFs are not.

**Sidebar** — A box of extra text, for example a study note about a place or a person, separate from the Scripture text. In USFM it starts with `\esb` and ends with `\esbe`. See the **Styles** tab.

**Signature** — A group of sheets that are folded together and sewn or glued into the book as one unit. See the **Finishing** tab.

**Span (Span Width)** — The full width of the text area, across both columns. Used for pictures and boxes.

**SpeedSlice** — A tool in the PDF Preview window that typesets only a few chapters of a long book, so each print is fast while you fix pages. Always turn it off before the final PDF. Not available for diglots. See the **PDF Preview** chapter.

**Spine** — The narrow back edge of a bound book, between the front and back covers. Its width depends on the number of pages and the paper. Books with fewer than about 80 pages usually have no spine text. Set it up in the **Cover Wizard**.

**Spot colour** — One extra, ready-mixed ink used with black, for example red for headings. See the **Finishing** tab.

**Spread** — Two facing pages of an open book: a left-hand page and the right-hand page beside it.

**Strong's numbers** — Numbers that identify each Hebrew and Greek word of the Bible. PTXprint can use them in cross-references and to make an index. See the **Notes+Refs** tab.

**Style** — The formatting rules for one marker: its font, size, colour, indents, alignment and spacing. Change styles on the **Styles** tab.

**Stylesheet** — A list of styles for all the markers. PTXprint combines the Paratext stylesheet with its own additions and your changes. See the **Styles** tab.

## 25.22 T

**Table of contents** — A list of the books with their page numbers, usually in the front matter. Turn it on with **Table of Contents** on the **Peripherals** tab.

**TeXpert settings** — About 125 fine settings for the typesetting engine, on the **Advanced** tab, **Other** sub-tab. For experienced users. Labels turn bold when a value is changed.

**Text area** — The part of the page where the main text goes. The margins are outside it.

**Thumb tab** — A coloured block at the outer edge of the page, with a short book name in it. When the book is closed, the reader can see the tabs and open the book at the right Bible book. See the **Tabs+Borders** tab.

**Tofu** — The empty box (☐) printed when the font has no shape for a character. Use a fallback font or another font to fix it.

**Transcelerator** — A Paratext plugin for making comprehension-checking questions. PTXprint can print the questions. See the **Notes+Refs** tab.

**Trim size** — The size of the finished book page after the printer cuts it. In PTXprint this is the **Page Size** on the **Layout** tab.

**Tutorial** — A file with a list of steps that PTXprint carries out one at a time on the current configuration, highlighting each control. Start it with **Run Tutorial...** on the **Basic** tab. Use a practice configuration.

**Typeface (face)** — One style of a font: Regular, Bold, Italic or Bold Italic.

## 25.23 U

**Underfilled page** — A page or column where the text stops before the bottom margin. PTXprint lists these in the PDF Preview window, so you can fix them.

**Unicode** — The international standard that gives a number to every character in every script. A character can be written as `U+` and a hexadecimal number, for example U+06DD.

**USFM** — Unified Standard Format Markers. The way Paratext stores Scripture text, with markers such as `\p`, `\v` and `\f` that say what each piece of text is.

**USX** — An XML format for Scripture text, used for example in DBL text bundles.

## 25.24 V

**Variable** — A place-holder in the front matter, written as `\zvar|name\*`. When you print, PTXprint replaces it with a value from the variables table on the **Peripherals** tab, for example the title of the book. When you copy a configuration to other projects, each project normally keeps its own language-specific variables (titles, language name).

**Variable Line Spacing** — A layout choice where PTXprint may stretch the space between lines a little so that every column is filled to the bottom. Compare **Align Text to Baseline**.

**View level** — How many settings PTXprint shows: **Mini**, **Basic**, **Regular** or **Full**. Hidden settings still work. Change it with **☰** › **View Level** (see the chapter **The main window, menu and view levels**).

## 25.25 W

**Watermark** — A light text or picture printed on every page, for example the word "DRAFT". Add it on the **Finishing** tab.

**Widow** — In typesetting, the last line of a paragraph left alone at the top of a column or page. On the **Body** tab, **Prevent Verse Widow Words** is a different idea: it stops a verse number and a short word being left alone at the end of a line. Compare **orphan**.

## 25.26 X

**XeTeX** — The typesetting program that PTXprint uses behind the scenes to place the text on the pages. You never need to use it yourself. Its report of the last print run is on the **View+Edit** tab (**XeTeX Log**).

## 25.27 Z

**z-codes** — Extra codes that start with `\z` and that PTXprint understands in addition to normal USFM markers, for example `\zcopyright`, `\zvar|...\*` or `\ztoc|main\*`. Used mostly in the front matter. See the **View+Edit** tab.

**ZIP file** — A file that holds other files packed together. PTXprint uses ZIP files for archives, image sets and printer orders.
