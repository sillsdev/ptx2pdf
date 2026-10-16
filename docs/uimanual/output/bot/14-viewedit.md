# View+Edit tab

## What this tab is for

The **View+Edit** tab lets you look at the files that PTXprint uses and creates. For two of
these files you can also make changes here: the **front matter** (the pages before the
Scripture text, such as the title page and the table of contents) and the **Adj List**
(the list of paragraph adjustments).

Come here when you want to:

* create or change the front matter (title page, copyright page, contents page, preface);
* make a paragraph one line longer or shorter so that a page fits better;
* look at the text exactly as PTXprint sent it to the typesetting program;
* look at the log of the last print run when something went wrong.

This tab is only shown in the **Default** and **Full** views. In the **Basic** view you
cannot see it, but PTXprint still uses the front matter and Adj List that you made before.

## The sub-tabs: which files you may edit

The tab has several small tabs (sub-tabs) along the top. Each one shows one file.

| Sub-tab | What it shows | Can you edit it here? |
|---|---|---|
| **Front Matter** | The front matter for this configuration (title page, copyright page, contents, and so on). | **Yes.** This is the main place to edit front matter. |
| **Adj List** | A table of paragraph adjustments for the **Book in Focus**. | **Yes.** You can change values in the table. |
| **Final SFM** | The text of one book after PTXprint has applied all its changes, as it was sent to the typesetter. | **No – look only.** It is created again each time you print. |
| **.tex file** | The control file that PTXprint wrote for the last print run. | **No – look only.** |
| **XeTeX Log** | The log (report) of the last print run. | **No – look only.** |
| **Settings** (up to three) | Other settings files that you chose to open from the **Advanced** tab. | Advanced users only – see the **Advanced** tab chapter. |

**Important:** Changes to the Scripture text itself must be made in Paratext. Do not try to
correct the text on the **Final SFM** sub-tab. That file is replaced every time you print.

The **.tex file** and **XeTeX Log** sub-tabs are useful when you ask for help. A supporter may
ask you to look for an error message in the **XeTeX Log**. You do not need to understand
these files to use PTXprint.

Very long log files are cut short on the screen. Click **View/Edit...** to see the whole file
in your computer's text editor.

## The buttons at the top of the tab

The row of buttons at the top changes with the sub-tab that is open. Some buttons are greyed
out on sub-tabs where they do not apply.

* **Refresh** reloads the file from the disk. Any changes you have not saved are lost.
* **Book in Focus** chooses which book is shown. It is only active on the **Adj List** and
  **Final SFM** sub-tabs.
* **Generate** creates new content for the open sub-tab (see below).
* **View/Edit...** opens the file in your computer's own text editor. On the look-only sub-tabs
  the button is called **View Only...**.
* **Edit Variables...** (only on the **Front Matter** sub-tab) takes you to the table of
  variables on the **Peripherals** tab.
* The information button (only active on the **Front Matter** sub-tab) shows a list of special
  codes when you hold the mouse over it.
* **Autosave** decides whether changes are saved without asking.
* The slider changes the size of the text in the editing area.

### Saving your changes

When you change the text on an editable sub-tab, the name of the sub-tab turns red. This means
there are unsaved changes. PTXprint saves the changes:

* when you click somewhere outside the text area (without asking if **Autosave** is ticked,
  or after asking you if it is not ticked);
* when you click **Print** while an editable sub-tab is open.

If you do not want your changes, click **Refresh** (or press F5) before you click elsewhere.

If the configuration is locked (see the **Basic** tab), you cannot generate or save front
matter, and **Autosave** is turned off.

## The Generate button

**Generate** does a different job on each sub-tab:

* **Front Matter** – opens the **Generate Front Matter** dialog, so you can start the front
  matter from a template.
* **Adj List** – makes a new adjustment list for the books you are printing (see
  **The Adj List** below).
* **Final SFM** – makes the Final SFM file again for the **Book in Focus**, so you can look at it.

On the other sub-tabs **Generate** is greyed out.

## The Generate Front Matter dialog

This dialog appears when you click **Generate** on the **Front Matter** sub-tab. You choose one
of four starting points:

* **BASIC** – a title page, a page with copyright and licence information, and a table of
  contents. This is a good start for most projects.
* **ADVANCED** – more sections (title page, publication data, foreword, preface, table of
  contents, alphabetical contents). It contains sample English text. You must change the text
  into your language, or delete the sections you do not want.
* **DIGLOT** – a fuller template for diglot or polyglot publications (two or more languages).
  It is only available when **Diglot** is turned on for this configuration. Delete the
  sections you do not need.
