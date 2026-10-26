# 7. Body tab

## 7.1 What this tab is for

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

## 7.2 Beginning and Ending Material

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

## 7.3 Include Scripture Text

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

## 7.4 Other Features

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

## 7.5 Common tasks

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

## 7.6 Common problems

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

## 7.7 Settings reference

### Body

#### Include Scripture Text

Checkbox, on · Basic+ · `c_mainBodyText` · cfg `document/ifmainbodytext`  
Also: Show or hide scripture text

> Normally you should leave this checked.
>
> BUT... if you require a printout of just the book introductions (usually for the purpose of final checking, or looking for consistency) then this option can be unchecked (to omit the verse text and everything else in the main body).

Unticking it **removes** chapter 1 and everything after it in every book. All other settings in the
**Include Scripture Text** area are greyed out while it is unticked.

#### Beginning and Ending Material

##### Book Introductions

Checkbox, on · Basic+ · `c_bookIntro` · cfg `document/bookintro`  
Also: Enable book introductions (\i..)

> Print the Book Introductions which appear at the beginning of each book. Includes markers like: \is \ip \im \ili etc.

Unticking it **removes** the introduction before typesetting (only material before chapter 1). The
outline is controlled separately by **Introductory Outlines**. Untick it for a "Scripture text only"
edition.

##### Introductory Outlines

Checkbox, on · Basic+ · `c_introOutline` · cfg `document/introoutline`  
Also: Enable introductory outlines

> Print the Introductory Outlines which appear at the beginning of each book. Includes markers: \io1 ... \io4 \ior \iot

Unticking it **removes** only the outline lines and the outline title. The rest of the introduction
stays if **Book Introductions** is ticked. Unticking it also unticks and greys out **Right-align \ior
With Tabbed Leaders**.

##### Right-align \ior With Tabbed Leaders

Checkbox, off · Regular+ · `c_prettyIntroOutline` · cfg `snippets/fancyintro`  
Also: Enable Right-aligned outlines with leaders · Needs: “Introductory Outlines”

> This will right-align and add leader tabs (. . . .) before the \ior numbers for a pretty Intro Outline Table.

Appearance only. Not applied to non-Scripture books.

##### Filter Glossary to Only Include Entries Used in the Text

Checkbox, off · Basic+ · `c_filterGlossary` · cfg `document/filterglossary`

> This option only has an effect if the Glossary (GLO) is one of the books being printed. If you have large glossary with many entries but are only printing a small selection of books, you may benefit from this option which will strip out any entries from the Glossary which are not marked-up in the text of the selected book(s) or chapter(s). i.e. only the \w marked-up\w* entries in the selected books/chapters will show in the glossary. Entries marked up inside a kept entry are also kept.

Use it when you print only a few books with a large glossary. All other entries are **removed** from
the printed glossary.

##### Start All Other Chapters on a New Page

Checkbox, off · Basic+ · `c_pagebreakAllChs` · cfg `document/pagebreakallchs`  
Also: Start every chapter on a new page

> Use this option to force a page break before every chapter. This is most commonly used for testing materials when each chapter needs to be printed and given to a different person.

Every chapter except chapter 1. It can use a lot of paper. To also start chapter 1 on a new page,
tick **Start 1st Chapter on a New Page**.

##### Start 1st Chapter on a New Page

Checkbox, off · Basic+ · `c_ch1pagebreak` · cfg `document/ch1pagebreak`  
Also: Start new page after introduction

> Use this option to automatically make a page break after a book's introduction section. The break will come right before the \c 1 marker.

Use it when the introductions are long, or for a cleaner look.

#### Include Scripture Text

##### Hide First Verse Number

Checkbox, on · Regular+ · `c_omitverseone` · cfg `document/ifomitverseone`  
Needs: “Include Scripture Text”

> It is quite common to hide the first verse number - especially when following a drop-cap chapter number. By default this option is on. If you prefer to see verse number 1, then uncheck this option.
>
> Note: verse 1 is only hidden when it follows a drop-cap chapter number, or when marginal verses are used.

This is the usual style. The verse still exists, so references still work.

##### Keep Repeated Words Together

Checkbox, off · Regular+ · `c_glueredupwords` · cfg `document/glueredupwords`  
Needs: “Include Scripture Text”

> This option encourages re-duplicated words (i.e. those which are intentionally repeated) to come together on the same line by inserting a NoBreakSpace between them (only words of 3 or more letters). For example, "gama gama", or "kala kala" need to be stuck together (with a NBSP) in order to be read meaningfully. However, if there are many of these in the language, then it may create other unwanted typesetting issues. Use with care!

