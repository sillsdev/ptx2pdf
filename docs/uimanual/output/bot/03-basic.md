# Basic tab

## What this tab is for

The **Basic** tab is the first tab in PTXprint. You come here to:

* choose the **project** (the Paratext project with the Scripture text),
* choose, save, lock, copy or delete a **configuration** (a named set of settings),
* choose **what to print** – one book, part of a book, several books, or a Bible module,
* check the **copyright and license** statement for the publication.

Start here every time. Most other settings depend on the project and configuration that you choose on this tab.

## Project

Choose your Paratext project in the **Project** list. PTXprint shows the full name of the project next to the list.

* When you change to another project, PTXprint first saves the current configuration. Then it opens the configuration that you last used with the new project (or **Default**).
* At the end of the **Project** list there is a blue item, **Import...**. It opens the **Import Scripture...** dialog. Use it when you do not have the text as a Paratext project, but you have a Scripture text bundle (a .zip file), or when you want to install the sample text (the Berean Standard Bible).

### Copyright & Licensing

(This area is only shown in the **Default** and **Full** views.) Click **Copyright & Licensing** to open the area. It has two parts:

* **Copyright** – the copyright statement. PTXprint fills it in from the Paratext project settings. You can change it here. Click **Reload copyright from Paratext project** to get the Paratext text back.
* **License** – choose one of the Creative Commons licenses, **All Rights Reserved**, or type your own license.

PTXprint puts these texts into the front matter (for example on the title page back) through the variables `\zcopyright` and `\zlicense`. Some special codes work in both boxes: `(c)` becomes ©, `(r)` becomes ®, `(tm)` becomes ™, `~` is a non-breaking space, and `//` forces a new line.

## Layout Configuration

A **configuration** (or layout) is a named set of settings. One project can have many configurations, for example one for a draft and one for the final book. See the chapter about the main window for more about configurations and saving.

* **Name** – the list of saved configurations. Choose one to load its settings. You can also type a new name here and click **Save** to make a new configuration. Use only the letters a–z and A–Z, numbers, brackets `( )`, underscores `_` and hyphens `-`. No spaces.
* The **Save As** button (an icon next to the name) opens the **Save Current Configuration As...** dialog, where you type a name for a new configuration.
* The **lock** button locks or unlocks the configuration with a password.
* The **Copy configuration to other projects** button opens the **Copy Configuration To...** dialog. (Default and Full views.)
* **Delete** removes the selected configuration. For the **Default** configuration, this button is replaced by **Reset**.
* **Import Settings...** opens the **Import Settings** dialog, where you can bring settings in from a PDF, a ZIP archive, or another configuration. See the chapter "Importing settings". (Basic, Default and Full views.)
* **Notes** – an optional description of the configuration, for you and your team. (Basic, Default and Full views.)

When you choose another configuration in the **Name** list, PTXprint does **not** save the current one. Click **Save** first.

## What to Print

Choose one of three ways to say what goes into the PDF:

* **Single Book** – choose one book in the list. You can also type chapter numbers in **From Chapter** and **To** to print only part of the book. When you choose a new book, PTXprint sets the chapters to the whole book.
* **Portions or Multiple Books** – click **Select Multiple Books...** to choose books by clicking them, or type a list in the box. You can type book codes (`MAT MRK LUK JHN`), book ranges (`MAT-REV`) and references (`JHN 2:1-12`, `PSA 23; 100; 117`, `GEN 1:1-2:3`). Use the 3-letter USFM codes (for example `JHN`, not `John`). Press **Ctrl+B** to jump to this box.
* **Bible Module** – print a Paratext module (a .sfm file that lists passages to include). Click **Choose...** to select the module file. Click **Edit...** to see it on the **View+Edit** tab. (Bible Module is shown in the **Basic**, **Default** and **Full** views; **Edit...** in **Default** and **Full**.)

If you type in **From Chapter** or **To**, PTXprint changes to **Single Book**. If you type in the book list, PTXprint changes to **Portions or Multiple Books**.

The FRT (front matter) book is not in the book lists. Set up the front matter on the **Peripherals** tab instead.

## Dialogs on this tab

### Save Current Configuration As...

Opens when you click the **Save As** button. Type a name in **Configuration Name** and click **OK**. PTXprint makes a new configuration with a copy of the current settings, saves it, and changes to it. The **OK** button stays greyed out until the name is valid. PTXprint shows a message below the box if the name has spaces or special characters, or if a configuration with that name already exists.

Tip: Click **Save** before you use **Save As...**. Then the new configuration starts from your latest settings.

### Lock/Unlock Configuration

Opens when you click the **lock** button. Locking protects a configuration so that nobody changes or deletes it by mistake.

