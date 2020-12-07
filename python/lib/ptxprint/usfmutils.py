from ptxprint.sfm import usfm, style
from ptxprint import sfm
import re, os, traceback
from collections import namedtuple
from itertools import groupby
from functools import reduce
from copy import deepcopy

verse_reg = re.compile(r"^\s*(\d+)(\D*?)(?:\s*(-)\s*(\d+)(\D*?))?\s*$")
def make_rangetuple(chap, verse, start=True):
    m = verse_reg.match(verse)
    if m:
        if m.group(3) and not start:
            return (int(chap), int(m.group(4)), m.group(5))
        else:
            return (int(chap), int(m.group(1)), m.group(2))
    else:
        return (int(chap), 0, verse)

class RefRange(namedtuple("RefRange", ["fromc", "fromv", "toc", "tov"])):
    def __init__(self, *a, **kw):
        super().__init__()
        self.start = make_rangetuple(self[0], self[1])
        self.end = make_rangetuple(self[2], self[3], start=False)

def isScriptureText(e):
    if 'nonvernacular' in e.meta.get('TextProperties', []):
        return False
    if e.name in ("h", "id"):
        return False
    return True

takslc_cats = {'Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Sm', 'Sc', 'Sk', 'So',
               'Nd', 'Nl', 'No', 
               'Pd', 'Pc', 'Pe', 'Ps', 'Pi', 'Pf', 'Po'}
space_cats = { 'Zs', 'Zl', 'Zp', 'Cf' }

class _Reference(sfm.Position):
    def __new__(cls, pos, ref):
        p = super().__new__(cls, *pos[:2])
        p.book = ref[0]
        p.chapter = ref[1]
        p.verse = ref[2]
        p.startref = make_rangetuple(p.chapter, p.verse)
        p.endref = make_rangetuple(p.chapter, p.verse, start=False)
        return p

    def __str__(self):
        return f"{self.book} {self.chapter}:{self.verse} line {self.line},{self.col}"

    def cmp_range(self, r):
        if self.endref < r.start:
            return -1
        elif self.startref > r.end:
            return 1
        return 0

class Sheets(dict):

    default = usfm._load_cached_stylesheet('usfm_sb.sty')

    def __init__(self, init=[], base=None):
        self.update(deepcopy(base) if base is not None else deepcopy(self.default))
        if init is None or not len(init):
            return
        for s in init:
            if os.path.exists(s):
                self.append(s)

    def append(self, sf):
        if os.path.exists(sf):
            with open(sf) as s:
                self.update_sheet(style.parse(s))

    def update_sheet(self, d):
        style.update_sheet(self, d, field_replace=True)

    def copy(self):
        return Sheets(base=self)

    def add_parparent(self, marker):
        for k, v in self.items():
            if 'p' in v['OccursUnder']:
                v['OccursUnder'].add(marker)

    def remove_parparent(self, marker):
        for k, v in self.items():
            v['OccursUnder'].discard(marker)


class UsfmCollection:
    def __init__(self, bkmapper, basedir, sheets):
        self.bkmapper = bkmapper
        self.basedir = basedir
        self.sheets = sheets
        self.books = {}
        self.tocs = []

    def get(self, bk):
        if bk not in self.books:
            bkfile = self.bkmapper(bk)
            if bkfile is None:
                return None
            bkfile = os.path.join(self.basedir, bkfile)
            if not os.path.exists(bkfile):
                return None
            with open(bkfile, encoding="utf-8") as inf:
                self.books[bk] = Usfm(inf, self.sheets)
        return self.books[bk]

