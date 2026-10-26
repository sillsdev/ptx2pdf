# 10. Pictures tab

## 10.1 What this tab is for

Use the **Pictures** tab when your publication has pictures (illustrations) or maps. Here you can:

* turn pictures on or off for the whole publication,
* tell PTXprint where to find the picture files,
* choose the size and position of every picture on the page,
* add or remove pictures, and add maps,
* look for new pictures in a catalogue of Bible illustrations,
* keep track of copyright, permissions and the checking of each picture.

**The PicList.** PTXprint keeps a list of all the pictures for each saved configuration. This list is called the **PicList** (picture list). Each line of the PicList says which picture file to use, where in the text it belongs (the *anchor*), its caption, its size and its position on the page.

When you generate the PicList, PTXprint copies the `\fig ... \fig*` entries from your Paratext books into the PicList. After that, PTXprint uses only the PicList. It ignores the `\fig` entries in the text when it typesets. This means:

* You can place, resize, add and remove pictures in PTXprint **without changing the Paratext text**.
* Each configuration can have different pictures. For example, a full Bible can have a few pictures, and a children's portion can have many.
* Changes you make here are **not** copied back into Paratext. If a caption or picture changes in Paratext, use **Refresh List** or **Generate...** to bring the change into PTXprint.

**View levels.** The Pictures tab is shown from the **Basic** view. In the **Basic** view you only see a few settings on the **Global Options** sub-tab. The picture table, the **Details** and **Checklist** sub-tabs and most buttons are only shown in the **Regular** and **Full** views.

Some words used in this chapter:

* **Anchor** – the place in the text (for example a verse) that a picture belongs to.
* **Caption** – the text printed with the picture, usually below it.
* **Cutout** – a space cut into the side of a paragraph, so that the text flows around a small picture.
* **Span** – the full width of the text area, across both columns.
* **Mirror** – flip a picture from left to right, like in a mirror.
* **Credit overlay** – a small copyright line printed on top of the picture itself.
* **Image set** – a downloadable collection of Bible illustrations that you can use in the catalogue.

## 10.2 The picture table (PicList)

The top half of the tab shows the PicList as a table. Each row is one picture. The columns shown change with the sub-tab: **Global Options** and **Checklist** show only a few columns; **Details** shows them all.

* Click a row to select it. Its settings appear in the **Details** sub-tab below.
* Double-click a row to jump to the **Details** sub-tab.
* You can select several rows at once (use Ctrl or Shift while clicking). Then you can change the size, position, scale or mirror setting of all of them together. Fields that must be different for each picture (anchor, caption, filename, reference) are greyed out while several rows are selected.
* Right-click a row for more actions: copy the `\fig` line for that picture (to paste into Paratext), jump to the reference in Paratext (Windows only), show the picture file in the file manager, copy the file path, or delete the picture(s).
* **Red** text in a row means the picture is probably too tall to fit on the page at this size and scale. Make the **Scale** smaller.
* **Grey** rows mean PTXprint cannot find the picture file. Check the file name and the picture folders (see below).

The buttons next to the table:

* **Add** – add a picture file by hand.
* **Del** – delete the selected picture(s) from the PicList at once (no question is asked).
* **Generate...** – (re)build the PicList from the `\fig` entries in the Paratext books.
* **Refresh List** – update only the captions and references from Paratext.
* **Add Maps...** / **Edit Maps...** – add maps at the end of the publication, and edit the map book.
* **Show Catalogue...** – open the **Select Images** dialog to choose illustrations from an image set.
* **Show Active Books** – show only the pictures of the books you have chosen to print.
* **Image** / **Position** – show either a preview of the picture, or a small drawing of where it will sit on the page.

When the **Checklist** sub-tab is open, the buttons are replaced by a **Filter Checklist** area. Use it to show only the pictures that still need checking, or only the approved ones.

## 10.3 Global Options

This sub-tab has the settings for all the pictures in the publication.

**Include Pictures (illustrations)** is the main switch. When it is not ticked, PTXprint prints no pictures, and most other picture settings are greyed out.

**Resolution.** Paratext usually keeps small, low-quality JPG copies of pictures in the project's `figures` folder. Large, high-quality copies are often kept in the project's `local\figures` folder, so that they are not shared by Send/Receive.

* **Low Resolution (Smaller File)** – PTXprint prefers JPG files, and the smaller file if there are two of the same kind. The PDF is small and easy to email. Use this for drafts and checking.
* **High Resolution (Larger File)** – PTXprint prefers TIF and PNG files, and the larger file. Use this for the final PDF for the printer.
* **Use Place-holders (Smallest PDF File)** – prints an empty box where each picture would go. The layout stays the same, but the PDF is very small.

**What to print.**

* **Omit Pictures Only Meant for Web or App** – leaves out pictures that are not marked for print.
* **Omit Captions** – prints the pictures without any caption.
* **Omit References (ch:vs)** – keeps the captions but removes the chapter:verse reference after them.
* **Omit Missing Pictures** – if a picture file cannot be found, PTXprint skips it and continues. After you print, the number of missing pictures is shown next to this option, and their names are listed at the bottom of the sub-tab.
* **Remove Image Borders** – cuts off thin lines at the edges of pictures. It affects every picture.

**Where PTXprint looks for picture files.** PTXprint searches these folders, and all the folders inside them (unless **Exclude Subfolders** is ticked):

