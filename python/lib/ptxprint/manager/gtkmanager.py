''' The window of the multi-project management tool: choose a configuration, check it in every
    project, and tick the repairs to make. Nothing in a project changes until Fix is clicked. '''

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GLib
from ptxprint.manager.validate import Validator, ERROR, WARNING, NOTE

ALLCONFIGS = "(all configurations)"
sevLabels = {ERROR: "Error", WARNING: "Warning", NOTE: "Note"}
sevColours = {ERROR: "#C00000", WARNING: "#B06000", NOTE: "#606060"}

# columns of the findings list
(C_TICK, C_CANFIX, C_SEV, C_PROJECT, C_CONFIG, C_MESSAGE, C_FIX, C_COLOUR, C_INDEX, C_WEIGHT) = range(10)

class ManagerWindow(Gtk.Window):

    def __init__(self, projectsDir):
        super().__init__(title="PTXprint Multi-Project Manager")
        self.set_default_size(1150, 700)
        self.findings = []
        self.validator = None
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
        self.notesCheck = Gtk.CheckButton(label="Show notes")
        self.notesCheck.connect("toggled", lambda w: self.fillList())
        top.pack_start(self.notesCheck, False, False, 12)
        self.checkButton = Gtk.Button(label="Check")
        self.checkButton.get_style_context().add_class("suggested-action")
        self.checkButton.connect("clicked", self.onCheck)
        top.pack_end(self.checkButton, False, False, 0)

        mid = Gtk.Paned()
        box.pack_start(mid, True, True, 0)

        # projects to check
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

        # what was found
        self.store = Gtk.ListStore(bool, bool, str, str, str, str, str, str, int, int)
        self.tree = Gtk.TreeView(model=self.store)
        tick = Gtk.CellRendererToggle()
        tick.connect("toggled", self.onFixToggled)
        self.tree.append_column(Gtk.TreeViewColumn("Fix", tick, active=C_TICK, visible=C_CANFIX))
        for title, col, wrap in (("", C_SEV, 0), ("Project", C_PROJECT, 0), ("Configuration", C_CONFIG, 0),
                                 ("What is wrong", C_MESSAGE, 430), ("What Fix will do", C_FIX, 300)):
            r = Gtk.CellRendererText()
            if wrap:
                r.set_property("wrap-width", wrap)
                r.set_property("wrap-mode", Pango.WrapMode.WORD)
            c = Gtk.TreeViewColumn(title, r, text=col, weight=C_WEIGHT)
            if col == C_SEV:
                c.add_attribute(r, "foreground", C_COLOUR)
            c.set_resizable(True)
            self.tree.append_column(c)
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.tree)
        mid.pack2(scroll, True, False)
        mid.set_position(170)

        bottom = Gtk.Box(spacing=6)
        box.pack_start(bottom, False, False, 0)
        self.status = Gtk.Label(label="", xalign=0)
        self.status.set_line_wrap(True)
        bottom.pack_start(self.status, True, True, 0)
        self.fixButton = Gtk.Button(label="Fix ticked")
        self.fixButton.connect("clicked", self.onFix)
        bottom.pack_end(self.fixButton, False, False, 0)
        for label, val in (("Tick none", False), ("Tick the safe ones", True)):
            b = Gtk.Button(label=label)
            b.connect("clicked", self.onTickAll, val)
            bottom.pack_end(b, False, False, 0)

        self.loadProjects(projectsDir)
        self.updateButtons()

    # ---- projects and configurations

    def loadProjects(self, projectsDir):
        self.validator = Validator(projectsDir)
        self.projectStore.clear()
        for prjid, cfgs in self.validator.projectsWithConfigs().items():
            self.projectStore.append([True, prjid, ", ".join(cfgs)])
        self.configCombo.remove_all()
        self.configCombo.append_text(ALLCONFIGS)
        common = self.validator.commonConfigs()
        for name, n in common:
            self.configCombo.append(name, f"{name}   ({n} project{'s' if n != 1 else ''})")
        self.configCombo.set_active(1 if len(common) else 0)
        self.findings = []
        self.fillList()
        self.status.set_text(f"{len(self.projectStore)} projects with PTXprint configurations. "
                             "Choose a configuration and click Check. Nothing is changed until you click Fix.")

    def onConfigChanged(self, w):
        ''' Tick the projects that have this configuration: they are the ones to check '''
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

    # ---- checking

    def onCheck(self, b):
        self.runCheck()

    def runCheck(self, keepStatus=False):
        self.findings = self.validator.validate(self.chosenProjects(), self.chosenConfigs())
        self.fillList()
        if not keepStatus:
            self.status.set_text(self.summary(self.numChecked()))

    def numChecked(self):
        ''' How many of the ticked projects have a configuration that is being checked '''
        cfgs = self.chosenConfigs()
        have = self.validator.projectsWithConfigs()
        return sum(1 for p in self.chosenProjects() if cfgs is None or any(c in have.get(p, []) for c in cfgs))

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

    # ---- fixing

    def onFix(self, b):
        todo = self.tickedFindings()
        if not len(todo):
            return
        dialog = Gtk.MessageDialog(transient_for=self, modal=True, message_type=Gtk.MessageType.QUESTION,
                                   buttons=Gtk.ButtonsType.OK_CANCEL,
                                   text=f"Make {len(todo)} change{'s' if len(todo) != 1 else ''} to the projects' configurations?")
        dialog.format_secondary_text("\n".join(f"{f.project} / {f.config}: {f.fix.description}" for f in todo[:25])
                                     + ("\n..." if len(todo) > 25 else ""))
        ok = dialog.run() == Gtk.ResponseType.OK
        dialog.destroy()
        if ok:
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


def runWindow(projectsDir):
    win = ManagerWindow(projectsDir)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    return 0
