''' Only a real click on Local Front Matter may switch the Colophon (issue #1270).

    Setting the check box from code fires the same signal, with the button as the argument, so the
    Cover Wizard turning Local Front Matter on used to untick Colophon. This calls the real handler
    on a stub, so that it needs no window.
'''

import os, sys, tempfile, unittest

testsdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(testsdir, "..", "python", "lib"))

from ptxprint.gtkview import GtkViewModel

class FakeButton:
    ''' What a button looks like when the user has clicked it: it has the focus '''
    def has_focus(self):
        return True

    def get_inconsistent(self):
        return False

class StubView:
    def __init__(self, frontmatter, colophon, frtfile):
        self.vals = {"c_frontmatter": frontmatter, "c_colophon": colophon,
                     "c_makeCoverPage": False, "l_statusLine": ""}
        self.loadingConfig = False
        self.frtfile = frtfile

    def get(self, k, *a, **kw):
        return self.vals.get(k)

    def set(self, k, v, *a, **kw):
        self.vals[k] = v

    def configFRT(self):
        return self.frtfile

    def doStatus(self, *a, **kw):
        pass

class TestColophonSwitch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from gi.repository import Gtk
        cls.Gtk = Gtk
        cls.tmpdir = tempfile.TemporaryDirectory()
        cls.frt = os.path.join(cls.tmpdir.name, "FRTlocal.sfm")
        with open(cls.frt, "w", encoding="utf-8") as outf:
            outf.write("\\id FRT\n")      # not empty, so the handler does not generate one

    @classmethod
    def tearDownClass(cls):
        cls.tmpdir.cleanup()

    def click(self, w, frontmatter, colophon):
        view = StubView(frontmatter, colophon, self.frt)
        GtkViewModel.onLocalFRTclicked(view, w)
        return view.vals["c_colophon"]

    def test_set_from_code_leaves_colophon(self):
        ''' The Cover Wizard turns Local Front Matter on with set(): the button is passed, with no focus '''
        button = self.Gtk.CheckButton()
        self.assertFalse(button.has_focus())
        self.assertTrue(self.click(button, frontmatter=True, colophon=True))
        self.assertTrue(self.click(button, frontmatter=False, colophon=False) is False)

    def test_called_by_ptxprint_leaves_colophon(self):
        self.assertTrue(self.click(None, frontmatter=True, colophon=True))
        self.assertTrue(self.click(None, frontmatter=False, colophon=False) is False)

    def test_user_click_still_switches(self):
        ''' Turning Local Front Matter on by hand turns the Colophon off, and off turns it on '''
        self.assertFalse(self.click(FakeButton(), frontmatter=True, colophon=True))
        self.assertTrue(self.click(FakeButton(), frontmatter=False, colophon=False))

    def noupdate(self, w, noupdate, colophon):
        view = StubView(False, colophon, self.frt)
        view.vals["c_noupdate"] = noupdate
        GtkViewModel.onNoUpdateClicked(view, w)
        return view.vals["c_colophon"]

    def test_layout_only_restored_from_code_leaves_colophon(self):
        ''' Layout Only is on by default and PTXprint re-sets it after every config load: not a user click '''
        button = self.Gtk.CheckButton()
        self.assertTrue(self.noupdate(button, noupdate=True, colophon=True))

    def test_user_ticking_layout_only_still_switches_colophon_off(self):
        self.assertFalse(self.noupdate(FakeButton(), noupdate=True, colophon=True))

    def test_loading_a_config_changes_nothing(self):
        view = StubView(True, True, self.frt)
        view.loadingConfig = True
        GtkViewModel.onLocalFRTclicked(view, FakeButton())
        self.assertTrue(view.vals["c_colophon"])

if __name__ == "__main__":
    unittest.main()
