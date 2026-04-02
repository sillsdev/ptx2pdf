#!/usr/bin/env python3
"""
coverwizard.py — PTXprint Cover Wizard
PTXprint integration note: see inline [PTXprint integration] comments.
"""

import os
import sys
import json
import math
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf


# ─────────────────────────────────────────────────────────────────────────────
# State model
# ─────────────────────────────────────────────────────────────────────────────

class WorkingCoverState:
    """
    Temporary in-memory cover state.  All fields are updated on every
    user interaction.  Finish() serialises to JSON.

    [PTXprint integration] Field → PTXprint config key mapping should be
    established in ptxprint/coverwizard.py when porting this module.
    """

    def __init__(self):
        # Step 1 — spine & binding
        self.spine_enabled: bool = False
        self.pagecount: int = 0
        self.binding_type: str = "paperback"     # paperback | hardcover
        self.rtl_binding: bool = False            # [PTXprint integration] → project/RTLbookBinding

        # Step 2 — artwork coverage + images     [PTXprint integration] → cover/image*
        self.coverage_pattern: str = "wrap_all"
        self.img_primary_path: str = ""
        self.img_primary_fit: str = "stretch"    # stretch | crop | none
        self.img_primary_opacity: int = 100
        self.img_secondary_path: str = ""
        self.img_secondary_fit: str = "stretch"
        self.img_secondary_opacity: int = 100

        # Step 3 — background                   [PTXprint integration] → cover/bgMode, bgColor
        self.bg_mode: str = "white"              # white | solid | gradient
        self.bg_color: str = "#4a90d9"
        self.bg_opacity: int = 100

        # Step 4 — front elements               [PTXprint integration] → project/Title, etc.
        self.title: str = ""
        self.title_position: str = "center"      # top | center | bottom
        self.title_in_box: bool = False

        self.subtitle_enabled: bool = False
        self.subtitle: str = ""
        self.subtitle_position: str = "center"

        self.langname_enabled: bool = False
        self.langname: str = ""                  # [PTXprint integration] → Language name
        self.langname_position: str = "bottom"

        self.fgimage_enabled: bool = False
        self.fgimage_path: str = ""
        self.fgimage_position: str = "center"

        # Step 5 — spine text                   [PTXprint integration] → cover/spineText*
        self.spine_title: bool = True
        self.spine_subtitle: bool = False
        self.spine_langname: bool = False
        self.spine_orientation: str = "v_ttb"    # v_ttb | v_btt | horizontal

        # Step 6 — back content                 [PTXprint integration] → cover/backText, isbn, logo
        self.backtext_enabled: bool = False
        self.backtext: str = ""
        self.isbn_enabled: bool = False
        self.isbn: str = ""
        self.logo_enabled: bool = False
        self.logo_path: str = ""
        self.logo_scale: int = 100               # percentage

    def toDict(self):
        return {k: v for k, v in self.__dict__.items()}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def hexToRgb(hexColor: str):
    """Convert '#rrggbb' to (r, g, b) floats 0..1."""
    h = hexColor.lstrip("#")
    if len(h) != 6:
        return (0.3, 0.6, 0.9)
    return (int(h[0:2], 16) / 255.0,
            int(h[2:4], 16) / 255.0,
            int(h[4:6], 16) / 255.0)


def gdkColorToHex(rgba: Gdk.RGBA) -> str:
    return "#{:02x}{:02x}{:02x}".format(
        int(rgba.red * 255), int(rgba.green * 255), int(rgba.blue * 255))


def openImageChooser(parent, title="Choose image file") -> str:
    """Open a GTK file chooser for image files; return chosen path or ''."""
    dlg = Gtk.FileChooserDialog(title=title, parent=parent,
                                action=Gtk.FileChooserAction.OPEN)
    dlg.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OPEN,   Gtk.ResponseType.OK)
    filt = Gtk.FileFilter()
    filt.set_name("Image files")
    for pat in ("*.png", "*.jpg", "*.jpeg", "*.svg", "*.tif", "*.tiff", "*.bmp"):
        filt.add_pattern(pat)
    dlg.add_filter(filt)
    path = ""
    if dlg.run() == Gtk.ResponseType.OK:
        path = dlg.get_filename() or ""
    dlg.destroy()
    return path


def wrapTextLines(text: str, maxChars: int) -> list:
    """
    Simple word-wrap: split text into lines of at most maxChars characters,
    breaking on word boundaries.  Returns a list of strings.
    """
    words  = text.split()
    lines  = []
    current = ""
    for word in words:
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= maxChars:
            current += " " + word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines if lines else [""]


# ─────────────────────────────────────────────────────────────────────────────
# Main application controller
# ─────────────────────────────────────────────────────────────────────────────

