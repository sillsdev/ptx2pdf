#!/usr/bin/python3
import sys, os
import ptxprint.sfm as sfm
from ptxprint.sfm import usfm
from ptxprint.sfm import style
import argparse, difflib, sys
from enum import Enum

debugPrint = False

class ChunkType(Enum):
    CHAPTER = 1
    HEADING = 2
    TITLE = 3
    INTRO = 4
    BODY = 5

_textype_map = {
    "Chapter":   ChunkType.CHAPTER,
    "Section":   ChunkType.HEADING,
    "Title":     ChunkType.TITLE,
    "Other":     ChunkType.INTRO,
    "VerseText": ChunkType.BODY
}

class Chunk(list):
    def __init__(self, *a, mode=None, chap=0, verse=0, end=0, pnum=0):
        super(Chunk, self).__init__(*a)
        self.type = mode
        self.chap = chap
        self.verse = verse
        self.end = verse
        self.pnum = pnum
        self.labelled = False

    def label(self, chap, verse, end, pnum):
        if self.labelled:
            self.end = end
            return
        self.chap = chap
        self.verse = verse
        self.end = end
        self.pnum = pnum
        self.labelled = True

    @property
    def ident(self):
        if len(self) == 0:
            return ("", 0, 0, 0, 0)
        return (self.type.name, self.chap, self.verse, self.end, self.pnum)

    def __str__(self):
        return "".join(str(x) for x in self)


nestedparas = set(('io2', 'io3', 'io4', 'toc2', 'toc3', 'ili2', 'cp', 'cl'))

def ispara(c):
    return 'paragraph' == str(c.meta.get('StyleType', 'none')).lower()
    
class Collector:
    def __init__(self, doc=None, primary=True, fsecondary=False):
        self.acc = []
        self.fsecondary = fsecondary
        self.chap = 0
        self.verse = 0
        self.end = 0
        self.counts = {}
        self.currChunk = None
        self.mode = ChunkType.INTRO
        if doc is not None:
            self.collect(doc, primary=primary)
            self.reorder()

    def pnum(self, c):
        if c is None:
            return 0
        res = self.counts.get(c.name, 1)
        self.counts[c.name] = res + 1
        return res

    def makeChunk(self, c=None):
        if c is None:
            currChunk = Chunk(mode=self.mode)
        else:
            mode = _textype_map.get(c.meta.get('TextType'), self.mode)
            currChunk = Chunk(mode=mode, chap=self.chap, verse=self.verse, end=self.end, pnum=self.pnum(c))
            self.mode = mode
        self.acc.append(currChunk)
        self.currChunk = currChunk
        return currChunk

    def collect(self, root, primary=True):
        ischap = sfm.text_properties('chapter')
        isverse = sfm.text_properties('verse')
        currChunk = None
        if len(self.acc) == 0:
            currChunk = self.makeChunk()
        for c in root[:]:
            if not isinstance(c, sfm.element):
                continue
            if c.name == "fig":
                if self.fsecondary == primary:
                    root.remove(c)
                    continue
            newchunk = False
            if ispara(c):
                newmode = _textype_map.get(c.meta.get('TextType'), self.mode)
                if newmode != self.mode:
                    newchunk = True
                elif self.mode == ChunkType.HEADING:
                    pass
                elif c.name not in nestedparas:
                    newchunk = True
            if newchunk:
                currChunk = self.makeChunk(c)
            if currChunk is not None:
                currChunk.append(c)
                root.remove(c)
            if ischap(c):
                self.chap = int(c.args[0])
                if currChunk is not None:
                    currChunk.chap = self.chap
                    currChunk.verse = 0
            elif isverse(c):
                if "-" in c.args[0]:
                    v, e = map(int, c.args[0].split('-'))
                else:
                    v = int(c.args[0])
                    e = v
                self.verse = v
                self.end = e
                self.counts = {}
                self.currChunk.label(self.chap, self.verse, self.end, 0)
            currChunk = self.collect(c, primary=primary) or currChunk
        return currChunk

    def reorder(self):
        for i in range(1, len(self.acc)):
            if self.acc[i-1].type == ChunkType.CHAPTER and self.acc[i].type == ChunkType.HEADING:
                self.acc[i-1], self.acc[i] = self.acc[i], self.acc[i-1]


