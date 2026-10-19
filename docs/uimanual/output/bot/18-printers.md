# Printers tab

## What this tab is for

The **Printers** tab helps you plan the printing of your book. It gives a rough **price estimate** from several print companies, shows how thick the book will be, and lets you **compare prices** between printers in a graph. For one printer (Pretore), you can also get an exact quotation and start an order directly from PTXprint.

Come here when the book is nearly finished and you want to know: "About how much will it cost to print 500 copies?", "Which printer is cheapest for this size and number of pages?", or "How thick will the spine be?"

The **Printers** tab is only shown in the **Full** view.

**Important:** most prices on this tab are *estimates*. PTXprint calculates them from price information collected earlier from each printer. Real prices change, and shipping and taxes are not included. Always get a real quotation from the printer before you make a decision.

The tab has three parts:

1. **Book & Job Specification** at the top – the facts about your book and print job.
2. The **printer list** – one row for each printer, with an estimated price per copy.
3. The **printer details** panel – the options and price details for the printer you click in the list.

## Book & Job Specification

These settings describe the job. All printers use them.

* **Pages** – the number of pages. PTXprint fills this in from the most recent PDF you made. You can change it, for example to add pages for front matter that is printed separately.
* **Copies** – how many books you want to print.
* **Interior** – **Black & white** or **Full color** for the inside pages.
* **Binding** – **Paperback (soft cover)**, **Hardcover** or **Saddle-stitched (stapled)**. Each printer uses its nearest matching binding. If a printer does not offer your choice, it says so in red in its details panel.
* **Currency** – the currency for all prices. PTXprint gets exchange rates from the internet, so prices from printers in other countries can be shown in your currency.
* **Trim size** – the finished page size (in mm). This comes from the page size on the **Layout** tab. You cannot change it here.
* **Thickness** – the estimated thickness of the book (spine), for the printer selected in the list. It depends on the number of pages, the paper that printer uses, and the binding. This is useful when you design a cover, because the spine width must match the book thickness.

Every time you change one of these settings, all the prices are calculated again.

## The printer list

Each row shows:

* a **Compare** tick box;
* the **Printer** name, its country and web address;
* **Est. per copy** – the estimated price for one copy, at the number of **Copies** you entered.

Under the price, a small word tells you where the price comes from:

* **estimate** – PTXprint calculated it from its own price model for that printer.
* **live quote** – the price came from the printer's own system over the internet (Pretore).
* **quote in panel** – this printer gives live quotes only. Open its panel and ask for a quotation.
* **no model yet** – PTXprint does not have price information for this printer yet. Use its web link to ask for a price.

When two or more printers have a price, the cheapest one is shown in **green**.

Click a printer's row to see its details panel below or beside the list.

**Per Copy** and **Total Job** show the price for the selected printer: for one copy, and for the whole job. The total can be for slightly more copies than you asked for, if that printer rounds the number of copies (see below).

### Compare Prices...

Click **Compare Prices...** to open the **Multi-Quote Comparison** window. It shows a graph of the price for each printer that is ticked in the **Compare** column, at several quantities (50, 100, 250, 500 and 1000 copies, plus your own number of **Copies**).

In this window you can:

* choose **Price per Copy** or **Total Price**;
* set a **Max Budget**, so that totals above your budget are left out (tick **No limit** to show everything);
* tick or untick printers under **Show Printers**;
* tick **Show smooth curves** to draw curves instead of straight lines between points;
* point at a dot on the graph to see the exact value.

Printers that have no price model cannot be ticked for comparison. For Pretore, PTXprint asks Pretore's server for prices when you click **Compare Prices...**; this only works if you have set up a Pretore account (see below).

## The printer details panels

Each printer has its own panel with extra options. These options only affect that printer's estimate.

### Pothi (India)

* **Paper type** – plain white, plain natural shade, or coated paper. For black-and-white books the price does not change with the paper. Coated paper costs more only with a full-colour interior.
* The panel shows how the price is made up: the **Nearest size** in Pothi's list of book sizes, the base price, the binding adjustment, the colour cost, and the **1-copy price**.
* A row of prices shows the discount for larger orders (1, 50+, 100+, 250+, 500+, 1000+ copies). The price for your number of copies is in bold.
* Red warnings appear if the job does not fit Pothi's rules. For example: saddle-stitching only up to 64 pages; soft cover only from 50 to 500 pages; for 1500 or more copies, contact Pothi directly.

