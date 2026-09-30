import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Pango
from usfmtc.reference import RefList
from ptxprint.utils import BuildParams, bookcodes, _
from ptxprint.multiprint import MultiPrint

def printSetup(view, args):
    print(args)
    for k, v in args.items():
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
        self._updateStatus()

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
        return res

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
                    val = self.view.pubvars.get(col, "")
                self.ts.append(parent_iter, self._childRow(col, val, pid))
        if len(self.ts) < 6:
            self.tv.expand_all()
        self._updateStatus()

    def save(self):
        """ Returns a new publications dictionary from the self.ts """
        self.ts = self.builder.get_object("ts_publications")
        res = {}
        for row in self.ts:
            currpid = row[0]
            res.setdefault(currpid, {})['__books'] = row[1]
            res[currpid]['__select'] = 'true' if row[2] else 'false'
            for crow in row.iterchildren():
                # don't use crow[6] since it may be out of date
                res[currpid][crow[5]] = crow[1]
        return res

    def iter_selected(self):
        for i, r in enumerate(self.ts):
            if r[2]:
                yield (i, r)

    def _checkBooks(self, books):
        """ Returns (foreground colour, tooltip markup) for a books value """
        books = books.strip()
        if not books:
            return (ERRORCOL, GLib.markup_escape_text(_("No books specified. Click here to enter "
                                        "a list of books, e.g. 'RUT JON' or 'MAT-JHN'.")))
        try:
            bks = [r.book for r in RefList(books, bookranges=True)]
        except SyntaxError:
            if os.path.isfile(books) or (getattr(self.view.project, "path", None) is not None
                                         and os.path.isfile(os.path.join(self.view.project.path, books))):
                return (NORMALCOL, None)        # a module file
            return (ERRORCOL, GLib.markup_escape_text(_("'{}' is not a valid list of books, "
                                        "nor an existing module file.").format(books)))
        bad = [b for b in bks if b not in bookcodes]
        if len(bad):
            return (ERRORCOL, GLib.markup_escape_text(_("Unknown book code(s): {}").format(" ".join(bad))))
        return (NORMALCOL, None)

    def _uniquePid(self, base):
        existing = set(r[0] for r in self.ts)
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
        return parent if parent is not None else titer

    def _selectAndShow(self, titer):
        path = self.ts.get_path(titer)
        self.tv.expand_row(path, False)
        self.tv.get_selection().select_iter(titer)
        self.tv.scroll_to_cell(path, None, False, 0, 0)

    def _updateStatus(self):
        total = len(self.ts)
        chosen = sum(1 for r in self.ts if r[2])
        if total == 0:
            msg = _("No publications yet. Click 'Add' to create one.")
        else:
            msg = _("{} of {} publications selected for printing").format(chosen, total)
            nbad = sum(1 for r in self.ts if r[8] == ERRORCOL)
            if nbad:
                msg += "  " + _("({} with invalid books)").format(nbad)
        self.builder.get_object("l_pubStatus").set_text(msg)
        self.cb_all.set_inconsistent(0 < chosen < total)
        self.cb_all.set_active(total > 0 and chosen == total)
        self.builder.get_object("btn_pubPrint").set_sensitive(chosen > 0 and not self.printing)
        hascurr = self._currentParent() is not None
        for w in ("btn_pubDuplicate", "btn_pubDel"):
            self.builder.get_object(w).set_sensitive(hascurr)

    def onPubAdd(self, btn):
        pid = self._uniquePid(_("New publication"))
        parent_iter = self.ts.append(None, self._parentRow(pid, "", False))
        for k in self._publishableKeys():
            self.ts.append(parent_iter, self._childRow(k, self.view.pubvars.get(k, ""), pid))
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
        newval = not all(r[2] for r in self.ts)
        for r in self.ts:
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
        new_val = not self.ts[titer][2]
        self.ts[titer][2] = new_val
        self._updateStatus()

    def onPubEdited(self, widget, path, new_text):
        titer = self.ts.get_iter(path)
        if widget is self.builder.get_object("cr_pub_field"):
            new_text = new_text.strip()
            if not new_text or new_text == self.ts[titer][0]:
                return
            if any(r[0] == new_text for r in self.ts):
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
        self.save()
        self.printing = True
        btn.set_sensitive(False)
        if getattr(self.view, 'mprint', None) is None:
            numproc = int(self.view.get("s_maxproc"))
            self.view.mprint = MultiPrint(numproc=numproc, progress=True)
        for (i, r) in self.iter_selected():
            pid = r[6]
            try:
                books = RefList(r[1], bookranges=True)
            except SyntaxError:
                books = [r[1]]      # treat as a module
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
            self.view.mprint.submit_print_job(books, bparms)
        w = self.builder.get_object("btn_pubPrint")
        w.get_style_context().add_class("active")
        self._progress_watch_id = GLib.timeout_add(1000, self._pollProgress)

    def _pollProgress(self):
        if self.view.mprint.is_finished():
            self.printing = False
            pbutton = self.builder.get_object("btn_pubPrint")
            pbutton.get_style_context().remove_class("active")
            self._updateStatus()
            return GLib.SOURCE_REMOVE
        return GLib.SOURCE_CONTINUE
