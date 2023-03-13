#!/usr/bin/python3
import sys, os, re
import ptxprint.sfm as sfm
from ptxprint.sfm import usfm
from ptxprint.sfm import style
import argparse, difflib, sys
from enum import Enum,Flag
from itertools import groupby
import logging

class MergeF(Flag):
    ChunkOnVerses=1
    NoSplitNB=2
    HeadWithText=4
    SwapChapterHead=8

settings= MergeF.NoSplitNB
logger = logging.getLogger(__name__)
debugPrint = False
class ChunkType(Enum):
    DEFSCORE = 0        # Value for default scores
    CHAPTER = 1
    HEADING = 2
    TITLE = 3
    INTRO = 4
    BODY = 5
    ID = 6
    TABLE = 7
    VERSE = 8           # A verse chunk, inside a paragraph 
    PARVERSE = 9           # A verse chunk, just after a paragraph 
    MIDVERSEPAR = 10     # A verse immediately after a paragraph
    PREVERSEPAR = 11    # A paragrpah where the next content is a verse number
    NOVERSEPAR = 12     # A paragraph which is not in verse-text, e.g inside a side-bar, or book/chapter introduction
    NPARA = 13          # A nested paragraph 
    NB = 14             # A nobreak mark 
    NBCHAPTER = 15      # A chapter that is followed by an NB
    CHAPTERPAR = 16      # A PREVERSEPAR that is following a chapter - never a good sync point!
    CHAPTERHEAD=17      #A Heading that is (was) following a chapter 
    PREVERSEHEAD=18      #A Heading that is just before  a verse 
    USERSYNC=19        #A preprocessing-inserted break point.


_chunkClass_map = {
ChunkType.DEFSCORE:'',
ChunkType.CHAPTER:'CHAPTER',
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
ChunkType.CHAPTERHEAD:'HEADING',
ChunkType.PREVERSEHEAD:'HEADING',
ChunkType.USERSYNC:'BODY'
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
    'id': ChunkType.TITLE,
    'ide': ChunkType.TITLE,
    'h': ChunkType.TITLE,
    'toc1': ChunkType.TITLE,
    'toc2': ChunkType.TITLE,
    'toc3': ChunkType.TITLE,
    'v': ChunkType.VERSE,
    'cl': ChunkType.CHAPTER,
    'nb': ChunkType.NB
}

_canonical_order={
    ChunkType.ID:0,
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
}
    

class Chunk(list):
    def __init__(self, *a, mode=None, chap=0, verse=0, end=0, pnum=0):
        super(Chunk, self).__init__(a)
        self.type = mode
        self.chap = chap
        self.verse = verse
        self.end = verse
        self.pnum = pnum
        self.hasVerse = False
        if mode in (ChunkType.MIDVERSEPAR, ChunkType.VERSE, ChunkType.PARVERSE):
            self.verseText = True
        else:
            self.verseText = False
        self.labelled = False
        self.score = None

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
    def position(self):
        return((self.chap,self.verse,_canonical_order[self.type] if self.type in _canonical_order else 9, self.pnum, self.type.name if self.type.name != 'VERSE' else '@VERSE'))
        #return("%03d:%03d:%04d:%s" % (self.chap,self.verse,self.pnum,self.type.name))

    @property
    def ident(self):
        if len(self) == 0:
            return ("", 0, 0,0) # , 0, 0)
        return (_chunkClass_map[self.type], self.chap, self.verse, self.pnum) # , self.end, self.pnum)

    def __str__(self):
        #return "".join(repr(x) for x in self)
        #return "".join(sfm.generate(x) for x in self)
        return sfm.generate(self)
_headingidx=4
_validatedhpi=False

nestedparas = set(('io2', 'io3', 'io4', 'toc2', 'toc3', 'ili2', 'cp', 'cl' ))

