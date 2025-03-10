#!/usr/bin/python3
import sys, os, re, io
from ptxprint.usxutils import Usfm, Sheets
from usfmtc.usfmgenerate import usx2usfm
import argparse, difflib, sys
from enum import Enum,Flag
from itertools import groupby
from functools import reduce
import configparser
import logging

class MergeF(Flag):
    ChunkOnVerses=1
    NoSplitNB=2
    HeadWithText=4  # Is a heading considered part of the text, or a separate chunk?
    SwapChapterHead=8
    HeadWithChapter=16  # Is a heading considered part of the chapter, or is it (initially) a separate chunk?
    CLwithChapter=32 # IS cl treated as part of a chapter or is it a heading?

settings= MergeF.NoSplitNB | MergeF.HeadWithChapter 
logger = logging.getLogger(__name__)
debugPrint = False

class ChunkType(Enum):
    DEFSCORE = 0        # Value for default scores
    CHAPTER = 1
    HEADING = 2
    HEADER = 3
    TITLE = 4
    INTRO = 5
    BODY = 6
    ID = 7
    TABLE = 8
    VERSE = 9 
    PARVERSE = 10
    MIDVERSEPAR = 11
    PREVERSEPAR = 12
    NOVERSEPAR = 13
    NPARA = 14
    NB = 15
    NBCHAPTER = 16
    CHAPTERPAR = 17
    CHAPTERHEAD = 18
    PREVERSEHEAD = 19
    USERSYNC = 20
    PARUSERSYNC =21 # User

_chunkDesc_map= {# prefix with (!) if not a valid break-point to list in the config file.
    ChunkType.CHAPTER :"A normal chapter number",
    ChunkType.HEADING :"A heading (e.g. s1)",
    ChunkType.HEADER: "Book info markers (e.g. h, toc1)",
    ChunkType.TITLE :"A title (e.g. mt1)",
    ChunkType.INTRO :"An introduction paragraph (e.g. ip)",
    ChunkType.BODY :"A generic paragraph (normally turned into something else)",
    ChunkType.ID :"(!)The \\id line",
    ChunkType.TABLE :"A table",
    ChunkType.VERSE :"A verse chunk, inside a paragraph",
    ChunkType.PARVERSE :"A verse chunk, first thing after starting a paragraph",
    ChunkType.MIDVERSEPAR :"A paragraph which is mid-paragraph",
    ChunkType.PREVERSEPAR :"A paragrpah where the next content is a verse number",
    ChunkType.NOVERSEPAR :"A paragraph which is not in verse-text, e.g inside a side-bar, or book/chapter introduction",
    ChunkType.NPARA :"(!)A block of nested paragraphs",
    ChunkType.NB :"A nobreak mark - often protected against breaking",
    ChunkType.NBCHAPTER :"A chapter that is followed by an NB - not normally a good sync point",
    ChunkType.CHAPTERPAR :"A PREVERSEPAR that is following a chapter - not normally a good sync point!",
    ChunkType.CHAPTERHEAD:"A Heading that is (was) following a chapter (and sometimes also the chapter number)",
    ChunkType.PREVERSEHEAD:"A Heading that is just before PREVERSEPAR",
    ChunkType.USERSYNC:"A preprocessing-inserted / manual sync point.",
    ChunkType.PARUSERSYNC:"A preprocessing-inserted / manual sync point, just after starting a paragraph."
}
_chunkClass_map = {
ChunkType.DEFSCORE:'',
ChunkType.CHAPTER:'CHAPTER',
ChunkType.HEADER:'HEADER',
ChunkType.HEADING:'HEADING',
ChunkType.TITLE:'TITLE',
ChunkType.INTRO:'INTRO',
ChunkType.BODY:'BODY',
ChunkType.ID:'ID',
ChunkType.TABLE:'TABLE',
ChunkType.VERSE:'VERSE',
ChunkType.PARVERSE:'VERSE',
ChunkType.MIDVERSEPAR:'BODY',
ChunkType.PREVERSEPAR:'BODY',
ChunkType.NOVERSEPAR:'BODY',
ChunkType.NPARA:'BODY',
ChunkType.NB:'BODY',
ChunkType.NBCHAPTER:'CHAPTER',
ChunkType.CHAPTERPAR:'BODY',
ChunkType.CHAPTERHEAD:'CHAPTER',
ChunkType.PREVERSEHEAD:'HEADING',
ChunkType.USERSYNC:'BODY',
ChunkType.PARUSERSYNC:'BODY'
}

splitpoints={
        ChunkType.VERSE:True
} 
_textype_map = {
    "ChapterNumber":   ChunkType.CHAPTER,
    "Section":   ChunkType.HEADING,
    "Title":     ChunkType.TITLE,
    "Other":     ChunkType.INTRO,
    "VerseText": ChunkType.BODY
}
_marker_modes = {
    'id': ChunkType.HEADER,
    'ide': ChunkType.HEADER,
    'h': ChunkType.HEADER,
    'h1': ChunkType.HEADER,
    'h2': ChunkType.HEADER,
    'h3': ChunkType.HEADER,
    'toc1': ChunkType.HEADER,
    'toc2': ChunkType.HEADER,
    'toc3': ChunkType.HEADER,
    'toca1': ChunkType.HEADER,
    'toca2': ChunkType.HEADER,
    'toca3': ChunkType.HEADER,
    'zthumbtab': ChunkType.HEADER,
    'rem': ChunkType.HEADER,
    'sts': ChunkType.HEADER,
    'usfm': ChunkType.HEADER,
    'v': ChunkType.VERSE,
    'cl': ChunkType.CHAPTERHEAD, # this gets overwritten.
    'nb': ChunkType.NB
}

_canonical_order={
    ChunkType.ID:0,
    ChunkType.HEADER:0,
    ChunkType.TITLE:0,
    ChunkType.CHAPTER:0,
    ChunkType.NBCHAPTER:0,
    ChunkType.CHAPTERHEAD:1,
    ChunkType.PREVERSEHEAD:2, # Takes the verse nr of its verse
    ChunkType.PREVERSEPAR:3, # Takes the verse nr of its verse
    ChunkType.CHAPTERPAR:4,
    ChunkType.PARVERSE:5,
    ChunkType.VERSE:6,
    ChunkType.MIDVERSEPAR:7,
    ChunkType.HEADING:7,
    ChunkType.USERSYNC:7,
    ChunkType.PARUSERSYNC:7,
    ChunkType.BODY:7,
}
    

