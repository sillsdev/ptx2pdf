from xml.etree import ElementTree as et
from ptxprint.usfmutils import Usfm, Sheets
from ptxprint import sfm
from hashlib import md5
from ptxprint.reference import Reference
import re, os

_refre = re.compile("^(\d?\D+?)\s+(\d+):(\S+)\s*$")

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
        m = _refre.match(s)
        if m:
            return (int(m[2]), m[3])
        else:
            raise SyntaxError("Bad Reference {}".format(s))

    def replaceindoc(self, doc, curref, lexemes, linelengths, mrk="+wit"):
        lexemes.sort()
        adj = 0
        vend = (0, 0)
        startl = None
        for e in doc.iterVerse(*curref):
            if isinstance(e, sfm.Element):
                if e.pos.line == vend[0] and e.pos.col == vend[1]:
                    e.adjust = 1    # Handle where there is no space after verse number in the text but PT presumes it is there
                if startl is None:   # starting col and line
                    startl = e.pos.line - 1
                    startc = e.pos.col - 1
                    vend = (e.pos.line, e.pos.col + 3 + len(e.args[0]))
                adj += getattr(e, 'adjust', 0)
                continue
            if e.parent is not None and e.parent.name == "fig":
                continue
            thisadj = adj - getattr(e.parent, 'adjust', 0)
            ispara = e.parent is None or e.parent.meta['StyleType'] != 'Character'
            thismrk = mrk[1:] if ispara else mrk
            lstart = sum(linelengths[startl:e.pos.line-1]) + e.pos.col-1 + startc
            lend = lstart + len(e)
            i = 0
            res = []
            for l in ((lex[0][0]-adj, lex[0][1], lex[1]) for lex in lexemes if lex[0][0] >= lstart and lex[0][0] < lend):
                if l[0]-lstart >= i:
                    res.append(e[i:l[0]-lstart])
                res.append(r"\{0} {1}|{2}\{0}*".format(thismrk, e[l[0]-lstart:l[0]+l[1]-lstart], l[2]))
                i = l[0] + l[1] - lstart
            if i < len(e):
                res.append(e[i:])
            e.data = str("".join(str(s) for s in res))

    def convertBk(self, bkid, doc, linelengths, mrk="+rb"):
        intname = "Interlinear_{}".format(self.lang)
        intfile = os.path.join(self.prjdir, intname, "{}_{}.xml".format(intname, bkid))
        if not os.path.exists(intfile):
            return
        doc.addorncv()

        dones = set()
        notdones = set()
        with open(intfile, "r", encoding="utf-8", errors="ignore") as inf:
            for (event, e) in et.iterparse(inf, ("start", "end")):
                if event == "start":
                    if e.tag == "Range":
                        currange = (int(e.get('Index').strip()), int(e.get('Length').strip()))
                    elif e.tag == "Lexeme":
                        lid = e.get('Id', '')
                        gid = e.get('GlossId', '')
                        if lid.startswith('Word:'):
                            wd = self.lexicon.get(lid, {}).get(gid, '')
                            lexemes.append((currange, str(wd)))
                elif event == "end":
                    if e.tag == "string":
                        curref = self.makeref(e.text)
                        m = re.match(r"(\d+)-(\d+)", curref[1])
                        if m:
                            vrange = list(range(int(m.group(1)), int(m.group(2))+1))
                        else:
                            vrange = [int(curref[1]), 0]
                        lexemes = []
                    elif e.tag == "VerseData":
                        if e.get('Hash', "") != "":
                            self.replaceindoc(doc, curref, lexemes, linelengths, mrk=mrk)
                            for v in vrange:
                                dones.add((curref[0], v))
                        else:
                            for v in vrange:
                                notdones.add((curref[0], v))
        self.fails.extend([Reference(bkid, a[0], a[1]) for a in notdones if a not in dones])

