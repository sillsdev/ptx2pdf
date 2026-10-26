#!/usr/bin/env python3
r"""
Apply reviewed tooltip/text edits from docs/uimanual/review/edits/*.json.

Each JSON file is a list of edits:
    {"file": "python/lib/ptxprint/ptxprint.glade",   # path relative to the repo root
     "widget": "c_fnOverride",                        # glade only: limit the search to this object
     "old": "exact text as it appears in the file",
     "new": "replacement text",
     "issue": "short reason"}

For a glade edit with a widget, "old" must occur exactly once inside that <object>. Otherwise
"old" must occur exactly once in the whole file. An edit whose "new" text is already present
(and "old" is gone) is treated as already applied. Glade files are checked to still parse.

Usage:
    python python/scripts/uimanual/apply_tooltip_edits.py [--dry-run] [files.json ...]
"""

import argparse
import glob
import json
import os
import re
import xml.etree.ElementTree as et


def objectSpan(text, wid):
    m = re.search(r'<object class="[^"]+" id="{}"'.format(re.escape(wid)), text)
    if not m:
        return None
    depth = 0
    for t in re.finditer(r"<object\b|</object>", text[m.start():]):
        if t.group(0) == "</object>":
            depth -= 1
            if depth == 0:
                return (m.start(), m.start() + t.end())
        else:
            depth += 1
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.abspath(os.path.join(here, "..", "..", ".."))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    files = args.files or sorted(glob.glob(os.path.join(repo, "docs", "uimanual", "review", "edits", "*.json")))
    cache = {}
    applied = skipped = failed = 0
    for jf in files:
        edits = json.load(open(jf, encoding="utf-8"))
        for e in edits:
            path = os.path.join(repo, e["file"])
            if path not in cache:
                cache[path] = open(path, encoding="utf-8", newline="").read()
            text = cache[path]
            start, end = 0, len(text)
            if e.get("widget") and path.endswith(".glade"):
                span = objectSpan(text, e["widget"])
                if span is None:
                    print(f"FAIL {os.path.basename(jf)}: widget {e['widget']} not found")
                    failed += 1
                    continue
                start, end = span
            block = text[start:end]
            if "\r\n" in text:      # match the file's line endings (edits are written with \n)
                e = dict(e, old=e["old"].replace("\r\n", "\n").replace("\n", "\r\n"),
                         new=e["new"].replace("\r\n", "\n").replace("\n", "\r\n"))
            n = block.count(e["old"])
            if e["old"] == e["new"]:
                print(f"FAIL {os.path.basename(jf)}: {e.get('widget') or e['file']}: edit changes nothing")
                failed += 1
            elif n == 1:
                block = block.replace(e["old"], e["new"])
                cache[path] = text[:start] + block + text[end:]
                applied += 1
            elif n == 0 and len(e["new"]) >= 20 and block.count(e["new"]) == 1:
                skipped += 1
            else:
                print(f"FAIL {os.path.basename(jf)}: {e.get('widget') or e['file']}: 'old' found {n} times: "
                      f"{e['old'][:70]!r}")
                failed += 1
    for path, text in cache.items():
        if path.endswith(".glade"):
            try:
                et.fromstring(text.encode("utf-8"))
            except et.ParseError as err:
                print(f"ERROR: {path} would no longer parse: {err}. Nothing written.")
                return 1
        elif path.endswith(".py"):
            try:
                compile(text, path, "exec")
            except SyntaxError as err:
                print(f"ERROR: {path} would no longer compile: {err}. Nothing written.")
                return 1
    if failed and not args.dry_run:
        print("Nothing written because some edits failed. Fix them and run again.")
        return 1
    if not args.dry_run:
        for path, text in cache.items():
            with open(path, "w", encoding="utf-8", newline="") as outf:
                outf.write(text)
    print(f"{'Would apply' if args.dry_run else 'Applied'} {applied}, already done {skipped}, failed {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
