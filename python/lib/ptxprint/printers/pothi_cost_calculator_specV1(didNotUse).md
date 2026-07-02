# Pothi.com Cost Calculator — PyGTK3+ Spec for Claude Code

## Overview

A standalone PyGTK3+ desktop app (using Glade for the UI) that calculates the
author/printing price of a book on Pothi.com given its specifications. The
formula was reverse-engineered from 21 verified data points with zero error.
Prices are in Indian Rupees (₹).

---

## Coding conventions

- PyGTK3+ with Glade (`.glade` XML file for UI layout)
- Python 3, UTF-8 source files
- camelCase for all variable and function names
- No pandas or numpy — plain Python arithmetic only
- File paths via `os.path.join(os.path.dirname(__file__), ...)`
- Entry point: `pothiCostCalc.py`
- Glade file: `pothiCostCalc.glade`

---

## Dropdown option wording (use exact Pothi.com site strings)

### Page size (id: `sizeCombo`)
Options in this order, using these exact strings as display labels:
```
5 inch x 7 inch
5 inch x 8 inch
A5
5.5 inch x 8.5 inch
6 inch x 9 inch
7 inch x 9 inch
8 inch x 11 inch
A4
```
Internal keys (for formula lookup): `5x7`, `5x8`, `a5`, `5585`, `6x9`, `7x9`, `8x11`, `a4`

### Binding (id: `bindingCombo`)
```
Soft Cover
Saddle Stitched Binding
Hard Cover
```
Internal keys: `soft`, `saddle`, `hard`

### Paper type (id: `paperCombo`)
```
Plain White (70-80 GSM)
Plain Natural Shade (70-80 GSM)
Coated (90-120 GSM)
```
Internal keys: `plain`, `plain`, `coated`
Note: Plain White and Plain Natural Shade price identically — both map to `plain`.

### Interior color (id: `colorCombo`)
```
B&W interior (colored cover)
Full Color (Interior & Cover)
```
Internal keys: `bw`, `full`

---

## Pricing constants (define at top of Python file)

```python
# Verified against 21 Pothi.com data points — zero error
# FORMAT: {key: {'fixed': float, 'rate': float, 'verified': bool}}
# 'fixed' = base fixed cost (₹), 'rate' = per-page rate (₹/page)
SIZE_PARAMS = {
    '5x7':  {'fixed': None, 'rate': None, 'verified': False},  # TODO: add data
    '5x8':  {'fixed': None, 'rate': None, 'verified': False},  # TODO: add data
    'a5':   {'fixed': 67.0, 'rate': 0.85, 'verified': True},
    '5585': {'fixed': 72.0, 'rate': 0.80, 'verified': True},
    '6x9':  {'fixed': None, 'rate': None, 'verified': False},  # TODO: add data
    '7x9':  {'fixed': None, 'rate': None, 'verified': False},  # TODO: add data
    '8x11': {'fixed': None, 'rate': None, 'verified': False},  # TODO: add data
    'a4':   {'fixed': 83.0, 'rate': 1.30, 'verified': True},
}

# Binding adjustments (flat ₹, added to base price)
# Verified: hard=+45 and saddle=-25 are consistent across A5, 5.5x8.5, A4
BINDING_ADJ = {
    'soft':   0,
    'saddle': -25,
    'hard':   +45,
}

# Full color premium: fixed charge + per-page rate
# Derived from two data points spanning 100-1200 pages
COLOR_FIXED = 1260 / 11   # ≈ 114.55
COLOR_RATE  = 463  / 220  # ≈ 2.105 per page

# Coated paper premium: applies ONLY when color == 'full'
COATED_RATE = 1.15  # ₹/page extra

# Bulk discount tiers (applied to 1-copy price)
DISCOUNT_TIERS = [
    (1,    0),
    (50,   10),
    (100,  20),
    (250,  25),
    (500,  40),
    (1000, 50),
]
```

---

## Calculation logic

```python
def calcPrice(sizeKey, bindingKey, paperKey, colorKey, pages, qty):
    """
    Returns (price1copy, pricePerCopyAtQty, totalPrice, discountPct, breakdown)
    breakdown is a dict of cost components for display.
    Returns None if sizeKey is unverified (no data yet).
    """
    params = SIZE_PARAMS[sizeKey]
    if not params['verified']:
        return None

    base = params['fixed'] + params['rate'] * pages
    bindAdj = BINDING_ADJ[bindingKey]
    colorCost = (COLOR_FIXED + COLOR_RATE * pages) if colorKey == 'full' else 0
    coatedCost = (COATED_RATE * pages) if (paperKey == 'coated' and colorKey == 'full') else 0

    price1 = base + bindAdj + colorCost + coatedCost

    discPct = 0
    for minQty, pct in DISCOUNT_TIERS:
        if qty >= minQty:
            discPct = pct

    priceAtQty = price1 * (1 - discPct / 100)
    totalPrice = priceAtQty * qty

    breakdown = {
        'base':    base,
        'bindAdj': bindAdj,
        'color':   colorCost,
        'coated':  coatedCost,
        'total':   price1,
    }
    return price1, priceAtQty, totalPrice, discPct, breakdown
```

