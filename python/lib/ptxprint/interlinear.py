from xml.etree import ElementTree as et
from ptxprint.usxutils import Usfm
from hashlib import md5
from ptxprint.reference import Reference
from usfmtc.usxmodel import iterusx
import re, os
import logging

logger = logging.getLogger(__name__)

_refre = re.compile(r"^(\d?\D+?)\s+(\d+):(\S+)\s*$")

def mkvss(v):
    res = []
    vs = v.split("-")
    for a in vs:
        m = re.match(r'(\d+)(\D*)', a)
        if m is None:
            res.append((0, ''))
        else:
            res.append((int(m.group(1)), m.group(2)))
    return res

def vcmp(a, b):
    avs = mkvss(a)
    bvs = mkvss(b)
    if avs == bvs:
        return 0
    elif avs > bvs:
        return 1
    return -1

class Interlinear:
    def __init__(self, lang, prjdir):
        self.lang = lang
        self.prjdir = prjdir
        self.fails = []
        lexpath = os.path.join(prjdir, "Lexicon.xml")
        if os.path.exists:
            self.read_lexicon(lexpath)

    def read_lexicon(self, fname):
        self.lexicon = {}
        for (event, e) in et.iterparse(fname, ("start", "end")):
            if event == "start":
                if e.tag == "item":
                    currlex = None
                    currsense = None
                elif e.tag == "Lexeme":
                    currlex = e.get("Type") + ":" + e.get("Form")
                elif e.tag == "Sense":
                    currsense = e.get("Id")
            elif event == "end":
                if e.tag == "Gloss":
                    if e.get("Language") == self.lang:
                        self.lexicon.setdefault(currlex, {})[currsense] = e.text or ""

    def makeref(self, s):
        # use Reference here and do it properly
        m = _refre.match(s)
        if m:
            return (int(m[2]), m[3])
        else:
            raise SyntaxError("Bad Reference {}".format(s))

    def replaceusx(self, doc, curref, lexemes, linelengths, mrk="wit"):
        if curref[0] >= len(doc.chapters):
            return
        parindex = doc.chapters[curref[0]]
        lexemes.sort()
        if curref[1] == "0":
            def stop(e):
                return e.tag == 'verse'
            def start(e):
                return e.tag == "chapter"
        else:
            def stop(e):
                return doc.getroot()[parindex] != e and (e.tag == 'chapter' or (e.tag == 'verse' and vcmp(e.get('number', "0"), curref[1]) > 0))
            def start(e):
                return e.tag == "verse" and e.get('number', 0) == curref[1]
        basepos = None
        for eloc, isin in iterusx(doc.getroot(), parindex=parindex, start=start, until=stop):
            if isin:
                if basepos is None:
                    basepos = doc.getroot()[0].pos if curref == (1, "0") else eloc.parent.pos
                if not eloc.text:
                    continue
                spos = getattr(eloc, 'textpos', None)
                if spos is None:
                    continue
                self.replacetext(eloc, isin, lexemes, basepos, linelengths, spos, mrk)
            else:                       # tail of an element
                spos = getattr(eloc, 'tailpos', None)
                if spos is None:
                    continue
                self.replacetext(eloc, isin, lexemes, basepos, linelengths, spos, mrk)

    def replacetext(self, eloc, isin, lexemes, basepos, linelengths, spos, mrk):
        if basepos is None:
            return
        cpos = sum(linelengths[basepos.l:spos.l]) - basepos.c + spos.c + 1
        if isin:
            t = eloc.text
            parent = eloc
            laste = eloc[0] if len(eloc) else None
        else:
            t = eloc.tail
            parent = eloc.parent
            last = eloc
        cend = cpos + len(t)
        i = cpos
        outt = None
        for l in ((lex[0][0], lex[0][1], lex[1]) for lex in lexemes if lex[0][0] >= cpos and lex[0][0] < cend):
            if l[0] >= i:
                outt = t[i-cpos:l[0]-cpos]
            newe = parent.makeelement("char", {'style': mrk, 'gloss': l[2]})
            newe.text = t[l[0]-cpos:l[0]+l[1]-cpos]
            i = l[0] + l[1]
            if laste is None:
                parent.text = outt
                parent.insert(0, newe)
            else:
                laste.tail = outt
                laste.addnext(newe)
            laste = newe
            outt = None
        if i < cend and laste is not None:
            laste.tail = t[i-cpos:cend-cpos]
            

    def convertBk(self, bkid, doc, mrk="rb", keep_punct=True):
        intname = "Interlinear_{}".format(self.lang)
        intfile = os.path.join(self.prjdir, intname, "{}_{}.xml".format(intname, bkid))
        if not os.path.exists(intfile):
            return
        doc.addorncv()
        linelengths = doc.parser.lexer.lengths

        dones = set()
        notdones = set()
        skipping = None
        with open(intfile, "r", encoding="utf-8", errors="ignore") as inf:
            for (event, e) in et.iterparse(inf, ("start", "end")):
                if event == "start" and skipping is None:
                    if e.tag == "Range":
                        currange = (int(e.get('Index').strip()), int(e.get('Length').strip()))
                    elif e.tag == "Lexeme":
                        lid = e.get('Id', '')
                        gid = e.get('GlossId', '')
                        if lid.startswith('Word:'): # or lid.startswith('Phrase:'): # not sure if we want this yet.
                            wd = self.lexicon.get(lid, {}).get(gid, '')
                            lexemes.append((currange, str(wd)))
                    elif e.tag == "AfterText":
                        lexemes.append((currange, e.text))
                    if e.tag == "Punctuation" and not keep_punct:
                        skipping = e.tag
                elif event == "end" and (skipping is None or e.tag != skipping):
                    if e.tag == "string":
                        curref = self.makeref(e.text)
                        m = re.match(r"(\d+)[-,](\d+)", curref[1])
                        if m:
                            vrange = list(range(int(m.group(1)), int(m.group(2))+1))
                        else:
                            vrange = [int(curref[1]), 0]
                        lexemes = []
                    elif e.tag == "VerseData":
                        if e.get('Hash', "") != "":
                            self.replaceusx(doc, curref, lexemes, linelengths, mrk)
                            for v in vrange:
                                dones.add((curref[0], v))
                        else:
                            for v in vrange:
                                notdones.add((curref[0], v))
                elif event == "end" and e.tag == skipping:
                    skipping = None
        self.fails.extend([Reference(bkid, a[0], a[1]) for a in notdones if a not in dones])


