# Notes+Refs tab

## What this tab is for

The **Notes+Refs** tab controls the extra pieces of information that sit outside the main Bible text. It has three sub-tabs: **Footnotes**, **Cross-References** and **Study Notes + Questions**. Come here when you want to show or hide notes, change where they appear on the page, change the small marks that point to them, or add thousands of cross-references from a ready-made list.

There are three kinds of notes. In simple words:

* **Footnotes** (`\f` in the text) explain something about the text. For example: "Some old manuscripts add the words …" or "Hebrew: *son of Adam*". The translation team writes them in Paratext.
* **Cross-references** (`\x` in the text) are only lists of other Bible places that talk about the same thing. For example: "Gen 1:1; Ps 33:6". They can come from the project text, or PTXprint can add them from an external list.
* **Extended notes or study notes** (`\ef` in the text) are longer explanations, like the notes in a study Bible. PTXprint prints them in their own area at the bottom of the page, usually in two columns. Transcelerator comprehension questions are printed in this same area.

Some words used in this chapter:

* **Caller** – the small mark in the Bible text (for example *a*, *b* or †) that tells the reader "there is a note about this". The same mark is usually repeated at the start of the note.
* **Rule** – a thin horizontal line between the Bible text and the notes area.
* **Gutter** – the empty space between two columns.
* **pt** (point) – a small unit of measure. 1 pt is about 0.35 mm, and 72 pt is about 25 mm (1 inch).

The **Notes+Refs** tab is shown in the **Basic** view and above. Many settings are only shown in the **Default** or **Full** view. External cross-reference lists and extended study notes are only shown in the **Full** view.

## Footnotes

On the **Footnotes** sub-tab, the top area decides *whether* footnotes are printed and *where* they go.

* **Include Footnotes** turns all footnotes on or off. When it is off, PTXprint removes every `\f ... \f*` note before it makes the PDF, and most other footnote settings are greyed out.
* **Placement of Footnotes** has these choices:
  * **End of Page** – the normal choice. Notes appear at the bottom of the page where their caller is.
  * **End of Column** – only possible with a **Two Column Layout** (set on the **Layout** tab). The notes are set at the width of one column and appear at the bottom of the second column.
  * **End of Book** – the notes are collected and printed at the end of each book, as end notes.
  * **Side Margin** – the notes go in a narrow column next to the text, as close as possible to the line with the caller. This option is greyed out until you tick **Margin Notes Col Width (mm)** on the **Layout** tab (**Page Setup** area). If you turn margin notes off again, PTXprint moves the footnotes back to **End of Page**.
* **Start Each Footnote on a New Line** – normally short footnotes run on one after the other in one paragraph, which saves a lot of space. Tick this if each note must start on its own line.

### Callers

The caller settings decide which marks are used for footnotes.

* **Show Callers** (in the text) – when ticked, PTXprint uses the sequence of marks in the box next to it. Separate the marks with commas and no spaces, for example `a,b,c,d,e` or `†,‡,§`. The reload button next to the box loads the callers from the Paratext project settings.
* **Show Callers in Notes Area** – repeats the caller at the start of each note, so the reader can find the note that belongs to the mark.
* **Reset Callers on Page** – starts the sequence again at the first mark on every new page.
* **Override hidden/automatic Footnote caller settings** – in Paratext, each footnote says how its caller works: `\f +` (automatic caller), `\f -` (no caller), or a fixed mark. Normally PTXprint obeys what is in the text. When you tick this option, PTXprint ignores that and uses the **Show Callers** setting for every footnote.

### Rule and Space Settings

This area controls the line above the notes area and the space around it. **Space Above Rule** is the space between the last line of Bible text and the rule. **Space Below Rule** is the space between the rule and the first note. Even when the rule is hidden, PTXprint still leaves both spaces. The **Rule Positioning** settings (indent, length, thickness and horizontal position) are only shown in the **Full** view.

PTXprint draws only one rule above the notes at the bottom of the page. Normally it uses the footnote rule settings, even for cross-references. It uses the settings on the **Cross-References** sub-tab only when the footnotes are placed at the **End of Book**.

### Miscellaneous Footnote Settings

This area (only in the **Full** view) has small text changes that PTXprint makes in all notes, and the spacing between notes that run on in one paragraph:

* add a colon after quoted words in a note,
* keep a book name with its chapter and verse numbers,
* turn glossary words into footnotes,
* the minimum and maximum horizontal space between run-on notes,
* the vertical space between the footnote block and the cross-reference block.

## Cross-References

The **Cross-References** sub-tab works like the **Footnotes** sub-tab, but it also lets you add cross-references from an external list.

### Where the cross-references come from

* **Include Cross-References (From Project Text)** prints the `\x ... \x*` notes that the team typed in Paratext.
* **Use External List of Cross-References** (only in the **Full** view) adds cross-references from a list that comes with PTXprint, or from your own file. PTXprint changes the book names into the short book names of your project (the abbreviations in the Paratext **Scripture Reference Settings**, which should match the `\toc3` lines). These cross-references are added without a caller in the text. They are usually used for a study or reference Bible, together with **Column Cross-References**.

You can use both sources at the same time.

### Placement of Cross-References

* **End of Page** – at the bottom of the page.
* **End of Column** – at the bottom of the second column.
* **End of Book** – collected at the end of each book.
* **Below Footnotes** – at the bottom of the page, in a separate block under the footnotes.
* **Blend with Footnotes** – mixed in with the footnotes as one paragraph. This saves space. PTXprint sets the `\x` style so that it joins the footnotes.
* **Column Cross-References** – in a narrow column of their own beside the text, as in many reference Bibles. With a two-column layout the column is between the two text columns. With a one-column layout you can choose the side.
* **Side Margin** – in the margin-notes column, next to the line they belong to. This needs **Margin Notes Col Width (mm)** on the **Layout** tab.

PTXprint keeps the footnote and cross-reference placement in step:

* If you choose **End of Column** for one kind of note, the other kind moves to **End of Column** too, and the same for **End of Page**.
* If you choose **Column Cross-References**, the footnote placement changes to **End of Column**, and the **Source for References** area opens.
* If you untick **Include Footnotes** while cross-references are **Below Footnotes** or **Blend with Footnotes**, the cross-references move to **End of Page** (or to **Column Cross-References** if you use an external list).

The caller settings (**Show Callers**, **Show Callers in Notes Area**, **Reset Callers on Page**, **Override…**) work the same way as for footnotes.

### Source for References

This area (only in the **Full** view) is active when **Use External List of Cross-References** is ticked.

**External Refs** chooses the list:

* **Standard list (fewest)** to **Standard list (most)** – one large list of more than 340,000 cross-references. People have voted for the references, so the most useful ones come first. The five sizes take more or fewer of them. **Standard list (fewest)** gives only the most important references, and **Standard list (most)** gives the most. Start with **Standard list** and change it if the column is too empty or too full.
* **Strong's list (all)** and **Strong's list (project)** – cross-references grouped by Strong's number (a number for each Hebrew or Greek word). The **(project)** list only uses words that have a rendering in your project's Biblical Terms. These two choices make the **Strong's References** area available.
* **TSK list** – the Treasury of Scripture Knowledge. It is very large.
* **BibleWorks™ list** – about 112,000 cross-references.
* **UBS GNT92 list** and **UBS GNT92 list (DC)** – the United Bible Societies list. Use **(DC)** if you need Deuterocanonical references.
* **Select a Custom list...** – use your own file. Then click **Select...** to choose it.

Hover the mouse over the small information button next to **Select...** to read a description of the chosen list.

**Include Refs for Books in** removes references that point to books your readers do not have. For example, if only the New Testament is translated, choose **New Testament**.

### Strong's References

