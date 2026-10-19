# Help tab and getting support

## What this tab is for

The **Help** tab is where you go when you need help, or when you need to find your files. It is shown in every view level.

On this tab you can:

* see where PTXprint keeps your PDF and other files, and open those folders;
* open the documentation, training material and the user community website;
* make an **archive** (a ZIP file) of your project to send to the support team;
* make a **report** about the last PDF, with warnings and errors;
* **Tidy Up** temporary files to save disk space;
* change the **Base Projects Directory** (the folder that holds your Paratext projects);
* open the **About** window to see which version of PTXprint you have.

Many of the links on this tab open web pages. These links are only shown when internet use is allowed. If you (or your organisation) ticked **Disable ALL Internet Use** on the **Advanced** tab, the internet links and the **About** button are hidden. Untick that setting to see them again. Some items are only shown in the **Full** view; this is noted for each one.

## Links and Help

### Folders

* **Output PDF Location** – the folder where PTXprint saves the PDF files it makes. Click the blue link to open the folder.
* **Base Projects Directory** – the folder that holds all your Paratext projects. Use **Change...** to choose a different one.
* **PTXprint Program Path** (only in the **Full** view) – the folder where PTXprint itself is installed.

Everything in the output location is made again each time you print. None of it is part of Paratext Send/Receive. Your settings are kept safely in a different place, inside the project's shared folder.

### Documentation and learning

These links open web pages or documents:

* **Documentation | FAQs | Gallery | Support | Download** – the PTXprint home page. Check here for new versions. PTXprint does not update itself, so you must download new versions yourself.
* **Learn: How to...** – short articles about common tasks.
* **Training (Videos and Presentations)** – videos on the Paratext website and on Vimeo.
* **Ornaments Catalog** and **Technical Reference** (only in the **Full** view) – PDF documents that come with PTXprint. They open even without internet.
* **Advanced Tech Docs** (only in the **Full** view) – technical documents for advanced users.
* **Support Agent** – an AI chatbot that answers questions about PTXprint.
* **The PTXprint User Community** – a website where you can ask questions and help other users.
* **Tell us what you think about PTXprint** – a short feedback form.
* **Report an Issue via GitHub** (only in the **Full** view) – for reporting bugs, if you have a GitHub account.

### Support tools

* **Create Archive...** – makes a ZIP file with everything needed to make your PDF again on another computer.
* **Create Report...** – makes a report page about the last PDF.
* **Tidy Up** – deletes temporary files.
* **About** – shows the version number and the names of the developers.

## How to ask for help

If PTXprint does not do what you expect, there are several places to get help:

1. **Read this manual** and the **Common problems** sections in each chapter.
2. **Ask the Support Agent** (the AI chatbot link on the **Help** tab). It knows this manual and can answer many questions quickly.
3. **Ask the PTXprint User Community** (the community link on the **Help** tab). Other users and the developers read it.
4. **Email the support team** at **ptxprint_support@sil.org**.

### Before you write

* **Use the latest version.** Check the PTXprint home page. Your problem may already be fixed. The **About** button shows your version.
* **Make sure you can repeat the problem.** Note the exact steps: which project, which configuration, which book, and what you clicked.
* **Make the problem small.** If the problem is in one book, set PTXprint to print only that book. If the problem is about text, and pictures are not involved, untick pictures for now.
* **Click Create Report...** and look at the warnings and errors. They may already tell you what is wrong.

### What to send to ptxprint_support@sil.org

Send one email with:

1. **A clear description of the problem.** What did you want? What happened instead? On which page and in which verse? Copy the exact text of any error message.
2. **Your PTXprint version** (from the **About** window) and your operating system (for example Windows 11).
3. **Screenshots.** One picture of the problem in the PDF, and one of the PTXprint setting you think is involved. Mark the problem area if you can.
4. **The archive ZIP file** made with **Create Archive...** (see below). This lets the support team make exactly the same PDF on their computer.

### Making a good archive file

1. Select the project and configuration that shows the problem.
2. Choose only the book(s) needed to show the problem. One book is best.
3. If the problem has nothing to do with pictures, untick pictures. Pictures make the archive much larger.
4. On the **Help** tab, click **Create Archive...**.
5. Choose where to save the ZIP file, and click **Save**. PTXprint first prints the PDF again, then collects the files. This can take a while.
6. When it is finished, PTXprint opens the folder that contains the ZIP file.
7. Attach the ZIP file to your email.

