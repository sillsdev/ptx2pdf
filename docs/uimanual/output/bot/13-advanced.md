# 16. Advanced tab

## 16.1 What this tab is for

The **Advanced** tab holds settings for experienced users. Most people never need it. Come here when another tab cannot give you the result you need, or when the support team asks you to change a specific setting.

The tab has two sub-tabs:

* **Main** – ways to change the text before it is typeset (a changes file, a processing script), extra stylesheets and TeX settings files, interlinear output, plugins, internet use, and locks that protect a finished layout.
* **Other** – about 125 "TeXpert" settings: fine controls for the typesetting engine, sorted into groups such as **Page Layout and Spacing** or **Footnotes, Cross-references, Study Notes**.

The tab is only shown in the **Regular** and **Full** views. Some **Main** settings are only shown in the **Full** view (noted below).

## 16.2 Before you change anything here

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

## 16.3 Main sub-tab: Text Processing & Stylesheets

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

## 16.4 Main sub-tab: General

Settings that do not fit anywhere else:

* **Sensitive Project** – shortens picture credits and keeps private data out of the PDF.
* **Auto-Correct USFM** – fixes common USFM mistakes and warns about serious ones. Leave it ticked.
* **Interlinear** – prints Paratext interlinear glosses under (or above) each word. (**Full** view only.)
* **Auto-tag Hebrew and Greek words** – marks these words so they use the right font.
* **Only Use English Links** and **Disable ALL Internet Use** – how PTXprint uses the internet.
* **Plugins** – loads extra parts of the typesetting code for special features. (**Full** view only.)
* **Lock XeTeX Layout Level** and **Lock UI Layout Settings** – protect a finished layout from changes. (**Full** view only.)

## 16.5 Main sub-tab: Capture tests?

Only shown in the **Full** view. A developer tool that records what you click to make an automatic test. Normal users do not need it.

## 16.6 Other sub-tab: the TeXpert settings

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

## 16.7 Common tasks

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

## 16.8 Common problems

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

## 16.9 Settings reference

### Advanced

#### Other

Label · Regular+ · `l_advOther`

> To balance columns of text on a page it is possible to specify paragraphs adjustments (shrink or expand):
>
> A Paragraph Adjust List needs to be in this format:  
> MRK 2.7 +1    (i.e. expand the para at Mark 2.7 by one line) MRK 3.20 -1   (i.e. shrink the para at Mark 3:20 by one line) %MARK 4.14 +1   (ignore this line - treat it as a comment) MRK 5.8 +2    (i.e. expand the para at Mark 5.8 by two lines) MRK 6.23 +1[2]  (expand the paragraph AFTER the paragraph  
>                               which contains MRK 6.23 e.g. a heading.) etc. Note that adjusting paragraphs needs to be done right at the end when all other settings have been finalized. Otherwise you are likely to have to re-do it all again.

The **Other** sub-tab label. The sub-tab holds the TeXpert settings in groups.

#### Filter: show only sections with non-default settings. Sectio...

Toggle, off · Regular+ · `btn_texpertFilter`

> Filter: show only sections with non-default settings. Sections where all values are default will be hidden. Sections with changed values will be expanded. Disable to restore all sections in collapsed state.

Inside the shown groups, only the changed settings are shown. The quickest way to see what has changed in a configuration. Only works while the **Other** sub-tab is shown.

#### Main

##### Text Processing & Stylesheets

###### Apply Customized Settings (ptxprint-mods.tex)

Checkbox, off · Regular+ · `c_useModsTex` · cfg `project/ifusemodstex`  
Also: Apply customized TeX settings

> This is the normal file for advanced users to configure TeX. This .tex file executes AFTER all the PTXprint settings.

Anything in this file wins over PTXprint's own settings. Use it only when a support person or expert gives you something to put in it. If printing suddenly fails, untick this box first to see whether the file is the cause.

###### Process Text With Custom Script at

Checkbox, off · Full · `c_processScript` · cfg `project/processscript`

> Processes the .usfm file through a program of your choosing. The program is run as `prog infile outfile` where infile is the source .usfm file and outfile the output .usfm that will then be typeset.

Use it for changes too complex for a changes file, such as converting the text to another writing system. Choose the program with **Select...** and when it runs with **start** or **end**. Experienced users only.

###### start

Radio · Full · `r_when2processScript_before` · cfg `project/when2processscript=before`  
Needs: “Process Text With Custom Script at”

> Execute processing script BEFORE running any printdraftchanges, canonicalisation (i.e. Auto-Correct USFM) or local changes which are all specified below.

The script works on the original USFM text. Choose this when your changes-file rules expect the text that the script produces.

###### end

Radio · Full · `r_when2processScript_after` · cfg `project/when2processscript=after`  
Needs: “Process Text With Custom Script at”

> Execute processing script AFTER running any printdraftchanges, canonicalisation (i.e. Auto-Correct USFM) or local changes which are all specified below.

The script then sees the text almost exactly as it will be typeset.

###### Select...

Button · Full · `btn_selectScript` · cfg `project/selectscript`  
Also: Select custom script · Needs: “Process Text With Custom Script at”

Accepts .bat, .exe, .py or .sh. Choosing a file ticks **Process Text With Custom Script at** for you; cancelling without a file turns the option off. Hover over the button to see the chosen file.

###### Apply Modifications to USFM Text (changes.txt)

Checkbox, off · Regular+ · `c_usePrintDraftChanges` · cfg `project/usechangesfile`  
Also: Enable changes.txt to be applied

> If there are changes that you wish to apply to the USFM file(s) prior to producing the printout, then these can be specified in these files:
>
> changes.txt - is used for changes that only apply to the current configuration;
>
> PrintDraftChanges.txt - specifies changes which apply to all configurations, and gets 'included' at the top of changes.txt

Use it to fix small problems in the text for printing only, such as spacing or punctuation. Your Paratext project is not changed. The rules are regular expressions, so test each new rule carefully.

###### Edit...

Button · Regular+ · `btn_editChangesFile`  
Also: Edit changes files · Needs: “Apply Modifications to USFM Text (changes.txt)”

> Switch to the View+Edit tab to show the Changes.txt file in one tab, and PrintDraftChanges.txt in the next tab to the right.
>
> Shortcut: Shift-Ctrl-C

`PrintDraftChanges.txt` opens in the next tab only if the project has one. Save there, then print again.

###### Edit...

Button · Regular+ · `btn_editModsTeX`  
Also: Edit customized TeX settings · Needs: “Apply Customized Settings (ptxprint-mods.tex)”

> Switch to the View+Edit tab to show the ptxprint-mods.tex file.
>
> Shortcut: Shift-Ctrl-T

Save the file there and print again.

###### Edit...

Button · Full · `btn_editModsSty`  
Also: Edit stylesheet overrides · Needs: “Apply Stylesheet Overrides (ptxprint-mods.sty)”

> Switch to the View+Edit tab to show the ptxprint-mods.sty file.
>
> Shortcut: Shift-Ctrl-S

Most style changes are easier and safer on the **Styles** tab.

###### Apply Stylesheet Overrides (ptxprint-mods.sty)

Checkbox, off · Full · `c_useModsSty` · cfg `project/ifusemodssty`

> It is recommended to leave this option unchecked (off) unless you have intentionally customized styles using the ptxprint-mods.sty stylesheet and wish for these to be used by PTXprint.

