## What this tab is for

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

## The picture table (PicList)

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

## Global Options

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

## Details

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

## Checklist

This sub-tab helps the team think about whether each picture is right for the readers. It is only shown in the **Regular** and **Full** views. The answers are stored with the picture's file, not with the anchor. So if the same picture is used twice, both uses share the answers. PTXprint saves the answers, the approval and the notes, and loads them again the next time you open the project.

* **Across Various Publications** – questions about the picture itself: is it clear, is it acceptable in the culture, and may it be mirrored? These answers are shared by all configurations of the project.
* **In This Publication** – questions about this use: why is it here, is it clear in this context, does it carry a wrong meaning, and does its style suit this publication? These answers belong to the current configuration.
* **Consultant Approval** – tick **Approved to be used in**, choose **any publication** or **this publication**, and type the initials and date.
* **Notes About This Picture** – a place to write comments, or to discuss the picture with the consultant.

Use the **Filter Checklist** area above the table to show, for example, only the pictures where some questions are still **Unknown**.

## Generate PicList dialog

This dialog opens when you click **Generate...** and a PicList already exists. (If there is no PicList yet, PTXprint makes one at once without asking.)

* **Append Pictures to PicList From These Books** – read the `\fig` entries again only for the books listed (the books selected on the **Basic** tab). Pictures from other books stay as they are.
* **Include Pictures From ALL Books** – read all the books of the project again.
* **Randomly Position Pictures on Page** – give new pictures a random corner (top-left, top-right, bottom-left or bottom-right). Without it, new pictures go top-left in two-column layout and at the top in single-column layout.
* **Protect existing PicList settings** – keep the size and position of pictures that are already in the PicList, and only add new ones. Untick it only if you want to start again from the Paratext text.

## Select Images dialog (the catalogue)

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

## Download & Install Image Sets dialog

This dialog lists the image sets that PTXprint can download. Tick the sets you want and click **OK**. Sets that are already installed show **Installed** and cannot be ticked. Some sets show their terms of use; you must agree to the terms before the set is installed. You need an internet connection, and some sets are large.

**Install from ZIP file...** installs a set from a ZIP file on your computer. This is useful at a workshop: download the file once and share it. A ZIP file that contains only pictures (and no image-set information) is unpacked into the project's `local\figures` folder.

## Illustration Credit Overlay dialog

Open this dialog with the **© ...** button on the **Details** sub-tab. It sets a small credit line that is printed on top of the picture. Some artists (for example David C Cook) require this.

* **Image Credit Text** – the text. Type `(c)` for ©, or `dcc` for the David C Cook credit.
* **Vertical Position** and **Horizontal Position** – which corner or edge of the picture.
* **Rotation** – turn the text to run up or down the side of the picture.
* **Background Box** – no box, a light box or a dark box behind the text, or the name of your own style.
* **Apply to ALL images in this series** – use the same text for all pictures of the same series (the same two letters at the start of the file name).
* **Overwrite any existing settings** – also replace the credit on pictures that already have one.

The credit is stored with the picture file, so it applies in all configurations of the project. The font, size and colour come from the `x-credit` style; click the **\x-credit** link to change it on the **Styles** tab.

## Add Map dialog

Click **Add Maps...** to add map pages at the end of the publication.

1. Choose the **Book Code for Maps** (usually **XXM**).
2. Click **Select Map...** and choose the map file.
3. Type a **Caption** if you want one, and set **Scale** and **Rotation**.
4. Click **Size and Position...** to choose the frame size and position (the same dialog is used for sidebars). The code you choose is shown in the box beside it.
5. Click **Add Another Map** to add this map and start the next one, or **OK - Done!** to add it and finish.

PTXprint adds each map to the PicList (anchors `XXM map01`, `XXM map02` ...), writes one page for each map into the map book, ticks **Include Maps** on the **Peripherals** tab, and adds the map book to the list of books to print. Use **Edit Maps...** to look at the map book on the **View+Edit** tab.

## Common tasks

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

## Common problems

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

## Control notes

### @c_includeillustrations
When ticked, PTXprint loads the PicList for this configuration and prints the pictures. When not ticked, the **Details** and **Checklist** sub-tabs are hidden. Turning it on can make printing slower.

### @lb_settings
Settings for every picture: resolution, captions, missing pictures and the picture folders.

### @lb_details
The settings of the picture selected in the table, such as anchor, caption, size and position.

### @lb_checklist
Records whether each picture is clear, culturally acceptable and approved. When this sub-tab is open, a **Filter Checklist** area appears above the table.

