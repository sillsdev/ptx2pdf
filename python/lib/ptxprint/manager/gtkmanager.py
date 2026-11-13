''' The window of the multi-project management tool. Choose a configuration and the projects, then:
      Problems      check it in every project, and tick the repairs to make
      Diglot texts  choose the other project(s) each diglot is printed beside
      Test print    have PTXprint print a book in every project, and see which fail
    Nothing in a project's settings changes until the user clicks a button that says so. '''

import os, threading
from concurrent.futures import ThreadPoolExecutor
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GLib
from ptxprint.manager.validate import Validator, ERROR, WARNING, NOTE
from ptxprint.manager.testprint import TestPrinter, PRINTED, FAILED, SKIPPED, STOPPED

ALLCONFIGS = "(all configurations)"
sevLabels = {ERROR: "Error", WARNING: "Warning", NOTE: "Note"}
sevColours = {ERROR: "#C00000", WARNING: "#B06000", NOTE: "#606060"}

# columns of the problems list
(C_TICK, C_CANFIX, C_SEV, C_PROJECT, C_CONFIG, C_MESSAGE, C_FIX, C_COLOUR, C_INDEX, C_WEIGHT) = range(10)
# columns of the diglot texts list
(D_PROJECT, D_CONFIG, D_SIDE, D_NOWPRJ, D_NOWCFG, D_NEWPRJ, D_NEWCFG, D_CFGMODEL, D_NOTE, D_WEIGHT, D_COLOUR) = range(11)
# columns of the test print list
(T_PROJECT, T_CONFIG, T_RESULT, T_TIME, T_MESSAGE, T_COLOUR, T_PDF, T_WEIGHT) = range(8)

printLabels = {PRINTED: "Printed", FAILED: "FAILED", SKIPPED: "Not tried", STOPPED: "Stopped"}
printColours = {PRINTED: "#007000", FAILED: "#C00000", SKIPPED: "#606060", STOPPED: "#606060"}

def textColumn(title, col, wrap=0, **attrs):
    r = Gtk.CellRendererText()
    if wrap:
        r.set_property("wrap-width", wrap)
        r.set_property("wrap-mode", Pango.WrapMode.WORD)
    c = Gtk.TreeViewColumn(title, r, text=col, **attrs)
    c.set_resizable(True)
    return c

def openFile(path):
    if hasattr(os, "startfile"):
        os.startfile(path)
    else:
        import subprocess
        subprocess.Popen(["xdg-open", path])


