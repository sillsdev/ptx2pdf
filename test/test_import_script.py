''' Importing a config from an archive must bring its process script with it (issue #917).

    The archive is made from one copy of a project (script outside the project), and imported
    into a *different* copy, so that ${prjdir} means something else on the way in.
'''

import sys, os, io, shutil, tempfile, unittest, contextlib, zipfile, configparser

testsdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, testsdir)
from test_headless import copyproject, loadview

PRJ = "WSGlatin"
CFG = "FrontPHM"
NEWCFG = "ImportedCfg"

class TestImportScript(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.TemporaryDirectory()
        tmp = cls.tmpdir.name
        src = os.path.join(tmp, "src")
        cls.tgt = os.path.join(tmp, "tgt")
        for d in (src, cls.tgt):
            os.makedirs(d)
            for p in (PRJ, "OGNT"):
                copyproject(d, p)
        ext = os.path.join(tmp, "elsewhere")
        os.makedirs(ext)
        with open(os.path.join(ext, "procscript.py"), "w", encoding="utf-8") as outf:
            outf.write('import sys\nimport archhelper\narchhelper.run(sys.argv)\n')
        with open(os.path.join(ext, "archhelper.py"), "w", encoding="utf-8") as outf:
            outf.write('def run(argv):\n    pass\n')

        cfgfile = os.path.join(src, PRJ, "shared", "ptxprint", CFG, "ptxprint.cfg")
        config = configparser.ConfigParser(interpolation=None)
        config.read(cfgfile, encoding="utf-8")
        config.set("project", "processscript", "True")
        config.set("project", "selectscript", f"{ext}/procscript.py")
        with open(cfgfile, "w", encoding="utf-8") as outf:
            config.write(outf)

        cls.zipname = os.path.join(tmp, "archive.zip")
        view = loadview(src, PRJ, CFG)
        with contextlib.redirect_stdout(io.StringIO()):
            view.createArchive(cls.zipname, nobuild=True)
        cls.zf = zipfile.ZipFile(cls.zipname)

    @classmethod
    def tearDownClass(cls):
        cls.zf.close()
        cls.tmpdir.cleanup()

    def doImport(self):
        view = loadview(self.tgt, PRJ, "Default")
        view.set("c_impEverything", True)
        prefix = f"{PRJ}/shared/ptxprint/{CFG}"      # as gtkview._findProjectInArchive finds it
        with contextlib.redirect_stdout(io.StringIO()):
            view.importConfig(self.zf, prefix=prefix, tgtPrj=view.project, tgtCfg=NEWCFG)
        return view

    def test_script_imported(self):
        view = self.doImport()
        cfgdir = os.path.join(self.tgt, PRJ, "shared", "ptxprint", NEWCFG)
        config = configparser.ConfigParser(interpolation=None)
        config.read(os.path.join(cfgdir, "ptxprint.cfg"), encoding="utf-8")
        saved = config.get("project", "selectscript", fallback=None)
        self.assertTrue(os.path.isfile(os.path.join(cfgdir, "procscript.py")), "script was not copied in")
        resolved = os.path.normpath((saved or "").replace("${prjdir}", os.path.join(self.tgt, PRJ)))
        self.assertTrue(os.path.isfile(resolved), f"saved selectscript {saved} does not point at a real file")
        self.assertEqual(os.path.dirname(resolved), os.path.normpath(cfgdir), "script should be in the config folder")
        self.assertTrue(os.path.isfile(os.path.join(cfgdir, "archhelper.py")), "module the script imports was not copied in")
        self.assertTrue(config.getboolean("project", "processscript"))

if __name__ == "__main__":
    unittest.main()
