import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Poppler", "0.18")
from gi.repository import Gtk, Poppler, GdkPixbuf
import cairo
from cairo import ImageSurface, Context
from pathlib import Path

class PDFViewer:
    def __init__(self, model, widget):
        # Get the scrolled window from the builder
        self.hbox = widget
        self.model = model
        self.pages = 0

    def load_pdf(self, pdf_path):
        # Convert the Windows path to a valid URI using pathlib
        file_uri = Path(pdf_path).as_uri()

        # Load the PDF document using Poppler
        try:
            self.document = Poppler.Document.new_from_file(file_uri, None)
            self.pages = self.document.get_n_pages()
        except Exception as e:
            print(f"Error opening PDF: {e}")
            return
            
    def show_pdf(self, page, bkview=True, rtl=False):
        self.hbox.hide()
        for child in self.hbox.get_children():
            self.hbox.remove(child)

        if bkview:
            spread = self.get_spread(page, rtl)
            for i in spread:
                if i in range(self.pages+1):
                    pg = self.document.get_page(i-1)
                    page_widget = self.render_page(pg)
                    self.hbox.pack_start(page_widget, False, False, 5)
        else:
            if page in range(self.pages+1):
                pg = self.document.get_page(page-1)
                page_widget = self.render_page(pg)
                self.hbox.pack_start(page_widget, False, False, 5)
        self.hbox.show_all()

    def get_spread(self, page, rtl=False):
        if page == 1:
            return (1,)  # Special case: Page 1 has no preceding page
        if page > int(self.pages):
            page = int(self.pages)
        if rtl:
            # For RTL books: odd pages are on the left, even pages are on the right
            if page % 2 == 0:
                return (page + 1, page)  # Even page -> (next odd, even)
            else:
                return (page, page - 1)  # Odd page -> (odd, previous even)
        else:
            # For LTR books: even pages are on the left, odd pages are on the right
            if page % 2 == 0:
                return (page, page + 1)  # Even page -> (even, next odd)
            else:
                return (page - 1, page)  # Odd page -> (previous even, odd)

    def render_page(self, page):
        # Get page size
        width, height = page.get_size()
        surface = ImageSurface(cairo.FORMAT_RGB24, int(width), int(height))
        context = Context(surface)

        # Fill the surface with white to avoid transparency artifacts
        context.set_source_rgb(1, 1, 1)  # White background
        context.paint()

        # Render the page to the Cairo surface
        page.render(context)

        # Convert the Cairo surface to a Pixbuf
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

        # Create an image widget to hold the Pixbuf and return it
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        return image
