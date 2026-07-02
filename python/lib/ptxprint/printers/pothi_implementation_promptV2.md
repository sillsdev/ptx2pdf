# Implementation Prompt: Pothi.com Book Cost Calculator

## Project Context

**PTXprint** is a GTK3 desktop application written in Python, using a single `.glade` XML file
(`ptxprint.glade`) for the UI and a `GtkViewModel` view class (`gtkview.py`) that dispatches
widget get/set through `getWidgetVal`/`setWidgetVal` helper functions in `gtkutils.py`.

Those helpers dispatch based on widget **name prefix** (e.g. `s_` for spinbuttons, `l_` for
labels, `fcb_` for fixed comboboxes). **The Pothi widgets do not follow this naming convention**
— they use plain names like `pagesSpin`, `sizeCombo`, `totalBreakAmt`, etc. For this reason,
all widget access in `pothi.py` must go **directly** through `self.view.builder.get_object(name)`
rather than through `self.view.get()` / `self.view.set()`.

---

## File Structure

The printers subsystem lives at:

```
python/lib/ptxprint/printers/
    __init__.py     # registry of all printers
    pothi.py        # the file to create
    pretore.py      # existing printer (for reference only)
```

### `__init__.py` — printer registry

```python
import importlib

printerlist = {
    'pretore':       ('Pretore',      'l_pr_pretore'),
    'print_gallery': ('PrintGallery', 'l_pr_print_gallery'),
    'pothi':         ('Pothi',        'l_pr_pothi'),
}

def init_printers(view):
    res = {}
    for k, v in printerlist.items():
        module = importlib.import_module("ptxprint.printers." + k)
        c = getattr(module, v[0])
        res[k] = c(view)
    return res

def printer_from_label(lid):
    for k, v in printerlist.items():
        if v[1] == lid:
            return k
    return None
```

### How the tab system calls into printers

In `gtkview.py`:

```python
def onChangedPrinterTab(self, nbk_printers, scrollObject, pgnum=-1):
    ppage = nbk_printers.get_nth_page(pgnum)
    lw = nbk_printers.get_tab_label(ppage)
    lid = self.getWidgetId(lw)
    k = printer_from_label(lid)
    if k:
        self.printers[k].prepare()

def onChangedMainTab(self, nbk_Main, scrollObject, pgnum=-1):
    pgid = Gtk.Buildable.get_name(nbk_Main.get_nth_page(pgnum))
    ...
    elif pgid == "tb_Printers":
        nbkw = self.builder.get_object("nbk_printers")
        self.onChangedPrinterTab(nbkw, None, nbkw.get_current_page())
```

`prepare()` is called every time the user navigates to the printer tab. `setup()` must only
run **once** (guarded by `_setupDone`), because `append_text()` on a `GtkComboBoxText`
accumulates — calling it twice doubles the entries.

---

## `pothi.py` — Full Implementation

