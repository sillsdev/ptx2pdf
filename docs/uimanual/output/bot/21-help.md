# 24. Help tab and getting support

## 24.1 What this tab is for

The **Help** tab is where you go when you need help, or need to find your files. It is shown in every view level.

On this tab you can:

* see where PTXprint keeps your PDF and other files, and open those folders;
* open the documentation, training material and the user community website;
* make an **archive** (a ZIP file) of your project to send to the support team;
* make a **report** about the last PDF, with warnings and errors;
* **Tidy Up** temporary files to save disk space;
* change the **Base Projects Directory** (the folder that holds your Paratext projects);
* open the **About** window to see which version of PTXprint you have.

Many links on this tab open web pages. They are only shown when internet use is allowed. If **Disable ALL Internet Use** is ticked on the **Advanced** tab, the internet links and the **About** button are hidden. Untick it to see them again. Some items are only shown in the **Full** view; this is noted for each one.

## 24.2 Links and Help

### Folders

* **Output PDF Location** – the folder where PTXprint saves the PDF files it makes. Click the blue link to open it.
* **Base Projects Directory** – the folder that holds all your Paratext projects. Use **Change...** to choose a different one.
* **PTXprint Program Path** (**Full** view only) – the folder where PTXprint itself is installed.

Everything in the output location is made again each time you print. None of it is part of Paratext Send/Receive. Your settings are kept safely in a different place, inside the project's shared folder.

### Documentation and learning

These links open web pages or documents:

* **Documentation | FAQs | Gallery | Support | Download** – the PTXprint home page. PTXprint does not update itself, so check here for new versions and download them yourself.
* **Learn: How to...** – short articles about common tasks.
* **Training (Videos and Presentations)** – videos on the Paratext website and on Vimeo, and a **Training Presentation** (a large set of Google Slides that trainers can use).
* **Ornaments Catalog** and **Technical Reference** (**Full** view only) – PDF documents that come with PTXprint. They open without internet.
* **Advanced Tech Docs** (**Full** view only) – technical documents for advanced users.
* **Support Agent** – an AI chatbot that answers questions about PTXprint.
* **The PTXprint User Community** – a website where you can ask questions and help other users.
* **Tell us what you think about PTXprint** – a short feedback form.
* **Report an Issue via GitHub** (**Full** view only) – for reporting bugs, if you have a GitHub account.

### Support tools

* **Create Archive...** – makes a ZIP file with everything needed to make your PDF again on another computer.
* **Create Report...** – makes a report page about the last PDF.
* **Tidy Up** – deletes temporary files.
* **About** – shows the version number and the names of the developers.

## 24.3 How to ask for help

If PTXprint does not do what you expect, you can get help here:

1. **Read this manual** and the **Common problems** sections in each chapter.
2. **Ask the Support Agent** (the AI chatbot link on the **Help** tab). It knows this manual and can answer many questions quickly.
3. **Ask the PTXprint User Community** (the community link on the **Help** tab). Other users and the developers read it.
4. **Email the support team** at **ptxprint_support@sil.org**.

### Before you write

* **Use the latest version.** Check the PTXprint home page. Your problem may already be fixed. The **About** button shows your version.
* **Make sure you can repeat the problem.** Note the exact steps: which project, which configuration, which book, and what you clicked.
* **Make the problem small.** If the problem is in one book, print only that book. If pictures are not involved, untick pictures for now.
* **Click Create Report...** and look at the warnings and errors. They may already tell you what is wrong.

### What to send to ptxprint_support@sil.org

Send one email with:

1. **A clear description of the problem.** What did you want? What happened instead? On which page and in which verse? Copy the exact text of any error message.
2. **Your PTXprint version** (from the **About** window) and your operating system (for example Windows 11).
3. **Screenshots.** One of the problem in the PDF, and one of the PTXprint setting you think is involved. Mark the problem area if you can.
4. **The archive ZIP file** made with **Create Archive...** (see below). With it, the support team can make exactly the same PDF on their computer.

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

An archive is also useful as a long-term record of how a publication was made.

## 24.4 Log tab

The **Log** tab is not normally shown in PTXprint. To read the messages from the typesetting program, use the **XeTeX Log** tab on the **View+Edit** tab, or use **Create Report...**.

## 24.5 About dialog

The **About** window shows the PTXprint version number, the copyright, a link to the PTXprint home page, the list of developers, and the licence (MIT). Click **Credits** or **License** to see more, and **Close** to return. Give the version number when you ask for help.

The **About** button is only shown when **Disable ALL Internet Use** is unticked on the **Advanced** tab.

## 24.6 Common tasks

### Find the PDF that PTXprint made

On the **Help** tab, click the blue link next to **Output PDF Location**. The folder opens on your computer.

### Send a problem to the support team

1. Follow the steps in **Making a good archive file** above.
2. Email **ptxprint_support@sil.org** with a description, your version number, screenshots and the ZIP file.

### Check the last PDF for problems

