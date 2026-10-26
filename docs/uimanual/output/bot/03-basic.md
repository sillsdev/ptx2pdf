# 4. Basic tab

## 4.1 What this tab is for

The **Basic** tab is the first tab in PTXprint. You come here to:

* choose the **project** (the Paratext project with the Scripture text),
* choose, save, lock, copy or delete a **configuration** (a named set of settings),
* choose **what to print** – one book, part of a book, several books, or a Bible module,
* check the **copyright and license** statement for the publication.

Start here every time. Most other settings depend on the project and configuration that you choose here.

## 4.2 Project

Choose your Paratext project in the **Project** list. PTXprint shows the full name of the project next to the list.

* When you change to another project, PTXprint first saves the current configuration. Then it opens the configuration that you last used with the new project (or **Default**).
* The last item in the **Project** list is a blue **Import...** item. It opens the **Import Scripture...** dialog. Use it when you have a Scripture text bundle (a .zip file) but not a Paratext project, or to install the sample text (the Berean Standard Bible).

### Copyright & Licensing

(Regular and Full views.) Click **Copyright & Licensing** to open the area. It has two parts:

* **Copyright** – the copyright statement. PTXprint fills it in from the Paratext project settings. You can change it here. Click **Reload copyright from Paratext project** to get the Paratext text back.
* **License** – choose one of the Creative Commons licenses, **All Rights Reserved**, or type your own license.

PTXprint puts these texts into the front matter (for example on the back of the title page) through the variables `\zcopyright` and `\zlicense`. Special codes work in both boxes: `(c)` becomes ©, `(r)` becomes ®, `(tm)` becomes ™, `~` is a non-breaking space, and `//` forces a new line.

## 4.3 Layout Configuration

A **configuration** (or layout) is a named set of settings. One project can have many configurations, for example one for a draft and one for the final book. See the chapter about the main window for more about configurations and saving.

* **Name** – the list of saved configurations. Choose one to load its settings. Or type a new name here and click **Save** to make a new configuration. Use only the letters a–z and A–Z, numbers, brackets `( )`, underscores `_` and hyphens `-`. No spaces.
* The **Save As** button (an icon next to the name) opens the **Save Current Configuration As...** dialog.
* The **lock** button locks or unlocks the configuration with a password.
* The **Copy configuration to other projects** button opens the **Copy Configuration To...** dialog. (Regular and Full views.) It is greyed out for the **Default** configuration, because **Default** is never copied to other projects.
* **Delete** removes the selected configuration. For the **Default** configuration, this button is replaced by **Reset**.
* **Import Settings...** opens the **Import Settings** dialog, to bring in settings from a PDF, a ZIP archive, or another configuration. See the chapter "Importing settings". (Basic, Regular and Full views.)
* **Run Tutorial...** steps through a tutorial file on the current project and configuration. See "Run a tutorial" below. (Basic, Regular and Full views.)
* **Notes** – an optional description of the configuration, for you and your team. (Basic, Regular and Full views.)

When you choose another configuration in the **Name** list, PTXprint does **not** save the current one. Click **Save** first.

## 4.4 What to Print

Choose one of three ways to say what goes into the PDF:

* **Single Book** – choose one book in the list. To print only part of the book, type chapter numbers in **From Chapter** and **To**. When you choose a new book, PTXprint sets the chapters to the whole book.
* **Portions or Multiple Books** – click **Select Multiple Books...** to choose books by clicking them, or type a list in the box. You can type book codes (`MAT MRK LUK JHN`), book ranges (`MAT-REV`) and references (`JHN 2:1-12`, `PSA 23; 100; 117`, `GEN 1:1-2:3`). Use the 3-letter USFM codes (for example `JHN`, not `John`). Press **Ctrl+B** to jump to this box.
* **Bible Module** – print a Paratext module (a .sfm file that lists passages to include). Click **Choose...** to select the module file. Click **Edit...** to see it on the **View+Edit** tab. (Bible Module: Basic, Regular and Full views; **Edit...**: Regular and Full.)

