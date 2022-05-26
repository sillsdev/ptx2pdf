
from ptxprint.utils import cachedData, pycodedir
from ptxprint.reference import RefList, RefRange, Reference, RefSeparators, BaseBooks
from ptxprint.unicode.ducet import get_sortkey, SHIFTTRIM, tailored
from ptxprint.usfmutils import Usfm
from unicodedata import normalize
import xml.etree.ElementTree as et
import re, os, gc
import logging

logger = logging.getLogger(__name__)

class NoBook:
    @classmethod
    def getLocalBook(cls, s, level=0):
        return ""

def usfmmark(ref, txt):
    if ref.mark == "+":
        return r"\+it {}\+it*".format(txt)
    return (ref.mark or "") + txt

class BaseXrefs:
    template = "\n\\AddTrigger {book}{dotref}\n\\x - \\cat strongs\\cat*\\xo {colnobook}\u00A0\\xt {refs}\\x*\n\\EndTrigger\n"
    addsep = RefSeparators(books="; ", chaps=";\u200A", verses=",\u200A", bkc="\u2000", mark=usfmmark, bksp="\u00A0")
    dotsep = RefSeparators(cv=".", onechap=True)

    def __init__(self, scriptsep):
        if scriptsep is not None:
            self.addsep = RefSeparators(**scriptsep)
            self.addsep.update(dict(books="; ", chaps=";\u200A", verses=",\u200A", bkc="\u2000", mark=usfmmark, bksp="\u00A0"))


class XrefFileXrefs(BaseXrefs):
    def __init__(self, xrfile, filters, separators=None, listsize=0):
        super().__init__(separators)
        self.filters = filters
        self.xrlistsize = listsize
        self.xrefdat = cachedData(xrfile, self.readdat)

    def readdat(self, inf):
        xrefdat = {}
        for l in inf.readlines():
            if '=' in l:
                (k, v) = l.split("=", maxsplit=1)
                if k.strip() == "attribution":
                    self.xrefcopyright = v.strip()
            v = RefList()
            for d in re.sub(r"[{}]", "", l).split():
                v.extend(RefList.fromStr(d.replace(".", " "), marks="+"))
            k = v.pop(0)
            xrefdat.setdefault(k.first.book, {})[k] = [v]
        return xrefdat

    def _addranges(self, results, ranges):
        for ra in ranges:
            acc = RefList()
            for r in ra.allrefs():
                if r in results:
                    acc.extend(results[r])
                    del results[r]
            if len(acc):
                results[ra] = acc

    def process(self, bk, outpath, ranges, owner):
        results = {}
        for k, v in self.xrefdat.get(bk, {}).items():
            outl = v[0]
            if len(v) > 1 and self.xrlistsize > 1:
                outl = sum(v[0:self.xrlistsize], RefList())
            results[k] = outl
        self._addranges(results, ranges)
        if len(results):
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
                        "dotref":       k.str(context=NoBook, addsep=self.dotsep),
                        "colnobook":    k.str(context=NoBook),
                        "refs":         v.str(owner.parent.ptsettings, addsep=self.addsep, level=2)
                    }
                    outf.write(self.template.format(**info))


class StandardXrefs(XrefFileXrefs):
    def readdat(self, inf):
        results = {}
        for l in inf.readlines():
            d = l.split("|")
            v = [RefList.fromStr(s) for s in d]
            results.setdefault(v[0][0].first.book, {})[v[0][0]] = v[1:]
        return results


class RefGroup(list):
    pass

