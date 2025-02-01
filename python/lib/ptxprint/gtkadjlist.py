from gi.repository import Gtk, Gdk
from ptxprint.utils import _

headers = ['Book', 'C.V', 'Para', 'Stretch', 'Marker', 'Expand', 'Comment']

class AdjListView:
    def __init__(self, parent):
        self.parent = parent
        self.adjlist = None
        self.view = Gtk.TreeView()

        # Enable multi-selection
        self.view.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)

        # Enable right-click event and keypress detection
        self.view.connect("button-press-event", self.on_right_click)
        self.view.connect("key-press-event", self.on_key_press)

        for i in range(7):
            cr = Gtk.CellRendererText(editable=True)
            cr.connect("edited", self.edit, i)
            col = Gtk.TreeViewColumn(cell_renderer=cr, text=i, title=headers[i])
            self.view.append_column(col)

        # Create right-click menu
        self.menu = Gtk.Menu()
        self.delete_item = Gtk.MenuItem(label=_("Delete Row(s)"))
        self.delete_item.connect("activate", self.delete_selected_rows)
        self.menu.append(self.delete_item)
        self.menu.show_all()

    def edit(self, widget, path, value, col):
        """Handles cell editing."""
        self.view.get_model()[path][col] = int(value) if col in (2, 5) else value

    def set_model(self, adjlist, save=True):
        """Sets the model for the TreeView."""
        if self.adjlist is not None and save:
            self.adjlist.save()

        self.adjlist = adjlist
        self.view.set_model(None if adjlist is None else adjlist.liststore)

        if adjlist is not None:
            adjlist.changed = True  # Mark as changed

    def on_right_click(self, widget, event):
        """Handles right-click events to show the context menu."""
        if event.button == 3:  # Right-click
            path_info = self.view.get_path_at_pos(int(event.x), int(event.y))
            if path_info is not None:
                path, _, _, _ = path_info
                self.view.get_selection().select_path(path)  # Select the row
                self.menu.popup_at_pointer(event)  # Show menu at cursor position
            return True  # Stop event propagation
        return False

    def delete_selected_rows(self, widget=None):
        """Deletes all selected rows from the model."""
        selection = self.view.get_selection()
        model, paths = selection.get_selected_rows()

        # Convert paths to iters, then delete in reverse order to avoid index shifting
        iters_to_remove = [model.get_iter(path) for path in reversed(paths)]
        for tree_iter in iters_to_remove:
            model.remove(tree_iter)

    def on_key_press(self, widget, event):
        """Handles keypress events to delete selected rows when DEL is pressed."""
        if event.keyval == Gdk.KEY_Delete:
            self.delete_selected_rows()
