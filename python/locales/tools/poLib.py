# Minimal PO reader/writer and placeholder validation (no third-party dependencies).
import re

_unescMap = {'n': '\n', 't': '\t', '"': '"', '\\': '\\'}


def unescape(s):
    return re.sub(r'\\(.)', lambda m: _unescMap.get(m.group(1), '\\' + m.group(1)), s)


def escape(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')


class Entry:
    def __init__(self):
        self.comments = []      # "# ..." and "#. ..." lines, verbatim
        self.refs = []          # source references from "#: " lines
        self.flags = []         # from "#, " lines
        self.msgid = ""
        self.msgstr = ""

    @property
    def isFuzzy(self):
        return 'fuzzy' in self.flags


def _readQuoted(line):
    line = line.strip()
    return unescape(line[1:-1])


def parsePo(path):
    """Return a list of Entry; the header (msgid "") is the first entry if present."""
    with open(path, encoding='utf-8') as f:
        return parsePoText(f.read(), path)


def parsePoText(text, path='<string>'):
    entries = []
    cur = None
    field = None
    lines = text.split('\n')
    for line in lines + ['']:
        if line.startswith('#~'):
            continue
        if not line.strip():
            if cur is not None and (cur.msgid or cur.msgstr or entries == [] or cur.refs):
                entries.append(cur)
            cur = None
            field = None
            continue
        if cur is None:
            cur = Entry()
        if line.startswith('#:'):
            cur.refs.extend(line[2:].split())
        elif line.startswith('#,'):
            cur.flags.extend(x.strip() for x in line[2:].split(','))
        elif line.startswith('#'):
            cur.comments.append(line)
        elif line.startswith('msgid '):
            field = 'msgid'
            cur.msgid = _readQuoted(line[6:])
        elif line.startswith('msgstr '):
            field = 'msgstr'
            cur.msgstr = _readQuoted(line[7:])
        elif line.startswith('"') and field:
            setattr(cur, field, getattr(cur, field) + _readQuoted(line))
        else:
            raise ValueError("Unsupported PO line in {}: {!r}".format(path, line))
    return entries


def _quoted(keyword, s, header=False):
    pieces = re.findall(r'[^\n]*\n|[^\n]+', s) or ['']
    if len(pieces) == 1 and not header:
        return '{} "{}"\n'.format(keyword, escape(pieces[0]))
    if header:
        out = '{} ""\n'.format(keyword)
        return out + ''.join('"{}"\n'.format(escape(p)) for p in pieces)
    out = '{} "{}"\n'.format(keyword, escape(pieces[0]))
    return out + ''.join('"{}"\n'.format(escape(p)) for p in pieces[1:])


def formatEntry(e):
    out = []
    out.extend(e.comments)
    if e.refs:
        out.append('#: ' + ' '.join(e.refs))
    if e.flags:
        out.append('#, ' + ', '.join(e.flags))
    text = ''.join(l + '\n' for l in out)
    isHeader = (e.msgid == "")
    text += _quoted('msgid', e.msgid)
    text += _quoted('msgstr', e.msgstr, header=isHeader)
    return text


def writePo(path, entries):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(formatEntry(e) for e in entries))


# ---- placeholder / markup validation -------------------------------------

_phRe = re.compile(r'\{\{|\}\}|\{[^{}\s]*\}|%\([^)]*\)[#0\-+]*\d*(?:\.\d+)?[sdifrxXeEgGc]'
                   r'|%[#0\-+]*\d*(?:\.\d+)?[sdifrxXeEgGc]|%%')
_tagRe = re.compile(r'</?[A-Za-z][^<>]*>')
_markerRe = re.compile(r'\\[A-Za-z][A-Za-z0-9]*\*?')


def _tokens(s):
    return sorted(_phRe.findall(s) + _tagRe.findall(s) + _markerRe.findall(s))


def isTranslatable(msgid):
    """False for TeX code, pure symbols/numbers and the header."""
    if not msgid.strip():
        return False
    if msgid.lstrip().startswith('\\'):
        return False
    return sum(c.isalpha() for c in msgid) >= 2


def fixWhitespace(msgid, msgstr):
    """Restore the leading/trailing whitespace of the English onto the translation."""
    core = msgstr.strip()
    lead = msgid[:len(msgid) - len(msgid.lstrip())]
    trail = msgid[len(msgid.rstrip()):]
    return lead + core + trail


def checkTranslation(msgid, msgstr):
    """Return a list of problems (empty list = acceptable)."""
    errs = []
    if not msgstr.strip():
        return ["translation is empty"]
    a, b = _tokens(msgid), _tokens(msgstr)
    if a != b:
        missing = list(a)
        extra = []
        for t in b:
            if t in missing:
                missing.remove(t)
            else:
                extra.append(t)
        if missing:
            errs.append("missing placeholders/markup: " + ' '.join(missing))
        if extra:
            errs.append("unexpected placeholders/markup: " + ' '.join(extra))
    if msgid.count('\n\n') != msgstr.count('\n\n'):
        errs.append("paragraph breaks (blank lines) must match the English: expected {}, got {}".format(
            msgid.count('\n\n'), msgstr.count('\n\n')))
    return errs
