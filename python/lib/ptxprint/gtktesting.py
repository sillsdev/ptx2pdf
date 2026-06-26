
from gi.repository import Gtk, GObject, GLib
import io, os, zipfile, json, shutil, tempfile, filecmp
import subprocess
from configparser import ConfigParser
from difflib import context_diff
from pathlib import Path
from glob import glob

from ptxprint.usxutils import simple_parse
from ptxprint.project import Project, ProjectDir


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return super().default(obj)

class GtkTester:
    def __init__(self, fname, view, full_archive=False):
        self.fname = fname
        self.view = view
        self.events = []
        self.currid = None
        self.usedids = set()
        self.projects = {}
        self.paused = False
        self.full_archive = full_archive
        if self.full_archive:
            self.view.createArchive(fname, for_test=True)
            self.zip = self.view.zf
        else:
            self.zip = None

    def addEvent(self, w, signal, t, val, a):
        ''' events are widget, type="signal", signal, parms; type="set", val '''
        if self.paused:
            return
        e = None
        laste = None
        if w in ("button",):
            return
        if val is not None and not w.startswith("btn_"):
            e = (w, 'set', val)
            if e == laste:
                e = None
            else:
                laste = e
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
        project = self.currid[0]
        if self.zip is None or self.paused:
            return

        self.pause()
        self.mkzipdir("{}/test".format(project.prjid))

        if self.full_archive:
            after_archive = self.view.createArchive(in_memory=True)

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
        for name in initial_files:
            if name not in final_files and 'test' not in name:
                deleted_files.append(name)

        self.zip.writestr("{}/test/deleted_files.txt".format(project.prjid), '\n'.join(deleted_files))

        events = json.dumps({"events": self.events}, ensure_ascii=False, indent=4, cls=CustomJSONEncoder)
        self.zip.writestr("{}/test/events.json".format(project.prjid), events)
        self.zip.close()

    def setuprun(self, fname, view):
        self.pause()
        projects = {}
        self.fname = fname
        self.runzip = zipfile.ZipFile(fname, "r")
        for fi in self.runzip.infolist():
            if fi.filename.endswith("events.json"):
                with self.runzip.open(fi) as src:
                    self.runevents = json.load(src)['events']

        self.runeventidx = 0

    def run_action(self, noclose):
        while self.runeventidx < len(self.runevents):
            e = self.runevents[self.runeventidx]
            # print(f"{self.runeventidx}: {e}")
            self.runeventidx += 1
            w = e[0]
            goround = False
            if e[1] == "set":
                self.view.set(w, e[2])
                goround = False
            elif e[1] == "signal":
                signal = e[2]
                widget = self.view.builder.get_object(w)
                widget.emit(signal, *e[3:])
                goround = True
            else:
                m = getattr(self, "_"+e[1], None)
                if m is not None:
                    goround = m(w, *e[2:])
            if goround and self.runeventidx < len(self.runevents):
                GLib.idle_add(self.run_action, noclose)
            if self.runeventidx == len(self.runevents):
                self.view.onDestroy(None)

    def run_finalise(self):
        # unpack the test zipfile to a temp location, then modify and delete files to allow use as a reference
        reference_tmpdir = tempfile.mkdtemp()
        with zipfile.ZipFile(self.fname) as z_initial:
            z_initial.extractall(reference_tmpdir)

        modified_files_dir = Path(reference_tmpdir) / self.view.project.prjid / "test" / "modified_files"
        for source_path in modified_files_dir.rglob("*"):
            if source_path.is_file():
                dest_path = Path(reference_tmpdir) / source_path.relative_to(modified_files_dir)
                try:
                    shutil.copyfile(str(source_path), str(dest_path))
                except Exception as e:
                    print(f"Error moving {source_path}: {e}")

        deleted_files_path = Path(reference_tmpdir) / self.view.project.prjid / "test" / "deleted_files.txt"
        with open(deleted_files_path) as f:
            deleted_files = [f.strip() for f in f.readlines()]
        for file in deleted_files:
            (Path(reference_tmpdir) / file).unlink()

        # also, remove the unique.id file and local/ dir created when running the test since this doesn't exist in the reference
        if os.path.isfile(os.path.join(self.view.project.path, "unique.id")):
            os.remove(os.path.join(self.view.project.path, "unique.id"))
        if os.path.isdir(os.path.join(self.view.project.path, "local")):
            shutil.rmtree(os.path.join(self.view.project.path, "local"))

        # reference is prepared, now we just run a diff
        return self.prepare_diff_report(self.view.project.path, str(Path(reference_tmpdir) / self.view.project.prjid))

    def prepare_diff_report(self, testdir, refdir):
        diff_results = {"test": [], "ref": [], "diff": [], "cfg": [], "sty": []}
        comparison = filecmp.dircmp(testdir, refdir)

        def collect_diff(cmp_obj):
            for file in cmp_obj.diff_files:
                diff_results["diff"].append((str(Path(cmp_obj.left) / file), str(Path(cmp_obj.right) / file)))
            for file in cmp_obj.left_only:
                diff_results["test"].append(str(Path(cmp_obj.left) / file))
            for file in cmp_obj.right_only:
                diff_results["ref"].append(str(Path(cmp_obj.right) / file))
            for subdir_cmp in cmp_obj.subdirs.values():
                collect_diff(subdir_cmp)

        collect_diff(comparison)
        for f in diff_results["diff"]:
            if f[0].endswith('.cfg'):
                with open(f[0]) as f0, open(f[1]) as f1:
                    cfg_diff = self.compare_cfg(f0, f1)
                if cfg_diff:
                    diff_results['cfg'] = cfg_diff

            elif f[0].endswith('.sty'):
                with open(f[0]) as f0, open(f[1]) as f1:
                    sty_diff = self.compare_sty(f0, f1)
                if sty_diff:
                    diff_results['sty'] = sty_diff
        diff_results["diff"] = [f for f in diff_results["diff"] if not f[0].endswith('.cfg') and not f[0].endswith('.sty')]
        return diff_results




