''' Tests for the multi-project management tool (ptxprint.manager): the checks, their repairs,
    the command line and the window, on copies of the test projects.
    unittest classes, so that test/conftest.py does not parametrize them as projects. '''

import sys, os, io, shutil, tempfile, unittest, contextlib, configparser

testsdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(testsdir, "..", "python", "lib"))

from ptxprint.manager.validate import Validator, ERROR, WARNING, NOTE
from ptxprint.manager.main import main

class _Projects(unittest.TestCase):
    projects = ("WSGlatin", "WSG", "OGNT")

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        for p in self.projects:
            shutil.copytree(os.path.join(testsdir, "projects", p), os.path.join(self.tmpdir.name, p),
                            ignore=lambda d, fs: ["local"] if os.path.basename(d) == p else [])
        # WSG gets WSGlatin's diglot config as an older PTXprint copied it: still saying WSGlatin
        self.src = os.path.join(self.tmpdir.name, "WSGlatin", "shared", "ptxprint", "Diglot2JN")
        self.dest = os.path.join(self.tmpdir.name, "WSG", "shared", "ptxprint", "Diglot2JN")
        shutil.copytree(self.src, self.dest)
        self.cfgpath = os.path.join(self.dest, "ptxprint.cfg")

    def tearDown(self):
        self.tmpdir.cleanup()

    def change(self, *changes):
        cfg = configparser.ConfigParser(interpolation=None)
        cfg.read(self.cfgpath, encoding="utf-8")
        for s, o, v in changes:
            cfg.set(s, o, v)
        with open(self.cfgpath, "w", encoding="utf-8") as outf:
            cfg.write(outf)

    def get(self, sect, opt):
        cfg = configparser.ConfigParser(interpolation=None)
        cfg.read(self.cfgpath, encoding="utf-8")
        return cfg.get(sect, opt)

    def codes(self, findings, prj="WSG"):
        return {f.code: f for f in findings if f.project == prj}


class TestValidate(_Projects):

    def test_inventory(self):
        v = Validator(self.tmpdir.name)
        self.assertEqual(set(v.projectsWithConfigs()), set(self.projects))
        self.assertIn(("Diglot2JN", 2), v.commonConfigs())

    def test_clean_config(self):
        ''' The source project's own diglot config has nothing wrong that stops a print '''
        v = Validator(self.tmpdir.name)
        errs = [f for f in v.validate(["WSGlatin"], ["Diglot2JN"]) if f.severity == ERROR]
        self.assertEqual(errs, [], [str(f) for f in errs])

    def test_primary(self):
        v = Validator(self.tmpdir.name)
        found = self.codes(v.validate(["WSG"], ["Diglot2JN"]))
        self.assertIn("diglotPrimary", found)
        self.assertEqual(found["diglotPrimary"].severity, ERROR)
        self.assertEqual(self.get("diglot_L", "projectid"), "WSGlatin")       # nothing changed by checking
        found["diglotPrimary"].fix.apply()
        self.assertEqual(self.get("diglot_L", "projectid"), "WSG")
        self.assertEqual(self.get("diglot_L", "projectguid"), v.projects["WSG"].guid)
        self.assertNotIn("diglotPrimary", self.codes(v.validate(["WSG"], ["Diglot2JN"])))

    def test_secondary_missing(self):
        self.change(("diglot_R", "projectid", "NoSuchBT"))
        with open(os.path.join(self.tmpdir.name, "WSG", "shared", "ptxprint", "ptxprint_project.cfg"), "w", encoding="utf-8") as outf:
            outf.write("[document]\n*diglotsecprj = OGNT\n")
        v = Validator(self.tmpdir.name)
        f = self.codes(v.validate(["WSG"], ["Diglot2JN"]))["diglotSecondaryMissing"]
        self.assertEqual(f.severity, ERROR)
        self.assertFalse(f.fix.safe)            # which project is the user's choice
        f.fix.apply()
        self.assertEqual(self.get("diglot_R", "projectid"), "OGNT")
        self.assertNotIn("diglotSecondaryMissing", self.codes(v.validate(["WSG"], ["Diglot2JN"])))

    def test_script_path(self):
        ''' ${prjdir}/Other/shared/x.py, as 3.1 saved it: the project's own copy is offered, else the other's '''
        os.makedirs(os.path.join(self.tmpdir.name, "WSGlatin", "shared"), exist_ok=True)
        with open(os.path.join(self.tmpdir.name, "WSGlatin", "shared", "myscript.py"), "w") as outf:
            outf.write("pass\n")
        self.change(("project", "processscript", "True"), ("project", "selectscript", "${prjdir}/WSGlatin\\shared\\myscript.py"))
        v = Validator(self.tmpdir.name)
        f = self.codes(v.validate(["WSG"], ["Diglot2JN"]))["pathMissing"]
        f.fix.apply()
        self.assertEqual(self.get("project", "selectscript"), "${settingsdir}/WSGlatin/shared/myscript.py")
        self.assertNotIn("pathMissing", self.codes(v.validate(["WSG"], ["Diglot2JN"])))
        # with a copy of its own, that is the one to use
        self.change(("project", "selectscript", "${prjdir}/WSGlatin\\shared\\other.py"))
        with open(os.path.join(self.tmpdir.name, "WSG", "shared", "other.py"), "w") as outf:
            outf.write("pass\n")
        f = self.codes(v.validate(["WSG"], ["Diglot2JN"]))["pathMissing"]
        f.fix.apply()
        self.assertEqual(self.get("project", "selectscript"), "${prjdir}/shared/other.py")

    def test_unused_path_ignored(self):
        self.change(("project", "processscript", "False"), ("project", "selectscript", "${prjdir}/nosuch.py"))
        v = Validator(self.tmpdir.name)
        self.assertNotIn("pathMissing", self.codes(v.validate(["WSG"], ["Diglot2JN"])))

    def test_variables(self):
        with open(os.path.join(self.dest, "FRTlocal.sfm"), "w", encoding="utf-8") as outf:
            outf.write('\\periph front|id="coverfront"\n\\mt1 \\zvar|maintitle\\*\n\\rem \\zvar|unusedvar\\*\n\\mt2 \\zvar|t1title\\*\n')
        cfg = configparser.ConfigParser(interpolation=None)
        cfg.read(self.cfgpath, encoding="utf-8")
        cfg.remove_section("vars")
        cfg.add_section("vars")
        cfg.set("vars", "t1title", "")
        cfg.set("vars", "isbn", "1234567890")
        with open(self.cfgpath, "w", encoding="utf-8") as outf:
            cfg.write(outf)
        found = self.codes(Validator(self.tmpdir.name).validate(["WSG"], ["Diglot2JN"]))
        self.assertIn("maintitle", found["variableUndefined"].message)
        self.assertNotIn("unusedvar", found["variableUndefined"].message)
        self.assertIn("t1title", found["variableEmpty"].message)
        self.assertIn("isbnPlaceholder", found)

    def test_empty_secondary_book(self):
        ''' A diglot whose other project has the book but no text in it (only verse numbers) '''
        ognt = os.path.join(self.tmpdir.name, "OGNT")
        for f in os.listdir(ognt):
            if "2JN" in f.upper():
                with open(os.path.join(ognt, f), "w", encoding="utf-8") as outf:
                    outf.write("\\id 2JN\n\\h 2 John\n\\c 1\n\\v 1\n\\v 2\n\\v 3 word\n\\v 4\n")
        v = Validator(self.tmpdir.name)
        self.assertTrue(v.bookIsEmpty("OGNT", "2JN"))
        self.assertFalse(v.bookIsEmpty("WSGlatin", "2JN"))
        self.assertFalse(v.bookIsEmpty("OGNT", "XXQ"))          # not there at all isn't "empty"
        found = self.codes(v.validate(["WSGlatin"], ["Diglot2JN"]), prj="WSGlatin")
        self.assertEqual(found["bookEmptySecondary"].severity, ERROR)
        self.assertIn("2JN", found["bookEmptySecondary"].message)

    def test_stale_cover(self):
        outdir = os.path.join(self.tmpdir.name, "WSG", "local", "ptxprint")
        os.makedirs(outdir)
        cover = os.path.join(outdir, "WSG_Diglot2JN_2JN_ptxp_cover.pdf")
        open(cover, "wb").close()
        self.change(("cover", "makecoverpage", "False"))
        f = self.codes(Validator(self.tmpdir.name).validate(["WSG"], ["Diglot2JN"]))["coverStale"]
        self.assertTrue(os.path.exists(cover))
        f.fix.apply()
        self.assertFalse(os.path.exists(cover))


