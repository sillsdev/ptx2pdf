#!/usr/bin/env python3
""" dbl2ptx: create a PTXprint archive from scripture text (typically a DBL bundle)
    and a base PTXprint configuration. All project specific settings (script,
    direction, font, size, linespacing, digits, title, copyright, books) are
    inferred from the source text and its metadata. No assumptions are made
    about script or direction. """

import argparse, os, sys, re, io, json, shutil, tempfile, logging, configparser
import unicodedata, urllib.request, urllib.parse
from zipfile import ZipFile, BadZipFile
from collections import Counter
from dataclasses import dataclass, field
import xml.etree.ElementTree as et
import regex

from ptxprint.dbl import readDBLMetadata, UnpackDBL, UnpackBundle, UnpackBooksDir, guessBookFile, BundleZip
from ptxprint.utils import bookcodes, allbooks
from ptxprint.unicode.ucd import get_ucd

logger = logging.getLogger("dbl2ptx")

LFF_LANG_URL = "https://lff.api.languagetechnology.org/lang/{}"
FAMILIES_URL = "https://raw.githubusercontent.com/silnrsi/fonts/main/families.json"

# Average base character height (in em) of ordinary Latin text set in a typical
# text font (Charis SIL measured over English scripture text). --textsize is
# interpreted as the point size Latin text would be set at, and other fonts and
# scripts are scaled so their average base character height matches.
REF_BASE_HEIGHT = 0.55

# Scripts that do not use spaces between words and need a line break locale
NOSPACE_SCRIPTS = {"Thai", "Laoo", "Khmr", "Mymr", "Lana", "Tavt", "Talu", "Tale", "Hani", "Hans", "Hant", "Jpan"}
# Scripts whose letters join, and so should also be measured in medial form
JOINING_SCRIPTS = {"Arab", "Aran", "Syrc", "Mong", "Nkoo", "Adlm", "Rohg", "Mand", "Phag"}

# Digit mappings available in ptx2pdf (src/mappings/<name>digits.*)
DIGIT_MAPPINGS = set("""adlam ahom arabic-indic balinese bengali bhaiksuki brahmi burmese chakma cham
    devanagari ethiopic extended-arabic fullwidth gujarati gunjala-gondi gurmukhi hanifi-rohingya
    hebrew javanese kannada kayah-li khmer khudawadi lao lepcha limbu malayalam masaram-gondi
    meetei-mayek modi mongolian mro myanmar myanmar-shan myanmar-tai-laing new-tai-lue newa nko
    nyiakeng-puachue-hmong ol-chiki oriya osmanya pahawh-hmong rumi saurashtra sharada sinhala-lith
    sora-sompeng sundanese tai-tham-hora tai-tham-tham takri tamil telugu thai tibetan tirhuta vai
    wancho warang-citi western-cham""".split())

# DBL language/numerals values to digit mappings (None = default European digits)
NUMERALS_MAP = {"arabic": None, "roman": None, "chinese": None, "farsi": "extended-arabic",
                "burmese": "myanmar", "eastern arabic": "arabic-indic", "arabic-indic": "arabic-indic"}

# Words that never form part of a title page; stripped from candidate titles
GENERIC_WORDS = set("""nt nt+ ot bible new testament protestant catholic common unicode dbl
    portions selections scripture scriptures edition version revised revision old""".split())


@dataclass
class TitleCandidate:
    text: str
    source: str
    forced: bool = False        # came from a title page or earlier config
    score: float = 0.
    script: float = 0.
    vocab: float = 0.


@dataclass
class ProjectInfo:
    prjid: str
    prjpath: str
    langtag: str = ""
    iso: str = ""
    script: str = ""
    direction: str = ""
    numerals: str = ""
    langname: str = ""
    autonym: str = ""
    books: list = field(default_factory=list)
    booknames: dict = field(default_factory=dict)       # bk: (long, short, abbr)
    copyright: str = ""
    rightsholder: str = ""
    fonthints: list = field(default_factory=list)       # [(family, source)]
    fontfeats: dict = field(default_factory=dict)       # family.casefold(): featstring
    titles: list = field(default_factory=list)          # [TitleCandidate]
    subtitles: list = field(default_factory=list)       # [TitleCandidate] forced subtitles
    basefont: str = None                                # body font family of the base config
    basefontdir: str = None                             # fonts that came with a base archive
    report: list = field(default_factory=list)

    def note(self, key, value, source):
        self.report.append((key, value, source))


@dataclass
class TextStats:
    clusters: Counter = field(default_factory=Counter)
    words: set = field(default_factory=set)
    digits: Counter = field(default_factory=Counter)
    scripts: Counter = field(default_factory=Counter)
    bidi: Counter = field(default_factory=Counter)
    bookorder: list = field(default_factory=list)
    tocs: dict = field(default_factory=dict)            # bk: [toc1, toc2, toc3]

    @property
    def mainscript(self):
        return self.scripts.most_common(1)[0][0] if len(self.scripts) else None

    def chars(self):
        res = Counter()
        for g, n in self.clusters.items():
            for c in g:
                res[c] += n
        return res


# ---------------------------------------------------------------------------
# Source import

def _innertext(e):
    return "".join(e.itertext()).strip() if e is not None else ""

def _statementText(el):
    """ Convert DBL copyright statementContent (html) into text with paragraph breaks """
    if el is None:
        return ""
    paras = []
    for p in el.iter('p'):
        bits = []
        def walk(e, top=False):
            if not top:
                if e.tag in ('em', 'i'):
                    bits.append("\\it ")
                elif e.tag in ('strong', 'b'):
                    bits.append("\\bf ")
                elif e.tag == 'br':
                    bits.append("\\\\ ")
            if e.text:
                bits.append(e.text)
            for c in e:
                walk(c)
                if c.tag in ('em', 'i'):
                    bits.append("\\it*")
                elif c.tag in ('strong', 'b'):
                    bits.append("\\bf*")
                if c.tail:
                    bits.append(c.tail)
        walk(p, top=True)
        t = re.sub(r"\s+", " ", "".join(bits)).strip()
        if t:
            paras.append(t)
    if not len(paras):
        paras = [re.sub(r"\s+", " ", _innertext(el))]
    return "\n".join(p for p in paras if p)

_titlemarkers = re.compile(r"^\\(mt\d?|mte\d?|periph|imt\d?)\b\s*(.*)$")

