# Advanced tab

## What this tab is for

The **Advanced** tab holds settings for experienced users. Most people never need to change anything here. Come here when another tab cannot give you the result you need, or when someone on the support team asks you to change a specific setting.

The tab has two sub-tabs:

* **Main** – ways to change the text before it is typeset (a changes file, a processing script), extra stylesheets and TeX settings files, interlinear output, plugins, internet use, and locks that protect a finished layout.
* **Other** – about 125 "TeXpert" settings. These are fine controls for the typesetting engine, sorted into groups such as **Page Layout and Spacing** or **Footnotes, Cross-references, Study Notes**.

The **Advanced** tab is only shown in the **Default** and **Full** views. Some settings on the **Main** sub-tab are only shown in the **Full** view (this is noted below).

## Before you change anything here

These are expert settings. A small change can move text on many pages. Follow these rules:

1. **Change one setting at a time.** Then print and look at the result. If you change several settings together, you cannot tell which one caused a change.
2. **Write down the original value** before you change it. Then you can always go back.
3. **Look for bold labels.** On the **Other** sub-tab, the label of a check box or number box turns **bold** when its value is different from the default value. This lets you see quickly what has been changed. (Drop-down lists do not turn bold.)
4. **To go back to the default value:**
   * For a number box, click its bold label. The value goes back to the default.
   * For a check box, click the check box again.
   * For a drop-down list, choose the first item in the list. The first item is always the default.
5. **Hover the mouse over a setting** to see its tooltip. The first line of the tooltip shows the internal name and the default value in square brackets. For a number box the brackets show several numbers: the first number is the default (the others are the lowest value, highest value and step sizes).

PTXprint saves a TeXpert setting in the configuration only when it is different from the default.

To find a TeXpert setting quickly, type part of its name in the **Search for settings** box at the bottom of the main window (Ctrl+F).

## Main sub-tab: Text Processing & Stylesheets

This area lets you change the text, or the way it is styled, using files that you edit yourself. Each option has a check box (to turn it on) and an **Edit...** button. The **Edit...** button is only active when its check box is ticked. It opens the file on the **View+Edit** tab, where you can type in it and save it.

These are advanced features. They are for people who understand USFM, regular expressions (a way to describe text patterns) or TeX. Never change these files if you are not sure what you are doing. Untick the check box to turn the file off again. You do not need to delete the file.

What each file does:

* **Apply Modifications to USFM Text (changes.txt)** – a list of search-and-replace rules. PTXprint applies them to a temporary copy of the text before it typesets it. Your Paratext project is never changed. `changes.txt` belongs to the current configuration only. `PrintDraftChanges.txt` (in the project folder) applies to all configurations of the project.
* **Apply Customized Settings (ptxprint-mods.tex)** – TeX settings that are applied after all the PTXprint settings. Use it for things that PTXprint has no control for. A support person may give you a line to add here.
* **Apply Initial Settings (ptxprint-premods.tex)** – TeX settings applied before the stylesheets and other settings. This is rarely needed. (**Full** view only.)
* **Apply Customized Styles (custom.sty)** – the project's own custom stylesheet, the same one Paratext uses. (**Full** view only.)
* **Apply Stylesheet Overrides (ptxprint-mods.sty)** – an extra stylesheet for this configuration that overrides other styles. Most style changes are easier on the **Styles** tab. (**Full** view only.)
* **Process Text With Custom Script at** – runs a program of your own on each book. (**Full** view only.)

PTXprint changes the text in this order:

1. A custom script, if **start** is chosen.
2. The rules in the changes files.
3. **Auto-Correct USFM** and other changes that PTXprint makes for settings on other tabs.
4. A custom script, if **end** is chosen.

## Main sub-tab: General

This area holds settings that do not fit anywhere else:

* **Sensitive Project** – for projects in sensitive locations. It shortens picture credits and keeps private data out of the PDF.
* **Auto-Correct USFM** – fixes common USFM mistakes and warns you about serious ones. Leave it ticked.
* **Interlinear** – prints Paratext interlinear glosses under (or above) each word. (**Full** view only.)
* **Auto-tag Hebrew and Greek words** – marks Hebrew and Greek words so they use the right font.
* **Only Use English Links** and **Disable ALL Internet Use** – control how PTXprint uses the internet.
* **Plugins** – loads extra parts of the typesetting code for special features. (**Full** view only.)
* **Lock XeTeX Layout Level** and **Lock UI Layout Settings** – protect a finished layout from changes. (**Full** view only.)

## Main sub-tab: Capture tests?

This area is only shown in the **Full** view. It is a tool for the PTXprint developers. It records what you click so that the developers can make an automatic test. Normal users do not need it.

## Other sub-tab: the TeXpert settings

The **Other** sub-tab lists the TeXpert settings in groups. Click a group name to open or close it. The button with the filter icon at the top shows only the groups that have changed settings. It is only active while the **Other** sub-tab is shown.

The sections below follow the groups on the screen. Remember: change one setting at a time, and write down the original value.

### Page Layout and Spacing

These settings control where books and introductions start, how two columns are balanced, line spacing, and notelines.

* **Where to start a new book** chooses if each book starts on the next page, on the same page as the end of the previous book, or on the next odd (right-hand) page. **Page full factor** sets how full the page can be before the next book is moved to a new page anyway.
* **Where to start a new intro page** does the same for book introductions. **Grouped** keeps adjacent introductions together and starts the group on an odd page.
* **Unbalanced Lines (Max)** is only used when **Allow Unbalanced Columns** is ticked on the **Layout** tab.
* **Variable line spacing maximum stretch** and **shrink** are only used when **Fill Columns** is ticked on the **Layout** tab.
* The **Noteline** settings change the lines for hand-written notes that you turn on with **Notelines** on the **Layout** tab. Set the noteline colour there too.
* **Maximum layout version** and **Legacy 1/14 LineSpacing** keep older projects looking the same after PTXprint is updated.
* **Maximum parallel processes** controls how many jobs run at the same time, for example when the page filler works.

### Chapter and Verse

These settings fine-tune chapter numbers and verse numbers: the space after them, the size of large (drop) chapter numbers, hanging verse numbers in poetry, and marginal verse numbers (verse numbers placed in the margin, set on the **Body** tab).

### Body Text

These settings control paragraph indents, line breaking and hyphenation, and clickable links.

Some of these are "penalties". A penalty is a number that tells the typesetting engine how much to avoid something. A higher penalty means "avoid this more strongly". 10000 means "never".

* **Hyphenation threshold**, **Penalty for inserting hyphen** and **Double hyphenation penalty** only matter when hyphenation is turned on (**Fonts+Script** tab).
* **Maximum orphan word length** is only used when **Prevent Orphan Words** is ticked on the **Body** tab.

### Fonts and Underline

These settings control how line heights are measured, whether system fonts can be used, and how underlines look.

### Footnotes, Cross-references, Study Notes

These settings control where notes go on a page, when notes may be split across pages, and fine details of the spacing of paragraphed notes. Many of these settings interact. Change them only to solve a specific problem, and check several pages after each change.

### Diglot

These settings are only used when you print two or more texts side by side (see the **Diglot** tab). They control notes, versification, shading, borders and what happens when a page cannot be printed.

### Pictures, Figures, Images, Sidebars

These settings control the default position of pictures, the order of caption and reference, the space around pictures and sidebars, and the style of picture credits.

### PDF Options, Covers, Show/Hide

These settings control bookmarks, links and transparency in the PDF. They also hold some cover sizes, and "show" options that put helpful marks on the pages while you proofread. Turn all the "show" options off again before you make the final PDF.

### Preview Pane: Adjustment and Analysis Settings

These settings control the PDF Preview window: the auto-update delay, how far the right-click menu can shrink or expand text, and how **Layout Analysis** finds bad spaces, collisions and rivers. A river is a line of white space that runs down through several lines of text. Changes here take effect in the preview straight away. You can also reach these settings from the PDF Preview window: click the delay text next to **Auto-update**, or the analysis settings link.

### Automatic Page Filler

These settings control the page filler tool in the PDF Preview window. The page filler stretches or shrinks paragraphs a little so that each page is filled. The settings balance speed against how good the text looks. See the chapter on the PDF Preview window for how to use the tool.

### Other Miscellaneous Settings

These settings control thumb tab text, the tilde (~) character, unwanted reference links from DBL text, and the space above the end-of-book decoration.

## Common tasks

### Apply a search-and-replace rule to the text (advanced)

