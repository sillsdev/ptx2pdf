''' The two tabs the manager's window has when it is started with --testing, for PTXprint's developers:
      Regression tests  print each test of the suite, compare it with its standard, and accept the right changes
      Test suite        what is tested, with which PTXprint, and the standards
    The work is done by regress.py; this is only the window's side of it. '''

import os, time, threading
from concurrent.futures import ThreadPoolExecutor
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from ptxprint.manager.regress import (TestSuite, RegressionRunner, ResultStore, summarise, statusLabels, ptxprintVersion,
                                      SAME, DIFFERENT, NOSTANDARD, NOCOMPARE, ACCEPTED, NOTRUN, ACCEPTABLE, INSTALLEDEXE)
from ptxprint.manager.testprint import FAILED, STOPPED
from ptxprint.manager.gtkmanager import textColumn, openFile

# columns of the regression tests list
(R_TICK, R_CONFIG, R_PROJECT, R_RESULT, R_TIME, R_DETAIL, R_STANDARD, R_COLOUR, R_WEIGHT, R_STATUS, R_PDF, R_DIFF) = range(12)
# columns of the test suite list
(U_TICK, U_ENABLED, U_CONFIG, U_PROJECT, U_STANDARD, U_VERSION, U_NOTE, U_COLOUR) = range(8)

resultColours = {SAME: "#007000", ACCEPTED: "#007000", DIFFERENT: "#C00000", FAILED: "#C00000", NOSTANDARD: "#B06000",
                 NOCOMPARE: "#B06000", STOPPED: "#606060", NOTRUN: "#606060"}
THISCOPY = "this"
INSTALLED = "installed"

def shortDate(t):
    return time.strftime("%Y-%m-%d", time.localtime(t))

def whenLabel(when):
    ''' "2026-11-14T09:30:00" as "14 Nov 09:30" '''
    try:
        return time.strftime("%d %b %H:%M", time.strptime(when, "%Y-%m-%dT%H:%M:%S"))
    except (ValueError, TypeError):
        return when or ""