def titlesFromUsfm(text, source):
    """ Returns (maintitle, subtitle) candidates from the first title block in USFM text """
    lines = text.splitlines()
    block = []
    for l in lines:
        m = _titlemarkers.match(l.strip())
        if m is None:
            if len(block) and l.strip().startswith("\\") and not l.strip().startswith(("\\rem", "\\b ", "\\b\n")):
                break
            continue
        mk, txt = m.groups()
        if mk == "periph":
            if len(block):
                break
            continue
        txt = re.sub(r"\\\+?[a-z0-9]+\*?\s?", "", txt)
        txt = re.sub(r"\|[^\\]*", "", txt).strip()
        if txt:
            block.append((mk, txt))
    res = []
    main = None
    for i, (mk, txt) in enumerate(block):
        if mk in ("mt1", "mt"):
            main = i
            break
    if main is None:
        return res
    res.append(TitleCandidate(block[main][1], source, forced=True))
    subs = [t for mk, t in block[main+1:] if mk.startswith("mt")] + [t for mk, t in block[:main] if mk.startswith("mt")]
    if len(subs):
        res.append(TitleCandidate(subs[0], source + " (subtitle)", forced=True))
    return res

def _readCfgTitles(cfgtext, source):
    """ Reads [vars] maintitle and subtitle from a ptxprint.cfg text """
    cp = configparser.ConfigParser(interpolation=None)
    try:
        cp.read_string(cfgtext)
    except configparser.Error:
        return (None, None)
    mt = cp.get("vars", "maintitle", fallback="").strip()
    st = cp.get("vars", "subtitle", fallback="").strip()
    return (TitleCandidate(mt, source, forced=True) if mt else None,
            TitleCandidate(st, source, forced=True) if st else None)

class _ZipTree:
    """ Uniform access to a zip file or a directory tree """
    def __init__(self, zf=None, path=None):
        self.zf = zf
        self.path = path

    def names(self):
        if self.zf is not None:
            return self.zf.namelist()
        res = []
        for dp, dn, fn in os.walk(self.path):
            dn[:] = [d for d in dn if d not in ("local", ".git", ".hg")]
            for f in fn:
                res.append(os.path.relpath(os.path.join(dp, f), self.path).replace(os.sep, "/"))
        return res

    def read(self, name):
        if self.zf is not None:
            data = self.zf.read(name)
        else:
            with open(os.path.join(self.path, name), "rb") as inf:
                data = inf.read()
        for enc in ("utf-8-sig", "utf-16", "cp1252"):
            try:
                return data.decode(enc)
            except UnicodeDecodeError:
                pass
        return data.decode("utf-8", errors="replace")

def harvestProjectTree(tree, info, prefix=""):
    """ Gets title page and earlier ptxprint configuration information from a
        Paratext project (zipped or not) """
    names = tree.names()
    cfgs = []
    for n in names:
        if re.search(r"(^|/)shared/ptxprint/(?:[^/]+/)?ptxprint\.cfg$", n, re.I):
            cfgs.append(n)
    for n in cfgs:
        mt, st = _readCfgTitles(tree.read(n), prefix + n)
        if mt is not None:
            info.titles.append(mt)
        if st is not None:
            info.subtitles.append(st)
    for n in names:
        b = os.path.basename(n)
        if re.search(r"FRT", b, re.I) and b.lower().endswith((".sfm", ".usfm")) \
                or b.lower() == "frtlocal.sfm":
            for t in titlesFromUsfm(tree.read(n), prefix + n):
                (info.subtitles if t.source.endswith("(subtitle)") else info.titles).append(t)
    for n in names:
        if n.lower().endswith("settings.xml") and n.count("/") <= 1:
            try:
                doc = et.fromstring(tree.read(n).encode("utf-8"))
            except et.ParseError:
                continue
            fn = doc.findtext("FullName")
            if fn:
                info.titles.append(TitleCandidate(fn.strip(), prefix + "Settings/FullName"))
            df = doc.findtext("DefaultFont")
            if df:
                info.fonthints.append((df.strip(), prefix + "Settings/DefaultFont"))
            if not info.copyright and doc.findtext("Copyright"):
                info.copyright = doc.findtext("Copyright").strip()
            if not info.langtag and doc.findtext("LanguageIsoCode"):
                info.langtag = re.sub('-(?=-|$)', '', doc.findtext("LanguageIsoCode").replace(":", "-"))
            break

def infoFromDBL(dinfo, inzip, info):
    g = dinfo.get
    info.langtag = dinfo.langtag
    info.iso = dinfo.iso
    info.script = dinfo.scriptcode
    info.direction = dinfo.direction
    info.numerals = dinfo.numerals
    info.langname = dinfo.langname
    info.autonym = dinfo.langnameLocal
    info.books = [b for b, _ in dinfo.books if b in bookcodes]
    info.booknames = dict(dinfo.booknames)
    info.copyright = _statementText(dinfo.meta.find("copyright/fullStatement/statementContent"))
    info.rightsholder = g("agencies/rightsHolder/nameLocal") or g("agencies/rightsHolder/name")
    for k, v in (("language", info.langtag), ("script", info.script), ("direction", info.direction)):
        info.note(k, v, "metadata")
    pub = dinfo.meta.find('publications/publication[@default="true"]')
    if pub is None:
        pub = dinfo.meta.find('publications/publication')
    fields = []
    if pub is not None:
        fields.append(("pub/nameLocal", pub.findtext("nameLocal")))
    fields += [("id/nameLocal", g("identification/nameLocal")),
               ("id/descriptionLocal", g("identification/descriptionLocal"))]
    if pub is not None:
        fields += [("pub/descriptionLocal", pub.findtext("descriptionLocal")),
                   ("pub/name", pub.findtext("name"))]
    fields += [("id/description", g("identification/description")),
               ("id/name", g("identification/name")),
               ("id/abbreviationLocal", g("identification/abbreviationLocal"))]
    if pub is not None:
        fields.append(("pub/description", pub.findtext("description")))
    fields.append(("paratext/fullName", g('identification/systemId[@type="paratext"]/fullName')))
    for src, txt in fields:
        if txt and txt.strip():
            info.titles.append(TitleCandidate(txt.strip(), src))
    if dinfo.stylesfile is not None:
        try:
            st = et.fromstring(inzip.read(dinfo.stylesfile))
            ff = st.findtext('.//property[@name="font-family"]')
            if ff:
                info.fonthints.append((ff.strip(), "styles.xml"))
        except et.ParseError:
            pass
    if dinfo.sourcezip is not None:
        try:
            szf = ZipFile(io.BytesIO(inzip.read(dinfo.sourcezip)))
            harvestProjectTree(_ZipTree(zf=szf), info, prefix="source.zip:")
        except (BadZipFile, KeyError) as e:
            logger.warning(f"Can't read {dinfo.sourcezip}: {e}")

