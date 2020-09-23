from ptxprint.sfm import usfm, style
from ptxprint import sfm
import re, os
from collections import namedtuple

RefRange = namedtuple("RefRange", ["fromc", "fromv", "toc", "tov"])

class _Reference(sfm.Position):
    def __new__(cls, pos, ref):
        p = super().__new__(cls, *pos)
        p.book = ref[0]
        p.chapter = ref[1]
        p.verse = ref[2]
        return p

class Sheets:
    def __init__(self, init=[]):
        self.sheet = usfm.default_stylesheet.copy()
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
        ref = [None] * 3
        def _g(_, e):
            if isinstance(e, sfm.Element):
                if e.name == 'id':
                    ref[0] = str(e[0]).split()[0]
                elif e.name == 'c':
                    ref[1] = e.args[0]
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
