#!/usr/bin/env python3
"""
coverwizard.py — PTXprint Cover Wizard
[PTXprint integration] markers indicate where fields map to project config.
"""

import os
import sys
import json
import math
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf
import cairo

from ptxprint.utils import coltoonemax, coltotex
from PIL import Image


# ─────────────────────────────────────────────────────────────────────────────
# State
# ─────────────────────────────────────────────────────────────────────────────

# Standard paper weight → thickness lookup (µm per sheet, approximate)
# Based on typical uncoated offset paper densities.
GSM_TO_UM = {
    60: 82, 70: 95, 75: 100, 80: 106, 90: 118, 100: 130,
    110: 143, 120: 156, 130: 169, 140: 182, 150: 195,
    160: 208, 170: 221, 180: 234, 200: 260, 250: 325, 300: 390,
}

def gsmToUm(gsm: float) -> float:
    """Approximate paper thickness in µm from gsm."""
    keys = sorted(GSM_TO_UM.keys())
    if gsm <= keys[0]:  return GSM_TO_UM[keys[0]]
    if gsm >= keys[-1]: return GSM_TO_UM[keys[-1]]
    # linear interpolation between nearest two entries
    for i in range(len(keys)-1):
        if keys[i] <= gsm <= keys[i+1]:
            lo, hi = keys[i], keys[i+1]
            t = (gsm - lo) / (hi - lo)
            return GSM_TO_UM[lo] + t * (GSM_TO_UM[hi] - GSM_TO_UM[lo])
    return 100.0

def umToGsm(um: float) -> float:
    """Reverse: derive gsm from thickness µm."""
    # Invert the table
    pairs = sorted((v, k) for k, v in GSM_TO_UM.items())
    if um <= pairs[0][0]:  return pairs[0][1]
    if um >= pairs[-1][0]: return pairs[-1][1]
    for i in range(len(pairs)-1):
        if pairs[i][0] <= um <= pairs[i+1][0]:
            lo_um, lo_g = pairs[i]
            hi_um, hi_g = pairs[i+1]
            t = (um - lo_um) / (hi_um - lo_um)
            return lo_g + t * (hi_g - lo_g)
    return 80.0


class WorkingCoverState:
    modelmap = {
        "": "coverbleed",
        "spine_width_computed_mm": "spinewidth",
        "": "coverartbleed",
        "": "spineoverlapback",
        "": "spineoverlapfront"
    }

    def __init__(self):
        # Step 1
        self.spine_enabled: bool = False
        self.pagecount: int = 0
        self.binding_type: str = "paperback"
        self.rtl_binding: bool = False
        self.spine_width_mode: str = "auto"    # auto | manual
        self.paper_gsm: float = 80.0
        self.paper_thickness_um: float = 106.0  # matches 80 gsm
        self.spine_width_mm: float = 0.0        # manual override
        self.spine_width_computed_mm: float = 0.0

        # Step 2
        self.coverage_pattern: str = "none"
        self.img_primary_path: str = ""
        self.img_primary_fit: str = "stretch"
        self.img_primary_opacity: int = 100
        self.img_secondary_path: str = ""
        self.img_secondary_fit: str = "stretch"
        self.img_secondary_opacity: int = 100
        # decorative border
        self.border_enabled: bool = False
        self.border_style: str = "Han1"
        self.border_color: str = "#000000"
        
        # Step 3
        self.bg_mode: str = "white"
        self.bg_color: str = "#4a90d9"
        self.bg_opacity: int = 100

        # Step 4
        self.title: str = ""
        self.title_position_pct: int = 25        # near top-quarter by default
        self.title_in_box: bool = False
        self.title_color: str = "#0d0d20"
        self.title_size_pct: int = 100

        self.subtitle_enabled: bool = False
        self.subtitle: str = ""
        self.subtitle_position_pct: int = 38
        self.subtitle_color: str = "#1a1a30"
        self.subtitle_size_pct: int = 80

        self.langname_enabled: bool = False
        self.langname: str = ""
        self.langname_position_pct: int = 80     # near bottom by default
        self.langname_color: str = "#1a1a30"
        self.langname_size_pct: int = 75

        self.fgimage_enabled: bool = False
        self.fgimage_path: str = ""
        self.fgimage_position_pct: int = 55      # centre-lower
        self.fgimage_bg_trans: int = 100  # 0=fully transparent, 100=opaque

        # Step 5
        # spine text styling
        self.spine_text_size_pct: int = 150
        self.spine_text_color: str = "#0d0d20"
        self.spine_text_vpos_pct: int = 50      # % down the spine
        self.spine_title: bool = True
        self.spine_subtitle: bool = False
        self.spine_langname: bool = False
        self.spine_orientation: str = "v_ttb"
        # publisher on spine
        self.spine_publisher_enabled: bool = False
        self.spine_publisher_size_pct: int = 75
        self.spine_publisher_vpos_pct: int = 85
        self.spine_publisher_color: str = "#0d0d20"
        self.spine_publisher: str = ""
        self.pub_orientation: str = "v_ttb"
        self.spine_pub_logo_enabled: bool = False
        self.spine_pub_logo_path: str = ""
        self.spine_pub_logo_scale: int = 70
        self.spine_pub_logo_vpos_pct: int = 90
        self.spine_pub_logo_rotation: str = "none"   # none | cw | ccw
        
        # Step 6
        self.backtext_enabled: bool = False
        self.backtext: str = ""
        self.logo_enabled: bool = False
        self.logo_path: str = ""
        self.logo_scale: int = 100
        self.logo_hpos: str = "centre"  # inner | centre | outer
        self.logo_vpos_pct: int = 90    # 0=top, 100=bottom (vertical position %)
        self.isbn_enabled: bool = False
        self.isbn: str = ""
        self.isbn_hpos: str = "inner"   # inner | centre | outer

    def saveConfig(self, config):
        for k, v in vars(self).items():
            if isinstance(v, (int, str)):
                config.set("coverwiz", k, str(v))
            elif isinstance(v, bool):
                config.set("coverwiz", k, "true" if v else "false")

    def updateView(self, view):
        def setfront(k, v, all=False):
            view.styleEditor.setval("cat:coverwhole|esb" if all else "cat:coverfront|esb", k, v)
        if self.border_enabled:
            setfront("BorderStyle", "ornaments")
            setfront("Border", "All")
            setfront("BorderRef", self.border_style)
            setfront("BorderColor", self.border_color)
        else:
            setfront("Border", None)
            for a in "Style Ref Color".split():
                setfront("Border"+a, "")
        setfront("BgColor", coltotex(coltoonemax(self.bg_color)), all=True)
        setfront("Alpha", self.bg_opacity / 100, all=True)
        for d in (True, False):
            for c in ("BgImage", "BgImageScale", "BgImageScaleTo", "BgImageAlpha"):
                setfront(c, None, all=d)
        if self.img_primary_path:
            wrap_all = self.coverage_pattern=="wrap_all"
            setfront("BgImage", self.img_primary_path, all=wrap_all)
            setfront("BgImageScaleTo", "colbleed", all=wrap_all)
            setfront("BgImageScale", "1x1" if self.img_primary_fit == "stretch" else "1", all=wrap_all)
            setfront("BgImageAlpha", self.img_primary_alpha / 100, all=wrap_all)
            setfront("BgImageAlpha", 1 - (self.img_primary_alpha / 100), all=not wrap_all)
        for m in (('mt1', 'title'), ('mt2', 'subtitle')):
            sz = view.styleEditor.getval(m[0], 'FontSize', 1.0)
            view.styleEditor.setval(f"cat:coverfront|{m[0]}", 'FontSize', sz * getattr(self, m[1]+"_size_pct") / 100)
            view.styleEditor.setval(f"cat:coverfront|{m[0]}", 'Color', coltotext(coltoonemax(getattr(self, m[1]+"_color"))))
            view.styleEditor.setval(f"cat:coverspine|{m[0]}", 'FontSize', sz * 0.65 * getattr(self, "spine_text_size_pct") / 100)
            view.styleEditor.setval(f"cat:coverspine|{m[0]}", 'Color', coltotext(coltoonemax(getattr(self, "spine_text_color"))))
        view.setvar('maintitle', self.title)
        if self.subtitle_enabled:
            view.setvar('subtitle', self.subtitle)
        if self.langname_enabled:
            view.setvar('languagename', self.langname)
        if self.isbn_enabled:
            view.setvar('isbn', self.isbn)
        self.createCoverPeriphs(view)

    def getBorderVal(self, view, mkr, vh, key):
        val = view.styleEditor.getval(mkr, f"{key}{vh}Padding", None)
        if val is None:
            val = view.styleEditor.getval(mkr, f"{key}Padding", 0)
        return val

    def get_image_height(self, path, pht, pwd):
        im = Image.open(path)
        scale = 1
        if scale * im.size[0] > pwd:
            scale *= pwd / im.size[0]
        if scale * im.size[1] > pht:
            scale = pht / im.size[1]
        return scale * im.size[1]

    def createCoverPeriphs(self, view):
        pwidth, pheight = view.calcPageSize()
        linefactor = float(view.get("s_linespacing")) * 72 / 25.4
        for a in ('front', 'spine', 'back'):
            res = []
            res.append(fr'\periph {a}|id="cover{a}"')
            if a == 'front':
                bits = []
                vremove = 0
                hremove = 0
                for p in ("Box", "Border"):
                    for v in ("T", "B"):
                        vremove += self.getBorderVal(view, f"cat:cover{a}|esb", v, p)
                    for v in ("L", "R"):
                        hremove += self.getBorderVal(view, f"cat:cover{a}|esb", v, p)
                theight = pheight - vremove
                twidth = pwidth - hremove
                title_height = view.styleEditor.getval(f"cat:cover{a}|mt1", "LineSpacing", 1.0)
                bits.append(theight * self.title_position_pct / 100, title_height * linefactor, r"\mt1 \zvar|maintitle\*")
                if self.subtitle_enabled:
                    subtitle_height = view.styleEditor.getval(f"cat:cover{a}|mt2", "LineSpacing", 1.0)
                    bits.append(theight * self.subtitle_position_pct / 100, subtitle_height * linefactor, r"\mt2 \zvar|subtitle\*")
                if self.langname_enabled:
                    langname_height = view.styleEditor.getval(f"cat:cover{a}|mt3", "LineSpacing", 1.0)
                    bits.append(theight * self.langname_position_pct / 100, langname_height * linefactor, r"\mt3 \zvar|languagename\*")
                if self.fgimage_enabled:
                    fgimage_height = self.get_image_height(self.fgimage_path, twidth, theight)
                    bits.append(theight * self.fgimage_position_pct / 100, fgimage_height, fr'\fig|src="{self.fgimage_path}" size="col", pgpos="pc"\fig*')
                basepos = 0
                for b in sorted(bits):
                    if b[0] > basepos:
                        res.append(fr"\zgap|{b[0]-basepos}mm\*")
                        basepos = b[0] + b[1]
                    else:
                        basepos += b[1]
                    res.append(b[2])
                res.append(r"\vfill")
                res.append(r"\endgraf")
            elif a == 'spine':
                theight = self.spine_width_computed_mm
                text_height = view.styleEditor.getval(f"cat:cover{a}|mt1", "LineSpacing", 1.0)
                res.append(rf"\mt2 \zvar|maintitle\* ~~-~~ \zvar|subtitle\*")
            elif a == "back":
                back_height = view.styleEditor.getval(f"cat:cover{a}|m", "LineSpacing", 1.0)
                positions = {"inner": "pi", "center": "pc", "outer": "po"}
                res.append(r"\zgap|1in\*")
                res.append(rf"\m {self.backtext}")
                if self.logo_enabled:
                    res.append(rf"\zgap|{self.logo_vpos_pct / 100 * pheight}\*")
                    res.append(rf'\fig|src="{self.logo_path}" pgpos="{positions[self.logo_hpos]}" size="col" scale="self.logo_scale / 100"\fig*')
                res.append(r"\vfill")
                if self.isbn_enabled:
                    res.append(r'\ztruetext')
                    res.append(fr'\esb\cat ISBNbox\cat*\pc \zISBNbarcode|var="isbn" pgpos="positions[self.isbn_hpos]" height="medium"\*\esbe')
                    res.append(r'\zgap 10pt\*')
                    res.append(r'\ztruetext*')
            view.periphs['cover'+a] = "\n".join(res)

    def computeSpineWidth(self):
        if self.spine_width_mode == "manual":
            self.spine_width_computed_mm = max(0.0, self.spine_width_mm)
        else:
            pages = max(0, self.pagecount)
            thickness_mm = self.paper_thickness_um / 1000.0
            self.spine_width_computed_mm = (pages / 2.0) * thickness_mm

    def toDict(self):
        return {k: v for k, v in self.__dict__.items() if isinstance(v, (int, bool, str))}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def hexToRgb(h: str):
    h = h.lstrip("#")
    if len(h) != 6:
        return (0.05, 0.05, 0.15)
    return (int(h[0:2], 16)/255, int(h[2:4], 16)/255, int(h[4:6], 16)/255)