class XMLXrefs(BaseXrefs):
    def __init__(self, xrfile, filters, localfile=None, ptsettings=None, separators=None, context=None, shownums=True):
        super().__init__(separators)
        self.filters = filters
        self.context = context or BaseBooks
        self.shownums = shownums
        if localfile is not None:
            sinfodoc = et.parse(os.path.join(os.path.dirname(__file__), "strongs_info.xml"))
            btmap = {}
            for s in sinfodoc.findall('.//strong'):
                btmap[s.get('btid')] = s.get('ref')
            with open(localfile, encoding="utf8") as inf:
                termsdoc = et.parse(inf)
            self.strongsfilter = set()
            for r in termsdoc.findall('.//TermRendering'):
                rend = r.findtext('Renderings')
                rid = normalize('NFC', r.get('Id'))
                if rend is not None and len(rend) and rid in btmap:
                    self.strongsfilter.add(btmap[rid])
            logger.debug("strongsfilter="+str(self.strongsfilter))
        else:
            self.strongsfilter = None
        self.xmldat = cachedData(xrfile, self.readxml)

    def readxml(self, inf):
        doc = et.parse(inf)
        xmldat = {}
        for xr in doc.findall('.//xref'):
            k = RefList.fromStr(xr.get('ref'))[0]
            a = self._unpackxml(xr)
            if len(a):
                xmldat.setdefault(k.first.book, {})[k.first] = a
        return xmldat

    def _unpackxml(self, xr):
        a = []
        for e in xr:
            st = e.get('strongs', None)
            if st is not None:
                if st[0] in "GH":
                    st = st[1:]
            if e.tag == "ref" and e.text is not None:
                r = RefList.fromStr(e.text, marks=("+", "\u203A"))
                a.append((st, e.get('style', None), r))
            elif e.tag == "refgroup":
                a.append((st, None, RefGroup(self._unpackxml(e))))
        return a

    def _procnested(self, xr):
        a = []
        for e in xr:
            st = e[0]
            if st is not None and self.strongsfilter is not None and st not in self.strongsfilter:
                continue
            s = '\\xts|strong="{}" align="r"\\*\\nobreak\u2006'.format(st) if st is not None and self.shownums else ""
            if isinstance(e[2], RefList):
                r = e[2]
                if self.filters is not None:
                    r.filterBooks(self.filters)
                r.sort()
                r.simplify()
                rs = r.str(context=self.context, addsep=self.addsep, level=2)
                if len(rs) and e[1] in ('backref', 'crossref'):
                    a.append(s + "\\+xti " + rs + "\\+xti*")
                elif len(rs):
                    a.append(s + rs)
            else:
                if len(e[2]):
                    a.append(s + "[\\nobreak " + self._procnested(e[2]) + "]")
        return " ".join(a)

    def _updatedat(newdat, dat):
        for k, v in dat.items():
            if k not in newdat:
                newdat[k] = v
                continue
            nd = {}
            for n in newdat[k]:
                nd.setdefault(n[1], []).append(n)
            for n in v:
                if n[1] in nd:
                    for nn in nd[n[1]]:
                        if nn[1] == n[1]:   # same styles
                            if isinstance(nn[2], RefList):
                                if isinstance(n[2], RefList):
                                    nn[2].extend(n[2])
                                else:
                                    nn[2] = RefGroup(nn[2]) + n[2]
                            elif isinstance(n[2], RefList):
                                nn[2].append(n[2])
                            else:
                                nn[2].extend(n[2])
                            break
                    else:
                        nd[d[1]].append(n)
                else:
                    nd[n[1]] = n

    def _addranges(self, dat, ranges):
        for ra in ranges:
            newdat = {}
            for r in ra.allrefs():
                if r in dat:
                    self._updatedat(newdat, dat[r])
                    del dat[r]
            if len(newdat):
                dat[ra] = newdat

    def process(self, bk, outpath, ranges, owner):
        xmldat = self.xmldat.get(bk, {})
        if len(xmldat):
            self._addranges(xmldat, ranges)
            with open(outpath + ".triggers", "w", encoding="utf-8") as outf:
                for k, v in xmldat.items():
                    res = self._procnested(v)
                    if len(res):
                        info = {
                            "book":         k.first.book,
                            "dotref":       k.str(context=NoBook, addsep=self.dotsep),
                            "colnobook":    k.str(context=NoBook),
                            "refs":         res
                        }
                        outf.write(self.template.format(**info))


class Xrefs:
    def __init__(self, parent, filters, prjdir, xrfile, listsize, source, localfile, showstrongsnums):
        self.parent = parent
        self.prjdir = prjdir
        self.template = "\n\\AddTrigger {book}{dotref}\n\\x - \\xo {colnobook}\u00A0\\xt {refs}\\x*\n\\EndTrigger\n"
        if not parent.ptsettings.hasLocalBookNames:
            usfms = parent.printer.get_usfms()
            usfms.makeBookNames()
            parent.ptsettings.bookStrs = usfms.booknames.bookStrs
            parent.ptsettings.bookNames = usfms.booknames.bookNames
            parent.hasLocalBookNames = True
        logger.debug(f"Source: {source}")
        seps = parent.printer.getScriptSnippet().getrefseps(parent.printer)
        if source == "strongs":
            self.xrefs = XMLXrefs(os.path.join(pycodedir(), "strongs.xml"), filters, localfile, separators=seps, context=parent.ptsettings, shownums=showstrongsnums)
        elif xrfile is None:
            self.xrefs = StandardXrefs(os.path.join(pycodedir(), "cross_references.txt"), filters, separators=seps, listsize=listsize)
        elif xrfile.endswith(".xml"):
            self.xrefs = XMLXrefs(xrfile, filters, separators=seps, context=parent.ptsettings)
        else:
            self.xrefs = XrefFileXrefs(xrfile, filters, separators=seps)
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

    def process(self, bk, outpath):
        fname = self.parent.printer.getBookFilename(bk)
        if fname is None:
            return
        infpath = os.path.join(self.prjdir, fname)
        with open(infpath) as inf:
            try:
                sfm = Usfm(inf, self.sheets)
                ranges = self._getVerseRanges(sfm.doc, bk)
            except:
                ranges = []
        self.xrefs.process(bk, outpath, ranges, self)



