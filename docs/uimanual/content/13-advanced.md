## What this tab is for

The **Advanced** tab holds settings for experienced users. Most people never need it. Come here when another tab cannot give you the result you need, or when the support team asks you to change a specific setting.

The tab has two sub-tabs:

* **Main** – ways to change the text before it is typeset (a changes file, a processing script), extra stylesheets and TeX settings files, interlinear output, plugins, internet use, and locks that protect a finished layout.
* **Other** – about 125 "TeXpert" settings: fine controls for the typesetting engine, sorted into groups such as **Page Layout and Spacing** or **Footnotes, Cross-references, Study Notes**.

The tab is only shown in the **Regular** and **Full** views. Some **Main** settings are only shown in the **Full** view (noted below).

## Before you change anything here

A small change here can move text on many pages. Follow these rules:

1. **Change one setting at a time.** Then print and look at the result. If you change several together, you cannot tell which one caused a change.
2. **Write down the original value** before you change it.
3. **Look for bold labels.** On the **Other** sub-tab, the label of a check box or number box turns **bold** when its value differs from the default. (Drop-down lists do not turn bold.)
4. **To go back to the default value:**
   * Number box: click its bold label.
   * Check box: click the check box again.
   * Drop-down list: choose the first item. The first item is always the default.
5. **Hover over a setting** to see its tooltip. The first line shows the internal name and the default value in square brackets. For a number box the first number in the brackets is the default; the others are the lowest value, highest value and step sizes.

PTXprint saves a TeXpert setting in the configuration only when it differs from the default.

To find a TeXpert setting quickly, type part of its name in the **Search for settings** box at the bottom of the main window (Ctrl+F).

## Main sub-tab: Text Processing & Stylesheets

Here you change the text, or how it is styled, with files you edit yourself. Each option has a check box (to turn it on) and an **Edit...** button, which is only active when the box is ticked. **Edit...** opens the file on the **View+Edit** tab, where you can type in it and save it.

These features are for people who understand USFM, regular expressions (a way to describe text patterns) or TeX. Never change these files if you are not sure what you are doing. To turn a file off, untick its box; you do not need to delete the file.

* **Apply Modifications to USFM Text (changes.txt)** – search-and-replace rules applied to a temporary copy of the text before typesetting. Your Paratext project is never changed. `changes.txt` belongs to the current configuration only; `PrintDraftChanges.txt` (in the project folder) applies to all configurations of the project.
* **Apply Customized Settings (ptxprint-mods.tex)** – TeX settings applied after all PTXprint settings, for things PTXprint has no control for. A support person may give you a line to add here.
* **Apply Initial Settings (ptxprint-premods.tex)** – TeX settings applied before the stylesheets and other settings. Rarely needed. (**Full** view only.)
* **Apply Customized Styles (custom.sty)** – the project's own custom stylesheet, the same one Paratext uses. (**Full** view only.)
* **Apply Stylesheet Overrides (ptxprint-mods.sty)** – an extra stylesheet for this configuration that overrides other styles. Most style changes are easier on the **Styles** tab. (**Full** view only.)
* **Process Text With Custom Script at** – runs a program of your own on each book. (**Full** view only.)

PTXprint changes the text in this order:

1. A custom script, if **start** is chosen.
2. The rules in the changes files.
3. **Auto-Correct USFM** and other changes PTXprint makes for settings on other tabs.
4. A custom script, if **end** is chosen.

## Main sub-tab: General

Settings that do not fit anywhere else:

* **Sensitive Project** – shortens picture credits and keeps private data out of the PDF.
* **Auto-Correct USFM** – fixes common USFM mistakes and warns about serious ones. Leave it ticked.
* **Interlinear** – prints Paratext interlinear glosses under (or above) each word. (**Full** view only.)
* **Auto-tag Hebrew and Greek words** – marks these words so they use the right font.
* **Only Use English Links** and **Disable ALL Internet Use** – how PTXprint uses the internet.
* **Plugins** – loads extra parts of the typesetting code for special features. (**Full** view only.)
* **Lock XeTeX Layout Level** and **Lock UI Layout Settings** – protect a finished layout from changes. (**Full** view only.)

