r"""Controller for the Printers tab: the shared job specification strip,
the printer directory list, and the per-printer detail panels (a GtkStack).
"""

import logging
from gi.repository import Gtk, GLib
from ptxprint.utils import _
from ptxprint.printers.base import JobSpec, PrinterBase
from ptxprint.printers.panel import PrinterPanel
from ptxprint.printers.currency import allcurrencies, getExchangeRates, \
        quoteQuantities, formatCurrency

logger = logging.getLogger(__name__)

BEST_PRICE_COLOR = "#2C7A44"


class PrinterTab:
    def __init__(self, view):
        self.view = view
        self.exchangeRates = getExchangeRates()
        self.panels = {}
        self.compare = {}
        self._updating = False
        self._build()

    def _canPrice(self, printer):
        return (type(printer).estimate is not PrinterBase.estimate
                or getattr(printer, 'liveQuotes', False))

    def _build(self):
        builder = self.view.builder
        currencyCombo = builder.get_object("fcb_prn_currency")
        for code in sorted(allcurrencies.keys()):
            currencyCombo.append(code, code)
        currencyCombo.set_active_id("EUR")
        self.exchangeRates.startFetch(onDone=lambda rates: GLib.idle_add(self.updateAll))

        self.stack = builder.get_object("stk_printerDetail")
        # pid, compare, name markup, price markup
        self.store = Gtk.ListStore(str, bool, str, str)
        for pid, printer in self.view.printers.items():
            panel = PrinterPanel(self.view, printer, self.onSpecChanged)
            self.panels[pid] = panel
            self.stack.add_named(panel.box, pid)
            panel.box.show_all()
            self.compare[pid] = self._canPrice(printer)
            domain = (printer.url or "").split("//")[-1].strip("/")
            name = "<b>{}</b>\n<small>{}</small>".format(printer.displayName,
                    " · ".join(x for x in (printer.countryName, domain) if x))
            self.store.append([pid, self.compare[pid], name, "—"])

        tv = Gtk.TreeView(model=self.store)
        tv.set_headers_visible(True)
        toggle = Gtk.CellRendererToggle()
        toggle.connect("toggled", self.onCompareToggled)
        tv.append_column(Gtk.TreeViewColumn(_("Compare"), toggle, active=1))
        nameCell = Gtk.CellRendererText()
        nameCol = Gtk.TreeViewColumn(_("Printer"), nameCell, markup=2)
        nameCol.set_expand(True)
        tv.append_column(nameCol)
        priceCell = Gtk.CellRendererText()
        priceCell.set_property("xalign", 1.0)
        tv.append_column(Gtk.TreeViewColumn(_("Est. per copy"), priceCell, markup=3))
        tv.get_selection().connect("changed", self.onPrinterSelected)
        scroller = builder.get_object("scr_printerList")
        scroller.add(tv)
        tv.show_all()
        self.listView = tv

        for wid, signal in (("s_prn_pages", "value-changed"),
                            ("s_prn_copies", "value-changed"),
                            ("fcb_prn_interior", "changed"),
                            ("fcb_prn_binding", "changed"),
                            ("fcb_prn_currency", "changed")):
            builder.get_object(wid).connect(signal, self.onSpecChanged)

        tv.get_selection().select_path(Gtk.TreePath.new_first())

    def jobSpec(self):
        g = self.view.get
        def asInt(v):
            try:
                return int(float(v))
            except (TypeError, ValueError):
                return 0
        width, height = self.view.calcPageSize()
        return JobSpec(pages=asInt(g("s_prn_pages")),
                       widthMm=width, heightMm=height,
                       copies=asInt(g("s_prn_copies")),
                       color=(g("fcb_prn_interior") == "color"),
                       binding=g("fcb_prn_binding") or "soft",
                       currency=g("fcb_prn_currency") or "EUR")

    def isCompared(self, pid):
        return self.compare.get(pid, False)

    def refresh(self):
        """Called whenever the Printers tab becomes visible."""
        self.refreshPageCount(update=False)
        width, height = self.view.calcPageSize()
        self.view.set("l_prn_trimSize", "{:.0f} × {:.0f} mm".format(width, height))
        pid = self.stack.get_visible_child_name()
        if pid in self.view.printers:
            self.view.printers[pid].prepare()
        self.updateAll()

    def refreshPageCount(self, update=True):
        pages = self.view.getPageCount()
        if pages is not None:
            self.view.set("s_prn_pages", pages)
            if update:
                self.updateAll()

    def onSpecChanged(self, *a):
        self.updateAll()

    def onCompareToggled(self, cell, path):
        row = self.store[path]
        printer = self.view.printers.get(row[0])
        if printer is None or not self._canPrice(printer):
            return
        row[1] = not row[1]
        self.compare[row[0]] = row[1]

    def onPrinterSelected(self, selection):
        model, it = selection.get_selected()
        if it is None:
            return
        pid = model[it][0]
        self.stack.set_visible_child_name(pid)
        printer = self.view.printers.get(pid)
        if printer is not None:
            printer.prepare()
            self.updateAll()

    def _priceText(self, perCopy, home, job, copies=1):
        amount = perCopy * copies
        converted = self.exchangeRates.convert(amount, home, job.currency)
        if converted is not None:
            return formatCurrency(converted, job.currency)
        return formatCurrency(amount, home)

    def updateAll(self):
        """Recompute estimates for every printer; refresh list and panels."""
        if self._updating:
            return
        self._updating = True
        try:
            self._updateAll()
        finally:
            self._updating = False

    def _updateAll(self):
        job = self.jobSpec()
        quantities = quoteQuantities(job.copies)
        perCopy = {}        # pid: (perCopyHome, homeCurrency)
        for pid, printer in self.view.printers.items():
            estimates = printer.estimate(job, quantities)
            if estimates and job.copies in estimates:
                perCopy[pid] = (estimates[job.copies], printer.homeCurrency)

        best = None
        if len(perCopy) > 1:
            comparable = {pid: self.exchangeRates.convert(v, home, job.currency)
                          for pid, (v, home) in perCopy.items()}
            comparable = {pid: v for pid, v in comparable.items() if v is not None}
            if len(comparable) > 1:
                best = min(comparable, key=comparable.get)

        for row in self.store:
            pid = row[0]
            printer = self.view.printers[pid]
            if pid in perCopy:
                value, home = perCopy[pid]
                text = self._priceText(value, home, job)
                if getattr(printer, 'liveQuotes', False):
                    text += "\n<small>live quote</small>"
                else:
                    text += "\n<small>estimate</small>"
                if pid == best:
                    text = '<span foreground="{}">{}</span>'.format(BEST_PRICE_COLOR, text)
            elif getattr(printer, 'liveQuotes', False):
                text = "—\n<small>{}</small>".format(_("quote in panel"))
            elif self._canPrice(printer):
                text = "—"
            else:
                text = "—\n<small>{}</small>".format(_("no model yet"))
            row[3] = text

            if self._canPrice(printer):
                if pid in perCopy:
                    value, home = perCopy[pid]
                    self.view.set("l_prn_{}_percopy".format(pid), self._priceText(value, home, job))
                    self.view.set("l_prn_{}_total".format(pid),
                                  self._priceText(value, home, job, copies=job.copies))
                else:
                    self.view.set("l_prn_{}_percopy".format(pid), "-")
                    self.view.set("l_prn_{}_total".format(pid), "-")
            self.view.set("l_prn_{}_warn".format(pid), "  ".join(printer.warnings(job)))
            printer.update(job)
