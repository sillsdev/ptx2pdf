#!/usr/bin/python3
r"""
Markdown to USX, so that PTXprint can typeset a Markdown file (a module whose file name ends in .md).

The document can start with a front matter block of settings:

    ---
    book: XXA
    headings: ms1 s1
    outline: 2
    ---

  book      the book code to use (default MOD).
  headings  the markers for the first heading levels; each deeper level takes the marker of the level
            above with its number one higher (with "ms1 s1": h3 is \s2 ... h6 is \s5). Default: h1 is \s1.
  outline   headings down to this level that have an id become PDF bookmarks (default 2).
  quote     the paragraph marker for block quotes (default pi1).
  bullet    what starts each item of a bulleted list (default •; "bullet:" on its own for nothing).

A heading that ends in {#id} gets an anchor with that id: links to "#id" jump to it, and (down to the
outline level) it is a bookmark. Links become \jmp, code \zcode and code blocks \zpre (define these two in
the job's stylesheet), and strikethrough \zs.

Footnotes ("text[^1]" with "[^1]: the note" anywhere, or inline "text^[the note]") become \f + \ft ...\f*
at the reference; a note's later paragraphs start with \fp.

An image is a figure: ![caption](file.jpg "description"){size=col loc=t ref="GEN 1:1"} becomes
\fig caption|src="file.jpg" alt="description" size="col" loc="t" ref="GEN 1:1"\fig* (any attribute in {}
is passed on).

A block between "::: esb-name" and ":::" is a sidebar of category name: \esb \cat name\cat* ... \esbe;
"::: esb" makes a sidebar with no category. No other "::: ..." block is recognised (its lines stay text),
so those names are free for other uses.

This needs the mdit-py-plugins package (front matter, footnotes, attributes, containers).
"""

import re

from markdown_it import MarkdownIt
try:
    from mdit_py_plugins.front_matter import front_matter_plugin
    from mdit_py_plugins.footnote import footnote_plugin
    from mdit_py_plugins.attrs import attrs_plugin
    from mdit_py_plugins.container import container_plugin
except ImportError:         # reported when a Markdown file is read, so PTXprint itself still starts
    front_matter_plugin = None
from usfmtc.xmlutils import ParentElement
from usfmtc import USX

HEADING_ID = re.compile(r"\s*\{#([^\s{}]+)\}\s*$")


def frontMatter(text):
    """The settings in a front matter block: "key: value" lines"""
    settings = {}
    for l in text.split("\n"):
        k, sep, v = l.partition(":")
        if sep and k.strip():
            settings[k.strip().lower()] = v.strip()
    return settings


def isSidebar(params, *args):
    """ Whether a "::: ..." block is a sidebar: "esb", or "esb-" and a category name """
    p = params.strip()
    return p == "esb" or re.fullmatch(r"esb-\S+", p) is not None


def documentBook(text):
    """The book code a Markdown document is typeset as (its front matter's "book", or MOD)"""
    m = re.match(r"---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", text, re.S)
    return frontMatter(m.group(1)).get("book", "MOD") if m else "MOD"


def outlineTitle(s):
    """s made safe for a bookmark title, which goes to TeX inside an attribute and on into a PDF string:
    straight double quotes become curly ones, a backslash a slash, and brackets that do not pair up
    square brackets."""
    s = re.sub(r'"([^"]*)"', "\u201c\\1\u201d", s).replace('"', "\u201d").replace("\\", "/")
    depth = 0
    for c in s:
        depth += {"(": 1, ")": -1}.get(c, 0)
        if depth < 0:
            break
    if depth != 0:
        s = s.replace("(", "[").replace(")", "]")
    return s


def nextMarker(marker):
    """The marker one level below: s4 -> s5, ms1 -> ms2, s -> s2"""
    m = re.match(r"^(.*?)(\d*)$", marker)
    return m.group(1) + str(int(m.group(2) or 1) + 1)