def importSource(src, projdir, prjid=None):
    """ Brings a DBL bundle, zipped project, project directory or directory of
        scripture files into projdir. Returns ProjectInfo. """
    info = None
    if os.path.isfile(src):
        with BundleZip(src) as inzip:
            dinfo = readDBLMetadata(inzip)
            if dinfo is not None:
                if prjid is None:
                    ltag = (dinfo.get("language/ldml") or dinfo.iso or "unk").split("-")[0]
                    prjid = ltag + (dinfo.get("identification/abbreviation") or "")
                    prjid = re.sub(r"[^A-Za-z0-9_]", "", prjid) or "DBL"
                info = ProjectInfo(prjid, os.path.join(projdir, prjid))
                infoFromDBL(dinfo, inzip, info)
                if not UnpackDBL(inzip, prjid, projdir, info=dinfo):
                    raise ValueError(f"Failed to unpack {src}")
            else:
                if prjid is None:
                    prjid = re.sub(r"[^A-Za-z0-9_]", "", os.path.splitext(os.path.basename(src))[0])
                info = ProjectInfo(prjid, os.path.join(projdir, prjid))
                harvestProjectTree(_ZipTree(zf=inzip), info)
        if dinfo is None and not UnpackBundle(src, prjid, projdir):
            raise ValueError(f"Failed to unpack {src}")
    elif os.path.isdir(src):
        if prjid is None:
            prjid = re.sub(r"[^A-Za-z0-9_]", "", os.path.basename(os.path.abspath(src)))
        info = ProjectInfo(prjid, os.path.join(projdir, prjid))
        harvestProjectTree(_ZipTree(path=src), info)
        if any(os.path.exists(os.path.join(src, f)) for f in ("Settings.xml", "ptxSettings.xml")):
            shutil.copytree(src, info.prjpath, ignore=shutil.ignore_patterns("local", ".git", ".hg", "*.bak"))
            # earlier configs are used for titles but must not leak into the output
            shutil.rmtree(os.path.join(info.prjpath, "shared", "ptxprint"), ignore_errors=True)
        elif not UnpackBooksDir(src, prjid, projdir):
            raise ValueError(f"No scripture files found in {src}")
    else:
        raise FileNotFoundError(src)
    _fillFromSettings(info)
    return info

def _fillFromSettings(info):
    """ Fill in gaps from the project's Settings and LDML """
    from ptxprint.ptsettings import ParatextSettings
    pts = ParatextSettings(info.prjpath)
    if not info.langtag:
        lt = pts.get("LanguageIsoCode", "")
        if lt:
            info.langtag = re.sub('-(?=-|$)', '', lt.replace(":", "-"))
        else:
            ldmls = [f for f in os.listdir(info.prjpath) if f.endswith(".ldml")]
            if len(ldmls) == 1:
                info.langtag = ldmls[0][:-5]
    if not info.iso and info.langtag:
        info.iso = info.langtag.split("-")[0]
    if not info.langname:
        info.langname = pts.get("Language", "")
    if not info.copyright:
        info.copyright = pts.get("Copyright", "")
    if not info.books:
        bp = pts.get("BooksPresent", "")
        info.books = [allbooks[i] for i, c in enumerate(bp) if c == "1" and i < len(allbooks)]
    if not info.booknames and getattr(pts, 'bookStrs', None):
        info.booknames = {k: tuple(v) for k, v in pts.bookStrs.items()}
    ldml = pts.ldml
    if ldml is not None:
        silns = "{urn://www.sil.org/ldml/0.1}"
        if not info.direction:
            d = ldml.findtext(".//layout/orientation/characterOrder")
            if d:
                info.direction = "rtl" if d.lower() == "right-to-left" else "ltr"
                info.note("direction", info.direction, "LDML")
        if not info.autonym and info.iso:
            for lang in ldml.findall(".//localeDisplayNames/languages/language"):
                if lang.get("type", "").split("-")[0].split("_")[0] == info.iso and lang.text:
                    info.autonym = lang.text.strip()
                    break
        fonts = ldml.findall('.//special/{0}external-resources/{0}font'.format(silns))
        for t in ("default", None):
            for f in fonts:
                if f.get('type', None) == t and f.get('name'):
                    info.fonthints.append((f.get('name'), "LDML"))
                    if f.get('features'):
                        info.fontfeats[f.get('name').casefold()] = f.get('features')


# ---------------------------------------------------------------------------
# Text analysis

def bookFiles(prjpath):
    res = {}
    for f in sorted(os.listdir(prjpath)):
        if not f.lower().endswith((".sfm", ".usfm")):
            continue
        bk, _ = guessBookFile(f)
        if bk is not None and bk in bookcodes and bk not in res:
            res[bk] = os.path.join(prjpath, f)
    return res

def analyseText(info):
    from ptxprint.usxutils import Usfm
    stats = TextStats()
    files = bookFiles(info.prjpath)
    order = [b for b in info.books if b in files] + sorted((b for b in files if b not in info.books),
                    key=lambda b: int(bookcodes.get(b, 999)) if str(bookcodes.get(b, "999")).isdigit() else 999)
    for bk in order:
        try:
            doc = Usfm.readfile(files[bk])
        except Exception as e:
            logger.warning(f"Failed to read {files[bk]}: {e}")
            continue
        if doc is None:
            continue
        stats.bookorder.append(bk)
        doc.collectClusters(stats.clusters, words=stats.words)
        root = doc.getroot()
        stats.tocs[bk] = [_innertext(root.find('.//para[@style="toc{}"]'.format(i))) for i in range(1, 4)]
        for e in root.iter():
            if e.tag in ("verse", "chapter"):
                for c in e.get("number", "") + e.get("pubnumber", ""):
                    if unicodedata.category(c) == "Nd":
                        stats.digits[c] += 1
    for g, n in stats.clusters.items():
        c = g[0]
        cat = unicodedata.category(c)
        if cat == "Nd":
            stats.digits[c] += n
        if cat.startswith("L") or cat.startswith("M"):
            sc = get_ucd(ord(c), "sc")
            if sc not in ("Zyyy", "Zinh", None):
                stats.scripts[sc] += n
            stats.bidi[unicodedata.bidirectional(c)] += n
    return stats

