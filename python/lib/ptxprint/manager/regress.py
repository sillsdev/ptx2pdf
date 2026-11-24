''' Regression tests, for PTXprint's developers. A test suite lists (project, configuration) pairs. Each is
    printed as a whole, as PTXprint's -P does, and the PDF compared with a "standard": a PDF from an earlier
    print that was looked at and found right, kept as <project>/local/ptxprint/<PRJ>_<CFG>_standard_ptxp.pdf.
    What differs is for a person to look at: if the change is right, the new PDF becomes the standard.

    The suite is a JSON file, <projects folder>/ptxprintTests.json unless another is given:

        {"version": 1,
         "settings": {"runs": 1, "diffPages": 10, "jobs": 4, "timeout": 3600, "program": "", "extraArgs": []},
         "entries": [{"project": "WSG", "config": "Short", "enabled": true, "extraArgs": [],
                      "standardVersion": "3.1.7", "note": ""}]}

    program "" is this copy of PTXprint; otherwise the path of an installed PTXprint.exe. The last result of
    each test is kept beside it (ptxprintTestResults.json), so that it can be looked at later.
    Nothing here uses GTK: the window (gtktesting.py) and the command line (main.py "regress") share it. '''

import os, re, json, time, shutil, threading, datetime, logging
from dataclasses import dataclass, field, fields, asdict
from typing import Optional
from ptxprint.manager.testprint import TestPrinter, ptxprintCommand, FAILED, STOPPED

logger = logging.getLogger(__name__)

SAME = "same"
DIFFERENT = "different"
NOSTANDARD = "nostandard"       # printed, but there is no standard to compare it with
NOCOMPARE = "nocompare"         # printed, but the comparison could not be made
ACCEPTED = "accepted"           # the new PDF was made the standard: as good as the same
NOTRUN = "notrun"               # no result yet
# FAILED and STOPPED are testprint's

statusLabels = {SAME: "Same", DIFFERENT: "DIFFERENT", NOSTANDARD: "No standard", NOCOMPARE: "Not compared",
                ACCEPTED: "Accepted", FAILED: "FAILED", STOPPED: "Stopped", NOTRUN: "Not run yet"}
# the results whose PDF can be made the standard
ACCEPTABLE = (DIFFERENT, NOSTANDARD, NOCOMPARE)

SUITENAME = "ptxprintTests.json"
DEFAULTSETTINGS = {"runs": 1, "diffPages": 10, "jobs": 4, "timeout": 3600, "program": "", "extraArgs": []}
INSTALLEDEXE = r"C:\Program Files\PTXprint\PTXprint.exe"
STANDARDSUFFIX = "_standard_ptxp.pdf"

# what PTXprint's comparison (pdf/pdfdiff.py createDiff) returns when it does not make a diff PDF
diffReasons = {"1": "PTXprint could not compare the PDFs: Poppler or the image libraries are not available.",
               "2": "PTXprint could not find the standard to compare with.",
               "3": "The pages are a different size from the standard's, so they could not be compared.",
               "5": "No pages could be compared."}

def standardName(prjid, cfg):
    return f"{prjid}_{cfg}{STANDARDSUFFIX}"

def writeJson(path, data):
    ''' Writes the file whole or not at all '''
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as outf:
        json.dump(data, outf, ensure_ascii=False, indent=1)
    os.replace(tmp, path)