### @tv_picListEdit
One row for each picture in this configuration. Double-click a row to open **Details**; right-click it for more actions. Red text means the picture is too tall for the page; a grey row means the file cannot be found.

### @btn_plAdd
PTXprint asks for a picture file, adds a row and opens the **Details** sub-tab. Then type the **Anchor Ref** (for example `JHN 3.16`) and a caption. Only the file name is saved, so the file must be in a folder that PTXprint searches.

### @btn_plDel
There is no undo, so check the selection first. It does not change the Paratext text or the picture file.

### @btn_plGenerate
If no PicList exists yet, PTXprint makes it at once; otherwise the **Generate PicList** dialog asks what to do. Use it after pictures are added in Paratext.

### @btn_refreshCaptions
Use it after captions are corrected in Paratext.

### @btn_addMaps2
Opens the **Add Map** dialog.

### @btn_editMaps2
Does nothing if the map book (for example XXM) does not exist yet; use **Add Maps...** first.

### @btn_getPictures
Opens the **Select Images** dialog, where you add pictures from an image set to the PicList. If no image set is installed, the download dialog opens first.

### @c_filterPicList
The books selected for printing are set on the **Basic** tab. This only changes what you see; it does not delete anything.

### @r_image_preview
If the box is empty, PTXprint could not find the picture file. Hover over the preview to see the file path.

### @r_image_location
Use it to check the **Frame Size** and position settings before you print.

### @fcb_chklstFilter
**All Unknown / Unchecked** – no question answered yet. **Any Unknown / Unchecked** – at least one question still open. **Approved** – the approved pictures. Only shown when the **Checklist** sub-tab is open.

### @c_picCheckInvFilter
For example, choose **Approved** and tick this to see all pictures that are not approved yet.

### @r_pictureRes_High
Use this for the final print PDF. **Request Access...** is only available with this option.

### @r_pictureRes_Low
Use this for drafts. PTXprint prefers JPG files and, of two files of the same type, the smaller one. Pictures may look blurred when printed.

### @c_figplaceholders
The page layout stays the same, so you can check it with a very small PDF. Untick it for the final PDF.

### @c_figexclwebapp
Keep it ticked for printed publications.

### @lb_omitPics
Opens a help web page.

### @c_fighidecaptions
Also removes the caption references.

### @c_fighiderefs
The caption text is kept.

### @c_skipmissingimages
After printing, the number of missing pictures is shown next to this option. Keep it ticked, but check the count before the final print.

### @c_cropborders
Check that no picture loses part of its content. The pictures are converted to JPG when this is on.

### @btn_requestIllustrations
PTXprint fills in the project name and the list of pictures. You must add your email and supervisor details.

### @btn_requestPermission
PTXprint fills in the list of pictures and the publication details. If country, language or number of copies are missing, PTXprint opens the **Peripherals** tab so that you can fill them in first.

### @c_useCustomFolder
When you tick it and no folder is chosen yet, PTXprint asks for the folder.

### @btn_selectFigureFolder
The chosen folder is shown beside the button.

### @c_exclusiveFiguresFolder
This applies when you print, when you make an archive and when PTXprint looks for the PicList files. The downloaded image sets are still searched fully, because each set is in a subfolder of its own. It is unticked automatically when you untick **Use Other Location**.

### @t_imageTypeOrder
Separate the types with spaces.

### @t_plAnchor
PTXprint changes `:` into `.` and the book code into capital letters for you. If the anchor is empty, you cannot move to another row. See "Details" above for the diglot, glossary and paragraph forms.

### @t_plRef
For example `4:39`.

### @t_plAltText
A short description of what the picture shows. It helps you recognise the picture in the table. Pictures added from the catalogue get the catalogue title here.

### @t_plFilename
The file name only, without a folder. PTXprint looks for it in the picture folders. Changing it updates the preview and the missing-file check.

### @t_plCopyright
Used in the credits that `\zimagecopyrights` prints in the colophon. For known series this box is hidden and **Automatic** is shown instead.

### @s_plScale
100% fills the frame width. Use 30–60% for cutouts and small pictures. If the row turns red, the picture is too tall for the page; reduce the scale.

### @fcb_plPgPos
The choices depend on **Frame Size**: Span Width allows **Top**, **Bottom** and **Below Notes**; Column Width allows **Top**, **Bottom**, **Before Verse**, **After Paragraph** and **Cutout**; the page sizes allow **Top**, **Center** and **Bottom**.

