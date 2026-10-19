# Importing settings

## What this dialog is for

The **Import Settings** dialog copies settings from somewhere else into a configuration. Use it when:

* you have a PDF that PTXprint made earlier, and you want the same layout again (for example, the settings were lost, or the PDF came from another person),
* someone sent you a PTXprint ZIP archive,
* another project or configuration has settings that you want to reuse – all of them, or only some groups (for example only the pictures, or only the header and footer).

You can also use it to **extract** the settings from a PDF or ZIP into a normal folder, so that you can look at them.

To open the dialog: on the **Basic** tab, in the **Layout Configuration** area, click **Import Settings...**. (This button is not shown in the **Mini** view.)

The dialog has three parts: **Source of Settings** (where the settings come from), **Target** (where they go), and a row of **category tabs** (what to bring in).

## Source of Settings

Choose one of two sources:

* **PDF file (with embedded settings) or ZIP archive file** – click **Select...** and choose the file.
  * A **PDF** only works if it was made by PTXprint with **Include Config Settings Within PDF** turned on (on the **Finishing** tab). Otherwise PTXprint says that it cannot find any settings in the file.
  * A **ZIP archive** is the kind of file that PTXprint makes with **Create Archive...** on the **Help** tab.
* **A Previously Saved Configuration** – choose the **Project** and then the **Configuration** to copy from. Settings are read from the saved files, so if the source is the configuration that is open now, click **Save** first.

## Target

Choose where the settings go:

* **A New/Existing Project and/or Configuration** – this is the usual choice. PTXprint fills in the current project and configuration. You can choose another existing project. You can choose another configuration, or type a **new** configuration name. A new configuration starts with the PTXprint default settings, and then the imported settings are added.
* **An External Folder of Settings** – click **Select...** and choose a folder. PTXprint copies **all** the settings files from the source into that folder. Nothing in your projects is changed. When this target is chosen, **Everything** is turned on and the category tabs are greyed out.

The **OK** button stays greyed out until the choices are complete: a file or a source configuration, a target folder or a target configuration, and at least one category ticked. It is also greyed out when the source and the target are the same configuration.

## What to import: the category tabs

Each tab has a check box in its label. Tick the box to import that group. Click the tab to see its options.

* **Pictures** – the picture settings and the picture list.
* **Layout** – the page and column layout.
* **Fonts+Script** – fonts and writing-system settings.
* **Styles** – the style settings from the **Styles** tab.
* **Other** – a list of other groups that you choose one by one.
* **Everything** – all settings. (Only shown in the **Default** and **Full** views.)

When **Everything** is ticked, PTXprint imports everything, no matter which other boxes are ticked or not ticked. Untick **Everything** if you want only some groups.

### What each category brings in

| Category | What is imported |
|---|---|
| **Pictures** | The general settings of the **Pictures** tab (include pictures, picture folder, resolution, captions shown, placeholders…) and the picture list. With **Import Entire PicList "as is"** the whole list is replaced. With **Import Elements of PicList** only the parts you tick are copied for each picture. |
| **Layout** | Page size, margins (top, bottom, side), mirror pages and binding gutter, number of columns and column gutter, vertical rule between columns, line spacing, note lines, margin notes, and related settings. It does **not** bring the font size (that is in **Fonts+Script**) or the header and footer (that is in **Other** › **Header+Footer settings**). |
| **Fonts+Script** | The main fonts (regular, bold, italic, bold italic, extra), the font size, the fallback font, text direction, script and line-breaking settings, word and letter spacing, coloured text, and script-specific options. Fonts that are set inside individual styles are not changed. |
| **Styles** | The style settings from the source (the **Styles** tab). Normally only styles that you have **not** changed in the target are updated. Tick **Override ALL Style Settings** to update all styles. |
| **Other** | Only the groups that you tick on the **Other** tab (see below). |
| **Everything** | All settings in the source configuration, including the book list, copyright text, diglot and Strong's settings, the whole picture list, styles, front matter, cover, and the special files from the **Advanced** tab. |

