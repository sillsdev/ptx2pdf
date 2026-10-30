## What this tab is for

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

## Header

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

## Other

This area is only shown in the **Regular** and **Full** views.

* **Starting Page Number (for Scripture Books)** – the page number of the first page of the first
  Scripture book.
* **Print Page Number at Bottom of Intro Page(s)** and **Print Name of Saved Config on Intro Page(s)**
  choose what goes in the footer of the first page of each book. Only one can be ticked; ticking one
  unticks the other.

## Footer

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

## Common tasks

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

## Common problems

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

## Control notes

### @ecb_hdrcenter
A common choice is **Page Number** or **Reference Range**. The center place does not change sides
with **Mirror Pages**, but **First Reference** and **Last Reference** still swap on left-hand pages.

### @ecb_hdrright
With **Mirror Pages** ticked, this is the outer edge: right on right-hand pages, left on left-hand
pages. A common choice is **Page Number** or a reference.

### @ecb_hdrleft
With **Mirror Pages** ticked, this is the inner edge (next to the spine): left on right-hand pages,
right on left-hand pages. Many publications leave it **-empty-**.

### @r_hdrLeft_Pri
References use the primary text's book names, and its header font is used.

### @r_hdrLeft_Sec
References use the secondary text's book names, and its header font is used.

### @r_hdrCenter_Pri
Primary text's book names and font for the center item.

### @r_hdrRight_Pri
Primary text's book names and font for the outer item.

### @r_hdrCenter_Sec
Secondary text's book names and font for the center item.

### @r_hdrRight_Sec
Secondary text's book names and font for the outer item. A common diglot setup is **Pri** for one
side and **Sec** for the other, so each language has its own reference.

### @c_rangeShowChapter
Example: "Mark 4". Unticking it greys out **Verse**. Unticking can be useful for one-chapter books or
non-Bible publications.

### @c_rangeShowVerse
Example: "Mark 4:3–5:2" instead of "Mark 4–5".

### @r_CVsep_colon
If the Paratext project has its own chapter-verse separator, PTXprint uses that one.

### @r_CVsep_period
Example: "4.3".

### @c_rangeShowBook
The name comes from the book's `\h` line. Untick it if the book name is already elsewhere in the
header, for example with **Book (\h)**.

### @lb_style_h
The `\h` style sets the font, size and colour of the running header text. The footer also follows
it unless changed separately.

### @s_startPageNum
For example 101. Front matter before the first Scripture book is numbered separately (roman numerals
i, ii, iii … in PTXprint's front matter), and the Scripture numbering then starts at this number.

### @c_pageNumTitlePage
That page has no header, so without this it has no page number at all. Ticking this unticks
**Print Name of Saved Config on Intro Page(s)**.

### @c_printConfigName
Ticking this unticks **Print Page Number at Bottom of Intro Page(s)**. Untick it for the final
publication.

### @ecb_ftrcenter
On the first page of each book, the **Other** area settings can replace it. **DRAFT** prints the word
"DRAFT". Own text uses the same codes and rules as the header. For drafts, **Date and Time** shows
when each printout was made.

### @r_ftrCenter_Sec
Uses the secondary text's font (and references) for the footer.

### @r_ftrCenter_Pri
Uses the primary text's font (and references) for the footer.