* **To lock:** type a password (up to 16 characters) and click **OK**. PTXprint saves the configuration and then locks it. The lock icon changes, and dots appear in the box next to the name.
* **To unlock:** click the lock button again, type the same password, and click **OK**. If the password is wrong, nothing happens.
* While a configuration is locked, **Save**, **Delete** and **Notes** are greyed out, and PTXprint does not save changes (not even when you print). You can still try out settings and print, but the changes are not kept.
* You cannot lock the **Default** configuration.

Note: if you click **Cancel** while the configuration is not locked, PTXprint may still lock it, with an empty password. To unlock it, click the lock button, leave the password box empty and click **OK**.

### Copy Configuration To...

Opens when you click the **Copy configuration to other projects** button. Use it when several projects need the same layout (for example, a series of New Testaments in related languages).

1. Click the projects that should receive a copy of the current configuration. The current project is shown in black and cannot be chosen. The **Recent** list at the bottom shows your selection, and remembers your last 10 selections.
2. Choose what to do if a target project already has a configuration with the same name:
   * **Do NOT Replace Existing Config** – skip those projects. Use this the first time you copy.
   * **Merge Configurations From Both** – combine the two. Settings that were changed in the target project since the first copy are kept.
   * **Overwrite With Recent Changes** – settings that were changed in this (source) project replace the target settings.
3. Click **OK**.

PTXprint copies the saved files of the configuration: the settings, the styles, the changes and TeX files, and the front matter. Adjust lists (paragraph adjustments) are not copied, because they belong to one text. Click **Save** before you copy, so that the copy has your latest settings.

### Select Books To Export to PDF

Opens when you click **Select Multiple Books...**. Each book in the project is a button. Click a button to select or unselect that book. Hold **Shift** and click another book to select or unselect all books between the two. The buttons at the side select groups: **All Books**, **Old Testament**, **New Testament**, **Deuterocanon**, **Extra Material**, **Toggle Books** (reverse the selection), and **Reset All** (unselect all). Click **OK**. PTXprint puts the books in the normal Bible order in the book list. You can then change the order in the list by typing, if needed.

### Import Scripture...

Opens when you choose **Import...** at the end of the **Project** list. There are two ways to get a text:

* **Install BSB** – installs the Berean Standard Bible, a public-domain English Bible that comes with PTXprint. It is good for practice and as a second text in a diglot.
* **Step 1 – Step 3** – install a Scripture text bundle (.zip):
  1. Download a bundle from the **Primary DBL site** (Digital Bible Library – you must log in) or the **Open.Bible site**. Choose a bundle that has the text (not only audio). The USX format is best.
  2. Click **Locate...** and choose the .zip file.
  3. Check the project name in **Assign a Name for the Project** and click **OK**.

PTXprint creates the new project in a folder called `_PTXprint` inside your Paratext projects folder, and opens it.

### Please Confirm...

PTXprint asks you to confirm before something that cannot be undone:

* **"You are about to REMOVE this Configuration"** – appears when you click **Delete**. Click **Yes** to delete the configuration, or **No** to keep it.
* **"You are about to CREATE a diglot (or polyglot) configuration"** – appears when you turn on a diglot. PTXprint suggests that you first use **Save As...** to make a new configuration for the diglot.

## Common tasks

### Start a new publication from an existing configuration

1. In **Project**, choose the project.
2. In **Name**, choose the configuration that is closest to what you want.
3. Click **Save** (so that the latest settings are on disk).
4. Click the **Save As** button. Type a new name (for example `NT_A5`) and click **OK**.
5. Now change the settings. The old configuration stays as it was.

### Print one book, or part of a book

1. Click **Single Book**.
2. Choose the book in the list.
3. To print only some chapters, type the first chapter in **From Chapter** and the last chapter in **To**.
4. Click **Print (Make PDF)**.

### Print several books, or selected passages

1. Click **Select Multiple Books...**.
2. Click the books you want (or click **New Testament**), then click **OK**.
3. Or type in the book list, for example `MAT-ACT` or `PSA 23; 100; 117 LUK 15:11-32`.
4. Click **Print (Make PDF)**.

### Protect a finished configuration

1. Choose the configuration in **Name** (not **Default**).
2. Click the **lock** button.
3. Type a password and click **OK**. Remember the password.

### Use the same layout for another project

1. Click **Save**.
2. Click the **Copy configuration to other projects** button. (Default or Full view.)
3. Click the target project(s).
4. Choose **Do NOT Replace Existing Config** and click **OK**.
5. In **Project**, choose the target project and check the copied configuration.

### Set or correct the copyright statement

1. Change to the **Default** or **Full** view if needed.
2. Click **Copyright & Licensing** to open it.
3. Type the copyright text (type `(c)` for ©), or click **Reload copyright from Paratext project**.
4. Choose or type the **License**.

### Get a text to practise with