### The Other tab

* **Body Tab settings** – the settings on the **Body** tab, including hyphenation, chapter and verse numbers, section headings, and glossary markup.
* **Notes+Refs settings** – footnotes, cross-references and study notes.
* **Header+Footer settings** – the content and position of the header and footer.
* **Thumb Tabs settings** – the thumb tab settings from the **Tabs+Borders** tab.
* **Advanced settings** – the options on the **Advanced** tab, and the special files that go with them (changes file, extra TeX files, extra style file, and a custom script if the source uses one).
* **Cover settings** – the cover settings, cover styles and cover pages.
* **Front +Back Matter** – most settings of the **Peripherals** tab (front and back PDFs, table of contents, front matter, section introductions), the front matter text, and any variables that the target does not have yet.
* **Overwrite Front Matter** – (only available when **Front +Back Matter** or **Cover settings** is ticked) replace the existing front matter in the target, not only add missing parts.
* **Custom Script** – the custom script processing set on the **Advanced** tab. Greyed out when the source is a PDF, because a PDF does not contain the script.
* **Borders + Decorations** – page borders, section-heading decorations, end-of-book and verse-number decorations. (Default and Full views.)
* **Variables + Meta Data** – the variables from the **Peripherals** tab and other information about the publication. (Default and Full views.)
* **Texpert Hacks** – the expert TeX settings on the **Advanced** tab. (Default and Full views.)
* **Finishing settings** – everything on the **Finishing** tab: PDF output format, watermark, crop marks, grid, pages per sheet, compare-PDF settings and similar. (Default and Full views.)

### What happens when you click OK

1. PTXprint reads the settings from the source.
2. It changes only the groups you ticked, in the target configuration.
3. It **saves** the target configuration at once.
4. It opens the target project and configuration, and shows a message such as "Imported Settings into: ABC::NT_A5".

There is no Undo. If you are not sure, import into a **new** configuration name first, and check the result there.

## RESET

The **RESET** button at the bottom of the dialog sets all settings of the **current** configuration back to the PTXprint defaults. It does not reset the style settings. The dialog stays open, and nothing is saved until you click **Save** or **Print (Make PDF)** (or until an import saves the configuration). Use it when you want the target to have only the imported settings, for example before you import styles.

## Common tasks

### Get back the settings that were used for a PDF

1. On the **Basic** tab, click **Import Settings...**.
2. Click **PDF file (with embedded settings) or ZIP archive file**, then **Select...**, and choose the PDF.
3. Under **Target**, click **A New/Existing Project and/or Configuration**. In **Configuration**, type a new name, for example `FromPDF`.
4. Tick **Everything** (change to the **Default** view if you cannot see it).
5. Click **OK**. PTXprint opens the new configuration with the settings from the PDF.

### Copy only the pictures from another configuration

1. Click **Import Settings...**.
2. Click **A Previously Saved Configuration** and choose the source **Project** and **Configuration**.
3. Check that the **Target** is the configuration you want.
4. Untick **Everything**, **Layout**, **Fonts+Script**, **Styles** and **Other**. Tick **Pictures**.
5. On the **Pictures** tab, choose **Import Entire PicList "as is"**, or choose **Import Elements of PicList** and tick only what you want (for example **Size, Position, Mirror, Rotation settings**).
6. Click **OK**.

### Copy the header and footer from another configuration

1. Click **Import Settings...** and choose the source configuration.
2. Untick **Everything** and all other categories, and tick **Other**.
3. On the **Other** tab, untick everything except **Header+Footer settings**.
4. Click **OK**.

### Look at the settings inside a PDF or ZIP without changing anything

1. Click **Import Settings...** and choose the PDF or ZIP file as the source.
2. Under **Target**, click **An External Folder of Settings**, then **Select...**, and choose an empty folder.
3. Click **OK**. The settings files are copied into that folder.

