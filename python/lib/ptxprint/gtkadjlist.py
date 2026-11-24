from gi.repository import Gtk, Gdk
from ptxprint.utils import _

headers = ['Book', 'C.V', 'Para', 'Stretch', 'Marker', 'Expand', 'Parameters', 'Comment']

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

        for i in range(len(headers)):
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
        if self.adjlist is None:
            return
        self.adjlist.changed = True
        if col == 6:        # the parameters are saved from adjlist.db, so put them there
            i = Gtk.TreePath(path).get_indices()[0]
            self.adjlist.db[i] = dict((k.strip(), v.strip()) for k, v in
                                      (b.split("=", 1) for b in value.split() if "=" in b))
        elif col in (0, 1, 2):     # the rows must stay in order (changeval looks them up by bisection)
            self.adjlist.sort()

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

        # Delete from the end, so earlier indices don't shift; adjlist.db runs alongside the rows
        for i in sorted((p.get_indices()[0] for p in paths), reverse=True):
            model.remove(model.get_iter(Gtk.TreePath(i)))
            if self.adjlist is not None and i < len(self.adjlist.db):
                self.adjlist.db.pop(i)
        if self.adjlist is not None:
            self.adjlist.changed = True

    def on_key_press(self, widget, event):
        """Handles keypress events to delete selected rows when DEL is pressed."""
        if event.keyval == Gdk.KEY_Delete:
            self.delete_selected_rows()
