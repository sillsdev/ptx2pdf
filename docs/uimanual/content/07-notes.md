## What this tab is for

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

## Footnotes

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

## Cross-References

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

## Study Notes + Questions

This sub-tab is for study Bibles and for comprehension testing.

### Extended Footnotes (\ef)

Tick **Extended Footnotes (\ef)** (only in the **Full** view) to print the `\ef ... \ef*` study notes from the text. They appear in their own two-column area at the bottom of the page, under the ordinary notes. If this box is not ticked, PTXprint removes all `\ef` notes before it makes the PDF. When it is ticked, the area below shows settings for the gutter, the vertical rule between the columns, callers, and the rule above the study notes.

**Sidebars (\esb ... \esbe)** prints the boxed sidebars of a study Bible. If it is not ticked, PTXprint removes them. The look of sidebars is set on the **Styles** tab and in the sidebar settings.

### Include Transcelerator Questions

Transcelerator is a Paratext plugin from SIL for making comprehension-checking questions. If your project has Transcelerator data, PTXprint can print the translated questions at the bottom of each page, in the same area as study notes. Each question appears near the verse it is about. This is useful for comprehension-testing printouts. The **Example Questions** text shows how your choices will look. If there is no Transcelerator data for the project, the checkbox is greyed out.

### Filter Categories

In a study Bible, notes and sidebars can have a category, for example `\cat History\cat*`. **Filter Categories** (only in the **Full** view) shows a list of the categories in the project, with a tick box for extended notes and for sidebars. In this version, PTXprint does not save this list with the configuration, and it does not use it when it makes the PDF.

## Generate Strong's Index dialog

To open this dialog, go to **Notes+Refs** › **Cross-References** and tick **Use External List of Cross-References**. Choose a **Strong's list** in **External Refs**, and then click **Generate Index...**.

The dialog makes a new book (in USFM, the Paratext file format) that lists each Strong's number and information about the word. Readers use it to look up a number they see in the cross-references. You choose:

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

## Common problems

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

## Control notes

### @btn_strong_ok
Makes the index book and closes the dialog. PTXprint also changes the book selection to multiple books. Any text already in that book is replaced without another warning.

### @btn_strong_cancel
Closes the dialog without making an index. Your choices in the dialog are kept.

### @c_strongsHeb
Lists the Hebrew (Old Testament) Strong's numbers. Untick it if your publication is only the New Testament.

### @c_strongsGrk
Lists the Greek (New Testament) Strong's numbers. Untick it if your publication is only the Old Testament.

### @lb_style_li+strong-s
The `\li` style is used for each entry in the Strong's index. Change it to adjust the font size or indent of the entries.

### @c_strongsNdx
Comes after the main lists. It lists your project's renderings in alphabetical order, each with its Strong's numbers, sorted with the Paratext project's sorting rules. It can only be made when the project has Biblical Terms renderings.

### @c_strongsSrcLg
Your font must contain Hebrew and Greek letters, or the words will not show correctly. The `\wh` and `\wg` styles control how these words look.

### @c_strongsTranslit
The `\wl` style controls how it looks.

### @c_strongsRenderings
Uses the Biblical Terms renderings in Paratext. This is usually the most useful part of each entry. If a word has no rendering, PTXprint uses the fallback settings below.

### @c_strongsKeyVref
The `\xt` style controls how it looks.

### @c_strongsDefn
The definition is in English and comes after the renderings. It makes the index longer.

### @lb_style_wl+strong-s
Opens the `\wl` style (the transliteration) used in the Strong's index.

### @lb_style_xt+strong-s
Opens the `\xt` style (the key verse reference) used in the Strong's index.

### @lb_style_wh+strong-s
Opens the `\wh` style (Hebrew words) used in the Strong's index. You can choose a font with Hebrew letters there.

### @lb_style_wg+strong-s
Opens the `\wg` style (Greek words) used in the Strong's index. You can choose a font with Greek letters there.

### @c_strongsNoComments
Removes any text in round brackets ( ) from the renderings. Readers usually do not need these comments.

### @fcb_strongswildcards
A wildcard such as `bless*` matches several word forms. **Change to hyphen-** prints a hyphen instead of the `*`.