class Chunk(list):
    def __init__(self, *a, mode=None, doc=None, chap=0, verse=0, end=0, pnum=0,syncp='~'):
        super(Chunk, self).__init__(a)
        self.type = mode
        self.otype = mode
        self.chap = chap
        self.verse = verse
        self.end = verse
        self.pnum = pnum
        self.syncp = syncp
        self.hasVerse = False
        if mode in (ChunkType.MIDVERSEPAR, ChunkType.VERSE, ChunkType.PARVERSE):
            self.verseText = True
        else:
            self.verseText = False
        self.labelled = False
        self.score = None
        self.doc = doc

    def label(self, chap, verse, end, pnum, syncp):
        if self.labelled:
            self.end = end
            if syncp != '':
              self.syncp=syncp
            return
        if syncp != '':
          m=re.match(r"\|p(\d+)$",syncp)
          if m:
            pnum=int(m.group(1))-1
            syncp="~"
            self.type=ChunkType.MIDVERSEPAR
        self.chap = chap
        self.verse = verse
        self.end = end
        self.pnum = pnum
        self.syncp = syncp
        self.labelled = True

    @property
    def position(self):
        return((self.chap,self.verse, _canonical_order[self.type] if self.type in _canonical_order else 9, self.syncp, self.pnum, self.type.name if self.type.name != 'VERSE' else '@VERSE'))
        #return("%03d:%03d:%04d:%s" % (self.chap,self.verse,self.pnum,self.type.name))

    @property
    def ident(self):
        if len(self) == 0:
            return ("", 0, 0,0) # , 0, 0)
        return (_chunkClass_map[self.type], self.chap, self.verse)# , self.pnum) # , self.end, self.pnum)

    def __str__(self):
        return self.astext()

    def astext(self):
        with io.StringIO() as outf:
            lastel = None
            for e in self:
                if e.tag == "para":
                    if lastel is not None and lastel.tail:
                        outf.write(lastel.tail)
                    outf.write(f"\n\\{e.get('style', '')} {e.text}")
                    lastel = e
                else:
                    lastel = usx2usfm(outf, e, grammar=(self.doc.grammar if self.doc is not None else None), lastel=lastel)
            if lastel is not None and lastel.tail:
                outf.write(lastel.tail)
            res = outf.getvalue() + "\n"
        return res

_headingidx=5
_validatedhpi=False # Has the heading(position)idx above been validated?

nestedparas = set(('io2', 'io3', 'io4', 'toc2', 'toc3', 'ili2', 'cp')) 

SyncPoints = {
    "chapter":{ChunkType.VERSE:0,ChunkType.PREVERSEPAR:0,ChunkType.PREVERSEHEAD:0,ChunkType.NOVERSEPAR:0,ChunkType.MIDVERSEPAR:0,ChunkType.HEADING:0,ChunkType.CHAPTER:1,ChunkType.CHAPTERHEAD:0,ChunkType.CHAPTERPAR:0,ChunkType.NBCHAPTER:1,ChunkType.USERSYNC:1,ChunkType.PARUSERSYNC:1}, # Just split at chapters
    "normal":{ChunkType.VERSE:0,ChunkType.PREVERSEPAR:1,ChunkType.PREVERSEHEAD:1,ChunkType.NOVERSEPAR:1,ChunkType.MIDVERSEPAR:1,ChunkType.HEADING:1,ChunkType.CHAPTER:1,ChunkType.CHAPTERHEAD:1,ChunkType.CHAPTERPAR:0,ChunkType.USERSYNC:1,ChunkType.PARUSERSYNC:1}, 
    "verse":{ChunkType.VERSE:1,ChunkType.PREVERSEPAR:1,ChunkType.PREVERSEHEAD:1,ChunkType.NOVERSEPAR:0,ChunkType.MIDVERSEPAR:0,ChunkType.HEADING:1,ChunkType.CHAPTER:1,ChunkType.CHAPTERHEAD:1,ChunkType.CHAPTERPAR:0,ChunkType.NBCHAPTER:1,ChunkType.USERSYNC:1,ChunkType.PARUSERSYNC:1}, # split at every verse
    "custom":{} # No default
}

globalcl = False # Has a cl been met?
def ispara(c):
    return 'paragraph' == str(c.meta.get('StyleType', 'none')).lower()
    