```python
from gi.repository import Gtk

# ---------------------------------------------------------------------------
# Pricing constants
# Reverse-engineered from 21 verified Pothi.com data points — zero error.
# Formula: price = fixed + rate * pages + bindingAdj + colorCost + coatedCost
# ---------------------------------------------------------------------------

# SIZE_PARAMS keys match sizeCombo index positions (see setup()).
# 'verified': True means the formula has been validated against real quotes.
# For unverified sizes, the calculator shows a warning and suppresses output.
SIZE_PARAMS = [
    # index 0 — "5 inch x 7 inch"
    {"fixed": None, "rate": None, "verified": False},
    # index 1 — "5 inch x 8 inch"
    {"fixed": None, "rate": None, "verified": False},
    # index 2 — "A5"
    {"fixed": 67.0, "rate": 0.85, "verified": True},
    # index 3 — "5.5 inch x 8.5 inch"
    {"fixed": 72.0, "rate": 0.80, "verified": True},
    # index 4 — "6 inch x 9 inch"
    {"fixed": None, "rate": None, "verified": False},
    # index 5 — "7 inch x 9 inch"
    {"fixed": None, "rate": None, "verified": False},
    # index 6 — "8 inch x 11 inch"
    {"fixed": None, "rate": None, "verified": False},
    # index 7 — "A4"
    {"fixed": 83.0, "rate": 1.30, "verified": True},
]

# Binding adjustment added to the base price (₹, flat per copy)
# Verified consistent across A5, 5.5×8.5, and A4.
BINDING_ADJ = {
    "soft":   0,    # Soft Cover — no adjustment
    "saddle": -25,  # Saddle Stitched — ₹25 cheaper than soft cover
    "hard":   +45,  # Hard Cover — ₹45 more than soft cover
}

# Binding keys in sizeCombo order (index matches bindingCombo)
BINDING_KEYS = ["soft", "saddle", "hard"]

# Full color interior premium: fixed charge + per-page rate
# Derived from two data points (100p A5 and 1200p 5.5×8.5) — zero error.
COLOR_FIXED = 1260.0 / 11   # ≈ ₹114.55
COLOR_RATE  = 463.0  / 220  # ≈ ₹2.105/page

# Coated paper surcharge — applies ONLY when interior is Full Color
COATED_RATE = 1.15  # ₹/page

# Bulk discount tiers: (minimum quantity, discount percentage)
DISCOUNT_TIERS = [
    (1,    0),
    (50,   10),
    (100,  20),
    (250,  25),
    (500,  40),
    (1000, 50),
]

# Page range constraints by binding type
SADDLE_MAX_PAGES = 64
SOFT_MIN_PAGES   = 50
SOFT_MAX_PAGES   = 500


class Pothi:
    def __init__(self, view):
        self.view = view
        self._setupDone = False

    def _widget(self, wname):
        return self.view.builder.get_object(wname)

    def setup(self):
        """Initialise default values and connect signals. Runs once only."""
        if self._setupDone:
            return
        self._setupDone = True
        try:
            sizeCombo = self._widget("p_sizeCombo")
            for label in [
                "5 inch x 7 inch",
                "5 inch x 8 inch",
                "A5",
                "5.5 inch x 8.5 inch",
                "6 inch x 9 inch",
                "7 inch x 9 inch",
                "8 inch x 11 inch",
                "A4",
            ]:
                sizeCombo.append_text(label)
            sizeCombo.set_active(2)  # Default: A5

            bindingCombo = self._widget("p_bindingCombo")
            for label in ["Soft Cover", "Saddle Stitched Binding", "Hard Cover"]:
                bindingCombo.append_text(label)
            bindingCombo.set_active(0)  # Default: Soft Cover

            paperCombo = self._widget("p_paperCombo")
            for label in [
                "Plain White (70-80 GSM)",
                "Plain Natural Shade (70-80 GSM)",
                "Coated (90-120 GSM)",
            ]:
                paperCombo.append_text(label)
            paperCombo.set_active(0)  # Default: Plain White

            colorCombo = self._widget("p_colorCombo")
            for label in [
                "B&W interior (colored cover)",
                "Full Color (Interior & Cover)",
            ]:
                colorCombo.append_text(label)
            colorCombo.set_active(0)  # Default: B&W

            pagesSpin = self._widget("p_pagesSpin")
            pagesSpin.set_value(200)

            qtySpin = self._widget("p_qtySpin")
            qtySpin.set_value(1)

            # Connect signals — all trigger the same recalculation handler
            pagesSpin.connect("value-changed", self.onInputChanged)
            qtySpin.connect("value-changed", self.onInputChanged)
            sizeCombo.connect("changed", self.onInputChanged)
            bindingCombo.connect("changed", self.onInputChanged)
            paperCombo.connect("changed", self.onInputChanged)
            colorCombo.connect("changed", self.onInputChanged)

            self.onInputChanged()

        except Exception as e:
            print(f"ERROR in Pothi setup: {e}")
            import traceback
            traceback.print_exc()

    def prepare(self):
        """Called every time the Pothi tab is made active."""
        self.setup()

    def onInputChanged(self, widget=None):
        """Recalculate and update all output labels whenever any input changes."""
        try:
            pages       = int(self._widget("p_pagesSpin").get_value())
            qty         = int(self._widget("p_qtySpin").get_value())
            sizeIdx     = self._widget("p_sizeCombo").get_active()
            bindingIdx  = self._widget("p_bindingCombo").get_active()
            paperIdx    = self._widget("p_paperCombo").get_active()
            colorIdx    = self._widget("p_colorCombo").get_active()

            params      = SIZE_PARAMS[sizeIdx]
            bindingKey  = BINDING_KEYS[bindingIdx]
            isCoated    = (paperIdx == 2)
            isFullColor = (colorIdx == 1)

            # --- Warnings ---
            warnings = []
            if not params["verified"]:
                warnings.append(
                    "Pricing for this page size has not yet been verified. "
                    "Add data to SIZE_PARAMS to enable the calculator."
                )
            if bindingKey == "saddle" and pages > SADDLE_MAX_PAGES:
                warnings.append(
                    f"Saddle Stitched Binding is only available up to {SADDLE_MAX_PAGES} pages."
                )
            if bindingKey == "soft" and pages < SOFT_MIN_PAGES:
                warnings.append(
                    f"Soft Cover requires a minimum of {SOFT_MIN_PAGES} pages."
                )
            if bindingKey == "soft" and pages > SOFT_MAX_PAGES:
                warnings.append(
                    f"Soft Cover maximum is {SOFT_MAX_PAGES} pages."
                )
            if qty >= 1500:
                warnings.append(
                    "For 1500+ copies, contact Pothi.com directly for a custom quote."
                )

            self._widget("p_warnLabel").set_text("  ".join(warnings))

            # Suppress output if size is unverified
            if not params["verified"]:
                for wid in [
                    "p_price1Amt", "p_priceQAmt", "p_priceTotalAmt",
                    "p_baseBreakAmt", "p_bindBreakAmt",
                    "p_colorBreakAmt", "p_coatedBreakAmt", "p_totalBreakAmt",
                    "p_discountBreakAmt",
                ]:
                    self._widget(wid).set_text("—")
                for i in range(6):
                    self._widget(f"p_discPrice{i}").set_text("—")
                return

            # --- Calculations ---
            base       = params["fixed"] + params["rate"] * pages
            bindAdj    = BINDING_ADJ[bindingKey]
            colorCost  = (COLOR_FIXED + COLOR_RATE * pages) if isFullColor else 0.0
            coatedCost = (COATED_RATE * pages) if (isCoated and isFullColor) else 0.0
            price1     = base + bindAdj + colorCost + coatedCost

            discPct = 0
            for minQty, pct in DISCOUNT_TIERS:
                if qty >= minQty:
                    discPct = pct
            priceAtQty = price1 * (1 - discPct / 100)
            total      = priceAtQty * qty

            # --- Summary labels ---
            self._widget("p_price1Amt").set_text(fmtRupees(price1))
            discStr = f" ({discPct}% off)" if discPct else ""
            self._widget("p_priceQAmt").set_text(fmtRupees(priceAtQty) + discStr)
            self._widget("p_priceTotalAmt").set_markup(
                f"<b>{fmtRupees(total)}</b>"
            )

            # --- Breakdown labels ---
            sizeName = self._widget("p_sizeCombo").get_active_text() or ""
            self._widget("p_baseBreakAmt").set_text(
                f"{fmtRupees(params['fixed'])} + "
                f"₹{params['rate']:.2f}/pg × {pages} = {fmtRupees(base)}"
            )
            if bindAdj != 0:
                sign = "+" if bindAdj > 0 else ""
                self._widget("p_bindBreakAmt").set_text(
                    f"{sign}{fmtRupees(bindAdj)}"
                )
            else:
                self._widget("p_bindBreakAmt").set_text("—")

            if isFullColor:
                self._widget("p_colorBreakAmt").set_text(
                    f"{fmtRupees(COLOR_FIXED)} + "
                    f"₹{COLOR_RATE:.3f}/pg × {pages} = {fmtRupees(colorCost)}"
                )
            else:
                self._widget("p_colorBreakAmt").set_text("—")

            if isCoated and isFullColor:
                self._widget("p_coatedBreakAmt").set_text(
                    f"₹{COATED_RATE:.2f}/pg × {pages} = {fmtRupees(coatedCost)}"
                )
            else:
                self._widget("p_coatedBreakAmt").set_text("—")

            self._widget("p_totalBreakAmt").set_markup(
                f"<b>{fmtRupees(price1)}</b>"
            )

            # --- Discount tier grid ---
            for i, (minQty, pct) in enumerate(DISCOUNT_TIERS):
                p = price1 * (1 - pct / 100)
                self._widget(f"p_discPrice{i}").set_text(fmtRupees(p))
                # Bold the active tier
                if pct == discPct:
                    self._widget(f"p_discPrice{i}").set_markup(
                        f"<b>{fmtRupees(p)}</b>"
                    )

        except Exception as e:
            print(f"ERROR in Pothi onInputChanged: {e}")
            import traceback
            traceback.print_exc()


def fmtRupees(amount):
    """Format a float as Indian-locale rupees: ₹X,XX,XXX.XX"""
    paise   = round(amount * 100)
    decPart = paise % 100
    intPart = paise // 100
    intStr  = str(intPart)
    if intPart >= 1000:
        parts  = [intStr[-3:]]
        intStr = intStr[:-3]
        while intStr:
            parts.append(intStr[-2:])
            intStr = intStr[:-2]
        intStr = ",".join(reversed(parts))
    return f"₹{intStr}.{decPart:02d}"
```