If you type in **From Chapter** or **To**, PTXprint changes to **Single Book**. If you type in the book list, PTXprint changes to **Portions or Multiple Books**.

The FRT (front matter) book is not in the book lists. Set up the front matter on the **Peripherals** tab instead.

## 4.5 Dialogs on this tab

### Save Current Configuration As...

Opens when you click the **Save As** button. Type a name in **Configuration Name** and click **OK**. PTXprint makes a new configuration with a copy of the current settings, saves it, and changes to it. **OK** stays greyed out until the name is valid. A message below the box says if the name has spaces or special characters, or if a configuration with that name already exists.

If the name already exists, you can tick **Replace it if it already exists**. Then PTXprint deletes the old configuration and saves the current settings in its place. The **Default** configuration can never be replaced. The box is unticked each time the dialog opens, so you must choose to replace each time.

Tip: Click **Save** before **Save As...**, so that the new configuration starts from your latest settings.

### Lock/Unlock Configuration

Opens when you click the **lock** button. Locking protects a configuration so that nobody changes or deletes it by mistake.

* **To lock:** type a password (up to 16 characters) and click **OK**. PTXprint saves the configuration and then locks it. The lock icon changes, and dots appear in the box next to the name.
* **To unlock:** click the lock button again, type the same password, and click **OK**. If the password is wrong, the configuration stays locked and the status line says "Incorrect password".
* You must type a password to lock. If the box is empty, PTXprint does not lock the configuration and asks you for a password.
* **Cancel** (or closing the dialog) never locks or unlocks anything.
* While a configuration is locked, **Save**, **Delete** and **Notes** are greyed out, and PTXprint does not save changes (not even when you print). You can still try out settings and print, but the changes are not kept.
* You cannot lock the **Default** configuration.

### Copy Configuration To...

Opens when you click the **Copy configuration to other projects** button. Use it when several projects need the same layout (for example, a series of New Testaments in related languages).

1. Click the projects that should receive a copy of the current configuration. The current project is shown in black and cannot be chosen. The **Recent** list at the bottom shows your selection, and remembers your last 10 selections.
2. Choose what to do if a target project already has a configuration with the same name:
   * **Do NOT Replace Existing Config** – skip those projects. Use this the first time you copy.
   * **Merge Configurations From Both** – combine the two. Settings that were changed in the target project since the first copy are kept.
   * **Overwrite With Recent Changes** – settings that were changed in this (source) project replace the target settings.
3. Leave **Keep each project's own language-specific variables** ticked (the normal choice), so that each target project keeps its own titles and language name. Untick it only if the target projects should get the same values as this project.
4. Click **OK**.

The **Default** configuration is never copied, and the button is greyed out while **Default** is selected. Use **Save As** to give the configuration a name first.

PTXprint copies the saved files of the configuration: the settings, the styles, the changes and TeX files, and the front matter. Adjust lists (paragraph adjustments) are not copied, because they belong to one text. Click **Save** before you copy, so that the copy has your latest settings.

### Select Books To Export to PDF

Opens when you click **Select Multiple Books...**. Each book in the project is a button. Click a button to select or unselect that book. Hold **Shift** and click another book to select or unselect all books between the two. The buttons at the side select groups: **All Books**, **Old Testament**, **New Testament**, **Deuterocanon**, **Extra Material**, **Toggle Books** (reverse the selection), and **Reset All** (unselect all). A group button selects all books of that group. If they are all selected already, it unselects them. Click **OK**. PTXprint puts the books in the book list in normal Bible order. You can then change the order by typing in the list.

### Import Scripture...

Opens when you choose **Import...** at the end of the **Project** list. There are two ways to get a text:

* **Install BSB** – installs the Berean Standard Bible that comes with PTXprint. It is good for practice and as a second text in a diglot.
* **Step 1 – Step 3** – install a Scripture text bundle (.zip):
  1. Download a bundle from the **Primary DBL site** (Digital Bible Library – you must log in) or the **Open.Bible site**. Choose a bundle that has the text (not only audio). The USX format is best.
  2. Click **Locate...** and choose the .zip file.
  3. Check the project name in **Assign a Name for the Project** and click **OK**.