def gdkColorToHex(rgba: Gdk.RGBA) -> str:
    return "#{:02x}{:02x}{:02x}".format(
        int(rgba.red*255), int(rgba.green*255), int(rgba.blue*255))

def makeLabel(text, bold=False, dim=False, wrap=True, xalign=0.0):
    lbl = Gtk.Label()
    lbl.set_xalign(xalign)
    lbl.set_line_wrap(wrap)
    if bold:
        lbl.set_markup(f"<b>{text}</b>")
    else:
        lbl.set_text(text)
    if dim:
        lbl.get_style_context().add_class("dim-label")
    lbl.show()
    return lbl

def makeHBox(spacing=8):
    b = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=spacing)
    b.show()
    return b

def makeVBox(spacing=6):
    b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=spacing)
    b.show()
    return b

def makeCheck(label):
    c = Gtk.CheckButton(label=label)
    c.show()
    return c

def makeRadio(label, group=None):
    r = Gtk.RadioButton.new_with_label_from_widget(group, label)
    r.show()
    return r

def makeEntry(placeholder="", width=-1):
    e = Gtk.Entry()
    e.set_placeholder_text(placeholder)
    if width > 0:
        e.set_width_chars(width)
    e.set_valign(Gtk.Align.CENTER)
    e.show()
    return e

def makeButton(label):
    b = Gtk.Button(label=label)
    b.set_valign(Gtk.Align.CENTER)
    b.show()
    return b

def makeColorButton(hexColor="#000000"):
    cb = Gtk.ColorButton()
    rgba = Gdk.RGBA()
    rgba.parse(hexColor)
    cb.set_rgba(rgba)
    cb.set_valign(Gtk.Align.CENTER)
    cb.show()
    return cb

def makeHScale(val, lo, hi, digits=0):
    adj = Gtk.Adjustment(value=val, lower=lo, upper=hi,
                         step_increment=1, page_increment=10)
    s = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj)
    s.set_draw_value(True)
    s.set_value_pos(Gtk.PositionType.RIGHT)
    s.set_digits(digits)
    s.set_hexpand(True)
    s.set_valign(Gtk.Align.CENTER)
    s.show()
    return s

def makeVScale(val, lo, hi):
    """Vertical slider: 0% at top, 100% at bottom."""
    adj = Gtk.Adjustment(value=val, lower=lo, upper=hi,
                         step_increment=1, page_increment=5)
    s = Gtk.Scale(orientation=Gtk.Orientation.VERTICAL, adjustment=adj)
    s.set_draw_value(True)
    s.set_value_pos(Gtk.PositionType.RIGHT)
    s.set_digits(0)
    s.set_vexpand(False)
    s.set_valign(Gtk.Align.FILL)
    s.set_size_request(60, 80)
    s.show()
    return s

def makeCombo(items):
    cb = Gtk.ComboBoxText()
    for item_id, item_label in items:
        cb.append(item_id, item_label)
    cb.set_active(0)
    cb.set_valign(Gtk.Align.CENTER)
    cb.set_hexpand(True)
    cb.show()
    return cb

def makeRevealer(child_widget, transition=Gtk.RevealerTransitionType.SLIDE_DOWN):
    rv = Gtk.Revealer()
    rv.set_transition_type(transition)
    rv.set_reveal_child(False)
    rv.add(child_widget)
    rv.show()
    return rv

def makeFrame(label_text=None, child=None, margin_start=0):
    fr = Gtk.Frame()
    if label_text:
        fr.set_label(label_text)
    if margin_start:
        fr.set_margin_start(margin_start)
    if child:
        fr.add(child)
    fr.show()
    return fr

def makeSpinner(val, lo, hi, step=1.0, digits=0):
    adj = Gtk.Adjustment(value=val, lower=lo, upper=hi,
                         step_increment=step, page_increment=step*10)
    sp = Gtk.SpinButton(adjustment=adj, climb_rate=1.0, digits=digits)
    sp.set_valign(Gtk.Align.CENTER)
    sp.set_numeric(True)
    sp.show()
    return sp

def openImageChooser(parent, title="Choose image"):
    dlg = Gtk.FileChooserDialog(title=title, parent=parent,
                                action=Gtk.FileChooserAction.OPEN)
    dlg.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OPEN,   Gtk.ResponseType.OK)
    ff = Gtk.FileFilter()
    ff.set_name("Image files")
    for p in ("*.png","*.jpg","*.jpeg","*.svg","*.tif","*.tiff","*.bmp"):
        ff.add_pattern(p)
    dlg.add_filter(ff)
    path = ""
    if dlg.run() == Gtk.ResponseType.OK:
        path = dlg.get_filename() or ""
    dlg.destroy()
    return path

def wrapText(text, maxChars):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        if not cur:
            cur = word
        elif len(cur) + 1 + len(word) <= maxChars:
            cur += " " + word
        else:
            lines.append(cur); cur = word
    if cur:
        lines.append(cur)
    return lines or [""]


# ─────────────────────────────────────────────────────────────────────────────
# Controller
# ─────────────────────────────────────────────────────────────────────────────

