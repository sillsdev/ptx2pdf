# Body tab

## What this tab is for

The **Body** tab controls *what* is printed from each book, and some of *how* the main text looks.
Come here when you want to:

* leave out parts of the text, for example the book introductions, section headings or empty verses;
* hide or show chapter numbers and verse numbers;
* put verse numbers in a column next to the text (marginal verses);
* change how glossary words are marked in the text;
* start chapters on a new page, or print some books in one column and others in two.

Some settings on this tab **remove text** before typesetting. Others only **change the
appearance** and keep all the text. This difference matters. For example, if you hide verse
numbers, the running header can still show chapter and verse references, because the verses are
still there. If you untick **Headings**, the section headings are taken out completely.
Each section below says which kind of setting it is.

The tab has three areas: **Beginning and Ending Material**, **Include Scripture Text** and
**Other Features**. Some settings are only shown in the **Default** or **Full** view.

## Beginning and Ending Material

These settings deal with the material at the start of each book (the introduction) and with the
glossary.

* **Book Introductions** and **Introductory Outlines** decide whether the introduction is printed.
  They **remove content**: if you untick them, PTXprint takes these paragraphs out of the text
  before it typesets it. Only the material before the first chapter is affected.
  * **Book Introductions** covers the introduction paragraphs and headings (markers such as
    `\is`, `\ip`, `\im`, `\ili`).
  * **Introductory Outlines** covers only the outline (markers `\io1`–`\io4`, `\iot`, `\ior`).
  * You can print the introduction without the outline, or the outline without the introduction.
* **Right-align \ior With Tabbed Leaders** only changes the appearance of the outline. It pushes the
  reference at the end of each outline line to the right edge and fills the gap with dots, like a
  table of contents. (Default and Full views.) It does nothing in non-Scripture books.
* **Filter Glossary to Only Include Entries Used in the Text** **removes content** from the
  glossary book (GLO). It only matters when GLO is one of the books you print.
* **Start 1st Chapter on a New Page** and **Start All Other Chapters on a New Page** add page breaks.
  They do not remove text.

## Include Scripture Text

The checkbox **Include Scripture Text** is the title of this area. Leave it ticked. If you untick
it, PTXprint **removes** everything from the first chapter onwards in every book, so only the
introductions (and other material before chapter 1) are printed. This is useful when you want to
check the introductions only. All the other settings in this area are greyed out while it is unticked.

### What is included

* **Headings** – section headings (`\s`, `\s1`, `\s2` …). Unticking it **removes** all section
  headings and also all parallel passage references.
* **Parallel Passage Refs** – the references printed under some section headings (`\r`), for
  example "(Mark 1:1-8)". Unticking it **removes** them. It is greyed out when **Headings** is unticked.
* **Hide Empty Verses** **removes** verses (and whole chapters) that have no text yet. Use it to print
  a draft where only part of the book is translated. Tick **Show '...'** as well if you want "..." to
  show the reader where text was left out.
* **Chapter numbers** and **Verse Numbers** only change the **appearance**. When unticked, the
  numbers are not printed, but the chapters and verses are still known to PTXprint. So headers,
  footnotes and cross-references still work.

### How the text looks

* **Justify Paragraphs** – ticked gives straight left and right edges. Unticked gives a ragged
  right edge (a ragged left edge for right-to-left scripts).
* **Indent First Paragraph** – when unticked, the first paragraph after a section heading starts at
  the margin, with no indent.
* **Hide First Verse Number** – hides the "1" of verse 1 when it comes straight after a large
  (dropped) chapter number, or when marginal verses are used.
* **Hanging Poetry Verse Numbers** – in poetry lines, the verse number is placed to the left of the
  line, so all the poetry lines stay lined up.
* **Prevent Verse Widow Words**, **Prevent Orphan Words** and **Keep Repeated Words Together**
  join some words together with a space that cannot break. This changes where lines break. It does
  not change the words.

### Marginal verses

Tick **Marginal Verses** to print the verse numbers in a narrow column beside the text, instead
of inside the text. Then choose the side in **Position on Page** and the width of that column in
**Col Width (pts)**. (A pt, or point, is about 0.35 mm.) While **Marginal Verses** is ticked,
**Hanging Poetry Verse Numbers** is turned off and greyed out.

### Style links

The small links **\s**, **\r**, **\c** and **\v** open the **Styles** tab at that marker. Use them to
change the font, size or spacing of section headings, parallel references, chapter numbers or
verse numbers.

## Other Features

This area is for special treatment of some books, and for glossary words.

* **Use Special Features for These Books** (Full view only) prints a text label before each chapter
  number, for example "Psalm 1" as a heading, instead of a large dropped number. This is common
  for Psalms. Type the label in **Chapter Label** and the book codes in the list box beside the
  checkbox. **Optimize Layout for Poetry Books** belongs to this group.
