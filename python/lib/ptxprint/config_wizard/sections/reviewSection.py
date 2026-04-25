import logging
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .sectionBase import SectionPanel, makeVBox, makeHBox, makeFrame, makeSectionTitle

logger = logging.getLogger(__name__)

SECTION_LABELS = {
    "recipe":      "Recipe",
    "audience":    "Audience",
    "production":  "Production",
    "trimBinding": "Trim & Binding",
    "content":     "Content",
    "peripherals": "Peripherals",
    "layout":      "Layout",
}

AUDIENCE_LABELS = {
    "purpose": "Purpose", "copyCount": "Copy count", "ageGroup": "Age group",
    "eyesightConsideration": "Eyesight", "readingContext": "Reading context",
    "literacyLevel": "Literacy level", "distributionModel": "Distribution",
    "budgetLevel": "Budget",
}
PRODUCTION_LABELS = {"method": "Method", "podProvider": "POD provider"}
TRIM_LABELS = {"trimSize": "Trim size", "bindingType": "Binding", "paperType": "Paper"}
CONTENT_LABELS = {"scope": "Scope", "isDiglot": "Diglot", "isTriglot": "Triglot"}
LAYOUT_LABELS = {
    "columns": "Columns", "bodyFontSize": "Font size (pt)",
    "bodyLeading": "Leading (pt)", "bodyFont": "Body font", "marginPreset": "Margins",
}


