# Peripherals tab (front and back matter)

## What this tab is for

The **Peripherals** tab controls everything that is printed **around** the Scripture text:

* the **front matter** – the pages before the Scripture text, such as the title page, the
  copyright page and the table of contents;
* the **back matter** – pages after the Scripture text, such as maps and the colophon;
* a **cover** for the book;
* ready-made PDF files that you want to add at the front or at the back.

Come here when you want a title page, a table of contents, a copyright statement, maps or a
cover. The words on these pages are written in the front matter. You edit the front matter on
the **View+Edit** tab. The special codes that you can use there (`\zcopyright`, `\ztoc`,
`\zvar` and others) are explained in the **View+Edit** tab chapter. This chapter explains the
settings that turn these parts on and off, and the table of **variables** (the values that
PTXprint puts into the front matter, such as the main title).

**View levels:** In the **Basic** view this tab shows only **Table of Contents**, **Local
Front Matter** and the variables table. All other settings on this tab are only shown in the
**Default** and **Full** views. When one of the main options on this tab is turned on, the
name of the tab is shown in a different colour, so you can see that the tab is in use.

## Cover

PTXprint can make a cover for the book: a back cover, a spine (the narrow back edge of a
bound book) and a front cover, all on one wide page (the "cover spread"). PTXprint saves the
cover in its **own PDF file**. The file has the same name as the main PDF, with **_cover** at
the end. Printers usually print the cover on different paper, so they want it as a separate file.

* Tick **Create Cover Page** to make a cover each time you print.
* Click **Cover Wizard...** to design the cover step by step (see below).
* The four links **Back Cover**, **Spine**, **Front Cover** and **Cover Spread** open the
  matching style on the **Styles** tab. Each part of the cover is a sidebar (a box). There you
  can change its background colour, background picture, border and other box settings. Use
  **Cover Spread** for things that go across the whole cover, for example one picture behind
  the back, spine and front.

The text on each part of the cover comes from special sections of the front matter
(`coverfront`, `coverspine` and `coverback`, plus `coverwhole` for the whole spread). So the
cover needs **Local Front Matter**. If you untick **Local Front Matter**, PTXprint also unticks
**Create Cover Page** and shows a message about it. If the front matter has no cover sections,
no cover is made. The easiest way to create these sections is the **Cover Wizard**.

There is no separate Cover tab in this version of PTXprint. Use the **Cover Wizard** and the
four style links instead.

### The Cover Wizard

Click **Cover Wizard...** (you must tick **Create Cover Page** first). A window opens. The
steps are on the left and a preview of the whole cover is on the right. Use **Next** and
**Back** to move between the steps.

1. **Book and Spine Setup** – type the approximate number of pages. PTXprint fills this in
   from the last PDF if it can. Choose whether the book has a spine (most books with fewer than
   about 80 pages do not have spine text). If it has a spine, choose **Paperback** or
   **Hardcover**, and choose how to find the spine width: **Automatic** (from the paper
   weight in gsm or the paper thickness in µm) or **Manual** (type the width in mm). Ask your
   printer for the paper thickness if you can. Tick the right-to-left binding option for
   books in scripts such as Arabic or Hebrew, which open on the other side.
2. **Picture / decoration** – choose where the main picture goes (no picture, across the whole
   cover, front only, front and spine, back only, back and spine, or separate pictures for
   front and back). Choose the picture file, how it fits (stretch or crop), and its opacity.
   You can also add a decorative border to the front cover.
3. **Background** – white, or a solid colour behind everything. (Gradient shading is not
   available yet.)
4. **Front cover text** – type the title (you must type a title before you can go on). You can
   also add a subtitle, the language name and a picture. Move the position slider of each item
   to place it higher or lower on the front cover. You can also change its colour and size.
5. **Spine text** (only when the book has a spine) – choose what to show on the spine (title,
   subtitle, language name), its colour, size, direction and position. (The publisher name on
   the spine is not available yet.)
6. **Back cover** – add a short text (a "blurb"), an ISBN barcode and a logo, and choose
   where they go.
7. **Review** – check the summary and the preview, then click **Finish**.

When you click **Finish**, PTXprint:

