import gi, os, datetime
gi.require_version("Gtk", "3.0")
gi.require_version("Poppler", "0.18")
from gi.repository import Gtk, Poppler, GdkPixbuf, Gdk, GLib
import cairo, re, time, sys
from cairo import ImageSurface, Context
from colorsys import rgb_to_hsv, hsv_to_rgb
from ptxprint.utils import _
from pathlib import Path
from threading import Thread, Event, Timer
from dataclasses import dataclass, InitVar, field
from multiprocessing import sharedctypes, Process
import logging
logger = logging.getLogger(__name__)

def render_page_image(page, zoomlevel):
    width, height = page.get_size()
    width, height = int(width * zoomlevel), int(height * zoomlevel)
    buf = bytearray(width * height * 4)
    render_page(page, zoomlevel, buf)
    return arrayImage(buf, width, height)

def render_page(page, zoomlevel, imarray):
    # Get page size, applying zoom factor
    width, height = page.get_size()
    width, height = width * zoomlevel, height * zoomlevel

    surface = ImageSurface.create_for_data(memoryview(imarray), cairo.FORMAT_RGB24, int(width), int(height))
    context = Context(surface)
    context.set_source_rgb(1, 1, 1)
    context.paint()
    context.scale(zoomlevel, zoomlevel)
    page.render(context)

def arrayImage(imarray, width, height):
    stride = cairo.Format.RGB24.stride_for_width(width)
    pixbuf = GdkPixbuf.Pixbuf.new_from_data(
        bytes(imarray),
        GdkPixbuf.Colorspace.RGB,
        True,
        8,
        width, height, stride)
    return Gtk.Image.new_from_pixbuf(pixbuf)


class PDFViewer:
    def __init__(self, model, widget): # widget is bx_previewPDF (which will have 2x .hbox L/R pages inside it)
        self.hbox = widget
        self.model = model
        self.numpages = 0
        self.current_page = None  # Keep track of the current page number
        self.zoomLevel = 1.0  # Initial zoom level is 100%
        self.old_zoom = 1.0
        self.spread_mode = self.model.get("c_bkView", False)
        self.parlocs = None
        self.psize = (0, 0)
        # self.drag_start_x = None
        # self.drag_start_y = None
        # self.is_dragging = False
        self.thread = None
        self.timer = None
        self.adjlist = None

        # Enable focus and event handling
        self.hbox.set_can_focus(True)
        self.hbox.add_events(Gdk.EventMask.SCROLL_MASK | Gdk.EventMask.BUTTON_PRESS_MASK)

        # Connect keyboard events
        self.hbox.connect("key-press-event", self.on_key_press_event)
        self.hbox.connect("scroll-event", self.on_scroll_event)
        self.hbox.set_can_focus(True)  # Ensure the widget can receive keyboard focus

    def exit(self):
        if self.thread is not None:
            self.thread.kill()

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
        file_uri = Path(pdf_path).as_uri()
        try:
            self.document = Poppler.Document.new_from_file(file_uri, None)
            self.numpages = self.document.get_n_pages()
        except Exception as e:
            print(f"Error opening PDF: {e}")
            return
        self.adjlist = adjlist
        if start is not None and start < self.numpages:
            self.current_page = start

    def show_pdf(self, page, rtl=False):
        if page is None:
            page = 1
        self.spread_mode = self.model.get("c_bkView", False)
        self.rtl_mode = self.model.get("c_RTLbookBinding", False)

        self.pages = []
        images = []
        if self.spread_mode:
            spread = self.get_spread(page, self.rtl_mode)
            self.create_boxes(len(spread))
            for i in spread:
                if i in range(self.numpages+1):
                    pg = self.document.get_page(i-1)
                    self.pages.append(pg)
                    self.psize = pg.get_size()
                    images.append(render_page_image(pg, self.zoomLevel))
        else:
            if page in range(self.numpages+1):
                self.create_boxes(1)
                pg = self.document.get_page(page-1)
                self.pages.append(pg)
                self.psize = pg.get_size()
                images.append(render_page_image(pg, self.zoomLevel))

        self.current_page = page
        self.update_boxes(images)

    # incomplete code calling for major refactor for cairo drawing
    def add_hints(self, page, context):
        bk = None
        for p, r in self.parlocs.getParas(page):
            nbk = p.ref[:3].upper()
            if nbk != bk:
                adjlist = self.model.get_adjlist(nbk)
                bk = nbk
            pnum = f"[{parref.parnum}]" if parref.parnum > 1 else ""
            info = adjlist.getinfo(p.ref + pnum)
            if not info:
                continue
            s = info[0]
            sv = int(re.sub(r"^[+-]*", s))
            sv = -sv if "-" in s else sv
            if sv != 0:
                # hsv(hue, saturation full colour at 1, black/white at 0, white at 1 and black at 0)
                col = (202 / 255., 1., min(-sv * 0.5)) if sv < 0 else (0., 1., max(1. - sv * .25, 0))
                # insert rect r.xstart-6, r.ystart, r.xstart, r.yend
            if info[1] != 100:
                col = (173, 255, min(12.5 * info[1] - 1000, 255)) if info[1] < 100 else (41, 255, 1500 - 12.5 * info[1])
                # insert rect r.xend, r.ystart, r.xend + 6, r.yend

    def loadnshow(self, fname, rtl=False, adjlist=None, parlocs=None, widget=None, page=None, isdiglot=False):
        self.load_pdf(fname, adjlist=adjlist, start=page, isdiglot=isdiglot)
        self.show_pdf(self.current_page, rtl=rtl)
        pdft = os.stat(fname).st_mtime
        mod_time = datetime.datetime.fromtimestamp(pdft)
        formatted_time = mod_time.strftime("   %d-%b  %H:%M")
        widget.set_title("PDF Preview: " + os.path.basename(fname) + formatted_time)
        widget.show_all()
        if parlocs is not None:     # and not isdiglot:
            self.load_parlocs(parlocs)                    

    def resize_pdf(self, scrolled=False):
        if self.zoomLevel == self.old_zoom:
            return
        width, height = self.psize
        width, height = int(width * self.zoomLevel), int(height * self.zoomLevel)

        children = self.hbox.get_children()
        if not len(children):
            return self.show_pdf(self.current_page)

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
            GLib.idle_add(self.show_pdf, self.current_page)
        if self.timer is not None:
            self.timer.cancel()
        if scrolled:
            self.timer = Timer(0.3, redraw)
            self.timer.start()
        else:
            redraw()
        self.model.set("t_zoomLevel", str(int(self.zoomLevel*100))+"%")
        #if self.thread is None:
        #    self.thread = ThreadRenderer(parent=self)
        #GLib.idle_add(self.thread.render_pages, list(range(len(self.pages))), self.zoomLevel, width, height)
