import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango, GObject
import sys

# import logging
# logger = logging.getLogger(__name__)

class TatweelDialog:
    def __init__(self, builder, font=None):
        self.builder = builder  # Store the builder object
        self.dialog = self.builder.get_object("dlg_makeTatweelRule")

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.last_clipboard_text = ""

        # Start polling clipboard every 1000ms (1 second)
        self.polling_timer_id = GObject.timeout_add(1000, self.check_clipboard)

        # Get UI Elements
        self.t_tatweelRef = builder.get_object("t_tatweelRef")
        self.t_tatweelFind = builder.get_object("t_tatweelFind")
        self.s_tatweelLength = builder.get_object("s_tatweelLength")
        self.t_tatweelPreview = builder.get_object("t_tatweelPreview")

        if font is not None:
            font_desc = Pango.FontDescription(font + " 14")
            self.t_tatweelFind.override_font(font_desc)
            self.t_tatweelPreview.override_font(font_desc)
        
        # Buttons
        self.btn_tatweel_insertRule = builder.get_object("btn_tatweel_insertRule")
        self.btn_tatweel_close = builder.get_object("btn_tatweel_close")

        # Track the last known cursor position in the source entry
        self.last_cursor_pos = 0

        # Connect signals
        self.t_tatweelFind.connect("notify::cursor-position", self.on_cursor_moved)
        self.s_tatweelLength.connect("value-changed", self.on_tatweel_length_changed)
        self.btn_tatweel_close.connect("clicked", self.on_close_dialog)

        self.dialog.show_all()

    def on_cursor_moved(self, entry, param):
        """Captures the cursor position in the source word."""
        self.last_cursor_pos = entry.get_position()
        self.on_tatweel_length_changed(None)

    def on_tatweel_length_changed(self, spin_button):
        """Inserts Tatweels at the stored cursor position and updates the preview rule."""
        tatweel_count = int(self.s_tatweelLength.get_value())  # Get Tatweel count
        tatweel_str = "ـ" * tatweel_count  # Generate Tatweel sequence
        source_text = self.t_tatweelFind.get_text().strip()
        cursor_pos = min(self.last_cursor_pos, len(source_text))
        new_text = source_text[:cursor_pos] + tatweel_str + source_text[cursor_pos:]
        verse_ref = self.t_tatweelRef.get_text().strip() or "???"  # Default to ??? if empty
        preview_rule = f"at {verse_ref} '{source_text}' > '{new_text}'"
        self.t_tatweelPreview.set_text(preview_rule)

    def check_clipboard(self):
        """Checks if clipboard content has changed and updates t_tatweelFind."""
        self.clipboard.request_text(self.on_clipboard_text_received)
        return True  # Keep checking periodically

    def on_clipboard_text_received(self, clipboard, text):
        """Updates t_tatweelFind only if the clipboard text changed and is 30 characters or less."""
        if text and text != self.last_clipboard_text:
            # Only update if the text is 30 characters or fewer
            if len(text) <= 30:
                self.last_clipboard_text = text
                self.t_tatweelFind.set_text(text)
                ref = self.read_scripture_reference()
                if ref is not None:
                    self.t_tatweelRef.set_text(ref)

    def read_scripture_reference(self):
        if sys.platform == "win32":
            import winreg
            # os.path.abspath(os.path.join(b, 'ptx2pdf'))
            key_path = r"Software\SantaFe\Focus\ScriptureReference"
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
                value, _ = winreg.QueryValueEx(key, "")
                winreg.CloseKey(key)
                # logger.debug(f"Retrieved Scripture Reference: {value}")
                return value
            except FileNotFoundError:
                logger.debug(f"Error: Registry Key not found: {key_path}")
            except WindowsError as e:
                logger.debug(f"Error: {e} while trying to read ref from registry")

        return None  # Return None if not found or on error

    def on_close_dialog(self, button):
        if hasattr(self, 'polling_timer_id'):
            GObject.source_remove(self.polling_timer_id)
            del self.polling_timer_id
        self.dialog.hide()
        
