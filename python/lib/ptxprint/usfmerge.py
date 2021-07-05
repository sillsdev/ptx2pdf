#!/usr/bin/python3
import sys, os, re
import ptxprint.sfm as sfm
from ptxprint.sfm import usfm
from ptxprint.sfm import style
import argparse, difflib, sys
from enum import Enum
from itertools import groupby

debugPrint = False

class ChunkType(Enum):
    CHAPTER = 1
    HEADING = 2
    TITLE = 3
    INTRO = 4
    BODY = 5

_textype_map = {
    "ChapterNumber":   ChunkType.CHAPTER,
    "Section":   ChunkType.HEADING,
    "Title":     ChunkType.TITLE,
    "Other":     ChunkType.INTRO,
    "VerseText": ChunkType.BODY
}
_marker_modes = {
    'id': ChunkType.TITLE,
    'ide': ChunkType.TITLE,
    'h': ChunkType.TITLE,
    'toc1': ChunkType.TITLE,
    'toc2': ChunkType.TITLE,
    'toc3': ChunkType.TITLE,

    'cl': ChunkType.CHAPTER,
}

class Chunk(list):
    def __init__(self, *a, mode=None, chap=0, verse=0, end=0, pnum=0):
        super(Chunk, self).__init__(*a)
        self.type = mode
        self.chap = chap
        self.verse = verse
        self.end = verse
        self.pnum = pnum
        self.hasVerse = False
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
            return ("", 0, 0) # , 0, 0)
        return (self.type.name, self.chap, self.verse) # , self.end, self.pnum)

    def __str__(self):
        #return "".join(repr(x) for x in self)
        #return "".join(sfm.generate(x) for x in self)
        return sfm.generate(self)


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
            if c.name == "cl" and self.chap == 0:
                mode = ChunkType.TITLE
            else:
                mode = _marker_modes.get(c.name, _textype_map.get(str(c.meta.get('TextType')), self.mode))
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
            if not isinstance(c, sfm.Element):
                continue
            if c.name == "fig":
                if self.fsecondary == primary:
                    root.remove(c)
                    continue
            newchunk = False
            if ispara(c):
                newmode = _marker_modes.get(c.name, _textype_map.get(str(c.meta.get('TextType')), self.mode))
                if newmode != self.mode:
                    newchunk = True
                elif self.mode in (ChunkType.HEADING, ChunkType.TITLE):
                    pass
                elif c.name not in nestedparas:
                    newchunk = True
            if newchunk:
                currChunk = self.makeChunk(c)
            if currChunk is not None:
                currChunk.append(c)
                root.remove(c)
            if ischap(c):
                vc = re.sub(r"[^0-9\-]", "", c.args[0])
                try:
                    self.chap = int(vc)
                except (ValueError, TypeError):
                    self.chap = 0
                if currChunk is not None:
                    currChunk.chap = self.chap
                    currChunk.verse = 0
            elif isverse(c):
                vc = re.sub(r"[^0-9\-]", "", c.args[0])
                try:
                    if "-" in c.args[0]:
                        v, e = map(int, vc.split('-'))
                    else:
                        v = int(vc)
                        e = v
                except (ValueError, TypeError):
                    v = 0
                    e = 0
                self.verse = v
                self.end = e
                self.counts = {}
                self.currChunk.label(self.chap, self.verse, self.end, 0)
                self.currChunk.hasVerse = True
            currChunk = self.collect(c, primary=primary) or currChunk
        return currChunk

    def reorder(self):
        bi = None
        for i in range(1, len(self.acc)):
            if self.acc[i].type == ChunkType.TITLE and self.acc[i-1].type == ChunkType.TITLE:
                if bi is None:
                    bi = i-1
                self.acc[bi].extend(self.acc[i])
                self.acc[i].deleteme = True
        # move everything after \c up to something with a \v in it, to before the \c
        for i in range(1, len(self.acc)):
            if self.acc[i-1].type == ChunkType.CHAPTER and not self.acc[i].hasVerse:
                self.acc[i-1], self.acc[i] = self.acc[i], self.acc[i-1]
        # merge \c with body chunk following
        for i in range(1, len(self.acc)):
            if getattr(self.acc[i], 'deleteme', False):
                continue
            if self.acc[i-1].type == ChunkType.CHAPTER and self.acc[i].type == ChunkType.BODY:
                tag = self.acc[i][0].name
                self.acc[i-1].extend(self.acc[i])
                self.acc[i-1].type = self.acc[i].type
                self.acc[i].deleteme = True
                if tag == "nb" and i > 1:
                    self.acc[i-2].extend(self.acc[i-1])
                    self.acc[i-1].deleteme = True
                elif tag.startswith("q") and i < len(self.acc) - 1 and self.acc[i+1][0].name.startswith("q"):
                    self.acc[i-1].extend(self.acc[i+1])
                    self.acc[i+1].deleteme = True
        self.acc = [x for x in self.acc if not getattr(x, 'deleteme', False)]