### Start a configuration again from defaults, then import styles

1. Open the configuration on the **Basic** tab.
2. Click **Import Settings...**, then **RESET**.
3. Choose the source, untick **Everything**, and tick **Styles** (and other groups you need).
4. Click **OK**.

## Common problems

### "Cannot find any settings to import from the selected file"

**Cause:** The PDF was made without **Include Config Settings Within PDF** (on the **Finishing** tab), or with a very old PTXprint version (before 2.3). **What to do:** Use another source, for example a ZIP archive made with **Create Archive...** on the **Help** tab.

### The OK button is greyed out

**Cause:** Something is missing: no file selected, no target folder, no target configuration, no category ticked – or the source and target are the same configuration. **What to do:** Check each part of the dialog.

### Everything was imported, but I ticked only one category

**Cause:** **Everything** was still ticked. In the **Basic** view the **Everything** tab is hidden, but it is still ticked (it is ticked by default). **What to do:** Change to the **Default** view (**☰** › **View Level** › **Default View**) and untick **Everything**.

### The styles did not change

**Cause:** Without **Override ALL Style Settings**, PTXprint only updates styles that are still unchanged in the target. **What to do:** Tick **Override ALL Style Settings**, or click **RESET** before you import.

### The font size did not change when I imported Layout

**Cause:** The font size belongs to **Fonts+Script**, not **Layout**. **What to do:** Tick **Fonts+Script** too.

### The header and footer did not change when I imported Layout

**Cause:** The header and footer belong to **Other** › **Header+Footer settings**. **What to do:** Tick **Other** and **Header+Footer settings**.

### Custom Script is greyed out

**Cause:** The source is a PDF. A PDF does not contain the custom script. **What to do:** Import from a ZIP archive or a saved configuration instead.

### Some options on the Other tab seem to have no effect

**Cause:** In the current version, **Thumb Tabs settings**, **Overwrite Front Matter**, **Variables + Meta Data** and **Custom Script** may not bring in their settings when they are used on their own. **What to do:** After importing, check the **Tabs+Borders**, **Peripherals** and **Advanced** tabs. If something is missing, import into a new configuration with **Everything** ticked, or set those few settings by hand.

## Settings reference: Importing settings

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Import Settings... (dialog)

#### RESET

- **Where:** Import Settings... (dialog)
- **Type:** Button
- **Description:** Reset the current Configuration's UI settings
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Warning! This will reset ALL the UI settings for the CURRENT configuration to their default values.
>
> Note that it will NOT reset the Style settings stored in the .sty files.
>
> The reset is not saved until you next save, print, or import with OK.

**Explanation:**

Sets every setting of the configuration that is open now back to the PTXprint defaults, at once and without asking. Style settings are not reset. The change is not saved until you click **Save**, **Print (Make PDF)**, or **OK** to import.

*(Internal ID: `btn_resetConfig`)*

#### OK

- **Where:** Import Settings... (dialog)
- **Type:** Button
- **View level:** Basic, Default and Full views

**Explanation:**

Imports the ticked groups into the target, saves the target configuration, and opens it. With an external folder as target, it copies the settings files into the folder instead. Greyed out until the choices are complete. Shortcut: **Alt+Enter**.

*(Internal ID: `btn_importSettingsOK`)*

#### Cancel

- **Where:** Import Settings... (dialog)
- **Type:** Button
- **View level:** Basic, Default and Full views

**Explanation:**

Closes the dialog without importing. (Changes made with **RESET** stay on the screen.) Shortcut: **Ctrl+W**.

*(Internal ID: `btn_importCancel`)*

#### Pictures

- **Where:** Import Settings... (dialog)
- **Type:** Checkbox (ticked by default)
- **Description:** Import Picture Settings
- **View level:** Basic, Default and Full views
- **Only available when:** “Everything” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Import the picture settings and the picture list. Use the Pictures tab of this dialog to choose how the picture list is combined.