---

## Validity rules (show warnings, not errors)

| Condition | Warning label text |
|---|---|
| `saddle` and pages > 64 | "Saddle stitched binding is only available for 10–64 pages." |
| `soft` and pages < 50 | "Soft cover requires a minimum of 50 pages." |
| `soft` and pages > 500 | "Soft cover maximum is 500 pages." |
| `hard` and pages > 500 | "Hard cover for 500+ pages — verify availability on Pothi.com." |
| size not yet verified | "Pricing data for this page size has not yet been verified. Results will appear once data is added." |
| `qty` >= 1500 | "For 1500+ copies, contact Pothi.com directly for a custom quote." |

Warnings are shown in a `GtkLabel` (id: `warnLabel`, styled amber/orange via CSS provider).
The calculator still shows its best estimate where possible; only the unverified-size case
suppresses output entirely.

---

## Output display

All monetary values formatted as Indian locale: `₹X,XX,XXX.XX`

```python
def fmtRupees(amount):
    # Indian grouping: last 3 digits, then groups of 2
    s = f"{amount:.2f}"
    integer, decimal = s.split('.')
    if len(integer) <= 3:
        return f"₹{integer}.{decimal}"
    last3 = integer[-3:]
    rest = integer[:-3]
    groups = []
    while len(rest) > 2:
        groups.insert(0, rest[-2:])
        rest = rest[:-2]
    if rest:
        groups.insert(0, rest)
    return f"₹{','.join(groups)},{last3}.{decimal}"
```

### Summary labels

| Widget id | Content |
|---|---|
| `price1Label` | 1-copy price e.g. `₹237.00` |
| `priceQLabel` | Per-copy price at qty e.g. `₹189.60 (20% off)` |
| `priceTotalLabel` | Total e.g. `₹1,896.00` |

### Breakdown labels

| Widget id | Content |
|---|---|
| `baseBreakLabel` | e.g. `₹67.00 + ₹0.85/pg × 200 = ₹237.00` |
| `bindBreakLabel` | e.g. `+₹45.00 (hard cover)` or `—` |
| `colorBreakLabel` | e.g. `₹114.55 + ₹2.11/pg × 200 = ₹536.45` or `—` |
| `coatedBreakLabel` | e.g. `₹1.15/pg × 200 = ₹230.00` or `—` |
| `totalBreakLabel` | Same as `price1Label` |

### Discount tier grid

Display 6 small cards in an `GtkFlowBox` or `GtkGrid` (3 col × 2 row), one per tier:
- Quantity label: `1`, `50+`, `100+`, `250+`, `500+`, `1000+`
- Price per copy at that tier
- Discount percentage: `—`, `10% off`, `20% off`, etc.
Highlight the active tier (matching current qty) with a colored border.

---

## UI layout (Glade)

Single `GtkWindow` (title: "Pothi.com Cost Calculator").

```
GtkWindow
└── GtkBox (vertical, spacing 12, margin 16)
    ├── GtkGrid (2 col) — sizeCombo, bindingCombo
    ├── GtkGrid (2 col) — paperCombo, colorCombo
    ├── GtkGrid (2 col) — pagesSpin (min 10, step 2), qtySpin (min 1, step 1)
    ├── GtkLabel (id: warnLabel, hidden by default)
    ├── GtkSeparator
    ├── GtkGrid (3 col) — price1Label, priceQLabel, priceTotalLabel
    ├── GtkSeparator
    ├── GtkGrid (2 col) — breakdown rows (label | value)
    ├── GtkSeparator
    └── GtkFlowBox or GtkGrid — discount tier cards (6 items)
```

---

## Signal connections

Connect `changed` on all four `GtkComboBoxText` widgets and `value-changed` on
both `GtkSpinButton` widgets to a single handler `onInputChanged(widget)`.

`onInputChanged` reads all widget values, calls `calcPrice`, and updates all
output labels and the discount grid.

---

## Entry point

```python
if __name__ == '__main__':
    app = PothiCostApp()
    Gtk.main()
```

`PothiCostApp.__init__` should:
1. Load the Glade file
2. Connect signals
3. Set default combo selections: A5 / Soft Cover / Plain White / B&W
4. Call `onInputChanged(None)` to populate defaults
5. Show the window

---

## Files to produce

- `pothiCostCalc.py` — application logic + signal handlers
- `pothiCostCalc.glade` — UI layout

Dependencies: PyGTK3 (`gi.repository.Gtk`) and Python stdlib (`math`, `os`) only.

---

## Adding data for unverified sizes later

To add a new size, replace its `None` values in `SIZE_PARAMS` and set
`'verified': True`. The rest of the app requires no changes — the warning
will disappear automatically and the calculator will activate for that size.

Recommended: gather at least 2–3 page-count data points per size (e.g. 100,
250, 500 pages, soft cover, plain white, B&W) and verify linearity before
marking as verified.