* writes new cover sections into the front matter (this **replaces** any cover sections that
  were there before);
* changes the cover styles (background, border, picture, title colours and sizes);
* puts the title, subtitle, language name and ISBN into the variables **maintitle**,
  **subtitle**, **languagename** and **isbn** in the variables table on this tab.

**Cancel** closes the wizard without changing anything. PTXprint remembers your wizard
answers with the configuration, so you can open the wizard again later and make changes.

## Front Matter PDF(s) and Back Matter PDF(s)

Use these when part of the book already exists as a PDF file, for example a title page made in
another program, or a set of maps or an index made elsewhere.

* Tick **Front Matter PDF(s)** and click **Select...** to choose one or more PDF files that
  go **before** the Scripture text.
* Tick **Back Matter PDF(s)** and click **Select...** to choose PDF files that go **after**
  the Scripture text.

The names of the chosen files are shown next to the button. Hold the mouse over **Select...**
to see the full path of each file. The PDF pages must have the same page size as your
publication.

## Table of Contents

Tick **Table of Contents** to let PTXprint make a table of contents (a list of the books with
their page numbers). It is useful when you print several books.

* **Title** – the heading of the table of contents, for example "Contents" in your language.
* **Use \toc1 / \toc2 / \toc3** – each book in Paratext has up to three names: `\toc1` (the
  long name), `\toc2` (the short name) and `\toc3` (the abbreviation). Each name that you tick
  becomes one column in the table of contents. At least one must be ticked.
* **Leaders** – dots or a line between the book name and the page number.

Where does the table of contents appear?

* If **Local Front Matter** is **not** ticked, PTXprint makes its own contents page with your
  title before the Scripture text.
* If **Local Front Matter** is ticked, the table of contents appears where the front matter
  has the code `\ztoc|main\*` (see the **View+Edit** tab chapter). The BASIC front matter
  template already contains this code.

PTXprint can only know the page numbers after the text has been typeset. It therefore
typesets the publication more than once when you click **Print**. If **Quick Run** is ticked,
it typesets only once. Then the status line says "Rerun to fix: table of contents", and you
must click **Print** again.

## Local Front Matter

PTXprint does not print the FRT (front matter) book of your Paratext project directly. It
keeps its own copy for each configuration. You change this copy on the **View+Edit** tab. Tick
**Local Front Matter** to print it. The first time you tick it, PTXprint makes a simple front
matter for you (title page, copyright page and table of contents) if there is none yet.

* **Edit...** takes you to the **Front Matter** sub-tab of the **View+Edit** tab.
* **Force Page Break at each Periph** – each section of the front matter (title page,
  copyright page, preface …) starts on a new page. Leave it ticked unless you want short
  sections to share a page.
* **Suppress Blank Page Before Scripture Text** – normally the Scripture text starts on a
  right-hand page, and PTXprint adds a blank page when needed. Tick this to stop the blank page.
* **Use Peripheral Introductory Sections** – see below.

**Note:** When you tick **Local Front Matter**, PTXprint unticks **Colophon at End of
Publication**, because most front matter already has a copyright page. When you untick
**Local Front Matter**, PTXprint ticks the colophon again (and turns off the cover). Check
these two settings after you change one of them.

### Use Peripheral Introductory Sections

Some projects have an INT (introductions) book in Paratext, with sections such as an
introduction to the Old Testament or to the Gospels. Each section starts with a `\periph`
line that has an id. Tick **Use Peripheral Introductory Sections** to make PTXprint put each
section in front of the first book of its group. The ids that PTXprint knows are:

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

The section is only printed when a book of that group is in the list of books to print.
**Force Page Break at each Periph** also decides whether these sections start on a new page.

## Maps

* **Add Maps...** opens the **Add Map** dialog. There you choose map pictures, and PTXprint
  writes one page for each map into a map book (usually XXM). This dialog is explained in the
  **Pictures** tab chapter.
* **Include Maps** adds the map book to the list of books to print (and changes the **Basic**
  tab to **Multiple Books** if needed). Untick it to take the map book out of the list again.
  PTXprint saves the configuration when you change this setting.
* **Edit...** shows the map book on the **View+Edit** tab. Nothing happens if there is no
  map book yet.