### @fcb_plSize
Choose this first, because it changes the choices in **Vertical Position** and **Horizontal Position**. Use **Page (to Edge)** for full-page maps.

### @fcb_plHoriz
Inner and outer keep a picture on the same side relative to the binding when pages are mirrored. Greyed out for **Span Width**. **Center** is only offered for **Before Verse**, **After Paragraph** and the page sizes.

### @fcb_plMirror
**Odd** or **Even** may need the PDF to be made twice to be right. Check the flipped picture carefully: writing in it will be backwards.

### @l_plOffsetNum
The label for **Number of Lines**. It changes to "Number of paragraphs" when **Vertical Position** is **After Paragraph**.

### @s_plLines
Only used with **Cutout** and **After Paragraph**. For a cutout, it is the number of lines below the start of the paragraph where the picture starts (decimals allowed). For **After Paragraph**, it is the number of paragraphs (whole numbers only).

### @c_plMediaP
Untick it to leave this picture out of print without deleting it from the PicList. Greyed out if the artist's licence does not allow this use. If you untick **Print**, **App** and **Web**, all three stay unticked when you open the project again.

### @c_plMediaA
It does not change the PDF. Greyed out if the artist's licence does not allow this use.

### @c_plMediaW
It does not change the PDF. Greyed out if the artist's licence does not allow this use.

### @l_autoCopyAttrib
Shown instead of the **Copyright Attribution** box for a series that PTXprint knows.

### @btn_overlayCredit
Opens the **Illustration Credit Overlay** dialog.

### @t_piccreditbox
The current overlay settings in short form: position, rotation and box (for example `bl,0,None`). Use the **© ...** button to change them.

### @t_plCaption
Changes here are not copied back to Paratext.

### @lb_style_fig
Change the caption font, size and alignment there.

### @t_picXetex
The caption is not rotated.

### @r_picclear_yes
This answer is shared by all configurations of the project.

### @r_picclear_no
This answer is shared by all configurations of the project.

### @r_picclear_unknown
The starting value. Pictures with this answer appear in the "Unknown / Unchecked" filters.

### @fcb_picaccept
This answer is shared by all configurations of the project.

### @r_picreverse_OK
The **Mirror** list on the **Details** sub-tab can then be used freely.

### @r_picreverse_never
For example because it contains writing. The **Mirror** list on the **Details** sub-tab is set to **Never** and greyed out.

### @r_picreverse_always
The **Mirror** list on the **Details** sub-tab is set to **Always** and greyed out.

### @fcb_pubusage
This answer belongs to the current configuration.

### @r_pubclear_yes
Saved for the current configuration.

### @r_pubclear_no
Consider another picture or another position.

### @r_pubclear_unchecked
Not checked yet for this publication. This is the starting value.

### @r_pubnoise_yes
Consider changing or removing the picture.

### @r_pubnoise_no
The picture gives the expected meaning here.

### @r_pubnoise_unchecked
Not checked yet for this publication. This is the starting value.

### @fcb_pubaccept
This answer belongs to the current configuration.

### @t_pubApprDate
Type it when you tick **Approved to be used in**.

### @t_pubInits
The initials of the person (usually the consultant) who approved the picture.

### @r_pubapprove_scopeAny
Use it when the picture is fine in every context.

### @r_pubapprove_scopeThis
The approval is only for the current configuration.

### @c_pubApproved
Then choose **any publication** or **this publication**, and type the initials and date. Approved pictures appear when you choose **Approved** in **Filter Checklist**.

### @textv_picNotes
Free notes about the selected picture, for example questions for the consultant and the answers. They are saved with the current configuration only. Other configurations have their own notes for the same picture.

### @r_generate_selected
Pictures of other books stay as they are. This is the safe choice.

### @r_generate_all
If **Protect existing PicList settings** is not ticked, all your changes to sizes and positions are lost.

### @c_randomPicPosn
It only affects pictures that have no position yet.

### @c_protectPicList
Only new pictures are added. Keep it ticked unless you want to start again from the Paratext text.

### @btn_gnr8pl_ok
Generates the PicList with the options chosen in the dialog.

### @btn_gnr8pl_cancel
Closes the dialog without changing the PicList.

### @ecb_artPictureSet
PTXprint remembers your last choice. To get more image sets, click **Download Image Set...**.

### @t_artRefRange
Shows only pictures for these references. It starts with the books you are printing. You can type ranges such as `GEN 1-3; MRK`, with 3-letter book codes. Clear the box to see all pictures in the set. Press Enter or click **Search + Update Images** to apply it.

