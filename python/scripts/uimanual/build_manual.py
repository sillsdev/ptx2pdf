#!/usr/bin/env python3
r"""
Build the PTXprint user manual from:
    docs/uimanual/data/ui_map.json     (made by extract_ui.py - always re-run that first)
    docs/uimanual/content/*.md         (explanations written for each chapter)

Writes to docs/uimanual/output/:
    PTXprint-Manual-for-AI.md          one file containing everything (for the support bot)
    bot/<chapter>.md                   the same content, one file per chapter
    PTXprint-User-Manual.html          the human-readable manual
    PTXprint-User-Manual.pdf           the same, as PDF (needs PyMuPDF and markdown-it-py)
    build-report.txt                   controls with no explanation, orphan notes, etc.

Content files: each docs/uimanual/content/<chapter-id>.md holds the prose for a chapter,
starting at heading level 2 (the build adds the chapter title as level 1). An optional last
section headed exactly "## Control notes" holds per-control explanations, each starting with
a level 3 heading of the form "### @widget_id". These notes are merged into the generated
settings reference, so a renamed or deleted widget is reported rather than silently kept.

Usage:
    python python/scripts/uimanual/extract_ui.py
    python python/scripts/uimanual/build_manual.py [--nopdf] [--skeleton]
"""

import argparse
import datetime
import html
import json
import os
import re
import sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chapters import chapters, chapterFor

levelShort = {2: "Mini+", 4: "Basic+", 5: "Regular+", 6: "Full"}

typeShort = {"Radio button": "Radio", "Number box": "Number", "Drop-down list": "Drop-down",
             "Toggle button": "Toggle", "Colour picker": "Colour"}

botPreface = """\
## Notes for the AI support assistant

* This manual covers every setting in the PTXprint window: chapters explain each tab, then a
  *Settings reference* lists every control under headings that give its location
  (tab or dialog › area › setting).
* Most users are **not technical**, and many speak English as a second or third language. Answer in
  short, simple sentences with click-by-click steps, using the on-screen names exactly as written here.
* **Never tell users to edit ptxprint.cfg, .sty or .tex files, or run commands.** Every answer must
  work in the PTXprint window. If something cannot be done there, say so and suggest
  ptxprint_support@sil.org.
* If a user cannot find a setting, check its view level: many settings are hidden in the Mini and
  Basic views (see "View levels"). Some settings are greyed out or hidden until another one is turned on.

### How to read a setting

```
##### <on-screen label>
<type>[, on/off by default] · <view level> · `<internal ID>` · cfg `<config key>`
<extra facts, separated by ·>
> <tooltip>
<explanation>
```

* **View level** – the lowest view that shows it: `Mini+` (all views), `Basic+`, `Regular+`, or
  `Full` (Full view only). `not shown` = hidden in all views; `experimental` = only in experimental mode.
* **Extra facts** – `Values:` range and default · `Choices:` options in a list · `Also:` the setting's
  descriptive name · `Beside:` the label next to it · `Needs:` only usable when that setting is on/selected ·
  `Greyed out by:` unusable while that setting is ticked · `Hidden until:` that box is ticked ·
  `Shown when:` the tab/area appears when that box is ticked.
* Quoted text (`>`) is the tooltip; the paragraph after it is a plain-language explanation.
* The internal ID and config key are for support staff, to match a line in a user's settings file or
  log to the place in the window. Do not ask users about them.
"""


def stripColon(s):
    if s is None:
        return None
    return s.strip().rstrip(":：").strip()


def controlTitle(c):
    """The on-screen label. A control with no label of its own borrows the label beside it, which is
    often a row or column heading shared by several controls, so its descriptive name is added."""
    own = stripColon(c.get("label"))
    beside = stripColon(c.get("fieldLabel"))
    name = c.get("name")
    if own:
        return own
    if beside and name and name.lower() != beside.lower():
        return f"{beside} – {name}"
    prim = beside or name
    if not prim:
        tip = (c.get("tooltip") or "").strip().split("\n")[0]
        prim = (tip[:60] + "...") if len(tip) > 60 else tip
    if not prim:
        prim = c.get("id") or "(unnamed)"
    return prim


