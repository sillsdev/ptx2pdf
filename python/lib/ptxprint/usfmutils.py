from ptxprint.sfm import usfm, style
from ptxprint import sfm
import re, os
from collections import namedtuple
from itertools import groupby

RefRange = namedtuple("RefRange", ["fromc", "fromv", "toc", "tov"])

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
        return p

class Sheets:
    def __init__(self, init=[]):
        self.sheet = {k: v.copy() for k, v in usfm.default_stylesheet.items()}
        for s in init:
            self.append(s)

    def append(self, sf):
        if os.path.exists(sf):
            with open(sf) as s:
                self.sheet = style.update_sheet(self.sheet, style.parse(s))

class Usfm:
    def __init__(self, iterable, sheets):
        tag_escapes = r"[^0-9A-Za-z]"
        self.doc = list(usfm.parser(iterable, stylesheet=sheets.sheet,
                                    canonicalise_footnotes=False,
                                    tag_escapes=tag_escapes))
        self.cvaddorned = False

    def __str__(self):
        return sfm.generate(self.doc)

    def addorncv(self):
        if self.cvaddorned:
            return
        self.chapters = []
        ref = [None] * 3
        def _g(_, e):
            if isinstance(e, sfm.Element):
                if e.name == 'id':
                    ref[0] = str(e[0]).split()[0]
                elif e.name == 'c':
                    ref[1] = e.args[0]
                    if ref[1] == len(self.chapters):
                        self.chapters.append(e)
                    else:
                        if ref[1] > len(self.chapters):
                            self.chapters += [None] * (ref[i] - len(self.chapters) + 1)
                        self.chapters[ref[1]] = e
                elif e.name == 'v':
                    ref[2] = e.args[0]
                return reduce(_g, e, None)
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

    def subdoc(self, refs, title=False, intro=False):
        ''' Creates a document consisting of only the text covered by the reference
            ranges. refs is a list of ranges of the form:
                (frombk, fromc, fromv, toc, tov)
            The list must include overlapping ranges'''
        self.addorncv()
        ranges = {}
        for r in refs:
            ranges.setdefault(r[0], []).append(RefRange(*r[1:]))
        for r in ranges.values:
            r.sort()
        def isintro(e):
            return e.pos.chapter is None
        def istitle(e):
            return e.pos.chapter is None and e.parent.name == "id" and not e.name.startswith("i")
        def filt(e):
            if e.parent is None:
                return True
            elif e.parent.name == "id" and e.name in ("h", "cl"):
                return True
            elif istitle(e):
                return title
            elif isintro(e):
                return intro
            for r in ranges[e.pos.book]:
                if ((r.fromc == e.pos.chapter and e.pos.verse >= r.fromv) or r.fromc < e.pos.chapter) \
                        and ((r.toc == e.pos.chapter and e.pos.verse <= r.tov) or r.toc > e.pos.chapter):
                    return True
            return False
        return self.doc.sfilter(filt, self.doc)

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