def merge_stylesheet(base, extras):
    for k, v in extras.items():
        if k in base:
            base[k].update(v)
        else:
            base[k] = v
    return base

def alignChunks(pchunks, schunks, pkeys, skeys, filt=None, fns=[], depth=0):
    pairs = []
    if filt is not None:
        pk = [filt(x) for x in pkeys]
        sk = [filt(x) for x in skeys]
    else:
        pk = pkeys
        sk = skeys
    diff = difflib.SequenceMatcher(None, pk, sk)
    for op in diff.get_opcodes():
        (action, ab, ae, bb, be) = op
        if debugPrint:
            print("    "*depth, op, debstr(pk[ab:ae]), debstr(sk[bb:be]))
        if action == "equal":
            pairs.extend([[pchunks[ab+i], schunks[bb+i]] for i in range(ae-ab)])
        elif action == "delete":
            if len(pairs):
                pairs[-1][0].extend(pchunks[ab:ae])
            else:
                pairs.extend([[pchunks[ab+i], ""] for i in range(ae-ab)])
        elif action == "insert":
            if len(pairs):
                pairs[-1][1].extend(schunks[bb:be])
            else:
                pairs.extend([["", schunks[bb+i]] for i in range(be-bb)])
        elif action == "replace":
            if len(fns):        # chain sub-alignment
                pairs.extend(fns[0](pchunks[ab:ae], schunks[bb:be], pkeys[ab:ae], skeys[bb:be], fns=fns[1:], depth=depth+1))
            else:
                for i in range(ae-ab):
                    pairs += [[pchunks[ab+i], ""]] + [["", schunks[bb+i]]]
    return pairs

def alignFilter(km):
    """ Returns an alignment function that calls the km filter on each key """
    def g(pchunks, schunks, pkeys, skeys, fns=[], depth=0):
        return alignChunks(pchunks, schunks, pkeys, skeys, filt=km, fns=fns, depth=depth)
    return g

def pairchunks(pchunks, schunks, pkeys, skeys, starti, i, startj, j, fns=[], depth=0):
    lchunks = pchunks[starti:i] if i > starti else []
    lkeys = pkeys[starti:i] if i > starti else []
    rchunks = schunks[startj:j] if j > startj else []
    rkeys = skeys[startj:j] if j > startj else []
    if not len(lchunks) and not len(rchunks):
        return []  
    if debugPrint:
        print("    "*depth, ("group", starti, i, startj, j), debstr(lkeys), debstr(rkeys))
    if len(fns):
        return fns[0](lchunks, rchunks, lkeys, rkeys, fns=fns[1:], depth=depth+1)
    else:
        return [["".join(str(x) for x in lchunks), "".join(str(x) for x in rchunks)]]

