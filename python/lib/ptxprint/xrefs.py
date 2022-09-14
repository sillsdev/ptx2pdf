
from ptxprint.utils import cachedData, pycodedir
from ptxprint.reference import RefList, RefRange, Reference, RefSeparators, BaseBooks
from ptxprint.unicode.ducet import get_sortkey, SHIFTTRIM, tailored, get_ces
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

    def __init__(self, scriptsep, rtl=False, shortrefs=False):
        if scriptsep is not None:
            self.addsep = RefSeparators(**scriptsep)
            self.addsep.update(dict(books="; ", chaps=";\u200B", verses=",\u200B", bkc="\u00A0", mark=usfmmark, bksp="\u00A0"))
        if rtl:
            self.addsep.update(dict(books="\u061B ", chaps="\u061B\u200B"))
        logger.debug(self.addsep)
        self.rtl = rtl
        self.shortrefs = shortrefs


class XrefFileXrefs(BaseXrefs):
    def __init__(self, xrfile, filters, separators=None, listsize=0, rtl=False, shortrefs=False):
        super().__init__(separators, rtl, shortrefs=shortrefs)
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
                        "colnobook":    k.str(context=NoBook) if not self.shortrefs else str(k.verse),
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
    def __init__(self, xrfile, filters, localfile=None, ptsettings=None, separators=None,
                 context=None, shownums=True, rtl=False, shortrefs=False):
        super().__init__(separators, rtl=rtl, shortrefs=shortrefs)
        self.filters = filters
        self.context = context or BaseBooks
        self.shownums = shownums
        self.xmldat = cachedData(xrfile, self.readxml)

    def _unpackxml(self, xr):
        a = []
        for e in xr:
            st = e.get('strongs', None)
            if e.tag == "ref" and e.text is not None:
                r = RefList.fromStr(e.text, marks=("+", "\u203A"))
                a.append((st, e.get('style', None), r))
            elif e.tag == "refgroup":
                a.append((st, None, RefGroup(self._unpackxml(e))))
        return a

    def readxml(self, inf):
        doc = et.parse(inf)
        xmldat = {}
        for xr in doc.findall('.//xref'):
            k = RefList.fromStr(xr.get('ref'))[0]
            a = self._unpackxml(xr)
            if len(a):
                xmldat.setdefault(k.first.book, {})[k.first] = a
        return xmldat

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

    def _procnested(self, xr, baseref):
        a = []
        for e in xr:
            st = e[0]
            if st is not None and self.strongsfilter is not None and st not in self.strongsfilter:
                continue
            s = '\\xts|strong="{}" align="r"\\*\\nobreak\u2006'.format(st.lstrip("G").lstrip("H")) if st is not None and self.shownums else ""
            if isinstance(e[2], RefList):
                r = e[2]
                if self.filters is not None:
                    r.filterBooks(self.filters)
                r.sort()
                r.simplify()
                rs = r.str(context=self.context, addsep=self.addsep, level=2, this=baseref)
                if len(rs) and e[1] in ('backref', 'crossref'):
                    a.append(s + "\\+xti " + rs + "\\+xti*")
                elif len(rs):
                    a.append(s + rs)
            else:
                if len(e[2]) > 1 or (len(e[2]) and e[2][0][0] is not None):
                    a.append(s + "[" + self._procnested(e[2], baseref) + "]")
                elif len(e[2]):
                    a.append(s + self._procnested(e[2], baseref))
        return r"\space ".join(a)

    def process(self, bk, outpath, ranges, owner):
        xmldat = self.xmldat.get(bk, {})
        if len(xmldat):
            self._addranges(xmldat, ranges)
            with open(outpath + ".triggers", "w", encoding="utf-8") as outf:
                for k, v in xmldat.items():
                    res = self._procnested(v, k)
                    if len(res):
                        info = {
                            "book":         k.first.book,
                            "dotref":       k.str(context=NoBook, addsep=self.dotsep),
                            "colnobook":    k.str(context=NoBook) if not self.shortrefs else str(k.verse),
                            "refs":         res,
                            "brtl":         r"\beginR" if self.rtl else "",
                            "ertl":         r"\endR" if self.rtl else ""
                        }
                        outf.write(self.template.format(**info))


