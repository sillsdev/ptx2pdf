# 21. Importing settings

## 21.1 What this dialog is for

The **Import Settings** dialog copies settings from somewhere else into a configuration. Use it when:

* you have a PDF that PTXprint made earlier, and want the same layout again (for example the settings were lost, or the PDF came from another person),
* someone sent you a PTXprint ZIP archive,
* another project or configuration has settings you want to reuse – all of them, or only some groups (for example only the pictures, or only the header and footer).

You can also **extract** the settings from a PDF or ZIP into a normal folder, to look at them.

To open it: on the **Basic** tab, in the **Layout Configuration** area, click **Import Settings...**. (Not shown in the **Mini** view.)

The dialog has three parts: **Source of Settings** (where the settings come from), **Target** (where they go), and a row of **category tabs** (what to bring in).

## 21.2 Source of Settings

Choose one of two sources:

* **PDF file (with embedded settings) or ZIP archive file** – click **Select...** and choose the file.
  * A **PDF** only works if PTXprint made it with **Include Config Settings Within PDF** turned on (on the **Finishing** tab). Otherwise PTXprint says it cannot find any settings in the file.
  * A **ZIP archive** is the kind of file made with **Create Archive...** on the **Help** tab.
* **A Previously Saved Configuration** – choose the **Project** and then the **Configuration** to copy from. Settings are read from the saved files, so if the source is the configuration that is open now, click **Save** first.

## 21.3 Target

Choose where the settings go:

* **A New/Existing Project and/or Configuration** – the usual choice. The current project and configuration are filled in. You can choose another existing project, and another configuration, or type a **new** configuration name. A new configuration starts with the PTXprint defaults, and then the imported settings are added. So for a new name, PTXprint ticks **Everything** and greys out the category boxes. If you then choose an existing configuration again, **Everything** is unticked again (unless you ticked it yourself).
* **An External Folder of Settings** – click **Select...** and choose a folder. PTXprint copies **all** the settings files from the source into that folder. Nothing in your projects is changed. **Everything** is turned on and the category tabs are greyed out.

**OK** stays greyed out until the choices are complete: a file or source configuration, a target folder or target configuration, and at least one category ticked. It is also greyed out when the source and target are the same configuration, and when the target **Project** name you typed is not one of your projects.

## 21.4 What to import: the category tabs

Each tab has a check box in its label: tick it to import that group. Click the tab to see its options.

* **Pictures** – the picture settings and the picture list.
* **Layout** – the page and column layout.
* **Fonts+Script** – fonts and writing-system settings.
* **Styles** – the settings from the **Styles** tab.
* **Other** – other groups that you choose one by one.
* **Everything** – all settings. (Only shown in the **Regular** and **Full** views.)

When **Everything** is ticked, everything is imported, whatever the other boxes say. Untick **Everything** to import only some groups.

### What each category brings in

| Category | What is imported |
|---|---|
| **Pictures** | The general settings of the **Pictures** tab (include pictures, picture folder, resolution, captions shown, placeholders…) and the picture list. With **Import Entire PicList "as is"** the whole list is replaced. With **Import Elements of PicList** only the parts you tick are copied for each picture. |
| **Layout** | Page size, margins (top, bottom, side), mirror pages and binding gutter, number of columns and column gutter, vertical rule between columns, line spacing, note lines, margin notes, and related settings. **Not** the fonts or font size (in **Fonts+Script**) or the header and footer (in **Other** › **Header+Footer settings**). |
| **Fonts+Script** | The main fonts (regular, bold, italic, bold italic, extra), the font size, the fallback font, text direction, script and line-breaking settings, word and letter spacing, coloured text, and script-specific options. Also the fonts set inside individual styles (for styles that the target already has). Styles whose font you changed in the target keep it, unless **Override ALL Style Settings** is ticked. |
| **Styles** | The style settings from the source (the **Styles** tab). Normally only styles that you have **not** changed in the target are updated. **Override ALL Style Settings** updates all styles. The fonts inside styles come with **Fonts+Script**, not with **Styles**. |
| **Other** | Only the groups that you tick on the **Other** tab (see the control notes below). |
| **Everything** | All settings in the source configuration, including the book list, copyright text, diglot and Strong's settings, the whole picture list, styles, front matter, cover, and the special files from the **Advanced** tab. |

### What happens when you click OK