These settings are only available when the source is one of the Strong's lists. You can show the Strong's numbers in the cross-references, show them in the Bible text itself, and make an index book with **Generate Index...** (see the **Generate Strong's Index** dialog below).

### Column Cross-References

These settings are only available when the placement is **Column Cross-References**. They set the width of the column, the gutter next to it, the side of the page, the vertical rules, and how the references are placed in the column. The column takes space from the Bible text. A larger page size, or a smaller `\x` font (about 6 pt), can help.

### Rule and Space Settings

These settings are for the cross-reference rule. As explained under **Footnotes** above, PTXprint uses them only when footnotes are at the **End of Book**, or for the rule above cross-references printed at the **End of Book**.

## Study Notes + Questions

This sub-tab is for study Bibles and for comprehension testing.

### Extended Footnotes (\ef)

Tick **Extended Footnotes (\ef)** (only in the **Full** view) to print the `\ef ... \ef*` study notes from the text. They appear in their own area at the bottom of the page, in two columns, under the ordinary notes. If this box is not ticked, PTXprint removes all `\ef` notes before it makes the PDF. When the box is ticked, the area below shows settings for the gutter, the vertical rule between the two columns, callers, and the rule above the study notes.

**Sidebars (\esb ... \esbe)** prints the boxed sidebars of a study Bible. If it is not ticked, PTXprint removes them. The look of sidebars is set on the **Styles** tab and in the sidebar settings.

### Include Transcelerator Questions

Transcelerator is a Paratext plugin from SIL for making comprehension-checking questions. If your project has Transcelerator data, PTXprint can print the translated questions at the bottom of each page, in the same area as study notes. Each question appears near the verse it is about. This is useful for printouts for comprehension testing. The **Example Questions** text shows how your choices will look. If there is no Transcelerator data for the project, the checkbox is greyed out.

### Filter Categories

In a study Bible, notes and sidebars can have a category, for example `\cat History\cat*`. **Filter Categories** (only in the **Full** view) shows a list of the categories in the project, with a tick box for extended notes and for sidebars. In this version, PTXprint does not save this list with the configuration, and it does not use it when it makes the PDF.

## Generate Strong's Index dialog

To open this dialog, go to **Notes+Refs** › **Cross-References** and tick **Use External List of Cross-References**. Choose a **Strong's list** in **External Refs**, and then click **Generate Index...**.

The dialog makes a new book (in USFM, the Paratext file format) that lists each Strong's number and information about the word. Readers can use it to look up a number they see in the cross-references. You choose:

* which sections to include: Hebrew words, Greek words, and an optional **Reverse Index** (an alphabetical list of words in your language, with their numbers);
* what each entry shows: the Hebrew or Greek word, a transliteration (the word written in Latin letters), your project's term renderings, a key verse reference, the definition and notes;
* what to use when your project has no rendering for a word: a rendering from another project, or a gloss in a major language;
* the headings of the index (in the table), the book to use, and one or two columns.

When you click **Create Index**, PTXprint writes the index into the chosen book of your project (normally **XXS**). **Warning:** anything that was already in that book is replaced. PTXprint then adds the book to the list of books to print and changes the book selection to multiple books. Click **Print** to see it.

The renderings come from your project's Biblical Terms renderings in Paratext. Fill those in first for a useful index.

## Common tasks

### Hide all footnotes (or all cross-references)

1. Go to the **Notes+Refs** tab, **Footnotes** sub-tab.
2. Untick **Include Footnotes**.
3. For cross-references, go to the **Cross-References** sub-tab and untick **Include Cross-References (From Project Text)**. If **Use External List of Cross-References** is ticked, untick it too.
4. Click **Print**.

### Change the footnote callers to symbols

1. On **Notes+Refs** › **Footnotes**, make sure **Include Footnotes** and **Show Callers** are ticked.
2. In the box next to **Show Callers**, type the marks, separated by commas with no spaces, for example `*,†,‡,§`. Check that your font has these symbols.
3. If some notes still show other marks, tick **Override hidden/automatic Footnote caller settings**.
4. If you want the sequence to start again on each page, tick **Reset Callers on Page**.
5. Click **Print**. If the reset does not show correctly, click **Print** a second time.

### Put each footnote on its own line

1. On **Notes+Refs** › **Footnotes**, tick **Start Each Footnote on a New Line**.
2. To do the same for cross-references, go to the **Cross-References** sub-tab and tick **Start Each Cross-Reference on a New Line**.

### Move footnotes to the end of each book

1. On **Notes+Refs** › **Footnotes**, under **Placement of Footnotes**, choose **End of Book**.
2. Click **Print**. The notes appear after the last chapter of each book.

### Save space by mixing cross-references with footnotes

1. On **Notes+Refs** › **Cross-References**, under **Placement of Cross-References**, choose **Blend with Footnotes**.
2. Make sure **Include Footnotes** is ticked on the **Footnotes** sub-tab.
3. Click **Print**.

### Make a reference Bible with a column of cross-references

1. Choose the **Full** view.
2. On **Notes+Refs** › **Cross-References**, tick **Use External List of Cross-References**.
3. Under **Placement of Cross-References**, choose **Column Cross-References**.
4. In **Source for References**, choose a list in **External Refs** (for example **Standard list**).
5. In **Include Refs for Books in**, choose which books the references may point to (for example **New Testament**).
6. In **Column Cross-References**, set **Column Width (pts)** (start with 60) and, for a one-column layout, the **Side of page**.
7. Click **Print**. If the column is too full, choose a smaller list. If the text column becomes too narrow, use a larger page size or a smaller `\x` font on the **Styles** tab.

### Print study notes in two columns

1. Choose the **Full** view.
2. On **Notes+Refs** › **Study Notes + Questions**, tick **Extended Footnotes (\ef)**.
3. Adjust **Gutter Width (mm)** and, if you want a line between the columns, tick **Vertical Rule in Gutter**.
4. Click **Print**.

### Add Transcelerator questions to a printout

1. In Paratext, make sure the questions are translated in Transcelerator.
2. On **Notes+Refs** › **Study Notes + Questions**, tick **Include Transcelerator Questions**.
3. Check the **Language Code**. It must be the code of the language the questions were translated into.
4. Choose **Show Overview Questions**, **Number the Questions** and **Include Chapter:Verse References** as needed. Look at **Example Questions** to see the result.
5. Click **Print**.

### Create a Strong's index book

1. Choose the **Full** view. On **Notes+Refs** › **Cross-References**, tick **Use External List of Cross-References**.
2. In **External Refs**, choose **Strong's list (all)** or **Strong's list (project)**.
3. In the **Strong's References** area, click **Generate Index...**.
4. Choose the sections and entry parts you want. Edit the headings in the table if needed.
5. Check **Create Index in Book** (normally **XXS**). Anything already in that book will be replaced.
6. Click **Create Index**, then click **Print**.

## Common problems

**The footnote or cross-reference settings are greyed out.**
Most footnote settings are greyed out when **Include Footnotes** is not ticked. The caller box and the related settings are greyed out when **Show Callers** is not ticked. **End of Column** needs **Two Column Layout** on the **Layout** tab. **Side Margin** needs **Margin Notes Col Width (mm)** on the **Layout** tab. The **Source for References** settings need **Use External List of Cross-References**. The **Column Cross-References** settings need the **Column Cross-References** placement.

**I cannot find external cross-references, extended notes or the rule settings.**
These are only shown in the **Full** view. Change the view level and look again.

**The callers in the PDF are not the ones I typed.**
The notes in the text can ask for no caller (`\f -`) or a fixed caller. Tick **Override hidden/automatic Footnote caller settings** (or the cross-reference version), so that PTXprint uses your sequence for every note.

**Reset Callers on Page does not seem to work.**
PTXprint needs to know the page breaks first. Click **Print** a second time.

**The footnotes run into the footer.**
Increase **Space Above Rule (pt)** on the **Footnotes** sub-tab. This makes the page break a little earlier.

**My cross-reference placement changed by itself.**
PTXprint changes the footnote and cross-reference placements together, so that they make sense together (see "Placement of Cross-References" above). Check both sub-tabs after you change one of them.

**Changing the cross-reference rule settings has no effect.**
PTXprint draws only one rule above the notes at the bottom of the page. It uses the footnote rule settings, unless footnotes are at the **End of Book**. Change the rule on the **Footnotes** sub-tab instead.

**The external cross-references show the wrong book names.**
PTXprint uses the short book names from the Paratext project (**Scripture Reference Settings**, which should match the `\toc3` lines). Correct them in Paratext, then print again.

**Making the PDF is very slow.**
**Show Numbers in the Text** (for Strong's numbers) takes a lot of time. Untick it while you work on the layout. Very large cross-reference lists (for example **TSK list** or **Standard list (most)**) also make the PDF slower.

**Include Transcelerator Questions is greyed out.**
PTXprint cannot find Transcelerator data for this project. Use the Transcelerator plugin in Paratext for this project first. If the box can be ticked but no questions are printed, check that the **Language Code** matches the language the questions were translated into.

**The study notes do not appear.**
Tick **Extended Footnotes (\ef)** on the **Study Notes + Questions** sub-tab (this is only shown in the **Full** view). If it is not ticked, PTXprint removes all `\ef` notes.

## Settings reference: Notes+Refs tab

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Generate Strong's Index... (dialog)

#### Create Index

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Click to generate the index book (USFM file) which will be appended to the list of books to be printed.
>
> Warning: This will overwrite the existing book/file.

**Explanation:**

Makes the index book and closes the dialog. PTXprint adds the book to the list of books to print and changes the book selection to multiple books. Any text that was already in that book is replaced without another warning.

*(Internal ID: `btn_strong_ok`)*

#### Cancel

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog without making an index. Your choices in the dialog are kept.

*(Internal ID: `btn_strong_cancel`)*

#### For Strong's Cross References to be most useful to readers, it is highly recommended to include an Index at the end of the publication. Set appropriate options here to create an Index file (in USFM format).

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Label
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Set the options (below), to create the Index file in a temporary book (XXS, or XXA...XXG). After clicking "Create Index", the generated index book will be appended to the list of books to be printed.

#### Hebrew Words (from the OT)

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Checkbox (ticked by default)
- **Description:** Strong's index: Include section for Hebrew words
- **View level:** Default and Full views

**Explanation:**

Adds a section that lists the Hebrew Strong's numbers (the Old Testament words). Untick it if your publication is only the New Testament.

*(Internal ID: `c_strongsHeb` · Config key: `strongsndx/showhebrew`)*

#### Greek Words (from the NT)

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Checkbox (ticked by default)
- **Description:** Strong's index: Include section for Greek words
- **View level:** Default and Full views

**Explanation:**

Adds a section that lists the Greek Strong's numbers (the New Testament words). Untick it if your publication is only the Old Testament.

*(Internal ID: `c_strongsGrk` · Config key: `strongsndx/showgreek`)*

#### \li

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Link
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Click to select this marker on the Styles tab.
>
> Select which components should be included in the Strong's index when it is generated.

**Explanation:**

Opens the **Styles** tab at the `\li` style used for each entry in the Strong's index. Change it there to adjust the font size or indent of the entries.

*(Internal ID: `lb_style_li+strong-s`)*

#### Reverse Index (alphabetical listing with numbers)

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Checkbox (not ticked by default)
- **Description:** Strong's index: Include section for reverse index
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This (optional) section is intended for readers who want to look up a word in their own language to find out the Strong's number.

**Explanation:**

Adds a reverse index after the main lists. It lists your project's renderings in alphabetical order, each with its Strong's numbers. PTXprint sorts the words with the sorting rules of the Paratext project. This section can only be made when the project has Biblical Terms renderings.

*(Internal ID: `c_strongsNdx` · Config key: `strongsndx/showindex`)*

#### Hebrew or Greek Word

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Checkbox (ticked by default)
- **Description:** Strong's index entry: Include Hebrew and/or Greek
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The word in the source language(s) can be displayed in the index if useful to readers.

**Explanation:**

Shows the Hebrew or Greek word in each entry. Your font must contain Hebrew and Greek letters, or the words will not show correctly. The `\wh` and `\wg` styles control how these words look.

*(Internal ID: `c_strongsSrcLg` · Config key: `strongsndx/sourcelang`)*

#### Transliteration (Latin Script)

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Checkbox (not ticked by default)
- **Description:** Strong's index entry: Include transliteration of source languages
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> If the readers are unfamiliar with Greek and Hebrew it may be more useful in some contexts to show the transliterated (romanized) source language words.

**Explanation:**

Shows the Hebrew or Greek word written in Latin letters. This is often more useful than the original script for readers who do not know Hebrew or Greek. The `\wl` style controls how it looks.

*(Internal ID: `c_strongsTranslit` · Config key: `strongsndx/transliterate`)*

#### Term Rendering(s)

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Checkbox (ticked by default)
- **Description:** Strong's index entry: Include receptor term renderings
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Show the term renderings from the project's Biblical Terms list.

**Explanation:**

Shows how your project translated the word, from the Biblical Terms renderings in Paratext. This is usually the most useful part of each entry. If a word has no rendering, PTXprint uses the fallback settings below.

*(Internal ID: `c_strongsRenderings` · Config key: `strongsndx/renderings`)*

#### If No Local Rendering Found

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Label
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> If no local term rendering is found in the Project's list of Biblical Term renderings, then several fallback options are possible:  
> a) Use the renderings from a regional language project b) Use a gloss from one of the majority languages c) Use the Biblical Term's definition (in English)

#### Key Verse Reference

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Checkbox (ticked by default)
- **Description:** Strong's index entry: Include key verse reference
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The primary book, chapter and verse reference for the entry helps users find the first item in the list of cross-references related to the term.

**Explanation:**

Adds one main Bible reference for the word. The `\xt` style controls how it looks.

*(Internal ID: `c_strongsKeyVref` · Config key: `strongsndx/keyvrsrefs`)*

#### Definition

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Checkbox (not ticked by default)
- **Description:** Strong's index entry: Include definitions
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Show the definition in addition to the term rendering(s).

**Explanation:**

Adds the definition of the word (in English) after the renderings. It makes the index longer.

*(Internal ID: `c_strongsDefn` · Config key: `strongsndx/definitions`)*

#### \wl

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Link
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Click to select this marker on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the `\wl` style (the transliteration) used in the Strong's index.

*(Internal ID: `lb_style_wl+strong-s`)*

#### \xt

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Link
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Click to select this marker on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the `\xt` style (the key verse reference) used in the Strong's index.

*(Internal ID: `lb_style_xt+strong-s`)*

#### \wh

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Link
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Click to select this marker on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the `\wh` style (Hebrew words) used in the Strong's index. You can choose a font with Hebrew letters there.

*(Internal ID: `lb_style_wh+strong-s`)*

#### \wg

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Link
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Click to select this marker on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the `\wg` style (Greek words) used in the Strong's index. You can choose a font with Greek letters there.

*(Internal ID: `lb_style_wg+strong-s`)*

#### Remove (Comments) from Renderings

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Checkbox (not ticked by default)
- **Description:** Strong's index entry: Remove comments from renderings
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Paratext allows for additional comments or notes to be added (in brackets) after term renderings. Check this option to prevent these from showing in the Strong's index.

**Explanation:**

Removes any text in round brackets ( ) from the renderings. In Paratext, translators often add comments in brackets after a rendering. Readers usually do not need them.

*(Internal ID: `c_strongsNoComments` · Config key: `strongsndx/nocomments`)*

#### Wildcard* handling

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Drop-down list
- **Description:** Strong's index entry: How to handle wildcard* character
- **View level:** Default and Full views
- **Choices:** Keep wildcard*; Remove wildcard; Change to hyphen-

**Tooltip (the text shown when you hover the mouse over it):**

> The asterisk * is used as a matching wildcard in Term Renderings. If you prefer for this not to be displayed, select an appropriate option.

**Explanation:**

Renderings in Paratext can contain `*` to match several word forms (for example `bless*`). Choose **Keep wildcard*** to print the `*`, **Remove wildcard** to delete it, or **Change to hyphen-** to print a hyphen instead.

*(Internal ID: `fcb_strongswildcards` · Config key: `strongsndx/wildcards`)*

