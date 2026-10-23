#!/usr/bin/python3
import argparse, sys, os, re, configparser, shlex
import site, logging, time, socket, multiprocessing, subprocess
from shutil import rmtree
from zipfile import ZipFile, is_zipfile

import ptxprint
from ptxprint.utils import saferelpath, appdirs, bookcodes
from ptxprint.runner import popen
from pathlib import Path
# import debugpy
# debugpy.listen(("localhost", 5678))
# print("Waiting for debugger to attach...")
# debugpy.wait_for_client()

def getnsetlang(config):
    envlang = os.getenv("LANG", None)
    oldlang = config.get("init", "syslang", fallback=None)
    newlang = config.get("init", "lang", fallback=None)
    if envlang is None or oldlang == envlang:
        return newlang
    config.set("init", "lang", envlang or "")
    config.set("init", "syslang", envlang or "")
    return envlang

class DictAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        vals = getattr(namespace, self.dest, None)
        if vals is None:
            vals = {}
            setattr(namespace, self.dest, vals)
        if "=" not in values:
            parser.error(f"{option_string} needs component=value, not {values}")
        (k, v) = values.split("=", 1)
        vals[k] = v

class StreamLogger:     # thanks to shellcat_zero https://stackoverflow.com/questions/19425736/how-to-redirect-stdout-and-stderr-to-logger-in-python
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.level, line.rstrip(), stacklevel=2)
    def flush(self):
        pass