### @tv_strvarEdit
A table of the headings PTXprint uses in the index: the title of the book (`index_book_title`), the Hebrew and Greek section titles, and the title of the reverse index. Click a value to type the heading in your language.

### @fcb_strongsNdxBookId
**XXS** is the default. Choose a book you do not use for anything else, because its contents are replaced.

### @c_strongs2cols
Recommended, because the entries are short. Untick it for one column.

### @c_strongsOpenIndex
Use it to check the new index file.

### @s_strongRag
A value of 1 to 4 can avoid large empty spaces.

### @c_strongsNotes
Adds this description text to each index entry. It is saved with the configuration, like the other settings in this dialog.

### @fcb_strongsMajorLg
Used only when there is no rendering in your project or in the fallback project. Choose **None** to leave these words without a gloss.

### @fcb_strongsFallbackProj
For example, a project in a regional language. PTXprint uses its Biblical Terms renderings for words with no rendering in your project.

### @c_fnomitcaller
Untick it to print the note without the mark. This saves a little space.

### @c_fnpageresetcallers
This keeps the callers short when you use symbols.

### @c_fnautocallers
When not ticked, the caller box is greyed out and no automatic caller sequence is used. Together with **Override hidden/automatic Footnote caller settings**, unticking it removes the callers from all footnotes.

### @t_fncallers
When the sequence reaches the end, it starts again. Make sure your font has the symbols you type.

### @btn_resetFNcallers
PTXprint's own default sequence is `a,b,c,d,e,f,✶,☆,✦,✪,†,‡,§`.

### @c_fnOverride
Use this when the callers in the PDF do not follow your settings. PTXprint changes every footnote to `\f +` if **Show Callers** is ticked, or to `\f -` if it is not.

### @c_fneachnewline
This uses more space than run-on notes. When both this and **Start Each Cross-Reference on a New Line** are ticked, the horizontal spacing settings are greyed out, because they are only used for run-on notes.

### @lb_style_f
Change the font size, line spacing and other footnote properties there.

### @r_fnpos_endnote
Use this when there are few notes or when you want clean pages.

### @r_fnpos_column
The notes are set at the width of one column. If cross-references are at **End of Page**, they also move to **End of Column**.

### @r_fnpos_normal
The usual choice. If cross-references are at **End of Column**, they move to **End of Page** too.

### @c_includeFootnotes
Unticked, all footnotes are left out of the PDF. They stay in your Paratext project. Most footnote settings are then greyed out. Cross-references set to **Below Footnotes** or **Blend with Footnotes** move to another placement.

### @c_frVerseOnly
This saves space, because the chapter is usually clear from the page.

### @r_fnpos_margin
If you turn margin notes off, the footnotes go back to **End of Page**.

### @s_fnAboveSpace
Also increase it if the notes look too close to the text. Negative values are possible but rarely useful.

### @s_fnBelowSpace
PTXprint adds this space even when the rule is hidden.

### @c_footnoterule
This rule is also used above cross-references at the bottom of the page. Untick it for a cleaner look. The space above and below is kept.

### @s_fnIndent
Use 0 for no indent.

### @s_fnLength
Short rules of 20 to 40 are common in books.

### @s_fnThick
The value is in pt. Use a smaller value, like 0.3, for a lighter line.

### @fcb_fnHorizPosn
Positions a footnote rule that is shorter than 100%.

### @c_addColon
For example "*light*: Or *brightness*". Use it if your team does not type the colon in the notes.

### @c_keepBookWithRefs
For example, "John 3:16" stays on one line.

### @c_glossaryFootnotes
The entries come from the GLO book. This adds many footnotes.

### @s_notespacingmin
The maximum must be larger, so PTXprint adjusts **Maximum Space** when you change this.

### @s_notespacingmax
PTXprint stretches or shrinks the space to fill lines. A larger range gives PTXprint more freedom.

### @s_internote
The default is 3.5.

### @r_xrpos_endnote
Collected and printed at the end of each book.

### @r_xrpos_column
Needs a two-column layout. If footnotes are at **End of Page**, they also move to **End of Column**.

