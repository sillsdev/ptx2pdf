
from ptxprint.utils import cachedData, pycodedir, regex_localiser
from ptxprint.reference import RefList, RefRange, Reference, RefSeparators, BaseBooks
from ptxprint.unicode.ducet import get_sortkey, SHIFTTRIM, tailored, get_ces
from ptxprint.usfmutils import Usfm
from ptxprint import sfm
from unicodedata import normalize
from functools import reduce
import xml.etree.ElementTree as et
import re, os, gc
import logging

logger = logging.getLogger(__name__)

class WordForm:
    def __init__(self, stem, prefix, suffix):
        self.stem = stem
        self.prefices = prefix if prefix is None else set([prefix])
        self.suffices = suffix if suffix is None else set([suffix])

    def __str__(self):
        res = []
        if self.prefices is not None:
            res.append("("+"|".join(sorted(self.prefices, key=len))+")")
        res.append(self.stem)
        if self.suffices is not None:
            res.append("("+"|".join(sorted(self.suffices, key=len))+")")
        return "".join(res)

    def merge(self, stem, prefix, suffix):
        if self.stem != stem:
            return False
        matchpref = (prefix is None and self.prefices is None) or (prefix in self.prefices)
        matchsuff = (suffix is None and self.suffix is None) or (suffix in self.suffixes)
        if matchpref and not matchsuff:
            if suffix is not None:
                self.suffices.add(suffix)
                return True
        elif not matchpref and matchsuff:
            if prefix is not None:
                self.prefices.add(prefix)
                return True
        elif matchpref and matchsuff:
            return True
        return False

class WordForms:
    def __init__(self, stem):
        self.stem = stem
        self.forms = []

    def __str__(self):
        return "("+"|".join(self.forms + [self.stem])+ ")"

    def merge(self, stem, prefix, suffix):
        if prefix is None and suffix is None:
            return True
        for f in self.forms:
            if f.merge(stem, prefix, suffix):
                break
        else:
            self.forms.append(WordForm(stem, prefix, suffix))


class NoBook:
    @classmethod
    def getLocalBook(cls, s, level=0):
        return ""

def usfmmark(ref, txt):
    if ref.mark == "+":
        return r"\+it {}\+it*".format(txt)
    return (ref.mark or "") + txt