def digitMapping(stats, numerals=""):
    """ Returns the ptx2pdf digit mapping name needed to show chapter and verse
        numbers in the digits the text uses, or None for European digits """
    blocks = Counter()
    for c, n in stats.digits.items():
        if "0" <= c <= "9":
            blocks[None] += n
            continue
        try:
            name = unicodedata.name(c)
        except ValueError:
            continue
        m = re.match(r"^(.*?) DIGIT", name)
        if m is None:
            continue
        b = m.group(1).lower().replace(" ", "-")
        if b == "extended-arabic-indic":
            b = "extended-arabic"
        blocks[b] += n
    if len(blocks):
        best = blocks.most_common(1)[0][0]
        return (best if best in DIGIT_MAPPINGS else None), "text"
    if numerals:
        n = numerals.casefold()
        if n in NUMERALS_MAP:
            return NUMERALS_MAP[n], "metadata"
        n = n.replace(" ", "-")
        if n in DIGIT_MAPPINGS:
            return n, "metadata"
    return None, "default"


# ---------------------------------------------------------------------------
# Title selection

def _words(s):
    return [w.casefold() for w in regex.findall(r"\w+", s)]

def cleanTitle(txt, info):
    """ Returns a list of cleaned up candidate strings from a metadata field value """
    langnames = [x for x in (info.langname, info.autonym) if x]
    res = []
    parts = [txt]
    m = re.match(r"^([^:]{1,80}):\s*(.+)$", txt)
    if m:
        pre = m.group(1).casefold()
        if any(l.casefold() in pre or pre in l.casefold() for l in langnames):
            parts = [m.group(2)]        # "Language: title"
        else:                           # let scoring decide
            parts = [m.group(2), m.group(1), txt]
    for p in parts:
        p = re.sub(r"\s-[A-Z][^-]*$", "", p)               # -Papua New Guinea 2009 (DBL 2014)
        p = re.sub(r"\[[^\]]*\]", "", p)                    # [iso]
        p = re.sub(r"\((?:DBL|[^)]*\d{4})[^)]*\)", "", p)  # (DBL 2016)
        p = re.sub(r"_DBL\b|\bDBL\b|\bUnicode\b", "", p, flags=re.I)
        p = re.sub(r"\((?:New|Old) Testament\+?\)", "", p, flags=re.I)
        # strip trailing generic English tokens (NT, Bible, New Testament...)
        while True:
            q = re.sub(r"[\s,;:–—-]*(?:\bNT\+?|\bOT\b|\bBible\b|\bNew Testament\+?|\bPortions\b|\b\d{4}\b)\s*$", "", p, flags=re.I)
            if q == p:
                break
            p = q
        p = re.sub(r"\s+", " ", p).strip(" ,;:-–—")
        if p:
            res.append(p)
    return res

def scoreTitle(cand, stats, info):
    ws = _words(cand.text)
    if not len(ws):
        return 0.
    letters = [c for c in cand.text if unicodedata.category(c).startswith("L")]
    main = stats.mainscript
    if len(letters) and main:
        cand.script = sum(1 for c in letters if get_ucd(ord(c), "sc") == main) / len(letters)
    else:
        cand.script = 1. if not letters else 0.
    ws = [w for w in ws if not w.isdigit()]
    if not len(ws):
        cand.vocab = 0.
    else:
        cand.vocab = sum(1 for w in ws if w in stats.words) / len(ws)
    cand.score = cand.script * cand.vocab
    return cand.score

def _isLangName(txt, info):
    t = txt.casefold()
    for l in (info.langname, info.autonym):
        if l and t == l.casefold():
            return True
    ws = [w for w in _words(txt) if w not in GENERIC_WORDS]
    lw = set(w for l in (info.langname, info.autonym) if l for w in _words(l))
    return len(ws) > 0 and all(w in lw for w in ws)

def _similar(a, b):
    fa, fb = a.casefold(), b.casefold()
    if fa in fb or fb in fa:
        return True
    wa, wb = set(_words(a)), set(_words(b))
    if not len(wa) or not len(wb):
        return False
    return len(wa & wb) / min(len(wa), len(wb)) > 0.5

def chooseTitles(info, stats, threshold=0.6):
    """ Returns (maintitle, subtitle, candidates). Never returns English """
    cands = []
    seen = {}
    for c in info.titles:
        texts = [c.text] if c.forced else cleanTitle(c.text, info)
        for t in texts:
            if not c.forced and (_isLangName(t, info) or all(w in GENERIC_WORDS for w in _words(t))):
                continue
            k = t.casefold()
            if k in seen:
                # prefer mixed case variant
                old = seen[k]
                if old.text.isupper() and not t.isupper():
                    old.text = t
                continue
            n = TitleCandidate(t, c.source, forced=c.forced)
            scoreTitle(n, stats, info)
            seen[k] = n
            cands.append(n)
    forced = [c for c in cands if c.forced]
    vern = [c for c in cands if not c.forced and c.score >= threshold]
    maintitle = None
    if len(forced):
        maintitle = forced[0]
    elif len(vern):
        best = max(c.score for c in vern)
        tops = [c for c in vern if c.score >= best - 0.05]
        maintitle = tops[0]
        # prefer a longer candidate that contains this one
        for c in tops[1:]:
            if maintitle.text.casefold() in c.text.casefold():
                maintitle = c
                break
    subtitle = None
    if len(info.subtitles):
        subtitle = info.subtitles[0]
    elif maintitle is not None:
        for c in vern:
            if c is not maintitle and not _similar(c.text, maintitle.text):
                subtitle = c
                break
    if maintitle is None:
        aut = info.autonym
        maintitle = TitleCandidate(aut, "language autonym") if aut else None
    if subtitle is None:
        rng = bookRange(info, stats)
        if rng:
            subtitle = TitleCandidate(rng, "book range")
    return maintitle, subtitle, cands

