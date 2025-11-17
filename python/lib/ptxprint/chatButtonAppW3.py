import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Rsvg', '2.0')
from gi.repository import Gtk, GdkPixbuf, Rsvg, Gio, Gdk

# The URL to open in the browser
CHAT_URL = "https://ptxprintsupport-55742.chipp.ai/w/chat/"

# The SVG data for the chat bubble icon
SVG_ICON_DATA = """<svg width="42" height="32" viewBox="0 0 42 32" xmlns="http://www.w3.org/2000/svg"><path d="M3.14742 30.0676L3.14805 30.0681C3.74355 30.5364 4.44972 30.8036 5.18251 30.8471L5.19311 30.8576H5.39966C5.82967 30.8576 6.26603 30.7784 6.68478 30.6224L6.68535 30.6222L11.1925 28.9376C12.4828 29.2978 13.8129 29.4797 15.151 29.4797H26.8491C34.9241 29.4797 41.5 22.987 41.5 14.9898C41.5 6.99272 34.9241 0.5 26.8491 0.5H15.151C7.07576 0.5 0.5 6.99272 0.5 14.9898C0.5 17.5035 1.17545 19.9774 2.45751 22.1779L1.81712 26.7687C1.8171 26.7689 1.81707 26.7691 1.81704 26.7693C1.63762 28.0369 2.13907 29.272 3.14742 30.0676ZM4.36825 21.9606L4.39324 21.7817L4.29807 21.6281L4.21767 21.4983C4.21749 21.498 4.21732 21.4978 4.21714 21.4975C2.99975 19.5144 2.35763 17.2649 2.35763 14.9898C2.35763 8.02633 8.08893 2.35211 15.1467 2.35211H26.8448C33.9024 2.35211 39.6339 8.02634 39.6339 14.9898C39.6339 21.9533 33.9024 27.6274 26.8448 27.6274H15.1467C13.8884 27.6274 12.6338 27.4399 11.424 27.0727L11.4226 27.0723L11.2811 27.0298L11.1199 26.9813L10.9622 27.0403L6.02653 28.8845L6.02629 28.8849C5.43626 29.1066 4.79708 29.0052 4.30309 28.6171C3.81392 28.2292 3.57446 27.6367 3.66061 27.0276L3.66073 27.0267L4.36825 21.9606Z" fill="white" stroke="none"/></svg>""".encode('utf-8')

# The CSS for the button
CSS_DATA = b"""
#chat-button {
    background-image: none;
    background-color: #004879; 
    border-radius: 9999px;
    border: none;
    outline: none;
    padding: 16px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease-in-out;
}
#chat-button image {
    -gtk-icon-effect: none;
    opacity: 1;
}
#chat-button:hover {
    background-color: #005a99;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
}
#chat-button:active {
    background-color: #003a63;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
}
"""

class ChatButtonWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="PyGTK Chat Button Example")
        self.set_default_size(500, 400)
        self.connect("destroy", Gtk.main_quit)

        self.load_css()
        
        overlay = Gtk.Overlay()
        self.add(overlay)

        # Main content area
        main_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        label = Gtk.Label(label="This is the main application content.")
        label.set_vexpand(True)
        main_content.add(label)
        overlay.add(main_content)
        
        # Create and add the button
        chat_button = self.create_chat_button()
        chat_button.set_halign(Gtk.Align.END)
        chat_button.set_valign(Gtk.Align.END)
        chat_button.set_margin_end(20)
        chat_button.set_margin_bottom(20)
        overlay.add_overlay(chat_button)
        
    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(CSS_DATA)
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def create_chat_button(self):
        input_stream = Gio.MemoryInputStream.new_from_data(SVG_ICON_DATA, None)
        pixbuf = GdkPixbuf.Pixbuf.new_from_stream_at_scale(input_stream, width=32, height=32, preserve_aspect_ratio=True)
        icon = Gtk.Image.new_from_pixbuf(pixbuf)
        button = Gtk.Button()
        button.add(icon)
        button.set_name("chat-button")
        button.set_size_request(64, 64)
        button.connect("clicked", self.on_chat_button_clicked)
        event_box = Gtk.EventBox()
        event_box.add(button)
        event_box.set_tooltip_text("Open PTXprint Support AI assistant")
        
        return event_box

    def on_chat_button_clicked(self, widget):
        Gtk.show_uri_on_window(self, CHAT_URL, Gdk.CURRENT_TIME)

if __name__ == "__main__":
    win = ChatButtonWindow()
    win.show_all()
    Gtk.main()