import logging
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .sectionBase import (SectionPanel, makeVBox, makeHBox, makeCombo,
                           makeFrame, makeSectionTitle, makeInfoRow, makeSpinner)

logger = logging.getLogger(__name__)

MARGIN_PRESETS = [
    ("tight",     "Tight — more text per page"),
    ("standard",  "Standard — balanced readability"),
    ("generous",  "Generous — good for annotation or study"),
]

# Text area at standard margins, by trim size (width_mm × height_mm)
TEXT_AREAS = {
    "a4":          (155, 242), "a5":         (115, 182), "a6":          (88,  135),
    "letter":      (152, 228), "halfLetter": (106, 174), "fiveByEight": (92,  165),
    "sixByNine":   (117, 196), "sevenByTen": (142, 222),
}
MARGIN_SCALE = {"tight": 1.08, "standard": 1.00, "generous": 0.88}


class LayoutSection(SectionPanel):
    sectionId = "layout"

    def _buildUi(self):
        self.pack_start(makeSectionTitle("Layout"), False, False, 0)

        # Columns
        colFrame = makeFrame("Columns")
        colInner = makeHBox(spacing=16)
        colInner.set_margin_start(8)
        colInner.set_margin_end(8)
        colInner.set_margin_top(6)
        colInner.set_margin_bottom(6)

        self._col1Radio = Gtk.RadioButton.new_with_label(None, "Single column")
        self._col1Radio.connect("toggled", self._onColumnsChanged)
        self._col1Radio.show()

        self._col2Radio = Gtk.RadioButton.new_with_label_from_widget(self._col1Radio, "Double column")
        self._col2Radio.connect("toggled", self._onColumnsChanged)
        self._col2Radio.show()

        colInner.pack_start(self._col1Radio, False, False, 0)
        colInner.pack_start(self._col2Radio, False, False, 0)
        colInner.show()
        colFrame.add(colInner)
        colFrame.show()
        self.pack_start(colFrame, False, False, 0)

        # Body font size
        self._fontSizeSpin = makeSpinner(10.5, 6.0, 24.0, step=0.5, digits=1)
        self._fontSizeSpin.connect("value-changed", self._onFontSizeChanged)
        self.pack_start(makeInfoRow(
            "Body font size (pt)",
            self._fontSizeSpin,
            "Main text font size. Large-print editions typically use 12pt+."
        ), False, False, 0)

        # Body leading
        self._leadingSpin = makeSpinner(12.5, 6.0, 36.0, step=0.5, digits=1)
        self._leadingSpin.connect("value-changed", self._onChange)
        self.pack_start(makeInfoRow(
            "Line spacing / leading (pt)",
            self._leadingSpin,
            "Distance between baselines. Typically 120% of font size."
        ), False, False, 0)

        # Body font picker
        self._fontBtn = Gtk.FontButton()
        self._fontBtn.set_valign(Gtk.Align.CENTER)
        self._fontBtn.set_hexpand(True)
        self._fontBtn.connect("font-set", self._onChange)
        self._fontBtn.show()
        self.pack_start(makeInfoRow(
            "Body font",
            self._fontBtn,
            "Font for the main Scripture text. Leave blank to use the project default."
        ), False, False, 0)

        # Margin preset
        self._marginCombo = makeCombo(MARGIN_PRESETS)
        self._marginCombo.connect("changed", self._onMarginChanged)
        self.pack_start(makeInfoRow(
            "Margin preset",
            self._marginCombo,
            "Tight margins fit more text per page; generous margins leave room to write notes."
        ), False, False, 0)

        # Read-only computed text area display
        self._textAreaLabel = Gtk.Label(label="Text area: —")
        self._textAreaLabel.set_xalign(0.0)
        self._textAreaLabel.get_style_context().add_class("dim-label")
        self._textAreaLabel.show()
        self.pack_start(self._textAreaLabel, False, False, 0)

        # Advanced note
        noteLbl = Gtk.Label(label=(
            "Advanced layout options (headers, footers, chapter drop, etc.) "
            "remain available in the main PTXprint interface after the wizard completes."
        ))
        noteLbl.set_xalign(0.0)
        noteLbl.set_line_wrap(True)
        noteLbl.get_style_context().add_class("dim-label")
        noteLbl.show()
        self.pack_start(noteLbl, False, False, 0)

        self._trimSize = None

    def _onColumnsChanged(self, radio):
        if not self._loading and radio.get_active():
            self._emitStateChanged()

    def _onFontSizeChanged(self, spin):
        if not self._loading:
            fontSize = spin.get_value()
            self._leadingSpin.set_value(round(fontSize * 1.2 * 2) / 2)
            self._emitStateChanged()

    def _onMarginChanged(self, *_args):
        self._updateTextAreaLabel()
        self._emitStateChanged()

    def _onChange(self, *_args):
        self._emitStateChanged()

    def updateTrimSize(self, trimSize):
        """Called by controller when trim size changes."""
        self._trimSize = trimSize
        self._updateTextAreaLabel()

    def _updateTextAreaLabel(self):
        if not self._trimSize:
            self._textAreaLabel.set_text("Text area: —")
            return
        baseW, baseH = TEXT_AREAS.get(self._trimSize, (115, 182))
        margin = self._marginCombo.get_active_id() or "standard"
        scale = MARGIN_SCALE.get(margin, 1.0)
        w = round(baseW * scale)
        h = round(baseH * scale)
        self._textAreaLabel.set_text(f"Text area: {w} × {h} mm")

    def _getColumns(self):
        return 2 if self._col2Radio.get_active() else 1

    def loadFromState(self, state):
        self._loading = True
        lay = state.layout
        if lay.columns == 2:
            self._col2Radio.set_active(True)
        else:
            self._col1Radio.set_active(True)
        if lay.bodyFontSize is not None:
            self._fontSizeSpin.set_value(lay.bodyFontSize)
        if lay.bodyLeading is not None:
            self._leadingSpin.set_value(lay.bodyLeading)
        if lay.bodyFont:
            self._fontBtn.set_font(lay.bodyFont)
        if lay.marginPreset:
            self._marginCombo.set_active_id(lay.marginPreset)
        self._loading = False

    def saveToState(self, state):
        state.layout.columns       = self._getColumns()
        state.layout.bodyFontSize  = self._fontSizeSpin.get_value()
        state.layout.bodyLeading   = self._leadingSpin.get_value()
        fontDesc = self._fontBtn.get_font()
        state.layout.bodyFont      = fontDesc if fontDesc else None
        state.layout.marginPreset  = self._marginCombo.get_active_id()

    def isComplete(self):
        return all([
            self._marginCombo.get_active_id() is not None,
            self._fontSizeSpin.get_value() > 0,
            self._leadingSpin.get_value() > 0,
        ])