#        self.thread.render_pages(self.pages, self.zoomLevel)

    def set_zoom(self, zoomlevel, scrolled=False):
        if zoomlevel == self.zoomLevel:
            return
        self.old_zoom = self.zoomLevel
        self.zoomLevel = zoomlevel
        self.model.set("t_zoomLevel", str(int(self.zoomLevel*100))+"%")
        self.resize_pdf(scrolled=scrolled)
    
    def print_document(self, fitToPage=False):
        if not hasattr(self, 'document') or self.document is None:
            return
        self.fitToPage = fitToPage
        print_op = Gtk.PrintOperation()
        print_op.set_n_pages(self.numpages)
        print_op.connect("draw_page", self.on_draw_page)

        try:
            result = print_op.run(Gtk.PrintOperationAction.PRINT_DIALOG, None)
            if result == Gtk.PrintOperationResult.APPLY:
                print("Print job sent.")
            else:
                print("Print job canceled or failed.")
        except Exception as e:
            print(f"An error occurred while printing: {e}")

    def on_draw_page(self, operation, context, page_number):
        if not hasattr(self, 'document') or self.document is None:
            return

        pdf_page = self.document.get_page(page_number)

        cairo_context = context.get_cairo_context()
        cairo_context.save()
        
        # Set background color to white
        cairo_context.set_source_rgb(1, 1, 1)
        cairo_context.paint()

        # Get the dimensions of the PDF page
        width, height = pdf_page.get_size()

        if self.fitToPage:
            # Calculate scale factors to fit the page
            scale_x = context.get_width() / width
            scale_y = context.get_height() / height
            scale = min(scale_x, scale_y)  # Uniform scaling to maintain aspect ratio
            cairo_context.scale(scale, scale)
        else:
            # Render at actual size (1:1 scale)
            scale = 1
            cairo_context.scale(scale, scale)

        # Render the PDF page
        pdf_page.render(cairo_context)

        # Restore the original context state
        cairo_context.restore()

    def load_parlocs(self, fname):
        self.parlocs = Paragraphs()
        self.parlocs.readParlocs(fname)

    def on_scroll_event(self, widget, event):
        ctrl_pressed = event.state & Gdk.ModifierType.CONTROL_MASK

        if ctrl_pressed:  # Zooming with Ctrl + Scroll
            zoom_in = event.direction == Gdk.ScrollDirection.UP
            zoom_out = event.direction == Gdk.ScrollDirection.DOWN

            # Get mouse position relative to the widget
            mouse_x, mouse_y = event.x, event.y
            posn = self.widgetPosition(widget) # 0=left page; 1=right page

            # Perform zoom operation centered on mouse
            if zoom_in:
                self.zoom_at_point(mouse_x, mouse_y, posn, zoom_in=True)
            elif zoom_out:
                self.zoom_at_point(mouse_x, mouse_y, posn, zoom_in=False)

            return True  # Prevent further handling of the scroll event

        # Default behavior: Scroll for navigation
        if event.direction == Gdk.ScrollDirection.UP:
            self.show_previous_page()
        elif event.direction == Gdk.ScrollDirection.DOWN:
            self.show_next_page()

        return True

    def widgetPosition(self, widget):
        children = self.hbox.get_children()
        for index, child in enumerate(children):
            if child == widget:
                return index  # Return the position (index) of the widget
        return -1  # If widget is not found, return -1

    def zoom_at_point(self, mouse_x, mouse_y, posn, zoom_in):
        self.old_zoom = self.zoomLevel
        self.zoomLevel = (min(self.zoomLevel * 1.1, 10.0) if zoom_in else max(self.zoomLevel * 0.9, 0.3))
        scale_factor = self.zoomLevel / self.old_zoom

        self.resize_pdf(scrolled=True)
        # Get the parent scrolled window and its adjustments
        scrolled_window = self.hbox.get_parent()
        h_adjustment = scrolled_window.get_hadjustment()
        v_adjustment = scrolled_window.get_vadjustment()

        # Handle inactive scrollbars or default to zero
        h_value = h_adjustment.get_value() if h_adjustment else 0
        v_value = v_adjustment.get_value() if v_adjustment else 0

        # Page dimensions
        hbox_width  = self.hbox.get_allocated_width()
        page_width  = hbox_width / 2 if self.spread_mode else hbox_width

        # Set page_offset if on right page (posn: 0=left, 1=right)
        page_offset = (posn * page_width)
        
        # New scroll positions to keep focus on the cursor
        new_h_value = (scale_factor - 1) * (mouse_x + page_offset) + h_value 
        new_v_value = (scale_factor - 1) *  mouse_y                + v_value
        # new_h_value = max(new_h_value, 0)
        # new_v_value = max(new_v_value, 0)
        h_adjustment.set_upper(h_adjustment.get_upper() * scale_factor)
        v_adjustment.set_upper(v_adjustment.get_upper() * scale_factor)
        h_adjustment.set_value(new_h_value)
        v_adjustment.set_value(new_v_value)

        # Redraw the canvas with the updated zoom level

    def show_next_page(self):
        next_page = min(self.current_page + (2 if self.spread_mode else 1), self.numpages)
        self.model.set("s_pgNum", next_page)
        self.show_pdf(next_page)

    def show_previous_page(self):
        previous_page = max(self.current_page - (2 if self.spread_mode else 1), 1)
        self.model.set("s_pgNum", previous_page)
        self.show_pdf(previous_page)

    # Handle keyboard shortcuts for navigation
    def on_key_press_event(self, widget, event):
        keyval = event.keyval
        state = event.state
        # Check if Control key is pressed
        ctrl = (state & Gdk.ModifierType.CONTROL_MASK)

        if ctrl and keyval == Gdk.KEY_Home:  # Ctrl+Home (Go to first page)
            self.model.set("s_pgNum", 1)
            self.show_pdf(1)
            return True
        elif ctrl and keyval == Gdk.KEY_End:  # Ctrl+End (Go to last page)
            p = self.numpages
            self.model.set("s_pgNum", p)
            self.show_pdf(p)
            return True
        elif keyval == Gdk.KEY_Page_Down:  # Page Down (Next page/spread)
            next_page = self.current_page + (2 if self.spread_mode else 1)
            p = min(next_page, self.numpages)
            self.model.set("s_pgNum", p)
            self.show_pdf(p)
            return True
        elif keyval == Gdk.KEY_Page_Up:  # Page Up (Previous page/spread)
            prev_page = self.current_page - (2 if self.spread_mode else 1)
            p = max(prev_page, 1)
            self.model.set("s_pgNum", p)
            self.show_pdf(p)
            return True
        elif ctrl and keyval == Gdk.KEY_equal:  # Ctrl+Plus (Zoom In)
            self.on_zoom_in(widget)
            return True
        elif ctrl and keyval == Gdk.KEY_minus:  # Ctrl+Minus (Zoom Out)
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
            self.show_pdf(self.current_page)  # Redraw the current page
            return True
            
    def get_spread(self, page, rtl=False):
        if page == 1:
            return (1,)
        if page > int(self.numpages):
            page = int(self.numpages)
        if rtl:
            if page % 2 == 0:
                return (page + 1, page)
            else:
                return (page, page - 1)
        else:
            if page % 2 == 0:
                return (page, page + 1)
            else:
                return (page - 1, page)

    def on_button_release(self, widget, event):
        # zl = self.zoomLevel
        # page_number = 999  # not sure where we were getting page_number from before. #fixMe!
        # if event.button == 1:  # Left-click
            # x, y = event.x, event.y
            # print(f"Left-click at x: {x}, y: {y}, on page {page_number}")
            # self.handle_left_click(x / zl, y / zl, widget, page_number)
        if event.button == 3:  # Right-click (for context menu)
            self.show_context_menu(widget, event)
        return True

    def get_parloc(self, widget, event):
        x = event.x / self.zoomLevel
        y = event.y / self.zoomLevel
        if self.spread_mode:
            side = self.widgetPosition(widget)
            pnum = self.get_spread(self.current_page)[side]     # this all only works for LTR
        else:
            pnum = self.current_page
        p = None
        a = self.hbox.get_allocation()

        if self.parlocs is not None:
            p = self.parlocs.findPos(pnum, x, self.psize[1] - y)
        # print(f"Parloc: {p=} {pnum=} {x=} y={self.psize[1]-y}   {self.psize=}   {a.x=} {a.y=}")
        return p

    def show_context_menu(self, widget, event):
        menu = Gtk.Menu()

        if False and self.isdiglot:
            info = []
        else:
            parref = self.get_parloc(widget, event)
            if parref is None:
                info = []
            else:
                pnum = f"[{parref.parnum}]" if parref.parnum > 1 else ""
                ref = parref.ref
                self.adjlist = self.model.get_adjlist(ref[:3].upper())
                if self.adjlist is not None:
                    info = self.adjlist.getinfo(ref + pnum, insert=True)

        logger.debug(f"{parref=} {info=}")
        if len(info):
            o = 4 if ref[3:4] in ("L", "R", "A", "B", "C", "D", "E", "F") else 3
            hdr = f"{ref[:o]} {ref[o:]}{pnum}   \\{parref.mrk}   {info[1] if len(info) else ''}%"
            header_info = Gtk.MenuItem(label=hdr)
            header_info.set_sensitive(False)  # Make the header item non-clickable and grayed out
            header_info.connect("activate", self.on_identify_paragraph, info[2])
            menu.append(header_info)
            menu.append(Gtk.SeparatorMenuItem())

            x = "Yes! Shrink" if ("-" in str(info[0]) and str(info[0]) != "-1") else "Try Shrink"
            shrink_para = Gtk.MenuItem(label=f"{x} -1 line ({parref.lines - 1})")
            expand_para = Gtk.MenuItem(label=f"Expand +1 line ({parref.lines + 1})")

            shrLim = max(self.shrinkLimit, info[1]-self.shrinkStep)
            shrink_text = Gtk.MenuItem(label=f"Shrink Text ({shrLim}%)")
            shrink_text.set_sensitive(not info[1] <= shrLim)  # clickable only if within limit%

            normal_text = Gtk.MenuItem(label=f"Normal Size (100%)")
            normal_text.set_sensitive(not info[1] == 100)  # non-clickable and grayed out if already at 100%

            expLim = min(self.expandLimit, info[1]+self.expandStep)
            expand_text = Gtk.MenuItem(label=f"Expand Text ({expLim}%)")
            expand_text.set_sensitive(not info[1] >= expLim)  # clickable only if within limit%

            shrink_para.connect("activate", self.on_shrink_paragraph, info, parref)
            expand_para.connect("activate", self.on_expand_paragraph, info, parref)
            shrink_text.connect("activate", self.on_shrink_text, info, parref)
            normal_text.connect("activate", self.on_normal_text, info, parref)
            expand_text.connect("activate", self.on_expand_text, info, parref)

            menu.append(shrink_para)
            menu.append(expand_para)
            menu.append(Gtk.SeparatorMenuItem())
            menu.append(shrink_text)
            menu.append(normal_text)
            menu.append(expand_text)
            menu.append(Gtk.SeparatorMenuItem())

        # Second section: Zoom In, Reset Zoom, Zoom Out
        zoom_in_item    = Gtk.MenuItem(label="Zoom In         (Ctrl +)")
        zoom_out_item   = Gtk.MenuItem(label="Zoom Out       (Ctrl -)")
        fit_zoom_item   = Gtk.MenuItem(label="Zoom to Fit (Ctrl + F)")
        reset_zoom_item = Gtk.MenuItem(label="Zoom 100%  (Ctrl + 0)")

        zoom_in_item.connect("activate", self.on_zoom_in)
        zoom_out_item.connect("activate", self.on_zoom_out)
        fit_zoom_item.connect("activate", self.set_zoom_fit_to_screen)
        reset_zoom_item.connect("activate", self.on_reset_zoom)

        menu.append(zoom_in_item)
        menu.append(zoom_out_item)
        menu.append(fit_zoom_item)
        menu.append(reset_zoom_item)

        menu.show_all()
        menu.popup(None, None, None, None, event.button, event.time)

    # Context menu item callbacks for paragraph actions
    def on_identify_paragraph(self, widget, info, parref):
        print("Identify paragraph option selected")

    def on_shrink_paragraph(self, widget, info, parref):
        if self.adjlist is not None:
            self.adjlist.increment(info[2], -1)

    def on_expand_paragraph(self, widget, info, parref):
        if self.adjlist is not None:
            self.adjlist.increment(info[2], 1)
        
    def on_shrink_text(self, widget, info, parref):
        if self.adjlist is not None:
            if info[1] - self.shrinkStep < self.shrinkLimit:
                self.adjlist.expand(info[2], self.shrinkLimit - info[1], mrk=parref.mrk)
            else:
                self.adjlist.expand(info[2], -self.shrinkStep, mrk=parref.mrk)

    def on_normal_text(self, widget, info, parref):
        if self.adjlist is not None:
            self.adjlist.expand(info[2], 100 - info[1], mrk=parref.mrk)

    def on_expand_text(self, widget, info, parref):
        if self.adjlist is not None:
            if info[1] + self.expandStep > self.expandLimit:
                self.adjlist.expand(info[2], self.expandLimit - info[1], mrk=parref.mrk)
            else:
                self.adjlist.expand(info[2], self.expandStep, mrk=parref.mrk)
        
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

        # Get the parent widget of self.hbox
        parent_widget = self.hbox.get_parent().get_parent()

        # Check if the parent widget exists to avoid AttributeError
        if parent_widget is not None:
            alloc = parent_widget.get_allocation()

        # Calculate the zoom level to fit the page within the dialog ( borders and padding subtracted)
        scale_x = (alloc.width - 32) / (page_width * (2 if self.spread_mode else 1))
        scale_y = (alloc.height - 32) / page_height
        self.set_zoom(min(scale_x, scale_y))


