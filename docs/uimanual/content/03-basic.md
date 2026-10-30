## What this tab is for

The **Basic** tab is the first tab in PTXprint. You come here to:

* choose the **project** (the Paratext project with the Scripture text),
* choose, save, lock, copy or delete a **configuration** (a named set of settings),
* choose **what to print** – one book, part of a book, several books, or a Bible module,
* check the **copyright and license** statement for the publication.

Start here every time. Most other settings depend on the project and configuration that you choose here.

## Project

Choose your Paratext project in the **Project** list. PTXprint shows the full name of the project next to the list.

* When you change to another project, PTXprint first saves the current configuration. Then it opens the configuration that you last used with the new project (or **Default**).
* The last item in the **Project** list is a blue **Import...** item. It opens the **Import Scripture...** dialog. Use it when you have a Scripture text bundle (a .zip file) but not a Paratext project, or to install the sample text (the Berean Standard Bible).

### Copyright & Licensing

(Regular and Full views.) Click **Copyright & Licensing** to open the area. It has two parts:

* **Copyright** – the copyright statement. PTXprint fills it in from the Paratext project settings. You can change it here. Click **Reload copyright from Paratext project** to get the Paratext text back.
* **License** – choose one of the Creative Commons licenses, **All Rights Reserved**, or type your own license.

PTXprint puts these texts into the front matter (for example on the back of the title page) through the variables `\zcopyright` and `\zlicense`. Special codes work in both boxes: `(c)` becomes ©, `(r)` becomes ®, `(tm)` becomes ™, `~` is a non-breaking space, and `//` forces a new line.

## Layout Configuration

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

## What to Print

Choose one of three ways to say what goes into the PDF:

* **Single Book** – choose one book in the list. To print only part of the book, type chapter numbers in **From Chapter** and **To**. When you choose a new book, PTXprint sets the chapters to the whole book.
* **Portions or Multiple Books** – click **Select Multiple Books...** to choose books by clicking them, or type a list in the box. You can type book codes (`MAT MRK LUK JHN`), book ranges (`MAT-REV`) and references (`JHN 2:1-12`, `PSA 23; 100; 117`, `GEN 1:1-2:3`). Use the 3-letter USFM codes (for example `JHN`, not `John`). Press **Ctrl+B** to jump to this box.
* **Bible Module** – print a Paratext module (a .sfm file that lists passages to include). Click **Choose...** to select the module file. Click **Edit...** to see it on the **View+Edit** tab. (Bible Module: Basic, Regular and Full views; **Edit...**: Regular and Full.)

If you type in **From Chapter** or **To**, PTXprint changes to **Single Book**. If you type in the book list, PTXprint changes to **Portions or Multiple Books**.

The FRT (front matter) book is not in the book lists. Set up the front matter on the **Peripherals** tab instead.

## Dialogs on this tab

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

## Common tasks

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

## Common problems

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

## Control notes

### @btn_dbl_ok
Installs the bundle chosen with **Locate...**, using the name in **Assign a Name for the Project**, and opens the new project. Greyed out until the name is valid and not already used.

### @btn_dbl_cancel
Closes the dialog without installing anything. PTXprint goes back to the project that was open before.

### @btn_locateDBLbundle
Opens a file chooser in the `Bundles` folder of your Paratext projects folder. PTXprint then shows the file name and suggests a project name from the bundle (adding a number if that name is already used). Shortcut: **Alt+O**.

### @t_DBLprojName
PTXprint suggests a name from the bundle. Use no spaces or special characters. A message appears below the box if the name cannot be used.

### @lb_DBLdownloads
Opens the Digital Bible Library website in your browser.

### @lb_openBible
Opens the Open.Bible website in your browser. Its bundles are openly licensed.

### @btn_cfg_ok
Creates the new configuration, saves it, and changes to it. Greyed out until the name is valid.

### @btn_cfg_cancel
Closes the dialog. No new configuration is made.

### @t_configName
Use a short, clear name such as `NT_A5` or `Draft_2col`. Letters with accents are not allowed. The message below the box says if the name is not valid or already exists. Write longer descriptions in **Notes** on the Basic tab.

### @btn_mbs_ok
Puts the selected books in the book list, in normal Bible order. PTXprint changes to **Portions or Multiple Books** if any books are selected.

### @btn_mbs_cancel
Closes the book selector without changing the book list.

### @btn_mps_ok
Copies the current configuration to all selected projects, using the option you chose. The copy uses the saved files, so click **Save** in the main window before you open this dialog.

### @btn_mps_cancel
Closes the dialog. Nothing is copied.

### @ecb_mpsTargets
You can also type project names here, separated by spaces. PTXprint remembers your last 10 selections, which helps when you copy to the same group of projects again and again.

### @r_copyConfig_noReplace
Projects that already have a configuration with this name are left unchanged. The safest choice.

### @r_copyConfig_merge
Settings not changed in the target are updated from this project.

### @r_copyConfig_overwrite
Use it when this project is the "master" layout for a group of projects.

### @btn_pw_ok
Locks the configuration with the password you typed, or unlocks it if the password matches. If the configuration is not locked and the box is empty, nothing is locked and PTXprint asks for a password. If the password is wrong, the configuration stays locked and the status line says so.

### @btn_pw_cancel
Closes the dialog. Nothing is locked or unlocked, and the password box is cleared.

