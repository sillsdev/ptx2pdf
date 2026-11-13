''' The multi-project management tool for PTXprint.

    With no command it opens its window. "validate" checks configurations from the command line:

        ptxprint-manager validate -c DiglotA5                 report only
        ptxprint-manager validate -c DiglotA5 --fix           ask about each repair
        ptxprint-manager validate -c DiglotA5 --fix --yes     make the safe repairs without asking
'''

import os, sys, argparse, configparser
from ptxprint.manager.validate import Validator, ERROR, WARNING, NOTE

def defaultProjectsDir():
    ''' The projects folder PTXprint itself last used '''
    pdir = os.getenv("PTXPRINT_PROJECTSDIR", None)
    if pdir is not None and os.path.isdir(pdir):
        return pdir
    try:
        from ptxprint.utils import appdirs
        conffile = os.path.join(appdirs.user_config_dir("ptxprint", "SIL"), "ptxprint_user.cfg")
        config = configparser.ConfigParser(interpolation=None)
        config.read(conffile, encoding="utf-8")
        pdir = config.get("init", "paratext", fallback=None)
        if pdir and os.path.isdir(pdir):
            return pdir
    except Exception:
        pass
    for p in (r"C:\My Paratext 9 Projects", r"C:\My Paratext 8 Projects", os.path.expanduser("~/Paratext8Projects")):
        if os.path.isdir(p):
            return p
    return None

def splitList(vals):
    res = []
    for v in vals or []:
        res.extend(x for x in v.replace(",", " ").split() if x)
    return res or None

def report(findings, out=None, notes=True):
    if out is None:
        out = sys.stdout
    last = None
    counts = {ERROR: 0, WARNING: 0, NOTE: 0}
    for f in findings:
        counts[f.severity] += 1
        if f.severity == NOTE and not notes:
            continue
        if (f.project, f.config) != last:
            last = (f.project, f.config)
            out.write(f"\n{f.project} / {f.config}\n")
        out.write(f"  {f.severity.upper():8s}{f.message}\n")
        if f.fix is not None:
            out.write(f"          can fix: {f.fix.description}{'' if f.fix.safe else '  (your choice: not done unless you say)'}\n")
    out.write(f"\n{counts[ERROR]} errors, {counts[WARNING]} warnings, {counts[NOTE]} notes; "
              f"{sum(1 for f in findings if f.fix is not None)} can be fixed here.\n")
    return counts

def doValidate(args):
    validator = Validator(args.projects)
    prjids = splitList(args.project)
    configs = splitList(args.config)
    unknown = [p for p in (prjids or []) if p not in validator.projects]
    if len(unknown):
        print("No such project: " + ", ".join(unknown))
        return 2
    findings = validator.validate(prjids, configs)
    counts = report(findings, notes=not args.quiet)
    fixable = [f for f in findings if f.fix is not None]
    if args.fix and len(fixable):
        print("")
        for f in fixable:
            if args.yes:
                doit = f.fix.safe
            else:
                ans = input(f"{f.project}/{f.config}: {f.fix.description}? [y/N] ").strip().lower()
                doit = ans in ("y", "yes")
            if doit:
                f.fix.apply()
                print(f"  fixed: {f.project}/{f.config}: {f.fix.description}")
        left = validator.validate(prjids, configs)
        print(f"\nAfter fixing: {sum(1 for f in left if f.severity == ERROR)} errors, "
              f"{sum(1 for f in left if f.severity == WARNING)} warnings.")
        return 1 if any(f.severity == ERROR for f in left) else 0
    return 1 if counts[ERROR] else 0

def main(argv=None):
    if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")      # titles in any script, on any console
    parser = argparse.ArgumentParser(prog="ptxprint-manager", description="Multi-project management tool for PTXprint")
    parser.add_argument("-p", "--projects", help="Folder the Paratext projects are in")
    sub = parser.add_subparsers(dest="command")
    val = sub.add_parser("validate", help="Check configurations across projects")
    val.add_argument("-P", "--project", action="append", help="Project(s) to check [all]")
    val.add_argument("-c", "--config", action="append", help="Configuration name(s) to check [all]")
    val.add_argument("--fix", action="store_true", help="Offer to repair what can be repaired")
    val.add_argument("--yes", action="store_true", help="With --fix: make the safe repairs without asking")
    val.add_argument("-q", "--quiet", action="store_true", help="Leave out the notes")
    args = parser.parse_args(argv)
    if args.projects is None:
        args.projects = defaultProjectsDir()
    if args.projects is None or not os.path.isdir(args.projects):
        print("Can't find the projects folder. Give it with -p.")
        return 2
    if args.command == "validate":
        return doValidate(args)
    from ptxprint.manager.gtkmanager import runWindow
    return runWindow(args.projects)

if __name__ == "__main__":
    sys.exit(main())
