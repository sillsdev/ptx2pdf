import os, sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python", "lib"))

pytest.importorskip("gi")
try:
    from ptxprint.gtkview import GtkViewModel
except Exception as e:      # no display / GTK
    pytest.skip(f"GtkViewModel not importable: {e}", allow_module_level=True)

DEFAULT = "Previous PDF (_1)"


class Stub:
    """ Just enough of the view for checkDiffPDF """
    def __init__(self, value):
        self.widgets = {"btn_selectDiffPDF": value, "lb_diffPDF": "x"}
        self.diffPDF = "unset"
        self.bold = None
        self.status = []

    def get(self, wid, default=None, **kw):
        return self.widgets.get(wid, default)

    def set(self, wid, value, **kw):
        self.widgets[wid] = value

    def makeLabelBold(self, lbl, bold=True):
        self.bold = bold

    def doStatus(self, txt="", warning=False):
        self.status.append(txt)


def check(value, announce=False):
    s = Stub(value)
    res = GtkViewModel.checkDiffPDF(s, announce=announce)
    return s, res


@pytest.mark.parametrize("junk", ["Select a particular PDF file to be compared",
                                  "document/diffpdf(btn_selectDiffPDF)",
                                  "C:/no/such/folder/old_1.pdf",
                                  "."])
def test_junkResetToPrevious(junk):
    s, res = check(junk, announce=True)
    assert res is True
    assert s.widgets["btn_selectDiffPDF"] is None
    assert s.diffPDF is None
    assert s.bold is False
    assert s.widgets["lb_diffPDF"] == DEFAULT
    assert len(s.status) == 1


@pytest.mark.parametrize("empty", [None, "", "  "])
def test_nothingChosenIsQuietlyThePreviousPDF(empty):
    s, res = check(empty, announce=True)
    assert res is False
    assert s.widgets["btn_selectDiffPDF"] is None
    assert s.widgets["lb_diffPDF"] == DEFAULT
    assert s.status == []


def test_existingPDFIsKept(tmp_path):
    f = tmp_path / "old_1.pdf"
    f.write_bytes(b"%PDF-1.4")
    s, res = check(str(f), announce=True)
    assert res is False
    assert s.widgets["btn_selectDiffPDF"] == str(f)
    assert s.widgets["lb_diffPDF"] == "old_1.pdf"
    assert s.bold is True
    assert s.diffPDF is not None


def test_existingFileThatIsNotAPDFIsReset(tmp_path):
    f = tmp_path / "notes.txt"
    f.write_text("hello")
    s, res = check(str(f))
    assert res is True and s.widgets["btn_selectDiffPDF"] is None