**Explanation:**

Imports the general picture settings (from the **Pictures** tab) and the picture list. The options on the **Pictures** tab of this dialog control how the picture list is combined. When you tick or untick this box, the **Pictures** tab of the dialog opens.

*(Internal ID: `c_impPictures`)*

#### Layout

- **Where:** Import Settings... (dialog)
- **Type:** Checkbox (ticked by default)
- **Description:** Import Layout Settings
- **View level:** Basic, Default and Full views
- **Only available when:** “Everything” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Import page size, margins, columns, line spacing and related settings.

**Explanation:**

Imports the page layout: page size, margins, gutters, columns, line spacing and similar. It does not import font size, fonts, or the header and footer. The text on the **Layout** tab of the dialog also mentions the header and footer, but they are imported with **Other** › **Header+Footer settings**.

*(Internal ID: `c_impLayout`)*

#### Fonts+Script

- **Where:** Import Settings... (dialog)
- **Type:** Checkbox (ticked by default)
- **Description:** Import Fonts and Script Settings
- **View level:** Basic, Default and Full views
- **Only available when:** “Everything” is selected

**Explanation:**

Imports the main fonts, the font size, and the writing-system settings (text direction, script, line breaking, spacing, fallback font, coloured text). Fonts that are set inside individual styles are not changed. Hyphenation settings are imported with **Other** › **Body Tab settings**, not here.

*(Internal ID: `c_impFontsScript`)*

#### Styles

- **Where:** Import Settings... (dialog)
- **Type:** Checkbox (ticked by default)
- **Description:** Import Styles Settings
- **View level:** Basic, Default and Full views
- **Only available when:** “Everything” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Import the style settings (Styles tab), merged into the target configuration.

**Explanation:**

Imports the style settings (the **Styles** tab) by merging them into the target. Only styles that are unchanged in the target are updated, unless **Override ALL Style Settings** is ticked. Font names and font features inside styles are only imported when **Everything** is ticked.

*(Internal ID: `c_impStyles`)*

#### Other

- **Where:** Import Settings... (dialog)
- **Type:** Checkbox (ticked by default)
- **Description:** Import Other Settings
- **View level:** Basic, Default and Full views
- **Only available when:** “Everything” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Use the Other tab of this dialog to choose more groups of settings. If this is not ticked, none of the boxes on the Other tab are used.

**Explanation:**

Turns on the **Other** tab, where you choose more groups one by one (Body, Notes+Refs, Header+Footer, Advanced, Cover, Front +Back Matter, Finishing…). If this box is not ticked, none of the boxes on the **Other** tab are used.

*(Internal ID: `c_impOther`)*

#### Everything

- **Where:** Import Settings... (dialog)
- **Type:** Checkbox (ticked by default)
- **Description:** Import All Settings
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Import all settings and files of the source configuration, whatever the other boxes say.

**Explanation:**

Imports all settings and files of the source configuration, whatever the other boxes say. Use it to recreate a configuration from a PDF or ZIP, or to make a full copy. It is ticked by default, and PTXprint ticks it again when you open the dialog with no category ticked. It is also turned on automatically when the target is an external folder. Only shown in the **Default** and **Full** views – in the **Basic** view it is hidden but still works.

*(Internal ID: `c_impEverything`)*

### Import Settings... (dialog) › Source of Settings

#### PDF file (with embedded settings) or ZIP archive file

- **Where:** Import Settings... (dialog) › Source of Settings
- **Type:** Radio button
- **Description:** Import: From existing PDF file or ZIP archive
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> It is possible to import settings from an existing PDF file which was produced earlier by PTXprint. But this only works if the settings are embedded within the PDF. (This is enabled on the Finishing tab).
>
> Importing from a PTXprint ZIP archive (created on the Help tab) is also possible.

**Explanation:**

