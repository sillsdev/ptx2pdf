#!/usr/bin/env python3
# ufwtv2usfm.py — Convert unfoldingWord (ufw) translation-help TSV files to PTXprint USFM outputs.
#
# DATA SOURCES
#   This script reads from the unfoldingWord translation-helps repositories:
#     - Translation Notes  (tn_BOOK.tsv):  columns Reference, SupportReference, GLQuote, Note, TATitle
#     - Translation Words Links (twl_BOOK.tsv):  columns Reference, GLQuote, TWTitle, TWLink
#     - Translation Words definitions (--wordsdir):  one markdown file per term under bible/<cat>/<term>.md
#     - Translation Academy articles (--articles):  one directory per article with title.md and 01.md
#
# OUTPUTS (all written relative to --projectdir / shared / ptxprint / --config)
#   triggers/<num>BOOK<prj>-<cfg>[-diglot].USFM.triggers
#       PTXprint trigger file; adds \ef extended-footnote notes before each annotated verse.
#   changes.txt
#       PTXprint regex changes; wraps key terms in \w...\w* markers and optionally adds footnotes.
#   <projectdir>/A9GLO<prj>.USFM
#       Glossary book (book code GLO) with word definitions drawn from TW markdown files.
#   <projectdir>/94XXA<prj>.USFM
#       Auxiliary book (code XXA) with Translation Academy article text.
#   <projectdir>/A7INT<prj>.USFM  (only when a front:intro note is present)
#       Introduction book (code INT) built from the front:intro translation note.
#
# USAGE EXAMPLE
#   python ufwtv2usfm.py \
#       --book MAT --projectdir /path/to/ParatextProject \
#       --config Default \
#       --notesdir /path/to/en_tn/bible/mat \
#       --wordlinksdir /path/to/en_twl/bible/mat \
#       --wordsdir /path/to/en_tw \
#       --articles /path/to/en_ta/translate

import argparse, csv, re, os
from ptxprint.markdown import MarkdownToUSX
from ptxprint.utils import bookcodes
import usfmtc
from usfmtc.xmlutils import ParentElement

def process_article(text):
    """Convert one TW markdown word-definition file to a list of USX para elements.

    The markdown heading format is "Term Title, optional subtitle" on an s/s1 element.
    The portion before the first comma becomes the \k glossary key.
    Only paragraphs that appear under an s2 "Definition" section are kept.
    Returns (key_string, [para_elements]).
    """
    md = MarkdownToUSX()
    text = text.replace("&", "...")   # & is illegal in XML/USX; ufw sources may use it as literal
    root = md.compile(text)
    res = []
    key = ""
    collecting = False
    for r in root:
        s = r.get("style")
        if s in ("s", "s1"):
            title = r.text
            key = r.text.split(",", 1)[0]   # "Chief Priest, priests" → key="Chief Priest"
        elif s == "s2":
            collecting = r.text.strip().startswith("Definition")
        elif collecting:
            res.append(r)
    # Inject a \k char wrapping the key at the start of the first definition paragraph,
    # with any title remainder ("chief priest, …" → ", priests") as the char's tail.
    kel = ParentElement("char", parent=res[0], attrib={"style": "k"})
    kel.tail = title[len(key)+1:] + ": " + res[0].text
    res[0].text = None
    kel.text = key
    res[0].insert(0, kel)
    return key, res

parser = argparse.ArgumentParser()
parser.add_argument("-b","--book",default="UNK",help="Book code")
parser.add_argument("-p","--projectdir", help="Project directory")
parser.add_argument("-c","--config", help="Configuration")
parser.add_argument("-n","--notesdir", help="Directory of tn.tsv files")
parser.add_argument("-w","--wordlinksdir", help="Directory of twl.tsv files")
parser.add_argument("-W","--wordsdir", help="Word definitions dir")
parser.add_argument("-a","--articles", help="Articles dir")
parser.add_argument("-d","--dedup",action="store_true",help="Don't repeat see in the same verse")
parser.add_argument("-D","--diglot",action="store_true",help="Generate -diglot triggers")
parser.add_argument("-x","--xref",action="store_true",help="Generate xrefs rather than footnotes")
args = parser.parse_args()

prj = re.sub(r"^.*/", "", args.projectdir)

# --notesdir and --wordlinksdir default to each other when only one is supplied
if args.wordlinksdir is None:
    args.wordlinksdir = args.notesdir
if args.notesdir is None:
    args.notesdir = args.wordlinksdir

book = args.book.upper()
notes = []
with open(os.path.join(args.notesdir, f"tn_{book}.tsv"), encoding="utf-8") as inf:
    reader = csv.DictReader(inf, delimiter="\t")
    for r in reader:
        notes.append(r)