## Colophon at End of Publication

A colophon is a short text at the very end of the book, for example the copyright, the
licence and the picture credits. Tick **Colophon at End of Publication** to show the text box.
PTXprint prints the colophon after the end of the last book.

* Type the colophon in the **Colophon Text** box. You can use USFM markers such as `\pc`
  (centred paragraph) and the special codes `\zcopyright`, `\zlicense` and
  `\zimagecopyrights` (see the **View+Edit** tab chapter).
* The reset button below the box puts back the standard colophon (copyright, licence, a blank
  line and the picture credits). For a diglot it also adds the copyright of the second
  language. Anything you typed is replaced.
* **Force Page Break Before Colophon** puts the colophon on a new page at the end, instead
  of under the last lines of the last book.

The picture credits (`\zimagecopyrights`) need the page numbers of the pictures. Click
**Print** a second time to get correct picture credits.

## Variables and Values

This table lists the **variables** used in the front matter (and in the colophon and cover).
A variable is a place-holder such as `\zvar|maintitle\*`. When you print, PTXprint puts the
value from this table in its place. The values are saved with the configuration. So two
configurations can use the same kind of front matter with different titles.

The table has three columns:

* **Pub** – tick this to make the variable a field of each publication on the
  **Publications** tab. Then each publication can have its own value (for example its own
  title). **maintitle** and **subtitle** are always used there.
* **Name** – the name of the variable. You cannot change it here.
* **Value** – click the value to change it. Press Enter to keep the new value.

Buttons:

* **Rescan peripheral variables** looks for all `\zvar|...\*` codes in the front matter and adds
  any missing ones to the table with the value `<Type Value Here>`. It saves the front matter
  first.
* **Add** asks for the name of a new variable. Use only letters, numbers and hyphens, and no
  spaces (for example `printedby` or `maintitlefr`).
* **Del** deletes the selected variables.

The variable `toctitle` is special: it always uses the **Title** of the **Table of Contents**,
so it is not in this table.

## Common tasks

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
5. If **Local Front Matter** is ticked, make sure that the front matter contains
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
4. Click **Print**, and then **Print** again, so that the picture credits are correct.

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

## Common problems

**The cover is not created.**
Check that **Local Front Matter** and **Create Cover Page** are both ticked. The front matter
must contain cover sections. Run the **Cover Wizard** and click **Finish** to create them.
Remember that the cover is in a **separate** PDF file (name ending in **_cover**), not in the
main PDF.

**Create Cover Page became unticked by itself.**
You unticked **Local Front Matter**. A cover cannot be made without it. Tick both again.

**The Cover Wizard button is greyed out.**
Tick **Create Cover Page** first.

**The Finish button in the Cover Wizard is greyed out.**
You must type a title in the front cover step, and you must be on the last (review) step.

**My hand-made changes to the cover text disappeared.**
**Finish** in the Cover Wizard replaces the cover sections of the front matter. Make the
changes again on the **View+Edit** tab after you use the wizard.

**The colophon disappeared after I turned on Local Front Matter.**
PTXprint unticks **Colophon at End of Publication** when you tick **Local Front Matter**. Tick
the colophon again if you want both.

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
**Rescan peripheral variables** (and generating front matter) adds every variable that is used
in the front matter. Remove the `\zvar` code from the front matter first, then delete the row.

**There is a blank page before the Scripture text.**
PTXprint starts the Scripture text on a right-hand page. Tick **Suppress Blank Page Before
Scripture Text** if you do not want this.

**The maps are printed although I do not want them.**
Untick **Include Maps**. This takes the map book out of the list of books to print.

**Most of the settings on this tab are missing.**
You are using the **Basic** view. Change to the **Default** or **Full** view.

## Settings reference: Peripherals tab (front and back matter)

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Peripherals tab

#### Create Cover Page

- **Where:** Peripherals tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Create an outer Cover
- **View level:** Default and Full views
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Create a cover (back, spine and front) as a separate PDF file ending in _cover.pdf. Needs Local Front Matter. Use the Cover Wizard... to design it.

**Explanation:**

