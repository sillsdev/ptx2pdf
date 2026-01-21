
import re, os
import regex
from usfmtc.reference import RefList
from functools import reduce
import logging

logger = logging.getLogger(__name__)

refmtfn = regex.compile(r"(?<!\\)\$([a-z]+)\{((?:(?R)|\\\}|[^}])*)\}|(?<!\\)\\(\d)")

functions = {
    "upper":    (1, lambda self,s:s.upper()),
    "lower":    (1, lambda self,s:s.lower()),
    "title":    (1, lambda self,s:s.title()),
    "v":        (1, lambda self,s:self.vars.get(s, "")),
    "set":      (2, lambda self,v,s:self.setvar(v, s))
}

def _procfn(self, m, p):
    if m.group(3):
        return p.group(int(m.group(3)))
    c = m.group(2)
    pc = refmtfn.sub(lambda x:_procfn(self, x, p), c)
    t = m.group(1)
    n, f = functions.get(t, (1, lambda s:s))
    if n > 1:
        b = regex.split(r"\s*,\s*", pc, n-1)
    else:
        b = [pc]
    return f(self, *b)

def complex_format(self, t, m):
    return refmtfn.sub(lambda x:_procfn(self, x, m), t)

class runChanges:
    def __init__(self, changes, dat, **kw):
        self.vars = {"bk": kw.get("bk", "")}
        self.res = self.run(changes, dat, **kw)

    def run(self, changes, dat, bk=None, errorfn=None):
        if dat is None:
            return dat
        def wrap(t, l):
            def proc(m):
                res = m.expand(t) if isinstance(t, str) else t(self, m)
                logger.log(5, "match({0},{1})={2}->{3} at {4}".format(m.start(), m.end(), m.string[m.start():m.end()], res, l))
                return res
            return proc
        for c in changes:
            if bk is not None:
                logger.debug("at {} Change: {}".format(bk, c))
            try:
                if c[0] is None:
                    dat = c[1].sub(wrap(c[2], c[3]), dat)
                elif isinstance(c[0], str):
                    if c[0] == bk:
                        dat = c[1].sub(wrap(c[2], c[3]), dat)
                else:
                    def simple(s):
                        return c[1].sub(wrap(c[2], c[3]), s)
                    dat = c[0](simple, bk, dat)
            except TypeError as e:
                raise TypeError(str(e) + "\n at "+c[3])
            except regex._regex_core.error as e:
                if errorfn is not None:
                    errorfn(str(e) + "\n at " + c[3])
        return dat

    def setvar(self, v, val):
        self.vars[v] = val
        return ""

def make_contextsfn(bk, *changes):
    # functional programmers eat your hearts out
    def makefn(reg, currfn):
        if currfn is not None:
            def compfn(fn, b, s):
                def domatch(m):
                    return currfn(lambda x:fn(m.group(0)), b, m.group(0))
                return reg.sub(domatch, s) if bk is None or b == bk else s
        else:
            def compfn(fn, b, s):
                return reg.sub(lambda m:fn(m.group(0)), s) if bk is None or b == bk else s
        return compfn
    return reduce(lambda currfn, are: makefn(are, currfn), reversed([c for c in changes if c is not None]), None)

def printError(msg, **kw):
    print(msg)

def _makecat_props(grammar):
    res = {}
    for m, c in grammar.marker_categories.items():
        res.setdefault(c, set()).add(m)
    for c, s in grammar.category_tags.items():
        res[c] = set().union(*[res[x] for x in s])
    res['table'] = res['cell'] | set(['tr'])
    return res

cats = {
    'para': r'[bdmqprs]|c[ld]|m[irs]|k[12]|l[fhi]|p[12bchim]|q[1234cdmr]|s[1234dpr]|cls|lit|nb|qa|sts|(?:li|lim|mi|ms|mte|ph|pi|qm|sd)[1234]?',
    'char': r'add|addpn|bd|bdit|bk|dc|efm|em|fm|fv|it|jmp|k|nd|ndx|no|ord|pn|png|pro|qt|rb|rq|sc|sig|sls|sup|tl|w|wg|wh',
    'header': r'ide|h|(?:h|toc|toca)[123]',
    'note': 'e?[fx]|fe|efe',
    'title': 'mt[1234]?',
    'intro': 'i(?:[bep]|m[iq]|o[rt]|p[iqr]|(?:mt[e]?|[oqs]|li|qis)[1234]?|ex|qt)',
    'table': 'tr|(?:t[hc][cr]?(?:[1-9]|10|11|12))'
}
def _convprop(m, cats):
    s = m.group(2)
    if cats is not None and (t := re.match(r"mkr\s*=\s*(.*?)\s*$", s)) is not None:
        curr = set()
        bits = re.split(r'([+-])', t.group(1))
        for i, b in enumerate(bits[::2]):
            g = cats.get(b.strip(), None)
            if g is None:
                continue
            if i == 0 or b[2*i-1] == '+':
                curr |= g
            else:
                curr -= g
        if len(curr):
            cr = "|".join(sorted(curr, key=lambda x:(-len(x), x)))
            if m.group(1) == "p":
                r = r"(?:\\(?:{}))".format(cr)
            else:
                r = r"(?:[^\\]|\\(?!{}))".format(cr)
        else:
            r = m.group(0)
    else:
        r = m.group(0)
    return r

propreg = re.compile(r"\\([pP])\{(.*?)\}")