The two words then always stay on the same line. Check the result before you keep it.

##### Indent First Paragraph

Checkbox, on · Regular+ · `c_firstParaIndent` · cfg `document/firstparaindent`  
Also: Indent first paragraph after section heading · Needs: “Include Scripture Text”

> If this option is unchecked, it will make the 1st  
> \p(aragraph) after a Section Heading appear as a \m(argin) paragraph with no indentation.

Unticked is common in many books. Appearance only.

##### Hanging Poetry Verse Numbers

Checkbox, on · Regular+ · `c_hangpoetry` · cfg `document/hangpoetry`  
Also: Use hanging verse number for poetry · Needs: “Include Scripture Text” · Greyed out by: “Marginal Verses”

> Verse numbers for Poetry elements all line up vertically on the margin, and Verse Bridges (3-4) also stack vertically.

Turned off and greyed out when **Marginal Verses** is ticked.

##### Prevent Verse Widow Words

Checkbox, off · Regular+ · `c_preventwidows` · cfg `document/preventwidows`  
Needs: “Include Scripture Text”

> This option prevents short words (of 3 characters or less) from occurring AFTER a verse begins near the end of a line.

Joins the verse number and the short word to the next word, so the verse number does not sit alone
at the end of a line. Changes line breaks only.

##### Prevent Orphan Words

Checkbox, off · Basic+ · `c_preventorphans` · cfg `document/preventorphans`  
Also: Prevent orphan words at end of paragraph or start of line. · Needs: “Include Scripture Text”

> This option limits short words at the ends of paragraphs from occurring on a line on their own. It also prevents short words at the end of sentences from starting on a new line.
>
> The maximum orphan word length can be set in the 'Body Text' section of the Advanced > Other tab.

Changes line breaks only. The maximum "short word" length is **Maximum orphan word length** on
the **Advanced** tab, **Other** tab, **Body Text** area (default 8 letters).

##### Justify Paragraphs

Checkbox, on · Basic+ · `c_justify` · cfg `paragraph/ifjustify`  
Needs: “Include Scripture Text”

> By default the text will be fully justified. If you prefer a ragged edge, then uncheck this option.
>
> Note that a justification setting of "Justify" in a style is subject to this setting.

Ragged text can be easier to read in narrow columns and in languages with long words.

##### Headings

Checkbox, on · Basic+ · `c_sectionHeads` · cfg `document/sectionheads`  
Also: Enable section headings · Needs: “Include Scripture Text”

> Uncheck this option if you don't want to print any Section Headings. Unchecking this option will ALSO uncheck the Parallel Passage Refs.

Removes `\s`, `\s1`, `\s2` … and all `\r` references. Unticking it also turns off **In Margin**.
Ticking it again ticks **Parallel Passage Refs** again.

##### \s

Link · Regular+ · `lb_style_s`  
Needs: “Headings”, “Include Scripture Text”

> Click to edit the marker's properties on the Styles tab.

Change the section heading's font, size, spacing or alignment.

##### In Margin

Checkbox, off · Regular+ · `c_headingInMargin` · cfg `document/headinginmargin`  
Also: Show Section Headings in Margin · Needs: “Include Scripture Text”

> If Margin Notes has been enabled on the Layout Tab, it is possible to also place the Section Headings in the margin. Note that Parallel Passage Refs (if used) will also be placed in the margin area.

Greyed out unless **Margin Notes** (on the **Layout** tab) and **Headings** are both on. In the
version this manual describes, the setting is saved but no part of the typesetting uses it yet, so it
may have no visible effect.

##### Parallel Passage Refs

Checkbox, on · Regular+ · `c_parallelRefs` · cfg `document/parallelrefs`  
Also: Enable parallel passage references · Needs: “Headings”, “Include Scripture Text”

> Uncheck this option to hide all the Parallel Passage References which occur below Section Headings.

Unticking it **removes** the `\r` references. The headings stay.

##### \r

Link · Regular+ · `lb_style_r`  
Needs: “Headings”, “Parallel Passage Refs”, “Include Scripture Text”

> Click to edit the marker's properties on the Styles tab.

Opens the parallel passage reference style (`\r`).

##### Hide Empty Verses

Checkbox, off · Basic+ · `c_hideEmptyVerses` · cfg `document/hidemptyverses`  
Also: Show or hide empty verses · Needs: “Include Scripture Text”

> Do not print any empty chapters or verses. Useful for when only part of the text has been drafted but you still need a printout of whatever has been translated so far.

