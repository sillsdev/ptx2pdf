# Header+Footer tab

## What this tab is for

The **Header+Footer** tab decides what is printed in the running header (the line at the top of
each page) and the footer (the line at the bottom of each page). Come here to:

* choose where the page number goes;
* show the references on each page (for example "Matthew 5:3–6:2");
* add a "DRAFT" message, a date or the time;
* choose the page number that the first Scripture book starts with;
* choose what is printed at the bottom of the first page of each book.

The **position** of the header and footer, the line (rule) under the header, and mirrored pages
are set on the **Layout** tab. The font and size of the header text are set by the `\h` style on the
**Styles** tab (click the **\h** link on this tab).

## Header

The header has three places: **Inner (Left)**, **Center** and **Outer (Right)**. Each place has a
drop-down list. You can choose a ready-made item or type your own text.

The ready-made items are:

* **-empty-** – nothing.
* **Page Number** – the page number.
* **First Reference** – the first verse on the page, for example "John 3:1".
* **Last Reference** – the last verse on the page.
* **Reference Range** – the first and last verse together, for example "John 3:1–4:5".
* **Book (\h)** – the book name from the `\h` line of the book.
* **Book Alt (\h1)** – the book name from the `\h1` line, if the book has one.
* In **Inner (Left)** only: the time, the date, or "Printed on" and the date.

### Mirrored headers

On the **Layout** tab, in the **Page Setup** area, the setting **Mirror Pages** changes how the
three places are used.

* **Mirror Pages ticked** (usual for a printed book): "Inner" means next to the spine and "Outer" means next to the
  page edge. On right-hand pages (odd page numbers) Inner is on the left; on left-hand pages (even page numbers) Inner is on the right.
  On left-hand pages PTXprint also swaps **First Reference** and **Last Reference**. So if you put
  **Last Reference** in **Outer (Right)**, the left-hand page shows its *first* verse at its outer
  edge, and the right-hand page shows its *last* verse at its outer edge. Like a dictionary, the two
  outer edges of an open book then show the range of the whole spread.
* **Mirror Pages unticked**: Left is always left and Right is always right, on every page.

### Which pages get a header

* On the **first page of each book** (the page with the book title), the header is empty and no rule is
  drawn under it.
* On pages without verses (for example pages of the introduction or the glossary), the reference items
  (**First Reference**, **Last Reference**, **Reference Range**) print nothing. Other items, such as
  the page number, are still printed.

### Reference format

Under **Include in References**, choose what the reference items contain (Default and Full views):

* **Book** – the book name.
* **Chapter** – the chapter number.
* **Verse** – the verse numbers too. This needs **Chapter**.
* **Chapter-Verse Separator** – **Colon (ch:vs)** or **Period (ch.vs)**.

Most Bibles show only book and chapter, for example "Matthew 5–6", because it is easier to find a chapter
when you turn the pages.

### Diglot options

When you print a diglot (two texts side by side), each place has two small buttons, **Pri** and **Sec**.
They choose which text the item comes from: the primary text or the secondary text. This decides
both the language of the book names in the references and the font used. These buttons are greyed out
until you turn on **Diglot (or Polyglot)** on the **Diglot** tab. (Default and Full views.)

### Typing your own text (advanced)

You can type in the box of each place instead of choosing an item. You can mix ordinary words with these
codes:

* `\pagenumber` – page number
* `\firstref`, `\lastref`, `\rangeref` – references
* `\book`, `\bookalt` – book name from `\h` or `\h1`
* `\isodate` – the date as YYYY-MM-DD; `\usdate` (month/day/year); `\ukdate` (day/month/year)
* `\hrsmins` – the time (HH:MM)
* `\empty` – nothing

Follow these rules:

* Put a backslash and a space (`\ `) for each space between words, for example `DRAFT\ \isodate`.
* Put a backslash before the characters `# % & ^ ~` and `\`. For example, type
  `This\ is\ page\ \#\pagenumber` to get "This is page #1".
* Put square brackets around a code to print brackets: `[\pagenumber]` gives "[12]".

## Other

This area is only shown in the **Default** and **Full** views.