* **Use One/Two Column Layout for These Books** (Full view only) lets some books use a different
  number of columns from the rest of the publication. The label changes: it says "Use One Column"
  when the publication is two columns (set on the **Layout** tab), and "Use Two Column" when it is
  one column.
* **Glossary Word Appearance** decides how words marked as glossary words (`\w ...\w*`) look in the text.
* **Show Chapter Numbers In: Single Chapter Books** and **Non-Scripture Books** decide whether a
  chapter number is printed in books with only one chapter (such as Jude), and in peripheral
  books (such as the glossary). For non-Scripture books, unticking **removes** the chapter markers.
* The links **\w** and **\zglm** open the **Styles** tab for the glossary word style and for the
  glossary bracket characters.

## Common tasks

### How do I print only the book introductions?

1. On the **Body** tab, untick **Include Scripture Text**.
2. Make sure **Book Introductions** (and **Introductory Outlines**, if you want them) are ticked.
3. Click **Print (Make PDF)**.
4. Remember to tick **Include Scripture Text** again afterwards.

### How do I print a draft that has many untranslated verses?

1. On the **Body** tab, in the **Include Scripture Text** area, tick **Hide Empty Verses**.
2. If readers should see where text is missing, tick **Show '...'**.
3. Print again.

### How do I remove all section headings?

1. On the **Body** tab, untick **Headings**.
2. The parallel passage references are removed too. You cannot keep the parallel references without
   the headings.

### How do I show verse number 1?

1. On the **Body** tab, untick **Hide First Verse Number**.
   (This is only shown in the **Default** and **Full** views.)

### How do I put the verse numbers in the margin?

1. On the **Body** tab, tick **Marginal Verses**.
2. In **Position on Page**, choose **Left**, **Right**, **Inner** (next to the spine) or **Outer**
   (next to the page edge).
3. In **Col Width (pts)**, give enough width for the longest verse number, for example 12–16.
4. Print and check that numbers like "176" fit.

### How do I print "Psalm 1", "Psalm 2" … instead of large chapter numbers in Psalms?

1. Switch to the **Full** view.
2. On the **Body** tab, in **Other Features**, tick **Use Special Features for These Books**.
3. In the list box, type `PSA`. (If you leave the list empty, the label is used in **all** books.)
4. In **Chapter Label**, type the word for "Psalm" in your language.
5. Print again.

### How do I print the glossary book in one column when the rest is two columns?

1. Switch to the **Full** view.
2. On the **Body** tab, tick **Use One Column Layout for These Books**.
3. In the box beside it, type `GLO`. Separate several books with spaces, for example `GLO PSA`.

### How do I change how glossary words look in the text?

1. On the **Body** tab, in **Other Features**, open **Glossary Word Appearance**.
2. Choose a style, for example **format as bold** or **star \*before word**.
3. To use your own formatting, choose **\w ...\w\* char style** and then click the **\w** link to
   edit that style on the **Styles** tab.

## Common problems

**The parallel references disappeared.**
Cause: **Headings** was unticked. This also unticks and greys out **Parallel Passage Refs**.
Fix: tick **Headings** again, then tick **Parallel Passage Refs**.

**Verse 1 is still printed, although "Hide First Verse Number" is ticked.**
Cause: this setting only hides verse 1 after a dropped chapter number (or with marginal verses).
If chapters use a label (for example "Psalm 1") or chapter numbers are hidden, verse 1 can still
show. Fix: check the chapter number settings on this tab.

**"Hanging Poetry Verse Numbers" is greyed out.**
Cause: **Marginal Verses** is ticked. The two settings cannot be used together.

**"Optimize Layout for Poetry Books" has no effect.**
Cause: it only works for the books listed beside **Use Special Features for These Books**. If that
list is empty, nothing is optimized. Fix: type the book codes (for example `PSA PRO`) in the list.

**The chapter label appears in every book, not only Psalms.**
Cause: the book list beside **Use Special Features for These Books** is empty. An empty list means
"all books". Fix: type the book codes in the list.

**The glossary is still very long after ticking "Filter Glossary…".**
Cause: an entry is kept when its word is marked as a glossary word (`\w ...\w*`) in the books you
print, or when it is marked inside another kept glossary entry. Words that are not marked in the
text do not count. Fix: check the glossary markup in Paratext.

**Some lines have large gaps after ticking "Keep Repeated Words Together" or "Prevent Orphan Words".**
Cause: these settings stop the line from breaking between some words, so the line breaks elsewhere.
Fix: untick the setting, or fix the few bad lines by hand.

**"In Margin" (for headings) is greyed out.**
Cause: it needs **Margin Notes** turned on (on the **Layout** tab) and **Headings** ticked.

