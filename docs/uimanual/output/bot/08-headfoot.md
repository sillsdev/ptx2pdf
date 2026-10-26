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
