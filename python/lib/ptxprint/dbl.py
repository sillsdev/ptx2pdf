
import xml.etree.ElementTree as et
import re, os, shutil, io
from zipfile import ZipFile
from ptxprint.ptsettings import books, allbooks, bookcodes
from ptxprint.utils import get_ptsettings, booknumbers
import usfmtc

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

def UnpackBooks(inzip, prjid, prjdir, subdir=None):
    for f in inzip.namelist():
        if subdir is not None and not f.startswith(subdir+"/"):
            continue
        fbase = os.path.basename(f)
        (fbk, fext) = os.path.splitext(fbase)
        ftype = usfmtc._filetypes.get(fext.lower(), None)
        if ftype is None:
            continue
        bk = None
        if fbk[:3].upper() in bookcodes:
            bk = fbk[:3]
        elif fbk[-3:].upper() in bookcodes:
            bk = fbk[-3:]
        if bk is not None:
            indoc = unpackBook(inzip, f, bk, ftype, prjid, prjdir)
            inzip.collectBookNames(indoc)
    if not inzip.hasbooknames:
        inzip.outBookNames(os.path.join(prjdir, prjid))
    return os.path.exists(prjdir, prjid)

def unpackBook(inzip, inname, bkid, informat, prjid, prjdir):
    prjpath = os.path.join(prjdir, prjid)
    outfname = "{}{}{}.USFM".format(bookcodes.get(bkid, "ZZ"), bkid, prjid)
    outpath = os.path.join(prjpath, outfname)
    os.makedirs(prjpath, exist_ok=True)
    with io.TextIOWrapper(inzip.open(inname), encoding="utf-8") as inf:
        indoc = usfmtc.readFile(inf, informat=informat)
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

def UnpackDBL(inzip, prjid, prjdir):
    info = {'prjid': prjid}
    bookshere = [0] * len(allbooks)
    subFolder = ""
    for name in inzip.namelist():
        if name == "metadata.xml":
            break
        if name.endswith("/metadata.xml"):
            subFolder = name[:-12]
            break
    else:
        return False
    with inzip.open(subFolder + "metadata.xml") as inmeta:
        metadoc = et.parse(inmeta)
        meta = metadoc.getroot()
    if prjid is None:
        prjid = meta.findtext('identification/abbreviation')
    prjpath = os.path.join(prjdir, prjid)
    os.makedirs(prjpath, exist_ok=True)
    for f in ('styles.xml', 'release/styles.xml'):
        try:
            with inzip.open(subFolder + f) as instyle:
                style = et.parse(instyle)
            break
        except KeyError:
            pass

    ldmlname = "{}_{}.ldml".format(meta.findtext('language/iso'), meta.findtext('language/ldml'))
    for f in (ldmlname, 'release/'+ldmlname):
        try:
            with inzip.open(subFolder + f) as source, \
                 open(os.path.join(prjpath, ldmlname), "wb") as target:
                shutil.copyfileobj(source, target)
            break
        except KeyError:
            pass

    metacontents = meta.find('publications/publication[@default="true"]/structure')
    if metacontents is not None:
        for contentel in metacontents.findall('content'):
            bkid = contentel.get("role")
            infname = contentel.get("src")
            inbook = unpackBook(inzip, infname, bkid, "usx", prjid, prjdir)
            inzip.collectBookNames(inbook)
    else:
        metacontents = meta.find('contents/bookList[@default="true"]/books')
        for contentel in metacontents.findall('book'):
            bkid = contentel.get('code')
            infname = 'USX_1/{}.usx'.format(bkid)
            inbook = unpackBook(inzip, infname, bkid, "usx", prjid, prjdir)
            inzip.collectBookNames(inbook)
    bkindex = books.get(bkid)+1
    bookshere[bkindex-1] = 1

    info['bookspresent'] = "".join(str(x) for x in bookshere)
    settings = et.Element('ScriptureText')
    settings.tail = "\n    "
    for k, v in _dblMapping.items():
        t, s = v
        if t == 'meta':
            val = meta.findtext(s)
        elif t == 'metamulti':
            val = "//".join(innertext(meta, s))
        elif t == 'styles':
            val = style.findtext(s)
        elif t == 'eval':
            val = s(info)
        elif t == 'string':
            val = s
        n = et.SubElement(settings, k)
        n.text = val
        n.tail = "\n    "
    n.tail = "\n"
    with open(os.path.join(prjpath, "ptxSettings.xml"), "wb") as outf:
        outf.write(et.tostring(settings, encoding="utf-8"))
    if not inzip.hasbooknames:
        inzip.outBookNames(prjpath)
    return True