def testport(host, port, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((host, port))
                return True
        except (socket.error, ConnectionRefusedError, socket.timeout):
            pass
    return False

def broadway_socket(wnum):
    """ GTK3 broadway on posix talks over a Unix socket named after display+1. On Linux it is
        in the abstract namespace, so there is no file to look for: connect to it instead. """
    if sys.platform in ("win32", "cygwin"):
        return None
    rundir = os.environ.get("XDG_RUNTIME_DIR")
    if not rundir:
        from gi.repository import GLib
        rundir = GLib.get_user_runtime_dir()
    res = os.path.join(rundir, "broadway{}.socket".format(wnum + 1))
    return "\0" + res if sys.platform.startswith("linux") else res

def broadway_listening(wnum):
    sockpath = broadway_socket(wnum)
    if sockpath is None:
        return testport("127.0.0.1", 8880 + wnum, timeout=0.1)
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(sockpath)
            return True
    except OSError:
        return False

def broadway_ready(wnum, server, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        if server is not None and server.poll() is not None:
            return False        # the daemon died
        if broadway_listening(wnum):
            return True
        time.sleep(0.1)
    return False

def run_broadway(wnum=None):
    """ Start a broadwayd on a free display (or on wnum). Returns (server, display) or (None, None) """
    bwname = "broadwayd.exe" if sys.platform in ("win32", "cygwin") else "broadwayd"
    for d in ([wnum] if wnum is not None else range(5, 64)):
        if broadway_listening(d) or testport("127.0.0.1", 8880 + d, timeout=0.1):
            continue        # someone else has this display
        try:
            server = popen([bwname, "-p", str(8880 + d), ":"+str(d)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError as e:
            print(f"Can't run {bwname}: {e}")
            return (None, None)
        if broadway_ready(d, server):
            return (server, d)
        if server.poll() is None:
            server.terminate()
        server.wait()
        if wnum is None and d >= 8:
            break           # something is wrong with broadwayd, not just a busy display
    return (None, None)

def start_test_display():
    """ Start a broadway server and point GTK at it. This must happen before anything imports Gtk
        (ptxprint.view does), since GTK opens its display on import. Returns the server or None. """
    server, broadway_display = run_broadway()
    if server is None:
        return None
    os.environ['GDK_BACKEND'] = "broadway"
    os.environ["BROADWAY_DISPLAY"] = ":" + str(broadway_display)
    for v in ("DISPLAY", "WAYLAND_DISPLAY"):    # never fall back to a real screen
        os.environ.pop(v, None)
    return server

def runtest(prjTree, config, macrosdir, project, doit, args):
    args.quiet = True
    return _runtest(prjTree, config, macrosdir, project, doit, args)

def _runtest(prjTree, config, macrosdir, project, doit, args):
    from ptxprint.gtkview import GtkViewModel, reset_gtk_direction
    from ptxprint.gtktesting import GtkTester
    from ptxprint.utils import setup_i18n
    from gi.repository import GLib
    setup_i18n(args.lang)
    reset_gtk_direction()
    mainw = GtkViewModel(prjTree, config, macrosdir, args)
    mainw.setup_ini()
    if args.nointernet:
        mainw.set('c_noInternet', True)
        mainw.noInt = True
    # copy files before loading config
    tester = GtkTester(None, mainw)
    tester.startReplayHooks()
    mainw.replayer = tester
    if args.teststep is None:
        mainw.doSysError = tester.handlerError     # run() makes this sys.excepthook
    tester.project = project
    tester.setuprun(args.test, mainw)
    if args.pid:
        mainw.setPrjid(args.pid, project.guid)
        mainw.setConfigId(args.config or "Default")
    else:
        print("No project found to run the test on")
        return 2

    GLib.idle_add(tester.run_action, args.testwithgui, args.teststep)
    mainw.run(doit)
    test_result = tester.run_finalise()
    if args.testing:
        resname = os.path.splitext(args.test)[0] + "_result.zip"
        tester.saveSnapshot(resname)
        print(f"Replay result saved in {resname}")
    # Files only in the test run's archive come from archiving more than when the test was
    # recorded, so they don't fail it, but say what they are.
    if test_result['test']:
        print(f"These files are only in the test run's archive: {', '.join(test_result['test'])}")
    if test_result['skipped']:
        skip_str = '\n\t'.join(['', *test_result['skipped']])
        print(f"These events were skipped:{skip_str}")
    if not any(v for k, v in test_result.items() if k not in ('test', 'skipped')):
        print('Test result: PASS. No differences found to test data.')
        return 0
    print('Test result: FAIL. The following differences to test data were found:')
    if test_result['errors']:
        err_str = '\n\t'.join(['', *test_result['errors']])
        print(f"The following events could not be replayed:{err_str}")
    if test_result['cfg']:
        cfg_str = '\n\t'.join(['', *test_result['cfg']])
        print(f"The following differences were found in the cfg:{cfg_str}")
    if test_result['sty']:
        sty_str = '\n\t'.join(['', *test_result['sty']])
        print(f"The following differences were found in the sty:{sty_str}")
    if test_result['ref']:
        print(f"The following files were found only in the reference: {', '.join(test_result['ref'])}")
    if test_result['diff']:
        print(f"The following files were not identical: {', '.join(test_result['diff'])}")
    return 1

commands = {
    'print': (),
    'fill': (),
    'archive': ()
}

def main(doitfn=None, argsline=None, retview=False, viewClass=None, argsfn=None):
    parser = argparse.ArgumentParser(description="PTXprint command-line interface")
    # parser.add_argument('-h','--help', help="show this help message and exit")

    # Positional Argument
    parser.add_argument('pid', nargs="?", help="Project ID or full path to a ptxprint.cfg file")
    parser.add_argument('cmd', nargs="?", choices=list(commands.keys()), help="Non interactive command to execute")

    # Commonly Used Arguments
    parser.add_argument('-b', '--books', help="List of books to print")
    parser.add_argument('-c', '--config', help="Path to a configuration file")
    parser.add_argument('-R', '--runs', type=int, default=0, help="Limit XeTeX runs")
    parser.add_argument('-P', '--print', action='store_true', help="Run print operation")
    parser.add_argument('-B', '--pub', action='append', default=[], help="Publication id to print (repeatable), requires -P")

    # Core Configuration
    parser.add_argument('-p', '--projects', action='append', default=[], help="Path(s) to project directories (repeatable)")
    parser.add_argument('-d', '--directory', help="Directory to store temporary files")
    parser.add_argument('-L', '--lang', help="Set UI language code")
    parser.add_argument('-Z', '--zip', help="Unzip into project directory and delete at end")

    # Execution & Processing
    parser.add_argument('-A', '--action', help="Perform a specific action instead of printing")
    parser.add_argument("-o", '--output', help="Output file for actions like archive")
    parser.add_argument('-m', '--macros', help="Directory containing TeX macros (paratext2.tex)")
    parser.add_argument('-M', '--module', help="Specify module to print")
    parser.add_argument('-S', '--enablescripts',action='store_true',help="Enable process scripts in CLI use")
    parser.add_argument('-T', '--testing',action='store_true',help="Run in testing, output xdv. And don't clear zip trees")
    parser.add_argument('-C', '--capture', metavar='FILE', help="Capture interaction events from UI session to zip file")
    parser.add_argument('-t', '--test',help="test file to run interactive test against")
    parser.add_argument('--testwithgui',action='store_true',help="Run test with visible gui and don't exit")
    parser.add_argument('--teststep', type=float, nargs='?', const=0., metavar='SECONDS',
                        help="Watch a test (-t) being replayed: one event every SECONDS, or with no value, "
                             "on each press of Step (or Space) in the replay window. Implies --testwithgui")
    
    # Performance & Debugging
    parser.add_argument("-j", "--jobs", type=int, default=1, help="Number of multiprocessing jobs to run")
    parser.add_argument("--restart", action="store_true", default=False, help="fill: start from the current adjustments")
    parser.add_argument("--stop", action="store_true", default=False, help="fill: stop each book at its first unfixable page")
    parser.add_argument('-q', '--quiet', action='store_true', help="Suppress splash screen and limit output")
    parser.add_argument('-l', '--logging', help="Logging level [DEBUG, INFO, WARN, ERROR, number]")
    parser.add_argument('--logfile', default='ptxprint.log', help='Set log file (default: ptxprint.log) or "none"')
    parser.add_argument('-to', '--timeout', type=int, default=1200, help="XeTeX runtime timeout (seconds)")
    parser.add_argument('--debug', action="store_true", help="Enable debug output")

    # Font Settings
    parser.add_argument('-f', '--fontpath', action='append', help="Specify directories containing fonts (repeatable)")
    parser.add_argument('--nofontcache', action="store_true", help="Disable font cache updates")
    parser.add_argument('--testsuite', action="store_true", help="Use only fonts from project and test suite")

    # PDF & Output Settings
    parser.add_argument('-F', '--difffile', help="Generate difference PDF against another file")
    parser.add_argument('--diffpages', type=int, default=0, help="Max pages to insert in diff file")
    parser.add_argument('--diffignore', help="Comma separated parts of the page to ignore when comparing: "
                        "headfoot (headers and footers), sides (margin notes, thumb tabs)")
    parser.add_argument('--diffsmart', action='store_true',
                        help="When comparing, line up each page first so that a moved text block is not a difference")
    parser.add_argument('--diffoffset', type=int, default=0,
                        help="Page offset when comparing: positive skips pages at the start of the old PDF, "
                             "negative skips pages at the start of the new PDF")
    parser.add_argument('--diffoutfile', help="Output filename for difference PDF")
    parser.add_argument('--diffdpi', type=int, default=0, help="DPI for PDF differencing")
    parser.add_argument('-V', '--pdfversion', type=int, default=14, help="PDF version to read/write (default: 14)")

    # Miscellaneous & Experimental
    parser.add_argument('-N', '--nointernet', action="store_true", help="Disable all internet access")
    parser.add_argument('-n', '--port', type=int, help="Port to listen on")
    parser.add_argument('--nox11', action='store_true', help="Don't switch to X11")
    parser.add_argument('-D', '--define', action=DictAction, help="Set UI component=value (repeatable)")
    parser.add_argument('-z', '--extras', type=int, default=0, help="Special flags (verbosity of xdvipdfmx, request PTdir, no config)")
    parser.add_argument('-I', '--identify', action="store_true", help="Add widget names to tooltips")
    parser.add_argument('-E', '--experimental', type=int, default=0, help="Enable experimental features (0 = UI extensions)")

    exit_code = 0

    if argsfn is not None:
        argsfn(parser)

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        from ptxprint.gtkutils import HelpTextViewWindow
        tv = HelpTextViewWindow()
        def print_message(message, file=None):
            tv.print_message(message)
        parser._print_message = print_message
        os.environ['PATH'] += os.pathsep + sys._MEIPASS.replace("/","\\")

    conffile = os.path.join(appdirs.user_config_dir("ptxprint", "SIL"), "ptxprint_user.cfg")
    config = configparser.ConfigParser(interpolation=None)
    envopts = os.getenv('PTXPRINT_OPTS', None)
    args = None
    if argsline is None and envopts is not None:
        argsline = envopts
    elif argsline is None and config.has_option('init', 'commandargs'):
        argsline = config.get('init', 'commandargs')
        config.remove_option('init', 'commandargs')
    if argsline is not None:
        opts = shlex.split(argsline)
        args = parser.parse_args(opts, args)
    args = parser.parse_args(None, args)
    if args.pid in commands and args.cmd is None:
        args.cmd = args.pid
        args.pid = None
    if args.cmd is None:
        if args.print:
            args.cmd = "print"
        elif args.action == "createArchive":
            args.cmd = "archive"

    testserver = None
    if args.teststep is not None:
        args.testwithgui = True
    if args.test is not None and not args.testwithgui:
        testserver = start_test_display()
        if testserver is None:
            print("Can't start a broadway server to run the test on. Is broadwayd installed?")
            return 2
        args.nox11 = True
    try:
        return _main(args, config, conffile, doitfn, retview, viewClass)
    finally:
        if testserver is not None:
            testserver.terminate()
            testserver.wait()

def _main(args, config, conffile, doitfn, retview, viewClass):
    exit_code = 0
    # We might need to do this AFTER reading in the user-config file (as the UI language needs to be read)
    # setup_i18n()

    multiprocessing.freeze_support()
    try:
        multiprocessing.set_start_method("spawn")
    except RuntimeError:
        pass
    logconffile = os.path.join(appdirs.user_config_dir("ptxprint", "SIL"), "ptxprint_logging.cfg")
    if sys.platform.startswith("win") and args.logfile == 'ptxprint.log':
        args.logfile = os.path.join(appdirs.user_config_dir("ptxprint", "SIL"), "ptxprint.log")
    if os.path.exists(logconffile):
        logging.config.fileConfig(logconffile)
    elif args.logging:
        try:
            loglevel = int(args.logging)
        except ValueError:
            loglevel = getattr(logging, args.logging.upper(), None)
        if isinstance(loglevel, int):
            parms = {'level': loglevel, 'datefmt': '%d/%b/%Y %H:%M:%S', 'format': '%(asctime)s.%(msecs)03d %(levelname)s:%(module)s(%(lineno)d) %(message)s'}
            if args.logfile.lower() != "none":
                logfh = open(args.logfile, "w", encoding="utf-8")
                parms.update(stream=logfh, filemode="w") #, encoding="utf-8")
            try:
                logging.basicConfig(**parms)
            except FileNotFoundError as e:      # no write access to the log
                print("Exception", e)
    log = logging.getLogger('ptxprint')
    log.info("git sha: $Id: 5efbc516bbe9dd1cbb328d871d163cae7b9ea0ce $")
    log.debug(args)

    if args.logging and getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        sys.stdio = StreamLogger(log, logging.INFO)
        sys.stderr = StreamLogger(log, logging.ERROR)

    from ptxprint.utils import _, setup_i18n, get_ptsettings, find_pt_candidates, \
                                pt_bindir, putenv, attach_console
    from ptxprint.font import initFontCache, cachepath, writefontsconf

    fontconfig_path = writefontsconf(args.fontpath,testsuite=args.testsuite)
    putenv("FONTCONFIG_FILE", fontconfig_path)

    from ptxprint.version import VersionStr
    from ptxprint.view import ViewModel, doError
    from ptxprint.runjob import RunJob, isLocked
    from ptxprint.project import ProjectList

    attach_console()
    if viewClass is None:
        viewClass = ViewModel
    savetreedirs = False
    ptxdir = None
    # necessary for the side effect of setting pt_bindir :(
    if not len(args.projects):
        pdir = os.getenv("PTXPRINT_PROJECTSDIR", None)
        if pdir is not None:
            args.projects.append(pdir)
        savetreedirs = True

    testtree = None
    if args.test:
        savetreedirs = False
        from ptxprint.gtktesting import load_project_from_archive
        # A test runs only on the project in its archive, never on the user's own projects
        try:
            with ZipFile(args.test) as zf:
                test_project = load_project_from_archive(zf)
        except Exception as e:
            print(f"Can't use {args.test} as a test: {e}")
            return 2
        args.pid = test_project.prjid
        args.projects = []
        conffile = '{}/ptxprint_user.cfg'.format(test_project.path)
        # the tree that holds the project, not the project itself
        testtree = os.path.dirname(test_project.path)
        args.projects.append(testtree)

    if (args.extras & 16) == 0 and os.path.exists(conffile):
        config.read(conffile, encoding="utf-8")
        if args.pid is None:
            if config.has_option("init", "project"):
                args.pid = config.get('init', 'project')
                if args.config is None and config.has_option("init", "config"):
                    args.config = config.get('init', 'config')
        else: # pid was specified
            if args.config is None and config.has_option("projects", args.pid):
                args.config = config.get("projects", args.pid)
        if not len(args.projects) and config.has_option("init", "paratext"):
            pdir = config.get("init", "paratext")
            if os.path.exists(pdir):
                args.projects.append(pdir)
                print(f"Adding {pdir}")
        if not len(args.projects) and config.has_section("projectdirs"):
            pdirs = config.options("projectdirs")
            if len(pdirs) and re.match(r"^\d{1,2}$", pdirs[0]):
                ps = [config.get("projectdirs", p) for p in sorted(pdirs, key=int)]
            else:
                ps = pdirs
            for p in ps:
                if p not in args.projects and os.path.exists(p):
                    args.projects.append(p)
                    print(f"Adding {p}")
    else:
        if not os.path.exists(os.path.dirname(conffile)):
            os.makedirs(os.path.dirname(conffile))
        config.add_section("init")
        config.add_section("projects")
    log.debug("Loaded config")

    if not len(args.projects):
        candidates = find_pt_candidates()
        if len(candidates) == 1:
            args.projects.append(candidates[0]['path'])
            print(f"Adding {candidates[0]['path']}")
        elif len(candidates) > 1:
            if not args.print and args.test is None and not args.cmd:
                from ptxprint.gtkview import chooseProjectsDir
                chosen = chooseProjectsDir(candidates)
                if chosen is None:
                    sys.exit(1)
                args.projects.append(str(chosen))
            else:
                # Non-GUI mode: add all found directories
                for c in candidates:
                    args.projects.append(c['path'])
                    print(f"Adding {c['path']}")
    elif not any(os.path.isdir(p) for p in args.projects):
        print(f"Projects directories do not exist in {args.projects}. Quitting")
        sys.exit(1)

    if args.lang is None:
        args.lang = getnsetlang(config)

    if sys.platform.startswith("linux") and not args.nox11:
        os.environ['GDK_BACKEND'] = 'x11'
    if (args.extras & 8) != 0 or not len(args.projects):
        if not args.print and args.test is None and not args.cmd:
            from ptxprint.gtkview import chooseProjectsDir
            chosen = chooseProjectsDir(find_pt_candidates())
            if chosen is None:
                sys.exit(1)
            args.projects = [str(chosen)]
        else:
            sys.exit(1)
    else:
        args.projects = [os.path.abspath(p.replace("\\", "/")) for p in args.projects if p is not None]
        args.projects = [p[:-1] if p.endswith("/") else p for p in args.projects]

    # Only remember project folders the user chose, not ones given with -p or a test's temporary tree
    if savetreedirs:
        config.remove_section("projectdirs")
        config.add_section("projectdirs")
        for i, p in enumerate(args.projects, 1):
            config.set("projectdirs", str(i), str(p))

    # handle being passed a .zip
    if not args.zip and args.pid is not None and args.pid.lower().endswith(".zip"):
        fname = os.path.basename(args.pid)[:-4]
        m = re.match(r"^(.+?)-(.+?)PTXprintArchive", fname)
        if m:
            args.zip = args.pid
            args.pid = m.group(1)
            args.config = m.group(2)
        else:
            print("Sorry - no match")
    # handle being passed the path to a ptxprint.cfg
    elif args.pid is not None and (any(x in args.pid for x in "\\/") or args.pid.lower().endswith(".cfg")):
        pidpath = saferelpath(args.pid, args.projects[0]).replace("\\", "/")
        if pidpath.startswith("..") or pidpath.startswith("/"):
            pidpath = os.path.abspath(args.pid).replace("\\", "/")
        pidbits = pidpath.split("/")
        if len(pidbits) > 4 and "ptxprint" in [x.lower() for x in pidbits[-3:-1]]:
            if pidbits[-2].lower() == "ptxprint":
                if len(pidbits) > 4:
                    args.projects[0] = "/".join(pidbits[:-4])
                pidbits = pidbits[-4:]
            elif pidbits[-3].lower() == "ptxprint":
                if len(pidbits) > 5:
                    args.projects[0] = "/".join(pidbits[:-5])
                pidbits = pidbits[-5:]
        if len(pidbits) == 5:
            args.config = pidbits[3]
        if len(pidbits) > 3:
            args.pid = pidbits[0]

    if args.directory is not None:
        args.directory = os.path.abspath(args.directory)
    else:
        args.directory = os.path.abspath(".")

    # Where to find the default for -p
    # HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Paratext\8:Settings_Directory

    log.debug(f"project id={args.pid}, config={args.config}, directory={args.directory}")

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        scriptsdir = os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__))), 'ptxprint')
    else:
        scriptsdir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    
    macrosdir = os.path.join(scriptsdir, 'ptx2pdf')
    if args.macros:
        macrosdir = args.macros
    elif os.path.exists("/usr/share/ptx2pdf") and not os.path.exists(macrosdir):
        scriptsdir = "/usr/share/ptx2pdf"
        macrosdir = "/usr/share/ptx2pdf/texmacros"
    elif not getattr(sys, 'frozen', False) and not os.path.exists(macrosdir):
        macrosdir = os.path.join(scriptsdir, "..", "..", "..", "src")

    if doitfn is None:
        def doit(printer, maxruns=0, noview=False, noaction=False, nothreads=False, forcedlooseness=None):
            if not isLocked():
                if maxruns > 0:
                    oldruns = args.runs
                    args.runs = maxruns
                runjob = RunJob(printer, scriptsdir, macrosdir, args)
                runjob.nothreads = nothreads
                runjob.forcedlooseness = forcedlooseness
                runjob.doit(noview=noview, noaction=noaction)
                if maxruns > 0:
                    args.runs = oldruns
                return runjob
            else:
                return None
    else:
        def doit(printer, **kw):
            return doitfn(printer, scriptsdir, macrosdir, args, **kw)

    if args.fontpath is not None:
        for p in args.fontpath:
            if os.path.exists(p):
                cachepath(p, nofclist=args.nofontcache)

    if args.zip:
        print(f"{args.projects=} {args.pid=} {args.config=}")
        if not os.path.isfile(args.zip) or not is_zipfile(args.zip):
            print(f"Can't read archive {args.zip}. Quitting")
            sys.exit(1)
        if not args.testsuite and len(args.projects[0]) and args.pid:
            rmtree(os.path.join(args.projects[0], args.pid), ignore_errors = True)
        zf = ZipFile(args.zip)
        zf.extractall(args.projects[0])
        zf.close()

    prjTree = ProjectList()
    for p in args.projects:
        prjTree.addTreedir(p)
        log.debug(f"Adding project tree: {p}")

    project = None
    if args.pid:
        project = prjTree.findProject(args.pid)
        if project is None:
            print(f"Can't find project {args.pid} in {prjTree.treedirs}")
            args.pid = None     # keep going anyway, just with no pid specified.
        if args.config:
            if project is None:
                args.config = None
            elif args.config != "Default" and args.config not in project.configs:
                # Keep going with it (as before), but say so: a mistyped name otherwise goes unnoticed
                print(f"Can't find config {args.config} in project {args.pid} ({project.srcPath(None)})")
    if args.test is not None:
        try:
            exit_code = runtest(prjTree, config, macrosdir, project, doit, args)
        finally:
            if testtree is not None and not args.testing:
                rmtree(testtree, ignore_errors=True)
    elif args.print or args.cmd is not None or retview:
        mainw = viewClass(prjTree, config, macrosdir, args, odir=scriptsdir)
        mainw.setup_ini()
        if args.pid:
            mainw.setPrjid(args.pid, project.guid, loadConfig=False, startup=True)
            mainw.setConfigId(args.config or "Default")
        if args.zip:
            mainw.set("c_usesysfonts", False)
        res = 0
        log.debug(f"Created viewmodel for {project} in {args.projects}")
        initFontCache(nofclist=args.nofontcache).wait()
        log.debug("Loaded fonts")
        if not retview and mainw.project is None and (args.print or args.cmd is not None):
            print("No project to work on. Quitting")
            sys.exit(1)
        if args.print or retview or args.cmd in ("print", "fill"):
            if args.pub:
                from ptxprint.publications import printSetup
                from ptxprint.utils import BuildParams
                from ptxprint.multiprint import MultiPrint
                from usfmtc.reference import RefList

                mprint = MultiPrint(numproc=args.jobs or None)
                for pub in args.pub:
                    if pub not in mainw.publications:
                        print(f"Can't find publication {pub} in config {mainw.cfgid}")
                        continue
                    pvars = mainw.publications[pub]
                    books = pvars.get("__books", "")
                    if not len(RefList(books)):
                        print(f"No books to print for publication {pub}")
                        continue
                    bparms = BuildParams(
                        prjtree = mainw.prjTree,
                        config = mainw.userconfig,
                        macrosdir = mainw.scriptsdir,
                        scriptsdir = mainw.scriptsdir,
                        args = mainw.args,
                        restart = False,
                        pid = mainw.project.prjid,
                        guid = mainw.project.guid,
                        cfgid = mainw.cfgid,
                        setupfn = printSetup,       # must be module global
                        setupargs = pvars,
                        pubid = pub)
                    mprint.submit_print_job(RefList(books), bparms)
                mprint.wait()
                sys.exit(0)
            if args.books is not None and len(args.books):
                mainw.bookNoUpdate = True
                mainw.set("ecb_booklist", args.books)
                mainw.set("r_book", "multiple")
            elif args.module is not None and len(args.module):
                mainw.set("r_book", "module")
                mainw.moduleFile = Path(args.module)
            if args.define is not None:
                for k, v in args.define.items():
                    if k.startswith("c_"):      # a checkbox wants a bool, not the string "False"
                        v = v.strip().lower() in ("true", "1", "yes", "on")
                    try:
                        mainw.set(k, v)
                    except ValueError as e:     # e.g. a spin button given a word
                        print(f"Can't set {k} to {v}: {e}")
            if args.difffile:
                mainw.set("btn_selectDiffPDF", None if args.difffile.lower() == 'last' else os.path.abspath(args.difffile))
                mainw.set("c_onlyDiffs", True)
                if args.diffpages > 0:
                    mainw.set("s_diffpages", str(args.diffpages))
                if args.diffignore is not None:
                    ignores = [x.strip().lower() for x in args.diffignore.split(",")]
                    mainw.set("c_diffIgnoreHeadFoot", "headfoot" in ignores)
                    mainw.set("c_diffIgnoreSides", "sides" in ignores)
                if args.diffsmart:
                    mainw.set("c_diffSmart", True)
                if args.diffoffset:
                    mainw.set("s_diffOffset", str(args.diffoffset))
                mainw.docreatediff = True
                if args.difffile.lower() == 'last':
                    mainw.set("s_keepVersions", "1")
            if retview:
                return mainw
            mainw.savePics()
            mainw.saveStyles()
            mainw.saveAdjlists()
            if not args.enablescripts:
                mainw.set("c_processScript", False)
            if args.cmd == "fill":
                from ptxprint.utils import BuildParams
                from ptxprint.multiprint import MultiPrint
                tout = float(mainw.get("s_pbtimeout") or 0) * 60
                bparms = BuildParams(
                    prjtree = mainw.prjTree,
                    config = mainw.userconfig,
                    macrosdir = mainw.scriptsdir,
                    scriptsdir = mainw.scriptsdir,
                    args = mainw.args,
                    restart = args.restart,
                    pid = mainw.project.prjid,
                    guid = mainw.project.guid,
                    cfgid = mainw.cfgid,
                    timeout = tout if tout >= 1 else None,
                    loglevel = int(getattr(logging, args.logging.upper(), args.logging)) if args.logging else None)
                mprint = MultiPrint(numproc=args.jobs or None)
                mprint.submit_fill_jobs(mainw.getBooks(), bparms, stop=args.stop)
                results = mprint.wait()
                mprint.teardown()
                print("\n".join(str(r) for r in sorted(results, key=lambda a:(int(bookcodes.get(a[0], 100)),) + a)))
            else:
                job = doit(mainw, noview=True, nothreads=True)
                res = 0 if job is None else job.res
                print(f"{res=}")
        if args.action:
            actionfn = getattr(mainw, args.action, None)
            if not callable(actionfn):
                print(f"Unknown action {args.action}")
                sys.exit(1)
            print(actionfn())
        elif args.cmd == "archive":
            mainw.createArchive(args.output, nobuild=True)
        sys.exit(res)
    else:
        from ptxprint.gtkview import GtkViewModel, reset_gtk_direction
        from ptxprint.ipcserver import make_server
        #from ptxprint.restserver import startRestServer
        goround = True
        loops = 0
        while (goround):
            setup_i18n(args.lang)
            reset_gtk_direction()
            goround = False
            mainw = GtkViewModel(prjTree, config, macrosdir, args)
            if not loops and args.port:
                (server, is_server) = make_server(mainw, "127.0.0.1", args.port)
                if not is_server:
                    server.transmit({"verb": "project", "params": [args.pid, args.config or "Default"]})
                    loops = -1
                    break
                else:
                    mainw.server = server
            #if not prjTree.findProject("BSB"):
            #    mainw._expandDBLBundle("BSB", "path/to/BSBDBL.zip")
            if not mainw.setup_ini():
                if mainw.splash is not None:
                    mainw.splash.terminate()
                print("Failed to open project directory")
                sys.exit(1)
            if args.zip:
                mainw.set("c_usesysfonts", False)
            if args.nointernet:
                mainw.set('c_noInternet', True)
                mainw.noInt = True
            if args.pid:
                mainw.setPrjid(args.pid, project.guid)
                mainw.setConfigId(args.config or "Default")
            else:
                mainw.setFallbackProject()
            if args.define is not None:
                for k, v in args.define.items():
                    if k.startswith("c_"):      # a checkbox wants a bool, not the string "False"
                        v = v.strip().lower() in ("true", "1", "yes", "on")
                    try:
                        mainw.set(k, v)
                    except ValueError as e:     # e.g. a spin button given a word
                        print(f"Can't set {k} to {v}: {e}")
            log.debug(f"Created gtkview for {args.projects}")
            mainw.run(doit)
            if mainw.lang != args.lang:
                if not sys.platform.startswith("win"):
                    mainw.lang += ".UTF-8"
                config.set("init", "lang", mainw.lang)
                # Reopen in the new language. Without langChanged, a user with no language set at
                # startup (args.lang None) was dropped out of PTXprint instead.
                if args.lang is not None or getattr(mainw, "langChanged", False):
                    args.lang = mainw.lang
                    print(f"{args.lang}")
                    project = mainw.project
                    if project is not None:
                        args.pid = project.prjid
                        args.config = mainw.cfgid
                    goround = True
            loops += 1
        if loops >= 0:
            if savetreedirs:
                mainw.prjTree.addToConfig(config)
            log.debug(f"Writing user config to {conffile}")
            with open(conffile, "w", encoding="utf-8") as outf:
                config.write(outf)
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
