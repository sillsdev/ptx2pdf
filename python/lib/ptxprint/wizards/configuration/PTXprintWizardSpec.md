# PTXprint Publication Wizard — Build Specification (v2)

| | |
|---|---|
| **Audience** | Coding agent implementing the wizard inside PTXprint |
| **Stack** | Python 3, PyGObject (GTK 3) + Glade |
| **Naming** | `camelCase` for all new identifiers (variables, functions, JSON keys, Glade IDs) |
| **Companion file** | `PTXprintWizardMatrix.xlsx` — authoritative settings matrix |
| **Working method** | ODD (Outcomes-Driven Development) — see §2 |
| **Spec version** | 2 — incorporates feedback from prototype walkthrough |

---

## 1. Purpose

A first-pass wizard that asks the user a small number of clear questions, then writes a coherent set of PTXprint configuration keys so the user reaches a working publication layout quickly.

The wizard does **not** aim to set every possible option — only the keys that meaningfully define the chosen layout. Everything else is left at PTXprint's defaults so the user can fine-tune later in the normal UI.

**Design ethos**

- Most users are not native English speakers. Every label, hint, description, and side-panel text uses short sentences, common words, and no PTXprint jargon.
- Beautiful, calm, uncluttered. One *topic* per page. Multiple short questions on one page are allowed when they are tightly related.
- Forgiving: every choice can be revisited; nothing is destructive until the final Apply.
- Explicit: when the wizard prefers or rejects an option, it shows *why*.
- Informative: every choice has a side panel explaining what each option means and why one might prefer it.

---

## 2. Epistemic ground rules (ODD axioms)

| Axiom | What it means here |
|---|---|
| **Reality Is Sovereign** | Before asserting that any PTXprint API exists, behaves a certain way, or that a config key has a certain effect — open the source file and observe. The matrix in `PTXprintWizardMatrix.xlsx` was built from `modelmap.py` and a sample `ptxprint.cfg`. The agent must re-verify against the *current* PTXprint repo at build time. |
| **A Claim Is a Debt** | Every "this layout sets X to Y" must trace to either (a) the matrix, or (b) a documented decision in this spec. No silently-invented defaults. If the agent is unsure of a value, it leaves the key untouched (PTXprint default applies) and adds the question to the follow-up list. |
| **Integrity Is Non-Negotiable Efficiency** | No "probably correct" guesses. If a tooltip would be technically wrong but more reassuring, write the technically correct one. Ship the slower version that works rather than the faster version that might not. |
| **You Cannot Verify What You Did Not Observe** | Every behavioural claim must be observed in the running system before the spec is treated as complete. The agent maintains a verification log (§13). |

When the spec says "MUST", "SHOULD", or "MAY" without citing a source, the agent treats that as an unverified claim and verifies it before relying on it.

---

## 3. High-level flow

```
  Welcome
     │
     ▼
  Intent group           (medium → stage → audience → product)
     │
     ▼
  Production group       (branches by medium)
     │   ├─ Print:    colour → budget/quality → page count → page size → printer → paper thickness
     │   └─ Digital:  screen target → colour → speed/quality
     ▼
  Layout & language      (diglot/interlinear; columns — auto-set if diglot)
     │
     ▼
  Summary                (review + Apply / Create new / Cancel)
```

**Step count for the user:**
- Print branch: ~9 visible pages (Welcome + 4 intent + 4 production + 1 layout + Summary).
- Digital branch: ~7 visible pages.

The wizard groups some related questions onto a single page where they fit comfortably (§5.1). The progress strip counts pages, not questions.

---

## 4. Architecture

### 4.1 File layout

```
ptxprint/
  wizard/
    __init__.py
    wizardController.py      # main controller, navigation, state
    wizardQuestions.json     # question tree (declarative, see §6)
    wizardQuestions.schema.json
    wizardState.py           # load / save / migrate per-publication state
    wizardMapping.py         # GENERATED: answers → PTXprint config keys
    wizardValidation.py      # cross-question warnings / gating / recommendations
    wizardStrings.py         # i18n string lookup (delegates to PTXprint helper)
    wizardSidePanel.py       # renders the per-step side panel
  glade/
    wizardDialog.glade       # custom GtkDialog with GtkStack
  tools/
    buildWizardMapping.py    # reads xlsx → emits wizardMapping.py
```

### 4.2 Dialog mechanism

Default to a custom `GtkDialog` containing a `GtkStack` for pages, plus a hand-built progress strip and footer. **TO VERIFY:** confirm `GtkAssistant`'s capabilities in the GTK 3 version PTXprint targets; if it cleanly supports branching, custom progress strips, and full keyboard control, prefer it. Otherwise the custom dialog stands.

### 4.3 Controller responsibilities

`WizardController` MUST:

1. Load `wizardQuestions.json` once at startup. Validate against the JSON schema. Fail loudly on schema violations.
2. Build pages dynamically from the page definitions. Pages of the same shape share a renderer; do not hard-code per-question widgets.
3. Maintain `answers: dict[str, Any]` keyed by `questionId`.
4. Re-evaluate **visibility, recommendations, and option ordering** on every answer change.
5. Persist `answers` to `wizardState.json` after every "Next" click and on Cancel.
6. On Apply / Create new, call `wizardMapping.applyAnswers(answers, ptxprintModel, target)`.
7. On Reset, delete `wizardState.json` and re-launch from page 1.
8. **Reset the scroll position to top on every page change** (§5.5).