1. Click **Print** to make the PDF.
2. On the **Help** tab, click **Create Report...**.
3. The report opens in your web browser. Look at the warnings (for example missing fonts, underfilled pages, or problem markers).

### Free up disk space

On the **Help** tab, click **Tidy Up**. PTXprint deletes the temporary working folders for all configurations of the current project. Your PDF files and settings are kept.

### Use projects from another Paratext folder

1. On the **Help** tab, click **Change...** next to **Base Projects Directory**.
2. In the **Choose Paratext Projects Folder** window, choose one of the folders that PTXprint found, or click **Browse for a different folder…**.
3. Choose the folder that *contains* your project folders, not a single project folder.
4. Click **Use Selected**. PTXprint goes back to the **Basic** tab. Choose a project from the new list.

### Show the internet links on the Help tab

1. Open the **Advanced** tab (shown in the **Regular** and **Full** views).
2. Untick **Disable ALL Internet Use**.
3. Return to the **Help** tab. The links are now shown.

## 24.7 Common problems

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
A file in the folder is still open, for example the PDF in a PDF viewer. Close it and click **Tidy Up** again.

**PTXprint does not show my projects.**
The **Base Projects Directory** may point to the wrong folder. Click **Change...** and choose the folder that contains your Paratext projects.

## 24.8 Settings reference

### Help

#### Links and Help

##### Output PDF Location

Label · Regular+ · `l_working_dir`

