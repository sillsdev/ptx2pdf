from ptxprint.sfm import usfm
import re
from collections import namedtuple

RefRange = namedtuple("RefRange", ["fromc", "fromv", "toc", "tov"])

def load_stylesheets(sheets):
    stylesheet=usfm._load_cached_stylesheet('usfm.sty')
    for s in stylesheets:
        if s is not None:
            stylesheet = style.parse(open(s), base=stylesheet)
    return stylesheet


class Usfm:
    def __init__(fnameordoc, stylesheet=None):
        if isinstance(fnameordoc, str):
            with open(fnameordoc, encoding="utf-8") as inf:
                self.doc = list(usfm.parser(inf, stylesheet=stylesheet, purefootnotes=True))
        else:
            self.doc = fnameordoc
        self.cvaddorned = False

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