### @t_password
PTXprint stores only a coded form of the password. If you forget it, you cannot unlock the configuration in PTXprint, so keep it somewhere safe.

### @fcb_project
When you change the project, PTXprint saves the current configuration first and opens the last configuration you used with the new project. The last item, **Import...** (in blue), opens the **Import Scripture...** dialog.

### @ecb_licenseText
Used in the front matter through `\zlicense`. Ask your organization which license to use.

### @textv_copyright
PTXprint fills it from the Paratext project settings when it is empty. `(c)`, `(r)` and `(tm)` change to ©, ® or ™ as you type. Used in the front matter through `\zcopyright`.

### @btn_resetCopyright
If Paratext has no copyright statement, PTXprint shows a message in the status line.

### @t_configNotes
For example "A5 NT for village distribution, 2 columns". Saved with the configuration, so other team members see it after Send/Receive. Greyed out when the configuration is locked.

### @t_invisiblePassword
Empty when the configuration is not locked. You cannot type here; use the lock button.

### @btn_lockunlock
Opens the **Lock/Unlock Configuration** dialog. The icon shows whether the configuration is locked.

### @btn_copyToTargetProj
Opens the **Copy Configuration To...** dialog. Greyed out when **Default** is selected (hold the mouse over the button to see why).

### @ecb_savedConfig
Choose a configuration to load its settings. Click **Save** first.

### @t_savedConfig
The text part of the configuration **Name** box. Type a new name and click **Save** to create a new configuration from the current settings. Characters that are not allowed (such as spaces) are removed.

### @btn_deleteConfig
Deletes the selected configuration after you click **Yes** in the **Please Confirm...** dialog. The dialog names the configuration, so check the name. PTXprint first changes to the **Default** configuration, then deletes the settings and working files of the old one. Other configurations are not touched. This cannot be undone. If some files cannot be deleted (for example because they are open in another program), the status line lists them. For the **Default** configuration you see **Reset** instead. Greyed out when the configuration is locked, and in the **Mini** view.

### @btn_resetDefaults
Only shown when the **Default** configuration is selected. PDF files are kept. The status line confirms when the reset is done. Use it only when you really want to start again. Greyed out in the **Mini** and **Basic** views.

### @btn_importSettings
In the dialog you also choose which groups of settings to bring in. See the chapter "Importing settings".

### @ecb_book
Used when **Single Book** is selected. When you choose a book, PTXprint sets **From Chapter** to 1 and **To** to the last chapter of that book, and changes to **Single Book**.

### @btn_chooseBooks
Opens the **Select Books To Export to PDF** dialog. Shortcut: **Alt+O**.

### @r_book_module
The module file is usually in the project's `Modules` folder. Choose it with **Choose...**.

### @r_book_multiple
Use it for several books, a range such as `MAT-REV`, or selected passages such as `PSA 23; 100`. PTXprint changes to this option when you type in the book list or pick books with **Select Multiple Books...**.

### @r_book_single
Use **From Chapter** and **To** for a range of chapters.

### @ecb_booklist
Separate items with spaces. Books print in the order you type. The drop-down remembers your recent lists.

### @t_chapfrom
Only numbers are allowed. If you type a number below 1 or above the last chapter, PTXprint corrects it. Typing here selects **Single Book**.

### @t_chapto
PTXprint corrects numbers that are too high or lower than **From Chapter**. Typing here selects **Single Book**.

### @btn_chooseBibleModule
Opens a file chooser (in the project's `Modules` folder) to select the module .sfm file. The file name is then shown next to the button and **Bible Module** is selected. If you cancel, PTXprint changes back to **Single Book**. Shortcut: **Alt+O**.

### @btn_editModule
Only works after you have chosen a module. You can look at the module there or change it.

### @b_saveAsNewConfig
Opens the **Save Current Configuration As...** dialog. The new configuration starts with the current settings, including unsaved changes. Use it to start a new publication from an existing one, or to make an unlocked copy of a locked configuration.

### @c_overwriteConfig
Leave it unticked in normal use; then PTXprint does not accept a name that already exists. When ticked, the old configuration is deleted when you click **OK**, and this cannot be undone. If you type the name of the configuration that you are in, PTXprint makes it again from the configuration it was first copied from (if PTXprint knows it), or else just saves it.

### @c_copyConfig_skipVars
The variables are listed on the **Peripherals** tab. After the copy, fill them in on each target project that did not have this configuration before.

### @b_installBSB
Installs the BSB as a project called `BSB` in your projects folder, opens it and closes the dialog. No internet is needed. Use it to practise, to try out settings, or as the second text in a diglot.

### @btn_runTutorial
Opens a file chooser for the tutorial file, then a small tutorial window. The steps really change the settings, so use a practice configuration. See "Run a tutorial" in this chapter.

### @b_mbsAll
If all books are already selected, it unselects them all.

### @b_mbsOT
If they are all selected already, it unselects them. Other books are not changed.

### @b_mbsNT
If they are all selected already, it unselects them. Other books are not changed.

### @b_mbsDC
If they are all selected already, it unselects them. Other books are not changed.

### @b_mbsXtra
Extra books are for example the glossary (GLO), the indexes (TDX, NDX) and XXA–XXG. If they are all selected already, it unselects them. Other books are not changed.

### @b_mbsToggle
For example, click **New Testament** and then **Toggle Books** to select everything except the New Testament.

### @b_mbsNone
Use it to start your selection again.