#### tv_strvarEdit

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Table
- **View level:** Default and Full views

**Explanation:**

A table of the headings PTXprint uses in the index: the title of the book (`index_book_title`), the Hebrew and Greek section titles, and the title of the reverse index. Click a value to type the heading in your language.

*(Internal ID: `tv_strvarEdit`)*

#### Create Index in Book

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Drop-down list
- **Description:** Strong's index: Extra book code to be used
- **View level:** Default and Full views
- **Choices:** XXS; XXA; XXB; XXC; XXD; XXE; XXF; XXG

**Tooltip (the text shown when you hover the mouse over it):**

> Select the temporary book to be used for the generated Strong's Cross Reference Index.
>
> By default, an extra book XXS is used to store the index. But if you prefer to use one of the other standard Paratext books XXA...XXG then select it here, but be aware that it will overwrite whatever is in that book without prior warning.

**Explanation:**

The book code PTXprint writes the index into. **XXS** is the default. You can choose one of the other extra books (**XXA** to **XXG**). Choose a book you do not use for anything else, because its contents are replaced.

*(Internal ID: `fcb_strongsNdxBookId` · Config key: `strongsndx/ndxbookid`)*

#### Two Column Layout

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Checkbox (ticked by default)
- **Description:** Strong's index: Use 2-column layout
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Using a two column layout for the index is highly recommended, but if you prefer a one column layout, uncheck this option.

**Explanation:**

Prints the index in two columns. This is recommended, because the entries are short. Untick it for one column.

*(Internal ID: `c_strongs2cols` · Config key: `strongsndx/twocols`)*

#### Open Index File in Editor

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Checkbox (not ticked by default)
- **Description:** Strong's index: Open index file after creating it
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Check this option to open the generated file in a text editor after the Index has been created.

**Explanation:**

Opens the new index file in your computer's text editor after it is made, so you can check it.

*(Internal ID: `c_strongsOpenIndex` · Config key: `strongsndx/openineditor`)*

#### Unbalanced Lines (max)

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Number box
- **Description:** Strong's index: Allow unbalanced lines
- **View level:** Default and Full views
- **Only available when:** “Two Column Layout” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> By default (when this is set to 0) PTXprint will balance the number of lines used in each column. Sometimes this results in large empty spaces at the end of a page.
>
> Increasing this number (recommended range 1-4) will allow up to that many unbalanced lines on the page.

**Explanation:**

Allows up to this many lines of difference between the two columns of the index. Only available when **Two Column Layout** is ticked in this dialog. A value of 1 to 4 can avoid large empty spaces.

*(Internal ID: `s_strongRag` · Config key: `strongsndx/raglines`)*

#### Notes

- **Where:** Generate Strong's Index... (dialog)
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This is the Description field from the project's Biblical Terms renderings.

**Explanation:**

Adds the description text from the project's Biblical Terms renderings to each entry. This setting is not saved with the configuration.

*(Internal ID: `c_strongsNotes`)*

### Generate Strong's Index... (dialog) › If No Local Rendering Found:

#### Use the Term Rendering from a Fallback Project

- **Where:** Generate Strong's Index... (dialog) › If No Local Rendering Found:
- **Type:** Label
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Select the project to search within for a term rendering for entries which do not have a local rendering.

#### Use Major Language Gloss

- **Where:** Generate Strong's Index... (dialog) › If No Local Rendering Found:
- **Type:** Drop-down list
- **Description:** Strong's index: Use major language gloss (if no rendering found)
- **View level:** Default and Full views
- **Choices:** None; English; French; Indonesian; Portuguese; Spanish

**Tooltip (the text shown when you hover the mouse over it):**

> If all else fails, you can display the gloss in a major language.

**Explanation:**

If PTXprint finds no rendering in your project or in the fallback project, it can show a short meaning (gloss) of the word in a major language. Choose **None** to leave these words without a gloss.

*(Internal ID: `fcb_strongsMajorLg` · Config key: `strongsndx/majorlang`)*

#### Use Major Language Gloss

- **Where:** Generate Strong's Index... (dialog) › If No Local Rendering Found:
- **Type:** Label
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> If all else fails, you can display the gloss in a major language.

#### Use the Term Rendering from a Fallback Project

- **Where:** Generate Strong's Index... (dialog) › If No Local Rendering Found:
- **Type:** Drop-down list
- **Description:** Strong's index: Use fallback project (if no rendering found)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Select the project to search within for a term rendering for entries which do not have a local rendering.

**Explanation:**

Choose another Paratext project, for example a project in a regional language. PTXprint uses its Biblical Terms renderings for words that have no rendering in your project.

*(Internal ID: `fcb_strongsFallbackProj` · Config key: `strongsndx/fallbackprj`)*

### Notes+Refs tab › Footnotes tab

#### Show Callers in Notes Area

- **Where:** Notes+Refs tab › Footnotes tab
- **Type:** Checkbox (ticked by default)
- **Description:** Show footnote callers in notes area
- **View level:** Default and Full views
- **Only available when:** “Include Footnotes”, “Show Callers in the Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Usually the "Caller" symbol is also shown in the notes area which helps the reader quickly find the footnote from the text.

**Explanation:**

When ticked, the caller is also printed at the start of the footnote. Untick it to print the note without the mark, which saves a little space. Greyed out when **Show Callers** is not ticked.

*(Internal ID: `c_fnomitcaller` · Config key: `notes/fnomitcaller`)*

#### Reset Callers on Page

- **Where:** Notes+Refs tab › Footnotes tab
- **Type:** Checkbox (ticked by default)
- **Description:** Reset footnote callers on each page
- **View level:** Default and Full views
- **Only available when:** “Include Footnotes”, “Show Callers in the Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If this is checked, then the sequence of callers starts again from the 1st item in the list of callers specified.
>
> Note that this feature doesn't always take effect straight away. You may need to hit Print a second time before it applies.

**Explanation:**

Starts the caller sequence again at the first mark on each page. This keeps the callers short when you use symbols. PTXprint needs to know the page breaks first, so you may need to click **Print** twice.

*(Internal ID: `c_fnpageresetcallers` · Config key: `notes/fnresetcallers`)*

#### Show Callers in the Text

- **Where:** Notes+Refs tab › Footnotes tab
- **Type:** Checkbox (ticked by default)
- **Description:** Show Footnote Callers in the Text
- **View level:** Default and Full views
- **Only available when:** “Include Footnotes” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> A "Caller" is a symbol (in the text) which alerts the reader that there is further information (in this case a footnote at the bottom of the page). Ideally, the caller should be distinct from the rest of the text, so a symbol works well if supported by the font. Otherwise the letters of the alphabet can be used.
>
> Separate callers with a comma (no spaces). For example: a,b,c,d,e,f,g,h, etc. or:  †,‡,§,∥,#    or: ✶,☆,✦,✪
>
> If you do not see the callers you are expecting in the PDF, then try using the "Override..." setting above.

**Explanation:**

When ticked, PTXprint uses the marks in the box next to it as callers. When not ticked, the box is greyed out, and no automatic caller sequence is used. Together with **Override hidden/automatic Footnote caller settings**, unticking it removes the callers from all footnotes.

*(Internal ID: `c_fnautocallers` · Config key: `notes/iffnautocallers`)*

#### Footnote Caller Sequence Entry

- **Where:** Notes+Refs tab › Footnotes tab
- **Type:** Text box
- **View level:** Default and Full views
- **Only available when:** “Include Footnotes”, “Show Callers in the Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> These callers should automatically be loaded from the settings in the Paratext project, but can be modified here if needed. (Use the button on the right to reload them if needed.)
>
> Separate callers with a comma (no spaces). For example: a,b,c,d,e,f,g,h, etc. or:  †,‡,§,∥,#    or: ✶,☆,✦,✪

**Explanation:**

Type the marks to use in order, separated by commas and no spaces, for example `a,b,c,d,e,f` or `*,†,‡,§`. When the sequence reaches the end, it starts again. Make sure your font has the symbols you type.

*(Internal ID: `t_fncallers` · Config key: `notes/fncallers`)*

#### Reload footnote callers from Paratext

- **Where:** Notes+Refs tab › Footnotes tab
- **Type:** Button
- **View level:** Default and Full views
- **Only available when:** “Include Footnotes”, “Show Callers in the Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Clicking this button will reload the footnote callers from the Paratext project settings.
>
> If the callers have not been defined in the Paratext project, or are already showing, then a default set will appear.

**Explanation:**

Loads the footnote callers from the Paratext project settings. If Paratext has none, or they are already in the box, PTXprint puts in its own default sequence (`a,b,c,d,e,f,✶,☆,✦,✪,†,‡,§`).

*(Internal ID: `btn_resetFNcallers`)*

#### Override hidden/automatic Footnote caller settings

- **Where:** Notes+Refs tab › Footnotes tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Override Footnote Settings in Text
- **View level:** Default and Full views
- **Only available when:** “Include Footnotes” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> The Footnotes specified in Paratext use  
> \f +(plus) to cycle through the callers, or \f - (minus) to omit the caller.
>
> If this option is enabled, the Show Callers settings below will override whatever has been specified within the text itself.

**Explanation:**

Use this when the callers in the PDF do not follow your settings. In the text, each footnote starts with `\f +` (automatic caller), `\f -` (no caller), or a fixed mark. When this box is ticked, PTXprint changes every footnote to `+` if **Show Callers** is ticked, or to `-` if it is not.

*(Internal ID: `c_fnOverride` · Config key: `notes/fnoverride`)*

#### Start Each Footnote on a New Line

- **Where:** Notes+Refs tab › Footnotes tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Include Footnotes” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Normally footnotes are arranged one after the other to form a block of text. But if you require each footnote to start on its own new line then set this option.

**Explanation:**

Each footnote starts on a new line, like a list. This uses more space than notes that run on in one paragraph. When both this and **Start Each Cross-Reference on a New Line** are ticked, the horizontal spacing settings are greyed out, because they are only used for run-on notes.

*(Internal ID: `c_fneachnewline` · Config key: `notes/fneachnewline`)*

#### \f

- **Where:** Notes+Refs tab › Footnotes tab
- **Type:** Link
- **View level:** Default and Full views
- **Only available when:** “Include Footnotes” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the Footnote properties on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the `\f` (footnote) style. There you can change the font size, line spacing and other properties of footnotes.

*(Internal ID: `lb_style_f`)*

#### End of Book

- **Where:** Notes+Refs tab › Footnotes tab
- **Type:** Radio button
- **Description:** Placement of footnotes: End notes
- **View level:** Default and Full views
- **Only available when:** “Include Footnotes” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This option will prevent footnotes showing on each page, but will gather them together and place them all at the end of the book.

**Explanation:**

Footnotes are not printed on each page. PTXprint collects them and prints them at the end of each book. Use this when there are few notes or when you want clean pages.

*(Internal ID: `r_fnpos_endnote` · Config key: `notes/fnpos=endnote`, `notes/columnnotes_=endnote`, `notes/endnotes_=endnote`, `notes/fnmarginal_=endnote`)*

#### End of Column

- **Where:** Notes+Refs tab › Footnotes tab
- **Type:** Radio button
- **Description:** Placement of footnotes: End of column
- **View level:** Default and Full views
- **Only available when:** “Two Column Layout”, “Include Footnotes” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Use this option (only available in 2-column layout) to show the footnotes at the end of the 2nd column of text.
>
> Footnotes and cross-references at the foot of the page are kept together, so changing this may also change where the cross-references are placed.

**Explanation:**

Puts the footnotes at the bottom of the second column, at the width of one column. Only available with **Two Column Layout** on the **Layout** tab. If cross-references are at **End of Page**, they also move to **End of Column**.

*(Internal ID: `r_fnpos_column` · Config key: `notes/fnpos=column`, `notes/columnnotes_=column`, `notes/endnotes_=column`, `notes/fnmarginal_=column`)*

#### End of Page

