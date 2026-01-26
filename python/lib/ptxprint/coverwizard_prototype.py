#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Standalone PTXprint Cover Wizard prototype (GTK3 + Glade).
- Uses PTXprint-style widget IDs (c_, r_, fr_, l_, btn_, etc.)
- Implements composable, reversible presets.
- Simulates a live preview with highlight (front/spine/back/spread).
- Implements exact step order with conditional Step 3a.
- “Advanced settings…” escape hatch stub.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib  # type: ignore


def _(s: str) -> str:
    # Placeholder for i18n (hook gettext in PTXprint integration)
    return s


# ============================================================
# Preset architecture: composable + reversible + inspectable
# ============================================================

@dataclass(frozen=True)
class CoverPreset:
    name: str
    settings: Dict[str, Any] = field(default_factory=dict)
    notes: str = ""

    def apply(self, settings: "SettingsAdapter") -> Dict[str, Any]:
        old: Dict[str, Any] = {}
        for k, v in self.settings.items():
            old[k] = settings.get(k)
            settings.set(k, v)
        return old


class PresetStack:
    def __init__(self) -> None:
        self._applied: List[Tuple[CoverPreset, Dict[str, Any]]] = []

    def clear(self) -> None:
        self._applied.clear()

    def apply(self, preset: CoverPreset, settings: "SettingsAdapter") -> None:
        diff = preset.apply(settings)
        self._applied.append((preset, diff))

    def rollback_all(self, settings: "SettingsAdapter") -> None:
        while self._applied:
            preset, diff = self._applied.pop()
            for k, oldval in diff.items():
                settings.set(k, oldval)

    def names(self) -> List[str]:
        return [p.name for p, _ in self._applied]


# ============================================================
# Settings + Preview adapters (prototype versions)
# ============================================================

class SettingsAdapter:
    """
    Prototype settings storage. In PTXprint integration, map these keys to
    real PTXprint config / periph / style keys.
    """
    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def snapshot(self) -> Dict[str, Any]:
        return dict(self._data)


class PreviewState:
    def __init__(self) -> None:
        self.highlight_region: str = "spread"
        self.last_settings: Dict[str, Any] = {}


# ============================================================
# Cover Wizard Controller (prototype)
# ============================================================

