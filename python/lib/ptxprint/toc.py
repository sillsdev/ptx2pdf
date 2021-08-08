#!/usr/bin/python3

import re
from ptxprint.utils import bookcodes
from ptxprint.sfm.ducet import get_sortkey

def parsetoc(infname):
    mode = 0
    tocentries = []
    with open(infname, encoding="utf-8") as inf:
        for l in inf.readlines():
            if mode == 0 and re.match(r"\\defTOC\{main\}", l):
                mode = 1
            elif mode == 1:
                m = re.match(r"\\doTOCline\{(.*)\}\{(.*)\}\{(.*)\}\{(.*)\}\{(.*)\}", l)
                if m:
                    tocentries.append(m.groups())
                elif l.startswith("}"):
                    mode = 0
                    break
    return tocentries

bkranges = {'ot': (0, 40), 'nt': (40, 68), 'dc': (67, 87)}

def createtocvariants(toc):
    res = {}
    res['main'] = toc
    for k, r in bkranges.items():
        ttoc = []
        res[k] = ttoc
        for e in toc:
            if r[0] < int(bookcodes.get(e[0], -1)) < r[1]:
                ttoc.append(e)
    for i in range(3):
        ttoc = []
        k = "sort"+chr(97+i)
        res[k] = ttoc
        for e in sorted(toc, key=lambda x:get_sortkey(x[i+1])):
            ttoc.append(e)
    return res

def generateTex(alltocs):
    res = []
    for k, v in alltocs.items():
        res.append(r"\defTOC{{{}}}{{".format(k))
        for e in v:
            res.append(r"\doTOCline"+"".join("{"+s+"}" for s in e))
        res.append("}")
    return "\n".join(res)
