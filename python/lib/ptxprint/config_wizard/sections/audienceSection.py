import logging
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .sectionBase import (SectionPanel, makeVBox, makeHBox, makeCombo,
                           makeSpinner, makeFrame, makeSectionTitle, makeInfoRow)

logger = logging.getLogger(__name__)

PURPOSE_ITEMS = [
    ("pewBible",          "Pew Bible — for use in church services"),
    ("evangelism",        "Evangelism — for distribution outreach"),
    ("personalReading",   "Personal Reading — devotional use"),
    ("trial",             "Trial / Draft — community feedback run"),
    ("study",             "Study — for in-depth Scripture study"),
    ("childrensScripture","Children's Scripture portion"),
]

AGE_ITEMS = [
    ("children", "Children"),
    ("youth",    "Youth"),
    ("adult",    "Adult"),
    ("elderly",  "Elderly"),
    ("mixed",    "Mixed / General"),
]

EYESIGHT_ITEMS = [
    ("standard",       "Standard"),
    ("largePrint",     "Large Print (12pt+)"),
    ("veryLargePrint", "Very Large Print (16pt+)"),
]

CONTEXT_ITEMS = [
    ("pulpit",  "Pulpit — large reference Bible"),
    ("pew",     "Pew — church seating use"),
    ("personal","Personal — home and travel"),
    ("field",   "Field — rugged outdoor use"),
    ("study",   "Study — desk reference"),
]

LITERACY_ITEMS = [
    ("newReader",  "New / Emerging reader"),
    ("developing", "Developing reader"),
    ("fluent",     "Fluent reader"),
]

DISTRIBUTION_ITEMS = [
    ("sold",         "Sold — purchase price covers costs"),
    ("donorFunded",  "Donor-funded — subsidised or grant-supported"),
    ("free",         "Free distribution"),
]

BUDGET_ITEMS = [
    ("low",          "Low — minimise cost per copy"),
    ("medium",       "Medium — balance quality and cost"),
    ("high",         "High — quality is the priority"),
    ("unconstrained","Unconstrained"),
]


