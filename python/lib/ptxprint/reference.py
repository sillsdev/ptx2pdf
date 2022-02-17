
from collections import namedtuple
import re, sys, os
from ptxprint.utils import chaps, oneChbooks, books, allbooks, binsearch, pycodedir
from base64 import b64encode
from functools import reduce
import json

startchaps = list(zip([b for b in allbooks if 0 < int(chaps[b]) < 999],
                      reduce(lambda a,x: a + [a[-1]+x], (int(chaps[b]) for b in allbooks if 0 < int(chaps[b]) < 999), [0])))
startchaps += [("special", startchaps[-1][1]+1)]
startbooks = dict(startchaps)
allchaps = ['GEN'] + sum([[b] * int(chaps[b]) for b in allbooks if 0 < int(chaps[b]) < 999], []) + ['special']
b64codes = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
b64lkup = {b:i for i, b in enumerate(b64codes)}

def readvrs(fname):
    ''' res[book number] [0] versenum of start of book from start of Bible
                         [1..n] number of verses from start of book to end of chapter'''
    res = [[] for i in range(len(allbooks))]
    with open(fname, encoding="utf-8") as inf:
        for li in inf.readlines():
            l = li.strip()
            if l.startswith("#"):
                continue
            b = l.split()
            if not len(b) or (len(b) == 5 and b[2] == "="):
                continue
            if b[0] not in books:
                continue
            verses = [int(x.split(':')[1]) for x in b[1:]]
            versesums = reduce(lambda a, x: (a[0] + [a[1]+x], a[1]+x), verses, ([0], 0))
            res[books[b[0]]] = versesums[0]
    curr = 0
    for b in res:
        if len(b):
            b[0] = curr
            curr += b[-1]
        else:
            b.append(curr)
    return res

class RefSeparators(dict):
    _defaults = {
        "books": "; ",      # separator between references in different books
        "chaps": ";",       # separator between references in different chapters
        "verses": ",",      # separator between references in the same chapter
        "cv": ":",          # separator between chapter and verse
        "bkc": " ",         # separator between book and chapter
        "onechap": False,   # output chapter in single chapter books
        "mark": lambda r, s: (r.mark or "") + s,
        "bksp": " ",
        "range": "-",
    }
    def __init__(self, **kw):
        self.update(kw)
        for k, v in self._defaults.items():
            if k not in self:
                self[k] = v

