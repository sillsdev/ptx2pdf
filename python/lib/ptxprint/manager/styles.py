r''' Compares styles between configurations: the same configuration in different projects, or
    different configurations of one project.

    What is compared is what prints. A style's value for an attribute comes from the last of
    these that gives one, which is the order TeX reads them in:
        the defaults (usfm_sb.sty, ptx2pdf.sty)
        the project's custom.sty            if the config uses it
        the config's ptxprint.sty           what PTXprint's Styles tab saves
        the config's ptxprint-mods.sty      if the config uses it
    Only attributes whose values differ between the configurations are reported, each with which
    of those files it came from.
'''

import os, re, sys, shutil, configparser
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional
from ptxprint.manager.validate import readConfig, asBool

DEFAULTS = "default"
COMMONEST = None            # compare with the value most of them have, not with one of them

# attributes that say what a style is, not how it looks
nonVisual = {"name", "description", "occursunder", "texttype", "styletype", "rank", "textproperties", "endmarker",
             "mrktype", "xmltag", "testylename", "colorname", "notrepeatable", "encoding", "attributes"}
onOffAttributes = {"bold", "italic", "superscript", "smallcaps", "subscript", "underline"}
listAttributes = {"occursunder", "textproperties"}
colourAttributes = {"color", "bordercolor", "borderfillcolor", "bgcolor", "bgimagecolor", "shadowcolor", "outlinecolor",
                    "bordercolour", "borderfillcolour", "bgcolour", "bgimagecolour", "shadowcolour", "outlinecolour"}

GROUPS = ["Text", "Headings", "Notes", "Introductions", "Cover", "Sidebars and categories"]

def styleGroup(marker):
    if "cover" in marker.lower():
        return "Cover"
    if marker.startswith("cat:") or marker in ("esb", "esbe"):
        return "Sidebars and categories"
    base = marker.split("|")[-1]
    if re.match(r"^(f|x|ef|ex|fe)([a-z]{0,3}\d?|SeeAlso.*)$", base) or base in ("fig", "zcaption"):
        return "Notes"
    if re.match(r"^(i[a-z]+\d?|toc\d?|ior)$", base) and base not in ("it",):
        return "Introductions"
    if re.match(r"^(mt|mte|ms|mr|s|sr|r|d|sp|sd|cl|cd|cp|h|rem|periph)\d?$", base):
        return "Headings"
    return "Text"

def defaultSheets():
    ''' The style sheets every configuration starts from '''
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # .../ptxprint
    dirs = [os.path.join(getattr(sys, "_MEIPASS", here), "ptx2pdf"), os.path.join(here, "ptx2pdf"),
            os.path.join(here, "..", "..", "..", "src"), "/usr/share/ptx2pdf/texmacros"]
    for d in dirs:
        if os.path.exists(os.path.join(d, "usfm_sb.sty")):
            return [os.path.join(d, f) for f in ("usfm_sb.sty", "ptx2pdf.sty") if os.path.exists(os.path.join(d, f))]
    return []

fieldRe = re.compile(r"^\s*\\(\S+)\s*(.*?)\s*$")

def parseSty(path):
    ''' Returns {marker: {attribute (lower case): value as written}} '''
    res = {}
    curr = None
    if not os.path.exists(path):
        return res
    with open(path, encoding="utf-8", errors="ignore") as inf:
        for l in inf:
            if l.lstrip().startswith("#"):
                continue
            m = fieldRe.match(l)
            if not m:
                continue
            key = m.group(1).lower()
            val = m.group(2)
            if key == "marker":
                curr = res.setdefault(val, {})
            elif curr is not None:
                if key not in ("name", "description"):
                    val = re.sub(r"\s+#.*$", "", val)       # a comment after the value
                curr[key] = val
    return res

# what a style has if nothing gives it the attribute
impliedValues = {"firstlineindent": "0", "leftmargin": "0", "rightmargin": "0", "spacebefore": "0", "spaceafter": "0",
                 "linespacing": "1", "raise": "0"}

def normalise(attr, val, paragraph=True):
    ''' A form of the value in which two ways of writing the same thing are the same.
        paragraph: for a paragraph style, bold that isn't given is bold that is off. (For a
        character style it is whatever the paragraph has, which is not the same as off.) '''
    if val is None:
        if attr in impliedValues:
            val = impliedValues[attr]
        elif attr in onOffAttributes and paragraph:
            return "off"
        else:
            return None
    v = val.strip()
    if attr in onOffAttributes:
        return "off" if v in ("-", "off", "false", "0") else ("on" if v == "" else v.lower())
    if attr in listAttributes:
        return " ".join(sorted(set(v.split())))
    if attr in colourAttributes:
        if re.match(r"^x[0-9A-Fa-f]{6}$", v):
            return v.lower()
        if re.match(r"^\d+$", v):               # Paratext's way: one number, blue green red
            n = int(v)
            return "x{:02x}{:02x}{:02x}".format(n & 0xFF, (n >> 8) & 0xFF, (n >> 16) & 0xFF)
        m = re.match(r"^([\d.]+)\s+([\d.]+)\s+([\d.]+)$", v)
        if m:                                   # three numbers from 0 to 1
            try:
                return "x" + "".join("{:02x}".format(min(255, round(float(x) * 255))) for x in m.groups())
            except ValueError:
                pass
        return v.lower()
    try:
        return "{:.3f}".format(float(v)).rstrip("0").rstrip(".")
    except ValueError:
        pass
    return v if attr in ("name", "description") else v.lower()