**The chapter numbers are missing in the glossary or other peripheral books.**
Cause: by default PTXprint removes chapter numbers from non-Scripture books. Fix: tick
**Non-Scripture Books** under **Show Chapter Numbers In**.

## Settings reference: Body tab

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Body tab › Beginning and Ending Material

#### Book Introductions

- **Where:** Body tab › Beginning and Ending Material
- **Type:** Checkbox (ticked by default)
- **Description:** Enable book introductions (\i..)
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Print the Book Introductions which appear at the beginning of each book. Includes markers like: \is \ip \im \ili etc.

**Explanation:**

Unticking this **removes** the introduction paragraphs and headings from the start of each book
before typesetting. The introductory outline is controlled separately by **Introductory Outlines**.
Only material before chapter 1 is removed. Untick it for a "Scripture text only" edition.

*(Internal ID: `c_bookIntro` · Config key: `document/bookintro`)*

#### Introductory Outlines

- **Where:** Body tab › Beginning and Ending Material
- **Type:** Checkbox (ticked by default)
- **Description:** Enable introductory outlines
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Print the Introductory Outlines which appear at the beginning of each book. Includes markers: \io1 ... \io4 \ior \iot

**Explanation:**

Unticking this **removes** only the outline part of the introduction (the `\io…` lines and the
outline title). The rest of the introduction stays, if **Book Introductions** is ticked. When you untick
it, **Right-align \ior With Tabbed Leaders** is also unticked and greyed out.

*(Internal ID: `c_introOutline` · Config key: `document/introoutline`)*

#### Right-align \ior With Tabbed Leaders

- **Where:** Body tab › Beginning and Ending Material
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable Right-aligned outlines with leaders
- **View level:** Default and Full views
- **Only available when:** “Introductory Outlines” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This will right-align and add leader tabs (. . . .) before the \ior numbers for a pretty Intro Outline Table.

**Explanation:**

This only changes the appearance of the introduction outline. The references at the end of each outline
line (`\ior`) move to the right edge, with a row of dots before them. It is not applied to
non-Scripture books. (Default and Full views.)

*(Internal ID: `c_prettyIntroOutline` · Config key: `snippets/fancyintro`)*

#### Filter Glossary to Only Include Entries Used in the Text

- **Where:** Body tab › Beginning and Ending Material
- **Type:** Checkbox (not ticked by default)
- **Description:** Filter glossary
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This option only has an effect if the Glossary (GLO) is one of the books being printed. If you have large glossary with many entries but are only printing a small selection of books, you may benefit from this option which will strip out any entries from the Glossary which are not marked-up in the text of the selected book(s) or chapter(s). i.e. only the \w marked-up\w* entries in the selected books/chapters will show in the glossary. Entries marked up inside a kept entry are also kept.

**Explanation:**

Use this when you print only a few books together with a large glossary. PTXprint keeps only the
glossary entries whose words are marked as glossary words (`\w ...\w*`) in the books you print,
and entries that kept entries point to. All other entries are **removed** from the printed glossary.
It only has an effect when the glossary book (GLO) is in the list of books to print.

*(Internal ID: `c_filterGlossary` · Config key: `document/filterglossary`)*

#### Start All Other Chapters on a New Page

- **Where:** Body tab › Beginning and Ending Material
- **Type:** Checkbox (not ticked by default)
- **Description:** Start every chapter on a new page
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Use this option to force a page break before every chapter. This is most commonly used for testing materials when each chapter needs to be printed and given to a different person.

**Explanation:**

Inserts a page break before every chapter except chapter 1. Use it for test or check copies,
where each chapter goes to a different reader. It can use a lot of paper. To also start chapter 1
on a new page, tick **Start 1st Chapter on a New Page**.

*(Internal ID: `c_pagebreakAllChs` · Config key: `document/pagebreakallchs`)*

#### Start 1st Chapter on a New Page

- **Where:** Body tab › Beginning and Ending Material
- **Type:** Checkbox (not ticked by default)
- **Description:** Start new page after introduction
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Use this option to automatically make a page break after a book's introduction section. The break will come right before the \c 1 marker.

**Explanation:**

Puts a page break between the book introduction and chapter 1, so the Scripture text starts on a
fresh page. Use it when the introductions are long, or for a cleaner look.

*(Internal ID: `c_ch1pagebreak` · Config key: `document/ch1pagebreak`)*

### Body tab › Include Scripture Text

#### Hide First Verse Number

- **Where:** Body tab › Include Scripture Text
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> It is quite common to hide the first verse number - especially when following a drop-cap chapter number. By default this option is on. If you prefer to see verse number 1, then uncheck this option.
>
> Note: verse 1 is only hidden when it follows a drop-cap chapter number, or when marginal verses are used.