### Print Gallery (India)

* **Paper type** – several paper weights (gsm = grams per square metre; a higher number is thicker paper).
* **Lamination** – a thin plastic layer on the cover to protect it.
* The panel shows the cost of covers, interior, lamination and binding, and how the pages are arranged on Print Gallery's large sheets (**Imposition**).
* Print Gallery prints on sheets that hold 4 pages, so the page count is rounded up to a multiple of 4. A5 books are printed in pairs, so an odd number of copies is rounded up by one. A red note tells you when this happens.
* Stapled binding is not used for books over 100 pages; perfect (glued) binding is priced instead.

### Pretore (Netherlands)

Pretore gives **live quotations** from its own system, and you can start an order from PTXprint. You need a Pretore account and an internet connection.

* **Paper Type**, **Cover Lamination**, **Shrink Wrap** and **Ribbons** (marker ribbons, for hardback only) – Pretore's own options.
* **Book Identifier** and **Description** – PTXprint fills these in from the project and the books you are printing. Both must be filled in before you can get a quotation or create an order.
* **Account...** – choose your Pretore account, or import an account key file that you downloaded from the Pretore website. The window has a link to register and download the key.
* **Get Precise Quotation** – asks Pretore for the real price of this job.
* **Create Order** – packs the finished PDF files into a ZIP file and creates an order at Pretore. The order reference, the ZIP file name and the status (**awaiting payment**) are shown. Use the copy button to copy the full path of the ZIP file.
* **Complete Order & Payment via website** – opens the Pretore website, where you upload the ZIP file and pay.

Pretore accepts books of 120 to 2000 pages. It does not offer saddle-stitching (it quotes paperback instead), and its price does not change between black-and-white and colour interiors.

### Snowfall Press (United States)

PTXprint does not yet have price information for this printer, so it is left out of comparisons. Use the link in the panel to visit the website and ask for a quotation.

## Common tasks

### Get a quick price estimate for my book

1. Make the PDF of the whole book first (click **Print**), so that the page count is correct.
2. Change to the **Full** view if the **Printers** tab is not visible.
3. Open the **Printers** tab. Check **Pages** and **Trim size**.
4. Enter the number of **Copies**, and choose **Interior** and **Binding**.
5. Choose your **Currency**.
6. Read the **Est. per copy** column. The cheapest printer is shown in green.

### Compare prices from several printers in a graph

1. Fill in the **Book & Job Specification** as above.
2. In the printer list, tick **Compare** for each printer you want in the graph.
3. Click **Compare Prices...**.
4. Choose **Price per Copy** or **Total Price**. Point at the dots to read exact prices.

### Find out how thick the book will be (for the cover spine)

1. Fill in **Pages** and **Binding**.
2. Click a printer in the list, then choose its paper in its details panel.
3. Read **Thickness**. Different printers and papers give different thicknesses. Ask the printer for the exact spine width before you finish the cover.

### Order from Pretore

1. Make the final PDF with the format Pretore asks for (see the **Finishing** tab).
2. On the **Printers** tab, click **Pretore** in the list.
3. Click **Account...** and choose or import your account key.
4. Choose the paper and other options. Check **Book Identifier** and **Description**.
5. Click **Get Precise Quotation** and check the price.
6. Click **Create Order**. PTXprint makes the ZIP file and shows the order reference.
7. Click **Complete Order & Payment via website** to upload the ZIP file and pay.

## Common problems

**I cannot see the Printers tab.**
The tab is only shown in the **Full** view. Change the view level.

**The number of pages is 99, or is wrong.**
PTXprint reads the page count from the last PDF you made for the current books. If you have not made a PDF yet, it shows 99. Click **Print** first, then come back to the tab. You can also type the correct number into **Pages**.

**A printer shows "—" and no price.**
Either this printer has no price model yet (**no model yet**), or it gives live quotes only (**quote in panel**). For Pretore, set up an account and click **Get Precise Quotation**. Also check the red warnings in the printer's panel: the job may be outside that printer's limits.

**Pretore says "No account configured".**
Click **Account...** in the Pretore panel and import the account key file from the Pretore website.

**"Get Precise Quotation" and "Create Order" are greyed out.**
**Book Identifier** and **Description** must both be filled in.

**"Create Order" says I must print the job first.**
PTXprint needs the finished PDF files to put in the ZIP file. Click **Print**, then try again.

