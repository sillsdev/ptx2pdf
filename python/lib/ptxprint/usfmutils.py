from ptxprint.sfm import usfm, style, sreduce
from ptxprint import sfm
from ptxprint.reference import RefList, RefRange, Reference, BookNames
import re, os, traceback, warnings
from collections import namedtuple
from itertools import groupby
from functools import reduce
from copy import deepcopy
import regex

def isScriptureText(e):
    if 'nonvernacular' in e.meta.get('TextProperties', []):
        return False
    if e.meta.get('TextType', "").lower() == "versetext":
        return True
    if e.meta.get('TextType', "").lower() == "other" and e.name.startswith("i"):
        return True
    if e.name in ("h", "id", "mt", "toc1", "toc2", "toc3"):
        return False
    return True

takslc_cats = {'Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Sm', 'Sc', 'Sk', 'So',
               'Nd', 'Nl', 'No', 
               'Pd', 'Pc', 'Pe', 'Ps', 'Pi', 'Pf', 'Po'}
space_cats = { 'Zs', 'Zl', 'Zp', 'Cf' }

class _Reference(sfm.Position):
    def __new__(cls, pos, ref):
        p = super().__new__(cls, *pos[:2])
        p.ref = RefList.fromStr("{} {}:{}".format(*ref))[0]
        return p

    def __str__(self):
        return f"{self.book} {self.chapter}:{self.verse} line {self.line},{self.col}"


class Sheets(dict):

    default = usfm._load_cached_stylesheet('usfm_sb.sty')

    def __init__(self, init=[], base=None):
        if base != "":
            self.update(deepcopy(base) if base is not None else deepcopy(self.default))
        if init is None or not len(init):
            return
        for s in init:
            if os.path.exists(s):
                self.append(s, nodefaults=base == "")
        usfm.resolve_milestones(self)

    def append(self, sf, nodefaults=False):
        if os.path.exists(sf):
            with open(sf, encoding="utf-8", errors="ignore") as s:
                sp = style.parse(s, fields = style.Marker({})) if nodefaults else style.parse(s)
                self.update_sheet(sp)

    def update_sheet(self, d):
        style.update_sheet(self, d, field_replace=True)

    def copy(self):
        return Sheets(base=self)

    def add_parparent(self, marker):
        for k, v in self.items():
            if 'p' in v['OccursUnder']:
                v['OccursUnder'].add(marker)

    def remove_parparent(self, marker):
        for k, v in self.items():
            v['OccursUnder'].discard(marker)


class UsfmCollection:
    def __init__(self, bkmapper, basedir, sheets):
        self.bkmapper = bkmapper
        self.basedir = basedir
        self.sheets = sheets
        self.books = {}
        self.tocs = []
        self.booknames = None

    def get(self, bk):
        if bk not in self.books:
            bkfile = self.bkmapper(bk)
            if bkfile is None:
                return None
            bkfile = os.path.join(self.basedir, bkfile)
            if not os.path.exists(bkfile):
                return None
            with open(bkfile, encoding="utf-8") as inf:
                self.books[bk] = Usfm(inf, self.sheets)
        return self.books[bk]

    def makeBookNames(self):
        if self.booknames is not None:
            return
        self.booknames = BookNames()
        bknamesp = os.path.join(self.basedir, "BookNames.xml")
        if os.path.exists(bknamesp):
           self.booknames.readBookNames(bknamesp)
        else:
            tocre = re.compile(r"^\\toc(\d)\s+(.*)\s*$")
            for bk in list(self.booknames.bookStrs.keys()):
                tocs = [None]*3
                bkfile = self.bkmapper(bk)
                if bkfile is None:
                    continue
                bkfile = os.path.join(self.basedir, bkfile)
                if not os.path.exists(bkfile):
                    continue
                with open(bkfile, encoding="utf-8") as inf:
                    for i in range(20):
                        l = inf.readline()
                        m = tocre.match(l)
                        if m:
                            r = int(m.group(1))
                            if r < len(tocs):
                                tocs[r] = m.group(2)
                tocs = reversed([x or tocs[i-1:i] for i,x in enumerate(tocs)])
                self.booknames.addBookName(bk, *tocs)