class Collector:
    """TODO: write more here
        synchronise : str
            This picks the ChunkTypes that will be contribute to scoring for this collection. 
        scores : int or {ChunkType.DEFSCORE:int, ...}
            Normally this takes a single value, which is promoted to the default score.
            For really interesting scoring, a mapping of ChunkType.*:score can
            be supplied, e.g. to force a chunk-break at all headings from one source)
             For any ChunkType  that is missing from the scores mapping (or for
            all ChunkTypes if a single value is supplied), then the default score is applied
            according to the rule-set chosen from synchronise
    """
    def __init__(self, doc=None, primary=True, fsecondary=False, stylesheet=None, colkey=None, scores=None, synchronise=None, protect={}):
        self.acc = []
        self.loc = {} # Locations to turn position into offset into acc[] array 
        self.lastloc = None # Locations to turn position into offset into acc[] array 
        self.colkey=colkey
        self.fsecondary = fsecondary
        self.stylesheet = stylesheet
        self.protect = protect  # reduce score by value at \\key
       
        self.chap = 0
        self.verse = 0
        self.end = 0
        self.waspar = False # Was the previous item an empty paragraph mark of some type?
        self.waschap = False # Was the previous item a chapter number?
        self.counts = {}
        self.scores = {} 
        self.currChunk = None
        self.mode = ChunkType.INTRO
        self.oldmode= None
        if (scores==None):
            raise ValueError("Scores can be integer or ChunkType:Score values, but must be supplied!")
        logger.debug(f"Scores supplied are: {type(scores)}, {scores=}")
        if synchronise in SyncPoints:
            logger.debug(f"Sync points: {synchronise.lower()}")
            syncpoints = SyncPoints[synchronise.lower()] 
        elif synchronise is None:
            syncpoints = SyncPoints['normal'] 
            logger.debug("Sync points are normal")
        else:
            raise ValueError(f"Synchronise method '{synchronise}' not recognised.")
        if (type(scores) == int):
            tmp = scores
            scores = {ChunkType.DEFSCORE:tmp}
            logger.debug(f"Default score = {scores[ChunkType.DEFSCORE]}")
        if 'nb' in self.protect:
            logger.debug(f"Protecing nbchapter, like nb")
            self.scores[ChunkType.NBCHAPTER.value] = -self.protect['nb']
            logger.debug(self.scores)
        for st in ChunkType:
            if st.value == ChunkType.DEFSCORE:
                self.scores[st.value] = scores[st]
            else:
                if (st.value not in self.scores):
                    self.scores[st.value] = 0
                if (st in scores):
                    self.scores[st.value] += scores[st] 
                elif (st in syncpoints):
                    self.scores[st.value] += scores[ChunkType.DEFSCORE] * syncpoints[st]
 
            #if (self.scores[st.value]):
            #    splitpoints[st] = True
            #else:
            #    if (st not in splitpoints):
            #        splitpoints[st] = False
            logger.debug(f"Score for {st}({st.value}) -> {self.scores[st.value]}, {syncpoints[st] if st in syncpoints else '-'}")
        self.doc = doc
        if doc is not None:
            self.collect(doc.getroot(), primary=primary)
            self.reorder()

    def text_properties(self, e):
        return set(self.stylesheet.get(e.get('style', ''), {}).get('textproperties', '').split())

    def texttype(self, e, default=''):
        return self.stylesheet.get(e.get('style', ''), {}).get('texttype', default)

    def pnum(self, c):
        if c is None:
            return 0
        res = self.counts[c] = self.counts.get(c, 0) + 1
        return res

    def makeChunk(self, c=None):
        global _validatedhpi, _headingidx
        if c is None:
            currChunk = Chunk(mode=self.mode, doc=doc)
            self.waspar = False
            self.waschap = False
        else:
            name = c.get("style", "")
            if name == "cl":
                if self.chap == 0: 
                  mode = ChunkType.TITLE 
                  logger.debug('cl found at chapter 0')
                  globalcl = True
                else:
                  if self.waschap:
                      mode = ChunkType.CHAPTERHEAD if not MergeF.CLwithChapter in settings else ChunkType.CHAPTER
                  else:
                    mode = ChunkType.HEADING
                logger.log(8, f'cl found for {self.chap} mode:{mode}')
            elif c.tag == "book":
                mode = ChunkType.ID
            elif name == "nb":
                mode = ChunkType.NB
            elif c.tag == "row":
                mode = ChunkType.TABLE
            elif 'diglotsync' in self.text_properties(c):
                mode = ChunkType.USERSYNC
                if (self.waspar):
                  mode = ChunkType.PARUSERSYNC
            elif name in nestedparas:
                mode = ChunkType.NPARA
            elif c.tag == "verse":
                if self.waspar:
                    mode = ChunkType.PARVERSE
                else:
                    mode = ChunkType.VERSE
            else:
                mode = _marker_modes.get(name, _textype_map.get(self.texttype(c), self.mode))
                if mode == ChunkType.HEADING:
                    if self.waschap:
                        mode = ChunkType.CHAPTERHEAD
                elif mode == ChunkType.BODY and c.tag == "para":
                    logger.log(8, f'Bodypar: vt?{self.currChunk.verseText} hv?{self.currChunk.hasVerse}: {len(self.acc)}')
                    if len(c) == 0:
                        logger.log(8, f'Bodypar(simple): {name} {c.text}')
                        if c.text and len(c.text.strip()) and self.currChunk.verseText:
                            mode = ChunkType.MIDVERSEPAR
                    elif len(c):
                        cs = list(c)
                        #Multi-component body paragraph
                        logger.log(8, f'Bodypar: {name}, {type(cs[0])}, {cs[0]}')
                        if (len(cs[0]) > 1 and self.currChunk.verseText):
                            mode = ChunkType.MIDVERSEPAR
                        elif cs[0].tag == "verse" or (len(cs) > 1 and cs[1].tag == "verse"):
                            mode = ChunkType.PREVERSEPAR
                        elif cs[0].tail or cs[0].text:
                            if self.currChunk.verseText:
                                mode = ChunkType.MIDVERSEPAR
                    logger.log(9, f"Conclusion: bodypar type is {mode}")
                        
            pn = self.pnum
            currChunk = Chunk(mode=mode, chap=self.chap, verse=self.verse, end=self.end, pnum=self.pnum(mode))
            if not _validatedhpi:
                p = currChunk.position
                assert p[_headingidx] == mode.name, "It looks like someone altered the position tuple, but didn't update _headingidx"
                _validatedhpi = True
            self.waspar = c.tag == "para"
            self.waschap = (mode in (ChunkType.CHAPTER,ChunkType.CHAPTERHEAD))
            self.mode = mode
        self.acc.append(currChunk)
        self.currChunk = currChunk
        return currChunk

    def collect(self, root, primary=True, depth=0):
        currChunk = None
        if depth == 0:
            self.type=None
        else:
            logger.log(9-depth,"{" * depth)
        elements = list(root)
        i = 0
        # if depth == 0:
        #     breakpoint()
        for c in elements:
            if c.tag == "figure" and self.fsecondary == primary:
                root.remove(c)
                continue
            newchunk = False
            name = c.get("style", "")
            if c.tag == "para" or c.tag == "book":
                newmode = _marker_modes.get(name, _textype_map.get(self.texttype(c), self.mode))
                ok = (newmode == ChunkType.HEADING and self.mode in (ChunkType.CHAPTERHEAD, ChunkType.PREVERSEHEAD))
                if name not in nestedparas and ((newmode != self.mode and not ok) \
                            or self.mode not in (ChunkType.HEADING, ChunkType.CHAPTERHEAD, ChunkType.TITLE, ChunkType.HEADER)):
                    newchunk = True
                logger.log(7, f"Para:{name} {newmode} {self.chap}:{self.verse} {newchunk} context: {self.oldmode}, {self.mode}")
            if 'diglotsync' in self.text_properties(c):
                newchunk = True
                try:
                    self.syncp = c.get("syncaddr", "")
                except (ValueError, TypeError):
                    self.syncp = '@'
                logger.log(8, f" {self.chap}:{self.verse}:{self.syncp} {c.name} {newchunk} context: {self.oldmode}, {self.mode  if isinstance(c, sfm.Element) else '-'}")
                M=re.search(r"v(\d+)(\D*)$", self.syncp)
                if (M is not None):
                    Mv = M.group(1)
                    Ms = M.group(2)
                    logger.log(7,f"RE: {M}, Match: '{Mv}.{Ms}'")
                    if Mv and len(Mv)>0:
                        self.verse = int(Mv)
                        self.end = int(Mv)
            if c.tag == "verse":
                vc = re.sub(r"[^0-9\-]", "", c.get("number", ""))
                try:
                    if "-" in vc:
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
                self.currChunk.hasVerse = True
                if MergeF.ChunkOnVerses in settings:
                    newchunk = True
                else:
                    self.currChunk.label(self.chap, self.verse, self.end, 0,'')
                logger.log(8, f" {self.chap}:{self.verse} {c.get('style', '')} {newchunk} context: {self.oldmode}, {self.mode}")
            if newchunk:
                self.oldmode = self.mode
                currChunk = self.makeChunk(c)
                if MergeF.ChunkOnVerses in settings:
                    if isverse(c):
                        currChunk.hasVerse = True # By definition!
                        self.currChunk.label(self.chap, self.verse, self.end, 0,'')
                        self.currChunk.hasVerse = True
                if 'diglotsync' in self.text_properties(c):
                    self.currChunk.label(self.chap, self.verse, self.end, 0,self.syncp)
                #elif (currChunk.type==ChunkType.BODY and ispara(c) and self.oldmode == ChunkType.MIDVERSEPAR): 
                    #currChunk.type=ChunkType.MIDVERSEPAR
            if c.tag == "chapter":
                logger.log(8, f" chapter {c}")
                self.verse = 0
                vc = re.sub(r"[^0-9\-]", "", c.get("number", ""))
                try:
                    self.chap = int(vc)
                except (ValueError, TypeError):
                    self.chap = 0
                if currChunk is None:
                    currChunk=makeChunk(c)
                else:
                    currChunk.chap = self.chap
                    currChunk.verse = self.verse
                    currChunk.append(c)
            else:
                self.currChunk.append(c)
            #logger.log(7,f'collecting {c.name}')
            if c.tag == "para":
                t = self.collect(c, primary=primary, depth=1+depth)
            #logger.log(7,f'collected {c.name}')
                if t is not None:
                    logger.log(7, t)
                    currChunk = t
        logger.log(9-depth,"}" * depth)
        return currChunk

    def reorder(self):
        # Merge contiguous title and table chunks, Merge in nested paragraphs
        ti = None
        bi = None
        ni = None
        #for i in range(0, 10):
            #print(i,self.acc[i].ident if isinstance(self.acc[i],Chunk) else '-' ,self.acc[i].type,self.acc[i])
        logger.log(7, "Chunks before reordering")
        for i in range(0, len(self.acc)):
            if isinstance(self.acc[i],Chunk):
              logger.log(7, f"r: {i}, {self.acc[i].ident}//{self.acc[i].position}, {self.acc[i].type=}, {self.acc[i]=}")
            else:
              logger.log(7, f"r: {i}, '-//-', {self.acc[i].type=}, {self.acc[i]=}")
        for i in range(1, len(self.acc)):
            if self.acc[i].type == ChunkType.TITLE and self.acc[i-1].type == ChunkType.TITLE:
                if bi is None:
                    bi = i-1
                self.acc[bi].extend(self.acc[i])
                self.acc[i].deleteme = True
                ti = None
                ni = None
                logger.debug(f"Merged.1: {'deleteme' in self.acc[bi]}, {self.acc[bi]}")
            elif self.acc[i].type == ChunkType.TABLE and self.acc[i-1].type == ChunkType.TABLE:
                if ti is None:
                    ti = i - 1
                self.acc[ti].extend(self.acc[i])
                self.acc[i].deleteme = True
                bi = None
                ni = None
                logger.debug(f"Merged.2: {'deleteme' in self.acc[ti]}, {self.acc[ti]}")
            elif self.acc[i].type == ChunkType.NPARA and self.acc[i-1].type != None:
                if ni is None:
                    ni = i - 1
                self.acc[ni].extend(self.acc[i])
                self.acc[i].deleteme = True
                bi = None
                ti = None
                logger.debug(f"Merged.3: {'deleteme' in self.acc[ni]}, {self.acc[ni]}")
        # Merge nb with chapter number and 1st verse.
        for i in range(1, len(self.acc) - 1):
            if self.acc[i].type is ChunkType.NB:
                self.acc[i-1].type = ChunkType.NBCHAPTER
                if MergeF.NoSplitNB in settings:
                    self.acc[i-1].extend(self.acc[i])
                    self.acc[i].deleteme = True
                    #print("NB met",self.acc[i-2].type ,self.acc[i-1].type ,self.acc[i].type )
                    if self.acc[i+1].type == ChunkType.PARVERSE:
                        self.acc[i-1].verse=self.acc[i+1].verse
                        self.acc[i-1].extend(self.acc[i+1])
                        logger.debug('Merged.4a')
                        self.acc[i+1].deleteme = True
                    if i>2 and self.acc[i-2].type in (ChunkType.VERSE, ChunkType.MIDVERSEPAR, ChunkType.PARVERSE, ChunkType.PREVERSEPAR):
                        self.acc[i-2].extend(self.acc[i-1])
                        self.acc[i-1].deleteme = True
                        logger.debug('Merged.4b')
                    logger.debug(f"Merged.4: {'deleteme' in self.acc[i-1]}, {self.acc[i-1]}")

        # Merge pre-verse paragraph and verses.
        for i in range(1, len(self.acc) ):
            if self.acc[i].type == ChunkType.PARVERSE:
                logger.log(7,f"Merge.5 {self.colkey}? {self.acc[i].position} prev:{self.acc[i-1].type}")
                if  self.acc[i-1].type in (ChunkType.PREVERSEPAR, ChunkType.NB):
                    # A PARVERSE gives its address and content up to the preceeding PREVERSEPAR, as the two may not be seperated
                    if bi is None:
                        bi=i-1
                    self.acc[bi].verse = self.acc[i].verse
                    self.acc[bi].pnum = self.acc[i].pnum
                    self.acc[bi].extend(self.acc[i])
                    self.acc[i].deleteme = True
                    logger.debug(f"Merged.5: {'deleteme' in self.acc[bi]}, {self.acc[bi].position}")
                    if bi>1 and self.acc[bi-1].type == ChunkType.CHAPTER:
                        self.acc[bi].type = ChunkType.CHAPTERPAR
                elif (self.acc[i-1].type in (ChunkType.CHAPTER, ChunkType.NBCHAPTER)):
                    pass 
                else:
                    logger.debug(f"Caught unexpected situtuation. Expected (PREVERSEPAR,PARVERSE), got: {self.acc[i-1].type} {self.acc[i].type}")
                    logger.debug(f"{self.acc[i-1]=}, {self.acc[i]=}")
                    #raise ValueError("Caught unexpected situtuation. Expected (PREVERSEPAR,PARVERSE), got: %,%" %  (self.acc[i-1].type, self.acc[i].type))
            elif self.acc[i].otype == ChunkType.PARUSERSYNC:
                if bi is None:
                    bi=i-1
                logger.log(7, f"Merge.5b: {self.acc[bi].position} , {self.acc[i].position}?")
                self.acc[i].verse = self.acc[i].verse
                self.acc[i].pnum = self.acc[i].pnum
                self.acc[i].insert(0,self.acc[bi][0])
                #self.acc[bi].syncp = self.acc[i].syncp
                #self.acc[bi].type = ChunkType.USERSYNC
                #self.acc[bi].extend(self.acc[i])
                self.acc[bi].deleteme = True
                logger.log(7, f"Merging.5b: {self.acc[bi].position} , {self.acc[i].position}?")
                logger.debug(f"Merged.5b: {'deleteme' in self.acc[bi]}, {self.acc[i]=} {self.acc[bi]=}")
            else:
                bi=None
        # make headings in the intro into intro
        for i in range(1, len(self.acc)):
            c = self.acc[i-1]
            if c.type == ChunkType.HEADING:
                cn = self.acc[i]
                logger.debug(f"Compare.6: {c.position=}, {c.type,cn.type=}")
                if cn.type == ChunkType.PREVERSEPAR:
                    c.verse = cn.verse
                    c.pnum = cn.pnum
                    c.type = ChunkType.PREVERSEHEAD
                    # c.extend(cn)
                    # cn.deleteme = True
                    logger.debug(f"Merged.6: {'deleteme' in c}, {c.position}")
                elif c.type in (ChunkType.CHAPTER, ChunkType.BODY, ChunkType.PREVERSEPAR):
                    pass
                else:
                    c.type = ChunkType.INTRO
        # Swap chapter and heading first
        for i in range(1, len(self.acc)):
          #logger.debug(debstr(self.acc[i].type));
          if  self.acc[i].type == ChunkType.CHAPTER and self.acc[i-1].type == ChunkType.HEADING:
              if not MergeF.SwapChapterHead in settings:
                self.acc[i-1].type = ChunkType.CHAPTERHEAD
                self.acc[i].extend(self.acc[i-1])
                self.acc[i-1].deleteme = True
                logger.debug(f"Merged.7: {'deleteme' in self.acc[i]}, {self.acc[i]}")
          elif self.acc[i-1].type == ChunkType.CHAPTER and self.acc[i].type == ChunkType.CHAPTERHEAD:
              if MergeF.SwapChapterHead in settings:
                logger.debug("SwapChapterHead");
                tmp=self.acc[i-1]
                self.acc[i-1] = self.acc[i]
                self.acc[i] = tmp
                logger.debug(f"Merged.7b: {'deleteme' in self.acc[i]}, {self.acc[i]}")
              else:
                if MergeF.HeadWithChapter in settings:
                    self.acc[i-1].extend(self.acc[i])
                    self.acc[i].deleteme = True
                    logger.debug(f"SwapMerged.7c: {'deleteme' in self.acc[i-1]}, {self.acc[i-1]=}")
        # Merge all chunks between \c and not including \v.
        if 0:
            for i in range(1, len(self.acc)):
                if self.acc[i-1].type == ChunkType.CHAPTER and not self.acc[i].hasVerse:
                    self.acc[i-1].extend(self.acc[i])
                    self.acc[i].deleteme = True
                    if debugPrint:
                        logger.debug(f"Merged.8: {deleteme in self.acc[i-1]}, {self.acc[i-1]}")
        logger.debug("Chunks before reordering: {}".format(len(self.acc)))
        self.acc = [x for x in self.acc if not getattr(x, 'deleteme', False)]
        logger.debug("Chunks after reordering: {}".format(len(self.acc)))
        for i in range(0, len(self.acc)):
            if isinstance(self.acc[i],Chunk):
              logger.log(7, f"r: {i}, {self.acc[i].ident}//{self.acc[i].position}, {self.acc[i].type=}, {self.acc[i]=}")
            else:
              logger.log(7, f"r: {i}, '-//-', {self.acc[i].type=}, {self.acc[i]=}")

    def score(self,results={}):
        """Calculate the scores for each chunk, returning an array of non-zero scores (potential break points)
        If the results parameter is given, then the return value is a summation
        """
        global debugPrint
        logger.debug("SCORES")
        for i in range(0, len(self.acc)):
            t=self.acc[i].type.value
            scval=self.scores[t]
            if self.acc[i][0].name in self.protect:
                logger.debug(f"Protecting \\{self.acc[i][0].name}")
                scval -= self.protect[self.acc[i][0].name]
            self.acc[i].score = scval
            pos=self.acc[i].position
            self.loc[pos] = i
            if pos in results:
                results[pos] += scval
                logger.debug("%s(%s)  + %d = %d" % (pos,self.acc[i][0].name, scval, results[pos]))
            else:
                results[pos] = scval
                logger.debug(f"{pos}({self.acc[i][0].name}) = {scval}")
        return results

    def getofs(self,pos, incremental=True):
        """Return the index into acc[] of the (end-point) pos. If an exact match for pos cannot be found, return the index of the next highest point. If incremental is true, it assumes that calls to this are always done in increasing sequence.
        """
        if pos in self.loc:
            self.lastloc=self.loc[pos]
        else:
            if self.lastloc is None or not incremental:
                self.lastloc = 0
            lim=len(self.acc)
            while self.lastloc < lim and self.acc[self.lastloc].position < pos:
                self.lastloc+=1
        return self.lastloc

