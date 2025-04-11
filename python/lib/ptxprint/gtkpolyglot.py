import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import re, json
from enum import IntEnum
from ptxprint.utils import _
from ptxprint.polyglot import PolyglotConfig
from ptxprint.pastelcolorpicker import ColorPickerDialog

_modeltypes = (str, str, str, str, bool, float, float, float, float, str, str, str, str, int)
_modelfields = ('code', 'pg', 'prj', 'cfg', 'captions', 'fontsize', 'baseline', 'fraction', 'weight', 'color', 'prjguid', 'tooltip', 'widcol', 'bold')
m = IntEnum('m', [(x, i) for i, x in enumerate(_modelfields)])

class PolyglotSetup(Gtk.Box):
    def __init__(self, builder, view, tv):
        print(f"__init__")
        self.builder = builder
        self.view = view
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.treeview = tv  
        self.treeview.set_reorderable(False)

        # Create ListStore model if not already set
        if self.treeview.get_model() is None:
            self.ls_treeview = Gtk.ListStore(*_modeltypes)
            self.treeview.set_model(self.ls_treeview)
        else:
            self.ls_treeview = self.treeview.get_model()
            
        self.ls_config = []  # List to store separate cfg listStores for each row

        # combo dropdown options (cfg gets filled in dynamincally)
        self.codes = ["L", "R", "A", "B", "C", "D", "E", "F", "G"]
        self.spread_side = ["1", "2"]
        self.project_liststore = self.builder.get_object("ls_projects")

        # Define Columns
        self.add_column("Code", m.code, editable=True, renderer_type="combo", options=self.codes, align="center", width=40)
        self.add_column("1|2", m.pg, editable=True, renderer_type="combo", options=self.spread_side, align="center", width=40)
        self.add_column("Project", m.prj, editable=True, renderer_type="combo", options=self.project_liststore, width=80)
        self.add_column("Configuration", m.cfg, editable=True, renderer_type="combo", options=[''], width=110)
        self.add_column("Captions", m.captions, editable=True, renderer_type="toggle", align="center", width=50)
        self.add_column("Font Size", m.fontsize, editable=True, renderer_type="text", align="right", width=60)
        self.add_column("Spacing", m.baseline, editable=True, renderer_type="text", align="right", width=60)
        self.add_column("% Width", m.fraction, editable=True, renderer_type="text", align="right", width=60)
        self.add_column("Weight", m.weight, editable=True, renderer_type="text", align="right", width=60)

        self.treeview.connect("button-press-event", self.on_right_click)

        # Connect tooltips
        for col_id in range(0, m.tooltip):
            self.treeview.set_has_tooltip(True)  # Enable tooltips
            self.treeview.connect("query-tooltip", self.on_query_tooltip)  # Connect event
        self.validate_page_widths() # Make sure % Width gets colored red if invalid (even on loading)

        # Add TreeView to Layout
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        scrolled_window.add(self.treeview)

        self.pack_start(scrolled_window, True, True, 0)

    def clear_polyglot_treeview(self):
        if not self.ls_treeview:
            return            
        self.ls_treeview.clear()
        self.update_layout_string()
        self.refresh_code_dropdowns()
        self.update_context_menu()
                
    def load_polyglots_into_treeview(self):
        row_index = self.find_or_create_row("L")
        row_index = self.find_or_create_row("R")
        for sfx in self.codes:
            if sfx not in self.view.polyglots:  # Only process existing polyglots
                continue
            plyglot = self.view.polyglots[sfx]
            row_index = self.find_or_create_row(sfx)  # Find or add row
            prjguid, available_configs = self.get_available_configs(getattr(plyglot, 'prj'))
            plyglot.prjguid = prjguid
            self.ls_config[row_index].clear()
            for c in available_configs:
                self.ls_config[row_index].append([c])                
            for idx, field in enumerate(_modelfields[1:11], start=1):
                val = getattr(plyglot, field)
                self.ls_treeview[row_index][idx] = val
            if sfx == "L":
                self.updateRow(row_index)
            # polyview = self.view
            # else:
                # polyview = self.view.createDiglotView(suffix=sfx)
            # if polyview is not None:
                # self.ls_treeview[row_index][m.fontsize] = float(polyview.get("s_fontsize", 11.11))
                # self.ls_treeview[row_index][m.baseline] = float(polyview.get("s_linespacing", 15.15))
        self.update_layout_string()

    def find_or_create_row(self, sfx, save=False):
        if len(self.ls_treeview) >= 9:
            self.view.doStatus("Maximum of 9 rows reached. Cannot add more.")
            return -1  # Indicate failure to add a row

        # Check if row already exists
        for i, row in enumerate(self.ls_treeview):
            if row[m.code] == sfx:
                return i  # Return existing row index

        # First row logic: Locked with primary project settings # FixMe!
        if len(self.ls_treeview) == 0 and sfx == "L":
            pri_prj, pri_prjguid = self.get_curr_proj()
            cfid = self.view.cfgid
        else:
            pri_prj = "(Select)"
            pri_prjguid = ""
            cfid = ""
        pg = "1" if sfx in ("LR") else "2"
        new_row = [sfx, pg, pri_prj, cfid, False, 11.0, 14.0, 55.0, 45.0, 
                   "#fefefe", pri_prjguid, "Tooltips", "#000000", 400]
        print(f"{new_row=}")
        self.ls_treeview.append(new_row)
        row_index = len(self.ls_treeview) - 1  
        if save and cfid != "":
            self.updateRow(row_index)
        return row_index  # Return the new row index
        
    def get_suffix_from_row(self, row_index):
        res = getattr(self.ls_treeview[row_index], m.code, None)
        return res
        
    def get_view(self, sfx):
        if sfx == "L":
            return self.view
        view = self.view.diglotViews.get(sfx, None)
        if view is None:
            view = self.view.createDiglotView(sfx)
        return view

    def add_column(self, title, col_id, editable=False, renderer_type="text", options=None, align="left", width=70):
        if renderer_type == "combo":
            # Create a CellRendererCombo
            renderer = Gtk.CellRendererCombo()
            renderer.set_property("editable", True)
            renderer.set_property("text-column", 0)
            renderer.set_property("has-entry", False)
            column = Gtk.TreeViewColumn(title, renderer, text=col_id)
            
            # Special handling for 'Code' column (column 0)
            if col_id == m.code:
                self.code_renderer = renderer  # Store renderer reference
                availCodes = self.get_available_codes()  # Get only available codes
                renderer.set_property("model", self.set_combo_options(availCodes))
                renderer.set_property("background-set", True)
                column = Gtk.TreeViewColumn(title, renderer, text=col_id, background=m.color)

            # Special handling for 'Config' column (column 3) a set of liststores - one per row
            if col_id == m.cfg:  # Special handling for "Configuration" column
                self.ls_config = [Gtk.ListStore(str) for _ in range(9)] # len(self.liststore) # Create a ListStore per row

                # Assign the correct ListStore to each row dynamically
                def set_config_model(column, cell, model, iter, data):
                    row_index = model.get_path(iter).get_indices()[0]      # Get row index
                    cell.set_property("model", self.ls_config[row_index])  # Set per-row ListStore

                column.set_cell_data_func(renderer, set_config_model)      # Attach function to dynamically assign models

            renderer.connect("edited", self.on_combo_changed, col_id)

            if isinstance(options, Gtk.ListStore):  # If options is a ListStore, use it directly
                renderer.set_property("model", options)
            else:  # Otherwise, assume it's a list and convert it
                renderer.set_property("model", self.set_combo_options(options))

            # Connect the signal to apply wrap-width dynamically
            if col_id == m.prj:
                renderer.connect("editing-started", self.on_editing_started)
            if align == "center":
                renderer.set_property("xalign", 0.5)

        elif renderer_type == "toggle":
            renderer = Gtk.CellRendererToggle()
            renderer.set_property("activatable", True)
            renderer.connect("toggled", self.on_toggle, col_id)
            column = Gtk.TreeViewColumn(title, renderer, active=col_id)  # Bind "active" property

        elif renderer_type == "text":
            renderer = Gtk.CellRendererText()
            renderer.set_property("editable", editable)
            column = Gtk.TreeViewColumn(title, renderer, text=col_id)
            
            # Only apply text color formatting to the % Width column
            if col_id == m.fraction:
                column.add_attribute(renderer, "foreground", m.widcol)  # text color
                column.add_attribute(renderer, "weight", m.bold)        # bold effect

            # Apply formatting function *only* to the % Width column (index 5)
            if col_id in [m.fontsize, m.baseline, m.fraction, m.weight]:
                column.set_cell_data_func(renderer, self.format_float_data_func, col_id)
                renderer.connect("edited", self.on_text_edited, col_id)  # Connect edit event
            
        # Common to all renderer_types:
        if align == 'right':
            column.set_alignment(1.0)
        elif align == 'center':
            column.set_alignment(0.5)
        else:
            column.set_alignment(0.0)
        column.set_fixed_width(width)
        column.set_resizable(True)
        if col_id not in [m.code, m.pg, m.prj]: # these are fixed-width, the rest should grow
            column.set_expand(True)
            
        # Create column (avoiding creation of duplicate columns)
        existing_columns = [col.get_title() for col in self.treeview.get_columns()]
        if title not in existing_columns:  # Prevent duplicate columns
            self.treeview.append_column(column)

    def get_available_configs(self, project):
        impprj = self.view.prjTree.findProject(project)
        if impprj is None:
            return None, []
        prjguid = impprj.guid
        prjobj = self.view.prjTree.getProject(prjguid)
        cfgList = list(prjobj.configs.keys())
        # print(f"get_available_configs: {project}:{prjguid} {cfgList}")
        if not len(cfgList):
            cfgList = ['Default']
        return prjguid, cfgList
        
    def on_editing_started(self, cell, editable, path):
        if isinstance(editable, Gtk.ComboBox):
            # Dynamically set wrap width based on the number of items
            num_projects = len(self.project_liststore) if hasattr(self, "project_liststore") else 0
            number_of_columns = max(1, num_projects // 16) + 1 if num_projects > 14 else 1
            editable.set_wrap_width(number_of_columns)

    def on_query_tooltip(self, widget, x, y, keyboard_mode, tooltip):
        path_info = self.treeview.get_path_at_pos(x, y)

        if path_info is not None:
            path, column, y, z = path_info

            # Find the correct column index
            col_id = self.treeview.get_columns().index(column)

            # Set tooltip text based on the column
            tooltips = {
                m.code:     _("Unique identifier for the text/glot (L, R, A, B, C, ... G)\nRight-click to change background color."),
                m.pg:       _("Specify whether the should be on the left (1) or right (2) page."),
                m.prj:      _("The (Paratext) project code."),
                m.cfg:      _("The configuration settings to be applied for the selected project."),
                m.captions: _("Whether to show captions for this text."),
                m.fontsize: _("The font size for this text."),
                m.baseline: _("The line spacing (baseline) for this text."),
                m.fraction:    _("The page width (as %) that this text should occupy.\nIf the values are red, this indicates that the total doesn't\nadd to 100%, so adjust the values.\nUse right-click menu option to distribute width evenly between columns."),
                m.weight:   _("The relative weight (as %) of this text when merging with other texts."),
            }

            # Apply the correct tooltip based on column
            if col_id in tooltips:
                tooltip.set_text(tooltips[col_id])
                return True  # Tooltip set successfully

        return False  # No tooltip found

    def on_text_edited(self, widget, path, new_text, col_id):
        print(f"on_text_edited: {path=} {new_text=} {col_id=}")
        try:
            new_value = float(new_text)      # Convert input to float
        except ValueError:
            self.view.doStatus(f"Invalid input: {new_text}")  # Handle non-numeric input gracefully
            return
        new_value = round(new_value, 2)  # Keep 2 decimal places
        # Update the ListStore
        self.ls_treeview[path][col_id] = new_value
        if col_id == m.fraction:
            self.validate_page_widths() # Validate total widths after any edit
        row_index = int(path)
        self.updateRow(row_index)
        sfx = self.ls_treeview[row_index][m.code]
        if col_id == m.fontsize or col_id == m.baseline:
            aview = self.get_view(sfx)
            if aview is not None:
                aview.set("s_fontsize" if col_id == m.fontsize else "s_linespacing", new_value)
                aview.changed()
        self.update_layout_string()

    def format_float_data_func(self, column, cell, model, iter, col_id):  # Added `data=None`
        value = model.get_value(iter, col_id)

        # Ensure the value is a float before formatting
        if isinstance(value, (int, float)):
            formatted_value = f"{value:.2f}"  # Format to 2 decimal places
            cell.set_property("text", formatted_value)
            cell.set_property("xalign", 1.0)  # 1.0 = Right, 0.5 = Center, 0.0 = Left
        else:
            cell.set_property("text", "")

    def get_available_codes(self, exclude_path=None):
        print(f"get_available_codes: {exclude_path=}")
        used_codes = {row[m.code] for row in self.ls_treeview if row[m.code]}  # Set of used codes

        if exclude_path is not None:
            current_code = self.ls_treeview[exclude_path][m.code]
            used_codes.discard(current_code)

        available_codes = [code for code in self.codes if code not in used_codes]
        return available_codes

    def set_combo_options(self, options):
        print(f"set_combo_options: {options}")
        model = Gtk.ListStore(str)
        if options is not None:
            for option in options:
                model.append([option])
        return model
        
    def on_combo_changed(self, widget, path, text, col_id):
        print(f"on_combo_changed: {path=} {text=} {col_id=}")
        row_index = int(path)
        old_cfg = self.ls_treeview[row_index][m.cfg] if 0 <= row_index < len(self.ls_treeview) else None
        if row_index == 0 and col_id not in [m.pg, m.fraction]:  # Row 0 should not be editable for these columns
            self.view.doStatus(_("Cannot edit that value for 'L' row"))
            return
        
        if col_id == m.code:  # Code changed
            if text in {row[m.code] for row in self.ls_treeview if row[m.code]}:
                self.view.doStatus(_("Duplicate Code not allowed"))
                return

        prjguid = None
        if col_id == m.prj:  # Project column changed
            prjguid, available_configs = self.get_available_configs(text)
            prj = text
            self.ls_treeview[row_index][m.prjguid] = prjguid

            # Update the ListStore for this specific row
            if row_index < len(self.ls_config):  # Ensure row is valid
                lsc = self.ls_config[row_index]
                lsc.clear()
                if available_configs:
                    for c in available_configs:
                        lsc.append([c])   
                    # Determine the new config to select
                    new_cfg = old_cfg if old_cfg in available_configs else available_configs[0]
                    tree_iter = self.ls_config[row_index].get_iter_first()
                    if tree_iter:
                        self.ls_config[row_index].set_value(tree_iter, 0, new_cfg)                
                # Set the selected config
            self.ls_treeview[row_index][m.cfg] = new_cfg
            self.treeview.queue_draw()  # Refresh UI
        else:
            prj = self.ls_treeview[row_index][m.prj]
            prjguid = self.ls_treeview[row_index][m.prjguid]

        if col_id == m.cfg:
            prj, cfg = self.get_prj_cfg()
        else:
            cfg = self.ls_treeview[row_index][m.cfg]

        if col_id == m.prj or col_id == m.cfg:  
            # Check for duplicated Project and Configuration names
            for i, row in enumerate(self.ls_treeview):
                if i != row_index and row[m.prj] == prj and row[m.cfg] == cfg:
                    self.view.doStatus(_("Duplicate Project+Configuration not allowed)"))
                    return

            sfx = self.ls_treeview[row_index][m.code]
            polyglot = self.view.polyglots.get(sfx, None)
            if polyglot is not None:
                polyglot.prj = prj
                polyglot.cfg = cfg
            polyview = self.get_view(sfx)
            if polyview is not None:
                polyview.updateProjectSettings(prj, prjguid, configName=cfg)
        else:
            polyview = None

        self.ls_treeview[path][col_id] = text

        print(f"About to updateRow: {row_index} {text}")
        self.updateRow(row_index)
        if polyview is not None:
            f = polyview.get('s_fontsize', 11.0)
            b = polyview.get('s_linespacing', 15.0)
            c = polyview.get('col_dibackcol', "#FFFFFF")
            self.ls_treeview[row_index][m.fontsize] = float(f)
            self.ls_treeview[row_index][m.baseline] = float(b)
            self.ls_treeview[row_index][m.color] = c
           
        # Refresh dropdowns and other dependencies after updating the combo box
        if col_id == m.code:    # Unique code changed
            self.refresh_code_dropdowns()
        elif col_id == m.pg:  # Page 1 or 2 changed
            self.validate_page_widths()
            self.treeview.queue_draw()  # Refresh UI

    def updateRow(self, row_index):
        print(f"updateRow: {row_index}")
        sfx = self.ls_treeview[row_index][m.code]
        plyglt = self.view.polyglots.get(sfx, None)
        if plyglt is None:
            plyglt = PolyglotConfig()
            self.view.polyglots[sfx] = plyglt
        for idx, field in enumerate(_modelfields[1:11], start=1):
            val = self.ls_treeview[row_index][idx]
            setattr(plyglt, field, val)
        if row_index == 0:
            for a, b in {"fontsize": "s_fontsize", "baseline" : "s_linespacing", "color": "col_dibackcol"}.items():
                self.view.set(b, self.ls_treeview[row_index][getattr(m, a)])
        
    def refresh_code_dropdowns(self):
        print(f"refresh_code_dropdowns")
        if hasattr(self, "code_renderer"):  # Ensure renderer exists before updating
            available_codes = self.get_available_codes()
            self.code_renderer.set_property("model", self.set_combo_options(available_codes))

    def set_color_from_menu(self, widget):
        selected = self.get_selected_row()
        if selected:
            model, iter, path = selected
            self.on_color_clicked(None, path, model[path][m.color])

    def on_color_clicked(self, widget, path, text):
        model = self.ls_treeview
        iter = model.get_iter(path)
        # Find the top-level window (main parent)
        parent_window = self.get_toplevel() if hasattr(self, "get_toplevel") else None
        
        # Set the current color (to highlight it in the dialog)
        current_color = model[path][m.color]  # Hex color format
        dialog = ColorPickerDialog(parent=parent_window, current_color=current_color)

        if dialog.run() == Gtk.ResponseType.OK:
            color_hex = dialog.selected_color  # Get the selected color
            
            # Handle case where custom color returns "rgb(r,g,b)" format
            if color_hex.startswith("rgb("):
                # Extract RGB values and convert to hex
                rgb = color_hex[4:-1].split(",")
                r, g, b = map(int, rgb)
                color_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
            
            # Update the model with the selected hex color
            model.set_value(iter, m.color, color_hex)
            row_index = int(path[0])
            self.updateRow(row_index)
            self.update_layout_string()

        dialog.destroy()

    def on_toggle(self, widget, path, col_id):
        model = self.ls_treeview
        iter = model.get_iter(path)  # Get the iterator for the row
        current_value = model.get_value(iter, col_id)  # Read current state
        model.set_value(iter, col_id, not current_value)  # Toggle it
        row_index = int(path)
        self.updateRow(row_index)
        self.update_layout_string()
        
    def get_selected_row(self):
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            return model, iter, model.get_path(iter)
        return None

    def on_right_click(self, widget, event):
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

            homogenize_fontsize_item = Gtk.MenuItem(label=_("Copy Font Size to All"))
            homogenize_fontsize_item.connect("activate", self.homogenize_fontsize)
            self.context_menu.append(homogenize_fontsize_item)

            homogenize_spacing_item = Gtk.MenuItem(label=_("Copy Spacing to All"))
            homogenize_spacing_item.connect("activate", self.homogenize_spacing)
            self.context_menu.append(homogenize_spacing_item)

            distribute_item = Gtk.MenuItem(label=_("Distribute Widths"))
            distribute_item.connect("activate", self.distribute_width_evenly)
            self.context_menu.append(distribute_item)

            delete_item = Gtk.MenuItem(label=_("Delete Row"))
            delete_item.connect("activate", self.delete_selected_row)
            delete_item.set_sensitive(not is_first_row)  # Disable if Row 0
            self.context_menu.append(delete_item)

            change_cfg_settings = Gtk.MenuItem(label=_("Edit Settings..."))
            change_cfg_settings.connect("activate", self.edit_other_config)
            change_cfg_settings.set_sensitive(not is_first_row)  # Disable if Row 0
            self.context_menu.append(change_cfg_settings)

            color_item = Gtk.MenuItem(label=_("Set Color..."))
            color_item.connect("activate", self.set_color_from_menu)
            self.context_menu.append(color_item)

            self.context_menu.show_all()
            self.update_context_menu()  # Apply correct state
            self.context_menu.popup_at_pointer(event)

    def delete_selected_row(self, widget):
        selected = self.get_selected_row()
        if selected:
            model, iter, path = selected
            row_index = int(path[0])
            sfx = self.ls_treeview[row_index][m.code]
            self.view.diglotViews.pop(sfx, None)
            self.view.polyglots.pop(sfx, None)
            model.remove(iter)
            self.update_layout_string()
            self.refresh_code_dropdowns()  # Refresh available codes
            self.update_context_menu()     # Refresh menu state
            self.validate_page_widths()    # Refresh color of % width

    def update_context_menu(self):
        if not len(self.ls_treeview):
            return
        max_rows = 9
        has_room = len(self.ls_treeview) < max_rows

        for item in self.context_menu.get_children():
            if isinstance(item, Gtk.MenuItem) and item.get_label() == "Add a row/text":
                item.set_sensitive(has_room)  # Enable/disable based on row count

    def get_prj_cfg(self):
        print(f"get_prj_cfg")
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            prj = model.get_value(iter, m.prj)
            cfg = model.get_value(iter, m.cfg)
            print(f"  {prj=} {cfg=}")
            return prj, cfg
        else:
            print(f"  Returned None, None")
            return None, None
        
    def edit_other_config(self, menu_item):
        print(f"edit_other_config")
        prj, cfg = self.get_prj_cfg()
        if prj is not None and cfg is not None:
            self.view.doStatus(_("Opening {}:{} ...").format(prj, cfg))

    def get_curr_proj(self):
        print(f"get_curr_proj")
        w = self.builder.get_object('fcb_project')
        m = w.get_model() # liststore
        aid = w.get_active_iter()
        prjid = m.get_value(aid, 0)
        prjguid = m.get_value(aid, 1)
        print(f"  {prjid=}  {prjguid=}")
        return prjid, prjguid

    def add_row(self, widget):
        print(f"add_row")
        if len(self.ls_treeview) >= 9:
            self.view.doStatus("Maximum of 9 rows reached. Cannot add more.")
            return  # Stop if the limit is reached
        available_codes = self.get_available_codes()
        next_code = str(available_codes[m.code]) if available_codes else ""  # Auto-assign next available code
        self.find_or_create_row(next_code, save=True)
        # Perform additional updates
        self.update_layout_string()
        self.refresh_code_dropdowns()
        self.validate_page_widths()
        self.update_context_menu()
        
    def move_selected_row(self, widget, direction):
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

                self.update_layout_string()

    # This is only needed for auto-adjusting a Diglot [not for polyglot] (and the L-fraction gets returned)
    def set_fraction(self, f):
        self.ls_treeview[0][m.fraction] = f * 100
        self.ls_treeview[1][m.fraction] = (1 - f) * 100
        self.view.set("polyfraction_", f * 100)
        self.view.diglotViews["R"].set("polyfraction_", (1 - f) * 100)
        self.updateRow(0)
        self.updateRow(1)

    def get_fraction(self):
        w = self.ls_treeview[0][m.fraction] / 100
        return w

    def homogenize_fontsize(self, widget):
        print(f"homogenize_fontsize")
        selected = self.get_selected_row()
        if not selected:
            print(f"  !returning prematurely")
            return  # No row selected

        model, iter, path = selected
        new_size = model[path][m.fontsize]

        # Apply the new size to each row
        for row in range(len(model)):
            model[row][m.fontsize] = new_size
            self.updateRow(row)

    def homogenize_spacing(self, widget):
        print(f"homogenize_spacing")
        selected = self.get_selected_row()
        if not selected:
            print(f"  !returning prematurely")
            return  # No row selected

        model, iter, path = selected
        new_spacing = model[path][m.baseline]

        # Apply the new size to each row
        for row in range(len(model)):
            model[row][m.baseline] = new_spacing
            self.updateRow(row)

    def distribute_width_evenly(self, widget):
        print(f"distribute_width_evenly")
        selected = self.get_selected_row()
        if not selected:
            print(f"  !returning prematurely")
            return  # No row selected

        model, iter, path = selected
        page = model[path][m.pg]

        # Find all rows that share the same page (1 or 2)
        same_page_rows = [row for row in range(len(model)) if model[row][m.pg] == page]
        row_count = len(same_page_rows)

        if row_count == 0:
            print(f"  !returning prematurely: row_count==0")
            return  # Avoid division by zero

        new_width = round(100.0 / row_count, 2)  # Calculate even width per row

        # Apply the new width to each row
        for row in same_page_rows:
            model[row][m.fraction] = new_width
            self.updateRow(row)

        self.update_layout_string()
        self.validate_page_widths()  # Refresh highlighting

    def validate_page_widths(self):
        print(f"validate_page_widths")
        page_totals = {"1": 0.0, "2": 0.0}  # Track total % width per page

        # Step 1: Calculate total widths for each page (1 or 2)
        for row in range(len(self.ls_treeview)):
            page = self.ls_treeview[row][m.pg]
            width = self.ls_treeview[row][m.fraction]
            if page is not None:
                page_totals[page] += width  # Accumulate width for each page

        # Step 2: Apply formatting to **every row** that shares the same `1|2` page value
        for row in range(len(self.ls_treeview)):
            page = self.ls_treeview[row][m.pg]
            total = page_totals[page]  # Get total width for this page
            is_invalid = abs(total - 100.0) > 0.02  # Allow small floating-point errors

            text_color = "#FF0000" if is_invalid else "#000000"  # Red if invalid, black if valid
            font_weight = 700 if is_invalid else 400  # Bold if invalid, normal if valid

            self.ls_treeview[row][m.widcol] = text_color   # Update text color
            self.ls_treeview[row][m.bold]   = font_weight  # Update font weight

        self.treeview.queue_draw()  # Refresh UI

    def update_layout_string(self):
        print(f"update_layout_string")
        t = self.generate_layout_from_treeview()
        self.view.set('t_layout', t)
        self.update_layout_preview()

    def generate_layout_from_treeview(self):
        # Step 1: Extract used codes and their '1|2' values from the ListStore
        codes_by_side = {"1": [], "2": []}  # Store codes grouped by page side
        for row in self.ls_treeview:
            code, side = row[m.code], row[m.pg]
            if code and side:
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
        # Rule 2: Ensure there are no spaces
        if " " in t_layout:
            return False, _("Spaces not allowed")

        # Extract used codes and their '1|2' values from the ListStore
        used_codes = {}  # Dictionary mapping codes -> '1' or '2'
        for row in liststore:
            code, side = row[m.code], row[m.pg]
            if code:
                used_codes[code] = side

        all_used_codes = set(used_codes.keys())  # Set of valid codes from TreeView
        all_layout_codes = set(re.findall(r"[A-Z]", t_layout))  # Extract all letter codes from layout
        all_letters = set("".join(t_layout.replace(",", "").replace("/", "")))

        # Rule 3: If both '1' and '2' exist in the ListStore, a comma must be present
        if "1" in used_codes.values() and "2" in used_codes.values() and "," not in t_layout:
            return False, "Comma required for\nmulti-page spread"

        # Rule 4: Ensure left-side codes appear in '1' and right-side codes in '2'
        if "," in t_layout:
            left_side, right_side = t_layout.split(",", 1)
            left_codes = set(left_side.replace("/", ""))
            right_codes = set(right_side.replace("/", ""))
            if not left_codes.issubset({k for k, v in used_codes.items() if v == "1"}):
                return False, _("Codes on left must {}be assigned to page '1'").format('\n')
            if not right_codes.issubset({k for k, v in used_codes.items() if v == "2"}):
                return False, _("Codes on right must {}be assigned to page '2'").format('\n')

        # Rule 5: Ensure '/' is used correctly (not at start or end, no consecutive slashes)
        if t_layout.startswith("/") or t_layout.endswith("/") or "//" in t_layout:
            return False, _("Invalid position for slash")
            
        # Rule 6: Ensure L and R are always present
        if not ("L" in all_letters and "R" in all_letters):
            return False, _("L or R missing")

        # Rule 7 (NEW): Ensure all codes in the TreeView are included in t_layout
        missing_codes = all_used_codes - all_layout_codes
        if missing_codes:
            return False, _("Missing: {}").format(','.join(missing_codes))
            
        # Rule 10: Hyphen '-' is allowed to indicate a blank page
        valid_chars = set(used_codes.keys()).union({",", "/", "-"})
        if not set(t_layout).issubset(valid_chars):
            return False, _("Invalid characters")

        # Rule 1: Ensure all letters in t_layout exist in the used_codes
        if not all_letters.issubset(set(used_codes.keys())):
            return False, _("Invalid codes used")

        return True, _("Valid layout")

    def update_layout_preview(self):
        widget = self.builder.get_object('bx_layoutPreview')
        layout = self.builder.get_object('t_layout').get_text()

        # Step 1: Clear the existing layout preview
        for child in widget.get_children():
            widget.remove(child)

        # Step 2: Validate t_layout
        is_valid, error_message = self.validate_layout(layout, self.ls_treeview)

        if not is_valid:
            # Display a red error frame with an error message
            error_frame = Gtk.Frame(label=_("Layout Error"))
            error_frame.set_label_align(0.5, 0.5)  # Center horizontally & vertically
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
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            box.set_hexpand(True)
            box.set_vexpand(True)

            # Retrieve width percentages from the TreeView
            widths = {}
            total_width = 0  # Used for normalization

            for row in self.ls_treeview:
                code = row[m.code]  # Column 0 = Code
                width_percentage = row[m.fraction]

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
                for row in self.ls_treeview:
                    if row[m.code] == code and row[m.color]:  # Match the code in the liststore
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

        
