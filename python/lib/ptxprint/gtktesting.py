
import gi
gi.require_version("Gtk", '3.0')
from gi.repository import Gtk, Gdk, GObject, GLib
import os, sys, zipfile, json, tempfile, traceback, time, shutil, subprocess, random
from io import StringIO
from configparser import ConfigParser
from difflib import context_diff
from pathlib import Path
from glob import glob

from ptxprint.usxutils import simple_parse
from ptxprint.utils import _
from ptxprint.project import Project, ProjectDir


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return super().default(obj)

# The signals recorded, and the widget classes they are recorded for
_signals = {
    'clicked': ("Button",),
    'changed': ("ComboBox", "Entry", "TreeSelection"),
    'color-set': ("ColorButton",),
    'change-current-page': ("Notebook",),
    'switch-page': ("Notebook",),       # clicking a tab
    'value-changed': ("SpinButton",),
    # 'state-set': ("Switch",),
    'row-activated': ("TreeView",),
}

def _picKey(row, model=None):
    """ A picture's anchor, e.g. "JON 1.3", with its image ("JON 1.3|oi00185.jpg") if another
        picture in the list has the same anchor """
    if model is not None and sum(1 for r in model if r[0] == row[0]) > 1:
        return f"{row[0]}|{row[2]}"
    return row[0]

def _picKeys(view, sel):
    model, paths = sel.get_selected_rows()
    return [_picKey(model[p], model) for p in paths]

def _picRows(view, keys):
    """ The picture list's rows (in its filtered model) for these keys. Each key takes the next row
        that matches it, since even anchor and image together needn't be unique. """
    model = view.picListView.model
    used = set()
    res = []
    for k in keys:
        anchor, _, src = k.partition("|")
        for r in model:
            if r[0] == anchor and (not src or r[2] == src) and r.path.to_string() not in used:
                used.add(r.path.to_string())
                res.append(r.iter)
                break
        else:
            raise ValueError(f"There is no picture {k} in the list (is it filtered out?):"
                             f" {', '.join(_picKey(r, model) for r in model)}")
    return res

# Lists whose selection is recorded and replayed: how to name the selected rows, and find them again
_selectables = {"tv_picListEdit": _picKeys}
_selectableRows = {"tv_picListEdit": _picRows}

def testsDir(project, cfgid):
    """ Where a project's tests for a config live: <project>/shared/tests/<config> """
    res = os.path.join(project.path, "shared", "tests", cfgid or "Default")
    os.makedirs(res, exist_ok=True)
    return res

def testLocation(fname):
    """ (project dir, config) for a test kept in <project>/shared/tests/<config>/, else None """
    cfgdir = os.path.dirname(os.path.abspath(fname))
    testsdir = os.path.dirname(cfgdir)
    shared = os.path.dirname(testsdir)
    if os.path.basename(testsdir) != "tests" or os.path.basename(shared) != "shared":
        return None
    return (os.path.dirname(shared), os.path.basename(cfgdir))

# Replays watching dialogs. A dialog that is run again after it answered (asking until the
# answers are acceptable) is waiting for a person again, so they must forget its answer.
_replays = []
_dialogRun = Gtk.Dialog.run

def _runDialog(dlg, *a, **kw):
    for r in _replays:
        r.responded.discard(dlg)
    return _dialogRun(dlg, *a, **kw)

Gtk.Dialog.run = _runDialog