components = [
    ("c_strongsSrcLg", r"\w{_lang} {lemma}\w{_lang}*", "lemma"),
    ("c_strongsTranslit", r"\wl {translit}\wl*", "translit"),
    ("c_strongsRenderings", r"{_defn};", "_defn"),
    ("c_strongsDefn", r"{trans};", "trans"),
    ("c_strongsKeyVref", r"\xt $a({head})\xt*", "head")
]
def _readTermRenderings(localfile, strongs, revwds, btmap, key):
    localdoc = et.parse(localfile)
    for r in localdoc.findall(".//TermRendering"):
        rid = normalize('NFC', r.get("Id"))
        rend = r.findtext('Renderings')
        if rid not in btmap or rend is None or not len(rend):
            continue
        sref = btmap[rid]
        strongs[sref][key] = ", ".join(rend.split("||"))
        if revwds is not None:
            for w in rend.split("||"):
                s = re.sub(r"\(.*?\)", "", w).strip()
                revwds.setdefault(s.lower(), set()).add(sref)

def generateStrongsIndex(bkid, cols, outfile, localfile, onlylocal, ptsettings, view):
    strongsdoc = et.parse(os.path.join(os.path.dirname(__file__), "strongs_info.xml"))
    strongs = {}
    btmap = {}
    revwds = {}
    lang = view.get('fcb_strongsMajorLg')
    if lang is None or lang == 'und':
        lang = 'en'
    #import pdb; pdb.set_trace()
    for s in strongsdoc.findall(".//strong"):
        sref = s.get('ref')
        le = s.find('.//trans[@{{http://www.w3.org/XML/1998/namespace}}lang="{}"]'.format(lang))
        strongs[sref] = {k: s.get(k) for k in ('btid', 'lemma', 'head', 'translit')}
        btmap[s.get('btid')] = sref
        if le is not None:
            strongs[sref]['def'] = le.get('gloss', None)
            strongs[sref]['trans'] = le.text or ""
        else:
            strongs[sref]['def'] = None
            strongs[sref]['trans'] = ""
            
    fallback = view.get("fcb_strongsFallbackProj")
    if fallback is not None and fallback and fallback != "None":
        fallbackfile = os.path.join(view.settings_dir, fallback, "TermRenderings.xml")
        if os.path.exists(fallbackfile):
            _readTermRenderings(fallbackfile, strongs, None, btmap, 'def')
    if localfile is not None:
        _readTermRenderings(localfile, strongs, revwds, btmap, 'local')
    title = view.getvar("index_book_title", dest="strongs") or "Strong's Index"
    with open(outfile, "w", encoding="utf-8") as outf:
        outf.write("\\id {0} Strong's based terms index\n\\h {1}\n\\NoXrefNotes\n\\strong-s\\*\n\\mt1 {1}\n".format(bkid, title))
        outf.write("\\onebody\n" if cols == 1 else "\\twobody\n")
        rag = view.get("s_strongRag", 0)
        if rag is not None and int(rag) > 0:
            outf.write("\\zBottomRag {}\n".format(rag))
        for a in ('Hebrew', 'Greek'):
            if (view.get("c_strongsHeb") and a == 'Hebrew') or (view.get("c_strongsGrk") and a == 'Greek'):
                hdr = ("\n\\mt2 {}\n\\p\n".format(view.getvar("{}_section_title".format(a.lower()), dest="strongs") or a))
                for k, v in sorted(strongs.items(), key=lambda x:int(x[0][1:])):
                    if not k.startswith(a[0]):
                        continue
                    d = v.get('local', v.get('def', None) if not onlylocal else None)
                    if d is None:
                        continue
                    if view.get("c_strongsNoComments"):
                        d = re.sub(r"\(.*?\)", "", d)
                    wc = view.get("fcb_strongswildcards") 
                    if wc in ("remove", "hyphen"):
                        d = d.replace("*", "" if wc == "remove" else "-")
                    if hdr:
                        outf.write(hdr)
                        hdr = ""
                    v["_defn"] = d
                    bits = [r"\{_marker} \bd {_key}\bd*"] + [cv for ck, cv, ct in components if view.get(ck) and v.get(ct, "")]
                    if bits[-1][-1] == ";":
                        bits[-1] = bits[-1][:-1]
                    outf.write(" ".join(bits).format(_key=k[1:], _lang=a[0].lower(), _marker="li", **v) + "\n")
        if len(revwds) and view.get("c_strongsNdx"):
            tailoring = ptsettings.getCollation()
            ducet = tailored(tailoring.text) if tailoring else None
            ldmlindices = ptsettings.getIndexList()
            indices = None if ldmlindices is None else sorted([c.lower() for c in ldmlindices], key=lambda s:(-len(s), s))
            lastinit = ""
            outf.write("\n\\mt2 {}\n".format(view.getvar("reverse_index_title", dest="strongs") or "Index"))
            for k, v in sorted(revwds.items(), key=lambda x:get_sortkey(x[0].replace("*",""), variable=SHIFTTRIM, ducet=ducet)):
                for i in range(len(k)):
                    if indices is None:
                        if k[i] not in "*\u0E40\u0E41\u0E42\u0E43\u0E44":
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
                    outf.write("\n\\m\n")
                    lastinit = init
                outf.write("{}\u200A({}) ".format(k, ", ".join(sorted(v, key=lambda s:(int(s[1:]), s[0]))))) 
        outf.write("\n\\singlecolumn\n\\strong-e\\*\n")