**Explanation:**

When ticked, the verse number "1" is not printed when it comes straight after a large dropped chapter
number (and also when marginal verses are used). This is the usual style. The verse still exists, so references still work.
Untick it if your readers expect to see verse 1. (Default and Full views.)

*(Internal ID: `c_omitverseone` · Config key: `document/ifomitverseone`)*

#### Keep Repeated Words Together

- **Where:** Body tab › Include Scripture Text
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This option encourages re-duplicated words (i.e. those which are intentionally repeated) to come together on the same line by inserting a NoBreakSpace between them (only words of 3 or more letters). For example, "gama gama", or "kala kala" need to be stuck together (with a NBSP) in order to be read meaningfully. However, if there are many of these in the language, then it may create other unwanted typesetting issues. Use with care!

**Explanation:**

When a word of 3 or more letters is repeated (for example "kala kala"), PTXprint joins the two copies with a
space that cannot break. The two words then always stay on the same line. If your language has many repeated
words, this can cause loose lines. Check the result before you keep it. (Default and Full views.)

*(Internal ID: `c_glueredupwords` · Config key: `document/glueredupwords`)*

#### Indent First Paragraph

- **Where:** Body tab › Include Scripture Text
- **Type:** Checkbox (ticked by default)
- **Description:** Indent first paragraph after section heading
- **View level:** Default and Full views
- **Only available when:** “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If this option is unchecked, it will make the 1st  
> \p(aragraph) after a Section Heading appear as a \m(argin) paragraph with no indentation.

**Explanation:**

Ticked: the first paragraph after a section heading is indented like any other paragraph.
Unticked: that paragraph starts at the margin (no indent), as is common in many books. This only
changes the appearance. (Default and Full views.)

*(Internal ID: `c_firstParaIndent` · Config key: `document/firstparaindent`)*

#### Hanging Poetry Verse Numbers

- **Where:** Body tab › Include Scripture Text
- **Type:** Checkbox (ticked by default)
- **Description:** Use hanging verse number for poetry
- **View level:** Default and Full views
- **Only available when:** “Include Scripture Text” is selected
- **Greyed out when:** “Marginal Verses” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Verse numbers for Poetry elements all line up vertically on the margin, and Verse Bridges (3-4) also stack vertically.

**Explanation:**

Places verse numbers in poetry to the left of the poetry line, so the text of all poetry lines
stays lined up. Verse ranges such as "3-4" are stacked. It is turned off and greyed out when
**Marginal Verses** is ticked. (Default and Full views.)

*(Internal ID: `c_hangpoetry` · Config key: `document/hangpoetry`)*

#### Prevent Verse Widow Words

- **Where:** Body tab › Include Scripture Text
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This option prevents short words (of 3 characters or less) from occurring AFTER a verse begins near the end of a line.

**Explanation:**

When a verse starts near the end of a line with a short word (3 letters or less), this joins the verse
number and that word to the next word. The verse number then does not sit alone at the end of a line.
It changes line breaks only. (Default and Full views.)

*(Internal ID: `c_preventwidows` · Config key: `document/preventwidows`)*

#### Prevent Orphan Words

- **Where:** Body tab › Include Scripture Text
- **Type:** Checkbox (not ticked by default)
- **Description:** Prevent orphan words at end of paragraph or start of line.
- **View level:** Basic, Default and Full views
- **Only available when:** “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This option limits short words at the ends of paragraphs from occurring on a line on their own. It also prevents short words at the end of sentences from starting on a new line.
>
> The maximum orphan word length can be set in the 'Body Text' section of the Advanced > Other tab.

**Explanation:**

Joins the last short word of a paragraph (or poetry line) to the word before it, so that a single
short word is not left alone on the last line. It changes line breaks only. The maximum length of
a "short word" is set by **Maximum orphan word length** on the **Advanced** tab, **Other** tab, **Body Text** area (default 8 letters).

*(Internal ID: `c_preventorphans` · Config key: `document/preventorphans`)*

#### Justify Paragraphs

- **Where:** Body tab › Include Scripture Text
- **Type:** Checkbox (ticked by default)
- **View level:** Basic, Default and Full views
- **Only available when:** “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> By default the text will be fully justified. If you prefer a ragged edge, then uncheck this option.
>
> Note that a justification setting of "Justify" in a style is subject to this setting.

**Explanation:**

Ticked: lines are stretched so both edges of the column are straight (justified). Unticked: lines are
not stretched and one edge is ragged. Paragraph styles set to "Justify" on the **Styles** tab follow this
setting. Ragged text can be easier to read in narrow columns and in languages with long words.

*(Internal ID: `c_justify` · Config key: `paragraph/ifjustify`)*

#### Headings

