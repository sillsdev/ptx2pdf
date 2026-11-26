""" Context help from the User Manual: F1 opens the manual in the PDF Preview window at the entry for the
    setting under the mouse (or the dialog, group of settings or tab it is in); Ctrl+click on a tab opens
    it at the part about that tab.

    Settings have anchors (named destinations in the PDF) made from their Glade ids (see ctrlAnchor);
    tabs, dialogs and groups of settings are found in a map beside the PDF, made with it by
    python/scripts/uimanual/build_manual.py. Whatever has neither, its parents are tried, out to the window.
"""

import os, re, json, logging
from gi.repository import Gtk, Gdk, GLib
from ptxprint.utils import _, pycodedir

logger = logging.getLogger(__name__)

manualName = "PTXprint-User-Manual.pdf"
helpMapName = "PTXprint-User-Manual-help.json"
mods = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD1_MASK


def manualDir():
    """ Where the manual is: with the other reference PDFs, or (running from the source) where its build puts it """
    d = os.path.join(pycodedir(), "PDFassets", "reference")
    if not os.path.exists(os.path.join(d, manualName)):
        d = os.path.normpath(os.path.join(pycodedir(), "..", "..", "..", "docs", "uimanual", "output"))
    return d


def ctrlAnchor(wid):
    """ A setting's anchor in the manual, as python/scripts/uimanual/htmlmanual.ctrlAnchor makes it """
    return "s-" + re.sub(r"[^A-Za-z0-9]+", "-", wid).strip("-")


def inside(widget, top, x, y, margin=0):
    """ Whether (x, y), relative to the window top, is on widget """
    if not widget.get_mapped():
        return False
    pos = widget.translate_coordinates(top, 0, 0)
    if pos is None:
        return False
    a = widget.get_allocation()
    return pos[0] - margin <= x < pos[0] + a.width + margin and pos[1] - margin <= y < pos[1] + a.height + margin


def pointerIn(top):
    """ Where the mouse is relative to the window top, or None if it is not over it """
    gw = top.get_window()
    if gw is None:
        return None
    seat = gw.get_display().get_default_seat()
    if seat is None or seat.get_pointer() is None:
        return None
    _w, x, y, _m = gw.get_device_position(seat.get_pointer())
    if not (0 <= x < top.get_allocated_width() and 0 <= y < top.get_allocated_height()):
        return None
    return x, y


def tabAt(nb, top, x, y):
    """ The page of the notebook nb whose tab is at (x, y) relative to top, or None """
    for i in range(nb.get_n_pages()):
        page = nb.get_nth_page(i)
        lab = nb.get_tab_label(page)
        if lab is not None and inside(lab, top, x, y, margin=4):
            return page
    return None