PTXprint creates the new project in a folder called `_PTXprint` inside your Paratext projects folder, and opens it.

### Please Confirm...

PTXprint asks you to confirm before something that cannot be undone:

* **"You are about to REMOVE the '...' configuration"** – appears when you click **Delete**. It names the configuration. Click **Yes** to delete it, or **No** to keep it. Its settings and working files are deleted. PDF files that you made from it are **not** deleted.
* **"You are about to CREATE a diglot (or polyglot) configuration"** – appears when you turn on a diglot. PTXprint suggests that you first use **Save As...** to make a new configuration for the diglot.

## 4.6 Common tasks

### Start a new publication from an existing configuration

1. In **Project**, choose the project.
2. In **Name**, choose the configuration that is closest to what you want.
3. Click **Save** (so that the latest settings are on disk).
4. Click the **Save As** button. Type a new name (for example `NT_A5`) and click **OK**.
5. Now change the settings. The old configuration stays as it was.

### Print one book, or part of a book

1. Click **Single Book** and choose the book in the list.
2. To print only some chapters, type the first chapter in **From Chapter** and the last chapter in **To**.
3. Click **Print (Make PDF)**.

### Print several books, or selected passages

1. Click **Select Multiple Books...**, click the books you want (or click **New Testament**), then click **OK**.
2. Or type in the book list, for example `MAT-ACT` or `PSA 23; 100; 117 LUK 15:11-32`.
3. Click **Print (Make PDF)**.

### Protect a finished configuration

1. Choose the configuration in **Name** (not **Default**).
2. Click the **lock** button.
3. Type a password and click **OK**. Remember the password.

### Use the same layout for another project

1. Click **Save**.
2. Click the **Copy configuration to other projects** button. (Regular or Full view. The configuration must not be **Default**.)
3. Click the target project(s).
4. Choose **Do NOT Replace Existing Config**, leave **Keep each project's own language-specific variables** ticked, and click **OK**.
5. In **Project**, choose the target project and check the copied configuration.

### Set or correct the copyright statement

1. Change to the **Regular** or **Full** view if needed.
2. Click **Copyright & Licensing** to open it.
3. Type the copyright text (type `(c)` for ©), or click **Reload copyright from Paratext project**.
4. Choose or type the **License**.

### Get a text to practise with

1. Open the **Project** list and choose **Import...** (the last item).
2. Click **Install BSB**. PTXprint installs and opens the BSB project.

### Delete a configuration that you do not need

1. Choose it in **Name**.
2. Click **Delete**. Check that the message names the right configuration, then click **Yes**.
3. PTXprint changes to the **Default** configuration and deletes the settings and working files of the old one. The PDF files that you made from it stay in the output folder.

### Run a tutorial

A tutorial is a file with a list of steps (a .json file, or a recorded test in a .zip file). You may get one from a trainer.

1. Choose the project and configuration to practise on. The tutorial makes its changes there, so use a practice configuration (for example make one with **Save As**).
2. Click **Run Tutorial...** and choose the tutorial file.
3. A small tutorial window opens. It shows the next step, and PTXprint highlights the control that the step uses.
4. Click **Step** (or press **Space**) to do the next step, **Skip** (or **S**) to leave it out, or **Play** (or **P**) to do the steps one after another. **Run to end** does all the remaining steps.
5. Close the tutorial window to stop. If the tutorial needed a higher view level, PTXprint changes the view level while it runs and changes it back when you close the window.

## 4.7 Common problems

### My recent changes were lost when I chose another configuration

**Cause:** Choosing another configuration in the **Name** list does not save the current one. **What to do:** Always click **Save** before you change configurations.

### The lock button is greyed out

**Cause:** The **Default** configuration cannot be locked. **What to do:** Use **Save As** to make a named configuration, then lock that one.

### I cannot save, and Delete and Notes are greyed out

**Cause:** The configuration is locked. **What to do:** Click the lock button and enter the password, or use **Save As** to make a new, unlocked copy.

### There is a Reset button instead of Delete