1. On the **Advanced** tab, **Main** sub-tab, in **Text Processing & Stylesheets**, tick **Apply Modifications to USFM Text (changes.txt)**.
2. Click the **Edit...** button next to it (or press Shift+Ctrl+C). PTXprint opens the **View+Edit** tab and shows `changes.txt`.
3. Add one rule on each line. A simple rule looks like `"old text" > "new text"`. The text in the first quotes is a regular expression, so some characters (such as `.` `(` `[` `\`) have a special meaning.
4. Save the file on the **View+Edit** tab.
5. Click **Print**. Check that the change appears in the PDF.

If PTXprint reports an error in the changes file, look at the last rule you added.

### Turn off a changes file or mods file without deleting it

1. Go to **Advanced** › **Main** › **Text Processing & Stylesheets**.
2. Untick the check box for that file (for example **Apply Customized Settings (ptxprint-mods.tex)**).
3. Print again. The file stays on disk, so you can tick the box later to use it again.

### Print an interlinear text

1. In Paratext, make sure the interlinear glosses are approved.
2. Change to the **Full** view.
3. On **Advanced** › **Main** › **General**, tick **Interlinear**.
4. In the box next to it, type the language code of the glosses (for example `en`). The code is the end of the folder name `Interlinear_en` in the project folder.
5. Tick **Ruby Text Above** if you want the glosses above the words instead of below.
6. Click **Print**.
7. To change the font size or colour of the glosses, click the **\gloss|rb** link. For the base text, click the **\rb** link.

### Protect a finished layout

1. Change to the **Full** view.
2. On **Advanced** › **Main** › **General**, tick **Lock XeTeX Layout Level**. Future PTXprint updates will then use the same layout rules as now.
3. Tick **Lock UI Layout Settings**. The main layout, font and style controls are now greyed out, so nobody can change them by accident.
4. Untick these boxes when you need to change the layout again.

### Find out which TeXpert settings have been changed

1. Go to the **Advanced** tab and click the **Other** sub-tab.
2. Click the filter button at the top. Only the groups with changed settings stay visible, and they open.
3. Look for the bold labels. These are the changed settings.
4. Click the filter button again to show all groups.

### Put a TeXpert setting back to its default value

1. Find the setting on **Advanced** › **Other**. Its label is bold.
2. For a number box, click the bold label. For a check box, click the check box. For a drop-down list, choose the first item.
3. Check that the label is no longer bold.
4. Print again.

### Start each book on a right-hand page

1. Go to **Advanced** › **Other** › **Page Layout and Spacing**.
2. Set **Where to start a new book** to **Odd page**.
3. Print. PTXprint adds a blank page where it is needed.

### Let books follow each other on the same page

1. Go to **Advanced** › **Other** › **Page Layout and Spacing**.
2. Set **Where to start a new book** to **Same page**.
3. If a new book still starts on a new page when you do not want it to, increase **Page full factor** a little (for example from 0.65 to 0.75).

### Mark places that need attention while proofreading

1. Go to **Advanced** › **Other** › **PDF Options, Covers, Show/Hide**.
2. Tick **Show Error Bars For Overfull Lines** to see lines that are too long. Tick **Show USFM codes** to see which marker each paragraph uses.
3. Print and check the PDF.
4. Untick these options before you make the final PDF.

## Common problems

**The Advanced tab is missing.** It is only shown in the **Default** and **Full** views. Change the view level (see the chapter on the main window).

**Some settings on the Main sub-tab are missing** (for example **Interlinear**, **Plugins**, **Process Text With Custom Script at**, or the locks). These are only shown in the **Full** view.

**An Edit... button is greyed out.** Tick the check box for that file first.

**My changes in changes.txt have no effect.** Make sure **Apply Modifications to USFM Text (changes.txt)** is ticked, the file is saved on the **View+Edit** tab, and you printed again. Check that the search text really matches the USFM text, including spaces and markers. Look at the Log tab for messages about the changes file.

**Printing fails after I edited a mods file.** Untick **Apply Customized Settings (ptxprint-mods.tex)** (or the box for the file you edited) and print again. If the problem goes away, the error is in that file. Undo your last change in the file.

**Interlinear printing says some references "need to be reapproved".** The glosses for those verses are not approved in the Paratext Interlinearizer. Approve them in Paratext and print again.

**Between Letters spacing is greyed out on the Fonts+Script tab.** **Interlinear** is ticked on the **Advanced** tab. These two settings cannot be used together.

**Layout, font and style controls are greyed out.** **Lock UI Layout Settings** is ticked on **Advanced** › **Main** › **General** (**Full** view). Untick it.

**Help links and the update check are missing.** **Disable ALL Internet Use** is ticked. Untick it if you want PTXprint to use the internet again.

**My PDF suddenly looks different but I did not change anything on the main tabs.** Someone may have changed a TeXpert setting. Open **Advanced** › **Other** and click the filter button to see the changed settings (look for bold labels). Also check whether a changes file or mods file is ticked on the **Main** sub-tab.

**Unbalanced Lines (Max) or the variable line spacing settings have no effect.** They only work when **Allow Unbalanced Columns** or **Fill Columns** is ticked on the **Layout** tab.

**I changed Use system fonts but nothing happened.** You must close and restart PTXprint for this setting to take effect.

**Coloured marks or labels appear in the margins of my PDF.** One of the "show" options in **PDF Options, Covers, Show/Hide** is ticked (**Show adjust points**, **Mark Trigger Points**, **Show USFM codes**, **Show Error Bars For Overfull Lines**), or **Show Diglot Trace Marks** in the **Diglot** group. Untick it.

## Settings reference: Advanced tab

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Advanced tab › Main tab › Text Processing & Stylesheets

#### Apply Customized Settings (ptxprint-mods.tex)

- **Where:** Advanced tab › Main tab › Text Processing & Stylesheets
- **Type:** Checkbox (not ticked by default)
- **Description:** Apply customized TeX settings
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This is the normal file for advanced users to configure TeX. This .tex file executes AFTER all the PTXprint settings.

**Explanation:**

Turns on the file `ptxprint-mods.tex` for this configuration. PTXprint reads it after all its own settings, so anything in it wins. Use it only when a support person or an expert gives you something to put in it. If printing suddenly fails, untick this box first to see whether the file is the cause.

*(Internal ID: `c_useModsTex` · Config key: `project/ifusemodstex`)*

#### Process Text With Custom Script at

- **Where:** Advanced tab › Main tab › Text Processing & Stylesheets
- **Type:** Checkbox (not ticked by default)
- **Description:** Process text with custom script
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Processes the .usfm file through a program of your choosing. The program is run as `prog infile outfile` where infile is the source .usfm file and outfile the output .usfm that will then be typeset.

**Explanation:**

Runs a program of your own on each book before it is typeset. The program gets the name of the input USFM file and the name of the output file to write. Use it for changes that are too complex for a changes file, such as converting the text from one writing system to another. Choose the program with **Select...** and choose when it runs with **start** or **end**. This is for experienced users only.

*(Internal ID: `c_processScript` · Config key: `project/processscript`)*

#### start

- **Where:** Advanced tab › Main tab › Text Processing & Stylesheets
- **Type:** Radio button
- **View level:** Full view only
- **Only available when:** “Process Text With Custom Script at” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Execute processing script BEFORE running any printdraftchanges, canonicalisation (i.e. Auto-Correct USFM) or local changes which are all specified below.

**Explanation:**

Runs the custom script first, on the original USFM text. After that, PTXprint applies the changes files and **Auto-Correct USFM**. Choose this when your rules in the changes files expect the text that the script produces.

*(Internal ID: `r_when2processScript_before` · Config key: `project/when2processscript=before`)*

#### end

- **Where:** Advanced tab › Main tab › Text Processing & Stylesheets
- **Type:** Radio button
- **View level:** Full view only
- **Only available when:** “Process Text With Custom Script at” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Execute processing script AFTER running any printdraftchanges, canonicalisation (i.e. Auto-Correct USFM) or local changes which are all specified below.

**Explanation:**

Runs the custom script last, after the changes files, **Auto-Correct USFM** and the other changes PTXprint makes. The script then sees the text almost exactly as it will be typeset.

*(Internal ID: `r_when2processScript_after` · Config key: `project/when2processscript=after`)*

#### Select...

- **Where:** Advanced tab › Main tab › Text Processing & Stylesheets
- **Type:** Button
- **Description:** Select custom script
- **View level:** Full view only
- **Only available when:** “Process Text With Custom Script at” is selected

**Explanation:**

Opens a file chooser to pick the script or program (.bat, .exe, .py or .sh). After you choose a file, PTXprint ticks **Process Text With Custom Script at** for you. Hover over the button to see the chosen file. If you cancel without choosing a file, the option is turned off.

*(Internal ID: `btn_selectScript` · Config key: `project/selectscript`)*

#### Apply Modifications to USFM Text (changes.txt)

- **Where:** Advanced tab › Main tab › Text Processing & Stylesheets
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable changes.txt to be applied
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> If there are changes that you wish to apply to the USFM file(s) prior to producing the printout, then these can be specified in these files:
>
> changes.txt - is used for changes that only apply to the current configuration;
>
> PrintDraftChanges.txt - specifies changes which apply to all configurations, and gets 'included' at the top of changes.txt

**Explanation:**

Applies the search-and-replace rules in `changes.txt` (for this configuration) and `PrintDraftChanges.txt` (for all configurations of the project) to a temporary copy of the text. Your Paratext project is not changed. Use it to fix small problems in the text for printing only, such as spacing or punctuation. The rules are regular expressions, so test each new rule carefully.

*(Internal ID: `c_usePrintDraftChanges` · Config key: `project/usechangesfile`)*

#### Edit...

- **Where:** Advanced tab › Main tab › Text Processing & Stylesheets
- **Type:** Button
- **Description:** Edit changes files
- **View level:** Default and Full views
- **Only available when:** “Apply Modifications to USFM Text (changes.txt)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Switch to the View+Edit tab to show the Changes.txt file in one tab, and PrintDraftChanges.txt in the next tab to the right.
>
> Shortcut: Shift-Ctrl-C

**Explanation:**

Opens `changes.txt` on the **View+Edit** tab. If the project has a `PrintDraftChanges.txt` file, it opens in the next tab too. Save the file there, then print again to see the result.

*(Internal ID: `btn_editChangesFile`)*

#### Edit...

- **Where:** Advanced tab › Main tab › Text Processing & Stylesheets
- **Type:** Button
- **Description:** Edit customized TeX settings
- **View level:** Default and Full views
- **Only available when:** “Apply Customized Settings (ptxprint-mods.tex)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Switch to the View+Edit tab to show the ptxprint-mods.tex file.
>
> Shortcut: Shift-Ctrl-T

**Explanation:**

Opens `ptxprint-mods.tex` on the **View+Edit** tab so that you can edit it. Save it there and print again. Only available when **Apply Customized Settings (ptxprint-mods.tex)** is ticked.

*(Internal ID: `btn_editModsTeX`)*

#### Edit...

- **Where:** Advanced tab › Main tab › Text Processing & Stylesheets
- **Type:** Button
- **Description:** Edit stylesheet overrides
- **View level:** Full view only
- **Only available when:** “Apply Stylesheet Overrides (ptxprint-mods.sty)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Switch to the View+Edit tab to show the ptxprint-mods.sty file.
>
> Shortcut: Shift-Ctrl-S

**Explanation:**

Opens `ptxprint-mods.sty` on the **View+Edit** tab. Most style changes are easier and safer on the **Styles** tab.

*(Internal ID: `btn_editModsSty`)*

#### Apply Stylesheet Overrides (ptxprint-mods.sty)

- **Where:** Advanced tab › Main tab › Text Processing & Stylesheets
- **Type:** Checkbox (not ticked by default)
- **Description:** Apply stylesheet overrides
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> It is recommended to leave this option unchecked (off) unless you have intentionally customized styles using the ptxprint-mods.sty stylesheet and wish for these to be used by PTXprint.

**Explanation:**

Uses the extra stylesheet `ptxprint-mods.sty` for this configuration. Leave it unticked unless you, or someone helping you, has written style changes in that file on purpose. Most people make style changes on the **Styles** tab instead.

*(Internal ID: `c_useModsSty` · Config key: `project/ifusemodssty`)*

#### Apply Customized Styles (custom.sty)

- **Where:** Advanced tab › Main tab › Text Processing & Stylesheets
- **Type:** Checkbox (not ticked by default)
- **Description:** Apply custom styles
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> It is recommended to leave this option unchecked (off) unless you have intentionally customized styles using the custom.sty stylesheet and wish for these to be used by PTXprint.

**Explanation:**

Uses the project's `custom.sty` stylesheet, the same file that Paratext uses for its own display. Leave it unticked unless you know that the project's custom styles should also be used for printing. If the file does not exist, nothing changes.

*(Internal ID: `c_useCustomSty` · Config key: `project/ifusecustomsty`)*

#### Edit...

- **Where:** Advanced tab › Main tab › Text Processing & Stylesheets
- **Type:** Button
- **Description:** Edit custom styles
- **View level:** Full view only
- **Only available when:** “Apply Customized Styles (custom.sty)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Switch to the View+Edit tab to show the custom.sty file.
>
> Shortcut: Shift-Ctrl-M

**Explanation:**

Opens the project's `custom.sty` on the **View+Edit** tab. Remember that this file is shared with Paratext, so a change here can also change how Paratext shows the text.

*(Internal ID: `btn_editCustomSty`)*

#### Edit...

- **Where:** Advanced tab › Main tab › Text Processing & Stylesheets
- **Type:** Button
- **Description:** Edit custom script
- **View level:** Full view only
- **Only available when:** “Process Text With Custom Script at” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Edit the processing script

**Explanation:**

Opens the chosen processing script on the **View+Edit** tab, so that you can read or change it. It is only active when a script has been selected.

*(Internal ID: `btn_editScript`)*

#### Edit...

- **Where:** Advanced tab › Main tab › Text Processing & Stylesheets
- **Type:** Button
- **Description:** Edit initial TeX settings
- **View level:** Full view only
- **Only available when:** “Apply Initial Settings (ptxprint-premods.tex)” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Switch to the View+Edit tab to show the ptxprint-premods.tex file.
>
> Shortcut: Shift-Ctrl-P

**Explanation:**

Opens `ptxprint-premods.tex` on the **View+Edit** tab. Only available when **Apply Initial Settings (ptxprint-premods.tex)** is ticked.

*(Internal ID: `btn_editModsPreTex`)*

#### Apply Initial Settings (ptxprint-premods.tex)

- **Where:** Advanced tab › Main tab › Text Processing & Stylesheets
- **Type:** Checkbox (not ticked by default)
- **Description:** Apply initial TeX settings
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> This .tex file is executed BEFORE any stylesheets of other settings are applied. This file is rarely used.

**Explanation:**

Uses the file `ptxprint-premods.tex`, which is read very early, before the stylesheets and the other settings. It is rarely needed. Most changes belong in `ptxprint-mods.tex` instead.

*(Internal ID: `c_usePreModsTex` · Config key: `project/ifusepremodstex`)*

### Advanced tab › Main tab › General

#### Sensitive Project

- **Where:** Advanced tab › Main tab › General
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> In sensitive locations the illustration copyright statement(s) can just contain the appropriate acronyms (e.g. BFBS or DCC) for some artists.
>
> In addition, the PDF's metadata will not contain sensitive project-specific data.

**Explanation:**

Tick this for a project that must be careful about security. The picture credits then use short names (for example "DCC" instead of the artist's full name) where that is allowed. The PDF's hidden information (metadata) does not include project details. Tick it before you make any PDF that will be shared.

*(Internal ID: `c_sensitive` · Config key: `document/sensitive`)*

#### Auto-Correct USFM

- **Where:** Advanced tab › Main tab › General
- **Type:** Checkbox (ticked by default)
- **Description:** Auto-correct common USFM syntax errors
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> PTXprint can analyze the USFM files and automatically correct some common errors in syntax. It will also notify you of errors which are likely to cause the print process to fail - giving you helpful feedback about how to fix the issue before re-trying to print.

**Explanation:**

Checks the USFM and fixes common small mistakes in a temporary copy before typesetting. If it finds serious errors, it shows a "USFM Check Error" message that lists the book and the problem. Leave this ticked. Untick it only if a support person asks you to, for example to find out whether the check itself causes a problem.

*(Internal ID: `c_canonicalise` · Config key: `project/canonicalise`)*

#### Interlinear  &  Code

- **Where:** Advanced tab › Main tab › General
- **Type:** Checkbox (not ticked by default)
- **Description:** Interlinear settings
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Convert Paratext's interlinear data text to ruby (glossing) so that an interlinear text can be printed.
>
> Note that  you may need to adjust the following marker styles:  
>   \rb    for the base text  
>   \gloss|rb    for the gloss text
>
> Note that if this Interlinear option is enabled, then the Spacing Adjustments Between Letters (on the Fonts+Scripts page) will be disabled as these two settings are mutually exclusive.

**Explanation:**

Prints the interlinear glosses from the Paratext Interlinearizer together with the text, so each word has its gloss. You must also type the gloss language code in the box next to it. While this is ticked, the **Between Letters** spacing option on the **Fonts+Script** tab is greyed out. If some verses have unapproved glosses, PTXprint lists the references that need to be approved in Paratext.

*(Internal ID: `c_interlinear` · Config key: `project/interlinear`)*

#### Interlinear language code to use. To find which code to use,...

- **Where:** Advanced tab › Main tab › General
- **Type:** Text box
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Interlinear language code to use. To find which code to use, look in the project folder for a folder named "Interlinear_xy" where xy is the language code. For example if the interlinear has been glossed into English, then the code would be "en".

**Explanation:**

Type the language code of the glosses here, for example `en` for English glosses. You find the code in the project folder: it is the end of the folder name `Interlinear_xx`. Interlinear output only works when this box has a code.

*(Internal ID: `t_interlinearLang` · Config key: `project/interlang`)*

#### Ruby Text Above

- **Where:** Advanced tab › Main tab › General
- **Type:** Checkbox (not ticked by default)
- **Description:** Place Ruby text above words
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Treat ruby text as ruby rather than interlinear text by placing it above the base text rather than below.
>
> Note that  you may need to adjust the following marker styles:  
>   \rb    for the base text  
>   \gloss|rb    for the gloss text Use the shortcut links on the right to locate those styles in the editor.

**Explanation:**

Puts the glosses above the words (like ruby text in East Asian scripts) instead of below them. It only has an effect when **Interlinear** is ticked. Use the **\rb** and **\gloss|rb** links to change the look of the base text and the glosses.

*(Internal ID: `c_ruby` · Config key: `project/ruby`)*

#### \rb

- **Where:** Advanced tab › Main tab › General
- **Type:** Link
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Click to jump to the \rb marker in the style editor to change the formatting of the ruby text.

**Explanation:**

Opens the **Styles** tab at the `\rb` marker. Change the font size or other formatting of the base text (the words that carry glosses) there.

*(Internal ID: `lb_style_rb`)*

#### \gloss|rb

- **Where:** Advanced tab › Main tab › General
- **Type:** Link
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Click to jump to the \gloss|rb marker in the style editor to change the formatting of the glosses for interlinear/ruby text.

**Explanation:**

Opens the **Styles** tab at the `\gloss|rb` style. Change the size, colour or spacing of the glosses there. Glosses are usually smaller than the base text.

*(Internal ID: `lb_style_gloss|rb`)*

#### Only Use English Links

- **Where:** Advanced tab › Main tab › General
- **Type:** Checkbox (not ticked by default)
- **Description:** Only use English links (do not G-translate)
- **View level:** Default and Full views
- **Greyed out when:** “Disable ALL Internet Use” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> When using a non-English interface (such as French, Spanish, Hindi, etc.) most links to external websites get sent via the Google Translate site so that you can read the information in the same language as the selected interface.
>
> Enable this option if Google is blocked in your country, or you simply prefer to read the original page in English.

**Explanation:**

When the PTXprint window uses a language other than English, many web links open through Google Translate. Tick this to open the original English pages directly. This is useful where Google is blocked. It is greyed out when **Disable ALL Internet Use** is ticked.

*(Internal ID: `c_useEngLinks`)*

#### Disable ALL Internet Use

- **Where:** Advanced tab › Main tab › General
- **Type:** Checkbox (not ticked by default)
- **Description:** Disable internet use
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> PTXprint checks for program updates and also contains links to external sites (mainly from the Styles tab and the Help tab). If this is an issue, then check this option to prevent PTXprint from accessing the internet.

**Explanation:**

Stops PTXprint from using the internet. It no longer checks for updates, and the links to websites (for example on the **Help** tab) are hidden. Use it where internet use is expensive, slow or not safe. This setting belongs to your computer, not to the configuration.

*(Internal ID: `c_noInternet`)*

#### Plugins

- **Where:** Advanced tab › Main tab › General
- **Type:** Text box
- **Description:** List of plugins
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Some advanced features load extra code that is not normally needed. List them here if you need to use them. For example, if you are generating a QR code, then you need to add qr to the list of plugins. For a polyglot, you can add polyglot-simplepages

**Explanation:**

Type the names of extra code modules that PTXprint does not load by default, separated by commas or spaces. For example, type `qr` if you want to make QR codes. PTXprint loads the plugins for ornaments, polyglot layouts and covers by itself when you use those features, so you do not need to type them. Leave the box empty unless you know you need a plugin.

*(Internal ID: `t_plugins` · Config key: `project/plugins`)*

#### Use Interlinear Punctuation

- **Where:** Advanced tab › Main tab › General
- **Type:** Checkbox (not ticked by default)
- **Description:** Place Ruby text above words
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Include specifically modified interlinearized punctuation.

**Explanation:**

Used with **Interlinear**. When ticked, punctuation that is stored in the Paratext interlinear data is included in the output. When unticked, PTXprint leaves out those punctuation entries.

*(Internal ID: `c_usePunctuation` · Config key: `project/interpunc`)*

#### Auto-tag Hebrew and Greek words

- **Where:** Advanced tab › Main tab › General
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Auto-tag Hebrew words \wh ... \wh* and Greek words with  \wg ... \wg*
>
> PTXprint can automatically tag all source language words (Hebrew and Greek) with the appropriate markup to ensure they display with the right font and direction for that script.

**Explanation:**

Finds Hebrew and Greek words in the text and marks them with the `\wh` and `\wg` markers. These markers give the words a font that has those letters, and the right text direction. This avoids empty boxes in place of letters. Leave it ticked unless the project already marks these words itself. (Hebrew words are not marked if the project itself uses the Hebrew script; the same applies to Greek.)

*(Internal ID: `c_autoTagHebGrk` · Config key: `project/autotaghebgrk`)*

#### Lock XeTeX Layout Level

- **Where:** Advanced tab › Main tab › General
- **Type:** Checkbox (not ticked by default)
- **Description:** Lock XeTeX Layout Settings
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> This feature enables final typesetting to proceed with minimal risk of change to the final layout by locking the TeX macros to use the current layout logic, which will prevent newer functionality from taking effect in the future. This sets the "Maximum Layout Version" value in the TeXpert Hacks section.

**Explanation:**

Freezes the layout rules at the current version. When you tick it, PTXprint sets **Maximum layout version** (on the **Other** sub-tab, **Page Layout and Spacing**) to the current version. Later updates to PTXprint then do not change how your pages break. Use it near the end of a project, when the layout is final. Unticking it sets **Maximum layout version** back to 0 (always use the newest rules).

*(Internal ID: `c_lockXeTeXLayout` · Config key: `config/lockxetexlayout`)*

#### Lock UI Layout Settings

- **Where:** Advanced tab › Main tab › General
- **Type:** Checkbox (not ticked by default)
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> This feature enables final typesetting to proceed with minimal risk of change to the final layout by disabling various controls (on the layout, fonts and styles tabs) so that settings can't be accidentally changed while doing final page layout.

**Explanation:**

Greys out the main controls that change the page layout: page size, margins, font size, line spacing, columns and gutters, and the whole **Fonts+Script** and **Styles** tabs. Use it during final page adjustments so that nobody changes these by accident. Untick it to make changes again.

*(Internal ID: `c_lockUI4Layout` · Config key: `config/lockui4layout`)*

### Advanced tab › Main tab › Capture tests?

#### Test recording in progress

- **Where:** Advanced tab › Main tab › Capture tests?
- **Type:** Checkbox (not ticked by default)
- **Description:** Sensitive project
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Record PTXPrint options clicked for use in creating an automated test.
>
> Will stop recording when Save is pressed or the checkbox is unticked and a dialog will allow saving the test in zip format.

**Explanation:**

A tool for developers. It records what you click so that it can become an automatic test. When you untick it (or save), PTXprint asks where to save the test as a zip file. Normal users do not need this.

*(Internal ID: `c_testrecording`)*

### Advanced tab

#### Other

- **Where:** Advanced tab
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> To balance columns of text on a page it is possible to specify paragraphs adjustments (shrink or expand):
>
> A Paragraph Adjust List needs to be in this format:  
> MRK 2.7 +1    (i.e. expand the para at Mark 2.7 by one line) MRK 3.20 -1   (i.e. shrink the para at Mark 3:20 by one line) %MARK 4.14 +1   (ignore this line - treat it as a comment) MRK 5.8 +2    (i.e. expand the para at Mark 5.8 by two lines) MRK 6.23 +1[2]  (expand the paragraph AFTER the paragraph  
>                               which contains MRK 6.23 e.g. a heading.) etc. Note that adjusting paragraphs needs to be done right at the end when all other settings have been finalized. Otherwise you are likely to have to re-do it all again.

**Explanation:**

The tab label of the **Other** sub-tab. This sub-tab holds the TeXpert settings, sorted into groups. Click a group name to open it.

*(Internal ID: `l_advOther`)*

#### Filter: show only sections with non-default settings. Sectio...

- **Where:** Advanced tab
- **Type:** Toggle button (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Filter: show only sections with non-default settings. Sections where all values are default will be hidden. Sections with changed values will be expanded. Disable to restore all sections in collapsed state.

**Explanation:**

Shows only the groups that have settings with non-default values, and opens those groups. Inside them, only the changed settings are shown. This is the quickest way to see what has been changed in a configuration. Click it again to show everything. It only works while the **Other** sub-tab is shown.

*(Internal ID: `btn_texpertFilter`)*

### Advanced tab › Other tab › Page Layout and Spacing

#### Maximum layout version

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 10, default 0

**Tooltip (the text shown when you hover the mouse over it):**

> Maximum layout version to use or 0 for any. Used to maintain backward compatibility when the TeX macros have been changed in newer versions of PTXprint.

**Explanation:**

The typesetting code improves with each PTXprint version, and sometimes pages break differently after an update. A value here tells PTXprint to use the layout rules of that older version. 0 means "use the newest rules". Normally you set this with **Lock XeTeX Layout Level** on the **Main** sub-tab, not by hand. Some settings depend on this. For example, from version 6 the enhanced paragraphed footnotes are always used.

*(Internal ID: `s_ptxversion` · Config key: `texpert/ptxversion`)*

#### Legacy 1/14 LineSpacing

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> In the past, SpaceAbove and SpaceBelow were, in effect units of 1/14 of the base line spacing. This has changed so they are now in units of 1/12 of the base line spacing. Enabling this compatibility reverts the units.

**Explanation:**

Use only for old projects. Older versions measured **Space Above** and **Space Below** in styles in units of 1/14 of the line spacing. Now the unit is 1/12. Tick this if an old project's spacing changed after an update and you want the old spacing back.

*(Internal ID: `c_linespacebase` · Config key: `texpert/linespacebase`)*

#### Where to start a new book

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Drop-down list
- **View level:** Default and Full views
- **Choices:** Next page; Same page; Odd page

**Tooltip (the text shown when you hover the mouse over it):**

> Does a scripture book start on a new page, the same page as the previous book (if <65% of page has been used), or an odd page

**Explanation:**

Chooses where a new book starts. **Next page** is the default. **Same page** saves paper, because a short book can start straight after the previous one. **Odd page** starts every book on a right-hand page and adds blank pages where needed. See also **Page full factor**.

*(Internal ID: `fcb_bookstartpage` · Config key: `texpert/bookstartpage`)*

#### Page full factor

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0.3 to 0.9, default 0.65

**Tooltip (the text shown when you hover the mouse over it):**

> This setting is related to how full a page needs to be to force the next book to start on a new page.

**Explanation:**

A number from 0.3 to 0.9 that means "part of the page". With **Same page**, if the previous book already fills more than this part of the page, the next book goes to a new page. The same factor is used when single-column text (such as a book title or introduction) is followed by two-column text. A higher value lets more books share a page. The default is 0.65 (about two thirds of the page).

*(Internal ID: `s_pagefullfactor` · Config key: `texpert/pagefullfactor`)*

#### Where to start a new intro page

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Drop-down list
- **View level:** Default and Full views
- **Choices:** Next page; No page breaks; On an odd page; Grouped

**Tooltip (the text shown when you hover the mouse over it):**

> Does an intro page start on a new page, the same page as the previous book, an odd page, or group all adjacent intro pages into an odd paged group

**Explanation:**

Chooses where a book introduction starts. **No page breaks** lets the introduction follow on the same page. **On an odd page** starts it on a right-hand page. **Grouped** keeps adjacent introductions together and starts the group on an odd page.

*(Internal ID: `fcb_intropagealign` · Config key: `texpert/intropagealign`)*

#### Unbalanced Lines (Max)

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 10, default 3

**Tooltip (the text shown when you hover the mouse over it):**

> Maximum number of unbalanced lines allowed in 2-column layout. Recommended range 1-5.

**Explanation:**

In two-column layout, the largest number of lines by which the two columns may differ in length at the end of a page or section. 0 forces balanced columns. It is only used when **Allow Unbalanced Columns** is ticked on the **Layout** tab. Values from 1 to 5 work best.

*(Internal ID: `s_bottomrag` · Config key: `texpert/bottomrag`)*

#### Variable line spacing maximum stretch

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 10, default 2

**Tooltip (the text shown when you hover the mouse over it):**

> Maximum stretch to insert between lines in variable line spacing in pts

**Explanation:**

How much extra space (in points; 1 pt is about 0.35 mm) can be added between lines to fill a column exactly. It is only used when **Fill Columns** is ticked on the **Layout** tab. A larger value fills columns more easily, but the line spacing looks less even.

*(Internal ID: `s_interlinestretch` · Config key: `texpert/interlinestretch`)*

#### Variable line spacing maximum shrink

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 3, default 0.3

**Tooltip (the text shown when you hover the mouse over it):**

> Maximum shrink to insert between lines in variable line spacing in pts

**Explanation:**

How much the space between lines can be reduced (in points) to fill a column. It is only used when **Fill Columns** is ticked on the **Layout** tab. Keep this small. Lines that are too close together are hard to read.

*(Internal ID: `s_interlineshrink` · Config key: `texpert/interlineshrink`)*

#### No Top Space

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Don’t insert space above headings at the start of a column

**Explanation:**

When ticked (the default), a heading at the top of a column does not get its **Space Above**. This keeps the tops of columns level. Untick it if you want the full space above every heading, even at the top of a column.

*(Internal ID: `c_squashgrid` · Config key: `texpert/squashgrid`)*

#### Suppress pagebreak after bookend-final

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Revert to old behaviour of not ensuring that the whole of the last book is output before back-matter PDFs

**Explanation:**

PTXprint normally ends the last book with a page break, so that any back-matter PDF starts on a new page. Tick this only to return to the old behaviour without that page break.

*(Internal ID: `c_lastnoeject` · Config key: `texpert/lastnoeject`)*

#### Noteline offset (mm)

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 100, default 3

**Tooltip (the text shown when you hover the mouse over it):**

> Gap (mm) between noteline and text

**Explanation:**

The gap in mm between the text and the notelines (the lines for hand-written notes). Notelines are turned on with **Notelines** on the **Layout** tab.

*(Internal ID: `s_notelineoffset` · Config key: `texpert/notelineoffset`)*

#### Noteline margin (mm)

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 100, default 10

**Tooltip (the text shown when you hover the mouse over it):**

> Gap (mm) between noteline and edge of page

**Explanation:**

The gap in mm between the notelines and the edge of the paper. A bigger value gives the lines more space from the edge, so they are not cut off when the pages are trimmed.

*(Internal ID: `s_notelinemargin` · Config key: `texpert/notelinemargin`)*

#### Noteline type

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Drop-down list
- **View level:** Default and Full views
- **Choices:** Solid line; Row of dots

**Tooltip (the text shown when you hover the mouse over it):**

> Sometimes it is preferable to use a series of dots rather than a solid line.

**Explanation:**

Chooses solid lines or rows of dots for the notelines. Dots are lighter on the page and disturb the text less.

*(Internal ID: `fcb_notelinetype` · Config key: `texpert/notelinetype`)*

#### Noteline spacing (mm)

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 25, default 0

**Tooltip (the text shown when you hover the mouse over it):**

> Line spacing between notelines. When set to 0.00 the default line spacing of the document is used.

**Explanation:**

The distance in mm between notelines. 0 uses the line spacing of the body text, so the notelines match the text lines. Increase it if readers need more room to write.

*(Internal ID: `s_noteliney` · Config key: `texpert/noteliney`)*

#### Noteline width (major)

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 10, default 0.5

**Tooltip (the text shown when you hover the mouse over it):**

> Thickness (pt) of major notelines. Specify the colour on the Layout page.

**Explanation:**

How thick the notelines are, in points (1 pt is about 0.35 mm). Thin lines (0.2 to 0.5) look best. Set the colour with **Notelines** on the **Layout** tab.

*(Internal ID: `s_notelinemajor` · Config key: `texpert/notelinemajor`)*

#### Double Sided Layout

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This setting can be disabled to turn off inner/outer margins, forcing the inner/outer gutter, and Notelines to always appear on the same side of the printed page.

**Explanation:**

When ticked (the default), odd and even pages are treated differently: inner and outer margins swap, and the headers and footers for even pages are used. Untick it for pages printed on one side only. Then every page uses the same margins, the odd-page header and footer, and notelines on the same side.

*(Internal ID: `c_doublesided` · Config key: `texpert/doublesided`)*

#### Maximum parallel processes

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Number box
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The maximum number of parallel processes to use for example when page filling

**Explanation:**

How many printing jobs PTXprint can run at the same time, for example when the page filler works on several books, or when you print several publications. The default depends on the number of processors in your computer. Lower it if your computer becomes slow or runs out of memory.

*(Internal ID: `s_maxproc` · Config key: `texpert/maxproc`)*

#### Maximum Filling Time (mins)

- **Where:** Advanced tab › Other tab › Page Layout and Spacing
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 100, default 0

**Tooltip (the text shown when you hover the mouse over it):**

> Stop page filling a book after this many minutes

**Explanation:**

This setting is meant to stop page filling of one book after a number of minutes. In the current code we could not confirm that it is used. To limit the time of the page filler, use **Time limit for the whole job (minutes)** in the **Automatic Page Filler** group.

*(Internal ID: `s_maxfilltime` · Config key: `texpert/maxfilltime`)*

### Advanced tab › Other tab › Chapter and Verse

#### Position of marginal verse hyphen if any

- **Where:** Advanced tab › Other tab › Chapter and Verse
- **Type:** Drop-down list
- **View level:** Default and Full views
- **Choices:** Always down; Always up; Up on left; Up on right; No hyphens

**Tooltip (the text shown when you hover the mouse over it):**

> Insert or not a marginal verse hyphen in verse ranges, whether on the first or second line

**Explanation:**

For marginal verse numbers (verse numbers placed in the margin) with a verse range, such as 3-4. This chooses whether the hyphen goes on the first or the second line, or is left out. **Up on left** and **Up on right** put it on the first line only in the left or right margin. Marginal verses are turned on with **Marginal Verses** on the **Body** tab.

*(Internal ID: `fcb_vhyphenmode` · Config key: `texpert/vhyphenmode`)*

#### Gutter space reduction for marginal verses

- **Where:** Advanced tab › Other tab › Chapter and Verse
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> If false, the space for marginal verses is taken from the column. If true, some space for marginal verses is taken from the margins or rule gutter

**Explanation:**

For marginal verse numbers. When unticked (the default), the space for the verse numbers is taken from the text column, so the column becomes narrower. When ticked, part of the space is taken from the margin or the gutter (the space between columns) instead, so the text keeps more width.

*(Internal ID: `c_mverseismargin` · Config key: `texpert/mverseismargin`)*

#### Auto Calc Optimum Chapter Size

- **Where:** Advanced tab › Other tab › Chapter and Verse
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Attempt to automatically calculate drop chapter number size

**Explanation:**

When ticked (the default), PTXprint calculates the size of a large chapter number so that it fills the height of two lines exactly. This happens when the chapter number style (`\c`) is not much larger than the body text. Untick it if you want to set the chapter number size yourself on the **Styles** tab.

*(Internal ID: `c_calcchapsize` · Config key: `texpert/calcchapsize`)*

#### Don't hang verse one beside a chapter (in poetry)

- **Where:** Advanced tab › Other tab › Chapter and Verse
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Hanging verses into a chapter number can result in clashes, depending on the after-chapter space. If so, then turn off hanging verse numbers for the first verse (in poetry only).

**Explanation:**

In poetry with hanging verse numbers, verse 1 can clash with a large chapter number. When ticked (the default), verse 1 does not hang. Untick it only if the after-chapter space is wide enough and you want verse 1 to hang like the others.

*(Internal ID: `c_nohangvone` · Config key: `texpert/nohangvone`)*

#### Alternate verse numbers also hang

- **Where:** Advanced tab › Other tab › Chapter and Verse
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> If there is an alternative verse and the current verse is hanging, does the alternate hang?

**Explanation:**

When a verse number hangs in the margin and also has an alternative verse number (`\va`), this decides whether the alternative number hangs too. Most projects do not use alternative verse numbers.

*(Internal ID: `c_hangva` · Config key: `texpert/hangva`)*

#### After chapter space factor

- **Where:** Advanced tab › Other tab › Chapter and Verse
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -0.2 to 1, default 0.25

**Tooltip (the text shown when you hover the mouse over it):**

> This sets the gap between the chapter number and the text following. The setting here is a multiple of the main body text size as specified in layout.

**Explanation:**

The gap between a large chapter number and the text next to it, as a part of the body text size. 0.25 means a quarter of the text size. Increase it if the text looks crowded against the chapter number. Negative values move the text closer.

*(Internal ID: `s_afterchapterspace` · Config key: `texpert/afterchapterspace`)*

#### After verse space factor

- **Where:** Advanced tab › Other tab › Chapter and Verse
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -0.2 to 1, default 0.15

**Tooltip (the text shown when you hover the mouse over it):**

> This sets the gap between the verse number and the text following. The setting here is a multiple of the main body text size as specified in layout.

**Explanation:**

The gap between a verse number and the text that follows it, as a part of the body text size. The default 0.15 is a small space. Change it only if verse numbers look too close to the text, or too far from it.

*(Internal ID: `s_afterversespace` · Config key: `texpert/afterversespace`)*

### Advanced tab › Other tab › Body Text

#### Allow Indent Para with Cutouts

- **Where:** Advanced tab › Other tab › Body Text
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Allow indented paragraphs at chapter start with cutouts

**Explanation:**

Decides whether the first paragraph of a chapter keeps its indent when it sits next to a large chapter number (a cutout). When unticked (the default), the lines next to the chapter number are not indented. Tick it to keep the paragraph's normal indent there too.

*(Internal ID: `c_chapindent` · Config key: `texpert/chapindent`)*

#### Allow Indent Para After Heading

- **Where:** Advanced tab › Other tab › Body Text
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Allow indented paragraphs following a heading

**Explanation:**

When ticked (the default), the first paragraph after a heading is indented like any other paragraph. Untick it if you want the first line after a heading to start at the margin, which is a common book style.

*(Internal ID: `c_afterheadindent` · Config key: `texpert/afterheadindent`)*

#### Maximum orphan word length

- **Where:** Advanced tab › Other tab › Body Text
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 1 to 20, default 8

**Tooltip (the text shown when you hover the mouse over it):**

> Maximum length of the word that will receive orphan protection at the end of a paragraph

**Explanation:**

An orphan word is a short word left alone on the last line of a paragraph. When **Prevent Orphan Words** is ticked on the **Body** tab, PTXprint joins the last word to the word before it, so they stay on the same line. This number is the longest word (in characters) that gets this protection. Longer last words can stand alone.

*(Internal ID: `s_maxorphanlength` · Config key: `texpert/maxorphanlength`)*

#### Bad space penalty

- **Where:** Advanced tab › Other tab › Body Text
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -10000 to 10000, default 100

**Tooltip (the text shown when you hover the mouse over it):**

> Penalty for a bad (but not impossible) place to break

**Explanation:**

The penalty for a line break at a "bad" space. PTXprint uses these spaces, for example, to keep orphan words with the word before them. A higher value makes such a break less likely. 10000 forbids it. A negative value encourages a break there.

*(Internal ID: `s_badsppen` · Config key: `texpert/badsppen`)*

#### Optional break penalty

- **Where:** Advanced tab › Other tab › Body Text
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 10000, default 300

**Tooltip (the text shown when you hover the mouse over it):**

> Penalty for the optional break

**Explanation:**

The strength of an optional line break. This is the place you mark with `//` in the USFM text. A higher value makes the break more attractive. Change it only if lines break at those places too often or too seldom.

*(Internal ID: `s_optbkpen` · Config key: `texpert/optbkpen`)*

#### Hyphenation threshold

- **Where:** Advanced tab › Other tab › Body Text
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -1 to 10000, default 100

**Tooltip (the text shown when you hover the mouse over it):**

> Paragraph badness threshold before trying hyphenation. Set to -1 to always hyphenate

**Explanation:**

Hyphenation is tried only for paragraphs that cannot be set well without it. This number says how bad a paragraph must look before PTXprint tries hyphenation. Lower values hyphenate more often. -1 means "always try hyphenation". It only matters when hyphenation is turned on.

*(Internal ID: `s_pretolerance` · Config key: `texpert/pretolerance`)*

#### Penalty for inserting hyphen

- **Where:** Advanced tab › Other tab › Body Text
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -9999 to 10000, default 50

**Tooltip (the text shown when you hover the mouse over it):**

> Hyphenation penalty

**Explanation:**

How much PTXprint avoids breaking a word with a hyphen. A higher value gives fewer hyphens but may give wider word spaces. A value of 10000 or more stops hyphenation completely.

*(Internal ID: `s_hyphenpenalty` · Config key: `texpert/hyphenpenalty`)*

#### Double hyphenation penalty

- **Where:** Advanced tab › Other tab › Body Text
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 1e+06, default 10000

**Tooltip (the text shown when you hover the mouse over it):**

> Penalty for consecutive hyphenation across two lines

**Explanation:**

An extra penalty when two lines in a row end with a hyphen. A higher value makes this rarer. The default is already high.

*(Internal ID: `s_doublehyphendemerits` · Config key: `texpert/doublehyphendemerits`)*

#### Use loc attrib on ref to make a link

- **Where:** Advanced tab › Other tab › Body Text
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The ref character style can include an attribute like loc="GEN 1:2". Should this be used to make a clickable link?

**Explanation:**

Some texts mark references with `\ref` and a `loc` attribute (for example GEN 1:2). When ticked, PTXprint turns these into links that you can click in the PDF to jump to that verse.

*(Internal ID: `c_userefloc` · Config key: `texpert/userefloc`)*

#### Use href-link attrib on jmp to make a link

- **Where:** Advanced tab › Other tab › Body Text
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The jmp character style can include an attribute like href-link="https://my.web.site/". Should this be used to make a clickable link?

**Explanation:**

When the text has `\jmp` markers with a web address (`href-link`), this turns them into clickable web links in the PDF. Untick it for a printed book where active links are not wanted.

*(Internal ID: `c_hreflink` · Config key: `texpert/hreflink`)*

#### Box style for URL links

- **Where:** Advanced tab › Other tab › Body Text
- **Type:** Drop-down list
- **View level:** Default and Full views
- **Choices:** Underline only; No line; Solid line; Row of dots; Dashed line; Viewer default

**Tooltip (the text shown when you hover the mouse over it):**

> Active web links in PDFs are marked by either a box (solid, dashed or dotted line) or an underline. Your viewer probably has a default setting. Set the colour with \def\URLLinkBorderCol{0.9 0.5 0.5} or similar in ptxprint-mods.tex.

**Explanation:**

How web links are marked in the PDF on screen: underline, a box, dots, dashes, nothing, or the PDF viewer's own default. This mark is only visible on screen. It is not printed. The link colour can only be changed by an expert, in `ptxprint-mods.tex`.

*(Internal ID: `fcb_urllinkborderstyle` · Config key: `texpert/urllinkborderstyle`)*

#### Box style for GOTO links

- **Where:** Advanced tab › Other tab › Body Text
- **Type:** Drop-down list
- **View level:** Default and Full views
- **Choices:** Underline only; No line; Solid line; Row of dots; Dashed line; Viewer default

**Tooltip (the text shown when you hover the mouse over it):**

> Active internal links in PDFs are marked by either a box (solid, dashed or dotted line) or an underline. Your viewer probably has a default setting. Set the colour with \def\GOTOLinkBorderCol{0.9 0.5 0.5} or similar in ptxprint-mods.tex.

**Explanation:**

How links inside the PDF (for example from a cross-reference to a verse) are marked on screen. The choices are the same as for web links. These marks are not printed.

*(Internal ID: `fcb_gotolinkborderstyle` · Config key: `texpert/gotolinkborderstyle`)*

### Advanced tab › Other tab › Fonts and Underline

#### Use glyph metrics

- **Where:** Advanced tab › Other tab › Fonts and Underline
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> PTXprint can use either the actual glyph metrics in a line or the font metrics to calculate line heights and depths. Font metrics gives more consistent results.

**Explanation:**

Decides how PTXprint measures the height of a line. Unticked (the default), it uses the font's design values, so every line is measured the same way and the spacing is even. Ticked, it uses the real shapes of the letters in that line. Leave it unticked unless a support person suggests otherwise.

*(Internal ID: `c_useglyphmetrics` · Config key: `texpert/useglyphmetrics`)*

#### Use system fonts

- **Where:** Advanced tab › Other tab › Fonts and Underline
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Use fonts from your system as well as your project. Note that you need to restart PTXprint for this setting to take effect.

**Explanation:**

When ticked (the default), PTXprint can use fonts installed on your computer as well as fonts in the project. Untick it to use only fonts stored with the project, so that the result is the same on every computer. You must restart PTXprint after you change this.

*(Internal ID: `c_usesysfonts` · Config key: `texpert/usesysfonts`)*

#### Underline thickness (em)

- **Where:** Advanced tab › Other tab › Fonts and Underline
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0.01 to 0.5, default 0.05

**Tooltip (the text shown when you hover the mouse over it):**

> This sets the thickness of the text underline, (measured in ems).

**Explanation:**

How thick underlines are, as a part of the text size (em – the size of the font). The default 0.05 is a thin line.

*(Internal ID: `s_underlinethickness` · Config key: `texpert/underlinethickness`)*

#### Underline vertical position (em)

- **Where:** Advanced tab › Other tab › Fonts and Underline
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -1 to 1, default 0.1

**Tooltip (the text shown when you hover the mouse over it):**

> This sets how far (in ems) the underline is below the text and what it is relative to. If negative, it is the distance below the baseline. If positive (or zero), it is the distance below the bottom of any descenders.

**Explanation:**

How far below the text the underline sits, in em. With a positive value (or 0), it is measured from the bottom of the letters with descenders (such as g and p). With a negative value, it is measured from the baseline, the line the letters sit on. Increase it if underlines touch the letters.

*(Internal ID: `s_underlineposition` · Config key: `texpert/underlineposition`)*

#### Underline Spaces

- **Where:** Advanced tab › Other tab › Fonts and Underline
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Underline spaces in underlined runs

**Explanation:**

When ticked (the default), the spaces between underlined words are underlined too, so the line is unbroken. Untick it to underline only the words.

*(Internal ID: `c_underlnsp` · Config key: `texpert/underlnsp`)*

#### Log font creation

- **Where:** Advanced tab › Other tab › Fonts and Underline
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Create <jobname>.fontusage in the local/ptxprint/<config>/ directory, which will list the page number and exact font definition when each new style is first used.

**Explanation:**

Makes a file that lists each font used and the page where each style first uses it. It is useful for finding where an unexpected font comes from. It does not change the PDF. A support person may ask you to turn this on.

*(Internal ID: `c_logfontusage` · Config key: `texpert/logfontusage`)*

### Advanced tab › Other tab › Footnotes, Cross-references, Study Notes

#### Mid-Page Footnotes

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Should footnotes go before a single-double column transition

**Explanation:**

For pages where single-column text (for example a book introduction) is followed by two-column text. When ticked, the footnotes of the single-column part are placed right after that part, in the middle of the page. When unticked (the default), all notes go to the bottom of the page.

*(Internal ID: `c_midnotes` · Config key: `texpert/midnotes`)*

#### Final Page Notes Down

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Push notes on the final page to the bottom of the page

**Explanation:**

On the last page of a book, the text may end high on the page. When ticked, the footnotes on that page are pushed down to the bottom margin. When unticked (the default), the notes follow straight after the text.

*(Internal ID: `c_fnotesdown` · Config key: `texpert/fnotesdown`)*

#### Reset Callers at Each Book

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Re-start the footnote and cross-reference callers at the start of each book

**Explanation:**

When ticked (the default), the note callers (such as a, b, c) start again at the start of each book. Untick it to continue the sequence across books.

*(Internal ID: `c_bookresetcallers` · Config key: `texpert/bookresetcallers`)*

#### Endnotes at Each Book

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Output endnotes at the end of each book

**Explanation:**

When ticked (the default), endnotes are printed at the end of each book. Untick it to collect all endnotes at the end of the last book.

*(Internal ID: `c_neachbook` · Config key: `texpert/neachbook`)*

#### Enhanced paragraphed footnotes

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Paragraphed footnotes which allow \fp to work and also the ifparnotes... controls below. Causes some spacing differences compared to old-style.

**Explanation:**

Turns on a newer way of making paragraphed footnotes (several notes run together in one paragraph). It allows the `\fp` marker and the other paragraphed-note settings in this group. With the current layout version this is already always on. The check box only matters when **Maximum layout version** is set to 5 or lower.

*(Internal ID: `c_newparnotes` · Config key: `texpert/newparnotes`)*

#### Remove depth above paragraphed notes

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Kern away (kill) the glyph/font depth of note types before paragraphed notes, using the value of \prevdepth

**Explanation:**

Fine-tunes the space above paragraphed notes. When ticked (the default), PTXprint removes the space below the letters of the note type above them. This keeps the space between different note types even. Change it only to solve a specific spacing problem.

*(Internal ID: `c_parntkillpd` · Config key: `texpert/parntkillpd`)*

#### Remove depth after paragraphed notes

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Kill the depth of (the last row of) paragraphed note styles. Paragraphed notes will use the margin as their baseline.

**Explanation:**

When ticked, the last line of paragraphed notes sits right on the bottom margin. When unticked (the default), the space for letters below the baseline (such as g and p) is kept.

*(Internal ID: `c_parntkilldepth` · Config key: `texpert/parntkilldepth`)*

#### Use grid not font/glyph height at rule

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> If true, the footnote rule is positioned relative to the hypothetical baseline above the topmost footnote, rather than relative to the glyph/font height.

**Explanation:**

Decides how the footnote rule (the line above the notes) is positioned. When ticked, it is placed relative to the line grid. When unticked (the default), it is placed relative to the height of the letters in the first note. Change it only if the space between the rule and the notes looks wrong.

*(Internal ID: `c_parntruletopskip` · Config key: `texpert/parntruletopskip`)*

#### Use grid not font/glyph height between notes

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> If true, then the \InterNoteSpace is relative to the hypothetical baseline above the topmost footnote, rather than the glyph/font height. \InterNoteSpace is triggered between note styles.

**Explanation:**

Decides how the space between two different note types (for example footnotes and cross-references) is measured. When ticked (the default), it is measured from the line grid. This gives the same space everywhere. Untick it to measure from the height of the letters instead.

*(Internal ID: `c_parntmidtopskip` · Config key: `texpert/parntmidtopskip`)*

#### Use glyph height not font height in footnotes

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Does the note use the font's descender design parameter, or the actual bottom of the glyph. If the former (and depth is not killed), then the bottom of notes have a common baseline across pages. If the latter, then the glyphs sit as close to the bottom margin as they can, which may permit an extra line of text.

**Explanation:**

Decides how the bottom of the notes is measured. Unticked (the default), PTXprint uses the font's design value, so the last line of notes is at the same height on every page. Ticked, it uses the real bottom of the letters. The notes then sit as low as possible, which sometimes leaves room for an extra line of text.

*(Internal ID: `c_fnxugm` · Config key: `texpert/fnxugm`)*

#### Last Note: interlinepenalty

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -9999 to 10000, default 10000

**Tooltip (the text shown when you hover the mouse over it):**

> Penalty for breaking between lines of the last footnote.

**Explanation:**

Controls whether the last footnote on a page can be split between two pages. The default 10000 means "never split it". Lower values allow a split. This can help fill pages that have many notes.

*(Internal ID: `s_lastnoteinterlinep` · Config key: `texpert/lastnoteinterlinep`)*

#### Last Note: widowpenalty

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -9999 to 10000, default 10000

**Tooltip (the text shown when you hover the mouse over it):**

> Extra penalty for breaking at the last line of the last footnote.

**Explanation:**

An extra penalty for a split that leaves only the last line of the last footnote on the next page. The default 10000 forbids this.

*(Internal ID: `s_lastnotewidowp` · Config key: `texpert/lastnotewidowp`)*

#### Last Note: clubpenalty

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -9999 to 10000, default 10000

**Tooltip (the text shown when you hover the mouse over it):**

> Extra penalty for breaking at the first line of the last footnote.

**Explanation:**

An extra penalty for a split that leaves only the first line of the last footnote on the page. The default 10000 forbids this.

*(Internal ID: `s_lastnoteclubp` · Config key: `texpert/lastnoteclubp`)*

#### Last Note: penalty at par

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -9999 to 10000, default 100

**Tooltip (the text shown when you hover the mouse over it):**

> Penalty for breaking at an explicit footnote-paragraph in the last footnote.

**Explanation:**

The penalty for splitting the last footnote at a place where the note itself starts a new paragraph. The default 100 allows this more easily than a split in the middle of a paragraph.

*(Internal ID: `s_lastnoteparp` · Config key: `texpert/lastnoteparp`)*

#### Split notes: Shortest note to shave

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 100, default 2

**Tooltip (the text shown when you hover the mouse over it):**

> If footnotes might be shaved, how many lines must it be?

**Explanation:**

When notes do not fit, PTXprint can split ("shave") a note and move part of it to the next page. This is the shortest note, in lines, that may be split. Notes shorter than this are kept whole.

*(Internal ID: `s_nshaveshort` · Config key: `texpert/nshaveshort`)*

#### Split notes: min lines to move.

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 100, default 2

**Tooltip (the text shown when you hover the mouse over it):**

> If a footnote is being shaved (split onto next page), what is the minimum number of lines to move?

**Explanation:**

When a note is split, at least this many lines must move to the next page. This avoids moving a single lonely line.

*(Internal ID: `s_nshavemin` · Config key: `texpert/nshavemin`)*

#### Split notes: note lines to stay

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 100, default 2

**Tooltip (the text shown when you hover the mouse over it):**

> If a footnote is being shaved (split onto next page), how many lines of (all) notes must remain on the page?

**Explanation:**

When a note is split, at least this many lines of notes must stay on the current page.

*(Internal ID: `s_nshavestay` · Config key: `texpert/nshavestay`)*

#### Study note factor-Single column

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 2100, default 400

**Tooltip (the text shown when you hover the mouse over it):**

> To avoid needless cylces/underful pages, what portion of a study note's height-estimate should TeX apply when gathering input in single-column mode? (100=10percent)

**Explanation:**

While PTXprint collects text for a page, it guesses how much space the study notes will need. This value is that guess as a portion of the full estimate, for single-column text (100 = 10%, 1000 = 100%). Lower values can give fuller pages but more work. Higher values can leave pages underfull. Change it only on advice.

*(Internal ID: `s_footnotemulsts` · Config key: `texpert/footnotemulsts`)*

#### Study note factor-Two column

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 2100, default 800

**Tooltip (the text shown when you hover the mouse over it):**

> To avoid needless cylces/underful pages, what portion of a study note's height-estimate should TeX apply when gathering input in two-column mode? (100=10percent)

**Explanation:**

Same as **Study note factor-Single column**, but for two-column text.

*(Internal ID: `s_footnotemulstt` · Config key: `texpert/footnotemulstt`)*

#### Study note factor-Diglot

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 2100, default 500

**Tooltip (the text shown when you hover the mouse over it):**

> To avoid needless cylces/underful pages, what portion of a study note's height-estimate should TeX apply when gathering diglot input? (100=10percent)

**Explanation:**

Same as **Study note factor-Single column**, but for diglot text.

*(Internal ID: `s_footnotemulstd` · Config key: `texpert/footnotemulstd`)*

#### Footnote factor-Single column

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 2100, default 400

**Tooltip (the text shown when you hover the mouse over it):**

> To avoid needless cylces/underful pages, what portion of a note's height-estimate should TeX apply when gathering input in single-column mode? (100=10percent)

**Explanation:**

Same idea as the study note factors, but for ordinary footnotes in single-column text (100 = 10%). Change it only on advice.

*(Internal ID: `s_footnotemuls` · Config key: `texpert/footnotemuls`)*

#### Footnote factor-Two column

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 2100, default 800

**Tooltip (the text shown when you hover the mouse over it):**

> To avoid needless cylces/underful pages, what portion of a note's height-estimate should TeX apply when gathering input in two-column mode? (100=10percent)

**Explanation:**

The footnote space estimate for two-column text. Change it only on advice.

*(Internal ID: `s_footnotemult` · Config key: `texpert/footnotemult`)*

#### Footnote factor-Diglot

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 2100, default 10

**Tooltip (the text shown when you hover the mouse over it):**

> To avoid needless cylces/underful pages, what portion of a note's height-estimate should TeX apply when gathering diglot input? (100=10percent)

**Explanation:**

The footnote space estimate for diglot text. Change it only on advice.

*(Internal ID: `s_footnotemuld` · Config key: `texpert/footnotemuld`)*

#### Footnote factor-Centre column

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 2100, default 1

**Tooltip (the text shown when you hover the mouse over it):**

> To avoid needless cylces/underful pages, what portion of a note's height-estimate should TeX apply when gathering centre-column notes? (100=10percent)

**Explanation:**

The space estimate for notes in a centre column (for example cross-references between two columns). These notes do not take space from the text column, so the default is very low.

*(Internal ID: `s_footnotemulc` · Config key: `texpert/footnotemulc`)*

#### Distance of margin notes from text

- **Where:** Advanced tab › Other tab › Footnotes, Cross-references, Study Notes
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 100, default 6

**Tooltip (the text shown when you hover the mouse over it):**

> The size of the gap between the margin notes and the text

**Explanation:**

The gap between the main text and the margin notes. A larger number moves the margin notes further away from the text. Margin notes are turned on, and their column width set, on the **Layout** tab in the **Page Setup** area (**Margin Notes Col Width (mm)** and **Margin Notes on Left/Inner**). Change it if the notes look too close to, or too far from, the text.

*(Internal ID: `s_marginnotesgap` · Config key: `texpert/marginnotesgap`)*

### Advanced tab › Other tab › Diglot

#### Balance diglot/polyglot notes

- **Where:** Advanced tab › Other tab › Diglot
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> When there's a note on column R (for example), does that reduce the space from other columns?

**Explanation:**

In a diglot or polyglot, when one column has a note, this decides whether the other columns lose the same space. Tick it to keep the bottoms of all columns level. Untick it (the default) so that each column uses its own space.

*(Internal ID: `c_diglotbalnotes` · Config key: `texpert/diglotbalnotes`)*

#### Diglot/polyglot merged paragraphed notes are RTL

- **Where:** Advanced tab › Other tab › Diglot
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> When merged notes are not shown as individual paragraphs, the result must be arranged as though RTL or LTR (however the induvidual notes are structured). This defines the paragraph alignment.

**Explanation:**

In a diglot or polyglot where the notes of the columns are merged into one paragraph, this sets the direction of that paragraph. Tick it when the merged notes should read right-to-left. Getting this wrong gives badly arranged notes, so match it to the language of the notes.

*(Internal ID: `c_mergednotesrtl` · Config key: `texpert/mergednotesrtl`)*

#### Adjust Versification of Projects

- **Where:** Advanced tab › Other tab › Diglot
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> If versification differs between projects, adjust diglot/polyglot projects to match the primary (L) project.

**Explanation:**

When the projects in a diglot or polyglot use different versification (verse numbering), PTXprint moves the verses of the other projects to match the primary (L) project. This keeps matching verses side by side. Leave it ticked unless the projects already use the same versification.

*(Internal ID: `c_reversify` · Config key: `texpert/reversify`)*

#### Keep existing verse numbers (as \vp)

- **Where:** Advanced tab › Other tab › Diglot
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> When adjusting versification, show the original verse numbers in their new (adjusted) location.

**Explanation:**

When versification is adjusted, verses may move to a new place. When ticked, the original verse numbers are still shown, so readers see the numbers of their own translation.

*(Internal ID: `c_showvpvrse` · Config key: `texpert/showvpvrse`)*

#### Show old chapter numbers if changed (in \vp)

- **Where:** Advanced tab › Other tab › Diglot
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> When adjusting versification, show the adjusted chapter numbers (only) if they have changed.

**Explanation:**

When versification is adjusted and a verse moves to a different chapter, the old chapter number is shown with the verse number. This only happens when the chapter has changed.

*(Internal ID: `c_showvpchap` · Config key: `texpert/showvpchap`)*

#### Show Diglot Trace Marks

- **Where:** Advanced tab › Other tab › Diglot
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Insert visible trace marks in diglot output

**Explanation:**

Puts visible marks in a diglot PDF where the text pieces of the columns are joined. It is a tool for finding layout problems. Turn it off for the final PDF.

*(Internal ID: `c_vistrace` · Config key: `texpert/vistrace`)*

#### Extra Trace Mark Info

- **Where:** Advanced tab › Other tab › Diglot
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Add extra information to diglot trace marks. (debugging only - can alter layout)

**Explanation:**

Adds more information to the diglot trace marks. It is for debugging only and can change the layout.

*(Internal ID: `c_vistracex` · Config key: `texpert/vistracex`)*

#### Diglot Shading Padding

- **Where:** Advanced tab › Other tab › Diglot
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -20 to 20, default 3

**Tooltip (the text shown when you hover the mouse over it):**

> The amount of side padding (pt) on the shaded background of a diglot

**Explanation:**

The extra space (in points) at the sides of the background colour shading of diglot columns. A larger value makes the shading extend further beyond the text. Negative values make it narrower than the text.

*(Internal ID: `s_diglotcolourpad` · Config key: `texpert/diglotcolourpad`)*

#### How does text-border behave in diglots?

- **Where:** Advanced tab › Other tab › Diglot
- **Type:** Drop-down list
- **View level:** Default and Full views
- **Choices:** Borders start at body text; Borders include book intros; Wide book intros for per-column textborders

**Tooltip (the text shown when you hover the mouse over it):**

> Historically, diglot text-borders put the border around book introductions. This control allows that (substandard) behaviour to be chosen, and also allows  experimental code to make books with per-column textborders use full-width text for introductory text.

**Explanation:**

How a text border behaves in a diglot. **Borders start at body text** (the default) leaves book introductions outside the border. **Borders include book intros** is the old behaviour. **Wide book intros for per-column textborders** is experimental: introductions use the full page width when each column has its own border.

*(Internal ID: `fcb_textbordermode` · Config key: `texpert/textbordermode`)*

#### Unprintable page recovery.

- **Where:** Advanced tab › Other tab › Diglot
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -1 to 10, default 2

**Tooltip (the text shown when you hover the mouse over it):**

> If notes / figures make a page unprintable: -1: immediately stop; 0: print failed contents and try to struggle on; >0 grow page height by up to N lines.

**Explanation:**

What to do when notes or pictures make a page impossible to print. -1 stops printing at once. 0 prints what it can and continues. A value above 0 allows the page to grow by up to that many lines, so it can be printed. Grown pages may extend into the bottom margin, so check them.

*(Internal ID: `s_growunprintable` · Config key: `texpert/growunprintable`)*

#### Page-full test.

- **Where:** Advanced tab › Other tab › Diglot
- **Type:** Drop-down list
- **View level:** Default and Full views
- **Choices:** 1xBiggest baseline; 2xSmallest baseline; 2xBiggest baseline; 3xSmallest baseline

**Tooltip (the text shown when you hover the mouse over it):**

> When a (non-title) chunk has finished, the amount of unused space below which diglot will immediately output a page,  rather than trying to fit the next chunk. (irrespective of how short it is). Higher values encourage underfilled pages, but can prevent orphaning of the 1st line of poetry.

**Explanation:**

In a diglot, after a piece of text is finished, if less than this much space is left on the page, PTXprint ends the page instead of trying to fit the next piece. Larger values give more underfilled pages, but can stop the first line of a poem being left alone at the bottom. Note: in the current version we could not confirm that a change here reaches the typesetting code.

*(Internal ID: `fcb_pagefulltest` · Config key: `texpert/pagefulltest`)*

### Advanced tab › Other tab › Pictures, Figures, Images, Sidebars

#### Default Figures Top Left

- **Where:** Advanced tab › Other tab › Pictures, Figures, Images, Sidebars
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Default figure positions to top left

**Explanation:**

When a picture in two-column layout has no usable position, PTXprint puts it at the top of a column, alternating between left and right. When ticked (the default), it starts with the left column.

*(Internal ID: `c_figleft` · Config key: `texpert/figleft`)*

#### Ref Before Caption

- **Where:** Advanced tab › Other tab › Pictures, Figures, Images, Sidebars
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Output reference before caption

**Explanation:**

Puts the verse reference before the caption text instead of after it.

*(Internal ID: `c_captreffirst` · Config key: `texpert/captreffirst`)*

#### Show Caption Before Image

- **Where:** Advanced tab › Other tab › Pictures, Figures, Images, Sidebars
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Output caption before image

**Explanation:**

Puts the caption above the picture instead of below it.

*(Internal ID: `c_captfirst` · Config key: `texpert/captfirst`)*

#### Space (pt) beside cutout/sidebar

- **Where:** Advanced tab › Other tab › Pictures, Figures, Images, Sidebars
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 50, default 10

**Tooltip (the text shown when you hover the mouse over it):**

> This sets the default gap (pt) between the body text and the side of a figure/sidebar in a cutout.

**Explanation:**

The default gap (in points) between the text and a picture or sidebar that sits in a cutout (a space cut into the side of the text). It is used when a picture or sidebar does not set its own space. **Default space beside picture** sets the same value, and it wins when it is changed from its default.

*(Internal ID: `s_cutouterpadding` · Config key: `texpert/cutouterpadding`)*

#### Space between picture & caption

- **Where:** Advanced tab › Other tab › Pictures, Figures, Images, Sidebars
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -10 to 20, default 0

**Tooltip (the text shown when you hover the mouse over it):**

> Increase/Reduce the gap between figures and their captions

**Explanation:**

Adds space between a picture and its caption (positive values) or removes space (negative values), in points.

*(Internal ID: `s_captionadj` · Config key: `texpert/captionadj`)*

#### Default space beside picture

- **Where:** Advanced tab › Other tab › Pictures, Figures, Images, Sidebars
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 100, default 10

**Tooltip (the text shown when you hover the mouse over it):**

> Picture horizontal margin*2

**Explanation:**

The default horizontal space (in points) beside a picture. This sets the same value as **Space (pt) beside cutout/sidebar**. When you change this one from its default (10), it is used instead.

*(Internal ID: `s_spbeside` · Config key: `texpert/spbeside`)*

#### Show comprehensive illustration credits

- **Where:** Advanced tab › Other tab › Pictures, Figures, Images, Sidebars
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Instead of using the catch-all phrasing 'All other illustrations by...' show a comprehensive list of every artist and all pages that contain their illustrations.

**Explanation:**

Picture credits normally list the main artists and then say "All other illustrations by...". Tick this to list every artist with all the pages that have their pictures.

*(Internal ID: `c_allpicredits` · Config key: `texpert/allpicredits`)*

### Advanced tab › Other tab › PDF Options, Covers, Show/Hide

#### No PDF Bookmarks

- **Where:** Advanced tab › Other tab › PDF Options, Covers, Show/Hide
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Don’t output PDF bookmarks

**Explanation:**

Stops PTXprint from making bookmarks (the list of books and chapters in the side panel of a PDF viewer). Some printers ask for a PDF without bookmarks.

*(Internal ID: `c_noactions` · Config key: `texpert/noactions`)*

#### Allow Active Links in PDF

- **Where:** Advanced tab › Other tab › PDF Options, Covers, Show/Hide
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Make links active inside PDF

**Explanation:**

When ticked (the default), links in the PDF work when you click them (for example cross-references and web links). Untick it for a PDF that is only for printing.

*(Internal ID: `c_actions` · Config key: `texpert/actions`)*

#### Use Book Codes in PDF Bookmarks

- **Where:** Advanced tab › Other tab › PDF Options, Covers, Show/Hide
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Use book codes instead of book names in bookmarks

**Explanation:**

Uses book codes (such as GEN, MAT) instead of book names in the PDF bookmarks. This can help when the book names are long or in a script the PDF viewer cannot show.

*(Internal ID: `c_refbkmks` · Config key: `texpert/refbkmks`)*

#### Disable Transparency in PDF

- **Where:** Advanced tab › Other tab › PDF Options, Covers, Show/Hide
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Disable transparency output in PDF

**Explanation:**

Some printers cannot handle transparent colours. When ticked, PTXprint changes each transparent colour into a solid colour that looks the same on white paper. Anything behind a transparent item is then hidden, so check pages with shading or overlapping pictures.

*(Internal ID: `c_notransparent` · Config key: `texpert/notransparent`)*

#### Show adjust points

- **Where:** Advanced tab › Other tab › PDF Options, Covers, Show/Hide
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Show adjust points in the margin of the text.

**Explanation:**

Shows marks in the margin where paragraph adjustments (stretch or shrink from the adjustment list) are applied. It helps you check your adjustments. Turn it off for the final PDF.

*(Internal ID: `c_showadjpoints` · Config key: `texpert/showadjpoints`)*

#### Mark Trigger Points

- **Where:** Advanced tab › Other tab › PDF Options, Covers, Show/Hide
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Display trigger points in output

**Explanation:**

Shows marks where triggers (instructions tied to a verse, such as a picture position or a style change) take effect. It helps you check them. Turn it off for the final PDF.

*(Internal ID: `c_mktrigpts` · Config key: `texpert/mktrigpts`)*

#### Show USFM codes

- **Where:** Advanced tab › Other tab › PDF Options, Covers, Show/Hide
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Show the USFM markers in the margin beside paragraphs.

**Explanation:**

Shows the USFM marker of each paragraph (such as p, q1, s1) in the margin. It helps you find which style to change on the **Styles** tab. Turn it off for the final PDF.

*(Internal ID: `c_showusfmcodes` · Config key: `texpert/showusfmcodes`)*

#### Show Error Bars For Overfull Lines

- **Where:** Advanced tab › Other tab › PDF Options, Covers, Show/Hide
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Enable this option to have TeX make overfull lines stand out.

**Explanation:**

Puts a black bar at the end of every line that is too long for the column (an overfull line). Use it while proofreading to find such lines. Fix them, for example with hyphenation or small changes to the text. Then turn this off.

*(Internal ID: `c_showhboxerrorbars` · Config key: `texpert/showhboxerrorbars`)*

#### Spine Overlap onto Back Cover (mm)

- **Where:** Advanced tab › Other tab › PDF Options, Covers, Show/Hide
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 50, default 0

**Tooltip (the text shown when you hover the mouse over it):**

> If you want the spine graphic or colour to spill over onto the back cover page, then set the amount of overlap here.

**Explanation:**

Lets the spine colour or picture extend this many mm onto the back cover. It helps hide small errors when the cover is folded. It is used when you make a cover on the **Peripherals** tab.

*(Internal ID: `s_spineoverlapback` · Config key: `texpert/spineoverlapback`)*

#### Spine Overlap onto Front Cover (mm)

- **Where:** Advanced tab › Other tab › PDF Options, Covers, Show/Hide
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 50, default 0

**Tooltip (the text shown when you hover the mouse over it):**

> If you want the spine graphic or colour to spill over onto the front cover page, then set the amount of overlap here.

**Explanation:**

Lets the spine colour or picture extend this many mm onto the front cover. It is used when you make a cover.

*(Internal ID: `s_spineoverlapfront` · Config key: `texpert/spineoverlapfront`)*

#### Cover Bleed (mm)

- **Where:** Advanced tab › Other tab › PDF Options, Covers, Show/Hide
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 25, default 5

**Tooltip (the text shown when you hover the mouse over it):**

> Bleed is the section of artwork that goes beyond where the paper is cut. This ensures that the image goes right to the edge of the cover after it has been trimmed.

**Explanation:**

The extra area (in mm) of cover artwork beyond the cut edge. After trimming, the picture or colour then goes right to the edge. Ask your printer how much bleed they need. Often it is 3 to 5 mm.

*(Internal ID: `s_bleed` · Config key: `texpert/bleed`)*

#### Hard Cover Art Bleed (mm)

- **Where:** Advanced tab › Other tab › PDF Options, Covers, Show/Hide
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 25, default 0

**Tooltip (the text shown when you hover the mouse over it):**

> Art Bleed is specifically for hard cover binding and is the setting which enables images to go beyond the size of the cover in order to wrap around the hard cover and stuck down under the inner backing sheet.

**Explanation:**

Extra bleed in mm for hard cover books. The cover picture must wrap around the board and be glued under the inside sheet, so it must be larger. Leave it at 0 for soft covers. Ask your printer for the right value.

*(Internal ID: `s_artbleed` · Config key: `texpert/artbleed`)*

### Advanced tab › Other tab › Preview Pane: Adjustment and Analysis Settings

#### Auto-update Delay (seconds)

- **Where:** Advanced tab › Other tab › Preview Pane: Adjustment and Analysis Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 120, default 3

**Tooltip (the text shown when you hover the mouse over it):**

> Right-clicking again on the PDF within this time (3 second default) will prevent the Auto-update from running.

**Explanation:**

When **Auto-update** is on in the PDF Preview window, a right-click adjustment starts a new print after this many seconds. If you right-click again within this time, PTXprint waits, so you can make several adjustments before it prints. Increase it if you need more time between adjustments.

*(Internal ID: `s_autoupdatedelay` · Config key: `texpert/autoupdatedelay`)*

#### Shrink Text Step Value (%)

- **Where:** Advanced tab › Other tab › Preview Pane: Adjustment and Analysis Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 1 to 5, default 1

**Tooltip (the text shown when you hover the mouse over it):**

> Step Value to shrink text using right-click context menu adjustment.

**Explanation:**

How many percent each "shrink text" step from the right-click menu in the PDF Preview window makes a paragraph smaller.

*(Internal ID: `s_shrinktextstep` · Config key: `texpert/shrinktextstep`)*

#### Minimum Text Shrink (%)

- **Where:** Advanced tab › Other tab › Preview Pane: Adjustment and Analysis Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 85 to 100, default 95

**Tooltip (the text shown when you hover the mouse over it):**

> Limit how much text can shrink to using right-click context menu adjustment.

**Explanation:**

The smallest size (in percent of normal) that a paragraph can be shrunk to with the right-click menu. 95 means at most 5% smaller. The page filler also uses this limit. Shrinking too much makes text look crowded.

*(Internal ID: `s_shrinktextlimit` · Config key: `texpert/shrinktextlimit`)*

#### Expand Text Step Value (%)

- **Where:** Advanced tab › Other tab › Preview Pane: Adjustment and Analysis Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 1 to 5, default 1

**Tooltip (the text shown when you hover the mouse over it):**

> Step Value to expand text using right-click context menu adjustment.

**Explanation:**

How many percent each "expand text" step from the right-click menu makes a paragraph larger.

*(Internal ID: `s_expandtextstep` · Config key: `texpert/expandtextstep`)*

#### Maximum Text Expand (%)

- **Where:** Advanced tab › Other tab › Preview Pane: Adjustment and Analysis Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 100 to 115, default 105

**Tooltip (the text shown when you hover the mouse over it):**

> Limit how much text can expand to using right-click context menu adjustment.

**Explanation:**

The largest size (in percent of normal) that a paragraph can be expanded to with the right-click menu. 105 means at most 5% larger.

*(Internal ID: `s_expandtextlimit` · Config key: `texpert/expandtextlimit`)*

#### Bad Space minimum width (em)

- **Where:** Advanced tab › Other tab › Preview Pane: Adjustment and Analysis Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 10, default 1.3

**Tooltip (the text shown when you hover the mouse over it):**

> Minimum width for a bad space. 0 says to calculate for the 20 worst spaces in the doc

**Explanation:**

**Layout Analysis** in the PDF Preview window marks word spaces wider than this, in em (the size of the font). With 0, PTXprint finds the 20 widest spaces in the document instead. A lower value marks more spaces.

*(Internal ID: `s_spaceEms` · Config key: `texpert/spaceEms`)*

#### Bad intercharacter space minimum width (em)

- **Where:** Advanced tab › Other tab › Preview Pane: Adjustment and Analysis Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 1, default 0.3

**Tooltip (the text shown when you hover the mouse over it):**

> Minimum width for a bad inter character space.

**Explanation:**

**Layout Analysis** marks spaces between letters wider than this, in em. It is only used when letter spacing is turned on (**Between Letters** on the **Fonts+Script** tab).

*(Internal ID: `s_charSpaceEms` · Config key: `texpert/charSpaceEms`)*

#### Precise collisions

- **Where:** Advanced tab › Other tab › Preview Pane: Adjustment and Analysis Settings
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Only show precise collisions between glyphs rather than overlapping bounding boxes - slow

**Explanation:**

When ticked, collision checking looks at the real shapes of the letters, not just the boxes around them. It finds fewer false collisions but is slow.

*(Internal ID: `c_collisionPrecise` · Config key: `texpert/collisionPrecise`)*

#### Collision Detection Padding (pt)

- **Where:** Advanced tab › Other tab › Preview Pane: Adjustment and Analysis Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -1 to 5, default 0.5

**Tooltip (the text shown when you hover the mouse over it):**

> Minimum space between bounding boxes of glyphs before a collision is flagged.

**Explanation:**

How close (in points) the boxes around letters on different lines can come before **Layout Analysis** reports a collision. A larger value reports more possible collisions.

*(Internal ID: `s_paddingwidth` · Config key: `texpert/paddingwidth`)*

#### River Detection Threshold (em)

- **Where:** Advanced tab › Other tab › Preview Pane: Adjustment and Analysis Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 1 to 1000, default 3

**Tooltip (the text shown when you hover the mouse over it):**

> The sum of all the widths in the river must be above this for the river to be detected

**Explanation:**

A river is a line of white space running down through several lines of text. A river is reported only when the widths of all its spaces add up to more than this, in em. Increase it to report only the worst rivers.

*(Internal ID: `s_riverthreshold` · Config key: `texpert/riverthreshold`)*

#### River Detection minimum required maximum width (em)

- **Where:** Advanced tab › Other tab › Preview Pane: Adjustment and Analysis Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0.1 to 5, default 1

**Tooltip (the text shown when you hover the mouse over it):**

> Minimum width required for the widest part of the river

**Explanation:**

A river is reported only if its widest space is at least this wide (in em).

*(Internal ID: `s_riverminmaxwidth` · Config key: `texpert/riverminmaxwidth`)*

#### River Detection minimum width (em)

- **Where:** Advanced tab › Other tab › Preview Pane: Adjustment and Analysis Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0.1 to 5, default 0.5

**Tooltip (the text shown when you hover the mouse over it):**

> Minimum width of any space in a river for it to be included

**Explanation:**

A space must be at least this wide (in em) to be counted as part of a river.

*(Internal ID: `s_riverminwidth` · Config key: `texpert/riverminwidth`)*

#### River Detection maximum line leading (em)

- **Where:** Advanced tab › Other tab › Preview Pane: Adjustment and Analysis Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 5, default 0.4

**Tooltip (the text shown when you hover the mouse over it):**

> Any lines separated by a gap greater than this will be considered not to be in the same river

**Explanation:**

Spaces on lines that are further apart than this (in em) are not counted as one river.

*(Internal ID: `s_rivergap` · Config key: `texpert/rivergap`)*

#### River Detection minimum overlap (em)

- **Where:** Advanced tab › Other tab › Preview Pane: Adjustment and Analysis Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -5 to 5, default 0.4

**Tooltip (the text shown when you hover the mouse over it):**

> Minimum overlap in ems required for two spaces above each other to be considered part of the same river

**Explanation:**

Two spaces on lines above each other must overlap by at least this much (in em) to belong to the same river.

*(Internal ID: `s_riveroverlap` · Config key: `texpert/riveroverlap`)*

### Advanced tab › Other tab › Automatic Page Filler

#### Time limit for the whole job (minutes)

- **Where:** Advanced tab › Other tab › Automatic Page Filler
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 1000, default 180

**Tooltip (the text shown when you hover the mouse over it):**

> The page filler works on all the books together. When this time is reached, the page filler stops. A book that is not finished keeps the pages that are already filled. Usually this affects only the longest book.  
> Higher: more time to find a good layout for every page.

**Explanation:**

The longest time in minutes that the page filler works on the whole job. When the time is up, it stops. Pages it has already filled are kept. 0 means no time limit. Increase it for a long Bible if the longest book does not finish.

*(Internal ID: `s_pbtimeout` · Config key: `texpert/pbtimeout`)*

#### Earlier pages to retry

- **Where:** Advanced tab › Other tab › Automatic Page Filler
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 10, default 4

**Tooltip (the text shown when you hover the mouse over it):**

> If the page filler cannot fill a page, it backtracks to the page before and tries a different layout there. This is the largest number of pages it can backtrack.  
> Higher: fewer failed pages, but much slower.  
> Lower: faster, but more pages may fail. 0 = never backtrack (fastest).  
> Affects: Speed.

**Explanation:**

When the page filler cannot fill a page, it can go back to earlier pages and try a different layout there. This is how many pages it may go back. Higher values fail on fewer pages but are much slower.

*(Internal ID: `s_pbbacktrack` · Config key: `texpert/pbbacktrack`)*

#### Paragraphs to adjust on each page

- **Where:** Advanced tab › Other tab › Automatic Page Filler
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 1 to 10, default 6

**Tooltip (the text shown when you hover the mouse over it):**

> The largest number of paragraphs on one page that the page filler may stretch or shrink. Each poetry line (\q1, \q2 …) counts as one paragraph. Each extra paragraph doubles the number of layouts the page filler tries.  
> Higher: more ways to fill each page, so fewer failed pages, but each page takes longer.  
> Lower: faster, but more pages may fail.  
> Affects: Speed.

**Explanation:**

How many paragraphs on one page the page filler may stretch or shrink. Each poetry line counts as a paragraph. Each extra paragraph doubles the work, so keep this low unless many pages fail.

*(Internal ID: `s_pbmaxr` · Config key: `texpert/pbmaxr`)*

#### Widest word space allowed (× text size)

- **Where:** Advanced tab › Other tab › Automatic Page Filler
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 10, default 1

**Tooltip (the text shown when you hover the mouse over it):**

> When the page filler stretches a paragraph, the average space between words must not be wider than this. 1.0 = as wide as the text size. A normal word space is about 0.3 to 0.5.  
> Higher: easier to fill pages, but the text can look too spread out.  
> Lower: tighter, better-looking text, but pages are harder to fill and take longer.  
> Affects: Quality and Speed.

**Explanation:**

The widest average word space the page filler allows when it stretches a paragraph, as a part of the text size. A normal word space is about 0.3 to 0.5. Lower values look better, but more pages may fail and filling takes longer.

*(Internal ID: `s_pbspacingtol` · Config key: `texpert/pbspacingtol`)*

#### Keep paragraphs close to normal width

- **Where:** Advanced tab › Other tab › Automatic Page Filler
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 10, default 1

**Tooltip (the text shown when you hover the mouse over it):**

> The page filler prefers small changes to a paragraph over big changes. This setting controls how strong that preference is. Higher: the page filler tries small changes first, so the text looks more even.  
> Lower: the page filler accepts big changes more easily.  
> Affects: Quality.

**Explanation:**

How strongly the page filler prefers small changes to paragraphs over large ones. Higher values give more even text.

*(Internal ID: `s_pbexpbad` · Config key: `texpert/pbexpbad`)*

#### Penalise shrink or stretch

- **Where:** Advanced tab › Other tab › Automatic Page Filler
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -5 to 5, default 1

**Tooltip (the text shown when you hover the mouse over it):**

> Tells the page filler whether to shrink paragraphs or stretch them when both are possible.  
> Positive numbers: penalise stretching (so the text prefers to shrink more).  
> Negative numbers: penalise shrinking. (so the text prefers to stretch more).  
> 0: no preference.  
> A bigger number (+ or −) means a higher penalty.  
> Affects: Quality.

**Explanation:**

Whether the page filler prefers to shrink or to stretch paragraphs when both would work. Positive values prefer shrinking. Negative values prefer stretching. 0 has no preference.

*(Internal ID: `s_pbexpcost` · Config key: `texpert/pbexpcost`)*

#### Keep neighbouring paragraphs alike

- **Where:** Advanced tab › Other tab › Automatic Page Filler
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 0 to 20, default 3

**Tooltip (the text shown when you hover the mouse over it):**

> The page filler compares each paragraph with the paragraph before it. It tries to avoid a very stretched paragraph next to a very shrunk one.  
> Higher: neighbouring paragraphs look more alike, so the page looks more even.  
> Lower: neighbouring paragraphs can look more different.  
> Affects: Quality.

**Explanation:**

How strongly the page filler avoids a very stretched paragraph next to a very shrunk one. Higher values give a more even page.

*(Internal ID: `s_pbcontrast` · Config key: `texpert/pbcontrast`)*

### Advanced tab › Other tab › Other Miscellaneous Settings

#### Use \toc3 for Tab Text

- **Where:** Advanced tab › Other tab › Other Miscellaneous Settings
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Use \toc3 for tab text if no \zthumbtab

**Explanation:**

When ticked (the default), the thumb tab text of a book comes from its `\toc3` (short book name), if the book has no `\zthumbtab` marker. Thumb tabs are set on the **Tabs+Borders** tab.

*(Internal ID: `c_tocthreetab` · Config key: `texpert/tocthreetab`)*

#### Tilde is No Break Space

- **Where:** Advanced tab › Other tab › Other Miscellaneous Settings
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Treat ~ as non breaking space

**Explanation:**

When ticked (the default), a tilde (~) in the text prints as a non-breaking space. A non-breaking space looks like a normal space, but the line never breaks there. Untick it only if your text needs to print a real tilde character.

*(Internal ID: `c_tildenbsp` · Config key: `texpert/tildenbsp`)*

#### Remove \ref ... \ref* links

- **Where:** Advanced tab › Other tab › Other Miscellaneous Settings
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> USFM 3.2 allows additional reference links to be inserted as part of \xt ... \xt* markup. This frequently appear in DBL text bundles, but are unhandled by PTXprint. Allow these to be removed from the USFM prior to typesetting.

**Explanation:**

Text from the Digital Bible Library (DBL) often has extra `\ref` links inside cross-references. PTXprint cannot use them. When ticked (the default), they are removed before typesetting, and only their visible text is kept.

*(Internal ID: `c_removextreflinks` · Config key: `texpert/removextreflinks`)*

#### End decoration skip

- **Where:** Advanced tab › Other tab › Other Miscellaneous Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -100 to 100, default 16

**Tooltip (the text shown when you hover the mouse over it):**

> The gap between the end of the book and the book-end decoration

**Explanation:**

The space (in points) between the end of the book text and the end-of-book decoration. The decoration is turned on in **Ornamental Decorations** on the **Tabs+Borders** tab. Use negative values to move the decoration up.

*(Internal ID: `s_bedskip` · Config key: `texpert/bedskip`)*

#### Thumbtab rotated adjustment

- **Where:** Advanced tab › Other tab › Other Miscellaneous Settings
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from -10 to 50, default -2

**Tooltip (the text shown when you hover the mouse over it):**

> Shift thumbtab text

**Explanation:**

Moves the text on rotated thumb tabs (in points) so that it sits in the middle of the tab. Change it if the tab text looks off-centre. Thumb tabs and **Rotate Tabs** are on the **Tabs+Borders** tab.

*(Internal ID: `s_thumbvvadj` · Config key: `texpert/thumbvvadj`)*