class BaseXrefs:
    template = "\\x - \\cat strongs\\cat*\\xo {colnobook}\u00A0\\xt {refs}\\x*"
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
    def __init__(self, xrfile, filters, separators=None, context=None, listsize=0, rtl=False, shortrefs=False):
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

    def _addranges(self, results, usfm):
        for ra in usfm.bridges.values():
            acc = []
            for r in ra.allrefs():
                if r in results:
                    acc = RefList(acc + results[r])
                    del results[r]
            if len(acc):
                results[ra] = acc
                logger.debug(f"{ra=} {acc=}")

    def process(self, bk, triggers, owner, usfm=None):
        results = {}
        for k, v in self.xrefdat.get(bk, {}).items():
            outl = v[0]
            if len(v) > 1 and self.xrlistsize > 1:
                outl = sum(v[0:self.xrlistsize], RefList())
            results[k] = outl
        if usfm is not None:
            self._addranges(results, usfm)
        if len(results):
            for k, v in sorted(results.items()):
                if self.filters is not None:
                    v.filterBooks(self.filters)
                v.simplify()
                if not len(v):
                    continue
                shortref = str(k.first.verse) if k.first.verse == k.last.verse else "{}-{}".format(k.first.verse, k.last.verse)
                info = {
                    "colnobook":    k.str(context=NoBook) if not self.shortrefs else shortref,
                    "refs":         v.str(owner.parent.ptsettings, addsep=self.addsep, level=2)
                }
                triggers[k.first] = triggers.get(k.first, "") + self.template.format(**info)
        return triggers


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
                 context=None, listsize=None, shownums=True, rtl=False, shortrefs=False):
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

    def simplify(self, groups):
        results = []
        for g in groups:
            if isinstance(g[2][0], (Reference, RefRange)):
                # demote top level ref under implicit refgroup
                self._updatedat(results, [(None, None, [g])], None)
            else:
                self._updatedat(results, [g], None)
        return results

    def readxml(self, inf):
        doc = et.parse(inf)
        xmldat = {}
        for xr in doc.findall('.//xref'):
            k = RefList.fromStr(xr.get('ref'))[0]
            a = self._unpackxml(xr)
            if len(a):
                xmldat.setdefault(k.first.book, {})[k.first] = self.simplify(a)
        return xmldat

    def _updatedat(self, newdat, dat, newr):
        if len(newdat) == 0:
            newdat.extend(dat)
            return
        newtemp = {v[0]:v for v in newdat}
        temp = {v[0]:v for v in dat}
        for k, v in temp.items():
            if k in newtemp:
                t = {x[0]: x for x in v[2]}
                for s in newtemp[k][2]:
                    if s[0] in t:
                        s[2].extend(t[s[0]][2])
                        del t[s[0]]
                for sk, sv in t.items():
                    newtemp[k][2].append(sv)
            else:
                newdat.append(v)
        if newr is not None:
            for r in newdat:
                try:
                    r[2].remove(newr)
                except ValueError:
                    continue

    def _addranges(self, dat, usfm, ref=None):
        for ra in usfm.bridges.values() if ref is None else [ref]:
            if ra in dat:
                continue
            newdat = []
            for r in ra.allrefs():
                if r in dat:
                    self._updatedat(newdat, dat[r], r)
                    del dat[r]
            if len(newdat):
                dat[ra] = sorted(newdat, key=lambda x:0 if x[0] is None else int(x[0].lstrip("GH")))

    def _procnested(self, xr, baseref):
        a = []
        for e in sorted(xr, key=lambda n:("", 0, []) if n is None or n[0] is None else (n[0][0], int(n[0][1:]), n)):
            st = e[0]
            if st is not None and self.strongsfilter is not None and st not in self.strongsfilter:
                continue
            s = '\\xts|strong="{}" align="r"\\*\\nobreak\u2006'.format(st.lstrip("GH")) if st is not None and self.shownums else ""
            if isinstance(e[2], RefList):
                r = e[2]
                if self.filters is not None:
                    r.filterBooks(self.filters)
                r.simplify()
                rs = r.str(context=self.context, addsep=self.addsep, level=2, this=baseref.last)
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

    def process(self, bk, triggers, owner, usfm=None):
        xmldat = self.xmldat.get(bk, {})
        if len(xmldat):
            #import pdb; pdb.set_trace()
            if usfm is not None:
                self._addranges(xmldat, usfm)
            for k, v in xmldat.items():
                res = self._procnested(v, k)
                shortref = str(k.first.verse) if k.first.verse == k.last.verse else "{}-{}".format(k.first.verse, k.last.verse)
                #kref = usfm.bridges.get(k, k) if usfm is not None else k
                if len(res):
                    info = {
                        "colnobook":    k.str(context=NoBook) if not self.shortrefs else shortref,
                        "refs":         res,
                        "brtl":         r"\beginR" if self.rtl else "",
                        "ertl":         r"\endR" if self.rtl else ""
                    }
                    triggers[k.first] = triggers.get(k.first, "") + self.template.format(**info)
        return triggers


components = [
    ("c_strongsSrcLg", r"\w{_lang} {lemma}\w{_lang}*", "lemma"),
    ("c_strongsTranslit", r"\wl {translit}\wl*", "translit"),
    ("c_strongsRenderings", r"\k {_defn}\k*;", "_defn"),
    ("c_strongsDefn", r"{trans};", "trans"),
    ("c_strongsKeyVref", r"\xt $a({head})\xt*", "head")
]