class MarkdownToUSX:

    charmap = {"strong": "bd", "em": "it", "s": "zs"}
    alignments = {"left": "", "right": "r", "center": "c"}

    def __init__(self, factory=ParentElement, mode=None):
        if front_matter_plugin is None:
            raise ImportError("Typesetting Markdown needs the mdit-py-plugins package: pip install mdit-py-plugins")
        self.md = (MarkdownIt("commonmark").enable("table").enable("strikethrough")
                   .use(front_matter_plugin).use(footnote_plugin)
                   .use(attrs_plugin, after=("image",))
                   .use(container_plugin, name="esb", validate=isSidebar))     # only "::: esb" and "::: esb-name"
        self.factory = factory
        self.mode = mode

    # --- settings ---
    def setup(self, settings):
        self.book = settings.get("book", "MOD")
        intro = self.mode == "intro"
        first = settings.get("headings", "").split() or ["is1" if intro else "s1"]
        self.headings = list(first[:6])
        while len(self.headings) < 6:
            self.headings.append(nextMarker(self.headings[-1]))
        try:
            self.outline = int(settings.get("outline", "2"))
        except ValueError:
            self.outline = 2
        self.parastyle = "ip" if intro else "p"
        self.liststyle = "ili" if intro else "li"
        self.quotestyle = settings.get("quote", "pi1")
        self.bullet = settings.get("bullet", "\u2022")

    # --- building ---
    def _el(self, tag, parent, style=None, **attrs):
        attrib = {"style": style} if style else {}
        attrib.update(attrs)
        el = self.factory(tag, parent=parent, attrib=attrib)
        parent.append(el)
        return el

    def _text(self, el, text):
        if len(el):
            el[-1].tail = (el[-1].tail or "") + text
        else:
            el.text = (el.text or "") + text

    def newPara(self, style):
        self.para = self._el("para", self.root, style)
        return self.para

    def blockStyle(self):
        """The paragraph marker for a paragraph here, and the text it starts with (a list number)"""
        if self.lists:
            depth = min(len(self.lists), 4)
            lst = self.lists[-1]
            prefix = ""
            if self.itemStart:
                self.itemStart = False
                prefix = f"{lst['n']}{lst['delim']} " if lst["ordered"] else (self.bullet + " " if self.bullet else "")
            return f"{self.liststyle}{depth}", prefix
        if self.quotes:
            return self.quotestyle, ""
        return self.parastyle, ""

    # --- inline ---
    def inline(self, target, children, heading=None):
        """Adds inline tokens to target (a para or cell). heading: (level, None) for a heading, whose
        trailing {#id} becomes an anchor."""
        children = list(children or [])
        if heading is not None:
            self.headingAnchor(target, children, heading)
        stack = [target]
        for c in children:
            t = c.type
            cur = stack[-1]
            if t in ("text", "text_special"):
                self._text(cur, c.content)
            elif t == "softbreak":
                self._text(cur, " ")
            elif t == "hardbreak":
                if len(stack) > 1 or target.tag != "para":
                    self._text(cur, " ")
                else:                           # the same paragraph style again, on a new line
                    target = self.newPara(target.get("style"))
                    stack = [target]
            elif t == "code_inline":
                el = self._el("char", cur, "zcode")
                el.text = c.content
            elif t.endswith("_open") and t[:-5] in self.charmap:
                stack.append(self._el("char", cur, self.charmap[t[:-5]]))
            elif t == "link_open":
                stack.append(self._el("char", cur, "jmp", **{"link-href": c.attrGet("href") or ""}))
            elif t.endswith("_close") and len(stack) > 1 and t[:-6] in list(self.charmap) + ["link"]:
                stack.pop()
            # raw HTML and images are left out (an image's text is kept)
            elif t == "footnote_ref":
                self.footnote(cur, c.meta["id"])
            elif t == "image":
                self.figure(cur, c)

    def headingAnchor(self, para, children, heading):
        level = heading
        last = children[-1] if children else None
        if last is None or last.type != "text":
            return
        m = HEADING_ID.search(last.content)
        if m is None:
            return
        last.content = last.content[:m.start()]
        title = "".join(c.content for c in children if c.type in ("text", "text_special", "code_inline")).strip()
        attrs = {"link-id": m.group(1)}
        if level <= self.outline and title:
            attrs["outline-entry"] = outlineTitle(title)
            attrs["outline-level"] = str(level)
        self._el("char", para, "jmp", **attrs)

    # --- figures and sidebars ---
    def figure(self, parent, img):
        """ \fig caption|src="..." alt="..." and any other attributes\fig* """
        attrs = {k: str(v) for k, v in img.attrs.items() if k not in ("src", "alt", "title") and v is not None}
        attrs["file"] = img.attrGet("src") or ""         # written as src="..." in USFM
        if img.attrGet("title"):
            attrs["alt"] = img.attrGet("title")
        fig = self._el("figure", parent, "fig", **attrs)
        self.inline(fig, img.children)

    def sidebar(self, info):
        """ The sidebar a "::: esb-name" block starts, of category name ("::: esb": none) """
        cat = info.strip()[4:]
        attrs = {"category": cat} if cat else {}
        self.boxes.append(self.root)
        self.root = self._el("sidebar", self.root, "esb", **attrs)

    # --- footnotes ---
    def takeFootnotes(self, tokens):
        """ Keeps each footnote's paragraphs (inline tokens' children) by its id, for when it is
            referred to, and returns the tokens without the footnotes block at the end """
        self.notes = {}
        out = []
        noteid = None
        for t in tokens:
            if t.type == "footnote_open":
                noteid = t.meta["id"]
                self.notes[noteid] = []
            elif t.type == "footnote_close":
                noteid = None
            elif noteid is not None:
                if t.type == "inline":
                    self.notes[noteid].append([c for c in t.children or [] if c.type != "footnote_anchor"])
            elif t.type not in ("footnote_block_open", "footnote_block_close"):
                out.append(t)
        return out

    def footnote(self, parent, noteid):
        """ A footnote at this point in parent: \f + \ft first paragraph \fp next ... \f* """
        note = self._el("note", parent, "f", caller="+")
        for k, kids in enumerate(self.notes.get(noteid, [])):
            self.inline(self._el("char", note, "ft" if k == 0 else "fp"), kids)

    # --- blocks ---
    def compile(self, md_text: str):
        tokens = self.md.parse(md_text)
        fm = tokens[0].content if tokens and tokens[0].type == "front_matter" else ""
        self.setup(frontMatter(fm))
        return self.compile_tokens(tokens)

    def compile_tokens(self, tokens):
        self.root = self.doc = self.factory("usx")      # root: where new paragraphs go (a sidebar's inside)
        self._el("book", self.root, "id", code=self.book)
        self.para = None
        self.lists = []         # {ordered, n, delim} for each open list
        self.itemStart = False
        self.quotes = 0
        self.row = None
        self.tablehead = False
        self.column = 0
        tokens = self.takeFootnotes(tokens)
        self.boxes = []         # the parents of the open sidebars
        for i, t in enumerate(tokens):
            ty = t.type
            if ty == "container_esb_open":
                self.sidebar(t.info)
            elif ty == "container_esb_close":
                self.root = self.boxes.pop()
            elif ty == "heading_open":
                level = int(t.tag[1])
                para = self.newPara(self.headings[level - 1])
                self.inline(para, tokens[i + 1].children, heading=level)
            elif ty == "paragraph_open":
                style, prefix = self.blockStyle()
                para = self.newPara(style)
                if prefix:
                    self._text(para, prefix)
                self.inline(para, tokens[i + 1].children)
            elif ty in ("bullet_list_open", "ordered_list_open"):
                self.lists.append({"ordered": ty == "ordered_list_open", "n": int(t.attrGet("start") or 1),
                                   "delim": t.markup or "."})
            elif ty in ("bullet_list_close", "ordered_list_close"):
                self.lists.pop()
            elif ty == "list_item_open":
                self.itemStart = True
            elif ty == "list_item_close":
                if self.itemStart:              # an empty item still takes its place (and number)
                    style, prefix = self.blockStyle()
                    self._text(self.newPara(style), prefix)
                self.lists[-1]["n"] += 1
            elif ty == "blockquote_open":
                self.quotes += 1
            elif ty == "blockquote_close":
                self.quotes -= 1
            elif ty in ("fence", "code_block"):
                for l in t.content.rstrip("\n").split("\n"):
                    self.newPara("zpre").text = l if l.strip() else " "
            elif ty == "hr":
                self.newPara("b")
            elif ty == "thead_open":
                self.tablehead = True
            elif ty == "thead_close":
                self.tablehead = False
            elif ty == "tr_open":
                self.row = self._el("row", self.root, "tr")
                self.column = 0
            elif ty in ("th_open", "td_open"):
                self.column += 1
                align = self.alignments.get((t.attrGet("style") or "").replace("text-align:", ""), "")
                kind = "h" if self.tablehead else "c"
                cell = self._el("cell", self.row, f"t{kind}{align}{self.column}")
                self.inline(cell, tokens[i + 1].children)
            # raw HTML blocks are left out
        return self.doc


def MarkDown(text):
    md = MarkdownToUSX()
    root = md.compile(text)
    res = USX(root)
    return res


def main():
    import sys
    if len(sys.argv) > 2:
        infile, outfile = sys.argv[1:3]
        with open(infile, encoding="utf-8") as inf:
            text = inf.read()
        doc = MarkDown(text)
        doc.saveAs(outfile)

if __name__ == "__main__":
    main()
