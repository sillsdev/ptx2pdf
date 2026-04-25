import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .sectionBase import (SectionPanel, makeVBox, makeHBox, makeFrame,
                           makeSectionTitle, makeButton)

logger = logging.getLogger(__name__)

PRESETS = {
    "minimal":  ["tableOfContents"],
    "standard": ["tableOfContents", "bookIntroductions", "crossReferences", "footnotes"],
    "study":    ["tableOfContents", "bookIntroductions", "crossReferences", "footnotes",
                 "studyNotes", "glossary", "maps", "parallelPassages", "weightsAndMeasures"],
}

STATUS_ICONS = {
    "available":          "✅",
    "notCreated":         "📝",
    "alwaysAvailable":    "⚙",
}

ALWAYS_AVAILABLE = {"tableOfContents", "readingPlan", "weightsAndMeasures"}


class PeripheralsSection(SectionPanel):
    sectionId = "peripherals"

    def __init__(self):
        self._catalogue = []
        self._itemChecks: Dict[str, Gtk.CheckButton] = {}
        self._projectAvailability: Dict[str, str] = {}
        super().__init__()

    def _buildUi(self):
        self.pack_start(makeSectionTitle("Peripheral content"), False, False, 0)

        intro = Gtk.Label(label=(
            "Choose which supplementary content to include. "
            "Items marked 📝 don't yet exist in the project — you can still select them "
            "and create them in PTXprint after the wizard completes."
        ))
        intro.set_xalign(0.0)
        intro.set_line_wrap(True)
        intro.show()
        self.pack_start(intro, False, False, 0)

        # Preset buttons
        presetRow = makeHBox(spacing=8)
        presetLbl = Gtk.Label(label="Quick preset:")
        presetLbl.show()
        presetRow.pack_start(presetLbl, False, False, 0)
        for presetId, presetLabel in [("minimal", "Minimal"), ("standard", "Standard"), ("study", "Study")]:
            btn = makeButton(presetLabel)
            btn.connect("clicked", self._onPreset, presetId)
            presetRow.pack_start(btn, False, False, 0)
        presetRow.show()
        self.pack_start(presetRow, False, False, 0)

        # Catalogue will be populated dynamically
        self._catalogueBox = makeVBox(spacing=6)
        self._catalogueBox.show()

        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sw.set_min_content_height(300)
        sw.add(self._catalogueBox)
        sw.show()
        self.pack_start(sw, True, True, 0)

    def loadCatalogue(self, catalogue: List[Dict]):
        """Populate the UI from peripheralsCatalogue.json data."""
        self._catalogue = catalogue
        for child in list(self._catalogueBox.get_children()):
            self._catalogueBox.remove(child)
        self._itemChecks.clear()

        for category in catalogue:
            catLabel = category.get("label", category.get("id", ""))
            catBox = makeVBox(spacing=3)
            catBox.set_margin_start(0)

            catTitleLbl = Gtk.Label()
            catTitleLbl.set_markup(f"<b>{catLabel}</b>")
            catTitleLbl.set_xalign(0.0)
            catTitleLbl.show()
            catBox.pack_start(catTitleLbl, False, False, 0)

            for item in category.get("items", []):
                itemId   = item.get("id", "")
                itemLabel = item.get("label", itemId)
                note      = item.get("note", "")
                pageEst   = item.get("estimatedPages", item.get("estimatedPagesPerBook", 0))

                row = makeHBox(spacing=6)

                chk = Gtk.CheckButton()
                chk.show()
                chk.connect("toggled", self._onItemToggled)
                self._itemChecks[itemId] = chk
                row.pack_start(chk, False, False, 0)

                availability = self._projectAvailability.get(
                    itemId, "alwaysAvailable" if itemId in ALWAYS_AVAILABLE else "notCreated")
                statusIcon = Gtk.Label(label=STATUS_ICONS.get(availability, "⚪"))
                statusIcon.show()
                row.pack_start(statusIcon, False, False, 0)

                textBox = makeVBox(spacing=0)
                mainLbl = Gtk.Label(label=itemLabel)
                mainLbl.set_xalign(0.0)
                mainLbl.show()
                textBox.pack_start(mainLbl, False, False, 0)

                if note:
                    noteLbl = Gtk.Label(label=note)
                    noteLbl.set_xalign(0.0)
                    noteLbl.set_line_wrap(True)
                    noteLbl.get_style_context().add_class("dim-label")
                    noteLbl.show()
                    textBox.pack_start(noteLbl, False, False, 0)
                textBox.show()
                row.pack_start(textBox, True, True, 0)

                if pageEst:
                    pageLbl = Gtk.Label(label=f"~{pageEst} pp")
                    pageLbl.get_style_context().add_class("dim-label")
                    pageLbl.show()
                    row.pack_end(pageLbl, False, False, 0)

                row.show()
                catBox.pack_start(row, False, False, 0)

            catBox.show()
            self._catalogueBox.pack_start(catBox, False, False, 0)

    def updateAvailability(self, availability: Dict[str, str]):
        """Update which items are available in the project. Call after PTXprint inspection."""
        self._projectAvailability = availability

    def _onPreset(self, _btn, presetId):
        selected = set(PRESETS.get(presetId, []))
        for itemId, chk in self._itemChecks.items():
            chk.set_active(itemId in selected)
        self._emitStateChanged()

    def _onItemToggled(self, *_args):
        self._emitStateChanged()

    def _getSelected(self) -> List[str]:
        return [itemId for itemId, chk in self._itemChecks.items() if chk.get_active()]

    def loadFromState(self, state):
        self._loading = True
        selected = set(state.peripherals.selected)
        for itemId, chk in self._itemChecks.items():
            chk.set_active(itemId in selected)
        self._loading = False

    def saveToState(self, state):
        state.peripherals.selected = self._getSelected()

    def isComplete(self):
        return True  # peripherals are always optional