**The total is for more copies than I asked for.**
Some printers print in pairs or round the number of copies. A red note in the printer's panel explains this.

**I cannot tick a printer in the Compare column.**
That printer has no price model, so it cannot be compared.

**Prices are shown in the wrong currency, or not converted.**
PTXprint downloads exchange rates from the internet. Without an internet connection (or when **Disable ALL Internet Use** is ticked on the **Advanced** tab), prices from another country may be shown in that printer's own currency, or left out of the comparison graph.

## Settings reference: Printers tab

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Printers tab › Book & Job Specification

#### Thickness

- **Where:** Printers tab › Book & Job Specification
- **Type:** Label
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Spine/book thickness for the currently selected printer, based on its paper stock and binding.

#### Trim size

- **Where:** Printers tab › Book & Job Specification
- **Type:** Label
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Finished page size of the book, from the Layout page settings.

#### Pages

- **Where:** Printers tab › Book & Job Specification
- **Type:** Number box
- **View level:** Full view only
- **Values:** from 1 to 9999, default 200

**Tooltip (the text shown when you hover the mouse over it):**

> Number of pages in the book. Filled in automatically from the most recently created PDF (99 if no PDF has been made yet), but can be adjusted manually.

**Explanation:**

Filled in from the most recent PDF of the selected books. If no PDF has been made yet, it shows 99, so make the PDF first. Change it by hand if the printed book will have more pages than the PDF (for example, extra blank pages or separately printed front matter). Printers usually charge per page, so this has a big effect on the price.

*(Internal ID: `s_prn_pages`)*

#### Copies

- **Where:** Printers tab › Book & Job Specification
- **Type:** Number box
- **View level:** Full view only
- **Values:** from 1 to 99999, default 50

**Tooltip (the text shown when you hover the mouse over it):**

> How many copies of the book to be printed.

**Explanation:**

The number of books to print. All prices, warnings and the total are based on this number. Printing more copies usually lowers the price per copy; use **Compare Prices...** to see this at 50, 100, 250, 500 and 1000 copies.

*(Internal ID: `s_prn_copies`)*

#### Interior

- **Where:** Printers tab › Book & Job Specification
- **Type:** Drop-down list
- **View level:** Full view only
- **Choices:** Black & white; Full color

**Tooltip (the text shown when you hover the mouse over it):**

> Whether the inside pages are printed in black & white or full color.

**Explanation:**

**Full color** is much more expensive at most printers, even if only a few pages have colour. Choose **Black & white** unless the inside of the book really needs colour. Some printers do not change the price for colour (Pretore), and some have no colour price data for every size yet (a red note tells you).

*(Internal ID: `fcb_prn_interior`)*

#### Binding

- **Where:** Printers tab › Book & Job Specification
- **Type:** Drop-down list
- **View level:** Full view only
- **Choices:** Paperback (soft cover); Hardcover; Saddle-stitched (stapled)

**Tooltip (the text shown when you hover the mouse over it):**

> Preferred binding style. Each printer maps this onto the nearest option it offers.

**Explanation:**

Paperback is the usual choice. Hardcover costs more but lasts longer. Saddle-stitched (stapled) is only for thin books; printers limit the number of pages (for example Pothi: up to 64 pages). If a printer does not offer your choice, its panel says which binding it priced instead. The binding also changes the **Thickness**.

*(Internal ID: `fcb_prn_binding`)*

#### Currency

- **Where:** Printers tab › Book & Job Specification
- **Type:** Drop-down list
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Currency used to display all quotations and estimates. Prices in other currencies are converted using exchange rates downloaded from the internet (a guide only).

**Explanation:**

Choose the currency you want to see all prices in. PTXprint converts each printer's prices from its own currency, using exchange rates downloaded from the internet. The conversion is only a guide; the printer will charge in its own currency.

*(Internal ID: `fcb_prn_currency`)*

### Printers tab

#### Compare Prices...

- **Where:** Printers tab
- **Type:** Button
- **View level:** Full view only

**Tooltip (the text shown when you hover the mouse over it):**

> Show a graph comparing prices (per copy or total) at several quantities across all the printers ticked in the Compare column above.

**Explanation:**

Opens the **Multi-Quote Comparison** graph for every printer ticked in the **Compare** column. For Pretore, PTXprint first asks Pretore's server for prices (this needs an account and an internet connection). If no ticked printer has a price, no graph appears.

*(Internal ID: `btn_prn_compare`)*