1. PTXprint reads the settings from the source.
2. It changes only the ticked groups in the target configuration.
3. It **saves** the target configuration at once.
4. It opens the target project and configuration, and shows a message such as "Imported Settings into: ABC::NT_A5".

There is no Undo. If you are not sure, import into a **new** configuration name first, and check the result there.

## 21.5 RESET

**RESET** at the bottom of the dialog sets all settings of the **current** configuration back to the PTXprint defaults, at once and without asking. It does not reset the style settings. The dialog stays open, and nothing is saved until you click **Save** or **Print (Make PDF)** (or until an import saves the configuration). Use it when you want the target to have only the imported settings, for example before you import styles.

## 21.6 Common tasks

### Get back the settings that were used for a PDF

1. On the **Basic** tab, click **Import Settings...**.
2. Click **PDF file (with embedded settings) or ZIP archive file**, then **Select...**, and choose the PDF.
3. Under **Target**, click **A New/Existing Project and/or Configuration**. In **Configuration**, type a new name, for example `FromPDF`.
4. Check that **Everything** is ticked. (For a new name, PTXprint ticks it for you. Change to the **Regular** view if you cannot see it.)
5. Click **OK**. PTXprint opens the new configuration with the settings from the PDF.

### Copy only the pictures from another configuration

1. Click **Import Settings...**.
2. Click **A Previously Saved Configuration** and choose the source **Project** and **Configuration**.
3. Check that the **Target** is the configuration you want.
4. Untick **Everything**, **Layout**, **Fonts+Script**, **Styles** and **Other**. Tick **Pictures**.
5. On the **Pictures** tab, choose **Import Entire PicList "as is"**, or **Import Elements of PicList** and tick only what you want (for example **Size, Position, Mirror, Rotation settings**).
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

## 21.7 Common problems

### "Cannot find any settings to import from the selected file"

**Cause:** The PDF was made without **Include Config Settings Within PDF** (on the **Finishing** tab), or with a very old PTXprint version (before 2.3). **What to do:** Use another source, for example a ZIP archive made with **Create Archive...** on the **Help** tab.

### The OK button is greyed out

**Cause:** Something is missing: no file selected, no target folder, no target configuration, no category ticked – or the source and target are the same configuration. **What to do:** Check each part of the dialog.

### Everything was imported, but I ticked only one category

**Cause:** **Everything** was still ticked. In the **Basic** view the **Everything** tab is hidden but still ticked (it is ticked by default). Also, when the target is a **new** configuration or an external folder, PTXprint ticks **Everything** itself and you cannot untick it. **What to do:** Import into an existing configuration. Change to the **Regular** view (**☰** › **View Level** › **Regular View**) and untick **Everything**.

### The styles did not change

**Cause:** Without **Override ALL Style Settings**, only styles still unchanged in the target are updated. **What to do:** Tick **Override ALL Style Settings**, or click **RESET** before you import.

### The font size did not change when I imported Layout

**Cause:** The font size belongs to **Fonts+Script**. **What to do:** Tick **Fonts+Script** too.

### The header and footer did not change when I imported Layout

**Cause:** They belong to **Other** › **Header+Footer settings**. **What to do:** Tick **Other** and **Header+Footer settings**.

### Custom Script is greyed out

**Cause:** The source is a PDF, which does not contain the custom script. **What to do:** Import from a ZIP archive or a saved configuration instead.

### The fonts in some styles did not change

**Cause:** Fonts inside styles come with **Fonts+Script** (not **Styles**), and styles whose font you changed in the target keep their font. **What to do:** Tick **Fonts+Script**. To replace the fonts in all styles, also tick **Override ALL Style Settings**.

### The category boxes are greyed out and Everything is ticked

**Cause:** The target is a configuration that does not exist yet (you typed a new name), or an external folder. A new configuration starts from the PTXprint defaults, so everything is imported. **What to do:** To import only some groups, choose an existing configuration as the target.

## 21.8 Settings reference

### Import Settings... (dialog)

#### RESET

Button · Basic+ · `btn_resetConfig`  
Also: Reset the current Configuration's UI settings

> Warning! This will reset ALL the UI settings for the CURRENT configuration to their default values.
>
> Note that it will NOT reset the Style settings stored in the .sty files.
>
> The reset is not saved until you next save, print, or import with OK.

Resets at once and without asking. See "RESET" in this chapter.

