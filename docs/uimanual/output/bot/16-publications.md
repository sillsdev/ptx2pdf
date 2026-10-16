# Publications tab

## What this tab is for

Sometimes you want to make several similar books from one project with the same design. For
example: one PDF for each Gospel, or a New Testament and a separate book of Psalms, each with
its own title. The **Publications** tab lets you do this without making a new configuration
for each book.

A **publication** here means: this configuration, printed with

* its own list of books, and
* its own values for some of the variables of the front matter (for example the main title
  and the subtitle).

All other settings (page size, fonts, layout, front matter, cover and so on) come from the
current configuration. You make a list of publications, tick the ones you want, and click
**Print Selected**. PTXprint then makes one PDF for each ticked publication.

This tab is only shown in the **Default** and **Full** views.

## The list of publications

The list has three columns:

* **Print** – tick the publications that you want to print. The checkbox in the column
  heading ticks or unticks all publications at once.
* **Publication ID / Field** – on the first (bold) line of each publication, this is the name
  of the publication. Under it are the names of its fields (variables).
* **Books / Value** – on the bold line, the books to print. Under it, the value of each field
  for this publication.

Click the small arrow beside a publication (or double-click its line) to show or hide its
fields. **Expand All** and **Collapse All** do this for all publications.

To change a value, click it, type the new text and press Enter. You can change:

* the **name** of a publication (the bold text in the second column). Each name must be
  different. The name is also used in the name of the PDF file, so keep it short and simple;
* the **books** of a publication (the bold text in the third column);
* the **value** of each field.

You cannot change the names of the fields here. They come from the variables table on the
**Peripherals** tab (see below).

### The books

Type the books in the same way as on the **Basic** tab, for example:

* `MRK` – one book;
* `RUT JON` – several books;
* `MAT-JHN` – a range of books;
* `JHN 1-5` – some chapters of one book.

You can also type the name of a module file (a file that lists which parts of the text to
print). If PTXprint cannot understand the books, the text turns red. Hold the mouse over it
to see what is wrong.

### The fields

Each publication always has the fields **maintitle** and **subtitle**. To add more fields,
go to the **Peripherals** tab and tick **Pub** beside a variable in the **Variables and
Values** table. The variable is then added to every publication. Untick **Pub** to remove it
again (except for **maintitle** and **subtitle**).

When you print a publication, PTXprint uses its values instead of the values on the
**Peripherals** tab. This only changes that one PDF. The values on the **Peripherals** tab are
not changed. For this to work, the front matter (or the cover) must use the variables, for
example `\zvar|maintitle\*` on the title page.

If the book has a cover with a spine, there is also a **pagecount** field. It holds the number
of pages of that publication. PTXprint uses it to work out the width of the spine for that
publication's cover.

## The buttons

* **Add** makes a new publication from the current settings: the books chosen on the
  **Basic** tab, and the current values of the variables. Its name is the main title (or
  "New publication"). It is ticked for printing.
* **Duplicate** makes a copy of the highlighted publication, called "Copy of ...". This is
  the quickest way to make a set of similar publications: duplicate, then change the name,
  books and title.
* **Delete** removes the highlighted publication, after asking you.
* **Expand All** / **Collapse All** show or hide the fields of all publications.
* **Print Selected** prints every ticked publication.

The line at the bottom shows how many publications are ticked, and how many have books that
PTXprint cannot understand.

## Printing the publications

When you click **Print Selected**, PTXprint:

1. saves the configuration (including the list of publications);
2. checks the books of each ticked publication. If some are wrong, it asks if it should
   print the others and skip these;
3. prints the publications in the background, several at the same time. The number at the
   same time is set by **Maximum parallel processes** on the **Advanced** tab;
4. opens the folder with the PDFs when all are finished.

Each PDF is named after the project, the configuration and the publication name. The PDFs are
not shown in the PDF preview. Open them from the folder.

While the publications are printing, **Print Selected** is greyed out.

The list of publications is saved with the configuration.

## Common tasks

### Make one PDF for each Gospel

1. On the **Peripherals** tab, tick **Local Front Matter** and make sure the title page uses
   `\zvar|maintitle\*` (the standard front matter does).
2. On the **Publications** tab, click **Add**.
3. Click the bold name and type `Matthew`. Click the books and type `MAT`.
4. Open the publication and click the value of **maintitle**. Type the title of Matthew in
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

## Common problems

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
The front matter does not use the variable, or it uses a different variable. Check that the
title page contains `\zvar|maintitle\*` (see the **View+Edit** tab chapter), and that
**Local Front Matter** is ticked on the **Peripherals** tab.

**A variable is not in the publications.**
Tick **Pub** beside the variable on the **Peripherals** tab.

**"A publication called ... already exists".**
Each publication needs a different name. Choose another name.

**The Publications tab is missing.**
You are using the **Basic** or **Minimal** view. Change to **Default** or **Full**.

## Settings reference: Publications tab

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Publications tab

#### Add

- **Where:** Publications tab
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Add a new publication, filled in from the current configuration: the books chosen on the Basic tab, and the title, subtitle and other publishable \zvars from the Peripherals tab.

**Explanation:**

Adds a new publication, ticked for printing. Its books are the books currently chosen on the
**Basic** tab (or the module, or the chapter range), and its fields get the current values of
the variables from the **Peripherals** tab. If a publication with that name already exists,
PTXprint adds a number, for example "(2)".

*(Internal ID: `btn_pubAdd`)*

#### Duplicate

- **Where:** Publications tab
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Make a complete copy of the highlighted publication, named 'Copy of ...' (Click a publication first.)

**Explanation:**

Copies the highlighted publication with all its books and values. Use it to make a series of
similar publications quickly. Greyed out until you click a publication in the list.

*(Internal ID: `btn_pubDuplicate`)*

#### Delete

- **Where:** Publications tab
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Delete the highlighted publication (you will be asked to confirm). (Click a publication first.)

**Explanation:**

Removes the highlighted publication from the list after you confirm. It does not delete PDFs
that were already made. Greyed out until you click a publication.

*(Internal ID: `btn_pubDel`)*

#### Expand All

- **Where:** Publications tab
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Show the details of every publication.

**Explanation:**

Opens all publications so that you can see every field and value. Useful for checking all
titles before you print.

*(Internal ID: `btn_pubExpandAll`)*

#### Collapse All

- **Where:** Publications tab
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Hide the details of every publication.

**Explanation:**

Closes all publications so that you only see their names and books. Useful when the list is
long.

*(Internal ID: `btn_pubCollapseAll`)*

#### tv_publications

- **Where:** Publications tab
- **Type:** Table
- **View level:** Default and Full views

**Explanation:**

The list of publications. The bold line of each publication shows the **Print** checkbox, the
name and the books. The lines under it show the fields (variables) and their values for that
publication. Click a name, the books or a value to change it; press Enter to keep the change.
Books that PTXprint cannot understand are shown in red.

*(Internal ID: `tv_publications`)*

#### Print Selected

- **Where:** Publications tab
- **Type:** Button
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Save the configuration, then create a PDF for each ticked publication (in the background). The folder with the PDFs opens when they are finished.

**Explanation:**

Saves the configuration, then prints each ticked publication in the background (several at
the same time) and opens the folder with the new PDFs when all are done. Publications with
wrong books are skipped after asking you. Greyed out when nothing is ticked or while printing.

*(Internal ID: `btn_pubPrint`)*