class GtkTester:
    def __init__(self, fname, view, full_archive=False, lean=False):
        self.fname = fname
        self.view = view
        self.events = []
        self.currid = None
        self.startid = None     # where the test starts: the project and config when the first event happened
        self.others = set()     # other projects the test needs (e.g. the other side of a diglot)
        self.usedids = set()
        self.projects = {}
        self.paused = False
        self.lastevent = None
        self.errors = []
        self.skipped = []
        self.full_archive = full_archive
        # A lean recording holds just the actions and the files they changed, not the project.
        # Replaying it starts from a copy of the same project, found with -p.
        self.makelean = lean
        self.setid(view.project, view.cfgid)
        self.lean = False
        if self.full_archive:
            self.base = self.takeSnapshot()
            self.zip = self.base is not None
        else:
            self.zip = None

    @classmethod
    def recordFromUser(cls, view):
        """ Ask where to save a test recording and start it. Returns the tester, or None """
        zip_file = view.fileChooser(_("Select the location and name for the test archive file"),
                filters={"ZIP files": {"pattern": "*.zip", "mime": "application/zip"}},
                multiple=False, folder=False, save=True,
                basedir=testsDir(view.project, view.cfgid))
        if zip_file is None:
            return None
        res = cls(str(zip_file[0]), view, full_archive=True)
        res.startRecording()
        return res

    def startRecording(self):
        random.seed(0)          # e.g. random picture positions: so that a replay makes the same ones
        self.ownwindows = set()
        self.uilevel = self.view.uilevel        # the highest view level used while recording
        self.recordcontrol = RecordControl(self)
        self.starttime = time.time()
        self.hook_ids = []
        for k, v in _signals.items():
            for w in v:
                o = getattr(Gtk, w)
                hook_id = GObject.add_emission_hook(o, k, self.emission_hook, k)
                self.hook_ids.append((o, k, hook_id))
        self._wrapFileChooser(record=True)

    def stopRecording(self):
        for obj, signal_name, hook_id in getattr(self, 'hook_ids', []):
            GObject.remove_emission_hook(obj, signal_name, hook_id)
        self.hook_ids = []
        self.view.__dict__.pop('fileChooser', None)
        if getattr(self, 'recordcontrol', None) is not None:
            self.recordcontrol.close()
            self.recordcontrol = None

    def _wrapFileChooser(self, record=False):
        """ A file chooser is not a widget in the builder, so what was chosen is an event of its
            own: ["", "choose", path, ...], with no paths for Cancel. Paths in the project are kept
            relative to it, so the replay picks the same file in its copy of the project. A replay
            queues the answer and the next file chooser gives it without showing a dialog. """
        orig = type(self.view).fileChooser.__get__(self.view)
        self.choices = []
        def chooser(*a, **kw):
            # a replay running while this records (as mkguitest does) gives the answer
            replaying = [r for r in _replays if r is not self or not record]
            if replaying:
                for r in replaying:
                    if r.choices:
                        res = r.choices.pop(0)
                        break
                else:
                    raise ValueError("A file chooser opened with no choose event before it")
                if not record:
                    return res
            else:
                res = orig(*a, **kw)
            prjdir = os.path.abspath(self.view.project.path)
            paths = []
            for f in (res or []):
                f = os.path.abspath(str(f))
                paths.append(os.path.relpath(f, prjdir).replace("\\", "/") if f.startswith(prjdir + os.sep) else f)
            # the click that opened the chooser is already recorded: the answer must come before it
            i = len(self.events)
            while i > 0 and self.events[i-1][1] != "signal":
                i -= 1
            self.events.insert(max(i-1, 0), ["", "choose"] + paths)
            self.lastevent = None
            return res
        self.view.fileChooser = chooser

    def _choose(self, w, *paths):
        if not len(paths):
            self.choices.append(None)
        else:
            prjdir = self.view.project.path
            self.choices.append([Path(p if os.path.isabs(p) else os.path.join(prjdir, p)) for p in paths])
        return False

    def addNote(self, text, widget=""):
        """ A note for someone stepping through the test, e.g. as a tutorial. Replays ignore it. """
        text = text.strip()
        if text:
            self.events.append([widget or "", "note", text])
            self.lastevent = None

    def emission_hook(self, w, *a):     # sigid, detail, self, *a):
        if isinstance(w, Gtk.TreeSelection):
            return self.selectionChanged(w)
        if self.paused or w.get_toplevel() in getattr(self, 'ownwindows', ()):
            return True
        sigid = a[-1]
        name = Gtk.Buildable.get_name(w)
        if name is None or name.startswith("___object_"):
            # Unnamed widgets get builder numbers that change between runs. The entry inside a
            # combo box is recorded as the combo; anything else can't be replayed, so skip it.
            p = w.get_parent()
            pname = Gtk.Buildable.get_name(p) if p is not None else None
            if isinstance(p, Gtk.ComboBox) and pname is not None and not pname.startswith("___object_"):
                name = pname
            else:
                return True
        if not self.userInitiated(w):
            return True
        val = self.view.get(name, skipmissing=True)
        self.uilevel = max(getattr(self, 'uilevel', 0), self.view.uilevel)
        self.addEvent(name, sigid, time.time() - self.starttime, val, a[:-1])
        return True

    def selectionChanged(self, sel):
        """ Picking rows in a list someone can select from: record what is selected, by the rows'
            keys (row paths change with the list's filter and contents). Ctrl-clicking more rows
            changes the selection several times, so keep just the last. """
        tv = sel.get_tree_view()
        name = Gtk.Buildable.get_name(tv) if tv is not None else None
        keyfn = _selectables.get(name, None)
        if self.paused or keyfn is None or not self.userInitiated(tv):
            return True
        e = (name, "select") + tuple(keyfn(self.view, sel))
        if self.events and self.lastevent is not None and self.events[-1] is self.lastevent \
                and self.lastevent[:2] == e[:2]:
            self.events.pop()
        self.events.append(e)
        self.lastevent = e
        return True

    def _select(self, w, *keys):
        rows = _selectableRows[w](self.view, keys)
        def doit():
            sel = self.view.builder.get_object(w).get_selection()
            sel.unselect_all()
            for it in rows:
                sel.select_iter(it)
        self._later(doit)
        return True

    def userInitiated(self, w):
        """ Whether the user did this, rather than PTXprint reacting to something (another
            widget's handler, a timer, loading a config). GTK knows which input event it is
            handling, even inside a handler or a dialog's own loop: keep the change only if that
            event was aimed at this widget. """
        ev = Gtk.get_current_event()
        if ev is None:
            return False        # a timer or idle callback
        ew = Gtk.get_event_widget(ev)
        if ev.get_event_type() in (Gdk.EventType.KEY_PRESS, Gdk.EventType.KEY_RELEASE):
            win = ew.get_toplevel() if ew is not None else None
            focus = win.get_focus() if isinstance(win, Gtk.Window) else None
            if focus is not None and (focus is w or focus.is_ancestor(w)):
                self.lasttyped = w
                return True
            # a button pressed from the keyboard: Enter for a dialog's default, Space, a mnemonic
            return isinstance(w, Gtk.Button)
        if w is getattr(self, 'lasttyped', None):
            return True         # e.g. a spin button taking what was typed as it loses focus
        if ew is None:
            return False
        # a choice from a drop-down list is a click in a menu attached to the combo box
        p = ew
        while p is not None and not isinstance(p, Gtk.Menu):
            p = p.get_parent()
        if p is not None and p.get_attach_widget() is not None:
            ew = p.get_attach_widget()
        return ew is w or ew.is_ancestor(w)

    def addEvent(self, w, signal, t, val, a):
        ''' events are widget, type="signal", signal, parms; type="set", val '''
        if self.paused:
            return
        e = None
        if w is None or w in ("button",):
            return
        if val is not None and not w.startswith("btn_"):
            if w.startswith("r_") and not val:
                return          # the radio button turned off when another was picked
            e = (w, 'set', val)
            # A SpinButton is also an Entry, so one change emits both value-changed and changed
            if e == self.lastevent:
                e = None
            elif self.events and self.lastevent is not None and self.events[-1] is self.lastevent \
                    and self.lastevent[0] == w and self.lastevent[1] == 'set':
                self.events.pop()       # typing, or clicking a spin button up: keep the final value
            if self.currid is not None and self.currid not in self.usedids:
                self.usedids.add(self.currid)
        elif (m := getattr(self, "s_"+signal.replace("-", ""), None)) is not None:
            e = m(w, signal, t, val, *a)
        else:
            parms = []
            e = (w, 'signal', signal, *[str(x) for x in a])
        if e is not None:
            # print(e)
            self.others.update(otherProjects(self.view))
            self.events.append(e)
            self.lastevent = e

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def setid(self, project, cfgid):
        self.currid = (project, cfgid)
        if not self.events:
            self.startid = self.currid

    def finalise(self):
        self.stopRecording()
        if not self.zip or self.paused:
            return
        project, cfgid = self.startid or self.currid
        self.pause()
        if not self.full_archive:
            # not implemented right now, but here it could be possible to have a more minimal test eg comparing only cfg files
            raise NotImplementedError
        final_files = self.takeSnapshot() or {}
        testdir = "{}/test/".format(project.prjid)
        with zipfile.ZipFile(self.fname, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            if not self.makelean:
                for name, content in sorted(self.base.items()):
                    zf.writestr(name, content)
            for name, content in sorted(final_files.items()):
                if self.base.get(name) != content:
                    zf.writestr(testdir + "modified_files/" + name, content)
            deleted_files = sorted(n for n in self.base if n not in final_files)
            zf.writestr(testdir + "deleted_files.txt", "\n".join(deleted_files))
            info = {"events": self.events,
                    "uilevel": getattr(self, 'uilevel', self.view.uilevel),
                    "project": project.prjid, "config": cfgid}
            others = sorted((self.others | set(otherProjects(self.view))) - {project.prjid})
            if others:
                info["projects"] = others
            events = json.dumps(info, ensure_ascii=False, indent=4, cls=CustomJSONEncoder)
            zf.writestr(testdir + "events.json", events)
        self.zip = None

    def setuprun(self, fname, view):
        self.pause()
        if fname is not None:
            self.fname = os.path.abspath(fname)
        self.runevents, self.runuilevel, self.runextra = readActions(fname)
        self.runeventidx = 0
        # A lean test holds only its actions and the files they changed: the state they changed
        # is that of the project at the start of the replay
        with zipfile.ZipFile(self.fname) as zf:
            self.lean = all("/test/" in n for n in zf.namelist() if not n.endswith("/"))

    @staticmethod
    def tidyEvents(events):
        """ What the recorder now does as it goes: one step for repeated changes to a widget
            (typing a name, clicking a spin button up), and no radio button turning off """
        res = []
        for e in events:
            if e[1] == "set" and e[0].startswith("r_") and not e[2]:
                continue
            if e[1] == "set" and res and res[-1][1] == "set" and res[-1][0] == e[0]:
                res[-1] = e
            else:
                res.append(e)
        return res

    def saveTutorial(self, fname):
        """ Save the (edited) actions as a tutorial: just the events, to run on any project """
        events = self.tidyEvents(self.runevents)
        with open(fname, "w", encoding="utf-8") as outf:
            # keep anything else that was in the file, e.g. a title someone added by hand
            res = dict(getattr(self, 'runextra', None) or {})
            res["events"] = events
            if getattr(self, 'runuilevel', None):
                res["uilevel"] = self.runuilevel
            json.dump(res, outf, ensure_ascii=False, indent=4)
        return len(self.runevents) - len(events)

    def ensureLevel(self):
        """ The user's view must show at least what the actions use: raise it if it is lower.
            Returns a message saying what changed, or None. """
        self.oldlevel = None
        self.levelmsg = None
        need = getattr(self, 'runuilevel', None)
        if need and self.view.uilevel < need:
            self.oldlevel = self.view.uilevel
            self.view.set_uiChangeLevel(need)
            self.levelmsg = _("Switched to {} for this, as it needs controls your view didn't show.").format(
                                levelName(self.view, need))
        return self.levelmsg

    def restoreLevel(self):
        if getattr(self, 'oldlevel', None):
            self.view.set_uiChangeLevel(self.oldlevel)
            self.oldlevel = None

    @classmethod
    def tutorialFromUser(cls, view):
        fname = view.fileChooser(_("Choose a tutorial to step through"),
                filters={"Tutorials and tests": {"patterns": ["*.json", "*.zip"]}},
                multiple=False, folder=False)
        if fname is not None:
            cls.runTutorial(view, str(fname[0]))

    @classmethod
    def runTutorial(cls, view, fname):
        """ Step through the actions in fname on the current project: no archive, no comparison """
        if getattr(view, 'replayer', None) is not None:
            view.doStatus(_("A tutorial or test is already running."), warning=True)
            return None
        try:
            events, uilevel, extra = readActions(fname)
        except (OSError, ValueError, KeyError, StopIteration, zipfile.BadZipFile) as e:
            view.doStatus(_("Can't read the tutorial {}: {}").format(fname, e), warning=True)
            return None
        res = cls(None, view)
        res.fname = os.path.abspath(fname)
        res.tutorial = True
        res.runevents = events
        res.runuilevel = uilevel
        res.runextra = extra
        res.runeventidx = 0
        res.startReplayHooks()
        view.replayer = res
        res.ensureLevel()
        res.control = ReplayControl(res, 0)
        return res

    def run_action(self, noclose, step=None):
        """ Replay the events. With step (seconds between events, 0 to wait for the Step button)
            show a control window and highlight each widget before acting on it. """
        if self.runeventidx == 0 and getattr(self, 'lean', False) and getattr(self, 'base', None) is None:
            self.base = self.takeSnapshot()
        if self.runeventidx == 0 and not hasattr(self, 'oldlevel'):
            self.ensureLevel()
        if step is not None:
            self.control = ReplayControl(self, step)
            return False
        if not self.ready():
            GLib.timeout_add(20, self.run_action, noclose)
            return False
        while self.runeventidx < len(self.runevents):
            e = self.runevents[self.runeventidx]
            # print(f"{self.runeventidx}: {e}")
            self.runeventidx += 1
            try:
                goround = self._replay(e)
            except Exception as ex:     # an exception here would stop the idle loop and hang the app
                self.errors.append(f"{self.runeventidx-1}: {e}: {type(ex).__name__}: {ex}\n" + traceback.format_exc())
                goround = False
            if goround:     # come back after the signal has run, even after the last event
                GLib.idle_add(self.run_action, noclose)
                return False
        self.finishReplay()
        if not noclose:
            self.view.onDestroy(None)
        return False

    def finishReplay(self):
        """ Take the result the same way recording does: an in memory archive of the UI state,
            made before the window is torn down (a replayed close button gets here via onDestroy). """
        if getattr(self, 'snapshot', None) is None and not getattr(self, 'tutorial', False):
            self.snapshot = self.takeSnapshot()

    def closing(self):
        """ PTXprint is closing (perhaps the last step was Quit) """
        self.finishReplay()
        control = getattr(self, 'control', None)
        if control is not None and control.edited:
            control.offerSave()

    def takeSnapshot(self):
        try:
            data = self.view.createArchive(in_memory=True, for_test=True, nobuild=True)
            self.view.zf.close()
        except Exception as ex:
            self.errors.append(f"Creating the result archive: {type(ex).__name__}: {ex}\n" + traceback.format_exc())
            return None
        with zipfile.ZipFile(data) as zf:
            res = {n: zf.read(n) for n in zf.namelist() if not n.endswith("/")}
        # The piclist a print makes from the config's one, with what printing does to it (positions,
        # disabled and non-print pictures dropped, copied file names). It is the only file in local/
        # that a test compares, and is there only if the test printed.
        prj = self.view.project
        if prj is not None and self.view.cfgid is not None:
            for f in sorted(glob(os.path.join(prj.printPath(self.view.cfgid), "*.piclist"))):
                with open(f, "rb") as inf:
                    res["/".join([prj.prjid] + list(Path(os.path.relpath(f, prj.path)).parts))] = inf.read()
        return res

    def replayOne(self):
        """ Replay the next event. Returns whether there are more. """
        e = self.runevents[self.runeventidx]
        self.runeventidx += 1
        try:
            self._replay(e)
        except Exception as ex:
            self.errors.append(f"{self.runeventidx-1}: {e}: {type(ex).__name__}: {ex}\n" + traceback.format_exc())
            print(self.errors[-1])
        return self.runeventidx < len(self.runevents)

    def skipOne(self):
        """ Move past the next event without replaying it. Returns whether there are more. """
        e = self.runevents[self.runeventidx]
        if e[1] not in ("note", "comment"):     # skipping these changes nothing
            self.skipped.append(f"{self.runeventidx}: {self.describe(e)}")
        self.runeventidx += 1
        return self.runeventidx < len(self.runevents)

    def eventWidget(self, e):
        w = self.view.builder.get_object(e[0])
        if e[0] == "tv_Styles":
            return w
        return w if isinstance(w, Gtk.Widget) else None

    def widgetLabel(self, name):
        """ What a user sees the widget called: its own label, a label pointing at it, or its tooltip """
        w = self.view.builder.get_object(name) if name else None
        if not isinstance(w, Gtk.Widget):
            return name
        txt = None
        if isinstance(w, Gtk.Button):
            txt = w.get_label()
            if txt and txt.startswith("gtk-"):     # a stock label, e.g. gtk-save-as
                txt = txt[4:].replace("-", " ").title()
        if not txt:
            labels = w.list_mnemonic_labels()
            if labels:
                txt = labels[0].get_text()
        if not txt:
            txt = self._neighbourLabel(w)
        if not txt:
            tip = w.get_tooltip_text()
            if tip:
                txt = tip.strip().split("\n")[0]
                if len(txt) > 60:
                    txt = txt[:57] + "..."
        if not txt:
            return name
        return " ".join(txt.replace("_", "").split()).rstrip(":.")

    @staticmethod
    def _textOf(c):
        """ The text a label-like widget shows: a label, a label inside an event box (the
            click-to-reset labels), or a check button labelling the widget beside it """
        if isinstance(c, Gtk.Label):
            return c.get_text().strip() or None
        if isinstance(c, Gtk.CheckButton):
            return (c.get_label() or "").strip() or None
        if isinstance(c, Gtk.EventBox):
            ch = c.get_child()
            return ch.get_text().strip() or None if isinstance(ch, Gtk.Label) else None
        return None

    @classmethod
    def _neighbourLabel(cls, w):
        """ The label just before w in its grid row or box, as it is usually laid out """
        p = w.get_parent()
        if isinstance(p, Gtk.Grid):
            top = p.child_get_property(w, "top-attach")
            left = p.child_get_property(w, "left-attach")
            best = None
            for c in p.get_children():
                if c is w or p.child_get_property(c, "top-attach") != top:
                    continue
                cl = p.child_get_property(c, "left-attach")
                if cl < left and (best is None or cl > best[0]):
                    txt = cls._textOf(c)
                    if txt:
                        best = (cl, txt)
            return best[1] if best else None
        elif isinstance(p, Gtk.Box):
            prev = None
            for c in p.get_children():
                if c is w:
                    break
                prev = c
            return cls._textOf(prev) if prev is not None else None
        return None

    def describe(self, e):
        """ The event in words a learner can follow """
        if e[1] in ("note", "comment"):
            return e[2]
        label = self.widgetLabel(e[0])
        if e[1] == "set":
            if isinstance(e[2], bool):
                return f"{'Tick' if e[2] else 'Untick'} {label}"
            return f"{label}: set to {e[2]}"
        elif e[1] == "signal" and e[2] == "clicked":
            return f"Click {label}"
        elif e[1] == "signal":
            return f"{label}: {e[2]}"
        elif e[1] == "rowactivated" and len(e) > 4:
            return f"Select the style {e[4]}"
        elif e[1] == "select":
            return _("Select {}").format(", ".join(e[2:])) if len(e) > 2 else _("Select nothing")
        elif e[1] == "choose":
            return _("In the file chooser, pick {}").format(", ".join(e[2:])) if len(e) > 2 else _("Cancel the file chooser")
        return f"{label}: {' '.join(str(x) for x in e[1:])}"

    def _note(self, w, *a):
        return False

    def _comment(self, w, *a):
        """ A comment for whoever edits the test or tutorial: never shown, never replayed """
        return False

    def quietErrors(self):
        """ During a replay nobody is there to close an error message: note it and carry on.
            Awkward clicks are meant to bring some of these up. """
        self.messages = []
        def doError(txt, threaded=False, secondary=None, **kw):
            msg = txt + (f" ({secondary})" if secondary else "")
            idx = getattr(self, 'runeventidx', 0)
            self.messages.append((idx - 1, msg))
            print(f"Message at event {idx-1}: {msg}")
        self.view.doError = doError

    def handlerError(self, tp, value, tb):
        """ Takes the place of the view's sys.excepthook during a replay: an exception in a
            handler is a test failure, not an error dialog that nobody is there to close """
        msg = f"{self.runeventidx-1}: {self.runevents[self.runeventidx-1] if self.runeventidx else ''}: " \
              + "".join(traceback.format_exception(tp, value, tb))
        self.errors.append(msg)
        print(msg)

    def _later(self, fn, *a):
        """ Emit a recorded signal from its own idle callback. A handler that runs a modal dialog
            blocks until the dialog closes, and the replay must carry on inside the dialog's loop,
            which it can't from a callback that is still running. """
        def doit():
            self.responded = set()
            mine = self.openDialogs()       # dialogs open before this signal
            self.inflight.append(mine)
            try:
                fn(*a)
            except Exception as ex:
                self.errors.append(f"{fn}{a}: {type(ex).__name__}: {ex}\n" + traceback.format_exc())
            finally:
                self.inflight.remove(mine)
            return False
        GLib.idle_add(doit)

    def startReplayHooks(self):
        """ Watch dialogs answering, so the replay knows when it is waiting on a person (see ready) """
        self.inflight = []
        self.responded = set()
        GObject.add_emission_hook(Gtk.Dialog, "response", self._dialogResponded)
        _replays.append(self)
        self._wrapFileChooser()

    def _dialogResponded(self, dlg, *a):
        self.responded.add(dlg)
        return True

    @staticmethod
    def openDialogs():
        return set(w for w in Gtk.Window.list_toplevels() if isinstance(w, Gtk.Dialog) and w.get_visible())

    def ready(self):
        """ Whether the next event can be replayed: every signal still being handled is
            waiting in a dialog it opened, so the events that follow belong to that dialog.
            Once the dialog has answered, wait for its handler to finish. """
        from ptxprint.runjob import isLocked
        if isLocked():
            return False        # wait for a print to finish
        inflight = getattr(self, 'inflight', [])
        if not inflight:
            return True
        waiting = self.openDialogs() - self.responded
        return all(waiting - before for before in inflight)

    def _replay(self, e):
        """ Replay one event. Returns True if it was emitted later, so callers come back after it """
        if getattr(self, 'runeventidx', 0) <= 1:
            random.seed(0)      # as recording does when it starts
        w = e[0]
        if e[1] in ("set", "signal"):
            widget = self.view.builder.get_object(w)
            if isinstance(widget, Gtk.Widget) and not widget.is_sensitive():
                raise ValueError(f"{w} is greyed out, so nobody could change it")
        if e[1] == "set":
            # later, like a signal: setting a checkbox can run a handler that asks in a dialog,
            # and the events that answer it must be able to run
            self._later(self._set, w, e[2])
            return True
        if e[1] == "signal":
            widget = self.view.builder.get_object(w)
            if widget is None:
                raise KeyError(f"No widget called {w}")
            self._later(widget.emit, e[2], *e[3:])
            return True
        m = getattr(self, "_"+e[1], None)
        if m is None:
            raise KeyError(f"Unknown event type {e[1]}")
        return m(w, *e[2:])

    def _set(self, w, val):
        self.view.set(w, val)
        widget = self.view.builder.get_object(w)
        if isinstance(widget, Gtk.ComboBox) and not widget.get_has_entry() and widget.get_id_column() >= 0 \
                and widget.get_active_id() != str(val):
            ids = [str(r[widget.get_id_column()]) for r in widget.get_model()]
            raise ValueError(f"{w} has no choice {val!r} (it has {', '.join(ids)})")
        if isinstance(widget, Gtk.Entry):      # spin buttons too
            # someone typing moves on to something else, and handlers listen for that
            ev = Gdk.Event.new(Gdk.EventType.FOCUS_CHANGE)
            ev.window = widget.get_window()
            ev.send_event = True
            widget.emit("focus-out-event", ev)
        if w.startswith("col_") and widget is not None:
            # setting a colour button's colour doesn't emit color-set, which is what
            # its handlers listen for (and what the recording saw)
            widget.emit("color-set")

    test_ignores = set(["fonts.conf", "ptxprint_user.cfg", "runtex.sh", "runtex.txt"])

    def run_finalise(self):
        """ Compare the archive taken at the end of the replay with the recorded final state:
            the initial archive with test/modified_files applied and test/deleted_files removed. """
        if getattr(self, 'snapshot', None) is None:
            res = {"test": [], "ref": [], "diff": [], "cfg": [], "sty": []}
            if not self.errors:
                self.errors.append("The replay did not complete")
        else:
            res = self.prepare_diff_report(self.snapshot, self.reference())
        res['errors'] = self.errors
        res['skipped'] = self.skipped
        return res

    def saveSnapshot(self, fname):
        if getattr(self, 'snapshot', None) is None:
            return
        with zipfile.ZipFile(fname, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for k, v in self.snapshot.items():
                zf.writestr(k, v)

    def reference(self):
        if self.fname is not None:
            self.fname = os.path.abspath(self.fname)
        with zipfile.ZipFile(self.fname) as zf:
            names = [n for n in zf.namelist() if not n.endswith("/")]
            testdirs = set(n[:n.index("/test/")+6] for n in names if "/test/" in n)
            if getattr(self, 'lean', False):
                res = dict(getattr(self, 'base', None) or {})
            else:
                res = {n: zf.read(n) for n in names if not any(n.startswith(t) for t in testdirs)}
            for t in testdirs:
                mfiles = t + "modified_files/"
                for n in names:
                    if n.startswith(mfiles):
                        res[n[len(mfiles):]] = zf.read(n)
                if t + "deleted_files.txt" in names:
                    for d in zf.read(t + "deleted_files.txt").decode("utf-8").splitlines():
                        res.pop(d.strip(), None)
        return res

    def prepare_diff_report(self, test, ref):
        """ test and ref are dicts of archive path: contents """
        diff_results = {"test": [], "ref": [], "diff": [], "cfg": [], "sty": []}
        def ignored(n):
            # A config's base/ holds a copy of the config it was made from, as that was on disk.
            # Recording copies the user's own file; a replay copies the archive's rewrite of it.
            # Fonts are whichever files the font names find on the machine making the archive.
            return os.path.basename(n) in self.test_ignores or "/base/" in n or "/shared/fonts/" in n
        diff_results["test"] = sorted(n for n in test if n not in ref and not ignored(n))
        diff_results["ref"] = sorted(n for n in ref if n not in test and not ignored(n))
        for n in sorted(set(test) & set(ref)):
            if ignored(n) or test[n] == ref[n]:
                continue
            if n.endswith('.cfg') or n.endswith('.sty'):
                fref = StringIO(ref[n].decode("utf-8", errors="replace"))
                ftest = StringIO(test[n].decode("utf-8", errors="replace"))
                if n.endswith('.cfg'):
                    diff_results['cfg'].extend(f"{n}: {d}" for d in self.compare_cfg(fref, ftest))
                else:
                    diff_results['sty'].extend(f"{n}: {d}" for d in self.compare_sty(fref, ftest))
            else:
                diff_results["diff"].append(n)
        return diff_results

#### special handlers
    def s_rowactivated(self, w, signal, t, val, p, col, *a):
        tv = self.view.builder.get_object(w)
        coli = tv.get_columns().index(col)
        res = [w, "rowactivated", str(p), str(coli)]
        if w == "tv_Styles":
            # paths depend on the tree's filter and contents, so also record the marker
            model = tv.get_model()
            res.append(model[model.get_iter(p)][0])
        return res

    def _rowactivated(self, w, *a):
        widget = self.view.builder.get_object(w)
        p = Gtk.TreePath.new_from_string(a[0])
        if w == "tv_Styles":
            if len(a) > 2:
                # someone can only pick a style they can see
                if not self.view.styleEditor.selectMarker(a[2]):
                    raise ValueError(f"Style {a[2]} isn't in the list of styles (is it filtered out?)")
            else:
                sel = widget.get_selection()
                sel.select_path(p)
                sel.emit("changed")
        else:
            col = widget.get_columns()[int(a[1])]
            self._later(widget.emit, "row-activated", p, col)
        return True         # we emitted a signal so go round

    def compare_cfg(self, old, new, **kw):
        options_to_ignore = ["gitversion", "config"]
        # other projects aren't in a test archive, so a reference to one can't survive loading
        section_options_to_ignore = {"import": ["project"]}
        res = []
        oldc = ConfigParser()
        oldc.read_file(old)
        newc = ConfigParser()
        newc.read_file(new)
        olds = set(oldc.sections())
        news = set(newc.sections())
        diffs = olds.symmetric_difference(news)
        if len(diffs):
            res.append(f"Differences in sections: {', '.join(sorted(diffs))}")
        for s in olds:
            if s not in news:
                continue
            oldo = set(oldc.options(s))
            newo = set(newc.options(s))
            ignores = options_to_ignore + section_options_to_ignore.get(s, [])
            diffs = oldo.symmetric_difference(newo).difference(ignores)
            if len(diffs):
                res.append(f"Differences in options in section {s}: {', '.join(sorted(diffs))}")
            for o in oldo:
                if o not in newo:
                    continue
                oldv = oldc.get(s, o)
                newv = newc.get(s, o)
                if oldv != newv and o not in ignores:
                    res.append(f"{s}/{o}: {oldv} -> {newv}")
        return res

    def compare_sty(self, old, new, **kw):
        res = []
        olds = simple_parse(old)
        news = simple_parse(new)
        newm = set(news.keys())
        oldm = set(olds.keys())
        diffs = newm.symmetric_difference(oldm)
        if len(diffs):
            res.append(f"Different markers: {', '.join(sorted(diffs))}")
        for m, r in news.items():
            if m not in oldm:
                continue
            o = olds[m]
            newk = set(r.keys())
            oldk = set(o.keys())
            diffs = newk.symmetric_difference(oldk)
            if len(diffs):
                res.append(f"Different fields in marker {m}: {', '.join(sorted(diffs))}")
            for k, v in r.items():
                if k not in o:
                    continue
                if v != o[k]:
                    res.append(f"{m}/{k}: {o[k]} -> {v}")
        return res

    def diffcompare(self, old, new, **kw):
        oldl = old.readlines()
        newl = new.readlines()
        fname = kw.get('filename', "UNK")
        res = context_diff(oldl, newl, fromfile="test/"+fname, tofile="result/"+fname, lineterm="")
        return res

def load_project_from_archive(zf, dir_to_extract=None, projectdirs=None):
    """
    zf is an open zipfile, containing an archive of a project created using the createArchive method
    Will be extracted to dir_to_extract if specified, to a temporary directory if not.
    A lean test archive holds no project, just test/: then the project is copied, so that the
    test never changes the original. The project and config are the ones the test names, found
    in one of projectdirs, or else where the test is kept (<project>/shared/tests/<config>/).
    """
    madedir = not dir_to_extract
    if madedir:
        dir_to_extract = tempfile.mkdtemp(prefix="ptxtest_")
    names = [n for n in zf.namelist() if not n.endswith("/")]
    testconfig = None
    if names and all("/test/" in n for n in names):
        try:
            prjid, testconfig = _copyTestProject(zf, names, dir_to_extract, projectdirs or [],
                                                 testLocation(zf.filename) if zf.filename else None)
        except Exception:
            if madedir:
                shutil.rmtree(dir_to_extract, ignore_errors=True)
            raise
    else:
        zf.extractall(dir_to_extract)
        # The project is the top level directory holding ptxSettings.xml. Take the prjid from the
        # path relative to the extraction dir: an absolute path's depth depends on where TMPDIR is.
        # Paratext projects have Settings.xml, ones PTXprint made have ptxSettings.xml
        prjids = set(p.relative_to(dir_to_extract).parts[0] for a in ("Settings.xml", "ptxSettings.xml")
                        for p in Path(dir_to_extract).glob("*/" + a))
        if len(prjids) != 1:
            if madedir:
                shutil.rmtree(dir_to_extract, ignore_errors=True)
            raise Exception("1 project was expected in the archive but {} were found.".format(len(prjids)))
        prjid = prjids.pop()
    project_dir = ProjectDir(prjid, None, os.path.join(dir_to_extract, prjid))
    project = Project(project_dir)
    project.testconfig = testconfig
    return project

# Outputs and working files a test doesn't need from the project it copies
_ignorefiles = shutil.ignore_patterns("*.pdf", "*.zip", "*.xdv", "*.log", "*.parlocs", "*.delayed",
                                      "*.notepages", "*.picpages", "__pycache__", ".git")

def _copyignores(path, names):
    res = _ignorefiles(path, names)
    # nor the tests kept in the project
    if os.path.basename(os.path.normpath(path)) == "shared" and "tests" in names:
        res.add("tests")
    return res

def copyTestProject(src, dest):
    """ Copy a project for a lean test to run on. In a git checkout (like the test suite's
        projects) only the files git tracks are copied, so that what earlier runs left behind
        in the project doesn't become part of the state the test starts from. """
    try:
        res = subprocess.run(["git", "-C", src, "ls-files", "-z", "--", "."],
                             capture_output=True, check=True)
        tracked = [f for f in res.stdout.decode("utf-8").split("\0") if f]
    except (OSError, subprocess.CalledProcessError):
        tracked = []
    if not tracked:
        shutil.copytree(src, dest, ignore=_copyignores, symlinks=True)
        return
    for f in tracked:
        d, n = os.path.split(f)
        if f.startswith("shared/tests/") or _ignorefiles(os.path.join(src, d), [n]):
            continue
        os.makedirs(os.path.join(dest, d), exist_ok=True)
        shutil.copy2(os.path.join(src, f), os.path.join(dest, f), follow_symlinks=False)

def _copyTestProject(zf, names, todir, projectdirs, location=None):
    """ Copy the project a lean test runs on into todir. The test names its project and config.
        The project is found in projectdirs, or else is the one the test is kept in (location:
        (project dir, config)), which also gives the project and config if the test doesn't.
        Returns (prjid, config) """
    evname = next((n for n in names if n.endswith("/test/events.json")), None)
    data = json.loads(zf.read(evname).decode("utf-8")) if evname is not None else {}
    prjid = data.get("project")
    cfgid = data.get("config")
    if location is not None and (prjid is None or os.path.basename(location[0]) == prjid):
        prjid = os.path.basename(location[0])
        cfgid = cfgid or location[1]
        srcs = [os.path.join(d, sub, prjid) for d in projectdirs for sub in ("", "_PTXprint")] + [location[0]]
    else:
        prjid = prjid or names[0].split("/", 1)[0]
        srcs = [os.path.join(d, sub, prjid) for d in projectdirs for sub in ("", "_PTXprint")]
    for src in srcs:
        if os.path.isdir(src):
            copyTestProject(src, os.path.join(todir, prjid))
            break
    else:
        raise Exception("The test runs on project {}, but it isn't in {}. Use -p to say where it is.".format(
                            prjid, ", ".join(projectdirs) or "any projects directory given"))
    # other projects the config uses, such as the other side of a diglot, from beside the test's one
    for other in data.get("projects", []):
        osrcs = [os.path.join(os.path.dirname(src), other)] \
                + [os.path.join(d, sub, other) for d in projectdirs for sub in ("", "_PTXprint")]
        osrc = next((x for x in osrcs if os.path.isdir(x)), None)
        if osrc is None:
            raise Exception(f"The test also needs project {other}, but it isn't beside {prjid}.")
        copyTestProject(osrc, os.path.join(todir, other))
    return (prjid, cfgid)

def otherProjects(view):
    """ The other projects a config uses, which a test of it needs: the other sides of a diglot """
    res = set()
    for pg in getattr(view, 'polyglots', {}).values():
        if pg.prj and pg.prj != view.project.prjid:
            res.add(pg.prj)
    return sorted(res)

def readActions(fname):
    """ The actions in a tutorial (.json) or a recorded test (.zip), the view level they need (the
        one recorded with them, or for older tests the one in the test's user settings), and
        anything else in the file, so saving can keep it """
    if zipfile.is_zipfile(fname):
        with zipfile.ZipFile(fname) as zf:
            names = zf.namelist()
            name = next(n for n in names if n.endswith("test/events.json"))
            data = json.loads(zf.read(name).decode("utf-8"))
            uilevel = data.get("uilevel")
            if uilevel is None:
                ucfg = next((n for n in names if n.count("/") == 1 and n.endswith("/ptxprint_user.cfg")), None)
                if ucfg is not None:
                    config = ConfigParser(interpolation=None)
                    config.read_string(zf.read(ucfg).decode("utf-8"))
                    uilevel = config.getint("init", "userinterface", fallback=None)
    else:
        with open(fname, encoding="utf-8") as inf:
            data = json.load(inf)
        uilevel = data.get("uilevel")
    extra = {k: v for k, v in data.items() if k not in ("events", "uilevel")}
    return (data['events'], int(uilevel) if uilevel else None, extra)

def levelName(view, level):
    for r in view.builder.get_object("ls_uiLevel"):
        try:
            if int(r[1]) == level:
                return r[0]
        except ValueError:
            pass
    return str(level)

def askNote(parent, title, text="", group=None, own=None):
    """ Ask for a note's text. Returns it, or None if cancelled """
    dlg = Gtk.Dialog(title=title, transient_for=parent, modal=True)
    dlg.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "OK", Gtk.ResponseType.OK)
    if group is not None:
        group.add_window(dlg)
    if own is not None:
        own.add(dlg)        # don't record what is typed here
    tv = Gtk.TextView()
    tv.set_wrap_mode(Gtk.WrapMode.WORD)
    tv.set_size_request(400, 120)
    tv.get_buffer().set_text(text)
    lbl = Gtk.Label(label="Shown before the next step, to someone stepping through this test:", xalign=0)
    dlg.get_content_area().pack_start(lbl, False, False, 4)
    dlg.get_content_area().pack_start(tv, True, True, 4)
    dlg.show_all()
    res = None
    if dlg.run() == Gtk.ResponseType.OK:
        buf = tv.get_buffer()
        res = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)
    if own is not None:
        own.discard(dlg)
    dlg.destroy()
    return res

