#!/usr/bin/env python3
r"""
Build the PTXprint user manual from:
    docs/uimanual/data/ui_map.json     (made by extract_ui.py - always re-run that first)
    docs/uimanual/content/*.md         (explanations written for each chapter)

Writes to docs/uimanual/output/:
    PTXprint-Manual-for-AI.md          one file containing everything (for the support bot)
    bot/<chapter>.md                   the same content, one file per chapter
    PTXprint-User-Manual.html          the human-readable manual
    PTXprint-User-Manual.md            the same, as one Markdown file, with the HTML edition's heading ids
                                       ("Title {#id}") and cross-reference links, for typesetting
    PTXprint-User-Manual.pdf           that Markdown typeset by PTXprint itself (docs/uimanual/ptx; not
                                       kept in git: the release builds make it with the program they built)
    build-report.txt                   controls with no explanation, orphan notes, etc.

Content files: each docs/uimanual/content/<chapter-id>.md holds the prose for a chapter,
starting at heading level 2 (the build adds the chapter title as level 1). An optional last
section headed exactly "## Control notes" holds per-control explanations, each starting with
a level 3 heading of the form "### @widget_id". These notes are merged into the generated
settings reference, so a renamed or deleted widget is reported rather than silently kept.

Usage:
    python python/scripts/uimanual/extract_ui.py
    python python/scripts/uimanual/build_manual.py [--nopdf] [--skeleton]
    python python/scripts/uimanual/build_manual.py --pdf-only [--ptxprint PTXprint.exe] [--out dir]
"""

import argparse
import datetime
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chapters import chapters, chapterFor, orderedChapters, partOf
from chapters import parts as partList
import htmlmanual
import mdwriter

levelShort = {2: "Mini+", 4: "Basic+", 5: "Regular+", 6: "Full"}
levelHuman = {2: "all views", 4: "Basic, Regular and Full views", 5: "Regular and Full views", 6: "Full view only"}

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
    marker = f" {{#{htmlmanual.ctrlAnchor(c['id'])}}}" if human and c.get("id") else ""
    out = [f"{hlevel} {esc(title)}{marker}", ""]

    # line 1: type, default state, view level, ids
    if human:       # words, not the shorthand of the AI edition
        typ = c["type"]
        if c.get("defaultOn") is not None and c["type"] in ("Checkbox", "Toggle button"):
            typ += " (ticked by default)" if c["defaultOn"] else " (not ticked by default)"
        first = [typ]
        if c.get("visibility") == "hidden":
            first.append("not normally shown")
        elif c.get("visibility") == "experimental":
            first.append("experimental")
        elif c.get("viewLevel"):
            first.append("shown in: " + levelHuman[c["viewLevel"]])
    else:
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
    chapterInfos = []
    lastPart = None
    for cid, title, places in orderedChapters():
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
        if partOf(cid) != lastPart:
            lastPart = partOf(cid)
            contents += ["", f"**Part {lastPart + 1}: {partList[lastPart][0]}** – {partList[lastPart][1]}", ""]
        contents.append(f"{num}. **{title}**")
        subs = [f"{num}.{i + 1} {t}" for i, t in enumerate(secTitles)]
        if ctrls:
            where = OrderedDict((stripTab(c["breadcrumbs"][0]), 1) for c in ctrls if c["breadcrumbs"])
            subs.append(f"{refnum} Settings reference ({', '.join(where)})")
        contents.extend(f"    - {s}" for s in subs)
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
            if human:
                chapterInfos.append(dict(cid=cid, num=num, title=title, part=partOf(cid), text=text))
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
    ctrlKeys = []
    for c in controls:
        if c.get("id") and not c.get("visibility"):
            own = stripColon(c.get("label"))
            keys = [own] if own else [stripColon(c.get("fieldLabel"))]
            ctrlKeys.append(dict(anchor=htmlmanual.ctrlAnchor(c["id"]), keys=[k for k in keys if k]))
    pageHtml, linker = htmlmanual.build(chapterInfos, ctrlKeys, partList, "PTXprint User Manual", today)
    with open(os.path.join(outdir, "PTXprint-User-Manual.html"), "w", encoding="utf-8") as outf:
        outf.write(pageHtml)
    print(f"HTML edition: {len(chapterInfos)} chapters, {linker.count} cross-reference links")
    linkedMd, mdLinks = makeLinkedMarkdown(humanParts[0], chapterInfos, ctrlKeys)
    with open(os.path.join(outdir, "PTXprint-User-Manual.md"), "w", encoding="utf-8") as outf:
        outf.write(linkedMd)
    print(f"Linked Markdown edition: {mdLinks} cross-reference links")
    if mdLinks != linker.count:
        print(f"Warning: the Markdown edition has {mdLinks} links but the HTML edition {linker.count}")
    if dopdf:
        makePdf(repo, os.path.join(outdir, "PTXprint-User-Manual.pdf"))
    print(f"Wrote {outdir}")


