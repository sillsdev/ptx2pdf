
from ptxprint.utils import refKey
from collections import UserList
import os,re
import logging

logger = logging.getLogger(__name__)

adjre = re.compile(r"^(\S{3})([A-Z]?)\s*(\d+[.:]\d+(?:[+-]*\d+)?|\S+)\s+([+-]?\d+)(?:\[(\d+)\])?")
refre = re.compile(r"^(\S{3})([A-Z]?)\s*(\d+[.:]\d+(?:[+-]*\d+)?|\S+)(?:\[(\d+)\])?")
restre = re.compile(r"^\s*(?:mrk=|\\)(\S+)\s*(?:expand=)?(\d+)(.*?)$")

class Liststore(list):
    """ structure: 
    """

    def get_value(self, line, col):
        return self[line][col]

    def set_value(self, line, col, val):
        self[line][col] = val

    def insert(self, i, row):
        rl = UserList(row)
        rl.iter = i
        super().insert(i, rl)
        for j, r in enumerate(self[i+1:], i+1):
            r.iter = j
        return rl.iter

    def append(self, row):
        rl = UserList(row)
        rl.iter = len(self)
        super().append(rl)
        return rl.iter
        


class AdjList:
    def __init__(self, centre, lowdiff, highdiff, diglotorder=[], gtk=None, fname=None, tname=None):
        self.lowdiff = lowdiff
        self.highdiff = highdiff
        self.centre = centre

        # book, c:v, para:int, stretch, mkr, expand:int, comment%
        if gtk is None:
            self.liststore = Liststore()
        else:
            self.liststore = gtk.ListStore(str, str, int, str, str, int, str)
        self.changed = False
        self.adjfile = fname
        self.trigfile = tname

    def clear(self):
        self.liststore.clear()

    def __len__(self):
        return len(self.liststore)

    def find(self, *k):
        for i, r in enumerate(self.liststore):
            if r[:len(k)] == k:
                return r
            elif r[1] > k[1] or r[1] == k[1] and r[2] > k[2]:
                return i
        return -1

    def sort(self):
        allvals = [[*r] for r in self.liststore]
        self.liststore.clear()
        for a in sorted(allvals, key=self.calckey):
            self.liststore.append(a)

    def setval(self, bk, cv, para, stretch, mkr, expand=None, append=False, force=False, comment=""):
        row = [bk, cv, para, stretch, mkr, expand or self.centre, comment]
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
        res = k[:3] + (k[5], row[2], k[3], k[4], k[6])
        return res

    def parseline(self, l):
        c = ""
        if '%' in l:
            c = l[l.find("%")+1:].strip()
            l = l[:l.find("%")]
        m = adjre.match(l)
        val = None
        if m:
            try:
                val = [m.group(1)+m.group(2), m.group(3), int(m.group(5) or 1),
                                m.group(4), None, self.centre, c]
            except ValueError:
                val = None
            if val is not None:
                n = restre.match(c)
                if n:
                    val[4] = n.group(1)
                    val[5] = int(n.group(2))
                    val[6] = n.group(3)
        return val

    def readAdjlist(self, fname):
        self.adjfile = fname
        allvals = []
        self.liststore.clear()
        with open(fname, "r", encoding="utf-8") as inf:
            for l in inf.readlines():
                val = self.parseline(l)
                if val is not None:
                    allvals.append(val)
        for a in sorted(allvals, key=self.calckey):
            self.liststore.append(a)

    def genline(self, r):
        cv = r[1].replace(":", ".").replace(" ", "")
        if r[2] > 1:
            line = "{0[0]} {1} {0[3]}[{0[2]}]".format(r, cv)
        else:
            line = "{0[0]} {1} {0[3]}".format(r, cv)
        if r[4]: # and r[5] != self.centre or r[6]:
            line += " % mrk={4} expand={5} {6}".format(*r)
        return line

    def createAdjlist(self, fname=None):
        if fname is None:
            fname = self.adjfile
        if fname is None:
            return
        if not len(self.liststore):
            self.remove_file(fname)
            return
        os.makedirs(os.path.dirname(fname), exist_ok=True) # Ensure the directory exists first
        with open(fname, "w", encoding="utf-8") as outf:
            for r in self.liststore:
                line = self.genline(r)
                outf.write(line + "\n")

    def createTriggerlist(self, fname=None):
        if fname is None:
            fname = self.trigfile
        if fname is None:
            return
        if not len(self.liststore):
            self.remove_file(fname)
            return
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        with open(fname, 'w', encoding='utf-8') as outf:
            for r in self.liststore:
                if r[5] == self.centre:
                    continue
                lines = [""]
                lines.append(rf"\AddTrigger {r[0]}{r[1]}={r[2]}")
                lines.append(rf"\zexp {r[5]}\*")
                lines.append(r"\EndTrigger")
                outf.write("\n".join(lines))

    def remove_file(self, fname):
        try:
            os.remove(fname)
        except FileNotFoundError:
            pass  # File does not exist, no action needed
        except PermissionError:
            self.model.statusMsg(_(f"Warning! File: {fname} is locked. Could not be deleted."))

    def save(self):
        if self.adjfile is None:
            return False
        self.createAdjlist()
        self.createTriggerlist()
        # possibly loop through the poly-glot configs here and then call createChanges with 
        # the right diglot letter, L,R,A,B,C and appropriate chfile for the other config.
        chfile = self.adjfile.replace(".adj", "_changes.txt")
        # self.createChanges(chfile)
        res = self.changed
        self.changed = False
        return res

    def changeval(self, parref, doit, insert=False):
        if not isinstance(parref, str):
            r = self.liststore[parref]
            doit(r, parref)
            return
        m = refre.match(parref)
        if not m:
            return False
        cp = [m.group(1)+m.group(2), m.group(3), int((m.group(4) if m.lastindex > 2 else 1) or 1)]
        cpk = self.calckey(cp)
        i = -1
        # rk = self.calckey([cp[0], "200:200", 1, 0, "", 100])
        for i, r in enumerate(self.liststore):
            rk = self.calckey(r)
            if rk >= cpk:
                break
        else:
            i += 1
            rk = self.calckey([cp[0], "200:200", 1, 0, "", 100, ""])
        if rk == cpk:
            doit(r, i)
        elif rk > cpk:
            if insert:
            # book, c:v, para, stretch, mkr, expand, comment%
                r = [cp[0], cp[1], cp[2], "0", "", 100, ""]
                self.liststore.insert(i, r)
                r = self.liststore[i]         # since the row is turned into something else
                self.changed = True
                doit(r, i)

    def increment(self, parref, offset, mrk=None):
        def mydoit(r, i):
            v = r[3]
            mult = 1
            hasplus = "+" in v
            v = int(v.replace("+", ""))
            if v < 0:
                mult = -1
            v += offset
            if (v < 0 or v > 0) and hasplus:
                f = "+" + str(v)
            elif v == 0 and mult:
                f = ("+" if hasplus else "") + ("-" if mult < 0 else "") + "0"
            else:
                f = str(v)
            self.liststore.set_value(r.iter, 3, f)
            if mrk is not None and not self.liststore.get_value(r.iter, 4):
                self.liststore.set_value(r.iter, 4, mrk)
            self.changed = True
        self.changeval(parref, mydoit)

    def expand(self, parref, offset, mrk=None):
        def mydoit(r, i):
            v = r[5] + offset
            self.liststore.set_value(r.iter, 5, v)
            self.changed = True
            if mrk is not None and not self.liststore.get_value(r.iter, 4):
                self.liststore.set_value(i, 4, mrk)
        self.changeval(parref, mydoit)

    def getinfo(self, parref, insert=False):
        """ returns (stretch:str, expand:int, adj line no:int) """
        res = []
        def mydoit(r, i):
            res.append(r[3])
            res.append(r[5])
            res.append(r.iter)
        self.changeval(parref, mydoit, insert=insert)
        return res

    def _parseTriggersFromComment(self, comment):
        if not comment:
            return []
        return re.findall(r"(?:^|\s)trig=([^\s]+)", comment)

    def _setTriggersInComment(self, comment, triggers):
        # remove existing trig=... tokens, then append normalized list
        base = re.sub(r"(?:^|\s)trig=[^\s]+", "", comment or "").strip()
        trigPart = " ".join(f"trig={t}" for t in triggers)
        if base and trigPart:
            return base + " " + trigPart
        return base or trigPart

    def getTriggers(self, parref):
        res = []
        def mydoit(r, i):
            res.extend(self._parseTriggersFromComment(r[6]))
        self.changeval(parref, mydoit, insert=False)
        return res

    def addTrigger(self, parref, payload, enabled=True, insert=True):
        def mydoit(r, i):
            triggers = set(self._parseTriggersFromComment(r[6]))
            if payload is None:
                triggers.clear()
            elif enabled:
                triggers.add(payload)
            else:
                triggers.discard(payload)
            newComment = self._setTriggersInComment(r[6], sorted(triggers))
            if newComment != r[6]:
                self.liststore.set_value(r.iter, 6, newComment)
                self.changed = True
        self.changeval(parref, mydoit, insert=insert)