### 4.4 State file location

```
<projectDir>/shared/ptxprint/<configName>/wizardState.json
```

One file per PTXprint config. **TO VERIFY:** path is writable in normal use. Fallback: `<userConfigDir>/ptxprint/wizardStates/<projectId>__<configName>.json`.

### 4.5 Re-entry

If `wizardState.json` exists when the wizard opens, the user lands on **page 1** with every field pre-filled. A "Skip to summary" link appears on page 1 only when state exists.

### 4.6 Reset

Quiet "Reset wizard" link in the footer of every page (not on Welcome). Clicking shows a confirmation modal:

> *"Start again from the beginning? Your current answers will be cleared."*

Buttons: **[Cancel]** *(default)*, **[Yes, start again]**.

---

## 5. Visual design

### 5.1 Page layout

Two-pane layout. Main pane carries the question(s); side panel carries explanation.

```
┌──────────────────────────────────────────────────────────────────┐
│  ●─●─●─○─○─○─○─○   Step 4 of 8                                   │  ← progress strip
│                                                                  │
│  ┌──────────────────────────────────┐  ┌──────────────────────┐  │
│  │  PAGE TITLE                      │  │  SIDE PANEL          │  │
│  │  Short helper sentence.          │  │                      │  │
│  │                                  │  │  Explains the        │  │
│  │  ┌────────────────────────────┐  │  │  currently selected  │  │
│  │  │  Question 1                │  │  │  / hovered option,   │  │
│  │  │  [option cards]            │  │  │  with pros and cons. │  │
│  │  └────────────────────────────┘  │  │                      │  │
│  │                                  │  │  Falls back to a     │  │
│  │  ┌────────────────────────────┐  │  │  static description  │  │
│  │  │  Question 2 (if grouped)   │  │  │  on simple steps.    │  │
│  │  │  [option cards]            │  │  │                      │  │
│  │  └────────────────────────────┘  │  └──────────────────────┘  │
│  └──────────────────────────────────┘                            │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│  Reset wizard       [Cancel]  [Apply]  [Create new]  [Back] [Next]│  ← footer
└──────────────────────────────────────────────────────────────────┘
```

Rules:

- **Topic per page, not question per page.** The wizard groups tightly-related short questions (e.g. "Diglot or interlinear?" + columns). Three is the absolute max per page.
- Main pane width ~520 px; side panel ~300 px; gutter between them.
- GTK theme default font everywhere. Heading: bold, ~1.3× body. Help text: regular, ~0.95× body, muted.
- Keyboard: **Enter** = Next; **Esc** = close (with confirm); **Alt+Left/Right** = Back/Next.

### 5.2 Side panel behaviour

Every page has a side panel.

