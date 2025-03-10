import re, regex, logging, os, time
from ptxprint.reference import MakeReference, BookNames
import usfmtc
from usfmtc.usfmparser import Grammar
from usfmtc.xmlutils import ParentElement, hastext, isempty
from usfmtc.usxmodel import iterusx
from copy import deepcopy

logger = logging.getLogger(__name__)

# current categories: attrib, cell, char, crossreference, crossreferencechar,
#   footnote, footnotechar, header, ident, internal, chapter, introchar,
#   introduction, list, listchar, milestone, otherpara, sectionpara, title,
#   versepara

_occurstypes = {
    'footnotechar': 'fe f efe ef',
    'crossreferencechar': 'ex x',
    'char': 'p',
    'introchar': 'ip',
    'listchar': 'li',
    'versepara': 'c',
    'header': 'id',
}

_typetypes = {      # type: (type, StyleType, TextType, startswith)
    'footnote': ('char', 'note', None, None),
    'introduction': ('header', 'paragraph', 'other', "i"),
    'list': ('versepara', 'paragraph', 'other', "l"),
    'milestone': (None, 'milestone', None, None),
    'otherpara': ('versepara', 'paragraph', 'other', None),
    'sectionpara': ('versepara', 'paragraph', 'section', None),
    'title': ('header', 'paragraph', 'other', "m"),
}
    
def simple_parse(source, categories=False, keyfield="Marker"):
    res = {}
    mkr = ""
    category = ""
    for l in source.readlines():
        m = re.match(r"\\(\S+)\s*(.*)\s*$", l)
        if m is not None:
            key = m.group(1)
            v = m.group(2)
        else:
            continue
        val = v.strip()
        if categories and key.lower() == "category":
            category = val
            key = "Marker"
            val = "esb"
        elif key.lower() == "endcategory":
            category = ""
            continue
        if key.lower() == keyfield.lower():
            mkr = f"cat:{category}|{val}" if category else val
        res.setdefault(mkr,{})[key.lower()] = val
    return res

def merge_sty(base, other, forced=False, exclfields=None):
    for m, ov in other.items():
        if m not in base or forced:
            base[m] = ov.copy()
        else:
            for k, v in ov.items():
                if exclfields is not None and k in exclfields:
                    continue
                base[m][k] = v

def out_sty(base, outf, keyfield="Marker"):
    for m, rec in base.items():
        outf.write(f"\n\\{keyfield} {m}\n")
        for k, v in rec.items():
            if isinstance(v, (set, list, tuple)):
                v = " ".join(v)
            outf.write(f"\\{k} {v}\n")


class Sheets(dict):
    ''' Extracts mrkr info relevant for parsing from the stylesheet '''

    def __init__(self, init=None, base=None):
        if base is not None and base != "":
            self.update(deepcopy(base))
        self.files = []
        if init is None or not len(init):
            return
        for s in init:
            if os.path.exists(s):
                self.append(s)
        self.cleanup()      # make extra markers etc.

    def copy(self):
        res = self.__class__(base=self)
        return res

    def append(self, sf):
        if os.path.exists(sf):
            with open(sf, encoding="utf-8", errors="ignore") as s:
                self.appendfh(s)
            self.files.append(sf)

    def appendfh(self, inf):
        news = simple_parse(inf)
        for k, v in news.items():
            if k in self:
                self[k].update(v)
            else:
                self[k] = v

    def cleanup(self):
        for k, v in list(self.items()):
            mt = self.mrktype(k)
            if mt == "milestone" and 'endmarker' in v:
                newk = v['endmarker']
                if newk not in self:
                    newv = v.copy()
                    self[newk] = newv

    def mrktype(self, mrk):
        if mrk not in self:
            return None
        mtype = self[mrk].get('mrktype', None)
        if mtype is not None:
            return mtype
        occurs = set(self[mrk].get('occursunder', "").split(' '))
        stype = self[mrk].get('styletype', "").lower()
        ttype = self[mrk].get('texttype', "").lower()
        for k, v in _occurstypes.items():
            if any(x in occurs for x in v.split(" ")):
                mtype = k
                break
        for k, v in _typetypes.items():
            matched = True
            for i, a in enumerate((mtype, stype, ttype)):
                if v[i] is not None and v[i] != a:
                    matched = False
                    break
            if v[3] is not None and not mrk.startswith(v[3]):
                matched = False
            if matched:
                mtype = k
                break
        if mtype is not None:
            self[mrk]['mrktype'] = mtype
        return mtype