class Usfm:
    def __init__(self, iterable, sheets):
        tag_escapes = r"[^0-9A-Za-z]"
        self.doc = None
        self.sheets = sheets
        with warnings.catch_warnings(record=True) as self.warnings:
            self.doc = list(usfm.parser(iterable, stylesheet=sheets,
                                canonicalise_footnotes=False,
                                error_level=sfm.ErrorLevel.Unrecoverable,
                                tag_escapes=tag_escapes))
        # self.warnings is a list of Exception type errors use print(w.message)
        self.cvaddorned = False
        self.tocs = []

    def __str__(self):
        return sfm.generate(self.doc)

    def addorncv(self):
        if self.cvaddorned:
            return
        ispara = sfm.text_properties('paragraph')
        self.chapters = []
        ref = ["", "0", "0"]
        pending = []

        def isHeading(e):
            if not isinstance(e, sfm.Element):
                return False
            if getattr(e, "meta", {}).get('StyleType', '').lower() != 'paragraph':
                return False
            if getattr(e, "meta", {}).get('TextType', '').lower() == 'section':
                return True
            return False

        def _g(_, e):
            if isinstance(e, sfm.Element):
                if e.name == 'id':
                    ref[0] = str(e[0]).split()[0]
                elif e.name == 'c':
                    ref[1] = e.args[0]
                    c = int(ref[1])
                    if c == len(self.chapters):
                        self.chapters.append(e)
                    else:
                        if c > len(self.chapters):
                            self.chapters += [None] * (c - len(self.chapters) + 1)
                        self.chapters[c] = e
                    ref[2] = "0"
                elif e.name == 'v':
                    ref[2] = e.args[0]
                    for t in pending:
                        t.pos = _Reference(t.pos, ref)
                    pending.clear()
                elif ref[2] != "0":
                    if isHeading(e) or len(pending):
                        pending.append(e)
                e.pos = _Reference(e.pos, ref)
                reduce(_g, e, None)
            else:
                if len(pending):
                    pending.append(e)
                else:
                    e.pos = _Reference(e.pos, ref)
        reduce(_g, self.doc, None)
        self.cvaddorned = True

    def readnames(self):
        if len(self.tocs) > 0:
            return
        for c in self.doc[0]:       # children of id
            if not isinstance(c, sfm.Element) or c.name != "h":
                continue
            for e in c:
                if not isinstance(e, sfm.Element):
                    continue
                m = re.match(r"^toc(\d)", e.name)
                if m:
                    ind = int(m.group(1))
                    if ind > len(self.tocs):
                        self.tocs.extend([""] * (ind - len(self.tocs) + 1))
                    self.tocs[ind-1] = e[0].strip()

    def getwords(self, init=None, constrain=None):
        ''' Counts words found in the document. If constrain then is a set or
            list that contains words to count, ignoring all others. Returns
            a dict of words: counts. '''
        wre = re.compile(r"(\w+)")
        if init is None:
            init = {}
        def addwords(s, a):
            if s is None:
                return a
            for w in wre.split(str(s))[1::2]:
                if constrain is None or w in constrain:
                    a[w] = a.get(w, 0) + 1
            return a
        def nullelement(e, a, c):
            return a
        words = sreduce(nullelement, addwords, self.doc, init)
        return words

    def subdoc(self, refrange, removes={}, strippara=False):
        ''' Creates a document consisting of only the text covered by the reference
            ranges. ref is a tuple in the form:
                (fromc, fromv, toc, tov)
            The list must include overlapping ranges'''
        self.addorncv()
        ispara = sfm.text_properties('paragraph')
        chaps = self.chapters[refrange.first.chap:refrange.last.chap+1]
        def pred(e):
            if isinstance(e.pos, _Reference) and e.pos.ref in refrange:
                if strippara and isinstance(e, sfm.Element) and ispara(e):
                    return False
                return True
            return False

        def _g(a, e):
            if isinstance(e, sfm.Text):
                if pred(e):
                    a.append(sfm.Text(e, e.pos, a or None))
                return a
            if e.name in removes:
                return a
            e_ = sfm.Element(e.name, e.pos, e.args, parent=a or None, meta=e.meta)
            reduce(_g, e, e_)
            if pred(e):
                a.append(e_)
            elif len(e_):
                a.extend(e_[:])
            return a
        return reduce(_g, chaps, [])

    def iter(self, e):
        def iterfn(el):
            yield el
            if isinstance(el, sfm.Element):
                for c in el:
                    for c1 in iterfn(c):
                        yield c1
        return iterfn(e)

    def iiterel(self, i, e, endfn=None):
        def iterfn(il, el):
            if isinstance(el, sfm.Element):
                yield (il, el)
                for il, c in list(enumerate(el)):
                    yield from iterfn(il, c)
                if endfn is not None:
                    endfn(el)
        return iterfn(i, e)

    def iterVerse(self, chap, verse):
        start = self.chapters[chap]
        it = self.iter(start)
        for e in it:
            if not isinstance(e, sfm.Element):
                continue
            if e.name == "c" and int(e.args[0]) != chap:
                # print(e.name, e.args, len(e))
                return
            elif verse == "0" or (e.name == "v" and e.args[0] == verse):
                yield e
                break
        else:
            return
        for e in it:
            if isinstance(e, sfm.Element) and (e.name == "c" or e.name == "v"):
                break
            yield e

    def _insertVerse(self, job, parent, offset, e):
        job.parent = parent
        if offset != 0:
            last = parent[offset - (1 if offset > 0 else 0)]
            if isinstance(last, sfm.Text) and last.data[-1] in " \n":
                newstr = last.data.rstrip()
                lc = last.data[len(newstr):]
                last.data = newstr
            else:
                lc = None
        else:
            lc = None
        if offset >= 0:
            parent.insert(offset, job)
            offset += 1
        else:
            parent.append(job)
        if lc is not None:
            t = sfm.Text(lc, pos=e.pos, parent=parent)
            if offset > 0:
                parent.insert(offset, t)
                offset += 1
            else:
                parent.append(t)
        return offset

    def versesToEnd(self):
        it = self.iiterel(0, self.doc[0])
        currjob = None
        lastpara = None
        thispara = None
        for i, e in it:
            if not isinstance(e, sfm.Element):
                continue
            etype = e.meta.get('texttype', '').lower()
            style = e.meta.get('styletype', '').lower()
            if style == 'paragraph' and etype == 'versetext':
                # if e.parent is not None and e.parent.name == 'p':
                    # print(e)
                thispara = e
                offset = 0
            elif style == 'paragraph':
                if currjob is not None:
                    self._insertVerse(currjob, lastpara, -1, e)
                    currjob = None
                thispara = None
                offset = 0
            if e.name == 'v':
                if currjob is not None:
                    if thispara is not None and i > 1:
                        offset = self._insertVerse(currjob, thispara, i+offset, e) - i
                    else:
                        self._insertVerse(currjob, lastpara, -1, e)
                currjob = sfm.Element('vp', e.pos, parent=e.parent, meta=self.sheets['vp'])
                currjob.append(sfm.Text(e.args[0], pos=e.pos, parent=currjob))
            if thispara is not None and thispara is not e:
                lastpara = thispara
        if currjob is not None:
            lastpara.append(currjob)
            lastpara.append(sfm.Text("\n", parent=lastpara))

    def normalise(self):
        ''' Normalise USFM in place '''
        ispara = sfm.text_properties("paragraph")
        def ensurenl(i, e):
            ''' Ensure element ends with a newline, if not already present.
                Passed index in parent and element. '''
            if isinstance(e, sfm.Element):
                if len(e):
                    ensurenl(len(e)-1, e[-1])
                else:
                    e.append(sfm.Text("\n", e.pos, e.parent))
                    return True
            elif not e.endswith("\n"):
                e.parent.insert(i+1, sfm.Text("\n", e.pos, e.parent))
                return True
            return False
        def ge(i, e):
            ''' Iterate document allowing in place editing '''
            res = False
            if isinstance(e, sfm.Element):
                if ispara(e) or e.name == "v":
                    if i > 0:
                        res = ensurenl(i-1, e.parent[i-1])
                j = 0
                while j < len(e):
                    if ge(j, e[j]):
                        j += 1
                    j += 1
            return res
        if self.doc is None or not len(self.doc):
               return
        ge(0, self.doc[0])

    def _proctext(self, fn, doc=None):
        def _g(e):
            if isinstance(e, sfm.Element):
                e[:] = map(_g, e)
                return e
            else:
                return fn(e)
        if doc is None:
            self.doc = map(_g, self.doc)
            return self.doc
        else:
            return map(_g, doc)

    def transform_text(self, *regs, doc=None):
        """ Given tuples of (lambda, match, replace) tests the lambda against the
            parent of a text node and if matches (or is None) does match and replace. """
        def fn(e):
            s = str(e)
            processed = False
            for r in regs:
                if r[0] is not None and not r[0](e.parent):
                    continue
                ns = r[1].sub(r[2], s)
                if ns != s:
                    processed = True
                    s = ns
            if processed:
                return sfm.Text(s, e.pos, e.parent)
            else:
                return e
        return list(self._proctext(fn, doc=doc))

    def letter_space(self, inschar, doc=None):
        from ptxprint.sfm.ucd import get_ucd
        def fn(e):
            if not e.parent or not isScriptureText(e.parent):
                return e
            done = False
            lastspace = id(e.parent[0]) != id(e)

            res = []
            for (islet, c) in groupby(str(e), key=lambda x:get_ucd(ord(x), "gc") in takslc_cats and x != "|"):
                chars = "".join(c)
                # print("{} = {}".format(chars, islet))
                if not len(chars):
                    continue
                if islet:
                    res.append(("" if lastspace else inschar) + inschar.join(chars))
                    done = True
                else:
                    res.append(chars)
                lastspace = get_ucd(ord(chars[-1]), "InSC") in ("Invisible_Stacker", "Virama") \
                            or get_ucd(ord(chars[-1]), "gc") in ("Cf", "WS") \
                            or chars[-1] in (r"\|")                
            return sfm.Text("".join(res), e.pos, e.parent) if done else e
        if self.doc is None or not len(self.doc):
               return            
        self._proctext(fn, doc=doc)

    def calc_PToffsets(self):
        def _ge(e, a, ac):
            attrs = e.meta.get('Attributes', None)
            if attrs is None:
                return None
            styletype = e.meta['StyleType']
            if styletype.lower() == "character":
                s = str(e[0])
                bits = s.split("|")
                if len(bits) < 2 or "=" in bits[1]:
                    return None
                default = attrs.split()[0]
                # incorporate ="" 3 chars
                e.adjust = len(default) + 3 - (1 if default.startswith("?") else 0)
                # print(f"{e.pos.line}.{e.pos.col} {e.name} +{e.adjust} {default}")
            return None
        def _gt(e, a):
            return None
        sreduce(_ge, _gt, self.doc, None)
        
    def stripIntro(self, noIntro=True, noOutline=True):
        newdoc = []
        if not isinstance(self.doc[0], sfm.Element):
            return
        for e in self.doc[0]:
            if not isinstance(e, sfm.Element):
                newdoc.append(e)
                continue
            if noOutline and e.name.startswith("io"):
                continue
            if noIntro and e.name.startswith("i") and not e.name.startswith("io"):
                continue
            newdoc.append(e)
        self.doc[0][:] = newdoc

    def stripEmptyChVs(self, ellipsis=False):
        def iterfn(el, top=False):
            if isinstance(el, sfm.Element):
                lastv = None
                predels = []
                for c in el[:]:
                    if not isinstance(c, sfm.Element) or c.name != "v":
                        if iterfn(c):           # False if deletable ~> empty
                            if len(predels):
                                if isinstance(predels[-1], sfm.Element) \
                                                 and predels[-1].name == "p" \
                                                 and len(predels[-1]) == 1 \
                                                 and str(predels[-1][0]).strip() == "...":
                                    predels.pop(-1)
                                for p in predels:
                                    if isinstance(p, sfm.Element):
                                        p.parent.remove(p)
                            lastv = None
                            predels = []
                        else:
                            predels.append(c)
                    elif isinstance(c, sfm.Element) and c.name == "v":
                        if lastv is not None:
                            for p in predels:
                                p.parent.remove(p)
                            predels = []
                            if ellipsis:
                                i = lastv.parent.index(lastv)
                                ell = sfm.Text("...", parent=lastv.parent)
                                lastv.parent.insert(i, ell)
                                predels.append(ell)
                                lastv.parent.pop(i+1)
                            else:
                                lastv.parent.remove(lastv)
                        lastv = c
                if lastv is not None:
                    lastv.parent.remove(lastv)
                res = len(el) != 0
                nonemptypredels = [p for p in predels if isinstance(p, sfm.Element) or not re.match(r"^\s*$", str(p))]
                ell = None
                if len(nonemptypredels):
                    if ellipsis:
                        p = nonemptypredels[0]
                        i = p.parent.index(p)
                        st = p.parent.meta.get("styletype", "")
                        if st is None or st.lower() == "paragraph":
                            ell = sfm.Text("...", parent=p.parent)
                        else:
                            ell = sfm.Element('p', parent=p.parent, meta=self.sheets['p'])
                            ell.append(sfm.Text("...\n", parent=ell))
                        p.parent.insert(i, ell)
                for p in predels:
                    p.parent.remove(p)
                predels = [ell] if ell is not None else []
                st = el.meta.get("styletype", "") 
                if (st is None or st.lower() == "paragraph") and len(el) == len(predels):
                    # el.parent.remove(el)
                    return True if st is None else False  # To handle empty markers like \pagebreak 
            elif re.match(r"^\s*$", str(el)) or re.match(r"\.{3}\s*$", str(el)):
                return False
            return True
        iterfn(self.doc[0], top=True)

