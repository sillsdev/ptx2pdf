from ptxprint.sfm import usfm, style
from ptxprint import sfm
import re, os
from collections import namedtuple
from itertools import groupby
from functools import reduce

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
        p = super().__new__(cls, *pos)
        p.book = ref[0]
        p.chapter = ref[1]
        p.verse = ref[2]
        p.startref = make_rangetuple(p.chapter, p.verse)
        p.endref = make_rangetuple(p.chapter, p.verse, start=False)
        return p

    def cmp_range(self, r):
        if self.endref < r.start:
            return -1
        elif self.startref > r.end:
            return 1
        return 0

class Sheets(dict):
    def __init__(self, init=[], base=None):
        self.update({k: v.copy() for k, v in \
                        (base.items() if base is not None else usfm.default_stylesheet.items())})
        if init is None or not len(init):
            return
        for s in init:
            self.append(s)

    def append(self, sf):
        if os.path.exists(sf):
            with open(sf) as s:
                self.update_sheet(style.parse(s))

    def update_sheet(self, d):
        style.update_sheet(self, d)

    def copy(self):
        return Sheets(base=self)

class UsfmCollection:
    def __init__(self, bkmapper, basedir, sheets):
        self.bkmapper = bkmapper
        self.basedir = basedir
        self.sheets = sheets
        self.books = {}

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
        self.doc = list(usfm.parser(iterable, stylesheet=sheets,
                                    canonicalise_footnotes=False,
                                    tag_escapes=tag_escapes))
        self.cvaddorned = False

    def __str__(self):
        return sfm.generate(self.doc)

    def addorncv(self):
        if self.cvaddorned:
            return
        self.chapters = []
        ref = ["", "0", "0"]
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
                e.pos = _Reference(e.pos, ref)
                reduce(_g, e, None)
            else:
                e.pos = _Reference(e.pos, ref)
        reduce(_g, self.doc, None)
        self.cvaddorned = True

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

    def subdoc(self, ref, removes={}):
        ''' Creates a document consisting of only the text covered by the reference
            ranges. ref is a tuple in the form:
                (fromc, fromv, toc, tov)
            The list must include overlapping ranges'''
        self.addorncv()
        r = RefRange(*ref)
        chaps = self.chapters[r.start[0]:r.end[0]+1]
        def pred(e):
            if isinstance(e.pos, _Reference) and e.pos.cmp_range(r) == 0:
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

    def _proctext(self, fn):
        def _g(e):
            if isinstance(e, sfm.Element):
                e[:] = map(_g, e)
                return e
            else:
                return fn(e)
        self.doc = map(_g, self.doc)

    def transform_text(self, *regs):
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
        self._proctext(fn)

    def letter_space(self, inschar):
        from ptxprint.sfm.ucd import get_ucd
        def fn(e):
            if not isScriptureText(e.parent):
                return e
            done = False
            lastspace = False
            res = []
            for (islet, c) in groupby(e, key=lambda x:get_ucd(ord(x), "gc") in takslc_cats):
                chars = "".join(c)
                print("{} = {}".format(chars, islet))
                if not len(chars):
                    continue
                if islet:
                    res.append(("" if lastspace else inschar) + inschar.join(chars))
                    done = True
                else:
                    res.append(chars)
                lastspace = get_ucd(ord(chars[-1]), "gc") in space_cats
            if done:
                print("{} -> {}".format(e, "".join(res)))
            return sfm.Text("".join(res), e.pos, e.parent) if done else e
        self._proctext(fn)

class Module:
    def __init__(self, fname, usfms):
        self.fname = fname
        self.usfms = usfms
        self.removes = set()
        self.sheets = usfm.sheets.copy()
        modinfo = { 'OccursUnder': {'id'}, 'TextType': 'Other', 'EndMarker': None, 'StyleType': 'Paragraph'}
        modsheet = {k: marker(modinfo) for k in ('inc', 'vrs', 'ref', 'refnp', 'rep', 'mod')}
        self.sheets.update(modsheet)
        with open(fname, encoding="utf-8") as inf:
            self.doc = read_module(inf, self.sheets)

    def parse(self):
        final = sum(map(self.parse_element, self.doc.doc), start=[])
        return final
        
    def parse_element(self, e):
        if isinstance(e, sfm.Text):
            return [e]
        elif e.name == "ref" or e.name == "refn":
            res = []
            for r in parse_refs(e[0]):
                p = self.get_passage(r, removes=self.removes)
                for i, t in enumerate(p):
                    if isinstance(t, sfm.Element) and t.meta.get('StyleType', '') == 'Paragraph':
                        if i:
                            p[0:i] = [self.new_element(e, "p" if e.name == "ref" else "np", p[0:i])]
                        break
                else:
                    p = [self.new_element(e, "p" if e.name == "ref" else "np", p)]
                res.extend(p)
            return res
        elif e.name == 'inc':
            s = "".join(e).strip()
            for c in s:
                if c == "-":
                    self.removes = set(sum(exclusionmap.values(), []))
                else:
                    self.removes.difference_update(exclusionmap.get(c, []))
        else:
            cs = sum(map(self.parse_element, e), start=[])
            e[:] = cs
        return [e]

    def get_passage(self, ref, removes={}):
        book = self.usfms.get(ref[0])
        if book is None:
            return []
        return book.subdoc(ref[1:], removes=removes)

    def new_element(self, e, name, content):
        return sfm.Element(name, e.pos, [], e.parent, content=[sfm.Text("\n", e.pos)] \
                                                        + content, meta=self.sheets.sheet[name])