def appendpair(pairs, ind, chunks):
    if len(pairs) and pairs[-1][ind] is not None:
        lastp = pairs[-1][ind]
        lastt = _chunkClass_map[lastp.type]
        end = None
        found = False
        for i, c in enumerate(chunks):
            if _chunkClass_map[c.type] == lastt:
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
        lastt = _chunkClass_map[lastp.type]
        logger.debug(f"appendpair:{lastt}")
        if _chunkClass_map[lasts.type] == lastt:
            while len(pchunks) and _chunkClass_map[pchunks[0].type] == lastt:
                lastp.extend(pchunks.pop(0))
                logger.log(7,"P")
            while len(schunks) and _chunkClass_map[schunks[0].type] == lastt:
                lasts.extend(schunks.pop(0))
                logger.log(7,"S")
    logger.debug(f"P: {len(pchunks)} S: {len(schunks)} p{len(pairs)}")
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

def alignChunks(primary, secondary):
    pchunks, pkeys = primary
    schunks, skeys = secondary
    pairs = []
    if isinstance(pchunks, Collector):
        pchunks=pchunks.acc
    if isinstance(schunks, Collector):
        schunks=schunks.acc
    logger.debug(f"alignChunks: {len(pchunks)}, {len(schunks)}")
    logger.log(7, "Primary:" + ", ".join(pkeys));
    logger.log(7, "Secondary:" + ", ".join(skeys));
    diff = difflib.SequenceMatcher(None, pkeys, skeys)
    for op in diff.get_opcodes():
        (action, ab, ae, bb, be) = op
        logger.debug(f"{op}, {debstr(pkeys[ab:ae])}, {debstr(skeys[bb:be])}")
        if action == "equal":
            pairs.extend([[pchunks[ab+i], schunks[bb+i]] for i in range(ae-ab)])
        elif action == "delete":
            appendpair(pairs, 0, pchunks[ab:ae])
        elif action == "insert":
            appendpair(pairs, 1, schunks[bb:be])
        elif action == "replace":
            pgk, pgg = zip(*[(k, list(g)) for k, g in groupby(pchunks[ab:ae], key=lambda c:_chunkClass_map[c.type])])
            sgk, sgg = zip(*[(k, list(g)) for k, g in groupby(schunks[bb:be], key=lambda c:_chunkClass_map[c.type])])
            diffg = difflib.SequenceMatcher(a=pgk, b=sgk)
            for opg in diffg.get_opcodes():
                (actiong, abg, aeg, bbg, beg) = opg
                logger.debug(f"--- {op}, {debstr(pgk[abg:aeg])}, {debstr(sgk[bbg:beg])}")
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

    logger.debug(f"alignChunks: {len(pairs)}")
    return pairs

