
from gi.repository import Gtk, GObject, GLib
import os, zipfile, json, shutil, configparser
from ptxprint.usxutils import simple_parse
from difflib import context_diff

class GtkTester:
    def __init__(self, fname, view):
        self.fname = fname
        self.view = view
        self.events = []
        self.currid = None
        self.usedids = set()
        self.projects = {}
        self.paused = False
        self.zip = None

    def addEvent(self, w, signal, t, val, a):
        ''' events are widget, type="signal", signal, parms; type="set", val '''
        if self.paused:
            return
        e = None
        laste = None
        if val is not None and not w.startswith("btn_"):
            e = (w, 'set', val)
            if e == laste:
                e = None
            else:
                laste = e
            if self.currid is not None and self.currid not in self.usedids:
                self.addid(*self.currid)
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

    def addid(self, project, cfgid):
        if self.zip is None and self.fname is not None:
            self.zip = zipfile.ZipFile(self.fname, mode="w", compression=zipfile.ZIP_BZIP2)
            self.zip.mkdir("before")
        if self.zip is None:
            return
        self.zip.mkdir("before/{}".format(project.prjid))
        for a in ("Settings.xml", "PTXSettings.xml"):
            fname = os.path.join(project.path, a)
            if os.path.exists(fname):
                self.zip.write(fname, "before/{}/{}".format(project.prjid, a))
                break
        for a in ("ptxprint.cfg", "ptxprint.sty"):
            self.writefile(a, "before", project, cfgid)
        self.projects[project.prjid] = project

    def writefile(self, name, side, project, cfgid):
        fname = os.path.join(project.configs[cfgid].path, name)
        if os.path.exists(fname):
            self.zip.write(fname, "{}/{}/{}/{}".format(side, project.prjid, cfgid, name))

    def finalise(self):
        if self.zip is None:
            return
        self.zip.mkdir("after")
        for f in self.zip.namelist():
            if not f.startswith("before/"):
                continue
            b = f.split("/", 3)
            if len(b) < 4:
                continue
            project = self.projects[b[1]]
            cfgid = b[2]
            if "after/{}".format(b[1]) not in self.zip.namelist():
                self.zip.mkdir("after/{}".format(b[1]))
            if "after/{}/{}".format(b[1], b[2]) not in self.zip.namelist():
                self.zip.mkdir("after/{}/{}".format(b[1], b[2]))
            a = b[3]
            self.writefile(a, "after", project, cfgid)
        events = json.dumps({"events": self.events}, ensure_ascii=False, indent=4)
        self.zip.writestr("events.json", events)
        self.zip.close()
        self.pause()

    def setuprun(self, fname, view):
        self.pause()
        projects = {}
        self.runzip = zipfile.ZipFile(fname, "r")
        for fi in self.runzip.infolist():
            if fi.filename == "events.json":
                with self.runzip.open(fi) as src:
                    self.runevents = json.load(src)['events']
            if not fi.filename.startswith("before/") or fi.is_dir():
                continue
            b = fi.filename.split("/", 3)[1:]
            f = b.pop()
            p = None; c = None
            if len(b) > 1:
                p, c = b[-2:]
            elif len(b):
                p = b[-1]
            if p is not None:
                if p not in projects:
                    projects[p] = view.prjTree.findProject(p)
                outpath = projects[p].path
                if c is not None:
                    outpath = os.path.join(outpath, "shared", "ptxprint", c)
                outpath = os.path.join(outpath, f)
                with self.runzip.open(fi) as src, open(outpath, "wb") as tgt:
                    shutil.copyfileobj(src, tgt)
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
                if w == "b_close" and signal == "clicked":
                    continue
                widget = self.view.builder.get_object(w)
                widget.emit(signal, *e[3:])
                goround = True
            else:
                m = getattr(self, "_"+e[1], None)
                if m is not None:
                    goround = m(w, *e[2:])
            if goround and self.runeventidx < len(self.runevents):
                GLib.idle_add(self.run_action, noclose)
                return

    def run_finalise(self):
        results = {}
        projects = {}
        for fi in self.runzip.infolist():
            if not fi.filename.startswith("after/") or fi.is_dir():
                continue
            b = fi.filename.split("/", 3)[1:]
            if len(b) < 4:
                continue        # only want configuration files
            ext = os.path.splitext(b[3])
            m = self.getattr("compare_"+ext[1:].lower(), None)
            if m is None:
                m = self.diffcompare
            if b[1] not in projects:
                projects[b[1]] = self.view.prjTree.findProject(b[1])
            outpath = os.path.join(projects[b[1]].path, "shared", "ptxprint", b[2], b[3])
            fpin = open(outpath, encoding="utf-8")
            zfbin = self.runzip.open(fi)
            zfin = io.TextIOWrapper(zfbin, encoding="utf-8")
            results["{1}/{2}/{3}".format(*b[3])] = m(fpin, zfin, filename=b[3])
            zfin.close()
            fpin.close()
        return results

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
                if oldv != newv:
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
        for m, r in newm.items():
            if m not in oldm:
                continue
            o = oldm[m]
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