Most people make style changes on the **Styles** tab instead.

###### Apply Customized Styles (custom.sty)

Checkbox, off · Full · `c_useCustomSty` · cfg `project/ifusecustomsty`  
Also: Apply custom styles

> It is recommended to leave this option unchecked (off) unless you have intentionally customized styles using the custom.sty stylesheet and wish for these to be used by PTXprint.

The same file Paratext uses for its own display. If the file does not exist, nothing changes.

###### Edit...

Button · Full · `btn_editCustomSty`  
Also: Edit custom styles · Needs: “Apply Customized Styles (custom.sty)”

> Switch to the View+Edit tab to show the custom.sty file.
>
> Shortcut: Shift-Ctrl-M

The file is shared with Paratext, so a change here can also change how Paratext shows the text.

###### Edit...

Button · Full · `btn_editScript`  
Also: Edit custom script · Needs: “Process Text With Custom Script at”

> Edit the processing script

Lets you read or change the chosen script. Only active when a script has been selected.

###### Edit...

Button · Full · `btn_editModsPreTex`  
Also: Edit initial TeX settings · Needs: “Apply Initial Settings (ptxprint-premods.tex)”

> Switch to the View+Edit tab to show the ptxprint-premods.tex file.
>
> Shortcut: Shift-Ctrl-P

Opens `ptxprint-premods.tex` for editing.

###### Apply Initial Settings (ptxprint-premods.tex)

Checkbox, off · Full · `c_usePreModsTex` · cfg `project/ifusepremodstex`  
Also: Apply initial TeX settings

> This .tex file is executed BEFORE any stylesheets of other settings are applied. This file is rarely used.

Most changes belong in `ptxprint-mods.tex` instead.

##### General

###### Sensitive Project

Checkbox, off · Regular+ · `c_sensitive` · cfg `document/sensitive`

> In sensitive locations the illustration copyright statement(s) can just contain the appropriate acronyms (e.g. BFBS or DCC) for some artists.
>
> In addition, the PDF's metadata will not contain sensitive project-specific data.