Makes a cover each time you print, and saves it as a separate PDF whose name ends with
**_cover**. The cover pages are taken out of the main PDF. It needs **Local Front Matter**,
because the cover text is kept in cover sections of the front matter; if you untick **Local
Front Matter**, this is unticked too. Use **Cover Wizard...** to create the cover sections.

*(Internal ID: `c_makeCoverPage` · Config key: `cover/makecoverpage`)*

#### Cover Wizard...

- **Where:** Peripherals tab
- **Type:** Button
- **Description:** Generate Cover (Basic settings to create a cover)
- **View level:** Default and Full views
- **Only available when:** “Create Cover Page” is selected
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Creating a cover from nothing takes a lot of effort. This tool enables you to create various kinds of covers which can easily be enhanced.

**Explanation:**

Opens the Cover Wizard, which leads you through 6 or 7 steps (page count and spine, pictures,
background, front text, spine text, back cover, review) with a live preview. **Finish** writes
the cover sections into the front matter, sets the cover styles, and fills in the
**maintitle**, **subtitle**, **languagename** and **isbn** variables. Any cover sections that
were in the front matter before are replaced. Greyed out until **Create Cover Page** is ticked.

*(Internal ID: `btn_coverGenerate`)*

#### Back Cover

- **Where:** Peripherals tab
- **Type:** Link
- **View level:** Default and Full views
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the Sidebar properties on the Styles tab for the Back Cover.

**Explanation:**

Opens the **Styles** tab at the style of the back cover box. Change its background colour,
background picture, border or padding there. The text of the back cover is in the `coverback`
section of the front matter.

*(Internal ID: `lb_style_cat:coverback|esb`)*

#### Spine

- **Where:** Peripherals tab
- **Type:** Link
- **View level:** Default and Full views
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the Sidebar properties on the Styles tab for the Spine.

**Explanation:**

Opens the **Styles** tab at the style of the spine box (background, border, text direction).
The spine text is in the `coverspine` section of the front matter.

*(Internal ID: `lb_style_cat:coverspine|esb`)*

#### Front Cover

- **Where:** Peripherals tab
- **Type:** Link
- **View level:** Default and Full views
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the Sidebar properties on the Styles tab for the Front Cover.

**Explanation:**

Opens the **Styles** tab at the style of the front cover box. Use it to change the front
background colour or picture, or the border. The front cover text is in the `coverfront`
section of the front matter.

*(Internal ID: `lb_style_cat:coverfront|esb`)*

#### Cover Spread

- **Where:** Peripherals tab
- **Type:** Link
- **View level:** Default and Full views
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the Sidebar properties on the Styles tab for the whole Cover Spread (the background behind the back, spine and front).

**Explanation:**

Opens the **Styles** tab at the style for the whole cover spread (back, spine and front
together). It is the bottom layer: the back, spine and front boxes are placed on top of it.
Use it for a background colour or one picture that goes across the whole cover.

*(Internal ID: `lb_style_cat:coverwhole|esb`)*

#### Front Matter PDF(s)

- **Where:** Peripherals tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable import of front matter PDF(s)
- **View level:** Default and Full views
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> One or more previously created PDF file(s) can be included BEFORE the scripture material being typeset. If more than one file is selected, then these will appear in alphabetical order.
>
> If you are creating an electronic publication and want to add a fancy (colour) cover, then consider designing a cover using the online Canva.com tool.

**Explanation:**

Adds ready-made PDF pages before the Scripture text (and before the local front matter).
Use it for pages made in another program. The pages should have the same page size as the
publication. **Select...** is greyed out until this box is ticked.

*(Internal ID: `c_inclFrontMatter` · Config key: `project/ifinclfrontpdf`)*

#### Select...

- **Where:** Peripherals tab
- **Type:** Button
- **Description:** Select front matter PDF(s) to import
- **View level:** Default and Full views
- **Only available when:** “Front Matter PDF(s)” is selected
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Explanation:**

Choose one or more PDF files. Hold the Ctrl key to choose several. The file names are then
shown next to the button, and the full paths are shown when you hold the mouse over the
button. To change the list, click the button again and choose all the files you want.

*(Internal ID: `btn_selectFrontPDFs` · Config key: `project/frontincludes`)*

