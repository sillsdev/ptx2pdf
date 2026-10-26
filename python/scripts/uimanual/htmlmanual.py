#!/usr/bin/env python3
r"""
The interactive, single-file HTML edition of the PTXprint manual.

build_manual.py hands this module the human-readable Markdown of every chapter. This module
  * gives every heading and every setting a stable anchor (#id) and a "link to this" mark,
  * turns cross-references in the text into links: tab names ("the Layout tab", "See also: Basic tab"),
    quoted or bold section names, and bold names of settings that exist in the settings reference,
  * adds navigation: a contents sidebar that follows the reader, "up / previous / next" bars at the end
    of every section, a mini contents at the top of every chapter, a task index in the how-to chapters,
    a "back to top" button and a search box (headings first, then all text),
  * wraps it all in one self-contained page (no external files, works offline).

Settings headings are marked in the Markdown as "Title {#s-the-widget-id}"; see ctrlAnchor().
"""

import datetime
import html
import re
from collections import OrderedDict, defaultdict

from markdown_it import MarkdownIt
from markdown_it.token import Token

from chapters import chapterAliases

# Names so common that linking every bold mention to "the" setting of that name would be noise
STOP = set("""ok cancel print save close add del delete edit reset select quit help yes no apply browse open
preview default full basic mini regular none left right top bottom center centre inner outer page pages
book books text font size style styles margin margins tab tabs scale rotation position name type
other main details general advanced""".split()) | {"print (make pdf)", "print (update pdf)"}

AREA_WORDS = re.compile(r"\s*(area|section|group|box|sub-tab|dialog|tab|chapter)", re.I)

MARKER = re.compile(r"\s*\{#([A-Za-z0-9-]+)\}\s*$")


def ctrlAnchor(ctrlId):
    """The anchor of a setting's entry in the settings reference."""
    return "s-" + re.sub(r"[^A-Za-z0-9]+", "-", ctrlId).strip("-")


def slug(s):
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s or "x"


def norm(s):
    """Normal form for comparing names: no markup, case, trailing colon/dots, leading section number."""
    s = re.sub(r"<[^>]+>", "", s or "").replace("\u2026", "...").replace("\u2019", "'")
    s = re.sub(r"\s+", " ", s).strip().strip(":\uff1a").strip()
    s = re.sub(r"\.{3}$", "", s).strip()
    s = re.sub(r"^\d+(\.\d+)*\.?\s+", "", s)
    return s.lower()


def plain(inline):
    """Plain text of an inline token."""
    return "".join(c.content for c in (inline.children or []) if c.type in ("text", "text_special", "code_inline"))


def tok(type_, tag="", nesting=0, content="", **attrs):
    t = Token(type_, tag, nesting)
    t.content = content
    for k, v in attrs.items():
        t.attrSet(k.replace("_", "-"), v)
    return t


def htmlBlock(s):
    return tok("html_block", content=s + "\n")


def esc(s):
    return html.escape(s, quote=True)


class Chapter:
    def __init__(self, info, tokens):
        self.cid = info["cid"]
        self.num = info["num"]
        self.title = info["title"]
        self.part = info["part"]
        self.tokens = tokens
        self.headings = []      # dicts: level, id, text, title, setting, idx
        self.id = "ch-" + self.cid

    @property
    def h2(self):
        return [h for h in self.headings if h["level"] == 2]


