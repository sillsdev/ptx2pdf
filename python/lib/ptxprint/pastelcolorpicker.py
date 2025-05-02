import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, cairo

PREDEFINED_COLORS = [
    ("#F2F0F0", "Light Gray"),
    ("#ECE5F5", "Soft Lilac"),
    ("#F1E8F4", "Light Mauve"),
    ("#F4E7F2", "Pastel Pink"),
    ("#F9E4E9", "Pale Rose"),
    ("#F8ECE8", "Creamy Beige"),
    ("#FCE8D9", "Soft Peach"),
    ("#FFF3E0", "Light Apricot"),
    ("#FDF7D6", "Pale Yellow"),
    ("#F5FAD8", "Mint Cream"),
    ("#EAF8E3", "Light Mint"),
    ("#E4F6EA", "Pale Green"),
    ("#E2F5F5", "Light Cyan"),
    ("#E9EEFA", "Pale Lavender"),
    ("#E6F3FA", "Baby Blue"),
    ("#FFFFFF", "None"),
]

class ColorPickerDialog(Gtk.Dialog):
    def __init__(self, parent, current_color=None):  # Add current_color parameter
        Gtk.Dialog.__init__(self, title="Choose a Color", transient_for=parent, flags=0)
        self.set_default_size(370, 300)
        self.selected_color = None
        self.current_color = current_color  # Store the current color
        box = self.get_content_area()

        grid = Gtk.Grid(column_spacing=10, row_spacing=10, margin=10)
        box.add(grid)

        for i, (hex_code, color_name) in enumerate(PREDEFINED_COLORS):
            event_box = Gtk.EventBox()
            event_box.set_size_request(80, 80)
            drawing_area = Gtk.DrawingArea()
            drawing_area.connect("draw", self.draw_color, hex_code, hex_code == current_color)
            event_box.add(drawing_area)
            event_box.connect("button-press-event", self.on_color_chosen, hex_code)
            event_box.set_tooltip_text(f"{color_name}\n{hex_code}")
            grid.attach(event_box, i % 4, i // 4, 1, 1)

        custom_button = Gtk.Button(label="Custom...")
        custom_button.set_size_request(80, 40)
        custom_button.connect("clicked", self.on_custom_color)
        grid.attach(custom_button, 0, (len(PREDEFINED_COLORS) + 3) // 4 + 1, 4, 1)

        self.show_all()

    def draw_color(self, widget, cr, hex_code, is_current=False):
        r = int(hex_code[1:3], 16) / 255.0
        g = int(hex_code[3:5], 16) / 255.0
        b = int(hex_code[5:7], 16) / 255.0

        cr.set_source_rgb(r, g, b)
        cr.rectangle(0, 0, 80, 80)
        cr.fill()

        # Draw border, thicker if it's the current color
        cr.set_source_rgb(0.5, 0.5, 0.5)
        cr.set_line_width(3 if is_current else 1)
        cr.rectangle(0, 0, 80, 80)
        cr.stroke()
        
    def on_color_chosen(self, widget, event, hex_code):
        self.selected_color = hex_code
        self.response(Gtk.ResponseType.OK)

    def on_custom_color(self, button):
        dialog = Gtk.ColorChooserDialog(title="Custom Color", parent=self)
        if dialog.run() == Gtk.ResponseType.OK:
            rgba = dialog.get_rgba()
            self.selected_color = rgba.to_string()
            self.response(Gtk.ResponseType.OK)
        dialog.destroy()