def createGrammar(sheets):
    grammar = Grammar()
    for k in sheets:
        if k not in grammar.marker_categories:
            v = sheets.mrktype(k)
            if v is not None:
                grammar.marker_categories[k] = v
    return grammar


class UsfmCollection:
    def __init__(self, bkmapper, basedir, sheets):
        self.bkmapper = bkmapper
        self.basedir = basedir
        self.sheets = sheets
        self.books = {}
        self.times = {}
        self.tocs = []
        self.booknames = None
        self.setgrammar()

    def setgrammar(self):
        self.grammar = createGrammar(self.sheets)

    def get(self, bk):
        bkfile = self.bkmapper(bk)
        if bkfile is None:
            return None
        bkfile = os.path.join(self.basedir, bkfile)
        if not os.path.exists(bkfile):
            return None
        mtime = os.stat(bkfile).st_mtime
        if mtime > self.times.get(bk, 0):
            self.books[bk] = Usfm.readfile(bkfile, self.grammar)
            self.times[bk] = time.time()
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
                tocs = [""] * 3
                bkfile = self.bkmapper(bk)
                if bkfile is None or not len(bkfile):
                    continue
                bkfile = os.path.join(self.basedir, bkfile)
                if not os.path.exists(bkfile):
                    continue
                nochap = True
                with open(bkfile, encoding="utf-8") as inf:
                    while nochap:
                        l = inf.readline()
                        m = tocre.match(l)
                        if m:
                            r = int(m.group(1))
                            if r <= len(tocs):
                                tocs[r-1] = m.group(2)
                        elif '\\c ' in l:
                            nochap = False
                for i in range(len(tocs)-2,-1, -1):
                    if tocs[i] == "":
                        tocs[i] = tocs[i+1]
                self.booknames.addBookName(bk, *tocs)

    def get_markers(self, bks):
        ''' returns a list of all markers used in the corpus '''
        res = set()
        for bk in bks:
            mkrs = self.get(bk).getmarkers()
            res.update(mkrs)
        return res

class RefPos:
    def __init__(self, pos, ref):
        if pos is not None:
            self.l = pos.l
            self.c = pos.c
            self.kw = pos.kw
        else:
            self.l = 0
            self.c = 0
            self.kw = {}
        self.ref = ref

_recat = re.compile(r"[_^].*?")

def category(s):
    s = _recat.sub("", s)
    return Grammar.marker_categories.get(s, "")

def istype(s, t):
    if isinstance(t, str):
        t = [t]
    return category(s) in t

def textiter(root, invertblocks=False, **kw):
    ''' Iterates the element hiearchy returning all non empty text. Optionally
        it ignores any elements whose style is in the blocked categories passed. '''
    for this in iterusx(root, unblocks=invertblocks, filt=[hastext], **kw):
        yield this.parent.text if this.head is None else this.head.tail

def modifytext(root, fn, invertblocks=False, **kw):
    for this in iterusx(root, unblocks=invertblocks, filt=[hastext], **kw):
        if this.head is None:
            this.parent.text = fn(this.parent.text, this.parent)
        else:
            this.head.tail = fn(this.head.tail, this.head)
    
def _addorncv_hierarchy(e, curr):
    e.pos = RefPos(e.pos, curr)
    for c in e:
        _addorncv_hierarchy(c, curr)


