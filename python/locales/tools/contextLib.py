# Gathers context for each msgid: glade widget info and Python call-site snippets.
import os
import xml.etree.ElementTree as ET

_kindMap = {'tooltip-text': 'tooltip', 'tooltip_text': 'tooltip', 'label': 'label', 'title': 'title',
            'text': 'text', 'placeholder-text': 'placeholder', 'col': 'list item', 'item': 'list item'}


class GladeIndex:
    """Maps an English string to where it occurs in ptxprint.glade."""

    def __init__(self, path):
        self.items = {}     # msgid -> list of dict(kind, widget, cls, path, note)
        self.order = {}     # msgid -> document order of first occurrence
        self.byOwner = {}   # widget -> its translatable strings (a label and its tooltip share one)
        if path and os.path.exists(path):
            self._parse(path)

    def _parse(self, path):
        stack = []
        count = 0
        for ev, el in ET.iterparse(path, events=('start', 'end')):
            if ev == 'start':
                stack.append(el)
                continue
            if el.get('translatable') == 'yes' and el.text:
                objs = [e for e in stack if e.tag in ('object', 'template')]
                owner = objs[-1] if objs else None
                named = [o.get('id') for o in objs[:-1] if o.get('id')]
                key = el.get('name') or el.tag
                info = {
                    'kind': _kindMap.get(key, key),
                    'widget': (owner.get('id') or '') if owner is not None else '',
                    'cls': owner.get('class') if owner is not None else '',
                    'path': named[-3:],
                    'note': el.get('comments', ''),
                    'owner': id(owner),
                }
                self.items.setdefault(el.text, []).append(info)
                self.order.setdefault(el.text, count)
                self.byOwner.setdefault(id(owner), []).append(el.text)
                count += 1
            stack.pop()

    def lookup(self, msgid):
        hits = self.items.get(msgid, [])
        if not hits:
            return None
        return hits[0]

    def sameWidget(self, msgid):
        """Other translatable strings on the same widget (e.g. the tooltip of this label)."""
        hit = self.lookup(msgid)
        if not hit:
            return []
        return [t for t in self.byOwner.get(hit['owner'], []) if t != msgid]


class CodeContext:
    """Returns a few lines of Python source around a reference like lib/ptxprint/gtkview.py:123."""

    def __init__(self, root, radius=2):
        self.root = root
        self.radius = radius
        self.cache = {}

    def snippet(self, ref):
        if ':' not in ref:
            return ''
        fname, _, ln = ref.rpartition(':')
        if not fname.endswith('.py') or not ln.isdigit():
            return ''
        if fname not in self.cache:
            p = os.path.join(self.root, fname)
            try:
                with open(p, encoding='utf-8', errors='replace') as f:
                    self.cache[fname] = f.read().split('\n')
            except OSError:
                self.cache[fname] = []
        lines = self.cache[fname]
        n = int(ln)
        lo, hi = max(0, n - 1 - self.radius), min(len(lines), n + self.radius)
        return '\n'.join(l.rstrip() for l in lines[lo:hi]).strip()
