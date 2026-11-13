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
from ptxprint.manager.publications import PublicationTable, MAIN, validBooks
from ptxprint.manager.compare import Comparison, NOTSET
from ptxprint.manager.styles import StyleComparison, COMMONEST, GROUPS

SAME = "·"             # a middle dot: the same as what it is compared with
MOSTLABEL = "(what most have)"
ACROSSPROJECTS = "projects"
ACROSSCONFIGS = "configs"
# fixed columns of the styles list; a column for each configuration compared follows
(S_TICK, S_MARKER, S_ATTR, S_BASE, S_INDEX, S_NFIXED) = range(6)

MAINLABEL = "(main variables)"
INHERITED = "#909090"       # a publication's value that is just the config's own
# fixed columns of the publications list; a value and a colour column for each variable follow
(P_TICK, P_PROJECT, P_CONFIG, P_PUBID, P_LABEL, P_BOOKS, P_STATE, P_WEIGHT, P_ISPUB, P_CANPRINT, P_NFIXED) = range(11)
# columns of the compare list
(X_TICK, X_SETTING, X_PROJECT, X_VALUE, X_REFVALUE, X_INDEX, X_ONESIDED) = range(7)

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
        self.notebook.append_page(self.makePublicationsPage(), Gtk.Label(label="Publications"))
        self.notebook.append_page(self.makeComparePage(), Gtk.Label(label="Compare settings"))
        self.notebook.append_page(self.makeStylesPage(), Gtk.Label(label="Compare styles"))

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

    def makePublicationsPage(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin=6)
        bar = Gtk.Box(spacing=6)
        page.pack_start(bar, False, False, 0)
        b = Gtk.Button(label="Show")
        b.get_style_context().add_class("suggested-action")
        b.connect("clicked", lambda w: self.fillPublications(reload=True))
        bar.pack_start(b, False, False, 0)
        for label, handler, tip in (
                ("Add publication...", self.onAddPublication, "Add a publication to every ticked project's configuration"),
                ("Delete", self.onDeletePublications, "Delete the highlighted publication(s)"),
                ("Add column...", self.onAddPubColumn, "Show another variable, so that publications can have their own value of it")):
            b = Gtk.Button(label=label)
            b.set_tooltip_text(tip)
            b.connect("clicked", handler)
            bar.pack_start(b, False, False, 0)
        self.pubApplyButton = Gtk.Button(label="Apply changes")
        self.pubApplyButton.connect("clicked", self.onApplyPublications)
        bar.pack_end(self.pubApplyButton, False, False, 0)
        self.pubPrintButton = Gtk.Button(label="Print ticked")
        self.pubPrintButton.set_tooltip_text("Have PTXprint print the ticked publications, each with its own books and variables")
        self.pubPrintButton.connect("clicked", self.onPrintPublications)
        bar.pack_end(self.pubPrintButton, False, False, 0)
        self.pubTree = Gtk.TreeView()
        self.pubTree.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.pubScroll = Gtk.ScrolledWindow()
        self.pubScroll.add(self.pubTree)
        page.pack_start(self.pubScroll, True, True, 0)
        page.pack_start(Gtk.Label(label="Click a value to change it. Grey values are the configuration's own (main) "
                                        "variables, which a publication uses unless it is given its own.", xalign=0), False, False, 0)
        self.pubTable = None
        self.pubStore = None
        self.pubColumns = []
        self.pubExtraColumns = []
        self.resetPubChanges()
        return page

    def makeComparePage(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin=6)
        bar = Gtk.Box(spacing=6)
        page.pack_start(bar, False, False, 0)
        bar.pack_start(Gtk.Label(label="Compare with:"), False, False, 0)
        self.refCombo = Gtk.ComboBoxText()
        self.refCombo.set_tooltip_text("The project whose settings the others are compared with, and copied from")
        bar.pack_start(self.refCombo, False, False, 0)
        b = Gtk.Button(label="Compare")
        b.get_style_context().add_class("suggested-action")
        b.connect("clicked", lambda w: self.runCompare())
        bar.pack_start(b, False, False, 0)
        bar.pack_start(Gtk.Label(label="  Find:"), False, False, 0)
        self.compareFind = Gtk.Entry()
        self.compareFind.set_width_chars(14)
        self.compareFind.set_tooltip_text("Show only the rows with this in them, e.g. margin, or a project's name")
        self.compareFind.connect("changed", lambda w: self.refilterCompare())
        bar.pack_start(self.compareFind, False, False, 0)
        self.oneSidedCheck = Gtk.CheckButton(label="Also where only one has the setting")
        self.oneSidedCheck.set_tooltip_text("A configuration last saved by an older PTXprint doesn't have the newer settings. "
                                            "PTXprint uses its default for them, which is usually the same thing.")
        self.oneSidedCheck.connect("toggled", lambda w: self.refilterCompare())
        bar.pack_start(self.oneSidedCheck, False, False, 6)
        self.copyButton = Gtk.Button(label="Copy ticked")
        self.copyButton.connect("clicked", self.onCopySettings)
        bar.pack_end(self.copyButton, False, False, 0)
        for label, val in (("Tick none", False), ("Tick shown", True)):
            b = Gtk.Button(label=label)
            b.connect("clicked", self.onTickCompare, val)
            bar.pack_end(b, False, False, 0)
        self.comparison = None
        self.differences = []
        self.compareStore = Gtk.ListStore(bool, str, str, str, str, int, bool)
        self.compareFilter = self.compareStore.filter_new()
        self.compareFilter.set_visible_func(self.compareRowVisible)
        self.compareTree = Gtk.TreeView(model=self.compareFilter)
        tick = Gtk.CellRendererToggle()
        tick.connect("toggled", self.onCompareToggled)
        self.compareTree.append_column(Gtk.TreeViewColumn("Copy", tick, active=X_TICK))
        self.compareTree.append_column(textColumn("Setting", X_SETTING))
        self.compareTree.append_column(textColumn("Project", X_PROJECT))
        self.compareTree.append_column(textColumn("Has", X_VALUE, 330))
        self.compareRefColumn = textColumn("Reference has", X_REFVALUE, 330)
        self.compareTree.append_column(self.compareRefColumn)
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.compareTree)
        page.pack_start(scroll, True, True, 0)
        page.pack_start(Gtk.Label(label="Settings that belong to a project (its variables, publications, diglot texts, books, "
                                        "included PDFs) are not compared. Nor are styles.", xalign=0), False, False, 0)
        return page

    def makeStylesPage(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin=6)
        bar = Gtk.Box(spacing=6)
        page.pack_start(bar, False, False, 0)
        self.styleMode = Gtk.ComboBoxText()
        self.styleMode.append(ACROSSPROJECTS, "This configuration in the ticked projects")
        self.styleMode.append(ACROSSCONFIGS, "The configurations of one project:")
        self.styleMode.set_active_id(ACROSSPROJECTS)
        self.styleMode.connect("changed", self.onStyleModeChanged)
        bar.pack_start(self.styleMode, False, False, 0)
        self.styleProject = Gtk.ComboBoxText()
        self.styleProject.connect("changed", self.onStyleProjectChanged)
        bar.pack_start(self.styleProject, False, False, 0)
        self.styleConfigs = Gtk.Entry()
        self.styleConfigs.set_width_chars(30)
        self.styleConfigs.set_tooltip_text("The configurations of that project to compare, with spaces between them")
        bar.pack_start(self.styleConfigs, False, False, 0)
        b = Gtk.Button(label="Compare")
        b.get_style_context().add_class("suggested-action")
        b.connect("clicked", lambda w: self.runStyleCompare())
        bar.pack_start(b, False, False, 0)

        bar = Gtk.Box(spacing=6)
        page.pack_start(bar, False, False, 0)
        bar.pack_start(Gtk.Label(label="Compare with:"), False, False, 0)
        self.styleRef = Gtk.ComboBoxText()
        self.styleRef.set_tooltip_text("What each is compared with: the value most of them have, or one of them")
        self.styleRef.connect("changed", lambda w: self.fillStyles())
        bar.pack_start(self.styleRef, False, False, 0)
        bar.pack_start(Gtk.Label(label="  Show:"), False, False, 0)
        self.styleGroup = Gtk.ComboBoxText()
        self.styleGroup.append("", "All styles")
        for g in GROUPS:
            self.styleGroup.append(g, g)
        self.styleGroup.set_active(0)
        self.styleGroup.connect("changed", lambda w: self.fillStyles())
        bar.pack_start(self.styleGroup, False, False, 0)
        bar.pack_start(Gtk.Label(label="  Find:"), False, False, 0)
        self.styleFind = Gtk.Entry()
        self.styleFind.set_width_chars(12)
        self.styleFind.set_tooltip_text("Show only the rows with this in the style or attribute, e.g. fontsize, or s1")
        self.styleFind.connect("changed", lambda w: self.fillStyles())
        bar.pack_start(self.styleFind, False, False, 0)
        self.styleStrays = Gtk.CheckButton(label="Only where one or two differ")
        self.styleStrays.set_tooltip_text("The quickest way to find the configuration that is out of step")
        self.styleStrays.connect("toggled", lambda w: self.fillStyles())
        bar.pack_start(self.styleStrays, False, False, 6)
        self.styleNonVisual = Gtk.CheckButton(label="Also names and structure")
        self.styleNonVisual.set_tooltip_text("Name, description, where a style may occur, and such, which don't change how a page looks")
        self.styleNonVisual.connect("toggled", lambda w: self.fillStyles())
        bar.pack_start(self.styleNonVisual, False, False, 0)

        bar = Gtk.Box(spacing=6)
        page.pack_start(bar, False, False, 0)
        self.styleCopyButton = Gtk.Button(label="Copy ticked")
        self.styleCopyButton.set_tooltip_text("Give the ticked rows' out of step configurations the 'Compare with' value, "
                                              "by changing their ptxprint.sty")
        self.styleCopyButton.connect("clicked", self.onCopyStyles)
        bar.pack_end(self.styleCopyButton, False, False, 0)
        self.styleCopyTo = Gtk.ComboBoxText()
        self.styleCopyTo.set_tooltip_text("Which of the configurations to change")
        self.styleCopyTo.connect("changed", lambda w: self.updateButtons())
        bar.pack_end(self.styleCopyTo, False, False, 0)
        bar.pack_end(Gtk.Label(label="in:"), False, False, 0)
        for label, handler, tip in (
                ("Tick none", lambda w: self.tickStyles(False), None),
                ("Tick whole style", self.onTickWholeStyle, "Tick every row shown for the highlighted row's style"),
                ("Tick shown", lambda w: self.tickStyles(True), "Tick the rows shown, except fonts and cover styles: tick those yourself")):
            b = Gtk.Button(label=label)
            if tip:
                b.set_tooltip_text(tip)
            b.connect("clicked", handler)
            bar.pack_end(b, False, False, 0)
        bar.pack_start(Gtk.Label(label="To bring configurations into line, tick the rows and click Copy ticked.", xalign=0), False, False, 0)
        self.styleTicked = set()        # (marker, attribute) of the ticked rows

        self.styleComparison = None
        self.styleDiffs = []
        self.styleShown = []
        self.styleTree = Gtk.TreeView()
        self.styleTree.set_property("has-tooltip", True)
        self.styleTree.connect("query-tooltip", self.onStyleTooltip)
        self.styleTree.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.styleTree)
        page.pack_start(scroll, True, True, 0)
        page.pack_start(Gtk.Label(label=f"A dot ({SAME}) is the same as the 'Compare with' value. Point at a value to see which file "
                                        "it comes from. What is compared is what prints: the defaults, then custom.sty, "
                                        "ptxprint.sty and ptxprint-mods.sty.", xalign=0), False, False, 0)
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
        self.compareStore.clear()
        self.differences = []
        self.pubTable = None
        self.resetPubChanges()
        self.pubTree.set_model(None)
        self.styleComparison = None
        self.styleDiffs = []
        self.styleTree.set_model(None)
        self.styleProject.remove_all()
        for prjid in self.validator.projectsWithConfigs():
            self.styleProject.append(prjid, prjid)
        self.onStyleModeChanged(None)
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
        # the projects this configuration can be compared with
        was = self.refCombo.get_active_id()
        self.refCombo.remove_all()
        if cfgs is not None:
            names = [p for p in have if cfgs[0] in have[p]]
            for p in names:
                self.refCombo.append(p, p)
            if len(names):
                self.refCombo.set_active_id(was if was in names else names[0])

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
        n = self.numPubChanges()
        self.pubApplyButton.set_label(f"Apply changes ({n})")
        self.pubApplyButton.set_sensitive(n > 0)
        n = sum(1 for r in self.compareStore if r[X_TICK])
        self.copyButton.set_label(f"Copy ticked ({n})")
        self.copyButton.set_sensitive(n > 0)
        if self.styleComparison is not None:
            todo, columns = self.styleCopyPlan()
            n = sum(1 for d in todo for c in d.differing if columns is None or c in columns)
        else:
            n = 0
        self.styleCopyButton.set_label(f"Copy ticked ({n})")
        self.styleCopyButton.set_sensitive(n > 0)

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

    # ---- publications

    def resetPubChanges(self):
        self.pubEdits = {}          # (project, config, pubid, key) -> new value
        self.pubAdds = {}           # (project, config, pubid) -> books
        self.pubDeletes = set()     # (project, config, pubid)

    def numPubChanges(self):
        return len(self.pubEdits) + len(self.pubAdds) + len(self.pubDeletes)

    def pubValue(self, prjid, cfg, pubid, key):
        ''' Returns (the value to show, whether it is the publication's own) with pending changes '''
        if (prjid, cfg, pubid, key) in self.pubEdits:
            return self.pubEdits[(prjid, cfg, pubid, key)], True
        c = self.pubTable.configs[(prjid, cfg)]
        if key == "__books":
            return (self.pubAdds[(prjid, cfg, pubid)] if (prjid, cfg, pubid) in self.pubAdds else c.booksOf(pubid)), True
        if pubid == MAIN:
            return c.variables.get(key, ""), True
        if key in c.pubs.get(pubid, {}):
            return c.pubs[pubid][key], True
        main = self.pubEdits.get((prjid, cfg, MAIN, key), c.variables.get(key, ""))
        return main, False

    def fillPublications(self, reload=False):
        if reload or self.pubTable is None:
            if self.numPubChanges() and not self.confirm("Forget the changes that have not been applied?",
                                                         [f"{self.numPubChanges()} changes to publications"]):
                return
            self.pubTable = PublicationTable(self.validator, self.chosenPairs())
            self.resetPubChanges()
        table = self.pubTable
        self.pubColumns = table.columns() + [k for k in self.pubExtraColumns if k not in table.columns()]
        ncols = len(self.pubColumns)
        self.pubStore = Gtk.ListStore(*([bool, str, str, str, str, str, str, int, bool, bool] + [str] * (2 * ncols)))
        rows = list(table.rows())
        for (prjid, cfg, pubid) in self.pubAdds:
            if (prjid, cfg) in table.configs:
                at = max(i for i, r in enumerate(rows) if r[:2] == (prjid, cfg))
                rows.insert(at + 1, (prjid, cfg, pubid))
        for (prjid, cfg, pubid) in rows:
            key = (prjid, cfg, pubid)
            state = "new" if key in self.pubAdds else ("will be deleted" if key in self.pubDeletes else "")
            changed = state != "" or any(k[:3] == key for k in self.pubEdits)
            vals = []
            cols = []
            for k in self.pubColumns:
                v, own = self.pubValue(prjid, cfg, pubid, k)
                vals.append(v)
                cols.append("#000000" if own else INHERITED)
            self.pubStore.append([False, prjid, cfg, pubid, MAINLABEL if pubid == MAIN else pubid,
                                  self.pubValue(prjid, cfg, pubid, "__books")[0], state, 700 if changed else 400,
                                  pubid != MAIN, pubid != MAIN and state == ""] + vals + cols)
        for c in self.pubTree.get_columns():
            self.pubTree.remove_column(c)
        tick = Gtk.CellRendererToggle()
        tick.connect("toggled", self.onPubTicked)
        self.pubTree.append_column(Gtk.TreeViewColumn("Print", tick, active=P_TICK, visible=P_CANPRINT))
        self.pubTree.append_column(textColumn("Project", P_PROJECT, weight=P_WEIGHT))
        self.pubTree.append_column(textColumn("Configuration", P_CONFIG, weight=P_WEIGHT))
        self.pubTree.append_column(textColumn("Publication", P_LABEL, weight=P_WEIGHT))
        r = Gtk.CellRendererText()
        r.connect("edited", self.onPubCellEdited, "__books")
        c = Gtk.TreeViewColumn("Books", r, text=P_BOOKS, weight=P_WEIGHT, editable=P_ISPUB)
        c.set_resizable(True)
        self.pubTree.append_column(c)
        for i, k in enumerate(self.pubColumns):
            r = Gtk.CellRendererText()
            r.set_property("editable", True)
            r.set_property("ellipsize", Pango.EllipsizeMode.END)
            r.connect("edited", self.onPubCellEdited, k)
            c = Gtk.TreeViewColumn(k, r, text=P_NFIXED + i, foreground=P_NFIXED + ncols + i, weight=P_WEIGHT)
            c.set_resizable(True)
            c.set_min_width(110 if "title" not in k else 220)
            self.pubTree.append_column(c)
        self.pubTree.append_column(textColumn("", P_STATE))
        self.pubTree.set_model(self.pubStore)
        self.updateButtons()
        npubs = sum(len(c.pubs) for c in table.configs.values())
        self.status.set_text(f"{len(table.configs)} configurations with {npubs} publication{'s' if npubs != 1 else ''}. "
                             "Nothing is changed until you click Apply changes.")

    def onPubTicked(self, r, path):
        if self.pubStore[path][P_CANPRINT]:
            self.pubStore[path][P_TICK] = not self.pubStore[path][P_TICK]

    def onPubCellEdited(self, r, path, text, key):
        row = self.pubStore[path]
        self.editPublication(row[P_PROJECT], row[P_CONFIG], row[P_PUBID], key, text)

    def editPublication(self, prjid, cfg, pubid, key, text):
        ''' Records a change (it is made by Apply) '''
        text = text.strip()
        ident = (prjid, cfg, pubid)
        if ident in self.pubDeletes:
            return
        if key == "__books":
            if pubid == MAIN:
                return
            if not validBooks(text):
                self.status.set_text(f"'{text}' isn't a list of books. Use book codes, e.g. JAS or JAS GLO or MAT-JHN.")
                return
            if ident in self.pubAdds:
                self.pubAdds[ident] = text.upper()
                self.fillPublications()
                return
            text = text.upper()
        c = self.pubTable.configs[(prjid, cfg)]
        if key == "__books":
            orig = c.booksOf(pubid)
        elif pubid == MAIN:
            orig = c.variables.get(key, "")
        else:
            orig = c.pubs.get(pubid, {}).get(key, None)         # None: it has no value of its own
            if orig is None and text == c.variables.get(key, "") and (prjid, cfg, pubid, key) not in self.pubEdits:
                return                                          # left as it was: still the main value
        if text == orig:
            self.pubEdits.pop((prjid, cfg, pubid, key), None)
        else:
            self.pubEdits[(prjid, cfg, pubid, key)] = text
        self.fillPublications()

    def askFields(self, title, fields):
        ''' fields: [(label, initial value or list of choices)]. Returns the values, or None '''
        dialog = Gtk.Dialog(title=title, transient_for=self, modal=True)
        dialog.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "OK", Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)
        grid = Gtk.Grid(column_spacing=8, row_spacing=6, margin=10)
        dialog.get_content_area().add(grid)
        widgets = []
        for i, (label, init) in enumerate(fields):
            grid.attach(Gtk.Label(label=label, xalign=0), 0, i, 1, 1)
            if isinstance(init, list):
                w = Gtk.ComboBoxText()
                for v in init:
                    w.append(v, v)
                w.set_active(0)
            else:
                w = Gtk.Entry()
                w.set_text(init)
                w.set_width_chars(34)
                w.set_activates_default(True)
            grid.attach(w, 1, i, 1, 1)
            widgets.append(w)
        dialog.show_all()
        ok = dialog.run() == Gtk.ResponseType.OK
        res = [w.get_active_id() if isinstance(w, Gtk.ComboBoxText) else w.get_text().strip() for w in widgets]
        dialog.destroy()
        return res if ok else None

    def onAddPublication(self, b):
        if self.pubTable is None:
            self.fillPublications(reload=True)
        if self.pubTable is None or not len(self.pubTable.configs):
            self.status.set_text("Tick the projects to add a publication to.")
            return
        n = len(self.pubTable.configs)
        res = self.askFields(f"Add a publication to {n} configuration{'s' if n != 1 else ''}",
                             [("Name of the publication:", ""), ("Its books (e.g. JAS or JAS GLO):", "")])
        if res is not None:
            self.addPublication(res[0], res[1])

    def addPublication(self, name, books):
        ''' A new publication in every config being shown that doesn't have one of that name '''
        name = name.strip()
        if not name or any(ch in name for ch in "[]\n\\/:*?\"<>|"):
            self.status.set_text("Give the publication a name (it becomes part of the PDF's file name, so no \\ / : * ? \" < > |).")
            return 0
        if not validBooks(books):
            self.status.set_text(f"'{books}' isn't a list of books. Use book codes, e.g. JAS or JAS GLO.")
            return 0
        added = 0
        for (prjid, cfg), c in self.pubTable.configs.items():
            if name not in c.pubs and (prjid, cfg, name) not in self.pubAdds:
                self.pubAdds[(prjid, cfg, name)] = books.strip().upper()
                added += 1
        self.fillPublications()
        self.status.set_text(f"'{name}' will be added to {added} configuration{'s' if added != 1 else ''} when you click Apply changes. "
                             "Fill in its titles first.")
        return added

    def onDeletePublications(self, b):
        model, paths = self.pubTree.get_selection().get_selected_rows()
        self.deletePublications([(model[p][P_PROJECT], model[p][P_CONFIG], model[p][P_PUBID]) for p in paths])

    def deletePublications(self, idents):
        for ident in idents:
            if ident[2] == MAIN:
                continue
            if ident in self.pubAdds:
                del self.pubAdds[ident]
            elif ident in self.pubDeletes:
                self.pubDeletes.discard(ident)      # a second Delete changes its mind
            else:
                self.pubDeletes.add(ident)
            for k in [k for k in self.pubEdits if k[:3] == ident]:
                del self.pubEdits[k]
        self.fillPublications()

    def onAddPubColumn(self, b):
        if self.pubTable is None:
            self.fillPublications(reload=True)
        choices = [k for k in self.pubTable.otherVariables() if k not in self.pubExtraColumns] if self.pubTable else []
        if not len(choices):
            self.status.set_text("There are no other variables to show.")
            return
        res = self.askFields("Show another variable", [("Variable:", choices)])
        if res is not None and res[0]:
            self.pubExtraColumns.append(res[0])
            self.fillPublications()

    def publicationChangeLines(self):
        lines = [f"{p} / {c}: add publication '{pub}' ({books})" for (p, c, pub), books in self.pubAdds.items()]
        lines += [f"{p} / {c}: delete publication '{pub}'" for (p, c, pub) in sorted(self.pubDeletes)]
        lines += [f"{p} / {c} / {pub or MAINLABEL}: {'books' if k == '__books' else k} = {v}"
                  for (p, c, pub, k), v in self.pubEdits.items()]
        return lines

    def onApplyPublications(self, b):
        n = self.numPubChanges()
        if n and self.confirm(f"Make {n} change{'s' if n != 1 else ''} to the publications and variables?",
                              self.publicationChangeLines()):
            self.applyPublications()

    def applyPublications(self):
        failed = []
        done = 0
        for (prjid, cfg), c in self.pubTable.configs.items():
            edits = [(k[2], k[3], v) for k, v in self.pubEdits.items() if k[:2] == (prjid, cfg)]
            adds = [(k[2], books) for k, books in self.pubAdds.items() if k[:2] == (prjid, cfg)]
            deletes = [k[2] for k in self.pubDeletes if k[:2] == (prjid, cfg)]
            if not (edits or adds or deletes):
                continue
            try:
                c.apply(edits, adds, deletes)
                done += len(edits) + len(adds) + len(deletes)
            except (ValueError, OSError) as e:
                failed.append(f"{prjid}/{cfg}: {e}")
        self.resetPubChanges()
        self.fillPublications(reload=True)
        self.status.set_text(f"Made {done} change{'s' if done != 1 else ''}."
                             + (f" Some could not be made: {'; '.join(failed[:3])}" if len(failed) else ""))

    def onPrintPublications(self, b):
        if self.pubStore is None:
            return
        if self.numPubChanges():
            self.status.set_text("Apply the changes first, so that what is printed is what you see.")
            return
        jobs = [(r[P_PROJECT], r[P_CONFIG], r[P_PUBID]) for r in self.pubStore if r[P_TICK] and r[P_CANPRINT]]
        if not len(jobs):
            self.status.set_text("Tick the publications to print, in the Print column.")
            return
        if self.printThread is not None:
            self.status.set_text("A print is already running.")
            return
        self.notebook.set_current_page(2)
        self.startTestPrint(jobs, None)

    # ---- compare settings

    def runCompare(self):
        cfgs = self.chosenConfigs()
        ref = self.refCombo.get_active_id()
        self.compareStore.clear()
        self.differences = []
        if cfgs is None or ref is None:
            self.status.set_text("Choose one configuration (at the top) and the project to compare the others with.")
            self.updateButtons()
            return
        self.comparison = Comparison(self.validator, cfgs[0], ref)
        others = [p for p in self.chosenProjects() if p != ref]
        self.differences = self.comparison.differences(others)
        self.compareRefColumn.set_title(f"{ref} has")
        for i, d in enumerate(self.differences):
            self.compareStore.append([False, d.setting, d.project, "(not set)" if d.value is NOTSET else d.value,
                                      "(not set)" if d.refValue is NOTSET else d.refValue, i, d.oneSided])
        self.refilterCompare()
        both = sum(1 for d in self.differences if not d.oneSided)
        nprj = len(set(d.project for d in self.differences if not d.oneSided))
        self.status.set_text(f"{cfgs[0]}: {both} settings differ from {ref} in {nprj} project{'s' if nprj != 1 else ''} "
                             f"({len(self.differences) - both} more where only one has the setting). "
                             "Tick the ones to bring into line and click Copy ticked.")

    def compareRowVisible(self, model, titer, data=None):
        if model[titer][X_ONESIDED] and not self.oneSidedCheck.get_active():
            return False
        find = self.compareFind.get_text().strip().lower()
        if not find:
            return True
        return any(find in (model[titer][c] or "").lower() for c in (X_SETTING, X_PROJECT, X_VALUE, X_REFVALUE))

    def refilterCompare(self):
        self.compareFilter.refilter()
        self.updateButtons()

    def onCompareToggled(self, r, path):
        row = self.compareStore[self.compareFilter.convert_path_to_child_path(Gtk.TreePath(path))]
        row[X_TICK] = not row[X_TICK]
        self.updateButtons()

    def onTickCompare(self, b, val):
        if val:
            for frow in self.compareFilter:
                self.compareStore[self.compareFilter.convert_iter_to_child_iter(frow.iter)][X_TICK] = True
        else:
            for row in self.compareStore:
                row[X_TICK] = False
        self.updateButtons()

    def tickedDifferences(self):
        return [self.differences[r[X_INDEX]] for r in self.compareStore if r[X_TICK]]

    def onCopySettings(self, b):
        todo = self.tickedDifferences()
        ref = self.comparison.reference
        if len(todo) and self.confirm(f"Copy {len(todo)} setting{'s' if len(todo) != 1 else ''} from {ref}?",
                [f"{d.project}: {d.setting} = {'(not set)' if d.refValue is NOTSET else d.refValue}" for d in todo]):
            self.copySettings(todo)

    def copySettings(self, todo):
        try:
            done = self.comparison.copy(todo)
        except OSError as e:
            self.status.set_text(f"Could not copy: {e}")
            return
        self.runCompare()
        self.status.set_text(f"Copied {done} setting{'s' if done != 1 else ''} from {self.comparison.reference}. "
                             "Test print to check the result.")

    # ---- compare styles

    def onStyleModeChanged(self, w):
        configs = self.styleMode.get_active_id() == ACROSSCONFIGS
        self.styleProject.set_sensitive(configs)
        self.styleConfigs.set_sensitive(configs)
        if configs and self.styleProject.get_active_id() is None:
            ticked = self.chosenProjects()
            if len(ticked):
                self.styleProject.set_active_id(ticked[0])

    def onStyleProjectChanged(self, w):
        ''' Offer the project's most widely used configurations '''
        prjid = self.styleProject.get_active_id()
        if prjid is None or self.validator is None:
            return
        have = self.validator.configNames(prjid)
        common = [c for c, n in self.validator.commonConfigs() if c in have and c != "Default"]
        self.styleConfigs.set_text(" ".join(common[:4]))

    def runStyleCompare(self):
        if self.styleMode.get_active_id() == ACROSSCONFIGS:
            prjid = self.styleProject.get_active_id()
            if prjid is None:
                self.status.set_text("Choose the project whose configurations are to be compared.")
                return
            wanted = self.styleConfigs.get_text().replace(",", " ").split()
            missing = [c for c in wanted if c not in self.validator.configNames(prjid)]
            if len(missing):
                self.status.set_text(f"{prjid} has no configuration called {', '.join(missing)}.")
                return
            self.compareStyles(StyleComparison.acrossConfigs(self.validator, prjid, wanted), f"{prjid}'s configurations")
        else:
            cfgs = self.chosenConfigs()
            if cfgs is None:
                self.status.set_text("Choose one configuration (at the top) to compare across the ticked projects.")
                return
            self.compareStyles(StyleComparison.acrossProjects(self.validator, cfgs[0], self.chosenProjects()), cfgs[0])

    def compareStyles(self, comparison, what):
        if len(comparison.columns) < 2:
            self.status.set_text("There need to be at least two to compare.")
            return
        self.styleComparison = comparison
        self.styleWhat = what
        self.styleRefFilling = True         # filling the list isn't the user choosing from it
        self.styleRef.remove_all()
        self.styleRef.append("", MOSTLABEL)
        for c in comparison.columns:
            self.styleRef.append(c, c)
        self.styleRef.set_active(0)
        self.styleCopyTo.remove_all()
        self.styleCopyTo.append("", "all that differ")
        for c in comparison.columns:
            self.styleCopyTo.append(c, c)
        self.styleCopyTo.set_active(0)
        self.styleRefFilling = False
        self.styleTicked = set()
        self.fillStyles()

    def styleRowShown(self, d):
        if not d.visual and not self.styleNonVisual.get_active():
            return False
        if self.styleStrays.get_active() and len(d.differing) > 2:
            return False
        group = self.styleGroup.get_active_id()
        if group and d.group != group:
            return False
        find = self.styleFind.get_text().strip().lower()
        if find and find not in d.marker.lower() and find not in d.attr:
            return False
        return True

    def fillStyles(self):
        comp = self.styleComparison
        if comp is None or getattr(self, "styleRefFilling", False):
            return
        ref = self.styleRef.get_active_id() or COMMONEST
        self.styleDiffs = comp.differences(reference=ref)
        self.styleShown = [d for d in self.styleDiffs if self.styleRowShown(d)]
        ncols = len(comp.columns)
        store = Gtk.ListStore(*([bool, str, str, str, int] + [str] * ncols))
        for i, d in enumerate(self.styleShown):
            store.append([(d.marker, d.attr) in self.styleTicked, d.marker, d.attr, d.baseline.shown(d.attr), i]
                         + [d.values[c].shown(d.attr) if c in d.differing else SAME for c in comp.columns])
        for c in self.styleTree.get_columns():
            self.styleTree.remove_column(c)
        tick = Gtk.CellRendererToggle()
        tick.connect("toggled", self.onStyleTicked)
        self.styleTree.append_column(Gtk.TreeViewColumn("Copy", tick, active=S_TICK))
        self.styleTree.append_column(textColumn("Style", S_MARKER))
        self.styleTree.append_column(textColumn("Attribute", S_ATTR))
        self.styleTree.append_column(textColumn("Most have" if ref is COMMONEST else f"{ref} has", S_BASE))
        for i, c in enumerate(comp.columns):
            r = Gtk.CellRendererText()
            r.set_property("ellipsize", Pango.EllipsizeMode.END)
            col = Gtk.TreeViewColumn(c, r, text=S_NFIXED + i)
            col.set_resizable(True)
            col.set_min_width(64)
            self.styleTree.append_column(col)
        self.styleTree.set_model(store)
        self.updateButtons()
        visual = [d for d in self.styleDiffs if d.visual]
        nstyles = len(set(d.marker for d in visual))
        self.status.set_text(f"{self.styleWhat}: {len(visual)} style attributes differ, in {nstyles} styles "
                             f"({len(self.styleDiffs) - len(visual)} more in names and structure). Showing {len(self.styleShown)}.")

    def onStyleTicked(self, r, path):
        row = self.styleTree.get_model()[path]
        row[S_TICK] = not row[S_TICK]
        key = (row[S_MARKER], row[S_ATTR])
        if row[S_TICK]:
            self.styleTicked.add(key)
        else:
            self.styleTicked.discard(key)
        self.updateButtons()

    def tickStyles(self, val, marker=None):
        ''' Tick (or untick) the rows shown, or those of one style. Fonts and cover styles are a
            project's or a publication's own more often than not, so "all" leaves them for the user. '''
        if not val:
            self.styleTicked = set()
        else:
            for d in self.styleShown:
                if marker is not None:
                    if d.marker == marker:
                        self.styleTicked.add((d.marker, d.attr))
                elif d.visual and d.group != "Cover" and "font" not in d.attr.replace("fontsize", "").replace("fontscale", ""):
                    self.styleTicked.add((d.marker, d.attr))
        self.fillStyles()

    def onTickWholeStyle(self, b):
        model, titer = self.styleTree.get_selection().get_selected()
        if titer is None:
            self.status.set_text("Click on a row of the style first.")
            return
        self.tickStyles(True, marker=model[titer][S_MARKER])

    def styleCopyPlan(self):
        ''' Returns (the ticked StyleDifferences, the columns to change or None for all that differ) '''
        todo = [d for d in self.styleDiffs if (d.marker, d.attr) in self.styleTicked]
        only = self.styleCopyTo.get_active_id() or None
        if only is not None:
            todo = [d for d in todo if only in d.differing]
        return todo, ([only] if only is not None else None)

    def onCopyStyles(self, b):
        todo, columns = self.styleCopyPlan()
        if not len(todo):
            return
        lines = []
        for d in todo:
            for c in d.differing:
                if columns is None or c in columns:
                    lines.append(f"{c}: \\{d.marker} {d.attr}: {d.values[c].shown(d.attr)} becomes {d.baseline.shown(d.attr)}")
        if self.confirm(f"Change {len(lines)} style value{'s' if len(lines) != 1 else ''} (in ptxprint.sty)?", lines):
            self.copyStyles(todo, columns)

    def copyStyles(self, todo, columns=None):
        try:
            changed, problems = self.styleComparison.copy(todo, columns)
        except OSError as e:
            self.status.set_text(f"Could not copy: {e}")
            return 0, [str(e)]
        self.styleTicked = set()
        self.fillStyles()
        msg = f"Changed {changed} style value{'s' if changed != 1 else ''}. Test print to check the result."
        if len(problems):
            msg += f" {len(problems)} could not be brought into line: " + "; ".join(problems[:3]) + ("..." if len(problems) > 3 else "")
        self.status.set_text(msg)
        return changed, problems

    def onStyleTooltip(self, tree, x, y, keyboard, tooltip):
        if self.styleComparison is None or keyboard:
            return False
        bx, by = tree.convert_widget_to_bin_window_coords(x, y)
        hit = tree.get_path_at_pos(bx, by)
        if hit is None:
            return False
        path, column = hit[0], hit[1]
        row = tree.get_model()[path]
        d = self.styleShown[row[S_INDEX]]
        cols = tree.get_columns()
        i = cols.index(column) - 4
        lines = []
        def describe(label, v):
            return f"{label}: {v.shown(d.attr)}   ({'the default' if v.source == 'default' else 'from ' + v.source})"
        if 0 <= i < len(self.styleComparison.columns):
            label = self.styleComparison.columns[i]
            lines.append(describe(label, d.values[label]))
            lines.append(describe("compared with", d.baseline))
        else:
            lines.append(f"\\{d.marker}  {d.attr}")
            lines.append(describe("compared with", d.baseline))
            lines.extend(describe(c, d.values[c]) for c in d.differing[:12])
        tooltip.set_text("\n".join(lines))
        tree.set_tooltip_cell(tooltip, path, column, None)
        return True

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
        ''' pairs: (project, config) to print books with, or (project, config, publication) to print '''
        self.printStore.clear()
        rows = {}
        for pair in pairs:
            label = pair[1] if len(pair) < 3 else f"{pair[1]}: {pair[2]}"
            rows[pair] = self.printStore.append([pair[0], label, "Waiting", "", "", "#606060", "", 400])
        if books is None:
            books = "the publications"
        self.printer = TestPrinter(self.validator)
        self.printButton.set_sensitive(False)
        self.stopButton.set_sensitive(True)
        self.printCounts = {PRINTED: 0, FAILED: 0, SKIPPED: 0, STOPPED: 0}
        self.status.set_text(f"Printing {books} in {len(pairs)} project configuration{'s' if len(pairs) != 1 else ''}...")
        printer = self.printer

        def one(pair):
            GLib.idle_add(self.showPrinting, rows[pair])
            res = printer.run(pair[0], pair[1], books, pub=pair[2] if len(pair) > 2 else None)
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
