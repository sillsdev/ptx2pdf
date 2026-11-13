''' Checks PTXprint configurations across projects, without loading them into PTXprint, and
    offers repairs for what can be repaired safely.

    A Validator is given the folder the projects are in. validate() returns Findings. A Finding
    that can be repaired has a Fix; nothing is changed until Fix.apply() is called, and the
    callers (command line and window) only do that for the ones the user has agreed to.
'''

import os, re, glob, configparser, logging
from dataclasses import dataclass, field
from typing import Optional, Callable
from ptxprint.project import ProjectList

logger = logging.getLogger(__name__)

ERROR = "error"         # this will stop a print, or print the wrong thing
WARNING = "warning"     # probably not what is wanted
NOTE = "note"           # worth knowing

severityOrder = {ERROR: 0, WARNING: 1, NOTE: 2}


@dataclass
class Fix:
    description: str                # what will be changed, for the user to agree to
    action: Callable[[], None] = field(repr=False, default=None)
    safe: bool = True               # False: there is a choice in it, so it isn't ticked for them
    done: bool = False

    def apply(self):
        self.action()
        self.done = True


@dataclass
class Finding:
    project: str
    config: str
    severity: str
    code: str
    message: str
    fix: Optional[Fix] = None

    def __str__(self):
        return f"{self.project}/{self.config}: {self.severity}: {self.message}"


def readConfig(path):
    config = configparser.ConfigParser(interpolation=None, strict=False)
    with open(path, encoding="utf-8-sig", errors="ignore") as inf:
        config.read_file(inf)
    return config

def asBool(config, sect, opt, default=False):
    v = config.get(sect, opt, fallback=None)
    if v is None:
        return default
    return v.strip().lower() in ("true", "1", "yes", "on")

def setOptions(cfgpath, changes):
    ''' changes is a list of (section, option, value). Rewrites the ptxprint.cfg as PTXprint does. '''
    config = readConfig(cfgpath)
    for sect, opt, val in changes:
        if not config.has_section(sect):
            config.add_section(sect)
        config.set(sect, opt, val)
    with open(cfgpath, "w", encoding="utf-8") as outf:
        config.write(outf)


# settings that hold a file or folder, and whether the config actually uses it
pathSettings = {
    ("project", "selectscript"):     lambda c: asBool(c, "project", "processscript"),
    ("project", "frontincludes"):    lambda c: asBool(c, "project", "ifinclfrontpdf"),
    ("project", "backincludes"):     lambda c: asBool(c, "project", "ifinclbackpdf"),
    ("project", "modulefile"):       lambda c: c.get("project", "bookscope", fallback="") == "module",
    ("paper", "watermarkpdf"):       lambda c: asBool(c, "paper", "ifwatermark"),
    ("document", "customfigfolder"): lambda c: asBool(c, "document", "customfiglocn") and asBool(c, "document", "ifinclfigs"),
}

