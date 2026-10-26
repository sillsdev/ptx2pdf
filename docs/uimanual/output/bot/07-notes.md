# 10. Notes+Refs tab

## 10.1 What this tab is for

The **Notes+Refs** tab controls the extra information that sits outside the main Bible text. It has three sub-tabs: **Footnotes**, **Cross-References** and **Study Notes + Questions**. Come here to show or hide notes, change where they appear on the page, change the small marks that point to them, or add thousands of cross-references from a ready-made list.

There are three kinds of notes:

* **Footnotes** (`\f` in the text) explain something about the text. For example: "Some old manuscripts add the words …" or "Hebrew: *son of Adam*". The translation team writes them in Paratext.
* **Cross-references** (`\x` in the text) are only lists of other Bible places about the same thing. For example: "Gen 1:1; Ps 33:6". They can come from the project text, or PTXprint can add them from an external list.
* **Extended notes or study notes** (`\ef` in the text) are longer explanations, like the notes in a study Bible. PTXprint prints them in their own area at the bottom of the page, usually in two columns. Transcelerator comprehension questions are printed in this same area.

Some words used in this chapter:

* **Caller** – the small mark in the Bible text (for example *a*, *b* or †) that tells the reader "there is a note about this". The same mark is usually repeated at the start of the note.
* **Rule** – a thin horizontal line between the Bible text and the notes area.
* **Gutter** – the empty space between two columns.
* **pt** (point) – a small unit of measure. 1 pt is about 0.35 mm, and 72 pt is about 25 mm (1 inch).

The **Notes+Refs** tab is shown in the **Basic** view and above. Many settings are only shown in the **Regular** or **Full** view. External cross-reference lists and extended study notes are only shown in the **Full** view.

## 10.2 Footnotes

On the **Footnotes** sub-tab, the top area decides *whether* footnotes are printed and *where* they go.

* **Include Footnotes** turns all footnotes on or off. When it is off, PTXprint removes every `\f ... \f*` note before it makes the PDF, and most other footnote settings are greyed out.
* **Placement of Footnotes** has these choices:
  * **End of Page** – the normal choice. Notes appear at the bottom of the page where their caller is.
  * **End of Column** – only possible with a **Two Column Layout** (set on the **Layout** tab). The notes are set at the width of one column, at the bottom of the second column.
  * **End of Book** – the notes are collected and printed at the end of each book, as end notes.
  * **Side Margin** – the notes go in a narrow column next to the text, as close as possible to the line with the caller. This is greyed out until you tick **Margin Notes Col Width (mm)** on the **Layout** tab (**Page Setup** area). If you turn margin notes off again, PTXprint moves the footnotes back to **End of Page**.
* **Start Each Footnote on a New Line** – normally short footnotes run on one after the other in one paragraph, which saves a lot of space. Tick this if each note must start on its own line.

### Callers

The caller settings decide which marks are used for footnotes.

* **Show Callers** (in the text) – when ticked, PTXprint uses the sequence of marks in the box next to it. Separate the marks with commas and no spaces, for example `a,b,c,d,e` or `†,‡,§`. The reload button next to the box loads the callers from the Paratext project settings.
* **Show Callers in Notes Area** – repeats the caller at the start of each note, so the reader can find the note that belongs to the mark.
* **Reset Callers on Page** – starts the sequence again at the first mark on every new page.
* **Override hidden/automatic Footnote caller settings** – in Paratext, each footnote says how its caller works: `\f +` (automatic caller), `\f -` (no caller), or a fixed mark. Normally PTXprint obeys the text. When you tick this option, PTXprint uses the **Show Callers** setting for every footnote instead.

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

## 10.3 Cross-References

The **Cross-References** sub-tab works like the **Footnotes** sub-tab, but it also lets you add cross-references from an external list.

### Where the cross-references come from

* **Include Cross-References (From Project Text)** prints the `\x ... \x*` notes that the team typed in Paratext.
* **Use External List of Cross-References** (only in the **Full** view) adds cross-references from a list that comes with PTXprint, or from your own file. PTXprint changes the book names into the short book names of your project (the abbreviations in the Paratext **Scripture Reference Settings**, which should match the `\toc3` lines). These cross-references have no caller in the text. They are usually used for a study or reference Bible, together with **Column Cross-References**.

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

* If you choose **End of Column** for one kind of note, the other kind moves to **End of Column** too. The same happens for **End of Page**.
* If you choose **Column Cross-References**, the footnote placement changes to **End of Column**, and the **Source for References** area opens.
* If you untick **Include Footnotes** while cross-references are **Below Footnotes** or **Blend with Footnotes**, the cross-references move to **End of Page** (or to **Column Cross-References** if you use an external list).

The caller settings (**Show Callers**, **Show Callers in Notes Area**, **Reset Callers on Page**, **Override…**) work the same way as for footnotes.

### Source for References

This area (only in the **Full** view) is active when **Use External List of Cross-References** is ticked.

**External Refs** chooses the list:

* **Standard list (fewest)** to **Standard list (most)** – one large list of more than 340,000 cross-references. People have voted for the references, so the most useful ones come first. The five sizes take more or fewer of them: **(fewest)** gives only the most important references, **(most)** gives the most. Start with **Standard list** and change it if the column is too empty or too full.
* **Strong's list (all)** and **Strong's list (project)** – cross-references grouped by Strong's number (a number for each Hebrew or Greek word). The **(project)** list only uses words that have a rendering in your project's Biblical Terms. These two choices make the **Strong's References** area available.
* **TSK list** – the Treasury of Scripture Knowledge. It is very large.
* **BibleWorks™ list** – about 112,000 cross-references.
* **UBS GNT92 list** and **UBS GNT92 list (DC)** – the United Bible Societies list. Use **(DC)** if you need Deuterocanonical references.
* **Select a Custom list...** – use your own file. Then click **Select...** to choose it.

Hover the mouse over the small information button next to **Select...** to read a description of the chosen list.

**Include Refs for Books in** removes references that point to books your readers do not have. For example, if only the New Testament is translated, choose **New Testament**.

### Strong's References

