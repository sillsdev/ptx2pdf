
from ptxprint.utils import refKey
from collections import UserList
import os,re
import logging

logger = logging.getLogger(__name__)

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
        

adjre = re.compile(r"^(\S{3})([A-Z]?)\s*(\d+[.:]\d+(?:[+-]*\d+)?|\S+)\s+([+-]?\d+)(?:\[(\d+)\])?")
refre = re.compile(r"^(\S{3})([A-Z]?)\s*(\d+[.:]\d+(?:[+-]*\d+)?|\S+)(?:\[(\d+)\])?")
restre = re.compile(r"^\s*(?:(?:mrk=|\\)(\S+)\s*)?(?:(?:expand=)?(\d+))?(.*?)$")


class AdjList:
    def __init__(self, centre, lowdiff, highdiff, diglotorder=[], gtk=None, fname=None, tname=None):
        self.lowdiff = lowdiff
        self.highdiff = highdiff
        self.centre = centre

        # book, c:v, para:int, stretch, mkr, expand:int, params, comment%
        if gtk is None:
            self.liststore = Liststore()
        else:
            self.liststore = gtk.ListStore(str, str, int, str, str, int, str, str)
        self.changed = False
        self.adjfile = fname
        self.trigfile = tname
        self.ftime = None
        self.db = []

    def clear(self):
        self.liststore.clear()
        self.db = []

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
        alldb = self.db[:]
        self.liststore.clear()
        for a in sorted(range(len(allvals)), key=lambda x:self.calckey(allvals[x])):
            self.liststore.append(allvals[a])
            self.db.append(alldb[a])

    def setval(self, bk, cv, para, stretch, mkr, expand=None, append=False, force=False, comment="", **kw):
        dstr = " ".join("{}={}".format(k, v) for k, v in kw.items())
        row = [bk, cv, para, stretch, mkr, expand or self.centre, dstr, comment]
        if append:
            self.liststore.append(row)
            self.db.append(kw)
            return
        i = self.find(bk, cv, para)
        if isinstance(i, int):
            if i >= 0:
                self.liststore.insert(i, row=row)
                self.db.insert(i, kw)
            else:
                self.liststore.append(row)
                self.db.append(kw)
        elif not force:       # got an iterator
            for j, k in enumerate(i):
                if row[j] != k:
                    self.liststore.set_value(i.iter, j, row[j])
        else:
            self.liststore[i.iter] = row
            self.db[i.iter] = comment

    def calckey(self, row):
        k = refKey("{0} {1}".format(*row))
        res = k[:3] + (k[5], row[2], k[3], k[4])
        return res

    def parseline(self, l, lineno=0):
        c = ""
        if '%' in l:
            c = l[l.find("%")+1:].strip()
            l = l[:l.find("%")]
        m = adjre.match(l)
        val = None
        if m:
            try:
                val = [m.group(1)+m.group(2), m.group(3), int(m.group(5) or 1),
                                m.group(4), None, self.centre, "", c]
            except ValueError:
                val = None
            dbval = {}
            if val is not None:
                bits = re.split(r"\s*(\S+\s*=\s*\S+)\s*", c)
                if bits is not None and len(bits):
                    rest = " ".join(bits[0::2])
                    val[7] = rest
                    for b in bits[1::2]:
                        (k, v) = (s.strip() for s in b.split("="))
                        if k == "expand":
                            val[5] = int(v)
                        elif k == "mrk":
                            val[4] = v
                        else:
                            dbval[k] = v
                    val[6] = " ".join(f"{k}={v}" for k, v in dbval.items())
            logger.log(7, f"{lineno}: {val}, {dbval}")
        return val, dbval

    def readAdjlist(self, fname):
        self.adjfile = fname
        allvals = []
        dbvals = []
        self.liststore.clear()
        with open(fname, "r", encoding="utf-8") as inf:
            for i,l in enumerate(inf.readlines()):
                val, dbval = self.parseline(l, lineno=i+1)
                if val is not None:
                    allvals.append(val)
                    dbvals.append(dbval)
        for a in sorted(range(len(allvals)), key=lambda x:self.calckey(allvals[x])):
            self.liststore.append(allvals[a])
            self.db.append(dbvals[a])
        self.ftime = os.lstat(fname).st_ctime

    def genline(self, i):
        r = self.liststore[i]
        d = self.db[i]
        cv = r[1].replace(":", ".").replace(" ", "")
        if r[2] > 1:
            line = "{0[0]} {1} {0[3]}[{0[2]}]".format(r, cv)
        else:
            line = "{0[0]} {1} {0[3]}".format(r, cv)

        extras = []
        if r[4]:
            extras.append(f"mrk={r[4]}")
        if r[5] != self.centre:
            extras.append(f"expand={r[5]}")
        for k, v in d.items():
            extras.append(f"{k}={v}")
        if r[7]:
            extras.append(r[7].strip())

        if extras:
            line += " % " + " ".join(extras)
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
            for i in range(len(self.liststore)):
                line = self.genline(i)
                outf.write(line + "\n")
        self.ftime = os.lstat(fname).st_ctime

    def _createUIExtensionLines(self, i):
        r = self.liststore[i]
        d = self.db[i]
        ref = rf"{r[0]}{r[1]}={r[2]}"
        triggerItems = []

        if r[5] != self.centre:
            triggerItems.append(rf"\zexp {r[5]}\*")

        triggeritems = self._getTriggersFromRow(i)

        if not triggerItems:
            return []

        res = ["", rf"\AddTrigger {ref}"]
        res.extend(triggerItems)
        res.append(r"\EndTrigger")
        return res

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
            for i in range(len(self.liststore)):
                lines = self._createUIExtensionLines(i)
                if lines:
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
                r = [cp[0], cp[1], cp[2], "0", "", 100, "", ""]
                self.liststore.insert(i, r)
                self.db.insert(i, {})
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

    def get_params(self):
        res = {}
        for r in self.liststore:
            # book, c:v, para:int, stretch, mkr, expand:int, comment%
            rk = f"{r[0]}{r[1].replace(':', '.')}[{r[2]}]"
            res[rk] = (r[5]/100, int(r[3]))
        return res

    def get_cache(self):
        shapes = {}
        probes = {}
        found = set()
        ckeyre = re.compile(r"([pm])(\d)")
        cvalre = re.compile(r"(\d+)([+-]\d+)?")
        for i, r in enumerate(self.liststore):
            rk = f"{r[0]}{r[1].replace(':', '.')}[{r[2]}]"
            for k, v in self.db[i].items():
                if (m := ckeyre.match(k)) is None: continue
                d = int(m.group(2)) if m.group(1) == "p" else -int(m.group(2))
                n = cvalre.match(v)
                if n is None: continue
                e = int(n.group(1)) / 100
                s = int(n.group(2)) if n.group(2) else 0
                shapes[(rk, d)] = (e, s)
                probes[(rk, e, s)] = d
        return shapes, probes

    def _setTriggersInComment(self, key, comment, triggers):

        # remove existing trig=... tokens, then append normalized list
        base = re.sub(rf"(?:^|\s){key}=[^\s]+", "", comment or "").strip()
        trigPart = " ".join(f"{key}={t}" for t in triggers)
        if base and trigPart:
            return base + " " + trigPart
        return base or trigPart

    def _getTriggersFromRow(self, i):
        d = self.db[i]
        return [v if v.startswith("\\") else "\\"+v for k, v in d.items() if k.startswith("trig")]

    def getTriggers(self, parref, key="trig"):
        res = []
        def mydoit(r, i):
            return self._getTriggersFromRow(i)
        self.changeval(parref, mydoit, insert=False)
        return res

    def addTrigger(self, parref, content, append=True, enabled=True, insert=True, key="trig"):
        def mydoit(r, i):
            if append:
                triggers = set(self._getTriggersFromRow(i))
            else:
                triggers = set()
            l = len(triggers)
            if content is None:
                triggers.clear()
            elif isinstance(content, (list, tuple)):
                if enabled:
                    triggers.update(content)
                else:
                    triggers.difference_update(content)
            elif enabled:
                triggers.add(content)
            else:
                triggers.discard(content)
            if len(triggers) != l:
                for k, v in list(self.db[i].items()):
                    if k.startswith(key):
                        del self.db[k]
                for j, t in enumerated(sorted(triggers)):
                    k = key if j == 0 else key+str(j)
                    self.db[i][k] = t
                r[6] = " ".join(f"{k}={v}" for k, v in self.db[i].items())
                self.changed = True
        self.changeval(parref, mydoit, insert=insert)

    def setdb(self, parref, key, value, insert=True):
        def mydoit(r, i):
            d = self.db[i]
            if key in d and value is None:
                del d[key]
            elif value is not None:
                d[key] = value
            r[6] = " ".join(f"{k}={v}" for k, v in d.items())
        self.changeval(parref, mydoit, insert=insert)