def appendpair(pairs, ind, chunks):
    if len(pairs) and pairs[-1][ind] is not None:
        lastp = pairs[-1][ind]
        lastt = lastp.type
        end = None
        found = False
        for i, c in enumerate(chunks):
            if c.type == lastt:
                found = True
                end = i
            elif found:
                break
        if end is not None:
            for c in chunks[:end+1]:
                lastp.extend(c)
            chunks = chunks[end+1:]
    if ind == 1:
        pairs.extend([[None, c] for c in chunks])
    else:
        pairs.extend([[c, None] for c in chunks])

def appendpairs(pairs, pchunks, schunks):
    if len(pairs) and pairs[-1][0] is not None and pairs[-1][1] is not None:
        lastp = pairs[-1][0]
        lasts = pairs[-1][1]
        lastt = lastp.type
        if lasts.type == lastt:
            while len(pchunks) and pchunks[0].type == lastt:
                lastp.extend(pchunks.pop(0))
            while len(schunks) and schunks[0].type == lastt:
                lasts.extend(schunks.pop(0))
    if len(pchunks):
        pc = pchunks[0]
        for c in pchunks[1:]:
            pc.extend(c)
    else:
        pc = None
    if len(schunks):
        sc = schunks[0]
        for c in schunks[1:]:
            sc.extend(c)
    else:
        sc = None
    pairs.append([pc, sc])

def alignChunks(pchunks, schunks, pkeys, skeys):
    pairs = []
    diff = difflib.SequenceMatcher(None, pkeys, skeys)
    for op in diff.get_opcodes():
        (action, ab, ae, bb, be) = op
        if debugPrint:
            print(op, debstr(pkeys[ab:ae]), debstr(skeys[bb:be]))
        if action == "equal":
            pairs.extend([[pchunks[ab+i], schunks[bb+i]] for i in range(ae-ab)])
        elif action == "delete":
            appendpair(pairs, 0, pchunks[ab:ae])
        elif action == "insert":
            appendpair(pairs, 1, schunks[bb:be])
        elif action == "replace":
            pgk, pgg = zip(*[(k, list(g)) for k, g in groupby(pchunks[ab:ae], key=lambda c:c.type)])
            sgk, sgg = zip(*[(k, list(g)) for k, g in groupby(schunks[bb:be], key=lambda c:c.type)])
            diffg = difflib.SequenceMatcher(a=pgk, b=sgk)
            for opg in diffg.get_opcodes():
                (actiong, abg, aeg, bbg, beg) = opg
                if debugPrint:
                    print("--- ", opg, debstr(pgk[abg:aeg]), debstr(sgk[bbg:beg]))
                if actiong == "equal":
                    appendpairs(pairs, sum(pgg[abg:aeg], []), sum(sgg[bbg:beg], []))
                elif action == "delete":
                    appendpair(pairs, 0, sum(pgg[abg:aeg], []))
                elif action == "insert":
                    appendpair(pairs, 0, sum(sgg[bbg:beg], []))
                elif action == "replace":
                    for zp in zip(range(abg, aeg), range(bbg, beg)):
                        appendpairs(pairs, pgg[zp[0]], sgg[zp[1]])
                    sg = bbg + aeg - abg
                    if sg < beg:
                        appendpair(pairs, 1, sum(sgg[sg:beg], []))
                    sg = abg + beg - bbg
                    if sg < aeg:
                        appendpair(pairs, 0, sum(pgg[sg:aeg], []))
    return pairs