class Reference:

    vrs = None

    def __init__(self, book, chap, verse, subverse=None, mark=None):
        self.book = book
        self.chap = chap
        self.verse = verse
        self.subverse = subverse
        self.mark = mark

    @classmethod
    def loadvrs(cls, fname=None):
        if fname is None:
            fname = os.path.join(pycodedir(), 'eng.vrs')
        cls.vrs = readvrs(fname)
        return cls.vrs

    def str(self, context=None, level=0, lastref=None, addsep=RefSeparators()):
        sep = ""
        hasbook = False
        if lastref is None or lastref.book != self.book:
            res = ["{}".format(self.book if context is None else context.getLocalBook(self.book, level)).replace(" ", addsep['bksp'])]
            if lastref is not None and lastref.book is not None:
                sep = addsep['books']
            hasbook = len(res[0]) != 0
        else:
            res = []
        if self.chap > 0 and (addsep['onechap'] or self.book not in oneChbooks) \
                    and (lastref is None or lastref.book != self.book or lastref.chap != self.chap):
            if not len(res):
                sep = sep or addsep['chaps']
            res.append("{}{}".format(addsep['bkc'] if hasbook else "", self.chap))
            if self.verse > 0:
                res.append("{}{}{}".format(addsep['cv'], *([self.verse, self.subverse or ""] if self.verse < 200 else ["end", ""])))
        elif (lastref is None or lastref.verse != self.verse) and 0 < self.verse:
            res.append("{}{}{}".format(" " if hasbook else "", *[self.verse if self.verse < 200 else "end", self.subverse or ""]))
            if lastref is not None:
                sep = sep or addsep['verses']
        result = sep + (addsep['mark'](self, "".join(res)) if getattr(self, 'mark', None) is not None else "".join(res))
        return result

    def __str__(self):
        return self.str()

    def __eq__(self, o):
        if not isinstance(o, Reference):
            return False
        return all(getattr(self, a) == getattr(o, a) for a in ("book", "chap", "verse", "subverse"))

    def __contains__(self, o):
        if isinstance(o, RefRange):
            return self in o
        return self == o        

    def __lt__(self, o):
        if o is None:
            return False
        elif not isinstance(o, Reference):
            return not o < self or o == self
        if self.book != o.book:
            return books.get(self.book, 200) < books.get(o.book, 200)
        elif self.chap != o.chap:
            return self.chap < o.chap
        elif self.verse != o.verse:
            return self.verse < o.verse
        elif self.subverse != o.subverse:
            if self.subverse is None:
                return True
            elif o.subverse is None:
                return False
            else:
                return self.subverse < o.subverse
        return False

    def __gt__(self, o):
        if o is None:
            return True
        return o < self

    def __le__(self, o):
        return not self > o

    def __ge__(self, o):
        return not self < o

    def __hash__(self):
        return hash((self.book, self.chap, self.verse, self.subverse))

    @property
    def first(self):
        return self

    @property
    def last(self):
        return self

    def copy(self):
        res = self.__class__(self.book, self.chap, self.verse, self.subverse, self.mark)
        return res

    def astag(self):
        if self.subverse:
            subverse = str(ord(self.subverse.lower()) - 0x61)
        else:
            subverse = ""
        if self.book == "PSA" and self.chap == 119 and self.verse > 126:
            c = startbooks["special"] + 1
            v = self.verse - 126
        else:
            c = startbooks[self.book] + self.chap
            v = min(self.verse, 127)
        vals = [(c >> 5) & 63, ((v & 64) >> 6) + ((c & 31) << 1), v & 63]
        return subverse + "".join(b64codes[v] for v in vals)

    def asint(self):
        if self.vrs is None:
            self.loadvrs()
        coffset = self.vrs[books[self.book]][self.chap-1] if self.chap > 1 else 0
        return self.vrs[books[self.book]][0] + coffset + self.verse

    @classmethod
    def fromtag(cls, s, remainder=False):
        if s[0] in "0123456789":
            subverse = chr(0x61 + int(s[0]))
            s = s[1:]
        else:
            subverse = None
        v = [b64lkup.get(x, 0) for x in s[:3]]
        verse = v[2] + ((v[1] & 1) << 6)
        c = (v[1] >> 1) + (v[0] << 5)
        def chcmp(a, i, cv):
            if a[i][1] >= cv:
                return 1
            elif i < len(a)-1 and a[i+1][1] < cv:
                return -1
            return 0
        #i = binsearch(startchaps, c, chcmp)
        #bk, start = startchaps[i]
        bk = allchaps[c]
        start = startbooks[bk]
        chap = c - start
        if bk == "special":
            if chap == 1:
                bk = "PSA"
                chap = 119
                verse += 126
        elif verse == 127:
            verse = 200
        res = cls(bk, chap, verse, subverse=subverse)
        if remainder:
            return (res, s[3:])
        return res

    @classmethod
    def fromint(cls, val, bkstarts=None, chapshift=0):
        if cls.vrs is None:
            cls.loadvrs()
        if bkstarts is None:
            bkstarts = [x[0] for x in cls.vrs]
        def testbk(arr, i, v):
            a = arr[i]
            if v < a:
                return 1
            elif i+1 < len(arr) and v >= arr[i+1]:
                return -1
            return 0
        def testchap(arr, i, v):
            v -= chapshift * i
            if i == 0:
                if v > arr[1]:
                    return -1
                return 0
            elif arr[i] > v:
                return 1
            elif i+1 < len(arr) and arr[i+1]  < v:
                return -1
            return 0
        ind = binsearch(bkstarts, val, testbk)
        v = val - bkstarts[ind]
        c = binsearch(cls.vrs[ind], v, testchap) + 1
        v1 = v
        v -= chapshift * (c - 1)
        if c > len(cls.vrs[ind]) or cls.vrs[ind][c] >= v:
            c -= 1
        if c > 0 and c < len(cls.vrs[ind]):
            v = v - cls.vrs[ind][c]
        return cls(allbooks[ind], c+1, v)

    def allrefs(self):
        yield self