1. the **Picture Folder** you chose (only when **Use Other Location** is ticked),
2. the project's `local\figures` folder,
3. the project's `figures` folder,
4. the image sets you have downloaded (in PTXprint's own data folder).

The PicList only stores the file **name**, not the folder. If several files have the same name (for example `hk00123.jpg` and `hk00123.tif`), **Image Types** decides which one is used. If you leave **Image Types** empty, PTXprint uses JPG first for low resolution and TIF first for high resolution. TIF and PNG pictures are converted to JPG while the PDF is made.

**Permissions.** **Request Access...** (only with **High Resolution**) and **Get Permission...** open online forms that PTXprint fills in with the list of pictures used in this configuration.

## 10.4 Details

This sub-tab shows the settings of the picture selected in the table. It is only shown in the **Regular** and **Full** views.

**Anchor Ref.** The anchor is where the picture belongs in the text. It has a 3-letter book code, a space, and the chapter and verse joined with a dot: `MRK 4.39`. PTXprint puts the picture on the same page as its anchor if there is room. If there is no room, the picture can move to a later page. To move a picture to an earlier or later page, change the anchor by a few verses. Other forms:

* In a diglot, add `L` or `R` to the book code (`MRKL 4.39`) to tie the picture to the primary (L) or secondary (R) text.
* In the glossary, `GLO k.Altar` ties a picture to the glossary entry `\k Altar\k*`. Spaces are removed (`GLO k.JohntheBaptist`).
* `=2` at the end (for example `PSA 23.4=3`) means "the 2nd (or 3rd) paragraph after this anchor". This is useful for poetry.

**Caption, Caption Ref and Filename.** The **Caption** is printed with the picture. The **Caption Ref** is the reference printed after the caption, for example `(4:39)`. It does not have to be the same as the anchor. The **Filename** is the name of the picture file. Changes here are not copied back to Paratext.

**Size and position.** Three settings work together. The choices in each list change with the one before it, so set them in this order:

1. **Frame Size** – how wide the area for the picture is:
   * **Column Width** – the width of one column (in two-column layout).
   * **Span Width** – the full width of the text, across both columns.
   * **Page (in Margins)** – a whole page inside the margins. The page header is still printed.
   * **Page (to Edge)** – the whole sheet of paper, with no margins, header or footer. Do not use a caption with this size.
   In single-column layout, Column Width and Span Width are the same.
2. **Vertical Position** – where the picture goes:
   * **Top** / **Bottom** – at the top or bottom of the page (or column).
   * **Below Notes** – below the footnotes (Span Width only).
   * **Before Verse** – in the text, just before the anchor verse.
   * **After Paragraph** – in the text, after the paragraph that contains the anchor.
   * **Cutout** – in a notch at the side of the paragraph. The text flows around the picture.
   For the page sizes, the choices are **Top**, **Center** and **Bottom** of the page.
3. **Horizontal Position** – **Left**, **Right**, **Inner** (near the binding), **Outer** (near the outside edge) and, where possible, **Center**. It is greyed out (shows **-**) for Span Width.

**Number of Lines** is used only with **Cutout** (how many lines below the start of the paragraph the picture starts; decimals are allowed) and **After Paragraph** (after how many paragraphs).

PTXprint stores the position as a short code (shown in the table's position column). You do not have to type these codes, but they help when you read the table:

| Code | Meaning |
|---|---|
| `t`, `b` | top or bottom of the page, full width |
| `B` | below the footnotes |
| `tl`, `tr`, `bl`, `br` | top or bottom of the left or right column |
| `hl`, `hc`, `hr` | "here" – just before the anchor verse, left, centre or right |
| `pc`, `pl2` | after the paragraph (the number = after that many paragraphs) |
| `cl2`, `cr3` | cutout on the left or right, starting 2 or 3 lines down |
| `P`, `Pt`, `Pb` | a page of its own, centred, at the top or at the bottom |
| `F` | a full page to the edge of the paper |

`i` and `o` (inner and outer) can be used instead of `l` and `r`.

**Scale** makes the picture smaller (or larger) inside its frame. 100% means the full width of the frame. For a cutout, 30–50% is common. If the row turns red, the picture is too tall for the page; make the scale smaller.

**Mirror** flips the picture. Use it, for example, so that people in the picture look into the page and not out of it, or so that an action is done with the right hand. **Odd** and **Even** flip the picture only when it lands on an odd or even page. **Mirror** is greyed out if the **Checklist** sub-tab says **Never mirror** or **Always mirror** for this picture.

**Media (Print, App, Web).** These boxes say where the picture may be used. A picture without **Print** is left out of the PDF. Some boxes are greyed out because the artist's licence does not allow that use. If you untick all three boxes, PTXprint remembers this when you open the project again.

**Copyright.** For the common series of Bible illustrations (for example file names that start with `cn`, `co`, `hk`, `lb`, `bk`, `dy`, `mn` or `wa` followed by five digits), PTXprint knows the copyright text. You see the word **Automatic** instead of a text box. For other pictures, type the credit in **Copyright Attribution**. PTXprint collects all the picture credits, with page numbers, into the colophon when the colophon contains `\zimagecopyrights` (set this on the **Peripherals** tab).

Some artists require a small credit printed **on** each picture. Click **© ...** to open the **Illustration Credit Overlay** dialog.

**Extra** is for advanced options such as rotating a picture (`rotated 90`, `rotate=edge`, `rotate=binding`) or choosing a page of a multi-page PDF (`page=2`).

## 10.5 Checklist

This sub-tab helps the team think about whether each picture is right for the readers. It is only shown in the **Regular** and **Full** views. The answers are stored with the picture's file, not with the anchor. So if the same picture is used twice, both uses share the answers. PTXprint saves the answers, the approval and the notes, and loads them again the next time you open the project.

* **Across Various Publications** – questions about the picture itself: is it clear, is it acceptable in the culture, and may it be mirrored? These answers are shared by all configurations of the project.
* **In This Publication** – questions about this use: why is it here, is it clear in this context, does it carry a wrong meaning, and does its style suit this publication? These answers belong to the current configuration.
* **Consultant Approval** – tick **Approved to be used in**, choose **any publication** or **this publication**, and type the initials and date.
* **Notes About This Picture** – a place to write comments, or to discuss the picture with the consultant.

Use the **Filter Checklist** area above the table to show, for example, only the pictures where some questions are still **Unknown**.

## 10.6 Generate PicList dialog

This dialog opens when you click **Generate...** and a PicList already exists. (If there is no PicList yet, PTXprint makes one at once without asking.)

* **Append Pictures to PicList From These Books** – read the `\fig` entries again only for the books listed (the books selected on the **Basic** tab). Pictures from other books stay as they are.
* **Include Pictures From ALL Books** – read all the books of the project again.
* **Randomly Position Pictures on Page** – give new pictures a random corner (top-left, top-right, bottom-left or bottom-right). Without it, new pictures go top-left in two-column layout and at the top in single-column layout.
* **Protect existing PicList settings** – keep the size and position of pictures that are already in the PicList, and only add new ones. Untick it only if you want to start again from the Paratext text.

## 10.7 Select Images dialog (the catalogue)

Click **Show Catalogue...** to open this dialog. It shows thumbnails of the pictures in an **Image Set**. If you have no image set yet, the **Download & Install Image Sets** dialog opens first.

* Choose the **Image Set** at the top.
* The **Limit to Range of References** box starts with the books you are printing. Only pictures for these references are shown. Clear it to see all pictures.
* Type words in **Search** to find pictures by keyword or title.
* Tick artists in the artist list to show only their pictures.
* Click **Search + Update Images** (or press Enter) after you change the search or references.
* Sort by **Scripture Reference** or by **Frequency of Use**.
* Move the mouse over a picture to see its number, artist, description and references. Right-click a picture to see a larger preview.
* Pictures with a peach-coloured background are already in your PicList.
* Click pictures to select them, then click **Add Images to PicList**.

The new pictures are anchored at their Bible reference, with **Column Width** and top-left position. Then go to the **Details** sub-tab and type a caption for each one.

## 10.8 Download & Install Image Sets dialog

This dialog lists the image sets that PTXprint can download. Tick the sets you want and click **OK**. Sets that are already installed show **Installed** and cannot be ticked. Some sets show their terms of use; you must agree to the terms before the set is installed. You need an internet connection, and some sets are large.

**Install from ZIP file...** installs a set from a ZIP file on your computer. This is useful at a workshop: download the file once and share it. A ZIP file that contains only pictures (and no image-set information) is unpacked into the project's `local\figures` folder.

## 10.9 Illustration Credit Overlay dialog

Open this dialog with the **© ...** button on the **Details** sub-tab. It sets a small credit line that is printed on top of the picture. Some artists (for example David C Cook) require this.

* **Image Credit Text** – the text. Type `(c)` for ©, or `dcc` for the David C Cook credit.
* **Vertical Position** and **Horizontal Position** – which corner or edge of the picture.
* **Rotation** – turn the text to run up or down the side of the picture.
* **Background Box** – no box, a light box or a dark box behind the text, or the name of your own style.
* **Apply to ALL images in this series** – use the same text for all pictures of the same series (the same two letters at the start of the file name).
* **Overwrite any existing settings** – also replace the credit on pictures that already have one.

The credit is stored with the picture file, so it applies in all configurations of the project. The font, size and colour come from the `x-credit` style; click the **\x-credit** link to change it on the **Styles** tab.

## 10.10 Add Map dialog

Click **Add Maps...** to add map pages at the end of the publication.

1. Choose the **Book Code for Maps** (usually **XXM**).
2. Click **Select Map...** and choose the map file.
3. Type a **Caption** if you want one, and set **Scale** and **Rotation**.
4. Click **Size and Position...** to choose the frame size and position (the same dialog is used for sidebars). The code you choose is shown in the box beside it.
5. Click **Add Another Map** to add this map and start the next one, or **OK - Done!** to add it and finish.

PTXprint adds each map to the PicList (anchors `XXM map01`, `XXM map02` ...), writes one page for each map into the map book, ticks **Include Maps** on the **Peripherals** tab, and adds the map book to the list of books to print. Use **Edit Maps...** to look at the map book on the **View+Edit** tab.

## 10.11 Common tasks

### Show the pictures that are in the Paratext text

1. On the **Pictures** tab, **Global Options** sub-tab, tick **Include Pictures (illustrations)**.
2. Make sure the view is **Regular** or **Full** (so that you can see the picture table).
3. Click **Generate...**. If a dialog opens, choose **Append Pictures to PicList From These Books**, keep **Protect existing PicList settings** ticked, and click **OK**.
4. Look for grey rows in the table (missing files) and fix them (see "Common problems").
5. Print.

### Move a picture to another place on the page

1. Select the picture in the table. Open the **Details** sub-tab.
2. Set **Frame Size** first, then **Vertical Position**, then **Horizontal Position**.
3. Click **Position** (beside **Image**) to see a small drawing of the position.
4. Print again to check.

### Move a picture to another page

1. Select the picture and open the **Details** sub-tab.
2. Change the verse in **Anchor Ref** to a few verses earlier (to move it back) or later (to move it forward). Keep the dot between chapter and verse: `LUK 2.7`.
3. Print again.

### Make a picture smaller and let the text flow around it

1. Select the picture. On the **Details** sub-tab, set **Frame Size** to **Column Width**.
2. Set **Vertical Position** to **Cutout** and **Horizontal Position** to **Left** or **Right** (or **Inner**/**Outer**).
3. Set **Scale** to about 40%.
4. Set **Number of Lines** to the line where the picture should start (0 = the first line of the paragraph).
5. Print again.

### Add a new picture from the catalogue

1. Click **Show Catalogue...**.
2. Choose the **Image Set**. Type a word in **Search**, or check the references in **Limit to Range of References**, and click **Search + Update Images**.
3. Click the pictures you want, then click **Add Images to PicList**.
4. For each new picture, type the **Caption** on the **Details** sub-tab, and check the **Anchor Ref**.

### Use high-quality pictures for the final PDF

1. Put the high-resolution files in the project's `local\figures` folder, or tick **Use Other Location** and click **Picture Folder...** to choose their folder.
2. On **Global Options**, choose **High Resolution (Larger File)**.
3. Print, and check that the missing-pictures count is 0.

### Make a small PDF to send by email

1. On **Global Options**, choose **Low Resolution (Smaller File)**.
2. If the file must be even smaller, tick **Use Place-holders (Smallest PDF File)**.

### Print the picture credits in the colophon

1. On the **Peripherals** tab, tick **Colophon at End of Publication**.
2. Make sure the colophon text contains `\zimagecopyrights`.
3. For pictures that do not show **Automatic** on the **Details** sub-tab, type the credit in **Copyright Attribution**.
4. Print. PTXprint lists each artist with the pages of their pictures.

### Add maps at the end of the book

1. Click **Add Maps...**.
2. Follow the steps in the "Add Map dialog" section above.
3. Click **OK - Done!**, then print.

## 10.12 Common problems

**The Pictures tab shows no table, or no Details sub-tab.**
The table and the **Details** and **Checklist** sub-tabs are only shown in the **Regular** and **Full** views. Change the view level. Also check that **Include Pictures (illustrations)** is ticked.

**No pictures appear in the PDF.**
* **Include Pictures (illustrations)** is not ticked. Tick it.
* The PicList is empty. Click **Generate...**. (Pictures in the Paratext text are only used after they are in the PicList.)
* **Use Place-holders** is ticked. Untick it.
* The **Print** box on the **Details** sub-tab is not ticked for these pictures.

**Some pictures are missing.**
* The row is grey in the table: PTXprint cannot find the file. Check the **Filename**. Make sure the file is in the project's `figures` or `local\figures` folder, or tick **Use Other Location** and choose the folder with **Picture Folder...**.
* **Image Types** contains only some types (for example only `TIF`), and the file is a different type. Clear **Image Types**.
* The picture's book is not one of the books you are printing.
* **Omit Missing Pictures** hides the problem. Look at the missing-pictures count and list on **Global Options** after printing.

**A picture I added with Add is not found.**
The PicList stores only the file name. If you chose a file from a folder that PTXprint does not search, copy the file into the project's `local\figures` folder, or set that folder with **Use Other Location**.

**A picture appears on the wrong page.**
A picture at the top or bottom of a page goes on the same page as its anchor only if there is room. Change the **Anchor Ref** by a few verses. Pictures that are too large also move to a later page; reduce the **Scale**.

**I cannot choose the position I want.**
The lists depend on each other. **Span Width** only allows **Top**, **Bottom** and **Below Notes**, and no horizontal position. **Center** is only offered for **Before Verse**, **After Paragraph** and the page sizes. Choose the **Frame Size** first.

**The picture is too big, or the row is red.**
The picture is taller than fits on the page. Reduce the **Scale**, or use **Column Width** instead of **Span Width**.

**A cutout picture jumps between two places each time I print.**
This can happen when the anchor is near the end of a paragraph. Choose an earlier anchor in the same paragraph and increase **Number of Lines**.

**Mirror is greyed out.**
On the **Checklist** sub-tab, **Never mirror** or **Always mirror** is chosen for this picture. Choose **OK to mirror** to use the **Mirror** list again.

**My changes to captions in Paratext do not show.**
PTXprint uses its own PicList. Click **Refresh List** to copy the captions and references again. Your size and position settings stay the same.

**Changes in PTXprint do not appear in Paratext.**
This is normal. PTXprint never changes the Paratext text. To copy a picture into Paratext, right-click its row and choose **Copy \fig String to Clipboard**, then paste it in Paratext.

**The copyright text is missing or wrong.**
* The colophon must contain `\zimagecopyrights` (**Peripherals** tab).
* For pictures that are not from a known series, type the credit in **Copyright Attribution**.
* If **Sensitive Project** is ticked (on the **Advanced** tab), PTXprint uses a shorter credit wording for some artists.
* By default, the most common artist is described as "all other illustrations". To list every artist with all pages, tick **Show comprehensive illustration credits** (on the **Advanced** tab, **Other** sub-tab, in the **Pictures, Figures, Images, Sidebars** area).

**I want the caption above the picture, or the reference before the caption.**
On the **Advanced** tab, **Other** sub-tab, in the **Pictures, Figures, Images, Sidebars** area, tick **Show Caption Before Image** or **Ref Before Caption**.

## 10.13 Settings reference

### Generate PicList (dialog)

#### OK

Button · Regular+ · `btn_gnr8pl_ok`

Generates the PicList with the options chosen in the dialog.

#### Cancel

Button · Regular+ · `btn_gnr8pl_cancel`

Closes the dialog without changing the PicList.

#### When Generating PicList

##### Append Pictures to PicList From These Books

Radio · Mini+ · `r_generate_selected`  
Also: Generate PicList: Append to existing list

> This option will ADD to any existing entries in the PicList and/or replace entries for the book(s) listed below.

Pictures of other books stay as they are. This is the safe choice.

##### Include Pictures From ALL Books

Radio · Mini+ · `r_generate_all`  
Also: Generate PicList: Replace existing list

> This option will REPLACE ALL entries in the existing PicList. Do you really want to do this?
>
> If in doubt, then click Cancel.

If **Protect existing PicList settings** is not ticked, all your changes to sizes and positions are lost.

##### Randomly Position Pictures on Page

Checkbox, on · Mini+ · `c_randomPicPosn` · cfg `project/randompicposn`  
Also: Generate PicList: Randomly position pictures on page

> By default all illustrations are placed in the top-left corner of a page (when double columns are used) and at the top in single column mode.
>
> Checking this option will randomly position the illustrations on the page (using top-left, top-right, bottom-left and bottom-right).
>
> You can change the location of pictures later if needed.

It only affects pictures that have no position yet.

##### Protect existing PicList settings

Checkbox, on · Regular+ · `c_protectPicList`  
Also: Generate PicList: Protect existing PicList settings

> When synchronizing the pictures from the Paratext files with PTXprint's PicList, don't change any of the (layout and size) settings and don't delete any pictures no longer found in the Paratext USFM text.

Only new pictures are added. Keep it ticked unless you want to start again from the Paratext text.

### Select Images... (dialog)

#### Download Image Set...

Button · Regular+ · `btn_getImageSet`  
Also: Download an Image Set from an online source

> If you don't already have appropriate scripture illustrations, then you can download an Image Set which contains low-resolution illustrations for trial publications from one of the links.

Opens the **Download & Install Image Sets** dialog.

#### Request Access...

Button · Regular+ · `btn_requestIllustrations2`

> Request for Access to High Quality Illustrations/Maps in the SIL repository.
>
> Click this button to fill in the form requesting access to the illustrations used in the current publication.
>
> After completing and submitting the online form you should receive an immediate response by email.

The same online form as **Request Access...** on **Global Options**.

#### Add Images to PicList

Button · Regular+ · `btn_imagePicker_ok`  
Also: Add Images to Current Configuration's PicList

> Add the selected images to the current Configuration where an appropriate caption should be added and other image properties selected.

Each picture is anchored at its Bible reference, with **Column Width** and top-left position. Then type a caption for each one on the **Details** sub-tab.

#### Cancel

Button · Regular+ · `btn_imagePicker_cancel`

Closes the catalogue without adding pictures.

#### Limit to Range of References

Text box · Regular+ · `t_artRefRange`

Shows only pictures for these references. It starts with the books you are printing. You can type ranges such as `GEN 1-3; MRK`, with 3-letter book codes. Clear the box to see all pictures in the set. Press Enter or click **Search + Update Images** to apply it.

#### Search – Image Selection Dialog: Search for an image by keyword

Search box · Regular+ · `t_artSearch`

Searches keywords and titles, for example `boat` or `shepherd`. Press Enter or click **Search + Update Images** to apply it. Clear the box to show all pictures again.

#### Image Set

Drop-down · Regular+ · `ecb_artPictureSet`  
Choices: Default

PTXprint remembers your last choice. To get more image sets, click **Download Image Set...**.

#### Enter a name for the configuration to be saved.

Text box · Regular+

> Enter a name for the configuration to be saved.
>
> Note that only Roman/Latin names are supported using: a-z A-Z, 0-9, parentheses, underscores and hyphens.
>
> Longer descriptions may be typed into the Notes field below.

#### Scripture Reference

Radio · Regular+ · `r_imgSort_ref`

> Sort the images according to the canonical order of scripture.

Uses the reference that matches your reference range.

#### Frequency of Use

Radio · Regular+ · `r_imgSort_pop`

> Sort the images based on how often other projects use them. The most popular illustrations appear at the top of the list.

The pictures used most often by other projects come first.

#### tv_artists

Table · Regular+ · `tv_artists`

The artists (picture series) in the image set. Tick one or more to show only their pictures. Untick all of them to show every artist.

#### Search + Update Images

Button · Regular+ · `btn_imgRefresh`

Updates the thumbnails after you change the search words or the reference range. It is only active when something has changed.

#### Print

Checkbox, on · Regular+ · `c_imgMediaP`

> Filter for illustrations that can be used in Print/PDF publications.

At the time of writing, this box does not change which thumbnails are shown.

#### App

Checkbox, off · Regular+ · `c_imgMediaA`

> Filter for illustrations that can be used in mobile phone Apps.

At the time of writing, this box does not change which thumbnails are shown.

#### Web

Checkbox, off · Regular+ · `c_imgMediaW`

> Filter for illustrations that can be used on websites.

At the time of writing, this box does not change which thumbnails are shown.

#### Reference

Label · Regular+ · `lb_imgRefs`

> Note that if a reference only contains a book and chapter number (with no specific verse mentioned), then the illustration will be placed in the middle of the chapter.

The references of the picture under the mouse. The reference in bold is the one PTXprint will use as the anchor. References in red already have this picture in your PicList.

#### Clear Selection

Button · Regular+ · `btn_imgClearSelection`

Unselects all the selected thumbnails, so you can start your choice again.

### Download & Install Image Sets (dialog)

#### OK

Button · Regular+ · `btn_imgSet_ok`

Downloads and installs the ticked image sets. This can take a while. When it is finished, the catalogue opens.

#### Cancel

Button · Regular+ · `btn_imgSet_cancel`

Closes the dialog without downloading anything.

#### Select All / None

Checkbox, off · Regular+ · `c_imgSet_selectAll`

Some sets are large downloads.

#### tv_imagesets

Table · Regular+ · `tv_imagesets`

The image sets that you can download, with artist, style, size and licence. Tick the sets you want, then click **OK**. Sets marked **Installed** cannot be ticked. Hover over a row for more information.

#### Install from ZIP file...

Link · Regular+ · `btn_installFromZip`

> Install an image set from a local ZIP file. Useful for offline installations or shared image sets at workshops (avoids repeated large downloads).

If the set has terms of use, you must agree to them. A ZIP file with only pictures in it is unpacked into the project's `local\figures` folder.

### Illustration Credit Overlay (dialog)

#### OK

Button · Regular+ · `btn_ovrly_ok`

Saves the credit overlay settings for this picture (and for the series, if chosen). The credit is kept even if you close PTXprint without selecting another picture first.

#### Cancel

Button · Regular+ · `btn_ovrly_cancel`

Closes the dialog without changing the credit.

#### Vertical Position – Image credit dialog: Vertical position of text

Drop-down · Regular+ · `fcb_plCreditVpos`  
Choices: Top | Center | Bottom | Fill

Where the credit sits on the picture.

#### Horizontal Position – Image credit dialog: Horizontal position of text

Drop-down · Regular+ · `fcb_plCreditHpos`  
Choices: Left | Center | Right | Inner | Outer

Inner and outer are useful if the picture may be mirrored or appear on both odd and even pages.

#### Background Box – Image credit dialog: Background color

Drop-down · Regular+ · `ecb_plCreditBoxStyle`  
Choices: None | Light | Dark

> Specify the kind of box (Light/Dark background) or enter the name of a style which should be applied. By selecting a (custom) style, you can change multiple parameters at once: font, size and color.

When you open the dialog again, a credit with no box shows **None**.

#### Rotation – Image credit dialog: Rotation of text

Drop-down · Regular+ · `fcb_plCreditRotate`  
Choices: None | Anti-clockwise | Clockwise

> Sometimes the credit text needs to be rotated.

Useful when the credit is at the left or right edge.

#### Image Credit Text – Image credit dialog: Credit (copyright) text

Text box · Regular+ · `t_plCreditText`

> Type the text for the Credit to be overlaid on the image. Note that there are shortcuts:  
>    (c)   --> ©  
>    dcc  --> © David C Cook  
>        or --> © DCC   (if Sensitive Project is set)

Keep it short; it is printed in small letters.

#### Apply to ALL images in this series

Checkbox, off · Regular+ · `c_plCreditApply2all`  
Also: Image credit dialog: Apply to all images in series

> The same Credit Overlay text can be applied to all images that match this illustration's filename (e.g. CN01234.tif, CN05654.tif, etc.) You can then adjust the position, background and rotation for specific illustrations later.
>
> Setting this option will not affect illustrations which already have Credit Overlay settings.

A series is the pictures with the same two letters at the start of the file name, for example all `cn` pictures. To change pictures that already have a credit, also tick **Overwrite any existing settings**.

#### \x-credit

Link · Regular+ · `lb_style_x-credit`

> Click to edit the Credit Overlay properties on the Styles tab.

Change the font, size and colours of all credit overlays there.

#### Overwrite any existing settings

Checkbox, off · Regular+ · `c_plCreditOverwrite`  
Also: Image credit dialog: Overwrite existing values · Needs: “Apply to ALL images in this series”

> WARNING:  
> If this option is checked, it will disregard any previous settings, and overwrite them with the new overlay information, position and other parameters.

Use with care: earlier settings for individual pictures are lost.

### Add Map (dialog)

#### Add Another Map

Button · Regular+ · `btn_mapAddAnother`

> Add as many maps as needed, one at a time.

Adds the current map and clears the form for the next one. Finish with **OK - Done!**, because the map book is only written then.

#### OK - Done!

Button · Regular+ · `btn_addMap`

Adds the current map (if a file is chosen) and finishes. PTXprint writes the map pages into the map book, ticks **Include Maps** on the **Peripherals** tab, and adds the map book to the books to print.

#### Cancel

Button · Regular+ · `btn_gnr8cover_cancel1`

Closes the dialog. The map book is not written. Maps already added with **Add Another Map** may still be in the PicList; delete them there if you do not want them.

#### Book Code for Maps – Maps: Book code to be used to store map details

Drop-down · Regular+ · `fcb_ptxMapBook`  
Choices: XXM | XXA | XXB | XXC | XXD | XXE | XXF | XXG | BAK

> Select the extra book code to be used for the list of maps.
>
> An extra book (e.g. XXM) can be used to store map details. If you prefer to use one of the other standard Paratext books XXA...XXG then select it here. If the book already exists, the new maps are added at the end of it.

**XXM** is the usual choice. Choose another book only if XXM is used for something else.

#### Add Map

##### Scale – Scale Map Size

Number · Regular+ · `s_mapScale`  
Values: 0.01–4 (default 1)

1 means the full size of the frame.

##### Border – Maps: Select Ornamental Border

Drop-down · Regular+ · `fcb_coordBorder`  
Choices: None | Han3 | Map Edge A | Map Edge B

> A selection of ornamental borders are available to choose from, to be drawn around the map.

At the time of writing, PTXprint does not use this setting when it adds the map.

##### Select Map...

Button · Regular+ · `btn_selectMap`  
Also: Maps: Select the map image file

Chooses the map image file (PNG, JPG, PDF or TIF). A preview is shown in the dialog.

##### Caption – Picture: Caption

Text box · Regular+ · `t_mapCaption`

> By default the caption will appear below the picture. To show it above the picture, tick 'Show Caption Before Image' on the Advanced tab (Other sub-tab, Pictures, Figures, Images, Sidebars).
>
> Note that captions are NOT processed by any changes specified in the PrintDraftChanges.txt file.

Optional. Leave it empty if the map fills the whole page to the edge.

##### Rotation – Maps: Rotation of map image

Drop-down · Regular+ · `fcb_mapRotate`  
Choices: None | Anti-clockwise | Clockwise

> Rotate the map image by 90 degrees (anti-clockwise or clockwise) if needed.

Use it for a wide map on a tall page.

##### Size and Position...

Button · Regular+ · `btn_mapSizePosition`

Opens the **Size and Position** dialog to choose the frame size (for example a full page) and the position of the map. The result is shown as a code in the box beside the button.

##### t_mapPgPos

Text box · Regular+ · `t_mapPgPos`

The position code chosen with **Size and Position...**, for example `Pc` (a page of its own, centred).

##### Spread

Checkbox, off · Regular+ · `c_mapSpread`  
Also: Spread Map Out Across Both Pages

> Only enable this option if the map needs to be spread out across both pages.

At the time of writing, PTXprint does not use this setting when it adds the map.

### Pictures

#### tv_picListEdit

Table · Regular+ · `tv_picListEdit`  
Shown when: “Include Pictures (illustrations)”

One row for each picture in this configuration. Double-click a row to open **Details**; right-click it for more actions. Red text means the picture is too tall for the page; a grey row means the file cannot be found.

#### Del

Button · Regular+ · `btn_plDel`  
Also: Delete picture(s) from PicList · Shown when: “Include Pictures (illustrations)”

> Click to immediately delete the currently highlighted picture(s). No confirmation will be asked for!

There is no undo, so check the selection first. It does not change the Paratext text or the picture file.

#### Generate...

Button · Regular+ · `btn_plGenerate`  
Also: Generate the PicList · Shown when: “Include Pictures (illustrations)”

> This button will (re-)generate the PicList from the USFM \fig ... \fig* definitions.
>
> If you just want to (re-)generate the PicList for a single book, then select that book on the Basic tab.

If no PicList exists yet, PTXprint makes it at once; otherwise the **Generate PicList** dialog asks what to do. Use it after pictures are added in Paratext.

#### Add

Button · Regular+ · `btn_plAdd`  
Also: Add picture to PicList · Shown when: “Include Pictures (illustrations)”

> Click to add another picture to the PicList. You will need to fill in all the details in the area below.

PTXprint asks for a picture file, adds a row and opens the **Details** sub-tab. Then type the **Anchor Ref** (for example `JHN 3.16`) and a caption. Only the file name is saved, so the file must be in a folder that PTXprint searches.

#### Refresh List

Button · Regular+ · `btn_refreshCaptions`  
Also: Refresh (reload) picture captions from Paratext · Shown when: “Include Pictures (illustrations)”

> Refresh Captions:  
> If you have edited the picture captions within the Paratext USFM files but those changes are not being reflected here, then click this button to refresh the captions.
>
> Note that only the Captions and Verse Refs will be updated. All other size and position settings will remain unchanged.

Use it after captions are corrected in Paratext.

#### Add Maps...

Button · Regular+ · `btn_addMaps2`  
Also: Add Maps to the Publication · Shown when: “Include Pictures (illustrations)”

> Maps for the end of the publication can be added to one of the XX* books or to the XXM book using this dialog.

Opens the **Add Map** dialog.

#### Edit Maps...

Button · Regular+ · `btn_editMaps2`  
Also: Edit Maps module · Shown when: “Include Pictures (illustrations)”

> Switch to the View+Edit tab to show/edit the Maps module.

Does nothing if the map book (for example XXM) does not exist yet; use **Add Maps...** first.

#### Show Catalogue...

Button · Regular+ · `btn_getPictures`  
Shown when: “Include Pictures (illustrations)”

> Browse the catalogue of commonly used Bible illustrations from a range of different artists.

Opens the **Select Images** dialog, where you add pictures from an image set to the PicList. If no image set is installed, the download dialog opens first.

#### Show Active Books

Checkbox, off · Regular+ · `c_filterPicList` · cfg `config/filterpics`  
Also: Only show pictures used in the set of active books · Shown when: “Include Pictures (illustrations)”

> Select this option to only display the pictures from the books that are currently in focus to be printed. When unchecked, then the list will show pictures from ALL the books in the project that have been added to the PicList. If pictures of a certain book are missing, then you may need to select that book and Generate the PicList details just for *that* book.

The books selected for printing are set on the **Basic** tab. This only changes what you see; it does not delete anything.

#### Image

Radio · Regular+ · `r_image_preview`  
Also: Show preview of pictures · Shown when: “Include Pictures (illustrations)”

> Display the picture currently in focus. Note that this is dependent on the image being located in the specified folder(s).

If the box is empty, PTXprint could not find the picture file. Hover over the preview to see the file path.

#### Position

Radio · Regular+ · `r_image_location`  
Also: Show position of picture on page · Shown when: “Include Pictures (illustrations)”

> Show the relative position of the picture on the page. When Inner/Outer is used, the position displayed represents the odd/right-hand page of a spread.

Use it to check the **Frame Size** and position settings before you print.

#### Global Options

Label · Basic+ · `lb_settings`  
Shown when: “Include Pictures (illustrations)”

> Overview of the Pictures used in the publication.

Settings for every picture: resolution, captions, missing pictures and the picture folders.

#### Details

Label · Regular+ · `lb_details`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Use this tab to change the position, location, size or orientation of the images.
>
> Note: Any changes you make here will NOT be reflected in the Paratext USFM files. So if you are changing an illustration, its caption or frame size (column or span), then it is advisable to do so in Paratext before regenerating the PicList here.

The settings of the picture selected in the table, such as anchor, caption, size and position.

#### Checklist

Label · Regular+ · `lb_checklist`  
Shown when: “Include Pictures (illustrations)”

> This tab encourages you to think through the appropriateness of the pictures used in this publication, as well as other contexts.

Records whether each picture is clear, culturally acceptable and approved. When this sub-tab is open, a **Filter Checklist** area appears above the table.

#### Filter Checklist

##### Filter pictures for checklist

Drop-down · not shown · `fcb_chklstFilter`  
Choices: All | All Unknown / Unchecked | Any Unknown / Unchecked | Approved · Shown when: “Include Pictures (illustrations)”

> The list of pictures can be filtered according to the status of the checking values.

**All Unknown / Unchecked** – no question answered yet. **Any Unknown / Unchecked** – at least one question still open. **Approved** – the approved pictures. Only shown when the **Checklist** sub-tab is open.

##### Exclude Matched

Checkbox, off · not shown · `c_picCheckInvFilter`  
Also: Exclude (don't show) pictures that match filter · Shown when: “Include Pictures (illustrations)”

> Flip the results of the filtered list to exclude any items that match.

For example, choose **Approved** and tick this to see all pictures that are not approved yet.

#### Global Options

##### Include Pictures (illustrations)

Checkbox, off · Basic+ · `c_includeillustrations` · cfg `document/ifinclfigs`, `document/ifusepiclist`, `document/includeimg`  
Shown when: “Include Pictures (illustrations)”

> This setting enables/disables all the other settings relating to pictures.
>
> Note that it is important to provide proper copyright attribution for the illustrations used in a publication, and this can be done very easily using the \zimagecopyrights magic code within the Colophon (see the Peripherals tab for details).

When ticked, PTXprint loads the PicList for this configuration and prints the pictures. When not ticked, the **Details** and **Checklist** sub-tabs are hidden. Turning it on can make printing slower.

##### Include Pictures (illustrations)

###### High Resolution (Larger File)

Radio · Regular+ · `r_pictureRes_High` · cfg `document/picresolution=High`  
Also: Use high-resolution pictures · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> If this option is selected, PTXprint prefers TIF, then PNG, then JPG files (and the larger file if there are two of the same type).
>
> The original higher-quality illustrations are usually larger (.TIF .PNG or .PDF files) and are stored in the local\Figures folder so that they are not shared via Send/Recv. If these are used, the resulting PDF could be very large, and therefore difficult to share electronically, but the image quality will be as good as possible.

Use this for the final print PDF. **Request Access...** is only available with this option.

###### Low Resolution (Smaller File)

Radio · Regular+ · `r_pictureRes_Low` · cfg `document/picresolution=Low`  
Also: Use low-resolution pictures · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Paratext stores low resolution .JPG versions of illustrations in the project's "Figures" folder. If these are used, the file size of the resulting PDF will be relatively small, and therefore easy to share, but the image quality will be low.

Use this for drafts. PTXprint prefers JPG files and, of two files of the same type, the smaller one. Pictures may look blurred when printed.

###### Use Place-holders (Smallest PDF File)

Checkbox, off · Regular+ · `c_figplaceholders` · cfg `document/iffigplaceholders`  
Also: Pictures: Only show empty place-holders · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Use this option to include an empty box wherever illustrations would be placed in the final PDF.
>
> WHY would someone want to do this? It is sometimes necessary to generate the smallest possible PDF file (usually in order to send by e-mail) or to produce a PDF to be printed without illustrations.

The page layout stays the same, so you can check it with a very small PDF. Untick it for the final PDF.

###### Omit Pictures Only Meant for Web or App

Checkbox, on · Regular+ · `c_figexclwebapp` · cfg `document/iffigexclwebapp`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Only allow illustrations with the 'P'rint attribute.
>
> If the illustrations have been marked up with the w/a/p notation, then it is easy to exclude any illustrations that do not have the 'p' attribute.  Note: w= web, a=app, p=print.

Keep it ticked for printed publications.

###### How?

Link · Regular+ · `lb_omitPics`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Open a web page that explains how to mark pictures in Paratext for print, web or app.

Opens a help web page.

###### Omit Captions

Checkbox, off · Regular+ · `c_fighidecaptions` · cfg `document/iffigshowcaptions`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> If you want to suppress the picture captions from being displayed below the picture, then check this option.

Also removes the caption references.

###### Omit References (ch:vs)

Checkbox, off · Regular+ · `c_fighiderefs` · cfg `document/iffighiderefs`  
Needs: “Include Pictures (illustrations)” · Greyed out by: “Omit Captions” · Shown when: “Include Pictures (illustrations)”

> If you only want to suppress the reference part of the caption, then check this option. Note that it is not possible to just have the references without the captions.

The caption text is kept.

###### Omit Missing Pictures ...

Checkbox, on · Regular+ · `c_skipmissingimages` · cfg `document/iffigskipmissing`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Rather than aborting the PDF export process, pre-process the list of illustrations and skip/ignore/remove any which are not found in the specified location of image files.
>
> If Pictures are missing after preparing a PDF, then they will be listed in the section below.

After printing, the number of missing pictures is shown next to this option. Keep it ticked, but check the count before the final print.

###### Remove Image Borders

Checkbox, off · Basic+ · `c_cropborders` · cfg `document/iffigcrop`  
Also: Pictures: Remove Image Borders · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Some images have a thin line on one or more of the edges of the picture. Enable this option to automatically crop these unwanted lines from the edge of pictures. Note that this setting affects ALL images, not just those with lines.

Check that no picture loses part of its content. The pictures are converted to JPG when this is on.

###### Request Access...

Button · Regular+ · `btn_requestIllustrations`  
Needs: “High Resolution (Larger File)”, “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Request Access to High Quality Illustrations/Maps in the SIL repository.
>
> Click this button to fill in the form requesting access to the illustrations used in the current publication.
>
> After completing and submitting the online form you should receive an immediate response by email with a link to download the illustrations (if approved).

PTXprint fills in the project name and the list of pictures. You must add your email and supervisor details.

###### Get Permission...

Button · Regular+ · `btn_requestPermission`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> If you are publishing (i.e. more than 50 copies) any material with illustrations that require prior permission to be obtained before publishing, then click this button to automatically fill in the form requesting permission.
>
> Note that any missing information will need to be filled in on the Peripherals tab before the form can be submitted.
>
> After filling in any remaining details, you will need to submit the Google form and wait for a response.

PTXprint fills in the list of pictures and the publication details. If country, language or number of copies are missing, PTXprint opens the **Peripherals** tab so that you can fill them in first.

###### Use Other Location

Checkbox, off · Basic+ · `c_useCustomFolder` · cfg `document/customfiglocn`  
Also: Use pictures from a particular folder · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> The following locations are scanned for pictures:  
>   My Paratext ... Projects\\figures  
>   My Paratext ... Projects\\local\figures  
>   Users\...\AppData\Local\SIL\ptxprint\imagesets
>
> If your pictures are in a different folder, then enable this option and select a Picture Folder to be scanned in addition to the folders listed above. Note that ALL subfolders are also scanned unless you explicitly enable the 'Exclude Subfolders' option.

When you tick it and no folder is chosen yet, PTXprint asks for the folder.

###### Picture Folder...

Button · Basic+ · `btn_selectFigureFolder` · cfg `document/customfigfolder`  
Also: Select the folder which contains pictures · Needs: “Use Other Location”, “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Select another folder which contains pictures. PTXprint will also scan the selected folder (and all its sub-folders) looking for all the required illustrations in the Picture List.

The chosen folder is shown beside the button.

###### Exclude Subfolders

Checkbox, off · Regular+ · `c_exclusiveFiguresFolder` · cfg `document/exclusivefolder`  
Also: Pictures: Exclusively Use Selected Folder · Needs: “Use Other Location”, “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> PTXprint normally searches all the sub-folders of the specified folder locations for the pictures it needs.
>
> If you would prefer that it only searches in the folder specified directly (and NOT look in any subfolders) then select this option. This should speed up searches for images, but may result in some images not being found at all.

This applies when you print, when you make an archive and when PTXprint looks for the PicList files. The downloaded image sets are still searched fully, because each set is in a subfolder of its own. It is unticked automatically when you untick **Use Other Location**.

###### Image Types – Pictures: Preferred image types

Text box · Regular+ · `t_imageTypeOrder` · cfg `document/imagetypepref`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> If multiple versions of an image are located (hk12345B.jpg, hk12345C.png or hk12345B.tif) then which one of these different image types should be used in the publication?
>
> If in doubt, leave this box empty. Then it will use one of two defaults:
>
> 1. Low Resolution Default Order:  
> JPG PNG TIF BMP PDF  (use JPGs first, if none then PNGs, TIFs etc.)
>
> 2. High Resolution Default Order:  
> TIF PNG JPG BMP PDF (use TIFs first, if none then PNGs, JPGs etc.)
>
> Or manually type in a custom order, for example:  
> PDF TIF PNG (use PDFs first, otherwise TIFs, or PNGs)  
>   or JPG  (only use JPGs - ignore all other file types)  
>   or TIF  (only use TIFs - ignore all other file types)
>
> NOTE: TIF files are converted internally to hi-res JPGs.
>
> You can specify your preference for which kinds of images are used. PTXprint will search multiple locations for any matching images, and use the one that best matches your preferences (if found).
>
> If the box is left empty, it will default to the following search sequences:  
>    jpg > png > tif > bmp > pdf   - for smallest file size or  
>    tif > png > jpg > bmp > pdf   - for largest file size

Separate the types with spaces.

#### Details

##### Anchor Ref – Picture: Anchor reference

Text box · Regular+ · `t_plAnchor`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> The anchor specifies what page in a book a picture will appear on. It appears on the same page as its anchor in the text. You can alter the Anchor Ref by a few verses to change the page on which it appears.
>
> An Anchor Ref must consist of a book code, perhaps followed by L or R (in the case of a diglot), then a space, then an in-book location which contains a dot (period). In a scripture book, the in-book location is Chap.Verse where the Verse matches the \v value precisely. In other books, the in-book location can be anything as long as it is unique in that book and contains a dot (period).
>
> Anchor Refs for Diglots use the L or R suffix on the 3-letter book code to indicate whether the picture is to be associated with the Primary (L) text or the Secondary (R) text.
>
> In the glossary book (GLO) there is special support for \k Keywords\k* where in-book location of k.keyword(s) will anchor a picture to the corresponding term. The in-book location must match the value of the \k Keyword or phrase\k* with its spaces removed. For example,
>
>     GLO k.Altar - would link it to \k Altar\k*  
>     GLO k.JohntheBaptist - would link a picture to  
>                a glossary entry \k John the Baptist\k*
>
> You can copy-and-paste a glossary word or phrase after typing GLO k. and PTXprint will automatically strip the spaces for you.
>
> Where there are no intervening anchors, you can anchor to the Nth paragraph of e.g. poetry or a keyterm definition, by specifying the paragraph number after an = sign. For example, GLO k.Harp=2 or PSA 23.4=3. This can avoid the need to insert an explicit milestone to anchor a cutout if there is a page or column break after the start of the verse.

PTXprint changes `:` into `.` and the book code into capital letters for you. If the anchor is empty, you cannot move to another row. See "Details" above for the diglot, glossary and paragraph forms.

##### Caption Ref – Picture: Caption reference

Text box · Regular+ · `t_plRef`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> The reference in the caption can be a single Ch:Vs or a range of verses 6:17-29. This Caption Ref is different from and independent of the Anchor Ref setting.
>
> By default, the caption will be followed by a Ch:Vs reference in parentheses ( ).
>
> To put the Caption Ref BEFORE the caption text, tick 'Ref Before Caption' on the Advanced tab (Other sub-tab, Pictures, Figures, Images, Sidebars).
>
> To prevent Caption Refs from appearing globally, use the Pictures > Global Options tab option:  
>     'Omit References (ch:vs)'

For example `4:39`.

##### Description: (Alt Text) – Picture: Description (alternative text)

Text box · Regular+ · `t_plAltText`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

A short description of what the picture shows. It helps you recognise the picture in the table. Pictures added from the catalogue get the catalogue title here.

##### Filename – Picture: Image filename

Text box · Regular+ · `t_plFilename`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Note that any changes you make to the filename here will NOT automatically be updated in the Paratext USFM files. Please edit/fit the figure information manually in Paratext if you change things here in PTXprint.

The file name only, without a folder. PTXprint looks for it in the picture folders. Changing it updates the preview and the missing-file check.

##### Copyright Attribution – Picture: Copyright attribution

Text box · Regular+ · `t_plCopyright`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> There are several shortcuts you can use:  
>    (c) --> ©  the copyright sign  
>    (r) --> ®  to denote registered trademarks  
>    (tm) --> ™  to denote trademarks in general
>
> For commonly used series of illustrations, PTXprint can automatically generate the appropriate copyright attribution statement(s) as part of the colophon text.
>
> For other less-known artists' you may enter the appropriate copyright information which is usually in the format of:  
>    by Artist Name © Year, Entity Name and License Type.

Used in the credits that `\zimagecopyrights` prints in the colophon. For known series this box is hidden and **Automatic** is shown instead.

##### Scale – Picture: Scale

Number · Regular+ · `s_plScale`  
Values: 5–200 (default 100) · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> An image (illustration) can be scaled to the given size. This is particularly useful for cutout images, and can prevent them from taking up too much space within the text.

100% fills the frame width. Use 30–60% for cutouts and small pictures. If the row turns red, the picture is too tall for the page; reduce the scale.

##### Vertical Position – Picture: Vertical position

Drop-down · Regular+ · `fcb_plPgPos`  
Choices: Top | Bottom | Below Notes | Before Verse | After Paragraph | Cutout · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Several options here are extensions to the normal USFM markup standard for illustrations and are not expected to work in other software. But PTXprint allows a greater level of control in placing pictures.
>
> Top: Above everything except the header line Bottom: Below all verse text (and footnotes in diglot) Below Notes: Below the footnotes (Span Width only) Before Verse: 'Here' where defined or before its Anchor Ref After Paragraph: After this paragraph Cutout: A notch/corner cut out of the text, starting at current line
>
> The above options may have other positioning parameters such as: Left, Right, Center, no. of lines (up or down).
>
> Several options here are extensions to the normal USFM markup standard for illustrations and are not expected to work in other software. But PTXprint allows a greater level of control in placing pictures.
>
> Top: Above everything except the header line Bottom: Below all verse text (and footnotes in diglot) Before Verse: 'Here' where defined or before its Anchor Ref After Paragraph: After this paragraph Cutout: A notch/corner cut out of the text, starting at current line
>
> The above options may have other positioning parameters such as: Left, Right, Center, no. of lines (up or down).

The choices depend on **Frame Size**: Span Width allows **Top**, **Bottom** and **Below Notes**; Column Width allows **Top**, **Bottom**, **Before Verse**, **After Paragraph** and **Cutout**; the page sizes allow **Top**, **Center** and **Bottom**.

##### Frame Size – Picture: Frame size

Drop-down · Regular+ · `fcb_plSize`  
Choices: Column Width | Span Width | Page (in Margins) | Page (to Edge) · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> The frame size determines the boundaries of where the picture will appear on the page.
>
> Span Width only allows a Top or Bottom vertical placement.
>
> Column Width allows several other more precise placement options: Before Verse, After Paragraph, or Cutout; and these can have Left/Inner or Right/Outer Horizontal positioning set.
>
> Page (in Margins) is intended for pictures that will cover an entire page (i.e. preventing any scripture text from being on that page), but will still show the header.
>
> Page (to Edge) is intended for pictures (or more commonly for maps) to fill the entire page, with no margins at all. Captions should not be used with 'Page (to Edge)' images.
>
> The frame size determines how large the picture will appear on the page.
>
> Span Width only allows a Top or Bottom vertical placement. Column Width allows several other more precise placement options: Before Verse, After Paragraph, or Cutout; and these can have Left/Inner or Right/Outer Horizontal positioning set.
>
> When using single column layout, there is no difference between Column Width and Span Width.

Choose this first, because it changes the choices in **Vertical Position** and **Horizontal Position**. Use **Page (to Edge)** for full-page maps.

##### Horizontal Position – Picture: Horizontal position

Drop-down · Regular+ · `fcb_plHoriz`  
Choices: Left | Center | Right | Inner | Outer | - · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> The options available here change based on the Frame Size and Vertical Position settings. So if you can't find an option you are looking for, then check those settings first.

Inner and outer keep a picture on the same side relative to the binding when pages are mirrored. Greyed out for **Span Width**. **Center** is only offered for **Before Verse**, **After Paragraph** and the page sizes.

##### Mirror

Label · Regular+  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> It is good typesetting practice to make people look outwards from the gutter, so you can set whether the image is to be mirrored just on odd pages or even pages.
>
> Some artists' pictures do not take into account the "dirty left-hand" culture. For example, it would be "awkward" to use a picture where Jesus is healing a person using his LEFT hand! What an insult!
>
> So this option allows the image to be mirrored (on both pages) in order to make the left become right. But you should check carefully to see what other unwanted side effects this mirroring may cause.
>
> Note: This option will be grayed out if the picture has the "Never Mirror" setting checked on the Checklist tab.

##### Mirror – Picture: Mirroring options

Drop-down · Regular+ · `fcb_plMirror`  
Choices: Never | Odd | Even | Always · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Never = The image will never be mirrored Odd = Mirrored only if image ends up on an odd page Even = Mirrored only if image ends up on an even page Always = Always mirrored (regardless of where it ends up)
>
> Note that if this option is grayed out, it is because you have already restricted the mirroring options on the Checklist tab.

**Odd** or **Even** may need the PDF to be made twice to be right. Check the flipped picture carefully: writing in it will be backwards.

##### Number of Lines

Label · Regular+ · `l_plOffsetNum`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Some vertical position options allow a picture to be moved up or down by a number of lines or paragraphs.
>
> -Negative (minus) values specify to move UP. +Positive (plus) values specify to move DOWN.
>
> Negative counts for cutouts raise the image, but the cutout will not affect earlier paragraphs. Note that negative and fractional paragraph counts are invalid.

The label for **Number of Lines**. It changes to "Number of paragraphs" when **Vertical Position** is **After Paragraph**.

##### Number of Lines – Picture: Lines to adjust vertically

Number · Regular+ · `s_plLines`  
Values: -24–24 · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Some vertical position options allow a picture to be moved up or down by a number of lines or paragraphs.
>
> -Negative (minus) values specify to move UP. +Positive (plus) values specify to move DOWN.
>
> Negative counts for cutouts raise the image, but the cutout will not affect earlier paragraphs. Note that negative and fractional paragraph counts are invalid.

Only used with **Cutout** and **After Paragraph**. For a cutout, it is the number of lines below the start of the paragraph where the picture starts (decimals allowed). For **After Paragraph**, it is the number of paragraphs (whole numbers only).

##### Print

Checkbox, off · Regular+ · `c_plMediaP`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Can be used in Print/PDF publications.

Untick it to leave this picture out of print without deleting it from the PicList. Greyed out if the artist's licence does not allow this use. If you untick **Print**, **App** and **Web**, all three stay unticked when you open the project again.

##### App

Checkbox, off · Regular+ · `c_plMediaA`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Can be used in mobile phone Apps.

It does not change the PDF. Greyed out if the artist's licence does not allow this use.

##### Web

Checkbox, off · Regular+ · `c_plMediaW`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Can be used on websites.

It does not change the PDF. Greyed out if the artist's licence does not allow this use.

##### Automatic

Label · Regular+ · `l_autoCopyAttrib`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> If the image is from the recognized set of pictures commonly used in Scripture publications, then there is no need to fill in the Copyright Attribution field, as this will be generated automatically for you.

Shown instead of the **Copyright Attribution** box for a series that PTXprint knows.

##### © ...

Button · Regular+ · `btn_overlayCredit`  
Also: Picture: Credit overlay options · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Credit Overlays... Some artists (e.g. David C Cook) require that each image has a copyright message printed on the image itself. The text and location can be set here.

Opens the **Illustration Credit Overlay** dialog.

##### Automatic – Picture: Credit overlay position and style

Text box · Regular+ · `t_piccreditbox`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Credit overlay position and style

The current overlay settings in short form: position, rotation and box (for example `bl,0,None`). Use the **© ...** button to change them.

##### Caption – Picture: Caption

Text box · Regular+ · `t_plCaption`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> By default the caption will appear below the picture. To show it above the picture, tick 'Show Caption Before Image' on the Advanced tab (Other sub-tab, Pictures, Figures, Images, Sidebars).
>
> Note that captions are NOT processed by any changes specified in the PrintDraftChanges.txt file.

Changes here are not copied back to Paratext.

##### \fig

Link · Regular+ · `lb_style_fig`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Click to edit the Figure Caption properties on the Styles tab.

Change the caption font, size and alignment there.

##### Extra – Picture: Additional attributes

Text box · Regular+ · `t_picXetex`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> One or more optional (x-xetex) attributes can be applied for rotation and/or PDF page selection. For example:  
> rotated 90     - anti-clockwise rotate=edge     - top to outside edge rotate=binding    - top to binding edge page=2     - select page 2 of multi-page PDF
>
> Multiple parameters should be space-separated:  
> rotate=binding page=2

The caption is not rotated.

#### Checklist

##### Questions to Consider

Label · Regular+  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Pictures are best used in situations where:  
> 1. The physical situation is not understood, or not common in the target culture.  
> 2. Where the physical situation is important to understanding the meaning of the passage (e.g., the type of clothing is often not important, but in some passages it might be).  
> 3. Where they help the reader to understand the passage.  
> 4. Where it entices the reader to read the passage.

##### Questions to Consider

###### Across Various Publications

Label · Regular+  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> First consider whether this picture is appropriate and culturally acceptable in any publications for this project.

###### Yes

Radio · Regular+ · `r_picclear_yes`  
Also: Picture checklist: What is happening is clear · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

This answer is shared by all configurations of the project.

###### No

Radio · Regular+ · `r_picclear_no`  
Also: Picture checklist: What is happening is NOT clear · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Is there anything confusing or misleading in this image that the reader might misunderstand if they look at this picture apart from the text? Yes and no are both appropriate answers as some images may need to be seen alongside text in order to be understood.

This answer is shared by all configurations of the project.

###### Unknown

Radio · Regular+ · `r_picclear_unknown`  
Also: Picture checklist: Not checked for clarity · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

The starting value. Pictures with this answer appear in the "Unknown / Unchecked" filters.

###### In This Publication

Label · Regular+  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Now consider whether there are any issues with using this picture in this particular publication (config-specific).

###### Is this image acceptable in your culture? – Picture checklist: Cultural acceptability

Drop-down · Regular+ · `fcb_picaccept`  
Choices: Unknown | Culturally Appropriate | Alien but Acceptable | Inappropriate · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Select the level to which this illustration is acceptable in the receptor culture.
>
> Be sure that there is nothing offensive or inappropriate in this image. This could be the way people are clothed, what actions they are doing, how they are depicted, etc. “Culturally Appropriate” means this image is in a style from this culture or a related one, “Acceptable” means this picture might be from a different culture or in a different style, but there are no issues using it. “Inappropriate” means there are issues that should prevent this image from being used. Answering “Inappropriate” will help avoid this image being used in other publications.

This answer is shared by all configurations of the project.

###### OK to mirror

Radio · Regular+ · `r_picreverse_OK`  
Also: Picture checklist: Can mirror if needed · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> It is fine to mirror the image if needed. It would not change the impact or response of the readers.

The **Mirror** list on the **Details** sub-tab can then be used freely.

###### Never mirror

Radio · Regular+ · `r_picreverse_never`  
Also: Picture checklist: Never mirror · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Ensure that this image is always shown as currently depicted in the preview. Do NOT allow it to be mirrored (reversed).

For example because it contains writing. The **Mirror** list on the **Details** sub-tab is set to **Never** and greyed out.

###### Always mirror

Radio · Regular+ · `r_picreverse_always`  
Also: Picture checklist: Always mirror · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Ensure that this image is always mirrored from what is currently shown in the preview. Therefore actions being done with the left hand will show as being done with the right hand, and vice versa.
>
> Sometimes mirroring (reversing) an image makes it acceptable since a left hand becomes a right hand, etc.
>
> Some artists' pictures do not take into account the "dirty left-hand" culture. For example, it would be "awkward" to use a picture where Jesus is healing a person using his left hand!

The **Mirror** list on the **Details** sub-tab is set to **Always** and greyed out.

###### Is this picture intended for: clarification, story enhancement, filler, unknown? – Picture checklist: Purpose of illustration

Drop-down · Regular+ · `fcb_pubusage`  
Choices: Unknown | Clarification | Story Enhancement | Space Filler · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Select the reason for including the illustration in this particular publication.
>
> Consider how this image is used alongside the text and what function it serves. Maybe it depicts a building or item from a biblical culture, or a scene from a story.

This answer belongs to the current configuration.

###### Yes

Radio · Regular+ · `r_pubclear_yes`  
Also: Picture checklist: What is happening is clear in this context · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

Saved for the current configuration.

###### No

Radio · Regular+ · `r_pubclear_no`  
Also: Picture checklist: What is happening is NOT clear in this context · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Does the image support what the text is saying? As they read the passage does the image help in their understanding?

Consider another picture or another position.

###### Unchecked

Radio · Regular+ · `r_pubclear_unchecked`  
Also: Picture checklist: Not checked for clarity in this context · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

Not checked yet for this publication. This is the starting value.

###### Yes

Radio · Regular+ · `r_pubnoise_yes`  
Also: Picture checklist: Carries wrong meaning in this context · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> For example, do the colors have the same meaning in the local culture? Is there anything in the background that is distracting from the story? Are there any objects, gestures, or other things that imply something unintended or that isn’t in the passage? Are there any anachronisms in the picture (a minaret in Bethlehem)?

Consider changing or removing the picture.

###### No

Radio · Regular+ · `r_pubnoise_no`  
Also: Picture checklist: Carries expected meaning in this context · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

The picture gives the expected meaning here.

###### Is the image appropriate for the publication? – Picture checklist: Appropriateness of illustration

Drop-down · Regular+ · `fcb_pubaccept`  
Choices: Unknown | Culturally Appropriate | Alien but Acceptable | Inappropriate · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Select the appropriateness of the illustration within this publication.
>
> Do the images and their style fit with the type of publication, i.e. Scripture, children’s materials, lectionary, etc.? Are people and actions depicted in acceptable ways?

This answer belongs to the current configuration.

###### Unchecked

Radio · Regular+ · `r_pubnoise_unchecked`  
Also: Picture checklist: Not checked if wrong meaning in this context · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

Not checked yet for this publication. This is the starting value.

###### Consultant Approval

Label · Regular+  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Now consider whether there are any issues with using this picture in this particular publication (config-specific).

###### Picture checklist: Approved by date

Text box · Regular+ · `t_pubApprDate`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> The most recent date that the consultant approval updated.

Type it when you tick **Approved to be used in**.

###### Picture checklist: Approved by initials

Text box · Regular+ · `t_pubInits`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

The initials of the person (usually the consultant) who approved the picture.

###### any publication

Radio · Regular+ · `r_pubapprove_scopeAny`  
Also: Picture checklist: Approved for use in ANY publication · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

Use it when the picture is fine in every context.

###### this publication

Radio · Regular+ · `r_pubapprove_scopeThis`  
Also: Picture checklist: Approved for use in THIS publication · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

The approval is only for the current configuration.

###### Approved to be used in

Checkbox, off · Regular+ · `c_pubApproved`  
Also: Picture checklist: Approved for use · Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

Then choose **any publication** or **this publication**, and type the initials and date. Approved pictures appear when you choose **Approved** in **Filter Checklist**.

###### textv_picNotes

Text area · Regular+ · `textv_picNotes`  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

Free notes about the selected picture, for example questions for the consultant and the answers. They are saved with the current configuration only. Other configurations have their own notes for the same picture.

###### Notes About This Picture

Label · Regular+  
Needs: “Include Pictures (illustrations)” · Shown when: “Include Pictures (illustrations)”

> Use the notes area below to record anything about this picture, or to dialog with the consultant. The notes entered here are saved with this configuration only (other configurations have their own).