class StrongsXrefs(XMLXrefs):
    def __init__(self, xrfile, filters, localfile=None, ptsettings=None, separators=None,
                 context=None, shownums=True, rtl=False, shortrefs=False):
        super().__init__(xrfile, filters, localfile=localfile, ptsettings=ptsettings, separators=separators,
                 context=context, shownums=shownums, rtl=rtl, shortrefs=shortrefs)
        self.regexes = {}
        self.btmap = None
        self.revwds = None
        self.strongs = None
        self.lang = None
        if localfile is not None:
            self.loadlocal(localfile, addfilter=True)
            logger.debug("strongsfilter="+str(self.strongsfilter))
        else:
            self.strongsfilter = None

    def getstrongs(self, ref):
        return [x[0] for x in self.xmldat[ref.first.book].get(ref.first,[])]

    def loadinfo(self, lang):
        if lang is None or lang == 'und':
            lang = 'en'
        if self.btmap is not None and lang == self.lang:
            return
        strongsdoc = et.parse(os.path.join(os.path.dirname(__file__), "strongs_info.xml"))
        self.strongs = {}
        self.btmap = {}
        self.lang = lang
        for s in strongsdoc.findall(".//strong"):
            sref = s.get('ref')
            le = s.find('.//trans[@{{http://www.w3.org/XML/1998/namespace}}lang="{}"]'.format(self.lang))
            self.strongs[sref] = {k: s.get(k) for k in ('btid', 'lemma', 'head', 'translit')}
            self.btmap[s.get('btid')] = sref
            if le is not None:
                d = le.get('gloss', None)
                self.strongs[sref]['def'] = [d] if d is not None else None
                self.strongs[sref]['trans'] = le.text or ""
            else:
                self.strongs[sref]['def'] = None
                self.strongs[sref]['trans'] = ""

    def _readTermRenderings(self, localfile, strongs, revwds, btmap, key, addfilter=False):
        if addfilter:
            self.strongsfilter = set()
        localdoc = et.parse(localfile)
        for r in localdoc.findall(".//TermRendering"):
            rid = normalize('NFC', r.get("Id"))
            rend = r.findtext('Renderings')
            if rid not in btmap or rend is None or not len(rend):
                continue
            st = btmap[rid]
            if addfilter:
                self.strongsfilter.add(st)
            strongs[st][key] = rend.split("||")
            if revwds is not None:
                for w in strongs[st][key]:
                    revwds.setdefault(w.lower(), set()).add(st)

    def loadlocal(self, localfile, addfilter=False):
        self.loadinfo(self.lang)
        if self.revwds is not None:
            return
        self.revwds = {}
        self._readTermRenderings(localfile, self.strongs, self.revwds, self.btmap, 'local', addfilter=addfilter)

    def addregexes(self, st):
        wds = self.strongs.get(st,{}).get('local', [])
        reg = []
        for w in wds:
            w = re.sub(r"\(.*?\)", "", w).strip()
            if " ** " in w:
                continue
            r = ""
            if w.startswith("*"):
                w = w[1:]
            else:
                r = r"\b"
            if w.endswith("*"):
                r += w[:-1]
            else:
                r += w + r"\b"
            reg.append(r)
        res = "(" + "|".join(sorted(reg, key=lambda s:(-len(s), s))) + ")" if len(reg) else ""
        self.regexes[st] = res
        return res

    def generateStrongsIndex(self, bkid, cols, outfile, onlylocal, view):
        lang = view.get('fcb_strongsMajorLg')
        self.loadinfo(lang)
        fallback = view.get("fcb_strongsFallbackProj")
        if fallback is not None and fallback and fallback != "None":
            fallbackfile = os.path.join(view.settings_dir, fallback, "TermRenderings.xml")
            if os.path.exists(fallbackfile):
                self._readTermRenderings(fallbackfile, self.strongs, None, self.btmap, 'def')
        title = view.getvar("index_book_title", dest="strongs") or "Strong's Index"
        with open(outfile, "w", encoding="utf-8") as outf:
            outf.write("\\id {0} Strong's based terms index\n\\h {1}\n\\NoXrefNotes\n\\strong-s\\*\n\\mt1 {1}\n".format(bkid, title))
            outf.write("\\onebody\n" if cols == 1 else "\\twobody\n")
            rag = view.get("s_strongRag", 0)
            if rag is not None and int(rag) > 0:
                outf.write("\\zBottomRag {}\n".format(rag))
            wc = view.get("fcb_strongswildcards") 
            for a in ('Hebrew', 'Greek'):
                if (view.get("c_strongsHeb") and a == 'Hebrew') or (view.get("c_strongsGrk") and a == 'Greek'):
                    hdr = ("\n\\mt2 {}\n\\p\n".format(view.getvar("{}_section_title".format(a.lower()), dest="strongs") or a))
                    for k, v in sorted(self.strongs.items(), key=lambda x:int(x[0][1:])):
                        if not k.startswith(a[0]):
                            continue
                        d = v.get('local', v.get('def', None) if not onlylocal else None)
                        if d is None:
                            continue
                        d = ", ".join(s.strip() for s in d)
                        if view.get("c_strongsNoComments"):
                            d = re.sub(r"\(.*?\)", "", d)
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
            if len(self.revwds) and view.get("c_strongsNdx"):
                tailoring = self.context.getCollation()
                ducet = tailored(tailoring.text) if tailoring else None
                ldmlindices = self.context.getIndexList()
                indices = None if ldmlindices is None else sorted([c.lower() for c in ldmlindices], key=lambda s:(-len(s), s))
                lastinit = ""
                outf.write("\n\\mt2 {}\n".format(view.getvar("reverse_index_title", dest="strongs") or "Index"))
                for k, v in sorted(self.revwds.items(), key=lambda x:get_sortkey(x[0].replace("*",""), variable=SHIFTTRIM, ducet=ducet)):
                    for a, b in (("G", "Grk"), ("H", "Heb")):
                        if not view.get("c_strongs{}".format(b)):
                            v = set((s for s in v if not s.startswith(a)))
                    if indices is None:
                        ces = next(get_ces(k))
                        init = ces.split(b"\000")[0]
                    else:
                        for i in range(len(k)):
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

