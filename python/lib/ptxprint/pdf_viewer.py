import gi, os, datetime
gi.require_version("Gtk", "3.0")
gi.require_version("Poppler", "0.18")
from gi.repository import Gtk, Poppler, GdkPixbuf, Gdk, GLib
import cairo, re, time, sys
import numpy as np
from cairo import ImageSurface, Context
from colorsys import rgb_to_hsv, hsv_to_rgb
from ptxprint.utils import _, refSort
from pathlib import Path
from dataclasses import dataclass, InitVar, field
from threading import Timer
import logging
logger = logging.getLogger(__name__)

def render_page_image(page, zoomlevel, pnum, annotatefn):
    width, height = page.get_size()
    width, height = int(width * zoomlevel), int(height * zoomlevel)
    buf = bytearray(width * height * 4)
    render_page(page, zoomlevel, buf, pnum, annotatefn)
    return arrayImage(buf, width, height)

def render_page(page, zoomlevel, imarray, pnum, annotatefn):
    # Get page size, applying zoom factor
    width, height = page.get_size()
    width, height = width * zoomlevel, height * zoomlevel

    surface = ImageSurface.create_for_data(memoryview(imarray), cairo.FORMAT_ARGB32, int(width), int(height))
    context = Context(surface)
    context.set_source_rgb(1, 1, 1)
    context.paint()
    context.scale(zoomlevel, zoomlevel)
    page.render(context)
    if annotatefn is not None:
        annotatefn(pnum, context, zoomlevel)

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
    def __init__(self, model, widget, tv): # widget is bx_previewPDF (which will have 2x .hbox L/R pages inside it)
        self.hbox = widget
        self.model = model
        self.sw = widget.get_parent()
        self.sw.connect("button-press-event", self.on_button_press)
        self.sw.connect("button-release-event", self.on_button_release)
        self.sw.connect("motion-notify-event", self.on_mouse_motion)
        self.swh = self.sw.get_hadjustment()
        self.swv = self.sw.get_vadjustment()
        self.toctv = tv
        cr = Gtk.CellRendererText()
        tvc = Gtk.TreeViewColumn("Title", cr, text=0)
        self.toctv.append_column(tvc)
        self.toctv.connect("row-activated", self.pickToc)
        self.numpages = 0
        self.document = None
        self.current_page = None  # Keep track of the current page number
        self.zoomLevel = 1.0  # Initial zoom level is 100%
        self.old_zoom = 1.0
        self.spread_mode = self.model.get("c_bkView", False)
        self.parlocs = None
        self.psize = (0, 0)
        # self.drag_start_x = None
        # self.drag_start_y = None
        self.is_dragging = False
        self.adjlist = None
        self.timer = None
        self.showadjustments = True

        # Enable focus and event handling
        self.hbox.set_can_focus(True)
        self.hbox.add_events(Gdk.EventMask.SCROLL_MASK | Gdk.EventMask.BUTTON_PRESS_MASK)

        # Connect keyboard events
        self.hbox.connect("key-press-event", self.on_key_press_event)
        self.hbox.connect("scroll-event", self.on_scroll_event)
        self.hbox.set_can_focus(True)  # Ensure the widget can receive keyboard focus

    def setShowAdjOverlay(self, val):
        self.showadjustments = val
        self.show_pdf()

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
                # event_box.connect("button-press-event", self.on_button_press)
                # event_box.connect("motion-notify-event", self.on_mouse_motion)
                event_box.connect("button-release-event", self.on_button_release)
                if self.rtl_mode:
                    self.hbox.pack_end(event_box, False, False, 1)
                else:
                    self.hbox.pack_start(event_box, False, False, 1)
                boxes.append(event_box)

    def update_boxes(self, images):
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

    def load_pdf(self, pdf_path, adjlist=None, start=None, isdiglot=False):
        self.shrinkStep = int(self.model.get('s_shrinktextstep'))
        self.expandStep = int(self.model.get('s_expandtextstep'))
        self.shrinkLimit = int(self.model.get('s_shrinktextlimit'))
        self.expandLimit = int(self.model.get('s_expandtextlimit'))
        
        self.isdiglot = isdiglot
        if pdf_path is None or not os.path.exists(pdf_path):
            self.document = None
            return False

        file_uri = Path(pdf_path).as_uri()
        try:
            self.document = Poppler.Document.new_from_file(file_uri, None)
            self.numpages = self.document.get_n_pages()
        except Exception as e:
            self.model.doStatus(_("Error opening PDF: ").format(e))
            self.document = None
            return False
        tocts = self.load_toc(self.document)
        self.toctv.set_model(tocts)
        
        self.adjlist = adjlist
        if start is not None and start < self.numpages:
            self.current_page = start
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
        #print(f"TOC: {title}, {pnum}")
        parent = tocts.append(parent, [title, pnum])
        toci = toci.get_child()
        havei = toci is not None
        while havei:
            self._add_toctree(tocts, toci, parent)
            havei = toci.next()

    def load_toc(self, document):
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
        return res

    def pickToc(self, tv, path, col):
        pnum = tv.get_model()[path][1]
        self.show_pdf(pnum)

    def show_pdf(self, page=None, rtl=False, setpnum=True):
        if self.document is None:
            self.clear()
            return
        if page is None:
            page = self.current_page or 1
        if setpnum and self.model.get("s_pgNum") != str(page):
            self.model.set("s_pgNum", page, mod=False)
            return
        if self.model.get("fcb_pagesPerSpread", "1") != "1":
            self.spread_mode = False
        else:
            self.spread_mode = self.model.get("c_bkView", False)
        self.rtl_mode = self.model.get("c_RTLbookBinding", False)

        images = []
        if self.spread_mode:
            spread = self.get_spread(page, self.rtl_mode)
            self.create_boxes(len(spread))
            for i in spread:
                if i in range(self.numpages+1):
                    pg = self.document.get_page(i-1)
                    self.psize = pg.get_size()
                    images.append(render_page_image(pg, self.zoomLevel, i, self.add_hints if self.showadjustments else None))
        else:
            if page in range(self.numpages+1):
                self.create_boxes(1)
                pg = self.document.get_page(page-1)
                self.psize = pg.get_size()
                images.append(render_page_image(pg, self.zoomLevel, page, self.add_hints if self.showadjustments else None))

        self.current_page = page
        self.update_boxes(images)

    # incomplete code calling for major refactor for cairo drawing
    def add_hints(self, page, context, zoomlevel):
        def make_rect(context, col, r, offset):
            red, green, blue = hsv_to_rgb(*col)
            context.set_source_rgba(red, green, blue, 0.4)
            context.rectangle((r.xstart if offset >= 0 else r.xend + offset),
                              (self.psize[1] - r.ystart), abs(offset), (r.ystart - r.yend))
            context.fill()
        bk = None
        for p, r in self.parlocs.getParas(page):
            nbk = getattr(p, "ref", bk or "")[:3].upper()
            if not len(nbk):
                continue
            if nbk != bk:
                adjlist = self.model.get_adjlist(nbk, gtk=Gtk)
                bk = nbk
            pnum = f"[{p.parnum}]" if getattr(p, 'parnum', 1) > 1 else ""
            ref = getattr(p, 'ref', (bk or "") + "0.0") + pnum
            info = adjlist.getinfo(ref)
            if not info:
                continue
            col = None
            s = info[0]
            sv = int(re.sub(r"^[+-]*", "", s))
            sv = -sv if "-" in s else sv
            if sv != 0:
                # hsv(hue, saturation full colour at 1, black/white at 0, white at 1 and black at 0)
                col = (202 / 255., 1., 1.) if sv < 0 else (0., 1., 1.)
                make_rect(context, col, r, abs(sv) * 3)
            if info[1] != 100:
                col = (41 / 255., 1., 1.) if info[1] < 100 else (173 / 255., 1., 1.)
                make_rect(context, col, r, abs(100 - info[1]) * -1)

    def loadnshow(self, fname, rtl=False, adjlist=None, parlocs=None, widget=None, page=None, isdiglot=False):
        if fname is None:
            return False
        if not self.load_pdf(fname, adjlist=adjlist, start=page, isdiglot=isdiglot):
            return False
        if parlocs is not None:     # and not isdiglot:
            self.load_parlocs(parlocs, rtl=rtl)
        self.show_pdf(rtl=rtl)
        pdft = os.stat(fname).st_mtime
        mod_time = datetime.datetime.fromtimestamp(pdft)
        formatted_time = mod_time.strftime("   %d-%b %H:%M")
        widget.set_title(_("PDF Preview:") + " " + os.path.basename(fname) + formatted_time)
        # Set the number of pages/spreads in the contents area
        pgSprds = _("pages") if self.model.get("fcb_pagesPerSpread", "1") == "1" else _("spreads")
        self.model.set_preview_pages(self.numpages, pgSprds)
        widget.show_all()
        return True

    def clear(self, widget=None):
        self.create_boxes(0)
        self.document = None
        m = self.toctv.get_model()
        if m:
            m.clear()
        if widget is not None:
            widget.set_title(_("PDF Preview:"))
        self.model.set_preview_pages(None)

    def set_zoom(self, zoomLevel, scrolled=False, setz=True):
        if zoomLevel == self.zoomLevel:
            return
        if setz and self.model.get("s_pdfZoomLevel") != str(int(zoomLevel * 100)):
            self.model.set("s_pdfZoomLevel", zoomLevel*100, mod=False)
            return
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
            GLib.idle_add(self.show_pdf)
        if self.timer is not None:
            self.timer.cancel()
        if scrolled:
            self.timer = Timer(0.3, redraw)
            self.timer.start()
        else:
            redraw()

    def load_parlocs(self, fname, rtl=False):
        self.parlocs = Paragraphs()
        self.parlocs.readParlocs(fname, rtl=rtl)

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
               self.show_previous_page()
            elif event.direction == Gdk.ScrollDirection.DOWN:
               self.show_next_page()
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

    def show_next_page(self):
        next_page = min(self.current_page + (2 if self.spread_mode else 1), self.numpages)
        self.show_pdf(next_page)

    def show_previous_page(self):
        previous_page = max(self.current_page - (2 if self.spread_mode else 1), 1)
        self.show_pdf(previous_page)

    # Handle keyboard shortcuts for navigation
    def on_key_press_event(self, widget, event):
        keyval = event.keyval
        state = event.state
        # Check if Control key is pressed
        ctrl = (state & Gdk.ModifierType.CONTROL_MASK)

        if ctrl and keyval == Gdk.KEY_Home:  # Ctrl+Home (Go to first page)
            self.show_pdf(1)
            return True
        elif ctrl and keyval == Gdk.KEY_End:  # Ctrl+End (Go to last page)
            p = self.numpages
            self.show_pdf(p)
            return True
        elif keyval == Gdk.KEY_Page_Down:  # Page Down (Next page/spread)
            next_page = self.current_page + (2 if self.spread_mode else 1)
            p = min(next_page, self.numpages)
            self.show_pdf(p)
            return True
        elif keyval == Gdk.KEY_Page_Up:  # Page Up (Previous page/spread)
            prev_page = self.current_page - (2 if self.spread_mode else 1)
            p = max(prev_page, 1)
            self.show_pdf(p)
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
            # print(f"Zoom reset to actual size: {self.zoomLevel=:.2f}")
            return True
        elif ctrl and keyval in {Gdk.KEY_F, Gdk.KEY_f}:  # Ctrl+F (Fit to screen)
            self.set_zoom_fit_to_screen(None)
            # print(f"Zoom adjusted to fit screen: {self.zoomLevel=:.2f}")
            self.show_pdf()  # Redraw the current page
            return True
            
    def get_spread(self, page, rtl=False):
        if page == 1:
            return (1,)
        if page > int(self.numpages):
            page = int(self.numpages)
        if page % 2 == 0:
            page += 1
        if page > int(self.numpages):
            return (page - 1,)
        if rtl:
            return (page, page - 1)
        else:
            return (page - 1, page)

    def on_button_press(self, widget, event):
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

    def get_parloc(self, widget, event):
        x = event.x / self.zoomLevel
        y = event.y / self.zoomLevel
        if self.spread_mode:
            side = self.widgetPosition(widget)
            if len(self.hbox.get_children()) > 1 and self.rtl_mode:
                side ^= 1 # swap side if RTL
            pnum = self.get_spread(self.current_page)[side]     # this all only works for LTR
        else:
            pnum = self.current_page
        p = None
        a = self.hbox.get_allocation()

        if self.parlocs is not None:
            p = self.parlocs.findPos(pnum, x, self.psize[1] - y, rtl=self.rtl_mode)
        # print(f"Parloc: {p=} {pnum=} {x=} y={self.psize[1]-y}   {self.psize=}   {a.x=} {a.y=}")
        return p

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

    def addSubMenuItem(self, parent_menu, label, submenu):
        menu_item = Gtk.MenuItem(label=label)  # Create a menu item for the parent
        menu_item.set_submenu(submenu)         # Attach the submenu
        parent_menu.append(menu_item)          # Add the parent item to the parent menu
        menu_item.show()                       # Show the parent item

    def show_context_menu(self, widget, event):
        menu = Gtk.Menu()
        ys        = _("Yes! Shrink")
        ts        = _("Try Shrink")
        expand    = _("Expand")
        minusline = _("-1 line")
        plusline  = _("+1 line")
        rp        = _("Reset Paragraph")
        st        = _("Shrink Text")
        et        = _("Expand Text")
        es        = _("Edit Style")
        z2f       = _("Zoom to Fit")
        z100      = _("Zoom 100%")
        if False and self.isdiglot:
            info = []
        else:
            parref = self.get_parloc(widget, event)
            if parref is None:
                info = []
            else:
                pnum = f"[{parref.parnum}]" if getattr(parref, 'parnum', 0) > 1 else ""
                ref = parref.ref
                self.adjlist = self.model.get_adjlist(ref[:3].upper(), gtk=Gtk)
                if self.adjlist is not None:
                    info = self.adjlist.getinfo(ref + pnum, insert=True)

        logger.debug(f"{parref=} {info=} ({event.x},{event.y})")
        if len(info) and self.model.get("fcb_pagesPerSpread", "1") == "1": # don't allow when 2-up or 4-up is enabled!
            o = 4 if ref[3:4] in ("L", "R", "A", "B", "C", "D", "E", "F") else 3
            l = info[0]
            if l[0] not in '+-':
                l = '+' + l
            hdr = f"{ref[:o]} {ref[o:]}{pnum}   \\{parref.mrk}  {l}  {info[1]}%"
            self.addMenuItem(menu, hdr, self.on_identify_paragraph, info, sensitivity=False)
            self.addMenuItem(menu, None, None)

            x = ys if ("-" in str(info[0]) and str(info[0]) != "-1") else ts
            self.addMenuItem(menu, f"{x} {minusline} ({parref.lines - 1})", self.on_shrink_paragraph, info, parref)
            self.addMenuItem(menu, f"{expand} {plusline} ({parref.lines + 1})", self.on_expand_paragraph, info, parref)
            self.addMenuItem(menu, None, None)
            self.addMenuItem(menu, f"{rp}", self.on_reset_paragraph, info, parref, sensitivity=not (info[1] == 100 and int(l.replace("+","")) == 0))
            self.addMenuItem(menu, None, None)

            shrLim = max(self.shrinkLimit, info[1]-self.shrinkStep)
            self.addMenuItem(menu, f"{st} ({shrLim}%)", self.on_shrink_text, info, parref, sensitivity=not info[1] <= shrLim)

            expLim = min(self.expandLimit, info[1]+self.expandStep)
            self.addMenuItem(menu, f"{et} ({expLim}%)", self.on_expand_text, info, parref, sensitivity=not info[1] >= expLim)
            self.addMenuItem(menu, None, None)
            if parref and parref.mrk is not None:
                self.addMenuItem(menu, f"{es} \\{parref.mrk}", self.edit_style, parref.mrk)
        else:
            # New section for image context menu
            imgref = self.get_imageref(widget, event)  # Assuming a method to get the image reference
            if False:
                self.addMenuItem(menu, _("Change Anchor Ref"), self.on_edit_anchor, imgref)

                class_menu = Gtk.Menu()
                for class_option in ["Column", "Span", "Cutout", "Page", "Full"]:
                    self.addMenuItem(class_menu, class_option, self.on_set_image_class, (imgref, class_option))
                self.addSubMenuItem(menu, _("Class of Position"), class_menu)

                position_menu = Gtk.Menu()
                for position_option in ["Top", "Bottom", "Inner", "Outer", "Left", "Right"]:
                    self.addMenuItem(position_menu, position_option, self.on_set_image_position, (imgref, position_option))
                self.addSubMenuItem(menu, _("Position"), position_menu)

                self.addMenuItem(menu, None, None)
                self.addMenuItem(menu, _("Shrink 5% size"), self.on_shrink_image, imgref)
                self.addMenuItem(menu, _("Grow 5% size"), self.on_grow_image, imgref)

                mirror_here_menu = Gtk.Menu()
                for mirror_here_option in ["Never", "Always", "If on odd page", "If on even page", ]:
                    self.addMenuItem(mirror_here_menu, mirror_here_option, self.on_set_mirror_here, (imgref, mirror_here_option))
                self.addSubMenuItem(menu, _("Mirror Here"), mirror_here_menu)
                    
                mirror_all_menu = Gtk.Menu()
                for mirror_all_option in ["Never", "Always", "If on odd page", "If on even page", ]:
                    self.addMenuItem(mirror_all_menu, mirror_all_option, self.on_set_mirror_all, (imgref, mirror_all_option))
                self.addSubMenuItem(menu, _("Mirror Always"), mirror_all_menu)
                    
                self.addMenuItem(menu, _("Reset Image to Defaults"), self.on_reset_image, imgref)
                self.addMenuItem(menu, f"{es} \\fig", self.edit_fig_style)
                self.addMenuItem(menu, None, None)
        self.addMenuItem(menu, f"{z2f} (Ctrl + F)", self.set_zoom_fit_to_screen)
        self.addMenuItem(menu, f"{z100} (Ctrl + 0)", self.on_reset_zoom)

        menu.popup(None, None, None, None, event.button, event.time)

    def get_imageref(self, widget, event):
        return True

    def on_edit_anchor(self, imgref):
        print(f"Editing anchor for image: {imgref}")

    def on_set_image_class(self, imgref, class_option):
        print(f"Setting class '{class_option}' for image: {imgref}")

    def on_set_image_position(self, imgref, position_option):
        print(f"Setting position '{position_option}' for image: {imgref}")

    def on_shrink_image(self, imgref):
        print(f"Shrinking image: {imgref}")

    def on_grow_image(self, imgref):
        print(f"Growing image: {imgref}")

    def on_reset_image(self, imgref):
        print(f"Resetting image to defaults: {imgref}")

    def on_set_mirror_here(self, imgref):
        print(f"Mirror here: {imgref}")

    def on_set_mirror_all(self, imgref):
        print(f"Mirror all: {imgref}")

    # Context menu item callbacks for paragraph actions
    def on_identify_paragraph(self, widget, info, parref):
        print("Identify paragraph option selected")

    def on_shrink_paragraph(self, widget, info, parref):
        if self.adjlist is not None:
            self.adjlist.increment(info[2], -1)
        self.show_pdf()

    def on_expand_paragraph(self, widget, info, parref):
        if self.adjlist is not None:
            self.adjlist.increment(info[2], 1)
        self.show_pdf()
        
    def on_reset_paragraph(self, widget, info, parref):
        if self.adjlist is not None:
            pc = int(info[0].replace("+-", "-"))
            self.adjlist.increment(info[2], - pc)
            self.adjlist.expand(info[2], 100 - info[1], mrk=parref.mrk)
        self.show_pdf()

    def on_shrink_text(self, widget, info, parref):
        if self.adjlist is not None:
            if info[1] - self.shrinkStep < self.shrinkLimit:
                self.adjlist.expand(info[2], self.shrinkLimit - info[1], mrk=parref.mrk)
            else:
                self.adjlist.expand(info[2], -self.shrinkStep, mrk=parref.mrk)
        self.show_pdf()

    # def on_normal_text(self, widget, info, parref):
        # if self.adjlist is not None:
            # self.adjlist.expand(info[2], 100 - info[1], mrk=parref.mrk)
        # self.show_pdf()

    def on_expand_text(self, widget, info, parref):
        if self.adjlist is not None:
            if info[1] + self.expandStep > self.expandLimit:
                self.adjlist.expand(info[2], self.expandLimit - info[1], mrk=parref.mrk)
            else:
                self.adjlist.expand(info[2], self.expandStep, mrk=parref.mrk)
        self.show_pdf()

    def edit_style(self, widget, mkr):
        if mkr is not None:
            self.model.styleEditor.selectMarker(mkr)
            mpgnum = self.model.notebooks['Main'].index("tb_StyleEditor")
            self.model.builder.get_object("nbk_Main").set_current_page(mpgnum)
            self.model.wiggleCurrentTabLabel()
        
    def edit_fig_style(self, widget):
        self.model.styleEditor.selectMarker('fig')
        mpgnum = self.model.notebooks['Main'].index("tb_StyleEditor")
        self.model.builder.get_object("nbk_Main").set_current_page(mpgnum)
        self.model.wiggleCurrentTabLabel()
        
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

    def _saveSetting(self, key, value):
        self.model.userconfig.set('printer', key, value)

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


