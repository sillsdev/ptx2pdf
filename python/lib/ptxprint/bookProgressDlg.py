"""
bookProgressDlg.py — Book Progress Monitor dialog for PTXprint page-fill jobs.

Displays a per-book progress grid updated in real time from ProgressEvent objects
delivered via the existing multiprocessing.Queue / GLib.io_add_watch infrastructure.
"""

import math, logging
from gi.repository import Gtk, Gdk, GLib
from ptxprint.utils import _

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------
STATUS_PENDING = "pending"
STATUS_RUNNING = "running"
STATUS_GOOD    = "good"
STATUS_WARNING = "warning"
STATUS_FAILED  = "failed"

# Colours drawn from report.py logcolors palette
_STATUS_COLORS = {
    STATUS_PENDING: "#AAAAAA",   # grey — not started
    STATUS_RUNNING: "#87CEEB",   # lightskyblue — in progress
    STATUS_GOOD:    "#98FB98",   # palegreen — complete, all OK
    STATUS_WARNING: "#FFA500",   # orange — complete with bad pages
    STATUS_FAILED:  "#FF4500",   # orangered — hard failure
}

stoplabel = _("Stop!")

def _rgba(hex_color):
    """Parse a #RRGGBB hex string into a Gdk.RGBA."""
    r = Gdk.RGBA()
    r.parse(hex_color)
    return r

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
    """Compact 2-line widget: coloured progress bar (with book+page text inside) + message label."""

    def __init__(self, bookCode: str, stylep=None):
        self.bookCode = bookCode
        self._hadBadPage = False
        self._status = STATUS_PENDING
        self._total = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        vbox.set_margin_start(3)
        vbox.set_margin_end(3)
        vbox.set_margin_top(0)
        vbox.set_margin_bottom(0)
        self.frame = vbox   # expose as .frame for grid attachment

        # Progress bar — text inside shows "BOK  p/total"
        self._bar = Gtk.ProgressBar()
        self._bar.set_show_text(True)
        self._bar.set_fraction(0.0)
        self._bar.set_text(f"{bookCode}")
        self._bar.get_style_context().add_provider(stylep, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        vbox.pack_start(self._bar, False, False, 0)

        # Single message label below the bar
        self._msgLabel = Gtk.Label(label="")
        self._msgLabel.set_halign(Gtk.Align.START)
        self._msgLabel.set_ellipsize(3)   # PANGO_ELLIPSIZE_END
        vbox.pack_start(self._msgLabel, False, False, 0)

        self._applyColor(STATUS_PENDING)
        vbox.show_all()

    def _applyColor(self, status):
        self._status = status
        hex_col = _STATUS_COLORS.get(status, "#AAAAAA")
        provider = Gtk.CssProvider()
        lcss = "progressbar trough, progressbar progress {{ background-color: {}; }}"
        provider.load_from_data(lcss.format(hex_col).encode())
        self._bar.get_style_context().add_provider(
            provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

    def _barText(self, page, total, prefix="pg done"):
        t = str(total) if total is not None else "?"
        return f"{self.bookCode}  {prefix} {page}/{t}"

    def reset(self):
        """Return cell to pending/grey state for a new job."""
        self._hadBadPage = False
        self._total = None
        self._bar.set_fraction(0.0)
        self._bar.set_text(self.bookCode)
        self._msgLabel.set_text("")
        self._applyColor(STATUS_PENDING)

    def update(self, event):
        """Apply a ProgressEvent to this cell. Must be called on GTK main thread."""
        mode = event.mode
        page = event.page
        total = event.total

        if total is not None:
            self._total = total

        if mode == "probe":
            total = event.total
            frac = (page / total) if total else 0.0
            self._bar.set_fraction(min(frac, 1.0))
            self._bar.set_text(self._barText(page, total, prefix="init"))
            self._msgLabel.set_text("")
            self._applyColor(STATUS_RUNNING)

        elif mode == "goodpage":
            frac = (page / self._total) if self._total else 0.0
            self._bar.set_fraction(min(frac, 1.0))
            self._bar.set_text(self._barText(page, self._total))
            self._msgLabel.set_text("")
            self._applyColor(STATUS_RUNNING)

        elif mode == "badpage":
            self._hadBadPage = True
            frac = (page / self._total) if self._total else 0.0
            self._bar.set_fraction(min(frac, 1.0))
            self._bar.set_text(self._barText(page, self._total))
            self._msgLabel.set_text(f"pg {page}: bad")
            self._applyColor(STATUS_RUNNING)

        elif mode == "complete":
            self._bar.set_fraction(1.0)
            self._bar.set_text(self._barText(self._total, self._total))
            self._msgLabel.set_text(event.msg or "Complete")
            self._applyColor(STATUS_WARNING if self._hadBadPage else STATUS_GOOD)

        elif mode == "failed":
            frac = (page / self._total) if (page and self._total) else self._bar.get_fraction()
            self._bar.set_fraction(frac)
            self._bar.set_text(self._barText(page, self._total))
            self._msgLabel.set_text(event.msg or "Failed")
            self._applyColor(STATUS_FAILED)

    def finish(self):
        if self._status not in (STATUS_GOOD, STATUS_WARNING, STATUS_FAILED):
            self._applyColor(STATUS_FAILED)


# ---------------------------------------------------------------------------
# BookProgressDialog
# ---------------------------------------------------------------------------

class BookProgressDialog:
    """Non-modal, persistent window showing per-book page-fill progress."""

    COLUMNS = 4

    def __init__(self, parentWindow, view):
        self._cells = {}   # bookCode -> BookProgressCell
        self.view = view

        self.window = Gtk.Window(title="Page Fill Progress")
        self.window.set_transient_for(parentWindow)
        self.window.set_destroy_with_parent(False)
        self.window.set_deletable(False)
        self.window.connect("delete-event", lambda w, e: (w.hide(), True)[1])

        # Main vertical container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.window.add(vbox)

        # Scrolled Window for the grid
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        
        # Pack the scrolled window (expand=True, fill=True)
        vbox.pack_start(scrolled, True, True, 0)

        self.grid = Gtk.Grid(column_spacing=8, row_spacing=4)
        self.grid.set_margin_start(8)
        self.grid.set_margin_end(8)
        self.grid.set_margin_top(1)
        self.grid.set_margin_bottom(1)
        scrolled.add(self.grid)

        # Action area at the bottom
        button_box = Gtk.ButtonBox(orientation=Gtk.Orientation.HORIZONTAL)
        button_box.set_layout(Gtk.ButtonBoxStyle.CENTER)
        button_box.set_spacing(8)
        button_box.set_margin_start(8)
        button_box.set_margin_end(8)
        button_box.set_margin_bottom(8)
        vbox.pack_start(button_box, False, False, 0)

        # Resume Fill and Restart Fill buttons
        resume_tip = _("Resume filling from the first underfilled page in each book.\n\nWarning: CPU-hungry. Go to lunch!")
        restart_tip = _("Restart filling from the beginning of each book.\n\nWarning: CPU-hungry. Go to lunch!")
        self.resume_button = Gtk.Button(label=_("Resume Fill"))
        self.resume_button.set_tooltip_text(resume_tip)
        self.resume_button.connect("clicked", lambda btn: self.view.onResumeFillClicked(btn))
        button_box.add(self.resume_button)

        self.restart_button = Gtk.Button(label=_("Restart Fill"))
        self.restart_button.set_tooltip_text(restart_tip)
        self.restart_button.connect("clicked", lambda btn: self.view.onRestartFillClicked(btn))
        button_box.add(self.restart_button)

        # The Stop button (insensitive until a fill is running)
        self.stop_button = Gtk.Button(label=stoplabel)
        self.stop_button.set_sensitive(False)
        self.stop_button.connect("clicked", self.on_stop_clicked)
        self.stop_button.set_sensitive(False)
        button_box.add(self.stop_button)

        self.stylep = Gtk.CssProvider()
        self.stylep.load_from_data(css)

    def populate(self, bookList: list, stop_sensitive=True):
        """Rebuild cells for a new job. bookList contains 3-letter book codes."""
        # Remove existing children
        for child in self.grid.get_children():
            self.grid.remove(child)
        self._cells.clear()

        n = len(bookList)
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

        self.stop_button.set_sensitive(stop_sensitive)
        self.stop_button.set_label(stoplabel)
        self.grid.show_all()

        # Compute natural size before showing so we can position without a flash.
        min_w, nat_w = self.window.get_preferred_width()
        min_h, nat_h = self.window.get_preferred_height()
        screen = self.window.get_screen()
        max_h = int(screen.get_height() * 0.85) if screen else 900
        dw, dh = nat_w, min(nat_h, max_h)
        self.window.resize(dw, dh)
        self._position_with_size(dw, dh)
        self.window.show_all()

    def updateEvent(self, event):
        """Route a ProgressEvent to the correct BookProgressCell."""
        cell = self._cells.get(event.book)
        print(f"{event.book=} {event.mode=} {event.page=} {event.total=}")

        if cell is not None:
            cell.update(event)

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

    def on_stop_clicked(self, button):
        logger.debug("Stop button clicked")
        button.set_sensitive(False)
        button.set_label(_("Stopping..."))
        self.view.onFillCancelled()

    def finished(self):
        self.stop_button.set_label(stoplabel)
        self.stop_button.set_sensitive(False)
        for k, v in self._cells.items():
            v.finish()
            