def makeLinkedMarkdown(preamble, chapterInfos, ctrlKeys):
    """The human edition as one Markdown file, with the HTML edition's heading ids ("Title {#id}") and
    cross-reference links, for typesetting. preamble (the title) is written as it is, then a contents
    list whose entries link to the chapters and their sections."""
    chapters, linker = htmlmanual.linkedChapters(chapterInfos, ctrlKeys)
    parts = [typesetSettings, preamble.rstrip("\n") + "\n", linkedContents(chapters)]
    parts += [mdwriter.tokensToMarkdown(ch.tokens) for ch in chapters]
    return "\n".join(parts), linker.count


# How PTXprint (markdown.py) typesets the linked edition: h1 (chapter) is \ms1, h2 \s1, h3 \s2 ... and
# headings down to level 3 are PDF bookmarks
typesetSettings = """---
book: XXA
headings: ms1 s1
outline: 3
---
"""


def linkedContents(chapters):
    """The contents (as in the other editions: parts, chapters, their sections) with every entry a link"""
    esc = mdwriter.escapeText
    out = ["## Contents {#contents}", ""]
    lastPart = None
    for ch in chapters:
        if ch.part != lastPart:
            lastPart = ch.part
            out += ["", f"**Part {ch.part + 1}: {esc(partList[ch.part][0])}** – {esc(partList[ch.part][1])}", ""]
        out.append(f"{ch.num}. [**{esc(ch.title)}**](#{ch.id})")
        out.extend(f"    - [{esc(h['text'])}](#{h['id']})" for h in ch.headings if h["level"] == 2)
    return "\n".join(out) + "\n"


def makePdf(repo, outpath, ptxprint=None):
    """Typesets the linked Markdown edition (output/PTXprint-User-Manual.md) with PTXprint, headless, using
    the project in docs/uimanual/ptx, and copies the PDF to outpath. ptxprint: the program to run, such as
    a PTXprint.exe just built; by default this repository's PTXprint. Returns whether it made the PDF."""
    base = os.path.join(repo, "docs", "uimanual", "ptx")
    prjid = "PTXprintManual"
    env = {k: v for k, v in os.environ.items() if k not in ("DISPLAY", "WAYLAND_DISPLAY")}
    if ptxprint:
        cmd = [ptxprint]
    else:
        paths = [os.path.join(repo, "python", "lib")]       # this repo's PTXprint, not an installed one
        if env.get("PYTHONPATH"):
            paths.append(env["PYTHONPATH"])
        env["PYTHONPATH"] = os.pathsep.join(paths)
        cmd = [sys.executable, os.path.join(repo, "python", "scripts", "ptxprint")]
    cmd += ["-p", base, "-c", "Default", "-P", prjid,
            "-f", os.path.join(repo, "fonts")]         # Charis, Source Code Pro, SymPub: no installed fonts needed
    print("Typesetting the PDF: " + " ".join(cmd))
    pdfglob = os.path.join(base, prjid, "local", "ptxprint", f"{prjid}_Default_*_ptxp.pdf")
    for old in glob.glob(pdfglob):              # so an old PDF is never taken for a new one
        os.remove(old)
    res = subprocess.run(cmd, env=env, capture_output=True, text=True)
    pdfs = glob.glob(pdfglob)
    if res.returncode or not pdfs:
        print(f"PTXprint could not make the PDF (exit {res.returncode}):\n" + "\n".join(res.stdout.splitlines()[-15:]))
        return False
    os.makedirs(os.path.dirname(os.path.abspath(outpath)), exist_ok=True)
    shutil.copy2(pdfs[0], outpath)
    print(f"Wrote {outpath}")
    return True


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.abspath(os.path.join(here, "..", "..", ".."))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=repo)
    ap.add_argument("--nopdf", action="store_true", help="Skip making the PDF")
    ap.add_argument("--skeleton", action="store_true", help="Also write per-chapter control listings to data/chapters/")
    ap.add_argument("--pdf-only", action="store_true",
                    help="Only typeset the PDF from output/PTXprint-User-Manual.md, as it is in git (for release builds)")
    ap.add_argument("--ptxprint", help="With --pdf-only: the PTXprint program to typeset with, e.g. a PTXprint.exe just built")
    ap.add_argument("--out", help="With --pdf-only: the folder to put the PDF in (default docs/uimanual/output)")
    args = ap.parse_args()
    if args.pdf_only:
        outdir = args.out or os.path.join(args.repo, "docs", "uimanual", "output")
        sys.exit(0 if makePdf(args.repo, os.path.join(outdir, "PTXprint-User-Manual.pdf"), args.ptxprint) else 1)
    build(args.repo, dopdf=not args.nopdf, skeleton=args.skeleton)


if __name__ == "__main__":
    main()
