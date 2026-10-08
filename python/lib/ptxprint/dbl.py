
import xml.etree.ElementTree as et
import re, os, shutil, io, logging
from dataclasses import dataclass, field
from zipfile import ZipFile
from ptxprint.ptsettings import books, allbooks, bookcodes
from ptxprint.utils import get_ptsettings, booknumbers
import usfmtc

logger = logging.getLogger(__name__)

class BundleZip(ZipFile):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.hasbooknames = False
        for f in self.namelist():
            if f.lower().endswith("booknames.xml"):
                self.hasbooknames = True
                break
        self.booknames = {}

    def collectBookNames(self, indoc):
        if not self.hasbooknames and indoc is not None:
            self.booknames[indoc.book] = [indoc.getroot().findtext('.//para[@style="toc{}"]'.format(i)) for i in range(1,4)]

    def outBookNames(self, path):
        if not len(self.booknames) or all(all(x is None for x in v) for v in self.booknames.values()):
            return
        fieldnames = "long short abbr".split()
        with open(os.path.join(path, "BookNames.xml"), "w", encoding="utf-8") as outf:
            outf.write("""<?xml version="1.0" encoding="utf-8"?>
<BookNames>
""")
            for b, v in sorted(self.booknames.items(), key=lambda k:booknumbers.get(k[0], 1000)):
                if all(x is None for x in v):
                    continue
                outf.write('  <book code="{}"'.format(b))
                for i, c in enumerate(v):
                    if c is not None:
                        outf.write(' {}="{}"'.format(fieldnames[i], c))
                outf.write('/>\n')
            outf.write("</BookNames>\n")

def proc_start_ms(el, tag, pref, emit, ws):
    if "style" not in el.attrib:
        return
    extra = ""
    if "altnumber" in el.attrib:
        extra += " \\{0}a {1}\\{0}a*".format(pref, el.get("altnumber"))
    if "pubnumber" in el.attrib:
        extra += " \\{0}p {1}".format(pref, el.get("pubnumber"))
    emit("\\{0} {1}{2}{3}".format(el.get("style"), el.get("number"), extra, ws))

def append_attribs(el, emit, tag=None, nows=False):
    if tag is not None and type(tag) != tuple:
        tag = (tag, tag)
    at_start = tag is None and not nows
    if tag is None:
        l = el.attrib.items()
    elif tag[1] not in el.attrib:
        return
    else:
        l = [(tag[0], el.get(tag[1], ""))]
    for k,v in l:
        if k in ("style", "status", "title"):
            continue
        if at_start:
            emit(" ")
            at_start = False
        emit('|{0}="{1}"'.format(k, v))

def get(el, k):
    return el.get(k, "")

class Emitter:
    def __init__(self, outf):
        self.outf = outf
        self.last_ws = None
        self.init = True

    def __call__(self, s, keepws=False):
        if s is None:
            return
        s = re.sub(r"\s*\n\s*", "\n", s)
        if not s.startswith("\n"):
            if self.last_ws is not None and len(self.last_ws):
                self.outf.write(self.last_ws)
            self.last_ws = ""
        if self.init:
            s = s.lstrip("\n")
            if len(s):
                self.init = False
        i = len(s) - 1
        while i >= 0:
            if s[i] not in " \n":
                break
            i -= 1
        self.last_ws = s[i+1:]
        if i >= 0:
            s = s[:i+1]
            self.outf.write(s)

    def hasnows(self):
        return self.last_ws is not None and not len(self.last_ws)

    def addws(self):
        if self.last_ws is not None and not len(self.last_ws):
            self.last_ws = " "


_dblMapping = {
    'Name':                         ('meta', 'identification/systemId[@type="paratext"]/name'),
    'Language':                     ('meta', 'language/name'),
    'Encoding':                     ('string', '65001'),
    'Copyright':                    ('metamulti', 'copyright/fullStatement/statementContent/p'),
    'DefaultFont':                  ('styles', 'property[@name="font-family"]'),
    'DefaultFontSize':              ('styles', 'property[@name="font-size"]'),
    'FileNamePostPart':             ('eval', lambda info: info['prjid']+".USFM"),
    'FileNameBookNameForm':         ('string', '41MAT'),
    'NoSpaceBetweenBookAndChapter': ('string', 'False'),
    'ChapterVerseSeparator':        ('string', ':'),
    'RangeIndicator':               ('string', '-'),
    'SequenceIndicator':            ('string', ','),
    'ChapterRangeSeparator':        ('string', '–'),
    'BookSequenceSeparator':        ('string', '; '),
    'ChapterNumberSeparator':       ('string', '; '),
    'FileNamePrePart':              ('string', ''),
    'StyleSheet':                   ('string', "usfm.sty"),
    'MinParatextVersion':           ('string', '8.0.63.1'),
    'FullName':                     ('meta', 'identification/systemId[@type="paratext"]/fullName'),
    'Editable':                     ('string', 'F'),
    'BooksPresent':                 ('eval', lambda info: info['bookspresent'])
}