class ManualHelp:
    def __init__(self, view):
        self.view = view
        self.helpMap = None
        self.previewGroup = None
        for o in view.builder.get_objects():
            if isinstance(o, Gtk.Window):
                o.connect("key-press-event", self.onKeyPress)
            elif isinstance(o, Gtk.Notebook):
                o.connect("button-press-event", self.onNotebookPress)
                if Gtk.Buildable.get_name(o) != "nbk_PDFviewer":     # (its tabs are the PDFs, not settings)
                    self.addTabHints(o)

    def addTabHints(self, nb):
        """ Says in each tab's tooltip that Ctrl+click opens the manual there """
        hint = _("Ctrl+click: read about this tab in the User Manual.\nF1: help on the setting under the mouse.")
        for i in range(nb.get_n_pages()):
            lab = nb.get_tab_label(nb.get_nth_page(i))
            if lab is None:
                continue
            markup, text = lab.get_tooltip_markup(), lab.get_tooltip_text()
            if markup:
                lab.set_tooltip_markup(markup + "\n\n<i>" + GLib.markup_escape_text(hint) + "</i>")
            elif text:
                lab.set_tooltip_text(text + "\n\n" + hint)
            else:
                lab.set_tooltip_text(hint)

    def loadHelpMap(self):
        if self.helpMap is None:
            self.helpMap = {}
            path = os.path.join(manualDir(), helpMapName)
            try:
                with open(path, encoding="utf-8") as inf:
                    self.helpMap = json.load(inf)
            except (OSError, ValueError) as e:
                logger.warning(f"No help map for the User Manual ({path}): {e}")
        return self.helpMap

    def onKeyPress(self, win, event):
        if event.keyval != Gdk.KEY_F1 or event.state & mods:
            return False
        preview = self.view.builder.get_object("dlg_preview")
        if win is preview and self.view.pdf_viewer.nbook.get_current_page() == self.view.pdf_viewer.boxcodes["manual"]:
            return True             # already reading the manual
        w = self.widgetAt(win) or win.get_focus() or win
        self.openManual(self.parents(w), fromWin=win)
        return True

    def onNotebookPress(self, nb, event):
        """ Ctrl+click on a tab: the tab is shown as usual, and the manual at the part about it """
        if event.type != Gdk.EventType.BUTTON_PRESS or event.button != 1 \
                or (event.state & mods) != Gdk.ModifierType.CONTROL_MASK:
            return False
        top = nb.get_toplevel()
        pos = pointerIn(top)
        page = tabAt(nb, top, *pos) if pos is not None else None
        if page is not None:        # after the click has done its work, so the manual ends up in front
            GLib.idle_add(lambda: self.openManual(self.parents(page), fromWin=top) and False)
        return False

    def widgetAt(self, top):
        """ The innermost widget under the mouse in the window top, or None if the mouse is not over it """
        pos = pointerIn(top)
        if pos is None:
            return None
        x, y = pos
        w = top
        while isinstance(w, Gtk.Container):
            if isinstance(w, Gtk.Notebook):
                page = tabAt(w, top, x, y)
                if page is not None:
                    return page
            kids = []
            w.forall(lambda c, l: l.append(c), kids)
            hits = [c for c in kids if c.get_visible() and inside(c, top, x, y)]
            if not hits:
                break
            w = hits[-1]            # the one on top, where widgets overlap
        return w

    def parents(self, w):
        """ w and the widgets it is in, out to its window: the places to look for help, best first """
        if isinstance(w, Gtk.Label) and w.get_mnemonic_widget() is not None:
            w = w.get_mnemonic_widget()     # a setting's label: the setting
        res = []
        while w is not None:
            res.append(w)
            p = w.get_parent()
            if p is None and isinstance(w, Gtk.Popover):
                p = w.get_relative_to()
            w = p
        return res

    def anchorFor(self, widgets, doc):
        """ The first of widgets that the manual (the Poppler document doc) has a place for: that place's name """
        hmap = self.loadHelpMap()
        for w in widgets:
            name = Gtk.Buildable.get_name(w)
            if not name:
                continue
            for a in (ctrlAnchor(name), hmap.get(name)):
                if a and doc.find_dest(a) is not None:
                    return a
        return None

    def openManual(self, widgets=None, fromWin=None):
        """ Shows the User Manual in the PDF Preview window, at the place about the first of widgets it has one
            for (else where it was), fitted to the window. fromWin: the window asking. Returns whether it could. """
        v = self.view
        manual = os.path.join(manualDir(), manualName)
        if not os.path.exists(manual):
            v.doStatus(_("The User Manual is not installed (make it with python/scripts/uimanual/build_manual.py)"), warning=True)
            return False
        preview = v.builder.get_object("dlg_preview")
        pv = v.pdf_viewer
        mv = pv.viewers[pv.boxcodes["manual"]]
        if mv.document is None or mv.fname != manual:
            pv.loadnshow(manual, widget=preview, tab="manual")
        else:
            pv.selectTab("manual")
        if mv.document is None:
            return False
        anchor = self.anchorFor(widgets, mv.document) if widgets else None
        if fromWin is not None and fromWin is not preview and fromWin.get_modal():
            self.letThrough(preview, fromWin)
        preview.present()
        if anchor is not None:
            mv.gotoNamedDest(anchor)
        mv.fitWhenSized()
        return True

    def letThrough(self, preview, dlg):
        """ A modal dialog (one being run) takes all the input; let the preview window have it too, until the
            dialog closes. Its own window group gets it past GTK's grab, and being modal itself gets it past
            Windows' (which lets every modal window have input). """
        if self.previewGroup is None:
            self.previewGroup = Gtk.WindowGroup()
            self.previewGroup.add_window(preview)
        if preview.get_modal():
            return
        preview.set_modal(True)
        handler = []
        def restore(*a):
            preview.set_modal(False)
            dlg.disconnect(handler[0])
        handler.append(dlg.connect("hide", restore))