- **Where:** Notes+Refs tab › Footnotes tab
- **Type:** Radio button
- **Description:** Placement of footnotes: End of page
- **View level:** Default and Full views
- **Only available when:** “Include Footnotes” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Footnotes (and cross-references) are usually placed at the end of each page.

**Explanation:**

The usual choice. Footnotes are printed at the bottom of the page on which their caller appears. If cross-references are at **End of Column**, they move to **End of Page** too.

*(Internal ID: `r_fnpos_normal` · Config key: `notes/fnpos=normal`, `notes/columnnotes_=normal`, `notes/endnotes_=normal`, `notes/fnmarginal_=normal`)*

#### Include Footnotes

- **Where:** Notes+Refs tab › Footnotes tab
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Select whether footnotes should be included.
>
> The specific settings for these are located on the Footnotes tab.

**Explanation:**

Untick this to leave all footnotes out of the PDF. The notes stay in your Paratext project. When unticked, most footnote settings are greyed out. If cross-references were set to **Below Footnotes** or **Blend with Footnotes**, PTXprint moves them to another placement.

*(Internal ID: `c_includeFootnotes` · Config key: `notes/includefootnotes`)*

#### Only show verse numbers from \fr

- **Where:** Notes+Refs tab › Footnotes tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The footnote reference \fr usually includes the chapter & verse number like this 3:16. If you prefer to hide the chapter, so that only 16 is shown, then enable this option.

**Explanation:**

At the start of a footnote, the reference (`\fr`) usually shows chapter and verse, for example `3:16`. Tick this to show only the verse number, `16`. This saves space, because the chapter is usually clear from the page.

*(Internal ID: `c_frVerseOnly` · Config key: `notes/frverseonly`)*

#### Side Margin

- **Where:** Notes+Refs tab › Footnotes tab
- **Type:** Radio button
- **Description:** Placement of footnotes: Side Margin
- **View level:** Default and Full views
- **Only available when:** “Margin Notes Col Width (mm)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This option will place footnotes (and optionally also the Cross-references and Section Headings) in a column next to the text and align them as closely as possible vertically to their caller.

**Explanation:**

Puts footnotes in the margin-notes column next to the text, as close as possible to the line with the caller. Greyed out until **Margin Notes Col Width (mm)** is ticked on the **Layout** tab. If you turn margin notes off, the footnotes go back to **End of Page**.

*(Internal ID: `r_fnpos_margin` · Config key: `notes/fnpos=margin`, `notes/columnnotes_=margin`, `notes/endnotes_=margin`, `notes/fnmarginal_=margin`)*

### Notes+Refs tab › Footnotes tab › Rule and Space Settings

#### Space Above Rule (pt)

- **Where:** Notes+Refs tab › Footnotes tab › Rule and Space Settings
- **Type:** Number box
- **Description:** Space above footnote rule
- **View level:** Default and Full views
- **Values:** from -50 to 50, default 6

**Tooltip (the text shown when you hover the mouse over it):**

> The vertical space between the main text body and the footnote rule.
>
> Note: if you make this value less than the descenders of the last lines of text, then the footnotes will push down into the footer area. If you see this happening, increase this value to trigger an earlier page break to solve the problem.
>
> The vertical space between the body text and the area containing footnotes and cross-references.
>
> If the Footnote Rule is not shown, the vertical space will still be calculated as the Space Above plus the Space Below (the imaginary) Rule.

**Explanation:**

The space (in pt) between the last line of text and the notes rule. The default is 6. Increase it if the notes push into the footer, or if the notes look too close to the text. Negative values are possible but rarely useful.

*(Internal ID: `s_fnAboveSpace` · Config key: `notes/abovenotespace`)*

#### Space Below Rule (pt)

- **Where:** Notes+Refs tab › Footnotes tab › Rule and Space Settings
- **Type:** Number box
- **Description:** Space below footnote rule
- **View level:** Default and Full views
- **Values:** from -50 to 50, default 2
- **Only available when:** “Show Footnote Rule” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This is the vertical space/gap (pts) between the rule and the footnotes.

**Explanation:**

The space (in pt) between the rule and the first line of the notes. The default is 2. PTXprint adds this space even when the rule is hidden. Greyed out when **Show Footnote Rule** is not ticked.

*(Internal ID: `s_fnBelowSpace` · Config key: `notes/belownoterulespace`)*

#### Show Footnote Rule

- **Where:** Notes+Refs tab › Footnotes tab › Rule and Space Settings
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This is the horizontal rule separating the body text from the footnote area.

**Explanation:**

Shows or hides the line above the notes at the bottom of the page. This line is also used above cross-references at the bottom of the page. Untick it for a cleaner look. The space above and below is kept.

*(Internal ID: `c_footnoterule` · Config key: `notes/iffootnoterule`)*

#### Rule Positioning and Parameters

- **Where:** Notes+Refs tab › Footnotes tab › Rule and Space Settings
- **Type:** Number box
- **Description:** Footnote rule: Indent
- **View level:** Full view only
- **Only available when:** “Show Footnote Rule” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Distance (mm) to move the rule in from the side chosen in Horizontal Position.

**Explanation:**

Moves the rule in from the side chosen in **Horizontal Position**. The value is in mm (the on-screen label says **Indent (mm)**). Use 0 for no indent.

*(Internal ID: `s_fnIndent` · Config key: `notes/fnruleindent`)*

#### Rule Positioning and Parameters

- **Where:** Notes+Refs tab › Footnotes tab › Rule and Space Settings
- **Type:** Number box
- **Description:** Footnote rule: Length
- **View level:** Full view only
- **Values:** from 20 to 100, default 100
- **Only available when:** “Show Footnote Rule” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> The length of the rule as a percentage of the column/page width.

**Explanation:**

The length of the rule, as a percentage of the width of the column or page. 100 is a full-width line. Short rules of 20 to 40 are common in books.

*(Internal ID: `s_fnLength` · Config key: `notes/fnrulelength`)*

#### Rule Positioning and Parameters

- **Where:** Notes+Refs tab › Footnotes tab › Rule and Space Settings
- **Type:** Number box
- **Description:** Footnote rule: Line Thickness
- **View level:** Full view only
- **Values:** from 0.1 to 2, default 0.5
- **Only available when:** “Show Footnote Rule” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> The thickness of the rule.

**Explanation:**

The thickness of the rule in pt. The default is 0.5. Use a smaller value, like 0.3, for a lighter line.

*(Internal ID: `s_fnThick` · Config key: `notes/fnrulethick`)*

#### Rule Positioning and Parameters

- **Where:** Notes+Refs tab › Footnotes tab › Rule and Space Settings
- **Type:** Drop-down list
- **Description:** Footnote rule: Horizontal position
- **View level:** Full view only
- **Choices:** Left; Right; Inner; Outer; Center
- **Only available when:** “Show Footnote Rule” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Which side of the column the rule is aligned to:  
> Left, Right, Center, Inner (spine side) or Outer. Inner and Outer swap sides on odd and even pages. This only matters when the Length is less than 100%.
>
> These settings control the rule (horizontal line) above the notes: its indent (mm), its length (% of the column width), its thickness (pt) and which side of the column it is aligned to.

**Explanation:**

Where a shorter rule sits: **Left**, **Right**, **Center**, **Inner** (the side near the spine) or **Outer** (the side away from the spine). **Inner** and **Outer** change sides on odd and even pages. This only matters when **Length** is less than 100.

*(Internal ID: `fcb_fnHorizPosn` · Config key: `notes/fnruleposn`)*

### Notes+Refs tab › Footnotes tab › Miscellaneous Footnote Settings

#### Add a Colon ':' After \fq and \xq

- **Where:** Notes+Refs tab › Footnotes tab › Miscellaneous Footnote Settings
- **Type:** Checkbox (not ticked by default)
- **Description:** Add colon after quoted text in notes
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Some projects prefer to separate the Quoted text from the footnote text with a colon ':' which helps keep the elements visually distinct.

**Explanation:**

Adds a colon and a space after the quoted words (`\fq` or `\xq`) and before the note text. For example "*light*: Or *brightness*". Use it if your team does not type the colon in the notes.

*(Internal ID: `c_addColon` · Config key: `notes/addcolon`)*

#### Keep Book Names and Refs Together

- **Where:** Notes+Refs tab › Footnotes tab › Miscellaneous Footnote Settings
- **Type:** Checkbox (ticked by default)
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> This option inserts a No-Break Space (\u00A0) between the book name and the Ch:Vs refs so that they don't get split across lines.
>
> It also prevents single letters being left at the end of a line in note text.
>
> Note:  This setting currently has no effect on cross-references imported from external lists.

**Explanation:**

Stops a line break between a book name and its chapter and verse (for example "John 3:16") inside notes. It also stops a single letter from being left alone at the end of a line in notes. This setting does not affect cross-references from external lists.

*(Internal ID: `c_keepBookWithRefs` · Config key: `notes/keepbookwithrefs`)*

#### Show All Glossary Entries as Footnotes

- **Where:** Notes+Refs tab › Footnotes tab › Miscellaneous Footnote Settings
- **Type:** Checkbox (not ticked by default)
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Glossary entries for ALL marked-up Biblical Terms on each page can be made to appear as footnotes.
>
> Glossary words are marked like \w word\w* in the USFM text file. Only the first paragraph of each glossary entry is used.
>
> This feature is extremely useful when producing printouts for comprehension testing (where  Key Biblical Terms in the passage which have Glossary Entries also need to be checked for understanding).

**Explanation:**

For every glossary word marked with `\w ... \w*` in the text, PTXprint adds a footnote with the glossary entry from the GLO book. This is useful for comprehension testing printouts, but it adds many footnotes. Only the first paragraph of each glossary entry is used.

*(Internal ID: `c_glossaryFootnotes` · Config key: `notes/glossaryfootnotes`)*

#### Horizontal Space Separating Notes

- **Where:** Notes+Refs tab › Footnotes tab › Miscellaneous Footnote Settings
- **Type:** Number box
- **Description:** Minimum Horizontal Space Separating Notes
- **View level:** Full view only
- **Values:** from 2 to 20, default 5

**Tooltip (the text shown when you hover the mouse over it):**

> This spacing is set in points (pts). Changing this will increase or decrease the MINIMUM horizontal space between notes that have been run together.
>
> The horizontal space between notes that are being run together as a single paragraph can be set here. The default space is calculated as 33% between min & max values.
>
> For example if min=6pt and max=15pt then the default horizontal space between notes would be 9pt.
>
> If this control is disabled, it is because both the Footnotes and Cross-References have been set to start on a new line. (see \f and \x settings above).

**Explanation:**

The smallest space (in pt) between two notes that run on in the same paragraph. The maximum must be larger, so PTXprint adjusts **Maximum Space** when you change this. Greyed out when both footnotes and cross-references start on a new line.

*(Internal ID: `s_notespacingmin` · Config key: `notes/horiznotespacemin`)*

#### Horizontal Space Separating Notes

- **Where:** Notes+Refs tab › Footnotes tab › Miscellaneous Footnote Settings
- **Type:** Number box
- **Description:** Maximum Horizontal Space Separating Notes
- **View level:** Full view only
- **Values:** from 5 to 40, default 25

**Tooltip (the text shown when you hover the mouse over it):**

> This spacing is set in points (pts). Changing this will increase or decrease the MAXIMUM horizontal space between notes that have been run together.

**Explanation:**

The largest space (in pt) between two run-on notes. PTXprint aims for a space about one third of the way from the minimum to the maximum, and stretches or shrinks it to fill lines. A larger range gives PTXprint more freedom.

*(Internal ID: `s_notespacingmax` · Config key: `notes/horiznotespacemax`)*

#### Vertical Space Between Footnotes and xRefs (pt)