class CoverWizardApp:

    STEPS_NO_SPINE   = ["pg_step1_spine","pg_step2_coverage","pg_step3_background",
                        "pg_step4_front","pg_step6_back","pg_step7_review"]
    STEPS_WITH_SPINE = ["pg_step1_spine","pg_step2_coverage","pg_step3_background",
                        "pg_step4_front","pg_step5_spine_content","pg_step6_back","pg_step7_review"]
    FIT_ITEMS = [
        ("stretch", "Stretch / Shrink"),
        ("crop_centre", "Crop Centre"),
        ("crop_top", "Crop Top"),
        ("crop_bottom", "Crop Bottom"),
        ("crop_left", "Crop Left"),
        ("crop_right", "Crop Right")
    ]

    def __init__(self):
        self.state = WorkingCoverState()
        self._pixbufCache = {}

        # Guard re-entrant spinner updates
        self._updating_spinners = False

        gladePath = os.path.join(os.path.dirname(__file__), "coverwizard.glade")
        builder = Gtk.Builder()
        try:
            builder.add_from_file(gladePath)
        except Exception as exc:
            dlg = Gtk.MessageDialog(message_type=Gtk.MessageType.ERROR,
                                    buttons=Gtk.ButtonsType.CLOSE,
                                    text=f"Cannot load UI:\n{gladePath}\n\n{exc}")
            dlg.run(); dlg.destroy(); sys.exit(1)

        builder.connect_signals(self)

        def w(n): return builder.get_object(n)

        # Hide old static header labels and separator
        for widget_id in ("l_header_title", "l_header_sub", "l_progress", "sep_header"):
            widget = w(widget_id)
            widget.hide()
            widget.set_no_show_all(True)

        self.window     = w("w_coverwizard")
        self.st_steps   = w("st_steps")
        self.da_preview = w("da_preview")
        self.btn_back   = w("btn_back")
        self.btn_next   = w("btn_next")
        self.btn_finish = w("btn_finish")

        self._pages = {
            1: w("pg_step1_spine"),
            2: w("pg_step2_coverage"),
            3: w("pg_step3_background"),
            4: w("pg_step4_front"),
            5: w("pg_step5_spine_content"),
            6: w("pg_step6_back"),
            7: w("pg_step7_review"),
        }

        self._buildPage1()
        self._buildPage2()
        self._buildPage3()
        self._buildPage4()
        self._buildPage5()
        self._buildPage6()
        self._buildPage7()

        self._stepIndex = 0
        self._updateStepList()
        self._goToStep(0)
        self.window.show_all()

    # ── Internal helpers ──────────────────────────────────────────────

    def _pack(self, page_num, widget, expand=False, fill=True, padding=0):
        self._pages[page_num].pack_start(widget, expand, fill, padding)

    def _refresh(self):
        total   = len(self._steps)
        self.btn_back.set_sensitive(self._stepIndex > 0)
        self.btn_next.set_sensitive(self._stepIndex < total - 1)
        onLast  = self._stepIndex == total - 1
        titleOk = bool(self.state.title.strip())
        self.btn_finish.set_sensitive(onLast and titleOk)
        if self._steps[self._stepIndex] == "pg_step4_front" and not titleOk:
            self.btn_next.set_sensitive(False)
        self._updateCoverageWidgets()
        self._updateSpineHorizVisibility()
        self._updateSummary()
        self.da_preview.queue_draw()

    def _updateStepList(self):
        self._steps = list(self.STEPS_WITH_SPINE if self.state.spine_enabled
                           else self.STEPS_NO_SPINE)

    def _goToStep(self, idx):
        self._stepIndex = max(0, min(idx, len(self._steps)-1))
        self.st_steps.set_visible_child_name(self._steps[self._stepIndex])
        self._refresh()

    def _updateCoverageWidgets(self):
        spine = self.state.spine_enabled
        self._r_cov_wrap_all.set_label(
            "Wrap all (one image across front + spine + back)" if spine
            else "Wrap all (one image across front + back)")
        for r in (self._r_cov_front_spine, self._r_cov_back_spine):
            r.set_visible(spine); r.set_sensitive(spine)
        if not spine and self.state.coverage_pattern in ("front_spine","back_spine"):
            self.state.coverage_pattern = "wrap_all"
            self._r_cov_wrap_all.set_active(True)
        noImg = self.state.coverage_pattern == "none"
        self._rv_img_primary.set_reveal_child(not noImg)
        isSep = self.state.coverage_pattern == "front_back_separate"
        self._rv_img_secondary.set_reveal_child(isSep)

    def _updateSpineHorizVisibility(self):
        """Reset horizontal orientation if page count drops below 500."""
        if self.state.pagecount < 500 and self.state.spine_orientation == "horiz":
            self.state.spine_orientation = "v_ttb"
            self._cb_spine_orientation.set_active(0)
            
    def _updateSummary(self):
        s = self.state
        s.computeSpineWidth()
        lines = []

        # ── Page 1: Book & spine ─────────────────────────────────────
        if s.spine_enabled:
            spine_mm = f"{s.spine_width_computed_mm:.1f} mm"
            binding  = "hardcover" if s.binding_type == "hardcover" else "paperback"
            lines.append(f"Book:         {s.pagecount} pages · {binding} with spine ({spine_mm})")
        else:
            lines.append(f"Book:         {s.pagecount} pages · no spine")
        if s.rtl_binding:
            lines.append(f"              RTL binding")

        # ── Page 2: Coverage & images ────────────────────────────────
        cov_labels = {
            "wrap_all":            "full-spread image",
            "front_only":          "front image only",
            "front_spine":         "front + spine image",
            "back_only":           "back image only",
            "back_spine":          "back + spine image",
            "front_back_separate": "separate front & back images",
            "none":                "no cover image",
        }
        cov = cov_labels.get(s.coverage_pattern, s.coverage_pattern)
        img_parts = [cov]
        if s.coverage_pattern != "none":
            if s.img_primary_path:
                img_parts.append(os.path.basename(s.img_primary_path))
            if s.img_primary_opacity < 100:
                img_parts.append(f"{s.img_primary_opacity}% opacity")
            if s.coverage_pattern == "front_back_separate" and s.img_secondary_path:
                img_parts.append(f"back: {os.path.basename(s.img_secondary_path)}")
        if s.border_enabled:
            img_parts.append(f"border: {s.border_style}")
        lines.append(f"Images:       {' · '.join(img_parts)}")

        # ── Page 3: Background ───────────────────────────────────────
        if s.bg_mode == "solid":
            op_str = f" {s.bg_opacity}% opacity" if s.bg_opacity < 100 else ""
            lines.append(f"Background:   solid colour {s.bg_color}{op_str}")
        elif s.bg_mode == "gradient":
            lines.append(f"Background:   gradient")
        # white = default, skip

        # ── Page 4: Front cover text ─────────────────────────────────
        if s.title:
            title_str = f'"{s.title}"'
            attrs = []
            if s.title_size_pct != 100:
                attrs.append(f"{s.title_size_pct}%")
            if s.title_in_box:
                attrs.append("boxed")
            if attrs:
                title_str += f" ({', '.join(attrs)})"
            lines.append(f"Title:        {title_str}  [pos {s.title_position_pct}%]")
        else:
            lines.append(f"Title:        (not set)")

        if s.subtitle_enabled and s.subtitle:
            sub_attrs = []
            if s.subtitle_size_pct != 80:
                sub_attrs.append(f"{s.subtitle_size_pct}%")
            sub_str = f'"{s.subtitle}"'
            if sub_attrs:
                sub_str += f" ({', '.join(sub_attrs)})"
            lines.append(f"Subtitle:     {sub_str}  [pos {s.subtitle_position_pct}%]")

        if s.langname_enabled and s.langname:
            lines.append(f"Language:     \"{s.langname}\"  [pos {s.langname_position_pct}%]")

        if s.fgimage_enabled:
            fg_str = os.path.basename(s.fgimage_path) if s.fgimage_path else "(no file)"
            lines.append(f"Fg image:     {fg_str}  [pos {s.fgimage_position_pct}%]")

        # ── Page 5: Spine text (only if spine exists) ────────────────
        if s.spine_enabled:
            spine_parts = []
            if s.spine_title:    spine_parts.append("title")
            if s.spine_subtitle and s.subtitle_enabled: spine_parts.append("subtitle")
            if s.spine_langname: spine_parts.append("language")
            orient_labels = {"v_ttb": "↓", "v_btt": "↑", "horiz": "→"}
            orient = orient_labels.get(s.spine_orientation, s.spine_orientation)
            if spine_parts:
                spine_str = ", ".join(spine_parts)
                size_str = f" {s.spine_text_size_pct}%" if s.spine_text_size_pct != 100 else ""
                lines.append(f"Spine text:   {spine_str}{size_str} {orient}  "
                             f"[pos {s.spine_text_vpos_pct}%]")
            else:
                lines.append(f"Spine text:   (none selected)")

            if s.spine_publisher_enabled:
                pub_parts = []
                if s.spine_publisher.strip():
                    pub_parts.append(f'"{s.spine_publisher.strip()}"')
                if s.spine_pub_logo_enabled:
                    logo_name = os.path.basename(s.spine_pub_logo_path) \
                                if s.spine_pub_logo_path else "(no file)"
                    rot = "" if s.spine_pub_logo_rotation == "none" \
                          else f" {s.spine_pub_logo_rotation}"
                    pub_parts.append(f"logo: {logo_name}{rot}")
                if pub_parts:
                    lines.append(f"Publisher:    {' · '.join(pub_parts)}")

        # ── Page 6: Back cover ───────────────────────────────────────
        back_parts = []
        if s.backtext_enabled:
            snippet = s.backtext.strip()[:35]
            if len(s.backtext.strip()) > 35:
                snippet += "…"
            back_parts.append(f'text: "{snippet}"' if snippet else "text (empty)")
        if s.isbn_enabled:
            isbn_str = s.isbn if s.isbn else "(no number)"
            back_parts.append(f"ISBN: {isbn_str}")
        if s.logo_enabled:
            logo_name = os.path.basename(s.logo_path) if s.logo_path else "(no file)"
            logo_attrs = []
            if s.logo_scale != 100:
                logo_attrs.append(f"{s.logo_scale}%")
            if s.logo_hpos != "centre":
                logo_attrs.append(s.logo_hpos)
            logo_str = logo_name
            if logo_attrs:
                logo_str += f" ({', '.join(logo_attrs)})"
            back_parts.append(f"logo: {logo_str}")
        if back_parts:
            lines.append(f"Back cover:   {' · '.join(back_parts)}")
        else:
            lines.append(f"Back cover:   (nothing added)")

        self._l_summary.set_text("\n".join(lines))

    # ── Pixbuf cache ──────────────────────────────────────────────────

    def _loadPixbuf(self, path):
        if not path or not os.path.isfile(path): return None
        if path in self._pixbufCache: return self._pixbufCache[path]
        try:
            pb = GdkPixbuf.Pixbuf.new_from_file(path)
            self._pixbufCache[path] = pb
            return pb
        except Exception:
            return None

    # ─────────────────────────────────────────────────────────────────
    # Page 1 builder
    # ─────────────────────────────────────────────────────────────────

    def _buildPage1(self):
        p = 1
        self._pack(p, makeLabel("Step 1 — Book and Spine Setup", bold=True))
        self._pack(p, makeLabel(
            "Set the page count and whether this book has a spine. "
            "If it has a spine, configure the binding type and let the wizard "
            "calculate the spine width from paper weight, or enter it manually.",
            dim=True))

        # Page count
        row = makeHBox()
        row.pack_start(makeLabel("Approximate page count:"), False, False, 0)
        self._t_pagecount = makeEntry("0", width=6)
        self._t_pagecount.set_text("0")
        self._t_pagecount.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self._t_pagecount.connect("changed", self.onPagecountChanged)
        row.pack_start(self._t_pagecount, False, False, 0)
        self._pack(p, row)
        self._pack(p, makeLabel("Typically spine text is only used at ~80+ pages.", dim=True))

        # Spine yes/no
        self._r_spine_no = makeRadio("No (thin booklet / under ~80 pages)")
        self._r_spine_no.set_active(True)
        self._r_spine_no.connect("toggled", self.onSpineToggled)
        self._pack(p, self._r_spine_no)
        self._r_spine_yes = makeRadio("Yes (printed book with spine)", group=self._r_spine_no)
        self._r_spine_yes.connect("toggled", self.onSpineToggled)
        self._pack(p, self._r_spine_yes)

        # ── Content revealed when spine enabled ───────────────────────
        spine_inner = makeVBox(8)
        spine_inner.set_margin_start(12)

        # Binding type
        sep_bt = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep_bt.show()
        spine_inner.pack_start(sep_bt, False, False, 0)
        spine_inner.pack_start(makeLabel("Binding type:", bold=True), False, False, 0)
        self._r_binding_pb = makeRadio("Paperback (same size as paper)")
        self._r_binding_pb.set_active(True)
        self._r_binding_pb.connect("toggled", self.onBindingTypeToggled)
        spine_inner.pack_start(self._r_binding_pb, False, False, 0)
        self._r_binding_hc = makeRadio(
            "Hardcover (cover extends beyond paper and wraps)", group=self._r_binding_pb)
        self._r_binding_hc.connect("toggled", self.onBindingTypeToggled)
        spine_inner.pack_start(self._r_binding_hc, False, False, 0)

        # Spine width
        sep_sw = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep_sw.show()
        spine_inner.pack_start(sep_sw, False, False, 0)
        spine_inner.pack_start(makeLabel("Spine width:", bold=True), False, False, 0)

        sw_mode_row = makeHBox(16)
        self._r_sw_auto   = makeRadio("Automatic")
        self._r_sw_auto.set_active(True)
        self._r_sw_auto.connect("toggled", self.onSpineWidthModeToggled)
        self._r_sw_manual = makeRadio("Manual", group=self._r_sw_auto)
        self._r_sw_manual.connect("toggled", self.onSpineWidthModeToggled)
        sw_mode_row.pack_start(self._r_sw_auto,   False, False, 0)
        sw_mode_row.pack_start(self._r_sw_manual, False, False, 0)
        spine_inner.pack_start(sw_mode_row, False, False, 0)

        # Auto sub-panel: both spinners always visible; each updates the other
        auto_box = makeVBox(4)
        auto_box.set_margin_start(12)

        row_gsm = makeHBox()
        row_gsm.pack_start(makeLabel("Paper weight (gsm):"), False, False, 0)
        self._sp_gsm = makeSpinner(80, 40, 400, 1.0, 0)
        self._sp_gsm.connect("value-changed", self.onGsmChanged)
        row_gsm.pack_start(self._sp_gsm, False, False, 8)
        auto_box.pack_start(row_gsm, False, False, 0)

        row_um = makeHBox()
        row_um.pack_start(makeLabel("Paper thickness (µm):"), False, False, 0)
        self._sp_um = makeSpinner(106, 50, 600, 1.0, 0)
        self._sp_um.connect("value-changed", self.onThicknessChanged)
        row_um.pack_start(self._sp_um, False, False, 8)
        auto_box.pack_start(row_um, False, False, 0)

        self._l_spine_computed = makeLabel("Computed spine: 0.0 mm")
        self._l_spine_computed.get_style_context().add_class("dim-label")
        auto_box.pack_start(self._l_spine_computed, False, False, 0)
        self._rv_sw_auto = makeRevealer(auto_box)
        self._rv_sw_auto.set_reveal_child(True)
        spine_inner.pack_start(self._rv_sw_auto, False, False, 0)

        # Manual sub-panel
        manual_box = makeHBox()
        manual_box.set_margin_start(12)
        manual_box.pack_start(makeLabel("Spine width (mm):"), False, False, 0)
        self._sp_spine_mm = makeSpinner(0, 0, 100, 0.5, 2)
        self._sp_spine_mm.set_digits(1)
        self._sp_spine_mm.connect("value-changed", self.onSpineMmChanged)
        manual_box.pack_start(self._sp_spine_mm, False, False, 8)
        self._rv_sw_manual = makeRevealer(manual_box)
        spine_inner.pack_start(self._rv_sw_manual, False, False, 0)

        self._rv_binding_type = makeRevealer(spine_inner)
        self._pack(p, self._rv_binding_type)

        # Separator before RTL
        sep2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep2.set_margin_top(4); sep2.set_margin_bottom(4); sep2.show()
        self._pack(p, sep2)

        # RTL
        self._c_rtl = makeCheck("This book uses right-to-left (RTL) binding")
        self._c_rtl.set_tooltip_text(
            "RTL scripts (Arabic, Hebrew, Urdu, etc.) typically have "
            "the binding on the right side of the cover.")
        self._c_rtl.connect("toggled", self.onRTLBindingToggled)
        self._pack(p, self._c_rtl)

    # ─────────────────────────────────────────────────────────────────
    # Page 2 builder
    # ─────────────────────────────────────────────────────────────────

    def _buildPage2(self):
        p = 2
        self._pack(p, makeLabel("Step 2 — Where should the main picture/decoration appear?", bold=True))
        self._pack(p, makeLabel("Choose where your artwork will be placed.", dim=True))

        # "No image" is first and is the group anchor
        self._r_cov_none = makeRadio("No image (colour/text only)")
        self._r_cov_none.connect("toggled", self.onCoverageToggled)
        self._pack(p, self._r_cov_none)

        for attr, label in [
            ("_r_cov_wrap_all",            "Wrap all (one image across front + back)"),
            ("_r_cov_front_only",          "Front only"),
            ("_r_cov_front_spine",         "Front + spine"),
            ("_r_cov_back_only",           "Back only"),
            ("_r_cov_back_spine",          "Back + spine"),
            ("_r_cov_front_back_separate", "Front and back (separate images)"),
        ]:
            r = makeRadio(label, group=self._r_cov_none)
            r.connect("toggled", self.onCoverageToggled)
            setattr(self, attr, r)
            self._pack(p, r)

        # Default selection
        self._r_cov_none.set_active(True)
        self.state.coverage_pattern = "none"

        pri_box = self._makeImgPickerBox("Primary image", "primary")
        self._rv_img_primary = makeRevealer(pri_box)
        self._rv_img_primary.set_reveal_child(True)
        self._pack(p, self._rv_img_primary)

        sec_box = self._makeImgPickerBox("Back cover image (separate)", "secondary")
        self._rv_img_secondary = makeRevealer(sec_box)
        self._pack(p, self._rv_img_secondary)

        # ── Decorative border ─────────────────────────────────────────
        sep_border = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep_border.set_margin_top(6); sep_border.set_margin_bottom(2)
        sep_border.show()
        self._pack(p, sep_border)

        self._c_border_enable = makeCheck("Add a decorative border to the front cover")
        self._c_border_enable.connect("toggled", self.onBorderEnableToggled)
        self._pack(p, self._c_border_enable)

        # Border controls (revealed when checkbox ticked)
        border_inner = makeVBox(6)
        border_inner.set_margin_start(24)
        border_inner.set_margin_top(4)

        row_style = makeHBox()
        row_style.pack_start(makeLabel("Border style:"), False, False, 0)
        self._cb_border_style = makeCombo([
            ("Han1",       "Han 1"),
            ("Han2",       "Han 2"),
            ("Han3",       "Han 3"),
            ("Han4",       "Han 4"),
            ("Han5",       "Han 5"),
            ("Vectorian1", "Vectorian 1"),
            ("Vectorian2", "Vectorian 2"),
            ("Vectorian3", "Vectorian 3"),
            ("Vectorian4", "Vectorian 4"),
            ("v85",        "v85"),
            ("v85r",       "v85r"),
            ("v85out",     "v85out"),
            ("v86c",       "v86c"),
            ("v86out",     "v86out"),
            ("v88r",       "v88r"),
            ("v88c",       "v88c"),
            ("v88out",     "v88out"),
        ])
        self._cb_border_style.connect("changed", self.onBorderStyleChanged)
        row_style.pack_start(self._cb_border_style, True, True, 0)
        border_inner.pack_start(row_style, False, False, 0)

        row_color = makeHBox()
        row_color.pack_start(makeLabel("Border colour:"), False, False, 0)
        self._cb_border_color = makeColorButton(self.state.border_color)
        self._cb_border_color.connect("color-set", self.onBorderColorSet)
        row_color.pack_start(self._cb_border_color, False, False, 0)
        border_inner.pack_start(row_color, False, False, 0)

        self._rv_border = makeRevealer(border_inner)
        self._pack(p, self._rv_border)

    def _makeImgPickerBox(self, frame_label, key):
        inner = makeVBox(5)
        inner.set_margin_top(6); inner.set_margin_bottom(6)
        inner.set_margin_start(8); inner.set_margin_end(8)

        row_file = makeHBox(6)
        btn = makeButton("Choose image…")
        btn.connect("clicked", lambda w: self._chooseImage(key))
        row_file.pack_start(btn, False, False, 0)
        lbl = Gtk.Label(label="(no file chosen)")
        lbl.set_ellipsize(3); lbl.set_max_width_chars(24)
        lbl.set_valign(Gtk.Align.CENTER); lbl.show()
        lbl.get_style_context().add_class("dim-label")
        row_file.pack_start(lbl, True, True, 0)
        setattr(self, f"_l_img_{key}_status", lbl)
        inner.pack_start(row_file, False, False, 0)

        row_fit = makeHBox()
        row_fit.pack_start(makeLabel("Fit:"), False, False, 0)
        cb = makeCombo(self.FIT_ITEMS)
        cb.connect("changed", lambda w: self._onImgFitChanged(key, w))
        row_fit.pack_start(cb, True, True, 0)
        setattr(self, f"_cb_img_{key}_fit", cb)
        inner.pack_start(row_fit, False, False, 0)

        row_op = makeHBox()
        row_op.pack_start(makeLabel("Opacity:"), False, False, 0)
        sl = makeHScale(100, 0, 100)
        sl.connect("value-changed", lambda w: self._onImgOpacityChanged(key, w))
        row_op.pack_start(sl, True, True, 0)
        setattr(self, f"_sl_img_{key}_opacity", sl)
        inner.pack_start(row_op, False, False, 0)

        return makeFrame(frame_label, inner)

    # ─────────────────────────────────────────────────────────────────
    # Page 3 builder
    # ─────────────────────────────────────────────────────────────────

    def _buildPage3(self):
        p = 3
        self._pack(p, makeLabel("Step 3 — Background colour or shading", bold=True))
        self._pack(p, makeLabel("This colour fills the whole spread behind everything else.", dim=True))

        self._r_bg_white = makeRadio("White (no background colour)")
        self._r_bg_white.set_active(True)
        self._r_bg_white.connect("toggled", self.onBgToggled)
        self._pack(p, self._r_bg_white)

        self._r_bg_solid = makeRadio("Solid colour", group=self._r_bg_white)
        self._r_bg_solid.connect("toggled", self.onBgToggled)
        self._pack(p, self._r_bg_solid)

        color_row = makeHBox(10)
        color_row.set_margin_start(24); color_row.set_margin_top(2)
        color_row.pack_start(makeLabel("Colour:"), False, False, 0)
        self._cb_bgcolor = makeColorButton(self.state.bg_color)
        self._cb_bgcolor.connect("color-set", self.onBgcolorSet)
        color_row.pack_start(self._cb_bgcolor, False, False, 0)
        color_row.pack_start(makeLabel("Opacity:"), False, False, 0)
        self._sl_bg_opacity = makeHScale(100, 0, 100)
        self._sl_bg_opacity.set_hexpand(False)
        self._sl_bg_opacity.set_size_request(130, -1)
        self._sl_bg_opacity.connect("value-changed", self.onBgOpacityChanged)
        color_row.pack_start(self._sl_bg_opacity, False, False, 0)
        self._rv_bgcolor = makeRevealer(color_row)
        self._pack(p, self._rv_bgcolor)

        self._r_bg_gradient = makeRadio("Gradient shading (coming soon)", group=self._r_bg_white)
        self._r_bg_gradient.set_sensitive(False)
        self._r_bg_gradient.connect("toggled", self.onBgToggled)
        self._pack(p, self._r_bg_gradient)

    # ─────────────────────────────────────────────────────────────────
    # Page 4 builder  (REDESIGNED: vertical sliders for position)
    # ─────────────────────────────────────────────────────────────────

    def _makeTextElementBlock(self, key, frame_label, placeholder, default_color,
                              default_size, default_pos_pct):
        """
        Build a frame containing:
          LEFT SIDE (vbox):  text entry | colour+size row
          RIGHT SIDE:        vertical position slider (0=top, 100=bottom)

        The outer container is a horizontal box so the slider sits to the
        right of all the other controls and spans their full height.
        """
        outer = makeHBox(0)
        outer.set_margin_top(4); outer.set_margin_bottom(4)
        outer.set_margin_start(8); outer.set_margin_end(4)

        # ── Left side: entry + controls ───────────────────────────────
        left = makeVBox(4)
        left.set_hexpand(True)

        entry = makeEntry(placeholder)
        entry.connect("changed", lambda w: self._onTextEntryChanged(key, w))
        left.pack_start(entry, False, False, 0)
        setattr(self, f"_t_{key}", entry)

        style_row = makeHBox(6)
        style_row.pack_start(makeLabel("Colour:"), False, False, 0)
        col_btn = makeColorButton(default_color)
        col_btn.connect("color-set", lambda w: self._onTextColorChanged(key, w))
        style_row.pack_start(col_btn, False, False, 0)
        setattr(self, f"_cb_{key}_color", col_btn)

        style_row.pack_start(makeLabel("Size:"), False, False, 0)
        size_sl = makeHScale(default_size, 50, 200)
        size_sl.set_size_request(110, -1)
        size_sl.set_hexpand(False)
        size_sl.connect("value-changed", lambda w: self._onTextSizeChanged(key, w))
        style_row.pack_start(size_sl, False, False, 0)
        style_row.pack_start(makeLabel("%"), False, False, 0)
        setattr(self, f"_sl_{key}_size", size_sl)

        if key == "title":
            self._c_title_box = makeCheck("In a box")
            self._c_title_box.connect("toggled", self.onTitleBoxToggled)
            style_row.pack_start(self._c_title_box, False, False, 4)

        left.pack_start(style_row, False, False, 0)
        outer.pack_start(left, True, True, 0)

        # ── Right side: vertical position slider ──────────────────────
        right = makeVBox(2)
        right.set_margin_start(8)

        pos_sl = makeVScale(default_pos_pct, 0, 100)
        pos_sl.set_tooltip_text("Vertical position (0% = top, 100% = bottom)")
        pos_sl.connect("value-changed", lambda w: self._onPosPctChanged(key, w))
        right.pack_start(pos_sl, True, True, 0)
        setattr(self, f"_sl_{key}_pos", pos_sl)

        outer.pack_start(right, False, False, 0)

        return makeFrame(frame_label, outer)

    def _buildPage4(self):
        p = 4
        self._pack(p, makeLabel("Step 4 — Front cover text and illustration", bold=True))
        self._pack(p, makeLabel(
            "Set the book's title and optionally a subtitle and language name."
            "Drag the Pos % slider on the right of each element to set its "
            "vertical position (0 = top, 100 = bottom).", dim=True))

        # Title (required)
        title_frame = self._makeTextElementBlock(
            "title", "Title * (required)", "Enter the book title…",
            self.state.title_color, self.state.title_size_pct,
            self.state.title_position_pct)
        self._pack(p, title_frame)

        # Subtitle
        self._c_subtitle_enable = makeCheck("Include a subtitle")
        self._c_subtitle_enable.connect("toggled", self.onSubtitleEnableToggled)
        self._pack(p, self._c_subtitle_enable)
        sub_frame = self._makeTextElementBlock(
            "subtitle", None, "Subtitle…",
            self.state.subtitle_color, self.state.subtitle_size_pct,
            self.state.subtitle_position_pct)
        sub_frame.set_margin_start(16)
        self._rv_subtitle = makeRevealer(sub_frame)
        self._pack(p, self._rv_subtitle)

        # Language name
        self._c_langname_enable = makeCheck("Include language / translation name")
        self._c_langname_enable.connect("toggled", self.onLangnameEnableToggled)
        self._pack(p, self._c_langname_enable)
        lang_frame = self._makeTextElementBlock(
            "langname", None, "Language / translation name…",
            self.state.langname_color, self.state.langname_size_pct,
            self.state.langname_position_pct)
        lang_frame.set_margin_start(16)
        self._rv_langname = makeRevealer(lang_frame)
        self._pack(p, self._rv_langname)

        # Foreground illustration
        self._c_fgimage_enable = makeCheck("Include a foreground picture / illustration")
        self._c_fgimage_enable.connect("toggled", self.onFgimageEnableToggled)
        self._pack(p, self._c_fgimage_enable)

        # Outer horizontal box: left controls | right position slider
        fg_outer = makeHBox(0)
        fg_outer.set_margin_top(4); fg_outer.set_margin_bottom(4)
        fg_outer.set_margin_start(8); fg_outer.set_margin_end(4)

        # Left side: file chooser + transparency slider
        fg_left = makeVBox(4)
        fg_left.set_hexpand(True)

        row_fgfile = makeHBox(6)
        self._btn_fgimage = makeButton("Choose image…")
        self._btn_fgimage.connect("clicked", lambda w: self._chooseFgImage())
        row_fgfile.pack_start(self._btn_fgimage, False, False, 0)
        self._l_fgimage_status = Gtk.Label(label="(no file chosen)")
        self._l_fgimage_status.set_ellipsize(3)
        self._l_fgimage_status.set_max_width_chars(20)
        self._l_fgimage_status.set_valign(Gtk.Align.CENTER)
        self._l_fgimage_status.get_style_context().add_class("dim-label")
        self._l_fgimage_status.show()
        row_fgfile.pack_start(self._l_fgimage_status, True, True, 0)
        fg_left.pack_start(row_fgfile, False, False, 0)

        row_fg_trans = makeHBox(6)
        row_fg_trans.pack_start(makeLabel("Transparency:"), False, False, 0)
        self._sl_fgimage_bg_trans = makeHScale(100, 0, 100)
        self._sl_fgimage_bg_trans.set_tooltip_text("0% = fully transparent, 100% = opaque")
        self._sl_fgimage_bg_trans.connect("value-changed", self.onFgimageBgTransChanged)
        row_fg_trans.pack_start(self._sl_fgimage_bg_trans, True, True, 0)
        row_fg_trans.pack_start(makeLabel("%"), False, False, 0)
        fg_left.pack_start(row_fg_trans, False, False, 0)

        fg_outer.pack_start(fg_left, True, True, 0)

        # Right side: vertical position slider
        fg_right = makeVBox(2)
        fg_right.set_margin_start(8)
        self._sl_fgimage_pos = makeVScale(self.state.fgimage_position_pct, 0, 100)
        self._sl_fgimage_pos.set_tooltip_text("Vertical position (0% = top, 100% = bottom)")
        self._sl_fgimage_pos.connect("value-changed", self.onFgimagePosPctChanged)
        fg_right.pack_start(self._sl_fgimage_pos, True, True, 0)
        fg_outer.pack_start(fg_right, False, False, 0)

        fg_frame = makeFrame(None, fg_outer, margin_start=16)
        self._rv_fgimage = makeRevealer(fg_frame)
        self._pack(p, self._rv_fgimage)

    # ─────────────────────────────────────────────────────────────────
    # Page 5 builder
    # ─────────────────────────────────────────────────────────────────

    def _buildPage5(self):
        p = 5
        self._pack(p, makeLabel("Step 5 — Spine text and Publisher Details", bold=True))
        self._pack(p, makeLabel("Choose what needs to appear on the spine.", dim=True))

        self._c_spine_title = makeCheck("Show title on spine")
        self._c_spine_title.set_active(True)
        self._c_spine_title.connect("toggled", self.onSpineContentToggled)
        self._pack(p, self._c_spine_title)
        self._c_spine_subtitle = makeCheck("Show subtitle on spine")
        self._c_spine_subtitle.set_sensitive(False)
        self._c_spine_subtitle.connect("toggled", self.onSpineContentToggled)
        self._pack(p, self._c_spine_subtitle)
        self._c_spine_langname = makeCheck("Show language name on spine")
        self._c_spine_langname.connect("toggled", self.onSpineContentToggled)
        self._pack(p, self._c_spine_langname)

        # ── Spine text style ──────────────────────────────────────────
        sep2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep2.set_margin_top(6); sep2.set_margin_bottom(6); sep2.show()
        self._pack(p, sep2)
        self._pack(p, makeLabel("Spine text style:", bold=True))
        st_outer = makeHBox(0)
        st_outer.set_margin_end(4)
        st_left = makeVBox(6)
        st_left.set_hexpand(True)

        row_st = makeHBox(6)
        row_st.pack_start(makeLabel("Colour:"), False, False, 0)
        self._cb_spine_text_color = makeColorButton(self.state.spine_text_color)
        self._cb_spine_text_color.connect("color-set", self.onSpineTextColorChanged)
        row_st.pack_start(self._cb_spine_text_color, False, False, 0)
        row_st.pack_start(makeLabel("Size:"), False, False, 0)
        self._sl_spine_text_size = makeHScale(100, 50, 200)
        self._sl_spine_text_size.set_size_request(100, -1)
        self._sl_spine_text_size.set_hexpand(False)
        self._sl_spine_text_size.connect("value-changed", self.onSpineTextSizeChanged)
        row_st.pack_start(self._sl_spine_text_size, False, False, 0)
        row_st.pack_start(makeLabel("%"), False, False, 0)
        st_left.pack_start(row_st, False, False, 0)

        row_st_orient = makeHBox(6)
        row_st_orient.pack_start(makeLabel("Orientation:"), False, False, 0)
        self._cb_spine_orientation = makeCombo([
            ("v_ttb", "Vertical (top to bottom)"),
            ("v_btt", "Vertical (bottom to top)"),
            ("horiz", "Horizontal (500+ pages only)"),
        ])
        self._cb_spine_orientation.connect("changed", self.onSpineOrientationComboChanged)
        row_st_orient.pack_start(self._cb_spine_orientation, True, True, 0)
        st_left.pack_start(row_st_orient, False, False, 0)

        st_outer.pack_start(st_left, True, True, 0)
        st_right = makeVBox(2)
        st_right.set_margin_start(8)
        self._sl_spine_text_vpos = makeVScale(self.state.spine_text_vpos_pct, 0, 100)
        self._sl_spine_text_vpos.set_size_request(60, 80)
        self._sl_spine_text_vpos.set_tooltip_text(
            "Vertical position of spine text (0% = top, 100% = bottom)")
        self._sl_spine_text_vpos.connect("value-changed", self.onSpineTextVposChanged)
        st_right.pack_start(self._sl_spine_text_vpos, False, False, 0)
        st_outer.pack_start(st_right, False, False, 0)
        self._pack(p, st_outer)
        
        # ── Publisher name on spine ───────────────────────────────────
        sep3 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep3.set_margin_top(6); sep3.set_margin_bottom(6); sep3.show()
        self._pack(p, sep3)

        self._c_spine_publisher = makeCheck("Include publisher name on spine")
        self._c_spine_publisher.connect("toggled", self.onSpinePublisherToggled)
        self._pack(p, self._c_spine_publisher)

        pub_revealed = makeVBox(6)
        pub_revealed.set_margin_start(24)
        pub_revealed.set_margin_top(4)
        pub_revealed.set_margin_end(4)

        pub_outer = makeHBox(0)

        pub_left = makeVBox(6)
        pub_left.set_hexpand(True)

        row_pub_name = makeHBox(8)
        row_pub_name.pack_start(makeLabel("Name:"), False, False, 0)
        self._t_spine_publisher = makeEntry("Publisher name…")
        self._t_spine_publisher.connect("changed", self.onSpinePublisherNameChanged)
        row_pub_name.pack_start(self._t_spine_publisher, True, True, 0)
        pub_left.pack_start(row_pub_name, False, False, 0)

        row_pub_style = makeHBox(6)
        row_pub_style.pack_start(makeLabel("Colour:"), False, False, 0)
        self._cb_spine_publisher_color = makeColorButton(self.state.spine_publisher_color)
        self._cb_spine_publisher_color.connect("color-set", self.onSpinePublisherColorChanged)
        row_pub_style.pack_start(self._cb_spine_publisher_color, False, False, 0)
        row_pub_style.pack_start(makeLabel("Size:"), False, False, 0)
        self._sl_spine_publisher_size = makeHScale(75, 50, 200)
        self._sl_spine_publisher_size.set_size_request(100, -1)
        self._sl_spine_publisher_size.set_hexpand(False)
        self._sl_spine_publisher_size.connect("value-changed", self.onSpinePublisherSizeChanged)
        row_pub_style.pack_start(self._sl_spine_publisher_size, False, False, 0)
        row_pub_style.pack_start(makeLabel("%"), False, False, 0)
        pub_left.pack_start(row_pub_style, False, False, 0)

        row_pub_orient = makeHBox(6)
        row_pub_orient.pack_start(makeLabel("Orientation:"), False, False, 0)
        self._cb_pub_orientation = makeCombo([
            ("v_ttb", "Vertical (top to bottom)"),
            ("v_btt", "Vertical (bottom to top)"),
            ("horiz", "Horizontal"),
        ])
        self._cb_pub_orientation.connect("changed", self.onPubOrientationChanged)
        row_pub_orient.pack_start(self._cb_pub_orientation, True, True, 0)
        pub_left.pack_start(row_pub_orient, False, False, 0)

        pub_outer.pack_start(pub_left, True, True, 0)

        pub_right = makeVBox(2)
        pub_right.set_margin_start(8)
        self._sl_spine_publisher_vpos = makeVScale(90, 0, 100)
        self._sl_spine_publisher_vpos.set_size_request(60, 80)
        self._sl_spine_publisher_vpos.set_tooltip_text(
            "Vertical position on spine (0% = top, 100% = bottom)")
        self._sl_spine_publisher_vpos.connect("value-changed", self.onSpinePublisherVposChanged)
        pub_right.pack_start(self._sl_spine_publisher_vpos, False, False, 0)
        pub_outer.pack_start(pub_right, False, False, 0)

        pub_revealed.pack_start(pub_outer, False, False, 0)
        self._rv_spine_publisher = makeRevealer(pub_revealed)
        self._pack(p, self._rv_spine_publisher)

        # ── Publisher logo on spine ───────────────────────────────────
        sep4 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep4.set_margin_top(6); sep4.set_margin_bottom(6); sep4.show()
        self._pack(p, sep4)

        self._c_spine_pub_logo = makeCheck("Include publisher logo on spine")
        self._c_spine_pub_logo.connect("toggled", self.onSpinePubLogoToggled)
        self._pack(p, self._c_spine_pub_logo)

        logo_revealed = makeVBox(6)
        logo_revealed.set_margin_start(24)
        logo_revealed.set_margin_top(4)
        logo_revealed.set_margin_end(4)

        logo_outer = makeHBox(0)

        logo_left = makeVBox(6)
        logo_left.set_hexpand(True)

        row_logo_file = makeHBox(6)
        self._btn_spine_pub_logo = makeButton("Choose logo…")
        self._btn_spine_pub_logo.connect("clicked", lambda w: self._chooseSpinePubLogo())
        row_logo_file.pack_start(self._btn_spine_pub_logo, False, False, 0)
        self._l_spine_pub_logo_status = Gtk.Label(label="(no file chosen)")
        self._l_spine_pub_logo_status.set_ellipsize(3)
        self._l_spine_pub_logo_status.set_max_width_chars(18)
        self._l_spine_pub_logo_status.set_valign(Gtk.Align.CENTER)
        self._l_spine_pub_logo_status.get_style_context().add_class("dim-label")
        self._l_spine_pub_logo_status.show()
        row_logo_file.pack_start(self._l_spine_pub_logo_status, True, True, 0)
        logo_left.pack_start(row_logo_file, False, False, 0)

        row_logo_scale = makeHBox(6)
        row_logo_scale.pack_start(makeLabel("Scale:"), False, False, 0)
        self._sl_spine_pub_logo_scale = makeHScale(100, 10, 200)
        self._sl_spine_pub_logo_scale.connect("value-changed", self.onSpinePubLogoScaleChanged)
        row_logo_scale.pack_start(self._sl_spine_pub_logo_scale, True, True, 0)
        row_logo_scale.pack_start(makeLabel("%"), False, False, 0)
        logo_left.pack_start(row_logo_scale, False, False, 0)

        row_logo_rot = makeHBox(6)
        row_logo_rot.pack_start(makeLabel("Rotation:"), False, False, 0)
        self._cb_spine_pub_logo_rot = makeCombo([
            ("none", "None"),
            ("cw",   "Clockwise 90°"),
            ("ccw",  "Anti-clockwise 90°"),
        ])
        self._cb_spine_pub_logo_rot.connect("changed", self.onSpinePubLogoRotChanged)
        row_logo_rot.pack_start(self._cb_spine_pub_logo_rot, True, True, 0)
        logo_left.pack_start(row_logo_rot, False, False, 0)

        logo_outer.pack_start(logo_left, True, True, 0)

        logo_right = makeVBox(2)
        logo_right.set_margin_start(8)
        self._sl_spine_pub_logo_vpos = makeVScale(50, 0, 100)
        self._sl_spine_pub_logo_vpos.set_size_request(60, 80)
        self._sl_spine_pub_logo_vpos.set_tooltip_text(
            "Vertical position of logo on spine (0% = top, 100% = bottom)")
        self._sl_spine_pub_logo_vpos.connect("value-changed", self.onSpinePubLogoVposChanged)
        logo_right.pack_start(self._sl_spine_pub_logo_vpos, False, False, 0)
        logo_outer.pack_start(logo_right, False, False, 0)

        logo_revealed.pack_start(logo_outer, False, False, 0)
        self._rv_spine_pub_logo = makeRevealer(logo_revealed)
        self._pack(p, self._rv_spine_pub_logo)
    # ─────────────────────────────────────────────────────────────────
    # Page 6 builder
    # ─────────────────────────────────────────────────────────────────

    def _buildPage6(self):
        p = 6
        self._pack(p, makeLabel("Step 6 — Back cover content", bold=True))

        # Back text
        self._c_backtext_enable = makeCheck("Include back cover text (blurb)")
        self._c_backtext_enable.connect("toggled", self.onBacktextEnableToggled)
        self._pack(p, self._c_backtext_enable)
        self._t_backtext = Gtk.TextView()
        self._t_backtext.set_wrap_mode(Gtk.WrapMode.WORD)
        self._t_backtext.show()
        sw_bt = Gtk.ScrolledWindow()
        sw_bt.set_min_content_height(60)
        sw_bt.set_max_content_height(300)
        sw_bt.set_propagate_natural_height(True)
        sw_bt.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sw_bt.set_margin_start(24)
        sw_bt.set_shadow_type(Gtk.ShadowType.IN)
        sw_bt.set_hexpand(False)
        sw_bt.add(self._t_backtext)
        sw_bt.show()
        self._t_backtext.get_buffer().connect("changed", self.onBacktextBufferChanged)
        self._rv_backtext = makeRevealer(sw_bt)
        self._pack(p, self._rv_backtext)

        # ISBN
        self._c_isbn_enable = makeCheck("Include ISBN / barcode area")
        self._c_isbn_enable.connect("toggled", self.onIsbnEnableToggled)
        self._pack(p, self._c_isbn_enable)
        isbn_inner = makeVBox(4)
        isbn_inner.set_margin_start(24)

        self._t_isbn = makeEntry("ISBN number…")
        self._t_isbn.connect("changed", self.onIsbnChanged)
        isbn_inner.pack_start(self._t_isbn, False, False, 0)

        row_isbn_hpos = makeHBox(8)
        row_isbn_hpos.pack_start(makeLabel("Position:"), False, False, 0)
        self._cb_isbn_hpos = makeCombo([
            ("inner",  "Inner (near spine)"),
            ("centre", "Centre"),
            ("outer",  "Outer (near edge)"),
        ])
        self._cb_isbn_hpos.set_active_id("inner")
        self._cb_isbn_hpos.connect("changed", self.onIsbnHposChanged)
        row_isbn_hpos.pack_start(self._cb_isbn_hpos, True, True, 0)
        isbn_inner.pack_start(row_isbn_hpos, False, False, 0)

        self._rv_isbn = makeRevealer(isbn_inner)
        self._pack(p, self._rv_isbn)

        # Logo
        self._c_logo_enable = makeCheck("Include a logo or emblem")
        self._c_logo_enable.connect("toggled", self.onLogoEnableToggled)
        self._pack(p, self._c_logo_enable)

        # Outer horizontal box: left controls | right vertical position slider
        logo_outer = makeHBox(0)
        logo_outer.set_margin_start(24)
        logo_outer.set_margin_top(4); logo_outer.set_margin_bottom(4)
        logo_outer.set_margin_end(4)

        # Left side
        logo_left = makeVBox(6)
        logo_left.set_hexpand(True)

        row_logo = makeHBox(8)
        self._btn_logo = makeButton("Choose logo file…")
        self._btn_logo.connect("clicked", lambda w: self._chooseLogo())
        row_logo.pack_start(self._btn_logo, False, False, 0)
        self._l_logo_status = Gtk.Label(label="(no file chosen)")
        self._l_logo_status.set_ellipsize(3)
        self._l_logo_status.set_max_width_chars(22)
        self._l_logo_status.set_valign(Gtk.Align.CENTER)
        self._l_logo_status.get_style_context().add_class("dim-label")
        self._l_logo_status.show()
        row_logo.pack_start(self._l_logo_status, True, True, 0)
        logo_left.pack_start(row_logo, False, False, 0)

        row_scale = makeHBox(8)
        row_scale.pack_start(makeLabel("Scale:"), False, False, 0)
        self._sl_logo_scale = makeHScale(100, 10, 200)
        self._sl_logo_scale.connect("value-changed", self.onLogoScaleChanged)
        row_scale.pack_start(self._sl_logo_scale, True, True, 0)
        row_scale.pack_start(makeLabel("%"), False, False, 0)
        logo_left.pack_start(row_scale, False, False, 0)

        row_logo_hpos = makeHBox(8)
        row_logo_hpos.pack_start(makeLabel("Horizontal:"), False, False, 0)
        self._cb_logo_hpos = makeCombo([
            ("inner",  "Inner (near spine)"),
            ("centre", "Centre"),
            ("outer",  "Outer (near edge)"),
        ])
        self._cb_logo_hpos.set_active_id("centre")
        self._cb_logo_hpos.connect("changed", self.onLogoHorizPosChanged)
        row_logo_hpos.pack_start(self._cb_logo_hpos, True, True, 0)
        logo_left.pack_start(row_logo_hpos, False, False, 0)

        logo_outer.pack_start(logo_left, True, True, 0)

        # Right side: vertical position slider
        logo_right = makeVBox(2)
        logo_right.set_margin_start(8)
        self._sl_logo_vpos = makeVScale(50, 0, 100)
        self._sl_logo_vpos.set_tooltip_text("Vertical position (0% = top, 100% = bottom)")
        self._sl_logo_vpos.connect("value-changed", self.onLogoVertPosChanged)
        logo_right.pack_start(self._sl_logo_vpos, True, True, 0)
        logo_outer.pack_start(logo_right, False, False, 0)

        self._rv_logo = makeRevealer(logo_outer)
        self._pack(p, self._rv_logo)

    # ─────────────────────────────────────────────────────────────────
    # Page 7 builder
    # ─────────────────────────────────────────────────────────────────

    def _buildPage7(self):
        p = 7
        self._pack(p, makeLabel("Step 7 — Review your cover", bold=True))
        self._pack(p, makeLabel(
            "Check the preview on the right, then click Finish to save your settings.",
            dim=True))
        self._l_summary = Gtk.Label(label="Summary will appear here.")
        self._l_summary.set_xalign(0); self._l_summary.set_yalign(0)
        self._l_summary.set_line_wrap(True); self._l_summary.set_selectable(True)
        self._l_summary.show()
        vp = Gtk.Viewport(); vp.set_shadow_type(Gtk.ShadowType.NONE)
        vp.add(self._l_summary); vp.show()
        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sw.set_hexpand(True); sw.add(vp); sw.show()
        self._pack(p, sw, expand=True)

    # ─────────────────────────────────────────────────────────────────
    # Signal handlers — Step 1
    # ─────────────────────────────────────────────────────────────────

    def onPagecountChanged(self, widget):
        try:
            self.state.pagecount = int(widget.get_text().strip())
        except ValueError:
            self.state.pagecount = 0
        if self.state.pagecount >= 80:
            self._r_spine_yes.set_active(True)
        else:
            self._r_spine_no.set_active(True)
        self._updateSpineComputed()
        self._refresh()

    def onSpineToggled(self, widget):
        if not widget.get_active(): return
        self.state.spine_enabled = self._r_spine_yes.get_active()
        self._rv_binding_type.set_reveal_child(self.state.spine_enabled)
        cur = self._steps[self._stepIndex]
        self._updateStepList()
        self._stepIndex = self._steps.index(cur) if cur in self._steps else 0
        self._refresh()

    def onBindingTypeToggled(self, widget):
        if not widget.get_active(): return
        self.state.binding_type = "paperback" if self._r_binding_pb.get_active() else "hardcover"
        self._refresh()

    def onSpineWidthModeToggled(self, widget):
        if not widget.get_active(): return
        self.state.spine_width_mode = "auto" if self._r_sw_auto.get_active() else "manual"
        self._rv_sw_auto.set_reveal_child(self.state.spine_width_mode == "auto")
        self._rv_sw_manual.set_reveal_child(self.state.spine_width_mode == "manual")
        self._updateSpineComputed()
        self._refresh()

    def onGsmChanged(self, widget):
        """GSM spinner changed: derive µm from gsm and update the other spinner."""
        if self._updating_spinners: return
        self.state.paper_gsm = widget.get_value()
        derived_um = gsmToUm(self.state.paper_gsm)
        self.state.paper_thickness_um = derived_um
        self._updating_spinners = True
        self._sp_um.set_value(round(derived_um))
        self._updating_spinners = False
        self._updateSpineComputed()
        self._refresh()

    def onThicknessChanged(self, widget):
        """µm spinner changed: derive gsm from µm and update the other spinner."""
        if self._updating_spinners: return
        self.state.paper_thickness_um = widget.get_value()
        derived_gsm = umToGsm(self.state.paper_thickness_um)
        self.state.paper_gsm = derived_gsm
        self._updating_spinners = True
        self._sp_gsm.set_value(round(derived_gsm))
        self._updating_spinners = False
        self._updateSpineComputed()
        self._refresh()

    def onSpineMmChanged(self, widget):
        self.state.spine_width_mm = widget.get_value()
        self._updateSpineComputed()
        self._refresh()

    def _updateSpineComputed(self):
        self.state.computeSpineWidth()
        self._l_spine_computed.set_text(
            f"Computed spine: {self.state.spine_width_computed_mm:.1f} mm")

    def onRTLBindingToggled(self, widget):
        self.state.rtl_binding = widget.get_active()
        self._refresh()

    # ─────────────────────────────────────────────────────────────────
    # Signal handlers — Step 2
    # ─────────────────────────────────────────────────────────────────

    def onCoverageToggled(self, widget):
        if not widget.get_active(): return
        patterns = [
            (self._r_cov_none,                "none"),
            (self._r_cov_wrap_all,            "wrap_all"),
            (self._r_cov_front_only,          "front_only"),
            (self._r_cov_front_spine,         "front_spine"),
            (self._r_cov_back_only,           "back_only"),
            (self._r_cov_back_spine,          "back_spine"),
            (self._r_cov_front_back_separate, "front_back_separate"),
        ]
        for radio, pattern in patterns:
            if widget is radio:
                self.state.coverage_pattern = pattern
                break
        self._refresh()

    def _chooseImage(self, key):
        path = openImageChooser(self.window)
        if path:
            setattr(self.state, f"img_{key}_path", path)
            self._pixbufCache.pop(path, None)
            getattr(self, f"_l_img_{key}_status").set_text(os.path.basename(path))
            getattr(self, f"_l_img_{key}_status").set_tooltip_text(path)
        self._refresh()

    def _onImgFitChanged(self, key, widget):
        fit = widget.get_active_id() or "stretch"
        setattr(self.state, f"img_{key}_fit", fit)
        self._refresh()

    def _onImgOpacityChanged(self, key, widget):
        setattr(self.state, f"img_{key}_opacity", int(widget.get_value()))
        self._refresh()

    def onBorderEnableToggled(self, widget):
        self.state.border_enabled = widget.get_active()
        self._rv_border.set_reveal_child(self.state.border_enabled)
        self._refresh()

    def onBorderStyleChanged(self, widget):
        self.state.border_style = widget.get_active_id() or "Han1"
        self._refresh()

    def onBorderColorSet(self, widget):
        self.state.border_color = gdkColorToHex(widget.get_rgba())
        self._refresh()

    # ─────────────────────────────────────────────────────────────────
    # Signal handlers — Step 3
    # ─────────────────────────────────────────────────────────────────

    def onBgToggled(self, widget):
        if not widget.get_active(): return
        if self._r_bg_white.get_active():   self.state.bg_mode = "white"
        elif self._r_bg_solid.get_active(): self.state.bg_mode = "solid"
        else:                               self.state.bg_mode = "gradient"
        self._rv_bgcolor.set_reveal_child(self.state.bg_mode == "solid")
        self._refresh()

    def onBgcolorSet(self, widget):
        self.state.bg_color = gdkColorToHex(widget.get_rgba())
        self._refresh()

    def onBgOpacityChanged(self, widget):
        self.state.bg_opacity = int(widget.get_value())
        self._refresh()

    # ─────────────────────────────────────────────────────────────────
    # Signal handlers — Step 4
    # ─────────────────────────────────────────────────────────────────

    def _onTextEntryChanged(self, key, widget):
        setattr(self.state, key, widget.get_text())
        self._refresh()

    def _onPosPctChanged(self, key, widget):
        """Vertical position slider changed (0=top, 100=bottom)."""
        setattr(self.state, f"{key}_position_pct", int(widget.get_value()))
        self._refresh()

    def _onTextColorChanged(self, key, widget):
        setattr(self.state, f"{key}_color", gdkColorToHex(widget.get_rgba()))
        self._refresh()

    def _onTextSizeChanged(self, key, widget):
        setattr(self.state, f"{key}_size_pct", int(widget.get_value()))
        self._refresh()

    def onTitleBoxToggled(self, widget):
        self.state.title_in_box = widget.get_active()
        self._refresh()

    def onSubtitleEnableToggled(self, widget):
        self.state.subtitle_enabled = widget.get_active()
        self._rv_subtitle.set_reveal_child(self.state.subtitle_enabled)
        if not self.state.subtitle_enabled:
            self.state.spine_subtitle = False
            self._c_spine_subtitle.set_active(False)
        self._refresh()

    def onLangnameEnableToggled(self, widget):
        self.state.langname_enabled = widget.get_active()
        self._rv_langname.set_reveal_child(self.state.langname_enabled)
        self._refresh()

    def _chooseFgImage(self):
        path = openImageChooser(self.window, "Choose foreground illustration")
        if path:
            self.state.fgimage_path = path
            self._pixbufCache.pop(path, None)
            self._l_fgimage_status.set_text(os.path.basename(path))
            self._l_fgimage_status.set_tooltip_text(path)
        self._refresh()

    def onFgimageEnableToggled(self, widget):
        self.state.fgimage_enabled = widget.get_active()
        self._rv_fgimage.set_reveal_child(self.state.fgimage_enabled)
        self._refresh()

    def onFgimagePosPctChanged(self, widget):
        self.state.fgimage_position_pct = int(widget.get_value())
        self._refresh()

    def onFgimageBgTransChanged(self, widget):
        self.state.fgimage_bg_trans = int(widget.get_value())
        self._refresh()

    # ─────────────────────────────────────────────────────────────────
    # Signal handlers — Step 5
    # ─────────────────────────────────────────────────────────────────

    def onSpineContentToggled(self, widget):
        self.state.spine_title    = self._c_spine_title.get_active()
        self.state.spine_subtitle = self._c_spine_subtitle.get_active()
        self.state.spine_langname = self._c_spine_langname.get_active()
        self._refresh()

    def onSpinePublisherToggled(self, widget):
        self.state.spine_publisher_enabled = widget.get_active()
        self._rv_spine_publisher.set_reveal_child(self.state.spine_publisher_enabled)
        self._refresh()
        
    def onSpinePublisherNameChanged(self, widget):
        self.state.spine_publisher = widget.get_text()
        self._refresh()

    def onSpinePubLogoToggled(self, widget):
        self.state.spine_pub_logo_enabled = widget.get_active()
        self._rv_spine_pub_logo.set_reveal_child(self.state.spine_pub_logo_enabled)
        self._refresh()

    def _chooseSpinePubLogo(self):
        path = openImageChooser(self.window, "Choose publisher logo")
        if path:
            self.state.spine_pub_logo_path = path
            self._pixbufCache.pop(path, None)
            self._l_spine_pub_logo_status.set_text(os.path.basename(path))
            self._l_spine_pub_logo_status.set_tooltip_text(path)
        self._refresh()

    def onSpinePubLogoScaleChanged(self, widget):
        self.state.spine_pub_logo_scale = int(widget.get_value())
        self._refresh()

    def onSpinePubLogoRotChanged(self, widget):
        self.state.spine_pub_logo_rotation = widget.get_active_id() or "none"
        self._refresh()

    def onSpinePublisherVposChanged(self, widget):
        self.state.spine_publisher_vpos_pct = int(widget.get_value())
        self._refresh()

    def onSpineTextColorChanged(self, widget):
        self.state.spine_text_color = gdkColorToHex(widget.get_rgba())
        self._refresh()

    def onSpineTextSizeChanged(self, widget):
        self.state.spine_text_size_pct = int(widget.get_value())
        self._refresh()

    def onSpineTextVposChanged(self, widget):
        self.state.spine_text_vpos_pct = int(widget.get_value())
        self._refresh()

    def onSpinePublisherColorChanged(self, widget):
        self.state.spine_publisher_color = gdkColorToHex(widget.get_rgba())
        self._refresh()

    def onSpinePublisherSizeChanged(self, widget):
        self.state.spine_publisher_size_pct = int(widget.get_value())
        self._refresh()

    def onSpineOrientationComboChanged(self, widget):
        self.state.spine_orientation = widget.get_active_id() or "v_ttb"
        self._refresh()

    def onPubOrientationChanged(self, widget):
        self.state.pub_orientation = widget.get_active_id() or "v_ttb"
        self._refresh()

    def onSpinePubLogoVposChanged(self, widget):
        self.state.spine_pub_logo_vpos_pct = int(widget.get_value())
        self._refresh()
        
    # ─────────────────────────────────────────────────────────────────
    # Signal handlers — Step 6
    # ─────────────────────────────────────────────────────────────────

    def onBacktextEnableToggled(self, widget):
        self.state.backtext_enabled = widget.get_active()
        self._rv_backtext.set_reveal_child(self.state.backtext_enabled)
        self._refresh()

    def onBacktextBufferChanged(self, buf):
        self.state.backtext = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)
        self._refresh()

    def onIsbnEnableToggled(self, widget):
        self.state.isbn_enabled = widget.get_active()
        self._rv_isbn.set_reveal_child(self.state.isbn_enabled)
        self._refresh()

    def onIsbnChanged(self, widget):
        self.state.isbn = widget.get_text()
        self._refresh()

    def onIsbnHposChanged(self, widget):
        self.state.isbn_hpos = widget.get_active_id() or "inner"
        self._refresh()
        
    def onLogoEnableToggled(self, widget):
        self.state.logo_enabled = widget.get_active()
        self._rv_logo.set_reveal_child(self.state.logo_enabled)
        self._refresh()

    def _chooseLogo(self):
        path = openImageChooser(self.window, "Choose logo file")
        if path:
            self.state.logo_path = path
            self._pixbufCache.pop(path, None)
            self._l_logo_status.set_text(os.path.basename(path))
            self._l_logo_status.set_tooltip_text(path)
        self._refresh()

    def onLogoScaleChanged(self, widget):
        self.state.logo_scale = int(widget.get_value())
        self._refresh()

    def onLogoHorizPosChanged(self, widget):
        self.state.logo_hpos = widget.get_active_id() or "centre"
        self._refresh()

    def onLogoVertPosChanged(self, widget):
        self.state.logo_vpos_pct = int(widget.get_value())
        self._refresh()

    # ─────────────────────────────────────────────────────────────────
    # Navigation
    # ─────────────────────────────────────────────────────────────────

    def onBackClicked(self, widget):    self._goToStep(self._stepIndex - 1)
    def onNextClicked(self, widget):    self._goToStep(self._stepIndex + 1)
    def onCancelClicked(self, widget):  self.window.destroy()

    def onAdvancedClicked(self, widget):
        dlg = Gtk.MessageDialog(transient_for=self.window,
                                message_type=Gtk.MessageType.INFO,
                                buttons=Gtk.ButtonsType.OK,
                                text="Advanced options will be connected to PTXprint's "
                                     "full cover settings when integrated.")
        dlg.run(); dlg.destroy()

    def onFinishClicked(self, widget):
        d = self.state.toDict()
        print("\n── Cover Wizard V5 finished ──")
        print(json.dumps(d, indent=2))
        out = os.path.join(os.getcwd(), "coverwizard_state.json")
        try:
            with open(out, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2)
            dlg = Gtk.MessageDialog(transient_for=self.window,
                                    message_type=Gtk.MessageType.INFO,
                                    buttons=Gtk.ButtonsType.OK,
                                    text=f"Cover settings saved to:\n{out}")
        except OSError as exc:
            dlg = Gtk.MessageDialog(transient_for=self.window,
                                    message_type=Gtk.MessageType.ERROR,
                                    buttons=Gtk.ButtonsType.CLOSE,
                                    text=f"Could not write file:\n{exc}")
        dlg.run(); dlg.destroy()
        self.window.destroy()

    def onWindowDestroy(self, widget):
        Gtk.main_quit()

    # ─────────────────────────────────────────────────────────────────
    # Cairo preview
    # ─────────────────────────────────────────────────────────────────

    def onPreviewDraw(self, widget, cr):
        alloc = widget.get_allocation()
        W, H  = alloc.width, alloc.height
        s     = self.state
        s.computeSpineWidth()

        MARGIN = 18
        drawW  = W - 2*MARGIN
        drawH  = H - 2*MARGIN
        topY   = MARGIN

        # Spine pixel width scaled to preview
        REF_PAGE_MM = 148.0
        if s.spine_enabled and s.spine_width_computed_mm > 0:
            total_mm = 2*REF_PAGE_MM + s.spine_width_computed_mm
            spineFrac = s.spine_width_computed_mm / total_mm
            spinePx  = max(10, int(drawW * spineFrac))
        elif s.spine_enabled:
            spinePx = max(10, int(drawW * 0.06))
        else:
            spinePx = 0

        sideW  = (drawW - spinePx) // 2
        frontW = drawW - sideW - spinePx
        rtl    = s.rtl_binding

        if not rtl:
            backX = MARGIN;         backW = sideW
            spineX = MARGIN + sideW
            frontX = spineX + spinePx
        else:
            frontX = MARGIN
            spineX = MARGIN + frontW
            backX  = spineX + spinePx; backW = sideW

        panelH = drawH

        pg     = self._steps[self._stepIndex]
        hlFront = pg == "pg_step4_front"
        hlSpine = pg == "pg_step5_spine_content"
        hlBack  = pg == "pg_step6_back"
        hlAll   = pg in ("pg_step2_coverage","pg_step3_background","pg_step7_review")

        self._drawBg(cr, s, MARGIN, topY, drawW, panelH)
        self._drawCoverage(cr, s, backX, backW, spineX, spinePx, frontX, frontW, topY, panelH)

        # Dividers
        cr.set_source_rgb(0.45,0.45,0.45); cr.set_line_width(1)
        if s.spine_enabled:
            for x in (spineX, spineX+spinePx):
                cr.move_to(x,topY); cr.line_to(x,topY+panelH); cr.stroke()
        else:
            divX = frontX if not rtl else spineX
            cr.move_to(divX,topY); cr.line_to(divX,topY+panelH); cr.stroke()

        cr.set_source_rgb(0.3,0.3,0.3); cr.set_line_width(1)
        cr.rectangle(MARGIN,topY,drawW,panelH); cr.stroke()

        HL = 3
        def hl(x,y,w,h):
            cr.set_source_rgb(0,0,0); cr.set_line_width(HL)
            cr.rectangle(x+HL/2,y+HL/2,w-HL,h-HL); cr.stroke()
        if hlAll:    hl(MARGIN,topY,drawW,panelH)
        elif hlFront: hl(frontX,topY,frontW,panelH)
        elif hlSpine and s.spine_enabled: hl(spineX,topY,spinePx,panelH)
        elif hlBack:  hl(backX,topY,backW,panelH)

        cr.set_source_rgba(0,0,0,0.20); cr.select_font_face("Sans",0,0); cr.set_font_size(10)
        def clbl(x,y,w,h,t):
            e = cr.text_extents(t)
            cr.move_to(x+(w-e.width)/2, y+h-8); cr.show_text(t)
        clbl(backX,topY,backW,panelH,"BACK")
        clbl(frontX,topY,frontW,panelH,"FRONT")
        if s.spine_enabled and spinePx > 18:
            cr.set_font_size(8)
            e = cr.text_extents("SPINE")
            cr.save()
            cr.translate(spineX+spinePx/2, topY+panelH/2)
            cr.rotate(-math.pi/2)
            cr.move_to(-e.width/2, e.height/2); cr.show_text("SPINE")
            cr.restore()

        self._drawFrontContent(cr, s, frontX, topY, frontW, panelH)
        if s.spine_enabled:
            self._drawSpineText(cr, s, spineX, topY, spinePx, panelH)
            self._drawSpinePublisher(cr, s, spineX, topY, spinePx, panelH)
        self._drawBackContent(cr, s, backX, topY, backW, panelH, rtl)

    # ── Sub-renderers ─────────────────────────────────────────────────

    def _drawBg(self, cr, s, x, y, w, h):
        if s.bg_mode == "white":
            cr.set_source_rgb(1,1,1); cr.rectangle(x,y,w,h); cr.fill()
        elif s.bg_mode == "solid":
            r,g,b = hexToRgb(s.bg_color)
            cr.set_source_rgb(1,1,1); cr.rectangle(x,y,w,h); cr.fill()
            cr.set_source_rgba(r,g,b,s.bg_opacity/100); cr.rectangle(x,y,w,h); cr.fill()
        else:
            pat = cairo.LinearGradient(x,y,x+w,y)
            pat.add_color_stop_rgb(0.0,0.85,0.90,0.98)
            pat.add_color_stop_rgb(0.5,0.60,0.72,0.92)
            pat.add_color_stop_rgb(1.0,0.40,0.55,0.80)
            cr.set_source(pat); cr.rectangle(x,y,w,h); cr.fill()

    def _paintPixbuf(self, cr, pb, x, y, w, h, opacity, fit):
        imgW, imgH = pb.get_width(), pb.get_height()
        cr.save()
        cr.rectangle(x,y,w,h); cr.clip()
        if fit == "stretch":
            cr.translate(x,y); cr.scale(w/imgW, h/imgH); sx, sy = 0, 0
        elif fit.startswith("crop"):
            # Handle directional cropping
            if fit == "crop_top":
                sc = max(w/imgW, h/imgH)
                sx = x + (w - imgW*sc)/2
                sy = y  # Align to top
            elif fit == "crop_bottom":
                sc = max(w/imgW, h/imgH)
                sx = x + (w - imgW*sc)/2
                sy = y + h - imgH*sc  # Align to bottom
            elif fit == "crop_left":
                sc = max(w/imgW, h/imgH)
                sx = x  # Align to left
                sy = y + (h - imgH*sc)/2
            elif fit == "crop_right":
                sc = max(w/imgW, h/imgH)
                sx = x + w - imgW*sc  # Align to right
                sy = y + (h - imgH*sc)/2
            else:  # fallback to centre crop
                sc = max(w/imgW, h/imgH)
                sx = x + (w - imgW*sc)/2
                sy = y + (h - imgH*sc)/2
            cr.translate(sx, sy)
            cr.scale(sc, sc)
            sx, sy = 0, 0
        else:
            sx = x+(w-imgW)/2; sy = y+(h-imgH)/2
            cr.translate(sx,sy); sx,sy = 0,0
        Gdk.cairo_set_source_pixbuf(cr, pb, sx, sy)
        cr.paint_with_alpha(opacity)
        cr.restore()

    def _drawCoverage(self, cr, s, backX, backW, spineX, spinePx, frontX, frontW, topY, panelH):
        IMG_R,IMG_G,IMG_B,IMG_A = 0.45,0.72,0.52,0.45

        def placeholder(x, w):
            cr.set_source_rgba(IMG_R,IMG_G,IMG_B,IMG_A)
            cr.rectangle(x,topY,w,panelH); cr.fill()
            cr.set_source_rgba(0.1,0.38,0.18,0.85)
            cr.select_font_face("Sans",0,1); cr.set_font_size(11)
            e = cr.text_extents("IMAGE")
            cr.move_to(x+(w-e.width)/2, topY+panelH/2); cr.show_text("IMAGE")

        def region(x, w, path, opacity, fit):
            pb = self._loadPixbuf(path) if path else None
            if pb:
                self._paintPixbuf(cr, pb, x, topY, w, panelH, opacity/100, fit)
            else:
                placeholder(x, w)

        p    = s.coverage_pattern
        priP = s.img_primary_path;   priO = s.img_primary_opacity;   priF = s.img_primary_fit
        secP = s.img_secondary_path; secO = s.img_secondary_opacity; secF = s.img_secondary_fit
        leftX = min(backX, frontX)
        totalW = backW + spinePx + frontW

        if p == "wrap_all":
            region(leftX, totalW, priP, priO, priF)
        elif p == "front_only":
            region(frontX, frontW, priP, priO, priF)
        elif p == "front_spine" and s.spine_enabled:
            lx = min(spineX, frontX)
            region(lx, spinePx+frontW, priP, priO, priF)
        elif p == "back_only":
            region(backX, backW, priP, priO, priF)
        elif p == "back_spine" and s.spine_enabled:
            lx = min(backX, spineX)
            region(lx, backW+spinePx, priP, priO, priF)
        elif p == "front_back_separate":
            region(frontX, frontW, priP, priO, priF)
            region(backX,  backW,  secP, secO, secF)

    def _pctToY(self, pct, panelTop, panelH, blockH, margin=10):
        """Convert 0–100% slider to a y coordinate within the panel."""
        usable = panelH - 2*margin - blockH
        return panelTop + margin + (pct/100.0) * usable

    def _drawFrontContent(self, cr, s, fx, fy, fw, fh):
        BASE_FONT = 14.0

        # Foreground illustration
        if s.fgimage_enabled and s.fgimage_path:
            pb = self._loadPixbuf(s.fgimage_path)
            if pb:
                maxW, maxH = fw*0.80, fh*0.40
                sc = min(maxW/pb.get_width(), maxH/pb.get_height())
                iw,ih = pb.get_width()*sc, pb.get_height()*sc
                iy = self._pctToY(s.fgimage_position_pct, fy, fh, ih)
                ix = fx + (fw-iw)/2
                cr.save()
                cr.rectangle(fx,fy,fw,fh); cr.clip()
                cr.translate(ix,iy); cr.scale(sc,sc)
                Gdk.cairo_set_source_pixbuf(cr, pb, 0, 0)
                # Apply transparency: ensure value is 0.0-1.0 range
                alpha = max(0.0, min(1.0, self.state.fgimage_bg_trans / 100.0))
                cr.paint_with_alpha(alpha)
                cr.restore()

        def drawTextLine(text, pos_pct, color_hex, size_pct, is_bold=True):
            fsize = BASE_FONT * (size_pct/100.0)
            cr.set_font_size(fsize)
            cr.select_font_face("Sans", 0, 1 if is_bold else 0)
            r,g,b = hexToRgb(color_hex)
            ty = self._pctToY(pos_pct, fy, fh, fsize+4)
            e  = cr.text_extents(text)
            tx = fx + (fw - e.width)/2
            # Draw box behind title if requested
            if s.title_in_box and pos_pct == s.title_position_pct:
                pad = 6
                cr.set_source_rgba(1,1,1,0.60)
                cr.rectangle(fx+8, ty-pad, fw-16, fsize+4+pad*2); cr.fill()
            cr.set_source_rgba(r,g,b,0.92)
            cr.move_to(tx, ty+fsize); cr.show_text(text)

        drawTextLine(s.title.strip() or "TITLE",
                     s.title_position_pct, s.title_color, s.title_size_pct, is_bold=True)
        if s.subtitle_enabled:
            drawTextLine(s.subtitle.strip() or "(subtitle)",
                         s.subtitle_position_pct, s.subtitle_color, s.subtitle_size_pct, is_bold=False)
        if s.langname_enabled:
            drawTextLine(s.langname.strip() or "(language)",
                         s.langname_position_pct, s.langname_color, s.langname_size_pct, is_bold=False)

        # Decorative border placeholder
        if s.border_enabled:
            r, g, b = hexToRgb(s.border_color)
            cr.set_source_rgba(r, g, b, 0.85)
            cr.set_line_width(3)
            inset = 16
            cr.rectangle(fx + inset, fy + inset, fw - inset*2, fh - inset*2)
            cr.stroke()
            # Style label in corner
            cr.set_font_size(7)
            cr.select_font_face("Sans", 0, 0)
            cr.move_to(fx + inset + 16, fy + inset + 10)
            cr.show_text(s.border_style)

    def _drawSpineText(self, cr, s, sx, sy, sw, sh):
        """Draw the main spine text (title / subtitle / language name)."""
        parts = []
        if s.spine_title:    parts.append(s.title.strip() or "Title")
        if s.spine_subtitle and s.subtitle_enabled:
            parts.append(s.subtitle.strip() or "Subtitle")
        if s.spine_langname: parts.append(s.langname.strip() or "Language")
        txt = " • ".join(parts)
        if not txt:
            return

        BASE_FONT = 9.0
        fsize = BASE_FONT * (s.spine_text_size_pct / 100.0)
        r, g, b = hexToRgb(s.spine_text_color)
        cr.set_source_rgba(r, g, b, 0.92)
        cr.select_font_face("Sans", 0, 0)
        cr.set_font_size(fsize)

        # Position along the spine height
        cx = sx + sw / 2
        cy = sy + (s.spine_text_vpos_pct / 100.0) * sh

        cr.save()
        if s.spine_orientation == "v_ttb":
            cr.translate(cx, cy); cr.rotate(math.pi / 2)
        elif s.spine_orientation == "v_btt":
            cr.translate(cx, cy); cr.rotate(-math.pi / 2)
        else:
            cr.translate(cx, cy)
        e = cr.text_extents(txt)
        cr.move_to(-e.width / 2, e.height / 2)
        cr.show_text(txt)
        cr.restore()

    def _drawSpinePublisher(self, cr, s, sx, sy, sw, sh):
        """
        Draw the publisher name and/or logo on the spine.
        Called independently of _drawSpineText so it always runs
        regardless of whether the main spine text checkboxes are ticked.
        """
        if not s.spine_publisher_enabled:
            return

        BASE_FONT = 8.0
        fsize = BASE_FONT * (s.spine_publisher_size_pct / 100.0)

        # Publisher name text — uses spine_publisher_vpos_pct
        if s.spine_publisher.strip():
            pub_cx = sx + sw / 2
            pub_cy = sy + (s.spine_publisher_vpos_pct / 100.0) * sh
            r, g, b = hexToRgb(s.spine_publisher_color)
            cr.set_source_rgba(r, g, b, 0.88)
            cr.select_font_face("Sans", 0, 0)
            cr.set_font_size(fsize)
            cr.save()
            if s.pub_orientation == "v_btt":
                cr.translate(pub_cx, pub_cy); cr.rotate(-math.pi / 2)
            elif s.pub_orientation == "horiz":
                cr.translate(pub_cx, pub_cy)
            else:  # v_ttb default
                cr.translate(pub_cx, pub_cy); cr.rotate(math.pi / 2)
            e = cr.text_extents(s.spine_publisher.strip())
            cr.move_to(-e.width / 2, e.height / 2)
            cr.show_text(s.spine_publisher.strip())
            cr.restore()

        # Publisher logo — uses spine_pub_logo_vpos_pct independently
        if s.spine_pub_logo_enabled and s.spine_pub_logo_path:
            pb = self._loadPixbuf(s.spine_pub_logo_path)
            if pb:
                logo_cx = sx + sw / 2
                logo_cy = sy + (s.spine_pub_logo_vpos_pct / 100.0) * sh
                REF = sw * 0.85
                baseFit = min(REF / max(pb.get_width(), 1),
                              REF / max(pb.get_height(), 1))
                finalScale = baseFit * (s.spine_pub_logo_scale / 100.0)
                drawW = pb.get_width()  * finalScale
                drawH = pb.get_height() * finalScale
                cr.save()
                cr.translate(logo_cx, logo_cy)
                if s.spine_pub_logo_rotation == "cw":
                    cr.rotate(math.pi / 2)
                elif s.spine_pub_logo_rotation == "ccw":
                    cr.rotate(-math.pi / 2)
                cr.translate(-drawW / 2, -drawH / 2)
                cr.scale(finalScale, finalScale)
                Gdk.cairo_set_source_pixbuf(cr, pb, 0, 0)
                cr.paint()
                cr.restore()

    def _drawBackContent(self, cr, s, bx, by, bw, bh, rtl):
        curY = by + 14
        PAD  = 10

        # Back text with word-wrap + clip
        if s.backtext_enabled:
            boxW = bw - PAD*2
            raw = s.backtext.strip() if s.backtext.strip() else "Back text here"
            cpl = max(10, int((boxW - 8) / (7 * 0.55)))
            lines = wrapText(raw, cpl)
            line_h = 10   # FS(7) + 3
            blkH = max(20, len(lines) * line_h + 8)
            blkH = min(blkH, bh // 2)

            cr.set_source_rgba(0.93, 0.93, 0.88, 0.82)
            cr.rectangle(bx+PAD, curY, boxW, blkH); cr.fill()
            cr.save()
            cr.rectangle(bx+PAD, curY, boxW, blkH); cr.clip()
            cr.set_source_rgba(0.15, 0.15, 0.15, 0.88)
            cr.select_font_face("Sans", 0, 0); cr.set_font_size(7)
            for i, ln in enumerate(lines):
                ly = curY + (i + 1) * line_h
                if ly > curY + blkH - 2: break
                cr.move_to(bx + PAD + 4, ly); cr.show_text(ln)
            cr.restore()
            curY += blkH + 8

        if s.logo_enabled:
            pb = self._loadPixbuf(s.logo_path) if s.logo_path else None
            if pb:
                # Scale: fit to a reference size, then apply user slider
                REF = min(bw * 0.4, bh * 0.25)   # reference dimension
                baseFit = min(REF / max(pb.get_width(), 1),
                              REF / max(pb.get_height(), 1))
                finalScale = baseFit * (s.logo_scale / 100.0)
                drawW = pb.get_width()  * finalScale
                drawH = pb.get_height() * finalScale

                # Horizontal position.
                # The back panel is on the LEFT of the spread (LTR), so
                # "inner" means near the spine = RIGHT edge of back panel,
                # "outer" means near the outer edge = LEFT edge of back panel.
                # For RTL the back panel is on the right, so it flips again.
                if not rtl:
                    # LTR: back is on left, spine is on right side of back
                    if s.logo_hpos == "inner":    # near spine = right
                        drawX = bx + bw - PAD - drawW
                    elif s.logo_hpos == "outer":  # near outer edge = left
                        drawX = bx + PAD
                    else:                          # centre
                        drawX = bx + (bw - drawW) / 2
                else:
                    # RTL: back is on right, spine is on left side of back
                    if s.logo_hpos == "inner":    # near spine = left
                        drawX = bx + PAD
                    elif s.logo_hpos == "outer":  # near outer edge = right
                        drawX = bx + bw - PAD - drawW
                    else:                          # centre
                        drawX = bx + (bw - drawW) / 2

                # Vertical position: full panel height, 0%=top 100%=bottom
                usableV = bh - drawH
                drawY = by + (s.logo_vpos_pct / 100.0) * usableV

                cr.save()
                cr.rectangle(bx, by, bw, bh)   # clip to full panel, not just laH
                cr.clip()
                cr.translate(drawX, drawY)
                cr.scale(finalScale, finalScale)
                Gdk.cairo_set_source_pixbuf(cr, pb, 0, 0)
                cr.paint()
                cr.restore()

            else:
                # Placeholder box
                cr.set_source_rgba(0.75, 0.85, 0.95, 0.85)
                cr.rectangle(bx + PAD, curY, 36, 36); cr.fill()
                cr.set_source_rgba(0.2, 0.3, 0.5, 0.75)
                cr.select_font_face("Sans", 0, 0); cr.set_font_size(8)
                cr.move_to(bx + PAD + 4, curY + 22); cr.show_text("Logo")
        # ISBN + barcode
        if s.isbn_enabled:
            blkW = min(55, bw // 2); blkH = 32
            isbnY = by + bh - blkH - 10

            # Back panel is on the LEFT in LTR, so inner = right (spine side),
            # outer = left (outer edge). Flipped for RTL.
            if not rtl:
                if s.isbn_hpos == "inner":    # near spine = right of back panel
                    isbnX = bx + bw - blkW - PAD
                elif s.isbn_hpos == "outer":  # near outer edge = left of back panel
                    isbnX = bx + PAD
                else:                          # centre
                    isbnX = bx + (bw - blkW) // 2
            else:
                if s.isbn_hpos == "inner":    # near spine = left of back panel
                    isbnX = bx + PAD
                elif s.isbn_hpos == "outer":  # near outer edge = right of back panel
                    isbnX = bx + bw - blkW - PAD
                else:                          # centre
                    isbnX = bx + (bw - blkW) // 2

            cr.set_source_rgba(0.97, 0.97, 0.97, 0.95)
            cr.rectangle(isbnX, isbnY, blkW, blkH); cr.fill()
            cr.set_source_rgb(0, 0, 0); cr.set_line_width(0.8)
            cr.rectangle(isbnX, isbnY, blkW, blkH); cr.stroke()
            sx2, sy2, sh2 = isbnX + 3, isbnY + 3, blkH - 14
            for i in range(16):
                cr.set_source_rgb(0, 0, 0) if i % 3 != 1 else cr.set_source_rgb(1, 1, 1)
                cr.rectangle(sx2 + i*3, sy2, 2, sh2); cr.fill()
            cr.set_source_rgb(0, 0, 0)
            cr.select_font_face("Sans", 0, 0); cr.set_font_size(6)
            cr.move_to(isbnX + 3, isbnY + blkH - 4)
            cr.show_text((s.isbn if s.isbn else "ISBN")[:18])


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    app = CoverWizardApp()
    Gtk.main()

if __name__ == "__main__":
    main()
