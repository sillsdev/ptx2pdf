import os, re, uuid
import xml.etree.ElementTree as et
import regex, logging
from ptxprint.utils import allbooks, books, bookcodes, chaps
from ptxprint.unicode.UnicodeSets import flatten
from ptxprint.reference import RefSeparators

logger = logging.getLogger(__name__)

ptrefsepvals = {
    'books': 'BookSequenceSeparator',
    'chaps': 'ChapterNumberSeparator',
    'cv': 'ChapterVerseSeparator',
    'range': 'RangeIndicator',
}

_versifications = ["", "", "lxx", "vul", "eng", "rsc", "rso"]    # 0=unk, 1=org

class ParatextSettings:
    def __init__(self, prjdir):
        self.dict = {}
        self.ldml = None
        self.prjdir = prjdir
        self.langid = None
        self.dir = "left"
        self.collation = None
        self.saveme = False
        self.parse()

    def parse(self):
        for a in ("Settings.xml", "ptxSettings.xml"):
            path = os.path.join(self.prjdir, a)
            if os.path.exists(path):
                doc = et.parse(path)
                for c in doc.getroot():
                    self.dict[c.tag] = c.text
                self.calcbookspresent()
                self.read_ldml()
                break
        self.inferValues()
        if 'FileNamePrePart' in self.dict:
            logger.debug("{FileNamePrePart} {FileNameBookNameForm} {FileNamePostPart}".format(**self.dict))
        path = os.path.join(self.prjdir, "BookNames.xml")
        if os.path.exists(path):
            self.read_bookNames(path)
            self.hasLocalBookNames = True
        else:
            self.default_bookNames()
            self.hasLocalBookNames = False
        self.collation = None
        self.refsep = False     # tristate: (False=undef), None, RefSeparator
        self.set_versification()
        return self

    def set_versification(self):
        self.versification = None
        if 'Versification' in self.dict:
            v = self.dict['Versification']
            if v in "012345":
                v = _versifications[int(v)]
                v += ".vrs"
                if not os.path.exists(os.path.join(self.prjdir, v)):
                    v = None
            self.versification = v
        if self.versification is None and os.path.exists(os.path.join(self.prjdir, "custom.vrs")):
            self.versification = "custom.vrs"
        return self

    def read_ldml(self):
        self.langid = re.sub('-(?=-|$)', '', self.get('LanguageIsoCode', "unk").replace(":", "-"))
        fname = os.path.join(self.prjdir, self.langid+".ldml")
        silns = "{urn://www.sil.org/ldml/0.1}"
        if os.path.exists(fname):
            self.ldml = et.parse(fname)
            for k in ['footnotes', 'crossrefs']:
                d = self.ldml.find('.//characters/special/{1}exemplarCharacters[@type="{0}"]'.format(k, silns))
                if d is not None:
                    self.dict[k] = ",".join(re.sub(r'^\[\s*(.*?)\s*\]', r'\1', d.text).split())
                    # print(k, self.dict[k].encode("unicode_escape"))
            fonts = self.ldml.findall('.//special/{0}external-resources/{0}font'.format(silns))
            for t in (None, "default"):
                for f in fonts:
                    if f.get('type', None) == t:
                        self.dict['DefaultFont'] = f.get('name', '')
                        self.dict['DeafultFontSize'] = float(f.get('size', 1.0)) * 12
            d = self.ldml.find(".//layout/orientation/characterOrder")
            if d is not None:
                if d.text.lower() == "right-to-left":
                    self.dir = "right"
        else:
            self.ldml = None

    def read_bookNames(self, fpath):
        bkstrs = {}
        self.bookStrs = {}
        doc = et.parse(fpath)
        for b in doc.findall(".//book"):
            bkid = b.get("code")
            tocs = [b.get(a, "") for a in ("long", "short", "abbr")]
            for i in range(len(tocs)-2,-1, -1):
                if tocs[i] == "":
                    tocs[i] = tocs[i+1]
            self.bookStrs[bkid] = tocs
            for s in tocs:
                for i in range(len(s)):
                    if s[i] == " ":
                        break
                    bkstrs[s[:i+1]] = "" if bkstrs.get(s[:i+1], bkid) != bkid else bkid
        if len(bkstrs):
            self.bkNames = {k:v for k,v in bkstrs.items() if v != ""}

    def default_bookNames(self):
        self.bookNames = {k: k for k, v in chaps.items() if 0 < int(v) < 999}
        self.bookStrs = {k: [k] * 3 for k in self.bookNames.keys()}

    def getLocalBook(self, s, level=0):
        return self.bookStrs.get(s, [s]*(level+1))[level] or s

    def __getitem__(self, key):
        return self.dict[key]

    def get(self, key, default=None):
        res = self.dict.get(key, default)
        if res is None:
            return default
        return res

    def find_ldml(self, path):
        if self.ldml is None:
            return None
        return self.ldml.find(path)

    def inferValues(self, forced=False):
        if forced or 'FileNameBookNameForm' not in self.dict:
            sfmfiles = [x for x in os.listdir(self.prjdir) if x.lower().endswith("sfm")]
            for f in sfmfiles:
                m = re.search(r"(\d{2})", f)
                if not m:
                    ei = f.rfind(".")
                    if ei > 0:
                        for i in range(len(f)-ei-2):
                            if f[i:i+3].upper() in allbooks:
                                bk = f[i:i+3].upper()
                                numi = i
                                break
                        else:
                            continue
                    else:
                        continue
                else:
                    bk = allbooks[int(m.group(1))-1]
                    numi = m.start(1)
                bki = f.lower().find(bk.lower())
                if bki < 0:
                    continue
                s = min(bki, numi)
                e = max(bki+3, numi+2)
                (pre, main, post) = f[:s], f[s:e], f[e:]
                self.dict['FileNamePrePart'] = pre
                self.dict['FileNamePostPart'] = post
                main = main[:numi-s] + "41" + main[numi-s+2:]
                main = main[:bki-s] + "MAT" + main[bki-s+3:]
                self.dict['FileNameBookNameForm'] = main
                break

        #self.dict['FullName'] = ""
        #self.dict['Copyright'] = ""
        if 'DefaultFont' not in self.dict:
            self.dict['DefaultFont'] = ""
        if 'Encoding'not in self.dict:
            self.dict['Encoding'] = 65001
        if 'BooksPresent' not in self.dict:
            self.calcbookspresent(inferred=forced)
        if 'Guid' not in self.dict:
            self.createGuid()
        self.set_versification()

    def createGuid(self):
        res = "{:X}".format(uuid.uuid1().int)
        self.dict['Guid'] = res
        self.saveme = True
        return res

    def calcbookspresent(self, inferred=False, forced=False):
        self.bookmap = {}
        booksfound = set()
        bookspresent = [0] * len(allbooks)
        if not inferred and 'FileNameBookNameForm' in self.dict:
            fbkfm = self.dict['FileNameBookNameForm']
            bknamefmt = self.get('FileNamePrePart', "") + \
                        fbkfm.replace("MAT","{bkid}").replace("41","{bkcode}") + \
                        self.get('FileNamePostPart', "")
            for k, v in books.items():
                fname = bknamefmt.format(bkid=k, bkcode=v+1)
                if os.path.exists(os.path.join(self.prjdir, fname)):
                    bookspresent[v-1] = 1
                    self.bookmap[k] = fname
                    booksfound.add(fname)
            if not len(booksfound) and not forced:     # buggy Settings.xml that doesn't fit the directory tree
                self.inferValues(forced=True)
                self.calcbookspresent(forced=True)
        else:
            for f in os.listdir(self.prjdir):
                if not f.lower().endswith("sfm") or f in booksfound or f.lower().startswith("regexbackup"):
                    continue
                with open(os.path.join(self.prjdir, f), encoding="utf-8", errors="ignore") as inf:
                    l = inf.readline()
                    m = re.match(r"^\uFEFF?\\id\s+(\S{3})\s*", l)
                    if m:
                        bkid = m.group(1).upper()
                        self.bookmap[bkid] = f
                        booksfound.add(f)
                        try:
                            v = int(bookcodes.get(bkid, -1))
                        except ValueError:
                            v = -1
                        if 0 <= v < len(allbooks):
                            bookspresent[v-1] = 1
        self.dict['BooksPresent'] = "".join(str(x) for x in bookspresent)

    def getBookFilename(self, bk):
        if bk in self.bookmap:
            return self.bookmap[bk]
        fbkfm = self.get('FileNameBookNameForm', "")
        bknamefmt = self.get('FileNamePrePart', "") + \
                    fbkfm.replace("MAT","{bkid}").replace("41","{bkcode}") + \
                    self.get('FileNamePostPart', "")
        fname = bknamefmt.format(bkid=bk, bkcode=bookcodes.get(bk, 0))
        return fname

    def getArchiveFiles(self):
        res = {}
        for a in ("Settings.xml", "BookNames.xml", "ptxSettings.xml"):
            path = os.path.join(self.prjdir, a)
            if os.path.exists(path):
                res[path] = a
        if self.langid is None:
            return res
        fname = os.path.join(self.prjdir, self.langid+".ldml")
        if os.path.exists(fname):
            res[fname] = self.langid+".ldml"
        return res

    def getCollation(self):
        if self.collation is None:
            self.collation = self.find_ldml('collations/collation[@type="standard"]/cr')
        return self.collation

    def getIndexList(self):
        s = self.find_ldml('characters/exemplarCharacters[@type="index"]')
        if s is None:
            return None
        res = list(flatten(s))
        return res

    def getRefSeparators(self):
        if self.refsep is not False:
            return self.refsep
        foundsetting = False
        vals = {}
        for k, v in ptrefsepvals.items():
            if v in self.dict:
                foundsetting = True
                vals[k] = re.sub(r"^(.*?)(\|.*)?$", r"\1", self.dict[v])
        if not foundsetting:
            self.refsep = None
        else:
            if self.dict.get('NoSpaceBetweenBookAndChapter', False):
                vals['bkc'] = ''
            self.refsep = RefSeparators(**vals)
        return self.refsep

    def saveAs(self, fname):
        import xml.etree.ElementTree as et
        settings = et.Element("ScriptureText")
        settings.text = "\n    "
        settings.tail = "\n"
        for k, v in sorted(self.dict.items()):
            n = et.SubElement(settings, k)
            n.text = str(v)
            n.tail = "\n    "
        n.tail = "\n"
        with open(fname, "wb") as outf:
            outf.write(et.tostring(settings, encoding="utf-8"))