These settings are only available when the source is one of the Strong's lists. You can show the Strong's numbers in the cross-references and in the Bible text itself, and make an index book with **Generate Index...** (see the **Generate Strong's Index** dialog below).

### Column Cross-References

These settings are only available when the placement is **Column Cross-References**. They set the width of the column, the gutter next to it, the side of the page, the vertical rules, and how the references are placed in the column. The column takes space from the Bible text. A larger page size, or a smaller `\x` font (about 6 pt), can help.

### Rule and Space Settings

These settings are for the cross-reference rule. PTXprint uses them only when footnotes or cross-references are at the **End of Book** (see **Footnotes** above).

## 10.4 Study Notes + Questions

This sub-tab is for study Bibles and for comprehension testing.

### Extended Footnotes (\ef)

Tick **Extended Footnotes (\ef)** (only in the **Full** view) to print the `\ef ... \ef*` study notes from the text. They appear in their own two-column area at the bottom of the page, under the ordinary notes. If this box is not ticked, PTXprint removes all `\ef` notes before it makes the PDF. When it is ticked, the area below shows settings for the gutter, the vertical rule between the columns, callers, and the rule above the study notes.

**Sidebars (\esb ... \esbe)** prints the boxed sidebars of a study Bible. If it is not ticked, PTXprint removes them. The look of sidebars is set on the **Styles** tab and in the sidebar settings.

### Include Transcelerator Questions

Transcelerator is a Paratext plugin from SIL for making comprehension-checking questions. If your project has Transcelerator data, PTXprint can print the translated questions at the bottom of each page, in the same area as study notes. Each question appears near the verse it is about. This is useful for comprehension-testing printouts. The **Example Questions** text shows how your choices will look. If there is no Transcelerator data for the project, the checkbox is greyed out.

### Filter Categories

In a study Bible, notes and sidebars can have a category, for example `\cat History\cat*`. **Filter Categories** (only in the **Full** view) shows a list of the categories in the project, with a tick box for extended notes and for sidebars. In this version, PTXprint does not save this list with the configuration, and it does not use it when it makes the PDF.

## 10.5 Generate Strong's Index dialog

To open this dialog, go to **Notes+Refs** › **Cross-References** and tick **Use External List of Cross-References**. Choose a **Strong's list** in **External Refs**, and then click **Generate Index...**.

The dialog makes a new book (in USFM, the Paratext file format) that lists each Strong's number and information about the word. Readers use it to look up a number they see in the cross-references. You choose:

* which sections to include: Hebrew words, Greek words, and an optional **Reverse Index** (an alphabetical list of words in your language, with their numbers);
* what each entry shows: the Hebrew or Greek word, a transliteration (the word written in Latin letters), your project's term renderings, a key verse reference, the definition and notes;
* what to use when your project has no rendering for a word: a rendering from another project, or a gloss in a major language;
* the headings of the index (in the table), the book to use, and one or two columns.

When you click **Create Index**, PTXprint writes the index into the chosen book of your project (normally **XXS**). **Warning:** anything that was already in that book is replaced. PTXprint then adds the book to the list of books to print and changes the book selection to multiple books. Click **Print** to see it.

The renderings come from your project's Biblical Terms renderings in Paratext. Fill those in first for a useful index.

## 10.6 Common tasks

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
2. For cross-references, tick **Start Each Cross-Reference on a New Line** on the **Cross-References** sub-tab.

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

## 10.7 Common problems

**The footnote or cross-reference settings are greyed out.**
Most footnote settings need **Include Footnotes**. The caller box and related settings need **Show Callers**. **End of Column** needs **Two Column Layout** on the **Layout** tab. **Side Margin** needs **Margin Notes Col Width (mm)** on the **Layout** tab. The **Source for References** settings need **Use External List of Cross-References**. The **Column Cross-References** settings need the **Column Cross-References** placement.

**I cannot find external cross-references, extended notes or the rule settings.**
These are only shown in the **Full** view. Change the view level and look again.

**The callers in the PDF are not the ones I typed.**
The notes in the text can ask for no caller (`\f -`) or a fixed caller. Tick **Override hidden/automatic Footnote caller settings** (or the cross-reference version), so that PTXprint uses your sequence for every note.

**Reset Callers on Page does not seem to work.**
PTXprint needs to know the page breaks first. Click **Print** a second time.

**The footnotes run into the footer.**
Increase **Space Above Rule (pt)** on the **Footnotes** sub-tab. This makes the page break a little earlier.

**My cross-reference placement changed by itself.**
PTXprint changes the footnote and cross-reference placements together (see "Placement of Cross-References" above). Check both sub-tabs after you change one of them.

**Changing the cross-reference rule settings has no effect.**
They are used only when footnotes are at the **End of Book** (see "Rule and Space Settings" under **Footnotes**). Change the rule on the **Footnotes** sub-tab instead.

**The external cross-references show the wrong book names.**
PTXprint uses the short book names from the Paratext project (**Scripture Reference Settings**, which should match the `\toc3` lines). Correct them in Paratext, then print again.

**Making the PDF is very slow.**
**Show Numbers in the Text** (for Strong's numbers) takes a lot of time. Untick it while you work on the layout. Very large cross-reference lists (for example **TSK list** or **Standard list (most)**) also make the PDF slower.

**Include Transcelerator Questions is greyed out.**
PTXprint cannot find Transcelerator data for this project. Use the Transcelerator plugin in Paratext for this project first. If the box can be ticked but no questions are printed, check that the **Language Code** matches the language the questions were translated into.

**The study notes do not appear.**
Tick **Extended Footnotes (\ef)** on the **Study Notes + Questions** sub-tab (only shown in the **Full** view). If it is not ticked, PTXprint removes all `\ef` notes.

## 10.8 Settings reference

### Generate Strong's Index... (dialog)

#### Create Index

Button · Regular+ · `btn_strong_ok`

> Click to generate the index book (USFM file) which will be appended to the list of books to be printed.
>
> Warning: This will overwrite the existing book/file.

Makes the index book and closes the dialog. PTXprint also changes the book selection to multiple books. Any text already in that book is replaced without another warning.

#### Cancel

Button · Regular+ · `btn_strong_cancel`

Closes the dialog without making an index. Your choices in the dialog are kept.

#### For Strong's Cross References to be most useful to readers, it is highly recommended to include an Index at the end of the publication. Set appropriate options here to create an Index file (in USFM format).

Label · Mini+

> Set the options (below), to create the Index file in a temporary book (XXS, or XXA...XXG). After clicking "Create Index", the generated index book will be appended to the list of books to be printed.

#### Hebrew Words (from the OT)

Checkbox, on · Regular+ · `c_strongsHeb` · cfg `strongsndx/showhebrew`  
Also: Strong's index: Include section for Hebrew words

Lists the Hebrew (Old Testament) Strong's numbers. Untick it if your publication is only the New Testament.

#### Greek Words (from the NT)

Checkbox, on · Regular+ · `c_strongsGrk` · cfg `strongsndx/showgreek`  
Also: Strong's index: Include section for Greek words

Lists the Greek (New Testament) Strong's numbers. Untick it if your publication is only the Old Testament.

#### \li

Link · Regular+ · `lb_style_li+strong-s`

> Click to select this marker on the Styles tab.
>
> Select which components should be included in the Strong's index when it is generated.

The `\li` style is used for each entry in the Strong's index. Change it to adjust the font size or indent of the entries.

#### Reverse Index (alphabetical listing with numbers)

Checkbox, off · Regular+ · `c_strongsNdx` · cfg `strongsndx/showindex`  
Also: Strong's index: Include section for reverse index

> This (optional) section is intended for readers who want to look up a word in their own language to find out the Strong's number.

Comes after the main lists. It lists your project's renderings in alphabetical order, each with its Strong's numbers, sorted with the Paratext project's sorting rules. It can only be made when the project has Biblical Terms renderings.

#### Hebrew or Greek Word

Checkbox, on · Regular+ · `c_strongsSrcLg` · cfg `strongsndx/sourcelang`  
Also: Strong's index entry: Include Hebrew and/or Greek

> The word in the source language(s) can be displayed in the index if useful to readers.

Your font must contain Hebrew and Greek letters, or the words will not show correctly. The `\wh` and `\wg` styles control how these words look.

#### Transliteration (Latin Script)

Checkbox, off · Regular+ · `c_strongsTranslit` · cfg `strongsndx/transliterate`  
Also: Strong's index entry: Include transliteration of source languages

> If the readers are unfamiliar with Greek and Hebrew it may be more useful in some contexts to show the transliterated (romanized) source language words.

The `\wl` style controls how it looks.

#### Term Rendering(s)

Checkbox, on · Regular+ · `c_strongsRenderings` · cfg `strongsndx/renderings`  
Also: Strong's index entry: Include receptor term renderings

> Show the term renderings from the project's Biblical Terms list.

Uses the Biblical Terms renderings in Paratext. This is usually the most useful part of each entry. If a word has no rendering, PTXprint uses the fallback settings below.

#### If No Local Rendering Found

Label · Mini+

> If no local term rendering is found in the Project's list of Biblical Term renderings, then several fallback options are possible:  
> a) Use the renderings from a regional language project b) Use a gloss from one of the majority languages c) Use the Biblical Term's definition (in English)

#### Key Verse Reference

Checkbox, on · Regular+ · `c_strongsKeyVref` · cfg `strongsndx/keyvrsrefs`  
Also: Strong's index entry: Include key verse reference

> The primary book, chapter and verse reference for the entry helps users find the first item in the list of cross-references related to the term.

The `\xt` style controls how it looks.

#### Definition

Checkbox, off · Regular+ · `c_strongsDefn` · cfg `strongsndx/definitions`  
Also: Strong's index entry: Include definitions

> Show the definition in addition to the term rendering(s).

The definition is in English and comes after the renderings. It makes the index longer.

#### \wl

Link · Regular+ · `lb_style_wl+strong-s`

> Click to select this marker on the Styles tab.

Opens the `\wl` style (the transliteration) used in the Strong's index.

#### \xt

Link · Regular+ · `lb_style_xt+strong-s`

> Click to select this marker on the Styles tab.

Opens the `\xt` style (the key verse reference) used in the Strong's index.

#### \wh

Link · Regular+ · `lb_style_wh+strong-s`

> Click to select this marker on the Styles tab.

Opens the `\wh` style (Hebrew words) used in the Strong's index. You can choose a font with Hebrew letters there.

#### \wg

Link · Regular+ · `lb_style_wg+strong-s`

> Click to select this marker on the Styles tab.

Opens the `\wg` style (Greek words) used in the Strong's index. You can choose a font with Greek letters there.

#### Remove (Comments) from Renderings

Checkbox, off · Regular+ · `c_strongsNoComments` · cfg `strongsndx/nocomments`  
Also: Strong's index entry: Remove comments from renderings