#### OK

Button · Basic+ · `btn_importSettingsOK`

Imports the ticked groups into the target, saves it, and opens it. With an external folder as target, it copies the settings files there instead. Greyed out until the choices are complete. Shortcut: **Alt+Enter**.

#### Cancel

Button · Basic+ · `btn_importCancel`

Closes without importing. (Changes made with **RESET** stay on the screen.) Shortcut: **Ctrl+W**.

#### Pictures

Checkbox, on · Basic+ · `c_impPictures`  
Also: Import Picture Settings

> Import the picture settings and the picture list. Use the Pictures tab of this dialog to choose how the picture list is combined.

Ticking or unticking it opens the **Pictures** tab of the dialog.

#### Layout

Checkbox, on · Basic+ · `c_impLayout`  
Also: Import Layout Settings

> Import page size, margins, columns, line spacing and related settings.

See the table in "What each category brings in". The text on the dialog's **Layout** tab also mentions the header and footer, but they are imported with **Other** › **Header+Footer settings**.

#### Fonts+Script

Checkbox, on · Basic+ · `c_impFontsScript`  
Also: Import Fonts and Script Settings

> Import the font and script settings (Fonts+Scripts tab), including fonts set within individual styles.

Imports fonts inside styles (font name and font features) even when **Styles** is not ticked. Hyphenation settings come with **Other** › **Body Tab settings**, not here.

#### Styles

Checkbox, on · Basic+ · `c_impStyles`  
Also: Import Styles Settings

> Import the style settings (Styles tab), merged into the target configuration.

Font names and font features inside styles are imported only when **Fonts+Script** (or **Everything**) is also ticked.

#### Other

Checkbox, on · Basic+ · `c_impOther`  
Also: Import Other Settings

> Use the Other tab of this dialog to choose more groups of settings. If this is not ticked, none of the boxes on the Other tab are used.

Groups on the **Other** tab include Body, Notes+Refs, Header+Footer, Advanced, Cover, Front +Back Matter and Finishing.

#### Everything

Checkbox, on · Regular+ · `c_impEverything`  
Also: Import All Settings

> Import all settings and files of the source configuration, whatever the other boxes say.

Use it to recreate a configuration from a PDF or ZIP, or to make a full copy. Ticked by default, and ticked again when you open the dialog with no category ticked. Also turned on automatically (with the other boxes greyed out) when the target is an external folder or a new configuration. In the **Basic** view it is hidden but still works.

#### Source of Settings

##### PDF file (with embedded settings) or ZIP archive file

Radio · Basic+ · `r_impSource_pdf`  
Also: Import: From existing PDF file or ZIP archive

> It is possible to import settings from an existing PDF file which was produced earlier by PTXprint. But this only works if the settings are embedded within the PDF. (This is enabled on the Finishing tab).
>
> Importing from a PTXprint ZIP archive (created on the Help tab) is also possible.

Click **Select...** to choose the file.

##### A Previously Saved Configuration

Radio · Basic+ · `r_impSource_config`  
Also: Import: From Saved Configuration

Choosing a project or configuration in the lists below also selects this option.

##### Project – Import: Project name

Drop-down · Basic+ · `fcb_impProject`  
Choices: unknown · Needs: “A Previously Saved Configuration”

> Select the project from which the settings will be imported.

Choosing a project fills the **Configuration** list with its configurations and selects **Default**.

##### Configuration – Import: Project configuration

Drop-down · Basic+ · `ecb_impConfig`  
Choices: (None) · Needs: “A Previously Saved Configuration”

> Select a configuration from the selected project from which the settings will be imported.

Settings are read from the saved files, so save the source configuration first if it is open.

##### Select...

Button · Basic+ · `btn_impSource_pdf`  
Also: Select PDF to import settings from · Needs: “PDF file (with embedded settings) or ZIP archive file”

> Select either a PTXprint PDF or ZIP archive to import the settings from.
>
> Importing from a PDF will only work if the PDF contains the PTXprint configuration settings (as enabled on the Finishing tab).

Starts in the output folder of the current project, where PTXprint keeps its PDFs. If the file has no PTXprint settings, PTXprint shows an error and changes back to **A Previously Saved Configuration**. The chosen file name is shown next to the button.

#### Target

##### An External Folder of Settings

