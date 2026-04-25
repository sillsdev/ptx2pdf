import logging
import math
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import cairo

logger = logging.getLogger(__name__)

COST_COLORS = {
    "low":     (0.2, 0.7, 0.2),
    "medium":  (0.9, 0.7, 0.1),
    "high":    (0.8, 0.2, 0.2),
    "unknown": (0.6, 0.6, 0.6),
}


class FeedbackPanel(Gtk.Box):

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.set_margin_start(8)
        self.set_margin_end(12)
        self.set_margin_top(12)
        self.set_margin_bottom(12)
        self._pageCount = 0
        self._spineWidth = None
        self._perCopy = "unknown"
        self._total = "unknown"
        self._violations = []
        self._columns = 1
        self._trimSize = "a5"
        self._buildUi()
        self.show()

    def _buildUi(self):
        titleLbl = Gtk.Label()
        titleLbl.set_markup("<b>Live Feedback</b>")
        titleLbl.set_xalign(0.0)
        titleLbl.show()
        self.pack_start(titleLbl, False, False, 0)

        sep = Gtk.Separator()
        sep.show()
        self.pack_start(sep, False, False, 0)

        # Thumbnail (Cairo DrawingArea)
        self._thumbFrame = Gtk.Frame()
        self._thumbFrame.set_label("Page preview")
        self._thumbFrame.set_label_align(0.0, 0.5)
        self._da = Gtk.DrawingArea()
        self._da.set_size_request(140, 180)
        self._da.connect("draw", self._onDraw)
        self._da.show()
        self._thumbFrame.add(self._da)
        self._thumbFrame.show()
        self.pack_start(self._thumbFrame, False, False, 0)

        # Page count
        self._pageCountBox = self._makeStatRow("Est. pages")
        self._pageCountLbl = self._pageCountBox[1]
        self.pack_start(self._pageCountBox[0], False, False, 0)

        # Spine width
        self._spineBox = self._makeStatRow("Spine width")
        self._spineLbl = self._spineBox[1]
        self.pack_start(self._spineBox[0], False, False, 0)

        sep2 = Gtk.Separator()
        sep2.show()
        self.pack_start(sep2, False, False, 0)

        # Cost bars
        costTitle = Gtk.Label()
        costTitle.set_markup("<b>Cost estimate</b>")
        costTitle.set_xalign(0.0)
        costTitle.show()
        self.pack_start(costTitle, False, False, 0)

        self._perCopyBar = self._makeCostBar("Per copy", "perCopy")
        self.pack_start(self._perCopyBar[0], False, False, 0)

        self._totalBar = self._makeCostBar("Total", "total")
        self.pack_start(self._totalBar[0], False, False, 0)

        sep3 = Gtk.Separator()
        sep3.show()
        self.pack_start(sep3, False, False, 0)

        # Warnings
        warnTitle = Gtk.Label()
        warnTitle.set_markup("<b>Warnings</b>")
        warnTitle.set_xalign(0.0)
        warnTitle.show()
        self.pack_start(warnTitle, False, False, 0)

        self._warningsBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self._warningsBox.show()

        self._noWarningsLbl = Gtk.Label(label="✅  No issues")
        self._noWarningsLbl.set_xalign(0.0)
        self._noWarningsLbl.show()
        self._warningsBox.pack_start(self._noWarningsLbl, False, False, 0)

        self.pack_start(self._warningsBox, False, False, 0)

    def _makeStatRow(self, label):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        lbl = Gtk.Label(label=f"{label}:")
        lbl.set_xalign(0.0)
        lbl.set_width_chars(14)
        lbl.show()
        val = Gtk.Label(label="—")
        val.set_xalign(0.0)
        val.show()
        row.pack_start(lbl, False, False, 0)
        row.pack_start(val, True, True, 0)
        row.show()
        return row, val

    def _makeCostBar(self, label, valueAttr):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        lbl = Gtk.Label(label=label)
        lbl.set_xalign(0.0)
        lbl.show()
        da = Gtk.DrawingArea()
        da.set_size_request(-1, 18)
        da.set_hexpand(True)
        da.connect("draw", self._onCostDraw, valueAttr)
        da.show()
        box.pack_start(lbl, False, False, 0)
        box.pack_start(da, False, False, 0)
        box.show()
        return box, da

    def update(self, pageCount: int, spineWidth, perCopy: str, total: str,
               violations: list, columns: int = 1, trimSize: str = "a5"):
        self._pageCount = pageCount
        self._spineWidth = spineWidth
        self._perCopy = perCopy
        self._total = total
        self._violations = violations
        self._columns = columns
        self._trimSize = trimSize

        self._pageCountLbl.set_text(f"~{pageCount}" if pageCount else "—")
        self._spineLbl.set_text(f"~{spineWidth} mm" if spineWidth else "—")

        self._perCopyBar[1].queue_draw()
        self._totalBar[1].queue_draw()

        self._refreshWarnings(violations)
        self._da.queue_draw()

    def _onCostDraw(self, _da, cr: cairo.Context, valueAttr: str):
        value = getattr(self, f"_{valueAttr}", "unknown")
        w = _da.get_allocated_width()
        h = _da.get_allocated_height()
        cr.set_source_rgb(0.85, 0.85, 0.85)
        cr.rectangle(0, 0, w, h)
        cr.fill()
        SEGMENTS = ["low", "medium", "high"]
        segW = w / 3
        for i, seg in enumerate(SEGMENTS):
            r, g, b = COST_COLORS.get(seg, (0.6, 0.6, 0.6))
            if seg == value:
                cr.set_source_rgb(r, g, b)
            else:
                cr.set_source_rgba(r, g, b, 0.25)
            cr.rectangle(i * segW + 1, 1, segW - 2, h - 2)
            cr.fill()
            cr.set_source_rgb(0, 0, 0)
            cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_BOLD if seg == value else cairo.FONT_WEIGHT_NORMAL)
            cr.set_font_size(9)
            te = cr.text_extents(seg.upper())
            cr.move_to(i * segW + (segW - te.width) / 2, (h + te.height) / 2 - 1)
            cr.show_text(seg.upper())

    def _refreshWarnings(self, violations: list):
        for child in list(self._warningsBox.get_children()):
            self._warningsBox.remove(child)

        if not violations:
            self._noWarningsLbl = Gtk.Label(label="✅  No issues")
            self._noWarningsLbl.set_xalign(0.0)
            self._noWarningsLbl.show()
            self._warningsBox.pack_start(self._noWarningsLbl, False, False, 0)
            return

        for v in violations[:8]:  # cap at 8 to avoid overflow
            sev = v.get("severity", "warning")
            icon = "⛔" if sev == "error" else "⚠"
            lbl = Gtk.Label(label=f"{icon} {v['message']}")
            lbl.set_xalign(0.0)
            lbl.set_line_wrap(True)
            lbl.set_max_width_chars(28)
            lbl.show()
            self._warningsBox.pack_start(lbl, False, False, 0)

    def _onDraw(self, _da, cr: cairo.Context):
        """Draw a schematic page thumbnail with columns and text lines."""
        w = _da.get_allocated_width()
        h = _da.get_allocated_height()

        # Page outline
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(4, 4, w - 8, h - 8)
        cr.fill()
        cr.set_source_rgb(0.6, 0.6, 0.6)
        cr.set_line_width(1)
        cr.rectangle(4, 4, w - 8, h - 8)
        cr.stroke()

        # Margins (proportional)
        margin = 10
        textX = 4 + margin
        textY = 4 + margin
        textW = w - 8 - margin * 2
        textH = h - 8 - margin * 2

        cols = self._columns or 1
        gutter = 6 if cols == 2 else 0
        colW = (textW - gutter * (cols - 1)) / cols

        lineH = 4
        lineGap = 2

        cr.set_source_rgb(0.7, 0.7, 0.85)
        for col in range(cols):
            colX = textX + col * (colW + gutter)
            y = textY
            while y + lineH <= textY + textH:
                # vary line width slightly for realism
                lineW = colW * (0.6 + 0.4 * abs(math.sin(y * 0.3)))
                cr.rectangle(colX, y, lineW, lineH)
                cr.fill()
                y += lineH + lineGap

        # Trim size label
        cr.set_source_rgb(0.4, 0.4, 0.4)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(7)
        label = self._trimSize or ""
        te = cr.text_extents(label)
        cr.move_to((w - te.width) / 2, h - 2)
        cr.show_text(label)