def groupChunks(pchunks, schunks, pkeys, skeys, texttype, fns=[], depth=0):
    pairs = []
    i = 0
    starti = 0
    j = 0
    startj = 0
    currt = None
    maxpkey = len(pkeys)
    maxskey = len(skeys)
    while i < len(pkeys) and j < len(skeys):
        curri = i
        currj = j
        boundarymerge = False
        (mi, ci, vi, ei, pi) = pkeys[i].split("_")
        (mj, cj, vj, ej, pj) = skeys[j].split("_")
        if (texttype(mi) != currt and currt is not None) or (currt is None and texttype(mi) != texttype(mj)):
            # scan for first skeys[j+1:] that matches type with pkeys[i]
            jt = j
            while jt < maxskey:
                (mjt, cjt, vjt, ejt, pjt) = skeys[jt].split("_")
                if texttype(mi) == texttype(mjt):
                    break
                jt += 1
            j = jt
            currt = texttype(mi)
            boundarymerge = True
        elif texttype(mj) != currt and currt is not None:
            # scan for first pkeys[i+1:] that matches type with skeys[k]
            it = i
            while it < maxpkey:
                (mit, cit, cit, eit, pit) = pkeys[it].split("_")
                if texttype(mj) == texttype(mit):
                    break
                it += 1
            i = it
            currt = texttype(mj)
            boundarymerge = True
        elif int(ei) != int(ej):
            # scan forward until both end verses are the same so long as they have the same texttype
            currm = max(int(ei), int(ej))
            lasti, lastj = i, j
            lastc = int(ci)
            while j < maxskey and i < maxpkey:
                if int(ej) <= currm and j < maxskey-1:
                    j += 1
                    laste = int(ej)
                    (mj, cj, vj, ej, pj) = skeys[j].split("_")
                    if texttype(mj) != texttype(mi) or int(cj) > lastc or (laste == currm and int(ej) > currm):
                        j -= 1
                        ej = laste
                    else:
                        currm = max(int(ei), int(ej))
                if int(ei) <= currm and i < maxpkey-1:
                    i += 1
                    laste = int(ei)
                    (mi, ci, vi, ei, pi) = pkeys[i].split("_")
                    if texttype(mi) != texttype(mj) or int(ci) > lastc or (laste == currm and int(ei) > currm):
                        i -= 1
                        ei = laste
                    else:
                        currm = max(int(ei), int(ej))
                if lasti == i and lastj == j:
                    break
                lasti, lastj = i, j
            j += 1
            i += 1
            boundarymerge = True

        if boundarymerge:
            pairs.extend(pairchunks(pchunks, schunks, pkeys, skeys, starti, i, startj, j, fns=[], depth=depth))
            if i > starti:
                starti = i
            if j > startj:
                startj = j
        if i <= curri and j <= currj:
            i = curri + 1
        if currt is None:
            currt = texttype(mi)

    if starti < len(pkeys) or startj < len(skeys):
        pairs.extend(pairchunks(pchunks, schunks, pkeys, skeys, starti, len(pkeys), startj, len(skeys), fns=fns, depth=depth))
    return pairs

def ptypekey(s, styles):
    """ Create a key that replaces a marker by its TextType """
    p = s[:s.find("_")]
    t = styles.get(p, {'TextType': 'other'}).get('TextType').lower()
    return t + s[s.find("_"):]

def usfmerge(infilea, infileb, outfile, stylesheetsa=[], stylesheetsb=[], fsecondary=False, debug=False):
    global debugPrint, debstr
    debugPrint = True
    stylesheeta = usfm._load_cached_stylesheet('usfm.sty')
    stylesheetb = stylesheeta.copy()
    if debugPrint:
        print(stylesheetsa, stylesheetsb)
    for s in stylesheetsa:
        stylesheeta = style.parse(open(s), base=stylesheeta)
    for s in stylesheetsb:
        stylesheetb = style.parse(open(s), base=stylesheetb)

    def texttype(m):
        res = stylesheet.get(m, {'TextType': 'other'}).get('TextType').lower()
        if res in ('chapternumber', 'versenumber'):
            res = 'versetext'
        return res

    debstr = lambda s: s
    #debstr = lambda s: ["{}({})".format(k, texttype(k[:k.find("_")])) for k in s]

    def myGroupChunks(*a, **kw):
        return groupChunks(*a, texttype, **kw)

    with open(infilea, encoding="utf-8") as inf:
        doc = list(usfm.parser(inf, stylesheet=stylesheeta, canonicalise_footnotes=True))
        pcoll = Collector(doc=doc, fsecondary=fsecondary)
    mainchunks = {c.ident: c for c in pcoll.acc}

    with open(infileb, encoding="utf-8") as inf:
        doc = list(usfm.parser(inf, stylesheet=stylesheetb, canonicalise_footnotes=True))
        scoll = Collector(doc=doc, primary=False)
    secondchunks = {c.ident: c for c in scoll.acc}
    mainkeys = ["_".join(str(x) for x in c.ident) for c in pcoll.acc]
    secondkeys = ["_".join(str(x) for x in c.ident) for c in scoll.acc]
    pairs = alignChunks(pcoll.acc, scoll.acc, mainkeys, secondkeys,
        fns=[myGroupChunks, alignFilter(lambda s:ptypekey(s, stylesheet)),
             alignFilter(lambda s:s[:s.find("_")])])

    if outfile is not None:
        outf = open(outfile, "w", encoding="utf-8")
    else:
        outf = sys.stdout

    for p in pairs:
        if not len(p[0]) and not len(p[1]):
            continue
        outf.write("\\lefttext\n")
        outf.write(str(p[0]))
        outf.write("\\p\n")
        outf.write("\\righttext\n")
        outf.write(str(p[1]))
        outf.write("\\p\n")

