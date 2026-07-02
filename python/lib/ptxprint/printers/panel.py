r"""Builds a printer's detail panel at runtime from its declarations.

Every widget is registered with the GtkBuilder via expose_object(), so
view.get()/view.set() work on dynamic widgets exactly as on Glade ones.
Adding a printer therefore requires no Glade editing at all.
"""

from gi.repository import Gtk, Pango
from ptxprint.utils import _
from ptxprint.printers.base import Choice, Spin


class PrinterPanel:
    def __init__(self, view, printer, onChanged):
        self.view = view
        self.printer = printer
        self.onChanged = onChanged
        self._row = 0

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        for setter in ("set_margin_start", "set_margin_end", "set_margin_top", "set_margin_bottom"):
            getattr(self.box, setter)(8)

        self._buildHeader()
        if printer.description:
            desc = Gtk.Label(label=_(printer.description))
            desc.set_halign(Gtk.Align.START)
            desc.set_line_wrap(True)
            desc.set_max_width_chars(52)
            desc.get_style_context().add_class("dim-label")
            self.box.pack_start(desc, False, False, 0)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(8)
        self.box.pack_start(self.grid, False, False, 0)

        for opt in printer.options:
            self._addOption(opt)
        for out in printer.outputs:
            self.addOutputRow(out.wid, _(out.label))
        printer.panelExtras(self)
        self._buildFooter()

    def expose(self, wid, widget):
        self.view.builder.expose_object(wid, widget)

    def _buildHeader(self):
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        name = Gtk.Label()
        name.set_markup("<b>{}</b>".format(self.printer.displayName))
        header.pack_start(name, False, False, 0)
        if self.printer.countryName:
            where = Gtk.Label(label=self.printer.countryName)
            where.get_style_context().add_class("dim-label")
            header.pack_start(where, False, False, 0)
        if self.printer.url:
            domain = self.printer.url.split("//")[-1].strip("/")
            link = Gtk.LinkButton(uri=self.printer.url, label=_("Visit {}").format(domain))
            link.set_halign(Gtk.Align.END)
            header.pack_end(link, False, False, 0)
        self.box.pack_start(header, False, False, 0)

    def _buildFooter(self):
        pid = self.printer.pid
        self.warnLabel = Gtk.Label()
        self.warnLabel.set_halign(Gtk.Align.START)
        self.warnLabel.set_line_wrap(True)
        self.warnLabel.set_max_width_chars(52)
        self.warnLabel.get_style_context().add_class("red-label")
        self.expose("l_prn_{}_warn".format(pid), self.warnLabel)
        self.box.pack_start(self.warnLabel, False, False, 0)

        price = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        for wid, caption, bold in (("l_prn_{}_percopy".format(pid), _("Per Copy:"), False),
                                   ("l_prn_{}_total".format(pid), _("Total Job:"), True)):
            cap = Gtk.Label()
            if bold:
                cap.set_markup("<b>{}</b>".format(caption))
            else:
                cap.set_label(caption)
            price.pack_start(cap, False, False, 6)
            val = Gtk.Label(label="-")
            val.set_halign(Gtk.Align.START)
            self.expose(wid, val)
            price.pack_start(val, False, False, 0)
        self.box.pack_end(price, False, False, 2)

    def _label(self, text):
        label = Gtk.Label(label=text)
        label.set_halign(Gtk.Align.END)
        return label

    def addRow(self, labelText, widget):
        """Attach a captioned widget as the next grid row."""
        self.grid.attach(self._label(labelText), 0, self._row, 1, 1)
        self.grid.attach(widget, 1, self._row, 1, 1)
        self._row += 1
        return widget

    def _addOption(self, opt):
        if isinstance(opt, Choice):
            w = Gtk.ComboBoxText()
            for iid, itext in opt.items:
                w.append(iid, _(itext))
            w.set_active_id(opt.default if opt.default is not None else opt.items[0][0])
            w.connect("changed", self.onChanged)
        elif isinstance(opt, Spin):
            adj = Gtk.Adjustment(value=opt.default, lower=opt.lower, upper=opt.upper,
                                 step_increment=opt.step, page_increment=opt.step * 5)
            w = Gtk.SpinButton(adjustment=adj, numeric=True)
            w.connect("value-changed", self.onChanged)
        else:
            raise NotImplementedError(f"Unknown option type {opt}")
        if opt.tip:
            w.set_tooltip_text(_(opt.tip))
        self.expose(opt.wid, w)
        self.addRow(_(opt.label), w)

    def addOutputRow(self, wid, labelText):
        """A read-only value row; returns the enclosing box so callers can
        pack further widgets (buttons, links) after the value."""
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        val = Gtk.Label(label="-")
        val.set_halign(Gtk.Align.START)
        self.expose(wid, val)
        box.pack_start(val, False, False, 0)
        self.addRow(labelText, box)
        return box

    def addEntryRow(self, wid, labelText, onChanged=None):
        entry = Gtk.Entry()
        entry.set_width_chars(24)
        if onChanged is not None:
            entry.connect("changed", onChanged)
        self.expose(wid, entry)
        return self.addRow(labelText, entry)

    def addButtonRow(self, wid, labelText, handler, labelWid=None):
        """A button in the widget column; labelWid adds a value label beside it."""
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn = Gtk.Button(label=labelText)
        btn.connect("clicked", handler)
        self.expose(wid, btn)
        box.pack_start(btn, False, False, 0)
        if labelWid is not None:
            val = Gtk.Label(label="")
            val.set_halign(Gtk.Align.START)
            self.expose(labelWid, val)
            box.pack_start(val, False, False, 0)
        self.grid.attach(box, 1, self._row, 1, 1)
        self._row += 1
        return btn

    def addTierStrip(self, pid, headers, wids):
        """A quantity/price strip: one column per discount tier."""
        strip = Gtk.Grid()
        strip.set_column_spacing(12)
        strip.set_row_spacing(2)
        for i, (hdr, wid) in enumerate(zip(headers, wids)):
            h = Gtk.Label()
            h.set_markup("<small><b>{}</b></small>".format(hdr))
            strip.attach(h, i, 0, 1, 1)
            val = Gtk.Label(label="-")
            self.expose(wid, val)
            strip.attach(val, i, 1, 1, 1)
        self.grid.attach(strip, 0, self._row, 2, 1)
        self._row += 1
        return strip
