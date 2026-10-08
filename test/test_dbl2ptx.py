#!/usr/bin/python3
# Tests for dbl2ptx: DBL bundle -> PTXprint configuration and archive.
# Uses unittest classes so that conftest's project parametrisation doesn't apply.

import unittest, os, shutil, tempfile, configparser, re
import xml.etree.ElementTree as et
from zipfile import ZipFile
from collections import Counter

def _stub_gi():
    """ ptxprint.view imports Gtk indirectly (report -> parlocs -> gtkutils). Tests
        don't need a display, so provide a stub if gi isn't usable here. """
    import sys, types
    from unittest import mock
    try:
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk
        return
    except (ImportError, ValueError):
        pass
    for k in [k for k in sys.modules if k == "gi" or k.startswith("gi.")]:
        del sys.modules[k]
    gi = types.ModuleType("gi")
    gi.require_version = lambda *a, **kw: None
    repo = types.ModuleType("gi.repository")
    for n in ("Gtk", "Gdk", "GLib", "GObject", "Pango", "GdkPixbuf", "Poppler"):
        setattr(repo, n, mock.MagicMock(name=n))
    gi.repository = repo
    sys.modules["gi"] = gi
    sys.modules["gi.repository"] = repo

from ptxprint import dbl2ptx
from ptxprint.dbl import readDBLMetadata, UnpackDBL, guessBookFile, BundleZip
from ptxprint.usxutils import Usfm

testdir = os.path.dirname(os.path.abspath(__file__))
metadir = os.path.join(testdir, "dbl", "metadata")
fontsdir = os.path.join(testdir, "fonts")
basecfg = os.path.join(testdir, "projects", "WSGlatin", "shared", "ptxprint", "Default", "ptxprint.cfg")

def metafile(prefix):
    for f in os.listdir(metadir):
        if f.startswith(prefix):
            return os.path.join(metadir, f)
    raise FileNotFoundError(prefix)

LDML = """<?xml version="1.0" encoding="utf-8"?>
<ldml xmlns:sil="urn://www.sil.org/ldml/0.1">
  <identity><language type="{lang}"/></identity>
  <localeDisplayNames><languages><language type="{lang}">{autonym}</language></languages></localeDisplayNames>
  <layout><orientation><characterOrder>{order}</characterOrder></orientation></layout>
  <special><sil:external-resources>{fonts}</sil:external-resources></special>
</ldml>
"""

STYLES = """<?xml version="1.0" encoding="utf-8"?>
<stylesheet><property name="font-family">{font}</property><property name="font-size" unit="pt">12</property></stylesheet>
"""

class StubFinder:
    """ A FontFinder that never goes to the network """
    def __init__(self, langfams=None):
        self.langfams = langfams or ([], {})
        self.asked = []
    def lang_families(self, langtag):
        self.asked.append(langtag)
        return self.langfams
    def family(self, name):
        return None
    def fetch_family(self, finfo, destdir):
        res = []
        for f in finfo.get("files", {}):
            src = os.path.join(fontsdir, f)
            if os.path.exists(src):
                os.makedirs(destdir, exist_ok=True)
                shutil.copy(src, destdir)
                res.append(os.path.join(destdir, f))
        return res

def usfm2usx(usfm):
    with tempfile.NamedTemporaryFile("w", suffix=".usfm", delete=False, encoding="utf-8") as outf:
        outf.write(usfm)
        fname = outf.name
    try:
        doc = Usfm.readfile(fname)
        return et.tostring(doc.getroot(), encoding="unicode")
    finally:
        os.unlink(fname)

def make_bundle(path, metaprefix, books, ldml=None, stylesfont=None, fontfiles=(), metaedit=None):
    """ Creates a DBL bundle zip at path from a real metadata sample and the given
        {bookid: usfm} books, which replace the publication's contents """
    meta = et.parse(metafile(metaprefix)).getroot()
    pub = meta.find('publications/publication[@default="true"]')
    if pub is None:
        pub = meta.find('publications/publication')
    struct = pub.find('structure')
    for c in list(struct):
        struct.remove(c)
    for bk in books:
        et.SubElement(struct, "content", {"name": "book-" + bk.lower(), "src": "release/USX_1/{}.usx".format(bk), "role": bk})
    if metaedit is not None:
        metaedit(meta)
    ldmlname = (meta.findtext("language/ldml") or meta.findtext("language/iso")) + ".ldml"
    with ZipFile(path, "w") as zf:
        zf.writestr("metadata.xml", et.tostring(meta, encoding="unicode"))
        for bk, usfm in books.items():
            zf.writestr("release/USX_1/{}.usx".format(bk), usfm2usx(usfm))
        if ldml is not None:
            zf.writestr("release/" + ldmlname, ldml)
        if stylesfont is not None:
            zf.writestr("release/styles.xml", STYLES.format(font=stylesfont))
        zf.writestr("release/versification.vrs", "# custom\nMAT 1:25\n")
        for f in fontfiles:
            zf.write(os.path.join(fontsdir, f), "release/" + f)
    return path