class ReviewSection(SectionPanel):
    sectionId = "review"

    def __init__(self, jumpCallback=None):
        self._jumpCb = jumpCallback
        self._applyNewCb = None
        self._applyCurrentCb = None
        self._closeNoCb = None
        super().__init__()

    def setCallbacks(self, applyNew, applyCurrent, closeNo):
        self._applyNewCb  = applyNew
        self._applyCurrentCb = applyCurrent
        self._closeNoCb   = closeNo

    def _buildUi(self):
        self.pack_start(makeSectionTitle("Review & Apply"), False, False, 0)

        # ── Summary block ──────────────────────────────────────────────
        summaryFrame = makeFrame("Summary")
        self._summaryBox = makeVBox(spacing=4)
        self._summaryBox.set_margin_start(8)
        self._summaryBox.set_margin_end(8)
        self._summaryBox.set_margin_top(6)
        self._summaryBox.set_margin_bottom(6)
        self._summaryBox.show()
        summaryFrame.add(self._summaryBox)
        summaryFrame.show()
        self.pack_start(summaryFrame, False, False, 0)

        # ── Estimates block ────────────────────────────────────────────
        estFrame = makeFrame("Estimates")
        self._estimatesBox = makeVBox(spacing=4)
        self._estimatesBox.set_margin_start(8)
        self._estimatesBox.set_margin_end(8)
        self._estimatesBox.set_margin_top(6)
        self._estimatesBox.set_margin_bottom(6)
        self._estimatesBox.show()
        estFrame.add(self._estimatesBox)
        estFrame.show()
        self.pack_start(estFrame, False, False, 0)

        # ── Warnings block ─────────────────────────────────────────────
        self._warningsFrame = makeFrame("Warnings & Errors")
        self._warningsBox = makeVBox(spacing=2)
        self._warningsBox.set_margin_start(8)
        self._warningsBox.set_margin_end(8)
        self._warningsBox.set_margin_top(6)
        self._warningsBox.set_margin_bottom(6)
        self._warningsBox.show()
        self._warningsFrame.add(self._warningsBox)
        self._warningsFrame.show()
        self._warningsFrame.set_no_show_all(True)
        self._warningsFrame.hide()
        self.pack_start(self._warningsFrame, False, False, 0)

        # ── Apply block ────────────────────────────────────────────────
        applyFrame = makeFrame("Apply")
        applyInner = makeVBox(spacing=8)
        applyInner.set_margin_start(8)
        applyInner.set_margin_end(8)
        applyInner.set_margin_top(8)
        applyInner.set_margin_bottom(8)

        self._btnCreateNew = Gtk.Button(label="Create new configuration…")
        self._btnCreateNew.set_hexpand(True)
        self._btnCreateNew.connect("clicked", self._onCreateNew)
        self._btnCreateNew.show()
        applyInner.pack_start(self._btnCreateNew, False, False, 0)

        createNewDesc = Gtk.Label(label="Prompts for a name and creates a fresh named PTXprint configuration.")
        createNewDesc.set_xalign(0.0)
        createNewDesc.set_line_wrap(True)
        createNewDesc.get_style_context().add_class("dim-label")
        createNewDesc.show()
        applyInner.pack_start(createNewDesc, False, False, 0)

        sep1 = Gtk.Separator()
        sep1.show()
        applyInner.pack_start(sep1, False, False, 0)

        self._btnApplyCurrent = Gtk.Button(label="Apply to current configuration")
        self._btnApplyCurrent.set_hexpand(True)
        self._btnApplyCurrent.connect("clicked", self._onApplyCurrent)
        self._btnApplyCurrent.show()
        applyInner.pack_start(self._btnApplyCurrent, False, False, 0)

        applyCurrentDesc = Gtk.Label(label="Shows a diff of changes, then applies to the currently active configuration.")
        applyCurrentDesc.set_xalign(0.0)
        applyCurrentDesc.set_line_wrap(True)
        applyCurrentDesc.get_style_context().add_class("dim-label")
        applyCurrentDesc.show()
        applyInner.pack_start(applyCurrentDesc, False, False, 0)

        sep2 = Gtk.Separator()
        sep2.show()
        applyInner.pack_start(sep2, False, False, 0)

        self._btnCloseNo = Gtk.Button(label="Close without applying")
        self._btnCloseNo.connect("clicked", self._onCloseNo)
        self._btnCloseNo.show()
        applyInner.pack_start(self._btnCloseNo, False, False, 0)

        applyInner.show()
        applyFrame.add(applyInner)
        applyFrame.show()
        self.pack_start(applyFrame, False, False, 0)

    def _onCreateNew(self, _btn):
        if self._applyNewCb:
            self._applyNewCb()

    def _onApplyCurrent(self, _btn):
        if self._applyCurrentCb:
            self._applyCurrentCb()

    def _onCloseNo(self, _btn):
        if self._closeNoCb:
            self._closeNoCb()

    def refresh(self, state, pageCount, spineWidth, perCopy, total, violations):
        """Repopulate all review content from current state."""
        self._refreshSummary(state)
        self._refreshEstimates(pageCount, spineWidth, perCopy, total)
        self._refreshWarnings(violations)

    def _refreshSummary(self, state):
        for child in list(self._summaryBox.get_children()):
            self._summaryBox.remove(child)

        sections = [
            ("audience",    AUDIENCE_LABELS,   vars(state.audience)),
            ("production",  PRODUCTION_LABELS, vars(state.production)),
            ("trimBinding", TRIM_LABELS,        vars(state.trimBinding)),
            ("content",     CONTENT_LABELS,     vars(state.content)),
            ("layout",      LAYOUT_LABELS,      vars(state.layout)),
        ]

        for sectionId, labels, values in sections:
            sectionLbl = Gtk.Label()
            sectionLbl.set_markup(f"<b>{SECTION_LABELS.get(sectionId, sectionId)}</b>")
            sectionLbl.set_xalign(0.0)
            sectionLbl.show()
            self._summaryBox.pack_start(sectionLbl, False, False, 0)

            hasAny = False
            for field, label in labels.items():
                val = values.get(field)
                if val is None or val == [] or val is False:
                    continue
                hasAny = True
                row = makeHBox(spacing=8)
                keyLbl = Gtk.Label(label=f"  {label}:")
                keyLbl.set_xalign(0.0)
                keyLbl.set_width_chars(22)
                keyLbl.show()
                valLbl = Gtk.Label(label=str(val))
                valLbl.set_xalign(0.0)
                valLbl.set_hexpand(True)
                valLbl.show()

                if self._jumpCb:
                    editBtn = Gtk.Button(label="Edit")
                    editBtn.set_relief(Gtk.ReliefStyle.NONE)
                    editBtn.set_valign(Gtk.Align.CENTER)
                    editBtn.connect("clicked", lambda _b, sid=sectionId: self._jumpCb(sid))
                    editBtn.show()
                    row.pack_end(editBtn, False, False, 0)

                row.pack_start(keyLbl, False, False, 0)
                row.pack_start(valLbl, True, True, 0)
                row.show()
                self._summaryBox.pack_start(row, False, False, 0)

            if not hasAny:
                notSet = Gtk.Label(label="  (not set)")
                notSet.set_xalign(0.0)
                notSet.get_style_context().add_class("dim-label")
                notSet.show()
                self._summaryBox.pack_start(notSet, False, False, 0)

            periph = state.peripherals.selected
            if sectionId == "layout" and periph:
                periLbl = Gtk.Label()
                periLbl.set_markup("<b>Peripherals</b>")
                periLbl.set_xalign(0.0)
                periLbl.show()
                self._summaryBox.pack_start(periLbl, False, False, 0)
                periValLbl = Gtk.Label(label="  " + ", ".join(periph))
                periValLbl.set_xalign(0.0)
                periValLbl.set_line_wrap(True)
                periValLbl.show()
                self._summaryBox.pack_start(periValLbl, False, False, 0)

    def _refreshEstimates(self, pageCount, spineWidth, perCopy, total):
        for child in list(self._estimatesBox.get_children()):
            self._estimatesBox.remove(child)

        def addRow(label, value):
            row = makeHBox(spacing=8)
            lbl = Gtk.Label(label=f"{label}:")
            lbl.set_width_chars(22)
            lbl.set_xalign(0.0)
            lbl.show()
            val = Gtk.Label(label=value)
            val.set_xalign(0.0)
            val.show()
            row.pack_start(lbl, False, False, 0)
            row.pack_start(val, True, True, 0)
            row.show()
            self._estimatesBox.pack_start(row, False, False, 0)

        addRow("Estimated page count", f"~{pageCount}" if pageCount else "—")
        addRow("Estimated spine width", f"~{spineWidth} mm" if spineWidth else "—")
        addRow("Per-copy cost band", perCopy or "—")
        addRow("Total cost band", total or "—")

    def _refreshWarnings(self, violations):
        for child in list(self._warningsBox.get_children()):
            self._warningsBox.remove(child)

        if not violations:
            self._warningsFrame.hide()
            return

        self._warningsFrame.show()
        for v in violations:
            sev = v.get("severity", "warning")
            icon = "⛔" if sev == "error" else "⚠"
            lbl = Gtk.Label(label=f"{icon}  {v['message']}")
            lbl.set_xalign(0.0)
            lbl.set_line_wrap(True)
            lbl.show()
            self._warningsBox.pack_start(lbl, False, False, 0)

    def loadFromState(self, state):
        pass  # refreshed explicitly via refresh()

    def saveToState(self, state):
        pass

    def isComplete(self):
        return True