def innertext(root, path):
    res = []
    for e in root.findall(path):
        res.append("".join(s.strip() for s in e.itertext()))
    return res

def GetDBLName(dblfile):
    with ZipFile(dblfile) as inzip:
        for name in inzip.namelist():
            if not name.endswith("metadata.xml"):
                continue
            with inzip.open(name) as inf:
                metadoc = et.parse(inf)
            ltag = metadoc.findtext("./language/ldml") or metadoc.findtext("./language/iso")
            if "-" in ltag:
                ltag = ltag[:ltag.find("-")]
            prjcode = metadoc.findtext("./identification/abbreviation")
            return ltag + prjcode
    return None

def UnpackBundle(dblfile, prjid, prjdir):
    with BundleZip(dblfile) as dblzip:
        fnames = dblzip.namelist()
        if any(f.endswith("metadata.xml") for f in fnames):
            return UnpackDBL(dblzip, prjid, prjdir)
        elif any(f.lower().endswith("settings.xml") for f in fnames):
            return UnpackPTX(dblzip, prjid, prjdir)
        else:
            return UnpackBooks(dblzip, prjid, prjdir)

def guessBookFile(fname):
    """ Returns (bookid or None, filetype) for a scripture file name, or (None, None) if
        it isn't a scripture file """
    fbase = os.path.basename(fname)
    (fbk, fext) = os.path.splitext(fbase)
    ftype = usfmtc._filetypes.get(fext.lower(), None)
    if ftype is None:
        return (None, None)
    bk = None
    if (m := re.match(r"^[0-9A-Z]\d([0-9A-Z]{3})", fbk, re.I)) and m.group(1).upper() in bookcodes:
        bk = m.group(1)         # Paratext style 41MATxxx
    elif fbk[:3].upper() in bookcodes:
        bk = fbk[:3]
    elif fbk[-3:].upper() in bookcodes:
        bk = fbk[-3:]
    elif (m := re.match(r".*?([a-z]{3}|\d[a-z]{2})", fbk)):
        if m.group(1).upper() in bookcodes:
            bk = m.group(1)
    return (bk.upper() if bk is not None else None, ftype)

def UnpackBooks(inzip, prjid, prjdir, subdir=None):
    for f in inzip.namelist():
        if subdir is not None and not f.startswith(subdir+"/"):
            continue
        bk, ftype = guessBookFile(f)
        if ftype is None:
            continue
        indoc = unpackBook(inzip, f, bk, ftype, prjid, prjdir)
        inzip.collectBookNames(indoc)
    if not inzip.hasbooknames:
        inzip.outBookNames(os.path.join(prjdir, prjid))
    return os.path.exists(os.path.join(prjdir, prjid))

class _DirZip:
    """ Presents a directory of files with enough of the ZipFile interface for unpackBook """
    def __init__(self, path):
        self.path = path
    def open(self, name):
        return open(os.path.join(self.path, name), "rb")

def UnpackBooksDir(srcdir, prjid, prjdir):
    """ Converts a directory of USFM/USX/USJ files into a project """
    namer = BundleZip.__new__(BundleZip)
    namer.hasbooknames = any(f.lower() == "booknames.xml" for f in os.listdir(srcdir))
    namer.booknames = {}
    dz = _DirZip(srcdir)
    found = False
    for f in sorted(os.listdir(srcdir)):
        if not os.path.isfile(os.path.join(srcdir, f)):
            continue
        bk, ftype = guessBookFile(f)
        if ftype is None:
            continue
        try:
            indoc = unpackBook(dz, f, bk, ftype, prjid, prjdir)
        except Exception as e:
            logger.warning(f"Failed to read {f}: {e}")
            continue
        found = True
        BundleZip.collectBookNames(namer, indoc)
    prjpath = os.path.join(prjdir, prjid)
    if namer.hasbooknames:
        for f in os.listdir(srcdir):
            if f.lower() == "booknames.xml":
                shutil.copy(os.path.join(srcdir, f), os.path.join(prjpath, "BookNames.xml"))
    elif found:
        BundleZip.outBookNames(namer, prjpath)
    return found

