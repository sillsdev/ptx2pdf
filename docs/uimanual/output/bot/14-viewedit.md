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
