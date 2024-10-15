import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Poppler", "0.18")
from gi.repository import Gtk, Poppler, GdkPixbuf
import cairo
from cairo import ImageSurface, Context
from pathlib import Path

class PDFViewer:
    def __init__(self, builder):
        # Get the scrolled window from the builder
        self.scrolled_window = builder.get_object("scr_previewPDF")

        # Check if vbox already exists, if not create it
        if not hasattr(self, 'vbox'):
            self.vbox = Gtk.VBox(spacing=10)
            self.scrolled_window.add_with_viewport(self.vbox)

    def load_pdf(self, pdf_path):
        # Clear any existing children from vbox
        for child in self.vbox.get_children():
            self.vbox.remove(child)

        # Convert the Windows path to a valid URI using pathlib
        file_uri = Path(pdf_path).as_uri()

        # Load the PDF document using Poppler
        try:
            self.document = Poppler.Document.new_from_file(file_uri, None)
        except Exception as e:
            print(f"Error opening PDF: {e}")
            return

        # Iterate over each page and add to the vbox
        for i in range(self.document.get_n_pages()):
            page = self.document.get_page(i)
            page_widget = self.render_page(page)
            self.vbox.pack_start(page_widget, False, False, 5)

        # Show all widgets in the scrolled window
        self.scrolled_window.show_all()

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