class ThreadRenderer(Thread):

    def __init__(self, *args, parent=None, **kw):
        super().__init__(*args, **kw)
        self.parent = parent
        self.pending = None
        self.startme = False
        self.quit = False
        self.lock = Event()
        self.lock.clear()
        self.start()

    def render_pages(self, pages, zoomlevel, w, h):
        self.pending = [zoomlevel, w, h] + list(pages)
        self.stopme = False
        self.lock.set()
        if self.startme:
            self.startme = False
            self.start()

    def stop(self):
        self.stopme = True
        self.pending = None

    def kill(self):
        self.quit = True
        self.lock.set()

    def run(self):
        while True:
            time.sleep(0.2)
            self.lock.wait()
            if self.quit:
                break
            pending = self.pending
            self.pending = None
            self.lock.clear()
            zoomlevel, w, h = pending[0:3]
            images = []
            for p in pending[3:]:
                imarray = sharedctypes.RawArray('B', w * h * 4)
                if sys.platform == "win32":
                    self.parent.render_pi(p, zoomlevel, imarray)
                else:
                    mp = Process(target=self.parent.render_pi, args=(p, zoomlevel, imarray))
                    mp.start()
                    mp.join()
                images.append(arrayImage(imarray, w, h))
            if not self.lock.is_set() and self.pending is None and not self.stopme and len(images) and self.parent is not None:
                GLib.idle_add(self.parent.update_boxes, images)
        self.startme = True


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
    partype:    str
    mrk:        str
    baseline:   float
    rects:      InitVar[None] = None

    def __str__(self):
        return f"{getattr(self, 'ref', '')}[{getattr(self, 'parnum', '')}] {self.baseline} {self.rects}"

    def __repr__(self):
        return self.__str__()

