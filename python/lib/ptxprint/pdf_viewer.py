import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Poppler", "0.18")
from gi.repository import Gtk, Poppler, GdkPixbuf, Gdk
import cairo
from cairo import ImageSurface, Context
from pathlib import Path

class PDFViewer:
    def __init__(self, model, widget):
        self.hbox = widget
        self.model = model
        self.pages = 0
        self.current_page = None  # Keep track of the current page
        self.zoom_level = 1.0  # Initial zoom level is 100%
        self.spread_mode = self.model.get("c_bkView", False)

        # Connect keyboard events
        self.hbox.connect("key-press-event", self.on_key_press_event)
        self.hbox.set_can_focus(True)  # Ensure the widget can receive keyboard focus


    def load_pdf(self, pdf_path):
        file_uri = Path(pdf_path).as_uri()
        try:
            self.document = Poppler.Document.new_from_file(file_uri, None)
            self.pages = self.document.get_n_pages()
        except Exception as e:
            print(f"Error opening PDF: {e}")
            return

    def show_pdf(self, page, rtl=False):
        self.hbox.hide()
        self.spread_mode = self.model.get("c_bkView", False)

        for child in self.hbox.get_children():
            self.hbox.remove(child)

        if self.spread_mode:
            spread = self.get_spread(page, rtl)
            for i in spread:
                if i in range(self.pages+1):
                    pg = self.document.get_page(i-1)
                    page_widget = self.render_page(pg, i)  # Pass the page number
                    self.hbox.pack_start(page_widget, False, False, 5)
        else:
            if page in range(self.pages+1):
                pg = self.document.get_page(page-1)
                page_widget = self.render_page(pg, page)  # Pass the page number
                self.hbox.pack_start(page_widget, False, False, 5)

        self.hbox.show_all()
        self.current_page = page

        # Grab focus so the widget receives keyboard events
        self.hbox.grab_focus()

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
            p = self.pages
            self.model.set("s_pgNum", p)
            self.show_pdf(p)
            return True
        elif keyval == Gdk.KEY_Page_Down:  # Page Down (Next page/spread)
            next_page = self.current_page + (2 if self.spread_mode else 1)
            p = min(next_page, self.pages)
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
            
    def get_spread(self, page, rtl=False):
        if page == 1:
            return (1,)
        if page > int(self.pages):
            page = int(self.pages)
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

    def render_page(self, page, page_number):
        # Get page size, applying zoom factor
        width, height = page.get_size()
        width, height = width * self.zoom_level, height * self.zoom_level

        surface = ImageSurface(cairo.FORMAT_RGB24, int(width), int(height))
        context = Context(surface)
        context.set_source_rgb(1, 1, 1)
        context.paint()

        # Apply zoom transformation to context
        context.scale(self.zoom_level, self.zoom_level)

        # Render the page to the Cairo surface
        page.render(context)

        data = surface.get_data()
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(
            data,
            GdkPixbuf.Colorspace.RGB,
            True,
            8,
            surface.get_width(),
            surface.get_height(),
            surface.get_stride()
        )

        image = Gtk.Image.new_from_pixbuf(pixbuf)
        event_box = Gtk.EventBox()
        event_box.add(image)

        # Pass the page number to the mouse click handler
        event_box.connect("button-press-event", self.on_mouse_click, page_number)

        return event_box

    def on_mouse_click(self, widget, event, page_number):
        zl = self.zoom_level
        if event.button == 1:  # Left-click
            x, y = event.x, event.y
            # print(f"Left-click at x: {x}, y: {y}, on page {page_number}")
            self.handle_left_click(x / zl, y / zl, widget, page_number)

        if event.button == 3:  # Right-click (for context menu)
            self.show_context_menu(widget, event)

    def handle_left_click(self, x, y, widget, page_number):
        zl = self.zoom_level
        # Print page number as well as coordinates
        print(f"Coordinates on page {page_number}: x={x}, y={y}, zl={zl}")

    def show_context_menu(self, widget, event):
        menu = Gtk.Menu()

        # First section: Identify, Shrink, Grow
        identify_ref = Gtk.MenuItem(label="Show Reference")
        shrink_item = Gtk.MenuItem(label="Shrink Paragraph")
        grow_item = Gtk.MenuItem(label="Grow Paragraph")

        identify_ref.connect("activate", self.on_identify_paragraph)
        shrink_item.connect("activate", self.on_shrink_paragraph)
        grow_item.connect("activate", self.on_grow_paragraph)

        menu.append(identify_ref)
        menu.append(shrink_item)
        menu.append(grow_item)

        # Separator between the two sections
        menu.append(Gtk.SeparatorMenuItem())

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
        self.zoom_level += 0.1  # Increase zoom by 10%
        # print(f"Zoom In: Zoom level = {self.zoom_level}")
        self.show_pdf(self.current_page)  # Redraw the current page

    def on_reset_zoom(self, widget):
        self.zoom_level = 1.0  # Reset zoom to 100%
        # print(f"Reset Zoom: Zoom level = {self.zoom_level}")
        self.show_pdf(self.current_page)  # Redraw the current page

    def on_zoom_out(self, widget):
        min_zoom = 0.3  # Set a minimum zoom level of 10%
        if self.zoom_level > min_zoom:
            self.zoom_level -= 0.1  # Decrease zoom by 10%
            # print(f"Zoom Out: Zoom level = {self.zoom_level}")
            self.show_pdf(self.current_page)  # Redraw the current page
        # else:
            # print("Zoom level is already at the minimum. Cannot zoom out further.")