SyncPoints = {
    "chapter":{ChunkType.VERSE:0,ChunkType.PREVERSEPAR:0,ChunkType.PREVERSEHEAD:0,ChunkType.NOVERSEPAR:0,ChunkType.MIDVERSEPAR:0,ChunkType.HEADING:0,ChunkType.CHAPTER:1,ChunkType.CHAPTERPAR:0,ChunkType.NBCHAPTER:1,ChunkType.USERSYNC:1}, # Just split at chapters
    "normal":{ChunkType.VERSE:0,ChunkType.PREVERSEPAR:1,ChunkType.PREVERSEHEAD:1,ChunkType.NOVERSEPAR:1,ChunkType.MIDVERSEPAR:1,ChunkType.HEADING:1,ChunkType.CHAPTER:1,ChunkType.CHAPTERPAR:0,ChunkType.USERSYNC:1}, 
    "verse":{ChunkType.VERSE:1,ChunkType.PREVERSEPAR:1,ChunkType.PREVERSEHEAD:1,ChunkType.NOVERSEPAR:0,ChunkType.MIDVERSEPAR:0,ChunkType.HEADING:1,ChunkType.CHAPTER:1,ChunkType.CHAPTERPAR:0,ChunkType.NBCHAPTER:1,ChunkType.USERSYNC:1} # split at every verse
}

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
        self.scores = {ChunkType.USERSYNC.value:100} # a usersync is always a sync-point
        self.currChunk = None
        self.mode = ChunkType.INTRO
        self.oldmode= None
        if (scores==None):
            raise ValueError("Scores can be integer or ChunkType:Score values, but must be supplied!")
        logger.debug(f"Scores supplied are: {type(scores)}, {scores=}")
        if synchronise in SyncPoints:
            logger.debug(f"Sync points: {synchronise.lower()}")
            syncpoints=SyncPoints[synchronise.lower()] 
        else:
            syncpoints=SyncPoints['normal'] 
            logger.debug("Sync points are normal")

        if (type(scores)==int):
            tmp=scores
            scores={ChunkType.DEFSCORE:tmp}
            logger.debug(f"Default score = {scores[ChunkType.DEFSCORE]}")
        if 'nb' in self.protect:
            logger.debug(f"Protecing nbchapter, like nb")
            self.scores[ChunkType.NBCHAPTER.value]=-self.protect['nb']
            logger.debug(self.scores)
        for st in ChunkType:
            if st.value==ChunkType.DEFSCORE:
                self.scores[st.value]=scores[st]
            else:
                if (st.value not in self.scores):
                    self.scores[st.value]=0
                if (st in scores):
                    self.scores[st.value]+=scores[st] 
                elif (st in syncpoints):
                    self.scores[st.value]+=scores[ChunkType.DEFSCORE] * syncpoints[st]
 
            #if (self.scores[st.value]):
            #    splitpoints[st] = True
            #else:
            #    if (st not in splitpoints):
            #        splitpoints[st] = False
            logger.debug(f"Score for {st}({st.value}) -> {self.scores[st.value]}, {syncpoints[st] if st in syncpoints else '-'}")
        if doc is not None:
            self.collect(doc, primary=primary)
            self.reorder()

    def pnum(self, c):
        if c is None:
            return 0
        if hasattr(c,'name') :
            n=c.name
        else:
            n=c
        res = self.counts.get(n, 0)
        #if debugPrint:
             #print(n,res)
        self.counts[n] = res + 1
        return res

    def makeChunk(self, c=None):
        global _validatedhpi,_headingidx
        if c is None:
            currChunk = Chunk(mode=self.mode)
            self.waspar = False
            self.waschap = False
        else:
            if c.name == "cl":
                mode = ChunkType.TITLE if self.chap == 0 else ChunkType.HEADING
            elif c.name == "id":
                mode = ChunkType.ID
            elif c.name == "nb":
                mode = ChunkType.NB
            elif c.name == "tr":
                mode = ChunkType.TABLE
            elif sfm.text_properties('diglotsync')(c):
                mode = ChunkType.USERSYNC
            elif c.name in nestedparas:
                mode = ChunkType.NPARA
            elif c.name == "v":
                if self.waspar:
                    mode = ChunkType.PARVERSE
                else:
                    mode = ChunkType.VERSE
            else:
                mode = _marker_modes.get(c.name, _textype_map.get(str(c.meta.get('TextType')), self.mode))
                if mode == ChunkType.HEADING:
                    if self.waschap:
                        mode = ChunkType.CHAPTERHEAD
                elif mode == ChunkType.BODY and ispara(c):
                    logger.log(7, f'Bodypar: vt?{self.currChunk.verseText} hv?{self.currChunk.hasVerse}: {len(self.acc)}')
                    if len(c)==1 and isinstance(c[0],sfm.Text):
                        logger.log(7, f'Bodypar(simple): {c.name} {c[0]} {type(c[0])}')
                        if (len(c[0])>2 and self.currChunk.verseText):
                            mode = ChunkType.MIDVERSEPAR
                    elif (len(c)>1):
                        #Multi-component body paragraph
                        logger.log(7, f'Bodypar: {c.name}, {type(c[0])}, {c[0]}, {type(c[1])}, {c[1]}')
                        if (len(c[0])>2 and self.currChunk.verseText):
                            mode = ChunkType.MIDVERSEPAR
                        elif(isinstance(c[0],sfm.Element)):
                            if (c[0].name=="v" ):
                                mode = ChunkType.PREVERSEPAR
                        elif(isinstance(c[1],sfm.Element)):
                            if (c[1].name=="v" ):
                                mode = ChunkType.PREVERSEPAR
                        elif(isinstance(c[1],sfm.Text)):
                            if self.currChunk.verseText:
                                mode = ChunkType.MIDVERSEPAR
                    logger.log(7, f"Conclusion: bodypar type is {mode}")
                        
            currChunk = Chunk(mode=mode, chap=self.chap, verse=self.verse, end=self.end, pnum=self.pnum(mode))
            if not _validatedhpi:
                p=currChunk.position
                assert p[_headingidx]==mode.name, "It looks like someone altered the position tuple, but didn't update _headingidx"
                _validatedhpi=True
            self.waspar = ispara(c)
            self.waschap = (mode in (ChunkType.CHAPTER,ChunkType.CHAPTERHEAD))
            self.mode = mode
        self.acc.append(currChunk)
        self.currChunk = currChunk
        return currChunk

    def collect(self, root, primary=True, depth=0):
        ischap = sfm.text_properties('chapter')
        isverse = sfm.text_properties('verse')
        issync = sfm.text_properties('diglotsync')

        currChunk = None
        if depth==0:
            self.type=None
        else:
            logger.debug("{" * depth)
        elements = root[:]
        if len(self.acc) == 0:
            if isinstance(root[0], sfm.Element) and root[0].name == "id":
                # turn \id into a paragraph level and main children as siblings
                elements = root[0][1:]
                idel = sfm.Element(root[0].name, args=root[0].args[:], content=root[0][0], meta=root[0].meta)
                currChunk = self.makeChunk(idel)
                currChunk.append(idel)
        for c in elements:
            if not isinstance(c, sfm.Element): 
                if (isinstance(c,sfm.Text) and len(c)>3):
                    self.waspar=False
                if(currChunk): # It's a text node, make sure it's attached to the right place.
                    currChunk.append(c)
                    root.remove(c)
                continue
            if c.name == "fig":
                if self.fsecondary == primary:
                    root.remove(c)
                    continue
            newchunk = False
            if ispara(c):
                newmode = _marker_modes.get(c.name, _textype_map.get(str(c.meta.get('TextType')), self.mode))
                if c.name not in nestedparas and (newmode != self.mode \
                                                  or self.mode not in (ChunkType.HEADING, ChunkType.CHAPTERHEAD, ChunkType.TITLE)):
                    newchunk = True
            if issync(c):
                newchunk = True
            if isverse(c):
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
                self.currChunk.hasVerse = True
                if MergeF.ChunkOnVerses in settings:
                    newchunk = True
                else:
                    self.currChunk.label(self.chap, self.verse, self.end, 0)
                logger.log(7, f" {self.chap}:{self.verse} {c.name} {newchunk} context: {self.oldmode}, {self.mode  if isinstance(c, sfm.Element) else '-'}")
            if newchunk:
                self.oldmode=self.mode
                currChunk = self.makeChunk(c)
                if MergeF.ChunkOnVerses in settings:
                    if isverse(c):
                        currChunk.hasVerse = True # By definition!
                        self.currChunk.label(self.chap, self.verse, self.end, 0)
                        self.currChunk.hasVerse = True
                #elif (currChunk.type==ChunkType.BODY and ispara(c) and self.oldmode == ChunkType.MIDVERSEPAR): 
                    #currChunk.type=ChunkType.MIDVERSEPAR
            if currChunk is not None:
                currChunk.append(c)
                if c in root:
                    root.remove(c)      # now separate thing in a chunk, it can't be in the content of something
            if ischap(c):
                self.verse = 0
                vc = re.sub(r"[^0-9\-]", "", c.args[0])
                try:
                    self.chap = int(vc)
                except (ValueError, TypeError):
                    self.chap = 0
                if currChunk is not None:
                    currChunk.chap = self.chap
                    currChunk.verse = self.verse
                newc = sfm.Element(c.name, pos=c.pos, parent=c.parent, args=c.args, meta=c.meta)
                currChunk[-1] = newc
            currChunk = self.collect(c, primary=primary,depth=1+depth) or currChunk
        logger.debug("}" * depth)
        return currChunk

    def reorder(self):
        # Merge contiguous title and table chunks, Merge in nested paragraphs
        ti = None
        bi = None
        ni = None
        #for i in range(0, 10):
            #print(i,self.acc[i].ident if isinstance(self.acc[i],Chunk) else '-' ,self.acc[i].type,self.acc[i])
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
                self.acc[i-1].type=ChunkType.NBCHAPTER
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
        for i in range(1, len(self.acc) - 1):
            if self.acc[i].type == ChunkType.PARVERSE:
                if  self.acc[i-1].type in (ChunkType.PREVERSEPAR, ChunkType.NB):
                    # A PARVERSE gives its address and content up to the preceeding PREVERSEPAR, as the two may not be seperated
                    if bi is None:
                        bi=i-1
                    self.acc[bi].verse=self.acc[i].verse
                    self.acc[bi].pnum=self.acc[i].pnum
                    self.acc[bi].extend(self.acc[i])
                    self.acc[i].deleteme = True
                    logger.debug(f"Merged.5: {'deleteme' in self.acc[bi]}, {self.acc[bi].position}")
                    if bi>1 and self.acc[bi-1].type == ChunkType.CHAPTER:
                        self.acc[bi].type=ChunkType.CHAPTERPAR
                elif (self.acc[i-1].type in (ChunkType.CHAPTER, ChunkType.NBCHAPTER)):
                    pass 
                else:
                    logger.debug(f"Caught unexpected situtuation. Expected (PREVERSEPAR,PARVERSE), got: {self.acc[i-1].type} {self.acc[i].type}")
                    logger.debug(f"{self.acc[i-1]=}, {self.acc[i]=}")
                    #raise ValueError("Caught unexpected situtuation. Expected (PREVERSEPAR,PARVERSE), got: %,%" %  (self.acc[i-1].type, self.acc[i].type))
            else:
                bi=None
        # make headings in the intro into intro
        for i in range(1, len(self.acc)):
            c = self.acc[i-1]
            if c.type == ChunkType.HEADING:
                cn = self.acc[i]
                logger.debug(f"Compare.6: {c.position=}, {c.type,cn.type=}")
                if cn.type == ChunkType.PREVERSEPAR:
                    c.verse=cn.verse
                    c.pnum=cn.pnum
                    c.type=ChunkType.PREVERSEHEAD
                    # c.extend(cn)
                    # cn.deleteme = True
                    logger.debug(f"Merged.6: {'deleteme' in c}, {c.position}")
                elif c.type in (ChunkType.CHAPTER, ChunkType.BODY, ChunkType.PREVERSEPAR):
                    pass
                else:
                    c.type == ChunkType.INTRO
        # Swap chapter and heading first
        if MergeF.SwapChapterHead in settings:
          for i in range(1, len(self.acc)):
            if  self.acc[i].type == ChunkType.CHAPTER and self.acc[i-1].type == ChunkType.HEADING:
                self.acc[i].extend(self.acc[i-1])
                self.acc[i-1].deleteme = True
                logger.debug(f"Merged.7: {'deleteme' in self.acc[i]}, {self.acc[i]}")
            elif self.acc[i-1].type == ChunkType.CHAPTER and self.acc[i].type == ChunkType.HEADING:
                self.acc[i].type=ChunkType.CHAPTERHEAD
                tmp=self.acc[i-1]
                self.acc[i-1]=self.acc[i]
                self.acc[i]=tmp
                logger.debug(f"Swapped: {'deleteme' in self.acc[i-1]}, {self.acc[i-1]=}, {self.acc[i]=}")
        # Merge all chunks between \c and not including \v.
        if 0:
            for i in range(1, len(self.acc)):
                if self.acc[i-1].type == ChunkType.CHAPTER and not self.acc[i].hasVerse:
                    self.acc[i-1].extend(self.acc[i])
                    self.acc[i].deleteme = True
                    if debugPrint:
                        print('Merged.8:', 'deleteme' in self.acc[i-1], self.acc[i-1])
        # merge \c with body chunk following
        if 0:
            lastchunk = None
            prelastchunk = None
            for i in range(1, len(self.acc)):
                if getattr(self.acc[i], 'deleteme', False):
                    continue
                if lastchunk is not None and lastchunk.type == ChunkType.CHAPTER and self.acc[i].type == ChunkType.BODY:
                    tag = self.acc[i][0].name
                    lastchunk.extend(self.acc[i])
                    lastchunk.type = self.acc[i].type
                    self.acc[i].deleteme = True
                    if tag == "nb" and prelastchunk is not None:
                        prelastchunk.extend(lastchunk)
                        lastchunk.deleteme = True
                    elif tag.startswith("q") and i < len(self.acc) - 1 and self.acc[i+1][0].name.startswith("q"):
                        lastchunk.extend(self.acc[i+1])
                        self.acc[i+1].deleteme = True
                if not getattr(lastchunk, 'deleteme', False):
                    prelastchunk = lastchunk
                else:
                    lastchunk = prelastchunk
                    prelastchunk = None     # can't really move backwards
                if not getattr(self.acc[i], 'deleteme', False):
                    lastchunk = self.acc[i]
        logger.debug("Chunks before reordering: {}".format(len(self.acc)))
        self.acc = [x for x in self.acc if not getattr(x, 'deleteme', False)]
        logger.debug("Chunks after reordering: {}".format(len(self.acc)))
        for i in range(0, len(self.acc)):
            logger.log(7, f"{i}, {self.acc[i].ident if isinstance(self.acc[i],Chunk) else '-'}, {self.acc[i].type=}, {self.acc[i]=}")
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
            self.acc[i].score=scval
            pos=self.acc[i].position
            self.loc[pos]=i
            if pos in results:
                results[pos]+=scval
                logger.debug("%s(%s)  + %d = %d" % (pos,self.acc[i][0].name, scval, results[pos]))
            else:
                results[pos]=scval
                logger.debug(f"{pos} = {scval}")
        return results
    def getofs(self,pos, incremental=True):
        """Return the index into acc[] of the (end-point) pos. If an exact match for pos cannot be found, return the index of the next highest point. If incremental is true, it assumes that calls to this are always done in increasing sequence.
        """
        if (pos in self.loc):
            self.lastloc=self.loc[pos]
        else:
            if (self.lastloc is None) or (not incremental):
                self.lastloc=0
            lim=len(self.acc)
            while self.lastloc< lim and self.acc[self.lastloc].position < pos:
                self.lastloc+=1
        return self.lastloc

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