def display(attr, val):
    if val is None:
        return "(none)"
    if attr in onOffAttributes:
        n = normalise(attr, val)
        return {"on": "yes", "off": "no"}.get(n, val)
    return val if val != "" else "(empty)"


@dataclass
class StyleValue:
    raw: Optional[str]          # as written, or None if nothing gives the style this attribute
    source: str = DEFAULTS      # which file it came from

    def shown(self, attr):
        return display(attr, self.raw)


class StyleSheet:
    ''' The styles one configuration prints with '''

    def __init__(self, validator, prjid, cfg, defaults=None):
        self.prjid = prjid
        self.cfg = cfg
        prjdir = validator.projects[prjid].path
        cfgdir = validator.configDir(prjid, cfg)
        try:
            config = readConfig(os.path.join(cfgdir, "ptxprint.cfg"))
        except (configparser.Error, OSError):
            config = configparser.ConfigParser()
        self.layers = [(DEFAULTS, defaults if defaults is not None else loadDefaults())]
        if asBool(config, "project", "ifusecustomsty"):
            self.layers.append(("custom.sty", parseSty(os.path.join(prjdir, "custom.sty"))))
        self.layers.append(("ptxprint.sty", parseSty(os.path.join(cfgdir, "ptxprint.sty"))))
        if asBool(config, "project", "ifusemodssty"):
            self.layers.append(("ptxprint-mods.sty", parseSty(os.path.join(cfgdir, "ptxprint-mods.sty"))))

    def changedMarkers(self):
        ''' {marker: attributes} that something other than the defaults sets '''
        res = {}
        for label, sheet in self.layers[1:]:
            for m, attrs in sheet.items():
                res.setdefault(m, set()).update(attrs)
        return res

    def value(self, marker, attr):
        for label, sheet in reversed(self.layers):
            if attr in sheet.get(marker, {}):
                return StyleValue(sheet[marker][attr], label)
        return StyleValue(None)

_defaults = None
def loadDefaults():
    global _defaults
    if _defaults is None:
        _defaults = {}
        for f in defaultSheets():
            for m, attrs in parseSty(f).items():
                _defaults.setdefault(m, {}).update(attrs)
    return _defaults


def attributeName(attr):
    ''' The attribute as PTXprint writes it in a style sheet: fontsize -> FontSize '''
    try:
        from ptxprint.styleditor import mkrexceptions
    except ImportError:
        mkrexceptions = {}
    t = attr.lower().title()
    return mkrexceptions.get(t, t)

def backupSty(validator, prjid, cfg):
    ''' Keep the style sheet as it was, in the config's working folder (which is not shared) '''
    src = os.path.join(validator.configDir(prjid, cfg), "ptxprint.sty")
    if not os.path.exists(src):
        return None
    destdir = os.path.join(validator.projects[prjid].path, "local", "ptxprint", cfg)
    os.makedirs(destdir, exist_ok=True)
    dest = os.path.join(destdir, "ptxprint.sty.before-copy")
    shutil.copyfile(src, dest)
    return dest

def setStyValue(path, marker, attr, value):
    r''' Set (or with value None, remove) one attribute of one style in a style sheet, leaving the
        rest of the file as it is. Returns whether the file was changed. '''
    lines = []
    if os.path.exists(path):
        with open(path, encoding="utf-8", errors="ignore") as inf:
            lines = inf.read().split("\n")
    attr = attr.lower()
    newline = None if value is None else ("\\{} {}".format(attributeName(attr), value)).rstrip()
    start = end = None          # the lines of this style's (last) block: after its \Marker, up to the next
    found = []
    curr = None
    for i, l in enumerate(lines):
        m = fieldRe.match(l)
        if not m or l.lstrip().startswith("#"):
            continue
        key = m.group(1).lower()
        if key == "marker":
            if curr == marker:
                end = i
            curr = m.group(2)
            if curr == marker:
                start, end = i + 1, None
        elif curr == marker and key == attr:
            found.append(i)
    if start is not None and end is None:
        end = len(lines)
    old = list(lines)
    if len(found):
        if newline is None:
            for i in reversed(found):
                del lines[i]
        else:
            lines[found[-1]] = newline
            for i in reversed(found[:-1]):      # an earlier one that the last overrode
                del lines[i]
    elif newline is not None:
        if start is None:
            while len(lines) and not lines[-1].strip():
                lines.pop()
            lines.extend(["", "\\Marker " + marker, newline, ""])
        else:
            at = end
            while at > start and not lines[at - 1].strip():     # before the blank line that ends the block
                at -= 1
            lines.insert(at, newline)
    if lines == old:
        return False
    with open(path, "w", encoding="utf-8") as outf:
        outf.write("\n".join(lines))
    return True