Import from a PDF made by PTXprint (with settings embedded) or from a PTXprint ZIP archive. Click **Select...** to choose the file.

*(Internal ID: `r_impSource_pdf`)*

#### A Previously Saved Configuration

- **Where:** Import Settings... (dialog) › Source of Settings
- **Type:** Radio button
- **Description:** Import: From Saved Configuration
- **View level:** Basic, Default and Full views

**Explanation:**

Import from a configuration that is saved on this computer. Choose the **Project** and **Configuration** below. Choosing a project or configuration in those lists also selects this option.

*(Internal ID: `r_impSource_config`)*

#### Project

- **Where:** Import Settings... (dialog) › Source of Settings
- **Type:** Drop-down list
- **Description:** Import: Project name
- **View level:** Basic, Default and Full views
- **Choices:** unknown
- **Only available when:** “A Previously Saved Configuration” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Select the project from which the settings will be imported.

**Explanation:**

The project that has the configuration you want to copy from. When you choose a project, the **Configuration** list is filled with its configurations, and **Default** is selected.

*(Internal ID: `fcb_impProject`)*

#### Configuration

- **Where:** Import Settings... (dialog) › Source of Settings
- **Type:** Drop-down list
- **Description:** Import: Project configuration
- **View level:** Basic, Default and Full views
- **Choices:** (None)
- **Only available when:** “A Previously Saved Configuration” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Select a configuration from the selected project from which the settings will be imported.

**Explanation:**

The configuration to copy settings from. The settings are read from the saved files, so save the source configuration first if it is open.

*(Internal ID: `ecb_impConfig`)*

#### Select...

- **Where:** Import Settings... (dialog) › Source of Settings
- **Type:** Button
- **Description:** Select PDF to import settings from
- **View level:** Basic, Default and Full views
- **Only available when:** “PDF file (with embedded settings) or ZIP archive file” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Select either a PTXprint PDF or ZIP archive to import the settings from.
>
> Importing from a PDF will only work if the PDF contains the PTXprint configuration settings (as enabled on the Finishing tab).

**Explanation:**

Opens a file chooser, starting in the output folder of the current project, where PTXprint keeps its PDFs. Choose a PDF or ZIP. If the file has no PTXprint settings, PTXprint shows an error and changes back to **A Previously Saved Configuration**. The chosen file name is shown next to the button.

*(Internal ID: `btn_impSource_pdf`)*

### Import Settings... (dialog) › Target

#### An External Folder of Settings

- **Where:** Import Settings... (dialog) › Target
- **Type:** Radio button
- **Description:** Extract settings to an external folder
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Settings can be extracted to an external folder.
>
> This may be useful when examining settings from a different user, or when there is a need to recover lost settings from a known good PDF or Zip archive.

**Explanation:**

Copy the settings files to a folder instead of into a configuration. No project is changed. This is useful to look at someone else's settings, or to rescue a few files from a good PDF or ZIP. **Everything** is used automatically.

*(Internal ID: `r_impTarget_folder`)*

#### A New/Existing Project and/or Configuration

- **Where:** Import Settings... (dialog) › Target
- **Type:** Radio button
- **Description:** Import: Into Project/Configuration
- **View level:** Basic, Default and Full views

**Explanation:**

Import into a configuration of a project on this computer. This is the usual choice. The current project and configuration are filled in when the dialog opens.

*(Internal ID: `r_impTarget_prjcfg`)*

#### Project

- **Where:** Import Settings... (dialog) › Target
- **Type:** Drop-down list
- **Description:** Import: Project name
- **View level:** Basic, Default and Full views
- **Choices:** unknown
- **Only available when:** “A New/Existing Project and/or Configuration” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Select an existing project into which the settings will be imported.  
>   OR Enter a NEW project name which causes a (temporary) project to be created in the normal Paratext folder.
>
> Select the project into which the settings will be imported.

**Explanation:**