def alignSimple(primary, *others):
    # import pdb; pdb.set_trace()
    pchunks, pkeys = primary
    if isinstance(pchunks, Collector):
        pchunks=pchunks.acc
    numkeys = len(pkeys)
    runs = [[[x, x]] for x in range(numkeys)]
    runindices = list(range(numkeys))
    for ochunks, okeys in others:
        runs = [x + [None] for x in runs]
        diff = difflib.SequenceMatcher(None, pkeys, okeys)
        for op in diff.get_opcodes():
            (action, ab, ae, bb, be) = op
            logger.log(7,f"{op}, {debstr(pkeys[ab:ae])}, {debstr(okeys[bb:be])}")
            if action == "equal":
                for i in range(ae-ab):
                    ri = runindices[ab+i]
                    if runs[ri][-1] is None:
                        runs[ri][-1] = [bb+i, bb+i]
                    else:
                        runs[ri][-1][1] = bb+i
            if action in ("delete", "replace"):
                ai = runindices[ab]
                for c in range(ab, ae):
                    ri = runindices[c]
                    if ri > ai:
                        for j in len(runs[0]):
                            runs[ai][j][1] = runs[ri][j][1]
                    for j in range(c, numkeys):
                        runindices[j] -= 1
                    runs = runs[:ri] + runs[ri+1:]
            if action in ("insert", "replace"):
                if (ab<numkeys):
                  ai = runindices[ab]
                  runs[ai][-1] = [bb, be-1]
                else: # This might be wrong, but it *seems* to work
                  ai=len(runs)-1
                  bb=runs[ai][-1][0]
                #logger.log(7,f"{debstr(runs)}")
                runs[ai][-1] = [bb, be-1]
                #logger.log(7,f"{debstr(runs)}")
    results = []
    for r in runs:
        res = [Chunk(*sum(pchunks[r[0][0]:r[0][1]+1], []), mode=pchunks[r[0][1]].type)]
        for i, (ochunks, okeys) in enumerate(others, 1):
            res.append(Chunk(*sum(ochunks.acc[r[i][0]:r[i][1]+1], []), mode=ochunks.acc[r[i][1]].type))
        results.append(res)
    return results

