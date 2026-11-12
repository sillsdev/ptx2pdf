# Tooltip and UI issues found while writing the manual

Generated 2026-11-12. One section per chapter; IDs refer to ptxprint.glade.


## 02-main-window-tooltip-issues

## Tooltip issues – 02-main-window (Main window, menu and view levels)

| ID | Problem | Suggested wording |
|----|---------|-------------------|
| `lb_Printers` | Tooltip "Adjust expert-level settings." is wrong. The Printers tab is about the print job specification (trim size, pages, thickness) and printing services, not expert settings. | "Describe the printed book (trim size, page count, paper) and get information or quotes from printing services." |
| `c_quickRun` | Spelling "dynamicly" -> "dynamically". Also the first-time default comes from the user preference (`init/quickrun`, fallback False), so the glade "active=True" is never seen. | "...the Table of Contents and other dynamically updated details..." |
| `c_noupdate` | "This is a temporary setting and resets when PTXprint restarts." It is not saved, and on restart it is ticked again (glade default active=True), so "resets" is ambiguous. The tooltip also does not say that PTXprint still processes the USFM when the source text changed or a processing setting was changed (the box then shows a dash). | "Not saved with the configuration. PTXprint still re-processes the USFM when the text has changed in Paratext, or when you change a setting that affects the text (the box then shows a dash until the next successful print)." |
| `lb_TabsBorders` | Spelling "embelishments" -> "embellishments". | |
| `lb_NotesRefs` | Missing comma: "Cross-references Study Notes" -> "Cross-references, Study Notes". | |
| `lb_Publications` | Uses the technical term "\zvars". | "...each with its own books, titles and other variables..." |
| `btn_menu_level`, `btn_menu_lang`, `btn_menu_showPDF` | No tooltips. | View Level: "Choose how many settings PTXprint shows. Hidden settings keep their values and still take effect." Language: "Change the language of the PTXprint interface (the window is reopened; save first)." Show PDF: "Choose how the PDF is shown after printing." |
| `btn_dismissStatusLine` | No tooltip; the button also becomes "Copy to Clipboard" for Unicode messages. | "Hide this message." |
| `t_find` (code) | `onFindKey` (Esc clears the search) exists in gtkview.py but is not connected to any signal in the glade file, so Esc does nothing. | Code fix: connect key-press-event to onFindKey. |


## 03-basic-tooltip-issues

## Tooltip issues – 03-basic (Basic tab and its dialogs)

| ID | Problem | Suggested wording |
|----|---------|-------------------|
| `btn_deleteConfig` | **Code/tooltip conflict (serious).** Tooltip says the PDFs "will remain in that folder", but `onDeleteConfig` calls `rmtree(self.project.printPath(None))`, which is the whole `local/ptxprint` folder of the project: all PDFs and working folders of **all** configurations. Probably meant `printPath(cfg)`. | Fix the code; keep the tooltip. |
| `btn_resetDefaults` | Tooltip says it does not reset "Stylesheets, or other advanced file-based settings", but the code (`onDeleteConfig` for Default) removes the whole Default config folder (`rmtree(srcPath('Default'))`), which includes ptxprint.sty, picture lists, adjust lists, FRTlocal.sfm, changes.txt etc. It also runs with no confirmation. | "Reset the Default configuration to PTXprint's default settings. Warning: this also removes the files stored in the Default configuration folder (styles, picture list, adjust lists, front matter). There is no confirmation." |
| `btn_pw_cancel` / `btn_pw_ok` | IDs are swapped: the button labelled **OK** is `btn_pw_cancel` and **Cancel** is `btn_pw_ok` (the responses are correct). Also, in `onLockUnlockSavedConfig` a CANCEL response sets `pw = ""` and then continues, so an unlocked config gets **locked with an empty password**. Closing the dialog with the window X returns without hiding the dialog. | Code fix: on CANCEL, hide the dialog and return. |
| `ecb_savedConfig` | The last sentence repeats the first: "Alternatively, select a previously-saved layout configuration to retrieve settings." It does not warn that changing configuration does not save the current one. | "Select a saved configuration to load its settings. Note: unsaved changes to the current configuration are not saved automatically. When the Paratext project is shared through Send/Receive, all saved configurations are also available to other users." |
| `ecb_booklist` | Refers to "the Choose... button"; the button is now **Select Multiple Books...**. | "...use the Select Multiple Books... button..." |
| `ecb_licenseText`, `textv_copyright` | Run-on sentence: "use ~ for places where a non-breaking space is needed use // where a line break needs to be forced but :// used in URLs will still be preserved". | "Use ~ where a non-breaking space is needed. Use // to force a line break (:// in URLs is not changed)." |
| `lb_openBible` | The last paragraph ("If you don't already have a Scripture Text Bundle...") belongs to the Step 1 label, not to this link. | Remove the last paragraph. |
| `t_DBLprojName` | Says "Use 8 characters or less", but the code does not check the length (only spaces/special characters and existing names). | Enforce the limit, or say "Use a short name (8 characters or fewer is best)". |
| `r_book_single`, `r_book_multiple`, `r_book_module`, `t_chapfrom`, `t_chapto` | No tooltips. | Single Book: "Print one book, or a range of its chapters." Multiple: "Print several books, or the passages listed in the box." Module: "Print a Paratext Bible module (.sfm list of passages)." Chapters: "First/last chapter to print." |
| `btn_copyToTargetProj` | Does not say that the saved files are copied (so save first), or that adjust lists are not copied to other projects. | "...Save first: the saved files are copied. Adjust lists are not copied." |
| `r_copyConfig_overwrite` | "then the source target setting will 'win'" - "source target" is confusing. | "...then the source project's setting wins." |


## 04-layout-tooltip-issues

## Tooltip issues – 04-layout

| ID | Problem | Suggested wording |
|---|---|---|
| `col_gridMajor` | Tooltip is copied from Thumb Tabs ("Thumb Tabs usually use a dark color…"). Not relevant. | "Colour of the major (thicker) grid lines." |
| `col_gridMinor` | Same Thumb Tabs tooltip copied in. | "Colour of the minor (thinner) grid lines between the major lines." |
| `btn_resetGrid` | Says "red and light green lines". Code (`onRefreshGridDefaults`) sets minor colour rgb(98,160,234) = light blue. Also has a double space. | "Reset the grid to the defaults: centimetres with 5 divisions (2 mm each), red major and light blue minor lines (0.2 pt thick), over the whole page." |
| `s_gridMinorDivisions` | Fine, but the widget label is "Minor Divisions" for three different controls (colour, thickness, count) – the extractor cannot tell them apart. | Consider separate accessible names/labels. |
| `s_indentUnit` | First tooltip says "(default=1, min=0, max=4)" but the default is 0.8. Two near-duplicate tooltips (label and spin). | "The basic paragraph and poetry indent, in inches. PTXprint halves it when you switch to two columns and doubles it when you switch back." |
| `c_doublecolumn` | Tooltip only explains why it may be greyed out (diglot); it never says what the setting does. | "Set the main text in two columns (ticked) or one column (unticked). This box is greyed out when a Diglot is active, because diglots need two columns. Some books can be set differently using 'Use One/Two Column Layout…' on the Body tab (Full view)." |
| `s_headerposition` | Two tooltips merged; the sentence "The top of the main text area is 1 base line spacing above…" appears twice. "the the" typo. | "The space (pt) between the bottom of the header and the top of the main text area. The header sits inside the top margin, so a larger value moves the header towards the page edge." |
| `s_rhruleposition`, `s_topmargin` | "the the main text area" (double "the"). | Remove the duplicate "the". |
| `s_ruleThickness` | Tooltip says it also controls the header rule and study-notes rule, but the control is greyed out in one-column layouts. Either the sensitivity or the tooltip is misleading. | Consider making it available whenever Horizontal Rule is ticked, or note "(only available with two columns)". |
| `c_noteLines` | "Wide- Margin" (stray space). Hint says settings are in "Advanced > Other tab"; correct, but could name the section exactly ("Page Layout and Spacing"). | "…'Wide-Margin Bibles'." |
| `btn_adjust_spacing` | Does not warn that with Lock Ratio ticked the font size also changes. | Add: "Note: if Lock Ratio is ticked, the font size will also change slightly." |
| `c_allowUnbalanced` | "abovementioned" → "above-mentioned"; refers to "Advanced page… Other tab" – fine. | Minor spelling fix. |
| `c_noinkinmargin` | Double space in "need  the page number". | Remove extra space. |
| `c_marginNotesInner` | Says "can be changed for single column layouts" – correct; could add that it is disabled for two columns. | "…(Not available for two-column layouts.)" |
| `c_noGrid` | The extracted tooltip merges the switch tooltip with the `l_gridAligned` label tooltip, so the same advice appears twice. | Keep one version on the switch. |


## 05-fonts-tooltip-issues

## Tooltip issues – 05-fonts

| ID | Problem | Suggested wording |
|---|---|---|
| `s_tatweelLength` | Spin-button tooltip has the typo "Hw many Tatweels". | "How many Tatweels should be inserted at the current cursor location?" |
| `s_minSpace` | The extracted tooltip ends with "Maximum size % that a space can grow to when necessary." – that sentence belongs to Max/Stretch, not Min/Shrink. | Replace the last sentence with "Minimum size % that a space can shrink to when necessary." |
| `fcb_script` | List of scripts with extra functionality is out of date: "arab, mymr, thai, knda, orya, mlym, taml, telu". Code (`scriptsnippets.py`) also has sinh, laoo, lana, talu, beng, hans, hant. Also says leave it as "Default", but PTXprint auto-detects the script on project load and the setting matters for shaping. | "Choose the script of the text. PTXprint uses it for font shaping and adds special processing for some scripts (Arabic, Myanmar, Thai, Lao, Tai Tham, New Tai Lue, Bengali, Malayalam, Tamil, Sinhala, Telugu, Kannada, Oriya, Han). If set to Default, PTXprint tries to detect the script when the project is opened." |
| `btn_scrsettings` | Says "(such as Burmese & Indic)"; Arabic and Han (Simplified/Traditional) also have settings. | "Some scripts (Myanmar, Indic scripts, Arabic, Han) have extra options which can be set here." |
| `fcb_fontdigits` | Fine, but the glade list store only has 4 entries; the real list is filled at run time (`_alldigits`). Not a tooltip issue as such, but the generated manual shows only 4 choices. | – |
| `c_hyphenate` | "using the button on the left" – the button is labelled "Import List..." while the tooltip of that button says "generate"; users look for a "Create" button. | "…first create a Hyphenation List using the 'Import List...' button…" |
| `btn_generateHyphenationList` | Button label "Import List..." vs dialog title "Create Hyphenation List" vs tooltip "generate". Inconsistent wording. | Use one verb, e.g. label "Create List...". |
| `c_nonBreakingHyphens` | "By default, word- medial may break…" – stray space and missing noun ("word-medial hyphens"). Also, the code (`texmodel.py` ~line 1388) only converts hyphens that are next to a space, plus uses U+2011 when generating the hyphen list – "word-medial" may not describe it accurately. | "Use non-breaking hyphens so that lines never break at a hyphen that is already in the text. Re-create the hyphenation list after changing this." |
| `c_letterSpacing` | Fine; could also mention that it is ignored when "Contextual Spaces" is set for the font. | Add: "Not used if the font uses Contextual Spaces." |
| `c_addSyllableBasedHyphens` | "hyphen- ation" (stray hyphen/space). | "…automated hyphenation is possible." |
| `c_hyphenLimitBooks` | Label is "Limit Hyphenation List to Words Found in" – the sentence is completed by a separate label with the book list; fine, but tooltip number "63929 words" is very specific; check it matches `Hyphenation.listlimit`. | – |
| `s_hyphMinBlock` | "Minimum word length for a word to block hyphenation." In `hyphen.py` the collected `nohyphendata` list is never used, so this setting currently has no effect. | Either implement it or hide/remove the control. |
| `s_hyphMinprefix` | Tooltip says start *or end* of the word, but `hyphen.py` checks `l.rindex("-") >= minaffix`, i.e. the last break point measured from the *start*. The end-of-word check seems missing (code issue). Also "the the word" typo. | Fix code to check `len(l) - l.rindex("-") - 1 >= minaffix`; fix "the the". |
| `bl_fontExtraR` | Two near-duplicate sentences ("Click to select a font…" / "Select a font…"). | Keep one. |
| `t_fontFeatures` | Example "litr=1, dig0=1…" is font-specific and unexplained. | "Font features for this font, e.g. smcp=1, cv12=2. Use 'Select Features...' to choose them from a list." |
| `fcb_fontFaces` | Second sentence ("not been installed 'For all Users'") belongs more to the font list than the typeface list. | Move to `tv_fontFamily` (which has no tooltip). |
| `tv_fontFamily`, `t_fontSearch`, `btn_fontFeatures`, `fcb_featsLangs` | No tooltip. | Add short tooltips, e.g. Language: "Choose the language the font should use; some fonts change letter shapes per language." |
| `c_fontGraphite` | Does not say that toggling it clears the font features. | Add: "Changing this clears the font features." |
| `t_linebreaklocale` | Tooltip is a bare list of codes; does not say when to use it. | "Language code for dictionary-based line breaking (for scripts without spaces between words): ja, km, ko, my, th, zh, or gr for a Graphite font's own rules." |


## 06-body-tooltip-issues

## Tooltip issues – 06-body (Body tab)

| ID | Problem | Suggested wording |
|----|---------|-------------------|
| `t_clHeading` | Tooltip says to type `\ZWNBSP` (double backslash). The macro is `\ZWNBSP` (the label `l_clHeading` tooltip has it right). "Non-Break" vs "Non Break" also differs between the two copies. | "...then just type the code \ZWNBSP here. This inserts an invisible Zero Width No-Break Space." |
| `c_filterGlossary` | Says "This option is only available if the GLO book is also selected", but the code never greys it out. It just has no effect without GLO. Also, entries referenced from kept entries are kept too. | "This only has an effect when the Glossary (GLO) is one of the books being printed. ... Entries marked up inside a kept entry are also kept." |
| `c_headingInMargin` | The setting (`document/headinginmargin`) is not used anywhere in texmodel.py, template.tex or the TeX macros, so it has no effect yet. Tooltip also doesn't say it needs Headings ticked. | Either implement it, or add "(not yet implemented)". |
| `c_chapterNumber` | Refers to an option "Hide Chapter Number in Single Chapter Books"; the on-screen control is "Show Chapter Numbers In: Single Chapter Books" (ticked = show). | "...Note that the 'Single Chapter Books' option in the Other Features area controls only one-chapter books." |
| `c_omitverseone` | Does not say that verse 1 is only hidden after a dropped chapter number (or with marginal verses). | "Hide verse number 1 when it follows a dropped (drop-cap) chapter number, or when marginal verses are used." |
| `c_glueredupwords` | Only words of 3+ letters are joined; not mentioned. | add "(words of 3 or more letters)". |
| `c_preventorphans` | Spelling "occuring" -> "occurring". Max length is set on Advanced tab (Maximum orphan word length) – worth mentioning. | |
| `c_parallelRefs` | Spelling "Pasage" -> "Passage". | |
| `c_useChapterLabel` | Spelling "overrirde" -> "override". | |
| `c_optimizePoetryLayout` | Double space "get  columns". Does not say it only applies to the books in the "Use Special Features" list (and does nothing if that list is empty). | add "Applies only to the books listed above (not when the list is empty)." |
| `c_pageNumTitlePage` (08) | – see 08 file. | |
| `s_columnShift` | Says "to the left of the column" but the column can be Right/Inner/Outer (fcb_marginVrsPosn). | "...space beside the text for the marginal verse numbers (pt)." |
| `fcb_glossaryMarkupStyle` | Choice labels "double ‡before word" / "double after‡ word" – "double" should be "double dagger". | |