class Linker:
    """Turns mentions of other parts of the manual into links."""

    def __init__(self, chapters, ctrlKeys, used):
        self.chapters = chapters
        self.byCid = {c.cid: c for c in chapters}
        self.headingsByTitle = defaultdict(list)          # norm title -> [(cid, id, level)]
        for ch in chapters:
            for h in ch.headings:
                if not h["setting"]:
                    self.headingsByTitle[norm(h["title"])].append((ch.cid, h["id"], h["level"]))
        keys = defaultdict(set)
        for ck in ctrlKeys:
            if ck["anchor"] not in used:
                continue
            for k in ck["keys"]:
                n = norm(k)
                if len(n) >= 3 and n not in STOP:
                    keys[n].add(ck["anchor"])
        self.unique = {n: next(iter(a)) for n, a in keys.items() if len(a) == 1}
        # tab names -> chapter id, from titles such as "Basic tab" or "Peripherals tab (front and back matter)"
        self.tabs = {}
        for ch in chapters:
            m = re.match(r"^(.+?) tab\b", ch.title)
            if m:
                self.tabs[norm(m.group(1))] = ch.cid
        self.aliases = {k: v for k, v in chapterAliases.items() if v in self.byCid}
        # plain-text phrases that are always links: whole chapter titles and "<Tab> tab"
        phrases = {ch.title: ch.cid for ch in chapters}
        for name, cid in self.tabs.items():
            phrases[self.byCid[cid].title.split(" tab")[0] + " tab"] = cid
        self.phrases = phrases
        alt = "|".join(re.escape(p) for p in sorted(phrases, key=len, reverse=True))
        self.textRe = re.compile(r"(?P<q>[\"\u201c][^\"\u201c\u201d\n]{3,90}[\"\u201d])|"
                                 r"(?P<a>(?<![\w+])(?:%s)(?![\w+]))" % alt)
        # "See also: ..." lines are navigation aids: every name in them is a link, and the usual alternative
        # names (" Main window", "PDF Preview window") count too
        self.phraseByNorm = {norm(p): cid for p, cid in phrases.items()}
        self.phraseByNorm.update(self.aliases)
        alt2 = "|".join(re.escape(p) for p in sorted(set(phrases) | set(chapterAliases), key=len, reverse=True))
        self.seeRe = re.compile(r"(?<![\w+])(?:%s)(?![\w+])" % alt2, re.I)
        self.cur = None
        self.curHeading = None
        self.seen = set()
        self.count = 0

    # --- resolving ---
    def _chapterTop(self, cid):
        return "#" + self.byCid[cid].id

    @staticmethod
    def _specific(n, lvl, following):
        """Chapter and section titles are specific enough; a short area name such as "Basic" or "Name" is
        only a reference when the text says so ("the Page Setup area")."""
        return lvl <= 2 or len(n.split()) >= 2 or bool(AREA_WORDS.match(following or ""))

    def _inChapter(self, n, following=""):
        c = [(cid, i, lvl) for cid, i, lvl in self.headingsByTitle.get(n, []) if cid == self.cur]
        return c[0][1] if len(c) == 1 and self._specific(n, c[0][2], following) else None

    def resolveBold(self, label, following):
        n = norm(label)
        if not n:
            return None
        base = n[:-4] if n.endswith(" tab") else n
        if base in self.tabs and (n.endswith(" tab") or re.match(r"\s*(tab|chapter)\b", following or "", re.I)):
            return None if self.tabs[base] == self.cur else self._chapterTop(self.tabs[base])
        if n in self.aliases and re.match(r"\s*(tab |window )?chapter\b", following or "", re.I):
            return None if self.aliases[n] == self.cur else self._chapterTop(self.aliases[n])
        target = self._inChapter(n, following)
        if target:
            return "#" + target
        if n in self.unique:
            return "#" + self.unique[n]
        glob = self.headingsByTitle.get(n, [])
        if len(glob) == 1 and glob[0][0] != self.cur and self._specific(n, glob[0][2], following):
            return "#" + glob[0][1]
        return None

    def resolveQuoted(self, inner):
        n = norm(inner)
        target = self._inChapter(n)
        if target:
            return "#" + target
        if n in self.unique:                    # a setting named in quotes, e.g. in "Needs: ..."
            return "#" + self.unique[n]
        glob = self.headingsByTitle.get(n, [])
        if len(glob) == 1 and self._specific(n, glob[0][2], ""):
            return "#" + glob[0][1]
        return None

    # --- applying ---
    def _make(self, href, children):
        o = tok("link_open", "a", 1)
        o.attrSet("href", href)
        o.attrSet("class", "xref")
        return [o] + children + [tok("link_close", "a", -1)]

    def _ok(self, href, force=False):
        if not href or href == "#" + (self.curHeading or "") or (href in self.seen and not force):
            return False
        self.seen.add(href)
        self.count += 1
        return True

    def linkText(self, t, seeAlso=False):
        text = t.content
        out, pos = [], 0
        for m in (self.seeRe if seeAlso else self.textRe).finditer(text):
            if not seeAlso and m.group("q"):
                href = self.resolveQuoted(m.group("q")[1:-1])
            else:
                cid = self.phraseByNorm.get(norm(m.group(0))) if seeAlso else self.phrases[m.group("a")]
                href = None if cid is None or cid == self.cur else self._chapterTop(cid)
            if not self._ok(href, seeAlso):
                continue
            if m.start() > pos:
                out.append(tok("text", content=text[pos:m.start()]))
            out += self._make(href, [tok("text", content=m.group(0))])
            pos = m.end()
        if not out:
            return [t]
        if pos < len(text):
            out.append(tok("text", content=text[pos:]))
        return out

    def link(self, children):
        seeAlso = bool(children) and children[0].type == "text" and children[0].content.startswith("See also:")
        out, i, n, depth = [], 0, len(children), 0
        while i < n:
            t = children[i]
            if t.type == "link_open":
                depth += 1
            elif t.type == "link_close":
                depth -= 1
            if depth or t.type in ("link_open", "link_close"):
                out.append(t)
                i += 1
            elif t.type == "strong_open":
                j = i + 1
                while j < n and children[j].type != "strong_close":
                    j += 1
                inner = children[i + 1:j]
                if j < n and inner and all(x.type in ("text", "text_special") for x in inner):
                    label = "".join(x.content for x in inner)
                    nxt = children[j + 1].content if j + 1 < n and children[j + 1].type == "text" else ""
                    href = self.resolveBold(label, nxt)
                    if self._ok(href):
                        out += self._make(href, children[i:j + 1])
                        i = j + 1
                        continue
                out.extend(children[i:j + 1])
                i = j + 1
            elif t.type == "text":
                out.extend(self.linkText(t, seeAlso))
                i += 1
            else:
                out.append(t)
                i += 1
        return out