def readJson(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as inf:
        res = json.load(inf)
    return res if isinstance(res, dict) else {}

def now():
    return datetime.datetime.now().isoformat(timespec="seconds")

def pageCount(pdf):
    ''' How many pages a PDF has, or None if it can't be read '''
    try:
        from ptxprint.pdfrw import PdfReader
        return len(PdfReader(pdf).pages)
    except Exception as e:
        logger.debug(f"Can't count the pages of {pdf}: {e}")
        return None

_versions = {}
def ptxprintVersion(program=""):
    ''' The version of PTXprint that program (or, if "", this copy) is, or "" if that can't be found '''
    if program in _versions:
        return _versions[program]
    res = ""
    if not program:
        from ptxprint.version import VersionStr
        res = VersionStr
    elif os.name == "nt":
        # the installer records it, with where it put PTXprint
        import winreg
        want = os.path.normcase(os.path.normpath(os.path.dirname(program)))
        for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            try:
                with winreg.OpenKey(hive, r"Software\Microsoft\Windows\CurrentVersion\Uninstall") as base:
                    for i in range(winreg.QueryInfoKey(base)[0]):
                        try:
                            with winreg.OpenKey(base, winreg.EnumKey(base, i)) as k:
                                where = winreg.QueryValueEx(k, "InstallLocation")[0]
                                if os.path.normcase(os.path.normpath(where)) == want:
                                    res = str(winreg.QueryValueEx(k, "DisplayVersion")[0])
                                    break
                        except OSError:
                            continue
            except OSError:
                continue
            if res:
                break
    _versions[program] = res
    return res


@dataclass
class TestEntry:
    project: str
    config: str
    enabled: bool = True
    extraArgs: list = field(default_factory=list)
    standardVersion: str = ""
    note: str = ""
    extra: dict = field(default_factory=dict)      # anything else in the file (from a later version): kept as it was

    @property
    def key(self):
        return (self.project, self.config)

    @classmethod
    def fromJson(cls, d):
        known = [f.name for f in fields(cls) if f.name != "extra"]
        return cls(**{k: d[k] for k in known if k in d}, extra={k: v for k, v in d.items() if k not in known})

    def toJson(self):
        res = dict(self.extra)
        res.update({k: v for k, v in asdict(self).items() if k != "extra"})
        return res


@dataclass
class TestResult:
    project: str
    config: str
    status: str
    seconds: float = 0.
    message: str = ""
    pdf: Optional[str] = None
    diff: Optional[str] = None
    when: str = ""
    version: str = ""
    pdfTime: float = 0.             # when pdf was written: so that it is known to be the one this result is about

    @property
    def key(self):
        return (self.project, self.config)

    @classmethod
    def fromJson(cls, d):
        return cls(**{f.name: d[f.name] for f in fields(cls) if f.name in d})

    def toJson(self):
        return asdict(self)

    def __str__(self):
        return f"{self.project}/{self.config}: {self.status}" + (f" ({self.message})" if self.message else "")


class TestSuite:

    def __init__(self, validator, path=None):
        self.validator = validator
        self.path = path or os.path.join(validator.projectsDir, SUITENAME)
        self.settings = dict(DEFAULTSETTINGS)
        self.entries = []
        self.extra = {}
        self.lock = threading.Lock()
        self.load()

    def load(self):
        data = readJson(self.path)
        self.settings = dict(DEFAULTSETTINGS)
        self.settings.update(data.get("settings", {}))
        self.entries = [TestEntry.fromJson(e) for e in data.get("entries", []) if "project" in e and "config" in e]
        self.extra = {k: v for k, v in data.items() if k not in ("version", "settings", "entries")}

    def save(self):
        with self.lock:
            data = dict(self.extra)
            data.update({"version": 1, "settings": self.settings, "entries": [e.toJson() for e in self.entries]})
            writeJson(self.path, data)

    def resultsPath(self):
        ''' Where the last results are kept: beside the suite '''
        base, ext = os.path.splitext(self.path)
        base = base[:-5] + "TestResults" if base.endswith("Tests") else base + "Results"
        return base + (ext or ".json")

    def find(self, prjid, cfg):
        return next((e for e in self.entries if e.key == (prjid, cfg)), None)

    def add(self, prjid, cfg):
        ''' Adds a test, unless it is there already. Returns the new entry, or None. Doesn't save. '''
        if self.find(prjid, cfg) is not None:
            return None
        e = TestEntry(prjid, cfg)
        self.entries.append(e)
        return e

    def remove(self, keys):
        ''' Takes the tests out of the suite (not their standards). Returns how many. Doesn't save. '''
        keys = set(keys)
        n = len(self.entries)
        self.entries = [e for e in self.entries if e.key not in keys]
        return n - len(self.entries)

    def enabled(self):
        return [e for e in self.entries if e.enabled]

    def projectPath(self, prjid):
        p = self.validator.projects.get(prjid)
        return p.path if p is not None else os.path.join(self.validator.projectsDir, prjid)

    def standardPath(self, prjid, cfg):
        return os.path.join(self.projectPath(prjid), "local", "ptxprint", standardName(prjid, cfg))

    def standardTime(self, prjid, cfg):
        ''' When the standard was made, or None if there isn't one '''
        p = self.standardPath(prjid, cfg)
        return os.path.getmtime(p) if os.path.exists(p) else None

    def findStandards(self, validator=None):
        ''' The (project, config) pairs that have a standard PDF but aren't in the suite '''
        validator = validator or self.validator
        res = []
        for prjid, cfgs in validator.projectsWithConfigs().items():
            outdir = os.path.join(validator.projects[prjid].path, "local", "ptxprint")
            if not os.path.isdir(outdir):
                continue
            have = set(os.listdir(outdir))
            for c in cfgs:
                if standardName(prjid, c) in have and self.find(prjid, c) is None:
                    res.append((prjid, c))
        return res

    def staleStandards(self, version):
        ''' Returns ({older version: how many standards were made with it}, how many don't say) '''
        old = {}
        unknown = 0
        for e in self.entries:
            if self.standardTime(*e.key) is None:
                continue
            if not e.standardVersion:
                unknown += 1
            elif e.standardVersion != version:
                old[e.standardVersion] = old.get(e.standardVersion, 0) + 1
        return old, unknown


class ResultStore:
    ''' The last result of each test, kept in a file so that it is still there next time '''

    def __init__(self, path):
        self.path = path
        self.results = {}
        self.lock = threading.Lock()
        try:
            data = readJson(path)
        except (OSError, ValueError) as e:
            logger.warning(f"Can't read the last results from {path}: {e}")
            data = {}
        for d in data.get("results", []):
            try:
                r = TestResult.fromJson(d)
            except TypeError:
                continue
            self.results[r.key] = r

    def get(self, prjid, cfg):
        return self.results.get((prjid, cfg))

    def record(self, res):
        with self.lock:
            self.results[res.key] = res
            try:
                writeJson(self.path, {"version": 1, "results": [r.toJson() for r in self.results.values()]})
            except OSError as e:
                logger.warning(f"Can't save the results in {self.path}: {e}")


def summarise(results):
    ''' e.g. "38 the same, 3 differ, 1 failed" '''
    n = {}
    for r in results:
        n[r.status] = n.get(r.status, 0) + 1
    parts = [(SAME, "the same"), (ACCEPTED, "accepted"), (DIFFERENT, "differ" if n.get(DIFFERENT, 0) != 1 else "differs"),
             (NOSTANDARD, "with no standard yet"), (NOCOMPARE, "not compared"), (FAILED, "failed"), (STOPPED, "stopped")]
    return ", ".join(f"{n[s]} {label}" for s, label in parts if n.get(s, 0)) or "Nothing was run"


class RegressionRunner(TestPrinter):
    ''' Runs the tests of a suite. Its methods block, and can be called from several threads at once,
        but never for the same (project, config) at the same time. '''

    def __init__(self, suite, results=None):
        super().__init__(suite.validator, timeout=int(suite.settings.get("timeout") or 3600))
        self.suite = suite
        self.results = results if results is not None else ResultStore(suite.resultsPath())
        self.running = set()
        self.runLock = threading.Lock()

    @property
    def program(self):
        return self.suite.settings.get("program") or ""

    def version(self):
        return ptxprintVersion(self.program)

    def command(self):
        if self.program:
            return [self.program], dict(os.environ)
        return ptxprintCommand()

    def cannotRun(self, prjid, cfg):
        if prjid not in self.validator.projects:
            return f"There is no project {prjid} in {self.validator.projectsDir}."
        if cfg not in self.validator.configNames(prjid):
            return f"{prjid} has no configuration {cfg}."
        if self.program and not os.path.exists(self.program):
            return f"Can't find {self.program}."
        return None

    def ptxprint(self, prjid, cfg, standard=None):
        ''' Prints the config as a whole, comparing it with standard if given. Returns (a TestResult that
            is final, or None; exit code, output, timed out?, start, new PDF) '''
        s = self.suite.settings
        entry = self.suite.find(prjid, cfg)
        cmd, env = self.command()
        # as the batch files that did this before: -S runs the config's script; no --readonly, so that the
        # PDFs are made as the existing standards were
        cmd = cmd + ["-p", self.validator.projectsDir, "-q", "-S", "-P", "-R", str(int(s.get("runs") or 1)), "-c", cfg]
        if standard is not None:
            cmd += ["-F", standard, "--diffpages", str(int(s.get("diffPages") or 0))]
        cmd += ["--logfile=none", "-l", "error"] + list(s.get("extraArgs") or []) \
               + list(entry.extraArgs if entry is not None else []) + [prjid]
        try:
            rc, out, timedout, start = self.execute(cmd, env)
        except OSError as e:
            return TestResult(prjid, cfg, FAILED, message=f"PTXprint could not be started: {e}"), None, "", False, 0, None
        if self.stopping:
            return TestResult(prjid, cfg, STOPPED, time.time() - start), None, "", False, start, None
        pdf = self.newPdf(out, start, skip=[standard] if standard else [])
        if pdf is None and not re.search(r"(?im)_ptxp\.pdf\s*$", out):
            # An installed PTXprint.exe (a windowed program) run from a console writes to that console,
            # not to us, so it can't say what it made. Look for it.
            pdf = self.pdfMadeSince(prjid, cfg, start)
        return None, rc, out, timedout, start, pdf

    def pdfMadeSince(self, prjid, cfg, start):
        ''' The newest <PRJ>_<CFG>_..._ptxp.pdf written since start, or None '''
        outdir = os.path.join(self.suite.projectPath(prjid), "local", "ptxprint")
        if not os.path.isdir(outdir):
            return None
        prefix = f"{prjid}_{cfg}_"
        # not those of another configuration whose name starts with this one's (e.g. Short_A5)
        others = [f"{prjid}_{c}_" for c in self.validator.configNames(prjid) if c != cfg and c.startswith(cfg + "_")]
        found = [os.path.join(outdir, f) for f in os.listdir(outdir) if f.startswith(prefix) and f.endswith("_ptxp.pdf")
                 and not f.endswith(STANDARDSUFFIX) and not any(f.startswith(o) for o in others)]
        found = [f for f in found if os.path.getmtime(f) >= start - 2]
        return max(found, key=os.path.getmtime) if len(found) else None

    def begin(self, prjid, cfg):
        ''' Returns a TestResult if the test can't be run now, else None (and it is marked as running) '''
        why = self.cannotRun(prjid, cfg)
        if why is not None:
            return TestResult(prjid, cfg, FAILED, message=why, when=now())
        if self.stopping:
            return TestResult(prjid, cfg, STOPPED, when=now())
        with self.runLock:
            if (prjid, cfg) in self.running:
                return TestResult(prjid, cfg, FAILED, message="It is already being printed.", when=now())
            self.running.add((prjid, cfg))
        return None

    def end(self, res, keep=True):
        with self.runLock:
            self.running.discard(res.key)
        res.when = res.when or now()
        res.version = res.version or self.version()
        if res.pdf and os.path.exists(res.pdf):
            res.pdfTime = os.path.getmtime(res.pdf)
        if keep and res.status != STOPPED:
            self.results.record(res)
        return res

    def run(self, prjid, cfg):
        ''' Prints and compares with the standard. Returns the TestResult, which is also kept. '''
        res = self.begin(prjid, cfg)
        if res is not None:
            return self.end(res, keep=res.status != STOPPED and "already" not in res.message)
        try:
            res = self.compare(prjid, cfg)
        except Exception as e:
            logger.exception(f"Testing {prjid}/{cfg}")
            res = TestResult(prjid, cfg, FAILED, message=f"Could not be tested: {e}")
        return self.end(res)

    def compare(self, prjid, cfg):
        standard = self.suite.standardPath(prjid, cfg)
        have = os.path.exists(standard)
        res, rc, out, timedout, start, pdf = self.ptxprint(prjid, cfg, standard if have else None)
        if res is not None:
            return res
        seconds = time.time() - start
        if timedout or pdf is None or rc not in (0, 5):
            return TestResult(prjid, cfg, FAILED, seconds, self.explain(prjid, cfg, out, timedout, start))
        if not have:
            return TestResult(prjid, cfg, NOSTANDARD, seconds, "There is no standard yet: look at the new PDF, "
                              "and accept it as the standard if it is right.", pdf)
        said = None
        for l in reversed(out.split("\n")):
            m = re.match(r"^diffresult=(.*)$", l.strip())
            if m:
                said = m.group(1).strip()
                break
        diff = pdf[:-4] + "_diff.pdf"
        fresh = os.path.exists(diff) and os.path.getmtime(diff) >= start - 2
        npdf, nstd = pageCount(pdf), pageCount(standard)
        pages = f"The new PDF has {npdf} pages, the standard {nstd}." if npdf is not None and nstd is not None \
                and npdf != nstd else ""
        if said is not None and said.lower().endswith("_diff.pdf"):
            return TestResult(prjid, cfg, DIFFERENT, seconds, pages, pdf, os.path.normpath(said))
        if said is None:
            # an older PTXprint, which doesn't say what the comparison found: only a diff PDF says something
            if fresh:
                return TestResult(prjid, cfg, DIFFERENT, seconds, pages, pdf, diff)
            if pages:
                return TestResult(prjid, cfg, DIFFERENT, seconds, pages, pdf)
            return TestResult(prjid, cfg, SAME, seconds, "No diff PDF was made, but this PTXprint doesn't say whether "
                              "the comparison was made, so that could not be confirmed.", pdf)
        if rc == 5 or said in diffReasons:
            return TestResult(prjid, cfg, NOCOMPARE, seconds, (diffReasons.get(said, diffReasons["2"]) + " " + pages).strip(), pdf)
        if said in ("0", "4"):
            if pages:       # only blank pages more or less: the comparison sees no difference, but there is one
                return TestResult(prjid, cfg, DIFFERENT, seconds, pages + " (The pages both have are the same.)", pdf)
            msg = "" if said == "0" else "No differences, but an old diff PDF is open and could not be removed."
            return TestResult(prjid, cfg, SAME, seconds, msg, pdf)
        return TestResult(prjid, cfg, NOCOMPARE, seconds, f"PTXprint's comparison said: {said}", pdf)

    def recreate(self, prjid, cfg):
        ''' Prints and makes the new PDF the standard (keeping the old one as .bak). Returns the TestResult. '''
        res = self.begin(prjid, cfg)
        if res is not None:
            return self.end(res, keep=False)
        try:
            res, rc, out, timedout, start, pdf = self.ptxprint(prjid, cfg)
            if res is None:
                seconds = time.time() - start
                if timedout or pdf is None or rc != 0:
                    res = TestResult(prjid, cfg, FAILED, seconds, "The standard was not changed. "
                                     + self.explain(prjid, cfg, out, timedout, start))
                else:
                    version = self.version()
                    self.makeStandard(prjid, cfg, pdf, version)
                    res = TestResult(prjid, cfg, ACCEPTED, seconds, "Printed again and made the standard.", pdf, version=version)
        except Exception as e:
            logger.exception(f"Recreating the standard of {prjid}/{cfg}")
            res = TestResult(prjid, cfg, FAILED, message=f"The standard could not be made: {e}")
        return self.end(res)

    def makeStandard(self, prjid, cfg, pdf, version):
        standard = self.suite.standardPath(prjid, cfg)
        os.makedirs(os.path.dirname(standard), exist_ok=True)
        if os.path.exists(standard):
            os.replace(standard, standard + ".bak")         # one generation back
        shutil.copyfile(pdf, standard)
        entry = self.suite.find(prjid, cfg) or self.suite.add(prjid, cfg)
        entry.standardVersion = version
        self.suite.save()

    def canAccept(self, prjid, cfg):
        ''' Why the last result's PDF can't be made the standard, or None '''
        res = self.results.get(prjid, cfg)
        if res is None or res.status not in ACCEPTABLE or not res.pdf:
            return "There is no new PDF that differs from the standard."
        if not os.path.exists(res.pdf):
            return f"{os.path.basename(res.pdf)} is not there any more."
        if res.pdfTime and abs(os.path.getmtime(res.pdf) - res.pdfTime) > 1:
            return f"{os.path.basename(res.pdf)} has been printed again since: run the test again."
        with self.runLock:
            if (prjid, cfg) in self.running:
                return "It is being printed."
        return None

    def accept(self, prjid, cfg):
        ''' Makes the PDF of the last result the standard, without printing again. Returns the new
            TestResult; raises ValueError if it can't be done. '''
        why = self.canAccept(prjid, cfg)
        if why is not None:
            raise ValueError(why)
        old = self.results.get(prjid, cfg)
        self.makeStandard(prjid, cfg, old.pdf, old.version)
        res = TestResult(prjid, cfg, ACCEPTED, old.seconds, "Accepted as the standard.", old.pdf, when=now(),
                         version=old.version, pdfTime=old.pdfTime)
        self.results.record(res)
        return res
