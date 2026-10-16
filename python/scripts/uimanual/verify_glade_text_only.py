#!/usr/bin/env python3
r"""
Check that two versions of a glade file differ only in user-visible text.

Allowed differences: the text of tooltip-text / tooltip-markup / name / label / title /
placeholder-text properties and of combo <item>/list <col> entries, plus newly added
tooltip-text properties. Anything else (ids, classes, signals, other properties, structure)
is reported as an error.

Usage: python verify_glade_text_only.py original.glade edited.glade
"""

import sys
import xml.etree.ElementTree as et

textProps = {"tooltip-text", "tooltip-markup", "name", "label", "title", "placeholder-text"}


def walk(elem, path, out):
    """Flatten into a list of (path, tag, attrib, text) skipping added-tooltip comparison later."""
    out.append((path, elem.tag, dict(elem.attrib), (elem.text or "").strip(), elem))
    for i, c in enumerate(elem):
        walk(c, path + "/" + c.tag + (("#" + c.get("id")) if c.get("id") else "") +
             (("@" + c.get("name")) if c.get("name") else ""), out)


def main():
    a = et.parse(sys.argv[1]).getroot()
    b = et.parse(sys.argv[2]).getroot()
    la, lb = [], []
    walk(a, "", la)
    walk(b, "", lb)
    # drop tooltip properties that exist only in b (newly added)
    akeys = {(p, t, tuple(sorted(at.items()))) for p, t, at, _, _ in la}
    added = [x for x in lb if x[1] == "property" and x[2].get("name") == "tooltip-text"
             and (x[0], x[1], tuple(sorted(x[2].items()))) not in akeys]
    lb2 = [x for x in lb if x not in added]
    errors = 0
    changed = 0
    if len(la) != len(lb2):
        print(f"ERROR: element count differs: {len(la)} vs {len(lb2)} (+{len(added)} added tooltips)")
        errors += 1
    for x, y in zip(la, lb2):
        if (x[0], x[1], x[2]) != (y[0], y[1], y[2]):
            print(f"ERROR: structure differs at {x[0]} vs {y[0]}: {x[1]}{x[2]} / {y[1]}{y[2]}")
            errors += 1
            if errors > 20:
                break
            continue
        if x[3] != y[3]:
            ok = (x[1] == "property" and x[2].get("name") in textProps) or x[1] in ("item", "col")
            if not ok:
                print(f"ERROR: non-text value changed at {x[0]}: {x[3][:60]!r} -> {y[3][:60]!r}")
                errors += 1
            else:
                changed += 1
    print(f"{changed} text values changed, {len(added)} tooltips added, {errors} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
