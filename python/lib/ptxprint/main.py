#!/usr/bin/python3
import argparse, sys, os, re, configparser, shlex
import site, logging
from shutil import rmtree
from zipfile import ZipFile

import ptxprint
from ptxprint.utils import saferelpath, appdirs
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
        (k, v) = values.split("=")
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

def main(doitfn=None):
    parser = argparse.ArgumentParser(description="PTXprint command-line interface")
    # parser.add_argument('-h','--help', help="show this help message and exit")

    # Positional Argument
    parser.add_argument('pid', nargs="?", help="Project ID or full path to a ptxprint.cfg file")

    # Commonly Used Arguments
    parser.add_argument('-b', '--books', help="List of books to print")
    parser.add_argument('-c', '--config', help="Path to a configuration file")
    parser.add_argument('-R', '--runs', type=int, default=0, help="Limit XeTeX runs")
    parser.add_argument('-P', '--print', action='store_true', help="Run print operation")

    # Core Configuration
    parser.add_argument('-p', '--projects', action='append', default=[], help="Path(s) to project directories (repeatable)")
    parser.add_argument('-d', '--directory', help="Directory to store temporary files")
    parser.add_argument('-L', '--lang', help="Set UI language code")
    parser.add_argument('-Z', '--zip', help="Unzip into project directory and delete at end")

    # Execution & Processing
    parser.add_argument('-A', '--action', help="Perform a specific action instead of printing")
    parser.add_argument('-m', '--macros', help="Directory containing TeX macros (paratext2.tex)")
    parser.add_argument('-M', '--module', help="Specify module to print")
    parser.add_argument('-T','--testing',action='store_true',help="Run in testing, output xdv. And don't clear zip trees")
    
    # Performance & Debugging
    parser.add_argument('-q', '--quiet', action='store_true', help="Suppress splash screen and limit output")
    parser.add_argument('-l', '--logging', help="Logging level [DEBUG, INFO, WARN, ERROR, number]")
    parser.add_argument('--logfile', default='ptxprint.log', help='Set log file (default: ptxprint.log) or "none"')
    parser.add_argument('--timeout', type=int, default=1200, help="XeTeX runtime timeout (seconds)")
    parser.add_argument('--debug', action="store_true", help="Enable debug output")
    parser.add_argument('-C', '--capture', help="Capture interaction events (not yet used)")

    # Font Settings
    parser.add_argument('-f', '--fontpath', action='append', help="Specify directories containing fonts (repeatable)")
    parser.add_argument('--nofontcache', action="store_true", help="Disable font cache updates")
    parser.add_argument('--testsuite', action="store_true", help="Use only fonts from project and test suite")

    # PDF & Output Settings
    parser.add_argument('-F', '--difffile', help="Generate difference PDF against another file")
    parser.add_argument('--diffpages', type=int, default=0, help="Max pages to insert in diff file")
    parser.add_argument('--diffoutfile', help="Output filename for difference PDF")
    parser.add_argument('--diffdpi', type=int, default=0, help="DPI for PDF differencing")
    parser.add_argument('-V', '--pdfversion', type=int, default=14, help="PDF version to read/write (default: 14)")

    # Miscellaneous & Experimental
    parser.add_argument('-N', '--nointernet', action="store_true", help="Disable all internet access")
    parser.add_argument('-n', '--port', type=int, help="Port to listen on")
    parser.add_argument('-D', '--define', action=DictAction, help="Set UI component=value (repeatable)")
    parser.add_argument('-z', '--extras', type=int, default=0, help="Special flags (verbosity of xdvipdfmx, request PTdir, no config)")
    parser.add_argument('-I', '--identify', action="store_true", help="Add widget names to tooltips")
    parser.add_argument('-E', '--experimental', type=int, default=0, help="Enable experimental features (0 = UI extensions)")

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
    argsline = None
    if envopts is not None:
        argsline = envopts
    elif config.has_option('init', 'commandargs'):
        argsline = config.get('init', 'commandargs')
        config.remove_option('init', 'commandargs')
    if argsline is not None:
        opts = shlex.split(argsline)
        args = parser.parse_args(opts, args)
    args = parser.parse_args(None, args)

    # We might need to do this AFTER reading in the user-config file (as the UI language needs to be read)
    # setup_i18n()

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

    from ptxprint.utils import _, setup_i18n, get_ptsettings, pt_bindir, putenv
    from ptxprint.font import initFontCache, cachepath, writefontsconf

    fontconfig_path = writefontsconf(args.fontpath,testsuite=args.testsuite)
    putenv("FONTCONFIG_FILE", fontconfig_path)
    if not args.print and not args.action:
        from ptxprint.gtkview import GtkViewModel, getPTDir, reset_gtk_direction
        from ptxprint.ipcserver import make_server
        #from ptxprint.restserver import startRestServer

    from ptxprint.view import ViewModel, VersionStr, doError
    from ptxprint.runjob import RunJob, isLocked
    from ptxprint.project import ProjectList

    savetreedirs = False
    ptxdir = None
    # necessary for the side effect of setting pt_bindir :(
    if not len(args.projects):
        pdir = os.getenv("PTXPRINT_PROJECTSDIR", None)
        if pdir is not None:
            args.projects.append(pdir)
        savetreedirs = True

    if (args.extras & 4) == 0 and os.path.exists(conffile):
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
        pdir = get_ptsettings()
        if pdir is not None:
            args.projects.append(pdir)
            print(f"Adding {pdir}")

    if args.lang is None:
        args.lang = getnsetlang(config)

    if (args.extras & 2) != 0 or not len(args.projects):
        # print("No Paratext Settings directory found - sys.exit(1)")
        if not args.print:
            pdir = getPTDir()
            if pdir is None:
                sys.exit(1)
            else:
                args.projects = [pdir]
        else:
            sys.exit(1)
    else:
        args.projects = [os.path.abspath(p.replace("\\", "/")) for p in args.projects if p is not None]
        args.projects = [p[:-1] if p.endswith("/") else p for p in args.projects]

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
        def doit(printer, maxruns=0, noview=False, nothreads=False, forcedlooseness=None):
            if not isLocked():
                if maxruns > 0:
                    oldruns = args.runs
                    args.runs = maxruns
                runjob = RunJob(printer, scriptsdir, macrosdir, args)
                runjob.nothreads = nothreads
                runjob.forcedlooseness = forcedlooseness
                runjob.doit(noview=noview)
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
        if not args.testsuite and len(args.projects[0]) and len(args.pid):
            rmtree(os.path.join(args.projects[0], args.pid), ignore_errors = True)
        zf = ZipFile(args.zip)
        zf.extractall(args.projects[0])
        zf.close()

    prjTree = ProjectList()
    for p in args.projects:
        prjTree.addTreedir(p)
        log.debug(f"Adding project tree: {p}")

    if args.pid:
        project = prjTree.findProject(args.pid)
        if project is None:
            print(f"Can't find project {args.pid} in {prjTree.treedirs}")
            args.pid = None     # keep going anyway, just with no pid specified.
        if args.config:
            if project is None or project.srcPath(args.config) is None:
                args.config = None

    if args.print or args.action is not None:
        mainw = ViewModel(prjTree, config, macrosdir, args)
        mainw.setup_ini()
        if args.pid:
            mainw.setPrjid(args.pid, project.guid, loadConfig=False)
            mainw.setConfigId(args.config or "Default")
        res = 0
        log.debug(f"Created viewmodel for {project} in {args.projects}")
        initFontCache(nofclist=args.nofontcache).wait()
        log.debug("Loaded fonts")
        if args.print:
            if args.books is not None and len(args.books):
                mainw.bookNoUpdate = True
                mainw.set("ecb_booklist", args.books)
                mainw.set("r_book", "multiple")
            elif args.module is not None and len(args.module):
                mainw.set("r_book", "module")
                mainw.moduleFile = Path(args.module)
            if args.define is not None:
                for k, v in args.define.items():
                    mainw.set(k, v)
            if args.difffile:
                mainw.set("btn_selectDiffPDF", None if args.difffile.lower() == 'last' else os.path.abspath(args.difffile))
                mainw.set("c_onlyDiffs", True)
                if args.diffpages > 0:
                    mainw.set("s_diffpages", str(args.diffpages))
                mainw.docreatediff = True
                if args.difffile.lower() == 'last':
                    mainw.set("s_keepVersions", "1")
            mainw.savePics()
            mainw.saveStyles()
            job = doit(mainw, noview=True, nothreads=True)
            if job is not None:
                res = job.res
            else:
                res = 0
        if args.action:
            print(getattr(mainw, args.action)())
        print(f"{res=}")
        sys.exit(res)
    else:
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
                    mainw.set(k, v)
            log.debug(f"Created gtkview for {args.projects}")
            mainw.run(doit)
            if mainw.lang != args.lang:
                if not sys.platform.startswith("win"):
                    mainw.lang += ".UTF-8"
                config.set("init", "lang", mainw.lang)
                if args.lang is not None:
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
            with open(conffile, "w", encoding="utf-8") as outf:
                config.write(outf)

if __name__ == "__main__":
    main()