def alignChunks(primary, secondary):
    pchunks, pkeys = primary
    schunks, skeys = secondary
    pairs = []
    if isinstance(pchunks, Collector):
        pchunks=pchunks.acc
    if isinstance(schunks, Collector):
        schunks=schunks.acc
    diff = difflib.SequenceMatcher(None, pkeys, skeys)
    for op in diff.get_opcodes():
        (action, ab, ae, bb, be) = op
        logger.log(7, f"{op}, {debstr(pkeys[ab:ae])}, {debstr(skeys[bb:be])}")
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
                logger.log(7, f"--- {opg}, {debstr(pgk[abg:aeg])}, {debstr(sgk[bbg:beg])}")
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
                ai = runindices[ab]
                runs[ai][-1] = [bb, be-1]
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
    # Ensure headings get split from preceding text if there's a coming break
    oldconfl=None
    conflicts=[]
    for i in range (0,len(positions)-1):
        if(positions[i][_headingidx] in ('HEADING','PREVERSEHEAD')):
            if (merged[positions[i+1]]>99):
                a=0
                while positions[i-a-1][3] in ('HEADING','PREVERSEHEAD'):
                    a+=1
                logger.debug(f"Splitting between positions {positions[i-a]} and {positions[i+1]}")
                merged[positions[i-a]]=100
                if MergeF.HeadWithText in settings:
                    merged[positions[i+1]]=0
                logger.debug(f"Not splitting between positions {positions[i]} and {positions[i+1]} (score={merged[positions[i+1]]})")
        elif(positions[i][_headingidx]=='CHAPTERHEAD'):
            a=1
            while(positions[i+a][_headingidx]=='CHAPTERHEAD'):
                a+=1
            if (merged[positions[i+a]]>99):
                if MergeF.HeadWithText in settings:
                    merged[positions[i+a]]=0
            
        confl=positions[i][0:(_headingidx)]
        if confl==oldconfl:
            conflicts.append(positions[i])
            print(f'matching posn {confl}: {conflicts}')
        else:
            if len(conflicts)>1:
                tot=0
                includesCPar = False
                includesHead = False
                includesMVPar = False
                for p in conflicts:
                    tot+=merged[p]
                    if (p[_headingidx] == 'CHAPTERPAR'):
                        includesCPar = True
                    if (p[_headingidx] in ( 'HEADING','PREVERSEHEAD')):
                        includesHead = True
                    if (p[_headingidx] == 'MIDVERSEPAR'):
                        includesMVPar = True
                if (not includesCPar) and not (includesMVPar and includesHead):
                    for p in conflicts:
                        del(merged[p])
                    merged[confl]=tot
                    print(f'Combined score at {confl} ({conflicts}) set to {tot}')
            conflicts=[positions[i]]
        oldconfl=confl
    del positions
    syncpositions=[k for k,v in merged.items() if v>=100]
    syncpositions.sort()
    print(syncpositions, sep=" ")
    results=[]
    colkeys={}
    for i in range(0,len(columns)):
        colkeys[columns[i][0].colkey]=i
    print("colkeys:", colkeys)
    ofs={}
    blank={}
    lim={}
    acc={}
    coln={}
    for c,i in colkeys.items():
        ofs[c]=0
        blank[c]=None
        lim[c]=len(columns[i][0].acc)
        coln[c]=columns[i][0]
        acc[c]=coln[c].acc
    syncpositions.append((999,999,999))
    for posn in syncpositions:
        chunks=blank.copy()
        logger.log(7, f"CHUNK: {posn}, {merged[posn] if posn in merged else '-'}")
        for c,i in colkeys.items():
            nxt=coln[c].getofs(posn) # Get the next offset.
            logger.log(7, f"{c=}, {ofs[c]=} ,{nxt=}, {lim[c]=}")
            if (ofs[c]==nxt and nxt<lim[c]):
                logger.log(7, f"not yet: {nxt} = {acc[c][nxt].position}")
            if (nxt>lim[c]):
                raise ValueError(f"This shouldn't happen, {nxt} > {lim[c]}!")
            p=merged
            while (ofs[c]<lim[c]) and (ofs[c]<nxt): 
                thispos=acc[c][ofs[c]].position
                logger.log(7,"=".join(ofs[c], thispos, merged[thispos] if thispos in merged else '0' ))  
                if chunks[c]:
                    chunks[c].append(acc[c][ofs[c]])
                else:
                    chunks[c]=[acc[c][ofs[c]]]
                ofs[c]+=1
            #print()
            if (chunks[c]):
                print(*chunks[c], sep="")
        results.append({c:chunks[c] for c in colkeys})
    return results

