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
from ptxprint.pdf.pdfdiff import createDiff, columnExtents


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


def makeZoned(path, header, left):
    """ A 300x400 page (about 106x141mm) with body text in the middle, plus optional marks in the top
        margin (header) and in the left margin. """
    w = pypdf.PdfWriter()
    page = w.add_blank_page(300, 400)
    s = DecodedStreamObject()
    ops = "100 150 50 50 re f "
    if header:
        ops += "100 385 40 8 re f "
    if left:
        ops += "5 200 12 40 re f "
    s.set_data(ops.encode())
    page[NameObject("/Contents")] = w._add_object(s)
    w.write(str(path))
    return str(path)


# 10mm top and bottom margins (28pt); the text is between x=40 and x=260
geometry = {"top": 10, "bottom": 10, "sides": {0: (40., 260.)}}


def test_headerChangeIgnored(tmp_path):
    new = makeZoned(tmp_path / "new.pdf", True, False)
    old = makeZoned(tmp_path / "old.pdf", False, False)
    assert createDiff(new, old, str(tmp_path / "d.pdf"), noError) != 0
    assert createDiff(new, old, str(tmp_path / "d.pdf"), noError, ignore=("topbottom",), geometry=geometry) == 0
    assert createDiff(new, old, str(tmp_path / "d.pdf"), noError, ignore=("sides",), geometry=geometry) != 0


def test_sideChangeIgnored(tmp_path):
    new = makeZoned(tmp_path / "new.pdf", False, True)
    old = makeZoned(tmp_path / "old.pdf", False, False)
    assert createDiff(new, old, str(tmp_path / "d.pdf"), noError) != 0
    assert createDiff(new, old, str(tmp_path / "d.pdf"), noError, ignore=("sides",), geometry=geometry) == 0
    assert createDiff(new, old, str(tmp_path / "d.pdf"), noError, ignore=("topbottom",), geometry=geometry) != 0


def test_bodyChangeNeverIgnored(tmp_path):
    new = makeBook(tmp_path / "new.pdf", [100])
    old = makeBook(tmp_path / "old.pdf", [150])
    out = str(tmp_path / "d.pdf")
    assert createDiff(new, old, out, noError, ignore=("topbottom", "sides"), geometry=geometry) == out


def test_columnExtents(tmp_path):
    bs = chr(92)
    sp = lambda pts: str(int(pts * 65536))        # scaled points: 65536 to the point
    lines = ["@pgstart{1}{400.0pt}{300.0pt}{400.0pt}",
             "@colstart{100.0pt}{0.0pt}{200.0pt}{" + sp(50) + "}{" + sp(380) + "}",
             "@pgstart{2}{0.0pt}{300.0pt}{400.0pt}",                    # no text columns
             "@pgstart{3}{400.0pt}{300.0pt}{400.0pt}",                  # two columns
             "@colstart{100.0pt}{0.0pt}{90.0pt}{" + sp(30) + "}{" + sp(380) + "}",
             "@colstart{100.0pt}{0.0pt}{90.0pt}{" + sp(150) + "}{" + sp(380) + "}"]
    f = tmp_path / "x.parlocs"
    f.write_text("".join(bs + l + chr(10) for l in lines), encoding="utf-8")
    ext = columnExtents(str(f))
    assert sorted(ext) == [0, 2]
    tobp = 72. / 72.27
    assert ext[0] == pytest.approx((50 * tobp, 250 * tobp))
    assert ext[2] == pytest.approx((30 * tobp, 240 * tobp))
    assert columnExtents(str(tmp_path / "missing.parlocs")) == {}


def test_extraPageIsADifference(tmp_path):
    two = makeBook(tmp_path / "two.pdf", [20, 80])
    three = makeBook(tmp_path / "three.pdf", [20, 80, 140])
    out = str(tmp_path / "d.pdf")
    assert createDiff(three, two, out, noError) == out        # a page that is not in the old PDF
    assert createDiff(two, three, out, noError) == out        # a page that is no longer in the new PDF


def test_nothingToCompareIsReported(tmp_path):
    new = makeBook(tmp_path / "new.pdf", [20, 80])
    old = makeBook(tmp_path / "old.pdf", [20, 80])
    assert createDiff(new, old, str(tmp_path / "d.pdf"), noError, offset=5) == 5


def test_subPixelShiftAndSpecksAreNotDifferences(tmp_path):
    def make(path, dx, speck):
        w = pypdf.PdfWriter()
        page = w.add_blank_page(300, 400)
        s = DecodedStreamObject()
        ops = f"{100 + dx} 150 50 50 re f "
        if speck:
            ops += "200 300 1 2 re f "
        s.set_data(ops.encode())
        page[NameObject("/Contents")] = w._add_object(s)
        w.write(str(path))
        return str(path)
    new = make(tmp_path / "new.pdf", 0.2, True)      # 0.2pt is well under a pixel; a speck is not a change
    old = make(tmp_path / "old.pdf", 0., False)
    assert createDiff(new, old, str(tmp_path / "d.pdf"), noError) == 0
