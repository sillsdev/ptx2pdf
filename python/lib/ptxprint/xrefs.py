
from ptxprint.utils import cachedData, pycodedir
from ptxprint.reference import RefList, RefRange, Reference, RefSeparators
from ptxprint.unicode.ducet import get_sortkey, SHIFTTRIM, tailored
from unicodedata import normalize
import xml.etree.ElementTree as et
import re, os, gc
import logging

logger = logging.getLogger(__name__)

class Xrefs:
    class NoBook:
        @classmethod
        def getLocalBook(cls, s, level=0):
            return ""

    @staticmethod
    def usfmmark(ref, txt):
        if ref.mark == "+":
            return r"\+it {}\+it*".format(txt)
        return (ref.mark or "") + txt

    def __init__(self, parent, filters, prjdir, xrfile, listsize, source, localfile):
        self.parent = parent
        self.filters = filters
        self.prjdir = prjdir
        self.xrfile = xrfile
        self.xrefdat = None
        self.xrlistsize = listsize
        self.addsep = RefSeparators(books="; ", chaps=";\u200A", verses=",\u200A", bkc="\u2000", mark=self.usfmmark, bksp="\u00A0")
        self.dotsep = RefSeparators(cv=".", onechap=True)
        self.template = "\n\\AddTrigger {book}{dotref}\n\\x - \\xo {colnobook}\u00A0\\xt {refs}\\x*\n\\EndTrigger\n"
        logger.debug(f"Source: {source}")
        if source == "strongs":
            self.readxml(os.path.join(os.path.dirname(__file__), "strongs.xml"), localfile)
        elif self.xrfile is None:
            def procxref(inf):
                results = {}
                for l in inf.readlines():
                    d = l.split("|")
                    v = [RefList.fromStr(s) for s in d]
                    results[v[0][0]] = v[1:]
                return results
            self.xrefdat = cachedData(os.path.join(pycodedir(), "cross_references.txt"), procxref)
        elif self.xrfile.endswith(".xml"):
            self.readxml(self.xrfile, None)
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
        gc.collect()

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
            if len(v) > 1 and self.xrlistsize > 1:
                outl = sum(v[0:self.xrlistsize], RefList())
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

    def _unpackxml(self, xr, stfilter):
        a = []
        for e in xr:
            st = e.get('strongs', None)
            if st is not None:
                if stfilter is not None and st not in stfilter:
                    continue
                if st[0] in "GH":
                    st = st[1:]
            s = '\\xts|strong="{}" align="r"\\*'.format(st) if st is not None else ""
            if e.tag == "ref" and e.text is not None:
                r = RefList.fromStr(e.text, marks=("+", "\u203A"))
                if self.filters is not None:
                    r.filterBooks(self.filters)
                r.sort()
                r.simplify()
                rs = r.str(context=self.parent.ptsettings, addsep=self.addsep)
                if len(rs) and e.get('style', '') in ('backref', 'crossref'):
                    a.append(s + "\\+xti " + rs + "\\+xti*")
                elif len(rs):
                    a.append(s + rs)
            elif e.tag == "refgroup":
                a.append(s + "[" + " ".join(self._unpackxml(e, stfilter)) + "]")
        return a

    def readxml(self, xrfile, localfile):
        # import pdb; pdb.set_trace()
        if localfile is not None:
            sinfodoc = et.parse(os.path.join(os.path.dirname(__file__), "strongs_info.xml"))
            btmap = {}
            for s in sinfodoc.findall('.//strong'):
                btmap[s.get('btid')] = s.get('ref')
            termsdoc = et.parse(localfile)
            strongsfilter = set()
            for r in termsdoc.findall('.//TermRendering'):
                rend = r.findtext('Renderings')
                rid = normalize('NFC', r.get('Id'))
                if rend is not None and len(rend) and rid in btmap:
                    strongsfilter.add(btmap[rid])
            logger.debug("strongsfilter="+str(strongsfilter))
        else:
            strongsfilter = None
        doc = et.parse(xrfile)
        self.xmldat = {}
        for xr in doc.findall('.//xref'):
            k = RefList.fromStr(xr.get('ref'))[0]
            a = self._unpackxml(xr, strongsfilter)
            if len(a):
                self.xmldat[k.first] = " ".join(self._unpackxml(xr, strongsfilter))

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

