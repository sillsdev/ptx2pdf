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

    For PTXprint's developers, --testing (not shown by --help) adds two tabs to the window, "Regression
    tests" and "Test suite", and the "regress" command. They replace PrintALLProjects.bat and
    RecreateALLstandards.bat: each test prints a project's configuration as a whole and compares the PDF
    with <project>/local/ptxprint/<PRJ>_<CFG>_standard_ptxp.pdf, a PDF that was checked and found right.

        ptxprint-manager --testing                              the window, with the testing tabs
        ptxprint-manager --testing regress --find               add the standards already there to the suite
        ptxprint-manager --testing regress                      run every test; exit code 1 if any differs or fails
        ptxprint-manager --testing regress -c Short -P WSG -j 2 run some of them, two at once
        ptxprint-manager --testing regress --list               the tests and their last results
        ptxprint-manager --testing regress -c Short --accept    make the PDFs that differed the standards
        ptxprint-manager --testing regress -c Short --recreate  print again and make the new PDFs the standards
        ptxprint-manager --testing regress -c Short -P WSG --add       add tests (--remove takes them out)

    The suite is <projects folder>/ptxprintTests.json (or --suite FILE); the last results are kept beside it,
    in ptxprintTestResults.json. Its settings say which PTXprint prints ("program": "" for this one, or the
    path of an installed PTXprint.exe), the XeTeX runs (-R), how many pages of differences to show, how
    many to run at once and the timeout in seconds; each test can have extra PTXprint arguments. Results:
        SAME         the comparison was made and found nothing
        DIFFERENT    look at the diff PDF; if the change is right, accept the new PDF as the standard
        NOSTANDARD   printed, but there is no standard yet: the new PDF can be accepted as the first
        NOCOMPARE    printed, but PTXprint could not compare (e.g. the pages are a different size)
        FAILED       no PDF, with the reason
    A standard that is replaced is kept as <standard>.bak (one generation). PTXprint prints "diffresult=..."
    on the command line, so that an identical PDF is told apart from a comparison that wasn't made; an older
    PTXprint that doesn't is judged by its diff PDF alone, and the result says so.
