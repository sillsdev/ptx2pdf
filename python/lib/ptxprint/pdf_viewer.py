import gi, os, datetime, ctypes, math
gi.require_version("Gtk", "3.0")
gi.require_version("Poppler", "0.18")
from gi.repository import Gtk, Poppler, GdkPixbuf, Gdk, GLib, Pango
import cairo, re, time, sys
import numpy as np
from cairo import ImageSurface, Context
from colorsys import rgb_to_hsv, hsv_to_rgb
from ptxprint.utils import _, f2s, coltoonemax, getcaller
from ptxprint.piclist import Piclist
from ptxprint.gtkpiclist import PicList
from ptxprint.parlocs import Paragraphs, ParInfo, FigInfo
from ptxprint.xdv.spacing_oddities import SpacingOddities
from pathlib import Path
from typing import Optional
from threading import Timer
import logging

# These libs are for Windows-only functionality to make 
# Paratext+Logos scroll to a Book ch:vs reference
if sys.platform.startswith("win"):
    import winreg
    import ctypes
    from ctypes import wintypes
    
logger = logging.getLogger(__name__)

reset  = {'para': _("Paragraph"), 'col': _("Column"), 'page': _("Page"), 'sprd': _("Spread")}
frame  = {'col': _("Column"), 'span': _("Span"), 'page': _("Page"), 'full': _("Full")}  # 'cut': _("Cutout"), 
mirror = {'': _("Never"), 'both': _("Always"), 'odd': _("If on odd page"), 'even': _("If on even page")}
vpos   = {'t': _("Top"), '-': _("Center"), 'b': _("Bottom"), 'h': _("Before Verse"), 'p': _("After Paragraph"), 'c': _("Cutout"), 'B': _("Below Notes")}
hpos   = {'l': _("Left"), 'c': _("Center"), 'r': _("Right"), 'i': _("Inner"), 'o': _("Outer"), '-': _("Unspecified")}

rev_reset  = {v:k for k, v in reset.items()}
rev_frame  = {v:k for k, v in frame.items()}
rev_mirror = {v:k for k, v in mirror.items()}
rev_vpos   = {v:k for k, v in vpos.items()}
rev_hpos   = {v:k for k, v in hpos.items()}

dsplyOpts = {'col':  ('tbhpc', 'lrio-'), 
             'span': ('tbB',''),
             'page': ('t-b','lcrio-'),
             'full': ('t-b','lcrio-')    }

mstr = {
    'sstm':       _("SpeedSlice"),  # Not yet ™
    'yesminus':   _("Yes! Shrink -1 line"),
    'tryminus':   _("Try Shrink -1 line"),
    'plusline':   _("Expand +1 line"),
    'rp':         _("Reset Adjustments"),
    'shrnkboth':  _("Shrink -1 line and Text"),
    'st':         _("Shrink Text"),
    'et':         _("Expand Text"),
    'es':         _("Edit Style"),
    'ecs':        _("Edit Caption Style"),
    'j2pt':       _("Send Ref to Paratext"),
    'z2f':        _("Zoom to Fit"),
    'z100':       _("Zoom 100%"),
    'ancrdat':    _("Anchored at:"),
    'ianf':       _("Image Anchor Not Found"),
    'cnganc':     _("Change Anchor Ref"),
    'frmsz':      _("Frame Size"),
    'vpos':       _("Vertical Position"),
    'hpos':       _("Horizontal Position"),
    'mirror':     _("Mirror Picture"),
    'shrinkpic':  _("Shrink by 1 line"),
    'growpic':    _("Grow by 1 line"),
    'shwdtl':     _("Show Details..."),
}

def mm_pts(n):
    return n * 72.27 / 25.4

def render_page_image(page, zoomlevel, pnum, annotatefns):
    width, height = page.get_size()
    width, height = int(width * zoomlevel), int(height * zoomlevel)
    buf = bytearray(width * height * 4)
    render_page(page, zoomlevel, buf, pnum, annotatefns)
    return arrayImage(buf, width, height)

def render_page(page, zoomlevel, imarray, pnum, annotatefns):
    # Get page size, applying zoom factor
    width, height = page.get_size()
    width, height = width * zoomlevel, height * zoomlevel

    surface = ImageSurface.create_for_data(memoryview(imarray), cairo.FORMAT_ARGB32, int(width), int(height))
    context = Context(surface)
    context.set_source_rgb(1, 1, 1)
    context.paint()
    context.scale(zoomlevel, zoomlevel)
    page.render(context)
    for f in annotatefns:
        f(page, pnum, context, zoomlevel)

def arrayImage(imarray, width, height):
    stride = cairo.Format.ARGB32.stride_for_width(width)
    if sys.byteorder == "little":       # vs "big"
        # a pixbuf assumes data comes as uint32s (or uint24s) not byte arrays.
        # cairo stores data in effect in big endian order
        # using new_from_bytes() makes no difference
        myarray = np.frombuffer(imarray, dtype=np.uint8)
        myarray = myarray.reshape(-1, 4)
        myarray[:, [0, 2]] = myarray[:, [2, 0]]
    pixbuf = GdkPixbuf.Pixbuf.new_from_data(
        bytes(imarray),
        GdkPixbuf.Colorspace.RGB,
        True,
        8,
        width, height, stride)
    return Gtk.Image.new_from_pixbuf(pixbuf)


class PDFViewer:
    boxcodes = {v: i for i, v in enumerate("""content cover diff manual""".split())}
    boxnames = ["bx_previewPDF", "bx_previewCover", "bx_previewDiff", "bx_previewManual"]

    def __init__(self, model, nbook, tv):
        self.model = model
        self.nbook = nbook
        self.lastpage = 0
        nbook.connect("notify::page", self.onPageChanged)
        self.viewers = []
        for k in self.boxnames:
            w = model.builder.get_object(k)
            self.viewers.append(PDFContentViewer(model, w, tv) if k == "bx_previewPDF" else PDFFileViewer(model, w))
        self.hide_unused()

    def _currview(self):
        curr = self.nbook.get_current_page()
        return self.viewers[curr]

    def __getattr__(self, name, default=None):
        v = self._currview()
        if hasattr(v, name):
            return getattr(self._currview(), name)
        v = self.__dict__.get('views', None)
        if v is None or not len(v):
            return default
        if hasattr(self.__dict__['views'][0], name):
            return getattr(self.__dict__['views'][0], name)
        return default

    def set(self, name, val):
        v = self._currview()
        # print(f"viewer page={self.nbook.get_current_page()}: {name}={val}")
        if hasattr(v, name):
            setattr(v, name, val)
        elif hasattr(self.views[0], name):
            setattr(self.views[0], name, val)
        else:
            raise AttributeError(f"No attribute {name} setting to {val}")

    def onTabChange(self, p):
        # called before the page is changed
        self.lastpage = self.nbook.get_current_page()
        
    def selectTab(self, name):
        i = self.boxcodes.get(name, None)
        if i is not None and i < len(self.viewers) and self.viewers[i] is not None:
            self.nbook.set_current_page(i)

    def onPageChanged(self, widget, pspec):
        # called after the page is changed
        p = self.nbook.get_current_page()
        page = self.viewers[p].current_index
        self.model.set("t_pgNum", str(page), mod=False)
        z = self.viewers[p].zoomLevel
        self.model.set("s_pdfZoomLevel", str(z*100), mod=False)
        self.model.set_preview_pages(self.numpages, _("Pages:"))

    def loadnshow(self, fname, tab=None, extras={}, **kw):
        fbits = os.path.splitext(fname) if fname is not None else None
        if tab is None:
            for i, a in enumerate(("{}{}", "{}_cover{}", "{}_diff{}")):
                if fbits is not None:
                    fpath = a.format(*fbits)
                v = self.nbook.get_nth_page(i)
                if fbits is not None and os.path.exists(fpath):
                    self.viewers[i].loadnshow(fpath, **kw)
                    v.show()
                    self.nbook.set_current_page(0)
                else:
                    v.hide()
            for k, v in sorted(extras.items()):
                n = k.strip()
                if n not in self.boxcodes:
                    i = len(self.boxcodes)
                    self.boxcodes[n] = i
                    self.boxnames.append("bx_preview{}".format(n))
                    if i >= self.nbook.get_n_pages():
                        b = Gtk.Box()
                        b.set_halign(Gtk.Align.CENTER)
                        b.set_valign(Gtk.Align.CENTER)
                        b.set_hexpand(True)
                        b.set_vexpand(True)
                        sc = Gtk.ScrolledWindow()
                        sc.set_shadow_type(Gtk.ShadowType.IN)
                        sc.set_propagate_natural_height(True)
                        sc.get_style_context().add_class("graybox")
                        sc.add_with_viewport(b)
                        tab = Gtk.Label(n)
                        tab.set_angle(270)
                        self.viewers.append(PDFFileViewer(self.model, b, alloc=self.nbook.get_nth_page(0).get_allocation()))
                        self.nbook.append_page(sc, tab)
                else:
                    i = self.boxcodes[n]
                self.viewers[i].loadnshow(v, **kw)
                t = self.nbook.get_nth_page(i)
                t.show()
        elif fname is not None and os.path.exists(fname):
            i = self.boxcodes[tab]
            v = self.nbook.get_nth_page(i)
            self.viewers[i].loadnshow(fname, **kw)
            v.show()
            self.nbook.set_current_page(i)
        self.hide_unused()

    def hide_unused(self):
        for i in range(1, self.nbook.get_n_pages()):
            if i >= len(self.viewers) or self.viewers[i].document is None:
                v = self.nbook.get_nth_page(i)
                v.hide()

    def clear(self, widget=None, view=None, remove=False):
        if view is None:
            viewIDs = range(len(self.viewers))
        else:
            viewIDs = [self.boxcodes.get(view, None)]
        for i in viewIDs:
            if i is None:
                continue
            v = self.viewers[i]
            if v is not None:
                v.clear(widget=widget)
                if remove:
                    t = self.nbook.get_nth_page(i)
                    t.hide()

    def settingsChanged(self):
        self.viewers[0].settingsChanged()


