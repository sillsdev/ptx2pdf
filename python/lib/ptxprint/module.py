import re, traceback
from ptxprint.usxutils import Usfm
from usfmtc.reference import RefList, RefRange
from usfmtc.usxmodel import iterusx
import logging

logger = logging.getLogger(__name__)

def read_module(inf, sheets):
    lines = inf.readlines()
    if not re.match(r"\uFEFF?\\id\s", lines[0]):
        lines.insert(0, "\\id MOD Module\n")
    return Usfm(lines, sheets)

#    e: ([mkrs], modelmap entry, invert_test)
exclusionmap = {
    'v': (['v'], "document/ifshowversenums", False),
    'x': (['x'], None, False),
    'f': (['f'], "notes/includefootnotes", True),
    's': (['s', 's1', 's2', 'r'], "document/sectionheads", False),
    'c': (['c'], 'document/ifshowchapternums', True),
    'p': (['fig'], None, False)
}

_abbrevmodes = {
    "Abbreviation": "a",
    "ShortNames": "s",
    "LongName": "l",
}

def getreflist(r, **kw):
    try:
        return RefList(r, **kw)
    except SyntaxError as e:
        s = "".join(traceback.format_stack())
        logger.warn(s)
    return RefList([])

class Module:

    #localise_re = re.compile(r"\$([asl]?)\(\s*(\S+\s+\d+(?::[^)\s]+)?\s*(?:-\s*\d+(?::[^)*\s]+)*)*)\)")
    localise_re = re.compile(r"\$([asl]?)\((.*?)\)")
    localcodes = {'a': 0, 's': 1, 'l': 2}

    def __init__(self, fname, usfms, model, usfm=None, text=None):
        self.fname = fname
        self.usfms = usfms
        self.model = model
        if self.model is not None:
            ptsettings = self.model.printer._getPtSettings()
            if ptsettings is None:
                self.refmode = "a"
            else:
                self.refmode = _abbrevmodes.get(ptsettings.get("BookSourceForMarkerR", "Abbreviation"), "a")
        else:
            self.refmode = None
        self.usfms.makeBookNames()
        grammar = self.usfms.grammar.copy()
        for k in ('inc', 'vrs', 'ref', 'refnp', 'rep', 'mod'):
            grammar.marker_categories[k] = "otherpara"
        if usfm is not None:
            self.doc = usfm
        else:
            if text is None and self.fname is not None:
                with open(self.fname, encoding="utf-8") as inf:
                    text = inf.read()
            self.doc = Usfm.readfile(text if text is not None else fname, grammar=grammar, informat="usfm")

    def getBookRefs(self):
        books = set()
        for e, isin in iterusx(self.doc.getroot()):
            if not isin:
                continue
            s = e.get("style", None)
            if s in ("ref", "refnp"):       # \ref is not a <ref> it has been reassigned to <para>
                if e.text:
                    for r in getreflist(e.text, booknames=self.usfms.booknames):
                        books.add(r.first.book)
        return books

    def localref(self, m):
        rl = getreflist(m.group(2), booknames=self.usfms.booknames)
        loctype = m.group(1) or self.refmode
        tocindex = self.localcodes.get(loctype.lower(), 0)
        return rl.str(env=self.usfms.booknames, level=tocindex)

    def testexclude(self, einfo):
        return einfo[1] is not None and (self.model is None or (self.model[einfo[1]] in (None, "")) ^ (not einfo[2]))

    def parse(self):
        self.removes = set((sum((e[0] for e in exclusionmap.values() if self.testexclude(e)), [])))
        skipme = 0
        for eloc, isin in iterusx(self.doc.getroot()):
            if skipme > 0:
                skipme -= 1
                continue
            if not isin:
                if eloc.tail is not None:
                    eloc.tail = self.localise_re.sub(self.localref, eloc.tail)
                continue
            if eloc.text is not None:
                eloc.text = self.localise_re.sub(self.localref, eloc.text)
            if eloc.tag == "para":
                s = eloc.get("style", None)
            elif eloc.tag == "ref":
                s = "ref"
            else:
                continue
            if s == "ref" or s == "refnp":
                res = []
                reps = []
                nc = eloc.getnext_sibling()
                if nc is not None and nc.get("style", "") == "rep":
                    m = re.match(r"^\s*(.*?)\s*=>\s*(.*?)\s*$", nc.text, re.M)
                    if m:
                        reps.append((None,
                                re.compile(r"\b"+m.group(1).replace("...","[^\n\r]+")+"(\\b|(?=\\s)|$)"),
                                m.group(2)))
                    eloc.parent.remove(nc)
                    skipme += 1
                try:
                    refs = RefList(eloc.text.strip(), booknames=self.usfms.booknames)
                except SyntaxError as e:
                    raise SyntaxError(f"{e} at {s} at line {eloc.pos.l} char {eloc.pos.c}")
                for r in refs:
                    if r.first.verse == 1:
                        if not isinstance(r, RefRange):
                            r = RefRange(r.first, r.first.copy())
                            r.last.verse = 1
                        r.first.verse = 0
                    p = self.get_passage(r, removes=self.removes, strippara= s=="refnp")
                    if not len(p):
                        continue
                    (curri, currp) = eloc._getindex()
                    for pe in reversed(p):
                        pe.parent = currp
                        currp.insert(curri, pe)
                    currp.remove(eloc)
                    skipme += 1
                    if len(reps):
                        self.doc.transform_text(*reps, parts=p)
            elif s == 'inc':
                for c in eloc.text.split():
                    einfo = exclusionmap.get(c, ([], None, False))
                    if c == "-":
                        self.removes = set(sum((x[0] for x in exclusionmap.values()), []))
                    elif not self.testexclude(einfo):
                        self.removes.difference_update(einfo[0])
            elif s == 'mod':
                dirname = os.path.dirname(self.fname)
                infpath = os.path.join(dirname, eloc.text.strip())
                mod = Module(infpath, self.usfms, self.model)
                mod.parse()
                curri, currp = eloc._getindex()
                for p in mod.doc.getroot():
                    p.parent = currp
                    currp.insert(curri, p)

    def get_passage(self, ref, removes={}, strippara=False):
        if ref.first.book is None:
            return []
        try:
            book = self.usfms.get(ref.first.book.upper())
        except SyntaxError:
            book = None
        if book is None:
            return []
        res = book.subdoc(ref, removes=removes, strippara=strippara, addzsetref=False).getroot()
        #zsetref = book.make_zsetref(ref.first, self.usfms.booknames.getLocalBook(ref.first.book, 1), res[0].parent, res[0].pos)
        if not len(res):
            return res
        zsetref = book.make_zsetref(ref.first, None, res[0].parent, res[0].pos)
        return [zsetref] + list(res)
