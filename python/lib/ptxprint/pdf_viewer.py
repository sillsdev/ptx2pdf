import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Poppler", "0.18")
from gi.repository import Gtk, Poppler, GdkPixbuf, Gdk, GLib
import cairo, re, time, sys
from cairo import ImageSurface, Context
from pathlib import Path
from threading import Thread, Event, Timer
from dataclasses import dataclass, InitVar, field
from multiprocessing import sharedctypes, Process

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
                    self.hbox.pack_end(event_box, False, False, 0)
                else:
                    self.hbox.pack_start(event_box, False, False, 0)
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

    def load_pdf(self, pdf_path):
        file_uri = Path(pdf_path).as_uri()
        try:
            self.document = Poppler.Document.new_from_file(file_uri, None)
            self.numpages = self.document.get_n_pages()
        except Exception as e:
            print(f"Error opening PDF: {e}")
            return

    def show_pdf(self, page, rtl=False):
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

    def render_pi(self, pi, zoomlevel, imarray):
        if pi >= len(self.pages):
            return
        return render_page(self.pages[pi], zoomlevel, imarray)

    def resize_pdf(self, scrolled=False):
        if self.zoomLevel == self.old_zoom:
            return
        width, height = self.psize
        width, height = int(width * self.zoomLevel), int(height * self.zoomLevel)

        children = self.hbox.get_children()
        if not len(children):
            return self.show_pdf(self.current_page)

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
        self.old_zoom = self.zoomLevel
        self.zoomLevel = zoomlevel
        self.model.set("t_zoomLevel", str(int(self.zoomLevel*100))+"%")
        self.resize_pdf(scrolled=scrolled)
    
    def print_document(self):
        if not hasattr(self, 'document') or self.document is None:
            return
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
        cairo_context.set_source_rgb(1, 1, 1)  # Set background color to white
        cairo_context.paint()

        width, height = pdf_page.get_size()
        scale_x = context.get_width() / width
        scale_y = context.get_height() / height
        cairo_context.scale(scale_x, scale_y)

        pdf_page.render(cairo_context)
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
        # Get all children of the hbox
        children = self.hbox.get_children()

        # Find the widget's index in the list of children
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
            print(f"Zoom reset to actual size: {self.zoomLevel=:.2f}")
            return True
        elif ctrl and keyval in {Gdk.KEY_F, Gdk.KEY_f}:  # Ctrl+F (Fit to screen)
            self.set_zoom_fit_to_screen()
            print(f"Zoom adjusted to fit screen: {self.zoomLevel=:.2f}")
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
        # End dragging when mouse button is released
        # if event.button == 1:
            # self.is_dragging = False
        zl = self.zoomLevel
        page_number = 999  # not sure where we were getting page_number from before. #fixMe!
        if event.button == 1:  # Left-click
            x, y = event.x, event.y
            print(f"Left-click at x: {x}, y: {y}, on page {page_number}")
            self.handle_left_click(x / zl, y / zl, widget, page_number)
        if event.button == 3:  # Right-click (for context menu)
            self.show_context_menu(widget, event)
        return True

    def handle_left_click(self, x, y, widget, page_number):
        zl = self.zoomLevel
        # Print page number as well as coordinates
        print(f"Coordinates on page {page_number}: x={x}, y={self.psize[1]-y}, zl={zl}")
        if self.parlocs is not None:
            p = self.parlocs.findPos(page_number, x, self.psize[1] - y)
            if p is not None:
                if p.parnum == 1:
                    print(f"Paragraph {p.ref} % \\{p.mrk}")
                else:
                    print(f"Paragraph {p.ref}[{p.parnum}] % \\{p.mrk}")

    # def on_button_press(self, widget, event):
        # Left-click initiates dragging
        # if event.button == 1:
            # self.is_dragging = True
            # self.drag_start_x = event.x
            # self.drag_start_y = event.y
        # return True

    # def on_mouse_motion(self, widget, event):
        # if self.is_dragging:
            # Calculate movement offset
            # dx = event.x - self.drag_start_x
            # dy = event.y - self.drag_start_y

            # Update PDF position by shifting the content in hbox
            # self.hbox.set_margin_left(self.hbox.get_margin_left() + int(dx))
            # self.hbox.set_margin_top(self.hbox.get_margin_top() + int(dy))

            # Update start coordinates for smooth continuous dragging
            # self.drag_start_x = event.x
            # self.drag_start_y = event.y
        # return True

    def show_context_menu(self, widget, event):
        menu = Gtk.Menu()

#------------- (put these lines back in when we have shrink and grow working)
        # First section: Identify, Shrink, Grow
        # identify_ref = Gtk.MenuItem(label="Show Reference")
        # shrink_item = Gtk.MenuItem(label="Shrink Paragraph")
        # grow_item = Gtk.MenuItem(label="Grow Paragraph")

        # identify_ref.connect("activate", self.on_identify_paragraph)
        # shrink_item.connect("activate", self.on_shrink_paragraph)
        # grow_item.connect("activate", self.on_grow_paragraph)

        # menu.append(identify_ref)
        # menu.append(shrink_item)
        # menu.append(grow_item)

        # Separator between the two sections
        # menu.append(Gtk.SeparatorMenuItem())