def mdEscape(s):
    s = s.replace("\\", "\\\\")
    for ch in "*_`[]<>":
        s = s.replace(ch, "\\" + ch)
    s = re.sub(r"(?m)^(\s*)([#+\-]|\d+\.)(\s)", lambda m: m.group(1) + "\\" + m.group(2) + m.group(3), s)
    return s


def quoteBlock(text, human):
    if human:
        text = mdEscape(text)
    lines = []
    for para in text.split("\n\n"):
        pl = para.split("\n")
        lines.append("  \n".join("> " + l.rstrip() if l.strip() else ">" for l in pl))
    return "\n>\n".join(lines)


def depText(lst):
    return ", ".join("“{}”".format(stripColon(d.get("label")) or d["id"]) for d in lst)


def renderControl(c, note, human, hlevel="#####"):
    """One setting: heading, a compact facts line (or two), the tooltip as a quote, then the explanation."""
    title = controlTitle(c)
    esc = mdEscape if human else (lambda s: s)
    out = [f"{hlevel} {esc(title)}", ""]

    # line 1: type, default state, view level, ids
    typ = typeShort.get(c["type"], c["type"])
    if c.get("defaultOn") is not None and c["type"] in ("Checkbox", "Toggle button"):
        typ += ", on" if c["defaultOn"] else ", off"
    first = [typ]
    if c.get("visibility") == "hidden":
        first.append("not shown")
    elif c.get("visibility") == "experimental":
        first.append("experimental")
    elif c.get("viewLevel"):
        first.append(levelShort[c["viewLevel"]])
    if not human:
        if c.get("id"):
            first.append(f"`{c['id']}`")
        keys = [k for k in (c.get("configKeys") or []) if "/" in k]    # skip template-only values like 'majorcolor_'
        if keys:
            first.append("cfg " + ", ".join(f"`{k}`" for k in keys))

    # line 2: everything else that applies
    facts = []
    r = c.get("range")
    if r and r.get("lower") is not None and r.get("upper") is not None:
        v = "{:g}–{:g}".format(r["lower"], r["upper"])
        if r.get("default") is not None:
            v += " (default {:g})".format(r["default"])
        facts.append("Values: " + v)
    texts = [x["text"] for x in (c.get("choices") or []) if x.get("text")]
    if texts:
        facts.append("Choices: " + " | ".join(esc(t) for t in texts))
    nm = c.get("name")
    if nm and nm.lower() not in title.lower():
        facts.append("Also: " + esc(nm))
    if c.get("fieldLabel") and c.get("label") and stripColon(c["fieldLabel"]) != title:
        facts.append("Beside: " + esc(stripColon(c["fieldLabel"])))
    if c.get("enabledBy"):
        facts.append("Needs: " + depText(c["enabledBy"]))
    if c.get("disabledBy"):
        facts.append("Greyed out by: " + depText(c["disabledBy"]))
    if c.get("collapsedUntil"):
        facts.append("Hidden until: " + depText([c["collapsedUntil"]]))
    if c.get("tabShownBy"):
        facts.append("Shown when: " + depText(c["tabShownBy"]))
    lines = [" · ".join(first)]
    if facts:
        lines.append(" · ".join(facts))
    out.append("  \n".join(lines))
    out.append("")
    if c.get("tooltip"):
        out.append(quoteBlock(c["tooltip"], human))
        out.append("")
    if note:
        out.append(note.strip())
        out.append("")
    return "\n".join(out)


def stripTab(s):
    """'Layout tab' -> 'Layout'; keeps dialog names as they are."""
    return s[:-4] if s.endswith(" tab") else s