class Paragraphs(list):
    parlinere = re.compile(r"^\\@([a-zA-Z@]+)\s*\{(.*?)\}\s*$")

    def readParlocs(self, fname):
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
        with open(fname, encoding="utf-8") as inf:
            for l in inf.readlines():
                m = self.parlinere.match(l)
                if not m:
                    continue
                c = m.group(1)
                p = m.group(2).split("}{")
                if c == "pgstart":          # pageno, available height
                    #pnum = int(p[0])
                    pnum += 1
                    self.pindex.append(len(self))
                    pheight = float(re.sub(r"[a-z]+", "", p[1]))
                    inpage = True
                elif c == "parpageend":     # bottomx, bottomy, type=bottomins, notes, verybottomins, pageend
                    pginfo = [readpts(x) for x in p[:2]] + [p[2]]
                    inpage = False
                elif c == "colstart":       # col height, col depth, col width, topx, topy
                    colinfos[polycol] = [readpts(x) for x in p]
                    cinfo = colinfos[polycol]
                    if currps[polycol] is not None:
                        currr = ParRect(pnum, cinfo[3], cinfo[4])
                        currps[polycol].rects.append(currr)
                elif c == "colstop" or c == "Poly@colstop":     # bottomx, bottomy [, polycode]
                    if currr is not None:
                        cinfo = colinfos[polycol]
                        currr.xend = cinfo[3] + cinfo[2]
                        currr.yend = readpts(p[1])
                        currr = None
                elif c == "parstart":       # mkr, baselineskip, partype=section etc., startx, starty
                    currp = ParInfo(p[0], p[1], readpts(p[2]))
                    currp.rects = []
                    cinfo = colinfos[polycol]
                    currr = ParRect(pnum, cinfo[3], readpts(p[4]) + currp.baseline)
                    currp.rects.append(currr)
                    currps[polycol] = currp
                    self.append(currp)
                elif c == "parend":         # badness, bottomx, bottomy
                    cinfo = colinfos[polycol]
                    if currps[polycol] is None:
                        breakpoint()
                    currps[polycol].lines = int(p[0])
                    currr.xend = cinfo[3] + cinfo[2]    # p[1] is xpos of last char in par
                    currr.yend = readpts(p[2])
                    endpar = True
                elif c == "parlen":         # ref, stretch, numlines, marker, adjustment
                    if not endpar:
                        continue
                    endpar = False
                    currp = currps[polycol]
                    if currp is None:
                        continue
                    currp.ref = p[0]
                    currp.parnum = int(p[1])
                    currp.lines = int(p[2]) # this seems to be the current number of lines in para
                    currp.nextmk = p[3]
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
        logger.debug(f"parlocs={self}")
        
    def findPos(self, pnum, x, y):
        done = False
        # just iterate over paragraphs on this page
        if pnum > len(self.pindex):
            return None
        e = self.pindex[pnum] if pnum < len(self.pindex) else len(self)

        for p in self[max(self.pindex[pnum-1]-1, 0):e+1]:
            for r in p.rects:
                if r.pagenum > pnum:
                    done = True
                    break
                elif r.pagenum < pnum:
                    continue
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
