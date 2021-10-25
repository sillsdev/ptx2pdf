
from ptxprint.utils import cachedData, pycodedir
from ptxprint.reference import RefList, RefRange, Reference, RefSeparators
import xml.etree.ElementTree as et
import re, os

class Xrefs:
    class NoBook:
        @classmethod
        def getLocalBook(cls, s, level=0):
            return ""

    @staticmethod
    def usfmmark(ref, txt):
        if ref.mark == "+":
            return r"\+it {}\+it*".format(txt)
        return txt

    def __init__(self, parent, filters, prjdir, xrfile, listsize):
        self.parent = parent
        self.filters = filters
        self.prjdir = prjdir
        self.xrfile = xrfile
        self.xrefdat = None
        self.xrlistsize = listsize
        self.addsep = RefSeparators(books="; ", chaps=";\u200B", verses=",\u200B", bkcv="\u2000", mark=self.usfmmark)
        self.dotsep = RefSeparators(cv=".", onechap=True)
        self.template = "\n\\AddTrigger {book}{dotref}\n\\x - \\xo {colnobook} \\xt {refs}\\x*\n\\EndTrigger\n"
        if self.xrfile is None:
            def procxref(inf):
                results = {}
                for l in inf.readlines():
                    d = l.split("|")
                    v = [RefList.fromStr(s) for s in d]
                    results[v[0][0]] = v[1:]
                return results
            self.xrefdat = cachedData(os.path.join(pycodedir(), "cross_references.txt"), procxref)
        elif self.xrfile.endswith(".xml"):
            self.readxml(self.xrfile)
        else:
            self.xrefdat = {}
            with open(xrfile) as inf:
                for l in inf.readlines():
                    if '=' in l:
                        (k, v) = l.split("=", maxsplit=1)
                        if k.strip() == "attribution":
                            self.xrefcopyright = v.strip()
                    v = RefList()
                    for d in re.sub(r"[{}]", "", l).split():
                        v.extend(RefList.fromStr(d.replace(".", " "), marks="+"))
                    k = v.pop(0)
                    self.xrefdat[k] = [v]

    def _getVerseRanges(self, sfm, bk):
        class Result(list):
            def __init__(self):
                super().__init__(self)
                self.chap = 0

        def process(a, e):
            if isinstance(e, (str, Text)):
                return a
            if e.name == "c":
                a.chap = int(e.args[0])
            elif e.name == "v" and "-" in e.args[0]:
                m = re.match(r"^(\d+)-(\d+)", e.args[0])
                if m is not None:
                    first = int(m.group(1))
                    last = int(m.group(2))
                    a.append(RefRange(Reference(bk, a.chap, first), Reference(bk, a.chap, last)))
            for c in e:
                process(a, c)
            return a
        return reduce(process, sfm, Result())

    def _iterref(self, ra, allrefs):
        curr = ra.first.copy()
        while curr <= ra.last:
            if curr in allrefs:
                yield curr
                curr.verse += 1
            else:
                curr.chap += 1
                curr.verse = 1

    def _addranges(self, results, ranges):
        for ra in ranges:
            acc = RefList()
            for r in self._iterref(ra, results):
                acc.extend(results[r])
                del results[r]
            if len(acc):
                results[ra] = acc

    def process(self, bk, outpath):
        if self.xrefdat is None:
            return self.processxml(bk, outpath)

        results = {}
        for k, v in self.xrefdat.items():
            if k.first.book != bk:
                continue
            outl = v[0]
            if len(v) > 1 and self.listsize > 1:
                outl = sum(v[0:self.listsize], RefList())
            results[k] = outl
        fname = self.parent.printer.getBookFilename(bk)
        if fname is None:
            return
        infpath = os.path.join(self.prjdir, fname)
        with open(infpath) as inf:
            try:
                sfm = Usfm(inf, self.sheets)
            except:
                sfm = None
            if sfm is not None:
                ranges = self._getVerseRanges(sfm.doc, bk)
                self._addranges(results, ranges)
        with open(outpath + ".triggers", "w", encoding="utf-8") as outf:
            for k, v in sorted(results.items()):
                if self.filters is not None:
                    v.filterBooks(self.filters)
                v.sort()
                v.simplify()
                if not len(v):
                    continue
                info = {
                    "book":         k.first.book,
                    "dotref":       k.str(context=self.NoBook, addsep=self.dotsep),
                    "colnobook":    k.str(context=self.NoBook),
                    "refs":         v.str(self.parent.ptsettings, addsep=self.addsep)
                }
                outf.write(self.template.format(**info))

    def _unpackxml(self, xr):
        a = []
        for e in xr:
            st = e.get('strongs', None)
            s = '\\xts|strong="{}" align="r"\\*'.format(st) if st is not None else ""
            if e.tag == "ref":
                r = RefList.fromStr(e.text)
                if self.filters is not None:
                    r.filterBooks(self.filters)
                r.sort()
                r.simplify()
                rs = r.str(self.parent.ptsettings, addsep=self.addsep)
                if len(rs) and e.get('style', '') in ('backref', 'crossref'):
                    a.append(s + "\\+xti " + rs + "\\+xti*")
                elif len(rs):
                    a.append(s + rs)
            elif e.tag == "refgroup":
                a.append(s + "[" + " ".join(self._unpackxml(e)) + "]")
        return a

    def readxml(self, xrfile):
        doc = et.parse(xrfile)
        self.xmldat = {}
        for xr in doc.findall('.//xref'):
            k = RefList.fromStr(xr.get('ref'))[0]
            a = self._unpackxml(xr)
            if len(a):
                self.xmldat[k.first] = " ".join(self._unpackxml(xr))

    def processxml(self, bk, outpath):
        with open(outpath + ".triggers", "w", encoding="utf-8") as outf:
            for k, v in self.xmldat.items():
                if k.first.book != bk:
                    continue
                info = {
                    "book":         k.first.book,
                    "dotref":       k.str(context=self.NoBook, addsep=self.dotsep),
                    "colnobook":    k.str(context=self.NoBook),
                    "refs":         v
                }
                outf.write(self.template.format(**info))
            