class CoverWizardController:
    STEP_IDS_ALL = [
        "step1_complexity",
        "step2_spine",
        "step3_background",
        "step3a_layering",   # conditional
        "step4_title",
        "step5_optional",
        "step6_review",
    ]

    def __init__(self, builder: Gtk.Builder, parent: Gtk.Window, settings: SettingsAdapter) -> None:
        self.builder = builder
        self.parent = parent
        self.settings = settings
        self.preset_stack = PresetStack()

        self.preview = PreviewState()

        # Dialog + key widgets
        self.dlg: Gtk.Dialog = builder.get_object("dlgCoverWizard")
        self.stk: Gtk.Stack = builder.get_object("stk_coverwizard")
        self.l_progress: Gtk.Label = builder.get_object("l_progress")
        self.l_summary: Gtk.Label = builder.get_object("l_summary")

        self.btn_back: Gtk.Button = builder.get_object("btn_back")
        self.btn_next: Gtk.Button = builder.get_object("btn_next")
        self.btn_finish: Gtk.Button = builder.get_object("btn_finish")

        self.da_preview: Gtk.DrawingArea = builder.get_object("da_preview")

        # Revealers (optional micro-panels)
        self.rv_subtitle: Gtk.Revealer = builder.get_object("rv_subtitle")
        self.rv_author: Gtk.Revealer = builder.get_object("rv_author")
        self.rv_backtext: Gtk.Revealer = builder.get_object("rv_backtext")
        self.rv_isbn: Gtk.Revealer = builder.get_object("rv_isbn")
        self.rv_border: Gtk.Revealer = builder.get_object("rv_border")

        # Decisions
        self.decisions: Dict[str, Any] = {
            "complexity": "simple",        # simple | published
            "spine": False,
            "background": "white",         # white | plain | one_image | two_images
            "image_layering": "behind",    # behind | overlay | front_only
            "title_placement": "center",   # center | top | bottom | box
            "optional": {
                "subtitle": False,
                "author": False,
                "backtext": False,
                "isbn": False,
                "border": False,
            },
        }

        # Active steps + index
        self.active_steps: List[str] = []
        self.step_index: int = 0

        # Configure dialog parenting
        self.dlg.set_transient_for(parent)
        self.dlg.set_modal(True)

        # initial build
        self._rebuild_active_steps()
        self._show_step(self.active_steps[self.step_index])
        self._apply_presets_up_to(self.active_steps[self.step_index])
        self._update_nav()
        self._update_preview_for_step()

    # ---------------------------
    # Step flow
    # ---------------------------

    def _rebuild_active_steps(self) -> None:
        steps = list(self.STEP_IDS_ALL)

        bg = self.decisions["background"]
        wants_images = bg in ("one_image", "two_images")
        if not wants_images and "step3a_layering" in steps:
            steps.remove("step3a_layering")

        # Simple mode hides “most” of the complexity (prototype choice: hide Step 5 + 3a)
        if self.decisions["complexity"] == "simple":
            if "step3a_layering" in steps:
                steps.remove("step3a_layering")
            if "step5_optional" in steps:
                steps.remove("step5_optional")

        self.active_steps = steps
        self.step_index = max(0, min(self.step_index, len(self.active_steps) - 1))

    def _show_step(self, step_id: str) -> None:
        self.stk.set_visible_child_name(step_id)
        self._update_progress_label()

    def _update_progress_label(self) -> None:
        step_no = self.step_index + 1
        total = len(self.active_steps)
        titles = {
            "step1_complexity": _("Choose a cover style"),
            "step2_spine": _("Spine"),
            "step3_background": _("Background"),
            "step3a_layering": _("Image layering"),
            "step4_title": _("Title placement"),
            "step5_optional": _("Optional elements"),
            "step6_review": _("Review"),
        }
        title = titles.get(self.active_steps[self.step_index], _("Cover Wizard"))
        self.l_progress.set_text(_("Step {}/{} — {}").format(step_no, total, title))

    def _update_nav(self) -> None:
        at_first = self.step_index == 0
        at_last = self.step_index == (len(self.active_steps) - 1)

        self.btn_back.set_sensitive(not at_first)
        self.btn_next.set_sensitive(not at_last)
        self.btn_finish.set_sensitive(at_last)

        self.dlg.set_default(self.btn_finish if at_last else self.btn_next)

    # ---------------------------
    # Preset mapping
    # ---------------------------

    def _apply_presets_up_to(self, step_id: str) -> None:
        # Rebuild deterministically: rollback everything, then apply in order.
        self.preset_stack.rollback_all(self.settings)
        self.preset_stack.clear()

        for sid in self.active_steps:
            for preset in self._presets_for_step(sid):
                self.preset_stack.apply(preset, self.settings)
            if sid == step_id:
                break

        self.preview.last_settings = self.settings.snapshot()
        self._update_summary()

        # redraw preview without blocking
        GLib.idle_add(self.da_preview.queue_draw)

    def _presets_for_step(self, step_id: str) -> List[CoverPreset]:
        d = self.decisions
        out: List[CoverPreset] = []

        if step_id == "step1_complexity":
            out.append(self._preset_simple_base() if d["complexity"] == "simple" else self._preset_published_base())
        elif step_id == "step2_spine":
            out.append(self._preset_spine(d["spine"]))
        elif step_id == "step3_background":
            out.append(self._preset_background(d["background"]))
        elif step_id == "step3a_layering":
            out.append(self._preset_layering(d["image_layering"]))
        elif step_id == "step4_title":
            out.append(self._preset_title(d["title_placement"]))
        elif step_id == "step5_optional":
            out.append(self._preset_optional(d["optional"]))
        elif step_id == "step6_review":
            pass

        return out

    # ---------------------------
    # Presets (prototype keys)
    # ---------------------------

    def _preset_simple_base(self) -> CoverPreset:
        return CoverPreset(
            name="simple_bw_minimal",
            notes=_("Minimal black & white cover with safe readable defaults."),
            settings={
                "cover.mode": "simple",
                "cover.color": "mono",
                "cover.use_images": False,
                "cover.spine.enabled": False,
                "cover.border.enabled": False,
                "cover.title.contrast_auto": True,
            },
        )

    def _preset_published_base(self) -> CoverPreset:
        return CoverPreset(
            name="published_color_pro",
            notes=_("Professional defaults: color/image ready, spine-capable."),
            settings={
                "cover.mode": "published",
                "cover.color": "color",
                "cover.use_images": True,
                "cover.title.contrast_auto": True,
                "cover.margins.safe": True,
            },
        )

    def _preset_spine(self, include_spine: bool) -> CoverPreset:
        if not include_spine:
            return CoverPreset(
                name="spine_none",
                notes=_("Disable spine"),
                settings={
                    "cover.spine.enabled": False,
                    "cover.spine.rotation": 0,
                    "cover.spine.width.mode": "none",
                },
            )
        return CoverPreset(
            name="spine_auto",
            notes=_("Enable spine with automatic safe defaults"),
            settings={
                "cover.spine.enabled": True,
                "cover.spine.width.mode": "auto",
                "cover.spine.rotation": 90,
                "cover.spine.align": "center",
            },
        )

    def _preset_background(self, bg: str) -> CoverPreset:
        if bg == "white":
            return CoverPreset(
                name="bg_white",
                notes=_("White background"),
                settings={"cover.bg.type": "none"},
            )
        if bg == "plain":
            return CoverPreset(
                name="bg_plain_color",
                notes=_("Plain color background"),
                settings={"cover.bg.type": "color", "cover.bg.color": "#f2f2f2"},
            )
        if bg == "one_image":
            return CoverPreset(
                name="bg_one_image",
                notes=_("One image background"),
                settings={"cover.bg.type": "image", "cover.bg.image.mode": "single", "cover.bg.image.scale": "cover"},
            )
        if bg == "two_images":
            return CoverPreset(
                name="bg_two_images",
                notes=_("Separate front/back images"),
                settings={"cover.bg.type": "image", "cover.bg.image.mode": "separate", "cover.bg.image.scale": "cover"},
            )
        return CoverPreset(name="bg_white_fallback", settings={"cover.bg.type": "none"})

    def _preset_layering(self, layering: str) -> CoverPreset:
        if layering == "behind":
            return CoverPreset(
                name="img_behind_text",
                notes=_("Image behind text"),
                settings={"cover.image.layer": "behind_text", "cover.title.contrast_auto": True},
            )
        if layering == "overlay":
            return CoverPreset(
                name="img_overlay_safe",
                notes=_("Overlay image with title protection"),
                settings={"cover.image.layer": "overlay", "cover.title.box.enabled": True, "cover.image.overlay.opacity": 0.25},
            )
        if layering == "front_only":
            return CoverPreset(
                name="img_front_only",
                notes=_("Front image only"),
                settings={"cover.image.front.enabled": True, "cover.image.back.enabled": False},
            )
        return CoverPreset(name="img_behind_text_fallback", settings={"cover.image.layer": "behind_text"})

    def _preset_title(self, placement: str) -> CoverPreset:
        if placement == "center":
            return CoverPreset(name="title_centered", settings={"cover.title.position": "center", "cover.title.box.enabled": False})
        if placement == "top":
            return CoverPreset(name="title_top", settings={"cover.title.position": "top", "cover.title.box.enabled": False})
        if placement == "bottom":
            return CoverPreset(name="title_bottom", settings={"cover.title.position": "bottom", "cover.title.box.enabled": False})
        if placement == "box":
            return CoverPreset(name="title_box", settings={"cover.title.position": "center", "cover.title.box.enabled": True, "cover.title.box.opacity": 0.75})
        return CoverPreset(name="title_centered_fallback", settings={"cover.title.position": "center"})

    def _preset_optional(self, opt: Dict[str, bool]) -> CoverPreset:
        return CoverPreset(
            name="optional_elements",
            settings={
                "cover.subtitle.enabled": bool(opt.get("subtitle")),
                "cover.author.enabled": bool(opt.get("author")),
                "cover.backtext.enabled": bool(opt.get("backtext")),
                "cover.isbn.enabled": bool(opt.get("isbn")),
                "cover.border.enabled": bool(opt.get("border")),
            },
        )

    # ---------------------------
    # Preview + Summary
    # ---------------------------

    def _update_preview_for_step(self) -> None:
        sid = self.active_steps[self.step_index]
        if sid == "step2_spine":
            self.preview.highlight_region = "spine"
        elif sid in ("step3_background", "step3a_layering", "step4_title"):
            self.preview.highlight_region = "front"
        elif sid == "step5_optional":
            self.preview.highlight_region = "back"
        else:
            self.preview.highlight_region = "spread"
        self.da_preview.queue_draw()

    def _update_summary(self) -> None:
        d = self.decisions
        opt = d["optional"]

        lines = [
            _("Cover style: {}").format(_("Simple") if d["complexity"] == "simple" else _("Published")),
            _("Spine: {}").format(_("Yes") if d["spine"] else _("No")),
            _("Background: {}").format({
                "white": _("White"),
                "plain": _("Plain color"),
                "one_image": _("One image"),
                "two_images": _("Different front/back images"),
            }.get(d["background"], d["background"])),
        ]

        if "step3a_layering" in self.active_steps and d["background"] in ("one_image", "two_images"):
            lines.append(_("Image layering: {}").format({
                "behind": _("Behind text"),
                "overlay": _("Overlay"),
                "front_only": _("Front only"),
            }.get(d["image_layering"], d["image_layering"])))

        lines.append(_("Title placement: {}").format({
            "center": _("Centered"),
            "top": _("Top"),
            "bottom": _("Bottom"),
            "box": _("Title box"),
        }.get(d["title_placement"], d["title_placement"])))

        if "step5_optional" in self.active_steps:
            enabled = [k for k, v in opt.items() if v]
            lines.append(_("Optional: {}").format(", ".join(enabled) if enabled else _("(none)")))

        lines.append("")
        lines.append(_("Applied presets: {}").format(", ".join(self.preset_stack.names()) or _("(none)")))

        self.l_summary.set_text("\n".join(lines))

    # ---------------------------
    # Button actions
    # ---------------------------

    def go_back(self) -> None:
        if self.step_index <= 0:
            return
        self.step_index -= 1
        self._show_step(self.active_steps[self.step_index])
        self._update_nav()
        self._update_preview_for_step()

    def go_next(self) -> None:
        if self.step_index >= len(self.active_steps) - 1:
            return
        # rebuild active steps in case conditional step changed
        self._rebuild_active_steps()
        current_sid = self.active_steps[self.step_index]
        self._apply_presets_up_to(current_sid)

        self.step_index = min(self.step_index + 1, len(self.active_steps) - 1)
        self._show_step(self.active_steps[self.step_index])

        # ensure summary up-to-date when entering review
        self._apply_presets_up_to(self.active_steps[self.step_index])

        self._update_nav()
        self._update_preview_for_step()

    def finish(self) -> None:
        self._apply_presets_up_to(self.active_steps[-1])
        self.dlg.response(Gtk.ResponseType.OK)

    def open_advanced(self) -> None:
        # Escape hatch stub: in PTXprint this would open existing cover dialogs.
        # We still apply current presets first.
        self._apply_presets_up_to(self.active_steps[self.step_index])
        md = Gtk.MessageDialog(
            transient_for=self.dlg,
            modal=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=_("Advanced settings (stub)"),
        )
        md.format_secondary_text(_("In PTXprint integration, this would open the existing cover dialogs pre-filled with the wizard’s settings."))
        md.run()
        md.destroy()

    # ---------------------------
    # Decision setters (called from signals)
    # ---------------------------

    def set_complexity(self, complexity: str) -> None:
        self.decisions["complexity"] = complexity
        self._rebuild_active_steps()
        self.step_index = 0
        self._show_step(self.active_steps[self.step_index])
        self._apply_presets_up_to("step1_complexity")
        self._update_nav()
        self._update_preview_for_step()

    def set_spine(self, enabled: bool) -> None:
        self.decisions["spine"] = enabled
        self._apply_presets_up_to("step2_spine")
        self._update_preview_for_step()

    def set_background(self, bg: str) -> None:
        self.decisions["background"] = bg
        self._rebuild_active_steps()
        self._apply_presets_up_to("step3_background")
        self._update_nav()
        self._update_preview_for_step()

    def set_layering(self, layering: str) -> None:
        self.decisions["image_layering"] = layering
        self._apply_presets_up_to("step3a_layering")
        self._update_preview_for_step()

    def set_title(self, placement: str) -> None:
        self.decisions["title_placement"] = placement
        self._apply_presets_up_to("step4_title")
        self._update_preview_for_step()

    def set_optional(self, key: str, enabled: bool) -> None:
        self.decisions["optional"][key] = enabled
        self._apply_presets_up_to("step5_optional")
        self._update_preview_for_step()

    # ---------------------------
    # Preview drawing (simple, effective)
    # ---------------------------

    def draw_preview(self, widget: Gtk.DrawingArea, cr) -> bool:
        # White background
        alloc = widget.get_allocation()
        w, h = alloc.width, alloc.height
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, w, h)
        cr.fill()

        # Compute spread rectangles: back | spine | front
        pad = 14
        usable_w = max(10, w - 2 * pad)
        usable_h = max(10, h - 2 * pad)

        # spine width relative
        spine_enabled = bool(self.settings.get("cover.spine.enabled", False))
        spine_w = int(usable_w * (0.10 if spine_enabled else 0.04))
        panel_w = int((usable_w - spine_w) / 2)

        x_back = pad
        x_spine = x_back + panel_w
        x_front = x_spine + spine_w
        y = pad

        # Draw panels
        def draw_panel(x, y, pw, ph, label: str, highlight: bool) -> None:
            # fill light gray
            cr.set_source_rgb(0.95, 0.95, 0.95)
            cr.rectangle(x, y, pw, ph)
            cr.fill()

            # outline
            if highlight:
                cr.set_line_width(3.0)
            else:
                cr.set_line_width(1.0)
            cr.set_source_rgb(0, 0, 0)
            cr.rectangle(x, y, pw, ph)
            cr.stroke()

            # label
            cr.set_source_rgb(0, 0, 0)
            cr.select_font_face("Sans", 0, 0)
            cr.set_font_size(12)
            cr.move_to(x + 8, y + 18)
            cr.show_text(label)

        region = self.preview.highlight_region
        draw_panel(x_back, y, panel_w, usable_h, _("Back"), highlight=(region in ("back", "spread")))
        draw_panel(x_spine, y, spine_w, usable_h, _("Spine"), highlight=(region in ("spine", "spread")))
        draw_panel(x_front, y, panel_w, usable_h, _("Front"), highlight=(region in ("front", "spread")))

        # Tiny status text at bottom
        cr.set_source_rgb(0, 0, 0)
        cr.set_font_size(10)
        status = _("Highlight: {}").format(region)
        cr.move_to(pad, h - 10)
        cr.show_text(status)

        return False