* **Starting Page Number (for Scripture Books)** – the page number of the first page of the first
  Scripture book.
* **Print Page Number at Bottom of Intro Page(s)** and **Print Name of Saved Config on Intro Page(s)**
  choose what goes in the footer of the first page of each book. You can tick only one of them;
  ticking one unticks the other.

## Footer

The footer has one place: **Center Footer**. Many Bibles leave it empty and put the page number in the
header. It is useful for a page number at the bottom of every page, or a "DRAFT" message with the
date. The choices and rules for typing your own text are the same as for the header.

The footer of the first page of each book follows the settings in the **Other** area:

* **Print Page Number at Bottom of Intro Page(s)** ticked: the page number.
* else, **Print Name of Saved Config on Intro Page(s)** ticked: the name of the configuration.
* else: the same as **Center Footer**.

For a diglot, the **Pri** and **Sec** buttons choose which text's font is used for the footer.

To move the footer up or down, use the **Layout** tab, **Margins** area (**Bottom of Text to Top of
Footer** and **Place Footer Text Above the Bottom Margin**).

## Common tasks

### How do I put the page number in the outer corner and the references in the center?

1. On the **Layout** tab, in **Page Setup**, tick **Mirror Pages**.
2. On the **Header+Footer** tab, set **Outer (Right)** to **Page Number**.
3. Set **Center** to **Reference Range**.
4. Set **Inner (Left)** to **-empty-**.
5. Print again.

### How do I show verse numbers in the header references?

1. Switch to the **Default** or **Full** view.
2. On the **Header+Footer** tab, make sure **Chapter** is ticked.
3. Tick **Verse**.
4. Choose **Colon (ch:vs)** or **Period (ch.vs)**.

### How do I add "DRAFT" and today's date to every page?

1. On the **Header+Footer** tab, open **Center Footer**.
2. Choose **Printed on YYYY-MM-DD**, or type `DRAFT\ \isodate` in the box.
3. Print again. The date is the date of printing.

### How do I start the page numbers at 101?

1. Switch to the **Default** or **Full** view.
2. On the **Header+Footer** tab, in **Other**, set **Starting Page Number (for Scripture Books)** to 101.
3. Print again.

### How do I put a line under the header?

1. On the **Layout** tab, in the **Margins** area, tick **Horizontal Rule**.
2. Set **Space between Rule and Top of Text (pt)** (a pt, or point, is about 0.35 mm).
3. The rule is not drawn on the first page of each book.

### How do I show the name of my configuration on the printout?

1. Switch to the **Default** or **Full** view.
2. On the **Header+Footer** tab, in **Other**, tick **Print Name of Saved Config on Intro Page(s)**.
3. The name is printed at the bottom of the first page of each book, instead of the page number.

### How do I set the headers for a diglot?

1. On the **Diglot** tab, turn on **Diglot (or Polyglot)**.
2. On the **Header+Footer** tab, choose an item for each place.
3. For each place, click **Pri** to use the primary text (its book names and font), or **Sec** for the secondary text.
4. Decide on **Mirror Pages** on the **Layout** tab. With it ticked, the primary text is next to the spine.

## Common problems

**There is no header on the first page of a book.**
This is normal. PTXprint does not print a header (or a rule) on the page where a book starts.
Use **Print Page Number at Bottom of Intro Page(s)** to have a page number there.

**The header references are empty on the introduction or glossary pages.**
This is normal. Those pages have no verses, so **First Reference**, **Last Reference** and
**Reference Range** print nothing there. The page number still prints.

**The header shows the last verse on the left page where I expected the first verse.**
Cause: **Mirror Pages** is ticked. On left-hand pages PTXprint swaps **First Reference** and
**Last Reference**. Fix: choose the other item, or untick **Mirror Pages** on the **Layout** tab.

**The header is on the wrong side on left-hand pages.**
Cause: with **Mirror Pages** ticked, **Inner** and **Outer** swap sides on left-hand pages. Fix:
untick **Mirror Pages** if you want the same layout on every page.

**"Verse" is greyed out.**
Cause: **Chapter** is unticked. Tick **Chapter** first.

