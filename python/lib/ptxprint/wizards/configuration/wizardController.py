"""PTXprint Publication Wizard — main controller (v2).

Integration points
------------------
PTXprint:
    from ptxprint.wizards.configuration import launchWizard
    launchWizard(ptxprintGtkViewModel, parentWindow)

Standalone (for testing / future headless use):
    python -m ptxprint.wizards.configuration <projectDir> <configName>
"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib, Pango
import os
import json
import math
import logging

try:
    import jsonschema
    _HAS_JSONSCHEMA = True
except ImportError:
    _HAS_JSONSCHEMA = False

from ptxprint.wizards.configuration import wizardState, wizardValidation
from ptxprint.wizards.configuration.wizardMapping import applyAnswers, PAGE_SIZE_PRESETS
from ptxprint.utils import getSrcDir
try:
    from ptxprint.utils import _
except ImportError:
    def _(s): return s

logger = logging.getLogger(__name__)

_WIZARD_DIR   = getSrcDir()
_GLADE_FILE   = os.path.join(_WIZARD_DIR, "wizardDialog.glade")
_QUESTIONS_FILE = os.path.join(_WIZARD_DIR, "wizardQuestions.json")
_SCHEMA_FILE  = os.path.join(_WIZARD_DIR, "wizardQuestions.schema.json")

_MAIN_PANE_WIDTH = 520
_SIDE_PANE_WIDTH = 300


def _interpNotch(idx_f, notches):
    """Return an integer value by linear interpolation between notch values at fractional index idx_f."""
    if not notches:
        return 0
    idx_lo = max(0, min(int(idx_f), len(notches) - 2))
    idx_hi = idx_lo + 1
    frac = idx_f - idx_lo
    return int(round(notches[idx_lo] + frac * (notches[idx_hi] - notches[idx_lo])))


def _findFracIdx(val, notches):
    """Return the fractional index in notches that corresponds to val by linear interpolation."""
    if not notches:
        return 0.0
    if val <= notches[0]:
        return 0.0
    if val >= notches[-1]:
        return float(len(notches) - 1)
    for i in range(len(notches) - 1):
        if notches[i] <= val <= notches[i + 1]:
            return i + (val - notches[i]) / (notches[i + 1] - notches[i])
    return float(len(notches) - 1)


def _loadPages():
    """Load and optionally validate wizardQuestions.json. Returns list of page dicts."""
    with open(_QUESTIONS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    if _HAS_JSONSCHEMA and os.path.exists(_SCHEMA_FILE):
        with open(_SCHEMA_FILE, encoding="utf-8") as f:
            schema = json.load(f)
        try:
            jsonschema.validate(data, schema)
        except jsonschema.ValidationError as e:
            raise RuntimeError("wizardQuestions.json schema validation failed: " + str(e)) from e
    version = data.get("version", 1)
    if version >= 2:
        return data["pages"]
    # v1 compatibility: wrap each question in a minimal page object
    pages = []
    for q in data.get("questions", []):
        pages.append({
            "id": q["id"],
            "step": q.get("step", "intent"),
            "titleString": q.get("label", ""),
            "helpString": q.get("help", ""),
            "tooltipString": q.get("label", q["id"])[:20],
            "showIf": q.get("showIf"),
            "staticPanel": None,
            "questions": [q],
        })
    return pages


class WizardController:
    """Controls the wizard dialog lifecycle.

    Parameters
    ----------
    model : object with .get(wid) and .set(wid, value, skipmissing=True)
        The PTXprint ViewModel. Pass None for pure-standalone mode.
    projectDir : str
    configName : str
    parentWindow : Gtk.Window or None
    ptxprintVersion : str
    onApply : callable(answers) or None
    """

    def __init__(self, model, projectDir, configName, parentWindow=None,
                 ptxprintVersion="", onApply=None):
        self.model = model
        self.projectDir = projectDir
        self.configName = configName
        self.parentWindow = parentWindow
        self.ptxprintVersion = ptxprintVersion
        self.onApply = onApply

        self.pages = _loadPages()
        self.answers = wizardState.loadState(projectDir, configName)
        self._snapshot = {}
        self._hoverPageSize = None

        self._buildUI()
        self._pageIndex = 0
        self._pages = []   # list of (pageId | "welcome" | "summary", GtkWidget)
        self._buildPages()
        self._goTo(0)

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _buildUI(self):
        builder = Gtk.Builder()
        builder.set_translation_domain("ptxprint")
        builder.add_from_file(_GLADE_FILE)
        self._builder = builder

        self._dialog = builder.get_object("dlg_wizard")
        if self.parentWindow:
            self._dialog.set_transient_for(self.parentWindow)

        self._stack       = builder.get_object("stk_pages")
        self._lblStep     = builder.get_object("lbl_stepCount")
        self._da          = builder.get_object("da_progressDots")
        self._btnBack     = builder.get_object("btn_back")
        self._btnNext     = builder.get_object("btn_next")
        self._btnReset    = builder.get_object("btn_reset")
        self._btnCancel   = builder.get_object("btn_cancel")
        self._btnApplyFt  = builder.get_object("btn_apply_footer")
        self._btnCreateNew = builder.get_object("btn_createNew")

        self._btnBack.connect("clicked", self._onBack)
        self._btnNext.connect("clicked", self._onNext)
        self._btnReset.connect("clicked", self._onReset)
        self._btnCancel.connect("clicked", self._onCancel)
        self._btnApplyFt.connect("clicked", self._onApply)
        self._btnCreateNew.connect("clicked", self._onCreateNew)

        self._da.connect("draw", self._drawProgressDots)
        self._da.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                            Gdk.EventMask.POINTER_MOTION_MASK |
                            Gdk.EventMask.LEAVE_NOTIFY_MASK)
        self._da.set_has_tooltip(True)
        self._da.connect("button-press-event", self._onDotClicked)
        self._da.connect("query-tooltip", self._onDotTooltip)
        self._dialog.connect("key-press-event", self._onKeyPress)
        self._dialog.connect("delete-event", self._onDeleteEvent)

        self._dialog.set_default(self._btnNext)

    def _buildPages(self):
        self._pages = [("welcome", self._makeWelcomePage())]

        for page in self.pages:
            widget = self._makePageWidget(page)
            self._pages.append((page["id"], widget))

        self._pages.append(("summary", self._makeSummaryPage()))

        for _pid, widget in self._pages:
            widget.show_all()
            self._stack.add(widget)

    # ------------------------------------------------------------------
    # Page factories
    # ------------------------------------------------------------------

    def _makeScrolledPage(self):
        """Create a GtkScrolledWindow that serves as the page container."""
        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sw.set_overlay_scrolling(False)   # always-visible scrollbar per §5.5
        return sw

    def _makeWelcomePage(self):
        sw = self._makeScrolledPage()
        hbox = self._makeTwoPaneLayout()
        main_box, side_lbl = hbox._mainBox, hbox._sideLabel

        h1 = self._makeHeading(_("Let's set up your publication."))
        main_box.pack_start(h1, False, False, 0)

        body = Gtk.Label(label=_("A few quick questions, then PTXprint will pick good starting settings for you. You can change anything later."))
        body.set_xalign(0)
        body.set_line_wrap(True)
        body.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        body.get_style_context().add_class("dim-label")
        main_box.pack_start(body, False, False, 4)

        if self.answers:
            lnk = Gtk.LinkButton.new_with_label("", _("Skip to summary →"))
            lnk.connect("activate-link", self._onSkipToSummary)
            main_box.pack_start(lnk, False, False, 8)

        side_lbl.set_markup(_("<b>Starting point</b>\n\nThis wizard sets up a starting configuration. You can fine-tune everything in the main PTXprint window afterwards.\n\nNothing is saved until you click Apply."))

        sw.add(hbox)
        sw._sideLabel = side_lbl
        return sw

    def _makePageWidget(self, page):
        """Build a two-pane scrolled page for a given page dict."""
        sw = self._makeScrolledPage()
        hbox = self._makeTwoPaneLayout()
        main_box, side_lbl, side_box = hbox._mainBox, hbox._sideLabel, hbox._sideBox

        h1 = self._makeHeading(_(page["titleString"]))
        main_box.pack_start(h1, False, False, 0)

        helpStr = page.get("helpString", "")
        if helpStr:
            lbl = Gtk.Label(label=_(helpStr))
            lbl.set_xalign(0)
            lbl.set_line_wrap(True)
            lbl.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
            lbl.get_style_context().add_class("dim-label")
            main_box.pack_start(lbl, False, False, 2)

        # A4 visual preview for the page-size selection page
        if page["id"] == "productionPageSize":
            # Reserve a fixed height for the text area so the graphic doesn't jump
            # as descriptions of different lengths are shown on hover (~5 text lines)
            side_lbl.set_size_request(-1, 104)
            da = Gtk.DrawingArea()
            preview_w = _SIDE_PANE_WIDTH - 24
            preview_h = int(preview_w * 297 / 210)
            da.set_size_request(preview_w, preview_h)
            da.connect("draw", self._drawPageSizePreview)
            # side_lbl was packed first in _makeTwoPaneLayout, so da goes below it
            side_box.pack_start(da, False, False, 0)
            self._pageSizePreviewDa = da

        # Render each visible question
        questions = page.get("questions", [])
        for q in questions:
            if not wizardValidation.evaluateShowIf(q.get("showIf"), self.answers):
                placeholder = Gtk.Box()
                placeholder.set_name("qhidden_" + q["id"])
                main_box.pack_start(placeholder, False, False, 0)
                continue
            self._appendQuestionWidget(main_box, q, len(questions) > 1, side_lbl)

        # Static side panel text for pages without option-level pros/cons
        staticPanel = page.get("staticPanel")
        if staticPanel:
            side_lbl.set_text(_(staticPanel))
        elif not any(q["type"] in ("singleSelect", "multiSelect")
                     for q in questions):
            side_lbl.set_text("")

        sw.add(hbox)
        sw._mainBox   = main_box
        sw._sideLabel = side_lbl
        sw._page      = page
        return sw

    def _appendQuestionWidget(self, container, q, showSubLabel, side_lbl):
        """Render one question into a named qblock container and pack into container."""
        qblock = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        qblock.set_name("qblock_" + q["id"])

        sectionLabel = q.get("sectionLabel")
        if sectionLabel:
            sl = Gtk.Label(label=_(sectionLabel))
            sl.set_xalign(0)
            attrs = Pango.AttrList()
            attrs.insert(Pango.attr_weight_new(Pango.Weight.SEMIBOLD))
            sl.set_attributes(attrs)
            qblock.pack_start(sl, False, False, 8)

        if showSubLabel and q.get("label"):
            sub_lbl = Gtk.Label(label=_(q["label"]))
            sub_lbl.set_xalign(0)
            attrs = Pango.AttrList()
            attrs.insert(Pango.attr_weight_new(Pango.Weight.SEMIBOLD))
            sub_lbl.set_attributes(attrs)
            qblock.pack_start(sub_lbl, False, False, 8)

        if q.get("help"):
            h_lbl = Gtk.Label(label=_(q["help"]))
            h_lbl.set_xalign(0)
            h_lbl.set_line_wrap(True)
            h_lbl.get_style_context().add_class("dim-label")
            qblock.pack_start(h_lbl, False, False, 2)

        qtype = q["type"]
        if qtype == "singleSelect":
            w = self._makeSingleSelect(q, side_lbl)
        elif qtype == "multiSelect":
            w = self._makeMultiSelect(q, side_lbl)
        elif qtype == "notchedSlider":
            w = self._makeNotchedSlider(q)
        elif qtype == "centredSlider":
            w = self._makeCentredSlider(q)
        else:
            w = Gtk.Label(label=_("(unsupported question type: {})").format(qtype))

        w.set_name("inputArea_" + q["id"])
        qblock.pack_start(w, False, False, 8)
        container.pack_start(qblock, False, False, 0)

    def _makeSummaryPage(self):
        sw = self._makeScrolledPage()
        hbox = self._makeTwoPaneLayout()
        main_box, side_lbl = hbox._mainBox, hbox._sideLabel

        h1 = self._makeHeading(_("Here's what you've chosen."))
        main_box.pack_start(h1, False, False, 0)

        side_lbl.set_markup(_("<b>Almost done</b>\n\nCheck your answers. Click Edit to change anything.\n\nWhen ready, click <b>Apply to current</b> or <b>Create new configuration</b>."))

        # Warning banner (hidden by default)
        self._warningBanner = Gtk.InfoBar()
        self._warningBanner.set_message_type(Gtk.MessageType.WARNING)
        self._warningLabel  = Gtk.Label(label="", wrap=True, xalign=0)
        self._warningLabel.set_line_wrap(True)
        self._warningBanner.get_content_area().pack_start(self._warningLabel, True, True, 0)
        self._warningBanner.set_no_show_all(True)
        main_box.pack_start(self._warningBanner, False, False, 0)

        # Summary grid (filled in _refreshSummary)
        self._summaryGrid = Gtk.Grid()
        self._summaryGrid.set_row_spacing(3)
        self._summaryGrid.set_column_spacing(12)
        self._summaryGrid.set_margin_start(8)
        main_box.pack_start(self._summaryGrid, False, False, 4)

        sw.add(hbox)
        sw._mainBox   = main_box
        sw._sideLabel = side_lbl
        return sw

    # ------------------------------------------------------------------
    # Layout helpers
    # ------------------------------------------------------------------

    def _makeTwoPaneLayout(self):
        """Return an HBox with _mainBox (left), _sideLabel and _sideBox (right) attached."""
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        hbox.set_margin_top(24)
        hbox.set_margin_bottom(24)
        hbox.set_margin_start(24)
        hbox.set_margin_end(24)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        main_box.set_size_request(_MAIN_PANE_WIDTH, -1)

        side_frame = Gtk.Frame()
        side_frame.set_shadow_type(Gtk.ShadowType.NONE)
        side_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        side_box.set_size_request(_SIDE_PANE_WIDTH, -1)
        side_box.set_margin_start(8)

        side_lbl = Gtk.Label()
        side_lbl.set_line_wrap(True)
        side_lbl.set_xalign(0)
        side_lbl.set_yalign(0)
        side_lbl.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        side_box.pack_start(side_lbl, False, False, 0)
        side_frame.add(side_box)

        hbox.pack_start(main_box, False, False, 0)
        hbox.pack_start(side_frame, True, True, 0)
        hbox._mainBox   = main_box
        hbox._sideLabel = side_lbl
        hbox._sideBox   = side_box
        return hbox

    def _makeHeading(self, text):
        h1 = Gtk.Label(label=text)
        h1.set_xalign(0)
        h1.set_line_wrap(True)
        h1.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        attrs = Pango.AttrList()
        attrs.insert(Pango.attr_weight_new(Pango.Weight.BOLD))
        attrs.insert(Pango.attr_scale_new(1.3))
        h1.set_attributes(attrs)
        return h1

    # ------------------------------------------------------------------
    # Widget helpers — question types
    # ------------------------------------------------------------------

    def _makeSingleSelect(self, q, side_lbl=None):
        visible_options = wizardValidation.visibleOptions(q, self.answers)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        group = None
        stored  = self.answers.get(q["id"])
        default = wizardValidation.resolveDefault(q, self.answers)

        for opt in visible_options:
            level, reason = wizardValidation.evaluateRecommendIf(opt, self.answers)

            rb = Gtk.RadioButton.new_with_label_from_widget(group, "")
            group = rb
            rb._optId = opt["id"]

            # Option card: label + description + rangeLabel + badge
            vb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)

            # Header row: main label + optional range label
            hrow = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            lbl_main = Gtk.Label(label=_(opt["label"]))
            lbl_main.set_xalign(0)
            attrs = Pango.AttrList()
            attrs.insert(Pango.attr_weight_new(Pango.Weight.SEMIBOLD))
            if level == "notAdvised":
                attrs.insert(Pango.attr_strikethrough_new(True))
                lbl_main.get_style_context().add_class("dim-label")
            elif level == "notOptimal":
                lbl_main.get_style_context().add_class("dim-label")
            lbl_main.set_attributes(attrs)
            hrow.pack_start(lbl_main, False, False, 0)

            rangeLabel = opt.get("rangeLabel", "")
            if rangeLabel:
                rl = Gtk.Label(label=_(rangeLabel))
                rl.set_xalign(1)
                rl.get_style_context().add_class("dim-label")
                hrow.pack_end(rl, False, False, 0)
            vb.pack_start(hrow, False, False, 0)

            if opt.get("description"):
                lbl_desc = Gtk.Label(label=_(opt["description"]))
                lbl_desc.set_xalign(0)
                lbl_desc.get_style_context().add_class("dim-label")
                vb.pack_start(lbl_desc, False, False, 0)

            # Recommendation badge
            if level == "recommended":
                badge = Gtk.Label()
                badge.set_markup('<span foreground="#2e7d32">✓ {}</span>'.format(_("Recommended")))
                badge.set_xalign(0)
                vb.pack_start(badge, False, False, 0)
            elif level == "notOptimal" and reason:
                badge = Gtk.Label()
                badge.set_markup('<span foreground="#e65100">⚠ {}</span>'.format(_(reason)))
                badge.set_xalign(0)
                badge.set_line_wrap(True)
                vb.pack_start(badge, False, False, 0)
            elif level == "notAdvised" and reason:
                badge = Gtk.Label()
                badge.set_markup('<span foreground="#c62828">✗ {}</span>'.format(_(reason)))
                badge.set_xalign(0)
                badge.set_line_wrap(True)
                vb.pack_start(badge, False, False, 0)

            rb.get_child().destroy()
            rb.add(vb)

            rb.set_sensitive(level != "notAdvised")

            rb.connect("toggled", self._onSingleSelectToggled, q["id"])
            if side_lbl is not None:
                rb.connect("toggled", lambda w, ql, ol: self._updateSidePanelForOption(ql, ol, side_lbl) if w.get_active() else None, q, opt)
                rb.connect("enter-notify-event", lambda w, e, ql, ol: self._onOptionHover(ql, ol, side_lbl), q, opt)
                if q["id"] == "pageSize":
                    rb.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)
                    rb.connect("leave-notify-event", lambda w, e: self._onPageSizeLeave(e))

            box.pack_start(rb, False, False, 2)

            if level != "notAdvised":
                if (stored is not None and opt["id"] == stored) or \
                   (stored is None and opt["id"] == default):
                    rb.set_active(True)
                    if side_lbl is not None:
                        self._updateSidePanelForOption(q, opt, side_lbl)

        box._questionId = q["id"]
        return box

    def _makeMultiSelect(self, q, side_lbl=None):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        stored  = self.answers.get(q["id"], []) or []
        default = wizardValidation.resolveDefault(q, self.answers) or []
        maxSel  = q.get("maxSelections", 99)

        for opt in q.get("options", []):
            cb = Gtk.CheckButton(label="")
            cb._optId = opt["id"]
            vb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
            lbl_main = Gtk.Label(label=_(opt["label"]))
            lbl_main.set_xalign(0)
            attrs = Pango.AttrList()
            attrs.insert(Pango.attr_weight_new(Pango.Weight.SEMIBOLD))
            lbl_main.set_attributes(attrs)
            vb.pack_start(lbl_main, False, False, 0)
            if opt.get("description"):
                lbl_desc = Gtk.Label(label=_(opt["description"]))
                lbl_desc.set_xalign(0)
                lbl_desc.get_style_context().add_class("dim-label")
                vb.pack_start(lbl_desc, False, False, 0)
            cb.get_child().destroy()
            cb.add(vb)
            active_list = stored if stored else default
            cb.set_active(opt["id"] in active_list)
            cb.connect("toggled", self._onMultiSelectToggled, q["id"], maxSel)
            if side_lbl is not None:
                cb.connect("toggled", lambda w, ql, ol: self._updateSidePanelForOption(ql, ol, side_lbl) if w.get_active() else None, q, opt)
                cb.connect("enter-notify-event", lambda w, e, ql, ol: self._updateSidePanelForOption(ql, ol, side_lbl), q, opt)
            box.pack_start(cb, False, False, 2)

        box._questionId = q["id"]
        return box

    def _makeNotchedSlider(self, q):
        notches     = q.get("notches", [])
        notchLabels = q.get("notchLabels", [str(n) for n in notches])
        stored  = self.answers.get(q["id"])
        default = wizardValidation.resolveDefault(q, self.answers)

        upper = float(max(len(notches) - 1, 1))
        adj = Gtk.Adjustment(value=0.0, lower=0.0, upper=upper,
                             step_increment=0.01, page_increment=0.1)
        scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj)
        scale.set_draw_value(False)
        scale.set_digits(2)
        scale.set_hexpand(True)

        for i, lbl in enumerate(notchLabels):
            scale.add_mark(float(i), Gtk.PositionType.BOTTOM, lbl)

        lbl_value = Gtk.Label()
        lbl_value.set_xalign(0.5)

        def _update_label(sc):
            val = _interpNotch(sc.get_value(), notches)
            unit = _("pages") if q["id"] == "pageCount" else ""
            lbl_value.set_markup("<b>{}</b>{}".format(val, " " + unit if unit else ""))

        scale.connect("value-changed", _update_label)
        scale.connect("value-changed", lambda sc: self._onSliderChanged(sc, q["id"], notches))

        init_val = stored if stored is not None else default
        if init_val is not None:
            adj.set_value(_findFracIdx(init_val, notches))
        _update_label(scale)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        box.pack_start(scale, False, False, 0)
        box.pack_start(lbl_value, False, False, 0)
        box._questionId = q["id"]
        return box

    def _makeCentredSlider(self, q):
        stored  = self.answers.get(q["id"])
        default = wizardValidation.resolveDefault(q, self.answers)
        init    = stored if stored is not None else (default if default is not None else 0.5)

        adj = Gtk.Adjustment(value=float(init), lower=0.0, upper=1.0,
                             step_increment=0.1, page_increment=0.25)
        scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj)
        scale.set_draw_value(False)
        scale.set_hexpand(True)
        scale.add_mark(0.0, Gtk.PositionType.BOTTOM, _(q.get("leftLabel", "")))
        scale.add_mark(0.5, Gtk.PositionType.BOTTOM, _(q.get("centreLabel", "")))
        scale.add_mark(1.0, Gtk.PositionType.BOTTOM, _(q.get("rightLabel", "")))
        scale.connect("value-changed", lambda sc: self._onSliderChanged(sc, q["id"], None))

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        box.pack_start(scale, False, False, 0)
        box._questionId = q["id"]
        return box

    # ------------------------------------------------------------------
    # Side panel
    # ------------------------------------------------------------------

    def _updateSidePanelForOption(self, question, option, side_lbl):
        """Update the side panel label for a hovered/selected option."""
        parts = []
        level, reason = wizardValidation.evaluateRecommendIf(option, self.answers)
        if level and reason:
            if level == "recommended":
                parts.append('<span foreground="#2e7d32"><b>✓ {}</b></span>\n{}'.format(
                    _("Recommended"), _(reason)))
            elif level == "notOptimal":
                parts.append('<span foreground="#e65100"><b>⚠ {}</b></span>\n{}'.format(
                    _("Not the ideal choice"), _(reason)))
            elif level == "notAdvised":
                parts.append('<span foreground="#c62828"><b>✗ {}</b></span>\n{}'.format(
                    _("Not advised"), _(reason)))

        desc = option.get("description", "")
        if desc:
            parts.append(_(desc))

        pros = option.get("pros", [])
        if pros:
            parts.append("<b>{}</b>".format(_("Pros")))
            parts.extend("  • " + _(p) for p in pros)

        cons = option.get("cons", [])
        if cons:
            parts.append("<b>{}</b>".format(_("Cons")))
            parts.extend("  • " + _(c) for c in cons)

        side_lbl.set_markup("\n".join(parts) if parts else "")

    def _onOptionHover(self, question, option, side_lbl):
        """Handle mouse entering a radio/checkbox option: update side text and preview."""
        self._updateSidePanelForOption(question, option, side_lbl)
        if question["id"] == "pageSize" and hasattr(self, "_pageSizePreviewDa"):
            self._hoverPageSize = option["id"]
            self._pageSizePreviewDa.queue_draw()

    def _onPageSizeLeave(self, event):
        """Clear the hover preview when the pointer truly leaves a page-size radio button."""
        if event.detail == Gdk.NotifyType.INFERIOR:
            return  # moved to a child widget, not actually leaving
        self._hoverPageSize = None
        if hasattr(self, "_pageSizePreviewDa"):
            self._pageSizePreviewDa.queue_draw()

    def _drawPageSizePreview(self, da, cr):
        """Draw A4 reference outline with selected page size centred inside it."""
        w = da.get_allocated_width()
        h = da.get_allocated_height()

        ps_id = self._hoverPageSize or \
                self.answers.get("pageSize") or \
                wizardValidation.resolveDefault(self._findQuestion("pageSize") or {}, self.answers) or "a5"
        preset = PAGE_SIZE_PRESETS.get(ps_id) or PAGE_SIZE_PRESETS.get("a5")

        a4_w_mm, a4_h_mm = 210, 297
        sel_w_mm, sel_h_mm = preset["mm"]

        margin = 12
        scale = min((w - 2 * margin) / a4_w_mm, (h - 2 * margin) / a4_h_mm)

        a4_px_w = a4_w_mm * scale
        a4_px_h = a4_h_mm * scale
        a4_x = (w - a4_px_w) / 2
        a4_y = (h - a4_px_h) / 2

        sel_px_w = sel_w_mm * scale
        sel_px_h = sel_h_mm * scale
        sel_x = a4_x + (a4_px_w - sel_px_w) / 2
        sel_y = a4_y + (a4_px_h - sel_px_h) / 2

        style  = da.get_style_context()
        fg     = style.get_color(Gtk.StateFlags.NORMAL)
        accent = style.get_color(Gtk.StateFlags.SELECTED)

        # A4 background (light grey)
        cr.set_source_rgba(0.88, 0.88, 0.88, 1.0)
        cr.rectangle(a4_x, a4_y, a4_px_w, a4_px_h)
        cr.fill()
        cr.set_source_rgba(0.55, 0.55, 0.55, 1.0)
        cr.set_line_width(1.0)
        cr.rectangle(a4_x, a4_y, a4_px_w, a4_px_h)
        cr.stroke()

        # Selected size (white fill, accent border)
        cr.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        cr.rectangle(sel_x, sel_y, sel_px_w, sel_px_h)
        cr.fill()
        cr.set_source_rgba(accent.red, accent.green, accent.blue, 1.0)
        cr.set_line_width(2.0)
        cr.rectangle(sel_x, sel_y, sel_px_w, sel_px_h)
        cr.stroke()

        # Short label: take the part before " (" to avoid overflowing small sizes
        full_label = preset.get("label", ps_id)
        label = full_label.split(" (")[0]
        cr.set_source_rgba(fg.red, fg.green, fg.blue, 0.85)
        cr.select_font_face("Sans", 0, 0)   # 0 = FONT_SLANT_NORMAL, 0 = FONT_WEIGHT_NORMAL
        cr.set_font_size(min(11, max(8, sel_px_h / 8)))
        te = cr.text_extents(label)
        tx = sel_x + (sel_px_w - te[2]) / 2
        ty = sel_y + (sel_px_h + te[3]) / 2
        cr.move_to(tx, ty)
        cr.show_text(label)

    # ------------------------------------------------------------------
    # Signal handlers
    # ------------------------------------------------------------------

    def _onSingleSelectToggled(self, rb, questionId):
        if rb.get_active():
            self.answers[questionId] = rb._optId
            self._onAnswerChanged(questionId)

    def _onMultiSelectToggled(self, cb, questionId, maxSel):
        selected = self._getMultiSelectValue(questionId)
        if cb.get_active() and len(selected) > maxSel:
            cb.set_active(False)
            return
        val = self._getMultiSelectValue(questionId)
        self.answers[questionId] = val
        self._onAnswerChanged(questionId)

    def _onSliderChanged(self, sc, questionId, notches):
        if notches:
            val = _interpNotch(sc.get_value(), notches)
        else:
            val = sc.get_value()
        self.answers[questionId] = val
        self._onAnswerChanged(questionId)

    def _onAnswerChanged(self, questionId):
        q = self._findQuestion(questionId)
        if q:
            for affectedId in q.get("affects", []):
                self._refreshQuestionInPage(affectedId)
        if questionId == "pageSize" and hasattr(self, "_pageSizePreviewDa"):
            self._pageSizePreviewDa.queue_draw()
        self._updateNavigation()

    def _onBack(self, btn):
        self._goTo(self._prevVisibleIndex(self._pageIndex))

    def _onNext(self, btn):
        nextIdx = self._nextVisibleIndex(self._pageIndex)
        if nextIdx is None:
            return
        if nextIdx == len(self._pages) - 1:
            self._refreshSummary()
        self._goTo(nextIdx)

    def _onApply(self, btn):
        self._doApply(createNew=False)

    def _onCreateNew(self, btn):
        self._doApply(createNew=True)

    def _onCancel(self, btn):
        dlg = Gtk.MessageDialog(
            transient_for=self._dialog,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            text=_("Close without applying?"),
        )
        dlg.format_secondary_text(_("Your answers will be saved so you can continue later."))
        dlg.add_button(_("Keep working"), Gtk.ResponseType.CANCEL)
        dlg.add_button(_("Close"), Gtk.ResponseType.OK)
        dlg.set_default_response(Gtk.ResponseType.CANCEL)
        resp = dlg.run()
        dlg.destroy()
        if resp == Gtk.ResponseType.OK:
            wizardState.saveState(self.projectDir, self.configName,
                                  self.answers, self.ptxprintVersion)
            self._dialog.response(Gtk.ResponseType.CANCEL)

    def _doApply(self, createNew=False):
        newConfigName = None
        if createNew:
            newConfigName = self._promptConfigName()
            if newConfigName is None:
                return  # user cancelled name prompt

        if self.model is not None:
            try:
                self._snapshot = applyAnswers(self.answers, self.model)
            except Exception as e:
                logger.exception("Wizard apply failed")
                self._showApplyError(str(e))
                return

        wizardState.saveState(self.projectDir, self.configName,
                              self.answers, self.ptxprintVersion)
        self._dialog.response(Gtk.ResponseType.OK)

        if self.onApply:
            try:
                self.onApply(self.answers)
            except Exception:
                logger.exception("onApply callback raised")

        if createNew and newConfigName:
            self._showToast(_('Created configuration "{}" and applied your settings. You can fine-tune anything in the main window.').format(newConfigName))
        else:
            self._showToast(_("Settings applied. You can fine-tune anything in the main window."))

    def _configExists(self, configName):
        """Return True if a PTXprint configuration directory already exists for this project."""
        if not self.projectDir or not configName:
            return False
        config_dir = os.path.join(self.projectDir, "shared", "ptxprint", configName)
        return os.path.isdir(config_dir)

    def _promptConfigName(self):
        dlg = Gtk.Dialog(title=_("New configuration name"),
                         transient_for=self._dialog, modal=True)
        dlg.add_button(_("Cancel"), Gtk.ResponseType.CANCEL)
        btn_create = dlg.add_button(_("Create"), Gtk.ResponseType.OK)
        dlg.set_default_response(Gtk.ResponseType.OK)

        content = dlg.get_content_area()
        content.set_spacing(8)
        content.set_margin_start(12)
        content.set_margin_end(12)
        content.set_margin_top(12)
        content.set_margin_bottom(12)

        content.pack_start(
            Gtk.Label(label=_("Enter a name for the new configuration:")),
            False, False, 0)

        entry = Gtk.Entry()
        entry.set_activates_default(True)
        content.pack_start(entry, False, False, 0)

        warn_lbl = Gtk.Label()
        warn_lbl.set_markup(
            '<span foreground="#c62828">⚠ ' +
            _("A configuration with this name already exists.") + '</span>')
        warn_lbl.set_xalign(0)
        warn_lbl.set_no_show_all(True)
        content.pack_start(warn_lbl, False, False, 0)

        overwrite_cb = Gtk.CheckButton(
            label=_("Overwrite existing configuration"))
        overwrite_cb.set_no_show_all(True)
        content.pack_start(overwrite_cb, False, False, 0)

        def _refresh(*_):
            name = entry.get_text().strip()
            exists = self._configExists(name)
            if exists:
                warn_lbl.show()
                overwrite_cb.show()
            else:
                warn_lbl.hide()
                overwrite_cb.hide()
                overwrite_cb.set_active(False)
            btn_create.set_sensitive(bool(name) and (not exists or overwrite_cb.get_active()))

        entry.connect("changed", _refresh)
        overwrite_cb.connect("toggled", _refresh)
        btn_create.set_sensitive(False)

        dlg.show_all()
        warn_lbl.hide()
        overwrite_cb.hide()

        resp = dlg.run()
        name = entry.get_text().strip()
        overwrite = overwrite_cb.get_active()
        dlg.destroy()

        if resp == Gtk.ResponseType.OK and name:
            if self._configExists(name) and not overwrite:
                return None
            return name
        return None

    def _showApplyError(self, detail):
        dlg = Gtk.MessageDialog(
            transient_for=self._dialog,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.NONE,
            text=_("Could not apply settings."),
        )
        dlg.format_secondary_text(detail)
        copy_btn = dlg.add_button(_("Copy details"), 1)
        copy_btn.connect("clicked",
                         lambda b: Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).set_text(detail, -1))
        dlg.add_button(_("Close"), Gtk.ResponseType.CLOSE)
        dlg.run()
        dlg.destroy()

    def _onReset(self, btn):
        dlg = Gtk.MessageDialog(
            transient_for=self._dialog,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            text=_("Start again from the beginning?"),
        )
        dlg.format_secondary_text(_("Your current answers will be cleared."))
        dlg.add_button(_("Cancel"), Gtk.ResponseType.CANCEL)
        dlg.add_button(_("Yes, start again"), Gtk.ResponseType.OK)
        dlg.set_default_response(Gtk.ResponseType.CANCEL)
        resp = dlg.run()
        dlg.destroy()
        if resp == Gtk.ResponseType.OK:
            wizardState.deleteState(self.projectDir, self.configName)
            self.answers = {}
            self._hoverPageSize = None
            # Reset index before clearing the list so any signals fired during
            # teardown/rebuild cannot index into a partially-populated list
            self._pageIndex = 0
            for _pid, w in self._pages:
                self._stack.remove(w)
            self._pages = []
            if hasattr(self, "_pageSizePreviewDa"):
                del self._pageSizePreviewDa
            self._buildPages()
            self._goTo(0)

    def _onDeleteEvent(self, *_):
        wizardState.saveState(self.projectDir, self.configName,
                              self.answers, self.ptxprintVersion)
        return False

    def _onSkipToSummary(self, *_):
        self._refreshSummary()
        self._goTo(len(self._pages) - 1)
        return True

    def _onKeyPress(self, _widget, event):
        key = event.keyval
        if key in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            self._btnNext.clicked()
            return True
        if key == Gdk.KEY_Escape:
            self._onCancel(None)
            return True
        if event.state & Gdk.ModifierType.MOD1_MASK:
            if key == Gdk.KEY_Left:
                self._btnBack.clicked()
                return True
            if key == Gdk.KEY_Right:
                self._btnNext.clicked()
                return True
        return False

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _goTo(self, index):
        if index is None:
            return
        total = len(self._pages)
        index = max(0, min(index, total - 1))
        self._pageIndex = index
        pid, widget = self._pages[index]
        self._stack.set_visible_child(widget)
        # Reset scroll position to top
        if isinstance(widget, Gtk.ScrolledWindow):
            adj = widget.get_vadjustment()
            if adj:
                adj.set_value(0)
        # Refresh page size preview when landing on that page
        if pid == "productionPageSize" and hasattr(self, "_pageSizePreviewDa"):
            GLib.idle_add(self._pageSizePreviewDa.queue_draw)
        self._updateNavigation()
        self._da.queue_draw()

    def _nextVisibleIndex(self, fromIndex):
        effective = self._effectiveAnswers()
        for i in range(fromIndex + 1, len(self._pages)):
            pid, _ = self._pages[i]
            if pid in ("welcome", "summary"):
                return i
            page = self._findPage(pid)
            if page and wizardValidation.evaluateShowIf(page.get("showIf"), effective):
                return i
        return None

    def _prevVisibleIndex(self, fromIndex):
        effective = self._effectiveAnswers()
        for i in range(fromIndex - 1, -1, -1):
            pid, _ = self._pages[i]
            if pid in ("welcome", "summary"):
                return i
            page = self._findPage(pid)
            if page and wizardValidation.evaluateShowIf(page.get("showIf"), effective):
                return i
        return None

    def _updateNavigation(self):
        if not self._pages or self._pageIndex >= len(self._pages):
            return
        idx = self._pageIndex
        pid = self._pages[idx][0]
        onWelcome = (pid == "welcome")
        onSummary = (pid == "summary")

        visible    = self._visiblePageList()
        visibleIdx = next((vi + 1 for vi, (pi, _) in enumerate(visible) if pi == idx), 1)
        self._lblStep.set_text(_("Step {} of {}").format(visibleIdx, len(visible)))

        prevIdx = self._prevVisibleIndex(idx)
        self._btnBack.set_sensitive(prevIdx is not None)

        self._btnNext.set_sensitive(not onSummary)

        self._btnReset.set_sensitive(True)
        self._btnCancel.set_sensitive(True)

        self._btnApplyFt.set_sensitive(onSummary)
        self._btnCreateNew.set_sensitive(onSummary)

        self._da.queue_draw()

    # ------------------------------------------------------------------
    # Progress dots
    # ------------------------------------------------------------------

    _DOT_R   = 5
    _DOT_GAP = 10

    def _visiblePageList(self):
        """Return [(page_index, pid)] for every visible page (uses effective answers with defaults)."""
        effective = self._effectiveAnswers()
        out = []
        for i, (pid, _) in enumerate(self._pages):
            if pid in ("welcome", "summary"):
                out.append((i, pid))
                continue
            page = self._findPage(pid)
            if page and wizardValidation.evaluateShowIf(page.get("showIf"), effective):
                out.append((i, pid))
        return out

    def _dotCentres(self, da_width, da_height):
        r, gap  = self._DOT_R, self._DOT_GAP
        visible = self._visiblePageList()
        total   = len(visible)
        if total == 0:
            return []
        totalW = total * (2 * r) + (total - 1) * gap
        x0 = (da_width - totalW) / 2.0
        cy = da_height / 2.0
        return [(x0 + vi * (2 * r + gap) + r, cy, pi, pid)
                for vi, (pi, pid) in enumerate(visible)]

    def _pageTooltip(self, pid):
        """1-2 word tooltip for the progress dot (uses tooltipString from page)."""
        if pid == "welcome":
            return _("Welcome")
        if pid == "summary":
            return _("Review")
        page = self._findPage(pid)
        if page:
            tt = page.get("tooltipString", "")
            if tt:
                return _(tt)
            return _(page.get("titleString", pid))[:20]
        return pid

    def _drawProgressDots(self, da, cr):
        w = da.get_allocated_width()
        h = da.get_allocated_height()
        centres = self._dotCentres(w, h)
        if not centres:
            return
        style  = da.get_style_context()
        sc     = style.get_color(Gtk.StateFlags.NORMAL)
        accent = style.get_color(Gtk.StateFlags.SELECTED)
        r      = self._DOT_R
        for cx, cy, pi, _pid in centres:
            if pi == self._pageIndex:
                cr.set_source_rgba(accent.red, accent.green, accent.blue, 1.0)
                draw_r = r + 1
            elif pi < self._pageIndex:
                cr.set_source_rgba(sc.red, sc.green, sc.blue, 0.7)
                draw_r = r
            else:
                cr.set_source_rgba(sc.red, sc.green, sc.blue, 0.2)
                draw_r = r
            cr.arc(cx, cy, draw_r, 0, 2 * math.pi)
            cr.fill()

    def _onDotClicked(self, da, event):
        w = da.get_allocated_width()
        h = da.get_allocated_height()
        centres = self._dotCentres(w, h)
        hit_r = self._DOT_R + 4
        for cx, cy, pi, pid in centres:
            if abs(event.x - cx) <= hit_r and abs(event.y - cy) <= hit_r:
                if pi <= self._pageIndex or pid == "summary":
                    if pid == "summary":
                        self._refreshSummary()
                    self._goTo(pi)
                return True
        return False

    def _onDotTooltip(self, da, x, y, keyboard_mode, tooltip):
        w = da.get_allocated_width()
        h = da.get_allocated_height()
        centres = self._dotCentres(w, h)
        hit_r = self._DOT_R + 6
        for cx, cy, pi, pid in centres:
            if abs(x - cx) <= hit_r and abs(y - cy) <= hit_r:
                tooltip.set_text(self._pageTooltip(pid))
                return True
        return False

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def _refreshSummary(self):
        effective = self._effectiveAnswers()
        warnings = wizardValidation.validate(effective)
        if warnings:
            msgs = "\n".join(w.message for w in warnings)
            self._warningLabel.set_text(msgs)
            self._warningBanner.show()
        else:
            self._warningBanner.hide()

        for child in self._summaryGrid.get_children():
            child.destroy()

        row = 0
        for page in self.pages:
            if not wizardValidation.evaluateShowIf(page.get("showIf"), effective):
                continue
            for q in page.get("questions", []):
                if not wizardValidation.evaluateShowIf(q.get("showIf"), effective):
                    continue
                val = self.answers.get(q["id"])
                if val is None:
                    val = wizardValidation.resolveDefault(q, effective)

                label_k = Gtk.Label(label=_(q["label"] or page["titleString"]))
                label_k.set_xalign(0)
                label_k.get_style_context().add_class("dim-label")

                label_v = Gtk.Label(label=self._formatAnswer(q, val))
                label_v.set_xalign(0)
                label_v.set_line_wrap(True)

                edit_lnk = Gtk.LinkButton.new_with_label("", _("Edit"))
                edit_lnk._targetPageId = page["id"]
                edit_lnk.connect("activate-link", self._onSummaryEdit)

                self._summaryGrid.attach(label_k, 0, row, 1, 1)
                self._summaryGrid.attach(label_v, 1, row, 1, 1)
                self._summaryGrid.attach(edit_lnk, 2, row, 1, 1)
                row += 1

        self._summaryGrid.show_all()

    def _onSummaryEdit(self, lnk):
        targetPageId = lnk._targetPageId
        for i, (pid, _) in enumerate(self._pages):
            if pid == targetPageId:
                self._goTo(i)
                return True
        return True

    def _formatAnswer(self, q, val):
        if val is None:
            return _("(not set)")
        qtype = q["type"]
        if qtype == "singleSelect":
            for opt in q.get("options", []):
                if opt["id"] == val:
                    lbl = _(opt["label"])
                    return lbl.split("  ·  ")[0] if "  ·  " in lbl else lbl
            return str(val)
        if qtype == "multiSelect":
            if not val:
                return _("(none)")
            labels = [_(opt["label"]) for opt in q.get("options", []) if opt["id"] in val]
            return ", ".join(labels) if labels else str(val)
        if qtype == "notchedSlider":
            notches = q.get("notches", [])
            labels  = q.get("notchLabels", [str(n) for n in notches])
            if val in notches:
                return labels[notches.index(val)]
            return str(val)
        if qtype == "centredSlider":
            if val <= 0.2:
                return _(q.get("leftLabel", str(val)))
            if val >= 0.8:
                return _(q.get("rightLabel", str(val)))
            return _(q.get("centreLabel", str(val)))
        return str(val)

    # ------------------------------------------------------------------
    # Page / question refresh
    # ------------------------------------------------------------------

    def _refreshQuestionInPage(self, questionId):
        """Rebuild question block(s) in their page after an answer change."""
        page = self._findPageForQuestion(questionId)
        if page is None:
            return
        pageId = page["id"]
        for i, (pid, widget) in enumerate(self._pages):
            if pid != pageId:
                continue
            main_box = getattr(widget, "_mainBox", None)
            if main_box is None:
                continue
            # Remove only qblock_ and qhidden_ children (leaves heading/help labels intact)
            for child in list(main_box.get_children()):
                name = child.get_name() if hasattr(child, "get_name") else ""
                if name.startswith("qblock_") or name.startswith("qhidden_"):
                    main_box.remove(child)
            side_lbl = getattr(widget, "_sideLabel", None)
            questions = page.get("questions", [])
            for q in questions:
                if not wizardValidation.evaluateShowIf(q.get("showIf"), self.answers):
                    placeholder = Gtk.Box()
                    placeholder.set_name("qhidden_" + q["id"])
                    placeholder.show()
                    main_box.pack_start(placeholder, False, False, 0)
                    continue
                self._appendQuestionWidget(main_box, q, len(questions) > 1, side_lbl)
            main_box.show_all()
            break

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _findPage(self, pageId):
        return next((p for p in self.pages if p["id"] == pageId), None)

    def _findQuestion(self, questionId):
        for page in self.pages:
            for q in page.get("questions", []):
                if q["id"] == questionId:
                    return q
        return None

    def _findPageForQuestion(self, questionId):
        for page in self.pages:
            for q in page.get("questions", []):
                if q["id"] == questionId:
                    return page
        return None

    def _getMultiSelectValue(self, questionId):
        target = "inputArea_" + questionId
        for _pid, widget in self._pages:
            main_box = getattr(widget, "_mainBox", None)
            if main_box is None:
                continue
            box = self._findWidgetByName(main_box, target)
            if box is not None:
                return [cb._optId for cb in box.get_children()
                        if isinstance(cb, Gtk.CheckButton) and cb.get_active()]
        return []

    def _findWidgetByName(self, parent, name):
        """Recursively find first child widget with the given name."""
        for child in parent.get_children():
            if child.get_name() == name:
                return child
            if hasattr(child, "get_children"):
                found = self._findWidgetByName(child, name)
                if found is not None:
                    return found
        return None

    def _effectiveAnswers(self):
        """Return answers dict with defaults applied for unanswered questions."""
        result = dict(self.answers)
        for page in self.pages:
            for q in page.get("questions", []):
                qid = q["id"]
                if qid not in result:
                    default = wizardValidation.resolveDefault(q, result)
                    if default is not None:
                        result[qid] = default
        return result

    def _showToast(self, message):
        pass  # PTXprint wires its own notification; standalone mode skips this

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self):
        """Show the dialog and block until closed. Returns Gtk.ResponseType."""
        self._dialog.show_all()
        resp = self._dialog.run()
        self._dialog.destroy()
        return resp