class TestingPages:
    ''' Adds the testing tabs to a ManagerWindow and handles them '''

    def __init__(self, win):
        self.win = win
        self.suite = None
        self.results = None
        self.runner = None
        self.runThread = None
        self.rows = {}              # (project, config) -> iter in resultStore
        self.extraKeys = set()      # tests being run that aren't enabled (their standards being recreated)
        self.filling = False        # the settings widgets are being set, not changed by the user
        self.runPage = self.makeRunPage()
        self.suitePage = self.makeSuitePage()
        win.notebook.append_page(self.runPage, Gtk.Label(label="Regression tests"))
        win.notebook.append_page(self.suitePage, Gtk.Label(label="Test suite"))

    @property
    def status(self):
        return self.win.status

    # ---- the pages

    def makeRunPage(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin=6)
        bar = Gtk.Box(spacing=6)
        page.pack_start(bar, False, False, 0)
        self.runAllButton = Gtk.Button(label="Run all")
        self.runAllButton.get_style_context().add_class("suggested-action")
        self.runAllButton.set_tooltip_text("Print every test in the suite that is switched on, and compare each with its standard")
        self.runAllButton.connect("clicked", lambda w: self.startRuns([e.key for e in self.suite.enabled()]))
        bar.pack_start(self.runAllButton, False, False, 0)
        self.runTickedButton = Gtk.Button(label="Run ticked")
        self.runTickedButton.connect("clicked", lambda w: self.startRuns(self.tickedKeys()))
        bar.pack_start(self.runTickedButton, False, False, 0)
        self.stopButton = Gtk.Button(label="Stop")
        self.stopButton.set_sensitive(False)
        self.stopButton.connect("clicked", self.onStop)
        bar.pack_start(self.stopButton, False, False, 0)
        bar.pack_start(Gtk.Label(label="  At once:"), False, False, 0)
        self.jobsSpin = Gtk.SpinButton.new_with_range(1, 32, 1)
        self.jobsSpin.set_tooltip_text("How many to print at the same time")
        self.jobsSpin.connect("value-changed", self.onSettingChanged, "jobs")
        bar.pack_start(self.jobsSpin, False, False, 0)
        self.onlyBadCheck = Gtk.CheckButton(label="Show only differences and failures")
        self.onlyBadCheck.connect("toggled", lambda w: self.resultFilter.refilter())
        bar.pack_start(self.onlyBadCheck, False, False, 12)
        self.acceptButton = Gtk.Button(label="Accept ticked as standard")
        self.acceptButton.set_tooltip_text("Make the ticked tests' new PDFs their standards, without printing again "
                                           "(the old standards are kept as .bak)")
        self.acceptButton.connect("clicked", self.onAccept)
        bar.pack_end(self.acceptButton, False, False, 0)
        for label, handler in (("Open standard", lambda w: self.openSelected("standard")),
                               ("Open new PDF", lambda w: self.openSelected("pdf"))):
            b = Gtk.Button(label=label)
            b.set_tooltip_text("Open the highlighted test's PDF")
            b.connect("clicked", handler)
            bar.pack_end(b, False, False, 0)

        bar = Gtk.Box(spacing=6)
        page.pack_start(bar, False, False, 0)
        bar.pack_start(Gtk.Label(label="Double-click a row to see its differences (or, if there are none to see, its new PDF).",
                                 xalign=0), False, False, 0)
        for label, val in (("Tick none", False), ("Tick different", True)):
            b = Gtk.Button(label=label)
            if val:
                b.set_tooltip_text("Tick the tests whose new PDF differs from its standard, or has none")
            b.connect("clicked", self.onTickResults, val)
            bar.pack_end(b, False, False, 0)

        self.resultStore = Gtk.ListStore(bool, str, str, str, str, str, str, str, int, str, str, str)
        self.resultFilter = self.resultStore.filter_new()
        self.resultFilter.set_visible_func(self.resultVisible)
        self.resultSort = Gtk.TreeModelSort(model=self.resultFilter)
        self.resultTree = Gtk.TreeView(model=self.resultSort)
        tick = Gtk.CellRendererToggle()
        tick.connect("toggled", self.onResultToggled)
        self.resultTree.append_column(Gtk.TreeViewColumn("", tick, active=R_TICK))
        for title, col, wrap, attrs in (("Configuration", R_CONFIG, 0, {}), ("Project", R_PROJECT, 0, {}),
                                        ("Result", R_RESULT, 0, {"foreground": R_COLOUR, "weight": R_WEIGHT}),
                                        ("Time", R_TIME, 0, {}), ("Detail", R_DETAIL, 460, {}),
                                        ("Standard made", R_STANDARD, 0, {})):
            c = textColumn(title, col, wrap, **attrs)
            if col in (R_CONFIG, R_PROJECT, R_RESULT):
                c.set_sort_column_id(col)
            self.resultTree.append_column(c)
        self.resultTree.connect("row-activated", self.onResultActivated)
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.resultTree)
        page.pack_start(scroll, True, True, 0)
        return page

    def makeSuitePage(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin=6)
        bar = Gtk.Box(spacing=6)
        page.pack_start(bar, False, False, 0)
        for label, handler, tip in (
                ("Add ticked projects with this configuration", self.onAddTests,
                 "Add a test of the configuration chosen at the top in each project ticked on the left"),
                ("Find existing standards", self.onFindStandards,
                 "Add a test for each standard PDF (<PRJ>_<CFG>_standard_ptxp.pdf) the projects already have"),
                ("Remove ticked", self.onRemoveTests, "Take the ticked tests out of the suite. Their standard PDFs are left alone.")):
            b = Gtk.Button(label=label)
            b.set_tooltip_text(tip)
            b.connect("clicked", handler)
            bar.pack_start(b, False, False, 0)
        self.recreateButton = Gtk.Button(label="Recreate ticked standards")
        self.recreateButton.set_tooltip_text("Print the ticked tests again and make the new PDFs their standards "
                                             "(the old ones are kept as .bak)")
        self.recreateButton.connect("clicked", self.onRecreate)
        bar.pack_end(self.recreateButton, False, False, 0)
        for label, val in (("Tick none", False), ("Tick all", True)):
            b = Gtk.Button(label=label)
            b.connect("clicked", self.onTickSuite, val)
            bar.pack_end(b, False, False, 0)

        bar = Gtk.Box(spacing=6)
        page.pack_start(bar, False, False, 0)
        bar.pack_start(Gtk.Label(label="Print with:"), False, False, 0)
        self.programCombo = Gtk.ComboBoxText()
        self.programCombo.append(THISCOPY, "This copy of PTXprint")
        self.programCombo.append(INSTALLED, "An installed PTXprint:")
        self.programCombo.connect("changed", self.onProgramChanged)
        bar.pack_start(self.programCombo, False, False, 0)
        self.programChooser = Gtk.FileChooserButton(title="The PTXprint program to test", action=Gtk.FileChooserAction.OPEN)
        self.programChooser.set_width_chars(28)
        self.programChooser.connect("file-set", self.onProgramChanged)
        bar.pack_start(self.programChooser, False, False, 0)
        self.spins = {}
        for label, key, lo, hi, tip in (("  XeTeX runs:", "runs", 1, 9, "How many times XeTeX runs (PTXprint's -R)"),
                                        ("  Max diff pages:", "diffPages", 0, 9999, "How many pages of differences the diff PDF "
                                         "shows at most (0: all)"),
                                        ("  Give up after (minutes):", "timeout", 1, 1440, "Stop a print that takes longer than this")):
            bar.pack_start(Gtk.Label(label=label), False, False, 0)
            s = Gtk.SpinButton.new_with_range(lo, hi, 1)
            s.set_tooltip_text(tip)
            s.connect("value-changed", self.onSettingChanged, key)
            bar.pack_start(s, False, False, 0)
            self.spins[key] = s

        self.suiteStore = Gtk.ListStore(bool, bool, str, str, str, str, str, str)
        self.suiteTree = Gtk.TreeView(model=self.suiteStore)
        tick = Gtk.CellRendererToggle()
        tick.connect("toggled", self.onSuiteToggled, U_TICK)
        self.suiteTree.append_column(Gtk.TreeViewColumn("", tick, active=U_TICK))
        tick = Gtk.CellRendererToggle()
        tick.connect("toggled", self.onSuiteToggled, U_ENABLED)
        c = Gtk.TreeViewColumn("Run", tick, active=U_ENABLED)
        self.suiteTree.append_column(c)
        for title, col in (("Configuration", U_CONFIG), ("Project", U_PROJECT)):
            c = textColumn(title, col)
            c.set_sort_column_id(col)
            self.suiteTree.append_column(c)
        self.suiteTree.append_column(textColumn("Standard", U_STANDARD, foreground=U_COLOUR))
        self.suiteTree.append_column(textColumn("Made with", U_VERSION))
        r = Gtk.CellRendererText()
        r.set_property("editable", True)
        r.connect("edited", self.onNoteEdited)
        c = Gtk.TreeViewColumn("Note", r, text=U_NOTE)
        c.set_resizable(True)
        c.set_min_width(200)
        self.suiteTree.append_column(c)
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.suiteTree)
        page.pack_start(scroll, True, True, 0)
        self.staleLabel = Gtk.Label(label="", xalign=0)
        self.staleLabel.set_line_wrap(True)
        page.pack_start(self.staleLabel, False, False, 0)
        page.pack_start(Gtk.Label(label="'Run' is whether Run all runs it. Click a note to change it. Changes here are saved "
                                        "at once; standards change only when you recreate or accept them.", xalign=0), False, False, 0)
        return page

    # ---- loading

    def load(self, suitePath=None):
        ''' The suite of the window's projects folder, and its last results '''
        self.stop()
        self.extraKeys = set()
        self.suite = TestSuite(self.win.validator, suitePath)
        self.results = ResultStore(self.suite.resultsPath())
        self.fillSettings()
        self.fillResults()
        self.fillSuite()
        if not len(self.suite.entries):
            self.status.set_text("No tests yet: click Find existing standards (in the Test suite tab).")
        else:
            stale = self.staleText()
            if stale:
                self.status.set_text(stale)

    def fillSettings(self):
        s = self.suite.settings
        self.filling = True
        self.jobsSpin.set_value(int(s.get("jobs") or 4))
        self.spins["runs"].set_value(int(s.get("runs") or 1))
        self.spins["diffPages"].set_value(int(s.get("diffPages") or 0))
        self.spins["timeout"].set_value(max(1, int(s.get("timeout") or 3600) // 60))
        program = s.get("program") or ""
        self.programCombo.set_active_id(INSTALLED if program else THISCOPY)
        if program:
            self.programChooser.set_filename(program)
        elif os.path.exists(INSTALLEDEXE):
            self.programChooser.set_filename(INSTALLEDEXE)
        self.programChooser.set_sensitive(bool(program))
        self.filling = False

    def version(self):
        return ptxprintVersion(self.suite.settings.get("program") or "")

    def staleText(self):
        ''' Says if standards were made with another PTXprint than the one that is testing, or "" '''
        version = self.version()
        old, unknown = self.suite.staleStandards(version)
        if not len(old):
            return ""
        n = sum(old.values())
        made = ", ".join(f"{v}" for v in sorted(old))
        return (f"{n} standard{'s were' if n != 1 else ' was'} made with {made}; this is {version or 'another version'}. "
                "After checking a full run, recreate or accept them.")

    # ---- the regression tests list

    def resultRow(self, key):
        e = self.suite.find(*key)
        res = self.results.get(*key)
        made = self.suite.standardTime(*key)
        std = "none yet" if made is None else shortDate(made) + (f" ({e.standardVersion})" if e is not None and e.standardVersion else "")
        if res is None:
            return [False, key[1], key[0], statusLabels[NOTRUN], "", "", std, resultColours[NOTRUN], 400, NOTRUN, "", ""]
        return [False, key[1], key[0], statusLabels.get(res.status, res.status), f"{res.seconds:.0f}s, {whenLabel(res.when)}",
                self.detail(res), std, resultColours.get(res.status, "#000000"),
                700 if res.status in (DIFFERENT, FAILED) else 400, res.status, res.pdf or "", res.diff or ""]

    def detail(self, res):
        if res.status == DIFFERENT and res.diff and not res.message.startswith("differences"):
            return ("differences: double-click to see them. " + res.message).strip()
        return res.message

    def fillResults(self):
        ticked = set(self.tickedKeys()) if len(self.resultStore) else set()
        self.resultStore.clear()
        self.rows = {}
        keys = [e.key for e in self.suite.enabled()] + [k for k in self.extraKeys if (self.suite.find(*k) is None or
                                                                                      not self.suite.find(*k).enabled)]
        for key in keys:
            row = self.resultRow(key)
            row[R_TICK] = key in ticked
            self.rows[key] = self.resultStore.append(row)
        self.updateButtons()

    def updateRow(self, key, running=None):
        titer = self.rows.get(key)
        if titer is None or not self.resultStore.iter_is_valid(titer):
            return
        row = self.resultStore[titer]
        if running is not None:
            row[R_RESULT] = running
            row[R_COLOUR] = "#606060"
            row[R_WEIGHT] = 400
            return
        tick = row[R_TICK]
        vals = self.resultRow(key)
        vals[R_TICK] = tick
        self.resultStore.set_row(titer, vals)

    def resultVisible(self, model, titer, data=None):
        if not self.onlyBadCheck.get_active():
            return True
        return model[titer][R_STATUS] in (DIFFERENT, FAILED, NOSTANDARD, NOCOMPARE)

    def storePath(self, path):
        ''' The path in resultStore of a path in the (sorted, filtered) list '''
        fpath = self.resultSort.convert_path_to_child_path(Gtk.TreePath(path))
        return None if fpath is None else self.resultFilter.convert_path_to_child_path(fpath)

    def onResultToggled(self, r, path):
        spath = self.storePath(path)
        if spath is not None:
            self.resultStore[spath][R_TICK] = not self.resultStore[spath][R_TICK]
            self.updateButtons()

    def onTickResults(self, b, val):
        for row in self.resultStore:
            row[R_TICK] = val and row[R_STATUS] in ACCEPTABLE
        self.updateButtons()

    def tickedKeys(self):
        return [(r[R_PROJECT], r[R_CONFIG]) for r in self.resultStore if r[R_TICK]]

    def acceptableKeys(self):
        return [(r[R_PROJECT], r[R_CONFIG]) for r in self.resultStore if r[R_TICK] and r[R_STATUS] in ACCEPTABLE and r[R_PDF]]

    def selectedRow(self):
        model, titer = self.resultTree.get_selection().get_selected()
        return None if titer is None else model[titer]

    def openSelected(self, which):
        row = self.selectedRow()
        if row is None:
            self.status.set_text("Click on a test first.")
            return
        path = row[R_PDF] if which == "pdf" else self.suite.standardPath(row[R_PROJECT], row[R_CONFIG])
        if path and os.path.exists(path):
            openFile(path)
        else:
            self.status.set_text(f"{row[R_PROJECT]} / {row[R_CONFIG]} has no {'new PDF' if which == 'pdf' else 'standard'} to open.")

    def onResultActivated(self, tree, path, col):
        row = tree.get_model()[path]
        for p in (row[R_DIFF], row[R_PDF]):
            if p and os.path.exists(p):
                openFile(p)
                return

    # ---- running

    def startRuns(self, keys, recreate=False):
        if self.runThread is not None:
            self.status.set_text("Tests are already running.")
            return False
        keys = list(dict.fromkeys(keys))        # each once
        if not len(keys):
            self.status.set_text("Tick the tests to run." if len(self.suite.entries) else
                                 "No tests yet: click Find existing standards (in the Test suite tab).")
            return False
        self.extraKeys = set(keys)
        self.fillResults()
        for k in keys:
            self.updateRow(k, running="Waiting")
        self.runner = RegressionRunner(self.suite, self.results)
        runner = self.runner
        self.runDone = []
        self.runTotal = len(keys)
        self.recreating = recreate
        workers = max(1, self.jobsSpin.get_value_as_int())
        self.status.set_text(f"{'Recreating the standards of' if recreate else 'Running'} {len(keys)} "
                             f"test{'s' if len(keys) != 1 else ''}, {workers} at once...")

        def one(key):
            GLib.idle_add(self.updateRow, key, "Printing...")
            res = runner.recreate(*key) if recreate else runner.run(*key)
            GLib.idle_add(self.showResult, key, res)

        def work():
            with ThreadPoolExecutor(max_workers=workers) as pool:
                list(pool.map(one, keys))
            GLib.idle_add(self.runsFinished)

        self.runThread = threading.Thread(target=work, daemon=True)
        self.runThread.start()
        self.updateButtons()
        return True

    def showResult(self, key, res):
        self.runDone.append(res)
        if res.status == STOPPED or "already" in res.message:
            # nothing new was kept: show what is
            self.updateRow(key)
            titer = self.rows.get(key)
            if titer is not None and self.resultStore.iter_is_valid(titer):
                self.resultStore[titer][R_RESULT] = statusLabels[res.status]
                self.resultStore[titer][R_DETAIL] = res.message
        else:
            self.updateRow(key)
        if not self.runner.stopping:
            self.status.set_text(f"Done {len(self.runDone)} of {self.runTotal}: {summarise(self.runDone)}.")
        return False

    def runsFinished(self):
        self.runThread = None
        msg = summarise(self.runDone) + "."
        if any(r.status in ACCEPTABLE for r in self.runDone):
            msg += " Look at each difference, then tick and Accept the ones that are right."
        self.status.set_text(msg)
        self.fillSuite()
        self.updateButtons()
        return False

    def onStop(self, b):
        if self.runner is not None and self.runThread is not None:
            self.runner.stop()
            self.status.set_text("Stopping...")

    def stop(self):
        if self.runner is not None:
            self.runner.stop()

    def onAccept(self, b):
        keys = self.acceptableKeys()
        if len(keys) and self.win.confirm(f"Make {len(keys)} new PDF{'s' if len(keys) != 1 else ''} the standard?",
                [f"{p} / {c}: {os.path.basename(self.results.get(p, c).pdf)}" for p, c in keys]
                + ["", "The old standards are kept as .bak."]):
            self.accept(keys)

    def accept(self, keys):
        runner = self.runner or RegressionRunner(self.suite, self.results)
        done = 0
        failed = []
        for key in keys:
            try:
                runner.accept(*key)
                done += 1
            except (ValueError, OSError) as e:
                failed.append(f"{key[0]}/{key[1]}: {e}")
            self.updateRow(key)
        self.fillSuite()
        self.updateButtons()
        msg = f"Made {done} new PDF{'s' if done != 1 else ''} the standard."
        if len(failed):
            msg += f" {len(failed)} could not be: " + "; ".join(failed[:3])
        self.status.set_text(msg)
        return done, failed

    # ---- the test suite

    def fillSuite(self):
        if self.suite is None:
            return
        ticked = {(r[U_PROJECT], r[U_CONFIG]) for r in self.suiteStore if r[U_TICK]}
        self.suiteStore.clear()
        for e in self.suite.entries:
            made = self.suite.standardTime(*e.key)
            self.suiteStore.append([e.key in ticked, e.enabled, e.config, e.project,
                                    "none yet" if made is None else shortDate(made), e.standardVersion, e.note,
                                    "#B06000" if made is None else "#000000"])
        self.staleLabel.set_text(self.staleText())
        self.updateButtons()

    def onSuiteToggled(self, r, path, col):
        row = self.suiteStore[path]
        row[col] = not row[col]
        if col == U_ENABLED:
            e = self.suite.find(row[U_PROJECT], row[U_CONFIG])
            if e is not None:
                e.enabled = row[col]
                self.save()
                if self.runThread is None:
                    self.fillResults()
        self.updateButtons()

    def onTickSuite(self, b, val):
        for row in self.suiteStore:
            row[U_TICK] = val
        self.updateButtons()

    def onNoteEdited(self, r, path, text):
        row = self.suiteStore[path]
        e = self.suite.find(row[U_PROJECT], row[U_CONFIG])
        if e is not None and e.note != text.strip():
            e.note = text.strip()
            row[U_NOTE] = e.note
            self.save()

    def tickedSuiteKeys(self):
        return [(r[U_PROJECT], r[U_CONFIG]) for r in self.suiteStore if r[U_TICK]]

    def save(self):
        try:
            self.suite.save()
            return True
        except OSError as e:
            self.status.set_text(f"Could not save {self.suite.path}: {e}")
            return False

    def onAddTests(self, b):
        pairs = self.win.chosenPairs()
        new = [p for p in pairs if self.suite.find(*p) is None]
        if not len(pairs):
            self.status.set_text("Tick the projects (on the left) that have the configuration chosen at the top.")
            return
        if self.win.chosenConfigs() is None and len(new) and not self.win.confirm(
                f"Add {len(new)} tests: every configuration of the ticked projects?", [f"{p} / {c}" for p, c in new]):
            return
        self.addTests(pairs)

    def addTests(self, pairs):
        added = [p for p in pairs if self.suite.add(*p) is not None]
        if len(added):
            self.save()
        self.fillSuite()
        if self.runThread is None:
            self.fillResults()
        self.status.set_text(f"Added {len(added)} test{'s' if len(added) != 1 else ''}"
                             + (f" ({len(pairs) - len(added)} were there already)" if len(pairs) > len(added) else "")
                             + ". Those with no standard yet: run them, look at the PDF, and accept it.")
        return len(added)

    def onFindStandards(self, b):
        self.findStandards()

    def findStandards(self):
        found = self.suite.findStandards()
        for p in found:
            self.suite.add(*p)
        if len(found):
            self.save()
        self.fillSuite()
        if self.runThread is None:
            self.fillResults()
        self.status.set_text(f"Found {len(found)} standard{'s' if len(found) != 1 else ''} not in the suite, and added "
                             f"{'them' if len(found) != 1 else 'it'}. The suite has {len(self.suite.entries)} tests."
                             if len(found) else f"There are no standards that aren't in the suite already "
                             f"({len(self.suite.entries)} tests).")
        return len(found)

    def onRemoveTests(self, b):
        keys = self.tickedSuiteKeys()
        if len(keys) and self.win.confirm(f"Take {len(keys)} test{'s' if len(keys) != 1 else ''} out of the suite?",
                                          [f"{p} / {c}" for p, c in keys] + ["", "Their standard PDFs are left alone."]):
            self.removeTests(keys)

    def removeTests(self, keys):
        n = self.suite.remove(keys)
        if n:
            self.save()
        self.fillSuite()
        if self.runThread is None:
            self.fillResults()
        self.status.set_text(f"Took {n} test{'s' if n != 1 else ''} out of the suite. Their standard PDFs are left alone.")
        return n

    def onRecreate(self, b):
        keys = self.tickedSuiteKeys()
        if not len(keys):
            return
        if self.runThread is not None:
            self.status.set_text("Wait for the tests that are running to finish, or stop them.")
            return
        if self.win.confirm(f"Print {len(keys)} test{'s' if len(keys) != 1 else ''} again and make the new PDFs the standards?",
                            [f"{p} / {c}" for p, c in keys] + ["", "The old standards are kept as .bak."]):
            self.win.notebook.set_current_page(self.win.notebook.page_num(self.runPage))
            self.startRuns(keys, recreate=True)

    def onProgramChanged(self, w):
        if self.filling:
            return
        installed = self.programCombo.get_active_id() == INSTALLED
        self.programChooser.set_sensitive(installed)
        program = (self.programChooser.get_filename() or "") if installed else ""
        if installed and not program:
            self.status.set_text("Choose the PTXprint program, e.g. " + INSTALLEDEXE)
            return
        self.suite.settings["program"] = program
        self.save()
        self.fillSuite()
        v = self.version()
        self.status.set_text(f"Tests will print with {'this copy of PTXprint' if not program else program}"
                             + (f" ({v})." if v else "."))

    def onSettingChanged(self, w, key):
        if self.filling or self.suite is None:
            return
        v = w.get_value_as_int()
        self.suite.settings[key] = v * 60 if key == "timeout" else v
        self.save()

    def updateButtons(self):
        if self.suite is None:
            return
        running = self.runThread is not None
        n = len(self.acceptableKeys())
        self.acceptButton.set_label(f"Accept ticked as standard ({n})")
        self.acceptButton.set_sensitive(n > 0 and not running)
        n = len(self.tickedSuiteKeys())
        self.recreateButton.set_label(f"Recreate ticked standards ({n})")
        self.recreateButton.set_sensitive(n > 0 and not running)
        self.runAllButton.set_sensitive(not running)
        self.runTickedButton.set_sensitive(not running and len(self.tickedKeys()) > 0)
        self.stopButton.set_sensitive(running)
