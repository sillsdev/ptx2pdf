# PTXprint UI Manual – writing guide

The manual is generated from two kinds of source: **facts read from the program itself**
(every control, its tooltip, its place in the window) and **explanations written by people (or AI)**
in `content/*.md`. This guide is for whoever writes or edits those explanations.

It produces, in `output/`:

* `PTXprint-Manual-for-AI.md` (+ `bot/*.md`, one file per chapter) – for the AI support bot.
* `PTXprint-User-Manual.html` – the manual for people: one self-contained page with a contents
  sidebar, search, and links between sections. It can be published as a website (for example with
  GitHub Pages). A PDF edition is also built (`PTXprint-User-Manual.pdf`, not kept in git).

## What is in git, and what is not

* **In git:** `content/*.md` (the only copy of the written explanations), the scripts in
  `python/scripts/uimanual/`, and the generated `output/` files above.
* **Not in git (made again whenever you build):** `data/` (the facts read from the program, and a
  per-chapter listing of every control with its Internal ID), `review/` and `sources/` (working
  notes).

## How it is built

1. `python python/scripts/uimanual/extract_ui.py` reads `ptxprint.glade`, `gtkview.py`,
   `modelmap.py` and `texpert.py` and writes `data/ui_map.json`: every control, its location,
   label, tooltip, view level, range/choices/default, and which other settings enable, disable or
   hide it.
2. `python python/scripts/uimanual/build_manual.py` combines that with `content/*.md` and writes
   `output/`. Add `--skeleton` to also write `data/chapters/<chapter>.md`, the generated listing of
   each chapter's controls (this is where you find each control's Internal ID and see exactly what
   is printed above a note). Add `--nopdf` to skip the slow PDF.
3. Read `output/build-report.txt`. It lists controls that have no explanation yet, and
   explanations whose control no longer exists. Fix every line it prints.

The chapters, the Parts they are grouped into, their order, and which tab or dialog belongs to
which chapter are all in `python/scripts/uimanual/chapters.py`. Chapter and section numbers are
made by the build; never type them.

## Updating the manual after the program changes

1. Run `extract_ui.py`, then `build_manual.py --skeleton`, and read the build report.
2. Write a note for each new control; delete notes for removed controls. Update the notes and
   text of controls whose tooltip, label, view level or behaviour changed.
3. Look for statements that are no longer true: "does nothing", "not used", "be careful", "no
   confirmation", "currently". Check each against the code, and remove or fix the ones that
   changed.
4. Rebuild, open the HTML and try a few links and the search box.

## Content file format

`content/<chapter-id>.md` – the chapter title (level 1 heading) is added by the build, so start at
level 2:

```markdown
## What this tab is for
...
## <One section per frame/area of the tab, using its on-screen name>
...
## Common tasks
...
## Common problems
...
## Control notes

### @c_mirrorpages
One or two sentences about this control...

### @s_fontsize
...
```

* `## Control notes` must be the **last** level-2 section and must be spelled exactly so. The
  prose-only chapters (introduction, getting started, how-to, problems, glossary) have none.
* Each note starts with `### @` followed by the exact Internal ID from `data/chapters/<id>.md`.
* Inside a note do **not** use `#` headings. Paragraphs, bullet lists and **bold** are fine.
* In the built manual each note is printed **after** the setting's heading, a line of facts (type,
  default, view level, values, "Needs", "Greyed out by" …) and its tooltip. So a note must
  **add** something: what the setting does in plain words, when to use it, a sensible value, what
  it interacts with, what to watch out for. Do not repeat the tooltip, the view level, the range or
  the dependency lines. For a trivial control ("OK", "Cancel") a few words are enough, but every
  control with an Internal ID still gets a note.

## Keep it compact

The manual is read mainly by an AI assistant, and every extra word costs. Start with the point.
Leave out "This setting allows you to…", "Note that…", "In other words…", "As mentioned above…".
Say a thing once, in the place the reader will look for it, and point to it from elsewhere.
Never remove a fact to save words.

## Who we are writing for

* People who use **only the PTXprint window**. Most are not technical. Many speak English as a
  second or third language.
* So: short sentences. Common words. Active voice ("Tick **Mirror Pages**", not "Mirror Pages
  should be ticked"). No idioms or jokes. One idea per sentence.
* Explain a technical word the first time it appears in a chapter (for example "gutter – the space
  between the two columns"), and add it to the glossary (`content/32-glossary.md`).
* Use the exact on-screen names in **bold**, and give the path:
  "On the **Layout** tab, in the **Page Setup** area, tick **Mirror Pages**."
* View levels are **Mini**, **Basic**, **Regular** and **Full** (Regular used to be called
  "Default"; "Default" now only means the Default configuration or a default value). If a setting
  is hidden at lower levels, say so: "(This is only shown in the **Full** view.)" Hidden settings
  still work, which is worth saying where it matters.
* If a setting is greyed out until another one is turned on, say which one.
* Use mm and pt as PTXprint does. Explain "pt" (point = about 0.35 mm) once per chapter where it
  matters.

## Links in the HTML edition

The HTML edition turns references into links automatically, so write them in a form it
recognises:

* **Tab and chapter names:** "the **Layout** tab", "the **Pictures** tab chapter", or a line
  ending a task: `See also: Layout tab; PDF Preview window.` (every name in a "See also:" line
  becomes a link). The names are the chapter titles, such as "Basic tab", "Main window",
  "PDF Preview window", "Importing settings".
* **Sections:** a section title in quotes or bold, for example `See "Compare PDFs" in this
  chapter.` or `see **Common problems**`, links to that section (the one in the same chapter
  wins).
* **Settings:** the exact on-screen label in bold, for example **Mirror Pages**, links to that
  setting's entry in the settings reference – but only when the label is unique. Very common words
  (Print, Save, Name, Basic …) are never linked.
* A target is linked once per heading block, so repeating a name does not clutter the page.

## Things we must never do

* **Never** tell users to edit `ptxprint.cfg`, `.sty`, `.tex` or other files outside PTXprint, run
  commands, or change the registry. Every instruction must be possible in the PTXprint window.
* Where PTXprint itself offers a text box or an editor for special codes (for example the front
  matter in **View+Edit**, header text fields, footnote callers, the Styles tab), it is fine to
  explain what to type there, step by step. Mark these as advanced.
* Do not invent features, defaults or behaviour. Check the code if a tooltip is unclear. If you
  cannot confirm something, leave it out.
* Do not write about mistakes in a tooltip ("ignore the tooltip text about…"). Fix the tooltip.

## Tooltips and labels

Tooltips and labels come from `ptxprint.glade` (and, for the Advanced › Other settings, from
`texpert.py`). If one is wrong, out of date, unclear or misspelt, fix it there – only the text,
never ids, signals or other properties – and rebuild. Anything that needs a decision (a rename, a
feature that does nothing) should be raised with the developers instead of being worked around in
the manual.