> Paratext allows for additional comments or notes to be added (in brackets) after term renderings. Check this option to prevent these from showing in the Strong's index.

Removes any text in round brackets ( ) from the renderings. Readers usually do not need these comments.

#### Wildcard* handling – Strong's index entry: How to handle wildcard* character

Drop-down · Regular+ · `fcb_strongswildcards` · cfg `strongsndx/wildcards`  
Choices: Keep wildcard* | Remove wildcard | Change to hyphen-

> The asterisk * is used as a matching wildcard in Term Renderings. If you prefer for this not to be displayed, select an appropriate option.

A wildcard such as `bless*` matches several word forms. **Change to hyphen-** prints a hyphen instead of the `*`.

#### tv_strvarEdit

Table · Regular+ · `tv_strvarEdit`

A table of the headings PTXprint uses in the index: the title of the book (`index_book_title`), the Hebrew and Greek section titles, and the title of the reverse index. Click a value to type the heading in your language.

#### Create Index in Book – Strong's index: Extra book code to be used

Drop-down · Regular+ · `fcb_strongsNdxBookId` · cfg `strongsndx/ndxbookid`  
Choices: XXS | XXA | XXB | XXC | XXD | XXE | XXF | XXG

> Select the temporary book to be used for the generated Strong's Cross Reference Index.
>
> By default, an extra book XXS is used to store the index. But if you prefer to use one of the other standard Paratext books XXA...XXG then select it here, but be aware that it will overwrite whatever is in that book without prior warning.

**XXS** is the default. Choose a book you do not use for anything else, because its contents are replaced.

#### Two Column Layout

Checkbox, on · Regular+ · `c_strongs2cols` · cfg `strongsndx/twocols`  
Also: Strong's index: Use 2-column layout

> Using a two column layout for the index is highly recommended, but if you prefer a one column layout, uncheck this option.

Recommended, because the entries are short. Untick it for one column.

#### Open Index File in Editor

Checkbox, off · Regular+ · `c_strongsOpenIndex` · cfg `strongsndx/openineditor`  
Also: Strong's index: Open index file after creating it

> Check this option to open the generated file in a text editor after the Index has been created.

Use it to check the new index file.

#### Unbalanced Lines (max) – Strong's index: Allow unbalanced lines

Number · Regular+ · `s_strongRag` · cfg `strongsndx/raglines`  
Needs: “Two Column Layout”

> By default (when this is set to 0) PTXprint will balance the number of lines used in each column. Sometimes this results in large empty spaces at the end of a page.
>
> Increasing this number (recommended range 1-4) will allow up to that many unbalanced lines on the page.

A value of 1 to 4 can avoid large empty spaces.

#### Notes

Checkbox, off · Regular+ · `c_strongsNotes` · cfg `strongsndx/notes`

> This is the Description field from the project's Biblical Terms renderings.

Adds this description text to each index entry. It is saved with the configuration, like the other settings in this dialog.

#### If No Local Rendering Found:

##### Use the Term Rendering from a Fallback Project

Label · Mini+

> Select the project to search within for a term rendering for entries which do not have a local rendering.

##### Use Major Language Gloss – Strong's index: Use major language gloss (if no rendering found)

Drop-down · Regular+ · `fcb_strongsMajorLg` · cfg `strongsndx/majorlang`  
Choices: None | English | French | Indonesian | Portuguese | Spanish

> If all else fails, you can display the gloss in a major language.

Used only when there is no rendering in your project or in the fallback project. Choose **None** to leave these words without a gloss.

##### Use Major Language Gloss

Label · Mini+

> If all else fails, you can display the gloss in a major language.

##### Use the Term Rendering from a Fallback Project – Strong's index: Use fallback project (if no rendering found)

Drop-down · Regular+ · `fcb_strongsFallbackProj` · cfg `strongsndx/fallbackprj`

> Select the project to search within for a term rendering for entries which do not have a local rendering.

For example, a project in a regional language. PTXprint uses its Biblical Terms renderings for words with no rendering in your project.

### Notes+Refs

#### Footnotes

##### Show Callers in Notes Area

Checkbox, on · Regular+ · `c_fnomitcaller` · cfg `notes/fnomitcaller`  
Also: Show footnote callers in notes area · Needs: “Include Footnotes”, “Show Callers in the Text”

> Usually the "Caller" symbol is also shown in the notes area which helps the reader quickly find the footnote from the text.

Untick it to print the note without the mark. This saves a little space.

##### Reset Callers on Page

Checkbox, on · Regular+ · `c_fnpageresetcallers` · cfg `notes/fnresetcallers`  
Also: Reset footnote callers on each page · Needs: “Include Footnotes”, “Show Callers in the Text”

> If this is checked, then the sequence of callers starts again from the 1st item in the list of callers specified.
>
> Note that this feature doesn't always take effect straight away. You may need to hit Print a second time before it applies.

This keeps the callers short when you use symbols.

##### Show Callers in the Text

Checkbox, on · Regular+ · `c_fnautocallers` · cfg `notes/iffnautocallers`  
Also: Show Footnote Callers in the Text · Needs: “Include Footnotes”

> A "Caller" is a symbol (in the text) which alerts the reader that there is further information (in this case a footnote at the bottom of the page). Ideally, the caller should be distinct from the rest of the text, so a symbol works well if supported by the font. Otherwise the letters of the alphabet can be used.
>
> Separate callers with a comma (no spaces). For example: a,b,c,d,e,f,g,h, etc. or:  †,‡,§,∥,#    or: ✶,☆,✦,✪
>
> If you do not see the callers you are expecting in the PDF, then try using the "Override..." setting above.

When not ticked, the caller box is greyed out and no automatic caller sequence is used. Together with **Override hidden/automatic Footnote caller settings**, unticking it removes the callers from all footnotes.

##### Footnote Caller Sequence Entry

Text box · Regular+ · `t_fncallers` · cfg `notes/fncallers`  
Needs: “Include Footnotes”, “Show Callers in the Text”

> These callers should automatically be loaded from the settings in the Paratext project, but can be modified here if needed. (Use the button on the right to reload them if needed.)
>
> Separate callers with a comma (no spaces). For example: a,b,c,d,e,f,g,h, etc. or:  †,‡,§,∥,#    or: ✶,☆,✦,✪

When the sequence reaches the end, it starts again. Make sure your font has the symbols you type.

##### Reload footnote callers from Paratext

Button · Regular+ · `btn_resetFNcallers`  
Needs: “Include Footnotes”, “Show Callers in the Text”

> Clicking this button will reload the footnote callers from the Paratext project settings.
>
> If the callers have not been defined in the Paratext project, or are already showing, then a default set will appear.

PTXprint's own default sequence is `a,b,c,d,e,f,✶,☆,✦,✪,†,‡,§`.

##### Override hidden/automatic Footnote caller settings

Checkbox, off · Regular+ · `c_fnOverride` · cfg `notes/fnoverride`  
Also: Override Footnote Settings in Text · Needs: “Include Footnotes”

> The Footnotes specified in Paratext use  
> \f +(plus) to cycle through the callers, or \f - (minus) to omit the caller.
>
> If this option is enabled, the Show Callers settings below will override whatever has been specified within the text itself.

Use this when the callers in the PDF do not follow your settings. PTXprint changes every footnote to `\f +` if **Show Callers** is ticked, or to `\f -` if it is not.

##### Start Each Footnote on a New Line

Checkbox, off · Basic+ · `c_fneachnewline` · cfg `notes/fneachnewline`  
Needs: “Include Footnotes”

> Normally footnotes are arranged one after the other to form a block of text. But if you require each footnote to start on its own new line then set this option.

This uses more space than run-on notes. When both this and **Start Each Cross-Reference on a New Line** are ticked, the horizontal spacing settings are greyed out, because they are only used for run-on notes.

##### \f

Link · Regular+ · `lb_style_f`  
Needs: “Include Footnotes”

> Click to edit the Footnote properties on the Styles tab.

Change the font size, line spacing and other footnote properties there.

##### End of Book

Radio · Regular+ · `r_fnpos_endnote` · cfg `notes/fnpos=endnote`, `notes/columnnotes_=endnote`, `notes/endnotes_=endnote`, `notes/fnmarginal_=endnote`  
Also: Placement of footnotes: End notes · Needs: “Include Footnotes”

> This option will prevent footnotes showing on each page, but will gather them together and place them all at the end of the book.

Use this when there are few notes or when you want clean pages.

