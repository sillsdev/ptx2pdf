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

levelPhrases = {2: "All view levels (Mini, Basic, Default, Full)", 4: "Basic, Default and Full views",
                5: "Default and Full views", 6: "Full view only"}

botPreface = """\
> **Notes for the AI support assistant**
>
> * This manual describes every setting in the PTXprint user interface (UI). Each setting lists
>   *where* it is (tab › section), *which view level* shows it, its *tooltip*, and a plain-language
>   explanation.
> * Most PTXprint users are **not technical**, and many speak English as a second or third language.
>   Answer in short, simple sentences. Give click-by-click directions using the tab and section
>   names exactly as written here.
> * **Do not tell users to edit configuration files (ptxprint.cfg), .sty or .tex files, or run
>   commands.** Every answer should be achievable in the PTXprint window. If something truly
>   cannot be done in the UI, say so and suggest contacting ptxprint_support@sil.org.
> * If a user cannot find a setting, check its *View level*. Many settings are hidden in the
>   Mini and Basic views. Tell the user how to change the view level (see "View levels").
> * Some settings are greyed out or hidden until another setting is turned on. This is shown as
>   "Only available when ..." and "Hidden until ...".
> * "Internal ID" and "Config key" lines are for support staff. They help you match a setting
>   that appears in a user's settings file or log to the place in the UI. Do not ask users about them.
"""


def stripColon(s):
    if s is None:
        return None
    return s.strip().rstrip(":：").strip()


def controlTitle(c):
    prim = stripColon(c.get("label")) or stripColon(c.get("fieldLabel"))
    name = c.get("name")
    if not prim:
        prim = name
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


def renderControl(c, note, human, hlevel="####"):
    title = controlTitle(c)
    out = [f"{hlevel} {mdEscape(title) if human else title}", ""]
    where = " › ".join(c["breadcrumbs"])
    facts = []
    facts.append(f"**Where:** {where}")
    typ = c["type"]
    if c.get("defaultOn") is not None and typ in ("Checkbox", "Toggle button"):
        typ += " (ticked by default)" if c["defaultOn"] else " (not ticked by default)"
    facts.append(f"**Type:** {typ}")
    nm = c.get("name")
    if nm and nm.lower() != title.lower():
        facts.append(f"**Description:** {nm}")
    if c.get("fieldLabel") and c.get("label") and stripColon(c["fieldLabel"]) != title:
        facts.append(f"**Next to the label:** {stripColon(c['fieldLabel'])}")
    if c.get("visibility") == "hidden":
        facts.append("**View level:** Not normally shown")
    elif c.get("visibility") == "experimental":
        facts.append("**View level:** Experimental (only shown when PTXprint is started in experimental mode)")
    elif c.get("viewLevel"):
        facts.append(f"**View level:** {levelPhrases[c['viewLevel']]}")
    r = c.get("range")
    if r:
        parts = []
        if r.get("lower") is not None and r.get("upper") is not None:
            parts.append("from {:g} to {:g}".format(r["lower"], r["upper"]))
        if r.get("default") is not None:
            parts.append("default {:g}".format(r["default"]))
        if parts:
            facts.append("**Values:** " + ", ".join(parts))
    ch = c.get("choices")
    if ch:
        texts = [x["text"] for x in ch if x.get("text")]
        if texts:
            facts.append("**Choices:** " + "; ".join(texts))
    if c.get("enabledBy"):
        facts.append("**Only available when:** " + depText(c["enabledBy"]) + " is selected")
    if c.get("disabledBy"):
        facts.append("**Greyed out when:** " + depText(c["disabledBy"]) + " is ticked")
    if c.get("collapsedUntil"):
        facts.append("**Hidden until:** " + depText([c["collapsedUntil"]]) + " is ticked")
    if c.get("tabShownBy"):
        facts.append("**This tab/section appears when:** " + depText(c["tabShownBy"]) + " is ticked")
    out.extend("- " + f for f in facts)
    out.append("")
    if c.get("tooltip"):
        out.append("**Tooltip (the text shown when you hover the mouse over it):**")
        out.append("")
        out.append(quoteBlock(c["tooltip"], human))
        out.append("")
    if note:
        out.append("**Explanation:**")
        out.append("")
        out.append(note.strip())
        out.append("")
    if not human and (c.get("id") or c.get("configKeys")):
        bits = []
        if c.get("id"):
            bits.append(f"Internal ID: `{c['id']}`")
        if c.get("configKeys"):
            bits.append("Config key: " + ", ".join(f"`{k}`" for k in c["configKeys"]))
        out.append("*(" + " · ".join(bits) + ")*")
        out.append("")
    return "\n".join(out)


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
    contents = "## Contents\n\n" + "\n".join(f"{i+1}. {t}" for i, (_, t, _) in enumerate(chapters)) + "\n"
    botParts.append(contents)
    humanParts.append(contents)
    for cid, title, places in chapters:
        prose, notes = parseContent(os.path.join(base, "content", cid + ".md"))
        ctrls = bych[cid]
        for k in notes:
            if k not in allIds:
                report.append(f"{cid}: note for unknown widget id '{k}'")
            elif not any(c["id"] == k for c in ctrls):
                report.append(f"{cid}: note for '{k}' which belongs to another chapter")
        for human in (False, True):
            parts = [f"# {title}", ""]
            if prose:
                parts.append(prose)
                parts.append("")
            elif not ctrls:
                continue
            if ctrls:
                parts.append(f"## Settings reference: {title}")
                parts.append("")
                parts.append("Every control in this part of PTXprint is listed below, grouped by where it appears.")
                parts.append("")
                groups = OrderedDict()
                for c in ctrls:
                    if human and c.get("visibility") in ("hidden", "experimental"):
                        continue
                    groups.setdefault(" › ".join(c["breadcrumbs"]), []).append(c)
                for g, cs in groups.items():
                    parts.append(f"### {mdEscape(g) if human else g}")
                    parts.append("")
                    for c in cs:
                        parts.append(renderControl(c, notes.get(c["id"]) if c["id"] else None, human))
            text = "\n".join(parts).rstrip() + "\n"
            if human:
                humanParts.append(text)
            else:
                botParts.append(text)
                with open(os.path.join(outdir, "bot", cid + ".md"), "w", encoding="utf-8") as outf:
                    outf.write(text)
                if skeleton and ctrls:
                    with open(os.path.join(base, "data", "chapters", cid + ".md"), "w", encoding="utf-8") as outf:
                        outf.write(text)
        missing = [c["id"] for c in ctrls if c["id"] and c["id"] not in notes and c.get("visibility") is None]
        if missing and (prose is not None):
            report.append(f"{cid}: {len(missing)} controls without a note: " + " ".join(missing))
        elif prose is None:
            report.append(f"{cid}: no content file yet ({len(ctrls)} controls)")
    if unassigned:
        report.append("Controls not assigned to any chapter: " +
                      ", ".join(f"{c['id']} [{' > '.join(c['breadcrumbs'])}]" for c in unassigned))

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