Credits use short names (for example "DCC" instead of the artist's full name) where allowed. Tick it before you make any PDF that will be shared.

###### Auto-Correct USFM

Checkbox, on · Regular+ · `c_canonicalise` · cfg `project/canonicalise`  
Also: Auto-correct common USFM syntax errors

> PTXprint can analyze the USFM files and automatically correct some common errors in syntax. It will also notify you of errors which are likely to cause the print process to fail - giving you helpful feedback about how to fix the issue before re-trying to print.

Fixes are made in a temporary copy. Serious errors show a "USFM Check Error" message with the book and the problem. Untick it only if a support person asks, for example to see whether the check itself causes a problem.

###### Interlinear  &  Code

Checkbox, off · Full · `c_interlinear` · cfg `project/interlinear`  
Also: Interlinear settings

> Convert Paratext's interlinear data text to ruby (glossing) so that an interlinear text can be printed.
>
> Note that  you may need to adjust the following marker styles:  
>   \rb    for the base text  
>   \gloss|rb    for the gloss text
>
> Note that if this Interlinear option is enabled, then the Spacing Adjustments Between Letters (on the Fonts+Scripts page) will be disabled as these two settings are mutually exclusive.

Uses glosses from the Paratext Interlinearizer. You must also type the gloss language code in the box next to it. If some verses have unapproved glosses, PTXprint lists the references to approve in Paratext.

###### Interlinear language code to use. To find which code to use,...

Text box · Full · `t_interlinearLang` · cfg `project/interlang`

> Interlinear language code to use. To find which code to use, look in the project folder for a folder named "Interlinear_xy" where xy is the language code. For example if the interlinear has been glossed into English, then the code would be "en".

Interlinear output only works when this box has a code.

###### Ruby Text Above

Checkbox, off · Full · `c_ruby` · cfg `project/ruby`  
Also: Place Ruby text above words

> Treat ruby text as ruby rather than interlinear text by placing it above the base text rather than below.
>
> Note that  you may need to adjust the following marker styles:  
>   \rb    for the base text  
>   \gloss|rb    for the gloss text Use the shortcut links on the right to locate those styles in the editor.

Like ruby text in East Asian scripts. Only has an effect when **Interlinear** is ticked.

###### \rb

Link · Full · `lb_style_rb`

> Click to jump to the \rb marker in the style editor to change the formatting of the ruby text.

The base text is the words that carry glosses.

###### \gloss|rb

Link · Full · `lb_style_gloss|rb`

> Click to jump to the \gloss|rb marker in the style editor to change the formatting of the glosses for interlinear/ruby text.

Change size, colour or spacing of the glosses there. Glosses are usually smaller than the base text.

###### Only Use English Links

Checkbox, off · Regular+ · `c_useEngLinks`  
Also: Only use English links (do not G-translate) · Greyed out by: “Disable ALL Internet Use”

> When using a non-English interface (such as French, Spanish, Hindi, etc.) most links to external websites get sent via the Google Translate site so that you can read the information in the same language as the selected interface.
>
> Enable this option if Google is blocked in your country, or you simply prefer to read the original page in English.

Useful where Google is blocked.

###### Disable ALL Internet Use

Checkbox, off · Regular+ · `c_noInternet`  
Also: Disable internet use

> PTXprint checks for program updates and also contains links to external sites (mainly from the Styles tab and the Help tab). If this is an issue, then check this option to prevent PTXprint from accessing the internet.

Website links (for example on the **Help** tab) are hidden. Use it where internet use is expensive, slow or not safe. This setting belongs to your computer, not to the configuration.

###### Plugins – List of plugins

Text box · Full · `t_plugins` · cfg `project/plugins`

> Some advanced features load extra code that is not normally needed. List them here if you need to use them. For example, if you are generating a QR code, then you need to add qr to the list of plugins. For a polyglot, you can add polyglot-simplepages

Separate names with commas or spaces. PTXprint loads the plugins for ornaments, polyglot layouts and covers by itself when you use those features. Leave the box empty unless you know you need a plugin.

###### Use Interlinear Punctuation

Checkbox, off · Full · `c_usePunctuation` · cfg `project/interpunc`  
Also: Place Ruby text above words

> Include specifically modified interlinearized punctuation.

Used with **Interlinear**: includes the punctuation stored in the Paratext interlinear data. When unticked, those punctuation entries are left out.

###### Auto-tag Hebrew and Greek words

Checkbox, on · Regular+ · `c_autoTagHebGrk` · cfg `project/autotaghebgrk`

> Auto-tag Hebrew words \wh ... \wh* and Greek words with  \wg ... \wg*
>
> PTXprint can automatically tag all source language words (Hebrew and Greek) with the appropriate markup to ensure they display with the right font and direction for that script.

This avoids empty boxes in place of letters. Leave it ticked unless the project already marks these words itself. Hebrew words are not marked if the project itself uses the Hebrew script; the same applies to Greek.

###### Lock XeTeX Layout Level

Checkbox, off · Full · `c_lockXeTeXLayout` · cfg `config/lockxetexlayout`  
Also: Lock XeTeX Layout Settings

> This feature enables final typesetting to proceed with minimal risk of change to the final layout by locking the TeX macros to use the current layout logic, which will prevent newer functionality from taking effect in the future. This sets the "Maximum Layout Version" value in the TeXpert Hacks section.

Ticking it sets **Maximum layout version** (**Other** › **Page Layout and Spacing**) to the current version, so later updates do not change how your pages break. Use it near the end of a project. Unticking it sets **Maximum layout version** back to 0 (newest rules).

###### Lock UI Layout Settings

Checkbox, off · Full · `c_lockUI4Layout` · cfg `config/lockui4layout`

> This feature enables final typesetting to proceed with minimal risk of change to the final layout by disabling various controls (on the layout, fonts and styles tabs) so that settings can't be accidentally changed while doing final page layout.

Greys out page size, margins, font size, line spacing, columns and gutters, and the whole **Fonts+Script** and **Styles** tabs. Untick it to make changes again.

##### Capture tests?

###### Test recording in progress

Checkbox, off · Full · `c_testrecording`  
Also: Sensitive project

> Record PTXPrint options clicked for use in creating an automated test.
>
> Will stop recording when Save is pressed or the checkbox is unticked and a dialog will allow saving the test in zip format.

When you untick it (or save), PTXprint asks where to save the test zip file. Normal users do not need this.

#### Other

##### Page Layout and Spacing

###### Maximum layout version

Number · Regular+ · `s_ptxversion` · cfg `texpert/ptxversion`  
Values: 0–10 (default 0)

> Maximum layout version to use or 0 for any. Used to maintain backward compatibility when the TeX macros have been changed in newer versions of PTXprint.

Pages sometimes break differently after an update. A value here uses the layout rules of that older version. Normally set it with **Lock XeTeX Layout Level**, not by hand. Some settings depend on it; for example, from version 6 the enhanced paragraphed footnotes are always used.

###### Legacy 1/14 LineSpacing

Checkbox, off · Regular+ · `c_linespacebase` · cfg `texpert/linespacebase`

> In the past, SpaceAbove and SpaceBelow were, in effect units of 1/14 of the base line spacing. This has changed so they are now in units of 1/12 of the base line spacing. Enabling this compatibility reverts the units.

For old projects only. Tick it if an old project's spacing changed after an update and you want the old spacing back.

###### Where to start a new book

Drop-down · Regular+ · `fcb_bookstartpage` · cfg `texpert/bookstartpage`  
Choices: Next page | Same page | Odd page

> Does a scripture book start on a new page, the same page as the previous book (if <65% of page has been used), or an odd page

**Same page** saves paper. **Odd page** adds blank pages where needed. See also **Page full factor**.

###### Page full factor

Number · Regular+ · `s_pagefullfactor` · cfg `texpert/pagefullfactor`  
Values: 0.3–0.9 (default 0.65)

> This setting is related to how full a page needs to be to force the next book to start on a new page.

The part of the page (0.65 = about two thirds). With **Same page**, if the previous book fills more than this, the next book goes to a new page. The same factor is used when single-column text (such as a book title or introduction) is followed by two-column text. A higher value lets more books share a page.

###### Where to start a new intro page

Drop-down · Regular+ · `fcb_intropagealign` · cfg `texpert/intropagealign`  
Choices: Next page | No page breaks | On an odd page | Grouped

> Does an intro page start on a new page, the same page as the previous book, an odd page, or group all adjacent intro pages into an odd paged group

**No page breaks** lets the introduction follow on the same page. **Grouped** keeps adjacent introductions together and starts the group on an odd page.

###### Unbalanced Lines (Max)

Number · Regular+ · `s_bottomrag` · cfg `texpert/bottomrag`  
Values: 0–10 (default 3)

> Maximum number of unbalanced lines allowed in 2-column layout. Recommended range 1-5.

How many lines the two columns may differ at the end of a page or section. 0 forces balanced columns.

###### Variable line spacing maximum stretch

Number · Regular+ · `s_interlinestretch` · cfg `texpert/interlinestretch`  
Values: 0–10 (default 2)

> Maximum stretch to insert between lines in variable line spacing in pts

1 pt is about 0.35 mm. A larger value fills columns more easily, but the line spacing looks less even.

###### Variable line spacing maximum shrink

Number · Regular+ · `s_interlineshrink` · cfg `texpert/interlineshrink`  
Values: 0–3 (default 0.3)

> Maximum shrink to insert between lines in variable line spacing in pts

Keep it small. Lines too close together are hard to read.

###### No Top Space

Checkbox, on · Regular+ · `c_squashgrid` · cfg `texpert/squashgrid`

> Don’t insert space above headings at the start of a column

Keeps the tops of columns level. Untick it for the full space above every heading, even at the top of a column.

###### Suppress pagebreak after bookend-final

Checkbox, off · Regular+ · `c_lastnoeject` · cfg `texpert/lastnoeject`

> Revert to old behaviour of not ensuring that the whole of the last book is output before back-matter PDFs

Normally the last book ends with a page break, so a back-matter PDF starts on a new page. Tick this only to go back to the old behaviour.

###### Noteline offset (mm)

Number · Regular+ · `s_notelineoffset` · cfg `texpert/notelineoffset`  
Values: 0–100 (default 3)

> Gap (mm) between noteline and text

Notelines are turned on with **Notelines** on the **Layout** tab.

###### Noteline margin (mm)

Number · Regular+ · `s_notelinemargin` · cfg `texpert/notelinemargin`  
Values: 0–100 (default 10)

> Gap (mm) between noteline and edge of page

A bigger value keeps the lines from being cut off when the pages are trimmed.

###### Noteline type

Drop-down · Regular+ · `fcb_notelinetype` · cfg `texpert/notelinetype`  
Choices: Solid line | Row of dots

> Sometimes it is preferable to use a series of dots rather than a solid line.

Dots are lighter and disturb the text less.

###### Noteline spacing (mm)

Number · Regular+ · `s_noteliney` · cfg `texpert/noteliney`  
Values: 0–25 (default 0)

> Line spacing between notelines. When set to 0.00 the default line spacing of the document is used.

0 makes the notelines match the text lines. Increase it if readers need more room to write.

###### Noteline width (major)

Number · Regular+ · `s_notelinemajor` · cfg `texpert/notelinemajor`  
Values: 0–10 (default 0.5)

> Thickness (pt) of major notelines. Specify the colour on the Layout page.

Thin lines (0.2 to 0.5) look best.

###### Double Sided Layout

Checkbox, on · Regular+ · `c_doublesided` · cfg `texpert/doublesided`

> This setting can be disabled to turn off inner/outer margins, forcing the inner/outer gutter, and Notelines to always appear on the same side of the printed page.

When ticked, inner and outer margins swap on even pages and the even-page headers and footers are used. Untick it for one-sided printing: every page then uses the same margins and the odd-page header and footer.

###### Maximum parallel processes

Number · Regular+ · `s_maxproc` · cfg `texpert/maxproc`

> The maximum number of parallel processes to use for example when page filling

Also used when you print several publications. The default depends on the number of processors in your computer. Lower it if your computer becomes slow or runs out of memory.

###### Maximum Filling Time (mins)

Number · Regular+ · `s_maxfilltime` · cfg `texpert/maxfilltime`  
Values: 0–100 (default 0)

> Stop page filling a book after this many minutes

We could not confirm that the current code uses this. To limit page filler time, use **Time limit for the whole job (minutes)** in **Automatic Page Filler**.

##### Chapter and Verse

###### Position of marginal verse hyphen if any

Drop-down · Regular+ · `fcb_vhyphenmode` · cfg `texpert/vhyphenmode`  
Choices: Always down | Always up | Up on left | Up on right | No hyphens

> Insert or not a marginal verse hyphen in verse ranges, whether on the first or second line

For a verse range such as 3-4 shown as a marginal verse number. **Up on left** and **Up on right** put the hyphen on the first line only in the left or right margin. Marginal verses are turned on with **Marginal Verses** on the **Body** tab.

###### Gutter space reduction for marginal verses

Checkbox, off · Regular+ · `c_mverseismargin` · cfg `texpert/mverseismargin`

> If false, the space for marginal verses is taken from the column. If true, some space for marginal verses is taken from the margins or rule gutter

Unticked, the column becomes narrower. Ticked, part of the space comes from the margin or the gutter (the space between columns), so the text keeps more width.

###### Auto Calc Optimum Chapter Size

Checkbox, on · Regular+ · `c_calcchapsize` · cfg `texpert/calcchapsize`

> Attempt to automatically calculate drop chapter number size

Makes a large chapter number fill exactly two lines, when the `\c` style is not much larger than the body text. Untick it to set the size yourself on the **Styles** tab.

###### Don't hang verse one beside a chapter (in poetry)

Checkbox, on · Regular+ · `c_nohangvone` · cfg `texpert/nohangvone`

> Hanging verses into a chapter number can result in clashes, depending on the after-chapter space. If so, then turn off hanging verse numbers for the first verse (in poetry only).

Untick it only if the after-chapter space is wide enough and you want verse 1 to hang like the others.

###### Alternate verse numbers also hang

Checkbox, off · Regular+ · `c_hangva` · cfg `texpert/hangva`

> If there is an alternative verse and the current verse is hanging, does the alternate hang?

For alternative verse numbers (`\va`). Most projects do not use them.

###### After chapter space factor

Number · Regular+ · `s_afterchapterspace` · cfg `texpert/afterchapterspace`  
Values: -0.2–1 (default 0.25)

> This sets the gap between the chapter number and the text following. The setting here is a multiple of the main body text size as specified in layout.

0.25 = a quarter of the text size. Increase it if text looks crowded against the chapter number. Negative values move the text closer.

###### After verse space factor

Number · Regular+ · `s_afterversespace` · cfg `texpert/afterversespace`  
Values: -0.2–1 (default 0.15)

> This sets the gap between the verse number and the text following. The setting here is a multiple of the main body text size as specified in layout.

Change it only if verse numbers look too close to the text, or too far from it.

##### Body Text

###### Allow Indent Para with Cutouts

Checkbox, off · Regular+ · `c_chapindent` · cfg `texpert/chapindent`

> Allow indented paragraphs at chapter start with cutouts

Unticked, the lines next to a large chapter number (a cutout) are not indented. Tick it to keep the paragraph's normal indent there.

###### Allow Indent Para After Heading

Checkbox, on · Regular+ · `c_afterheadindent` · cfg `texpert/afterheadindent`

> Allow indented paragraphs following a heading

Untick it to start the first line after a heading at the margin, a common book style.

###### Maximum orphan word length

Number · Regular+ · `s_maxorphanlength` · cfg `texpert/maxorphanlength`  
Values: 1–20 (default 8)

> Maximum length of the word that will receive orphan protection at the end of a paragraph

An orphan word is a short word alone on the last line of a paragraph. With **Prevent Orphan Words** (**Body** tab), PTXprint keeps the last word with the word before it. Longer last words (in characters) can stand alone.

###### Bad space penalty

Number · Regular+ · `s_badsppen` · cfg `texpert/badsppen`  
Values: -10000–10000 (default 100)

> Penalty for a bad (but not impossible) place to break

PTXprint uses "bad" spaces, for example, to keep orphan words with the word before them. Higher = break less likely; 10000 forbids it. A negative value encourages a break.

###### Optional break penalty

Number · Regular+ · `s_optbkpen` · cfg `texpert/optbkpen`  
Values: 0–10000 (default 300)

> Penalty for the optional break

The optional break is the place you mark with `//` in the USFM text. A higher value makes the break more attractive. Change it only if lines break there too often or too seldom.

###### Hyphenation threshold

Number · Regular+ · `s_pretolerance` · cfg `texpert/pretolerance`  
Values: -1–10000 (default 100)

> Paragraph badness threshold before trying hyphenation. Set to -1 to always hyphenate

Hyphenation is tried only for paragraphs that look bad without it. Lower values hyphenate more often. Only matters when hyphenation is on.

###### Penalty for inserting hyphen

Number · Regular+ · `s_hyphenpenalty` · cfg `texpert/hyphenpenalty`  
Values: -9999–10000 (default 50)

> Hyphenation penalty

Higher = fewer hyphens, but possibly wider word spaces. 10000 or more stops hyphenation completely.

###### Double hyphenation penalty

Number · Regular+ · `s_doublehyphendemerits` · cfg `texpert/doublehyphendemerits`  
Values: 0–1e+06 (default 10000)

> Penalty for consecutive hyphenation across two lines

Higher makes two hyphenated lines in a row rarer. The default is already high.

###### Use loc attrib on ref to make a link

Checkbox, on · Regular+ · `c_userefloc` · cfg `texpert/userefloc`

> The ref character style can include an attribute like loc="GEN 1:2". Should this be used to make a clickable link?

Turns `\ref` references into links you can click in the PDF to jump to that verse.

###### Use href-link attrib on jmp to make a link

Checkbox, on · Regular+ · `c_hreflink` · cfg `texpert/hreflink`

> The jmp character style can include an attribute like href-link="https://my.web.site/". Should this be used to make a clickable link?

Untick it for a printed book where active links are not wanted.

###### Box style for URL links

Drop-down · Regular+ · `fcb_urllinkborderstyle` · cfg `texpert/urllinkborderstyle`  
Choices: Underline only | No line | Solid line | Row of dots | Dashed line | Viewer default

> Active web links in PDFs are marked by either a box (solid, dashed or dotted line) or an underline. Your viewer probably has a default setting. Set the colour with \def\URLLinkBorderCol{0.9 0.5 0.5} or similar in ptxprint-mods.tex.

The mark is only visible on screen; it is not printed. The link colour can only be changed by an expert, in `ptxprint-mods.tex`.

###### Box style for GOTO links

Drop-down · Regular+ · `fcb_gotolinkborderstyle` · cfg `texpert/gotolinkborderstyle`  
Choices: Underline only | No line | Solid line | Row of dots | Dashed line | Viewer default

> Active internal links in PDFs are marked by either a box (solid, dashed or dotted line) or an underline. Your viewer probably has a default setting. Set the colour with \def\GOTOLinkBorderCol{0.9 0.5 0.5} or similar in ptxprint-mods.tex.

For links inside the PDF, for example from a cross-reference to a verse. Not printed.

##### Fonts and Underline

###### Use glyph metrics

Checkbox, off · Regular+ · `c_useglyphmetrics` · cfg `texpert/useglyphmetrics`

> PTXprint can use either the actual glyph metrics in a line or the font metrics to calculate line heights and depths. Font metrics gives more consistent results.

Unticked, every line is measured the same way and spacing is even. Ticked, the real letter shapes in each line are used. Leave it unticked unless a support person suggests otherwise.

###### Use system fonts

Checkbox, on · Regular+ · `c_usesysfonts` · cfg `texpert/usesysfonts`

> Use fonts from your system as well as your project. Note that you need to restart PTXprint for this setting to take effect.

Untick it to use only fonts stored with the project, so the result is the same on every computer.

###### Underline thickness (em)

Number · Regular+ · `s_underlinethickness` · cfg `texpert/underlinethickness`  
Values: 0.01–0.5 (default 0.05)

> This sets the thickness of the text underline, (measured in ems).

em = the size of the font. 0.05 is a thin line.

###### Underline vertical position (em)

Number · Regular+ · `s_underlineposition` · cfg `texpert/underlineposition`  
Values: -1–1 (default 0.1)

> This sets how far (in ems) the underline is below the text and what it is relative to. If negative, it is the distance below the baseline. If positive (or zero), it is the distance below the bottom of any descenders.

Descenders are the parts of letters like g and p that go below the baseline (the line letters sit on). Increase it if underlines touch the letters.

###### Underline Spaces

Checkbox, on · Regular+ · `c_underlnsp` · cfg `texpert/underlnsp`

> Underline spaces in underlined runs

Ticked, the underline is unbroken. Untick it to underline only the words.

###### Log font creation

Checkbox, off · Regular+ · `c_logfontusage` · cfg `texpert/logfontusage`

> Create <jobname>.fontusage in the local/ptxprint/<config>/ directory, which will list the page number and exact font definition when each new style is first used.

Useful for finding where an unexpected font comes from. It does not change the PDF. A support person may ask you to turn it on.

##### Footnotes, Cross-references, Study Notes

###### Mid-Page Footnotes

Checkbox, off · Regular+ · `c_midnotes` · cfg `texpert/midnotes`

> Should footnotes go before a single-double column transition

For single-column text (for example an introduction) followed by two-column text. Ticked, the notes of the single-column part come right after it, mid-page. Unticked, all notes go to the bottom of the page.

###### Final Page Notes Down

Checkbox, off · Regular+ · `c_fnotesdown` · cfg `texpert/fnotesdown`

> Push notes on the final page to the bottom of the page

For the last page of a book, where the text may end high. Unticked, the notes follow straight after the text.

###### Reset Callers at Each Book

Checkbox, on · Regular+ · `c_bookresetcallers` · cfg `texpert/bookresetcallers`

> Re-start the footnote and cross-reference callers at the start of each book

Untick it to continue the caller sequence (a, b, c …) across books.

###### Endnotes at Each Book

Checkbox, on · Regular+ · `c_neachbook` · cfg `texpert/neachbook`

> Output endnotes at the end of each book

Untick it to collect all endnotes at the end of the last book.

###### Enhanced paragraphed footnotes

Checkbox, off · Regular+ · `c_newparnotes` · cfg `texpert/newparnotes`

> Paragraphed footnotes which allow \fp to work and also the ifparnotes... controls below. Causes some spacing differences compared to old-style.

Paragraphed footnotes run several notes together in one paragraph. With the current layout version this is always on; the box only matters when **Maximum layout version** is 5 or lower.

###### Remove depth above paragraphed notes

Checkbox, on · Regular+ · `c_parntkillpd` · cfg `texpert/parntkillpd`

> Kern away (kill) the glyph/font depth of note types before paragraphed notes, using the value of \prevdepth

Keeps the space between different note types even. Change it only to solve a specific spacing problem.

###### Remove depth after paragraphed notes

Checkbox, off · Regular+ · `c_parntkilldepth` · cfg `texpert/parntkilldepth`

> Kill the depth of (the last row of) paragraphed note styles. Paragraphed notes will use the margin as their baseline.

Ticked, the last line of paragraphed notes sits on the bottom margin. Unticked, space for letters below the baseline (such as g and p) is kept.

###### Use grid not font/glyph height at rule

Checkbox, off · Regular+ · `c_parntruletopskip` · cfg `texpert/parntruletopskip`

> If true, the footnote rule is positioned relative to the hypothetical baseline above the topmost footnote, rather than relative to the glyph/font height.

The footnote rule is the line above the notes. Unticked, it is placed relative to the height of the letters in the first note. Change it only if the space between rule and notes looks wrong.

###### Use grid not font/glyph height between notes

Checkbox, on · Regular+ · `c_parntmidtopskip` · cfg `texpert/parntmidtopskip`

> If true, then the \InterNoteSpace is relative to the hypothetical baseline above the topmost footnote, rather than the glyph/font height. \InterNoteSpace is triggered between note styles.

For the space between two note types (for example footnotes and cross-references). Ticked gives the same space everywhere. Untick it to measure from the letter height.

###### Use glyph height not font height in footnotes

Checkbox, off · Regular+ · `c_fnxugm` · cfg `texpert/fnxugm`

> Does the note use the font's descender design parameter, or the actual bottom of the glyph. If the former (and depth is not killed), then the bottom of notes have a common baseline across pages. If the latter, then the glyphs sit as close to the bottom margin as they can, which may permit an extra line of text.

Unticked, the last line of notes is at the same height on every page. Ticked, notes sit as low as possible, which sometimes leaves room for an extra line of text.

###### Last Note: interlinepenalty

Number · Regular+ · `s_lastnoteinterlinep` · cfg `texpert/lastnoteinterlinep`  
Values: -9999–10000 (default 10000)

> Penalty for breaking between lines of the last footnote.

10000 = never split the last footnote across pages. Lower values allow a split, which can help fill pages with many notes.

###### Last Note: widowpenalty

Number · Regular+ · `s_lastnotewidowp` · cfg `texpert/lastnotewidowp`  
Values: -9999–10000 (default 10000)

> Extra penalty for breaking at the last line of the last footnote.

For a split that leaves only the last line on the next page. 10000 forbids it.

###### Last Note: clubpenalty

Number · Regular+ · `s_lastnoteclubp` · cfg `texpert/lastnoteclubp`  
Values: -9999–10000 (default 10000)

> Extra penalty for breaking at the first line of the last footnote.

For a split that leaves only the first line on the page. 10000 forbids it.

###### Last Note: penalty at par

Number · Regular+ · `s_lastnoteparp` · cfg `texpert/lastnoteparp`  
Values: -9999–10000 (default 100)

> Penalty for breaking at an explicit footnote-paragraph in the last footnote.

The default 100 allows a split at a note paragraph more easily than mid-paragraph.

###### Split notes: Shortest note to shave

Number · Regular+ · `s_nshaveshort` · cfg `texpert/nshaveshort`  
Values: 0–100 (default 2)

> If footnotes might be shaved, how many lines must it be?

"Shaving" splits a note that does not fit and moves part to the next page. Shorter notes are kept whole.

###### Split notes: min lines to move.

Number · Regular+ · `s_nshavemin` · cfg `texpert/nshavemin`  
Values: 0–100 (default 2)

> If a footnote is being shaved (split onto next page), what is the minimum number of lines to move?

Avoids moving a single lonely line.

###### Split notes: note lines to stay

Number · Regular+ · `s_nshavestay` · cfg `texpert/nshavestay`  
Values: 0–100 (default 2)

> If a footnote is being shaved (split onto next page), how many lines of (all) notes must remain on the page?

Counts lines of all notes.

###### Study note factor-Single column

Number · Regular+ · `s_footnotemulsts` · cfg `texpert/footnotemulsts`  
Values: 0–2100 (default 400)

> To avoid needless cycles/underfull pages, what portion of a study note's height-estimate should TeX apply when gathering input in single-column mode? (100=10percent)

PTXprint guesses how much space study notes need while it collects text for a page. 1000 = 100%. Lower values can give fuller pages but more work; higher values can leave pages underfull. Change it only on advice.

###### Study note factor-Two column

Number · Regular+ · `s_footnotemulstt` · cfg `texpert/footnotemulstt`  
Values: 0–2100 (default 800)

> To avoid needless cycles/underfull pages, what portion of a study note's height-estimate should TeX apply when gathering input in two-column mode? (100=10percent)

Same as **Study note factor-Single column**, for two-column text.

###### Study note factor-Diglot

Number · Regular+ · `s_footnotemulstd` · cfg `texpert/footnotemulstd`  
Values: 0–2100 (default 500)

> To avoid needless cycles/underfull pages, what portion of a study note's height-estimate should TeX apply when gathering diglot input? (100=10percent)

Same as **Study note factor-Single column**, for diglot text.

###### Footnote factor-Single column

Number · Regular+ · `s_footnotemuls` · cfg `texpert/footnotemuls`  
Values: 0–2100 (default 400)

> To avoid needless cycles/underfull pages, what portion of a note's height-estimate should TeX apply when gathering input in single-column mode? (100=10percent)

Same idea for ordinary footnotes. Change it only on advice.

###### Footnote factor-Two column

Number · Regular+ · `s_footnotemult` · cfg `texpert/footnotemult`  
Values: 0–2100 (default 800)

> To avoid needless cycles/underfull pages, what portion of a note's height-estimate should TeX apply when gathering input in two-column mode? (100=10percent)

Change it only on advice.

###### Footnote factor-Diglot

Number · Regular+ · `s_footnotemuld` · cfg `texpert/footnotemuld`  
Values: 0–2100 (default 10)

> To avoid needless cycles/underfull pages, what portion of a note's height-estimate should TeX apply when gathering diglot input? (100=10percent)

Change it only on advice.

###### Footnote factor-Centre column

Number · Regular+ · `s_footnotemulc` · cfg `texpert/footnotemulc`  
Values: 0–2100 (default 1)

> To avoid needless cycles/underfull pages, what portion of a note's height-estimate should TeX apply when gathering centre-column notes? (100=10percent)

For example cross-references between two columns. These notes do not take space from the text column, so the default is very low.

###### Distance of margin notes from text

Number · Regular+ · `s_marginnotesgap` · cfg `texpert/marginnotesgap`  
Values: 0–100 (default 6)

> The size of the gap between the margin notes and the text

A larger number moves margin notes further from the text. Margin notes are turned on, and their width set, on the **Layout** tab, **Page Setup** area (**Margin Notes Col Width (mm)** and **Margin Notes on Left/Inner**).

##### Diglot

###### Balance diglot/polyglot notes

Checkbox, off · Regular+ · `c_diglotbalnotes` · cfg `texpert/diglotbalnotes`

> When there's a note on column R (for example), does that reduce the space from other columns?

Tick it to keep the bottoms of all columns level. Unticked, each column uses its own space.

###### Diglot/polyglot merged paragraphed notes are RTL

Checkbox, off · Regular+ · `c_mergednotesrtl` · cfg `texpert/mergednotesrtl`

> When merged notes are not shown as individual paragraphs, the result must be arranged as though RTL or LTR (however the individual notes are structured). This defines the paragraph alignment.

Tick it when the merged notes should read right-to-left. Getting this wrong arranges the notes badly, so match it to the language of the notes.

###### Adjust Versification of Projects

Checkbox, on · Regular+ · `c_reversify` · cfg `texpert/reversify`

> If versification differs between projects, adjust diglot/polyglot projects to match the primary (L) project.

Keeps matching verses side by side. Leave it ticked unless the projects already use the same versification.

###### Keep existing verse numbers (as \vp)

Checkbox, on · Regular+ · `c_showvpvrse` · cfg `texpert/showvpvrse`

> When adjusting versification, show the original verse numbers in their new (adjusted) location.

Readers then see the verse numbers of their own translation.

###### Show old chapter numbers if changed (in \vp)

Checkbox, on · Regular+ · `c_showvpchap` · cfg `texpert/showvpchap`

> When adjusting versification, show the adjusted chapter numbers (only) if they have changed.

The old chapter number is shown with the verse number.

###### Show Diglot Trace Marks

Checkbox, off · Regular+ · `c_vistrace` · cfg `texpert/vistrace`

> Insert visible trace marks in diglot output

Marks where the column pieces are joined, to find layout problems. Turn it off for the final PDF.

###### Extra Trace Mark Info

Checkbox, off · Regular+ · `c_vistracex` · cfg `texpert/vistracex`

> Add extra information to diglot trace marks. (debugging only - can alter layout)

Debugging only; it can change the layout.

###### Diglot Shading Padding

Number · Regular+ · `s_diglotcolourpad` · cfg `texpert/diglotcolourpad`  
Values: -20–20 (default 3)

> The amount of side padding (pt) on the shaded background of a diglot

Larger extends the shading further beyond the text. Negative values make it narrower than the text.

###### How does text-border behave in diglots?

Drop-down · Regular+ · `fcb_textbordermode` · cfg `texpert/textbordermode`  
Choices: Borders start at body text | Borders include book intros | Wide book intros for per-column textborders

> Historically, diglot text-borders put the border around book introductions. This control allows that (substandard) behaviour to be chosen, and also allows  experimental code to make books with per-column textborders use full-width text for introductory text.

**Borders start at body text** leaves book introductions outside the border. **Borders include book intros** is the old behaviour. **Wide book intros for per-column textborders** is experimental: introductions use the full page width when each column has its own border.

###### Unprintable page recovery.

Number · Regular+ · `s_growunprintable` · cfg `texpert/growunprintable`  
Values: -1–10 (default 2)

> If notes / figures make a page unprintable: -1: immediately stop; 0: print failed contents and try to struggle on; >0 grow page height by up to N lines.

Grown pages may extend into the bottom margin, so check them.

###### Page-full test.

Drop-down · Regular+ · `fcb_pagefulltest` · cfg `texpert/pagefulltest`  
Choices: 1xBiggest baseline | 2xSmallest baseline | 2xBiggest baseline | 3xSmallest baseline

> When a (non-title) chunk has finished, the amount of unused space below which diglot will immediately output a page,  rather than trying to fit the next chunk. (irrespective of how short it is). Higher values encourage underfilled pages, but can prevent orphaning of the 1st line of poetry.

We could not confirm that a change here reaches the typesetting code in the current version.

##### Pictures, Figures, Images, Sidebars

###### Default Figures Top Left

Checkbox, on · Regular+ · `c_figleft` · cfg `texpert/figleft`

> Default figure positions to top left

For two-column pictures with no usable position: PTXprint places them at the top of a column, alternating left and right. Ticked, it starts with the left column.

###### Ref Before Caption

Checkbox, off · Regular+ · `c_captreffirst` · cfg `texpert/captreffirst`

> Output reference before caption

Puts the verse reference before the caption text.

###### Show Caption Before Image

Checkbox, off · Regular+ · `c_captfirst` · cfg `texpert/captfirst`

> Output caption before image

Puts the caption above the picture.

###### Space (pt) beside cutout/sidebar

Number · Regular+ · `s_cutouterpadding` · cfg `texpert/cutouterpadding`  
Values: 0–50 (default 10)

> This sets the default gap (pt) between the body text and the side of a figure/sidebar in a cutout.

A cutout is a space cut into the side of the text. This value is used when a picture or sidebar does not set its own space. **Default space beside picture** sets the same value and wins when changed from its default.

###### Space between picture & caption

Number · Regular+ · `s_captionadj` · cfg `texpert/captionadj`  
Values: -10–20 (default 0)

> Increase/Reduce the gap between figures and their captions

Negative values remove space, in points.

###### Default space beside picture

Number · Regular+ · `s_spbeside` · cfg `texpert/spbeside`  
Values: 0–100 (default 10)

> Picture horizontal margin*2

Horizontal space, in points. Sets the same value as **Space (pt) beside cutout/sidebar**; when changed from its default (10), this one is used.

###### Show comprehensive illustration credits

Checkbox, off · Regular+ · `c_allpicredits` · cfg `texpert/allpicredits`

> Instead of using the catch-all phrasing 'All other illustrations by...' show a comprehensive list of every artist and all pages that contain their illustrations.

Lists every artist with all the pages of their pictures.

##### PDF Options, Covers, Show/Hide

###### No PDF Bookmarks

Checkbox, off · Regular+ · `c_noactions` · cfg `texpert/noactions`

> Don’t output PDF bookmarks

Bookmarks are the list of books and chapters in a PDF viewer's side panel. Some printers ask for a PDF without them.

###### Allow Active Links in PDF

Checkbox, on · Regular+ · `c_actions` · cfg `texpert/actions`

> Make links active inside PDF

For example cross-references and web links. Untick it for a PDF only for printing.

###### Use Book Codes in PDF Bookmarks

Checkbox, off · Regular+ · `c_refbkmks` · cfg `texpert/refbkmks`

> Use book codes instead of book names in bookmarks

Helps when book names are long or in a script the PDF viewer cannot show.

###### Disable Transparency in PDF

Checkbox, off · Regular+ · `c_notransparent` · cfg `texpert/notransparent`

> Disable transparency output in PDF

For printers that cannot handle transparent colours. Each one becomes a solid colour that looks the same on white paper. Anything behind it is then hidden, so check pages with shading or overlapping pictures.

###### Show adjust points

Checkbox, off · Regular+ · `c_showadjpoints` · cfg `texpert/showadjpoints`

> Show adjust points in the margin of the text.

Marks where paragraph adjustments (stretch or shrink from the adjustment list) apply. Turn it off for the final PDF.

###### Mark Trigger Points

Checkbox, off · Regular+ · `c_mktrigpts` · cfg `texpert/mktrigpts`

> Display trigger points in output

Triggers are instructions tied to a verse, such as a picture position or a style change. Turn it off for the final PDF.

###### Show USFM codes

Checkbox, off · Regular+ · `c_showusfmcodes` · cfg `texpert/showusfmcodes`

> Show the USFM markers in the margin beside paragraphs.

Helps you find which style to change on the **Styles** tab. Turn it off for the final PDF.

###### Show Error Bars For Overfull Lines

Checkbox, off · Regular+ · `c_showhboxerrorbars` · cfg `texpert/showhboxerrorbars`

> Enable this option to have TeX make overfull lines stand out.

A black bar at the end of every overfull line. Fix such lines, for example with hyphenation or small text changes. Then turn this off.

###### Spine Overlap onto Back Cover (mm)

Number · Regular+ · `s_spineoverlapback` · cfg `texpert/spineoverlapback`  
Values: 0–50 (default 0)

> If you want the spine graphic or colour to spill over onto the back cover page, then set the amount of overlap here.

Helps hide small errors when the cover is folded. Used when you make a cover on the **Peripherals** tab.

###### Spine Overlap onto Front Cover (mm)

Number · Regular+ · `s_spineoverlapfront` · cfg `texpert/spineoverlapfront`  
Values: 0–50 (default 0)

> If you want the spine graphic or colour to spill over onto the front cover page, then set the amount of overlap here.

Used when you make a cover.

###### Cover Bleed (mm)

Number · Regular+ · `s_bleed` · cfg `texpert/bleed`  
Values: 0–25 (default 5)

> Bleed is the section of artwork that goes beyond where the paper is cut. This ensures that the image goes right to the edge of the cover after it has been trimmed.

Ask your printer how much bleed they need; often 3 to 5 mm.

###### Hard Cover Art Bleed (mm)

Number · Regular+ · `s_artbleed` · cfg `texpert/artbleed`  
Values: 0–25 (default 0)

> Art Bleed is specifically for hard cover binding and is the setting which enables images to go beyond the size of the cover in order to wrap around the hard cover and stuck down under the inner backing sheet.

Leave it at 0 for soft covers. Ask your printer for the right value.

##### Preview Pane: Adjustment and Analysis Settings

###### Auto-update Delay (seconds)

Number · Regular+ · `s_autoupdatedelay` · cfg `texpert/autoupdatedelay`  
Values: 0–120 (default 3)

> Right-clicking again on the PDF within this time (3 second default) will prevent the Auto-update from running.

A right-click adjustment with **Auto-update** on starts a new print after this delay, so you can make several adjustments first. Increase it if you need more time between adjustments.

###### Shrink Text Step Value (%)

Number · Regular+ · `s_shrinktextstep` · cfg `texpert/shrinktextstep`  
Values: 1–5 (default 1)

> Step Value to shrink text using right-click context menu adjustment.

Percent per "shrink text" step.

###### Minimum Text Shrink (%)

Number · Regular+ · `s_shrinktextlimit` · cfg `texpert/shrinktextlimit`  
Values: 85–100 (default 95)

> Limit how much text can shrink to using right-click context menu adjustment.

95 = at most 5% smaller. The page filler also uses this limit. Shrinking too much makes text look crowded.

###### Expand Text Step Value (%)

Number · Regular+ · `s_expandtextstep` · cfg `texpert/expandtextstep`  
Values: 1–5 (default 1)

> Step Value to expand text using right-click context menu adjustment.

Percent per "expand text" step.

###### Maximum Text Expand (%)

Number · Regular+ · `s_expandtextlimit` · cfg `texpert/expandtextlimit`  
Values: 100–115 (default 105)

> Limit how much text can expand to using right-click context menu adjustment.

105 = at most 5% larger.

###### Bad Space minimum width (em)

Number · Regular+ · `s_spaceEms` · cfg `texpert/spaceEms`  
Values: 0–10 (default 1.3)

> Minimum width for a bad space. 0 says to calculate for the 20 worst spaces in the doc

Used by **Layout Analysis** in the PDF Preview window; em = the size of the font. A lower value marks more spaces.

###### Bad intercharacter space minimum width (em)

Number · Regular+ · `s_charSpaceEms` · cfg `texpert/charSpaceEms`  
Values: 0–1 (default 0.3)

> Minimum width for a bad inter character space.

Only used when **Between Letters** spacing is on (**Fonts+Script** tab).

###### Precise collisions

Checkbox, off · Regular+ · `c_collisionPrecise` · cfg `texpert/collisionPrecise`

> Only show precise collisions between glyphs rather than overlapping bounding boxes - slow

Finds fewer false collisions.

###### Collision Detection Padding (pt)

Number · Regular+ · `s_paddingwidth` · cfg `texpert/paddingwidth`  
Values: -1–5 (default 0.5)

> Minimum space between bounding boxes of glyphs before a collision is flagged.

For boxes around letters on different lines. A larger value reports more possible collisions.

###### River Detection Threshold (em)

Number · Regular+ · `s_riverthreshold` · cfg `texpert/riverthreshold`  
Values: 1–1000 (default 3)

> The sum of all the widths in the river must be above this for the river to be detected

Increase it to report only the worst rivers.

###### River Detection minimum required maximum width (em)

Number · Regular+ · `s_riverminmaxwidth` · cfg `texpert/riverminmaxwidth`  
Values: 0.1–5 (default 1)

> Minimum width required for the widest part of the river

In em.

###### River Detection minimum width (em)

Number · Regular+ · `s_riverminwidth` · cfg `texpert/riverminwidth`  
Values: 0.1–5 (default 0.5)

> Minimum width of any space in a river for it to be included

Narrower spaces are not counted as part of a river.

###### River Detection maximum line leading (em)

Number · Regular+ · `s_rivergap` · cfg `texpert/rivergap`  
Values: 0–5 (default 0.4)

> Any lines separated by a gap greater than this will be considered not to be in the same river

In em.

###### River Detection minimum overlap (em)

Number · Regular+ · `s_riveroverlap` · cfg `texpert/riveroverlap`  
Values: -5–5 (default 0.4)

> Minimum overlap in ems required for two spaces above each other to be considered part of the same river

For two spaces on lines above each other.

##### Automatic Page Filler

###### Time limit for the whole job (minutes)

Number · Regular+ · `s_pbtimeout` · cfg `texpert/pbtimeout`  
Values: 0–1000 (default 180)

> The page filler works on all the books together. When this time is reached, the page filler stops. A book that is not finished keeps the pages that are already filled. Usually this affects only the longest book.  
> Higher: more time to find a good layout for every page.

0 means no time limit. Increase it for a long Bible if the longest book does not finish.

###### Earlier pages to retry

Number · Regular+ · `s_pbbacktrack` · cfg `texpert/pbbacktrack`  
Values: 0–10 (default 4)

> If the page filler cannot fill a page, it backtracks to the page before and tries a different layout there. This is the largest number of pages it can backtrack.  
> Higher: fewer failed pages, but much slower.  
> Lower: faster, but more pages may fail. 0 = never backtrack (fastest).  
> Affects: Speed.

How many earlier pages the page filler may go back to try a different layout.

###### Paragraphs to adjust on each page

Number · Regular+ · `s_pbmaxr` · cfg `texpert/pbmaxr`  
Values: 1–10 (default 6)

> The largest number of paragraphs on one page that the page filler may stretch or shrink. Each poetry line (\q1, \q2 …) counts as one paragraph. Each extra paragraph doubles the number of layouts the page filler tries.  
> Higher: more ways to fill each page, so fewer failed pages, but each page takes longer.  
> Lower: faster, but more pages may fail.  
> Affects: Speed.

Keep it low unless many pages fail.

###### Widest word space allowed (× text size)

Number · Regular+ · `s_pbspacingtol` · cfg `texpert/pbspacingtol`  
Values: 0–10 (default 1)

> When the page filler stretches a paragraph, the average space between words must not be wider than this. 1.0 = as wide as the text size. A normal word space is about 0.3 to 0.5.  
> Higher: easier to fill pages, but the text can look too spread out.  
> Lower: tighter, better-looking text, but pages are harder to fill and take longer.  
> Affects: Quality and Speed.

As a part of the text size.

###### Keep paragraphs close to normal width

Number · Regular+ · `s_pbexpbad` · cfg `texpert/pbexpbad`  
Values: 0–10 (default 1)

> The page filler prefers small changes to a paragraph over big changes. This setting controls how strong that preference is. Higher: the page filler tries small changes first, so the text looks more even.  
> Lower: the page filler accepts big changes more easily.  
> Affects: Quality.

Higher values give more even text.

###### Penalise shrink or stretch

Number · Regular+ · `s_pbexpcost` · cfg `texpert/pbexpcost`  
Values: -5–5 (default 1)

> Tells the page filler whether to shrink paragraphs or stretch them when both are possible.  
> Positive numbers: penalise stretching (so the text prefers to shrink more).  
> Negative numbers: penalise shrinking. (so the text prefers to stretch more).  
> 0: no preference.  
> A bigger number (+ or −) means a higher penalty.  
> Affects: Quality.

Applies when both shrinking and stretching would work.

###### Keep neighbouring paragraphs alike

Number · Regular+ · `s_pbcontrast` · cfg `texpert/pbcontrast`  
Values: 0–20 (default 3)

> The page filler compares each paragraph with the paragraph before it. It tries to avoid a very stretched paragraph next to a very shrunk one.  
> Higher: neighbouring paragraphs look more alike, so the page looks more even.  
> Lower: neighbouring paragraphs can look more different.  
> Affects: Quality.

Higher values give a more even page.

###### The cost of imbalance in a polyglot slice

Number · Regular+ · `s_pbpolyimbalance` · cfg `texpert/pbpolyimbalance`  
Values: 0–10 (default 1)

> How bad is it for a polyglot slice to not be balanced. This the multiplier of that cost  
> Only relevant to diglot and polyglot projects

The page filler works on slices: pieces of text that belong together across the columns, such as the same verses in each language. A slice is unbalanced when one column ends lower than another. This sets how much to avoid that, compared with stretching or shrinking paragraphs. Higher: columns end more evenly, but paragraphs may change more. Lower: paragraphs look more even, but one column may end a few lines lower. Change it only if your diglot columns are often uneven after page filling.

##### Other Miscellaneous Settings

###### Use \toc3 for Tab Text

Checkbox, on · Regular+ · `c_tocthreetab` · cfg `texpert/tocthreetab`

> Use \toc3 for tab text if no \zthumbtab

`\toc3` is the short book name. Thumb tabs are set on the **Tabs+Borders** tab.

###### Tilde is No Break Space

Checkbox, on · Regular+ · `c_tildenbsp` · cfg `texpert/tildenbsp`

> Treat ~ as non breaking space

A non-breaking space looks like a normal space, but the line never breaks there. Untick it only if your text needs a real tilde.

###### Remove \ref ... \ref* links

Checkbox, on · Regular+ · `c_removextreflinks` · cfg `texpert/removextreflinks`

> USFM 3.2 allows additional reference links to be inserted as part of \xt ... \xt* markup. This frequently appear in DBL text bundles, but are unhandled by PTXprint. Allow these to be removed from the USFM prior to typesetting.

These `\ref` links inside cross-references come from Digital Bible Library (DBL) text. Only their visible text is kept.

###### End decoration skip

Number · Regular+ · `s_bedskip` · cfg `texpert/bedskip`  
Values: -100–100 (default 16)

> The gap between the end of the book and the book-end decoration

In points. The decoration is turned on in **Ornamental Decorations** on the **Tabs+Borders** tab. Negative values move it up.

###### Thumbtab rotated adjustment

Number · Regular+ · `s_thumbvvadj` · cfg `texpert/thumbvvadj`  
Values: -10–50 (default -2)

> Shift thumbtab text

Moves the text on rotated thumb tabs (in points) to centre it on the tab. Thumb tabs and **Rotate Tabs** are on the **Tabs+Borders** tab.