def navBar(links, cls="secnav"):
    """links: list of (label, href) with None entries dropped."""
    items = "".join(f'<a href="{esc(h)}">{l}</a>' for l, h in links if h)
    return f'<nav class="{cls}" aria-label="Section navigation">{items}</nav>'


def prepare(ch, used):
    """First pass over a chapter: give headings their ids, remove the setting markers."""
    toks = ch.tokens
    for idx, t in enumerate(toks):
        if t.type != "heading_open":
            continue
        inline = toks[idx + 1]
        level = int(t.tag[1])
        m = MARKER.search(inline.content)
        setting = bool(m)
        if m:
            hid = m.group(1)
            inline.content = inline.content[:m.start()]
            last = inline.children[-1] if inline.children else None
            if last is not None and last.type == "text":
                last.content = MARKER.sub("", last.content)
        elif level == 1:
            hid = ch.id
        else:
            hid = f"{ch.cid}--{slug(re.sub(r'^[0-9.]+ ', '', plain(inline)))}"
        base, k = hid, 1
        while hid in used:
            k += 1
            hid = f"{base}-{k}"
        used.add(hid)
        t.attrSet("id", hid)
        text = plain(inline)
        ch.headings.append(dict(level=level, id=hid, text=text, title=re.sub(r"^[0-9.]+ ", "", text),
                                setting=setting, idx=idx))


