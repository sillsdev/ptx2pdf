#!/usr/bin/env python3
"""Observe the production loop for https://github.com/sillsdev/ptx2pdf/issues/1258.

Runs real XeTeX without injecting or editing coordinates. All wrappers only
record evidence; the production solver and loop make the rerun decisions.
"""
import argparse
from contextlib import redirect_stdout
from decimal import Decimal
import io
import json
import os
from pathlib import Path
import re
import shutil
from xml.sax.saxutils import escape
import subprocess
from types import SimpleNamespace
from unittest.mock import patch

from ptxprint import runjob
from ptxprint.marginnotes import SP, MarginNotes
from ptxprint.version import VersionStr

FIXTURE = Path(__file__).resolve().parent
REPO = FIXTURE.parents[2]
EXTS = ("parlocs", "marginnotes", "toc", "picpages", "log")
BLOCK = (210 * 2.8453, (210 - 15) * 2.8453, 15 * 2.8453)


def differences(before, after):
    """Report note coordinate deltas in sp and all other changed records."""
    a, b = before.splitlines(), after.splitlines()
    coords, offsets, other = [], [], []
    for index in range(max(len(a), len(b))):
        la = a[index] if index < len(a) else ""
        lb = b[index] if index < len(b) else ""
        if la == lb:
            continue
        marker = la.split("{", 1)[0]
        fields = {r"\@marginnote": (11, 12), r"\@noteid": (4, 5)}.get(marker)
        va, vb = re.findall(r"\{([^{}]*)\}", la), re.findall(r"\{([^{}]*)\}", lb)
        if (fields and lb.startswith(marker + "{") and len(va) == len(vb)
                and len(va) > max(fields)):
            for field in fields:
                if va[field] != vb[field]:
                    coords.append({"line": index + 1, "record": va[0], "field": field,
                                   "delta_sp": int(vb[field]) - int(va[field])})
            offset_fields = (8, 9) if marker == r"\@marginnote" else ()
            for field in offset_fields:
                delta = (Decimal(vb[field].removesuffix("pt"))
                         - Decimal(va[field].removesuffix("pt"))) * SP
                if delta:
                    offsets.append({"line": index + 1, "record": va[0], "field": field,
                                    "delta_sp": float(delta)})
            if all(x == y for i, (x, y) in enumerate(zip(va, vb))
                   if i not in fields + offset_fields):
                continue
        other.append({"line": index + 1, "before": la, "after": lb})
    return {"coordinates": coords, "offsets": offsets, "other_records": other}


