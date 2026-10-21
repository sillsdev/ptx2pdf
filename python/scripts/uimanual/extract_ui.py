#!/usr/bin/env python3
r"""
Extract a structured map of the PTXprint user interface.

Reads (without importing GTK or running PTXprint):
    python/lib/ptxprint/ptxprint.glade   widgets, labels, tooltips, ranges, choices
    python/lib/ptxprint/gtkview.py       view levels, sensitivity rules, collapsible sections
    python/lib/ptxprint/modelmap.py      config keys for each widget
    python/lib/ptxprint/texpert.py       TeXpert (Advanced > Other) settings

Writes docs/uimanual/data/ui_map.json, which build_manual.py combines with the
hand-written (or AI-assisted) notes in docs/uimanual/content/ to produce the manual.

Usage:
    python python/scripts/uimanual/extract_ui.py [--repo C:/ptx2pdf] [-o out.json]
"""

import argparse
import ast
import json
import os
import re
import xml.etree.ElementTree as et
from collections import OrderedDict

# Interactive widget classes that a user can see and change/click
controlClasses = {
    "GtkCheckButton": "Checkbox",
    "GtkRadioButton": "Radio button",
    "GtkSpinButton": "Number box",
    "GtkScale": "Slider",
    "GtkEntry": "Text box",
    "GtkSearchEntry": "Search box",
    "GtkComboBox": "Drop-down list",
    "GtkComboBoxText": "Drop-down list",
    "GtkButton": "Button",
    "GtkToggleButton": "Toggle button",
    "GtkMenuButton": "Menu button",
    "GtkLinkButton": "Link",
    "GtkColorButton": "Colour picker",
    "GtkFontButton": "Font picker",
    "GtkFileChooserButton": "File picker",
    "GtkTextView": "Text area",
    "GtkTreeView": "Table",
    "GtkSwitch": "Switch",
}

dialogTitles = {
    "mainAppWindow": "Main window",
    "mainapp_win": "Main window",
    "menu_main": "Main menu (top-right ☰ button)",
    "pop_locateIssues": "PDF Preview > Issue types popup",
    "dlg_about": "About dialog",
}

stockLabels = {"gtk-ok": "OK", "gtk-cancel": "Cancel", "gtk-delete": "Delete", "gtk-about": "About",
               "gtk-help": "Help", "gtk-close": "Close", "gtk-apply": "Apply", "gtk-save": "Save",
               "gtk-open": "Open", "gtk-add": "Add", "gtk-remove": "Remove", "gtk-refresh": "Refresh"}


def cleanText(s):
    if s is None:
        return None
    s = re.sub(r"<[^>]+>", "", s)           # strip Pango markup
    s = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
    s = re.sub(r"\s*\n\s*", " ", s.strip())
    return s or None


def unwrapTooltip(s):
    """Tooltips are hard-wrapped for display. Re-flow paragraphs but keep lists and blank lines."""
    if s is None:
        return None
    if "<" in s:
        s = re.sub(r'<a href="([^"]*)">[^<]*</a>', r"\1", s)
        s = re.sub(r"<[^>]+>", "", s)
        s = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
    s = s.strip()
    paras = re.split(r"\n\s*\n", s)
    out = []
    for p in paras:
        lines = p.split("\n")
        merged = []
        for l in lines:
            ls = l.rstrip()
            if merged and ls and not re.match(r"^\s*([-*•\\]|\d+[.)]|[A-Za-z]{1,3}\s+[–-]\s)", ls) \
                    and not merged[-1].endswith(":") and not l.startswith("  "):
                merged[-1] = merged[-1] + " " + ls.strip()
            else:
                merged.append(ls if l.startswith("  ") else ls.strip())
        out.append("\n".join(merged))
    return "\n\n".join(out)