# words is keyed by "chap:verse" reference so addkey() can look up relevant terms per verse
words = {}
with open(os.path.join(args.wordlinksdir, f"twl_{book}.tsv"), encoding="utf-8") as inf:
    reader = csv.DictReader(inf, delimiter="\t")
    for r in reader:
        words.setdefault(r['Reference'], []).append(r)

# mainroot accumulates the chapter/verse structure used only by create_triggers()
# (not the final GLO/XXA/INT books, which build their own ParentElement trees)
mainroot = ParentElement("usx")
def addel(tag, style):
    el = ParentElement(tag, parent=mainroot)
    if style is not None:
        el.set("style", style)
    mainroot.append(el)
    return el

def addkey(el, istext, key):
    """Wrap the first occurrence of a TWL GLQuote inside el.text (istext=True) or el.tail
    (istext=False) with a \w char marker carrying the term's lemma attribute.

    If the entire text/tail IS the quote, the element itself is relabelled \w in-place.
    Otherwise the text is split: the prefix stays in el.text/tail, a new \w child is
    inserted containing the quote, and any suffix becomes its tail.
    Each TWL entry is marked 'used' after the first match to prevent double-tagging.
    """
    t = el.text if istext else el.tail
    if t is None:
        return
    for w in words.get(key, []):
        if w.get('used', False):
            continue
        if w['GLQuote'] in t:
            i = t.find(w['GLQuote'])
            kid = re.sub(r"^.*/", "", w['TWLink'])  # strip rc:// path, keep bare term id
            w['used'] = True
            if i == 0 and len(w['GLQuote']) == len(t):
                # Whole text is the quote — just relabel the element
                el.set('style', "w")
                el.set('lemma', kid)
            else:
                # Partial match: split text around the quote and insert a \w child
                pel = el if istext else el.parent
                wel = ParentElement("char", parent=pel, attrib={"style": "w", "lemma": kid})
                # When operating on el.text, j=-1 so insert(0,...) makes wel the first child.
                # When operating on el.tail, insert after el in the parent.
                j = -1 if istext else pel.index(el)
                pel.insert(j+1, wel)
                wel.text = w['GLQuote']
                wel.tail = t[i+len(w['GLQuote']):]
                if istext:
                    el.text = el.text[:i]
                else:
                    el.tail = el.tail[:i]
            break   # only tag the first matching term per element/verse

def addkeys(el, verse, chap):
    addkey(el, True, f"{chap}:{verse}")
    for c in el:
        addkeys(c, verse, chap)
    addkey(el, False, f"{chap}:{verse}")

def usfmtxt(el):
    return usfmtc.USX(el).outUsfm(None, book=args.book, version=[3, 1])

b = addel("book", "id")
b.set("code", args.book)
h = addel("para", "h")
h.text = args.book

# Two MarkdownToUSX instances: md is standard (paragraph→\p), mdp leaves defaults
# (used for intro sidebars where paragraph mapping stays as \ip via mdp)
md = MarkdownToUSX()
typemap = md.typemap.copy()
typemap['paragraph'] = lambda t: ("char", "fp")  # paragraphs inside notes become \fp
md.typemap = typemap
mdp = MarkdownToUSX()

