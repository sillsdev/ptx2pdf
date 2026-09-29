import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from usfmtc.reference import RefList
from ptxprint.utils import BuildParams
from ptxprint.multiprint import MultiPrint

def printSetup(view, args):
    print(args)
    for k, v in args.items():
        view.setvar(k, v)

class PublicationsView:

    _methods = """onPubAdd onPubDel onPubPrint onPubSelect onPubEdited
               """.split()

    def __init__(self, view):
        self.view = view
        self.builder = view.builder
        self.view.register(self, self._methods)
        self.count = 0
        self.ts = self.builder.get_object("ts_publications")

    def load(self, data: dict):
        selected_keys = ['maintitle', 'subtitle']
        selected_keys.extend([k for k,v in self.view.pubvars_publishable.items()
                                    if k not in selected_keys and v])
        # TreeStore layout:
        # 0: label (str)       -> "Field" column text (blank-ish on parent rows)
        # 1: value_text (str)  -> "Value" column text (blank on parent rows)
        # 2: select (bool)     -> "Select" column, meaningful only on parent rows
        # 3: is_parent (bool)  -> controls visibility of Select toggle / editability
        # 4: editable (bool)   -> whether the key text renderer can be edited (for the pid)
        # 5: col_key (str)     -> underlying data column name (child rows only)
        # 6: row_key (str)     -> key into `data` for the publication (set on both)
        self.ts.clear()
        for pid, pub in sorted(self.view.publications.items()):
            select_bool = pub.get("__select", "0").lower() == "true"
            parent_iter = self.ts.append(None, [pid, pub.get("__books", ""), select_bool, True,
                                                    True, "__books", pid]) 
            for col in selected_keys:
                val = pub.get(col)
                if val is None:
                    val = self.view.pubvars.get(col, "")
                self.ts.append(parent_iter, [col, str(val), False, False, False, col, pid])
        if len(self.ts) < 6:
            self.builder.get_object("tv_publications").expand_all()

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

    def onPubAdd(self, btn):
        selected_keys = ['maintitle', 'subtitle']
        selected_keys.extend([k for k,v in self.view.pubvars_publishable.items()
                                    if k not in selected_keys and v])
        self.count += 1
        pid = f"pub_{self.count}"
        parent_iter = self.ts.append(None, [pid, "", False, True, True, "__books", pid])
        for k in selected_keys:
            self.ts.append(parent_iter, [k, self.view.pubvars.get(k, ""), False, False, False, k, pid])

    def onPubDel(self, btn):
        for i, r in reversed(self.iter_selected()):
            self.ts.remove(r.iter)

    def onPubSelect(self, btn, path):
        titer = self.ts.get_iter(path)
        new_val = not self.ts[titer][2]
        self.ts[titer][2] = new_val

    def onPubEdited(self, widget, path, new_text):
        titer = self.ts.get_iter(path)
        if widget is self.builder.get_object("cr_pub_field"):
            print(f"pid change to {new_text} for {path}")
            self.ts[titer][0] = new_text
            self.ts[titer][6] = new_text
        else:   
            print(f"{self.ts[titer][0]} change to {new_text} for {path}")
            self.ts[titer][1] = new_text

    def onPubPrint(self, btn):
        self.save()
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
                setupargs = pvars)
            self.view.mprint.submit_print_job(books, bparms)
        w = self.builder.get_object("btn_pubPrint")
        w.get_style_context().add_class("active")
        self._progress_watch_id = GLib.timeout_add(1000, self._pollProgress)

    def _pollProgress(self):
        if self.view.mprint.is_finished():
            pbutton = self.builder.get_object("btn_pubPrint")
            pbutton.set_sensitive(True)
            pbutton.get_style_context().remove_class("active")
            return GLib.SOURCE_REMOVE
        return GLib.SOURCE_CONTINUE
