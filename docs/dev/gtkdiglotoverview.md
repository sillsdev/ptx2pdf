# Diglot / Polyglot System — Developer Overview

A diglot (or polyglot) layout places two or more parallel translations side by side on the
page. This document describes how that feature is structured across the Python/GTK layer so
that a developer can modify it without getting lost.

---

## Terminology

| Term | Meaning |
|------|---------|
| **diglot** | Two-column parallel text (L + R). A special case of polyglot. |
| **polyglot** | Any multi-column parallel layout (L, R, A … G, up to 9 columns). |
| **suffix / code** | Single letter that identifies one column: `"L"` is always the primary project. |
| **L column** | The primary project loaded in PTXprint. Its settings live in the main config file, not in a separate `[diglot_L]`-derived `ViewModel`. |
| **diglot view** | A `ViewModel` instance that carries a *secondary* column's complete project settings. Lives in `self.diglotViews[suffix]`. |

---

## Files at a Glance

| File | Responsibility |
|------|---------------|
| `python/lib/ptxprint/polyglot.py` | `PolyglotConfig` data class — per-column metadata (project, config, fraction, fontsize, …). Reads/writes its own `[diglot_X]` config section. |
| `python/lib/ptxprint/gtkpolyglot.py` | `PolyglotSetup(Gtk.Box)` — the GTK tree-view widget that lets the user configure columns. Bridges between the UI and `PolyglotConfig` objects. |
| `python/lib/ptxprint/view.py` | `ViewModel` — owns `self.polyglots` (dict of `PolyglotConfig`) and `self.diglotViews` (dict of secondary `ViewModel`s). Handles config read/write for `[diglot_X]` sections. |
| `python/lib/ptxprint/gtkview.py` | `GtkViewModel` (subclass of `ViewModel`) — GTK signal handlers, creates `PolyglotSetup`, and calls `loadPolyglotSettings()`. |
| `src/ptx-diglot.tex` | TeX macros that implement the actual column balancing at typeset time. |

---

## Core Data Structures

### `PolyglotConfig` (`polyglot.py`)

One instance per column. All fields default to `None`.

```
code       — suffix letter ("L", "R", "A", …)
prj        — Paratext project ID string
prjguid    — project GUID
cfg        — configuration name within that project
pg         — spread page assignment ("1" = left, "2" = right)
fraction   — column width as a percentage (e.g. 50.0)
weight     — relative weight for text merging
fontsize   — font size in points
baseline   — line spacing (points)
captions   — whether figure captions are shown
color      — background colour hex string
```

`writeConfig()` skips any field that is still `None`, so unconfigured columns write no
spurious keys.

`configmap` maps config-file key names to `(attribute_name, type, [texmodel_keys])`.
The `texmodel_keys` list tells `updateTM()` which TeX-model dict entries to populate.

### `self.polyglots` (`ViewModel`)

`dict[str, PolyglotConfig]` keyed by suffix. Populated from `[diglot_X]` sections when
a config is loaded, and from `PolyglotSetup.updateRow()` whenever the UI changes.

### `self.diglotViews` (`ViewModel`)

`dict[str, ViewModel]` keyed by suffix (never contains `"L"`).
Each value is a full `ViewModel` loaded with the secondary project's own config. Used at
print time to drive TeX generation for that column. `"L"` is absent because the primary
`ViewModel` *is* the L column.

### `self.gtkpolyglot` (`GtkViewModel`)

Holds the single `PolyglotSetup` instance, or `None` when diglot is disabled.

---

## UI Widget: `PolyglotSetup`

`PolyglotSetup` is a `Gtk.Box` that wraps a `Gtk.TreeView` (`self.tv_polyglot`).

The ListStore model (`self.ls_treeview`) has one row per column. Column indices are named
via the `m` IntEnum:

```
m.code  m.pg  m.prj  m.cfg  m.captions  m.fontsize  m.baseline
m.fraction  m.weight  m.color  m.prjguid  m.tooltip  m.widcol  m.bold
```

