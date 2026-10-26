# 17. Publications tab

## 17.1 What this tab is for

Use this tab to make several similar books from one project with the same design, without
making a new configuration for each. For example: one PDF for each Gospel, or a New Testament
and a separate book of Psalms, each with its own title.

A **publication** here means this configuration, printed with

* its own list of books, and
* its own values for some front matter variables (for example the main title and the
  subtitle).

All other settings (page size, fonts, layout, front matter, cover and so on) come from the
current configuration. Make a list of publications, tick the ones you want, and click
**Print Selected**. PTXprint makes one PDF for each ticked publication.

This tab is only shown in the **Full** view. (In the other views the **Pub** column in the
variables table on the **Peripherals** tab is hidden too.)

## 17.2 The list of publications

The list has three columns:

* **Print** – tick the publications to print. The checkbox in the column heading ticks or
  unticks all at once.
* **Publication ID / Field** – on the first (bold) line of each publication, its name. Under
  it, the names of its fields (variables).
* **Books / Value** – on the bold line, the books to print. Under it, the value of each field
  for this publication.

Click the small arrow beside a publication (or double-click its line) to show or hide its
fields.

To change a value, click it, type the new text and press Enter. You can change:

* the **name** of a publication (bold, second column). Each name must be different. The name
  is also used in the PDF file name, so keep it short and simple;
* the **books** of a publication (bold, third column);
* the **value** of each field.

You cannot change field names here. They come from the variables table on the
**Peripherals** tab (see below).

### The books

Type the books as on the **Basic** tab, for example:

* `MRK` – one book;
* `RUT JON` – several books;
* `MAT-JHN` – a range of books;
* `JHN 1-5` – some chapters of one book.

You can also type the name of a module file (a file that lists which parts of the text to
print). If PTXprint cannot understand the books, the text turns red. Hold the mouse over it
to see what is wrong.

### The fields

Each publication always has the fields **maintitle** and **subtitle**. To add more, tick
**Pub** beside a variable in the **Variables and Values** table on the **Peripherals** tab.
The variable is then added to every publication. Untick **Pub** to remove it again (not
possible for **maintitle** and **subtitle**).

When you print a publication, PTXprint uses its values instead of the values on the
**Peripherals** tab, for that one PDF only. The values on the **Peripherals** tab are not
changed. The front matter (or the cover) must use the variables, for example
`\zvar|maintitle\*` on the title page.

If the book has a cover with a spine, there is also a **pagecount** field: the number of pages
of that publication. PTXprint uses it to work out the spine width for that publication's cover.

## 17.3 The buttons

* **Add** makes a new publication from the current settings.
* **Duplicate** copies the highlighted publication, called "Copy of ...". This is the quickest
  way to make a set: duplicate, then change the name, books and title.
* **Delete** removes the highlighted publication, after asking you.
* **Expand All** / **Collapse All** show or hide the fields of all publications.
* **Print Selected** prints every ticked publication.

The line at the bottom shows how many publications are ticked, and how many have books that
PTXprint cannot understand.

## 17.4 Printing the publications

When you click **Print Selected**, PTXprint:

1. saves the configuration (including the list of publications);
2. checks the books of each ticked publication. If some are wrong, it asks whether to print
   the others and skip these;
3. prints the publications in the background, several at the same time. **Maximum parallel
   processes** on the **Advanced** tab sets how many;
4. opens the folder with the PDFs when all are finished.

Each PDF is named after the project, the configuration and the publication name. The PDFs are
not shown in the PDF preview. Open them from the folder.

**Print Selected** is greyed out while the publications are printing.

Each configuration saves its own list of publications. When you switch configuration, the list
shows the publications of that configuration (empty if it has none).

## 17.5 Common tasks

### Make one PDF for each Gospel

1. On the **Peripherals** tab, tick **Local Front Matter** and check that the title page uses
   `\zvar|maintitle\*` (the standard front matter does).
2. On the **Publications** tab, click **Add**.
3. Click the bold name and type `Matthew`. Click the books and type `MAT`.
4. Open the publication, click the value of **maintitle** and type the title of Matthew in
   your language.
5. Click **Duplicate**. Change the copy's name to `Mark`, its books to `MRK`, and its title.
6. Do the same for Luke and John.
7. Tick all four and click **Print Selected**.

### Give each publication its own value for another variable

1. On the **Peripherals** tab, in the **Variables and Values** table, tick **Pub** beside the
   variable (for example **isbn**).
2. On the **Publications** tab, open each publication and type its value.

### Print only some of the publications

1. Untick all publications with the checkbox in the **Print** column heading.
2. Tick the ones you want.
3. Click **Print Selected**.

### Remove a publication

1. Click the publication (or one of its fields).
2. Click **Delete**, then confirm.

## 17.6 Common problems

**Print Selected is greyed out.**
No publication is ticked, or PTXprint is still printing the last set.

**Duplicate and Delete are greyed out.**
Click a publication in the list first.

**The books are shown in red.**
PTXprint cannot understand the list of books. Hold the mouse over the red text to see the
problem. Use the 3-letter book codes, separated by spaces, for example `GEN EXO`.

**"None of the selected publications can be printed".**
All ticked publications have no books or wrong books. Correct the books.

**All the PDFs have the same title.**
The front matter does not use the variable, or uses a different one. Check that the title
page contains `\zvar|maintitle\*` (see the **View+Edit** tab chapter), and that **Local Front
Matter** is ticked on the **Peripherals** tab.

**A variable is not in the publications.**
Tick **Pub** beside the variable on the **Peripherals** tab (the **Pub** column is only shown
in the **Full** view).

**"A publication called ... already exists".**
Each publication needs a different name.

**The Publications tab is missing.**
Change the view level to **Full**.

**My publications have gone.**
Check that you are using the right configuration. Each configuration keeps its own list.

## 17.7 Settings reference

### Publications

#### Add

Button · Full · `btn_pubAdd`

> Add a new publication, filled in from the current configuration: the books chosen on the Basic tab, and the title, subtitle and other publishable \zvars from the Peripherals tab.

The new publication is ticked for printing. Its books are those chosen on the **Basic** tab (or
the module, or the chapter range). Its name is the main title (or "New publication"); if that
name exists, PTXprint adds a number, for example "(2)".

#### Duplicate

Button · Full · `btn_pubDuplicate`

> Make a complete copy of the highlighted publication, named 'Copy of ...' (Click a publication first.)

Copies all books and values. Greyed out until you click a publication.

#### Delete

Button · Full · `btn_pubDel`

> Delete the highlighted publication (you will be asked to confirm). (Click a publication first.)

Does not delete PDFs that were already made. Greyed out until you click a publication.

#### Expand All

Button · Full · `btn_pubExpandAll`

> Show the details of every publication.

Useful for checking all titles before you print.

#### Collapse All

Button · Full · `btn_pubCollapseAll`

> Hide the details of every publication.

Shows only names and books. Useful when the list is long.

#### tv_publications

Table · Full · `tv_publications`

The bold line of each publication shows the **Print** checkbox, the name and the books; the
lines under it show its fields and values. Click a name, the books or a value to change it;
press Enter to keep the change. Books that PTXprint cannot understand are shown in red.

#### Print Selected

Button · Full · `btn_pubPrint`

> Save the configuration, then create a PDF for each ticked publication (in the background). The folder with the PDFs opens when they are finished.

Prints several publications at the same time. Publications with wrong books are skipped after
asking you. Greyed out when nothing is ticked or while printing.