#### Table of Contents   Title

- **Where:** Peripherals tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable table of contents
- **View level:** Default and Full views
- **This tab/section appears when:** “Table of Contents   Title”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This will automatically generate the Table of Contents for all the books included in the publication using one or more of the \toc1, \toc2 and \toc3 fields as specified. This option is ignored unless the "Multiple Books" option has been set on the Basic tab.
>
> NOTE: PTXprint typesets the text more than once to get the page numbers right, so printing takes longer. (With Quick Run on, click Print a second time.) If Local Front Matter is on, put \ztoc|main\* in the front matter where the ToC should appear.

**Explanation:**

Turns on the automatic table of contents. Without **Local Front Matter**, PTXprint makes its
own contents page with the **Title**. With **Local Front Matter**, the table appears where the
front matter has `\ztoc|main\*`. PTXprint typesets several times to get the page numbers
right, so printing takes longer. With **Quick Run** ticked, click **Print** twice.

*(Internal ID: `c_autoToC` · Config key: `document/toc`)*

#### Table of contents title

- **Where:** Peripherals tab
- **Type:** Text box
- **View level:** Default and Full views
- **Only available when:** “Table of Contents   Title” is selected
- **This tab/section appears when:** “Table of Contents   Title”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The heading for the Table of Contents (for example 'Contents' in your language). It can also be used in the front matter as \zvar|toctitle\*

**Explanation:**

The heading of the table of contents, in the language of the publication. PTXprint uses it
on its own contents page, and the front matter can use it with `\zvar|toctitle\*`.

*(Internal ID: `t_tocTitle` · Config key: `document/toctitle`)*

#### Table of contents: Use \toc1

- **Where:** Peripherals tab
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Table of Contents   Title” is selected
- **This tab/section appears when:** “Table of Contents   Title”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Select which of the \toc markers should be included in the generated Table of Contents.

**Explanation:**

Uses the long book names (`\toc1` in Paratext) as a column of the table of contents. Ticked by
default. If you untick all three `\toc` options, PTXprint ticks this one again.

*(Internal ID: `c_usetoc1` · Config key: `document/usetoc1`)*

#### Table of contents: Use \toc2

- **Where:** Peripherals tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Table of Contents   Title” is selected
- **This tab/section appears when:** “Table of Contents   Title”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Select which of the \toc markers should be included in the generated Table of Contents.

**Explanation:**

Uses the short book names (`\toc2`) as a column of the table of contents. Tick it if you want
short names instead of, or as well as, the long names.

*(Internal ID: `c_usetoc2` · Config key: `document/usetoc2`)*

#### Table of contents: Use \toc3

- **Where:** Peripherals tab
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Table of Contents   Title” is selected
- **This tab/section appears when:** “Table of Contents   Title”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Select which of the \toc markers should be included in the generated Table of Contents.

**Explanation:**

Uses the book abbreviations (`\toc3`) as a column of the table of contents. Ticked by default.
If you use thumb tabs, the thumb tabs can also show the `\toc3` text; when this is unticked,
the thumb tab text must come from `\zthumbtab` instead.

*(Internal ID: `c_usetoc3` · Config key: `document/usetoc3`)*

#### Leaders

- **Where:** Peripherals tab
- **Type:** Drop-down list
- **Description:** Style of leaders for table of contents
- **View level:** Default and Full views
- **Choices:** None; ......................; . . . . . . . . . . . . .; - - - - - - - - -; ________________
- **Only available when:** “Table of Contents   Title” is selected
- **This tab/section appears when:** “Table of Contents   Title”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Leaders display dots or a line between the text and the page number. Select the style of leader you wish to apply.

**Explanation:**

The characters between each book name and its page number: close dots, spaced dots, dashes,
or a solid line. **None** leaves the space empty. Leaders help the reader follow the line
across a wide page.

*(Internal ID: `fcb_leaderStyle` · Config key: `document/tocleaders`)*

#### Use Peripheral Introductory Sections

- **Where:** Peripherals tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Check this option if the INT book contains peripheral divisions (sub-sections) which need to be inserted at the appropriate position between books. For example:  
>   \periph Old Testament Introduction|id="intot"  
>   \periph New Testament Introduction|id="intnt"  
>   \periph Gospels Introduction|id="intgospels"