1. Open the **Project** list and choose **Import...** (the last item).
2. Click **Install BSB**.
3. PTXprint installs and opens the BSB project.

### Delete a configuration that you do not need

1. Choose it in **Name**.
2. Click **Delete**, then **Yes**.
3. Before you delete, copy any PDF files that you want to keep to another folder (click the **Open folder containing the PDF** button at the bottom of the window to find them).

## Common problems

### My recent changes were lost when I chose another configuration

**Cause:** Choosing another configuration in the **Name** list does not save the current one. **What to do:** Always click **Save** before you change configurations.

### The lock button is greyed out

**Cause:** The **Default** configuration cannot be locked. **What to do:** Use **Save As** to make a named configuration, then lock that one.

### I cannot save, and Delete and Notes are greyed out

**Cause:** The configuration is locked. **What to do:** Click the lock button and enter the password, or use **Save As** to make a new, unlocked copy.

### There is a Reset button instead of Delete

**Cause:** The **Default** configuration is selected. It cannot be deleted. **Reset** is shown instead. Be careful: **Reset** asks no question. It sets all settings back to the PTXprint defaults at once.

### The OK button in "Save Current Configuration As..." is greyed out

**Cause:** The name is empty, has spaces or special characters, or is already used. **What to do:** Read the message below the box. Use only letters a–z and A–Z, numbers, `(`, `)`, `_` and `-`.

### PTXprint says "Unknown book code"

**Cause:** The book list has a word that is not a 3-letter USFM book code (for example `John`). **What to do:** Use the codes, for example `JHN`, `MAT`, `1CO`.

### I cannot find the FRT book in the list

**Cause:** PTXprint does not list FRT as a book. **What to do:** Set up front matter on the **Peripherals** tab.

### The Primary DBL site and Open.Bible site links do not work

**Cause:** **Disable ALL Internet Use** is ticked on the **Advanced** tab. **What to do:** Untick it, or download the bundle another way and use **Locate...**.

### Copyright & Licensing or Copy configuration are missing, or Reset is greyed out

**Cause:** They are only available in the **Default** and **Full** views. **What to do:** Click **☰** › **View Level** › **Default View**.

## Settings reference: Basic tab

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Import Scripture... (dialog)

#### OK