class PDFFileViewer:
    def __init__(self, model, widget, alloc=None): # widget is bx_previewPDF (which will have 2x .hbox L/R pages inside it)
        self.hbox = widget
        self.model = model      # a view/gtkview
        self.sw = widget.get_parent()
        self.sw.connect("button-press-event", self.on_button_press)
        self.sw.connect("button-release-event", self.on_button_release)
        self.sw.connect("motion-notify-event", self.on_mouse_motion)
        self.sw.connect("scroll-event", self.on_scroll_parent_event) # outer box (not the pages)
        
        self.swh = self.sw.get_hadjustment()
        self.swv = self.sw.get_vadjustment()
        self.numpages = 0
        self.document = None
        self.fname = None
        self.current_page = None    # current folio page number
        self.current_index = None   # current pdf page index starts at 1
        self.zoomLevel = 1.0        # Initial zoom level is 100%
        self.old_zoom = 1.0
        self.spread_mode = False    # self.model.get("c_bkView", False)
        self.psize = (0, 0)
        self.piczoom = 85
        self.rtl_mode = False
        self.widget = None
        self.timer = None
        self.is_dragging = False

        # Enable focus and event handling
        self.hbox.set_can_focus(True)
        self.hbox.add_events(Gdk.EventMask.SCROLL_MASK | Gdk.EventMask.BUTTON_PRESS_MASK)

        # Connect keyboard events
        self.hbox.connect("key-press-event", self.on_key_press_event)
        self.hbox.connect("scroll-event", self.on_scroll_event)
        self.hbox.set_can_focus(True)  # Ensure the widget can receive keyboard focus
        if alloc is not None:
            self.sw.set_allocation(alloc)
            self.hbox.set_allocation(alloc)

    def create_boxes(self, num):
        boxes = self.hbox.get_children()
        if len(boxes) == num:
            return
        elif len(boxes) > num:
            for c in boxes[num:]:
                self.hbox.remove(c)
        elif len(boxes) < num:
            while len(boxes) < num: 
                event_box = Gtk.EventBox()
                event_box.set_events(Gdk.EventMask.SCROLL_MASK |
                                     Gdk.EventMask.BUTTON_PRESS_MASK |
                                     Gdk.EventMask.BUTTON_RELEASE_MASK |
                                     Gdk.EventMask.POINTER_MOTION_MASK)
                
                event_box.connect("scroll-event", self.on_scroll_event)
                event_box.connect("button-release-event", self.on_button_release)
                if self.rtl_mode:
                    self.hbox.pack_end(event_box, False, False, 1)
                else:
                    self.hbox.pack_start(event_box, False, False, 1)
                boxes.append(event_box)

    def update_boxes(self, images, index=0):
        self.hbox.hide()
        children = self.hbox.get_children()
        for i,c in enumerate(children):
            if i >= len(images):
                break
            im = images[i]
            for oldim in c.get_children():     # only 1 child (in theory)
                oldim.destroy()                # removes from parent
            c.add(im)
            im.show()
            c.show()
        self.hbox.show()
        self.hbox.grab_focus()

    def load_pdf(self, pdf_path, **kw):
        if pdf_path is not None and os.path.exists(pdf_path):
            logger.debug(f"Loading pdf: {pdf_path}")
            file_uri = Path(pdf_path).as_uri()
            try:
                self.document = Poppler.Document.new_from_file(file_uri, None)
                self.numpages = self.document.get_n_pages()
            except Exception as e:
                self.model.doStatus(_("Error opening PDF: ").format(e))
                self.document = None
                return False
            self.hbox.show()
        else:
            self.hbox.hide()
        return True

    def show_pdf(self, cpage=None, rtl=False, setpnum=True):
        """ cpage is a index (1 based) """
        if self.document is None:
            self.clear()
            return
        if cpage is None:
            cpage = self.current_index or 1
        page = cpage
        images = []
        if cpage in range(self.numpages+1):
            self.create_boxes(1)
            pg = self.document.get_page(cpage-1)
            self.psize = pg.get_size()
            images.append(render_page_image(pg, self.zoomLevel, cpage, []))
        else:
            pg = None

        self.current_page = page
        self.current_index = cpage
        if setpnum and str(page) != self.model.get("t_pgNum"):
            self.model.set("t_pgNum", str(page), mod=False)
        self.update_boxes(images)
        self.updatePageNavigation()
        return pg

    def loadnshow(self, fname, rtl=False, widget=None, page=None, hook=None, **kw):
        self.rtl_mode = rtl
        if fname is None:
            fname = self.fname
        else:
            self.fname = fname
        if fname is None:
            return False
        if not self.load_pdf(fname, **kw):
            return False
        if hook is not None:
            hook(self)
        self.show_pdf(rtl=rtl)
        pdft = os.stat(fname).st_mtime
        mod_time = datetime.datetime.fromtimestamp(pdft)
        formatted_time = mod_time.strftime("   %d-%b %H:%M")
        if widget is None:
            widget = self.widget
        self.widget = widget
        if widget is not None:
            widget.set_title(_("PDF Preview 3.0.0") + "   " + os.path.basename(self.fname) + formatted_time)
        self.model.set_preview_pages(self.numpages, _("Pages:"))
        self.widget.show_all()
        self.set_zoom_fit_to_screen(None)
        self.updatePageNavigation()
        return True

    def clear(self, widget=None):
        self.create_boxes(0)
        self.document = None
        if widget is not None:
            widget.set_title(_("PDF Preview:"))

    def minmaxnumpages(self):
        rmin = 0
        rmax = self.document.get_n_pages() if self.document else 0
        return (rmin, rmax, rmax)

    def getpnum(self, n, d):
        return n

    def closestpnum(self, pg):
        return pg

    def seekUFpage(self, direction):
        pass

    def set_zoom(self, zoomLevel, scrolled=False, setz=True):
        if math.fabs(zoomLevel - self.zoomLevel) < 0.01:
            return
        if setz and self.model.get("s_pdfZoomLevel") != str(int(zoomLevel * 100)):
            self.zoomLevel = zoomLevel
            self.model.set("s_pdfZoomLevel", zoomLevel*100, mod=False)
        self.old_zoom = self.zoomLevel
        self.zoomLevel = zoomLevel
        width, height = self.psize
        width, height = int(width * self.zoomLevel), int(height * self.zoomLevel)

        children = self.hbox.get_children()
        if not len(children):
            return self.show_pdf()

        if scrolled:
            images = []
            for i,c in enumerate(children):
                im = c.get_children()[0]
                pbuf = im.get_pixbuf()
                np = pbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
                nim = Gtk.Image.new_from_pixbuf(np)
                images.append(nim)
            self.update_boxes(images)

        def redraw():
            self.show_pdf()

        if self.timer is not None:
            GLib.source_remove(self.timer)
        if scrolled:
            self.timer = GLib.timeout_add(300, redraw)
        else:
            self.show_pdf()

    def on_scroll_parent_event(self, widget, event):
        ctrl_pressed = event.state & Gdk.ModifierType.CONTROL_MASK
        if ctrl_pressed:
            return False 
        if event.direction == Gdk.ScrollDirection.SMOOTH:
            _, _, z = event.get_scroll_deltas()
            if z < 0:
                self.set_page(self.swap4rtl("previous"))
            elif z > 0:
                self.set_page(self.swap4rtl("next"))
        elif event.direction == Gdk.ScrollDirection.UP:
            self.set_page(self.swap4rtl("previous"))
        elif event.direction == Gdk.ScrollDirection.DOWN:
            self.set_page(self.swap4rtl("next"))
        return True

    def on_scroll_event(self, widget, event):
        ctrl_pressed = event.state & Gdk.ModifierType.CONTROL_MASK

        if ctrl_pressed:  # Zooming with Ctrl + Scroll
            zoom_in = event.direction == Gdk.ScrollDirection.UP
            zoom_out = event.direction == Gdk.ScrollDirection.DOWN

            # Get mouse position relative to the widget
            mouse_x, mouse_y = event.x, event.y
            posn = self.widgetPosition(widget) # 0=left page; 1=right page

            if zoom_in:
                self.zoom_at_point(mouse_x, mouse_y, posn, zoom_in=True)
            elif zoom_out:
                self.zoom_at_point(mouse_x, mouse_y, posn, zoom_in=False)

            return True  # Prevent further handling of the scroll event

        # Get the parent scrolled window and its adjustments
        scrolled_window = self.hbox.get_parent()
        v_adjustment = scrolled_window.get_vadjustment()
        if v_adjustment.get_upper() > v_adjustment.get_page_size():
            return False # v_adjustment is active
        else:
            # Default behavior: Scroll for navigation
            if event.direction == Gdk.ScrollDirection.UP:
                self.set_page(self.swap4rtl("previous"))
            elif event.direction == Gdk.ScrollDirection.DOWN:
                self.set_page(self.swap4rtl("next"))
            return True

        return False

    def widgetPosition(self, widget):
        children = self.hbox.get_children()
        for index, child in enumerate(children):
            if child == widget:
                return index  # Return the position (index) of the widget
        return -1  # If widget is not found, return -1

    def zoom_at_point(self, mouse_x, mouse_y, posn, zoom_in):
        self.old_zoom = self.zoomLevel
        zoomLevel = (min(self.zoomLevel * 1.1, 8.0) if zoom_in else max(self.zoomLevel * 0.9, 0.3))
        scale_factor = zoomLevel / self.old_zoom

        self.set_zoom(zoomLevel, scrolled=True)
        scrolled_window = self.hbox.get_parent()
        h_adjustment = scrolled_window.get_hadjustment()
        v_adjustment = scrolled_window.get_vadjustment()
        h_value = h_adjustment.get_value() if h_adjustment else 0
        v_value = v_adjustment.get_value() if v_adjustment else 0

        hbox_width  = self.hbox.get_allocated_width()
        page_width  = hbox_width / 2 if self.spread_mode else hbox_width
        page_offset = (posn * page_width)
        
        new_h_value = (scale_factor - 1) * (mouse_x + page_offset) + h_value 
        new_v_value = (scale_factor - 1) *  mouse_y                + v_value
        h_adjustment.set_upper(h_adjustment.get_upper() * scale_factor)
        v_adjustment.set_upper(v_adjustment.get_upper() * scale_factor)
        h_adjustment.set_value(new_h_value)
        v_adjustment.set_value(new_v_value)

        # Redraw the canvas with the updated zoom level

    # Handle keyboard shortcuts for navigation
    def on_key_press_event(self, widget, event):
        keyval = event.keyval
        state = event.state
        # Check if Control key is pressed
        ctrl = (state & Gdk.ModifierType.CONTROL_MASK)

        if ctrl and keyval == Gdk.KEY_Home:  # Ctrl+Home (Go to first page)
            self.set_page(self.swap4rtl("first"))
            return True
        elif ctrl and keyval == Gdk.KEY_End:  # Ctrl+End (Go to last page)
            self.set_page(self.swap4rtl("last"))
            return True
        elif keyval == Gdk.KEY_Page_Down:  # Page Down (Next page/spread)
            self.set_page(self.swap4rtl("next"))
            return True
        elif keyval == Gdk.KEY_Page_Up:  # Page Up (Previous page/spread)
            self.set_page(self.swap4rtl("previous"))
            return True
        elif ctrl and keyval in {Gdk.KEY_equal, Gdk.KEY_plus}:  # Ctrl+Plus (Zoom In)
            self.on_zoom_in(widget)
            return True
        elif ctrl and keyval in {Gdk.KEY_minus, Gdk.KEY_underscore}:  # Ctrl+Minus (Zoom Out)
            self.on_zoom_out(widget)
            return True
        elif ctrl and keyval == Gdk.KEY_0:  # Ctrl+Zero (Reset Zoom)
            self.on_reset_zoom(widget)
            return True
        elif ctrl and keyval == Gdk.KEY_1:  # Ctrl+1 (Actual size, 100%)
            self.set_zoom(1.0)
            return True
        elif ctrl and keyval in {Gdk.KEY_F, Gdk.KEY_f}:  # Ctrl+F (Fit to screen)
            self.set_zoom_fit_to_screen(None)
            self.show_pdf()  # Redraw the current page
            return True
        elif keyval == Gdk.KEY_Right:  # Right arrow → Next page
            self.set_page(self.swap4rtl("next"))
            return True
        elif keyval == Gdk.KEY_Left:  # Left arrow → Previous page
            self.set_page(self.swap4rtl("previous"))
            return True
            
    def updatePageNavigation(self):
        """Update button sensitivity and tooltips dynamically based on the current index."""
        is_rtl = self.rtl_mode and self.model.lang != 'ar_SA'
        pg = self.current_index or 1
        num_pages = self.numpages

        # Enable or disable navigation buttons based on position
        if is_rtl:
            self.model.builder.get_object("btn_page_first").set_sensitive(pg < num_pages)
            self.model.builder.get_object("btn_page_previous").set_sensitive(pg < num_pages)
            self.model.builder.get_object("btn_page_last").set_sensitive(pg > 1)
            self.model.builder.get_object("btn_page_next").set_sensitive(pg > 1)
        else:
            self.model.builder.get_object("btn_page_first").set_sensitive(pg > 1)
            self.model.builder.get_object("btn_page_previous").set_sensitive(pg > 1)
            self.model.builder.get_object("btn_page_last").set_sensitive(pg < num_pages)
            self.model.builder.get_object("btn_page_next").set_sensitive(pg < num_pages)

        seekPrevBtn = self.model.builder.get_object("btn_seekPage2fill_previous")
        seekNextBtn = self.model.builder.get_object("btn_seekPage2fill_next")
        seekPrevBtn.set_sensitive(False)
        seekNextBtn.set_sensitive(False)

    def on_button_press(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 2:  # Button 2 = Middle Mouse Button
            self.on_update_pdf(None)
            return
        if event.button == 2:
            self.is_dragging = True
            self.mouse_start_x = event.x_root
            self.mouse_start_y = event.y_root
            return True

    def on_mouse_motion(self, widget, event):
        if self.is_dragging:
            mh = (self.mouse_start_x - event.x_root)
            mv = (self.mouse_start_y - event.y_root)
            self.mouse_start_x = event.x_root
            self.mouse_start_y = event.y_root
            self.swh.set_value(self.swh.get_value() + mh)
            self.swv.set_value(self.swv.get_value() + mv)
            return True

    def on_button_release(self, widget, event):
        if event.button == 2:   # middle click
            self.is_dragging = False
        if event.button == 3:  # Right-click (for context menu)
            self.show_context_menu(widget, event)
        return True

    def show_context_menu(self, widget, event):
        pass

    # Zoom functionality
    def on_zoom_in(self, widget):
        if self.zoomLevel < 2.0:
            zoomLevel = (1.2 * self.zoomLevel)  # Increase zoom by 20% of current level
        elif self.zoomLevel < 5.0:
            zoomLevel = (1.5 * self.zoomLevel)  # Increase zoom by 50% of current level
        elif self.zoomLevel < 8.0:
            zoomLevel = min(self.zoomLevel * 2, 8.0)  # Double zoom, cap at 8.0
        else:
            zoomLevel = 8.0  # Ensure max zoom is 8.0
        self.set_zoom(zoomLevel)

    def on_reset_zoom(self, widget):
        self.set_zoom(1.0)

    def on_zoom_out(self, widget):
        min_zoom = 0.3  # Set a minimum zoom level of 30%
        if self.zoomLevel > 5.0:
            zoomLevel = max(self.zoomLevel / 2, 5.0)  # Halve zoom, cap at 5.0
        elif self.zoomLevel > 2.0:
            zoomLevel = (0.5 * self.zoomLevel)  # Decrease zoom by 50% of current level
        elif self.zoomLevel > min_zoom:
            zoomLevel = (0.8 * self.zoomLevel)  # Decrease zoom by 20% of current level
            if self.zoomLevel < min_zoom:
                zoomLevel = min_zoom  # Prevent going below 0.3
        else:
            zoomLevel = min_zoom  # Ensure minimum zoom is 0.3
        self.set_zoom(zoomLevel)

    def on_window_size_allocate(self, widget, allocation):
        if self.current_page is None:
            return
        self.set_zoom_fit_to_screen(None)

    def set_zoom_fit_to_screen(self, x):
        if not hasattr(self, "document") or self.document is None or self.current_page is None:
            return
        page = self.document.get_page(self.current_page - 1)
        try:
            page_width, page_height = page.get_size()
        except AttributeError:
            return

        parent_widget = self.hbox.get_parent() # .get_parent()
        if parent_widget is not None:
            alloc = parent_widget.get_allocation()
            scale_x = (alloc.width + 0) / (page_width * (2 if self.spread_mode else 1))
            scale_y = (alloc.height + 0) / page_height
            self.set_zoom(min(scale_x, scale_y))

    def set_page(self, action):
        if self.current_index is None:
            return
        increment = 2 if self.spread_mode and self.current_page % 2 == 1 else 1
        pg = min(self.current_index, self.numpages)
        try:
            if action == self.swap4rtl("first"):
                pg = 1
            elif action == self.swap4rtl("last"):
                pg = self.numpages
            elif action == self.swap4rtl("next"):
                pg = min(pg + increment, self.numpages)
            elif action == self.swap4rtl("previous"):
                pg = max(pg - increment, 1)
            else:
                logger.error(f"Unknown action: {action}")
                return
        except IndexError:
            pg = 1
        logger.debug(f"page {pg=} {self.current_page=}")
        self.show_pdf(pg)
    
    def swap4rtl(self, action):
        # Only swap the buttons for RTL if we're NOT in Arabic UI mode
        if (self.rtl_mode or False) and self.model.lang != 'ar_SA':
            if action == _('first'):
                return _('last')
            elif action == _('last'):
                return _('first')
            elif action == _('next'):
                return _('previous')
            elif action == _('previous'):
                return _('next')
            else:
                return action
        else:
            return action

    def print_document(self, fitToPage=False):
        if not hasattr(self, 'document') or self.document is None:
            return
        self.fitToPage = fitToPage
        print_op = Gtk.PrintOperation()
        if self.model.userconfig.has_section('printer'):
            settings = print_op.get_print_settings()
            if settings is not None and settings.get("printer") == self.model.userconfig.get("printer", "printer"):
                for k, v in self.model.userconfig.items('printer'):
                    settings.set(k, v)
                print_op.set_print_settings(settings)
        print_op.set_n_pages(self.numpages)
        print_op.connect("draw_page", self.on_draw_page)

        try:
            result = print_op.run(Gtk.PrintOperationAction.PRINT_DIALOG, None)
        except Exception as e:
            self.model.doStatus(_("An error occurred while printing: ").format(e))
        if result == Gtk.PrintOperationResult.APPLY:
            self.model.doStatus(_("Print job sent to printer."))
            if not self.model.userconfig.has_section("printer"):
                self.model.userconfig.add_section("printer")
            settings = print_op.get_print_settings()
            settings.foreach(self._saveSetting)
        else:
            self.model.doStatus(_("Print job canceled or failed."))

    def on_draw_page(self, operation, context, page_number):
        if not getattr(self, 'document', None):
            return

        pdf_page = self.document.get_page(page_number)

        cairo_context = context.get_cairo_context()
        cairo_context.save()
        cairo_context.set_source_rgb(1, 1, 1)
        cairo_context.paint()

        pdf_width, pdf_height = pdf_page.get_size()
        paper_width = context.get_width()
        paper_height = context.get_height()

        dpi_x = context.get_dpi_x()
        dpi_y = context.get_dpi_y()
        scale_x = dpi_x / 72  # Convert from PDF points per inch to printer DPI
        scale_y = dpi_y / 72
        scale = min(scale_x, scale_y)

        offset_x = (paper_width - pdf_width * scale) / 2
        offset_y = (paper_height - pdf_height * scale) / 2
        cairo_context.translate(offset_x, offset_y)
        cairo_context.scale(scale, scale)

        pdf_page.render(cairo_context)
        cairo_context.restore()

    def _saveSetting(self, key, value):
        self.model.userconfig.set('printer', key, value)


class PDFContentViewer(PDFFileViewer):

    def __init__(self, model, widget, tv): # widget is bx_previewPDF (which will have 2x .hbox L/R pages inside it)
        super().__init__(model, widget)
        self.toctv = tv
        self.cr = Gtk.CellRendererText()
        tvc = Gtk.TreeViewColumn("Title", self.cr, text=0)
        self.toctv.append_column(tvc)
        self.toctv.connect("row-activated", self.pickToc)
        self.parlocfile = None
        self.parlocs = None
        self.widget = None
        # self.drag_start_x = None
        # self.drag_start_y = None
        self.adjlist = None
        self.showadjustments = True
        self.showguides = False
        self.showgrid = False
        self.showrects = False # self.model.get("c_pdfadjoverlay", False)
        self.showanalysis = False
        self.spacethreshold = 0
        self.charthreshold = 0
        self.ufCurrIndex = 0
        self.currpref = None
        self.timer_id = None  # Stores the timer reference
        self.last_click_time = 0  # Timestamp of the last right-click
        self.linespacing = float(self.model.get("s_linespacing", "12"))
        self.collisionpages = []
        self.spacepages = []
        self.riverpages = []
        
        # This may end up in page rendering code. Just collect data for now
        display = Gdk.Display.get_default()
        screen = display.get_default_screen()
        window = screen.get_root_window()
        scale = window.get_scale_factor()
        logger.debug(f"Window scaling = {scale}")

    def setShowAdjOverlay(self, val):
        self.showadjustments = val
        self.show_pdf()

    def setShowParaBoxes(self, val):
        self.showrects = val
        self.show_pdf()

    def setShowAnalysis(self, val, threshold):
        self.showanalysis = val
        self.spacethreshold = threshold
        if self.showanalysis:
            self.load_analysis(self.parlocfile)
            self.loadnshow(None, page=self.current_page)
        self.show_pdf()

    def settingsChanged(self):
        self.shrinkStep = int(self.model.get('s_shrinktextstep', 2))
        self.expandStep = int(self.model.get('s_expandtextstep', 3))
        self.shrinkLimit = int(self.model.get('s_shrinktextlimit', 90))
        self.expandLimit = int(self.model.get('s_expandtextlimit', 110))
        self.riverparms = {
            'max_v_gap': float(self.model.get("s_rivergap", 0.4)),
            'min_h': float(self.model.get('s_riverminwidth', 0.5)),
            'min_overlap': float(self.model.get('s_riveroverlap', 0.4)),
            'minmax_h': float(self.model.get('s_riverminmaxwidth', 1)),
            'total_width': float(self.model.get("s_riverthreshold", 3)),
        }
        self.spacethreshold = float(self.model.get("s_spaceEms", 3.0))
        self.charthreshold = float(self.model.get("s_charSpaceEms", 0))

    def load_pdf(self, pdf_path, adjlist=None, isdiglot=False, **kw):
        self.settingsChanged()
        
        self.isdiglot = isdiglot
        if pdf_path is None or not os.path.exists(pdf_path):
            self.document = None
            return False

        file_uri = Path(pdf_path).as_uri()
        self.fname = pdf_path
        try:
            self.document = Poppler.Document.new_from_file(file_uri, None)
            self.numpages = self.document.get_n_pages()
        except Exception as e:
            self.model.doStatus(_("Error opening PDF: ").format(e))
            self.document = None
            return False

        tocts = self.load_toc(self.document, self.toctv)
        self.toctv.set_model(tocts)
        fontR = str(self.model.get('bl_fontR', None)).split("|")[0]
        if fontR:
            font_desc = Pango.FontDescription(fontR + " 12")  # Font name and size
            self.cr.set_property("font-desc", font_desc)
        
        self.adjlist = adjlist
        # print(f"In load_pdf. No longer calling: updatePgCtrlButtons")
        # self.model.updatePgCtrlButtons(None)
        return True

    def _add_toctree(self, tocts, toci, parent):
        action = toci.get_action()
        if action.type != Poppler.ActionType.GOTO_DEST:
            return
        title = action.any.title
        dest = action.goto_dest.dest
        if dest.type == Poppler.DestType.NAMED:
            dest = self.document.find_dest(dest.named_dest)
        pnum = dest.page_num
        parent = tocts.append(parent, [title, pnum])
        toci = toci.get_child()
        havei = toci is not None
        while havei:
            self._add_toctree(tocts, toci, parent)
            havei = toci.next()

    def load_toc(self, document, treeview):
        ''' Table of Contents: [name:str, pagenum:int] '''
        res = Gtk.TreeStore(str, int)
        indexi = None
        if document is not None:
            try:
                indexi = Poppler.IndexIter.new(document)
            except TypeError:
                return res
        if indexi is not None:
            havei = True
            while havei:
                self._add_toctree(res, indexi, None)
                havei = indexi.next()

        # Expand nodes conditionally based on top-level count
        num_top_level_nodes = self._count_top_level_nodes(res)
        if num_top_level_nodes < 8:
            self._expand_all_nodes(treeview, res)

        return res

    def _count_top_level_nodes(self, treestore):
        """Counts only the top-level nodes in the TreeStore."""
        count = 0
        iter = treestore.get_iter_first()  # Start with the first top-level node
        while iter is not None:
            count += 1
            iter = treestore.iter_next(iter)  # Move to the next top-level node
        return count

    def _expand_all_nodes(self, treeview, treestore):
        def expand_later():
            def expand_recursive(model, path, iter, data):
                treeview.expand_row(path, False)
            treestore.foreach(expand_recursive, None)
            return False

        GLib.idle_add(expand_later)
    
    def pickToc(self, tv, path, col):
        pnum = tv.get_model()[path][1]
        self.show_pdf(pnum)

    def show_pdf(self, cpage=None, rtl=False, setpnum=True):
        """ cpage is a index (1 based) """
        if self.document is None:
            self.clear()
            return
        if cpage is None:
            cpage = self.current_index or self.parlocs.pnums.get(1, 1) if self.parlocs is not None else 1
        self.spread_mode = self.model.get("c_bkView", False)
        # page = self.parlocs.pnumorder[cpage-1] if self.parlocs is not None and cpage > 0 and cpage <= len(self.parlocs.pnumorder) else cpage 
        if self.parlocs and self.parlocs.pnumorder and 0 < cpage <= len(self.parlocs.pnumorder):
            page = self.parlocs.pnumorder[cpage - 1]
        else:
            page = cpage
        # print(f"{self.parlocs.pnums}")
        # print(f"in show_pdf: {cpage=}   {page=}")
        layerfns = []
        if self.showgrid:
            layerfns.append(self._draw_grid)
        if self.showguides:
            layerfns.append(self._draw_guides)
        if self.showadjustments:        # draw annotations over the rest
            layerfns.append(self.add_hints)
        if self.showrects:
            layerfns.append(self._draw_rectangles)
        if self.showanalysis:
            layerfns.append(self._draw_spaces)
            layerfns.append(self._draw_collisions)
            layerfns.append(self._draw_whitespace_rivers)
        
        images = []
        if self.spread_mode:
            spread = self.get_spread(cpage, self.rtl_mode)
            self.create_boxes(len(spread))
            for i in spread:
                if i in range(self.numpages+1):
                    pg = self.document.get_page(i-1)
                    self.psize = pg.get_size()
                    images.append(render_page_image(pg, self.zoomLevel, i, layerfns))
                    self.parlocs.load_page(self.document, pg, i)
        elif cpage in range(self.numpages+1):
            self.create_boxes(1)
            pg = self.document.get_page(cpage-1)
            self.psize = pg.get_size()
            images.append(render_page_image(pg, self.zoomLevel, cpage, layerfns))
            self.parlocs.load_page(self.document, pg, cpage)

        self.current_page = page
        self.current_index = cpage
        if setpnum and str(page) != self.model.get("t_pgNum"):
            self.model.set("t_pgNum", str(page), mod=False)
        self.update_boxes(images)
        self.updatePageNavigation()

    def _get_margins(self, pindex):
        margin = mm_pts(float(self.model.get("s_margins")))
        gutter = mm_pts(float(self.model.get("s_pagegutter"))) if self.model.get("c_pagegutter") else 0.
        left = margin
        right = margin
        if self.model.get("c_pagegutter"):
            pnum = self.parlocs.pnumorder[pindex-1] if self.parlocs is not None \
                        and pindex <= len(self.parlocs.pnumorder) else pindex

            flip = self.rtl_mode  # Reverse logic if RTL mode is enabled
            if self.model.get("c_outerGutter") == ((pnum & 1 == 0) == flip):
                right += gutter
            else:
                left += gutter
        return (left, right)

    def _draw_guides(self, page, pindex, context, zoomlevel):
        def drawline(x, y, width, height, col):
            context.set_source_rgba(col[0], col[1], col[2], 1)
            context.rectangle(x, y, width, height)
            context.fill()

        haveCrop = self.model.get("c_cropmarks")
        pwidth, pheight = page.get_size()
        (marginmms, topmarginmms, bottommarginmms, headerpos, footerpos, rulerpos,
                headerlabel, footerlabel, hfontsizemms) = self.model.getMargins()
        texttop = mm_pts(float(self.model.get("s_topmargin"))) + (36 if haveCrop else 0)
        hdrbot = float(self.model.get("s_headerposition"))
        ftrtop = float(self.model.get("s_footerposition"))
        textbot = mm_pts(float(self.model.get("s_bottommargin"))) + (36 if haveCrop else 0)
        lineheight = float(self.model.get("s_linespacing")) * 72 / 72.27
        textsize = float(self.model.get("s_fontsize"))
        colgutterwidth = mm_pts(float(self.model.get("s_colgutterfactor")))
        minorcol = (0.68, 0.85, 0.68)
        majorcol = (0.8, 0.6, 0.6)
        left, right = self._get_margins(pindex)
        innerheight = pheight - texttop - textbot
        if haveCrop:
            left += 36
            right += 36

        # header
        drawline(left, mm_pts(headerpos) + (36 if haveCrop else 0), pwidth - right - left, 0.5, minorcol)
        drawline(left, mm_pts(headerpos) + mm_pts(hfontsizemms) + (36 if haveCrop else 0), pwidth - right - left, 0.5, minorcol)
        drawline(0, texttop - 0.4, pwidth, 0.8, majorcol)       # main top margin
        tstop = pheight - textbot
        tstart = texttop
        while tstart < tstop:
            tstart += lineheight
            drawline(0, tstart, pwidth, 0.5, minorcol)          # text base lines
        # footer
        drawline(0, pheight - textbot, pwidth, 0.8, majorcol)   # main bottom margin
        drawline(left, pheight - textbot + ftrtop, pwidth - right - left, 0.5, minorcol)
        drawline(left, pheight - textbot + ftrtop + textsize, pwidth - right - left, 0.5, minorcol)

        # vertical lines
        drawline(left - 0.4, 0, 0.8, pheight, majorcol)         # left margin
        drawline(pwidth - right - 0.4, 0, 0.8, pheight, majorcol)       # right margin

        if self.model.get("c_doublecolumn"):
            centre = 0.5 * (left + pwidth - right)
            drawline(centre - 0.4, 0, 0.8, pheight, majorcol)   # centre line
            gap = colgutterwidth * 0.5
            if self.model.get("r_xrpos") == "centre":
                gap += (float(self.model.get("s_centreColWidth")) + float(self.model.get("s_xrGutterWidth"))) * 0.5
            lgap = rgap = gap
            if self.model.get("c_marginalverses"):
                cshift = float(self.model.get("s_columnShift"))
                mode = self.model.get("fcb_marginVrsPosn")
                if mode == "left" or mode == "inner":
                    rgap += cshift
                if mode == "left" or mode == "outer":
                    drawline(left + cshift - 0.25, texttop, 0.5, innerheight, minorcol)     # extra margin verses
                if mode == "right" or mode == "inner":
                    lgap += cshift
                if mode == "right" or mode == "outer":
                    drawline(pwidth - right - 0.25, texttop, 0.5, innerheight, minorcol)    # extra margin verses
            drawline(centre - lgap - 0.25, texttop, 0.5, innerheight, minorcol)     # left of centre mini margin
            drawline(centre + rgap - 0.25, texttop, 0.5, innerheight, minorcol)     # right of centre mini margin

    def _draw_grid(self, page, pnum, context, zoomlevel):
        def drawline(x, y, width, height, col):
            context.set_source_rgba(col[0], col[1], col[2], 1)
            context.rectangle(x, y, width, height)
            context.fill()

        haveCrop = self.model.get("c_cropmarks")
        pwidth, pheight = page.get_size()
        units = self.model.get("fcb_gridUnits")
        minordivs = int(self.model.get("s_gridMinorDivisions"))
        edge = self.model.get("fcb_gridOffset")
        majorcol = coltoonemax(self.model.get("col_gridMajor"))
        majorthick = float(self.model.get("s_gridMajorThick"))
        minorcol = coltoonemax(self.model.get("col_gridMinor"))
        minorthick = float(self.model.get("s_gridMinorThick"))
        texttop = mm_pts(float(self.model.get("s_topmargin"))) + (36 if haveCrop else 0)
        textbot = mm_pts(float(self.model.get("s_bottommargin"))) + (36 if haveCrop else 0)
        (left, right) = self._get_margins(pnum)
        if haveCrop:
            left += 36
            right += 36

        if edge == "page":
            jobs = [((0,0), (pwidth, pheight))]
        elif edge == "text":
            jobs = [((left, texttop), (pwidth - right, pheight - textbot))]
        elif edge == "margin":
            jobs = [((0, 0), (pwidth, texttop))]
            jobs.append(((0, pheight - textbot), (pwidth, pheight))) 
            jobs.append(((0, texttop), (left, pheight - textbot))) 
            jobs.append(((pwidth - right, texttop), (pwidth, pheight - textbot))) 
        # now we can do multiple jobs for bits outside the margins
        for j in jobs:
            major = 72.27 if units == "in" else mm_pts(10)
            minor = major / minordivs
            # horizontals
            start = j[0][1]     # y
            while start < j[1][1]:
                nextv = min(start + major, j[1][1])
                if start > j[0][1]:
                    drawline(j[0][0], start, j[1][0] - j[0][0], majorthick, majorcol)
                v = start + minor
                while v < nextv:
                    drawline(j[0][0], v, j[1][0] - j[0][0], minorthick, minorcol)
                    v += minor
                start += major
            # verticals
            start = j[0][0]
            while start < j[1][0]:
                nextv = min(start + major, j[1][0])
                if start > j[0][0]:
                    drawline(start, j[0][1], majorthick, j[1][1] - j[0][1], majorcol)
                v = start + minor
                while v < nextv:
                    drawline(v, j[0][1], minorthick, j[1][1] - j[0][1], minorcol)
                    v += minor
                start += major

    def _draw_rectangles(self, page, pnum, context, zoomlevel):
        def make_rect(r, width, col=(0.2, 0.2, 0.8, 0.4)):
            context.set_source_rgba(*col)
            context.rectangle(r.xstart, self.psize[1] - r.ystart, r.xend - r.xstart, r.ystart - r.yend)
            context.set_line_width(width)
            context.stroke()
        for p, r in self.parlocs.getParas(pnum):
            make_rect(r, 1)

    def _draw_spaces(self, page, pnum, context, zoomlevel):
        def make_rect(x, y, width, col=(0.2, 0.7, 0.8, 0.5), height=6):
            context.set_source_rgba(*col)
            context.rectangle(x, y - height, width, height)
            context.fill()
        threshold = self.spacethreshold
        if threshold == 0:
            if not hasattr(self, 'badspaces'):
                self.badspaces = self.parlocs.getnbadspaces()
            if len(self.badspaces):
                self.model.set("s_spaceEms", self.badspaces[0].widthem)
            for s in self.badspaces:
                if s.pnum == pnum:
                    make_rect(*s.pos, s.width)
        else:
            for s in self.parlocs.getbadspaces(pnum, threshold, self.charthreshold if self.model.get('c_letterSpacing', False) else 0.):
                make_rect(*s.pos, s.width)

    def _draw_collisions(self, page, pnum, context, zoomlevel):
        def make_rect(r, col=(1.0, 0, 0.2, 0.6)):
            context.set_source_rgba(*col)
            context.rectangle(*r)
            context.fill()

        for c in self.parlocs.getcollisions(pnum):
            make_rect(c)
            
    def _draw_whitespace_rivers(self, page, pnum, context, zoomlevel):
        def make_rect(r, col=(1, 1, 0.1, 0.4)):
            context.set_source_rgba(*col)
            context.rectangle(*r)
            context.fill()
            
        for r in self.parlocs.getrivers(pnum, **self.riverparms):
            for s in r.spaces:
                make_rect(s)

    # incomplete code calling for major refactor for cairo drawing
    def add_hints(self, pdfpage, page, context, zoomlevel):
        """ page is a page index"""
        def make_dashed(context, col, r, width, length):
            red, green, blue = hsv_to_rgb(*col)
            context.set_source_rgba(red, green, blue, 0.4)
            s = self.psize[1] - r.ystart
            e = self.psize[1] - r.yend
            if length < 0:
                s -= length
                length = -length
            y = s
            x = r.xstart if width >= 0 else r.xend + width
            while y < e:
                l = length if y + length < e else e - y
                context.rectangle(x, y, abs(width), l)
                context.fill()
                logger.log(7, f"dash({x}, {y}, {abs(width)}, {l}) @ ({red}, {green}, {blue})")
                y += 2 * length
            
        def make_rect(context, col, r, width):
            red, green, blue = hsv_to_rgb(*col)
            context.set_source_rgba(red, green, blue, 0.4)
            context.rectangle((r.xstart if width >= 0 else r.xend + width),
                              (self.psize[1] - r.ystart), abs(width), (r.ystart - r.yend))
            logger.log(7, f"rect({r.xstart if width >= 0 else r.xend + width}, {self.psize[1] -r.ystart}, {abs(width)}, {r.ystart - r.yend}) @ ({red}, {green}, {blue})")
            context.fill()
        bk = None
        for p, r in self.parlocs.getParas(page):
            if not isinstance(p, ParInfo):
                continue
            # print(f"{p.ref=}[{getattr(p, 'parnum', '')}]")
            nbk = getattr(p, "ref", bk or "")[:3].upper()
            if not len(nbk):
                continue
            if nbk != bk:
                adjlist = self.model.get_adjlist(nbk, gtk=Gtk)
                bk = nbk
            parnum = getattr(p, 'parnum', 0) or 0
            parnum = "["+str(parnum)+"]" if parnum > 1 else ""            
            ref = getattr(p, 'ref', (bk or "") + "0.0") + parnum
            info = adjlist.getinfo(ref)
            if not info:
                continue
            col = None
            s = info[0]
            sv = int(re.sub(r"^[+-]*", "", s))  # num lines
            sv = -sv if "-" in s else sv
            # right is grow, left is shrink
            # lines = blue, orange = text
            blue = (173 / 255., 1., 1.)
            orange = (0., 1., 1.)
            lwidth = sv * -3
            twidth = 100 - info[1]
            lh = 2 * p.baseline / 3.
            if sv < 0:      # compress (lhs)
                if info[1] < 100:       # both compress
                    make_dashed(context, blue, r, lwidth, lh)  # dashed for lines
                    make_dashed(context, orange, r, twidth, -lh)  # dashed for text
                else:
                    make_rect(context, blue, r, lwidth)
                    if info[1] > 100:
                        make_rect(context, orange, r, twidth)
            elif sv > 0:    # expand (rhs)
                if info[1] > 100:       # both expand
                    make_dashed(context, blue, r, lwidth, lh)
                    make_dashed(context, orange, r, twidth, -lh)
                else:
                    make_rect(context, blue, r, lwidth)
                    if info[1] < 100:
                        make_rect(context, orange, r, twidth)
            elif info[1] != 100:
                make_rect(context, orange, r, twidth)

    def loadnshow(self, fname, rtl=False, adjlist=None, parlocs=None, widget=None, page=None, isdiglot=False, **kw):
        def plocs(self):
            self.load_parlocs(self.parlocfile, rtl=rtl)
            if page is not None and page in self.parlocs.pnums:
                self.current_page = page
                self.current_index = self.parlocs.pnums[page]
        if parlocs is None:
            parlocs = self.parlocfile
        if parlocs is not None:
            self.parlocfile = parlocs
        if not super().loadnshow(fname, rtl=rtl, page=page, parlocs=parlocs, widget=widget, isdiglot=isdiglot, hook=plocs, **kw):
            return False
        if widget is not None:
            widget.set_title(_("PDF Preview 3.0.0") + "   " + os.path.basename(self.fname))
        self.model.set_preview_pages(self.numpages, _("Pages:"))
        return True

    def clear(self, widget=None):
        super().clear(widget=widget)
        m = self.toctv.get_model()
        if m:
            m.clear()
        self.model.set_preview_pages(None)

    def load_parlocs(self, fname, rtl=False):
        self.parlocs = Paragraphs()
        self.parlocs.readParlocs(fname, rtl=rtl)
        self.parlocs.load_dests(self.document)
        if self.showanalysis:
            self.load_analysis(fname)

    def load_analysis(self, fname):
        xdvname = fname.replace(".parlocs", ".xdv")
        print(f"Reading {xdvname}")
        cthreshold = float(self.model.get("s_paddingwidth", 0.5))
        xdvreader = SpacingOddities(xdvname, parent=self.parlocs, collision_threshold=cthreshold,
                                    fontsize=float(self.model.get("s_fontsize", 1)))
        for (opcode, data) in xdvreader.parse():
            pass
        if self.spacethreshold == 0:
            self.badspaces = self.parlocs.getnbadspaces()
            if len(self.badspaces):
                self.model.set("s_spaceEms", self.badspaces[0].widthem)
        wanted = 7
        self.spacepages, self.collisionpages, self.riverpages = \
            self.parlocs.getstats(wanted, float(self.model.get('s_spaceEms', 4)),
                    float(self.model.get('s_charSpaceEms', 4) if self.model.get('c_letterSpacing', False) else 0.))

    def get_spread(self, page, rtl=False):
        """ page is a page index not folio """
        logger.debug(f"get_spread({page}, {rtl=})")
        if page == 1:
            return (1,)
        if page % 2 == 0:
            page += 1
        if page > int(self.numpages):
            return (int(self.numpages),)
        if rtl:
            return (page, page - 1)
        else:
            return (page - 1, page)

    def seekUFpage(self, direction):
        pages = self.numpages
        if not pages or not self.model.ufPages:
            return
        pgnum = self.current_index
        try:
            current_pg = self.parlocs.pnumorder[pgnum - 1] if self.parlocs is not None else 1
        except IndexError:
            print(f"Index Error in seekUFpage: {pgnum=} {pages=}")
            current_pg = 1
        if direction == self.swap4rtl('next'):
            next_page = None
            for pg in self.all_pages: # self.model.ufPages:
                if pg > current_pg:
                    next_page = pg
                    break
            if next_page:
                self.ufCurrIndex = self.all_pages.index(next_page)  # self.model.ufPages
        else:  # 'previous'
            prev_page = None
            for pg in reversed(self.all_pages):
                if pg < current_pg:
                    prev_page = pg
                    break
            if prev_page:
                self.ufCurrIndex = self.all_pages.index(prev_page)
        pg = self.all_pages[self.ufCurrIndex]
        pnum = self.parlocs.pnums.get(pg, pg) if self.parlocs is not None else pg
        self.show_pdf(pnum)
        
    def updatePageNavigation(self):
        super().updatePageNavigation()

        self.all_pages = []
        pg = self.current_index or 1
        pnumpg = self.parlocs.pnumorder[pg - 1] if self.parlocs and pg <= len(self.parlocs.pnumorder) else 1
        is_rtl = self.rtl_mode and self.model.lang != 'ar_SA'
        num_pages = self.numpages

        seekPrevBtn = self.model.builder.get_object("btn_seekPage2fill_previous")
        seekNextBtn = self.model.builder.get_object("btn_seekPage2fill_next")
        if not self.model.get('c_layoutAnalysis', False):
            ufPages         = self.model.ufPages or []
            collisionPages  = []
            horizWhitespace = []
            vertRivers      = []
        else:
            ufPages         = self.model.ufPages or [] if self.model.get('c_findUnbalanced', False) else []
            collisionPages  = self.collisionpages      if self.model.get('c_findCollisions', False) else []
            horizWhitespace = self.spacepages          if self.model.get('c_findWhitespace', False) else []
            vertRivers      = self.riverpages          if self.model.get('c_findRivers',     False) else []

        # Merge lists in order with uniqueness
        for lst in [ufPages, collisionPages, horizWhitespace, vertRivers]:
            for p in lst:
                if p not in self.all_pages:
                    self.all_pages.append(p)
        self.all_pages = sorted(self.all_pages)
        
        total_count = len(self.all_pages)
        self.model.builder.get_object("bx_seekPage").set_sensitive(total_count > 0)

        for btn in [
            "btn_page_first", "btn_page_previous", "btn_page_next", "btn_page_last",
            "btn_seekPage2fill_previous", "btn_seekPage2fill_next"
        ]:
            action = btn.split("_")[-1]
            o = self.model.builder.get_object(btn)

            if not 'seekPage' in btn:
                # Update navigation tooltips for normal page buttons
                tt = o.get_tooltip_text()
                o.set_tooltip_text(re.sub(action.title(), self.swap4rtl(action).title(), tt))
                continue

            # "Seek" buttons — build multi-color tooltip
            if total_count < 1:
                seekText = _("Locate {} issue page.{}(None identified)").format(self.swap4rtl(action), "\n")
            else:
                curr_pos = 0
                if pnumpg in self.all_pages:
                    curr_pos = self.all_pages.index(pnumpg)

                locatefirstPage = self.all_pages[0]
                locatelastPage  = self.all_pages[-1]

                if is_rtl:  # Fix later to include Arabic UI detection
                    hide_prev = pnumpg >= locatelastPage or pnumpg == num_pages
                    hide_next = pnumpg <= locatefirstPage or pnumpg == 1
                else:
                    hide_prev = pnumpg <= locatefirstPage or pnumpg == 1
                    hide_next = pnumpg >= locatelastPage or pnumpg == num_pages

                seekPrevBtn.set_sensitive(not hide_prev)
                seekNextBtn.set_sensitive(not hide_next)

                window_size = 5  # Show 3 numbers before and after the current one

                # Determine which pages to display
                if total_count <= 12:
                    display_pages = self.all_pages
                    elipsis = ""
                else:
                    start_idx = max(0, curr_pos - window_size)
                    end_idx   = min(total_count, curr_pos + window_size + 1)
                    display_pages = self.all_pages[start_idx:end_idx]
                    elipsis = f" (of {total_count})"
                    if start_idx > 0:
                        display_pages.insert(0, "...")
                    if end_idx < total_count:
                        display_pages.append("...")

                # Color-code pages
                formatted_pages = []
                for p in display_pages:
                    if p == "...":
                        formatted_pages.append("...")
                        continue
                    if p in collisionPages:
                        text = f"<span foreground='red'><b>{p}</b></span>"
                    elif p in horizWhitespace and p in vertRivers:
                        text = f"<span foreground='lightgreen'><b>{p}</b></span>"
                    elif p in horizWhitespace:
                        text = f"<span foreground='lightblue'><b>{p}</b></span>"
                    elif p in vertRivers:
                        text = f"<span foreground='yellow'><b>{p}</b></span>"
                    else: # if p in ufPages:
                        text = f"<b>{p}</b>"

                    # Mark current page with <>
                    if p == pnumpg:
                        text = f"&lt;{text}&gt;"

                    formatted_pages.append(text)

                # RTL handling
                if is_rtl or self.model.lang == 'ar_SA':
                    formatted_pages = list(reversed(formatted_pages))

                pgs = "  ".join(formatted_pages)
                seekText = _("Locate {} issue page.").format(self.swap4rtl(action)) + "\n" + pgs + elipsis
            # Use markup so colors are shown
            o.set_tooltip_markup(seekText)

    def minmaxnumpages(self):
        if self.parlocs is None or not len(self.parlocs.pnums):
            return super().minmaxnumpages()
        minPg = min(self.parlocs.pnums)
        last_key = list(self.parlocs.pnums.keys())[-1]
        numpg = len(self.parlocs.pnums)
        return (minPg, last_key, numpg)

    def getpnum(self, n, d):
        if self.parlocs is not None:
            return self.parlocs.pnums.get(self.current_page, d)
        else:
            return n

    def closestpnum(self, pg):
        if self.parlocs is not None:
            available_pnums = self.parlocs.pnums.keys()
            if len(available_pnums) and pg not in available_pnums:
                pg = min(available_pnums, key=lambda p: abs(p - pg))
        return pg

    def get_parloc(self, widget, event):
        x = event.x / self.zoomLevel
        y = event.y / self.zoomLevel
        if self.spread_mode:
            side = self.widgetPosition(widget)
            if len(self.hbox.get_children()) > 1 and self.rtl_mode:
                side ^= 1 # swap side if RTL
            pnum = self.get_spread(self.current_index)[side]     # this all only works for LTR
        else:
            pnum = self.current_index
        p = None
        a = self.hbox.get_allocation()

        if self.parlocs is not None:
            p, r, a = self.parlocs.findPos(pnum, x, self.psize[1] - y, rtl=self.rtl_mode)
        return p, pnum, a

    def addMenuItem(self, menu, label, fn, *args, sensitivity=None):
        if label is None:
            res = Gtk.SeparatorMenuItem.new()
        else:
            res = Gtk.MenuItem(label=label)
            if sensitivity is not None:
                res.set_sensitive(sensitivity)
            if fn is not None:
                res.connect("activate", fn, *args)
        res.show()
        menu.append(res)
        return res

    def hitPrint(self):
        """ Delayed execution of print with a N-second debounce timer. """
        if self.model.get("c_updatePDF"):
            now = time.time()
            self.last_click_time = now
            if self.timer_id:
                GLib.source_remove(self.timer_id)  # Cancel previous timer if it exists
            # Schedule a delayed execution, but check timestamp before running
            self.timer_id = GLib.timeout_add(self.autoUpdateDelay * 1000, self.executePrint)

    def executePrint(self):
        """ Actually triggers print only if no new clicks happened in the last N seconds. """
        self.timer_id = None  # Reset timer reference
        # If the last click was within the last N seconds, cancel execution
        if time.time() - self.last_click_time < self.autoUpdateDelay:
            return False  # Do nothing, just stop the timer
        self.model.onOK(None)
        self.updatePageNavigation()
        return False

    def on_update_pdf(self, x): # From middle-button click
        self.model.onOK(None)
        self.updatePageNavigation()

    def addSubMenuItem(self, parent_menu, label, submenu):
        menu_item = Gtk.MenuItem(label=label)  # Create a menu item for the parent
        menu_item.set_submenu(submenu)         # Attach the submenu
        parent_menu.append(menu_item)          # Add the parent item to the parent menu
        menu_item.show()                       # Show the parent item

    def clear_menu(self, menu):
        for child in menu.get_children():
            child.destroy()

    def show_context_menu(self, widget, event):
        self.autoUpdateDelay = float(self.model.get('s_autoupdatedelay', 3.0))
        self.last_click_time = time.time()

        menu = Gtk.Menu()
        self.clear_menu(menu)
        
        info = []
        parref = None
        parref, pgindx, annot = self.get_parloc(widget, event)
        if isinstance(parref, ParInfo):
            parnum = getattr(parref, 'parnum', 0) or 0
            parnum = "["+str(parnum)+"]" if parnum > 1 else ""
            ref = parref.ref
            self.adjlist = self.model.get_adjlist(ref[:3].upper(), gtk=Gtk)
            if self.adjlist is not None:
                info = self.adjlist.getinfo(ref + parnum, insert=True)
        logger.debug(f"{event.x=},{event.y=}")

        if len(info) and re.search(r'[.:]', parref.ref):
            if ref[3:4] in "LRABCDEFG":
                pref = ref[3:4]
                o = 4
            else:
                pref = "L"
                o = 3
            l = info[0]
            if l[0] not in '+-':
                l = '+' + l
            hdr = f"{ref[:o]} {ref[o:]}{parnum}   \\{parref.mrk}  {l}  {info[1]}%"
            self.addMenuItem(menu, hdr, None, info, sensitivity=False)
            self.addMenuItem(menu, None, None)

            shrLim = max(self.shrinkLimit, info[1]-self.shrinkStep)
            shrinkText = mstr['yesminus'] if ("-" in str(info[0]) and str(info[0]) != "-1") else mstr['tryminus']
            self.addMenuItem(menu, f"{mstr['shrnkboth']} ({int(info[1])+self.shrinkBothAmt(info)}%)", self.on_shrink_both, info, parref, sensitivity=not info[1] <= shrLim)
            self.addMenuItem(menu, f"{shrinkText} ({parref.lines - 1})", self.on_shrink_paragraph, info, parref)
            self.addMenuItem(menu, f"{mstr['st']} ({shrLim}%)", self.on_shrink_text, info, parref, sensitivity=not info[1] <= shrLim)
            self.addMenuItem(menu, None, None)
            
            self.addMenuItem(menu, f"{mstr['plusline']} ({parref.lines + 1})", self.on_expand_paragraph, info, parref)
            expLim = min(self.expandLimit, info[1]+self.expandStep)
            self.addMenuItem(menu, f"{mstr['et']} ({expLim}%)", self.on_expand_text, info, parref, sensitivity=not info[1] >= expLim)

            reset_menu = Gtk.Menu()
            self.clear_menu(reset_menu)
            for k, v in reset.items():
                if k == "sprd" and not self.spread_mode or \
                   k == "sprd" and len(self.get_spread(pgindx)) < 2 or \
                   k == "col"  and not self.model.get('c_doublecolumn', True):
                    continue
                menu_item = Gtk.MenuItem(label=f"{v}")
                menu_item.connect("activate", self.on_reset_adjustments, k, pgindx, info, parref)
                menu_item.set_sensitive((k == "para" and not (info[1] == 100 and int(l.replace("+","")) == 0)) \
                                     or (k == "col" ) or (k == "page") \
                                     or (k == "sprd" and self.spread_mode and len(self.get_spread(pgindx))))
                menu_item.show()
                reset_menu.append(menu_item)
            self.addSubMenuItem(menu, mstr['rp'], reset_menu)            
            self.addMenuItem(menu, None, None)
            
            if not self.model.get("c_diglot", False) and parref.mrk in ("p", "m"): # add other conditions like: odd page, 1st rect on page, etc
                self.addMenuItem(menu, mstr['sstm'], self.speed_slice, info, parref) # , sensitivity=False)

            if parref and parref.mrk is not None:
                # self.addMenuItem(menu, None, None)
                self.addMenuItem(menu, f"{mstr['es']} \\{parref.mrk}", self.edit_style, (parref.mrk, pref if pref != "L" else None))

            if sys.platform.startswith("win"): # and ALSO (later) check for valid ref
                # self.addMenuItem(menu, None, None)
                self.addMenuItem(menu, mstr['j2pt'], self.on_broadcast_ref, ref)

            # self.addMenuItem(menu, None, None)
            self.addMenuItem(menu, mstr['z2f']+" (Ctrl + F)", self.set_zoom_fit_to_screen)
            if not self.model.get("c_updatePDF"):
                # self.addMenuItem(menu, None, None)
                self.addMenuItem(menu, "Print (Update PDF)", self.on_update_pdf)

        # New section for image context menu which is a lot more complicated
        elif parref is not None and isinstance(parref, FigInfo):
            showmenu = True
            imgref = parref.ref.strip('-preverse')
            pic = None
            if m := re.match(r"^(\d?[A-Z]+)(.*)$", imgref):
                imgref = m.group(1) + " " + m.group(2)
            if not self.model.picinfos:
                showmenu = False
            else:
                pics = self.model.picinfos.find(anchor=imgref)
                if len(pics):
                    pic = pics[0]
                    self.addMenuItem(menu, mstr['ancrdat']+" "+imgref, None, sensitivity=False)
                else:
                    showmenu = False
                    self.addMenuItem(menu, mstr['ianf'], None, sensitivity=False)
            if pic is not None:
                pgpos = pic.get('pgpos', 'tl')
                curr_frame = pic.get('size', 'col')
                if curr_frame in ('page', 'full'): # P,Pl,Pr,Pt,Pb,Pct,Pco,
                    pgpos = pgpos.strip("PF")[::-1]
                    
                if len(pgpos) == 1:
                    curr_vpos = pgpos[:1]
                    curr_hpos = '-'
                elif len(pgpos) > 1:
                    curr_vpos = pgpos[:1]
                    curr_hpos = next((char for char in reversed(pgpos) if char.isalpha()), None) # pgpos[2:3]
                else:
                    curr_vpos = 'c'
                    curr_hpos = 'c'
                if showmenu:
                    self.addMenuItem(menu, mstr['cnganc'], self.on_edit_anchor, (pic, parref))

                    frame_menu = Gtk.Menu()
                    self.clear_menu(frame_menu)
                    for frame_opt in frame.values():
                        menu_item = Gtk.MenuItem(label=f"● {frame_opt}" if frame_opt == frame[curr_frame] else f"   {frame_opt}")
                        if frame_opt == frame[curr_frame]:
                            menu_item.set_sensitive(False)
                        menu_item.connect("activate", self.on_set_image_frame, (pic, frame_opt))
                        menu_item.show()
                        frame_menu.append(menu_item)
                    self.addSubMenuItem(menu, mstr['frmsz'], frame_menu)

                    vpos_menu = Gtk.Menu()
                    self.clear_menu(vpos_menu)
                    for k, vpos_opt in vpos.items():
                        if k in dsplyOpts[pic['size']][0]:
                            menu_item = Gtk.MenuItem(label=f"● {vpos_opt}" if vpos_opt == vpos[curr_vpos] else f"   {vpos_opt}")
                            if vpos_opt == vpos[curr_vpos]:
                                menu_item.set_sensitive(False)
                            menu_item.connect("activate", self.on_set_image_vpos, (pic, vpos_opt, curr_vpos, curr_hpos))
                            menu_item.show()
                            vpos_menu.append(menu_item)
                    self.addSubMenuItem(menu, mstr['vpos'], vpos_menu)

                    if curr_frame != 'span':
                        hpos_menu = Gtk.Menu()
                        self.clear_menu(hpos_menu)
                        p = pic.get('pgpos', 'o')
                        for k, hpos_opt in hpos.items():
                            if k in dsplyOpts[pic['size']][1]:
                                menu_item = Gtk.MenuItem(label=f"● {hpos_opt}" if hpos_opt == hpos[curr_hpos] else f"   {hpos_opt}")
                                if hpos_opt == hpos[curr_hpos]:
                                    menu_item.set_sensitive(False)
                                menu_item.connect("activate", self.on_set_image_hpos, (pic, hpos_opt, curr_vpos, curr_hpos))
                                menu_item.show()
                                hpos_menu.append(menu_item)
                        self.addSubMenuItem(menu, mstr['hpos'], hpos_menu)

                    mirror_menu = Gtk.Menu()
                    self.clear_menu(mirror_menu)
                    curr_mirror = pic.get('mirror', '')
                    for mirror_opt in mirror.values():
                        menu_item = Gtk.MenuItem(label=f"● {mirror_opt}" if mirror_opt == mirror[curr_mirror] else f"   {mirror_opt}")
                        if mirror_opt == mirror[curr_mirror]:
                            menu_item.set_sensitive(False)                    
                        menu_item.connect("activate", self.on_set_image_mirror, (pic, mirror_opt))
                        menu_item.show()
                        mirror_menu.append(menu_item)
                    self.addSubMenuItem(menu, mstr['mirror'], mirror_menu)

                    self.addMenuItem(menu, None, None)
                    self.addMenuItem(menu, mstr['shrinkpic'], self.on_shrink_image, (pic, parref))
                    self.addMenuItem(menu, mstr['growpic'], self.on_grow_image, (pic, parref))
                    self.addMenuItem(menu, None, None)

                    self.addMenuItem(menu, mstr['shwdtl'], self.on_image_show_details, pic)
                    self.addMenuItem(menu, mstr['ecs']+" \\fig", self.edit_fig_style)
            if showmenu:
                if sys.platform.startswith("win"):
                    self.addMenuItem(menu, None, None)
                    self.addMenuItem(menu, mstr['j2pt'], self.on_broadcast_ref, imgref)
                if not self.model.get("c_updatePDF"):
                    self.addMenuItem(menu, None, None)
                    self.addMenuItem(menu, "Print (Update PDF)", self.on_update_pdf)
        if len(menu):
            menu.popup(None, None, None, None, event.button, event.time)

    def on_edit_anchor(self, widget, data):
        pic, parref = data
        a = pic['anchor']
        piciter = self.model.picListView.find_row(a)
        self.model.set("t_newAnchor", a, mod=False)
        dialog = self.model.builder.get_object("dlg_newAnchor")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            v = self.model.get("t_newAnchor")
            if piciter is not None:
                pic['anchor'] = v
                self.model.picListView.set_val(piciter, anchor=v)
                parref.ref = v.replace(" ","")+'-preverse'
                self.hitPrint()
        dialog.hide()

    def on_set_image_frame(self, widget, data):
        pic, frame_opt = data
        f = rev_frame[frame_opt]
        orig_pgpos = pic['pgpos']
        piciter = self.model.picListView.find_row(pic['anchor'])
        if piciter is not None:
            pic['size'] = f
            self.model.picListView.set_val(piciter, size=f)
            if f in ('page', 'full'):
                pic['pgpos'] = f[:1].upper()
                self.model.picListView.set_val(piciter, pgpos=f[:1].upper())
            elif f == 'span':
                pic['pgpos'] = 't'
                self.model.picListView.set_val(piciter, pgpos='t')
            else: # 'col'
                pic['pgpos'] = 'tl'
                self.model.picListView.set_val(piciter, pgpos='tl')
                self.hitPrint()

    def on_set_image_vpos(self, widget, data):
        pic, vpos_opt, orig_v, orig_h = data
        orig_pgpos = pic['pgpos']
        if orig_pgpos[:1] in ('P', 'F'):
            v = orig_pgpos[:1] + orig_h + rev_vpos[vpos_opt]
            v = v.strip('c')
        else:
            v = re.sub(orig_v, rev_vpos[vpos_opt], orig_pgpos)
        v = re.sub('-', '', v)
        piciter = self.model.picListView.find_row(pic['anchor'])
        if piciter is not None:
            pic['pgpos'] = v
            self.model.picListView.set_val(piciter, pgpos=v)
            self.hitPrint()

    def on_set_image_hpos(self, widget, data):
        pic, hpos_opt, orig_v, orig_h = data
        orig_pgpos = pic['pgpos']
        if orig_pgpos[:1] in ('P', 'F'):
            h = orig_pgpos[:1] + rev_hpos[hpos_opt] + orig_v
            h = h.strip('c')
        elif len(orig_pgpos) == 1:
            h = orig_pgpos + rev_hpos[hpos_opt]
        else:
            h = re.sub(orig_h, rev_hpos[hpos_opt], orig_pgpos)
        h = re.sub('-', '', h)
        piciter = self.model.picListView.find_row(pic['anchor'])
        if piciter is not None:
            pic['pgpos'] = h
            self.model.picListView.set_val(piciter, pgpos=h)
            self.hitPrint()

    def on_set_image_mirror(self, widget, data):
        pic, mirror_opt = data
        m = rev_mirror[mirror_opt]
        piciter = self.model.picListView.find_row(pic['anchor'])
        if piciter is not None:
            pic['mirror'] = m
            self.model.picListView.set_val(piciter, mirror=m)
            self.hitPrint()
            
    def on_shrink_image(self, widget, data):
        pic, parref = data
        line_height = float(self.model.get("s_linespacing", 12))
        self.adjust_fig_size(pic, parref.size, -1 * line_height)
        
    def on_grow_image(self, widget, data):
        pic, parref = data
        line_height = float(self.model.get("s_linespacing", 12))
        self.adjust_fig_size(pic, parref.size, line_height)

    def adjust_fig_size(self, pic, psize, adj):
        '''adj is the value in pts (+ve/-ve)'''
        if psize[1] == 0:
            return
        
        ratio = float(pic.get('scale', 1))
        nr = ratio * (adj / psize[1] + 1)
        if nr < .05 or nr > 2. :
            return
        v = f2s(nr)
        pic['scale'] = v
        vint = int(float(v) * 100)
        piciter = self.model.picListView.find_row(pic['anchor'])
        if piciter is not None:
            self.model.picListView.set_val(piciter, scale=vint)
            self.hitPrint()

    def on_image_show_details(self, widget, pic):
        piciter = self.model.picListView.find_row(pic['anchor'])
        if piciter is not None:
            mpgnum = self.model.notebooks['Main'].index("tb_Pictures")
            self.model.builder.get_object("nbk_Main").set_current_page(mpgnum)
            self.model.builder.get_object("nbk_PicList").set_current_page(1)
            self.model.mainapp.win.present()
            self.model.wiggleCurrentTabLabel()
            treeview = self.model.builder.get_object("tv_picListEdit")
            model = treeview.get_model()
            path = model.get_path(piciter)
            treeview.scroll_to_cell(path, None, True, 0.5, 0.0)  # Ask MH: How to do this for the StyleEditor jumps?
            self.model.picListView.select_row(piciter)

    def speed_slice(self, widget, info, parref):
        if parref.ref is not None and parref.ref != self.model.get("t_sliceRef", ""):
            self.model.set("t_sliceWord", "", mod=False)
        if parref.ref is not None:
            ref = parref.ref[:3]+' '+parref.ref[3:].replace(".",":")
        self.model.set("t_sliceRef", ref, mod=False)
        dialog =   self.model.builder.get_object("dlg_slice4speed")
        textview = self.model.builder.get_object("t_sliceWord")
        fontR = str(self.model.get('bl_fontR', None)).split("|")[0]
        if fontR:
            font_desc = Pango.FontDescription(fontR + " 12")
            textview.modify_font(font_desc)
        response = dialog.run()
        dialog.hide()
        if response != Gtk.ResponseType.OK:
            self.model.set("t_sliceRef", "", mod=False)
        self.hitPrint()

    def shrinkBothAmt(self, info):
        offset = int(0.5 * (self.shrinkLimit - info[1]) - 0.1)
        if offset > -self.shrinkStep:
            offset = self.shrinkLimit - info[1]
        return offset

    def on_shrink_both(self, widget, info, parref):
        if self.adjlist is not None:
            if info[1] > self.shrinkLimit:
                self.adjlist.expand(info[2], self.shrinkBothAmt(info), mrk=parref.mrk)
            if int(info[0]) >= 0:
                offset = -(int(info[0]) + 1)
                self.adjlist.increment(info[2], offset)
        self.show_pdf()
        self.hitPrint()

    def on_shrink_paragraph(self, widget, info, parref):
        if self.adjlist is not None:
            self.adjlist.increment(info[2], -1)
        self.show_pdf()
        self.hitPrint()

    def on_expand_paragraph(self, widget, info, parref):
        if self.adjlist is not None:
            self.adjlist.increment(info[2], 1)
        self.show_pdf()
        self.hitPrint()

    def on_reset_adjustments(self, widget, scope, pgindx, info, parref):
        if self.adjlist is None:
            return
        refs2del = []
        if scope == 'para':
            refs2del.append((parref.ref, getattr(parref, 'parnum', '')))
        elif scope == 'col':
            for p, r in self.parlocs.getParasByColumnOrParref(parref=parref):
                refs2del.append((p.ref, getattr(p, 'parnum', '')))
        elif scope == 'page':
            for p, r in self.parlocs.getParas(pgindx):
                refs2del.append((p.ref, getattr(p, 'parnum', '')))
        elif scope == 'sprd':
            for pg in self.get_spread(pgindx):
                for p, r in self.parlocs.getParas(pg):
                    refs2del.append((p.ref, getattr(p, 'parnum', '')))
        
        # Remove duplicates while preserving order
        refs2del = list(dict.fromkeys(refs2del)) 
        refs2del = refs2del[1:] if pgindx > 1 and len(refs2del) > 1 else refs2del

        # x = '\n'.join(map(str, refs2del))
        # print(f"\n\nDeleting Adjustments for:\n{x}\n")
        model = self.adjlist.liststore
        for row in model:
            row_ref = (row[0] + str(row[1]), int(row[2]))
            if row_ref in refs2del:
                model.remove(row.iter)
            
        self.show_pdf()
        self.hitPrint()

    def on_shrink_text(self, widget, info, parref):
        if self.adjlist is not None:
            if info[1] - self.shrinkStep < self.shrinkLimit:
                self.adjlist.expand(info[2], self.shrinkLimit - info[1], mrk=parref.mrk)
            else:
                self.adjlist.expand(info[2], -self.shrinkStep, mrk=parref.mrk)
        self.show_pdf()
        self.hitPrint()

    def on_expand_text(self, widget, info, parref):
        if self.adjlist is not None:
            if info[1] + self.expandStep > self.expandLimit:
                self.adjlist.expand(info[2], self.expandLimit - info[1], mrk=parref.mrk)
            else:
                self.adjlist.expand(info[2], self.expandStep, mrk=parref.mrk)
        self.show_pdf()
        self.hitPrint()

    def edit_style(self, widget, a):
        (mkr, pref) = a
        if pref != self.currpref:
            if self.currpref is not None:
                self.model.onOK(None)
            if pref is not None:
                self.model.switchToDiglot(pref)
            self.currpref = pref
        if mkr is not None:
            self.model.styleEditor.selectMarker(mkr)
            mpgnum = self.model.notebooks['Main'].index("tb_StyleEditor")
            self.model.builder.get_object("nbk_Main").set_current_page(mpgnum)
            self.model.mainapp.win.present()
            self.model.wiggleCurrentTabLabel()
        
    def edit_fig_style(self, widget):
        self.model.styleEditor.selectMarker('fig')
        mpgnum = self.model.notebooks['Main'].index("tb_StyleEditor")
        self.model.builder.get_object("nbk_Main").set_current_page(mpgnum)
        self.model.mainapp.win.present()
        self.model.wiggleCurrentTabLabel()
        
    def cleanRef(self, reference):
        ''' JHN1.4 --> JHN 1:4, MRKL12.14 --> MRK 12:14 '''
        pattern = r"([123A-Z]{3})\s?(?:[LRA-G]?)(\d+)\.(\d+)"
        match = re.match(pattern, reference)
        if not match:
            return reference
        book, chapter, verse = match.groups()
        return f"{book} {chapter}:{verse}"
    
    def on_broadcast_ref(self, widget, ref):
        if not sys.platform.startswith("win"):
            return

        key_path = r"Software\SantaFe\Focus\ScriptureReference"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        except FileNotFoundError:
            logger.debug(f"Error: Registry Key not found: {path}")
            return

        try:
            if key is not None:
                vref = self.cleanRef(ref)
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, vref)
                winreg.CloseKey(key)
                logger.debug(f"Set Scr Ref in registry to: {vref}")
        except WindowsError as e:
            logger.debug(f"Error: {e} while trying to set ref in registry")
            return

        # Load user32.dll
        user32 = ctypes.windll.user32

        # Define argument and return types for RegisterWindowMessage and PostMessage
        user32.RegisterWindowMessageW.argtypes = [wintypes.LPCWSTR]  # Wide string
        user32.RegisterWindowMessageW.restype = wintypes.UINT        # Unsigned int

        user32.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
        user32.PostMessageW.restype = wintypes.BOOL                  # Boolean return

        # Step 1: Register the custom Windows message
        santa_fe_focus_msg = user32.RegisterWindowMessageW("SantaFeFocus")
        if not santa_fe_focus_msg:
            raise ctypes.WinError(ctypes.get_last_error())

        # Step 2: Post the message to all top-level windows (-1 or HWND_BROADCAST)
        HWND_BROADCAST = 0xFFFF  # -1 in the Windows API means broadcasting to all top-level windows
        WPARAM = 1               # Parameter for the message
        LPARAM = 0               # Additional parameter for the message

        # Post the message
        success = user32.PostMessageW(HWND_BROADCAST, santa_fe_focus_msg, WPARAM, LPARAM)
        if not success:
            raise ctypes.WinError(ctypes.get_last_error())
        logger.debug(f"Message 'SantaFeFocus' ({santa_fe_focus_msg}) posted successfully!")

