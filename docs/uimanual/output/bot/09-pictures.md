# Pictures tab

## What this tab is for

Use the **Pictures** tab when your publication has pictures (illustrations) or maps. Here you can:

* turn pictures on or off for the whole publication,
* tell PTXprint where to find the picture files,
* choose the size and position of every picture on the page,
* add or remove pictures, and add maps,
* look for new pictures in a catalogue of Bible illustrations,
* keep track of copyright, permissions and the checking of each picture.

**The PicList.** PTXprint keeps a list of all the pictures for each saved configuration. This list
is called the **PicList** (picture list). Each line of the PicList says which picture file to use, where
in the text it belongs (the *anchor*), its caption, its size and its position on the page.

When you generate the PicList, PTXprint reads the `\fig ... \fig*` entries in your Paratext books and
copies them into the PicList. After that, PTXprint uses only the PicList. It ignores the `\fig` entries
in the text when it typesets. This means:

* You can place, resize, add and remove pictures in PTXprint **without changing the Paratext text**.
* Each configuration can have different pictures. For example, a full Bible can have a few pictures,
  and a children's portion can have many.
* Changes you make here are **not** copied back into Paratext. If a caption or picture changes in
  Paratext, use **Refresh List** or **Generate...** to bring the change into PTXprint.

**View levels.** The Pictures tab is shown from the **Basic** view. In the **Basic** view you only see a
few settings on the **Global Options** sub-tab. The picture table, the **Details** and **Checklist**
sub-tabs and most buttons are only shown in the **Default** and **Full** views.

Some words used in this chapter:

* **Anchor** – the place in the text (for example a verse) that a picture belongs to.
* **Caption** – the text printed with the picture, usually below it.
* **Cutout** – a space cut into the side of a paragraph, so that the text flows around a small picture.
* **Span** – the full width of the text area, across both columns.
* **Mirror** – flip a picture from left to right, like in a mirror.
* **Credit overlay** – a small copyright line printed on top of the picture itself.
* **Image set** – a downloadable collection of Bible illustrations that you can use in the catalogue.

## The picture table (PicList)

The top half of the tab shows the PicList as a table. Each row is one picture. The columns shown
change with the sub-tab you are on: **Global Options** and **Checklist** show only a few columns;
**Details** shows them all.

* Click a row to select it. Its settings appear in the **Details** sub-tab below.
* Double-click a row to jump to the **Details** sub-tab.
* You can select several rows at once (use Ctrl or Shift while clicking). Then you can change the
  size, position, scale or mirror setting of all of them together. Fields that must be different for
  each picture (anchor, caption, filename, reference) are greyed out while several rows are selected.
* Right-click a row for more actions: copy the `\fig` line for that picture (to paste into Paratext),
  jump to the reference in Paratext (Windows only), show the picture file in the file manager, copy the
  file path, or delete the picture(s).
* **Red** text in a row means the picture is probably too tall to fit on the page at this size and scale.
  Make the **Scale** smaller.
* **Grey** rows mean PTXprint cannot find the picture file. Check the file name and the picture folders
  (see below).

The buttons next to the table:

* **Add** – add a picture file by hand.
* **Del** – delete the selected picture(s) from the PicList at once (no question is asked).
* **Generate...** – (re)build the PicList from the `\fig` entries in the Paratext books.
* **Refresh List** – update only the captions and references from Paratext.
* **Add Maps...** / **Edit Maps...** – add maps at the end of the publication, and edit the map book.
* **Show Catalogue...** – open the **Select Images** dialog to choose illustrations from an image set.
* **Show Active Books** – show only the pictures of the books you have chosen to print.
* **Image** / **Position** – show either a preview of the picture, or a small drawing of where it will
  sit on the page.

When the **Checklist** sub-tab is open, the buttons are replaced by a **Filter Checklist** area. Use it to
show only the pictures that still need checking, or only the approved ones.

## Global Options

This sub-tab has the settings for all the pictures in the publication.

**Include Pictures (illustrations)** is the main switch. When it is not ticked, PTXprint prints no
pictures, and most other picture settings are greyed out.

**Resolution.** Paratext usually keeps small, low-quality JPG copies of pictures in the project's
`figures` folder. Large, high-quality copies are often kept in the project's `local\figures` folder, so
that they are not shared by Send/Receive.

* **Low Resolution (Smaller File)** – PTXprint prefers JPG files, and the smaller file if there are two
  of the same kind. The PDF is small and easy to email. Use this for drafts and checking.
* **High Resolution (Larger File)** – PTXprint prefers TIF and PNG files, and the larger file. Use this for
  the final PDF for the printer.
* **Use Place-holders (Smallest PDF File)** – prints an empty box where each picture would go. The layout
  stays the same, but the PDF is very small.

**What to print.**

* **Omit Pictures Only Meant for Web or App** – leaves out pictures that are not marked for print.
* **Omit Captions** – prints the pictures without any caption.
* **Omit References (ch:vs)** – keeps the captions but removes the chapter:verse reference after them.
* **Omit Missing Pictures** – if a picture file cannot be found, PTXprint skips it and continues. The
  number of missing pictures is shown next to this option after you print, and their names are listed at
  the bottom of the sub-tab.
* **Remove Image Borders** – cuts off thin lines at the edges of pictures. It affects every picture.

**Where PTXprint looks for picture files.** PTXprint searches these folders, and all the folders inside
them:

1. the **Picture Folder** you chose (only when **Use Other Location** is ticked),
2. the project's `local\figures` folder,
3. the project's `figures` folder,
4. the image sets you have downloaded (in PTXprint's own data folder).

The PicList only stores the file **name**, not the folder. If several files have the same name (for
example `hk00123.jpg` and `hk00123.tif`), **Image Types** decides which one is used. If you leave
**Image Types** empty, PTXprint uses JPG first for low resolution and TIF first for high resolution.
TIF and PNG pictures are converted to JPG while the PDF is made.

**Permissions.** **Request Access...** (only with **High Resolution**) and **Get Permission...** open
online forms that PTXprint fills in with the list of pictures used in this configuration.

## Details

This sub-tab shows the settings of the picture selected in the table. It is only shown in the
**Default** and **Full** views.

**Anchor Ref.** The anchor is where the picture belongs in the text. It has a 3-letter book code, a
space, and the chapter and verse joined with a dot: `MRK 4.39`. PTXprint puts the picture on the same
page as its anchor if there is room. If there is no room, the picture can move to a later page. To move a
picture to an earlier or later page, change the anchor by a few verses. Other forms:

* In a diglot, add `L` or `R` to the book code (`MRKL 4.39`) to tie the picture to the primary (L) or
  secondary (R) text.
* In the glossary, `GLO k.Altar` ties a picture to the glossary entry `\k Altar\k*`. Spaces are removed
  (`GLO k.JohntheBaptist`).
* `=2` at the end (for example `PSA 23.4=3`) means "the 2nd (or 3rd) paragraph after this anchor". This
  is useful for poetry.

**Caption, Caption Ref and Filename.** The **Caption** is printed with the picture. The **Caption Ref**
is the reference printed after the caption, for example `(4:39)`. It does not have to be the same as the
anchor. The **Filename** is the name of the picture file. Remember that changes here are not copied back
to Paratext.

**Size and position.** Three settings work together. The choices in each list change with the one
before it, so set them in this order:

1. **Frame Size** – how wide the area for the picture is:
   * **Column Width** – the width of one column (in two-column layout).
   * **Span Width** – the full width of the text, across both columns.
   * **Page (in Margins)** – a whole page inside the margins. The page header is still printed.
   * **Page (to Edge)** – the whole sheet of paper, with no margins, header or footer. Do not use a
     caption with this size.
   In single-column layout, Column Width and Span Width are the same.
2. **Vertical Position** – where the picture goes:
   * **Top** / **Bottom** – at the top or bottom of the page (or column).
   * **Below Notes** – below the footnotes (Span Width only).
   * **Before Verse** – in the text, just before the anchor verse.
   * **After Paragraph** – in the text, after the paragraph that contains the anchor.
   * **Cutout** – in a notch at the side of the paragraph. The text flows around the picture.
   For the page sizes, the choices are **Top**, **Center** and **Bottom** of the page.
3. **Horizontal Position** – **Left**, **Right**, **Inner** (near the binding), **Outer** (near the
   outside edge) and, where possible, **Center**. It is greyed out (shows **-**) for Span Width.

**Number of Lines** is used only with **Cutout** (how many lines below the start of the paragraph the
picture starts; decimals are allowed) and **After Paragraph** (after how many paragraphs).

PTXprint stores the position as a short code (shown in the table's position column). You do not have to
type these codes, but they help when you read the table:

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

**Scale** makes the picture smaller (or larger) inside its frame. 100% means the full width of the frame.
For a cutout, 30–50% is common. If the row turns red, the picture is too tall for the page; make the
scale smaller.

**Mirror** flips the picture. Use it, for example, so that people in the picture look into the page and
not out of it, or so that an action is done with the right hand. **Odd** and **Even** flip the picture
only when it lands on an odd or even page. **Mirror** is greyed out if the **Checklist** sub-tab says
**Never mirror** or **Always mirror** for this picture.

**Media (Print, App, Web).** These boxes say where the picture may be used. A picture without **Print**
is left out of the PDF. Some boxes are greyed out because the artist's licence does not allow that use.

**Copyright.** For the common series of Bible illustrations (for example file names that start with
`cn`, `co`, `hk`, `lb`, `bk`, `dy`, `mn` or `wa` followed by five digits), PTXprint knows the copyright
text. You see the word **Automatic** instead of a text box. For other pictures, type the credit in
**Copyright Attribution**. PTXprint collects all the picture credits, with page numbers, into the colophon
when the colophon contains `\zimagecopyrights` (set this on the **Peripherals** tab).

Some artists require a small credit printed **on** each picture. Click **© ...** to open the
**Illustration Credit Overlay** dialog.

**Extra** is for advanced options such as rotating a picture (`rotated 90`, `rotate=edge`,
`rotate=binding`) or choosing a page of a multi-page PDF (`page=2`).

## Checklist

This sub-tab helps the team think about whether each picture is right for the readers. It is only shown
in the **Default** and **Full** views. The answers are stored with the picture's file, not with the
anchor. So if the same picture is used twice, both uses share the answers.

* **Across Various Publications** – questions about the picture itself: is it clear, is it acceptable in
  the culture, and may it be mirrored? These answers are shared by all configurations of the project.
* **In This Publication** – questions about this use: why is it here, is it clear in this context, does
  it carry a wrong meaning, and does its style suit this publication? These answers belong to the
  current configuration.
* **Consultant Approval** – tick **Approved to be used in**, choose **any publication** or **this
  publication**, and type the initials and date.
* **Notes About This Picture** – a place to write comments, or to discuss the picture with the consultant.

Use the **Filter Checklist** area above the table to show, for example, only the pictures where some
questions are still **Unknown**.

## Generate PicList dialog

This dialog opens when you click **Generate...** and a PicList already exists. (If there is no PicList
yet, PTXprint makes one at once without asking.)

* **Append Pictures to PicList From These Books** – read the `\fig` entries again only for the books
  listed (the books selected on the **Basic** tab). Pictures from other books stay as they are.
* **Include Pictures From ALL Books** – read all the books of the project again.
* **Randomly Position Pictures on Page** – give new pictures a random corner (top-left, top-right,
  bottom-left or bottom-right). Without it, new pictures go top-left in two-column layout and at the top
  in single-column layout.
* **Protect existing PicList settings** – keep the size and position of pictures that are already in the
  PicList, and only add new ones. Untick it only if you want to start again from the Paratext text.

## Select Images dialog (the catalogue)

Click **Show Catalogue...** to open this dialog. It shows thumbnails of the pictures in an **Image Set**.
If you have no image set yet, the **Download & Install Image Sets** dialog opens first.

* Choose the **Image Set** at the top.
* The **Limit to Range of References** box starts with the books you are printing. Only pictures for
  these references are shown. Clear it to see all pictures.
* Type words in **Search** to find pictures by keyword or title.
* Tick artists in the artist list to show only their pictures.
* Click **Search + Update Images** (or press Enter) after you change the search or references.
* Sort by **Scripture Reference** or by **Frequency of Use**.
* Move the mouse over a picture to see its number, artist, description and references. Right-click a
  picture to see a larger preview.
* Pictures with a peach-coloured background are already in your PicList.
* Click pictures to select them, then click **Add Images to PicList**.

The new pictures are anchored at their Bible reference, with **Column Width** and top-left position. Then
go to the **Details** sub-tab and type a caption for each one.

## Download & Install Image Sets dialog

This dialog lists the image sets that PTXprint can download. Tick the sets you want and click **OK**.
Sets that are already installed show **Installed** and cannot be ticked. Some sets show their terms of
use; you must agree to the terms before the set is installed. You need an internet connection, and some
sets are large.

**Install from ZIP file...** installs a set from a ZIP file on your computer. This is useful at a
workshop: download the file once and share it. A ZIP file that contains only pictures (and no image-set
information) is unpacked into the project's `local\figures` folder.

## Illustration Credit Overlay dialog

Open this dialog with the **© ...** button on the **Details** sub-tab. It sets a small credit line that is
printed on top of the picture. Some artists (for example David C Cook) require this.

* **Image Credit Text** – the text. Type `(c)` for ©, or `dcc` for the David C Cook credit.
* **Vertical Position** and **Horizontal Position** – which corner or edge of the picture.
* **Rotation** – turn the text to run up or down the side of the picture.
* **Background Box** – no box, a light box or a dark box behind the text, or the name of your own style.
* **Apply to ALL images in this series** – use the same text for all pictures of the same series
  (the same two letters at the start of the file name).
* **Overwite any existing settings** – also replace the credit on pictures that already have one.

The credit is stored with the picture file, so it applies in all configurations of the project. The font,
size and colour come from the `x-credit` style; click the **\x-credit** link to change it on the
**Styles** tab.

## Add Map dialog

Click **Add Maps...** to add map pages at the end of the publication.

1. Choose the **Book Code for Maps** (usually **XXM**).
2. Click **Select Map...** and choose the map file.
3. Type a **Caption** if you want one, and set **Scale** and **Rotation**.
4. Click **Size and Position...** to choose the frame size and position (the same dialog is used for
   sidebars). The code you choose is shown in the box beside it.
5. Click **Add Another Map** to add this map and start the next one, or **OK - Done!** to add it and
   finish.

PTXprint adds each map to the PicList (anchors `XXM map01`, `XXM map02` ...), writes one page for each map
into the map book, ticks **Include Maps** on the **Peripherals** tab, and adds the map book to the list of
books to print. Use **Edit Maps...** to look at the map book on the **View+Edit** tab.

## Common tasks

### Show the pictures that are in the Paratext text

1. On the **Pictures** tab, **Global Options** sub-tab, tick **Include Pictures (illustrations)**.
2. Make sure the view is **Default** or **Full** (so that you can see the picture table).
3. Click **Generate...**. If a dialog opens, choose **Append Pictures to PicList From These Books**, keep
   **Protect existing PicList settings** ticked, and click **OK**.
4. Look for grey rows in the table (missing files) and fix them (see "Common problems").
5. Print.

### Move a picture to another place on the page

1. Select the picture in the table. Open the **Details** sub-tab.
2. Set **Frame Size** first, then **Vertical Position**, then **Horizontal Position**.
3. Click **Position** (beside **Image**) to see a small drawing of the position.
4. Print again to check.

### Move a picture to another page

1. Select the picture and open the **Details** sub-tab.
2. Change the verse in **Anchor Ref** to a few verses earlier (to move it back) or later (to move it
   forward). Keep the dot between chapter and verse: `LUK 2.7`.
3. Print again.

### Make a picture smaller and let the text flow around it

1. Select the picture. On the **Details** sub-tab, set **Frame Size** to **Column Width**.
2. Set **Vertical Position** to **Cutout** and **Horizontal Position** to **Left** or **Right**
   (or **Inner**/**Outer**).
3. Set **Scale** to about 40%.
4. Set **Number of Lines** to the line where the picture should start (0 = the first line of the
   paragraph).
5. Print again.

### Add a new picture from the catalogue

1. Click **Show Catalogue...**.
2. Choose the **Image Set**. Type a word in **Search**, or check the references in **Limit to Range of
   References**, and click **Search + Update Images**.
3. Click the pictures you want, then click **Add Images to PicList**.
4. For each new picture, type the **Caption** on the **Details** sub-tab, and check the **Anchor Ref**.

### Use high-quality pictures for the final PDF

1. Put the high-resolution files in the project's `local\figures` folder, or tick **Use Other Location**
   and click **Picture Folder...** to choose their folder.
2. On **Global Options**, choose **High Resolution (Larger File)**.
3. Print, and check that the missing-pictures count is 0.

### Make a small PDF to send by email

1. On **Global Options**, choose **Low Resolution (Smaller File)**.
2. If the file must be even smaller, tick **Use Place-holders (Smallest PDF File)**.

### Print the picture credits in the colophon

1. On the **Peripherals** tab, tick **Colophon at End of Publication**.
2. Make sure the colophon text contains `\zimagecopyrights`.
3. For pictures that do not show **Automatic** on the **Details** sub-tab, type the credit in
   **Copyright Attribution**.
4. Print. PTXprint lists each artist with the pages of their pictures.

### Add maps at the end of the book

1. Click **Add Maps...**.
2. Follow the steps in the "Add Map dialog" section above.
3. Click **OK - Done!**, then print.

## Common problems

**The Pictures tab shows no table, or no Details sub-tab.**
The table and the **Details** and **Checklist** sub-tabs are only shown in the **Default** and **Full**
views. Change the view level. Also check that **Include Pictures (illustrations)** is ticked.

**No pictures appear in the PDF.**
* **Include Pictures (illustrations)** is not ticked. Tick it.
* The PicList is empty. Click **Generate...**. (Pictures in the Paratext text are only used after they
  are in the PicList.)
* **Use Place-holders** is ticked. Untick it.
* The **Print** box on the **Details** sub-tab is not ticked for these pictures.

**Some pictures are missing.**
* The row is grey in the table: PTXprint cannot find the file. Check the **Filename**. Make sure the file
  is in the project's `figures` or `local\figures` folder, or tick **Use Other Location** and choose the
  folder with **Picture Folder...**.
* **Image Types** contains only some types (for example only `TIF`), and the file is a different type.
  Clear **Image Types**.
* The picture's book is not one of the books you are printing.
* **Omit Missing Pictures** hides the problem. Look at the missing-pictures count and list on **Global
  Options** after printing.

**A picture I added with Add is not found.**
The PicList stores only the file name. If you chose a file from a folder that PTXprint does not search,
copy the file into the project's `local\figures` folder, or set that folder with **Use Other Location**.

**A picture appears on the wrong page.**
A picture at the top or bottom of a page goes on the same page as its anchor only if there is room.
Change the **Anchor Ref** by a few verses. Pictures that are too large also move to a later page; reduce
the **Scale**.

**I cannot choose the position I want.**
The lists depend on each other. **Span Width** only allows **Top**, **Bottom** and **Below Notes**, and
no horizontal position. **Center** is only offered for **Before Verse**, **After Paragraph** and the page
sizes. Choose the **Frame Size** first.

**The picture is too big, or the row is red.**
The picture is taller than fits on the page. Reduce the **Scale**, or use **Column Width** instead of
**Span Width**.

**A cutout picture jumps between two places each time I print.**
This can happen when the anchor is near the end of a paragraph. Choose an earlier anchor in the same
paragraph and increase **Number of Lines**.

**Mirror is greyed out.**
On the **Checklist** sub-tab, **Never mirror** or **Always mirror** is chosen for this picture. Choose
**OK to mirror** to use the **Mirror** list again.

**My changes to captions in Paratext do not show.**
PTXprint uses its own PicList. Click **Refresh List** to copy the captions and references again. Your
size and position settings stay the same.

**Changes in PTXprint do not appear in Paratext.**
This is normal. PTXprint never changes the Paratext text. To copy a picture into Paratext, right-click
its row and choose **Copy \fig String to Clipboard**, then paste it in Paratext.

**The copyright text is missing or wrong.**
* The colophon must contain `\zimagecopyrights` (**Peripherals** tab).
* For pictures that are not from a known series, type the credit in **Copyright Attribution**.
* If **Sensitive Project** is ticked (on the **Advanced** tab), PTXprint uses a shorter credit wording
  for some artists.
* By default, the most common artist is described as "all other illustrations". To list every artist
  with all pages, tick **Show comprehensive illustration credits** (on the **Advanced** tab, **Other**
  sub-tab, in the **Pictures, Figures, Images, Sidebars** area).

**I want the caption above the picture, or the reference before the caption.**
On the **Advanced** tab, **Other** sub-tab, in the **Pictures, Figures, Images, Sidebars** area, tick
**Show Caption Before Image** or **Ref Before Caption**.

## Settings reference: Pictures tab

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Generate PicList (dialog)

#### OK

- **Where:** Generate PicList (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Generates the PicList with the options chosen in the dialog.

*(Internal ID: `btn_gnr8pl_ok`)*

#### Cancel

- **Where:** Generate PicList (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog without changing the PicList.

*(Internal ID: `btn_gnr8pl_cancel`)*

### Generate PicList (dialog) › When Generating PicList

#### Append Pictures to PicList From These Books

- **Where:** Generate PicList (dialog) › When Generating PicList
- **Type:** Radio button
- **Description:** Generate PicList: Append to existing list
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> This option will ADD to any existing entries in the PicList and/or replace entries for the book(s) listed below.

**Explanation:**

Reads the `\fig` entries again only for the books shown in the dialog (the books selected on the **Basic**
tab). Pictures of other books stay as they are. This is the safe choice.

*(Internal ID: `r_generate_selected`)*

#### Include Pictures From ALL Books

- **Where:** Generate PicList (dialog) › When Generating PicList
- **Type:** Radio button
- **Description:** Generate PicList: Replace existing list
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> This option will REPLACE ALL entries in the existing PicList. Do you really want to do this?
>
> If in doubt, then click Cancel.

**Explanation:**

Reads the `\fig` entries again from all books of the project. If **Protect existing PicList settings** is
not ticked, all your changes to sizes and positions are lost. If in doubt, click **Cancel**.

*(Internal ID: `r_generate_all`)*

#### Randomly Position Pictures on Page

- **Where:** Generate PicList (dialog) › When Generating PicList
- **Type:** Checkbox (ticked by default)
- **Description:** Generate PicList: Randomly position pictures on page
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> By default all illustrations are placed in the top-left corner of a page (when double columns are used) and at the top in single column mode.
>
> Checking this option will randomly position the illustrations on the page (using top-left, top-right, bottom-left and bottom-right).
>
> You can change the location of pictures later if needed.

**Explanation:**

Gives new pictures a random corner (top-left, top-right, bottom-left or bottom-right) instead of all at
the top-left. This can give a more varied look. You can still change each position later. It only affects
pictures that have no position yet.

*(Internal ID: `c_randomPicPosn` · Config key: `project/randompicposn`)*

#### Protect existing PicList settings

- **Where:** Generate PicList (dialog) › When Generating PicList
- **Type:** Checkbox (ticked by default)
- **Description:** Generate PicList: Protect existing PicList settings
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> When synchronizing the pictures from the Paratext files with PTXprint's PicList, don't change any of the (layout and size) settings and don't delete any pictures no longer found in the Paratext USFM text.

**Explanation:**

Keeps the settings of pictures that are already in the PicList, and does not remove pictures that are no
longer in the Paratext text. Only new pictures are added. Keep it ticked unless you want to start again
from the Paratext text.

*(Internal ID: `c_protectPicList`)*

### Select Images... (dialog)

#### Download Image Set...

- **Where:** Select Images... (dialog)
- **Type:** Button
- **Description:** Download an Image Set from an online source
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> If you don't already have appropriate scripture illustrations, then you can download an Image Set which contains low-resolution illustrations for trial publications from one of the links.

**Explanation:**

Opens the **Download & Install Image Sets** dialog to download more image sets.

*(Internal ID: `btn_getImageSet`)*

#### Request Access...

- **Where:** Select Images... (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Request for Access to High Quality Illustrations/Maps in the SIL repository.
>
> Click this button to fill in the form requesting access to the illustrations used in the current publication.
>
> After completing and submitting the online form you should receive an immediate response by email.

**Explanation:**

Opens the same online form as **Request Access...** on **Global Options**: a request for the high-quality
versions of the pictures used in this configuration.

*(Internal ID: `btn_requestIllustrations2`)*

#### Add Images to PicList

- **Where:** Select Images... (dialog)
- **Type:** Button
- **Description:** Add Images to Current Configuration's PicList
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Add the selected images to the current Configuration where an appropriate caption should be added and other image properties selected.

**Explanation:**

Adds the selected pictures to the PicList. Each one is anchored at its Bible reference (in the middle of
the chapter if the reference has no verse), with **Column Width** and top-left position. Then type a caption
for each one on the **Details** sub-tab.

*(Internal ID: `btn_imagePicker_ok`)*

#### Cancel

- **Where:** Select Images... (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the catalogue without adding pictures.

*(Internal ID: `btn_imagePicker_cancel`)*

#### Limit to Range of References

- **Where:** Select Images... (dialog)
- **Type:** Text box
- **View level:** Default and Full views

**Explanation:**

Shows only pictures for these references. It starts with the books you are printing. You can type ranges
such as `GEN 1-3; MRK`. Use 3-letter book codes. Clear the box to see all pictures in the set. Press Enter
or click **Search + Update Images** to apply it.

*(Internal ID: `t_artRefRange`)*

#### Search

- **Where:** Select Images... (dialog)
- **Type:** Search box
- **Description:** Image Selection Dialog: Search for an image by keyword
- **View level:** Default and Full views

**Explanation:**

Finds pictures by words in their keywords or title, for example `boat` or `shepherd`. Press Enter or click
**Search + Update Images** to apply it. Clear the box to show all pictures again.

*(Internal ID: `t_artSearch`)*

#### Image Set

- **Where:** Select Images... (dialog)
- **Type:** Drop-down list
- **View level:** Default and Full views
- **Choices:** Default

**Explanation:**

Chooses which installed image set to show. PTXprint remembers your last choice. To get more image sets,
click **Download Image Set...**.

*(Internal ID: `ecb_artPictureSet`)*

#### Enter a name for the configuration to be saved.

- **Where:** Select Images... (dialog)
- **Type:** Text box
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Enter a name for the configuration to be saved.
>
> Note that only Roman/Latin names are supported using: a-z A-Z, 0-9, parentheses, underscores and hyphens.
>
> Longer descriptions may be typed into the Notes field below.

#### Scripture Reference

- **Where:** Select Images... (dialog)
- **Type:** Radio button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Sort the images according to the canonical order of scripture.

**Explanation:**

Sorts the pictures in Bible order, by the reference that matches your reference range.

*(Internal ID: `r_imgSort_ref`)*

#### Frequency of Use

- **Where:** Select Images... (dialog)
- **Type:** Radio button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Sort the images based on how often other projects use them. The most popular illustrations appear at the top of the list.

**Explanation:**

Sorts the pictures so that those used most often by other projects come first.

*(Internal ID: `r_imgSort_pop`)*

#### tv_artists

- **Where:** Select Images... (dialog)
- **Type:** Table
- **View level:** Default and Full views

**Explanation:**

The list of artists (picture series) in the image set. Tick one or more artists to show only their
pictures. Untick all of them to show every artist.

*(Internal ID: `tv_artists`)*

#### Search + Update Images

- **Where:** Select Images... (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Updates the thumbnails after you change the search words or the reference range. It is only active when
something has changed.

*(Internal ID: `btn_imgRefresh`)*

#### Print

- **Where:** Select Images... (dialog)
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Filter for illustrations that can be used in Print/PDF publications.

**Explanation:**

Meant to show only pictures that may be used in print. At the time of writing, this box does not change which thumbnails are shown.

*(Internal ID: `c_imgMediaP`)*

#### App

- **Where:** Select Images... (dialog)
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Filter for illustrations that can be used in mobile phone Apps.

**Explanation:**

Meant to show only pictures that may be used in phone apps. At the time of writing, this box does not change which thumbnails are shown.

*(Internal ID: `c_imgMediaA`)*

#### Web

- **Where:** Select Images... (dialog)
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Filter for illustrations that can be used on websites.

**Explanation:**

Meant to show only pictures that may be used on websites. At the time of writing, this box does not change which thumbnails are shown.

*(Internal ID: `c_imgMediaW`)*

#### Reference

- **Where:** Select Images... (dialog)
- **Type:** Label
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Note that if a reference only contains a book and chapter number (with no specific verse mentioned), then the illustration will be placed in the middle of the chapter.

**Explanation:**

The references of the picture under the mouse. The reference shown in bold is the one that PTXprint will
use as the anchor. References in red already have this picture in your PicList.

*(Internal ID: `lb_imgRefs`)*

#### Clear Selection

- **Where:** Select Images... (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Unselects all the selected thumbnails, so you can start your choice again.

*(Internal ID: `btn_imgClearSelection`)*

### Download & Install Image Sets (dialog)

#### OK

- **Where:** Download & Install Image Sets (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Downloads and installs the ticked image sets. This can take a while. When it is finished, the catalogue
opens.

*(Internal ID: `btn_imgSet_ok`)*

#### Cancel

- **Where:** Download & Install Image Sets (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog without downloading anything.

*(Internal ID: `btn_imgSet_cancel`)*

#### Select All / None

- **Where:** Download & Install Image Sets (dialog)
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views

**Explanation:**

Ticks or unticks all the image sets in the list. Remember that some sets are large downloads.

*(Internal ID: `c_imgSet_selectAll`)*

#### tv_imagesets

- **Where:** Download & Install Image Sets (dialog)
- **Type:** Table
- **View level:** Default and Full views

**Explanation:**

The list of image sets that you can download, with artist, style, size and licence. Tick the sets you want,
then click **OK**. Sets marked **Installed** cannot be ticked. Hover over a row for more information.

*(Internal ID: `tv_imagesets`)*

#### Install from ZIP file...

- **Where:** Download & Install Image Sets (dialog)
- **Type:** Link
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Install an image set from a local ZIP file. Useful for offline installations or shared image sets at workshops (avoids repeated large downloads).

**Explanation:**

Installs an image set from a ZIP file on your computer, without downloading it. If the set has terms of
use, you must agree to them. A ZIP file with only pictures in it is unpacked into the project's
`local\figures` folder.

*(Internal ID: `btn_installFromZip`)*

### Illustration Credit Overlay (dialog)

#### OK

- **Where:** Illustration Credit Overlay (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Saves the credit overlay settings for this picture (and for the series, if chosen).

*(Internal ID: `btn_ovrly_ok`)*

#### Cancel

- **Where:** Illustration Credit Overlay (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog without changing the credit.

*(Internal ID: `btn_ovrly_cancel`)*

#### Vertical Position

- **Where:** Illustration Credit Overlay (dialog)
- **Type:** Drop-down list
- **Description:** Image credit dialog: Vertical position of text
- **View level:** Default and Full views
- **Choices:** Top; Center; Bottom; Fill

**Explanation:**

Puts the credit at the top, centre or bottom of the picture.

*(Internal ID: `fcb_plCreditVpos`)*

#### Horizontal Position

- **Where:** Illustration Credit Overlay (dialog)
- **Type:** Drop-down list
- **Description:** Image credit dialog: Horizontal position of text
- **View level:** Default and Full views
- **Choices:** Left; Center; Right; Inner; Outer

**Explanation:**

Puts the credit at the left, centre or right of the picture, or on the inner (binding) or outer side.
Inner and outer are useful if the picture may be mirrored or appear on both odd and even pages.

*(Internal ID: `fcb_plCreditHpos`)*

#### Background Box

- **Where:** Illustration Credit Overlay (dialog)
- **Type:** Drop-down list
- **Description:** Image credit dialog: Background color
- **View level:** Default and Full views
- **Choices:** None; Light; Dark

**Tooltip (the text shown when you hover the mouse over it):**

> Specify the kind of box (Light/Dark background) or enter the name of a style which should be applied. By selecting a (custom) style, you can change multiple parameters at once: font, size and color.

**Explanation:**

Prints a light or dark box behind the credit so that it can be read on any picture. You can also type the
name of your own style for the credit to change its font, size and colour together.

*(Internal ID: `ecb_plCreditBoxStyle`)*

#### Rotation

- **Where:** Illustration Credit Overlay (dialog)
- **Type:** Drop-down list
- **Description:** Image credit dialog: Rotation of text
- **View level:** Default and Full views
- **Choices:** None; Anti-clockwise; Clockwise

**Tooltip (the text shown when you hover the mouse over it):**

> Sometimes the credit text needs to be rotated.

**Explanation:**

Turns the credit text so that it runs up (anti-clockwise) or down (clockwise) the side of the picture.
Useful when the credit is placed at the left or right edge.

*(Internal ID: `fcb_plCreditRotate`)*

#### Image Credit Text

- **Where:** Illustration Credit Overlay (dialog)
- **Type:** Text box
- **Description:** Image credit dialog: Credit (copyright) text
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Type the text for the Credit to be overlaid on the image. Note that there are shortcuts:  
>    (c)   --> ©  
>    dcc  --> © David C Cook  
>        or --> © DCC   (if Sensitive Project is set)

**Explanation:**

The credit text printed on the picture. Type `(c)` to get ©. Type `dcc` to get the David C Cook credit (a
shorter form is used if **Sensitive Project** is ticked on the **Advanced** tab). Keep it short; it is
printed in small letters.

*(Internal ID: `t_plCreditText`)*

#### Apply to ALL images in this series

- **Where:** Illustration Credit Overlay (dialog)
- **Type:** Checkbox (not ticked by default)
- **Description:** Image credit dialog: Apply to all images in series
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The same Credit Overlay text can be applied to all images that match this illustration's filename (e.g. CN01234.tif, CN05654.tif, etc.) You can then adjust the position, background and rotation for specific illustrations later.
>
> Setting this option will not affect illustrations which already have Credit Overlay settings.

**Explanation:**

Uses this credit for all pictures of the same series (the same two letters at the start of the file name,
for example all `cn` pictures). Pictures that already have a credit are not changed unless you also tick
**Overwite any existing settings**.

*(Internal ID: `c_plCreditApply2all`)*

#### \x-credit

- **Where:** Illustration Credit Overlay (dialog)
- **Type:** Link
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the Credit Overlay properties on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the `x-credit` style, where you can change the font, size and colours of all
credit overlays.

*(Internal ID: `lb_style_x-credit`)*

#### Overwrite any existing settings

- **Where:** Illustration Credit Overlay (dialog)
- **Type:** Checkbox (not ticked by default)
- **Description:** Image credit dialog: Overwrite existing values
- **View level:** Default and Full views
- **Only available when:** “Apply to ALL images in this series” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> WARNING:  
> If this option is checked, it will disregard any previous settings, and overwrite them with the new overlay information, position and other parameters.

**Explanation:**

Replaces the credit on pictures that already have one. Only available when **Apply to ALL images in this
series** is ticked. Use with care: earlier settings for individual pictures are lost.

*(Internal ID: `c_plCreditOverwrite`)*

### Add Map (dialog)

#### Add Another Map

- **Where:** Add Map (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Add as many maps as needed, one at a time.

**Explanation:**

Adds the current map and clears the form so that you can choose the next one. Finish with **OK -
Done!**, because the map book is only written then.

*(Internal ID: `btn_mapAddAnother`)*

#### OK - Done!

- **Where:** Add Map (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Adds the current map (if a file is chosen) and finishes. PTXprint writes the map pages into the map book,
ticks **Include Maps** on the **Peripherals** tab, and adds the map book to the books to print.

*(Internal ID: `btn_addMap`)*

#### Cancel

- **Where:** Add Map (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog. The map book is not written. Maps already added with **Add Another Map** may still be
in the PicList; delete them there if you do not want them.

*(Internal ID: `btn_gnr8cover_cancel1`)*

#### Book Code for Maps

- **Where:** Add Map (dialog)
- **Type:** Drop-down list
- **Description:** Maps: Book code to be used to store map details
- **View level:** Default and Full views
- **Choices:** XXM; XXA; XXB; XXC; XXD; XXE; XXF; XXG; BAK

**Tooltip (the text shown when you hover the mouse over it):**

> Select the extra book code to be used for the list of maps.
>
> An extra book (e.g. XXM) can be used to store map details. If you prefer to use one of the other standard Paratext books XXA...XXG then select it here. If the book already exists, the new maps are added at the end of it.

**Explanation:**

The extra book in which PTXprint writes the map pages. **XXM** is the usual choice. If the book already
exists, PTXprint adds the new maps at its end. Choose another XX book only if XXM is used for something
else.

*(Internal ID: `fcb_ptxMapBook`)*

### Add Map (dialog) › Add Map

#### Scale

- **Where:** Add Map (dialog) › Add Map
- **Type:** Number box
- **Description:** Scale Map Size
- **View level:** Default and Full views
- **Values:** from 0.01 to 4, default 1

**Explanation:**

Makes the map smaller or larger inside its frame. 1 means the full size of the frame.

*(Internal ID: `s_mapScale`)*

#### Border

- **Where:** Add Map (dialog) › Add Map
- **Type:** Drop-down list
- **Description:** Maps: Select Ornamental Border
- **View level:** Default and Full views
- **Choices:** None; Han3; Map Edge A; Map Edge B

**Tooltip (the text shown when you hover the mouse over it):**

> A selection of ornamental borders are available to choose from, to be drawn around the map.

**Explanation:**

A choice of ornamental border for the map. At the time of writing, PTXprint does not use this setting when
it adds the map.

*(Internal ID: `fcb_coordBorder`)*

#### Select Map...

- **Where:** Add Map (dialog) › Add Map
- **Type:** Button
- **Description:** Maps: Select the map image file
- **View level:** Default and Full views

**Explanation:**

Chooses the map image file (PNG, JPG, PDF or TIF). A preview is shown in the dialog.

*(Internal ID: `btn_selectMap`)*

#### Caption

- **Where:** Add Map (dialog) › Add Map
- **Type:** Text box
- **Description:** Picture: Caption
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> By default the caption will appear below the picture. To show it above the picture, tick 'Show Caption Before Image' on the Advanced tab (Other sub-tab, Pictures, Figures, Images, Sidebars).
>
> Note that captions are NOT processed by any changes specified in the PrintDraftChanges.txt file.

**Explanation:**

An optional caption for the map. Leave it empty if the map will fill the whole page to the edge.

*(Internal ID: `t_mapCaption`)*

#### Rotation

- **Where:** Add Map (dialog) › Add Map
- **Type:** Drop-down list
- **Description:** Maps: Rotation of map image
- **View level:** Default and Full views
- **Choices:** None; Anti-clockwise; Clockwise

**Tooltip (the text shown when you hover the mouse over it):**

> Rotate the map image by 90 degrees (anti-clockwise or clockwise) if needed.

**Explanation:**

Turns the map image by 90° (anti-clockwise or clockwise). Use it for a wide map on a tall page.

*(Internal ID: `fcb_mapRotate`)*

#### Size and Position...

- **Where:** Add Map (dialog) › Add Map
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Opens the **Size and Position** dialog to choose the frame size (for example a full page) and the position
of the map. The result is shown as a code in the box beside the button.

*(Internal ID: `btn_mapSizePosition`)*

#### t_mapPgPos

- **Where:** Add Map (dialog) › Add Map
- **Type:** Text box
- **View level:** Default and Full views

**Explanation:**

Shows the position code chosen with **Size and Position...**, for example `Pc` (a page of its own,
centred).

*(Internal ID: `t_mapPgPos`)*

#### Spread

- **Where:** Add Map (dialog) › Add Map
- **Type:** Checkbox (not ticked by default)
- **Description:** Spread Map Out Across Both Pages
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Only enable this option if the map needs to be spread out across both pages.

**Explanation:**

Meant for a map that spreads across two facing pages. At the time of writing, PTXprint does not use this
setting when it adds the map.

*(Internal ID: `c_mapSpread`)*

### Pictures tab

#### tv_picListEdit

- **Where:** Pictures tab
- **Type:** Table
- **View level:** Default and Full views
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Explanation:**

The PicList table: one row for each picture in this configuration. Click a row to see its settings;
double-click it to open the **Details** sub-tab; right-click it for more actions (copy the `\fig` line,
jump to Paratext, show the file, delete). Red text means the picture is too tall for the page; a grey
row means the file cannot be found.

*(Internal ID: `tv_picListEdit`)*

#### Del

- **Where:** Pictures tab
- **Type:** Button
- **Description:** Delete picture(s) from PicList
- **View level:** Default and Full views
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to immediately delete the currently highlighted picture(s). No confirmation will be asked for!

**Explanation:**

Deletes the selected picture(s) from the PicList at once. There is no question and no undo, so check the
selection first. It does not change the Paratext text or the picture file.

*(Internal ID: `btn_plDel`)*

#### Generate...

- **Where:** Pictures tab
- **Type:** Button
- **Description:** Generate the PicList
- **View level:** Default and Full views
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This button will (re-)generate the PicList from the USFM \fig ... \fig* definitions.
>
> If you just want to (re-)generate the PicList for a single book, then select that book on the Basic tab.

**Explanation:**

Builds the PicList from the `\fig` entries in the Paratext books. If no PicList exists yet, it does this
at once; otherwise the **Generate PicList** dialog asks what to do. Use it after pictures are added in
Paratext.

*(Internal ID: `btn_plGenerate`)*

#### Add

- **Where:** Pictures tab
- **Type:** Button
- **Description:** Add picture to PicList
- **View level:** Default and Full views
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to add another picture to the PicList. You will need to fill in all the details in the area below.

**Explanation:**

Adds a new picture. PTXprint asks you to choose a picture file, then adds a row and opens the
**Details** sub-tab. You must then type the **Anchor Ref** (for example `JHN 3.16`) and a caption. Only
the file name is saved, so the file must be in a folder that PTXprint searches.

*(Internal ID: `btn_plAdd`)*

#### Refresh List

- **Where:** Pictures tab
- **Type:** Button
- **Description:** Refresh (reload) picture captions from Paratext
- **View level:** Default and Full views
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Refresh Captions:  
> If you have edited the picture captions within the Paratext USFM files but those changes are not being reflected here, then click this button to refresh the captions.
>
> Note that only the Captions and Verse Refs will be updated. All other size and position settings will remain unchanged.

**Explanation:**

Copies the captions and caption references again from the `\fig` entries in Paratext. Use it after the
captions were corrected in Paratext. Sizes, positions and other settings in PTXprint stay the same.

*(Internal ID: `btn_refreshCaptions`)*

#### Add Maps...

- **Where:** Pictures tab
- **Type:** Button
- **Description:** Add Maps to the Publication
- **View level:** Default and Full views
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Maps for the end of the publication can be added to one of the XX* books or to the XXM book using this dialog.

**Explanation:**

Opens the **Add Map** dialog to add map pages at the end of the publication.

*(Internal ID: `btn_addMaps2`)*

#### Edit Maps...

- **Where:** Pictures tab
- **Type:** Button
- **Description:** Edit Maps module
- **View level:** Default and Full views
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Switch to the View+Edit tab to show/edit the Maps module.

**Explanation:**

Opens the map book (for example XXM) on the **View+Edit** tab so that you can look at or change it. It
does nothing if the map book does not exist yet; use **Add Maps...** first.

*(Internal ID: `btn_editMaps2`)*

#### Show Catalogue...

- **Where:** Pictures tab
- **Type:** Button
- **View level:** Default and Full views
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Browse the catalogue of commonly used Bible illustrations from a range of different artists.

**Explanation:**

Opens the **Select Images** dialog (the catalogue) so that you can browse an image set and add pictures
to the PicList. If no image set is installed, the download dialog opens first.

*(Internal ID: `btn_getPictures`)*

#### Show Active Books

- **Where:** Pictures tab
- **Type:** Checkbox (not ticked by default)
- **Description:** Only show pictures used in the set of active books
- **View level:** Default and Full views
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Select this option to only display the pictures from the books that are currently in focus to be printed. When unchecked, then the list will show pictures from ALL the books in the project that have been added to the PicList. If pictures of a certain book are missing, then you may need to select that book and Generate the PicList details just for *that* book.

**Explanation:**

When ticked, the table shows only the pictures of the books selected for printing (on the **Basic** tab).
When not ticked, it shows the pictures of all books in the PicList. This only changes what you see; it
does not delete anything.

*(Internal ID: `c_filterPicList` · Config key: `config/filterpics`)*

#### Image

- **Where:** Pictures tab
- **Type:** Radio button
- **Description:** Show preview of pictures
- **View level:** Default and Full views
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Display the picture currently in focus. Note that this is dependent on the image being located in the specified folder(s).

**Explanation:**

Shows a preview of the selected picture in the box beside the table. If the box is empty, PTXprint could
not find the picture file. Hover over the preview to see the file path.

*(Internal ID: `r_image_preview`)*

#### Position

- **Where:** Pictures tab
- **Type:** Radio button
- **Description:** Show position of picture on page
- **View level:** Default and Full views
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Show the relative position of the picture on the page. When Inner/Outer is used, the position displayed represents the odd/right-hand page of a spread.

**Explanation:**

Shows a small drawing of a page with the selected picture in its position. Use it to check the **Frame
Size** and position settings before you print.

*(Internal ID: `r_image_location`)*

#### Global Options

- **Where:** Pictures tab
- **Type:** Label
- **View level:** Basic, Default and Full views
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Overview of the Pictures used in the publication.

**Explanation:**

The **Global Options** sub-tab. It holds the settings that apply to every picture: resolution, captions,
missing pictures and the folders where PTXprint looks for picture files.

*(Internal ID: `lb_settings`)*

#### Details

- **Where:** Pictures tab
- **Type:** Label
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Use this tab to change the position, location, size or orientation of the images.
>
> Note: Any changes you make here will NOT be reflected in the Paratext USFM files. So if you are changing an illustration, its caption or frame size (column or span), then it is advisable to do so in Paratext before regenerating the PicList here.

**Explanation:**

The **Details** sub-tab. It shows the settings of the picture selected in the table, such as anchor,
caption, size and position. Remember that changes here are not copied into the Paratext text.

*(Internal ID: `lb_details`)*

#### Checklist

- **Where:** Pictures tab
- **Type:** Label
- **View level:** Default and Full views
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This tab encourages you to think through the appropriateness of the pictures used in this publication, as well as other contexts.

**Explanation:**

The **Checklist** sub-tab. Use it to record whether each picture is clear, culturally acceptable and
approved. When this sub-tab is open, a **Filter Checklist** area appears above the table.

*(Internal ID: `lb_checklist`)*

### Pictures tab › Filter Checklist

#### Filter pictures for checklist

- **Where:** Pictures tab › Filter Checklist
- **Type:** Drop-down list
- **View level:** Not normally shown
- **Choices:** All; All Unknown / Unchecked; Any Unknown / Unchecked; Approved
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The list of pictures can be filtered according to the status of the checking values.

**Explanation:**

Shows only some pictures in the table, based on the **Checklist** answers. **All Unknown / Unchecked**
shows pictures where no question has been answered yet. **Any Unknown / Unchecked** shows pictures where
at least one question is still open. **Approved** shows the approved pictures. It is only shown when the
**Checklist** sub-tab is open.

*(Internal ID: `fcb_chklstFilter`)*

#### Exclude Matched

- **Where:** Pictures tab › Filter Checklist
- **Type:** Checkbox (not ticked by default)
- **Description:** Exclude (don't show) pictures that match filter
- **View level:** Not normally shown
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Flip the results of the filtered list to exclude any items that match.

**Explanation:**

Turns the filter round: the table shows the pictures that do **not** match the filter. For example,
choose **Approved** and tick this to see all pictures that are not approved yet.

*(Internal ID: `c_picCheckInvFilter`)*

### Pictures tab › Global Options tab › Include Pictures (illustrations)

#### High Resolution (Larger File)

- **Where:** Pictures tab › Global Options tab › Include Pictures (illustrations)
- **Type:** Radio button
- **Description:** Use high-resolution pictures
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> If this option is selected, PTXprint prefers TIF, then PNG, then JPG files (and the larger file if there are two of the same type).
>
> The original higher-quality illustrations are usually larger (.TIF .PNG or .PDF files) and are stored in the local\Figures folder so that they are not shared via Send/Recv. If these are used, the resulting PDF could be very large, and therefore difficult to share electronically, but the image quality will be as good as possible.

**Explanation:**

Use this for the final print PDF. PTXprint prefers TIF, then PNG, then JPG files, and if there are two
files of the same type, the larger one. The PDF can be very large. The **Request Access...** button is
only available with this option.

*(Internal ID: `r_pictureRes_High` · Config key: `document/picresolution=High`)*

#### Low Resolution (Smaller File)

- **Where:** Pictures tab › Global Options tab › Include Pictures (illustrations)
- **Type:** Radio button
- **Description:** Use low-resolution pictures
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Paratext stores low resolution .JPG versions of illustrations in the project's "Figures" folder. If these are used, the file size of the resulting PDF will be relatively small, and therefore easy to share, but the image quality will be low.

**Explanation:**

Use this for drafts. PTXprint prefers JPG files and, if there are two of the same type, the smaller one.
The PDF is small and easy to share, but pictures may look blurred when printed.

*(Internal ID: `r_pictureRes_Low` · Config key: `document/picresolution=Low`)*

#### Use Place-holders (Smallest PDF File)

- **Where:** Pictures tab › Global Options tab › Include Pictures (illustrations)
- **Type:** Checkbox (not ticked by default)
- **Description:** Pictures: Only show empty place-holders
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Use this option to include an empty box wherever illustrations would be placed in the final PDF.
>
> WHY would someone want to do this? It is sometimes necessary to generate the smallest possible PDF file (usually in order to send by e-mail) or to produce a PDF to be printed without illustrations.

**Explanation:**

Prints an empty box instead of each picture. The page layout stays the same, so you can check the layout
with a very small PDF. Untick it for the final PDF.

*(Internal ID: `c_figplaceholders` · Config key: `document/iffigplaceholders`)*

#### Omit Pictures Only Meant for Web or App

- **Where:** Pictures tab › Global Options tab › Include Pictures (illustrations)
- **Type:** Checkbox (ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Only allow illustrations with the 'P'rint attribute.
>
> If the illustrations have been marked up with the w/a/p notation, then it is easy to exclude any illustrations that do not have the 'p' attribute.  Note: w= web, a=app, p=print.

**Explanation:**

Leaves out pictures that are marked only for web or app use (not for print). Keep it ticked for printed
publications.

*(Internal ID: `c_figexclwebapp` · Config key: `document/iffigexclwebapp`)*

#### How?

- **Where:** Pictures tab › Global Options tab › Include Pictures (illustrations)
- **Type:** Link
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Open a web page that explains how to mark pictures in Paratext for print, web or app.

**Explanation:**

Opens a web page that explains how to mark pictures in Paratext as meant for print, web or app.

*(Internal ID: `lb_omitPics`)*

#### Omit Captions

- **Where:** Pictures tab › Global Options tab › Include Pictures (illustrations)
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> If you want to suppress the picture captions from being displayed below the picture, then check this option.

**Explanation:**

Prints the pictures without captions or caption references. When ticked, **Omit References (ch:vs)** is
greyed out.

*(Internal ID: `c_fighidecaptions` · Config key: `document/iffigshowcaptions`)*

#### Omit References (ch:vs)

- **Where:** Pictures tab › Global Options tab › Include Pictures (illustrations)
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **Greyed out when:** “Omit Captions” is ticked
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> If you only want to suppress the reference part of the caption, then check this option. Note that it is not possible to just have the references without the captions.

**Explanation:**

Keeps the caption text but removes the chapter:verse reference after it. Greyed out when **Omit
Captions** is ticked.

*(Internal ID: `c_fighiderefs` · Config key: `document/iffighiderefs`)*

#### Omit Missing Pictures ...

- **Where:** Pictures tab › Global Options tab › Include Pictures (illustrations)
- **Type:** Checkbox (ticked by default)
- **Description:** Omit Missing Pictures
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Rather than aborting the PDF export process, pre-process the list of illustrations and skip/ignore/remove any which are not found in the specified location of image files.
>
> If Pictures are missing after preparing a PDF, then they will be listed in the section below.

**Explanation:**

When ticked, pictures whose files cannot be found are left out, and printing continues. After printing,
the number of missing pictures is shown next to this option and the file names are listed at the bottom
of the sub-tab. Keep it ticked, but check the count before the final print.

*(Internal ID: `c_skipmissingimages` · Config key: `document/iffigskipmissing`)*

#### Remove Image Borders

- **Where:** Pictures tab › Global Options tab › Include Pictures (illustrations)
- **Type:** Checkbox (not ticked by default)
- **Description:** Pictures: Remove Image Borders
- **View level:** Basic, Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Some images have a thin line on one or more of the edges of the picture. Enable this option to automatically crop these unwanted lines from the edge of pictures. Note that this setting affects ALL images, not just those with lines.

**Explanation:**

Cuts thin lines off the edges of pictures. It is applied to every picture, so check that no picture loses
part of its content. The pictures are converted to JPG when this is on.

*(Internal ID: `c_cropborders` · Config key: `document/iffigcrop`)*

#### Request Access...

- **Where:** Pictures tab › Global Options tab › Include Pictures (illustrations)
- **Type:** Button
- **View level:** Default and Full views
- **Only available when:** “High Resolution (Larger File)”, “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Request Access to High Quality Illustrations/Maps in the SIL repository.
>
> Click this button to fill in the form requesting access to the illustrations used in the current publication.
>
> After completing and submitting the online form you should receive an immediate response by email with a link to download the illustrations (if approved).

**Explanation:**

Opens an online form to ask for access to the high-quality versions of the illustrations used in this
configuration. PTXprint fills in the project name and the list of pictures. You must add your email and
supervisor details. Only available with **High Resolution**.

*(Internal ID: `btn_requestIllustrations`)*

#### Get Permission...

- **Where:** Pictures tab › Global Options tab › Include Pictures (illustrations)
- **Type:** Button
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> If you are publishing (i.e. more than 50 copies) any material with illustrations that require prior permission to be obtained before publishing, then click this button to automatically fill in the form requesting permission.
>
> Note that any missing information will need to be filled in on the Peripherals tab before the form can be submitted.
>
> After filling in any remaining details, you will need to submit the Google form and wait for a response.

**Explanation:**

Opens an online form to ask permission to publish pictures that need permission (usually when you print
more than 50 copies). PTXprint fills in the list of pictures and the publication details. If details such
as country, language or number of copies are missing, PTXprint opens the **Peripherals** tab so that you can
fill them in first.

*(Internal ID: `btn_requestPermission`)*

#### Use Other Location

- **Where:** Pictures tab › Global Options tab › Include Pictures (illustrations)
- **Type:** Checkbox (not ticked by default)
- **Description:** Use pictures from a particular folder
- **View level:** Basic, Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The following locations are scanned for pictures:  
>   My Paratext ... Projects\\figures  
>   My Paratext ... Projects\\local\figures  
>   Users\...\AppData\Local\SIL\ptxprint\imagesets
>
> If your pictures are in a different folder, then enable this option and select a Picture Folder to be scanned in addition to the folders listed above. Note that ALL subfolders are also scanned unless you explicitly enable the 'Exclude Subfolders' option.

**Explanation:**

Tick this if your pictures are in a folder that PTXprint does not search by itself. When you tick it and
no folder is chosen yet, PTXprint asks for the folder. This folder is searched in addition to the usual
ones.

*(Internal ID: `c_useCustomFolder` · Config key: `document/customfiglocn`)*

#### Picture Folder...

- **Where:** Pictures tab › Global Options tab › Include Pictures (illustrations)
- **Type:** Button
- **Description:** Select the folder which contains pictures
- **View level:** Basic, Default and Full views
- **Only available when:** “Use Other Location”, “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Select another folder which contains pictures. PTXprint will also scan the selected folder (and all its sub-folders) looking for all the required illustrations in the Picture List.

**Explanation:**

Chooses the extra folder with picture files. The chosen folder is shown beside the button. Only available
when **Use Other Location** is ticked.

*(Internal ID: `btn_selectFigureFolder` · Config key: `document/customfigfolder`)*

#### Exclude Subfolders

- **Where:** Pictures tab › Global Options tab › Include Pictures (illustrations)
- **Type:** Checkbox (not ticked by default)
- **Description:** Pictures: Exclusively Use Selected Folder
- **View level:** Default and Full views
- **Only available when:** “Use Other Location”, “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> PTXprint normally searches all the sub-folders of the specified folder locations for the pictures it needs.
>
> If you would prefer that it only searches in the folder specified directly (and NOT look in any subfolders) then select this option. This should speed up searches for images, but may result in some images not being found at all.

**Explanation:**

Asks PTXprint not to search the subfolders of the picture folders. This can make searching faster, but
pictures in subfolders may not be found. It is unticked automatically when you untick **Use Other
Location**.

*(Internal ID: `c_exclusiveFiguresFolder` · Config key: `document/exclusivefolder`)*

#### Image Types

- **Where:** Pictures tab › Global Options tab › Include Pictures (illustrations)
- **Type:** Text box
- **Description:** Pictures: Preferred image types
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

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

**Explanation:**

Leave this empty unless you have a reason. If the same picture exists as several file types, PTXprint uses
the first type in this list. For example, `PDF TIF PNG` prefers PDF files; `JPG` alone uses only JPG
files and ignores the others. Separate the types with spaces.

*(Internal ID: `t_imageTypeOrder` · Config key: `document/imagetypepref`)*

### Pictures tab › Global Options tab

#### Include Pictures (illustrations)

- **Where:** Pictures tab › Global Options tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Basic, Default and Full views
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This setting enables/disables all the other settings relating to pictures.
>
> Note that it is important to provide proper copyright attribution for the illustrations used in a publication, and this can be done very easily using the \zimagecopyrights magic code within the Colophon (see the Peripherals tab for details).

**Explanation:**

The main switch for pictures. When ticked, PTXprint loads the PicList for this configuration and prints
the pictures. When not ticked, no pictures are printed, the **Details** and **Checklist** sub-tabs are
hidden, and the picture settings are greyed out. Turning it on can make printing slower.

*(Internal ID: `c_includeillustrations` · Config key: `document/ifinclfigs`, `document/ifusepiclist`, `document/includeimg`)*

### Pictures tab › Details tab

#### Anchor Ref

- **Where:** Pictures tab › Details tab
- **Type:** Text box
- **Description:** Picture: Anchor reference
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

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

**Explanation:**

The anchor: where the picture belongs in the text, for example `MRK 4.39` (book code, space, chapter,
dot, verse). PTXprint changes `:` into `.` and the book code into capital letters for you. If the anchor
is empty, PTXprint will not let you move to another row. See the "Details" section for diglot, glossary
and paragraph forms.

*(Internal ID: `t_plAnchor`)*

#### Caption Ref

- **Where:** Pictures tab › Details tab
- **Type:** Text box
- **Description:** Picture: Caption reference
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The reference in the caption can be a single Ch:Vs or a range of verses 6:17-29. This Caption Ref is different from and independent of the Anchor Ref setting.
>
> By default, the caption will be followed by a Ch:Vs reference in parentheses ( ).
>
> To put the Caption Ref BEFORE the caption text, tick 'Ref Before Caption' on the Advanced tab (Other sub-tab, Pictures, Figures, Images, Sidebars).
>
> To prevent Caption Refs from appearing globally, use the Pictures > Global Options tab option:  
>     'Omit References (ch:vs)'

**Explanation:**

The reference printed after the caption, for example `4:39` or `6:17-29`. It can be different from the
anchor. To hide all caption references, use **Omit References (ch:vs)** on **Global Options**.

*(Internal ID: `t_plRef`)*

#### Description: (Alt Text)

- **Where:** Pictures tab › Details tab
- **Type:** Text box
- **Description:** Picture: Description (alternative text)
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Explanation:**

A short description of what the picture shows. It helps you recognise the picture in the table. Pictures
added from the catalogue get the catalogue title here.

*(Internal ID: `t_plAltText`)*

#### Filename

- **Where:** Pictures tab › Details tab
- **Type:** Text box
- **Description:** Picture: Image filename
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Note that any changes you make to the filename here will NOT automatically be updated in the Paratext USFM files. Please edit/fit the figure information manually in Paratext if you change things here in PTXprint.

**Explanation:**

The name of the picture file, without a folder. PTXprint looks for this name in the picture folders. If
you change it, the preview and the missing-file check are updated.

*(Internal ID: `t_plFilename`)*

#### Copyright Attribution

- **Where:** Pictures tab › Details tab
- **Type:** Text box
- **Description:** Picture: Copyright attribution
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> There are several shortcuts you can use:  
>    (c) --> ©  the copyright sign  
>    (r) --> ®  to denote registered trademarks  
>    (tm) --> ™  to denote trademarks in general
>
> For commonly used series of illustrations, PTXprint can automatically generate the appropriate copyright attribution statement(s) as part of the colophon text.
>
> For other less-known artists' you may enter the appropriate copyright information which is usually in the format of:  
>    by Artist Name © Year, Entity Name and License Type.

**Explanation:**

The copyright credit for a picture that PTXprint does not know. It is used in the list of picture credits
that `\zimagecopyrights` prints in the colophon. For known series this box is hidden and **Automatic** is
shown instead.

*(Internal ID: `t_plCopyright`)*

#### Scale

- **Where:** Pictures tab › Details tab
- **Type:** Number box
- **Description:** Picture: Scale
- **View level:** Default and Full views
- **Values:** from 5 to 200, default 100
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> An image (illustration) can be scaled to the given size. This is particularly useful for cutout images, and can prevent them from taking up too much space within the text.

**Explanation:**

Makes the picture smaller or larger inside its frame. 100% fills the frame width. Use smaller values
(for example 30–60%) for cutouts and small pictures. If the picture's row turns red, the picture is too
tall to fit on the page; reduce the scale.

*(Internal ID: `s_plScale`)*

#### Vertical Position

- **Where:** Pictures tab › Details tab
- **Type:** Drop-down list
- **Description:** Picture: Vertical position
- **View level:** Default and Full views
- **Choices:** Top; Bottom; Below Notes; Before Verse; After Paragraph; Cutout
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

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

**Explanation:**

Where the picture goes on the page or in the text. The choices depend on **Frame Size**: Span Width allows
**Top**, **Bottom** and **Below Notes**; Column Width allows **Top**, **Bottom**, **Before Verse**, **After
Paragraph** and **Cutout**; the page sizes allow **Top**, **Center** and **Bottom**. **Before Verse**,
**After Paragraph** and **Cutout** are PTXprint extensions and may not work in other programs.

*(Internal ID: `fcb_plPgPos`)*

#### Frame Size

- **Where:** Pictures tab › Details tab
- **Type:** Drop-down list
- **Description:** Picture: Frame size
- **View level:** Default and Full views
- **Choices:** Column Width; Span Width; Page (in Margins); Page (to Edge)
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

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

**Explanation:**

How wide the picture's area is. Choose this first, because it changes the choices in **Vertical Position**
and **Horizontal Position**. Use **Page (to Edge)** for full-page maps, without a caption.

*(Internal ID: `fcb_plSize`)*

#### Horizontal Position

- **Where:** Pictures tab › Details tab
- **Type:** Drop-down list
- **Description:** Picture: Horizontal position
- **View level:** Default and Full views
- **Choices:** Left; Center; Right; Inner; Outer; -
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The options available here change based on the Frame Size and Vertical Position settings. So if you can't find an option you are looking for, then check those settings first.

**Explanation:**

Left, right, centre, inner (near the binding) or outer (near the outside edge). Inner and outer are useful
when pages are mirrored, so that a picture stays on the same side relative to the binding. Greyed out for
**Span Width**. **Center** is only offered for **Before Verse**, **After Paragraph** and the page sizes.

*(Internal ID: `fcb_plHoriz`)*

#### Mirror

- **Where:** Pictures tab › Details tab
- **Type:** Label
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> It is good typesetting practice to make people look outwards from the gutter, so you can set whether the image is to be mirrored just on odd pages or even pages.
>
> Some artists' pictures do not take into account the "dirty left-hand" culture. For example, it would be "awkward" to use a picture where Jesus is healing a person using his LEFT hand! What an insult!
>
> So this option allows the image to be mirrored (on both pages) in order to make the left become right. But you should check carefully to see what other unwanted side effects this mirroring may cause.
>
> Note: This option will be grayed out if the picture has the "Never Mirror" setting checked on the Checklist tab.

#### Mirror

- **Where:** Pictures tab › Details tab
- **Type:** Drop-down list
- **Description:** Picture: Mirroring options
- **View level:** Default and Full views
- **Choices:** Never; Odd; Even; Always
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Never = The image will never be mirrored Odd = Mirrored only if image ends up on an odd page Even = Mirrored only if image ends up on an even page Always = Always mirrored (regardless of where it ends up)
>
> Note that if this option is grayed out, it is because you have already restricted the mirroring options on the Checklist tab.

**Explanation:**

Flips the picture from left to right. **Odd** or **Even** flips it only when it lands on an odd or even
page; this may need the PDF to be made twice to be right. Check the flipped picture carefully: writing
in it will be backwards. Greyed out when the **Checklist** sub-tab says **Never mirror** or **Always
mirror**.

*(Internal ID: `fcb_plMirror`)*

#### Number of Lines

- **Where:** Pictures tab › Details tab
- **Type:** Label
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Some vertical position options allow a picture to be moved up or down by a number of lines or paragraphs.
>
> -Negative (minus) values specify to move UP. +Positive (plus) values specify to move DOWN.
>
> Negative counts for cutouts raise the image, but the cutout will not affect earlier paragraphs. Note that negative and fractional paragraph counts are invalid.

**Explanation:**

The label for **Number of Lines**. It changes to "Number of paragraphs" when **Vertical Position** is
**After Paragraph**.

*(Internal ID: `l_plOffsetNum`)*

#### Number of Lines

- **Where:** Pictures tab › Details tab
- **Type:** Number box
- **Description:** Picture: Lines to adjust vertically
- **View level:** Default and Full views
- **Values:** from -24 to 24
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Some vertical position options allow a picture to be moved up or down by a number of lines or paragraphs.
>
> -Negative (minus) values specify to move UP. +Positive (plus) values specify to move DOWN.
>
> Negative counts for cutouts raise the image, but the cutout will not affect earlier paragraphs. Note that negative and fractional paragraph counts are invalid.

**Explanation:**

Only used with **Cutout** and **After Paragraph**. For a cutout, it is the number of lines below the start
of the paragraph where the picture starts (decimals allowed; negative values raise the picture). For
After Paragraph, it is the number of paragraphs (whole numbers only).

*(Internal ID: `s_plLines`)*

#### Print

- **Where:** Pictures tab › Details tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Can be used in Print/PDF publications.

**Explanation:**

Ticked = the picture is printed in the PDF. Untick it to leave this picture out of print without deleting
it from the PicList. Greyed out if the artist's licence does not allow this use.

*(Internal ID: `c_plMediaP`)*

#### App

- **Where:** Pictures tab › Details tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Can be used in mobile phone Apps.

**Explanation:**

Marks the picture as allowed in phone apps. It does not change the PDF. Greyed out if the artist's licence
does not allow this use.

*(Internal ID: `c_plMediaA`)*

#### Web

- **Where:** Pictures tab › Details tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Can be used on websites.

**Explanation:**

Marks the picture as allowed on websites. It does not change the PDF. Greyed out if the artist's licence
does not allow this use.

*(Internal ID: `c_plMediaW`)*

#### Automatic

- **Where:** Pictures tab › Details tab
- **Type:** Label
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> If the image is from the recognized set of pictures commonly used in Scripture publications, then there is no need to fill in the Copyright Attribution field, as this will be generated automatically for you.

**Explanation:**

Shown instead of the **Copyright Attribution** box when the picture belongs to a series that PTXprint
knows. The credit is then created for you.

*(Internal ID: `l_autoCopyAttrib`)*

#### © ...

- **Where:** Pictures tab › Details tab
- **Type:** Button
- **Description:** Picture: Credit overlay options
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Credit Overlays... Some artists (e.g. David C Cook) require that each image has a copyright message printed on the image itself. The text and location can be set here.

**Explanation:**

Opens the **Illustration Credit Overlay** dialog to print a small credit line on top of the picture. Some
artists require this.

*(Internal ID: `btn_overlayCredit`)*

#### Automatic

- **Where:** Pictures tab › Details tab
- **Type:** Text box
- **Description:** Picture: Credit overlay position and style
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Credit overlay position and style

**Explanation:**

Shows the current credit-overlay settings of this picture in short form: position, rotation and box (for
example `bl,0,None`). Use the **© ...** button to change them.

*(Internal ID: `t_piccreditbox`)*

#### Caption

- **Where:** Pictures tab › Details tab
- **Type:** Text box
- **Description:** Picture: Caption
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> By default the caption will appear below the picture. To show it above the picture, tick 'Show Caption Before Image' on the Advanced tab (Other sub-tab, Pictures, Figures, Images, Sidebars).
>
> Note that captions are NOT processed by any changes specified in the PrintDraftChanges.txt file.

**Explanation:**

The caption printed with the picture. To show the caption above the picture instead of below it, use
**Show Caption Before Image** on the **Advanced** tab (**Other** sub-tab). Changes here are not copied back
to Paratext.

*(Internal ID: `t_plCaption`)*

#### \fig

- **Where:** Pictures tab › Details tab
- **Type:** Link
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to edit the Figure Caption properties on the Styles tab.

**Explanation:**

Opens the **Styles** tab at the style for picture captions, where you can change the caption font, size and
alignment.

*(Internal ID: `lb_style_fig`)*

#### Extra

- **Where:** Pictures tab › Details tab
- **Type:** Text box
- **Description:** Picture: Additional attributes
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> One or more optional (x-xetex) attributes can be applied for rotation and/or PDF page selection. For example:  
> rotated 90     - anti-clockwise rotate=edge     - top to outside edge rotate=binding    - top to binding edge page=2     - select page 2 of multi-page PDF
>
> Multiple parameters should be space-separated:  
> rotate=binding page=2

**Explanation:**

Advanced options for the picture, separated by spaces. `rotated 90` turns the picture 90° anti-clockwise;
`rotate=edge` turns its top towards the outside edge; `rotate=binding` turns its top towards the binding;
`page=2` uses page 2 of a multi-page PDF file. The caption is not rotated.

*(Internal ID: `t_picXetex`)*

### Pictures tab › Checklist tab › Questions to Consider

#### Across Various Publications

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Label
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> First consider whether this picture is appropriate and culturally acceptable in any publications for this project.

#### Yes

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Radio button
- **Description:** Picture checklist: What is happening is clear
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Explanation:**

"Yes, it is clear what is happening in the picture." This answer is shared by all configurations of the
project.

*(Internal ID: `r_picclear_yes`)*

#### No

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Radio button
- **Description:** Picture checklist: What is happening is NOT clear
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Is there anything confusing or misleading in this image that the reader might misunderstand if they look at this picture apart from the text? Yes and no are both appropriate answers as some images may need to be seen alongside text in order to be understood.

**Explanation:**

"No, the picture is not clear on its own." This is not always a problem: some pictures only make sense
next to the text.

*(Internal ID: `r_picclear_no`)*

#### Unknown

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Radio button
- **Description:** Picture checklist: Not checked for clarity
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Explanation:**

Not checked yet. This is the starting value. Pictures with this answer appear in the "Unknown / Unchecked"
filters.

*(Internal ID: `r_picclear_unknown`)*

#### In This Publication

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Label
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Now consider whether there are any issues with using this picture in this particular publication (config-specific).

#### Is this image acceptable in your culture?

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Drop-down list
- **Description:** Picture checklist: Cultural acceptability
- **View level:** Default and Full views
- **Choices:** Unknown; Culturally Appropriate; Alien but Acceptable; Inappropriate
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Select the level to which this illustration is acceptable in the receptor culture.
>
> Be sure that there is nothing offensive or inappropriate in this image. This could be the way people are clothed, what actions they are doing, how they are depicted, etc. “Culturally Appropriate” means this image is in a style from this culture or a related one, “Acceptable” means this picture might be from a different culture or in a different style, but there are no issues using it. “Inappropriate” means there are issues that should prevent this image from being used. Answering “Inappropriate” will help avoid this image being used in other publications.

**Explanation:**

How acceptable the picture is in the readers' culture. This answer is shared by all configurations, so
marking a picture **Inappropriate** helps other publications of the project avoid it.

*(Internal ID: `fcb_picaccept`)*

#### OK to mirror

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Radio button
- **Description:** Picture checklist: Can mirror if needed
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> It is fine to mirror the image if needed. It would not change the impact or response of the readers.

**Explanation:**

The picture may be mirrored. The **Mirror** list on the **Details** sub-tab can then be used freely.

*(Internal ID: `r_picreverse_OK`)*

#### Never mirror

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Radio button
- **Description:** Picture checklist: Never mirror
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Ensure that this image is always shown as currently depicted in the preview. Do NOT allow it to be mirrored (reversed).

**Explanation:**

The picture must never be mirrored (for example because it contains writing). The **Mirror** list on the
**Details** sub-tab is set to **Never** and greyed out.

*(Internal ID: `r_picreverse_never`)*

#### Always mirror

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Radio button
- **Description:** Picture checklist: Always mirror
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Ensure that this image is always mirrored from what is currently shown in the preview. Therefore actions being done with the left hand will show as being done with the right hand, and vice versa.
>
> Sometimes mirroring (reversing) an image makes it acceptable since a left hand becomes a right hand, etc.
>
> Some artists' pictures do not take into account the "dirty left-hand" culture. For example, it would be "awkward" to use a picture where Jesus is healing a person using his left hand!

**Explanation:**

The picture should always be mirrored (for example so that an action is done with the right hand). The
**Mirror** list on the **Details** sub-tab is set to **Always** and greyed out.

*(Internal ID: `r_picreverse_always`)*

#### Is this picture intended for: clarification, story enhancement, filler, unknown?

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Drop-down list
- **Description:** Picture checklist: Purpose of illustration
- **View level:** Default and Full views
- **Choices:** Unknown; Clarification; Story Enhancement; Space Filler
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Select the reason for including the illustration in this particular publication.
>
> Consider how this image is used alongside the text and what function it serves. Maybe it depicts a building or item from a biblical culture, or a scene from a story.

**Explanation:**

Why the picture is used in this publication: to explain something, to make the story more lively, or to
fill space. This answer belongs to the current configuration.

*(Internal ID: `fcb_pubusage`)*

#### Yes

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Radio button
- **Description:** Picture checklist: What is happening is clear in this context
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Explanation:**

"Yes, in this place the picture helps the reader understand the text." Saved for the current
configuration.

*(Internal ID: `r_pubclear_yes`)*

#### No

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Radio button
- **Description:** Picture checklist: What is happening is NOT clear in this context
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Does the image support what the text is saying? As they read the passage does the image help in their understanding?

**Explanation:**

"No, in this place the picture does not help." Consider another picture or another position.

*(Internal ID: `r_pubclear_no`)*

#### Unchecked

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Radio button
- **Description:** Picture checklist: Not checked for clarity in this context
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Explanation:**

Not checked yet for this publication. This is the starting value.

*(Internal ID: `r_pubclear_unchecked`)*

#### Yes

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Radio button
- **Description:** Picture checklist: Carries wrong meaning in this context
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> For example, do the colors have the same meaning in the local culture? Is there anything in the background that is distracting from the story? Are there any objects, gestures, or other things that imply something unintended or that isn’t in the passage? Are there any anachronisms in the picture (a minaret in Bethlehem)?

**Explanation:**

"Yes, the picture could give a wrong meaning here" (for example colours, gestures, or things that did not
exist in Bible times). Consider changing or removing the picture.

*(Internal ID: `r_pubnoise_yes`)*

#### No

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Radio button
- **Description:** Picture checklist: Carries expected meaning in this context
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Explanation:**

"No, the picture gives the expected meaning here."

*(Internal ID: `r_pubnoise_no`)*

#### Is the image appropriate for the publication?

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Drop-down list
- **Description:** Picture checklist: Appropriateness of illustration
- **View level:** Default and Full views
- **Choices:** Unknown; Culturally Appropriate; Alien but Acceptable; Inappropriate
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Select the appropriateness of the illustration within this publication.
>
> Do the images and their style fit with the type of publication, i.e. Scripture, children’s materials, lectionary, etc.? Are people and actions depicted in acceptable ways?

**Explanation:**

Whether the picture and its style suit this kind of publication (for example a Bible, a children's book or
a lectionary). This answer belongs to the current configuration.

*(Internal ID: `fcb_pubaccept`)*

#### Unchecked

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Radio button
- **Description:** Picture checklist: Not checked if wrong meaning in this context
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Explanation:**

Not checked yet for this publication. This is the starting value.

*(Internal ID: `r_pubnoise_unchecked`)*

#### Consultant Approval

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Label
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Now consider whether there are any issues with using this picture in this particular publication (config-specific).

#### Picture checklist: Approved by date

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Text box
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The most recent date that the consultant approval updated.

**Explanation:**

The date of the consultant's approval. Type it when you tick **Approved to be used in**.

*(Internal ID: `t_pubApprDate`)*

#### Picture checklist: Approved by initials

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Text box
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Explanation:**

The initials of the person (usually the consultant) who approved the picture.

*(Internal ID: `t_pubInits`)*

#### any publication

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Radio button
- **Description:** Picture checklist: Approved for use in ANY publication
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Explanation:**

The approval is for any publication of this project. Use it when the picture is fine in every context.

*(Internal ID: `r_pubapprove_scopeAny`)*

#### this publication

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Radio button
- **Description:** Picture checklist: Approved for use in THIS publication
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Explanation:**

The approval is only for the current configuration (this publication).

*(Internal ID: `r_pubapprove_scopeThis`)*

#### Approved to be used in

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Checkbox (not ticked by default)
- **Description:** Picture checklist: Approved for use
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Explanation:**

Tick this when the picture has been approved. Then choose **any publication** or **this publication**, and
type the initials and date. Approved pictures appear when you choose **Approved** in the **Filter
Checklist** list.

*(Internal ID: `c_pubApproved`)*

#### textv_picNotes

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Text area
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Explanation:**

Free notes about the selected picture, for example questions for the consultant and the answers. (The
tooltip says the notes are shared by all configurations; in the current program they are saved with the
current configuration's checklist.)

*(Internal ID: `textv_picNotes`)*

#### Notes About This Picture

- **Where:** Pictures tab › Checklist tab › Questions to Consider
- **Type:** Label
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Use the notes area below to record anything about this picture, or to dialog with the consultant. The notes entered here will be available and editable in ALL publications of this project (not just THIS one).

### Pictures tab › Checklist tab

#### Questions to Consider

- **Where:** Pictures tab › Checklist tab
- **Type:** Label
- **View level:** Default and Full views
- **Only available when:** “Include Pictures (illustrations)” is selected
- **This tab/section appears when:** “Include Pictures (illustrations)” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Pictures are best used in situations where:  
> 1. The physical situation is not understood, or not common in the target culture.  
> 2. Where the physical situation is important to understanding the meaning of the passage (e.g., the type of clothing is often not important, but in some passages it might be).  
> 3. Where they help the reader to understand the passage.  
> 4. Where it entices the reader to read the passage.