##### End of Column

Radio · Regular+ · `r_fnpos_column` · cfg `notes/fnpos=column`, `notes/columnnotes_=column`, `notes/endnotes_=column`, `notes/fnmarginal_=column`  
Also: Placement of footnotes: End of column · Needs: “Two Column Layout”, “Include Footnotes”

> Use this option (only available in 2-column layout) to show the footnotes at the end of the 2nd column of text.
>
> Footnotes and cross-references at the foot of the page are kept together, so changing this may also change where the cross-references are placed.

The notes are set at the width of one column. If cross-references are at **End of Page**, they also move to **End of Column**.

##### End of Page

Radio · Regular+ · `r_fnpos_normal` · cfg `notes/fnpos=normal`, `notes/columnnotes_=normal`, `notes/endnotes_=normal`, `notes/fnmarginal_=normal`  
Also: Placement of footnotes: End of page · Needs: “Include Footnotes”

> Footnotes (and cross-references) are usually placed at the end of each page.

The usual choice. If cross-references are at **End of Column**, they move to **End of Page** too.

##### Include Footnotes

Checkbox, on · Basic+ · `c_includeFootnotes` · cfg `notes/includefootnotes`

> Select whether footnotes should be included.
>
> The specific settings for these are located on the Footnotes tab.

Unticked, all footnotes are left out of the PDF. They stay in your Paratext project. Most footnote settings are then greyed out. Cross-references set to **Below Footnotes** or **Blend with Footnotes** move to another placement.

##### Only show verse numbers from \fr

Checkbox, off · Regular+ · `c_frVerseOnly` · cfg `notes/frverseonly`

> The footnote reference \fr usually includes the chapter & verse number like this 3:16. If you prefer to hide the chapter, so that only 16 is shown, then enable this option.

This saves space, because the chapter is usually clear from the page.

##### Side Margin

Radio · Regular+ · `r_fnpos_margin` · cfg `notes/fnpos=margin`, `notes/columnnotes_=margin`, `notes/endnotes_=margin`, `notes/fnmarginal_=margin`  
Also: Placement of footnotes: Side Margin · Needs: “Margin Notes Col Width (mm)”

> This option will place footnotes (and optionally also the Cross-references and Section Headings) in a column next to the text and align them as closely as possible vertically to their caller.
>
> This option is only available if Margin Notes has been enabled on the Layout Tab.

If you turn margin notes off, the footnotes go back to **End of Page**.

##### Rule and Space Settings

###### Space Above Rule (pt) – Space above footnote rule

Number · Regular+ · `s_fnAboveSpace` · cfg `notes/abovenotespace`  
Values: -50–50 (default 6)

> The vertical space between the main text body and the footnote rule.
>
> Note: if you make this value less than the descenders of the last lines of text, then the footnotes will push down into the footer area. If you see this happening, increase this value to trigger an earlier page break to solve the problem.
>
> The vertical space between the body text and the area containing footnotes and cross-references.
>
> If the Footnote Rule is not shown, the vertical space will still be calculated as the Space Above plus the Space Below (the imaginary) Rule.

Also increase it if the notes look too close to the text. Negative values are possible but rarely useful.

###### Space Below Rule (pt) – Space below footnote rule

Number · Regular+ · `s_fnBelowSpace` · cfg `notes/belownoterulespace`  
Values: -50–50 (default 2) · Needs: “Show Footnote Rule”

> This is the vertical space/gap (pts) between the rule and the footnotes.

PTXprint adds this space even when the rule is hidden.

###### Show Footnote Rule

Checkbox, on · Regular+ · `c_footnoterule` · cfg `notes/iffootnoterule`

> This is the horizontal rule separating the body text from the footnote area.

This rule is also used above cross-references at the bottom of the page. Untick it for a cleaner look. The space above and below is kept.

###### Rule Positioning and Parameters – Footnote rule: Indent

Number · Full · `s_fnIndent` · cfg `notes/fnruleindent`  
Needs: “Show Footnote Rule”

> Distance (mm) to move the rule in from the side chosen in Horizontal Position.

Use 0 for no indent.

###### Rule Positioning and Parameters – Footnote rule: Length

Number · Full · `s_fnLength` · cfg `notes/fnrulelength`  
Values: 20–100 (default 100) · Needs: “Show Footnote Rule”

> The length of the rule as a percentage of the column/page width.

Short rules of 20 to 40 are common in books.

###### Rule Positioning and Parameters – Footnote rule: Line Thickness

Number · Full · `s_fnThick` · cfg `notes/fnrulethick`  
Values: 0.1–2 (default 0.5) · Needs: “Show Footnote Rule”

> The thickness of the rule.

The value is in pt. Use a smaller value, like 0.3, for a lighter line.

###### Rule Positioning and Parameters – Footnote rule: Horizontal position

Drop-down · Full · `fcb_fnHorizPosn` · cfg `notes/fnruleposn`  
Choices: Left | Right | Inner | Outer | Center · Needs: “Show Footnote Rule”

> Which side of the column the rule is aligned to:  
> Left, Right, Center, Inner (spine side) or Outer. Inner and Outer swap sides on odd and even pages. This only matters when the Length is less than 100%.
>
> These settings control the rule (horizontal line) above the notes: its indent (mm), its length (% of the column width), its thickness (pt) and which side of the column it is aligned to.

Positions a footnote rule that is shorter than 100%.

##### Miscellaneous Footnote Settings

###### Add a Colon ':' After \fq and \xq

Checkbox, off · Full · `c_addColon` · cfg `notes/addcolon`  
Also: Add colon after quoted text in notes

> Some projects prefer to separate the Quoted text from the footnote text with a colon ':' which helps keep the elements visually distinct.

For example "*light*: Or *brightness*". Use it if your team does not type the colon in the notes.

###### Keep Book Names and Refs Together

Checkbox, on · Full · `c_keepBookWithRefs` · cfg `notes/keepbookwithrefs`

> This option inserts a space that discourages line breaks between the book name and the Ch:Vs refs so that they don't get split across lines.
>
> It also prevents single letters being left at the end of a line in note text.
>
> Note:  This setting currently has no effect on cross-references imported from external lists.

For example, "John 3:16" stays on one line.

###### Show All Glossary Entries as Footnotes

Checkbox, off · Full · `c_glossaryFootnotes` · cfg `notes/glossaryfootnotes`

> Glossary entries for ALL marked-up Biblical Terms on each page can be made to appear as footnotes.
>
> Glossary words are marked like \w word\w* in the USFM text file. Only the first paragraph of each glossary entry is used.
>
> This feature is extremely useful when producing printouts for comprehension testing (where  Key Biblical Terms in the passage which have Glossary Entries also need to be checked for understanding).

The entries come from the GLO book. This adds many footnotes.

###### Horizontal Space Separating Notes – Minimum Horizontal Space Separating Notes

Number · Full · `s_notespacingmin` · cfg `notes/horiznotespacemin`  
Values: 2–20 (default 5)

> This spacing is set in points (pts). Changing this will increase or decrease the MINIMUM horizontal space between notes that have been run together.
>
> The horizontal space between notes that are being run together as a single paragraph can be set here. The default space is calculated as 33% between min & max values.
>
> For example if min=6pt and max=15pt then the default horizontal space between notes would be 9pt.
>
> If this control is disabled, it is because both the Footnotes and Cross-References have been set to start on a new line. (see \f and \x settings above).

The maximum must be larger, so PTXprint adjusts **Maximum Space** when you change this.

###### Horizontal Space Separating Notes – Maximum Horizontal Space Separating Notes

Number · Full · `s_notespacingmax` · cfg `notes/horiznotespacemax`  
Values: 5–40 (default 25)

> This spacing is set in points (pts). Changing this will increase or decrease the MAXIMUM horizontal space between notes that have been run together.

PTXprint stretches or shrinks the space to fill lines. A larger range gives PTXprint more freedom.

###### Vertical Space Between Footnotes and xRefs (pt) – Vertical Space Between Footnotes and xRefs

Number · Full · `s_internote` · cfg `notes/internotespace`  
Needs: “Column Cross-References” · Greyed out by: “Blend with Footnotes”

> When Footnotes and Cross-references are not blended together in the same block then the Footnotes appear in one block and the Cross-references in another block just below them. This setting (pts) lets you adjust the vertical space between these two sections.

The default is 3.5.

#### Cross-References

##### End of Book

