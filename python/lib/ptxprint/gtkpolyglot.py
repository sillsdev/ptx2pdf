import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import re, json
from enum import IntEnum
from ptxprint.utils import _, coltoonemax, brent
from ptxprint.polyglot import PolyglotConfig
from ptxprint.pastelcolorpicker import ColorPickerDialog

_modeltypes = (str, str, str, str, bool, float, float, float, float, str, str, str, str, int)
_modelfields = ('code', 'pg', 'prj', 'cfg', 'captions', 'fontsize', 'baseline', 'fraction', 'weight', 'color', 'prjguid', 'tooltip', 'widcol', 'bold')
m = IntEnum('m', [(x, i) for i, x in enumerate(_modelfields)])

class PolyglotSetup(Gtk.Box):

    _methods = """onDiglotClicked loadPolyglotSettings onDiglotAutoAdjust update_diglot_polyglot_UI
               """.split()

    def __init__(self, builder, view, tv):
        self.builder = builder
        self.view = view
        self.view.register(self, self._methods)
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

        self.ensure_right_click_handler()

        # Connect tooltips
        for col_id in range(0, m.tooltip):
            self.treeview.set_has_tooltip(True)  # Enable tooltips
            self.treeview.connect("query-tooltip", self.on_query_tooltip)  # Connect event
        self.validate_page_widths() # Make sure % Width gets colored red if invalid (even on loading)

        # Safely reparent the treeview
        parent = self.treeview.get_parent()
        if parent is not None:
            parent.remove(self.treeview)

        # Create a new scrolled window and add the treeview
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        scrolled_window.add(self.treeview)

        self.pack_start(scrolled_window, True, True, 0)

    def ensure_right_click_handler(self):
        # If a handler exists and is valid, disconnect it
        if hasattr(self.view, "_right_click_handler_id") and self.view._right_click_handler_id:
            try:
                self.treeview.disconnect(self.view._right_click_handler_id)
            except (TypeError, ValueError) as e:
                print("Warning: could not disconnect handler:", e)
        # Ensure only ONE handler is ever active
        self.view._right_click_handler_id = self.treeview.connect("button-press-event", self.on_right_click)

    def clear_polyglot_treeview(self):
        if not self.ls_treeview:
            return            
        self.ls_treeview.clear()
        self.update_layout_string(force=True)
        self.refresh_code_dropdowns()
        self.ensure_right_click_handler()
        self.update_context_menu()
                
    def load_polyglots_into_treeview(self):
        l_row_index = self.find_or_create_row("L")
        row_index = self.find_or_create_row("R")
        for sfx in self.codes:
            if sfx not in self.view.polyglots:  # Only process existing polyglots
                continue
            plyglot = self.view.polyglots[sfx]
            row_index = self.find_or_create_row(sfx)  # Find or add row
            prjguid, available_configs = self.get_available_configs(getattr(plyglot, 'prj'))
            plyglot.prjguid = prjguid
            plyglot.code = sfx
            self.ls_config[row_index].clear()
            for c in available_configs:
                self.ls_config[row_index].append([c])
            for idx, field in enumerate(_modelfields[1:11], start=1):
                val = getattr(plyglot, field)
                if sfx == "L" and idx in (m.fontsize, m.baseline):
                    val = 0
                self.ls_treeview[row_index][idx] = val
            if sfx == "L":
                polyview = self.view
            else:
                try:
                    polyview = self.view.createDiglotView(suffix=sfx)
                except ValueError:
                    listiter = self.ls_treeview.get_iter(row_index)
                    self.ls_treeview.remove(listiter)
                    continue
            if polyview is not None:
                if self.ls_treeview[row_index][m.fontsize] == 0:
                    self.ls_treeview[row_index][m.fontsize] = float(polyview.get("s_fontsize", 11.00))
                if self.ls_treeview[row_index][m.baseline] == 0:
                    self.ls_treeview[row_index][m.baseline] = float(polyview.get("s_linespacing", 15.00))
                if self.ls_treeview[row_index][m.color] in ("#FFFFFE", None):
                    c = polyview.get('_dibackcol', "#FFFFFE")
                    if c is not None and c.startswith("rgb("):
                        rgb = coltoonemax(c)
                        c = "#{0:02x}{1:02x}{2:02x}".format(*[int(x * 255) for x in rgb])
                    self.ls_treeview[row_index][m.color] = c
        # Always sync the L row to polyglots (creates polyglots["L"] if missing,
        # and ensures polyfraction_ is set in the view's _dict for config saving).
        self.updateRow(l_row_index)

        self.update_layout_string()
        self.ensure_right_click_handler()
        self.view.update_diglot_polyglot_UI()

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
        new_row = [sfx, pg, pri_prj, cfid, False, 11.0, 14.0, 50.0, 50.0, 
                   "#FFFFFE", pri_prjguid, "Tooltips", "#000000", 400]
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
        try:
            new_value = float(new_text)
        except ValueError:
            self.view.doStatus(f"Invalid input: {new_text}")
            return

        new_value = round(new_value, 2)
        self.ls_treeview[path][col_id] = new_value

        row_index = int(path)
        self.updateRow(row_index)

        sfx = self.ls_treeview[row_index][m.code]

        view_keys = {
            m.fraction: "polyfraction_",
            m.fontsize: "s_fontsize",
            m.baseline: "s_linespacing"
        }

        if col_id in view_keys:
            if col_id == m.fraction:
                self.validate_page_widths()

            aview = self.get_view(sfx)
            if aview is not None:
                aview.set(view_keys[col_id], new_value)
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
        used_codes = {row[m.code] for row in self.ls_treeview if row[m.code]}  # Set of used codes

        if exclude_path is not None:
            current_code = self.ls_treeview[exclude_path][m.code]
            used_codes.discard(current_code)

        available_codes = [code for code in self.codes if code not in used_codes]
        return available_codes

    def set_combo_options(self, options):
        model = Gtk.ListStore(str)
        if options is not None:
            for option in options:
                model.append([option])
        return model
        
    def on_combo_changed(self, widget, path, text, col_id):
        # self.model[row_index][col_id] is the the value BEFORE the change and 'text' is the new value !!!
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
            if prjguid is None:
                return
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
            cfg = text
        else:
            cfg = self.ls_treeview[row_index][m.cfg]

        sfx = self.ls_treeview[row_index][m.code]
        polyglot = self.view.polyglots.get(sfx, None)
        if col_id == m.prj or col_id == m.cfg:  
            # Check for duplicated Project and Configuration names
            for i, row in enumerate(self.ls_treeview):
                if i != row_index and row[m.prj] == prj and row[m.cfg] == cfg:
                    self.view.doStatus(_("Duplicate Project+Configuration not allowed)"))
                    return

            if polyglot is not None:
                polyglot.prj = prj
                polyglot.cfg = cfg
            polyview = self.get_view(sfx)
            if polyview is not None:
                polyview.updateProjectSettings(prj, prjguid, configName=cfg)
                if sfx != "L":
                    self.view.reloadDiglotPics(polyview, sfx, sfx)
        else:
            polyview = None

        self.ls_treeview[path][col_id] = text
        self.updateRow(row_index)
        if polyview is not None:
            f = polyview.get('s_fontsize', 11.0)
            self.ls_treeview[row_index][m.fontsize] = float(f)

            b = polyview.get('s_linespacing', 15.0)
            self.ls_treeview[row_index][m.baseline] = float(b)

            c = polyview.get('_dibackcol', "#FFFFFE")
            if c is not None and c.startswith("rgb("):
                rgb = coltoonemax(c)
                c = "#{0:02x}{1:02x}{2:02x}".format(*[int(x * 255) for x in rgb])      
            self.ls_treeview[row_index][m.color] = c
           
        # Refresh dropdowns and other dependencies after updating the combo box
        if col_id == m.code:    # Unique code changed
            if text != polyglot.code:
                self.view.moveDiglot(polyglot.code, text)
                self.refresh_code_dropdowns()
        elif col_id == m.pg:  # Page 1 or 2 changed
            self.validate_page_widths()
            self.update_layout_string(force=True)
            self.treeview.queue_draw()  # Refresh UI
        self.view.updateDialogTitle()
            
    def changeConfigName(self, config):
        if len(self.ls_treeview):
            self.ls_treeview[0][m.cfg] = config
            self.updateRow(0)
        self.view.updateDialogTitle()

    def updateRow(self, row_index):
        sfx = self.ls_treeview[row_index][m.code]
        plyglt = self.view.polyglots.get(sfx, None)
        if plyglt is None:
            plyglt = PolyglotConfig()
            plyglt.code = sfx
            self.view.polyglots[sfx] = plyglt
        for idx, field in enumerate(_modelfields[1:11], start=1):
            val = self.ls_treeview[row_index][idx]
            setattr(plyglt, field, val)
        if row_index == 0 and not self.view.noUpdate:
            for a, b in {"fontsize": "s_fontsize", "baseline" : "s_linespacing", "fraction": "polyfraction_", "color": "_dibackcol"}.items():
                self.view.set(b, self.ls_treeview[row_index][getattr(m, a)])
                self.view.changed()
        else:
            aview = self.get_view(sfx)
            if aview is not None:
                aview.changed()
        
    def refresh_code_dropdowns(self):
        if hasattr(self, "code_renderer"):  # Ensure renderer exists before updating
            available_codes = self.get_available_codes()
            self.code_renderer.set_property("model", self.set_combo_options(available_codes))

    def set_color_from_menu(self, widget):
        selected = self.get_selected_row()
        if selected:
            model, iter, path = selected
            self.on_color_clicked(None, path, model[path][m.color])

    def remove_color_shading(self, widget):
        for i, row in enumerate(self.ls_treeview):
            row[m.color] = "#FFFFFE"
            self.updateRow(i)
        self.update_layout_preview()
                
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
            rgb = coltoonemax(color_hex)
            color_hex = "#{0:02x}{1:02x}{2:02x}".format(*(int(x * 255) for x in rgb))
            
            # Update the model with the selected hex color
            model.set_value(iter, m.color, color_hex)
            row_index = int(path[0])
            self.updateRow(row_index)
            self.update_layout_string()

        dialog.destroy()

    def on_toggle(self, widget, path, col_id):
        row_index = int(path)
        model = self.ls_treeview
        iter = model.get_iter(path)  # Get the iterator for the row
        current_value = model.get_value(iter, col_id)  # Read current state
        if row_index == 0:
            self.view.doStatus(_("You cannot disable captions for the primary 'L' project in a diglot."))
        else:
            model.set_value(iter, col_id, not current_value)  # Toggle it
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

            # Properly dispose of old context menu
            if hasattr(self, "context_menu") and self.context_menu:
                self.context_menu.destroy()
                self.context_menu = None  # Clear reference

            # Now safely build a new menu            
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
            move_up_item.set_sensitive(not is_first_row and not row_index == 1)  # Disable if Row 0 + 1
            self.context_menu.append(move_up_item)

            move_down_item = Gtk.MenuItem(label=_("Move Down"))
            move_down_item.connect("activate", self.move_selected_row, 1)
            move_down_item.set_sensitive(not is_first_row and not row_index == 1)  # Disable if Row 0 + 1
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
            delete_item.set_sensitive(not is_first_row and not row_index == 1)  # Disable if Row 0 + 1
            self.context_menu.append(delete_item)

            change_cfg_settings = Gtk.MenuItem(label=_("Edit Settings..."))
            change_cfg_settings.connect("activate", self.edit_other_config)
            change_cfg_settings.set_sensitive(not is_first_row)  # Disable if Row 0
            self.context_menu.append(change_cfg_settings)

            color_item = Gtk.MenuItem(label=_("Set Color..."))
            color_item.connect("activate", self.set_color_from_menu)
            self.context_menu.append(color_item)

            remove_color_item = Gtk.MenuItem(label=_("Remove All Colors"))
            remove_color_item.connect("activate", self.remove_color_shading)
            self.context_menu.append(remove_color_item)

            self.context_menu.show_all()
            self.update_context_menu()  # Apply correct state
            self.context_menu.popup_at_pointer(event)

    def delete_selected_row(self, widget):
        selected = self.get_selected_row()
        if selected:
            model, iter, path = selected
            row_index = int(path[0])
            sfx = self.ls_treeview[row_index][m.code]
            self.view.removeDiglotView(sfx)
            model.remove(iter)
            self.update_layout_string(force=True)
            self.refresh_code_dropdowns()  # Refresh available codes
            self.update_context_menu()     # Refresh menu state
            self.view.update_diglot_polyglot_UI()
            self.validate_page_widths()    # Refresh color of % width
        self.view.updateDialogTitle()

    def update_context_menu(self):
        if not len(self.ls_treeview):
            return
        max_rows = 9
        has_room = len(self.ls_treeview) < max_rows

        for item in self.context_menu.get_children():
            if isinstance(item, Gtk.MenuItem) and item.get_label() == "Add a row/text":
                item.set_sensitive(has_room)  # Enable/disable based on row count

    def get_prj_cfg(self):
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            prj = model.get_value(iter, m.prj)
            cfg = model.get_value(iter, m.cfg)
            return prj, cfg
        else:
            return None, None
        
    def edit_other_config(self, menu_item):
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            pref = model.get_value(iter, m.code)
            self.view.switchToDiglot(pref)

    def get_curr_proj(self):
        w = self.builder.get_object('fcb_project')
        m = w.get_model() # liststore
        aid = w.get_active_iter()
        prjid = m.get_value(aid, 0)
        prjguid = m.get_value(aid, 1)
        return prjid, prjguid

    def add_row(self, widget):
        if len(self.ls_treeview) >= 9:
            self.view.doStatus("Maximum of 9 rows reached. Cannot add more.")
            return  # Stop if the limit is reached
        available_codes = self.get_available_codes()
        next_code = str(available_codes[m.code]) if available_codes else ""  # Auto-assign next available code
        self.find_or_create_row(next_code, save=True)
        # Perform additional updates
        self.update_layout_string(force=True)
        self.refresh_code_dropdowns()
        self.view.update_diglot_polyglot_UI()
        self.validate_page_widths()
        self.update_context_menu()
        self.view.updateDialogTitle()
        
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
        self.view.updateDialogTitle()

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

    def setfontsize(self, size):
        self.ls_treeview[0][m.fontsize] = float(size)
        self.updateRow(0)

    def setbaseline(self, spacing):
        self.ls_treeview[0][m.baseline] = float(spacing)
        self.updateRow(0)

    def homogenize_fontsize(self, widget):
        selected = self.get_selected_row()
        if not selected:
            return  # No row selected

        model, iter, path = selected
        new_size = model[path][m.fontsize]

        # Apply the new size to each row
        for row in range(len(model)):
            model[row][m.fontsize] = new_size
            self.updateRow(row)

    def homogenize_spacing(self, widget):
        selected = self.get_selected_row()
        if not selected:
            return  # No row selected

        model, iter, path = selected
        new_spacing = model[path][m.baseline]

        # Apply the new size to each row
        for row in range(len(model)):
            model[row][m.baseline] = new_spacing
            self.updateRow(row)

    def distribute_width_evenly(self, widget):
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
            model[row][m.fraction] = new_width
            self.updateRow(row)

        self.update_layout_string()
        self.validate_page_widths()  # Refresh highlighting

    def validate_page_widths(self):
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

    def update_layout_string(self, force=False):
        ot = self.view.get('t_layout', None)
        t = self.generate_layout_from_treeview()
        if len(t) > len(ot) or force:
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
        # Rule 2: Ensure there are no spaces and don't allow complex layouts (yet)
        if " " in t_layout:
            return False, _("Spaces not allowed")
        allow_complex = hasattr(self, 'view') and hasattr(self.view, 'args') and self.view.args.experimental & 1 != 0
        if not allow_complex and ("/" in t_layout or "\\" in t_layout):
            return False, _("Complex layouts are not yet supported")
            
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

    def updatePluginsForLayout(self, layout):
        plugins_widget = self.builder.get_object('t_plugins')
        if plugins_widget is None:
            return
        current = plugins_widget.get_text()
        plugins = [p.strip() for p in current.split(',') if p.strip()]
        if "/" in layout:
            if "polyglot-complexpages" not in plugins:
                plugins = [p for p in plugins if p != "polyglot-simplepages"]
                plugins.append("polyglot-complexpages")
                plugins_widget.set_text(",".join(plugins))
        elif "," in layout:
            if "polyglot-simplepages" not in plugins and "polyglot-complexpages" not in plugins:
                plugins.append("polyglot-simplepages")
                plugins_widget.set_text(",".join(plugins))

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

        self.updatePluginsForLayout(layout)

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
                color_hex = "#FFFFFE"  # Default to white
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

