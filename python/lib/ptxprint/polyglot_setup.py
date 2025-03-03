import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import re, json
from enum import IntEnum
from ptxprint.utils import _

_modeltypes = (str, str, str, str, bool, float, str, str, str, int)
_modelfields = ('code', 'pg', 'prj', 'cfg', 'captions', 'width', 'color', 'tooltip', 'widcol', 'bold')
m = IntEnum('m', [(x, i) for i, x in enumerate(_modelfields)])

class PolyglotSetup(Gtk.Box):
    def __init__(self, builder, tv):
        self.builder = builder
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # Load data from JSON file #FixMe!
        try:
            with open('data.json', 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

        # Dropdown options
        self.codes = ["L", "R", "A", "B", "C", "D", "E", "F", "G"]
        self.spread_side = ["1", "2"]
        # Get the shared project ListStore from the builder
        self.project_liststore = self.builder.get_object("ls_projects")

        # Use the existing treeview instead of creating a new one
        self.treeview = tv  
        self.treeview.set_reorderable(True)

        # Create ListStore model if not already set
        if self.treeview.get_model() is None:
            self.liststore = Gtk.ListStore(*_modeltypes)  
            self.treeview.set_model(self.liststore)
        else:
            self.liststore = self.treeview.get_model()

        for item in self.data:
            code = list(item.keys())[m.code]
            values = item[code]
            self.liststore.append([
                code, values.get("spread_side", "1"), values['prj'], values['cfg'],
                values['captions'], values.get("percentage", 50.0), values.get('color', "#FFFFFF"),
                "Right-Click for options", "#000000", 400
            ])

        # Define Columns
        self.add_column("Code", m.code, editable=True, renderer_type="combo", options=self.codes, align="center")
        self.add_column("1|2", m.pg, editable=True, renderer_type="combo", options=self.spread_side, align="center")
        self.add_column("Project", m.prj, editable=True, renderer_type="combo", options=self.project_liststore)
        self.add_column("Configuration", m.cfg, editable=True, renderer_type="combo", options=['(None)'])
        self.add_column("Captions", m.captions, editable=True, renderer_type="toggle")
        self.add_column("% Width", m.width, editable=True, renderer_type="text")

        # Enable drag and drop
        self.treeview.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, [('text/plain', 0, 0)], Gdk.DragAction.MOVE)
        self.treeview.enable_model_drag_dest([('text/plain', 0, 0)], Gdk.DragAction.MOVE)
        self.treeview.connect("drag-data-received", self.on_drag_data_received)
        self.treeview.connect("drag-data-get", self.on_drag_data_get)
        self.treeview.connect("button-press-event", self.on_right_click)

        self.validate_page_widths() # Make sure % Width gets colored red if invalid (even on loading)

        # Add TreeView to Layout
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        scrolled_window.add(self.treeview)

        self.pack_start(scrolled_window, True, True, 0)
        self.update_layout_string()
        self.update_layout_preview()

    def row_draggable(self, model, path):
        """Prevents Row 0 from being dragged."""
        row_index = path.get_indices()[0]  # Get row index
        if row_index == 0:
            print("Drag prevented: Row 0 cannot be moved.")
            return False  # 🚫 Prevent Row 0 from being dragged
        return True  # ✅ Allow other rows to be dragged

    def row_drop_possible(self, model, dest_path, selection_data):
        """Prevents dropping any row into Row 0."""
        target_index = dest_path.get_indices()[0]  # Get destination row index
        dragged_index = int(selection_data.get_text().strip()) if selection_data.get_text() else None

        # 🚫 Prevent dropping into Row 0
        if target_index == 0:
            print("Drop prevented: Cannot drop into Row 0.")
            return False

        # 🚫 Prevent Row 0 from being moved at all
        if dragged_index == 0:
            print("Drop prevented: Row 0 cannot be moved.")
            return False

        return True  # ✅ Allow all other valid drops

    def get_treeview(self):
        """ Expose the TreeView for integration with other modules. """
        return self.treeview        
        
    def add_column(self, title, column_id, editable=False, renderer_type="text", options=None, align="left"):
        """Adds a column with the specified properties."""
        if renderer_type == "text":
            renderer = Gtk.CellRendererText()
            renderer.set_property("editable", editable)
            
            # Only apply text color formatting to the % Width column
            column = Gtk.TreeViewColumn(title, renderer, text=column_id)
            if column_id == 5:
                column.add_attribute(renderer, "foreground", 8)  # Use column 8 for text color
                column.add_attribute(renderer, "weight", 9)      # Use column 9 for bold effect

            # Store tooltips inside the last column (index 7)
            if column_id in range(0,7):
                self.treeview.set_has_tooltip(True)  # Enable tooltips
                self.treeview.connect("query-tooltip", self.on_query_tooltip)  # Connect event

            # Apply formatting function *only* to the % Width column (index 5)
            if column_id == 5:
                column.set_cell_data_func(renderer, self.format_width_data_func)
                renderer.connect("edited", self.on_width_edited, column_id)  # Connect edit event
            column.set_fixed_width(70)  # Increase width (default is often too narrow)
            column.set_alignment(1.0)   # This sets the column title on the right.
            column.set_resizable(True)
            # column.set_expand(True)
            
            self.treeview.append_column(column)
            return

        elif renderer_type == "toggle":
            renderer = Gtk.CellRendererToggle()
            renderer.set_property("activatable", True)
            renderer.connect("toggled", self.on_toggle, column_id)

            column = Gtk.TreeViewColumn(title, renderer, active=column_id)  # Bind "active" property
            column.set_fixed_width(70)  # Increase width (default is often too narrow)
            column.set_alignment(0.5)
            column.set_resizable(True)
            # column.set_expand(True)

            self.treeview.append_column(column)
            return  # Important! Prevents duplicate column creation

        elif renderer_type == "combo":
            # Function to disable editing and gray out text for Row 0
            def disable_edit_for_first_row(column, cell, model, iter, data=None):
                path = model.get_path(iter).to_string()
                if path == "0" and column_id in [0, 2, 3]:  # Lock Code, Project, and Config in Row 0
                    cell.set_property("editable", False)  # Prevent edits
                    cell.set_property("foreground", "#888888")  # Gray out text
                    cell.set_property("has-entry", False)  # Hide dropdown
                else:
                    cell.set_property("editable", True)  # Normal for other rows
                    cell.set_property("foreground", "#000000")  # Black text
                    # cell.set_property("has-entry", True)  # Allow dropdown

            # Create a CellRendererCombo
            renderer = Gtk.CellRendererCombo()
            renderer.set_property("editable", True)
            renderer.set_property("text-column", 0)
            renderer.set_property("has-entry", False)
            renderer.connect("edited", self.on_combo_changed, column_id)

            # Special handling for 'Code' column (column 0)
            if column_id == 0:
                self.code_renderer = renderer  # Store renderer reference
                options = self.get_available_codes()  # Get only available codes
                renderer.set_property("model", self.get_combo_model(options))

                # renderer = Gtk.CellRendererText()
                # renderer.set_property("editable", True)
                renderer.set_property("background-set", True)
                column = Gtk.TreeViewColumn(title, renderer, text=column_id, background=m.color)
                self.treeview.append_column(column)
                self.treeview.connect("row-activated", self.on_color_clicked, column_id)                

            # Special handling for 'Config' column (column 3)
            if column_id == 3:  # Special handling for 'Config' column
                renderer = Gtk.CellRendererCombo()
                renderer.set_property("editable", True)
                renderer.set_property("text-column", 0)
                renderer.set_property("has-entry", False)
                renderer.connect("edited", self.on_combo_changed, column_id)

                column = Gtk.TreeViewColumn(title, renderer, text=column_id)
                column.set_cell_data_func(renderer, self.config_cell_data_func)  # Dynamic per-row options
                column.set_resizable(True)
                column.set_expand(True)

                self.treeview.append_column(column)
                return

            wide = int(len(options) / 16) + 1 if len(options) > 14 else 1

            if isinstance(options, Gtk.ListStore):  # If options is a ListStore, use it directly
                renderer.set_property("model", options)
            else:  # Otherwise, assume it's a list and convert it
                renderer.set_property("model", self.get_combo_model(options))

            # Connect the signal to apply wrap-width dynamically
            renderer.connect("editing-started", self.on_editing_started)

            if align == "center":
                renderer.set_property("xalign", 0.5)
            
            # Create column (avoiding duplicates)
            existing_columns = [col.get_title() for col in self.treeview.get_columns()]
            if title not in existing_columns:  # Prevent duplicate columns
                column = Gtk.TreeViewColumn(title, renderer, text=column_id)
                if column_id == 2:
                    column.set_fixed_width(100)  # Increase width (default is often too narrow)
                    column.set_resizable(True)
                column.set_cell_data_func(renderer, disable_edit_for_first_row)  # Apply locking
                self.treeview.append_column(column)

        if not isinstance(renderer, Gtk.CellRendererToggle):
            renderer.set_property("editable", editable)

        column = Gtk.TreeViewColumn(title, renderer, text=column_id)
        # Center-align the headers for Code, 1|2, and Captions
        if column_id in [0, 1, 4]:  
            column.set_alignment(0.5)  # Center align the column title
        if column_id in [0, 1, 2]:
            return
        column.set_resizable(True)
        column.set_expand(True)
        self.treeview.append_column(column)

    def on_editing_started(self, cell, editable, path):
        """
        This method is called when a cell with a dropdown is being edited.
        It dynamically applies wrap width to the dropdown for multi-column support.
        """
        if isinstance(editable, Gtk.ComboBox):
            # Dynamically set wrap width based on the number of items
            num_projects = len(self.project_liststore) if hasattr(self, "project_liststore") else 0
            number_of_columns = max(1, num_projects // 16) + 1 if num_projects > 14 else 1
            editable.set_wrap_width(number_of_columns)

    def on_color_typed(self, widget, path, text, column_id):
        """Handles direct text input in the Color column, ensuring valid HEX codes."""
        text = text.strip()  # Remove spaces

        # Validate HEX color format
        if len(text) == 7 and text.startswith("#"):
            try:
                # Convert from HEX to ensure validity
                int(text[1:], 16)  
                self.liststore[path][column_id] = text  # Save valid color
                self.save_data()
            except ValueError:
                print(f"Invalid color code: {text}")  # Invalid HEX
        else:
            print(f"Invalid color format: {text}")  # Wrong format

    def on_query_tooltip(self, widget, x, y, keyboard_mode, tooltip):
        """Displays tooltips dynamically based on column."""
        path_info = self.treeview.get_path_at_pos(x, y)

        if path_info is not None:
            path, column, y, z = path_info

            # Find the correct column index
            column_id = self.treeview.get_columns().index(column)

            # Set tooltip text based on the column
            tooltips = {
                0: _("Unique identifier for the text/glot (L, R, A, B, C, ... G)"),
                1: _("Specify whether the should be on the left (1) or right (2) page."),
                2: _("The (Paratext) project code."),
                3: _("The configuration settings to be applied for the selected project."),
                4: _("Whether to show captions for this text."),
                5: _("The page width (as %) that this text should occupy.\nIf the values are red, this indicates that the total doesn't\nadd to 100%, so adjust the values.\nUse right-click menu option to distribute width evenly between columns."),
                # 6: _("[Optional] Type #color code, or right-click to change background color for this text.")
            }

            # Apply the correct tooltip based on column
            if column_id in tooltips:
                tooltip.set_text(tooltips[column_id])
                return True  # Tooltip set successfully

        return False  # No tooltip found

    def config_cell_data_func(self, column, cell, model, iter, data=None):
        """Dynamically sets the available configurations per row and locks Row 0."""
        path = model.get_path(iter).to_string()
        project = model.get_value(iter, 2)  # Column 2 contains the Project
        available_configs = self.get_available_configs(project)  # Get configs for that project

        # Ensure Row 0 is locked
        if path == "0":  # If this is the first row
            cell.set_property("editable", False)  # Disable dropdown
            cell.set_property("foreground", "#888888")  # Gray out text
            cell.set_property("has-entry", False)  # Prevent dropdown
        else:
            cell.set_property("editable", True)  # Enable dropdown for other rows
            cell.set_property("foreground", "#000000")  # Normal text color
            # cell.set_property("has-entry", True)  # Allow dropdown

        # Apply the correct config options for the row
        cell.set_property("model", self.get_combo_model(available_configs))

    def on_width_edited(self, widget, path, new_text, column_id):
        """Handles editing of the % Width column and ensures it updates the ListStore."""
        try:
            new_value = float(new_text)      # Convert input to float
            new_value = round(new_value, 2)  # Keep 2 decimal places

            # Update the ListStore
            self.liststore[path][column_id] = new_value
            self.validate_page_widths() # Validate total widths after any edit
            self.save_data()  # Save changes

        except ValueError:
            print(f"Invalid input for % Width: {new_text}")  # Handle non-numeric input gracefully

    def format_width_data_func(self, column, cell, model, iter, data=None):  # Added `data=None`
        """Formats the % Width column to display 2 decimal places."""
        value = model.get_value(iter, 5)  # Column index for % Width

        # Ensure the value is a float before formatting
        if isinstance(value, (int, float)):
            formatted_value = f"{value:.2f}"  # Format to 2 decimal places
            cell.set_property("text", formatted_value)
            cell.set_property("xalign", 1.0)  # 1.0 = Right, 0.5 = Center, 0.0 = Left
        else:
            cell.set_property("text", "")

    def get_available_codes(self, exclude_path=None):
        """Returns a list of unused codes, excluding the code in the given row (if any)."""
        used_codes = {row[m.code] for row in self.liststore if row[m.code]}  # Set of used codes

        if exclude_path is not None:
            current_code = self.liststore[exclude_path][m.code]
            used_codes.discard(current_code)

        available_codes = [code for code in self.codes if code not in used_codes]
        return available_codes

    def get_combo_model(self, options):
        """Creates a ListStore model for a combo box with given options."""
        model = Gtk.ListStore(str)
        for option in options:
            model.append([option])
        return model
        
    def on_combo_changed(self, widget, path, text, column_id):
        """Handles changes in combo box selections, preventing duplicate Code or Project+Config combinations. Prevents edits in row 0 for certain fields."""
        if path == "0" and column_id in [0, 2, 3]:  # Row 0 should not be editable for these columns
            print(f"Editing not allowed for Row 0 in column {column_id}.")
            return
        
        if column_id == 0:  # Code column
            if text in {row[m.code] for row in self.liststore if row[m.code]}:
                print(f"Duplicate Code not allowed: {text}")
                return  # Prevent duplicate
            
        if column_id == 2:  # Project column changed
            available_configs = self.get_available_configs(text)  # Get new configs for the selected project
            self.liststore[path][m.cfg] = available_configs[m.code]  # Set first available config for this row
            self.treeview.queue_draw()  # Refresh UI

        if column_id == 2 or column_id == 3:  # Project or Configuration columns
            prj = self.liststore[path][m.prj]
            cfg = self.liststore[path][m.cfg]
            
            if column_id == 2:
                prj = text  # If changing project
            else:
                cfg = text  # If changing configuration
            
            for row in self.liststore:
                if row[m.prj] == prj and row[m.cfg] == cfg and self.liststore[path][m.code] != row[m.code]:
                    # FixMe! Turn this into a proper error/warning message.
                    print("Duplicate Project+Configuration not allowed.")
                    return  # Prevent duplicate
            
        self.liststore[path][column_id] = text
        self.save_data()
        
        # Refresh dropdowns and other dependencies after updating the combo box
        if column_id == 0:    # Unique code changed
            self.refresh_code_dropdowns()
        elif column_id == 1:  # Page 1 or 2 changed
            self.validate_page_widths()
            self.treeview.queue_draw()  # Refresh UI
        elif column_id == 2:  # Project changed
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

    def set_color_from_menu(self, widget):
        """Opens the color picker for the selected row via the context menu."""
        selected = self.get_selected_row()
        if selected:
            model, iter, path = selected
            column_id = 6  # Color column index
            self.on_color_clicked(None, path, model[path][column_id], column_id)

    def on_color_clicked(self, widget, path, text, column_id):
        """Opens a color picker and updates the selected row's color."""
        model = self.liststore
        iter = model.get_iter(path)
        # Find the top-level window (main parent)
        parent_window = self.get_toplevel() if hasattr(self, "get_toplevel") else None
        # Create the color picker with a valid parent
        dialog = Gtk.ColorChooserDialog(title="Pick a background color", parent=parent_window)

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

    def on_right_click(self, widget, event):
        """Shows a context menu on right-click, disabling options for Row 0."""
        if event.button == 3:  # Right-click
            self.context_menu = Gtk.Menu()  # Store reference

            # Get the row that was right-clicked on
            path_info = self.treeview.get_path_at_pos(int(event.x), int(event.y))
            if path_info:
                path, column, a, b = path_info
                row_index = path.get_indices()[0]  # Extract the row index
            else:
                row_index = None  # No valid row found

            is_first_row = row_index == 0  # Check if row 0 was clicked

            add_item = Gtk.MenuItem(label=_("Add a row/text"))
            add_item.connect("activate", self.add_row)
            self.context_menu.append(add_item)

            move_up_item = Gtk.MenuItem(label=_("Move Up"))
            move_up_item.connect("activate", self.move_selected_row, -1)
            move_up_item.set_sensitive(not is_first_row and not row_index == 1)  # Disable if Row 0
            self.context_menu.append(move_up_item)

            move_down_item = Gtk.MenuItem(label=_("Move Down"))
            move_down_item.connect("activate", self.move_selected_row, 1)
            move_down_item.set_sensitive(not is_first_row)  # Disable if Row 0
            self.context_menu.append(move_down_item)

            distribute_item = Gtk.MenuItem(label=_("Distribute Widths"))
            distribute_item.connect("activate", self.distribute_width_evenly)
            self.context_menu.append(distribute_item)

            delete_item = Gtk.MenuItem(label=_("Delete Row"))
            delete_item.connect("activate", self.delete_selected_row)
            delete_item.set_sensitive(not is_first_row)  # Disable if Row 0
            self.context_menu.append(delete_item)

            color_item = Gtk.MenuItem(label=_("Set Color..."))
            color_item.connect("activate", self.set_color_from_menu)
            self.context_menu.append(color_item)

            self.context_menu.show_all()
            self.update_context_menu()  # Apply correct state
            self.context_menu.popup_at_pointer(event)

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
            self.update_context_menu()     # Refresh menu state
            self.validate_page_widths()    # Refresh color of % width

    def update_context_menu(self):
        """Enables or disables the 'Add a row/text' menu option based on the row count."""
        max_rows = 9
        has_room = len(self.liststore) < max_rows

        for item in self.context_menu.get_children():
            if isinstance(item, Gtk.MenuItem) and item.get_label() == "Add a row/text":
                item.set_sensitive(has_room)  # Enable/disable based on row count

    def edit_other_config(self, widget):
        """Starts up another instance of PTXprint to edit one of the polyglot configs."""
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            prj = model.get_value(iter, 2)
            cfg = model.get_value(iter, 3)
            print(f"Editing other config for: {prj}+{cfg}")

    def add_row(self, widget):
        """Adds a new row with the next available code; ensuring row 0 is locked to 'L'."""
        if len(self.liststore) >= 9:
            print("Maximum of 9 rows reached. Cannot add more.")
            return  # Stop if the limit is reached

        if len(self.liststore) == 0:  # First row must be locked
            pri_prj = 'WSG' # FixMe!
            pri_cfg = 'Gospels-n-Acts' # FixMe!
            self.liststore.append(["L", "1", pri_prj, pri_cfg, False, 33.33, "#FFFFFF", "Right-Click for options", "#000000", 400])
        else:
            available_codes = self.get_available_codes()
            next_code = str(available_codes[m.code]) if available_codes else ""  # Auto-assign next available code

            self.liststore.append([next_code, "1", "(None)", "(None)", False, 50.0, "#FFFFFF", "Right-Click for options", "#000000", 400])

        self.save_data()
        self.refresh_code_dropdowns()  # Refresh available codes
        self.validate_page_widths() # Validate total widths after adding a row
        self.update_context_menu()  # Refresh menu state
        self.save_data()

    def move_selected_row(self, widget, direction):
        """Moves the selected row up (-1) or down (+1)."""
        selected = self.get_selected_row()
        if selected:
            model, iter, path = selected
            index = path.get_indices()[m.code]
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
            
            # Allow row 0 to be dragged, but do not move it
            selection_data.set_text(path, -1)  # Store it in drag data

    def on_drag_data_received(self, treeview, drag_context, x, y, selection, info, time):
        """Handles dropping a row at a new position in the TreeView."""
        model = treeview.get_model()
        drop_info = treeview.get_dest_row_at_pos(x, y)

        dragged_path_str = selection.get_text()  # Get the dragged row path as a string

        if not dragged_path_str:  # Check if dragged data is empty
            return  # Prevent crashes if the selection is empty or None

        dragged_path_str = dragged_path_str.strip()  # Safe to call .strip() now

        dragged_iter = model.get_iter_from_string(dragged_path_str)  # Get the dragged row iterator
        dragged_data = list(model[dragged_iter])  # Copy row data before removing

        # Get the target row at the drop position
        if drop_info:
            path, position = drop_info
            
            # Prevent dropping row 0 to another row
            if dragged_path_str == "0":
                # Re-insert row 0 at its original position
                model.insert_before(model.get_iter_first(), dragged_data)  # Insert at the beginning (index 0)
                return  # Row 0 goes back to where it was; no need to proceed further

            # Prevent drop on row 0
            if path.to_string() == "0":
                return  # Do nothing if trying to drop onto row 0

            target_iter = model.get_iter(path)

            # Move before or after the target row
            if position == Gtk.TreeViewDropPosition.BEFORE:
                new_iter = model.insert_before(target_iter, dragged_data)
            else:
                new_iter = model.insert_after(target_iter, dragged_data)

            # Remove the old row after insertion
            model.remove(dragged_iter)

            self.save_data()  # Save changes

    def distribute_width_evenly(self, widget):
        """Evenly distributes the % Width across all rows sharing the same page (1 or 2)."""
        selected = self.get_selected_row()
        if not selected:
            return  # No row selected

        model, iter, path = selected
        page = model[path][m.pg]

        # Find all rows that share the same page (1 or 2)
        same_page_rows = [row for row in range(len(model)) if model[row][m.pg] == page]
        row_count = len(same_page_rows)

        if row_count == 0:
            return  # Avoid division by zero

        new_width = round(100.0 / row_count, 2)  # Calculate even width per row

        # Apply the new width to each row
        for row in same_page_rows:
            model[row][m.width] = new_width

        self.save_data()
        self.validate_page_widths()  # Refresh highlighting

    def validate_page_widths(self):
        """Checks that the total width per page (1|2) is 100% and highlights invalid rows."""
        page_totals = {"1": 0.0, "2": 0.0}  # Track total % width per page

        # Step 1: Calculate total widths for each page (1 or 2)
        for row in range(len(self.liststore)):
            page = self.liststore[row][m.pg]
            width = self.liststore[row][m.width]
            page_totals[page] += width  # Accumulate width for each page

        # Step 2: Apply formatting to **every row** that shares the same `1|2` page value
        for row in range(len(self.liststore)):
            page = self.liststore[row][m.pg]
            total = page_totals[page]  # Get total width for this page
            is_invalid = abs(total - 100.0) > 0.02  # Allow small floating-point errors
            # print(f"{page=}  {total=}  {is_invalid=}")

            text_color = "#FF0000" if is_invalid else "#000000"  # Red if invalid, black if valid
            font_weight = 700 if is_invalid else 400  # Bold if invalid, normal if valid

            self.liststore[row][8] = text_color  # Update text color
            self.liststore[row][9] = font_weight  # Update font weight

        self.treeview.queue_draw()  # Refresh UI

    def get_available_configs(self, project=None): #FixMe!
        # This method will need to be updated once integrated into the main code.
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

    def save_data(self): #FixMe!
        """Saves the liststore data to a JSON file."""
        data = [{row[m.code]: {"spread_side": row[m.pg], "prj": row[m.prj], "cfg": row[m.cfg], "captions": row[m.captions], "percentage": row[m.width], "color": row[m.color]}} for row in self.liststore]
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)
        self.update_layout_string()
            
    def update_layout_string(self):
        t = self.generate_layout_from_treeview()
        w = self.builder.get_object('t_layout')
        if not "\\" in w.get_text():
            w.set_text(t)
            self.update_layout_preview()

    def generate_layout_from_treeview(self):
        """
        Generates a valid layout string based on the current TreeView data.
        - Extracts the letter codes and their '1|2' values.
        - Constructs a valid layout format (without '/' for now).
        - Ensures 'L' and 'R' are always included.
        - Adds a ',' if there are texts on both '1' and '2'.
        
        :return: A valid layout string.
        """

        # Step 1: Extract used codes and their '1|2' values from the ListStore
        codes_by_side = {"1": [], "2": []}  # Store codes grouped by page side
        for row in self.liststore:
            code, side = row[m.code], row[m.pg]
            if code:
                codes_by_side[side].append(code)

        # Step 2: Construct the layout string
        left_side = "".join(codes_by_side["1"])  # Combine left side letters
        right_side = "".join(codes_by_side["2"])  # Combine right side letters

        # Step 3: If both '1' and '2' exist, separate them with a comma ','
        if left_side and right_side:
            return f"{left_side},{right_side}"
        else:
            return left_side or right_side  # Return whichever side has values

    def validate_layout(self, t_layout, liststore):
        """
        Validates the layout string in t_layout based on the updated rules.

        :param t_layout: The input string from the text box.
        :param liststore: The Gtk.ListStore containing used letter codes and their assigned 1|2 values.
        :return: (is_valid, error_message) - Boolean validity and error message if invalid.
        """
        # Rule 2: Ensure there are no spaces
        if " " in t_layout:
            return False, "Layout must not contain spaces."

        # Extract used codes and their '1|2' values from the ListStore
        used_codes = {}  # Dictionary mapping codes -> '1' or '2'
        for row in liststore:
            code, side = row[m.code], row[m.pg]
            if code:
                used_codes[code] = side

        all_used_codes = set(used_codes.keys())  # Set of valid codes from TreeView
        all_layout_codes = set(re.findall(r"[A-Z]", t_layout))  # Extract all letter codes from layout

        # Rule 1: Ensure all letters in t_layout exist in the used_codes
        all_letters = set("".join(t_layout.replace(",", "").replace("/", "")))
        if not all_letters.issubset(set(used_codes.keys())):
            return False, "Layout contains invalid codes."

        # Rule 3: If both '1' and '2' exist in the ListStore, a comma must be present
        if "1" in used_codes.values() and "2" in used_codes.values() and "," not in t_layout:
            return False, "Layout must contain a comma to indicate separate sides."

        # Rule 4: Ensure left-side codes appear in '1' and right-side codes in '2'
        if "," in t_layout:
            left_side, right_side = t_layout.split(",", 1)
            left_codes = set(left_side.replace("/", ""))
            right_codes = set(right_side.replace("/", ""))
            if not left_codes.issubset({k for k, v in used_codes.items() if v == "1"}):
                return False, "Left-side codes must be assigned to '1'."
            if not right_codes.issubset({k for k, v in used_codes.items() if v == "2"}):
                return False, "Right-side codes must be assigned to '2'."

        # Rule 5: Ensure '/' is used correctly (not at start or end, no consecutive slashes)
        if t_layout.startswith("/") or t_layout.endswith("/") or "//" in t_layout:
            return False, "Slashes must be between letters and not at the start or end."
            
        # Rule 6: Ensure L and R are always present
        if not ("L" in all_letters and "R" in all_letters):
            return False, "Layout must include both L and R."

        # Rule 7 (NEW): Ensure all codes in the TreeView are included in t_layout
        missing_codes = all_used_codes - all_layout_codes
        if missing_codes:
            return False, f"Missing codes in layout: {', '.join(missing_codes)}"
            
        # Rule 10: Hyphen '-' is allowed to indicate a blank page
        valid_chars = set(used_codes.keys()).union({",", "/", "-"})
        if not set(t_layout).issubset(valid_chars):
            return False, "Layout contains invalid characters."

        return True, "Valid layout."

    def testValidator(self, x):
        print(f"Layout: {t}")
        for l in "LR L,R L/R L,RA LR,A L,R/A L/R,A L/R,AB L/R,A/B LR,ABC L/RA,B/CD L/A/B,R/C/D LR/ /LR AB AB,CD A/B LR/AB".split():
            is_valid, message = self.validate_layout(l, self.liststore)

            if not is_valid:
                print(f"Error: {l} - {message}")
            else:
                print(f"Valid: {l}")

    def update_layout_preview(self):
        """
        Generates a dynamic UI representation of the t_layout text using GtkFrames and attaches it to the given widget (bx_layoutPreview).
        - Parses t_layout to determine structure (left/right pages, horizontal/vertical layout).
        - Uses colors from the TreeView's color column.
        - Automatically resizes to fit available space.
        """
        widget = self.builder.get_object('bx_layoutPreview')
        layout = self.builder.get_object('t_layout').get_text()

        # Step 1: Clear the existing layout preview
        for child in widget.get_children():
            widget.remove(child)

        # Step 2: Validate t_layout
        is_valid, error_message = self.validate_layout(layout, self.liststore)

        if not is_valid:
            # Display a red error frame with an error message
            error_frame = Gtk.Frame(label="Error")
            error_label = Gtk.Label(label=error_message)
            error_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 0, 0, 1))  # Red color
            error_frame.add(error_label)
            widget.add(error_frame)
            widget.show_all()
            return

        # Step 3: Parse t_layout into left and right pages
        if "," in layout:
            left_side, right_side = layout.split(",", 1)
        else:
            left_side, right_side = layout, ""

        # Step 4: Create the horizontal box for the spread (landscape book layout)
        spread_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        spread_box.set_hexpand(True)
        spread_box.set_vexpand(True)

        def create_horizontal_box(codes):
            """
            Creates a horizontal GtkBox containing individual frames for each letter code.
            Each frame's width is proportional to the '% Width' column in the TreeView.

            :param codes: String containing letter codes (e.g., "LRA").
            :return: Gtk.Box containing frames with proportional widths.
            """
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            box.set_hexpand(True)
            box.set_vexpand(True)

            # Retrieve width percentages from the TreeView
            widths = {}
            total_width = 0  # Used for normalization

            for row in self.liststore:
                code = row[m.code]  # Column 0 = Code
                width_percentage = row[m.width]

                if code in codes:
                    widths[code] = width_percentage
                    total_width += width_percentage

            # Normalize widths to prevent errors (Ensure sum = 100%)
            if total_width > 0:
                for code in widths:
                    widths[code] = widths[code] / total_width  # Convert to ratio (0.0 - 1.0)

            # Create Frames with Proportional Widths
            for code in codes:
                frame = Gtk.Frame()
                frame.set_shadow_type(Gtk.ShadowType.IN)

                # Retrieve the background color from the TreeView
                color_hex = "#FFFFFF"  # Default to white
                for row in self.liststore:
                    if row[m.code] == code:  # Match the code in the liststore
                        color_hex = row[m.color]  # Column 6 contains the color
                        break

                # Apply background color
                rgba = Gdk.RGBA()
                rgba.parse(color_hex)
                frame.override_background_color(Gtk.StateFlags.NORMAL, rgba)

                # Centered label inside the frame
                label = Gtk.Label(label=code)
                label.set_hexpand(True)
                label.set_vexpand(True)
                label.set_justify(Gtk.Justification.CENTER)

                frame.add(label)

                # Create an event box to wrap frame & set width proportionally
                event_box = Gtk.EventBox()
                event_box.add(frame)

                if code in widths:
                    width_ratio = widths[code]  # Get proportion (0.0 - 1.0)
                    event_box.set_size_request(int(100 * width_ratio), -1)  # Scale width (135px is arbitrary)

                box.pack_start(event_box, True, True, 0)

            return box

        # Step 5: Helper function to create a page frame
        def create_page_frame(codes, is_right_page, is_single, rtl):
            """
            Creates a page frame with the appropriate orientation and labels.
            - If '/' is present, a vertical split is created.
            - If there is only ONE '/', it creates a 2-section layout where the top contains the first item,
              and the bottom contains the remaining items in a horizontal row.
            :param codes: String of codes for this page.
            :param is_right_page: Boolean indicating if this is the right page.
            :param is_single: Boolean indicating if this is the only page (don't display L/R).
            :param rtl: Boolean indicating if this is an RTL publication (not implemented yet).
            """
            if "/" in codes:
                parts = codes.split("/")  # Split based on `/`
                num_splits = len(parts)  # Count number of groups

                # Create a vertical GtkBox for stacking sections
                page_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
                page_box.set_hexpand(True)
                page_box.set_vexpand(True)

                if num_splits == 2:  # Special handling when only ONE `/`
                    top_section = create_horizontal_box(parts[m.code])  # First part alone
                    bottom_section = create_horizontal_box(parts[m.pg])  # Remaining in a row
                    page_box.pack_start(top_section, True, True, 0)
                    page_box.pack_start(bottom_section, True, True, 0)
                else:
                    # If more than one '/', treat each section as a row
                    for part in parts:
                        section_box = create_horizontal_box(part)  # Each section in a row
                        page_box.pack_start(section_box, True, True, 0)

            else:
                # Default case (horizontal layout with no '/')
                page_box = create_horizontal_box(codes)

            # Create the page frame with 'Left Page' or 'Right Page' labels
            if is_single:
                page_frame = Gtk.Frame(label="")
            else:
                page_frame = Gtk.Frame(label=_("Right Page (2)") if is_right_page else _("Left Page (1)"))
            page_frame.set_label_align(0.5, 0.5)  # Center horizontally & vertically
            page_frame.set_shadow_type(Gtk.ShadowType.NONE)
            page_frame.set_size_request(50, -1)  # Width = 70px, Height flexible
            page_frame.set_hexpand(True)
            page_frame.set_vexpand(True)
            page_frame.add(page_box)

            return page_frame

        # Step 6: Generate left and right page layouts
        left_page = create_page_frame(left_side, is_right_page=False, is_single=right_side == "", rtl=False)
        right_page = create_page_frame(right_side, is_right_page=True, is_single=False, rtl=False) if right_side else None

        # Step 7: Pack into the spread box
        spread_box.pack_start(left_page, True, True, 0)
        if right_page:
            spread_box.pack_start(right_page, True, True, 0)

        # Step 8: Attach to the provided widget and show
        widget.add(spread_box)
        widget.show_all()