**Explanation:**

Inserts sections of the INT book in front of the matching group of books, using the `\periph`
ids such as `intot`, `intnt` or `intgospels` (see the table in this chapter). A section is
only printed if a book of its group is being printed. Leave it unticked if your project has
no INT book with such sections.

*(Internal ID: `c_useSectIntros` · Config key: `project/sectintros`)*

#### Local Front Matter

- **Where:** Peripherals tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable (local) front matter
- **View level:** Default and Full views
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> PTXprint does not directly typeset the FRT book from Paratext. Instead, it uses a "local" PTXprint-specific copy of Paratext's FRT book which can be enhanced by additional codes which are described on the View+Edit tab's Information button.
>
> Note: turning this on turns the Colophon off (you can turn it on again). A cover needs Local Front Matter.

**Explanation:**

Prints the PTXprint front matter for this configuration (edited on the **View+Edit** tab).
The first time, PTXprint creates a simple front matter if there is none. Ticking this unticks
**Colophon at End of Publication**; unticking it ticks the colophon again and turns off
**Create Cover Page**.

*(Internal ID: `c_frontmatter` · Config key: `project/iffrontmatter`, `document/hasnofront_`)*

#### Edit...

- **Where:** Peripherals tab
- **Type:** Button
- **Description:** View (or edit) front matter
- **View level:** Default and Full views
- **Only available when:** “Local Front Matter” is selected
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Explanation:**

Goes to the **Front Matter** sub-tab of the **View+Edit** tab, where you can change the text
of the front matter.

*(Internal ID: `btn_editFrontMatter`)*

#### Force Page Break at each Periph

- **Where:** Peripherals tab
- **Type:** Checkbox (ticked by default)
- **Description:** Front matter: Force page break at each periph section
- **View level:** Default and Full views
- **Only available when:** “Local Front Matter” is selected
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This option is normally checked so that each different section of the front matter will begin on a new page.

**Explanation:**

Starts each `\periph` section of the front matter (and each introduction section from the INT
book) on a new page. Untick it only if you want short sections, such as a copyright notice and
a dedication, to follow each other on one page.

*(Internal ID: `c_periphPageBreak` · Config key: `project/periphpagebreak`)*

#### Suppress Blank Page Before Scripture Text

- **Where:** Peripherals tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Front matter: Suppress blank page at start of scripture text
- **View level:** Default and Full views
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> By default, the main body of scripture always starts on an odd (right-hand-side) page. PTXprint will automatically insert a pagebreak if needed to make this happen. If you wish to override this behavior, then check this option (to NOT insert a blank page after any front matter material).

**Explanation:**

Normally PTXprint makes the Scripture text start on a right-hand (odd) page, and adds a blank
page when needed. Tick this to start the Scripture text straight after the front matter. This
is useful for PDFs that are read on screen.

*(Internal ID: `c_periphSuppressPage` · Config key: `document/noblankpage`)*

#### Include Maps

- **Where:** Peripherals tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Add the map book (usually XXM) to the list of books to print. Use Add Maps... to create the map pages.

**Explanation:**

Adds the map book (usually XXM, chosen in the **Add Map** dialog) to the list of books to
print, and switches the **Basic** tab to **Multiple Books**. Unticking it removes the map book
from the list. PTXprint saves the configuration each time you change this.

*(Internal ID: `c_inclMaps` · Config key: `project/inclmaps`)*

#### Add Maps...

- **Where:** Peripherals tab
- **Type:** Button
- **Description:** Add Maps to the Publication
- **View level:** Default and Full views
- **Only available when:** “Include Maps” is selected
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Maps for the end of the publication can be added to one of the XX* books or to the XXM book using this dialog.

**Explanation:**

Opens the **Add Map** dialog, where you choose map pictures and their captions. PTXprint
writes one page for each map into the map book and adds the maps to the picture list. See the
**Pictures** tab chapter for the dialog.

*(Internal ID: `btn_addMaps1`)*

#### Edit...