### View methods

    def onDiglotClicked(self, btn):
        # Guard against re-entry when we programmatically restore the checkbox state below.
        if getattr(self, '_restoringDiglot', False):
            return

        # GTK3 fires 'clicked' from set_active() as well as from real user clicks.
        # During config/project loading, loadingConfig=True — run only the cheap UI
        # updates and return immediately so no dialog can ever appear mid-load.
        if self.view.loadingConfig:
            self.view.sensiVisible("c_diglot")
            self.view.colorTabs()
            return

        # ---- Interactive click only beyond this point ----

        # User just unchecked diglot: restore it visually and offer Save-As-Monoglot.
        if not self.view.get("c_diglot"):
            self._restoringDiglot = True
            btn.set_active(True)          # restore visual state (triggers clicked again)
            self._restoringDiglot = False
            self._showSaveAsMonoglotDialog()
            return

        # User just checked diglot: confirm this is intentional.
        dialog = self.builder.get_object("dlg_confirmDiglot")
        response = dialog.run()
        dialog.hide()
        if response != Gtk.ResponseType.YES:
            # User declined – silently restore the checkbox to unchecked and return
            # before any UI state has changed.  handler_block prevents re-entering
            # this function; mod=False avoids marking the config as changed.
            btn.handler_block_by_func(self.onDiglotClicked)
            self.view.set("c_diglot", False, mod=False)
            btn.handler_unblock_by_func(self.onDiglotClicked)
            return

        # ---- Normal path: activation confirmed ----
        self.view.sensiVisible("c_diglot")
        self.view.colorTabs()
        if self.view.get("c_diglot"):
            self.loadPolyglotSettings()
            self.view.createDiglotView()  # stores result in self.diglotViews['R'] only when non-None
            self.view.set("c_doublecolumn", True)
            self.builder.get_object("c_doublecolumn").set_sensitive(False)
            # Open the Project dropdown for the R row so the user immediately knows
            # they need to select a secondary project.
            tv = self.treeview
            cols = tv.get_columns()
            if len(cols) > 2:
                proj_col = cols[2]   # Code=0, 1|2=1, Project=2
                def _open_project_dropdown(tv=tv, proj_col=proj_col):
                    model = tv.get_model()
                    for i, row in enumerate(model):
                        if row[0] == "R":   # m.code == 0
                            path = Gtk.TreePath([i])
                            tv.scroll_to_cell(path, proj_col, False, 0.0, 0.0)
                            tv.set_cursor(path, proj_col, True)
                            break
                    return False
                GLib.idle_add(_open_project_dropdown)
        else:
            self.builder.get_object("c_doublecolumn").set_sensitive(True)
            self.view.setPrintBtnStatus(2)
            self.view.diglotViews = {}
        self.view.updateDialogTitle()
        self.view.disableLayoutAnalysis()
        self.view.loadPics(mustLoad=False, force=True)
        if self.view.get("c_includeillustrations"):
            self.view.onUpdatePicCaptionsClicked(None)

    def _onMonoglotNameChanged(self, entry):
        """Live validation for the 't_newMonoglotConfigName' entry in dlg_saveAsMonoglot."""
        cfg = entry.get_text()
        ok_btn   = self.builder.get_object("btn_disableDiglot_ok")
        msg_lbl  = self.builder.get_object("l_diableDiglotNewCfgMsg")
        cleanCfg = re.sub('[^-a-zA-Z0-9_()]+', '', cfg)
        cpath    = self.view.project.srcPath(cleanCfg) if cleanCfg and self.project else None
        if cfg != cleanCfg:
            msg = _("Do not use spaces or special characters")
        elif not len(cfg):
            msg = ""
        elif cpath is not None and os.path.exists(cpath):
            msg = _("That Configuration already exists.\nUse another name.")
        else:
            ok_btn.set_sensitive(True)
            msg_lbl.set_text("")
            return
        ok_btn.set_sensitive(False)
        msg_lbl.set_text(msg)

    def _showSaveAsMonoglotDialog(self):
        r"""Show the 'Save As Monoglot' dialog and act on the response.

        Cancel  -> c_diglot stays True (already restored before this is called).
        OK      -> The current settings are saved under the chosen name with
                  c_diglot turned off; that new monoglot configuration becomes active.
                  The original diglot configuration is left untouched on disk.
        """
        entry   = self.builder.get_object("t_newMonoglotConfigName")
        ok_btn  = self.builder.get_object("btn_disableDiglot_ok")
        msg_lbl = self.builder.get_object("l_diableDiglotNewCfgMsg")

        # Reset dialog widgets to a clean state
        entry.set_text("")
        ok_btn.set_sensitive(False)
        msg_lbl.set_text("")

        # Connect live validation once (avoid duplicate connections on repeated opens)
        if not getattr(self, '_monoglotDlgSigConnected', False):
            entry.connect("changed", self._onMonoglotNameChanged)
            self._monoglotDlgSigConnected = True

        dialog   = self.builder.get_object("dlg_saveAsMonoglot")
        dialog.show_all()
        response = dialog.run()
        dialog.hide()

        if response != Gtk.ResponseType.OK:
            return  # User cancelled – diglot remains active, nothing to do.

        cfg = re.sub('[^-a-zA-Z0-9_()]+', '', entry.get_text())
        if not cfg:
            return  # Safety guard – shouldn't be reachable while OK button is insensitive.

        # ── Step 1: Save the current state as a new configuration ──
        # This mirrors onSaveAsNewConfig exactly.  Internally, onSaveConfig calls
        # updateProjectSettings(readConfig=True) which copies the existing diglot
        # config files to the new name and then re-reads them from disk.  That
        # read restores c_diglot=True in memory, so we must NOT try to turn diglot
        # off before this call – we do it in step 2 instead.
        self.view.set("ecb_savedConfig", cfg)
        self.view.doConfigNameChange(cfg)
        self.view.changed()
        self.view.onSaveConfig(None)
        # After onSaveConfig the new config is on disk but still has c_diglot=True
        # because the re-read from the copied file restored that value in memory.

        # ── Step 2: Turn off diglot in memory and overwrite the new config ──
        # Block the signal so set() doesn't re-enter onDiglotClicked.
        diglot_btn = self.builder.get_object("c_diglot")
        diglot_btn.handler_block_by_func(self.onDiglotClicked)
        self.view.set("c_diglot", False)   # marks isChanged=True via changed()
        diglot_btn.handler_unblock_by_func(self.onDiglotClicked)
        self.view.saveConfig()             # writes c_diglot=False to the new config on disk

        # ── Step 3: Finalise the new config identity ──
        # Now that c_diglot=False, loadPolyglotSettings will only clear the
        # treeview rather than trying to load diglot data.
        self.view.updateConfigIdentity(cfg)

        # ── Step 4: Run the deactivation housekeeping that onDiglotClicked would ──
        # have done in its 'else' branch (and the shared tail code after it).
        self.view.sensiVisible("c_diglot")
        self.view.colorTabs()
        self.builder.get_object("c_doublecolumn").set_sensitive(True)
        self.view.setPrintBtnStatus(2)
        self.view.diglotViews = {}
        self.view.updateDialogTitle()
        self.view.disableLayoutAnalysis()
        self.view.loadPics(mustLoad=False, force=True)
        if self.view.get("c_includeillustrations"):
            self.view.onUpdatePicCaptionsClicked(None)

    def switchToDiglot(self, pref):
        dv = None
        dvprj = None
        dvcfg = None
        if self.view.otherDiglot is not None:
            if pref is not None:
                dv = self.view.otherDiglot[2].get(pref, None)
        elif self.view.diglotViews is not None:
            dv = self.view.diglotViews.get(pref, None)
        if dv is None:
            if self.view.otherDiglot is not None:
                dvprj, dvcfg = self.otherDiglot[:2]
            else:
                return False
        elif dv:
            dv.saveConfig()
            dvprj = dv.project
            dvcfg = dv.cfgid
        if pref is not None:
            if self.view.otherDiglot is None:
                self.view.otherDiglot = (self.view.project, self.view.cfgid, self.view.diglotViews.copy())
            # self.builder.get_object("b_print2ndDiglotText").set_visible(True)
            self.view.changeBtnLabel("b_print", _("Return to Primary"))
            self.builder.get_object("b_reprint").set_sensitive(False)
            self.builder.get_object("b_print2ndDiglotText").set_visible(True)
        else:
            self.view.changeBtnLabel("b_print", _("Print (Make PDF)"))
            self.builder.get_object("b_print2ndDiglotText").set_visible(False)
            self.builder.get_object("b_reprint").set_sensitive(True)
            if self.view.otherDiglot is not None:
                self.view.diglotViews = self.view.otherDiglot[2]
                self.view.otherDiglot = None
        self.view.set("fcb_project", dvprj.prjid)
        self.view.set("ecb_savedConfig", dvcfg)
        self.view.disableLayoutAnalysis()
        # self.updateProjectSettings(dvprj.prjid, dvprj.guid, configName=dv.cfgid)
        # self.updateDialogTitle()
        return True

    def onDiglotAutoAdjust(self, btn):
        if self.isDiglotMeasuring:
            btn.set_active(True)
            return
        elif not self.get("c_diglot"):
            btn.set_active(False)
            return
        elif not btn.get_active():
            return
        self.isDiglotMeasuring = True
        btn.set_active(True)
        xdvname = os.path.join(self.view.project.printPath(self.view.cfgid), self.view.baseTeXPDFnames()[0] + ".xdv")
        def score(x):
            self.set_fraction(x)
            runjob = self.view.callback(self, maxruns=1, noview=True)
            while runjob.thread.is_alive():
                Gtk.main_iteration_do(False)
            runres = runjob.res
            return 20000 if runres else xdvigetpages(xdvname)
        mid = self.get_fraction()
        res = brent(0., 1., mid, score, 0.001)
        self.set_fraction(res)
        self.isDiglotMeasuring = False
        self.view.callback(self)
        btn.set_active(False)

    def update_diglot_polyglot_UI(self):
        dglt = True if len(self.ls_treeview) < 3 else False
        self.builder.get_object("btn_adjust_diglot").set_sensitive(dglt)
        orig = self.view.get("fcb_diglotMerge", "scores")
        merge_types = {
            _("Document based"):   "doc",
            _("Chapter Verse"):    "simple",
            _("Scored"):           "scores",
            _("Scored (Chapter)"): "scores-chapter",
            _("Scored (Verse)"):   "scores-verse"
            }
        mrgtyplist = self.builder.get_object("ls_diglotMerge")
        mrgtyplist.clear()
        for desc, code in merge_types.items():
            if dglt or code.startswith("scores"):
                mrgtyplist.append([desc, code])
        found = any(row[1] == orig for row in mrgtyplist)
        self.view.set("fcb_diglotMerge", orig if found else "scores") 

    def loadPolyglotSettings(self, config=None):
        self.clear_polyglot_treeview()
        if self.view.get("c_diglot"):
            if config is not None:
                self.view.polyglots["L"].cfg = config
            self.load_polyglots_into_treeview()

