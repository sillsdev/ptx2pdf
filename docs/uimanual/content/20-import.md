## What this dialog is for

The **Import Settings** dialog copies settings from somewhere else into a configuration. Use it when:

* you have a PDF that PTXprint made earlier, and want the same layout again (for example the settings were lost, or the PDF came from another person),
* someone sent you a PTXprint ZIP archive,
* another project or configuration has settings you want to reuse – all of them, or only some groups (for example only the pictures, or only the header and footer).

You can also **extract** the settings from a PDF or ZIP into a normal folder, to look at them.

To open it: on the **Basic** tab, in the **Layout Configuration** area, click **Import Settings...**. (Not shown in the **Mini** view.)

The dialog has three parts: **Source of Settings** (where the settings come from), **Target** (where they go), and a row of **category tabs** (what to bring in).

## Source of Settings

Choose one of two sources:

* **PDF file (with embedded settings) or ZIP archive file** – click **Select...** and choose the file.
  * A **PDF** only works if PTXprint made it with **Include Config Settings Within PDF** turned on (on the **Finishing** tab). Otherwise PTXprint says it cannot find any settings in the file.
  * A **ZIP archive** is the kind of file made with **Create Archive...** on the **Help** tab.
* **A Previously Saved Configuration** – choose the **Project** and then the **Configuration** to copy from. Settings are read from the saved files, so if the source is the configuration that is open now, click **Save** first.

## Target

Choose where the settings go:

* **A New/Existing Project and/or Configuration** – the usual choice. The current project and configuration are filled in. You can choose another existing project, and another configuration, or type a **new** configuration name. A new configuration starts with the PTXprint defaults, and then the imported settings are added. So for a new name, PTXprint ticks **Everything** and greys out the category boxes. If you then choose an existing configuration again, **Everything** is unticked again (unless you ticked it yourself).
* **An External Folder of Settings** – click **Select...** and choose a folder. PTXprint copies **all** the settings files from the source into that folder. Nothing in your projects is changed. **Everything** is turned on and the category tabs are greyed out.

**OK** stays greyed out until the choices are complete: a file or source configuration, a target folder or target configuration, and at least one category ticked. It is also greyed out when the source and target are the same configuration, and when the target **Project** name you typed is not one of your projects.

## What to import: the category tabs

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

## RESET

**RESET** at the bottom of the dialog sets all settings of the **current** configuration back to the PTXprint defaults, at once and without asking. It does not reset the style settings. The dialog stays open, and nothing is saved until you click **Save** or **Print (Make PDF)** (or until an import saves the configuration). Use it when you want the target to have only the imported settings, for example before you import styles.

## Common tasks

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

## Common problems

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

## Control notes

### @btn_resetConfig
Resets at once and without asking. See "RESET" in this chapter.

### @btn_importSettingsOK
Imports the ticked groups into the target, saves it, and opens it. With an external folder as target, it copies the settings files there instead. Greyed out until the choices are complete. Shortcut: **Alt+Enter**.

### @btn_importCancel
Closes without importing. (Changes made with **RESET** stay on the screen.) Shortcut: **Ctrl+W**.

### @c_impPictures
Ticking or unticking it opens the **Pictures** tab of the dialog.

### @c_impLayout
See the table in "What each category brings in". The text on the dialog's **Layout** tab also mentions the header and footer, but they are imported with **Other** › **Header+Footer settings**.

### @c_impFontsScript
Imports fonts inside styles (font name and font features) even when **Styles** is not ticked. Hyphenation settings come with **Other** › **Body Tab settings**, not here.

### @c_impStyles
Font names and font features inside styles are imported only when **Fonts+Script** (or **Everything**) is also ticked.

### @c_impOther
Groups on the **Other** tab include Body, Notes+Refs, Header+Footer, Advanced, Cover, Front +Back Matter and Finishing.

