## What this tab is for

The **Body** tab controls *what* is printed from each book, and some of *how* the main text looks.
Come here when you want to:

* leave out parts of the text, for example the book introductions, section headings or empty verses;
* hide or show chapter numbers and verse numbers;
* put verse numbers in a column next to the text (marginal verses);
* change how glossary words are marked in the text;
* start chapters on a new page, or print some books in one column and others in two.

Some settings **remove text** before typesetting. Others only **change the appearance** and keep
all the text. This matters. For example, if you hide verse numbers, the running header can still
show chapter and verse references, because the verses are still there. If you untick **Headings**,
the section headings are taken out completely. Each section below says which kind of setting it is.

The tab has three areas: **Beginning and Ending Material**, **Include Scripture Text** and
**Other Features**. Some settings are only shown in the **Regular** or **Full** view.

## Beginning and Ending Material

These settings deal with the introduction at the start of each book, and with the glossary.

* **Book Introductions** and **Introductory Outlines** **remove content** when unticked: PTXprint
  takes these paragraphs out before typesetting. Only material before the first chapter is affected.
  * **Book Introductions** covers the introduction paragraphs and headings (`\is`, `\ip`, `\im`, `\ili` …).
  * **Introductory Outlines** covers only the outline (`\io1`–`\io4`, `\iot`, `\ior`).
  * You can print the introduction without the outline, or the outline without the introduction.
* **Right-align \ior With Tabbed Leaders** only changes the appearance of the outline: the reference
  at the end of each outline line goes to the right edge, with dots before it, like a table of
  contents. It does nothing in non-Scripture books.
* **Filter Glossary to Only Include Entries Used in the Text** **removes content** from the
  glossary book (GLO). It only matters when GLO is one of the books you print.
* **Start 1st Chapter on a New Page** and **Start All Other Chapters on a New Page** add page breaks.
  They do not remove text.

## Include Scripture Text

The checkbox **Include Scripture Text** is the title of this area. Leave it ticked. Unticking it
**removes** everything from the first chapter onwards in every book, so only the introductions (and
other material before chapter 1) are printed. This is useful for checking the introductions. All
other settings in this area are greyed out while it is unticked.

### What is included

* **Headings** – section headings (`\s`, `\s1`, `\s2` …). Unticking it **removes** all section
  headings and all parallel passage references.
* **Parallel Passage Refs** – the references under some section headings (`\r`), for example
  "(Mark 1:1-8)". Unticking it **removes** them. Greyed out when **Headings** is unticked.
* **Hide Empty Verses** **removes** verses (and whole chapters) that have no text yet, for a draft
  where only part of the book is translated. Tick **Show '...'** as well to show the reader where
  text was left out.
* **Chapter numbers** and **Verse Numbers** only change the **appearance**. When unticked, the
  numbers are not printed, but PTXprint still knows the chapters and verses. So headers, footnotes
  and cross-references still work.

### How the text looks

* **Justify Paragraphs** – ticked gives straight left and right edges. Unticked gives a ragged
  right edge (ragged left for right-to-left scripts).
* **Indent First Paragraph** – when unticked, the first paragraph after a section heading starts at
  the margin.
* **Hide First Verse Number** – hides the "1" of verse 1 after a large (dropped) chapter number, or
  when marginal verses are used.
* **Hanging Poetry Verse Numbers** – the verse number sits to the left of the poetry line, so all
  poetry lines stay lined up.
* **Prevent Verse Widow Words**, **Prevent Orphan Words** and **Keep Repeated Words Together**
  join some words with a space that cannot break. This changes where lines break, not the words.

### Marginal verses

Tick **Marginal Verses** to print verse numbers in a narrow column beside the text. Then choose the
side in **Position on Page** and the column width in **Col Width (pts)**. (A pt, or point, is about
0.35 mm.) While **Marginal Verses** is ticked, **Hanging Poetry Verse Numbers** is turned off and
greyed out.

### Style links

The small links **\s**, **\r**, **\c** and **\v** open the **Styles** tab at that marker, to change
the font, size or spacing of section headings, parallel references, chapter numbers or verse numbers.

## Other Features

This area is for special treatment of some books, and for glossary words.

* **Use Special Features for These Books** (Full view only) prints a text label before each chapter
  number, for example "Psalm 1" as a heading, instead of a large dropped number. This is common
  for Psalms. Type the label in **Chapter Label** and the book codes in the list box beside the
  checkbox. **Optimize Layout for Poetry Books** belongs to this group.
* **Use One/Two Column Layout for These Books** (Full view only) lets some books use a different
  number of columns from the rest. The label says "Use One Column" when the publication is two
  columns (set on the **Layout** tab), and "Use Two Column" when it is one column.
* **Glossary Word Appearance** decides how glossary words (`\w ...\w*`) look in the text.
* **Show Chapter Numbers In: Single Chapter Books** and **Non-Scripture Books** decide whether a
  chapter number is printed in one-chapter books (such as Jude) and in peripheral books (such as
  the glossary). For non-Scripture books, unticking **removes** the chapter markers.