class StrongsXrefs(XMLXrefs):
    def __init__(self, xrfile, filters, localfile=None, ptsettings=None, separators=None,
                 context=None, shownums=True, rtl=False, shortrefs=False, wanal=None):
        super().__init__(xrfile, filters, localfile=localfile, ptsettings=ptsettings, separators=separators,
                 context=context, shownums=shownums, rtl=rtl, shortrefs=shortrefs)
        self.regexes = {}
        self.btmap = None
        self.revwds = None
        self.strongs = None
        self.lang = None
        self.wfi = {}
        if localfile is not None or wanal is not None:
            self.loadlocal(localfile, addfilter=True, wordanalysisfile=wanal)
            logger.debug("strongsfilter="+str(self.strongsfilter))
        else:
            self.strongsfilter = None

    def simplify(self, groups):
        return groups

    def getstrongs(self, ref):
        if ref.first != ref.last and ref not in self.xmldat[ref.first.book] and ref.last.verse < 200:
            self._addranges(self.xmldat[ref.first.book], None, ref=ref)
        return [x[0] for x in self.xmldat[ref.first.book].get(ref,[])]

    def loadinfo(self, lang):
        if lang is None:
            lang = 'und'
        if self.btmap is not None and len(self.btmap) and lang == self.lang:
            return
        strongsdoc = et.parse(os.path.join(os.path.dirname(__file__), "xrefs", "strongs_info.xml"))
        self.lang = lang
        if self.strongs is None:
            self.strongs = {}
            self.btmap = {}
        for s in strongsdoc.findall(".//strong"):
            sref = s.get('ref')
            le = s.find('.//trans[@{{http://www.w3.org/XML/1998/namespace}}lang="{}"]'.format(self.lang))
            self.strongs.setdefault(sref, {}).update({k: s.get(k) for k in ('btid', 'lemma', 'head', 'translit')})
            self.btmap[s.get('btid')] = sref
            if le is not None:
                d = le.get('gloss', None)
                self.strongs[sref]['def'] = [d] if d is not None else None
                self.strongs[sref]['trans'] = le.text or ""
            else:
                self.strongs[sref]['def'] = None
                self.strongs[sref]['trans'] = ""

    def _readWordAnalysis(self, fname):
        self.wfi = {}
        doc = et.parse(fname)
        for e in doc.findall(".//Analysis"):
            d = {}
            for l in e.findall("Lexeme"):
                (t, v) = l.text.split(":")
                d.setdefault(t, []).append(v)
            stem = "".join(d['Stem']) or None
            prefix = "".join(d['Prefix']) or None
            suffix = "".join(d['Suffix']) or None
            if stem is not None:
                if stem not in self.wfi:
                    self.wfi[stem] = WordForms(stem)
                self.wfi[stem].merge(stem, suffix, prefix)

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

    def loadlocal(self, localfile, addfilter=False, wordanalysisfile=None):
        self.loadinfo(self.lang)
        if self.revwds is not None:
            return
        self.revwds = {}
        if localfile is not None:
            self._readTermRenderings(localfile, self.strongs, self.revwds, self.btmap, 'local', addfilter=addfilter)
        if wordanalysisfile is not None:
            self._readWordAnalysis(wordanalysisfile)

    def addregexes(self, st):
        if self.strongs is None:
            return ""
        wds = self.strongs.get(st,{}).get('local', [])
        reg = []
        for w in wds:
            for i, b in enumerate(re.sub(r"\(.*?\)", "", w).split()):
                t = b.strip()
                p = ""
                r = ""
                s = ""
                if t == "**":
                    reg.append(r"(?:\s+\w+)*")
                    continue
                elif t == "*":
                    reg.append(r"(?:\s+\w+)?")
                    continue
                if not t.startswith("*"):
                    r = r"\bb"
                else:
                    t = t[1:]
                if not t.endswith("*"):
                    p = r"\ba"
                else:
                    t = t[:-1]
                if "/" in t:            # allows two words in either order
                    (a, b) = t.split("/")
                    t = a
                else:
                    a = None
                if i == 0 and t in self.wfi:  # test for word forms
                    s = str(self.wfi[t])
                else:
                    s = t.replace("*", r"\w*")
                if a is not None:
                    a = s
                    s += r"\s+" + b
                    b = s + "r\s+" + a
                    reg.append(r + b + p)
                reg.append(r + s + p)
        res = "(" + "|".join(sorted(reg, key=lambda s:(-len(s), s))) + ")" if len(reg) else ""
        res = regex_localiser(res)
        logger.debug(f"strongs regexes {st} = {res}")
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
                            if not onlylocal:
                                d = []
                            else:
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
            if self.revwds is not None and len(self.revwds) and view.get("c_strongsNdx"):
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


xreftypes = {
    ".xre": StandardXrefs,
    ".xml": XMLXrefs,
    ".xrf": XrefFileXrefs
}
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
        if source.startswith("strongs"):
            self.xrefs = getattr(parent.printer, 'strongs', None)
            if self.xrefs is None:
                self.xrefs = StrongsXrefs(os.path.join(pycodedir(), 'xrefs', "strongs.xml"), filters,
                        localfile, separators=seps, context=parent.ptsettings,
                        shownums=showstrongsnums, rtl=rtl, shortrefs=shortrefs)
        else:
            testf = os.path.join(pycodedir(), 'xrefs', source) if xrfile is None else xrfile
            if os.path.exists(testf):
                t = xreftypes.get(os.path.splitext(testf)[1], None)
                fp = testf
            else:
                for a, at in xreftypes.items():
                    fp = testf + a
                    if os.path.exists(fp):
                        t = at
                        break
                else:
                    t = None
            self.xrefs = t(fp, filters, separators=seps, context=parent.ptsettings,
                        listsize=listsize, rtl=rtl, shortrefs=shortrefs) if t is not None else None
        gc.collect()

    def process(self, bk, triggers, usfm=None):
        if usfm is not None:
            usfm.addorncv()
        if self.xrefs is not None:
            return self.xrefs.process(bk, triggers, self, usfm=usfm)
        return triggers

