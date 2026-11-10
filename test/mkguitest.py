#!/usr/bin/env python3
""" Make a lean GUI test (.zip) from a list of actions (.json, the tutorial format).

    The actions are replayed in PTXprint on a copy of the project, under a broadway display,
    with test recording on, so the result is just what recording them by hand with
    `ptxprint -C test.zip --lean` gives: the actions and the files they changed. The .json names
    the project and config ("project", "config"), and may give the view level ("uilevel"). For
    a .json kept in <project>/shared/tests/<config>/ they default to that project and config.

    mkguitest.py projects/WSGlatin/shared/tests/Default/styleedits.json   # writes styleedits.zip

    Check the files the test changed (test/modified_files in the zip) before using it: the test
    passes as long as PTXprint keeps doing whatever it did when the test was made.
"""

import sys, os, json, argparse, tempfile, shutil, shlex

testdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(testdir, "..", "python", "lib"))

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("actions", help="actions to replay (.json)")
    parser.add_argument("-o", "--output", help="test file to write (default: the actions file with .zip, "
                        "if that is in the project's shared/tests/<config>, else there)")
    parser.add_argument("-p", "--projects", action="append", default=[],
                        help="directory holding the project (default: test/projects)")
    args = parser.parse_args()

    with open(args.actions, encoding="utf-8") as inf:
        spec = json.load(inf)
    # <project>/shared/tests/<config>/name.json
    cfgdir = os.path.dirname(os.path.abspath(args.actions))
    parts = cfgdir.split(os.sep)
    intests = len(parts) > 3 and parts[-2] == "tests" and parts[-3] == "shared"
    prjid = spec.get("project", parts[-4] if intests else None)
    cfgid = spec.get("config", parts[-1] if intests else "Default")
    if prjid is None:
        print("The actions don't say which project they are for (\"project\")")
        return 2
    projdirs = args.projects or [os.path.join(testdir, "projects")]
    if intests and parts[-4] == prjid:
        projdirs.append(os.sep.join(parts[:-4]))
    events = spec["events"]
    uilevel = spec.get("uilevel")
    name = os.path.splitext(os.path.basename(args.actions))[0] + ".zip"
    if args.output:
        outfile = os.path.abspath(args.output)
    elif intests:
        outfile = os.path.join(cfgdir, name)
    else:
        outfile = None

    work = tempfile.mkdtemp(prefix="mkguitest_")
    try:
        return build(work, projdirs, prjid, cfgid, events, uilevel, outfile, name)
    finally:
        shutil.rmtree(work, ignore_errors=True)

def build(work, projdirs, prjid, cfgid, events, uilevel, outfile, name):
    from ptxprint.main import start_test_display, main as ptxmain
    for d in projdirs:
        src = os.path.join(d, prjid)
        if os.path.isdir(src):
            break
    else:
        print(f"Can't find project {prjid} in {projdirs}")
        return 2
    if outfile is None:
        outfile = os.path.join(src, "shared", "tests", cfgid, name)
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    # PTXprint saves its user settings when it closes: keep them away from the real ones
    os.environ["XDG_CONFIG_HOME"] = os.path.join(work, "config")
    os.environ["XDG_DATA_HOME"] = os.path.join(work, "data")      # GTK's recent files
    os.environ.setdefault("XDG_RUNTIME_DIR", os.path.join(work, "run"))
    os.makedirs(os.environ["XDG_RUNTIME_DIR"], mode=0o700, exist_ok=True)

    server = start_test_display()       # before anything imports Gtk
    if server is None:
        print("Can't start a broadway server. Is broadwayd installed?")
        return 2
    try:
        # replaying a lean test copies the project the same way
        from ptxprint.gtktesting import copyTestProject
        tree = os.path.join(work, "projects")
        copyTestProject(src, os.path.join(tree, prjid))
        from gi.repository import GLib
        from ptxprint.gtkview import GtkViewModel
        from ptxprint.gtktesting import GtkTester

        state = {}
        origrun = GtkViewModel.run

        def startReplay(view):
            if view.testing is None:
                return True         # recording hasn't started yet
            replayer = state['replayer']
            view.testing.events = [list(e) for e in events]
            if uilevel:
                view.testing.uilevel = max(uilevel, view.testing.uilevel)
            GLib.idle_add(replayer.run_action, False)
            return False

        def run(view, callback):
            replayer = GtkTester(None, view)
            replayer.tutorial = True        # no result snapshot: the recorder makes the test
            replayer.startReplayHooks()
            replayer.runevents = events
            replayer.runuilevel = uilevel
            replayer.runextra = {}
            replayer.runeventidx = 0
            view.replayer = replayer
            view.doSysError = replayer.handlerError
            state['replayer'] = replayer
            GLib.timeout_add(100, startReplay, view)
            return origrun(view, callback)
        GtkViewModel.run = run

        argsline = shlex.join(["-q", "-N", "-C", outfile, "--lean", "-p", os.path.dirname(os.path.join(tree, prjid)),
                               "-c", cfgid, prjid])
        sys.argv[1:] = []       # main() parses these as well as argsline
        try:
            ptxmain(argsline=argsline)
        except SystemExit:
            pass
    finally:
        server.terminate()
        server.wait()

    errors = state['replayer'].errors if 'replayer' in state else ["PTXprint did not start"]
    if errors:
        print("The actions could not all be replayed:\n" + "\n".join(errors))
        if os.path.exists(outfile):
            os.unlink(outfile)
        return 1
    if not os.path.exists(outfile):
        print("No test was written")
        return 1
    print(f"Wrote {outfile}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
