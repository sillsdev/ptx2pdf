import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Pango
from ptxprint.utils import BuildParams, parseBookList, startfile, chaps, asfloat, _
from ptxprint.multiprint import MultiPrint

def printSetup(view, args):
    for k, v in args.items():
        if k.startswith("__"):
            continue
        view.setvar(k, v)

# TreeStore layout:
# 0: label (str)       -> "Field" column text (the pid on parent rows)
# 1: value_text (str)  -> "Value" column text (the books on parent rows)
# 2: select (bool)     -> "Print" column, meaningful only on parent rows
# 3: is_parent (bool)  -> controls visibility of Select toggle / editability
# 4: editable (bool)   -> whether the key text renderer can be edited (for the pid)
# 5: col_key (str)     -> underlying data column name
# 6: row_key (str)     -> key into `data` for the publication (set on both)
# 7: weight (int)      -> bold for parent rows
# 8: foreground (str)  -> red when the books value is invalid
# 9: tooltip (str)     -> markup explaining a problem, if any
NORMALCOL = "#000000"
ERRORCOL = "#FF0000"
MAINCOL = "#808080"
MAINKEY = "⁠main⁠"   # row_key of the read-only "main" row (invisible marks, so no pid clashes)

class ButtonCellRenderer(Gtk.CellRendererText):
    """ Draws a cell like a (small) GtkButton, using a real button's theme styling """

    def __init__(self, button):
        super().__init__()
        self.button = button
        self.set_property("xalign", 0.5)
        self.set_property("xpad", 10)
        self.set_property("ypad", 3)
        self.set_property("scale", 0.85)

    def do_render(self, cr, widget, bg_area, cell_area, flags):
        ctx = self.button.get_style_context()
        x, y = cell_area.x + 2, cell_area.y + 1
        w, h = cell_area.width - 4, cell_area.height - 2
        Gtk.render_background(ctx, cr, x, y, w, h)
        Gtk.render_frame(ctx, cr, x, y, w, h)
        layout = widget.create_pango_layout(self.get_property("text"))
        font = ctx.get_font(Gtk.StateFlags.NORMAL).copy()
        font.set_size(int(font.get_size() * 0.85))
        layout.set_font_description(font)
        tw, th = layout.get_pixel_size()
        Gtk.render_layout(ctx, cr, x + (w - tw) / 2, y + (h - th) / 2, layout)

