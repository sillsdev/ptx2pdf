import re, regex, logging, os, time
from ptxprint.reference import MakeReference, BookNames
import usfmtc
from usfmtc.usfmparser import Grammar
from usfmtc.xmlutils import ParentElement, hastext, isempty
from usfmtc.usxmodel import iterusx, addesids
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
    'footnote': ('char', 'note', 'NoteText', None),
    'introduction': ('header', 'paragraph', 'other', "i"),
    'list': ('versepara', 'paragraph', 'other', "l"),
    'milestone': (None, 'milestone', None, None),
    'otherpara': ('versepara', 'paragraph', 'other', None),
    'sectionpara': ('versepara', 'paragraph', 'section', None),
    'title': ('header', 'paragraph', 'other', "m"),
    'standalone': (None, 'Standalone', None, None),
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
        sheet = self.get(mrk, None)
        if sheet is None:
            return None
        return mrktype(sheet, mrk)

def mrktype(sheet, mrk):
    mtype = sheet.get('mrktype', None)
    if mtype is not None:
        return mtype
    occurs = set(sheet.get('occursunder', {}))
    stype = sheet.get('styletype', "").lower()
    ttype = sheet.get('texttype', "").lower()
    for k, v in _occurstypes.items():
        if k in ("footnotechar", "crossreferencechar"):
            m = all(x in occurs for x in v.split(" "))
        else:
            m = any(x in occurs for x in v.split(" "))
        if m:
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
        sheet['mrktype'] = mtype
    return mtype

def typesFromMrk(mtype):
    ''' returns StyleType and TextType '''
    tinfo = _typetypes.get(mtype, None)
    if tinfo is not None:   # covers: footnote, introduction, list, milestone, otherpara, sectionpara, title
        return tinfo[1], tinfo[2]
    elif mtype in ('footnotechar', 'crossreferencechar'):
        return ('Character', 'NoteText')
    elif mtype in ('header', ):
        return ('Paragraph', 'Other')
    elif mtype in ('introchar',):
        return ('Character', 'Other')
    elif mtype in ('char', 'listchar', 'cell'):
        return ('Character', 'VerseText')
    elif mtype in ('versepara', ):
        return ('Paragraph', 'VerseText')
    elif mtype in ('crossreference', ):
        return ('Note', 'NoteText')
    return (None, None)

def createGrammar(sheets):
    grammar = Grammar()
    for k in sheets:
        if k not in grammar.marker_categories:
            v = sheets.mrktype(k)
            if v is not None:
                grammar.marker_categories[k] = v
        a = sheets[k].get("attributes", None)
        if a is not None and k not in grammar.attribmap:
            attrib = a.split()[0].replace("?", "")
            grammar.attribmap[k] = attrib
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
            self.books[bk] = Usfm.readfile(bkfile, self.grammar, elfactory=ParentElement)
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
    for this, isin in iterusx(root, unblocks=invertblocks, filt=[hastext], **kw):
        yield this.text if isin else this.tail

def modifytext(root, fn, invertblocks=False, **kw):
    for this, isin in iterusx(root, unblocks=invertblocks, filt=[hastext], **kw):
        if isin:
            this.text = fn(this.text, this)
        else:
            this.tail = fn(this.tail, this)
    
def _addorncv_hierarchy(e, curr):
    e.pos = RefPos(e.pos, curr)
    for c in e:
        _addorncv_hierarchy(c, curr)

def allparas(root):
    for e in root:
        if e.tag in ("para", "book", "chapter"):
            yield e
        if e.tag in ("sidebar", ):
            yield from allparas(e)