class RefRange:
    ''' Inclusive range of verses with first and last '''
    def __init__(self, first, last):
        self.first = first
        self.last = last

    def str(self, context=None, level=0, lastref=None, addsep=RefSeparators()):
        lastsep = RefSeparators(books="", chaps="", verses="", cv=addsep['cv'])
        res = "{}{}{}".format(self.first.str(context, level, lastref, addsep=addsep),
                              addsep['range'],
                              self.last.str(context, level, self.first, addsep=lastsep))
        return res

    def __str__(self):
        return self.str()

    def __eq__(self, other):
        if not isinstance(other, RefRange):
            return False
        return self.first == other.first and self.last == other.last

    def __lt__(self, o):
        return self.last <= o.first

    def __le__(self, o):
        return self.last <= o.last

    def __gt__(self, o):
        return self.first >= o.last

    def __ge__(self, o):
        return self.first >= o.first

    def __hash__(self):
        return hash((self.first, self.last))

    def __contains__(self, r):
        if isinstance(r, RefRange):
            return self.first <= r.first and r.last <= self.last
        return self.first <= r <= self.last

    def astag(self):
        return "{}-{}".format(self.first.astag(), self.last.astag())

    @classmethod
    def fromtag(cls, s, remainder=False):
        first, s = Reference.fromtag(s, remainder=True)
        if len(s) and s[0] == "-":
            last, s = Reference.fromtag(s[1:], remainder=True)
            res = cls(first, last)
        else:
            res = first
        if remainder:
            return (res, s)
        return res

    def _getmaxvrs(self, bk, chap):
        vrs = self.first.vrs or Reference.loadvrs()
        if bk not in books or len(vrs[books[bk]]) < chap:
            maxvrs = 200
        else:
            maxvrs = vrs[books[bk]][chap] - (vrs[books[bk]][chap-1] if chap > 1 else 0)
        return maxvrs

    def allrefs(self):
        vrs = self.first.vrs or Reference.loadvrs()
        r = self.first.copy()
        maxvrs = self._getmaxvrs(r.book, r.chap)
        while r <= self.last:
            yield r
            r.verse += 1
            if r.verse > maxvrs:
                r.chap += 1
                r.verse = 1
                if r.chap >= len(vrs[books[r.book]]):
                    newbk = books[r.book] + 1
                    while newbk < len(allbooks) and allbooks[newbk] not in books:
                        newbk += 1
                    if newbk >= len(allbooks):
                        return
                    r.book = allbooks[newbk]
                    r.chap = 1
                maxvrs = self._getmaxvrs(r.book, r.chap)

class AnyBooks:
    @classmethod
    def getBook(cls, s):
        return s

    @classmethod
    def getLocalBook(cls, s):
        return s

class BaseBooks:
    bookStrs = {k: [k]*3 for k, v in chaps.items() if 0 < int(v) < 999}
    bookNames = {k: k for k,v in chaps.items() if 0 < int(v) < 999}

    @classmethod
    def getBook(cls, s):
        ''' Returns canonical book name if the book is matched in our list '''
        return cls.bookNames.get(s, cls.bookNames.get(s.upper(), s.upper()))

    @classmethod
    def getLocalBook(cls, s, level=0):
        return cls.bookStrs[s][level]


class BookNames(BaseBooks):
    bookStrs = {}
    bookNames = {}

    def __init__(self):
        self.bookStrs = BaseBooks.bookStrs.copy()
        self.bookNames = BaseBooks.bookNames.copy()

    def getBook(self, s):
        ''' Returns canonical book name if the book is matched in our list '''
        return self.bookNames.get(s, self.bookNames.get(s.upper(), None))

    def getLocalBook(self, s, level=0):
        return self.bookStrs[s][level]

    def readBookNames(self, fpath):
        from xml.etree import ElementTree as et
        doc = et.parse(fpath)
        for b in doc.findall(".//book"):
            bkid = b.get("code")
            strs = [b.get(a) for a in ("abbr", "short", "long")]
            self.addBookName(bkid, *strs)

    def addBookName(self, bkid, *strs):
        self.bookNames[bkid] = bkid
        self.bookStrs[bkid] = strs
        bkstrs = {}
        for s in strs:
            for i in range(len(s)):
                if s[i] is None or s[i] == " ":
                    break
                bkstrs[s[:i+1]] = "" if bkstrs.get(s[:i+1], bkid) != bkid else bkid
                self.bookNames.update({k:v for k,v in bkstrs.items() if v != ""})