def unpackBook(inzip, inname, bkid, informat, prjid, prjdir):
    prjpath = os.path.join(prjdir, prjid)
    os.makedirs(prjpath, exist_ok=True)
    with io.TextIOWrapper(inzip.open(inname), encoding="utf-8") as inf:
        indoc = usfmtc.readFile(inf, informat=informat)
    if bkid is None:
        bkid = indoc.book
    outfname = "{}{}{}.USFM".format(bookcodes.get(bkid, "ZZ"), bkid, prjid)
    outpath = os.path.join(prjpath, outfname)
    indoc.saveAs(outpath)
    return indoc

def UnpackPTX(inzip, prjid, prjdir):
    path = os.path.join(prjdir, prjid)
    inzip.extractall(path)
    if not inzip.hasbooknames:
        for f in [x for x in os.listdir(path) if x.lower().endswith("sfm")]:
            indoc = usfmtc.readFile(os.path.join(path, f))
            inzip.collectBookNames(indoc)
        inzip.outBookNames(path)
    return True

@dataclass
class DBLInfo:
    """ Parsed contents of a DBL bundle's metadata.xml plus the locations of
        interesting support files inside the bundle zip. """
    meta: et.Element
    subfolder: str = ""
    iso: str = ""
    langtag: str = ""
    scriptcode: str = ""
    direction: str = ""
    numerals: str = ""
    langname: str = ""
    langnameLocal: str = ""
    books: list = field(default_factory=list)       # [(bookid, zip path)]
    booknames: dict = field(default_factory=dict)   # bookid: (long, short, abbr)
    ldmlfile: str = None
    stylesfile: str = None
    vrsfile: str = None
    sourcezip: str = None
    fontfiles: list = field(default_factory=list)

    def get(self, path, default=""):
        return (self.meta.findtext(path) or default).strip()

def _findMetadata(inzip):
    for name in inzip.namelist():
        if name == "metadata.xml":
            return ""
        if name.endswith("/metadata.xml") and name.count("/") == 1:
            return name[:-12]
    for name in inzip.namelist():
        if name.endswith("/metadata.xml"):
            return name[:-12]
    return None

def _findLdml(names, sub, iso, ldml):
    """ Bundles name their ldml file in all sorts of ways. Try the common ones
        and then anything that looks like it is for this language (rather than
        a national language, e.g. azz_es.ldml) """
    cands = []
    if ldml:
        cands.append(ldml + ".ldml")
    if iso and ldml:
        cands.append("{}_{}.ldml".format(iso, ldml))
    cands.append("ldml.xml")
    for c in cands:
        for d in ("", "release/"):
            if sub + d + c in names:
                return sub + d + c
    for n in names:
        b = os.path.basename(n)
        if not b.endswith(".ldml") or not n.startswith(sub):
            continue
        if iso and b.lower().startswith(iso.lower()) and not re.search(r"_[a-z]{2,3}\.ldml$", b):
            return n
    return None