**The Pri / Sec buttons are greyed out.**
Cause: diglot is not turned on. Turn on **Diglot (or Polyglot)** on the **Diglot** tab.

**"Print Name of Saved Config" unticked itself.**
Cause: you ticked **Print Page Number at Bottom of Intro Page(s)**. Only one of the two can be used.

**My own header text prints wrongly, or the PDF fails.**
Cause: a space or a special character (`# % & ^ ~ \`) was typed without a backslash before it.
Fix: type `\ ` for spaces and `\#`, `\%` and so on.

**The footer shows "<Enter ID>" instead of the time.**
Cause: a mistake in the **Time (HH:MM)** item of the **Center Footer** list. Fix: type `\hrsmins` in the
**Center Footer** box instead of choosing the item.

**The page numbers do not start at the "Starting Page Number".**
The number is applied when the first Scripture book starts, if the pages before it use the separate
front matter numbering (as PTXprint sets up by default). If the front matter has been given normal page
numbers, the numbering simply continues from the front matter.

## Settings reference: Header+Footer tab

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Header+Footer tab › Header

#### Center

- **Where:** Header+Footer tab › Header
- **Type:** Drop-down list
- **Description:** Center page header settings
- **View level:** Basic, Default and Full views
- **Choices:** -empty-; Page Number; First Reference; Last Reference; Reference Range; Book (\h); Book Alt (\h1)

**Tooltip (the text shown when you hover the mouse over it):**

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

**Explanation:**

The item printed in the middle of the header on every page (except the first page of each book).
A common choice is **Page Number** or **Reference Range**. You can also type your own text (see
"Typing your own text"). The center place does not change sides when **Mirror Pages** is ticked, but
**First Reference** and **Last Reference** are still swapped on left-hand pages.

*(Internal ID: `ecb_hdrcenter` · Config key: `header/hdrcenter`)*

#### Outer (Right)

- **Where:** Header+Footer tab › Header
- **Type:** Drop-down list
- **Description:** Outer (right) page header settings
- **View level:** Basic, Default and Full views
- **Choices:** -empty-; Page Number; First Reference; Last Reference; Reference Range; Book (\h); Book Alt (\h1)

**Tooltip (the text shown when you hover the mouse over it):**

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

**Explanation:**

The item printed at the right of the header. With **Mirror Pages** ticked (on the **Layout** tab), this
is the outer edge: the right on right-hand pages and the left on left-hand pages. A common choice
is **Page Number** or a reference. On left-hand pages **First Reference** and **Last Reference** swap.

*(Internal ID: `ecb_hdrright` · Config key: `header/hdrright`)*

#### Inner (Left)

- **Where:** Header+Footer tab › Header
- **Type:** Drop-down list
- **Description:** Inner (left) page header settings
- **View level:** Basic, Default and Full views
- **Choices:** -empty-; Page Number; First Reference; Last Reference; Reference Range; Book (\h); Book Alt (\h1); Time (HH:MM); Date (YYYY-MM-DD); Printed on YYYY-MM-DD

**Tooltip (the text shown when you hover the mouse over it):**

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

**Explanation:**

The item printed at the left of the header. With **Mirror Pages** ticked, this is the inner edge (next to
the spine): the left on right-hand pages and the right on left-hand pages. This list also has the
time and date items, which are useful for drafts. Many publications leave this **-empty-**.

*(Internal ID: `ecb_hdrleft` · Config key: `header/hdrleft`)*

#### Pri

- **Where:** Header+Footer tab › Header
- **Type:** Radio button
- **Description:** Use formatting from primary project (inner header)
- **View level:** Default and Full views
- **Only available when:** “Diglot (or Polyglot)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If setting the header for a diglot you will need to specify whether this part of the header (its text and formatting) should come from the Primary (Left) or the Secondary text.
>
> Note: To activate or change this setting, you must first enable Diglot.

**Explanation:**

For a diglot: take the inner header item from the **primary** text. References then use the
primary text's book names, and the primary text's header font is used. Greyed out until diglot is turned on.

*(Internal ID: `r_hdrLeft_Pri` · Config key: `header/hdrleftside=Pri`)*

#### Sec

- **Where:** Header+Footer tab › Header
- **Type:** Radio button
- **Description:** Use formatting from secondary project (inner header)
- **View level:** Default and Full views
- **Only available when:** “Diglot (or Polyglot)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If setting the header for a diglot you will need to specify whether this part of the header (its text and formatting) should come from the Primary (Left) or the Secondary text.
>
> Note: To activate or change this setting, you must first enable Diglot.

**Explanation:**

For a diglot: take the inner header item from the **secondary** text, with the secondary text's book
names and header font. Greyed out until diglot is turned on.

*(Internal ID: `r_hdrLeft_Sec` · Config key: `header/hdrleftside=Sec`)*

#### Pri

- **Where:** Header+Footer tab › Header
- **Type:** Radio button
- **Description:** Use formatting from primary project (center header)
- **View level:** Default and Full views
- **Only available when:** “Diglot (or Polyglot)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If setting the header for a diglot you will need to specify whether this part of the header (its text and formatting) should come from the Primary (Left) or the Secondary text.
>
> Note: To activate or change this setting, you must first enable Diglot.

**Explanation:**

For a diglot: take the center header item from the **primary** text (book names and font).
Greyed out until diglot is turned on.

*(Internal ID: `r_hdrCenter_Pri` · Config key: `header/hdrcenterside=Pri`)*

#### Pri

- **Where:** Header+Footer tab › Header
- **Type:** Radio button
- **Description:** Use formatting from primary project (outer header)
- **View level:** Default and Full views
- **Only available when:** “Diglot (or Polyglot)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If setting the header for a diglot you will need to specify whether this part of the header (its text and formatting) should come from the Primary (Left) or the Secondary text.
>
> Note: To activate or change this setting, you must first enable Diglot.

**Explanation:**

For a diglot: take the outer header item from the **primary** text (book names and font).
Greyed out until diglot is turned on.

*(Internal ID: `r_hdrRight_Pri` · Config key: `header/hdrrightside=Pri`)*

#### Sec

- **Where:** Header+Footer tab › Header
- **Type:** Radio button
- **Description:** Use formatting from secondary project (center header)
- **View level:** Default and Full views
- **Only available when:** “Diglot (or Polyglot)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If setting the header for a diglot you will need to specify whether this part of the header (its text and formatting) should come from the Primary (Left) or the Secondary text.
>
> Note: To activate or change this setting, you must first enable Diglot.

**Explanation:**

For a diglot: take the center header item from the **secondary** text (book names and font).
Greyed out until diglot is turned on.

*(Internal ID: `r_hdrCenter_Sec` · Config key: `header/hdrcenterside=Sec`)*

#### Sec

- **Where:** Header+Footer tab › Header
- **Type:** Radio button
- **Description:** Use formatting from secondary project (outer header)
- **View level:** Default and Full views
- **Only available when:** “Diglot (or Polyglot)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If setting the header for a diglot you will need to specify whether this part of the header (its text and formatting) should come from the Primary (Left) or the Secondary text.
>
> Note: To activate or change this setting, you must first enable Diglot.

**Explanation:**

For a diglot: take the outer header item from the **secondary** text (book names and font).
A common diglot setup is **Pri** for one side and **Sec** for the other, so each language has
its own reference. Greyed out until diglot is turned on.

*(Internal ID: `r_hdrRight_Sec` · Config key: `header/hdrrightside=Sec`)*

#### Chapter

- **Where:** Header+Footer tab › Header
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> By default, the chapter number will be included in any references in the header line. If you prefer to suppress that (and just show the book name) then uncheck this option. (Verse numbers can only be shown if Chapter is ticked.)

**Explanation:**

Ticked: header references include the chapter number, for example "Mark 4". Unticked: only the book
name is shown, and **Verse** is greyed out. Unticking it can be useful for books with only one chapter or for
non-Bible publications.

*(Internal ID: `c_rangeShowChapter` · Config key: `header/ifshowchapter`)*

#### Verse

- **Where:** Header+Footer tab › Header
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Chapter” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> By default only the Book and Chapter number is included in the Header. If you also want to include the verse numbers, then check this option.
>
> Keep in mind that including the verse numbers actually makes it harder to read/absorb when flicking through pages to find the right chapter.

**Explanation:**

Adds the verse numbers to the header references, for example "Mark 4:3–5:2" instead of "Mark 4–5".
Readers usually find a chapter more quickly without the verses. Greyed out unless **Chapter** is
ticked.

*(Internal ID: `c_rangeShowVerse` · Config key: `header/ifshowverse`)*

#### Colon (ch:vs)

- **Where:** Header+Footer tab › Header
- **Type:** Radio button
- **View level:** Default and Full views
- **Only available when:** “Verse”, “Chapter” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Use a colon (:) to separate chapter & verse numbers in the header reference.

**Explanation:**

Uses a colon between chapter and verse in the header references. If the Paratext project has its own
chapter-verse separator, PTXprint uses that one. Only used when **Verse** is ticked.

*(Internal ID: `r_CVsep_colon` · Config key: `header/chvseparator=colon`)*

#### Period (ch.vs)

- **Where:** Header+Footer tab › Header
- **Type:** Radio button
- **View level:** Default and Full views
- **Only available when:** “Verse”, “Chapter” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Use a period (.) to separate chapter & verse numbers in the header reference.

**Explanation:**

Uses a period between chapter and verse in the header references, for example "4.3". Only used
when **Verse** is ticked.

*(Internal ID: `r_CVsep_period` · Config key: `header/chvseparator=period`)*

#### Book

- **Where:** Header+Footer tab › Header
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> By default, the book name will be included in any references in the header line. But if you wish to suppress that (and just show the chapter and/or verse numbers) then uncheck this option.

**Explanation:**

Ticked: header references include the book name (from the book's `\h` line). Unticked: only the chapter
(and verse) numbers are shown. Untick it if the book name is already in another place of the header,
for example with **Book (\h)**.

*(Internal ID: `c_rangeShowBook` · Config key: `header/ifshowbook`)*

#### \h

- **Where:** Header+Footer tab › Header
- **Type:** Link
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the marker's properties on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the `\h` style. That style sets the font, size and color of the
running header text. (The footer also follows this style unless it is changed separately.)

*(Internal ID: `lb_style_h`)*

### Header+Footer tab › Other

#### Starting Page Number (for Scripture Books)

- **Where:** Header+Footer tab › Other
- **Type:** Number box
- **Description:** Start numbering scripture books from page N
- **View level:** Default and Full views
- **Values:** from 1 to 9999, default 1

**Tooltip (the text shown when you hover the mouse over it):**

> If the document you are creating needs to be appended to another, you can start the page numbering from where the previous document ends by entering the subsequent page number here. (If the front matter already uses normal page numbers, the numbering just continues instead.)
>
> If you want front matter pages to be numbered with roman numerals (i, ii, iii, iv, v, etc) then add this line to the front matter to trigger it:  
>        \resetpagenums -1 and normal page numbering will restart as soon as the first scripture book is encountered.
>
> If the document you are creating needs to be appended to another, you can start the page numbering from where the previous document ends by entering the subsequent page number here.
>
> If you want front matter pages to be numbered with roman numerals (i, ii, iii, iv, v, etc) then add this line to the front matter to trigger it:  
>        \resetpagenums -1 and normal page numbering will restart as soon as the first scripture book is encountered.

**Explanation:**

The page number of the first page of the first Scripture book. Use it when this PDF continues
another document, for example 101. Pages before the first Scripture book (front matter) are
numbered separately (roman numerals i, ii, iii … in PTXprint's front matter), and the Scripture
numbering then starts at this number. (Default and Full views.)

*(Internal ID: `s_startPageNum` · Config key: `document/startpagenum`)*

#### Print Page Number at Bottom of Intro Page(s)

- **Where:** Header+Footer tab › Other
- **Type:** Checkbox (ticked by default)
- **Description:** Print page number at each book's Intro page footer
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Print the page number at the bottom of the first page of each book (the title page, where the header is not shown).
>
> This cannot be used together with 'Print Name of Saved Config on Intro Page(s)'.

**Explanation:**

Prints the page number in the footer of the first page of each book (the page with the book title).
That page has no header, so without this it has no page number at all. Ticking this unticks
**Print Name of Saved Config on Intro Page(s)**. (Default and Full views.)

*(Internal ID: `c_pageNumTitlePage` · Config key: `footer/ifftrtitlepagenum`)*

#### Print Name of Saved Config on Intro Page(s)

- **Where:** Header+Footer tab › Other
- **Type:** Checkbox (not ticked by default)
- **Description:** Print the name of the config on Intro pages' footer
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> It may be helpful to print the Name of the Saved Configuration on the first page (of every book) as a reminder for later - as to which settings were used to produce the PDF.
>
> This cannot be used together with 'Print Page Number at Bottom of Intro Page(s)'.

**Explanation:**

Prints the name of the saved configuration in the footer of the first page of each book. This helps
you remember which settings made a test printout. Ticking this unticks **Print Page Number at
Bottom of Intro Page(s)**. Untick it for the final publication. (Default and Full views.)

*(Internal ID: `c_printConfigName` · Config key: `footer/ifprintconfigname`)*

### Header+Footer tab › Footer

#### Center Footer

- **Where:** Header+Footer tab › Footer
- **Type:** Drop-down list
- **Description:** Center page footer settings
- **View level:** Basic, Default and Full views
- **Choices:** -empty-; Page Number; Reference Range; DRAFT; Time (HH:MM); Date (YYYY-MM-DD); Printed on YYYY-MM-DD

**Tooltip (the text shown when you hover the mouse over it):**

> It is not considered best-practice to include information in a footer for scripture publications. This is usually better placed in the header. However, if there is a need to have the page number at the footer for all pages (not just the 1st page of each book) then that can be set here. Similarly, you may want to add a DRAFT message and/or date to the end of each page. Note that you can select a preset option OR type your own text as needed.
>
> For example:  
> [\pagenumber]   places square brackets around the page number DRAFT\ \isodate\ \hrsmins   would give "DRAFT YYYY-MM-DD HH:MM"  
> -empty-     places nothing in that location
>
> Note that if you really must have Inner/Outer Footers, these can be set in the ptxprint-mods.tex file.
>
> It is not considered best-practice to include information in a footer for scripture publications. This is usually better placed in the header. However, if there is a need to have the page number at the footer for all pages (not just the 1st page of each book) then that can be set here. Similarly, you may want to add a DRAFT message and/or date to the end of each page. Note that you can select a preset option OR type your own text as needed. Note that if you really must have Inner/Outer Footers, these can be set in the ptxprint-mods.tex file.

**Explanation:**

The item printed in the middle of the footer on every page. On the first page of each book, the
settings in the **Other** area can replace it. **DRAFT** prints the word "DRAFT". You can type your
own text with the same codes and rules as the header, for example `DRAFT\ \isodate`. If you choose
**Time (HH:MM)** and the footer shows "<Enter ID>", type `\hrsmins` instead.

*(Internal ID: `ecb_ftrcenter` · Config key: `footer/ftrcenter`)*

#### Sec

- **Where:** Header+Footer tab › Footer
- **Type:** Radio button
- **Description:** Use formatting from secondary project (center footer)
- **View level:** Default and Full views
- **Only available when:** “Diglot (or Polyglot)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If setting the footer for a diglot you will need to specify whether this part of the footer (its text and formatting) should come from the Primary (Left) or the Secondary text.

**Explanation:**

For a diglot: use the **secondary** text's font (and references) for the footer. Greyed out until
diglot is turned on.

*(Internal ID: `r_ftrCenter_Sec` · Config key: `footer/ftrcenterside=Sec`)*

#### Pri

- **Where:** Header+Footer tab › Footer
- **Type:** Radio button
- **Description:** Use formatting from primary project (center footer)
- **View level:** Default and Full views
- **Only available when:** “Diglot (or Polyglot)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If setting the footer for a diglot you will need to specify whether this part of the footer (its text and formatting) should come from the Primary (Left) or the Secondary text.

**Explanation:**

For a diglot: use the **primary** text's font (and references) for the footer. Greyed out until
diglot is turned on.

*(Internal ID: `r_ftrCenter_Pri` · Config key: `footer/ftrcenterside=Pri`)*
