import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import json
from ptxprint.utils import _

class PolyglotSetup(Gtk.Box):
    def __init__(self, treeview):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # Load data from JSON file #FixMe!
        try:
            with open('data.json', 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

        # Dropdown options
        self.codes = ["L", "R", "A", "B", "C", "D", "E", "F", "G"]
        # Need to connect this to the liststore for fcb_projects!
        self.prjs = ["(None)", "BSB", "WSG", "WSGdev", "GRKNT", "WSGgong", "WSGlatin", "WSGBTpub"]
        self.spread_side = ["1", "2"]

        # Use the existing treeview instead of creating a new one
        self.treeview = treeview  
        self.treeview.set_reorderable(True)

        # Create ListStore model if not already set
        if self.treeview.get_model() is None:
            self.liststore = Gtk.ListStore(str, str, str, str, bool, float, str, str, str, int)  
            self.treeview.set_model(self.liststore)
        else:
            self.liststore = self.treeview.get_model()

        for item in self.data:
            code = list(item.keys())[0]
            values = item[code]
            self.liststore.append([
                code, values.get("spread_side", "1"), values['prj'], values['cfg'],
                values['captions'], values.get("percentage", 50.0), values.get('color', "#FFFFFF"),
                "Right-Click for options", "#000000", 400
            ])

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

        self.validate_page_widths() # Make sure % Width gets colored red if invalid (even on loading)

        # Add TreeView to Layout
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        scrolled_window.add(self.treeview)

        self.pack_start(scrolled_window, True, True, 0)

    def get_treeview(self):
        """ Expose the TreeView for integration with other modules. """
        return self.treeview        
        
    def add_column(self, title, column_id, editable=False, renderer_type="text", options=None, align="left"):
        """Adds a column with the specified properties."""
        if renderer_type == "text":
            renderer = Gtk.CellRendererText()
            renderer.set_property("editable", editable)
            
            # Only apply color formatting to the % Width column
            if column_id == 5:
                column = Gtk.TreeViewColumn(title, renderer, text=column_id)
                column.add_attribute(renderer, "foreground", 8)  # Use column 8 for text color
                column.add_attribute(renderer, "weight", 9)      # Use column 9 for bold effect
            else:
                column = Gtk.TreeViewColumn(title, renderer, text=column_id)

            # Store tooltips inside the last column (index 7)
            if column_id in range(0,7):
                self.treeview.set_has_tooltip(True)  # Enable tooltips
                self.treeview.connect("query-tooltip", self.on_query_tooltip)  # Connect event

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
            column.set_alignment(0.5)
            column.set_resizable(True)
            column.set_expand(True)

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

            # Special handling for 'Config' column (column 3)
            if column_id == 3:  # Special handling for 'Config' column
                renderer = Gtk.CellRendererCombo()
                renderer.set_property("editable", True)
                renderer.set_property("text-column", 0)
                renderer.set_property("has-entry", False)
                renderer.connect("edited", self.on_combo_changed, column_id)

                column = Gtk.TreeViewColumn(title, renderer, text=column_id)
                column.set_cell_data_func(renderer, self.config_cell_data_func)  # Dynamic per-row options
                # column.set_cell_data_func(renderer, disable_edit_for_first_row)  # Lock Row 0
                column.set_resizable(True)
                column.set_expand(True)

                self.treeview.append_column(column)
                return

            # Apply model for other columns (including Project - column 2)
            renderer.set_property("model", self.get_combo_model(options))
            if align == "center":
                renderer.set_property("xalign", 0.5)

            # Create column (avoiding duplicates)
            existing_columns = [col.get_title() for col in self.treeview.get_columns()]
            if title not in existing_columns:  # Prevent duplicate columns
                column = Gtk.TreeViewColumn(title, renderer, text=column_id)
                column.set_cell_data_func(renderer, disable_edit_for_first_row)  # Apply locking
                self.treeview.append_column(column)

        elif renderer_type == "color":
            renderer = Gtk.CellRendererText()
            renderer.set_property("editable", True)
            renderer.set_property("background-set", True)
            column = Gtk.TreeViewColumn(title, renderer, text=column_id, background=column_id)
            column.add_attribute(renderer, "foreground", column_id)  # Set the text color to match the background
            column.set_resizable(True)
            column.set_expand(True)
            renderer.connect("edited", self.on_color_typed, column_id)
            self.treeview.append_column(column)
            self.treeview.connect("row-activated", self.on_color_clicked, column_id)
            return
        
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
                6: _("[Optional] Type #color code, or right-click to change background color for this text.")
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
        """Handles changes in combo box selections, preventing duplicate Code or Project+Config combinations. Prevents edits in row 0 for certain fields."""
        if path == "0" and column_id in [0, 2, 3]:  # Row 0 should not be editable for these columns
            print(f"Editing not allowed for Row 0 in column {column_id}.")
            return
        
        if column_id == 0:  # Code column
            if text in {row[0] for row in self.liststore if row[0]}:
                print(f"Duplicate Code not allowed: {text}")
                return  # Prevent duplicate
            
        if column_id == 2:  # Project column changed
            available_configs = self.get_available_configs(text)  # Get new configs for the selected project
            self.liststore[path][3] = available_configs[0]  # Set first available config for this row
            self.treeview.queue_draw()  # Refresh UI

        if column_id == 2 or column_id == 3:  # Project or Configuration columns
            prj = self.liststore[path][2]
            cfg = self.liststore[path][3]
            
            if column_id == 2:
                prj = text  # If changing project
            else:
                cfg = text  # If changing configuration
            
            for row in self.liststore:
                if row[2] == prj and row[3] == cfg and self.liststore[path][0] != row[0]:
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
        if event.button == 3:  # Right-click
            self.context_menu = Gtk.Menu()  # Store reference

            add_item = Gtk.MenuItem(label=_("Add a row/text"))
            add_item.connect("activate", self.add_row)
            self.context_menu.append(add_item)

            move_up_item = Gtk.MenuItem(label=_("Move Up"))
            move_up_item.connect("activate", self.move_selected_row, -1)
            self.context_menu.append(move_up_item)

            move_down_item = Gtk.MenuItem(label=_("Move Down"))
            move_down_item.connect("activate", self.move_selected_row, 1)
            self.context_menu.append(move_down_item)

            distribute_item = Gtk.MenuItem(label=_("Distribute Widths"))
            distribute_item.connect("activate", self.distribute_width_evenly)
            self.context_menu.append(distribute_item)

            delete_item = Gtk.MenuItem(label=_("Delete Row"))
            delete_item.connect("activate", self.delete_selected_row)
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
            next_code = str(available_codes[0]) if available_codes else ""  # Auto-assign next available code

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

    def distribute_width_evenly(self, widget):
        """Evenly distributes the % Width across all rows sharing the same page (1 or 2)."""
        selected = self.get_selected_row()
        if not selected:
            return  # No row selected

        model, iter, path = selected
        page = model[path][1]  # Column index 1 stores "1" or "2"

        # Find all rows that share the same page (1 or 2)
        same_page_rows = [row for row in range(len(model)) if model[row][1] == page]
        row_count = len(same_page_rows)

        if row_count == 0:
            return  # Avoid division by zero

        new_width = round(100.0 / row_count, 2)  # Calculate even width per row

        # Apply the new width to each row
        for row in same_page_rows:
            model[row][5] = new_width  # Column index 5 is % Width

        self.save_data()
        self.validate_page_widths()  # Refresh highlighting

    def validate_page_widths(self):
        """Checks that the total width per page (1|2) is 100% and highlights invalid rows."""
        page_totals = {"1": 0.0, "2": 0.0}  # Track total % width per page

        # Step 1: Calculate total widths for each page (1 or 2)
        for row in range(len(self.liststore)):
            page = self.liststore[row][1]  # Column index 1 stores "1" or "2"
            width = self.liststore[row][5]  # Column index 5 stores % Width
            page_totals[page] += width  # Accumulate width for each page

        # Step 2: Apply formatting to **every row** that shares the same `1|2` page value
        for row in range(len(self.liststore)):
            page = self.liststore[row][1]  # "1" or "2"
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
        data = [{row[0]: {"spread_side": row[1], "prj": row[2], "cfg": row[3], "captions": row[4], "percentage": row[5], "color": row[6]}} for row in self.liststore]
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)