**Cause:** The **Default** configuration is selected. It cannot be deleted, so **Reset** is shown instead. Be careful: **Reset** asks no question. It at once sets all settings of the Default configuration back to the PTXprint defaults, and deletes the files in the Default configuration folder. Other configurations are not changed.

### The OK button in "Save Current Configuration As..." is greyed out

**Cause:** The name is empty, has spaces or special characters, or is already used. **What to do:** Read the message below the box. Use only letters a–z and A–Z, numbers, `(`, `)`, `_` and `-`.

### PTXprint says "Unknown book code"

**Cause:** The book list has a word that is not a 3-letter USFM book code (for example `John`). **What to do:** Use the codes, for example `JHN`, `MAT`, `1CO`.

### I cannot find the FRT book in the list

**Cause:** PTXprint does not list FRT as a book. **What to do:** Set up front matter on the **Peripherals** tab.

### The Primary DBL site and Open.Bible site links do not work

**Cause:** **Disable ALL Internet Use** is ticked on the **Advanced** tab. **What to do:** Untick it, or download the bundle another way and use **Locate...**.

### Copyright & Licensing or Copy configuration are missing, or Reset is greyed out

**Cause:** They are only available in the **Regular** and **Full** views. **What to do:** Click **☰** › **View Level** › **Regular View**.

### The Copy configuration to other projects button is greyed out

**Cause:** The **Default** configuration is selected. PTXprint never copies **Default** to other projects. **What to do:** Use **Save As** to save the settings under another name, then copy that configuration.

## 4.8 Settings reference

### Import Scripture... (dialog)

#### OK

Button · Regular+ · `btn_dbl_ok`

Installs the bundle chosen with **Locate...**, using the name in **Assign a Name for the Project**, and opens the new project. Greyed out until the name is valid and not already used.

#### Cancel

Button · Regular+ · `btn_dbl_cancel`

Closes the dialog without installing anything. PTXprint goes back to the project that was open before.

#### Install BSB

Button · Mini+ · `b_installBSB`

> The Berean Standard Bible is a Public Domain English Bible. It is bundled with PTXprint but needs to be installed in your Projects folder.
>
> This is a good training project and can also be used in diglots.

Installs the BSB as a project called `BSB` in your projects folder, opens it and closes the dialog. No internet is needed. Use it to practise, to try out settings, or as the second text in a diglot.

#### Locate...

Button · Basic+ · `btn_locateDBLbundle`  
Also: Locate DBL bundle

> After downloading a scripture text bundle (.zip) file you need to tell PTXprint where the .zip file is located so that it can install it as a special resource project.

Opens a file chooser in the `Bundles` folder of your Paratext projects folder. PTXprint then shows the file name and suggests a project name from the bundle (adding a number if that name is already used). Shortcut: **Alt+O**.

#### Step 3 Assign a Name for the Project – Assign a name to a DBL bundle

Text box · Basic+ · `t_DBLprojName`

> PTXprint will create this project within a subfolder called '_PTXprint'. Use a short name (8 characters or fewer is best) for the new project. Do not use the name of an existing Project.

PTXprint suggests a name from the bundle. Use no spaces or special characters. A message appears below the box if the name cannot be used.

#### Primary DBL site

Link · Basic+ · `lb_DBLdownloads`  
Also: Visit the Digital Bible Library to download a DBL Scripture bundle

> There are hundreds of Scripture bundles available at the Digital Bible Library website which you may download and use in a publication. You must log in to the site in order to access resources.
>
> Use resources which contain the text (not just the audio) and preferably select the USX download option.
>
> Note: If this option is disabled, it is due to the "Disable ALL Internet Use" option which has been set on the General section of the Advanced tab.

Opens the Digital Bible Library website in your browser.

#### Open.Bible site

Link · Basic+ · `lb_openBible`  
Also: Visit the Open.Bible site to download a Scripture bundle

> There are hundreds of Scripture bundles at the Open.Bible website which you may download and use in a publication.
>
> Use resources which contain the text (not just the audio) and preferably select the USX download option.
>
> Note: If this option is disabled, it is due to the "Disable ALL Internet Use" option which has been set on the General section of the Advanced tab.
>
> If you don't already have a Scripture Text Bundle, then you can download a USX or USFM text bundle from an online scripture repository.

