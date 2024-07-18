import re, os, regex
from ptxprint.utils import universalopen, runChanges, _
import logging

logger = logging.getLogger(__name__)

class Hyphenation:

    listlimit = 63929

    @classmethod
    def fromPTXFile(cls, view, prjid, prjdir, inbooks=False, addsyls=False, strict=False, hyphen="\u2010"):
        infname = os.path.join(prjdir, 'hyphenatedWords.txt')
        outfname = os.path.join(prjdir, "shared", "ptxprint", 'hyphen-{}.tex'.format(prjid))
        hyphenatedWords = []
        if not os.path.exists(infname):
            self.m1 = _("Failed to Generate Hyphenation List")
            self.m2 = _("{} Paratext Project's Hyphenation file not found:\n{}").format(prjid, infname)
            return self
        z = 0
        m2b = ""
        m2c = ""
        m2d = ""
        nohyphendata = []
        with universalopen(infname) as inf:
            for l in inf.readlines()[8:]: # Skip over the Paratext header lines
                l = l.strip().replace(u"\uFEFF", "")
                l = re.sub(r"[\",;:!?']", "", l) # to be continued...
                l = re.sub(r"-", hyphen, l)
                l = re.sub(r"=", "-", l)
                # Paratext doesn't seem to allow segments of 1 character to be hyphenated  (for example: a-shame-d) 
                # (so there's nothing to filter them out, because they don't seem to exist!)
                # Also need to strip out words with punctuation chars (eg. Burmese \u104C .. \u104F)
                if strict and not l.startswith("*"):
                    continue
                l = l.lstrip("*")
                if "-" in l:
                    if regex.search('[^\\p{L}\\p{M}\\-\u2010\u2011]', l):
                        # print(f"Skipped: {l}")
                        z += 1
                    else:
                        if l[0] != "-" and len(l) > 5:
                            hyphenatedWords.append(l)
                elif len(l) > 9:
                    # print(f"No hyphen data for long word: {l}")
                    nohyphendata.append(l)
        snippet = view.getScriptSnippet()
        scriptregs = snippet.regexes(view)
        c = len(hyphenatedWords)
        if c >= cls.listlimit or len(scriptregs) or inbooks:
            hyphwords = set([x.replace("-", "") for x in hyphenatedWords])
            acc = {}
            usfms = view.get_usfms()
            for bk in view.getBooks():
                u = view.get_usfm(bk)
                if u is None:
                    continue
                u.getwords(init=acc, lowercase=True)
            if inbooks: # cut the list down to only include words that are actually in the text
                hyphenatedWords = [w for w in hyphenatedWords if w.replace("-","") in acc]
                c = len(hyphenatedWords)
                
            if c >= cls.listlimit:
                hyphcounts = {k:acc.get(k.replace("-",""), 0) for k in hyphenatedWords}
                hyphenatedWords = [k for k, v in sorted(hyphcounts.items(), key = lambda x: (-x[1], -len(x[0])))][:cls.listlimit]
                m2b = _("\n\nThat is too many for XeTeX! List truncated to longest {} words found in the active sources.").format(len(hyphenatedWords))
            elif addsyls and len(scriptregs):
                moreWords = []
                incnthyphwords = 0
                for w in sorted(acc.keys(), key=lambda x:-acc[x]):
                    if len(w) < 7:
                        continue
                    if w in hyphwords:
                        incnthyphwords += 1
                        continue
                    if regex.search('[^\\p{L}\\p{M}\\-\u2010\u2011]', w):
                        z += 1
                        continue
                    a = runChanges(scriptregs, None, w)
                    if len(a) == len(w):
                        continue
                    moreWords.append(re.sub("[\u00AD\u200B]", "-", a))
                    if len(moreWords) + c >= cls.listlimit:
                        break
                moreWords.sort(key=len, reverse=True)
                hyphenatedWords.extend(moreWords)
                m2b = _("\n{} additional words were added using syllable-based rules.").format(len(moreWords)) + \
                        _("\nResulting in a total of {} words in the hyphenation list.").format(len(hyphenatedWords))
        self = cls({x.lower().replace("-", ""): x for x in hyphenatedWords})
        self.analyse()
        self.outTeX(outfname)
        if len(hyphenatedWords) > 1:
            self.m1 = _("Hyphenation List Generated")
            m2a = _("{} words were gathered from Paratext's hyphenation word list.").format(c)
            if z > 0:
                m2c = _("\n\nNote: {} words containing non-Letters and non-Marks").format(z) + \
                        _("\n(ZWJ, ZWNJ, etc.) have not been included in the hyphenation list.")
            self.m2 = m2a + m2b + m2c
        else:
            self.m1 = _("Hyphenation List was NOT Generated")
            self.m2 = _("No valid words were found in Paratext's Hyphenation List")
        # print("Long words (len>9) with no hyhphenation points: ", len(nohyphendata))
        return self

    @classmethod
    def fromTeXFile(cls, prjid, prjdir):
        infname = os.path.join(prjdir, "shared", "ptxprint", 'hyphen-{}.tex'.format(prjid))
        if os.path.exists(infname):
            with universalopen(infname) as inf:
                hyphenatedWords = [l.strip() for l in inf.readlines() if len(l) and l[0] not in "\\{}"]
            self = cls({x.lower().replace("-", ""): x for x in hyphenatedWords})
            self.analyse()
        else:
            self = cls()
        return self

    def __init__(self, words=None):
        self.wordlist = words or {}
        self.has2010 = False
        self.has2011 = False
        self.chars = None

    def __len__(self):
        return len(self.wordlist)

    def __contains__(self, s):
        return s in self.wordlist

    def get(self, k, default=None):
        return self.wordlist.get(k, default)

    def analyse(self):
        self.calcChars()
        self.has2010 = "\u2010" in self.chars
        self.has2011 = "\u2011" in self.chars

    def get_hyphen_char(self):
        return "\u2010" if self.has2010 else "-"
            
    def outTeX(self, outfname):
        hyphenatedWords = sorted(self.wordlist.values(), key=lambda x:(-len(x), x))
        # hyphenatedWords.sort(key = lambda s: s.casefold())
        outlist = '\\catcode"200C=12\n\\catcode"200D=12\n\\hyphenation{\n' + "\n".join(hyphenatedWords) + "\n}"
        with open(outfname, "w", encoding="utf-8") as outf:
            outf.write(outlist)

    def calcChars(self):
        if self.chars is not None:
            return
        self.chars = set()
        for k in self.wordlist.keys():
            self.chars.update(k)
        self.splitre = re.compile(r"(?i)([^{}]+)".format("".join(sorted(self.chars))))

    def hyphenate(self, t, hyphenchar):
        t = t.replace("-", hyphenchar)
        bits = self.splitre.split(t)
        for i in range(0, len(bits), 2):
            s = bits[i].replace("-", hyphenchar)
            if s.lower() in hyph:
                h = self.get(s.lower()).lower()
                if s.lower() != s:
                    hbits = h.split("-")
                    hpos = list(accumulate([len(x) for x in hbits]))
                    r = [s[x:y] for x, y in zip([0] + hpos, hpos)]
                    bits[i] = "\u00AD".join(r)
                    logger.log(6,f"hyphenating {s} at {hpos} giving {'-'.join(r)}")
                else:
                    logger.log(6,f"hyphenating {s} giving {h}")
                    bits[i] = h.replace("-", "\u00AD")
            else:
                bits[i] = s
        return "".join(bits)


class Hunspell:

    def __init_(self, infile):
        from spylls.hunspell import Dictioanry
        if infile.lower().endswith(".zip"):
            self.dict = Dictionary.from_zip(infile)
        else:
            self.dict = Dictionary.from_files(infile)
        self.chars = None
        self.has2010 = False
        self.splitre = None

    def analyse(self):
        if self.chars is not None:
            return
        self.chars = set()
        for w in self.dict.dic.words:
            self.chars.update(w.stem)
        self.has2010 = "\u2010" in self.chars
        self.splitre = re.compile(r"(?i)([^{}]+)".format("".join(sorted(self.chars))))

    def get_hyphen_char(self):
        return "\u2010" if self.has2010 else "-"

    def hyphenate(self, t, hyphenchar):
        if hyphenchar != "-":
            t = t.replace("-", hyphenchar)
        bits = self.splitre.split(t)
        for i in range(0, len(bits), 2):
            bw = self.dict.lookuper.break_word(bits[i])
            bits[i] = max(bw, key=len)      # maximal breaking
        return "".join(bits)



