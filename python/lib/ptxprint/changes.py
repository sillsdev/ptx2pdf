
import re, os
import regex
from ptxprint.utils import universalopen
from usfmtc.reference import RefList
from functools import reduce
import logging

logger = logging.getLogger(__name__)


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

def readChanges(fname, bk, passes=None, get_usfm=None, doError=printError):
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
            pass
        if usfm is not None:
            usfm.addorncv()
    qreg = r'(?:"((?:[^"\\]|\\.)*?)"|' + r"'((?:[^'\\]|\\.)*?)')"
    with universalopen(fname) as inf:
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
                lchs = readChanges(os.path.join(os.path.dirname(fname), m.group(2)), bk, passes=passes, get_usfm=get_usfm)
                for k, v in lchs.items():
                    changes.setdefault(k, []).extend(v)
                continue
            # test for "at" command
            m = re.match(r"^\s*at\s+(.*?)\s+(?=in|['\"])", l)
            if m:
                try:
                    atref = RefList(m.group(1), strict=False)
                except SyntaxError as e:
                    atref = []
                    atcontexts = [None]
                    doError("at reference error: {} in changes file at line {}".format(str(e), i+1))
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
                    contexts.append(regex.compile(m.group(1) or m.group(2), flags=regex.M))
                except re.error as e:
                    doError("Regular expression error: {} in changes file at line {}".format(str(e), i+1))
                    break
                l = l[m.end():].strip()
            # capture the actual change
            m = re.match(r"^"+qreg+r"\s*>\s*"+qreg, l)
            if m:
                try:
                    r = regex.compile(m.group(1) or m.group(2), flags=regex.M)
                    # t = regex.template(m.group(3) or m.group(4) or "")
                except (re.error, regex._regex_core.error) as e:
                    doError("Regular expression error: {} in changes file at line {}".format(str(e), i+1))
                    continue
                for at in atcontexts:
                    if at is None:
                        context = make_contextsfn(None, *contexts) if len(contexts) else None
                    elif len(contexts) or at[1] is not None:
                        context = make_contextsfn(at[0], at[1], *contexts)
                    else:
                        context = at[0]
                    ch = (context, r, m.group(3) or m.group(4) or "", f"{fname} line {i+1}")
                    for p in passes:
                        changes.setdefault(p, []).append(ch)
                    logger.log(7, f"{context=} {r=} {m.groups()=}")
                continue
            elif len(l):
                logger.warning(f"Faulty change line found in {fname} at line {i}:\n{l}")
    return changes