@dataclass
class StyleDifference:
    marker: str
    attr: str
    values: dict                    # column label -> StyleValue
    baseline: StyleValue            # what it is compared with: the commonest, or the reference's
    differing: list = field(default_factory=list)       # the column labels that differ from the baseline

    @property
    def visual(self):
        return self.attr not in nonVisual

    @property
    def group(self):
        return styleGroup(self.marker)


class StyleComparison:

    def __init__(self, validator, columns):
        ''' columns: [(label, project, config)], e.g. the same config in several projects (labelled
            by project) or several configs of one project (labelled by config) '''
        self.validator = validator
        self.columns = [c[0] for c in columns]
        self.targets = {label: (prjid, cfg) for label, prjid, cfg in columns}
        defaults = loadDefaults()
        self.sheets = {label: StyleSheet(validator, prjid, cfg, defaults) for label, prjid, cfg in columns}

    @classmethod
    def acrossProjects(cls, validator, cfg, prjids):
        return cls(validator, [(p, p, cfg) for p in prjids if cfg in validator.configNames(p)])

    @classmethod
    def acrossConfigs(cls, validator, prjid, cfgs):
        have = validator.configNames(prjid)
        return cls(validator, [(c, prjid, c) for c in cfgs if c in have])

    def reload(self):
        defaults = loadDefaults()
        self.sheets = {label: StyleSheet(self.validator, prjid, cfg, defaults) for label, (prjid, cfg) in self.targets.items()}

    def copy(self, differences, columns=None):
        ''' Give the configurations that differ (or just these columns of them) the value they are
            compared with, by changing their ptxprint.sty and nothing else. Returns
            (how many values were changed, [why any could not be brought into line]). '''
        changed = 0
        problems = []
        backedUp = set()
        for d in differences:
            for col in d.differing:
                if columns is not None and col not in columns:
                    continue
                prjid, cfg = self.targets[col]
                sheet = self.sheets[col]
                paragraph = (sheet.value(d.marker, "styletype").raw or "").lower() not in ("character", "note")
                want = normalise(d.attr, d.baseline.raw, paragraph)
                path = os.path.join(self.validator.configDir(prjid, cfg), "ptxprint.sty")
                if path not in backedUp:
                    backupSty(self.validator, prjid, cfg)
                    backedUp.add(path)
                # what it would be without its own ptxprint.sty saying anything
                below = next((s[d.marker][d.attr] for label, s in reversed(sheet.layers)
                              if label in (DEFAULTS, "custom.sty") and d.attr in s.get(d.marker, {})), None)
                if normalise(d.attr, below, paragraph) == want:
                    setStyValue(path, d.marker, d.attr, None)           # so just stop it saying otherwise
                elif d.baseline.raw is not None:
                    setStyValue(path, d.marker, d.attr, d.baseline.raw)
                else:
                    problems.append(f"{col}: \\{d.marker} {d.attr} can't be set to nothing: "
                                    f"its {sheet.value(d.marker, d.attr).source} gives it a value")
                    continue
                changed += 1
        self.reload()
        # anything still out of line is being set by a file that is read after ptxprint.sty
        for d in differences:
            for col in d.differing:
                if columns is not None and col not in columns:
                    continue
                now = self.sheets[col].value(d.marker, d.attr)
                paragraph = (self.sheets[col].value(d.marker, "styletype").raw or "").lower() not in ("character", "note")
                if normalise(d.attr, now.raw, paragraph) != normalise(d.attr, d.baseline.raw, paragraph) \
                        and not any(p.startswith(f"{col}: \\{d.marker} {d.attr} ") for p in problems):
                    problems.append(f"{col}: \\{d.marker} {d.attr} is still {now.shown(d.attr)}, because its {now.source} sets it")
        return changed, problems

    def differences(self, reference=COMMONEST):
        ''' Returns the StyleDifferences: every attribute of every style that isn't the same in all of
            them, compared with the value most have, or with the reference column's '''
        cells = {}
        for sheet in self.sheets.values():
            for m, attrs in sheet.changedMarkers().items():
                cells.setdefault(m, set()).update(attrs)
        res = []
        for m in sorted(cells, key=str.lower):
            kinds = [(self.sheets[c].value(m, "styletype").raw or "").lower() for c in self.columns]
            paragraph = not any(k in ("character", "note") for k in kinds)
            for attr in sorted(cells[m]):
                vals = {c: self.sheets[c].value(m, attr) for c in self.columns}
                norm = {c: normalise(attr, v.raw, paragraph) for c, v in vals.items()}
                if len(set(norm.values())) < 2:
                    continue
                if reference is COMMONEST or reference not in vals:
                    common = Counter(norm.values()).most_common(1)[0][0]
                    basecol = next(c for c in self.columns if norm[c] == common)
                else:
                    basecol = reference
                res.append(StyleDifference(m, attr, vals, vals[basecol],
                                           [c for c in self.columns if norm[c] != norm[basecol]]))
        return res
