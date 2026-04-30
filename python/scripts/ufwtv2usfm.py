#!/usr/bin/env python3

import argparse, csv, re, os
from ptxprint.markdown import MarkdownToUSX
from ptxprint.utils import bookcodes
import usfmtc
from usfmtc.xmlutils import ParentElement

def process_article(text):
    md = MarkdownToUSX()
    text = text.replace("&", "...")
    root = md.compile(text)
    res = []
    key = ""
    collecting = False
    for r in root:
        s = r.get("style")
        if s in ("s", "s1"):
            title = r.text
            key = r.text.split(",", 1)[0]
        elif s == "s2":
            if r.text.strip().startswith("Definition"):
                collecting = True
            else:
                collecting = False
        elif collecting:
            res.append(r)
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

words = {}
with open(os.path.join(args.wordlinksdir, f"twl_{book}.tsv"), encoding="utf-8") as inf:
    reader = csv.DictReader(inf, delimiter="\t")
    for r in reader:
        words.setdefault(r['Reference'], []).append(r)

mainroot = ParentElement("usx")
def addel(tag, style):
    el = ParentElement(tag, parent=mainroot)
    if style is not None:
        el.set("style", style)
    mainroot.append(el)
    return el

def addkey(el, istext, key):
    t = el.text if istext else el.tail
    if t is None:
        return
    for w in words.get(key, []):
        if w.get('used', False):
            continue
        if w['GLQuote'] in t:
            i = t.find(w['GLQuote'])
            kid = re.sub(r"^.*/", "", w['TWLink'])
            w['used'] = True
            if i == 0 and len(w['GLQuote']) == len(t):
                el.set('style', "w")
                el.set('lemma', kid)
            else:
                pel = el if istext else el.parent
                wel = ParentElement("char", parent=pel, attrib={"style": "w", "lemma": kid})
                j = -1 if istext else pel.index(el)
                pel.insert(j+1, wel)
                wel.text = w['GLQuote']
                wel.tail = t[i+len(w['GLQuote']):]
                if istext:
                    el.text = el.text[:i]
                else:
                    el.tail = el.tail[:i]
            break

def addkeys(el, verse, chap):
    k = f"{chap}:{verse}"
    #if k == "1:3":
    #    breakpoint()
    addkey(el, True, k)
    for c in el:
        addkeys(c, verse, chap)
    addkey(el, False, k)

def usfmtxt(el):
    return usfmtc.USX(el).outUsfm(None, book=args.book, version=[3, 1])

b = addel("book", "id")
b.set("code", args.book)
h = addel("para", "h")
h.text = args.book

md = MarkdownToUSX()
typemap = md.typemap.copy()
typemap['paragraph'] = lambda t: ("char", "fp")
md.typemap = typemap
mdp = MarkdownToUSX()

def create_triggers(notes):
    # Create trigger file
    lastchap = 0
    lastverse = 0
    lastextra = ""
    results = []
    efel = None
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
        extra = m.group(3)
        root = md.compile(t)
        r = root[1:]
        if chap != lastchap:
            c = addel("chapter", "c")
            c.set("number", str(chap))
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
            if len(r) < 2 and l['TATitle']:
                elj = ParentElement("char", parent=r[-1], attrib={"style": "jmp", "href": na})
                elj.text = l['TATitle']
                if len(r[0]):
                    r[0][-1].tail = (r[0][-1].tail or "") + " \u2192"
                else:
                    r[0].text = (r[0].text or "") + " \u2192"
                r[0].append(elj)
            r = r[1:] if len(r) > 1 else []
        if newv:
            if len(results):
                results.append("\\EndTrigger\n")
            if verse != "intro":
                results.append(rf"\AddTrigger {args.book}{chap}.{verse}-preverse")
        if verse == "intro":
            root = mdp.compile(t)
            esbel = ParentElement("sidebar", attrib={"style": "esb", "category": "chapintro"})
            for e in root[1:]:
                e.parent = esbel
                esbel.append(e)
            results.append(rf"\AddTrigger {args.book}{chap}.1-preverse")
            results.append(usfmtxt(esbel))
            efel = None
        else:
            for e in r:
                e.parent = efel
                efel.append(e)
        if l['TATitle'] and len(r):
            elj = ParentElement("char", parent=r[-1], attrib={"style": "jmp", "href": na})
            elj.text = l['TATitle']
            if len(r[-1]):
                r[-1][-1].tail = (r[-1][-1].tail or "") + " \u2192"
            else:
                r[-1].text = (r[-1].text or "") + " \u2192"
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
ofile = bookcodes[book]+book+prj+'-'+args.config+digextra+".USFM.triggers"
with open(os.path.join(cfgdir, "triggers", ofile), "w", encoding="utf-8") as outf:
    outf.write("\n".join(results))

def create_changes(words, cfgdir):
    # Create Changes
    articles = set()
    f = "x" if args.xref else "f"
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
                    extra = f'\\\\{f} - \\\\{f}q \\1 \\\\{f}t \u2192{t}\\\\{f}*'
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
    # Create GLO
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
    # Create XXA articles file
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
                elj = ParentElement("char", parent=r, attrib={"style": "jmp", "id": a})
                elj.tail = r.text
                r.text = None
                r.insert(0, elj)
    return xxa

xxa = create_xxa(notearticles)
xfname = os.path.join(args.projectdir, f"94XXA{prj}.USFM")
xxa.saveAs(xfname)

def create_intro(notes):
    # Create intro INT
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
    intfname = os.path.join(args.projectdir, f"A7INT{prj}.USFM")
    intdoc.saveAs(intfname)