The project that receives the settings. Choose one of your existing projects. Choosing a project here also selects **A New/Existing Project and/or Configuration** and fills the **Configuration** list.

*(Internal ID: `ecb_targetProject`)*

#### Select...

- **Where:** Import Settings... (dialog) › Target
- **Type:** Button
- **Description:** Select target folder for extracted settings
- **View level:** Basic, Default and Full views
- **Only available when:** “An External Folder of Settings” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Select a folder to save the settings in. This could be in a temporary location from where just the needed settings can be accessed and copied into the appropriate place of an existing config.

**Explanation:**

Opens a folder chooser for **An External Folder of Settings**. Choose an empty folder, so that the extracted files are easy to find. The chosen folder is shown next to the button.

*(Internal ID: `btn_tgtFolder`)*

#### Configuration

- **Where:** Import Settings... (dialog) › Target
- **Type:** Drop-down list
- **View level:** Basic, Default and Full views
- **Choices:** Default
- **Only available when:** “A New/Existing Project and/or Configuration” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Choose a configuration from the selected project into which the settings will be imported.  
>   OR Enter a NEW config name which causes a new configuration to be created for the current/new project.
>
> Select a configuration in the selected project into which the settings will be imported.

**Explanation:**

The configuration that receives the settings. Choose an existing one, or type a new name to create a new configuration. Importing into a new configuration is the safest way to try an import, because your existing configurations are not changed.

*(Internal ID: `ecb_targetConfig`)*

#### Enter a name for the configuration to be saved.

- **Where:** Import Settings... (dialog) › Target
- **Type:** Text box
- **View level:** Basic, Default and Full views
- **Only available when:** “A New/Existing Project and/or Configuration” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Enter a name for the configuration to be saved.
>
> Note that only Roman/Latin names are supported using: a-z A-Z, 0-9, parentheses, underscores and hyphens.

**Explanation:**

The text part of the target **Configuration** box. Type a new configuration name here. Use only letters a–z and A–Z, numbers, `(`, `)`, `_` and `-`, with no spaces. A new configuration starts from the PTXprint defaults, so tick **Everything** (or all the groups you need).

*(Internal ID: `t_targetConfig`)*

### Import Settings... (dialog) › Pictures tab

#### Import Entire PicList "as is" (overwrite existing PicList)

- **Where:** Import Settings... (dialog) › Pictures tab
- **Type:** Radio button
- **Description:** Import: Entire PicList "as is" (overwrite existing PicList)
- **View level:** Default and Full views
- **Only available when:** “Pictures” is selected

**Explanation:**

Replaces the target's whole picture list with the source's picture list. Pictures that were only in the target are removed. Use it when the source is the "master" picture list. (Default and Full views.)

*(Internal ID: `r_impPics_entire`)*

#### Import Elements of PicList (preserving existing PicList)

- **Where:** Import Settings... (dialog) › Pictures tab
- **Type:** Radio button
- **Description:** Import: Elements of PicList (preserving existing PicList)
- **View level:** Default and Full views
- **Only available when:** “Pictures” is selected

**Explanation:**

Keeps the target's picture list, and copies only the parts you tick below (captions, size and position, copyright) for pictures that are in both lists. Use **Add Any New Pictures** and **Remove Any Old Pictures** to control which pictures are in the list. (Default and Full views.)

*(Internal ID: `r_impPics_elements`)*

#### Captions

- **Where:** Import Settings... (dialog) › Pictures tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Import Elements of PicList (preserving existing PicList)”, “Pictures” is selected

**Explanation:**

Copies the caption text, the caption of the second text in a diglot, and the reference shown with the picture. Leave it unticked if the target is in another language, because the captions would then be in the wrong language.

*(Internal ID: `c_pic_Captions`)*

#### Size, Position, Mirror, Rotation settings

- **Where:** Import Settings... (dialog) › Pictures tab
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Import Elements of PicList (preserving existing PicList)”, “Pictures” is selected