def renderReference(ctrls, notes, human):
    """Settings reference as a tree: ### tab/dialog, #### area, ##### sub-area; settings one level deeper."""
    esc = mdEscape if human else (lambda s: s)
    tree = OrderedDict()            # path tuple -> list of controls, in order of first appearance
    for c in ctrls:
        if human and c.get("visibility") in ("hidden", "experimental"):
            continue
        path = tuple(c["breadcrumbs"]) or ("Other",)
        if len(path) > 3:           # headings stop at level 5; join anything deeper
            path = path[:2] + (" › ".join(path[2:]),)
        tree.setdefault(path, []).append(c)
    # order paths so that all children of a heading follow it
    order, seen = [], {}
    for path in tree:
        for i in range(1, len(path) + 1):
            seen.setdefault(path[:i], len(seen))
    out, done = [], set()
    for path in sorted(tree, key=lambda p: [seen[p[:i]] for i in range(1, len(p) + 1)]):
        for i in range(1, len(path) + 1):
            if path[:i] not in done:
                done.add(path[:i])
                out.append(f"{'#' * (2 + i)} {esc(stripTab(path[i - 1]))}\n")
        for c in tree[path]:
            out.append(renderControl(c, notes.get(c["id"]) if c["id"] else None, human,
                                     hlevel="#" * (3 + len(path))))
    return "\n".join(out)


def numberSections(prose, num):
    """Number the level-2 headings of a chapter: '## Margins' -> '## 4.3 Margins'. Returns text and titles."""
    titles = []
    infence = False
    lines = prose.split("\n")
    for i, l in enumerate(lines):
        if l.startswith("```"):
            infence = not infence
        elif not infence and l.startswith("## "):
            titles.append(l[3:].strip())
            lines[i] = f"## {num}.{len(titles)} {l[3:].strip()}"
    return "\n".join(lines), titles


def parseContent(path):
    """Return (prose, notes dict)."""
    if not os.path.exists(path):
        return None, {}
    text = open(path, encoding="utf-8").read()
    notes = OrderedDict()
    m = re.search(r"(?m)^## Control notes\s*$", text)
    if m:
        prose = text[:m.start()].rstrip()
        rest = text[m.end():]
        for blk in re.split(r"(?m)^### @", rest)[1:]:
            ident, _, body = blk.partition("\n")
            notes[ident.strip()] = body.strip()
    else:
        prose = text.rstrip()
    return prose, notes