Turn it off for the final publication, so you do not hide verses by mistake.

##### Show '...'

Checkbox, off · Basic+ · `c_elipsizeMissingVerses` · cfg `document/elipsizemptyvs`  
Also: Show elipsis in place of missing verses · Needs: “Hide Empty Verses”, “Include Scripture Text”

> Indicate using ellipsis that verses and/or entire chapters are missing by placing '...' in the text to alert the reader that some parts of the text have been skipped.

Applies to verses or chapters removed by **Hide Empty Verses**.

##### Marginal Verses

Checkbox, off · Basic+ · `c_marginalverses` · cfg `document/marginalverses`  
Also: Show verse numbers in the margin · Needs: “Include Scripture Text”

> Some language communities prefer the verse numbers to be displayed in a vertical stack NEXT to the text (rather than within the text itself). If that is what is required, check this option and also adjust the width of that column to fit the verse numbers.

**Hanging Poetry Verse Numbers** is turned off. Verse 1 is hidden when **Hide First Verse Number** is
ticked. If two short verses start on the same line, their numbers can collide; you may need to
adjust that paragraph.

##### Position on Page – Horizontal position of marginal verses

Drop-down · Basic+ · `fcb_marginVrsPosn` · cfg `document/marginalposn`  
Choices: Left | Right | Inner | Outer · Needs: “Marginal Verses”, “Include Scripture Text”

> Marginal verses are usually placed on the left of the text, but can be positioned elsewhere if needed.

**Inner** is next to the spine, **Outer** next to the page edge; these change sides on left-hand and
right-hand pages.

##### Col Width (pts) – Column width for marginal verses

Number · Basic+ · `s_columnShift` · cfg `document/columnshift`  
Needs: “Marginal Verses”, “Include Scripture Text”

> This is the amount of space beside the column of text to accommodate marginal verse numbers. (pts)

Make it wide enough for your longest verse number in your verse number font, for example 12–16 pt.
Too small, and the numbers touch the text. Too large, and you lose text space.

##### Chapter numbers

Checkbox, on · Basic+ · `c_chapterNumber` · cfg `document/ifshowchapternums`  
Also: Show chapter numbers · Needs: “Include Scripture Text”

> Uncheck this option to hide all chapter numbers - making the publication read more like an ordinary book.
>
> Note that the 'Single Chapter Books' option lower down (Show Chapter Numbers in:) controls chapter numbers in one-chapter books only.

Appearance only: the chapters still exist, so the running header can still show chapter references.

##### \c

Link · Regular+ · `lb_style_c`  
Needs: “Include Scripture Text”

> Click to edit the marker's properties on the Styles tab.

Change the size, font or colour of chapter numbers.

##### Verse Numbers

Checkbox, on · Basic+ · `c_verseNumbers` · cfg `document/ifshowversenums`  
Also: Show verse numbers · Needs: “Include Scripture Text”

> Uncheck this option to hide all verse numbers - making the publication read more like an ordinary book.

Appearance only: the verses still exist, so headers and notes still work.

##### \v

Link · Regular+ · `lb_style__v`  
Needs: “Include Scripture Text”

> Click to edit the marker's properties on the Styles tab.

Change the font, size, colour or raised position of verse numbers.

#### Other Features

##### Use Special Features for These Books

Checkbox, off · Full · `c_useChapterLabel` · cfg `document/ifchaplabels`  
Also: Enable special features for some books

> Some Poetical books like the Psalms, and maybe even Proverbs look better without drop-cap chapter numbers. Instead, they can use a prefix like "Chapter" or "Psalm" at the start of the chapter. Note: If the text already has one or more \cl markers, then these settings will override what has been set in the text.

Type the label in **Chapter Label** and the books in the list box beside it.

##### List of books with special features enabled

Text box · Full · `t_clBookList` · cfg `document/clabelbooks`  
Needs: “Use Special Features for These Books”

> Add the 3-letter book codes for any books that this "Chapter Label" setting should be applied to.
>
> Note: If this list of books is left empty, then this setting will be applied to ALL books

Separate codes with spaces, for example `PSA PRO`. The same list is used by **Optimize Layout for
Poetry Books**.

##### Chapter Label – Chapter label (for special feature books)

Text box · Full · `t_clHeading` · cfg `document/clabel`  
Needs: “Use Special Features for These Books”

> The chapter “label” to be used when rendering chapter divisions as headings (instead of drop-cap numerals). For example, "Chapter" or "Psalm".
>
> If you want the chapter number to appear centered and above the Section Header WITHOUT any preceding text, then just put the code \ZWNBSP in here. This will insert a Zero Width No-Break Space.