- **Where:** Notes+Refs tab › Footnotes tab › Miscellaneous Footnote Settings
- **Type:** Number box
- **Description:** Vertical Space Between Footnotes and xRefs
- **View level:** Full view only
- **Values:** default 3.5
- **Only available when:** “Column Cross-References” is selected
- **Greyed out when:** “Blend with Footnotes” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> When Footnotes and Cross-references are not blended together in the same block then the Footnotes appear in one block and the Cross-references in another block just below them. This setting (pts) lets you adjust the vertical space between these two sections.

**Explanation:**

The vertical space (in pt) between the block of footnotes and the block of cross-references when they are not blended. The default is 3.5. In this version, the box is only available when **Column Cross-References** is chosen. It is greyed out with **Blend with Footnotes**.

*(Internal ID: `s_internote` · Config key: `notes/internotespace`)*

### Notes+Refs tab › Cross-References tab

#### End of Book

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Radio button
- **Description:** Placement of cross-references: As End Notes
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This option will prevent cross-references showing on each page, but will gather them together and place them all at the end of the book.

**Explanation:**

Cross-references are not printed on each page. PTXprint collects them and prints them at the end of each book.

*(Internal ID: `r_xrpos_endnote` · Config key: `notes/xrlocation=endnote`, `notes/xrpos=endnote`, `notes/xrmarginal_=endnote`)*

#### End of Column

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Radio button
- **Description:** Placement of cross-references: End of column
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Use this option (only available in 2-column layout) to show the cross-references at the end of the 2nd column of text.
>
> Footnotes and cross-references at the foot of the page are kept together, so changing this may also change where the footnotes are placed.

**Explanation:**

Puts the cross-references at the bottom of the second column. If footnotes are at **End of Page**, they also move to **End of Column**. This needs a two-column layout.

*(Internal ID: `r_xrpos_column` · Config key: `notes/xrlocation=column`, `notes/xrpos=column`, `notes/xrmarginal_=column`)*

#### End of Page

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Radio button
- **Description:** Placement of cross-references: End of page
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Cross-references are usually placed at the end of each page.

**Explanation:**

Cross-references are printed at the bottom of the page on which their caller appears. If footnotes are at **End of Column**, they move to **End of Page** too.

*(Internal ID: `r_xrpos_normal` · Config key: `notes/xrlocation=normal`, `notes/xrpos=normal`, `notes/xrmarginal_=normal`)*

#### Start Each Cross-Reference on a New Line

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Normally cross-references are arranged one after the other to form a block of text. But if you require each cross-reference to start on its own new line then set this option.

**Explanation:**

Each cross-reference starts on a new line. This uses more space than run-on notes. When both this and **Start Each Footnote on a New Line** are ticked, the horizontal spacing settings on the **Footnotes** sub-tab are greyed out.

*(Internal ID: `c_xreachnewline` · Config key: `notes/xreachnewline`)*

#### Override hidden/automatic Cross-reference caller settings

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Override Cross-Reference Settings in Text
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Cross-references specified in Paratext use  
> \x +(plus) to cycle through the callers, or \x - (minus) to omit the caller.
>
> If this option is enabled, the Show Callers settings below will override whatever has been specified within the text itself.

**Explanation:**

When ticked, PTXprint ignores the `\x +` / `\x -` / fixed-caller setting in each cross-reference. It uses `+` for all of them if **Show Callers** is ticked, and `-` (no caller) if it is not.

*(Internal ID: `c_xrOverride` · Config key: `notes/xroverride`)*

#### Show Callers in the Text

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Checkbox (ticked by default)
- **Description:** Show Cross-Reference Callers in the Text
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> A "Caller" is a symbol (in the text) which alerts the reader that there is further information (in this case a cross-reference at the bottom of the page). Some people prefer not to indicate cross-references in the text itself, but just to include them at the bottom of the page.
>
> Separate callers with a comma (no spaces). For example: a,b,c,d,e,f,g,h, etc. or:  †,‡,§,∥,#    or: ✶,☆,✦,✪
>
> If you do not see the callers you are expecting in the PDF, then try using the "Override..." setting above.

**Explanation:**

When ticked, PTXprint uses the marks in the box next to it as callers for cross-references. Some publications do not show cross-reference callers in the text at all. Untick this and tick **Override…** for that.

*(Internal ID: `c_xrautocallers` · Config key: `notes/ifxrautocallers`)*

#### Cross-Reference Caller Sequence Entry

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Text box
- **View level:** Default and Full views
- **Only available when:** “Show Callers in the Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> These callers should automatically be loaded from the settings in the Paratext project, but can be modified here if needed. (Use the button on the right to reload them if needed.)
>
> Separate callers with a comma (no spaces). For example: a,b,c,d,e,f,g,h, etc. or:  †,‡,§,∥,#    or: ✶,☆,✦,✪

**Explanation:**

Type the marks for cross-reference callers, separated by commas and no spaces, for example `†,‡,§`. Choose marks that are different from the footnote callers, so readers can tell the two kinds of notes apart.

*(Internal ID: `t_xrcallers` · Config key: `notes/xrcallers`)*

#### Reload cross-reference callers from Paratext

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Button
- **View level:** Default and Full views
- **Only available when:** “Show Callers in the Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Clicking this button will reload the cross-ref callers from the Paratext project settings.
>
> If the callers have not been defined in the Paratext project, or are already showing, then a default set will appear.

**Explanation:**

Loads the cross-reference callers from the Paratext project settings. If Paratext has none, or they are already in the box, PTXprint puts in its default sequence (`†,‡,§,∥,#`).

*(Internal ID: `btn_resetXRcallers`)*

#### Show Callers in Notes Area

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Checkbox (ticked by default)
- **Description:** Show cross-reference callers in notes area
- **View level:** Default and Full views
- **Only available when:** “Show Callers in the Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Usually the "Caller" symbol is also shown in the notes area which helps the reader quickly find the cross-reference from the text.

**Explanation:**

When ticked, the caller is also printed at the start of the cross-reference in the notes area. Untick it to save a little space.

*(Internal ID: `c_xromitcaller` · Config key: `notes/xromitcaller`)*

#### Reset Callers on Page

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Checkbox (ticked by default)
- **Description:** Reset cross-reference callers on each page
- **View level:** Default and Full views
- **Only available when:** “Show Callers in the Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If this is checked, then the sequence of callers starts again from the 1st item in the list of callers specified.
>
> Note that this feature doesn't always take effect straight away. You may need to hit Print a second time before it applies.

**Explanation:**

Starts the cross-reference caller sequence again on each page. You may need to click **Print** twice before it shows correctly.

*(Internal ID: `c_xrpageresetcallers` · Config key: `notes/xrresetcallers`)*

#### \x

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Link
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the Cross-Reference properties on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the `\x` (cross-reference) style, where you can change the font size and other properties. For column cross-references, a small size (about 6 pt) is often needed.

*(Internal ID: `lb_style_x`)*

#### Below Footnotes

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Radio button
- **Description:** Placement of cross-references: Below footnotes
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Cross-references will be listed in a separate block underneath the footnotes (rather than combined along with the footnotes as a single paragraph).

**Explanation:**

Cross-references are printed at the bottom of the page, in their own block under the footnotes. This keeps the two kinds of notes clearly apart. **Vertical Space Between Footnotes and xRefs** sets the gap between the two blocks.

*(Internal ID: `r_xrpos_below` · Config key: `notes/xrlocation=below`, `notes/xrpos=below`, `notes/xrmarginal_=below`)*

#### Blend with Footnotes

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Radio button
- **Description:** Placement of cross-references: Blend with footnotes
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> To save space in the footnote area, you can combine the  footnotes and cross-references as a single paragraph (rather than the cross- references appearing in a separate block underneath the footnotes). If this option is used, the Cross-References can only have one type of caller (rather than a sequence) which must be specified above.

**Explanation:**

Cross-references and footnotes are mixed together in one paragraph at the bottom of the page. This saves space. PTXprint sets the `\x` style on the **Styles** tab so that it joins the footnotes.

*(Internal ID: `r_xrpos_blend` · Config key: `notes/xrlocation=blend`, `notes/xrpos=blend`, `notes/xrmarginal_=blend`)*

#### Column Cross-References

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Radio button
- **Description:** Placement of cross-references: Vertical column
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> When there are numerous cross-references (usually when using an external list of references) then it may be useful to place them in their own column.
>
> The cross references will appear in a narrow vertical column similar to a study/reference Bible layout.

**Explanation:**

Cross-references go in a narrow column of their own, like in a reference Bible. With a two-column layout the column is between the text columns. With one column, choose the side in **Side of page**. Choosing this also sets footnotes to **End of Column**, and opens the **Source for References** area. Set the width and other settings in the **Column Cross-References** area.

*(Internal ID: `r_xrpos_centre` · Config key: `notes/xrlocation=centre`, `notes/xrpos=centre`, `notes/xrmarginal_=centre`)*

#### Use External List of Cross-References

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Instead of using a handful of cross-references as specified within the project's USFM text, you can select an external list containing many 1000's of cross-references. These will automatically be localized into the project's language using the  
> \toc3 values specified in the Paratext project settings (See: Scripture reference settings...)
>
> This feature is usually used for Study or Reference Bibles in conjunction with the 'Column Cross-References' placement option.

**Explanation:**

Adds cross-references from a ready-made list (or your own file) for every verse that has them in the list. Choose the list in **Source for References**. The book names are changed to your project's short book names. The added references have no caller in the text. When ticked, the **Cross-References** sub-tab name is highlighted. (Only in the **Full** view.)

*(Internal ID: `c_useXrefList` · Config key: `notes/ifxrexternalist`)*

#### Show Extended Cross-References

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Study Bibles can (optionally) use extended cross-references (\ex) which can be displayed along with other kinds of cross-references.

**Explanation:**

Some study Bibles have extended cross-references marked `\ex ... \ex*`. Tick this to print them like ordinary cross-references. When it is not ticked, PTXprint removes all `\ex` notes.

*(Internal ID: `c_extendedXrefs` · Config key: `notes/showextxrefs`)*

#### Include Cross-References (From Project Text)

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Checkbox (ticked by default)
- **Description:** Include cross-references (from project)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Select whether cross-references from the project's text should be included.
>
> The specific settings for these are located on the Cross-References tab.

**Explanation:**

Prints the cross-references that the team typed in the project text (`\x ... \x*`). Untick it to leave them out. This does not affect cross-references from an external list.

*(Internal ID: `c_includeXrefs` · Config key: `notes/includexrefs`)*

#### Only show verse numbers from \xo

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The cross-reference origin \xo usually includes the chapter & verse number like this 3:16. If you prefer to hide the chapter, so that only 16 is shown, then enable this option.

**Explanation:**

At the start of a cross-reference, the origin reference (`\xo`) usually shows chapter and verse, for example `3:16`. Tick this to show only `16`. This also applies to cross-references from external lists.

*(Internal ID: `c_xoVerseOnly` · Config key: `notes/xrverseonly`)*

#### Side Margin

- **Where:** Notes+Refs tab › Cross-References tab
- **Type:** Radio button
- **Description:** Placement of cross-references: Side Margin
- **View level:** Default and Full views
- **Only available when:** “Margin Notes Col Width (mm)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This option will place references (and optionally also the Footnotes and Section Headings) in a column next to the text and align them as closely as possible vertically to their caller.

**Explanation:**

Puts cross-references in the margin-notes column next to the text, close to the line they belong to. Greyed out until **Margin Notes Col Width (mm)** is ticked on the **Layout** tab. If you turn margin notes off, the cross-references go back to **End of Page**.

*(Internal ID: `r_xrpos_margin` · Config key: `notes/xrlocation=margin`, `notes/xrpos=margin`, `notes/xrmarginal_=margin`)*

### Notes+Refs tab › Cross-References tab › Source for References

#### Include Refs for Books in

- **Where:** Notes+Refs tab › Cross-References tab › Source for References
- **Type:** Drop-down list
- **Description:** Include references for which category of books
- **View level:** Full view only
- **Choices:** Whole Bible; Paratext Project; This Publication; New Testament; Old Testament
- **Only available when:** “Use External List of Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> The various cross-reference lists often contain hundreds of 1000s of references. You may want to only include target references that are currently available to your readers by selecting a subset of Biblical books.
>
> So for example, if there is no Old Testament yet, you may want to only include target cross-references to NT Books.
>
> If you select Books in "This Publication", then only cross-references targeting books in the "Portions or Multiple Books" list on the Basic tab will be included.