class Usfm:

    def __init__(self, xml, parser=None, grammar=None):
        self.xml = xml
        self.parser = parser
        self.grammar = grammar
        self.cvaddorned = False

    @classmethod
    def readfile(cls, fname, grammar=None, sheet=None):           # can also take the data straight
        if grammar is None and sheet is not None:
            grammar = createGrammar(sheet)
        usxdoc = usfmtc.readFile(fname, informat="usfm", keepparser=True, grammar=grammar)
        return cls(usxdoc, usxdoc.parser, grammar=grammar)

    def getroot(self):
        return self.xml.getroot()

    def asUsfm(self):
        return self.xml.outUsfm()

    def outUsx(self, fname):
        return self.xml.outUsx(fname)

    def addorncv(self, curr=None, factory=ParentElement):
        if self.cvaddorned:
            return
        root = self.getroot()
        self.bridges = {}
        bk = root[0].get('code')
        self.factory = factory
        self.chapters = [0]
        sections = []
        i = -1
        for x in iterusx(root):
            if x.head is None:
                continue
            p = x.head
            if x.parent == root:
                i += 1
            if p.tag == "chapter":
                currc = int(p.get("number", 0))
                if currc >= len(self.chapters):
                    self.chapters.extend([i] * (currc - len(self.chapters) + 1))
                self.chapters[currc] = i
                curr = MakeReference(bk, currc, 0)
            elif curr is None:
                continue
            elif p.tag == "para":
                if istype(p.get("style", ""), ('sectionpara', 'title')):
                    sections.append(p)
                else:
                    if isempty(p.text) and len(p) and p[0].tag == "verse":
                        currv = p[0].get("number", curr.last.verse)
                        curr = MakeReference(bk, curr.first.chap, currv)
                        if curr.first != curr.last and curr.last.verse < 200 and curr.first not in self.bridges:
                            for r in curr.allrefs():
                                self.bridges[r] = curr
                        # add to bridges if a RefRange
                    _addorncv_hierarchy(p, curr)
                    for s in sections:
                        _addorncv_hierarchy(s, curr)
                    sections = []
            elif p.tag == "verse":
                currv = p.get("number", curr.last.verse)
                curr = MakeReference(bk, curr.first.chap, currv)
                # add to bridges if a RefRange
            p.pos = RefPos(p.pos, curr)
        for s in sections:
            _addorncv_hierarchy(s, curr)
        self.cvaddorned = True

    def readnames(self):
        root = self.getroot()
        res = [""] * 3
        for i in range(3):
            e = root.find('.//para[@style="toc{}"]'.format(i+1))
            if e is not None:
                res[i] = e.text.strip()
        self.tocs = res

    nonvernacular = ('otherpar', 'header', 'attrib')
    def getwords(self, init=None, constrain=None, lowercase=False):
        root = self.getroot()
        wre = regex.compile(r"([\p{L}\p{M}\p{Cf}]+)")
        if init is None:
            init = {}
        a = init
        for s in textiter(root, blocks=self.nonvernacular):
            for w in wre.split(str(s))[1::2]:
                if lowercase:
                    w = w.lower()
                if constrain is None or w in constrain:
                    a[w] = a.get(w, 0) + 1
        return a

    def hyphenate(self, hyph, nbhyphens):
        hyphenchar = "\u2011" if nbhyphens else hyph.get_hyphen_char()
        def dohyphenate(txt, parent):
            return hyph.hyphenate(txt, hyphenchar)
        modifytext(self.getroot(), dohyphenate, blocks=self.nonvernacular)

    tagmapping = {"chapter": "c", "verse": "v", "ref": "ref"}

    def getmarkers(self, root=None, acc=None):
        if root is None:
            root = self.getroot()
        if acc is None:
            acc = set()
        if root.tag in ("char", "para", "note", "ms", "figure", "link", "book", "row", "sidebar", "cell"):
            acc.add(root.get("style", ""))
        elif root.tag in self.tagmapping:
            acc.add(self.tagmapping[root.tag])
        for c in root:
            self.getmarkers(c, acc)
        return acc

    def make_zsetref(self, ref, book, parent):
        attribs = {'bkid': str(ref.book), 'chapter': str(ref.chap), 'verse': str(ref.verse)}
        if book is not None:
            attribs['book'] = book
        res = self.factory("ms", attribs, parent=parent)
        return res

    def subdoc(self, refranges, removes={}, strippara=False, keepchap=False, addzsetref=True):
        ''' Creates a document consisting of only the text covered by the reference
            ranges. refrange is a RefList of RefRange or a RefRange'''
        self.addorncv()
        if not isinstance(refranges, list):
            refranges = [refranges]
        last = (0, -1)
        chaps = []
        for i, r in enumerate(refranges):
            if r.first.chap > last[1] or r.first.chap < last[0]:
                chaps.append((self.chapters[r.first.chap:r.last.chap+2], [i]))
                last = (r.first.chap, r.last.chap)
            elif r.first.chap >= last[0] and r.last.chap <= last[1]:
                chaps[-1][1].append(i)
            else:
                chaps[-1][0].extend(self.chapters[last[1]+1:r.last.chap+1])
                chaps[-1][1].append(i)
                last = (last[0], r.last.chap)
        def pred(e, rlist):
            if e.parent is None:
                return True
            if e.parent.get('style', e.tag) in removes:
                return False
            if any(e.pos.ref in refranges[i] for i in rlist) \
                    and (e.pos.ref.first.verse != 0 or refranges[i].first.verse == 0 or e.get('style', e.tag) == "c"):
                if strippara and e.tag == "para":
                    return False
                return True
            return False

        def copyrange(start, out, rlist, pstyle=None) -> bool:
            res = out
            if start.tag == "para":
                pstyle = start.get("style", "p")
            isactive = False
            if pred(start, rlist):
                isactive = True
                if out.tag == "usx" and start.tag != "para":
                    out = self.factory("para", attrib=dict(style=pstyle), parent=out, pos=start.pos)
                res = self.factory(start.tag, start.attrib, parent=out, pos=start.pos)
                out.append(res)
                res.text = start.text
            endactive = isactive
            for c in start:
                endactive = copyrange(c, res, rlist, pstyle)
            if endactive:
                res.tail = start.tail
            return endactive

        root = self.getroot()
        d = list(root)
        res = self.factory("usx", root.attrib)
        res.text = root.text
        for c in chaps:
            if addzsetref:
                minref = min(refranges[r].first for r in c[1])
                if minref.verse > 0:
                    res.append(self.make_zsetref(minref, None, c[0][0].parent, c[0][0].pos))
            if len(c[0]) > 2:
                print(f"chapter too long: {c[0]}")
            for chap in range(c[0][0], c[0][-1]):
                copyrange(d[chap], res, c[1])
        return Usfm(usfmtc.USX(res), parser=self.parser)

    def getsubbook(self, refrange, removes={}):
        return self.subdoc(refrange, removes=removes)

    def versesToEnd(self):
        root = self.getroot()
        addesids(root)
        for el in root.findall('verse[eid=""]'):
            el.parent.remove(el)
        for el in root.findall('verse'):
            ref = RefList.fromStr(el.get('eid'))[0]
            el.set('number', str(ref.verse) + (ref.subverse or ""))
            del el.attrib['eid']

    def iterel(self, e, atend=None):
        yield e
        for c in e:
            yield from self.iterel(c, atend=atend)
        if atend is not None:
            atend(e)

    def iterVerse(self, chap, verse):
        if chap >= len(self.chapters):
            return
        start = list(self.getroot())[self.chapters[chap]]
        it = self.iterel(start)
        for e in it:
            if e.tag == "chapter" and int(e.get('number')) != chap:
                return
            elif verse == "0" or (e.tag == "verse" and e.get('number') == verse):
                yield e
                break
        else:
            return
        for e in it:
            if e.tag in ("chapter", "verse"):
                break
            yield e

    def normalise(self):
        ''' Normalise USFM in place '''
        canonicalise(self.getroot())

    def transform_text(self, *regs, parts):
        """ Given tuples of (lambda, match, replace) tests the lambda against the
            parent of a text node and if matches (or is None) does match and replace. """
        def fn(s, parent=None):
            if s is None or not len(s):
                return s
            for r in regs:
                if r[0] is not None and parent is not None and not r[0](parent):
                    continue
                s = r[1].sub(r[2], s)
            return s
        for p in parts:
            modifytext(p, fn)

    def stripIntro(self, noIntro=True, noOutline=True):
        if noIntro and noOutline:
            def filter(e):
                return self.grammar.marker_categories.get(e.get('style', ''), "") == "introduction"
        elif noOutline:
            def filter(e):
                return e.get("style", "").startswith("io")
        elif noIntro:
            def filter(e):
                return not e.get("style", "").startswith("io") and self.grammar.marker_categories.get(e.get('style', ''), "") == "introduction"
        else:
            return
        root = self.getroot()
        inels = list(root)
        count = 0
        for i, c in enumerate(inels):
            if c.tag == "chapter" or self.grammar.marker_categories.get(c.get('style', ''), "") == "versepara":
                break
            if filter(c):
                count += 1
                root.remove(c)
        logger.debug(f"stripIntro removed {count} paragraphs")

    def stripEmptyChVs(self, ellipsis=False):
        def hastext(c):
            if c.tail is not None and c.tail.strip() != "":
                return True
            if c.text is not None and c.text.strip() != "":
                return True
            return False
        def removeslice(e, s, f):
            els = list(e)
            for i in range(s, f):
                try:
                    e.remove(els[i])
                except IndexError:
                    raise IndexError(f"slice bug {i=}, {s=}, {f=}, {len(els)=}")
            return s-f
        root = self.getroot()
        inels = list(root)
        # scan for first chapter
        for i, e in enumerate(inels):
            if e.tag == "chapter":
                break
        else:
            return
        startc = i
        i += 1
        for e in inels[i:]:
            # process paragraphs and perhaps remove them if empty
            if e.tag == "para":
                isempty = False
                offset = 0
                for j, c in enumerate(list(e)):
                    if c.tag == "verse":
                        if not hastext(c):
                            if not isempty:
                                startv = j + offset
                                startve = c
                            isempty = True
                    elif hastext(c) and isempty and j + offset > startv + 1:
                        if startve is not None:
                            startve.tail = "..."
                        offset += removeslice(e, startv + 1, j + offset)
                        isempty = False
                if isempty:
                    if startv == 0:
                        root.remove(e)
                    else:
                        removeslice(e, startv + 1, len(e))
                        if startve is not None:
                            startve.tail = "..."
                            startve = None
                            startv = 0
            elif e.tag != "chapter":
                if hastext(e):
                    isempty = False
        # deal with empty chapter ranges
        inels = list(root)      # updated root due to removes above
        offset = 0
        for j, e in enumerate(inels[i:], i):
            if e.tag != "chapter":
                if j > 0 and i >= 0:
                    offset += removeslice(root, i, j + offset)
                    i = -1
            elif i < 0:
                i = j + offset
        return

    def addStrongs(self, strongs, showall):
        self.addorncv()
        currstate = [None, set()]
        root = self.getroot()
        enters = "cell char versepara".split()
        for x in iterusx(root, blocks=enters, unblocks=True, filt=[hastext]):
            if x.head is None:
                t = x.parent.text
                r = x.parent.pos.ref if hasattr(x.parent.pos, 'ref') else None
            else:
                t = x.head.tail
                r = x.head.pos.ref
            if r != currstate[0]:
                currstate = [r, set(strongs.getstrongs(r))]
            for st in list(currstate[1]):
                regs = strongs.regexes[st] if st in strongs.regexes else strongs.addregexes(st)
                if not len(regs):
                    currstate[1].remove(st)
                    continue
                matched = False
                try:
                    regre = regex.compile(("(?<!\u200A?)" if not showall else "") + regs, regex.I | regex.F)
                except regex._regex_core.error as e:
                    raise SyntaxError(f"Faulty regex in {regs}: {e}")
                b = regre.split(t)
                if len(b) > 1:
                    if x.head is None:
                        x.parent.text = b[0] + "\u200B"
                        i = 0
                    else:
                        x.head.tail = b[0] + "\u200B"
                        i = list(x.parent).index(x.head) + 1
                    for a in range(1, len(b), 2):
                        e = self.factory("char", attrib={"style": "xts", "strong": st.lstrip("GH"), "align": "r"})
                        e.text = "\\nobreak \u200A" + b[a]
                        if a < len(b) - 2:
                            e.tail = b[a+1]
                        x.parent.insert(i, e)
                        i += 1
                    matched = True
                logger.log(6, f"{r}{'*' if matched else ''} {regs=} {st=}")
