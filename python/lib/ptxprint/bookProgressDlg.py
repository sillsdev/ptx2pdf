"""
bookProgressDlg.py — Book Progress Monitor dialog for PTXprint page-fill jobs.

Displays a per-book progress grid updated in real time from ProgressEvent objects
delivered via the existing multiprocessing.Queue / GLib.io_add_watch infrastructure.
"""

import math
from gi.repository import Gtk, Gdk
from ptxprint.utils import _

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
        min-height: 8px; margin-top: 0px; margin-bottom: 0px;
    }
    progressbar text {
        color: black;
        font-size: 12px; padding-top: 2px; padding-bottom: 0px;
        margin-top: -2px; margin-bottom: -2px;
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

    def _barText(self, page, total, msg=""):
        t = str(total) if total else "?"
        return f"{self.bookCode} {msg} {page}/{t}"

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
            self._bar.set_fraction(0)
            self._bar.set_text(self._barText(page, event.total, msg="init"))
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
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(100) # Increased slightly for better view
        scrolled.set_min_content_width(200)
        
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
        button_box.set_margin_bottom(8)
        vbox.pack_start(button_box, False, False, 0)

        # The Stop button
        self.stop_button = Gtk.Button(label=stoplabel)
        self.stop_button.connect("clicked", self.on_stop_clicked)
        # Optional: Add a CSS class or icon if you want it to look urgent
        # self.stop_button.get_style_context().add_class("destructive-action")
        button_box.add(self.stop_button)

        self.stylep = Gtk.CssProvider()
        self.stylep.load_from_data(css)

        self.window.show_all()

    def populate(self, bookList: list):
        """Rebuild cells for a new job. bookList contains 3-letter book codes."""
        # Remove existing children
        for child in self.grid.get_children():
            self.grid.remove(child)
        self._cells.clear()

        n = len(bookList)
        if n == 0:
            return

        # Adapt column count to book count so small jobs get a compact window
        cols = min(self.COLUMNS, n)
        rows = math.ceil((n + cols - 1) / cols)

        # Size window proportionally — cells are compact (2 lines each)
        cell_w = 180
        cell_h = 46
        self.window.set_default_size(
            cols * cell_w + 24,
            min(rows * cell_h + 24, 500)
        )

        for i, bk in enumerate(bookList):
            cell = BookProgressCell(bk, self.stylep)
            col = i // rows
            row = i % rows
            self.grid.attach(cell.frame, col, row, 1, 1)
            self._cells[bk] = cell

        self.stop_button.set_sensitive("True")
        self.stop_button.set_label(stoplabel)
        self.grid.show_all()

    def updateEvent(self, event):
        """Route a ProgressEvent to the correct BookProgressCell."""
        cell = self._cells.get(event.book)
        if cell is not None:
            cell.update(event)

    def show(self):
        self.window.show_all()
        self.window.present()

    def hide(self):
        self.window.hide()

    def toggle(self):
        if self.window.get_visible():
            self.hide()
        else:
            self.show()

    def on_stop_clicked(self, button):
        print("You pressed THE Button!")
        button.set_sensitive(False)
        button.set_label(_("Stopping..."))
        self.view.onFillCancelled()

