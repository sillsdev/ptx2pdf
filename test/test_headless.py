''' Crash tests for headless ptxprint that run in process and don't run XeTeX.

    Most load a config from a copy of a test project, change some settings and then
    make the TeX file, as a print does, checking nothing raises an exception.
    Tests are unittest classes so test/conftest.py does not parametrize them as projects.

    PTXPRINT_ZOODIRS (a list of project directories, separated by os.pathsep) also loads
    and makes the TeX for every config found in those projects.
'''

import sys, os, io, re, copy, shutil, tempfile, unittest, contextlib, configparser, traceback
import pytest

testsdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(testsdir, "..", "python", "lib"))

from ptxprint.main import main
from ptxprint import runjob
from ptxprint.runjob import RunJob
from ptxprint.modelmap import ModelMap
from ptxprint.piclist import Piclist, Picture
from ptxprint.interlinear import Interlinear
from ptxprint.dimension import Dimension
import ptxprint.view as ptxview

def copyproject(destdir, prj="WSGlatin"):
    ''' Copy a test project without its outputs '''
    dest = os.path.join(destdir, prj)
    shutil.copytree(os.path.join(testsdir, "projects", prj), dest,
                    ignore=lambda d, fs: ["local"] if os.path.basename(d) == prj else [])
    return dest

def loadview(prjdir, prj, cfg):
    ''' Returns the ViewModel that a headless print of this config uses '''
    oldargv = sys.argv
    sys.argv = ["ptxprint", "-p", prjdir, "--testsuite", "--nofontcache", "-f", os.path.join(testsdir, "fonts"),
                "-z", "16", "-l", "critical", "--logfile=none", "-P", "-c", cfg, prj]
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            view = main(retview=True)
    finally:
        sys.argv = oldargv
    view.doError = lambda *a, **kw: None
    return view

def maketex(view):
    ''' Do all of a print except running XeTeX '''
    job = RunJob(view, view.scriptsdir, view.scriptsdir, view.args)
    job.norun = True
    job.nothreads = True
    cwd = os.getcwd()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            job.doit(noview=True)
    finally:
        runjob.unlockme()
        os.chdir(cwd)       # norun leaves us in the job's folder
    return job

def failsite(e):
    ''' Where in ptxprint an exception came from '''
    tb = traceback.extract_tb(e.__traceback__)
    return next((f"{os.path.basename(f.filename)}:{f.lineno}" for f in reversed(tb) if "ptxprint" in f.filename), "?")

class Mutator:
    ''' Applies changes to a loaded view, putting it back as loaded before each one '''
    def __init__(self, view):
        self.view = view
        self.base = copy.deepcopy(view.dict)
        self.attrs = {w[0]: getattr(view, w[0], None) for w in view._attributes.values()}

    def reset(self):
        self.view.dict = copy.deepcopy(self.base)
        for k, v in self.attrs.items():
            setattr(self.view, k, v)

    def tryall(self, changes):
        ''' changes is a list of (label, fn(view)). Returns {(exception, site): [labels]} '''
        fails = {}
        for label, fn in changes:
            self.reset()
            try:
                fn(self.view)
                maketex(self.view)
            except Exception as e:
                fails.setdefault((type(e).__name__, failsite(e)), []).append(f"{label}: {str(e)[:100]}")
        self.reset()
        return fails

def report(fails):
    return "\n".join(f"{k[0]} at {k[1]} for {len(v)} cases, e.g. {v[:3]}" for k, v in sorted(fails.items()))