def build(repo, dopdf=True, skeleton=False):
    base = os.path.join(repo, "docs", "uimanual")
    data = json.load(open(os.path.join(base, "data", "ui_map.json"), encoding="utf-8"))
    controls = data["controls"]
    bych = OrderedDict((c[0], []) for c in chapters)
    unassigned = []
    for c in controls:
        cid = chapterFor(c["breadcrumbs"])
        if cid is None:
            unassigned.append(c)
        else:
            bych[cid].append(c)

    report = []
    allIds = {c["id"] for c in controls if c["id"]}
    outdir = os.path.join(base, "output")
    os.makedirs(os.path.join(outdir, "bot"), exist_ok=True)
    if skeleton:
        os.makedirs(os.path.join(base, "data", "chapters"), exist_ok=True)
    today = datetime.date.today().isoformat()
    botParts = [f"# PTXprint User Interface Manual (AI support edition)\n\nGenerated {today} from the PTXprint "
                f"source code and the explanations in docs/uimanual/content.\n\n{botPreface}"]
    humanParts = [f"# PTXprint User Manual\n\nGenerated {today}.\n"]
    chapterTexts = {False: [], True: []}
    contents = ["## Contents", ""]
    num = 0
    for cid, title, places in chapters:
        prose, notes = parseContent(os.path.join(base, "content", cid + ".md"))
        ctrls = bych[cid]
        for k in notes:
            if k not in allIds:
                report.append(f"{cid}: note for unknown widget id '{k}'")
            elif not any(c["id"] == k for c in ctrls):
                report.append(f"{cid}: note for '{k}' which belongs to another chapter")
        hasContent = prose is not None
        if not prose and not ctrls:
            continue
        num += 1
        prose, secTitles = numberSections(prose or "", num)
        refnum = f"{num}.{len(secTitles) + 1}"
        contents.append(f"{num}. **{title}**")
        subs = [f"{num}.{i + 1} {t}" for i, t in enumerate(secTitles)]
        if ctrls:
            where = OrderedDict((stripTab(c["breadcrumbs"][0]), 1) for c in ctrls if c["breadcrumbs"])
            subs.append(f"{refnum} Settings reference ({', '.join(where)})")
        contents.extend(f"   - {s}" for s in subs)
        for human in (False, True):
            parts = [f"# {num}. {title}", ""]
            if prose:
                parts.append(prose)
                parts.append("")
            if ctrls:
                parts.append(f"## {refnum} Settings reference")
                parts.append("")
                parts.append(renderReference(ctrls, notes, human))
            text = "\n".join(parts).rstrip() + "\n"
            chapterTexts[human].append(text)
            if not human:
                with open(os.path.join(outdir, "bot", cid + ".md"), "w", encoding="utf-8") as outf:
                    outf.write(text)
                if skeleton and ctrls:
                    with open(os.path.join(base, "data", "chapters", cid + ".md"), "w", encoding="utf-8") as outf:
                        outf.write(text)
        missing = [c["id"] for c in ctrls if c["id"] and c["id"] not in notes and c.get("visibility") is None]
        if missing and hasContent:
            report.append(f"{cid}: {len(missing)} controls without a note: " + " ".join(missing))
        elif not hasContent:
            report.append(f"{cid}: no content file yet ({len(ctrls)} controls)")
    if unassigned:
        report.append("Controls not assigned to any chapter: " +
                      ", ".join(f"{c['id']} [{' > '.join(c['breadcrumbs'])}]" for c in unassigned))

    contentsText = "\n".join(contents) + "\n"
    botParts += [contentsText] + chapterTexts[False]
    humanParts += [contentsText] + chapterTexts[True]
    botText = "\n\n".join(botParts)
    with open(os.path.join(outdir, "PTXprint-Manual-for-AI.md"), "w", encoding="utf-8") as outf:
        outf.write(botText)
    humanText = "\n\n".join(humanParts)
    with open(os.path.join(outdir, "build-report.txt"), "w", encoding="utf-8") as outf:
        outf.write("\n".join(report) + "\n")
    print("\n".join(r[:300] for r in report))
    reviewDir = os.path.join(base, "review")
    if os.path.isdir(reviewDir):
        revs = [f"# Tooltip and UI issues found while writing the manual\n\nGenerated {today}. "
                "One section per chapter; IDs refer to ptxprint.glade.\n"]
        for f in sorted(os.listdir(reviewDir)):
            if f.endswith(".md"):
                txt = open(os.path.join(reviewDir, f), encoding="utf-8").read()
                txt = re.sub(r"(?m)^(#+)", r"#\1", txt)     # demote headings under the file heading
                revs.append(f"## {f[:-3]}\n\n{txt.strip()}\n")
        with open(os.path.join(outdir, "Tooltip-Issues.md"), "w", encoding="utf-8") as outf:
            outf.write("\n\n".join(revs))
    htmlText = makeHtml(humanText)
    with open(os.path.join(outdir, "PTXprint-User-Manual.html"), "w", encoding="utf-8") as outf:
        outf.write(htmlText)
    if dopdf:
        makePdf(htmlText, os.path.join(outdir, "PTXprint-User-Manual.pdf"))
    print(f"Wrote {outdir}")