def alignSimple(pchunks, schunks, pkeys, skeys):
    pairs = []
    diff = difflib.SequenceMatcher(None, pkeys, skeys)
    for op in diff.get_opcodes():
        (action, ab, ae, bb, be) = op
        if debugPrint:
            print(op, debstr(pkeys[ab:ae]), debstr(skeys[bb:be]))
        if action == "equal":
            pairs.extend([[pchunks[ab+i], schunks[bb+i]] for i in range(ae-ab)])
        if action in ("delete", "replace"):
            for c in pchunks[ab:ae]:
                pairs[-1][0].extend(c)
        if action in ("insert", "replace"):
            for c in schunks[bb:be]:
                pairs[-1][1].extend(c)
    return pairs

def appendsheet(fname, sheet):
    if os.path.exists(fname):
        with open(fname) as s:
            sheet = style.update_sheet(sheet, style.parse(s))
    return sheet

modes = {
    "doc": alignChunks,
    "simple": alignSimple
}

def usfmerge2(infilea, infileb, outfile, stylesheetsa=[], stylesheetsb=[], fsecondary=False, mode="doc", debug=False):
    global debugPrint, debstr
    debugPrint = debug
    stylesheeta = usfm._load_cached_stylesheet('usfm.sty')
    stylesheetb = {k: v.copy() for k, v in stylesheeta.items()}
    tag_escapes = r"[^a-zA-Z0-9]"
    if debugPrint:
        print(stylesheetsa, stylesheetsb)
    for s in stylesheetsa:
        stylesheeta = appendsheet(s, stylesheeta)
    for s in stylesheetsb:
        stylesheetb = appendsheet(s, stylesheetb)

    def texttype(m):
        res = stylesheet.get(m, {'TextType': 'other'}).get('TextType').lower()
        if res in ('chapternumber', 'versenumber'):
            res = 'versetext'
        return res

    debstr = lambda s: s

    def myGroupChunks(*a, **kw):
        return groupChunks(*a, texttype, **kw)

    with open(infilea, encoding="utf-8") as inf:
        doc = list(usfm.parser(inf, stylesheet=stylesheeta,
                               canonicalise_footnotes=False, tag_escapes=tag_escapes))
        pcoll = Collector(doc=doc, fsecondary=fsecondary)
    mainchunks = {c.ident: c for c in pcoll.acc}

    with open(infileb, encoding="utf-8") as inf:
        doc = list(usfm.parser(inf, stylesheet=stylesheetb,
                               canonicalise_footnotes=False, tag_escapes=tag_escapes))
        scoll = Collector(doc=doc, primary=False)
    secondchunks = {c.ident: c for c in scoll.acc}
    mainkeys = ["_".join(str(x) for x in c.ident) for c in pcoll.acc]
    secondkeys = ["_".join(str(x) for x in c.ident) for c in scoll.acc]
    f = modes[mode]
    pairs = f(pcoll.acc, scoll.acc, mainkeys, secondkeys)
    #pairs = alignChunks(pcoll.acc, scoll.acc, mainkeys, secondkeys)

    if outfile is not None:
        outf = open(outfile, "w", encoding="utf-8")
    else:
        outf = sys.stdout

    isright = True
    for i, p in enumerate(pairs):
        if p[0] is not None and len(p[0]):
            if isright:
                outf.write("\\lefttext\n")
                isright = False
            outf.write(str(p[0]))
            if p[0].type != ChunkType.HEADING and p[0].type != ChunkType.TITLE:
                outf.write("\\p\n")
        elif i != 0 and isright and p[1] is not None and len(p[1]):
            outf.write("\\nolefttext\n")
            isright = False
        if p[1] is not None and len(p[1]):
            if not isright:
                outf.write("\\righttext\n")
                isright = True
            outf.write(str(p[1]))
            if p[1].type != ChunkType.HEADING and p[1].type != ChunkType.TITLE:
                outf.write("\\p\n")
        elif not isright:
            outf.write("\\norighttext\n")

