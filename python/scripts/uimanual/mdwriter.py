#!/usr/bin/env python3
r"""
Writes markdown-it tokens (CommonMark plus tables and strikethrough) back out as Markdown.

The manual's links and heading ids are added to the token stream (see htmlmanual.Linker), so the way to
get Markdown with those links in it is to write the tokens out again. A heading with an "id" attribute
is written as "Title {#id}", which markdown.py (and Pandoc, kramdown, ...) read as the heading's anchor.

The output parses back to the same tokens; the spelling of the source may change (escapes, list
markers, spacing), not its meaning.
"""

import re

from markdown_it.tree import SyntaxTreeNode

# Characters that could start markup anywhere in a line: "\\" only before punctuation (\q1 stays), "_" only at the edge of a word (a_b is never
# emphasis), "&" only where it would read as an entity, "!" only before "[" (an image)
INLINE_SPECIAL = re.compile(r"(\\(?=[!-/:-@\[-`{-~]|$)|[`*\[\]<]|(?<!\w)_|_(?!\w)|&(?=#?\w+;)|!(?=\[))")
# Things that would start a block if they began a line
LINE_START = re.compile(r"^(\s*)([#>+=-]|\d+[.)]|~~~|```)")


def escapeText(s, inTable=False):
    s = INLINE_SPECIAL.sub(r"\\\1", s)
    if inTable:
        s = s.replace("|", r"\|")
    return s


def escapeLineStart(m):
    mark = m.group(2)
    if mark[0].isdigit():               # "1." -> "1\.": the delimiter is what makes the list item
        return m.group(1) + mark[:-1] + "\\" + mark[-1]
    return m.group(1) + "\\" + mark


def codeSpan(s):
    """Backticks around s: one more than the longest run of backticks in it."""
    runs = [len(m) for m in re.findall(r"`+", s)]
    fence = "`" * (max(runs) + 1 if runs else 1)
    pad = " " if s.startswith("`") or s.endswith("`") or (s.startswith(" ") and s.endswith(" ") and s.strip()) else ""
    return fence + pad + s + pad + fence


def linkDest(href, title):
    dest = f"<{href}>" if re.search(r"[\s()<>]", href) else href
    if title:
        dest += ' "' + title.replace('"', r'\"') + '"'
    return dest


class MarkdownWriter:

    def __init__(self, inTable=False):
        self.inTable = inTable

    def write(self, tokens):
        return self.blocks(SyntaxTreeNode(tokens).children).rstrip("\n") + "\n"

    # --- inline ---
    def inline(self, node, lineStarts=True):
        """Text of an inline node. lineStarts: escape a line that would start a block (a heading, list
        item, quote ...); not needed in a heading, which is one line after its "#"s."""
        text = "".join(self.span(c) for c in node.children)
        if not lineStarts:
            return text
        return "\n".join(LINE_START.sub(escapeLineStart, l) for l in text.split("\n"))

    def span(self, n):
        t = n.type
        if t == "text":
            return escapeText(n.content, self.inTable)
        if t == "softbreak":
            return "\n"
        if t == "hardbreak":
            return "\\\n"
        if t == "code_inline":
            s = codeSpan(n.content)
            return s.replace("|", r"\|") if self.inTable else s
        if t == "html_inline":
            return n.content
        if t in ("strong", "em", "s"):
            mark = n.markup or {"strong": "**", "em": "*", "s": "~~"}[t]
            return mark + "".join(self.span(c) for c in n.children) + mark
        if t == "link":
            inner = "".join(self.span(c) for c in n.children)
            href = n.attrGet("href") or ""
            if n.markup == "autolink":
                return f"<{href}>"
            return f"[{inner}]({linkDest(href, n.attrGet('title'))})"
        if t == "image":
            alt = "".join(self.span(c) for c in n.children)
            return f"![{alt}]({linkDest(n.attrGet('src') or '', n.attrGet('title'))})"
        raise ValueError(f"mdwriter: no rule for inline token {t}")

    # --- blocks ---
    def blocks(self, nodes, tight=False):
        parts = [self.block(n) for n in nodes]
        return ("\n" if tight else "\n\n").join(p for p in parts if p is not None)

    def block(self, n):
        t = n.type
        if t == "heading":
            text = self.inline(n.children[0], lineStarts=False).replace("\n", " ")
            hid = n.attrGet("id")
            return "#" * int(n.tag[1]) + " " + text + (f" {{#{hid}}}" if hid else "")
        if t == "paragraph":
            return self.inline(n.children[0])
        if t == "inline":
            return self.inline(n)
        if t in ("bullet_list", "ordered_list"):
            return self.list(n)
        if t == "blockquote":
            body = self.blocks(n.children)
            return "\n".join("> " + l if l else ">" for l in body.split("\n"))
        if t == "fence":
            mark = n.markup or "```"
            return f"{mark}{n.info}\n{n.content}{mark}"
        if t == "code_block":
            return "\n".join("    " + l if l else "" for l in n.content.rstrip("\n").split("\n"))
        if t == "hr":
            return "---"
        if t == "html_block":
            return n.content.rstrip("\n")
        if t == "table":
            return self.table(n)
        raise ValueError(f"mdwriter: no rule for block token {t}")

    def list(self, n):
        ordered = n.type == "ordered_list"
        start = int(n.attrGet("start") or 1) if ordered else None
        tight = all(p.hidden for item in n.children for p in item.children if p.type == "paragraph")
        items = []
        for i, item in enumerate(n.children):
            marker = f"{start + i}{item.markup or '.'} " if ordered else f"{item.markup or '-'} "
            body = self.blocks(item.children, tight=tight)
            lines = body.split("\n") if body else [""]
            pad = " " * len(marker)
            items.append("\n".join([marker + lines[0]] + [(pad + l if l else "") for l in lines[1:]]))
        return ("\n" if tight else "\n\n").join(items)

    def table(self, n):
        rows, aligns = [], []
        for sect in n.children:                 # thead, tbody
            for tr in sect.children:
                cells = []
                for cell in tr.children:
                    w = MarkdownWriter(inTable=True)
                    cells.append(w.inline(cell.children[0]).replace("\n", " ") if cell.children else "")
                    if sect.type == "thead":
                        style = cell.attrGet("style") or ""
                        aligns.append(style.replace("text-align:", ""))
                rows.append(cells)
        delim = [{"left": ":--", "right": "--:", "center": ":-:"}.get(a, "---") for a in aligns]
        lines = ["| " + " | ".join(rows[0]) + " |", "| " + " | ".join(delim) + " |"]
        lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
        return "\n".join(lines)


def tokensToMarkdown(tokens):
    return MarkdownWriter().write(tokens)