#### special handlers
    def s_rowactivated(self, w, signal, t, val, p, col, *a):
        tv = self.view.builder.get_object(w)
        coli = tv.get_columns().index(col)
        res = [w, "rowactivated", str(p), str(coli)]
        return res

    def _rowactivated(self, w, *a):
        widget = self.view.builder.get_object(w)
        p = Gtk.TreePath.new_from_string(a[0])
        if w == "tv_Styles":
            sel = widget.get_selection()
            sel.select_path(p)
            sel.emit("changed")
        else:
            col = widget.get_columns()[int(a[1])]
            parms = [p, col]
            widget.emit("row-activated", *parms)
        return True         # we emitted a signal so go round

    def compare_cfg(self, old, new, **kw):
        options_to_ignore = ["gitversion", "config"]
        res = []
        oldc = ConfigParser()
        oldc.read_file(old)
        newc = ConfigParser()
        newc.read_file(new)
        olds = set(oldc.sections())
        news = set(newc.sections())
        diffs = olds.difference(news)
        if len(diffs):
            res.append(f"Differences in sections: {', '.join(sorted(diffs))}")
        for s in olds:
            if s not in news:
                continue
            oldo = set(oldc.options(s))
            newo = set(newc.options(s))
            diffs = oldo.difference(newo)
            if len(diffs):
                res.append(f"Differences in options in section {s}: {', '.join(sorted(diffs))}")
            for o in oldo:
                if o not in newo:
                    continue
                oldv = oldc.get(s, o)
                newv = newc.get(s, o)
                if oldv != newv and o not in options_to_ignore:
                    res.append(f"{s}/{o}: {oldv} -> {newv}")
        return res

    def compare_sty(self, old, new, **kw):
        res = []
        olds = simple_parse(old)
        news = simple_parse(new)
        newm = set(news.keys())
        oldm = set(olds.keys())
        diffs = newm.difference(oldm)
        if len(diffs):
            res.append(f"Different markers: {', '.join(sorted(diffs))}")
        for m, r in news.items():
            if m not in oldm:
                continue
            o = olds[m]
            newk = set(r.keys())
            oldk = set(o.keys())
            diffs = newk.difference(oldk)
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
    if not dir_to_extract:
        dir_to_extract = tempfile.mkdtemp()
    zf.extractall(dir_to_extract)
    cfg_path = list(Path(dir_to_extract).glob("*/shared/ptxprint/*/ptxprint.cfg"))
    if len(cfg_path) != 1:
        raise Exception("1 cfg file was expected in the archive but {} were found.".format(len(cfg_path)))
    prjid = cfg_path[0].parts[3]
    project_dir = ProjectDir(prjid, None, dir_to_extract)
    project = Project(project_dir)
    return project