The archive includes your settings, the USFM text of the selected books, the fonts, the pictures that are used, the PDF, and PTXprint's own typesetting files. Many email systems do not accept attachments larger than about 20 MB. If your ZIP file is too large, make it smaller (fewer books, no pictures), or share it through a file-sharing service and send the link.

The text of your project is inside the archive. If the text is sensitive, check with your project leader before you send it.

## Log tab

The **Log** tab is not normally shown in PTXprint. To read the messages from the typesetting program, use the **XeTeX Log** tab on the **View+Edit** tab, or use **Create Report...**.

## About dialog

The **About** window shows the PTXprint version number, the copyright, a link to the PTXprint home page, the list of developers, and the licence (MIT). Click **Credits** or **License** to see more, and **Close** to return. Give the version number when you ask for help.

The **About** button is only shown when **Disable ALL Internet Use** is unticked on the **Advanced** tab.

## Common tasks

### Find the PDF that PTXprint made

1. Open the **Help** tab.
2. Click the blue link next to **Output PDF Location**. The folder opens on your computer.

### Send a problem to the support team

1. Follow the steps in **Making a good archive file** above.
2. Write an email to **ptxprint_support@sil.org** with a description, your version number, screenshots and the ZIP file.

### Check the last PDF for problems

1. Click **Print** to make the PDF.
2. On the **Help** tab, click **Create Report...**.
3. The report opens in your web browser. Look at the warnings (for example missing fonts, underfilled pages, or problem markers).

### Free up disk space

1. On the **Help** tab, click **Tidy Up**.
2. PTXprint deletes the temporary working folders for all configurations of the current project. Your PDF files and settings are kept.

### Use projects from another Paratext folder

1. On the **Help** tab, click **Change...** next to **Base Projects Directory**.
2. In the **Choose Paratext Projects Folder** window, choose one of the folders that PTXprint found, or click **Browse for a different folder…**.
3. Choose the folder that *contains* your project folders, not a single project folder.
4. Click **Use Selected**. PTXprint goes back to the **Basic** tab. Choose a project from the new list.

### Show the internet links on the Help tab

1. Open the **Advanced** tab (shown in the **Default** and **Full** views).
2. Untick **Disable ALL Internet Use**.
3. Return to the **Help** tab. The links are now shown.

## Common problems

**The Help tab has very few links.**
**Disable ALL Internet Use** is ticked on the **Advanced** tab. Untick it to see the links. Some items (for example the **Technical Reference** and the **PTXprint Program Path**) are only shown in the **Full** view.

**A link opens the page in another language, or through Google Translate.**
When PTXprint is in a language other than English, some links go through Google Translate. Tick **Only Use English Links** on the **Advanced** tab to open the original English pages.

**Create Archive... takes a long time.**
PTXprint prints the whole job again before it makes the archive. Choose fewer books, or untick pictures, to make it faster and smaller.

**The archive ZIP file is too big to email.**
Archive only the book that shows the problem. Untick pictures if they are not part of the problem. If it is still too big, use a file-sharing service and send a link.

**"Cannot create Archive!" message.**
The ZIP file is open in another program, or you are saving over a file that is in use. Close the other program, or choose a different file name.

**Tidy Up shows a warning that some folders could not be deleted.**
A file in the folder is still open, for example the PDF in a PDF viewer, or a file in another program. Close it and click **Tidy Up** again.

**PTXprint does not show my projects.**
The **Base Projects Directory** may point to the wrong folder. Click **Change...** and choose the folder that contains your Paratext projects.

## Settings reference: Help tab and getting support

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Help tab › Links and Help

#### Output PDF Location

