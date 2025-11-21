import re, traceback
from ptxprint.usxutils import Usfm
from ptxprint.utils import runChanges
from usfmtc.reference import RefList, RefRange
from usfmtc.usxmodel import iterusx
import logging

logger = logging.getLogger(__name__)

def read_module(inf, sheets):
    lines = inf.readlines()
    if not re.match(r"\uFEFF?\\id\s", lines[0]):
        lines.insert(0, "\\id MOD Module\n")
    return Usfm(lines, sheets)

#    e: ([mkrs], modelmap entry, invert_test, element tag)
#    If modelmap entry is not empty test the marker, using invert_test
exclusionmap = {
#    'v': (None, "document/ifshowversenums", False, 'verse'),    # opposite use of %
    'x': (('x',), "notes/includexrefs", True, 'note'),
    'f': (('f',), "notes/includefootnotes", True, 'note'), 
    's': (('s', 's1', 's2', 'r'), "document/sectionheads", True, 'para'),
#    'c': (None, 'document/ifshowchapternums', True, 'chapter'),
    'p': (None, None, False, 'figure'),
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

    def __init__(self, fname, usfms, model, usfm=None, text=None, changes=[]):
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
            if len(changes):
                text = runChanges(changes, None, text, self.model._changeError)
            self.doc = Usfm.readfile(text if text is not None else fname, grammar=grammar, informat="usfm")

    def outUsfm(self, fname, **kw):
        self.doc.asUsfm(file=fname, **kw)

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
        loctype = m.group(1) or self.refmode
        text = m.group(2).strip()
        if (m := re.match(r"^[a-z]+[.:](.+)$", text)) is not None:
            ptsettings = self.model.printer._getPtSettings()
            return ptsettings.get_ldml(loctype, text) if ptsettings is not None else m.group(1).strip()
        else:
            rl = getreflist(text, booknames=self.usfms.booknames)
            tocindex = self.localcodes.get(loctype.lower(), 0)
            return rl.str(env=self.model.printer.getRefEnv(), level=tocindex)

    def testexclude(self, einfo):
        return einfo[1] is not None and (self.model is None or (self.model[einfo[1]] in (None, "")) ^ (not einfo[2]))

    def parse(self, piclist=None):
        logger.log(5, self.doc.xml.outUsx(None))
        self.doc.xml.book = "MOD"
        count = 0
        self.removes = set((e for e in exclusionmap.values() if self.testexclude(e)))
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
            elif eloc.tag == "figure":
                # breakpoint()
                src = eloc.get("src", eloc.get("file", None))
                if piclist is not None and src is not None:
                    anchor = piclist.getAnchor(src, "MOD")
                if anchor is None:
                    if piclist is not None:
                        anchor = piclist.emptyAnchor("MOD")
                    else:
                        anchor = f"{count:03d}"
                        count += 1
                    p = piclist.add_from_fig("MOD", anchor, eloc)
                    p["src"] = src
                    p.set_position(2 if self.model.printer.get("c_doublecolumn") else 1)
                eloc.tag = "ms"
                eloc.attrib = {"style": "zfiga", "id": anchor}
                eloc.text = None
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
                values = [v for v in eloc.text.split() if v.strip()]
                # breakpoint()
                for c in values:
                    einfo = exclusionmap.get(c, (tuple(), None, False, ""))
                    if c == "-":
                        self.removes = set(exclusionmap.values())
                    elif not self.testexclude(einfo):
                        self.removes.discard(einfo)
                print(f"{self.removes=}")
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
        res = book.xml.getrefs(ref, titles=False, headers=not any(x[0] is not None and 's' in x[0] for x in removes),
                                    chapters= not any('chapter' in x[3] for x in removes))
        if True:        # this should be a filter test
            firstp = res.getroot()[0]
            firstp.attrib.pop('vid', None)
        for e, isin in res.iterusx():
            if not isin:
                continue
            for r in removes:
                if e.tag == r[3] and (r[0] is None or e.get('style', '') in r[0]):
                    if e.tail:
                        i = e.parent.index(e)
                        if i == 0:
                            e.parent.text = (e.parent.text or "") + e.tail
                        else:
                            e.parent[i-1].tail = (e.parent[i-1].tail or "") + e.tail
                    e.parent.remove(e)
                    break
        return res.getroot()