### @c_impEverything
Use it to recreate a configuration from a PDF or ZIP, or to make a full copy. Ticked by default, and ticked again when you open the dialog with no category ticked. Also turned on automatically (with the other boxes greyed out) when the target is an external folder or a new configuration. In the **Basic** view it is hidden but still works.

### @r_impSource_pdf
Click **Select...** to choose the file.

### @r_impSource_config
Choosing a project or configuration in the lists below also selects this option.

### @fcb_impProject
Choosing a project fills the **Configuration** list with its configurations and selects **Default**.

### @ecb_impConfig
Settings are read from the saved files, so save the source configuration first if it is open.

### @btn_impSource_pdf
Starts in the output folder of the current project, where PTXprint keeps its PDFs. If the file has no PTXprint settings, PTXprint shows an error and changes back to **A Previously Saved Configuration**. The chosen file name is shown next to the button.

### @r_impTarget_folder
No project is changed. **Everything** is used automatically.

### @r_impTarget_prjcfg
The usual choice. The current project and configuration are filled in when the dialog opens.

### @ecb_targetProject
You cannot import into a new project. If you type a name that is not one of your projects, **OK** stays greyed out. Choosing a project here also selects **A New/Existing Project and/or Configuration** and fills the **Configuration** list.

### @btn_tgtFolder
Choose an empty folder, so the extracted files are easy to find. The chosen folder is shown next to the button.

### @ecb_targetConfig
Importing into a new configuration is the safest way to try an import, because your existing configurations are not changed.

### @t_targetConfig
The text part of the target **Configuration** box. No spaces. When you type a new name, PTXprint ticks **Everything** for you.

### @r_impPics_entire
Pictures that were only in the target are removed.

### @r_impPics_elements
The parts are captions, size and position, and copyright. **Add Any New Pictures** and **Remove Any Old Pictures** control which pictures are in the list.

### @c_pic_Captions
Also copies the caption of the second text in a diglot. Unticked for another language because the captions would be in the wrong language.

### @c_pic_SizePosn
Useful when two projects share the same pictures and layout.

### @c_pic_Copyright
Copies the picture credits.

### @c_impPicsAddNew
Leave it ticked unless you want to keep exactly the pictures the target already has.

### @c_impPicsDelOld
Use it with a complete, final source list.

### @c_sty_OverrideAllStyles
Without it, your own style changes in the target are kept.

### @c_oth_Body
Includes how books and chapters start, chapter and verse numbers, section headings, hyphenation, glossary markup, and similar.

### @c_oth_NotesRefs
Footnotes, cross-references, note callers, note rules and study notes.

### @c_oth_HeaderFooter
What is shown in the header and footer, and their positions.

### @c_oth_ThumbTabs
Use it when two configurations or projects should have matching thumb tabs.

### @c_oth_OverwriteFrtMatter
Leave it unticked if the target has its own front matter (for example in another language) that you want to keep.

### @c_oth_Advanced
Includes the changes file, the extra TeX files, and the extra style file (merged with the target's). For the custom script, tick **Custom Script**. custom.sty is not imported.

### @c_oth_Cover
Also turns on decorations, which the cover uses.

### @c_oth_FrontMatter
Includes front and back PDFs, table of contents, front matter, colophon and section introductions, plus the source's front matter pages and any variables the target does not have yet. Existing variable values in the target are not changed.

### @c_oth_customScript
Includes whether the script is used and when it runs. PTXprint finds the script in the source (also inside a ZIP made with **Create Archive...**), copies it into the target configuration folder, and points the **Advanced** tab at the copy. For a Python script, other Python files it uses from the same folder are copied too. Greyed out (and unticked) when the source is a PDF.

### @c_oth_Decorate
Includes page borders and the book-title border.

### @c_oth_Variables
Variables that the target is missing are also added by **Front +Back Matter**.

### @c_oth_Texpert
Use it only if you know that the source used special TeX settings.

### @c_oth_Finish
PDF output format, watermark, crop marks, grid, pages per sheet and sheet size, the compare-PDF settings, and whether settings are included in the PDF.