class Validator:

    def __init__(self, projectsDir, pdfAssets=None):
        self.projectsDir = os.path.normpath(projectsDir)
        self.prjTree = ProjectList()
        self.prjTree.addTreedir(self.projectsDir)
        self.projects = {p.prjid: p for p in self.prjTree.projects.values()
                         if os.path.normpath(os.path.dirname(p.path)) == self.projectsDir}
        self.pdfAssets = pdfAssets or os.path.join(os.path.dirname(os.path.dirname(__file__)), "PDFassets")

    # ---- what is there

    def projectsWithConfigs(self):
        ''' Returns {prjid: [config names]} for the projects that have any PTXprint configuration '''
        res = {}
        for prjid in sorted(self.projects, key=str.lower):
            cfgs = self.configNames(prjid)
            if len(cfgs):
                res[prjid] = cfgs
        return res

    def configDir(self, prjid, cfg):
        return os.path.join(self.projects[prjid].path, "shared", "ptxprint", cfg)

    def configNames(self, prjid):
        base = os.path.join(self.projects[prjid].path, "shared", "ptxprint")
        if not os.path.isdir(base):
            return []
        return sorted((d for d in os.listdir(base) if os.path.exists(os.path.join(base, d, "ptxprint.cfg"))), key=str.lower)

    def commonConfigs(self, prjids=None):
        ''' Returns [(config name, number of projects that have it)], the most widely used first '''
        counts = {}
        for prjid, cfgs in self.projectsWithConfigs().items():
            if prjids is not None and prjid not in prjids:
                continue
            for c in cfgs:
                counts[c] = counts.get(c, 0) + 1
        return sorted(counts.items(), key=lambda x: (-x[1], x[0].lower()))

    def hasBook(self, prjid, bk):
        path = self.projects[prjid].path
        # projects name their book files in different ways: 41MATaArp.SFM, 44JHNSGA.txt, MAT.usfm
        return any(bk.upper() in f.upper() and os.path.splitext(f)[1].lower() in (".sfm", ".txt", ".usfm", ".usx")
                   for f in os.listdir(path))

    def bookIsEmpty(self, prjid, bk):
        ''' Is the book there but with (almost) no text in its verses: a book that has been
            created in Paratext and not yet translated? A diglot can't be typeset against one. '''
        path = self.projects[prjid].path
        for f in os.listdir(path):
            if bk.upper() in f.upper() and os.path.splitext(f)[1].lower() in (".sfm", ".txt", ".usfm"):
                try:
                    with open(os.path.join(path, f), encoding="utf-8", errors="ignore") as inf:
                        text = inf.read()
                except OSError:
                    return False
                words = sum(len(m.split()) for m in re.findall(r"\\v \S+[ \t]*([^\\\n]*)", text))
                return words < 5
        return False

    def projectSettings(self, prjid, cfg=None):
        ''' The settings a project lays down for all its configs: {(section, option): value} '''
        res = {}
        files = [os.path.join(self.projects[prjid].path, "shared", "ptxprint", "ptxprint_project.cfg")]
        if cfg is not None:
            files.insert(0, os.path.join(self.configDir(prjid, cfg), "ptxprint_override.cfg"))
        for f in files:
            if not os.path.exists(f):
                continue
            try:
                config = readConfig(f)
            except configparser.Error:
                continue
            for s in config.sections():
                for o, v in config.items(s):
                    res[(s, o.strip("*"))] = v
        return res

    def expectedSecondary(self, prjid):
        ''' The project this one is normally printed beside in a diglot, if it says '''
        return self.projectSettings(prjid).get(("document", "diglotsecprj"), None) or None

    def resolvePath(self, val, prjid, cfg):
        ''' Returns the file a config's path value means '''
        v = val.strip()
        prjdir = self.projects[prjid].path
        for k, base in (("${prjdir}", prjdir), ("${settingsdir}", self.projectsDir), ("${pdfassets}", self.pdfAssets),
                        ("${workingdir}", os.path.join(prjdir, "local", "ptxprint", cfg))):
            if v.startswith(k):
                rest = v[len(k):].lstrip("/\\").replace("\\", "/")
                if re.match(r"^[A-Za-z]:/", rest):       # a whole path stuck on to a variable
                    return rest
                return os.path.normpath(os.path.join(base, rest))
        if os.path.isabs(v) or re.match(r"^[A-Za-z]:[\\/]", v):
            return os.path.normpath(v)
        return os.path.normpath(os.path.join(prjdir, v))

    # ---- checking

    def validate(self, prjids=None, configs=None):
        ''' Returns the Findings for these projects' configs (all of them, if not given) '''
        res = []
        for prjid, cfgs in self.projectsWithConfigs().items():
            if prjids is not None and prjid not in prjids:
                continue
            for cfg in cfgs:
                if configs is not None and cfg not in configs:
                    continue
                res.extend(self.validateConfig(prjid, cfg))
        res.sort(key=lambda f: (f.project.lower(), f.config.lower(), severityOrder[f.severity]))
        return res

    def validateConfig(self, prjid, cfg):
        res = []
        def add(severity, code, message, fix=None):
            res.append(Finding(prjid, cfg, severity, code, message, fix))
        cfgpath = os.path.join(self.configDir(prjid, cfg), "ptxprint.cfg")
        try:
            config = readConfig(cfgpath)
        except (configparser.Error, OSError) as e:
            add(ERROR, "unreadable", f"The configuration file can't be read: {e}")
            return res
        def fixTo(description, changes, safe=True):
            return Fix(description, lambda: setOptions(cfgpath, changes), safe=safe)

        self.checkIdentity(prjid, cfg, config, add, fixTo)
        isDiglot = asBool(config, "document", "ifdiglot")
        sides = {}
        if isDiglot:
            sides = self.checkDiglot(prjid, cfg, config, add, fixTo)
        self.checkBooks(prjid, cfg, config, sides, add)
        self.checkPaths(prjid, cfg, config, add, fixTo)
        self.checkVariables(prjid, cfg, config, add)
        self.checkCover(prjid, cfg, config, add)
        return res

    def checkIdentity(self, prjid, cfg, config, add, fixTo):
        v = config.get("project", "id", fallback=prjid)
        if v != prjid:
            add(NOTE, "projectId", f"The configuration says it belongs to project {v}.",
                fixTo(f"Record the project as {prjid}", [("project", "id", prjid)]))
        v = config.get("config", "name", fallback=cfg)
        if v != cfg:
            add(NOTE, "configName", f"The configuration says its name is {v}.",
                fixTo(f"Record the name as {cfg}", [("config", "name", cfg)]))

    def checkDiglot(self, prjid, cfg, config, add, fixTo):
        ''' Returns {side: (project, config)} '''
        sects = [s for s in config.sections() if s.startswith("diglot_")]
        if not len(sects):
            # an old-format diglot, or one of the other texts of a diglot that has the box ticked
            sec = config.get("document", "diglotsecprj", fallback=None)
            if sec:
                add(WARNING, "diglotOldFormat", f"This diglot (with {sec}) is in the format used before PTXprint 2.7. "
                    "Open it in PTXprint and save it to bring it up to date.")
            return {}
        sides = {s[7:]: (config.get(s, "projectid", fallback=""), config.get(s, "config", fallback=""),
                         config.get(s, "projectguid", fallback="")) for s in sects}
        me = self.projects[prjid]
        if "L" not in sides:
            add(ERROR, "diglotNoPrimary", "The diglot has no primary (L) text.")
        else:
            (lprj, lcfg, lguid) = sides["L"]
            if lprj != prjid or lguid != me.guid or lcfg != cfg:
                was = lprj if lprj != prjid else (lcfg if lcfg != cfg else "the wrong project ID")
                add(ERROR if lprj != prjid else NOTE, "diglotPrimary",
                    f"The diglot's primary (L) text is recorded as {was}; it must be {prjid}, {cfg}. "
                    "(This comes from copying the configuration from another project.)",
                    fixTo(f"Set the primary (L) text to {prjid}, {cfg}",
                          [("diglot_L", "projectid", prjid), ("diglot_L", "projectguid", me.guid), ("diglot_L", "config", cfg)]))
        if len(sides) < 2:
            add(ERROR, "diglotNoSecondary", "The diglot has no secondary (R) text.")
        expected = self.expectedSecondary(prjid)
        for k, (sprj, scfg, sguid) in sorted(sides.items()):
            if k == "L":
                continue
            sect = f"diglot_{k}"
            better = None
            if k == "R" and expected and expected != sprj and expected in self.projects:
                usecfg = scfg if scfg in self.configNames(expected) else (cfg if cfg in self.configNames(expected) else None)
                if usecfg is not None:
                    better = fixTo(f"Set the secondary (R) text to {expected}, {usecfg} (the project's own settings name {expected})",
                                   [(sect, "projectid", expected), (sect, "projectguid", self.projects[expected].guid),
                                    (sect, "config", usecfg)], safe=False)
            if sprj not in self.projects:
                add(ERROR, "diglotSecondaryMissing", f"The diglot's {k} text is project {sprj}, and there is no such project here.", better)
                continue
            if sprj == prjid:
                add(ERROR, "diglotSecondarySelf", f"The diglot's {k} text is this same project.", better)
                continue
            if scfg not in self.configNames(sprj):
                samecfg = cfg if cfg in self.configNames(sprj) else None
                add(ERROR, "diglotSecondaryConfig", f"The diglot's {k} text uses configuration {scfg} of {sprj}, which {sprj} doesn't have.",
                    fixTo(f"Use configuration {samecfg} of {sprj} for the {k} text", [(sect, "config", samecfg)], safe=False)
                    if samecfg else None)
            elif better is not None:
                add(WARNING, "diglotSecondaryUnexpected",
                    f"The diglot's {k} text is {sprj}, but this project's own settings say it goes with {expected}.", better)
            elif sguid != self.projects[sprj].guid:
                add(NOTE, "diglotSecondaryId", f"The project ID recorded for the {k} text ({sprj}) is out of date.",
                    fixTo(f"Update the project ID recorded for {sprj}", [(sect, "projectguid", self.projects[sprj].guid)]))
        layout = config.get("document", "diglotlayout", fallback="")
        letters = set(re.findall(r"[A-Z]", layout))
        if layout and letters != set(sides):
            add(ERROR, "diglotLayout", f"The diglot layout '{layout}' doesn't match its texts ({', '.join(sorted(sides))}).")
        return {k: (v[0], v[1]) for k, v in sides.items()}

    def selectedBooks(self, config):
        scope = config.get("project", "bookscope", fallback="single")
        if scope == "single":
            bks = [config.get("project", "book", fallback="")]
        elif scope == "multiple":
            bks = re.split(r"[\s,;]+", config.get("project", "booklist", fallback="").strip())
        else:
            bks = []
        return [b.upper() for b in bks if re.match(r"^[A-Za-z0-9]{3}$", b) and not b.isdigit()]

    def checkBooks(self, prjid, cfg, config, sides, add):
        serial = set(config.get("document", "diglotserialbooks", fallback="").split())
        for bk in self.selectedBooks(config):
            if bk in ("FRT", "INT", "BAK"):
                continue
            if not self.hasBook(prjid, bk):
                add(WARNING, "bookMissing", f"The book last chosen, {bk}, is not in this project.")
            for k, (sprj, scfg) in sides.items():
                if k == "L" or sprj not in self.projects or bk in serial:
                    continue
                if not self.hasBook(sprj, bk):
                    add(WARNING, "bookMissingSecondary", f"The book last chosen, {bk}, is not in the diglot's {k} project {sprj}.")
                elif self.bookIsEmpty(sprj, bk) and not self.bookIsEmpty(prjid, bk):
                    add(ERROR, "bookEmptySecondary", f"The book last chosen, {bk}, has no text yet in the diglot's {k} project {sprj} "
                        "(only verse numbers). A diglot can't be typeset with one side empty: the typesetting stops "
                        "with an error such as 'Missing number'.")

    def checkPaths(self, prjid, cfg, config, add, fixTo):
        prjdir = self.projects[prjid].path
        for (sect, opt), isUsed in pathSettings.items():
            val = config.get(sect, opt, fallback=None)
            if not val or val == "None" or not isUsed(config):
                continue
            for one in val.split("\n"):
                if not one.strip():
                    continue
                path = self.resolvePath(one, prjid, cfg)
                if os.path.exists(path):
                    continue
                fix = None
                name = os.path.basename(path.replace("\\", "/"))
                rest = one[len("${prjdir}/"):].replace("\\", "/") if one.startswith("${prjdir}/") else None
                if "\n" not in val:
                    # the same file in this project's own shared folder, or the file in another project
                    # that PTXprint 3.0-3.1.6 mis-saved as being inside this one
                    own = os.path.join(prjdir, "shared", name)
                    if os.path.isfile(own):
                        fix = fixTo(f"Use this project's own copy: shared/{name}", [(sect, opt, "${prjdir}/shared/" + name)])
                    elif rest and "/" in rest and os.path.isfile(os.path.join(self.projectsDir, rest)):
                        fix = fixTo(f"Use the file in the other project: {rest}", [(sect, opt, "${settingsdir}/" + rest)])
                what = {"selectscript": "The script", "frontincludes": "A PDF to include at the front",
                        "backincludes": "A PDF to include at the back", "modulefile": "The Bible module",
                        "watermarkpdf": "The watermark PDF", "customfigfolder": "The pictures folder"}[opt]
                onThisMachine = re.match(r"^[A-Za-z]:[\\/]", one) is not None
                add(WARNING if onThisMachine else ERROR, "pathMissing",
                    f"{what} was not found: {one}" + (" (a location on one particular computer)" if onThisMachine else ""), fix)

    def checkVariables(self, prjid, cfg, config, add):
        variables = dict(config.items("vars")) if config.has_section("vars") else {}
        for (s, o), v in self.projectSettings(prjid, cfg).items():
            if s == "vars":
                variables[o] = v
        frt = os.path.join(self.configDir(prjid, cfg), "FRTlocal.sfm")
        if not os.path.exists(frt):
            return
        with open(frt, encoding="utf-8", errors="ignore") as inf:
            text = "\n".join(l for l in inf.read().split("\n") if not l.lstrip().startswith("\\rem"))
        used = set(m.lower() for m in re.findall(r"\\zvar\s*\|\s*([^\\\s|]+?)\s*\\\*", text))
        used.update(m.lower() for m in re.findall(r'\bvar="([^"]+)"', text))
        used.discard("toctitle")
        undefined = sorted(v for v in used if v not in variables)
        if len(undefined):
            hint = ""
            if set(undefined) & {"maintitle", "subtitle"} and set(variables) & {"t1title", "t2title"}:
                hint = " This configuration has t1title and t2title instead, so those titles will print blank."
            add(WARNING, "variableUndefined", "The front matter uses variables this configuration doesn't have: "
                + ", ".join(undefined) + "." + hint)
        empty = sorted(v for v in used if v in variables and (not variables[v].strip() or "type value here" in variables[v].lower()))
        if len(empty):
            add(NOTE, "variableEmpty", "Variables used in the front matter have no value: " + ", ".join(empty) + ".")
        if re.match(r"^(0123456789|1234567890|0+)$", variables.get("isbn", "").replace("-", "")):
            add(WARNING, "isbnPlaceholder", f"The ISBN is a placeholder: {variables['isbn']}.")

    # ---- the texts of a diglot

    def diglotSides(self, prjid, cfg):
        ''' Returns {side: (project, config)} for a diglot or polyglot config, else {} '''
        try:
            config = readConfig(os.path.join(self.configDir(prjid, cfg), "ptxprint.cfg"))
        except (configparser.Error, OSError):
            return {}
        if not asBool(config, "document", "ifdiglot"):
            return {}
        return {s[7:]: (config.get(s, "projectid", fallback=""), config.get(s, "config", fallback=""))
                for s in config.sections() if s.startswith("diglot_")}

    def bestConfig(self, prjid, wanted):
        ''' The config of prjid to use beside another project's: the first of wanted that it has '''
        have = self.configNames(prjid)
        for w in wanted:
            if w in have:
                return w
        return "Default" if "Default" in have else (have[0] if len(have) else None)

    def setDiglotSide(self, prjid, cfg, side, newprj, newcfg):
        ''' Make another project and config the diglot's text on this side (not L: that is the project itself) '''
        if side == "L":
            raise ValueError("The primary (L) text is always the project itself")
        if newprj not in self.projects:
            raise ValueError(f"No such project: {newprj}")
        if newprj == prjid:
            raise ValueError("A diglot can't have the same project on both sides")
        if newcfg not in self.configNames(newprj):
            raise ValueError(f"{newprj} has no configuration {newcfg}")
        sect = f"diglot_{side}"
        setOptions(os.path.join(self.configDir(prjid, cfg), "ptxprint.cfg"),
                   [(sect, "projectid", newprj), (sect, "projectguid", self.projects[newprj].guid), (sect, "config", newcfg)])

    def checkCover(self, prjid, cfg, config, add):
        outdir = os.path.join(self.projects[prjid].path, "local", "ptxprint")
        if asBool(config, "cover", "makecoverpage") or not os.path.isdir(outdir):
            return
        stale = [f for f in os.listdir(outdir) if f.startswith(f"{prjid}_{cfg}_") and f.endswith("_cover.pdf")]
        if len(stale):
            def remove():
                for f in stale:
                    os.remove(os.path.join(outdir, f))
            add(WARNING, "coverStale", "Make Cover Page is off, but the preview will still show old cover file(s): " + ", ".join(stale),
                Fix("Delete the old cover file(s)", remove))