def run_once(destination):
    # Refuse to overwrite evidence. A new directory guarantees a clean run.
    destination.mkdir(parents=True, exist_ok=False)
    for filename in ("test.tex", "test.sty", "test.usfm"):
        shutil.copy2(FIXTURE / filename, destination / filename)
    env = dict(os.environ)
    env["TEXINPUTS"] = os.pathsep.join([str(destination), str(REPO / "src"),
                                       str(REPO / "fonts"), env.get("TEXINPUTS", "")])
    # As in the Makefile: XeTeX finds the [Charis-*.ttf] files via TTFONTS.
    env["TTFONTS"] = os.pathsep.join([str(REPO / "fonts"), env.get("TTFONTS", "")])
    fontconfig = destination / "fonts.conf"
    fontconfig.write_text(
        '<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd">'
        '<fontconfig><include>/etc/fonts/fonts.conf</include><dir>'
        + escape(str(REPO / "fonts")) + '</dir></fontconfig>\n')
    env["FONTCONFIG_FILE"] = str(fontconfig)
    printer = SimpleNamespace(get=lambda key, default=0: default,
                              incrementProgress=lambda **kw: None,
                              editFile_delayed=lambda *a: None)
    job = runjob.RunJob(printer, "", str(REPO / "src"), SimpleNamespace())
    job.tmpdir = str(destination)
    job.env = env
    job.maxRuns = 5
    job.nopdf = job.silent = True
    job.info = SimpleNamespace(printer=printer, getTextBlockSize=lambda: BLOCK)
    passes = []
    console = io.StringIO()
    real_tidy = runjob.tidymarginnotes
    message_start = 0

    def snapshot(label):
        directory = destination / f"pass-{len(passes):02d}" / label
        directory.mkdir(parents=True, exist_ok=True)
        for ext in EXTS:
            source = destination / f"test.{ext}"
            if source.exists():
                shutil.copy2(source, directory / source.name)

    def finish_pass():
        nonlocal message_start
        if not passes:
            return
        snapshot("adjusted")
        passes[-1]["production_messages"] = console.getvalue()[message_start:].splitlines()
        passes[-1]["rerunReasons"] = list(job.rerunReasons)
        message_start = len(console.getvalue())

    def process(cmd, **kwargs):
        finish_pass()
        passes.append({"pass": len(passes) + 1})
        out = destination / f"pass-{len(passes):02d}"
        out.mkdir()
        with (out / "process.txt").open("w") as stream:
            kwargs["stdout"] = stream
            kwargs["stderr"] = subprocess.STDOUT
            result = subprocess.run(cmd, **kwargs)
        passes[-1]["tex_returncode"] = result.returncode
        snapshot("raw")
        return result

    def tidy(path, **kwargs):
        solver = MarginNotes(path, **kwargs)
        solver.processpages()
        passes[-1]["max_solver_shift_sp"] = max(
            (abs(n.yshift) * SP for page in solver.pages for n in page), default=0)
        changed = real_tidy(path, **kwargs)
        passes[-1]["solver_requested_rerun"] = changed
        return changed

    with patch.object(runjob, "call", process), patch.object(runjob, "tidymarginnotes", tidy):
        with redirect_stdout(console):
            job.run_xetex("test.tex", "test.pdf")
            finish_pass()
    (destination / "loop.txt").write_text(console.getvalue())
    for previous, current in zip(passes, passes[1:]):
        current["differences"] = {}
        for label in ("raw", "adjusted"):
            for ext in ("parlocs", "marginnotes"):
                paths = [destination / f"pass-{p['pass']:02d}" / label / f"test.{ext}"
                         for p in (previous, current)]
                texts = [p.read_text() if p.exists() else "" for p in paths]
                current["differences"][f"{label}.{ext}"] = differences(*texts)
    summary = {"ptxprint": VersionStr,
               "xetex": subprocess.check_output(["xetex", "--version"], text=True).splitlines()[0],
               "pass_count": len(passes), "returncode": job.res, "passes": passes}
    late = passes[2:]
    summary["rounding_jitter_reproduced"] = (
        job.res == 0 and len(passes) == 5 and all(
            p.get("solver_requested_rerun", False)
            and 0 < p["max_solver_shift_sp"] <= 1
            and p["differences"]["raw.parlocs"]["coordinates"]
            and all(not diff["other_records"] and all(
                abs(d["delta_sp"]) <= 1 for d in diff["coordinates"] + diff["offsets"])
                for diff in p["differences"].values())
            for p in late))
    (destination / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"{destination}: {len(passes)} passes, TeX return code {job.res}")
    for p in passes:
        diffs = p.get("differences", {}).get("raw.marginnotes", {})
        deltas = [d["delta_sp"] for d in diffs.get("coordinates", [])]
        print(f"  pass {p['pass']}: solver={p.get('max_solver_shift_sp', 0):.6g} sp, "
              f"solver rerun={p.get('solver_requested_rerun', False)}, raw note deltas={deltas}, reasons={p['production_messages'] or p['rerunReasons']}")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=FIXTURE / "converge")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--verify-reproduction", action="store_true",
                        help="fail unless every run exhibits <=1 sp jitter through pass five")
    parser.add_argument("--verify-convergence", action="store_true",
                        help="fail unless every run converges within three successful passes")
    args = parser.parse_args()
    if args.runs < 1:
        parser.error("--runs must be positive")
    summaries = [run_once(args.output.resolve() / f"run-{i:02d}")
                 for i in range(1, args.runs + 1)]
    if args.verify_reproduction and not all(s["rounding_jitter_reproduced"] for s in summaries):
        print("Expected rounding jitter was not reproduced; inspect summary.json.")
        return 1
    if args.verify_convergence and not all(
            s["returncode"] == 0 and 1 <= s["pass_count"] <= 3
            and all(p["tex_returncode"] == 0 for p in s["passes"])
            and not s["passes"][-1].get("solver_requested_rerun", False)
            and not s["passes"][-1]["rerunReasons"] for s in summaries):
        print("Expected convergence was not observed; inspect summary.json.")
        return 1
    return 1 if any(s["returncode"] for s in summaries) else 0


if __name__ == "__main__":
    raise SystemExit(main())