def decorate(ch, linker, chapters, parts, taskIndex):
    """Second pass: links, navigation, permalinks, classes. Returns the new token list."""
    toks = ch.tokens
    byIdx = {h["idx"]: h for h in ch.headings}
    h2s = ch.h2
    pos = {h["id"]: i for i, h in enumerate(h2s)}
    ci = chapters.index(ch)
    prevCh = chapters[ci - 1] if ci > 0 else None
    nextCh = chapters[ci + 1] if ci + 1 < len(chapters) else None
    out = []
    linker.cur = ch.cid
    linker.seen = set()
    linker.curHeading = ch.id
    curH2 = curH3 = None
    inRef = False
    state = None

    def closeH3():
        if curH3 is not None and inRef:
            out.append(htmlBlock(navBar([("\u2191 Settings reference", "#" + curH2["id"]),
                                         ("\u2191\u2191 Top of chapter", "#" + ch.id)], "secnav small")))

    def closeH2():
        if curH2 is None:
            return
        i = pos[curH2["id"]]
        prev = h2s[i - 1] if i > 0 else None
        nxt = h2s[i + 1] if i + 1 < len(h2s) else None
        links = [("\u2191 Top of chapter", "#" + ch.id), ("\u21d1 Contents", "#contents")]
        if prev:
            links.append((f"\u2190 {esc(prev['text'])}", "#" + prev["id"]))
        if nxt:
            links.append((f"{esc(nxt['text'])} \u2192", "#" + nxt["id"]))
        elif nextCh:
            links.append((f"Next chapter: {esc(nextCh.title)} \u2192", "#" + nextCh.id))
        out.append(htmlBlock(navBar(links)))

    for idx, t in enumerate(toks):
        h = byIdx.get(idx)
        if t.type == "heading_open":
            state = None
            level = h["level"]
            if level <= 3:
                closeH3()
                curH3 = None
            if level <= 2:
                closeH2()
                curH2 = None
            if level == 1:
                part = parts[ch.part]
                out.append(htmlBlock(f'<p class="crumb"><a href="#contents">Contents</a> \u203a '
                                     f'<a href="#part-{ch.part + 1}">{esc(part[0])}</a></p>'))
            if level == 2:
                curH2, inRef = h, h["text"].rstrip().lower().endswith("settings reference")
            if level == 3:
                curH3 = h
            linker.seen = set()
            linker.curHeading = h["id"]
            if h["setting"]:
                t.attrSet("data-kind", "setting")
            out.append(t)
            continue
        if t.type == "heading_close":
            out.append(t)
            hh = next((x for x in reversed(ch.headings) if x["idx"] < idx and x["level"] == int(t.tag[1])), None)
            if hh and hh["setting"]:
                state = "facts"
            if hh and hh["level"] == 1:
                if len(h2s) >= 3:
                    items = "".join(f'<li><a href="#{x["id"]}">{esc(x["text"])}</a></li>' for x in h2s)
                    out.append(htmlBlock(f'<nav class="mini-toc" aria-label="In this chapter"><strong>In this '
                                         f'chapter</strong><ol>{items}</ol></nav>'))
            if hh and hh["level"] == 2 and ch.cid in taskIndex:
                nxt = [x for x in ch.headings if x["idx"] > hh["idx"]]
                kids = []
                for x in nxt:
                    if x["level"] <= 2:
                        break
                    if x["level"] == 3:
                        kids.append(x)
                if kids:
                    items = "".join(f'<li><a href="#{x["id"]}">{esc(x["text"])}</a></li>' for x in kids)
                    out.append(htmlBlock(f'<ul class="task-list">{items}</ul>'))
            continue
        if t.type == "inline" and idx > 0 and toks[idx - 1].type == "heading_open":
            hh = byIdx[idx - 1]
            t.children.append(tok("html_inline", content=f' <a class="pl" href="#{hh["id"]}" '
                                                         f'title="Link to this heading">#</a>'))
            out.append(t)
            continue
        if t.type == "inline":
            t.children = linker.link(t.children)
        if state == "facts" and t.type == "paragraph_open":
            t.attrJoin("class", "facts")
            state = "tip"
        elif state == "tip" and t.type == "paragraph_close":
            state = "tip-next"
        elif state == "tip-next":
            if t.type == "blockquote_open":
                t.attrJoin("class", "tip")
            state = None
        elif state == "tip" and t.type != "inline":
            state = None
        out.append(t)
    closeH3()
    closeH2()
    if nextCh or prevCh:
        links = [("\u2191 Top of chapter", "#" + ch.id), ("\u21d1 Contents", "#contents")]
        if prevCh:
            links.insert(0, (f"\u2190 Previous chapter: {esc(prevCh.title)}", "#" + prevCh.id))
        if nextCh:
            links.append((f"Next chapter: {esc(nextCh.title)} \u2192", "#" + nextCh.id))
        out.append(htmlBlock(navBar(links, "secnav chapnav")))
    return out


def sidebar(chapters, parts):
    out = ['<div class="sb-search"><input id="q" type="search" placeholder="Search the manual   ( / )" '
           'autocomplete="off" aria-label="Search the manual"></div><div id="results" hidden></div>',
           '<div id="toc">']
    lastPart = None
    for ch in chapters:
        if ch.part != lastPart:
            lastPart = ch.part
            out.append(f'<a class="sb-part" href="#part-{ch.part + 1}">{esc(parts[ch.part][0])}</a>')
        items, ref = [], False
        for h in ch.headings:
            if h["level"] == 2:
                ref = h["text"].rstrip().lower().endswith("settings reference")
                items.append(f'<li><a href="#{h["id"]}">{esc(h["text"])}</a></li>')
            elif h["level"] == 3 and ref and not h["setting"]:
                items.append(f'<li class="sub"><a href="#{h["id"]}">{esc(h["text"])}</a></li>')
        out.append(f'<details class="chap" data-ch="{ch.id}"><summary><a href="#{ch.id}">'
                   f'<span class="n">{ch.num}.</span> {esc(ch.title)}</a></summary>'
                   f'<ul>{"".join(items)}</ul></details>')
    out.append("</div>")
    return "\n".join(out)


