import sys, os, re, types, shutil, tempfile, unittest
from pathlib import Path
import pytest

# Tests are unittest classes so test/conftest.py does not parametrize them as projects.

# Load ptxprint.marginnotes without pulling in GTK and friends
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python", "lib"))
_premodules = set(sys.modules)
if "ptxprint" not in sys.modules:
    pkg = types.ModuleType("ptxprint")
    pkg.__path__ = [os.path.join(os.path.dirname(__file__), "..", "python", "lib", "ptxprint")]
    sys.modules["ptxprint"] = pkg
for modname in ("ptxprint.utils", "ptxprint.parlocs"):
    if modname not in sys.modules:
        sys.modules[modname] = types.ModuleType(modname)

def _readpts(s):
    s = re.sub(r"(?:\s*(?:plus|minus)\s+[-\d.]+\s*(?:pt|in|sp|em))+$", "", s)
    if s.endswith("pt"):
        return float(s[:-2])
    elif s.endswith("sp"):
        return float(s[:-2]) / 65536.
    return float(s) / 65536.

sys.modules["ptxprint.utils"].universalopen = getattr(sys.modules["ptxprint.utils"], "universalopen",
                                                      lambda f: open(f, encoding="utf-8"))
sys.modules["ptxprint.parlocs"].readpts = getattr(sys.modules["ptxprint.parlocs"], "readpts", _readpts)

from ptxprint.marginnotes import MarginNotes, tidymarginnotes

for k in set(sys.modules) - _premodules:
    if k == "ptxprint" or k.startswith("ptxprint."):
        del sys.modules[k]

TOP = 500.
BOT = 100.

def note(ref, pnum=1, xpos=50., ypos=400., yoff=0., marker="f", hpos="outer", vpos="top",
         height=20., depth=0., width=50., gap=5.):
    ''' A note line as TeX writes it. ypos is the note's position this run. '''
    return ("\\@marginnote{{{}}}{{{}}}{{{}}}{{{}}}{{{}pt}}{{{}pt}}{{{}pt}}{{{}pt}}{{0.0pt}}{{{}pt}}"
            "{{{}}}{{{}}}{{{}}}\n").format(ref, marker, hpos, vpos, gap, width, height, depth, yoff,
                                         pnum, int(round(xpos * 65536)), int(round(ypos * 65536)))

def run(tmp_path, text, name="test.marginnotes", **kw):
    ''' Runs one pass. Returns (changed, output text, MarginNotes) '''
    fpath = tmp_path / name
    fpath.write_text(text, encoding="utf-8")
    kw.setdefault("top", TOP)
    kw.setdefault("bot", BOT)
    m = MarginNotes(str(fpath), **kw)
    m.processpages()
    changed = m.outfile(str(fpath))
    return changed, fpath.read_text(encoding="utf-8"), m

def converge(tmp_path, text, **kw):
    ''' Runs a pass, then checks a second pass is a fixed point '''
    changed, out, m = run(tmp_path, text, **kw)
    changed2, out2, _ = run(tmp_path, out, **kw)
    assert out2 == out
    assert not changed2
    return changed, out, m

def parse(out):
    notes = {}
    pushes = {}
    for l in out.splitlines():
        f = re.findall(r"\{(.*?)\}", l)
        if l.startswith("\\@marginnotepush"):
            pushes[f[0]] = (int(f[2]), int(f[3]), f[4])
        else:
            notes[f[0]] = {"yoffset": float(f[9][:-2]), "pnum": int(f[10]),
                           "ypos": int(f[12]) / 65536., "anchor": int(f[12]) / 65536. + float(f[9][:-2])}
    return notes, pushes

def byref(m):
    return {n.ref: n for n in m.notes}

def twocol(rtl=False, extra=""):
    x0, x1 = (250., 50.) if rtl else (50., 250.)
    text = "".join(note("C{}".format(i), xpos=x0, ypos=490.-i*16) for i in range(22))
    text += "".join(note("D{}".format(i), xpos=x1, ypos=490.-i*16) for i in range(23))
    text += note("E1", pnum=2, xpos=x0, ypos=300.) + extra
    return text


