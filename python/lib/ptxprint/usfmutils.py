from ptxprint.sfm import usfm
import re

def load_stylesheets(sheets):
    stylesheet=usfm._load_cached_stylesheet('usfm.sty')
    for s in stylesheets:
        if s is not None:
            stylesheet = style.parse(open(s), base=stylesheet)
    return stylesheet


class Usfm:
    def __init__(fname, stylesheet):
        with open(fname, encoding="utf-8") as inf:
            self.doc = list(usfm.parser(inf, stylesheet=stylesheet, purefootnotes=True))

    def getwords(self, init=None, constrain=None):
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
