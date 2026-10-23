import os, sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python", "lib"))

pypdf = pytest.importorskip("pypdf")
gi = pytest.importorskip("gi")
try:
    gi.require_version('Poppler', '0.18')
    from gi.repository import Poppler
except (ValueError, ImportError):
    pytest.skip("Poppler not available", allow_module_level=True)

from pypdf.generic import RectangleObject, DecodedStreamObject, NameObject
from ptxprint.pdf.pdfdiff import createDiff


def makePDF(path, margin, extra=""):
    """ A 300x400 page with a square on it, surrounded by `margin` of media (like crop marks give). """
    w = pypdf.PdfWriter()
    page = w.add_blank_page(300 + 2 * margin, 400 + 2 * margin)
    s = DecodedStreamObject()
    s.set_data(f"{50 + margin} {50 + margin} 60 60 re f {extra}".encode())
    page[NameObject("/Contents")] = w._add_object(s)
    page.trimbox = RectangleObject([margin, margin, margin + 300, margin + 400])
    w.write(str(path))
    return str(path)


def noError(*a, **kw):
    raise AssertionError(f"Unexpected error report: {a}")


def test_cropmarksIgnoredByDefault(tmp_path):
    plain = makePDF(tmp_path / "plain.pdf", 0)
    crops = makePDF(tmp_path / "crops.pdf", 20, extra="0 0 10 10 re f")     # a mark in the margin only
    assert createDiff(plain, crops, str(tmp_path / "d.pdf"), noError) == 0


def test_realChangeStillFound(tmp_path):
    plain = makePDF(tmp_path / "plain.pdf", 0)
    changed = makePDF(tmp_path / "changed.pdf", 20, extra="150 150 30 30 re f")
    out = str(tmp_path / "d.pdf")
    assert createDiff(plain, changed, out, noError) == out


def test_wholePageSizeMismatchReported(tmp_path):
    plain = makePDF(tmp_path / "plain.pdf", 0)
    crops = makePDF(tmp_path / "crops.pdf", 20)
    errors = []
    res = createDiff(plain, crops, str(tmp_path / "d.pdf"), lambda *a, **kw: errors.append(a), boxmode="page")
    assert res == 3 and len(errors) == 1


def makeBook(path, positions):
    """ One page per entry in positions: a square at that x offset, so each page differs from the others. """
    w = pypdf.PdfWriter()
    for x in positions:
        page = w.add_blank_page(300, 400)
        s = DecodedStreamObject()
        s.set_data(f"{x} 50 40 40 re f".encode())
        page[NameObject("/Contents")] = w._add_object(s)
    w.write(str(path))
    return str(path)


def test_offsetSkipsExtraPagesInOld(tmp_path):
    new = makeBook(tmp_path / "new.pdf", [20, 80, 140])
    old = makeBook(tmp_path / "old.pdf", [200, 20, 80, 140])        # old has an extra page at the front
    assert createDiff(new, old, str(tmp_path / "d.pdf"), noError) != 0
    assert createDiff(new, old, str(tmp_path / "d.pdf"), noError, offset=1) == 0


def test_negativeOffsetSkipsExtraPagesInNew(tmp_path):
    new = makeBook(tmp_path / "new.pdf", [200, 20, 80, 140])        # new has an extra page at the front
    old = makeBook(tmp_path / "old.pdf", [20, 80, 140])
    assert createDiff(new, old, str(tmp_path / "d.pdf"), noError, offset=-1) == 0


def test_offsetStillFindsChanges(tmp_path):
    new = makeBook(tmp_path / "new.pdf", [20, 80, 150])
    old = makeBook(tmp_path / "old.pdf", [200, 20, 80, 140])
    out = str(tmp_path / "d.pdf")
    assert createDiff(new, old, out, noError, offset=1) == out