class AudienceSection(SectionPanel):
    sectionId = "audience"

    def _buildUi(self):
        self.pack_start(makeSectionTitle("Who is this Scripture for?"), False, False, 0)

        # Purpose — radio group
        purposeFrame = makeFrame("Publication purpose")
        purposeInner = makeVBox(spacing=4)
        purposeInner.set_margin_start(8)
        purposeInner.set_margin_end(8)
        purposeInner.set_margin_top(6)
        purposeInner.set_margin_bottom(6)

        self._purposeRadios = {}
        group = None
        for purposeId, purposeLabel in PURPOSE_ITEMS:
            radio = Gtk.RadioButton.new_with_label_from_widget(group, purposeLabel)
            radio.show()
            if group is None:
                group = radio
            radio.connect("toggled", self._onPurposeToggled, purposeId)
            purposeInner.pack_start(radio, False, False, 0)
            self._purposeRadios[purposeId] = radio

        purposeInner.show()
        purposeFrame.add(purposeInner)
        purposeFrame.show()
        self.pack_start(purposeFrame, False, False, 0)

        # Copy count
        self._copyCountSpin = makeSpinner(100, 1, 999999, step=1.0, digits=0)
        self._copyCountSpin.connect("value-changed", self._onChange)
        self.pack_start(makeInfoRow(
            "Number of copies",
            self._copyCountSpin,
            "How many copies do you need? This affects which production methods and cost levels are practical."
        ), False, False, 0)

        # Age group
        self._ageCombo = makeCombo(AGE_ITEMS)
        self._ageCombo.connect("changed", self._onChange)
        self.pack_start(makeInfoRow(
            "Primary age group",
            self._ageCombo,
            "Influences font size recommendations and layout defaults."
        ), False, False, 0)

        # Eyesight
        self._eyesightCombo = makeCombo(EYESIGHT_ITEMS)
        self._eyesightCombo.connect("changed", self._onChange)
        self.pack_start(makeInfoRow(
            "Eyesight consideration",
            self._eyesightCombo,
            "Large-print editions use a larger body font. This triggers a minimum font size recommendation."
        ), False, False, 0)

        # Reading context
        self._contextCombo = makeCombo(CONTEXT_ITEMS)
        self._contextCombo.connect("changed", self._onChange)
        self.pack_start(makeInfoRow(
            "Reading context",
            self._contextCombo,
            "Where will this Scripture be read? Affects size, margin, and binding recommendations."
        ), False, False, 0)

        # Literacy level
        self._literacyCombo = makeCombo(LITERACY_ITEMS)
        self._literacyCombo.connect("changed", self._onChange)
        self.pack_start(makeInfoRow(
            "Reader literacy level",
            self._literacyCombo,
            "New readers benefit from larger fonts, wider line spacing, and single-column layouts."
        ), False, False, 0)

        # Distribution model
        self._distributionCombo = makeCombo(DISTRIBUTION_ITEMS)
        self._distributionCombo.connect("changed", self._onChange)
        self.pack_start(makeInfoRow(
            "Distribution model",
            self._distributionCombo,
            "How will readers receive this Scripture? Affects cost sensitivity."
        ), False, False, 0)

        # Budget
        self._budgetCombo = makeCombo(BUDGET_ITEMS)
        self._budgetCombo.connect("changed", self._onChange)
        self.pack_start(makeInfoRow(
            "Budget level",
            self._budgetCombo,
            "A rough guide for cost recommendations. Does not affect layout."
        ), False, False, 0)

    def _onPurposeToggled(self, radio, purposeId):
        if not self._loading and radio.get_active():
            self._emitStateChanged()

    def _onChange(self, *_args):
        self._emitStateChanged()

    def _getActivePurpose(self):
        for purposeId, radio in self._purposeRadios.items():
            if radio.get_active():
                return purposeId
        return None

    def loadFromState(self, state):
        self._loading = True
        aud = state.audience

        if aud.purpose and aud.purpose in self._purposeRadios:
            self._purposeRadios[aud.purpose].set_active(True)

        if aud.copyCount is not None:
            self._copyCountSpin.set_value(aud.copyCount)

        if aud.ageGroup:
            self._ageCombo.set_active_id(aud.ageGroup)

        if aud.eyesightConsideration:
            self._eyesightCombo.set_active_id(aud.eyesightConsideration)

        if aud.readingContext:
            self._contextCombo.set_active_id(aud.readingContext)

        if aud.literacyLevel:
            self._literacyCombo.set_active_id(aud.literacyLevel)

        if aud.distributionModel:
            self._distributionCombo.set_active_id(aud.distributionModel)

        if aud.budgetLevel:
            self._budgetCombo.set_active_id(aud.budgetLevel)

        self._loading = False

    def saveToState(self, state):
        state.audience.purpose = self._getActivePurpose()
        state.audience.copyCount = int(self._copyCountSpin.get_value())
        state.audience.ageGroup = self._ageCombo.get_active_id()
        state.audience.eyesightConsideration = self._eyesightCombo.get_active_id()
        state.audience.readingContext = self._contextCombo.get_active_id()
        state.audience.literacyLevel = self._literacyCombo.get_active_id()
        state.audience.distributionModel = self._distributionCombo.get_active_id()
        state.audience.budgetLevel = self._budgetCombo.get_active_id()

    def isComplete(self):
        return all([
            self._getActivePurpose() is not None,
            self._copyCountSpin.get_value() >= 1,
            self._ageCombo.get_active_id() is not None,
            self._eyesightCombo.get_active_id() is not None,
            self._contextCombo.get_active_id() is not None,
            self._literacyCombo.get_active_id() is not None,
            self._distributionCombo.get_active_id() is not None,
            self._budgetCombo.get_active_id() is not None,
        ])
