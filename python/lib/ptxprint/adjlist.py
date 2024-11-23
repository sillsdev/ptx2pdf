
from ptxprint.utils import refKey
import re

adjre = re.compile(r"^(\S+)\s+(\d+[.:]\d+(?:[+-]*\d+)?|\S+)\s+([+-]?\d+)(?:\[(\d+)\])?")
restre = re.compile(r"^\s*\\(\S+)\s*(\d+)")

class AdjList:
    def __init__(self, centre, lowdiff, highdiff, diglotorder=[], gtk=None):
        self.lowdiff = lowdiff
        self.highdiff = highdiff
        self.centre = centre

        # book, c:v, para, stretch, mkr, expand%
        if gtk is None:
            self.liststore = []
        else:
            self.liststore = gtk.ListStore(str, str, int, str, str, int)
        self.changed = False
        self.adjfile = None

    def clear(self):
        self.liststore.clear()

    def find(self, *k):
        for i, r in enumerate(self.liststore):
            if r[:len(k)] == k:
                return r
            elif r[1] > k[1] or r[1] == k[1] and r[2] > k[2]:
                return i
        return -1

    def sort(self):
        allvals = [r for r in self.liststore]
        self.liststore.clear()
        for a in sorted(allvals, key=self.calckey):
            self.liststore.append(a)

    def setval(self, bk, cv, para, stretch, mkr, expand=None, append=False, force=False):
        row = [bk, cv, para, stretch, mkr, expand or self.centre]
        if append:
            self.liststore.append(row)
            return
        i = self.find(bk, cv, para)
        if isinstance(i, int):
            if i >= 0:
                self.liststore.insert(i, row=row)
            else:
                self.liststore.append(row)
        elif not force:       # got an iterator
            for j, k in enumerate(i):
                if row[j] != k:
                    self.liststore.set_value(i.iter, j, row[j])
        else:
            self.liststore[i.iter] = row

    def calckey(self, row):
        k = refKey("{0} {1}".format(*row))
        res = [k, row[2]]
        return res

    def readAdjlist(self, fname):
        self.adjfile = fname
        allvals = []
        self.liststore.clear()
        with open(fname, "r") as inf:
            for l in inf.readlines():
                c = ""
                if '%' in l:
                    c = l[l.find("%")+1:]
                    l = l[:l.find("%")]
                m = adjre.match(l)
                if m:
                    try:
                        val = [m.group(1), m.group(2), int(m.group(4) or 1), m.group(3), None, self.centre]
                    except ValueError:
                        val = None
                    if val is not None:
                        n = restre.match(c)
                        if n:
                            val[4] = n.group(1)
                            val[5] = int(n.group(2))
                        allvals.append(val)
        for a in sorted(allvals, key=self.calckey):
            self.liststore.append(a)

    def createAdjlist(self, fname=None):
        if fname is None:
            fname = self.adjfile
        if fname is None:
            return
        with open(fname, "w") as outf:
            for r in self.liststore:
                cv = r[1].replace(":", ".").replace(" ", "")
                if r[2] > 1:
                    line = "{0[0]} {1} {0[3]}[{0[2]}]".format(r, cv)
                else:
                    line = "{0[0]} {1} {0[3]}".format(r, cv)
                if r[4] and r[5] != self.centre:
                    line += " % \\{4} {5}".format(*r)
                outf.write(line + "\n")

    def createChanges(self, fname, diglot=""):
        lines = []
        for r in self.liststore:
            if not r[5] or r[5] == self.centre:
                continue
            if len(r[0]) > 3 and r[0][4] != diglot:
                continue
            c, v = re.split(r"[:.]", r[1], 1)
            firstv = v.split("-", 1)
            v = int(v) - 1
            if v < 0:
                c = int(c) - 1
                v = "end"
            else:
                c = int(c)
            lines.append("{0} {1}:{2} '\\\\{3}\s' > '\\{3}^{4} '".format(r[0][:3], c, v, r[4], r[5]))
        if len(lines):
            with open(fname, "w") as outf:
                outf.write("\n".join(lines))

    def save(self):
        if self.adjfile is None:
            return
        self.createAdjlist()
        chfile = self.adjfile.replace(".adj", "_changes.txt")
        self.createChanges(chfile)

    def increment(self, parref, offset):
        m = adjre.match(parref)
        if not m:
            return False
        cp = [m.group(0), m.group(1), int(m.group(2) or 0)]
        cpk = self.calckey(cp)
        for i, r in enumerate(self.liststore()):
            rk = self.calckey(r)
            if rk == cpk:
                self.liststore.set_value(r.iter, 2, r[2]+offset)