---

## Glade Fragment for the Pothi Tab

The Pothi panel is one page inside the `GtkNotebook` with id `nbk_printers`. The notebook
must have this signal wired:

```xml
<signal name="switch-page" handler="onChangedPrinterTab" swapped="no"/>
```

The outer `nbk_Main` notebook also needs `onChangedMainTab` connected to `switch-page`
(already present in the app). When the main tab `tb_Printers` is selected,
`onChangedMainTab` delegates to `onChangedPrinterTab`.

### Tab label widget

The tab label widget ID must be `l_pr_pothi` — this is what `printer_from_label()` in
`__init__.py` matches against to dispatch `prepare()` calls.

### Adjustments needed in the glade file

The Pothi tab page is a `GtkBox` (orientation vertical, spacing 6) containing these
children **in order**:

1. **Bold heading label** — `<b>Pothi.com Book Cost Calculator</b>`
2. **Input grid** (`GtkGrid`, column-spacing 12, row-spacing 8)
3. **Separator**
4. **Cost Breakdown grid** (`GtkGrid`, column-spacing 12, row-spacing 4)
5. **Discount tier grid** (`GtkGrid`, column-spacing 8, row-spacing 4)
6. **Link button** — "Visit Pothi.com" (`https://pothi.com`)

---

### Input Grid Layout