'''

import os, sys, time, argparse, configparser
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

def chosenPairs(validator, args):
    prjids = splitList(args.project)
    configs = splitList(args.config)
    have = validator.projectsWithConfigs()
    return [(p, c) for p in have if prjids is None or p in prjids for c in have[p] if configs is None or c in configs]

def doPublications(args):
    from ptxprint.manager.publications import PublicationTable, MAIN
    validator = Validator(args.projects)
    table = PublicationTable(validator, chosenPairs(validator, args))
    cols = table.columns()
    for (prjid, cfg, pubid) in table.rows():
        c = table.configs[(prjid, cfg)]
        if pubid == MAIN:
            print(f"\n{prjid} / {cfg}   (book last chosen: {c.books})")
        vals = "; ".join(f"{k} = {c.value(pubid, k)}" for k in cols if c.value(pubid, k).strip())
        print(f"  {'main variables' if pubid == MAIN else pubid + ' [' + c.booksOf(pubid) + ']'}: {vals}")
    return 0

def doCompare(args):
    from ptxprint.manager.compare import Comparison, NOTSET
    validator = Validator(args.projects)
    configs = splitList(args.config)
    if configs is None or len(configs) != 1 or args.ref is None:
        print("Give one configuration and the project to compare with: -c NAME --ref PROJECT")
        return 2
    if args.ref not in validator.projects or configs[0] not in validator.configNames(args.ref):
        print(f"{args.ref} has no configuration {configs[0]}")
        return 2
    comparison = Comparison(validator, configs[0], args.ref)
    diffs = comparison.differences([p for p, c in chosenPairs(validator, args)])
    if not args.all:
        diffs = [d for d in diffs if not d.oneSided]
    wanted = set(args.copy or [])
    show = lambda v: "(not set)" if v is NOTSET else v
    for d in diffs:
        print(f"{d.setting:38s} {d.project:10s} {show(d.value)}   ({args.ref}: {show(d.refValue)})")
    print(f"\n{len(diffs)} differences from {args.ref} in {len(set(d.project for d in diffs))} projects.")
    if len(wanted):
        todo = [d for d in diffs if d.setting in wanted]
        if not len(todo):
            print("None of those settings differ.")
        elif args.yes or input(f"Copy {len(todo)} settings from {args.ref}? [y/N] ").strip().lower() in ("y", "yes"):
            print(f"Copied {comparison.copy(todo)} settings.")
    return 0

def doStyles(args):
    from ptxprint.manager.styles import StyleComparison, COMMONEST
    validator = Validator(args.projects)
    configs = splitList(args.config)
    if args.within is not None:
        if args.within not in validator.projects or configs is None or len(configs) < 2:
            print("Give the project and at least two of its configurations: --within PROJECT -c A -c B")
            return 2
        comp = StyleComparison.acrossConfigs(validator, args.within, configs)
    else:
        if configs is None or len(configs) != 1:
            print("Give one configuration to compare across projects: -c NAME")
            return 2
        prjids = splitList(args.project) or list(validator.projectsWithConfigs())
        comp = StyleComparison.acrossProjects(validator, configs[0], prjids)
    if len(comp.columns) < 2:
        print("There need to be at least two to compare.")
        return 2
    if args.ref is not None and args.ref not in comp.columns:
        print(f"{args.ref} is not one of those being compared: {', '.join(comp.columns)}")
        return 2
    diffs = [d for d in comp.differences(reference=args.ref or COMMONEST) if args.all or d.visual]
    if args.strays:
        diffs = [d for d in diffs if len(d.differing) <= 2]
    base = f"{args.ref} has" if args.ref else "most have"
    for d in diffs:
        others = ";  ".join(f"{c}: {d.values[c].shown(d.attr)} [{d.values[c].source}]" for c in d.differing)
        print(f"\\{d.marker:24s} {d.attr:18s} {base} {d.baseline.shown(d.attr)}  |  {others}")
    print(f"\n{len(diffs)} style attributes differ, in {len(set(d.marker for d in diffs))} styles.")
    return 0

def resultLine(res):
    from ptxprint.manager.regress import statusLabels
    return f"{statusLabels.get(res.status, res.status).upper():14s}{res.project} / {res.config}  {res.seconds:.0f}s  " \
           f"{res.message or ''}{'  ' if res.message else ''}{res.diff or res.pdf or ''}"

def doRegress(args):
    from concurrent.futures import ThreadPoolExecutor
    from ptxprint.manager.regress import TestSuite, RegressionRunner, summarise, statusLabels, SAME, ACCEPTED, NOTRUN
    validator = Validator(args.projects)
    suite = TestSuite(validator, args.suite)
    prjids = splitList(args.project)
    configs = splitList(args.config)
    def chosen(e):
        return (prjids is None or e.project in prjids) and (configs is None or e.config in configs)
    if args.find:
        found = suite.findStandards()
        for p, c in found:
            suite.add(p, c)
        if len(found):
            suite.save()
        print(f"Added {len(found)} tests that have a standard already; the suite ({suite.path}) has {len(suite.entries)}.")
        return 0
    if args.add:
        if configs is None:
            print("Say which configuration(s) to add: -c NAME")
            return 2
        added = [suite.add(p, c) for p, c in chosenPairs(validator, args)]
        n = sum(1 for e in added if e is not None)
        if n:
            suite.save()
        print(f"Added {n} tests ({len(added) - n} were there already).")
        return 0
    if args.remove:
        if prjids is None and configs is None:
            print("Say which tests to take out: -c NAME and/or -P PROJECT")
            return 2
        n = suite.remove([e.key for e in suite.entries if chosen(e)])
        if n:
            suite.save()
        print(f"Took {n} tests out of the suite. Their standard PDFs are left as they are.")
        return 0
    runner = RegressionRunner(suite)
    if args.list:
        for e in suite.entries:
            if not chosen(e):
                continue
            res = runner.results.get(*e.key)
            made = suite.standardTime(*e.key)
            std = "none yet" if made is None else time.strftime("%Y-%m-%d", time.localtime(made)) \
                  + (f" with {e.standardVersion}" if e.standardVersion else "")
            print(f"{'(off) ' if not e.enabled else ''}{e.project} / {e.config}: standard {std}; last result: "
                  + (f"{statusLabels.get(res.status, res.status)} ({res.when}) {res.message}" if res else statusLabels[NOTRUN]))
        return 0
    entries = [e for e in (suite.entries if args.recreate or args.accept else suite.enabled()) if chosen(e)]
    if not len(entries):
        print("There are no tests to run." + ("" if len(suite.entries) else " Add the standards already there with --find."))
        return 2
    if args.accept:
        done = [runner.accept(*e.key) for e in entries if runner.canAccept(*e.key) is None]
        for res in done:
            print(resultLine(res))
        print(f"\nMade {len(done)} new PDFs the standards (the old ones are kept as .bak)." if len(done)
              else "None of those has a new PDF that differs from its standard.")
        return 0
    jobs = args.jobs or int(suite.settings.get("jobs") or 4)
    version = runner.version()
    print(f"{'Recreating the standards of' if args.recreate else 'Running'} {len(entries)} tests with PTXprint "
          f"{version or suite.settings.get('program')}, {jobs} at once.", flush=True)
    def one(e):
        res = runner.recreate(*e.key) if args.recreate else runner.run(*e.key)
        print(resultLine(res), flush=True)
        return res
    pool = ThreadPoolExecutor(max_workers=max(1, jobs))
    try:
        results = list(pool.map(one, entries))
    except KeyboardInterrupt:
        runner.stop()
        pool.shutdown(wait=True)
        print("Stopped.")
        return 1
    pool.shutdown()
    print("\n" + summarise(results) + ".")
    return 0 if all(r.status in (SAME, ACCEPTED) for r in results) else 1

def main(argv=None):
    if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")      # titles in any script, on any console
    if argv is None:
        argv = sys.argv[1:]
    testing = "--testing" in argv
    parser = argparse.ArgumentParser(prog="ptxprint-manager", description="Multi-project management tool for PTXprint")
    parser.add_argument("-p", "--projects", help="Folder the Paratext projects are in")
    # for PTXprint's developers: the regression tests (see above). Not shown to users.
    parser.add_argument("--testing", action="store_true", help=argparse.SUPPRESS)
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
    pub = sub.add_parser("publications", help="List the publications and title variables of configurations")
    pub.add_argument("-P", "--project", action="append", help="Project(s) [all]")
    pub.add_argument("-c", "--config", action="append", help="Configuration name(s) [all]")
    cmp = sub.add_parser("compare", help="Compare a configuration's settings with one project's")
    cmp.add_argument("-P", "--project", action="append", help="Project(s) to compare [all that have the configuration]")
    cmp.add_argument("-c", "--config", action="append", help="The configuration")
    cmp.add_argument("--ref", help="The project to compare the others with")
    cmp.add_argument("--all", action="store_true", help="Also the settings only one of them has")
    cmp.add_argument("--copy", action="append", metavar="SECTION/SETTING", help="Copy this setting from the reference (repeatable)")
    cmp.add_argument("--yes", action="store_true", help="With --copy: don't ask")
    sty = sub.add_parser("styles", help="Compare styles: one configuration across projects, or a project's configurations")
    sty.add_argument("-P", "--project", action="append", help="Project(s) to compare [all that have the configuration]")
    sty.add_argument("-c", "--config", action="append", help="The configuration (or, with --within, each one to compare)")
    sty.add_argument("--within", metavar="PROJECT", help="Compare configurations of this one project")
    sty.add_argument("--ref", help="Compare with this one [with what most have]")
    sty.add_argument("--strays", action="store_true", help="Only where one or two differ")
    sty.add_argument("--all", action="store_true", help="Also names and structure, which don't change the page")
    if testing:
        reg = sub.add_parser("regress", help="Regression tests: print each test of the suite and compare it with its standard")
        reg.add_argument("-P", "--project", action="append", help="Project(s) [all in the suite]")
        reg.add_argument("-c", "--config", action="append", help="Configuration name(s) [all in the suite]")
        reg.add_argument("-j", "--jobs", type=int, help="How many to print at once [the suite's setting, 4]")
        reg.add_argument("--suite", help="The test suite [<projects folder>/ptxprintTests.json]")
        act = reg.add_mutually_exclusive_group()
        act.add_argument("--recreate", action="store_true", help="Print again and make the new PDFs the standards")
        act.add_argument("--accept", action="store_true", help="Make the PDFs of the last run that differed the standards")
        act.add_argument("--list", action="store_true", help="List the tests and their last results")
        act.add_argument("--find", action="store_true", help="Add the projects' existing standard PDFs to the suite")
        act.add_argument("--add", action="store_true", help="Add the -c configuration(s) of the -P projects to the suite")
        act.add_argument("--remove", action="store_true", help="Take the chosen tests out of the suite (not their standards)")
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
    elif args.command == "publications":
        return doPublications(args)
    elif args.command == "compare":
        return doCompare(args)
    elif args.command == "styles":
        return doStyles(args)
    elif args.command == "secondary":
        if args.to is not None and splitList(args.project) is None:
            print("Say which project(s) to change: -P NAME")
            return 2
        return doSecondary(args)
    elif args.command == "regress":
        return doRegress(args)
    from ptxprint.manager.gtkmanager import runWindow
    return runWindow(args.projects, testing=args.testing)

if __name__ == "__main__":
    sys.exit(main())