def hero(chapters, parts, title, today):
    have = {c.cid: c for c in chapters}

    def card(cid, head, text):
        if cid not in have:
            return ""
        return f'<a class="card" href="#{have[cid].id}"><strong>{head}</strong><span>{text}</span></a>'

    cards = "".join([
        card("01-getting-started", "New here?", "A first walk-through, from opening PTXprint to your first PDF."),
        card("30-howto", "How do I\u2026?", "Step-by-step instructions for common jobs."),
        card("31-troubleshooting", "Something went wrong", "Problems, why they happen and what to do."),
        card("02-main-window", "I cannot find a setting", "View levels, search and the parts of the window."),
        card("32-glossary", "What does this word mean?", "The words used in this manual."),
    ])
    lists = []
    for i, (pt, descr, cids) in enumerate(parts):
        items = "".join(f'<li><a href="#{have[c].id}">{esc(have[c].title)}</a></li>' for c in cids if c in have)
        lists.append(f'<div class="partlist"><h3><a href="#part-{i + 1}">Part {i + 1}: {esc(pt)}</a></h3>'
                     f'<p>{esc(descr)}</p><ul>{items}</ul></div>')
    return (f'<section class="hero" id="top"><h1 class="doc-title">{esc(title)}</h1>'
            f'<p class="muted">Generated {today}. The whole manual is on this one page. Use the contents on the left, '
            f'the search box (press <kbd>/</kbd>), and the blue links in the text to jump to another place. '
            f'The <kbd>#</kbd> beside a heading links to that exact heading.</p>'
            f'<div class="cards">{cards}</div><h2 class="contents-title" id="contents">Contents</h2>'
            f'<div class="partlists">{"".join(lists)}</div></section>')