def widgetvalues():
    ''' {widget: [values]} for the combo boxes and radio buttons in the UI that the ModelMap uses '''
    import xml.etree.ElementTree as et
    root = et.parse(os.path.join(os.path.dirname(ptxview.__file__), "ptxprint.glade")).getroot()
    objs = {o.get("id"): o for o in root.iter("object") if o.get("id")}
    def prop(o, n):
        return next((p.text for p in o.findall("property") if p.get("name") == n), None)
    widgets = {v.widget for v in ModelMap.values() if v.widget}
    res = {}
    for wid, o in objs.items():
        if wid.startswith("fcb_") and wid in widgets and prop(o, "model") in objs:
            col = int(prop(o, "id-column") or 0)
            res[wid] = [c.text for r in objs[prop(o, "model")].iter("row")
                                    for c in r.findall("col") if int(c.get("id")) == col]
        elif wid.startswith("r_") and wid.count("_") > 1:
            (_, grp, val) = wid.split("_", 2)
            if "r_" + grp in widgets:
                res.setdefault("r_" + grp, []).append(val)
    return res


class TestPiclistParsing(unittest.TestCase):

    def test_bad_lines(self):
        ''' Lines without a reference are skipped '''
        pl = Piclist(None)
        pl.read_piclist(io.StringIO("% comment\nJON\nJON|src=\"a.jpg\"\n\n"
                                    "JON 1.3 Caption|src=\"a.jpg\" size=\"col\" pgpos=\"t\" ref=\"1.3\"\n"))
        self.assertEqual(["JON 1.3"], [p['anchor'] for p in pl.get_pics()])

    def test_usfm2_line(self):
        pl = Piclist(None)
        pl.read_piclist(io.StringIO("JON 3.6 Caption|a.jpg|col|tl||copy|caption|3.6\n"))
        self.assertEqual(1, len(pl.get_pics()))

    def test_bad_scale(self):
        ''' A scale that isn't a number doesn't stop the piclist being written '''
        pl = Piclist(None)
        pl.read_piclist(io.StringIO('JON 1.4 Bad|src="a.jpg" size="col" pgpos="t" scale="big" ref="1.4"\n'
                                    'JON 1.5 Empty|src="b.jpg" size="col" pgpos="t" scale="" ref="1.5"\n'))
        for p in pl.get_pics():
            p.outstr()

class TestOddInputs(unittest.TestCase):

    def test_interlinear_no_lexicon(self):
        with tempfile.TemporaryDirectory() as d:
            il = Interlinear("en", d)
            self.assertEqual({}, il.lexicon)

    def test_dimension(self):
        for s, v in (("12mm", 12 * 72.27 / 25.4), ("3pt", 3.), ("", 0.), ("junk", 0.), ("1in", 72.27)):
            self.assertAlmostEqual(v, Dimension(s).asunits("pt"), places=3)

class TestChanges(unittest.TestCase):
    """ Odd lines in a changes.txt are reported, not crashed on """
    lines = ['"a" > "b"', '"(" > "x"', '"a" > "\\9"', 'at JHN 3 "a" > "b"', 'at XYZ 99:99 "a" > "b"',
             'in "\\v (" : "a" > "b"', '"a" >', '> "b"', 'include "nothere.txt"', 'sfm "q" > "p"',
             '"a" > "b" "c"', 'at JHN 3:16-JHN "a" > "b"', '"\\u12" > "x"', '"a" > "\\g<nope>"',
             'at JHN;JAS "a" > "b"', 'at JHN 3:16 in "x": in "(" : "a" > "b"', '"\\" > "x"', '"a"x > "b"',
             '"" > "x"', 'in "" : "a" > "b"', '"(a)" > "\\2"', '"a" > "$nofn{x}"', '"a" > "$upper{"',
             'at JHN 99 "a" > "b"', '"a" > "\\u00"']
    text = "\\id JHN\n\\c 1\n\\p\n\\v 1 In the beginning a word\n\\v 2 another (word)\n\\c 3\n\\v 16 For God so loved\n"

    def test_lines(self):
        from ptxprint.changes import readChanges
        from ptxprint.utils import runChanges
        fails = []
        with tempfile.TemporaryDirectory() as d:
            fname = os.path.join(d, "changes.txt")
            for l in self.lines:
                with open(fname, "w", encoding="utf-8") as outf:
                    outf.write(l + "\n")
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        changes = readChanges(fname, "JHN", doError=lambda *a, **kw: None)
                        runChanges(changes, "JHN", self.text, errorfn=lambda *a, **kw: None)
                except Exception as e:
                    fails.append(f"{l}: {type(e).__name__} {e} at {failsite(e)}")
        self.assertFalse(fails, "\n".join(fails))