* The links **\w** and **\zglm** open the **Styles** tab for the glossary word style and for the
  glossary bracket characters.

## Common tasks

### How do I print only the book introductions?

1. On the **Body** tab, untick **Include Scripture Text**.
2. Make sure **Book Introductions** (and **Introductory Outlines**, if wanted) are ticked.
3. Click **Print (Make PDF)**.
4. Tick **Include Scripture Text** again afterwards.

### How do I print a draft that has many untranslated verses?

1. On the **Body** tab, tick **Hide Empty Verses**.
2. If readers should see where text is missing, tick **Show '...'**.
3. Print again.

### How do I remove all section headings?

On the **Body** tab, untick **Headings**. The parallel passage references are removed too; you
cannot keep them without the headings.

### How do I show verse number 1?

On the **Body** tab, untick **Hide First Verse Number** (shown in the **Regular** and **Full** views).

### How do I put the verse numbers in the margin?

1. On the **Body** tab, tick **Marginal Verses**.
2. In **Position on Page**, choose **Left**, **Right**, **Inner** (next to the spine) or **Outer**
   (next to the page edge).
3. In **Col Width (pts)**, give enough width for the longest verse number, for example 12–16.
4. Print and check that numbers like "176" fit.

### How do I print "Psalm 1", "Psalm 2" … instead of large chapter numbers in Psalms?

1. Switch to the **Full** view.
2. On the **Body** tab, in **Other Features**, tick **Use Special Features for These Books**.
3. In the list box, type `PSA`. (An empty list means **all** books.)
4. In **Chapter Label**, type the word for "Psalm" in your language.
5. Print again.

### How do I print the glossary book in one column when the rest is two columns?

1. Switch to the **Full** view.
2. On the **Body** tab, tick **Use One Column Layout for These Books**.
3. In the box beside it, type `GLO`. Separate several books with spaces, for example `GLO PSA`.

### How do I change how glossary words look in the text?

1. On the **Body** tab, in **Other Features**, open **Glossary Word Appearance**.
2. Choose a style, for example **format as bold** or **star \*before word**.
3. For your own formatting, choose **\w ...\w\* char style** and click the **\w** link to edit that
   style on the **Styles** tab.

## Common problems

**The parallel references disappeared.**
Cause: **Headings** was unticked. This also unticks and greys out **Parallel Passage Refs**.
Fix: tick **Headings** again, then tick **Parallel Passage Refs**.

**Verse 1 is still printed, although "Hide First Verse Number" is ticked.**
Cause: verse 1 is only hidden after a dropped chapter number (or with marginal verses). If chapters
use a label (for example "Psalm 1") or chapter numbers are hidden, verse 1 can still show.
Fix: check the chapter number settings on this tab.

**"Hanging Poetry Verse Numbers" is greyed out.**
Cause: **Marginal Verses** is ticked. The two cannot be used together.

**"Optimize Layout for Poetry Books" has no effect.**
Cause: it only works for the books listed beside **Use Special Features for These Books**, and only
while that is ticked. If the list is empty, nothing is optimized.
Fix: tick **Use Special Features for These Books** and type the book codes (for example `PSA PRO`).

**The chapter label appears in every book, not only Psalms.**
Cause: the book list beside **Use Special Features for These Books** is empty, which means
"all books". Fix: type the book codes in the list.

**The glossary is still very long after ticking "Filter Glossary…".**
Cause: an entry is kept when its word is marked as a glossary word (`\w ...\w*`) in the books you
print, or inside another kept entry. Words not marked in the text do not count.
Fix: check the glossary markup in Paratext.

**Some lines have large gaps after ticking "Keep Repeated Words Together" or "Prevent Orphan Words".**
Cause: these settings stop the line breaking between some words, so it breaks elsewhere.
Fix: untick the setting, or fix the few bad lines by hand.

**"In Margin" (for headings) is greyed out.**
Cause: it needs **Margin Notes** turned on (on the **Layout** tab) and **Headings** ticked.

**The chapter numbers are missing in the glossary or other peripheral books.**
Cause: by default PTXprint removes chapter numbers from non-Scripture books. Fix: tick
**Non-Scripture Books** under **Show Chapter Numbers In**.

## Control notes

### @c_bookIntro
Unticking it **removes** the introduction before typesetting (only material before chapter 1). The
outline is controlled separately by **Introductory Outlines**. Untick it for a "Scripture text only"
edition.

### @c_introOutline
Unticking it **removes** only the outline lines and the outline title. The rest of the introduction
stays if **Book Introductions** is ticked. Unticking it also unticks and greys out **Right-align \ior
With Tabbed Leaders**.

### @c_prettyIntroOutline
Appearance only. Not applied to non-Scripture books.

### @c_filterGlossary
Use it when you print only a few books with a large glossary. All other entries are **removed** from
the printed glossary.

