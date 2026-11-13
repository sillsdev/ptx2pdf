''' Test prints: has PTXprint itself print a book with a project's configuration, as a separate
    program, and reports whether a PDF came out and, if not, why not. '''

import os, re, sys, time, subprocess, logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

PRINTED = "printed"
FAILED = "failed"
SKIPPED = "skipped"       # not tried: e.g. the project doesn't have the book
STOPPED = "stopped"

@dataclass
class PrintResult:
    project: str
    config: str
    books: str
    status: str
    seconds: float = 0.
    pdf: Optional[str] = None
    message: str = ""

    def __str__(self):
        return f"{self.project}/{self.config} {self.books}: {self.status}" + (f" ({self.message})" if self.message else "")


def ptxprintCommand():
    ''' Returns (the command that starts PTXprint, its environment) '''
    env = dict(os.environ)
    if getattr(sys, 'frozen', False):
        exe = os.path.join(os.path.dirname(sys.executable), "ptxprint.exe" if os.name == "nt" else "ptxprint")
        return [exe], env
    libdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env["PYTHONPATH"] = libdir + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    env["PYTHONIOENCODING"] = "utf-8"
    return [sys.executable, "-m", "ptxprint.main"], env

def texError(logfile):
    ''' The first error in a XeTeX log, in a line or two '''
    if not os.path.exists(logfile):
        return ""
    with open(logfile, encoding="utf-8", errors="ignore") as inf:
        lines = inf.read().split("\n")
    for i, l in enumerate(lines):
        if l.startswith("! "):
            where = next((x for x in lines[i+1:i+40] if re.match(r"^l\.\d+ ", x)), "")
            return (l[2:].strip() + ("  [at " + where.strip()[:80] + "]" if where else "")).strip()
    return ""

class TestPrinter:

    def __init__(self, validator, timeout=900):
        self.validator = validator
        self.timeout = timeout
        self.processes = set()
        self.stopping = False

    def booksIn(self, books):
        return [b.upper() for b in re.split(r"[\s,;]+", books.strip()) if re.match(r"^[A-Za-z0-9]{3}$", b)]

    def cannotPrint(self, prjid, cfg, books):
        ''' Why this can't be tried at all, or None '''
        bks = self.booksIn(books)
        if not len(bks):
            return "No book was given to print."
        missing = [b for b in bks if not self.validator.hasBook(prjid, b)]
        if len(missing):
            return f"{prjid} does not have {', '.join(missing)}."
        return None

    def run(self, prjid, cfg, books, pub=None):
        ''' Prints books (e.g. "3JN" or "JAS GLO"), or the config's publication pub with its own books
            and variables, and returns a PrintResult. Blocks until done. '''
        if pub is not None:
            books = pub
        else:
            why = self.cannotPrint(prjid, cfg, books)
            if why is not None:
                return PrintResult(prjid, cfg, books, SKIPPED, message=why)
        if self.stopping:
            return PrintResult(prjid, cfg, books, STOPPED)
        cmd, env = ptxprintCommand()
        # -S: run the config's script, as printing from PTXprint's window does
        # --readonly: a test must not change the configuration it tests
        cmd = cmd + ["-p", self.validator.projectsDir, "-q", "-S", "--readonly", "-l", "error", "--logfile=none",
                     "-c", cfg, "-P"] + (["-B", pub] if pub is not None else ["-b", " ".join(self.booksIn(books))]) + [prjid]
        start = time.time()
        try:
            proc = subprocess.Popen(cmd, cwd=self.validator.projectsDir, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except OSError as e:
            return PrintResult(prjid, cfg, books, FAILED, message=f"PTXprint could not be started: {e}")
        self.processes.add(proc)
        try:
            out, _ = proc.communicate(timeout=self.timeout)
            timedout = False
        except subprocess.TimeoutExpired:
            proc.kill()
            out, _ = proc.communicate()
            timedout = True
        finally:
            self.processes.discard(proc)
        seconds = time.time() - start
        out = out.decode("utf-8", errors="replace")
        if self.stopping:
            return PrintResult(prjid, cfg, books, STOPPED, seconds)
        pdf = None
        if pub is not None:
            pdf = os.path.join(self.validator.projects[prjid].path, "local", "ptxprint", f"{prjid}_{cfg}_{pub}_ptxp.pdf")
            if not os.path.exists(pdf):
                pdf = None
        for l in ([] if pub is not None else reversed(out.split("\n"))):
            l = l.strip()
            if l.lower().endswith("_ptxp.pdf") and os.path.exists(l):
                pdf = os.path.normpath(l)
                break
        if pdf is not None and os.path.getmtime(pdf) < start - 2:
            pdf = None          # an old one: nothing was made this time
        if proc.returncode == 0 and pdf is not None:
            return PrintResult(prjid, cfg, books, PRINTED, seconds, pdf)
        return PrintResult(prjid, cfg, books, FAILED, seconds, message=self.explain(prjid, cfg, out, timedout, start,
                                                   books=None if pub is not None else books))

    def explain(self, prjid, cfg, out, timedout, start, books=None):
        if timedout:
            return f"Took longer than {self.timeout // 60} minutes and was stopped."
        said = []
        for l in out.split("\n"):
            l = l.strip()
            if l.startswith("Status:"):
                said.append(l[7:].strip())
            elif l.startswith("Can't find publication") or l.startswith("No books to print"):
                said.append(l)
        logdir = os.path.join(self.validator.projects[prjid].path, "local", "ptxprint", cfg)
        tex = ""
        if os.path.isdir(logdir):
            # a publication is printed in a folder of its own inside this one
            logs = [os.path.join(d, f) for d, _, fs in os.walk(logdir) for f in fs
                    if f.startswith(f"{prjid}_{cfg}_") and f.endswith(".log")]
            logs = [f for f in logs if os.path.getmtime(f) >= start - 2]
            if len(logs):
                tex = texError(max(logs, key=os.path.getmtime))
        if tex:
            said.append("Typesetting error: " + tex)
            # the commonest cause of an error where a diglot's columns end: one side has nothing in it
            if "polyglotendcols" in tex:
                empty = [f"{b} in {sprj}" for k, (sprj, scfg) in self.validator.diglotSides(prjid, cfg).items()
                         if k != "L" and sprj in self.validator.projects
                         for b in self.booksIn(books or "") if self.validator.hasBook(sprj, b) and self.validator.bookIsEmpty(sprj, b)]
                if len(empty):
                    said.append("Probably because " + ", ".join(empty) + " has no text yet, only verse numbers.")
        if not len(said):
            lines = [l.strip() for l in out.split("\n") if l.strip() and "Warning" not in l]
            said = lines[-2:] if len(lines) else ["PTXprint gave no reason."]
        return "  ".join(dict.fromkeys(said))[:600]

    def stop(self):
        self.stopping = True
        for p in list(self.processes):
            try:
                p.kill()
            except OSError:
                pass