class Usfm:
    def __init__(self, iterable, sheets):
        tag_escapes = r"[^0-9A-Za-z]"
        try:
            self.doc = list(usfm.parser(iterable, stylesheet=sheets,
                                    canonicalise_footnotes=False,
                                    tag_escapes=tag_escapes))
        except:
            traceback.print_exc()
        self.cvaddorned = False
        self.tocs = []

    def __str__(self):
        return sfm.generate(self.doc)

    def addorncv(self):
        if self.cvaddorned:
            return
        ispara = sfm.text_properties('paragraph')
        self.chapters = []
        ref = ["", "0", "0"]
        pending = []

        def isHeading(e):
            if not isinstance(e, sfm.Element):
                return False
            if e.meta.get('StyleType', '').lower() != 'paragraph':
                return False
            if e.meta.get('TextType', '').lower() == 'section':
                return True
            return False

        def _g(_, e):
            if isinstance(e, sfm.Element):
                if e.name == 'id':
                    ref[0] = str(e[0]).split()[0]
                elif e.name == 'c':
                    ref[1] = e.args[0]
                    c = int(ref[1])
                    if c == len(self.chapters):
                        self.chapters.append(e)
                    else:
                        if c > len(self.chapters):
                            self.chapters += [None] * (c - len(self.chapters) + 1)
                        self.chapters[c] = e
                    ref[2] = "0"
                elif e.name == 'v':
                    ref[2] = e.args[0]
                    for t in pending:
                        t.pos = _Reference(t.pos, ref)
                    pending.clear()
                elif ref[2] != "0":
                    if isHeading(e) or len(pending):
                        pending.append(e)
                e.pos = _Reference(e.pos, ref)
                reduce(_g, e, None)
            else:
                if len(pending):
                    pending.append(e)
                else:
                    e.pos = _Reference(e.pos, ref)
        reduce(_g, self.doc, None)
        self.cvaddorned = True

    def readnames(self):
        if len(self.tocs) > 0:
            return
        for c in self.doc[0]:       # children of id
            if not isinstance(c, sfm.Element) or c.name != "h":
                continue
            for e in c:
                if not isinstance(e, sfm.Element):
                    continue
                m = re.match(r"^toc(\d)", e.name)
                if m:
                    ind = int(m.group(1))
                    if ind > len(self.tocs):
                        self.tocs.extend([""] * (ind - len(self.tocs) + 1))
                    self.tocs[ind-1] = e[0]

    def getwords(self, init=None, constrain=None):
        ''' Counts words found in the document. If constrain then is a set or
            list that contains words to count, ignoring all others. Returns
            a dict of words: counts. '''
        wre = re.compile(r"(\w+)")
        if init is None:
            init = {}
        def addwords(s, a):
            for w in wre.split(s)[1::2]:
                if constrain is None or w in constrain:
                    a[w] = a.get(w, 0) + 1
        def nullelement(e, a, c):
            pass
        words = self.sreduce(nullelement, addwords, self.doc, init)
        return words

    def subdoc(self, ref, removes={}, strippara=False):
        ''' Creates a document consisting of only the text covered by the reference
            ranges. ref is a tuple in the form:
                (fromc, fromv, toc, tov)
            The list must include overlapping ranges'''
        self.addorncv()
        ispara = sfm.text_properties('paragraph')
        r = RefRange(*ref)
        chaps = self.chapters[r.start[0]:r.end[0]+1]
        def pred(e):
            if isinstance(e.pos, _Reference) and e.pos.cmp_range(r) == 0:
                if strippara and isinstance(e, sfm.Element) and ispara(e):
                    return False
                return True
            return False

        def _g(a, e):
            if isinstance(e, sfm.Text):
                if pred(e):
                    a.append(sfm.Text(e, e.pos, a or None))
                return a
            if e.name in removes:
                return a
            e_ = sfm.Element(e.name, e.pos, e.args, parent=a or None, meta=e.meta)
            reduce(_g, e, e_)
            if pred(e):
                a.append(e_)
            elif len(e_):
                a.extend(e_[:])
            return a
        return reduce(_g, chaps, [])

    def iter(self, e):
        def iterfn(el):
            yield el
            if isinstance(el, sfm.Element):
                for c in el:
                    for c1 in iterfn(c):
                        yield c1
        return iterfn(e)

    def iterVerse(self, chap, verse):
        start = self.chapters[chap]
        it = self.iter(start)
        for e in it:
            if not isinstance(e, sfm.Element):
                continue
            if e.name == "c" and int(e.args[0]) != chap:
                print(e.name, e.args, len(e))
                return
            elif e.name == "v" and e.args[0] == verse:
                yield e
                break
        else:
            return
        for e in it:
            yield e
            if not isinstance(e, sfm.Element):
                continue
            if e.name == "c" or e.name == "v":
                break

    def normalise(self):
        ''' Normalise USFM in place '''
        ispara = sfm.text_properties("paragraph")
        def ensurenl(i, e):
            ''' Ensure element ends with a newline, if not already present.
                Passed index in parent and element. '''
            if isinstance(e, sfm.Element):
                if len(e):
                    ensurenl(len(e)-1, e[-1])
                else:
                    e.append(sfm.Text("\n", e.pos, e.parent))
                    return True
            elif not e.endswith("\n"):
                e.parent.insert(i+1, sfm.Text("\n", e.pos, e.parent))
                return True
            return False
        def ge(i, e):
            ''' Iterate document allowing in place editing '''
            res = False
            if isinstance(e, sfm.Element):
                if ispara(e) or e.name == "v":
                    if i > 0:
                        res = ensurenl(i-1, e.parent[i-1])
                j = 0
                while j < len(e):
                    if ge(j, e[j]):
                        j += 1
                    j += 1
            return res
        ge(0, self.doc[0])

    def _proctext(self, fn, doc=None):
        def _g(e):
            if isinstance(e, sfm.Element):
                e[:] = map(_g, e)
                return e
            else:
                return fn(e)
        if doc is None:
            self.doc = map(_g, self.doc)
            return self.doc
        else:
            return map(_g, doc)

    def transform_text(self, *regs, doc=None):
        """ Given tuples of (lambda, match, replace) tests the lambda against the
            parent of a text node and if matches (or is None) does match and replace. """
        def fn(e):
            s = str(e)
            processed = False
            for r in regs:
                if r[0] is not None and not r[0](e.parent):
                    continue
                ns = r[1].sub(r[2], s)
                if ns != s:
                    processed = True
                    s = ns
            if processed:
                return sfm.Text(s, e.pos, e.parent)
            else:
                return e
        self._proctext(fn, doc=doc)

    def letter_space(self, inschar, doc=None):
        from ptxprint.sfm.ucd import get_ucd
        def fn(e):
            if not isScriptureText(e.parent):
                return e
            done = False
            lastspace = False
            res = []
            for (islet, c) in groupby(str(e), key=lambda x:get_ucd(ord(x), "gc") in takslc_cats):
                chars = "".join(c)
                # print("{} = {}".format(chars, islet))
                if not len(chars):
                    continue
                if islet:
                    res.append(("" if lastspace else inschar) + inschar.join(chars))
                    done = True
                else:
                    res.append(chars)
                lastspace = get_ucd(ord(chars[-1]), "gc") in space_cats
            # if done:
                # print("{} -> {}".format(e, "".join(res)))
            return sfm.Text("".join(res), e.pos, e.parent) if done else e
        self._proctext(fn, doc=doc)

