
from collections import namedtuple
import re
from ptxprint.utils import chaps, oneChbooks, books

class Reference:
    def __init__(self, book, chap, verse, subverse=None):
        self.book = book
        self.chap = chap
        self.verse = verse
        self.subverse = subverse

    def __str__(self, context=None, level=0, lastref=None):
        if lastref is None or lastref.book != self.book:
            res = ["{}".format(self.book if context is None else context.getBook(self.book, level))]
        else:
            res = []
        if self.chap > 0 and self.book not in oneChbooks and (lastref is None or lastref.chap != self.chap):
            res.append("{}{}".format(" " if len(res) else "", self.chap))
            if self.verse > 0:
                res.append(":{}{}".format(*([self.verse, self.subverse or ""] if self.verse < 200 else ["end", ""])))
        elif (lastref is None or lastref.verse != self.verse) and 0 < self.verse:
            res.append("{}{}{}".format(" " if len(res) else "", *[self.verse if self.verse < 200 else "end", self.subverse or ""]))
        return "".join(res)

    def __eq__(self, o):
        if not isinstance(o, Reference):
            return False
        return all(getattr(self, a) == getattr(o, a) for a in ("book", "chap", "verse", "subverse"))

    def __lt__(self, o):
        if not isinstance(o, Reference):
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
        return o < self

    def __le__(self, o):
        return not self > o

    def __ge__(self, o):
        return not self < o

    def copy(self):
        res = self.__class__(self.book, self.chap, self.verse, self.subverse)
        return res


class RefRange:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    def __str__(self, context=None, level=0, lastref=None):
        res = "{}-{}".format(self.first.__str__(context, level, lastref),
                             self.last.__str__(context, level, self.first))
        return res

    def __eq__(self, other):
        if not isinstance(other, RefRange):
            return False
        return self.first == other.first and self.last == other.last

    def __lt__(self, o):
        return self.last <= o if isinstance(o, Reference) else self.last <= o.first

    def __le__(self, o):
        return self.last <= (o if isinstance(o, Reference) else o.last)

    def __gt__(self, o):
        return self.first >= o if isinstance(o, Reference) else self.first >= o.last

    def __ge__(self, o):
        return self.first >= (o if isinstance(o, Reference) else o.first)


class BaseBooks:
    bookStrs = chaps

    @classmethod
    def getBook(cls, s):
        ''' Returns canonical book name if the book is matched in our list '''
        res = cls.bookStrs.get(s, 0)
        if res != 0 and res != 999:
            return s
        return None


class BookNames(BaseBooks):
    @classmethod
    def readBookNames(cls, fpath):
        bkstrs = {}
        cls.bookNames = {}
        from xml.etree import ElementTree as et
        doc = et.parse(fpath)
        for b in doc.findall("//book"):
            bkid = b.get("code")
            strs = [b.get(a) for a in ("long", "short", "abbr")]
            cls.bookNames[bkid] = strs
            for s in strs:
                for i in range(len(s)):
                    if s[i] == " ":
                        break
                    bkstrs[s[:i+1]] = "" if bkstrs.get(s[:i+1], bkid) != bkid else bkid
        cls.bookStrs = {k:v for k,v in bkstrs.items() if v != ""}


class RefList(list):
    @classmethod
    def fromStr(cls, s, context=BaseBooks, starting=None):
        self = cls()
        curr = Reference(None, 0, 0) if starting is None else starting
        start = None
        mode = ""
        for b in re.split(r"[\s;,]+", s):
            while len(b):
                if b == "end":
                    if mode != "r":
                        curr = self._addRefOrRange(start, curr)
                    if curr.chap > 0 and curr.verse == 0:
                        curr.chap = 200
                        mode = "c"
                    elif curr.verse > 0:
                        curr.verse = 200
                        mode = "v"
                    b = ""
                    continue
                m = re.match(r"^\d?[^0-9\-:]+", b)
                if m:
                    if mode != "r" and mode != "":
                        curr = self._addRefOrRange(start, curr)
                    curr.book = context.getBook(m.group(0))
                    mode = "b"
                    b = b[m.end():]
                    continue
                m = re.match(r"^(\d+)[:.](\d+)([a-z]?)", b)
                if m:
                    if mode not in "br":
                        curr = self._addRefOrRange(start, curr)
                    curr.chap = int(m.group(1))
                    if m.group(2):
                        curr.verse = int(m.group(2))
                    if m.group(3):
                        curr.subverse = m.group(3) or None
                    b = b[m.end():]
                    mode = "v"
                    continue
                m = re.match(r"(\d+)([a-z]?)", b)
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
                            curr = self._addRefOrRange(start, curr)
                            curr.chap = c
                        curr.subverse = m.group(2) or None
                        curr.verse = v
                    else:
                        if mode not in "bcr":
                            curr = self._addRefOrRange(start, curr)
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
            self._addRefOrRange(start, curr)
        return self

    def __str__(self, context=None, level=0):
        res = []
        lastref = Reference(None, 0, 0)
        for r in self:
            res.append(r.__str__(context, level, lastref))
            lastref = r.last if isinstance(r, RefRange) else r
        return ", ".join(res)

    def __eq__(self, other):
        return len(self) == len(other) and all(z[0] == z[1] for z in zip(self, other))

    def _addRefOrRange(self, start, curr):
        self.append(curr if start is None else RefRange(start, curr))
        return Reference(curr.book, 0, 0)


class TestException(Exception):
    pass


def tests():
    def r(b, c, v, sv=None):
        return Reference(b, c, v, sv)
    def t(s, *r):
        res = RefList.fromStr(s)
        if len(res) != len(r):
            raise TestException("Failed '{}' resulted in {} references, {}, rather than {}".format(s, len(res), res, len(r)))
        for z in zip(res, r):
            if z[0] != z[1]:
                raise TestException("Failed '{}', {} != {}".format(s, z[0], z[1]))
        if str(res) != s:
            raise TestException("{} != canonical string of {}".format(s, str(res)))

    t("GEN 1:1", r("GEN", 1, 1))
    t("JHN 3", r("JHN", 3, 0))
    t("3JN 3", r("3JN", 1, 3))
    t("1CO 6:5a", r("1CO", 6, 5, "a"))
    t("MAT 5:1-7", RefRange(r("MAT", 5, 1), r("MAT", 5, 7)))
    t("MAT 7:1, 2, 8:6b-9:4", r("MAT", 7, 1), r("MAT", 7, 2), RefRange(r("MAT", 8, 6, "b"), r("MAT", 9, 4)))
    t("LUK 3:47-end", RefRange(r("LUK", 3, 47), r("LUK", 3, 200)))

if __name__ == "__main__":
    tests()