### @r_xrpos_normal
If footnotes are at **End of Column**, they move to **End of Page** too.

### @c_xreachnewline
This uses more space than run-on notes. When both this and **Start Each Footnote on a New Line** are ticked, the horizontal spacing settings on the **Footnotes** sub-tab are greyed out.

### @c_xrOverride
PTXprint uses `\x +` for every cross-reference if **Show Callers** is ticked, and `\x -` (no caller) if it is not.

### @c_xrautocallers
To show no cross-reference callers in the text at all, untick this and tick **Override…**.

### @t_xrcallers
Choose marks that are different from the footnote callers, so readers can tell the two kinds of notes apart.

### @btn_resetXRcallers
PTXprint's default sequence is `†,‡,§,∥,#`.

### @c_xromitcaller
Untick it to save a little space.

### @c_xrpageresetcallers
Works like **Reset Callers on Page** for footnotes.

### @lb_style_x
For column cross-references, a small size (about 6 pt) is often needed.

### @r_xrpos_below
**Vertical Space Between Footnotes and xRefs** sets the gap between the two blocks.

### @r_xrpos_blend
This saves space. PTXprint sets the `\x` style on the **Styles** tab so that it joins the footnotes.

### @r_xrpos_centre
With a two-column layout the column is between the text columns. With one column, choose the side in **Side of page**. Choosing this sets footnotes to **End of Column** and opens the **Source for References** area. Set the width and other settings in the **Column Cross-References** area.

### @c_useXrefList
The list can also be your own file. Choose it in **Source for References**. The added references have no caller in the text. When ticked, the **Cross-References** sub-tab name is highlighted.

### @c_extendedXrefs
When it is not ticked, PTXprint removes all `\ex ... \ex*` notes.

### @c_includeXrefs
This does not affect cross-references from an external list.

### @c_xoVerseOnly
This also applies to cross-references from external lists. For a bridged verse (two or more verses joined), the whole range is shown, for example `13-14`.

### @r_xrpos_margin
If you turn margin notes off, the cross-references go back to **End of Page**.

### @fcb_filterXrefs
* **Whole Bible** – keep all references.
* **Paratext Project** – only books that exist in the project.
* **This Publication** – only the books in the list of books to print (**Basic** tab, **What to Print** area).
* **New Testament** or **Old Testament** – only that part of the Bible.

### @fcb_xRefExtListSource
The **Strong's** lists group references by Hebrew and Greek word, and make the **Strong's References** settings available. **Select a Custom list...** makes the **Select...** button available. Larger lists need more space on the page and take longer to process. See **Source for References** above for each list.

### @btn_selectXrFile
Chooses your own cross-reference file. It starts in the Paratext `_Cross References` folder. PTXprint can read `.xrf` (the Paratext cross-reference format), `.xre` and `.xml` files. Only available when **External Refs** is **Select a Custom list...**. After you choose a file, hover over the button to see the file name.

### @r_xrSource_standard
Not shown on screen. Its text is the description of the **Standard list** shown by the information button. Choose the list in **External Refs**.

### @r_xrSource_strongs
Not shown on screen. Its text is the description of the **Strong's** lists shown by the information button. Choose the list in **External Refs**.

### @r_xrSource_tsk
Not shown on screen. Its text is the description of the **TSK list** shown by the information button. Choose the list in **External Refs**.

### @r_xrSource_works
Not shown on screen. Its text is the description of the **BibleWorks™ list** shown by the information button. Choose the list in **External Refs**.

### @r_xrSource_ubs
Not shown on screen. Its text is the description of the **UBS GNT92** lists shown by the information button. Choose the list in **External Refs**.

### @r_xrSource_custom
Not shown on screen. Its text is the description of a custom list shown by the information button. To use your own list, choose **Select a Custom list...** in **External Refs** and click **Select...**.

### @btn_infoXrefSource
The description gives the size of the list chosen in **External Refs**, where it comes from and any copyright notes.

### @c_strongsShowInText
Uses your project's Biblical Terms renderings. Only for the Strong's lists. It makes the PDF much slower to produce. PTXprint keeps each number on the same line as the word after it, so a number is never left alone at the end of a line. The same text and settings always give the same numbers in the same places, so two PDFs made from the same text can be compared.

