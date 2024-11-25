from gi.repository import Gtk

headers = ['Book', 'C.V', 'Para', 'Stretch', 'Marker', 'Expand']

class AdjListView:
    def __init__(self, parent):
        self.parent = parent
        self.adjlist = None
        self.view = Gtk.TreeView()
        for i in range(6):
            cr = Gtk.CellRendererText(editable=True)
            cr.connect("edited", self.edit, i)
            col = Gtk.TreeViewColumn(cell_renderer=cr, text=i, title=headers[i])
            self.view.append_column(col)

    def edit(self, widget, path, value, col):
        self.view.get_model()[path][col] = int(value) if col in (2, 5) else value

    def set_model(self, adjlist, save=True):
        if self.adjlist is not None:
            if save:
                self.adjlist.save()
        self.adjlist = adjlist
        self.view.set_model(None if adjlist is None else adjlist.liststore)
        if adjlist is not None:
            adjlist.changed = True      # close enough