class Xrefs:
    def __init__(self, parent, filters, prjdir, xrfile, listsize, source, localfile, showstrongsnums, shortrefs):
        self.parent = parent
        self.prjdir = prjdir
        self.template = "\n\\AddTrigger {book}{dotref}\n\\x - \\xo {colnobook}\u00A0\\xt {refs}\\x*\n\\EndTrigger\n"
        if not parent.ptsettings.hasLocalBookNames:
            usfms = parent.printer.get_usfms()
            usfms.makeBookNames()
            parent.ptsettings.bookStrs = usfms.booknames.bookStrs
            parent.ptsettings.bookNames = usfms.booknames.bookNames
            parent.hasLocalBookNames = True
        rtl = parent['document/ifrtl'] == 'true'
        logger.debug(f"Source: {source}, {rtl=}")
        seps = parent.printer.getScriptSnippet().getrefseps(parent.printer)
        seps['verseonly'] = parent.printer.getvar('verseident') or "v"
        if source == "strongs":
            self.xrefs = getattr(parent.printer, 'strongs', None)
            if self.xrefs is None:
                self.xrefs = StrongsXrefs(os.path.join(pycodedir(), "strongs.xml"), filters,
                        localfile, separators=seps, context=parent.ptsettings,
                        shownums=showstrongsnums, rtl=rtl, shortrefs=shortrefs)
        elif xrfile is None:
            self.xrefs = StandardXrefs(os.path.join(pycodedir(), "cross_references.txt"),
                    filters, separators=seps, listsize=listsize, rtl=rtl, shortrefs=shortrefs)
        elif xrfile.endswith(".xml"):
            self.xrefs = XMLXrefs(xrfile, filters, separators=seps, context=parent.ptsettings, rtl=rtl, shortrefs=shortrefs)
        else:
            self.xrefs = XrefFileXrefs(xrfile, filters, separators=seps, rtl=rtl, shortrefs=shortrefs)
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
    ("c_strongsRenderings", r"\k {_defn}\k*;", "_defn"),
    ("c_strongsDefn", r"{trans};", "trans"),
    ("c_strongsKeyVref", r"\xt $a({head})\xt*", "head")
]