- **Where:** Body tab › Include Scripture Text
- **Type:** Checkbox (ticked by default)
- **Description:** Enable section headings
- **View level:** Basic, Default and Full views
- **Only available when:** “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Uncheck this option if you don't want to print any Section Headings. Unchecking this option will ALSO uncheck the Parallel Passage Refs.

**Explanation:**

Unticking this **removes** all section headings (`\s`, `\s1`, `\s2` …) and all parallel passage
references (`\r`). When you untick it, **Parallel Passage Refs** is also unticked, and **In Margin**
is turned off. When you tick it again, **Parallel Passage Refs** is ticked again.

*(Internal ID: `c_sectionHeads` · Config key: `document/sectionheads`)*

#### \s

- **Where:** Body tab › Include Scripture Text
- **Type:** Link
- **View level:** Default and Full views
- **Only available when:** “Headings”, “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the marker's properties on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the section heading style (`\s`), so you can change its font, size,
spacing or alignment. (Default and Full views.)

*(Internal ID: `lb_style_s`)*

#### In Margin

- **Where:** Body tab › Include Scripture Text
- **Type:** Checkbox (not ticked by default)
- **Description:** Show Section Headings in Margin
- **View level:** Default and Full views
- **Only available when:** “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If Margin Notes has been enabled on the Layout Tab, it is possible to also place the Section Headings in the margin. Note that Parallel Passage Refs (if used) will also be placed in the margin area.

**Explanation:**

This is meant to place section headings in the outer margin area, next to the text, when
**Margin Notes** is turned on in the **Layout** tab. It is greyed out unless **Margin Notes** and
**Headings** are both on. In the version this manual describes, the setting is saved but no part
of the typesetting uses it yet, so it may have no visible effect.

*(Internal ID: `c_headingInMargin` · Config key: `document/headinginmargin`)*

#### Parallel Passage Refs

- **Where:** Body tab › Include Scripture Text
- **Type:** Checkbox (ticked by default)
- **Description:** Enable parallel passage references
- **View level:** Default and Full views
- **Only available when:** “Headings”, “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Uncheck this option to hide all the Parallel Passage References which occur below Section Headings.

**Explanation:**

Unticking this **removes** the parallel passage references (`\r`) that are printed under some
section headings. The headings stay. It is greyed out when **Headings** is unticked.
(Default and Full views.)

*(Internal ID: `c_parallelRefs` · Config key: `document/parallelrefs`)*

#### \r

- **Where:** Body tab › Include Scripture Text
- **Type:** Link
- **View level:** Default and Full views
- **Only available when:** “Headings”, “Parallel Passage Refs”, “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the marker's properties on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the parallel passage reference style (`\r`). It is greyed out when
**Headings** or **Parallel Passage Refs** is unticked. (Default and Full views.)

*(Internal ID: `lb_style_r`)*

#### Hide Empty Verses

- **Where:** Body tab › Include Scripture Text
- **Type:** Checkbox (not ticked by default)
- **Description:** Show or hide empty verses
- **View level:** Basic, Default and Full views
- **Only available when:** “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Do not print any empty chapters or verses. Useful for when only part of the text has been drafted but you still need a printout of whatever has been translated so far.

**Explanation:**

**Removes** verses that have no text, and whole chapters with no text. Use it to print a partly
drafted book without many empty verse numbers. Turn it off for the final publication, so you do
not hide verses by mistake. Tick **Show '...'** to mark the gaps.

*(Internal ID: `c_hideEmptyVerses` · Config key: `document/hidemptyverses`)*

#### Show '...'

- **Where:** Body tab › Include Scripture Text
- **Type:** Checkbox (not ticked by default)
- **Description:** Show elipsis in place of missing verses
- **View level:** Basic, Default and Full views
- **Only available when:** “Hide Empty Verses”, “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Indicate using ellipsis that verses and/or entire chapters are missing by placing '...' in the text to alert the reader that some parts of the text have been skipped.

**Explanation:**

When **Hide Empty Verses** removes verses or chapters, this puts "..." where the text was left out.
Readers then know that something is missing. It is greyed out unless **Hide Empty Verses** is ticked.

*(Internal ID: `c_elipsizeMissingVerses` · Config key: `document/elipsizemptyvs`)*

#### Marginal Verses

- **Where:** Body tab › Include Scripture Text
- **Type:** Checkbox (not ticked by default)
- **Description:** Show verse numbers in the margin
- **View level:** Basic, Default and Full views
- **Only available when:** “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Some language communities prefer the verse numbers to be displayed in a vertical stack NEXT to the text (rather than within the text itself). If that is what is required, check this option and also adjust the width of that column to fit the verse numbers.

**Explanation:**