def read_module(inf, sheets):
    lines = inf.readlines()
    if not re.match(r"\uFEFF?\\id\s", lines[0]):
        lines.insert(0, "\\id MOD Module\n")
    return Usfm(lines, sheets)

exclusionmap = {
    'v': ['v'],
    'x': ['x'],
    'f': ['f'],
    's': ['s', 's1', 's2'],
    'p': ['fig']
}

class Module:

    localise_re = re.compile(r"\$([asl]?)\(\s*(\S+\s+\d+(?::[^)\s]+)?)\s*\)")
    localcodes = {'a': 0, 's': 1, 'l': 2}

    def __init__(self, fname, usfms, usfm=None):
        self.fname = fname
        self.usfms = usfms
        self.usfms.makeBookNames()
        self.sheets = self.usfms.sheets.copy()
        modinfo = { 'OccursUnder': {'id'}, 'TextType': 'Other', 'EndMarker': None, 'StyleType': 'Paragraph'}
        modsheet = {k: style.Marker(modinfo) for k in ('inc', 'vrs', 'ref', 'refnp', 'rep', 'mod')}
        self.sheets.update(modsheet)
        for k, v in self.sheets.items():
            if 'OccursUnder' in v and 'c' in v['OccursUnder']:
                v['OccursUnder'].add('id')
        if usfm is not None:
            self.doc = usfm
        else:
            with open(fname, encoding="utf-8") as inf:
                self.doc = read_module(inf, self.sheets)

    def parse(self):
        if self.doc.doc is None:
            return []
        #self.removes = set()
        self.removes = set(sum(exclusionmap.values(), []))
        final = sum(map(self.parse_element, self.doc.doc), [])
        return final

    def localref(self, m):
        rl = RefList.fromStr(m.group(2), context=self.usfms.booknames)
        loctype = m.group(1) or "a"
        tocindex = self.localcodes.get(loctype.lower(), 0)
        return rl.str(context=self.usfms.booknames, level=tocindex)

    def parse_element(self, e):
        if isinstance(e, sfm.Text):
            t = self.localise_re.sub(self.localref, str(e))
            if t != e:
                return [sfm.Text(t, e.pos, e.parent)]
            return [e]
        elif e.name == "ref" or e.name == "refnp":
            res = []
            isidparent = e.parent is None or e.parent.name == "id"
            reps = []
            curr = e.parent.index(e)
            while curr + 1 < len(e.parent):
                rep = e.parent[curr+1]
                if not isinstance(rep, sfm.Element) or rep.name != "rep":
                    break
                # parse rep
                m = re.match("^\s*(.*?)\s*=>\s*(.*?)\s*$", str(rep[0]), re.M)
                if m:
                    reps.append((None,
                            re.compile(r"\b"+m.group(1).replace("...","[^\n\r]+")+"(\\b|(?=\\s)|$)"),
                            m.group(2)))
                del e.parent[curr+1]
            for r in RefList.fromStr(str(e[0]), context=self.usfms.booknames):
                p = self.get_passage(r, removes=self.removes, strippara=e.name=="refnp")
                if e.name == "ref":
                    for i, t in enumerate(p):
                        if isinstance(t, sfm.Element) and t.meta.get('StyleType', '').lower() == 'paragraph':
                            if i:
                                p[0:i] = [self.new_element(e, "p1" if isidparent else "p", p[0:i])]
                            break
                    else:

                        p = [self.new_element(e, "p1" if isidparent else "p", p)]
                res.extend(p)
            if len(reps):
                res = self.doc.transform_text(*reps, doc=res)
            return res
        elif e.name == 'inc':
            s = "".join(map(str, e)).strip()
            for c in s:
                if c == "-":
                    self.removes = set(sum(exclusionmap.values(), []))
                else:
                    self.removes.difference_update(exclusionmap.get(c, []))
        elif e.name == 'mod':
            mod = Module(e[0].strip(), self.usfms)
            return mod.parse()
        else:
            cs = sum(map(self.parse_element, e), [])
            e[:] = cs
        return [e]

    def get_passage(self, ref, removes={}, strippara=False):
        if ref.first.book is None:
            return []
        book = self.usfms.get(ref.first.book.upper())
        if book is None:
            return []
        return book.subdoc(ref, removes=removes, strippara=strippara)

    def new_element(self, e, name, content):
        return sfm.Element(name, e.pos, [], e.parent, content=[sfm.Text("\n", e.pos)] \
                                                        + content, meta=self.sheets[name])
