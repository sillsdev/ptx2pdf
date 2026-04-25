import logging
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .sectionBase import (SectionPanel, makeVBox, makeHBox, makeCombo,
                           makeFrame, makeSectionTitle, makeInfoRow)

logger = logging.getLogger(__name__)

TRIM_SIZES = [
    ("a4",          "A4 (210×297 mm) — large, study/reference"),
    ("a5",          "A5 (148×210 mm) — popular compact size"),
    ("a6",          "A6 (105×148 mm) — pocket size"),
    ("letter",      "Letter (216×279 mm) — US standard"),
    ("halfLetter",  "Half Letter (140×216 mm) — US compact"),
    ("fiveByEight", "5×8 in (127×203 mm) — trade paperback"),
    ("sixByNine",   "6×9 in (152×229 mm) — standard POD trade"),
    ("sevenByTen",  "7×10 in (178×254 mm) — large trade/study"),
]

BINDING_TYPES = [
    ("saddleStitch", "Saddle-stitch (stapled) — up to ~64 pages, lays flat"),
    ("perfectBound", "Perfect-bound (glued spine) — standard paperback"),
    ("caseBound",    "Case-bound (hardcover) — durable, premium"),
    ("spiral",       "Spiral / comb — lies completely flat"),
]

PAPER_TYPES = [
    ("standard",     "Standard 80–90 gsm white"),
    ("cream",        "Cream / off-white 80 gsm — easier on the eyes"),
    ("biblePaper28", "Bible paper 28 gsm — very thin, reduces bulk"),
    ("biblePaper36", "Bible paper 36 gsm — thin, slightly more opaque"),
]


class TrimBindingSection(SectionPanel):
    sectionId = "trimBinding"

    def _buildUi(self):
        self.pack_start(makeSectionTitle("Trim size, binding & paper"), False, False, 0)

        self._trimCombo = makeCombo(TRIM_SIZES)
        self._trimCombo.connect("changed", self._onChange)
        self.pack_start(makeInfoRow(
            "Trim size",
            self._trimCombo,
            "The physical page dimensions. POD providers restrict which sizes they support."
        ), False, False, 0)

        self._bindingCombo = makeCombo(BINDING_TYPES)
        self._bindingCombo.connect("changed", self._onChange)
        self.pack_start(makeInfoRow(
            "Binding type",
            self._bindingCombo,
            "How pages are held together. Saddle-stitch is limited to ~64 pages."
        ), False, False, 0)

        self._paperCombo = makeCombo(PAPER_TYPES)
        self._paperCombo.connect("changed", self._onChange)
        self.pack_start(makeInfoRow(
            "Paper type",
            self._paperCombo,
            "Bible paper (lightweight) is generally only available through offset printers."
        ), False, False, 0)

        self._warningLabel = Gtk.Label()
        self._warningLabel.set_xalign(0.0)
        self._warningLabel.set_line_wrap(True)
        self._warningLabel.get_style_context().add_class("dim-label")
        self._warningLabel.set_no_show_all(True)
        self._warningLabel.hide()
        self.pack_start(self._warningLabel, False, False, 0)

    def _onChange(self, *_args):
        self._emitStateChanged()

    def onConstraintsChanged(self, engine, flat):
        """Refresh which trim sizes are available given the production method/provider."""
        allowedTrims = engine.allowedValues("trimBinding.trimSize", flat)
        if allowedTrims:
            self._refreshCombo(self._trimCombo, TRIM_SIZES, allowedTrims)

        allowedBindings = engine.allowedValues("trimBinding.bindingType", flat)
        if allowedBindings:
            self._refreshCombo(self._bindingCombo, BINDING_TYPES, allowedBindings)

        allowedPapers = engine.allowedValues("trimBinding.paperType", flat)
        if allowedPapers:
            self._refreshCombo(self._paperCombo, PAPER_TYPES, allowedPapers)

    def _refreshCombo(self, combo, allItems, allowedIds):
        current = combo.get_active_id()
        combo.remove_all()
        for itemId, itemLabel in allItems:
            if itemId in allowedIds:
                combo.append(itemId, itemLabel)
        if current and current in allowedIds:
            combo.set_active_id(current)
        elif combo.get_model() and len(combo.get_model()) > 0:
            combo.set_active(0)

    def loadFromState(self, state):
        self._loading = True
        if state.trimBinding.trimSize:
            self._trimCombo.set_active_id(state.trimBinding.trimSize)
        if state.trimBinding.bindingType:
            self._bindingCombo.set_active_id(state.trimBinding.bindingType)
        if state.trimBinding.paperType:
            self._paperCombo.set_active_id(state.trimBinding.paperType)
        self._loading = False

    def saveToState(self, state):
        state.trimBinding.trimSize    = self._trimCombo.get_active_id()
        state.trimBinding.bindingType = self._bindingCombo.get_active_id()
        state.trimBinding.paperType   = self._paperCombo.get_active_id()

    def isComplete(self):
        return all([
            self._trimCombo.get_active_id() is not None,
            self._bindingCombo.get_active_id() is not None,
            self._paperCombo.get_active_id() is not None,
        ])
