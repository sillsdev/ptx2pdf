import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from .wizardController import WizardController, SECTION_ORDER
from .sidebarDashboard import SidebarDashboard
from .feedbackPanel import FeedbackPanel

logger = logging.getLogger(__name__)

CSS = b"""
.sidebar-active {
    background-color: alpha(@theme_selected_bg_color, 0.15);
}
.sidebar-active label {
    font-weight: bold;
}
"""


class WizardWindow:
    """
    Top-level modal window for the PTXprint Setup Wizard.
    Call run() to show the dialog.  The window is modal: it blocks interaction
    with the parent PTXprint window until the user closes or finishes.
    """

    def __init__(self, parent: Optional[Gtk.Window] = None,
                 dataDir: Optional[Path] = None,
                 statePath: Optional[Path] = None,
                 autoLaunch: bool = False):

        if dataDir is None:
            dataDir = Path(__file__).parent / "data"

        self._controller = WizardController(dataDir=dataDir, statePath=statePath)
        self._autoLaunch = autoLaunch
        self._parent = parent

        self._applyStyles()
        self._buildWindow(parent)
        self._wireSections()
        self._controller.jumpToSection("recipe")

    # ── Style ──────────────────────────────────────────────────────────────

    def _applyStyles(self):
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    # ── Build ──────────────────────────────────────────────────────────────

    def _buildWindow(self, parent):
        self._win = Gtk.Window(title="PTXprint Setup Wizard")
        self._win.set_default_size(1100, 700)
        self._win.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self._win.set_modal(True)
        if parent:
            self._win.set_transient_for(parent)
        self._win.connect("delete-event", self._onDeleteEvent)

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self._win.add(root)

        # Header bar
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        header.set_margin_start(12)
        header.set_margin_end(12)
        header.set_margin_top(6)
        header.set_margin_bottom(6)

        self._headerSectionLbl = Gtk.Label()
        self._headerSectionLbl.set_markup("<b>PTXprint Setup Wizard</b>")
        self._headerSectionLbl.set_xalign(0.0)
        self._headerSectionLbl.set_hexpand(True)
        self._headerSectionLbl.show()
        header.pack_start(self._headerSectionLbl, True, True, 0)

        if self._autoLaunch:
            skipBtn = Gtk.Button(label="Skip wizard, set up manually")
            skipBtn.connect("clicked", lambda _b: self._closeWindow(save=False))
            skipBtn.show()
            header.pack_start(skipBtn, False, False, 0)

        header.show()
        root.pack_start(header, False, False, 0)

        root.pack_start(Gtk.Separator(), False, False, 0)

        # Three-pane layout
        outerPaned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        outerPaned.set_vexpand(True)

        # Left: sidebar
        self._sidebar = SidebarDashboard(
            onSectionClicked=self._controller.jumpToSection,
            onBack=self._controller.goBack,
            onNext=self._onNext,
        )
        self._sidebar.set_size_request(200, -1)

        sidebarFrame = Gtk.Frame()
        sidebarFrame.set_shadow_type(Gtk.ShadowType.NONE)
        sidebarFrame.add(self._sidebar)
        sidebarFrame.show()

        outerPaned.pack1(sidebarFrame, resize=False, shrink=False)

        # Center + Right
        innerPaned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        innerPaned.set_hexpand(True)

        # Center: scrolled section area
        self._sectionStack = Gtk.Stack()
        self._sectionStack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self._sectionStack.set_hexpand(True)
        self._sectionStack.set_vexpand(True)

        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sw.set_hexpand(True)
        sw.set_vexpand(True)
        sw.add(self._sectionStack)
        sw.show()

        panels = self._controller.createSections()
        for sectionId, panel in panels.items():
            self._sectionStack.add_named(panel, sectionId)

        self._sectionStack.show()
        innerPaned.pack1(sw, resize=True, shrink=False)

        # Right: feedback panel
        self._feedback = FeedbackPanel()
        feedSw = Gtk.ScrolledWindow()
        feedSw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        feedSw.set_size_request(200, -1)
        feedSw.add(self._feedback)
        feedSw.show()
        innerPaned.pack2(feedSw, resize=False, shrink=False)
        innerPaned.set_position(680)
        innerPaned.show()

        outerPaned.pack2(innerPaned, resize=True, shrink=False)
        outerPaned.set_position(200)
        outerPaned.show()

        root.pack_start(outerPaned, True, True, 0)
        root.show()

    # ── Wire controller callbacks ──────────────────────────────────────────

    def _wireSections(self):
        self._controller.setOnSectionSwitched(self._onSectionSwitched)
        self._controller.setOnFeedbackUpdated(self._onFeedbackUpdated)
        self._controller.setOnSidebarUpdated(self._onSidebarUpdated)

        # Wire review apply buttons
        reviewPanel = self._controller._sections.get("review")
        if reviewPanel:
            reviewPanel.setCallbacks(
                applyNew=self._onApplyNew,
                applyCurrent=self._onApplyCurrent,
                closeNo=lambda: self._closeWindow(save=True),
            )

    # ── Controller callback implementations ───────────────────────────────

    def _onSectionSwitched(self, sectionId: str, panel):
        self._sectionStack.set_visible_child_name(sectionId)
        self._sidebar.setActiveSection(sectionId)

        idx = SECTION_ORDER.index(sectionId)
        self._sidebar.setBackSensitive(idx > 0)
        isLast = (idx == len(SECTION_ORDER) - 1)
        self._sidebar.setNextLabel("Finish" if isLast else "Next →")

        sectionTitles = {
            "recipe": "Recipe", "audience": "Audience", "production": "Production",
            "trimBinding": "Trim & Binding", "content": "Content",
            "peripherals": "Peripherals", "layout": "Layout", "review": "Review & Apply",
        }
        title = sectionTitles.get(sectionId, sectionId)
        self._headerSectionLbl.set_markup(
            f"<b>PTXprint Setup Wizard</b>  —  {title}")

    def _onFeedbackUpdated(self, pageCount, spineWidth, perCopy, total,
                           violations, columns, trimSize):
        self._feedback.update(pageCount, spineWidth, perCopy, total,
                              violations, columns, trimSize)

    def _onSidebarUpdated(self, sectionId, status):
        self._sidebar.updateStatus(sectionId, status)

    # ── Navigation ─────────────────────────────────────────────────────────

    def _onNext(self):
        active = self._controller.activeSection
        if active == SECTION_ORDER[-1]:
            self._closeWindow(save=False)
        else:
            self._controller.goNext()

    # ── Apply actions ──────────────────────────────────────────────────────

    def _onApplyNew(self):
        dlg = Gtk.Dialog(title="Create new configuration",
                         transient_for=self._win, modal=True)
        dlg.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dlg.add_button("Create", Gtk.ResponseType.OK)
        dlg.set_default_response(Gtk.ResponseType.OK)

        box = dlg.get_content_area()
        box.set_spacing(8)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(8)
        box.set_margin_bottom(8)

        lbl = Gtk.Label(label="Configuration name:")
        lbl.set_xalign(0.0)
        lbl.show()
        box.add(lbl)

        entry = Gtk.Entry()
        entry.set_activates_default(True)
        entry.show()
        box.add(entry)
        box.show()

        response = dlg.run()
        configName = entry.get_text().strip()
        dlg.destroy()

        if response == Gtk.ResponseType.OK and configName:
            ok = self._controller.applyToNewConfig(configName)
            if ok:
                self._showInfo(f"Configuration '{configName}' created.\n"
                               "You can now generate a PDF from the main PTXprint window.")
                self._closeWindow(save=False)

    def _onApplyCurrent(self):
        # TODO(integrate): pass real currentConfig from PTXprint
        diff = self._controller.applyToCurrentConfig({})
        if not diff:
            self._showInfo("No changes to apply.")
            return

        dlg = Gtk.Dialog(title="Confirm changes",
                         transient_for=self._win, modal=True)
        dlg.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dlg.add_button("Apply", Gtk.ResponseType.OK)
        dlg.set_default_response(Gtk.ResponseType.OK)
        dlg.set_default_size(500, 350)

        box = dlg.get_content_area()
        box.set_spacing(8)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(8)
        box.set_margin_bottom(8)

        lbl = Gtk.Label(label="The following settings will be changed:")
        lbl.set_xalign(0.0)
        lbl.show()
        box.add(lbl)

        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sw.set_min_content_height(200)
        diffBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        diffBox.set_margin_start(4)
        for key, oldVal, newVal in diff:
            row = Gtk.Label(label=f"  {key}: {oldVal!r} → {newVal!r}")
            row.set_xalign(0.0)
            row.show()
            diffBox.add(row)
        diffBox.show()
        sw.add(diffBox)
        sw.show()
        box.add(sw)
        box.show()

        response = dlg.run()
        dlg.destroy()

        if response == Gtk.ResponseType.OK:
            # TODO(integrate): call PTXprint's applyConfigDiff(configName, {k: v for k,_,v in diff})
            logger.info(f"Would apply {len(diff)} setting changes")
            self._showInfo("Settings applied.\n"
                           "You can now generate a PDF from the main PTXprint window.")
            self._closeWindow(save=False)

    # ── Window lifecycle ───────────────────────────────────────────────────

    def _onDeleteEvent(self, _win, _event):
        self._promptSaveOnClose()
        return True  # prevent default destroy; we handle it ourselves

    def _promptSaveOnClose(self):
        dlg = Gtk.Dialog(title="Close wizard?",
                         transient_for=self._win, modal=True)
        dlg.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dlg.add_button("Discard", Gtk.ResponseType.REJECT)
        dlg.add_button("Save for later", Gtk.ResponseType.OK)
        dlg.set_default_response(Gtk.ResponseType.OK)

        box = dlg.get_content_area()
        lbl = Gtk.Label(label="Save your wizard progress for later?")
        lbl.set_margin_start(12)
        lbl.set_margin_end(12)
        lbl.set_margin_top(8)
        lbl.set_margin_bottom(8)
        lbl.show()
        box.add(lbl)
        box.show()

        response = dlg.run()
        dlg.destroy()

        if response == Gtk.ResponseType.CANCEL:
            return
        self._closeWindow(save=(response == Gtk.ResponseType.OK))

    def _closeWindow(self, save: bool):
        if save:
            self._controller.saveNow()
        self._win.destroy()

    def _showInfo(self, message: str):
        dlg = Gtk.MessageDialog(transient_for=self._win, modal=True,
                                message_type=Gtk.MessageType.INFO,
                                buttons=Gtk.ButtonsType.OK,
                                text=message)
        dlg.run()
        dlg.destroy()

    # ── Public API ─────────────────────────────────────────────────────────

    def run(self):
        """Show the wizard window. Returns immediately (non-blocking show)."""
        self._win.show_all()

    def runModal(self):
        """Show as modal and block until closed (useful for standalone testing)."""
        self._win.show_all()
        Gtk.main()