# The frame goes on the widget and on the button and entry inside it too, else a combo box's
# button covers it and only its corners show
_highlightcss = b"""
.ptxtest-highlight, .ptxtest-highlight button, .ptxtest-highlight entry {
    box-shadow: inset 0 0 0 2px #e01b24; }
.ptxtest-highlight { outline: 2px solid #e01b24; }
"""

class ReplayControl:
    """ A small window for watching a test replay. The label shows the next event, and its widget
        is highlighted, before it happens. Space steps (does it), S skips it, P plays or pauses. """

    def __init__(self, tester, delay):
        self.tester = tester
        self.view = tester.view
        self.timer = None
        self.highlighted = None
        css = Gtk.CssProvider()
        css.load_from_data(_highlightcss)
        mainwin = self.view.builder.get_object("mainapp_win")
        Gtk.StyleContext.add_provider_for_screen(mainwin.get_screen(), css,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.tutorial = getattr(tester, 'tutorial', False)
        self.title = "PTXprint tutorial: " + os.path.splitext(os.path.basename(tester.fname))[0] \
                        if self.tutorial else "PTXprint test replay"
        win = Gtk.Window(title=self.title)
        win.set_keep_above(True)
        win.set_transient_for(mainwin)
        # Its own window group, so a modal dialog that a step opens doesn't block Step
        self.group = Gtk.WindowGroup()
        self.group.add_window(win)
        win.set_border_width(8)
        win.set_default_size(420, -1)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        # The buttons go at the top and the text below them in a fixed size area, so a long
        # note or step never moves a button out from under the mouse.
        textbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.levelinfo = Gtk.Label(xalign=0, yalign=0)    # if the view level had to change
        self.note = Gtk.Label(xalign=0, yalign=0)     # a note in the test, shown large
        self.label = Gtk.Label(xalign=0, yalign=0)
        self.label.set_selectable(False)
        for w in (self.levelinfo, self.note, self.label):
            w.set_line_wrap(True)
            w.set_width_chars(60)
            w.set_max_width_chars(60)
            textbox.pack_start(w, False, False, 0)
        bbox = Gtk.Box(spacing=6)
        self.stepbtn = Gtk.Button(label="Step")
        self.stepbtn.set_tooltip_text("Do the next event (Space)")
        self.stepbtn.connect("clicked", self.onStep)
        self.skipbtn = Gtk.Button(label="Skip")
        self.skipbtn.set_tooltip_text("Move past the next event without doing it (S)")
        self.skipbtn.connect("clicked", self.onSkip)
        self.playbtn = Gtk.ToggleButton(label="Play")
        self.playbtn.set_tooltip_text("Do an event every few seconds (P)")
        self.playbtn.connect("toggled", self.onPlay)
        self.endbtn = Gtk.Button(label="Run to end")
        self.endbtn.connect("clicked", self.onRunToEnd)
        self.speed = Gtk.SpinButton.new_with_range(0.1, 10, 0.1)
        self.speed.set_value(delay if delay else 1.)
        for w in (self.stepbtn, self.skipbtn, self.playbtn, self.endbtn):
            bbox.pack_start(w, False, False, 0)
        bbox.pack_end(Gtk.Label(label="s/event"), False, False, 0)
        bbox.pack_end(self.speed, False, False, 0)
        box.pack_start(bbox, False, False, 0)
        # editing the test as you step through it
        ebox = Gtk.Box(spacing=6)
        self.delbtn = Gtk.Button(label="Delete step")
        self.delbtn.set_tooltip_text("Remove the next step from the test (Delete). Use it for steps "
                                     "PTXprint did by itself; removing a step you did makes the test fail.")
        self.delbtn.connect("clicked", self.onDelete)
        self.addnotebtn = Gtk.Button(label="Add note...")
        self.addnotebtn.set_tooltip_text("Add a note before the next step")
        self.addnotebtn.connect("clicked", self.onAddNote)
        self.editnotebtn = Gtk.Button(label="Edit note...")
        self.editnotebtn.set_tooltip_text("Change the note shown above")
        self.editnotebtn.connect("clicked", self.onEditNote)
        self.savebtn = Gtk.Button(label="Save tutorial...")
        self.savebtn.set_tooltip_text("Save the steps, with your changes, as a tutorial (.json) to run on "
                                      "any project. Repeated changes to the same control (e.g. typing a "
                                      "name) become one step.")
        self.savebtn.connect("clicked", self.onSave)
        for w in (self.delbtn, self.addnotebtn, self.editnotebtn):
            ebox.pack_start(w, False, False, 0)
        ebox.pack_end(self.savebtn, False, False, 0)
        box.pack_start(ebox, False, False, 0)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_size_request(-1, 160)
        scroll.add(textbox)
        box.pack_start(scroll, True, True, 0)
        self.edited = False
        win.add(box)
        # A test's window goes when the replay finishes; closing a tutorial's ends it
        win.connect("delete-event", self.onClose)
        win.connect("key-press-event", self.onKey)
        win.show_all()
        self.note.hide()
        msg = getattr(tester, 'levelmsg', None)
        if msg and self.tutorial:
            self.levelinfo.set_markup("<i>{}</i>".format(GLib.markup_escape_text(
                    msg + " " + _("Your own view comes back when you close this window."))))
        else:
            self.levelinfo.hide()
        self.stepbtn.grab_focus()           # so Space steps
        self.win = win
        self.showNext()
        if delay:
            self.playbtn.set_active(True)

    def showNext(self):
        t = self.tester
        if self.highlighted is not None:
            self.highlighted.get_style_context().remove_class("ptxtest-highlight")
            self.highlighted = None
        while t.runeventidx < len(t.runevents) and t.runevents[t.runeventidx][1] == "comment":
            t.runeventidx += 1      # comments are for whoever edits the file, not a step
        if t.runeventidx >= len(t.runevents):
            self.finished()
            return
        e = t.runevents[t.runeventidx]
        self.editnotebtn.set_sensitive(e[1] == "note")
        # count steps and notes, not comments
        shown = [i for i, x in enumerate(t.runevents) if x[1] != "comment"]
        pos = f"{shown.index(t.runeventidx) + 1}/{len(shown)}"
        if e[1] == "note":
            self.note.set_markup("<big>{}</big>".format(GLib.markup_escape_text(e[2])))
            self.note.show()
            self.label.set_text(f"Note {pos}")
        else:
            self.note.hide()
            self.label.set_text(f"Next {pos}: {t.describe(e)}")
        self.label.set_tooltip_text(json.dumps(e, ensure_ascii=False))
        w = t.eventWidget(e)
        if w is None:
            return
        self.reveal(w)
        w.get_style_context().add_class("ptxtest-highlight")
        self.highlighted = w

    def reveal(self, w):
        """ Bring the notebook pages holding w to the front """
        child = w
        p = w.get_parent()
        while p is not None:
            if isinstance(p, Gtk.Notebook):
                n = p.page_num(child)
                if n >= 0 and p.get_current_page() != n:
                    p.set_current_page(n)
            child = p
            p = p.get_parent()

    def onKey(self, win, event):
        if not self.stepbtn.get_sensitive():
            return False
        if self.speed.has_focus() and event.keyval not in (Gdk.KEY_space,):
            return False        # typing a speed
        if event.keyval == Gdk.KEY_space:
            self.onStep()
        elif event.keyval in (Gdk.KEY_s, Gdk.KEY_S):
            self.onSkip()
        elif event.keyval == Gdk.KEY_Delete:
            self.onDelete()
        elif event.keyval in (Gdk.KEY_p, Gdk.KEY_P):
            self.playbtn.set_active(not self.playbtn.get_active())
        else:
            return False
        return True

    def setEdited(self):
        self.edited = True
        self.win.set_title(self.title + " (edited, not saved)")

    def onClose(self, *a):
        if not self.tutorial:
            return True         # a test's replay window stays until the test ends
        if self.edited:
            self.offerSave()
        self.pausePlay()
        if self.highlighted is not None:
            self.highlighted.get_style_context().remove_class("ptxtest-highlight")
            self.highlighted = None
        self.tester.restoreLevel()
        self.view.replayer = None
        self.win.destroy()
        return True

    def onDelete(self, *a):
        t = self.tester
        if t.runeventidx >= len(t.runevents):
            return
        del t.runevents[t.runeventidx]
        self.setEdited()
        self.showNext()

    def pausePlay(self):
        if self.playbtn.get_active():
            self.playbtn.set_active(False)

    def onAddNote(self, *a):
        self.pausePlay()
        idx = self.tester.runeventidx       # where it goes, whatever happens while the dialog is open
        text = askNote(self.win, "Add a note before the next step", group=self.group)
        if text is not None and text.strip():
            self.tester.runevents.insert(idx, ["", "note", text.strip()])
            if self.tester.runeventidx > idx:
                self.tester.runeventidx += 1
            self.setEdited()
            self.showNext()

    def onEditNote(self, *a):
        t = self.tester
        if t.runeventidx >= len(t.runevents) or t.runevents[t.runeventidx][1] != "note":
            return
        self.pausePlay()
        e = t.runevents[t.runeventidx]
        text = askNote(self.win, "Edit the note", text=e[2], group=self.group)
        if text is None:
            return
        try:
            idx = next(i for i, x in enumerate(t.runevents) if x is e)    # the note we opened
        except StopIteration:
            return
        if text.strip():
            t.runevents[idx] = [e[0], "note", text.strip()]
        else:
            del t.runevents[idx]                # an emptied note goes
            if t.runeventidx > idx:
                t.runeventidx -= 1
        self.setEdited()
        self.showNext()

    def offerSave(self):
        """ PTXprint is closing with unsaved edits to the test """
        dlg = Gtk.MessageDialog(transient_for=self.win, modal=True, message_type=Gtk.MessageType.QUESTION,
                                buttons=Gtk.ButtonsType.YES_NO, text="Save your changes to the test?")
        self.group.add_window(dlg)
        res = dlg.run()
        dlg.destroy()
        if res == Gtk.ResponseType.YES:
            self.onSave()

    def onSave(self, *a):
        self.pausePlay()
        dlg = Gtk.FileChooserDialog(title="Save the tutorial", transient_for=self.win,
                                    action=Gtk.FileChooserAction.SAVE)
        dlg.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Save", Gtk.ResponseType.OK)
        dlg.set_do_overwrite_confirmation(True)
        filt = Gtk.FileFilter()
        filt.set_name("Tutorials (*.json)")
        filt.add_pattern("*.json")
        dlg.add_filter(filt)
        src = self.tester.fname
        dlg.set_current_folder(os.path.dirname(src))
        dlg.set_current_name(os.path.splitext(os.path.basename(src))[0] + ".json")
        self.group.add_window(dlg)
        fname = dlg.get_filename() if dlg.run() == Gtk.ResponseType.OK else None
        dlg.destroy()
        if fname is None:
            return
        if not fname.lower().endswith(".json"):
            fname += ".json"
        merged = self.tester.saveTutorial(fname)
        self.edited = False
        self.win.set_title(self.title)
        self.label.set_text(f"Saved {os.path.basename(fname)}"
                            + (f" ({merged} repeated changes merged)" if merged else ""))

    def onSkip(self, *a):
        if self.tester.runeventidx >= len(self.tester.runevents):
            return
        self.tester.skipOne()
        self.showNext()

    def onStep(self, *a):
        if self.tester.runeventidx >= len(self.tester.runevents) or not self.tester.ready():
            return
        self.tester.replayOne()
        GLib.idle_add(self.afterStep)     # after any signal the step emitted (see GtkTester._later)

    def afterStep(self):
        self.showNext()
        if self.stepbtn.get_sensitive():
            self.stepbtn.grab_focus()
        return False

    def onPlay(self, btn):
        if btn.get_active():
            btn.set_label("Pause")
            self.schedule()
        else:
            btn.set_label("Play")
            if self.timer is not None:
                GLib.source_remove(self.timer)
                self.timer = None

    def schedule(self):
        delay = self.speed.get_value()
        t = self.tester
        if t.runeventidx < len(t.runevents) and t.runevents[t.runeventidx][1] == "note":
            delay = max(delay, 2 + len(t.runevents[t.runeventidx][2]) / 15)    # time to read it
        self.timer = GLib.timeout_add(int(delay * 1000), self.onTick)

    def onTick(self):
        self.timer = None
        if not self.tester.ready():         # the last step is still being handled
            self.timer = GLib.timeout_add(50, self.onTick)
            return False
        self.onStep()
        if self.playbtn.get_active() and self.tester.runeventidx < len(self.tester.runevents):
            self.schedule()
        return False

    def onRunToEnd(self, *a):
        self.speed.set_value(0.1)
        self.playbtn.set_active(True)

    def finished(self):
        self.note.hide()
        if self.timer is not None:
            GLib.source_remove(self.timer)
            self.timer = None
        self.tester.finishReplay()
        n = len(self.tester.errors)
        k = len(self.tester.skipped)
        actions = sum(1 for e in self.tester.runevents if e[1] not in ("note", "comment"))
        if self.tutorial:
            self.label.set_text("That's the end of the tutorial." + (f" ({n} steps could not be done.)" if n else ""))
        else:
            self.label.set_text(f"Replayed {actions - k} steps"
                                + (f", skipped {k}" if k else "")
                                + (f", {n} could not be replayed" if n else "")
                                + ". Close PTXprint to see the result.")
        for w in (self.stepbtn, self.skipbtn, self.playbtn, self.endbtn, self.speed,
                  self.delbtn, self.editnotebtn):
            w.set_sensitive(False)
        if self.edited:
            self.label.set_text(self.label.get_text() + " Your edits are not saved yet.")


class RecordControl:
    """ A small window shown while recording a test: how many events so far, Add note and Stop """

    def __init__(self, tester):
        self.tester = tester
        self.view = tester.view
        mainwin = self.view.builder.get_object("mainapp_win")
        win = Gtk.Window(title="Recording PTXprint test")
        win.set_keep_above(True)
        win.set_transient_for(mainwin)
        # Its own window group, so Add note and Stop still work while a modal dialog is open
        self.group = Gtk.WindowGroup()
        self.group.add_window(win)
        win.set_border_width(8)
        box = Gtk.Box(spacing=6)
        self.count = Gtk.Label(label="Recording")
        box.pack_start(self.count, False, False, 0)
        notebtn = Gtk.Button(label="Add note...")
        notebtn.set_tooltip_text("Add a note that someone stepping through the test (e.g. as a tutorial) sees before the next step")
        notebtn.connect("clicked", self.onAddNote)
        stopbtn = Gtk.Button(label="Stop recording")
        stopbtn.connect("clicked", self.onStop)
        box.pack_end(stopbtn, False, False, 0)
        box.pack_end(notebtn, False, False, 0)
        win.add(box)
        win.connect("delete-event", lambda *a: True)
        win.show_all()
        self.win = win
        tester.ownwindows.add(win)
        self.timer = GLib.timeout_add(1000, self.update)

    def update(self):
        n = len(self.tester.events)
        self.count.set_text(f"Recording: {n} event{'' if n == 1 else 's'}")
        return True

    def onAddNote(self, btn):
        text = askNote(self.win, "Add a note to the test", group=self.group, own=self.tester.ownwindows)
        if text is not None:
            self.tester.addNote(text)
            self.update()

    def onStop(self, btn):
        if getattr(self.view, 'testing', None) is self.tester:
            self.view.finalise_testing()

    def close(self):
        if self.timer is not None:
            GLib.source_remove(self.timer)
            self.timer = None
        self.tester.ownwindows.discard(self.win)
        self.win.destroy()