def readpts(s):
    s = re.sub(r"(?:\s*(?:plus|minus)\s+[-\d.]+\s*(?:pt|in|sp|em))+$", "", s)
    if s.endswith("pt"):
        return float(s[:-2])
    elif s.endswith("in"):
        return float(s[:-2]) * 72
    elif s.endswith("sp"):
        return float(s[:-2]) / 65536.
    else:
        return float(s) / 65536.

@dataclass
class ParRect:
    pagenum:    int
    xstart:     float
    ystart:     float
    xend:       float = 0.
    yend:       float = 0.
    
    def __str__(self):
        return f"{self.pagenum} ({self.xstart},{self.ystart}-{self.xend},{self.yend})"

    def __repr__(self):
        return self.__str__()

@dataclass
class ParInfo:
    ref:        str
    partype:    str
    mrk:        str
    baseline:   float
    rects:      InitVar[None] = None

    def __str__(self):
        return f"{self.ref}[{getattr(self, 'parnum', '')}] {self.baseline} {self.rects}"

    def __repr__(self):
        return self.__str__()

    def sortKey(self):
        return (self.rects[-1].pagenum, refSort(self.ref), getattr(self, 'parnum', 0))

class ParlocLinesIterator:
    def __init__(self, fname):
        self.fname = fname
        self.collection = []
        self.replay = False

    def __iter__(self):
        if os.path.exists(self.fname):
            with open(self.fname, encoding="utf-8") as inf:
                self.lines = inf.readlines()
        else:
            self.lines = []
        return self

    def __next__(self):
        if self.replay:
            if len(self.collection):
                return self.collection.pop(0)
            else:
                self.replay = False
        if not len(self.lines):
            raise StopIteration
        return self.lines.pop(0)

    def collectuntil(self, limit, lines):
        self.collection = lines
        while len(self.lines):
            l = self.lines.pop(0)
            self.collection.append(l)
            if l.startswith(limit):
                break

    def startreplay(self):
        if len(self.collection):
            self.replay = True
            logger.log(7, "Starting replay of {len(self.collection)} lines")