Radio · Regular+ · `r_xrpos_endnote` · cfg `notes/xrlocation=endnote`, `notes/xrpos=endnote`, `notes/xrmarginal_=endnote`  
Also: Placement of cross-references: As End Notes

> This option will prevent cross-references showing on each page, but will gather them together and place them all at the end of the book.

Collected and printed at the end of each book.

##### End of Column

Radio · Regular+ · `r_xrpos_column` · cfg `notes/xrlocation=column`, `notes/xrpos=column`, `notes/xrmarginal_=column`  
Also: Placement of cross-references: End of column

> Use this option (only available in 2-column layout) to show the cross-references at the end of the 2nd column of text.
>
> Footnotes and cross-references at the foot of the page are kept together, so changing this may also change where the footnotes are placed.

Needs a two-column layout. If footnotes are at **End of Page**, they also move to **End of Column**.

##### End of Page

Radio · Regular+ · `r_xrpos_normal` · cfg `notes/xrlocation=normal`, `notes/xrpos=normal`, `notes/xrmarginal_=normal`  
Also: Placement of cross-references: End of page

> Cross-references are usually placed at the end of each page.

If footnotes are at **End of Column**, they move to **End of Page** too.

##### Start Each Cross-Reference on a New Line

Checkbox, off · Basic+ · `c_xreachnewline` · cfg `notes/xreachnewline`

> Normally cross-references are arranged one after the other to form a block of text. But if you require each cross-reference to start on its own new line then set this option.

This uses more space than run-on notes. When both this and **Start Each Footnote on a New Line** are ticked, the horizontal spacing settings on the **Footnotes** sub-tab are greyed out.

##### Override hidden/automatic Cross-reference caller settings

Checkbox, off · Regular+ · `c_xrOverride` · cfg `notes/xroverride`  
Also: Override Cross-Reference Settings in Text

> Cross-references specified in Paratext use  
> \x +(plus) to cycle through the callers, or \x - (minus) to omit the caller.
>
> If this option is enabled, the Show Callers settings below will override whatever has been specified within the text itself.

PTXprint uses `\x +` for every cross-reference if **Show Callers** is ticked, and `\x -` (no caller) if it is not.

##### Show Callers in the Text

Checkbox, on · Regular+ · `c_xrautocallers` · cfg `notes/ifxrautocallers`  
Also: Show Cross-Reference Callers in the Text

> A "Caller" is a symbol (in the text) which alerts the reader that there is further information (in this case a cross-reference at the bottom of the page). Some people prefer not to indicate cross-references in the text itself, but just to include them at the bottom of the page.
>
> Separate callers with a comma (no spaces). For example: a,b,c,d,e,f,g,h, etc. or:  †,‡,§,∥,#    or: ✶,☆,✦,✪
>
> If you do not see the callers you are expecting in the PDF, then try using the "Override..." setting above.

To show no cross-reference callers in the text at all, untick this and tick **Override…**.

##### Cross-Reference Caller Sequence Entry

Text box · Regular+ · `t_xrcallers` · cfg `notes/xrcallers`  
Needs: “Show Callers in the Text”

> These callers should automatically be loaded from the settings in the Paratext project, but can be modified here if needed. (Use the button on the right to reload them if needed.)
>
> Separate callers with a comma (no spaces). For example: a,b,c,d,e,f,g,h, etc. or:  †,‡,§,∥,#    or: ✶,☆,✦,✪

Choose marks that are different from the footnote callers, so readers can tell the two kinds of notes apart.

##### Reload cross-reference callers from Paratext

Button · Regular+ · `btn_resetXRcallers`  
Needs: “Show Callers in the Text”

> Clicking this button will reload the cross-ref callers from the Paratext project settings.
>
> If the callers have not been defined in the Paratext project, or are already showing, then a default set will appear.

PTXprint's default sequence is `†,‡,§,∥,#`.

##### Show Callers in Notes Area

Checkbox, on · Regular+ · `c_xromitcaller` · cfg `notes/xromitcaller`  
Also: Show cross-reference callers in notes area · Needs: “Show Callers in the Text”

> Usually the "Caller" symbol is also shown in the notes area which helps the reader quickly find the cross-reference from the text.

Untick it to save a little space.

##### Reset Callers on Page

Checkbox, on · Regular+ · `c_xrpageresetcallers` · cfg `notes/xrresetcallers`  
Also: Reset cross-reference callers on each page · Needs: “Show Callers in the Text”

> If this is checked, then the sequence of callers starts again from the 1st item in the list of callers specified.
>
> Note that this feature doesn't always take effect straight away. You may need to hit Print a second time before it applies.

Works like **Reset Callers on Page** for footnotes.

##### \x

Link · Regular+ · `lb_style_x`

> Click to edit the Cross-Reference properties on the Styles tab.

For column cross-references, a small size (about 6 pt) is often needed.

##### Below Footnotes

Radio · Regular+ · `r_xrpos_below` · cfg `notes/xrlocation=below`, `notes/xrpos=below`, `notes/xrmarginal_=below`  
Also: Placement of cross-references: Below footnotes

> Cross-references will be listed in a separate block underneath the footnotes (rather than combined along with the footnotes as a single paragraph).

**Vertical Space Between Footnotes and xRefs** sets the gap between the two blocks.

##### Blend with Footnotes

Radio · Regular+ · `r_xrpos_blend` · cfg `notes/xrlocation=blend`, `notes/xrpos=blend`, `notes/xrmarginal_=blend`  
Also: Placement of cross-references: Blend with footnotes

> To save space in the footnote area, you can combine the  footnotes and cross-references as a single paragraph (rather than the cross- references appearing in a separate block underneath the footnotes). If this option is used, the Cross-References can only have one type of caller (rather than a sequence) which must be specified above.

This saves space. PTXprint sets the `\x` style on the **Styles** tab so that it joins the footnotes.

##### Column Cross-References

Radio · Regular+ · `r_xrpos_centre` · cfg `notes/xrlocation=centre`, `notes/xrpos=centre`, `notes/xrmarginal_=centre`  
Also: Placement of cross-references: Vertical column

> When there are numerous cross-references (usually when using an external list of references) then it may be useful to place them in their own column.
>
> The cross references will appear in a narrow vertical column similar to a study/reference Bible layout.

With a two-column layout the column is between the text columns. With one column, choose the side in **Side of page**. Choosing this sets footnotes to **End of Column** and opens the **Source for References** area. Set the width and other settings in the **Column Cross-References** area.

##### Use External List of Cross-References

Checkbox, off · Full · `c_useXrefList` · cfg `notes/ifxrexternalist`

> Instead of using a handful of cross-references as specified within the project's USFM text, you can select an external list containing many 1000's of cross-references. These will automatically be localized into the project's language using the  
> \toc3 values specified in the Paratext project settings (See: Scripture reference settings...)
>
> This feature is usually used for Study or Reference Bibles in conjunction with the 'Column Cross-References' placement option.

The list can also be your own file. Choose it in **Source for References**. The added references have no caller in the text. When ticked, the **Cross-References** sub-tab name is highlighted.

##### Show Extended Cross-References

Checkbox, off · Full · `c_extendedXrefs` · cfg `notes/showextxrefs`

> Study Bibles can (optionally) use extended cross-references (\ex) which can be displayed along with other kinds of cross-references.

When it is not ticked, PTXprint removes all `\ex ... \ex*` notes.

##### Include Cross-References (From Project Text)

Checkbox, on · Basic+ · `c_includeXrefs` · cfg `notes/includexrefs`  
Also: Include cross-references (from project)

> Select whether cross-references from the project's text should be included.
>
> The specific settings for these are located on the Cross-References tab.

This does not affect cross-references from an external list.

##### Only show verse numbers from \xo

Checkbox, off · Regular+ · `c_xoVerseOnly` · cfg `notes/xrverseonly`

> The cross-reference origin \xo usually includes the chapter & verse number like this 3:16. If you prefer to hide the chapter, so that only 16 is shown, then enable this option.

This also applies to cross-references from external lists. For a bridged verse (two or more verses joined), the whole range is shown, for example `13-14`.

##### Side Margin

Radio · Regular+ · `r_xrpos_margin` · cfg `notes/xrlocation=margin`, `notes/xrpos=margin`, `notes/xrmarginal_=margin`  
Also: Placement of cross-references: Side Margin · Needs: “Margin Notes Col Width (mm)”

> This option will place references (and optionally also the Footnotes and Section Headings) in a column next to the text and align them as closely as possible vertically to their caller.
>
> This option is only available if Margin Notes has been enabled on the Layout Tab.