def appendsheet(fname, sheet):
    if os.path.exists(fname):
        with open(fname) as s:
            sheet = style.update_sheet(sheet, style.parse(s))
    return sheet

modes = {
    "doc": alignChunks,
    "simple": alignSimple,
    "scores" : alignScores
}

def usfmerge2(infilearr, keyarr, outfile, stylesheets=[],stylesheetsa=[], stylesheetsb=[], fsecondary=False, mode="doc", debug=False, scorearr={}, synchronise="normal",protect={}):
    global debugPrint, debstr,settings
    # print(f"{stylesheetsa=}, {stylesheetsb=}, {fsecondary=}, {mode=}, {debug=}")
    tag_escapes = r"[^a-zA-Z0-9]"
    # Check input
    sheets={}
    if len(keyarr)==0:
        keyarr=['L','R']
    if (len(keyarr) != len(infilearr)):
        raise ValueError("Cannot have %d keys and %d files!" % (len(keyarr),len(infilearr)) )
        
    if type(scorearr)==list:
        tmp=zip(keyarr,scorearr)
        scorearr={}
        for k,v in tmp:
            if k in scorearr:
                raise ValueError("Cannot have reapeated entries in key array! (%c already seen)" %(k))
            scorearr[k]=int(v)
        del tmp
    logger.debug(f"{type(scorearr)}, {scorearr=}")
    logger.debug(f"{type(keyarr)}, {keyarr=}")
    logger.log(7, f"{stylesheetsa=}, {stylesheetsb=}")
    
    # load stylesheets
    for k in keyarr[:]:
        logger.debug(f"defining stylesheet {k}")
        sheets[k]=usfm._load_cached_stylesheet('usfm_sb.sty')
    for s in stylesheetsa:
        logger.log(7, f"Appending {s} to stylesheet L")
        sheets['L']=appendsheet(s, sheets['L'])
    for s in stylesheetsb:
        logger.log(7, f"Appending {s} to stylesheet R")
        sheets['R']=appendsheet(s, sheets['R'])
    for k,s in stylesheets:
        logger.log(7, f"Appending {s} to stylesheet {k}")
        sheets[k] = appendsheet(s,sheet[k])
    # Set-up potential synch points
    tmp=synchronise.split(",")
    if len(tmp)==1:
        syncarr={k:synchronise for k in keyarr}
    else:
        if len(tmp)!=len(keyarr):
            raise ValueError("Cannot have %d keys and %d synchronisation modes!" % (len(keyarr),len(tmp)) )
        else:
            syncarr=tmp


    if len(scorearr)==0:
        s=int(1+100/len(keyarr))
        scorearr={k:s for k in keyarr}
    elif len(scorearr)!=len(keyarr) :
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
        settings= settings | MergeF.ChunkOnVerses
    if (mode != "scores"):
        settings = settings | MergeF.SwapChapterHead
    for colkey,infile in zip(keyarr,infilearr):
        logger.debug(f"Reading {colkey}: {infile}")
        with open(infile, encoding="utf-8") as inf:
            doc = list(usfm.parser(inf, stylesheet=sheets[colkey],
                                   canonicalise_footnotes=False, tag_escapes=tag_escapes))
            while len(doc) > 1:
                if isinstance(doc[0], sfm.Text):
                    doc.pop(0)
                else:
                    break
            colls[colkey] = Collector(doc=doc, colkey=colkey, fsecondary=fsecondary, stylesheet=sheets[colkey], scores=scorearr[colkey],synchronise=syncarr[colkey],protect=protect)
        chunks[colkey] = {c.ident: c for c in colls[colkey].acc}
        chunklocs[colkey] = ["_".join(str(x) for x in c.ident) for c in colls[colkey].acc]

    f = modes[mode]
    pairs = f(*((colls[k], chunklocs[k]) for k in keyarr))

    if outfile is not None:
        outf = open(outfile, "w", encoding="utf-8")
    else:
        outf = sys.stdout

    if mode in ('scores'):
        for i, p in enumerate(pairs):
            for col,data in p.items():
                if data is not None:
                    outf.write("\\polyglotcolumn %c\n" % col)
                    for d in data:
                        outf.write(str(d))
            outf.write("\n\\polyglotendcols\n")
    else:
        isright = True
        for i, p in enumerate(pairs):
            if p[0] is not None and len(p[0]):
                outf.write("\\polyglotcolumn L\n")
                outf.write(str(p[0]))
                if p[0].type != ChunkType.HEADING and p[0].type != ChunkType.TITLE:
                    outf.write("\\p\n")
            if p[1] is not None and len(p[1]):
                outf.write("\\polyglotcolumn R\n")
                isright = True
                outf.write(str(p[1]))
                if p[1].type != ChunkType.HEADING and p[1].type != ChunkType.TITLE:
                    outf.write("\\p\n")
            outf.write("\\polyglotendcols\n")