class TestHyphenation(unittest.TestCase):
    """ Hyphenation lists with odd entries """

    def test_odd_words(self):
        from ptxprint.hyphen import Hyphenation
        h = Hyphenation({"ab]c": "ab-]c", "x\\y": "x-\\y", "^up": "^-up", "nor(mal": "nor-(mal", "": ""})
        h.analyse()
        h.hyphenate("a nor(mal ab]c word ^up", "-")

    def test_print(self):
        with tempfile.TemporaryDirectory() as d:
            copyproject(d, "WSGlatin")
            with open(os.path.join(d, "WSGlatin", "shared", "ptxprint", "hyphen-WSGlatin.tex"), "w", encoding="utf-8") as outf:
                outf.write("\\hyphenation{\n% a comment\nbo-āzna\nnao-mī\nab-]c\n^-up\nx-\\y\n\n}\n")
            view = loadview(d, "WSGlatin", "DecorRUT")
            view.set("c_hyphenate", True)
            view.set("c_letterSpacing", True)
            maketex(view)

class TestAdjList(unittest.TestCase):
    """ Odd lines in an adjust list """
    lines = ["RUT 1.1 0 % \\p 98", "RUT", "RUT 1.1", "RUT 1.1 x", "RUT x.y 1", "RUT 1.1 +1[2]", "RUT 1.1 -1 % \\p",
             "RUT 1.1 0 % \\p abc", "% comment", "", "RUT 1.1 0 %", "RUT 1.1[3] +2", "RUT 1.1 2 mrk=q", "XYZ 1.1 1",
             "\ufeffRUT 1.1 1", "RUT 1.1 1e5", "RUT 1.1 *", "RUT 1.1 +1 % \\p 98 % \\q 50", "RUT 1:1 1", "RUT 1.1.2 1"]

    def test_lines(self):
        from ptxprint.adjlist import AdjList
        with tempfile.TemporaryDirectory() as d:
            fname = os.path.join(d, "test.adj")
            with open(fname, "w", encoding="utf-8") as outf:
                outf.write("\n".join(self.lines) + "\n")
            a = AdjList(90, 95, 105)
            a.readAdjlist(fname)
            for i in range(len(a)):
                a.genline(i)
            a.createAdjlist(fname + ".out")

class TestUIDefaults(unittest.TestCase):
    ''' Headless, settings missing from a config take the UI's defaults '''

    def test_defaults(self):
        d = ptxview.gladeDefaults()
        self.assertGreater(len(d), 200)
        for w in ("s_fontsize", "s_linespacing", "s_margins", "s_topmargin", "fcb_pagesPerSpread", "r_book"):
            self.assertIn(w, d)
        self.assertGreater(float(d["s_fontsize"]), 0)

    def test_combo_defaults_in_model(self):
        ''' A combo box default must be one of its values (GTK ignores an active-id that isn't) '''
        vals = widgetvalues()
        for w, v in ptxview.gladeDefaults().items():
            if w.startswith("fcb_") and vals.get(w):
                self.assertIn(v, vals[w], w)

    def test_spin_clamped(self):
        view = loadview(os.path.join(testsdir, "projects"), "WSGlatin", "Default")
        view.set("s_margins", 0)
        self.assertGreater(float(view.get("s_margins")), 0)
        view.set("s_fontsize", 1000)
        self.assertLessEqual(float(view.get("s_fontsize")), 100)