If you turn margin notes off, the cross-references go back to **End of Page**.

##### Source for References

###### Include Refs for Books in – Include references for which category of books

Drop-down · Full · `fcb_filterXrefs` · cfg `notes/xrfilterbooks`  
Choices: Whole Bible | Paratext Project | This Publication | New Testament | Old Testament · Needs: “Use External List of Cross-References”

> The various cross-reference lists often contain hundreds of 1000s of references. You may want to only include target references that are currently available to your readers by selecting a subset of Biblical books.
>
> So for example, if there is no Old Testament yet, you may want to only include target cross-references to NT Books.
>
> If you select Books in "This Publication", then only cross-references targeting books in the "Portions or Multiple Books" list on the Basic tab will be included.

* **Whole Bible** – keep all references.
* **Paratext Project** – only books that exist in the project.
* **This Publication** – only the books in the list of books to print (**Basic** tab, **What to Print** area).
* **New Testament** or **Old Testament** – only that part of the Bible.

###### External Refs – Select external list of cross-references

Drop-down · Full · `fcb_xRefExtListSource` · cfg `notes/xrlistsource`, `notes/xrextlistsource`  
Choices: Standard list (fewest) | Standard list (fewer) | Standard list | Standard list (more) | Standard list (most) | Strong's list (all) | Strong's list (project) | TSK list | BibleWorks™ list | UBS GNT92 list | UBS GNT92 list (DC) | Select a Custom list... · Needs: “Use External List of Cross-References”

> There are multiple options to choose from if you wish to use an external list of cross-references. Select whichever is most appropriate and the list will automatically be localized to use the abbreviated book names as defined in Paratext's Scripture Reference Settings which should match the \toc3 markers.
>
> The five Standard list sizes take fewer or more references from the same prioritized list (fewest = only the most important ones).

The **Strong's** lists group references by Hebrew and Greek word, and make the **Strong's References** settings available. **Select a Custom list...** makes the **Select...** button available. Larger lists need more space on the page and take longer to process. See **Source for References** above for each list.

###### Select...

Button · Full · `btn_selectXrFile` · cfg `project/selectxrfile`  
Also: Select a custom cross-reference list · Needs: “Use External List of Cross-References”

Chooses your own cross-reference file. It starts in the Paratext `_Cross References` folder. PTXprint can read `.xrf` (the Paratext cross-reference format), `.xre` and `.xml` files. Only available when **External Refs** is **Select a Custom list...**. After you choose a file, hover over the button to see the file name.

###### Standard

Radio · Full · `r_xrSource_standard`  
Also: Source of cross-references: Standard list · Needs: “Use External List of Cross-References”

> The Standard List contains more than 340,000 cross-references which have been prioritized by crowd-sourcing.

Not shown on screen. Its text is the description of the **Standard list** shown by the information button. Choose the list in **External Refs**.

###### Strongs

Radio · Full · `r_xrSource_strongs`  
Also: Source of cross-references: Strong's list · Needs: “Use External List of Cross-References”

> The Strong's List contains a curated subset of cross-references generated from the Strong's Numbers. Optionally an index for these numbers can also be created as an additional book that can be appended to the publication.
>
> Each set of cross-references is indexed by a Hebrew or Greek Strong's number which can be looked up in the (optional) Index which can be generated using the "Generate Index..." button.

Not shown on screen. Its text is the description of the **Strong's** lists shown by the information button. Choose the list in **External Refs**.

###### TSK

Radio · Full · `r_xrSource_tsk`  
Also: Source of cross-references: Treasury of Scripture Knowledge · Needs: “Use External List of Cross-References”

> For generations, the Treasury of Scripture Knowledge has been an enduring cross-reference resource for Bible students worldwide. This highly respected and nearly exhaustive compilation of cross-references was developed by R.A. Torrey from references in the Rev. Thomas Scott's Commentary and the Comprehensive Bible. With nearly 500,000 cross-references it is the most thorough source available.

Not shown on screen. Its text is the description of the **TSK list** shown by the information button. Choose the list in **External Refs**.

###### BibWrx

Radio · Full · `r_xrSource_works`  
Also: Source of cross-references: The Works · Needs: “Use External List of Cross-References”

> The BibleWorks list contains 112,000 cross-references which were formerly part of the BibleWorks software which has been discontinued.

Not shown on screen. Its text is the description of the **BibleWorks™ list** shown by the information button. Choose the list in **External Refs**.

###### UBS

Radio · Full · `r_xrSource_ubs`  
Also: Source of cross-references: UBS GNT92 list · Needs: “Use External List of Cross-References”

> This list contains New Testament and Old Testament references (NO Deuterocanonical  references). Short Bible Reference System, edited by Robert G. Bratcher, (c) 1961 United Bible Societies. This list was used in GNT92. Organizations that have a Paratext license may use this list in their publication without attribution or notifying UBS. All other rights to use this list are reserved.
>
> Use the (DC) list if Deutero Canonical references are needed.

Not shown on screen. Its text is the description of the **UBS GNT92** lists shown by the information button. Choose the list in **External Refs**.

###### Custom

Radio · Full · `r_xrSource_custom`  
Also: Source of cross-references: Custom .xrf list · Needs: “Use External List of Cross-References”

> You can select a specially-curated list of cross-references. For example, it is possible to extract cross-references from another project (in the .xrf file format) to be included here. There is also an .xre format (extended .xrf) and an .xml format which can be used as external cross-references. These formats are explained in the documentation. See the PTXprint documentation (xrefs.md).

Not shown on screen. Its text is the description of a custom list shown by the information button. To use your own list, choose **Select a Custom list...** in **External Refs** and click **Select...**.

###### Hover here to read about the selected cross-reference list.

Button · Full · `btn_infoXrefSource`  
Needs: “Use External List of Cross-References”

> Hover here to read about the selected cross-reference list.

The description gives the size of the list chosen in **External Refs**, where it comes from and any copyright notes.

##### Source for References › Strong's References

###### Show Numbers in the Text

Checkbox, off · Full · `c_strongsShowInText` · cfg `strongsndx/showintext`  
Also: Show Strong's numbers in the text · Needs: “Use External List of Cross-References”

> If the project's Biblical Terms list includes renderings, then it is possible to show Strong's numbers in the text itself, which should make it easier to look up the appropriate cross-references for a word in a Study Bible.
>
> Note that this option is disabled by default as it can clutter the scripture text and will also slow down the production of the PDF.

Uses your project's Biblical Terms renderings. Only for the Strong's lists. It makes the PDF much slower to produce. PTXprint keeps each number on the same line as the word after it, so a number is never left alone at the end of a line. The same text and settings always give the same numbers in the same places, so two PDFs made from the same text can be compared.

###### Show Numbers in Cross-References

Checkbox, on · Full · `c_strongsShowNums` · cfg `strongsndx/shownums`  
Also: Show Strong's numbers in cross-references · Needs: “Use External List of Cross-References”

> If you are generating a localized Strong's index, then it is highly recommended to include the Strong's numbers in the list of cross-references in the text.
>
> But if you only want to show the references without any Strong's numbers, then uncheck this option for a more compact list.

Shows the number in front of each group of references.

###### Generate Index...

