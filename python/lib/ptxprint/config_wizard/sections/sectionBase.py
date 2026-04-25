import logging
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

logger = logging.getLogger(__name__)


def makeLabel(text, bold=False, dim=False, wrap=True, xalign=0.0):
    lbl = Gtk.Label()
    lbl.set_xalign(xalign)
    lbl.set_line_wrap(wrap)
    if bold:
        lbl.set_markup(f"<b>{GLib_escape(text)}</b>")
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


def makeCombo(items):
    """items: list of (id, label) tuples."""
    cb = Gtk.ComboBoxText()
    for item_id, item_label in items:
        cb.append(item_id, item_label)
    cb.set_valign(Gtk.Align.CENTER)
    cb.set_hexpand(True)
    cb.show()
    return cb


def makeSpinner(val, lo, hi, step=1.0, digits=0):
    adj = Gtk.Adjustment(value=val, lower=lo, upper=hi,
                         step_increment=step, page_increment=step * 10)
    sp = Gtk.SpinButton(adjustment=adj, climb_rate=1.0, digits=digits)
    sp.set_valign(Gtk.Align.CENTER)
    sp.set_numeric(True)
    sp.show()
    return sp


def makeFrame(labelText=None, child=None):
    fr = Gtk.Frame()
    if labelText:
        fr.set_label(labelText)
    if child:
        fr.add(child)
    fr.show()
    return fr


def makeSectionTitle(text):
    lbl = Gtk.Label()
    lbl.set_markup(f"<b><big>{text}</big></b>")
    lbl.set_xalign(0.0)
    lbl.set_margin_bottom(8)
    lbl.show()
    return lbl


def makeInfoRow(labelText, widget, infoText=None):
    """Return a Gtk.Box row with label + widget + optional ⓘ expander."""
    row = makeVBox(spacing=2)
    hbox = makeHBox(spacing=8)

    lbl = Gtk.Label(label=labelText)
    lbl.set_xalign(0.0)
    lbl.set_hexpand(True)
    lbl.show()
    hbox.pack_start(lbl, True, True, 0)
    hbox.pack_start(widget, False, False, 0)

    if infoText:
        infoBtn = Gtk.Button(label="ⓘ")
        infoBtn.set_relief(Gtk.ReliefStyle.NONE)
        infoBtn.set_valign(Gtk.Align.CENTER)
        infoBtn.show()

        infoLbl = Gtk.Label(label=infoText)
        infoLbl.set_xalign(0.0)
        infoLbl.set_line_wrap(True)
        infoLbl.get_style_context().add_class("dim-label")
        infoLbl.show()

        revealer = Gtk.Revealer()
        revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
        revealer.set_reveal_child(False)
        revealer.add(infoLbl)
        revealer.show()

        infoBtn.connect("clicked", lambda _b, rv=revealer: rv.set_reveal_child(not rv.get_reveal_child()))
        hbox.pack_start(infoBtn, False, False, 0)
        row.pack_start(hbox, False, False, 0)
        row.pack_start(revealer, False, False, 0)
    else:
        row.pack_start(hbox, False, False, 0)

    row.show()
    return row


def GLib_escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class SectionPanel(Gtk.Box):
    """Abstract base for all wizard section panels."""

    sectionId: str = "base"

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_margin_start(16)
        self.set_margin_end(16)
        self.set_margin_top(12)
        self.set_margin_bottom(12)
        self._stateChangedCb = None
        self._loading = False
        self._buildUi()
        self.show()

    def setStateChangedCallback(self, cb):
        self._stateChangedCb = cb

    def _emitStateChanged(self):
        if not self._loading and self._stateChangedCb:
            self._stateChangedCb(self.sectionId)

    def _buildUi(self):
        """Override to build the section's widget tree."""
        pass

    def loadFromState(self, state) -> None:
        """Populate widgets from WizardState. Override in subclasses."""
        pass

    def saveToState(self, state) -> None:
        """Write widget values back into WizardState. Override in subclasses."""
        pass

    def onConstraintsChanged(self, engine, flat) -> None:
        """Refresh allowed values / sensitive states. Override in subclasses."""
        pass

    def isComplete(self) -> bool:
        """Return True when all required fields are filled. Override in subclasses."""
        return False
