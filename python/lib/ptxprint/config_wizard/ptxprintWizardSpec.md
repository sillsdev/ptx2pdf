# PTXprint Setup Wizard — Specification

**Status:** Draft v1 — for handoff to a coding LLM
**Target stack:** Python 3.11+, PyGTK3 (Gtk 3.x via PyGObject), programmatic GTK (no Glade)
**Naming convention:** camelCase throughout (Python identifiers, JSON keys, Glade widget IDs)
**Audience:** An LLM with access to the PTXprint source tree, generating an initial implementation that the PTXprint maintainers will review and refine.

---

## 1. Purpose & Scope

A wizard that guides a user from "I want to print Scripture" to a working PTXprint configuration, working from end-user needs back to layout decisions. It produces either a new named configuration or applies changes to the current one. It auto-launches when a project is opened with no existing configuration, and is also accessible from the main PTXprint menu.

### 1.1 Non-goals

- Authoring peripherals (glossary, maps, etc.) — the wizard only flags which peripherals exist and lets the user mark which to include.
- Sending jobs to printers or POD services.
- Managing Paratext content directly.
- Replacing the existing full PTXprint UI; the wizard is an additional path.

---

## 2. Conventions

- **Naming:** camelCase for all identifiers, including JSON keys, Python variables, methods, classes (PascalCase for class names as usual), Glade widget IDs.
- **Localisation:** all user-facing strings go through PTXprint's existing localisation mechanism. The coding LLM should match how the rest of the codebase wraps strings.
- **Logging:** use PTXprint's existing logger.
- **No new heavy dependencies.** Stick to PyGObject, the standard library, and whatever PTXprint already pulls in.
- **JSON files** live under `config-wizard/data/` within the PTXprint resources tree.

---

## 3. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     WizardWindow (Gtk.Window)               │
│ ┌──────────────┬──────────────────────┬──────────────────┐  │
│ │              │                      │                  │  │
│ │   Sidebar    │   Active Section     │  Feedback Panel  │  │
│ │  Dashboard   │      Panel           │   (live preview, │  │
│ │              │                      │    page count,   │  │
│ │  - Recipe    │  (one of 7 sections) │    cost L/M/H,   │  │
│ │  - Audience  │                      │    warnings)     │  │
│ │  - Producti. │                      │                  │  │
│ │  - Trim/Bind │                      │                  │  │
│ │  - Content   │                      │                  │  │
│ │  - Periph.   │                      │                  │  │
│ │  - Layout    │                      │                  │  │
│ │  - Review    │                      │                  │  │
│ │              │                      │                  │  │
│ │ [Back][Next] │                      │                  │  │
│ └──────────────┴──────────────────────┴──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
        │                  │                     │
        ▼                  ▼                     ▼
   WizardState       ConstraintsEngine      CostEstimator
   (in-memory)       (JSON-driven)          (JSON-driven)
        │                  │                     │
        └────────┬─────────┴─────────────────────┘
                 ▼
          SettingsMapper
        (wizard answers → PTXprint config keys)
                 ▼
          PTXprint Project