class RefList(list):
    @classmethod
    def fromStr(cls, s, context=BaseBooks, starting=None, marks=None):
        rerefs = re.compile(r"[\s;,]+")
        
        remarks = re.compile("^(["+"".join(marks)+r"])") if marks is not None else None
        rebook = re.compile(r"^(\d?[^0-9\-:.]+)")
        recv = re.compile(r"^(\d+)[:.](\d+|end)([a-z]?)")
        rec = re.compile(r"(\d+)([a-z]?)")
        self = cls()
        curr = Reference(None, 0, 0) if starting is None else starting
        currmark = None
        start = None
        mode = ""
        txt = re.sub(r"[\u200F]", "", s)
        for b in rerefs.split(txt):
            while len(b):
                if b == "end":
                    if mode != "r":
                        curr = self._addRefOrRange(start, curr)
                        start = None
                    if curr.chap > 0 and curr.verse == 0:
                        curr.chap = 200
                        mode = "c"
                    elif curr.verse > 0:
                        curr.verse = 200
                        mode = "v"
                    b = ""
                    continue
                if remarks is not None:
                    m = remarks.match(b)
                    if m:
                        currmark = m.group(1)
                        b = b[m.end():]
                        continue
                m = rebook.match(b)
                if m:
                    if mode != "r" and mode != "":
                        (curr, currmark) = self._addRefOrRange(start, curr, currmark)
                        start = None
                    bookinfo = m.groups()
                    curr.book = context.getBook(bookinfo[-1])
                    mode = "b"
                    b = b[m.end():]
                    continue
                m = recv.match(b)
                if m:
                    if mode not in "br":
                        (curr, currmark) = self._addRefOrRange(start, curr, currmark)
                        start = None
                    curr.chap = int(m.group(1))
                    if m.group(2):
                        curr.verse = 200 if m.group(2) == "end" else int(m.group(2))
                    if m.group(3):
                        curr.subverse = m.group(3) or None
                    b = b[m.end():]
                    mode = "v"
                    continue
                m = rec.match(b)
                if m:
                    v = int(m.group(1))
                    if m.group(2) or curr.verse > 0 or curr.book in oneChbooks:
                        if curr.book in oneChbooks:
                            curr.chap = 1
                            mode = "c"
                        if m.group(2) and curr.chap == 0:
                            raise SyntaxError("invalid string {} in context of {}".format(b, curr))
                        if mode not in "bcr":
                            c = curr.chap
                            (curr, currmark) = self._addRefOrRange(start, curr, currmark)
                            start = None
                            curr.chap = c
                        curr.subverse = m.group(2) or None
                        curr.verse = v
                    else:
                        if mode not in "bcr":
                            (curr, currmark) = self._addRefOrRange(start, curr, currmark)
                            start = None
                        mode = "c"
                        curr.chap = v
                    mode = "v"
                    b = b[m.end():]
                    continue
                if b.startswith("-"):
                    start = curr
                    curr = start.copy()
                    curr.subverse = None
                    b = b[1:]
                    mode = "r"
                    continue
                raise SyntaxError("Unknown string component {} in {}".format(b, s))
        if mode != "r" and mode != "":
            self._addRefOrRange(start, curr, currmark)
        return self

    def str(self, context=None, level=0, addsep=RefSeparators()):
        res = []
        lastref = None # Reference(None, 0, 0)
        for r in self:
            res.append(r.str(context, level, lastref, addsep=addsep))
            lastref = r.last if isinstance(r, RefRange) else r
        return "".join(res)

    def __str__(self):
        return self.str()

    def __eq__(self, other):
        return len(self) == len(other) and all(z[0] == z[1] for z in zip(self, other))

    def __add__(self, other):
        return self.__class__(self[:] + other[:])

    def __contains__(self, other):
        return any(other in x for x in self)

    def _addRefOrRange(self, start, curr, currmark):
        curr.mark = currmark
        self.append(curr if start is None else RefRange(start, curr))
        res = Reference(curr.book, 0, 0)
        currmark = None
        return (res, currmark)

    def simplify(self):
        res = []
        lastref = Reference(None, 0, 0)
        for r in self:
            t, u = (r.first, r.last)
            if t.book == lastref.book and t.chap == lastref.chap \
                    and t.subverse is None and t.verse == lastref.verse + 1:
                if isinstance(res[-1], RefRange):
                    res[-1].last = u
                else:
                    res[-1] = RefRange(lastref, u)
            else:
                res.append(r)
            lastref = u
        self[:] = res

    def filterBooks(self, books):
        self[:] = [r for r in self if r.first.book in books]

    def astag(self):
        return "".join(r.astag() for r in self)

    @classmethod
    def fromtag(cls, s):
        res = cls()
        while len(s) > 2:
            l, s = RefRange.fromtag(s, remainder=True)
            res.append(l)
        return res

    def allrefs(self):
        for r in self:
            if isinstance(r, RefRange):
                yield from r.allrefs()
            else:
                yield r

class RefJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Reference, RefRange, RefList)):
            return str(obj)
        elif isinstance(obj, set):
            return sorted(obj)
        return super()(obj)

class TestException(Exception):
    pass


def tests():
    r = Reference
    def t(s, t, *r):
        res = RefList.fromStr(s)
        tag = res.astag()
        tagref = RefList.fromtag(tag)
        if len(res) != len(r):
            raise TestException("Failed '{}' resulted in {} references, {}, rather than {}".format(s, len(res), res, len(r)))
        for z in zip(res, r):
            if z[0] != z[1]:
                raise TestException("Reference list failed '{}', {} != {}".format(s, z[0], z[1]))
        for z in zip(tagref, r):
            if z[0] != z[1]:
                raise TestException("Reference list from tag failed '{}', {} != {}: tag={}".format(s, z[0], z[1], tag))
        if str(res) != s:
            raise TestException("{} != canonical string of {}".format(s, str(res)))
        if tag != t:
            raise TestException("{} != {} in {}".format(tag, t, s))
        refint = res[0].first.asint()
        intref = Reference.fromint(refint)
        temp = res[0].first.copy()
        temp.subverse = None
        if intref != temp:
            raise TestException("{} has int({}) but that is {}".format(res[0].first, refint, intref))

    def testrange(s, a, b):
        res = RefList.fromStr(s)
        init = a.asint()
        end = b.asint()
        for r in res.allrefs():
            if r.asint() != init:
                raise TestException("{} in {} is out of order".format(r, s))
            if init > end:
                raise TestException("{} in {} is beyond the end {}".format(r, s, b))
            init += 1

    t("GEN 1:1", "ACB", r("GEN", 1, 1))
    t("JHN 3", "fQA", r("JHN", 3, 0))
    t("3JN 3", "kcD", r("3JN", 1, 3))
    t("1CO 6:5a", "0hYF", r("1CO", 6, 5, "a"))
    t("MAT 5:1-7", "dMB-dMH", RefRange(r("MAT", 5, 1), r("MAT", 5, 7)))
    t("MAT 7:1,2;8:6b-9:4", "dQBdQC1dSG-dUE", r("MAT", 7, 1), r("MAT", 7, 2), RefRange(r("MAT", 8, 6, "b"), r("MAT", 9, 4)))
    t("LUK 3:35-end", "egj-eh/", RefRange(r("LUK", 3, 35), r("LUK", 3, 200)))
    testrange("PSA 125:4-128:4", r("PSA", 125, 4), r("PSA", 128, 4))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if len(sys.argv) == 2 and 2 < len(sys.argv[1]) < 5:
            res = Reference.fromtag(sys.argv[1])
        else:
            res = RefList.fromStr(" ".join(sys.argv[1:]))
        tag = res.astag()
        print("{}: {}".format(res, tag))
    else:
        tests()