class Glade:
    def __init__(self, path):
        self.tree = et.parse(path)
        self.root = self.tree.getroot()
        self.parent = {c: p for p in self.root.iter() for c in p}
        self.byid = {o.get("id"): o for o in self.root.iter("object") if o.get("id")}

    @staticmethod
    def prop(o, name):
        for p in o.findall("property"):
            if p.get("name") == name:
                return p.text
        return None

    def objParent(self, o):
        """Nearest ancestor <object> element"""
        p = self.parent.get(o)
        while p is not None and p.tag != "object":
            p = self.parent.get(p)
        return p

    def childElem(self, o):
        """The <child> element wrapping o"""
        p = self.parent.get(o)
        return p if p is not None and p.tag == "child" else None

    def packing(self, o, name):
        c = self.childElem(o)
        if c is None:
            return None
        pk = c.find("packing")
        if pk is None:
            return None
        for p in pk.findall("property"):
            if p.get("name") == name:
                return p.text
        return None

    def ownLabel(self, o):
        """The text shown on/in this widget itself."""
        lab = self.prop(o, "label")
        if lab is not None:
            if lab in stockLabels:
                return stockLabels[lab]
            lab = lab.replace("_", "") if self.prop(o, "use-underline") == "True" else lab
            return cleanText(lab)
        # buttons often contain a GtkLabel or a box with a label
        for c in o.findall("child"):
            co = c.find("object")
            if co is None or c.get("type") == "label":
                continue
            if co.get("class") == "GtkLabel":
                return cleanText(self.prop(co, "label"))
            if co.get("class") in ("GtkBox", "GtkGrid"):
                for sub in co.iter("object"):
                    if sub.get("class") == "GtkLabel" and self.prop(sub, "label"):
                        return cleanText(self.prop(sub, "label"))
        return None

    def containerLabel(self, o):
        """Label for a frame or expander (may be a label widget or a checkbox)."""
        lab = self.prop(o, "label")
        if lab:
            return cleanText(lab.replace("_", "") if self.prop(o, "use-underline") == "True" else lab), None
        for c in o.findall("child"):
            if c.get("type") == "label":
                co = c.find("object")
                if co is not None:
                    return self.ownLabel(co) or cleanText(self.prop(co, "label")), co.get("id")
        return None, None

    def notebookTab(self, page):
        """Given a page object that is a direct child of a notebook, return its tab label."""
        nb = self.objParent(page)
        kids = nb.findall("child")
        for i, c in enumerate(kids):
            if c.find("object") is page:
                for c2 in kids[i + 1:]:
                    if c2.get("type") == "tab":
                        t = c2.find("object")
                        return (self.ownLabel(t) or cleanText(self.prop(t, "label"))), t.get("id")
                    if c2.get("type") is None:
                        break
        return None, None

    def adjacentLabel(self, o):
        """Find a GtkLabel that labels this widget: l_<suffix> convention, or the label to its left."""
        oid = o.get("id") or ""
        if "_" in oid:
            suffix = oid.split("_", 1)[1]
            for cand in ("l_" + suffix, "l_" + suffix[0].lower() + suffix[1:]):
                lo = self.byid.get(cand)
                if lo is not None and self.prop(lo, "label"):
                    return cleanText(self.prop(lo, "label")), cand
        par = self.objParent(o)
        if par is None:
            return None, None
        if par.get("class") == "GtkGrid":
            try:
                left = int(self.packing(o, "left-attach") or 0)
                top = int(self.packing(o, "top-attach") or 0)
            except ValueError:
                return None, None
            best = None
            for c in par.findall("child"):
                co = c.find("object")
                if co is None or co.get("class") != "GtkLabel" or not self.prop(co, "label"):
                    continue
                try:
                    cl = int(self.packing(co, "left-attach") or 0)
                    ct = int(self.packing(co, "top-attach") or 0)
                except ValueError:
                    continue
                if ct == top and cl < left and (best is None or cl > best[0]):
                    best = (cl, co)
            if best is not None:
                return cleanText(self.prop(best[1], "label")), best[1].get("id")
        elif par.get("class") in ("GtkBox", "GtkButtonBox"):
            prev = None
            for c in par.findall("child"):
                co = c.find("object")
                if co is o:
                    break
                if co is not None:
                    prev = co
            if prev is not None and prev.get("class") == "GtkLabel" and self.prop(prev, "label"):
                return cleanText(self.prop(prev, "label")), prev.get("id")
        return None, None

    def labelledControl(self, lab, classes):
        """The control that this GtkLabel labels: same grid row to the right, or next in a box."""
        lid = lab.get("id") or ""
        if lid.startswith("l_"):
            suffix = lid[2:]
            for pre in ("s_", "t_", "fcb_", "ecb_", "c_", "col_", "btn_"):
                for cand in (pre + suffix, pre + suffix[0].lower() + suffix[1:]):
                    if cand in self.byid and self.byid[cand].get("class") in classes:
                        return self.byid[cand]
        par = self.objParent(lab)
        if par is None:
            return None
        if par.get("class") == "GtkGrid":
            try:
                left = int(self.packing(lab, "left-attach") or 0)
                top = int(self.packing(lab, "top-attach") or 0)
            except ValueError:
                return None
            best = None
            for c in par.findall("child"):
                co = c.find("object")
                if co is None or co.get("class") not in classes:
                    continue
                try:
                    cl = int(self.packing(co, "left-attach") or 0)
                    ct = int(self.packing(co, "top-attach") or 0)
                except ValueError:
                    continue
                if ct == top and cl > left and (best is None or cl < best[0]):
                    best = (cl, co)
            if best is not None and best[0] == left + 1:
                return best[1]
        elif par.get("class") in ("GtkBox", "GtkButtonBox"):
            found = False
            for c in par.findall("child"):
                co = c.find("object")
                if co is lab:
                    found = True
                elif found and co is not None:
                    return co if co.get("class") in classes else None
        return None

    def breadcrumbs(self, o):
        """List of (text, id) from top-level down to (not including) o."""
        crumbs = []
        cur = o
        while True:
            par = self.objParent(cur)
            if par is None:
                # cur is top-level
                cid = cur.get("id")
                if cid in dialogTitles:
                    crumbs.append((dialogTitles[cid], cid))
                else:
                    title = cleanText(self.prop(cur, "title"))
                    if title:
                        title = re.sub(r"^PTXprint:\s*", "", title)
                        crumbs.append((title + " (dialog)", cid))
                    elif cid:
                        crumbs.append((cid, cid))
                break
            pc = par.get("class")
            if pc == "GtkNotebook":
                ce = self.childElem(cur)
                if ce is not None and ce.get("type") is None:
                    t, tid = self.notebookTab(cur)
                    if t:
                        crumbs.append((t + " tab", cur.get("id") or tid))
            elif pc in ("GtkFrame", "GtkExpander"):
                ce = self.childElem(cur)
                if ce is None or ce.get("type") != "label":
                    t, tid = self.containerLabel(par)
                    if t:
                        crumbs.append((t, par.get("id") or tid))
            cur = par
        crumbs.reverse()
        # The main window and its notebook are implied by the tab name
        if len(crumbs) > 1 and crumbs[0][1] in ("mainAppWindow", "mainapp_win"):
            crumbs = crumbs[1:]
        return crumbs

    def ancestorsIds(self, o):
        res = []
        cur = self.objParent(o)
        while cur is not None:
            if cur.get("id"):
                res.append(cur.get("id"))
            cur = self.objParent(cur)
        return res

    def choices(self, o):
        res = []
        items = o.find("items")
        if items is not None:
            for it in items.findall("item"):
                res.append({"id": it.get("id"), "text": cleanText(it.text)})
            return res
        model = self.prop(o, "model")
        if model and model in self.byid:
            store = self.byid[model]
            data = store.find("data")
            if data is not None:
                idcol = self.prop(o, "id-column")
                for row in data.findall("row"):
                    cols = {c.get("id"): c.text for c in row.findall("col")}
                    text = cleanText(cols.get("0"))
                    ident = cols.get(idcol) if idcol is not None else cols.get("1")
                    res.append({"id": ident, "text": text})
        return res

    def spinInfo(self, o):
        adj = self.prop(o, "adjustment")
        res = {}
        if adj and adj in self.byid:
            a = self.byid[adj]
            for k in ("lower", "upper", "step-increment", "value"):
                v = self.prop(a, k)
                if v is not None:
                    res[{"step-increment": "step", "value": "default"}.get(k, k)] = float(v)
        d = self.prop(o, "digits")
        if d is not None:
            res["digits"] = int(d)
        return res


