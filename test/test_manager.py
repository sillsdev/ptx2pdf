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