## Main sub-tab: Capture tests?

Only shown in the **Full** view. A developer tool that records what you click to make an automatic test. Normal users do not need it.

## Other sub-tab: the TeXpert settings

Click a group name to open or close it. The filter button at the top shows only the groups that have changed settings; it is only active while the **Other** sub-tab is shown.

The sections below follow the groups on the screen.

### Page Layout and Spacing

Where books and introductions start, how two columns are balanced, line spacing, and notelines.

* **Where to start a new book**: next page, same page as the end of the previous book, or next odd (right-hand) page. **Page full factor** sets how full the page can be before the next book is moved to a new page anyway.
* **Where to start a new intro page** does the same for book introductions.
* **Unbalanced Lines (Max)** is only used when **Allow Unbalanced Columns** is ticked on the **Layout** tab.
* **Variable line spacing maximum stretch** and **shrink** are only used when **Fill Columns** is ticked on the **Layout** tab.
* The **Noteline** settings change the lines for hand-written notes, which you turn on (and colour) with **Notelines** on the **Layout** tab.
* **Maximum layout version** and **Legacy 1/14 LineSpacing** keep older projects looking the same after PTXprint is updated.
* **Maximum parallel processes** limits how many jobs run at the same time, for example when the page filler works.

### Chapter and Verse

Space after chapter and verse numbers, the size of large (drop) chapter numbers, hanging verse numbers in poetry, and marginal verse numbers (verse numbers in the margin, set on the **Body** tab).

### Body Text

Paragraph indents, line breaking and hyphenation, and clickable links.

Some of these are "penalties": a number that tells the typesetting engine how much to avoid something. Higher = avoid more strongly. 10000 means "never".

* **Hyphenation threshold**, **Penalty for inserting hyphen** and **Double hyphenation penalty** only matter when hyphenation is on (**Fonts+Script** tab).
* **Maximum orphan word length** is only used when **Prevent Orphan Words** is ticked on the **Body** tab.

### Fonts and Underline

How line heights are measured, whether system fonts can be used, and how underlines look.

### Footnotes, Cross-references, Study Notes

Where notes go on a page, when notes may be split across pages, fine spacing of paragraphed notes, and the gap to margin notes. Many of these interact. Change them only to solve a specific problem, and check several pages after each change.

### Diglot

Only used when you print two or more texts side by side (see the **Diglot** tab): notes, versification, shading, borders, and what happens when a page cannot be printed.

### Pictures, Figures, Images, Sidebars

Default picture position, order of caption and reference, space around pictures and sidebars, and the style of picture credits.

### PDF Options, Covers, Show/Hide

Bookmarks, links and transparency in the PDF, some cover sizes, and "show" options that put helpful marks on the pages while you proofread. Turn all "show" options off before you make the final PDF.

### Preview Pane: Adjustment and Analysis Settings

The PDF Preview window: the auto-update delay, how far the right-click menu can shrink or expand text, and how **Layout Analysis** finds bad spaces, collisions and rivers. A river is a line of white space running down through several lines of text. Changes here take effect in the preview straight away. You can also reach these settings from the PDF Preview window: click the delay text next to **Auto-update**, or the analysis settings link.

### Automatic Page Filler

The page filler tool in the PDF Preview window stretches or shrinks paragraphs a little so each page is filled. These settings balance speed against how good the text looks. **The cost of imbalance in a polyglot slice** is only used for diglot and polyglot projects. See the PDF Preview chapter for how to use the tool.

### Other Miscellaneous Settings

Thumb tab text, the tilde (~) character, unwanted reference links from DBL text, and the space above the end-of-book decoration.

## Common tasks

### Apply a search-and-replace rule to the text (advanced)

