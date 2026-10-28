import os, sys, time
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python", "lib"))

gi = pytest.importorskip("gi")
try:
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from ptxprint.adjlist import AdjList
    from ptxprint.parlocs import ParInfo
    from ptxprint.pdf_viewer import PDFContentViewer
except (ValueError, ImportError) as e:
    pytest.skip(f"GTK / ptxprint not importable: {e}", allow_module_level=True)

ADJ = "MRK 1.1 +1\nMRK 1.3 -1[2] % expand=97\nMRK 3.7-8 +2\nMRK 4.2 +1 % keep this\n"


def makeAdj(path, centre=100, text=ADJ):
    path.write_text(text, encoding="utf-8")
    a = AdjList(centre, 5, 5, gtk=Gtk, fname=str(path), tname=str(path) + ".triggers")
    a.readAdjlist(str(path))
    return a


class Viewer:
    """ Just enough of the PDF viewer for on_reset_adjustments """
    def __init__(self, adj):
        self.adjlist = adj
    def disableLayoutOnly(self): pass
    def show_pdf(self): pass
    def hitPrint(self): pass


def para(ref, parnum=None):
    p = ParInfo(ref, "p", "p", 0., None)
    if parnum is not None:
        p.parnum = parnum
    return p


def reset(adj, p):
    pn = getattr(p, 'parnum', 0) or 0
    info = adj.getinfo(p.ref + (f"[{pn}]" if pn > 1 else ""), insert=True)     # as the right-click menu does
    PDFContentViewer.on_reset_adjustments(Viewer(adj), None, 'para', 1, info, p)


def rows(adj):
    return {(r[0] + r[1], r[2]): (r[3], r[5]) for r in adj.liststore}


@pytest.mark.parametrize("p, key", [
    (para("MRK1.1"), ("MRK1.1", 1)),               # no paragraph number recorded: the reported bug
    (para("MRK1.1", 1), ("MRK1.1", 1)),
    (para("MRK1.3", 2), ("MRK1.3", 2)),
    (para("MRK3.7-8"), ("MRK3.7-8", 1)),           # a verse bridge, no paragraph number
])
def test_resetFindsTheParagraph(tmp_path, p, key):
    adj = makeAdj(tmp_path / "MRK.adj")
    assert rows(adj)[key][0] != "0"
    reset(adj, p)
    assert rows(adj)[key] == ("0", 100)
    assert adj.changed
    others = {k: v for k, v in rows(adj).items() if k != key}
    assert all(v[0] != "0" for v in others.values())      # only that paragraph was reset


def test_resetUsesTheFontsOwnWidth(tmp_path):
    adj = makeAdj(tmp_path / "MRK.adj", centre=90, text="MRK 1.1 +1 % expand=95\n")
    reset(adj, para("MRK1.1"))
    assert rows(adj)[("MRK1.1", 1)] == ("0", 90)


def test_resetParagraphsLeaveTheFile(tmp_path):
    f = tmp_path / "MRK.adj"
    adj = makeAdj(f)
    reset(adj, para("MRK1.1"))
    reset(adj, para("MRK1.3", 2))
    reset(adj, para("MRK4.2"))                      # has a comment, so it stays (as 0)
    adj.save()
    text = f.read_text(encoding="utf-8")
    assert "1.1" not in text and "1.3" not in text
    assert "MRK 3.7-8 +2" in text
    assert "MRK 4.2 0" in text and "keep this" in text


def test_handEditIsReadBack(tmp_path):
    f = tmp_path / "MRK.adj"
    adj = makeAdj(f)
    time.sleep(0.05)
    f.write_text("MRK 2.2 -1\n", encoding="utf-8")
    os.utime(f, (time.time() + 5, time.time() + 5))      # make sure the time differs on coarse file systems
    assert adj.reloadIfChanged()
    assert list(rows(adj)) == [("MRK2.2", 1)]
    assert len(adj.db) == len(adj.liststore)
    assert not adj.reloadIfChanged()                     # nothing more to read


def test_deletedFileEmptiesTheList(tmp_path):
    f = tmp_path / "MRK.adj"
    adj = makeAdj(f)
    f.unlink()
    assert adj.reloadIfChanged()
    assert len(adj.liststore) == 0


def test_unsavedChangesInPTXprintWin(tmp_path):
    f = tmp_path / "MRK.adj"
    adj = makeAdj(f)
    reset(adj, para("MRK1.1"))                           # changed in PTXprint, not saved yet
    f.write_text("MRK 2.2 -1\n", encoding="utf-8")
    os.utime(f, (time.time() + 5, time.time() + 5))
    assert not adj.reloadIfChanged()
    assert rows(adj)[("MRK1.1", 1)] == ("0", 100)


def test_savingDoesNotLookLikeAHandEdit(tmp_path):
    f = tmp_path / "MRK.adj"
    adj = makeAdj(f)
    reset(adj, para("MRK1.1"))
    adj.save()
    assert not adj.reloadIfChanged()