def _shortname(bk, info, stats):
    bn = info.booknames.get(bk)
    if bn:
        for i in (1, 0, 2):
            if bn[i]:
                return bn[i]
    toc = stats.tocs.get(bk)
    if toc:
        for i in (1, 0, 2):
            if toc[i]:
                return toc[i]
    return None

def bookRange(info, stats):
    """ "first book – last book" using vernacular short names, ignoring peripherals """
    order = [b for b in (stats.bookorder or info.books) if b in bookcodes]
    canon = [b for b in order if b not in _peripherals]
    order = canon or order
    if not order:
        return None
    first = _shortname(order[0], info, stats)
    last = _shortname(order[-1], info, stats)
    if first is None:
        return None
    if len(order) == 1 or last is None or last == first:
        return first
    return "{} – {}".format(first, last)

_peripherals = set("FRT INT BAK OTH CNC GLO TDX NDX XXA XXB XXC XXD XXE XXF XXG".split())


# ---------------------------------------------------------------------------
# Fonts

def _fetchjson(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "ptxprint-dbl2ptx"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))

def _download(url, dest, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "ptxprint-dbl2ptx"})
    with urllib.request.urlopen(req, timeout=timeout) as resp, open(dest, "wb") as outf:
        shutil.copyfileobj(resp, outf)

def _normfam(s):
    return re.sub(r"[\s_-]", "", s or "").casefold()

class FontFinder:
    """ Finds font families via the Language Font Finder and SIL fonts data """
    def __init__(self, fetch=_fetchjson, download=_download):
        self.fetch = fetch
        self.download = download
        self._families = None

    def lang_families(self, langtag):
        """ Returns (defaultfamilies, {familyid: familyinfo}) for a language tag """
        tag = re.sub(r"-x-.*$", "", langtag or "")
        tags = []
        bits = tag.split("-")
        for i in range(len(bits), 0, -1):
            tags.append("-".join(bits[:i]))
        for t in tags:
            if not t or t == "und":
                continue
            try:
                res = self.fetch(LFF_LANG_URL.format(urllib.parse.quote(t)))
            except Exception as e:
                logger.info(f"Language font finder failed for {t}: {e}")
                continue
            if not isinstance(res, dict):
                continue
            fams = res.get("families", {}) or {}
            defs = res.get("defaultfamily", []) or []
            if isinstance(defs, str):
                defs = [defs]
            if len(fams) or len(defs):
                return defs, fams
        return [], {}

    def families(self):
        if self._families is None:
            try:
                self._families = self.fetch(FAMILIES_URL) or {}
            except Exception as e:
                logger.info(f"Failed to get font families list: {e}")
                self._families = {}
        return self._families

    def family(self, name):
        """ Returns family info for a family name or id """
        k = _normfam(name)
        fams = self.families()
        for fid, f in fams.items():
            if not isinstance(f, dict):
                continue
            if _normfam(fid) == k or _normfam(f.get("family")) == k:
                return f
        return None

    def fetch_family(self, finfo, destdir):
        """ Downloads regular, bold, italic, bold italic ttf files. Returns list of paths """
        files = finfo.get("files", {}) or {}
        want = {}
        for fname, fdata in files.items():
            if not fname.lower().endswith(".ttf") or not isinstance(fdata, dict):
                continue
            axes = fdata.get("axes", {}) or {}
            wght = axes.get("wght", 700 if re.search("bold", fname, re.I) else 400)
            ital = axes.get("ital", 1 if re.search("italic", fname, re.I) else 0)
            try:
                key = ("B" if float(wght) >= 600 else "R") + ("I" if float(ital) else "")
            except (TypeError, ValueError):
                continue
            if float(wght) not in (400, 700) and key in want:
                continue
            url = fdata.get("flourl") or fdata.get("url")
            if url:
                want[key] = (fname, url)
        res = []
        os.makedirs(destdir, exist_ok=True)
        for k, (fname, url) in sorted(want.items()):
            dest = os.path.join(destdir, fname)
            try:
                self.download(url, dest)
                res.append(dest)
            except Exception as e:
                logger.warning(f"Failed to download {url}: {e}")
        return res

def fontFamilyInfo(path):
    """ Returns (family, subfamily) of a font file """
    from fontTools.ttLib import TTFont as FTFont
    try:
        f = FTFont(path, fontNumber=0, lazy=True)
        n = f["name"]
        fam = n.getDebugName(16) or n.getDebugName(1)
        sub = n.getDebugName(17) or n.getDebugName(2)
        f.close()
        return fam, sub
    except Exception:
        return None, None

def fontCoverage(path, chars):
    """ Returns (fraction of character occurrences not covered, missing chars) """
    from fontTools.ttLib import TTFont as FTFont
    try:
        f = FTFont(path, fontNumber=0, lazy=True)
        cmap = f.getBestCmap() or {}
        f.close()
    except Exception:
        return 1., []
    total = 0
    missed = 0
    missing = []
    for c, n in chars.items():
        cat = unicodedata.category(c)
        if cat[0] in "ZC":              # spaces, controls, ZWJ etc.
            continue
        total += n
        if ord(c) not in cmap:
            missed += n
            missing.append(c)
    return (missed / total if total else 0.), missing

def _familyFiles(fontdir):
    """ Returns {family: {subfamily: path}} for the fonts in a directory """
    res = {}
    if not os.path.isdir(fontdir):
        return res
    for f in sorted(os.listdir(fontdir)):
        if not f.lower().endswith((".ttf", ".otf")):
            continue
        p = os.path.join(fontdir, f)
        fam, sub = fontFamilyInfo(p)
        if fam:
            res.setdefault(fam, {})[sub or "Regular"] = p
    return res

def _cachedRegular(fcache, name):
    """ Path to the regular face of a family in the ptxprint font cache. Fonts
        added from directories store the regular face under an empty style. """
    faces = fcache.cache.get(name, None) if hasattr(fcache, "cache") else None
    if faces is None:
        for k, v in getattr(fcache, "cache", {}).items():
            if _normfam(k) == _normfam(name):
                faces = v
                break
    if not faces:
        return None
    for k in ("Regular", "", "regular", "Book", "Roman", "Normal"):
        if faces.get(k):
            return faces[k]
    return None

def _regular(faces):
    for k in ("Regular", "Book", "Roman", "Normal"):
        if k in faces:
            return faces[k]
    return sorted(faces.items())[0][1]