class ManagerWindow(Gtk.Window):

    def __init__(self, projectsDir):
        super().__init__(title="PTXprint Multi-Project Manager")
        self.set_default_size(1200, 720)
        self.findings = []
        self.validator = None
        self.printer = None
        self.printThread = None
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin=8)
        self.add(box)

        top = Gtk.Box(spacing=6)
        box.pack_start(top, False, False, 0)
        top.pack_start(Gtk.Label(label="Projects folder:"), False, False, 0)
        self.dirButton = Gtk.FileChooserButton(title="Folder the Paratext projects are in",
                                               action=Gtk.FileChooserAction.SELECT_FOLDER)
        self.dirButton.set_filename(projectsDir)
        self.dirButton.connect("file-set", self.onDirChosen)
        top.pack_start(self.dirButton, False, False, 0)
        top.pack_start(Gtk.Label(label="   Configuration:"), False, False, 0)
        self.configCombo = Gtk.ComboBoxText()
        self.configCombo.connect("changed", self.onConfigChanged)
        top.pack_start(self.configCombo, False, False, 0)

        mid = Gtk.Paned()
        box.pack_start(mid, True, True, 0)

        # projects to work on
        self.projectStore = Gtk.ListStore(bool, str, str)       # ticked, project, its configs
        ptree = Gtk.TreeView(model=self.projectStore)
        tick = Gtk.CellRendererToggle()
        tick.connect("toggled", self.onProjectToggled)
        ptree.append_column(Gtk.TreeViewColumn("", tick, active=0))
        ptree.append_column(Gtk.TreeViewColumn("Project", Gtk.CellRendererText(), text=1))
        ptree.set_tooltip_column(2)
        pscroll = Gtk.ScrolledWindow()
        pscroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        pscroll.add(ptree)
        pbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        pbox.pack_start(pscroll, True, True, 0)
        allBox = Gtk.Box(spacing=4)
        for label, val in (("All", True), ("None", False)):
            b = Gtk.Button(label=label)
            b.connect("clicked", self.onAllProjects, val)
            allBox.pack_start(b, True, True, 0)
        pbox.pack_start(allBox, False, False, 0)
        mid.pack1(pbox, False, False)

        self.notebook = Gtk.Notebook()
        mid.pack2(self.notebook, True, False)
        mid.set_position(170)
        self.notebook.append_page(self.makeProblemsPage(), Gtk.Label(label="Problems"))
        self.notebook.append_page(self.makeDiglotPage(), Gtk.Label(label="Diglot texts"))
        self.notebook.append_page(self.makePrintPage(), Gtk.Label(label="Test print"))

        self.status = Gtk.Label(label="", xalign=0)
        self.status.set_line_wrap(True)
        box.pack_start(self.status, False, False, 0)
        self.connect("destroy", self.onDestroy)

        self.loadProjects(projectsDir)
        self.updateButtons()

    # ---- the pages

    def makeProblemsPage(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin=6)
        bar = Gtk.Box(spacing=6)
        page.pack_start(bar, False, False, 0)
        self.checkButton = Gtk.Button(label="Check")
        self.checkButton.get_style_context().add_class("suggested-action")
        self.checkButton.connect("clicked", self.onCheck)
        bar.pack_start(self.checkButton, False, False, 0)
        self.notesCheck = Gtk.CheckButton(label="Show notes")
        self.notesCheck.connect("toggled", lambda w: self.fillList())
        bar.pack_start(self.notesCheck, False, False, 12)
        self.fixButton = Gtk.Button(label="Fix ticked")
        self.fixButton.connect("clicked", self.onFix)
        bar.pack_end(self.fixButton, False, False, 0)
        for label, val in (("Tick none", False), ("Tick the safe ones", True)):
            b = Gtk.Button(label=label)
            b.connect("clicked", self.onTickAll, val)
            bar.pack_end(b, False, False, 0)
        self.store = Gtk.ListStore(bool, bool, str, str, str, str, str, str, int, int)
        self.tree = Gtk.TreeView(model=self.store)
        tick = Gtk.CellRendererToggle()
        tick.connect("toggled", self.onFixToggled)
        self.tree.append_column(Gtk.TreeViewColumn("Fix", tick, active=C_TICK, visible=C_CANFIX))
        self.tree.append_column(textColumn("", C_SEV, weight=C_WEIGHT, foreground=C_COLOUR))
        self.tree.append_column(textColumn("Project", C_PROJECT, weight=C_WEIGHT))
        self.tree.append_column(textColumn("Configuration", C_CONFIG, weight=C_WEIGHT))
        self.tree.append_column(textColumn("What is wrong", C_MESSAGE, 430, weight=C_WEIGHT))
        self.tree.append_column(textColumn("What Fix will do", C_FIX, 300, weight=C_WEIGHT))
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.tree)
        page.pack_start(scroll, True, True, 0)
        return page

    def makeDiglotPage(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin=6)
        bar = Gtk.Box(spacing=6)
        page.pack_start(bar, False, False, 0)
        b = Gtk.Button(label="Show")
        b.get_style_context().add_class("suggested-action")
        b.connect("clicked", lambda w: self.fillDiglots())
        bar.pack_start(b, False, False, 0)
        bar.pack_start(Gtk.Label(label="Click in 'Change to project' to choose a different project for a diglot's other text."),
                       False, False, 6)
        self.applyButton = Gtk.Button(label="Apply changes")
        self.applyButton.connect("clicked", self.onApplyDiglots)
        bar.pack_end(self.applyButton, False, False, 0)
        # one row for each other text (R, and A, B... of a polyglot) of each diglot config
        self.diglotStore = Gtk.ListStore(str, str, str, str, str, str, str, Gtk.ListStore, str, int, str)
        self.projectChoices = Gtk.ListStore(str)
        self.diglotTree = Gtk.TreeView(model=self.diglotStore)
        self.diglotTree.append_column(textColumn("Project", D_PROJECT))
        self.diglotTree.append_column(textColumn("Configuration", D_CONFIG))
        self.diglotTree.append_column(textColumn("Text", D_SIDE))
        self.diglotTree.append_column(textColumn("Is now project", D_NOWPRJ, foreground=D_COLOUR))
        self.diglotTree.append_column(textColumn("configuration", D_NOWCFG))
        r = Gtk.CellRendererCombo()
        r.set_property("model", self.projectChoices)
        r.set_property("text-column", 0)
        r.set_property("has-entry", False)
        r.set_property("editable", True)
        r.connect("changed", self.onDiglotProjectChosen)
        c = Gtk.TreeViewColumn("Change to project", r, text=D_NEWPRJ, weight=D_WEIGHT)
        c.set_min_width(150)
        self.diglotTree.append_column(c)
        r = Gtk.CellRendererCombo()
        r.set_property("text-column", 0)
        r.set_property("has-entry", False)
        r.set_property("editable", True)
        r.connect("changed", self.onDiglotConfigChosen)
        c = Gtk.TreeViewColumn("configuration", r, text=D_NEWCFG, model=D_CFGMODEL, weight=D_WEIGHT)
        c.set_min_width(130)
        self.diglotTree.append_column(c)
        self.diglotTree.append_column(textColumn("", D_NOTE, 330))
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.diglotTree)
        page.pack_start(scroll, True, True, 0)
        return page

    def makePrintPage(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin=6)
        bar = Gtk.Box(spacing=6)
        page.pack_start(bar, False, False, 0)
        bar.pack_start(Gtk.Label(label="Book(s) to print:"), False, False, 0)
        self.bookEntry = Gtk.Entry()
        self.bookEntry.set_text("3JN")
        self.bookEntry.set_width_chars(16)
        self.bookEntry.set_tooltip_text("The book to print in every ticked project, e.g. 3JN. Several books, e.g. JAS GLO, "
                                        "are printed together as one PDF. A short book is quickest.")
        self.bookEntry.connect("activate", self.onTestPrint)
        bar.pack_start(self.bookEntry, False, False, 0)
        self.printButton = Gtk.Button(label="Test print")
        self.printButton.get_style_context().add_class("suggested-action")
        self.printButton.connect("clicked", self.onTestPrint)
        bar.pack_start(self.printButton, False, False, 0)
        self.stopButton = Gtk.Button(label="Stop")
        self.stopButton.connect("clicked", self.onStopPrint)
        self.stopButton.set_sensitive(False)
        bar.pack_start(self.stopButton, False, False, 0)
        bar.pack_start(Gtk.Label(label="Double-click a printed row to open its PDF."), False, False, 12)
        self.printStore = Gtk.ListStore(str, str, str, str, str, str, str, int)
        self.printTree = Gtk.TreeView(model=self.printStore)
        self.printTree.append_column(textColumn("Project", T_PROJECT))
        self.printTree.append_column(textColumn("Configuration", T_CONFIG))
        self.printTree.append_column(textColumn("Result", T_RESULT, foreground=T_COLOUR, weight=T_WEIGHT))
        self.printTree.append_column(textColumn("Time", T_TIME))
        self.printTree.append_column(textColumn("Why", T_MESSAGE, 620))
        self.printTree.connect("row-activated", self.onPrintRowActivated)
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.printTree)
        page.pack_start(scroll, True, True, 0)
        return page

    # ---- projects and configurations

    def loadProjects(self, projectsDir):
        self.validator = Validator(projectsDir)
        self.projectStore.clear()
        self.projectChoices.clear()
        for prjid, cfgs in self.validator.projectsWithConfigs().items():
            self.projectStore.append([True, prjid, ", ".join(cfgs)])
            self.projectChoices.append([prjid])
        self.configCombo.remove_all()
        self.configCombo.append_text(ALLCONFIGS)
        common = self.validator.commonConfigs()
        for name, n in common:
            self.configCombo.append(name, f"{name}   ({n} project{'s' if n != 1 else ''})")
        self.configCombo.set_active(1 if len(common) else 0)
        self.findings = []
        self.fillList()
        self.diglotStore.clear()
        self.printStore.clear()
        self.status.set_text(f"{len(self.projectStore)} projects with PTXprint configurations. "
                             "Choose a configuration and click Check. Nothing is changed until you click Fix.")

    def onConfigChanged(self, w):
        ''' Tick the projects that have this configuration: they are the ones to work on '''
        if self.validator is None:
            return
        cfgs = self.chosenConfigs()
        have = self.validator.projectsWithConfigs()
        for row in self.projectStore:
            row[0] = cfgs is None or any(c in have.get(row[1], []) for c in cfgs)

    def onDirChosen(self, w):
        self.loadProjects(w.get_filename())

    def onProjectToggled(self, r, path):
        self.projectStore[path][0] = not self.projectStore[path][0]

    def onAllProjects(self, b, val):
        for row in self.projectStore:
            row[0] = val

    def chosenProjects(self):
        return [r[1] for r in self.projectStore if r[0]]

    def chosenConfigs(self):
        cid = self.configCombo.get_active_id()
        return None if cid is None else [cid]

    def chosenPairs(self):
        ''' The (project, config) pairs being worked on '''
        cfgs = self.chosenConfigs()
        have = self.validator.projectsWithConfigs()
        return [(p, c) for p in self.chosenProjects() for c in have.get(p, []) if cfgs is None or c in cfgs]

    # ---- problems

    def onCheck(self, b):
        self.runCheck()

    def runCheck(self, keepStatus=False):
        self.findings = self.validator.validate(self.chosenProjects(), self.chosenConfigs())
        self.fillList()
        if not keepStatus:
            self.status.set_text(self.summary(self.numChecked()))

    def numChecked(self):
        ''' How many of the ticked projects have a configuration that is being checked '''
        return len(set(p for p, c in self.chosenPairs()))

    def summary(self, nprojects):
        n = {s: sum(1 for f in self.findings if f.severity == s) for s in (ERROR, WARNING, NOTE)}
        fixable = sum(1 for f in self.findings if f.fix is not None)
        if not len(self.findings):
            return f"Checked {nprojects} projects: nothing wrong was found."
        return (f"Checked {nprojects} projects: {n[ERROR]} errors, {n[WARNING]} warnings, {n[NOTE]} notes. "
                f"{fixable} can be fixed here: tick the ones you want and click Fix.")

    def fillList(self):
        self.store.clear()
        showNotes = self.notesCheck.get_active()
        for i, f in enumerate(self.findings):
            if f.severity == NOTE and not showNotes and f.fix is None:
                continue
            self.store.append([f.fix is not None and f.fix.safe, f.fix is not None, sevLabels[f.severity], f.project, f.config,
                               f.message, "" if f.fix is None else f.fix.description + ("" if f.fix.safe else "\n(your choice)"),
                               sevColours[f.severity], i, 700 if f.severity == ERROR else 400])
        self.updateButtons()

    def onFixToggled(self, r, path):
        if self.store[path][C_CANFIX]:
            self.store[path][C_TICK] = not self.store[path][C_TICK]
            self.updateButtons()

    def onTickAll(self, b, val):
        for row in self.store:
            if row[C_CANFIX]:
                row[C_TICK] = val and self.findings[row[C_INDEX]].fix.safe
        self.updateButtons()

    def tickedFindings(self):
        return [self.findings[r[C_INDEX]] for r in self.store if r[C_CANFIX] and r[C_TICK]]

    def updateButtons(self):
        n = len(self.tickedFindings())
        self.fixButton.set_label(f"Fix ticked ({n})")
        self.fixButton.set_sensitive(n > 0)
        n = len(self.diglotChanges())
        self.applyButton.set_label(f"Apply changes ({n})")
        self.applyButton.set_sensitive(n > 0)

    def confirm(self, text, lines):
        dialog = Gtk.MessageDialog(transient_for=self, modal=True, message_type=Gtk.MessageType.QUESTION,
                                   buttons=Gtk.ButtonsType.OK_CANCEL, text=text)
        dialog.format_secondary_text("\n".join(lines[:25]) + ("\n..." if len(lines) > 25 else ""))
        ok = dialog.run() == Gtk.ResponseType.OK
        dialog.destroy()
        return ok

    def onFix(self, b):
        todo = self.tickedFindings()
        if len(todo) and self.confirm(f"Make {len(todo)} change{'s' if len(todo) != 1 else ''} to the projects' configurations?",
                                      [f"{f.project} / {f.config}: {f.fix.description}" for f in todo]):
            self.applyFixes(todo)

    def applyFixes(self, todo):
        done = 0
        failed = []
        for f in todo:
            try:
                f.fix.apply()
                done += 1
            except Exception as e:
                failed.append(f"{f.project}/{f.config}: {e}")
        self.runCheck(keepStatus=True)
        msg = f"Made {done} change{'s' if done != 1 else ''}. " + self.summary(self.numChecked())
        if len(failed):
            msg = f"{len(failed)} could not be made ({'; '.join(failed[:3])}). " + msg
        self.status.set_text(msg)

    # ---- diglot texts

    def configChoices(self, prjid):
        res = Gtk.ListStore(str)
        if prjid in self.validator.projects:
            for c in self.validator.configNames(prjid):
                res.append([c])
        return res

    def fillDiglots(self):
        self.diglotStore.clear()
        ndiglots = 0
        for prjid, cfg in self.chosenPairs():
            sides = self.validator.diglotSides(prjid, cfg)
            if len(sides):
                ndiglots += 1
            expected = self.validator.expectedSecondary(prjid)
            for side in sorted(k for k in sides if k != "L"):
                (sprj, scfg) = sides[side]
                note = ""
                colour = "#000000"
                if sprj not in self.validator.projects:
                    note = f"There is no project {sprj} here."
                    colour = "#C00000"
                elif scfg not in self.validator.configNames(sprj):
                    note = f"{sprj} has no configuration {scfg}."
                    colour = "#C00000"
                if side == "R" and expected and expected != sprj:
                    note = (note + " " if note else "") + f"The project's own settings name {expected}."
                self.diglotStore.append([prjid, cfg, side, sprj, scfg, sprj, scfg, self.configChoices(sprj), note, 400, colour])
        self.updateButtons()
        if not ndiglots:
            self.status.set_text("None of the ticked projects' configurations is a diglot or polyglot.")
        else:
            self.status.set_text(f"{ndiglots} diglot or polyglot configuration{'s' if ndiglots != 1 else ''}. "
                                 "Nothing is changed until you click Apply changes.")

    def markDiglotRow(self, row):
        row[D_WEIGHT] = 700 if (row[D_NEWPRJ], row[D_NEWCFG]) != (row[D_NOWPRJ], row[D_NOWCFG]) else 400
        self.updateButtons()

    def setDiglotProject(self, path, newprj):
        row = self.diglotStore[path]
        if newprj == row[D_PROJECT]:
            self.status.set_text("A diglot can't have the same project on both sides.")
            return
        row[D_NEWPRJ] = newprj
        row[D_CFGMODEL] = self.configChoices(newprj)
        # the same configuration name there as was used before, or as this diglot's own
        row[D_NEWCFG] = self.validator.bestConfig(newprj, [row[D_NOWCFG], row[D_CONFIG]]) or ""
        self.markDiglotRow(row)

    def onDiglotProjectChosen(self, r, path, citer):
        self.setDiglotProject(path, self.projectChoices[citer][0])

    def onDiglotConfigChosen(self, r, path, citer):
        row = self.diglotStore[path]
        row[D_NEWCFG] = row[D_CFGMODEL][citer][0]
        self.markDiglotRow(row)

    def diglotChanges(self):
        ''' Returns [(project, config, side, new project, new config)] the user has chosen '''
        return [(r[D_PROJECT], r[D_CONFIG], r[D_SIDE], r[D_NEWPRJ], r[D_NEWCFG]) for r in self.diglotStore
                if (r[D_NEWPRJ], r[D_NEWCFG]) != (r[D_NOWPRJ], r[D_NOWCFG]) and r[D_NEWCFG]]

    def onApplyDiglots(self, b):
        todo = self.diglotChanges()
        if len(todo) and self.confirm(f"Make {len(todo)} change{'s' if len(todo) != 1 else ''} to the diglots' other texts?",
                                      [f"{p} / {c}: the {s} text becomes {np}, {nc}" for p, c, s, np, nc in todo]):
            self.applyDiglots(todo)

    def applyDiglots(self, todo):
        failed = []
        for (p, c, s, np, nc) in todo:
            try:
                self.validator.setDiglotSide(p, c, s, np, nc)
            except (ValueError, OSError) as e:
                failed.append(f"{p}/{c}: {e}")
        self.fillDiglots()
        if len(self.findings):
            self.runCheck(keepStatus=True)
        self.status.set_text(f"Made {len(todo) - len(failed)} change{'s' if len(todo) - len(failed) != 1 else ''}."
                             + (f" {len(failed)} could not be made: {'; '.join(failed[:3])}" if len(failed) else ""))

    # ---- test print

    def onTestPrint(self, b):
        if self.printThread is not None:
            return
        books = self.bookEntry.get_text().strip()
        pairs = self.chosenPairs()
        probe = TestPrinter(self.validator)
        if not len(probe.booksIn(books)):
            self.status.set_text("Type the book to print, e.g. 3JN.")
            return
        if not len(pairs):
            self.status.set_text("Tick the projects to print.")
            return
        if self.chosenConfigs() is None and len(pairs) > 30 and not self.confirm(
                    f"Print {books} with all {len(pairs)} configurations?", ["This may take a long time."]):
            return
        self.startTestPrint(pairs, books)

    def startTestPrint(self, pairs, books, workers=3):
        self.printStore.clear()
        rows = {}
        for (p, c) in pairs:
            rows[(p, c)] = self.printStore.append([p, c, "Waiting", "", "", "#606060", "", 400])
        self.printer = TestPrinter(self.validator)
        self.printButton.set_sensitive(False)
        self.stopButton.set_sensitive(True)
        self.printCounts = {PRINTED: 0, FAILED: 0, SKIPPED: 0, STOPPED: 0}
        self.status.set_text(f"Printing {books} in {len(pairs)} project configuration{'s' if len(pairs) != 1 else ''}...")
        printer = self.printer

        def one(pair):
            GLib.idle_add(self.showPrinting, rows[pair])
            res = printer.run(pair[0], pair[1], books)
            GLib.idle_add(self.showPrintResult, rows[pair], res)

        def work():
            with ThreadPoolExecutor(max_workers=workers) as pool:
                list(pool.map(one, pairs))
            GLib.idle_add(self.printsFinished, books)

        self.printThread = threading.Thread(target=work, daemon=True)
        self.printThread.start()

    def showPrinting(self, titer):
        if self.printStore.iter_is_valid(titer) and self.printStore[titer][T_RESULT] == "Waiting":
            self.printStore[titer][T_RESULT] = "Printing..."
        return False

    def showPrintResult(self, titer, res):
        self.printCounts[res.status] += 1
        if self.printStore.iter_is_valid(titer):
            row = self.printStore[titer]
            row[T_RESULT] = printLabels[res.status]
            row[T_TIME] = f"{res.seconds:.0f}s" if res.seconds else ""
            row[T_MESSAGE] = res.message
            row[T_COLOUR] = printColours[res.status]
            row[T_PDF] = res.pdf or ""
            row[T_WEIGHT] = 700 if res.status == FAILED else 400
        return False

    def printsFinished(self, books):
        self.printThread = None
        self.printButton.set_sensitive(True)
        self.stopButton.set_sensitive(False)
        n = self.printCounts
        msg = f"Test print of {books}: {n[PRINTED]} printed, {n[FAILED]} failed"
        if n[SKIPPED]:
            msg += f", {n[SKIPPED]} not tried"
        if n[STOPPED]:
            msg += f", {n[STOPPED]} stopped"
        self.status.set_text(msg + ".")
        return False

    def onStopPrint(self, b):
        if self.printer is not None:
            self.printer.stop()
            self.status.set_text("Stopping...")

    def onPrintRowActivated(self, tree, path, col):
        pdf = self.printStore[path][T_PDF]
        if pdf and os.path.exists(pdf):
            openFile(pdf)

    def onDestroy(self, w):
        if self.printer is not None:
            self.printer.stop()


def runWindow(projectsDir):
    win = ManagerWindow(projectsDir)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    return 0