Prints verse numbers in a narrow column beside the text, instead of inside the lines. When you
tick it, choose **Position on Page** and **Col Width (pts)**. **Hanging Poetry Verse Numbers** is
turned off. Verse 1 is hidden when **Hide First Verse Number** is ticked. If two short verses start on the same
line, their numbers can collide; you may need to adjust that paragraph.

*(Internal ID: `c_marginalverses` · Config key: `document/marginalverses`)*

#### Position on Page

- **Where:** Body tab › Include Scripture Text
- **Type:** Drop-down list
- **Description:** Horizontal position of marginal verses
- **View level:** Basic, Default and Full views
- **Choices:** Left; Right; Inner; Outer
- **Only available when:** “Marginal Verses”, “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Marginal verses are usually placed on the left of the text, but can be positioned elsewhere if needed.

**Explanation:**

Chooses where the column of marginal verse numbers goes: **Left** or **Right** of the text, or
**Inner** (next to the spine) or **Outer** (next to the page edge). Inner and Outer change sides on
left-hand and right-hand pages. Greyed out unless **Marginal Verses** is ticked.

*(Internal ID: `fcb_marginVrsPosn` · Config key: `document/marginalposn`)*

#### Col Width (pts)

- **Where:** Body tab › Include Scripture Text
- **Type:** Number box
- **Description:** Column width for marginal verses
- **View level:** Basic, Default and Full views
- **Values:** default 12
- **Only available when:** “Marginal Verses”, “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This is the amount of space beside the column of text to accommodate marginal verse numbers. (pts)

**Explanation:**

The width of the column for marginal verse numbers, in points (1 pt is about 0.35 mm). Make it wide
enough for your longest verse number in your verse number font, for example 12–16 pt. Too small, and the numbers
touch the text. Too large, and you lose space for text. Greyed out unless **Marginal Verses** is ticked.

*(Internal ID: `s_columnShift` · Config key: `document/columnshift`)*

#### Chapter numbers

- **Where:** Body tab › Include Scripture Text
- **Type:** Checkbox (ticked by default)
- **Description:** Show chapter numbers
- **View level:** Basic, Default and Full views
- **Only available when:** “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Uncheck this option to hide all chapter numbers - making the publication read more like an ordinary book.
>
> Note that the 'Single Chapter Books' option lower down (Show Chapter Numbers in:) controls chapter numbers in one-chapter books only.

**Explanation:**

Unticking this hides **all** chapter numbers. This only changes the appearance: the chapters still
exist, so the running header can still show chapter references. To hide the chapter number only in
one-chapter books, use **Single Chapter Books** in the **Other Features** area instead.

*(Internal ID: `c_chapterNumber` · Config key: `document/ifshowchapternums`)*

#### \c

- **Where:** Body tab › Include Scripture Text
- **Type:** Link
- **View level:** Default and Full views
- **Only available when:** “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the marker's properties on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the chapter number style (`\c`). Use it to change the size, font or
color of the chapter numbers. (Default and Full views.)

*(Internal ID: `lb_style_c`)*

#### Verse Numbers

- **Where:** Body tab › Include Scripture Text
- **Type:** Checkbox (ticked by default)
- **Description:** Show verse numbers
- **View level:** Basic, Default and Full views
- **Only available when:** “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Uncheck this option to hide all verse numbers - making the publication read more like an ordinary book.

**Explanation:**

Unticking this hides **all** verse numbers, so the text reads like an ordinary book. This only changes
the appearance; the verses still exist, so headers and notes still work.

*(Internal ID: `c_verseNumbers` · Config key: `document/ifshowversenums`)*

#### \v

- **Where:** Body tab › Include Scripture Text
- **Type:** Link
- **View level:** Default and Full views
- **Only available when:** “Include Scripture Text” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the marker's properties on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the verse number style (`\v`). Use it to change the font, size, color or
raised position of verse numbers. (Default and Full views.)

*(Internal ID: `lb_style__v`)*

### Body tab

#### Include Scripture Text

- **Where:** Body tab
- **Type:** Checkbox (ticked by default)
- **Description:** Show or hide scripture text
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Normally you should leave this checked.
>
> BUT... if you require a printout of just the book introductions (usually for the purpose of final checking, or looking for consistency) then this option can be unchecked (to omit the verse text and everything else in the main body).

**Explanation:**

Leave this ticked for normal printing. Unticking it **removes** chapter 1 and everything after it in
every book, so only the introductions are printed. This is useful for checking the introductions.
All other settings in the **Include Scripture Text** area are greyed out while it is unticked.

*(Internal ID: `c_mainBodyText` · Config key: `document/ifmainbodytext`)*

### Body tab › Other Features

#### Use Special Features for These Books

