
import gi
gi.require_version("Gtk", '3.0')
from gi.repository import Gtk, Gdk, GObject, GLib
import os, sys, zipfile, json, tempfile, traceback, time, shutil
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
    'changed': ("ComboBox", "Entry"),
    'color-set': ("ColorButton",),
    'change-current-page': ("Notebook",),
    'value-changed': ("SpinButton",),
    # 'state-set': ("Switch",),
    'row-activated': ("TreeView",),
}

class GtkTester:
    def __init__(self, fname, view, full_archive=False):
        self.fname = fname
        self.view = view
        self.events = []
        self.currid = None
        self.usedids = set()
        self.projects = {}
        self.paused = False
        self.lastevent = None
        self.errors = []
        self.skipped = []
        self.full_archive = full_archive
        self.setid(view.project, view.cfgid)
        if self.full_archive:
            self.view.createArchive(fname, for_test=True, nobuild=True)
            self.zip = self.view.zf
        else:
            self.zip = None

    @classmethod
    def recordFromUser(cls, view):
        """ Ask where to save a test recording and start it. Returns the tester, or None """
        zip_file = view.fileChooser(_("Select the location and name for the test archive file"),
                filters={"ZIP files": {"pattern": "*.zip", "mime": "application/zip"}},
                multiple=False, folder=False, save=True,
                basedir=os.path.join(view.project.printPath(view.cfgid), '..'))
        if zip_file is None:
            return None
        res = cls(str(zip_file[0]), view, full_archive=True)
        res.startRecording()
        return res

    def startRecording(self):
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

    def stopRecording(self):
        for obj, signal_name, hook_id in getattr(self, 'hook_ids', []):
            GObject.remove_emission_hook(obj, signal_name, hook_id)
        self.hook_ids = []
        if getattr(self, 'recordcontrol', None) is not None:
            self.recordcontrol.close()
            self.recordcontrol = None

    def addNote(self, text, widget=""):
        """ A note for someone stepping through the test, e.g. as a tutorial. Replays ignore it. """
        text = text.strip()
        if text:
            self.events.append([widget or "", "note", text])
            self.lastevent = None

    def emission_hook(self, w, *a):     # sigid, detail, self, *a):
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
            self.events.append(e)
            self.lastevent = e

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def setid(self, project, cfgid):
        self.currid = (project, cfgid)

    def mkzipdir(self, name):
        if not name.endswith("/"):
            name += "/"
        try:
            self.zip.getinfo(name)
        except KeyError:
            self.zip.mkdir(name)

    def writefile(self, name, side, project, cfgid=None):
        if cfgid is None:
            fname = os.path.join(project.path, name)
        else:
            fname = os.path.join(project.configs[cfgid].path, name)
        outpath = "{}/{}{}/{}".format(side, project.prjid, "/"+cfgid if cfgid else "", name)
        exists = True
        try:
            self.zip.getinfo(outpath)
        except KeyError:
            exists = False
        if os.path.exists(fname) and not exists:
            self.zip.write(fname, outpath)
            return True
        return False

    def finalise(self):
        self.stopRecording()
        if self.zip is None or self.paused:
            return
        project = self.currid[0]
        self.pause()
        self.mkzipdir("{}/test".format(project.prjid))

        if self.full_archive:
            after_archive = self.view.createArchive(in_memory=True, for_test=True, nobuild=True)
            self.view.zf.close()

            initial_files = {name: self.zip.read(name) for name in self.zip.namelist()}

            after_archive.seek(0)
            with zipfile.ZipFile(after_archive) as z_final:
                final_files = {name: z_final.read(name)
                            for name in z_final.namelist()}

            modified_files = []
            deleted_files = []

            for name, content in final_files.items():
                if name not in initial_files or initial_files[name] != content:
                    modified_files.append(name)
                    self.zip.writestr("{}/test/modified_files/{}".format(project.prjid, name), content)
            testdir = "{}/test/".format(project.prjid)
            for name in initial_files:
                if name not in final_files and not name.startswith(testdir):
                    deleted_files.append(name)

            self.zip.writestr("{}/test/deleted_files.txt".format(project.prjid), '\n'.join(deleted_files))
        else:
            # not implemented right now, but here it could be possible to have a more minimal test eg comparing only cfg files
            raise NotImplementedError

        events = json.dumps({"events": self.events, "uilevel": getattr(self, 'uilevel', self.view.uilevel)},
                            ensure_ascii=False, indent=4, cls=CustomJSONEncoder)
        self.zip.writestr("{}/test/events.json".format(project.prjid), events)
        self.zip.close()

    def setuprun(self, fname, view):
        self.pause()
        if fname is not None:
            self.fname = os.path.abspath(fname)
        self.runevents, self.runuilevel, self.runextra = readActions(fname)
        self.runeventidx = 0

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
            return {n: zf.read(n) for n in zf.namelist() if not n.endswith("/")}

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
        return f"{label}: {' '.join(str(x) for x in e[1:])}"

    def _note(self, w, *a):
        return False

    def _comment(self, w, *a):
        """ A comment for whoever edits the test or tutorial: never shown, never replayed """
        return False

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
        inflight = getattr(self, 'inflight', [])
        if not inflight:
            return True
        waiting = self.openDialogs() - self.responded
        return all(waiting - before for before in inflight)

    def _replay(self, e):
        """ Replay one event. Returns True if it was emitted later, so callers come back after it """
        w = e[0]
        if e[1] == "set":
            self.view.set(w, e[2])
            return False
        elif e[1] == "signal":
            widget = self.view.builder.get_object(w)
            if widget is None:
                raise KeyError(f"No widget called {w}")
            self._later(widget.emit, e[2], *e[3:])
            return True
        m = getattr(self, "_"+e[1], None)
        if m is None:
            raise KeyError(f"Unknown event type {e[1]}")
        return m(w, *e[2:])

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
                self.view.styleEditor.selectMarker(a[2])
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

def load_project_from_archive(zf, dir_to_extract=None):
    """
    zf is an open zipfile, containing an archive of a project created using the createArchive method
    Will be extracted to dir_to_extract if specified, to a temporary directory if not
    """
    madedir = not dir_to_extract
    if madedir:
        dir_to_extract = tempfile.mkdtemp(prefix="ptxtest_")
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
    return project

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