**Explanation:**

Copies the size, the position on the page, the scale, mirroring and rotation of each picture. This is useful when two projects share the same pictures and layout.

*(Internal ID: `c_pic_SizePosn`)*

#### Copyright Information

- **Where:** Import Settings... (dialog) › Pictures tab
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Import Elements of PicList (preserving existing PicList)”, “Pictures” is selected

**Explanation:**

Copies the copyright (credit) information of each picture.

*(Internal ID: `c_pic_Copyright`)*

#### Add Any New Pictures

- **Where:** Import Settings... (dialog) › Pictures tab
- **Type:** Checkbox (ticked by default)
- **View level:** Basic, Default and Full views
- **Only available when:** “Pictures” is selected

**Explanation:**

Adds pictures that are in the source list but not yet in the target list. Leave it ticked unless you want to keep exactly the pictures that the target already has.

*(Internal ID: `c_impPicsAddNew`)*

#### Remove Any Old Pictures

- **Where:** Import Settings... (dialog) › Pictures tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Basic, Default and Full views
- **Only available when:** “Pictures” is selected

**Explanation:**

Removes pictures from the target list that are not in the source list. Tick it when the source list is the complete, final list.

*(Internal ID: `c_impPicsDelOld`)*

### Import Settings... (dialog) › Styles tab

#### Override ALL Style Settings

- **Where:** Import Settings... (dialog) › Styles tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Normally only styles that have not been changed in the receiving configuration will be imported. But if you require ALL styles to be updated regardless of whether they have already been modified locally, then enable this option.

**Explanation:**

Normally, PTXprint only updates styles that you have not changed in the target, so your own style changes are kept. Tick this box to update all styles from the source, even the ones you changed.

*(Internal ID: `c_sty_OverrideAllStyles`)*

### Import Settings... (dialog) › Other tab

#### Body Tab settings

- **Where:** Import Settings... (dialog) › Other tab
- **Type:** Checkbox (ticked by default)
- **View level:** Basic, Default and Full views
- **Only available when:** “Other” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Import the settings of the Body tab.

**Explanation:**

Imports the settings of the **Body** tab: how books and chapters start, chapter and verse numbers, section headings, hyphenation, glossary markup, and similar.

*(Internal ID: `c_oth_Body`)*

#### Notes+Refs settings

- **Where:** Import Settings... (dialog) › Other tab
- **Type:** Checkbox (ticked by default)
- **View level:** Basic, Default and Full views
- **Only available when:** “Other” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Import the settings of the Notes+Refs tab.

**Explanation:**

Imports the settings of the **Notes+Refs** tab: footnotes, cross-references, note callers, note rules and study notes.

*(Internal ID: `c_oth_NotesRefs`)*

#### Header+Footer settings

- **Where:** Import Settings... (dialog) › Other tab
- **Type:** Checkbox (ticked by default)
- **View level:** Basic, Default and Full views
- **Only available when:** “Other” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Import the settings of the Header+Footer tab.

**Explanation:**

Imports the settings of the **Header+Footer** tab: what is shown in the header and footer, and the header and footer positions.

*(Internal ID: `c_oth_HeaderFooter`)*

#### Thumb Tabs settings

- **Where:** Import Settings... (dialog) › Other tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Basic, Default and Full views
- **Only available when:** “Other” is selected

**Explanation:**

Meant to import the thumb tab settings from the **Tabs+Borders** tab. In the current version it may not bring in these settings; after importing, check the **Tabs+Borders** tab.

*(Internal ID: `c_oth_ThumbTabs`)*

#### Overwrite Front Matter

- **Where:** Import Settings... (dialog) › Other tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Basic, Default and Full views
- **Only available when:** “Front +Back Matter”, “Cover settings”, “Other” is selected

**Explanation:**

