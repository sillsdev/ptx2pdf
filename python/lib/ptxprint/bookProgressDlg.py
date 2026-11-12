"""
bookProgressDlg.py — Book Progress Monitor dialog for PTXprint page-fill jobs.

Displays a per-book progress grid updated in real time from ProgressEvent objects
delivered via the existing multiprocessing.Queue / GLib.io_add_watch infrastructure.
"""

import math, logging, time
from gi.repository import Gtk, Gdk, GLib
from ptxprint.utils import _

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------
STATUS_PENDING       = "pending"
STATUS_PROBING       = "probing"
STATUS_RUNNING       = "running"
STATUS_RUNNINGFAILED = "failing"
STATUS_GOOD          = "good"
STATUS_WARNING       = "warning"
STATUS_FAILED        = "failed"
STATUS_ALREADY_FILLED = "already_filled"
STATUS_SKIPPED        = "skipped"
STATUS_PAGE          = "page"

# Single source of truth: status → (hex_color, msgid).
# Insertion order determines Color Key display order.
_STATUS_DATA = {
    STATUS_PENDING:        ("#AAAAAA", "Not yet started"),
    STATUS_ALREADY_FILLED: ("#98FB98", "Already filled — no action needed"),
    STATUS_SKIPPED:        ("#FFDAB9", "No page data — skipped pages, may need attention"),
    STATUS_PROBING:        ("#98BCCA", "Probing — initial analysis"),
    STATUS_RUNNING:        ("#87CEEB", "Filling in progress"),
    STATUS_RUNNINGFAILED:  ("#D8C291", "Filling with bad pages"),
    STATUS_GOOD:           ("#98FB98", "Complete — all pages filled"),
    STATUS_WARNING:        ("#FFA500", "Incomplete — page(s) could not be solved"),
    STATUS_FAILED:         ("#F08080", "Failed — fault or timeout"),
}

# The colour legend under the bars shows one chip per group, in this order, using the colour
# of the group's first status. The ⓘ button lists every status, grouped the same way.
_LEGEND_GROUPS = (
    ("Waiting",   (STATUS_PENDING,)),
    ("Analysing", (STATUS_PROBING,)),
    ("Filling",   (STATUS_RUNNING, STATUS_RUNNINGFAILED)),
    ("Done",      (STATUS_GOOD, STATUS_ALREADY_FILLED)),
    ("Check",     (STATUS_WARNING, STATUS_SKIPPED)),
    ("Failed",    (STATUS_FAILED,)),
)
_DONE_STATUSES  = (STATUS_GOOD, STATUS_ALREADY_FILLED)
_CHECK_STATUSES = (STATUS_WARNING, STATUS_SKIPPED)

stoplabel = _("Stop!")

css = """
    progressbar trough, progressbar progress {
        min-height: 1.8em;
    }
    progressbar text {
        color: black;
    }
"""

# ---------------------------------------------------------------------------
# BookProgressCell
# ---------------------------------------------------------------------------