SAPOSA_MRK = r"""\id MRK
\h Mak
\toc1 Rof Foun Ten Mak
\toc2 Mak
\mt1 Mak
\c 1
\s1 Jon u vurungan
\p \v 1 U Vurungan Rof Foun ten Gov nane Jisas Krais.\f + \fr 1:1 \ft English note words testament\f* Gov u tara.
\v 2 Rof foun u Jisas Krais ten Gov.
\p \v 3 Nane u vurungan ten Gov, sà̄pà̄ mamaŋ.
"""

SAPOSA_REV = r"""\id REV
\toc1 Rof Foun Ten Revelesen
\toc2 Revelesen
\c 1
\p \v 1 U vurungan ten Jisas Krais, Gov nane.
"""

ARABIC_JHN = """\\id JHN
\\toc2 يوحنا
\\c 1
\\p \\v 1 في البدء كان الكلمة والكلمة كان عند الله ٢٠٢٢.
\\v 2 العهد الجديد بالدارجة التونسية ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨.
\\p \\v 3 ترجمة جديدة للعهد الجديد باللهجة التونسية ٩ ٠.
"""

TAIDAM_MRK = r"""\id MRK
\toc1 Pưn Mak
\toc2 Mak
\c 1
\p \v 1 Khăm kin di ma ʼŭ Pha Chao.
"""

TAIDAM_ACT = r"""\id ACT
\toc1 Pưn Kăn Hĕt
\toc2 Kăn Hĕt
\c 1
\p \v 1 Pha Chao ma kin di.
"""


class TestVisibleText(unittest.TestCase):
    def test_notes_skipped(self):
        txt = "".join(Usfm.readfile(self._file(SAPOSA_MRK)).visibleText())
        self.assertIn("Vurungan", txt)
        self.assertNotIn("English", txt)
        self.assertNotIn("Rof Foun Ten Mak", txt)       # toc is a header
        words = set()
        c = Usfm.readfile(self._file(SAPOSA_MRK)).collectClusters(words=words)
        self.assertNotIn("testament", words)
        self.assertIn("gov", words)
        self.assertIn("à̄", c)                           # multi codepoint cluster

    def _file(self, text):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d)
        p = os.path.join(d, "t.usfm")
        with open(p, "w", encoding="utf-8") as outf:
            outf.write(text)
        return p


class TestDBL(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)

    def test_guessbook(self):
        self.assertEqual(guessBookFile("41MATxyz.SFM")[0], "MAT")
        self.assertEqual(guessBookFile("release/USX_1/1CO.usx"), ("1CO", "usx"))

    def test_unpack(self):
        z = make_bundle(os.path.join(self.tmp, "b.zip"), "sps", {"MRK": SAPOSA_MRK, "REV": SAPOSA_REV},
                        ldml=LDML.format(lang="sps", autonym="Saposa", order="left-to-right", fonts=""))
        with BundleZip(z) as zf:
            info = readDBLMetadata(zf)
            self.assertEqual(info.scriptcode, "Latn")
            self.assertEqual(info.langtag, "sps")
            self.assertEqual(info.ldmlfile, "release/sps.ldml")
            self.assertTrue(UnpackDBL(zf, "SPS", self.tmp, info=info))
        prj = os.path.join(self.tmp, "SPS")
        self.assertTrue(os.path.exists(os.path.join(prj, "sps.ldml")))
        self.assertTrue(os.path.exists(os.path.join(prj, "custom.vrs")))
        st = et.parse(os.path.join(prj, "ptxSettings.xml")).getroot()
        bp = st.findtext("BooksPresent")
        self.assertEqual(bp.count("1"), 2)
        self.assertEqual(st.findtext("LanguageIsoCode"), "sps")
        bn = et.parse(os.path.join(prj, "BookNames.xml")).getroot()
        self.assertIsNotNone(bn.find('book[@code="GEN"]'))

    def test_ldml_names(self):
        f = dbl2ptx.__dict__.get("_findLdml") or __import__("ptxprint.dbl", fromlist=["_findLdml"])._findLdml
        self.assertEqual(f({"release/aeb-Arab-TN.ldml"}, "", "aeb", "aeb-Arab-TN"), "release/aeb-Arab-TN.ldml")
        self.assertEqual(f({"release/ldml.xml"}, "", "xyz", "xyz"), "release/ldml.xml")
        self.assertEqual(f({"release/azz_es.ldml", "release/azz-Latn.ldml"}, "", "azz", "azz"), "release/azz-Latn.ldml")
        self.assertEqual(f({"release/mil_mil.ldml"}, "", "mil", "mil"), "release/mil_mil.ldml")