All widget IDs are prefixed `p_` to avoid collision with other printer widgets.

| Row | Col 0 label | Col 1 widget | Widget ID | Notes |
|-----|-------------|--------------|-----------|-------|
| 0 | Page size: | GtkComboBoxText | `p_sizeCombo` | Populated in Python |
| 1 | Binding: | GtkComboBoxText | `p_bindingCombo` | Populated in Python |
| 2 | Paper type: | GtkComboBoxText | `p_paperCombo` | Populated in Python |
| 3 | Interior color: | GtkComboBoxText | `p_colorCombo` | Populated in Python |
| 4 | Pages: | GtkSpinButton | `p_pagesSpin` | Uses adjustment `p_adj_pages` |
| 5 | Quantity: | GtkSpinButton | `p_qtySpin` | Uses adjustment `p_adj_qty` |
| 6 | (colspan 2) | GtkLabel | `p_warnLabel` | Warning text; empty by default |

All comboboxes: `visible=True`, `can-focus=False`, `active=0`. **No** `has-entry=True` —
these must be non-editable dropdowns.

Spin buttons: `can-focus=True`, `climb-rate=1`, `digits=0`, `numeric=True`.

Adjustments:
- `p_adj_pages`: value=200, lower=10, upper=9999, step-increment=2
- `p_adj_qty`: value=1, lower=1, upper=9999, step-increment=1