class TestMarginNotes(unittest.TestCase):

    def setUp(self):
        self.tmp_path = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp_path, ignore_errors=True)

    def test_fixedpoint_texformat(self):
        text = note("A", ypos=300.) + note("B", ypos=200.)
        changed, out, _ = converge(self.tmp_path, text)
        assert not changed      # only the number formatting differs

    def test_tex_spelling(self):
        # TeX prints 10182296sp as 155.3695pt, we print it as 155.36951pt
        _, out, _ = run(self.tmp_path, note("A", ypos=300., yoff=155.3695))
        changed, _, _ = run(self.tmp_path, out.replace("155.36951pt", "155.3695pt"))
        assert not changed

    def test_doubleshift(self):
        text = "".join(note(r, ypos=300.) for r in "ABCD")
        changed, out, _ = converge(self.tmp_path, text)
        assert changed
        first, _ = parse(out)
        for i in range(3):
            _, out, _ = run(self.tmp_path, out)
        again, _ = parse(out)
        assert again == first
        # equal weights spread the four notes evenly around their anchor
        assert first["A"]["yoffset"] == pytest.approx(-30.)
        assert first["D"]["yoffset"] == pytest.approx(30.)

    def test_single_note_bounds(self):
        # note with a stale -12.45pt offset whose top is 8.3pt above the text block
        text = note("A", ypos=510., yoff=-12.45, height=10.75)
        changed, out, m = converge(self.tmp_path, text)
        assert changed
        n = byref(m)["A"]
        assert n.ymax + n.yshift == pytest.approx(TOP)
        notes, _ = parse(out)
        assert notes["A"]["anchor"] == pytest.approx(497.55, abs=1e-4)

    def test_stale_offset_removed(self):
        text = note("A", ypos=300., yoff=-12.45)
        changed, out, _ = converge(self.tmp_path, text)
        assert changed
        notes, _ = parse(out)
        assert notes["A"]["yoffset"] == 0
        assert notes["A"]["ypos"] == pytest.approx(287.55, abs=1e-4)

    def test_bottom_bounds(self):
        text = note("A", ypos=90.)        # bottom 90, below the text block
        changed, out, m = converge(self.tmp_path, text)
        n = byref(m)["A"]
        assert n.ymin + n.yshift == pytest.approx(BOT)

    def test_single_column_overflow(self):
        # 25 notes of 20pt on page 1 (cap 400 = 20 notes), 2 notes on page 2
        text = "".join(note("A{}".format(i), ypos=490.-i*16) for i in range(25))
        text += note("B1", pnum=2, ypos=480.) + note("B2", pnum=2, ypos=300.)
        changed, out, m = converge(self.tmp_path, text, ncols=1)
        notes, pushes = parse(out)
        assert set(pushes) == {"A{}".format(i) for i in range(20, 25)}
        assert all(p[:2] == (2, 0) for p in pushes.values())
        assert pushes["A20"][2] == "left"           # outer on an even page
        lines = out.splitlines()
        assert lines[-5:] == ["\\@marginnotepush{{A{}}}{{f}}{{2}}{{0}}{{left}}".format(i) for i in range(20, 25)]
        ns = byref(m)
        # pushed note lines are unchanged anchors
        for i in range(20, 25):
            assert ns["A{}".format(i)].inline in out
        for i in range(20, 25):
            assert ns["A{}".format(i)].yshift == 0
        # natives on page 2 lie below the 100pt block
        assert ns["B1"].ymax + ns["B1"].yshift == pytest.approx(TOP - 100.)
        assert ns["B2"].yshift == 0
        # the rest of page 1 fits exactly
        assert ns["A0"].ymax + ns["A0"].yshift == pytest.approx(TOP)
        assert ns["A19"].ymin + ns["A19"].yshift == pytest.approx(BOT)

    def test_two_columns(self):
        for rtl in (False, True):
            with self.subTest(rtl=rtl):
                changed, out, m = converge(self.tmp_path, twocol(rtl), rtl=rtl)
                assert m.ncols == 2
                notes, pushes = parse(out)
                # col 0 overflow (C20, C21) goes to col 1 on page 1 ahead of col 1's own notes,
                # which then overflow (D18..D22) to col 0 of page 2
                assert pushes["C20"] == (1, 1, "left" if rtl else "right")
                assert pushes["C21"] == (1, 1, "left" if rtl else "right")
                for i in range(18, 23):
                    assert pushes["D{}".format(i)] == (2, 0, "right" if rtl else "left")
                assert "D17" not in pushes
                pushorder = [l for l in out.splitlines() if l.startswith("\\@marginnotepush")]
                assert [re.findall(r"\{(.*?)\}", l)[0] for l in pushorder] == ["C20", "C21"] + ["D{}".format(i) for i in range(18, 23)]
                ns = byref(m)
                assert ns["E1"].ymax + ns["E1"].yshift <= TOP - 100. + 1e-6

    def test_cascade(self):
        text = "".join(note("A{}".format(i), height=40., ypos=490.-i*5) for i in range(25))     # 10 fit, 15 pushed
        text += note("B1", pnum=2, ypos=450.) + note("B2", pnum=2, ypos=400.)
        changed, out, m = converge(self.tmp_path, text, ncols=1)
        notes, pushes = parse(out)
        assert all(pushes["A{}".format(i)][0] == 2 for i in range(10, 20))
        assert all(pushes["A{}".format(i)][0] == 3 for i in range(20, 25))
        assert pushes["B1"][0] == 3 and pushes["B2"][0] == 3
        order = [re.findall(r"\{(.*?)\}", l)[0] for l in out.splitlines() if l.startswith("\\@marginnotepush")]
        assert order[-7:] == ["A20", "A21", "A22", "A23", "A24", "B1", "B2"]

    def test_oversized(self):
        text = note("A", height=450., ypos=490.) + note("B", ypos=200.)
        with self.assertLogs("ptxprint.marginnotes", level="ERROR") as logs:
            changed, out, m = converge(self.tmp_path, text, ncols=1)
        assert any("too tall" in l for l in logs.output)
        notes, pushes = parse(out)
        assert "A" not in pushes
        assert pushes["B"] == (2, 0, "left")
        assert byref(m)["A"].ymax + byref(m)["A"].yshift == pytest.approx(TOP)

    def test_oversized_pushed(self):
        text = note("A", ypos=490.) + note("B", height=450., ypos=200., vpos="bottom") + note("C", ypos=150.)
        changed, out, m = converge(self.tmp_path, text, ncols=1)
        notes, pushes = parse(out)
        assert pushes["B"] == (2, 0, "left")
        assert pushes["C"] == (3, 0, "right")

    def test_fixed_side(self):
        text = "".join(note("C{}".format(i), hpos="left", xpos=50., ypos=490.-i*16) for i in range(22))
        text += note("D1", xpos=250., ypos=400.)
        changed, out, m = converge(self.tmp_path, text)
        notes, pushes = parse(out)
        assert pushes["C20"] == (2, 0, "left")
        assert pushes["C21"] == (2, 0, "left")

    def test_fixed_side_rtl(self):
        text = "".join(note("C{}".format(i), hpos="right", xpos=250., ypos=490.-i*16) for i in range(22))
        text += note("D1", xpos=50., ypos=400.)
        changed, out, m = converge(self.tmp_path, text, rtl=True)
        notes, pushes = parse(out)
        assert pushes["C20"] == (2, 0, "right")

    def test_coming_back(self):
        text = "".join(note("A{}".format(i), ypos=490.-i*16) for i in range(22))
        changed, out, m = converge(self.tmp_path, text, ncols=1)
        assert "\\@marginnotepush" in out
        # delete two notes from what TeX would write next time (pushes echoed)
        lines = [l for l in out.splitlines(True) if not l.startswith("\\@marginnote{A0}") and not l.startswith("\\@marginnote{A1}")]
        changed, out, m = converge(self.tmp_path, "".join(l for l in lines if not l.startswith("\\@marginnotepush")), ncols=1)
        assert "\\@marginnotepush" not in out

    def test_pushes_fixed_point_with_echo(self):
        ''' If TeX echoes the push lines it read, a rerun with no movement reports no change '''
        text = "".join(note("A{}".format(i), ypos=490.-i*16) for i in range(22))
        _, out, _ = run(self.tmp_path, text, ncols=1)
        pushes = [l for l in out.splitlines(True) if l.startswith("\\@marginnotepush")]
        notes = [l for l in out.splitlines(True) if not l.startswith("\\@marginnotepush")]
        changed, out2, _ = run(self.tmp_path, "".join(pushes + notes), ncols=1)
        assert not changed

    def grid(self, text, **kw):
        _, _, m = run(self.tmp_path, text, **kw)
        return m

    def test_grid_mirrored(self):
        text = note("A", pnum=1, xpos=50.) + note("B", pnum=1, xpos=250.) \
             + note("C", pnum=2, xpos=70.) + note("D", pnum=2, xpos=270.)
        m = self.grid(text)
        assert m.ncols == 2
        assert m.grid[1] == [50., 250.] and m.grid[0] == [70., 270.]
        assert [n.col for n in m.notes] == [0, 1, 0, 1]

    def test_grid_outlier(self):
        text = note("A", xpos=50.) + note("B", xpos=50.) + note("C", xpos=250.) + note("D", xpos=250.) \
             + note("E", xpos=150.5)
        m = self.grid(text)
        assert m.grid[1] == [50., 250.]
        assert byref(m)["E"].col == 1

    def test_grid_single(self):
        text = note("A", pnum=1, xpos=50.) + note("B", pnum=2, xpos=70.)
        m = self.grid(text)
        assert m.ncols == 1
        assert [n.col for n in m.notes] == [0, 0]
        m = self.grid(text + note("C", pnum=1, xpos=250.), ncols=1)
        assert m.ncols == 1

    def test_grid_one_parity(self):
        text = note("A", pnum=1, xpos=50.) + note("B", pnum=1, xpos=250.) + note("C", pnum=2, xpos=268.)
        m = self.grid(text)
        assert m.grid[0] == [68., 268.]
        assert byref(m)["C"].col == 1

if __name__ == "__main__":
    unittest.main()