## 07-notes-tooltip-issues

## Tooltip issues – 07-notes (Notes+Refs tab, Generate Strong's Index dialog)

| ID | Problem | Suggested wording |
|----|---------|-------------------|
| `fcb_fnHorizPosn`, `fcb_xrHorizPosn`, `fcb_snHorizPosn` | The tooltip is about vertical space ("The vertical space between the body text and the area containing…"). It was copied from the space settings and does not describe horizontal position. | "Where a shorter rule sits: Left, Right, Center, Inner (spine side) or Outer. Inner/Outer swap on odd and even pages. Only matters when Length is less than 100%." |
| `s_fnAboveSpace`, `s_xrAboveSpace`, `s_snAboveSpace` | The tooltip has two texts joined together that say almost the same thing. `s_xrAboveSpace` and `s_snAboveSpace` talk about the "Footnote Rule". | Keep one text and name the right rule (cross-reference rule / study note rule). |
| `s_fnIndent`, `s_xrIndent`, `s_snIndent` | "This is the amount to indent the rule." gives no unit. The code uses mm (`\hskip … mm`). The label says "Indent (mm)", but the tooltip should say it too. | "Distance (mm) to move the rule in from the side chosen in Horizontal Position." |
| `c_fnautocallers`, `c_xrautocallers` | Says 'try using the "Override..." setting above', but the Override checkbox is not above these controls in the layout. | 'If you do not see the callers you expect in the PDF, tick "Override hidden/automatic … caller settings".' |
| `c_fnOverride` | The footnote override tooltip says "\x +(plus) … \x - (minus)". It should say `\f`. | "Footnotes in Paratext use \f + to cycle through the callers, or \f - to omit the caller. …" |
| `t_fncallers`, `t_xrcallers` | "Use to button on the right" – should be "Use the button". | "(Use the button on the right to reload them if needed.)" |
| `r_fnpos_column`, `r_xrpos_column` | "End of the 2nd column" – a correct description, but the tooltip does not say that the notes are set at the width of one column, and that changing one placement also changes the other. | Add: "Footnotes and cross-references are kept together: choosing End of Column for one also moves the other." |
| `s_internote` | The tooltip describes the gap between the footnote block and the cross-reference block (the **Below Footnotes** case). In `_sensitivities` the control is only enabled for **Column Cross-References** (`r_xrpos_centre`), so it is greyed out for **Below Footnotes**, where it would be most useful. This may be a logic bug, not a tooltip problem. The description also says "Footnoes". | Check the sensitivity rule. Fix "Footnoes" → "Footnotes" in the widget name/description. |
| `c_xrefrule` and the cross-reference rule settings | `notes/ifxrefrule` is not used in `template.tex`. `calcRuleParameters` uses the xref rule settings only when footnotes are endnotes (or for the endnote rule). So for most layouts, these settings and the checkbox do nothing. The tooltips do not say this. | Either wire the settings up, or add: "Used only when footnotes are placed at the End of Book. Otherwise the Footnote rule settings apply." |
| `c_studynoterule` | The tooltip says "separating the body text from the footnote area". It should be the study note area. | "This is the horizontal rule above the study notes (extended footnotes) area." |
| `s_snBelowSpace` | "…between the rule and the footnotes." Should be study notes. | "…between the rule and the study notes." |
| `s_ef_colgutterfactor`, `s_ef_bottomRag`, `s_ef_colgutteroffset` | Each tooltip has the same text twice in different words. | Keep one version. |
| `s_ef_bottomRag` | The control is always insensitive in glade and has no config key, so it does nothing. The long tooltip suggests it works. | Remove the control or wire it up. |
| `s_ef_internote` | `studynotes/internote` is written to the config but is not used in `template.tex`. We could not confirm that it has any effect. | Check and wire it up, or remove it. |
| `c_ef_showCallers` | Long sentence. Also, the code removes callers from the text as well as from the notes area when unticked. | "Show callers for extended notes in the text and in the notes area. Usually off for study Bibles, which have many notes. Only a–z callers are possible." |
| `r_xrSource_standard` … `r_xrSource_custom` | These radio buttons are in a hidden box (`no-show-all`). Users never see them. They only hold descriptions for `btn_infoXrefSource`. The `r_xrSource_ubs` and `r_xrSource_works` descriptions are both "Source of cross-references: The Works". | Fix the `r_xrSource_ubs` name to "UBS GNT92 list". Perhaps move the texts to a dictionary in code. |
| `r_xrSource_custom` | "it is possible … For example. it is possible" – broken punctuation. It also tells users to "Search Google", which a manual should not need. | "…for example, cross-references extracted from another project in .xrf format. .xre (extended .xrf) and .xml formats are also supported." |
| `btn_infoXrefSource` | The default tooltip "External Cross-Reference List Source Description" is only a label, until a list is chosen. | "Hover here to read about the selected cross-reference list." |
| `fcb_xRefExtListSource` | Does not explain the five Standard list sizes. | Add: "The five Standard list sizes take fewer or more references from the same list (fewest = only the most important)." |
| `fcb_filterXrefs` | Says 'the list of Multiple Books on the Basic tab'. The on-screen option is "Portions or Multiple Books" in **What to Print**. Minor. | '…only cross-references to books in the "Portions or Multiple Books" list on the Basic tab will be included.' |
| `c_strongsShowAll` | The label is spelled "Show All Occurences". The description is the same as for `c_strongsShowNums` ("Show Strong's numbers in cross-references"), which is wrong. | Label: "Show All Occurrences". Description: "Tag every occurrence of a word with its Strong's number". |
| `c_strongsShowInText` | Recommends the option "Show Localized Terms Only", which does not exist in the UI. | Remove that sentence, or name the real option. |
| `fcb_strongsNdxBookId` | The tooltip is repeated twice (once with "bookx", once with "books"). | Keep one copy, spelled "books". |
| `fcb_strongsMajorLg` | The choice "Portugese" is misspelled. | "Portuguese". |
| `c_strongsNotes` | Not saved in the config (no modelmap entry), so it resets each session. | Add a `strongsndx/notes` config key. |
| `s_strongRag` | `strongsndx/raglines` is saved, but `generateStrongsIndex` does not use it. We could not confirm that it has any effect. | Wire it up (e.g. a \bottomrag line in the generated book), or remove it. |
| `lb_style_li+strong-s` | The second line ("Select which components should be included…") seems to belong to the frame, not to the `\li` link. | Remove the second line from the link tooltip. |
| `c_filterCats`, `tv_sbCatEdit` | The category list is not saved (the `sbcats` var code is commented out), and nothing in texmodel/template uses it. The tooltip promises filtering that does not happen. | Wire it up, or hide the feature until it works. |
| `c_txlQuestionsRefs` | "the reference will in parenthesis" – a word is missing. | "…the reference will be shown in parentheses (ch:vs)." |
| `c_glossaryFootnotes` | "Glossary \w markup|mark\w* looks like this" is hard to read. Also, only the first paragraph of each glossary entry is used. | "Glossary words are marked like \w word\w* in the text. Only the first paragraph of each glossary entry is used." |
| `c_keepBookWithRefs` | Fine, but the code also stops single letters from being stranded in note text. | Optional: add "It also prevents single letters being left at the end of a line in notes." |


## 08-headfoot-tooltip-issues

## Tooltip / UI issues – 08-headfoot (Header+Footer tab)