`p_warnLabel`: `visible=True`, `wrap=True`, `halign=start`, empty initial text,
styled amber/orange via a CSS provider applied in Python.

#### Combobox tooltips

```
p_sizeCombo:
  "Page size of the printed book.
   Verified sizes (formula validated against real Pothi.com quotes):
     A5, 5.5×8.5 inch, A4
   Unverified sizes (pricing data not yet collected):
     5×7 inch, 5×8 inch, 6×9 inch, 7×9 inch, 8×11 inch
   The calculator will show a warning and suppress output for unverified sizes."

p_bindingCombo:
  "Binding type affects the per-copy price:
     Soft Cover            — standard flat-spine paperback (50–500 pages)
     Saddle Stitched Binding — stapled through the spine (10–64 pages max)
     Hard Cover            — premium hardbound (+₹45 over soft cover)
   Saddle stitching is ₹25 cheaper than soft cover at the same page count."

p_paperCombo:
  "Paper stock for the interior pages.
     Plain White (70-80 GSM)        — standard uncoated paper
     Plain Natural Shade (70-80 GSM) — cream-toned uncoated; prices identically to Plain White
     Coated (90-120 GSM)            — glossy/art paper; adds ₹1.15/page surcharge
                                       (only when Full Color is selected)"

p_colorCombo:
  "Interior printing method:
     B&W interior (colored cover)  — black and white interior, full-color cover
     Full Color (Interior & Cover) — full color throughout
   Full color adds a fixed setup charge (≈₹114.55) plus ≈₹2.10 per page.
   Coated paper surcharge (₹1.15/page) only applies with Full Color."

p_pagesSpin:
  "Total number of pages in the book (both sides of each leaf count as 2 pages).
   Pothi.com requires even page counts. Constraints by binding:
     Soft Cover:             50–500 pages
     Saddle Stitched:        10–64 pages
     Hard Cover:             up to ~500 pages (verify for very large books)"

p_qtySpin:
  "Number of copies to order. Bulk discounts are applied automatically:
     1 copy:     full price
     50+ copies: 10% off
     100+ copies: 20% off
     250+ copies: 25% off
     500+ copies: 40% off
     1000+ copies: 50% off
   For 1500+ copies, contact Pothi.com directly for a custom quote."
```

---

### Cost Breakdown Grid Layout

Two-column table. Column 0 = static label (`halign=start`), column 1 = dynamic value
label (`halign=end`). No `hexpand` on value labels — keeps the grid compact.

| Row | Col 0 (static label, glade) | Col 1 widget ID | Notes |
|-----|-----------------------------|-----------------|-------|
| 0 | `<b>Cost Breakdown (1 copy):</b>` (colspan 2) | — | Heading, `use-markup=True` |
| 1 | Base (fixed + per-page): | `p_baseBreakAmt` | e.g. `₹67.00 + ₹0.85/pg × 200 = ₹237.00` |
| 2 | Binding adjustment: | `p_bindBreakAmt` | e.g. `+₹45.00` or `—` |
| 3 | Full color premium: | `p_colorBreakAmt` | e.g. `₹114.55 + ₹2.10/pg × 200 = ₹534.55` or `—` |
| 4 | Coated paper surcharge: | `p_coatedBreakAmt` | e.g. `₹1.15/pg × 200 = ₹230.00` or `—` |
| 5 | `<b>1-copy price:</b>` | `p_totalBreakAmt` | `use-markup=True`; value set with `set_markup("<b>…</b>")` |
| 6 | Price per copy (your qty): | `p_priceQAmt` | e.g. `₹189.60 (20% off)` |
| 7 | `<b>Total for quantity:</b>` | `p_priceTotalAmt` | `use-markup=True`; value set with `set_markup("<b>…</b>")` |

All value labels: `visible=True`, `can-focus=False`, `selectable=True`, initial text `—`.

---

### Discount Tier Grid Layout

A `GtkGrid` (6 columns × 3 rows) showing all bulk discount tiers side-by-side.
The active tier (matching current quantity) is displayed in bold.