class TestCommandLine(_Projects):

    def run_main(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = main(["-p", self.tmpdir.name] + list(args))
        return rc, out.getvalue()

    def test_report_changes_nothing(self):
        before = open(self.cfgpath, encoding="utf-8").read()
        rc, out = self.run_main("validate", "-P", "WSG", "-c", "Diglot2JN")
        self.assertEqual(rc, 1)
        self.assertIn("primary (L)", out)
        self.assertIn("can fix", out)
        self.assertEqual(before, open(self.cfgpath, encoding="utf-8").read())

    def test_fix_yes_only_safe(self):
        self.change(("diglot_R", "projectid", "NoSuchBT"))
        with open(os.path.join(self.tmpdir.name, "WSG", "shared", "ptxprint", "ptxprint_project.cfg"), "w", encoding="utf-8") as outf:
            outf.write("[document]\ndiglotsecprj = OGNT\n")
        rc, out = self.run_main("validate", "-P", "WSG", "-c", "Diglot2JN", "--fix", "--yes")
        self.assertEqual(self.get("diglot_L", "projectid"), "WSG")           # safe: done
        self.assertEqual(self.get("diglot_R", "projectid"), "NoSuchBT")      # a choice: left
        self.assertEqual(rc, 1)

    def test_unknown_project(self):
        rc, out = self.run_main("validate", "-P", "Nope")
        self.assertEqual(rc, 2)


class TestWindow(_Projects):
    ''' The window, driven without showing it '''

    def test_check_and_fix(self):
        try:
            from ptxprint.manager.gtkmanager import ManagerWindow, C_TICK, C_CANFIX, C_PROJECT
            from gi.repository import Gtk
            if not Gtk.init_check()[0]:
                raise ImportError("no display")
        except (ImportError, ValueError) as e:
            self.skipTest(f"No GTK: {e}")
        self.change(("diglot_R", "projectid", "NoSuchBT"))
        with open(os.path.join(self.tmpdir.name, "WSG", "shared", "ptxprint", "ptxprint_project.cfg"), "w", encoding="utf-8") as outf:
            outf.write("[document]\ndiglotsecprj = OGNT\n")
        win = ManagerWindow(self.tmpdir.name)
        try:
            win.configCombo.set_active_id("Diglot2JN")
            self.assertEqual(sorted(win.chosenProjects()), ["WSG", "WSGlatin"])       # those that have it
            win.runCheck()
            rows = [r for r in win.store if r[C_PROJECT] == "WSG" and r[C_CANFIX]]
            self.assertEqual(len(rows), 3)
            # the safe repair is ticked for the user, the one with a choice in it is not
            ticked = {f.code for f in win.tickedFindings()}
            self.assertEqual(ticked, {"diglotPrimary", "projectId"})
            self.assertEqual(self.get("diglot_L", "projectid"), "WSGlatin")
            win.applyFixes(win.tickedFindings())
            self.assertEqual(self.get("diglot_L", "projectid"), "WSG")
            self.assertEqual(self.get("diglot_R", "projectid"), "NoSuchBT")
            self.assertEqual({f.code for f in win.findings if f.fix is not None}, {"diglotSecondaryMissing"})
            win.onTickAll(None, False)
            self.assertFalse(win.fixButton.get_sensitive())
        finally:
            win.destroy()

    def test_diglot_texts_and_print(self):
        try:
            from ptxprint.manager.gtkmanager import (ManagerWindow, D_PROJECT, D_NEWPRJ, D_NEWCFG, D_NOTE,
                                                     T_RESULT, T_MESSAGE)
            from gi.repository import Gtk, GLib
            if not Gtk.init_check()[0]:
                raise ImportError("no display")
        except (ImportError, ValueError) as e:
            self.skipTest(f"No GTK: {e}")
        self.change(("diglot_R", "projectid", "NoSuchBT"))
        win = ManagerWindow(self.tmpdir.name)
        try:
            win.configCombo.set_active_id("Diglot2JN")
            win.fillDiglots()
            rows = {r[D_PROJECT]: r for r in win.diglotStore}
            self.assertEqual(sorted(rows), ["WSG", "WSGlatin"])
            self.assertIn("no project NoSuchBT", rows["WSG"][D_NOTE])
            self.assertEqual(win.diglotChanges(), [])
            # choosing the project picks a configuration of it; nothing is written yet
            win.setDiglotProject(rows["WSG"].path, "OGNT")
            self.assertEqual(win.diglotChanges(), [("WSG", "Diglot2JN", "R", "OGNT", "Default")])
            self.assertEqual(self.get("diglot_R", "projectid"), "NoSuchBT")
            win.setDiglotProject(rows["WSG"].path, "WSG")           # itself: refused
            self.assertEqual(win.diglotChanges()[0][3], "OGNT")
            win.applyDiglots(win.diglotChanges())
            self.assertEqual(self.get("diglot_R", "projectid"), "OGNT")
            self.assertEqual(self.get("diglot_R", "projectguid"), win.validator.projects["OGNT"].guid)
            self.assertEqual(win.diglotChanges(), [])
            # a test print of a book the projects don't have is reported, not run
            win.startTestPrint(win.chosenPairs(), "XXQ")
            loop = GLib.MainLoop()
            def poll():
                if win.printThread is None:
                    loop.quit()
                    return False
                return True
            GLib.timeout_add(50, poll)
            GLib.timeout_add(20000, loop.quit)
            loop.run()
            self.assertIsNone(win.printThread)
            self.assertEqual({r[T_RESULT] for r in win.printStore}, {"Not tried"})
            self.assertTrue(all("XXQ" in r[T_MESSAGE] for r in win.printStore))
        finally:
            win.destroy()


    def test_publications_and_compare(self):
        try:
            from ptxprint.manager.gtkmanager import (ManagerWindow, P_PROJECT, P_PUBID, P_STATE, P_NFIXED, P_CANPRINT,
                                                     X_TICK, X_SETTING, X_PROJECT, MAINLABEL)
            from ptxprint.manager.publications import MAIN
            from gi.repository import Gtk
            if not Gtk.init_check()[0]:
                raise ImportError("no display")
        except (ImportError, ValueError) as e:
            self.skipTest(f"No GTK: {e}")
        self.change(("vars", "maintitle", "WSG title"), ("paper", "margins", "33"))
        before = open(self.cfgpath, encoding="utf-8").read()
        win = ManagerWindow(self.tmpdir.name)
        try:
            win.configCombo.set_active_id("Diglot2JN")
            win.fillPublications(reload=True)
            self.assertIn("maintitle", win.pubColumns)
            col = P_NFIXED + win.pubColumns.index("maintitle")
            self.assertEqual({(r[P_PROJECT], r[P_PUBID]) for r in win.pubStore}, {("WSG", MAIN), ("WSGlatin", MAIN)})
            # a new publication in both projects, with a title of its own in one, and a main title changed
            self.assertEqual(win.addPublication("Second John", "2jn"), 2)
            self.assertEqual(win.addPublication("Bad:name", "2JN"), 0)
            self.assertEqual(win.addPublication("Third", "not books!"), 0)
            win.editPublication("WSG", "Diglot2JN", "Second John", "maintitle", "2 John in WSG")
            win.editPublication("WSGlatin", "Diglot2JN", MAIN, "maintitle", "Latin main")
            rows = {(r[P_PROJECT], r[P_PUBID]): r for r in win.pubStore}
            self.assertEqual(rows[("WSG", "Second John")][col], "2 John in WSG")
            self.assertEqual(rows[("WSGlatin", "Second John")][col], "Latin main")     # inherits the pending main value
            self.assertEqual(rows[("WSG", "Second John")][P_STATE], "new")
            self.assertFalse(rows[("WSG", "Second John")][P_CANPRINT])                 # not until it is saved
            self.assertEqual(win.numPubChanges(), 4)
            self.assertEqual(before, open(self.cfgpath, encoding="utf-8").read())      # nothing written yet
            win.applyPublications()
            self.assertEqual(win.numPubChanges(), 0)
            self.assertEqual(self.get("publication.Second John", "__books"), "2JN")
            self.assertEqual(self.get("publication.Second John", "maintitle"), "2 John in WSG")
            self.assertEqual(self.get("vars.publishable", "maintitle"), "True")
            self.assertEqual(self.get("vars", "maintitle"), "WSG title")
            # delete it again from one project
            win.deletePublications([("WSG", "Diglot2JN", "Second John"), ("WSG", "Diglot2JN", MAIN)])
            self.assertEqual(win.pubDeletes, {("WSG", "Diglot2JN", "Second John")})
            win.applyPublications()
            self.assertEqual({(r[P_PROJECT], r[P_PUBID]) for r in win.pubStore},
                             {("WSG", MAIN), ("WSGlatin", MAIN), ("WSGlatin", "Second John")})

            # compare WSG with WSGlatin: the margin differs, the titles and the diglot's projects aren't compared
            win.refCombo.set_active_id("WSGlatin")
            win.runCompare()
            settings = {(r[X_SETTING], r[X_PROJECT]) for r in win.compareStore}
            self.assertIn(("paper/margins", "WSG"), settings)
            self.assertFalse(any(s.startswith(("vars/", "diglot_", "publication.")) or s == "project/id" for s, p in settings))
            win.compareFind.set_text("margins")
            self.assertEqual(len(win.compareFilter), 1)
            win.onTickCompare(None, True)
            self.assertEqual([d.setting for d in win.tickedDifferences()], ["paper/margins"])
            self.assertEqual(self.get("paper", "margins"), "33")
            win.copySettings(win.tickedDifferences())
            cfg = configparser.ConfigParser(interpolation=None)
            cfg.read(os.path.join(self.src, "ptxprint.cfg"), encoding="utf-8")
            self.assertEqual(self.get("paper", "margins"), cfg.get("paper", "margins"))
            self.assertNotIn(("paper/margins", "WSG"), {(r[X_SETTING], r[X_PROJECT]) for r in win.compareStore})
        finally:
            win.destroy()


class TestPublications(_Projects):

    def test_table(self):
        from ptxprint.manager.publications import PublicationTable, ConfigPublications, MAIN, validBooks
        v = Validator(self.tmpdir.name)
        c = ConfigPublications(v, "WSG", "Diglot2JN")
        c.apply(adds=[("PubA", "JAS GLO")], edits=[("PubA", "isbn", "978-1"), (MAIN, "isbn", "000")])
        self.assertEqual(c.booksOf("PubA"), "JAS GLO")
        self.assertEqual((c.value("PubA", "isbn"), c.value(MAIN, "isbn")), ("978-1", "000"))
        self.assertIn("isbn", c.publishable)
        self.assertIn("maintitle", c.publishable)       # these stay as they were
        with self.assertRaises(ValueError):
            c.apply(adds=[("PubA", "JAS")])
        table = PublicationTable(v, [("WSG", "Diglot2JN"), ("WSGlatin", "Diglot2JN")])
        self.assertIn("isbn", table.columns())
        self.assertEqual(table.publicationNames(), ["PubA"])
        self.assertIn(("WSG", "Diglot2JN", "PubA"), table.rows())
        c.apply(deletes=["PubA"])
        self.assertEqual(c.pubs, {})
        self.assertTrue(all(validBooks(b) for b in ("JAS", "jas glo", "MAT-JHN", "MAT 1-7")))
        self.assertFalse(any(validBooks(b) for b in ("", "James", "JAS!")))

    def test_ptxprint_reads_it(self):
        ''' What is written is what PTXprint loads as the publication's variables '''
        from ptxprint.manager.publications import ConfigPublications
        from test_headless import loadview
        v = Validator(self.tmpdir.name)
        ConfigPublications(v, "WSGlatin", "Diglot2JN").apply(adds=[("PubA", "2JN")], edits=[("PubA", "t1title", "Title One")])
        view = loadview(self.tmpdir.name, "WSGlatin", "Diglot2JN")
        self.assertEqual(view.publications["PubA"]["t1title"], "Title One")
        self.assertEqual(view.publications["PubA"]["__books"], "2JN")
        self.assertTrue(view.pubvars_publishable.get("t1title"))


class TestCompare(_Projects):

    def test_differences_and_copy(self):
        from ptxprint.manager.compare import Comparison, NOTSET, isShared
        self.change(("paper", "margins", "33"), ("paper", "height", "210.0mm"), ("vars", "maintitle", "Mine"))
        cfg = configparser.ConfigParser(interpolation=None)
        cfg.read(self.cfgpath, encoding="utf-8")
        cfg.remove_option("paper", "width")
        cfg.set("paper", "onlyhere", "x")
        with open(self.cfgpath, "w", encoding="utf-8") as outf:
            cfg.write(outf)
        comp = Comparison(Validator(self.tmpdir.name), "Diglot2JN", "WSGlatin")
        diffs = {d.setting: d for d in comp.differences(["WSG", "WSGlatin", "OGNT"])}
        self.assertEqual(set(diffs), {"paper/margins", "paper/height", "paper/width", "paper/onlyhere"} & set(diffs))
        self.assertIn("paper/margins", diffs)
        self.assertNotIn("vars/maintitle", diffs)
        self.assertNotIn("diglot_L/projectid", diffs)
        self.assertTrue(diffs["paper/width"].oneSided and diffs["paper/width"].value is NOTSET)
        self.assertTrue(diffs["paper/onlyhere"].refValue is NOTSET)
        self.assertFalse(isShared("publication.X", "isbn"))
        self.assertTrue(Comparison.sameValue("0.50", "0.5") and Comparison.sameValue("True", "true"))
        self.assertTrue(Comparison.sameValue("${prjdir}/shared\\x.py", "${prjdir}/shared/x.py"))
        self.assertEqual(comp.copy([diffs["paper/margins"], diffs["paper/width"], diffs["paper/onlyhere"]]), 3)
        left = {d.setting for d in comp.differences(["WSG"])}
        self.assertEqual(left & {"paper/margins", "paper/width", "paper/onlyhere"}, set())
        self.assertEqual(self.get("vars", "maintitle"), "Mine")

    def test_command(self):
        self.change(("paper", "margins", "33"))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = main(["-p", self.tmpdir.name, "compare", "-c", "Diglot2JN", "--ref", "WSGlatin", "--copy", "paper/margins", "--yes"])
            rc2 = main(["-p", self.tmpdir.name, "compare", "-c", "Diglot2JN"])
            rc3 = main(["-p", self.tmpdir.name, "publications", "-c", "Diglot2JN"])
        self.assertEqual((rc, rc2, rc3), (0, 2, 0))
        self.assertIn("paper/margins", out.getvalue())
        self.assertIn("Copied 1 settings", out.getvalue())
        self.assertNotEqual(self.get("paper", "margins"), "33")
        self.assertIn("WSG / Diglot2JN", out.getvalue())


class TestStyles(_Projects):

    def writeSty(self, prj, cfg, name, text):
        with open(os.path.join(self.tmpdir.name, prj, "shared", "ptxprint", cfg, name), "w", encoding="utf-8") as outf:
            outf.write(text)

    def setUp(self):
        super().setUp()
        # WSG and WSGlatin: the same but for the size of \s, written differently where they agree
        self.writeSty("WSGlatin", "Diglot2JN", "ptxprint.sty",
                      "\\Marker s\n\\FontSize 12\n\\Italic -\n\\LeftMargin 0\n\\Name Heading\n\n\\Marker p\n\\Color x0000ff\n\\SpaceBefore 0.50\n")
        self.writeSty("WSG", "Diglot2JN", "ptxprint.sty",
                      "\\Marker s\n\\FontSize 14\n\\Name Section head\n\n\\Marker p\n\\Color 16711680\n\\SpaceBefore 0.5   # as the others\n")

    def diffs(self, comp, **kw):
        return {(d.marker, d.attr): d for d in comp.differences(**kw)}

    def test_normalise(self):
        from ptxprint.manager.styles import normalise, styleGroup, parseSty, loadDefaults
        self.assertEqual(normalise("fontsize", "12.0"), normalise("fontsize", "12"))
        self.assertEqual(normalise("color", "16711680"), normalise("color", "x0000ff"))
        self.assertEqual(normalise("bold", "-"), "off")
        self.assertEqual(normalise("bold", None), "off")                        # a paragraph's
        self.assertIsNone(normalise("bold", None, paragraph=False))             # a character style inherits
        self.assertEqual(normalise("leftmargin", None), normalise("leftmargin", "0"))
        self.assertEqual(normalise("occursunder", "c p  id"), normalise("occursunder", "id c p"))
        self.assertEqual([styleGroup(m) for m in ("p", "s1", "f", "xt", "ip", "cat:coverfront|mt1", "cat:box|esb")],
                         ["Text", "Headings", "Notes", "Notes", "Introductions", "Cover", "Sidebars and categories"])
        self.assertIn("p", loadDefaults())

    def test_across_projects(self):
        from ptxprint.manager.styles import StyleComparison
        comp = StyleComparison.acrossProjects(Validator(self.tmpdir.name), "Diglot2JN", ["WSG", "WSGlatin", "OGNT"])
        self.assertEqual(comp.columns, ["WSG", "WSGlatin"])
        found = self.diffs(comp, reference="WSGlatin")
        self.assertEqual(set(found), {("s", "fontsize"), ("s", "name")})        # not bold, margin, colour or space
        d = found[("s", "fontsize")]
        self.assertEqual((d.values["WSG"].raw, d.values["WSG"].source, d.baseline.raw), ("14", "ptxprint.sty", "12"))
        self.assertEqual(d.differing, ["WSG"])
        self.assertTrue(d.visual and not found[("s", "name")].visual)
        self.assertEqual(d.group, "Headings")
        self.assertEqual(self.diffs(comp, reference="WSG")[("s", "fontsize")].differing, ["WSGlatin"])

    def test_layers(self):
        ''' custom.sty and ptxprint-mods.sty count only if the configuration uses them, and mods wins '''
        from ptxprint.manager.styles import StyleComparison
        with open(os.path.join(self.tmpdir.name, "WSG", "custom.sty"), "w", encoding="utf-8") as outf:
            outf.write("\\Marker q1\n\\LeftMargin 0.9\n\n\\Marker s\n\\FontSize 20\n")
        self.writeSty("WSG", "Diglot2JN", "ptxprint-mods.sty", "\\Marker s\n\\FontSize 9\n")
        self.change(("project", "ifusecustomsty", "False"), ("project", "ifusemodssty", "False"))
        v = Validator(self.tmpdir.name)
        found = self.diffs(StyleComparison.acrossProjects(v, "Diglot2JN", ["WSG", "WSGlatin"]))
        self.assertNotIn(("q1", "leftmargin"), found)
        self.assertEqual(found[("s", "fontsize")].values["WSG"].raw, "14")
        self.change(("project", "ifusecustomsty", "True"), ("project", "ifusemodssty", "True"))
        found = self.diffs(StyleComparison.acrossProjects(v, "Diglot2JN", ["WSG", "WSGlatin"]))
        self.assertEqual(found[("q1", "leftmargin")].values["WSG"].source, "custom.sty")
        self.assertEqual((found[("s", "fontsize")].values["WSG"].raw, found[("s", "fontsize")].values["WSG"].source),
                         ("9", "ptxprint-mods.sty"))

    def readSty(self, prj, cfg, name="ptxprint.sty"):
        with open(os.path.join(self.tmpdir.name, prj, "shared", "ptxprint", cfg, name), encoding="utf-8") as inf:
            return inf.read()

    def test_set_value(self):
        from ptxprint.manager.styles import setStyValue, parseSty
        path = os.path.join(self.tmpdir.name, "x.sty")
        with open(path, "w", encoding="utf-8") as outf:
            outf.write("\\Marker s\n\\FontSize 14\n\\Name Section head\n\n\\Marker p\n\\Color 16711680\n# a comment\n")
        self.assertTrue(setStyValue(path, "s", "fontsize", "12"))           # change one
        self.assertTrue(setStyValue(path, "s", "spacebefore", "3"))         # add one to a style that is there
        self.assertTrue(setStyValue(path, "q1", "leftmargin", "0.5"))       # add a style
        self.assertTrue(setStyValue(path, "p", "color", None))              # remove one
        self.assertFalse(setStyValue(path, "p", "color", None))             # nothing to do
        self.assertFalse(setStyValue(path, "s", "fontsize", "12"))
        text = open(path, encoding="utf-8").read()
        self.assertEqual(parseSty(path), {"s": {"fontsize": "12", "name": "Section head", "spacebefore": "3"},
                                          "p": {}, "q1": {"leftmargin": "0.5"}})
        self.assertIn("\\Marker s\n\\FontSize 12\n\\Name Section head\n\\SpaceBefore 3\n\n\\Marker p\n", text)
        self.assertIn("# a comment", text)                                  # the rest is left as it was
        self.assertIn("\\Marker q1\n\\LeftMargin 0.5", text)

    def test_copy(self):
        from ptxprint.manager.styles import StyleComparison
        v = Validator(self.tmpdir.name)
        comp = StyleComparison.acrossProjects(v, "Diglot2JN", ["WSG", "WSGlatin"])
        before = self.readSty("WSGlatin", "Diglot2JN")
        found = self.diffs(comp, reference="WSGlatin")
        changed, problems = comp.copy([found[("s", "fontsize")]])
        self.assertEqual((changed, problems), (1, []))
        self.assertNotIn("FontSize", self.readSty("WSG", "Diglot2JN"))             # 12 is the default: no need to say it
        self.assertIn("\\Name Section head", self.readSty("WSG", "Diglot2JN"))      # only what was asked for
        self.assertEqual(before, self.readSty("WSGlatin", "Diglot2JN"))             # the reference isn't touched
        self.assertNotIn(("s", "fontsize"), self.diffs(comp, reference="WSGlatin"))
        # the sheet as it was is kept, out of the shared folder
        backup = os.path.join(self.tmpdir.name, "WSG", "local", "ptxprint", "Diglot2JN", "ptxprint.sty.before-copy")
        with open(backup, encoding="utf-8") as inf:
            self.assertIn("\\FontSize 14", inf.read())

    def test_copy_default(self):
        ''' Where the others just have the default, the override is taken out, not a value written '''
        from ptxprint.manager.styles import StyleComparison
        self.writeSty("WSGlatin", "Diglot2JN", "ptxprint.sty", "\\Marker p\n\\Color x0000ff\n")
        self.writeSty("WSG", "Diglot2JN", "ptxprint.sty", "\\Marker p\n\\Color x0000ff\n\\FirstLineIndent 0.7\n")
        comp = StyleComparison.acrossProjects(Validator(self.tmpdir.name), "Diglot2JN", ["WSG", "WSGlatin"])
        d = self.diffs(comp, reference="WSGlatin")[("p", "firstlineindent")]
        self.assertEqual(d.baseline.source, "default")
        self.assertEqual(comp.copy([d]), (1, []))
        self.assertNotIn("FirstLineIndent", self.readSty("WSG", "Diglot2JN"))
        self.assertEqual(self.diffs(comp, reference="WSGlatin"), {})

    def test_copy_overridden(self):
        ''' custom.sty is read before ptxprint.sty, so a value there has to be countered; ptxprint-mods.sty
            is read after it, so a value there can't be, and the user is told '''
        from ptxprint.manager.styles import StyleComparison
        self.writeSty("WSGlatin", "Diglot2JN", "ptxprint.sty", "\\Marker p\n\\Color x0000ff\n")
        self.writeSty("WSG", "Diglot2JN", "ptxprint.sty", "\\Marker p\n\\Color x0000ff\n")
        with open(os.path.join(self.tmpdir.name, "WSG", "custom.sty"), "w", encoding="utf-8") as outf:
            outf.write("\\Marker q1\n\\LeftMargin 0.9\n")
        self.writeSty("WSG", "Diglot2JN", "ptxprint-mods.sty", "\\Marker q2\n\\LeftMargin 0.8\n")
        self.change(("project", "ifusecustomsty", "True"), ("project", "ifusemodssty", "True"))
        mods = self.readSty("WSG", "Diglot2JN", "ptxprint-mods.sty")
        comp = StyleComparison.acrossProjects(Validator(self.tmpdir.name), "Diglot2JN", ["WSG", "WSGlatin"])
        found = self.diffs(comp, reference="WSGlatin")
        want = found[("q1", "leftmargin")].baseline.raw
        changed, problems = comp.copy([found[("q1", "leftmargin")], found[("q2", "leftmargin")]])
        self.assertIn(f"\\Marker q1\n\\LeftMargin {want}", self.readSty("WSG", "Diglot2JN"))
        self.assertEqual(len(problems), 1)
        self.assertIn("q2", problems[0])
        self.assertIn("ptxprint-mods.sty", problems[0])
        left = self.diffs(comp, reference="WSGlatin")
        self.assertEqual(set(left), {("q2", "leftmargin")})
        # only ptxprint.sty is ever written
        self.assertEqual(mods, self.readSty("WSG", "Diglot2JN", "ptxprint-mods.sty"))
        with open(os.path.join(self.tmpdir.name, "WSG", "custom.sty"), encoding="utf-8") as inf:
            self.assertEqual(inf.read(), "\\Marker q1\n\\LeftMargin 0.9\n")

    def test_copy_window(self):
        try:
            from ptxprint.manager.gtkmanager import ManagerWindow, S_TICK, S_MARKER, S_ATTR
            from gi.repository import Gtk
            if not Gtk.init_check()[0]:
                raise ImportError("no display")
        except (ImportError, ValueError) as e:
            self.skipTest(f"No GTK: {e}")
        self.writeSty("WSG", "Diglot2JN", "ptxprint.sty",
                      "\\Marker s\n\\FontSize 14\n\\SpaceBefore 9\n\\FontName Charis\n\n\\Marker cat:coverfront|mt1\n\\FontSize 30\n"
                      "\n\\Marker p\n\\Color x0000ff\n\\SpaceBefore 0.5\n")
        win = ManagerWindow(self.tmpdir.name)
        try:
            win.configCombo.set_active_id("Diglot2JN")
            win.runStyleCompare()
            win.styleRef.set_active_id("WSGlatin")
            self.assertFalse(any(r[S_TICK] for r in win.styleTree.get_model()))        # nothing is ticked for the user
            self.assertFalse(win.styleCopyButton.get_sensitive())
            win.tickStyles(True)            # "tick shown" leaves the font and the cover style
            self.assertEqual(win.styleTicked, {("s", "fontsize"), ("s", "spacebefore")})
            win.tickStyles(False)
            win.tickStyles(True, marker="s")                                            # the whole style
            self.assertEqual(win.styleTicked, {("s", "fontsize"), ("s", "spacebefore"), ("s", "fontname")})
            win.styleTicked.discard(("s", "fontname"))
            win.styleCopyTo.set_active_id("WSGlatin")       # the reference itself: nothing of it differs
            self.assertEqual(win.styleCopyPlan()[0], [])
            win.styleCopyTo.set_active_id("")
            todo, columns = win.styleCopyPlan()
            self.assertEqual(len(todo), 2)
            self.assertIn("\\FontSize 14", self.readSty("WSG", "Diglot2JN"))            # nothing written until Copy
            changed, problems = win.copyStyles(todo, columns)
            self.assertEqual((changed, problems), (2, []))
            sty = self.readSty("WSG", "Diglot2JN")
            self.assertNotIn("\\FontSize 14", sty)
            self.assertNotIn("SpaceBefore 9", sty)
            self.assertIn("\\FontName Charis", sty)
            self.assertEqual({(r[S_MARKER], r[S_ATTR]) for r in win.styleTree.get_model()},
                             {("s", "fontname"), ("cat:coverfront|mt1", "fontsize")})
            self.assertEqual(win.styleTicked, set())
        finally:
            win.destroy()

    def test_ptxprint_reads_copy(self):
        ''' A value copied into ptxprint.sty is what PTXprint loads '''
        from ptxprint.manager.styles import StyleComparison
        from test_headless import loadview
        comp = StyleComparison.acrossProjects(Validator(self.tmpdir.name), "Diglot2JN", ["WSG", "WSGlatin"])
        comp.copy([self.diffs(comp, reference="WSG")[("s", "fontsize")]])          # WSGlatin takes WSG's 14
        view = loadview(self.tmpdir.name, "WSGlatin", "Diglot2JN")
        self.assertAlmostEqual(float(view.styleEditor.getval("s", "FontSize")) * 12, 14, places=1)

    def test_commonest(self):
        from ptxprint.manager.styles import StyleComparison
        # three configurations of one project, one out of step
        for cfg in ("A", "B", "C"):
            d = os.path.join(self.tmpdir.name, "WSG", "shared", "ptxprint", cfg)
            shutil.copytree(self.dest, d)
            self.writeSty("WSG", cfg, "ptxprint.sty", "\\Marker p\n\\FontSize {}\n".format(11 if cfg == "B" else 12))
        comp = StyleComparison.acrossConfigs(Validator(self.tmpdir.name), "WSG", ["A", "B", "C", "Nope"])
        self.assertEqual(comp.columns, ["A", "B", "C"])
        d = self.diffs(comp)[("p", "fontsize")]
        self.assertEqual((d.baseline.raw, d.differing), ("12", ["B"]))

    def test_command_and_window(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = main(["-p", self.tmpdir.name, "styles", "-c", "Diglot2JN", "-P", "WSG,WSGlatin", "--ref", "WSGlatin"])
            rc2 = main(["-p", self.tmpdir.name, "styles", "--within", "WSG", "-c", "Diglot2JN"])
        self.assertEqual((rc, rc2), (0, 2))
        self.assertIn("fontsize", out.getvalue())
        self.assertIn("1 style attributes differ", out.getvalue())
        try:
            from ptxprint.manager.gtkmanager import ManagerWindow, S_MARKER, S_ATTR, S_BASE, S_NFIXED, SAME
            from gi.repository import Gtk
            if not Gtk.init_check()[0]:
                raise ImportError("no display")
        except (ImportError, ValueError) as e:
            self.skipTest(f"No GTK: {e}")
        before = {f: open(os.path.join(self.dest, f), encoding="utf-8").read() for f in ("ptxprint.sty", "ptxprint.cfg")}
        win = ManagerWindow(self.tmpdir.name)
        try:
            win.configCombo.set_active_id("Diglot2JN")
            win.runStyleCompare()
            store = win.styleTree.get_model()
            self.assertEqual([(r[S_MARKER], r[S_ATTR]) for r in store], [("s", "fontsize")])
            cols = win.styleComparison.columns
            row = store[0]
            # with two, either is "what most have": the other shows its value, the first a dot
            self.assertEqual(sorted([row[S_NFIXED + i] for i in range(len(cols))]), sorted([SAME, "14"]) if row[S_BASE] == "12"
                             else sorted([SAME, "12"]))
            win.styleRef.set_active_id("WSG")
            row = win.styleTree.get_model()[0]
            self.assertEqual((row[S_BASE], row[S_NFIXED + cols.index("WSGlatin")], row[S_NFIXED + cols.index("WSG")]), ("14", "12", SAME))
            win.styleNonVisual.set_active(True)
            self.assertEqual(len(win.styleTree.get_model()), 2)
            win.styleFind.set_text("name")
            self.assertEqual([r[S_ATTR] for r in win.styleTree.get_model()], ["name"])
            win.styleFind.set_text("")
            win.styleGroup.set_active_id("Notes")
            self.assertEqual(len(win.styleTree.get_model()), 0)
            # the configurations of one project
            win.styleMode.set_active_id("configs")
            win.styleProject.set_active_id("WSG")
            win.styleConfigs.set_text("Diglot2JN Default")
            win.styleGroup.set_active_id("")
            win.runStyleCompare()
            self.assertEqual(win.styleComparison.columns, ["Diglot2JN", "Default"])
        finally:
            win.destroy()
        # looking changes nothing
        self.assertEqual(before, {f: open(os.path.join(self.dest, f), encoding="utf-8").read() for f in before})


class TestDiglotSides(_Projects):

    def test_set_side(self):
        v = Validator(self.tmpdir.name)
        self.assertEqual(v.diglotSides("WSG", "Diglot2JN")["R"], ("OGNT", "Default"))
        self.assertEqual(v.diglotSides("WSG", "Default"), {})
        for bad in (("L", "OGNT", "Default"), ("R", "WSG", "Default"), ("R", "Nope", "Default"), ("R", "OGNT", "NoCfg")):
            with self.assertRaises(ValueError):
                v.setDiglotSide("WSG", "Diglot2JN", *bad)
        v.setDiglotSide("WSG", "Diglot2JN", "R", "WSGlatin", "Default")
        self.assertEqual(v.diglotSides("WSG", "Diglot2JN")["R"], ("WSGlatin", "Default"))
        self.assertEqual(self.get("diglot_R", "projectguid"), v.projects["WSGlatin"].guid)

    def test_command(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = main(["-p", self.tmpdir.name, "secondary", "-c", "Diglot2JN"])
            rc2 = main(["-p", self.tmpdir.name, "secondary", "-c", "Diglot2JN", "--to", "WSGlatin"])    # which project?
            rc3 = main(["-p", self.tmpdir.name, "secondary", "-c", "Diglot2JN", "-P", "WSG", "--to", "WSGlatin"])
        self.assertEqual((rc, rc2, rc3), (0, 2, 0))
        self.assertIn("WSG / Diglot2JN: R is OGNT, Default", out.getvalue())
        self.assertEqual(self.get("diglot_R", "projectid"), "WSGlatin")


class TestTestPrint(_Projects):

    def test_not_tried(self):
        from ptxprint.manager.testprint import TestPrinter, SKIPPED
        t = TestPrinter(Validator(self.tmpdir.name))
        self.assertEqual(t.booksIn("jas, GLO  3jn"), ["JAS", "GLO", "3JN"])
        self.assertEqual(t.run("WSGlatin", "Default", "XXQ").status, SKIPPED)
        self.assertEqual(t.run("WSGlatin", "Default", "").status, SKIPPED)

    def test_tex_error(self):
        from ptxprint.manager.testprint import texError
        log = os.path.join(self.tmpdir.name, "x.log")
        with open(log, "w", encoding="utf-8") as outf:
            outf.write("This is XeTeX\n! Missing number, treated as zero.\n<to be read again>\n   \\relax\nl.151 \\polyglotendcols\n")
        self.assertEqual(texError(log), "Missing number, treated as zero.  [at l.151 \\polyglotendcols]")
        self.assertEqual(texError(os.path.join(self.tmpdir.name, "none.log")), "")

    def test_real_print(self):
        ''' PTXprint is run as a separate program and its result reported, whichever it is '''
        from ptxprint.manager.testprint import TestPrinter, PRINTED, FAILED
        t = TestPrinter(Validator(self.tmpdir.name), timeout=600)
        res = t.run("WSGlatin", "Default", "2JN")
        self.assertIn(res.status, (PRINTED, FAILED), res)
        if res.status == PRINTED:
            self.assertTrue(os.path.exists(res.pdf))
        else:       # e.g. the project's fonts aren't installed on this machine
            self.assertTrue(res.message)
        # a diglot whose other project is missing is a failure with its reason
        self.change(("diglot_L", "projectid", "WSG"), ("diglot_R", "projectid", "NoSuchBT"), ("diglot_R", "projectguid", "0" * 40))
        res = t.run("WSG", "Diglot2JN", "JHN")
        self.assertEqual(res.status, FAILED, res)
        self.assertIn("NoSuchBT", res.message)

if __name__ == "__main__":
    unittest.main()