# ---------- Python source helpers (no imports of ptxprint itself) ----------

class _Lit(ast.NodeTransformer):
    """Turn _("x") into "x", O(...) into dict, and anything non-literal into None."""
    def visit_Call(self, node):
        self.generic_visit(node)
        f = node.func
        if isinstance(f, ast.Name) and f.id == "_" and node.args:
            return node.args[0]
        if isinstance(f, ast.Attribute) and f.attr == "split" and isinstance(f.value, ast.Constant):
            return ast.List(elts=[ast.Constant(s) for s in f.value.value.split()], ctx=ast.Load())
        if isinstance(f, ast.Name) and f.id == "O":
            names = ["ident", "group", "val", "output", "name", "descr", "fn", "valfn", "method"]
            keys, vals = [], []
            for n, a in zip(names, node.args):
                keys.append(ast.Constant(n)); vals.append(a)
            for kw in node.keywords:
                keys.append(ast.Constant(kw.arg)); vals.append(kw.value)
            return ast.Dict(keys=keys, values=vals)
        return ast.Constant(None)

    def visit_Lambda(self, node):
        return ast.Constant(None)

    def visit_BinOp(self, node):
        self.generic_visit(node)
        try:
            return ast.Constant(ast.literal_eval(node))
        except Exception:
            return ast.Constant(None)