| Row | Content |
|-----|---------|
| 0 | Static header labels: `1`, `50+`, `100+`, `250+`, `500+`, `1000+` (one per column) |
| 1 | Dynamic price labels: `p_discPrice0` … `p_discPrice5` |
| 2 | Static discount labels: `—`, `10% off`, `20% off`, `25% off`, `40% off`, `50% off` |

Header labels: `font-weight=bold`, `halign=center`.
Price labels: `halign=center`, `selectable=True`, initial text `—`.
Discount labels: `halign=center`, `font-style=italic`,
`color=var(--color-text-secondary)` (or set via CSS).

---

### Link Button

```xml
<object class="GtkLinkButton" id="p_pothiLink">
    <property name="label" translatable="yes">Visit Pothi.com</property>
    <property name="visible">True</property>
    <property name="can-focus">True</property>
    <property name="receives-default">True</property>
    <property name="uri">https://pothi.com</property>
</object>
```

---

## Calculation Logic Summary

### Formula

```
price = fixed[size] + rate[size] × pages
      + bindingAdj[binding]
      + colorCost                   (if Full Color)
      + coatedCost                  (if Full Color AND Coated paper)
```

Where:
```
colorCost  = COLOR_FIXED + COLOR_RATE × pages   (≈ 114.55 + 2.105 × pages)
coatedCost = COATED_RATE × pages                (1.15 × pages)
```

### Verified size parameters

| Size | Fixed (₹) | Per-page rate (₹) |
|---|---|---|
| A5 | 67.00 | 0.85 |
| 5.5 inch x 8.5 inch | 72.00 | 0.80 |
| A4 | 83.00 | 1.30 |

### Binding adjustments (flat ₹, added to base)

| Binding | Adjustment |
|---|---|
| Soft Cover | ±₹0 |
| Saddle Stitched Binding | −₹25 |
| Hard Cover | +₹45 |

### Paper type

Plain White and Plain Natural Shade price identically — both use the base formula
with no adjustment. Coated paper adds ₹1.15/page **only when Full Color is selected**.

### Bulk discounts

Applied to the 1-copy price:

| Minimum quantity | Discount |
|---|---|
| 1 | 0% |
| 50 | 10% |
| 100 | 20% |
| 250 | 25% |
| 500 | 40% |
| 1000 | 50% |
| 1500+ | Custom quote — contact Pothi.com |

### Currency formatting

Indian locale: `₹X,XX,XXX.XX` (last group of 3 digits, then groups of 2 from the right).
Examples: `₹237.00`, `₹1,234.50`, `₹12,345.00`, `₹1,23,456.00`

---

## Key Implementation Constraints

1. **Never call `self.view.get(widgetName)`** for these widgets — the name-prefix dispatch
   in `gtkutils.getWidgetVal` won't recognise them and returns `None`. Always use
   `self._widget(name).get_value()` / `.get_active()` / `.set_text()` etc. directly.

2. **`setup()` must be idempotent** — guard with `self._setupDone`. The `prepare()` method
   is called every time the tab is activated; running `append_text()` twice creates
   duplicate combo entries.

3. **Signal connections** are made in `setup()` (once). The `onInputChanged` handler accepts
   an optional `widget` argument (GTK passes the emitting widget; it can be ignored since
   we re-read all widget states each time).

4. **All widget IDs are prefixed `p_`** to avoid collision with Print Gallery or other
   printer widgets in the shared `.glade` file.

5. **Tab label widget ID** must be `l_pr_pothi` — this is what `printer_from_label()` in
   `__init__.py` matches against to dispatch `prepare()` calls.

6. **Unverified sizes** suppress all output and show a warning. Do not display estimated
   or guessed prices — output `—` for all breakdown and summary fields. When a size is
   later verified, set `"verified": True` and fill `fixed`/`rate` in `SIZE_PARAMS`.
   No other code changes are required.

7. **Adding a new verified size**: collect at least 2–3 data points at different page counts
   (e.g. 100, 250, 500 pages; Soft Cover; Plain White; B&W; 1 copy) and confirm that prices
   fit a straight line (`price = fixed + rate × pages`) before marking as verified.