Opens the Open.Bible website in your browser. Its bundles are openly licensed.

### Save Current Configuration As... (dialog)

#### OK

Button · Basic+ · `btn_cfg_ok`

Creates the new configuration, saves it, and changes to it. Greyed out until the name is valid.

#### Cancel

Button · Basic+ · `btn_cfg_cancel`

Closes the dialog. No new configuration is made.

#### Configuration Name – Enter a name for the configuration to be saved

Text box · Basic+ · `t_configName`

> Enter a name for the configuration to be saved.
>
> Note that only Roman/Latin names are supported using: a-z A-Z, 0-9, parentheses, underscores and hyphens. Spaces are not permitted.

Use a short, clear name such as `NT_A5` or `Draft_2col`. Letters with accents are not allowed. The message below the box says if the name is not valid or already exists. Write longer descriptions in **Notes** on the Basic tab.

#### Replace it if it already exists

Checkbox, off · Basic+ · `c_overwriteConfig`

> If a configuration with this name already exists, delete it and save the current settings in its place. (Useful for tests and tutorials that make a fresh copy each time they run.)

Leave it unticked in normal use; then PTXprint does not accept a name that already exists. When ticked, the old configuration is deleted when you click **OK**, and this cannot be undone. If you type the name of the configuration that you are in, PTXprint makes it again from the configuration it was first copied from (if PTXprint knows it), or else just saves it.

### Select Books To Export to PDF (dialog)

#### OK

Button · Regular+ · `btn_mbs_ok`

Puts the selected books in the book list, in normal Bible order. PTXprint changes to **Portions or Multiple Books** if any books are selected.

#### Cancel

Button · Regular+ · `btn_mbs_cancel`

Closes the book selector without changing the book list.

#### All Books

Button · Mini+ · `b_mbsAll`

> Click to turn ALL books on/off.

If all books are already selected, it unselects them all.

#### Old Testament

Button · Mini+ · `b_mbsOT`

> Click to turn OT books on/off.

If they are all selected already, it unselects them. Other books are not changed.

#### New Testament

Button · Mini+ · `b_mbsNT`

> Click to turn NT books on/off.

If they are all selected already, it unselects them. Other books are not changed.

#### Deuterocanon

Button · Mini+ · `b_mbsDC`

> Click to turn DC books on/off.

If they are all selected already, it unselects them. Other books are not changed.

#### Extra Material

Button · Mini+ · `b_mbsXtra`

> Click to turn Extra books on/off.

Extra books are for example the glossary (GLO), the indexes (TDX, NDX) and XXA–XXG. If they are all selected already, it unselects them. Other books are not changed.

#### Toggle Books

Button · Mini+ · `b_mbsToggle`

> Click to toggle ALL books. Those which are selected will be deselected, and the unselected ones will be selected.

For example, click **New Testament** and then **Toggle Books** to select everything except the New Testament.

#### Reset All

Button · Mini+ · `b_mbsNone`

> Click to turn OFF all books.

Use it to start your selection again.

#### Why is FRT not listed?

Label · Mini+

> The FRT book in Paratext contains front matter for a publication. Visit the Peripherals page to set up front matter for this publication.

### Copy Configuration To... (dialog)

#### OK

Button · Regular+ · `btn_mps_ok`

Copies the current configuration to all selected projects, using the option you chose. The copy uses the saved files, so click **Save** in the main window before you open this dialog.

#### Cancel

Button · Regular+ · `btn_mps_cancel`

Closes the dialog. Nothing is copied.

#### Recent

Drop-down · Regular+ · `ecb_mpsTargets`

> Shows selected target projects. Pick a previous selection from the dropdown, or select projects in the grid above.

You can also type project names here, separated by spaces. PTXprint remembers your last 10 selections, which helps when you copy to the same group of projects again and again.

#### Do NOT Replace Existing Config