class TestTitles(unittest.TestCase):
    def _info(self, prefix, books):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        z = make_bundle(os.path.join(tmp, "b.zip"), prefix, books)
        info = dbl2ptx.importSource(z, tmp)
        stats = dbl2ptx.analyseText(info)
        return info, stats

    def test_saposa(self):
        info, stats = self._info("sps", {"MRK": SAPOSA_MRK, "REV": SAPOSA_REV})
        mt, st, cands = dbl2ptx.chooseTitles(info, stats)
        self.assertEqual(mt.text, "U Vurungan Rof Foun Ten Gov Nane Jisas Krais")
        self.assertTrue(st is None or not re.search(r"(?i)testament|\bNT\b", st.text))

    def test_arabic(self):
        info, stats = self._info("aeb", {"JHN": ARABIC_JHN})
        mt, st, cands = dbl2ptx.chooseTitles(info, stats)
        self.assertEqual(mt.text, "العهد الجديد بالدارجة التونسية")
        self.assertEqual(st.text, "ترجمة جديدة للعهد الجديد باللهجة التونسية")
        self.assertEqual(dbl2ptx.digitMapping(stats, info.numerals)[0], "arabic-indic")
        self.assertEqual(info.direction, "rtl")

    def test_fallback(self):
        info, stats = self._info("blt", {"MRK": TAIDAM_MRK, "ACT": TAIDAM_ACT})
        mt, st, cands = dbl2ptx.chooseTitles(info, stats)
        self.assertEqual(mt.text, "Thai Den")           # language/nameLocal
        bn = info.booknames
        self.assertEqual(st.text, "{} – {}".format(bn["MRK"][1], bn["ACT"][1]))

    def test_cleaning(self):
        info = dbl2ptx.ProjectInfo("x", "x", langname="Mixtec, Peñoles", autonym="Mixtec, Peñoles")
        self.assertEqual(dbl2ptx.cleanTitle("Mixtec, Peñoles: Tnúhu ní cáháⁿ", info), ["Tnúhu ní cáháⁿ"])
        self.assertEqual(dbl2ptx.cleanTitle("Loina Tabu Auwauna NT", info), ["Loina Tabu Auwauna"])
        self.assertEqual(dbl2ptx.cleanTitle("Sa'a NT [apb] -Solomon Islands (DBL 2016)", info), ["Sa'a"])

    def test_frt(self):
        frt = "\\id FRT\n\\periph Title Page|id=\"title\"\n\\mt2 Pretitle\n\\mt1 Main Title\n\\mt3 Sub\n\\periph Foreword\n\\mt1 Other\n"
        res = dbl2ptx.titlesFromUsfm(frt, "FRT")
        self.assertEqual(res[0].text, "Main Title")
        self.assertEqual(res[1].text, "Sub")


