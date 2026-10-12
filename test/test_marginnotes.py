#!/usr/bin/python3
"""Convergence regressions for https://github.com/sillsdev/ptx2pdf/issues/1258.

The process-output tests inject coordinates; they are not natural XeTeX
reproductions.
"""

import unittest, tempfile, shutil
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from ptxprint.marginnotes import SP, MarginNote, MarginNotes
from ptxprint import runjob

ONE_SP = 1 / SP  # one scaled point, in pt


def note(y):
    return MarginNote("GEN1.1", "f", "inner", "bottom", 8.5, 68, 10,
                      0, 0, 0, 0, 100, y)


def margin_record(y, pnum=1):
    return (r"\@marginnote{GEN1.1}{f}{inner}{bottom}{8.50000pt}{68.00000pt}"
            r"{10.00000pt}{0.00000pt}{0.00000pt}{0.00000pt}"
            f"{{{pnum}}}{{6553600}}"
            f"{{{y}}}\n")


def par_record(y, par_y=19660800):
    return (rf"\@parstart {{GEN1.1}}{{versetext}}{{p}}{{12.83333pt}}{{6553600}}{{{par_y}}}" + "\n"
            + rf"\@noteid{{7}}{{f}}{{n}}{{1}}{{6553600}}{{{y}}}" + "\n")


class TmpDirTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)


class TestSolverConvergence(TmpDirTestCase):
    """#1258: outfile must not request a rerun for a sub-sp correction."""

    def check(self, overlap):
        solver = MarginNotes(psize=600, top=580, bot=20)
        solver.pages = [[note(300), note(290 + overlap)]]
        solver.processpages()
        shifts = [abs(n.yshift) for n in solver.pages[0]]
        if overlap == ONE_SP:
            self.assertTrue(0 < max(shifts) <= ONE_SP)
        changed = solver.outfile(self.tmp / "notes.marginnotes")
        self.assertEqual(changed, overlap > ONE_SP,
                         f"residual shifts (sp): {[s / ONE_SP for s in shifts]}")

    def test_settled(self):
        self.check(0)

    def test_one_sp(self):
        self.check(ONE_SP)

    def test_substantial(self):
        self.check(2.0)


class TestFivePassCacheConvergence(TmpDirTestCase):
    """#1258: isolated cache jitter must settle before the five-pass limit.

    Real run_xetex and solver; only process execution is replaced. A single
    unconstrained note ensures the solver cannot itself ask for a rerun.
    """

    def check(self, ext, delta):
        tmp = self.tmp
        printer = SimpleNamespace(
            get=lambda key, default=0: default,
            incrementProgress=lambda **kw: None,
            editFile_delayed=lambda *a: None,
        )
        job = runjob.RunJob(printer, "", "", SimpleNamespace())
        job.tmpdir = str(tmp)
        job.maxRuns = 5
        job.silent = job.nopdf = True
        job.info = SimpleNamespace(printer=printer, getTextBlockSize=lambda: (600, 580, 20))
        # Seed the parlocs file with what pass 1 writes, so only the alternating
        # positions ever differ. Ask for the usual initial warm-up pass in the
        # log so both caches are loaded before alternating positions.
        (tmp / "jitter.parlocs").write_text(par_record(19660800))
        passes = []
        solver_changes = []
        real_tidy = runjob.tidymarginnotes

        def tidy(*args, **kwargs):
            changed = real_tidy(*args, **kwargs)
            solver_changes.append(changed)
            return changed

        def process(*args, **kwargs):
            offset = (len(passes) % 2) * delta
            passes.append(offset)
            (tmp / "jitter.log").write_text(
                ("PARLOC: Rerun.\n" if len(passes) == 1 else "")
                + "Output written on jitter.xdv (1 page).\n")
            (tmp / "jitter.parlocs").write_text(par_record(19660800 + (offset if ext == "parlocs" and delta == 1 else 0),
                           par_y=19660800 + (offset if ext == "parlocs" and delta > 1 else 0)))
            (tmp / "jitter.marginnotes").write_text(margin_record(19660800 + (offset if ext == "marginnotes" and delta == 1 else 0),
                              pnum=2 if ext == "marginnotes" and delta > 1 and offset else 1))
            return 0

        with mock.patch.object(runjob, "call", process), \
                mock.patch.object(runjob, "tidymarginnotes", tidy), \
                mock.patch.object(runjob.logger, "warning") as warning:
            job.run_xetex("jitter.tex", "jitter.pdf")
        self.assertEqual(job.res, 0)
        self.assertFalse(any(solver_changes), "cache comparison must be the only rerun source")
        if delta > 1:
            self.assertEqual(len(passes), 5)
            self.assertIn("chapter positions" if ext == "parlocs" else "margin note positions",
                          job.rerunReasons)
        else:
            self.assertEqual(len(passes), 2, f"{ext}: {len(passes)} passes, reasons={job.rerunReasons}")
        limit_warnings = [c for c in warning.call_args_list if "Rerun limit reached" in str(c.args[0])]
        self.assertEqual(len(limit_warnings), 1 if delta > 1 else 0)

    def test_identical_parlocs(self):
        self.check("parlocs", 0)

    def test_one_sp_parlocs(self):
        self.check("parlocs", 1)

    def test_substantial_parlocs(self):
        self.check("parlocs", 65536)

    def test_identical_marginnotes(self):
        self.check("marginnotes", 0)

    def test_one_sp_marginnotes(self):
        self.check("marginnotes", 1)

    def test_substantial_marginnotes(self):
        self.check("marginnotes", 65536)


