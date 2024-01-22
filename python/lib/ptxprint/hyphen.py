import re, os
from ptxprint.utils import universalopen, runChanges

def generateHyphenationFile(view, prjid, prjdir, inbooks=False, addsyls=False, strict=False):
    listlimit = 63929
    infname = os.path.join(prjdir, 'hyphenatedWords.txt')
    outfname = os.path.join(prjdir, "shared", "ptxprint", 'hyphen-{}.tex'.format(prjid))
    hyphenatedWords = []
    if not os.path.exists(infname):
        m1 = _("Failed to Generate Hyphenation List")
        m2 = _("{} Paratext Project's Hyphenation file not found:\n{}").format(prjid, infname)
        return (m1, m2)
    z = 0
    m2b = ""
    m2c = ""
    m2d = ""
    nohyphendata = []
    with universalopen(infname) as inf:
        for l in inf.readlines()[8:]: # Skip over the Paratext header lines
            l = l.strip().replace(u"\uFEFF", "")
            l = re.sub(r"[*\",;:!?']", "", l) # to be continued...
            l = re.sub(r"-", "\u2010", l)
            l = re.sub(r"=", "-", l)
            # Paratext doesn't seem to allow segments of 1 character to be hyphenated  (for example: a-shame-d) 
            # (so there's nothing to filter them out, because they don't seem to exist!)
            # Also need to strip out words with punctuation chars (eg. Burmese \u104C .. \u104F)
            if strict and not l.startswith("*"):
                continue
            if "-" in l:
                if regex.search(r'[^\p{L}\p{M}\-]', l):
                    z += 1
                else:
                    if l[0] != "-" and len(l) > 5:
                        hyphenatedWords.append(l)
            elif "\u2010" not in l:
                lng = len(l)
                if lng > 9:
                    nohyphendata.append(l)
    snippet = view.getScriptSnippet()
    scriptregs = snippet.regexes(view)
    c = len(hyphenatedWords)
    if c >= listlimit or len(scriptregs) or inbooks:
        hyphwords = set([x.replace("-", "") for x in hyphenatedWords])
        acc = {}
        usfms = view.get_usfms()
        for bk in view.getBooks():
            u = view.get_usfm(bk)
            if u is None:
                continue
            u.getwords(init=acc)
        if inbooks: # cut the list down to only include words that are actually in the text
            hyphenatedWords = [w for w in hyphenatedWords if w.replace("-","") in acc]
            c = len(hyphenatedWords)
        if c >= listlimit:
            hyphcounts = {k:acc.get(k.replace("-",""), 0) for k in hyphenatedWords}
            hyphenatedWords = [k for k, v in sorted(hyphcounts.items(), key = lambda x: (-x[1], -len(x[0])))][:listlimit]
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
                if regex.search(r'[^\p{L}\p{M}\-]', w):
                    z += 1
                    continue
                a = runChanges(scriptregs, None, w)
                if len(a) == len(w):
                    continue
                moreWords.append(re.sub("[\u00AD\u200B]", "-", a))
                if len(moreWords) + c >= listlimit:
                    break
            moreWords.sort(key=len, reverse=True)
            hyphenatedWords.extend(moreWords)
            m2b = _("\n{} additional words were added using syllable-based rules.").format(len(moreWords)) + \
                    _("\nResulting in a total of {} words in the hyphenation list.").format(len(hyphenatedWords))
            
    # hyphenatedWords.sort(key = lambda s: s.casefold())
    outlist = '\\catcode"200C=12\n\\catcode"200D=12\n\\hyphenation{\n' + "\n".join(hyphenatedWords) + "\n}"
    with open(outfname, "w", encoding="utf-8") as outf:
        outf.write(outlist)
    if len(hyphenatedWords) > 1:
        m1 = _("Hyphenation List Generated")
        m2a = _("{} words were gathered from Paratext's hyphenation word list.").format(c)
        if z > 0:
            m2c = _("\n\nNote: {} words containing non-Letters and non-Marks").format(z) + \
                    _("\n(ZWJ, ZWNJ, etc.) have not been included in the hyphenation list.")
        m2 = m2a + m2b + m2c
    else:
        m1 = _("Hyphenation List was NOT Generated")
        m2 = _("No valid words were found in Paratext's Hyphenation List")
    return (m1, m2)

