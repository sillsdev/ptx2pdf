# Book Cost Calculator — PyGTK3+ Spec for Claude Code

## Overview

A standalone PyGTK3+ desktop app (using Glade for the UI) that calculates the print/binding cost of a book given its parameters. The logic mirrors a working web calculator and must produce identical results.

---

## Coding conventions

- PyGTK3+ with Glade (`.glade` XML file for UI layout)
- Python 3, UTF-8 source files
- camelCase for all variable and function names (e.g. `numPages`, `calcCost`, `coverSheets`)
- No pandas or numpy — plain Python arithmetic only
- File paths via `os.path.join(os.path.dirname(__file__), ...)` (never hardcoded)
- Single-file Python entry point: `bookCostCalc.py`
- Glade file: `bookCostCalc.glade`

---

## Rates (constants — define at top of Python file)

```python
RATES = {
    'cover300':  20,    # ₹/A3 sheet — 300 GSM wrap cover (perfect, staple)
    'cover130':  19,    # ₹/A3 sheet — 130 GSM board cover (case binding only)
    'bw':        10,    # ₹/A3 sheet — B&W interior printing
    'color':     14,    # ₹/A3 sheet — colour interior printing
    'lam':       20,    # ₹/A3 sheet — thermal lamination on cover
    'perfect':  150,    # ₹/copy — perfect binding
    'case':     250,    # ₹/copy — case (hardcover) binding
    'staple':    55,    # ₹/copy — book stapling
}
```

---

## Input fields

| Field | Widget | Values |
|---|---|---|
| Paper size | `GtkComboBoxText` (id: `sizeCombo`) | `a5` = "A5 (2-up on A3)", `a4` = "Larger than A5 (1-up on A3)" |
| Binding type | `GtkComboBoxText` (id: `bindingCombo`) | `perfect`, `case`, `staple` |
| Interior printing | `GtkComboBoxText` (id: `printCombo`) | `bw` = "B&W", `color` = "Colour" |
| Lamination | `GtkComboBoxText` (id: `lamCombo`) | `yes`, `no` |
| Number of pages | `GtkSpinButton` (id: `pagesSpin`) | min 8, step 8, default 128 |
| Number of copies | `GtkSpinButton` (id: `copiesSpin`) | min 1, step 1, default 5 |

All inputs connect to a single handler `onInputChanged` which recalculates on every change.

---

## Calculation logic

### Step 1 — Normalise page count
```python
pages = math.ceil(rawPages / 8) * 8
```
If `pages != rawPages`, show a warning label (id: `pageWarnLabel`):
`"Rounded up to nearest multiple of 8"`

### Step 2 — Normalise copy count (A5 only)
```python
if size == 'a5' and copies % 2 != 0:
    copies += 1
```
If copies were adjusted, show warning label (id: `copyWarnLabel`):
`"A5 books print in pairs — printing N copies"`
(substitute actual N)

### Step 3 — Sheet counts

**Interior sheets per copy:**
```python
interiorSheetsPerCopy = pages / 4   # double-sided A3 = 8 A5 pages = 4 pages per sheet
```

**A5 books (2-up on A3):**
```python
pairs = copies / 2
coverSheets   = pairs
interiorSheets = pairs * interiorSheetsPerCopy
lamSheets      = pairs
```

**Larger-than-A5 books (1-up on A3):**
```python
coverSheets    = copies
interiorSheets = copies * interiorSheetsPerCopy
lamSheets      = copies
```

### Step 4 — Costs

```python
coverRate    = RATES['cover130'] if binding == 'case' else RATES['cover300']
coverCost    = coverSheets * coverRate
interiorCost = interiorSheets * RATES[printType]
lamCost      = lamSheets * RATES['lam'] if laminate else 0
bindCost     = copies * RATES[binding]
total        = coverCost + interiorCost + lamCost + bindCost
perCopy      = total / copies
```

---

## Output display

All monetary values formatted as `₹X,XX,XXX.XX` (Indian locale grouping).

### Summary labels (update on every recalc)

| Label id | Content |
|---|---|
| `totalCostLabel` | Total cost e.g. `₹8,250.00` |
| `perCopyLabel` | Cost per copy e.g. `₹1,650.00` |
| `copiesPrintedLabel` | Effective copies printed e.g. `5` |

### Breakdown labels (update on every recalc)

| Label id | Example content |
|---|---|
| `coverBreakLabel` | `4 sheets × ₹20 = ₹80.00` |
| `interiorBreakLabel` | `160 sheets × ₹10 = ₹1,600.00` |
| `lamBreakLabel` | `4 sheets × ₹20 = ₹80.00` or `—` if no lam |
| `bindBreakLabel` | `5 copies × ₹150 = ₹750.00` |
| `totalBreakLabel` | Same as `totalCostLabel` |

---

## UI layout (Glade)

Single `GtkWindow` (title: "Book Cost Calculator"), not resizable preferred.

Suggested structure (vertical `GtkBox`):

```
GtkWindow
└── GtkBox (vertical, spacing 12, margin 16)
    ├── GtkGrid (2 col) — inputs: sizeCombo, bindingCombo, printCombo, lamCombo
    ├── GtkGrid (2 col) — inputs: pagesSpin + pageWarnLabel, copiesSpin + copyWarnLabel
    ├── GtkSeparator
    ├── GtkGrid (3 col) — summary: totalCostLabel, perCopyLabel, copiesPrintedLabel
    ├── GtkSeparator
    └── GtkGrid (2 col) — breakdown rows (label | value)
```

Warning labels (`pageWarnLabel`, `copyWarnLabel`) should be hidden by default (`visible=False`) and shown only when relevant. Style them orange/amber if possible via CSS provider.

---

## Signal connections (in Glade or Python)

Connect `changed` signal of all `GtkComboBoxText` widgets and `value-changed` of both `GtkSpinButton` widgets to `onInputChanged(widget)`.

`onInputChanged` reads all current widget values, runs the calculation, and updates all output labels.

---

## Entry point

```python
if __name__ == '__main__':
    app = BookCostApp()
    Gtk.main()
```

`BookCostApp.__init__` should:
1. Load the Glade file
2. Connect signals
3. Call `onInputChanged(None)` to populate outputs with defaults
4. Show the window

---

## Files to produce

- `bookCostCalc.py` — application logic + signal handlers
- `bookCostCalc.glade` — UI layout

No external dependencies beyond PyGTK3 (`gi.repository.Gtk`) and Python stdlib (`math`, `os`).