class BookProgressCell:
    """Single progress bar per book: colour conveys status, bar text shows progress then final status."""

    def __init__(self, bookCode: str, stylep=None):
        self.bookCode = bookCode
        self._hadBadPage = False
        self.firstBadPage = None        # for the end-of-run summary
        self._status = STATUS_PENDING
        self._total = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        vbox.set_margin_start(3)
        vbox.set_margin_end(3)
        vbox.set_margin_top(0)
        vbox.set_margin_bottom(0)
        self.frame = vbox   # expose as .frame for grid attachment

        self._bar = Gtk.ProgressBar()
        self._bar.set_show_text(True)
        self._bar.set_fraction(0.0)
        self._bar.set_text(f"{bookCode}")
        self._bar.get_style_context().add_provider(stylep, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        vbox.pack_start(self._bar, False, False, 0)

        self._applyColor(STATUS_PENDING)
        vbox.show_all()

    def _applyColor(self, status):
        self._status = status
        hex_col = _STATUS_DATA.get(status, ("#AAAAAA", ""))[0]
        provider = Gtk.CssProvider()
        lcss = "progressbar trough, progressbar progress {{ background-color: {}; }}"
        provider.load_from_data(lcss.format(hex_col).encode())
        self._bar.get_style_context().add_provider(
            provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

    def _barText(self, page, total, prefix="pg done"):
        t = str(total) if total is not None else "?"
        return f"{self.bookCode}  {prefix} {page}/{t}"

    def _barStatusText(self, msg):
        return f"{self.bookCode}  {msg}"

    def reset(self):
        """Return cell to pending/grey state for a new job."""
        self._hadBadPage = False
        self.firstBadPage = None
        self._total = None
        self._bar.set_fraction(0.0)
        self._bar.set_text(self.bookCode)
        self._applyColor(STATUS_PENDING)

    def update(self, event):
        """Apply a ProgressEvent to this cell. Must be called on GTK main thread."""
        mode = event.mode
        total = event.total if event.total is not None and event.total > 0 else self._total
        page = event.page or 0

        if total is not None:
            self._total = total

        if mode == "probe":
            total = event.total
            frac = (page / total) if total else 0.0
            self._bar.set_fraction(min(frac, 1.0))
            self._bar.set_text(self._barText(page, total, prefix="init"))
            self._applyColor(STATUS_PROBING)

        elif mode == "goodpage" or mode == "page":
            frac = (page / self._total) if self._total else 0.0
            self._bar.set_fraction(min(frac, 1.0))
            self._bar.set_text(self._barText(page, self._total))
            self._applyColor(STATUS_RUNNINGFAILED if self._hadBadPage else STATUS_RUNNING)

        elif mode == "badpage":
            self._hadBadPage = True
            if page and (self.firstBadPage is None or page < self.firstBadPage):
                self.firstBadPage = page
            frac = (page / self._total) if self._total else 0.0
            self._bar.set_fraction(min(frac, 1.0))
            self._bar.set_text(self._barText(page, self._total))
            self._applyColor(STATUS_RUNNINGFAILED if self._hadBadPage else STATUS_RUNNING)

        elif mode == "complete":
            self._bar.set_fraction(1.0)
            if not self._total:
                self._applyColor(STATUS_SKIPPED)
            elif self._hadBadPage or event.total == -1:     # -1: the filler says some pages failed
                self._bar.set_text(self._barStatusText(event.msg or _("Failed")) + f"({self._total})")
                self._applyColor(STATUS_WARNING)
            else:
                self._bar.set_text(self._barStatusText(_("Complete ({self._total})").format(self=self)))
                self._applyColor(STATUS_GOOD)

        elif mode == "failed":
            frac = (page / self._total) if (page and self._total) else self._bar.get_fraction()
            self._bar.set_fraction(frac)
            self._bar.set_text(self._barStatusText(event.msg or _("Failed")))
            self._applyColor(STATUS_FAILED)

        elif mode == "already_filled":
            self._bar.set_fraction(1.0)
            self._bar.set_text(self._barStatusText(_("Already Filled")))
            self._applyColor(STATUS_SKIPPED if not self._total else STATUS_ALREADY_FILLED)

    def finish(self):
        if self._status not in (STATUS_GOOD, STATUS_WARNING, STATUS_FAILED, STATUS_ALREADY_FILLED, STATUS_SKIPPED):
            self._applyColor(STATUS_FAILED)


# ---------------------------------------------------------------------------
# BookProgressDialog
# ---------------------------------------------------------------------------

class BookProgressDialog:
    """Non-modal, persistent window: what Analyse & Fill does, and per-book progress while it runs."""

    COLUMNS = 4

    def __init__(self, parentWindow, view):
        self._cells = {}   # bookCode -> BookProgressCell
        self.view = view
        self.start_time = 0
        self._stopped = False

        self.window = Gtk.Window(title=_("PTXprint: Analyse & Fill"))
        self.window.set_transient_for(parentWindow)
        self.window.set_destroy_with_parent(False)
        self.window.set_deletable(False)
        self.window.connect("delete-event", lambda w, e: (w.hide(), True)[1])

        # Main vertical container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_top(8)
        self.window.add(vbox)

        # Header: what this window is for, and which books it will work on
        intro = Gtk.Label()
        intro.set_markup("<b>" + GLib.markup_escape_text(
                _("Adjusts the spacing of paragraphs so that every page ends full.")) + "</b>")
        intro.set_halign(Gtk.Align.START)
        intro.set_margin_start(8)
        intro.set_margin_end(8)
        vbox.pack_start(intro, False, False, 0)

        self.lb_books = Gtk.Label()
        self.lb_books.set_halign(Gtk.Align.START)
        self.lb_books.set_xalign(0)
        self.lb_books.set_line_wrap(True)
        self.lb_books.set_max_width_chars(60)
        self.lb_books.set_margin_start(8)
        self.lb_books.set_margin_end(8)
        self.lb_books.get_style_context().add_class("dim-label")
        vbox.pack_start(self.lb_books, False, False, 0)

        # Scrolled Window for the grid of progress bars
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        vbox.pack_start(scrolled, False, False, 0)

        self.grid = Gtk.Grid(column_spacing=8, row_spacing=4)
        self.grid.set_margin_start(8)
        self.grid.set_margin_end(8)
        self.grid.set_margin_top(1)
        self.grid.set_margin_bottom(1)
        scrolled.add(self.grid)

        # Colour legend: one chip per group, ⓘ for the full key
        legend = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        legend.set_margin_start(8)
        legend.set_margin_end(8)
        for label, statuses in _LEGEND_GROUPS:
            chip = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            chip.pack_start(self._swatch(_STATUS_DATA[statuses[0]][0], 12, 12), False, False, 0)
            lbl = Gtk.Label(label=_(label))
            chip.pack_start(lbl, False, False, 0)
            chip.set_tooltip_text("\n".join(_(_STATUS_DATA[s][1]) for s in statuses))
            legend.pack_start(chip, False, False, 0)
        key_button = Gtk.Button(label="ⓘ")
        key_button.set_relief(Gtk.ReliefStyle.NONE)
        key_button.set_tooltip_text(_("What each colour means"))
        key_button.connect("clicked", self._onColorKeyClicked)
        legend.pack_end(key_button, False, False, 0)
        vbox.pack_start(legend, False, False, 0)

        vbox.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0)

        # Information area: what the buttons do (when idle), what is happening, or how the run went
        self.lb_info = Gtk.Label()
        self.lb_info.set_halign(Gtk.Align.START)
        self.lb_info.set_valign(Gtk.Align.START)
        self.lb_info.set_xalign(0)
        self.lb_info.set_line_wrap(True)
        self.lb_info.set_max_width_chars(70)
        self.lb_info.set_margin_start(8)
        self.lb_info.set_margin_end(8)
        vbox.pack_start(self.lb_info, True, True, 0)
        self._showIdleInfo()

        # Action area at the bottom: the buttons, safest first, then a footer with Settings and the run status
        button_box = Gtk.ButtonBox(orientation=Gtk.Orientation.HORIZONTAL)
        button_box.set_layout(Gtk.ButtonBoxStyle.CENTER)
        button_box.set_spacing(8)
        button_box.set_margin_start(8)
        button_box.set_margin_end(8)
        vbox.pack_start(button_box, False, False, 0)

        footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        footer.set_margin_start(8)
        footer.set_margin_end(8)
        footer.set_margin_bottom(6)
        vbox.pack_start(footer, False, False, 0)

        resume_tip = _("Fill from the first underfilled page in each book, keeping the adjustments already made.\n\n"
                       "This can take a long time and keeps your processor busy.")
        start_tip = _("Fill each book again from its beginning.\n"
                      "All existing adjustments, including any you made by hand, are thrown away.\n\n"
                      "This can take a long time and keeps your processor busy.")
        self.resume_button = Gtk.Button(label=_("Resume Fill"))
        self.resume_button.set_tooltip_text(resume_tip)
        self.resume_button.connect("clicked", lambda btn: self.view.onResumeFillClicked(btn))
        button_box.add(self.resume_button)

        self.restart_button = Gtk.Button(label=_("Start Fill…"))
        self.restart_button.set_tooltip_text(start_tip)
        self.restart_button.connect("clicked", lambda btn: self.view.onRestartFillClicked(btn))
        button_box.add(self.restart_button)

        # The Stop button (insensitive until a fill is running)
        self.stop_button = Gtk.Button(label=stoplabel)
        self.stop_button.set_sensitive(False)
        self.stop_button.set_tooltip_text(_("Stop after each book's current layout run. The adjustments found so far are kept."))
        self.stop_button.connect("clicked", self.on_stop_clicked)
        button_box.add(self.stop_button)

        # Settings shortcut link
        settings_ebox = Gtk.EventBox()
        settings_lbl = Gtk.Label()
        settings_lbl.set_markup('<span foreground="#1c71d8" underline="single">{}</span>'.format(
                GLib.markup_escape_text(_("Settings"))))
        settings_lbl.set_margin_start(4)
        settings_lbl.set_margin_end(4)
        settings_lbl.set_tooltip_text(_("Open Advanced → Other settings for page filler options"))
        settings_ebox.add(settings_lbl)
        settings_ebox.connect("button-release-event", self._onSettingsClicked)
        footer.pack_start(settings_ebox, False, False, 0)

        # Run status: elapsed (wall-clock) time and the processor time all the workers used
        self.lb_status = Gtk.Label()
        self.lb_status.get_style_context().add_class("dim-label")
        self.lb_status.set_tooltip_text(_("Elapsed: how long this run has taken so far.\n"
            "CPU time: the processor time used by all the parallel workers added together.\n"
            "When it is larger than the elapsed time, several processor cores are sharing the work."))
        footer.pack_end(self.lb_status, False, False, 0)
        self._showStatus(None, None)

        self.stylep = Gtk.CssProvider()
        self.stylep.load_from_data(css)

    @staticmethod
    def _swatch(hexColor, width, height):
        """ A small block of colour, for the legend and the colour key """
        rgba = Gdk.RGBA()
        rgba.parse(hexColor)
        area = Gtk.DrawingArea()
        area.set_size_request(width, height)
        area.set_valign(Gtk.Align.CENTER)
        def draw(w, cr):
            cr.set_source_rgb(rgba.red, rgba.green, rgba.blue)
            cr.rectangle(0, 0, w.get_allocated_width(), w.get_allocated_height())
            cr.fill_preserve()
            cr.set_source_rgba(0, 0, 0, 0.35)
            cr.set_line_width(1)
            cr.stroke()
            return False
        area.connect("draw", draw)
        return area

    def _setInfo(self, markup):
        self.lb_info.set_markup(markup)

    def _showIdleInfo(self):
        b = lambda s: "<b>" + GLib.markup_escape_text(s) + "</b>"
        e = GLib.markup_escape_text
        self._setInfo("\n".join([
            b(_("Resume Fill")) + "  " + e(_("continues from the first underfilled page in each book, "
                                              "keeping the adjustments already made.")),
            b(_("Start Fill…")) + "  " + e(_("starts again from the beginning of each book and "
                                              "throws away all existing adjustments.")),
            "",
            e(_("Filling can take from minutes to hours and keeps your processor busy. "
                "The preview updates when every book is finished."))]))

    def populate(self, bookList: list, running=True):
        """Rebuild cells, for a new run or because the books in What to Print have changed.
           bookList contains 3-letter book codes."""
        # Remove existing children
        for child in self.grid.get_children():
            self.grid.remove(child)
        self._cells.clear()
        self._stopped = False
        self._showStatus(None, None)

        n = len(bookList)
        self.lb_books.set_text(_("No books are selected in What to Print.") if n == 0 else
                (_("1 book from What to Print: {0}") if n == 1 else
                 _("{1} books from What to Print: {0}")).format(" ".join(bookList), n))
        self.setRunning(running and n > 0)
        if n == 0:
            return

        cols = min(self.COLUMNS, n)
        rows = math.ceil(n / cols)

        for i, bk in enumerate(bookList):
            cell = BookProgressCell(bk, self.stylep)
            col = i // rows
            row = i % rows
            self.grid.attach(cell.frame, col, row, 1, 1)
            self._cells[bk] = cell

        logging.log(16, f"populate with {len(self._cells)} cells")
        self.grid.show_all()
        self.start_time = time.time()

        # Compute natural size before showing so we can position without a flash.
        min_w, nat_w = self.window.get_preferred_width()
        min_h, nat_h = self.window.get_preferred_height()
        screen = self.window.get_screen()
        max_h = int(screen.get_height() * 0.85) if screen else 900
        dw, dh = nat_w, max(360, min(nat_h, max_h))
        if self.window.get_visible():
            # refreshed while open (e.g. What to Print changed): grow if needed, but don't jump about
            cw, ch = self.window.get_size()
            self.window.resize(max(cw, dw), max(ch, dh))
        else:
            self.window.resize(dw, dh)
            self._position_with_size(dw, dh)
        self.window.show_all()

    def setRunning(self, running):
        """ While a run is under way only Stop is available """
        self.resume_button.set_sensitive(not running)
        self.restart_button.set_sensitive(not running)
        self.stop_button.set_sensitive(running)
        self.stop_button.set_label(stoplabel)
        if running:
            self._setInfo(GLib.markup_escape_text(_("Filling… Each bar shows how far that book has got. "
                    "The preview updates when every book is finished.")))
        else:
            self._showIdleInfo()

    @staticmethod
    def _hms(secs):
        hours, remainder = divmod(int(secs), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def _showStatus(self, elapsed, cpuSecs):
        """ Show the run's elapsed and CPU times in the footer; None shows a placeholder """
        none = "--:--:--"
        self.lb_status.set_text(_("Elapsed {0}   ·   CPU time {1}").format(
                none if elapsed is None else self._hms(elapsed),
                none if cpuSecs is None else self._hms(cpuSecs)))

    def updateEvent(self, event, cpuSecs=0., elapsed=0.):
        """Route a ProgressEvent to the correct BookProgressCell."""
        if event is not None:
            cell = self._cells.get(event.book)
            if cell is not None:
                cell.update(event)
        if elapsed > 0.:
            self._showStatus(elapsed, cpuSecs)

    def show(self):
        dw, dh = self.window.get_size()
        self._position_with_size(dw, dh)
        self.window.show_all()
        self.window.present()

    def _position_with_size(self, dw, dh):
        try:
            main_win = self.view.builder.get_object("mainapp_win")
            if main_win is None:
                return
            gdk_win = main_win.get_window()
            if gdk_win is None:
                return
            _, wx, wy = gdk_win.get_origin()
            tw = main_win.get_allocated_width()
            th = main_win.get_allocated_height()
            margin = 20
            self.window.move(wx + tw - dw - margin, wy + th - dh - margin)
        except Exception:
            pass

    def hide(self):
        self.window.hide()

    def toggle(self):
        if self.window.get_visible():
            self.hide()
        else:
            self.show()

    def _onSettingsClicked(self, widget, event):
        self.view.highlightwidget('s_pbtimeout')
        self.view.mainapp.win.present()

    def _onColorKeyClicked(self, button):
        """ The full colour key: every status, under the legend group it belongs to """
        pop = Gtk.Popover.new(button)
        pop.set_position(Gtk.PositionType.TOP)
        grid = Gtk.Grid(column_spacing=10, row_spacing=4)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        row_i = 0
        for label, statuses in _LEGEND_GROUPS:
            head = Gtk.Label()
            head.set_markup("<b>" + GLib.markup_escape_text(_(label)) + "</b>")
            head.set_halign(Gtk.Align.START)
            if row_i:
                head.set_margin_top(6)
            grid.attach(head, 0, row_i, 2, 1)
            row_i += 1
            for status in statuses:
                color, msgid = _STATUS_DATA[status]
                lbl = Gtk.Label(label=_(msgid))
                lbl.set_halign(Gtk.Align.START)
                grid.attach(self._swatch(color, 40, 14), 0, row_i, 1, 1)
                grid.attach(lbl, 1, row_i, 1, 1)
                row_i += 1
        grid.show_all()
        pop.add(grid)
        pop.popup()

    def on_stop_clicked(self, button):
        logger.debug("Stop button clicked")
        self._stopped = True
        button.set_sensitive(False)
        button.set_label(_("Stopping..."))
        self.view.onFillCancelled()

    def finished(self):
        for k, v in self._cells.items():
            v.finish()
        stopped = self._stopped
        self.setRunning(False)
        self._showSummary(stopped)

    def _showSummary(self, stopped=False):
        """ Replace the idle text with how the run went """
        cells = list(self._cells.values())
        if not cells:
            return
        e = GLib.markup_escape_text
        done = [c for c in cells if c._status in _DONE_STATUSES]
        check = [c for c in cells if c._status in _CHECK_STATUSES]
        failed = [c for c in cells if c._status not in _DONE_STATUSES + _CHECK_STATUSES]
        lines = []
        if stopped:
            lines.append("<b>" + e(_("Stopped.")) + "</b> " + e(_("The adjustments found so far have been kept; "
                         "Resume Fill carries on from where each book got to.")))
        if len(done) == len(cells):
            lines.append("<b>" + e(_("All {0} books are done.").format(len(cells)) if len(cells) > 1
                                   else _("The book is done.")) + "</b>")
        else:
            lines.append("<b>" + e(_("{0} of {1} books done.").format(len(done), len(cells))) + "</b>")
        if check:
            names = ", ".join(c.bookCode + ("" if c.firstBadPage is None else " " + _("(from p.{0})").format(c.firstBadPage))
                              for c in check)
            lines.append(e(_("To check: {0}").format(names)))
        if failed and not stopped:
            lines.append(e(_("Failed: {0}").format(", ".join(c.bookCode for c in failed))))
        if check or (failed and not stopped):
            lines.append(e(_("Use the previous/next page-with-issues buttons in the preview to find what needs "
                             "attention, then Resume Fill or adjust those pages by hand.")))
        self._setInfo("\n".join(lines))
