import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, cairo

PREDEFINED_COLORS = [
    ("#F4E7F2", "Pastel Pink"),
    ("#F9E4E9", "Pale Rose"),
    ("#FCE8D9", "Soft Peach"),
    ("#FFF3E0", "Light Apricot"),
    ("#FDF7D6", "Pale Yellow"),
    ("#F5FAD8", "Mint Cream"),
    ("#EAF8E3", "Light Mint"),
    ("#E4F6EA", "Pale Green"),
    ("#E2F5F5", "Light Cyan"),
    ("#E6F3FA", "Baby Blue"),
    ("#E9EEFA", "Pale Lavender"),
    ("#ECE5F5", "Soft Lilac"),
    ("#F1E8F4", "Light Mauve"),
    ("#F5E9F0", "Pale Plum"),
    ("#F8ECE8", "Creamy Beige"),
    ("#F2F0F0", "Light Gray"),
]

class ColorPickerDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="Choose a Color", transient_for=parent, flags=0)
        self.set_default_size(370, 300)
        self.selected_color = None
        box = self.get_content_area()

        grid = Gtk.Grid(column_spacing=10, row_spacing=10, margin=10)
        box.add(grid)

        # Create color swatches using EventBox and DrawingArea
        for i, (hex_code, color_name) in enumerate(PREDEFINED_COLORS):
            event_box = Gtk.EventBox()
            event_box.set_size_request(80, 80)
            drawing_area = Gtk.DrawingArea()
            drawing_area.connect("draw", self.draw_color, hex_code)
            event_box.add(drawing_area)
            event_box.connect("button-press-event", self.on_color_chosen, hex_code)
            # Add tooltip with name and hex code
            event_box.set_tooltip_text(f"{color_name}\n{hex_code}")
            grid.attach(event_box, i % 4, i // 4, 1, 1)

        # Custom color chooser
        custom_button = Gtk.Button(label="Custom...")
        custom_button.set_size_request(80, 40)
        custom_button.connect("clicked", self.on_custom_color)
        grid.attach(custom_button, 0, (len(PREDEFINED_COLORS) + 3) // 4 + 1, 4, 1)

        self.show_all()

    def draw_color(self, widget, cr, hex_code):
        # Parse hex code to RGB
        r = int(hex_code[1:3], 16) / 255.0
        g = int(hex_code[3:5], 16) / 255.0
        b = int(hex_code[5:7], 16) / 255.0

        # Set the color and fill the rectangle
        cr.set_source_rgb(r, g, b)
        cr.rectangle(0, 0, 80, 80)
        cr.fill()

        # Draw a border
        cr.set_source_rgb(0.5, 0.5, 0.5)  # Gray border
        cr.set_line_width(1)
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

# Demo window
def main():
    win = Gtk.Window(title="Test Color Picker")
    win.connect("destroy", Gtk.main_quit)
    win.set_border_width(10)

    def open_dialog(button):
        dialog = ColorPickerDialog(win)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Chosen color:", dialog.selected_color)
        dialog.destroy()

    button = Gtk.Button(label="Pick a Color")
    button.connect("clicked", open_dialog)
    win.add(button)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()