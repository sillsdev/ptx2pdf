import logging
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .wizardState import SectionStatus

logger = logging.getLogger(__name__)

STATUS_ICONS = {
    SectionStatus.notStarted:  "⚪",
    SectionStatus.inProgress:  "🟡",
    SectionStatus.complete:    "✅",
    SectionStatus.hasWarnings: "⚠",
    SectionStatus.stale:       "🔄",
}

SECTION_ORDER = [
    ("recipe",      "Recipe"),
    ("audience",    "Audience"),
    ("production",  "Production"),
    ("trimBinding", "Trim & Binding"),
    ("content",     "Content"),
    ("peripherals", "Peripherals"),
    ("layout",      "Layout"),
    ("review",      "Review"),
]


class SidebarDashboard(Gtk.Box):

    def __init__(self, onSectionClicked, onBack, onNext):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self._onSectionClicked = onSectionClicked
        self._onBack = onBack
        self._onNext = onNext
        self._activeSection = "recipe"
        self._rows: dict = {}  # sectionId -> (row_box, statusLabel)
        self._buildUi()
        self.show()

    def _buildUi(self):
        # Title
        titleLbl = Gtk.Label()
        titleLbl.set_markup("<b>Setup Wizard</b>")
        titleLbl.set_margin_start(12)
        titleLbl.set_margin_top(12)
        titleLbl.set_margin_bottom(8)
        titleLbl.set_xalign(0.0)
        titleLbl.show()
        self.pack_start(titleLbl, False, False, 0)

        sep = Gtk.Separator()
        sep.show()
        self.pack_start(sep, False, False, 0)

        # Section rows
        for sectionId, sectionLabel in SECTION_ORDER:
            row = self._makeRow(sectionId, sectionLabel)
            self.pack_start(row, False, False, 0)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        spacer.show()
        self.pack_start(spacer, True, True, 0)

        sep2 = Gtk.Separator()
        sep2.show()
        self.pack_start(sep2, False, False, 0)

        # Back / Next buttons
        navBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        navBox.set_margin_start(8)
        navBox.set_margin_end(8)
        navBox.set_margin_top(8)
        navBox.set_margin_bottom(8)

        self._btnBack = Gtk.Button(label="← Back")
        self._btnBack.set_sensitive(False)
        self._btnBack.connect("clicked", lambda _b: self._onBack())
        self._btnBack.show()

        self._btnNext = Gtk.Button(label="Next →")
        self._btnNext.connect("clicked", lambda _b: self._onNext())
        self._btnNext.show()

        navBox.pack_start(self._btnBack, True, True, 0)
        navBox.pack_start(self._btnNext, True, True, 0)
        navBox.show()
        self.pack_start(navBox, False, False, 0)

    def _makeRow(self, sectionId, sectionLabel):
        eventBox = Gtk.EventBox()
        eventBox.connect("button-press-event",
                         lambda _w, _e, sid=sectionId: self._onSectionClicked(sid))

        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row.set_margin_start(12)
        row.set_margin_end(8)
        row.set_margin_top(6)
        row.set_margin_bottom(6)

        nameLbl = Gtk.Label(label=sectionLabel)
        nameLbl.set_xalign(0.0)
        nameLbl.set_hexpand(True)
        nameLbl.show()

        statusLbl = Gtk.Label(label=STATUS_ICONS[SectionStatus.notStarted])
        statusLbl.show()

        row.pack_start(nameLbl, True, True, 0)
        row.pack_start(statusLbl, False, False, 0)
        row.show()
        eventBox.add(row)
        eventBox.show()

        self._rows[sectionId] = (eventBox, statusLbl, nameLbl)
        return eventBox

    def setActiveSection(self, sectionId: str):
        self._activeSection = sectionId
        for sid, (box, _status, nameLbl) in self._rows.items():
            ctx = box.get_style_context()
            if sid == sectionId:
                ctx.add_class("sidebar-active")
                nameLbl.set_markup(f"<b>{nameLbl.get_text()}</b>")
            else:
                ctx.remove_class("sidebar-active")
                nameLbl.set_markup(nameLbl.get_text())

    def updateStatus(self, sectionId: str, status: SectionStatus):
        if sectionId in self._rows:
            _, statusLbl, _ = self._rows[sectionId]
            statusLbl.set_text(STATUS_ICONS.get(status, "⚪"))

    def setBackSensitive(self, sensitive: bool):
        self._btnBack.set_sensitive(sensitive)

    def setNextLabel(self, label: str):
        self._btnNext.set_label(label)