def alignScores(*columns):
    # get the basic scores.
    merged={}
    for ochunks, okeys in columns:
        merged=ochunks.score(merged)
    positions=[k for k,v in merged.items()]
    positions.sort()
    logger.debug("Potential sync positions:" + " ".join(map(str,positions)))
    # Ensure headings get split from preceding text if there's a coming break
    oldconfl=None
    conflicts=[]
    for i in range (0, len(positions)-1):
        if globalcl:
          chlist=('CHAPTERHEAD','CHAPTER')
        else:
          chlist=('CHAPTERHEAD')
        if positions[i][_headingidx] in ('HEADING','PREVERSEHEAD'):
            if merged[positions[i+1]] > 99:
                a = 0
                while positions[i-a-1][3] in ('HEADING','PREVERSEHEAD'):
                    a += 1
                logger.debug(f"Splitting between positions {positions[i-a]} and {positions[i+1]}")
                merged[positions[i-a]] = 100
                if MergeF.HeadWithText in settings:
                    merged[positions[i+1]] = 0
                    logger.debug(f"Not splitting between positions {positions[i]} and {positions[i+1]} (score={merged[positions[i+1]]})")
        elif positions[i][_headingidx] in chlist:
            a = 1
            while positions[i+a][_headingidx] in chlist:
                a += 1
            if MergeF.HeadWithText in settings:
                logger.debug(f"Not splitting head from text between positions {positions[i]} and {positions[i+a]}")
                merged[positions[i+a]] = 0
            else:
                logger.debug(f"Splitting head from text between positions {positions[i]} and {positions[i+a]}")
                merged[positions[i+a]] = 100
            
        confl = positions[i][0:_headingidx]
        if confl == oldconfl:
            conflicts.append(positions[i])
            logger.debug(f'matching posn {confl}: {conflicts}')
        else:
            if len(conflicts) > 1:
                tot = 0
                includesCPar = False
                includesHead = False
                includesMVPar = False
                for p in conflicts:
                    tot += merged[p]
                    if (p[_headingidx] == 'CHAPTERPAR'):
                        includesCPar = True
                    if (p[_headingidx] in ( 'HEADING','PREVERSEHEAD')):
                        includesHead = True
                    if (p[_headingidx] == 'MIDVERSEPAR'):
                        includesMVPar = True
                if (not includesCPar) and not (includesMVPar and includesHead):
                    for p in conflicts:
                        del(merged[p])
                    merged[confl] = tot
                    logger.debug(f'Combined score at {confl} ({conflicts}) set to {tot}')
            conflicts = [positions[i]]
        oldconfl = confl
    del positions
    syncpositions = [k for k,v in merged.items() if v >= 100]
    syncpositions.sort()
    logger.debug("Sync positions:" + " ".join(map(str,syncpositions)))
    results = []
    colkeys = {}
    for i in range(0, len(columns)):
        colkeys[columns[i][0].colkey] = i
    logger.debug("colkeys:", colkeys)
    ofs = {}
    blank = {}
    lim = {}
    acc = {}
    coln = {}
    for c, i in colkeys.items():
        ofs[c] = 0
        blank[c] = None
        lim[c] = len(columns[i][0].acc)
        coln[c] = columns[i][0]
        acc[c] = coln[c].acc
    syncpositions.append((999,999,999))
    for posn in syncpositions:
        chunks = blank.copy()
        logger.log(7, f"CHUNK: {posn}, {merged[posn] if posn in merged else '-'}")
        for c,i in colkeys.items():
            nxt = coln[c].getofs(posn) # Get the next offset.
            logger.log(7, f"{c=}, {ofs[c]=} ,{posn=}, {nxt=}, {lim[c]=}")
            if ofs[c] == nxt and nxt < lim[c]:
                logger.log(7, f"not yet: {nxt} = {acc[c][nxt].position}")
            if nxt > lim[c]:
                raise ValueError(f"This shouldn't happen, {nxt} > {lim[c]}!")
            p = merged
            while ofs[c] < lim[c] and ofs[c] < nxt: 
                thispos = acc[c][ofs[c]].position
                logger.log(7,f"{ofs[c]}={thispos} {merged[thispos] if thispos in merged else '0'}")  
                if chunks[c]:
                    chunks[c].append(acc[c][ofs[c]])
                else:
                    chunks[c] = [acc[c][ofs[c]]]
                ofs[c] += 1
            #print()
            if chunks[c]:
                logger.log(7,"".join(map(str,chunks[c])))
        results.append({c: chunks[c] for c in colkeys})
    return results

def createSheets(sheets):
    res = Sheets(sheets[0])
    for s in sheets[1:]:
        res.append(s)

modes = {
    "doc": alignChunks,
    "simple": alignSimple,
    "scores" : alignScores
}