> The PDF file created is stored in this folder (but should automatically open in your system's PDF viewer anyway).
>
> Note that ALL the files and subfolders in this location are TEMPORARY and can be deleted. None of these files are included in Paratext's Send/Recv data.

The folder is inside the project, in the local PTXprint folder. Click the blue link beside it to open it. **Tidy Up** deletes the temporary working files in its sub-folders.

##### Training (Videos and Presentations)

Label · not shown · `l_trainingVideos`

> There is a growing range of videos to teach you how to use some of the more advanced features of this very powerful software.

A heading for the training links. Only shown when internet use is allowed.

##### Videos via Paratext

Link · not shown · `lb_trainingOnPTsite`  
Also: Link to training videos on the Paratext website

> There is a growing range of videos to teach you how to use some of the more advanced features of this very powerful software.
>
> The videos on the Paratext site are high-quality and carefully curated, but they may not always cover the latest features available in PTXprint.

Opens the videos in your web browser. Only shown when internet use is allowed.

##### Report a Bug

Label · not shown · `l_reportBugs`

> Found a bug? If you have a GitHub account, report it here. Otherwise email ptxprint_support@sil.org.

A heading for the bug-report link. Only shown in the **Full** view, and only when internet use is allowed.

##### Report an Issue via GitHub

Link · not shown · `lb_reportBugs`  
Also: Link to report an issue with PTXprint

Opens a new issue form on GitHub. You need a GitHub account; without one, email ptxprint_support@sil.org. Only shown in the **Full** view, and only when internet use is allowed.

##### Documentation | FAQs | Gallery | Support | Download

Link · not shown · `lb_homePage`  
Also: Link to PTXprint home page

Opens the PTXprint home page, with documentation, FAQs, a gallery of examples, support information and downloads. Only shown when internet use is allowed.

##### PTXprint Home Page

Label · not shown · `l_homePage`

> PTXprint does not have an auto-updating feature, so you are encouraged to check for new updates at the Home Page. Please ensure you are using the latest version before reporting an issue.

A heading for the home page link. Visit the home page from time to time to download the newest version.

##### Reference Documentation

Label · Regular+ · `l_techFAQ`

> Reference documents for PTXprint:  
> the Ornaments Catalog, the Technical Reference (for advanced users) and, when online, the Advanced Tech Docs.

A heading for the reference documents. Only shown in the **Full** view.

##### Advanced Tech Docs

Link · not shown · `lb_techFAQ`  
Also: Link to deeper technical help

Opens the advanced technical documentation (on GitHub) in your web browser. It is for expert users and often describes things that cannot be set in the PTXprint window. Only shown in the **Full** view, and only when internet use is allowed.

##### PTXprint Program Path

Label · Regular+ · `l_ptxprintdir`

> Among other things, this folder contains:  
> * ReleaseNotes.txt  
> * AboutPTXprint.txt  
> * MIT License.txt

You normally do not need this folder, unless the support team asks for it. Only shown in the **Full** view.

##### Create Archive...

Button · Basic+ · `btn_createZipArchiveXtra`

> Create a ZIPped archive of all the files required to replicate this configuration. Useful for long-term archiving; but also helpful when availing technical support. The job is printed again first, so this may take a while.
>
> Keep the size to a minimum by turning off features (pictures?) that don't affect the issue being reported.
>
> Email the ZIPped archive file to:  
> mailto:ptxprint_support@sil.org

See **Making a good archive file** in this chapter for what to do before you click and what the archive contains.

##### The PTXprint User Community

Link · not shown · `lb_community`  
Also: Link to PTXprint user community site

Opens the PTXprint user community website, where you can search earlier questions, ask your own, and share tips. Only shown when internet use is allowed.

##### Got a Question? Get Help and Support from

Label · not shown · `l_community`

> Scripture Software Community site where you can interact with other PTXprint users and the developers.

A heading for the community link. A good place to ask "How do I…?" questions, because other users may have had the same question.

##### About

Button · not shown · `btn_about`  
Also: About PTXprint

> Discover more about PTXprint.

Opens the **About** window (see **About dialog** above). Only shown when internet use is allowed.

##### Tidy Up

Button · Basic+ · `btn_deleteTempFiles`  
Also: Delete temporary files and folders

> Delete the TEMPORARY working folders of ALL configurations of this project. This will not delete the resulting PDF files, but will save some space by deleting unneeded files.

Your settings are not deleted either. The next print takes a little longer, because PTXprint must make the working files again. If a file is still open in another program, PTXprint warns that some folders could not be deleted.

##### Give Feedback

Label · not shown · `l_giveFeedback`

> Psst! Can we have 5 minutes of your time? You could help us make PTXprint better!
>
> The developers of PTXprint would love to know how this tool is being used. What is your favorite feature? Are there any annoyances? Tell us what you like, or don't like. Tell us what you dream for in the future.

A heading for the feedback link. Only shown when internet use is allowed.

##### Tell us what you think about PTXprint

Link · not shown · `lb_giveFeeback`  
Also: Link to PTXprint Feedback Form (Google Form)

> Click this link to fill in the Google form or type this in a browser: http://tiny.cc/ptxprintfeedback

Opens the feedback form in your web browser. Only shown when internet use is allowed.

##### Videos via Vimeo

Link · not shown · `lb_trainingOnVimeo`  
Also: Link to training videos on the Vimeo platform

> There is a growing range of videos to teach you how to use some of the more advanced features of this very powerful software.
>
> The videos on Vimeo tend to be longer and more detailed, but less polished. However, these videos cover the latest available features.

Opens the videos in your web browser. Only shown when internet use is allowed.

##### Ornaments Catalog

Link · Regular+ · `lb_ornaments_cat`  
Also: Show the Ornaments Catalog

> Click to Open the Ornaments Catalog used for decorating the PDF (refer to the Tabs+Borders settings).

Shows all the decorative ornaments you can use on the **Tabs+Borders** tab. The file comes with PTXprint, so it opens without internet. Only shown in the **Full** view.

##### Technical Reference

Link · Regular+ · `lb_tech_ref`  
Also: Show the Technical Reference document

> Click to open the Technical Reference document. (For advanced users only).

The PDF comes with PTXprint and explains many settings in detail. Only shown in the **Full** view.

##### Learn: How to...

Link · not shown · `lb_learnHowTo`  
Also: Link to the Learn page with How To... articles

Opens the "Learn" page on the PTXprint website, with short How To... articles for common tasks. Only shown when internet use is allowed.

##### Technical Support

Label · Regular+ · `l_techSupport1`

> Before contacting support, make sure that it is possible to replicate the issue. Then use the "Create Archive..." button to make a ZIP file which needs to be emailed to:  
> mailto:ptxprint_support@sil.org

See **How to ask for help** in this chapter.

##### Create Report...

Button · Regular+ · `btn_generateReport`

> Generate a summary report with details about the PDF produced. This contains informational, warning and error messages about fonts, styles, layout and so on.

Opens the report in your web browser. Its sections include project overview, layout, USFM checks, fonts, writing system, peripheral components, output format, files and log analysis. Make the PDF first, so that the report is up to date. It is a good first check before you ask for help, and you can attach it to your email to the support team.

##### Support Agent

Link · not shown · `lb_chatBot`  
Also: Use the PTXprint Support Agent (AI chatbot) to answer your questions instantly

Opens the Support Agent in your web browser. Ask it questions in plain words, for example "How do I make the text two columns?". It answers quickly, but check its answers in PTXprint. Only shown when internet use is allowed.

##### Base Projects Directory

Label · Regular+ · `l_projects_dir`

> The folder that contains all your Paratext project folders. Use Change... to choose a different folder.

PTXprint lists the projects it finds in this folder on the **Basic** tab. Click the link beside it to open the folder.

##### Change...

Button · Regular+ · `btn_changeProjectsDir`

> Use this button to change the Base Projects Directory. For example, to use projects from a different version of Paratext.
>
> Do not select a specific project folder, but the parent folder which contains one or more projects.

Opens the **Choose Paratext Projects Folder** window. It lists the Paratext folders PTXprint found and says which ones contain projects. You can also browse for another folder. After the change, PTXprint returns to the **Basic** tab, so you can choose a project from the new list.

##### Training Presentation

Link · not shown · `lb_masterSlides`  
Also: Link to training presentation slides

> There is an extensive Google Slides presentation which can be used as a reference for training.

Opens the slides in your web browser. Trainers can use them to teach PTXprint. Only shown when internet use is allowed.

### Log

#### tv_logging

Text area · not shown · `tv_logging`

The text area on the **Log** tab, which is not normally shown. See **Log tab** above.
