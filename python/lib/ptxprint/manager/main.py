''' The multi-project management tool for PTXprint.

    With no command it opens its window. "validate" checks configurations from the command line:

        ptxprint-manager validate -c DiglotA5                 report only
        ptxprint-manager validate -c DiglotA5 --fix           ask about each repair
        ptxprint-manager validate -c DiglotA5 --fix --yes     make the safe repairs without asking

    "testprint" has PTXprint print a book with a configuration in every project that has it:

        ptxprint-manager testprint -c DiglotA5 -b 3JN

    "secondary" shows, or sets, the other project of diglot configurations:

        ptxprint-manager secondary -c DiglotA5
        ptxprint-manager secondary -c DiglotA5 -P bSum --to bG1BT
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

def doTestPrint(args):
    from concurrent.futures import ThreadPoolExecutor
    from ptxprint.manager.testprint import TestPrinter, PRINTED, FAILED
    validator = Validator(args.projects)
    prjids = splitList(args.project)
    configs = splitList(args.config)
    if configs is None:
        print("Say which configuration to print with: -c NAME")
        return 2
    have = validator.projectsWithConfigs()
    pairs = [(p, c) for p in have if prjids is None or p in prjids for c in have[p] if c in configs]
    if not len(pairs):
        print("No project has that configuration.")
        return 2
    printer = TestPrinter(validator, timeout=args.timeout)
    def one(pair):
        res = printer.run(pair[0], pair[1], args.books)
        print(f"{res.status.upper():8s}{res.project} / {res.config}  {res.seconds:.0f}s  {res.pdf or res.message}", flush=True)
        return res
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        results = list(pool.map(one, pairs))
    nfail = sum(1 for r in results if r.status == FAILED)
    print(f"\n{sum(1 for r in results if r.status == PRINTED)} printed, {nfail} failed, "
          f"{sum(1 for r in results if r.status not in (PRINTED, FAILED))} not tried.")
    return 1 if nfail else 0

def doSecondary(args):
    validator = Validator(args.projects)
    prjids = splitList(args.project)
    configs = splitList(args.config)
    have = validator.projectsWithConfigs()
    rc = 0
    for p in have:
        if prjids is not None and p not in prjids:
            continue
        for c in have[p]:
            if configs is not None and c not in configs:
                continue
            sides = validator.diglotSides(p, c)
            if args.side not in sides:
                continue
            if args.to is None:
                print(f"{p} / {c}: {args.side} is {sides[args.side][0]}, {sides[args.side][1]}")
                continue
            newcfg = args.toconfig or validator.bestConfig(args.to, [sides[args.side][1], c])
            try:
                validator.setDiglotSide(p, c, args.side, args.to, newcfg)
                print(f"{p} / {c}: {args.side} is now {args.to}, {newcfg}")
            except ValueError as e:
                print(f"{p} / {c}: not changed: {e}")
                rc = 1
    return rc

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
    tp = sub.add_parser("testprint", help="Have PTXprint print a book with a configuration in each project")
    tp.add_argument("-P", "--project", action="append", help="Project(s) to print [all that have the configuration]")
    tp.add_argument("-c", "--config", action="append", help="Configuration name(s) to print with")
    tp.add_argument("-b", "--books", default="3JN", help="Book(s) to print [3JN]")
    tp.add_argument("-j", "--jobs", type=int, default=3, help="How many to print at once [3]")
    tp.add_argument("--timeout", type=int, default=900, help="Give up on a print after this many seconds [900]")
    sec = sub.add_parser("secondary", help="Show, or with --to set, the other project of diglot configurations")
    sec.add_argument("-P", "--project", action="append", help="Project(s) [all]")
    sec.add_argument("-c", "--config", action="append", help="Configuration name(s) [all]")
    sec.add_argument("--side", default="R", help="Which text of the diglot [R]")
    sec.add_argument("--to", help="The project to use")
    sec.add_argument("--toconfig", help="Its configuration [the same name as before, if it has it]")
    args = parser.parse_args(argv)
    if args.projects is None:
        args.projects = defaultProjectsDir()
    if args.projects is None or not os.path.isdir(args.projects):
        print("Can't find the projects folder. Give it with -p.")
        return 2
    if args.command == "validate":
        return doValidate(args)
    elif args.command == "testprint":
        return doTestPrint(args)
    elif args.command == "secondary":
        if args.to is not None and splitList(args.project) is None:
            print("Say which project(s) to change: -P NAME")
            return 2
        return doSecondary(args)
    from ptxprint.manager.gtkmanager import runWindow
    return runWindow(args.projects)

if __name__ == "__main__":
    sys.exit(main())