def read_module(inf, sheets):
    lines = inf.readlines()
    if not re.match(r"\uFEFF?\\id\s", lines[0]):
        lines.insert(0, "\\id MOD Module\n")
    return Usfm(lines, sheets)

def parse_refs(s):
    bits = re.split(r"([,;])", s)
    bk = ""
    c = "0"
    for ref, sep in zip(bits[::2], [""] + bits[1::2]):
        m = re.match(r"^\s*([A-Z]{3})?\s*(\d+[a-z]?)\s*(?:([.:])\s*(\d*[a-z]?))?\s*(?:(-)\s*(\d*[a-z]?)\s*(?:([.:])\s*(\d*[a-z]?))?)?", ref)
        if m:
            bk = m.group(1) or bk
            if m.group(3):
                firstc = m.group(2) or c
                firstv = m.group(4)
            elif sep == ",":
                firstc = c
                firstv = m.group(2)
            else:
                firstc = m.group(2) or c
                firstv = "0"
            if m.group(5):
                if m.group(7):
                    c = m.group(6) or firstc
                    lastv = m.group(8) or "200"
                elif firstv == "":
                    c = m.group(6) or firstc
                    lastv = "200"
                else:
                    c = firstc
                    lastv = m.group(6) or "200"
            else:
                c = firstc
                lastv = "200" if firstv == "0" else firstv
            yield (bk, firstc, firstv or "0", c, lastv or "0")
        else:
            print("Bad ref: {}".format(ref))