CSS = r"""
:root{--bg:#fff;--fg:#1d2733;--muted:#5a6a7a;--accent:#1b5ea8;--accent2:#e8f0fa;--line:#d5dde6;--tip:#f4f7fb;--code:#eef2f6;--hl:#fff3b0;--side:#f7f9fb}
@media (prefers-color-scheme:dark){:root{--bg:#14181d;--fg:#dde5ee;--muted:#9aa9b9;--accent:#79b2ee;--accent2:#1f2e40;--line:#2c3743;--tip:#1a2129;--code:#1f2730;--hl:#5a4d00;--side:#181d23}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--accent)}[id]{scroll-margin-top:4.2rem}
.skip{position:absolute;left:-999px}.skip:focus{left:1rem;top:1rem;background:var(--bg);padding:.5rem;z-index:99}
.topbar{position:sticky;top:0;z-index:20;display:flex;gap:.8rem;align-items:center;padding:.5rem 1rem;background:var(--bg);border-bottom:1px solid var(--line)}
.topbar .tt{font-weight:600}#crumb{color:var(--muted);font-size:.9rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1}
#navtoggle{display:none;font:inherit;padding:.3rem .7rem;border:1px solid var(--line);background:var(--accent2);color:var(--fg);border-radius:6px;cursor:pointer}
.layout{display:flex;align-items:flex-start}
#sidebar{position:sticky;top:3.1rem;flex:0 0 22rem;max-height:calc(100vh - 3.1rem);overflow:auto;background:var(--side);border-right:1px solid var(--line);padding:.6rem .5rem 3rem;font-size:.92rem}
main{flex:1;min-width:0;max-width:60rem;padding:1rem 2rem 6rem}
.sb-search input{width:100%;font:inherit;padding:.45rem .6rem;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)}
#results{margin:.4rem 0 .8rem;border:1px solid var(--line);border-radius:6px;background:var(--bg);max-height:60vh;overflow:auto}
#results a{display:block;padding:.35rem .6rem;text-decoration:none;color:var(--fg);border-bottom:1px solid var(--line)}
#results a:hover,#results a.sel{background:var(--accent2)}#results small{display:block;color:var(--muted)}
#results .rh{padding:.25rem .6rem;font-size:.75rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);background:var(--tip)}
#results mark,.snip mark{background:var(--hl);color:inherit}
.sb-part{display:block;margin:.9rem .4rem .2rem;font-size:.75rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);text-decoration:none}
details.chap>summary{cursor:pointer;padding:.15rem .3rem;border-radius:4px;list-style-position:inside}
details.chap>summary a{text-decoration:none;color:var(--fg)}details.chap>summary .n{color:var(--muted)}
details.chap ul{list-style:none;margin:.1rem 0 .4rem 1.3rem;padding:0}details.chap li a{display:block;padding:.1rem .4rem;text-decoration:none;color:var(--muted);border-radius:4px;line-height:1.35}
details.chap li.sub{margin-left:.9rem;font-size:.88rem}
#sidebar a.active{background:var(--accent2);color:var(--accent);font-weight:600}#sidebar a:hover{text-decoration:underline}
h1,h2,h3,h4,h5,h6{line-height:1.25}h1{font-size:1.9rem;margin:2.5rem 0 .6rem;padding-bottom:.35rem;border-bottom:3px solid var(--accent)}
h2{font-size:1.45rem;margin:2.4rem 0 .6rem;color:var(--accent)}h3{font-size:1.2rem;margin:1.8rem 0 .5rem}h4{font-size:1.05rem;margin:1.5rem 0 .4rem;padding:.2rem .5rem;background:var(--accent2);border-radius:4px}
h5{font-size:1rem;margin:1.3rem 0 .2rem;padding-top:.5rem;border-top:1px solid var(--line)}h6{font-size:.95rem;margin:1.1rem 0 .2rem;border-top:1px solid var(--line);padding-top:.4rem}
a.pl{visibility:hidden;margin-left:.4rem;font-weight:400;text-decoration:none;color:var(--muted)}:is(h1,h2,h3,h4,h5,h6):hover a.pl{visibility:visible}
:target{animation:flash 2.2s ease-out}@keyframes flash{0%,35%{background:var(--hl)}100%{background:transparent}}
.hero{padding:1rem 0 0}.doc-title{font-size:2.4rem;border:0;margin:.5rem 0}.muted{color:var(--muted)}kbd{border:1px solid var(--line);border-bottom-width:2px;border-radius:4px;padding:0 .35rem;font-size:.85em;background:var(--tip)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(14rem,1fr));gap:.8rem;margin:1.2rem 0}
.card{display:block;padding:.8rem 1rem;border:1px solid var(--line);border-radius:10px;background:var(--tip);text-decoration:none;color:var(--fg)}.card:hover{border-color:var(--accent);background:var(--accent2)}.card strong{display:block;color:var(--accent);font-size:1.05rem}.card span{color:var(--muted);font-size:.9rem}
.contents-title{margin-top:2rem}.partlists{display:grid;grid-template-columns:repeat(auto-fit,minmax(18rem,1fr));gap:1rem}.partlist h3{margin:.2rem 0}.partlist p{margin:.1rem 0 .3rem;color:var(--muted);font-size:.9rem}.partlist ul{margin:0;padding-left:1.1rem}
.part-banner{margin:4rem 0 .5rem;padding:.8rem 1rem;border-left:6px solid var(--accent);background:var(--accent2);border-radius:0 8px 8px 0;font-size:1.05rem}.part-banner span{display:block;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}.part-banner strong{font-size:1.5rem}
.crumb{margin:2.5rem 0 0;font-size:.85rem;color:var(--muted)}.crumb a{color:var(--muted)}.crumb+h1{margin-top:.3rem}
.mini-toc{margin:1rem 0 1.5rem;padding:.7rem 1rem;border:1px solid var(--line);border-radius:8px;background:var(--tip)}.mini-toc ol{margin:.3rem 0 0;padding-left:1.4rem;columns:2 16rem}.mini-toc li{break-inside:avoid;margin:.1rem 0}
.task-list{columns:2 18rem;margin:.4rem 0 1rem;padding-left:1.2rem;font-size:.95rem}.task-list li{break-inside:avoid;margin:.1rem 0}
.secnav{display:flex;flex-wrap:wrap;gap:.3rem 1.1rem;margin:2rem 0 0;padding:.5rem 0;border-top:1px solid var(--line);font-size:.88rem}.secnav a{text-decoration:none}.secnav a:hover{text-decoration:underline}
.secnav.small{margin:.8rem 0 0;border-top:1px dashed var(--line);font-size:.8rem}.chapnav{margin-bottom:1rem}
a.xref{text-decoration:underline dotted;text-underline-offset:3px}a.xref:hover{text-decoration:underline solid}
blockquote{margin:.4rem 0 .6rem;padding:.4rem .9rem;border-left:4px solid var(--line);background:var(--tip);color:var(--fg)}blockquote p{margin:.3rem 0}
blockquote.tip{border-left-color:var(--accent);font-style:italic}blockquote.tip::before{content:"Tooltip";display:block;font-style:normal;font-size:.7rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
p.facts{margin:.1rem 0 .4rem;color:var(--muted);font-size:.88rem}
code{background:var(--code);padding:.05rem .3rem;border-radius:4px;font-size:.9em}pre{background:var(--code);padding:.7rem;border-radius:6px;overflow:auto}
table{border-collapse:collapse;margin:.6rem 0;display:block;overflow-x:auto}td,th{border:1px solid var(--line);padding:.35rem .6rem;vertical-align:top}th{background:var(--accent2);text-align:left}
#totop{position:fixed;right:1.2rem;bottom:1.2rem;padding:.5rem .8rem;border-radius:999px;background:var(--accent);color:#fff;text-decoration:none;box-shadow:0 2px 8px rgba(0,0,0,.3);opacity:0;pointer-events:none;transition:opacity .2s}#totop.on{opacity:.92;pointer-events:auto}
@media (max-width:900px){#navtoggle{display:inline-block}#sidebar{position:fixed;z-index:30;top:3.1rem;bottom:0;left:0;width:min(88vw,22rem);max-height:none;transform:translateX(-102%);transition:transform .2s;box-shadow:2px 0 12px rgba(0,0,0,.25)}body.navopen #sidebar{transform:none}main{padding:.5rem 1rem 6rem}.topbar .tt{display:none}}
@media print{.topbar,#sidebar,.secnav,#totop,.mini-toc,a.pl{display:none!important}main{max-width:none;padding:0}h1{page-break-before:always}a{color:inherit;text-decoration:none}}
"""