class TestMeasure(unittest.TestCase):
    font = os.path.join(fontsdir, "CharisSIL-Regular.ttf")

    def test_stacking(self):
        base = dbl2ptx.measureText(self.font, Counter({"a": 10}), script="latn")
        stacked = dbl2ptx.measureText(self.font, Counter({"a\u0301\u0304": 10}), script="latn")
        self.assertGreater(stacked.top, base.top)

    def test_in_context(self):
        # a Myanmar stack measured in its word hangs below the baseline; its consonant alone doesn't
        padauk = os.path.join(fontsdir, "Padauk-Regular.ttf")
        word = dbl2ptx.measureText(padauk, Counter({"\u1000\u1039\u1000": 1}), script="mymr")
        alone = dbl2ptx.measureText(padauk, Counter({"\u1000": 1}), script="mymr")
        self.assertGreater(word.depthmax, alone.depthmax)

    def test_rare_descenders(self):
        # a few deep descenders hardly change the spacing; common ones do
        common = Counter({"name": 1000, "man": 1000, "time": 1000})
        rare = common + Counter({"gypsy": 5})
        many = common + Counter({"gypsy": 1000})
        ls = [dbl2ptx.sizeFromMeasurement(dbl2ptx.measureText(self.font, c, c, script="latn"), textsize=10).linespacing
              for c in (common, rare, many)]
        self.assertLessEqual(ls[1] - ls[0], 0.1)
        self.assertGreater(ls[2] - ls[0], 0.3)

    def test_size(self):
        m = dbl2ptx.Measurement(1000, top=800, depth=250, basetop=550)
        dbl2ptx.sizeFromMeasurement(m, textsize=10, gap=0.45, mingap=0.5)
        self.assertAlmostEqual(m.fontsize, round(10 * dbl2ptx.REF_BASE_TOP / 0.55, 2), places=2)
        self.assertAlmostEqual(m.linespacing, round((1.05 + 0.45) * m.fontsize, 1))
        self.assertFalse(m.floored)

    def test_mingap(self):
        m = dbl2ptx.sizeFromMeasurement(dbl2ptx.Measurement(1000, top=800, depth=250, basetop=737),
                                        textsize=10, gap=0.01, mingap=2)
        self.assertTrue(m.floored)
        self.assertAlmostEqual(m.linespacing, round(1.05 * 10 + 2, 1))

    def test_spacing_table(self):
        self.assertEqual(dbl2ptx.spacingGap("normal", "Latn", "Charis SIL"), (0.45, "default"))
        self.assertEqual(dbl2ptx.spacingGap("tight", "Arab", "Scheherazade New"), (0.18, "Arab"))
        self.assertEqual(dbl2ptx.spacingGap("loose", "Arab", "Awami Nastaliq"), (0.52, "default"))
        self.assertEqual(dbl2ptx.spacingGap("normal", "Aran", "Some Font")[1], "default")
        tall = dbl2ptx.Measurement(1000, top=1400, depth=300, basetop=600)
        self.assertEqual(dbl2ptx.spacingGap("normal", "Arab", "Unknown", tall)[1], "default")


class TestEndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _stub_gi()

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        from ptxprint.font import cachepath
        cachepath(fontsdir)

    def test_bundle_to_archive(self):
        z = make_bundle(os.path.join(self.tmp, "sps.zip"), "sps", {"MRK": SAPOSA_MRK, "REV": SAPOSA_REV},
                        ldml=LDML.format(lang="sps", autonym="Saposa", order="left-to-right",
                                         fonts='<sil:font name="Charis SIL" features="cv43=2" types="default"/>'),
                        stylesfont="Nonexistent Font")
        out = os.path.join(self.tmp, "out.zip")
        res = dbl2ptx.main([z, "-c", basecfg, "-o", out, "--keep", os.path.join(self.tmp, "work")],
                           finder=StubFinder())
        self.assertEqual(res, 0)
        with ZipFile(out) as zf:
            names = zf.namelist()
            cfgname = [n for n in names if n.endswith("shared/ptxprint/Default/ptxprint.cfg")][0]
            cp = configparser.ConfigParser(interpolation=None)
            cp.read_string(zf.read(cfgname).decode("utf-8"))
            self.assertTrue(any(n.endswith(".usfm") or n.endswith(".USFM") for n in names))
            self.assertTrue(any(n.endswith("sps.ldml") for n in names))
        self.assertTrue(cp.get("document", "fontregular").startswith("Charis SIL|"))
        self.assertIn("cv43=2", cp.get("document", "fontregular"))
        self.assertEqual(cp.get("document", "ifrtl"), "ltr")
        self.assertEqual(cp.get("document", "script"), "Latn")
        self.assertEqual(cp.get("vars", "maintitle"), "U Vurungan Rof Foun Ten Gov Nane Jisas Krais")
        self.assertEqual(cp.get("project", "booklist"), "MRK REV")
        self.assertGreater(float(cp.get("paragraph", "linespacing")), float(cp.get("paper", "fontfactor")))

    def test_usfm_dir(self):
        src = os.path.join(self.tmp, "src")
        os.makedirs(src)
        for bk, t in (("MRK", SAPOSA_MRK), ("REV", SAPOSA_REV)):
            with open(os.path.join(src, bk + ".usfm"), "w", encoding="utf-8") as outf:
                outf.write(t)
        info = dbl2ptx.importSource(src, os.path.join(self.tmp, "p"), "SRC")
        stats = dbl2ptx.analyseText(info)
        self.assertEqual(stats.bookorder, ["MRK", "REV"])
        self.assertEqual(stats.mainscript, "Latn")

    def test_paratext_dir(self):
        src = os.path.join(testdir, "projects", "WSGlatin")
        info = dbl2ptx.importSource(src, os.path.join(self.tmp, "p"))
        self.assertEqual(info.prjid, "WSGlatin")
        self.assertFalse(os.path.exists(os.path.join(info.prjpath, "shared", "ptxprint")))
        self.assertTrue(any(c.forced for c in info.titles))      # from earlier configs or FRTlocal


if __name__ == "__main__":
    unittest.main()