Radio · Regular+ · `r_copyConfig_noReplace`  
Also: Copy Config: Do NOT Replace Existing Config

> Selecting this option will prevent any changes overwriting an existing configuration of the same name in the target project(s).
>
> This option is usually used when copying a configuration to other projects for the first time.

Projects that already have a configuration with this name are left unchanged. The safest choice.

#### Merge Configurations From Both

Radio · Regular+ · `r_copyConfig_merge`  
Also: Copy Config: MERGE Configurations From Both

> Selecting this option will MERGE the settings from the source configuration with the identically named configuration in the target project. Any changes that were made to the target project's configuration since it was first shared will be kept (i.e. modified target settings are retained if there is a clash of settings).

Settings not changed in the target are updated from this project.

#### Overwrite With Recent Changes

Radio · Regular+ · `r_copyConfig_overwrite`  
Also: Copy Config: OVERWRITE With Recent Changes

> Selecting this option will REPLACE (or overwrite) any settings in the identically named configuration in the target project IF those settings were changed in the source project since the configuration was first shared. (i.e. if both source and target projects modified a setting, then the source project's setting will "win").

Use it when this project is the "master" layout for a group of projects.

#### Keep each project's own language-specific variables

Checkbox, on · Regular+ · `c_copyConfig_skipVars`  
Also: Copy Config: Keep target project's own variables

> When checked, the variable values (such as the main title, subtitle and language name, and the Strong's index titles) are NOT copied, so each target project keeps its own. A configuration that is new to a target project starts without them, rather than with the source project's values.
>
> Uncheck this to copy these values as well.

The variables are listed on the **Peripherals** tab. After the copy, fill them in on each target project that did not have this configuration before.

### Lock/Unlock Configuration (dialog)

#### OK

Button · Regular+ · `btn_pw_ok`

Locks the configuration with the password you typed, or unlocks it if the password matches. If the configuration is not locked and the box is empty, nothing is locked and PTXprint asks for a password. If the password is wrong, the configuration stays locked and the status line says so.

#### Cancel

Button · Regular+ · `btn_pw_cancel`

Closes the dialog. Nothing is locked or unlocked, and the password box is cleared.

#### Enter Password – Enter password for config

Text box · Mini+ · `t_password`

> Enter a password of up to 16 characters to lock/unlock this saved configuration.

PTXprint stores only a coded form of the password. If you forget it, you cannot unlock the configuration in PTXprint, so keep it somewhere safe.

### Basic

#### Layout Configuration

Label · Mini+

> A Layout (or Config) is a collection of settings that can be saved. By naming and saving a layout you can recall those settings later.

#### Project

##### Project ID – Paratext project code

Drop-down · Mini+ · `fcb_project`  
Choices: Unknown

When you change the project, PTXprint saves the current configuration first and opens the last configuration you used with the new project. The last item, **Import...** (in blue), opens the **Import Scripture...** dialog.

##### Copyright & Licensing

Label · Regular+

> It is important to include copyright and license statements on every publication. By default this will be set according to the Paratext project settings, but you can edit it here if needed by expanding the section below.

##### Copyright & Licensing

###### Copyright

Label · Regular+

> It is important to include a copyright statement on every publication. By default this will be set according to the Paratext project settings, but you can edit it here if needed.

###### License – License details

Drop-down · Regular+ · `ecb_licenseText` · cfg `project/license`  
Choices: This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND). | This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC). | This work is licensed under a Creative Commons Attribution-Sharealike 4.0 International License (CC BY-SA). | This work is licensed under a Creative Commons Attribution 4.0 International License (CC BY). | All Rights Reserved.

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

Used in the front matter through `\zlicense`. Ask your organization which license to use.

###### Copyright text entry

Text area · Regular+ · `textv_copyright`

> It is important to include a copyright statement on every publication. Note: There are several shortcuts you can use:  
>    (c) --> ©  the copyright sign  
>    (r) --> ®  to denote registered trademarks  
>    (tm) --> ™  to denote trademarks in general
>
> Other special codes converted at print time:  
> Use ~ where a non-breaking space is needed. Use // to force a line break (:// in URLs is not changed).

