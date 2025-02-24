import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import json

class PolyglotSetup(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Settings for Polyglot")
        self.set_default_size(600, 450)

        # Load data from JSON file
        try:
            with open('data.json', 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

        # Dropdown options
        self.codes = ["L", "R", "A", "B", "C", "D", "E", "F", "G"]
        self.prjs = ["(None)", "BSB", "WSG", "WSGdev", "GRKNT", "WSGgong", "WSGlatin", "WSGBTpub"]
        # self.cfgs = ["(None)", "Normal", "2ndary", "Plain", "Gunjala", "Modern", "Default"]
        self.spread_side = ["1", "2"]

        # Create ListStore model
        self.liststore = Gtk.ListStore(str, str, str, str, bool, float, str)
        for item in self.data:
            code = list(item.keys())[0]
            values = item[code]
            self.liststore.append([
                code, values.get("spread_side", "1"), values['prj'], values['cfg'], \
                values['captions'], values.get("percentage", 50.0), values.get('color', "#FFFFFF")
            ])

        # Create TreeView
        self.treeview = Gtk.TreeView(model=self.liststore)
        self.treeview.set_reorderable(True)

        # Define Columns
        self.add_column("Code", 0, editable=True, renderer_type="combo", options=self.codes, align="center")
        self.add_column("1|2", 1, editable=True, renderer_type="combo", options=self.spread_side, align="center")
        self.add_column("Project", 2, editable=True, renderer_type="combo", options=self.prjs)
        self.add_column("Configuration", 3, editable=True, renderer_type="combo", options=['(None)'])
        self.add_column("Captions", 4, editable=True, renderer_type="toggle")
        self.add_column("% Width", 5, editable=True, renderer_type="text")
        self.add_column("Color", 6, editable=True, renderer_type="color")

        # Enable drag and drop
        self.treeview.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, [('text/plain', 0, 0)], Gdk.DragAction.MOVE)
        self.treeview.enable_model_drag_dest([('text/plain', 0, 0)], Gdk.DragAction.MOVE)
        self.treeview.connect("drag-data-received", self.on_drag_data_received)
        self.treeview.connect("drag-data-get", self.on_drag_data_get)
        self.treeview.connect("button-press-event", self.on_right_click)

        # We need to set up a unique cell renderer for each of the rows - based on the project
        # But I have no idea how to do so yet!
        # for row in self.liststore:
            # self.get_available_configs(row[2])
                    
        # Add TreeView to ScrolledWindow
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.treeview)

        # Layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.pack_start(scrolled_window, True, True, 0)
        self.add(vbox)
        
    def add_column(self, title, column_id, editable=False, renderer_type="text", options=None, align="left"):
        """Adds a column with the specified properties."""
        if renderer_type == "text":
            renderer = Gtk.CellRendererText()
            renderer.set_property("editable", editable)
            
            column = Gtk.TreeViewColumn(title, renderer, text=column_id)

            # Apply formatting function *only* to the % Width column (index 5)
            if column_id == 5:
                column.set_cell_data_func(renderer, self.format_width_data_func)
                renderer.connect("edited", self.on_width_edited, column_id)  # Connect edit event

            column.set_resizable(True)
            column.set_expand(True)
            
            self.treeview.append_column(column)
            return

        elif renderer_type == "toggle":
            renderer = Gtk.CellRendererToggle()
            renderer.set_property("activatable", True)
            renderer.connect("toggled", self.on_toggle, column_id)

            column = Gtk.TreeViewColumn(title, renderer, active=column_id)  # Bind "active" property
            column.set_resizable(True)
            column.set_expand(True)

            self.treeview.append_column(column)
            return  # Important! Prevents duplicate column creation

        elif renderer_type == "combo":
            renderer = Gtk.CellRendererCombo()
            # renderer.set_property("editable", editable)

            if column_id == 0:  # Special handling for 'Code' column
                self.code_renderer = renderer  # Store renderer reference
                options = self.get_available_codes()  # Get only available codes

            if column_id == 3:  # Special handling for 'Config' column
                self.config_renderer = renderer  # Store renderer reference
                options = self.get_available_configs()  # Get only available configs

            renderer.set_property("model", self.get_combo_model(options))
            renderer.set_property("text-column", 0)
            renderer.set_property("has-entry", False)
            renderer.connect("edited", self.on_combo_changed, column_id)
            if align == "center":
                renderer.set_property("xalign", 0.5)

        elif renderer_type == "color":
            renderer = Gtk.CellRendererText()
            renderer.set_property("text", " 🎨 Pick")
            column = Gtk.TreeViewColumn(title, renderer, text=column_id, background=column_id)
            column.set_resizable(True)
            column.set_expand(True)
            # renderer.connect("editing-started", self.on_color_clicked, column_id)
            self.treeview.append_column(column)
            self.treeview.connect("row-activated", self.on_color_clicked, column_id)
            # self.treeview.connect("editing-started", self.on_color_clicked, column_id)
            return
        
        if not isinstance(renderer, Gtk.CellRendererToggle):
            renderer.set_property("editable", editable)

        column = Gtk.TreeViewColumn(title, renderer, text=column_id)
        column.set_resizable(True)
        column.set_expand(True)
        self.treeview.append_column(column)

    def on_width_edited(self, widget, path, new_text, column_id):
        """Handles editing of the % Width column and ensures it updates the ListStore."""
        try:
            new_value = float(new_text)  # Convert input to float
            new_value = round(new_value, 1)  # Keep only 1 decimal place

            # Update the ListStore
            self.liststore[path][column_id] = new_value
            self.save_data()  # Save changes

            print(f"Updated % Width: Row {path} = {new_value}")  # Debug output

        except ValueError:
            print(f"Invalid input for % Width: {new_text}")  # Handle non-numeric input gracefully

    def format_width_data_func(self, column, cell, model, iter, data=None):  # Added `data=None`
        """Formats the % Width column to display only 1 decimal place."""
        value = model.get_value(iter, 5)  # Column index for % Width

        # Ensure the value is a float before formatting
        if isinstance(value, (int, float)):
            formatted_value = f"{value:.1f}"  # Format to 1 decimal place
            cell.set_property("text", formatted_value)
        else:
            cell.set_property("text", "")

    def get_available_codes(self, exclude_path=None):
        """Returns a list of unused codes, excluding the code in the given row (if any)."""
        used_codes = {row[0] for row in self.liststore if row[0]}  # Set of used codes

        if exclude_path is not None:
            current_code = self.liststore[exclude_path][0]  # Get current code of the row
            used_codes.discard(current_code)  # Allow reselecting the same code in the row

        available_codes = [code for code in self.codes if code not in used_codes]
        return available_codes

    def get_combo_model(self, options):
        """Creates a ListStore model for a combo box with given options."""
        model = Gtk.ListStore(str)
        for option in options:
            model.append([option])
        return model
        
    def on_combo_changed(self, widget, path, text, column_id):
        """Handles changes in combo box selections, preventing duplicate Code or Project+Config combinations."""
        if column_id == 0:  # Code column
            if text in {row[0] for row in self.liststore if row[0]}:
                print(f"Duplicate Code not allowed: {text}")
                return  # Prevent duplicate

        if column_id == 2:  # Project column changed
            available_configs = self.get_available_configs()
            
            # Update the configuration dropdown for this row
            self.liststore[path][3] = available_configs[0]  # Set first available config
            self.refresh_config_dropdown()  # Update the dropdown list

        if column_id == 2 or column_id == 3:  # Project or Configuration columns
            prj = self.liststore[path][2]
            cfg = self.liststore[path][3]
            
            if column_id == 2:
                prj = text  # If changing project
            else:
                cfg = text  # If changing configuration
            
            for row in self.liststore:
                if row[2] == prj and row[3] == cfg and self.liststore[path][0] != row[0]:  
                    print("Duplicate Project+Configuration not allowed.")
                    return  # Prevent duplicate
            
        self.liststore[path][column_id] = text
        self.save_data()
        
        # Refresh the Code and Config dropdowns after updating
        if column_id == 0:
            self.refresh_code_dropdowns()
        if column_id == 2:
            self.refresh_config_dropdown()

    def refresh_code_dropdowns(self):
        """Refreshes the combo box dropdown for the Code column with updated available codes."""
        if hasattr(self, "code_renderer"):  # Ensure renderer exists before updating
            available_codes = self.get_available_codes()
            self.code_renderer.set_property("model", self.get_combo_model(available_codes))

    def refresh_config_dropdown(self):
        """Refreshes the combo box dropdown for the Config column with updated available configs for the project."""
        if hasattr(self, "config_renderer"):  # Ensure renderer exists before updating
            available_configs = self.get_available_configs()
            self.config_renderer.set_property("model", self.get_combo_model(available_configs))

    def on_color_clicked(self, widget, path, text, column_id):
        """Opens a color picker and updates the selected row's color."""
        model = self.liststore
        iter = model.get_iter(path)
        dialog = Gtk.ColorChooserDialog(title="Pick a background color", parent=self)
        current_color = model[path][column_id]  # Hex color format
        if current_color:
            rgba = Gdk.RGBA()
            rgba.parse(current_color)
            dialog.set_rgba(rgba)

        if dialog.run() == Gtk.ResponseType.OK:
            color = dialog.get_rgba()
            color_hex = "#{:02x}{:02x}{:02x}".format(
                int(color.red * 255),
                int(color.green * 255),
                int(color.blue * 255)
            )
            model.set_value(iter, column_id, color_hex)  # Update color in ListStore
            self.save_data()  # Save changes

        dialog.destroy()

    def on_toggle(self, widget, path, column_id):
        """Handles toggling checkboxes in the Captions column."""
        model = self.liststore
        iter = model.get_iter(path)  # Get the iterator for the row
        current_value = model.get_value(iter, column_id)  # Read current state
        model.set_value(iter, column_id, not current_value)  # Toggle it
        self.save_data()
        
    def get_selected_row(self):
        """Returns (model, iter, path) of the selected row, or None if none is selected."""
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            return model, iter, model.get_path(iter)
        return None

    def on_drag_data_received(self, treeview, drag_context, x, y, selection, info, time):
        """Handles dropping a row at a new position in the TreeView."""
        model = treeview.get_model()
        drop_info = treeview.get_dest_row_at_pos(x, y)

        dragged_path_str = selection.get_text().strip()  # Get the dragged row path as a string
        if not dragged_path_str:
            return  # Prevent crashes if the selection is empty

        dragged_iter = model.get_iter_from_string(dragged_path_str)  # Get the dragged row iterator
        dragged_data = list(model[dragged_iter])  # Copy row data before removing

        if drop_info:
            path, position = drop_info
            target_iter = model.get_iter(path)

            # Move before or after the target row
            if position == Gtk.TreeViewDropPosition.BEFORE:
                new_iter = model.insert_before(target_iter, dragged_data)
            else:
                new_iter = model.insert_after(target_iter, dragged_data)

            # Remove the old row after insertion
            model.remove(dragged_iter)

            self.save_data()

    def on_right_click(self, widget, event):
        """Shows a context menu on right-click."""
        if event.button == 3:
            menu = Gtk.Menu()

            add_item = Gtk.MenuItem(label="Add a row/text")
            add_item.connect("activate", self.add_row)
            menu.append(add_item)

            delete_item = Gtk.MenuItem(label="Delete Row")
            delete_item.connect("activate", self.delete_selected_row)
            menu.append(delete_item)

            move_up_item = Gtk.MenuItem(label="Move Up")
            move_up_item.connect("activate", self.move_selected_row, -1)
            menu.append(move_up_item)

            move_down_item = Gtk.MenuItem(label="Move Down")
            move_down_item.connect("activate", self.move_selected_row, 1)
            menu.append(move_down_item)

            move_down_item = Gtk.MenuItem(label="Edit Configuration...")
            move_down_item.connect("activate", self.edit_other_config)
            menu.append(move_down_item)

            menu.show_all()
            menu.popup_at_pointer(event)

    def change_config(self, prj, cfg):
        """Stub function for opening config."""
        print(f"Opening config for Project: {prj}, Configuration: {cfg} ...")

    def delete_selected_row(self, widget):
        """Deletes the selected row."""
        selected = self.get_selected_row()
        if selected:
            model, iter, _ = selected
            model.remove(iter)
            self.save_data()
            self.refresh_code_dropdowns()  # Refresh available codes

    def edit_other_config(self, widget):
        """Starts up another instance of PTXprint to edit one of the polyglot configs."""
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            prj = model.get_value(iter, 2)
            cfg = model.get_value(iter, 3)
            print(f"Editing other config for: {prj}+{cfg}")

    def add_row(self, widget):
        """Adds a new row to the list."""
        self.liststore.append(["", "1", "(None)", "(None)", False, 33.3, "#FFFFFF"])
        self.save_data()
        
    def move_selected_row(self, widget, direction):
        """Moves the selected row up (-1) or down (+1)."""
        selected = self.get_selected_row()
        if selected:
            model, iter, path = selected
            index = path.get_indices()[0]
            new_index = index + direction

            if 0 <= new_index < len(model):
                row_data = list(model[iter])
                model.remove(iter)
                new_iter = model.insert(new_index, row_data)

                # Update selection to new position
                selection = self.treeview.get_selection()
                selection.select_iter(new_iter)

                self.save_data()

    def on_drag_data_get(self, treeview, drag_context, selection_data, info, time):
        """Stores the dragged row's index in the selection_data object."""
        model, iter = treeview.get_selection().get_selected()
        if iter:
            path = model.get_path(iter).to_string()  # Get row index as a string
            selection_data.set_text(path, -1)  # Store it in drag data

    def on_drag_data_received(self, treeview, drag_context, x, y, selection, info, time):
        """Handles dropping a row at a new position in the TreeView."""
        model = treeview.get_model()
        drop_info = treeview.get_dest_row_at_pos(x, y)

        dragged_path_str = selection.get_text().strip()  # Get the dragged row path as a string
        if not dragged_path_str:
            return  # Prevent crashes if the selection is empty

        dragged_iter = model.get_iter_from_string(dragged_path_str)  # Get the dragged row iterator
        dragged_data = list(model[dragged_iter])  # Copy row data before removing

        if drop_info:
            path, position = drop_info
            target_iter = model.get_iter(path)

            # Move before or after the target row
            if position == Gtk.TreeViewDropPosition.BEFORE:
                new_iter = model.insert_before(target_iter, dragged_data)
            else:
                new_iter = model.insert_after(target_iter, dragged_data)

            # Remove the old row after insertion
            model.remove(dragged_iter)

            self.save_data()  # Save changes

    def get_available_configs(self, project=None):
        """Returns a list of available configurations for the current row's project."""
        configs = {
            "BSB": ["Default", "Modern"],
            "WSG": ["Normal", "2ndary", "Plain", "Gospels-n-Acts"],
            "WSGdev": ["Default", "Plain"],
            "GRKNT": ["Normal", "Modern", "Plain"],
            "WSGgong": ["Gunjala", "2ndary"],
            "WSGlatin": ["Default", "Modern", "Gospels-n-Acts"],
            "WSGBTpub": ["Normal", "Plain"],
        }
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        if project is None:
            if iter:
                project = model.get_value(iter, 2)
            else:
                project = "(None)"
        return configs.get(project, ["(None)"])  # Default to ["(None)"] if project not found

    def save_data(self):
        """Saves the liststore data to a JSON file."""
        data = [{row[0]: {"spread_side": row[1], "prj": row[2], "cfg": row[3], "captions": row[4], "percentage": row[5], "color": row[6]}} for row in self.liststore]
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)

win = PolyglotSetup()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