* **PARATEXT** – copies the FRT (front matter) book from your Paratext project. It is greyed
  out if the project has no FRT book. After the copy, changes in Paratext are **not** copied
  here automatically. Generate again if you want the new Paratext version.

**Warning:** When you click **OK**, the new template **replaces** all of the front matter that
is there now. Your earlier changes are lost. If you have worked on your front matter, click
**Cancel**.

After you click **OK**, PTXprint also looks for variables (`\zvar|...\*` codes) in the new
front matter and adds any new ones to the variables table on the **Peripherals** tab.

## The front matter and its special codes (advanced)

The front matter uses USFM markers, the same kind of markers that Paratext uses (for example
`\mt1` for a main title and `\pc` for a centred paragraph). PTXprint also understands some
extra codes. These start with `\z` and are often called **z-codes**. Hold the mouse over the
information button to see a short list.

Each configuration has its own front matter. If you make a new configuration, check its
front matter too.

### Sections (periph)

The front matter is divided into sections. Each section starts with a line such as:

    \periph Title Page|id="title"

Each section normally starts on a new page.

### Text from other settings

* `\zcopyright` – the copyright statement from the **Basic** tab.
* `\zlicense` – the licence statement from the **Basic** tab. (Type it with an **s**.)
* `\zimagecopyrights` – a list of the pictures used, with their pages and copyright credits.
  You can add a language code at the end, for example `\zimagecopyrightsfr` for French.
  The list is only correct after you have printed **twice**, because PTXprint first needs to
  find out on which page each picture is.

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
`\toc1`, `\toc2` or `\toc3`). The table of contents must also be turned on with
**Table of Contents** on the **Peripherals** tab.

### Code Snippets buttons

On the **Front Matter** sub-tab, buttons under **Code Snippets** list ready-made codes in
groups (for example **Periph+Var**, **Insert**, **ISBN+QR**, **Contents**, **Pages**,
**Diglot**). Put the cursor where you want the code. Click a group button, then choose an item.
PTXprint inserts the code at the cursor. Hold the mouse over an item to see what it does.
The **Settings** sub-tabs have their own snippet buttons for the type of file that is open.

### Keyboard shortcuts in the front matter editor

* Ctrl+0 or Ctrl+comma – turn the current line into a comment (`\rem`), or back again.
* Ctrl+D – copy (duplicate) the current line.
* Ctrl+L – delete the current line.
* Ctrl+Up / Ctrl+Down – move the current line up or down.
* Ctrl+minus / Ctrl+equals – make the text in the editor smaller or larger.
* Alt+X – show the Unicode values of the selected characters in the status bar.

## The Adj List (adjustment list)

PTXprint fills each page with lines of text. Sometimes a page ends badly: for example, one
line of a paragraph is alone at the top of the next page, or the two columns do not end at
the same height. You can often fix this by asking PTXprint to set one paragraph a little
tighter (so it uses one line less) or a little looser (so it uses one line more).

The **Adj List** is the list of these requests. Each row is one paragraph. The columns are:

* **Book** and **C.V** – the book and the chapter and verse where the paragraph is.
* **Para** – which paragraph: 1 is the paragraph that contains the verse, 2 is the next one,
  and so on. This lets you adjust, for example, the paragraph after a heading.
* **Stretch** – the change. `+1` asks for one line more, `-1` for one line less. After
  **Generate**, you will also see values such as `+0`, `-0` or `+-0`. These mean "no change
  yet", and they show whether the paragraph *can* grow (+) or shrink (-).
* **Marker** – the paragraph marker (for example `p` or `q1`).
* **Expand** – how much the letters are spread out or squeezed, in percent. 100 is normal.
* **Parameters** and **Comment** – extra information.

Click a cell to change its value. To delete rows, select them and press the Delete key, or
right-click and choose **Delete Row(s)**.

For a diglot, the book code has an L or R after it (for example `MATL` and `MATR`), to say
which side the paragraph is on.

**Generate** on the **Adj List** sub-tab prints the books three times in the background (once
normal, once tight, once loose). From this it learns which paragraphs can shrink or grow. This
can take some time. If an Adj List already exists, PTXprint asks if you want to replace it
(**Yes**), merge the new information into it (**No** – the safe choice), or do nothing
(**Cancel**).

In most cases it is easier to make adjustments from the **PDF Preview** window. There you can
right-click a paragraph and choose to shrink or expand it. PTXprint writes those changes into
this same Adj List.

**Do paragraph adjustments last.** Any change to fonts, margins, pictures or other layout
settings moves the text, and your adjustments may then be wrong.