def WriteSyncPoints(mergeconfigfile,variety,confname,scores,synchronise):
    config = {}#configparser.ConfigParser()
    flaga = {}
    for k in MergeF:
      flaga[k.name] = k in settings
    config['FLAGS'] = flaga
    config['DEFAULT'] = {k:(scores[k] if k in scores else  0) for k in ChunkType if k != ChunkType.DEFSCORE}
    config['L'] = {'WEIGHT': 51}
    config['R'] = {'WEIGHT': 51}
    if variety != "":
        config[variety] = {}
    if confname != "":
        config[confname] = {}
    logger.debug(f"Writing default configuration to {mergeconfigfile}")
    with open(mergeconfigfile,'w') as configfile:
        configfile.write("# Custom merge configuration file.\n")
        configfile.write(f"# This was written because no merge-{synchronise}.cfg file could be found.\n")
        configfile.write(f"# As generated it contains all potential break-points the program expects,\n")
        configfile.write(f"# with settings appropriate for the '{synchronise}' merge. Customisation of\n")
        configfile.write(f"# this file can entirely change the behaviour of merge strategy '{synchronise}'\n")
        configfile.write("""#(delete file to reverse any customisation)
#
# YOU HAVE BEEN WARNED! 
# 
# Items in the [FLAGS] section (if specified) are global values, affecting the
# entire merge process, and override the defaults, including such matters as
# whether verses are synchronisation points or not.
#
# Items in the [DEFAULT] section define the global defaults, which apply if
# there are no overriding values in a given section.  Valid sections include
# [L] and [R] (primary and secondary), [configuration], and [variety] for
# custom-variety.
# Sections [L] and [R] are ignored if the file is in the root paratext
# directory.  The scores (from all columns) are added and a sum of 100 or more
# at a given point causes splitting and synchronisation.
# Any value not listed is assumed to be 0.
# Values -2<=x<=2 are treated as multiplyers of the WEIGHT value.  Other values
# are treated as absolute values. Non-integer values (e.g. 0.5) are allowed.
# Chapter and verse numbers are remembered, other break-points increment a
# paragraph counter.\n""")
        #configfile.write("# The number at the end of the comment indicates the group a given break-point falls into,\n")
        #configfile.write("# i.e. to which other positions it will be compared\n")
        for section in config:
            configfile.write(f"\n[{section}]\n\n")
            for k in config[section]:
                v = config[section][k]
                if k in _chunkDesc_map:
                    comment = _chunkDesc_map[k]
                    if not comment.startswith('(!)'):
                        #cannon=_canonical_order[k] if k in _canonical_order else 9
                        #configfile.write(f"#{comment} ({cannon})\n{k.name} = {v}\n")
                        configfile.write(f"#{comment}\n{k.name} = {v}\n")
                elif section == "FLAGS":
                    configfile.write(f"# {k} = {v}\n")
                else:
                    configfile.write(f"{k} = {v}\n")
        #config.write(configfile)

def ReadSyncPoints(mergeconfigfile,column,variety,confname,fallbackweight=51.0):
    """ Given a specified filepath, column (or None if this is a generic config), custime-variety and config name, find the relevant sycnpoints for a given file.
    """
    global settings
    logger.debug(f"Reading config file {mergeconfigfile} for ({column if column is not None else ''}, {variety}, {confname})")
    config = configparser.ConfigParser()
    config.read(mergeconfigfile)
    if config.has_section("FLAGS"):
      for key in MergeF:
        if config.has_option("FLAGS", key.name):
          tf = config.getboolean("FLAGS", key.name)
          logger.debug(f"Flag {key} is set to {tf}")
          if tf:
            settings = settings | key
          else:
            settings = settings & (~key)
    if not config.has_section('zzzDEFAULT'):
        config['zzzDEFAULT'] = {} # make it possible to access the DEFAULT values.
    if column is None:
        if variety == "":
            keys = [confname, "zzzDEFAULT"]
        else:
            keys = [variety, confname, "zzzDEFAULT"]
    else:
        if variety == "":
            keys = [column, confname, "zzzDEFAULT"]
        else:
            keys = [variety + "-" + column, variety, column, confname, "zzzDEFAULT"]
    logger.debug(f"Keys: {keys}")
    for key in keys:
        if config.has_section(key):
            weight = config.getfloat(key, "WEIGHT", fallback=fallbackweight)
            scores={}
            for st in ChunkType:
                if st == ChunkType.DEFSCORE:
                    continue
                val=config.getfloat(key, str(st.name), fallback=0)
                if (val >= -2 and val <= 2):
                    scores[st] = val * weight
                else:
                    scores[st] = val
                logger.log(7,f"score for {st} is {val} -> {scores[st]}")
            return(scores)
        else:
            logger.debug(f"No section {key}")
    if synchronise in  SyncPoints:
        synchronise = "normal"
    logger.debug(f"Did not find expected custom merge section(s) ' {keys} '. Resorting {synchronise}.")
    return(SyncPoints[{synchronise}])
    