**Explanation:**

Removes references that point to books your readers do not have:
* **Whole Bible** – keep all references.
* **Paratext Project** – only books that exist in the project.
* **This Publication** – only the books in the list of books to print (**Basic** tab, **What to Print** area).
* **New Testament** or **Old Testament** – only that part of the Bible.

*(Internal ID: `fcb_filterXrefs` · Config key: `notes/xrfilterbooks`)*

#### External Refs

- **Where:** Notes+Refs tab › Cross-References tab › Source for References
- **Type:** Drop-down list
- **Description:** Select external list of cross-references
- **View level:** Full view only
- **Choices:** Standard list (fewest); Standard list (fewer); Standard list; Standard list (more); Standard list (most); Strong's list (all); Strong's list (project); TSK list; BibleWorks™ list; UBS GNT92 list; UBS GNT92 list (DC); Select a Custom list...
- **Only available when:** “Use External List of Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> There are multiple options to choose from if you wish to use an external list of cross-references. Select whichever is most appropriate and the list will automatically be localized to use the abbreviated book names as defined in Paratext's Scripture Reference Settings which should match the \toc3 markers.
>
> The five Standard list sizes take fewer or more references from the same prioritized list (fewest = only the most important ones).

**Explanation:**

Chooses the external list. The five **Standard list** sizes take more or fewer references from the same list, from **(fewest)** to **(most)**. The **Strong's** lists group references by Hebrew and Greek word, and make the **Strong's References** settings available. **Select a Custom list...** makes the **Select...** button available. Larger lists need more space on the page and take longer to process.

*(Internal ID: `fcb_xRefExtListSource` · Config key: `notes/xrlistsource`, `notes/xrextlistsource`)*

#### Select...

- **Where:** Notes+Refs tab › Cross-References tab › Source for References
- **Type:** Button
- **Description:** Select a custom cross-reference list
- **View level:** Full view only
- **Only available when:** “Use External List of Cross-References” is selected

**Explanation:**

Opens a file chooser to select your own cross-reference file. It starts in the `_Cross References` folder of Paratext. PTXprint can read `.xrf` files (the Paratext cross-reference format), `.xre` files and `.xml` files. Only available when **External Refs** is set to **Select a Custom list...**. After you choose a file, hover over the button to see the file name.

*(Internal ID: `btn_selectXrFile` · Config key: `project/selectxrfile`)*

#### Standard

- **Where:** Notes+Refs tab › Cross-References tab › Source for References
- **Type:** Radio button
- **Description:** Source of cross-references: Standard list
- **View level:** Full view only
- **Only available when:** “Use External List of Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> The Standard List contains more than 340,000 cross-references which have been prioritized by crowd-sourcing.

**Explanation:**

This option is not shown on screen. Its text is used for the description of the **Standard list** when you hover over the information button. Choose the list in **External Refs**.

*(Internal ID: `r_xrSource_standard`)*

#### Strongs

- **Where:** Notes+Refs tab › Cross-References tab › Source for References
- **Type:** Radio button
- **Description:** Source of cross-references: Strong's list
- **View level:** Full view only
- **Only available when:** “Use External List of Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> The Strong's List contains a curated subset of cross-references generated from the Strong's Numbers. Optionally an index for these numbers can also be created as an additional book that can be appended to the publication.
>
> Each set of cross-references is indexed by a Hebrew or Greek Strong's number which can be looked up in the (optional) Index which can be generated using the "Generate Index..." button.

**Explanation:**

This option is not shown on screen. Its text is used for the description of the **Strong's** lists when you hover over the information button. Choose the list in **External Refs**.

*(Internal ID: `r_xrSource_strongs`)*

#### TSK

- **Where:** Notes+Refs tab › Cross-References tab › Source for References
- **Type:** Radio button
- **Description:** Source of cross-references: Treasury of Scripture Knowledge
- **View level:** Full view only
- **Only available when:** “Use External List of Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> For generations, the Treasury of Scripture Knowledge has been an enduring cross-reference resource for Bible students worldwide. This highly respected and nearly exhaustive compilation of cross-references was developed by R.A. Torrey from references in the Rev. Thomas Scott's Commentary and the Comprehensive Bible. With nearly 500,000 cross-references it is the most thorough source available.

**Explanation:**

This option is not shown on screen. Its text is used for the description of the **TSK list** when you hover over the information button. Choose the list in **External Refs**.

*(Internal ID: `r_xrSource_tsk`)*

#### BibWrx

- **Where:** Notes+Refs tab › Cross-References tab › Source for References
- **Type:** Radio button
- **Description:** Source of cross-references: The Works
- **View level:** Full view only
- **Only available when:** “Use External List of Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> The BibleWorks list contains 112,000 cross-references which were formerly part of the BibleWorks software which has been discontinued.

**Explanation:**

This option is not shown on screen. Its text is used for the description of the **BibleWorks™ list** when you hover over the information button. Choose the list in **External Refs**.

*(Internal ID: `r_xrSource_works`)*

#### UBS

- **Where:** Notes+Refs tab › Cross-References tab › Source for References
- **Type:** Radio button
- **Description:** Source of cross-references: UBS GNT92 list
- **View level:** Full view only
- **Only available when:** “Use External List of Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This list contains New Testament and Old Testament references (NO Deuterocanonical  references). Short Bible Reference System, edited by Robert G. Bratcher, (c) 1961 United Bible Societies. This list was used in GNT92. Organizations that have a Paratext license may use this list in their publication without attribution or notifying UBS. All other rights to use this list are reserved.
>
> Use the (DC) list if Deutero Canonical references are needed.

**Explanation:**

This option is not shown on screen. Its text is used for the description of the **UBS GNT92** lists when you hover over the information button. Choose the list in **External Refs**.

*(Internal ID: `r_xrSource_ubs`)*

#### Custom

- **Where:** Notes+Refs tab › Cross-References tab › Source for References
- **Type:** Radio button
- **Description:** Source of cross-references: Custom .xrf list
- **View level:** Full view only
- **Only available when:** “Use External List of Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> You can select a specially-curated list of cross-references. For example, it is possible to extract cross-references from another project (in the .xrf file format) to be included here. There is also an .xre format (extended .xrf) and an .xml format which can be used as external cross-references. These formats are explained in the documentation. Search Google for "ptx2pdf/xrefs.md"

**Explanation:**

This option is not shown on screen. Its text is used for the description of a custom list when you hover over the information button. To use your own list, choose **Select a Custom list...** in **External Refs** and click **Select...**.

*(Internal ID: `r_xrSource_custom`)*

#### Hover here to read about the selected cross-reference list.

- **Where:** Notes+Refs tab › Cross-References tab › Source for References
- **Type:** Button
- **View level:** Full view only
- **Only available when:** “Use External List of Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Hover here to read about the selected cross-reference list.

**Explanation:**

Hover the mouse over this button to read a description of the list chosen in **External Refs**: how many references it has, where it comes from and any copyright notes.

*(Internal ID: `btn_infoXrefSource`)*

### Notes+Refs tab › Cross-References tab › Source for References › Strong's References

#### Show Numbers in the Text

- **Where:** Notes+Refs tab › Cross-References tab › Source for References › Strong's References
- **Type:** Checkbox (not ticked by default)
- **Description:** Show Strong's numbers in the text
- **View level:** Full view only
- **Only available when:** “Use External List of Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If the project's Biblical Terms list includes renderings, then it is possible to show Strong's numbers in the text itself, which should make it easier to look up the appropriate cross-references for a word in a Study Bible.
>
> Note that this option is disabled by default as it can clutter the scripture text and will also slow down the production of the PDF.

**Explanation:**

Adds the Strong's number next to the words in the Bible text, using your project's Biblical Terms renderings. This helps readers of a study Bible find the right cross-references, but it fills the text with numbers and makes the PDF much slower to produce. Only available for the Strong's lists.

*(Internal ID: `c_strongsShowInText` · Config key: `strongsndx/showintext`)*

#### Show Numbers in Cross-References

- **Where:** Notes+Refs tab › Cross-References tab › Source for References › Strong's References
- **Type:** Checkbox (ticked by default)
- **Description:** Show Strong's numbers in cross-references
- **View level:** Full view only
- **Only available when:** “Use External List of Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If you are generating a localized Strong's index, then it is highly recommended to include the Strong's numbers in the list of cross-references in the text.
>
> But if you only want to show the references without any Strong's numbers, then uncheck this option for a more compact list.

**Explanation:**

Shows the Strong's number in front of each group of references in the cross-reference list. Keep it ticked if you make a Strong's index, so readers can look the numbers up. Untick it for a shorter list.

*(Internal ID: `c_strongsShowNums` · Config key: `strongsndx/shownums`)*

#### Generate Index...