class Usfm:

    def __init__(self, xml, parser=None, grammar=None, book=None):
        self.xml = xml
        self.parser = parser
        self.grammar = grammar
        self.cvaddorned = False
        self.book = book

    @classmethod
    def readfile(cls, fname, grammar=None, sheet=None, elfactory=None):       # can also take the data straight
        if grammar is None:
            grammar = createGrammar(sheet if sheet is not None else [])
        usxdoc = usfmtc.readFile(fname, informat="usfm", keepparser=True, grammar=grammar, elfactory=elfactory)
        book = None
        bkel = usxdoc.getroot().find(".//book")
        if bkel is not None:
            book = bkel.get("code", None)
        return cls(usxdoc, usxdoc.parser, grammar=grammar, book=book)

    def getroot(self):
        return self.xml.getroot()

    def asUsfm(self, grammar=None):
        return self.xml.outUsfm(grammar=grammar)

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
        self.kpars = {}
        sections = []
        i = -1
        currpi = None
        for x, isin in iterusx(root):
            if isin:
                if x.tag == 'para':
                    currp = x
                continue
            p = x
            if x.parent == root:
                i += 1
            if p.tag == "chapter":
                currc = int(p.get("number", 0))
                if currc >= len(self.chapters):
                    self.chapters.extend([self.chapters[-1]] * (currc - len(self.chapters) + 1))
                self.chapters[currc] = i
                curr = MakeReference(bk, currc, 0)
            elif p.tag == "para":
                if istype(p.get("style", ""), ('sectionpara', 'title')):
                    sections.append(p)
                else:
                    if isempty(p.text) and len(p) and p[0].tag == "verse":
                        currv = p[0].get("number", curr.last.verse if curr is not None else None)
                        curr = MakeReference(bk, curr.first.chapter, currv)
                        if curr.first != curr.last and curr.last.verse < 200 and curr.first not in self.bridges:
                            for r in curr.allrefs():
                                self.bridges[r] = curr
                        # add to bridges if a RefRange
                    _addorncv_hierarchy(p, curr)
                    for s in sections:
                        _addorncv_hierarchy(s, curr)
                    sections = []
            elif p.tag == "verse":
                if curr is not None:
                    currv = p.get("number", curr.last.verse)
                    curr = MakeReference(bk, curr.first.chapter, currv)
                # add to bridges if a RefRange
            elif p.tag == "char":
                s = p.get("style")
                if s == "k":
                    v = p.get("key", p.text.strip().replace(" ", ""))    # there is more to this
                    self.kpars[v] = currp
            p.pos = RefPos(p.pos, curr)
        self.chapters.append(i)
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

    nonvernacular = ('otherpara', 'header', 'attribute')
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

    def visitall(self, fn, root, state=None):
        state = fn(root, state)
        for c in root:
            state = self.visitall(fn, c, state=state)
        return state

    def make_zsetref(self, ref, book, parent, pos):
        attribs = {'style': 'zsetref', 'bkid': str(ref.book), 'chapter': str(ref.chapter), 'verse': str(ref.verse)}
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
            if r.first.chapter > last[1] or r.first.chapter < last[0]:
                chaps.append((self.chapters[r.first.chapter:r.last.chapter+2], [i]))
                last = (r.first.chapter, r.last.chapter)
            elif r.first.chapter >= last[0] and r.last.chapter <= last[1]:
                chaps[-1][1].append(i)
            else:
                chaps[-1][0].extend(self.chapters[last[1]+1:r.last.chapter+1])
                chaps[-1][1].append(i)
                last = (last[0], r.last.chapter)
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
                if out.tag == "usx" and start.tag not in ("para", "chapter", "book"):
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
                    res.append(self.make_zsetref(minref, None, root, None))
            if len(c[0]) > 2:
                logger.error(f"chapter too long: {c[0]}")
            for chap in range(c[0][0], c[0][-1]):
                copyrange(d[chap], res, c[1])
        return Usfm(usfmtc.USX(res, self.grammar), parser=self.parser, grammar=self.grammar)

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

    def transform_text(self, *regs, parts=[]):
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
        if not len(parts):
            parts = [self.getroot()]
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
        for i, c in enumerate(allparas(inels)):
            if c.tag == "chapter" or self.grammar.marker_categories.get(c.get('style', ''), "") == "versepara":
                break
            if filter(c):
                count += 1
                root.remove(c)
        logger.debug(f"stripIntro removed {count} paragraphs")

    def stripEmptyChVs(self, ellipsis=False):
        def hastext(c):
            if c.tail is not None: # and c.tail.strip() != "":
                return True
            if c.text is not None: # and c.text.strip() != "":
                return True
            return False
        def removeslice(e, s, f):
            els = list(e)
            f = min(f, len(els))
            for i in range(s, f):
                try:
                    e.remove(els[i])
                except IndexError:
                    raise IndexError(f"slice bug {i=}, {s=}, {f=}, {len(els)=}")
            return (s - f) if f > s else 0
        def addellipsis(r, s):
            e = r.__class__("para", attrib = {"style": "p"}, parent = r)
            e.text = "..."
            r.insert(s + 1, e)
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
        for e in allparas(inels[i:]):
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
                    elif hastext(c): 
                        if isempty and j + offset > startv + 1:
                            if startve is not None:
                                startve.tail = "..." if ellipsis else ""
                            offset += removeslice(e, startv + 1, j + offset - 1)
                        isempty = False
                if isempty:
                    if startv == 0:
                        root.remove(e)
                    else:
                        removeslice(e, startv + 1, len(e))
                        if startve is not None:
                            startve.tail = "..." if ellipsis else ""
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
                    end = j + offset - 1
                    offset += removeslice(root, i, end)
                    if ellipsis and i < end:
                        addellipsis(root, i - 1)
                        offset += 1
                    i = -1
            elif i < 0:
                i = j + offset
        if j > 0 and i >= 0:
            removeslice(root, i, j + offset + 1)
            if ellipsis and i < j + offset - 1:
                addellipsis(root, i - 1)
        return

    def addStrongs(self, strongs, showall):
        self.addorncv()
        currstate = [None, set()]
        root = self.getroot()
        enters = "cell char versepara".split()
        for x, isin in iterusx(root, blocks=enters, unblocks=True, filt=[hastext]):
            if isin:
                t = x.text
                r = x.pos.ref if hasattr(x.pos, 'ref') else None
            else:
                t = x.tail
                r = x.pos.ref
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
                    if isin:
                        x.text = b[0] + "\u200B"
                        i = 0
                    else:
                        x.tail = b[0] + "\u200B"
                        i = list(x.parent).index(x) + 1
                    for a in range(1, len(b), 2):
                        e = self.factory("char", attrib={"style": "xts", "strong": st.lstrip("GH"), "align": "r"})
                        e.text = "\\nobreak \u200A" + b[a]
                        if a < len(b) - 2:
                            e.tail = b[a+1]
                        if isin:
                            x.insert(i, e)
                        else:
                            x.parent.insert(i, e)
                        i += 1
                    matched = True
                logger.log(6, f"{r}{'*' if matched else ''} {regs=} {st=}")

    def getcvpara(self, c, v):
        if all(x in "0123456789" for x in c):
            c = int(c)
            if c >= len(self.chapters) - 1:
                logger.error(f"Failed to find chapter {c} of {len(self.chapters)}")
                return None
            pstart = self.chapters[c]
            pend = self.chapters[c+1]
            for i, p in enumerate(list(self.getroot()[pstart:pend]), pstart):
                for c in p:
                    if c.tag == "verse" and c.get("number") == v:
                        return p
        elif c == "k" and v in self.kpars:
            return self.kpars[v]
        return None

    def removeGlosses(self, glosses):
        killme = False
        root = self.getroot()
        for e in list(root):
            if e.tag == "para":
                for ke in e:
                    if ke.tag == "char" and ke.get("style", "") == "k":
                        kval = ke.get("key", re.sub("[ ]", "", ke.text))
                        killme = kval.lower() not in glosses
                if killme:
                    root.remove(e)

    def apply_adjlist(self, bk, adjlist):
        if adjlist is None:
            return
        self.addorncv()
        for a in adjlist.liststore:
            # book, c:v, para:int, stretch, mkr, expand:int, comment%
            if a[0] != bk or a[5] == 100:
                continue
            c, v = a[1].replace(":", ".").split(".")
            p = self.getcvpara(c, v)
            if p is None:
                continue
            for i in range(a[2] - 1):
                p = p.getnext()
            s = p.get("style", "")
            if "^" not in s and p.tag == "para":    # Just in case it isn't a para
                p.set("style", f"{s}^{a[5]}")