- **Where:** Body tab › Other Features
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable special features for some books
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Some Poetical books like the Psalms, and maybe even Proverbs look better without drop-cap chapter numbers. Instead, they can use a prefix like "Chapter" or "Psalm" at the start of the chapter. Note: If the text already has one or more \cl markers, then these settings will override what has been set in the text.

**Explanation:**

Prints a label before each chapter number (for example "Psalm 1") as a heading, instead of a large
dropped chapter number. Type the label in **Chapter Label** and the books in the list box beside it.
If the books already contain `\cl` labels, this setting replaces them. (Full view only.)

*(Internal ID: `c_useChapterLabel` · Config key: `document/ifchaplabels`)*

#### List of books with special features enabled

- **Where:** Body tab › Other Features
- **Type:** Text box
- **View level:** Full view only
- **Only available when:** “Use Special Features for These Books” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Add the 3-letter book codes for any books that this "Chapter Label" setting should be applied to.
>
> Note: If this list of books is left empty, then this setting will be applied to ALL books

**Explanation:**

Type the 3-letter book codes (for example `PSA PRO`), separated by spaces. Only these books get the
chapter label. If you leave the box empty, the label is used in **all** books. The same list is
used by **Optimize Layout for Poetry Books**. (Full view only.)

*(Internal ID: `t_clBookList` · Config key: `document/clabelbooks`)*

#### Chapter Label

- **Where:** Body tab › Other Features
- **Type:** Text box
- **Description:** Chapter label (for special feature books)
- **View level:** Full view only
- **Only available when:** “Use Special Features for These Books” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> The chapter “label” to be used when rendering chapter divisions as headings (instead of drop-cap numerals). For example, "Chapter" or "Psalm".
>
> If you want the chapter number to appear centered and above the Section Header WITHOUT any preceding text, then just put the code \\ZWNBSP in here. This will insert a Zero Width No-Break Space.
>
> The chapter “label” to be used when rendering chapter divisions as headings (instead of drop-cap numerals). For example, "Chapter" or "Psalm".
>
> If you want the chapter number to appear centered and above the Section Header WITHOUT any preceding text, then just put the code \ZWNBSP in here. This will insert a Zero Width No-Break Space.

**Explanation:**

The word printed before each chapter number in the listed books, for example the word for "Psalm"
in your language. Advanced: if you want only the number, centered above the first heading, with no word
before it, type `\ZWNBSP` (an invisible character). (Full view only.)

*(Internal ID: `t_clHeading` · Config key: `document/clabel`)*

#### Use One/Two Column Layout for These Books

- **Where:** Body tab › Other Features
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable 1 or 2 column layout for certain books
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Some books (e.g. Introduction, Glossary, Psalms, and maybe even Proverbs) look better formatted as single column, even though most of the books are typeset in two column layout. This allows the same publication to have both single and double column layouts.
>
> Add the 3-letter book codes for any books that should be typeset using a different column layout.
>
> Note that if the layout for the entire publication is set to single column, then the books listed here would use double-column layout. Conversely, if the publication is set as double-column (on the layout page) then any books listed here would be set in single-column layout.

**Explanation:**

Lets some books use a different number of columns from the rest of the publication. If the
publication is two columns (on the **Layout** tab), the books you list here are printed in one column; if
it is one column, they are printed in two. The label of this checkbox changes to show which. A typical use is a two-column Bible with a
one-column glossary. (Full view only.)

*(Internal ID: `c_differentColLayout` · Config key: `document/diffcolayout`)*

#### Optimize Layout for Poetry Books

- **Where:** Body tab › Other Features
- **Type:** Checkbox (ticked by default)
- **View level:** Full view only
- **Only available when:** “Use Special Features for These Books” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Trying to get columns of poetry to balance often creates all sorts of unforeseen issues and unwanted whitespace. This option allows columns to be unbalanced, which might improve the overall look. But note that it also allows Widow and Orphan lines to occur, which is a negative side-effect.

**Explanation:**

For the books listed beside **Use Special Features for These Books**, this lets the two columns end
at different heights, and allows single lines at the top or bottom of a column. This often removes
large white gaps in poetry books like Psalms. It does nothing if that book list is empty. Greyed
out unless **Use Special Features for These Books** is ticked. (Full view only.)

*(Internal ID: `c_optimizePoetryLayout` · Config key: `document/cloptimizepoetry`)*

#### List of books with different column settings

- **Where:** Body tab › Other Features
- **Type:** Text box
- **View level:** Full view only
- **Only available when:** “Use One/Two Column Layout for These Books” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Some books (e.g. Introduction, Glossary, Psalms, and maybe even Proverbs) look better formatted as single column, even though most of the books are typeset in two column layout. This allows the same publication to have both single and double column layouts.
>
> Add the 3-letter book codes for any books that should be typeset using a different column layout.
>
> Note that if the layout for the entire publication is set to single column, then the books listed here would use double-column layout. Conversely, if the publication is set as double-column (on the layout page) then any books listed here would be set in single-column layout.

