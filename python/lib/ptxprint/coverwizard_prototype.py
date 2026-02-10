#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Standalone GTK3 (PyGObject) prototype of a surface-based Cover Wizard.

Changes in this revision (per user list):
1) Removed Step-2 "Coverage diagram" widget entirely.
2) Added right margin gap (12) to bx_left in Glade.
3) Preview now draws panels with NO gap and SINGLE divider lines (no doubled lines).
4) Spine orientation has 2 vertical directions + 1 horizontal.
5) ISBN + barcode placeholder merged and positioned near the spine edge on the back panel.
6) Added option to include Subtitle on spine (after title, before language).
7) Step-2 first option label dynamically avoids mentioning spine when spine disabled.
8) Header title changed to: "A guided cover wizard for translators"
9) Removed unwanted divider line between left and preview by replacing GtkPaned with GtkBox.
"""

from __future__ import annotations

import json
import os, sys
from dataclasses import asdict, dataclass
from typing import List

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # type: ignore


def _(s: str) -> str:
    # Placeholder for gettext integration later.
    return s


@dataclass
class WorkingCoverState:
    spine_enabled: bool = False
    pagecount: int = 0

    coverage_pattern: str = "wrap_all"  # wrap_all|front_only|front_spine|back_only|back_spine|front_back_separate|none

    bg_mode: str = "white"  # white|solid|gradient
    bg_color: str = "#f2f2f2"  # hex

    title: str = ""
    subtitle_enabled: bool = False
    subtitle: str = ""
    langname_enabled: bool = False
    langname: str = ""

    title_placement: str = "center"  # top|center|bottom|box

    spine_title: bool = True
    spine_subtitle: bool = False  # NEW
    spine_langname: bool = False
    spine_orientation: str = "v_ttb"  # v_ttb|v_btt|horizontal

    backtext_enabled: bool = False
    backtext: str = ""
    isbn_enabled: bool = False
    isbn: str = ""
    logo_enabled: bool = False


class CoverWizardApp:
    ALL_PAGES = [
        "pg_step1_spine",
        "pg_step2_coverage",
        "pg_step3_background",
        "pg_step4_front",
        "pg_step5_spinecontent",  # conditional
        "pg_step6_back",
        "pg_step7_review",
    ]

    def __init__(self, glade_path: str) -> None:
        self.glade_path = glade_path
        self.builder = Gtk.Builder()

        try:
            self.builder.add_from_file(glade_path)
        except Exception as e:
            raise SystemExit(f"Failed to load glade file: {glade_path}\n{e}")

        self.builder.connect_signals(self)

        self.w_coverwizard: Gtk.Window = self._get("w_coverwizard", Gtk.Window)
        self.st_steps: Gtk.Stack = self._get("st_steps", Gtk.Stack)
        self.l_progress: Gtk.Label = self._get("l_progress", Gtk.Label)
        self.l_summary: Gtk.Label = self._get("l_summary", Gtk.Label)

        self.btn_back: Gtk.Button = self._get("btn_back", Gtk.Button)
        self.btn_next: Gtk.Button = self._get("btn_next", Gtk.Button)
        self.btn_finish: Gtk.Button = self._get("btn_finish", Gtk.Button)

        self.da_preview: Gtk.DrawingArea = self._get("da_preview", Gtk.DrawingArea)

        # Revealers
        self.rv_subtitle: Gtk.Revealer = self._get("rv_subtitle", Gtk.Revealer)
        self.rv_langname: Gtk.Revealer = self._get("rv_langname", Gtk.Revealer)
        self.rv_backtext: Gtk.Revealer = self._get("rv_backtext", Gtk.Revealer)
        self.rv_isbn: Gtk.Revealer = self._get("rv_isbn", Gtk.Revealer)
        self.rv_logo: Gtk.Revealer = self._get("rv_logo", Gtk.Revealer)

        # Step 1
        self.t_pagecount: Gtk.Entry = self._get("t_pagecount", Gtk.Entry)
        self.r_spine_no: Gtk.RadioButton = self._get("r_spine_no", Gtk.RadioButton)
        self.r_spine_yes: Gtk.RadioButton = self._get("r_spine_yes", Gtk.RadioButton)

        # Step 2
        self.r_cov_wrap_all: Gtk.RadioButton = self._get("r_cov_wrap_all", Gtk.RadioButton)
        self.r_cov_front_only: Gtk.RadioButton = self._get("r_cov_front_only", Gtk.RadioButton)
        self.r_cov_front_spine: Gtk.RadioButton = self._get("r_cov_front_spine", Gtk.RadioButton)
        self.r_cov_back_only: Gtk.RadioButton = self._get("r_cov_back_only", Gtk.RadioButton)
        self.r_cov_back_spine: Gtk.RadioButton = self._get("r_cov_back_spine", Gtk.RadioButton)
        self.r_cov_front_back_separate: Gtk.RadioButton = self._get("r_cov_front_back_separate", Gtk.RadioButton)
        self.r_cov_none: Gtk.RadioButton = self._get("r_cov_none", Gtk.RadioButton)

        # Step 3
        self.r_bg_white: Gtk.RadioButton = self._get("r_bg_white", Gtk.RadioButton)
        self.r_bg_solid: Gtk.RadioButton = self._get("r_bg_solid", Gtk.RadioButton)
        self.r_bg_gradient: Gtk.RadioButton = self._get("r_bg_gradient", Gtk.RadioButton)
        self.cb_bgcolor: Gtk.ColorButton = self._get("cb_bgcolor", Gtk.ColorButton)

        # Step 4
        self.t_title: Gtk.Entry = self._get("t_title", Gtk.Entry)
        self.c_subtitle_enable: Gtk.CheckButton = self._get("c_subtitle_enable", Gtk.CheckButton)
        self.t_subtitle: Gtk.Entry = self._get("t_subtitle", Gtk.Entry)
        self.c_langname_enable: Gtk.CheckButton = self._get("c_langname_enable", Gtk.CheckButton)
        self.t_langname: Gtk.Entry = self._get("t_langname", Gtk.Entry)

        self.r_title_top: Gtk.RadioButton = self._get("r_title_top", Gtk.RadioButton)
        self.r_title_center: Gtk.RadioButton = self._get("r_title_center", Gtk.RadioButton)
        self.r_title_bottom: Gtk.RadioButton = self._get("r_title_bottom", Gtk.RadioButton)
        self.r_title_box: Gtk.RadioButton = self._get("r_title_box", Gtk.RadioButton)

        # Step 5
        self.c_spine_title: Gtk.CheckButton = self._get("c_spine_title", Gtk.CheckButton)
        self.c_spine_subtitle: Gtk.CheckButton = self._get("c_spine_subtitle", Gtk.CheckButton)
        self.c_spine_langname: Gtk.CheckButton = self._get("c_spine_langname", Gtk.CheckButton)
        self.r_spine_text_v_ttb: Gtk.RadioButton = self._get("r_spine_text_v_ttb", Gtk.RadioButton)
        self.r_spine_text_v_btt: Gtk.RadioButton = self._get("r_spine_text_v_btt", Gtk.RadioButton)
        self.r_spine_text_horizontal: Gtk.RadioButton = self._get("r_spine_text_horizontal", Gtk.RadioButton)

        # Step 6
        self.c_backtext_enable: Gtk.CheckButton = self._get("c_backtext_enable", Gtk.CheckButton)
        self.t_backtext: Gtk.TextView = self._get("t_backtext", Gtk.TextView)
        self.c_isbn_enable: Gtk.CheckButton = self._get("c_isbn_enable", Gtk.CheckButton)
        self.t_isbn: Gtk.Entry = self._get("t_isbn", Gtk.Entry)
        self.c_logo_enable: Gtk.CheckButton = self._get("c_logo_enable", Gtk.CheckButton)
        self.l_logo_status: Gtk.Label = self._get("l_logo_status", Gtk.Label)

        # IMPORTANT: GtkTextView buffer change signal must be connected in Python.
        self.t_backtext.get_buffer().connect("changed", self.on_backtext_buffer_changed)

        self.state = WorkingCoverState()
        self.enabled_pages: List[str] = []
        self.current_step_index: int = 0

        # Values: spread|front|spine|back
        self.active_surface: str = "spread"

        self._ui_guard: bool = False

        self._init_defaults()
        self._rebuild_enabled_pages()
        self._go_to_index(0)
        self._refresh_everything()

        self.w_coverwizard.connect("destroy", Gtk.main_quit)
        self.w_coverwizard.show_all()

    def _get(self, obj_id: str, cls):
        o = self.builder.get_object(obj_id)
        if o is None:
            raise RuntimeError(f"Glade object not found: {obj_id}")
        if not isinstance(o, cls):
            raise RuntimeError(f"Glade object {obj_id} expected {cls}, got {type(o)}")
        return o

    def _init_defaults(self) -> None:
        rgba = Gdk.RGBA()
        rgba.parse(self.state.bg_color)
        self.cb_bgcolor.set_rgba(rgba)

        self.r_spine_no.set_active(True)
        self.r_cov_wrap_all.set_active(True)
        self.r_bg_white.set_active(True)
        self.r_title_center.set_active(True)

        self.c_spine_title.set_active(True)
        self.c_spine_subtitle.set_active(False)
        self.c_spine_langname.set_active(False)
        self.r_spine_text_v_ttb.set_active(True)

        self.rv_subtitle.set_reveal_child(False)
        self.rv_langname.set_reveal_child(False)
        self.rv_backtext.set_reveal_child(False)
        self.rv_isbn.set_reveal_child(False)
        self.rv_logo.set_reveal_child(False)

    # -------------------------
    # Dynamic step management
    # -------------------------

    def _rebuild_enabled_pages(self) -> None:
        pages = list(self.ALL_PAGES)
        if not self.state.spine_enabled and "pg_step5_spinecontent" in pages:
            pages.remove("pg_step5_spinecontent")
        self.enabled_pages = pages
        self.current_step_index = max(0, min(self.current_step_index, len(self.enabled_pages) - 1))

    def _go_to_index(self, idx: int) -> None:
        self.current_step_index = max(0, min(idx, len(self.enabled_pages) - 1))
        page_id = self.enabled_pages[self.current_step_index]
        self.st_steps.set_visible_child_name(page_id)
        self._update_progress_label()
        self._update_nav_buttons()
        self._update_active_surface()
        self._update_finish_sensitivity()

    def _update_progress_label(self) -> None:
        step_no = self.current_step_index + 1
        total = len(self.enabled_pages)

        title_map = {
            "pg_step1_spine": _("Spine"),
            "pg_step2_coverage": _("Artwork coverage"),
            "pg_step3_background": _("Background"),
            "pg_step4_front": _("Front content"),
            "pg_step5_spinecontent": _("Spine content"),
            "pg_step6_back": _("Back content"),
            "pg_step7_review": _("Review"),
        }
        page_id = self.enabled_pages[self.current_step_index]
        self.l_progress.set_text(_("Step {} of {} — {}").format(step_no, total, title_map.get(page_id, page_id)))

    def _update_nav_buttons(self) -> None:
        at_first = self.current_step_index == 0
        at_last = self.current_step_index == (len(self.enabled_pages) - 1)
        self.btn_back.set_sensitive(not at_first)
        self.btn_next.set_sensitive(not at_last)
        self.btn_finish.set_sensitive(at_last and self._is_title_valid())
        self.w_coverwizard.set_default(self.btn_finish if at_last else self.btn_next)

    def _update_active_surface(self) -> None:
        page_id = self.enabled_pages[self.current_step_index]
        if page_id in ("pg_step2_coverage", "pg_step3_background", "pg_step7_review"):
            self.active_surface = "spread"
        elif page_id == "pg_step4_front":
            self.active_surface = "front"
        elif page_id == "pg_step5_spinecontent":
            self.active_surface = "spine"
        elif page_id == "pg_step6_back":
            self.active_surface = "back"
        else:
            self.active_surface = "spread"

    # -------------------------
    # Validation / Finish
    # -------------------------

    def _is_title_valid(self) -> bool:
        return bool(self.state.title.strip())

    def _update_finish_sensitivity(self) -> None:
        at_last = self.current_step_index == (len(self.enabled_pages) - 1)
        self.btn_finish.set_sensitive(at_last and self._is_title_valid())

    def _finish(self) -> None:
        payload = asdict(self.state)
        print(json.dumps(payload, indent=2, ensure_ascii=False))

        try:
            with open("coverwizard_state.json", "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self._show_error(_("Could not write coverwizard_state.json"), str(e))
            return

        md = Gtk.MessageDialog(
            transient_for=self.w_coverwizard,
            modal=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=_("Saved coverwizard_state.json"),
        )
        md.format_secondary_text(_("State also printed to console as JSON."))
        md.run()
        md.destroy()

    # -------------------------
    # UI refresh (central)
    # -------------------------

    def _refresh_everything(self) -> None:
        self._apply_spine_coverage_disclosure()
        self._apply_spine_subtitle_disclosure()

        self._update_summary()
        self.da_preview.queue_draw()

        self._update_nav_buttons()

    def _apply_spine_coverage_disclosure(self) -> None:
        spine = self.state.spine_enabled

        # Requirement #7: adjust wrap_all label based on spine
        if spine:
            self.r_cov_wrap_all.set_label(_("Wrap all (one image across front + spine + back)"))
        else:
            self.r_cov_wrap_all.set_label(_("Wrap all (one image across front + back)"))

        # Hide spine-related patterns if no spine
        self.r_cov_front_spine.set_visible(spine)
        self.r_cov_back_spine.set_visible(spine)

        # If current selection is invalid while spine is off, coerce safely
        if not spine and self.state.coverage_pattern in ("front_spine", "back_spine"):
            self.state.coverage_pattern = "front_only"
            self._ui_guard = True
            try:
                self.r_cov_front_only.set_active(True)
            finally:
                self._ui_guard = False

    def _apply_spine_subtitle_disclosure(self) -> None:
        """
        Spine-subtitle checkbox should only be meaningful if subtitle exists/enabled.
        Keep it calm: disable the checkbox if subtitle not enabled on front.
        """
        can_use = self.state.subtitle_enabled
        self.c_spine_subtitle.set_sensitive(can_use)
        if not can_use and self.state.spine_subtitle:
            self._ui_guard = True
            try:
                self.c_spine_subtitle.set_active(False)
            finally:
                self._ui_guard = False
            self.state.spine_subtitle = False

    def _update_summary(self) -> None:
        s = self.state
        cov_label = {
            "wrap_all": _("Wrap all"),
            "front_only": _("Front only"),
            "front_spine": _("Front + spine"),
            "back_only": _("Back only"),
            "back_spine": _("Back + spine"),
            "front_back_separate": _("Front/back separate"),
            "none": _("None (plain)"),
        }.get(s.coverage_pattern, s.coverage_pattern)

        bg_label = {"white": _("White"), "solid": _("Solid"), "gradient": _("Gradient")}.get(s.bg_mode, s.bg_mode)

        orient_label = {
            "v_ttb": _("Vertical (top to bottom)"),
            "v_btt": _("Vertical (bottom to top)"),
            "horizontal": _("Horizontal"),
        }.get(s.spine_orientation, s.spine_orientation)

        lines = []
        lines.append(_("Spine: {} (pagecount={})").format(_("Yes") if s.spine_enabled else _("No"), s.pagecount))
        lines.append(_("Artwork coverage: {}").format(cov_label))
        lines.append(_("Background: {}").format(bg_label + (f" {s.bg_color}" if s.bg_mode == "solid" else "")))
        lines.append(_("Title placement: {}").format(s.title_placement))
        lines.append(_("Title: {}").format(s.title.strip() if s.title.strip() else _("(missing)")))

        if s.subtitle_enabled:
            lines.append(_("Subtitle: {}").format(s.subtitle.strip() or _("(empty)")))
        if s.langname_enabled:
            lines.append(_("Language/Translation: {}").format(s.langname.strip() or _("(empty)")))

        if s.spine_enabled:
            lines.append(_("Spine title: {}").format(_("on") if s.spine_title else _("off")))
            lines.append(_("Spine subtitle: {}").format(_("on") if s.spine_subtitle else _("off")))
            lines.append(_("Spine language name: {}").format(_("on") if s.spine_langname else _("off")))
            lines.append(_("Spine orientation: {}").format(orient_label))

        if s.backtext_enabled:
            lines.append(_("Back text: enabled"))
        if s.isbn_enabled:
            lines.append(_("ISBN: {}").format(s.isbn.strip() or _("(empty)")))
        if s.logo_enabled:
            lines.append(_("Logo: enabled (stub)"))

        self.l_summary.set_text("\n".join(lines))

    # -------------------------
    # Helpers
    # -------------------------

    def _parse_int(self, text: str, default: int = 0) -> int:
        try:
            t = text.strip()
            if not t:
                return default
            return int(t)
        except Exception:
            return default

    def _rgba_to_hex(self, rgba: Gdk.RGBA) -> str:
        r = max(0, min(255, int(rgba.red * 255)))
        g = max(0, min(255, int(rgba.green * 255)))
        b = max(0, min(255, int(rgba.blue * 255)))
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def _hex_to_rgb01(self, hex_color: str):
        hc = hex_color.strip().lstrip("#")
        if len(hc) != 6:
            return (0.95, 0.95, 0.95)
        r = int(hc[0:2], 16) / 255.0
        g = int(hc[2:4], 16) / 255.0
        b = int(hc[4:6], 16) / 255.0
        return (r, g, b)

    def _show_error(self, primary: str, secondary: str) -> None:
        md = Gtk.MessageDialog(
            transient_for=self.w_coverwizard,
            modal=True,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=primary,
        )
        md.format_secondary_text(secondary)
        md.run()
        md.destroy()

    # -------------------------
    # Navigation button handlers
    # -------------------------

    def on_btn_cancel_clicked(self, _btn: Gtk.Button) -> None:
        self.w_coverwizard.close()

    def on_btn_back_clicked(self, _btn: Gtk.Button) -> None:
        if self.current_step_index > 0:
            self._go_to_index(self.current_step_index - 1)
            self._refresh_everything()

    def on_btn_next_clicked(self, _btn: Gtk.Button) -> None:
        if self.current_step_index < len(self.enabled_pages) - 1:
            self._rebuild_enabled_pages()
            self._go_to_index(self.current_step_index + 1)
            self._refresh_everything()

    def on_btn_finish_clicked(self, _btn: Gtk.Button) -> None:
        if self.current_step_index == len(self.enabled_pages) - 1 and self._is_title_valid():
            self._finish()

    def on_btn_advanced_clicked(self, _btn: Gtk.Button) -> None:
        md = Gtk.MessageDialog(
            transient_for=self.w_coverwizard,
            modal=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=_("Advanced settings (prototype)"),
        )
        md.format_secondary_text(_("In PTXprint integration this would open the existing cover dialogs pre-filled."))
        md.run()
        md.destroy()

    # -------------------------
    # Step 1: spine + pagecount
    # -------------------------

    def on_t_pagecount_changed(self, entry: Gtk.Entry) -> None:
        if self._ui_guard:
            return
        pc = self._parse_int(entry.get_text(), default=0)
        self.state.pagecount = max(0, pc)
        self._refresh_everything()

    def on_r_spine_no_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self.state.spine_enabled = False
        self._rebuild_enabled_pages()
        if self.enabled_pages[self.current_step_index] == "pg_step5_spinecontent":
            self._go_to_index(min(self.current_step_index, len(self.enabled_pages) - 1))
        self._refresh_everything()

    def on_r_spine_yes_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self.state.spine_enabled = True
        self._rebuild_enabled_pages()
        self._refresh_everything()

    # -------------------------
    # Step 2: coverage patterns
    # -------------------------

    def _set_coverage(self, value: str) -> None:
        self.state.coverage_pattern = value
        self._refresh_everything()

    def on_r_cov_wrap_all_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self._set_coverage("wrap_all")

    def on_r_cov_front_only_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self._set_coverage("front_only")

    def on_r_cov_front_spine_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self._set_coverage("front_spine")

    def on_r_cov_back_only_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self._set_coverage("back_only")

    def on_r_cov_back_spine_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self._set_coverage("back_spine")

    def on_r_cov_front_back_separate_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self._set_coverage("front_back_separate")

    def on_r_cov_none_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self._set_coverage("none")

    # -------------------------
    # Step 3: background
    # -------------------------

    def on_r_bg_white_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self.state.bg_mode = "white"
        self._refresh_everything()

    def on_r_bg_solid_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self.state.bg_mode = "solid"
        self._refresh_everything()

    def on_r_bg_gradient_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self.state.bg_mode = "gradient"
        self._refresh_everything()

    def on_cb_bgcolor_color_set(self, cb: Gtk.ColorButton) -> None:
        if self._ui_guard:
            return
        rgba = cb.get_rgba()
        self.state.bg_color = self._rgba_to_hex(rgba)
        self._refresh_everything()

    # -------------------------
    # Step 4: front content
    # -------------------------

    def on_t_title_changed(self, entry: Gtk.Entry) -> None:
        if self._ui_guard:
            return
        self.state.title = entry.get_text()
        self._refresh_everything()

    def on_c_subtitle_enable_toggled(self, cb: Gtk.CheckButton) -> None:
        if self._ui_guard:
            return
        self.state.subtitle_enabled = cb.get_active()
        self.rv_subtitle.set_reveal_child(self.state.subtitle_enabled)
        self._refresh_everything()

    def on_t_subtitle_changed(self, entry: Gtk.Entry) -> None:
        if self._ui_guard:
            return
        self.state.subtitle = entry.get_text()
        self._refresh_everything()

    def on_c_langname_enable_toggled(self, cb: Gtk.CheckButton) -> None:
        if self._ui_guard:
            return
        self.state.langname_enabled = cb.get_active()
        self.rv_langname.set_reveal_child(self.state.langname_enabled)
        self._refresh_everything()

    def on_t_langname_changed(self, entry: Gtk.Entry) -> None:
        if self._ui_guard:
            return
        self.state.langname = entry.get_text()
        self._refresh_everything()

    def on_r_title_top_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self.state.title_placement = "top"
        self._refresh_everything()

    def on_r_title_center_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self.state.title_placement = "center"
        self._refresh_everything()

    def on_r_title_bottom_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self.state.title_placement = "bottom"
        self._refresh_everything()

    def on_r_title_box_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self.state.title_placement = "box"
        self._refresh_everything()

    # -------------------------
    # Step 5: spine content
    # -------------------------

    def on_c_spine_title_toggled(self, cb: Gtk.CheckButton) -> None:
        if self._ui_guard:
            return
        self.state.spine_title = cb.get_active()
        self._refresh_everything()

    def on_c_spine_subtitle_toggled(self, cb: Gtk.CheckButton) -> None:
        if self._ui_guard:
            return
        self.state.spine_subtitle = cb.get_active()
        self._refresh_everything()

    def on_c_spine_langname_toggled(self, cb: Gtk.CheckButton) -> None:
        if self._ui_guard:
            return
        self.state.spine_langname = cb.get_active()
        self._refresh_everything()

    def on_r_spine_text_v_ttb_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self.state.spine_orientation = "v_ttb"
        self._refresh_everything()

    def on_r_spine_text_v_btt_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self.state.spine_orientation = "v_btt"
        self._refresh_everything()

    def on_r_spine_text_horizontal_toggled(self, rb: Gtk.RadioButton) -> None:
        if self._ui_guard or not rb.get_active():
            return
        self.state.spine_orientation = "horizontal"
        self._refresh_everything()

    # -------------------------
    # Step 6: back content
    # -------------------------

    def on_c_backtext_enable_toggled(self, cb: Gtk.CheckButton) -> None:
        if self._ui_guard:
            return
        self.state.backtext_enabled = cb.get_active()
        self.rv_backtext.set_reveal_child(self.state.backtext_enabled)
        self._refresh_everything()

    def on_backtext_buffer_changed(self, buf: Gtk.TextBuffer) -> None:
        if self._ui_guard:
            return
        start, end = buf.get_bounds()
        self.state.backtext = buf.get_text(start, end, True)
        self._refresh_everything()

    def on_c_isbn_enable_toggled(self, cb: Gtk.CheckButton) -> None:
        if self._ui_guard:
            return
        self.state.isbn_enabled = cb.get_active()
        self.rv_isbn.set_reveal_child(self.state.isbn_enabled)
        self._refresh_everything()

    def on_t_isbn_changed(self, entry: Gtk.Entry) -> None:
        if self._ui_guard:
            return
        self.state.isbn = entry.get_text()
        self._refresh_everything()

    def on_c_logo_enable_toggled(self, cb: Gtk.CheckButton) -> None:
        if self._ui_guard:
            return
        self.state.logo_enabled = cb.get_active()
        self.rv_logo.set_reveal_child(self.state.logo_enabled)
        self._refresh_everything()

    def on_btn_logo_choose_clicked(self, _btn: Gtk.Button) -> None:
        dlg = Gtk.FileChooserDialog(
            title=_("Choose logo file"),
            transient_for=self.w_coverwizard,
            action=Gtk.FileChooserAction.OPEN,
        )
        dlg.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        resp = dlg.run()
        if resp == Gtk.ResponseType.OK:
            path = dlg.get_filename()
            self.l_logo_status.set_text(os.path.basename(path) if path else _("No file selected"))
        dlg.destroy()

    # -------------------------
    # Drawing: main live preview
    # -------------------------

    def on_da_preview_draw(self, widget: Gtk.DrawingArea, cr) -> bool:
        alloc = widget.get_allocation()
        w, h = alloc.width, alloc.height

        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, w, h)
        cr.fill()

        pad = 16
        self._draw_spread(cr, pad, pad, w - 2 * pad, h - 2 * pad, show_text=True)
        return False

    def _draw_spread(self, cr, x: int, y: int, w: int, h: int, show_text: bool) -> None:
        s = self.state

        # Background
        self._fill_background(cr, x, y, w, h, s.bg_mode, s.bg_color)

        spine_enabled = s.spine_enabled

        # Requirement #3: no gap between panels, and draw SINGLE divider lines ourselves
        gap = 0
        spine_w = int(w * (0.10 if spine_enabled else 0.0))

        if spine_enabled:
            panel_w = int((w - spine_w - 2 * gap) / 2)
            back = (x, y, panel_w, h)
            spine = (x + panel_w + gap, y, spine_w, h)
            front = (x + panel_w + gap + spine_w + gap, y, panel_w, h)
        else:
            panel_w = int((w - gap) / 2)
            back = (x, y, panel_w, h)
            spine = None
            front = (x + panel_w + gap, y, panel_w, h)

        # Whole outline (highlight spread steps)
        self._draw_outline(cr, x, y, w, h, highlight=(self.active_surface == "spread"))

        # Divider lines (single line only)
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(1.0)
        if spine_enabled and spine:
            # back|spine divider
            x1 = back[0] + back[2]
            cr.move_to(x1, y)
            cr.line_to(x1, y + h)
            cr.stroke()
            # spine|front divider
            x2 = spine[0] + spine[2]
            cr.move_to(x2, y)
            cr.line_to(x2, y + h)
            cr.stroke()
        else:
            # back|front divider
            x1 = back[0] + back[2]
            cr.move_to(x1, y)
            cr.line_to(x1, y + h)
            cr.stroke()

        # Panel highlight rectangles (thicker line) — drawn last so it's clear, but does not create double separators normally.
        self._draw_highlight_panel(cr, back, highlight=(self.active_surface == "back"))
        if spine_enabled and spine:
            self._draw_highlight_panel(cr, spine, highlight=(self.active_surface == "spine"))
        self._draw_highlight_panel(cr, front, highlight=(self.active_surface == "front"))

        margin = 14

        # Coverage
        self._draw_coverage(cr, back, spine, front, margin)

        if not show_text:
            return

        # FRONT
        self._draw_front_text(cr, front, margin)

        # SPINE
        if spine_enabled and spine:
            self._draw_spine_text(cr, spine, margin)

        # BACK
        self._draw_back_blocks(cr, back, margin, spine_enabled=spine_enabled)

        self._draw_footer_hint(cr, x, y, w, h)

    def _fill_background(self, cr, x: int, y: int, w: int, h: int, mode: str, hex_color: str) -> None:
        if mode == "white":
            cr.set_source_rgb(1, 1, 1)
            cr.rectangle(x, y, w, h)
            cr.fill()
            return

        if mode == "solid":
            r, g, b = self._hex_to_rgb01(hex_color)
            cr.set_source_rgb(r, g, b)
            cr.rectangle(x, y, w, h)
            cr.fill()
            return

        # gradient: simple bands (fast)
        r, g, b = self._hex_to_rgb01("#f2f2f2")
        bands = 10
        for i in range(bands):
            t = i / max(1, bands - 1)
            shade = 0.92 + (0.06 * t)
            cr.set_source_rgba(r * shade, g * shade, b * shade, 1.0)
            cr.rectangle(x, y + int(h * t), w, int(h / bands) + 1)
            cr.fill()

    def _draw_outline(self, cr, x: int, y: int, w: int, h: int, highlight: bool) -> None:
        cr.set_line_width(3.0 if highlight else 1.0)
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(x, y, w, h)
        cr.stroke()

    def _draw_highlight_panel(self, cr, rect, highlight: bool) -> None:
        if not highlight:
            return
        x, y, w, h = rect
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(3.0)
        cr.rectangle(x, y, w, h)
        cr.stroke()

    def _draw_coverage(self, cr, back, spine, front, margin: int) -> None:
        s = self.state
        pat = s.coverage_pattern

        def tint_rect(rect, label="IMAGE"):
            x, y, w, h = rect
            x2 = x + margin
            y2 = y + margin
            w2 = max(10, w - 2 * margin)
            h2 = max(10, h - 2 * margin)

            cr.set_source_rgba(0.2, 0.5, 0.9, 0.18)
            cr.rectangle(x2, y2, w2, h2)
            cr.fill()

            cr.set_source_rgba(0.2, 0.5, 0.9, 0.45)
            cr.set_line_width(1.0)
            cr.rectangle(x2, y2, w2, h2)
            cr.stroke()

            cr.set_source_rgb(0.1, 0.2, 0.4)
            cr.select_font_face("Sans", 0, 0)
            cr.set_font_size(11)
            cr.move_to(x2 + 6, y2 + 16)
            cr.show_text(label)

        if pat == "none":
            return

        if pat == "wrap_all":
            tint_rect(front)
            tint_rect(back)
            if s.spine_enabled and spine:
                tint_rect(spine)
            return

        if pat == "front_only":
            tint_rect(front)
            return

        if pat == "back_only":
            tint_rect(back)
            return

        if pat == "front_spine":
            tint_rect(front)
            if s.spine_enabled and spine:
                tint_rect(spine)
            return

        if pat == "back_spine":
            tint_rect(back)
            if s.spine_enabled and spine:
                tint_rect(spine)
            return

        if pat == "front_back_separate":
            tint_rect(front, label="IMAGE (front)")
            tint_rect(back, label="IMAGE (back)")
            return

    def _draw_front_text(self, cr, front, margin: int) -> None:
        s = self.state
        x, y, w, h = front

        if s.title_placement == "top":
            base_y = y + margin + 30
        elif s.title_placement == "bottom":
            base_y = y + h - margin - 60
        else:
            base_y = y + int(h * 0.45)

        if s.title_placement == "box":
            box_w = int(w * 0.80)
            box_h = 70
            bx = x + int((w - box_w) / 2)
            by = base_y - 40
            cr.set_source_rgba(1, 1, 1, 0.75)
            cr.rectangle(bx, by, box_w, box_h)
            cr.fill()
            cr.set_source_rgba(0, 0, 0, 0.25)
            cr.set_line_width(1.0)
            cr.rectangle(bx, by, box_w, box_h)
            cr.stroke()

        title = s.title.strip() if s.title.strip() else "TITLE"
        cr.set_source_rgb(0, 0, 0)
        cr.select_font_face("Sans", 0, 0)
        cr.set_font_size(18)
        self._draw_centered_text(cr, title, x + margin, base_y, w - 2 * margin)

        if s.subtitle_enabled:
            subtitle = s.subtitle.strip() if s.subtitle.strip() else "Subtitle"
            cr.set_font_size(12)
            self._draw_centered_text(cr, subtitle, x + margin, base_y + 26, w - 2 * margin)

        if s.langname_enabled:
            lang = s.langname.strip() if s.langname.strip() else "Language / Translation"
            cr.set_font_size(11)
            self._draw_centered_text(cr, lang, x + margin, base_y + 46, w - 2 * margin)

    def _draw_spine_text(self, cr, spine, margin: int) -> None:
        s = self.state
        x, y, w, h = spine

        parts = []
        if s.spine_title:
            parts.append(s.title.strip() if s.title.strip() else "TITLE")

        # Requirement #6: subtitle between title and langname, only if subtitle enabled AND opted in
        if s.spine_subtitle and s.subtitle_enabled:
            parts.append(s.subtitle.strip() if s.subtitle.strip() else "Subtitle")

        if s.spine_langname and s.langname_enabled:
            parts.append(s.langname.strip() if s.langname.strip() else "Language")

        text = " • ".join(parts) if parts else "SPINE"

        cr.set_source_rgb(0, 0, 0)
        cr.select_font_face("Sans", 0, 0)
        cr.set_font_size(11)

        if s.spine_orientation == "horizontal":
            self._draw_centered_text(cr, text, x + margin, y + int(h / 2), w - 2 * margin)
            return

        # Vertical orientations
        cr.save()
        cx = x + int(w / 2)
        cy = y + int(h / 2)
        cr.translate(cx, cy)

        if s.spine_orientation == "v_ttb":
            # top-to-bottom reading direction (visual)
            cr.rotate(-1.57079632679)  # -pi/2
        else:
            # bottom-to-top
            cr.rotate(1.57079632679)   # +pi/2

        # draw centered along rotated axis
        self._draw_centered_text(cr, text, -int(h / 2) + margin, 0, h - 2 * margin)
        cr.restore()

    def _draw_back_blocks(self, cr, back, margin: int, spine_enabled: bool) -> None:
        s = self.state
        x, y, w, h = back

        if s.backtext_enabled:
            bx = x + margin
            by = y + margin + 30
            bw = w - 2 * margin
            bh = int(h * 0.45)
            cr.set_source_rgba(1, 1, 1, 0.75)
            cr.rectangle(bx, by, bw, bh)
            cr.fill()
            cr.set_source_rgba(0, 0, 0, 0.25)
            cr.set_line_width(1.0)
            cr.rectangle(bx, by, bw, bh)
            cr.stroke()

            cr.set_source_rgb(0, 0, 0)
            cr.select_font_face("Sans", 0, 0)
            cr.set_font_size(10)
            cr.move_to(bx + 6, by + 16)
            cr.show_text("Back text here")

        # Requirement #5: ISBN+barcode merged and positioned near spine edge of back panel
        if s.isbn_enabled:
            block_w = int(w * 0.58)
            block_h = 56
            # place near spine (right side of back panel)
            ix = x + w - margin - block_w
            iy = y + h - margin - block_h

            cr.set_source_rgba(1, 1, 1, 0.85)
            cr.rectangle(ix, iy, block_w, block_h)
            cr.fill()
            cr.set_source_rgba(0, 0, 0, 0.25)
            cr.set_line_width(1.0)
            cr.rectangle(ix, iy, block_w, block_h)
            cr.stroke()

            cr.set_source_rgb(0, 0, 0)
            cr.select_font_face("Sans", 0, 0)
            cr.set_font_size(10)
            cr.move_to(ix + 6, iy + 16)
            cr.show_text("ISBN + BARCODE")

            cr.set_font_size(9)
            val = s.isbn.strip() if s.isbn.strip() else "978-..."
            cr.move_to(ix + 6, iy + 32)
            cr.show_text(val)

            # barcode stripes placeholder at right side of same box
            bx = ix + int(block_w * 0.62)
            bw = int(block_w * 0.35)
            by = iy + 10
            bh = block_h - 20
            cr.set_source_rgba(0, 0, 0, 0.10)
            cr.rectangle(bx, by, bw, bh)
            cr.fill()
            cr.set_source_rgba(0, 0, 0, 0.25)
            cr.rectangle(bx, by, bw, bh)
            cr.stroke()

            cr.set_source_rgb(0, 0, 0)
            cr.set_font_size(8)
            cr.move_to(bx + 6, by + 14)
            cr.show_text("BARCODE")

        if s.logo_enabled:
            lx = x + w - margin - 70
            ly = y + margin + 30
            lw = 60
            lh = 60
            cr.set_source_rgba(1, 1, 1, 0.75)
            cr.rectangle(lx, ly, lw, lh)
            cr.fill()
            cr.set_source_rgba(0, 0, 0, 0.25)
            cr.set_line_width(1.0)
            cr.rectangle(lx, ly, lw, lh)
            cr.stroke()
            cr.set_source_rgb(0, 0, 0)
            cr.set_font_size(9)
            cr.move_to(lx + 6, ly + 16)
            cr.show_text("Logo")

    def _draw_footer_hint(self, cr, x: int, y: int, w: int, h: int) -> None:
        cr.set_source_rgb(0, 0, 0)
        cr.select_font_face("Sans", 0, 0)
        cr.set_font_size(9)
        text = _("Active surface: {}").format(self.active_surface)
        cr.move_to(x + 4, y + h - 6)
        cr.show_text(text)

    def _draw_centered_text(self, cr, text: str, x: int, y: int, w: int) -> None:
        xbearing, ybearing, tw, th, xadv, yadv = cr.text_extents(text)
        tx = x + max(0, int((w - tw) / 2)) - xbearing
        ty = y
        cr.move_to(tx, ty)
        cr.show_text(text)


def main() -> None:
    # glade_path = "coverwizard_prototype.glade"
    glade_path = os.path.join(os.path.dirname(__file__), "coverwizard_prototype.glade")
    print(f"{glade_path=}")
    app = CoverWizardApp(glade_path)
    Gtk.main()


if __name__ == "__main__":
    main()