def readDBLMetadata(inzip):
    """ Returns a DBLInfo for a bundle zip or None if it isn't a DBL bundle """
    sub = _findMetadata(inzip)
    if sub is None:
        return None
    with inzip.open(sub + "metadata.xml") as inmeta:
        meta = et.parse(inmeta).getroot()
    names = set(inzip.namelist())
    info = DBLInfo(meta=meta, subfolder=sub)
    info.iso = info.get("language/iso")
    ldml = info.get("language/ldml")
    info.scriptcode = info.get("language/scriptCode")
    if ldml:
        info.langtag = ldml
    elif info.iso:
        info.langtag = info.iso + ("-" + info.scriptcode if info.scriptcode else "")
    info.direction = info.get("language/scriptDirection").lower()
    info.numerals = info.get("language/numerals")
    info.langname = info.get("language/name")
    info.langnameLocal = info.get("language/nameLocal")

    pub = meta.find('publications/publication[@default="true"]')
    if pub is None:
        pub = meta.find('publications/publication')
    structure = pub.find('structure') if pub is not None else None
    if structure is not None:
        for c in structure.iter('content'):
            if c.get("src") and c.get("role"):
                info.books.append((c.get("role").split()[0], sub + c.get("src")))
    else:
        bks = meta.find('contents/bookList[@default="true"]/books')
        if bks is not None:
            for b in bks.findall('book'):
                info.books.append((b.get('code'), sub + 'USX_1/{}.usx'.format(b.get('code'))))
    for n in meta.findall('names/name'):
        nid = n.get('id', '')
        if not nid.startswith('book-'):
            continue
        info.booknames[nid[5:].upper()] = tuple((n.findtext(k) or "").strip() for k in ("long", "short", "abbr"))

    info.ldmlfile = _findLdml(names, sub, info.iso, ldml)
    for f in ('styles.xml', 'release/styles.xml'):
        if sub + f in names:
            info.stylesfile = sub + f
            break
    for n in sorted(names):
        if not n.startswith(sub):
            continue
        l = n.lower()
        if l.endswith(".vrs") and info.vrsfile is None:
            info.vrsfile = n
        elif l.endswith((".ttf", ".otf")):
            info.fontfiles.append(n)
        elif l.endswith("source/source.zip"):
            info.sourcezip = n
    return info

def UnpackDBL(inzip, prjid, prjdir, info=None):
    if info is None:
        info = readDBLMetadata(inzip)
    if info is None:
        return False
    meta = info.meta
    if prjid is None:
        prjid = meta.findtext('identification/abbreviation')
    prjpath = os.path.join(prjdir, prjid)
    os.makedirs(prjpath, exist_ok=True)
    style = None
    if info.stylesfile is not None:
        with inzip.open(info.stylesfile) as instyle:
            style = et.parse(instyle)

    langid = info.langtag or "unk"
    if info.ldmlfile is not None:
        with inzip.open(info.ldmlfile) as source, \
                open(os.path.join(prjpath, langid + ".ldml"), "wb") as target:
            shutil.copyfileobj(source, target)
    if info.vrsfile is not None:
        with inzip.open(info.vrsfile) as source, \
                open(os.path.join(prjpath, "custom.vrs"), "wb") as target:
            shutil.copyfileobj(source, target)
    if len(info.fontfiles):
        fontdir = os.path.join(prjpath, "shared", "fonts")
        os.makedirs(fontdir, exist_ok=True)
        for f in info.fontfiles:
            with inzip.open(f) as source, \
                    open(os.path.join(fontdir, os.path.basename(f)), "wb") as target:
                shutil.copyfileobj(source, target)

    bookshere = [0] * len(allbooks)
    for bkid, infname in info.books:
        try:
            inbook = unpackBook(inzip, infname, bkid, "usx", prjid, prjdir)
        except KeyError:
            logger.warning(f"Missing book {infname} in bundle")
            continue
        inzip.collectBookNames(inbook)
        if bkid in books:
            bookshere[books[bkid]] = 1

    binfo = {'prjid': prjid, 'bookspresent': "".join(str(x) for x in bookshere)}
    settings = et.Element('ScriptureText')
    settings.tail = "\n    "
    for k, v in _dblMapping.items():
        t, s = v
        if t == 'meta':
            val = meta.findtext(s)
        elif t == 'metamulti':
            val = "//".join(innertext(meta, s))
        elif t == 'styles':
            val = style.findtext(s) if style is not None else None
        elif t == 'eval':
            val = s(binfo)
        elif t == 'string':
            val = s
        n = et.SubElement(settings, k)
        n.text = val
        n.tail = "\n    "
    for k, v in (('LanguageIsoCode', langid), ('Versification', '4')):
        n = et.SubElement(settings, k)
        n.text = v
        n.tail = "\n    "
    n.tail = "\n"
    with open(os.path.join(prjpath, "ptxSettings.xml"), "wb") as outf:
        outf.write(et.tostring(settings, encoding="utf-8"))
    if len(info.booknames):
        inzip.booknames = {k: [v[0] or None, v[1] or None, v[2] or None] for k, v in info.booknames.items()}
        inzip.outBookNames(prjpath)
    elif not inzip.hasbooknames:
        inzip.outBookNames(prjpath)
    return True