def findFont(info, stats, fontdir, finder, forcefont=None, maxmissing=0.001):
    """ Returns (family, path to regular face, source) for the first candidate
        font that covers the text """
    from ptxprint.font import getfontcache
    chars = stats.chars()
    fcache = getfontcache()
    tried = set()

    def located(name):
        local = _familyFiles(fontdir)
        for fam, faces in local.items():
            if _normfam(fam) == _normfam(name):
                return fam, _regular(faces)
        fcache.wait()
        p = _cachedRegular(fcache, name)
        if p is not None:
            return name, p
        finfo = finder.family(name)
        if finfo is not None:
            if finder.fetch_family(finfo, fontdir):
                return located_local(name, finfo.get("family"))
        return None, None

    def located_local(*names):
        local = _familyFiles(fontdir)
        for name in names:
            for fam, faces in local.items():
                if _normfam(fam) == _normfam(name):
                    return fam, _regular(faces)
        return None, None

    def test(name, source):
        if not name or _normfam(name) in tried:
            return None
        tried.add(_normfam(name))
        fam, path = located(name)
        if path is None:
            logger.info(f"Font {name} ({source}) not found")
            return None
        miss, missing = fontCoverage(path, chars)
        if miss > maxmissing:
            logger.info(f"Font {name} ({source}) lacks {''.join(missing[:20])}")
            return None
        return (fam, path, source)

    cands = []
    if forcefont:
        cands.append((forcefont, "--font"))
    for fam in _familyFiles(fontdir).keys():
        cands.append((fam, "bundled font"))
    cands.extend(info.fonthints)
    for name, src in cands:
        r = test(name, src)
        if r is not None:
            return r
    defs, fams = finder.lang_families(info.langtag)
    order = list(defs) + [k for k in fams.keys() if k not in defs]
    for fid in order:
        finfo = fams.get(fid) if isinstance(fams, dict) else None
        name = (finfo or {}).get("family", fid)
        if _normfam(name) in tried:
            continue
        if finfo is not None and finfo.get("files"):
            local = located_local(name)
            if local[1] is None and _cachedRegular(fcache, name) is None:
                finder.fetch_family(finfo, fontdir)
        r = test(name, "language font finder")
        if r is not None:
            return r
    # last resort: the base configuration's own font, if it covers the text
    if info.basefont and _normfam(info.basefont) not in tried:
        if info.basefontdir:
            for fam, faces in _familyFiles(info.basefontdir).items():
                if _normfam(fam) == _normfam(info.basefont):
                    for p in faces.values():
                        shutil.copy(p, fontdir)
        r = test(info.basefont, "base configuration")
        if r is not None:
            return r
    return None


# ---------------------------------------------------------------------------
# Measurement

def _weighted_percentile(pairs, pct):
    """ pairs is [(value, weight)]. Returns the value at the given percentile """
    pairs = sorted(pairs)
    total = sum(w for _, w in pairs)
    if not total:
        return 0
    if pct >= 100:
        return pairs[-1][0]
    limit = total * pct / 100.
    acc = 0
    for v, w in pairs:
        acc += w
        if acc >= limit:
            return v
    return pairs[-1][0]

@dataclass
class Measurement:
    upem: int
    height: float           # font units
    depth: float            # font units (positive)
    avgbase: float          # font units
    fontsize: float = 0.
    linespacing: float = 0.

def measureText(fontpath, clusters, script=None, lang=None, direction=None, features=None,
                percentile=99.5):
    """ Shapes each distinct grapheme cluster and measures its ink extents """
    import uharfbuzz as hb
    blob = hb.Blob.from_file_path(fontpath)
    face = hb.Face(blob)
    font = hb.Font(face)
    upem = face.upem
    joining = script in JOINING_SCRIPTS

    def shape(text, start, length):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        if script:
            try:
                buf.script = script
            except Exception:
                pass
        if lang:
            try:
                buf.language = lang
            except Exception:
                pass
        if direction in ("ltr", "rtl"):
            buf.direction = direction
        hb.shape(font, buf, features or {})
        top = None
        bot = None
        y = 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            if start <= info.cluster < start + length:
                ext = font.get_glyph_extents(info.codepoint)
                if ext is not None and ext.height != 0:
                    gt = y + pos.y_offset + ext.y_bearing
                    gb = gt + ext.height
                    top = gt if top is None else max(top, gt)
                    bot = gb if bot is None else min(bot, gb)
            y += pos.y_advance
        return top, bot

    heights = []
    depths = []
    basesum = 0
    basen = 0
    basecache = {}
    for g, n in clusters.items():
        if g.isspace():
            continue
        top, bot = shape(g, 0, len(g))
        if joining and unicodedata.category(g[0]).startswith("L"):
            # measure the medial form too; ZWJ is invisible
            t2, b2 = shape("\u200D" + g + "\u200D", 1, len(g))
            if t2 is not None:
                top = t2 if top is None else max(top, t2)
                bot = b2 if bot is None else min(bot, b2)
        if top is None:
            continue
        heights.append((top, n))
        depths.append((-bot, n))
        if unicodedata.category(g[0]).startswith("L"):
            b = g[0]
            if b not in basecache:
                basecache[b] = shape(b, 0, 1)[0]
            if basecache[b] is not None:
                basesum += basecache[b] * n
                basen += n
    height = _weighted_percentile(heights, percentile)
    depth = max(0, _weighted_percentile(depths, percentile))
    avgbase = basesum / basen if basen else upem * REF_BASE_HEIGHT
    return Measurement(upem, height, depth, avgbase)

def sizeFromMeasurement(m, textsize=8., leading=0.5):
    ratio = m.avgbase / m.upem
    if ratio <= 0:
        ratio = REF_BASE_HEIGHT
    m.fontsize = round(textsize * REF_BASE_HEIGHT / ratio, 2)
    m.linespacing = round((m.height + m.depth) / m.upem * m.fontsize + leading, 1)
    return m


# ---------------------------------------------------------------------------
# Base configuration

_skipcfgfiles = re.compile(r"(?i)(\.piclist|^AdjLists$|\.adj$|^changes\.txt$|^picChecks\.txt$|^ptxprint_override\.cfg$)")