`m.widcol` and `m.bold` are display-only (red/bold when % widths don't sum to 100 on a page).

### Virtual widget `polyfraction_`

`polyfraction_` is not a real GTK widget. It is stored directly in the view's `_dict` by
`updateRow(0)`:

```python
self.view.set("polyfraction_", self.ls_treeview[0][m.fraction])
```

`createConfig()` reads it back via `self.get("polyfraction_", asstr=True, skipmissing=True)`
and writes it to `[poly] fraction` in the config file. If `updateRow(0)` never runs before
`createConfig()`, the key is absent from the saved file.

---

## Config Lifecycle

### Reading a config

```
view.readConfig()
  └─ loadConfig(config)            — reads all ModelMap widgets into _dict
  └─ if c_diglot and not isDiglot:
       for each [diglot_X] section:
         PolyglotConfig.readConfig() → self.polyglots[X]
         createDiglotView(X)         → self.diglotViews[X]  (for X != "L")
```

The L column is *not* read via `PolyglotConfig.readConfig()`; its settings come from the
standard ModelMap widgets (font size, line spacing, etc.) in the main config sections.

### Displaying a config in the UI

```
gtkview.loadPolyglotSettings()
  └─ gtkpolyglot.clear_polyglot_treeview()
  └─ gtkpolyglot.load_polyglots_into_treeview()
       ├─ find_or_create_row("L")   — always creates row 0 if absent
       ├─ find_or_create_row("R")   — always creates row 1 if absent
       ├─ for each suffix in polyglots:
       │    find_or_create_row(sfx)
       │    populate row from PolyglotConfig attributes
       │    if sfx != "L": createDiglotView(sfx) to get fontsize/baseline defaults
       └─ updateRow(l_row_index)    — ALWAYS called unconditionally after the loop
            ├─ creates polyglots["L"] if missing
            ├─ copies L row data into polyglots["L"]
            └─ sets polyfraction_, s_fontsize, s_linespacing, _dibackcol in view._dict
```

`loadPolyglotSettings()` is called from:
- `gtkview.updateConfig()` — whenever a new project/config is loaded
- `gtkview.updateConfigIdentity()` — when the config name changes
- `gtkview.onDiglotClicked()` — when the user turns diglot on

### Writing a config

```
view.writeConfig()
  └─ createConfig()        — iterates ModelMap; reads polyfraction_ from _dict
  └─ if c_diglot:
       for k, p in self.polyglots.items():
           p.writeConfig(config, f"diglot_{k}")
```

`PolyglotConfig.writeConfig()` writes `[diglot_L]`, `[diglot_R]`, etc. sections.
`polyfraction_` ends up in `[poly] fraction` via the standard ModelMap path, *not* via
`PolyglotConfig.writeConfig()`.

---

## The L-Column Bootstrap Problem (and Fix)

**Symptom:** On the very first Print after enabling diglot and assigning projects, the
saved config is missing `[diglot_L]` and `[poly] fraction = …`.

**Root cause:**

1. `readConfig()` only populates `polyglots["L"]` if a `[diglot_L]` section already
   exists in the file.
2. `load_polyglots_into_treeview()` previously called `updateRow()` for L only inside
   the loop — i.e., only if `"L" in self.view.polyglots`. On a fresh setup neither was
   true, so `updateRow(0)` never ran.
3. Without `updateRow(0)`, `polyglots["L"]` was never created and `polyfraction_` was
   never written to `_dict`. `createConfig()` therefore skipped `poly/fraction`, and
   `writeConfig()` had no `polyglots["L"]` to serialize.

**Fix (`gtkpolyglot.py`):** `updateRow(l_row_index)` is now called **unconditionally
after the loop**, regardless of whether `"L"` was already in `self.view.polyglots`.
This guarantees `polyglots["L"]` exists and `polyfraction_` is set every time the UI
loads — even on the very first use.

---

## `updateRow()` — The Central Sync Point

```python
def updateRow(self, row_index):
    sfx = self.ls_treeview[row_index][m.code]
    plyglt = self.view.polyglots.get(sfx, None)
    if plyglt is None:
        plyglt = PolyglotConfig()
        plyglt.code = sfx
        self.view.polyglots[sfx] = plyglt          # creates polyglots[sfx]
    for idx, field in enumerate(_modelfields[1:11], start=1):
        setattr(plyglt, field, self.ls_treeview[row_index][idx])  # UI → PolyglotConfig
    if row_index == 0 and not self.view.noUpdate:
        # L row: also push values into the main view's _dict
        for a, b in {"fontsize": "s_fontsize", "baseline": "s_linespacing",
                     "fraction": "polyfraction_", "color": "_dibackcol"}.items():
            self.view.set(b, self.ls_treeview[row_index][getattr(m, a)])
```

`updateRow()` is the authoritative path for syncing the ListStore → `PolyglotConfig` →
view `_dict`. Call it whenever you change a ListStore row value programmatically.

---

## `createDiglotView()` — Creating a Secondary ViewModel

`view.createDiglotView(suffix)`:
1. Looks up `polyglots[suffix]` for project GUID and config name.
2. Constructs a new `ViewModel`, marks `isDiglot = True`, sets the project and config.
3. Stores the result in `self.diglotViews[suffix]`.
4. Raises `ValueError` (caught silently by callers) if the project or config is not found.

The L column **never** gets a `diglotViews` entry; `get_view("L")` in `PolyglotSetup`
returns `self.view` directly.

---

## Turning Diglot On and Off

**Enable (`onDiglotClicked`):**
```
sensiVisible("c_diglot")   — show/hide related widgets
loadPolyglotSettings()     — build PolyglotSetup, populate treeview
createDiglotView("R")      — create the R ViewModel (legacy fast path for simple diglot)
set("c_doublecolumn", True)
```

**Disable (`onDiglotClicked`):**
```
set_sensitive("c_doublecolumn", True)
self.diglotViews = {}      — drop all secondary ViewModels
```

`self.polyglots` is cleared at the start of `readConfig()` (when a new config is loaded),
and at the start of `onNewPrjClicked()` (when a new project is selected).

---

## Row 0 and Row 1 Are Special

- **Row 0 (L):** Code, project, and config are locked (cannot be changed via the combo
  cells — `on_combo_changed` returns early for row 0 except for `pg` and `fraction`).
  The project always mirrors the primary PTXprint project.
- **Row 1 (R):** Move-up/move-down and delete are disabled alongside row 0 to prevent the
  user from removing the mandatory L+R pair.

---

## Layout String (`t_layout`)

The `t_layout` text widget stores a compact description of the page spread, e.g. `LR` or
`LA,RB`. It is generated from the treeview by `generate_layout_from_treeview()` and
validated by `validate_layout()`. The preview widget (`bx_layoutPreview`) is re-rendered
on every change via `update_layout_preview()`.

Rules enforced by `validate_layout()`:
- L and R must always be present.
- A comma separates page 1 codes from page 2 codes.
- A slash (`/`) stacks codes vertically within a page (complex layouts, limited support).
- All codes present in the treeview must appear in the layout string.
- % widths on each page must sum to 100 (red highlight in the treeview if not).

---

## Right-Click Context Menu

The treeview right-click menu is rebuilt on every right-click (to avoid stale state). It
provides: Add row, Move Up/Down, Copy Font Size to All, Copy Spacing to All, Distribute
Widths, Delete Row, Edit Settings (opens the secondary project's config dialog via
`switchToDiglot()`), Set Color, Remove All Colors.

`ensure_right_click_handler()` disconnects any previous signal handler before connecting a
new one, preventing duplicate handler accumulation across config reloads.

---

## Switching to a Secondary Column's Config

`switchToDiglot(pref)` in `GtkViewModel` saves the current config, then temporarily
replaces the main window's project with the secondary column's `ViewModel`. The main window
button label changes to "Return to Primary". On return, the primary state is restored.
This allows the user to edit settings for column R (or A, B, …) using the full PTXprint UI.

---

## Common Pitfalls

1. **Forgetting `updateRow()` after a programmatic ListStore change.** Any code that sets
   `self.ls_treeview[row][col] = value` directly must call `updateRow(row)` afterwards to
   sync the change to `PolyglotConfig` and the view's `_dict`.

2. **`polyfraction_` disappearing from the config.** This only gets written to `_dict` by
   `updateRow(0)`. If you add a new code path that skips `load_polyglots_into_treeview()`
   or bypasses `updateRow(0)`, `[poly] fraction` will be missing from the saved file.

3. **`createDiglotView()` returns `None` silently.** If `polyglots[suffix]` exists but has
   a `None` project or config (fresh row not yet filled in), `createDiglotView()` raises
   `ValueError`. Callers catch this and skip the row — check logs if a column disappears.

4. **`PolyglotConfig.writeConfig()` skips `None` fields.** A field that was never set will
   not appear in the saved config section. On reload, `PolyglotConfig.readConfig()` leaves
   that attribute at `None`, and `updateTM()` skips `None` values. This is intentional
   fallback behaviour but can cause confusion when debugging missing config keys.

5. **`isDiglot` flag.** Secondary `ViewModel` instances have `isDiglot = True`. Certain
   code paths in `view.py` and `gtkview.py` branch on `not self.isDiglot` to avoid
   re-entrant diglot setup or double-writing config sections. Do not set this flag on the
   primary view.