**Explanation:**

Type the 3-letter book codes that should use the other column layout, separated by spaces, for
example `GLO` or `PSA PRO`. Greyed out unless **Use One/Two Column Layout for These Books** is ticked.
(Full view only.)

*(Internal ID: `t_differentColBookList` · Config key: `document/diffcolayoutbooks`)*

#### Glossary Word Appearance

- **Where:** Body tab › Other Features
- **Type:** Drop-down list
- **Description:** Markup for glossary words in text
- **View level:** Basic, Default and Full views
- **Choices:** None; format as bold; format as italics; format as bold italics; format with emphasis; with ⸤floor⸥ brackets; with ⌊floor⌋ characters; with ⌞corner⌟ characters; star *before word; star after* word; star *before and after*; circumflex ^before word; circumflex after^ word; dagger †before word; dagger after† word; double dagger ‡before word; double dagger after‡ word; \w ...\w* char style; \w keep|as is\w*

**Tooltip (the text shown when you hover the mouse over it):**

> Glossary words are marked up with special \w glossary\w* tags. Specify how these words should be highlighted in the printed output.
>
> The final option \w keeps|markup\w* as it is without removing any parameters such as Strong's numbers.
>
> Glossary words may be marked up with \w glossary\w* tags. Specify how these words should appear in the printed output.
>
> If you wish to apply your own custom styling to \w then select the \w ...\w* character style option.

**Explanation:**

Chooses how words marked as glossary words (`\w ...\w*`) appear in the text:
* **None** – the word is printed as plain text.
* **format as bold / italics / bold italics / with emphasis** – the word gets that formatting.
* **with ⸤floor⸥ brackets**, **⌊floor⌋** or **⌞corner⌟ characters** – the word is placed between
  these characters. Use the **\zglm** link to style them. Your font must contain these characters.
* **star**, **circumflex**, **dagger** or **double dagger** options – a mark is put before
  or after the word (or both, for star).
* **\w ...\w\* char style** – use the `\w` style from the **Styles** tab, so you can design your own format.
* **\w keep|as is\w\*** – the markup is left exactly as it is, including extra information such as
  the glossary form or Strong's numbers. Choose this only if another feature needs that
  information (for Strong's numbers, see the **Notes+Refs** tab).

With all choices except the last, any extra part after a `|` (for example `\w word|glossaryform\w*`)
is removed, so only the word itself is printed.

*(Internal ID: `fcb_glossaryMarkupStyle` · Config key: `document/glossarymarkupstyle`)*

#### Single Chapter Books

- **Where:** Body tab › Other Features
- **Type:** Checkbox (ticked by default)
- **Description:** Show chapters in single chapter books
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Select this option to show the 1 at the beginning of books that only have a single chapter (OBA, PHM, 2JN, 3JN, JUD, etc.)

**Explanation:**

Ticked: books with only one chapter (Obadiah, Philemon, 2 John, 3 John, Jude) show the chapter
number "1" like other books. Unticked: that chapter number is not shown. This only changes the
appearance. It has no effect when **Chapter numbers** is unticked.

*(Internal ID: `c_show1chBookNum` · Config key: `document/ifshow1chbooknum`)*

#### Non-Scripture Books

- **Where:** Body tab › Other Features
- **Type:** Checkbox (not ticked by default)
- **Description:** Show chapters in non-scripture books
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Peripheral books often have more than one "chapter" but do not need the chapter number to be printed. By default, PTXprint removes the chapter numbers from non-scripture books. If you need it to retain (and show) those chapter numbers then check this option.

**Explanation:**

By default PTXprint **removes** chapter markers from non-Scripture books (for example the glossary or
other peripheral books), so no chapter numbers are printed there. Tick this if those books really need
their chapter numbers.

*(Internal ID: `c_showNonScriptureChapters` · Config key: `document/showxtrachapnums`)*

#### \w

- **Where:** Body tab › Other Features
- **Type:** Link
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the marker's properties on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the glossary word style (`\w`). This style is used when **Glossary
Word Appearance** is set to **\w ...\w\* char style**. (Default and Full views.)

*(Internal ID: `lb_style_w`)*

#### \zglm

- **Where:** Body tab › Other Features
- **Type:** Link
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The \zglm style is used to format the floor brackets used in glossary markup.
>
> Click to edit the marker's properties on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the `\zglm` style. This style formats the bracket characters (floor or
corner brackets) placed around glossary words. Use it, for example, to make the brackets smaller
or a different color. (Default and Full views.)

*(Internal ID: `lb_style_zglm`)*