## Common tasks

### Create front matter for the first time

1. Go to the **Peripherals** tab and tick **Local Front Matter**. If there is no front matter
   yet, PTXprint makes a BASIC one for you.
2. Go to the **View+Edit** tab and click the **Front Matter** sub-tab.
3. If you want a different template, click **Generate**, choose **BASIC**, **ADVANCED**,
   **DIGLOT** or **PARATEXT**, and click **OK**.
4. Click **Edit Variables...** and type the values (title, subtitle and so on) in the
   **Value** column.
5. Click **Print**. If the front matter has a table of contents or picture credits, click
   **Print** a second time.

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
2. Open the PDF in the **PDF Preview** window and right-click the paragraph to shrink or
   expand it. This is the easiest way.
3. Or: on the **View+Edit** tab, click the **Adj List** sub-tab, choose the **Book in Focus**,
   find the paragraph and type `-1` or `+1` in the **Stretch** column.
4. Click **Print** and check the result.

### See what text PTXprint actually typeset

1. Click **Print** once, so the file exists.
2. On the **View+Edit** tab, click the **Final SFM** sub-tab.
3. Choose the book in **Book in Focus**.
4. Read the text. Do not edit it – make corrections in Paratext instead.

### Look at the log after a failed print

1. Click the **XeTeX Log** sub-tab.
2. Scroll to the end. Error messages usually start with `!`.
3. If the log is cut short, click **View Only...** to open the whole file.

## Common problems

**My changes to the front matter disappeared.**
You probably clicked **Generate** and then **OK**. This replaces the whole front matter. Or you
clicked **Refresh**, or answered "No" when PTXprint asked "Save changes?". There is no undo.
In future, keep a copy of important text before you generate a new template.

**The front matter does not appear in the PDF.**
**Local Front Matter** on the **Peripherals** tab must be ticked.

**A variable prints as "<Type Value Here>".**
PTXprint found the variable in the front matter but nobody has given it a value. Go to the
**Peripherals** tab and type a value for it in the variables table.

**The licence statement does not print.**
Check that the code is spelled `\zlicense` (with an **s**).

**The table of contents or the picture credits are empty or wrong.**
PTXprint needs a first print run to find the page numbers. Click **Print** again.

**The View+Edit tab is missing.**
You are using the **Basic** or **Minimal** view. Change the view level to **Default** or
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

## Settings reference: View+Edit tab

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Generate Front Matter (dialog)

#### OK