Radio · Basic+ · `r_impTarget_folder`  
Also: Extract settings to an external folder

> Settings can be extracted to an external folder.
>
> This may be useful when examining settings from a different user, or when there is a need to recover lost settings from a known good PDF or Zip archive.

No project is changed. **Everything** is used automatically.

##### A New/Existing Project and/or Configuration

Radio · Basic+ · `r_impTarget_prjcfg`  
Also: Import: Into Project/Configuration

The usual choice. The current project and configuration are filled in when the dialog opens.

##### Project – Import: Project name

Drop-down · Basic+ · `ecb_targetProject`  
Choices: unknown · Needs: “A New/Existing Project and/or Configuration”

> Select an existing project into which the settings will be imported.
>
> Select the project into which the settings will be imported.

You cannot import into a new project. If you type a name that is not one of your projects, **OK** stays greyed out. Choosing a project here also selects **A New/Existing Project and/or Configuration** and fills the **Configuration** list.

##### Select...

Button · Basic+ · `btn_tgtFolder`  
Also: Select target folder for extracted settings · Needs: “An External Folder of Settings”

> Select a folder to save the settings in. This could be in a temporary location from where just the needed settings can be accessed and copied into the appropriate place of an existing config.

Choose an empty folder, so the extracted files are easy to find. The chosen folder is shown next to the button.

##### Configuration

Drop-down · Basic+ · `ecb_targetConfig`  
Choices: Default · Needs: “A New/Existing Project and/or Configuration”

> Choose a configuration from the selected project into which the settings will be imported.  
>   OR Enter a NEW config name which causes a new configuration to be created for the current/new project.
>
> Select a configuration in the selected project into which the settings will be imported.

Importing into a new configuration is the safest way to try an import, because your existing configurations are not changed.

##### Enter a name for the configuration to be saved.

Text box · Basic+ · `t_targetConfig`  
Needs: “A New/Existing Project and/or Configuration”

> Enter a name for the configuration to be saved.
>
> Note that only Roman/Latin names are supported using: a-z A-Z, 0-9, parentheses, underscores and hyphens.

The text part of the target **Configuration** box. No spaces. When you type a new name, PTXprint ticks **Everything** for you.

#### Pictures

##### Import Entire PicList "as is" (overwrite existing PicList)

Radio · Regular+ · `r_impPics_entire`  
Also: Import: Entire PicList "as is" (overwrite existing PicList) · Needs: “Pictures”

> Replace the target's whole picture list with the source's. Pictures only in the target are removed. Use it when the source is the master list.

Pictures that were only in the target are removed.

##### Import Elements of PicList (preserving existing PicList)

Radio · Regular+ · `r_impPics_elements`  
Also: Import: Elements of PicList (preserving existing PicList) · Needs: “Pictures”

> Keep the target's picture list and copy only the parts ticked below, for pictures in both lists.

The parts are captions, size and position, and copyright. **Add Any New Pictures** and **Remove Any Old Pictures** control which pictures are in the list.

##### Captions

Checkbox, off · Regular+ · `c_pic_Captions`  
Needs: “Import Elements of PicList (preserving existing PicList)”, “Pictures”

> Copy the captions and the reference shown with each picture. Leave unticked if the target is in another language.

Also copies the caption of the second text in a diglot. Unticked for another language because the captions would be in the wrong language.

##### Size, Position, Mirror, Rotation settings

Checkbox, on · Regular+ · `c_pic_SizePosn`  
Needs: “Import Elements of PicList (preserving existing PicList)”, “Pictures”

> Copy the size, position, scale, mirroring and rotation of each picture.

Useful when two projects share the same pictures and layout.

##### Copyright Information

Checkbox, on · Regular+ · `c_pic_Copyright`  
Needs: “Import Elements of PicList (preserving existing PicList)”, “Pictures”

> Copy the copyright (credit) information of each picture.

Copies the picture credits.

##### Add Any New Pictures

Checkbox, on · Basic+ · `c_impPicsAddNew`  
Needs: “Pictures”

> Add pictures that are in the source list but not yet in the target list.

Leave it ticked unless you want to keep exactly the pictures the target already has.

##### Remove Any Old Pictures

Checkbox, off · Basic+ · `c_impPicsDelOld`  
Needs: “Pictures”

> Remove pictures from the target list that are not in the source list. Tick it when the source list is the complete, final list.