| ID | Problem | Suggested wording / fix |
|----|---------|-------------------------|
| `ecb_ftrcenter` | **Bug (glade, not just tooltip):** the item "Time (HH:MM)" has `id="<Enter ID>"`. `_getcomboval` returns the active id, so choosing it puts the literal text `<Enter ID>` in the footer instead of `\hrsmins`. | Remove the id (or set `id="\hrsmins"`). |
| `ecb_ftrcenter` | Tooltip tells users to edit ptxprint-mods.tex for inner/outer footers (manual rule: no file editing). Tooltip text also appears twice (label + widget versions differ). "YYYY-MM-YY" typo. | Drop the mods.tex sentence; fix "YYYY-MM-DD". |
| `ecb_hdrleft` | Item labels "Date (YYY-MM-DD)" and "Printed on YYY-MM-DD" (three Y's). Works (ids are used) but looks wrong and differs from the footer list. | "Date (YYYY-MM-DD)", "Printed on YYYY-MM-DD". |
| `ecb_hdrright`, `ecb_hdrleft` | Example says "DRAFT YYYY-MM-YY HH:MM" (should be YYYY-MM-DD; ecb_hdrcenter has it right). | |
| `ecb_hdr*` | Tooltips don't mention that with Mirror Pages on, First/Last Reference swap on even pages, which surprises users. | add "With Mirror Pages on, First and Last Reference are swapped on left-hand pages." |
| `r_hdrRight_Sec` | Description (accessible name) says "Use formatting from primary project (outer header)" – should be "secondary". | |
| `r_hdr*`, `r_ftrCenter_*` | "Primary (Left) text's formatting should be used ... or the Secondary format" – the choice also decides which text the reference/book name comes from, not just formatting. | "...whether this item (reference, book name and font) comes from the Primary or the Secondary text." |
| `c_pageNumTitlePage` | "Intoductory" -> "Introductory". Also it actually applies to the first page of each book (the title page), not to all intro pages. Says "By default there is no page number" but the checkbox is ticked by default. | "Print the page number at the bottom of the first page of each book (where there is no header)." |
| `c_printConfigName` | Doesn't say it is mutually exclusive with c_pageNumTitlePage (ticking one unticks the other). | add that note. |
| `c_rangeShowChapter` | Fine; could mention that Verse needs it. | |
| `s_startPageNum` | Only applies when the page number is still in front-matter (<1) numbering when the first Scripture book starts (`\ifnum\pageno<1`). | add "If the front matter uses normal page numbers, numbering continues instead." |


## 09-pictures-tooltip-issues

## Tooltip issues – 09-pictures

| ID | Problem | Suggested wording |
|---|---|---|
| `r_pictureRes_High` | Says it searches "first for PDFs, then PNGs, and finally JPGs". The code (piclist.build_searchlist) uses TIF > PNG > JPG > BMP > PDF for high resolution, and prefers the larger file when two have the same type. | "PTXprint prefers TIF, then PNG, then JPG files (and the larger file if there are two of the same type). High-quality originals are usually kept in the project's local\Figures folder so that they are not shared by Send/Receive. The PDF can be very large, but the picture quality is as good as possible." |
| `t_imageTypeOrder` | Whole tooltip text is duplicated (two versions of the same explanation in one tooltip). | Keep only the first version (the numbered list of default orders and examples). |
| `fcb_plSize` | Text is duplicated ("The frame size determines..." and "Span Width only allows..." appear twice). | Remove the second copy of the first and second paragraphs. |
| `t_picXetex` | Text duplicated; "Mulitple" misspelt (twice); "multipage"/"multi-page" inconsistent. | Keep one copy; "Multiple parameters should be separated by spaces: rotate=binding page=2". |
| `t_plCreditText` | Text duplicated; one copy says "David C Cook", the other "David C. Cook". | Keep one copy. |
| `t_plCaption`, `t_mapCaption` | Tells users to add `\CaptionFirsttrue` to ptxprint-mods.tex. There is now a UI option for this (Advanced tab › Other › Pictures, Figures, Images, Sidebars › "Show Caption Before Image"). | "By default the caption appears below the picture. To show it above the picture, tick 'Show Caption Before Image' on the Advanced tab (Other sub-tab). Note that captions are NOT processed by changes in PrintDraftChanges.txt." |
| `t_plRef` | Tells users to add `\CaptionRefFirsttrue` to ptxprint-mods.tex (UI option "Ref Before Caption" exists on Advanced › Other). Also refers to "Pictures > Settings tab" and "Omit References (ch:vs) From Caption"; the sub-tab is now "Global Options" and the option is "Omit References (ch:vs)". | "...To put the reference BEFORE the caption, tick 'Ref Before Caption' on the Advanced tab (Other sub-tab). To hide caption references everywhere, use 'Omit References (ch:vs)' on the Global Options sub-tab." |
| `c_includeillustrations` | Says `\zimagecopyrights` is used "within the Colophon (see the Header+Footer tab for details)". The colophon is on the Peripherals tab. | "...using the \zimagecopyrights code in the Colophon (see the Peripherals tab)." |
| `btn_requestIllustrations2` | Button label "Request Accesss..." (3 s). Tooltip: "sumitting". | Label "Request Access..."; "submitting". |
| `btn_requestIllustrations` | "sumitting". | "submitting". |
| `c_plCreditOverwrite` | Label "Overwite any existing settings". | "Overwrite any existing settings". |
| `btn_plDel` | "highligted"; also deletes all selected rows, not just one. | "Click to delete the selected picture(s) immediately. No confirmation is asked for!" |
| `c_useCustomFolder` | "getted scanned", "explicity". | "Note that ALL subfolders are also scanned unless you explicitly enable the 'Exclude Subfolders' option." |
| `c_randomPicPosn` | "are place in" ; "top-right bottom-left" missing comma. | "By default all illustrations are placed in the top-left corner... (top-left, top-right, bottom-left and bottom-right)." |
| `fcb_ptxMapBook` | "bookx"; says it "will overwrite whatever is in that book without prior warning", but `addMapsClicked` appends to an existing book file. | "...If you prefer to use one of the other Paratext books XXA...XXG, select it here. If the book already exists, the maps are added at its end." |
| `fcb_coordBorder` | Description and tooltip are copied from the cover dialog ("Generate cover: Select Ornamental Border", "...applied to the front cover page"). Also the setting does not appear to be used by `addAnotherMapClicked`. | Tooltip: "Choose an ornamental border for the map." (and check whether the setting should be wired up). |
| `btn_selectMap` | Description "Generate cover: Select Background Picure (or Image)" – copied from cover dialog; "Picure" misspelt. | "Maps: Select the map image file". |
| `fcb_mapRotate` | Description/tooltip copied from credit dialog ("Rotation of text", "Sometimes the credit text needs to be rotated"). It rotates the map image. | "Rotate the map image by 90° (anti-clockwise or clockwise)." |
| `c_mapSpread` | Setting does not appear to be used anywhere in the Python code. | Check whether it should be wired up, or hide it. |
| `c_imgMediaP`, `c_imgMediaA`, `c_imgMediaW` (Select Images dialog) | These filter checkboxes are not read anywhere in picselect.py/gtkview.py, so they do not filter the thumbnails. | Wire them up, or hide them until they work. |
| `c_exclusiveFiguresFolder` | Tooltip says only the selected folder is searched. In the code, `exclusive` is passed to `build_searchlist` but `gatherIllustrations`/`getFigureSources` are called without `exclusive`, so `os.walk` still searches subfolders at print time. | Check the code; then reword if needed. |
| `textv_picNotes` (label "Notes About This Picture") | Label tooltip says notes are "available and editable in ALL publications of this project". `PicChecks.savepic` saves notes into `cfgProject` (per-configuration picChecks.txt), and `loadpic` has a comment "MH - this doesn't seem to be working". | Either store notes in the shared picInfo.txt, or change the tooltip to "...saved with this configuration". |
| `fcb_plPgPos` | Tooltip lines run together (no line breaks between "Top: ...", "Bottom: ..." etc.), and "Below Notes" is not described. | Put each position on its own line and add "Below Notes: below the footnotes (Span Width only)". |
| `fcb_plMirror` | Lines run together ("Never = ... Odd = ..."). | Put each choice on its own line. |
| `lb_omitPics` | No tooltip on the "How?" link. | "Open a web page that explains how to mark pictures in Paratext for print, web or app." |
| `c_protectPicList` | Text "[In future...] This option may highlight..." describes a future feature. | Remove the "[In future...]" paragraph. |


## 10-diglot-tooltip-issues

## Tooltip issues – 10-diglot

| ID | Problem | Suggested wording |
|----|---------|-------------------|
| `t_layout` (and its label) | Says a forward slash `/` puts one text under another, but `validate_layout()` rejects `/` ("Complex layouts are not yet supported") unless the experimental flag is set. Also does not mention `-` (blank page). | "The Layout string describes where each text goes. Letters together share a page side by side; a comma starts the facing page; a hyphen (-) is a page with no text. Every code in the table above must be included. It is normally filled in for you from the 1\|2 column." |
| `fcb_diglotMerge` / `l_diglotMergeMode` | "Scored (Verses)" in the tooltip, but the list item is "Scored (Verse)". Double spaces ("weighted scores which  tries"); "which tries" should be "which try". | "...* Scored (Verse) – as a minimum, forces alignment at each verse, which can result in many breaks." |
| `c_diglotHeaders` | Widget is hidden (`no-show-all`, not visible) and `document/diglotheaders` is not used anywhere in texmodel/template/TeX, so the tooltip promises behaviour that does not happen. | Remove the control, or implement it. |
| `c_diglot` | Tooltip does not warn that ticking cannot be undone simply (unticking opens Save As Monoglot), nor that a secondary project/config must be chosen. | "A Diglot contains two languages, scripts or texts; a Polyglot contains more. Right-click in the table below to add texts. Tip: use Save As first – a diglot configuration cannot simply be switched back to a single text." |
| Grid column **1\|2** (gtkpolyglot.py tooltip) | Missing word: "Specify whether the should be on the left (1) or right (2) page." | "Specify whether this text should be on the left (1) or right (2) page of the spread." |
| Grid column **Code** (gtkpolyglot.py) | "Right-click to change background color" – right-click opens a menu; the colour is via **Set Color...** in that menu. | "Unique identifier for the text (L, R, A, B, ... G). Right-click and choose Set Color... to shade this text's column." |
| Grid column **Weight** (gtkpolyglot.py) | "(as %)" is misleading; values are relative weights passed to the merge scorer, not percentages that must sum to 100. | "The relative weight of this text when the texts are merged and aligned. Leave equal unless alignment is poor." |
| `btn_adjust_diglot` | Mentions "the starting position of the slider" – there is no slider any more; widths are in the % Width column. Also not stated that it only works for exactly two texts. | "Automatically find the % Width for L and R that gives the fewest pages. It prints the job 10 or more times, so select a short book first. Only available for a diglot with two texts." |
| `b_print2ndDiglotText` | Fine, but the big button is labelled "Return to Primary", not "Return". | "...Use the larger 'Return to Primary' button to get back..." |
| `t_newMonoglotConfigName` | "Roman/Latin names" – ok, but should mention brackets are allowed (code allows `()`); the tooltip says parentheses – fine. No change needed beyond consistency. | – |

### Code issues noticed (not tooltips)

* `view.py` `mergeCaptions()` reads `self.get("s_diglotSerialBooks", "FRT BAK GLO")`, but the widget is `t_diglotSerialBooks`, so the user's serial book list is never used for picture caption merging (always the default "FRT BAK GLO").
* `gtkpolyglot.py` `onDiglotAutoAdjust()` sets `self.isDiglotMeasuring = False` on the PolyglotSetup object instead of `self.view.isDiglotMeasuring`, so after one auto-adjust run the view flag stays True and the button may not work again until restart.


## 11-tabsborders-tooltip-issues

## Tooltip issues – 11-tabsborders

| ID | Problem | Suggested wording |
|----|---------|-------------------|
| `r_sectHead_legacy` | Copied from the page border: "Use an existing PDF Border for the entire publication." This option places a PDF graphic behind each section heading. | "Place a PDF graphic behind each section heading (\s, \s1, \s2). Use Select... to choose it, and Scale/Shift to fit it." |
| `r_sectHead_dynamic` | Copied from the page border: "Place a decorative border only around the Scripture text (excludes introductions...)". | "Draw a box around each section heading that grows with the heading. Its look is set by the cat:headingsbox\|esb style." |
| `lb_style_vp` | Says "edit the \v marker's properties" – the link opens the `\vp` style. | "Click to edit the \vp style (used for verse numbers moved to the end of the verse)." |
| `r_thumbText_toc3`, `r_thumbText_zthumbtab` | Spelling: "Pheripherals" → "Peripherals". Glade `name` (description) is wrong for both: "Decorative verse numbers: Use end of Ayah". Also the greying-out only happens when the Table of Contents is enabled. | Fix spelling; names "Thumb tabs: Use \toc3 text" / "Thumb tabs: Use \zthumbtab text". |
| `r_thumbText_zthumbtab` | Two apostrophes after `\zthumbtab''` (typo). | Remove the stray quotes. |
| `col_thumbback` | Tooltip repeats the same idea twice ("Thumb Tabs usually use a dark color..." twice). | "The background colour of the tabs. Use a dark colour; set the light text colour with the Edit Style link." |
| `s_thumbtabs` | Mentions "Width" – there is no Width control; the controls are Height and Length. | "...calculated from the Height (or Length when rotated), page size and margins..." |
| `fcb_rotateTabs` | Listed label is "Length" (shares a label with the length spin button) – there is no visible label of its own; consider a label "Orientation:". Tooltip OK. | – |
| `btn_resetTabGroups` | Label in listing is "Grouped Tabs" (same as the text box); a clearer button tooltip could say the typed groups will be replaced. | "Replace the Grouped Tabs list with PTXprint's default groups." |
| `c_thumbtabs` | "help the user find a scripture book easier" → "more easily". | – |
| `s_inclSectionShift` vs `s_verseDecoratorShift` | Opposite sign conventions (section: + = down; verse: + = up). Tooltips are correct but this is confusing; consider making them consistent. | – |
| `s_inclSectionScale` / `s_verseDecoratorScale` | "1.0 is unity" – unclear for non-native speakers. | "1 = the graphic's own size; 0.5 = half size; 2 = double size." |
| `lb_style_textborder` | Handler `onOpenTextBorderDialog` calls `self.styleEditor.sidebarBorderDialog()`, which does not exist in gtkstyleditor.py (AttributeError). The link probably does nothing / errors. | Fix code: use `onEditStyleClicked` like the other links. |
| `lb_style_pageborder` | No signal handler is connected (only a non-URL `uri`), and no `\pageborder` style or TeX implementation exists for `fancy/pagebordertype=page`. The **Page Border** option (`r_border_page`) appears to have no effect. | Implement or hide. |
| `fcb_sbBorderStyle` | Glade `name` is "Font Selection Dialog: Typeface" (copy-paste). No tooltip. | name "Borders dialog: Border type"; tooltip "None, a single line, a double line, or an ornamental pattern." |
| `fcb_sbBorderOrnament` | Glade `name` is "Generate cover: Select Ornamental Border" – this is the Border Settings dialog, not the cover. List item "c86out" looks like a typo for "v86out"? | name "Borders dialog: Ornamental border". Check "c86out". |
| `s_sbBoxPadT/B/L/R`, `s_sbBdrPadT/B/L/R` | Glade `name` descriptions don't match position (e.g. `s_sbBoxPadT` = "Horizontal box padding", `s_sbBoxPadB` = "Horizontal border padding" on the Box tab). The "All/Top (pt)" label tooltip talks about horizontal space between left/right borders. All tooltips say "in the sidebar", although the dialog is also used for text borders, title boxes and heading boxes. | Names: "Borders dialog: Box padding top/bottom/left/right" and "Border padding ...". Label tooltips: "Top padding (all sides when Uniform is ticked)" etc. Replace "sidebar" with "box". |
| `lb_openOrnamentsCatalog` | "Click to Open" capital O. | "Click to open a PDF catalogue of the ornamental borders (pages 4–7)." |
| `s_sbBorderWidth` | Default 2 pt; for ornaments "at least 10pt" – fine. | – |


## 12-styles-tooltip-issues

## Tooltip issues – 12-styles (Styles tab and its dialogs)

| ID | Problem | Suggested new wording |
|---|---|---|
| `s_sbiCutoutLines` | Wrong tooltip. It is copied from the graph-paper grid setting ("number of minor divisions … centimeters/inches"). | "Number of lines below the top of the sidebar where the cutout for the foreground image starts." |
| `fcb_sbi_posn_above`, `fcb_sbi_posn_beside` | Tooltip is copied from picture placement (Top/Bottom of page, Before Verse, After Paragraph). These lists place the image *inside* the sidebar. | above: "Where the foreground image goes in its own strip above or below the sidebar text (top/bottom, and left/inner/centre/right/outer)." beside: "Which side of the sidebar text the foreground image goes on, and whether it is at the top, centre or bottom of that side." |
| `fcb_sbi_posn_cutout` | No tooltip. | "Which side of the sidebar text the cutout for the foreground image is on." |
| `s_sbWidth` | Says "as a percentage (%)" but the value is a factor (0.25–2.5, 1 = full width). | "Sidebar width as a proportion of the column/page width (1.0 = full width, 0.5 = half)." |
| `fcb_sbSize` | The text is repeated twice (two versions merged). | Keep one copy: the first four paragraphs plus "When using single column layout, there is no difference between Column Width and Span Width." |
| `fcb_styType` | Same sentence repeated twice with small differences. | "[Required] This tells PTXprint what kind of marker this is." |
| `col_sb_backColor` | Two different sentences joined ("Sets the background color for sidebar. Background shading color."). | "Sets the background colour of this category of sidebar." |
| `s_styFontSize` | "This a factor" – missing "is". Also does not mention that it is disabled for \p. | "This is a factor of the base font size. 1.0 is the same as the Base Font Size on the Layout tab. (For \p, set the size on the Layout tab.)" |
| `s_styLineSpacing` | "This a proportion" – missing "is". | "This is a proportion of the base line spacing…" |
| `c_styFontScale` | "an an amount"; refers to "Font Size Unit", which is not a name the user sees. | "Normally the font size is relative to the Base Font Size (Layout tab). Tick this to make it relative to the size of the surrounding text instead. Note that \p has a font size of 12 in the underlying stylesheet." |
| `s_stySpaceAfter` | "layout tab" – should be capitalised "Layout tab" (consistent with Space Before). | "…multiplied by the base line spacing from the Layout tab." |
| `fcb_sbiLayerOrder` | Spelling: "tranpsarent". Also has an odd line break after "background image". | "…Line art PDFs with a transparent background…" |
| `t_sbiBgCropOfs` | Says it is used when Oversize is set to Crop, but the Crop choice is labelled "(unimplemented)". | Add "(Crop is not implemented yet, so this currently has no effect.)" – or hide the control until Crop works. |
| `btn_styDel` | Does not say that only user-added styles can be deleted; for standard styles the button silently does nothing. | "Click to delete this style (only styles you have added can be deleted). Warning: There is no confirmation or undo!" |
| `btn_styReset` | Does not say what "default values" are, and that it removes all Styles-tab changes for this marker. | "Click to remove all changes made on this tab to this style, returning it to the values in the underlying stylesheets." |
| `fcb_sbPgPos` | Run-on text with no line breaks; "Fill" and "Below Notes" not explained. | "Top: above everything except the header. Bottom: below the text. Below Notes: below the footnotes (Span Width only). Before Verse: where it is in the text. After Paragraph: after this paragraph. Cutout: a notch cut out of the text, starting at the current line. Fill: stretch to fill the page (page sizes only)." |
| `s_sbLines` | Description says "Picture: Lines to adjust vertically" although this is the sidebar dialog (shared with maps). Minor. | "Sidebar/map: lines (or paragraphs) to move vertically". |
| `s_styNoteCallerRaise` | Description is "Note caller style" but the control is the note caller *raise*. | "Note settings: Note caller raise". |
| `btn_sbSizePosition`, `fcb_stytcVpos`, `btn_sbSelectFile`, `t_styMarker` | No tooltip. | Size and Position: "Choose the frame size and position of this category of sidebar on the page." tcVpos: "Where text sits vertically in a table cell that is shorter than the tallest cell in the row. Gridded Center keeps the text on whole lines." Marker: "The marker code without the backslash, e.g. zpeople or cat:people\|esb. Can only be set when adding a new style." |

Documentation note (not a tooltip): `docs/documentation/SideBars.md` still calls the publishable control "Hide/exclude contents of marker"; the UI now uses the opposite sense, "Include Contents of Marker".


## 15-peripherals-tooltip-issues

## Tooltip issues – 15-peripherals (Peripherals tab)

| ID | Problem | Suggested new wording |
|---|---|---|
| `lb_style_cat:coverwhole\|esb` | Tooltip says "for the Front Cover" (copied from the Front Cover link). This link is for the whole cover spread. | "Click to edit the Sidebar properties on the Styles tab for the whole Cover Spread (the background behind the back, spine and front)." |
| `t_tocTitle` | Out of date. No file called "combined.toc" is made, and the ToC is not "prepended to the output PDF": it goes on PTXprint's own contents page (no local front matter) or where `\ztoc\|main\*` is in the front matter. The tooltip does not say what the box is for. | "The heading for the Table of Contents (for example 'Contents' in your language). It can also be used in the front matter as \zvar\|toctitle**." |
| `c_autoToC` | "the print process will be run at least twice … So it may be worth leaving this option OFF until the final run" – PTXprint now reruns automatically within one click of Print (unless Quick Run is ticked). The claim "ignored unless Multiple Books has been set" could not be confirmed in the code (the ToC is generated whenever the option is on). | "…PTXprint typesets the text more than once to get the page numbers right, so printing takes longer. (With Quick Run on, click Print a second time.) If Local Front Matter is on, put \ztoc\|main\* in the front matter where the ToC should appear." |
| (label "Colophon Text", no ID) | Lists the localized `\zimagecopyrights` languages as "ro, hu, es, fr, ru". picCopyrights.json has en, es, fr, hu, id, pt, ro – there is no `ru`. | "(es, fr, hu, id, pt, ro available)". |
| `c_colophon` | "The colophon will not appear the first time you run it, but will appear on subsequent runs." The colophon text is placed directly by the template; only the picture credits (`\zimagecopyrights`) need a second run. | "NOTE: The picture credits (\zimagecopyrights) are only correct after you click Print a second time." |
| `c_inclFrontMatter` | Mentions a Canva.com "link provided", but there is no such link on the tab. | Remove the second paragraph, or add the link. |
| `c_inclFrontMatter`, `c_inclBackMatter` | Say that multiple files "will appear in alphabetical order". The code keeps the files in the order returned by the file dialog; no sorting was found. Please check. | Either sort the list in code, or remove "in alphabetical order". |
| `c_frontmatter` | Does not mention the side effects: ticking it unticks "Colophon at End of Publication"; unticking it ticks the colophon and turns off "Create Cover Page". Users are surprised by this. | Add: "Note: turning this on turns the Colophon off (you can turn it on again). A cover needs Local Front Matter." |
| `c_makeCoverPage` | No tooltip. | "Create a cover (back, spine and front) as a separate PDF file ending in _cover.pdf. Needs Local Front Matter. Use the Cover Wizard to design it." |
| `c_inclMaps` | No tooltip. | "Add the map book (usually XXM) to the list of books to print. Use Add Maps... to create the map pages." |
| `btn_resetColophon` | Fine, but does not warn that the current colophon text is replaced. | "…Your current colophon text will be replaced." |


## 16-publications-tooltip-issues

## Tooltip issues – 16-publications (Publications tab)

| ID | Problem | Suggested new wording |
|---|---|---|
| `tv_publications` | No tooltip. Users may not know that the names, books and values can be edited by clicking them. | "Click a publication name, its books, or a field value to change it. Books shown in red cannot be understood – hold the mouse over them to see why." |
| `btn_pubPrint` | Does not say that the PDFs are made in the background, are not shown in the preview, and that the folder is opened when all are done. | "Save the configuration, then create a PDF for each ticked publication (in the background). The folder with the PDFs opens when they are finished." |
| `btn_pubDuplicate`, `btn_pubDel` | Do not mention that they are greyed out until a publication is highlighted. | Add "(Click a publication first.)" |


## 17-finishing-tooltip-issues

## Tooltip issues – 17-finishing (Finishing tab)

| ID | Problem | Suggested wording |
|----|---------|-------------------|
| `s_foldCutMargin` | The same sentence appears twice ("The width of the area…" and "The minimum width of the area…"). | "The minimum width (in mm) of the area that is cut off after the signature is folded." |
| `col_ndiffColor` | The first sentence is repeated, and a general sentence is in between. | "Colour used in the diff PDF for anything added (or moved to this place) in the new PDF." |
| `col_odiffColor` | The first sentence is repeated, and a general sentence is in between. | "Colour used in the diff PDF for anything deleted (or moved from this place) since the old PDF." |
| `s_diffpages` | The 2nd and 3rd paragraphs were copied from the colour pickers and are about colour, not page count. | Keep only: "The diff PDF contains page images, which make it large. Limit how many diff pages are created; this also makes it faster." |
| `c_createDiff` | Says "(set on the Finishing tab under 'Compare PDFs')" while the control is itself in that area. | "Make a PDF that shows the differences between this PDF and the selected earlier PDF (see Select... below). If differences are found, the diff PDF opens. Shortcut: Ctrl-R" |
| `c_scaleToFit` | Says the scaling is "based on the Pages per Spread", but the code greys this option out unless Pages Per Spread is 1-up, and it scales each single page to the Physical Paper Size. | "Only for 1-up: scale every page (up or down) so that it fits the Physical Paper Size, centred on the sheet." |
| `col_spotColor` | Says the hue "will get converted to the closest matching Pantone color code". The code (pdf/fixcol.py) only has a comment "convert this to closest pantone code"; no Pantone conversion is done – the separation is named `hsvRRGGBB`. | "Select the hue of the spot colour. Colours close to this hue are printed with the spot ink; everything else in black/grey. Tell your printer which ink to use." |
| `fcb_outputFormat` (and its label) | The combo and label tooltips differ: the label still mentions "Transparency (if CMYK is required)" and "Archive (largest size…)" as if they were formats. Neither mentions Gray or Spot. | Use one text for both: "Screen (fastest, no post-processing); Digital-RGB (PDF/X-4, screens and office printing); Digital-CMYK (PDF/X-4 with transparency); Print-CMYK / Print-Gray / Print-Spot (PDF/X-1a, for professional printers). Tick 'Archive' to also follow PDF/A-4." |
| `s_keepVersions` | The sentence "Up to 20 previous versions can be kept" appears twice. | "By default PTXprint keeps one previous PDF (_1). Up to 20 can be kept. Compare PDFs needs at least 1. Rename a PDF yourself to keep it longer." |
| `c_coverSeparatePDF` | Says "only available if Create Cover is enabled on the Cover tab", but the Cover tab is hidden, and no code reads `cover/makeseparatePDF`: the cover is always split out (`_cover.pdf`) when a cover page is made. | Either connect the setting in the code, or reword: "When a cover is made, it is saved as a separate PDF (_cover.pdf)." |
| `c_applyWatermark` / `btn_selectWatermarkPDF` | The accessible name says "Marks & Guides dialog", but the controls are on the Finishing tab. `btn_selectWatermarkPDF` has no tooltip. | Name: "Finishing: Apply watermark". Button tooltip: "Choose the watermark PDF. It should be the same size as the book page." |
| `l_ndiffOld` | The label **Old Text** has the same tooltip (and accessible name "Colour of new text") as **New Text**, so it describes the colour for *added* text. Also `col_ndiffColor` has the accessible name "Compare PDFs: " (shown as its field label) and `col_odiffColor` has none. | Tooltip: "Use this colour to show anything that has been deleted (or moved from the previous location) in the old PDF." Names: "Compare PDFs: Colour of new text" / "Compare PDFs: Colour of old text". |

### Possible code issues noticed (not tooltips)

* `pdf/procpdf.py`: `_pdfmodes['cmyk']` contains `"Transparency"`, but the combo ID for **Digital-CMYK (Transparency)** is `"Transparent"`. So for that format `colour` becomes `"transparent"`, which `fixpdffile()` does not handle; no CMYK conversion seems to happen. Please check.
* `snippets.py` `PDFx1aOutput`: `_iccnumcols` is set to 3 for Screen/Digital, but the following `if pdftype == "Gray": … else: "4"` overwrites it with 4 for every non-Gray format, including the sRGB ones.
* `runjob.py` `done_job()`: `createDiff(..., color=odiffcolor, ..., oldcolor=ndiffcolor, ...)` – the new/old colours look swapped by name; please check that the colours in the diff match the labels. *(Checked Oct 2026 update: they do. `pdfdiff.createDiff` colours the "new ink" end of the old-minus-new image with `oldcolor`, so passing `ndiffcolor` there is correct: added text is shown in the New Text colour.)*


## 18-printers-tooltip-issues

## Tooltip issues – 18-printers (Printers tab)

| ID | Problem | Suggested wording |
|----|---------|-------------------|
| `lb_Printers` (tab label) | Tab tooltip is "Adjust expert-level settings." – copied from elsewhere; it says nothing about printers. | "Estimate printing costs, compare printers, check book thickness, and (for some printers) get a quotation and place an order." |
| `s_prn_pages` | Does not say what happens before any PDF exists (the code shows 99). | "Number of pages in the book. Filled in from the most recent PDF (99 if no PDF has been made yet). Change it if the printed book has extra pages." |
| `btn_prn_compare` | Says "per-copy prices", but the graph can also show total price. Doesn't say that printers without a price model are left out. | "Show a graph of prices (per copy or total) at several quantities for all printers ticked in the Compare column." |
| `fcb_prn_currency` | Doesn't say that exchange rates come from the internet. | "Currency used to show all prices. Prices from other countries are converted using exchange rates downloaded from the internet (a guide only)." |
| Pretore `s_prnl_ribbons` (runtime widget) | Uses "Hardback" while the Binding list says "Hardcover". | "Number of marker ribbons (Hardcover only)." |


## 19-preview-tooltip-issues

## Tooltip issues – 19-preview (PDF Preview window, SpeedSlice, anchor dialog)

| ID | Problem | Suggested wording |
|---|---|---|
| `b_reprint` | Says "Shortcuts: Ctrl-P or click the middle mouse button". I could not find any code that prints on a plain middle-click. In the preview, middle-button drag pans the page and Ctrl/Shift+middle-click resets a paragraph's adjustments. | "Update the PDF. Shortcut: Ctrl+P" |
| `c_updatePDF`, `l_updateDelay` | Says the delay is in "Advanced > Other > Other Miscellaneous Settings". The setting (Auto-update Delay) is actually in the group "Preview Pane: Adjustment and Analysis Settings". | "...This delay can be changed by clicking on the value shown here, or in Advanced > Other > Preview Pane: Adjustment and Analysis Settings." |
| `c_layoutAnalysis` | Lists only 3 issue types (collisions, horizontal space, rivers). The Locate popup also has Bad Glyphs (missing characters). Underfilled pages are found without analysis. | "Analyzes the text to highlight layout issues: glyph collisions, missing glyphs (bad glyphs), excessive horizontal space, and vertical rivers of space. Also enables the Locate... button." |
| `c_pdfadjoverlay` | Spelling: "ajustment". Also "shrink/expand" wording in the key is repeated; "stretched/expanded" should be "shrunk/expanded"? | "These adjustment annotations are not part of the PDF..." and "Interleaved red+blue indicates that both the number of lines and the text width have been changed." |
| `l_pdfPgCount` (shown on `btn_page_first` in the listing) | Grammar: "Negative page number refer to the peripheral pages". Also the extractor attached this label's text "(15)+52" to `btn_page_first`. | "Negative page numbers refer to the front pages before the main text begins on Page 1." |
| `s_pdfZoomLevel` | Spin range is 10–1000 but the code clamps the zoom to 10–800 (`onZoomLevelChanged`). | Change the adjustment upper limit to 800, or the clamp to 1000. |
| `l_newAnchorMsg1` (SpeedSlice dialog label) | Spelling: "pevious". | "Enter a chapter number (e.g. JHN 4) or the last verse of the previous page (e.g. GEN 3:23)" |
| `t_sliceRef` | "Previous content will be skipped over" – does not warn that the slice stays on until Disable is clicked. | Add: "SpeedSlice stays on (and the PDF contains only the slice) until you click Disable." |
| `btn_slice_ok`, `btn_slice_cancel` | No tooltip. Users may not realise "Disable" is how to turn SpeedSlice off later. | Enable: "Print only this slice of the book (for quick layout work)." Disable: "Turn SpeedSlice off and print the whole book again." |
| `btn_prvAutoFill` / `icon_prvAutoFill2` | Button says "Page Fill tool", icon says "Auto Page Fill dialog", window title is "PTXprint: Page Filler". Three names for one thing. | Use one name everywhere, e.g. "Show/hide the Auto Page Filler (with progress monitor)". |
| Page Filler window `Start Fill` (bookProgressDlg.py) | Tooltip says "Restart filling from the beginning of each book" but does not say that existing adjustments (including manual ones) are discarded. | "Fill from the beginning of each book, starting from no adjustments (existing AdjList entries for these books are replaced). Warning: CPU-hungry." |
| `btn_findButton` | "It is only enabled when Layout Analysis is active" – fine, but the underfilled-page arrows work without it, which is confusing. | No change needed if the behaviour is intended; otherwise mention it. |


## 20-import-tooltip-issues

## Tooltip issues – 20-import (Import Settings dialog)

Several import options do not work as labelled because of name mismatches in `view.py` `importConfig` and `modelmap.py`:

| ID | Problem | Suggested fix |
|----|---------|---------------|
| `c_oth_Variables` | **Code bug:** `importConfig` checks `self.get("c_impVariables")`, which is not a widget. Ticking **Variables + Meta Data** does nothing (only Everything, or the "missing vars" step of Front+Back Matter, imports variables). | Use `c_oth_Variables` (and respect `c_impOther`). |
| `c_impFontsScript` | **Code bug:** `exclfields = None if impAll or self.get("c_impFontsScripts")` - typo (extra "s"). Font fields in styles are always excluded unless Everything is ticked. | `c_impFontsScript`. |
| `c_oth_OverwriteFrtMatter` | **Code bug:** the code reads `c_oth_OverwriteFrontMatter`; the widget is `c_oth_OverwriteFrtMatter`. The checkbox has no effect. | Use the right ID. |
| `c_oth_ThumbTabs` | **Code bug:** `ImportCategories` maps it to category `'thumbtabs'`, but the thumb tab entries in ModelMap use category `'tabsborders'`. No thumb tab settings are imported. | Change the category name in one of the two places. |
| `c_oth_customScript` | Not used in `importConfig`; the custom script is imported under `c_oth_Advanced` (when the source has `processscript`). | Use this checkbox for the script part, or remove it. |
| `c_impEverything` (tab text) | Tab text says Everything is "automatically enabled when the target Project or Configuration does not already exist". The code only does this for an external-folder target (`# FIX ME` in `setImportButtonOKsensitivity`). A new target config starts from PTXprint defaults, so without Everything most settings are default. | Implement it, or change the text to "...when exporting to an external folder." |
| `c_impEverything` (code) | `_sensitivities["c_impEverything"]` makes the five category boxes sensitive only when Everything is ticked (inverted logic). It is only applied in loadConfig and is overridden by `setImportButtonOKsensitivity`, but it is misleading (the generated listing says "Only available when Everything is selected"). | Move to `_nonsensitivities` or remove. |
| `c_impLayout` (tab text) | Says it imports "header and footer" settings. Header/footer entries are category `headfoot` (Other > Header+Footer settings), not `layout`. Font size (`paper/fontfactor`) is in Fonts+Script, not Layout. | "...page size, column layout, margins, line spacing and related settings. (Font size is in Fonts+Script; header and footer are in Other.)" |
| `c_impFontsScript` (tab text) | Says it imports "spacing and hyphenation". Hyphenation entries are category `body` (Other > Body Tab settings). | "...the major font and script settings and spacing. (Hyphenation is imported with Other > Body Tab settings.)" |
| `c_impStyles` (tab text) | Says "This will also import styles from ptxprint-mods.sty". In the code, ptxprint-mods.sty is only merged with Advanced settings or Everything. | Merge mods.sty under Styles, or change the text. |
| `ecb_targetProject` | Says you can "Enter a NEW project name which causes a (temporary) project to be created". `_getProject` returns None for an unknown name and `importConfig` then fails on `tgtPrj.guid`. The second paragraph ("Select the project from which the settings will be imported") is copied from the source tooltip and is wrong here. | "Select the project into which the settings will be imported." |
| `ecb_targetConfig` | Second paragraph "Select a configuration from the selected project from which the settings will be imported" is wrong for the target. | Remove it. |
| `t_targetConfig` | Mentions "the Notes field below" - there is no Notes field in this dialog. | Remove that sentence. |
| `r_impTarget_prjcfg` | Description (accessible name) is "Import: From Saved Configuration" - a copy of the source radio. | "Import: Into Project/Configuration". |
| `btn_resetConfig` | Does not say that the reset is not saved until Save/Print/OK. | Add "The change is saved when you next save, print or import." |
| `c_impPictures` ... `c_oth_Finish` | Most category checkboxes have no tooltip. | Short tooltips listing what each brings in (see the manual chapter). |
| `ecb_targetProject` | The tooltip says the same thing twice ("Select an existing project into which..." / "Select the project into which..."). | "Select the existing project into which the settings will be imported." |

### Possible code issues noticed (Oct 2026 update)

* `view.py` `_importConfigInto()`: the `c_impOther` tooltip says that if **Other** is not ticked, none of the boxes on the Other tab are used. That is true for the settings categories (the `c_oth_` loop) and for Custom Script and Variables, but the file handling for **Advanced settings** (mods.sty, changes.txt, mods.tex), **Cover settings** (cover styles and periphs) and **Front +Back Matter** (FRTlocal periphs, missing variables) tests `self.get("c_oth_Advanced")` / `c_oth_Cover` / `c_oth_FrontMatter` without `hasOther`. A box left ticked on the greyed Other tab therefore still brings in those files. The manual follows the tooltip.


## 21-help-tooltip-issues

## Tooltip issues – 21-help (Help tab)

| ID | Problem | Suggested wording |
|----|---------|-------------------|
| `l_projects_dir` | Tooltip was copied from `l_working_dir` (talks about the PDF output folder and temporary files). That is wrong for the Base Projects Directory. | "The folder that contains all your Paratext project folders. Use Change... to choose a different one." |
| `btn_generateReport` | Spelling: "mesaages". | "…informational, warning and error messages about fonts, styles, layout and so on." |
| `lb_masterSlides` | "There is a an extensive…" (extra "a"). Also this link is in `_ui_keepHidden` and is not in the `noInternetClicked()` list, so it is never shown. | "There is an extensive Google Slides presentation which can be used as a reference for training." |
| `l_techFAQ` | Tells users to copy code snippets into ptxprint-mods.tex or changes.txt, but the label is now the heading for the Ornaments Catalog and Technical Reference PDFs. | "Reference documents that come with PTXprint: the Ornaments Catalog and the Technical Reference (for advanced users)." |
| `l_reportBugs` | Long text about Python/PyGTK/Glade/XeTeX is not useful for users. | "Found a bug? If you have a GitHub account, report it here. Otherwise email ptxprint_support@sil.org." |
| `btn_createZipArchiveXtra` | Could mention that the job is printed again first (it takes time) and that fonts, pictures and text are included. | "Create a ZIP file of everything needed to make this PDF again (settings, text, fonts, pictures). The job is printed again first. Keep it small: select only the book(s) with the problem and turn off pictures if they are not involved. Email it to ptxprint_support@sil.org" |
| `btn_deleteTempFiles` | Does not say it deletes the temporary folders of *all* configurations of the project, not only the current one. | "Delete the TEMPORARY working folders of all configurations of this project. PDF files and settings are kept." |
| `lb_giveFeeback` | Widget ID is misspelled ("Feeback"). Not user-visible. | – |

### Behaviour notes (not tooltips)

* `l_ptxprintdir`, `l_techFAQ`, `lb_ornaments_cat`, `lb_tech_ref`: the UI map says Default and Full views, but `noInternetClicked()` sets them visible only when `uilevel >= 6` (Full). The manual follows the code.
* `tb_Logging` / `tv_logging` (Log tab) are in `_ui_keepHidden` and never shown. Consider removing them, or adding a way to show them.


## DECISIONS

## Decisions needed – PTXprint UI review

Items found while writing the UI manual that need a decision from the PTXprint team before
anything is changed. The obvious text fixes (spelling, wrong/copied tooltips, missing tooltips,
outdated names) have already been applied to ptxprint.glade, gtkpolyglot.py and printers/pretore.py.

Each item: **Issue**, **Options**, **Suggested**. Grouped by manual chapter; the triage list
below picks out the most important ones first.

### Triage – most important first

**1. Data loss**
- 03-basic › `btn_deleteConfig`: deleting ANY configuration deletes the whole `local/ptxprint`
  folder (every configuration's PDFs and working files) – `rmtree(printPath(None))`.
- 03-basic › `btn_resetDefaults`: Reset on Default deletes the Default folder (styles, piclist,
  adjlists, FRTlocal.sfm) with no confirmation.
- 12-styles › `btn_styReset`: style Reset likely wipes user-created styles (key case mismatch in `onStyleRefresh`).

**2. Features that are broken by small code bugs**
- 08-headfoot › `ecb_ftrcenter`: "Time (HH:MM)" item has id `<Enter ID>` – prints that text instead of the time.
- 03-basic › password dialog: Cancel locks the config with an empty password; OK/Cancel ids swapped.
- 20-import: Variables, Fonts (in styles), Overwrite Front Matter and Thumb Tabs import options do nothing (wrong widget/category names).
- 10-diglot: `mergeCaptions()` reads `s_diglotSerialBooks` (should be `t_`); `onDiglotAutoAdjust` resets the wrong flag (button stuck).
- 07-notes / 20-import › `_sensitivities`: duplicate dict keys (`r_xrpos`, `c_doublecolumn`) – only the second entry of each is used.
- 08-headfoot › `texmodel._addLR`: missing comma joins `\isodate` and `\book`.
- 17-finishing: `"Transparency"` vs `"Transparent"` (Digital-CMYK gets no CMYK conversion); `_iccnumcols` needs `elif`; diff colours look swapped.
- 11-tabsborders: `\textborder` link calls a method that does not exist; Page Border option has no implementation.

**3. Settings that are saved but do nothing** (wire up, hide, or say so in the tooltip)
- Filter Categories, cross-reference rule checkbox, `s_ef_bottomRag`, `s_ef_internote`, `s_strongRag` (07-notes);
  Heading in Margin, Optimize Poetry Layout (06-body); `s_hyphMinBlock` (05-fonts);
  Add Map Border/Spread, image picker Print/App/Web filters, Exclude Subfolders (09-pictures);
  `c_coverSeparatePDF` (17-finishing); `c_diglotHeaders` (10-diglot).

**4. Naming and wording choices** – everything else below (renames, defaults to quote, how to describe partly-working features).

---

### 02-main-window (3 items)

Edits made (see `edits/02-main-window.json`): `lb_Printers`, `c_quickRun` (spelling), `c_noupdate`,
`lb_TabsBorders`, `lb_NotesRefs`, `lb_Publications`, and new tooltips for `btn_menu_level`,
`btn_menu_lang`, `btn_menu_showPDF`, `btn_dismissStatusLine`.

#### t_find (onFindKey not connected)

**Issue:** `onFindKey` in gtkview.py (Esc clears the search box) is not connected to any signal in
ptxprint.glade, so pressing Esc in **Search for settings** does nothing.

**Options:**
- Add `<signal name="key-press-event" handler="onFindKey" swapped="no"/>` to `t_find`.
- Remove the unused `onFindKey` method.

**Suggested:** Connect the signal – the handler already exists and Esc-to-clear is expected behaviour.
Check that it returns False for other keys so normal typing is not blocked.

#### btn_menu_lang (language change warning)

**Issue:** The reviewer suggested the tooltip warn "the window is reopened; save first".
`changeInterfaceLang` destroys the main window and calls `onDestroy`, which does not save the
configuration. Whether unsaved changes are lost depends on how the app restarts, which I could not
confirm. The added tooltip only says what the menu does.

**Options:**
- Leave the tooltip as added.
- Add "Unsaved changes may be lost – save first." after confirming the behaviour.
- Make `changeInterfaceLang` save the current config before rebuilding the window.

**Suggested:** Save the config in code before switching (safest for users); then no warning is needed.

#### btn_dismissStatusLine (Copy to Clipboard mode)

**Issue:** For Alt-X (Unicode) status messages the same button is relabelled "Copy to Clipboard" and
copies the text. The new static tooltip only says "Hide this message."

**Options:**
- Keep the static tooltip.
- Also set the tooltip in `doStatus` when the label changes (e.g. "Copy these codes to the clipboard and hide the message.").

**Suggested:** Set the tooltip in `doStatus` alongside the label – a one-line code change.

### 03-basic (4 items)

Edits made (see `edits/03-basic.json`): `btn_resetDefaults`, `ecb_savedConfig`, `ecb_booklist` (2 places:
combo and its entry), `ecb_licenseText`, `textv_copyright`, new tooltips for `r_book_single`,
`r_book_multiple`, `r_book_module`, `t_chapfrom`, `t_chapto`, and `btn_copyToTargetProj`,
`r_copyConfig_overwrite`.

#### btn_deleteConfig (deletes ALL output of the project)

**Issue:** Serious. The tooltip says previously created PDFs "will remain in that folder", but
`onDeleteConfig` (gtkview.py ~line 2874) calls `rmtree(self.project.printPath(None))`, which removes the
whole `local/ptxprint` folder: the PDFs and working folders of **all** configurations. The error
message on the next lines already uses `printPath(self.cfgid)`, which suggests `printPath(cfg)` was meant.

**Options:**
- Change to `rmtree(self.project.printPath(cfg))` (only that configuration's working folder) – tooltip stays correct.
- Keep the code and rewrite the tooltip to warn that all PDFs of the project are deleted.

**Suggested:** Fix the code to `printPath(cfg)` (note: `cfg`, the config being deleted, not `self.cfgid`).
Deleting every PDF of every configuration is almost certainly unintended.

#### btn_pw_cancel / btn_pw_ok (password dialog)

**Issue:** The IDs are swapped (button labelled **OK** is `btn_pw_cancel`, **Cancel** is `btn_pw_ok`);
the responses are correct so users do not see this. But in `onLockUnlockSavedConfig` a CANCEL response
sets `pw = ""` and continues, so clicking Cancel on an unlocked config **locks it with an empty
password**. Closing with the window X returns without `dialog.hide()`.

**Options:**
- On CANCEL (and any other response): hide the dialog, clear `t_password` and return.
- Also swap the two IDs to match their labels (check for code references first).

**Suggested:** Fix the CANCEL branch and hide the dialog on every exit path. Swapping the IDs is optional tidy-up.

#### t_DBLprojName (and the "Step 3" label next to it) – "8 characters or less"

**Issue:** The tooltip says "Use 8 characters or less", but `onProjectKeyPressed` only rejects spaces /
special characters and existing names; the entry allows 20 characters (`max-length`).

**Options:**
- Enforce an 8-character limit (set `max-length` to 8 or check in `onProjectKeyPressed`).
- Soften the text to "Use a short name (8 characters or fewer is best)".
- Leave as is (it reads as advice).

**Suggested:** Soften the wording on both the entry and the Step 3 label – Paratext short names are
usually short, but nothing breaks with longer ones, so a hard limit is not needed.

#### btn_resetDefaults (no confirmation)

**Issue:** The tooltip was corrected to say that the Default configuration folder (styles, picture list,
adjust lists, front matter …) is deleted and that there is no confirmation. Whether that behaviour is
wanted is a separate question.

**Options:**
- Keep behaviour (tooltip now matches).
- Add a confirmation dialog (like `dlg_confirmDelete` for other configs).
- Only reset `ptxprint.cfg` and keep the other files (then revert the tooltip edit).

**Suggested:** Add a confirmation dialog – a one-click, unconfirmed delete of styles and front matter is
easy to trigger by accident.

### 04-layout (1 item)

#### s_ruleThickness, l_ruleThickness
**Issue:** The tooltip says this sets the thickness of the header rule, the column gutter rule and the
study-notes rule, but both widgets sit inside `gr_doubleColumn`, which is greyed out when
`c_doublecolumn` is off. So in one-column layouts the header-rule thickness cannot be changed, although
`\RuleThickness` (template.tex) still applies.
**Options:**
- Move the control out of `gr_doubleColumn` (or make it sensitive whenever a horizontal rule is used).
- Leave the sensitivity and add "(only available with two columns)" to the tooltip.
**Suggested:** Move the control out of `gr_doubleColumn` so it is always available. The value is used in
one-column layouts too, so greying it out there is wrong.

### 05-fonts (4 items)

#### btn_generateHyphenationList (also c_hyphenate)
**Issue:** The button label is "Import List...", the widget name and dialog title say "Create
Hyphenation List", and the tooltip says "generate". Users look for a "Create" button. (The c_hyphenate
tooltip now names the button "'Import List...'" to match today's label.)
**Options:**
- Rename the label to "Create List..." (and update c_hyphenate's tooltip to match).
- Keep "Import List..." and change the dialog title/tooltip to "import".
- Leave as is.
**Suggested:** Rename the label to "Create List...". It matches the dialog title, and the button builds a TeX
list from Paratext's HyphenatedWords.txt rather than importing one as is.

#### c_nonBreakingHyphens
**Issue:** The tooltip (wording now fixed) says hyphens *within words* never break. But
texmodel.py (~line 1398) only converts hyphens that are next to a space (`(?<=\s)-|-(?=\s)`) to U+2011.
When the hyphen list is generated, the flag makes PTXprint use U+2011 instead of U+2010 in
gtkview.py/hyphen.py. It is not clear whether ordinary word-medial hyphens ("well-known") in the text
are really made non-breaking.
**Options:**
- Check the behaviour and reword the tooltip to describe exactly what is converted.
- Change the code so that all word-medial hyphens become U+2011 when ticked.
**Suggested:** Ask the developer what is intended, then fix whichever (code or tooltip) is wrong. I can't
confirm this from the code alone.

#### s_hyphMinBlock
**Issue:** "Minimum word length for a word to block hyphenation." In hyphen.py the `nohyphendata` list
built with `minblock` is never used, so this setting has no effect.
**Options:**
- Implement it (for example, write the long words without hyphen data as `\hyphenation{word}` with no breaks).
- Hide/remove the control.
- Add "(not yet implemented)" to the tooltip.
**Suggested:** Hide the control until it is implemented. A control that does nothing confuses users.

#### s_hyphMinprefix (code)
**Issue:** The tooltip says a hyphen must be at least N characters from the start *or end* of the word.
hyphen.py checks `l.index("-") >= minaffix and l.rindex("-") >= minaffix`. Both checks measure from
the start, so the end-of-word check is missing. (The "the the" typo is fixed in the edits.)
**Options:**
- Fix the code: `len(l) - l.rindex("-") - 1 >= minaffix`.
- Change the tooltip to say "beginning" only.
**Suggested:** Fix the code. The tooltip describes the sensible behaviour.

### 06-body (3 items)

#### t_clHeading, l_clHeading (\ZWNBSP vs \\ZWNBSP)
**Issue:** The reviewer wants `t_clHeading` changed from `\\ZWNBSP` to `\ZWNBSP` (as in `l_clHeading`).
But texmodel.py (~line 1249) inserts the label with
`makeChange(r"(\\c )", r"\\cl {}\n\1".format(clabel))`, so the value is used as a *regex replacement
template*. I tested it: a single `\ZWNBSP` raises "bad escape \Z", and only `\\ZWNBSP` produces `\cl \ZWNBSP`.
So with the current code the `t_clHeading` tooltip (`\\ZWNBSP`) is the correct one and `l_clHeading` is
wrong. Any label containing a backslash or `\1`-style text is affected. (The "Non-Break"/"Non Break"
wording is fixed in the edits to "No-Break".)
**Options:**
- Fix the code to escape the label (e.g. `clabel.replace("\\", "\\\\")` or use a lambda replacement), then
  change `t_clHeading` to `\ZWNBSP`.
- Leave the code and change `l_clHeading` to `\\ZWNBSP`.
**Suggested:** Fix the code, then make both tooltips say `\ZWNBSP`. Users should not need to know about
regex escaping.

#### c_headingInMargin
**Issue:** `document/headinginmargin` is mapped in modelmap.py but not used anywhere in texmodel.py,
template.tex or the TeX macros, so ticking it has no effect. The tooltip also doesn't say that Section
Headings must be on (updateHeadingInMargin needs both Margin Notes and Section Headings).
**Options:**
- Implement the feature.
- Hide the control until it works.
- Add "(not yet implemented)" and "Section Headings must be enabled" to the tooltip.
**Suggested:** Hide the control until it is implemented. If it is kept visible, add both notes to the tooltip.

#### c_optimizePoetryLayout
**Issue:** The setting (`document/cloptimizepoetry`) is never read. texmodel.py's `%\optimizepoetry`
handler applies the poetry balancing hooks whenever "Use Special Features for These Books" is ticked and
the book list is not empty, whether this box is ticked or not. The reviewer also asked for the tooltip to
say it only applies to the listed books (true for the current code). (The double space is fixed in the
edits.)
**Options:**
- Fix texmodel.py to also check `document/cloptimizepoetry`, then add "Applies only to the books listed
  above (not when the list is empty)." to the tooltip.
- Remove the checkbox and document the behaviour as part of "Use Special Features".
**Suggested:** Fix the code to respect the checkbox, then add the scope sentence to the tooltip.

### 07-notes (11 items)

Obvious text fixes are in `edits/07-notes.json` (36 edits). The items below need the lead's input.

#### s_internote, l_internote (sensitivity)
**Issue:** The tooltip describes the gap between the footnote block and the cross-reference block
(when they are *not* blended). In `gtkview.py` `_sensitivities` the key `"r_xrpos"` appears **twice**
in the same dict literal; Python keeps only the second one, so the effective rule is
`r_xrpos_blend → l_internote, s_internote`. The control is therefore enabled only when
cross-references are **blended** with footnotes, which is the opposite of what the tooltip describes.
(The first, overwritten entry also controlled `fr_colXrefs`, `l_xrColWid`, `s_centreColWidth` for
`r_xrpos_centre`, so those are not being toggled either.) The "Footnoes" typo in the name is fixed in the edits.
**Options:** (a) merge the two `"r_xrpos"` entries and decide which positions enable `s_internote`
(probably `r_xrpos_below`/`normal`); (b) leave the code and rewrite the tooltip to match.
**Suggested:** (a) – `\InterNoteSpace` is the vertical kern between separate note classes, so it matters most for "Below Footnotes".

#### r_fnpos_column, gr_doubleColumn (sensitivity)
**Issue:** The key `"c_doublecolumn"` also appears twice in `_sensitivities`; the second entry
(`["l_colXRside", "fcb_colXRside"]`) replaces the first (`["gr_doubleColumn", "r_fnpos_column"]`).
So "End of Column" for footnotes is not greyed out in single-column layout, although its tooltip says it is "only available in 2-column layout".
**Options:** merge both lists under one `"c_doublecolumn"` key; or remove "only available in 2-column layout" from the tooltips.
**Suggested:** merge the lists (code fix, one line).

#### c_xrefrule and the cross-reference rule settings (s_xrAboveSpace, s_xrBelowSpace, s_xrIndent, s_xrLength, s_xrThick, fcb_xrHorizPosn)
**Issue:** `notes/ifxrefrule` is not used in `template.tex`, so the "Show Cross-Reference Rule" checkbox does nothing.
`calcRuleParameters` uses the `xr` rule settings only when footnotes are End of Book (the xref rule then becomes the foot rule) or when cross-references are End of Book (end-note rule). In the usual layout these settings have no effect, and the tooltips do not say so.
**Options:** (a) wire up `ifxrefrule` (like `iffootnoterule`) and use the xr settings for a separate xref block; (b) add to the tooltips: "Used only when footnotes or cross-references are placed at the End of Book. Otherwise the Footnote rule settings apply."; (c) hide the section unless one note type is an endnote.
**Suggested:** (b) now (cheap and honest), (a) later if separate xref rules are wanted.

#### s_ef_bottomRag, l_ef_bottomRag
**Issue:** Always insensitive in glade and has no modelmap key, so it does nothing; the tooltip describes it as working.
**Options:** remove the control; wire it up (a `\bottomrag`-style setting for the study-note columns); or add "(not yet available)" to the tooltip.
**Suggested:** remove (or hide) until it is implemented.

#### s_ef_internote, l_ef_internoteSpace
**Issue:** `studynotes/internote` is written to the config but not used in `template.tex`; the controls are also insensitive in glade. No visible effect.
**Options:** wire it up in the template, or remove the control.
**Suggested:** remove/hide unless the TeX side has a matching parameter ready to use.

#### r_xrSource_standard … r_xrSource_custom (hidden radios used as text store)
**Issue:** These radios sit in a hidden (`no-show-all`) box and exist only to hold descriptions that `onExtListSourceChanges` copies into the `btn_infoXrefSource` tooltip. (The wrong UBS description and the punctuation in the Custom text are fixed in the edits.)
**Options:** keep as is; move the descriptions to a `_()`-wrapped dict in gtkview.py and delete the radios.
**Suggested:** move to a dict in code – simpler and translators still get the strings.

#### r_xrSource_custom ("Search Google for ptx2pdf/xrefs.md")
**Issue:** The tooltip tells users to search Google for the documentation. Not wrong, but a manual-style link would be better.
**Options:** keep; replace with "See the PTXprint documentation (xrefs.md)."; link to the wiki page.
**Suggested:** replace with a short pointer to the documentation once the target location is agreed.

#### c_strongsNotes
**Issue:** No modelmap entry, so the "Notes" component checkbox is not saved and resets each session (xrefs.py reads it directly from the widget).
**Options:** add `"strongsndx/notes": ("c_strongsNotes", "strongs", None)` to modelmap; leave as is.
**Suggested:** add the config key (consistent with the other component checkboxes).

#### s_strongRag, l_strongRag
**Issue:** `strongsndx/raglines` is saved but `generateStrongsIndex` does not use it; no confirmed effect.
**Options:** wire it up (e.g. write a `\bottomrag`/balancing setting into the generated index book); remove the control.
**Suggested:** wire it up if 2-column index balancing is a real need, otherwise remove.

#### c_filterCats, tv_sbCatEdit
**Issue:** The category list is not saved (the `sbcats` code in gtkview.py is commented out) and nothing in texmodel/template uses it. The tooltip promises filtering that does not happen.
**Options:** finish the feature; hide the frame until it works; add "(not yet working)" to the tooltip.
**Suggested:** hide until it works.

#### c_keepBookWithRefs (character used)
**Issue:** The tooltip says a No-Break Space (` `) is inserted, but texmodel.py inserts ` ` (EN QUAD) for this option. Left unchanged because it is unclear whether the tooltip or the code is the intended behaviour.
**Options:** change the tooltip to "a non-breaking space"; change the code to ` `.
**Suggested:** make the tooltip generic ("a non-breaking space") once confirmed that ` ` is treated as non-breaking by the TeX side.

### 08-headfoot (5 items)

Obvious text fixes are in `edits/08-headfoot.json` (21 edits). The items below need the lead's input.

#### ecb_ftrcenter – "Time (HH:MM)" item has id `<Enter ID>` (code/ID bug)
**Issue:** In the glade file the item is `<item id="&lt;Enter ID&gt;" translatable="yes">Time (HH:MM)</item>`.
`_getcomboval` (gtkutils.py) returns the active id when there is one, so choosing "Time (HH:MM)" stores the
literal text `<Enter ID>` and that is printed in the footer instead of `\hrsmins`. None of the other items in this
combo have ids; they are mapped by their text through `localhdrmappings()`.
**Options:** (a) remove the `id` attribute, so the text "Time (HH:MM)" is mapped to `\hrsmins` like the other items;
(b) set `id="\hrsmins"`.
**Suggested:** (a) – consistent with the other items in this combo and with `ecb_hdrcenter`/`ecb_hdrright`.
Existing configs that saved `<Enter ID>` would need re-selecting (or a one-line migration).

#### ecb_ftrcenter, l_ftrcenter – "set Inner/Outer Footers in ptxprint-mods.tex"
**Issue:** The tooltip tells users to edit ptxprint-mods.tex for inner/outer footers. There is no UI option for this, so the advice is still the only way, but the manual's rule is "no file editing".
**Options:** keep the sentence; drop it; replace with "Inner/Outer footers are not available in the UI."
**Suggested:** drop it from both tooltips – it is an expert workaround, better covered in the technical reference.

#### texmodel.py `_addLR` – missing comma (code bug, found while checking r_hdr*)
**Issue:** The list `[r"\firstref", …, r"\isodate" r"\book", r"\bookalt"]` has no comma between `r"\isodate"` and `r"\book"`, so they join into one string `\isodate\book`. In diglots, `\isodate` and `\book` therefore fall through to the `\headfootL{…}`/`\headfootR{…}` branch instead of getting the L/R suffix like the other codes.
**Options:** add the comma; leave as is if the fallback branch is acceptable.
**Suggested:** add the comma (and check a diglot header with Book (\h) on the Secondary side).

#### ecb_hdrleft – item ids vs. other header combos
**Issue:** Only `ecb_hdrleft` has item ids (`\pagenumber`, `\isodate`, `Printed on \isodate` …); `ecb_hdrcenter`, `ecb_hdrright` and `ecb_ftrcenter` have none and rely on text mapping. The `Printed on \isodate` id also differs from the mapping `Printed\ on\ \isodate` (escaped spaces). Only the visible "YYY" typos were fixed in the edits.
**Options:** make all four combos consistent (all ids or no ids); leave as is.
**Suggested:** remove the ids from `ecb_hdrleft` so all four combos work the same way, and test saving/loading a config.

#### s_startPageNum – "\resetpagenums -1" advice
**Issue:** `template.tex` already starts with `\pageno=-1`, so front matter is numbered with roman numerals by default; the tooltip's advice to add `\resetpagenums -1` to get roman numerals looks out of date. (A short note that the start number only applies while front matter uses roman numbering was added in the edits.)
**Options:** keep the paragraph; change it to "Front matter is numbered with roman numerals by default (i, ii, iii …). To use normal numbers there, add \resetpagenums 1 to the front matter."; remove it.
**Suggested:** rewrite as in option 2 after confirming in a test PDF.

### 09-pictures (5 items)

#### fcb_coordBorder (Add Maps dialog, "Border")
**Issue:** The readable name and tooltip were copied from the cover dialog (fixed in the edits file). But the combo starts greyed out (`sensitive=False`) and its value is not read anywhere in the code (`addAnotherMapClicked` doesn't use it). So it can never be used, and choosing a border would do nothing.
**Options:**
- Wire it up so that the chosen border is drawn around the map.
- Hide it until it works.
- Leave it greyed out and add "(not available yet)" to the tooltip.
**Suggested:** Hide it until it is wired up. A permanently greyed-out control confuses users.

#### c_mapSpread (Add Maps dialog, "Spread")
**Issue:** The setting is never read in the Python code, and it starts greyed out. Ticking it has no effect.
**Options:**
- Wire it up so the map is spread across two facing pages.
- Hide it.
**Suggested:** Hide it until spreads are supported, for the same reason as fcb_coordBorder.

#### c_imgMediaP, c_imgMediaA, c_imgMediaW (Select Images dialog)
**Issue:** These filter checkboxes are not read anywhere (picselect.py/gtkview.py only list them for view levels), so they don't filter the thumbnails.
**Options:**
- Make them filter the thumbnails by media type (P/A/W).
- Hide them.
- Add "(not working yet)" to their tooltips.
**Suggested:** Wire them up if that is cheap, otherwise hide them. Controls that do nothing get reported as bugs.

#### c_exclusiveFiguresFolder ("Exclude Subfolders")
**Issue:** The tooltip says only the named folder is searched. `build_searchlist(exclusive=...)` does respect this (view.py, gtkpiclist.py). But `getFigureSources` defaults to `exclusive=False` and runs `os.walk` on every folder in the search list, and runjob.py `gatherIllustrations` calls it without `exclusive`. So at print time subfolders may still be searched.
**Options:**
- Pass `exclusive` through to `getFigureSources` so the option works as the tooltip says.
- Change the tooltip to say it only affects the picture list/thumbnails.
**Suggested:** Fix the code (pass `exclusive` through). The tooltip describes the behaviour users expect.

#### textv_picNotes / its label "Notes About This Picture"
**Issue:** The label tooltip says the notes are "available and editable in ALL publications of this project". `PicChecks.savepic` saves the notes into `cfgProject` (the per-configuration picChecks.txt), not into the shared file. In `loadpic` there is also a comment "MH - this doesn't seem to be working".
**Options:**
- Save the notes in the shared picInfo/picChecks file so that the tooltip is true.
- Change the tooltip to "...saved with this configuration only".
**Suggested:** First check whether notes load at all (see the MH comment). Then decide where they belong. Shared notes are probably what users expect.

### 10-diglot (4 items)

Edits made in `edits/10-diglot.json`: merge-mode tooltip (`fcb_diglotMerge` incl. its entry child,
`l_diglotMergeMode`), `c_diglot` (Save As tip), grid column tooltips 1|2 / Code / Weight
(gtkpolyglot.py), `btn_adjust_diglot`, `b_print2ndDiglotText`.

#### `t_layout` (and its id-less "Layout:" label)
**Issue:** The tooltip says a forward slash `/` puts one text under another on the same page, but
`validate_layout()` rejects `/` ("Complex layouts are not yet supported") unless experimental flag 1
is set. The reviewer also suggested mentioning `-` for a blank page, but that is not safe either:
`all_letters` keeps the `-`, so Rule 1 ("Invalid codes used") rejects a layout containing `-` even
though Rule 10 lists it as allowed. So neither `/` nor `-` works for normal users today.
**Options:**
1. Remove the `/` sentence from both tooltips (describe letters + comma only).
2. Keep it but add "(experimental – not yet available)".
3. Fix `validate_layout()` so `-` works, then document `-`; leave `/` as experimental.
**Suggested:** 1 now (tooltip text: "Letters together share a page side by side; a comma starts
the facing page. Every code in the table above must be included."), plus 3 as a code fix later.
The tooltip should not advertise input that the validator rejects.

#### `c_diglotHeaders`
**Issue:** The checkbox is hidden (`no-show-all`) and `document/diglotheaders` (modelmap.py) is not
read anywhere in texmodel/template/TeX, so its tooltip promises behaviour that does not exist.
**Options:** remove the widget and config key; implement it; leave hidden as is.
**Suggested:** Leave hidden for now (users cannot see it), and remove it in a code clean-up unless
someone plans to implement it. No tooltip change needed while it is invisible.

#### Code bug: `view.py` `mergeCaptions()`
**Issue:** It reads `self.get("s_diglotSerialBooks", "FRT BAK GLO")`, but the widget is
`t_diglotSerialBooks`, so the user's Serial Books list is never used for picture-caption merging
(always the default). (Note: the result is also a substring test on a string, not a set lookup.)
**Options:** change to `t_diglotSerialBooks` and split into a set; leave.
**Suggested:** Fix the widget id and use `set(self.get("t_diglotSerialBooks", "").split())`
(as texmodel.py/runjob.py do).

#### Code bug: `gtkpolyglot.py` `onDiglotAutoAdjust()`
**Issue:** At the end it sets `self.isDiglotMeasuring = False` (on the PolyglotSetup object) instead
of `self.view.isDiglotMeasuring = False`. After one auto-adjust run the view flag stays True, so
the next click just re-activates the toggle and returns; the button does not work again until restart.
**Options:** fix the attribute; leave.
**Suggested:** Fix (`self.view.isDiglotMeasuring = False`) – one-line, clear bug.

### 11-tabsborders (6 items)

Edits made in `edits/11-tabsborders.json`: `r_sectHead_legacy`, `r_sectHead_dynamic`, `lb_style_vp`,
`r_thumbText_toc3` / `r_thumbText_zthumbtab` (spelling, readable names, stray `''`), `col_thumbback`,
Number of Tab Positions label (in `gr_thumbs`), `btn_resetTabGroups`, `c_thumbtabs`,
`l_inclSectionScale` / `l_verseDecoratorScale` ("1.0 is unity"), `fcb_sbBorderStyle` (name + new
tooltip), `fcb_sbBorderOrnament` (name), the eight `s_sbBoxPad*` / `s_sbBdrPad*` names, "sidebar" ->
"box" in the box-padding and padding-label tooltips, the two "All/Top (pt)" label tooltips (in
`fr_padding`), `lb_openOrnamentsCatalog`.

#### `lb_style_textborder` (code bug)
**Issue:** Its `clicked` handler `onOpenTextBorderDialog` calls `self.styleEditor.sidebarBorderDialog()`,
which does not exist anywhere (AttributeError). The link does not open anything; the tooltip
promises it does.
**Options:** connect it like the other style links (`activate-link` -> `onEditStyleClicked`, which
derives the marker `textborder` from the id) and keep `setPublishableTextBorder()`; or implement
`sidebarBorderDialog()` to open the Border Settings dialog directly.
**Suggested:** Make `onOpenTextBorderDialog` call `setPublishableTextBorder()` and then
`onEditStyleClicked(btn)` (open the `textborder` style on the Styles tab) – matches the tooltip and the
other links.

#### `r_border_page` / `lb_style_pageborder` (Page Border)
**Issue:** Both are `sensitive=False` in the glade file; the link has no signal handler; there is no
`\pageborder` style or TeX code for `fancy/pagebordertype=page`. The option appears to do nothing,
yet the radio is marked `active` in glade.
**Options:** implement it; hide both widgets; leave greyed out and add "(not implemented yet)" to the tooltip.
**Suggested:** Hide both until implemented (they are already insensitive, so users only see a
greyed-out promise). If kept visible, add "(not available yet)" to the tooltip.

#### `fcb_sbBorderOrnament` / `ls_coverBorder` item "c86out"
**Issue:** The list contains `c86out`; `src/standardborders.sty` defines `v86out` (and the cover
wizard uses `v86out`). Because the item text is also the stored id (`id-column` 0), choosing
`c86out` asks for a border that does not exist.
**Options:** rename the item to `v86out`; leave.
**Suggested:** Rename to `v86out` (glade `ls_coverBorder`). It is data as well as text, so not
done as an "obvious" edit; configs that saved `c86out` were already broken.

#### `fcb_rotateTabs` has no label of its own
**Issue:** It shares the "Length" label with the length spin button; nothing says what the combo is.
**Options:** add a label such as "Orientation:"; leave.
**Suggested:** Add "Orientation:" (layout change, so needs your OK).

#### `s_inclSectionShift` vs `s_verseDecoratorShift` sign convention
**Issue:** Section heading graphic: + moves down. Verse decorator: + moves up (per the tooltips,
which the reviewer found correct; not re-checked in TeX). The two controls on the same tab behave oppositely.
**Options:** make the code consistent (would change existing configs' meaning); leave and keep the tooltips.
**Suggested:** Leave the behaviour (changing it silently breaks existing settings); tooltips already
state the direction correctly.

#### `r_thumbText_toc3` / `r_thumbText_zthumbtab` greying-out
**Issue:** The tooltip says the \toc3 option is disabled when \toc3 is not in the ToC. In code,
`onTabsClicked` always greys both radios when `c_usetoc3` is off, but `onTocClicked` only does so when
`c_autoToC` is on (otherwise it re-enables them). Behaviour is inconsistent.
**Options:** make both handlers use the same rule; soften the tooltip ("may be disabled").
**Suggested:** Make the handlers consistent (code), then the tooltip is right as it stands.

### 12-styles (2 items)

Edits made in `edits/12-styles.json`: `s_sbiCutoutLines`, `fcb_sbi_posn_above`, `fcb_sbi_posn_beside`,
`fcb_sbi_posn_cutout` (new), `s_sbWidth` + `l_sbWidth`, `fcb_sbSize`, `fcb_styType`, `col_sb_backColor`,
`l_styFontSize`, `l_styLineSpacing`, `c_styFontScale`, `l_stySpaceAfter`, `fcb_sbiLayerOrder`,
`btn_styDel`, `btn_styReset`, `fcb_sbPgPos`, `s_sbLines` (name), `s_styNoteCallerRaise` (name), and new
tooltips for `btn_sbSizePosition`, `fcb_stytcVpos`, `btn_sbSelectFile`, `t_styMarker`.

Notes on review items that were not quite as described:
* `fcb_sbSize`, `fcb_styType`, `col_sb_backColor`: the "repeated text" was the label tooltip plus the
  widget tooltip shown together; each single tooltip was not duplicated. Small fixes were still made
  (single-column note added to the combo, stray blank line removed, missing article).
* `s_styFontSize`, `s_styLineSpacing`, `s_stySpaceAfter`: the text is on the labels
  (`l_styFontSize`, `l_styLineSpacing`, `l_stySpaceAfter`), so those were edited.

#### `t_sbiBgCropOfs` (Crop offset)
**Issue:** Tooltip says it is used when Oversize is set to Crop, but that list item is labelled
"Crop (unimplemented)". The control currently has no effect.
**Options:** add "(Crop is not implemented yet, so this has no effect.)"; hide the control (and the
Crop item) until Crop works; leave.
**Suggested:** Hide `t_sbiBgCropOfs` and its label while Crop is unimplemented, so users are not
offered a setting that does nothing. If hiding is not wanted, add the "not implemented yet" note.

#### Documentation: `docs/documentation/SideBars.md`
**Issue:** Still calls the publishable control "Hide/exclude contents of marker"; the UI now says
"Include Contents of Marker" (opposite sense).
**Options:** update SideBars.md; leave.
**Suggested:** Update the wording in SideBars.md (not a tooltip, so outside these edits).

### 15-peripherals (2 items)

#### c_autoToC – "ignored unless Multiple Books"
**Issue:** The outdated "run at least twice … leave OFF until the final run" note has been fixed in the edits file. The sentence "This option is ignored unless the 'Multiple Books' option has been set on the Basic tab" has been kept, because the code does not clearly support it. The ToC is generated whenever the option is on (template.tex: `\GenerateTOC`, and PTXprint's own contents page when there is no local front matter). `document/multibook` only controls whether unwanted `\toc1/2/3` lines are removed (texmodel.py, around line 1419).
**Options:**
- Remove the sentence.
- Reword it: "The \toc1/\toc2/\toc3 choices are only applied when Multiple Books is set."
- Change the code so that the ToC really is only made for multiple books.
**Suggested:** Reword it as in option 2. This matches the code without changing behaviour.

#### c_inclFrontMatter, c_inclBackMatter – "in alphabetical order"
**Issue:** Both tooltips say multiple PDFs "will appear in alphabetical order". `_onPDFClicked` stores the files in the order the GTK file chooser returns them, and `modelmap.py` writes `\includepdf` lines in that same order. There is no sorting. The chooser's order may be alphabetical on some platforms, but the code doesn't guarantee it.
**Options:**
- Sort the list in `_onPDFClicked` (e.g. `sorted(vals)`) so that the tooltip is true.
- Remove "in alphabetical order" from both tooltips.
**Suggested:** Sort in code. It's a one-line change and makes the order predictable, which is what the tooltip promises.

### 16-publications (1 item)

#### tv_publications (publications list)
**Issue:** The list has no general tooltip, so users may not know that names, books and values can be edited by clicking them. But the tree view already uses `tooltip-column` 9 for per-row tooltips: books that cannot be understood are shown in red, with an explanation. If a `tooltip-text` property is added as well, GTK may show the general text instead of, or as well as, the per-row explanation. That needs testing, so it isn't a safe text-only edit.
**Options:**
- Add the hint to the visible intro label (`l_pubIntro`) instead, e.g. "Click a publication name, its books, or a field value to change it. Books shown in red cannot be understood – hold the mouse over them to see why."
- Add a `tooltip-text` to `tv_publications` and test that the red-book tooltips still appear.
- Set a fallback tooltip in publications.py for rows with no problem (column 9 empty).
**Suggested:** Option 1 (extend `l_pubIntro`). It is always visible and cannot interfere with the per-row tooltips.

### 17-finishing (4 items)

#### c_coverSeparatePDF
**Issue:** The tooltip says the option "is only available if Create Cover is enabled on the Cover tab". The control is hidden (`no-show-all`, insensitive), and no code reads `cover/makeseparatePDF` (only modelmap.py maps it). The cover is always split out as `_cover.pdf` when a cover is made, whatever this box says.
**Options:**
- Make the code use the setting (only split the cover when ticked).
- Leave it hidden and reword the tooltip: "When a cover is made, it is saved as a separate PDF (_cover.pdf)."
- Remove the control and the config key.
**Suggested:** Remove it (or leave it hidden). It is invisible and does nothing, and the cover is always split out, which is the behaviour people want. Changing the tooltip of a hidden control does not help anyone.

#### fcb_outputFormat – Digital-CMYK (Transparency) does no CMYK conversion (code)
**Issue:** `pdf/procpdf.py` `_pdfmodes['cmyk'] = ("CMYK", "Transparency")`, but the combo ID for Digital-CMYK is `"Transparent"`. So `colour` becomes `"transparent"`, and `fixpdffile()` (fixcol.py) only handles `cmyk`, `rgbx4`, `spot` and `gray`. It looks as if no CMYK conversion happens for Digital-CMYK. (runjob.py has its own `_pdfmodes` too – check it as well.)
**Options:**
- Change `"Transparency"` to `"Transparent"` in `_pdfmodes`.
- Leave as is if Digital-CMYK is meant to keep RGB.
**Suggested:** Fix the key to `"Transparent"`. The new combo tooltip (in the edits) says "CMYK with transparency", which is only true after this fix.

#### fcb_outputFormat – ICC colour count for Screen/Digital (code)
**Issue:** In `snippets.py` `PDFx1aOutput`, `_iccnumcols` is set to "3" for Screen/Digital, but the next `if pdftype == "Gray": … else: "4"` overwrites it with "4" for every non-Gray format, including the sRGB ones.
**Options:** Change the second `if` to `elif`; or leave as is.
**Suggested:** Change to `elif`. An sRGB ICC profile with `/N 4` is wrong and can make PDF/X-4 checks fail.

#### col_ndiffColor / col_odiffColor – colours may be swapped (code)
**Issue:** `runjob.py` (about line 868) calls `createDiff(..., color=odiffcolor, ..., oldcolor=ndiffcolor, ...)`. The names look swapped. The defaults in pdfdiff.py are red for `color`, blue for `oldcolor`; the UI defaults are blue for new and red for old.
**Options:** Swap the arguments; or confirm by making a test diff and leave as is.
**Suggested:** Make a quick test diff (add a word) and check that the added text shows in the "Show New Text" colour. Swap the arguments if it does not.

### 19-preview (3 items)

#### s_pdfZoomLevel / a_pdfZoomLevel
**Issue:** The spin range (adjustment `a_pdfZoomLevel`) is 10–1000, but `pdf_viewer.py` `onZoomLevelChanged` clamps the zoom to 10–800 (and `on_zoom_in` caps at 8.0). Typing 900 shows 900 but zooms to 800.
**Options:**
- Change the adjustment `upper` to 800.
- Change the clamp to 1000.
**Suggested:** Set the adjustment upper limit to 800 – matches the zoom-in cap already in the code; a one-property glade change.

#### Page Filler window "Start Fill" (bookProgressDlg.py `start_tip`)
**Issue:** The reviewer wants the tooltip to warn that existing adjustments (including manual ones) are discarded. I could not confirm this. In `page_filler.py`, a non-resumed run uses the current paragraph settings as its starting point (`self.base_params = dict(state.paragraph_params)`), which suggests existing AdjList entries are kept as the start, not cleared.
**Options:**
- Leave the tooltip as is.
- Add a sentence once the behaviour is confirmed (e.g. "Starts from the current adjustments" or "Existing adjustments are replaced").
**Suggested:** Ask the developer (MH) what Start Fill does with existing/manual adjustments, then add one sentence saying so. Users need to know if manual work can be lost.

#### btn_prvAutoFill / icon_prvAutoFill2 – feature name (tooltips already edited; confirm the name)
**Issue:** Three names for one thing: "Page Fill tool", "Auto Page Fill dialog", window title "PTXprint: Page Filler"; the Advanced group is "Automatic Page Filler". The edits make both tooltips say "Page Filler" (the window title).
**Options:** Keep "Page Filler" (as edited); or use "Automatic Page Filler" everywhere (window title too).
**Suggested:** Keep "Page Filler" for now (matches what the user sees in the window title). If the lead prefers "Automatic Page Filler", change the window title and the two tooltips together.

### 20-import (10 items)

Edits made (see `edits/20-import.json`): `l_tgtProject`, `l_tgtConfig` (the wrong "from which"
paragraphs the review listed under `ecb_targetProject` / `ecb_targetConfig` are on these labels),
`t_targetConfig`, `r_impTarget_prjcfg` (readable name), `btn_resetConfig`, Layout tab text
(`tb_impLayout`), and new tooltips for `c_impPictures`, `c_impLayout`, `c_impStyles`, `c_impOther`,
`c_impEverything`, `c_oth_Body`, `c_oth_NotesRefs`, `c_oth_HeaderFooter`, `c_oth_Cover`, `c_oth_Texpert`.

#### c_oth_Variables (checkbox does nothing)

**Issue:** `importConfig` (view.py ~2426) checks `self.get("c_impVariables", False)`, which is not a
widget. Ticking **Variables + Meta Data** has no effect; variables are only imported by Everything, or
(missing ones only) by Front +Back Matter.

**Options:**
- Change to `self.get("c_oth_Variables")`, and only when `c_impOther` is ticked (like the other `c_oth_` boxes).
- Remove the checkbox.

**Suggested:** Fix the ID and respect `c_impOther`. Then add a tooltip ("Import the variables from the
Peripherals tab and the publication meta data.") – none was added now because it would describe a
feature that does not work.

#### c_impFontsScript (typo excludes style fonts) and its tab text

**Issue:** view.py ~2448: `exclfields = None if impAll or self.get("c_impFontsScripts") else (...)` –
the extra "s" means style font fields are always excluded unless Everything is ticked. The tab text
says "It will not alter any fonts that have been directly set within Styles", which matches today's
(buggy) behaviour, not the intended one. The tab text also says it imports "hyphenation", but
hyphenation entries are category `body` (Other > Body Tab settings).

**Options:**
- Fix the typo; then rewrite the tab text: fonts in styles *are* updated when Fonts+Script is ticked; hyphenation is under Other > Body.
- Keep the behaviour (never touch style fonts unless Everything) and remove the dead condition; only fix the "hyphenation" part of the text.

**Suggested:** Decide the intended behaviour first, then fix code and text together. No tooltip was added
to `c_impFontsScript` for the same reason. Hyphenation wording, e.g. "...the major font and script
settings and spacing. (Hyphenation is imported with Other > Body Tab settings.)"

#### c_oth_OverwriteFrtMatter (checkbox has no effect)

**Issue:** view.py ~2590 reads `self.get("c_oth_OverwriteFrontMatter")`; the widget is
`c_oth_OverwriteFrtMatter`. The checkbox has no effect.

**Options:** Fix the ID in view.py; or remove the checkbox.

**Suggested:** Fix the ID (one-word change). Then add a tooltip ("Replace the front matter in the target
with the source's, instead of only adding missing parts.").

#### c_oth_ThumbTabs (no thumb tab settings imported)

**Issue:** `ImportCategories` (modelmap.py ~546) maps it to `'thumbtabs'`, but the thumb tab ModelMap
entries use category `'tabsborders'`. Nothing is imported.

**Options:**
- Change `ImportCategories['c_oth_ThumbTabs']` to `'tabsborders'` (check that nothing else in `tabsborders` should be excluded – decorations are category `decorate`).
- Change the ModelMap category of the `thumbtabs/*` entries to `'thumbtabs'`.

**Suggested:** Change `ImportCategories` to `'tabsborders'` – smallest change. Add a tooltip after.

#### c_oth_customScript (not used) and c_oth_Advanced tooltip

**Issue:** `c_oth_customScript` is not read in `importConfig`; the custom script is imported under
`c_oth_Advanced` (when the source has `processscript`). The `c_oth_Advanced` tooltip says it excludes
"Custom Script processing", which is the opposite of what the code does.

**Options:**
- Make the custom-script block depend on `c_oth_customScript` instead of `c_oth_Advanced` (tooltips then correct).
- Remove `c_oth_customScript` and change the Advanced tooltip to say it includes the custom script.

**Suggested:** Wire the script part to `c_oth_customScript` – the UI already promises it.

#### c_impEverything – tab text "automatically enabled when the target ... does not already exist"

**Issue:** The code only forces Everything for an external-folder target (`# FIX ME` in
`setImportButtonOKsensitivity`). A new target config starts from defaults, so without Everything most
settings stay at default.

**Options:**
- Implement: tick Everything when the target project/config does not exist yet.
- Change the text to "...when exporting to an external folder of settings."

**Suggested:** Implement it – importing into a new config with only some groups gives a confusing
half-default result. If not, change the text.

#### c_impEverything – `_sensitivities` entry (inverted)

**Issue:** `_sensitivities["c_impEverything"]` (gtkview.py ~667) makes the five category boxes sensitive
only when Everything is ticked – the opposite of the real behaviour. It is overridden by
`setImportButtonOKsensitivity`, but it is misleading (generated docs say "Only available when
Everything is selected").

**Options:** Move it to `_nonsensitivities`; or remove it.

**Suggested:** Move to `_nonsensitivities` so the declared logic matches what the user sees.

#### c_impStyles – tab text "also import styles from ptxprint-mods.sty"

**Issue:** In `importConfig`, ptxprint-mods.sty is only merged with Advanced settings or Everything, not
with Styles.

**Options:**
- Also merge ptxprint-mods.sty when Styles is ticked.
- Change the text: "Styles from ptxprint-mods.sty are imported with Other > Advanced settings."

**Suggested:** Change the text (the code grouping with Advanced is deliberate – mods files are advanced).

#### ecb_targetProject – "Enter a NEW project name" creates a temporary project

**Issue:** `_getProject` returns None for an unknown name, and `importConfig` then fails on
`tgtPrj.guid`. Typing a new project name crashes the import.

**Options:**
- Implement creating the (temporary) project.
- Remove the "OR Enter a NEW project name..." part of the tooltip and block OK when the project does not exist.

**Suggested:** Remove the claim from the tooltip and disable OK for an unknown project (in
`setImportButtonOKsensitivity`); creating projects from the Import dialog is out of scope.

#### Pictures sub-options (r_impPics_*, c_pic_*, c_impPicsAddNew, c_impPicsDelOld)

**Issue:** These have no tooltips either. They were not in the review's range and need care about
merge semantics.

**Options:** Add tooltips based on the manual text (chapter 20); or leave.

**Suggested:** Add later, using the manual wording for `c_impPicsAddNew` / `c_impPicsDelOld`.

### 21-help (5 items)

Edits made (see `edits/21-help.json`): `l_projects_dir`, `btn_generateReport` (spelling),
`lb_masterSlides` (wording), `l_techFAQ`, `btn_createZipArchiveXtra` (says the job is printed again
first), `btn_deleteTempFiles`.

#### lb_masterSlides (never shown)

**Issue:** The Training Presentation link is in `_ui_keepHidden` and is not in the list that
`noInternetClicked()` shows/hides, so it is never visible (the tooltip spelling was still fixed).

**Options:**
- Add it to the `noInternetClicked()` list (shown when Internet use is allowed) and remove it from `_ui_keepHidden`.
- Leave it hidden (or remove it) if the slides are no longer maintained.

**Suggested:** Ask whether https://tiny.cc/ptxslides is still current; if yes, add it to the
`noInternetClicked()` list like the other links.

#### l_reportBugs (tooltip content)

**Issue:** The tooltip talks about Python, PyGTK, Glade and XeTeX, which does not help users. It is a
style/content choice, not an error.

**Options:**
- Replace with: "Found a bug? If you have a GitHub account, report it here.\nOtherwise email ptxprint_support@sil.org."
- Keep the current text.

**Suggested:** Replace – shorter and gives a route for users without GitHub.

#### btn_createZipArchiveXtra (more advice; tooltip overwritten at run time)

**Issue:** The reviewer also suggested saying that fonts, pictures and text are included and to select
only the book(s) with the problem. Only the "printed again first" fact was added. Also note:
`onCreateZipArchiveClicked` replaces the whole tooltip with the archive file path after the first use,
so the help text disappears for the rest of the session.

**Options:**
- Extend the tooltip with "Keep it small: select only the book(s) with the problem".
- Stop overwriting the tooltip in code (show the path in the status line instead, which already happens via `startfile`).

**Suggested:** Stop overwriting the tooltip in code; optionally add the "select only the book(s)" hint.

#### l_ptxprintdir, l_techFAQ, lb_ornaments_cat, lb_tech_ref (view level)

**Issue:** The UI map lists these for Default and Full views, but `noInternetClicked()` shows them
only when `uilevel >= 6` (Full). The manual follows the code.

**Options:** Change the UI map to Full only; or change the code to `uilevel >= 5`.

**Suggested:** Show the Ornaments Catalog and Technical Reference from Default (5) up – they are useful
reference documents and are local files (no Internet needed); keep folder paths Full-only.

#### tb_Logging / tv_logging (Log tab never shown)

**Issue:** The Log tab is in `_ui_keepHidden` and is never shown.

**Options:** Remove it from the glade file and code; or add a way to show it (e.g. Full view only).

**Suggested:** Remove it unless a developer still uses it – dead UI adds translation and maintenance cost.

---

### Appendix: review items dropped as not real problems

#### 02-main-window

- `c_quickRun` "glade active=True is never seen": not user-visible; the value is always set from the
  user preference at start-up. No change needed (the spelling fix was made).

#### 03-basic

- `ecb_savedConfig` "last sentence repeats the first": the combo's current tooltip has only one sentence.
  The "Alternatively, select a previously-saved…" text is on the `l_cfgName` label, where it is not a
  repeat. The other part of the issue (unsaved changes warning) was made as an edit.
- `lb_openBible` "last paragraph belongs to the Step 1 label": the current tooltip does not contain that
  paragraph; it is already only on the Step 1 label.

#### 04-layout

- `s_gridMinorDivisions`: the widgets already have distinct `name` descriptions ("Grid: Minor line color",
  "Grid: Minor line thickness", "Grid: Number of minor divisions"). The repeated "Minor Divisions" label is
  an extractor/manual issue, not a UI text problem.
- `s_headerposition`: the "merged" tooltip is the extractor joining the spin button and `l_headerposition`
  tooltips. Each widget's own text is fine. The "the the" typo in `l_headerposition` is fixed in the edits.
- `c_noGrid`: same as above. The switch and the `l_gridAligned` label have separate tooltips; the
  duplication only happens in the extractor.
- `c_noteLines` (section name): the tooltip already names "'Page Layout and Spacing' section of the
  Advanced > Other tab". Only the split "Wide-/Margin" was fixed.
- `s_indentUnit` (rewrite): only the wrong default was fixed (1 → 0.8). The halving/doubling on
  1↔2 columns is already explained in the `l_indentUnit` tooltip.


#### s_indentUnit (moved here from the edits during review)
**Issue:** The tooltip says "(default=1, min=0, max=4)". The glade adjustment default is 0.8, but modelmap.py falls back to "1.0", and 0.8 is really the two-column value, so it is not clear which number to quote.
**Options:** (a) say 0.8; (b) say 1.0; (c) remove the default from the tooltip.
**Suggested:** (c) – the default depends on the layout, so leave it out.

#### 05-fonts

- `fcb_fontdigits`: not a UI text problem. The real list is filled at run time (`_alldigits`), and only the
  generated manual shows the 4 placeholder entries from the glade list store.
- `c_hyphenLimitBooks`: the "63929 words" figure matches `Hyphenation.listlimit = 63929`.
- `bl_fontExtraR`: the button has a single sentence. The near-duplicate comes from the `l_fallbackFont`
  label tooltip, which the extractor merged.
- `fcb_fontFaces`: instead of moving the text, a tooltip with the "not installed For all Users" hint was
  added to `tv_fontFamily`. The "Typeface:" label keeps its tooltip, which is harmless. (fcb_fontFaces
  itself has no tooltip.)

#### 06-body

- `c_pageNumTitlePage`: covered in the 08-headfoot review file.

#### 07-notes

* `c_fnautocallers`, `c_xrautocallers` – the reviewer said the Override checkbox is not above these controls, but in the grid `c_fnOverride`/`c_xrOverride` are at row 3 and the callers box at row 4, i.e. directly above. Not a problem.
* `s_fnAboveSpace`, `s_xrAboveSpace` "two texts joined" – each widget has a single text; the second text is the tooltip of the neighbouring label (`l_text2NotesSpace1` etc.). Only the study-note copies named the wrong rule – fixed in edits.
* `s_ef_colgutterfactor`, `s_ef_bottomRag`, `s_ef_colgutteroffset` "same text twice" – again the spin button and its label each have one tooltip; not a duplicate. (`s_ef_colgutteroffset` was reflowed in the edits because it was one very long line.)
* `fcb_strongsNdxBookId` "tooltip repeated twice" – the second copy is on its label; only the "bookx" typo needed fixing (done).
* `lb_style_li+strong-s` – its tooltip is only "Click to select this marker on the Styles tab."; the "Select which components…" line belongs to the neighbouring label. Not a problem.
* `fcb_fnHorizPosn` etc. – the wrong "vertical space" tooltip was actually on the "Rule Positioning and Parameters" labels (`l_fnRulePosParms`, `l_snRulePosParms`, unnamed label in `gr_xrRulePosParms`); fixed there, and new tooltips added to the three combos.

#### 08-headfoot

* `ecb_ftrcenter` "tooltip text appears twice (label + widget versions differ)" – the label `l_ftrcenter` and the combo each have their own tooltip; the shorter label version is not wrong. Only the date typo needed fixing (done; mods.tex sentence is a decision above).

#### 09-pictures

- `t_imageTypeOrder` "whole tooltip duplicated": not actually a problem. The glade file holds two different texts, one on the "Image Types:" label and one on the entry. Each is shown on its own when you hover over that widget. The manual extractor joined them into one.
- `fcb_plSize` "text duplicated": same cause. The label and the combo each have their own tooltip, and the extractor joined them.
- `t_picXetex` "text duplicated": same cause (label + entry). The real problems, the 'Mulitple' spelling and 'multipage' vs 'multi-page', are fixed in the edits file.
- `t_plCreditText` "text duplicated": same cause (label + entry). The 'David C. Cook' vs 'David C Cook' mismatch is fixed in the label, to match what the `dcc` shortcut inserts.
- `fcb_plPgPos` "lines run together": not a problem in the glade file, where each position is already on its own line. Only the extractor joined them. The missing "Below Notes" line is added in the edits file.
- `fcb_plMirror` "lines run together": same cause. The glade file already has one line per choice.

#### 10-diglot

* `t_newMonoglotConfigName` – reviewer says no change needed; tooltip already mentions parentheses, which the code allows.
* Reviewer's "double spaces" in the merge-mode tooltip – these are the indentation of a wrapped bullet line, not a typo (the grammar part was fixed).

#### 11-tabsborders

* `s_sbBorderWidth` – reviewer found nothing wrong.
* `col_thumbback` "same idea twice" – the label and the button had different tooltips (the review joined them); the button's own text was still reworded for clarity.

#### 12-styles

* None.

#### 15-peripherals

(none)

#### 16-publications

- `btn_pubPrint` "not shown in the preview": not added. The other points (saves the config first, prints in the background, opens the folder when finished) were confirmed in publications.py and are in the edits file. That the PDFs aren't shown in the preview is implied by "in the background" and the folder opening.

#### 17-finishing

- `col_ndiffColor`, `col_odiffColor` "first sentence repeated": not actually a problem. The extractor joined the label tooltip (general sentence + specific sentence) with the colour button tooltip. Each tooltip on its own is fine.

(`s_diffpages`, `s_keepVersions` and `s_foldCutMargin` are handled in the edits: the duplicated text came from the extractor joining label and widget tooltips; the wrong text on `l_diffpages` was replaced, and the spin tooltips were adjusted.)

#### 18-printers

- (none)

#### 19-preview

- (none – `btn_findButton` and `l_pdfPgCount` were handled in the edits; the "(15)+52 on btn_page_first" note was only an extractor artefact.)

#### 21-help

- `lb_giveFeeback` misspelled ID: not user-visible; renaming the ID needs matching code changes
  (gtkview.py lists) for no user benefit.