class Paragraphs(list):
    parlinere = re.compile(r"^\\@([a-zA-Z@]+)\s*\{(.*?)\}\s*$")

    def readParlocs(self, fname, rtl=False):
        self.pindex = []
        currp = None
        currr = None
        endpar = True
        inpage = False
        pnum = 0
        polycol = "L"
        currps = {polycol: None}
        colinfos = {}
        innote = False
        pwidth = 0.
        lines = ParlocLinesIterator(fname)
        for l in lines:
            m = self.parlinere.match(l)
            if not m:
                continue
            logger.log(5, l[:-1])
            c = m.group(1)
            p = m.group(2).split("}{")
            if c == "pgstart":          # pageno, available height, pagewidth, pageheight
                pnum += 1
                if len(p) > 3:
                    pwidth = readpts(p[2])
                else:
                    pwidth = 0.
                self.pindex.append(len(self))
                inpage = True
                cinfo = [readpts(x) for x in p[1:4]]
                colinfos[polycol] = [cinfo[0], 0, cinfo[1], 0, cinfo[2]]
            elif c == "parpageend":     # bottomx, bottomy, type=bottomins, notes, verybottomins, pageend
                pginfo = [readpts(x) for x in p[:2]] + [p[2]]
                inpage = False
            elif c == "colstart":       # col height, col depth, col width, topx, topy
                cinfo = [readpts(x) for x in p]
                logger.log(5, f"Test replay: {lines.replay} {pwidth=} width={cinfo[2]} left={cinfo[3]}")
                if rtl and not lines.replay and ((pwidth == 0. and cinfo[3] > cinfo[2]) or (cinfo[3] + cinfo[2]) * 2 < pwidth):
                    # right column. So swap it
                    logger.debug(f"Start column swap at {cinfo}")
                    lines.collectuntil("\\@colstop", [l])
                    continue
                colinfos[polycol] = cinfo
                if currps[polycol] is not None:
                    currr = ParRect(pnum, cinfo[3], cinfo[4])
                    currps[polycol].rects.append(currr)
            elif c == "colstop" or c == "Poly@colstop":     # bottomx, bottomy [, polycode]
                if currr is not None:
                    cinfo = colinfos[polycol]
                    currr.xend = cinfo[3] + cinfo[2]
                    currr.yend = readpts(p[1])
                    currr = None
                lines.startreplay()
            elif c == "parstart":       # mkr, baselineskip, partype=section etc., startx, starty
                # print(f"{p=}")
                if len(p) == 5:
                    p.insert(0, "")
                logger.log(5, f"Starting para {p[0]}")
                currp = ParInfo(p[0], p[1], p[2], readpts(p[3]))
                currp.rects = []
                cinfo = colinfos[polycol]
                currr = ParRect(pnum, cinfo[3], readpts(p[5]) + currp.baseline)
                currp.rects.append(currr)
                currps[polycol] = currp
                self.append(currp)
            elif c == "parend":         # badness, bottomx, bottomy
                cinfo = colinfos[polycol]
                if currps[polycol] is None:
                    continue
                currr.xend = cinfo[3] + cinfo[2]    # p[1] is xpos of last char in par
                if len(p) > 2:
                    currps[polycol].lines = int(p[0])
                    currr.yend = readpts(p[2])
                else:
                    currr.yend = readpts(p[1])
                endpar = True
            elif c == "parlen":         # ref, stretch, numlines, marker, adjustment
                if not endpar:
                    continue
                endpar = False
                currp = currps[polycol]
                if currp is None:
                    continue
                currp.lastref = p[0]
                currp.parnum = int(p[1])
                currp.lines = int(p[2]) # this seems to be the current number of lines in para
                # currp.badness = p[4]  # current p[4] = p[1] = parnum (badness not in @parlen yet)
                currps[polycol] = None
                currr = None
            elif c == "Poly@colstart": # height, depth, width, topx, topy, polycode
                polycol = p[5]
                colinfos[polycol] = [readpts(x) for x in p[:-1]]
                cinfo = colinfos[polycol]
                if polycol not in currps:
                    currps[polycol] = None
                if currps[polycol] is not None:
                    currr = ParRect(pnum, cinfo[3], cinfo[4])
                    currps[polycol].rects.append(currr)
            # "parnote":        # type, callerx, callery
            # "notebox":        # type, width, height
            # "parlines":       # numlines in previous paragraph (occurs after @parlen)
        self.sort(key=lambda x:x.sortKey())
        logger.log(7, "parlocs=" + "\n".join([str(p) for p in self]))
        
    def findPos(self, pnum, x, y, rtl=False):
        done = False
        # just iterate over paragraphs on this page
        if pnum > len(self.pindex):
            return None
        e = self.pindex[pnum] if pnum < len(self.pindex) else len(self)

        logger.debug(f"Parloc testing: {self.pindex[pnum-1]-1} -> {e}")
        for p in self[max(self.pindex[pnum-1]-1, 0):e+1]:
            for i,r in enumerate(p.rects):
                if r.pagenum > pnum:
                    if rtl and i != 0:
                        continue
                    done = True
                    break
                elif r.pagenum < pnum:
                    continue
                logger.log(7, f"Testing {r} against ({x},{y})")
                if r.xstart <= x and x <= r.xend and r.ystart >= y and r.yend <= y:
                    return p
            if done:
                break
        return None

    def getParas(self, pnum):
        if pnum > len(self.pindex):
            return
        e = self.pindex[pnum] if pnum < len(self.pindex) else len(self)

        for p in self[max(self.pindex[pnum-1]-1, 0):e+1]:
            for r in p.rects:
                if r.pagenum > pnum:
                    done = True
                    break
                elif r.pagenum < pnum:
                    continue
                yield (p, r)
