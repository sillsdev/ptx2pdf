import os, re
import xml.etree.ElementTree as et
import regex
from ptxprint.utils import allbooks, books, bookcodes, chaps
from ptxprint.unicode.UnicodeSets import flatten


class ParatextSettings:
    def __init__(self, basedir, prjid):
        self.dict = {}
        self.ldml = None
        self.basedir = basedir
        self.prjid = prjid
        self.langid = None
        self.dir = "left"
        self.collation = None
        self.parse()

    def parse(self):
        path = os.path.join(self.basedir, self.prjid, "Settings.xml")
        pathmeta = os.path.join(self.basedir, self.prjid, "metadata.xml")
        for a in ("Settings.xml", "ptxSettings.xml"):
            path = os.path.join(self.basedir, self.prjid, a)
            if os.path.exists(path):
                doc = et.parse(path)
                for c in doc.getroot():
                    self.dict[c.tag] = c.text
                self.calcbookspresent()
                self.read_ldml()
                break
        else:
            self.inferValues()
        path = os.path.join(self.basedir, self.prjid, "BookNames.xml")
        if os.path.exists(path):
            self.read_bookNames(path)
            self.hasLocalBookNames = True
        else:
            self.default_bookNames()
            self.hasLocalBookNames = False
        self.collation = None
        return self

    def read_ldml(self):
        self.langid = re.sub('-(?=-|$)', '', self.get('LanguageIsoCode', "unk").replace(":", "-"))
        fname = os.path.join(self.basedir, self.prjid, self.langid+".ldml")
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
        return self.bookStrs.get(s, [s]*(level+1))[level]

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

    def inferValues(self):
        path = os.path.join(self.basedir, self.prjid)
        sfmfiles = [x for x in os.listdir(path) if x.lower().endswith("sfm")]
        for f in sfmfiles:
            m = re.search(r"(\d{2})", f)
            if not m:
                continue
            bk = allbooks[int(m.group(1))-1]
            bki = f.lower().find(bk.lower())
            if bki < 0:
                continue
            numi = m.start(1)
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
        self.dict['DefaultFont'] = ""
        self.dict['Encoding'] = 65001
        self.calcbookspresent()

    def calcbookspresent(self):
        self.bookmap = {}
        booksfound = set()
        bookspresent = [0] * len(allbooks)
        path = os.path.join(self.basedir, self.prjid)
        if 'FileNameBookNameForm' in self.dict:
            fbkfm = self.dict['FileNameBookNameForm']
            bknamefmt = self.get('FileNamePrePart', "") + \
                        fbkfm.replace("MAT","{bkid}").replace("41","{bkcode}") + \
                        self.get('FileNamePostPart', "")
            for k, v in books.items():
                fname = bknamefmt.format(bkid=k, bkcode=v+1)
                if os.path.exists(os.path.join(path, fname)):
                    bookspresent[v-1] = 1
                    self.bookmap[k] = fname
                    booksfound.add(fname)
        for f in os.listdir(path):
            if not f.lower().endswith("sfm") or f in booksfound:
                continue
            with open(os.path.join(path, f), encoding="utf-8") as inf:
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
            path = os.path.join(self.basedir, self.prjid, a)
            if os.path.exists(path):
                res[path] = a
        if self.langid is None:
            return res
        fname = os.path.join(self.basedir, self.prjid, self.langid+".ldml")
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