#-------------
        # Second section: Zoom In, Reset Zoom, Zoom Out
        zoom_in_item = Gtk.MenuItem(label="Zoom In      Ctrl +")
        reset_zoom_item = Gtk.MenuItem(label="Reset Zoom    Ctrl 0")
        zoom_out_item = Gtk.MenuItem(label="Zoom Out      Ctrl -")

        zoom_in_item.connect("activate", self.on_zoom_in)
        reset_zoom_item.connect("activate", self.on_reset_zoom)
        zoom_out_item.connect("activate", self.on_zoom_out)

        menu.append(zoom_in_item)
        menu.append(reset_zoom_item)
        menu.append(zoom_out_item)

        menu.show_all()
        menu.popup(None, None, None, None, event.button, event.time)

    # Context menu item callbacks for paragraph actions
    def on_identify_paragraph(self, widget):
        print("Identify paragraph option selected")

    def on_shrink_paragraph(self, widget):
        print("Shrink paragraph option selected")

    def on_grow_paragraph(self, widget):
        print("Grow paragraph option selected")
        
    # Zoom functionality
    def on_zoom_in(self, widget):
        if self.zoomLevel < 2.0:
            zoomLevel = (1.2 * self.zoomLevel)  # Increase zoom by 20% of current level
        elif self.zoomLevel < 5.0:
            zoomLevel = (1.5 * self.zoomLevel)  # Increase zoom by 50% of current level
        elif self.zoomLevel < 10.0:
            zoomLevel = min(self.zoomLevel * 2, 10.0)  # Double zoom, cap at 10.0
        else:
            zoomLevel = 10.0  # Ensure max zoom is 10.0
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
        self.set_zoom_fit_to_screen()

    def set_zoom_fit_to_screen(self):
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
    else:
        return float(s) / 65536.

@dataclass
class ParRect:
    pagenum:    int
    xstart:     float
    ystart:     float
    xend:       float = 0.
    yend:       float = 0.

@dataclass
class ParInfo:
    partype:    str
    mrk:        str
    baseline:   float
    rects:      InitVar[None] = None

class Paragraphs(list):
    parlinere = re.compile(r"^\\@([a-zA-Z]+)\s*\{(.*?)\}\s*$")

    def readParlocs(self, fname):
        self.pindex = []
        currp = None
        currr = None
        endpar = True
        inpage = False
        pnum = 0
        with open(fname, encoding="utf-8") as inf:
            for l in inf.readlines():
                m = self.parlinere.match(l)
                if not m:
                    continue
                c = m.group(1)
                p = m.group(2).split("}{")
                if c == "pgstart":
                    #pnum = int(p[0])
                    pnum += 1
                    self.pindex.append(len(self))
                    pheight = float(re.sub(r"[a-z]+", "", p[1]))
                    inpage = True
                elif c == "parpageend":
                    pginfo = [readpts(x) for x in p[:2]] + [p[2]]
                    inpage = False
                elif c == "colstart":
                    colinfo = [readpts(x) for x in p]
                    if currp is not None:
                        currr = ParRect(pnum, colinfo[3], colinfo[4])
                        currp.rects.append(currr)
                elif c == "colstop":
                    if currr is not None:
                        currr.xend = colinfo[3] + colinfo[2]
                        currr.yend = readpts(p[1])
                        if currr.pagenum == 2:
                            print(currr)
                        currr = None
                elif c == "parstart":
                    currp = ParInfo(p[0], p[1], readpts(p[2]))
                    currp.rects = []
                    currr = ParRect(pnum, colinfo[3], readpts(p[4]) + currp.baseline)
                    currp.rects.append(currr)
                    self.append(currp)
                elif c == "parend":
                    currp.lines = int(p[0])
                    currr.xend = colinfo[3] + colinfo[2]    # p[1] is xpos of last char in par
                    currr.yend = readpts(p[2])
                    endpar = True
                elif c == "parlen":
                    if not endpar:
                        continue
                    endpar = False
                    if currp is None:
                        continue
                    currp.ref = p[0]
                    currp.parnum = int(p[1])
                    currp.badness = int(p[2])
                    currp.nextmk = p[3]
                    currp = None
                    if currr.pagenum == 2:
                        print(currr)
                    currr = None

    def findPos(self, pnum, x, y):
        done = False
        # just iterate over paragraphs on this page
        if pnum >= len(self.pindex):
            return None
        e = self.pindex[pnum+1] if pnum < len(self.pindex) - 1 else len(self)

        for p in self[self.pindex[pnum]:e+1]:
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