- **Where:** Notes+Refs tab › Cross-References tab › Source for References › Strong's References
- **Type:** Button
- **Description:** Generate Index (based on Strong's numbers)
- **View level:** Full view only
- **Only available when:** “Use External List of Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> For Strong's Cross References to be most useful, it is recommended to include an Index at the end of the publication. Click this button to set various options to be used to generate the index.

**Explanation:**

Opens the **Generate Strong's Index** dialog, where you can make an index book of Strong's numbers to print at the end of the publication. Only available for the Strong's lists.

*(Internal ID: `btn_strongsGenerate`)*

#### Show All Occurrences

- **Where:** Notes+Refs tab › Cross-References tab › Source for References › Strong's References
- **Type:** Checkbox (not ticked by default)
- **Description:** Show Strong's numbers on every occurrence of a word
- **View level:** Full view only
- **Only available when:** “Show Numbers in the Text”, “Use External List of Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If a particular word occurs more than once in the given verse, each occurrence will be tagged with the Strong's number. If a word matches more than one Strong's number then both will be displayed.
>
> This may be rather confusing for the reader, but could be helpful for a consultant to easily identify overlap issues with the project's Biblical terms renderings.

**Explanation:**

Only available when **Show Numbers in the Text** is ticked. Tags every place where a word appears in the verse, and shows all numbers if a word matches more than one. This can confuse readers, but it helps a consultant find overlaps in the Biblical Terms renderings.

*(Internal ID: `c_strongsShowAll` · Config key: `strongsndx/showall`)*

#### \xts

- **Where:** Notes+Refs tab › Cross-References tab › Source for References › Strong's References
- **Type:** Link
- **View level:** Full view only
- **Only available when:** “Use External List of Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the Strong's 4 digit cell number properties on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the `\xts` style, which controls how the Strong's numbers look in the cross-references.

*(Internal ID: `lb_style_xts`)*

### Notes+Refs tab › Cross-References tab › Source for References › Column Cross-References

#### Column Width (pts)

- **Where:** Notes+Refs tab › Cross-References tab › Source for References › Column Cross-References
- **Type:** Number box
- **Description:** Column width of column-based cross-references
- **View level:** Full view only
- **Values:** from 30 to 150, default 60
- **Only available when:** “Column Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This sets the width of the centre column in points. Note that 72pts is 1 inch, and increasing the size here will decrease the amount of space available for the 2 columns of scripture text.
>
> Consider using a larger page size if you want to use Centre Column xRefs.
>
> If this centre column isn't wide enough to fit the references, then you should also consider reducing the size of the \x font (to approx 6pt).

**Explanation:**

The width of the cross-reference column, in pt (72 pt is about 25 mm). The default is 60. A wider column leaves less space for the Bible text. If the references do not fit, make the `\x` font smaller rather than the column much wider.

*(Internal ID: `s_centreColWidth` · Config key: `notes/xrcentrecolwidth`)*

#### Gutter Width (pts)

- **Where:** Notes+Refs tab › Cross-References tab › Source for References › Column Cross-References
- **Type:** Number box
- **Description:** Gutter width of column-based cross-references
- **View level:** Full view only
- **Values:** from 0.1 to 20, default 2
- **Only available when:** “Column Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This sets the space between the main body text and the column of cross-references.

**Explanation:**

The empty space (in pt) between the Bible text and the cross-reference column. The default is 2.

*(Internal ID: `s_xrGutterWidth` · Config key: `notes/xrguttermargin`)*

#### Side of page

- **Where:** Notes+Refs tab › Cross-References tab › Source for References › Column Cross-References
- **Type:** Drop-down list
- **Description:** Position of column-based cross-references
- **View level:** Full view only
- **Choices:** Left; Right; Inner; Outer
- **Only available when:** “Column Cross-References” is selected
- **Greyed out when:** “Two Column Layout” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Select where the column of cross-references should be located on the page. Note that the 2-column layout insists on the cross-references being positioned between the columns of text.

**Explanation:**

For a one-column layout, the side of the page for the cross-reference column: **Left**, **Right**, **Inner** (near the spine) or **Outer** (away from the spine). Greyed out with **Two Column Layout**, because then the column is always between the text columns.

*(Internal ID: `fcb_colXRside` · Config key: `notes/xrcolside`)*

#### Vertical Rule(s) Between Columns

- **Where:** Notes+Refs tab › Cross-References tab › Source for References › Column Cross-References
- **Type:** Checkbox (ticked by default)
- **Description:** Include a vertical rule between columns
- **View level:** Full view only
- **Only available when:** “Column Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Check this option to include a vertical line separating the text and cross-references.

**Explanation:**

Draws a thin vertical line between the Bible text and the cross-reference column.

*(Internal ID: `c_xrColumnRule` · Config key: `notes/xrcolrule`)*

#### Fill Upward From Bottom of Column

- **Where:** Notes+Refs tab › Cross-References tab › Source for References › Column Cross-References
- **Type:** Checkbox (not ticked by default)
- **Description:** Fill cross-references upward from bottom of column
- **View level:** Full view only
- **Only available when:** “Column Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If there are only a small number of cross-references, it may appear better for them to be placed nearer the end (or bottom) of the page. Check this option if you prefer the references to fill the column upward from the end of the page.

**Explanation:**

Places the references at the bottom of the column instead of the top. This can look better when there are only a few references on a page.

*(Internal ID: `c_xrColumnBottom` · Config key: `notes/xrcolbottom`)*

#### Side Align Notes

- **Where:** Notes+Refs tab › Cross-References tab › Source for References › Column Cross-References
- **Type:** Checkbox (not ticked by default)
- **Description:** Align notes to the edge of the main text
- **View level:** Full view only
- **Only available when:** “Column Cross-References” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> For side column notes, should the text of the notes align to the edge of the main text?

**Explanation:**

Aligns the text of the references to the edge of the main text, instead of to the edge of the column.

*(Internal ID: `c_xrSideAlign` · Config key: `notes/xrcolalign`)*

### Notes+Refs tab › Cross-References tab › Rule and Space Settings

#### Show Cross-Reference Rule

- **Where:** Notes+Refs tab › Cross-References tab › Rule and Space Settings
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This is the horizontal rule separating the body text from the cross-reference area.

**Explanation:**

Shows the settings for the rule above cross-references. PTXprint uses these settings only when footnotes are at **End of Book**, or for cross-references printed at the end of the book. To hide the rule above the bottom-of-page notes, untick **Show Footnote Rule** on the **Footnotes** sub-tab.

*(Internal ID: `c_xrefrule` · Config key: `notes/ifxrefrule`)*

#### Space Above Rule (pt)

- **Where:** Notes+Refs tab › Cross-References tab › Rule and Space Settings
- **Type:** Number box
- **Description:** Space above cross-reference rule
- **View level:** Default and Full views
- **Values:** from -50 to 50

**Tooltip (the text shown when you hover the mouse over it):**

> The vertical space between the main text body and the cross-reference rule.
>
> The vertical space between the body text and the area containing cross-references.
>
> If the Cross-Reference Rule is not shown, the vertical space will still be calculated as the Space Above plus the Space Below (the imaginary) Rule.

**Explanation:**

The space (in pt) between the text and the cross-reference rule. PTXprint uses it only when the cross-reference rule settings are used (see **Show Cross-Reference Rule**).

*(Internal ID: `s_xrAboveSpace` · Config key: `notes/abovexrefspace`)*

#### Space Below Rule (pt)

- **Where:** Notes+Refs tab › Cross-References tab › Rule and Space Settings
- **Type:** Number box
- **Description:** Space below cross-reference rule
- **View level:** Default and Full views
- **Values:** from -50 to 50
- **Only available when:** “Show Cross-Reference Rule” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This is the vertical space/gap (pts) between the rule and the cross-references.

**Explanation:**

The space (in pt) between the cross-reference rule and the first cross-reference. Greyed out when **Show Cross-Reference Rule** is not ticked.

*(Internal ID: `s_xrBelowSpace` · Config key: `notes/belowxrefrulespace`)*

#### Rule Positioning and Parameters

- **Where:** Notes+Refs tab › Cross-References tab › Rule and Space Settings
- **Type:** Number box
- **Description:** Cross-reference rule: Indent
- **View level:** Full view only
- **Only available when:** “Show Cross-Reference Rule” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Distance (mm) to move the rule in from the side chosen in Horizontal Position.

**Explanation:**

Moves the cross-reference rule in from the side chosen in **Horizontal Position**. The value is in mm.

*(Internal ID: `s_xrIndent` · Config key: `notes/xrruleindent`)*

#### Rule Positioning and Parameters

- **Where:** Notes+Refs tab › Cross-References tab › Rule and Space Settings
- **Type:** Number box
- **Description:** Cross-reference rule: Length
- **View level:** Full view only
- **Values:** from 20 to 100
- **Only available when:** “Show Cross-Reference Rule” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> The length of the rule as a percentage of the column/page width.

**Explanation:**

The length of the cross-reference rule, as a percentage of the column or page width.

*(Internal ID: `s_xrLength` · Config key: `notes/xrrulelength`)*

#### Rule Positioning and Parameters

- **Where:** Notes+Refs tab › Cross-References tab › Rule and Space Settings
- **Type:** Number box
- **Description:** Cross-reference rule: Thickness
- **View level:** Full view only
- **Values:** from 0.1 to 2
- **Only available when:** “Show Cross-Reference Rule” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> The thickness of the rule.

**Explanation:**

The thickness of the cross-reference rule in pt.

*(Internal ID: `s_xrThick` · Config key: `notes/xrrulethick`)*

#### Rule Positioning and Parameters

- **Where:** Notes+Refs tab › Cross-References tab › Rule and Space Settings
- **Type:** Drop-down list
- **Description:** Cross-reference rule: Horizontal position
- **View level:** Full view only
- **Choices:** Left; Right; Inner; Outer; Center
- **Only available when:** “Show Cross-Reference Rule” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Which side of the column the rule is aligned to:  
> Left, Right, Center, Inner (spine side) or Outer. Inner and Outer swap sides on odd and even pages. This only matters when the Length is less than 100%.
>
> These settings control the rule (horizontal line) above the notes: its indent (mm), its length (% of the column width), its thickness (pt) and which side of the column it is aligned to.

**Explanation:**

Where a shorter cross-reference rule sits: **Left**, **Right**, **Center**, **Inner** or **Outer**. **Inner** and **Outer** change sides on odd and even pages.

*(Internal ID: `fcb_xrHorizPosn` · Config key: `notes/xrruleposn`)*

### Notes+Refs tab › Study Notes + Questions tab › Extended Footnotes (\ef)

#### Gutter Width (mm)

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Extended Footnotes (\ef)
- **Type:** Number box
- **Description:** Gutter width between columns of extended notes
- **View level:** Full view only
- **Values:** from 1 to 40
- **Only available when:** “Extended Footnotes (\ef)” is selected
- **Hidden until:** “Extended Footnotes (\ef)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This is the space between the text of the two columns (measured in millimeters).
>
> This is the space (mm) between the text of the two columns.

**Explanation:**

The space (in mm) between the two columns of study notes. A larger value makes the notes easier to read but uses more space.

*(Internal ID: `s_ef_colgutterfactor` · Config key: `studynotes/colgutterfactor`)*

#### Unbalanced Lines (max)

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Extended Footnotes (\ef)
- **Type:** Number box
- **Description:** Allow N unbalanced lines in extended notes
- **View level:** Full view only
- **Only available when:** “Extended Footnotes (\ef)” is selected
- **Hidden until:** “Extended Footnotes (\ef)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> PTXprint will attempt to balance the number of lines in each column of the extended notes. Sometimes this results in wasted empty space. Increasing this number (recommended range 1-4) will allow up to that many unbalanced lines in the extended notes area.
>
> By default (when this is set to 0) PTXprint will balance the number of lines used in each column. Sometimes this results in large empty spaces at the end of a page.
>
> Increasing this number (recommended range 1-4) will allow up to that many unbalanced lines on the page. Note that you can still stretch/shrink paragraphs using AdjLists to refine the output by manually balancing pages.

**Explanation:**

This setting is always greyed out in this version, so you cannot change it.

*(Internal ID: `s_ef_bottomRag`)*

#### Vertical Space Between Notes

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Extended Footnotes (\ef)
- **Type:** Number box
- **Description:** Vertical space between extended/study notes
- **View level:** Full view only
- **Values:** from -20 to 20
- **Only available when:** “Extended Footnotes (\ef)” is selected
- **Hidden until:** “Extended Footnotes (\ef)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This setting (pts) lets you adjust the vertical space between extended footnotes. Usually there is no space between them.

**Explanation:**

The extra vertical space (in pt) between one study note and the next. The default is no extra space. A small value such as 1 or 2 can make separate notes easier to see.

*(Internal ID: `s_ef_internote` · Config key: `studynotes/internote`)*

#### Vertical Rule in Gutter

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Extended Footnotes (\ef)
- **Type:** Checkbox (not ticked by default)
- **Description:** Vertical rule in study notes area gutter
- **View level:** Full view only
- **Only available when:** “Extended Footnotes (\ef)” is selected
- **Hidden until:** “Extended Footnotes (\ef)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Check this option to include a center line between the two columns.

**Explanation:**

Draws a thin vertical line in the gutter between the two columns of study notes. When ticked, **Adjust Top (pt)** becomes available.

*(Internal ID: `c_ef_verticalrule` · Config key: `studynotes/ifverticalrule`)*

#### Adjust Top (pt)

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Extended Footnotes (\ef)
- **Type:** Number box
- **View level:** Full view only
- **Values:** from -50 to 50
- **Only available when:** “Vertical Rule in Gutter”, “Extended Footnotes (\ef)” is selected
- **Hidden until:** “Extended Footnotes (\ef)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This setting raises (using a negative value) or lowers (using a positive value) the starting point of the vertical rule between columns (pt).
>
> This setting raises (using a negative value) or lowers (using a positive value) the starting point of the vertical rule between columns.

**Explanation:**

Moves the top of the vertical line between the study-note columns. A negative value raises it, a positive value lowers it. Only available when **Vertical Rule in Gutter** is ticked.

*(Internal ID: `s_ef_colgutteroffset` · Config key: `studynotes/colgutteroffset`)*

#### Show Note Callers

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Extended Footnotes (\ef)
- **Type:** Checkbox (not ticked by default)
- **Description:** Show study note callers in notes area
- **View level:** Full view only
- **Only available when:** “Extended Footnotes (\ef)” is selected
- **Hidden until:** “Extended Footnotes (\ef)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Show callers for extended (study) notes, both in the text and in the notes area. A caller alerts the reader that there is further information (in this case an extended footnote) at the end of the page. As a Study Bible has many such notes, this option is normally turned off for extended footnotes. Note that currently only a,b,c...x,y,z callers are possible for this option.

**Explanation:**

When ticked, study notes get a caller in the text and in the notes area. When it is not ticked, PTXprint removes the callers of all study notes, even if the text asks for them. Study Bibles have very many notes, so callers are normally off. Only the letters a to z can be used as callers here.

*(Internal ID: `c_ef_showCallers` · Config key: `studynotes/showcallers`)*

### Notes+Refs tab › Study Notes + Questions tab › Extended Footnotes (\ef) › Rule and Space Settings

#### Rule Positioning and Parameters

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Extended Footnotes (\ef) › Rule and Space Settings
- **Type:** Number box
- **Description:** Study note rule: Indent
- **View level:** Full view only
- **Hidden until:** “Extended Footnotes (\ef)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Distance (mm) to move the rule in from the side chosen in Horizontal Position.

**Explanation:**

Moves the rule above the study notes in from the side chosen in **Horizontal Position**. The value is in mm.

*(Internal ID: `s_snIndent` · Config key: `notes/snruleindent`)*

#### Rule Positioning and Parameters

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Extended Footnotes (\ef) › Rule and Space Settings
- **Type:** Number box
- **Description:** Study note rule: Length
- **View level:** Full view only
- **Values:** from 20 to 100, default 100
- **Hidden until:** “Extended Footnotes (\ef)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The length of the rule as a percentage of the column/page width.

**Explanation:**

The length of the study-note rule, as a percentage of the page width. The default is 100 (full width).

*(Internal ID: `s_snLength` · Config key: `notes/snrulelength`)*

#### Rule Positioning and Parameters

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Extended Footnotes (\ef) › Rule and Space Settings
- **Type:** Number box
- **Description:** Study note rule: Thickness
- **View level:** Full view only
- **Values:** from 0.1 to 2, default 0.5
- **Hidden until:** “Extended Footnotes (\ef)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The thickness of the rule.

**Explanation:**

The thickness of the study-note rule in pt. The default is 0.5.

*(Internal ID: `s_snThick` · Config key: `notes/snrulethick`)*

#### Rule Positioning and Parameters

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Extended Footnotes (\ef) › Rule and Space Settings
- **Type:** Drop-down list
- **Description:** Study note rule: Horizontal position
- **View level:** Full view only
- **Choices:** Left; Right; Inner; Outer; Center
- **Hidden until:** “Extended Footnotes (\ef)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Which side of the column the rule is aligned to:  
> Left, Right, Center, Inner (spine side) or Outer. Inner and Outer swap sides on odd and even pages. This only matters when the Length is less than 100%.
>
> These settings control the rule (horizontal line) above the notes: its indent (mm), its length (% of the column width), its thickness (pt) and which side of the column it is aligned to.

**Explanation:**

Where a shorter study-note rule sits: **Left**, **Right**, **Center**, **Inner** or **Outer**. **Inner** and **Outer** change sides on odd and even pages.

*(Internal ID: `fcb_snHorizPosn` · Config key: `notes/snruleposn`)*

#### Show Study Note Rule

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Extended Footnotes (\ef) › Rule and Space Settings
- **Type:** Checkbox (ticked by default)
- **View level:** Full view only
- **Hidden until:** “Extended Footnotes (\ef)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This is the horizontal rule separating the body text from the study notes area.

**Explanation:**

Shows or hides the line between the ordinary notes (or the text) and the study notes area.

*(Internal ID: `c_studynoterule` · Config key: `notes/ifstudynoterule`)*

#### Space Above Rule (pt)

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Extended Footnotes (\ef) › Rule and Space Settings
- **Type:** Number box
- **Description:** Space above study note rule
- **View level:** Full view only
- **Values:** from -50 to 50, default 6
- **Hidden until:** “Extended Footnotes (\ef)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The vertical space between the main text body and the study note rule.
>
> Note: if you make this value less than the descenders of the last lines of text, then the study notes will push down into the footer area. If you see this happening, increase this value to trigger an earlier page break to solve the problem.
>
> The vertical space between the body text and the area containing study notes.
>
> If the Study Note Rule is not shown, the vertical space will still be calculated as the Space Above plus the Space Below (the imaginary) Rule.

**Explanation:**

The space (in pt) above the study-note rule. The default is 6.

*(Internal ID: `s_snAboveSpace` · Config key: `notes/abovestudyspace`)*

#### Space Below Rule (pt)

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Extended Footnotes (\ef) › Rule and Space Settings
- **Type:** Number box
- **Description:** Space below study note rule
- **View level:** Full view only
- **Values:** from -50 to 50, default 2
- **Hidden until:** “Extended Footnotes (\ef)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This is the vertical space/gap (pts) between the rule and the study notes.

**Explanation:**

The space (in pt) between the study-note rule and the first study note. The default is 2.

*(Internal ID: `s_snBelowSpace` · Config key: `notes/belowstudyrulespace`)*

### Notes+Refs tab › Study Notes + Questions tab

#### Extended Footnotes (\ef)

- **Where:** Notes+Refs tab › Study Notes + Questions tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Use extended/study footnotes
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Extended Footnotes are the primary means for displaying study notes. These are similar to ordinary footnotes but appear as a 2-column block at the end of each page.

**Explanation:**

Prints the `\ef ... \ef*` study notes in their own two-column area at the bottom of the page. When it is not ticked, PTXprint removes all `\ef` notes from the text before making the PDF. Ticking it shows the layout and rule settings for study notes.

*(Internal ID: `c_extendedFnotes` · Config key: `studynotes/includextfn`)*

#### Sidebars (\esb ... \esbe)

- **Where:** Notes+Refs tab › Study Notes + Questions tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Include study note sidebars (\esb)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Sidebars (\esb ... \esbe) are used to contain larger blocks of topic-specific information.

**Explanation:**

Prints the study Bible sidebars (`\esb ... \esbe`), which are boxes with longer information about a topic. When it is not ticked, PTXprint removes them. Their appearance is set on the **Styles** tab.

*(Internal ID: `c_sidebars` · Config key: `studynotes/includesidebar`)*

#### Include Transcelerator Questions

- **Where:** Notes+Refs tab › Study Notes + Questions tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Include (Transcelerator) Checking Questions
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Use this option to include questions which have been created with SIL's Transcelerator tool for the purpose of comprehension testing.
>
> These will be displayed at the bottom of the page in the area normally used for Study Notes.
>
> Note that this option is only made available if the Transcelerator plugin's data folder for the project can be located.

**Explanation:**

Prints the Transcelerator checking questions in the notes area at the bottom of the page, near the verses they ask about. Greyed out when PTXprint cannot find Transcelerator data in the project. Ticking it shows the question settings and an example.

*(Internal ID: `c_txlQuestionsInclude` · Config key: `studynotes/txlinclquestions`)*

### Notes+Refs tab › Study Notes + Questions tab › Include Transcelerator Questions

#### Language Code

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Include Transcelerator Questions
- **Type:** Text box
- **View level:** Default and Full views
- **Only available when:** “Include Transcelerator Questions” is selected
- **Hidden until:** “Include Transcelerator Questions” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Enter the language code for the questions to be included. Usually this will be a 3-letter Ethnologue code (but other language tags such as en-US, fr, es are also acceptable).

**Explanation:**

The language of the questions to print. PTXprint fills this in from the Paratext project's language code when it is empty. It must match the language the questions were translated into in Transcelerator. Questions with no translation in this language are not printed.

*(Internal ID: `t_txlQuestionsLang` · Config key: `studynotes/txllangtag`)*

#### Show Overview Questions

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Include Transcelerator Questions
- **Type:** Checkbox (not ticked by default)
- **Description:** Transcelerator: Show overview questions
- **View level:** Default and Full views
- **Only available when:** “Include Transcelerator Questions” is selected
- **Hidden until:** “Include Transcelerator Questions” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Overview questions are designed to test the general understanding of the passage.

**Explanation:**

Also prints the overview questions, which ask about a whole passage rather than one verse.

*(Internal ID: `c_txlQuestionsOverview` · Config key: `studynotes/txloverview`)*

#### Number the Questions

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Include Transcelerator Questions
- **Type:** Checkbox (ticked by default)
- **Description:** Transcelerator: Number the questions
- **View level:** Default and Full views
- **Only available when:** “Include Transcelerator Questions” is selected
- **Hidden until:** “Include Transcelerator Questions” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This option enables the questions to be numbered sequentially for each book.

**Explanation:**

Numbers the questions 1, 2, 3 … in each book. This makes it easy to talk about a question during testing.

*(Internal ID: `c_txlQuestionsNumbered` · Config key: `studynotes/txlnumbered`)*

#### Include Chapter:Verse References

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Include Transcelerator Questions
- **Type:** Checkbox (not ticked by default)
- **Description:** Transcelerator: Include ch:vs references
- **View level:** Default and Full views
- **Only available when:** “Include Transcelerator Questions” is selected
- **Hidden until:** “Include Transcelerator Questions” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This option enables the questions to include the chapter:verse numbers.
>
> If the questions are also being numbered then the reference will be shown in parentheses (ch:vs).

**Explanation:**

Adds the chapter and verse of each question, for example `3:25`. If the questions are also numbered, the reference is shown in brackets after the number, for example `13. (3:25)`.

*(Internal ID: `c_txlQuestionsRefs` · Config key: `studynotes/txlshowrefs`)*

#### \ef

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Include Transcelerator Questions
- **Type:** Link
- **View level:** Full view only
- **Only available when:** “Include Transcelerator Questions” is selected
- **Hidden until:** “Include Transcelerator Questions” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the Extended Footnote properties on the Styles tab.
>
> The line spacing factor will modify the space between the questions.

**Explanation:**

Opens the **Styles** tab at the `\ef` style, which controls how study notes and Transcelerator questions look. Change the line spacing there to change the space between questions.

*(Internal ID: `lb_style_ef`)*

### Notes+Refs tab › Study Notes + Questions tab › Filter Categories › Filter Categories

#### tv_sbCatEdit

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Filter Categories › Filter Categories
- **Type:** Table
- **View level:** Full view only
- **Only available when:** “Filter Categories” is selected

**Explanation:**

The list of categories found in the project's study notes and sidebars, with a tick box for **Extended Footnote (\ef)** and one for **Sidebar (\esb)**. In this version, PTXprint does not save this list and does not use it when it makes the PDF.

*(Internal ID: `tv_sbCatEdit`)*

#### Add

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Filter Categories › Filter Categories
- **Type:** Button
- **Description:** Add sidebar category to filter
- **View level:** Full view only
- **Only available when:** “Filter Categories” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Add a new Category.

**Explanation:**

Adds a category to the list. Type its name in the box that opens.

*(Internal ID: `b_sb_addcat`)*

#### Del

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Filter Categories › Filter Categories
- **Type:** Button
- **Description:** Delete sidebar category from filter
- **View level:** Full view only
- **Only available when:** “Filter Categories” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Delete the currently selected Category.

**Explanation:**

Removes the selected category from the list.

*(Internal ID: `b_sb_delcat`)*

#### ↺

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Filter Categories › Filter Categories
- **Type:** Button
- **Description:** Rescan categories to filter sidebars
- **View level:** Full view only
- **Only available when:** “Filter Categories” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Clicking this button will rescan the project to add any Categories missing from this list.

**Explanation:**

Searches all books of the project for `\cat ... \cat*` and fills the list again with the categories it finds. The list is also filled when you first tick **Filter Categories**.

*(Internal ID: `btn_sb_rescanCats`)*

### Notes+Refs tab › Study Notes + Questions tab › Filter Categories

#### Filter Categories

- **Where:** Notes+Refs tab › Study Notes + Questions tab › Filter Categories
- **Type:** Checkbox (not ticked by default)
- **Description:** Filter study note sidebars
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Use this option to restrict certain categories of extended study notes and sidebars from being displayed.

**Explanation:**

Shows the category list. When you tick it and the list is empty, PTXprint searches the project for categories. In this version, the filter does not change the PDF.

*(Internal ID: `c_filterCats` · Config key: `studynotes/filtercats`)*