Use it with a complete, final source list.

#### Styles

##### Override ALL Style Settings

Checkbox, off · Basic+ · `c_sty_OverrideAllStyles`

> Normally only styles that have not been changed in the receiving configuration will be imported. But if you require ALL styles to be updated regardless of whether they have already been modified locally, then enable this option. (This also applies to fonts in styles imported with Fonts+Script.)

Without it, your own style changes in the target are kept.

#### Other

##### Body Tab settings

Checkbox, on · Basic+ · `c_oth_Body`  
Needs: “Other”

> Import the settings of the Body tab.

Includes how books and chapters start, chapter and verse numbers, section headings, hyphenation, glossary markup, and similar.

##### Notes+Refs settings

Checkbox, on · Basic+ · `c_oth_NotesRefs`  
Needs: “Other”

> Import the settings of the Notes+Refs tab.

Footnotes, cross-references, note callers, note rules and study notes.

##### Header+Footer settings

Checkbox, on · Basic+ · `c_oth_HeaderFooter`  
Needs: “Other”

> Import the settings of the Header+Footer tab.

What is shown in the header and footer, and their positions.

##### Thumb Tabs settings

Checkbox, off · Basic+ · `c_oth_ThumbTabs`  
Needs: “Other”

> Import the thumb tab settings (Tabs+Borders tab).

Use it when two configurations or projects should have matching thumb tabs.

##### Overwrite Front Matter

Checkbox, off · Basic+ · `c_oth_OverwriteFrtMatter`  
Needs: “Front +Back Matter”, “Cover settings”, “Other”

> Replace the front matter in the target with the source's, instead of only adding the parts that are missing.

Leave it unticked if the target has its own front matter (for example in another language) that you want to keep.

##### Advanced settings

Checkbox, off · Basic+ · `c_oth_Advanced`  
Needs: “Other”

> This includes everything on the Advanced tab with the exception of Custom Script processing and Customized Styles (custom.sty).

Includes the changes file, the extra TeX files, and the extra style file (merged with the target's). For the custom script, tick **Custom Script**. custom.sty is not imported.

##### Cover settings

Checkbox, off · Basic+ · `c_oth_Cover`  
Needs: “Other”

> Import the cover settings, cover styles and the cover pages of the front matter.

Also turns on decorations, which the cover uses.

##### Front +Back Matter

Checkbox, off · Basic+ · `c_oth_FrontMatter`  
Needs: “Other”

> This includes most of the settings on the Peripherals tab, but not the Variables and Values. Front Matter and also Section Introductions are included in this.

Includes front and back PDFs, table of contents, front matter, colophon and section introductions, plus the source's front matter pages and any variables the target does not have yet. Existing variable values in the target are not changed.

##### Custom Script

Checkbox, off · Basic+ · `c_oth_customScript`  
Needs: “Other”

> This includes the Custom Script processing defined on the Advanced tab.
>
> Note that it is not possible to extract a custom script from a PDF file, which is why this option is sometimes disabled.

Includes whether the script is used and when it runs. PTXprint finds the script in the source (also inside a ZIP made with **Create Archive...**), copies it into the target configuration folder, and points the **Advanced** tab at the copy. For a Python script, other Python files it uses from the same folder are copied too. Greyed out (and unticked) when the source is a PDF.

##### Borders + Decorations

Checkbox, off · Regular+ · `c_oth_Decorate`  
Needs: “Other”

> This includes the various decorative borders and other ornamental features including section headers, end-of-book and verse number decorators.

Includes page borders and the book-title border.

##### Variables + Meta Data

Checkbox, off · Regular+ · `c_oth_Variables`  
Needs: “Other”

> Import the variables (Peripherals tab) and the publication details: copyright statement, licence, colophon and configuration notes. The book selection and any password are not imported.

Variables that the target is missing are also added by **Front +Back Matter**.

##### Texpert Hacks

Checkbox, off · Regular+ · `c_oth_Texpert`  
Needs: “Other”

> Import the expert TeX (TeXpert) settings.

Use it only if you know that the source used special TeX settings.

##### Finishing settings

Checkbox, off · Regular+ · `c_oth_Finish`  
Needs: “Other”

> This includes everything on the Finishing tab.

PDF output format, watermark, crop marks, grid, pages per sheet and sheet size, the compare-PDF settings, and whether settings are included in the PDF.
