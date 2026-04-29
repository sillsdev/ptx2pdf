from markdown_it import MarkdownIt
from usfmtc.xmlutils import ParentElement
from usfmtc import USX


class MarkdownToUSX:

    typemap = {
        "paragraph":    lambda t: ("para", "p"),
        "heading":      lambda t: ("para", f"s{t[1]}"),
        "blockquote":   lambda t: ("para", "q1"),
        "strong":       lambda t: ("char", "bd"),
        "em":           lambda t: ("char", "it"),
        "table":        lambda t: ("table", None)
    }
    alignments = {
        "left":     "",
        "right":    "r",
        "center":   "c"
    }

    def __init__(self, factory=ParentElement):
        self.md = MarkdownIt("commonmark").enable("table", "strikethrough")
        self.factory = factory

    def _add_el(self, tag, style):
        el = self.factory(tag, parent=self.curr, attrib={"style": style})
        self.curr.append(el)
        self.curr = el
        return el

    def _add_text(self, text):
        if len(self.curr):
            self.curr[-1].tail = (self.curr[-1].tail or "") + text
        else:
            self.curr.text = (self.curr.text or "") + text

    def compile(self, md_text: str):
        root = self.factory("usx")
        root.append(self.factory("book", parent=root, attrib={"code": "MOD", "style": "id"}))
        self.curr = root
        tokens = self.md.parse(md_text)
        self.skip_para = False
        for t in tokens:
            isopen = True
            if t.type.endswith("_close"):
                isopen = False
                t.type = t.type[:-6]
            elif t.type.endswith("_open"):
                t.type = t.type[:-5]

            if t.type in self.typemap:
                if self.skip_para:
                    self.skip_para = isopen
                elif isopen:
                    tag, style = self.typemap[t.type](t.tag)
                    self._add_el(tag, style)
                else:
                    self.curr = self.curr.parent

            elif t.type == "code_block":
                el = self._add_el("para", "pre")
                el.text = t.content
                self.curr = self.curr.parent

            elif t.type == "list_item":
                if isopen:
                    el = self._add_el("para", "li")
                    self.skip_para = True
                else:
                    self.curr = self.curr.parent

            elif t.type == "inline":
                for c in t.children or []:
                    isopen = True
                    if c.type.endswith("_close"):
                        isopen = False
                        c.type = c.type[:-6]
                    elif c.type.endswith("_open"):
                        c.type = c.type[:-5]

                    if c.type == "text":
                        self._add_text(c.content)

                    elif c.type in self.typemap:
                        if isopen:
                            tag, style = self.typemap[c.type](c.tag)
                            self._add_el(tag, style)
                        else:
                            self.curr = self.curr.parent

                    # code
                    elif c.type == "code_inline":
                        el = self._add_el("char", "code")
                        el.text = c.content
                        self.curr = self.curr.parent

                    elif c.type == "link":
                        if isopen:
                            href = dict(c.attrs or {}).get("href", "")
                            el = self._add_el("char", "jmp")
                            el.set("href", href)
                        else:
                            self.curr = self.curr.parent

                    elif c.type == "softbreak":
                        self._add_text(" ")

            elif t.type == "thead":
                self.tablehead = isopen

            elif t.type == "tr":
                if isopen:
                    self._add_el("row", "tr")
                    self.column = 0
                    self.tablehead = False
                else:
                    self.curr = self.curr.parent

            elif t.type == "td":
                if isopen:
                    self.column += 1
                    align = self.alignments.get(t.style[11:], "")
                    t = "h" if self.tablehead else "c"
                    self._add_el("cell", f"t{t}{align}{self.column}")
                else:
                    self.curr = self.curr.parent

            elif t.type in ("html_block", "html_inline"):
                pass
        return root

def MarkDown(text):
    md = MarkdownToUSX()
    root = md.compile(text)
    res = USX(root)
    return res