def generateStrongsIndex(bkid, cols, outfile, localfile, onlylocal, ptsettings, view):
    strongsdoc = et.parse(os.path.join(os.path.dirname(__file__), "strongs_info.xml"))
    strongs = {}
    btmap = {}
    revwds = {}
    for s in strongsdoc.findall(".//strong"):
        sref = s.get('ref')
        strongs[sref] = {k: s.get(k) for k in ('btid', 'lemma', 'head', 'translit')}
        strongs[sref]['def'] = s.text
        btmap[s.get('btid')] = sref
    if localfile is not None:
        localdoc = et.parse(localfile)
        for r in localdoc.findall(".//TermRendering"):
            rid = normalize('NFC', r.get("Id"))
            rend = r.findtext('Renderings')
            if rid not in btmap or rend is None or not len(rend):
                continue
            sref = btmap[rid]
            strongs[sref]['local'] = ", ".join(rend.split("||"))
            for w in rend.split("||"):
                s = re.sub(r"\(.*?\)", "", w).strip()
                revwds.setdefault(s.lower(), set()).add(sref)
    title = view.getvar("strongs_title") or "Strongs"
    with open(outfile, "w", encoding="utf-8") as outf:
        outf.write("\\id {0} Strongs based terms index\n\\h {1}\n\\NoXrefNotes\n\\strong-s\\*\n\\mt1 {1}\n".format(bkid, title))
        outf.write("\\onebody\n" if cols == 1 else "\\twobody\n")
        for a in ('Hebrew', 'Greek'):
            hdr = ("\n\\mt2 {}\n\\p\n".format(view.getvar("strongs_{}".format(a.lower())) or a))
            for k, v in sorted(strongs.items(), key=lambda x:int(x[0][1:])):
                if not k.startswith(a[0]):
                    continue
                d = v.get('local', v.get('def', None) if not onlylocal else None)
                if d is None:
                    continue
                if hdr:
                    outf.write(hdr)
                    hdr = ""
                outf.write(r"\{_marker} \bd {_key}\bd* \w{_lang} {lemma}\w{_lang}* \wl {translit}\wl* {_defn} \xt $a({head})\xt*".format(
                    _key=k[1:], _lang=a[0].lower(), _marker="li", _defn=d, **v) + "\n")
        if len(revwds):
            tailoring = ptsettings.getCollation()
            ducet = tailored(tailoring.text) if tailoring else None
            ldmlindices = ptsettings.getIndexList()
            indices = None if ldmlindices is None else sorted([c.lower() for c in ldmlindices], key=lambda s:(-len(s), s))
            lastinit = ""
            outf.write("\n\\mt2 {}\n".format(view.getvar("strongs_index") or "Index"))
            for k, v in sorted(revwds.items(), key=lambda x:get_sortkey(x[0], variable=SHIFTTRIM, ducet=ducet)):
                for i in range(len(k)):
                    if indices is None:
                        if k[i] not in "\u0E40\u0E41\u0E42\u0E43\u0E44":
                            init = k[i]
                            break
                    else:
                        for s in indices:
                            if k[i:].startswith(s):
                                init = s
                                break
                        else:
                            continue
                        break
                if init != lastinit:
                    outf.write("\n\\p\n")
                    lastinit = init
                outf.write("{}({}) ".format(k, ", ".join(sorted(v, key=lambda s:(int(s[1:]), s[0]))))) 
        outf.write("\\strong-e\\*\n")
