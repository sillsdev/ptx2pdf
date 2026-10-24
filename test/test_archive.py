''' Archive completeness: everything a config pulls in must be in its archive, and every
    reference to it, once the archive is unpacked somewhere else, must find it there.

    The project copy is given files that changes.txt, ptxprint-mods.tex, custom.sty,
    ptxprint.sty and the process script pull in, some inside the project and some outside it
    (which the archive has to move into the project and rewrite the reference to).
'''

import sys, os, re, io, shutil, tempfile, unittest, contextlib, zipfile, configparser

testsdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, testsdir)
from test_headless import copyproject, loadview

PRJ = "WSGlatin"
CFG = "FrontPHM"

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as outf:
        outf.write(text)

def inside(path, root):
    return os.path.commonpath([os.path.realpath(path), os.path.realpath(root)]) == os.path.realpath(root)

class TestArchiveContents(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.TemporaryDirectory()
        tmp = cls.tmpdir.name
        prjs = os.path.join(tmp, "projects")
        os.makedirs(prjs)
        for p in (PRJ, "OGNT"):
            copyproject(prjs, p)
        prj = os.path.join(prjs, PRJ)
        cfgdir = os.path.join(prj, "shared", "ptxprint", CFG)
        ext = os.path.join(tmp, "elsewhere")       # outside the project
        cls.ext = ext

        # changes.txt includes: in the project (not in the config tree) and outside it, nested
        write(os.path.join(cfgdir, "changes.txt"),
              'include "$PRJDIR/changes/extra.txt"\n'
              f'include "{ext}/outside_changes.txt"\n'
              '"zzzcfg" > "zzzcfg"\n')
        write(os.path.join(prj, "changes", "extra.txt"), 'include "nested.txt"\n"zzzextra" > "zzzextra"\n')
        write(os.path.join(prj, "changes", "nested.txt"), '"zzznested" > "zzznested"\n')
        write(os.path.join(ext, "outside_changes.txt"), 'include "outside_nested.txt"\n"zzzouter" > "zzzouter"\n')
        write(os.path.join(ext, "outside_nested.txt"), '"zzzouternested" > "zzzouternested"\n')

        # ptxprint-mods.tex \inputs, relative to the working directory, in and outside the project
        write(os.path.join(cfgdir, "ptxprint-mods.tex"),
              '\\input ../../../shared/texinc/inproj.tex\n'
              f'\\input "{ext}/outside.tex"\n'
              '% \\input commented/out.tex\n')
        write(os.path.join(prj, "shared", "texinc", "inproj.tex"),
              '% zzzinproj\n\\input{../../../shared/texinc/nested}\n')
        write(os.path.join(prj, "shared", "texinc", "nested.tex"), '% zzztexnested\n')
        write(os.path.join(ext, "outside.tex"), '% zzzoutsidetex\n')

        # stylesheets: a font only custom.sty asks for, and sidebar images in and outside the project
        write(os.path.join(prj, "custom.sty"),
              '\\Marker ior\n\\FontName Gentium Book Plus\n\n'
              f'\\Marker cat:bgtest|esb\n\\BgImage "{ext}/outbg.png"\n')
        shutil.copy(os.path.join(prj, "figures", "alpha.png"), os.path.join(ext, "outbg.png"))
        with open(os.path.join(cfgdir, "ptxprint.sty"), "a", encoding="utf-8") as outf:
            outf.write('\n\\Marker cat:fgtest|esb\n\\FgImage "../../../figures/text.png"\n')

        # a process script outside the project, with a module of its own
        write(os.path.join(ext, "procscript.py"), 'import sys\nimport archhelper\narchhelper.run(sys.argv)\n')
        write(os.path.join(ext, "archhelper.py"), 'def run(argv):\n    pass\n')

        # front matter PDFs: one shipped with PTXprint, one in the project, one outside it
        shutil.copy(os.path.join(prj, "figures", "deco.pdf"), os.path.join(ext, "front.pdf"))
        # and a custom cross reference list outside the project
        write(os.path.join(ext, "myxrefs.txt"), "JON 1:1 = RUT 1:1\n")

        cfgfile = os.path.join(cfgdir, "ptxprint.cfg")
        config = configparser.ConfigParser(interpolation=None)
        config.read(cfgfile, encoding="utf-8")
        for k, v in (("ifusecustomsty", "True"), ("ifusemodstex", "True"), ("usechangesfile", "True"),
                     ("processscript", "True"), ("selectscript", f"{ext}/procscript.py"),
                     ("ifinclfrontpdf", "True"), ("selectxrfile", f"{ext}/myxrefs.txt"),
                     ("frontincludes", "${pdfassets}/watermarks/A5-Draft.pdf\n"
                                       f"{ext}/front.pdf\n${{prjdir}}/figures/deco.pdf")):
            config.set("project", k, v)
        with open(cfgfile, "w", encoding="utf-8") as outf:
            config.write(outf)

        cls.zipname = os.path.join(tmp, "archive.zip")
        view = loadview(prjs, PRJ, CFG)
        with contextlib.redirect_stdout(io.StringIO()):
            view.createArchive(cls.zipname, nobuild=True)
        cls.outdir = os.path.join(tmp, "unpacked")
        with zipfile.ZipFile(cls.zipname) as zf:
            cls.names = zf.namelist()
            zf.extractall(cls.outdir)
        cls.prj = os.path.join(cls.outdir, PRJ)
        cls.cfgdir = os.path.join(cls.prj, "shared", "ptxprint", CFG)
        cls.workdir = os.path.join(cls.prj, "local", "ptxprint", CFG)
        os.makedirs(cls.workdir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        cls.tmpdir.cleanup()

    def assertResolves(self, path, what):
        self.assertTrue(os.path.isfile(path), f"{what} -> {path} is not in the archive")
        self.assertTrue(inside(path, self.prj), f"{what} -> {path} is outside the archived project")

    def readchain(self, fname, follow, seen=None):
        ''' Returns the text of fname and everything it pulls in, checking each one resolves '''
        seen = set() if seen is None else seen
        if fname in seen:
            return ""
        seen.add(fname)
        with open(fname, encoding="utf-8") as inf:
            text = inf.read()
        res = [text]
        for ref, path in follow(fname, text):
            self.assertResolves(path, f"{os.path.basename(fname)}: {ref}")
            res.append(self.readchain(path, follow, seen))
        return "\n".join(res)

    def test_changes_includes(self):
        def follow(fname, text):
            for m in re.finditer(r'^\s*include\s+(["\'])(.*?)\1', text, flags=re.M):
                t = m.group(2).replace("$PRJDIR", self.prj)
                yield (m.group(2), os.path.normpath(os.path.join(os.path.dirname(fname), t)))
        text = self.readchain(os.path.join(self.cfgdir, "changes.txt"), follow)
        for s in ("zzzcfg", "zzzextra", "zzznested", "zzzouter", "zzzouternested"):
            self.assertIn(s, text)

    def test_mods_inputs(self):
        def follow(fname, text):
            for l in text.splitlines():
                l = re.sub(r"(?<!\\)%.*$", "", l)
                for m in re.finditer(r'\\input\s*(?:\{([^}]*)\}|"([^"]*)"|(\S+))', l):
                    t = m.group(1) or m.group(2) or m.group(3)
                    p = os.path.normpath(os.path.join(self.workdir, t))
                    if not os.path.exists(p) and os.path.exists(p + ".tex"):
                        p += ".tex"
                    yield (t, p)
        text = self.readchain(os.path.join(self.cfgdir, "ptxprint-mods.tex"), follow)
        for s in ("zzzinproj", "zzztexnested", "zzzoutsidetex"):
            self.assertIn(s, text)

    def test_custom_sty_font(self):
        self.assertIn(f"{PRJ}/shared/fonts/GentiumBookPlus-Regular.ttf", self.names)

    def test_sty_images(self):
        found = {}
        for sty in (os.path.join(self.prj, "custom.sty"), os.path.join(self.cfgdir, "ptxprint.sty")):
            mrk = None
            with open(sty, encoding="utf-8") as inf:
                for l in inf.readlines():
                    m = re.match(r"^\\Marker\s+(\S+)", l)
                    if m:
                        mrk = m.group(1)
                    m = re.match(r'^\\([BF]gImage)\s+"?([^"]*?)"?\s*$', l)
                    if m:
                        found[mrk] = m.group(2)     # ptxprint.sty is read last, so it wins
        for mrk in ("cat:bgtest|esb", "cat:fgtest|esb"):
            self.assertIn(mrk, found)
            self.assertResolves(os.path.normpath(os.path.join(self.workdir, found[mrk])), mrk)

    def test_process_script(self):
        config = configparser.ConfigParser(interpolation=None)
        config.read(os.path.join(self.cfgdir, "ptxprint.cfg"), encoding="utf-8")
        script = config.get("project", "selectscript").replace("${prjdir}", self.prj)
        self.assertResolves(os.path.normpath(script), "selectscript")
        self.assertResolves(os.path.join(os.path.dirname(script), "archhelper.py"), "procscript.py: import archhelper")

    def cfgpaths(self, key):
        config = configparser.ConfigParser(interpolation=None)
        config.read(os.path.join(self.cfgdir, "ptxprint.cfg"), encoding="utf-8")
        return [l.strip() for l in config.get("project", key).splitlines() if l.strip()]

    def test_front_pdfs(self):
        vals = self.cfgpaths("frontincludes")
        self.assertEqual(len(vals), 3, f"front PDFs are now {vals}")
        self.assertEqual(vals[0], "${pdfassets}/watermarks/A5-Draft.pdf")
        for v in vals[1:]:
            self.assertTrue(v.startswith("${prjdir}/"), v)
            self.assertResolves(os.path.join(self.prj, v[10:]), "frontincludes")

    def test_xref_file(self):
        vals = self.cfgpaths("selectxrfile")
        self.assertTrue(vals[0].startswith("${prjdir}/"), vals)
        self.assertResolves(os.path.join(self.prj, vals[0][10:]), "selectxrfile")

    def test_no_absolute_paths(self):
        ''' Nothing archived still points at where the files were '''
        for dp, dn, fn in os.walk(self.prj):
            for f in fn:
                if os.path.splitext(f)[1].lower() in (".cfg", ".sty", ".txt", ".tex"):
                    with open(os.path.join(dp, f), encoding="utf-8", errors="replace") as inf:
                        self.assertNotIn(self.ext, inf.read(), f"{f} still refers to {self.ext}")


class TestArchiveLocal(unittest.TestCase):
    ''' A real archive (not a GUI test one) keeps what is in local/ '''

    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.TemporaryDirectory()
        prjs = os.path.join(cls.tmpdir.name, "projects")
        os.makedirs(prjs)
        for p in (PRJ, "OGNT"):
            copyproject(prjs, p)
        cls.prjs = prjs

    @classmethod
    def tearDownClass(cls):
        cls.tmpdir.cleanup()

    def archive(self, cfg):
        view = loadview(self.prjs, PRJ, cfg)
        zipname = os.path.join(self.tmpdir.name, cfg + ".zip")
        with contextlib.redirect_stdout(io.StringIO()):
            view.createArchive(zipname, nobuild=True)
        with zipfile.ZipFile(zipname) as zf:
            return zf.namelist()

    def test_pictures(self):
        names = self.archive("PicsJON")
        self.assertTrue(any(n.startswith(f"{PRJ}/local/figures/") for n in names),
                        "no pictures in local/figures")

    def test_diglot_fonts(self):
        ''' The secondary's fonts go where the archive's fonts.conf looks: the main project's shared/fonts '''
        names = self.archive("Diglot2JN")
        self.assertIn(f"{PRJ}/shared/fonts/GalSILR.ttf", names)