### @t_artSearch
Searches keywords and titles, for example `boat` or `shepherd`. Press Enter or click **Search + Update Images** to apply it. Clear the box to show all pictures again.

### @r_imgSort_ref
Uses the reference that matches your reference range.

### @r_imgSort_pop
The pictures used most often by other projects come first.

### @tv_artists
The artists (picture series) in the image set. Tick one or more to show only their pictures. Untick all of them to show every artist.

### @btn_imgRefresh
Updates the thumbnails after you change the search words or the reference range. It is only active when something has changed.

### @c_imgMediaP
At the time of writing, this box does not change which thumbnails are shown.

### @c_imgMediaA
At the time of writing, this box does not change which thumbnails are shown.

### @c_imgMediaW
At the time of writing, this box does not change which thumbnails are shown.

### @lb_imgRefs
The references of the picture under the mouse. The reference in bold is the one PTXprint will use as the anchor. References in red already have this picture in your PicList.

### @btn_imgClearSelection
Unselects all the selected thumbnails, so you can start your choice again.

### @btn_getImageSet
Opens the **Download & Install Image Sets** dialog.

### @btn_requestIllustrations2
The same online form as **Request Access...** on **Global Options**.

### @btn_imagePicker_ok
Each picture is anchored at its Bible reference, with **Column Width** and top-left position. Then type a caption for each one on the **Details** sub-tab.

### @btn_imagePicker_cancel
Closes the catalogue without adding pictures.

### @tv_imagesets
The image sets that you can download, with artist, style, size and licence. Tick the sets you want, then click **OK**. Sets marked **Installed** cannot be ticked. Hover over a row for more information.

### @c_imgSet_selectAll
Some sets are large downloads.

### @btn_installFromZip
If the set has terms of use, you must agree to them. A ZIP file with only pictures in it is unpacked into the project's `local\figures` folder.

### @btn_imgSet_ok
Downloads and installs the ticked image sets. This can take a while. When it is finished, the catalogue opens.

### @btn_imgSet_cancel
Closes the dialog without downloading anything.

### @t_plCreditText
Keep it short; it is printed in small letters.

### @fcb_plCreditVpos
Where the credit sits on the picture.

### @fcb_plCreditHpos
Inner and outer are useful if the picture may be mirrored or appear on both odd and even pages.

### @fcb_plCreditRotate
Useful when the credit is at the left or right edge.

### @ecb_plCreditBoxStyle
When you open the dialog again, a credit with no box shows **None**.

### @c_plCreditApply2all
A series is the pictures with the same two letters at the start of the file name, for example all `cn` pictures. To change pictures that already have a credit, also tick **Overwrite any existing settings**.

### @c_plCreditOverwrite
Use with care: earlier settings for individual pictures are lost.

### @lb_style_x-credit
Change the font, size and colours of all credit overlays there.

### @btn_ovrly_ok
Saves the credit overlay settings for this picture (and for the series, if chosen). The credit is kept even if you close PTXprint without selecting another picture first.

### @btn_ovrly_cancel
Closes the dialog without changing the credit.

### @fcb_ptxMapBook
**XXM** is the usual choice. Choose another book only if XXM is used for something else.

### @btn_selectMap
Chooses the map image file (PNG, JPG, PDF or TIF). A preview is shown in the dialog.

### @t_mapCaption
Optional. Leave it empty if the map fills the whole page to the edge.

### @s_mapScale
1 means the full size of the frame.

### @fcb_mapRotate
Use it for a wide map on a tall page.

### @btn_mapSizePosition
Opens the **Size and Position** dialog to choose the frame size (for example a full page) and the position of the map. The result is shown as a code in the box beside the button.

### @t_mapPgPos
The position code chosen with **Size and Position...**, for example `Pc` (a page of its own, centred).

### @fcb_coordBorder
At the time of writing, PTXprint does not use this setting when it adds the map.

### @c_mapSpread
At the time of writing, PTXprint does not use this setting when it adds the map.

### @btn_mapAddAnother
Adds the current map and clears the form for the next one. Finish with **OK - Done!**, because the map book is only written then.

### @btn_addMap
Adds the current map (if a file is chosen) and finishes. PTXprint writes the map pages into the map book, ticks **Include Maps** on the **Peripherals** tab, and adds the map book to the books to print.

### @btn_gnr8cover_cancel1
Closes the dialog. The map book is not written. Maps already added with **Add Another Map** may still be in the PicList; delete them there if you do not want them.