def importBaseConfig(base, prjpath, cfgname=None, info=None):
    """ Copies the base configuration into the new project. Returns the config name.
        Records the base body font (and any fonts from a base archive) in info. """
    cfgname = _importBaseConfig(base, prjpath, cfgname, info)
    if info is not None:
        cp = configparser.ConfigParser(interpolation=None)
        try:
            cp.read(os.path.join(prjpath, "shared", "ptxprint", cfgname, "ptxprint.cfg"), encoding="utf-8")
            fr = cp.get("document", "fontregular", fallback="")
        except configparser.Error:
            fr = ""
        if fr.split("|")[0].strip():
            info.basefont = fr.split("|")[0].strip()
    return cfgname

def _importBaseConfig(base, prjpath, cfgname, info):
    sharedir = os.path.join(prjpath, "shared", "ptxprint")
    os.makedirs(sharedir, exist_ok=True)
    if base.lower().endswith(".zip"):
        with ZipFile(base) as zf:
            cfgs = {}
            for n in zf.namelist():
                m = re.match(r"^(?:[^/]+/)?shared/ptxprint/(?:([^/]+)/)?ptxprint\.cfg$", n)
                if m:
                    cfgs[m.group(1) or "Default"] = os.path.dirname(n)
            if not cfgs:
                raise ValueError(f"No configuration found in {base}")
            if cfgname is None:
                cfgname = "Default" if "Default" in cfgs else sorted(cfgs)[0]
            if cfgname not in cfgs:
                raise ValueError(f"No configuration {cfgname} in {base}")
            src = cfgs[cfgname] + "/"
            dest = os.path.join(sharedir, cfgname)
            for n in zf.namelist():
                if n.startswith(src) and not n.endswith("/"):
                    rel = n[len(src):]
                    if "/" in rel or _skipcfgfiles.search(rel):
                        continue
                    os.makedirs(dest, exist_ok=True)
                    with zf.open(n) as inf, open(os.path.join(dest, rel), "wb") as outf:
                        shutil.copyfileobj(inf, outf)
            if info is not None:
                fdir = os.path.join(os.path.dirname(prjpath), "_basefonts")
                for n in zf.namelist():
                    if re.search(r"(^|/)shared/fonts/[^/]+\.(ttf|otf)$", n, re.I):
                        os.makedirs(fdir, exist_ok=True)
                        with zf.open(n) as inf, open(os.path.join(fdir, os.path.basename(n)), "wb") as outf:
                            shutil.copyfileobj(inf, outf)
                if os.path.isdir(fdir):
                    info.basefontdir = fdir
        return cfgname
    if os.path.isdir(base):
        base = os.path.join(base, "ptxprint.cfg")
    if not os.path.exists(base):
        raise FileNotFoundError(base)
    srcdir = os.path.dirname(os.path.abspath(base))
    if cfgname is None:
        cfgname = os.path.basename(srcdir)
        if cfgname.lower() == "ptxprint":
            cfgname = "Default"
    _copycfgdir(srcdir, os.path.join(sharedir, cfgname))
    return cfgname

def _copycfgdir(srcdir, destdir):
    shutil.copytree(srcdir, destdir, dirs_exist_ok=True,
                    ignore=lambda d, fs: [f for f in fs if _skipcfgfiles.search(f)])


# ---------------------------------------------------------------------------
# Settings

def inferSettings(info, stats, args, finder):
    """ Returns (widget settings dict, vars dict, font family or None) """
    from ptxprint.font import cachepath
    settings = {}
    pvars = {}
    # script
    script = info.script
    tscript = stats.mainscript
    if not script:
        script = tscript or "Zyyy"
        info.note("script", script, "text")
    elif tscript and tscript != script and stats.scripts[tscript] > 0.8 * sum(stats.scripts.values()):
        logger.warning(f"Metadata script {script} disagrees with text script {tscript}; using {tscript}")
        script = tscript
        info.note("script", script, "text (overrides metadata)")
    settings["fcb_script"] = script
    # direction
    direction = info.direction
    if not direction:
        rtl = stats.bidi.get("R", 0) + stats.bidi.get("AL", 0)
        direction = "rtl" if rtl > 0.5 * sum(stats.bidi.values()) else "ltr"
        info.note("direction", direction, "text")
    settings["fcb_textDirection"] = direction
    settings["c_RTLbookBinding"] = direction == "rtl"
    settings["c_RTLpagination"] = direction == "rtl"
    # line breaking
    if script in NOSPACE_SCRIPTS:
        settings["c_linebreakon"] = True
        settings["t_linebreaklocale"] = info.langtag.split("-")[0] if info.langtag else ""
    if script == "Mymr":
        settings["c_scrmymrSyllable"] = True
    # books
    books = [b for b in (info.books or stats.bookorder) if b in stats.bookorder] or stats.bookorder
    if len(books):
        settings["r_book"] = "multiple"
        settings["ecb_booklist"] = " ".join(books)
    # copyright
    if info.copyright:
        settings["txbf_copyright"] = info.copyright
    elif info.rightsholder:
        settings["txbf_copyright"] = "© " + info.rightsholder
    # titles
    mt, st, cands = chooseTitles(info, stats)
    for c in cands:
        info.note("title candidate", f"{c.text!r} score={c.score:.2f} (script {c.script:.2f} vocab {c.vocab:.2f})", c.source)
    # always set these so that nothing from the base config's project leaks through
    pvars["maintitle"] = mt.text if mt is not None else ""
    pvars["subtitle"] = st.text if st is not None else ""
    info.note("maintitle", pvars["maintitle"], mt.source if mt is not None else "none found")
    info.note("subtitle", pvars["subtitle"], st.source if st is not None else "none found")
    if info.autonym or info.langname:
        pvars["languagename"] = info.autonym or info.langname
    if info.iso:
        pvars["langiso"] = info.iso
    # fonts
    fontdir = os.path.join(info.prjpath, "shared", "fonts")
    os.makedirs(fontdir, exist_ok=True)
    found = findFont(info, stats, fontdir, finder, forcefont=args.font)
    family = None
    if found is None:
        logger.error("No font found that covers the text")
    else:
        family, fpath, fsource = found
        cachepath(fontdir)
        info.note("font", family, fsource)
        feats = info.fontfeats.get(family.casefold(), "")
        mapping, msource = digitMapping(stats, info.numerals)
        if mapping:
            info.note("digits", mapping, msource)
        settings["_font"] = (family, feats, mapping, script)
        hbfeats = {}
        for f in re.split(r"[,\s]+", feats or ""):
            if "=" in f:
                k, v = f.split("=", 1)
                try:
                    hbfeats[k.strip()] = int(v)
                except ValueError:
                    pass
        m = measureText(fpath, stats.clusters, script=script.lower() if script else None,
                        lang=info.langtag.split("-")[0] if info.langtag else None,
                        direction=direction, features=hbfeats, percentile=args.percentile)
        sizeFromMeasurement(m, args.textsize, args.leading)
        info.note("font size", m.fontsize, f"avg base height {m.avgbase/m.upem:.3f}em")
        info.note("line spacing", m.linespacing, f"height {m.height/m.upem:.3f}em depth {m.depth/m.upem:.3f}em")
        settings["s_fontsize"] = m.fontsize
        settings["s_linespacing"] = m.linespacing
        settings["c_lockFontSize2Baseline"] = False
    return settings, pvars, family