def create_triggers(notes):
    """Build PTXprint pre-verse trigger USFM from the TN note rows.

    Each group of notes sharing the same chapter:verse is accumulated into a single
    \ef extended-footnote (efel). When the verse changes the buffered \ef is serialised
    and a new one started.  Intro notes (Reference == "N:intro") get \esb sidebar
    treatment instead of an \ef note.

    Returns (list_of_usfm_strings, set_of_SupportReference_article_ids).
    """
    lastchap = 0
    lastverse = 0
    lastextra = ""
    results = []
    efel = None         # buffered \ef element for the current verse; None between verses
    notearticles = set()
    for l in notes:
        cv = l['Reference']
        t = l['Note']
        t = t.replace("&", "...")
        t = t.replace("\\n", "\n")
        na = l['SupportReference'].replace("rc://*/ta/man/", "")
        notearticles.add(na)
        m = re.match(r"^(\d+):(\d+|intro)(.*)$", cv)
        if not m:
            continue
        chap = int(m.group(1))
        verse = m.group(2) if m.group(2) == "intro" else int(m.group(2))
        extra = m.group(3)  # extra disambiguator present in some references (e.g. "a", "b")
        root = md.compile(t)
        r = root[1:]    # skip the dummy \book element that compile() always prepends
        if chap != lastchap:
            c = addel("chapter", "c")
            c.set("number", str(chap))
        # Build the bold+jmp header: \bd\jmp{GLQuote}\jmp*\bd*: note text
        el = ParentElement("char", parent=r[0], attrib={"style": "bd"})
        elj = ParentElement("char", parent=el, attrib={"style": "jmp", "href": na})
        elj.text = l['GLQuote'].replace('&', '...')
        el.append(elj)
        el.tail = ": " + r[0].text
        r[0].text = None
        r[0].insert(0, el)
        newv = verse != lastverse or chap != lastchap
        newe = extra != lastextra
        if (newv or newe):
            # Flush the previous verse's buffered \ef before starting the new one
            if efel is not None:
                results.append(usfmtxt(efel))
            efel = ParentElement("note", attrib={"style": "ef", "caller": "-"})
            effr = ParentElement("char", parent=efel, attrib={"style": "fr"})
            effr.text = f"{chap}:{verse} "
            efel.append(effr)
            efft = ParentElement("char", parent=efel, attrib={"style": "ft"})
            efel.append(efft)
            efft.text = r[0].text
            for e in r[0]:
                e.parent = efft
                efft.append(e)
            # If only one paragraph and a TATitle exists, append an arrow+jmp link to TA
            if len(r) < 2 and l['TATitle']:
                elj = ParentElement("char", parent=r[-1], attrib={"style": "jmp", "href": na})
                elj.text = l['TATitle']
                if len(r[0]):
                    r[0][-1].tail = (r[0][-1].tail or "") + " →"
                else:
                    r[0].text = (r[0].text or "") + " →"
                r[0].append(elj)
            r = r[1:] if len(r) > 1 else []
        if newv:
            if len(results):
                results.append("\\EndTrigger\n")
            if verse != "intro":
                results.append(rf"\AddTrigger {args.book}{chap}.{verse}-preverse")
        if verse == "intro":
            # Intro notes become chapter-intro sidebars rather than \ef notes
            root = mdp.compile(t)
            esbel = ParentElement("sidebar", attrib={"style": "esb", "category": "chapintro"})
            for e in root[1:]:
                e.parent = esbel
                esbel.append(e)
            results.append(rf"\AddTrigger {args.book}{chap}.1-preverse")
            results.append(usfmtxt(esbel))
            efel = None
        else:
            # Append additional paragraphs of a multi-paragraph note to the current \ef
            for e in r:
                e.parent = efel
                efel.append(e)
        # Append TATitle arrow+link to the last paragraph when more than one paragraph
        if l['TATitle'] and len(r):
            elj = ParentElement("char", parent=r[-1], attrib={"style": "jmp", "href": na})
            elj.text = l['TATitle']
            if len(r[-1]):
                r[-1][-1].tail = (r[-1][-1].tail or "") + " →"
            else:
                r[-1].text = (r[-1].text or "") + " →"
            r[-1].append(elj)
        lastverse = verse
        lastchap = chap
        lastextra = extra

    if efel is not None:
        results.append(usfmtxt(efel))
    if len(results):
        results.append(r"\EndTrigger")
    return (results, notearticles)

results, notearticles = create_triggers(notes)
cfgdir = os.path.join(args.projectdir, "shared", "ptxprint", args.config)
os.makedirs(os.path.join(cfgdir, "triggers"), exist_ok=True)
digextra = "-diglot" if args.diglot else ""
# bookcodes maps 3-letter USFM book codes to their canonical 2-digit sort prefix (e.g. "MAT" → "40")
ofile = bookcodes[book]+book+prj+'-'+args.config+digextra+".USFM.triggers"
with open(os.path.join(cfgdir, "triggers", ofile), "w", encoding="utf-8") as outf:
    outf.write("\n".join(results))

def create_changes(words, cfgdir):
    """Write changes.txt with PTXprint regex rules that wrap key terms in \w markers.

    The line format is:
        at BOOK C:V '(GLQuote)' > '\\w \\1\\w*[footnote]'
    where \\1 is the regex back-reference to the captured quote.
    When the term title differs from the GL quote an inline footnote/xref citing the
    title is appended.  --dedup prevents the same term appearing twice in one verse.
    Returns the set of TWLink article paths referenced (used to build the GLO file).
    """
    articles = set()
    f = "x" if args.xref else "f"  # xref marker vs footnote marker
    with open(os.path.join(cfgdir, "changes.txt"), "w", encoding="utf-8") as outf:
        lastref = None
        for k, ws in words.items():
            for w in ws:
                if w['Reference'] != lastref:
                    usedset = set()
                lastref = w['Reference']
                if w['TWTitle'] in usedset:
                    continue
                t = re.sub(r'^([^,]+).*$', r'\1', w['TWTitle'] or "")
                if t != w['GLQuote'] and w['TWTitle'] not in usedset:
                    # Add an inline note pointing to the term's title in the TW definition
                    extra = f'\\\\{f} - \\\\{f}q \\1 \\\\{f}t →{t}\\\\{f}*'
                else:
                    extra = ''
                line = fr"at {book} {w['Reference']} '({w['GLQuote'].replace('&','.*?')})' > '\\w \1\\w*{extra}'"
                article = w['TWLink'].replace("rc://*/tw/dict/bible/", "")
                articles.add(article)
                outf.write(line + "\n")
                if args.dedup:
                    usedset.add(w['TWTitle'])
    return articles