css = """
body { font-family: sans-serif; font-size: 10pt; line-height: 1.35; color: #222; }
h1 { font-size: 20pt; color: #1b4f8a; margin-top: 0; padding-bottom: 4pt; border-bottom: 2px solid #1b4f8a; page-break-before: always; }
h2 { font-size: 15pt; color: #1b4f8a; margin-top: 16pt; }
h3 { font-size: 12pt; color: #2e6db4; margin-top: 12pt; }
h4 { font-size: 10.5pt; color: #000; margin-top: 10pt; margin-bottom: 2pt; background-color: #eef3fa; padding: 2pt; }
blockquote { margin-left: 10pt; padding-left: 6pt; color: #444; font-style: italic; border-left: 2px solid #bbb; }
code { font-family: monospace; font-size: 9pt; }
ul, ol { margin-top: 2pt; margin-bottom: 4pt; }
li { margin-bottom: 1pt; }
table { border-collapse: collapse; }
td, th { border: 1px solid #aaa; padding: 2pt 4pt; vertical-align: top; }
th { background-color: #eef3fa; }
"""


def makeHtml(mdText):
    from markdown_it import MarkdownIt
    md = MarkdownIt("commonmark").enable("table").enable("strikethrough")
    body = md.render(mdText)
    return ("<!DOCTYPE html>\n<html><head><meta charset='utf-8'><title>PTXprint User Manual</title>"
            f"<style>{css}</style></head><body>\n{body}\n</body></html>\n")


def makePdf(htmlText, outpath):
    try:
        import fitz
    except ImportError:
        print("PyMuPDF (fitz) is not installed: skipping PDF")
        return
    body = re.sub(r"(?s)^.*<body>|</body>.*$", "", htmlText)
    # first h1 is the cover title: don't break before it
    body = body.replace("<h1>", "<h1 style='page-break-before: avoid'>", 1)
    story = fitz.Story(html=body, user_css=css)
    mediabox = fitz.paper_rect("a4")
    where = mediabox + (50, 50, -50, -60)
    toc = []

    def recorder(pos):
        if pos.heading in (1, 2, 3) and pos.open_close & 1 and pos.text:
            toc.append([pos.heading, pos.text.strip(), pos.page_num, pos.rect[1]])

    import io
    tmp = io.BytesIO()
    writer = fitz.DocumentWriter(tmp)
    more = 1
    pno = 0
    while more:
        dev = writer.begin_page(mediabox)
        more, _ = story.place(where)
        story.element_positions(recorder, {"page_num": pno})
        story.draw(dev)
        writer.end_page()
        pno += 1
    writer.close()
    doc = fitz.open("pdf", tmp.getvalue())
    for i, page in enumerate(doc):
        if i > 0:
            page.insert_text((mediabox.width / 2 - 10, mediabox.height - 30), str(i + 1), fontsize=9, color=(0.4, 0.4, 0.4))
    outline = []
    for lvl, text, pg, y in toc:
        if not outline and lvl > 1:
            lvl = 1
        while outline and lvl > outline[-1][0] + 1:
            lvl -= 1
        outline.append([lvl, text, pg + 1, {"kind": fitz.LINK_GOTO, "page": pg, "to": fitz.Point(0, y), "zoom": 0}])
    try:
        doc.set_toc([o[:3] for o in outline])
    except Exception as e:
        print(f"Could not set PDF bookmarks: {e}")
    doc.set_metadata({"title": "PTXprint User Manual", "author": "PTXprint team", "subject": "PTXprint user interface"})
    doc.save(outpath, garbage=3, deflate=True)
    doc.close()
    print(f"Wrote {outpath} ({pno} pages)")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.abspath(os.path.join(here, "..", "..", ".."))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=repo)
    ap.add_argument("--nopdf", action="store_true", help="Skip making the PDF")
    ap.add_argument("--skeleton", action="store_true", help="Also write per-chapter control listings to data/chapters/")
    args = ap.parse_args()
    build(args.repo, dopdf=not args.nopdf, skeleton=args.skeleton)


if __name__ == "__main__":
    main()