def moduleLiterals(path, names):
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    res = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            n = node.targets[0].id
            if n in names:
                v = _Lit().visit(node.value)
                ast.fix_missing_locations(v)
                try:
                    res[n] = ast.literal_eval(v)
                except Exception as e:
                    print(f"Could not evaluate {n} in {path}: {e}")
    return res


def readModelMap(path):
    """widget id -> list of config keys"""
    res = {}
    for m in re.finditer(r'^\s*"([^"]+)":\s*\("([^"]*)"\s*,\s*"([^"]*)"', open(path, encoding="utf-8").read(), re.M):
        key, widget, cat = m.groups()
        res.setdefault(widget, []).append({"key": key, "category": cat})
    return res


def readTeXpertGroups(path):
    src = open(path, encoding="utf-8").read()
    m = re.search(r"groupCats\s*=\s*\{(.*?)\}", src, re.S)
    res = {}
    if m:
        for k, v in re.findall(r"'(\w+)'\s*:\s*'([^']*)'", m.group(1)):
            res[k] = v
    return res


def flattenSens(d):
    """_sensitivities values may be nested dicts for radio groups: return controller -> [targets]."""
    res = {}
    for k, v in d.items():
        if isinstance(v, dict):
            for k2, v2 in v.items():
                res.setdefault(k2, []).extend(v2)
        else:
            res.setdefault(k, []).extend(v)
    return res


# ---------- main extraction ----------

levelNames = {2: "Mini", 4: "Basic", 5: "Regular", 6: "Full"}