### @c_strongsShowNums
Shows the number in front of each group of references.

### @btn_strongsGenerate
Only available for the Strong's lists. See "Generate Strong's Index dialog" above.

### @c_strongsShowAll
Meant for a consultant who checks the renderings, rather than for readers.

### @lb_style_xts
The `\xts` style controls how the Strong's numbers look in the cross-references.

### @s_centreColWidth
If the references do not fit, make the `\x` font smaller rather than the column much wider.

### @s_xrGutterWidth
In pt.

### @fcb_colXRside
For a one-column layout only. **Inner** is near the spine, **Outer** is away from it.

### @c_xrColumnRule
Draws a thin vertical line.

### @c_xrColumnBottom
Places the references at the bottom of the column instead of the top.

### @c_xrSideAlign
When not ticked, the text aligns to the edge of the column.

### @c_xrefrule
To hide the rule above the bottom-of-page notes, untick **Show Footnote Rule** on the **Footnotes** sub-tab.

### @s_xrAboveSpace
In other cases, change **Space Above Rule** on the **Footnotes** sub-tab.

### @s_xrBelowSpace
Used only at **End of Book**.

### @s_xrIndent
Works like **Indent** for the footnote rule. Used only at **End of Book**.

### @s_xrLength
Works like **Length** for the footnote rule. Used only at **End of Book**.

### @s_xrThick
In pt. Used only at **End of Book**.

### @fcb_xrHorizPosn
Positions a cross-reference rule that is shorter than 100%. Used only at **End of Book**.

### @s_ef_colgutterfactor
A larger value makes the notes easier to read but uses more space.

### @s_ef_bottomRag
This setting is always greyed out in this version, so you cannot change it.

### @s_ef_internote
A small value such as 1 or 2 can make separate notes easier to see.

### @c_ef_verticalrule
When ticked, **Adjust Top (pt)** becomes available.

### @s_ef_colgutteroffset
Moves only the top end of the line.

### @c_ef_showCallers
When not ticked, PTXprint removes the callers of all study notes, even if the text asks for them.

### @s_snIndent
In mm.

### @s_snLength
100 is a full-width line.

### @s_snThick
In pt.

### @fcb_snHorizPosn
Positions a study-note rule that is shorter than 100%.

### @c_studynoterule
It sits between the ordinary notes (or the text) and the study notes area.

### @s_snAboveSpace
In pt.

### @s_snBelowSpace
In pt.

### @c_extendedFnotes
When it is not ticked, PTXprint removes all `\ef` notes from the text before making the PDF. Ticking it shows the layout and rule settings for study notes.

### @c_sidebars
When it is not ticked, PTXprint removes them. Their appearance is set on the **Styles** tab.

### @c_txlQuestionsInclude
Each question is printed near the verse it asks about. Ticking it shows the question settings and an example.

### @t_txlQuestionsLang
PTXprint fills this in from the Paratext project's language code when it is empty. It must match the language the questions were translated into in Transcelerator. Questions with no translation in this language are not printed.

### @c_txlQuestionsOverview
Overview questions ask about a whole passage rather than one verse.

### @c_txlQuestionsNumbered
This makes it easy to talk about a question during testing.

### @c_txlQuestionsRefs
For example `3:25`, or `13. (3:25)` when the questions are numbered.

### @lb_style_ef
The `\ef` style controls how study notes and Transcelerator questions look.

### @tv_sbCatEdit
The categories found in the project's study notes and sidebars, with a tick box for **Extended Footnote (\ef)** and one for **Sidebar (\esb)**. In this version, PTXprint does not save this list and does not use it when it makes the PDF.

### @b_sb_addcat
Type its name in the box that opens.

### @b_sb_delcat
Removes the selected category.

### @btn_sb_rescanCats
Searches all books for `\cat ... \cat*` and fills the list again. The list is also filled when you first tick **Filter Categories**.

### @c_filterCats
Shows the category list. If the list is empty, PTXprint searches the project for categories. In this version, the filter does not change the PDF.