Only available when **Front +Back Matter** or **Cover settings** is ticked. It is meant to replace the front matter in the target with the source's front matter, instead of only adding missing parts. In the current version it may have no effect unless **Everything** is ticked; check the front matter on the **Peripherals** tab after importing.

*(Internal ID: `c_oth_OverwriteFrtMatter`)*

#### Advanced settings

- **Where:** Import Settings... (dialog) › Other tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Basic, Default and Full views
- **Only available when:** “Other” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This includes everything on the Advanced tab with the exception of Custom Script processing and Customized Styles (custom.sty).

**Explanation:**

Imports the options of the **Advanced** tab and the files that go with them: the changes file, the extra TeX files, and the extra style file (merged with the target's). If the source uses a custom script and the script file is in the source, it is copied too. The customized styles file (custom.sty) is not imported.

*(Internal ID: `c_oth_Advanced`)*

#### Cover settings

- **Where:** Import Settings... (dialog) › Other tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Basic, Default and Full views
- **Only available when:** “Other” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Import the cover settings, cover styles and the cover pages of the front matter.

**Explanation:**

Imports the cover settings, the cover styles, and the cover pages from the source's front matter. It also turns on decorations, which the cover uses.

*(Internal ID: `c_oth_Cover`)*

#### Front +Back Matter

- **Where:** Import Settings... (dialog) › Other tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Basic, Default and Full views
- **Only available when:** “Other” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This includes most of the settings on the Peripherals tab, but not the Variables and Values. Front Matter and also Section Introductions are included in this.

**Explanation:**

Imports the settings of the **Peripherals** tab (front and back PDFs, table of contents, front matter, colophon, section introductions), the front matter pages from the source, and any variables that the target does not have yet. Existing variable values in the target are not changed.

*(Internal ID: `c_oth_FrontMatter`)*

#### Custom Script

- **Where:** Import Settings... (dialog) › Other tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Basic, Default and Full views
- **Only available when:** “Other” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This includes the Custom Script processing defined on the Advanced tab.
>
> Note that it is not possible to extract a custom script from a PDF file, which is why this option is sometimes disabled.

**Explanation:**

Meant for the custom script set on the **Advanced** tab. Greyed out when the source is a PDF, because a PDF does not hold the script. In the current version the script is imported together with **Advanced settings**, so tick that box as well.

*(Internal ID: `c_oth_customScript`)*

#### Borders + Decorations

- **Where:** Import Settings... (dialog) › Other tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Other” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This includes the various decorative borders and other ornamental features including section headers, end-of-book and verse number decorators.

**Explanation:**

Imports the decoration settings from the **Tabs+Borders** tab: page borders, section-heading decorations, the book-title border, end-of-book decorations and verse-number decorations. (Default and Full views.)

*(Internal ID: `c_oth_Decorate`)*

#### Variables + Meta Data

- **Where:** Import Settings... (dialog) › Other tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Other” is selected

**Explanation:**

Meant to import the variables (the values on the **Peripherals** tab) and information about the publication. In the current version it may have no effect on its own; variables that the target is missing are also added by **Front +Back Matter**. (Default and Full views.)

*(Internal ID: `c_oth_Variables`)*

#### Texpert Hacks

- **Where:** Import Settings... (dialog) › Other tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Other” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> Import the expert TeX (TeXpert) settings.

**Explanation:**

Imports the expert TeX settings (the "TeXpert" options on the **Advanced** tab). Use it only if you know that the source used special TeX settings. (Default and Full views.)

*(Internal ID: `c_oth_Texpert`)*

#### Finishing settings

- **Where:** Import Settings... (dialog) › Other tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Other” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> This includes everything on the Finishing tab.

**Explanation:**

Imports the settings of the **Finishing** tab: PDF output format, watermark, crop marks, grid, pages per sheet and sheet size, the compare-PDF settings, and whether settings are included in the PDF. (Default and Full views.)

*(Internal ID: `c_oth_Finish`)*
