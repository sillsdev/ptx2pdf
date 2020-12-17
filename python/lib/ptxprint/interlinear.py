from xml.etree import ElementTree as et
from ptxprint.usfmutils import Usfm, Sheets
from ptxprint import sfm
from hashlib import md5
import re, os

_refre = re.compile("^(\d?\D+?)\s+(\d+):(\S+)\s*$")

class Interlinear:
    def __init__(self, lang, prjdir):
        self.lang = lang
        self.prjdir = prjdir
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
                        self.lexicon.setdefault(currlex, {})[currsense] = e.text

    def makeref(self, s):
        m = _refre.match(s)
        if m:
            return (int(m[2]), m[3])
        else:
            raise SyntaxError("Bad Reference {}".format(s))

    def replaceindoc(self, doc, curref, lexemes, linelengths, mrk="+wit"):
        lexemes.sort()
        #allstr = []
        adj = 0
        for e in doc.iterVerse(*curref):
            #allstr.append(str(e))
            if isinstance(e, sfm.Element):
                if e.name == "v":   # starting col and line
                    startl = e.pos.line - 1
                    startc = e.pos.col - 1
                adj += getattr(e, 'adjust', 0)
                continue
            if e.parent.name == "fig":
                continue
            thisadj = adj - getattr(e.parent, 'adjust', 0)
            lstart = sum(linelengths[startl:e.pos.line-1]) + e.pos.col-1 + startc + thisadj
            lend = lstart + len(e)
            #print(f"{e.pos.chapter}:{e.pos.verse} ({e.pos.col}, {e.pos.line}), ({startc}, {startl}), {lstart}, {lend} {linelengths[startl:e.pos.line-1]}")
            i = 0
            res = []
            for l in (lex for lex in lexemes if lex[0][0] >= lstart and lex[0][0] < lend):
                if l[0][0]-lstart >= i:
                    res.append(e[i:l[0][0]-lstart])
                res.append(r"\{0} {1}|{2}\{0}*".format(mrk, e[l[0][0]-lstart:l[0][0]+l[0][1]-lstart], l[1]))
                i = l[0][0] + l[0][1] - lstart
            if i < len(e):
                res.append(e[i:])
            e.data = str("".join(str(s) for s in res))
        #hashstr =  md5()
        #hashstr.update("".join(allstr)[:-1].encode("utf-16LE"))
        #print(curref, allstr, hashstr.hexdigest())

    def convertBk(self, bkid, doc, linelengths, mrk="+rb"):
        intname = "Interlinear_{}".format(self.lang)
        intfile = os.path.join(self.prjdir, intname, "{}_{}.xml".format(intname, bkid))
        if not os.path.exists(intfile):
            return
        doc.addorncv()

        for (event, e) in et.iterparse(intfile, ("start", "end")):
            if event == "start":
                if e.tag == "Range":
                    currange = (int(e.get('Index').strip()), int(e.get('Length').strip()))
                elif e.tag == "Lexeme":
                    lid = e.get('Id', '')
                    gid = e.get('GlossId', '')
                    if lid.startswith('Word:'):
                        lexemes.append((currange, str(self.lexicon.get(lid, {}).get(gid, ''))))
            elif event == "end":
                if e.tag == "string":
                    curref = self.makeref(e.text)
                    lexemes = []
                elif e.tag == "VerseData" and e.get('Hash', "") != "":
                    self.replaceindoc(doc, curref, lexemes, linelengths, mrk=mrk)