def usfmerge2(infilearr, keyarr, outfile, stylesheets=[],stylesheetsa=[], stylesheetsb=[], fsecondary=False, mode="doc", debug=False, scorearr={}, synchronise="normal", protect={}, configarr=None, changes=[], book=None):
    global debugPrint, debstr,settings
    if debug:
      debugPrint = True
      logger.debug("Writing debug files")
    else:
      logger.debug("Not Writing debug files")
    # print(f"{stylesheetsa=}, {stylesheetsb=}, {fsecondary=}, {mode=}, {debug=}")
    tag_escapes = r"[^a-zA-Z0-9]"
    # Check input
    sheets={}
    if len(keyarr) == 0:
        keyarr = ['L', 'R']
    if (len(keyarr) != len(infilearr)):
        raise ValueError("Cannot have %d keys and %d files!" % (len(keyarr),len(infilearr)) )
        
    if type(scorearr) == list:
        tmp = zip(keyarr, scorearr)
        scorearr = {}
        for k, v in tmp:
            if k in scorearr:
                raise ValueError("Cannot have reapeated entries in key array! (%c already seen)" %(k))
            scorearr[k] = int(v)
        del tmp
    logger.debug(f"{type(scorearr)}, {scorearr=}")
    logger.debug(f"{type(keyarr)}, {keyarr=}")
    logger.log(7, f"{stylesheetsa=}, {stylesheetsb=}")
    if configarr is None:
        configarr = {}
        for k in keyarr:
            configarr[k] = None
        
    # load stylesheets
    sheets['L'] = Sheets(stylesheetsa)
    sheets['R'] = Sheets(stylesheetsb)
    for k, s in stylesheets:
        sheets[k] = Sheets(s)
    # Set-up potential synch points
    tmp=synchronise.split(",")
    if len(tmp) == 1:
        syncarr = {k:synchronise for k in keyarr}
    else:
        if len(tmp) != len(keyarr):
            raise ValueError("Cannot have %d keys and %d synchronisation modes!" % (len(keyarr),len(tmp)) )
        else:
            syncarr= {k: val for k, val in zip(keyarr,tmp)}

    logger.debug(f"{type(syncarr)}, {syncarr=}")

    if len(scorearr) == 0:
        s = int(1 + 100 / len(keyarr))
        scorearr = {k: s for k in keyarr}
    elif len(scorearr) != len(keyarr):
        raise ValueError("Cannot have %d keys and %d scores!" % (len(keyarr),len(scorearr)) )

    def texttype(m):
        res = stylesheet.get(m, {'TextType': 'other'}).get('TextType').lower()
        #if res in ('chapternumber', 'versenumber'):
        #   res = 'versetext'
        return res

    debstr = lambda s: s

    def myGroupChunks(*a, **kw):
        return groupChunks(*a, texttype, **kw)
    chunks={}
    chunklocs={}
    colls={}
    if (mode == "scores") or ("verse"  in syncarr) or ("chapter" in syncarr) : #Score-based splitting may force the break-up of an NB, the others certainly will.
        settings =  settings & (~MergeF.NoSplitNB)
    if (mode == "scores") or ("verse"  in syncarr):
        settings = settings | MergeF.ChunkOnVerses
    if (mode == "scores"):
        settings = settings & (~MergeF.HeadWithChapter) #  scores needs them initially separated
        priconfname = None
        priptpath = None
        priconfpath = None
        for colkey,infile in zip(keyarr,infilearr):
            if (colkey == 'L'):
                #Primary might be in a different place to other files, if run
                # from command line. If so, that should take priority.
                (prifilepath, filename) = os.path.split(os.path.abspath(infile))
                priconfname = os.path.basename(prifilepath)
                priptpath = os.path.dirname(os.path.dirname(os.path.dirname(prifilepath)))
                priconfpath = os.path.join(priptpath, "shared", "ptxprint", priconfname)
        for colkey,infile in zip(keyarr, infilearr):
                #if (syncarr[colkey].startswith("custom")):
                # determine the config name; and  determine the custom merge control file.
                # Look for merge config file in : (1) same dir as file, (2) {Project}/shared/ptxprint/{config}, (3) {Project}
                if (syncarr[colkey] == "custom"):
                    variety=""
                    varfile = None
                else:
                    variety=syncarr[colkey][7:]
                    varfile = "merge-" + synchronise+variety + ".cfg"
                (filepath,filename) = os.path.split(os.path.abspath(infile))
                confname = os.path.basename(filepath)
                ptpath = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))
                confpath = os.path.join(ptpath, "shared", "ptxprint", confname)
                searchlist = []
                cfile="merge-" + synchronise + ".cfg"
                if (varfile is not None):
                    if (colkey != 'L' and prifilepath != filepath):
                        searchlist.extend(((os.path.join(prifilepath,varfile),1),(os.path.join(priconfpath,varfile),1)))
                    searchlist.extend(((os.path.join(filepath,varfile),1),(os.path.join(confpath,varfile),1),(os.path.join(ptpath,varfile),0)))
                    
                searchlist.extend(((os.path.join(prifilepath,cfile),1),(os.path.join(priconfpath,cfile),1),(os.path.join(priptpath,cfile),0)))
                if (colkey!='L' and prifilepath != filepath):
                    searchlist.extend((os.path.join(ptpath,cfile),0))
                done=0
                for searchpair in searchlist:
                    (confpath,useLR)=searchpair
                    logger.debug(f"Checking if {colkey} config file {confpath} exists")
                    if (os.path.exists(confpath)):
                        scorearr[colkey]=ReadSyncPoints(confpath,(colkey if useLR else None),variety,confname)
                        logger.debug(f"found {confpath}!")
                        done=1
                        break
                if (not done):
                    logger.debug(f"Did not find expected custom merge file. Resorting to normal.")
                    if os.path.exists(priconfpath):
                        WriteSyncPoints(os.path.join(priconfpath,cfile),variety,confname,SyncPoints[synchronise],synchronise)
                    else:
                        WriteSyncPoints(os.path.join(prifilepath,cfile),variety,confname,SyncPoints[synchronise],synchronise)

    for colkey,infile in zip(keyarr,infilearr):
        logger.debug(f"Reading {colkey}: {infile}")
        with open(infile, encoding="utf-8") as inf:
            doc = Usfm.readfile(infile, sheet=sheets[colkey])
            colls[colkey] = Collector(doc=doc, colkey=colkey, primary=(colkey=='L'), fsecondary=fsecondary, stylesheet=sheets[colkey], scores=scorearr[colkey],synchronise=syncarr[colkey],protect=protect)
        chunks[colkey] = {c.ident: c for c in colls[colkey].acc}
        chunklocs[colkey] = ["_".join(str(x) for x in c.ident) for c in colls[colkey].acc]

    f = modes[mode]
    pairs = f(*((colls[k], chunklocs[k]) for k in keyarr))

    debugf={}
    if debugPrint:
      logger.debug("opening debug files")
      for col in keyarr:
        if outfile is None:
          debugf[col]=open("mergerewrite-"+col,"w",encoding="utf-8")
        else:
          debugf[col]=open(outfile+"-"+col,"w",encoding="utf-8")
    if len(changes):
        outf = io.StringIO()
    elif outfile is not None:
        outf = open(outfile, "w", encoding="utf-8")
    else:
        outf = sys.stdout

    if mode in ('scores',):
        for i, p in enumerate(pairs):
            for col,data in p.items():
                if data is not None:
                    outf.write("\\polyglotcolumn %c\n" % col)
                    for d in data:
                        s=re.sub(r"\\zcolsync.*?\\\*","",str(d))
                        outf.write(s)
                        if debugPrint:
                          debugf[col].write(str(d))
            outf.write("\n\\polyglotendcols\n")
    else:
        isright = True
        for i, p in enumerate(pairs):
            if p[0] is not None and len(p[0]):
                #outf.write("\\rem " + str(p[0].ident) + str(p[0].type) + "\n")
                outf.write("\\polyglotcolumn L\n")
                outf.write(str(p[0]))
                if debugPrint:
                  debugf['L'].write(str(p[0]))
                if not (p[0].type in  (ChunkType.PREVERSEHEAD, ChunkType.HEADING, ChunkType.TITLE, ChunkType.CHAPTERHEAD)):
                    outf.write("\\p\n")
            if p[1] is not None and len(p[1]):
                outf.write("\\polyglotcolumn R\n")
                isright = True
                outf.write(str(p[1]))
                if debugPrint:
                  debugf['R'].write(str(p[1]))
                if not (p[1].type in  (ChunkType.PREVERSEHEAD, ChunkType.HEADING, ChunkType.TITLE, ChunkType.CHAPTERHEAD)):
                    outf.write("\\p\n")
            outf.write("\\polyglotendcols\n")
    if len(changes):
        text = out.getvalue()
        out.close()
        text = runChanges(changes, book, text)
        if outfile is not None:
            with open(outfile, "w", encoding="utf-8") as outf:
                outf.write(text)
        else:
            print(text)


