import re
from ptxprint.usxutils import Usfm
from ptxprint.reference import RefList, RefRange
from usfmtc.usxmodel import iterusx

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

class Module:

    #localise_re = re.compile(r"\$([asl]?)\(\s*(\S+\s+\d+(?::[^)\s]+)?\s*(?:-\s*\d+(?::[^)*\s]+)*)*)\)")
    localise_re = re.compile(r"\$([asl]?)\((.*?)\)")
    localcodes = {'a': 0, 's': 1, 'l': 2}

    def __init__(self, fname, usfms, model, usfm=None, text=None):
        self.fname = fname
        self.usfms = usfms
        self.model = model
        self.usfms.makeBookNames()
        self.sheets = self.usfms.sheets.copy()
        modinfo = { 'mrktype': 'otherpara', 'texttype': 'Other', 'endmarker': None, 'styletype': 'Paragraph'}
        for k in ('inc', 'vrs', 'ref', 'refnp', 'rep', 'mod'):
            self.sheets[k].update(modinfo)
        if usfm is not None:
            self.doc = usfm
        else:
            if text is None and self.fname is not None:
                with open(self.fname, encoding="utf-8") as inf:
                    text = inf.read()
            self.doc = Usfm.readfile(text if text is not None else fname, sheet=self.sheets)

    def getBookRefs(self):
        books = set()
        for e in iterusx(self.doc.getroot()):
            if e.head is not None:
                continue
            s = e.parent.get("style", None)
            if s == "ref" or "refnp":       # \ref is not a <ref> it has been reassigned to <para>
                for r in RefList.fromStr(e.parent.text, context=self.usfms.booknames):
                    books.add(r.first.book)
        return books

    def localref(self, m):
        rl = RefList.fromStr(m.group(2), context=self.usfms.booknames)
        loctype = m.group(1) or "a"
        tocindex = self.localcodes.get(loctype.lower(), 0)
        return rl.str(context=self.usfms.booknames, level=tocindex)

    def testexclude(self, einfo):
        return einfo[1] is not None and (self.model is None or (self.model[einfo[1]] in (None, "")) ^ (not einfo[2]))

    def parse(self):
        self.removes = set((sum((e[0] for e in exclusionmap.values() if self.testexclude(e)), [])))
        skipme = 0
        for eloc in iterusx(self.doc.getroot()):
            if skipme > 0:
                skipme -= 1
                continue
            if eloc.head is not None:
                if eloc.head.tail is not None:
                    eloc.head.tail = self.localise_re.sub(self.localref, eloc.head.tail)
                continue
            e = eloc.parent
            if e.text is not None:
                e.text = self.localise_re.sub(self.localref, e.text)
            if e.tag == "para":
                s = e.get("style", None)
            elif e.tag == "ref":
                s = "ref"
            else:
                continue
            if s == "ref" or s == "refnp":
                res = []
                reps = []
                nc = e.getnext_sibling()
                if nc is not None and nc.get("style", "") == "rep":
                    m = re.match(r"^\s*(.*?)\s*=>\s*(.*?)\s*$", nc.text, re.M)
                    if m:
                        reps.append((None,
                                re.compile(r"\b"+m.group(1).replace("...","[^\n\r]+")+"(\\b|(?=\\s)|$)"),
                                m.group(2)))
                    e.parent.remove(nc)
                    skipme += 1
                for r in RefList.fromStr(e.text, context=self.usfms.booknames):
                    if r.first.verse == 1:
                        if not isinstance(r, RefRange):
                            r = RefRange(r.first, r.first.copy())
                            r.last.verse = 1
                        r.first.verse = 0
                    p = self.get_passage(r, removes=self.removes, strippara= s=="refnp")
                    if not len(p):
                        continue
                    (curri, currp) = e._getindex()
                    for pe in reversed(p):
                        pe.parent = currp
                        currp.insert(curri, pe)
                    currp.remove(e)
                    skipme += 1
                    if len(reps):
                        self.doc.transform_text(*reps, parts=p)
            elif s == 'inc':
                for c in e.text.split():
                    einfo = exclusionmap.get(c, ([], None, False))
                    if c == "-":
                        self.removes = set(sum((x[0] for x in exclusionmap.values()), []))
                    elif not self.testexclude(einfo):
                        self.removes.difference_update(einfo[0])
            elif s == 'mod':
                dirname = os.path.dirname(self.fname)
                infpath = os.path.join(dirname, e.text.strip())
                mod = Module(infpath, self.usfms, self.model)
                mod.parse()
                curri, currp = e._getindex()
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