# ============================================================
# App wiring: Glade signals -> controller methods
# ============================================================

class App:
    def __init__(self, glade_path: str) -> None:
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_path)
        self.builder.connect_signals(self)

        self.w_main: Gtk.Window = self.builder.get_object("w_main")
        self.settings = SettingsAdapter()
        self.wiz: Optional[CoverWizardController] = None

        self.w_main.connect("destroy", Gtk.main_quit)
        self.w_main.show_all()

    def on_btn_open_wizard_clicked(self, _btn: Gtk.Button) -> None:
        self.wiz = CoverWizardController(self.builder, self.w_main, self.settings)

        # show dialog
        self.wiz.dlg.show_all()

        # ensure correct step is visible (stack needs this after show_all sometimes)
        self.wiz._show_step(self.wiz.active_steps[self.wiz.step_index])
        self.wiz._update_nav()
        self.wiz._update_preview_for_step()

        resp = self.wiz.dlg.run()
        self.wiz.dlg.hide()

        if resp == Gtk.ResponseType.OK:
            # For prototype visibility: print final settings snapshot
            print("FINAL SETTINGS:", self.settings.snapshot())
        else:
            print("Wizard closed (resp=%s)" % resp)

    # ---------- Nav buttons ----------
    def on_btn_back_clicked(self, _btn: Gtk.Button) -> None:
        if self.wiz:
            self.wiz.go_back()

    def on_btn_next_clicked(self, _btn: Gtk.Button) -> None:
        if self.wiz:
            self.wiz.go_next()

    def on_btn_finish_clicked(self, _btn: Gtk.Button) -> None:
        if self.wiz:
            self.wiz.finish()

    def on_btn_advanced_clicked(self, _btn: Gtk.Button) -> None:
        if self.wiz:
            self.wiz.open_advanced()

    # ---------- Step 1 complexity ----------
    def on_r_complex_simple_toggled(self, rb: Gtk.RadioButton) -> None:
        if self.wiz and rb.get_active():
            self.wiz.set_complexity("simple")

    def on_r_complex_published_toggled(self, rb: Gtk.RadioButton) -> None:
        if self.wiz and rb.get_active():
            self.wiz.set_complexity("published")

    # ---------- Step 2 spine ----------
    def on_r_spine_no_toggled(self, rb: Gtk.RadioButton) -> None:
        if self.wiz and rb.get_active():
            self.wiz.set_spine(False)

    def on_r_spine_yes_toggled(self, rb: Gtk.RadioButton) -> None:
        if self.wiz and rb.get_active():
            self.wiz.set_spine(True)

    # ---------- Step 3 background ----------
    def on_r_bg_white_toggled(self, rb: Gtk.RadioButton) -> None:
        if self.wiz and rb.get_active():
            self.wiz.set_background("white")

    def on_r_bg_plain_toggled(self, rb: Gtk.RadioButton) -> None:
        if self.wiz and rb.get_active():
            self.wiz.set_background("plain")

    def on_r_bg_oneimg_toggled(self, rb: Gtk.RadioButton) -> None:
        if self.wiz and rb.get_active():
            self.wiz.set_background("one_image")

    def on_r_bg_twoimg_toggled(self, rb: Gtk.RadioButton) -> None:
        if self.wiz and rb.get_active():
            self.wiz.set_background("two_images")

    # ---------- Step 3a layering ----------
    def on_r_img_behind_toggled(self, rb: Gtk.RadioButton) -> None:
        if self.wiz and rb.get_active():
            self.wiz.set_layering("behind")

    def on_r_img_overlay_toggled(self, rb: Gtk.RadioButton) -> None:
        if self.wiz and rb.get_active():
            self.wiz.set_layering("overlay")

    def on_r_img_frontonly_toggled(self, rb: Gtk.RadioButton) -> None:
        if self.wiz and rb.get_active():
            self.wiz.set_layering("front_only")

    # ---------- Step 4 title ----------
    def on_r_title_center_toggled(self, rb: Gtk.RadioButton) -> None:
        if self.wiz and rb.get_active():
            self.wiz.set_title("center")

    def on_r_title_top_toggled(self, rb: Gtk.RadioButton) -> None:
        if self.wiz and rb.get_active():
            self.wiz.set_title("top")

    def on_r_title_bottom_toggled(self, rb: Gtk.RadioButton) -> None:
        if self.wiz and rb.get_active():
            self.wiz.set_title("bottom")

    def on_r_title_box_toggled(self, rb: Gtk.RadioButton) -> None:
        if self.wiz and rb.get_active():
            self.wiz.set_title("box")

    # ---------- Step 5 optional ----------
    def on_c_subtitle_toggled(self, cb: Gtk.CheckButton) -> None:
        if self.wiz:
            enabled = cb.get_active()
            self.wiz.rv_subtitle.set_reveal_child(enabled)
            self.wiz.set_optional("subtitle", enabled)

    def on_c_author_toggled(self, cb: Gtk.CheckButton) -> None:
        if self.wiz:
            enabled = cb.get_active()
            self.wiz.rv_author.set_reveal_child(enabled)
            self.wiz.set_optional("author", enabled)

    def on_c_backtext_toggled(self, cb: Gtk.CheckButton) -> None:
        if self.wiz:
            enabled = cb.get_active()
            self.wiz.rv_backtext.set_reveal_child(enabled)
            self.wiz.set_optional("backtext", enabled)

    def on_c_isbn_toggled(self, cb: Gtk.CheckButton) -> None:
        if self.wiz:
            enabled = cb.get_active()
            self.wiz.rv_isbn.set_reveal_child(enabled)
            self.wiz.set_optional("isbn", enabled)

    def on_c_border_toggled(self, cb: Gtk.CheckButton) -> None:
        if self.wiz:
            enabled = cb.get_active()
            self.wiz.rv_border.set_reveal_child(enabled)
            self.wiz.set_optional("border", enabled)

    # ---------- Preview draw ----------
    def on_da_preview_draw(self, widget: Gtk.DrawingArea, cr) -> bool:
        if self.wiz:
            return self.wiz.draw_preview(widget, cr)
        return False


def main() -> None:
    import sys, os
    glade_path = os.path.join(os.path.dirname(__file__), "coverwizard_prototype.glade")
    if len(sys.argv) > 1:
        glade_path = sys.argv[1]
    App(glade_path)
    Gtk.main()


if __name__ == "__main__":
    main()