JS = r"""
(function(){
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var side=$('#sidebar'),q=$('#q'),res=$('#results'),crumb=$('#crumb'),totop=$('#totop');
$('#navtoggle').addEventListener('click',function(){document.body.classList.toggle('navopen')});
side.addEventListener('click',function(e){if(e.target.closest('a')&&window.matchMedia('(max-width:900px)').matches)document.body.classList.remove('navopen')});
/* ---- follow the reader: highlight the current place in the contents ---- */
var spy=$$('main h1[id],main h2[id],main h3[id]'),tops=[],links={},active=null,activeCh=null,tick=false;
$$('#toc a[href^="#"]').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
function measure(){tops=spy.map(function(e){return e.getBoundingClientRect().top+window.scrollY})}
function chapterOf(el){var c=el.closest('section.chapter');return c?c.getAttribute('data-title'):''}
function update(){
 tick=false;var y=window.scrollY+110,i=-1;
 for(var k=0;k<tops.length;k++){if(tops[k]<=y)i=k;else break}
 totop.classList.toggle('on',window.scrollY>700);
 if(i<0){crumb.textContent='';return}
 var h=spy[i],j=i;while(j>0&&!links[spy[j].id])j--;var a=links[spy[j].id];
 var ch=h.closest('section.chapter'),t=ch?ch.getAttribute('data-title'):'';
 crumb.textContent=(h.tagName==='H1')?t:t+' \u203a '+h.textContent.replace(/#$/,'').trim();
 if(a===active)return;
 if(active)active.classList.remove('active');
 active=a;if(!a)return;a.classList.add('active');
 var d=a.closest('details');
 if(d&&d!==activeCh){if(activeCh)activeCh.open=false;d.open=true;activeCh=d}
 var r=a.getBoundingClientRect(),s=side.getBoundingClientRect();
 if(r.top<s.top+60||r.bottom>s.bottom-20)side.scrollTop+=r.top-s.top-side.clientHeight/3;
}
window.addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(update)}},{passive:true});
window.addEventListener('resize',function(){measure();update()});
window.addEventListener('load',function(){measure();update()});
measure();update();
/* ---- search: headings first, then every paragraph ---- */
var heads=null,texts=null,sel=-1;
function build(){
 heads=[];texts=[];var cur='',curId='',curTitle='';
 $$('main section.chapter').forEach(function(sec){
  var title=sec.getAttribute('data-title');cur=title;
  $$('h1[id],h2[id],h3[id],h4[id],h5[id],h6[id],p,li,td',sec).forEach(function(e){
   if(/^H\d$/.test(e.tagName)){
    var txt=e.textContent.replace(/#$/,'').trim();curId=e.id;curTitle=txt;
    var extra='';if(e.getAttribute('data-kind')==='setting'){var n=e.nextElementSibling;if(n&&n.classList.contains('facts'))extra=n.textContent}
    heads.push({id:e.id,t:txt,ch:title,lvl:+e.tagName[1],x:(txt+' '+extra).toLowerCase()});
   }else if(!(e.tagName==='LI'&&e.querySelector('p'))&&!e.closest('.secnav,.mini-toc,.task-list')){
    var s=e.textContent.replace(/\s+/g,' ').trim();if(s.length>3)texts.push({id:curId,h:curTitle,ch:title,s:s,l:s.toLowerCase()});
   }
  });
 });
}
function mk(s,words){var o=s;words.forEach(function(w){if(!w)return;o=o.replace(new RegExp('('+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig'),'\u0001$1\u0002')});
 return o.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/\u0001/g,'<mark>').replace(/\u0002/g,'</mark>')}
function search(){
 var v=q.value.trim().toLowerCase();sel=-1;
 if(v.length<2){res.hidden=true;$('#toc').hidden=false;return}
 if(!heads)build();
 var words=v.split(/\s+/);
 var hs=heads.filter(function(h){return words.every(function(w){return h.x.indexOf(w)>=0})});
 hs.sort(function(a,b){var sa=a.t.toLowerCase().indexOf(v)===0?0:1,sb=b.t.toLowerCase().indexOf(v)===0?0:1;return sa-sb||a.lvl-b.lvl});
 var ts=texts.filter(function(x){return words.every(function(w){return x.l.indexOf(w)>=0})});
 var out='';
 if(hs.length){out+='<div class="rh">Headings and settings ('+hs.length+')</div>';
  hs.slice(0,25).forEach(function(h){out+='<a href="#'+h.id+'">'+mk(h.t,words)+'<small>'+mk(h.ch,[])+'</small></a>'})}
 if(ts.length){out+='<div class="rh">In the text ('+ts.length+')</div>';
  ts.slice(0,25).forEach(function(x){var i=x.l.indexOf(words[0]),a=Math.max(0,i-50),sn=x.s.substr(a,150);
   out+='<a href="#'+x.id+'"><span class="snip">'+(a?'\u2026':'')+mk(sn,words)+'\u2026</span><small>'+mk(x.ch+' \u203a '+x.h,[])+'</small></a>'})}
 if(!out)out='<div class="rh">Nothing found. Try fewer or different words.</div>';
 res.innerHTML=out;res.hidden=false;$('#toc').hidden=true;
}
q.addEventListener('input',search);
q.addEventListener('keydown',function(e){
 var items=$$('a',res);
 if(e.key==='Escape'){q.value='';search();q.blur()}
 else if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();if(!items.length)return;
  sel=(sel+(e.key==='ArrowDown'?1:-1)+items.length)%items.length;items.forEach(function(a,i){a.classList.toggle('sel',i===sel)});items[sel].scrollIntoView({block:'nearest'})}
 else if(e.key==='Enter'){var t=items[sel>=0?sel:0];if(t){location.hash=t.getAttribute('href');if(window.matchMedia('(max-width:900px)').matches)document.body.classList.remove('navopen')}}
});
res.addEventListener('click',function(e){if(e.target.closest('a')&&window.matchMedia('(max-width:900px)').matches)document.body.classList.remove('navopen')});
document.addEventListener('keydown',function(e){
 if(e.key==='/'&&!/INPUT|TEXTAREA|SELECT/.test((e.target.tagName||''))&&!e.ctrlKey&&!e.metaKey){e.preventDefault();document.body.classList.add('navopen');q.focus();q.select()}
});
})();
"""