### @c_pagebreakAllChs
Every chapter except chapter 1. It can use a lot of paper. To also start chapter 1 on a new page,
tick **Start 1st Chapter on a New Page**.

### @c_ch1pagebreak
Use it when the introductions are long, or for a cleaner look.

### @c_omitverseone
This is the usual style. The verse still exists, so references still work.

### @c_glueredupwords
The two words then always stay on the same line. Check the result before you keep it.

### @c_firstParaIndent
Unticked is common in many books. Appearance only.

### @c_hangpoetry
Turned off and greyed out when **Marginal Verses** is ticked.

### @c_preventwidows
Joins the verse number and the short word to the next word, so the verse number does not sit alone
at the end of a line. Changes line breaks only.

### @c_preventorphans
Changes line breaks only. The maximum "short word" length is **Maximum orphan word length** on
the **Advanced** tab, **Other** tab, **Body Text** area (default 8 letters).

### @c_justify
Ragged text can be easier to read in narrow columns and in languages with long words.

### @c_sectionHeads
Removes `\s`, `\s1`, `\s2` … and all `\r` references. Unticking it also turns off **In Margin**.
Ticking it again ticks **Parallel Passage Refs** again.

### @lb_style_s
Change the section heading's font, size, spacing or alignment.

### @c_headingInMargin
Greyed out unless **Margin Notes** (on the **Layout** tab) and **Headings** are both on. In the
version this manual describes, the setting is saved but no part of the typesetting uses it yet, so it
may have no visible effect.

### @c_parallelRefs
Unticking it **removes** the `\r` references. The headings stay.

### @lb_style_r
Opens the parallel passage reference style (`\r`).

### @c_hideEmptyVerses
Turn it off for the final publication, so you do not hide verses by mistake.

### @c_elipsizeMissingVerses
Applies to verses or chapters removed by **Hide Empty Verses**.

### @c_marginalverses
**Hanging Poetry Verse Numbers** is turned off. Verse 1 is hidden when **Hide First Verse Number** is
ticked. If two short verses start on the same line, their numbers can collide; you may need to
adjust that paragraph.

### @fcb_marginVrsPosn
**Inner** is next to the spine, **Outer** next to the page edge; these change sides on left-hand and
right-hand pages.

### @s_columnShift
Make it wide enough for your longest verse number in your verse number font, for example 12–16 pt.
Too small, and the numbers touch the text. Too large, and you lose text space.

### @c_chapterNumber
Appearance only: the chapters still exist, so the running header can still show chapter references.

### @lb_style_c
Change the size, font or colour of chapter numbers.

### @c_verseNumbers
Appearance only: the verses still exist, so headers and notes still work.

### @lb_style__v
Change the font, size, colour or raised position of verse numbers.

### @c_mainBodyText
Unticking it **removes** chapter 1 and everything after it in every book. All other settings in the
**Include Scripture Text** area are greyed out while it is unticked.

### @c_useChapterLabel
Type the label in **Chapter Label** and the books in the list box beside it.

### @t_clBookList
Separate codes with spaces, for example `PSA PRO`. The same list is used by **Optimize Layout for
Poetry Books**.

### @t_clHeading
Advanced: `\ZWNBSP` is an invisible character.

### @c_differentColLayout
The checkbox label changes to show which (one or two columns). A typical use is a two-column Bible
with a one-column glossary.

### @c_optimizePoetryLayout
Allows single lines at the top or bottom of a column. This often removes large white gaps in poetry
books like Psalms. Other books are not changed. Untick it to keep normal column balancing for the
listed books. It does nothing if the book list is empty.

### @t_differentColBookList
Separate codes with spaces, for example `GLO` or `PSA PRO`.

### @fcb_glossaryMarkupStyle
* **None** – plain text.
* **format as bold / italics / bold italics / with emphasis** – the word gets that formatting.
* **with ⸤floor⸥ brackets**, **⌊floor⌋** or **⌞corner⌟ characters** – the word goes between
  these characters. Style them with the **\zglm** link. Your font must contain them.
* **star**, **circumflex**, **dagger** or **double dagger** – a mark before or after the word. For a
  star on both sides, choose **star \*before and after\***.
* **\w ...\w\* char style** – uses the `\w` style from the **Styles** tab, so you can design your own.
* **\w keep|as is\w\*** – keeps extra information such as the glossary form or Strong's numbers.
  Choose it only if another feature needs that (for Strong's numbers, see the **Notes+Refs** tab).

With all choices except the last, any part after a `|` (for example `\w word|glossaryform\w*`) is
removed, so only the word itself is printed.

### @c_show1chBookNum
Appearance only. No effect when **Chapter numbers** is unticked.

### @c_showNonScriptureChapters
Tick it only if those books really need their chapter numbers.

### @lb_style_w
Used when **Glossary Word Appearance** is **\w ...\w\* char style**.

### @lb_style_zglm
For example, to make the brackets smaller or a different colour.
