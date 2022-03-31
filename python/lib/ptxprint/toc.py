#!/usr/bin/python3

import re
from ptxprint.utils import bookcodes, _allbkmap, refKey, _hebOrder
from ptxprint.unicode.ducet import get_sortkey, SHIFTTRIM, tailored
import logging

logger = logging.getLogger(__name__)

bkranges = {'ot':   ([b for b, i in _allbkmap.items() if 1  < i < 41], True),
            'nt':   ([b for b, i in _allbkmap.items() if 60 < i < 88], True),
            'dc':   ([b for b, i in _allbkmap.items() if 40 < i < 61], True),
            'pre':  ([b for b, i in _allbkmap.items() if 0 <= i < 2], False),
            'post': ([b for b, i in _allbkmap.items() if 87 < i], False),
            'heb':  (_hebOrder, True)}

def sortToC(toc, booklist):
    bknums = {k:i for i,k in enumerate(booklist[0])}
    return sorted(toc, key=(lambda b: refKey(b[0])) if booklist[1] else (lambda b: b[-1]))

def generateTex(alltocs):
    res = []
    for k, v in alltocs.items():
        res.append(r"\defTOC{{{}}}{{".format(k))
        for e in v:
            res.append(r"\doTOCline"+"".join("{"+s+"}" for s in e))
        res.append("}")
    return "\n".join(res)

class TOC:
    def __init__(self, infname):
        mode = 0
        self.tocentries = []
        self.sides = set()
        with open(infname, encoding="utf-8") as inf:
            for l in inf.readlines():
                logger.debug("TOCline: {}".format(l.strip()))
                if mode == 0 and re.match(r"\\defTOC\{main\}", l):
                    mode = 1
                elif mode == 1:
                    m = re.match(r"\\doTOCline\{(.*)\}\{(.*)\}\{(.*)\}\{(.*)\}\{(.*)\}", l)
                    if m:
                        self.tocentries.append(m.groups())
                        if m.group(1)[3:] != "":
                            self.sides.add(m.group(1)[3:])
                    elif l.startswith("}"):
                        mode = 0
                        break

    def createtocvariants(self, booklist, ducet=None):
        res = {}
        for s in list(self.sides) + [""]:
            tocentries = [t for t in self.tocentries if s == "" or t[0][3:] == s]
            res['main' + s] = sortToC(tocentries, booklist)
            for k, r in bkranges.items():
                ttoc = []
                for e in tocentries:
                    try:
                        if e[0][:3] in r[0]:
                            ttoc.append(e)
                    except ValueError:
                        pass
                res[k+s] = sortToC(ttoc, booklist)
            for i in range(3):
                ttoc = []
                k = "sort"+chr(97+i)+s
                res[k] = ttoc
                if i == 2:
                    ducet = tailored("&[first primary ignorable] << 0 << 1 << 2 << 3 << 4 << 5 << 6 << 7 << 8 << 9", ducet)
                def makekey(txt):
                    return int(txt) if txt.isdigit() else get_sortkey(txt, variable=SHIFTTRIM, ducet=ducet)
                def naturalkey(txt):
                    return [makekey(c) for c in reversed(re.split('(\d+)', txt))]
                for e in sorted(tocentries, key=lambda x:naturalkey(x[i+1])):
                    ttoc.append(e)
        return res