PTXprint fills it from the Paratext project settings when it is empty. `(c)`, `(r)` and `(tm)` change to ©, ® or ™ as you type. Used in the front matter through `\zcopyright`.

###### Reload copyright from Paratext project

Button · Regular+ · `btn_resetCopyright`

> Clicking this button will reload the Copyright Statement from the Paratext project settings.

If Paratext has no copyright statement, PTXprint shows a message in the status line.

#### Layout Configuration

##### Notes – (Optional) Notes about configuration

Text box · Basic+ · `t_configNotes` · cfg `config/notes`

> Optional: Provide a description about the saved/shared configuration named above.

For example "A5 NT for village distribution, 2 columns". Saved with the configuration, so other team members see it after Send/Receive. Greyed out when the configuration is locked.

##### Name

Text box · Basic+ · `t_invisiblePassword` · cfg `config/pwd`

> Dots indicate that a password has been set for this configuration.

Empty when the configuration is not locked. You cannot type here; use the lock button.

##### Name – Lock configuration

Button · Mini+ · `btn_lockunlock`

> When Config is UNLOCKED:  
> Click to set a password to prevent anyone from accidentally changing the saved settings or deleting the configuration.
>
> When Config is LOCKED:  
> Click to enter the password to unlock this configuration and allow changes to be saved or the configuration to be deleted.
>
> Note that the Default config cannot be locked.

Opens the **Lock/Unlock Configuration** dialog. The icon shows whether the configuration is locked.

##### Name – Copy configuration to other projects

Button · Regular+ · `btn_copyToTargetProj`

> A saved configuration can be copied to other Paratext projects in order to avoid having to manually re-create all the same settings for a similar project.
>
> Save first: the saved files are copied. Adjust lists are not copied.

Opens the **Copy Configuration To...** dialog. Greyed out when **Default** is selected (hold the mouse over the button to see why).

##### Name

Drop-down · Mini+ · `ecb_savedConfig`  
Choices: Default

> Select a previously-saved layout configuration to retrieve those settings.
>
> Note: changes to the current configuration are not saved automatically when you switch. Save first to keep them.
>
> When the Paratext project is shared through Send/Recv, all saved layout configurations will also be made available to other PTXprint users of the same Paratext project.
>
> Alternatively, select a previously-saved layout configuration to retrieve settings.

Choose a configuration to load its settings. Click **Save** first.

##### Enter a name for the layout configuration to be saved.

Text box · Mini+ · `t_savedConfig`

> Enter a name for the layout configuration to be saved.
>
> Note that only Roman/Latin names are supported using: a-z A-Z, 0-9, parentheses, underscores and hyphens.
>
> Longer descriptions may be typed into the Notes field below.

The text part of the configuration **Name** box. Type a new name and click **Save** to create a new configuration from the current settings. Characters that are not allowed (such as spaces) are removed.

##### gtk-save-as

Button · Mini+ · `b_saveAsNewConfig`

> Save the current settings as a new Configuration.
>
> When the Paratext project is shared through Send/Recv, all saved configurations will be also made available to other PTXprint users of the same Paratext project.

Opens the **Save Current Configuration As...** dialog. The new configuration starts with the current settings, including unsaved changes. Use it to start a new publication from an existing one, or to make an unlocked copy of a locked configuration.

##### Delete

Button · Basic+ · `btn_deleteConfig`  
Also: Delete configuration

> Delete this Saved Configuration
>
> This also deletes the corresponding subfolder of temporary files in the local\ptxprint folder but does not delete the previously created PDF files which will remain in that folder.

Deletes the selected configuration after you click **Yes** in the **Please Confirm...** dialog. The dialog names the configuration, so check the name. PTXprint first changes to the **Default** configuration, then deletes the settings and working files of the old one. Other configurations are not touched. This cannot be undone. If some files cannot be deleted (for example because they are open in another program), the status line lists them. For the **Default** configuration you see **Reset** instead. Greyed out when the configuration is locked, and in the **Mini** view.

##### Reset

Button · Regular+ · `btn_resetDefaults`