def build(chapterInfos, ctrlKeys, parts, title, today, taskIndex=("30-howto", "31-troubleshooting")):
    """chapterInfos: [{cid, num, title, part, text}], ctrlKeys: [{anchor, keys}], parts: chapters.parts"""
    md = MarkdownIt("commonmark").enable("table").enable("strikethrough")
    used = {"top", "contents"}
    chapters = []
    for info in chapterInfos:
        ch = Chapter(info, md.parse(info["text"]))
        prepare(ch, used)
        chapters.append(ch)
    linker = Linker(chapters, ctrlKeys, used)
    body, lastPart = [], None
    for ch in chapters:
        if ch.part != lastPart:
            lastPart = ch.part
            body.append(f'<div class="part-banner" id="part-{ch.part + 1}"><span>Part {ch.part + 1}</span>'
                        f'<strong>{esc(parts[ch.part][0])}</strong> \u2013 {esc(parts[ch.part][1])}</div>')
        toks = decorate(ch, linker, chapters, parts, taskIndex)
        rendered = md.renderer.render(toks, md.options, {})
        body.append(f'<section class="chapter" data-title="{esc(ch.title)}">\n{rendered}</section>')
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><style>{CSS}</style></head>
<body id="body"><a class="skip" href="#main">Skip to the text</a>
<header class="topbar"><button id="navtoggle" aria-label="Show or hide the contents">Contents</button>
<a class="tt" href="#top" style="text-decoration:none;color:inherit">{esc(title)}</a><span id="crumb"></span></header>
<div class="layout"><nav id="sidebar" aria-label="Contents">
{sidebar(chapters, parts)}
</nav><main id="main">
{hero(chapters, parts, title, today)}
{chr(10).join(body)}
</main></div>
<a id="totop" href="#top" aria-label="Back to the top">\u2191 Top</a>
<script>{JS}</script></body></html>
"""
    return page, linker
