# About this manual

## What PTXprint is

PTXprint is a program that makes print-ready PDF files of Scripture. It takes the text from a
Paratext project and lays it out on pages: with columns, headings, chapter and verse numbers,
footnotes, cross-references, pictures, headers and footers. You can use the PDF for checking and
proofreading, or send it to a printer to make a book.

Behind the scenes, PTXprint uses a typesetting program called **XeTeX**. XeTeX does the work of
placing every letter and line on the page. You never need to use XeTeX yourself. You make all
your choices in the PTXprint window, and PTXprint tells XeTeX what to do.

PTXprint never changes your Paratext text. It reads the text, makes a temporary copy, and
typesets that copy. To correct the words of the text, use Paratext.

## Who this manual is for

This manual is for everyone who uses the PTXprint window: translators, typesetters, project
leaders and support staff. You do not need to know anything about typesetting or computers to use
it.

* Every instruction in this manual can be done in the PTXprint window. You never need to edit
  files by hand or type commands.
* Some sections are marked **advanced**. They explain how to type special codes in the few places
  where PTXprint gives you a text box for them (for example the front matter). You can skip these
  sections until you need them.
* Technical words are explained the first time they appear in a chapter. They are also listed in
  the **Glossary of terms** at the end of the manual.

## How this manual is organised

The manual starts with two general chapters. Then there is one chapter for each tab of the
PTXprint window, in the same order as the tabs. After that come chapters about the PDF Preview
window, importing settings and getting help. The manual ends with step-by-step tasks, solutions
to problems, and a glossary.

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
* **Settings reference** – a list of every setting on the tab (see below).

## How to read a settings-reference entry

At the end of each tab chapter, the **Settings reference** lists every setting (check box, list,
number box, button and so on) in that part of PTXprint. Each entry starts with the name of the
setting as you see it on the screen. Then it gives some or all of these facts:

* **Where** – the path to the setting: the tab, then the area or sub-tab. For example:
  *Layout tab › Page Setup*.
* **Type** – what kind of control it is, for example a check box, a drop-down list, a number box or
  a button. For a check box, it also says if it is ticked or not ticked by default.
* **Description** – a short name for the setting, when the label on the screen does not say
  enough.
* **Next to the label** – the label that is beside the control on the screen, when this is
  different from the name of the entry.
* **View level** – in which view levels you can see the setting (see below).
* **Values** – for a number box: the lowest and highest number you can type, and the default value.
* **Choices** – for a drop-down list: the items in the list.
* **Only available when** – the setting is greyed out until another setting is turned on.
* **Greyed out when** – the setting cannot be used while another setting is turned on.
* **Hidden until** – the setting is not shown until another setting is ticked.
* **Tooltip** – the help text that PTXprint shows when you hold the mouse over the setting.
* **Explanation** – a description in plain words: what the setting does, when to use it, a
  sensible value, and what to watch out for.

If you cannot find a setting in the window, look first at its **View level**, then at **Only
available when** and **Hidden until**.

## A short note about view levels

PTXprint has hundreds of settings, but most people need only a few of them. So PTXprint can hide
the settings that you do not need. This is called the **view level**. There are four view levels:
**Mini**, **Basic**, **Default** and **Full**. **Mini** shows the fewest settings. **Full** shows
every setting.

To change the view level, click the **☰** button at the top-right of the window, point to
**View Level**, and choose a level.

A hidden setting still works. It keeps its value and it still changes the PDF. So if the PDF
does not look the way you expect, change to the **Full** view and check the settings again.

In this manual, a note such as "(Default and Full views)" tells you which view levels show a
setting. For more about view levels, see the chapter **The main window, menu and view levels**.