class _ProjectCopy(unittest.TestCase):
    project = "WSGlatin"
    others = ()         # other projects needed, e.g. for a diglot

    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.TemporaryDirectory()
        for p in (cls.project, ) + cls.others:
            copyproject(cls.tmpdir.name, p)

    @classmethod
    def tearDownClass(cls):
        cls.tmpdir.cleanup()

    def view(self, cfg):
        return loadview(self.tmpdir.name, self.project, cfg)

class TestConfigFuzz(_ProjectCopy):
    ''' Each setting a config can have, read from a config with an odd value '''

    others = ("OGNT", )

    def fuzz(self, cfg):
        view = self.view(cfg)
        m = Mutator(view)
        def setcfg(k, val):
            def fn(v):
                c = configparser.ConfigParser(interpolation=None)
                (s, o) = k.split("/", 1)
                c.add_section(s)
                c.set(s, o, val)
                v.loadConfig(c, clearvars=False)
            return fn
        changes = [(f"{k}={val!r}", setcfg(k, val)) for k in ModelMap if "/" in k and not k.endswith("_")
                        for val in ("junk", "")]
        fails = m.tryall(changes)
        self.assertFalse(fails, report(fails))

    def test_fuzz(self):
        self.fuzz("Default")

    @pytest.mark.slow
    def test_fuzz_cover(self):
        self.fuzz("Cover")

    @pytest.mark.slow
    def test_fuzz_diglot(self):
        self.fuzz("Diglot2JN")

class TestConfigUpgrade(_ProjectCopy):
    """ Old configs, each with the settings that one of the upgrade steps changes """
    others = ("OGNT", )
    cases = {
        "v2_14": ("2.14", {"config/pwd": "secret", "project/plugins": "ornaments, other"}),
        "v2_16": ("2.16", {"fancy/pageborder": "True", "fancy/enableborders": "True", "fancy/sectionheader": "True"}),
        "v2_17": ("2.17", {"project/ifstarthalfpage": "True"}),
        "v2_18": ("2.18", {"document/pagefullfactor": "0.9", "document/afterchapterspace": "junk"}),
        "v2_19": ("2.19", {"paper/bottomrag": "junk"}),
        "v2_20": ("2.20", {}),
        "v2_21": ("2.21", {"snippets/adjlabelling": "True", "snippets/paralabelling": "junk"}),
        "v2_22": ("2.22", {"paper/ifgrid": "False"}),
        "v2_23": ("2.23", {"snippets/diglot": "True", "document/diglotsecprj": "OGNT", "document/diglotsecconfig": "Default",
                           "document/diglotprifraction": "junk", "document/diglotpicsources": "both",
                           "document/diglotswapside": "True", "paper/fontfactor": ""}),
        "v2_24": ("2.24", {"project/iffrontmatter": "False", "cover/makecoverpage": "True"}),
        "v3_00": ("3.00", {"texpert/vhyphen": "True", "texpert/vhyphenup": "True"}),
        "v3_01": ("3.01", {"document/diglotmergemode": "doc"}),
        "v3_02": ("3.02", {"fancy/sectionheadershift": "junk"}),
        "vjunk": ("junk", {"covergen/borderstyle": "c86out", "header/chvseparator": "True"}),
        "vempty": ("", {"header/chvseparator": "False"}),
        "vnone": (None, {}),
    }

    def test_upgrade(self):
        cfgsdir = os.path.join(self.tmpdir.name, self.project, "shared", "ptxprint")
        for name, (version, settings) in self.cases.items():
            c = configparser.ConfigParser(interpolation=None)
            c.read(os.path.join(cfgsdir, "Default", "ptxprint.cfg"), encoding="utf-8")
            c.set("config", "name", name)
            if version is None:
                c.remove_option("config", "version")
            else:
                c.set("config", "version", version)
            for k, v in settings.items():
                (sect, opt) = k.split("/", 1)
                if not c.has_section(sect):
                    c.add_section(sect)
                c.set(sect, opt, v)
            os.makedirs(os.path.join(cfgsdir, name, "adjLists"))
            with open(os.path.join(cfgsdir, name, "adjLists", "bogus.adj"), "w", encoding="utf-8") as outf:
                outf.write("This file doesn't exist yet.\n")
            with open(os.path.join(cfgsdir, name, "ptxprint.cfg"), "w", encoding="utf-8") as outf:
                c.write(outf)
        fails = []
        for name in self.cases:
            try:
                maketex(self.view(name))
            except Exception as e:
                fails.append(f"{name}: {type(e).__name__} {str(e)[:100]} at {failsite(e)}")
        self.assertFalse(fails, "\n".join(fails))