Advanced: `\ZWNBSP` is an invisible character.

##### Use One/Two Column Layout for These Books

Checkbox, off · Full · `c_differentColLayout` · cfg `document/diffcolayout`  
Also: Enable 1 or 2 column layout for certain books

> Some books (e.g. Introduction, Glossary, Psalms, and maybe even Proverbs) look better formatted as single column, even though most of the books are typeset in two column layout. This allows the same publication to have both single and double column layouts.
>
> Add the 3-letter book codes for any books that should be typeset using a different column layout.
>
> Note that if the layout for the entire publication is set to single column, then the books listed here would use double-column layout. Conversely, if the publication is set as double-column (on the layout page) then any books listed here would be set in single-column layout.

The checkbox label changes to show which (one or two columns). A typical use is a two-column Bible
with a one-column glossary.

##### Optimize Layout for Poetry Books

Checkbox, on · Full · `c_optimizePoetryLayout` · cfg `document/cloptimizepoetry`  
Needs: “Use Special Features for These Books”

> Trying to get columns of poetry to balance often creates all sorts of unforeseen issues and unwanted whitespace. This option allows columns to be unbalanced, which might improve the overall look. But note that it also allows Widow and Orphan lines to occur, which is a negative side-effect. It applies only to the books listed above.

Allows single lines at the top or bottom of a column. This often removes large white gaps in poetry
books like Psalms. Other books are not changed. Untick it to keep normal column balancing for the
listed books. It does nothing if the book list is empty.

##### List of books with different column settings

Text box · Full · `t_differentColBookList` · cfg `document/diffcolayoutbooks`  
Needs: “Use One/Two Column Layout for These Books”

> Some books (e.g. Introduction, Glossary, Psalms, and maybe even Proverbs) look better formatted as single column, even though most of the books are typeset in two column layout. This allows the same publication to have both single and double column layouts.
>
> Add the 3-letter book codes for any books that should be typeset using a different column layout.
>
> Note that if the layout for the entire publication is set to single column, then the books listed here would use double-column layout. Conversely, if the publication is set as double-column (on the layout page) then any books listed here would be set in single-column layout.

Separate codes with spaces, for example `GLO` or `PSA PRO`.

##### Glossary Word Appearance – Markup for glossary words in text

Drop-down · Basic+ · `fcb_glossaryMarkupStyle` · cfg `document/glossarymarkupstyle`  
Choices: None | format as bold | format as italics | format as bold italics | format with emphasis | with ⸤floor⸥ brackets | with ⌊floor⌋ characters | with ⌞corner⌟ characters | star *before word | star after* word | star *before and after* | circumflex ^before word | circumflex after^ word | dagger †before word | dagger after† word | double dagger ‡before word | double dagger after‡ word | \w ...\w* char style | \w keep|as is\w*

> Glossary words are marked up with special \w glossary\w* tags. Specify how these words should be highlighted in the printed output.
>
> The final option \w keeps|markup\w* as it is without removing any parameters such as Strong's numbers.
>
> Glossary words may be marked up with \w glossary\w* tags. Specify how these words should appear in the printed output.
>
> If you wish to apply your own custom styling to \w then select the \w ...\w* character style option.

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

##### Single Chapter Books

Checkbox, on · Basic+ · `c_show1chBookNum` · cfg `document/ifshow1chbooknum`  
Also: Show chapters in single chapter books

> Select this option to show the 1 at the beginning of books that only have a single chapter (OBA, PHM, 2JN, 3JN, JUD, etc.)

Appearance only. No effect when **Chapter numbers** is unticked.

##### Non-Scripture Books

Checkbox, off · Basic+ · `c_showNonScriptureChapters` · cfg `document/showxtrachapnums`  
Also: Show chapters in non-scripture books

> Peripheral books often have more than one "chapter" but do not need the chapter number to be printed. By default, PTXprint removes the chapter numbers from non-scripture books. If you need it to retain (and show) those chapter numbers then check this option.

Tick it only if those books really need their chapter numbers.

##### \w

Link · Regular+ · `lb_style_w`

> Click to edit the marker's properties on the Styles tab.

Used when **Glossary Word Appearance** is **\w ...\w\* char style**.

##### \zglm

Link · Regular+ · `lb_style_zglm`

> The \zglm style is used to format the floor brackets used in glossary markup.
>
> Click to edit the marker's properties on the Styles tab.

For example, to make the brackets smaller or a different colour.