articles = create_changes(words, cfgdir)

def create_glo(articles):
    """Build the GLO (Glossary) USFM book from TW word-definition markdown files.

    Articles are sorted by reversed path segments so that terms within a category
    sort together (e.g. kt/lord before kt/son rather than alphabetical by full path).
    The file is written to <projectdir>/A9GLO<prj>.USFM; the A9 prefix places it after
    the NT in Paratext's canonical book order.
    """
    root = ParentElement("usx")
    root.append(ParentElement("book", parent=root, attrib={"code": "GLO", "style": "id"}))
    glossary = usfmtc.USX(root)
    for a in sorted(articles, key=lambda s:list(reversed(s.split("/")))):
        path = os.path.join(args.wordsdir, "bible", a+".md")
        with open(path, encoding="utf-8") as inf:
            text = inf.read()
        (key, articleps) = process_article(text)
        for e in articleps:
            e.parent = root
            root.append(e)
    return glossary

glossary = create_glo(articles)
gfname = os.path.join(args.projectdir, f"A9GLO{prj}.USFM")
glossary.saveAs(gfname)

def create_xxa(notearticles):
    """Build the XXA auxiliary book from Translation Academy (TA) article directories.

    Each article directory is expected to contain title.md (plain text title) and
    01.md (the main article body in markdown).  A \jmp anchor with the article id is
    inserted at the start of the first paragraph so the content can be hyperlinked from
    \jmp refs in trigger notes.
    The file is written to <projectdir>/94XXA<prj>.USFM; 94 places it late in Paratext's
    canonical order.
    """
    root = ParentElement("usx")
    root.append(ParentElement("book", parent=root, attrib={"code": "XXA", "style": "id"}))
    xxa = usfmtc.USX(root)
    for a in sorted(notearticles, key=lambda s:list(reversed(s.split("/")))):
        basedir = os.path.join(args.articles, a)
        if not os.path.exists(basedir) or not os.path.exists(os.path.join(basedir, 'title.md')):
            continue
        with open(os.path.join(basedir, "title.md")) as inf:
            title = inf.read()
        with open(os.path.join(basedir, "01.md")) as inf:
            text = inf.read()
        text = text.replace("&", "...")
        md = MarkdownToUSX()
        ps = md.compile(text)
        titlel = ParentElement("para", parent=root, attrib={"style": "s2"})
        titlel.text = title.strip()
        root.append(titlel)
        for i, r in enumerate(ps[1:]):
            r.parent = root
            root.append(r)
            if i == 0:
                # Inject a \jmp anchor at the top of the first paragraph so \jmp href="..."
                # links from trigger notes can resolve to this article
                elj = ParentElement("char", parent=r, attrib={"style": "jmp", "id": a})
                elj.tail = r.text
                r.text = None
                r.insert(0, elj)
    return xxa

xxa = create_xxa(notearticles)
xfname = os.path.join(args.projectdir, f"94XXA{prj}.USFM")
xxa.saveAs(xfname)

def create_intro(notes):
    """Build an INT introduction book from the 'front:intro' translation note if present.

    Uses MarkdownToUSX in "intro" mode, which maps paragraph → \ip and heading → \is*.
    Returns the USX object, or None if no front:intro note exists in this book's TN file.
    """
    md = MarkdownToUSX(mode="intro")
    intdoc = None
    for l in notes:
        if l['Reference'] != 'front:intro':
            continue
        t = l['Note']
        t = t.replace("\\n", "\n")
        t = t.replace("&", "...")
        root = md.compile(t)
        intdoc = usfmtc.USX(root)
        break
    return intdoc

intdoc = create_intro(notes)
if intdoc is not None:
    # A7 places the INT book just before NT in Paratext's canonical book order
    intfname = os.path.join(args.projectdir, f"A7INT{prj}.USFM")
    intdoc.saveAs(intfname)
