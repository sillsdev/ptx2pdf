import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango, GObject

import sys

class TatweelDialog:
    def __init__(self, builder, font=None):
        self.builder = builder
        self.dialog = self.builder.get_object("dlg_makeTatweelRule")

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.last_clipboard_text = ""

        # Start polling clipboard every 1000ms (1 second)
        self.polling_timer_id = GObject.timeout_add(1000, self.check_clipboard)

        # Get UI Elements
        self.t_tatweelRef = builder.get_object("t_tatweelRef")
        self.t_tatweelText = builder.get_object("t_tatweelText")
        self.s_tatweelLength = builder.get_object("s_tatweelLength")
        self.t_tatweelPreview = builder.get_object("t_tatweelPreview")

        if font is not None:
            font_desc = Pango.FontDescription(font + " 14")
            self.t_tatweelText.override_font(font_desc)
            self.t_tatweelPreview.override_font(font_desc)

        # Buttons
        self.btn_tatweel_insertRule = builder.get_object("btn_tatweel_insertRule")
        self.btn_tatweel_close = builder.get_object("btn_tatweel_close")

        # Track cursor position
        self.last_cursor_pos = 0

        # Connect signals
        self.t_tatweelText.connect("notify::cursor-position", self.on_cursor_moved)
        self.s_tatweelLength.connect("value-changed", self.update_preview)
        self.btn_tatweel_close.connect("clicked", self.on_close_dialog)
        self.t_tatweelText.connect("key-press-event", self.on_key_press)

        self.dialog.show_all()

    def on_cursor_moved(self, entry, param):
        """Captures the cursor position in the source word."""
        self.last_cursor_pos = entry.get_position()

    def on_key_press(self, widget, event):
        """Handles key press events. Inserts Tatweel when Ctrl + Grave (`) is pressed."""
        if event.state & Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_grave:
            self.insert_tatweel()
            return True  # Prevent default behavior
        return False  # Allow normal key processing

    def insert_tatweel(self):
        """Inserts Tatweel characters at the current cursor position."""
        tatweel_count = int(self.s_tatweelLength.get_value())  # Get Tatweel count
        tatweel_str = "ـ" * tatweel_count  # Generate Tatweel sequence
        edited_text = self.t_tatweelText.get_text()
        cursor_pos = min(self.last_cursor_pos, len(edited_text))

        # Insert Tatweel at cursor position
        new_text = edited_text[:cursor_pos] + tatweel_str + edited_text[cursor_pos:]
        self.t_tatweelText.set_text(new_text)

        # Move cursor after inserted Tatweels
        self.t_tatweelText.set_position(cursor_pos + tatweel_count)

        # Update preview
        self.update_preview()

    def update_preview(self, *args):
        """Updates the preview rule with the latest Tatweel insertions."""
        edited_text = self.t_tatweelText.get_text().strip()
        verse_ref = self.t_tatweelRef.get_text().strip() or "???"
        preview_rule = f"at {verse_ref} '{self.last_clipboard_text}' > '{edited_text}'"
        self.t_tatweelPreview.set_text(preview_rule)

    def check_clipboard(self):
        """Checks if clipboard content has changed and updates t_tatweelText."""
        self.clipboard.request_text(self.on_clipboard_text_received)
        return True  # Keep checking periodically

    def on_clipboard_text_received(self, clipboard, text):
        """Updates t_tatweelText only if the clipboard text changed and is 60 characters or fewer."""
        if text and text != self.last_clipboard_text:
            if len(text) <= 60:  # Increased limit from 30 to 60
                self.last_clipboard_text = text
                self.t_tatweelText.set_text(text)
                ref = self.read_scripture_reference()
                if ref is not None:
                    self.t_tatweelRef.set_text(ref)
        self.update_preview()

    def read_scripture_reference(self):
        """Reads the scripture reference from Windows Registry (if on Windows)."""
        if sys.platform == "win32":
            import winreg
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
        """Stops clipboard polling and hides the dialog."""
        if hasattr(self, 'polling_timer_id'):
            GObject.source_remove(self.polling_timer_id)
            del self.polling_timer_id
        self.dialog.hide()