- **Where:** Peripherals tab
- **Type:** Button
- **Description:** Edit Maps module
- **View level:** Default and Full views
- **Only available when:** “Include Maps” is selected
- **This tab/section appears when:** “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Switch to the View+Edit tab to show/edit the Maps module.

**Explanation:**

Shows the map book on the **View+Edit** tab, so that you can check or change it. Nothing
happens if the map book does not exist yet; use **Add Maps...** first.

*(Internal ID: `btn_editMaps1`)*

#### Colophon at End of Publication

- **Where:** Peripherals tab
- **Type:** Checkbox (ticked by default)
- **Description:** Enable colophon at end of publication
- **View level:** Default and Full views
- **This tab/section appears when:** “Colophon at End of Publication”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> What is a Colophon? A brief statement containing information about the publication such as the place of publication, the publisher, and the date of publication. This will be printed at the END of the book. Similar to a "biblio-page" or a "copyright-page" at the front of a book.
>
> NOTE: The picture credits (\zimagecopyrights) are only correct after you click Print a second time.

**Explanation:**

Prints the colophon text at the end of the last book. When you tick it and the text box is
empty, PTXprint fills in the standard colophon. It is unticked automatically when you tick
**Local Front Matter**, so tick it again if you want both.

*(Internal ID: `c_colophon` · Config key: `project/ifcolophon`)*

#### Back Matter PDF(s)

- **Where:** Peripherals tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable import of back matter PDF(s)
- **View level:** Default and Full views
- **This tab/section appears when:** “Back Matter PDF(s)”, “Front Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> One or more previously created PDF file(s) can be included AFTER the scripture material being typeset. If more than one file is selected, then these will appear in alphabetical order.

**Explanation:**

Adds ready-made PDF pages after the Scripture text, for example a glossary, an index or maps
made in another program. The pages should have the same page size as the publication.
**Select...** is greyed out until this box is ticked.

*(Internal ID: `c_inclBackMatter` · Config key: `project/ifinclbackpdf`)*

#### Select...

- **Where:** Peripherals tab
- **Type:** Button
- **Description:** Select back matter PDF(s) to import
- **View level:** Default and Full views
- **Only available when:** “Back Matter PDF(s)” is selected
- **This tab/section appears when:** “Back Matter PDF(s)”, “Front Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter”, “Colophon at End of Publication” is ticked

**Explanation:**

Choose one or more PDF files to add at the end. Hold the Ctrl key to choose several. The file
names are shown next to the button.

*(Internal ID: `btn_selectBackPDFs` · Config key: `project/backincludes`)*

#### Rescan peripheral variables

- **Where:** Peripherals tab
- **Type:** Button
- **View level:** Default and Full views
- **This tab/section appears when:** “Local Front Matter”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Clicking this button will rescan the Front Matter for any \zvar|variables\* and add any that are missing to this table of variable names and values.

**Explanation:**

Saves the front matter, then looks for every `\zvar|...\*` code in it. Any variable that is not
yet in the table is added with the value `<Type Value Here>` (and **copiesprinted** with 50).
Use it after you add new variables to the front matter by hand. Existing values are not changed.

*(Internal ID: `btn_rescanFRTvars`)*

#### tv_zvarEdit

- **Where:** Peripherals tab
- **Type:** Table
- **View level:** Default and Full views
- **This tab/section appears when:** “Local Front Matter”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Colophon at End of Publication” is ticked

**Explanation:**

The table of variables. Click a **Value** to change it, and press Enter to keep it. Tick **Pub**
to give each publication on the **Publications** tab its own value for that variable. The
**Name** cannot be changed; to rename a variable, add a new one and delete the old one.

*(Internal ID: `tv_zvarEdit`)*

#### Variables and Values

- **Where:** Peripherals tab
- **Type:** Label
- **View level:** Default and Full views
- **This tab/section appears when:** “Local Front Matter”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This table lists the standard set of \zvar|variables\* which can be used as part of front matter and/or colophon. As these \zvar|variables\* are customizable, you can add your own as needed. For example, you may need the \zvar|maintitle\* in more than one language so you can add 'fr' or 'es' to create a new one:  
>   \zvar|maintitlefr\* or you might want to add a custom variable such as:  
>    \zvar|printedby\*
>
> The values of these variables are saved with the config as they might vary from one publication to another.