# ---------------------------------------------------------------------------
# PTXprint model

def _macrosdir():
    scriptsdir = os.path.abspath(os.path.dirname(__file__))
    macrosdir = os.path.join(scriptsdir, 'ptx2pdf')
    if not os.path.exists(macrosdir):
        if os.path.exists("/usr/share/ptx2pdf/texmacros"):
            macrosdir = "/usr/share/ptx2pdf/texmacros"
        else:
            macrosdir = os.path.join(scriptsdir, "..", "..", "..", "src")
    return os.path.abspath(macrosdir)

def applyToConfig(projdir, prjid, cfgname, settings, pvars, defines, output):
    from ptxprint.view import ViewModel
    from ptxprint.project import ProjectList
    from ptxprint.font import initFontCache, FontRef
    args = argparse.Namespace(debug=False, extras=0, nofontcache=True, paratext=None, print=False,
                    runs=0, pdfversion=14, diffdpi=0, diffoutfile=None, nointernet=False,
                    enablescripts=False, testing=False, timeout=1200)
    userconfig = configparser.ConfigParser(interpolation=None)
    userconfig.add_section("projectdirs")
    prjTree = ProjectList()
    prjTree.addTreedir(projdir)
    project = prjTree.findProject(prjid)
    if project is None:
        raise ValueError(f"Can't find project {prjid} in {projdir}")
    initFontCache().wait()
    view = ViewModel(prjTree, userconfig, _macrosdir(), args)
    view.setup_ini()
    view.setPrjid(prjid, project.guid, loadConfig=False, startup=True)
    view.setConfigId(cfgname)
    font = settings.pop("_font", None)
    for k, v in settings.items():
        view.set(k, v)
    if font is not None:
        family, feats, mapping, script = font
        fref = FontRef(family, "")
        if feats:
            fref.updateFeats(feats)
        if mapping:
            fref.feats['mapping'] = 'mappings/{}digits'.format(mapping)
        view.set("bl_fontR", fref)
        view.onFontChanged(None)
    for k in view.allvars():
        if k not in pvars and view.getvar(k):
            logger.warning(f"Base configuration variable kept: {k} = {view.getvar(k)}")
    for k, v in pvars.items():
        view.setvar(k, v)
    for k, v in (defines or {}).items():
        view.set(k, v)
    view.saveConfig(force=True)
    view.createArchive(output, nobuild=True)
    return view


# ---------------------------------------------------------------------------
# Main

class DictAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        d = getattr(namespace, self.dest) or {}
        k, _, v = values.partition("=")
        d[k] = v
        setattr(namespace, self.dest, d)

def parseArgs(argv=None):
    parser = argparse.ArgumentParser(description="Create a PTXprint archive from a DBL bundle (or other scripture source) and a base configuration")
    parser.add_argument("source", help="DBL bundle zip, zipped project, Paratext project directory or directory of USFM/USX files")
    parser.add_argument("-c", "--config", required=True, help="Base configuration: path to a ptxprint.cfg or a PTXprint archive zip")
    parser.add_argument("-o", "--output", help="Output archive (default <prjid>-<cfg>PTXprintArchive.zip)")
    parser.add_argument("--prjid", help="Project id to create")
    parser.add_argument("--cfgname", help="Configuration name to use (and to pick from an archive)")
    parser.add_argument("--textsize", type=float, default=8., help="Equivalent Latin text size in points [8]")
    parser.add_argument("--leading", type=float, default=0.5, help="Extra space (pt) added to measured text height + depth [0.5]")
    parser.add_argument("--percentile", type=float, default=99.5, help="Percentile of cluster occurrences that must fit in the line spacing [99.5]")
    parser.add_argument("--font", help="Font family to try before any inferred ones")
    parser.add_argument("-D", "--define", action=DictAction, default={}, help="Set UI component=value after inference (repeatable)")
    parser.add_argument("-l", "--logging", default="WARNING", help="Logging level")
    parser.add_argument("--keep", help="Keep the working project tree in this directory")
    return parser.parse_args(argv)

def printReport(info):
    print(f"Project {info.prjid}:")
    for k, v, src in info.report:
        print(f"  {k:16} {v}   [{src}]")

def main(argv=None, finder=None):
    args = parseArgs(argv)
    logging.basicConfig(level=getattr(logging, args.logging.upper(), logging.WARNING),
                        format="%(levelname)s:%(module)s %(message)s")
    if args.keep:
        os.makedirs(args.keep, exist_ok=True)
        projdir = args.keep
        tmpdir = None
    else:
        tmpdir = tempfile.mkdtemp(prefix="dbl2ptx")
        projdir = tmpdir
    try:
        info = importSource(args.source, projdir, args.prjid)
        cfgname = importBaseConfig(args.config, info.prjpath, args.cfgname, info=info)
        stats = analyseText(info)
        if not len(stats.clusters):
            raise ValueError("No scripture text found")
        settings, pvars, family = inferSettings(info, stats, args, finder or FontFinder())
        output = args.output or "{}-{}PTXprintArchive.zip".format(info.prjid, cfgname)
        output = os.path.abspath(output)
        applyToConfig(projdir, info.prjid, cfgname, settings, pvars, args.define, output)
        printReport(info)
        print(f"Archive written to {output}")
        return 0 if family is not None else 1
    finally:
        if tmpdir is not None:
            shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(main())