def _edit(path, fn):
    with open(path, encoding="utf-8") as inf:
        dat = inf.read()
    with open(path, "w", encoding="utf-8") as outf:
        outf.write(fn(dat))

class TestBrokenProject(unittest.TestCase):
    """ Project and config files that are missing, corrupt or odd """

    cases = {
        "no BookNames": lambda p: os.remove(os.path.join(p, "BookNames.xml")),
        "bad BookNames": lambda p: open(os.path.join(p, "BookNames.xml"), "w").write("<BookNames><book code=\"2JN\" abbr=\"\"/><book/>"),
        "empty BookNames": lambda p: open(os.path.join(p, "BookNames.xml"), "w").write(""),
        "no ldml": lambda p: os.remove(os.path.join(p, "wsg-Latn.ldml")),
        "bad ldml": lambda p: open(os.path.join(p, "wsg-Latn.ldml"), "w").write("<ldml><collations><collation type=\"standard\"><cr><![CDATA[&a < b <<"),
        "settings no naming": lambda p: _edit(os.path.join(p, "Settings.xml"), lambda d: re.sub(r"<Naming[^>]*/>", "", d)),
        "settings odd encoding": lambda p: _edit(os.path.join(p, "Settings.xml"), lambda d: re.sub(r"<Encoding>.*?</Encoding>", "<Encoding>99999</Encoding>", d) if "<Encoding>" in d else d.replace("</ScriptureText>", "<Encoding>99999</Encoding></ScriptureText>")),
        "settings no versification": lambda p: _edit(os.path.join(p, "Settings.xml"), lambda d: re.sub(r"<Versification>.*?</Versification>", "<Versification>99</Versification>", d)),
        "settings bad xml": lambda p: _edit(os.path.join(p, "Settings.xml"), lambda d: d[:len(d)//2]),
        "settings rtl": lambda p: _edit(os.path.join(p, "Settings.xml"), lambda d: d.replace("</ScriptureText>", "<RightToLeft>T</RightToLeft><LanguageIsoCode>xyz:::</LanguageIsoCode></ScriptureText>")),
        "no settings": lambda p: os.remove(os.path.join(p, "Settings.xml")),
        "bad custom.sty": lambda p: open(os.path.join(p, "custom.sty"), "w").write("\\Marker\n\\FontSize big\n\\Marker q\n\\TextProperties paragraph\n\\Endmarker\n\\Color 999999999\n"),
        "bad ptxprint_project.cfg": lambda p: open(os.path.join(p, "shared", "ptxprint", "ptxprint_project.cfg"), "w").write("[paper]\nmargins = junk\n[project\n"),
        "bad picInfo": lambda p: open(os.path.join(p, "shared", "ptxprint", "picInfo.txt"), "w").write("[x.jpg]\ncopy = \n[\n"),
        "bad changes": lambda p: open(os.path.join(p, "PrintDraftChanges.txt"), "w").write('"(" > "x"\nat XYZ "a" > "b"\n'),
        "binary book": lambda p: open(os.path.join(p, "642JNWSGlatin.SFM"), "wb").write(b"\\id 2JN\n\xff\xfe\x00\x01 \\c 1\n\\v 1 \x80\x81"),
        "empty book": lambda p: open(os.path.join(p, "642JNWSGlatin.SFM"), "w").write(""),
        "id mismatch": lambda p: _edit(os.path.join(p, "642JNWSGlatin.SFM"), lambda d: d.replace("\\id 2JN", "\\id 3JN")),
        "no id": lambda p: _edit(os.path.join(p, "642JNWSGlatin.SFM"), lambda d: re.sub(r"^\\id [^\n]*\n", "", d)),
        "cfg syntax": lambda p: _edit(os.path.join(p, "shared/ptxprint/Default/ptxprint.cfg"), lambda d: d.replace("[paper]", "[paper\nnot a setting")),
        "cfg dup key": lambda p: _edit(os.path.join(p, "shared/ptxprint/Default/ptxprint.cfg"), lambda d: d.replace("[paper]\n", "[paper]\nmargins = 10\nmargins = 12\n")),
        "cfg dup section": lambda p: _edit(os.path.join(p, "shared/ptxprint/Default/ptxprint.cfg"), lambda d: d + "\n[paper]\nmargins = 9\n"),
        "cfg bom": lambda p: _edit(os.path.join(p, "shared/ptxprint/Default/ptxprint.cfg"), lambda d: "\ufeff" + d),
        "cfg empty": lambda p: open(os.path.join(p, "shared/ptxprint/Default/ptxprint.cfg"), "w").write(""),
        "cfg binary": lambda p: open(os.path.join(p, "shared/ptxprint/Default/ptxprint.cfg"), "wb").write(b"\x00\xff[paper]\x80"),
    }

    def test_broken(self):
        fails = []
        for name, fn in self.cases.items():
            with tempfile.TemporaryDirectory() as d:
                copyproject(d, "WSGlatin")
                fn(os.path.join(d, "WSGlatin"))
                try:
                    view = loadview(d, "WSGlatin", "Default")
                    view.set("ecb_book", "2JN")
                    view.set("r_book", "single")
                    maketex(view)
                except Exception as e:
                    fails.append(f"{name}: {type(e).__name__} {str(e)[:100]} at {failsite(e)}")
        self.assertFalse(fails, "\n".join(fails))

class TestSettingsSweep(_ProjectCopy):
    ''' Each UI setting changed in turn to each value it can have '''
    others = ("OGNT", )

    def sweep(self, cfg):
        view = self.view(cfg)
        m = Mutator(view)
        vals = widgetvalues()
        changes = []
        def setw(w, val):
            return lambda v: v.set(w, val)
        for w in sorted({x.widget for x in ModelMap.values() if x.widget}):
            cur = m.base.get(w)
            if w.startswith("c_"):
                changes.append((f"{w}={not cur}", setw(w, not cur)))
            elif w in vals:
                changes.extend((f"{w}={x}", setw(w, x)) for x in vals[w] if x != cur)
            elif w.startswith("s_"):
                changes.extend((f"{w}={x}", setw(w, x)) for x in (0, 1, 3, 1000))
            elif w.startswith("t_"):
                changes.extend((f"{w}={x!r}", setw(w, x)) for x in ("", "a%b\\c{d}$#_^&"))
        fails = m.tryall(changes)
        self.assertFalse(fails, report(fails))

    @pytest.mark.slow
    def test_frontmatter(self):
        self.sweep("FrontPHM")

    def test_pictures(self):
        self.sweep("PicsJON")

    @pytest.mark.slow
    def test_oddusfm(self):
        self.sweep("OddUSFM")

    @pytest.mark.slow
    def test_triglot(self):
        self.sweep("Triglot2JN")

class TestPrintMethods(_ProjectCopy):
    ''' Things a headless print or -A can do to a loaded config '''

    def test_saves(self):
        view = self.view("PicsJON")
        view.savePics()
        view.saveStyles()
        view.saveAdjlists()
        maketex(view)

    def test_archive(self):
        view = self.view("FrontPHM")
        outf = os.path.join(self.tmpdir.name, "test.zip")
        with contextlib.redirect_stdout(io.StringIO()):
            view.createArchive(outf, nobuild=True)
        self.assertTrue(os.path.exists(outf))

    def test_books(self):
        view = self.view("Default")
        for bks in ("RUT", "RUT JON", "GEN", "", "JON 2", "RUT 1-2 PHM", "XYZ"):
            view.set("r_book", "multiple")
            view.set("ecb_booklist", bks)
            maketex(view)


zoodirs = [d for d in os.getenv("PTXPRINT_ZOODIRS", "").split(os.pathsep) if d]

@pytest.mark.skipif(not zoodirs, reason="Set PTXPRINT_ZOODIRS to load configs from other projects")
class TestConfigZoo(_ProjectCopy):
    ''' Loads every config in the PTXPRINT_ZOODIRS projects into a copy of WSGlatin and makes the TeX for JON '''

    def test_zoo(self):
        cfgsdir = os.path.join(self.tmpdir.name, self.project, "shared", "ptxprint")
        zoo = {}
        for d in zoodirs:
            for dp, dns, fns in os.walk(d):
                dns[:] = [x for x in dns if x != "local"]
                if "ptxprint.cfg" in fns and re.search(r"[\\/]shared[\\/]ptxprint", dp):
                    name = "Z{}".format(len(zoo) + 1)
                    zoo[name] = os.path.join(dp, "ptxprint.cfg")
                    os.makedirs(os.path.join(cfgsdir, name))
                    shutil.copy(zoo[name], os.path.join(cfgsdir, name, "ptxprint.cfg"))
        view = self.view("Default")
        fails = {}
        for name, path in zoo.items():
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    view.setConfigId(name)
                view.set("r_book", "multiple")
                view.set("ecb_booklist", "JON")
                maketex(view)
            except Exception as e:
                fails.setdefault((type(e).__name__, failsite(e)), []).append(f"{path}: {str(e)[:100]}")
        self.assertFalse(fails, report(fails))


def runptxprint(prjsdir, prj, cfg, *opts, cmd=None):
    ''' Run ptxprint headless as the test suite does. Returns (returncode, output) '''
    import subprocess
    args = [sys.executable, os.path.join(testsdir, "..", "python", "scripts", "ptxprint"), "-p", prjsdir, "-S",
            "--testsuite", "--nofontcache", "-f", os.path.join(testsdir, "fonts"), "-l", "info",
            "--logfile=" + os.path.join(prjsdir, "ptxprint.log"), "-c", cfg] + list(opts) + [prj]
    if cmd is not None:
        args.append(cmd)
    res = subprocess.run(args, cwd=prjsdir, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1200)
    return res.returncode, res.stdout + res.stderr

class _Run(unittest.TestCase):
    projects = ("WSGlatin", )

    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.TemporaryDirectory()
        for p in cls.projects:
            copyproject(cls.tmpdir.name, p)

    @classmethod
    def tearDownClass(cls):
        cls.tmpdir.cleanup()

    def run_ok(self, prj, cfg, *opts, cmd=None):
        rc, out = runptxprint(self.tmpdir.name, prj, cfg, *opts, cmd=cmd)
        self.assertNotIn("Traceback", out, out[-3000:])
        self.assertEqual(0, rc, out[-3000:])
        return out

class TestFill(_Run):
    ''' The page filler, on a short book '''

    def test_fill(self):
        out = self.run_ok("WSGlatin", "Default", "-j", "1", "-b", "2JN", cmd="fill")
        self.assertIn("Complete 2JN", out)

    def test_fill_restart_stop(self):
        self.run_ok("WSGlatin", "Default", "-j", "1", "-b", "2JN", cmd="fill")
        self.run_ok("WSGlatin", "Default", "-j", "1", "-b", "2JN", "--restart", "--stop", cmd="fill")

@pytest.mark.slow
class TestPolyFill(_Run):
    ''' The polyglot filler '''
    projects = ("WSGlatin", "OGNT", "aArp", "aArpBT")

    def test_diglot_fill(self):
        out = self.run_ok("WSGlatin", "Diglot2JN", "-j", "1", cmd="fill")
        self.assertIn("Complete 2JN", out)

    def test_diglot_fill_jas(self):
        shutil.copytree(os.path.join(testsdir, "projects", "aArp", "local", "figures"),
                        os.path.join(self.tmpdir.name, "aArp", "local", "figures"))
        out = self.run_ok("aArp", "TestDiglotA5", "-j", "1", "-b", "JAS", cmd="fill")
        self.assertIn("Complete JAS", out)

class TestCommandLine(_Run):
    ''' Headless command line options with odd values '''

    def test_defines(self):
        self.run_ok("WSGlatin", "Default", "-P", "-b", "2JN", "-D", "c_inclFrontMatter=False",
                    "-D", "t_invisiblePassword=a=b", "-D", "s_fontsize=big", "-D", "fcb_outputFormat=nosuch")

    def test_archive_quality_cover(self):
        ''' PDF 2.0 output (print archive) with a cover to split off '''
        self.run_ok("WSGlatin", "CoverJON", "-P", "-D", "c_printArchive=True")
        self.assertTrue(os.path.exists(os.path.join(self.tmpdir.name, "WSGlatin", "local", "ptxprint", "WSGlatin_CoverJON_JON_ptxp_cover.pdf")))

    def test_missing(self):
        ''' A config or project that doesn't exist '''
        rc, out = runptxprint(self.tmpdir.name, "WSGlatin", "NoSuchConfig", "-P", "-b", "2JN")
        self.assertNotIn("Traceback", out, out[-3000:])
        rc, out = runptxprint(self.tmpdir.name, "NoSuchProject", "Default", "-P")
        self.assertNotIn("Traceback", out, out[-3000:])

    def test_bad_args(self):
        badzip = os.path.join(self.tmpdir.name, "bad.zip")
        with open(badzip, "w") as outf:
            outf.write("not a zip file\n")
        for opts in (("-P", "-Z", "nosuch.zip"), ("-P", "-Z", badzip), ("-P", "-b", "2JN", "-A", "nosuchaction"),
                     ("-P", "-b", "XYZ"), ("-P", "-b", ""), ("-P", "-M", "nosuch.sfm"), ("-P", "-b", "2JN 1:5-1:2"),
                     ("-P", "-b", "2JN", "-F", "nosuch.pdf"), ("-P", "-b", "2JN", "-D", "c_diglot")):
            rc, out = runptxprint(self.tmpdir.name, "WSGlatin", "Default", *opts)
            self.assertNotIn("Traceback", out, f"{opts}: {out[-3000:]}")
        self.assertTrue(os.path.exists(os.path.join(self.tmpdir.name, "WSGlatin", "Settings.xml")))

    def test_publications(self):
        ''' Printing publications (-B), including ones with no books or that don't exist '''
        cfgdir = os.path.join(self.tmpdir.name, "WSGlatin", "shared", "ptxprint", "Pubs")
        os.makedirs(cfgdir)
        with open(os.path.join(self.tmpdir.name, "WSGlatin", "shared", "ptxprint", "Default", "ptxprint.cfg"), encoding="utf-8") as inf:
            dat = inf.read().replace("name = Default", "name = Pubs")
        dat += ("\n[publication.pubA]\n__books = 2JN\nmaintitle = Publication A\n\n"
                "[publication.pubB]\n__books = 3JN XYZ\nsubtitle = B\n\n[publication.pubC]\n__books = \n")
        with open(os.path.join(cfgdir, "ptxprint.cfg"), "w", encoding="utf-8") as outf:
            outf.write(dat)
        self.run_ok("WSGlatin", "Pubs", "-j", "2", "-P", "-B", "pubA", "-B", "pubB", "-B", "pubC", "-B", "nosuch")
        self.assertTrue(os.path.exists(os.path.join(self.tmpdir.name, "WSGlatin", "local", "ptxprint", "WSGlatin_Pubs_pubA_ptxp.pdf")))
