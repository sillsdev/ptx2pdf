
import xml.etree.ElementTree as et
import re, os, shutil
from zipfile import ZipFile
from ptxprint.ptsettings import books, allbooks
from ptxprint.utils import get_ptsettings

def proc_start_ms(el, tag, pref, emit, ws):
    if "style" not in el.attrib:
        return
    extra = ""
    if "altnumber" in el.attrib:
        extra += " \\{0}a {1}\\{0}a*".format(pref, el.get("altnumber"))
    if "pubnumber" in el.attrib:
        extra += " \\{0}p {1}".format(pref, el.get("pubnumber"))
    emit("\\{0} {1}{2}{3}".format(el.get("style"), el.get("number"), extra, ws))

def append_attribs(el, emit, tag=None):
    if tag is not None and type(tag) != tuple:
        tag = (tag, tag)
    at_start = tag is None
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

def usx2usfm(fname, outf):
    emit = Emitter(outf)
    parent = None
    stack = []
    lastel = None
    for (ev, el) in et.iterparse(fname, ("start", "end")):
        s = el.get("style", "")
        if lastel is not None:
            emit(lastel.tail, True)
        if ev == "start":
            if lastel is None and parent is not None:
                if parent.text is not None and len(parent.text.strip()):
                    emit.addws()
                emit(parent.text, True)
            if el.tag in ("chapter", "book", "para", "row", "sidebar", "verse") and s != "":
                emit("\n")
            if el.tag == "chapter":
                proc_start_ms(el, "chapter", "c", emit, "\n")
            elif el.tag == "verse":
                proc_start_ms(el, "verse", "v", emit, " ")
            elif el.tag == "book":
                emit("\\{0} {1} ".format(s, el.get("code")))
            elif el.tag in ("row", "para"):
                emit("\\{0}".format(s))
            elif el.tag in ("link", "char"):
                nested = "+" if parent is not None and parent.tag == "char" else ""
                emit("\\{0} ".format(nested + s))
            elif el.tag in ("note", "sidebar"):
                emit("\\{0} {1} ".format(s, el.get("caller")))
                if "category" in el.attrib:
                    emit("\\cat {0}\\cat*".format(el.get("category")))
            elif el.tag == "unmatched":
                emit("\\" + el.get(marker))
            elif el.tag == "figure":
                emit("\\{} ".format(s))
            elif el.tag == "cell":
                if "colspan" in el.attrib:
                    emit("\\{0}-{1} ".format(s, el.get("colspan")))   # check colspan ScrStylesheet.RangeMarker
                else:
                    emit("\\{} ".format(s))
            elif el.tag == "optbreak":
                emit("//")
            elif el.tag == "ms":
                emit("\\{}".format(s))
                append_attribs(el, emit)
                emit("\\*")
            elif el.tag in ("usx", "annot", "table", "usfm", "text", "ref"):
                pass
            else:
                raise SyntaxError(el.tag)
            stack.append(parent)
            parent = el
            lastel = None
            lastopen = el
        elif ev == "end":
            if id(lastopen) == id(el):
                if el.text is not None and len(el.text.strip()):
                    emit.addws()
                emit(el.text, True)
            parent = stack.pop()
            if el.tag == "note" and el.get("closed", "true") == "true":
                emit("\\{}*".format(s))
            elif el.tag in ("char", "link"):
                nested = "+" if parent is not None and parent.tag == "char" else ""
                if el.get("closed", "true") == "true":
                    append_attribs(el, emit)
                    emit("\\{}*".format(nested + s))
            elif el.tag == "figure":
                for k in ("alt", ("src", "file"), "size", "loc", "copy", "ref"):
                    append_attribs(el, emit, k)
                emit("\\{}*".format(s))
            elif el.tag == "sidebar":
                emit.addws()
                if el.get("closed", "true") == "true":
                    emit("\\{}e ".format(s))
            lastel = el


_dblMapping = {
    'Name':             ('meta', 'identification/systemId[@type="paratext"]/name'),
    'Language':         ('meta', 'language/name'),
    'Encoding':         ('string', '65001'),
    'Copyright':        ('metamulti', 'copyright/fullStatement/statementContent/p'),
    'DefaultFont':      ('styles', 'property[@name="font-family"]'),
    'DefaultFontSize':  ('styles', 'property[@name="font-size"]'),
    'FileNamePostPart': ('eval', lambda info: info['prjid']+".USFM"),
    'FileNameBookNameForm': ('string', '41MAT'),
    'FileNamePrePart':  ('string', ''),
    'StyleSheet':       ('string', "usfm.sty"),
    'MinParatextVersion': ('string', '8.0.63.1'),
    'FullName':         ('meta', 'identification/systemId[@type="paratext"]/fullName'),
    'Editable':         ('string', 'F'),
    'BooksPresent':     ('eval', lambda info: info['bookspresent'])
}

def innertext(root, path):
    res = []
    for e in root.findall(path):
        res.append("".join(s.strip() for s in e.itertext()))
    return res

def UnpackDBL(dblfile, prjid, prjdir):
    info = {'prjid': prjid}
    bookshere = [0] * len(allbooks)
    with ZipFile(dblfile) as inzip:
        with inzip.open("metadata.xml") as inmeta:
            metadoc = et.parse(inmeta)
            meta = metadoc.getroot()
        if prjid is None:
            prjid = meta.findtext('identification/abbreviation')
        prjpath = os.path.join(prjdir, prjid)
        os.makedirs(prjpath, exist_ok=True)
        for f in ('styles.xml', 'release/styles.xml'):
            try:
                with inzip.open(f) as instyle:
                    style = et.parse(instyle)
                break
            except KeyError:
                pass

        ldmlname = "{}_{}.ldml".format(meta.findtext('language/iso'), meta.findtext('language/ldml'))
        for f in (ldmlname, 'release/'+ldmlname):
            try:
                with inzip.open(f) as source, \
                     open(os.path.join(prjpath, ldmlname), "wb") as target:
                    shutil.copyfileobj(source, target)
                break
            except KeyError:
                pass

        def process_usx(bkid, infname):
            bkindex = books.get(bkid)
            bookshere[bkindex-1] = 1
            outfname = "{:02}{}{}.USFM".format(bkindex, bkid, prjid)
            outpath = os.path.join(prjpath, outfname)
            with inzip.open(infname) as inf:
                with open(outpath, "w", encoding="utf-8") as outf:
                    usx2usfm(inf, outf)

        metacontents = meta.find('publications/publication[@default="true"]/structure')
        if metacontents is not None:
            for contentel in metacontents.findall('content'):
                bkid = contentel.get("role")
                infname = contentel.get("src")
                process_usx(bkid, infname)
        else:
            metacontents = meta.find('contents/bookList[@default="true"]/books')
            for contentel in metacontents.findall('book'):
                bkid = contentel.get('code')
                infname = 'USX_1/{}.usx'.format(bkid)
                process_usx(bkid, infname)

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
