## What PTXprint is

PTXprint makes print-ready PDF files of Scripture. It takes the text from a Paratext project and
lays it out on pages: with columns, headings, chapter and verse numbers, footnotes,
cross-references, pictures, headers and footers. You can use the PDF for checking and
proofreading, or send it to a printer to make a book.

PTXprint uses a typesetting program called **XeTeX** to place every letter and line on the page.
You never need to use XeTeX yourself. You make all your choices in the PTXprint window, and
PTXprint tells XeTeX what to do.

PTXprint never changes your Paratext text. It reads the text, makes a temporary copy, and
typesets that copy. To correct the words of the text, use Paratext.

## Who this manual is for

This manual is for everyone who uses the PTXprint window: translators, typesetters, project
leaders and support staff. You do not need to know about typesetting or computers.

* Every instruction can be done in the PTXprint window. You never need to edit files by hand or
  type commands.
* Sections marked **advanced** explain how to type special codes in the few places where
  PTXprint gives you a text box for them (for example the front matter). You can skip them until
  you need them.
* Technical words are explained the first time they appear in a chapter, and listed in the
  **Glossary of terms** at the end.

## How this manual is organised

The manual has four parts.

**Part 1: Start here**

* **About this manual** – this chapter.
* **Getting started with PTXprint** – a first walk-through: from opening PTXprint to your first PDF.
* **The main window, menu and view levels** – the parts of the window, configurations, view
  levels, and how PTXprint saves your settings.

**Part 2: Find an answer**

* **How do I...? (step-by-step tasks)** – short instructions for common jobs.
* **Problems and solutions** – what to do when something goes wrong.

**Part 3: Reference, tab by tab**

One chapter for each tab of the PTXprint window, in the same order as the tabs. Then come chapters
about the PDF Preview window, importing settings and getting help.

* **Basic tab** – choose the project, the configuration and the books to print.
* **Layout tab** – page size, margins, columns, font size and line spacing.
* **Fonts+Script tab** – fonts, writing system, hyphenation and spacing.
* **Body tab** – what is printed from each book (introductions, headings, verse numbers…).
* **Notes+Refs tab** – footnotes, cross-references and study notes.
* **Header+Footer tab** – the running header and footer, and page numbers.
* **Pictures tab** – illustrations and maps.
* **Diglot tab (two or more languages)** – two or more texts side by side.
* **Tabs+Borders tab** – thumb tabs and decorative borders.
* **Styles tab** – the look of each kind of text (each USFM marker).
* **Advanced tab** – settings for experienced users.
* **View+Edit tab** – front matter, the adjustment list, and the files PTXprint makes.
* **Peripherals tab (front and back matter)** – front matter, table of contents, colophon, maps and covers.
* **Publications tab** – a list of publications that you can print together.
* **Finishing tab** – PDF type for the printer, crop marks, booklets and comparing PDFs.
* **Printers tab** – price estimates and orders from print companies.
* **PDF Preview window, layout analysis and page filling** – look at the PDF and fix the layout of pages.
* **Importing settings** – copy settings from a PDF, an archive or another configuration.
* **Help tab and getting support** – find your files, and ask for help.

**Part 4: Glossary**

* **Glossary of terms** – the meaning of the words used in this manual.

Most tab chapters have the same parts:

* **What this tab is for** – when you would use the tab.
* One section for each area of the tab, using the names you see on the screen.
* **Common tasks** – numbered steps for the things people do most often.
* **Common problems** – what you see, why it happens, and what to change.
* **Settings reference** – every setting on the tab (see below).

## How to read a settings-reference entry

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

## A short note about view levels

PTXprint has hundreds of settings, but most people need only a few. So PTXprint can hide the
settings you do not need. This is the **view level**. There are four: **Mini** (fewest settings),
**Basic**, **Regular** and **Full** (every setting).

To change the view level, click the **☰** button at the top-left of the window, point to
**View Level**, and choose a level.

A hidden setting still works. It keeps its value and still changes the PDF. So if the PDF does
not look as you expect, change to the **Full** view and check the settings again.

A note such as "(Regular and Full views)" tells you which view levels show a setting. For more,
see the chapter **The main window, menu and view levels**.
