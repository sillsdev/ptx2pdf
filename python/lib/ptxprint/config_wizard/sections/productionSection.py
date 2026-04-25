import logging
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .sectionBase import (SectionPanel, makeVBox, makeHBox, makeCombo,
                           makeFrame, makeSectionTitle, GLib_escape)

logger = logging.getLogger(__name__)

METHODS = [
    ("localPrinter",     "Desktop / Local Printer",
     "Run size: 1–50",   "Per-copy cost: medium", "Setup: none", "Lead time: hours",
     "Best for very small trial runs. Limited quality and paper options."),
    ("officeDuplex",     "Office Duplex Laser",
     "Run size: 10–200", "Per-copy cost: low",    "Setup: none", "Lead time: hours–days",
     "Low cost for modest runs. Stapled or spiral-bound finish. No Bible paper."),
    ("podService",       "Print-on-Demand (POD) Service",
     "Run size: 1–500",  "Per-copy cost: high",   "Setup: none", "Lead time: 1–3 weeks",
     "No setup fee, easy reordering, global distribution options. Limited trim sizes."),
    ("shortRunDigital",  "Short-Run Digital Press",
     "Run size: 50–2000","Per-copy cost: medium", "Setup: low",  "Lead time: 1–4 weeks",
     "Good quality, faster than offset. Good middle ground for 100–2 000 copies."),
    ("offset",           "Offset Press",
     "Run size: 1000+",  "Per-copy cost: low@vol","Setup: high", "Lead time: 4–12 weeks",
     "Lowest per-copy cost at volume. Bible paper available. High setup cost."),
]

POD_PROVIDERS = [
    ("lulu",         "Lulu"),
    ("ingramSpark",  "IngramSpark"),
    ("kdp",          "Amazon KDP"),
    ("other",        "Other / Custom"),
]


class ProductionSection(SectionPanel):
    sectionId = "production"

    def _buildUi(self):
        self.pack_start(makeSectionTitle("How will this be printed?"), False, False, 0)

        intro = Gtk.Label(label=(
            "Choose the production method that best fits your run size, budget, and timeline."
        ))
        intro.set_xalign(0.0)
        intro.set_line_wrap(True)
        intro.show()
        self.pack_start(intro, False, False, 0)

        self._methodRadios = {}
        group = None

        for (methodId, methodLabel, runSize, costBand, setup, leadTime, note) in METHODS:
            card = self._makeMethodCard(methodId, methodLabel, runSize, costBand, setup, leadTime, note, group)
            if group is None:
                for child in card.get_children():
                    if isinstance(child, Gtk.RadioButton):
                        group = child
                        break
            self.pack_start(card, False, False, 0)

        # POD provider sub-combo
        self._podBox = makeVBox(spacing=4)
        self._podBox.set_margin_start(20)

        podLbl = Gtk.Label(label="POD Service provider:")
        podLbl.set_xalign(0.0)
        podLbl.show()

        self._podCombo = makeCombo(POD_PROVIDERS)
        self._podCombo.connect("changed", self._onPodProviderChanged)

        podRow = makeHBox(spacing=8)
        podRow.pack_start(podLbl, False, False, 0)
        podRow.pack_start(self._podCombo, False, False, 0)
        podRow.show()

        self._podBox.pack_start(podRow, False, False, 0)
        self._podBox.show()
        self._podBox.set_no_show_all(True)
        self._podBox.set_visible(False)

        self.pack_start(self._podBox, False, False, 0)

    def _makeMethodCard(self, methodId, methodLabel, runSize, costBand, setup, leadTime, note, group):
        frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)

        inner = makeVBox(spacing=2)
        inner.set_margin_start(8)
        inner.set_margin_end(8)
        inner.set_margin_top(6)
        inner.set_margin_bottom(6)

        radio = Gtk.RadioButton.new_with_label_from_widget(group, methodLabel)
        radio.connect("toggled", self._onMethodToggled, methodId)
        radio.show()
        self._methodRadios[methodId] = radio
        inner.pack_start(radio, False, False, 0)

        statsRow = makeHBox(spacing=16)
        for stat in (runSize, costBand, setup, leadTime):
            lbl = Gtk.Label(label=stat)
            lbl.get_style_context().add_class("dim-label")
            lbl.show()
            statsRow.pack_start(lbl, False, False, 0)
        statsRow.show()
        inner.pack_start(statsRow, False, False, 0)

        noteLbl = Gtk.Label(label=note)
        noteLbl.set_xalign(0.0)
        noteLbl.set_line_wrap(True)
        noteLbl.get_style_context().add_class("dim-label")
        noteLbl.show()
        inner.pack_start(noteLbl, False, False, 0)

        inner.show()
        frame.add(inner)
        frame.show()
        return frame

    def _onMethodToggled(self, radio, methodId):
        if not self._loading and radio.get_active():
            self._podBox.set_visible(methodId == "podService")
            self._emitStateChanged()

    def _onPodProviderChanged(self, *_args):
        self._emitStateChanged()

    def _getActiveMethod(self):
        for methodId, radio in self._methodRadios.items():
            if radio.get_active():
                return methodId
        return None

    def onConstraintsChanged(self, engine, flat):
        # Could grey out methods that conflict with current audience — left for future refinement
        pass

    def loadFromState(self, state):
        self._loading = True
        method = state.production.method
        if method and method in self._methodRadios:
            self._methodRadios[method].set_active(True)
            self._podBox.set_visible(method == "podService")
        if state.production.podProvider:
            self._podCombo.set_active_id(state.production.podProvider)
        self._loading = False

    def saveToState(self, state):
        state.production.method = self._getActiveMethod()
        if state.production.method == "podService":
            state.production.podProvider = self._podCombo.get_active_id()
        else:
            state.production.podProvider = None

    def isComplete(self):
        return self._getActiveMethod() is not None