def _transreg(s, cats):
    def _c(m):
        return _convprop(m, cats)
    s = propreg.sub(_c, s)
    return s

def _mkfmtfn(s):
    if not s:
        return s
    elif regex.search(r"(?<!\\)\$[a-z]+\{", s):
        return lambda x,m:complex_format(x, s, m)
    else:
        return s

def readChanges(fname, bk, passes=None, get_usfm=None, doError=printError, grammar=None):
    if grammar is not None:
        cats = _makecat_props(grammar)
    else:
        cats = None
    changes = {}
    if passes is None:
        passes = ["default"]
    if not os.path.exists(fname):
        return {}
    logger.debug("Reading changes file: "+fname)
    usfm = None
    if get_usfm and bk:
        try:
            usfm = get_usfm(bk)
        except SyntaxError:
            usfm = None
        if usfm is not None:
            usfm.addorncv()
    qreg = r'(?:"((?:[^"\\]|\\.)*?)"|' + r"'((?:[^'\\]|\\.)*?)')"
    with open(fname, encoding="utf-8", errors="replace") as inf:
        alllines = list(inf.readlines())
        i = 0
        while i < len(alllines):
            l = alllines[i].strip().replace(u"\uFEFF", "")
            i += 1
            while l.endswith("\\") and i < len(alllines):
                l = l[:-1] + alllines[i].strip()
                i += 1
            l = re.sub(r"\s*#.*$", "", l)
            if not len(l):
                continue
            contexts = []
            atcontexts = []
            m = re.match(r"^\s*sections\s*\((.*?)\)", l)
            if m:
                ts = m.group(1).split(",")
                passes = [t.strip(' \'"') for t in ts]  # don't require ""
                for p in passes:
                    if p not in changes:
                        changes[p] = []
                continue
            m = re.match(r"^\s*include\s+(['\"])(.*?)\1", l)
            if m:
                lchs = readChanges(os.path.join(os.path.dirname(fname), m.group(2)), bk,
                                passes=passes, doError=doError, get_usfm=get_usfm, grammar=grammar)
                for k, v in lchs.items():
                    changes.setdefault(k, []).extend(v)
                continue
            # test for "at" command
            m = re.match(r"^\s*at\s+(.*?)\s+(?=in|['\"])", l)
            if m:
                try:
                    atref = RefList(m.group(1), strict=False, single=False)
                except SyntaxError as e:
                    atref = []
                    atcontexts = [None]
                    doError("at reference error: {} in changes file at line {}: {}".format(str(e), i+1, l))
                for r in atref:
                    if getattr(r.first, 'chapter', None) in (None, 0):
                        atcontexts.append((r.book, None))
                        continue
                    for cr in r.allchaps():
                        if cr.first.verse is None:
                            atcontexts.append((r.book, regex.compile(r"(?<=\\c {}\D).*?(?=$|\\c\s)".format(r.chapter), flags=regex.S)))
                        elif cr.first.verse == 0:
                            atcontexts.append((r.book, regex.compile(r"(?<=\\c {}\D).*?(?=$|\\[cv]\s)".format(r.chapter), flags=regex.S)))
                        else:
                            for cv in r:
                                v = None
                                if cv.first != cv.last:
                                    v = cv
                                elif usfm is not None:
                                    v = usfm.bridges.get(cv, cv)
                                    if v.first == v.last:
                                        v = None
                                if v is None:
                                    outv = '{}{}'.format(cv.verse, cv.subverse or "")
                                else:
                                    outv = "{}{}-{}{}".format(v.first.verse, v.first.subverse or "", v.last.verse, v.last.subverse or "")
                                atcontexts.append((cv.book, regex.compile(r"\\c {}\D(?:[^\\]|\\(?!c\s))*?\K\\v {}\D.*?(?=$|\\[cv]\s)".format(cv.chapter, outv), flags=regex.S|regex.V1)))
                l = l[m.end():].strip()
            else:
                atcontexts = [None]
            # test for 1+ "in" commands
            while True:
                m = re.match(r"^\s*in\s+"+qreg+r"\s*:\s*", l)
                if not m:
                    break
                try:
                    contexts.append(regex.compile(m.group(1) or m.group(2), flags=regex.M | regex.S))
                except re.error as e:
                    doError("Regular expression error: {} in changes file at line {}: {}".format(str(e), i+1, l))
                    break
                l = l[m.end():].strip()
            # capture the actual change
            m = re.match(r"^"+qreg+r"\s*>\s*"+qreg, l)
            if m:
                s = _transreg(m.group(1) or m.group(2), cats)
                try:
                    r = regex.compile(s, flags=regex.M)
                    # t = regex.template(m.group(3) or m.group(4) or "")
                except (re.error, regex._regex_core.error) as e:
                    doError("Regular expression error: {} in changes file at line {}: {}".format(str(e), i+1, l))
                    continue
                for at in atcontexts:
                    if at is None:
                        context = make_contextsfn(None, *contexts) if len(contexts) else None
                    elif len(contexts) or at[1] is not None:
                        context = make_contextsfn(at[0], at[1], *contexts)
                    else:
                        context = at[0]
                    ch = (context, r, _mkfmtfn(m.group(3) or m.group(4)) or "", f"{fname} line {i+1}")
                    for p in passes:
                        changes.setdefault(p, []).append(ch)
                    logger.log(7, f"{context=} {r=} {m.groups()=}")
                continue
            elif len(l):
                logger.warning(f"Faulty change line found in {fname} at line {i}:\n{l}")
    return changes