- **Where:** Generate Front Matter (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Replaces the current front matter with the template you chose. Anything you typed in the
front matter before is lost, so only click this if you really want to start again.

*(Internal ID: `btn_gnr8frt_ok`)*

#### Cancel

- **Where:** Generate Front Matter (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog and keeps your front matter as it is. Click this if you are not sure.

*(Internal ID: `btn_gnr8frt_cancel`)*

### Generate Front Matter (dialog) › Generate Front Matter

#### BASIC: Front matter contains just a few essentials with publication information

- **Where:** Generate Front Matter (dialog) › Generate Front Matter
- **Type:** Radio button
- **Description:** Generate front matter: BASIC (just the essentials)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This option will create a simple verso page containing essential copyright and licensing information followed by a table of contents.

**Explanation:**

The simplest template: a title page, a publication data page (copyright, licence and picture
credits) and a table of contents. The titles come from variables such as **maintitle** and
**subtitle**, so you only need to fill in the variables table on the **Peripherals** tab.
A good choice for most first-time users.

*(Internal ID: `r_generateFRT_basic`)*

#### ADVANCED: template contains several sections (some of which require editing before use)

- **Where:** Generate Front Matter (dialog) › Generate Front Matter
- **Type:** Radio button
- **Description:** Generate front matter: ADVANCED (requires editing)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This option will create an extensive template with multiple sections (each of which will start on a new page in the final publication). You will need to edit the sample text provided so that it communicates in the required language(s). You can also remove unwanted sections if they are inappropriate for this publication. Note: In order to make this template generic for several different publications in this project, you are encouraged to use \zvar|variables\*  which will be replaced with publication-specific info when printed. For example:  
> \mt1 \zvar|maintitle\*  
> \mt2 \zvar|subtitle\*  
> \pc \zvar|maintitlefr\*  
> \pc \zvar|subtitlefr\*  
> \pc \zvar|languagename\*  
> \pc \zvar|copiesprinted\*

**Explanation:**

A longer template with title page, publication data, foreword, preface, table of contents and
an alphabetical contents list. The foreword and preface contain sample English text that you
must replace or delete. It also uses more variables (for example **languagename**,
**copiesprinted**, **printedby**), which you fill in on the **Peripherals** tab.

*(Internal ID: `r_generateFRT_advanced`)*

#### Include sections for a separate cover page

- **Where:** Generate Front Matter (dialog) › Generate Front Matter
- **Type:** Checkbox (ticked by default)
- **Description:** Generate front matter: Include sections for cover page
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> (Not yet implemented) Enable this option if you want to include the following sections (used for creating a cover page):  
> \periph Cover - detailing text and optional picture  
> \periph Spine - text for the spine of the cover

**Explanation:**

This option does not do anything yet in the current version, whether it is ticked or not.
To make a cover, use **Create Cover Page** and the **Cover Wizard...** on the
**Peripherals** tab instead.

*(Internal ID: `c_includeCoverSections` · Config key: `project/inclcoverperiphs`)*

#### DIGLOT: template for a Diglot or Polyglot publication (deliberately fuller — delete sections you do not need)

- **Where:** Generate Front Matter (dialog) › Generate Front Matter
- **Type:** Radio button
- **Description:** Generate front matter: DIGLOT (for Diglot/Polyglot publications)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This option creates a DIGLOT / POLYGLOT front matter template designed for publications with two (or more) languages or scripts. It is deliberately more complete than the BASIC and ADVANCED templates because diglots are inherently complex: two (or more) texts, often two contents lists, two prefaces, sometimes two scripts and two writing directions. Delete the sections you do not need.
>
> Like the ADVANCED template it uses \zvar|variables\* and  
> \zglot|L\* / \zglot|R\* markers for column-specific content, so it requires editing before use and is NOT suitable for use inside Paratext without prior modification.
>
> If this option is disabled, the Diglot setting is not enabled for this configuration.

**Explanation:**

A template for publications with two or more languages. It includes sections for both
languages (for example two prefaces taken from each side's INT book) and also cover
sections. It is greyed out unless **Diglot** is turned on for this configuration. Expect to
delete several sections you do not need.

*(Internal ID: `r_generateFRT_diglot`)*

#### PARATEXT: Make a copy of the Project's FRT book (which may be edited to make use of \zvar|variables\*)

- **Where:** Generate Front Matter (dialog) › Generate Front Matter
- **Type:** Radio button
- **Description:** Generate front matter: PARATEXT (make a local copy)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This option will create a COPY of the Paratext project's FRT book to be used exclusively by PTXprint. You can edit the front matter to make use of PTXprint-specific  
> \zvar|variables\* but note that none of these edits will be reflected in Paratext. In addition, if you edit the FRT book in Paratext, those changes will not be reflected here until you regenerate this (local) Front Matter.
>
> If option is disabled, it is due to not having a FRT book in the Paratext project (so there is nothing to import).

**Explanation:**

Copies the FRT book from the Paratext project into PTXprint's own front matter. After that,
the two are separate: edits in Paratext do not appear here, and edits here do not go back to
Paratext. Use this if your team already keeps good front matter in Paratext. It is greyed out
if the project has no FRT book.

*(Internal ID: `r_generateFRT_paratext`)*

### View+Edit tab

#### Refresh

- **Where:** View+Edit tab
- **Type:** Button
- **Description:** Reload current file in view from saved version
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Discard any changes that have been made and restore the contents of this file as it was when last saved.
>
> Shortcut: F5

**Explanation:**

Reloads the file shown on the current sub-tab from the disk. Use it to throw away changes you
have not saved yet, or after you changed the file in an outside editor. It is greyed out on
the look-only sub-tabs.

*(Internal ID: `btn_refreshViewerText`)*

#### Book in Focus

- **Where:** View+Edit tab
- **Type:** Drop-down list
- **Description:** Book in focus for editor (or viewer)
- **View level:** Default and Full views
- **Choices:** NONE

**Tooltip (the text shown when you hover the mouse over it):**

> Choose any book (including those which are not currently in the list to be printed.)

**Explanation:**

Chooses the book shown on the **Adj List** and **Final SFM** sub-tabs. On other sub-tabs it is
greyed out. When printing a module instead of books, it is always greyed out.

*(Internal ID: `ecb_examineBook`)*

#### Generate

- **Where:** View+Edit tab
- **Type:** Button
- **Description:** Generate ... (context sensitive)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This button will (re-)generate content for Front Matter, AdjList(s) and Final SFM.
>
> If you only want to (re-)generate an Adj List for a single book, then just select that book on the Basic tab. Otherwise it will (re-)generate a Pic/Adj list for each of the books listed for printing.
>
> Shortcut: Ctrl-G

**Explanation:**

What it creates depends on the open sub-tab: the **Generate Front Matter** dialog on
**Front Matter**, a new adjustment list on **Adj List**, or a fresh Final SFM file for the
**Book in Focus** on **Final SFM**. Generating an Adj List prints the books three times in the
background, so it can take a while for large books.

*(Internal ID: `btn_Generate`)*

#### View/Edit...

- **Where:** View+Edit tab
- **Type:** Button
- **Description:** View (or edit) file in external editor
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> You may view (and in some cases edit) the file in your system's text Editor.
>
> Warning: If you edit settings in an external editor, be careful to save them (externally) and then click the refresh button (within PTXprint) before you hit Print. Otherwise you could lose changes that were made.
>
> If nothing happens when you click here, it is probably because you have not associated the file type (.sfm, .piclist, .adjlist, .tex, .log, .sty etc.) with a text editor (such as Notepad or NP++).
>
> Note that any changes to the Final SFM text get overwritten each time you hit Print. So any changes to the text or markers need to be made in Paratext.
>
> Shortcut: Ctrl-E

**Explanation:**

Opens the current file in your computer's own text editor, which can be easier for long files
or for searching. If you change a file there, save it in that editor and then click
**Refresh** in PTXprint before you print. Otherwise PTXprint may save its own older copy over
your changes.

*(Internal ID: `btn_viewEdit`)*

#### Edit Variables...

- **Where:** View+Edit tab
- **Type:** Button
- **Description:** Edit peripheral variables
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> If you have used \zvar_variable names in the front matter template, these may be edited on the "Pub. Info" tab. Click this button to show that tab.

**Explanation:**

Takes you to the variables table on the **Peripherals** tab. Before it goes there, it saves the
front matter and adds any new `\zvar` names it finds to the table, so you can type their values.
It is only shown on the **Front Matter** sub-tab.

*(Internal ID: `btn_editZvars`)*

#### Use the following codes to include special text in front mat...

- **Where:** View+Edit tab
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

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

**Explanation:**

An information button. Hold the mouse over it to see a short list of the special codes you
can type in the front matter. It is only active on the **Front Matter** sub-tab. See the section
"The front matter and its special codes" in this chapter for a fuller explanation.

*(Internal ID: `btn_infoViewEdit`)*

#### Autosave

- **Where:** View+Edit tab
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Save any changes made below without a confirmation check.

**Explanation:**

When ticked, PTXprint saves your edits as soon as you click outside the text area. When not
ticked, it asks "Save changes?" first. Untick it if you often experiment and want to be asked.
It is greyed out on the look-only sub-tabs and when the configuration is locked.

*(Internal ID: `c_autoSave` · Config key: `config/autosave`)*

#### Book in Focus

- **Where:** View+Edit tab
- **Type:** Slider
- **Description:** Adjust display font size
- **View level:** Default and Full views
- **Values:** from 8 to 20, default 12

**Tooltip (the text shown when you hover the mouse over it):**

> Use this slider to adjust the size of the text on the View+Edit tab as well as in other locations that use a specialized font or script.
>
> Keyboard Shortcuts:  
>   Ctrl-Minus - shrink text size  
>   Ctrl-Plus - grow text size

**Explanation:**

Changes only how large the text looks on the screen in the editor (and in some other boxes that
use the project font). It has no effect on the printed PDF.

*(Internal ID: `s_viewEditFontSize` · Config key: `config/displayfontsize`)*

#### Adj List

- **Where:** View+Edit tab
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

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

**Explanation:**

The name of the **Adj List** sub-tab. The table on this sub-tab shows one row per paragraph for
the **Book in Focus**. Type `+1` or `-1` in the **Stretch** column to make a paragraph one line
longer or shorter. See "The Adj List (adjustment list)" in this chapter for the meaning of
each column.

*(Internal ID: `l_AdjList`)*

#### Code Snippets

- **Where:** View+Edit tab
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Use the buttons below to insert various code snippets as required.

**Explanation:**

The heading over the snippet buttons. The buttons appear on the **Front Matter** and
**Settings** sub-tabs. Each button opens a menu of ready-made codes; choose one to insert it at
the cursor.

*(Internal ID: `l_codeSnippets`)*

#### More...

- **Where:** View+Edit tab
- **Type:** Link
- **Description:** Link to deeper technical help
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Online documentation on a structured list of code snippets which can be copied and pasted into the appropriate settings files.

**Explanation:**

Opens a web page that explains more code snippets. Most of these are for advanced users who
work with the settings files on the **Advanced** tab.

*(Internal ID: `lb_snippets`)*