- **For singleSelect / multiSelect questions with multiple meaningful options** (printer, binding, product type, page size, etc.): the panel updates as the user **hovers or focuses** an option. It shows: the option's full description, *pros* (bulleted), *cons* (bulleted), and (where relevant) the recommendation reason.
- **For sliders, ranges, or simple yes/no questions** where there are no meaningful per-option pros/cons: the panel shows a **static** explanation of what the question controls and how to think about the trade-off.
- The panel never empties. If neither hover nor focus is active, it shows the description of the *currently selected* option (or the question's default explanation).

Each option in the question tree carries `pros: [...]` and `cons: [...]` arrays for use here. Static-panel pages carry `staticPanel: "..."` text on the page node.

### 5.3 Recommendation states (replaces the old "disable + reason")

Every option in a `singleSelect` or `multiSelect` MAY be tagged with a recommendation level computed from current answers:

| Level | Visual | Selectable | Meaning |
|---|---|---|---|
| `recommended` | Small green check or accent border | Yes | Best fit for the user's earlier choices. |
| *(no level)* | Default | Yes | No recommendation rule fired. |
| `notOptimal` | Small orange warning icon, muted text | Yes | Possible but not the best choice. Reason shown in side panel. |
| `notAdvised` | Small red icon, struck-through label, muted | **No** | Not advised for the user's choices. Reason shown in side panel. |

There are **three** explicit levels (`recommended`, `notOptimal`, `notAdvised`). The "no level" state is the implicit default and renders the option normally.

When the user hovers a non-default-state option, the side panel shows the recommendation reason near the top, before pros/cons.

### 5.4 Progress strip

- Dots only. The "Step N of M" label sits next to the strip and is the authoritative count.
- **Tooltip on each dot is at most 1–2 words.** Examples: *"Audience"*, *"Printer"*, *"Page size"*. Never a full sentence.
- Already-answered dots are clickable (jump back). Future dots are not.

### 5.5 Scrolling

- Each page has its own independent scroll container. The window itself does not scroll.
- On every page change, the page's scroll position resets to the top.
- Scroll bars are always visible (`overlay-scrolling = false`) so users do not miss content below the fold.

### 5.6 Tone of voice

| ✗ Avoid | ✓ Use |
|---|---|
| "Specify the target output medium for your publication." | "Will this primarily be printed, or read on a screen?" |
| "Configure prepress settings appropriate to your print vendor." | "Where will this be printed?" |
| "Diglot configuration enables parallel multilingual layout." | "Two languages, side by side." |
| "Saddle-stitch binding is suitable for low page counts." | "Folded and stapled in the middle. Best for small books." |

Drafting rules:

- Prefer questions to commands.
- One idea per sentence. Maximum two sentences per hint.
- Avoid idioms, contractions, and Latinate words where a plainer alternative exists.
- Numbers: digits, no thousand-separators (so `5000`, never `5,000` or `5 000`). Always include the unit on first appearance ("500 copies"). The unit may be omitted on a slider's value-readout when the slider's label already names it.

### 5.7 Internationalisation

All user-visible strings come from `wizardQuestions.json` (or `wizardStrings.py` for non-question strings) and are wrapped with PTXprint's existing i18n helper at render time. **No strings hard-coded in Python.** Each string carries an optional `translatorNote`.

**TO VERIFY:** PTXprint's i18n helper name and call signature; reuse it.

### 5.8 Theming

The wizard inherits PTXprint's GTK theme. Custom colours only for:

- Progress strip's "filled" dot — theme accent colour.
- Recommendation badges — green / orange / red, theme-derived where possible.
- Muted help text — `theme_unfocused_fg_color`.

Fallback neutral grey: `#666` light / `#999` dark.

---

## 6. Question tree (`wizardQuestions.json`)

### 6.1 Top-level shape

```jsonc
{
  "version": 2,
  "pages": [ /* see §6.2 */ ]
}
```

The unit is now the **page**, not the question. A page contains one or more questions plus its side-panel content.

### 6.2 Page object

```jsonc
{
  "id": "intentMedium",
  "step": "intent",
  "titleString": "Will this be printed, or read on a screen?",
  "helpString": "Pick the way most people will use this. You can change anything later.",
  "tooltipString": "Output",
  "showIf": null,
  "staticPanel": null,
  "questions": [ /* see §6.3 */ ]
}
```

### 6.3 Question object

```jsonc
{
  "id": "outputMedium",
  "type": "singleSelect",
  "label": "",
  "translatorNote": "Top-level branch.",
  "required": true,
  "default": "print",
  "options": [
    {
      "id": "print",
      "label": "Primarily printed on paper",
      "description": "A book or booklet that will be printed.",
      "pros": ["Best for sharing physical copies.", "More layout control."],
      "cons": ["Costs money to print.", "Harder to update later."]
    },
    {
      "id": "digital",
      "label": "Read on a screen",
      "description": "A PDF for a phone, tablet, or computer.",
      "pros": ["Free to share.", "Easy to update."],
      "cons": ["Some people cannot read on screens."]
    }
  ],
  "affects": ["productionGroup"]
}
```

### 6.4 Question types

| `type` | Widget | Notes |
|---|---|---|
| `singleSelect` | Vertical list of large radio cards | Each card: label + 1-line description + recommendation badge if set. |
| `multiSelect` | Vertical list of checkbox cards | Optional `maxSelections` (e.g. 3 for audience). |
| `notchedSlider` | `GtkScale` with notch marks | `notches: [...]`; integer value below. No thousand-separators. |
| `centredSlider` | `GtkScale` with three labels | For "budget ↔ quality" / "speed ↔ quality". Centre = neutral default. |
| `dropdownDual` | Two adjacent dropdowns (mm + inches, gsm + lb) | Selecting either side updates the other. |
| `pageSizePicker` | Dropdown + side preview pane | Shows selected size as a filled rectangle on an A4 reference outline; preview lives in the side panel area. |

### 6.5 Visibility, recommendations, and ranking

Three independent primitives:

| Primitive | Where | Behaviour |
|---|---|---|
| `showIf` | Page or question | Hide entirely. |
| `recommendIf` | Per option | Tag with `recommended` / `notOptimal` / `notAdvised`. `notAdvised` is unselectable. |
| `rankBy` | Per question | Reorder options so promoted IDs float to top. Order otherwise stable. |

Example option block:

```jsonc
{
  "id": "homeInkjet",
  "label": "Home inkjet",
  "rangeLabel": "Best for 1–50 copies",
  "description": "A printer at home, for a few copies.",
  "pros": [
    "No setup cost.",
    "You control the timing."
  ],
  "cons": [
    "Slow for many copies.",
    "Ink is expensive over time.",
    "Cannot do thick books."
  ],
  "recommendIf": [
    { "level": "notOptimal",
      "when": { "answers": { "productType": { "in": ["pewBible","pastorsBible"] } } },
      "reason": "Pew and pastor's Bibles usually need many copies. A copy shop or print-on-demand service will be cheaper." }
  ]
}
```

Conditional defaults use the same primitives:

```jsonc
"default": {
  "rules": [
    { "if": { "answers": { "screenTarget": "phone" } }, "then": false },
    { "if": { "answers": { "diglotInterlinear": { "contains": "diglot" } } }, "then": true }
  ],
  "else": true
}
```

### 6.6 Schema validation

`wizardQuestions.schema.json` MUST be checked in alongside the data file. Controller validates on load. Failed validation aborts launch with a clear log entry and a "Wizard could not start" toast.

### 6.7 Concrete page list

#### Welcome (page 0)

Headline: *"Let's set up your publication."*
Body: *"A few quick questions, then PTXprint will pick good starting settings for you. You can change anything later."*
Buttons: **[Skip wizard]** *(quiet)*, **[Continue →]** *(primary)*.
Static panel: short explanation that this is a starting point, not a full configuration.

#### Page 1 — Output medium

Title: *"Will this primarily be printed, or read on a screen?"*
Help: *"Pick the way most people will use this."*
Tooltip: *"Output"*

Single question `outputMedium`:

| id | Label | Description |
|---|---|---|
| `print` | Primarily printed on paper | A book or booklet that will be printed. |
| `digital` | Read on a screen | A PDF for a phone, tablet, or computer. |

#### Page 2 — Publication stage

Title: *"Is this a finished version, or a draft?"*
Tooltip: *"Stage"*

Single question `publicationStage`:

| id | Label | Description |
|---|---|---|
| `prePublication` | A draft, during translation | A version for the team or community to read and check while translation is still going on. |
| `publicRelease` | A finished version | A final version for general use. |

#### Page 3 — Audience

Title: *"Who will mainly read this?"*
Help: *"Pick up to 3."*
Tooltip: *"Audience"*

Single question `audience`, type `multiSelect`, `maxSelections: 3`:

`children`, `youth`, `adults`, `pastors`, `churched`, `unchurched`, `lowVision`.

(Labels and descriptions are short and plain; full text in the JSON.)

#### Page 4 — Product type

Title: *"What kind of book are you making?"*
Tooltip: *"Product"*

Single question `productType`. Options depend on `publicationStage`. The selected `audience` re-ranks the list (most-likely first) but never hides options.

When `publicationStage = prePublication`:

| id | Label | Description |
|---|---|---|
| `teamCheck` | Team check | A draft for the translation team to review. |
| `communityCheck` | Community check | A draft for the wider community, including comprehension testing. |
| `consultantUns` | Consultant / UNS check | A draft for a translation consultant or for back-translation checking. |
| `exegeticalCheck` | Exegetical check | A draft focused on meaning, with notes and cross-references visible. |

When `publicationStage = publicRelease`:

| id | Label | Description | Note |
|---|---|---|---|
| `pewBible` | Pew Bible | A standard Bible for church use. Compact and affordable. | |
| `childrensBible` | Children's Bible | Larger text, pictures, simple layout. | |
| `pastorsBible` | Pastor's Bible | Smaller text, many cross-references and notes. | |
| `largePrintBible` | Large-print Bible | Big text and wide spacing for easier reading. | |
| `lifeApplicationBible` | Life Application Bible | Includes side notes and study material. | *Needs extra study material — add to the description.* |
| `journalingBible` | Journaling Bible | Wide outer margin with lines for writing. | |
| `lectionary` | Lectionary | A book of readings for church services. | |

Audience-driven ranking (recommended, not exclusive):

- `audience` contains `children` → promote `childrensBible`.
- `audience` contains `lowVision` → promote `largePrintBible`.
- `audience` contains `pastors` → promote `pastorsBible`.
- `audience` contains `unchurched` → promote `pewBible`, `lifeApplicationBible`.

#### Page 5 — Printer (PRINT branch only)

Title: *"Where will this be printed?"*
Help: *"Pick the kind of printer or service. The number of copies that fit each option is shown on the right."*
Tooltip: *"Printer"*

**This page replaces the old separate "How many copies?" question.** Volume is now communicated via each option's *range* label. Internally the wizard derives a `volumeBand` from the chosen printer for use by validation rules.

Single question `printer`:

| id | Label | Range label | Description |
|---|---|---|---|
| `homeInkjet` | Home inkjet | Best for 1–50 copies | A printer at home, for a few copies. |
| `officeLaser` | High-speed office laser | Best for 1–100 copies | A normal office printer. |
| `photocopyShop` | Local copy shop | Best for 1–200 copies | A nearby photocopy or print shop. |
| `podLow` | Print-on-demand (small runs) | Best for 1–200 copies | Online services that print one or a few copies. |
| `podHigh` | Print-on-demand (bigger runs) | Best for 50–500 copies | Online services with a minimum of around 50. |
| `offset` | Offset printing | Best for 500–5000 copies | A commercial press for big print runs. |

Each option carries pros/cons (already drafted in the JSON template).

`volumeBand` derivation (for downstream rules):

```
homeInkjet     → low
officeLaser    → low
photocopyShop  → mediumLow
podLow         → mediumLow
podHigh        → mediumHigh
offset         → high
```

#### Page 6 — Colour (PRINT branch)

Title: *"Inside pages — colour or black-and-white?"*
Tooltip: *"Colour"*

Single question `colour`: `colour`, `blackAndWhite`. Default: `blackAndWhite` for print.

Side panel: static. Explains that colour costs more, especially for inkjet, and that most Bibles are black-and-white inside.

#### Page 7 — Budget vs quality (PRINT branch)

Title: *"Lower cost, or better quality?"*
Tooltip: *"Budget"*

Single question `budgetQuality`, type `centredSlider`. Left = "Cheaper", centre = "Balanced", right = "Better quality". Default: centre.

Side panel: static. Explains the trade-off in plain terms (paper, balanced columns, etc.).

#### Page 8 — Page count (PRINT branch)

Title: *"About how many pages will the finished book have?"*
Tooltip: *"Pages"*

Single question `pageCount`, type `notchedSlider`.
Notches: `10, 20, 50, 100, 200, 500, 1000, 1500, 2000, 3000, 5000`. Logarithmic spacing. The slider snaps to the nearest notch when released. Value display: integer, no thousand-separators.

Side panel: static. Explains why this matters (binding feasibility, paper choice, spine width).

#### Page 9 — Page size (PRINT branch)

Title: *"How big will each page be?"*
Tooltip: *"Page size"*

Single question `pageSize`, type `pageSizePicker`. Options sorted small-to-large; full list is the union of every page size PTXprint already supports plus any standard sizes the agent confirms missing during build (verification step).

The dropdown shows each size as `<metric label> · <imperial label>` so both units are visible without a unit-toggle.

**Side panel for this page:** a visual preview. An A4 outline drawn at fixed scale on the panel's canvas; the currently selected size drawn filled (with theme accent at low alpha) inside it, anchored at the top-left corner. The aspect ratio of the selected size is preserved. Below the preview: the size's name plus its dimensions in both units.

**TO VERIFY:** the full list of page sizes already supported by PTXprint's paper-size dropdown.

#### Page 10 — Binding (PRINT branch)

Title: *"How will the pages be held together?"*
Tooltip: *"Binding"*

Single question `binding`. Recommendation level for each option is computed from `printer` (which determines `volumeBand`) and `pageCount`. The agent uses the `PrinterBindingCompat` sheet of `PTXprintWizardMatrix.xlsx` for the printer dimension and the page-count rules below for the page-count dimension.

Page-count rules (per binding):

| id | `notAdvised` when | `notOptimal` when |
|---|---|---|
| `saddleStitch` | `pageCount > 64` | `pageCount > 48` |
| `spiral` | `pageCount > 500` | `pageCount > 300` |
| `sideStitched` | `pageCount > 200` | — |
| `perfect` | `pageCount < 32` | `pageCount < 64` |
| `hardcover` | `pageCount < 64` | `pageCount < 100` |

If both dimensions place an option in different states, the **stricter** state wins (`notAdvised` > `notOptimal` > `recommended` > none). The agent **TO VERIFY** these page-count thresholds against PTXprint's existing cover/spine logic and may adjust during the verification pass.

#### Page 11 — Paper thickness (PRINT branch)

Title: *"How thick will the paper be?"*
Tooltip: *"Paper"*

Single question `paperThickness`, type `dropdownDual` (gsm + lb). The list of available papers is filtered by `printer`. Default: a sensible middle weight per printer.

**TO VERIFY:** PTXprint's existing paper-weight catalogue.

#### Pages 5d–7d — Digital branch

When `outputMedium = digital`, pages 5–11 above are skipped and replaced with:

##### Page 5d — Screen target

Title: *"What kind of screen will people read this on?"*
Tooltip: *"Screen"*

Single question `screenTarget`: `phone`, `tablet`, `pc`. Default: `tablet`.

##### Page 6d — Colour

As page 6, but default = `colour`.

##### Page 7d — Speed vs quality

Title: *"Faster output, or better-looking output?"*
Tooltip: *"Speed"*

Single question `speedQuality`, type `centredSlider`. Left = "Faster", centre = "Balanced", right = "Better quality". Default: centre.

#### Page 12 — Layout & language (BOTH branches)

Title: *"Layout"*
Help: *"A couple of last questions."*
Tooltip: *"Layout"*

Two questions on one page:

1. `diglotInterlinear`, type `multiSelect`, optional, no max:

   | id | Label | Description |
   |---|---|---|
   | `diglot` | Two languages, side by side | The text is shown in two languages, one beside the other. |
   | `interlinear` | Word-by-word translation | Each word has another language under or above it. |

2. `columns`, type `singleSelect`:

   | id | Label | Description |
   |---|---|---|
   | `single` | One column | All text in a single block down the page. |
   | `double` | Two columns | Two columns of text side by side. |

   Default: conditional. Single for `childrensBible`, `largePrintBible`, `journalingBible`, all pre-publication layouts, and digital with `screenTarget = phone`. Double otherwise.

   **`columns` is hidden** when `diglotInterlinear` contains `diglot`. A diglot publication is forced to a two-column layout (one language per column) and the question would be confusing; the wizard sets `paper/columns = True` automatically and shows a small note in the side panel: *"Two columns will be used automatically — one language per column."*

#### Page 13 — Summary

Title: *"Here's what you've chosen."*
Tooltip: *"Review"*

Read-only summary of every answered question, grouped by step. Each group has an "Edit" link that jumps back to the relevant page.

Above the action buttons, a **soft warnings banner** appears (yellow background) listing any cross-question oddness from `wizardValidation`. The banner is informational; it does not block any action.

Footer actions on this page (in addition to the always-on Cancel and Reset):

- **[Apply to current configuration]** — primary. Writes settings into the *active* PTXprint config (overwriting current values for the in-scope keys).
- **[Create new configuration]** — secondary. Prompts for a name; creates a new PTXprint configuration as a sibling of the current one (e.g. sibling of `Default`); switches the active configuration to the new one; then writes the wizard's settings into it.

Both buttons are disabled on every page except the Summary.

---

## 7. Footer and persistent buttons

### 7.1 Layout

```
  Reset wizard       [Cancel]   [Apply]   [Create new]   [Back]   [Next]
  └── always         └── always └─ Summary └─ Summary    └── always └── always
                                  page only  page only
```

- **Cancel** is shown on every page (not Welcome). Clicking shows a confirm modal. State *is* persisted on cancel so the user does not lose their answers if they cancel by mistake.
- **Apply** and **Create new** appear in the footer on every page but are *disabled* until the user reaches the Summary page. This keeps the user oriented (they can see where this is heading) without letting them shoot themselves in the foot.
- **Back** is hidden on Welcome and disabled on page 1.
- **Next** is hidden on the Summary page.

### 7.2 Apply behaviour

See §10.

---

## 8. Question tree primitives — full reference

### 8.1 Conditions (used in `showIf`, `recommendIf.when`, `default.rules.if`)

```jsonc
{ "answers": { "<questionId>": <matcher> } }
```

Matchers:

| Form | Matches when |
|---|---|
| literal value | answer === value |
| `{ "in": [...] }` | answer is in array |
| `{ "contains": "x" }` | answer (an array) contains x |
| `{ "lt": n }` | answer < n |
| `{ "gt": n }` | answer > n |
| `{ "between": [a, b] }` | a ≤ answer ≤ b |
| `{ "anyOf": [<cond>, ...] }` | any sub-condition true |
| `{ "allOf": [<cond>, ...] }` | all sub-conditions true |
| `{ "not": <cond> }` | sub-condition false |

### 8.2 Recommendation precedence

When multiple `recommendIf` rules fire on the same option, the strictest level wins. Strictness order: `notAdvised` > `notOptimal` > `recommended`.

### 8.3 Required answers

A question is required unless `required: false`. The Next button on a page is disabled until all required questions on that page have an answer.

---

## 9. Mapping answers to PTXprint config

### 9.1 Source of truth

`PTXprintWizardMatrix.xlsx` is authoritative. `wizardMapping.py` is **generated** from it by `tools/buildWizardMapping.py`. Regenerate when the xlsx changes.

### 9.2 Mapping structure

```python
LAYOUT_OVERRIDES = {
    "pewBible":             { "paper/columns": True,  "thumbtabs/ifthumbtabs": True, ... },
    "childrensBible":       { "paper/columns": False, "document/ifinclfigs": True,  ... },
    # ... one entry per layout (§6.7 Page 4)
}
MODIFIER_OVERRIDES = {
    "diglot":      { "document/ifdiglot": True, "poly/fraction": 50.0, ... },
    "interlinear": { "project/interlinear": True, ... },
    "sensitive":   { "document/sensitive": True },
    "colour":      { "snippets/pdfoutput": "PDF/X-4", "transparency_": "true", ... },
}
PRINTER_OVERRIDES = {
    "homeInkjet":   { ... },
    "officeLaser":  { ... },
    # ...
}
BINDING_OVERRIDES = {
    "saddleStitch": { ... },
    "perfect":      { "cover/makeCoverPage": True, "cover/includeSpine": True, ... },
    # ...
}
OUTPUT_MEDIUM_OVERRIDES = {
    "print":   { ... },
    "digital": { "snippets/pdfoutput": "Screen", "transparency_": "true", ... },
}
```

### 9.3 Application order (last-wins)

1. PTXprint defaults (no action — user's config is the base).
2. `OUTPUT_MEDIUM_OVERRIDES[outputMedium]`.
3. `LAYOUT_OVERRIDES[productType]`.
4. `MODIFIER_OVERRIDES[m]` for each selected modifier (`diglot`, `interlinear`, `sensitive` if pre-pub, `colour` if selected).
5. `PRINTER_OVERRIDES[printer]` (print only).
6. `BINDING_OVERRIDES[binding]` (print only).
7. Explicit `paper/columns` from the `columns` answer (or forced True if diglot).

### 9.4 Writing values

For each `(configKey, value)`, look up the widget ID in `ModelMap` and write through PTXprint's existing widget-set path. **Do not write the config file by hand** — the lambdas in `modelmap.py` translate config-file values to widget values and bypassing them creates silent inconsistencies.

**TO VERIFY:** the exact PTXprint API for "set this widget's value programmatically and trigger downstream effects". The agent finds it by reading PTXprint's existing config-load path and reusing that mechanism.

### 9.5 Computed values

- `cover/totalPages` ← `pageCount` answer.
- `cover/spinewidth` ← computed from `pageCount × paperThickness`. Use PTXprint's existing spine-width calculator if present (**TO VERIFY**); otherwise leave at default and add to follow-ups.
- `paper/pagesize` ← composed from `pageSize` answer (e.g. `"148mm, 210mm (A5)"`).

### 9.6 Refresh after apply

Trigger PTXprint's existing main-window UI-refresh hook. Verify by changing a setting, applying, and observing the main UI's widget reflects the new value without restart.

---

## 10. Apply / Create new behaviour

### 10.1 Pre-action checklist

Before writing anything, the controller MUST:

1. Confirm `answers` has values for every required question.
2. Confirm no option in `answers` is currently `notAdvised` (defensive — these should already be unselectable).
3. Run `wizardValidation`; collect soft warnings for the Summary banner. Warnings do not block.
4. Take an in-memory snapshot of the relevant config so a failed write can be rolled back.

### 10.2 Apply to current configuration

1. Compose overrides per §9.3.
2. For each `(configKey, value)`, write through the existing widget-set path.
3. Trigger main-window refresh.
4. Save `wizardState.json`.
5. Close the wizard.
6. Show a non-modal toast: *"Settings applied. You can fine-tune anything in the main window."*

### 10.3 Create new configuration

1. Prompt the user for a configuration name. Use PTXprint's existing config-name validation rules (**TO VERIFY** — same constraints as the existing "New configuration" feature).
2. If the name is invalid or already exists, show an inline error and let the user retry.
3. Call PTXprint's existing API for creating a new sibling configuration (**TO VERIFY**).
4. Switch the active configuration to the new one.
5. Then run §10.2 against the new configuration.
6. The success toast becomes: *"Created configuration «{name}» and applied your settings. You can fine-tune anything in the main window."*

### 10.4 Failure path

If any write throws:

1. Restore the snapshot from §10.1.4.
2. Do **not** save `wizardState.json` (so the user can retry).
3. Show an error dialog with the exception text and a "Copy details" button.
4. Leave the wizard open on the Summary page.
5. If a new configuration was created and the apply failed mid-way, also offer **[Delete the new configuration]** so the user is not left with an empty sibling.

---

## 11. Validation and warnings

### 11.1 Three feedback levels

| Level | Where shown | Example |
|---|---|---|
| **Recommendation badge** | On individual options inside the affected question | "Hardcover" tagged `notAdvised` when printer is home inkjet. |
| **Soft warning** | Yellow info banner on the Summary page | "You picked very thick paper with many pages. The book will be very heavy." |
| **None** (block) | — | The wizard never blocks Apply. |

### 11.2 Cross-question rules (`wizardValidation.py`)

Single home for cross-question logic. Returns `Warning(severity, questionIds, message)` objects. Examples:

- `pageCount > 1500 ∧ binding = saddleStitch` → "Saddle-stitch binding does not work for books this thick." (already enforced as `notAdvised` on the binding page; banner restates plainly.)
- `outputMedium = digital ∧ colour = blackAndWhite` → "Most digital readers can show colour. Are you sure you want black and white?"
- `productType = lifeApplicationBible` → reminder: "This layout uses extra study material. Make sure your project includes it before publishing."

The agent populates this list from the matrix's `PrintProduction`, `Layout`, and new `PrinterBindingCompat` sheets; do not invent constraints.

---

## 12. Persistence

### 12.1 State schema (`wizardState.json`)

```jsonc
{
  "version": 2,
  "savedAt": "2026-05-02T12:34:56Z",
  "ptxprintVersion": "3.x.y",
  "configName": "Default",
  "answers": {
    "outputMedium": "print",
    "publicationStage": "publicRelease",
    "audience": ["adults", "pastors"],
    "productType": "pastorsBible",
    "printer": "podHigh",
    "colour": "blackAndWhite",
    "budgetQuality": 0.6,
    "pageCount": 1500,
    "pageSize": { "mm": [148, 210], "label": "A5" },
    "binding": "perfect",
    "paperThickness": { "gsm": 60 },
    "diglotInterlinear": [],
    "columns": "double"
  }
}
```

### 12.2 Migration from v1

If `version: 1` is loaded, drop the `volume` field if present (no longer used) and add `version: 2`. Other fields carry over unchanged.

### 12.3 Not persisted

- Current page index (re-entry always lands on page 1).
- Highest-reached page (recomputed from `answers`).
- Scroll positions (per §5.5, always reset).

---

## 13. Implementation checklist for the coding agent

| # | Task | Verification |
|---|---|---|
| 1 | Read `modelmap.py` in the current PTXprint repo. Confirm every `configKey` referenced in the matrix still exists with the same widget ID. | Diff against `PTXprintWizardMatrix.xlsx`; record any drift in follow-ups. |
| 2 | Identify PTXprint's config-load code path. Note the function that "writes a value to a widget and fires downstream effects". | Call it from a test harness; observe the widget update. |
| 3 | Identify PTXprint's i18n helper. Note the call signature. | Call it from a throwaway script; observe a translated string. |
| 4 | Identify PTXprint's API for "create sibling configuration" and "switch active configuration". Note the validation rules for config names. | Manually create a sibling config via the API; observe the active config switch. |
| 5 | Decide GtkAssistant vs custom GtkDialog. | Test page 1 of each; pick whichever supports branching, custom progress strip, and full keyboard control. |
| 6 | Create `wizardQuestions.json` and `wizardQuestions.schema.json` from §6 and §8. | `jsonschema`-validate the JSON; commit both files. |
| 7 | Implement the renderer for each question `type` in §6.4, including the side panel (§5.2) and recommendation badges (§5.3). | Render every page once via a debug menu; screenshot each; eyeball against §5.1. |
| 8 | Implement `WizardController` (navigation, state, persistence, scroll reset). | Click through full Print and Digital branches; reload mid-wizard; observe state restored; observe scroll reset on every transition. |
| 9 | Implement `wizardValidation.py` (recommendations, soft warnings). | Force every gating condition; observe correct badges and banner messages. |
| 10 | Generate `wizardMapping.py` from the xlsx via `tools/buildWizardMapping.py`. | Spot-check 5 random `(layout, key, value)` triples against the xlsx. |
| 11 | Implement `applyAnswers` with snapshot/rollback for both Apply and Create-new. | Apply each layout to a fresh project; diff resulting `ptxprint.cfg` against an expected fixture; create + apply to sibling; observe active-config switch. |
| 12 | Wire the wizard into PTXprint's menu/launch UI. | Launch from the menu, reset, re-enter, skip, complete. |
| 13 | i18n pass: extract every string into the helper. | `grep` confirms zero hard-coded user-visible strings. |

---

## 14. Verification log

Per ODD axiom 4, the agent maintains `docs/wizardBuildVerificationLog.md` with rows of the form:

```
| Date | Claim | How verified | Outcome |
```

Every "TO VERIFY" tag in this spec MUST appear as a row before the wizard ships. Unverifiable items are recorded as such, and the affected feature is degraded gracefully.

---

## 15. Follow-up items (non-blocking)

### 15.1 Open design questions

1. **Lectionary advanced sub-config.** Lectionaries differ between RC, Anglican, and other traditions. The wizard treats lectionary as a single product type; a second-level branch (or a modal sub-form) is needed for cycle and pericope source. Out of scope for v1.
2. **Speed/quality slider mapping.** Currently maps to `paper/allowunbalanced` and `viewer/find*`. Candidate additions to consider: `document/picresolution`, `paragraph/ifhyphenate`. Pick after user testing.
3. **Audience overlap with product.** "Low vision" overlaps with "Large-print Bible". Current rule re-ranks but does not auto-select. Confirm with users.
4. **Confidence-flagged matrix cells.** ~20 cells flagged "M" (medium) or "L" (low) confidence need a sanity-check pass.
5. **Default config baseline.** The matrix's *Default* column was taken from one supplied `ptxprint.cfg`. If a fresh PTXprint project's defaults differ, the matrix needs updating.
6. **Page-count thresholds for binding.** The page-count rules in §6.7 Page 10 are conservative best-effort; verify against PTXprint's existing cover-spine logic and adjust.
7. **Printer × Binding compatibility.** First-pass matrix in `PTXprintWizardMatrix.xlsx` (sheet `PrinterBindingCompat`); needs a review by someone with field experience.

### 15.2 Verification stubs (TO VERIFY tags)

- §4.2 — `GtkAssistant` constraints in PTXprint's targeted GTK version.
- §4.4 — write-permissions on `<projectDir>/shared/ptxprint/<configName>/`.
- §5.7 — PTXprint's i18n helper name and signature.
- §6.7 Page 9 — full list of page sizes already supported by PTXprint's paper-size dropdown.
- §6.7 Page 10 — page-count thresholds against PTXprint's cover/spine logic.
- §6.7 Page 11 — PTXprint's paper-weight catalogue.
- §9.4 — exact API for "set widget programmatically + trigger downstream effects".
- §9.5 — existence of a spine-width calculator.
- §9.6 — main-window UI-refresh hook.
- §10.3 — "create sibling configuration" API and config-name validation rules.

### 15.3 Out of scope (deliberately)

- Generating an actual cover PDF.
- Setting fonts.
- Multi-project batch application.
- Importing settings from another project (PTXprint already has Import).

### 15.4 oddkit-canon item

The four ODD axioms (klappy.dev/canon/values/axioms.md, Klappy 2026) are integrated in §2 and §13–§14. If the canon evolves, this spec needs a corresponding update.

---

## Appendix A — Glossary

For non-native English readers building or testing the wizard.

| Term | Plain meaning |
|---|---|
| Diglot | Two languages shown side by side. |
| Interlinear | Words in one language with a translation written under each word. |
| Saddle-stitch | Folded in the middle and stapled. |
| Perfect-bound | Pages glued at the spine, like a paperback. |
| Lectionary | A book of Bible readings for church services, in the order they are read through the year. |
| gsm | Grams per square metre. A measure of how thick paper is. |
| Pew Bible | A standard Bible meant for church seating. |
| POD | Print-on-demand. Online services that print one or a few copies at a time. |
| UNS | Uninitiated Native Speaker. A person from the language community who has not been involved in the translation, used for comprehension testing. |

---

## Appendix B — Directory of artefacts

| File | Purpose | Source |
|---|---|---|
| `PTXprintWizardMatrix.xlsx` | Authoritative settings matrix | Companion deliverable |
| `wizardQuestions.json` | Declarative question + page tree | Built from §6 |
| `wizardQuestions.schema.json` | JSON schema | Built from §6 + §8 |
| `wizardState.json` | Per-publication saved answers | Runtime, written by controller |
| `wizardMapping.py` | Generated mapping dict | `tools/buildWizardMapping.py` reads the xlsx |
| `wizardDialog.glade` | Glade definition of the dialog shell | Hand-built per §5 |
| `docs/wizardBuildVerificationLog.md` | ODD verification log | Maintained by the agent |

---

## Appendix C — Summary of changes from v1

For reviewers comparing against the previous spec.

1. **Volume question removed.** Number-of-copies is now communicated via range labels on each printer card. `volume` is no longer in `answers`; a derived `volumeBand` is used internally.
2. **Recommendation system replaces disable-with-reason.** Three explicit levels (`recommended`, `notOptimal`, `notAdvised`); only `notAdvised` is unselectable.
3. **Side panel on every page.** Dynamic pros/cons for option-pickers; static description for sliders and simple inputs.
4. **Pages, not single questions.** Tightly-related questions can share a page; tree's top-level unit is now `page`. Diglot/interlinear and columns share a page.
5. **Diglot suppresses columns question.** Diglot forces double-column; the columns question is hidden.
6. **A4 reference preview** for page size.
7. **Per-page scroll containers**, scroll resets on page change, scroll bars always visible.
8. **Progress-strip tooltips capped at 1–2 words.**
9. **No thousand-separators in any number.**
10. **Apply / Create new / Cancel buttons in persistent footer**, disabled until Summary except Cancel.
11. **Pre-publication described as "during translation".**
12. **Audience-product overlap softened** by re-ranking with a `recommended` badge instead of just sorting.
13. **Audience max stays at 3.**
14. **Printer ranges:** home-inkjet 1–50; office-laser 1–100; copy-shop 1–200; POD-low 1–200; POD-high 50–500; offset 500–5000.
15. **Binding now gated by both `pageCount` and `printer`** (via `volumeBand`); see new `PrinterBindingCompat` sheet in the matrix.