```

### 3.1 Core components

| Component | Responsibility |
|---|---|
| `WizardWindow` | Top-level Gtk.Window holding the three panes |
| `SidebarDashboard` | Section list, states, navigation, Back/Next |
| `SectionPanel` (abstract) | One per section; loads its own Glade fragment |
| `FeedbackPanel` | Live updates: page-count estimate, cost L/M/H, warnings, thumbnail |
| `WizardState` | In-memory model of every answer; serialisable to JSON for save/resume |
| `ConstraintsEngine` | Loads `constraints.json`; validates state, computes section staleness, filters allowed values |
| `CostEstimator` | Loads `costRules.json`; computes per-copy and total cost as L/M/H |
| `PageCountEstimator` | Computes estimated page count from content scope, trim, font, columns, peripherals |
| `RecipeLoader` | Loads `recipes/*.json`; applies a recipe to `WizardState` |
| `SettingsMapper` | Translates `WizardState` into PTXprint config setting keys/values; produces a diff |
| `WizardController` | Glues everything together; handles section transitions, state changes, event propagation |

---

## 4. Module / File Layout

```
ptxprint/
└── config-wizard/
    ├── __init__.py
    ├── wizardWindow.py            # WizardWindow class
    ├── wizardController.py        # WizardController
    ├── wizardState.py             # WizardState dataclass + serialisation
    ├── sidebarDashboard.py        # SidebarDashboard widget
    ├── feedbackPanel.py           # FeedbackPanel widget
    ├── constraintsEngine.py       # ConstraintsEngine
    ├── costEstimator.py           # CostEstimator
    ├── pageCountEstimator.py      # PageCountEstimator
    ├── recipeLoader.py            # RecipeLoader
    ├── settingsMapper.py          # SettingsMapper
    ├── sections/
    │   ├── __init__.py
    │   ├── sectionBase.py         # Abstract SectionPanel
    │   ├── recipeSection.py
    │   ├── audienceSection.py
    │   ├── productionSection.py
    │   ├── trimBindingSection.py
    │   ├── contentSection.py
    │   ├── peripheralsSection.py
    │   ├── layoutSection.py
    │   └── reviewSection.py
    └── data/
        ├── constraints.json
        ├── costRules.json
        ├── peripheralsCatalogue.json
        └── recipes/
            ├── trialNewTestament.json
            ├── pewBible.json
            ├── distributionBible.json
            ├── pocketNewTestament.json
            ├── largePrintPsalms.json
            ├── childrenScripturePortion.json
            ├── diglotNewTestament.json
            └── studyBible.json
```

---

## 5. Data Model

### 5.1 WizardState (Python dataclass)

```python
@dataclass
class WizardState:
    schemaVersion: int = 1
    recipeId: Optional[str] = None       # which recipe was loaded, if any
    audience: AudienceState = field(default_factory=AudienceState)
    production: ProductionState = field(default_factory=ProductionState)
    trimBinding: TrimBindingState = field(default_factory=TrimBindingState)
    content: ContentState = field(default_factory=ContentState)
    peripherals: PeripheralsState = field(default_factory=PeripheralsState)
    layout: LayoutState = field(default_factory=LayoutState)
    sectionStatus: Dict[str, SectionStatus] = field(default_factory=dict)
    # SectionStatus enum: notStarted, inProgress, complete, stale, hasWarnings

@dataclass
class AudienceState:
    purpose: Optional[str] = None        # e.g. "pewBible", "evangelism", "personalReading", "trial", "study"
    copyCount: Optional[int] = None
    ageGroup: Optional[str] = None       # "children", "youth", "adult", "elderly", "mixed"
    eyesightConsideration: Optional[str] = None  # "standard", "largePrint", "veryLargePrint"
    readingContext: Optional[str] = None # "pulpit", "pew", "personal", "field", "study"
    literacyLevel: Optional[str] = None  # "newReader", "developing", "fluent"
    distributionModel: Optional[str] = None  # "sold", "donorFunded", "free"
    budgetLevel: Optional[str] = None    # "low", "medium", "high", "unconstrained"

@dataclass
class ProductionState:
    method: Optional[str] = None         # "localPrinter", "officeDuplex", "podService", "shortRunDigital", "offset"
    podProvider: Optional[str] = None    # "lulu", "ingramSpark", "kdp", "other"  -- relevant only if method == podService

@dataclass
class TrimBindingState:
    trimSize: Optional[str] = None       # named size, e.g. "a5", "sixByNine", "letter"
    bindingType: Optional[str] = None    # "saddleStitch", "perfectBound", "caseBound", "spiral"
    paperType: Optional[str] = None      # "standard", "cream", "biblePaper28", "biblePaper36"

@dataclass
class ContentState:
    scope: Optional[str] = None          # "wholeBible", "newTestament", "oldTestament", "portion", "custom"
    selectedBooks: List[str] = field(default_factory=list)  # USFM 3-letter codes
    isDiglot: bool = False
    isTriglot: bool = False
    secondaryProject: Optional[str] = None
    tertiaryProject: Optional[str] = None
    includeUnchecked: bool = False       # if True, books with incomplete checks are included with warning

@dataclass
class PeripheralsState:
    selected: List[str] = field(default_factory=list)  # IDs from peripheralsCatalogue.json

@dataclass
class LayoutState:
    columns: Optional[int] = None        # 1 or 2
    bodyFontSize: Optional[float] = None
    bodyLeading: Optional[float] = None
    bodyFont: Optional[str] = None
    marginPreset: Optional[str] = None   # "tight", "standard", "generous"
    # advanced overrides remain accessible via main PTXprint UI
```

### 5.2 constraints.json — schema

```json
{
  "schemaVersion": 1,
  "fields": {
    "audience.purpose": {
      "type": "enum",
      "values": ["pewBible", "evangelism", "personalReading", "trial", "study", "childrensScripture"]
    },
    "audience.copyCount": { "type": "integer", "min": 1 },
    "production.method": {
      "type": "enum",
      "values": ["localPrinter", "officeDuplex", "podService", "shortRunDigital", "offset"]
    },
    "trimBinding.trimSize": {
      "type": "enum",
      "values": ["a4", "a5", "a6", "letter", "halfLetter", "fiveByEight", "sixByNine", "sevenByTen"]
    }
    // ... one entry per WizardState field
  },
  "rules": [
    {
      "id": "offsetMinimumQuantity",
      "severity": "warning",
      "when": { "production.method": "offset" },
      "require": { "audience.copyCount": { "min": 1000 } },
      "message": "Offset printing is rarely economical below ~1000 copies. Consider short-run digital or POD."
    },
    {
      "id": "saddleStitchPageLimit",
      "severity": "error",
      "when": { "trimBinding.bindingType": "saddleStitch" },
      "require": { "estimatedPageCount": { "max": 64 } },
      "message": "Saddle-stitch binding is impractical above ~64 pages."
    },
    {
      "id": "biblePaperOnlyOffset",
      "severity": "warning",
      "when": { "trimBinding.paperType": ["biblePaper28", "biblePaper36"] },
      "require": { "production.method": "offset" },
      "message": "Bible paper (lightweight) is generally only available through offset printers."
    },
    {
      "id": "podTrimSizeAllowed",
      "severity": "error",
      "when": { "production.method": "podService", "production.podProvider": "ingramSpark" },
      "require": { "trimBinding.trimSize": ["fiveByEight", "sixByNine", "sevenByTen", "a5"] },
      "message": "IngramSpark does not offer the selected trim size."
    },
    {
      "id": "largePrintFontFloor",
      "severity": "warning",
      "when": { "audience.eyesightConsideration": "largePrint" },
      "require": { "layout.bodyFontSize": { "min": 12.0 } },
      "message": "Large-print editions typically use at least 12pt body text."
    }
    // ... etc
  ],
  "dependencies": [
    { "section": "production",   "dependsOn": ["audience"] },
    { "section": "trimBinding",  "dependsOn": ["production", "audience"] },
    { "section": "content",      "dependsOn": ["audience"] },
    { "section": "peripherals",  "dependsOn": ["audience", "content"] },
    { "section": "layout",       "dependsOn": ["audience", "trimBinding"] },
    { "section": "review",       "dependsOn": ["audience", "production", "trimBinding", "content", "peripherals", "layout"] }
  ],
  "filterRules": [
    {
      "id": "podLimitsTrimSize",
      "field": "trimBinding.trimSize",
      "when": { "production.method": "podService", "production.podProvider": "lulu" },
      "allowedValues": ["a5", "fiveByEight", "sixByNine", "halfLetter"]
    }
    // filterRules dynamically restrict the values shown in dropdowns
  ]
}
```

### 5.3 costRules.json — schema

Cost is reported on two axes: `perCopy` and `total`, each as `low | medium | high`. Rules are evaluated in order; the first matching rule per axis wins. If no rule matches, return `unknown`.

```json
{
  "schemaVersion": 1,
  "perCopy": [
    { "when": { "production.method": "offset", "audience.copyCount": { "min": 5000 } }, "value": "low" },
    { "when": { "production.method": "offset" }, "value": "medium" },
    { "when": { "production.method": "officeDuplex" }, "value": "low" },
    { "when": { "production.method": "localPrinter" }, "value": "medium" },
    { "when": { "production.method": "shortRunDigital" }, "value": "medium" },
    { "when": { "production.method": "podService" }, "value": "high" }
  ],
  "total": [
    { "when": { "production.method": "offset" }, "value": "high" },
    { "when": { "audience.copyCount": { "min": 1000 } }, "value": "high" },
    { "when": { "audience.copyCount": { "min": 200 } }, "value": "medium" },
    { "when": {}, "value": "low" }
  ]
}
```

These tables are rough-and-ready; PTXprint maintainers tune them in the JSON without code changes.

### 5.4 peripheralsCatalogue.json

```json
{
  "schemaVersion": 1,
  "categories": [
    {
      "id": "navigation",
      "label": "Navigation & Reference",
      "items": [
        { "id": "tableOfContents", "label": "Table of Contents", "estimatedPages": 2 },
        { "id": "bookIntroductions", "label": "Book Introductions", "estimatedPagesPerBook": 1 },
        { "id": "crossReferences", "label": "Cross-references", "estimatedPagesDelta": 0, "note": "Adds inline column space; doesn't add pages directly" }
      ]
    },
    {
      "id": "study",
      "label": "Study Helps",
      "items": [
        { "id": "footnotes", "label": "Footnotes", "estimatedPagesDelta": 0 },
        { "id": "studyNotes", "label": "Study Notes", "estimatedPagesDelta": 0 },
        { "id": "glossary", "label": "Glossary", "estimatedPages": 8 },
        { "id": "concordance", "label": "Concordance", "estimatedPages": 40 },
        { "id": "strongsIndex", "label": "Strong's Index", "estimatedPages": 60 },
        { "id": "weightsAndMeasures", "label": "Weights & Measures", "estimatedPages": 2 },
        { "id": "readingPlan", "label": "Reading Plan", "estimatedPages": 4 },
        { "id": "parallelPassages", "label": "Parallel Passages", "estimatedPages": 4 }
      ]
    },
    {
      "id": "visual",
      "label": "Visual Content",
      "items": [
        { "id": "maps", "label": "Maps", "estimatedPages": 8 },
        { "id": "illustrations", "label": "Illustrations", "estimatedPagesDelta": 0, "note": "Inline; affects page flow" }
      ]
    }
  ]
}
```

The `available` flag for each peripheral at runtime comes from PTXprint inspecting the project — see §10.

### 5.5 Recipe schema

Each recipe in `recipes/*.json` is a partial `WizardState` plus metadata:

```json
{
  "id": "trialNewTestament",
  "label": "Trial New Testament for Community Feedback",
  "description": "A modest run of the New Testament, A5, perfect-bound, printed locally — for community review and feedback before a full publication.",
  "tags": ["nt", "draft", "smallRun"],
  "state": {
    "audience": {
      "purpose": "trial",
      "copyCount": 50,
      "ageGroup": "adult",
      "eyesightConsideration": "standard",
      "readingContext": "personal",
      "distributionModel": "free",
      "budgetLevel": "low"
    },
    "production": { "method": "localPrinter" },
    "trimBinding": {
      "trimSize": "a5",
      "bindingType": "perfectBound",
      "paperType": "standard"
    },
    "content": { "scope": "newTestament" },
    "peripherals": { "selected": ["tableOfContents", "bookIntroductions"] },
    "layout": {
      "columns": 1,
      "bodyFontSize": 10.5,
      "bodyLeading": 12.5,
      "marginPreset": "standard"
    }
  }
}
```

---

## 6. Constraints Engine — Semantics

### 6.1 Inputs
- The full `WizardState`
- Computed values: `estimatedPageCount`, `spineWidthMm`, `costPerCopy`, `costTotal`

### 6.2 Outputs
- Per field: list of allowed values (after `filterRules`)
- Per rule: `passed | warning | error` plus the rule's message
- Per section: aggregate status (`complete`, `inProgress`, `stale`, `hasWarnings`)

### 6.3 Staleness
A section becomes `stale` when:
- It was previously `complete`, AND
- A field in a section it `dependsOn` has changed since this section was last visited.

The engine tracks a per-field `lastModifiedSeq` counter and a per-section `lastVisitedSeq`. `stale` = any dependency field's `lastModifiedSeq` > this section's `lastVisitedSeq`.

### 6.4 Rule evaluation
- `when` clauses are AND-combined. A clause matches if every key matches the given value (scalar, list = "any of", or `{ "min": x, "max": y }`).
- `require` clauses are AND-combined and use the same matcher.
- A rule that matches `when` but fails `require` produces a violation at its declared `severity`.

### 6.5 Section completeness
A section is `complete` when every required field (declared per-section in `constraints.json`) has a non-null value AND no `error`-severity rules are currently violated for fields owned by that section. `hasWarnings` overlays on `complete` if warning-severity rules are active.

---

## 7. UI Specification

### 7.1 Top-level WizardWindow

- Modal-ish: not strictly modal, but takes focus. Closing prompts "save and resume later? / discard / cancel-close".
- Three-pane horizontal layout (Gtk.Paned), proportions roughly 22% / 53% / 25%.
- Header bar with title, current section name, and close button.

### 7.2 Sidebar Dashboard

Vertical list. Each row:
```
[icon]  Section Name           [statusBadge]
```
- Icon: small graphic per section.
- Status badge: colour + glyph: ⚪ notStarted, 🟡 inProgress, ✅ complete, ⚠ hasWarnings, 🔄 stale.
- Clicking a row switches the centre pane to that section. No gating on jumping forward, but sections that can't be evaluated yet show a "depends on earlier sections" notice in the centre pane.
- Bottom of sidebar: `Back` and `Next` buttons. `Next` advances through the standard order, skipping disabled sections. On the last section (Review), `Next` becomes `Finish`.

### 7.3 Section Panels

Each section panel is loaded from its own Glade file. Common contract:

```python
class SectionPanel(Gtk.Box):
    sectionId: str

    def loadFromState(self, state: WizardState) -> None: ...
    def saveToState(self, state: WizardState) -> None: ...
    def onConstraintsChanged(self, engine: ConstraintsEngine) -> None: ...
        # called whenever upstream answers change; refreshes allowed values
    def isComplete(self) -> bool: ...
```

Each section emits a `stateChanged` signal that the controller listens to.

### 7.4 Feedback Panel

Right-hand pane, always visible. Updates on every state change.

Contents:
- **Estimated page count** (single integer, recomputed live)
- **Estimated spine width** (mm, when binding/paper/page-count permit)
- **Per-copy cost** — bar with three segments, active = L / M / H
- **Total cost** — same
- **Warnings list** — collapsible; one line per active warning/error
- **Thumbnail preview** — small image showing trim size, columns, rough text density. Generated from a templated SVG (no live LaTeX run; just a representative thumbnail). Optional in v1; placeholder acceptable.

### 7.5 Glade widget IDs

All widget IDs use camelCase and a section prefix, e.g. `audiencePurposeCombo`, `trimBindingTrimSizeCombo`, `feedbackPageCountLabel`. The coding LLM should adopt this convention consistently.

---

## 8. Section-by-Section Specification

### 8.1 Recipe section

- List of bundled recipes (cards: label, description, tags).
- "Start from scratch" option.
- "Load saved wizard state" option (resume).
- Selecting a recipe populates `WizardState` and marks all touched sections as `inProgress`. The user can then edit anything.
- This section is itself optional — skipping goes straight to Audience.

### 8.2 Audience section

Fields and widget types:

| Field | Widget | Notes |
|---|---|---|
| `purpose` | radio group | with one-line descriptions |
| `copyCount` | spinbutton | min 1, no upper bound; "more than 10 000?" warning past large numbers |
| `ageGroup` | combo | |
| `eyesightConsideration` | combo | "standard / large print / very large print" |
| `readingContext` | combo | |
| `literacyLevel` | combo | |
| `distributionModel` | combo | |
| `budgetLevel` | combo | low / medium / high / unconstrained |

Each field has an info button (ⓘ) that opens an inline expander with "why this matters."

### 8.3 Production section

- Radio group of methods: localPrinter, officeDuplex, podService, shortRunDigital, offset.
- Each option shows: typical run size range, typical per-copy cost band, typical setup cost, typical lead time, typical strengths/weaknesses (one-liners, sourced from `constraints.json`).
- If `podService`: a sub-combo for provider (lulu / ingramSpark / kdp / other).
- Constraints engine warns or errors on mismatches with `audience.copyCount`.

### 8.4 Trim & Binding section

- `trimSize`: combo, dynamically filtered by production method + provider via `filterRules`.
- `bindingType`: combo, dynamically filtered.
- `paperType`: combo, dynamically filtered (Bible paper grayed out for non-offset).
- Each combo entry shows a one-line note about what it's typically used for.

### 8.5 Content section

- `scope`: radio (wholeBible, newTestament, oldTestament, portion, custom).
- `selectedBooks`: tree/list of all books in the project, with check status badges:
  - ✅ ready (passed all enabled Paratext checks)
  - 🟡 in progress (some checks failing or not run)
  - ⚪ not started
  - ⚠ has errors
- Filter toggle: "Show ready books only."
- Bulk actions: "Select all ready," "Select NT," "Select OT."
- `includeUnchecked` checkbox with appropriate warning.
- `isDiglot` / `isTriglot` checkboxes; when checked, project picker(s) appear for secondary/tertiary project.
- Diglot/triglot also affects book selector — books must be present in all selected projects to be selectable; missing-from-secondary books are flagged.

### 8.6 Peripherals section

- Driven by `peripheralsCatalogue.json` plus per-project availability data.
- Grouped by category. Each item:
  - Checkbox to include
  - Status indicator: "available in project" / "not yet created in project" / "always available (generated)"
  - Page-cost estimate
- Items that are `not yet created` are still selectable, but a note appears: "You will need to create this in PTXprint after the wizard completes."
- A bulk preset row at the top: "Minimal / Standard / Study" — sets sensible defaults.

### 8.7 Layout section

- `columns`: 1 or 2 (radio).
- `bodyFontSize`: spinbutton (8.0–18.0, step 0.5).
- `bodyLeading`: spinbutton (auto-suggested from font size; user can override).
- `bodyFont`: font picker, populated from PTXprint's available fonts list.
- `marginPreset`: tight / standard / generous (radio).
- Read-only display of resulting text-area dimensions (computed).
- Note: "Advanced layout options remain available in the main PTXprint interface after the wizard completes."

### 8.8 Review section

Three blocks:

1. **Summary** — every answer in a labelled list, grouped by section, each with an "Edit" link that jumps back.
2. **Estimates** — page count, spine width, cost L/M/H (per-copy and total), active warnings.
3. **Apply** — three buttons:
   - **Create new configuration** — prompts for a name; creates a new named PTXprint config and switches to it.
   - **Apply to current configuration** — shows a diff dialog (list of "setting X: oldValue → newValue") with confirm/cancel; on confirm, applies.
   - **Close without applying** — offers to save the wizard state for resume.

After apply, the wizard closes and the user is back in PTXprint with the configuration active; they can hit "generate PDF" themselves at any point.

---

## 9. Cost Estimation

- Inputs: relevant fields of `WizardState` plus `estimatedPageCount`.
- Engine walks `costRules.json` in order, returns the first match.
- Per-copy and total are independent; both can be `unknown` if no rule matches.
- Rules are intentionally coarse (L/M/H) so the JSON stays maintainable without market research.

---

## 10. Page Count Estimation

A heuristic, not a true layout. Inputs:
- Total source word count of selected books (PTXprint can already compute this; integration point).
- Trim size → text area width × height (lookup table in JSON).
- Body font size + leading → approximate words-per-page.
- Columns multiplier.
- Peripheral additions (sum of `estimatedPages` from catalogue).

Output: `estimatedPageCount: int`. Documented as approximate ±15%.

---

## 11. Integration Points with PTXprint

These are the places the coding LLM will need to plug into the existing PTXprint codebase. Each is marked **TODO(integrate)** in the generated code.

| Need | What's required from PTXprint |
|---|---|
| Read project's available books | Function returning list of `(usfmCode, checkStatus)` |
| Read project's check status per book | Function returning per-book status enum |
| Read project's available fonts | Existing font list |
| Read project's existing peripherals | Function returning which catalogue items are present in the project (e.g. has glossary file) |
| Read list of secondary projects (for diglot) | Existing project list |
| Apply settings to current config | Function `applyConfigDiff(configName, diffDict)` |
| Create named configuration | Function `createConfig(name, settings)` |
| Auto-launch on empty project | Hook in PTXprint's "project opened" event: if no config, call `WizardController.launch()` |
| Menu entry | Add "Setup Wizard..." to appropriate PTXprint menu, calling `WizardController.launch()` |
| Localisation | Use existing `_()` (or whatever PTXprint uses) for all user strings |
| Logger | Use existing logger |
| Save/resume state file location | Use PTXprint's per-project settings directory; filename `wizardState.json` |

---

## 12. SettingsMapper

A pure function: `WizardState → Dict[str, Any]` where the dict keys are PTXprint setting identifiers.

This module is the most PTXprint-specific piece. The coding LLM should generate a stub with one mapping function per logical group, **leaving the actual setting key names as TODOs for the maintainer to fill in**, since they are internal to PTXprint and not stable across versions.

Sketch:

```python
class SettingsMapper:
    def mapAll(self, state: WizardState) -> Dict[str, Any]:
        result = {}
        result.update(self._mapTrim(state))
        result.update(self._mapLayout(state))
        result.update(self._mapContent(state))
        result.update(self._mapPeripherals(state))
        return result

    def _mapTrim(self, s: WizardState) -> Dict[str, Any]:
        # TODO(integrate): map s.trimBinding.trimSize -> PTXprint paper size key
        # TODO(integrate): map s.trimBinding.paperType -> PTXprint paper colour/weight
        ...

    def _mapLayout(self, s: WizardState) -> Dict[str, Any]:
        # TODO(integrate): map columns, bodyFontSize, bodyLeading, bodyFont, marginPreset
        ...

    # etc.

    def computeDiff(self, currentConfig: Dict[str, Any], newSettings: Dict[str, Any]) -> List[Tuple[str, Any, Any]]:
        # returns [(key, oldValue, newValue), ...] for every change
        ...
```

---

## 13. Bundled Recipes (initial set)

| Recipe ID | Description |
|---|---|
| `trialNewTestament` | NT, ~50 copies, A5, perfect-bound, local printer, minimal peripherals. For community feedback. |
| `pewBible` | Whole Bible, ~500 copies, 6×9, double-column, POD service (IngramSpark), TOC + book intros + cross-refs. |
| `distributionBible` | Whole Bible, 5000+ copies, 6×9, double-column, offset, Bible paper, full apparatus (TOC, intros, x-refs, glossary, maps). |
| `pocketNewTestament` | NT, A6 or 4×6, single column, perfect-bound, POD or short-run digital. Compact for distribution. |
| `largePrintPsalms` | Psalms only, A5 or 6×9, single column, 14pt body, generous margins. For elderly readers. |
| `childrenScripturePortion` | Selected stories, A5, single column, 12pt body, illustrations enabled. |
| `diglotNewTestament` | NT in two parallel languages, two columns, perfect-bound, POD or short-run digital. |
| `studyBible` | Whole Bible, 1000+ copies, 7×10, double column, study notes + cross-refs + glossary + maps + concordance. |

---

## 14. Behaviours

### 14.1 Auto-launch
On project open, PTXprint checks: does this project have any saved config? If no → invoke `WizardController.launch(projectPath, autoLaunch=True)`. Auto-launch shows a "Skip wizard, set up manually" link prominently.

### 14.2 Save & Resume
- On any state change, debounce 500 ms, write `wizardState.json` to the project's settings dir.
- On launch, if `wizardState.json` exists, the recipe section offers "Resume previous setup" as the top option.
- A "Reset wizard" button on the recipe section clears saved state.

### 14.3 Backtracking
- Changing a field marks all sections that depend on it as `stale` (visible in sidebar).
- The user is not forced to revisit; the review section will list every active warning/error.
- Filter rules re-evaluate immediately, so combos refresh; if a previously-selected value is no longer allowed, it is cleared and the section's status drops to `inProgress`.

### 14.4 Apply outcomes
- **Create new config:** generates the new named config, switches PTXprint to it, closes wizard.
- **Apply to current:** shows diff dialog; on confirm, applies and closes.
- **Close without applying:** offers to save state for later resume.

### 14.5 Don't-show-again
A checkbox on the auto-launched recipe section: "Don't auto-launch the wizard for new projects." Stored in PTXprint user settings.

---

## 15. Error Handling

- Missing JSON file at startup → log error, disable wizard menu entry, do not crash PTXprint.
- Malformed JSON → load defaults, surface a warning in the wizard's status bar.
- PTXprint integration call failure (e.g. cannot list books) → section shows an inline error and a "Retry" button; wizard remains usable for other sections.
- Apply step failure → leave config unchanged, surface error, keep wizard open so user can retry or close.

---

## 16. Testing Hooks

- `WizardState` is fully serialisable → snapshot tests are trivial.
- `ConstraintsEngine`, `CostEstimator`, `PageCountEstimator` are pure functions of state + JSON → unit-testable without GTK.
- Each recipe should round-trip through the engine with no errors and produce a `complete` state in every section.

---

## 17. Out of Scope for v1

- Live PDF preview (use static thumbnail).
- Cost estimation in actual currency.
- Fetching recipes from a server.
- Editing peripherals from inside the wizard.
- Wizard-driven Paratext check runs.

---

## 18. Items the PTXprint maintainer must confirm before coding starts

1. Exact path under PTXprint's resources tree where `wizard/data/` should live.
2. Names of PTXprint config setting keys for: trim size, paper, columns, body font size, body leading, margins, content scope, diglot setup, peripheral toggles. (Listed as TODOs throughout.)
3. The exact API for "list books with check status" and "apply config diff."
4. Whether section icons should reuse existing PTXprint iconography or use a new set.
5. Whether the wizard window should be modal or non-modal.

---

*End of specification.*