exclusionmap = {
    'v': ['v'],
    'x': ['x'],
    'f': ['f'],
    's': ['s', 's1', 's2'],
    'p': ['fig']
}

class Module:

    localise_re = re.compile(r"\$([asl]?)\(\s*(\S+)\s+(\d+):([^)\s]+)\s*\)")
    localcodes = {'a': 3, 's': 2, 'l': 1}

    def __init__(self, fname, usfms):
        self.fname = fname
        self.usfms = usfms
        self.sheets = self.usfms.sheets.copy()
        modinfo = { 'OccursUnder': {'id'}, 'TextType': 'Other', 'EndMarker': None, 'StyleType': 'Paragraph'}
        modsheet = {k: style.Marker(modinfo) for k in ('inc', 'vrs', 'ref', 'refnp', 'rep', 'mod')}
        self.sheets.update(modsheet)
        for k, v in self.sheets.items():
            if 'OccursUnder' in v and 'c' in v['OccursUnder']:
                v['OccursUnder'].add('id')
        with open(fname, encoding="utf-8") as inf:
            self.doc = read_module(inf, self.sheets)

    def parse(self):
        self.removes = set()
        final = sum(map(self.parse_element, self.doc.doc), [])
        return final

    def localref(self, m):
        loctype = m.group(1) or "a"
        bk = m.group(2)
        c = m.group(3)
        v = m.group(4)
        book = self.usfms.get(bk)
        if book is None:
            return ''
        book.readnames()
        tocindex = self.localcodes.get(loctype.lower(), 0)
        if tocindex > len(book.tocs):
            return ''
        else:
            return '{} {}:{}'.format(book.tocs[tocindex-1], c, v)

    def parse_element(self, e):
        if isinstance(e, sfm.Text):
            t = self.localise_re.sub(self.localref, e)
            if t != e:
                return [sfm.Text(t, e.pos, e.parent)]
            return [e]
        elif e.name == "ref" or e.name == "refnp":
            res = []
            isidparent = e.parent is None or e.parent.name == "id"
            reps = []
            curr = e.parent.index(e)
            while curr + 1 < len(e.parent):
                rep = e.parent[curr+1]
                if rep.name != "rep":
                    break
                # parse rep
                m = re.match("^\s*(.*?)\s*=>\s*(.*?)\s*$", rep[0], re.M)
                if m:
                    reps.append((None,
                            re.compile(r"(?<=\s|^)"+m.group(1).replace("...","[^\n\r]+")+"(\\b|(?=\\s)|$)",
                            m.group(2))))
                del e.parent[curr+1]
            for r in parse_refs(e[0]):
                p = self.get_passage(r, removes=self.removes, strippara=e.name=="refnp")
                if e.name == "ref":
                    for i, t in enumerate(p):
                        if isinstance(t, sfm.Element) and t.meta.get('StyleType', '').lower() == 'paragraph':
                            if i:
                                p[0:i] = [self.new_element(e, "p1" if isidparent else "p", p[0:i])]
                            break
                    else:
                        p = [self.new_element(e, "p1" if isidparent else "p", p)]
                res.extend(p)
            if len(reps):
                res = self.doc.transform_text(*reps, doc=res)
            return res
        elif e.name == 'inc':
            s = "".join(e).strip()
            for c in s:
                if c == "-":
                    self.removes = set(sum(exclusionmap.values(), []))
                else:
                    self.removes.difference_update(exclusionmap.get(c, []))
        elif e.name == 'mod':
            mod = Module(e[0].strip(), self.usfms)
            return mod.parse()
        else:
            cs = sum(map(self.parse_element, e), [])
            e[:] = cs
        return [e]

    def get_passage(self, ref, removes={}, strippara=False):
        book = self.usfms.get(ref[0])
        if book is None:
            return []
        return book.subdoc(ref[1:], removes=removes, strippara=strippara)

    def new_element(self, e, name, content):
        return sfm.Element(name, e.pos, [], e.parent, content=[sfm.Text("\n", e.pos)] \
                                                        + content, meta=self.sheets[name])