class TestOutfile(TmpDirTestCase):
    def test_fixed_point(self):
        path = self.tmp / "notes.marginnotes"
        path.write_text(margin_record(19660800).replace("8.50000pt", "5.0pt")
                        .replace("0.00000pt}{1}", "48.856pt}{1}"))
        solver = MarginNotes(path, top=580, bot=20)
        solver.processpages()
        self.assertIs(solver.outfile(path), False)
        first = path.read_bytes()
        solver = MarginNotes(path, top=580, bot=20)
        solver.processpages()
        self.assertIs(solver.outfile(path), False)
        self.assertEqual(path.read_bytes(), first)

    def test_predicts_ypos(self):
        path = self.tmp / "notes.marginnotes"
        for shift_sp in (-7, -1, 0, 1, 7):
            with self.subTest(shift_sp=shift_sp):
                solver = MarginNotes()
                n = note(300)
                n.yoffset = 5
                n.yshift = shift_sp * ONE_SP
                solver.pages = [[n]]
                self.assertEqual(solver.outfile(path), shift_sp != 0)
                written = MarginNotes(path).pages[0][0]
                self.assertEqual(written.yoffset, 5 - shift_sp * ONE_SP)
                self.assertEqual(written.ypos, 300 + shift_sp * ONE_SP)


class TestCmpTexRecords(unittest.TestCase):
    cases = [
        ("", "", True),
        ("", par_record(0), False),
        (par_record(0), "", False),
        (par_record(0), par_record(0) + "extra\n", False),
        (par_record(0) + "extra\n", par_record(0), False),
        (par_record(0), par_record(65536), True),
        (par_record(0), par_record(0).replace("{6553600}{0}", "{6553601}{0}"), True),
        (par_record(0), par_record(0).replace("{7}", "{8}"), False),
        (par_record(0), par_record(0).replace("{7}{f}", "{7}{x}"), False),
        (par_record(0), par_record(0).replace("{n}{1}", "{n}{2}"), False),
        (par_record(0), par_record(0, par_y=19660801), False),
        (margin_record(0), margin_record(65536), True),
        (margin_record(0), margin_record(0, pnum=2), False),
        (margin_record(0), margin_record(0).replace("{8.50000pt}", "{8.50001pt}"), False),
        (r"\@noteid{7}{f}{n}{1}{0}{0}", r"\@noteid{7}{f}{n}{1}{0}", False),
        (r"\@noteid{7}{f}{n}{1}{0}{0}", r"\@other{7}{f}{n}{1}{0}{0}", False),
        (r"\@parnote{f}{GEN1.1}{1}{a}{0}{0}", r"\@parnote{f}{GEN1.1}{1}{a}{0}{1}", True),
        (r"\@parnote{f}{GEN1.1}{1}{a}{0}{0}", r"\@parnote{f}{GEN1.1}{1}{b}{0}{0}", False),
        (r"\@parpageend {0}{0}{bottomins}", r"\@parpageend {1}{1}{bottomins}", True),
        (r"\@parpageend {0}{0}{bottomins}", r"\@parpageend {0}{0}{notes}", False),
        ("comment a", "comment b", False),
    ]

    def test_cmptexrecords(self):
        for i, (before, after, equal) in enumerate(self.cases):
            with self.subTest(case=i, before=before, after=after):
                self.assertEqual(runjob.cmptexrecords(before, after, ignore=runjob.TEXIGNOREDFIELDS), equal)


if __name__ == "__main__":
    unittest.main()
