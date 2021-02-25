
import sys

# if 'gi.repository.Gtk' in sys.modules:

if 'gi.repository.Gtk' in sys.modules:
    from gi.repository import Gtk
    class MiniDialog(Gtk.Dialog):
        def __init__(self, parent, structure, title="Mini Dialog"):
            super().__init__(title=title, flags=0)
            self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK)
            self.parent = parent
            self.structure = structure
            box = self.get_content_area()
            box.set_orientation(Gtk.Orientation.VERTICAL)
            box.set_margin_bottom(6)
            box.set_margin_top(6)
            box.set_margin_left(6)
            box.set_margin_right(6)
            self.add_structure(structure, box)
            self.show_all()

        def add_structure(self, structure, box):
            for e in structure:
                if isinstance(e, (list, tuple)):
                    if box.get_orientation() == Gtk.Orientation.VERTICAL:
                        b = Gtk.HBox()
                    else:
                        b = Gtk.VBox()
                    box.add(b)
                    self.add_structure(e, b)
                else:
                    e.add_to(box, self.parent)

        def read_structure(self, structure):
            for e in structure:
                if isinstance(e, (list, tuple)):
                    self.read_structure(e)
                else:
                    e.read_val(self.parent)

        def _map(self, fn, structure):
            res = []
            for e in structure:
                if isinstance(e, (list, tuple)):
                    res += self._map(fn, e)
                else:
                    res.append(fn(e))
            return res

        def map(self, fn):
            return self._map(fn, self.structure)
            
        def run(self):
            response = super().run()
            if response == Gtk.ResponseType.OK:
                self.read_structure(self.structure)
            return response


class MiniWidget:
    def __init__(self, modelid, label):
        self.modelid = modelid
        self.label = label
        self.widget = None

    def get_model_val(self, view):
        return view.get(self.modelid, skipmissing=True)

    def set_model_val(self, view, val):
        view.set(self.modelid, val, skipmissing=True)


class MiniCheckButton(MiniWidget):
    def __init__(self, modelid, label, **kw):
        super().__init__(modelid, label)

    def add_to(self, box, view):
        if self.label is not None:
            self.widget = Gtk.CheckButton.new_with_label(self.label)
        else:
            self.widget = Gtk.CheckButton.new()
        val = self.get_model_val(view)
        self.widget.set_active(val)
        box.add(self.widget)

    def read_val(self, view):
        self.set_model_val(view, self.widget.get_active())     