- **Where:** Import Scripture... (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Installs the bundle that you chose with **Locate...**, using the name in **Assign a Name for the Project**, and opens the new project. It is greyed out until the name is valid and not already used.

*(Internal ID: `btn_dbl_ok`)*

#### Cancel

- **Where:** Import Scripture... (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog without installing anything. PTXprint goes back to the project that was open before.

*(Internal ID: `btn_dbl_cancel`)*

#### Install BSB

- **Where:** Import Scripture... (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> The Berean Standard Bible is a Public Domain English Bible. It is bundled with PTXprint but needs to be installed in your Projects folder.
>
> This is a good training project and can also be used in diglots.

#### Locate...

- **Where:** Import Scripture... (dialog)
- **Type:** Button
- **Description:** Locate DBL bundle
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> After downloading a scripture text bundle (.zip) file you need to tell PTXprint where the .zip file is located so that it can install it as a special resource project.

**Explanation:**

Opens a file chooser in the `Bundles` folder of your Paratext projects folder. Choose the .zip file that you downloaded. PTXprint then shows the file name and suggests a project name from the bundle (adding a number if that name is already used). Shortcut: **Alt+O**.

*(Internal ID: `btn_locateDBLbundle`)*

#### Step 3 Assign a Name for the Project

- **Where:** Import Scripture... (dialog)
- **Type:** Text box
- **Description:** Assign a name to a DBL bundle
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> PTXprint will create this project within a subfolder called '_PTXprint'. Use 8 characters or less for the new project name. Do not use the name of an existing Project.

**Explanation:**

The short name (ID) of the new project. PTXprint suggests one from the bundle. Change it if you want. Use 8 characters or fewer, with no spaces or special characters, and do not use the name of a project you already have. A message appears below the box if the name cannot be used.

*(Internal ID: `t_DBLprojName`)*

#### Primary DBL site

- **Where:** Import Scripture... (dialog)
- **Type:** Link
- **Description:** Visit the Digital Bible Library to download a DBL Scripture bundle
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> There are hundreds of Scripture bundles available at the Digital Bible Library website which you may download and use in a publication. You must log in to the site in order to access resources.
>
> Use resources which contain the text (not just the audio) and preferably select the USX download option.
>
> Note: If this option is disabled, it is due to the "Disable ALL Internet Use" option which has been set on the General section of the Advanced tab.

**Explanation:**

Opens the Digital Bible Library website in your browser. You need a DBL login to download bundles. Choose a text bundle (not audio only), preferably in USX format. Greyed out when **Disable ALL Internet Use** is ticked on the **Advanced** tab.

*(Internal ID: `lb_DBLdownloads`)*

#### Open.Bible site

- **Where:** Import Scripture... (dialog)
- **Type:** Link
- **Description:** Visit the Open.Bible site to download a Scripture bundle
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> There are hundreds of Scripture bundles at the Open.Bible website which you may download and use in a publication.
>
> Use resources which contain the text (not just the audio) and preferably select the USX download option.
>
> Note: If this option is disabled, it is due to the "Disable ALL Internet Use" option which has been set on the General section of the Advanced tab.
>
> If you don't already have a Scripture Text Bundle, then you can download a USX or USFM text bundle from an online scripture repository.

**Explanation:**

Opens the Open.Bible website in your browser, where you can download openly licensed Scripture bundles. Choose a text bundle, preferably USX. Greyed out when **Disable ALL Internet Use** is ticked on the **Advanced** tab.

*(Internal ID: `lb_openBible`)*

### Save Current Configuration As... (dialog)

#### OK

- **Where:** Save Current Configuration As... (dialog)
- **Type:** Button
- **View level:** Basic, Default and Full views

**Explanation:**

Creates the new configuration with the name you typed, saves it, and changes to it. It is greyed out until the name is valid.

*(Internal ID: `btn_cfg_ok`)*

#### Cancel

- **Where:** Save Current Configuration As... (dialog)
- **Type:** Button
- **View level:** Basic, Default and Full views

**Explanation:**

Closes the dialog. No new configuration is made.

*(Internal ID: `btn_cfg_cancel`)*

#### Configuration Name

- **Where:** Save Current Configuration As... (dialog)
- **Type:** Text box
- **Description:** Enter a name for the configuration to be saved
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Enter a name for the configuration to be saved.
>
> Note that only Roman/Latin names are supported using: a-z A-Z, 0-9, parentheses, underscores and hyphens. Spaces are not permitted.

**Explanation:**

Type the name of the new configuration. Use a short, clear name such as `NT_A5` or `Draft_2col`. Spaces and letters with accents are not allowed. The message below the box tells you if the name is not valid or already exists. Write longer descriptions in **Notes** on the Basic tab.

*(Internal ID: `t_configName`)*

### Select Books To Export to PDF (dialog)

#### OK

- **Where:** Select Books To Export to PDF (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the book selector and puts the selected books in the book list, in normal Bible order. PTXprint changes to **Portions or Multiple Books** if any books are selected.

*(Internal ID: `btn_mbs_ok`)*

#### Cancel

- **Where:** Select Books To Export to PDF (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the book selector without changing the book list.

*(Internal ID: `btn_mbs_cancel`)*

#### All Books

- **Where:** Select Books To Export to PDF (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Click to turn ALL books on/off.

#### Old Testament

- **Where:** Select Books To Export to PDF (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Click to turn OT books on/off.

#### New Testament

- **Where:** Select Books To Export to PDF (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Click to turn NT books on/off.

#### Deuterocanon

- **Where:** Select Books To Export to PDF (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Click to turn DC books on/off.

#### Extra Material

- **Where:** Select Books To Export to PDF (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Click to turn Extra books on/off.

#### Toggle Books

- **Where:** Select Books To Export to PDF (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Click to toggle ALL books. Those which are selected will be deselected, and the unselected ones will be selected.

#### Reset All

- **Where:** Select Books To Export to PDF (dialog)
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Click to turn OFF all books.

#### Why is FRT not listed?

- **Where:** Select Books To Export to PDF (dialog)
- **Type:** Label
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> The FRT book in Paratext contains front matter for a publication. Visit the Peripherals page to set up front matter for this publication.

### Copy Configuration To... (dialog)

#### OK

- **Where:** Copy Configuration To... (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Copies the current configuration to all selected projects, using the option you chose (Do NOT Replace, Merge, or Overwrite). The copy uses the saved files, so click **Save** in the main window before you open this dialog.

*(Internal ID: `btn_mps_ok`)*

#### Cancel

- **Where:** Copy Configuration To... (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog. Nothing is copied.

*(Internal ID: `btn_mps_cancel`)*

#### Recent

- **Where:** Copy Configuration To... (dialog)
- **Type:** Drop-down list
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Shows selected target projects. Pick a previous selection from the dropdown, or select projects in the grid above.

**Explanation:**

Shows the names of the projects that you selected in the grid. You can also type project names here, separated by spaces, or choose an earlier selection from the list. PTXprint remembers your last 10 selections. This is useful when you copy to the same group of projects again and again.

*(Internal ID: `ecb_mpsTargets`)*

#### Do NOT Replace Existing Config

- **Where:** Copy Configuration To... (dialog)
- **Type:** Radio button
- **Description:** Copy Config: Do NOT Replace Existing Config
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Selecting this option will prevent any changes overwriting an existing configuration of the same name in the target project(s).
>
> This option is usually used when copying a configuration to other projects for the first time.

**Explanation:**

Copies the configuration only to projects that do **not** already have a configuration with this name. Projects that already have it are left unchanged. This is the safest choice, and the right choice the first time.

*(Internal ID: `r_copyConfig_noReplace`)*

#### Merge Configurations From Both

- **Where:** Copy Configuration To... (dialog)
- **Type:** Radio button
- **Description:** Copy Config: MERGE Configurations From Both
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Selecting this option will MERGE the settings from the source configuration with the identically named configuration in the target project. Any changes that were made to the target project's configuration since it was first shared will be kept (i.e. modified target settings are retained if there is a clash of settings).

**Explanation:**

For projects that already have a configuration with this name, PTXprint combines the two. When a setting was changed in the target project after the first copy, the target's value is kept. Other settings are updated from this project.

*(Internal ID: `r_copyConfig_merge`)*

#### Overwrite With Recent Changes

- **Where:** Copy Configuration To... (dialog)
- **Type:** Radio button
- **Description:** Copy Config: OVERWRITE With Recent Changes
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Selecting this option will REPLACE (or overwrite) any settings in the identically named configuration in the target project IF those settings were changed in the source project since the configuration was first shared. (i.e. if both source and target projects modified a setting, then the source project's setting will "win").

**Explanation:**

For projects that already have a configuration with this name, settings that were changed in this (source) project replace the values in the target. Use it when this project is the "master" layout for a group of projects.

*(Internal ID: `r_copyConfig_overwrite`)*

### Lock/Unlock Configuration (dialog)

#### OK

- **Where:** Lock/Unlock Configuration (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

This is the **OK** button of the Lock/Unlock dialog. It locks the configuration with the password you typed, or unlocks it if the password matches.

*(Internal ID: `btn_pw_cancel`)*

#### Cancel

- **Where:** Lock/Unlock Configuration (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

This is the **Cancel** button of the Lock/Unlock dialog. Note: if the configuration is not locked, clicking it may lock the configuration with an empty password. To undo this, open the dialog again, leave the box empty and click **OK**.

*(Internal ID: `btn_pw_ok`)*

#### Enter Password

- **Where:** Lock/Unlock Configuration (dialog)
- **Type:** Text box
- **Description:** Enter password for config
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Enter a password of up to 16 characters to lock/unlock this saved configuration.

**Explanation:**

Type the password here. PTXprint does not store the password itself, only a coded form of it. If you forget the password, you cannot unlock the configuration in PTXprint, so keep it somewhere safe.

*(Internal ID: `t_password`)*

### Basic tab › Project

#### Project ID

- **Where:** Basic tab › Project
- **Type:** Drop-down list
- **Description:** Paratext project code
- **View level:** All view levels (Mini, Basic, Default, Full)
- **Choices:** Unknown

**Explanation:**

Choose the Paratext project to print. When you change the project, PTXprint saves the current configuration first and opens the last configuration you used with the new project. The last item, **Import...** (in blue), opens the **Import Scripture...** dialog.

*(Internal ID: `fcb_project`)*

#### Copyright & Licensing

- **Where:** Basic tab › Project
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> It is important to include copyright and license statements on every publication. By default this will be set according to the Paratext project settings, but you can edit it here if needed by expanding the section below.

### Basic tab › Project › Copyright & Licensing

#### Copyright

- **Where:** Basic tab › Project › Copyright & Licensing
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> It is important to include a copyright statement on every publication. By default this will be set according to the Paratext project settings, but you can edit it here if needed.

#### License

- **Where:** Basic tab › Project › Copyright & Licensing
- **Type:** Drop-down list
- **Description:** License details
- **View level:** Default and Full views
- **Choices:** This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND).; This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC).; This work is licensed under a Creative Commons Attribution-Sharealike 4.0 International License (CC BY-SA).; This work is licensed under a Creative Commons Attribution 4.0 International License (CC BY).; All Rights Reserved.

**Tooltip (the text shown when you hover the mouse over it):**

> Select one of these licenses, or type a different license.
>
> Note: There are several shortcuts you can use:  
>    (c) --> ©  the copyright sign  
>    (r) --> ®  to denote registered trademarks  
>    (tm) --> ™  to denote trademarks in general
>
> Other special codes converted at print time:  
> Use ~ where a non-breaking space is needed. Use // to force a line break (:// in URLs is not changed).
>
> For more detailed information about the various Creative Commons licenses, refer to:  
> https://creativecommons.org/licenses/
>
> Select one of these licenses, or type a different license.
>
> Note: There are several shortcuts you can use:  
>    (c) --> ©  the copyright sign  
>    (r) --> ®  to denote registered trademarks  
>    (tm) --> ™  to denote trademarks in general
>
> Other special codes converted at print time:  
> use ~ for places where a non-breaking space is needed use // where a line break needs to be forced but :// used in URLs will still be preserved
>
> For more detailed information about the various Creative Commons licenses, refer to:  
> https://creativecommons.org/licenses/

**Explanation:**

Choose a Creative Commons license or **All Rights Reserved**, or type your own text. It is used in the front matter through `\zlicense`. Ask your organization which license to use. The special codes `(c)`, `(r)`, `(tm)`, `~` and `//` work here too.

*(Internal ID: `ecb_licenseText` · Config key: `project/license`)*

#### Copyright text entry

- **Where:** Basic tab › Project › Copyright & Licensing
- **Type:** Text area
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> It is important to include a copyright statement on every publication. Note: There are several shortcuts you can use:  
>    (c) --> ©  the copyright sign  
>    (r) --> ®  to denote registered trademarks  
>    (tm) --> ™  to denote trademarks in general
>
> Other special codes converted at print time:  
> Use ~ where a non-breaking space is needed. Use // to force a line break (:// in URLs is not changed).

**Explanation:**

The copyright statement for the publication. PTXprint fills it from the Paratext project settings when it is empty. When you type `(c)`, `(r)` or `(tm)`, PTXprint changes it to ©, ® or ™ at once. The text is used in the front matter through `\zcopyright`.

*(Internal ID: `textv_copyright`)*

#### Reload copyright from Paratext project

- **Where:** Basic tab › Project › Copyright & Licensing
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Clicking this button will reload the Copyright Statement from the Paratext project settings.

**Explanation:**

Replaces the text in the copyright box with the copyright statement from the Paratext project settings. If Paratext has no copyright statement, PTXprint shows a message in the status line.

*(Internal ID: `btn_resetCopyright`)*

### Basic tab › Layout Configuration

#### Notes

- **Where:** Basic tab › Layout Configuration
- **Type:** Text box
- **Description:** (Optional) Notes about configuration
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Optional: Provide a description about the saved/shared configuration named above.

**Explanation:**

A short description of this configuration, for example "A5 NT for village distribution, 2 columns". It is saved with the configuration, so other team members see it after Send/Receive. Greyed out when the configuration is locked.

*(Internal ID: `t_configNotes` · Config key: `config/notes`)*

#### Name

- **Where:** Basic tab › Layout Configuration
- **Type:** Text box
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Dots indicate that a password has been set for this configuration.

**Explanation:**

Shows dots when the configuration is locked with a password, and is empty when it is not locked. You cannot type here; use the lock button.

*(Internal ID: `t_invisiblePassword` · Config key: `config/pwd`)*

#### Name

- **Where:** Basic tab › Layout Configuration
- **Type:** Button
- **Description:** Lock configuration
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> When Config is UNLOCKED:  
> Click to set a password to prevent anyone from accidentally changing the saved settings or deleting the configuration.
>
> When Config is LOCKED:  
> Click to enter the password to unlock this configuration and allow changes to be saved or the configuration to be deleted.
>
> Note that the Default config cannot be locked.

**Explanation:**

Opens the **Lock/Unlock Configuration** dialog. The icon shows whether the configuration is locked. Greyed out for the **Default** configuration.

*(Internal ID: `btn_lockunlock`)*

#### Name

- **Where:** Basic tab › Layout Configuration
- **Type:** Button
- **Description:** Copy configuration to other projects
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> A saved configuration can be copied to other Paratext projects in order to avoid having to manually re-create all the same settings for a similar project.
>
> Save first: the saved files are copied. Adjust lists are not copied.

**Explanation:**

Opens the **Copy Configuration To...** dialog, to copy this configuration to one or more other Paratext projects. Save first. Only shown in the **Default** and **Full** views.

*(Internal ID: `btn_copyToTargetProj`)*

#### Name

- **Where:** Basic tab › Layout Configuration
- **Type:** Drop-down list
- **View level:** All view levels (Mini, Basic, Default, Full)
- **Choices:** Default

**Tooltip (the text shown when you hover the mouse over it):**

> Select a previously-saved layout configuration to retrieve those settings.
>
> Note: changes to the current configuration are not saved automatically when you switch. Save first to keep them.
>
> When the Paratext project is shared through Send/Recv, all saved layout configurations will also be made available to other PTXprint users of the same Paratext project.
>
> Alternatively, select a previously-saved layout configuration to retrieve settings.

**Explanation:**

The list of configurations saved for this project. Choose one to load its settings. PTXprint does **not** save the current configuration when you change to another one, so click **Save** first. Configurations are shared with other users of the project through Paratext Send/Receive.

*(Internal ID: `ecb_savedConfig`)*

#### Enter a name for the layout configuration to be saved.

- **Where:** Basic tab › Layout Configuration
- **Type:** Text box
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Enter a name for the layout configuration to be saved.
>
> Note that only Roman/Latin names are supported using: a-z A-Z, 0-9, parentheses, underscores and hyphens.
>
> Longer descriptions may be typed into the Notes field below.

**Explanation:**

The text part of the configuration **Name** box. You can type a new name here and click **Save** to create a new configuration from the current settings. Characters that are not allowed (such as spaces) are removed.

*(Internal ID: `t_savedConfig`)*

#### gtk-save-as

- **Where:** Basic tab › Layout Configuration
- **Type:** Button
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Save the current settings as a new Configuration.
>
> When the Paratext project is shared through Send/Recv, all saved configurations will be also made available to other PTXprint users of the same Paratext project.

#### Delete

- **Where:** Basic tab › Layout Configuration
- **Type:** Button
- **Description:** Delete configuration
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Delete this Saved Configuration
>
> This also deletes the corresponding subfolder of temporary files in the local\ptxprint folder but does not delete the previously created PDF files which will remain in that folder.

**Explanation:**

Deletes the selected configuration after you click **Yes** in the **Please Confirm...** dialog. PTXprint then opens the **Default** configuration. This cannot be undone. Before you delete, copy any PDF files that you want to keep to another folder. Not available for the **Default** configuration (you see **Reset** instead). Greyed out when the configuration is locked, and in the **Mini** view.

*(Internal ID: `btn_deleteConfig`)*

#### Reset

- **Where:** Basic tab › Layout Configuration
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Reset the Default configuration to PTXprint's default settings.
>
> Warning: this also deletes the files kept in the Default configuration folder (such as styles, picture list, adjust lists and front matter). There is no confirmation.

**Explanation:**

Only shown when the **Default** configuration is selected. It sets all settings of the Default configuration back to the PTXprint defaults, at once and without asking. The files kept in the Default configuration folder (for example its styles and picture list) are also removed. Use it only when you really want to start again. In the **Mini** and **Basic** views the button is greyed out.

*(Internal ID: `btn_resetDefaults`)*

#### Name

- **Where:** Basic tab › Layout Configuration
- **Type:** Button
- **Description:** Import settings from PDFs, ZIP files or other Configurations
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Open the Import Settings dialog to select options for importing settings from other PDFs, ZIP archives, or different project configurations.
>
> By default, imported settings are applied to the current project and configuration. However, you can also choose to import them into other projects or export them to an external folder.

**Explanation:**

Opens the **Import Settings** dialog. There you can bring settings into this (or another) configuration from a PTXprint PDF, a PTXprint ZIP archive, or another saved configuration, and choose which groups of settings to bring in. See the chapter "Importing settings". Not shown in the **Mini** view.

*(Internal ID: `btn_importSettings`)*

#### Layout Wizard...

- **Where:** Basic tab › Layout Configuration
- **Type:** Button
- **View level:** Experimental (only shown when PTXprint is started in experimental mode)

**Explanation:**

Opens the Layout Wizard, a step-by-step helper for setting up a layout. It is an experimental feature and is only shown when PTXprint is started in experimental mode.

*(Internal ID: `btn_layoutWizard`)*

### Basic tab

#### Layout Configuration

- **Where:** Basic tab
- **Type:** Label
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> A Layout (or Config) is a collection of settings that can be saved. By naming and saving a layout you can recall those settings later.

### Basic tab › What to Print

#### Single book chooser

- **Where:** Basic tab › What to Print
- **Type:** Drop-down list
- **View level:** All view levels (Mini, Basic, Default, Full)
- **Choices:** NONE

**Explanation:**

Choose the book to print when **Single Book** is selected. When you choose a book, PTXprint sets **From Chapter** to 1 and **To** to the last chapter of that book, and changes to **Single Book**.

*(Internal ID: `ecb_book` · Config key: `project/book`)*

#### Select Multiple Books...

- **Where:** Basic tab › What to Print
- **Type:** Button
- **Description:** Multiple book selector
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Select one or more Biblical books to be printed from the project.

**Explanation:**

Opens the **Select Books To Export to PDF** dialog, where you click the books you want. Shortcut: **Alt+O**.

*(Internal ID: `btn_chooseBooks`)*

#### Bible Module

- **Where:** Basic tab › What to Print
- **Type:** Radio button
- **Description:** Bible module selector
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Print a Paratext Bible module (a .sfm file that lists the passages to include).

**Explanation:**

Prints a Paratext Bible module instead of whole books. A module is a .sfm file (usually in the project's `Modules` folder) that lists the passages to include. Choose the file with **Choose...**. Not shown in the **Mini** view.

*(Internal ID: `r_book_module` · Config key: `project/bookscope=module`)*

#### Portions or Multiple Books

- **Where:** Basic tab › What to Print
- **Type:** Radio button
- **Description:** Choose books or enter ranges to print
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Print several books, or the passages listed in the box.

**Explanation:**

Prints the books or passages in the book list. Use it for several books, for a range such as `MAT-REV`, or for selected passages such as `PSA 23; 100`. PTXprint changes to this option when you type in the book list or pick books with **Select Multiple Books...**.

*(Internal ID: `r_book_multiple` · Config key: `document/multibook`)*

#### Single Book

- **Where:** Basic tab › What to Print
- **Type:** Radio button
- **Description:** Single book selector
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Print one book, or a range of its chapters.

**Explanation:**

Prints one book, or a range of chapters in one book (with **From Chapter** and **To**).

*(Internal ID: `r_book_single` · Config key: `project/bookscope=single`)*

#### Use 3-letter USFM book codes (e.g. JHN, not John; MRK, not M...

- **Where:** Basic tab › What to Print
- **Type:** Drop-down list
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Use 3-letter USFM book codes (e.g. JHN, not John; MRK, not Mark).
>
> A list of references can be entered if printing less than an entire book or chapter, or if you need to include portions from several books. For example:  
>   JHN 2:1-12  
>   MRK 1-5  
>   PSA 23; 100; 117  
>   EXO 20:12-17 MAT 5:3-11  
>   GEN 1:1-2:3 PSA 23:1-end LUK 15:11-32 GLO  
>   GEN 24:1-17; 24:22-30  
>   MAT-REV
>
> If working on several books, use the Select Multiple Books... button to select them. For example:  
>   LUK ACT GLO NDX prints Luke, Acts, Glossary and Names Index. The list is editable, so books can be re-ordered if need be (for example, for the Hebrew canon).
>
> Shortcut: Ctrl-B

**Explanation:**

The list of books or passages to print with **Portions or Multiple Books**. Separate items with spaces. You can type references with chapters and verses, ranges of books (`MAT-REV`) and lists (`PSA 23; 100; 117`). The order you type is the order of printing, so you can change the order of books if needed. The drop-down remembers your recent lists. Shortcut: **Ctrl+B**.

*(Internal ID: `ecb_booklist` · Config key: `project/booklist`, `document/subject`)*

#### Multiple books editable list entry

- **Where:** Basic tab › What to Print
- **Type:** Text box
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Use 3-letter USFM book codes (e.g. JHN, not John; MRK, not Mark).
>
> A list of references can be entered if printing less than an entire book or chapter, or if you need to include portions from several books. For example:  
>   JHN 2:1-12  
>   MRK 1-5  
>   PSA 23; 100; 117  
>   EXO 20:12-17 MAT 5:3-11  
>   GEN 1:1-2:3 PSA 23:1-end LUK 15:11-32 GLO  
>   GEN 24:1-17; 24:22-30  
>   MAT-REV
>
> If working on several books, use the Select Multiple Books... button to select them. For example:  
>   LUK ACT GLO NDX prints Luke, Acts, Glossary and Names Index. The list is editable, so books can be re-ordered if need be (for example, for the Hebrew canon).
>
> Shortcut: Ctrl-B

#### From Chapter

- **Where:** Basic tab › What to Print
- **Type:** Text box
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> If you want to print less than the entire book, enter the chapter number to start at.

**Explanation:**

The first chapter to print in **Single Book** mode. Only numbers are allowed. If you type a number below 1 or above the last chapter, PTXprint corrects it. Typing here selects **Single Book**.

*(Internal ID: `t_chapfrom` · Config key: `document/chapfrom`)*

#### To

- **Where:** Basic tab › What to Print
- **Type:** Text box
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> If you want to print less than the entire book, enter the chapter number to end with.

**Explanation:**

The last chapter to print in **Single Book** mode. PTXprint corrects numbers that are too high or lower than **From Chapter**. Typing here selects **Single Book**.

*(Internal ID: `t_chapto` · Config key: `document/chapto`)*

#### Choose...

- **Where:** Basic tab › What to Print
- **Type:** Button
- **Description:** Bible module chooser button
- **View level:** Basic, Default and Full views

**Explanation:**

Opens a file chooser (in the project's `Modules` folder) to select the module .sfm file. The file name is then shown next to the button and **Bible Module** is selected. If you cancel, PTXprint changes back to **Single Book**. Shortcut: **Alt+O**.

*(Internal ID: `btn_chooseBibleModule` · Config key: `project/modulefile`)*

#### Edit...

- **Where:** Basic tab › What to Print
- **Type:** Button
- **Description:** Edit Bible module
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Switch to the View+Edit tab to show the selected Bible module.

**Explanation:**

Opens the selected module file on the **View+Edit** tab, so you can look at it or change it. Only works after you have chosen a module. Only shown in the **Default** and **Full** views.

*(Internal ID: `btn_editModule`)*