#### Del

- **Where:** Peripherals tab
- **Type:** Button
- **Description:** Delete a peripheral variable
- **View level:** Default and Full views
- **This tab/section appears when:** “Local Front Matter”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Delete the currently selected variable(s).

**Explanation:**

Deletes the selected variables from the table. If the front matter still uses a variable, it
will come back the next time the variables are rescanned. You can select several rows with
Ctrl or Shift.

*(Internal ID: `btn_delzvar`)*

#### Add

- **Where:** Peripherals tab
- **Type:** Button
- **Description:** Add a peripheral variable
- **View level:** Default and Full views
- **This tab/section appears when:** “Local Front Matter”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Colophon at End of Publication” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Add a new variable.

**Explanation:**

Asks for the name of a new variable and adds it with an empty value. Use only letters, numbers
and hyphens (no spaces). Then type its value in the table, and use it in the front matter as
`\zvar|name\*`. Nothing is added if a variable with that name already exists.

*(Internal ID: `btn_addzvar`)*

### Peripherals tab › Colophon at End of Publication

#### Colophon Text

- **Where:** Peripherals tab › Colophon at End of Publication
- **Type:** Label
- **View level:** Default and Full views
- **Only available when:** “Colophon at End of Publication” is selected
- **Hidden until:** “Colophon at End of Publication” is ticked
- **This tab/section appears when:** “Colophon at End of Publication”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

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

#### Colophon text entry

- **Where:** Peripherals tab › Colophon at End of Publication
- **Type:** Text area
- **View level:** Default and Full views
- **Only available when:** “Colophon at End of Publication” is selected
- **Hidden until:** “Colophon at End of Publication” is ticked
- **This tab/section appears when:** “Colophon at End of Publication”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Note: There are several shortcuts you can use:  
>    (c) --> ©  the copyright sign  
>    (r) --> ®  to denote registered trademarks  
>    (tm) --> ™  to denote trademarks in general
>
> Other special codes converted at print time:  
> use ~ for places where a non-breaking space is needed use // where a line break needs to be forced but :// used in URLs will still be preserved

**Explanation:**

The text of the colophon, written with USFM markers. Start each paragraph with a marker such
as `\pc` (centred). The special codes `\zcopyright`, `\zlicense` and `\zimagecopyrights` insert
the copyright, the licence and the list of picture credits. For a translated picture-credit
list, add a language code, for example `\zimagecopyrightsfr`.

*(Internal ID: `textv_colophon`)*

#### Clicking this button will reload the default Colophon text m...

- **Where:** Peripherals tab › Colophon at End of Publication
- **Type:** Button
- **View level:** Default and Full views
- **Only available when:** “Colophon at End of Publication” is selected
- **Hidden until:** “Colophon at End of Publication” is ticked
- **This tab/section appears when:** “Colophon at End of Publication”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Clicking this button will reload the default Colophon text markers which include the Copyright statement tag, the License statement tag, and the Illustration credits tag. Your current colophon text will be replaced.

**Explanation:**

Replaces the colophon text with the standard text: copyright, licence, a blank line and the
picture credits. For a diglot it also includes the copyright of the second language. Your
own colophon text is lost.

*(Internal ID: `btn_resetColophon`)*

#### Force Page Break Before Colophon

- **Where:** Peripherals tab › Colophon at End of Publication
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Colophon at End of Publication” is selected
- **Hidden until:** “Colophon at End of Publication” is ticked
- **This tab/section appears when:** “Colophon at End of Publication”, “Front Matter PDF(s)”, “Back Matter PDF(s)”, “Table of Contents   Title”, “Local Front Matter” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Normally the colophon is inserted at the end of the last page of the last book. If this option is checked, then the colophon will appear at the bottom of a new page at the end of the publication.
>
> In Diglot publications, the colophon always appears on its own page - regardless of this setting.

**Explanation:**

Puts the colophon on a new page at the end of the book. Without it, the colophon follows the
last lines of the last book on the same page (if there is room).

*(Internal ID: `c_standAloneColophon` · Config key: `project/pgbreakcolophon`)*