class CoverWizardApp:
    """
    Controller for the PTXprint Cover Wizard.
    All GTK signals are event-driven; no polling loops.
    """

    STEPS_NO_SPINE = [
        "pg_step1_spine",
        "pg_step2_coverage",
        "pg_step3_background",
        "pg_step4_front",
        "pg_step6_back",
        "pg_step7_review",
    ]
    STEPS_WITH_SPINE = [
        "pg_step1_spine",
        "pg_step2_coverage",
        "pg_step3_background",
        "pg_step4_front",
        "pg_step5_spine_content",
        "pg_step6_back",
        "pg_step7_review",
    ]

    def __init__(self):
        self.state = WorkingCoverState()

        # Pre-initialise everything used by _refreshUi
        self._steps = list(self.STEPS_NO_SPINE)
        self._stepIndex = 0

        # Cache for loaded pixbufs to avoid reloading on every redraw
        self._pixbufCache: dict = {}

        gladePath = os.path.join(os.path.dirname(__file__), "coverwizard.glade")
        builder = Gtk.Builder()
        try:
            builder.add_from_file(gladePath)
        except Exception as exc:
            dlg = Gtk.MessageDialog(
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CLOSE,
                text=f"Could not load UI file:\n{gladePath}\n\n{exc}",
            )
            dlg.run(); dlg.destroy(); sys.exit(1)

        builder.connect_signals(self)

        def w(name):
            return builder.get_object(name)

        # Core
        self.window     = w("w_coverwizard")
        self.st_steps   = w("st_steps")
        self.da_preview = w("da_preview")
        self.l_progress = w("l_progress")
        self.l_summary  = w("l_summary")
        self.btn_back   = w("btn_back")
        self.btn_next   = w("btn_next")
        self.btn_finish = w("btn_finish")

        # Step 1
        self.t_pagecount         = w("t_pagecount")
        self.r_spine_no          = w("r_spine_no")
        self.r_spine_yes         = w("r_spine_yes")
        self.rv_binding_type     = w("rv_binding_type")
        self.r_binding_paperback = w("r_binding_paperback")
        self.r_binding_hardcover = w("r_binding_hardcover")
        self.c_RTLbookBinding    = w("c_RTLbookBinding")

        # Step 2
        self.r_cov_wrap_all            = w("r_cov_wrap_all")
        self.r_cov_front_only          = w("r_cov_front_only")
        self.r_cov_front_spine         = w("r_cov_front_spine")
        self.r_cov_back_only           = w("r_cov_back_only")
        self.r_cov_back_spine          = w("r_cov_back_spine")
        self.r_cov_front_back_separate = w("r_cov_front_back_separate")
        self.r_cov_none                = w("r_cov_none")
        self.rv_img_primary            = w("rv_img_primary")
        self.l_img_primary_status      = w("l_img_primary_status")
        self.cb_img_primary_fit        = w("cb_img_primary_fit")
        self.sl_img_primary_opacity    = w("sl_img_primary_opacity")
        self.rv_img_secondary          = w("rv_img_secondary")
        self.l_img_secondary_status    = w("l_img_secondary_status")
        self.cb_img_secondary_fit      = w("cb_img_secondary_fit")
        self.sl_img_secondary_opacity  = w("sl_img_secondary_opacity")

        # Step 3
        self.r_bg_white    = w("r_bg_white")
        self.r_bg_solid    = w("r_bg_solid")
        self.r_bg_gradient = w("r_bg_gradient")
        self.rv_bgcolor    = w("rv_bgcolor")
        self.cb_bgcolor    = w("cb_bgcolor")
        self.sl_bg_opacity = w("sl_bg_opacity")

        # Step 4
        self.t_title            = w("t_title")
        self.cb_title_position  = w("cb_title_position")
        self.c_title_box        = w("c_title_box")
        self.c_subtitle_enable  = w("c_subtitle_enable")
        self.rv_subtitle        = w("rv_subtitle")
        self.t_subtitle         = w("t_subtitle")
        self.cb_subtitle_position = w("cb_subtitle_position")
        self.c_langname_enable  = w("c_langname_enable")
        self.rv_langname        = w("rv_langname")
        self.t_langname         = w("t_langname")
        self.cb_langname_position = w("cb_langname_position")
        self.c_fgimage_enable   = w("c_fgimage_enable")
        self.rv_fgimage         = w("rv_fgimage")
        self.l_fgimage_status   = w("l_fgimage_status")
        self.cb_fgimage_position = w("cb_fgimage_position")

        # Step 5
        self.c_spine_title            = w("c_spine_title")
        self.c_spine_subtitle         = w("c_spine_subtitle")
        self.c_spine_langname         = w("c_spine_langname")
        self.r_spine_text_v_ttb       = w("r_spine_text_v_ttb")
        self.r_spine_text_v_btt       = w("r_spine_text_v_btt")
        self.r_spine_text_horizontal  = w("r_spine_text_horizontal")

        # Step 6
        self.c_backtext_enable = w("c_backtext_enable")
        self.rv_backtext       = w("rv_backtext")
        self.t_backtext        = w("t_backtext")
        self.c_isbn_enable     = w("c_isbn_enable")
        self.rv_isbn           = w("rv_isbn")
        self.t_isbn            = w("t_isbn")
        self.c_logo_enable     = w("c_logo_enable")
        self.rv_logo           = w("rv_logo")
        self.l_logo_status     = w("l_logo_status")
        self.sl_logo_scale     = w("sl_logo_scale")

        # Connect GtkTextBuffer signal in Python (cannot be done in Glade)
        self.t_backtext.get_buffer().connect("changed", self.onBacktextBufferChanged)

        # Initialise combo defaults (active index 1 = "center")
        self.cb_title_position.set_active(1)
        self.cb_subtitle_position.set_active(1)
        self.cb_langname_position.set_active(2)   # default bottom
        self.cb_fgimage_position.set_active(1)
        self.cb_img_primary_fit.set_active(0)
        self.cb_img_secondary_fit.set_active(0)

        # Set initial background colour
        initialRgba = Gdk.RGBA()
        initialRgba.parse(self.state.bg_color)
        self.cb_bgcolor.set_rgba(initialRgba)

        self._stepIndex = 0
        self._updateStepList()
        self._goToStep(0)
        self.window.show_all()

    # ── Step management ───────────────────────────────────────────────

    def _updateStepList(self):
        self._steps = list(
            self.STEPS_WITH_SPINE if self.state.spine_enabled
            else self.STEPS_NO_SPINE
        )

    def _goToStep(self, index: int):
        self._stepIndex = max(0, min(index, len(self._steps) - 1))
        self.st_steps.set_visible_child_name(self._steps[self._stepIndex])
        self._refreshUi()

    def _refreshUi(self):
        if not hasattr(self, "_steps") or not hasattr(self, "_stepIndex"):
            return
        total   = len(self._steps)
        current = self._stepIndex + 1
        self.l_progress.set_text(f"Step {current} of {total}")

        self.btn_back.set_sensitive(self._stepIndex > 0)
        self.btn_next.set_sensitive(self._stepIndex < total - 1)

        onLast  = (self._stepIndex == total - 1)
        titleOk = bool(self.state.title.strip())
        self.btn_finish.set_sensitive(onLast and titleOk)

        # Block Next on Step 4 until title entered
        if self._steps[self._stepIndex] == "pg_step4_front" and not titleOk:
            self.btn_next.set_sensitive(False)

        self._updateCoverageOptions()
        self._updateSpineHorizontalVisibility()
        self.c_spine_subtitle.set_sensitive(self.state.subtitle_enabled)
        self._updateSummary()
        self.da_preview.queue_draw()

    def _updateCoverageOptions(self):
        spine = self.state.spine_enabled
        self.r_cov_wrap_all.set_label(
            "Wrap all (one image across front + spine + back)" if spine
            else "Wrap all (one image across front + back)"
        )
        for radio in (self.r_cov_front_spine, self.r_cov_back_spine):
            radio.set_visible(spine)
            radio.set_sensitive(spine)
        if not spine and self.state.coverage_pattern in ("front_spine", "back_spine"):
            self.state.coverage_pattern = "wrap_all"
            self.r_cov_wrap_all.set_active(True)

        # Image pickers visibility
        noImage = (self.state.coverage_pattern == "none")
        self.rv_img_primary.set_reveal_child(not noImage)
        isSeparate = (self.state.coverage_pattern == "front_back_separate")
        self.rv_img_secondary.set_reveal_child(isSeparate)

    def _updateSpineHorizontalVisibility(self):
        """Show 'Horizontal' spine option only when pagecount >= 500."""
        showHoriz = (self.state.pagecount >= 500)
        self.r_spine_text_horizontal.set_visible(showHoriz)
        self.r_spine_text_horizontal.set_sensitive(showHoriz)
        # If horizontal was selected but now hidden, revert to v_ttb
        if not showHoriz and self.state.spine_orientation == "horizontal":
            self.state.spine_orientation = "v_ttb"
            self.r_spine_text_v_ttb.set_active(True)

    def _newupdateSummary(self):
        s = self.state
        parts = []

        # Pages + spine
        if s.pagecount:
            parts.append(f"{s.pagecount} pages")

        if s.spine_enabled:
            parts.append(f"{s.binding_type} with spine")
        else:
            parts.append("no spine")

        # Coverage
        coverageMap = {
            "wrap_all": "wrap image",
            "front_only": "front image",
            "front_spine": "front + spine image",
            "back_only": "back image",
            "back_spine": "back + spine image",
            "front_back_separate": "separate front/back images",
            "none": "no image"
        }
        parts.append(coverageMap.get(s.coverage_pattern, s.coverage_pattern))

        # Background
        if s.bg_mode == "solid":
            parts.append(f"{s.bg_color} background")
        elif s.bg_mode == "white":
            parts.append("white background")
        else:
            parts.append("gradient background")

        # Back content
        if s.backtext_enabled:
            parts.append("back text")
        if s.isbn_enabled:
            parts.append("ISBN")
        if s.logo_enabled:
            parts.append("logo")

        summary = ", ".join(parts)
        self.l_summary.set_text(summary)

    def _updateSummary(self):
        s = self.state
        lines = [f"Spine:        {'Yes' if s.spine_enabled else 'No'} (pages: {s.pagecount})"]
        if s.spine_enabled:
            lines.append(f"Binding type: {s.binding_type}")
        lines.append(f"Binding dir:  {'RTL' if s.rtl_binding else 'LTR'}")
        lines.append(f"Coverage:     {s.coverage_pattern}")
        if s.img_primary_path:
            lines.append(f"Image 1:      {os.path.basename(s.img_primary_path)} "
                         f"fit={s.img_primary_fit} op={s.img_primary_opacity}%")
        if s.img_secondary_path:
            lines.append(f"Image 2:      {os.path.basename(s.img_secondary_path)} "
                         f"fit={s.img_secondary_fit} op={s.img_secondary_opacity}%")
        lines.append(f"Background:   {s.bg_mode}"
                     + (f" {s.bg_color} op={s.bg_opacity}%" if s.bg_mode == "solid" else ""))
        lines.append(f"Title:        {s.title or '(empty)'} [{s.title_position}]"
                     + (" [boxed]" if s.title_in_box else ""))
        if s.subtitle_enabled:
            lines.append(f"Subtitle:     {s.subtitle or '(empty)'} [{s.subtitle_position}]")
        if s.langname_enabled:
            lines.append(f"Language:     {s.langname or '(empty)'} [{s.langname_position}]")
        if s.fgimage_enabled:
            lines.append(f"Fg image:     {os.path.basename(s.fgimage_path) or '(none)'} [{s.fgimage_position}]")
        if s.spine_enabled:
            parts = [x for x, b in [("title", s.spine_title),
                                     ("subtitle", s.spine_subtitle),
                                     ("language", s.spine_langname)] if b]
            lines.append(f"Spine text:   {', '.join(parts) or '(none)'} [{s.spine_orientation}]")
        if s.backtext_enabled:
            snippet = s.backtext.strip()[:48] + ("…" if len(s.backtext.strip()) > 48 else "")
            lines.append(f"Back text:    {snippet or '(empty)'}")
        if s.isbn_enabled:
            lines.append(f"ISBN:         {s.isbn or '(empty)'}")
        if s.logo_enabled:
            lines.append(f"Logo:         {os.path.basename(s.logo_path) or '(none)'} scale={s.logo_scale}%")
        self.l_summary.set_text("\n".join(lines))

    # ── Pixbuf helper ─────────────────────────────────────────────────

    def _loadPixbuf(self, path: str) -> GdkPixbuf.Pixbuf | None:
        """Load an image file into a GdkPixbuf, caching by path."""
        if not path or not os.path.isfile(path):
            return None
        if path in self._pixbufCache:
            return self._pixbufCache[path]
        try:
            pb = GdkPixbuf.Pixbuf.new_from_file(path)
            self._pixbufCache[path] = pb
            return pb
        except Exception:
            return None

    # ── Signal handlers — Step 1 ──────────────────────────────────────

    def onPagecountChanged(self, widget):
        try:
            self.state.pagecount = int(widget.get_text().strip())
        except ValueError:
            self.state.pagecount = 0
        # Auto-suggest spine
        if self.state.pagecount >= 80:
            self.r_spine_yes.set_active(True)
        else:
            self.r_spine_no.set_active(True)
        self._refreshUi()

    def onSpineToggled(self, widget):
        if not widget.get_active():
            return
        self.state.spine_enabled = self.r_spine_yes.get_active()
        self.rv_binding_type.set_reveal_child(self.state.spine_enabled)
        currentPage = self._steps[self._stepIndex]
        self._updateStepList()
        self._stepIndex = self._steps.index(currentPage) if currentPage in self._steps else 0
        self._refreshUi()

    def onBindingTypeToggled(self, widget):
        if not widget.get_active():
            return
        self.state.binding_type = "paperback" if self.r_binding_paperback.get_active() else "hardcover"
        self._refreshUi()

    def onRTLBindingToggled(self, widget):
        """RTL binding is a single checkbox — no sub-radios."""
        self.state.rtl_binding = widget.get_active()
        self._refreshUi()

    # ── Signal handlers — Step 2 ──────────────────────────────────────

    def onCoverageToggled(self, widget):
        if not widget.get_active():
            return
        mapping = {
            "r_cov_wrap_all":            "wrap_all",
            "r_cov_front_only":          "front_only",
            "r_cov_front_spine":         "front_spine",
            "r_cov_back_only":           "back_only",
            "r_cov_back_spine":          "back_spine",
            "r_cov_front_back_separate": "front_back_separate",
            "r_cov_none":                "none",
        }
        self.state.coverage_pattern = mapping.get(Gtk.Buildable.get_name(widget), "wrap_all")
        self._refreshUi()

    def onImgPrimaryChooseClicked(self, widget):
        path = openImageChooser(self.window, "Choose primary cover image")
        if path:
            self.state.img_primary_path = path
            self._pixbufCache.pop(path, None)   # invalidate cache
            self.l_img_primary_status.set_text(os.path.basename(path))
            self.l_img_primary_status.set_tooltip_text(path)
        self._refreshUi()

    def onImgPrimaryFitChanged(self, widget):
        fits = ["stretch", "crop", "none"]
        idx = widget.get_active()
        self.state.img_primary_fit = fits[idx] if 0 <= idx < len(fits) else "stretch"
        self._refreshUi()

    def onImgPrimaryOpacityChanged(self, widget):
        self.state.img_primary_opacity = int(widget.get_value())
        self._refreshUi()

    def onImgSecondaryChooseClicked(self, widget):
        path = openImageChooser(self.window, "Choose back cover image")
        if path:
            self.state.img_secondary_path = path
            self._pixbufCache.pop(path, None)
            self.l_img_secondary_status.set_text(os.path.basename(path))
            self.l_img_secondary_status.set_tooltip_text(path)
        self._refreshUi()

    def onImgSecondaryFitChanged(self, widget):
        fits = ["stretch", "crop", "none"]
        idx = widget.get_active()
        self.state.img_secondary_fit = fits[idx] if 0 <= idx < len(fits) else "stretch"
        self._refreshUi()

    def onImgSecondaryOpacityChanged(self, widget):
        self.state.img_secondary_opacity = int(widget.get_value())
        self._refreshUi()

    # ── Signal handlers — Step 3 ──────────────────────────────────────

    def onBgToggled(self, widget):
        if not widget.get_active():
            return
        if self.r_bg_white.get_active():
            self.state.bg_mode = "white"
        elif self.r_bg_solid.get_active():
            self.state.bg_mode = "solid"
        else:
            self.state.bg_mode = "gradient"
        self.rv_bgcolor.set_reveal_child(self.state.bg_mode == "solid")
        self._refreshUi()

    def onBgcolorSet(self, widget):
        self.state.bg_color = gdkColorToHex(widget.get_rgba())
        self._refreshUi()

    def onBgOpacityChanged(self, widget):
        self.state.bg_opacity = int(widget.get_value())
        self._refreshUi()

    # ── Signal handlers — Step 4 ──────────────────────────────────────

    def onTitleChanged(self, widget):
        self.state.title = widget.get_text()
        self._refreshUi()

    def onTitlePositionChanged(self, widget):
        positions = ["top", "center", "bottom"]
        idx = widget.get_active()
        self.state.title_position = positions[idx] if 0 <= idx < 3 else "center"
        self._refreshUi()

    def onTitleBoxToggled(self, widget):
        self.state.title_in_box = widget.get_active()
        self._refreshUi()

    def onSubtitleEnableToggled(self, widget):
        self.state.subtitle_enabled = widget.get_active()
        self.rv_subtitle.set_reveal_child(self.state.subtitle_enabled)
        if not self.state.subtitle_enabled:
            self.state.spine_subtitle = False
            self.c_spine_subtitle.set_active(False)
        self._refreshUi()

    def onSubtitleChanged(self, widget):
        self.state.subtitle = widget.get_text()
        self._refreshUi()

    def onSubtitlePositionChanged(self, widget):
        positions = ["top", "center", "bottom"]
        idx = widget.get_active()
        self.state.subtitle_position = positions[idx] if 0 <= idx < 3 else "center"
        self._refreshUi()

    def onLangnameEnableToggled(self, widget):
        self.state.langname_enabled = widget.get_active()
        self.rv_langname.set_reveal_child(self.state.langname_enabled)
        self._refreshUi()

    def onLangnameChanged(self, widget):
        self.state.langname = widget.get_text()
        self._refreshUi()

    def onLangnamePositionChanged(self, widget):
        positions = ["top", "center", "bottom"]
        idx = widget.get_active()
        self.state.langname_position = positions[idx] if 0 <= idx < 3 else "bottom"
        self._refreshUi()

    def onFgimageEnableToggled(self, widget):
        self.state.fgimage_enabled = widget.get_active()
        self.rv_fgimage.set_reveal_child(self.state.fgimage_enabled)
        self._refreshUi()

    def onFgimageChooseClicked(self, widget):
        path = openImageChooser(self.window, "Choose foreground illustration")
        if path:
            self.state.fgimage_path = path
            self._pixbufCache.pop(path, None)
            self.l_fgimage_status.set_text(os.path.basename(path))
            self.l_fgimage_status.set_tooltip_text(path)
        self._refreshUi()

    def onFgimagePositionChanged(self, widget):
        positions = ["top", "center", "bottom"]
        idx = widget.get_active()
        self.state.fgimage_position = positions[idx] if 0 <= idx < 3 else "center"
        self._refreshUi()

    # ── Signal handlers — Step 5 ──────────────────────────────────────

    def onSpineContentToggled(self, widget):
        self.state.spine_title    = self.c_spine_title.get_active()
        self.state.spine_subtitle = self.c_spine_subtitle.get_active()
        self.state.spine_langname = self.c_spine_langname.get_active()
        self._refreshUi()

    def onSpineOrientationToggled(self, widget):
        if not widget.get_active():
            return
        if self.r_spine_text_v_ttb.get_active():
            self.state.spine_orientation = "v_ttb"
        elif self.r_spine_text_v_btt.get_active():
            self.state.spine_orientation = "v_btt"
        else:
            self.state.spine_orientation = "horizontal"
        self._refreshUi()

    # ── Signal handlers — Step 6 ──────────────────────────────────────

    def onBacktextEnableToggled(self, widget):
        self.state.backtext_enabled = widget.get_active()
        self.rv_backtext.set_reveal_child(self.state.backtext_enabled)
        self._refreshUi()

    def onBacktextBufferChanged(self, buffer):
        """Connected in Python to GtkTextBuffer — not expressible in Glade."""
        start = buffer.get_start_iter()
        end   = buffer.get_end_iter()
        self.state.backtext = buffer.get_text(start, end, False)
        self._refreshUi()

    def onIsbnEnableToggled(self, widget):
        self.state.isbn_enabled = widget.get_active()
        self.rv_isbn.set_reveal_child(self.state.isbn_enabled)
        self._refreshUi()

    def onIsbnChanged(self, widget):
        self.state.isbn = widget.get_text()
        self._refreshUi()

    def onLogoEnableToggled(self, widget):
        self.state.logo_enabled = widget.get_active()
        self.rv_logo.set_reveal_child(self.state.logo_enabled)
        self._refreshUi()

    def onLogoChooseClicked(self, widget):
        path = openImageChooser(self.window, "Choose logo file")
        if path:
            self.state.logo_path = path
            self._pixbufCache.pop(path, None)
            self.l_logo_status.set_text(os.path.basename(path))
            self.l_logo_status.set_tooltip_text(path)
        self._refreshUi()

    def onLogoScaleChanged(self, widget):
        self.state.logo_scale = int(widget.get_value())
        self._refreshUi()

    # ── Navigation ────────────────────────────────────────────────────

    def onBackClicked(self, widget):
        self._goToStep(self._stepIndex - 1)

    def onNextClicked(self, widget):
        self._goToStep(self._stepIndex + 1)

    def onCancelClicked(self, widget):
        self.window.destroy()

    def onAdvancedClicked(self, widget):
        dlg = Gtk.MessageDialog(
            transient_for=self.window, message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Advanced options are not available in this prototype.\n\n"
                 "They will be connected to PTXprint's full cover settings when integrated.",
        )
        dlg.run(); dlg.destroy()

    def onFinishClicked(self, widget):
        stateDict = self.state.toDict()
        print("\n── Cover Wizard finished ──")
        print(json.dumps(stateDict, indent=2))
        outputPath = os.path.join(os.getcwd(), "coverwizard_state.json")
        try:
            with open(outputPath, "w", encoding="utf-8") as f:
                json.dump(stateDict, f, indent=2)
            print(f"\nState written to: {outputPath}")
            dlg = Gtk.MessageDialog(
                transient_for=self.window, message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=f"Cover settings saved to:\n{outputPath}",
            )
        except OSError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            dlg = Gtk.MessageDialog(
                transient_for=self.window, message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CLOSE, text=f"Could not write file:\n{exc}",
            )
        dlg.run(); dlg.destroy()
        self.window.destroy()

    def onWindowDestroy(self, widget):
        Gtk.main_quit()

    # ─────────────────────────────────────────────────────────────────
    # Cairo preview renderer
    # ─────────────────────────────────────────────────────────────────

    def onPreviewDraw(self, widget, cr):
        """
        Draw the live cover preview.

        Layout (RTL-aware):
          LTR no spine:  [ BACK | FRONT ]
          LTR spine:     [ BACK | SP | FRONT ]
          RTL no spine:  [ FRONT | BACK ]
          RTL spine:     [ FRONT | SP | BACK ]
        """
        alloc = widget.get_allocation()
        W, H  = alloc.width, alloc.height
        s     = self.state

        MARGIN         = 18
        SPINE_FRACTION = 0.07

        drawW = W - 2 * MARGIN
        drawH = H - 2 * MARGIN
        topY  = MARGIN

        # Panel geometry
        if s.spine_enabled:
            spinePx = max(16, int(drawW * SPINE_FRACTION))
            sideW   = (drawW - spinePx) // 2
            frontW  = drawW - sideW - spinePx
        else:
            spinePx = 0
            sideW   = drawW // 2
            frontW  = drawW - sideW

        rtl = s.rtl_binding
        if not rtl:
            backX  = MARGIN;          backW = sideW
            spineX = MARGIN + sideW
            frontX = spineX + spinePx
        else:
            frontX = MARGIN
            spineX = MARGIN + frontW
            backX  = spineX + spinePx; backW = sideW

        panelH = drawH

        # Active-surface highlight flags
        pageName = self._steps[self._stepIndex]
        hlFront  = pageName == "pg_step4_front"
        hlSpine  = pageName == "pg_step5_spine_content"
        hlBack   = pageName == "pg_step6_back"
        hlAll    = pageName in ("pg_step2_coverage", "pg_step3_background", "pg_step7_review")

        # ── Background ────────────────────────────────────────────────
        self._drawBackground(cr, s, MARGIN, topY, drawW, panelH)

        # ── Coverage images ───────────────────────────────────────────
        self._drawCoverage(cr, s, backX, backW, spineX, spinePx, frontX, frontW, topY, panelH)

        # ── Divider lines ─────────────────────────────────────────────
        cr.set_source_rgb(0.45, 0.45, 0.45)
        cr.set_line_width(1)
        if s.spine_enabled:
            for x in (spineX, spineX + spinePx):
                cr.move_to(x, topY); cr.line_to(x, topY + panelH); cr.stroke()
        else:
            divX = frontX if not rtl else spineX
            cr.move_to(divX, topY); cr.line_to(divX, topY + panelH); cr.stroke()

        # ── Outer border ──────────────────────────────────────────────
        cr.set_source_rgb(0.3, 0.3, 0.3)
        cr.set_line_width(1)
        cr.rectangle(MARGIN, topY, drawW, panelH)
        cr.stroke()

        # ── Active-surface highlight ──────────────────────────────────
        HL = 3
        def highlightRect(x, y, w, h):
            cr.set_source_rgb(0, 0, 0)
            cr.set_line_width(HL)
            cr.rectangle(x + HL/2, y + HL/2, w - HL, h - HL)
            cr.stroke()

        if hlAll:
            highlightRect(MARGIN, topY, drawW, panelH)
        elif hlFront:
            highlightRect(frontX, topY, frontW, panelH)
        elif hlSpine and s.spine_enabled:
            highlightRect(spineX, topY, spinePx, panelH)
        elif hlBack:
            highlightRect(backX, topY, backW, panelH)

        # ── Panel dim labels ──────────────────────────────────────────
        cr.set_source_rgba(0, 0, 0, 0.20)
        cr.select_font_face("Sans", 0, 0)
        cr.set_font_size(10)

        def centredLabel(x, y, w, h, text):
            ext = cr.text_extents(text)
            cr.move_to(x + (w - ext.width)/2, y + h - 8)
            cr.show_text(text)

        centredLabel(backX, topY, backW, panelH, "BACK")
        centredLabel(frontX, topY, frontW, panelH, "FRONT")
        if s.spine_enabled and spinePx > 18:
            cr.set_font_size(8)
            ext = cr.text_extents("SPINE")
            cr.save()
            cr.translate(spineX + spinePx/2, topY + panelH/2)
            cr.rotate(-math.pi/2)
            cr.move_to(-ext.width/2, ext.height/2)
            cr.show_text("SPINE")
            cr.restore()

        # ── Front content ─────────────────────────────────────────────
        self._drawFrontContent(cr, s, frontX, topY, frontW, panelH)

        # ── Spine text ────────────────────────────────────────────────
        if s.spine_enabled:
            self._drawSpineText(cr, s, spineX, topY, spinePx, panelH)

        # ── Back content ──────────────────────────────────────────────
        self._drawBackContent(cr, s, backX, topY, backW, panelH, rtl)

    # ── Sub-renderers ─────────────────────────────────────────────────

    def _drawBackground(self, cr, s, x, y, w, h):
        if s.bg_mode == "white":
            cr.set_source_rgb(1, 1, 1)
            cr.rectangle(x, y, w, h); cr.fill()
        elif s.bg_mode == "solid":
            r, g, b = hexToRgb(s.bg_color)
            alpha   = s.bg_opacity / 100.0
            cr.set_source_rgb(1, 1, 1)
            cr.rectangle(x, y, w, h); cr.fill()
            cr.set_source_rgba(r, g, b, alpha)
            cr.rectangle(x, y, w, h); cr.fill()
        elif s.bg_mode == "gradient":
            import cairo
            pat = cairo.LinearGradient(x, y, x + w, y)
            pat.add_color_stop_rgb(0.0, 0.85, 0.90, 0.98)
            pat.add_color_stop_rgb(0.5, 0.60, 0.72, 0.92)
            pat.add_color_stop_rgb(1.0, 0.40, 0.55, 0.80)
            cr.set_source(pat)
            cr.rectangle(x, y, w, h); cr.fill()

    def _drawCoverage(self, cr, s, backX, backW, spineX, spinePx, frontX, frontW, topY, panelH):
        """Draw coverage regions — real image if available, tinted placeholder otherwise."""

        def paintRegion(x, w, path, opacity, fit):
            """Fill a panel region with image or tinted placeholder."""
            pb = self._loadPixbuf(path) if path else None
            if pb:
                self._paintPixbuf(cr, pb, x, topY, w, panelH, opacity, fit)
            else:
                # Tinted placeholder
                cr.set_source_rgba(0.45, 0.72, 0.52, 0.45)
                cr.rectangle(x, topY, w, panelH); cr.fill()
                cr.set_source_rgba(0.1, 0.38, 0.18, 0.80)
                cr.select_font_face("Sans", 0, 1)
                cr.set_font_size(11)
                ext = cr.text_extents("IMAGE")
                cr.move_to(x + (w - ext.width)/2, topY + panelH/2)
                cr.show_text("IMAGE")

        p    = s.coverage_pattern
        pri  = s.img_primary_path
        priO = s.img_primary_opacity / 100.0
        priF = s.img_primary_fit
        sec  = s.img_secondary_path
        secO = s.img_secondary_opacity / 100.0
        secF = s.img_secondary_fit

        if p == "wrap_all":
            paintRegion(backX, backW + spinePx + frontW, pri, priO, priF)
        elif p == "front_only":
            paintRegion(frontX, frontW, pri, priO, priF)
        elif p == "front_spine" and s.spine_enabled:
            lx = min(spineX, frontX)
            paintRegion(lx, spinePx + frontW, pri, priO, priF)
        elif p == "back_only":
            paintRegion(backX, backW, pri, priO, priF)
        elif p == "back_spine" and s.spine_enabled:
            lx = min(backX, spineX)
            paintRegion(lx, backW + spinePx, pri, priO, priF)
        elif p == "front_back_separate":
            paintRegion(frontX, frontW, pri, priO, priF)
            paintRegion(backX,  backW,  sec, secO, secF)
        # "none" → nothing

    def _paintPixbuf(self, cr, pb, x, y, w, h, opacity, fit):
        """
        Render a GdkPixbuf into the rectangle (x,y,w,h) with the given
        fit mode and opacity.  Cairo clip ensures no bleed outside the panel.
        """
        imgW = pb.get_width()
        imgH = pb.get_height()

        cr.save()
        cr.rectangle(x, y, w, h)
        cr.clip()

        if fit == "stretch":
            scaleX = w / imgW
            scaleY = h / imgH
            cr.translate(x, y)
            cr.scale(scaleX, scaleY)
            drawX, drawY = 0, 0
        elif fit == "crop":
            scale = max(w / imgW, h / imgH)
            scaledW = imgW * scale
            scaledH = imgH * scale
            drawX = x + (w - scaledW) / 2
            drawY = y + (h - scaledH) / 2
            cr.translate(drawX, drawY)
            cr.scale(scale, scale)
            drawX, drawY = 0, 0
        else:   # none: 100% as-is, centred
            drawX = x + (w - imgW) / 2
            drawY = y + (h - imgH) / 2
            cr.translate(drawX, drawY)
            drawX, drawY = 0, 0

        Gdk.cairo_set_source_pixbuf(cr, pb, drawX, drawY)
        cr.paint_with_alpha(opacity)
        cr.restore()

    def _positionY(self, placement: str, panelTop: float, panelH: float,
                   blockH: float, margin: float = 28) -> float:
        """Convert a placement string to a y coordinate for a text/image block."""
        if placement == "top":
            return panelTop + margin
        elif placement == "bottom":
            return panelTop + panelH - blockH - margin
        else:  # center
            return panelTop + (panelH - blockH) / 2

    def _drawFrontContent(self, cr, s, fx, fy, fw, fh):
        """
        Draw all enabled front-cover elements, each at its own vertical position.
        Elements: title, subtitle, langname, foreground illustration.
        """
        LINE_H = 19

        # ── Foreground illustration ───────────────────────────────────
        if s.fgimage_enabled and s.fgimage_path:
            pb = self._loadPixbuf(s.fgimage_path)
            if pb:
                imgMaxH = fh * 0.40
                imgMaxW = fw * 0.80
                scale   = min(imgMaxW / pb.get_width(), imgMaxH / pb.get_height())
                iw = pb.get_width()  * scale
                ih = pb.get_height() * scale
                iy = self._positionY(s.fgimage_position, fy, fh, ih, 20)
                ix = fx + (fw - iw) / 2
                cr.save()
                cr.rectangle(fx, fy, fw, fh); cr.clip()
                cr.translate(ix, iy)
                cr.scale(scale, scale)
                Gdk.cairo_set_source_pixbuf(cr, pb, 0, 0)
                cr.paint()
                cr.restore()

        # ── Title ─────────────────────────────────────────────────────
        titleText = s.title.strip() or "TITLE"
        titleH    = LINE_H + 4

        tyBase = self._positionY(s.title_position, fy, fh, titleH, 20)
        if s.title_in_box:
            pad = 7
            cr.set_source_rgba(1, 1, 1, 0.62)
            cr.rectangle(fx + 8, tyBase - pad, fw - 16, titleH + pad * 2)
            cr.fill()
        cr.select_font_face("Sans", 0, 1)
        cr.set_font_size(15)
        cr.set_source_rgba(0.05, 0.05, 0.15, 0.92)
        ext = cr.text_extents(titleText)
        cr.move_to(fx + (fw - ext.width) / 2, tyBase + LINE_H)
        cr.show_text(titleText)

        # ── Subtitle ──────────────────────────────────────────────────
        if s.subtitle_enabled:
            subText = s.subtitle.strip() or "(subtitle)"
            subH    = LINE_H
            syBase  = self._positionY(s.subtitle_position, fy, fh, subH, 20)
            cr.select_font_face("Sans", 0, 0)
            cr.set_font_size(10)
            cr.set_source_rgba(0.1, 0.1, 0.2, 0.78)
            ext = cr.text_extents(subText)
            cr.move_to(fx + (fw - ext.width) / 2, syBase + LINE_H)
            cr.show_text(subText)

        # ── Language / translation name ───────────────────────────────
        if s.langname_enabled:
            lnText = s.langname.strip() or "(language)"
            lnH    = LINE_H
            lyBase = self._positionY(s.langname_position, fy, fh, lnH, 20)
            cr.select_font_face("Sans", 0, 0)
            cr.set_font_size(10)
            cr.set_source_rgba(0.1, 0.1, 0.2, 0.72)
            ext = cr.text_extents(lnText)
            cr.move_to(fx + (fw - ext.width) / 2, lyBase + LINE_H)
            cr.show_text(lnText)

    def _drawSpineText(self, cr, s, sx, sy, sw, sh):
        parts = []
        if s.spine_title:
            parts.append(s.title.strip() or "Title")
        if s.spine_subtitle and s.subtitle_enabled:
            parts.append(s.subtitle.strip() or "Subtitle")
        if s.spine_langname:
            parts.append(s.langname.strip() or "Language")
        spineText = " • ".join(parts)
        if not spineText:
            return

        cr.set_source_rgba(0.05, 0.05, 0.2, 0.88)
        cr.select_font_face("Sans", 0, 0)
        cr.set_font_size(9)
        orient = s.spine_orientation
        cx = sx + sw / 2
        cy = sy + sh / 2

        cr.save()
        if orient == "v_ttb":
            cr.translate(cx, cy); cr.rotate(math.pi / 2)
        elif orient == "v_btt":
            cr.translate(cx, cy); cr.rotate(-math.pi / 2)
        else:   # horizontal
            cr.translate(cx, cy)
        ext = cr.text_extents(spineText)
        cr.move_to(-ext.width / 2, ext.height / 2)
        cr.show_text(spineText)
        cr.restore()

    def _drawBackContent(self, cr, s, bx, by, bw, bh, rtl):
        """Draw back-panel content with proper text wrapping inside the box."""
        cursorY = by + 14
        PAD     = 10

        # ── Back text with proper word-wrap + clipping ────────────────
        if s.backtext_enabled:
            blockH   = min(70, bh // 3)
            textBoxW = bw - PAD * 2
            cr.set_source_rgba(0.93, 0.93, 0.88, 0.82)
            cr.rectangle(bx + PAD, cursorY, textBoxW, blockH); cr.fill()

            cr.save()
            cr.rectangle(bx + PAD, cursorY, textBoxW, blockH); cr.clip()

            cr.set_source_rgba(0.15, 0.15, 0.15, 0.88)
            cr.select_font_face("Sans", 0, 0)
            FONT_SIZE = 7
            cr.set_font_size(FONT_SIZE)

            rawText   = s.backtext.strip() if s.backtext.strip() else "Back text here"
            # Estimate chars per line from pixel width
            charWidth = FONT_SIZE * 0.55   # rough monospace approximation
            charsPerLine = max(10, int((textBoxW - 8) / charWidth))
            lines     = wrapTextLines(rawText, charsPerLine)
            lineSpacing = FONT_SIZE + 3

            for i, line in enumerate(lines):
                lineY = cursorY + (i + 1) * lineSpacing
                if lineY > cursorY + blockH - 2:
                    break
                cr.move_to(bx + PAD + 4, lineY)
                cr.show_text(line)
            cr.restore()
            cursorY += blockH + 8

        # ── Logo: render actual image if available ────────────────────
        if s.logo_enabled:
            logoAreaH = 50
            logoAreaW = bw - PAD * 2
            pb = self._loadPixbuf(s.logo_path) if s.logo_path else None
            if pb:
                scale    = (s.logo_scale / 100.0)
                dispW    = pb.get_width()  * scale
                dispH    = pb.get_height() * scale
                # Fit within available area
                fitScale = min(logoAreaW / max(dispW, 1), logoAreaH / max(dispH, 1), 1.0)
                drawW    = dispW * fitScale
                drawH    = dispH * fitScale
                drawX    = bx + PAD + (logoAreaW - drawW) / 2
                drawY    = cursorY + (logoAreaH - drawH) / 2
                cr.save()
                cr.rectangle(bx + PAD, cursorY, logoAreaW, logoAreaH); cr.clip()
                cr.translate(drawX, drawY)
                cr.scale(drawW / pb.get_width(), drawH / pb.get_height())
                Gdk.cairo_set_source_pixbuf(cr, pb, 0, 0)
                cr.paint()
                cr.restore()
            else:
                # Placeholder box
                cr.set_source_rgba(0.75, 0.85, 0.95, 0.85)
                cr.rectangle(bx + PAD, cursorY, 40, 40); cr.fill()
                cr.set_source_rgba(0.2, 0.3, 0.5, 0.75)
                cr.select_font_face("Sans", 0, 0); cr.set_font_size(8)
                cr.move_to(bx + PAD + 4, cursorY + 24)
                cr.show_text("Logo")
            cursorY += logoAreaH + 6

        # ── ISBN + barcode block near spine edge ──────────────────────
        if s.isbn_enabled:
            blockW  = max(55, bw * 2 // 3)
            blockH  = 42
            isbnY   = by + bh - blockH - 10
            isbnX   = (bx + bw - blockW - 4) if not rtl else (bx + 4)

            cr.set_source_rgba(0.97, 0.97, 0.97, 0.95)
            cr.rectangle(isbnX, isbnY, blockW, blockH); cr.fill()
            cr.set_source_rgb(0, 0, 0)
            cr.set_line_width(0.8)
            cr.rectangle(isbnX, isbnY, blockW, blockH); cr.stroke()

            # Barcode stripes
            sx2, sy2, sh2 = isbnX + 4, isbnY + 4, blockH - 18
            for i in range(20):
                cr.set_source_rgb(0, 0, 0) if i % 3 != 1 else cr.set_source_rgb(1, 1, 1)
                cr.rectangle(sx2 + i * 3, sy2, 2, sh2); cr.fill()

            cr.set_source_rgb(0, 0, 0)
            cr.select_font_face("Sans", 0, 0); cr.set_font_size(7)
            display = s.isbn if s.isbn else "ISBN + BARCODE"
            cr.move_to(isbnX + 4, isbnY + blockH - 5)
            cr.show_text(display[:24])


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    app = CoverWizardApp()
    Gtk.main()

if __name__ == "__main__":
    main()