Button · Full · `btn_strongsGenerate`  
Also: Generate Index (based on Strong's numbers) · Needs: “Use External List of Cross-References”

> For Strong's Cross References to be most useful, it is recommended to include an Index at the end of the publication. Click this button to set various options to be used to generate the index.

Only available for the Strong's lists. See "Generate Strong's Index dialog" above.

###### Show All Occurrences

Checkbox, off · Full · `c_strongsShowAll` · cfg `strongsndx/showall`  
Also: Show Strong's numbers on every occurrence of a word · Needs: “Show Numbers in the Text”, “Use External List of Cross-References”

> If a particular word occurs more than once in the given verse, each occurrence will be tagged with the Strong's number. If a word matches more than one Strong's number then both will be displayed.
>
> This may be rather confusing for the reader, but could be helpful for a consultant to easily identify overlap issues with the project's Biblical terms renderings.

Meant for a consultant who checks the renderings, rather than for readers.

###### \xts

Link · Full · `lb_style_xts`  
Needs: “Use External List of Cross-References”

> Click to edit the Strong's 4 digit cell number properties on the Styles tab.

The `\xts` style controls how the Strong's numbers look in the cross-references.

##### Source for References › Column Cross-References

###### Column Width (pts) – Column width of column-based cross-references

Number · Full · `s_centreColWidth` · cfg `notes/xrcentrecolwidth`  
Values: 30–150 (default 60) · Needs: “Column Cross-References”

> This sets the width of the centre column in points. Note that 72pts is 1 inch, and increasing the size here will decrease the amount of space available for the 2 columns of scripture text.
>
> Consider using a larger page size if you want to use Centre Column xRefs.
>
> If this centre column isn't wide enough to fit the references, then you should also consider reducing the size of the \x font (to approx 6pt).

If the references do not fit, make the `\x` font smaller rather than the column much wider.

###### Gutter Width (pts) – Gutter width of column-based cross-references

Number · Full · `s_xrGutterWidth` · cfg `notes/xrguttermargin`  
Values: 0.1–20 (default 2) · Needs: “Column Cross-References”

> This sets the space between the main body text and the column of cross-references.

In pt.

###### Side of page – Position of column-based cross-references

Drop-down · Full · `fcb_colXRside` · cfg `notes/xrcolside`  
Choices: Left | Right | Inner | Outer · Needs: “Column Cross-References” · Greyed out by: “Two Column Layout”

> Select where the column of cross-references should be located on the page. Note that the 2-column layout insists on the cross-references being positioned between the columns of text.

For a one-column layout only. **Inner** is near the spine, **Outer** is away from it.

###### Vertical Rule(s) Between Columns

Checkbox, on · Full · `c_xrColumnRule` · cfg `notes/xrcolrule`  
Also: Include a vertical rule between columns · Needs: “Column Cross-References”

> Check this option to include a vertical line separating the text and cross-references.

Draws a thin vertical line.

###### Fill Upward From Bottom of Column

Checkbox, off · Full · `c_xrColumnBottom` · cfg `notes/xrcolbottom`  
Also: Fill cross-references upward from bottom of column · Needs: “Column Cross-References”

> If there are only a small number of cross-references, it may appear better for them to be placed nearer the end (or bottom) of the page. Check this option if you prefer the references to fill the column upward from the end of the page.

Places the references at the bottom of the column instead of the top.

###### Side Align Notes

Checkbox, off · Full · `c_xrSideAlign` · cfg `notes/xrcolalign`  
Also: Align notes to the edge of the main text · Needs: “Column Cross-References”

> For side column notes, should the text of the notes align to the edge of the main text?

When not ticked, the text aligns to the edge of the column.

##### Rule and Space Settings

###### Show Cross-Reference Rule

Checkbox, on · Regular+ · `c_xrefrule` · cfg `notes/ifxrefrule`

> This is the horizontal rule separating the body text from the cross-reference area. (Used only when footnotes or cross-references are placed at the End of Book. Otherwise the Footnote rule settings apply.)

To hide the rule above the bottom-of-page notes, untick **Show Footnote Rule** on the **Footnotes** sub-tab.

###### Space Above Rule (pt) – Space above cross-reference rule

Number · Regular+ · `s_xrAboveSpace` · cfg `notes/abovexrefspace`  
Values: -50–50

> The vertical space between the main text body and the cross-reference rule. (Used only when footnotes or cross-references are placed at the End of Book. Otherwise the Footnote rule settings apply.)
>
> The vertical space between the body text and the area containing cross-references.
>
> If the Cross-Reference Rule is not shown, the vertical space will still be calculated as the Space Above plus the Space Below (the imaginary) Rule.

In other cases, change **Space Above Rule** on the **Footnotes** sub-tab.

###### Space Below Rule (pt) – Space below cross-reference rule

Number · Regular+ · `s_xrBelowSpace` · cfg `notes/belowxrefrulespace`  
Values: -50–50 · Needs: “Show Cross-Reference Rule”

> This is the vertical space/gap (pts) between the rule and the cross-references. (Used only when footnotes or cross-references are placed at the End of Book. Otherwise the Footnote rule settings apply.)

Used only at **End of Book**.

###### Rule Positioning and Parameters – Cross-reference rule: Indent

Number · Full · `s_xrIndent` · cfg `notes/xrruleindent`  
Needs: “Show Cross-Reference Rule”

> Distance (mm) to move the rule in from the side chosen in Horizontal Position. (Used only when footnotes or cross-references are placed at the End of Book. Otherwise the Footnote rule settings apply.)

Works like **Indent** for the footnote rule. Used only at **End of Book**.

###### Rule Positioning and Parameters – Cross-reference rule: Length

Number · Full · `s_xrLength` · cfg `notes/xrrulelength`  
Values: 20–100 · Needs: “Show Cross-Reference Rule”

> The length of the rule as a percentage of the column/page width. (Used only when footnotes or cross-references are placed at the End of Book. Otherwise the Footnote rule settings apply.)

Works like **Length** for the footnote rule. Used only at **End of Book**.

###### Rule Positioning and Parameters – Cross-reference rule: Thickness

Number · Full · `s_xrThick` · cfg `notes/xrrulethick`  
Values: 0.1–2 · Needs: “Show Cross-Reference Rule”

> The thickness of the rule. (Used only when footnotes or cross-references are placed at the End of Book. Otherwise the Footnote rule settings apply.)

In pt. Used only at **End of Book**.

###### Rule Positioning and Parameters – Cross-reference rule: Horizontal position

Drop-down · Full · `fcb_xrHorizPosn` · cfg `notes/xrruleposn`  
Choices: Left | Right | Inner | Outer | Center · Needs: “Show Cross-Reference Rule”

> Which side of the column the rule is aligned to:  
> Left, Right, Center, Inner (spine side) or Outer. Inner and Outer swap sides on odd and even pages. This only matters when the Length is less than 100%. (Used only when footnotes or cross-references are placed at the End of Book. Otherwise the Footnote rule settings apply.)
>
> These settings control the rule (horizontal line) above the notes: its indent (mm), its length (% of the column width), its thickness (pt) and which side of the column it is aligned to.

Positions a cross-reference rule that is shorter than 100%. Used only at **End of Book**.

#### Study Notes + Questions

##### Extended Footnotes (\ef)

Checkbox, off · Full · `c_extendedFnotes` · cfg `studynotes/includextfn`  
Also: Use extended/study footnotes

> Extended Footnotes are the primary means for displaying study notes. These are similar to ordinary footnotes but appear as a 2-column block at the end of each page.

When it is not ticked, PTXprint removes all `\ef` notes from the text before making the PDF. Ticking it shows the layout and rule settings for study notes.

##### Sidebars (\esb ... \esbe)

Checkbox, off · Regular+ · `c_sidebars` · cfg `studynotes/includesidebar`  
Also: Include study note sidebars (\esb)

> Sidebars (\esb ... \esbe) are used to contain larger blocks of topic-specific information.

When it is not ticked, PTXprint removes them. Their appearance is set on the **Styles** tab.

##### Include Transcelerator Questions

Checkbox, off · Basic+ · `c_txlQuestionsInclude` · cfg `studynotes/txlinclquestions`  
Also: Include (Transcelerator) Checking Questions

> Use this option to include questions which have been created with SIL's Transcelerator tool for the purpose of comprehension testing.
>
> These will be displayed at the bottom of the page in the area normally used for Study Notes.
>
> Note that this option is only made available if the Transcelerator plugin's data folder for the project can be located.

Each question is printed near the verse it asks about. Ticking it shows the question settings and an example.

##### Extended Footnotes (\ef)

###### Gutter Width (mm) – Gutter width between columns of extended notes

Number · Full · `s_ef_colgutterfactor` · cfg `studynotes/colgutterfactor`  
Values: 1–40 · Needs: “Extended Footnotes (\ef)” · Hidden until: “Extended Footnotes (\ef)”

> This is the space between the text of the two columns (measured in millimeters).
>
> This is the space (mm) between the text of the two columns.

A larger value makes the notes easier to read but uses more space.

###### Unbalanced Lines (max) – Allow N unbalanced lines in extended notes

Number · Full · `s_ef_bottomRag`  
Needs: “Extended Footnotes (\ef)” · Hidden until: “Extended Footnotes (\ef)”

> PTXprint will attempt to balance the number of lines in each column of the extended notes. Sometimes this results in wasted empty space. Increasing this number (recommended range 1-4) will allow up to that many unbalanced lines in the extended notes area.
>
> By default (when this is set to 0) PTXprint will balance the number of lines used in each column. Sometimes this results in large empty spaces at the end of a page.
>
> Increasing this number (recommended range 1-4) will allow up to that many unbalanced lines on the page. Note that you can still stretch/shrink paragraphs using AdjLists to refine the output by manually balancing pages.

This setting is always greyed out in this version, so you cannot change it.

###### Vertical Space Between Notes – Vertical space between extended/study notes

Number · Full · `s_ef_internote` · cfg `studynotes/internote`  
Values: -20–20 · Needs: “Extended Footnotes (\ef)” · Hidden until: “Extended Footnotes (\ef)”

> This setting (pts) lets you adjust the vertical space between extended footnotes. Usually there is no space between them.

A small value such as 1 or 2 can make separate notes easier to see.

###### Vertical Rule in Gutter

Checkbox, off · Full · `c_ef_verticalrule` · cfg `studynotes/ifverticalrule`  
Also: Vertical rule in study notes area gutter · Needs: “Extended Footnotes (\ef)” · Hidden until: “Extended Footnotes (\ef)”

> Check this option to include a center line between the two columns.

When ticked, **Adjust Top (pt)** becomes available.

###### Adjust Top (pt)

Number · Full · `s_ef_colgutteroffset` · cfg `studynotes/colgutteroffset`  
Values: -50–50 · Needs: “Vertical Rule in Gutter”, “Extended Footnotes (\ef)” · Hidden until: “Extended Footnotes (\ef)”

> This setting raises (using a negative value) or lowers (using a positive value) the starting point of the vertical rule between columns (pt).
>
> This setting raises (using a negative value) or lowers (using a positive value) the starting point of the vertical rule between columns.

Moves only the top end of the line.

###### Show Note Callers

Checkbox, off · Full · `c_ef_showCallers` · cfg `studynotes/showcallers`  
Also: Show study note callers in notes area · Needs: “Extended Footnotes (\ef)” · Hidden until: “Extended Footnotes (\ef)”

> Show callers for extended (study) notes, both in the text and in the notes area. A caller alerts the reader that there is further information (in this case an extended footnote) at the end of the page. As a Study Bible has many such notes, this option is normally turned off for extended footnotes. Note that currently only a,b,c...x,y,z callers are possible for this option.

When not ticked, PTXprint removes the callers of all study notes, even if the text asks for them.

##### Extended Footnotes (\ef) › Rule and Space Settings

###### Rule Positioning and Parameters – Study note rule: Indent

Number · Full · `s_snIndent` · cfg `notes/snruleindent`  
Hidden until: “Extended Footnotes (\ef)”

> Distance (mm) to move the rule in from the side chosen in Horizontal Position.

In mm.

###### Rule Positioning and Parameters – Study note rule: Length

Number · Full · `s_snLength` · cfg `notes/snrulelength`  
Values: 20–100 (default 100) · Hidden until: “Extended Footnotes (\ef)”

> The length of the rule as a percentage of the column/page width.

100 is a full-width line.

###### Rule Positioning and Parameters – Study note rule: Thickness

Number · Full · `s_snThick` · cfg `notes/snrulethick`  
Values: 0.1–2 (default 0.5) · Hidden until: “Extended Footnotes (\ef)”

> The thickness of the rule.

In pt.

###### Rule Positioning and Parameters – Study note rule: Horizontal position

Drop-down · Full · `fcb_snHorizPosn` · cfg `notes/snruleposn`  
Choices: Left | Right | Inner | Outer | Center · Hidden until: “Extended Footnotes (\ef)”

> Which side of the column the rule is aligned to:  
> Left, Right, Center, Inner (spine side) or Outer. Inner and Outer swap sides on odd and even pages. This only matters when the Length is less than 100%.
>
> These settings control the rule (horizontal line) above the notes: its indent (mm), its length (% of the column width), its thickness (pt) and which side of the column it is aligned to.

Positions a study-note rule that is shorter than 100%.

###### Show Study Note Rule

Checkbox, on · Full · `c_studynoterule` · cfg `notes/ifstudynoterule`  
Hidden until: “Extended Footnotes (\ef)”

> This is the horizontal rule separating the body text from the study notes area.

It sits between the ordinary notes (or the text) and the study notes area.

###### Space Above Rule (pt) – Space above study note rule

Number · Full · `s_snAboveSpace` · cfg `notes/abovestudyspace`  
Values: -50–50 (default 6) · Hidden until: “Extended Footnotes (\ef)”

> The vertical space between the main text body and the study note rule.
>
> Note: if you make this value less than the descenders of the last lines of text, then the study notes will push down into the footer area. If you see this happening, increase this value to trigger an earlier page break to solve the problem.
>
> The vertical space between the body text and the area containing study notes.
>
> If the Study Note Rule is not shown, the vertical space will still be calculated as the Space Above plus the Space Below (the imaginary) Rule.

In pt.

###### Space Below Rule (pt) – Space below study note rule

Number · Full · `s_snBelowSpace` · cfg `notes/belowstudyrulespace`  
Values: -50–50 (default 2) · Hidden until: “Extended Footnotes (\ef)”

> This is the vertical space/gap (pts) between the rule and the study notes.

In pt.

##### Include Transcelerator Questions

###### Language Code

Text box · Basic+ · `t_txlQuestionsLang` · cfg `studynotes/txllangtag`  
Needs: “Include Transcelerator Questions” · Hidden until: “Include Transcelerator Questions”

> Enter the language code for the questions to be included. Usually this will be a 3-letter Ethnologue code (but other language tags such as en-US, fr, es are also acceptable).

PTXprint fills this in from the Paratext project's language code when it is empty. It must match the language the questions were translated into in Transcelerator. Questions with no translation in this language are not printed.

###### Show Overview Questions

Checkbox, off · Basic+ · `c_txlQuestionsOverview` · cfg `studynotes/txloverview`  
Also: Transcelerator: Show overview questions · Needs: “Include Transcelerator Questions” · Hidden until: “Include Transcelerator Questions”

> Overview questions are designed to test the general understanding of the passage.

Overview questions ask about a whole passage rather than one verse.

###### Number the Questions

Checkbox, on · Basic+ · `c_txlQuestionsNumbered` · cfg `studynotes/txlnumbered`  
Also: Transcelerator: Number the questions · Needs: “Include Transcelerator Questions” · Hidden until: “Include Transcelerator Questions”

> This option enables the questions to be numbered sequentially for each book.

This makes it easy to talk about a question during testing.

###### Include Chapter:Verse References

Checkbox, off · Basic+ · `c_txlQuestionsRefs` · cfg `studynotes/txlshowrefs`  
Also: Transcelerator: Include ch:vs references · Needs: “Include Transcelerator Questions” · Hidden until: “Include Transcelerator Questions”

> This option enables the questions to include the chapter:verse numbers.
>
> If the questions are also being numbered then the reference will be shown in parentheses (ch:vs).

For example `3:25`, or `13. (3:25)` when the questions are numbered.

###### \ef

Link · Full · `lb_style_ef`  
Needs: “Include Transcelerator Questions” · Hidden until: “Include Transcelerator Questions”

> Click to edit the Extended Footnote properties on the Styles tab.
>
> The line spacing factor will modify the space between the questions.

The `\ef` style controls how study notes and Transcelerator questions look.

##### Filter Categories › Filter Categories

###### tv_sbCatEdit

Table · Full · `tv_sbCatEdit`  
Needs: “Filter Categories”

The categories found in the project's study notes and sidebars, with a tick box for **Extended Footnote (\ef)** and one for **Sidebar (\esb)**. In this version, PTXprint does not save this list and does not use it when it makes the PDF.

###### Add

Button · Full · `b_sb_addcat`  
Also: Add sidebar category to filter · Needs: “Filter Categories”

> Add a new Category.

Type its name in the box that opens.

###### Del

Button · Full · `b_sb_delcat`  
Also: Delete sidebar category from filter · Needs: “Filter Categories”

> Delete the currently selected Category.

Removes the selected category.

###### ↺

Button · Full · `btn_sb_rescanCats`  
Also: Rescan categories to filter sidebars · Needs: “Filter Categories”

> Clicking this button will rescan the project to add any Categories missing from this list.

Searches all books for `\cat ... \cat*` and fills the list again. The list is also filled when you first tick **Filter Categories**.

##### Filter Categories

###### Filter Categories

Checkbox, off · Full · `c_filterCats` · cfg `studynotes/filtercats`  
Also: Filter study note sidebars

> Use this option to restrict certain categories of extended study notes and sidebars from being displayed.

Shows the category list. If the list is empty, PTXprint searches the project for categories. In this version, the filter does not change the PDF.
