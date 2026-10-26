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
   * the **☰** button at the top-left, for the main menu;
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