1. On **Advanced** › **Main** › **Text Processing & Stylesheets**, tick **Apply Modifications to USFM Text (changes.txt)**.
2. Click **Edit...** next to it (or press Shift+Ctrl+C). `changes.txt` opens on the **View+Edit** tab.
3. Add one rule per line. A simple rule looks like `"old text" > "new text"`. The first quoted text is a regular expression, so some characters (such as `.` `(` `[` `\`) have a special meaning.
4. Save the file on the **View+Edit** tab.
5. Click **Print** and check the change in the PDF.

If PTXprint reports an error in the changes file, look at the last rule you added.

### Turn off a changes file or mods file without deleting it

1. Go to **Advanced** › **Main** › **Text Processing & Stylesheets**.
2. Untick the box for that file (for example **Apply Customized Settings (ptxprint-mods.tex)**).
3. Print again. The file stays on disk, so you can tick the box later to use it again.

### Print an interlinear text

1. In Paratext, make sure the interlinear glosses are approved.
2. Change to the **Full** view.
3. On **Advanced** › **Main** › **General**, tick **Interlinear**.
4. In the box next to it, type the gloss language code (for example `en`).
5. Tick **Ruby Text Above** if you want the glosses above the words.
6. Click **Print**.
7. To change the size or colour of the glosses, click the **\gloss|rb** link. For the base text, click **\rb**.

### Protect a finished layout

1. Change to the **Full** view.
2. On **Advanced** › **Main** › **General**, tick **Lock XeTeX Layout Level**. Future PTXprint updates will then use the same layout rules as now.
3. Tick **Lock UI Layout Settings**. The main layout, font and style controls are greyed out, so nobody changes them by accident.
4. Untick these boxes when you need to change the layout again.

### Find out which TeXpert settings have been changed

1. On the **Advanced** tab, click the **Other** sub-tab.
2. Click the filter button at the top. Only the groups with changed settings stay visible, and they open.
3. The bold labels are the changed settings.
4. Click the filter button again to show all groups.

### Put a TeXpert setting back to its default value

1. Find the setting on **Advanced** › **Other**. Its label is bold.
2. Number box: click the bold label. Check box: click the box. Drop-down list: choose the first item.
3. Check that the label is no longer bold, then print again.

### Start each book on a right-hand page

1. Go to **Advanced** › **Other** › **Page Layout and Spacing**.
2. Set **Where to start a new book** to **Odd page**.
3. Print. PTXprint adds blank pages where needed.

### Let books follow each other on the same page

1. Go to **Advanced** › **Other** › **Page Layout and Spacing**.
2. Set **Where to start a new book** to **Same page**.
3. If a book still starts on a new page when you do not want it to, increase **Page full factor** a little (for example from 0.65 to 0.75).

### Mark places that need attention while proofreading

1. Go to **Advanced** › **Other** › **PDF Options, Covers, Show/Hide**.
2. Tick **Show Error Bars For Overfull Lines** to see lines that are too long. Tick **Show USFM codes** to see which marker each paragraph uses.
3. Print and check the PDF.
4. Untick these options before you make the final PDF.

## Common problems

**The Advanced tab is missing.** It is only shown in the **Regular** and **Full** views. Change the view level (see the chapter on the main window).

**Some settings on the Main sub-tab are missing** (for example **Interlinear**, **Plugins**, **Process Text With Custom Script at**, or the locks). These are only shown in the **Full** view.

**An Edit... button is greyed out.** Tick the check box for that file first.

**My changes in changes.txt have no effect.** Make sure **Apply Modifications to USFM Text (changes.txt)** is ticked, the file is saved on the **View+Edit** tab, and you printed again. Check that the search text really matches the USFM text, including spaces and markers. Look at the Log tab for messages about the changes file.

**Printing fails after I edited a mods file.** Untick the box for the file you edited (for example **Apply Customized Settings (ptxprint-mods.tex)**) and print again. If the problem goes away, the error is in that file. Undo your last change in it.

**Interlinear printing says some references "need to be reapproved".** The glosses for those verses are not approved in the Paratext Interlinearizer. Approve them in Paratext and print again.

**Between Letters spacing is greyed out on the Fonts+Script tab.** **Interlinear** is ticked on the **Advanced** tab. The two cannot be used together.

**Layout, font and style controls are greyed out.** Untick **Lock UI Layout Settings** on **Advanced** › **Main** › **General** (**Full** view).

**Help links and the update check are missing.** **Disable ALL Internet Use** is ticked. Untick it to let PTXprint use the internet again.

**My PDF suddenly looks different but I did not change anything on the main tabs.** Someone may have changed a TeXpert setting. Open **Advanced** › **Other** and click the filter button to see the changed settings (bold labels). Also check whether a changes file or mods file is ticked on the **Main** sub-tab.

**Unbalanced Lines (Max) or the variable line spacing settings have no effect.** They only work when **Allow Unbalanced Columns** or **Fill Columns** is ticked on the **Layout** tab.

**I changed Use system fonts but nothing happened.** Close and restart PTXprint.

**Coloured marks or labels appear in the margins of my PDF.** One of the "show" options in **PDF Options, Covers, Show/Hide** is ticked (**Show adjust points**, **Mark Trigger Points**, **Show USFM codes**, **Show Error Bars For Overfull Lines**), or **Show Diglot Trace Marks** in the **Diglot** group. Untick it.

## Control notes

### @c_useModsTex
Anything in this file wins over PTXprint's own settings. Use it only when a support person or expert gives you something to put in it. If printing suddenly fails, untick this box first to see whether the file is the cause.

### @c_processScript
Use it for changes too complex for a changes file, such as converting the text to another writing system. Choose the program with **Select...** and when it runs with **start** or **end**. Experienced users only.

### @r_when2processScript_before
The script works on the original USFM text. Choose this when your changes-file rules expect the text that the script produces.

### @r_when2processScript_after
The script then sees the text almost exactly as it will be typeset.

### @btn_selectScript
Accepts .bat, .exe, .py or .sh. Choosing a file ticks **Process Text With Custom Script at** for you; cancelling without a file turns the option off. Hover over the button to see the chosen file.

### @c_usePrintDraftChanges
Use it to fix small problems in the text for printing only, such as spacing or punctuation. Your Paratext project is not changed. The rules are regular expressions, so test each new rule carefully.

### @btn_editChangesFile
`PrintDraftChanges.txt` opens in the next tab only if the project has one. Save there, then print again.

### @btn_editModsTeX
Save the file there and print again.

### @btn_editModsSty
Most style changes are easier and safer on the **Styles** tab.

### @c_useModsSty
Most people make style changes on the **Styles** tab instead.

### @c_useCustomSty
The same file Paratext uses for its own display. If the file does not exist, nothing changes.

### @btn_editCustomSty
The file is shared with Paratext, so a change here can also change how Paratext shows the text.

### @btn_editScript
Lets you read or change the chosen script. Only active when a script has been selected.

### @btn_editModsPreTex
Opens `ptxprint-premods.tex` for editing.

### @c_usePreModsTex
Most changes belong in `ptxprint-mods.tex` instead.

### @c_sensitive
Credits use short names (for example "DCC" instead of the artist's full name) where allowed. Tick it before you make any PDF that will be shared.

### @c_canonicalise
Fixes are made in a temporary copy. Serious errors show a "USFM Check Error" message with the book and the problem. Untick it only if a support person asks, for example to see whether the check itself causes a problem.

### @c_interlinear
Uses glosses from the Paratext Interlinearizer. You must also type the gloss language code in the box next to it. If some verses have unapproved glosses, PTXprint lists the references to approve in Paratext.

### @t_interlinearLang
Interlinear output only works when this box has a code.

### @c_ruby
Like ruby text in East Asian scripts. Only has an effect when **Interlinear** is ticked.

### @lb_style_rb
The base text is the words that carry glosses.

### @lb_style_gloss|rb
Change size, colour or spacing of the glosses there. Glosses are usually smaller than the base text.

### @c_useEngLinks
Useful where Google is blocked.

### @c_noInternet
Website links (for example on the **Help** tab) are hidden. Use it where internet use is expensive, slow or not safe. This setting belongs to your computer, not to the configuration.

### @t_plugins
Separate names with commas or spaces. PTXprint loads the plugins for ornaments, polyglot layouts and covers by itself when you use those features. Leave the box empty unless you know you need a plugin.

### @c_usePunctuation
Used with **Interlinear**: includes the punctuation stored in the Paratext interlinear data. When unticked, those punctuation entries are left out.

### @c_autoTagHebGrk
This avoids empty boxes in place of letters. Leave it ticked unless the project already marks these words itself. Hebrew words are not marked if the project itself uses the Hebrew script; the same applies to Greek.

### @c_lockXeTeXLayout
Ticking it sets **Maximum layout version** (**Other** › **Page Layout and Spacing**) to the current version, so later updates do not change how your pages break. Use it near the end of a project. Unticking it sets **Maximum layout version** back to 0 (newest rules).

### @c_lockUI4Layout
Greys out page size, margins, font size, line spacing, columns and gutters, and the whole **Fonts+Script** and **Styles** tabs. Untick it to make changes again.

### @c_testrecording
When you untick it (or save), PTXprint asks where to save the test zip file. Normal users do not need this.

### @l_advOther
The **Other** sub-tab label. The sub-tab holds the TeXpert settings in groups.

### @btn_texpertFilter
Inside the shown groups, only the changed settings are shown. The quickest way to see what has changed in a configuration. Only works while the **Other** sub-tab is shown.

### @s_ptxversion
Pages sometimes break differently after an update. A value here uses the layout rules of that older version. Normally set it with **Lock XeTeX Layout Level**, not by hand. Some settings depend on it; for example, from version 6 the enhanced paragraphed footnotes are always used.

### @c_linespacebase
For old projects only. Tick it if an old project's spacing changed after an update and you want the old spacing back.

### @fcb_bookstartpage
**Same page** saves paper. **Odd page** adds blank pages where needed. See also **Page full factor**.

### @s_pagefullfactor
The part of the page (0.65 = about two thirds). With **Same page**, if the previous book fills more than this, the next book goes to a new page. The same factor is used when single-column text (such as a book title or introduction) is followed by two-column text. A higher value lets more books share a page.

### @fcb_intropagealign
**No page breaks** lets the introduction follow on the same page. **Grouped** keeps adjacent introductions together and starts the group on an odd page.

### @s_bottomrag
How many lines the two columns may differ at the end of a page or section. 0 forces balanced columns.

### @s_interlinestretch
1 pt is about 0.35 mm. A larger value fills columns more easily, but the line spacing looks less even.

### @s_interlineshrink
Keep it small. Lines too close together are hard to read.

### @c_squashgrid
Keeps the tops of columns level. Untick it for the full space above every heading, even at the top of a column.

### @c_lastnoeject
Normally the last book ends with a page break, so a back-matter PDF starts on a new page. Tick this only to go back to the old behaviour.

### @s_notelineoffset
Notelines are turned on with **Notelines** on the **Layout** tab.

### @s_notelinemargin
A bigger value keeps the lines from being cut off when the pages are trimmed.

### @fcb_notelinetype
Dots are lighter and disturb the text less.

### @s_noteliney
0 makes the notelines match the text lines. Increase it if readers need more room to write.

### @s_notelinemajor
Thin lines (0.2 to 0.5) look best.

### @c_doublesided
When ticked, inner and outer margins swap on even pages and the even-page headers and footers are used. Untick it for one-sided printing: every page then uses the same margins and the odd-page header and footer.

### @s_maxproc
Also used when you print several publications. The default depends on the number of processors in your computer. Lower it if your computer becomes slow or runs out of memory.

### @s_maxfilltime
We could not confirm that the current code uses this. To limit page filler time, use **Time limit for the whole job (minutes)** in **Automatic Page Filler**.

### @fcb_vhyphenmode
For a verse range such as 3-4 shown as a marginal verse number. **Up on left** and **Up on right** put the hyphen on the first line only in the left or right margin. Marginal verses are turned on with **Marginal Verses** on the **Body** tab.

### @c_mverseismargin
Unticked, the column becomes narrower. Ticked, part of the space comes from the margin or the gutter (the space between columns), so the text keeps more width.

### @c_calcchapsize
Makes a large chapter number fill exactly two lines, when the `\c` style is not much larger than the body text. Untick it to set the size yourself on the **Styles** tab.

### @c_nohangvone
Untick it only if the after-chapter space is wide enough and you want verse 1 to hang like the others.

### @c_hangva
For alternative verse numbers (`\va`). Most projects do not use them.

### @s_afterchapterspace
0.25 = a quarter of the text size. Increase it if text looks crowded against the chapter number. Negative values move the text closer.

### @s_afterversespace
Change it only if verse numbers look too close to the text, or too far from it.

### @c_chapindent
Unticked, the lines next to a large chapter number (a cutout) are not indented. Tick it to keep the paragraph's normal indent there.

### @c_afterheadindent
Untick it to start the first line after a heading at the margin, a common book style.

### @s_maxorphanlength
An orphan word is a short word alone on the last line of a paragraph. With **Prevent Orphan Words** (**Body** tab), PTXprint keeps the last word with the word before it. Longer last words (in characters) can stand alone.

### @s_badsppen
PTXprint uses "bad" spaces, for example, to keep orphan words with the word before them. Higher = break less likely; 10000 forbids it. A negative value encourages a break.

### @s_optbkpen
The optional break is the place you mark with `//` in the USFM text. A higher value makes the break more attractive. Change it only if lines break there too often or too seldom.

### @s_pretolerance
Hyphenation is tried only for paragraphs that look bad without it. Lower values hyphenate more often. Only matters when hyphenation is on.

### @s_hyphenpenalty
Higher = fewer hyphens, but possibly wider word spaces. 10000 or more stops hyphenation completely.

### @s_doublehyphendemerits
Higher makes two hyphenated lines in a row rarer. The default is already high.

### @c_userefloc
Turns `\ref` references into links you can click in the PDF to jump to that verse.

### @c_hreflink
Untick it for a printed book where active links are not wanted.

### @fcb_urllinkborderstyle
The mark is only visible on screen; it is not printed. The link colour can only be changed by an expert, in `ptxprint-mods.tex`.

### @fcb_gotolinkborderstyle
For links inside the PDF, for example from a cross-reference to a verse. Not printed.

### @c_useglyphmetrics
Unticked, every line is measured the same way and spacing is even. Ticked, the real letter shapes in each line are used. Leave it unticked unless a support person suggests otherwise.

### @c_usesysfonts
Untick it to use only fonts stored with the project, so the result is the same on every computer.

### @s_underlinethickness
em = the size of the font. 0.05 is a thin line.

### @s_underlineposition
Descenders are the parts of letters like g and p that go below the baseline (the line letters sit on). Increase it if underlines touch the letters.

### @c_underlnsp
Ticked, the underline is unbroken. Untick it to underline only the words.

### @c_logfontusage
Useful for finding where an unexpected font comes from. It does not change the PDF. A support person may ask you to turn it on.

### @c_midnotes
For single-column text (for example an introduction) followed by two-column text. Ticked, the notes of the single-column part come right after it, mid-page. Unticked, all notes go to the bottom of the page.

### @c_fnotesdown
For the last page of a book, where the text may end high. Unticked, the notes follow straight after the text.

### @c_bookresetcallers
Untick it to continue the caller sequence (a, b, c …) across books.

### @c_neachbook
Untick it to collect all endnotes at the end of the last book.

### @c_newparnotes
Paragraphed footnotes run several notes together in one paragraph. With the current layout version this is always on; the box only matters when **Maximum layout version** is 5 or lower.

### @c_parntkillpd
Keeps the space between different note types even. Change it only to solve a specific spacing problem.

### @c_parntkilldepth
Ticked, the last line of paragraphed notes sits on the bottom margin. Unticked, space for letters below the baseline (such as g and p) is kept.

### @c_parntruletopskip
The footnote rule is the line above the notes. Unticked, it is placed relative to the height of the letters in the first note. Change it only if the space between rule and notes looks wrong.

### @c_parntmidtopskip
For the space between two note types (for example footnotes and cross-references). Ticked gives the same space everywhere. Untick it to measure from the letter height.

### @c_fnxugm
Unticked, the last line of notes is at the same height on every page. Ticked, notes sit as low as possible, which sometimes leaves room for an extra line of text.

### @s_lastnoteinterlinep
10000 = never split the last footnote across pages. Lower values allow a split, which can help fill pages with many notes.

### @s_lastnotewidowp
For a split that leaves only the last line on the next page. 10000 forbids it.

### @s_lastnoteclubp
For a split that leaves only the first line on the page. 10000 forbids it.

### @s_lastnoteparp
The default 100 allows a split at a note paragraph more easily than mid-paragraph.

### @s_nshaveshort
"Shaving" splits a note that does not fit and moves part to the next page. Shorter notes are kept whole.

### @s_nshavemin
Avoids moving a single lonely line.

### @s_nshavestay
Counts lines of all notes.

### @s_footnotemulsts
PTXprint guesses how much space study notes need while it collects text for a page. 1000 = 100%. Lower values can give fuller pages but more work; higher values can leave pages underfull. Change it only on advice.

### @s_footnotemulstt
Same as **Study note factor-Single column**, for two-column text.

### @s_footnotemulstd
Same as **Study note factor-Single column**, for diglot text.

### @s_footnotemuls
Same idea for ordinary footnotes. Change it only on advice.

### @s_footnotemult
Change it only on advice.

### @s_footnotemuld
Change it only on advice.

### @s_footnotemulc
For example cross-references between two columns. These notes do not take space from the text column, so the default is very low.

### @c_diglotbalnotes
Tick it to keep the bottoms of all columns level. Unticked, each column uses its own space.

### @c_mergednotesrtl
Tick it when the merged notes should read right-to-left. Getting this wrong arranges the notes badly, so match it to the language of the notes.

### @c_reversify
Keeps matching verses side by side. Leave it ticked unless the projects already use the same versification.

### @c_showvpvrse
Readers then see the verse numbers of their own translation.

### @c_showvpchap
The old chapter number is shown with the verse number.

### @c_vistrace
Marks where the column pieces are joined, to find layout problems. Turn it off for the final PDF.

### @c_vistracex
Debugging only; it can change the layout.

### @s_diglotcolourpad
Larger extends the shading further beyond the text. Negative values make it narrower than the text.

### @fcb_textbordermode
**Borders start at body text** leaves book introductions outside the border. **Borders include book intros** is the old behaviour. **Wide book intros for per-column textborders** is experimental: introductions use the full page width when each column has its own border.

### @s_growunprintable
Grown pages may extend into the bottom margin, so check them.

### @fcb_pagefulltest
We could not confirm that a change here reaches the typesetting code in the current version.

### @c_figleft
For two-column pictures with no usable position: PTXprint places them at the top of a column, alternating left and right. Ticked, it starts with the left column.

### @c_captreffirst
Puts the verse reference before the caption text.

### @c_captfirst
Puts the caption above the picture.

### @s_cutouterpadding
A cutout is a space cut into the side of the text. This value is used when a picture or sidebar does not set its own space. **Default space beside picture** sets the same value and wins when changed from its default.

### @s_captionadj
Negative values remove space, in points.

### @s_spbeside
Horizontal space, in points. Sets the same value as **Space (pt) beside cutout/sidebar**; when changed from its default (10), this one is used.

### @c_allpicredits
Lists every artist with all the pages of their pictures.

### @c_noactions
Bookmarks are the list of books and chapters in a PDF viewer's side panel. Some printers ask for a PDF without them.

### @c_actions
For example cross-references and web links. Untick it for a PDF only for printing.

### @c_refbkmks
Helps when book names are long or in a script the PDF viewer cannot show.

### @c_notransparent
For printers that cannot handle transparent colours. Each one becomes a solid colour that looks the same on white paper. Anything behind it is then hidden, so check pages with shading or overlapping pictures.

### @c_showadjpoints
Marks where paragraph adjustments (stretch or shrink from the adjustment list) apply. Turn it off for the final PDF.

### @c_mktrigpts
Triggers are instructions tied to a verse, such as a picture position or a style change. Turn it off for the final PDF.

### @c_showusfmcodes
Helps you find which style to change on the **Styles** tab. Turn it off for the final PDF.

### @c_showhboxerrorbars
A black bar at the end of every overfull line. Fix such lines, for example with hyphenation or small text changes. Then turn this off.

### @s_spineoverlapback
Helps hide small errors when the cover is folded. Used when you make a cover on the **Peripherals** tab.

### @s_spineoverlapfront
Used when you make a cover.

### @s_bleed
Ask your printer how much bleed they need; often 3 to 5 mm.

### @s_artbleed
Leave it at 0 for soft covers. Ask your printer for the right value.

### @s_autoupdatedelay
A right-click adjustment with **Auto-update** on starts a new print after this delay, so you can make several adjustments first. Increase it if you need more time between adjustments.

### @s_shrinktextstep
Percent per "shrink text" step.

### @s_shrinktextlimit
95 = at most 5% smaller. The page filler also uses this limit. Shrinking too much makes text look crowded.

### @s_expandtextstep
Percent per "expand text" step.

### @s_expandtextlimit
105 = at most 5% larger.

### @s_spaceEms
Used by **Layout Analysis** in the PDF Preview window; em = the size of the font. A lower value marks more spaces.

### @s_charSpaceEms
Only used when **Between Letters** spacing is on (**Fonts+Script** tab).

### @c_collisionPrecise
Finds fewer false collisions.

### @s_paddingwidth
For boxes around letters on different lines. A larger value reports more possible collisions.

### @s_riverthreshold
Increase it to report only the worst rivers.

### @s_riverminmaxwidth
In em.

### @s_riverminwidth
Narrower spaces are not counted as part of a river.

### @s_rivergap
In em.

### @s_riveroverlap
For two spaces on lines above each other.

### @s_pbtimeout
0 means no time limit. Increase it for a long Bible if the longest book does not finish.

### @s_pbbacktrack
How many earlier pages the page filler may go back to try a different layout.

### @s_pbmaxr
Keep it low unless many pages fail.

### @s_pbspacingtol
As a part of the text size.

### @s_pbexpbad
Higher values give more even text.

### @s_pbexpcost
Applies when both shrinking and stretching would work.

### @s_pbcontrast
Higher values give a more even page.

### @s_pbpolyimbalance
The page filler works on slices: pieces of text that belong together across the columns, such as the same verses in each language. A slice is unbalanced when one column ends lower than another. This sets how much to avoid that, compared with stretching or shrinking paragraphs. Higher: columns end more evenly, but paragraphs may change more. Lower: paragraphs look more even, but one column may end a few lines lower. Change it only if your diglot columns are often uneven after page filling.

### @c_tocthreetab
`\toc3` is the short book name. Thumb tabs are set on the **Tabs+Borders** tab.

### @c_tildenbsp
A non-breaking space looks like a normal space, but the line never breaks there. Untick it only if your text needs a real tilde.

### @c_removextreflinks
These `\ref` links inside cross-references come from Digital Bible Library (DBL) text. Only their visible text is kept.

### @s_bedskip
In points. The decoration is turned on in **Ornamental Decorations** on the **Tabs+Borders** tab. Negative values move it up.

### @s_thumbvvadj
Moves the text on rotated thumb tabs (in points) to centre it on the tab. Thumb tabs and **Rotate Tabs** are on the **Tabs+Borders** tab.

### @s_marginnotesgap
A larger number moves margin notes further from the text. Margin notes are turned on, and their width set, on the **Layout** tab, **Page Setup** area (**Margin Notes Col Width (mm)** and **Margin Notes on Left/Inner**).