def extract(repo):
    lib = os.path.join(repo, "python", "lib", "ptxprint")
    g = Glade(os.path.join(lib, "ptxprint.glade"))
    gv = moduleLiterals(os.path.join(lib, "gtkview.py"),
                        {"_ui_minimal", "_ui_basic", "_ui_regular", "_ui_full", "_ui_experimental",
                         "_ui_keepHidden", "_showActiveTabs", "_collapsibleSections", "_sensitivities",
                         "_nonsensitivities"})
    mm = readModelMap(os.path.join(lib, "modelmap.py"))
    tx = moduleLiterals(os.path.join(lib, "texpert.py"), {"texpertOptions"}).get("texpertOptions", {})
    txgroups = readTeXpertGroups(os.path.join(lib, "gtkview.py"))

    allPrefixes = ("bl", "btn", "bx", "c", "col", "ecb", "ex", "fcb", "fr", "gr", "l", "lb", "r", "s",
                   "scr", "t", "tb", "textv", "tv", "rule", "img")
    shown = {}
    cumulative = set()
    for lvl, name in ((2, "_ui_minimal"), (4, "_ui_basic"), (5, "_ui_regular"), (6, "_ui_full")):
        cumulative |= set(gv.get(name, []))
        shown[lvl] = set(cumulative)
    experimental = set(gv.get("_ui_experimental", []))
    keepHidden = set(gv.get("_ui_keepHidden", []))

    def isToggled(wid):
        return wid and "_" in wid and wid.split("_", 1)[0] in allPrefixes

    # notebook page id -> its tab label id (a page whose tab label is hidden can't be reached)
    tabLabelOf = {}
    for nb in g.root.iter("object"):
        if nb.get("class") == "GtkNotebook":
            for c in nb.findall("child"):
                po = c.find("object")
                if po is not None and c.get("type") is None and po.get("id"):
                    tabLabelOf[po.get("id")] = g.notebookTab(po)[1]

    def minLevel(o):
        ids = [o.get("id")] + g.ancestorsIds(o)
        ids += [tabLabelOf[i] for i in ids if tabLabelOf.get(i)]
        ids = [i for i in ids if isToggled(i)]
        if any(i in keepHidden for i in ids):
            return None, "hidden"
        if any(i in experimental for i in ids):
            return None, "experimental"
        for lvl in (2, 4, 5):
            if all(i in shown[lvl] for i in ids):
                return lvl, None
        return 6, None

    sens = flattenSens(gv.get("_sensitivities", {}))
    nonsens = flattenSens(gv.get("_nonsensitivities", {}))
    enabledBy, disabledBy = {}, {}
    for k, vs in sens.items():
        for v in vs:
            enabledBy.setdefault(v, []).append(k)
    for k, vs in nonsens.items():
        for v in vs:
            disabledBy.setdefault(v, []).append(k)
    tabsShownBy = {}
    for k, vs in gv.get("_showActiveTabs", {}).items():
        for v in vs:
            tabsShownBy.setdefault(v, []).append(k)
    collapsible = {}
    for fr, contents, chk, descr in gv.get("_collapsibleSections", []):
        collapsible[fr] = {"contents": contents, "checkbox": chk, "description": descr}
        collapsible[contents] = collapsible[fr]

    def inherited(o, table):
        """Rules applying to this widget or any of its ancestors"""
        res = []
        for i in [o.get("id")] + g.ancestorsIds(o):
            if i in table:
                res.extend(x for x in table[i] if x not in res)
        return res

    def describe(wid):
        o = g.byid.get(wid)
        if o is None:
            return {"id": wid}
        return {"id": wid, "label": g.ownLabel(o) or g.adjacentLabel(o)[0] or cleanText(g.prop(o, "name"))}

    # A GtkLabel with a tooltip that labels a control is merged into that control
    labelTips = {}          # control element -> tooltip of its label
    mergedLabels = set()
    for o in g.root.iter("object"):
        if o.get("class") != "GtkLabel" or (o.get("id") or "").startswith("lb_"):
            continue
        ltip = g.prop(o, "tooltip-text") or g.prop(o, "tooltip-markup")
        if not ltip:
            continue
        target = g.labelledControl(o, controlClasses)
        if target is not None:
            mergedLabels.add(o)
            labelTips.setdefault(target, ltip)

    controls = []
    seenIds = set()
    imageOwners = {g.prop(o, "image") for o in g.root.iter("object") if g.prop(o, "image")}
    for o in g.root.iter("object"):
        cls = o.get("class")
        wid = o.get("id")
        tip = g.prop(o, "tooltip-text") or g.prop(o, "tooltip-markup")
        if cls not in controlClasses and not tip:
            continue
        if cls not in controlClasses and (cls in ("GtkBox", "GtkGrid") or wid in imageOwners or g.objParent(o) is None):
            continue
        if cls not in controlClasses:
            # an image or label inside a button: its tooltip belongs to the button
            anc = g.objParent(o)
            while anc is not None and anc.get("class") not in controlClasses:
                anc = g.objParent(anc)
            if anc is not None:
                continue
        if cls in ("GtkEntry",) and not wid and not tip:
            continue        # internal entry of an editable combo box
        if not tip and g.prop(o, "image") in g.byid:
            im = g.byid[g.prop(o, "image")]
            tip = g.prop(im, "tooltip-text") or g.prop(im, "tooltip-markup")
        if not tip and cls in controlClasses:
            for sub in o.iter("object"):
                if sub is not o and sub.get("class") in ("GtkImage", "GtkLabel"):
                    tip = g.prop(sub, "tooltip-text") or g.prop(sub, "tooltip-markup")
                    if tip:
                        break
        if cls in ("GtkLabel",) and not tip and not (wid or "").startswith("lb_"):
            continue
        if o in mergedLabels:
            continue
        if o in labelTips:
            lt = labelTips[o]
            if not tip:
                tip = lt
            elif re.sub(r"\s+", " ", lt).strip() not in re.sub(r"\s+", " ", tip):
                tip = tip + "\n\n" + lt
        if cls in ("GtkTreeViewColumn", "GtkCellRendererText", "GtkCellRendererToggle"):
            continue
        if wid and wid in seenIds:
            continue
        if wid:
            seenIds.add(wid)
        own = g.ownLabel(o)
        adj, adjid = (None, None) if own and cls not in ("GtkSpinButton", "GtkEntry", "GtkComboBox", "GtkComboBoxText", "GtkScale")                         else g.adjacentLabel(o)
        readable = cleanText(g.prop(o, "name"))
        if readable and wid and readable == wid:
            readable = None
        crumbs = g.breadcrumbs(o)
        lvl, hidden = minLevel(o)
        rec = OrderedDict()
        rec["id"] = wid
        rec["type"] = controlClasses.get(cls, cls.replace("Gtk", ""))
        rec["gtkclass"] = cls
        rec["label"] = own
        rec["fieldLabel"] = adj if adj and adj != own else None
        rec["name"] = readable
        rec["breadcrumbs"] = [c[0] for c in crumbs]
        rec["breadcrumbIds"] = [c[1] for c in crumbs]
        rec["tooltip"] = unwrapTooltip(tip)
        rec["tooltipRaw"] = tip
        rec["viewLevel"] = lvl
        rec["viewLevelName"] = levelNames.get(lvl)
        rec["visibility"] = hidden
        if cls in ("GtkSpinButton", "GtkScale"):
            rec["range"] = g.spinInfo(o)
        if cls in ("GtkComboBox", "GtkComboBoxText"):
            rec["choices"] = g.choices(o)
            rec["editable"] = g.prop(o, "has-entry") == "True" or cls == "GtkComboBoxText" and (wid or "").startswith("ecb_")
        if cls in ("GtkCheckButton", "GtkRadioButton", "GtkToggleButton"):
            rec["defaultOn"] = g.prop(o, "active") == "True"
        if cls == "GtkRadioButton":
            rec["group"] = g.prop(o, "group") or wid
        if cls in ("GtkEntry",):
            rec["defaultText"] = g.prop(o, "text")
            rec["placeholder"] = g.prop(o, "placeholder-text")
        if cls == "GtkLinkButton":
            rec["uri"] = g.prop(o, "uri")
        mmkeys = [x["key"] for x in mm.get(wid, [])] if wid else []
        if not mmkeys and cls == "GtkRadioButton" and wid:
            m = re.match(r"^(r_.+)_([^_]+)$", wid)
            if m and m.group(1) in mm:
                mmkeys = [x["key"] + "=" + m.group(2) for x in mm[m.group(1)]]
        rec["configKeys"] = mmkeys
        rec["enabledBy"] = [describe(x) for x in inherited(o, enabledBy)]
        rec["disabledBy"] = [describe(x) for x in inherited(o, disabledBy)]
        rec["tabShownBy"] = [describe(x) for x in inherited(o, tabsShownBy)]
        coll = next((collapsible[i] for i in [wid] + g.ancestorsIds(o) if i in collapsible), None)
        if coll and coll["checkbox"] != wid:
            rec["collapsedUntil"] = describe(coll["checkbox"])
        rec["glade"] = True
        controls.append(rec)

    # Radio groups: record the group's label (the label of the first member's row)
    # TeXpert settings (Advanced > Other tab, built in code)
    texpertCrumbs = None
    gt = g.byid.get("gr_texoptions")
    if gt is not None:
        texpertCrumbs = [c[0] for c in g.breadcrumbs(gt)]
        texpertLevel = minLevel(gt)[0]
    for k, opt in tx.items():
        if not isinstance(opt, dict):
            continue
        val = opt.get("val")
        if isinstance(val, bool):
            pref, typ = "c_", "Checkbox"
        elif isinstance(val, (tuple, list)):
            pref, typ = "s_", "Number box"
        elif isinstance(val, dict):
            pref, typ = "fcb_", "Drop-down list"
        else:
            continue
        rec = OrderedDict()
        rec["id"] = pref + opt["ident"]
        rec["type"] = typ
        rec["gtkclass"] = None
        rec["label"] = opt.get("name")
        rec["fieldLabel"] = None
        rec["name"] = opt.get("name")
        rec["breadcrumbs"] = (texpertCrumbs or ["Advanced tab", "Other"]) + [txgroups.get(opt["group"], opt["group"])]
        rec["breadcrumbIds"] = [None] * len(rec["breadcrumbs"])
        rec["tooltip"] = opt.get("descr")
        rec["tooltipRaw"] = opt.get("descr")
        rec["viewLevel"] = texpertLevel if gt is not None else 6
        rec["viewLevelName"] = levelNames.get(rec["viewLevel"])
        rec["visibility"] = None
        if typ == "Number box":
            v = list(val) + [None] * 6
            rec["range"] = {"default": v[0], "lower": v[1], "upper": v[2], "step": v[3], "digits": v[5]}
        elif typ == "Drop-down list":
            rec["choices"] = [{"id": a, "text": b} for a, b in val.items()]
            rec["default"] = list(val.keys())[0]
        else:
            rec["defaultOn"] = val
        rec["configKeys"] = ["texpert/" + opt["ident"]]
        rec["texpertName"] = k
        rec["texpertGroup"] = opt["group"]
        rec["enabledBy"] = []
        rec["disabledBy"] = []
        rec["tabShownBy"] = []
        rec["glade"] = False
        controls.append(rec)

    # Containers (frames/expanders/tabs) so the manual can show the structure
    sections = []
    for o in g.root.iter("object"):
        cls = o.get("class")
        if cls in ("GtkFrame", "GtkExpander"):
            t, tid = g.containerLabel(o)
            if not t:
                continue
            crumbs = g.breadcrumbs(o)
            lvl, hidden = minLevel(o)
            sections.append({"id": o.get("id"), "labelWidget": tid, "title": t, "kind": cls[3:],
                             "breadcrumbs": [c[0] for c in crumbs], "viewLevel": lvl, "visibility": hidden,
                             "tooltip": unwrapTooltip(g.prop(o, "tooltip-text"))})

    tabs = []
    for nbid in ("nbk_Main", "nbk_fnxr", "nbk_PicList", "nbk_Advanced", "nbk_Viewer", "nbk_Import", "nbk_PDFviewer"):
        nb = g.byid.get(nbid)
        if nb is None:
            continue
        for c in nb.findall("child"):
            po = c.find("object")
            if po is None or c.get("type") == "tab":
                continue
            t, tid = g.notebookTab(po)
            if not t:
                continue
            lvl, hidden = minLevel(po)
            tl = g.byid.get(tid)
            tabs.append({"notebook": nbid, "id": po.get("id"), "tabLabelId": tid, "title": t,
                         "breadcrumbs": [x[0] for x in g.breadcrumbs(po)], "viewLevel": lvl, "visibility": hidden,
                         "shownBy": [describe(x) for x in tabsShownBy.get(po.get("id"), [])],
                         "tooltip": unwrapTooltip(g.prop(tl, "tooltip-text")) if tl is not None else None})

    dialogs = []
    for o in g.root.findall("object"):
        if o.get("class") in ("GtkDialog", "GtkMessageDialog", "GtkPopover", "GtkAboutDialog"):
            dialogs.append({"id": o.get("id"), "title": g.breadcrumbs(o)[0][0] if o.get("id") else None})

    return {
        "source": "ptxprint.glade + gtkview.py + modelmap.py + texpert.py",
        "viewLevels": [{"level": k, "name": v} for k, v in levelNames.items()],
        "tabs": tabs,
        "sections": sections,
        "dialogs": dialogs,
        "controls": controls,
    }


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.abspath(os.path.join(here, "..", "..", ".."))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=repo)
    ap.add_argument("-o", "--outfile", default=None)
    args = ap.parse_args()
    outfile = args.outfile or os.path.join(args.repo, "docs", "uimanual", "data", "ui_map.json")
    data = extract(args.repo)
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    with open(outfile, "w", encoding="utf-8") as outf:
        json.dump(data, outf, indent=1, ensure_ascii=False)
    n = len(data["controls"])
    tipped = sum(1 for c in data["controls"] if c["tooltip"])
    print(f"Wrote {outfile}: {n} controls ({tipped} with tooltips), {len(data['sections'])} sections, "
          f"{len(data['tabs'])} tabs, {len(data['dialogs'])} dialogs")


if __name__ == "__main__":
    main()