> Reset the Default configuration to PTXprint's default settings.
>
> Warning: this also deletes the files kept in the Default configuration folder (such as styles, picture list, adjust lists and front matter). There is no confirmation.

Only shown when the **Default** configuration is selected. PDF files are kept. The status line confirms when the reset is done. Use it only when you really want to start again. Greyed out in the **Mini** and **Basic** views.

##### Name – Import settings from PDFs, ZIP files or other Configurations

Button · Basic+ · `btn_importSettings`

> Open the Import Settings dialog to select options for importing settings from other PDFs, ZIP archives, or different project configurations.
>
> By default, imported settings are applied to the current project and configuration. However, you can also choose to import them into other projects or export them to an external folder.

In the dialog you also choose which groups of settings to bring in. See the chapter "Importing settings".

##### Run Tutorial...

Button · Basic+ · `btn_runTutorial`

> Step through a tutorial on the current project and configuration: a list of actions saved as .json from the test replay window, or the actions in a recorded test (.zip).

Opens a file chooser for the tutorial file, then a small tutorial window. The steps really change the settings, so use a practice configuration. See "Run a tutorial" in this chapter.

#### What to Print

##### Single book chooser

Drop-down · Mini+ · `ecb_book` · cfg `project/book`  
Choices: NONE

Used when **Single Book** is selected. When you choose a book, PTXprint sets **From Chapter** to 1 and **To** to the last chapter of that book, and changes to **Single Book**.

##### Select Multiple Books...

Button · Mini+ · `btn_chooseBooks`  
Also: Multiple book selector

> Select one or more Biblical books to be printed from the project.

Opens the **Select Books To Export to PDF** dialog. Shortcut: **Alt+O**.

##### Bible Module

Radio · Basic+ · `r_book_module` · cfg `project/bookscope=module`  
Also: Bible module selector

> Print a Paratext Bible module (a .sfm file that lists the passages to include).

The module file is usually in the project's `Modules` folder. Choose it with **Choose...**.

##### Portions or Multiple Books

Radio · Mini+ · `r_book_multiple` · cfg `document/multibook`  
Also: Choose books or enter ranges to print

> Print several books, or the passages listed in the box.

Use it for several books, a range such as `MAT-REV`, or selected passages such as `PSA 23; 100`. PTXprint changes to this option when you type in the book list or pick books with **Select Multiple Books...**.

##### Single Book

Radio · Mini+ · `r_book_single` · cfg `project/bookscope=single`  
Also: Single book selector

> Print one book, or a range of its chapters.

Use **From Chapter** and **To** for a range of chapters.

##### Use 3-letter USFM book codes (e.g. JHN, not John; MRK, not M...

Drop-down · Mini+ · `ecb_booklist` · cfg `project/booklist`, `document/subject`

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

Separate items with spaces. Books print in the order you type. The drop-down remembers your recent lists.

##### Multiple books editable list entry

Text box · Mini+

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

##### From Chapter

Text box · Mini+ · `t_chapfrom` · cfg `document/chapfrom`

> If you want to print less than the entire book, enter the chapter number to start at.

Only numbers are allowed. If you type a number below 1 or above the last chapter, PTXprint corrects it. Typing here selects **Single Book**.

##### To

Text box · Mini+ · `t_chapto` · cfg `document/chapto`

> If you want to print less than the entire book, enter the chapter number to end with.

PTXprint corrects numbers that are too high or lower than **From Chapter**. Typing here selects **Single Book**.

##### Choose...

Button · Basic+ · `btn_chooseBibleModule` · cfg `project/modulefile`  
Also: Bible module chooser button

Opens a file chooser (in the project's `Modules` folder) to select the module .sfm file. The file name is then shown next to the button and **Bible Module** is selected. If you cancel, PTXprint changes back to **Single Book**. Shortcut: **Alt+O**.

##### Edit...

Button · Regular+ · `btn_editModule`  
Also: Edit Bible module

> Switch to the View+Edit tab to show the selected Bible module.

Only works after you have chosen a module. You can look at the module there or change it.