class PublicationsView:

    _methods = """onPubAdd onPubDel onPubDuplicate onPubPrint onPubSelect onPubEdited
                  onPubExpandAll onPubCollapseAll onPubRowActivated onPubSelectionChanged
               """.split()

    def __init__(self, view):
        self.view = view
        self.builder = view.builder
        self.view.register(self, self._methods)
        self.printing = False
        self.ts = self.builder.get_object("ts_publications")
        self.tv = self.builder.get_object("tv_publications")
        self._setupSelectAllHeader()
        self._setupMainRowAndButtons()
        self._updateStatus()

    def _setupMainRowAndButtons(self):
        """ Grey out the main row, and add 'to main' / 'from main' button columns """
        self.tv.set_tooltip_column(-1)
        self.tv.set_has_tooltip(True)
        self.tv.connect("query-tooltip", self._onQueryTooltip)
        self.tv.connect("button-press-event", self._onButtonPress)
        self.fcr = self.builder.get_object("cr_pub_field")
        self.builder.get_object("col_pub_field").set_cell_data_func(self.fcr, self._greyMain)
        self.vcr = self.builder.get_object("cr_pub_value")
        self.builder.get_object("col_pub_value").set_cell_data_func(self.vcr, self._greyMain)
        self.btncols = {}
        for key, label in (("tomain", _("to main")), ("frommain", _("from main"))):
            cr = ButtonCellRenderer(self.builder.get_object("btn_pubAdd"))
            cr.set_property("text", label)
            col = Gtk.TreeViewColumn("", cr)
            col.set_cell_data_func(cr, self._showButton)
            self.tv.append_column(col)
            self.btncols[col] = key
        self.btntips = {
            "tomain": _("This will copy the book and variables from this publication "
                        "into the main areas on the Basic and Peripheral tabs"),
            "frommain": _("This will copy the book and variables from the main areas "
                          "on the Basic and Peripheral tabs into this publication")}
        self.maintip = _("To edit these values, either load them from a specific publication "
                         "or change them in the Basic and Peripheral tabs")

    def _isMainIter(self, model, titer):
        return model[titer][6] == MAINKEY

    def _greyMain(self, col, cr, model, titer, *a):
        ismain = self._isMainIter(model, titer)
        if ismain:
            cr.set_property("foreground", MAINCOL)
        elif cr is self.vcr:
            cr.set_property("foreground", model[titer][8] or NORMALCOL)
        else:
            cr.set_property("foreground", NORMALCOL)
        if cr is self.vcr:
            cr.set_property("editable", not ismain)

    def _showButton(self, col, cr, model, titer, *a):
        cr.set_property("visible", model[titer][3] and not self._isMainIter(model, titer))

    def _onQueryTooltip(self, tv, x, y, keyboard, tooltip):
        ok, x, y, model, path, titer = tv.get_tooltip_context(x, y, keyboard)
        if not ok:
            return False
        res = tv.get_path_at_pos(x, y) if not keyboard else None
        col = res[1] if res else None
        if self._isMainIter(model, titer):
            tip = GLib.markup_escape_text(self.maintip)
        elif col in self.btncols and model[titer][3]:
            tip = GLib.markup_escape_text(self.btntips[self.btncols[col]])
        else:
            tip = model[titer][9]
        if not tip:
            return False
        tooltip.set_markup(tip)
        tv.set_tooltip_row(tooltip, path)
        return True

    def _onButtonPress(self, tv, event):
        if event.button != 1:
            return False
        res = tv.get_path_at_pos(int(event.x), int(event.y))
        if res is None:
            return False
        path, col = res[0], res[1]
        if col not in self.btncols:
            return False
        titer = self.ts.get_iter(path)
        r = self.ts[titer]
        if not r[3] or r[6] == MAINKEY:
            return False
        if self.btncols[col] == "tomain":
            self.toMain(r[6])
        else:
            self.fromMain(titer)
        return True

    def _mainValues(self):
        """ Returns (books, {key: value}) from the Basic and Peripheral tabs """
        return (self._currentBooks(), {k: str(self._defaultValue(k)) for k in self._publishableKeys()})

    def _mainIter(self):
        titer = self.ts.get_iter_first()
        if titer is not None and self.ts[titer][6] == MAINKEY:
            return titer
        return None

    def refreshMain(self):
        """ (Re)builds the grey 'main' row at the top from the Basic and Peripheral tabs """
        books, vals = self._mainValues()
        titer = self._mainIter()
        expanded = False
        if titer is not None:
            expanded = self.tv.row_expanded(self.ts.get_path(titer))
            self.ts.remove(titer)
        titer = self.ts.prepend(None, [_("main"), books, False, False, False, "__books", MAINKEY,
                                       Pango.Weight.BOLD, MAINCOL, None])
        for k, v in vals.items():
            self.ts.append(titer, [k, v, False, False, False, k, MAINKEY, Pango.Weight.NORMAL, MAINCOL, None])
        if expanded:
            self.tv.expand_row(self.ts.get_path(titer), False)

    def _pubRows(self):
        """ The publication rows, without the main row """
        return [r for r in self.ts if r[6] != MAINKEY]

    def toMain(self, pid):
        """ Copies a publication's books and variables to the Basic and Peripheral tabs """
        self.applyToView(pid=pid)
        self.refreshMain()
        self.view.doStatus(_("Copied '{}' into the Basic and Peripheral tabs").format(pid))

    def fromMain(self, titer):
        """ Copies the books and variables on the Basic and Peripheral tabs into a publication """
        row = self.ts[titer]
        books, vals = self._mainValues()
        changes = []
        if row[1].strip() and row[1].strip() != books.strip():
            changes.append(_("books: '{}' \u2192 '{}'").format(row[1], books))
        existing = {cr[5]: cr[1] for cr in row.iterchildren()}
        for k, v in vals.items():
            old = existing.get(k, "")
            if old and old != v:
                changes.append("{}: '{}' \u2192 '{}'".format(k, old, v))
        if changes and not self.view.msgQuestion(_("Overwrite publication '{}'?").format(row[0]),
                    _("Copying from main will change:") + "\n\n" + "\n".join(changes)):
            return
        row[1] = books
        row[8], row[9] = self._checkBooks(books)
        children = {cr[5]: cr.iter for cr in row.iterchildren()}
        for k, v in vals.items():
            if k in children:
                self.ts[children[k]][1] = v
            else:
                self.ts.append(titer, self._childRow(k, v, row[6]))
        self._updateStatus()
        self.view.doStatus(_("Copied the Basic and Peripheral tab values into '{}'").format(row[0]))

    def _setupSelectAllHeader(self):
        """ Put a checkbox in the Print column header that ticks/unticks everything """
        col = self.builder.get_object("col_pub_select")
        self.cb_all = Gtk.CheckButton()
        self.cb_all.set_tooltip_text(_("Tick or untick all publications"))
        self.cb_all.show()
        col.set_widget(self.cb_all)
        col.set_clickable(True)
        col.connect("clicked", self.onPubToggleAll)

    def _publishableKeys(self):
        res = ['maintitle', 'subtitle']
        res.extend([k for k,v in self.view.pubvars_publishable.items() if k not in res and v])
        # keep the row if any publication has a value, so it is not lost when saving
        haspc = any("pagecount" in p for p in self.view.publications.values())
        if (self.view.get("c_inclSpine") or haspc) and "pagecount" not in res:
            res.append("pagecount")     # used to calculate each publication's spine width
        return res

    def _defaultValue(self, key):
        """ Returns the value a publication starts with for this key """
        if key == "pagecount":
            return str(self.view.get("s_totalPages") or "")
        return self.view.getvar(key, "")

    def _parentRow(self, pid, books, select):
        fg, tip = self._checkBooks(books)
        return [pid, books, select, True, True, "__books", pid, Pango.Weight.BOLD, fg, tip]

    def _childRow(self, key, val, pid):
        return [key, str(val), False, False, False, key, pid, Pango.Weight.NORMAL, NORMALCOL, None]

    def load(self, data: dict):
        selected_keys = self._publishableKeys()
        self.ts.clear()
        for pid, pub in sorted(self.view.publications.items()):
            select_bool = pub.get("__select", "0").lower() == "true"
            parent_iter = self.ts.append(None, self._parentRow(pid, pub.get("__books", ""), select_bool))
            for col in selected_keys:
                val = pub.get(col)
                if val is None:
                    val = self._defaultValue(col)
                self.ts.append(parent_iter, self._childRow(col, val, pid))
        if len(self.ts) < 6:
            self.tv.expand_all()
        self.refreshMain()
        self._updateStatus()

    def save(self):
        """ Returns a new publications dictionary from the self.ts """
        self.ts = self.builder.get_object("ts_publications")
        res = {}
        for row in self._pubRows():
            currpid = row[0]
            res.setdefault(currpid, {})['__books'] = row[1]
            res[currpid]['__select'] = 'true' if row[2] else 'false'
            for crow in row.iterchildren():
                # don't use crow[6] since it may be out of date
                res[currpid][crow[5]] = crow[1]
        return res

    def iter_selected(self):
        for i, r in enumerate(self.ts):
            if r[2] and r[6] != MAINKEY:
                yield (i, r)

    def _checkBooks(self, books):
        """ Returns (foreground colour, tooltip markup) for a books value """
        books = books.strip()
        if not books:
            return (ERRORCOL, GLib.markup_escape_text(_("No books specified. Click here to enter "
                                        "a list of books, e.g. 'RUT JON' or 'MAT-JHN'.")))
        if self._isModule(books):
            return (NORMALCOL, None)
        refs, err = parseBookList(books)
        if err is not None:
            return (ERRORCOL, GLib.markup_escape_text(err))
        return (NORMALCOL, None)

    def _isModule(self, books):
        """ A books value may instead be the path to a module file """
        if os.path.isfile(books):
            return True
        prjpath = getattr(self.view.project, "path", None)
        return prjpath is not None and os.path.isfile(os.path.join(prjpath, books))

    def _uniquePid(self, base):
        existing = set(r[0] for r in self._pubRows())
        if base not in existing:
            return base
        i = 2
        while f"{base} ({i})" in existing:
            i += 1
        return f"{base} ({i})"

    def _currentParent(self):
        """ Returns the iter of the publication containing the highlighted row, or None """
        model, titer = self.tv.get_selection().get_selected()
        if titer is None:
            return None
        parent = model.iter_parent(titer)
        res = parent if parent is not None else titer
        return None if model[res][6] == MAINKEY else res

    def _selectAndShow(self, titer):
        path = self.ts.get_path(titer)
        self.tv.expand_row(path, False)
        self.tv.get_selection().select_iter(titer)
        self.tv.scroll_to_cell(path, None, False, 0, 0)

    def _updateStatus(self):
        pubs = self._pubRows()
        total = len(pubs)
        chosen = sum(1 for r in pubs if r[2])
        if total == 0:
            msg = _("No publications yet. Click 'Add' to create one.")
        else:
            msg = _("{} of {} publications selected for printing").format(chosen, total)
            nbad = sum(1 for r in pubs if r[8] == ERRORCOL)
            if nbad:
                msg += "  " + _("({} with invalid books)").format(nbad)
        self.builder.get_object("l_pubStatus").set_text(msg)
        self.cb_all.set_inconsistent(0 < chosen < total)
        self.cb_all.set_active(total > 0 and chosen == total)
        self.builder.get_object("btn_pubPrint").set_sensitive(chosen > 0 and not self.printing)
        hascurr = self._currentParent() is not None
        for w in ("btn_pubDuplicate", "btn_pubDel"):
            self.builder.get_object(w).set_sensitive(hascurr)

    def _currentBooks(self):
        """ Returns the books/range/module currently chosen on the Basic tab """
        scope = self.view.get("r_book")
        if scope == "module":
            return str(self.view.moduleFile or "")
        elif scope == "multiple":
            return self.view.get("ecb_booklist", "").strip()
        bk = self.view.get("ecb_book") or ""
        if not bk:
            return ""
        try:
            fromch = round(asfloat(self.view.get("t_chapfrom"), 1))
            toch = round(asfloat(self.view.get("t_chapto"), 0))
        except ValueError:
            return bk
        maxch = int(chaps.get(bk, "0"))
        if fromch <= 1 and (toch <= 0 or toch >= maxch):
            return bk
        elif fromch == toch:
            return f"{bk} {fromch}"
        return f"{bk} {fromch}-{toch}"

    def onPubAdd(self, btn):
        """ Adds a publication pre-filled from the current configuration """
        title = self.view.getvar("maintitle", "").strip()
        pid = self._uniquePid(title or _("New publication"))
        parent_iter = self.ts.append(None, self._parentRow(pid, self._currentBooks(), True))
        for k in self._publishableKeys():
            self.ts.append(parent_iter, self._childRow(k, self._defaultValue(k), pid))
        self._selectAndShow(parent_iter)
        self._updateStatus()

    def onPubDuplicate(self, btn):
        src = self._currentParent()
        if src is None:
            return
        srcrow = self.ts[src]
        pid = self._uniquePid(_("Copy of {}").format(srcrow[0]))
        newrow = list(srcrow)
        newrow[0] = newrow[6] = pid
        new_iter = self.ts.insert_after(None, src, newrow)
        for crow in srcrow.iterchildren():
            c = list(crow)
            c[6] = pid
            self.ts.append(new_iter, c)
        self._selectAndShow(new_iter)
        self._updateStatus()

    def onPubDel(self, btn):
        titer = self._currentParent()
        if titer is None:
            return
        pid = self.ts[titer][0]
        if not self.view.msgQuestion(_("Delete publication?"),
                    _("Are you sure you want to delete the publication '{}'?").format(pid)):
            return
        self.ts.remove(titer)
        self._updateStatus()

    def onPubToggleAll(self, col):
        pubs = self._pubRows()
        newval = not all(r[2] for r in pubs)
        for r in pubs:
            r[2] = newval
        self._updateStatus()

    def onPubExpandAll(self, btn):
        self.tv.expand_all()

    def onPubCollapseAll(self, btn):
        self.tv.collapse_all()

    def onPubRowActivated(self, tv, path, col):
        """ Double-click on a publication expands/collapses it """
        if tv.row_expanded(path):
            tv.collapse_row(path)
        else:
            tv.expand_row(path, False)

    def onPubSelectionChanged(self, sel):
        self._updateStatus()

    def onPubSelect(self, btn, path):
        titer = self.ts.get_iter(path)
        if self.ts[titer][6] == MAINKEY:
            return
        new_val = not self.ts[titer][2]
        self.ts[titer][2] = new_val
        self._updateStatus()

    def applyToView(self, view=None, pid=None):
        if view is None:
            view = self.view
        if pid is None:
            piter = self._currentParent()
            if piter is None:       # no publication highlighted: print the view as it is
                return
        else:
            for piter, r in enumerate(self.ts):
                if r[6] == pid and pid != MAINKEY:
                    break
            else:
                return
        row = self.ts[piter] 
        books = row[1].strip()
        if self._isModule(books):
            view.set("r_book", "module")
            view.moduleFile = books
        else:
            view.set("r_book", "multiple")
            view.set("ecb_booklist", books)
        printSetup(view, {cr[5]: cr[1] for cr in row.iterchildren()})

    def onPubEdited(self, widget, path, new_text):
        titer = self.ts.get_iter(path)
        if self.ts[titer][6] == MAINKEY:
            return
        if widget is self.builder.get_object("cr_pub_field"):
            new_text = new_text.strip()
            if not new_text or new_text == self.ts[titer][0]:
                return
            if any(r[0] == new_text for r in self._pubRows()):
                self.view.doError(_("A publication called '{}' already exists.").format(new_text))
                return
            self.ts[titer][0] = new_text
            self.ts[titer][6] = new_text
            for crow in self.ts[titer].iterchildren():
                crow[6] = new_text
        else:
            self.ts[titer][1] = new_text
            if self.ts[titer][3]:
                fg, tip = self._checkBooks(new_text)
                self.ts[titer][8] = fg
                self.ts[titer][9] = tip
        self._updateStatus()

    def onPubPrint(self, btn):
        # Save the config first so that the publications (and any other changes) are kept
        self.view.onSaveConfig(None)
        jobs = []
        skipped = []
        for (i, r) in self.iter_selected():
            books = r[1].strip()
            if self._isModule(books):
                jobs.append((r, books))     # a module is printed from its file name
                continue
            refs, err = parseBookList(books)
            if err is not None or not len(refs):
                skipped.append("{}: {}".format(r[0], err or _("No books specified")))
            else:
                jobs.append((r, refs))
        if len(skipped):
            msg = "\n".join(skipped)
            if not len(jobs):
                self.view.doError(_("None of the selected publications can be printed"), secondary=msg)
                return
            if not self.view.msgQuestion(_("Some publications have invalid books"),
                        msg + "\n\n" + _("These will be skipped. Print the other publications anyway?")):
                return
        self.printing = True
        btn.set_sensitive(False)
        # not the page filler's pool: starting a fill would stop these, and their progress would mix
        if getattr(self.view, 'pubprint', None) is None:
            numproc = int(self.view.get("s_maxproc"))
            self.view.pubprint = MultiPrint(numproc=numproc, progress=False)     # (nothing reads its progress)
        for (r, books) in jobs:
            pid = r[6]
            pvars = {}
            for cr in r.iterchildren():
                pvars[cr[5]] = cr[1]
            bparms = BuildParams(
                prjtree = self.view.prjTree,
                config = self.view.userconfig,
                macrosdir = self.view.scriptsdir,
                scriptsdir = self.view.scriptsdir,
                args = self.view.args,
                restart = False,
                pid = self.view.project.prjid,
                guid = self.view.project.guid,
                cfgid = self.view.cfgid,
                setupfn = printSetup,       # must be module global
                setupargs = pvars,
                pubid = pid)
            self.view.pubprint.submit_print_job(books, bparms)
        w = self.builder.get_object("btn_pubPrint")
        w.get_style_context().add_class("active")
        self._progress_watch_id = GLib.timeout_add(1000, self._pollProgress)

    def _pollProgress(self):
        if self.view.pubprint.is_finished():
            self.printing = False
            pbutton = self.builder.get_object("btn_pubPrint")
            pbutton.get_style_context().remove_class("active")
            self._updateStatus()
            # each is (books, worker, res, ...): res 0 is printed (False is a failed job, and False == 0)
            results = self.view.pubprint.get_results()
            failed = [str(r[0]) for r in results if not (len(r) > 2 and type(r[2]) is int and r[2] == 0)]
            if len(failed):
                self.view.doError(_("Some publications failed to print"),
                                  secondary=_("Failed: {}").format(", ".join(failed)))
            # Show the user where the publication PDFs were created
            startfile(self.view.project.printPath(None))
            return GLib.SOURCE_REMOVE
        return GLib.SOURCE_CONTINUE