- **Where:** Help tab › Links and Help
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The PDF file created is stored in this folder (but should automatically open in your system's PDF viewer anyway).
>
> Note that ALL the files and subfolders in this location are TEMPORARY and can be deleted. None of these files are included in Paratext's Send/Recv data.

**Explanation:**

Shows the folder where PTXprint saves the finished PDF files (inside the project, in the local PTXprint folder). Click the blue link beside it to open the folder. The working files in the sub-folders are temporary and can be deleted with **Tidy Up**; they are not shared through Paratext Send/Receive.

*(Internal ID: `l_working_dir`)*

#### Training (Videos and Presentations)

- **Where:** Help tab › Links and Help
- **Type:** Label
- **View level:** Not normally shown

**Tooltip (the text shown when you hover the mouse over it):**

> There is a growing range of videos to teach you how to use some of the more advanced features of this very powerful software.

**Explanation:**

A heading for the training video links. Like the other internet links, it is only shown when **Disable ALL Internet Use** (on the **Advanced** tab) is unticked.

*(Internal ID: `l_trainingVideos`)*

#### Videos via Paratext

- **Where:** Help tab › Links and Help
- **Type:** Link
- **Description:** Link to training videos on the Paratext website
- **View level:** Not normally shown

**Tooltip (the text shown when you hover the mouse over it):**

> There is a growing range of videos to teach you how to use some of the more advanced features of this very powerful software.
>
> The videos on the Paratext site are high-quality and carefully curated, but they may not always cover the latest features available in PTXprint.

**Explanation:**

Opens the PTXprint training videos on the Paratext website in your web browser. These videos are well produced, but some may show an older version of PTXprint. Only shown when internet use is allowed.

*(Internal ID: `lb_trainingOnPTsite`)*

#### Report a Bug

- **Where:** Help tab › Links and Help
- **Type:** Label
- **View level:** Not normally shown

**Tooltip (the text shown when you hover the mouse over it):**

> PTXprint is built with Python & PyGTK3, using Glade for the User-Interface. The PDFs are produced by recently enhanced XeTeX macros with a long and reliable history. This is a work in progress, so when you come across bugs, annoyances or can't make it work right, please file an issue using this link.

**Explanation:**

A heading for the bug-report link. Only shown in the **Full** view, and only when internet use is allowed.

*(Internal ID: `l_reportBugs`)*

#### Report an Issue via GitHub

- **Where:** Help tab › Links and Help
- **Type:** Link
- **Description:** Link to report an issue with PTXprint
- **View level:** Not normally shown

**Explanation:**

Opens a new issue form on GitHub, where you can report a bug in PTXprint. You need a GitHub account. If you do not have one, email ptxprint_support@sil.org instead. Only shown in the **Full** view, and only when internet use is allowed.

*(Internal ID: `lb_reportBugs`)*

#### Documentation | FAQs | Gallery | Support | Download

- **Where:** Help tab › Links and Help
- **Type:** Link
- **Description:** Link to PTXprint home page
- **View level:** Not normally shown

**Explanation:**

Opens the PTXprint home page, with documentation, FAQs, a gallery of examples, support information and downloads. Only shown when internet use is allowed.

*(Internal ID: `lb_homePage`)*

#### PTXprint Home Page

- **Where:** Help tab › Links and Help
- **Type:** Label
- **View level:** Not normally shown

**Tooltip (the text shown when you hover the mouse over it):**

> PTXprint does not have an auto-updating feature, so you are encouraged to check for new updates at the Home Page. Please ensure you are using the latest version before reporting an issue.

**Explanation:**

A heading for the home page link. PTXprint does not update itself, so visit the home page from time to time to download the newest version. Always check that you have the latest version before you report a problem.

*(Internal ID: `l_homePage`)*

#### Reference Documentation

- **Where:** Help tab › Links and Help
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Reference documents for PTXprint:  
> the Ornaments Catalog, the Technical Reference (for advanced users) and, when online, the Advanced Tech Docs.

**Explanation:**

A heading for the reference documents (**Ornaments Catalog** and **Technical Reference**). Only shown in the **Full** view.

*(Internal ID: `l_techFAQ`)*

#### Advanced Tech Docs

- **Where:** Help tab › Links and Help
- **Type:** Link
- **Description:** Link to deeper technical help
- **View level:** Not normally shown

**Explanation:**

Opens the advanced technical documentation (on GitHub) in your web browser. It is written for expert users and often describes things that cannot be set in the PTXprint window. Only shown in the **Full** view, and only when internet use is allowed.

*(Internal ID: `lb_techFAQ`)*

#### PTXprint Program Path

- **Where:** Help tab › Links and Help
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Among other things, this folder contains:  
> * ReleaseNotes.txt  
> * AboutPTXprint.txt  
> * MIT License.txt

**Explanation:**

Shows the folder where PTXprint is installed. The release notes and licence files are in this folder. You normally do not need it, except when the support team asks for it. Only shown in the **Full** view.

*(Internal ID: `l_ptxprintdir`)*

#### Create Archive...

- **Where:** Help tab › Links and Help
- **Type:** Button
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Create a ZIPped archive of all the files required to replicate this configuration. Useful for long-term archiving; but also helpful when availing technical support. The job is printed again first, so this may take a while.
>
> Keep the size to a minimum by turning off features (pictures?) that don't affect the issue being reported.
>
> Email the ZIPped archive file to:  
> mailto:ptxprint_support@sil.org

**Explanation:**

Makes a ZIP file with everything needed to create this PDF on another computer: settings, the USFM text of the selected books, fonts, pictures, the PDF and PTXprint's typesetting files. PTXprint prints the job again first, so this can take some time. Before you click, choose only the book(s) that show the problem, and untick pictures if they are not involved, to keep the file small. Send the ZIP file to ptxprint_support@sil.org with a description of the problem. It is also useful as a long-term record of how a publication was made.

*(Internal ID: `btn_createZipArchiveXtra`)*

#### The PTXprint User Community

- **Where:** Help tab › Links and Help
- **Type:** Link
- **Description:** Link to PTXprint user community site
- **View level:** Not normally shown

**Explanation:**

Opens the PTXprint user community website, where you can search earlier questions, ask your own, and share tips. Only shown when internet use is allowed.

*(Internal ID: `lb_community`)*

#### Got a Question? Get Help and Support from

- **Where:** Help tab › Links and Help
- **Type:** Label
- **View level:** Not normally shown

**Tooltip (the text shown when you hover the mouse over it):**

> Scripture Software Community site where you can interact with other PTXprint users and the developers.

**Explanation:**

A heading for the community link. The community website is a good place to ask "How do I…?" questions, because other users may have had the same question.

*(Internal ID: `l_community`)*

#### About

- **Where:** Help tab › Links and Help
- **Type:** Button
- **Description:** About PTXprint
- **View level:** Not normally shown

**Tooltip (the text shown when you hover the mouse over it):**

> Discover more about PTXprint.

**Explanation:**

Opens the **About** window, with the version number, developers and licence. Give the version number when you ask for help. Only shown when internet use is allowed.

*(Internal ID: `btn_about`)*

#### Tidy Up

- **Where:** Help tab › Links and Help
- **Type:** Button
- **Description:** Delete temporary files and folders
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Delete the TEMPORARY working folders of ALL configurations of this project. This will not delete the resulting PDF files, but will save some space by deleting unneeded files.

**Explanation:**

Deletes the temporary working folders of every configuration in the current project. Your PDF files and your settings are not deleted. The next print takes a little longer, because PTXprint must make the working files again. If a file is still open in another program, PTXprint warns that some folders could not be deleted.

*(Internal ID: `btn_deleteTempFiles`)*

#### Give Feedback

- **Where:** Help tab › Links and Help
- **Type:** Label
- **View level:** Not normally shown

**Tooltip (the text shown when you hover the mouse over it):**

> Psst! Can we have 5 minutes of your time? You could help us make PTXprint better!
>
> The developers of PTXprint would love to know how this tool is being used. What is your favorite feature? Are there any annoyances? Tell us what you like, or don't like. Tell us what you dream for in the future.

**Explanation:**

A heading for the feedback link. Only shown when internet use is allowed.

*(Internal ID: `l_giveFeedback`)*

#### Tell us what you think about PTXprint

- **Where:** Help tab › Links and Help
- **Type:** Link
- **Description:** Link to PTXprint Feedback Form (Google Form)
- **View level:** Not normally shown

**Tooltip (the text shown when you hover the mouse over it):**

> Click this link to fill in the Google form or type this in a browser: http://tiny.cc/ptxprintfeedback

**Explanation:**

Opens a short online form where you can tell the developers what you like, what annoys you, and what you would like in the future. Only shown when internet use is allowed.

*(Internal ID: `lb_giveFeeback`)*

#### Videos via Vimeo

- **Where:** Help tab › Links and Help
- **Type:** Link
- **Description:** Link to training videos on the Vimeo platform
- **View level:** Not normally shown

**Tooltip (the text shown when you hover the mouse over it):**

> There is a growing range of videos to teach you how to use some of the more advanced features of this very powerful software.
>
> The videos on Vimeo tend to be longer and more detailed, but less polished. However, these videos cover the latest available features.

**Explanation:**

Opens the PTXprint training videos on Vimeo. These videos are longer and less polished, but they cover newer features. Only shown when internet use is allowed.

*(Internal ID: `lb_trainingOnVimeo`)*

#### Ornaments Catalog

- **Where:** Help tab › Links and Help
- **Type:** Link
- **Description:** Show the Ornaments Catalog
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Click to Open the Ornaments Catalog used for decorating the PDF (refer to the Tabs+Borders settings).

**Explanation:**

Opens the Ornaments Catalog PDF, which shows all the decorative ornaments you can use for borders and decorations on the **Tabs+Borders** tab. The file comes with PTXprint, so it opens without internet. Only shown in the **Full** view.

*(Internal ID: `lb_ornaments_cat`)*

#### Technical Reference

- **Where:** Help tab › Links and Help
- **Type:** Link
- **Description:** Show the Technical Reference document
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Click to open the Technical Reference document. (For advanced users only).

**Explanation:**

Opens the Technical Reference PDF that comes with PTXprint. It explains many settings in detail, but it is written for advanced users. Only shown in the **Full** view.

*(Internal ID: `lb_tech_ref`)*

#### Learn: How to...

- **Where:** Help tab › Links and Help
- **Type:** Link
- **Description:** Link to the Learn page with How To... articles
- **View level:** Not normally shown

**Explanation:**

Opens the "Learn" page on the PTXprint website, with short How To... articles for common tasks. Only shown when internet use is allowed.

*(Internal ID: `lb_learnHowTo`)*

#### Technical Support

- **Where:** Help tab › Links and Help
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Before contacting support, make sure that it is possible to replicate the issue. Then use the "Create Archive..." button to make a ZIP file which needs to be emailed to:  
> mailto:ptxprint_support@sil.org

**Explanation:**

A reminder of how to get technical support: first make sure you can repeat the problem, then make an archive with **Create Archive...** and email it to ptxprint_support@sil.org. See **How to ask for help** in this chapter.

*(Internal ID: `l_techSupport1`)*

#### Create Report...

- **Where:** Help tab › Links and Help
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Generate a summary report with details about the PDF produced. This contains informational, warning and error messages about fonts, styles, layout and so on.
>
> Generate a summary report with details about the PDF produced. This contains informational, warning and error mesaages about fonts, styles, layout and so on.

**Explanation:**

Makes a report about the most recent PDF and opens it in your web browser. The report lists information, warnings and errors in sections such as project overview, layout, USFM checks, fonts, writing system, peripheral components, output format, files and log analysis. Make the PDF first, so that the report is up to date. The report is a good first check before you ask for help, and you can attach it to your email to the support team.

*(Internal ID: `btn_generateReport`)*

#### Support Agent

- **Where:** Help tab › Links and Help
- **Type:** Link
- **Description:** Use the PTXprint Support Agent (AI chatbot) to answer your questions instantly
- **View level:** Not normally shown

**Explanation:**

Opens the PTXprint Support Agent, an AI chatbot, in your web browser. Ask it questions in plain words, for example "How do I make the text two columns?". It answers quickly, but check its answers in PTXprint. Only shown when internet use is allowed.

*(Internal ID: `lb_chatBot`)*

#### Base Projects Directory

- **Where:** Help tab › Links and Help
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The folder that contains all your Paratext project folders. Use Change... to choose a different folder.

**Explanation:**

Shows the Base Projects Directory: the folder that contains all your Paratext project folders. PTXprint lists the projects it finds in this folder on the **Basic** tab. Click the link beside it to open the folder.

*(Internal ID: `l_projects_dir`)*

#### Change...

- **Where:** Help tab › Links and Help
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Use this button to change the Base Projects Directory. For example, to use projects from a different version of Paratext.
>
> Do not select a specific project folder, but the parent folder which contains one or more projects.

**Explanation:**

Opens the **Choose Paratext Projects Folder** window. PTXprint lists the Paratext folders it found and says which ones contain projects. You can also browse for another folder. Choose the folder that *contains* the project folders, not one project folder. After the change, PTXprint returns to the **Basic** tab, so that you can choose a project from the new list. This is useful if you have more than one version of Paratext, or keep projects in a different folder.

*(Internal ID: `btn_changeProjectsDir`)*

#### Training Presentation

- **Where:** Help tab › Links and Help
- **Type:** Link
- **Description:** Link to training presentation slides
- **View level:** Not normally shown

**Tooltip (the text shown when you hover the mouse over it):**

> There is an extensive Google Slides presentation which can be used as a reference for training.

**Explanation:**

A link to a large set of training slides. It is currently not shown in the PTXprint window.

*(Internal ID: `lb_masterSlides`)*

### Log tab

#### tv_logging

- **Where:** Log tab
- **Type:** Text area
- **View level:** Not normally shown

**Explanation:**

The text area on the **Log** tab. The **Log** tab is not normally shown. To see the messages from the typesetting run, use the **XeTeX Log** tab on the **View+Edit** tab, or click **Create Report...**.

*(Internal ID: `tv_logging`)*
