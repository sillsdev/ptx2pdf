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
